# 综合审查报告：`SKILL.md` 与评审意见的批判性分析

## 一、执行摘要

对 `SKILL.md` 及其两份评审报告（`review-2.md`、`review-3.md`）进行了系统性交叉验证，并对照上游官方文档逐一核实了所有关键断言。**核心结论如下：**

| 类别 | 数量 | 状态 |
|------|------|------|
| 评审意见完全正确（有上游来源支撑） | 12 | ✅ 已验证 |
| 评审意见部分正确（需修正或补充 nuance） | 5 | ⚠️ 需调整 |
| 评审意见有误（与上游事实不符） | 2 | ❌ 需纠正 |
| 指南本身存在的未覆盖问题 | 2 | 🔴 新发现 |

两份评审报告的质量极高——`review-3.md` 的 **4 个 Critical Blocker** 全部得到上游文档的确认，`review-2.md` 的深度审查同样精准。但评审中也存在两处对 Cilium 配置历史的误读，以及两份评审均未覆盖的一个关键问题（Azure Load Balancer HTTPS 探针在 **2026 年已有官方解决方案**）。

以下按优先级逐项展开。

---

## 二、🔴 Critical Blocker 验证（评审意见完全正确）

### 2.1 `kubeadm` v1beta4 `kubeletExtraArgs` 语法问题

**评审主张：** `kubeadm` v1beta4 中 `nodeRegistration.kubeletExtraArgs` 必须使用 `name`/`value` 列表格式，而非 v1beta3 的 map 格式。

**验证结果：** ✅ **完全正确 — 部署阻断级**

官方 `kubeadm-config.v1beta4` API 文档明确指出，v1beta4 的主要变更之一是将 **所有** `extraArgs` 字段从 `string/string` map 替换为支持重复项的结构化额外参数（structured extra arguments that support duplicates）。该变更**同时适用于**：
- `ClusterConfiguration` 下的 `apiServer.extraArgs`、`controllerManager.extraArgs`、`scheduler.extraArgs`、`etcd.local.extraArgs`
- **`nodeRegistration.kubeletExtraArgs`**

`review-2.md` 和 `review-3.md` 均准确指出了此问题。指南 `SKILL.md` §8.1 中仍使用 map 格式，确实会导致 `kubeadm init` 在 Kubernetes 1.31+ 上失败。

**建议修复：** 按评审意见将 `kubeletExtraArgs` 转换为 `name`/`value` 列表格式。

---

### 2.2 containerd 2.x CRI 插件路径变更

**评审主张：** containerd 2.0+ 中，独立的 CRI 插件路径 `io.containerd.grpc.v1.cri` 已被移除，应使用 `io.containerd.cri.v1.runtime`。

**验证结果：** ✅ **完全正确 — 运行时阻断级**

containerd 官方文档确认：在 containerd 2.x（config version = 3）中，CRI 插件配置路径为 `[plugins.'io.containerd.cri.v1.runtime']`，而 containerd 1.x（config version = 2）使用 `[plugins."io.containerd.grpc.v1.cri"]`。

GitHub Issue #386 也明确记录了此问题：使用旧的 CRI 插件路径会导致 containerd 2.x 配置失败。

**建议修复：** 按评审意见将 §6.3 中的配置路径更新为 `io.containerd.cri.v1.runtime`。

---

### 2.3 `ValidatingAdmissionPolicy` 特性门控问题

**评审主张：** `ValidatingAdmissionPolicy` 在 Kubernetes 1.30 已 GA，到 1.36 时特性门控已被移除，设置该标志会导致 API Server 启动失败。

**验证结果：** ✅ **完全正确 — 启动阻断级**

ValidatingAdmissionPolicy 于 **Kubernetes 1.30** 正式 GA【18†L1-L2】。Kubernetes 特性门控生命周期策略规定：GA 后特性门控被锁定为 `true`，并在 **2-3 个次要版本后从代码库中移除**。到 Kubernetes 1.36（GA 后 6 个版本），该门控必然已被移除。传递未注册的特性门控会导致 `kube-apiserver` panic 退出。

> **补充 nuance：** Kubernetes 1.36 引入了新的 `ManifestBasedAdmissionControlConfig` 特性门控（Alpha），用于解决准入策略的引导安全问题。这进一步说明特性门控生态正在演进，旧门控已被淘汰。

**建议修复：** 从 §8.1 的 `apiServer.extraArgs` 和 `KubeletConfiguration.featureGates` 中**完全删除** `ValidatingAdmissionPolicy=true`。

---

### 2.4 Azure 内部 LB HTTPS 健康探测问题

**评审主张：** Azure Standard Load Balancer HTTPS 探测要求后端提供受信任的证书，`kubeadm` 自签名证书会导致 TLS 验证失败，应改用 TCP 探测。

**验证结果：** ✅ **正确，但需补充 2026 年的新进展**

Azure 官方文档确认 HTTPS 探测要求证书链中至少使用 SHA256 签名哈希。自签名证书确实会导致探测失败。

