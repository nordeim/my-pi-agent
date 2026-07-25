```markdown
--- DOMAIN PACK: Academic (v10.1) ---
VERSION: 1.1
TRIGGER: 论文, 引用, 审稿, 他引, 自引, 组会, 预印本, 影响因子, 同行评审, 文献综述, 消融实验, paper, citation, peer review, manuscript, journal, preprint, impact factor, bibliometric, ablation, literature review, state of the art

## MODALITY TABLE (Pillar 1: Epistemic Modality & Hedging)
*Academic integrity relies on precise degrees of certainty. NEVER upgrade or downgrade the author's epistemic commitment.*

| Source Term | Target Term | Direction | Note |
|---|---|---|---|
| 证明 | demonstrates / proves | CN→EN | Strong claim. Use ONLY for mathematical/logical proof. |
| 表明 | indicates / shows | CN→EN | Moderate claim. Standard for empirical findings. |
| 提示 | suggests / implies | CN→EN | Tentative claim. **NEVER "proves"**. |
| 暗示 | hints at / suggests | CN→EN | Very tentative. |
| 推测 | hypothesizes / conjectures | CN→EN | Speculative. |
| demonstrates | 证明 / 表明 | EN→CN | Match source strength. |
| suggests | 提示 | EN→CN | **NEVER 证明**. |
| to the best of our knowledge | 据我们所知 | EN→CN | Standard academic hedge. |
| it remains an open question | 仍是一个悬而未决的问题 | EN→CN | |
| we conjecture | 我们推测 | EN→CN | |
| suboptimal | 次优的 | EN→CN | |
| fails to converge | 未能收敛 | EN→CN | |
| yields no significant improvement | 未产生显著改进 | EN→CN | |

## COLLOCATION TABLE (Pillars 2, 3, 4: Bibliometrics, Methodology, Lifecycle)

| Source Phrase | Target Phrase | Direction | Note |
|---|---|---|---|
| 他引 | independent citation / external citation | CN→EN | **CRITICAL: NEVER "self-citation"**. 他 = other. |
| 自引 | self-citation | CN→EN | |
| 严格他引 | strict independent citation | CN→EN | |
| 被引频次 | citation count | CN→EN | |
| 影响因子 | impact factor | CN→EN | |
| h 指数 | h-index | CN→EN | Preserve hyphen. |
| 预印本 | preprint | CN→EN | |
| 顶会 | top-tier conference | CN→EN | |
| 核心期刊 | core journal | CN→EN | |
| 同行评审 | peer review | CN→EN | |
| 开放获取 | open access (OA) | CN→EN | |
| 消融实验 | ablation study | CN→EN | |
| 基线模型 | baseline model | CN→EN | |
| 基准真值 | ground truth | CN→EN | |
| 显著性差异 | significant difference | CN→EN | |
| 置信区间 | confidence interval | CN→EN | |
| 稳健性检验 | robustness check | CN→EN | |
| 最新进展 | state-of-the-art (SOTA) | CN→EN | |
| 泛化能力 | generalization ability | CN→EN | |
| 桌面拒稿 / 秒拒 | desk reject | CN→EN | |
| 大修 | major revision | CN→EN | |
| 小修 | minor revision | CN→EN | |
| 回复信 | rebuttal / response letter | CN→EN | |
| 终稿 | camera-ready | CN→EN | |
| 项目负责人 | Principal Investigator (PI) | CN→EN | |
| 课题申请 | grant proposal | CN→EN | |

## ENTITY OVERRIDES (Journals, Funding, Roles)

| Source Entity | Target Entity | Note |
|---|---|---|
| Nature | 《自然》 (CN) / *Nature* (EN) | Apply Title-of-Works mapping (§9.3). |
| Science | 《科学》 (CN) / *Science* (EN) | |
| NeurIPS / CVPR | NeurIPS / CVPR | Preserve acronyms verbatim. |
| 国家自然科学基金 | National Natural Science Foundation of China (NSFC) | Official EN name. |
| 通讯作者 | corresponding author | CN→EN |
| 第一作者 | first author | CN→EN |
| 共同第一作者 | co-first author | CN→EN |

## TOPOLOGY & ASYMMETRY RULES (Pillar 5 & Deep-Dive)
*Structural rules to prevent formatting decay and register drift.*

1. **Citation Topology (CRITICAL):** Citation brackets `[1, 2-4]` MUST remain half-width and comma-separated. **NEVER** convert to full-width `【1，2-4】` or `【1，2-4】`.
2. **Author Truncation:** `et al.` ↔ `等`. (e.g., "Smith et al." ↔ "Smith 等").
3. **Cross-References:** Figure 1 ↔ 图 1, Table 2 ↔ 表 2, Eq. 3 ↔ 式 3 / 公式 3, Section 4 ↔ 第 4 节.
4. **The "We" Pronoun Asymmetry:** 
   - **CN→EN:** English academic papers heavily use active voice. Inject "We" or "This paper" ("本文提出" → "We propose"). Avoid passive voice where "We" is natural.
   - **EN→CN:** Chinese academic papers often omit the subject or use "本文". Drop "We" and use "本文" or passive ("We demonstrate" → "实验表明" / "本文证明").
5. **Abstract Tense Convention:** 
   - **EN Abstracts:** Use **Present Tense** for established facts, proposals, and conclusions ("This paper proposes...", "Results show..."). Use **Past Tense** for specific experimental actions ("We evaluated the model on...").
   - **CN→EN Mapping:** Map CN aspect particles (了, 过) to Past Tense for experimental actions, and use Present Tense for general claims.

## ANTI-TRANSLATIONESE PAIRS (Pillar 6: False Friends)

| Wrong | Correct | Note |
|---|---|---|
| Article (journal) → 文章 | Article → **论文** | "文章" is for general essays/blog posts. |
| Thesis (PhD) → Thesis | Dissertation → **学位论文** | Master's = thesis; PhD = dissertation. |
| Resume → 简历 | CV → **简历** | Academic context = CV (curriculum vitae). |
| Argument (math/code) → 论点 | Argument → **参数** | Humanities/debate = 论点. |
| related work (section) → 相关工作 | Related Work → **Related Work** | Capitalize as a section title. |

## CALIBRATION ANCHORS (Behavioral Few-Shots)
*Internalize these transformations to anchor the target register.*

**Anchor 1 (STEM Abstract CN→EN):**
- Source: "本文提出了一种新架构，消融实验表明其性能优于基线模型，但仍存在局限性。"
- Target: "We propose a novel architecture. Ablation studies indicate that its performance outperforms the baseline model, although limitations remain."
- *Key:* "We propose" (Active), "indicate" (Moderate modality for 表明), "baseline model", "limitations".

**Anchor 2 (Bibliometrics CN→EN):**
- Source: "该学者的 h 指数为 45，其严格他引率在核心期刊中名列前茅。"
- Target: "The scholar's h-index is 45, and their strict independent citation rate ranks among the top in core journals."
- *Key:* "h-index", "strict independent citation rate" (NEVER self-citation).

**Anchor 3 (Peer Review EN→CN):**
- Source: "The reviewers recommended a major revision. The desk reject was avoided."
- Target: "审稿人建议进行大修。避免了桌面拒稿（秒拒）。"
- *Key:* "major revision", "desk reject".

**Anchor 4 (Citation Topology Invariant):**
- Source: "Recent studies [1, 3-5] show..."
- Target: "Recent studies [1, 3-5] show..." (or CN equivalent preserving the exact half-width bracket topology).
- *Key:* Brackets remain `[ ]`, NOT `【 】`.

--- END DOMAIN PACK ---
```

---
