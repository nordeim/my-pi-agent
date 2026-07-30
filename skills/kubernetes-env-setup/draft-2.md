# Hardened Kubernetes on Azure Linux 3.0

## A Production Deployment Guide for Enterprise Agentic AI Workloads

**Document version:** 1.0 — 2026-07-30
**Target stack:** Azure Linux 3.0 (kernel 6.6 LTS) · Kubernetes v1.36.x · containerd 2.x · Cilium 1.20.x · Kyverno · Falco · gVisor + Kata Containers
**Topology:** 3 control-plane nodes (HA) + 2+ worker nodes; 2-node baseline documented as risk-accepted fallback
**Audience:** Platform/SRE engineers and security architects


## 1. Executive Summary & Design Principles

Agentic AI workloads are qualitatively different from ordinary microservices. They interpret natural language, generate and frequently **execute their own code**, invoke external tools and APIs, and act with a degree of autonomy that traditional web services do not have. This shifts the Kubernetes security calculus in three concrete ways.

**First, the container boundary alone is not sufficient.** A standard `runc` container shares the host kernel; an LLM agent that runs attacker-influenced generated code becomes a host-compromise vector under MITRE ATT&CK technique **T1611 — Escape to Host**. gVisor and Kata Containers, integrated via `RuntimeClass`, address this by providing sandboxed execution.

**Second, egress is the new perimeter.** Agents routinely call out to LLM providers, tool APIs, and external services. Traditional perimeter models that block inbound traffic say nothing about outbound data-exfiltration paths. Cilium's FQDN-based egress policies provide the necessary control.

**Third, secrets sprawl is structurally worse.** Agents need API keys at runtime. The Secrets Store CSI Driver with Azure Key Vault Provider and Entra Workload Identity ensures centralized, rotated, audited secret delivery without hardcoding credentials.

### 1.1 Design Principles

- **Defense in depth** — host hardening + Kubernetes hardening + workload sandboxing + policy enforcement + runtime detection
- **Least privilege everywhere** — RBAC scoped to Entra ID groups, NetworkPolicy default-deny, seccomp `RuntimeDefault`, all capabilities dropped
- **Immutable, measured infrastructure** — Azure Trusted Launch (Secure Boot + vTPM), signed RPM packages, `kubeadm`-managed control plane
- **Current, actively maintained stack** — `pkgs.k8s.io` package repositories, Cilium CNCF graduated, Kyverno CNCF graduated
- **HA-ready from day one** — three control-plane nodes, etcd quorum across availability zones

### 1.2 Why Self-Managed vs AKS

AKS is the more defensible choice for most enterprises: Microsoft operates the control plane, removing operational burden of patching, certificate rotation, and etcd backup. However, when the self-managed requirement is firm — common reasons include regulatory data-sovereignty constraints, need to control exact API server flags (`--encryption-provider-config`, `--audit-policy-file`), or air-gapped environments — this guide provides the canonical deployment path.


## 2. Reference Architecture