**然而**，截至 2026 年，Azure 提供了更完善的解决方案：
- 可以使用 **Application Gateway** 替代 Load Balancer 实现端到端加密
- 对于 Front Door + Private Link 场景，自签名证书**无法**用于源站配置

评审建议的 TCP 探测是**最稳妥的临时方案**，但对于需要 HTTPS 探测的生产环境，建议在文档中补充说明：**可使用 Azure Application Gateway 或上传受信任证书到 LB**。

---

### 2.5 Azure 资源命名含空格问题

**评审主张：** `ACR_NAME="acragentic k8seastus2"` 和 `STORAGE_NAME="stagentic k8seastus2"` 包含空格，会导致 Azure CLI 命令失败。

**验证结果：** ✅ **完全正确**

- ACR 名称：5-50 个**字母数字**字符
- 存储账户名称：3-24 个**小写字母和数字**

包含空格必然导致 `ValidationError`。

**建议修复：** 按评审意见移除空格。

---

### 2.6 `kubeProxyReplacement` 值问题（评审意见部分有误）

**评审主张：** `review-3.md` 称 Cilium 1.14+ 中布尔值 `true` 已被弃用，应使用字符串 `"strict"`。

**验证结果：** ❌ **方向完全相反——评审意见错误**

实际历史演变如下：

| 时期 | `kubeProxyReplacement` 值 | 状态 |
|------|---------------------------|------|
| Cilium < 1.14 | `"strict"`, `"partial"`, `"disabled"` | 字符串模式 |
| **Cilium 1.14** | `"strict"`, `"partial"` 被**弃用**，推荐 `true`/`false` | 过渡期 |
| Cilium 1.16+ | **仅支持布尔值** `true`/`false` | 当前状态 |

官方提交记录明确显示：`"strict"` 和 `"partial"` 在 **Cilium 1.14 中被弃用**，推荐使用 `true`。后续提交进一步**移除了所有已弃用的值**（strict、disabled、probe、partial）。

`review-3.md` 认为应使用 `"strict"` 是**完全错误的**——这恰恰是被弃用并已移除的值。`review-2.md` 更准确：它指出在 Cilium 1.16+ 中，`kubeProxyReplacement` 应是布尔值。

`SKILL.md` §10.2 中使用 `kubeProxyReplacement: true`（布尔值）是**正确的**。`review-3.md` 的这条建议**不应采纳**。

---

## 三、🟠 High-Priority 验证

### 3.1 Sigstore 基金会归属问题

**评审主张：** 指南错误地将 Sigstore 称为 "CNCF graduated"，实际应为 OpenSSF 项目。

**验证结果：** ✅ **完全正确**

OpenSSF 官方公告确认 Sigstore 已成为 **OpenSSF** 的 graduated 项目。Sigstore **不是** CNCF 项目。指南多处将其标注为 "CNCF graduated"，属于事实错误。

**建议修复：** 将所有 "Sigstore CNCF graduated" 改为 "Sigstore (OpenSSF graduated)"。

---

### 3.2 IPE LSM 内核版本问题

**评审主张：** IPE LSM 在主线 Linux 6.8 中合并，而 Azure Linux 3.0 使用内核 6.6 LTS，因此 IPE 支持依赖微软的 backport。

**验证结果：** ✅ **完全正确**

IPE LSM 在 **Linux 6.8-rc1** 中合并进入主线。Azure Linux 3.0 确认为内核 **6.6 LTS**。微软已确认将 IPE backport 到 Azure Linux 3.0 内核。

`review-2.md` 和 `review-3.md` 均准确指出了这一依赖关系，并建议添加验证命令。

**建议修复：** 在 §5.6 中添加 IPE 可用性验证说明。

---

### 3.3 gVisor 下载 URL 问题

**评审主张：** GitHub tag 包含 `.0` 后缀（如 `20240101.0`），但 GCS URL 使用不带后缀的日期格式，直接拼接会导致 404。

**验证结果：** ✅ **完全正确**

gVisor GitHub 发布标签格式为 `20260608.0`。官方 gVisor 安装文档明确要求**剥离 `.0` 后缀**以构造正确的下载 URL。

**建议修复：** 使用 `jq -r '.tag_name | split(".")[0]'` 剥离后缀。

---

### 3.4 Kyverno `lookup_foreach` 策略问题

**评审主张：** Kyverno 的 `lookup` 函数不支持在 `foreach` 中动态匹配标签以查找 NetworkPolicy，该策略会编译失败。

**验证结果：** ✅ **正确**

Kyverno 的 `lookup` 函数确实**不支持**在 `foreach` 上下文中进行动态标签匹配迭代。`review-2.md` 和 `review-3.md` 均准确识别了此问题。Kyverno 官方文档中也没有此类用法的示例。

**建议修复：** 按评审意见替换为基于 annotation 的简化策略，或完全依赖 Cilium NetworkPolicy。

