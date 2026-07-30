# Hardened Kubernetes on Azure Linux
### A Production Deployment Guide for Enterprise Agentic AI Workloads

> **Scope.** This guide builds a self-managed, CIS/NSA-CISA-aligned Kubernetes cluster on **Azure Linux 3.0** (the Microsoft-maintained, FedRAMP-certified successor to CBL-Mariner), consisting of a minimum of **two nodes** — one control-plane node and one worker node — sized and hardened for running **agentic AI workloads** (LLM-driven agents that call tools, execute generated code, and reach external APIs) in an enterprise setting. Every technical claim in this document is grounded in current (2025–2026) upstream documentation, CNCF projects, and Microsoft Learn/Tech Community sources; see **Appendix F — Sources** for citations.

---

## Table of Contents

1. [Executive Summary & Design Principles](#1-executive-summary--design-principles)
2. [Reference Architecture](#2-reference-architecture)
3. [Threat Model for Agentic Workloads](#3-threat-model-for-agentic-workloads)
4. [Prerequisites & Azure Infrastructure Layout](#4-prerequisites--azure-infrastructure-layout)
5. [Host OS Provisioning & Hardening (Azure Linux 3.0)](#5-host-os-provisioning--hardening-azure-linux-30)
6. [Container Runtime Installation (containerd)](#6-container-runtime-installation-containerd)
7. [Kubernetes Package Installation](#7-kubernetes-package-installation)
8. [Bootstrapping the Control Plane with kubeadm](#8-bootstrapping-the-control-plane-with-kubeadm)
9. [Joining the Worker Node](#9-joining-the-worker-node)
10. [CNI: Cilium (eBPF, encryption, egress control)](#10-cni-cilium-ebpf-encryption-egress-control)
11. [Identity, Authentication & RBAC](#11-identity-authentication--rbac)
12. [Secrets Management & Encryption at Rest](#12-secrets-management--encryption-at-rest)
13. [Pod & Workload Hardening](#13-pod--workload-hardening)
14. [Sandboxing Agentic Workloads (gVisor / Kata Containers)](#14-sandboxing-agentic-workloads-gvisor--kata-containers)
15. [Policy-as-Code with Kyverno](#15-policy-as-code-with-kyverno)
16. [Supply Chain Security](#16-supply-chain-security)
17. [Runtime Security & Observability](#17-runtime-security--observability)
18. [Optional: GPU Nodes for Local Inference](#18-optional-gpu-nodes-for-local-inference)
19. [Backup, Restore & Disaster Recovery](#19-backup-restore--disaster-recovery)
20. [Patching & Lifecycle Management](#20-patching--lifecycle-management)
21. [Compliance Validation (kube-bench / Kubescape)](#21-compliance-validation-kube-bench--kubescape)
22. [Appendix A — Full Reference Manifests](#appendix-a--full-reference-manifests)
23. [Appendix B — Variable Reference](#appendix-b--variable-reference)
24. [Appendix C — Hardening Checklist](#appendix-c--hardening-checklist)
25. [Appendix D — Upgrade Runbook](#appendix-d--upgrade-runbook)
26. [Appendix E — Troubleshooting](#appendix-e--troubleshooting)
27. [Appendix F — Sources](#appendix-f--sources)

---

## 1. Executive Summary & Design Principles

Agentic AI workloads are qualitatively different from ordinary microservices: they interpret natural language, generate and often **execute their own code**, invoke external tools/APIs, and act with a degree of autonomy. This changes the security calculus for Kubernetes in three ways:

1. **The container boundary is not sufficient.** An LLM agent that runs arbitrary generated code inside a standard `runc` container shares the host kernel; a kernel exploit in generated code becomes a host compromise (MITRE ATT&CK T1611). This is not theoretical — the pre-auth RCE in Langflow (CVE-2025-3248, CVSS 9.8, added to CISA's KEV catalog May 2025) was caused by exactly this pattern: unauthenticated code executed via `exec()` with no sandbox isolation.
2. **Egress is the new perimeter.** Agents routinely call out to LLM providers, tool APIs, and package registries. Traditional "block everything inbound" perimeter models say nothing about controlling *outbound* data exfiltration paths that an agent (or a prompt-injected agent) might use.
3. **Secrets sprawl.** Agents need API keys (LLM providers, vector DBs, internal services) at runtime, which makes centralized, rotated, audited secret delivery non-negotiable.

This guide's design principles, applied throughout:

- **Defense in depth** — host hardening + Kubernetes hardening + workload sandboxing + policy enforcement + runtime detection, so no single control failure yields full compromise.
- **Least privilege everywhere** — RBAC, NetworkPolicy default-deny, seccomp/capabilities drop, minimal node OS footprint.
- **Immutable, measured infrastructure** — Azure Trusted Launch (Secure Boot + vTPM), signed images, `kubeadm`-managed static control plane manifests instead of hand-rolled `systemd` units.
- **Current, actively maintained stack only** — Kubernetes with `kubeadm` v1beta4 config, containerd 2.x, Cilium (eBPF, CNCF graduated), Kyverno (CNCF incubating), Falco (CNCF graduated), all installed from their official 2025/2026 release channels.
- **Two-node minimum, HA-ready design** — the requested topology (1 control-plane + 1 worker) is explicitly a **non-HA baseline**. Every control-plane configuration below is written so that adding two more control-plane nodes later (recommended for real production HA and etcd quorum) is a config-file change, not a redesign. See [Appendix D](#appendix-d--upgrade-runbook).

---

## 2. Reference Architecture

```
                                   ┌───────────────────────────────────────────┐
                                   │              Azure Subscription             │
                                   │  ┌─────────────────────────────────────┐  │
                                   │  │   VNet 10.60.0.0/16                  │  │
                                   │  │                                     │  │
      Admin workstation            │  │  ┌───────────────┐                  │  │
      (kubectl, SSH) ──── Bastion ─┼──┼─▶│ AzureBastionSubnet│               │  │
                                   │  │  └───────────────┘                  │  │
                                   │  │                                     │  │
                                   │  │  ┌────────────────── nsg-cp ──────┐ │  │
                                   │  │  │  cp-subnet 10.60.1.0/24        │ │  │
                                   │  │  │  ┌──────────────────────────┐ │ │  │
                                   │  │  │  │  node-cp-01              │ │ │  │
                                   │  │  │  │  Azure Linux 3.0 (Trusted│ │ │  │
                                   │  │  │  │  Launch, vTPM, SecureBoot│ │ │  │
                                   │  │  │  │  kube-apiserver          │ │ │  │
                                   │  │  │  │  kube-controller-manager │ │ │  │
                                   │  │  │  │  kube-scheduler          │ │ │  │
                                   │  │  │  │  etcd (local, encrypted) │ │ │  │
                                   │  │  │  │  containerd + Cilium     │ │ │  │
                                   │  │  │  └──────────────────────────┘ │ │  │
                                   │  │  └────────────────────────────────┘ │  │
                                   │  │                                     │  │
                                   │  │  ┌────────────────── nsg-wk ──────┐ │  │
                                   │  │  │  worker-subnet 10.60.2.0/24    │ │  │
                                   │  │  │  ┌──────────────────────────┐ │ │  │
                                   │  │  │  │  node-wk-01              │ │ │  │
                                   │  │  │  │  Azure Linux 3.0         │ │ │  │
                                   │  │  │  │  kubelet + containerd    │ │ │  │
                                   │  │  │  │  RuntimeClasses:         │ │ │  │
                                   │  │  │  │    runc  (trusted infra) │ │ │  │
                                   │  │  │  │    gvisor (agent tools)  │ │ │  │
                                   │  │  │  │    kata (code exec)      │ │ │  │
                                   │  │  │  │  Falco, GPU Operator*    │ │ │  │
                                   │  │  │  └──────────────────────────┘ │ │  │
                                   │  │  └────────────────────────────────┘ │  │
                                   │  └─────────────────────────────────────┘  │
                                   │                                             │
                                   │  Azure Key Vault  (etcd KMS + agent secrets)│
                                   │  Azure Storage (Velero + etcd snapshots)    │
                                   │  Azure Monitor / Log Analytics (audit sink) │
                                   └───────────────────────────────────────────┘
                                   * GPU Operator only if the worker has an NVIDIA-family Azure VM SKU (e.g. NCads_H100_v5)
```

**Cluster layer stack (2026 current):**

| Layer | Component | Version family used in this guide |
|---|---|---|
| Host OS | Azure Linux 3.0 (kernel 6.6, systemd 255) | latest 3.0.x |
| Container runtime | containerd (via `moby-containerd`) | 2.x, `SystemdCgroup=true`, cgroup v2 |
| Cluster bootstrapper | kubeadm | v1beta4 config API |
| Kubernetes | kube-apiserver / controller-manager / scheduler / kubelet / kubectl | current stable minor (pin explicitly, e.g. `v1.34.x`) |
| CNI | Cilium (eBPF, kube-proxy replacement) | 1.17.x |
| Sandbox runtimes | gVisor (`runsc`), Kata Containers | latest stable |
| Policy engine | Kyverno | latest (CNCF incubating, graduated 2024) |
| Runtime security | Falco (eBPF probe) | latest |
| Secrets | Secrets Store CSI Driver + Azure Key Vault provider, Entra Workload ID | latest |
| Backup | Velero + etcd snapshot | latest |
| GPU (optional) | NVIDIA GPU Operator | latest |

---

## 3. Threat Model for Agentic Workloads

| Threat | Example | Primary control(s) in this guide |
|---|---|---|
| Agent executes attacker-controlled or self-generated code that attempts a container/kernel escape | Prompt-injected agent runs a Python "helper script" containing a kernel exploit | §14 gVisor/Kata `RuntimeClass`, seccomp, non-root, capability drop |
| Agent exfiltrates secrets or internal data to an external endpoint | Compromised MCP/tool server posts credentials to attacker domain | §10 Cilium default-deny egress + FQDN allow-lists, §17 Falco egress rules |
| Credential/API-key sprawl in manifests or images | Hardcoded OpenAI/Azure OpenAI key in a ConfigMap | §12 Key Vault CSI + Workload Identity, no plaintext secrets in Git |
| Supply-chain compromise of an agent framework image | Malicious PyPI/npm dependency baked into the agent image | §16 image signing (cosign), SBOM, Kyverno `verifyImages`, registry allow-list |
| Lateral movement after a single pod is compromised | Compromised agent pod scans/attacks other namespaces | §10/§13 NetworkPolicy default-deny, namespace isolation, PSA `restricted` |
| Privilege escalation via the Kubernetes API itself | Over-privileged ServiceAccount token stolen from a pod | §11 least-privilege RBAC, no `automountServiceAccountToken` by default |
| Unencrypted secrets/etcd compromise | Attacker reads `/var/lib/etcd` snapshot or backup | §12 etcd `EncryptionConfiguration` (KMS v2 with Key Vault), TLS everywhere |
| Untracked/undetected malicious behaviour at runtime | Agent spawns reverse shell after tool-call injection | §17 Falco eBPF runtime detection with custom agentic-workload rules |
| Node-level compromise / rootkit persistence | Attacker tampers with node binaries after gaining root | §5 Trusted Launch (Secure Boot + vTPM), SELinux enforcing, immutable `/usr` (OS Guard where available) |

This maps directly onto the **NSA/CISA Kubernetes Hardening Guidance** categories (scan images, least privilege, network separation, firewalling + encryption, strong authN/authZ, audit logging, periodic review) — each is implemented in a dedicated section below.

---

## 4. Prerequisites & Azure Infrastructure Layout

### 4.1 Required tooling (admin workstation)

- Azure CLI ≥ 2.65 (`az`)
- `kubectl`, `helm` ≥ 3.14, `cilium` CLI, `velero` CLI
- SSH key pair (no password-based SSH anywhere)

### 4.2 Azure resources

```bash
# Variables used throughout this guide
export RG="rg-agentic-k8s-prod"
export LOC="eastus2"
export VNET="vnet-agentic-k8s"
export CP_VM="node-cp-01"
export WK_VM="node-wk-01"
export ADMIN_USER="k8sadmin"

az group create -n "$RG" -l "$LOC"

# Network: dedicated subnets for control-plane, workers and Bastion (no public IPs on nodes)
az network vnet create -g "$RG" -n "$VNET" --address-prefix 10.60.0.0/16 \
  --subnet-name cp-subnet --subnet-prefix 10.60.1.0/24
az network vnet subnet create -g "$RG" --vnet-name "$VNET" \
  --name worker-subnet --address-prefix 10.60.2.0/24
az network vnet subnet create -g "$RG" --vnet-name "$VNET" \
  --name AzureBastionSubnet --address-prefix 10.60.250.0/26

# Bastion for break-glass SSH access (no SSH exposed to the internet)
az network public-ip create -g "$RG" -n pip-bastion --sku Standard
az network bastion create -g "$RG" -n bastion-agentic-k8s \
  --vnet-name "$VNET" --public-ip-address pip-bastion --location "$LOC"

# NSGs: control-plane and worker each get a locked-down NSG
az network nsg create -g "$RG" -n nsg-cp
az network nsg create -g "$RG" -n nsg-wk

# Control-plane NSG: allow 6443 (API server) & 2379-2380 (etcd) only from the VNet,
# 10250 (kubelet) only from the worker subnet, SSH only from AzureBastionSubnet
az network nsg rule create -g "$RG" --nsg-name nsg-cp --name allow-apiserver-vnet \
  --priority 100 --source-address-prefixes 10.60.0.0/16 --destination-port-ranges 6443 \
  --access Allow --protocol Tcp
az network nsg rule create -g "$RG" --nsg-name nsg-cp --name allow-etcd-cp \
  --priority 110 --source-address-prefixes 10.60.1.0/24 --destination-port-ranges 2379-2380 \
  --access Allow --protocol Tcp
az network nsg rule create -g "$RG" --nsg-name nsg-cp --name allow-kubelet-from-workers \
  --priority 120 --source-address-prefixes 10.60.2.0/24 --destination-port-ranges 10250 \
  --access Allow --protocol Tcp
az network nsg rule create -g "$RG" --nsg-name nsg-cp --name allow-ssh-bastion \
  --priority 130 --source-address-prefixes 10.60.250.0/26 --destination-port-ranges 22 \
  --access Allow --protocol Tcp
az network nsg rule create -g "$RG" --nsg-name nsg-cp --name deny-all-inbound \
  --priority 4096 --source-address-prefixes '*' --destination-port-ranges '*' \
  --access Deny --protocol '*'
```

> **Design note.** No node has a public IP. All administrative access goes through Azure Bastion. All API-server access from outside the VNet should go through a private endpoint / VPN / ExpressRoute — do **not** expose `:6443` to the internet.

### 4.3 VM sizing guidance

| Node | Minimum SKU | Notes |
|---|---|---|
| Control plane | `Standard_D4s_v5` (4 vCPU / 16 GiB) | etcd is latency-sensitive; use Premium SSD v2 for `/var/lib/etcd` |
| Worker (agentic workloads, CPU-only) | `Standard_D8s_v5` (8 vCPU / 32 GiB) | scale per concurrent agent/tool-execution count |
| Worker (with local LLM inference) | `Standard_NC-series` / `NCads_H100_v5` | see [§18](#18-optional-gpu-nodes-for-local-inference) |

Both VMs are created with **`--security-type TrustedLaunch --enable-secure-boot true --enable-vtpm true`** — this is a first-class Azure Linux feature: Trusted Launch provides measured, attested boot backed by a virtual TPM, closing the gap that lets a compromised early-boot component persist rootkits.

```bash
IMG="MicrosoftCBLMariner:cbl-mariner:cbl-mariner-3-gen2:latest"  # Azure Linux 3.0 Gen2

az vm create -g "$RG" -n "$CP_VM" --image "$IMG" \
  --size Standard_D4s_v5 --vnet-name "$VNET" --subnet cp-subnet \
  --nsg nsg-cp --public-ip-address "" \
  --admin-username "$ADMIN_USER" --ssh-key-values ~/.ssh/id_ed25519.pub \
  --security-type TrustedLaunch --enable-secure-boot true --enable-vtpm true \
  --os-disk-size-gb 128

az vm create -g "$RG" -n "$WK_VM" --image "$IMG" \
  --size Standard_D8s_v5 --vnet-name "$VNET" --subnet worker-subnet \
  --nsg nsg-wk --public-ip-address "" \
  --admin-username "$ADMIN_USER" --ssh-key-values ~/.ssh/id_ed25519.pub \
  --security-type TrustedLaunch --enable-secure-boot true --enable-vtpm true \
  --os-disk-size-gb 256
```

> Confirm the current Azure Linux 3.0 Marketplace image alias with `az vm image list --publisher MicrosoftCBLMariner --all -o table`, since Marketplace SKU strings are periodically renamed as new minor images ship.

---

## 5. Host OS Provisioning & Hardening (Azure Linux 3.0)

Azure Linux 3.0 is Microsoft's FedRAMP-certified, minimal-footprint Linux distribution — the base of >80% of Microsoft's own AKS fleet — built with a 6.6 kernel, `systemd` 255, RPM/`tdnf` package management, FIPS 140-3 validated crypto (SymCrypt), and native Secure Boot/measured-boot integration. Run the following **on every node**.

### 5.1 Baseline update & minimal packages

```bash
sudo tdnf makecache
sudo tdnf update -y
sudo tdnf install -y chrony auditd firewalld policycoreutils-python-utils tar curl jq
```

### 5.2 Time sync, hostname, /etc/hosts

```bash
sudo systemctl enable --now chronyd
sudo hostnamectl set-hostname "$(hostname)"
# Add static entries for both nodes on both nodes (or use private DNS zone in production)
sudo tee -a /etc/hosts >/dev/null <<EOF
10.60.1.4  node-cp-01
10.60.2.4  node-wk-01
EOF
```

### 5.3 Kernel & sysctl hardening

```bash
sudo tee /etc/modules-load.d/k8s.conf >/dev/null <<EOF
overlay
br_netfilter
EOF
sudo modprobe overlay
sudo modprobe br_netfilter

sudo tee /etc/sysctl.d/99-kubernetes-hardening.conf >/dev/null <<'EOF'
# Required for CNI bridging / Kubernetes networking
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1

# Kernel / network hardening (CIS Distribution Independent Linux + NSA/CISA guidance)
kernel.kptr_restrict          = 2
kernel.dmesg_restrict         = 1
kernel.perf_event_paranoid    = 3
kernel.unprivileged_bpf_disabled = 0   # required by Cilium eBPF datapath; restrict via LSM instead
net.ipv4.conf.all.rp_filter   = 1
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.all.send_redirects   = 0
net.ipv4.conf.all.accept_source_route = 0
net.ipv4.icmp_echo_ignore_broadcasts = 1
net.ipv4.tcp_syncookies        = 1
fs.protected_hardlinks         = 1
fs.protected_symlinks          = 1
fs.suid_dumpable                = 0
EOF
sudo sysctl --system
```

### 5.4 Disable swap (mandatory for kubelet)

```bash
sudo swapoff -a
sudo sed -ri '/\sswap\s/s/^/#/' /etc/fstab
```

### 5.5 SELinux — keep it enforcing

Azure Linux ships SELinux; do **not** disable it (unlike common but insecure guidance for other distros). Instead, run kubelet/containerd with proper container SELinux typing:

```bash
getenforce   # expect: Enforcing
sudo tdnf install -y container-selinux
```

If a specific policy denial blocks a legitimate container operation, generate a targeted policy module with `audit2allow` rather than switching to `permissive`/`disabled`. For OS Guard–enabled images (public preview at the time of writing), mandatory access control and code-integrity enforcement (IPE) ship in **audit mode**; plan a validation pass before switching to `enforcing` in a later hardening iteration.

### 5.6 Firewall (host-level, defense-in-depth under the NSG)

```bash
sudo systemctl enable --now firewalld
# Control-plane node
sudo firewall-cmd --permanent --add-port=6443/tcp
sudo firewall-cmd --permanent --add-port=2379-2380/tcp
sudo firewall-cmd --permanent --add-port=10250-10252/tcp
sudo firewall-cmd --permanent --add-port=10259/tcp
sudo firewall-cmd --permanent --add-port=10257/tcp
# Cilium/VXLAN/health/Hubble ports (both nodes)
sudo firewall-cmd --permanent --add-port=4240/tcp   # cilium-health
sudo firewall-cmd --permanent --add-port=8472/udp   # VXLAN overlay
sudo firewall-cmd --permanent --add-port=51871/udp  # Cilium WireGuard encryption
sudo firewall-cmd --reload
```

### 5.7 SSH hardening

```bash
sudo sed -ri \
  -e 's/^#?PermitRootLogin.*/PermitRootLogin no/' \
  -e 's/^#?PasswordAuthentication.*/PasswordAuthentication no/' \
  -e 's/^#?ChallengeResponseAuthentication.*/ChallengeResponseAuthentication no/' \
  -e 's/^#?X11Forwarding.*/X11Forwarding no/' \
  /etc/ssh/sshd_config
echo "AllowUsers ${ADMIN_USER}" | sudo tee -a /etc/ssh/sshd_config
sudo systemctl restart sshd
```

### 5.8 auditd baseline (feeds host-level audit trail, complements the K8s API audit log)

```bash
sudo tee /etc/audit/rules.d/k8s-node.rules >/dev/null <<'EOF'
-w /etc/kubernetes/ -p wa -k k8s-config
-w /var/lib/etcd/ -p wa -k etcd-data
-w /etc/containerd/ -p wa -k containerd-config
-w /usr/bin/kubelet -p x -k kubelet-exec
-w /usr/bin/containerd -p x -k containerd-exec
EOF
sudo augenrules --load
sudo systemctl enable --now auditd
```

### 5.9 Unattended, controlled security patching

Azure Linux uses `tdnf`; enable automatic security-only updates with a maintenance window rather than blind auto-upgrade of the whole system (to avoid uncontrolled kubelet/containerd version drift):

```bash
sudo tdnf install -y dnf-automatic 2>/dev/null || sudo tdnf install -y tdnf-plugin-auto-update 2>/dev/null || true
# If unavailable, schedule a systemd timer running `tdnf update --security -y` weekly,
# excluding kubelet/kubeadm/kubectl/containerd (version-pinned, upgraded via the runbook in Appendix D).
sudo tee /etc/tdnf/tdnf.conf.d/hold-k8s.conf >/dev/null <<'EOF'
[main]
exclude=kubelet kubeadm kubectl moby-containerd
EOF
```

---

## 6. Container Runtime Installation (containerd)

Kubernetes requires a CRI-compliant runtime. On Azure Linux, containerd ships as `moby-containerd` from the built-in `tdnf` repositories (Azure Linux 3.0 ships containerd 2.x by default).

```bash
sudo tdnf install -y moby-containerd
sudo mkdir -p /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml >/dev/null

# Use the systemd cgroup driver (required to match kubelet's default since 1.22+)
sudo sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml

# Harden the runtime: disable unneeded plugins, use a distinct sandbox (pause) image,
# and pre-stage support for multiple runtime classes (runc / gVisor / Kata) — see §14.
sudo sed -i 's#sandbox_image = .*#sandbox_image = "registry.k8s.io/pause:3.10"#' /etc/containerd/config.toml

sudo systemctl enable --now containerd
sudo systemctl status containerd --no-pager
```

Verify cgroup v2 is active (Azure Linux 3.0 defaults to unified cgroup v2, required for modern kubelet/containerd):

```bash
stat -fc %T /sys/fs/cgroup/   # expect: cgroup2fs
```

---

## 7. Kubernetes Package Installation

Since **March 4, 2024** the legacy Google-hosted `apt.kubernetes.io` / `yum.kubernetes.io` repositories are frozen; the Kubernetes project now publishes packages through the community-owned **`pkgs.k8s.io`** infrastructure (OpenBuildService), with per-minor-version RPM/DEB repositories. Run on **every node**:

```bash
export K8S_MINOR="v1.34"   # pin explicitly; verify current supported minors at kubernetes.io/releases

sudo tee /etc/yum.repos.d/kubernetes.repo >/dev/null <<EOF
[kubernetes]
name=Kubernetes
baseurl=https://pkgs.k8s.io/core:/stable:/${K8S_MINOR}/rpm/
enabled=1
gpgcheck=1
gpgkey=https://pkgs.k8s.io/core:/stable:/${K8S_MINOR}/rpm/repodata/repomd.xml.key
exclude=kubelet kubeadm kubectl cri-tools kubernetes-cni
EOF

sudo tdnf install -y kubelet kubeadm kubectl --disableexcludes=kubernetes
sudo systemctl enable --now kubelet
```

> `tdnf` is API/CLI compatible with `dnf`/`yum` for repository and package operations, so the official `pkgs.k8s.io` RPM feed installs cleanly on Azure Linux. Pin the exact patch version if you need strict reproducibility, e.g. `tdnf install -y kubelet-1.34.5 kubeadm-1.34.5 kubectl-1.34.5`, and lock further updates via the `hold-k8s.conf` exclude file from §5.9.

---

## 8. Bootstrapping the Control Plane with kubeadm

### 8.1 kubeadm v1beta4 cluster configuration

`kubeadm`'s `v1beta4` config API (default since Kubernetes 1.31, `v1beta3` deprecated) is used below. It restructures `extraArgs` as name/value lists (supporting duplicate flags) and adds a `Timeouts` block — reflect that in your own edits.

Create `/root/kubeadm-config.yaml` **on `node-cp-01`**:

```yaml
apiVersion: kubeadm.k8s.io/v1beta4
kind: InitConfiguration
localAPIEndpoint:
  advertiseAddress: 10.60.1.4
  bindPort: 6443
nodeRegistration:
  name: node-cp-01
  criSocket: unix:///var/run/containerd/containerd.sock
  taints:
    - key: node-role.kubernetes.io/control-plane
      effect: NoSchedule
  kubeletExtraArgs:
    - name: "protect-kernel-defaults"
      value: "true"
---
apiVersion: kubeadm.k8s.io/v1beta4
kind: ClusterConfiguration
kubernetesVersion: v1.34.5
clusterName: agentic-prod
controlPlaneEndpoint: "10.60.1.4:6443"      # replace with an LB VIP if/when you scale to 3 control planes
networking:
  podSubnet: 10.244.0.0/16
  serviceSubnet: 10.96.0.0/12
  dnsDomain: cluster.local
apiServer:
  certSANs:
    - "10.60.1.4"
    - "node-cp-01"
    - "kubernetes.internal.example.com"
  extraArgs:
    - name: anonymous-auth
      value: "false"
    - name: authorization-mode
      value: "Node,RBAC"
    - name: enable-admission-plugins
      value: "NodeRestriction,PodSecurity,ServiceAccount,LimitRanger,ResourceQuota,DenyServiceExternalIPs"
    - name: audit-log-path
      value: "/var/log/kubernetes/audit/audit.log"
    - name: audit-log-maxage
      value: "30"
    - name: audit-log-maxbackup
      value: "10"
    - name: audit-log-maxsize
      value: "100"
    - name: audit-policy-file
      value: "/etc/kubernetes/audit-policy.yaml"
    - name: encryption-provider-config
      value: "/etc/kubernetes/encryption-config.yaml"
    - name: profiling
      value: "false"
    - name: service-account-lookup
      value: "true"
    - name: tls-min-version
      value: "VersionTLS12"
    - name: tls-cipher-suites
      value: "TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256"
    - name: request-timeout
      value: "300s"
controllerManager:
  extraArgs:
    - name: bind-address
      value: "127.0.0.1"
    - name: use-service-account-credentials
      value: "true"
    - name: terminated-pod-gc-threshold
      value: "50"
    - name: profiling
      value: "false"
scheduler:
  extraArgs:
    - name: bind-address
      value: "127.0.0.1"
    - name: profiling
      value: "false"
etcd:
  local:
    dataDir: /var/lib/etcd
    extraArgs:
      - name: auto-compaction-retention
        value: "8"
      - name: quota-backend-bytes
        value: "4294967296"
---
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
cgroupDriver: systemd
containerRuntimeEndpoint: unix:///var/run/containerd/containerd.sock
protectKernelDefaults: true
readOnlyPort: 0
eventRecordQPS: 5
streamingConnectionIdleTimeout: 5m
serverTLSBootstrap: true
tlsCipherSuites:
  - TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384
  - TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
authentication:
  anonymous:
    enabled: false
  webhook:
    enabled: true
authorization:
  mode: Webhook
```

> `bind-address: 127.0.0.1` for `controller-manager`/`scheduler` follows CIS guidance for single/co-located control-plane hosts, restricting the insecure metrics/health ports to localhost. If you later split components across multiple control-plane nodes with a load balancer, adjust `bind-address` and firewall accordingly.

### 8.2 Audit policy

Create `/etc/kubernetes/audit-policy.yaml` **before** running `kubeadm init`:

```yaml
apiVersion: audit.k8s.io/v1
kind: Policy
rules:
  - level: None
    resources:
      - group: ""
        resources: ["events"]
  - level: RequestResponse
    resources:
      - group: ""
        resources: ["secrets", "configmaps"]
  - level: RequestResponse
    verbs: ["create", "update", "patch", "delete"]
    resources:
      - group: "rbac.authorization.k8s.io"
      - group: "policy"
      - group: "cilium.io"
      - group: "kyverno.io"
  - level: Metadata
    omitStages: ["RequestReceived"]
```

### 8.3 etcd/secrets encryption configuration

Create `/etc/kubernetes/encryption-config.yaml` **before** `kubeadm init` (see [§12](#12-secrets-management--encryption-at-rest) for the KMS v2 + Key Vault production variant):

```yaml
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
  - resources:
      - secrets
    providers:
      - aescbc:
          keys:
            - name: key1
              secret: <base64-encoded-32-byte-random-key>
      - identity: {}
```

Generate the key with `head -c 32 /dev/urandom | base64`, and prepare the audit-log directory:

```bash
sudo mkdir -p /var/log/kubernetes/audit
```

### 8.4 Initialize the control plane

```bash
sudo kubeadm config images pull --kubernetes-version v1.34.5
sudo kubeadm init --config /root/kubeadm-config.yaml --upload-certs

mkdir -p "$HOME/.kube"
sudo cp -i /etc/kubernetes/admin.conf "$HOME/.kube/config"
sudo chown "$(id -u):$(id -g)" "$HOME/.kube/config"
chmod 600 "$HOME/.kube/config"
```

Save the printed `kubeadm join ...` command — you'll use it (worker variant) in §9. Because `certificate-key` values expire after two hours, regenerate if needed with `kubeadm init phase upload-certs --upload-certs`.

### 8.5 Lock down `/etc/kubernetes` and PKI file permissions (CIS 1.1.x)

```bash
sudo chmod 600 /etc/kubernetes/admin.conf /etc/kubernetes/*.conf
sudo chown root:root /etc/kubernetes/*.conf
sudo find /etc/kubernetes/pki -type f -name '*.key' -exec chmod 600 {} \;
sudo find /etc/kubernetes/pki -type f -name '*.crt' -exec chmod 644 {} \;
sudo chown -R root:root /etc/kubernetes/pki
sudo chmod 700 /var/lib/etcd
```

---

## 9. Joining the Worker Node

On `node-wk-01`, after completing §5–§7:

```bash
sudo kubeadm join 10.60.1.4:6443 \
  --token <token-from-init-output> \
  --discovery-token-ca-cert-hash sha256:<hash-from-init-output> \
  --cri-socket unix:///var/run/containerd/containerd.sock
```

If the token has expired (default TTL 24h), create a new one from the control plane:

```bash
kubeadm token create --print-join-command
```

Verify from the admin workstation:

```bash
kubectl get nodes -o wide
kubectl get pods -n kube-system
```

Label the worker node for scheduling and future policy targeting:

```bash
kubectl label node node-wk-01 node-role.kubernetes.io/worker=worker workload-class=agentic
```

> **Two-node trade-off, stated explicitly.** With a single control-plane node, etcd cannot achieve quorum-based fault tolerance (`etcd` HA needs an odd number ≥3 members) and there is a single point of failure for the API server. This guide accepts that trade-off per the stated 2-node requirement, but mitigates it operationally with automated etcd snapshotting (§19) and documents the exact upgrade path to a 3-node control plane in [Appendix D](#appendix-d--upgrade-runbook).

---

## 10. CNI: Cilium (eBPF, Encryption, Egress Control)

Cilium is the most widely deployed CNCF-graduated CNI in 2026, used in production at Google, Microsoft, and AWS, and is the right choice here because it gives us — natively, without extra components — the eBPF datapath, a full `kube-proxy` replacement, WireGuard transparent encryption, Hubble flow observability, and **FQDN-based egress policies** that are essential for controlling agentic workloads calling out to LLM/tool APIs by domain name rather than brittle IP allow-lists.

### 10.1 Install

```bash
helm repo add cilium https://helm.cilium.io/
helm repo update

API_SERVER_IP=10.60.1.4
API_SERVER_PORT=6443

helm install cilium cilium/cilium --version 1.17.0 \
  --namespace kube-system \
  --set kubeProxyReplacement=true \
  --set k8sServiceHost="${API_SERVER_IP}" \
  --set k8sServicePort="${API_SERVER_PORT}" \
  --set hubble.enabled=true \
  --set hubble.relay.enabled=true \
  --set hubble.ui.enabled=true \
  --set encryption.enabled=true \
  --set encryption.type=wireguard \
  --set encryption.nodeEncryption=true \
  --set egressGateway.enabled=true \
  --set bpf.masquerade=true \
  --set operator.replicas=1
```

Install the CLI and validate:

```bash
CILIUM_CLI_VERSION=$(curl -s https://raw.githubusercontent.com/cilium/cilium-cli/main/stable.txt)
curl -L --remote-name-all "https://github.com/cilium/cilium-cli/releases/download/${CILIUM_CLI_VERSION}/cilium-linux-amd64.tar.gz"
tar xzvf cilium-linux-amd64.tar.gz && sudo mv cilium /usr/local/bin

cilium status --wait
cilium connectivity test   # optional, run in a non-prod window — creates test workloads
```

Because `kubeProxyReplacement=true`, no `kube-proxy` DaemonSet is required; confirm `kubectl -n kube-system get ds` shows no `kube-proxy` pods (or delete the kubeadm-created one if present: `kubectl -n kube-system delete ds kube-proxy`).

### 10.2 Default-deny network policy baseline

Apply a cluster-wide default deny, then explicit allows — this is the single highest-leverage network control for agentic workloads, since a compromised agent pod with no configured egress is much less useful to an attacker.

```yaml
# 01-default-deny-all.yaml
apiVersion: cilium.io/v2
kind: CiliumClusterwideNetworkPolicy
metadata:
  name: default-deny-all-egress
spec:
  endpointSelector: {}
  egress: []
  ingress: []
```

```yaml
# 02-allow-dns-and-cluster.yaml
apiVersion: cilium.io/v2
kind: CiliumClusterwideNetworkPolicy
metadata:
  name: allow-dns-and-intra-cluster
spec:
  endpointSelector: {}
  egress:
    - toEndpoints:
        - matchLabels:
            "k8s:io.kubernetes.pod.namespace": kube-system
            "k8s:k8s-app": kube-dns
      toPorts:
        - ports:
            - port: "53"
              protocol: ANY
    - toEntities: ["cluster", "kube-apiserver"]
```

### 10.3 FQDN-scoped egress for agentic workloads

Rather than "deny all but allow the internet," scope each agent namespace's egress to the exact model/tool endpoints it needs — this directly limits data-exfiltration blast radius if an agent is compromised via prompt injection.

```yaml
# agent-namespace-egress.yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: agent-allow-llm-and-tools
  namespace: agentic-workloads
spec:
  endpointSelector:
    matchLabels:
      app: llm-agent
  egress:
    - toFQDNs:
        - matchName: "api.openai.com"
        - matchPattern: "*.openai.azure.com"
        - matchName: "your-vector-db.example.com"
      toPorts:
        - ports:
            - port: "443"
              protocol: TCP
    - toEndpoints:
        - matchLabels:
            "k8s:io.kubernetes.pod.namespace": kube-system
            "k8s:k8s-app": kube-dns
      toPorts:
        - ports:
            - port: "53"
              protocol: ANY
          rules:
            dns:
              - matchPattern: "*"
```

Cilium's DNS proxy observes the resolution of the allow-listed FQDNs and dynamically authorizes only the resolved IPs — solving the classic problem of cloud APIs sitting behind large, frequently changing CIDR ranges.

### 10.4 L7 HTTP policy for MCP/tool servers

If agents call an internal tool-server over HTTP, Cilium can restrict by path/method (L7, enforced via an in-cluster Envoy proxy managed by Cilium):

```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: restrict-tool-server-api
  namespace: agentic-workloads
spec:
  endpointSelector:
    matchLabels:
      app: tool-server
  ingress:
    - fromEndpoints:
        - matchLabels:
            app: llm-agent
      toPorts:
        - ports:
            - port: "8080"
              protocol: TCP
          rules:
            http:
              - method: "POST"
                path: "/v1/tools/invoke"
              - method: "GET"
                path: "/healthz"
```

---

## 11. Identity, Authentication & RBAC

- **Disable anonymous authentication** and **static tokens** on the API server (already set in §8.1).
- **Use `Node,RBAC` authorization mode** (set in §8.1) so kubelets can only access objects related to their own node (`NodeRestriction` admission plugin enforces this).
- **Prefer external OIDC** (Microsoft Entra ID) for human users instead of long-lived client certificates or the static `admin.conf` — configure `--oidc-issuer-url`, `--oidc-client-id`, `--oidc-username-claim=upn`, `--oidc-groups-claim=groups` on the API server, and map Entra groups to Kubernetes `RoleBinding`/`ClusterRoleBinding`s. Never distribute `admin.conf` to end users; treat it as a break-glass credential stored in Key Vault.
- **Namespace-scoped least privilege** for agent workloads — never grant `cluster-admin` to a workload ServiceAccount. Example minimal role for an agent that only needs to read its own ConfigMaps/Secrets and create ephemeral Jobs for tool execution:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: agentic-workloads
  name: agent-runtime
rules:
  - apiGroups: [""]
    resources: ["configmaps"]
    verbs: ["get", "list", "watch"]
  - apiGroups: ["batch"]
    resources: ["jobs"]
    verbs: ["create", "get", "list", "watch", "delete"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: agent-runtime-binding
  namespace: agentic-workloads
subjects:
  - kind: ServiceAccount
    name: llm-agent-sa
    namespace: agentic-workloads
roleRef:
  kind: Role
  name: agent-runtime
  apiGroup: rbac.authorization.k8s.io
```

- **Disable automatic ServiceAccount token mounting** unless the pod explicitly needs to call the Kubernetes API (most agent pods do not):

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: llm-agent-sa
  namespace: agentic-workloads
automountServiceAccountToken: false
```

- **Bind kubelet client certificates** via `serverTLSBootstrap: true` (set in §8.1) and auto-approve only via the `csrapproving` controller, never manually approving arbitrary CSRs.

---

## 12. Secrets Management & Encryption at Rest

Two complementary layers: (1) **etcd encryption at rest** so cluster-internal `Secret` objects are never stored as plaintext on disk, and (2) **external secret delivery** so agent API keys never live in Git, images, or plain Kubernetes `Secret` objects to begin with.

### 12.1 etcd encryption — production KMS v2 provider backed by Azure Key Vault

Replace the bootstrap `aescbc` configuration from §8.3 with a KMS v2 provider once the cluster is up, so the Data Encryption Key (DEK) is itself wrapped by a Key Encryption Key (KEK) held in Azure Key Vault and never persisted in plaintext:

```bash
az keyvault create --name kv-agentic-k8s --resource-group "$RG" --location "$LOC" --enable-purge-protection true
az keyvault key create --vault-name kv-agentic-k8s --name k8s-etcd-kek --protection hsm --size 2048
```

```yaml
# /etc/kubernetes/encryption-config.yaml (KMS v2)
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
  - resources:
      - secrets
    providers:
      - kms:
          apiVersion: v2
          name: azure-kms
          endpoint: unix:///var/run/kmsplugin/azurekms.sock
          timeout: 3s
      - identity: {}
```

Run the [Azure Key Vault KMS plugin](https://github.com/Azure/kubernetes-kms) as a static pod / DaemonSet using a Workload-Identity-federated managed identity scoped to `Key Vault Crypto User` only, mount its Unix socket at `/var/run/kmsplugin/azurekms.sock`, restart `kube-apiserver`, then re-encrypt existing secrets:

```bash
kubectl get secrets --all-namespaces -o json | kubectl replace -f -
```

Rotate the KEK on a fixed schedule (quarterly is a common enterprise baseline) and keep the previous key available (read-only) until all data has been re-encrypted with the new key.

### 12.2 External secrets for agent API keys — Key Vault CSI Driver + Workload Identity

Never bake LLM/tool provider API keys into images or plain `Secret` manifests. Use the **Secrets Store CSI Driver** with the **Azure Key Vault provider**, authenticated via **Microsoft Entra Workload ID** (OIDC federation), which is the same pattern AKS uses and works on a self-managed cluster once you publish your own OIDC discovery document.

```bash
helm repo add secrets-store-csi-driver https://kubernetes-sigs.github.io/secrets-store-csi-driver/charts
helm repo add csi-secrets-store-provider-azure https://azure.github.io/secrets-store-csi-driver-provider-azure/charts
helm install csi-secrets-store secrets-store-csi-driver/secrets-store-csi-driver \
  -n kube-system --set enableSecretRotation=true --set rotationPollInterval=2m
helm install csi-secrets-store-provider-azure csi-secrets-store-provider-azure/csi-secrets-store-provider-azure -n kube-system
```

```yaml
apiVersion: secrets-store.csi.x-k8s.io/v1
kind: SecretProviderClass
metadata:
  name: agent-llm-keys
  namespace: agentic-workloads
spec:
  provider: azure
  parameters:
    usePodIdentity: "false"
    clientID: "<workload-identity-client-id>"
    keyvaultName: "kv-agentic-k8s"
    tenantId: "<entra-tenant-id>"
    objects: |
      array:
        - |
          objectName: openai-api-key
          objectType: secret
  secretObjects:
    - secretName: llm-agent-secrets
      type: Opaque
      data:
        - objectName: openai-api-key
          key: OPENAI_API_KEY
```

Mount it as a CSI volume in the agent pod spec, and consume `llm-agent-secrets` as an env var only where the application demands it (file mounts are strictly preferable — no plaintext env-var leakage into `kubectl describe`/logs). With rotation enabled, Key Vault key/secret rotation automatically propagates to the mounted volume and synced `Secret` within the polling interval.

### 12.3 GitOps-safe secrets for platform config

For cluster/platform-level secrets that must live in Git (e.g., referenced from a GitOps pipeline), use **Mozilla SOPS** with Azure Key Vault as the encryption backend, so only the in-cluster reconciler can decrypt values while diffs remain readable.

---

## 13. Pod & Workload Hardening

### 13.1 Pod Security Admission (built into the API server, no extra components)

Enforce the `restricted` Pod Security Standard on every agentic-workload namespace:

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: agentic-workloads
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/enforce-version: latest
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

### 13.2 Hardened pod template baseline

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llm-agent
  namespace: agentic-workloads
spec:
  replicas: 2
  selector:
    matchLabels: { app: llm-agent }
  template:
    metadata:
      labels: { app: llm-agent }
    spec:
      serviceAccountName: llm-agent-sa
      automountServiceAccountToken: false
      runtimeClassName: gvisor        # see §14
      securityContext:
        runAsNonRoot: true
        runAsUser: 10001
        fsGroup: 10001
        seccompProfile: { type: RuntimeDefault }
      containers:
        - name: agent
          image: myregistry.azurecr.io/agentic/llm-agent:1.4.2@sha256:<digest>
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities: { drop: ["ALL"] }
          resources:
            requests: { cpu: "500m", memory: "512Mi" }
            limits: { cpu: "2", memory: "2Gi" }
          volumeMounts:
            - name: tmp
              mountPath: /tmp
            - name: secrets
              mountPath: /mnt/secrets
              readOnly: true
      volumes:
        - name: tmp
          emptyDir: {}
        - name: secrets
          csi:
            driver: secrets-store.csi.k8s.io
            readOnly: true
            volumeAttributes:
              secretProviderClass: agent-llm-keys
```

### 13.3 Namespace resource governance

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: agentic-quota
  namespace: agentic-workloads
spec:
  hard:
    requests.cpu: "16"
    requests.memory: 32Gi
    limits.cpu: "32"
    limits.memory: 64Gi
    pods: "40"
---
apiVersion: v1
kind: LimitRange
metadata:
  name: agentic-limits
  namespace: agentic-workloads
spec:
  limits:
    - type: Container
      default: { cpu: "1", memory: "1Gi" }
      defaultRequest: { cpu: "250m", memory: "256Mi" }
      max: { cpu: "4", memory: "8Gi" }
```

---

## 14. Sandboxing Agentic Workloads (gVisor / Kata Containers)

This is the most important control unique to agentic workloads. Standard `runc` containers share the host kernel; if an agent executes generated or tool-provided code, a single kernel vulnerability can escalate to the node. The Kubernetes `RuntimeClass` API lets you run different isolation levels **side by side on the same cluster**, selected per-pod via `spec.runtimeClassName` — with no change to how the pod is otherwise deployed.

| Runtime | Isolation model | Startup cost | Use for |
|---|---|---|---|
| `runc` (default) | Shared kernel (namespaces/cgroups) | none | Trusted platform/system components only |
| **gVisor** (`runsc`) | Syscall interception in userspace (Sentry), no dedicated VM kernel | milliseconds | Agents that only call external APIs / tools, no arbitrary code execution — good default for most agent pods |
| **Kata Containers** (KVM or Firecracker VMM) | Hardware-level isolation, dedicated guest kernel per pod | ~125–300ms | Agents that execute arbitrary/generated code (Python/shell "code interpreter" tools), multi-tenant untrusted workloads |
| Confidential Containers (TDX/SEV-SNP) | Hardware enclave | higher, workload-dependent | Regulated data where you must also distrust the host operator — optional, out of scope of the 2-node baseline |

This decision matrix reflects the actively-evolving **`kubernetes-sigs/agent-sandbox`** project (SIG Apps, launched KubeCon Atlanta, Nov 2025), which layers a `Sandbox`/`SandboxTemplate` CRD on top of exactly these two `RuntimeClass` backends to manage long-running, stateful, singleton agent workloads (pause/resume lifecycle) — worth adopting once it reaches GA, but the underlying `RuntimeClass` mechanics below work today, standalone.

### 14.1 Install gVisor on the worker node

```bash
curl -fsSL https://gvisor.dev/archive.key | sudo gpg --dearmor -o /usr/share/keyrings/gvisor-archive-keyring.gpg
ARCH=$(uname -m)
URL="https://storage.googleapis.com/gvisor/releases/release/latest/${ARCH}"
sudo curl -fsSL "${URL}/runsc" -o /usr/local/bin/runsc
sudo curl -fsSL "${URL}/containerd-shim-runsc-v1" -o /usr/local/bin/containerd-shim-runsc-v1
sudo chmod +x /usr/local/bin/runsc /usr/local/bin/containerd-shim-runsc-v1

sudo tee -a /etc/containerd/config.toml >/dev/null <<'EOF'

[plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runsc]
  runtime_type = "io.containerd.runsc.v1"
EOF
sudo systemctl restart containerd
```

```yaml
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: gvisor
handler: runsc
```

### 14.2 Install Kata Containers on the worker node

Kata requires nested virtualization support (KVM) on the Azure VM — use a `_v5`/`_v6` size family with nested virtualization enabled (default on most current-generation Azure VM sizes):

```bash
# Confirm KVM is available
lsmod | grep kvm || sudo modprobe kvm
[ -e /dev/kvm ] && echo "KVM available" || echo "WARNING: enable nested virtualization on this VM size"

sudo tdnf install -y kata-containers 2>/dev/null || \
  (curl -fsSL https://raw.githubusercontent.com/kata-containers/kata-containers/main/utils/kata-manager.sh | bash -s -- install)

sudo tee -a /etc/containerd/config.toml >/dev/null <<'EOF'

[plugins."io.containerd.grpc.v1.cri".containerd.runtimes.kata]
  runtime_type = "io.containerd.kata.v2"
EOF
sudo systemctl restart containerd
```

```yaml
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: kata
handler: kata
```

### 14.3 Routing agent pods to the right sandbox

```yaml
# Code-interpreter / shell-executing agent tool -> Kata (VM-level isolation)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agent-code-interpreter
  namespace: agentic-workloads
spec:
  replicas: 1
  selector: { matchLabels: { app: agent-code-interpreter } }
  template:
    metadata: { labels: { app: agent-code-interpreter } }
    spec:
      runtimeClassName: kata
      automountServiceAccountToken: false
      securityContext:
        runAsNonRoot: true
        seccompProfile: { type: RuntimeDefault }
      containers:
        - name: interpreter
          image: myregistry.azurecr.io/agentic/code-interpreter:2.1.0@sha256:<digest>
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities: { drop: ["ALL"] }
          resources:
            requests: { cpu: "1", memory: "1Gi" }
            limits: { cpu: "2", memory: "2Gi" }
```

**Rule of thumb** codified across current field guidance: if the agent only calls external HTTP APIs, gVisor's userspace syscall interception is sufficient and cheap; if the agent executes shell/Python/generated code, default to Kata (or Kata+Firecracker) for hardware-level isolation, matching how CVE-2025-3248-class incidents (Langflow pre-auth RCE via `exec()`) are mitigated in production.

---

## 15. Policy-as-Code with Kyverno

Kyverno (CNCF, graduated to incubating maturity in 2024) is used here over OPA/Gatekeeper because policies are plain Kubernetes YAML — no Rego to learn — and it natively supports validating, **mutating**, generating, and **image-verifying** admission policies, which maps well onto an agentic-workload platform team that needs to move fast without a Rego specialist on staff. (Gatekeeper remains a valid choice if your org has existing OPA/Rego investment across non-Kubernetes systems.)

```bash
helm repo add kyverno https://kyverno.github.io/kyverno/
helm repo update
helm install kyverno kyverno/kyverno -n kyverno --create-namespace
helm install kyverno-policies kyverno/kyverno-policies -n kyverno
```

### 15.1 Require signed images (cosign) for agent workloads

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: verify-agent-image-signatures
spec:
  validationFailureAction: Enforce
  rules:
    - name: verify-signature
      match:
        any:
          - resources:
              kinds: ["Pod"]
              namespaces: ["agentic-workloads"]
      verifyImages:
        - imageReferences:
            - "myregistry.azurecr.io/agentic/*"
          attestors:
            - count: 1
              entries:
                - keys:
                    publicKeys: |-
                      -----BEGIN PUBLIC KEY-----
                      <cosign public key>
                      -----END PUBLIC KEY-----
```

### 15.2 Disallow the default `RuntimeClass`/`runc` for untrusted namespaces

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-sandboxed-runtimeclass
spec:
  validationFailureAction: Enforce
  rules:
    - name: require-runtimeclass
      match:
        any:
          - resources:
              kinds: ["Pod"]
              namespaces: ["agentic-workloads"]
      validate:
        message: "Agentic workloads must set runtimeClassName to 'gvisor' or 'kata'."
        pattern:
          spec:
            runtimeClassName: "gvisor | kata"
```

### 15.3 Block registries other than your approved registry

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: restrict-image-registries
spec:
  validationFailureAction: Enforce
  rules:
    - name: allowed-registries
      match:
        any: [{ resources: { kinds: ["Pod"] } }]
      validate:
        message: "Only images from myregistry.azurecr.io are allowed."
        pattern:
          spec:
            containers:
              - image: "myregistry.azurecr.io/*"
```

---

## 16. Supply Chain Security

1. **Private registry only.** Use Azure Container Registry with content-trust / geo-replication disabled to untrusted regions; disable anonymous pull.
2. **Image scanning in CI.** Run Trivy (or Grype) against every agent/tool image before push; fail the pipeline on Critical/High CVEs without an accepted exception.
3. **SBOM generation.** Generate an SBOM (Syft, or `docker buildx imagetools`) per image and store it alongside the artifact for audit and rapid CVE-impact assessment.
4. **Sign every image** with `cosign sign --key azurekms://<key-vault-key-uri> <image>@<digest>` (cosign supports Azure Key Vault as a KMS signer directly — no private key material leaves Key Vault).
5. **Enforce signature verification at admission** — §15.1 above.
6. **Pin by digest, not tag**, in every manifest (`image: repo/name@sha256:...`) to prevent tag-mutation attacks.
7. **Track agent framework and model dependencies** (LangChain/LangGraph/CrewAI/AutoGen-class libraries and their transitive PyPI/npm trees) with the same SBOM + scan pipeline — 2025's Langflow and multiple MCP-server CVEs originated in this exact layer, not in Kubernetes itself.

---

## 17. Runtime Security & Observability

### 17.1 Falco — eBPF runtime threat detection

```bash
helm repo add falcosecurity https://falcosecurity.github.io/charts
helm repo update
helm install falco falcosecurity/falco \
  --namespace falco --create-namespace \
  --set driver.kind=modern_ebpf \
  --set falcosidekick.enabled=true \
  --set falcosidekick.webui.enabled=true \
  --set collectors.kubernetes.enabled=true
```

`modern_ebpf` uses the CO-RE eBPF probe, requires no kernel headers or module signing, and works cleanly on Azure Linux's hardened, SELinux-enforcing kernel — there is no good reason to use the legacy kernel-module driver on a current cluster.

Add agentic-workload-specific detection rules, e.g. flag any unexpected outbound connection or shell spawned from an agent pod:

```yaml
# /etc/falco/rules.d/agentic-workloads.yaml
- rule: Unexpected shell spawned in agent pod
  desc: An agent container spawned an interactive shell — often indicative of prompt-injection-driven code execution
  condition: >
    spawned_process and container and
    k8s.ns.name = "agentic-workloads" and
    proc.name in (bash, sh, zsh) and
    not proc.pname in (supervisord, tini)
  output: >
    Shell spawned in agent pod (user=%user.name pod=%k8s.pod.name
    container=%container.name cmdline=%proc.cmdline)
  priority: WARNING
  tags: [agentic, shell]

- rule: Agent pod unexpected outbound connection
  desc: Outbound connection from an agent pod to a destination outside the allow-listed FQDN set
  condition: >
    outbound and container and
    k8s.ns.name = "agentic-workloads" and
    not fd.sip in (allowed_llm_provider_ips)
  output: >
    Unexpected egress from agent pod (pod=%k8s.pod.name dest=%fd.rip:%fd.rport)
  priority: CRITICAL
  tags: [agentic, network, exfiltration]
```

### 17.2 Metrics, logs, traces

- **Prometheus + Grafana** (via `kube-prometheus-stack` Helm chart) for cluster and node metrics, plus Cilium/Hubble metrics for network flow visibility.
- **Loki or Azure Monitor / Log Analytics** as the audit-log and Falco-alert sink — ship `kube-apiserver` audit logs and Falco output there for centralized, tamper-evident retention (write-once storage account with immutability policy is recommended for the audit trail).
- **Hubble UI** for real-time L3/L4/L7 flow visibility, especially useful for validating that agentic-workload egress policies match observed behavior before flipping them from `audit` to `enforce`.

---

## 18. Optional: GPU Nodes for Local Inference

If agentic workloads require on-cluster LLM inference (vLLM, TGI, etc.) rather than calling an external hosted API, add a GPU-backed worker (e.g., `Standard_NC-series`/`NCads_H100_v5`) and install the **NVIDIA GPU Operator**, which packages the driver, container toolkit, and device plugin as cluster-managed DaemonSets:

```bash
kubectl create namespace gpu-operator
helm repo add nvidia https://helm.ngc.nvidia.com/nvidia
helm repo update
helm install gpu-operator nvidia/gpu-operator \
  -n gpu-operator \
  --set driver.enabled=true \
  --set toolkit.enabled=true
```

Verify `nvidia.com/gpu` appears as an allocatable resource (`kubectl describe node <gpu-node> | grep nvidia.com/gpu`), then request it explicitly in the inference Deployment's `resources.limits`. Apply the same Pod Security / RuntimeClass / NetworkPolicy controls from §§13–15 to GPU inference pods — GPU access does not exempt a workload from the hardening baseline. Note that **Kata Containers with GPU passthrough** requires additional VFIO configuration; if you need both sandboxing and local GPU inference, validate this combination in a staging environment before production rollout, as GPU passthrough through a microVM boundary is more operationally involved than CPU-only Kata pods.

---

## 19. Backup, Restore & Disaster Recovery

### 19.1 etcd snapshotting (control-plane state)

```bash
sudo ETCDCTL_API=3 etcdctl snapshot save /var/backups/etcd/etcd-snapshot-$(date +%F).db \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key

az storage blob upload --account-name <storageaccount> --container-name etcd-backups \
  --file /var/backups/etcd/etcd-snapshot-$(date +%F).db --name etcd-snapshot-$(date +%F).db
```

Automate with a `systemd` timer (daily, with off-box upload) and **test the restore procedure quarterly** — an untested backup is not a backup.

### 19.2 Velero (application-layer resources + persistent volumes)

```bash
velero install \
  --provider azure \
  --plugins velero/velero-plugin-for-microsoft-azure:latest \
  --bucket velero-backups \
  --secret-file ./credentials-velero \
  --backup-location-config resourceGroup=$RG,storageAccount=<storageaccount> \
  --snapshot-location-config apiTimeout=5m,resourceGroup=$RG

velero schedule create daily-agentic-backup \
  --schedule="0 2 * * *" --ttl 720h --include-namespaces agentic-workloads
```

Note that Velero backs up via the Kubernetes API (Deployments, Services, ConfigMaps, Secrets, CRDs, and PV snapshots), **not** etcd internals directly — you need both Velero (application recovery) and etcd snapshots (control-plane/cluster-identity recovery) for full disaster recovery.

---

## 20. Patching & Lifecycle Management

1. **Host OS**: weekly `tdnf update --security` window, excluding pinned Kubernetes/container-runtime packages (§5.9); reboot via a controlled, drained maintenance window.
2. **Kubernetes minor upgrades**: follow the official skew policy (upgrade one minor version at a time), always control plane before workers:
   ```bash
   sudo kubeadm upgrade plan
   sudo kubeadm upgrade apply v1.35.x
   sudo tdnf install -y kubelet-1.35.x kubectl-1.35.x
   sudo systemctl restart kubelet
   # then, per worker:
   kubectl drain node-wk-01 --ignore-daemonsets --delete-emptydir-data
   sudo kubeadm upgrade node
   sudo tdnf install -y kubelet-1.35.x kubectl-1.35.x
   sudo systemctl restart kubelet
   kubectl uncordon node-wk-01
   ```
3. **Cilium/Kyverno/Falco**: track upstream release notes; upgrade via `helm upgrade` in a staging cluster or canary namespace first.
4. **Certificate rotation**: kubeadm-managed certs default to 1-year validity; `kubeadm certs renew all` before expiry, and monitor with `kubeadm certs check-expiration`.

---

## 21. Compliance Validation (kube-bench / Kubescape)

Validate the hardening work against the **CIS Kubernetes Benchmark** using `kube-bench` (Aqua Security, Apache-2.0, supports vanilla kubeadm clusters across CIS 1.5.1 through the current 1.12 series covering Kubernetes 1.15–1.34+):

```bash
kubectl apply -f https://raw.githubusercontent.com/aquasecurity/kube-bench/main/job-master.yaml
kubectl apply -f https://raw.githubusercontent.com/aquasecurity/kube-bench/main/job-node.yaml
kubectl logs -l app=kube-bench --tail=-1
```

For broader coverage (CIS + NSA-CISA + MITRE ATT&CK mappings, plus image and RBAC risk scanning), run **Kubescape** as a periodic scheduled scan:

```bash
helm repo add kubescape https://kubescape.github.io/helm-charts/
helm install kubescape kubescape/kubescape-operator -n kubescape --create-namespace
```

Treat both tools' output as a living checklist — re-run after every Kubernetes minor upgrade and after any change to `kube-apiserver`/`kubelet` flags, and track remediation of `WARN`/`FAIL` items with owners and due dates rather than leaving them open indefinitely.

---

## Appendix A — Full Reference Manifests

All manifests in this guide are also collected, ready to `kubectl apply -f`, in the companion repository structure suggested below:

```
k8s-manifests/
├── 00-namespaces/agentic-workloads-namespace.yaml
├── 01-network-policy/{default-deny-all.yaml, allow-dns-cluster.yaml, agent-egress-fqdn.yaml}
├── 02-runtimeclasses/{gvisor.yaml, kata.yaml}
├── 03-rbac/{agent-role.yaml, agent-rolebinding.yaml}
├── 04-secrets/{secretproviderclass-llm-keys.yaml}
├── 05-policies/{verify-images.yaml, require-runtimeclass.yaml, restrict-registries.yaml}
├── 06-quotas/{resourcequota.yaml, limitrange.yaml}
└── 07-workloads/{llm-agent-deployment.yaml, code-interpreter-deployment.yaml}
```

## Appendix B — Variable Reference

| Variable | Example | Purpose |
|---|---|---|
| `K8S_MINOR` | `v1.34` | Pins the `pkgs.k8s.io` repo minor version |
| `RG`, `LOC`, `VNET` | see §4 | Azure resource naming |
| `CP_VM` / `WK_VM` | `node-cp-01` / `node-wk-01` | Node hostnames |
| `API_SERVER_IP` | `10.60.1.4` | Used by Cilium `k8sServiceHost` |
| `kv-agentic-k8s` | Key Vault name | etcd KMS + agent secrets |

## Appendix C — Hardening Checklist

- [ ] Trusted Launch (Secure Boot + vTPM) enabled on all VMs
- [ ] SELinux `Enforcing` on all nodes
- [ ] Swap disabled; kernel sysctl hardening applied
- [ ] No public IP on any node; Bastion-only SSH; password auth disabled
- [ ] `anonymous-auth=false`, `authorization-mode=Node,RBAC`, admission plugins set
- [ ] Audit logging enabled with a retained, tamper-evident sink
- [ ] etcd encryption at rest (KMS v2 + Key Vault in production)
- [ ] PKI file permissions locked to `600`/`644`, owned by `root:root`
- [ ] Cilium installed with `kubeProxyReplacement`, WireGuard encryption, Hubble
- [ ] Default-deny `NetworkPolicy`/`CiliumClusterwideNetworkPolicy` applied cluster-wide
- [ ] Agent egress scoped to explicit FQDN allow-lists
- [ ] Pod Security Admission `restricted` enforced on all workload namespaces
- [ ] `RuntimeClass` (`gvisor`/`kata`) required for all agentic workloads via Kyverno
- [ ] Images signed (cosign) and verified at admission; registries allow-listed; digests pinned
- [ ] Falco deployed with agentic-workload-specific rules; alerts routed to SOC tooling
- [ ] Velero + etcd snapshot backups scheduled and restore-tested quarterly
- [ ] `kube-bench` / Kubescape run clean (or exceptions tracked with owners/dates)

## Appendix D — Upgrade Runbook: 2-Node → HA 3-Control-Plane

1. Provision two additional control-plane VMs (`node-cp-02`, `node-cp-03`) with identical hardening (§5–§7).
2. Stand up an internal Azure Load Balancer (or HAProxy/keepalived pair) fronting `:6443` across all three control-plane nodes; update DNS for `controlPlaneEndpoint`.
3. Re-issue the `controlPlaneEndpoint` via `kubeadm init phase upload-certs --upload-certs` on `node-cp-01`, then join the two new nodes with `kubeadm join <LB-VIP>:6443 --control-plane --certificate-key <key>`.
4. Confirm a 3-member etcd quorum: `etcdctl member list` shows three healthy members.
5. Update `apiServer.certSANs` to include the load-balancer VIP/DNS name and re-run `kubeadm init phase certs apiserver` region if regenerating.

## Appendix E — Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `kubelet` fails to start, cgroup errors | cgroup driver mismatch | Ensure both containerd (`SystemdCgroup = true`) and `KubeletConfiguration.cgroupDriver: systemd` agree |
| Pods stuck `ContainerCreating`, CNI errors | Cilium not fully rolled out, or `kube-proxy` DS conflicting with `kubeProxyReplacement` | `cilium status --wait`; delete leftover `kube-proxy` DaemonSet |
| `kubeadm join` fails with cert hash mismatch | Stale/expired bootstrap token | `kubeadm token create --print-join-command` on the control plane |
| Kata pods never schedule | KVM unavailable (nested virtualization off) | Use a VM size with nested virtualization; verify `/dev/kvm` exists |
| SELinux denials block container start | Missing/incorrect SELinux type | Use `audit2allow` to build a targeted module; do not disable SELinux |
| Agent pod cannot reach its LLM API | FQDN egress policy too narrow / DNS not allow-listed | Confirm the DNS-allow rule precedes the FQDN rule; check `hubble observe --verdict DROPPED` |

## Appendix F — Sources

- Kubernetes official docs: kubeadm HA/etcd setup, `kubeadm-config.v1beta4` reference, Pod Security Admission, KMS provider docs — kubernetes.io
- Kubernetes blog, "CRI-O is moving towards pkgs.k8s.io" (Oct 2023) — community package repository migration
- Microsoft Tech Community: "Introducing Azure Linux with OS Guard" (Aug 2025), "Azure Linux: Driving Security in the Era of AI Innovation" (Nov 2025), EOL of Azure Linux 2.0 (Jul 2025)
- InfoWorld: "Up and running with Azure Linux 3.0" (Aug 2025)
- CNCF Blog: "Kubernetes hardening made easy: Running CIS Benchmarks with kube-bench" (Apr 2025)
- NSA/CISA Kubernetes Hardening Guidance (updated editions) and derivative summaries (CNCF benchmark report, Apr 2024)
- Cilium documentation and current community tutorials on WireGuard encryption, Hubble, FQDN/L7 policy (2025–2026)
- kubernetes-sigs/agent-sandbox project material and independent field-guide analyses on gVisor/Kata for AI agent isolation (2026), including CVE-2025-3248 (Langflow) analysis
- Kyverno vs OPA Gatekeeper comparative analyses (CNCF project status, 2025–2026)
- Falco documentation and eBPF driver guidance (2026)
- Azure Key Vault Provider for Secrets Store CSI Driver and Workload Identity documentation (Microsoft Learn / Tech Community)
- Velero documentation and production backup/DR guides (2025–2026)
- NVIDIA GPU Operator documentation
- Aqua Security kube-bench and Kubescape documentation

> **Disclaimer.** Package repository URLs, Marketplace image aliases, and exact current stable minor versions change over time — always cross-check `kubernetes.io/releases`, `pkgs.k8s.io`, and the Azure Linux Marketplace listing immediately before a real deployment, and pin every version explicitly in your own infrastructure-as-code.