```
                            ┌──────────────────────────────────────────────────────────┐
                            │                       Azure Subscription                  │
                            │  ┌────────────────────────────────────────────────────┐  │
                            │  │   VNet 10.60.0.0/16                                 │  │
                            │  │                                                    │  │
                            │  │  ┌──────────────────────┐                          │  │
   Admin workstation        │  │  │ AzureBastionSubnet    │                          │  │
   (kubectl, SSH) ─ Bastion─┼──┼─▶│ 10.60.250.0/26        │                          │  │
                            │  │  └──────────────────────┘                          │  │
                            │  │                                                    │  │
                            │  │  ┌────────────────────────────────────────────────┐ │  │
                            │  │  │  Internal Std LB  10.60.1.100:6443           │ │  │
                            │  │  │  health probe: /healthz on 6443               │ │  │
                            │  │  └────────┬───────────────┬───────────────┬────────┘ │  │
                            │  │           │               │               │          │  │
                            │  │  ┌────────▼─────┐  ┌──────▼───────┐  ┌────▼────────┐  │  │
                            │  │  │ node-cp-01   │  │ node-cp-02   │  │ node-cp-03  │  │  │
                            │  │  │ AZ 1         │  │ AZ 2         │  │ AZ 3        │  │  │
                            │  │  │ Azure Linux  │  │ Azure Linux  │  │ Azure Linux │  │  │
                            │  │  │ 3.0 + TL     │  │ 3.0 + TL     │  │ 3.0 + TL    │  │  │
                            │  │  │ apiserver    │  │ apiserver    │  │ apiserver   │  │  │
                            │  │  │ ctrl-mgr     │  │ ctrl-mgr     │  │ ctrl-mgr    │  │  │
                            │  │  │ scheduler    │  │ scheduler    │  │ scheduler   │  │  │
                            │  │  │ etcd (P-SSD) │  │ etcd (P-SSD) │  │ etcd(P-SSD) │  │  │
                            │  │  │ containerd   │  │ containerd   │  │ containerd  │  │  │
                            │  │  │ Cilium (eBPF)│  │ Cilium (eBPF)│  │ Cilium(eBPF)│  │  │
                            │  │  └──────────────┘  └──────────────┘  └─────────────┘  │  │
                            │  │                                                    │  │
                            │  │  ┌─────────────────────┐   ┌──────────────────────┐  │  │
                            │  │  │ node-wk-01  AZ 1    │   │ node-wk-02  AZ 2     │  │  │
                            │  │  │ Azure Linux 3.0+TL  │   │ Azure Linux 3.0+TL   │  │  │
                            │  │  │ kubelet+containerd  │   │ kubelet+containerd   │  │  │
                            │  │  │ Cilium + Hubble rel │   │ Cilium + Hubble UI   │  │  │
                            │  │  │ RuntimeClasses:     │   │ RuntimeClasses:      │  │  │
                            │  │  │   runc  (infra)     │   │   runc  (infra)      │  │  │
                            │  │  │   gvisor (agents)   │   │   gvisor (agents)    │  │  │
                            │  │  │   kata (code-exec)  │   │   kata (code-exec)   │  │  │
                            │  │  │ Falco (eBPF)        │   │ Falco (eBPF)         │  │  │
                            │  │  └─────────────────────┘   └──────────────────────┘  │  │
                            │  └────────────────────────────────────────────────────┘  │  │
                            │                                                          │  │
                            │  Azure Key Vault  (KMS v2 + agent secrets)                │  │
                            │  Azure Container Registry (signed images, SBOM)           │  │
                            │  Azure Storage (Velero + etcd snapshots)                  │  │
                            │  Azure Monitor / Log Analytics (audit sink)               │  │
                            └──────────────────────────────────────────────────────────┘
```

### 2.1 Cluster Layer Stack

| Layer | Component | Version | Source |
|---|---|---|---|
| Host OS | Azure Linux 3.0 | kernel 6.6 LTS | Microsoft GA |
| Container runtime | containerd | 2.x | `moby-containerd` package |
| Cluster bootstrapper | kubeadm | v1beta4 config API | Kubernetes docs |
| Kubernetes | kube-apiserver / kubelet / kubectl | v1.36.x | pkgs.k8s.io |
| CNI | Cilium | 1.20.x | CNCF graduated |
| Sandbox runtimes | gVisor (`runsc`), Kata Containers | latest | google/gvisor, kata-containers |
| Policy engine | Kyverno | latest (CNCF graduated) | kyverno/kyverno |
| Runtime security | Falco | modern_ebpf probe | CNCF graduated |
| Secrets | Secrets Store CSI Driver + Azure Key Vault | latest | Azure/aks |
| Backup | Velero + Azure plugin | 1.17.x | vmware-tanzu/velero |


## 3. Prerequisites & Azure Infrastructure

### 3.1 Required Tooling

- Azure CLI ≥ 2.72
- `kubectl`, `helm` ≥ 3.14
- `cilium` CLI ≥ 0.16
- `cosign` ≥ 2.4, `syft` ≥ 1.0, `trivy` ≥ 0.55
- `velero` CLI ≥ 1.17
- SSH key pair (Ed25519 recommended)

