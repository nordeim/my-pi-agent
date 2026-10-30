# Critical Comparative Audit — Three Big-Tech Research Skills vs. Wall Street Standards

## Verification basis

I inspected the three `SKILL.md` files, their reference documents, templates, assets, script docstrings, and the repository’s regression-test suite via the public GitHub repository. I did **not** clone or execute the code in this environment. One raw-file rendering of `note_audit.py` truncated at a `TODO` marker; the GitHub contents API reports a 12,298-byte file and a dedicated test suite, so I treat the implementation as present but could not read every line. Script-level findings below are therefore based on docstrings, visible code, and tests — not a full line-by-line execution audit. Confidence labels are used throughout.

---

## Verdict at a glance

| Dimension | Assessment |
|---|---|
| **Epistemic discipline** | **Best-in-class for an AI research workflow.** Competing hypotheses, confidence taxonomy, primary-source hierarchy, consensus vintage/statistic controls, and explicit exclusion of at least one hypothesis are stronger than most sell-side notes. |
| **Accounting rigor** | **Strong.** ASC 280 segment-map staleness gate, Reg G/Item 10(e) reconciliation, FCF ex-SBC, GAAP-to-adjusted bridging, multi-class market-cap handling, and beta-regime diagnostics are genuinely institutional-grade controls. |
| **Auditability / engineering** | **Unusually strong.** Machine-checked number registries, provenance sealing, render/a11y gates, byte-identical vendoring, and a CI regression suite are rare in this category. |
| **Valuation** | **The defining gap.** No DCF, no SOTP, no comparable-company-derived target, no scenario-weighted fair value, no price target, no rating. The skills explicitly firewall themselves as “attribution” products. |
| **Forward modeling** | **Absent.** No 3-statement model, no revenue/margin build, no independent estimates. Consensus is consumed, not produced. Variant views are optional at best. |
| **Primary research** | **Explicitly excluded.** “Public-source-only” — no channel checks, expert calls, management access, or surveys. This is a stated limitation, not an oversight. |
| **Regulatory compliance** | **Narrow but honest.** The output is labeled “not a research report,” internal-use-only, with no Reg AC certification and no FINRA 2241 package. It is compliant *as an internal pre-read*, not as published sell-side research. |
| **Empirical validation** | **Pending.** The methodology’s validation protocol is explicitly “documented harness pending” — no backtest or accuracy study. |
| **Wall Street readiness** | **Strong internal IC attribution note; not a substitute for a full equity research report or investment memo.** |

**Overall:** These are among the more rigorous AI-generated equity-research frameworks publicly available, particularly on evidence discipline and machine-checkable auditability. But they deliberately stop short of the core deliverable of Wall Street equity research: a **forward-looking valuation**. Against the highest standards of a major investment bank or fund manager, they are a sophisticated **input** to the research process, not a complete research product.

---

## 1. What each skill actually is

| | **Skill 1 — `analyzing-us-bigtech-stocks`** | **Skill 2 — `big-tech-earnings-postmortem`** | **Skill 3 — `bigtech-equity-research`** |
|---|---|---|---|
| **Positioning** | Flagship full-pipeline event RCA and trend report. 12–16 page HTML IC deck. | Lightweight single-file post-earnings note. Fastest-ship member. | Quantified single-note with segment deep-dive and options math. |
| **Workflow** | Phases 0–10; nine-lens hypothesis tree including market microstructure. | 7-step workflow; layered driver attribution; no full fact base. | 7-phase process; ASC 280 segment gate; 14-section HTML note. |
| **Evidence layer** | Full `fact_base.json`; every number sourced; decision-critical numbers double-sourced. | Lite number registry (`fact_base_lite.json`); machine-checked against the note. | Lite registry plus segment-map gate and canonical peer baskets. |
| **Audit gates** | Full fact-base audit, render, a11y, provenance; schema gates CONSENSUS / EPISTEMIC / WATERFALL / MANDATE / TEMPORAL. | Lite registry gate, placeholder/disclosure gate, render, a11y, provenance. | Same lite gate set plus segment-map staleness gate. |
| **Relative rigor** | Most **comprehensive** and broadest. | Least rigorous by design; narrowest scope. | Most **technically rigorous** on segment accounting and options math; narrower than Skill 1. |
| **Best use** | IC pre-read for a major price event or multi-quarter trend. | Fast post-earnings explainer. | Single-name deep dive where segment mix and options-implied move matter. |

