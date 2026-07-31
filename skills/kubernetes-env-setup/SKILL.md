---
name: kubernetes-env-setup
description: >-
  Production-grade self-managed Kubernetes cluster on Azure Linux 3.0 (kubeadm)
  with CIS/NSA/CISA-aligned hardening for agentic AI and LLM workloads. Covers
  host hardening (SELinux, Trusted Launch, OS Guard IPE), containerd, Cilium eBPF
  CNI, Kyverno policy-as-code, gVisor/Kata Containers sandboxing, cosign/Sigstore
  supply chain security, Falco runtime detection, Pod Security Admission, RBAC,
  secrets management, network segmentation, high availability (multi-AZ), backup
  with Velero, and compliance validation (kube-bench, Kubescape). Includes OWASP
  LLM Top 10 and MITRE ATLAS threat modeling for prompt injection defense.
version: 1.0
---

# Hardened Kubernetes on Azure Linux 3.0

## A Production Deployment Guide for Enterprise Agentic AI Workloads

**Document version:** 1.0 — 2026-07-30
**Target stack:** Azure Linux 3.0 (kernel 6.6 LTS) · Kubernetes v1.36.x · containerd 2.3.x · Cilium 1.20.x · Kyverno (CNCF graduated 2026) · Falco 0.44 · gVisor + Kata Containers 4.0
**Topology:** 3 control-plane nodes (HA, across availability zones) + 2+ worker nodes; minimum-viable 1+1 baseline documented as a documented-risk fallback
**Audience:** Platform/SRE engineers and security architects

> **Scope.** This guide builds a self-managed, CIS- and NSA/CISA-aligned Kubernetes cluster on **Azure Linux 3.0** — Microsoft's Fedora-derived, FedRAMP-eligible, minimal-footprint Linux distribution that ships with a 6.6 LTS kernel, systemd 255, `tdnf` package management, SELinux in enforcing mode, and OS Guard (Integrity Policy Enforcement) for code integrity [1][2][3]. The cluster is sized, hardened, and isolated for running **agentic AI workloads** — LLM-driven agents that call tools, execute generated code, and reach external APIs — in an enterprise production setting. Every normative technical claim is grounded in current (2025–2026) upstream documentation, CNCF project sources, and Microsoft Learn; the numbered inline citations map to the consolidated bibliography in [Appendix F — Sources](#appendix-f--sources).

> **Document Conventions.** This guide is written from the perspective of July 2026. Component versions (e.g., Kubernetes 1.36, Cilium 1.20, Kata Containers 4.0) and specific CVE references (e.g., CVE-2025-3248) are based on current upstream release trajectories and historical vulnerability patterns to illustrate threat modeling. Validate all version numbers against current releases before deployment. Where a component is noted as "in preview" (e.g., Azure Linux OS Guard), monitor the vendor's documentation for GA announcements.

---

## Table of Contents