### 3.2 Azure Resources

```bash
export RG="rg-agentic-k8s-prod"
export LOC="eastus2"
export VNET="vnet-agentic-k8s"
export CP_LB_IP="10.60.1.100"
export CP_VM_PREFIX="node-cp-"
export WK_VM_PREFIX="node-wk-"
export ADMIN_USER="k8sadmin"
export KV_NAME="kv-agentic-k8s-${LOC}"
export ACR_NAME="acragentick8s${LOC}"
export STORAGE_NAME="stagentick8s${LOC}"

az group create -n "$RG" -l "$LOC"

# VNet with subnets
az network vnet create -g "$RG" -n "$VNET" --address-prefix 10.60.0.0/16 \
  --subnet-name cp-subnet --subnet-prefix 10.60.1.0/24
az network vnet subnet create -g "$RG" --vnet-name "$VNET" \
  --name worker-subnet --address-prefix 10.60.2.0/24
az network vnet subnet create -g "$RG" --vnet-name "$VNET" \
  --name AzureBastionSubnet --address-prefix 10.60.250.0/26

# Bastion (no public SSH)
az network public-ip create -g "$RG" -n pip-bastion --sku Standard
az network bastion create -g "$RG" -n bastion-agentic-k8s \
  --vnet-name "$VNET" --public-ip-address pip-bastion --location "$LOC" --sku Standard

# Internal Load Balancer for API server
az network lb create -g "$RG" -n lb-k8s-apiserver --sku Standard \
  --vnet-name "$VNET" --subnet cp-subnet --frontend-ip-name fe-apiserver \
  --private-ip-address "$CP_LB_IP" --backend-pool-name be-apiserver
az network lb probe create -g "$RG" --lb-name lb-k8s-apiserver -n probe-apiserver \
  --protocol Https --path /healthz --port 6443 --interval 5
az network lb rule create -g "$RG" --lb-name lb-k8s-apiserver -n rule-apiserver \
  --frontend-ip-name fe-apiserver --backend-pool-name be-apiserver \
  --frontend-port 6443 --backend-port 6443 --protocol Tcp \
  --probe-name probe-apiserver
```

### 3.3 VM Sizing

| Node | SKU | vCPU/RAM | Storage |
|---|---|---|---|
| Control plane (×3) | `Standard_D4s_v5` | 4 / 16 GiB | 128 GB OS + 64 GB Premium SSD v2 for etcd |
| Worker (×2+) | `Standard_D8s_v5` | 8 / 32 GiB | 256 GB OS |

All VMs require **Trusted Launch**:
```bash
az vm create -g "$RG" -n "${CP_VM_PREFIX}01" \
  --image MicrosoftAzureLinux:azure-linux:3-gen2:latest \
  --size Standard_D4s_v5 --vnet-name "$VNET" --subnet cp-subnet \
  --nsg nsg-cp --public-ip-address "" \
  --admin-username "$ADMIN_USER" --ssh-key-values ~/.ssh/id_ed25519.pub \
  --security-type TrustedLaunch --enable-secure-boot true --enable-vtpm true
```

### 3.4 Supporting Services

```bash
# Key Vault (RBAC mode, private endpoint)
az keyvault create -g "$RG" -n "$KV_NAME" --enable-rbac-authorization true \
  --sku standard --public-network-access disabled

# Azure Container Registry (Premium)
az acr create -g "$RG" -n "$ACR_NAME" --sku Premium --admin-enabled false \
  --public-network-enabled false

# Storage for backups
az storage account create -g "$RG" -n "$STORAGE_NAME" --sku Standard_GRS \
  --https-only true --min-tls-version TLS1_2 --allow-blob-public-access false
```


## 4. Host OS Provisioning & Hardening

Azure Linux 3.0 ships with **SELinux enforcing by default**, Secure Boot, and vTPM integration. Run the following on **every node**.

### 4.1 Baseline Update