The hierarchy is clear and consistently documented: Skill 1 is the canonical source of family doctrine; Skill 2 is the standalone lightweight execution; Skill 3 is the quantitative single-note specialist. The routing language in each `SKILL.md` is explicit about when to use which, which is good product discipline.

---

## 2. What is genuinely strong — and rare

### 2.1 Competing hypotheses and explicit elimination

Skill 1 requires a 5–8 hypothesis tree across nine lenses, including market microstructure and flow, and requires at least one hypothesis to be explicitly excluded with evidence. Skill 2 mirrors this with a “ranked driver table plus at least one explicitly rejected driver”. This is a meaningful improvement over the common sell-side practice of presenting a single, tidy narrative. It directly addresses confirmation bias.

### 2.2 Confidence taxonomy with an epistemic split

The family uses `Verified` / `Reasoned (derived)` / `Reasoned (judged)` / `Assumed` / `Unverifiable`, and the schema enforces the split between deterministic derivation and analytical judgment. This is a strong control: a driver-decomposition weight is not allowed to masquerade as a measured fact. The `waterfall_check` is explicitly described as an arithmetic consistency check, not evidence of causation. That is exactly the right caveat.

### 2.3 Primary-source hierarchy and consensus discipline

Tier 1 is SEC filings, IR releases, and official transcripts; Tier 2 is named press; Tier 3 is aggregators for prices only. Consensus figures must carry a named provider, a vintage within 1–3 trading days, a recorded statistic (mean/median/undisclosed), and a T1/T2 source. The audit mechanically enforces these fields. This is more rigorous than most AI-generated research and comparable to a good buy-side workflow. The explicit warning that two aggregators scraping the same wire story do not corroborate anything is a particularly sharp control.

### 2.4 Accounting and market-mechanics rigor

- **Event-window rule:** after-close event → T+1 close; pre-market/intraday event → T+0 close. This avoids contaminating the event return with an extra session.
- **Multi-class market-cap delta:** compute each share class separately and sum; never one class’s shares with another’s price.
- **Beta regime diagnostics:** R² floor of 0.30 and trailing-vol z-score threshold of 2.0; if breached, the canonical 2-year monthly beta is treated as fitting a broken regime.
- **ASC 280 segment-map staleness gate:** the filing’s own segment note is the source of truth; a stale map fails the build, not warns. This is a sophisticated control that prevents a confidently wrong variance table from passing a numeric audit.
- **Reg G / Item 10(e):** every non-GAAP metric must reconcile to GAAP, with the basis of each beat/miss stated.
- **FCF ex-SBC:** mandatory, not optional, for US mega-cap tech.

### 2.5 Machine-checkable audit trail

The full fact base is the single source of truth; if a number is not in it, it does not go in the report. The audit checks forward (every fact appears on the slides), reverse (every slide number is registered), formula arithmetic, placeholder tokens, and `Assumed` facts on the method page. The lite variant closes the “credibility spillover” gap by giving Skills 2 and 3 a machine-checked registry too. Provenance sealing with SHA-256 provides post-delivery tamper evidence. The test suite includes regression tests for the audit gates, byte-identical vendoring, and cross-skill consistency. This engineering discipline is rare in the AI-skill ecosystem and is a genuine strength.

### 2.6 Two-sidedness and counter-case

Both the full and lite workflows require a counter-case — “what the market may be underweighting” — with sourced evidence. This is a credibility feature that many sell-side notes lack in practice.

---

## 3. Critical gaps against top-tier Wall Street standards

### 3.1 Valuation is excluded — the single largest gap

The skills explicitly state that they do **not** produce a DCF, SOTP, scenario-weighted fair value, price target, or rating. The 14-section note includes a “Valuation Impact & Boundary” section, but it contains only a forward-multiple band as *context*, explicitly not an intrinsic valuation.

For a major investment bank or fund manager, valuation is not an optional appendix. Equity research is fundamentally about determining whether the market price diverges from intrinsic value. A report that explains why a stock moved but refuses to opine on whether it is now cheap or expensive is an **attribution note**, not an equity research report. The skills are honest about this — they firewall themselves as “IC pre-read attribution notes” — but the user’s benchmark is the highest Wall Street standard, and on that benchmark this is a decisive limitation.