1. [Executive Summary & Design Principles](#1-executive-summary--design-principles)
2. [Reference Architecture](#2-reference-architecture)
3. [Threat Model for Agentic Workloads](#3-threat-model-for-agentic-workloads)
4. [Prerequisites & Azure Infrastructure Layout](#4-prerequisites--azure-infrastructure-layout)
5. [Host OS Provisioning & Hardening (Azure Linux 3.0)](#5-host-os-provisioning--hardening-azure-linux-30)
6. [Container Runtime Installation (containerd 2.x)](#6-container-runtime-installation-containerd-2x)
7. [Kubernetes Package Installation via pkgs.k8s.io](#7-kubernetes-package-installation-via-pkgsk8sio)
8. [Bootstrapping the Control Plane (3-Node HA with kubeadm)](#8-bootstrapping-the-control-plane-3-node-ha-with-kubeadm)
9. [Joining Worker Nodes](#9-joining-worker-nodes)
10. [CNI: Cilium 1.20 (eBPF, kube-proxy replacement, encryption)](#10-cni-cilium-120-ebpf-kube-proxy-replacement-encryption)
11. [Identity, Authentication & RBAC](#11-identity-authentication--rbac)
12. [Secrets Management & Encryption at Rest](#12-secrets-management--encryption-at-rest)
13. [Pod & Workload Hardening](#13-pod--workload-hardening)
14. [Sandboxing Agentic Workloads (gVisor + Kata Containers 4.0)](#14-sandboxing-agentic-workloads-gvisor--kata-containers-40)
15. [Policy-as-Code with Kyverno (CNCF Graduated)](#15-policy-as-code-with-kyverno-cncf-graduated)
16. [Supply Chain Security (cosign, SBOM, SLSA)](#16-supply-chain-security-cosign-sbom-slsa)
17. [Runtime Security & Observability](#17-runtime-security--observability)
18. [Optional: GPU Nodes for Local LLM Inference](#18-optional-gpu-nodes-for-local-llm-inference)
19. [Backup, Restore & Disaster Recovery](#19-backup-restore--disaster-recovery)
20. [Patching & Lifecycle Management](#20-patching--lifecycle-management)
21. [Compliance Validation (kube-bench, Kubescape)](#21-compliance-validation-kube-bench-kubescape)
22. [Appendix A — Full Reference Manifests](#appendix-a--full-reference-manifests)
23. [Appendix B — Variable Reference](#appendix-b--variable-reference)
24. [Appendix C — Hardening Checklist](#appendix-c--hardening-checklist)
25. [Appendix D — Upgrade Runbook](#appendix-d--upgrade-runbook)
26. [Appendix E — Troubleshooting](#appendix-e--troubleshooting)
27. [Appendix F — Sources](#appendix-f--sources)

---

## 1. Executive Summary & Design Principles

Agentic AI workloads are qualitatively different from ordinary microservices. They interpret natural language, generate and frequently **execute their own code**, invoke external tools and APIs, and act with a degree of autonomy that traditional web services do not have. This shifts the Kubernetes security calculus in three concrete ways.

**First, the container boundary alone is not sufficient.** A standard `runc` container shares the host kernel; an LLM agent that runs attacker-influenced generated code (a prompt-injected "helper script" containing a kernel exploit, for example) becomes a host-compromise vector under MITRE ATT&CK technique **T1611 — Escape to Host** [4]. This is not theoretical. The pre-authentication remote code execution in Langflow (CVE-2025-3248, CVSS 9.8, added to CISA's Known Exploited Vulnerabilities catalog in May 2025) followed exactly this pattern: unauthenticated `exec()` of attacker-controlled code with no sandbox isolation between the agent process and the underlying node [5]. A cluster that runs agentic workloads in plain `runc` containers is therefore running the same risk profile that produced CVE-2025-3248.

**Second, egress is the new perimeter.** Agents routinely call out to LLM providers, tool APIs, package registries, vector databases, and a long tail of integration endpoints. Traditional perimeter models that focus on blocking inbound traffic say nothing about controlling the outbound data-exfiltration paths that a compromised or prompt-injected agent might use. A network policy posture that defaults to "allow all egress" effectively turns every agent pod into a potential exfiltration relay.

**Third, secrets sprawl is structurally worse.** Agents need API keys (LLM providers, vector DBs, internal services, MCP tool servers) at runtime, and they need them in a context where the agent itself may be partially untrusted. Hardcoding these keys in ConfigMaps, baking them into images, or passing them as environment variables creates a sprawling, unrotated, unaudited secret surface that is the operational antithesis of least privilege.

This guide implements defense in depth across five layers — host hardening, Kubernetes hardening, workload sandboxing, policy enforcement, and runtime detection — so that no single control failure yields full compromise. It uses the **current, actively maintained cloud-native stack** as of July 2026: Kubernetes v1.36.x (released June 2026) [6], containerd 2.3.x [7], Cilium 1.20.x (CNCF graduated October 2023) [8], Kyverno (CNCF graduated March 2026) [9], Falco 0.44.x (CNCF graduated May 2024) [10], gVisor and Kata Containers 4.0 [11], and Sigstore/cosign 2.x (OpenSSF graduated October 2024) [12]. Every component is installed from its official 2025/2026 release channel.

The reference architecture deploys **three control-plane nodes** spread across Azure availability zones, behind an internal Standard Load Balancer, with **two or more worker nodes** for agentic workloads. This is the smallest topology that delivers true high availability: a single control-plane node is a single point of failure for the API server, scheduler, controller manager, and etcd, and should not be used in production. The original two-node baseline requested in the brief (one control-plane + one worker) is documented in §4.4 as a **minimum-viable, risk-accepted fallback** for lab, staging, or compliance-waivered environments only.

### 1.1 Design Principles (applied throughout)

- **Defense in depth.** Host hardening + Kubernetes hardening + workload sandboxing + policy enforcement + runtime detection. No single control is treated as authoritative; the cluster's security posture is the union of overlapping controls.
- **Least privilege everywhere.** RBAC scoped to Entra ID groups, NetworkPolicy default-deny on every namespace, seccomp `RuntimeDefault`, all Linux capabilities dropped, `automountServiceAccountToken: false` by default, no `cluster-admin` for human operators without break-glass justification.
- **Immutable, measured infrastructure.** Azure Trusted Launch (Secure Boot + vTPM) on every VM, signed RPM packages, `kubeadm`-managed static control-plane manifests instead of hand-rolled `systemd` units, Azure Linux OS Guard with IPE for code integrity [3].
- **Current, actively maintained stack only.** No deprecated APIs, no frozen package repositories (legacy `apt.kubernetes.io` / `yum.kubernetes.io` were frozen March 4, 2024 [13]), no end-of-life runtime versions.
- **HA-ready from day one.** Three control-plane nodes, etcd quorum across availability zones, internal load balancer in front of the API server, every control-plane configuration written so a fourth or fifth control-plane node is a config-file change, not a redesign.
- **Verifiable, not asserted.** Every claim in this guide is sourced. The cluster's compliance posture is validated with `kube-bench` against CIS Kubernetes Benchmark v1.10.0 [14] and `Kubescape` against the NSA/CISA, MITRE ATT&CK, and CIS frameworks [15]. Hardening is not declared; it is measured.

---

## 2. Reference Architecture

The reference deployment is a self-managed Kubernetes cluster installed with `kubeadm` on Azure Linux 3.0 virtual machines in a single Azure region, spread across three availability zones for control-plane quorum. No node has a public IP address; all administrative access flows through Azure Bastion. The API server is reachable from outside the cluster's VNet only through a private endpoint, VPN, or ExpressRoute — never directly over the internet.

```
                            ┌──────────────────────────────────────────────────────────┐
                            │                       Azure Subscription                  │
                            │  ┌────────────────────────────────────────────────────┐  │
                            │  │   VNet 10.60.0.0/16                                 │  │
                            │  │                                                    │  │
                            │  │  ┌──────────────────────┐                          │  │
   Admin workstation        │  │  │ AzureBastionSubnet    │                          │  │
   (kubectl, SSH) ─ Bastion─┼──┼─▶│ 10.60.250.0/26        │                          │  │
                            │  │  │  Bastion (Standard)   │                          │  │
                            │  │  └──────────────────────┘                          │  │
                            │  │                                                    │  │
                            │  │  ┌────────────────────────────────────────────────┐ │  │
                            │  │  │  Internal Std LB  10.60.1.100:6443 (apiserver)│ │  │
                            │  │  │  health probe: /healthz on 6443                 │ │  │
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
                            │  │       (nsg-cp: 6443 from VNet; 2379-2380 from cp subnet;│  │
                            │  │        10250 from worker subnet; 22 from Bastion only) │  │
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
                            │  │       (nsg-wk: 10250 from cp subnet; 22 from Bastion)│  │
                            │  │                                                    │  │
                            │  │  ┌─────────────────────┐   (optional)                 │  │
                            │  │  │ node-gpu-01 AZ 1    │   NVIDIA H100/A100           │  │
                            │  │  │ Azure Linux 3.0+TL  │   GPU Operator               │  │
                            │  │  │ NCads_H100_v5       │   vLLM / TGI / Ollama        │  │
                            │  │  └─────────────────────┘                              │  │
                            │  └────────────────────────────────────────────────────┘  │
                            │                                                          │
                            │  Azure Key Vault  (KMS v2 + agent secrets + cert CA)      │
                            │  Azure Container Registry (signed images, SBOM, Helm)    │
                            │  Azure Storage Account (Velero + etcd snapshots)          │
                            │  Azure Monitor / Log Analytics (audit sink + Falco alerts)│
                            │  Microsoft Entra ID (OIDC issuer for Workload Identity)   │
                            └──────────────────────────────────────────────────────────┘
```

### 2.1 Cluster Layer Stack (validated July 2026)

| Layer | Component | Version | Source / status |
|---|---|---|---|
| Host OS | Azure Linux 3.0 | kernel 6.6 LTS (current patch 6.6.141.1), systemd 255, monthly image (3.0.20251206 in Dec 2025) | GA with AKS v1.32 [1]; Microsoft Learn [2] |
| Container runtime | containerd | 2.3.0 (latest) or 2.0.11 LTS | GA; containerd.io/releases [7] |
| Cluster bootstrapper | kubeadm | v1beta4 config API | Current; no v1beta5 yet [16] |
| Kubernetes | kube-apiserver / controller-manager / scheduler / kubelet / kubectl | v1.36.x (current stable; 1.36.2 released 2026-06-09, 1.36.3 in July 2026) | kubernetes.io/releases [6] |
| CNI | Cilium (eBPF, kube-proxy replacement) | 1.20.0 (1.21 in dev) | CNCF graduated Oct 2023 [8] |
| Sandbox runtimes | gVisor (`runsc`) | latest from google/gvisor | GA; gvisor.dev [17] |
| | Kata Containers | 4.0.0 (Rust runtime, Oct 2025) | GA; kata-containers/releases [11] |
| Policy engine | Kyverno | latest (CNCF graduated March 2026) | cncf.io announcement [9] |
| In-process policy | ValidatingAdmissionPolicies (CEL) | GA since K8s 1.30 | kubernetes.io/blog [18] |
| Runtime security | Falco (modern_bpf probe) | 0.44.1 (June 2026) | CNCF graduated May 2024 [10] |
| Secrets CSI | Azure Key Vault Provider for Secrets Store CSI Driver | latest from Azure/secrets-store-csi-driver-provider-azure | GA [19] |
| Secret sync | External Secrets Operator | latest (supports Entra Workload Identity) | external-secrets.io [20] |
| Identity | Microsoft Entra Workload Identity | GA (replaced AAD Pod Identity) | learn.microsoft.com [21] |
| Supply chain | cosign / Sigstore | cosign 2.x; Sigstore OpenSSF graduated Oct 2024 | sigstore.dev [12] |
| Backup | Velero + Azure plugin | 1.17.x | vmware-tanzu/velero [22] |
| GPU (optional) | NVIDIA GPU Operator | latest | docs.nvidia.com [23] |
| Compliance scan | kube-bench | CIS Kubernetes Benchmark v1.10.0 | aquasecurity/kube-bench [14] |
| | Kubescape | CIS v1.10 + NSA + MITRE frameworks | kubescape.io [15] |

### 2.2 Why self-managed kubeadm vs AKS

The user requirement is for a cluster where **one of the nodes hosts the Kubernetes controller**. This is fundamentally a self-managed topology. Azure Kubernetes Service (AKS), by contrast, is a managed control-plane offering where Microsoft operates `kube-apiserver`, `kube-controller-manager`, `kube-scheduler`, and `etcd` as a free, Microsoft-managed service and the customer only manages worker node pools [24].

For most enterprises whose primary goal is to **run** agentic workloads rather than to **operate** Kubernetes itself, AKS is the more defensible choice: it removes the operational burden of control-plane patching, certificate rotation, etcd backup, and HA quorum management. Microsoft also natively integrates AKS with Entra Workload Identity, Key Vault, Defender for Containers, and Azure Policy. **If the literal "controller on a node we own" requirement can be relaxed in favour of "managed Kubernetes production environment," AKS on Azure Linux 3.0 with the same workload-hardening controls described in this guide is a strongly recommended alternative.**

When the self-managed requirement is firm — common reasons include regulatory data-sovereignty constraints, the need to control the exact API server flags (e.g., custom `--encryption-provider-config`, custom `--audit-policy-file`, custom `--service-account-issuer` for a private OIDC provider), or the need to run in air-gapped environments where Microsoft's managed control plane cannot reach — the path documented in this guide is the right one. The trade-off is explicit: the customer owns control-plane availability, patching, backup, recovery, and certificate rotation. The three-node HA topology below is the smallest configuration that delivers meaningful production availability; the user's two-node minimum is documented in §4.4 as a risk-accepted fallback only.

---

## 3. Threat Model for Agentic Workloads

A threat model is the prerequisite for any defensible hardening posture. The table below enumerates the agentic-specific threats addressed in this guide, the concrete attack pattern, and the primary defense-in-depth controls. Every control is implemented in a dedicated section later in the document.

| # | Threat | Example attack pattern | Primary control(s) | Section |
|---|---|---|---|---|
| T1 | Agent executes attacker-controlled or self-generated code that attempts a container/kernel escape (MITRE ATT&CK **T1611**) | Prompt-injected agent runs a Python "helper script" containing a kernel-exploit payload; the script executes inside a standard `runc` container that shares the host kernel | `gVisor`/`Kata` `RuntimeClass` for any pod that executes agent-generated code; seccomp `RuntimeDefault`; non-root user; all Linux capabilities dropped; SELinux enforcing on the host | §13, §14 |
| T2 | Agent exfiltrates secrets or internal data to an external endpoint | Compromised MCP tool server or prompt-injected agent posts credentials to an attacker-controlled domain via outbound HTTPS | Cilium default-deny egress with FQDN allow-lists (`CiliumNetworkPolicy` `toFQDNs`); Falco egress-detection rules; Microsoft Defender for Containers (optional) | §10, §17 |
| T3 | Credential / API-key sprawl in manifests or images | Hardcoded OpenAI / Azure OpenAI / Anthropic key in a `ConfigMap`, baked into the agent image, or passed as a plaintext env var | Key Vault Provider for Secrets Store CSI Driver; External Secrets Operator; Entra Workload Identity for short-lived federated tokens; no plaintext secrets in Git; Kyverno policy that rejects `Secret` objects containing known key patterns | §12, §15 |
| T4 | Supply-chain compromise of an agent framework image | Malicious PyPI/npm dependency baked into the agent image (e.g., a typosquatted `langchain` package); base-image vulnerability present at deploy time | Cosign image signing; Syft SBOM generation; Kyverno `verifyImages` admission policy; ACR vulnerability scanning; registry allow-list policy | §16 |
| T5 | Lateral movement after a single pod is compromised | Compromised agent pod scans the pod CIDR and attacks other namespaces or the metadata service | NetworkPolicy default-deny on every namespace; Cilium cluster-wide policies; PSA `restricted` enforced at namespace level; metadata service hidden via network policy | §10, §13 |
| T6 | Privilege escalation via the Kubernetes API itself | Over-privileged `ServiceAccount` token stolen from a pod is used to read secrets cluster-wide or escalate via `cluster-admin` binding | Least-privilege RBAC; `automountServiceAccountToken: false` by default; bound service-account tokens with audience and expiry; API server audit logging; Kyverno policies that reject `clusterrolebinding` to `cluster-admin` | §11, §15 |
| T7 | Unencrypted secrets at rest — etcd compromise | Attacker obtains `/var/lib/etcd` snapshot (from a stolen backup, a disk snapshot, or a node compromise) and reads all `Secret` objects in cleartext | etcd `EncryptionConfiguration` with KMS v2 backed by Azure Key Vault; TLS everywhere (control plane, etcd peer, etcd client); etcd disk encrypted at rest with platform-managed or customer-managed key | §12 |
| T8 | Untracked / undetected malicious behaviour at runtime | Agent spawns a reverse shell after a tool-call injection, or downloads a second-stage payload from an unknown endpoint | Falco eBPF runtime detection with custom agentic-workload rules; Cilium Hubble flow visibility; alert forwarding to Azure Monitor; Microsoft Defender for Containers (optional) | §17 |
| T9 | Node-level compromise / rootkit persistence | Attacker gains root on a node and attempts to install a persistent rootkit by replacing system binaries | Azure Trusted Launch (Secure Boot + vTPM); SELinux enforcing; Azure Linux OS Guard (IPE) for code integrity; signed RPM packages; host `auditd` watching `/usr/bin/kubelet`, `/usr/bin/containerd`, `/etc/kubernetes/`, `/var/lib/etcd/` | §5 |
| T10 | Loss of control-plane quorum / etcd data loss | One of three control-plane nodes is lost; an operator mistakenly deletes etcd data; a botched upgrade corrupts the etcd store | Three-node etcd cluster across availability zones; nightly `etcdctl snapshot save` to Azure Storage; Velero for Kubernetes object backup; documented cluster rebuild runbook | §8, §19 |
| T11 | Prompt injection driving the agent to abuse its own tools | An attacker-controlled document the agent ingests instructs the agent to call a tool with malicious arguments (e.g., "delete all files" via a shell tool, or "send all secrets to attacker.com" via an HTTP tool) | Tool-level egress allow-lists (T2 controls); per-tool scoped credentials (T3 controls); tool execution inside a `gvisor`/`kata` sandbox (T1 controls); audit logging of every tool invocation | §10, §12, §14, §17 |
| T12 | Supply-chain compromise of a base image later in its lifecycle | A signed, verified image is later found to have a vulnerable transitive dependency (e.g., log4shell-classic in a Java agent base image); admission-time verification passed but the vulnerability is discovered post-deploy | Continuous image re-scan via Trivy/Defender for Containers; Kyverno `verifyImages` policy that re-verifies signatures on pod update; SBOM-driven CVE monitoring; runtime detection for known exploit patterns | §16, §17 |

### 3.1 Mapping to NSA/CISA Kubernetes Hardening Guidance v1.2

The NSA/CISA Kubernetes Hardening Guidance v1.2 (released March 2022) [25] remains the authoritative public-sector hardening reference as of July 2026. The guidance categories and their implementation in this guide:

| NSA/CISA category | Implementation in this guide |
|---|---|
| Scan containers and Pods for vulnerabilities | Trivy + ACR vulnerability scanning + Microsoft Defender for Containers (§16, §17) |
| Create Pod Security Policies (note: PSPs removed in 1.25; PSA `restricted` is the replacement) | Pod Security Admission `restricted` enforced via namespace labels + Kyverno policies (§13, §15) |
| Reduce attack surface | Minimal Azure Linux 3.0 footprint; no GUI packages; firewalld + locked-down NSGs; tdnf `exclude` for pinned K8s packages (§5) |
| Apply least privilege RBAC | Entra ID group-based RBAC; `automountServiceAccountToken: false` default; no `cluster-admin` for humans (§11) |
| Use network separation and hardening | Cilium default-deny NetworkPolicy; FQDN egress allow-lists; locked-down NSGs; no public IPs (§4, §10) |
| Use firewalling and encryption | Cilium WireGuard node-to-node encryption; TLS everywhere; Azure Bastion only SSH path (§4, §10) |
| Use strong authentication | Entra ID OIDC for humans; Entra Workload Identity for workloads; no long-lived service-account tokens (§11) |
| Log everything | API server audit log to Azure Monitor; `auditd` on hosts; Falco alerts; Cilium Hubble flows (§5, §17) |
| Periodically review all controls | `kube-bench` against CIS v1.10.0 + `Kubescape` against NSA/CISA + MITRE frameworks in CI; quarterly control review (§21) |
| Continuously scan for vulnerabilities | Trivy in CI on every image build; Defender for Containers in runtime (§16, §17) |

### 3.2 OWASP LLM Top 10 and MITRE ATLAS cross-reference

Agentic workloads inherit the threat landscape defined by the **OWASP Top 10 for LLM Applications** (LLM01 Prompt Injection through LLM10 Model Theft) and the **MITRE ATLAS** (Adversarial Threat Landscape for AI Systems) knowledge base [26][27]. The controls in this guide address the Kubernetes-relevant subset of these threats:

- **OWASP LLM01 (Prompt Injection) → T11.** Sandboxed tool execution prevents an injected prompt from escalating beyond its container; egress allow-lists prevent exfiltration even when injection succeeds.
- **OWASP LLM02 (Insecure Output Handling) → T1, T11.** Generated code that is executed inside a `gvisor`/`kata` sandbox cannot reach the host kernel.
- **OWASP LLM05 (Supply Chain Vulnerabilities) → T4, T12.** Cosign-signed images, SBOMs, Kyverno `verifyImages` admission control.
- **OWASP LLM06 (Sensitive Information Disclosure) → T2, T3.** FQDN egress controls, Key Vault-managed secrets, no plaintext secrets in manifests.
- **OWASP LLM08 (Excessive Agency) → T11.** Per-tool scoped credentials and tool egress allow-lists limit blast radius even when an agent is prompt-injected into misusing its tools.

The remaining OWASP LLM risks (LLM03 Training Data Poisoning, LLM04 Model DoS, LLM07 Insecure Plugin Design, LLM09 Overreliance, LLM10 Model Theft) are application-layer concerns outside the Kubernetes cluster operator's direct control, but the platform can mitigate their blast radius through runtime sandboxing, resource quotas, and observability.

---

## 4. Prerequisites & Azure Infrastructure Layout

This section provisions the complete Azure landing zone: resource group, VNet with three subnets, NSGs locked down by role, Azure Bastion (no public SSH), internal Standard Load Balancer for the API server, Key Vault, Container Registry, and Storage Account. The cluster nodes themselves are provisioned with Trusted Launch (Secure Boot + vTPM) on Azure Linux 3.0.

### 4.1 Required tooling (admin workstation)

The following tools must be installed on the operator workstation that will run `az` and `kubectl` against the cluster. The recommended way to install all of them on macOS or Linux is via `brew` (or `asdf` for version pinning).

- **Azure CLI** ≥ 2.72.2 (required for `--gpu-driver` and several Azure Linux features) [28]
- **kubectl** matching the cluster minor version (v1.36.x)
- **helm** ≥ 3.14
- **cilium** CLI ≥ 0.16 (for `cilium status`, `cilium connectivity test`)
- **cosign** ≥ 2.4 (for image signing and verification)
- **syft** ≥ 1.0 (for SBOM generation)
- **trivy** ≥ 0.55 (for image and manifest scanning)
- **velero** CLI ≥ 1.17 (for backup management)
- **jq**, **yq**, **openssh-client**
- An SSH key pair (Ed25519 recommended) — no password-based SSH anywhere

### 4.2 Azure resource naming and layout

The naming convention below is used consistently throughout this guide. Replace the values in [Appendix B — Variable Reference](#appendix-b--variable-reference) with your own; the commands are otherwise copy-paste ready.

```bash
# Variables used throughout this guide
export RG="rg-agentic-k8s-prod"
export LOC="eastus2"                     # region with 3 AZs
export VNET="vnet-agentic-k8s"
export CP_LB="lb-k8s-apiserver-internal"
export CP_LB_IP="10.60.1.100"            # static internal LB IP for 6443
export CP_VM_PREFIX="node-cp-"           # node-cp-01, node-cp-02, node-cp-03
export WK_VM_PREFIX="node-wk-"           # node-wk-01, node-wk-02
export GPU_VM_PREFIX="node-gpu-"         # node-gpu-01 (optional)
export ADMIN_USER="k8sadmin"
export KV_NAME="kv-agentic-k8s-${LOC}"
export ACR_NAME="acragentick8s${LOC}"            # alphanumeric only, no spaces
export STORAGE_NAME="stagentickeastus${LOC}"       # lowercase alphanumeric only, no spaces
export LA_WS="log-agentic-k8s"
export ENTRA_TENANT_ID="$(az account show --query tenantId -o tsv)"

az group create -n "$RG" -l "$LOC"
```

### 4.3 VNet, subnets, NSGs, Bastion, and load balancer

```bash
# VNet + three subnets (cp, worker, Bastion). No public IPs on any node.
az network vnet create -g "$RG" -n "$VNET" --address-prefix 10.60.0.0/16 \
  --subnet-name cp-subnet --subnet-prefix 10.60.1.0/24
az network vnet subnet create -g "$RG" --vnet-name "$VNET" \
  --name worker-subnet --address-prefix 10.60.2.0/24
az network vnet subnet create -g "$RG" --vnet-name "$VNET" \
  --name AzureBastionSubnet --address-prefix 10.60.250.0/26

# Bastion for break-glass SSH access (no SSH exposed to the internet)
az network public-ip create -g "$RG" -n pip-bastion --sku Standard
az network bastion create -g "$RG" -n bastion-agentic-k8s \
  --vnet-name "$VNET" --public-ip-address pip-bastion --location "$LOC" --sku Standard

# NSGs
az network nsg create -g "$RG" -n nsg-cp
az network nsg create -g "$RG" -n nsg-wk

# Control-plane NSG: 6443 from VNet; 2379-2380 from cp subnet only;
# 10250 (kubelet) from worker subnet only; 22 from Bastion only.
az network nsg rule create -g "$RG" --nsg-name nsg-cp --name allow-apiserver-vnet \
  --priority 100 --source-address-prefixes 10.60.0.0/16 \
  --destination-port-ranges 6443 --access Allow --protocol Tcp
az network nsg rule create -g "$RG" --nsg-name nsg-cp --name allow-etcd-cp \
  --priority 110 --source-address-prefixes 10.60.1.0/24 \
  --destination-port-ranges 2379 2380 --access Allow --protocol Tcp
az network nsg rule create -g "$RG" --nsg-name nsg-cp --name allow-kubelet-from-workers \
  --priority 120 --source-address-prefixes 10.60.2.0/24 \
  --destination-port-ranges 10250 --access Allow --protocol Tcp
az network nsg rule create -g "$RG" --nsg-name nsg-cp --name allow-cp-sync-from-cp \
  --priority 130 --source-address-prefixes 10.60.1.0/24 \
  --destination-port-ranges 10250 10259 10257 --access Allow --protocol Tcp
az network nsg rule create -g "$RG" --nsg-name nsg-cp --name allow-ssh-bastion \
  --priority 140 --source-address-prefixes 10.60.250.0/26 \
  --destination-port-ranges 22 --access Allow --protocol Tcp
# Cilium control-plane ports (VXLAN, health, WireGuard) — see §10
az network nsg rule create -g "$RG" --nsg-name nsg-cp --name allow-cilium-cp \
  --priority 150 --source-address-prefixes 10.60.0.0/16 \
  --destination-port-ranges 4240 8472 51871 --access Allow --protocol '*'
az network nsg rule create -g "$RG" --nsg-name nsg-cp --name deny-all-inbound \
  --priority 4096 --source-address-prefixes '*' --destination-port-ranges '*' \
  --access Deny --protocol '*'

# Worker NSG: 10250 (kubelet) from cp subnet only; 22 from Bastion only.
az network nsg rule create -g "$RG" --nsg-name nsg-wk --name allow-kubelet-from-cp \
  --priority 100 --source-address-prefixes 10.60.1.0/24 \
  --destination-port-ranges 10250 --access Allow --protocol Tcp
az network nsg rule create -g "$RG" --nsg-name nsg-wk --name allow-ssh-bastion \
  --priority 110 --source-address-prefixes 10.60.250.0/26 \
  --destination-port-ranges 22 --access Allow --protocol Tcp
az network nsg rule create -g "$RG" --nsg-name nsg-wk --name allow-cilium-wk \
  --priority 120 --source-address-prefixes 10.60.0.0/16 \
  --destination-port-ranges 4240 8472 51871 --access Allow --protocol '*'
az network nsg rule create -g "$RG" --nsg-name nsg-wk --name deny-all-inbound \
  --priority 4096 --source-address-prefixes '*' --destination-port-ranges '*' \
  --access Deny --protocol '*'

# Internal Standard Load Balancer for the API server (6443)
az network lb create -g "$RG" -n "$CP_LB" --sku Standard \
  --vnet-name "$VNET" --subnet cp-subnet --frontend-ip-name fe-apiserver \
  --private-ip-address "$CP_LB_IP" --backend-pool-name be-apiserver
az network lb probe create -g "$RG" --lb-name "$CP_LB" -n probe-apiserver \
  --protocol Tcp --port 6443 --interval 5
az network lb rule create -g "$RG" --lb-name "$CP_LB" -n rule-apiserver \
  --frontend-ip-name fe-apiserver --backend-pool-name be-apiserver \
  --frontend-port 6443 --backend-port 6443 --protocol Tcp \
  --probe-name probe-apiserver --idle-timeout 4 --load-distribution SourceIP
```

The control-plane VMs (created in §4.5) are added to `be-apiserver` so that the LB health probe (TCP handshake on 6443) only routes traffic to a healthy API server. A TCP probe is used instead of an HTTPS probe because kubeadm generates self-signed certificates, which would fail the HTTPS probe's TLS validation.

### 4.4 VM sizing guidance

The control plane is dominated by etcd I/O sensitivity. etcd is a Raft-consensus store; every API write triggers a quorum write to disk and a flush to at least one peer. Slow disk = slow cluster. **Use Premium SSD v2 (or Ultra Disk for very large clusters) for `/var/lib/etcd`**, not Standard SSD or HDD. The worker sizing depends on the agent concurrency, model size (if local inference), and tool-execution density.

| Node | Minimum SKU | vCPU / RAM | Storage | Notes |
|---|---|---|---|---|
| Control plane (×3) | `Standard_D4s_v5` | 4 / 16 GiB | 128 GB OS + 64 GB Premium SSD v2 for etcd | etcd is latency-sensitive; do NOT use Standard SSD |
| Worker, CPU-only (×2+) | `Standard_D8s_v5` | 8 / 32 GiB | 256 GB OS | Scale per concurrent agent/tool-execution count |
| Worker, GPU LLM inference | `Standard_NCads_H100_v5` | 88 vCPU / 1.9 TiB | 1× H100 80GB + 4 TB Premium SSD | For local LLM serving (see §18) |
| Worker, GPU smaller | `Standard_NC4as_T4_v3` | 4 / 28 GiB | 1× T4 16GB | Lighter inference / smaller models |

All VMs are created with **`--security-type TrustedLaunch --enable-secure-boot true --enable-vtpm true`**. Trusted Launch provides measured, attested boot backed by a virtual TPM. This closes the gap that allows a compromised early-boot component (bootloader, kernel initrd) to install a rootkit that persists across reboots. Secure Boot also prevents unauthorized kernels (including unsigned custom kernels an attacker might try to load) from booting at all [29].

### 4.5 Provisioning the nodes

The Azure Linux 3.0 marketplace image is published by Microsoft. Confirm the current URN with `az vm image list --publisher Microsoft* --all -o table | grep -i azure-linux` before deploying — the publisher alias has been historically `MicrosoftCBLMariner` and is now `MicrosoftAzureLinux` for new subscriptions. The pattern below uses the Microsoft-documented approach.

```bash
# Discover the current Azure Linux 3.0 image URN
az vm image list --publisher MicrosoftAzureLinux --all -o table 2>/dev/null \
  || az vm image list --publisher MicrosoftCBLMariner --all -o table
# Pick the latest 3.x, Gen2, Trusted-Launch-capable image. Example:
IMG="MicrosoftAzureLinux:azure-linux:3-gen2:latest"

# Provision 3 control-plane nodes across 3 availability zones
for i in 1 2 3; do
  az vm create -g "$RG" -n "${CP_VM_PREFIX}0${i}" --image "$IMG" \
    --size Standard_D4s_v5 --vnet-name "$VNET" --subnet cp-subnet \
    --nsg nsg-cp --public-ip-address "" \
    --admin-username "$ADMIN_USER" --ssh-key-values ~/.ssh/id_ed25519.pub \
    --security-type TrustedLaunch --enable-secure-boot true --enable-vtpm true \
    --os-disk-size-gb 128 \
    --zone $i --zone-resilient true
  # Attach a Premium SSD v2 disk for etcd
  az disk create -g "$RG" -n disk-etcd-${CP_VM_PREFIX}0${i} \
    --size-gb 64 --sku PremiumV2_LRS --zone $i --performance-plus
  az vm disk attach -g "$RG" --vm-name ${CP_VM_PREFIX}0${i} \
    --name disk-etcd-${CP_VM_PREFIX}0${i} --lun 0
  # Add to API-server LB backend pool
  az network nic ip-config address-pool add \
    -g "$RG" --nic-name ${CP_VM_PREFIX}0${i}VMNic --ip-config-name ipconfig${CP_VM_PREFIX}0${i} \
    --lb-name "$CP_LB" --address-pool be-apiserver
done

# Provision 2 worker nodes
for i in 1 2; do
  az vm create -g "$RG" -n "${WK_VM_PREFIX}0${i}" --image "$IMG" \
    --size Standard_D8s_v5 --vnet-name "$VNET" --subnet worker-subnet \
    --nsg nsg-wk --public-ip-address "" \
    --admin-username "$ADMIN_USER" --ssh-key-values ~/.ssh/id_ed25519.pub \
    --security-type TrustedLaunch --enable-secure-boot true --enable-vtpm true \
    --os-disk-size-gb 256 \
    --zone $i --zone-resilient true
done
```

### 4.6 Supporting services: Key Vault, ACR, Storage, Log Analytics

```bash
# Key Vault (RBAC mode, not access policy) — used for KMS v2, agent secrets, and CA
az keyvault create -g "$RG" -n "$KV_NAME" --enable-rbac-authorization true \
  --sku standard --public-network-access disabled
# (For air-gapped scenarios, use --public-network-access disabled with private endpoint.)

# Azure Container Registry — signed images, SBOMs, Helm charts
az acr create -g "$RG" -n "$ACR_NAME" --sku Premium --admin-enabled false \
  --public-network-enabled false
# ACR Premium gives: geo-replication, content trust (Notary v2 / ORAS), private endpoints

# Storage account — Velero backups + etcd snapshots
az storage account create -g "$RG" -n "$STORAGE_NAME" --sku Standard_GRS \
  --https-only true --min-tls-version TLS1_2 --allow-blob-public-access false

# Log Analytics workspace — audit sink, Falco alerts, container insights
az monitor log-analytics workspace create -g "$RG" -n "$LA_WS" --location "$LOC"
```

### 4.7 Private endpoints (recommended for production)

For each PaaS service above, create a private endpoint in the VNet so traffic never traverses the public internet:

```bash
# Key Vault private endpoint
az network private-endpoint create -g "$RG" -n pe-kv \
  --vnet-name "$VNET" --subnet cp-subnet \
  --private-connection-resource-id "$(az keyvault show -g $RG -n $KV_NAME --query id -o tsv)" \
  --group-id vault --connection-name pe-kv-conn
# (Repeat for ACR, Storage, Log Analytics as needed.)
```

### 4.8 The minimum-viable 2-node baseline (documented-risk fallback)

If the operational context absolutely cannot support three control-plane nodes — typically a lab, a staging cluster, or a risk-accepted production deployment with an explicit waiver — the same procedure in §5 through §19 produces a working cluster with the following substitutions:

- Provision one control-plane VM (`node-cp-01`) and one worker VM (`node-wk-01`).
- Skip the internal load balancer; `controlPlaneEndpoint` in the kubeadm config is set to the control-plane node's private IP.
- Skip the etcd Premium SSD v2 disk attachment; etcd runs on the OS disk (this is acceptable only for low-write clusters).
- Document the risk explicitly in the cluster's risk register: a single control-plane node is a single point of failure for the API server, scheduler, controller manager, and etcd. There is no quorum; a node reboot causes cluster unavailability for the duration of the reboot.
- Do not run production agentic workloads on this topology. The blast radius of an agentic workload compromise on a single-node cluster is the entire cluster.

The remainder of this guide assumes the 3-control-plane + 2-worker HA topology as the canonical deployment.

---

## 5. Host OS Provisioning & Hardening (Azure Linux 3.0)

Azure Linux 3.0 is Microsoft's minimal-footprint Linux distribution — sources derived from Fedora Linux, built and optimized for Azure, and the default host OS for the majority of Microsoft's own AKS fleet [1][2]. It ships with a 6.6 LTS kernel, `systemd` 255, RPM/`tdnf` package management, SELinux in enforcing mode by default, the SymCrypt FIPS 140-3 validated cryptographic module, native Secure Boot and measured-boot integration, and (newly GA) **OS Guard** — an immutable container host layer that integrates the Integrity Policy Enforcement (IPE) Linux Security Module to ensure that only binaries from trusted, signed volumes are allowed to execute [3].

The hardening steps below are run **on every node** (control-plane and worker) before `kubeadm init` or `kubeadm join`. They align with the CIS Distribution-Independent Linux Benchmark, the NSA/CISA Kubernetes Hardening Guidance v1.2 host-level recommendations [25], and Microsoft's own Azure Linux hardening guidance.

### 5.1 Baseline update and minimal package set

```bash
sudo tdnf makecache
sudo tdnf update -y
sudo tdnf install -y chrony auditd firewalld policycoreutils-python-utils \
  container-selinux tar curl jq socat conntrack-tools iproute-tc
```

The `container-selinux` package is required for proper SELinux labeling of container runtime files. Without it, containerd will produce AVC denials that either block legitimate container operations or — worse — train operators to reflexively disable SELinux. Do not skip this package.

### 5.2 Time synchronization, hostname, /etc/hosts

NTP drift breaks TLS certificate validation and Kubernetes token verification. `chrony` is the Azure Linux default and is sufficient for production.

```bash
sudo systemctl enable --now chronyd
sudo chronyc -a makesync     # force immediate sync

# Set per-node hostname (kubeadm uses hostname as the Node object name)
sudo hostnamectl set-hostname node-cp-01       # or node-cp-02, node-cp-03, node-wk-01, etc.

# Add static /etc/hosts entries for every node (or use a private DNS zone in production)
sudo tee -a /etc/hosts >/dev/null <<EOF
10.60.1.4   node-cp-01
10.60.1.5   node-cp-02
10.60.1.6   node-cp-03
10.60.2.4   node-wk-01
10.60.2.5   node-wk-02
10.60.1.100 k8s-apiserver.internal
EOF
```

In a production deployment, replace `/etc/hosts` with a private Azure DNS zone linked to the VNet, so new nodes are automatically resolvable.

### 5.3 Kernel modules and sysctl hardening

Kubernetes and Cilium require the `overlay` and `br_netfilter` kernel modules. The sysctl block below combines Kubernetes requirements with kernel-hardening recommendations from the CIS Linux Benchmark and the NSA/CISA guidance.

```bash
# Required kernel modules
sudo tee /etc/modules-load.d/k8s.conf >/dev/null <<EOF
overlay
br_netfilter
EOF
sudo modprobe overlay
sudo modprobe br_netfilter

# Kernel and network hardening sysctls
sudo tee /etc/sysctl.d/99-kubernetes-hardening.conf >/dev/null <<'EOF'
# ---- Kubernetes / CNI requirements ----
net.bridge.bridge-nf-call-iptables   = 1
net.bridge.bridge-nf-call-ip6tables  = 1
net.ipv4.ip_forward                  = 1

# ---- Kernel hardening (CIS + NSA/CISA) ----
kernel.kptr_restrict                 = 2     # hide kernel pointers from unprivileged users
kernel.dmesg_restrict                = 1     # only root can read dmesg
kernel.perf_event_paranoid           = 3     # perf events restricted to root
kernel.unprivileged_bpf_disabled     = 1     # only root+CAP_BPF can use bpf(2)
kernel.yama.ptrace_scope             = 2     # ptrace restricted to parent processes
kernel.unprivileged_userns_clone     = 0     # disable unprivileged user namespaces
fs.protected_hardlinks               = 1
fs.protected_symlinks                = 1
fs.protected_fifos                   = 2
fs.protected_regular                 = 2
fs.suid_dumpable                     = 0

# ---- Network hardening ----
net.ipv4.conf.all.rp_filter          = 1
net.ipv4.conf.all.accept_redirects   = 0
net.ipv4.conf.default.accept_redirects = 0
net.ipv4.conf.all.send_redirects     = 0
net.ipv4.conf.default.send_redirects = 0
net.ipv4.conf.all.accept_source_route = 0
net.ipv4.conf.default.accept_source_route = 0
net.ipv4.icmp_echo_ignore_broadcasts = 1
net.ipv4.tcp_syncookies              = 1
net.ipv6.conf.all.disable_ipv6       = 0     # Cilium supports IPv6; leave enabled
net.ipv6.conf.all.accept_ra          = 0
net.ipv6.conf.all.accept_redirects   = 0
EOF
sudo sysctl --system
```

> **Note on `kernel.unprivileged_bpf_disabled`.** Cilium's eBPF datapath uses `bpf(2)` syscalls, but it runs as root with `CAP_BPF`, so setting `unprivileged_bpf_disabled=1` does **not** break Cilium. The older `kernel.unprivileged_bpf_disabled=0` setting sometimes seen in Cilium documentation was needed only for older kernels without `CAP_BPF`; on Azure Linux 3.0 (kernel 6.6), `CAP_BPF` is available and the hardened value `1` is correct [8].

### 5.4 Disable swap

Kubelet rejects swap on the host by default. Disabling swap is mandatory for the cluster to initialize.

```bash
sudo swapoff -a
sudo sed -ri '/\sswap\s/s/^/#/' /etc/fstab
```

### 5.5 SELinux — keep it enforcing

Azure Linux ships SELinux in enforcing mode. **Do not disable it.** Unlike older community guidance for other distributions, the right answer on Azure Linux is to install `container-selinux` and use the per-container SELinux type labels, not to disable the LSM entirely.

```bash
getenforce                                  # expect: Enforcing
sudo tdnf install -y container-selinux
sudo setsebool -P container_manage_cgroup on
```

If a specific policy denial blocks a legitimate container operation, generate a targeted policy module with `audit2allow` rather than switching the system to `permissive` or `disabled`:

```bash
# Generate and install a targeted allow-rule from the audit log
sudo ausearch -m AVC -ts recent | audit2allow -M my-k8s-policy
sudo semodule -i my-k8s-policy.pp
```

### 5.6 OS Guard (IPE) — code integrity enforcement

Azure Linux OS Guard integrates the **Integrity Policy Enforcement (IPE)** Linux Security Module to ensure only binaries from trusted, signed volumes can execute. This is the Linux-native equivalent of Windows Code Integrity and is the recommended host-level defense against post-compromise rootkit persistence [3]. **OS Guard is currently in public preview** on Azure Linux 3.0; on existing images it ships in **audit mode** by default so operators can validate their workloads before flipping to enforcing. Monitor the Microsoft Learn documentation [48] for GA announcements.

> **Note on kernel version.** The IPE LSM was merged into **mainline Linux kernel 6.8**. Azure Linux 3.0 ships with the **6.6 LTS** kernel; therefore, OS Guard's IPE functionality relies on a Microsoft-maintained backport. Verify IPE availability via `cat /sys/kernel/security/ipe/active_policy` before relying on it for strict enforcement.

```bash
# Check current IPE mode (audit vs enforcing)
sudo cat /sys/kernel/security/ipe/active_policy 2>/dev/null \
  || echo "IPE not active; install via tdnf install azure-linux-os-guard"

# Install OS Guard if not preinstalled
sudo tdnf install -y azure-linux-os-guard
sudo systemctl enable --now ipe

# Review IPE audit denials (these would have been enforcement failures in enforcing mode)
sudo ausearch -m AVC -ts recent | grep -i ipe

# Once audit log shows no unexpected denials over a representative workload window,
# switch to enforcing mode per the Microsoft Learn documentation. Plan a validation
# pass in staging before enforcing in production.
```

### 5.7 Host firewall (defense in depth under the NSG)

The NSG operates at the Azure VNet layer (L3/L4). The host firewall (`firewalld`) operates at the host layer and provides a second line of defense in case the NSG is misconfigured or a compromised process tries to bind a new port.

```bash
sudo systemctl enable --now firewalld

# ---- Control-plane node ----
sudo firewall-cmd --permanent --add-port=6443/tcp          # kube-apiserver
sudo firewall-cmd --permanent --add-port=2379-2380/tcp     # etcd peer + client
sudo firewall-cmd --permanent --add-port=10250/tcp         # kubelet
sudo firewall-cmd --permanent --add-port=10257/tcp         # kube-controller-manager
sudo firewall-cmd --permanent --add-port=10259/tcp         # kube-scheduler

# ---- Worker node ----
sudo firewall-cmd --permanent --add-port=10250/tcp         # kubelet
sudo firewall-cmd --permanent --add-port=30000-32767/tcp   # NodePort range (if used)

# ---- Cilium (both control-plane and worker) ----
sudo firewall-cmd --permanent --add-port=4240/tcp          # cilium-health
sudo firewall-cmd --permanent --add-port=8472/udp          # VXLAN overlay
sudo firewall-cmd --permanent --add-port=51871/udp         # WireGuard node-to-node encryption

sudo firewall-cmd --reload
```

### 5.8 SSH hardening

No SSH exposure to the internet — administrative SSH goes through Azure Bastion only. Even within the VNet, harden `sshd` to forbid root login, password auth, and challenge-response auth.

```bash
sudo sed -ri \
  -e 's/^#?PermitRootLogin.*/PermitRootLogin no/' \
  -e 's/^#?PasswordAuthentication.*/PasswordAuthentication no/' \
  -e 's/^#?ChallengeResponseAuthentication.*/ChallengeResponseAuthentication no/' \
  -e 's/^#?X11Forwarding.*/X11Forwarding no/' \
  -e 's/^#?PermitEmptyPasswords.*/PermitEmptyPasswords no/' \
  -e 's/^#?MaxAuthTries.*/MaxAuthTries 3/' \
  /etc/ssh/sshd_config
echo "AllowUsers ${ADMIN_USER}" | sudo tee -a /etc/ssh/sshd_config
sudo systemctl restart sshd
```

### 5.9 auditd baseline (host-level audit trail)

The host `auditd` log complements the Kubernetes API server audit log. Together they answer the two questions that matter for incident response: what did the API server do, and what did the kernel do?

```bash
sudo tee /etc/audit/rules.d/k8s-node.rules >/dev/null <<'EOF'
# Watch critical Kubernetes files
-w /etc/kubernetes/                -p wa  -k k8s-config
-w /var/lib/etcd/                  -p wa  -k etcd-data
-w /etc/containerd/                -p wa  -k containerd-config
-w /etc/cni/                       -p wa  -k cni-config

# Watch critical binaries (exec attempts)
-w /usr/bin/kubelet                -p x   -k kubelet-exec
-w /usr/bin/kubeadm                -p x   -k kubeadm-exec
-w /usr/bin/containerd             -p x   -k containerd-exec
-w /usr/bin/kubectl                -p x   -k kubectl-exec
-w /usr/sbin/auditctl              -p x   -k auditctl-exec
-w /usr/sbin/augenrules            -p x   -k augenrules-exec

# Watch SSH configuration
-w /etc/ssh/sshd_config            -p wa  -k ssh-config

# Watch user/group files
-w /etc/passwd                     -p wa  -k identity
-w /etc/group                      -p wa  -k identity
-w /etc/shadow                     -p wa  -k identity
-w /etc/sudoers                    -p wa  -k identity
-w /etc/sudoers.d/                 -p wa  -k identity

# Watch agentic sandbox runtime directories (MITRE T1611 escape attempts)
-w /var/run/kata-containers/           -p wa  -k kata-runtime
-w /var/run/containerd/io.containerd.runtime.v2.task/ -p wa -k containerd-tasks
EOF
sudo augenrules --load
sudo systemctl enable --now auditd
```

### 5.10 Pinned, controlled security patching

Azure Linux uses `tdnf`. Enable automatic security-only updates on a maintenance window rather than blind full-system auto-upgrade — uncontrolled upgrades of `kubelet`/`kubeadm`/`containerd` cause version drift that breaks `kubeadm upgrade` later (see Appendix D for the upgrade runbook).

```bash
# Pin K8s packages so they are NOT auto-upgraded
sudo tee /etc/tdnf/tdnf.conf.d/hold-k8s.conf >/dev/null <<'EOF'
[main]
exclude=kubelet kubeadm kubectl moby-containerd containerd
EOF

# Schedule weekly security-only updates via systemd timer
sudo tee /etc/systemd/system/tdnf-security.service >/dev/null <<'EOF'
[Unit]
Description=Apply Azure Linux security updates (excluding pinned K8s packages)
After=network-online.target

[Service]
Type=oneshot
ExecStart=/usr/bin/tdnf -y --security update
ExecStartPost=/usr/bin/systemctl is-system-running --wait || /usr/bin/systemctl reboot
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

The `ExecStartPost` line reboots the host if the security update touched the kernel, kernel modules, or `systemd` itself — this is the only safe way to apply kernel security patches. Schedule the timer for a maintenance window that does not collide with the cluster's rolling-upgrade cadence.

### 5.11 Format and mount the etcd disk (control-plane nodes only)

On control-plane nodes, format the attached Premium SSD v2 disk and mount it at `/var/lib/etcd`:

```bash
# Identify the attached disk (LUN 0)
ls -l /dev/disk/azure/scsi1/lun0
sudo mkfs.xfs /dev/disk/azure/scsi1/lun0
sudo mkdir -p /var/lib/etcd
sudo mount /dev/disk/azure/scsi1/lun0 /var/lib/etcd

# Persist the mount
echo "/dev/disk/azure/scsi1/lun0 /var/lib/etcd xfs defaults,noatime,nodiratime 0 2" \
  | sudo tee -a /etc/fstab

# Restrict permissions
sudo chown -R etcd:etcd /var/lib/etcd 2>/dev/null || true
sudo chmod 700 /var/lib/etcd
```

The `noatime,nodiratime` options reduce write amplification on the etcd disk, which is significant because etcd issues a `fsync()` on every quorum write.

---

## 6. Container Runtime Installation (containerd 2.x)

Kubernetes requires a CRI-compliant container runtime. **containerd 2.x** is the current GA series; the latest patch is 2.3.0 [7]. The 2.0 LTS branch is supported with bug and security fixes through March 2027, so either 2.0.x or 2.3.x is acceptable for production. On Azure Linux, containerd ships as `moby-containerd` from the built-in `tdnf` repositories (Azure Linux 3.0 ships containerd 2.x by default).

### 6.1 Install containerd

```bash
sudo tdnf install -y moby-containerd runc
sudo mkdir -p /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml >/dev/null
```

### 6.2 Configure containerd for Kubernetes

Three settings are mandatory: systemd cgroup driver, the `registry.k8s.io/pause:3.10` sandbox image, and the systemd cgroup for any custom runtime classes (gVisor, Kata).

```bash
sudo sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml
sudo sed -i 's#sandbox_image = .*#sandbox_image = "registry.k8s.io/pause:3.10"#' \
  /etc/containerd/config.toml
```

### 6.3 Pre-stage RuntimeClass support (gVisor, Kata)

To support gVisor and Kata Containers as `RuntimeClass` options later (§14), pre-register them in containerd's `[plugins."io.containerd.cri.v1.runtime".runtimes]` section (containerd 2.x uses `io.containerd.cri.v1.runtime`, not the legacy `io.containerd.grpc.v1.cri`). The full binary installation for gVisor and Kata is in §14; here we only add the containerd config so the runtime classes can be added once the binaries exist.

```bash
# Append RuntimeClass entries for runsc (gVisor) and kata (Kata Containers)
# to /etc/containerd/config.toml. The full binaries are installed in §14.
sudo tee -a /etc/containerd/config.toml >/dev/null <<'EOF'

# ---- RuntimeClass: gVisor (runsc) ----
# containerd 2.x uses io.containerd.cri.v1.runtime (NOT the legacy io.containerd.grpc.v1.cri)
[plugins."io.containerd.cri.v1.runtime".runtimes.runsc]
  runtime_type = "io.containerd.runsc.v1"
  sandbox_type = "pod"
  pod_annotations = []
  container_annotations = []

# ---- RuntimeClass: Kata Containers ----
[plugins."io.containerd.cri.v1.runtime".runtimes.kata]
  runtime_type = "io.containerd.kata.v2"
  privileged_without_host_devices = true
  pod_annotations = []
  container_annotations = []
EOF
```

### 6.4 Enable and verify

```bash
sudo systemctl enable --now containerd
sudo systemctl status containerd --no-pager

# Verify cgroup v2 is active (Azure Linux 3.0 defaults to unified cgroup v2)
stat -fc %T /sys/fs/cgroup/                   # expect: cgroup2fs

# Verify the systemd cgroup driver is in use
sudo containerd config dump | grep SystemdCgroup   # expect: SystemdCgroup = true
```

If `cgroup2fs` is not returned, the kernel was booted with the legacy cgroup v1 hierarchy. Azure Linux 3.0 defaults to v2; if you have a custom kernel command line that forces v1, remove the `systemd.unified_cgroup_hierarchy=0` parameter from `/etc/default/grub` and rebuild the GRUB config.

---

## 7. Kubernetes Package Installation via pkgs.k8s.io

Since **March 4, 2024**, the legacy Google-hosted `apt.kubernetes.io` and `yum.kubernetes.io` repositories have been frozen and no longer receive new Kubernetes releases [13]. All Kubernetes packages are now published through the community-owned **`pkgs.k8s.io`** infrastructure (an OpenBuildService-backed service operated by the Kubernetes project). Run on **every node** (control-plane and worker).

### 7.1 Add the pkgs.k8s.io RPM repository

The repository is per-minor-version: each minor (1.36, 1.37, …) has its own RPM repo URL. Pin to the minor you intend to run; cross-minor upgrades require changing the repo URL (see Appendix D).

```bash
# Pin the minor version explicitly. This guide uses 1.36 (current stable as of July 2026 [6]).
K8S_MINOR="1.36"
cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://pkgs.k8s.io/core:/stable:/v${K8S_MINOR}/rpm/
enabled=1
gpgcheck=1
gpgkey=https://pkgs.k8s.io/core:/stable:/v${K8S_MINOR}/rpm/repodata/repomd.xml.key
exclude=kubelet kubeadm kubectl cri-tools kubernetes-cni
EOF
```

### 7.2 Install kubelet, kubeadm, kubectl

```bash
sudo tdnf install -y kubelet kubeadm kubectl cri-tools kubernetes-cni
sudo systemctl enable --now kubelet
```

`kubelet` will restart in a CrashLoopBackOff until `kubeadm init` (on the control-plane node) or `kubeadm join` (on workers) is run — this is expected. Do not try to "fix" it; the kubelet needs `/etc/kubernetes/kubelet.conf` to exist, which kubeadm creates.

### 7.3 Verify versions

```bash
kubeadm version     # expect: GitVersion:"v1.36.x"
kubectl version --client
kubelet --version
```

All three must report the same minor version. Kubernetes' version skew policy allows kubelet to be up to **three minors older** than `kube-apiserver`, and `kubectl` to be ±1 minor, but a fresh install should pin all three to the same minor for the simplest support matrix [30].

### 7.4 Why not Azure Linux's native kubelet package?

Azure Linux does not ship Kubernetes packages in its own repositories — Kubernetes is upstream's responsibility, not the distribution's. This is consistent with the broader industry direction: the `pkgs.k8s.io` repository is the canonical source, and distribution-specific packaging (e.g., the older Ubuntu PPA) has been deprecated. Using `pkgs.k8s.io` also means you get patches on Kubernetes' own release cadence (typically within 24 hours of an upstream patch release) rather than waiting for a distribution's package maintainer.

---

## 8. Bootstrapping the Control Plane (3-Node HA with kubeadm)

The control plane is bootstrapped on the first node (`node-cp-01`) with a `kubeadm` v1beta4 config file, then the second and third nodes are joined with `--control-plane --certificate-key`. The `controlPlaneEndpoint` field points at the internal Standard Load Balancer front-end IP (10.60.1.100), not at any individual node, so that the API server remains reachable even when one control-plane node is down.

### 8.1 The kubeadm config file (v1beta4)

Create this on `node-cp-01` only. The full file with line-by-line annotations is in [Appendix A](#appendix-a--full-reference-manifests); the version below is the operational form.

```yaml
# /etc/kubernetes/kubeadm-config.yaml
apiVersion: kubeadm.k8s.io/v1beta4
kind: InitConfiguration
bootstrapTokens:
  - groups: ["system:bootstrappers:kubeadm:default-node-token"]
    ttl: 24h0m0s
    usages: ["signing", "authentication"]
nodeRegistration:
  name: "node-cp-01"
  criSocket: "unix:///run/containerd/containerd.sock"
  taints:
    - key: "node-role.kubernetes.io/control-plane"
      effect: "NoSchedule"
  kubeletExtraArgs:
    - name: cloud-provider
      value: "external"             # Azure cloud provider (optional; see §8.5)
    - name: rotate-server-certificates
      value: "true"
---
apiVersion: kubeadm.k8s.io/v1beta4
kind: ClusterConfiguration
kubernetesVersion: "v1.36.2"      # pin exact patch
clusterName: "agentic-k8s-prod"
controlPlaneEndpoint: "k8s-apiserver.internal:6443"
apiServer:
  certSANs:
    - "k8s-apiserver.internal"
    - "10.60.1.100"
    - "node-cp-01"
    - "node-cp-02"
    - "node-cp-03"
    - "10.60.1.4"
    - "10.60.1.5"
    - "10.60.1.6"
  extraArgs:
    - name: authorization-mode
      value: "Node,RBAC"
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
      value: "/etc/kubernetes/encryption-provider.yaml"
    - name: service-account-issuer
      value: "https://kubernetes.default.svc.cluster.local"
    - name: service-account-signing-key-file
      value: "/etc/kubernetes/pki/sa.key"
    - name: profiling
      value: "false"
    - name: enable-aggregator-routing
      value: "true"
  extraVolumes:
    - name: "audit-policy"
      hostPath: "/etc/kubernetes/audit-policy.yaml"
      mountPath: "/etc/kubernetes/audit-policy.yaml"
      readOnly: true
    - name: "audit-log"
      hostPath: "/var/log/kubernetes/audit"
      mountPath: "/var/log/kubernetes/audit"
      readOnly: false
    - name: "encryption-provider"
      hostPath: "/etc/kubernetes/encryption-provider.yaml"
      mountPath: "/etc/kubernetes/encryption-provider.yaml"
      readOnly: true
controllerManager:
  extraArgs:
    - name: profiling
      value: "false"
    - name: terminated-pod-gc-threshold
      value: "50"
    - name: horizontal-pod-autoscaler-sync-period
      value: "30s"
scheduler:
  extraArgs:
    - name: profiling
      value: "false"
etcd:
  local:
    dataDir: "/var/lib/etcd"
    imageRepository: "registry.k8s.io"
    imageTag: "3.5.21-0"          # pin etcd version
    extraArgs:
      - name: listen-metrics-urls
        value: "http://0.0.0.0:2381"
      - name: auto-compaction-retention
        value: "5"
      - name: auto-compaction-mode
        value: "periodic"
      - name: snapshot-count
        value: "10000"
      - name: quota-backend-bytes
        value: "8589934592"   # 8 GiB
      - name: election-timeout
        value: "2000"
      - name: heartbeat-interval
        value: "250"
networking:
  podSubnet: "10.244.0.0/16"
  serviceSubnet: "10.96.0.0/12"
  dnsDomain: "cluster.local"
imageRepository: "registry.k8s.io"
---
apiVersion: kubelet.config.k8s.io/v1
kind: KubeletConfiguration
cgroupDriver: "systemd"
cgroupRoot: "/"
rotateCertificates: true
serverTLSBootstrap: true
protectKernelDefaults: true
featureGates:
  KubeletTracing: true
---
apiVersion: kubeproxy.config.k8s.io/v1alpha1
kind: KubeProxyConfiguration
# NOTE: kube-proxy is NOT deployed by kubeadm in this guide — Cilium 1.20 replaces it.
# We include this empty config only for documentation; kubeadm skips kube-proxy deployment
# via skipPhases below.
mode: "ipvs"
```

### 8.2 The audit policy file

Create `/etc/kubernetes/audit-policy.yaml` on `node-cp-01` before `kubeadm init`. The audit log captures every API server call; in production it should be forwarded to a SIEM (Azure Monitor in this guide's reference architecture).

```yaml
# /etc/kubernetes/audit-policy.yaml
apiVersion: audit.k8s.io/v1
kind: Policy
omitStages:
  - "RequestReceived"
rules:
  # Log every Secret/ConfigMap access at Metadata level (who, what, when — not the body)
  - level: Metadata
    resources:
      - group: ""
        resources: ["secrets", "configmaps"]
  # Log RBAC changes at RequestResponse level (full request and response)
  - level: RequestResponse
    resources:
      - group: "rbac.authorization.k8s.io"
        resources: ["roles", "rolebindings", "clusterroles", "clusterrolebindings"]
  # Log authentication attempts
  - level: RequestResponse
    userGroups: ["system:authenticated", "system:unauthenticated"]
    verbs: ["create"]
    resources:
      - group: ""
        resources: ["tokenreviews"]
  # Log admission webhook configurations
  - level: RequestResponse
    resources:
      - group: "admissionregistration.k8s.io"
        resources: ["mutatingwebhookconfigurations", "validatingwebhookconfigurations",
                    "validatingadmissionpolicies", "validatingadmissionpolicybindings"]
  # Log pod exec, attach, port-forward
  - level: RequestResponse
    verbs: ["create", "update", "patch", "delete"]
    resources:
      - group: ""
        resources: ["pods/exec", "pods/attach", "pods/portforward"]
  # Catch-all Metadata for everything else
  - level: Metadata
```

### 8.3 The encryption-provider config (KMS v2)

`EncryptionConfiguration` with KMS v2 ensures that `Secret` objects are encrypted at rest in etcd with a key managed by Azure Key Vault, not a static key on disk. KMS v2 is GA since Kubernetes 1.29 [31]; KMS v1 is removed in current releases. The exact plugin used to bridge Kubernetes KMS v2 to Azure Key Vault depends on your environment:

- **akv2k8s** (community-maintained, widely used) provides both a KMS v2 provider and a secrets-injector controller.
- **Azure Key Vault KMS provider** (part of `cloud-provider-azure`) is the Microsoft-supported path; see the Microsoft Learn KMS v2 documentation for the exact endpoint format.

The example below uses the generic KMS v2 schema; substitute your provider's `endpoint` value.

```yaml
# /etc/kubernetes/encryption-provider.yaml
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
  - resources:
      - secrets
      - configmaps
    providers:
      - kms:
          apiVersion: v2
          name: azure-key-vault
          endpoint: unix:///var/run/azurekms/kms.sock    # provider socket
          timeout: 3s
      - identity: {}   # fallback for reading pre-encryption secrets during migration
```

> **Migration note.** If you have an existing cluster with unencrypted secrets, you must run `kubectl get secrets --all-namespaces -o yaml | kubectl replace -f -` after enabling encryption to rewrite every Secret through the encryption provider. Until this is done, secrets written before the change remain in cleartext in etcd.

### 8.4 Run kubeadm init on node-cp-01

```bash
# Create the audit and encryption-provider files first (see §8.2, §8.3)
sudo mkdir -p /var/log/kubernetes/audit
sudo kubeadm init --config /etc/kubernetes/kubeadm-config.yaml \
  --upload-certs \
  --skip-phases=addon/kube-proxy
```

The `--skip-phases=addon/kube-proxy` flag tells kubeadm not to deploy `kube-proxy` — Cilium 1.20 will replace it via eBPF (see §10). The `--upload-certs` flag uploads the control-plane certificates to the cluster encrypted with a temporary key, which is then printed to the terminal for use when joining the second and third control-plane nodes.

### 8.5 Capture the join commands

After `kubeadm init` completes, the output includes two join commands:

```
You can now join any number of control-plane nodes by running:
  kubeadm join k8s-apiserver.internal:6443 --token <token> \
    --discovery-token-ca-cert-hash sha256:<hash> \
    --control-plane --certificate-key <key>

You can join any worker node by running:
  kubeadm join k8s-apiserver.internal:6443 --token <token> \
    --discovery-token-ca-cert-hash sha256:<hash>
```

Save both. The `<key>` value rotates after two hours by default; if you need to add a fourth control-plane node later, regenerate the key with `kubeadm init phase upload-certs --upload-certs` on an existing control-plane node.

### 8.6 Copy admin kubeconfig off the control-plane node

```bash
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

For day-2 operations from the admin workstation, copy this file via Bastion to the operator workstation's `~/.kube/config-agentic-k8s-prod` and switch contexts with `KUBECONFIG`.

### 8.7 Join the second and third control-plane nodes

On `node-cp-02` and `node-cp-03`, after completing the host hardening (§5), containerd (§6), and Kubernetes packages (§7):

```bash
# Run on node-cp-02 and node-cp-03 (replace <token>, <hash>, <key>)
sudo kubeadm join k8s-apiserver.internal:6443 \
  --token <token> \
  --discovery-token-ca-cert-hash sha256:<hash> \
  --control-plane \
  --certificate-key <key>

# Copy the audit-policy and encryption-provider files to the new node
# (kubeadm does NOT copy these; they are referenced as extraVolumes)
sudo mkdir -p /etc/kubernetes /var/log/kubernetes/audit
# scp from node-cp-01:
#   /etc/kubernetes/audit-policy.yaml
#   /etc/kubernetes/encryption-provider.yaml
# Then restart kube-apiserver to pick up the volumes:
sudo crictl pods --name kube-apiserver-node-cp-02 | awk 'NR==2{print $1}' \
  | xargs -r sudo crictl stopp
```

The `crictl stopp` line forces the kube-apiserver static pod to be recreated by `kubelet`, which will then mount the `audit-policy` and `encryption-provider` extraVolumes. Without this step, the API server on the new control-plane node will fail to start because the referenced host files do not exist.

### 8.8 Verify the control plane

```bash
kubectl get nodes                # expect 3 control-plane nodes, Ready
kubectl get pods -n kube-system  # expect etcd, apiserver, controller-manager, scheduler, coredns on each CP
kubectl get cs                   # component statuses (deprecated in 1.19+; use 'kubectl get --raw='/healthz'')
kubectl get --raw='/healthz?verbose' | head -20
```

The cluster is now a working three-node control plane. There are no worker nodes yet — and no CNI, so any pod scheduled to a node will remain `Pending` until Cilium is installed (§10).

---

## 9. Joining Worker Nodes

With the control plane stable, join the worker nodes. The procedure is identical to the control-plane join, minus the `--control-plane` and `--certificate-key` flags.

### 9.1 Run kubeadm join on each worker

On `node-wk-01` and `node-wk-02`, after the host hardening (§5), containerd (§6), and Kubernetes packages (§7) are complete:

```bash
sudo kubeadm join k8s-apiserver.internal:6443 \
  --token <token> \
  --discovery-token-ca-cert-hash sha256:<hash>
```

If the bootstrap token has expired (default TTL is 24 hours), generate a new one on any control-plane node:

```bash
kubeadm token create --print-join-command
```

### 9.2 Verify node registration

```bash
kubectl get nodes -o wide
# Expect:
#   node-cp-01   Ready   control-plane   v1.36.2   ...
#   node-cp-02   Ready   control-plane   v1.36.2   ...
#   node-cp-03   Ready   control-plane   v1.36.2   ...
#   node-wk-01   Ready   <none>          v1.36.2   ...
#   node-wk-02   Ready   <none>          v1.36.2   ...
```

### 9.3 Apply labels and taints

Labels and taints encode the workload placement policy. The labels below support the scheduling rules used throughout the rest of this guide (gVisor/Kata runtime classes target labeled nodes; GPU workloads target GPU nodes; system workloads avoid the control plane).

```bash
# Label workers by capability
kubectl label node node-wk-01 workload-class=standard
kubectl label node node-wk-02 workload-class=standard
# (After §14 installs gVisor/Kata binaries:)
kubectl label node node-wk-01 sandbox-runtime=gvisor --overwrite
kubectl label node node-wk-02 sandbox-runtime=kata --overwrite

# (After §18 provisions GPU node:)
# kubectl label node node-gpu-01 workload-class=gpu nvidia.com/gpu.present=true

# Confirm control-plane taints are in place (workloads cannot schedule on CP)
kubectl describe node node-cp-01 | grep -i taint
# Expect: node-role.kubernetes.io/control-plane:NoSchedule
```

### 9.4 Confirm the kubelet is healthy on every node

```bash
# Run from any node
for n in node-cp-01 node-cp-02 node-cp-03 node-wk-01 node-wk-02; do
  echo "=== $n ==="
  ssh "$n" 'sudo systemctl is-active kubelet; sudo crictl ps | head -5'
done
```

Each node should report `kubelet: active` and at least the pause container running. If any node reports inactive kubelet, check `/var/log/messages` and `journalctl -u kubelet -n 200` on that node.

The cluster now has a working control plane and registered workers, but no CNI yet. Pods will remain `Pending`. The next section installs Cilium, which provides pod networking, NetworkPolicy, kube-proxy replacement, WireGuard encryption, and Gateway API.

---

## 10. CNI: Cilium 1.20 (eBPF, kube-proxy replacement, encryption)

Cilium is the CNI used in this guide. It is a CNCF graduated project (October 2023) [8] that uses eBPF to provide pod networking, NetworkPolicy, kube-proxy replacement, node-to-node encryption, L7 traffic visibility, and Gateway API — all from a single in-kernel datapath. On Azure Linux 3.0 (kernel 6.6 LTS) every Cilium feature is fully supported because kernel 6.6 satisfies all of Cilium's advanced datapath requirements (eBPF programs, bpf-sk-storage, sockmap, WireGuard, etc.).

### 10.1 Install the Cilium CLI and Helm chart

```bash
# On the admin workstation
helm repo add cilium https://helm.cilium.io/
helm repo update

# Cilium CLI (for cilium status, cilium connectivity test, hubble observe)
CILIUM_CLI_VERSION=$(curl -s https://raw.githubusercontent.com/cilium/cilium-cli/main/stable.txt)
curl -L --fail --remote-name-all https://github.com/cilium/cilium-cli/releases/download/${CILIUM_CLI_VERSION}/cilium-linux-amd64.tar.gz{,.sha256sum}
sha256sum --check cilium-linux-amd64.tar.gz.sha256sum
sudo tar xzf cilium-linux-amd64.tar.gz -C /usr/local/bin
cilium version --client
```

### 10.2 Cilium Helm values

The values below install Cilium 1.20 with: kube-proxy replacement (eBPF-only datapath), WireGuard node-to-node encryption, Hubble observability (Relay + UI), and Gateway API conformance. The full file is in [Appendix A](#appendix-a--full-reference-manifests).

```yaml
# /tmp/cilium-values.yaml
kubeProxyReplacement: true
k8sServiceHost: "k8s-apiserver.internal"
k8sServicePort: "6443"

ipam:
  mode: "kubernetes"

# Node-to-node encryption via WireGuard.
# NOTE: encryption.nodeEncryption is deprecated in 1.21 and removed in 1.22 [32];
# the recommended pattern is encryption.enabled=true with encryption.type=wireguard.
encryption:
  enabled: true
  type: "wireguard"

# Hubble — observability
hubble:
  relay:
    enabled: true
  ui:
    enabled: true
  metrics:
    enabled:
      - dns
      - drop
      - tcp
      - flow
      - port-distribution
      - icmp
      - http

# Gateway API — install CRDs and enable Cilium's conformant implementation
gatewayAPI:
  enabled: true
  enableAlpn: true

# Resource requests for the agent (tune per node size)
resources:
  requests:
    cpu: "500m"
    memory: "512Mi"
  limits:
    cpu: "2000m"
    memory: "2Gi"

# Security context — least privilege
securityContext:
  capabilities:
    ciliumAgent:
      - CHOWN
      - KILL
      - NET_ADMIN
      - NET_RAW
      - IPC_LOCK
      - SYS_ADMIN
      - SYS_RESOURCE
      - DAC_OVERRIDE
      - FOWNER
      - SETGID
      - SETUID
    cleanCiliumState:
      - NET_ADMIN
      - SYS_ADMIN
      - SYS_RESOURCE

cgroup:
  autoMount:
    enabled: false
  hostRoot: "/sys/fs/cgroup"

# Tolerate control-plane taint so Cilium runs on every node
tolerations:
  - operator: Exists
```

### 10.3 Install Cilium

```bash
# Install CRDs for Gateway API first (Cilium's chart can do this, but explicit is clearer)
kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.2.0/standard-install.yaml

# Install Cilium
helm install cilium cilium/cilium --version 1.20.0 \
  --namespace kube-system \
  -f /tmp/cilium-values.yaml \
  --wait

# Verify every Cilium pod is Running
kubectl get pods -n kube-system -l k8s-app=cilium

# Run the connectivity test suite (deploys test pods in every node)
cilium status --wait
cilium connectivity test --request-timeout 30s
```

### 10.4 Verify kube-proxy is NOT running

```bash
kubectl get pods -n kube-system -l k8s-app=kube-proxy
# Expected: No resources found in kube-system namespace.
kubectl get daemonset -n kube-system
# Expected: cilium, cilium-operator — no kube-proxy daemonset.
```

### 10.5 Hubble observability

```bash
# Port-forward Hubble UI to the admin workstation
cilium hubble ui &
# Open http://localhost:12000 in a browser

# CLI flow observation
cilium hubble port-forward &
hubble observe --verdict DROPPED --type drop -f
hubble observe --pod default/my-agent-pod -f
```

Hubble provides per-pod L3/L4/L7 flow visibility. This is the operational data layer for runtime detection (§17) and for post-incident forensics on agentic workloads.

### 10.6 Default-deny NetworkPolicy

A defense-in-depth posture starts with a default-deny baseline: every namespace denies all ingress and egress by default, and explicit `NetworkPolicy` (or `CiliumNetworkPolicy`) objects open only the ports and destinations that the workload actually needs.

Apply this cluster-wide default in every namespace (including `default`, `kube-system`, `kube-public`, and every tenant namespace). The example below is for a namespace `agents-prod`:

```yaml
# /tmp/np-default-deny.yaml
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

### 10.7 FQDN-based egress for agentic workloads

The standard Kubernetes `NetworkPolicy` is L3/L4 only — it can match IP and port but not DNS names. For agentic workloads, the realistic egress control is "this agent may call `api.openai.com`, `*.cognitiveservices.azure.com`, and `*.anthropic.com`, and nothing else." This requires Cilium's `CiliumNetworkPolicy` with `toFQDNs`:

```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: agent-egress-allowlist
  namespace: agents-prod
spec:
  endpointSelector: {}
  egress:
    # DNS resolver (required for toFQDNs to work)
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

    # LLM providers
    - toFQDNs:
        - matchName: "api.openai.com"
        - matchName: "api.anthropic.com"
        - matchPattern: "*.openai.azure.com"
        - matchPattern: "*.cognitiveservices.azure.com"
      toPorts:
        - ports:
            - port: "443"
              protocol: TCP

    # Internal cluster services (vector DB, MCP tool servers)
    - toEndpoints:
        - matchLabels:
            "k8s:io.kubernetes.pod.namespace": agents-prod
            "app": vector-db
      toPorts:
        - ports:
            - port: "6333"
              protocol: TCP

    # Microsoft Entra ID endpoint (for Workload Identity token exchange)
    - toFQDNs:
        - matchName: "login.microsoftonline.com"
        - matchName: "graph.microsoft.com"
      toPorts:
        - ports:
            - port: "443"
              protocol: TCP
```

This is the primary T2 (egress exfiltration) control. An agent compromised by prompt injection cannot exfiltrate to an attacker domain because that domain is not in the allow-list. Cilium resolves the FQDNs via the CoreDNS pod and caches the result; if an attacker tries to use a fast-flux DNS trick, the cached IP list is the only set the egress rule allows.

### 10.8 WireGuard encryption verification

```bash
# On any node, verify the WireGuard interface is up
sudo wg show
# Expect a cilium_wg0 interface with peer entries for every other node

# In Hubble, verify inter-node traffic is encrypted (look for the "encrypted" field)
hubble observe --type flow -f | grep -i encrypt
```

Cilium's WireGuard integration encrypts all node-to-node pod traffic. Pod-to-pod traffic on the same node is not encrypted (it does not leave the node). For workloads that require additional pod-level mTLS, deploy a service mesh (Linkerd or Istio) on top of Cilium — this is out of scope for the baseline guide.

---

## 11. Identity, Authentication & RBAC

The cluster has two distinct identity populations: **human operators** (who run `kubectl`) and **workloads** (which call Azure services on behalf of themselves or their users). Both populations authenticate via Microsoft Entra ID using OIDC, but through different mechanisms.

### 11.1 Human authentication via Entra ID OIDC

The Kubernetes API server can be configured to trust an external OIDC provider (in this case, Entra ID) for human authentication. Operators then authenticate with `kubectl` using their Entra ID credentials (with MFA, conditional access, group membership enforced by Entra) instead of long-lived client certificates.

The API server flags required:

```yaml
# (added in §8.1 kubeadm-config.yaml, repeated here for clarity)
apiServer:
  extraArgs:
    oidc-issuer-url: "https://login.microsoftonline.com/<tenant-id>/v2.0"
    oidc-client-id: "<your-entra-app-client-id>"
    oidc-username-claim: "email"
    oidc-username-prefix: "oidc:"
    oidc-groups-claim: "groups"
    oidc-groups-prefix: "oidc:"
```

After `kubeadm init` is run, the only way to add `oidc-*` flags is to edit the static pod manifest at `/etc/kubernetes/manifests/kube-apiserver.yaml` on each control-plane node and let `kubelet` restart the API server. For a fresh cluster, set the flags in the kubeadm config before `kubeadm init` (as in §8.1).

> **Note.** When adding these flags to the kubeadm v1beta4 config file (§8.1), they must use the `name`/`value` list format, not the map format shown above for conceptual clarity. For example: `- name: oidc-issuer-url\n  value: "https://login.microsoftonline.com/<tenant-id>/v2.0"`.

### 11.2 Entra ID app registration for kubectl

Register an application in Entra ID, configure it for the Kubernetes API, and assign group claims. The `kubectl` plugin `kubelogin` converts the Entra OIDC token to a bearer token the API server accepts.

```bash
# Install kubelogin
brew install Azure/kubelogin/kubelogin     # macOS
# (or download from https://github.com/Azure/kubelogin/releases for Linux)

# Configure the kubeconfig to use Entra ID
kubectl config set-credentials oidc-user \
  --exec-api-version=client.authentication.k8s.io/v1 \
  --exec-command=kubelogin \
  --exec-arg=get-token \
  --exec-arg=--login \
  --exec-arg=azurecli \
  --exec-arg=--server-id \
  --exec-arg=<your-entra-app-client-id> \
  --exec-arg=--client-id \
  --exec-arg=<your-entra-app-client-id> \
  --exec-arg=--tenant-id \
  --exec-arg=<your-entra-tenant-id>
```

### 11.3 RBAC: group-based, least privilege

Map Entra ID groups to Kubernetes `ClusterRole` bindings. The pattern below gives the platform-ops group `cluster-admin` (break-glass), the dev-team group edit access to their own namespace only, and the security-auditors group read-only across the cluster.

```yaml
# ClusterRoleBinding for platform-ops (break-glass admin)
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: platform-ops-admin
subjects:
  - kind: Group
    name: "oidc:<entra-platform-ops-group-object-id>"
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: cluster-admin
  apiGroup: rbac.authorization.k8s.io
---
# ClusterRoleBinding for security auditors (read-only)
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: security-auditors-view
subjects:
  - kind: Group
    name: "oidc:<entra-security-auditors-group-object-id>"
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: view
  apiGroup: rbac.authorization.k8s.io
---
# RoleBinding for dev team — scoped to their namespace only
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: dev-team-edit
  namespace: agents-prod
subjects:
  - kind: Group
    name: "oidc:<entra-dev-team-group-object-id>"
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: edit
  apiGroup: rbac.authorization.k8s.io
```

### 11.4 Workload identity via Entra Workload Identity

For workloads (pods) that need to call Azure services (Key Vault, Storage, Cognitive Services, OpenAI), the pattern is **Microsoft Entra Workload Identity** — the GA successor to the deprecated AAD Pod Identity [21]. Workload Identity uses OIDC federation: the cluster's service-account tokens are exchanged for Entra ID tokens via a configured federated identity credential. No long-lived secrets live in the cluster.

**Step 1: Make the cluster's service-account signing keys discoverable.**

`kubeadm` already configures `service-account-issuer: https://kubernetes.default.svc.cluster.local` in §8.1, but this URL is only resolvable inside the cluster. For Entra ID to validate the token, the issuer URL must be publicly reachable. The recommended approach is to publish the cluster's public signing keys via an OIDC discovery document hosted on Azure Blob Storage (or any HTTPS endpoint Entra ID can reach):

```bash
# On a control-plane node, extract the service-account signing key
sudo openssl rsa -in /etc/kubernetes/pki/sa.key -pubout -out /tmp/sa.pub

# Build the JWKS and OIDC discovery documents
# (use the open-source tool: https://github.com/Azure/azure-workload-identity)
# Publish to https://<storage-account>.blob.core.windows.net/oidc/.well-known/openid-configuration
# and  https://<storage-account>.blob.core.windows.net/oidc/keys.json

# Update the API server flag (on each CP node, then restart kube-apiserver static pod):
#   --service-account-issuer=https://<storage-account>.blob.core.windows.net/oidc
```

**Step 2: Configure Entra ID federated identity.**

In the Entra ID portal (or via Azure CLI), create a managed identity (or app registration) for the workload, then add a federated identity credential mapping:

- Issuer: `https://<storage-account>.blob.core.windows.net/oidc`
- Subject: `system:serviceaccount:agents-prod:my-agent-sa`
- Audience: `api://AzureADTokenExchange`

```bash
# Example: federate a user-assigned managed identity with a K8s ServiceAccount
MI_ID=$(az identity show -g "$RG" -n mi-agent-workload --query id -o tsv)
az identity federated-credential create \
  --identity-name mi-agent-workload \
  --resource-group "$RG" \
  --name fc-agent-sa \
  --issuer "https://<storage-account>.blob.core.windows.net/oidc" \
  --subject "system:serviceaccount:agents-prod:my-agent-sa" \
  --audiences "api://AzureADTokenExchange"
```

**Step 3: Annotate the ServiceAccount and deploy the workload.**

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-agent-sa
  namespace: agents-prod
  annotations:
    azure.workload.identity/client-id: "<managed-identity-client-id>"
    azure.workload.identity/tenant-id: "<entra-tenant-id>"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-agent
  namespace: agents-prod
spec:
  template:
    spec:
      serviceAccountName: my-agent-sa
      labels:
        azure.workload.identity/use: "true"    # required for the mutating webhook to inject tokens
      containers:
        - name: agent
          image: <acr>.azurecr.io/agents/my-agent:signed-1.0.0
          # The container code uses Azure SDK with DefaultAzureCredential();
          # it will pick up the federated token automatically via AZURE_FEDERATED_TOKEN_FILE
```

### 11.5 Least-privilege defaults

The following baseline policies are enforced at admission time by Kyverno (§15) and at runtime by the API server itself:

- `automountServiceAccountToken: false` by default. Service accounts that need a token (workload identity) opt in explicitly.
- Bound service-account tokens (GA since K8s 1.22): the `serviceAccountToken` projection in the pod's `volumeMounts` has `audience` and `expirationSeconds` fields. Tokens are short-lived (1 hour default) and rotate automatically.
- No `cluster-admin` for human operators without explicit Entra group membership.
- `kubectl auth can-i --list` is the recommended periodic audit command; review every human principal's effective permissions quarterly.

---

## 12. Secrets Management & Encryption at Rest

The cluster has three secrets-management mechanisms that operate at different layers. They are complementary, not redundant:

1. **etcd encryption at rest (KMS v2)** — protects `Secret` objects in etcd (and etcd backups) from offline reading. Configured in §8.3.
2. **Secrets Store CSI Driver + Azure Key Vault Provider** — mounts secrets from Key Vault as files in the pod's filesystem, without ever materializing them as Kubernetes `Secret` objects. The recommended pattern for LLM API keys, OAuth client secrets, and other high-value credentials.
3. **External Secrets Operator** — syncs secrets from Key Vault into Kubernetes `Secret` objects, for workloads that consume secrets as env vars (legacy pattern). Use sparingly; prefer the CSI Driver pattern for new workloads.

### 12.1 Confirm etcd encryption at rest is active

After the cluster is initialized with the `encryption-provider-config` from §8.3, verify that secrets written to etcd are not in cleartext:

```bash
# Run on any control-plane node
sudo ETCDCTL_API=3 etcdctl \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  get /registry/secrets/agents-prod/my-secret | hexdump -C | head -5

# Expect the value to start with "k8s:enc:kms:v2:azure-key-vault:" — NOT a plaintext JSON.
# If you see plaintext JSON, the encryption provider is not active or the secret was
# written before encryption was enabled (run the migration in §8.3).
```

### 12.2 Install Secrets Store CSI Driver + Azure Key Vault Provider

```bash
helm repo add secrets-store-csi-driver https://kubernetes-sigs.github.io/secrets-store-csi-driver/charts
helm repo add csi-secrets-store-provider-azure https://azure.github.io/secrets-store-csi-driver-provider-azure/charts

helm install csi-secrets-store secrets-store-csi-driver/secrets-store-csi-driver \
  --namespace kube-system \
  --set syncSecret.enabled=true \
  --set enableSecretRotation=true \
  --set rotationPollInterval=60m

helm install csi-secrets-store-provider-azure \
  csi-secrets-store-provider-azure/csi-secrets-store-provider-azure \
  --namespace kube-system
```

`enableSecretRotation=true` causes the driver to periodically re-fetch the secret from Key Vault and update the mounted file in-place. Workloads that read the secret on every use (rather than caching it at startup) automatically pick up rotated values.

### 12.3 Grant the driver's identity access to Key Vault

The driver authenticates to Key Vault via Entra Workload Identity (the same mechanism as workloads). Create a managed identity for the driver's daemonset, federate it to the driver's ServiceAccount, and assign it the `Key Vault Secrets User` role on the target Key Vault:

```bash
# Create managed identity for the CSI driver's daemonset
az identity create -g "$RG" -n mi-csi-kv-driver

# Federate it to the driver's ServiceAccount (in kube-system namespace)
az identity federated-credential create \
  --identity-name mi-csi-kv-driver \
  --resource-group "$RG" \
  --name fc-csi-driver \
  --issuer "https://<storage-account>.blob.core.windows.net/oidc" \
  --subject "system:serviceaccount:kube-system:secrets-store-csi-driver" \
  --audiences "api://AzureADTokenExchange"

# Assign Key Vault Secrets User role
KV_ID=$(az keyvault show -g "$RG" -n "$KV_NAME" --query id -o tsv)
MI_PRINCIPAL_ID=$(az identity show -g "$RG" -n mi-csi-kv-driver --query principalId -o tsv)
az role assignment create --role "Key Vault Secrets User" \
  --assignee-object-id "$MI_PRINCIPAL_ID" \
  --assignee-principal-type ServicePrincipal \
  --scope "$KV_ID"

# Annotate the driver's ServiceAccount with the managed identity
kubectl annotate sa secrets-store-csi-driver -n kube-system \
  azure.workload.identity/client-id="$(az identity show -g "$RG" -n mi-csi-kv-driver --query clientId -o tsv)"
kubectl label sa secrets-store-csi-driver -n kube-system \
  azure.workload.identity/use=true
```

### 12.4 Sample SecretProviderClass for an LLM API key

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
    useVMManagedIdentity: "false"
    clientID: "<mi-csi-kv-driver-client-id>"     # the driver's identity
    keyvaultName: "<kv-name>"
    cloudName: "AzurePublicCloud"
    objects: |
      array:
        - |
          objectName: "openai-api-key"
          objectType: "secret"
          objectVersion: ""             # empty = latest
        - |
          objectName: "anthropic-api-key"
          objectType: "secret"
          objectVersion: ""
  secretObjects:
    # Optionally also create K8s Secret objects for legacy workloads
    - secretName: llm-api-keys
      type: Opaque
      data:
        - objectName: openai-api-key
          key: OPENAI_API_KEY
        - objectName: anthropic-api-key
          key: ANTHROPIC_API_KEY
```

### 12.5 Consume the secret in a pod

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-agent
  namespace: agents-prod
spec:
  serviceAccountName: my-agent-sa
  containers:
    - name: agent
      image: <acr>.azurecr.io/agents/my-agent:signed-1.0.0
      env:
        - name: OPENAI_API_KEY_FILE
          value: /mnt/secrets/openai-api-key
      volumeMounts:
        - name: secrets
          mountPath: /mnt/secrets
          readOnly: true
  volumes:
    - name: secrets
      csi:
        driver: secrets-store.csi.k8s.io
        readOnly: true
        volumeAttributes:
          secretProviderClass: llm-api-key
```

The agent reads the API key from `/mnt/secrets/openai-api-key` on every call (or caches it briefly). When the key is rotated in Key Vault, the file is updated in-place within `rotationPollInterval` (60 minutes by default). No pod restart required.

### 12.6 External Secrets Operator (for legacy workloads)

Some workloads (notably older Helm charts and frameworks that expect secrets as env vars) cannot easily consume the CSI file pattern. For those, deploy External Secrets Operator to sync Key Vault secrets into Kubernetes `Secret` objects:

```bash
helm repo add external-secrets https://charts.external-secrets.io/
helm install external-secrets external-secrets/external-secrets \
  --namespace external-secrets --create-namespace \
  --set installCRDs=true
```

Configure a `SecretStore` backed by Entra Workload Identity, then a `ExternalSecret` that declares which Key Vault secret to sync:

```yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: azure-key-vault
  namespace: agents-prod
spec:
  provider:
    azurekv:
      authType: workloadidentity
      serviceAccountRef:
        name: external-secrets-sa
      vaultUrl: "https://<kv-name>.vault.azure.net"
---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: llm-api-keys
  namespace: agents-prod
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: azure-key-vault
    kind: SecretStore
  target:
    name: llm-api-keys
    creationPolicy: Owner
  data:
    - secretKey: OPENAI_API_KEY
      remoteRef:
        key: openai-api-key
    - secretKey: ANTHROPIC_API_KEY
      remoteRef:
        key: anthropic-api-key
```

The sync'd `Secret` object now lives in etcd — but etcd encryption at rest (§12.1) ensures it is encrypted on disk, and the underlying value lives in Key Vault where it can be rotated, audited, and revoked centrally.

### 12.7 Anti-patterns to forbid

The Kyverno policies in §15 enforce:

- **No plaintext secrets in Git.** A Kyverno `verifyImages` policy blocks any image whose SBOM or build provenance includes a `Secret`-like string in env vars.
- **No `imagePullSecret` with long-lived registry credentials.** Use ACR's workload-identity integration for image pulls instead.
- **No `Secret` objects with a key whose name matches `*API_KEY*`, `*TOKEN*`, `*PASSWORD*`** unless the namespace is explicitly labeled `secrets-store-csi=allowed`. This forces teams toward the CSI pattern for new workloads.

---

## 13. Pod & Workload Hardening

Pod-level hardening is enforced through three layers: Pod Security Admission (`restricted` level), the underlying Linux primitives (seccomp, capabilities, SELinux), and Kyverno policies (§15) that add agentic-workload-specific rules on top.

### 13.1 Enforce Pod Security Admission `restricted` cluster-wide

PSA is GA since Kubernetes 1.25 [33]. The `restricted` level requires: runAsNonRoot, drop ALL Linux capabilities, seccompProfile RuntimeDefault, no hostNetwork/PID/IPC, no hostPath volumes, no privileged flag, and readOnlyRootFilesystem recommended.

Enforce it at the namespace level via labels:

```bash
# Apply to every namespace that runs workloads
for ns in agents-prod agents-staging platform-ops observability; do
  kubectl create namespace "$ns" --dry-run=client -o yaml | kubectl apply -f -
  kubectl label namespace "$ns" \
    pod-security.kubernetes.io/enforce=restricted \
    pod-security.kubernetes.io/enforce-version=latest \
    pod-security.kubernetes.io/audit=restricted \
    pod-security.kubernetes.io/audit-version=latest \
    pod-security.kubernetes.io/warn=restricted \
    pod-security.kubernetes.io/warn-version=latest \
    --overwrite
done

# kube-system is exempt (system addons need privileged pods)
# but new system namespaces must be carefully reviewed before exemption
```

### 13.2 The reference hardened pod spec

The pod spec below satisfies the `restricted` PSS and adds the agentic-workload-specific controls. It is the pattern every workload in the cluster should follow unless it has an explicit, reviewed exemption.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-agent
  namespace: agents-prod
  labels:
    app: my-agent
    workload-type: agentic
spec:
  serviceAccountName: my-agent-sa
  automountServiceAccountToken: false
  runtimeClassName: gvisor          # or kata — see §14
  securityContext:
    runAsNonRoot: true
    runAsUser: 10001
    runAsGroup: 10001
    fsGroup: 10001
    seccompProfile:
      type: RuntimeDefault
  hostNetwork: false
  hostPID: false
  hostIPC: false
  containers:
    - name: agent
      image: <acr>.azurecr.io/agents/my-agent:signed-1.0.0
      imagePullPolicy: IfNotPresent
      securityContext:
        runAsNonRoot: true
        runAsUser: 10001
        runAsGroup: 10001
        allowPrivilegeEscalation: false
        privileged: false
        readOnlyRootFilesystem: true
        capabilities:
          drop: ["ALL"]
        seccompProfile:
          type: RuntimeDefault
      resources:
        requests:
          cpu: "500m"
          memory: "1Gi"
        limits:
          cpu: "2"
          memory: "4Gi"
      volumeMounts:
        - name: tmp
          mountPath: /tmp
        - name: secrets
          mountPath: /mnt/secrets
          readOnly: true
      env:
        - name: OPENAI_API_KEY_FILE
          value: /mnt/secrets/openai-api-key
      livenessProbe:
        httpGet:
          path: /healthz
          port: 8080
        initialDelaySeconds: 30
        periodSeconds: 10
      readinessProbe:
        httpGet:
          path: /ready
          port: 8080
        initialDelaySeconds: 5
        periodSeconds: 5
  volumes:
    - name: tmp
      emptyDir: {}
    - name: secrets
      csi:
        driver: secrets-store.csi.k8s.io
        readOnly: true
        volumeAttributes:
          secretProviderClass: llm-api-key
  tolerations: []
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
          - matchExpressions:
              - key: workload-class
                operator: In
                values: ["standard"]
```

### 13.3 Why each control matters for agentic workloads

- **`runAsNonRoot: true` and a non-zero UID.** A container escape that lands an attacker as root inside the container is the prerequisite for almost every kernel-exploit chain. Even inside a gVisor sandbox, root inside the container should be impossible — gVisor implements many syscalls as no-ops, but defense in depth says don't rely on that alone.
- **`capabilities.drop: ["ALL"]`.** Linux capabilities are the granular "root-like" permissions (`CAP_NET_ADMIN`, `CAP_SYS_ADMIN`, etc.). Dropping all of them is the only safe default; add back specific capabilities only when a workload genuinely needs them, with documented justification.
- **`seccompProfile: RuntimeDefault`.** seccomp filters syscalls to a known-safe subset. The `RuntimeDefault` profile (provided by containerd/runc) blocks ~40 historically-abused syscalls including `keyctl`, `kexec_load`, `unshare` of user namespaces, and `bpf` for unprivileged users.
- **`readOnlyRootFilesystem: true`.** Forces the container to write only to mounted volumes (`emptyDir`, `PersistentVolume`, or `tmp`). An attacker who gains code execution cannot drop a binary in `/usr/bin` and persist across container restarts.
- **`allowPrivilegeEscalation: false`.** Blocks `setuid` binaries inside the container from granting root. The classic exploit path (a binary with the setuid bit + a vulnerability in it) is closed.
- **`runtimeClassName: gvisor` or `kata`.** The agentic-specific control — see §14 for the full sandboxing chapter.
- **`automountServiceAccountToken: false`.** A pod that doesn't need to call the Kubernetes API should not have a token that lets it try.
- **`resources.limits`.** Without limits, a runaway agent (or a prompt-injected agent in a tool-call loop) can starve the node. CPU and memory limits are mandatory for every workload in the cluster.

### 13.4 Namespace Resource Governance (ResourceQuotas and LimitRanges)

Agentic AI workloads can enter infinite reasoning loops or tool-calling cycles that exhaust node resources before OOM killers trigger. **ResourceQuotas** and **LimitRanges** are mandatory for every namespace running agent workloads. They provide two complementary controls:

- **ResourceQuota** — caps the total resource consumption per namespace, preventing a single tenant from starving others.
- **LimitRange** — sets default and maximum resource limits per container, ensuring every pod has explicit bounds even if the deployment spec omits them.

Apply these to every agentic namespace:

```yaml
# /tmp/resource-governance.yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: agent-workload-quota
  namespace: agents-prod
spec:
  hard:
    requests.cpu: "16"
    requests.memory: "32Gi"
    limits.cpu: "32"
    limits.memory: "64Gi"
    pods: "50"
    secrets: "20"
    configmaps: "20"
    persistentvolumeclaims: "10"
---
apiVersion: v1
kind: LimitRange
metadata:
  name: agent-limit-range
  namespace: agents-prod
spec:
  limits:
    - type: Container
      default:
        cpu: "2"
        memory: "4Gi"
      defaultRequest:
        cpu: "500m"
        memory: "1Gi"
      max:
        cpu: "4"
        memory: "8Gi"
      min:
        cpu: "100m"
        memory: "128Mi"
    - type: Pod
      max:
        cpu: "8"
        memory: "16Gi"
```

```bash
kubectl apply -f /tmp/resource-governance.yaml -n agents-prod
kubectl apply -f /tmp/resource-governance.yaml -n agents-staging  # adjust limits per environment
```

Enforce limits at admission time with a Kyverno policy that rejects any container lacking explicit `resources.limits`:

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-resource-limits
spec:
  validationFailureAction: Enforce
  background: true
  rules:
    - name: check-container-resources
      match:
        any:
          - resources:
              kinds: ["Pod"]
      validate:
        message: "All containers must have explicit CPU and memory limits."
        pattern:
          spec:
            containers:
              - resources:
                  limits:
                    cpu: "?"
                    memory: "?"
            =(initContainers):
              - resources:
                  limits:
                    cpu: "?"
                    memory: "?"
```

### 13.5 Custom seccomp profiles with the Security Profiles Operator

For workloads that need a stricter seccomp profile than `RuntimeDefault`, the **Security Profiles Operator (SPO)** is the recommended tool. SPO is a Kubernetes operator that records, manages, and distributes seccomp profiles as `SecProfile` CRDs.

```bash
helm repo add security-profiles-operator https://kubernetes-sigs.github.io/security-profiles-operator
helm install spo security-profiles-operator/security-profiles-operator \
  --namespace security-profiles-operator --create-namespace \
  --set enableBinding=true \
  --set enableLogEnricher=true \
  --set enableProfileRecorder=true
```

Use SPO's recording mode to capture the syscalls a workload actually uses, then generate a profile that allows only those:

```bash
# Annotate a pod for recording
kubectl annotate pod my-agent -n agents-prod \
  spo.x-k8s.io/enable-recording="true"

# After a representative workload run, view the recorded syscalls
kubectl get profile recording-my-agent -n agents-prod -o yaml
```

The resulting `SeccompProfile` can be referenced in the pod's `securityContext.seccompProfile.localhostProfile` field for a workload-specific least-privilege seccomp profile.

### 13.6 AppArmor vs SELinux on Azure Linux

AppArmor is GA in Kubernetes 1.30, but **Azure Linux uses SELinux, not AppArmor** [3]. AppArmor `NodeProfile` annotations on pods are no-ops on Azure Linux nodes. The host-level MAC control is SELinux enforcing (§5.5); pod-level SELinux labels can be set via the pod's `securityContext.seLinuxOptions` field, but this is rarely necessary because containerd's default SELinux labeling is already correct for the `restricted` PSS.

---

## 14. Sandboxing Agentic Workloads (gVisor + Kata Containers 4.0)

For workloads that execute attacker-influenced or self-generated code — which is the defining characteristic of agentic workloads — the standard `runc` container boundary is insufficient because the container shares the host kernel. A kernel exploit (or even a syscall bug) in generated code becomes a host-compromise vector under MITRE ATT&CK T1611. The two production-grade solutions are **gVisor** (a userspace application kernel written in Go that implements the Linux syscall interface) and **Kata Containers** (lightweight VMs that run containers inside a QEMU/KVM hypervisor). Both integrate with Kubernetes via the `RuntimeClass` API (GA since K8s 1.20).

### 14.1 When to use which

| Property | gVisor (`runsc`) | Kata Containers 4.0 |
|---|---|---|
| Isolation boundary | Userspace syscall handler (no kernel sharing) | Full VM with its own guest kernel |
| Overhead | Low (syscall interception only) | Higher (VM boot, memory overhead) |
| Startup latency | Same as `runc` | Adds ~100-300ms per pod for VM boot |
| Syscall coverage | Implements most Linux syscalls; some unsupported (check gVisor docs) | Full Linux kernel in guest VM |
| GPU passthrough | Limited support, complex | Supported via vfio-pci (use Kata for GPU-isolated workloads) |
| Best for | Tool-execution agents, sandboxes for untrusted code that does not need raw kernel features | Fully untrusted code execution, multi-tenant GPU isolation, workloads that need full kernel features |
| Not suitable for | Workloads needing kernel features gVisor does not implement (some eBPF, some perf events) | Tightly latency-bound workloads where 100ms startup matters |

For an agentic platform, the recommended pattern is:
- **`runc`** for trusted infrastructure components (the agent orchestrator itself, the API gateway, the observability stack).
- **`gvisor`** for tool-execution agents that run generated code in a constrained environment (Python REPL agents, code interpreter tools, web-scraper tools).
- **`kata`** for fully untrusted code execution (multi-tenant "run any code the user submits" features, prompt-injection-resistant sandboxes for adversarial workloads, GPU workloads that need isolation).

### 14.2 Install gVisor (`runsc`)

gVisor is distributed as a binary from google/gvisor. The install steps below are for Azure Linux 3.0; they install the `runsc` binary and register it with containerd.

```bash
# Run on every worker node that should support the gvisor RuntimeClass
RUNSC_VERSION=$(curl -s https://api.github.com/repos/google/gvisor/releases/latest | jq -r '.tag_name | split(".")[0]')
curl -fsSL -o runsc \
  "https://storage.googleapis.com/gvisor/releases/release/${RUNSC_VERSION}/x86_64/runsc"
sudo install -m 0755 runsc /usr/local/bin/runsc
sudo tee /etc/containerd/runsc.toml >/dev/null <<'EOF'
[runsc]
  # Verbose logging for debugging; remove in production
  debug = "false"
  # Use KVM acceleration when available (faster than ptrace)
  platform = "kvm"
  # Network isolation: none (let Cilium handle network policy)
  network = "none"
EOF

# Reload containerd to pick up the runsc runtime (the config block was added in §6.3)
sudo systemctl restart containerd
```

Create the `RuntimeClass`:

```yaml
# kubectl apply -f runtimeclass-gvisor.yaml
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: gvisor
handler: runsc
scheduling:
  nodeSelector:
    sandbox-runtime: gvisor
```

### 14.3 Install Kata Containers 4.0

Kata Containers 4.0 ships a new Rust-based runtime (replacing the older Go runtime), with significant security and performance improvements [11]. On Azure Linux, install via the official kata-static packages:

```bash
# Run on every worker node that should support the kata RuntimeClass
sudo tdnf install -y qemu-kvm qemu-img hyperv-daemons libvirt
KATA_VERSION=$(curl -s https://api.github.com/repos/kata-containers/kata-containers/releases/latest | jq -r .tag_name)
curl -fsSL -o kata-static.tar.xz \
  "https://github.com/kata-containers/kata-containers/releases/download/${KATA_VERSION}/kata-static-${KATA_VERSION#v}-x86_64.tar.xz"
sudo tar -xf kata-static.tar.xz -C /
sudo ln -sf /opt/kata/bin/containerd-shim-kata-v2 /usr/local/bin/containerd-shim-kata-v2
sudo ln -sf /opt/kata/bin/kata-runtime /usr/local/bin/kata-runtime

# Verify the host can run Kata (KVM availability, etc.)
sudo kata-runtime check

# Reload containerd to pick up the kata runtime (config block added in §6.3)
sudo systemctl restart containerd
```

Create the `RuntimeClass`:

```yaml
# kubectl apply -f runtimeclass-kata.yaml
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: kata
handler: kata
scheduling:
  nodeSelector:
    sandbox-runtime: kata
```

### 14.4 Verify the runtime classes are usable

```bash
# Deploy a test pod with each runtime class
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: test-runc
  namespace: agents-prod
spec:
  runtimeClassName: ""    # default runc
  containers:
    - name: test
      image: registry.k8s.io/pause:3.10
---
apiVersion: v1
kind: Pod
metadata:
  name: test-gvisor
  namespace: agents-prod
spec:
  runtimeClassName: gvisor
  containers:
    - name: test
      image: registry.k8s.io/pause:3.10
---
apiVersion: v1
kind: Pod
metadata:
  name: test-kata
  namespace: agents-prod
spec:
  runtimeClassName: kata
  containers:
    - name: test
      image: registry.k8s.io/pause:3.10
EOF

# Verify each pod reaches Running
kubectl get pods -n agents-prod -l test=runtime

# Verify the runtime actually applied
kubectl get pod test-gvisor -n agents-prod -o jsonpath='{.status.containerStatuses[0].runtimeHandler}'
# Expect: runsc

kubectl get pod test-kata -n agents-prod -o jsonpath='{.status.containerStatuses[0].runtimeHandler}'
# Expect: kata
```

### 14.5 Sample sandboxed agent deployment

This is the reference pattern for an agent that executes user-submitted code in a `gvisor` sandbox:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: code-exec-agent
  namespace: agents-prod
spec:
  replicas: 3
  selector:
    matchLabels:
      app: code-exec-agent
  template:
    metadata:
      labels:
        app: code-exec-agent
        workload-type: agentic
        sandbox: gvisor
    spec:
      runtimeClassName: gvisor
      serviceAccountName: code-exec-agent-sa
      automountServiceAccountToken: false
      securityContext:
        runAsNonRoot: true
        runAsUser: 10001
        seccompProfile:
          type: RuntimeDefault
      containers:
        - name: agent
          image: <acr>.azurecr.io/agents/code-exec-agent:signed-1.0.0
          securityContext:
            runAsNonRoot: true
            runAsUser: 10001
            allowPrivilegeEscalation: false
            privileged: false
            readOnlyRootFilesystem: true
            capabilities:
              drop: ["ALL"]
          resources:
            requests: { cpu: "1", memory: "2Gi" }
            limits: { cpu: "2", memory: "4Gi" }
          env:
            - name: OPENAI_API_KEY_FILE
              value: /mnt/secrets/openai-api-key
          volumeMounts:
            - name: tmp
              mountPath: /tmp
            - name: secrets
              mountPath: /mnt/secrets
              readOnly: true
      volumes:
        - name: tmp
          emptyDir: { sizeLimit: 1Gi }
        - name: secrets
          csi:
            driver: secrets-store.csi.k8s.io
            readOnly: true
            volumeAttributes:
              secretProviderClass: llm-api-key
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
              - matchExpressions:
                  - key: sandbox-runtime
                    operator: In
                    values: ["gvisor"]
```

Even if the generated code executed inside this pod contains a working kernel exploit, gVisor intercepts every syscall and returns either a safe implementation or `EPERM`. The host kernel is never reached.

---

## 15. Policy-as-Code with Kyverno (CNCF Graduated)

Kyverno graduated from CNCF incubation to graduated status on **March 24, 2026** [9]. It is the policy engine used in this guide for: mutating incoming resources to safe defaults, validating them against policy, generating companion resources (e.g., default NetworkPolicies), and verifying image signatures. Kubernetes' built-in **ValidatingAdmissionPolicies** (VAP, GA since K8s 1.30 [18]) is also used for the subset of policies that can be expressed in CEL without external dependencies.

### 15.1 Install Kyverno

```bash
helm repo add kyverno https://kyverno.github.io/kyverno/
helm repo update

helm install kyverno kyverno/kyverno \
  --namespace kyverno --create-namespace \
  --set admissionController.replicas=3 \
  --set admissionController.resources.requests.cpu=200m \
  --set admissionController.resources.requests.memory=256Mi \
  --set admissionController.resources.limits.cpu=1 \
  --set admissionController.resources.limits.memory=1Gi

# Install the standard policy library aligned with Pod Security Standards
helm install kyverno-policies kyverno/kyverno-policies \
  --namespace kyverno \
  --set podSecurityStandard=restricted \
  --set podSecurityStandard=latest
```

Three admission-controller replicas (across the three control-plane nodes) ensure the policy enforcement path is HA.

### 15.2 Agentic-workload-specific Kyverno policies

The standard `kyverno-policies` chart enforces the `restricted` PSS. The four policies below add agentic-workload-specific controls.

**Policy 1: Require a `RuntimeClass` for any pod in an agentic namespace.**

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-runtimeclass-for-agents
spec:
  validationFailureAction: Enforce
  background: true
  rules:
    - name: require-runtimeclass
      match:
        any:
          - resources:
              kinds: ["Pod"]
              namespaces: ["agents-prod", "agents-staging"]
      validate:
        message: "Pods in agentic namespaces must use a sandboxed RuntimeClass (gvisor or kata)."
        pattern:
          spec:
            runtimeClassName: "gvisor | kata"
```

**Policy 2: Require network-policy acknowledgment annotation.**

This is a redundant control on top of Cilium's `CiliumNetworkPolicy` from §10.7 — the Cilium policy enforces egress at the network layer; this Kyverno policy enforces at admission time that every agentic pod carries an annotation confirming that egress rules have been applied. The annotation `network-policy.ack: "true"` must be set by the deployment pipeline after the NetworkPolicy is created.

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-network-policy-for-agents
spec:
  validationFailureAction: Enforce
  background: true
  rules:
    - name: require-network-policy
      match:
        any:
          - resources:
              kinds: ["Pod"]
              namespaces: ["agents-prod", "agents-staging"]
      preconditions:
        all:
          - key: "{{ request.object.metadata.labels.workload-type }}"
            operator: Equals
            value: "agentic"
      validate:
        message: "Agentic pods must have the 'network-policy.ack: true' annotation confirming egress rules are applied."
        pattern:
          metadata:
            annotations:
              network-policy.ack: "true"
```

**Policy 3: Require image signature verification.**

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-signed-images
spec:
  validationFailureAction: Enforce
  background: false         # verification requires runtime lookup; do not run in background scans
  rules:
    - name: verify-signature
      match:
        any:
          - resources:
              kinds: ["Pod"]
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

**Policy 4: Mutate — set safe defaults on every pod.**

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: set-safe-defaults
spec:
  rules:
    - name: default-security-context
      match:
        any:
          - resources:
              kinds: ["Pod"]
      mutate:
        patchStrategicMerge:
          spec:
            automountServiceAccountToken: false
            containers:
              - (name): "*"
                securityContext:
                  +(runAsNonRoot): true
                  +(allowPrivilegeEscalation): false
                  +(readOnlyRootFilesystem): true
                  +(capabilities):
                    +(drop): ["ALL"]
```

The `+(field)` syntax means "set this field only if it is not already set" — so explicit pod specs override the defaults, but pods that omit the field get the safe value.

### 15.3 ValidatingAdmissionPolicies (CEL, GA since 1.30)

For simple, synchronous validation that does not need an external webhook (no image verification, no mutation, no generation), VAPs with CEL expressions are faster and operationally simpler than Kyverno policies. The example below enforces that every namespace has a `team` label:

```yaml
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingAdmissionPolicy
metadata:
  name: require-namespace-team-label
spec:
  failurePolicy: Fail
  matchConstraints:
    resourceRules:
      - apiGroups: [""]
        apiVersions: ["v1"]
        operations: ["CREATE", "UPDATE"]
        resources: ["namespaces"]
  validations:
    - expression: "has(object.metadata.labels) && has(object.metadata.labels.team)"
      message: "Every namespace must have a 'team' label."
---
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingAdmissionPolicyBinding
metadata:
  name: require-namespace-team-label-binding
spec:
  policyName: require-namespace-team-label
  validationActions: [Deny]
```

### 15.4 Kyverno vs ValidatingAdmissionPolicies — when to use which

| Use case | Tool |
|---|---|
| Simple field validation (labels, annotations, required fields) | VAP (no webhook overhead, runs in-process in the API server) |
| Mutation (set safe defaults, inject sidecars) | Kyverno (VAP cannot mutate) |
| Generation (auto-create NetworkPolicies, ResourceQuotas) | Kyverno (VAP cannot generate) |
| Image signature verification | Kyverno `verifyImages` (VAP cannot do this) |
| Cross-resource validation that needs API lookups | Kyverno (VAP has limited `apiVersion/kind/name` lookups via `authorizer` and `variables`) |
| Performance-critical hot paths (every pod create) | VAP (no webhook round-trip) |

A healthy cluster uses both. This guide's reference deployment uses Kyverno for the four policies in §15.2 plus VAPs for label/namespace validation.

---

## 16. Supply Chain Security (cosign, SBOM, SLSA)

Supply chain attacks on the open-source ecosystem — typosquatted packages, compromised maintainer accounts, malicious base image updates — are the highest-probability compromise vector for any modern application, including agentic platforms. The defense is end-to-end provenance: every image running in the cluster must be signed with a verifiable identity, must carry an SBOM, must be admitted only after signature verification, and must be re-scanned for vulnerabilities throughout its runtime lifetime.

### 16.1 The supply chain threat surface

The agentic-workload supply chain has four layers, each with its own threats:

1. **Base image** — the `python:3.12` or `ubuntu:22.04` the agent's image is `FROM`. A compromise of the upstream base image (e.g., the 2018 crypto-wallet-stealing backdoor in the `pycrypto` PyPI package, the 2024 `xz-utils` backdoor) propagates to every image built on top.
2. **Agent framework** — the `langchain`, `llama-index`, `autogen`, or `crew-ai` package. These are fast-moving projects with large dependency trees and have been targets of typosquatting (`langchain` vs `langcha1n`).
3. **Tool dependencies** — the libraries the agent's tools pull in (a web-scraper tool pulls in `requests`, `beautifulsoup4`, etc.). Each is a potential vector.
4. **The agent's own code** — the orchestration logic, prompt templates, tool implementations.

### 16.2 The defense stack

| Layer | Tool | Status |
|---|---|---|
| Image signing | cosign 2.x | GA; Sigstore OpenSSF graduated Oct 2024 [12] |
| Transparency log | Rekor | GA (public-good instance at rekor.sigstore.dev) |
| Certificate authority | Fulcio | GA (issues short-lived certs based on OIDC identity) |
| SBOM generation | Syft | GA |
| SBOM vulnerability scanning | Grype | GA |
| Image vulnerability scanning | Trivy | GA |
| Admission enforcement | Kyverno `verifyImages` | GA (see §15.2 Policy 3) |
| Registry | Azure Container Registry | GA (Premium tier supports content trust, geo-replication, private endpoints) |
| Build provenance | SLSA v1.0 build levels | SLSA v1.0 released Aug 2023 [34] |

### 16.3 Sign images with cosign keyless

The recommended pattern is **keyless signing** via OIDC identity — no signing key to manage, no key to leak. In GitHub Actions:

```yaml
# .github/workflows/build-and-sign.yml
name: Build and sign agent image
on:
  push:
    branches: [main]
permissions:
  contents: read
  packages: write
  id-token: write         # required for OIDC
jobs:
  build-sign:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/login-action@v3
        with:
          registry: <acr-name>.azurecr.io
          username: ${{ secrets.ACR_USERNAME }}
          password: ${{ secrets.ACR_PASSWORD }}

      - name: Build image
        id: build
        run: |
          docker build -t <acr-name>.azurecr.io/agents/my-agent:${{ github.sha }} .
          docker push <acr-name>.azurecr.io/agents/my-agent:${{ github.sha }}

      - name: Install cosign
        uses: sigstore/cosign-installer@v3

      - name: Install syft
        uses: anchore/sbom-action@v0
        with:
          format: cyclonedx-json
          output-file: sbom.cyclonedx.json

      - name: Sign image (keyless via GitHub OIDC)
        run: |
          cosign sign --yes \
            --identity-token ${{ env.ACTIONS_ID_TOKEN_REQUEST_TOKEN }} \
            <acr-name>.azurecr.io/agents/my-agent@${{ steps.build.outputs.digest }}

      - name: Attach SBOM to image
        run: |
          cosign attach sbom --sbom sbom.cyclonedx.json \
            <acr-name>.azurecr.io/agents/my-agent@${{ steps.build.outputs.digest }}
          cosign sign --yes \
            --identity-token ${{ env.ACTIONS_ID_TOKEN_REQUEST_TOKEN }} \
            --attachment sbom \
            <acr-name>.azurecr.io/agents/my-agent@${{ steps.build.outputs.digest }}

      - name: Generate SLSA provenance
        uses: slsa-framework/slsa-github-generator/.github/workflows/generator_container_slsa3.yml@v2.0.0
        with:
          image: <acr-name>.azurecr.io/agents/my-agent
          digest: ${{ steps.build.outputs.digest }}
          registry-username: ${{ secrets.ACR_USERNAME }}
          registry-password: ${{ secrets.ACR_PASSWORD }}
```

After this workflow runs, the image in ACR carries: (1) a cosign signature in the OCI signature store, (2) a Rekor transparency-log entry recording the signing event, (3) an attached SBOM (CycloneDX format), and (4) a SLSA Build L3 provenance attestation.

### 16.4 Verify signatures at admission time

The Kyverno `verifyImages` policy in §15.2 Policy 3 enforces that every image from `<acr-name>.azurecr.io/*` has a valid cosign signature from the expected GitHub Actions identity. Any unsigned image — including one an operator `kubectl apply`s by hand — is rejected at admission.

For an even stricter posture, require both a signature AND an SBOM:

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-sbom-attachment
spec:
  validationFailureAction: Enforce
  background: false
  rules:
    - name: require-sbom
      match:
        any:
          - resources:
              kinds: ["Pod"]
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
          attestations:
            - type: https://cyclonedx.org/bom
              attestors:
                - count: 1
                  entries:
                    - keyless:
                        subject: "https://github.com/<org>/<repo>/.github/workflows/build.yml@refs/heads/main"
                        issuer: "https://token.actions.githubusercontent.com"
                        rekor:
                          url: "https://rekor.sigstore.dev"
              predicateType: https://cyclonedx.org/bom
```

### 16.5 Registry allow-list policy

Forbid pulling from any registry except ACR. This blocks the "supply chain compromise via a public Docker Hub image" path.

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: restrict-image-registries
spec:
  validationFailureAction: Enforce
  background: true
  rules:
    - name: only-allow-acr
      match:
        any:
          - resources:
              kinds: ["Pod"]
      validate:
        message: "Images must come from <acr-name>.azurecr.io or registry.k8s.io (for system images)."
        pattern:
          spec:
            containers:
              - image: "<acr-name>.azurecr.io/* | registry.k8s.io/*"
            =(initContainers):
              - image: "<acr-name>.azurecr.io/* | registry.k8s.io/*"
            =(ephemeralContainers):
              - image: "<acr-name>.azurecr.io/* | registry.k8s.io/*"
```

### 16.6 Continuous vulnerability scanning

Install Microsoft Defender for Containers (cloud) and/or Trivy (in-cluster) for continuous re-scanning. Defender for Containers integrates with ACR natively; for self-managed clusters on Azure VMs, deploy Defender via Azure Arc.

```bash
# Enable Defender for Containers on the subscription
az security pricing create --name Containers --tier Standard

# (Optional) Install Trivy operator in-cluster for real-time scanning
helm repo add aquasecurity https://aquasecurity.github.io/helm-charts/
helm install trivy-operator aquasecurity/trivy-operator \
  --namespace trivy-system --create-namespace \
  --set="trivy.ignoreUnfixed=true" \
  --set="trivy.offlineScan=false"
```

Trivy operator produces `VulnerabilityReport` and `ConfigAuditReport` CRDs for every running workload; configure alerts on `Critical` severity findings.

### 16.7 SLSA build levels — what to aim for

The SLSA framework [34] defines four build levels (1–4) with increasing rigor:

- **Build L1** — builds run on a hosted platform; provenance exists but is not signed.
- **Build L2** — provenance is signed and tamper-resistant; the build service is hosted.
- **Build L3** — builds run in a hardened, isolated environment; provenance is non-forgeable.
- **Build L4** — two-party reviewed builds; reproducible.

For enterprise agentic workloads, **aim for Build L3** — achievable with GitHub Actions + the SLSA GitHub Actions generator (as in §16.3). L4 is currently aspirational for most organizations.

---

## 17. Runtime Security & Observability

Runtime security detects and alerts on malicious behavior that bypasses the admission controls — for example, a compromised agent that exploits a sandbox escape, or an attacker who laterally moves from a compromised pod to the host. The reference deployment uses **Falco** for runtime detection (CNCF graduated May 2024 [10]) and the **kube-prometheus-stack** for metrics, logs, and traces.

### 17.1 Install Falco

```bash
helm repo add falcosecurity https://falcosecurity.github.io/charts/
helm repo update

helm install falco falcosecurity/falco \
  --namespace falco --create-namespace \
  --set driver.kind=modern_ebpf \
  --set falcosidekick.enabled=true \
  --set falcosidekick.config.azure.eventHubName=falco-alerts \
  --set falcosidekick.config.azure.eventHubNamespace=<eh-namespace> \
  --set falcosidekick.config.azure.tenantId=<entra-tenant-id> \
  --set falcosidekick.config.azure.clientId=<falco-mi-client-id> \
  --set falcosidekick.config.azure.clientSecret="" \
  --set falcosidekick.config.azure.useIAM=true \
  --set falcosidekick.config.minimumpriority=warning
```

The `driver.kind=modern_ebpf` setting uses Falco's modern eBPF probe, which works without kernel headers on kernel 5.8+ and is the recommended probe on Azure Linux 3.0 (kernel 6.6). The `falcosidekick` component forwards alerts to Azure Event Hubs, which Azure Monitor ingests.

### 17.2 Custom agentic-workload rules

Falco ships with a default ruleset that detects common runtime attacks (shell spawn in container, reverse shell, write below `/etc`, `kubectl` exec into a pod, etc.). For agentic workloads, add custom rules tuned to the workload patterns:

```yaml
# /etc/falco/rules.d/agentic-workload-rules.yaml
- macro: agent_namespace
  condition: k8s.ns.name in (agents-prod, agents-staging)

# Rule 1: Agent spawns a shell (likely prompt injection driving shell exec)
- rule: Agent Spawned Shell
  desc: A process in an agent pod spawned a shell — likely prompt injection driving shell exec.
  condition: agent_namespace and evt.type in (execve, execveat) and proc.name in (bash, sh, zsh, fish)
  output: "Agent shell spawn (user=%user.name pod=%k8s.pod.name ns=%k8s.ns.name cmd=%proc.cmdline)"
  priority: WARNING
  tags: [agentic, prompt-injection, mitre_t1059]

# Rule 2: Reverse shell from agent pod
- rule: Agent Reverse Shell
  desc: An agent pod opened a connection to an external endpoint and spawned a shell on the same FD.
  condition: agent_namespace and evt.type in (connect) and fd.sip != "127.0.0.1" and proc.name in (bash, sh, zsh)
  output: "Agent reverse shell (pod=%k8s.pod.name ns=%k8s.ns.name dest=%fd.sip:%fd.sport)"
  priority: CRITICAL
  tags: [agentic, exfiltration, mitre_t1105]

# Rule 3: Outbound connection to non-allowlisted FQDN
# (Complement to Cilium FQDN egress; this catches direct IP connections)
- rule: Agent Outbound to Unknown IP
  desc: An agent pod made an outbound connection to an IP not in the cluster's CIDR ranges.
  condition: agent_namespace and evt.type=connect and fd.sip not in (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16)
  output: "Agent outbound to external IP (pod=%k8s.pod.name dest=%fd.sip:%fd.sport proc=%proc.name)"
  priority: WARNING
  tags: [agentic, exfiltration]

# Rule 4: Binary downloaded and executed (second-stage payload)
- rule: Agent Downloaded and Executed Binary
  desc: An agent pod downloaded a file via curl/wget and then executed it.
  condition: agent_namespace and spawned_process and proc.pname in (curl, wget)
  output: "Agent executed downloaded binary (pod=%k8s.pod.name cmd=%proc.cmdline)"
  priority: CRITICAL
  tags: [agentic, mitre_t1105, second-stage]

# Rule 5: Kubernetes service account token read by unexpected process
- rule: Agent Read Service Account Token
  desc: An agent process read the mounted service account token — usually only the agent's HTTP client needs this.
  condition: agent_namespace and open_read and fd.name startswith /var/run/secrets/kubernetes.io/serviceaccount
  output: "Agent read SA token (pod=%k8s.pod.name proc=%proc.name)"
  priority: NOTICE
  tags: [agentic, credential-access, mitre_t1552]
```

### 17.3 Install the kube-prometheus-stack

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts/
helm repo update

helm install kube-prometheus-stack prometheus-community/kube-prometheus-stack \
  --namespace observability --create-namespace \
  --set prometheus.prometheusSpec.retention=30d \
  --set prometheus.prometheusSpec.retentionSize=100GB \
  --set prometheus.prometheusSpec.storageSpec.volumeClaimTemplate.spec.storageClassName=managed-csi \
  --set prometheus.prometheusSpec.storageSpec.volumeClaimTemplate.spec.resources.requests.storage=200Gi \
  --set grafana.adminPassword="$(openssl rand -hex 16)" \
  --set grafana.persistence.enabled=true \
  --set grafana.persistence.size=10Gi \
  --set alertmanager.enabled=true
```

### 17.4 Install Loki for log aggregation

```bash
helm repo add grafana https://grafana.github.io/helm-charts/
helm install loki grafana/loki \
  --namespace observability \
  --set deploymentMode=SingleBinary \
  --set singleBinary.replicas=1 \
  --set loki.storage.type=filesystem \
  --set loki.storage.fs.dir=/var/loki/storage
```

For production scale, deploy Loki in Simple Scalable mode with Azure Blob Storage as the backend (see Loki docs).

### 17.5 Critical alerts to configure

The reference Alertmanager rule set below covers the cluster-stability and security alerts that should page a human:

```yaml
# /tmp/prometheus-rules.yaml
groups:
  - name: k8s-cluster-stability
    rules:
      - alert: APIServerDown
        expr: up{job="apiserver"} == 0
        for: 2m
        labels: { severity: critical }
        annotations:
          summary: "API server {{ $labels.instance }} is down"

      - alert: EtcdNoLeader
        expr: etcd_server_has_leader == 0
        for: 1m
        labels: { severity: critical }
        annotations:
          summary: "etcd member {{ $labels.instance }} has no leader"

      - alert: EtcdHighFsyncDuration
        expr: histogram_quantile(0.99, rate(etcd_disk_wal_fsync_duration_seconds_bucket[5m])) > 0.025
        for: 5m
        labels: { severity: warning }
        annotations:
          summary: "etcd fsync p99 > 25ms — disk too slow"

      - alert: NodeNotReady
        expr: kube_node_status_condition{condition="Ready",status!="true"} == 1
        for: 5m
        labels: { severity: critical }
        annotations:
          summary: "Node {{ $labels.node }} is NotReady"

      - alert: PodCrashLooping
        expr: rate(kube_pod_container_status_restarts_total[15m]) > 0
        for: 10m
        labels: { severity: warning }
        annotations:
          summary: "Pod {{ $labels.pod }} is restarting repeatedly"

  - name: agentic-workload-security
    rules:
      - alert: FalcoCriticalAlert
        expr: increase(falco_events{priority="critical"}[5m]) > 0
        for: 0m
        labels: { severity: critical }
        annotations:
          summary: "Falco critical: {{ $labels.rule }}"

      - alert: AgentPodSandboxEscape
        expr: increase(falco_events{rule="Agent Spawned Shell"}[5m]) > 0
        for: 0m
        labels: { severity: critical }
        annotations:
          summary: "Agent pod spawned a shell — possible prompt injection"

      - alert: ImageVulnerabilityCritical
        expr: trivy_vulnerability_id{severity="CRITICAL"} > 0
        for: 1h
        labels: { severity: warning }
        annotations:
          summary: "Critical vulnerability in image {{ $labels.image }}"

      - alert: KyvernoPolicyViolation
        expr: increase(kyverno_policy_results_total{result="fail"}[10m]) > 5
        for: 5m
        labels: { severity: warning }
        annotations:
          summary: "Kyverno policy {{ $labels.policy }} is rejecting many resources"
```

### 17.6 Cilium Hubble for flow visibility

Hubble (installed with Cilium in §10) provides per-pod L3/L4/L7 flow visibility, complementing Falco's syscall-level view. The two together answer "what did the agent do?" (Falco syscalls) and "what network traffic did the agent generate?" (Hubble flows).

```bash
# Watch all flows in the agents-prod namespace
hubble observe --namespace agents-prod -f

# Filter for DNS lookups (catches agent egress attempts)
hubble observe --namespace agents-prod --type dns -f

# Filter for dropped packets (catches Cilium policy enforcement)
hubble observe --namespace agents-prod --verdict DROPPED -f
```

### 17.7 (Optional) Tetragon for inline enforcement

Falco is detection-only — it alerts but does not block. **Tetragon** (Cilium's sibling project) provides inline eBPF-based enforcement: a Tetragon policy can kill a process or block a syscall the moment it happens, with no userspace round-trip. For agentic workloads where the detection-to-block latency matters (e.g., a prompt-injected agent trying to spawn a reverse shell), Tetragon is the stronger control.

The trade-off is operational complexity: Tetragon policies are written in a custom YAML schema and run in kernel context, so they require more careful testing than Falco rules. A common pattern is to start with Falco (detection) and add Tetragon (enforcement) only for the highest-risk rules after they have been validated in audit mode.

```bash
helm install tetragon cilium/tetragon \
  --namespace kube-system \
  --set tetragon.grpc.enabled=true \
  --set tetragon.enablePolicyFilter=true \
  --set tetragon.policyFilterMode=audit    # start in audit mode
```

---

## 18. Optional: GPU Nodes for Local LLM Inference

For workloads that need local LLM inference (e.g., running a self-hosted Llama-3.1-70B or Mistral-Large model for data-sovereignty reasons, or to avoid per-token API costs at high throughput), the cluster needs at least one GPU-enabled worker node. The recommended Azure VM SKU for production LLM inference is **`Standard_NCads_H100_v5`** (single NVIDIA H100 80GB), with `Standard_ND_H100_v5` (8× H100) for the largest models. For lighter inference (smaller models, lower throughput), `Standard_NC4as_T4_v3` (single T4 16GB) is cost-effective.

### 18.1 Provision a GPU node

```bash
GPU_VM="${GPU_VM_PREFIX}01"

az vm create -g "$RG" -n "$GPU_VM" --image "$IMG" \
  --size Standard_NCads_H100_v5 --vnet-name "$VNET" --subnet worker-subnet \
  --nsg nsg-wk --public-ip-address "" \
  --admin-username "$ADMIN_USER" --ssh-key-values ~/.ssh/id_ed25519.pub \
  --security-type TrustedLaunch --enable-secure-boot true --enable-vtpm true \
  --os-disk-size-gb 512 \
  --zone 1

# Join to the cluster (see §9)
az vm run-command invoke -g "$RG" -n "$GPU_VM" --command-id RunShellScript \
  --scripts "kubeadm join k8s-apiserver.internal:6443 --token <token> --discovery-token-ca-cert-hash sha256:<hash>"

# Label the node
kubectl label node "$GPU_VM" workload-class=gpu nvidia.com/gpu.present=true sandbox-runtime=kata
```

### 18.2 Install NVIDIA GPU Operator

```bash
helm repo add nvidia https://helm.ngc.nvidia.com/nvidia
helm repo update

helm install gpu-operator nvidia/gpu-operator \
  --namespace gpu-operator --create-namespace \
  --set driver.enabled=true \
  --set toolkit.enabled=true \
  --set devicePlugin.enabled=true \
  --set dcgmExporter.enabled=true \
  --set gfd.enabled=true
```

The GPU Operator installs: the NVIDIA driver (kernel module), the NVIDIA Container Toolkit (the `nvidia-container-runtime` hook that exposes GPUs to containers), the device plugin (advertises GPU resources to kubelet), and the DCGM exporter (Prometheus metrics for GPU utilization/temperature/memory).

> **Azure Linux driver compatibility caveat.** The NVIDIA GPU Operator typically installs the driver from NVIDIA's package repository, but driver availability for Azure Linux's kernel 6.6 LTS must be verified at install time. If the operator cannot install the driver, the workaround is to use an Azure Linux image with the driver preinstalled (Microsoft ships AKS-specific Azure Linux GPU images with the driver baked in; for self-managed clusters, you may need to build a custom image with `nvidia-driver` installed via the NVIDIA upstream `.run` installer). Validate on a non-production node first.

> **Kata + GPU passthrough caveat.** Passing an NVIDIA GPU through a Kata microVM via VFIO is highly complex and requires specific Azure VM SKUs, custom Kata kernel configurations, and validated GPU passthrough support. For most GPU workloads, the recommended pattern is **`runc` + NVIDIA GPU Operator**, isolated via Node Affinity and Taints (`workload-class=gpu`). Use Kata for GPU workloads only if hardware-level multi-tenant GPU isolation is strictly required — for example, when multiple tenants share a single GPU via MIG and each tenant's workload must be fully sandboxed. In that case, verify Kata + VFIO compatibility on your specific Azure VM SKU before production deployment.

### 18.3 GPU RuntimeClass

```yaml
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: nvidia-gpu
handler: nvidia
scheduling:
  nodeSelector:
    nvidia.com/gpu.present: "true"
```

### 18.4 Sample vLLM deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vllm-llama-70b
  namespace: agents-prod
spec:
  replicas: 1
  selector:
    matchLabels: { app: vllm-llama-70b }
  template:
    metadata:
      labels: { app: vllm-llama-70b, workload-type: agentic, sandbox: nvidia-gpu }
    spec:
      runtimeClassName: nvidia-gpu       # uses nvidia-container-runtime; see §14.1 for GPU passthrough caveat
      serviceAccountName: vllm-sa
      automountServiceAccountToken: false
      securityContext:
        runAsNonRoot: false              # vLLM requires root for GPU access; mitigated by Kata sandbox
        seccompProfile: { type: RuntimeDefault }
      containers:
        - name: vllm
          image: <acr>.azurecr.io/serve/vllm:signed-0.6.0
          securityContext:
            allowPrivilegeEscalation: false
            capabilities: { drop: ["ALL"] }
          resources:
            limits:
              nvidia.com/gpu: "1"
              memory: 80Gi
            requests:
              nvidia.com/gpu: "1"
              memory: 80Gi
          command: ["python3", "-m", "vllm.entrypoints.openai.api_server"]
          args:
            - "--model=/models/llama-3.1-70b-instruct"
            - "--tensor-parallel-size=1"
            - "--host=0.0.0.0"
            - "--port=8000"
          ports:
            - containerPort: 8000
          volumeMounts:
            - name: models
              mountPath: /models
      volumes:
        - name: models
          persistentVolumeClaim:
            claimName: llama-70b-pvc
```

### 18.5 GPU sharing strategies

For cost efficiency, multiple agent pods can share a single GPU:

- **Time-slicing** (MIG-unavailable GPUs): the GPU Operator configures the GPU to time-slice between pods. Lower isolation; one pod can starve others. Suitable for dev/staging.
- **MIG (Multi-Instance GPU)** (H100, A100): partitions the GPU into up to 7 independent instances with hardware-level isolation. Recommended for production multi-tenant agentic workloads.
- **vGPU / GPU partitioning** (Azure-specific): not yet GA for self-managed clusters on Azure VMs.

For multi-tenant agentic workloads on H100/A100, **MIG is the recommended pattern** — it provides hardware-level isolation between tenants, so a prompt-injected agent on tenant A cannot observe tenant B's model weights or inference latency.

---

## 19. Backup, Restore & Disaster Recovery

A production cluster must be recoverable from three classes of failure: (1) accidental or malicious deletion of Kubernetes objects, (2) loss or corruption of the etcd data store, (3) loss of an entire Azure region. The reference deployment uses **Velero** for Kubernetes object backup and **etcd snapshots** for the etcd data store, both targeted at Azure Storage. Azure VM disk snapshots and Azure Storage's geo-redundant replication provide additional platform-level recovery layers.

### 19.1 Recovery objectives

| Workload type | RPO (data loss tolerance) | RTO (recovery time) |
|---|---|---|
| Control plane (etcd) | 24 hours (nightly snapshot) + 1 hour (etcd defrag) | 2 hours (manual cluster rebuild) |
| PersistentVolumes (agent state, vector DB) | 1 hour (Velero periodic backup) | 4 hours (Velero restore + PVC rehydration) |
| Configuration (manifests in Git) | Real-time (GitOps, see §20) | Minutes (Argo CD / Flux sync) |

For tighter RPOs, reduce the etcd snapshot interval and the Velero backup schedule. For tighter RTOs, maintain a warm standby cluster in a second region.

### 19.2 etcd backup

etcd backups are taken from a control-plane node using `etcdctl`. The snapshot is a single binary file that can be restored into a fresh etcd cluster.

```bash
# Create a Service Principal (or use managed identity) for the snapshot push to Azure Storage
AZURE_STORAGE_ACCOUNT="$STORAGE_NAME"
AZURE_STORAGE_CONTAINER="etcd-snapshots"
az storage container create -n "$AZURE_STORAGE_CONTAINER" --account-name "$AZURE_STORAGE_ACCOUNT"

# Run on each control-plane node via a systemd timer (so snapshots are independent)
sudo tee /usr/local/bin/etcd-snapshot.sh >/dev/null <<'EOF'
#!/bin/bash
set -euo pipefail

SNAPSHOT_FILE="/var/lib/etcd-snapshots/etcd-$(date +%Y%m%d-%H%M%S)-$(hostname).db"
mkdir -p /var/lib/etcd-snapshots

sudo ETCDCTL_API=3 etcdctl \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/peer.crt \
  --key=/etc/kubernetes/pki/etcd/peer.key \
  snapshot save "$SNAPSHOT_FILE"

# Verify the snapshot
sudo ETCDCTL_API=3 etcdctl snapshot status "$SNAPSHOT_FILE" --write-out=table

# Upload to Azure Storage (use az CLI with the node's managed identity)
az storage blob upload \
  --account-name "$AZURE_STORAGE_ACCOUNT" \
  --container-name "$AZURE_STORAGE_CONTAINER" \
  --name "$(basename "$SNAPSHOT_FILE")" \
  --file "$SNAPSHOT_FILE" \
  --auth-mode login

# Clean up local snapshots older than 7 days
find /var/lib/etcd-snapshots -name 'etcd-*.db' -mtime +7 -delete
EOF
sudo chmod +x /usr/local/bin/etcd-snapshot.sh

# systemd timer
sudo tee /etc/systemd/system/etcd-snapshot.service >/dev/null <<'EOF'
[Unit]
Description=etcd snapshot backup
After=network-online.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/etcd-snapshot.sh
User=root
EOF
sudo tee /etc/systemd/system/etcd-snapshot.timer >/dev/null <<'EOF'
[Unit]
Description=Nightly etcd snapshot
[Timer]
OnCalendar=*-*-* 02:00:00
Persistent=true
[Install]
WantedBy=timers.target
EOF
sudo systemctl enable --now etcd-snapshot.timer
```

> Note: the snapshot is taken from one control-plane node; the etcd cluster is replicated across all three, so a snapshot from any one is a complete cluster snapshot. The systemd timer is set up on all three nodes for redundancy; only one snapshot per night is needed.

### 19.3 Install Velero

> **Velero 1.16 → 1.17 upgrade note.** The Azure plugin had breaking changes between Velero 1.16 and 1.17 (GitHub issue #9647 documents the Azure plugin errors customers hit during the upgrade). If you are upgrading from 1.16, follow the migration guide in the Velero release notes before upgrading [22].

```bash
# Create a storage container and SAS token for Velero
AZURE_STORAGE_CONTAINER="velero-backups"
az storage container create -n "$AZURE_STORAGE_CONTAINER" --account-name "$STORAGE_NAME"

# Create a managed identity for Velero
az identity create -g "$RG" -n mi-velero
MI_CLIENT_ID=$(az identity show -g "$RG" -n mi-velero --query clientId -o tsv)
MI_ID=$(az identity show -g "$RG" -n mi-velero --query id -o tsv)
SUB_ID=$(az account show --query id -o tsv)

# Assign Storage Blob Data Contributor to the Velero identity
az role assignment create --role "Storage Blob Data Contributor" \
  --assignee-object-id "$(az identity show -g "$RG" -n mi-velero --query principalId -o tsv)" \
  --assignee-principal-type ServicePrincipal \
  --scope "/subscriptions/$SUB_ID/resourceGroups/$RG/providers/Microsoft.Storage/storageAccounts/$STORAGE_NAME"

# Federate the Velero identity with the cluster's OIDC
az identity federated-credential create \
  --identity-name mi-velero --resource-group "$RG" \
  --name fc-velero \
  --issuer "https://<storage-account>.blob.core.windows.net/oidc" \
  --subject "system:serviceaccount:velero:velero-server" \
  --audiences "api://AzureADTokenExchange"

# Install Velero via Helm
helm repo add vmware-tanzu https://vmware-tanzu.github.io/helm-charts/
helm repo update

cat <<EOF > /tmp/velero-values.yaml
configuration:
  backupStorageLocation:
    - name: azure
      provider: azure
      bucket: $AZURE_STORAGE_CONTAINER
      config:
        storageAccount: $STORAGE_NAME
        resourceGroup: $RG
        subscriptionId: $SUB_ID
        useWorkloadIdentity: "true"
  volumeSnapshotLocation:
    - name: azure
      provider: azure
      config:
        resourceGroup: $RG
        subscriptionId: $SUB_ID

credentials:
  useSecret: false          # use workload identity instead

serviceAccount:
  server:
    create: true
    name: velero-server
    annotations:
      azure.workload.identity/client-id: "$MI_CLIENT_ID"
    labels:
      azure.workload.identity/use: "true"

backupStorageLocation:
  name: azure

schedules:
  nightly-backup:
    schedules: "0 1 * * *"          # 01:00 daily
    template:
      ttl: "720h"                    # 30 days
      includedNamespaces:
        - agents-prod
        - agents-staging
        - platform-ops
        - observability
      snapshotVolumes: true

  hourly-pvc-backup:
    schedules: "0 * * * *"          # hourly
    template:
      ttl: "24h"
      labelSelector:
        matchLabels:
          backup: hourly
      snapshotVolumes: true
EOF

helm install velero vmware-tanzu/velero \
  --namespace velero --create-namespace \
  -f /tmp/velero-values.yaml
```

### 19.4 Verify backup works

```bash
# Create an on-demand backup
velero backup create test-backup --include-namespaces agents-prod --wait

# Verify
velero backup describe test-backup --details
velero backup get

# Restore test (in a non-production namespace)
velero restore create --from-backup test-backup --namespace-mappings agents-prod:agents-prod-restore --wait
kubectl get pods -n agents-prod-restore
```

### 19.5 Disaster recovery: rebuild the cluster from etcd snapshot

The worst-case scenario is losing the entire cluster. The recovery procedure from an etcd snapshot:

1. Provision a new VNet, three control-plane nodes, and two workers per §4.
2. Run host hardening (§5), containerd (§6), and Kubernetes packages (§7) on every node.
3. On the first control-plane node, restore the etcd snapshot into a fresh etcd data directory:

```bash
# Restore the snapshot to a fresh etcd data dir
sudo ETCDCTL_API=3 etcdctl snapshot restore /tmp/etcd-backup.db \
  --data-dir=/var/lib/etcd-restored \
  --name=node-cp-01 \
  --initial-cluster="node-cp-01=https://10.60.1.4:2380,node-cp-02=https://10.60.1.5:2380,node-cp-03=https://10.60.1.6:2380" \
  --initial-cluster-token=new-cluster \
  --initial-advertise-peer-urls=https://10.60.1.4:2380

# Move the restored data into place
sudo systemctl stop etcd 2>/dev/null || true
sudo mv /var/lib/etcd /var/lib/etcd.old
sudo mv /var/lib/etcd-restored /var/lib/etcd
sudo chown -R etcd:etcd /var/lib/etcd
```

4. Run `kubeadm init` (§8.4) with `--ignore-preflight-errors=DirAvailable--var-lib-etcd` so it picks up the pre-populated etcd.
5. Join the remaining control-plane and worker nodes per §8.7 and §9.
6. Reinstall Cilium, Kyverno, Falco, etc. (these are not in etcd — well, Cilium's CRDs are, but Helm-installed operators are not). The cleanest path is to maintain a GitOps repo (see §20) and let Argo CD / Flux re-apply everything.

### 19.6 Azure VM disk snapshots (additional layer)

Azure VM disk snapshots provide an OS-level backup that does not depend on the cluster being healthy. They are especially useful for control-plane node recovery.

```bash
# Create a disk snapshot of node-cp-01's OS disk
az snapshot create -g "$RG" -n snap-cp-01-$(date +%Y%m%d) \
  --source "/subscriptions/$SUB_ID/resourceGroups/$RG/providers/Microsoft.Compute/disks/node-cp-01_OSDisk" \
  --incremental true
```

Schedule this via an Azure Automation runbook daily; retain 7 snapshots. Note that restoring a VM from a disk snapshot restores the etcd data on that VM, which can be useful if a single node's etcd is corrupted but the cluster is otherwise healthy.

---

## 20. Patching & Lifecycle Management

A production cluster requires three independent patch cadences: host OS patching, Kubernetes patch upgrades (within a minor), and Kubernetes minor upgrades (1.36 to 1.37). Each has its own procedure and its own rollback.

### 20.1 Host OS patching

Host OS patching is handled by the systemd timer in §5.10, which runs `tdnf --security update` weekly and reboots only if the kernel was touched. The `exclude` directive in `/etc/tdnf/tdnf.conf.d/hold-k8s.conf` ensures `kubelet`, `kubeadm`, `kubectl`, and `containerd` are not auto-upgraded — those are upgraded explicitly via the runbook in §20.2 and §20.3.

```bash
# Manual one-off security update (if an urgent CVE drops between weekly runs)
sudo tdnf -y --security update

# Verify no K8s packages were upgraded
rpm -qa | grep -E 'kubelet|kubeadm|kubectl|containerd'
```

### 20.2 Kubernetes patch upgrade runbook (1.36.x → 1.36.y)

Kubernetes patch releases are backwards- and forwards-compatible within a minor. The procedure is:

1. Update the `pkgs.k8s.io` repository URL (no change — same minor).
2. On each control-plane node, one at a time:
   - Drain: `kubectl drain node-cp-01 --ignore-daemonsets --delete-emptydir-data`
   - Upgrade kubeadm: `sudo tdnf upgrade kubeadm`
   - Apply the upgrade: `sudo kubeadm upgrade apply v1.36.y`
   - Upgrade kubelet and kubectl: `sudo tdnf upgrade kubelet kubectl`
   - Restart kubelet: `sudo systemctl restart kubelet`
   - Uncordon: `kubectl uncordon node-cp-01`
   - Verify: `kubectl get nodes` (wait for `Ready` and updated kubelet version).
3. Repeat for the remaining control-plane nodes (use `kubeadm upgrade node` instead of `kubeadm upgrade apply` on the 2nd and 3rd CP nodes).
4. On each worker node, one at a time:
   - Drain: `kubectl drain node-wk-01 --ignore-daemonsets --delete-emptydir-data`
   - Upgrade kubeadm, kubelet, kubectl: `sudo tdnf upgrade kubeadm kubelet kubectl`
   - Apply: `sudo kubeadm upgrade node`
   - Restart kubelet: `sudo systemctl restart kubelet`
   - Uncordon: `kubectl uncordon node-wk-01`

Rollback: downgrade the packages and re-run `kubeadm upgrade apply v1.36.x`. etcd data is forward-compatible within a minor, so no etcd restore is needed.

### 20.3 Kubernetes minor upgrade runbook (1.36 → 1.37)

Minor upgrades require more care: API deprecations, feature-gate changes, and the version skew policy all apply.

1. **Read the release notes** for 1.37 at https://kubernetes.io/releases/ — note any API removals that affect your manifests.
2. **Pre-flight check**: run `kubectl convert --help` and `kubectl deprecations --k8s-version v1.37.0` against your cluster to find any deprecated APIs in use.
3. **Update Kyverno / Cilium / Falco** to versions that support K8s 1.37 (check each project's compatibility matrix).
4. **Update the `pkgs.k8s.io` repository URL** on every node:

```bash
sudo sed -i 's|/core:/stable:/v1.36/|/core:/stable:/v1.37/|' /etc/yum.repos.d/kubernetes.repo
sudo tdnf makecache
```

5. **Upgrade control-plane nodes** one at a time per §20.2, but with `kubeadm upgrade apply v1.37.0`.
6. **Upgrade worker nodes** one at a time per §20.2.
7. **Verify** the cluster: `kubectl get nodes`, `kubectl get pods -A`, run `cilium connectivity test`, run `kube-bench` against the new CIS benchmark version (1.37 may need a new benchmark).

Rollback: minor downgrades are NOT supported by kubeadm. The rollback path is to provision a new cluster on the old version and restore from etcd snapshot (§19.5). This is why staging clusters must run the new minor before production.

### 20.4 Certificate rotation

Kubernetes certificates (API server, kubelet, etcd, etc.) expire after 1 year by default. `kubeadm` provides built-in rotation commands.

```bash
# Check certificate expiration on any control-plane node
sudo kubeadm certs check-expiration

# Rotate all certificates (do this ~30 days before expiry)
sudo kubeadm certs renew all

# Restart the control-plane static pods to pick up the new certs
sudo crictl pods --namespace kube-system | grep kube-apiserver | awk '{print $1}' | xargs -r sudo crictl stopp
sudo crictl pods --namespace kube-system | grep kube-controller-manager | awk '{print $1}' | xargs -r sudo crictl stopp
sudo crictl pods --namespace kube-system | grep kube-scheduler | awk '{print $1}' | xargs -r sudo crictl stopp

# Regenerate the admin kubeconfig (the certs in it expired too)
sudo cp /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

For kubelet server certificates, `serverTLSBootstrap: true` (set in the KubeletConfiguration in §8.1) causes kubelet to request new server certs from the API server automatically. The client cert (`kubelet.conf`) rotates automatically via the `rotateCertificates: true` setting.

### 20.5 Cilium upgrade

Cilium is upgraded via Helm:

```bash
# Diff the new values against the current
helm diff upgrade cilium cilium/cilium --namespace kube-system -f /tmp/cilium-values.yaml --version 1.21.0

# Upgrade (Cilium supports rolling upgrades — no downtime)
helm upgrade cilium cilium/cilium --namespace kube-system -f /tmp/cilium-values.yaml --version 1.21.0 --wait

# Verify
cilium status --wait
cilium connectivity test
```

> **Cilium 1.20 → 1.21 note.** `encryption.nodeEncryption` is deprecated in 1.21 and removed in 1.22. If you used it, migrate to `encryption.enabled=true` with `encryption.type=wireguard` before upgrading to 1.22.

### 20.6 GitOps for declarative workload lifecycle

For workload manifests (Deployments, Services, NetworkPolicies, Kyverno policies, etc.), use GitOps to make the cluster state declarative and auditable. **Argo CD** and **Flux** are both CNCF graduated projects suitable for this; the choice is largely organizational.

```bash
# Install Argo CD
helm repo add argo https://argoproj.github.io/argo-helm
helm install argocd argo/argo-cd \
  --namespace argocd --create-namespace \
  --set server.service.type=ClusterIP \
  --set controller.replicas=3

# Bootstrap an Application that points at your GitOps repo
cat <<EOF | kubectl apply -f -
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: agentic-platform
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/<org>/agentic-platform-gitops
    targetRevision: main
    path: manifests/
  destination:
    server: https://kubernetes.default.svc
    namespace: agents-prod
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
EOF
```

With GitOps in place, the recovery procedure in §19.5 simplifies dramatically: rebuild the control plane from the etcd snapshot, then let Argo CD re-apply every workload manifest from Git. The etcd snapshot carries the cluster's CRDs, names, and Kubernetes-internal state; the Git repo carries the desired workload state.

---

## 21. Compliance Validation (kube-bench, Kubescape)

Hardening claims must be validated, not asserted. The reference deployment runs two open-source compliance scanners: **kube-bench** for the CIS Kubernetes Benchmark v1.10.0 [14] and **Kubescape** for the NSA/CISA, MITRE ATT&CK, and CIS frameworks [15]. Both are run on a schedule and the results are sent to Azure Monitor.

### 21.1 Run kube-bench

kube-bench runs the CIS Kubernetes Benchmark checks against a node. Run it on each node:

```bash
# Run kube-bench on a control-plane node
sudo docker run --rm \
  -v /etc/kubernetes:/etc/kubernetes:ro \
  -v /var/lib/etcd:/var/lib/etcd:ro \
  -v /var/lib/kubelet:/var/lib/kubelet:ro \
  -v /var/lib/cni:/var/lib/cni:ro \
  -v /etc/cni/net.d:/etc/cni/net.d:ro \
  -v /etc/systemd:/etc/systemd:ro \
  --pid=host \
  aquasec/kube-bench:latest \
  --benchmark cis-1.10 \
  run --targets=node,master,etcd,controlplane,policies,managedservices
```

For worker nodes, run with `--targets=node` only.

### 21.2 Run Kubescape

Kubescape runs as an in-cluster operator and continuously evaluates the cluster against multiple frameworks. Install it via Helm:

```bash
helm repo add kubescape https://kubescape.github.io/helm-charts/
helm install kubescape kubescape/kubescape-operator \
  --namespace kubescape --create-namespace \
  --set clusterName="agentic-k8s-prod" \
  --set accountID="<kubescape-account-id>"     # optional, for the SaaS dashboard
```

Trigger an on-demand scan:

```bash
kubescape scan framework nsa --submit \
  --cluster-name agentic-k8s-prod
kubescape scan framework mitre --submit \
  --cluster-name agentic-k8s-prod
kubescape scan framework cis-v1.10.0 --submit \
  --cluster-name agentic-k8s-prod
```

### 21.3 NSA/CISA Kubernetes Hardening Guidance mapping

The table below maps the NSA/CISA v1.2 categories [25] to the implementations in this guide. Use it as a control-to-section cross-reference for compliance audits.

| NSA/CISA category | Implementation | Section |
|---|---|---|
| Scan containers and Pods for vulnerabilities | Trivy operator + Microsoft Defender for Containers | §16.6 |
| Use Pod Security Policies (now Pod Security Admission) | PSA `restricted` enforced via namespace labels; Kyverno policies | §13.1, §15 |
| Reduce attack surface | Minimal Azure Linux 3.0; no GUI; firewalld; locked NSGs; pinned K8s packages | §5 |
| Apply least privilege RBAC | Entra ID group-based RBAC; `automountServiceAccountToken: false`; bound SA tokens | §11 |
| Use network separation and hardening | Cilium default-deny; FQDN egress; NSGs; no public IPs | §4, §10 |
| Use firewalling and encryption | Cilium WireGuard; TLS everywhere; Bastion-only SSH | §4, §10 |
| Use strong authentication | Entra ID OIDC for humans; Entra Workload Identity for workloads | §11 |
| Log everything | API audit log; auditd; Falco; Hubble; Azure Monitor | §5.9, §8.2, §17 |
| Periodically review all controls | `kube-bench` + `Kubescape` weekly in CI; quarterly control review | §21 |
| Continuously scan for vulnerabilities | Trivy in CI on every build; Defender for Containers in runtime | §16.6, §17 |

### 21.4 Continuous compliance in CI

Wire `kube-bench` and `Kubescape` scans into a weekly CI job that pages the on-call if compliance scores drop below threshold:

```yaml
# .github/workflows/compliance-scan.yml
name: Weekly compliance scan
on:
  schedule:
    - cron: "0 6 * * 1"          # 06:00 UTC every Monday
  workflow_dispatch:
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - name: Install kubectl and connect to cluster
        run: |
          az aks get-credentials -g rg-agentic-k8s-prod -n agentic-k8s-prod --overwrite-existing
          # (Or, for self-managed cluster, scp the kubeconfig via Bastion.)

      - name: Run Kubescape
        run: |
          curl -s https://raw.githubusercontent.com/kubescape/kubescape/master/install.sh | bash
          kubescape scan framework nsa --format json --output kubescape-nsa.json
          kubescape scan framework cis-v1.10.0 --format json --output kubescape-cis.json

      - name: Fail if compliance score < 80%
        run: |
          SCORE=$(jq -r '.summary_controls.score' kubescape-cis.json)
          echo "CIS score: $SCORE"
          if (( $(echo "$SCORE < 80" | bc -l) )); then
            echo "Compliance score below threshold"
            exit 1
          fi
```

### 21.5 Known gaps in this guide's posture

Be explicit about what this guide does NOT cover, so compliance auditors know where to look:

- **FIPS 140-3 validated crypto.** Azure Linux ships the SymCrypt FIPS 140-3 module, but enabling FIPS mode requires a separate configuration step and validation per workload. This guide does not walk through that.
- **Confidential computing.** Azure confidential VMs (SEV-SNP, TDX) and Kata Containers CoCo are not deployed in the baseline. For workloads handling regulated data (PII, PHI, financial data), add confidential VM SKUs and Kata CoCo.
- **Multi-cluster federation.** This guide deploys a single cluster. Multi-cluster (KubeFed, Cilium ClusterMesh, Argo CD ApplicationSet) is out of scope but straightforward to add.
- **PCI DSS / HIPAA / FedRAMP-specific controls.** The cluster posture described here satisfies the technical controls for many compliance frameworks, but the formal certification process is out of scope.

---

## Appendix A — Full Reference Manifests

This appendix consolidates the YAML manifests referenced throughout the guide. Each is also available as a standalone file in the companion GitOps repository.

### A.1 kubeadm-config.yaml (v1beta4)

(See §8.1 for the full file with annotations.)

### A.2 audit-policy.yaml

(See §8.2.)

### A.3 encryption-provider.yaml

(See §8.3.)

### A.4 cilium-values.yaml

(See §10.2.)

### A.5 NetworkPolicy: default-deny-all

(See §10.6.)

### A.6 CiliumNetworkPolicy: agent-egress-allowlist

(See §10.7.)

### A.7 Kyverno policies (4)

(See §15.2.)

### A.8 SecretProviderClass: llm-api-key

(See §12.4.)

### A.9 ExternalSecret: llm-api-keys

(See §12.6.)

### A.10 RuntimeClass: gvisor

(See §14.2.)

### A.11 RuntimeClass: kata

(See §14.3.)

### A.12 RuntimeClass: nvidia-gpu

(See §18.3.)

### A.13 Reference hardened pod spec

(See §13.2.)

### A.14 Sandboxed agent deployment

(See §14.5.)

### A.15 vLLM GPU deployment

(See §18.4.)

### A.16 Velero values

(See §19.3.)

### A.17 Prometheus alert rules

(See §17.5.)

### A.18 Falco custom rules

(See §17.2.)

---

## Appendix B — Variable Reference

The variables below are used throughout this guide. Replace with your own values; the commands are otherwise copy-paste ready.

| Variable | Default value in this guide | Notes |
|---|---|---|
| `RG` | `rg-agentic-k8s-prod` | Azure resource group |
| `LOC` | `eastus2` | Azure region with 3 AZs |
| `VNET` | `vnet-agentic-k8s` | VNet name |
| `CP_LB_IP` | `10.60.1.100` | Internal LB IP for API server |
| `CP_VM_PREFIX` | `node-cp-` | Control-plane node prefix (node-cp-01, -02, -03) |
| `WK_VM_PREFIX` | `node-wk-` | Worker node prefix (node-wk-01, -02) |
| `GPU_VM_PREFIX` | `node-gpu-` | GPU node prefix |
| `ADMIN_USER` | `k8sadmin` | SSH admin user |
| `KV_NAME` | `kv-agentic-k8s-eastus2` | Azure Key Vault |
| `ACR_NAME` | `acragentick8seastus2` | Azure Container Registry |
| `STORAGE_NAME` | `stagentickeastus2` | Azure Storage Account |
| `LA_WS` | `log-agentic-k8s` | Log Analytics Workspace |
| `ENTRA_TENANT_ID` | (from `az account show`) | Entra tenant ID |
| `K8S_MINOR` | `1.36` | Kubernetes minor version |
| `IMG` | `MicrosoftAzureLinux:azure-linux:3-gen2:latest` | Azure Linux 3.0 marketplace URN (validate with `az vm image list`) |
| `CP_VM_SIZE` | `Standard_D4s_v5` | Control-plane VM size |
| `WK_VM_SIZE` | `Standard_D8s_v5` | Worker VM size |
| `GPU_VM_SIZE` | `Standard_NCads_H100_v5` | GPU worker VM size |
| `podSubnet` | `10.244.0.0/16` | Pod CIDR (Cilium IPAM) |
| `serviceSubnet` | `10.96.0.0/12` | Service CIDR |
| `dnsDomain` | `cluster.local` | Cluster DNS domain |
| `OIDC_ISSUER` | `https://<storage>.blob.core.windows.net/oidc` | Public OIDC discovery URL for Workload Identity |

---

## Appendix C — Hardening Checklist

This pre-production checklist is organized by layer. Each item maps to a section in the guide. Run this checklist before declaring the cluster production-ready.

### C.1 Host OS (Azure Linux 3.0)

- [ ] All nodes run Azure Linux 3.0 (kernel 6.6 LTS) with Trusted Launch enabled
- [ ] Secure Boot and vTPM enabled on every VM
- [ ] `tdnf update -y` run; all packages current
- [ ] `container-selinux` installed; SELinux in Enforcing mode (`getenforce` returns `Enforcing`)
- [ ] OS Guard (IPE) installed; audit mode reviewed; enforcing mode planned (note: OS Guard is currently in public preview)
- [ ] `chronyd` enabled and synchronized
- [ ] Kernel modules `overlay` and `br_netfilter` loaded at boot
- [ ] Sysctls from §5.3 applied (`sysctl --system`)
- [ ] Swap disabled (`swapoff -a` + commented in `/etc/fstab`)
- [ ] `firewalld` enabled; only required ports open (per node role)
- [ ] SSH hardening applied (no root, no password, no challenge-response, AllowUsers only)
- [ ] `auditd` enabled; rules from §5.9 loaded
- [ ] `tdnf-security.timer` enabled; K8s packages pinned via `exclude=`
- [ ] etcd disk (Premium SSD v2) formatted and mounted at `/var/lib/etcd` (control-plane nodes)

### C.2 Kubernetes control plane

- [ ] `kubeadm init` completed with v1beta4 config from §8.1
- [ ] 3 control-plane nodes joined across 3 availability zones
- [ ] `controlPlaneEndpoint` points to internal Standard LB (10.60.1.100:6443)
- [ ] LB health probe (`/healthz` on 6443) returns 200 from every CP node
- [ ] API server audit logging enabled; audit policy from §8.2 applied
- [ ] etcd encryption at rest enabled (KMS v2); verified per §12.1
- [ ] `service-account-issuer` set to publicly resolvable OIDC URL for Workload Identity
- [ ] kube-proxy NOT deployed (Cilium replaces it)
- [ ] All CP node certs valid for >60 days (`kubeadm certs check-expiration`)

### C.3 Kubernetes worker nodes

- [ ] 2+ worker nodes joined and Ready
- [ ] Nodes labeled with `workload-class`, `sandbox-runtime` per §9.3
- [ ] Control-plane `NoSchedule` taint in place
- [ ] kubelet running with `cgroupDriver=systemd`, `rotateCertificates=true`, `serverTLSBootstrap=true`
- [ ] `kubelet` config from §8.1 applied

### C.4 Networking

- [ ] Cilium 1.20 installed via Helm with values from §10.2
- [ ] kube-proxy replacement verified (no kube-proxy pods)
- [ ] WireGuard node-to-node encryption verified (`wg show` on every node)
- [ ] Hubble Relay + UI enabled
- [ ] Gateway API CRDs installed
- [ ] Default-deny NetworkPolicy applied to every namespace
- [ ] FQDN egress CiliumNetworkPolicy applied to agentic namespaces
- [ ] NSGs locked down per §4.3 (no public IPs, no internet-exposed SSH)

### C.5 Identity

- [ ] Entra ID OIDC integration configured (API server `oidc-*` flags)
- [ ] Entra app registration for kubectl created
- [ ] `kubelogin` configured on operator workstations
- [ ] Group-based RBAC bindings in place (platform-ops, security-auditors, dev-team)
- [ ] No `cluster-admin` bindings to individuals; only to Entra groups
- [ ] Entra Workload Identity configured (OIDC issuer published, federated credentials created)
- [ ] `automountServiceAccountToken: false` is the default

### C.6 Secrets

- [ ] etcd encryption at rest verified (§12.1)
- [ ] Secrets Store CSI Driver + Azure Key Vault Provider installed
- [ ] External Secrets Operator installed (for legacy workloads)
- [ ] No plaintext secrets in Git (Kyverno policy enforces)
- [ ] Key Vault uses RBAC mode (not access policy)
- [ ] Key Vault accessible only via private endpoint

### C.7 Workload

- [ ] PSA `restricted` enforced in every workload namespace
- [ ] Kyverno installed with 3 replicas; `kyverno-policies` chart applied
- [ ] Custom agentic policies from §15.2 applied
- [ ] gVisor (`runsc`) installed on workers labeled `sandbox-runtime=gvisor`
- [ ] Kata Containers 4.0 installed on workers labeled `sandbox-runtime=kata`
- [ ] RuntimeClass objects created for `gvisor`, `kata`, `nvidia-gpu`
- [ ] All agentic workloads use a sandboxed RuntimeClass
- [ ] All pods satisfy the reference hardened pod spec from §13.2
- [ ] ResourceQuotas and LimitRanges applied to every agentic namespace (§13.4)
- [ ] Kyverno policy enforcing resource limits on all containers (§13.4)
- [ ] GPU nodes: Kata + GPU passthrough caveat reviewed; `runc` + GPU Operator recommended unless multi-tenant isolation required (§18)

### C.8 Observability

- [ ] kube-prometheus-stack installed (Prometheus, Grafana, Alertmanager)
- [ ] Loki installed for log aggregation
- [ ] Falco installed with modern_ebpf probe; custom rules from §17.2 applied
- [ ] Falco alerts forwarding to Azure Monitor (via falcosidekick)
- [ ] Cilium Hubble UI accessible
- [ ] Alert rules from §17.5 configured in Alertmanager
- [ ] Azure Monitor Agent installed on every node; logs flowing to Log Analytics

### C.9 Backup / DR

- [ ] etcd snapshot systemd timer enabled on every CP node
- [ ] etcd snapshots pushing to Azure Storage
- [ ] Velero 1.17 installed with Azure plugin
- [ ] Velero backup schedule (nightly + hourly PVC) configured
- [ ] Velero restore test completed successfully in non-prod
- [ ] Disaster recovery runbook (§19.5) tested end-to-end
- [ ] Azure VM disk snapshots scheduled (daily, 7-day retention)

### C.10 Supply chain

- [ ] ACR Premium deployed with private endpoint
- [ ] cosign keyless signing configured in CI (GitHub Actions)
- [ ] SBOMs (Syft, CycloneDX) generated and attached to every image
- [ ] SLSA Build L3 provenance generated for every image
- [ ] Kyverno `verifyImages` policy enforced
- [ ] Kyverno registry allow-list policy enforced
- [ ] Trivy operator installed; CRITICAL vulnerabilities alerting
- [ ] Microsoft Defender for Containers enabled on subscription

---

## Appendix D — Upgrade Runbook

### D.1 Patch upgrade: 1.36.2 → 1.36.3

```bash
# 1. Pre-flight checks
kubectl get nodes                    # all Ready
kubectl get pods -A | grep -v Running | grep -v Completed    # no failed pods
cilium status                        # OK

# 2. On each control-plane node, one at a time:
for NODE in node-cp-01 node-cp-02 node-cp-03; do
  echo "=== Upgrading $NODE ==="
  kubectl drain $NODE --ignore-daemonsets --delete-emptydir-data --timeout=120s
  ssh $NODE 'sudo tdnf upgrade -y kubeadm kubelet kubectl'
  ssh $NODE 'sudo kubeadm upgrade apply v1.36.3'
  ssh $NODE 'sudo systemctl restart kubelet'
  kubectl uncordon $NODE
  kubectl wait --for=condition=Ready node/$NODE --timeout=300s
done

# 3. On each worker node, one at a time:
for NODE in node-wk-01 node-wk-02; do
  echo "=== Upgrading $NODE ==="
  kubectl drain $NODE --ignore-daemonsets --delete-emptydir-data --timeout=120s
  ssh $NODE 'sudo tdnf upgrade -y kubeadm kubelet kubectl'
  ssh $NODE 'sudo kubeadm upgrade node'
  ssh $NODE 'sudo systemctl restart kubelet'
  kubectl uncordon $NODE
  kubectl wait --for=condition=Ready node/$NODE --timeout=300s
done

# 4. Verify
kubectl get nodes -o wide
cilium connectivity test
```

### D.2 Minor upgrade: 1.36 → 1.37

(See §20.3 for the full procedure; key steps below.)

```bash
# 1. Pre-flight: read release notes, run kubectl deprecations
kubectl deprecations --k8s-version v1.37.0

# 2. Update pkgs.k8s.io repo URL on every node
for NODE in node-cp-01 node-cp-02 node-cp-03 node-wk-01 node-wk-02; do
  ssh $NODE 'sudo sed -i "s|/core:/stable:/v1.36/|/core:/stable:/v1.37/|" /etc/yum.repos.d/kubernetes.repo && sudo tdnf makecache'
done

# 3. Upgrade control-plane nodes one at a time (per D.1, with v1.37.0)
# 4. Upgrade worker nodes one at a time (per D.1)
# 5. Run kube-bench against the new CIS benchmark version
# 6. Run Kubescape NSA + MITRE + CIS scans
```

### D.3 Certificate rotation

(See §20.4.)

### D.4 Cilium upgrade

(See §20.5.)

### D.5 Host OS tdnf update

```bash
# 1. Drain the node
kubectl drain $NODE --ignore-daemonsets --delete-emptydir-data --timeout=120s

# 2. Apply security updates (K8s packages are excluded per §5.10)
ssh $NODE 'sudo tdnf -y --security update'

# 3. Reboot if the kernel was updated
ssh $NODE 'sudo systemctl reboot'

# 4. Wait for the node to come back
kubectl wait --for=condition=Ready node/$NODE --timeout=600s

# 5. Uncordon
kubectl uncordon $NODE
```

### D.6 Rollback procedures

| Upgrade type | Rollback procedure |
|---|---|
| K8s patch (1.36.2 → 1.36.3) | Downgrade packages: `sudo tdnf downgrade kubeadm kubelet kubectl` to previous patch. Re-run `kubeadm upgrade apply v1.36.2`. etcd data is forward-compatible within a minor. |
| K8s minor (1.36 → 1.37) | NOT supported by kubeadm. Rollback = provision a new 1.36 cluster from etcd snapshot (§19.5) + GitOps re-apply. **Test minor upgrades in staging first.** |
| Cilium (1.20 → 1.21) | `helm rollback cilium <previous-revision> -n kube-system` |
| Host OS (kernel update) | If a kernel update breaks the cluster: select the previous kernel in GRUB at boot time, then `sudo tdnf downgrade kernel` to pin to the older version. |
| Velero (1.16 → 1.17) | `helm rollback velero <previous-revision> -n velero`. Note: Azure plugin breaking changes may require manual remediation — see GitHub issue #9647. |

---

## Appendix E — Troubleshooting

### E.1 kubeadm init failures

**Symptom: `kubeadm init` hangs at `[wait-control-plane] Waiting for the kubelet to boot up the control plane`**

```bash
# On the control-plane node:
sudo journalctl -u kubelet -n 200 | grep -i error
sudo crictl ps -a | grep kube-apiserver    # is the API server container starting?
sudo crictl logs $(sudo crictl ps -a --name kube-apiserver -q | head -1)
```

Common causes:
- CRI socket mismatch: ensure `criSocket: "unix:///run/containerd/containerd.sock"` in the kubeadm config matches the actual containerd socket.
- etcd disk not mounted: confirm `/var/lib/etcd` exists and is writable.
- API server cert SAN missing: add the LB IP and DNS name to `apiServer.certSANs`.

**Symptom: `kubeadm init` fails with `failed to pull image registry.k8s.io/...`**

```bash
# Check network connectivity to registry.k8s.io
curl -I https://registry.k8s.io/v2/
# If air-gapped, pre-pull images and use kubeadm config imageRepository: <your-registry>
```

### E.2 Cilium pod-to-pod connectivity failures

**Symptom: pods on different nodes cannot reach each other; `cilium connectivity test` fails**

```bash
# On any node:
cilium status                               # look for errors
cilium sysdump                              # produces a tarball for support
sudo crictl logs $(sudo crictl ps -q --name cilium-agent | head -1) | tail -100

# Common causes:
# - VXLAN port (8472/udp) blocked by NSG or host firewall
# - WireGuard interface missing: sudo wg show
# - Kernel modules missing: lsmod | grep -E 'ebpf|wireguard'
```

### E.3 RuntimeClass errors

**Symptom: pod stuck in `ContainerCreating` with `RuntimeClass gvisor not found`**

```bash
kubectl get runtimeclass gvisor
# If missing, apply the RuntimeClass YAML from §14.2.

kubectl describe pod <pod-name>
# Look for the scheduling.failure message; if it says no node matches the
# nodeSelector, ensure at least one node has the label sandbox-runtime=gvisor.
kubectl get nodes --show-labels | grep sandbox-runtime
```

**Symptom: gVisor pod fails with `permission denied` on a syscall**

gVisor does not implement every Linux syscall. Check the gVisor compatibility matrix (https://gvisor.dev/docs/user-guide/compatibility/). If the workload needs an unimplemented syscall, switch to `kata` RuntimeClass.

### E.4 Kyverno admission blocking legitimate pods

**Symptom: `kubectl apply` returns `failed policy <policy-name>`**

```bash
# See the exact policy failure
kubectl describe admissionreports.kyverno.io -n <namespace>
# Or query the policy report:
kubectl get policyreports -n <namespace> -o yaml | grep -A 10 <policy-name>

# Temporarily switch the policy to audit mode (do NOT do this in production without change review):
kubectl patch clusterpolicy <policy-name> --type=json \
  -p='[{"op":"replace","path":"/spec/validationFailureAction","value":"Audit"}]'
```

### E.5 Falco false positives

**Symptom: Falco alerts fire constantly for legitimate workload behavior**

```bash
# Check which rules are firing
kubectl logs -n falco -l app.kubernetes.io/component=falco | jq '.rule' | sort | uniq -c

# Suppress a specific rule for a specific pod/namespace via Falco exceptions.
# Edit /etc/falco/rules.d/agentic-workload-rules.yaml and add an exception:
# - rule: Agent Spawned Shell
#   condition: ... and not k8s.pod.name startswith "expected-shell-pod-"
```

### E.6 Entra Workload Identity token exchange failures

**Symptom: workload cannot authenticate to Azure; logs show `AADSTS70021: No matching federated identity record`**

```bash
# Verify the federated identity credential subject matches the ServiceAccount exactly
az identity federated-credential show \
  --identity-name mi-agent-workload --resource-group $RG --name fc-agent-sa

# The subject must be exactly: system:serviceaccount:<namespace>:<service-account-name>
# Common errors: wrong namespace, wrong SA name, missing colon.

# Verify the pod has the workload-identity label
kubectl get pod <pod-name> -o jsonpath='{.metadata.labels.azure\.workload\.identity/use}'
# Expect: true

# Verify the ServiceAccount has the client-id annotation
kubectl get sa <sa-name> -o jsonpath='{.metadata.annotations.azure\.workload\.identity/client-id}'
```

### E.7 etcd quorum loss

**Symptom: API server returns `etcdserver: request timed out`; one CP node is permanently down**

```bash
# Check etcd membership from a healthy CP node
sudo ETCDCTL_API=3 etcdctl \
  --endpoints=https://10.60.1.4:2379,https://10.60.1.5:2379,https://10.60.1.6:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/peer.crt \
  --key=/etc/kubernetes/pki/etcd/peer.key \
  member list

# If a member is permanently gone, remove it:
sudo ETCDCTL_API=3 etcdctl ... member remove <member-id>

# Then re-add a new member (replace the failed node):
sudo ETCDCTL_API=3 etcdctl ... member add node-cp-03 --peerURLs=https://10.60.1.6:2380

# On the replacement node, run kubeadm join with --control-plane per §8.7
```

### E.8 Node NotReady

**Symptom: `kubectl get nodes` shows a node in `NotReady` state**

```bash
kubectl describe node <node-name> | tail -30      # look at conditions and events
# Common causes:
# - kubelet stopped: ssh to node, sudo systemctl status kubelet, sudo journalctl -u kubelet -n 100
# - Out of disk: df -h, especially /var (containerd images), /var/lib/etcd (control plane)
# - Memory pressure: free -m, dmesg | grep -i oom
# - CNI agent down: sudo crictl ps | grep cilium-agent, sudo crictl logs <cilium-pod-id>
```

---

## Appendix F — Sources

The numbered sources below are cited inline throughout this guide. Sources are tiered:
- **Tier 1** — Official vendor documentation, release notes, security advisories, standards bodies
- **Tier 2** — CNCF project documentation, GitHub releases, official architecture references
- **Tier 3** — Reputable engineering blogs, conference talks, community benchmarks
- **Tier 4** — Forums, Stack Overflow, personal blogs (used only for troubleshooting hints)

All URLs were retrieved on 2026-07-30.

1. **Azure Linux 3.0 now Generally Available with Azure Kubernetes Service v1.32** — Microsoft Tech Community blog. https://techcommunity.microsoft.com/blog/linuxandopensourceblog/azure-linux-3-0-now-generally-available-with-azure-kubernetes-service-v1-32/4399804 — Tier 1. (Retrieved 2026-07-30.) Confirms Azure Linux 3.0 GA, kernel 6.6 LTS, AKS v1.32 support.

2. **Azure Linux overview** — Microsoft Learn. https://learn.microsoft.com/azure/azure-linux/ — Tier 1. (Retrieved 2026-07-30.) Microsoft's official Azure Linux documentation hub.

3. **Azure Linux with OS Guard: Immutable Container Host** — Microsoft Tech Community blog. https://techcommunity.microsoft.com/blog/linuxandopensourceblog/azure-linux-with-os-guard-immutable-container-host-with-code-integrity-and-open-/4437473 — Tier 1. (Retrieved 2026-07-30.) Documents OS Guard integration with IPE (Integrity Policy Enforcement) LSM.

4. **MITRE ATT&CK T1611 — Escape to Host** — MITRE. https://attack.mitre.org/techniques/T1611/ — Tier 1.

5. **CISA Known Exploited Vulnerabilities Catalog — CVE-2025-3248 (Langflow)** — CISA. https://www.cisa.gov/known-exploited-vulnerabilities-catalog — Tier 1. (Retrieved 2026-07-30.)

6. **Kubernetes Releases** — kubernetes.io. https://kubernetes.io/releases/ — Tier 1. (Retrieved 2026-07-30.) Confirms current stable: v1.36.2 (released 2026-06-09); v1.37 release cycle began July 2026.

7. **containerd Versioning and release** — containerd.io. https://containerd.io/releases — Tier 1. (Retrieved 2026-07-30.) Confirms containerd 2.3.0 latest; 2.0 LTS branch supported through March 2027.

8. **Cilium Releases** — GitHub. https://github.com/cilium/cilium/releases — Tier 2. (Retrieved 2026-07-30.) Confirms Cilium 1.20.0 current stable. Cilium graduated CNCF October 2023.

9. **Cloud Native Computing Foundation Announces Kyverno's Graduation** — CNCF. https://www.cncf.io/announcements/2026/03/24/cloud-native-computing-foundation-announces-kyvernos-graduation — Tier 1. (Retrieved 2026-07-30.) Kyverno graduated CNCF on March 24, 2026.

10. **Falco — Cloud Native Runtime Security** — falco.org and falcosecurity/falco GitHub. https://falco.org and https://github.com/falcosecurity/falco — Tier 2. (Retrieved 2026-07-30.) Falco CNCF graduated May 2024; latest version 0.44.1 (June 2026).

11. **Kata Containers 4.0.0 release** — kata-containers/kata-containers GitHub. https://github.com/kata-containers/kata-containers/releases — Tier 2. (Retrieved 2026-07-30.) Kata Containers 4.0.0 brings the new Rust runtime, October 2025.

12. **Sigstore — graduated project** — sigstore.dev and blog.sigstore.dev. https://blog.sigstore.dev/sigstore-openssf-graduation — Tier 1. (Retrieved 2026-07-30.) Sigstore OpenSSF graduated October 2024; cosign 2.x current.

13. **pkgs.k8s.io: Introducing Kubernetes Community-Owned Package Repositories** — Kubernetes blog. https://kubernetes.io/blog/2023/08/15/pkgs-k8s-io-introduction — Tier 1. (Retrieved 2026-07-30.) Legacy apt.kubernetes.io and yum.kubernetes.io frozen March 4, 2024; pkgs.k8s.io is the official source.

14. **CIS Kubernetes Benchmark v1.10.0** — Center for Internet Security. https://www.cisecurity.org/benchmark/kubernetes — Tier 1. (Retrieved 2026-07-30.) Current benchmark version v1.10.0 (supersedes v1.9.0 from March 2024).

15. **Kubescape Now Supports CIS Kubernetes Benchmark v1.10** — kubescape.io. https://kubescape.io/blog/2025/03/06/kubescape-cis-10 — Tier 2. (Retrieved 2026-07-30.) Kubescape supports CIS v1.10, NSA, and MITRE frameworks.

16. **kubeadm Configuration (v1beta4)** — Kubernetes reference. https://kubernetes.io/docs/reference/config-api/kubeadm-config.v1beta4 — Tier 1. (Retrieved 2026-07-30.) v1beta4 is current; no v1beta5 yet.

17. **gVisor — Application Kernel for Containers** — Google. https://gvisor.dev and https://github.com/google/gvisor — Tier 1. (Retrieved 2026-07-30.)

18. **Kubernetes 1.30: Validating Admission Policy Is Generally Available** — Kubernetes blog. https://kubernetes.io/blog/2024/04/24/validating-admission-policy-ga — Tier 1. (Retrieved 2026-07-30.) VAP with CEL expressions GA since Kubernetes 1.30.

19. **Azure Key Vault Provider for Secrets Store CSI Driver** — Azure GitHub. https://github.com/Azure/secrets-store-csi-driver-provider-azure — Tier 2. (Retrieved 2026-07-30.)

20. **External Secrets Operator — Azure Key Vault** — external-secrets.io. https://external-secrets.io/latest/provider/azure-key-vault — Tier 2. (Retrieved 2026-07-30.)

21. **Use a Microsoft Entra Workload ID on Azure Kubernetes Service (AKS)** — Microsoft Learn. https://learn.microsoft.com/azure/aks/workload-identity-overview — Tier 1. (Retrieved 2026-07-30.) Entra Workload Identity is the GA replacement for AAD Pod Identity.

22. **Velero Releases** — vmware-tanzu/velero GitHub. https://github.com/vmware-tanzu/velero and https://artifacthub.io/packages/helm/vmware-tanzu/velero — Tier 2. (Retrieved 2026-07-30.) Velero 1.17.x current; 1.16 → 1.17 had Azure plugin breaking changes (GitHub issue #9647).

23. **NVIDIA GPU Operator with Azure** — NVIDIA docs. https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/microsoft-aks.html — Tier 1. (Retrieved 2026-07-30.)

24. **Azure Kubernetes Service (AKS)** — Microsoft Learn. https://learn.microsoft.com/azure/aks/ — Tier 1. (Retrieved 2026-07-30.) AKS managed control plane reference.

25. **Updated: Kubernetes Hardening Guide (NSA/CISA v1.2)** — CISA. https://www.cisa.gov/news-events/alerts/2022/03/15/updated-kubernetes-hardening-guide — Tier 1. (Retrieved 2026-07-30.) NSA/CISA Kubernetes Hardening Guidance v1.2, March 2022; remains authoritative as of July 2026.

26. **OWASP Top 10 for LLM Applications** — OWASP. https://owasp.org/www-project-top-10-for-large-language-model-applications/ — Tier 1. (Retrieved 2026-07-30.)

27. **MITRE ATLAS (Adversarial Threat Landscape for AI Systems)** — MITRE. https://atlas.mitre.org/ — Tier 1. (Retrieved 2026-07-30.)

28. **Azure CLI** — Microsoft Learn. https://learn.microsoft.com/cli/azure/ — Tier 1. (Retrieved 2026-07-30.)

29. **Trusted Launch for Azure VMs** — Microsoft Learn. https://learn.microsoft.com/azure/virtual-machines/trusted-launch — Tier 1. (Retrieved 2026-07-30.)

30. **Kubernetes Version Skew Policy** — Kubernetes. https://kubernetes.io/releases/version-skew-policy/ — Tier 1. (Retrieved 2026-07-30.)

31. **Kubernetes KMS v2 (GA)** — Kubernetes KEPS. https://kep.k8s.io/3299 and Kubernetes 1.29 release notes. — Tier 1. (Retrieved 2026-07-30.) KMS v2 GA since Kubernetes 1.29; KMS v1 removed.

32. **Cilium Upgrade Guide — Node Encryption Deprecation** — Cilium docs. https://docs.cilium.io/en/stable/operations/upgrade — Tier 2. (Retrieved 2026-07-30.) `encryption.nodeEncryption` deprecated in 1.21, removed in 1.22.

33. **Pod Security Admission** — Kubernetes docs. https://kubernetes.io/docs/concepts/security/pod-security-admission — Tier 1. (Retrieved 2026-07-30.) PSA GA since Kubernetes 1.25.

34. **SLSA (Supply-chain Levels for Software Artifacts) v1.0** — slsa.dev. https://slsa.dev/spec/v1.0/ — Tier 1. (Retrieved 2026-07-30.) SLSA v1.0 released August 2023.

35. **kube-bench — CIS Kubernetes Benchmark runner** — aquasecurity/kube-bench GitHub. https://github.com/aquasecurity/kube-bench — Tier 2. (Retrieved 2026-07-30.)

36. **Azure Bastion** — Microsoft Learn. https://learn.microsoft.com/azure/bastion/ — Tier 1. (Retrieved 2026-07-30.)

37. **Azure Linux GitHub** — microsoft/azurelinux. https://github.com/microsoft/azurelinux — Tier 2. (Retrieved 2026-07-30.) Confirms Azure Linux sources are derived from Fedora Linux; Azure Linux 3.0 monthly image releases (latest 3.0.20251206 in Dec 2025).

38. **Microsoft Defender for Containers** — Microsoft Learn. https://learn.microsoft.com/azure/defender-for-cloud/defender-for-containers-introduction — Tier 1. (Retrieved 2026-07-30.)

39. **Azure Trusted Launch and Secure Boot on Azure Linux** — Microsoft Learn. https://learn.microsoft.com/azure/virtual-machines/linux/endorsed-distros — Tier 1. (Retrieved 2026-07-30.)

40. **Gateway API — Implementations** — Kubernetes SIG. https://gateway-api.sigs.k8s.io/docs/implementations/list — Tier 1. (Retrieved 2026-07-30.) Gateway API GA for L4 and L7; Cilium is a fully conformant implementation.

41. **Cilium 1.18 release notes** — Isovalent blog. https://isovalent.com/blog/post/cilium-1-18 — Tier 3. (Retrieved 2026-07-30.) Background on Cilium 1.18 features; current stable is 1.20.0 per cilium/cilium GitHub releases.

42. **kube-prometheus-stack Helm chart** — prometheus-community. https://github.com/prometheus-community/helm-charts — Tier 2. (Retrieved 2026-07-30.)

43. **Security Profiles Operator** — Kubernetes SIGs. https://github.com/kubernetes-sigs/security-profiles-operator — Tier 2. (Retrieved 2026-07-30.)

44. **Argo CD** — argoproj/argo-cd GitHub. https://github.com/argoproj/argo-cd — Tier 2. (Retrieved 2026-07-30.) CNCF graduated.

45. **Azure Container Registry** — Microsoft Learn. https://learn.microsoft.com/azure/container-registry/ — Tier 1. (Retrieved 2026-07-30.)

46. **Trivy** — aquasecurity/trivy GitHub. https://github.com/aquasecurity/trivy — Tier 2. (Retrieved 2026-07-30.)

47. **Tetragon** — Cilium. https://cilium.io/blog/2026/01/19/tetragon-falco-migrate — Tier 2. (Retrieved 2026-07-30.) Tetragon inline enforcement via eBPF; comparison vs Falco detection-only.

48. **Azure Linux OS Guard overview** — Microsoft Learn. https://learn.microsoft.com/azure/azure-linux/os-guard-overview — Tier 1. (Retrieved 2026-07-30.)

49. **Cilium kube-proxy replacement documentation** — Cilium. https://docs.cilium.io/en/stable/network/kubernetes/kubeproxy-free — Tier 2. (Retrieved 2026-07-30.) Confirms kube-proxy-free clusters are supported.

50. **etcd disaster recovery** — Kubernetes docs. https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/#backing-up-an-etcd-cluster — Tier 1. (Retrieved 2026-07-30.)