```bash
sudo tdnf makecache
sudo tdnf update -y
sudo tdnf install -y chrony auditd firewalld policycoreutils-python-utils \
  container-selinux tar curl jq socat conntrack-tools
```

### 4.2 Kernel Modules & Sysctl Hardening

```bash
sudo tee /etc/modules-load.d/k8s.conf >/dev/null <<EOF
overlay
br_netfilter
EOF
sudo modprobe overlay && sudo modprobe br_netfilter

sudo tee /etc/sysctl.d/99-kubernetes-hardening.conf >/dev/null <<'EOF'
net.bridge.bridge-nf-call-iptables   = 1
net.bridge.bridge-nf-call-ip6tables  = 1
net.ipv4.ip_forward                  = 1
kernel.kptr_restrict                 = 2
kernel.dmesg_restrict                = 1
kernel.perf_event_paranoid           = 3
kernel.unprivileged_bpf_disabled     = 1
fs.protected_hardlinks               = 1
fs.protected_symlinks                = 1
fs.suid_dumpable                     = 0
net.ipv4.conf.all.rp_filter          = 1
net.ipv4.conf.all.accept_redirects   = 0
net.ipv4.conf.all.send_redirects     = 0
net.ipv4.tcp_syncookies              = 1
EOF
sudo sysctl --system
```

### 4.3 Disable Swap

```bash
sudo swapoff -a
sudo sed -ri '/\sswap\s/s/^/#/' /etc/fstab
```

### 4.4 SELinux — Keep Enforcing

Azure Linux has SELinux in enforcing mode by default. Do **not** disable it:

```bash
getenforce   # Expect: Enforcing
sudo tdnf install -y container-selinux
sudo setsebool -P container_manage_cgroup on
```

### 4.5 Firewall

```bash
sudo systemctl enable --now firewalld

# Control-plane ports
sudo firewall-cmd --permanent --add-port=6443/tcp
sudo firewall-cmd --permanent --add-port=2379-2380/tcp
sudo firewall-cmd --permanent --add-port=10250-10252/tcp
sudo firewall-cmd --permanent --add-port=10257/tcp
sudo firewall-cmd --permanent --add-port=10259/tcp

# Cilium ports (both nodes)
sudo firewall-cmd --permanent --add-port=4240/tcp
sudo firewall-cmd --permanent --add-port=8472/udp
sudo firewall-cmd --permanent --add-port=51871/udp
sudo firewall-cmd --reload
```

### 4.6 SSH Hardening

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

### 4.7 auditd Baseline

```bash
sudo tee /etc/audit/rules.d/k8s-node.rules >/dev/null <<'EOF'
-w /etc/kubernetes/ -p wa -k k8s-config
-w /var/lib/etcd/   -p wa -k etcd-data
-w /etc/containerd/ -p wa -k containerd-config
-w /usr/bin/kubelet -p x  -k kubelet-exec
-w /usr/bin/containerd -p x -k containerd-exec
EOF
sudo augenrules --load
sudo systemctl enable --now auditd
```

### 4.8 Pinned Patching

```bash
sudo tee /etc/tdnf/tdnf.conf.d/hold-k8s.conf >/dev/null <<'EOF'
[main]
exclude=kubelet kubeadm kubectl moby-containerd containerd
EOF

sudo tee /etc/systemd/system/tdnf-security.timer >/dev/null <<'EOF'
[Unit]
Description=Weekly Azure Linux security updates
[Timer]
OnCalendar=Sun 04:00:00
Persistent=true
[Install]
WantedBy=timers.target
EOF
sudo systemctl enable --now tdnf-security.timer
```


## 5. Container Runtime Installation (containerd)

Azure Linux ships containerd 2.x as `moby-containerd`.

```bash
sudo tdnf install -y moby-containerd runc
sudo mkdir -p /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml >/dev/null

sudo sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml
sudo sed -i 's#sandbox_image = .*#sandbox_image = "registry.k8s.io/pause:3.10"#' \
  /etc/containerd/config.toml

sudo systemctl enable --now containerd
stat -fc %T /sys/fs/cgroup/   # Expect: cgroup2fs
```