**What is missing:** DCF with explicit WACC and terminal growth; comparable-company analysis with justified multiple selection; SOTP for multi-segment names; scenario-weighted fair value; target price derivation; rating definitions and horizon; sensitivity tables.

### 3.2 No forward earnings model or independent estimates

The skills consume consensus but do not build their own forward estimates. There is no 3-statement model, no revenue build by segment, no margin bridge, no capex/depreciation schedule, and no working-capital model. A variant view is optional and, when omitted, simply logged as an open item.

Wall Street research differentiates through **estimate revisions** and a **variant view versus consensus**. A report that takes consensus as an input but never forms its own forecast cannot generate a differentiated call. It can explain the past; it cannot underwrite the future.

### 3.3 No primary research

The skills are explicitly “public-source-only”: no channel checks, expert calls, surveys, or management access. This is disclosed as a limitation, not hidden. But primary research is one of the main ways major banks and funds generate informational advantage. A public-source-only product is structurally undifferentiated at the insight layer, even if its process is rigorous.

### 3.4 “Machine-checked” means internal consistency, not source truth

The fact-base audit verifies that numbers in the deck match the fact base, that formulas evaluate, and that fields are populated. It does **not** fetch the cited URL, parse the filing, or independently verify that the number in the fact base matches the source. A fact base entry could contain an incorrect number with a valid-looking URL and pass every audit gate.

This is an important distinction. The system is strong on **traceability** and **internal consistency**, but it is not a source-verification engine. For a bank’s model-risk or compliance function, that difference matters. The registry is populated by the agent and/or analyst; the audit checks structure and cross-references, not truth.

### 3.5 No formal research-compliance package

The skills correctly avoid pretending to be regulated research: they carry “not a research report,” “internal analytical pre-read,” and “public-source-only” legends; they state no Reg AC certification and no FINRA 2241 disclosure package. That is the right scoping decision.

But against the standard of a major investment bank, the following are absent:
- Analyst certification under Regulation AC;
- FINRA Rule 2241 conflict-management disclosures, rating distribution, and banking-relationship disclosure;
- Supervisory approval and records-retention workflow;
- Formal information-barrier procedures beyond “suspect MNPI → stop and escalate”;
- A research-rating committee or coverage-review process.

The buy-side conflict disclosure (`meta.mandate_context` with `fund_position` and `position_as_of`) is a good CFA Standard I(B) control, but it is conditional on an IC audience and optional for other audiences. For a fund manager, conflict disclosure should be unconditional on any investment recommendation.

### 3.6 No empirical validation of the methodology

The methodology document explicitly labels the validation protocol as “documented harness pending”. There is no backtest showing that the RCA framework improves post-event classification accuracy, forecast accuracy, or portfolio returns. The worked Alphabet example is concrete and internally consistent, but it is an illustration, not validation.

For a bank’s model-risk standards, an analytical framework that has not been empirically validated is a **tier-2 / judgment-based** tool, not a validated model. That is acceptable for an IC pre-read; it is not sufficient for a systematic research process.

### 3.7 Limited industry, competitive, and management analysis

The hypothesis tree includes a “structural narrative threat” lens and a capital-allocation regime break, but there is no formal industry analysis (Porter’s five forces, TAM, competitive dynamics), no management-quality scorecard, no capital-allocation track record, and no ESG/governance assessment. These are standard components of a full initiating-coverage report.

### 3.8 Portfolio construction and sizing are out of scope

The optional Expected Fundamental Value matrix weights fundamental outcomes by subjective probabilities and produces an EV-adjusted fundamental range, explicitly not a price target or fair-value claim. It is a useful asymmetry profile, but it is not a position-sizing framework, risk-budget model, or portfolio-construction input. A fund manager would need to translate the fundamental range into expected return, correlation, and position size — none of which the skills provide.

### 3.9 Data limitations

Prices come from Tier 3 aggregators; consensus is “as reported by a named outlet,” not a licensed point-in-time feed; there is no survivorship-bias-free universe, no alternative data, and no proprietary data. The skills are transparent about this, but it is a structural disadvantage versus a bank with Bloomberg/FactSet/Visible Alpha terminals and alternative-data subscriptions.