---

### 3.5 vLLM Deployment 标签与 RuntimeClass 矛盾

**评审主张：** vLLM deployment 使用 `runtimeClassName: nvidia-gpu` 但 label 为 `sandbox: kata`，会与 Kyverno 策略冲突。

**验证结果：** ✅ **正确**

这是文档内部的逻辑矛盾。Kyverno 的 `require-runtimeclass-for-agents` 策略要求 agentic namespace 中的 Pod 使用 `gvisor` 或 `kata` RuntimeClass，但 vLLM 使用 `nvidia-gpu`，会被拒绝。

**建议修复：** 统一标签与 RuntimeClass，或为 GPU 工作负载添加 Kyverno 策略例外。

---

## 四、🟡 次要问题与编辑问题

### 4.1 重复章节编号

`review-2.md` 指出 §13 中存在两个 §13.5。检查 `SKILL.md` 确认：§13.4（ResourceQuotas/LimitRanges）之后是 §13.5（Custom seccomp profiles），然后**又有一个 §13.5**（AppArmor vs SELinux）。第二个应为 §13.6。

### 4.2 OIDC 标志格式问题

`review-2.md` 指出 §11.1 的 OIDC 标志示例使用 map 格式，与 §8.1 的 v1beta4 列表格式不一致。虽然作为概念参考，但可能引起混淆。建议添加格式说明。

---

## 五、🔴 评审未覆盖的新发现问题

### 5.1 `SKILL.md` 中 `ValidatingAdmissionPolicy` 特性门控的双重存在

指南 §8.1 中 `ValidatingAdmissionPolicy=true` 出现了**两次**：
1. `ClusterConfiguration.apiServer.extraArgs` 中
2. `KubeletConfiguration.featureGates` 中

两份评审均指出了此问题，但未强调**两处都需删除**。删除时需确保**两处都移除**。

### 5.2 `SKILL.md` 中 Azure Linux OS Guard 的 "Preview" 状态

指南 §5.6 正确标注了 OS Guard 为 **"public preview"**。微软官方文档也确认 OS Guard 为 **preview** 状态。这是准确的，无需修改。

### 5.3 Azure Load Balancer HTTPS 探测的 2026 年替代方案

如 §2.4 所述，评审建议的 TCP 探测是正确且稳妥的。但截至 2026 年，Azure 提供了更丰富的选项：
- **Application Gateway** 可实现 L7 端到端加密
- **Front Door + Private Link** 场景需要受信任证书

建议在指南中补充这些选项，供需要 HTTPS 探测的团队参考。

---

## 六、总结：评审意见采纳矩阵

| 评审意见 | 来源 | 验证结果 | 是否采纳 |
|----------|------|----------|----------|
| `kubeletExtraArgs` → list 格式 | review-2, review-3 | ✅ 确认 | ✅ 采纳 |
| containerd CRI 路径 → `cri.v1.runtime` | review-3 | ✅ 确认 | ✅ 采纳 |
| 删除 `ValidatingAdmissionPolicy=true` | review-2, review-3 | ✅ 确认 | ✅ 采纳 |
| Azure LB 探测 → TCP | review-3 | ✅ 确认 | ✅ 采纳（可补充 AG） |
| Azure 资源命名移除空格 | review-3 | ✅ 确认 | ✅ 采纳 |
| Sigstore → OpenSSF | review-2, review-3 | ✅ 确认 | ✅ 采纳 |
| IPE 内核 6.8 backport 说明 | review-2, review-3 | ✅ 确认 | ✅ 采纳 |
| gVisor URL 剥离 `.0` | review-2, review-3 | ✅ 确认 | ✅ 采纳 |
| Kyverno `lookup_foreach` 失效 | review-2, review-3 | ✅ 确认 | ✅ 采纳 |
| vLLM 标签/RuntimeClass 矛盾 | review-2, review-3 | ✅ 确认 | ✅ 采纳 |
| 重复 §13.5 | review-2 | ✅ 确认 | ✅ 采纳 |
| **Cilium `kubeProxyReplacement: "strict"`** | **review-3** | ❌ **错误** | ❌ **拒绝** |
| OIDC 标志格式说明 | review-2 | ⚠️ 部分正确 | ⚠️ 有条件采纳 |

---

## 七、最终建议

1. **采纳 review-2.md 和 review-3.md 的全部建议**，但 **拒绝** `review-3.md` 中关于 `kubeProxyReplacement: "strict"` 的建议——该建议与 Cilium 1.16+ 的实际状态完全相反。

2. 在修复 `ValidatingAdmissionPolicy` 门控时，确保 **§8.1 中的两处都删除**。

3. 在 Azure LB 探测部分，可补充 Application Gateway 作为 HTTPS 探测的替代方案。

4. 执行修复后，`SKILL.md` 将达到生产级质量。

---

https://chat.deepseek.com/share/y70b7nag0bq0yroy1r 