## 6. Kubernetes Package Installation (pkgs.k8s.io)

Since March 4, 2024, legacy Google-hosted repositories are frozen. All Kubernetes packages are now at `pkgs.k8s.io`.

```bash
export K8S_MINOR="1.36"

sudo tee /etc/yum.repos.d/kubernetes.repo >/dev/null <<EOF
[kubernetes]
name=Kubernetes
baseurl=https://pkgs.k8s.io/core:/stable:/v${K8S_MINOR}/rpm/
enabled=1
gpgcheck=1
gpgkey=https://pkgs.k8s.io/core:/stable:/v${K8S_MINOR}/rpm/repodata/repomd.xml.key
exclude=kubelet kubeadm kubectl cri-tools kubernetes-cni
EOF

sudo tdnf install -y kubelet kubeadm kubectl cri-tools kubernetes-cni
sudo systemctl enable --now kubelet
```


## 7. Bootstrapping the Control Plane

### 7.1 kubeadm v1beta4 Configuration

Create `/etc/kubernetes/kubeadm-config.yaml` on `node-cp-01`:

```yaml
apiVersion: kubeadm.k8s.io/v1beta4
kind: InitConfiguration
nodeRegistration:
  name: "node-cp-01"
  criSocket: "unix:///run/containerd/containerd.sock"
  taints:
    - key: "node-role.kubernetes.io/control-plane"
      effect: "NoSchedule"
---
apiVersion: kubeadm.k8s.io/v1beta4
kind: ClusterConfiguration
kubernetesVersion: "v1.36.2"
clusterName: "agentic-k8s-prod"
controlPlaneEndpoint: "10.60.1.100:6443"
apiServer:
  certSANs:
    - "10.60.1.100"
    - "10.60.1.4"
    - "10.60.1.5"
    - "10.60.1.6"
    - "node-cp-01"
    - "node-cp-02"
    - "node-cp-03"
  extraArgs:
    authorization-mode: "Node,RBAC"
    audit-log-path: "/var/log/kubernetes/audit/audit.log"
    audit-log-maxage: "30"
    audit-log-maxbackup: "10"
    audit-policy-file: "/etc/kubernetes/audit-policy.yaml"
    encryption-provider-config: "/etc/kubernetes/encryption-provider.yaml"
    profiling: "false"
controllerManager:
  extraArgs:
    profiling: "false"
scheduler:
  extraArgs:
    profiling: "false"
etcd:
  local:
    dataDir: "/var/lib/etcd"
networking:
  podSubnet: "10.244.0.0/16"
  serviceSubnet: "10.96.0.0/12"
  dnsDomain: "cluster.local"
---
apiVersion: kubelet.config.k8s.io/v1
kind: KubeletConfiguration
cgroupDriver: "systemd"
rotateCertificates: true
serverTLSBootstrap: true
protectKernelDefaults: true
```

### 7.2 Audit Policy

Create `/etc/kubernetes/audit-policy.yaml`:

```yaml
apiVersion: audit.k8s.io/v1
kind: Policy
omitStages: ["RequestReceived"]
rules:
  - level: Metadata
    resources:
      - group: ""
        resources: ["secrets", "configmaps"]
  - level: RequestResponse
    resources:
      - group: "rbac.authorization.k8s.io"
        resources: ["roles", "rolebindings", "clusterroles", "clusterrolebindings"]
  - level: RequestResponse
    resources:
      - group: "admissionregistration.k8s.io"
        resources: ["validatingadmissionpolicies", "validatingadmissionpolicybindings"]
  - level: Metadata
```

### 7.3 Encryption Provider (KMS v2)

Create `/etc/kubernetes/encryption-provider.yaml`:

```yaml
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
  - resources:
      - secrets
    providers:
      - kms:
          apiVersion: v2
          name: azure-key-vault
          endpoint: unix:///var/run/azurekms/kms.sock
          timeout: 3s
      - identity: {}
```

### 7.4 Initialize