### 3.10 Overlap and maintenance risk

Three overlapping skills with different rigor levels create a maintenance and user-confusion risk. The repository mitigates this with canonical-doctrine rules, byte-identical vendoring, and `test_repo_consistency.py`. That is a good engineering control, but the underlying product architecture still has three partially redundant research workflows, each with its own audit layer. A bank’s research technology stack would typically prefer one canonical pipeline with configurable depth, not three separate products.

---

## 4. Comparative assessment against Wall Street standards

| Standard | Skill 1 | Skill 2 | Skill 3 | Wall Street expectation |
|---|---|---|---|---|
| **Primary-source grounding** | Strong | Strong | Strong | SEC filings, transcripts, company IR — met |
| **Consensus discipline** | Strong | Lite version | Strong | Provider, vintage, statistic, contributor count — met |
| **Hypothesis testing / falsification** | Strong | Strong | Strong | Best practice — exceeded |
| **Accounting rigor** | Strong | Moderate | Very strong | ASC 280, Reg G, FCF ex-SBC — met |
| **Segment analysis** | Good | Moderate | Very strong, with staleness gate | Segment build — met |
| **Options / market mechanics** | Good | Moderate | Strong, with implied-move math | Good |
| **Valuation** | **Absent** | **Absent** | **Absent** | **Core requirement — not met** |
| **Forward model / estimates** | **Absent** | **Absent** | **Absent** | **Core requirement — not met** |
| **Variant view vs. consensus** | Optional | Optional | Optional | **Expected — not met** |
| **Primary research** | Excluded | Excluded | Excluded | **Differentiator — not met** |
| **Rating / target price** | Excluded | Excluded | Excluded | **Core sell-side output — not met** |
| **Reg AC / FINRA 2241** | Not applicable; disclaimed | Not applicable; disclaimed | Not applicable; disclaimed | **Required for published research — not met** |
| **Model validation / backtest** | Pending | Pending | Pending | **Expected — not met** |
| **Auditability / provenance** | Very strong | Strong | Very strong | Stronger than many internal tools |
| **Accessibility / rendering QA** | Strong | Strong | Strong | Good engineering hygiene |

**Interpretation:** The skills are not trying to be full sell-side research reports. They explicitly position as internal IC pre-reads. Judged against that narrower standard, they are strong. Judged against the **highest Wall Street standard** — a published initiating-coverage report or a full buy-side investment memo — the absence of valuation, forward estimates, primary research, and a formal compliance package is disqualifying. The correct conclusion is not “these are bad”; it is “these are excellent **attribution** tools that should not be mistaken for **complete equity research**.”

---

## 5. Specific technical and verification concerns

1. **`note_audit.py` raw rendering truncated.** The raw view stopped at a `TODO` marker at line 45, but the GitHub contents API reports a 12,298-byte file and a dedicated test suite. I could not fully inspect the implementation, so I cannot confirm whether the `TODO` is a real placeholder or a rendering artifact. This should be checked directly in the repository before relying on the gate.
2. **Provenance sealing is SHA-256 only.** No firm-key signing, WORM archival, or retention scheduling; the skill explicitly scopes these out. This is adequate tamper evidence, not enterprise records management.
3. **Accessibility gate is a static subset.** It checks language, heading order, image alt, and WCAG-AA contrast, but not full axe-core parity, keyboard operability, or ARIA semantics. The claim is appropriately scoped.
4. **Numeric matching is heuristic.** The audit uses anchored, sign/symbol-tolerant matching; it can produce false positives/negatives, which is why strict modes are opt-in. This is a reasonable engineering tradeoff, but it is not a formal proof of numerical integrity.
5. **Formula checks verify arithmetic identity, not economic correctness.** A formula with a wrong economic assumption but internally consistent arithmetic will pass. The audit is a consistency check, not a model-validation check.
6. **Beta diagnostics use heuristic thresholds.** R² < 0.30 and |z| > 2 are sensible flags, but they are not a formal structural-break test. They are better than no regime check, but not equivalent to a bank’s model-risk diagnostics.
7. **Consensus “undisclosed” statistic is honest but weaker.** Allowing `undisclosed` records that the analyst looked; it does not solve the underlying data-quality problem. A licensed point-in-time consensus feed would be stronger.