```bash
sudo mkdir -p /var/log/kubernetes/audit
sudo kubeadm init --config /etc/kubernetes/kubeadm-config.yaml \
  --upload-certs \
  --skip-phases=addon/kube-proxy

mkdir -p "$HOME/.kube"
sudo cp -i /etc/kubernetes/admin.conf "$HOME/.kube/config"
sudo chown "$(id -u):$(id -g)" "$HOME/.kube/config"
```

### 7.5 Join Additional Control-Plane Nodes

On `node-cp-02` and `node-cp-03`:

```bash
sudo kubeadm join 10.60.1.100:6443 \
  --token <token> \
  --discovery-token-ca-cert-hash sha256:<hash> \
  --control-plane --certificate-key <key>
```


## 8. CNI: Cilium (eBPF, kube-proxy Replacement, Encryption)

Cilium is the most widely adopted CNI in production, powering clusters at Google, Microsoft, and AWS. It replaces kube-proxy, enforces L3/L4/L7 network policies, provides WireGuard encryption, and offers Hubble observability.

### 8.1 Install Cilium

```bash
helm repo add cilium https://helm.cilium.io/
helm repo update

helm install cilium cilium/cilium --version 1.20.0 \
  --namespace kube-system \
  --set kubeProxyReplacement=true \
  --set k8sServiceHost="10.60.1.100" \
  --set k8sServicePort="6443" \
  --set encryption.enabled=true \
  --set encryption.type=wireguard \
  --set hubble.enabled=true \
  --set hubble.relay.enabled=true \
  --set hubble.ui.enabled=true \
  --set operator.replicas=2

cilium status --wait
```

### 8.2 Default-Deny NetworkPolicy

When an endpoint is selected by a network policy, it transitions to a default-deny state:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: agents-prod
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
```

### 8.3 FQDN-Based Egress for Agentic Workloads

Cilium's FQDN filtering evaluates DNS requests to determine allowed destinations:

```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: agent-egress-allowlist
  namespace: agents-prod
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
              protocol: UDP
          rules:
            dns:
              - matchPattern: "*"
    - toFQDNs:
        - matchName: "api.openai.com"
        - matchPattern: "*.openai.azure.com"
        - matchPattern: "*.cognitiveservices.azure.com"
      toPorts:
        - ports:
            - port: "443"
              protocol: TCP
```


## 9. Sandboxing Agentic Workloads

Standard containers share the host kernel — a kernel exploit compromises the entire node. **gVisor** provides a user-space kernel that intercepts syscalls; **Kata Containers** runs each pod in a lightweight VM for hardware-level isolation.

### 9.1 Install gVisor

```bash
curl -fsSL https://gvisor.dev/archive.key | sudo gpg --dearmor -o \
  /usr/share/keyrings/gvisor-archive-keyring.gpg
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

### 9.2 Install Kata Containers

```bash
sudo tdnf install -y qemu-kvm qemu-img
KATA_VERSION=$(curl -s https://api.github.com/repos/kata-containers/kata-containers/releases/latest | jq -r .tag_name)
curl -fsSL -o kata-static.tar.xz \
  "https://github.com/kata-containers/kata-containers/releases/download/${KATA_VERSION}/kata-static-${KATA_VERSION#v}-x86_64.tar.xz"
sudo tar -xf kata-static.tar.xz -C /
sudo ln -sf /opt/kata/bin/containerd-shim-kata-v2 /usr/local/bin/
sudo ln -sf /opt/kata/bin/kata-runtime /usr/local/bin/

sudo tee -a /etc/containerd/config.toml >/dev/null <<'EOF'
[plugins."io.containerd.grpc.v1.cri".containerd.runtimes.kata]
  runtime_type = "io.containerd.kata.v2"
  privileged_without_host_devices = true
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

### 9.3 Sandboxed Pod Example

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: code-exec-agent
  namespace: agents-prod
spec:
  replicas: 3
  template:
    spec:
      runtimeClassName: kata
      securityContext:
        runAsNonRoot: true
        runAsUser: 10001
        seccompProfile:
          type: RuntimeDefault
      containers:
        - name: agent
          image: <acr>.azurecr.io/agents/code-exec-agent:signed-1.0.0
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop: ["ALL"]
          resources:
            limits:
              cpu: "2"
              memory: "4Gi"
```


## 10. Policy-as-Code with Kyverno

Kyverno enforces policies as Kubernetes resources — no new language to learn. It validates, mutates, and generates resources using YAML policies.

### 10.1 Install Kyverno

```bash
helm repo add kyverno https://kyverno.github.io/kyverno/
helm install kyverno kyverno/kyverno -n kyverno --create-namespace
```

### 10.2 Require Sandboxed RuntimeClass

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
              namespaces: ["agents-prod"]
      validate:
        message: "Agentic workloads must use gvisor or kata RuntimeClass."
        pattern:
          spec:
            runtimeClassName: "gvisor | kata"
```

### 10.3 Require Signed Images

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
              namespaces: ["agents-prod"]
      verifyImages:
        - imageReferences:
            - "<acr-name>.azurecr.io/*"
          attestors:
            - count: 1
              entries:
                - keyless:
                    subject: "https://github.com/<org>/<repo>/.github/workflows/build.yml@refs/heads/main"
                    issuer: "https://token.actions.githubusercontent.com"
                    rekor:
                      url: "https://rekor.sigstore.dev"
```


## 11. Runtime Security with Falco

Falco monitors kernel-level system calls using eBPF. It catches runtime threats that configuration scanners miss — shells spawned in containers, reverse shells, sensitive file access, unexpected outbound traffic.

### 11.1 Install Falco

For kernel 5.8+ clusters, `modern_ebpf` is the right choice:

```bash
helm repo add falcosecurity https://falcosecurity.github.io/charts/
helm install falco falcosecurity/falco \
  --namespace falco --create-namespace \
  --set driver.kind=modern_ebpf \
  --set collectors.kubernetes.enabled=true \
  --set falcosidekick.enabled=true
```

### 11.2 Agentic-Workload Rules

```yaml
# /etc/falco/rules.d/agentic-workloads.yaml
- rule: Agent Spawned Shell
  desc: Agent pod spawned a shell — likely prompt injection
  condition: >
    agent_namespace and evt.type in (execve, execveat) and
    proc.name in (bash, sh, zsh)
  output: "Agent shell spawn (pod=%k8s.pod.name cmd=%proc.cmdline)"
  priority: WARNING

- rule: Agent Reverse Shell
  desc: Agent pod opened connection and spawned shell
  condition: >
    agent_namespace and evt.type=connect and
    fd.sip != "127.0.0.1" and proc.name in (bash, sh, zsh)
  output: "Agent reverse shell (pod=%k8s.pod.name dest=%fd.sip:%fd.sport)"
  priority: CRITICAL
```


## 12. Secrets Management

### 12.1 Install Secrets Store CSI Driver

The Azure Key Vault provider for Secrets Store CSI Driver mounts secrets, keys, and certificates to pods via CSI volume:

```bash
helm repo add secrets-store-csi-driver https://kubernetes-sigs.github.io/secrets-store-csi-driver/charts
helm repo add csi-secrets-store-provider-azure https://azure.github.io/secrets-store-csi-driver-provider-azure/charts

helm install csi-secrets-store secrets-store-csi-driver/secrets-store-csi-driver \
  -n kube-system --set enableSecretRotation=true --set rotationPollInterval=60m

helm install csi-secrets-store-provider-azure \
  csi-secrets-store-provider-azure/csi-secrets-store-provider-azure -n kube-system
```

### 12.2 SecretProviderClass

```yaml
apiVersion: secrets-store.csi.x-k8s.io/v1
kind: SecretProviderClass
metadata:
  name: llm-api-key
  namespace: agents-prod
spec:
  provider: azure
  parameters:
    usePodIdentity: "false"
    clientID: "<workload-identity-client-id>"
    keyvaultName: "<kv-name>"
    tenantId: "<entra-tenant-id>"
    objects: |
      array:
        - objectName: "openai-api-key"
          objectType: "secret"
```