---

## 6. What would be required to reach top-tier Wall Street standards

If the goal is to move from “excellent internal attribution note” to “institutional-grade equity research,” the following additions are necessary:

1. **Valuation module.** DCF with explicit WACC, terminal growth, and sensitivity tables; comparable-company analysis with justified peer selection and multiple selection; SOTP for multi-segment names; scenario-weighted fair value; target price and rating with a defined horizon.
2. **Forward 3-statement model.** Revenue build by segment, margin bridge, capex/depreciation schedule, working-capital model, and a variant view versus consensus with explicit estimate differences.
3. **Primary-research layer.** Expert-network calls, channel checks, management access, or licensed alternative data — or an explicit partnership with a provider. Public-source-only is a legitimate limitation, but it caps the insight ceiling.
4. **Formal compliance wrapper.** Reg AC certification, FINRA 2241 disclosures, rating definitions, supervisory approval, records retention, and information-barrier procedures — if the output is ever distributed externally.
5. **Independent model validation.** Backtest the RCA framework against actual post-event outcomes; measure classification accuracy, calibration of confidence labels, and decision usefulness. Publish the validation harness.
6. **Accounting-quality scorecard.** Accruals, cash conversion, DuPont decomposition, lease/pension adjustments, and working-capital quality — beyond the current one-off inventory.
7. **Industry/competitive deep dive.** Porter’s five forces, TAM, competitive positioning, management quality, and capital-allocation track record.
8. **Portfolio/sizing layer.** Translate the fundamental range into expected return, risk contribution, and position size; integrate with a portfolio-construction framework.
9. **Source verification.** Fetch and hash source content, not just record URLs; consider a source-snapshot archive for audit defensibility.
10. **Product consolidation.** One canonical pipeline with configurable depth (lite / standard / full) would reduce the maintenance and confusion risk of three overlapping skills.

---

## 7. Bottom line

**For an AI-driven research workflow, this is a serious, thoughtfully engineered body of work.** The epistemic discipline, consensus controls, accounting gates, and machine-checked audit trail are genuinely impressive and materially better than the typical “LLM stock summary.” The decision to firewall the output as an internal IC pre-read rather than a regulated research report is the correct compliance judgment.

**But the user’s benchmark is the highest standard of major investment banks and fund managers, and on that benchmark the skills fall short in four decisive areas:** valuation, forward modeling, primary research, and formal research compliance. They explain price moves with rigor; they do not value businesses, forecast earnings independently, or generate actionable ratings. They are a strong **input** to an investment process, not a substitute for a complete equity research product.

**Recommended framing:** Treat Skill 1 as the flagship internal attribution engine; Skill 3 as the segment/options specialist; Skill 2 as the fast post-earnings note. Do not present any of them as a sell-side research report, and do not use them as the sole basis for a position without a separate valuation and forward-model overlay.

---

### Verification ledger

| Claim | How checked | Confidence |
|---|---|---|
| Skill 1 requires 5–8 hypotheses and explicit exclusion | Read `SKILL.md` lines 181–202 | Verified |
| Skills exclude DCF, SOTP, price targets, ratings | Read `SKILL.md` valuation-boundary sections in all three skills | Verified |
| Consensus requires provider, vintage, statistic, T1/T2 | Read `SKILL.md` and `methodology.md` consensus sections | Verified |
| Segment-map staleness gate fails the build | Read `segment-maps.md` and `segment_map_check.py` docstring | Verified |
| Provenance sealing is SHA-256 only, no signing | Read `provenance_seal.py` docstring | Verified |
| Methodology validation is “pending” | Read `methodology.md` table of contents | Verified |
| Full audit verifies internal consistency, not source truth | Read `fact_base_audit.py` docstring; audit checks appearance/arithmetic, not URL retrieval | Reasoned |
| `note_audit.py` raw view truncated | Observed raw rendering; API reports 12 KB file and tests exist | Verified observation; file completeness unverified |
| Skills are compliant as internal pre-reads, not as research reports | Read compliance sections in all three `SKILL.md` files | Verified |
| Wall Street valuation/forward-model/primary-research expectations | General industry knowledge; consistent with sell-side research structure sources | Reasoned |

**Not executed:** The scripts and test suite were not run in this environment. No claim about passing audits or test results is made.

---