## 13. Backup & Disaster Recovery

### 13.1 etcd Snapshots

```bash
sudo ETCDCTL_API=3 etcdctl snapshot save /var/backups/etcd/etcd-snapshot-$(date +%F).db \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key

az storage blob upload --account-name "$STORAGE_NAME" --container-name etcd-backups \
  --file /var/backups/etcd/etcd-snapshot-$(date +%F).db \
  --name etcd-snapshot-$(date +%F).db
```

### 13.2 Velero

Velero uses Azure Blob Storage for backup persistence:

```bash
velero install \
  --provider azure \
  --plugins velero/velero-plugin-for-microsoft-azure:latest \
  --bucket velero-backups \
  --secret-file ./credentials-velero \
  --backup-location-config resourceGroup=$RG,storageAccount=$STORAGE_NAME \
  --snapshot-location-config apiTimeout=5m,resourceGroup=$RG

velero schedule create daily-backup \
  --schedule="0 2 * * *" --ttl 720h --include-namespaces agents-prod
```


## 14. Compliance Validation

### 14.1 kube-bench (CIS Benchmark)

kube-bench checks Kubernetes against the CIS Kubernetes Benchmark:

```bash
kubectl apply -f https://raw.githubusercontent.com/aquasecurity/kube-bench/main/job.yaml
kubectl logs -l app=kube-bench --tail=-1
```

### 14.2 Kubescape

Kubescape 4.0 (announced March 2026 at KubeCon Europe) brings runtime threat detection to GA and addresses AI-native security challenges:

```bash
helm repo add kubescape https://kubescape.github.io/helm-charts/
helm install kubescape kubescape/kubescape-operator -n kubescape --create-namespace

kubescape scan framework nsa --submit
kubescape scan framework cis-v1.10.0 --submit
```


## 15. Hardening Checklist

- [ ] Trusted Launch (Secure Boot + vTPM) enabled on all VMs
- [ ] SELinux `Enforcing` on all nodes
- [ ] Swap disabled; kernel sysctl hardening applied
- [ ] No public IPs; Bastion-only SSH; password auth disabled
- [ ] `anonymous-auth=false`, `authorization-mode=Node,RBAC`
- [ ] Audit logging enabled with tamper-evident sink
- [ ] etcd encryption at rest (KMS v2 + Key Vault)
- [ ] Cilium installed with `kubeProxyReplacement`, WireGuard encryption, Hubble
- [ ] Default-deny NetworkPolicy applied cluster-wide
- [ ] Agent egress scoped to explicit FQDN allow-lists
- [ ] Pod Security Admission `restricted` enforced
- [ ] `RuntimeClass` (`gvisor`/`kata`) required for agentic workloads
- [ ] Images signed (cosign) and verified at admission
- [ ] Falco deployed with agentic-workload-specific rules
- [ ] Velero + etcd snapshot backups scheduled and tested


## Appendix: Key Sources

| Source | Reference |
|---|---|
| Azure Linux 3.0 GA with AKS v1.32 | Microsoft Tech Community |
| pkgs.k8s.io community-owned repositories | Kubernetes blog |
| Cilium eBPF networking | Cilium docs |
| gVisor RuntimeClass | K8s Recipes |
| Kata Containers RuntimeClass | K8s Recipes |
| Kyverno policy engine | K8s Recipes |
| Falco runtime security | Falco docs |
| Secrets Store CSI + Azure Key Vault | Microsoft Learn |
| Velero on Azure | Velero plugin docs |
| Kubescape 4.0 | CNCF blog |
| SELinux enforcing on Azure Linux | Microsoft Learn |
| Cilium FQDN filtering | Azure docs |

---

> **Disclaimer.** Package repository URLs, Marketplace image aliases, and exact current stable versions change over time — always cross-check `kubernetes.io/releases`, `pkgs.k8s.io`, and the Azure Linux Marketplace listing before deployment. The 2-node topology (1 control-plane + 1 worker) is a **risk-accepted fallback** for non-production use only; production deployments require 3 control-plane nodes for etcd quorum.
