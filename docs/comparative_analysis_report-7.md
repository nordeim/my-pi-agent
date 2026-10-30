## Audit Summary

**Scope:** Three sibling skills in `nordeim/my-pi-agent` — `analyzing-us-bigtech-stocks` (v1.3.0, 301-line SKILL.md + references/ + scripts/), `big-tech-earnings-postmortem` (v1.3.0, 290-line SKILL.md + assets/ + scripts/), and `bigtech-equity-research` (v1.2.0, 140-line SKILL.md + reference/ + templates/ + scripts/). The audit covers their SKILL.md doctrine, supporting reference documents, Python/Node audit scripts, and HTML deliverable templates, benchmarked against Wall Street institutional standards for equity research objectivity, auditability, model validation, and IC-memo evidence discipline.

**Finding counts by severity:**

| Severity | Count | Nature |
|---|---|---|
| **Critical** | 2 | Regulatory compliance gap; provenance/audit-chain void |
| **High** | 4 | Analyst-certification absence; forecast/estimate sourcing opacity; “Reasoned” label overload; segment-map staleness risk |
| **Medium** | 5 | Script-level verification gaps; disclosure-needle incompleteness; statistical label imprecision; conflict-of-interest omission; render-gate scope |
| **Low** | 3 | Naming/consistency; template redundancy; helper coverage |
| **Informational** | 2 | Family architecture strengths; evidence-discipline innovations |

**Bottom line:** These skills represent a genuinely rigorous epistemic architecture — substantially above the median of LLM-generated “equity research” tooling. The confidence taxonomy, two-axis driver classification, fact-base schema, and compute-don’t-recall discipline are materially stronger than most sell-side junior-analyst workflows. **However, they are not yet “investment-bank-grade” in the regulatory or provenance dimensions.** The skills explicitly position themselves as internal analytical notes, not sell-side research (line 28–29 of `sourcing-and-confidence.md`), which is a defensible scoping choice — but if that framing is taken at face value, the “Wall Street standards” comparison shifts from *sell-side regulatory compliance* to *buy-side IC-memo evidentiary discipline*, where the skills perform better but still leave material gaps in forecast sourcing and conflict disclosure.

The three skills are **not three independent products**; they are a layered family with a shared doctrine. `analyzing-us-bigtech-stocks` is the flagship (full pipeline, fact-base audit, 12–16 page IC deck). `big-tech-earnings-postmortem` is a compressed, standalone execution of the same doctrine (single-file note, lite audits, canonical framework borrowed from the flagship). `bigtech-equity-research` is the quantified single-note variant (segment deep-dive, options math, `quant_helpers.py`). The family is architecturally coherent — a rarity in skill libraries — but that coherence creates a single point of doctrinal failure: if the flagship’s framework is wrong, all three inherit the error. The repository’s `tests/test_repo_consistency.py` (referenced at line 29 of the postmortem and line 14 of the framework) is designed to guard against drift, which is a commendable control.

---

## Critical Findings

### C-1. No analyst certification, no conflict-of-interest disclosure, no rating/PT framework — regulatory non-compliance if positioned as research

**Locations:** `bigtech-equity-research/reference/sourcing-and-confidence.md` lines 26–31; `bigtech-equity-research/SKILL.md` lines 14–15 (disclaimer: “Analytical output only — not investment advice”); `analyzing-us-bigtech-stocks/SKILL.md` lines 51–53 (explicitly excludes price targets and trading signals). All three skills omit any mechanism for the disclosures required by SEC Regulation AC, FINRA Rule 2241, or MiFID II Article 13.

**Evidence:** The skills produce documents that explain price moves, attribute causes, and — in the case of `bigtech-equity-research` — compute implied moves, price-target cuts, and forward-multiple bands (lines 26–41 of `formulas.md`, lines 32–37 of `report-structure.md`). A reader could reasonably treat such a document as a research report. Yet the skills contain **no analyst certification** (“views accurately reflect personal views”), **no compensation-disclosure statement**, **no rating or price-target definition**, **no conflict-of-interest disclosure**, and **no supervisory-analyst approval mechanism**. The disclaimer at line 28–29 of `sourcing-and-confidence.md` (“not for distribution as sell-side research: no rating, no price target, no analyst certification or conflict disclosures”) is a **scoping disclaimer**, not a compliance substitute. Under Regulation AC, a “research report” is defined by content and distribution, not by the author’s self-labeling. A document that says “why GOOGL dropped 12% and what it means for the forward multiple band” is functionally a research report, even if it disclaims sell-side status.

**Impact:** If these skills are used inside a regulated broker-dealer, investment adviser, or fund manager, the produced artifacts may trigger recordkeeping, certification, and disclosure obligations that the skills do not satisfy. Even in a purely internal buy-side context, the absence of conflict disclosure (e.g., the fund’s existing position in the covered name) undermines IC-memo integrity. CFA Institute Standard I(B) and FINRA Rule 2241 both require analysts to disclose conflicts and maintain independence; the skills address *epistemic* independence but not *conflict* independence.

**Severity:** Critical. **Confidence:** Verified (the omissions are visible in the files).

**Recommended fix:** Either (a) harden the disclaimer into a structured “Scope & Limitations” page that states the document is not a research report under Regulation AC / FINRA 2241, specifies the internal-use-only distribution, and includes a conflict-of-interest declaration (e.g., “The author/fund may hold positions in the covered securities; see attached holdings disclosure”); or (b) add an optional “sell-side compliance module” that injects analyst certification, rating definitions, PT methodology, conflict disclosures, and a supervisory-approval stamp. The skills should also adopt a **position-disclosure field** in the fact-base schema (`fund_position`, `position_as_of`) when used by an asset manager.

---

### C-2. No immutable provenance chain or audit-trail persistence — the “audit” is point-in-time, not defensible

**Locations:** `fact_base_audit.py` lines 8–32 (the audit modes); `note_audit.py` (disclosure needles); `note_overflow_audit.mjs` (render gate). None of the scripts produce a tamper-evident record, a versioned hash of the fact base, or a timestamped audit log that survives delivery.

**Evidence:** The audit scripts verify that numbers on slides match the fact base, that placeholders are absent, and that disclosures are present (lines 3–32 of `fact_base_audit.py`). But the fact base itself is a mutable JSON file. There is no hash, no signature, no append-only log of fact-base changes, no linkage between the delivered HTML file and the fact-base version it was built from, and no retention mechanism. The delivered HTML contains a “verification-status line” (lines 8–13 of `report-structure.md`), but that line is **self-reported**; nothing prevents a user from editing the HTML after the gate passes and re-labeling it “gates passed.” SEC Rule 17a-4 requires a “complete time-stamped audit trail” that permits recreation of the original record; the skills offer a **pre-delivery check**, not a **provenance chain**.

**Impact:** In an institutional setting, a PM or compliance reviewer cannot demonstrate that the delivered note corresponds to the audited fact base. If a number is later challenged, the firm cannot produce a defensible chain of custody. This is precisely the gap that BlueMatrix’s Research Provenance Standard (search result 3) and Rule 17a-4’s audit-trail alternative are designed to close. The skills’ own evidence ledger (`templates/evidence-ledger.md`) is a **content** ledger, not a **technical** provenance ledger — it lists sources and confidence tags, not hashes and timestamps.

**Severity:** Critical. **Confidence:** Verified.

**Recommended fix:** Add a `--seal` mode to `fact_base_audit.py` that computes a SHA-256 hash of the fact base and the rendered HTML, writes the hash and timestamp into a `provenance.json` sidecar, and embeds the hash in the HTML footer. The verification-status line should reference the hash, not just “gates passed.” For regulated deployments, optionally sign the manifest with a firm key. This is a technical control the skills currently lack entirely.

---

## High Findings

### H-1. Consensus/forecast sourcing is named but not operationalized — the “double-sourcing” rule does not apply to the most decision-critical input

**Locations:** `bigtech-equity-research/reference/methodology.md` lines 13–16 (“Consensus estimates — FactSet/Visible Alpha/Refinitiv (LSEG)-referencing notes or Bloomberg consensus **as reported by a named outlet**”); `big-tech-earnings-postmortem/SKILL.md` lines 90–111 (scorecard construction); `analyzing-us-bigtech-stocks/references/fact-base-schema.md` lines 23–27 (decision-critical facts require ≥2 cross-checks).

**Evidence:** The skills repeatedly emphasize double-sourcing for *reported* figures — revenue, EPS, FCF, segment splits. But the **consensus estimate** is the denominator of every beat/miss delta, and the skills do not require the same evidentiary rigor for consensus. A consensus number “as reported by a named outlet” may be stale, based on a different share class, or computed on a non-comparable basis. The fact-base schema’s `decision_critical` list (lines 23–27 of `fact-base-schema.md`) is intended to include consensus facts, but the schema does not mandate a **consensus vintage** field (e.g., `consensus_as_of`, `contributor_count`, `consensus_source_chain`). In practice, a junior analyst could pull a single consensus print from Yahoo Finance (Tier 3 for fundamentals per the skills’ own hierarchy) and the audit would not catch it unless the fact was manually flagged as decision-critical and the auditor noticed the missing cross-check.

**Impact:** Beat/miss deltas are the atomic unit of the analysis (line 16 of `bigtech-equity-research/reference/methodology.md`: “The delta, not the absolute, is what moves price”). If the consensus is wrong, every delta is wrong, and the entire causal narrative is built on sand. This is a **root-cause input** that the skills treat as a Tier 2/3 convenience rather than a Tier 1 constraint. Sell-side research standards require consensus to be sourced from a named provider with a stated as-of date and contributor count; the skills gesture at this but do not enforce it.

**Severity:** High. **Confidence:** Reasoned (the schema could accommodate consensus fields, but the SKILL.md workflow does not require them).

**Recommended fix:** Add `consensus_vintage`, `consensus_source_tier`, and `consensus_provider` to the fact-base schema and make them **required for any fact in the `guidance` or `fundamentals` category used in a beat/miss delta**. Extend `fact_base_audit.py` to fail if a delta fact lacks a consensus-side fact with a Tier 1/2 source and a vintage within a configurable window (e.g., 5 trading days before the event).

---

### H-2. “Reasoned” is overloaded to cover both deterministic derivation and judgment — the boundary is stated but not mechanically enforced

**Locations:** `analyzing-us-bigtech-stocks/SKILL.md` lines 56–63 (confidence table: `Reasoned` = “Logical inference or computation from `Verified` inputs”); `bigtech-equity-research/SKILL.md` lines 40–43 (“Driver-decomposition weights and structural-vs-cyclical calls are `Reasoned` analysis, not reported facts”); `bigtech-equity-research/templates/evidence-ledger.md` lines 16–20 (“root-cause weights are `Reasoned` judgment, not reported fact — the sum-to-move identity is an arithmetic consistency check, not evidence of causation”).

**Evidence:** The skills correctly distinguish “Reasoned” (derived from verified inputs) from “Verified” (directly observed), and they explicitly warn that waterfall weights are judgment, not measurement (lines 27–31 of `report-structure.md`). This is better than most sell-side notes. But the **label itself conflates two qualitatively different epistemic objects**: (a) deterministic arithmetic derivation (e.g., `FCF = OCF − Capex`, `market-cap delta = shares × Δprice`) and (b) subjective analytical judgment (e.g., “this driver explains 40% of the move”). A deterministic derivation is reproducible; a judgment allocation is not. The skills acknowledge this in prose but do not encode it in the schema or the audit. The `fact_base_audit.py` `formula` checker (lines 15–18) validates arithmetic for facts with a `formula` field, but it does not validate the **sum-to-move consistency** of a waterfall whose components are tagged `Reasoned`. The evidence ledger template (line 19) says the sum-to-move identity is “an arithmetic consistency check, not evidence of causation,” but nothing in the scripts checks that the signed weights actually sum to the realized move.

**Impact:** A waterfall labeled `Reasoned` can ship with component weights that do not sum to the total move, and the only safeguard is a human reader noticing the arithmetic error. In an IC setting, a PM could reasonably ask “what is the decomposition methodology?” and the skills would answer “signed judgment weights, consistency-checked” — but the consistency check is not automated. This is a **soft control** where the skills claim a **hard gate**.

**Severity:** High. **Confidence:** Verified (the audit script does not enforce waterfall sum consistency).

**Recommended fix:** Split the taxonomy into `Derived` (deterministic, formula present, auditable) and `Judged` (analyst allocation, signed, sum-checked, explicitly non-causal). Add a `waterfall_sum_check` mode to `fact_base_audit.py` that parses the decomposition fact and verifies `Σ weights ≈ realized_move` within tolerance, failing the build if not. This would turn a prose commitment into a mechanical gate.

---

### H-3. Segment maps carry a staleness risk that the schema acknowledges but the workflow does not fail-safe against

**Locations:** `bigtech-equity-research/SKILL.md` lines 48–52 (“Respect the segment map’s vintage. Check `last_verified_against_filing` against the filing you are actually using”); `bigtech-equity-research/reference/segment-maps.md` (not fully fetched, but referenced as versioned); `bigtech-equity-research/SKILL.md` lines 101–104 (definition-of-done: “the segment map’s `last_verified_against_filing` is not older than the filing used”).

**Evidence:** The skills correctly identify that segment structures change (e.g., Alphabet’s reclassification of Google Cloud, Meta’s segment reporting shifts) and that a stale map “silently breaks the tie-out” (line 51). But the control is **advisory**, not enforcing: the analyst is told to check the vintage, and the definition-of-done checklist asks whether it was checked, but no script compares the filing date to the map’s `last_verified_against_filing` and blocks the build. In an agentic workflow, an LLM under time pressure could skip the manual comparison and produce a segment variance table against an obsolete structure.

**Impact:** Segment attribution is the analytical core of `bigtech-equity-research` (Phase 3, lines 40–47 of `reference/methodology.md`). A stale segment map produces a **confidently wrong** variance table that passes the numeric audit (because the numbers match the fact base) but misattributes the cause. This is the most insidious failure mode: the gate passes, the conclusion is wrong.

**Severity:** High. **Confidence:** Reasoned (the schema could enforce this; the workflow does not).

**Recommended fix:** Make the segment map a **machine-readable structured file** (JSON) with `last_verified_against_filing_date` and `filing_accession_number`. Extend `quant_helpers.py` or add a `segment_map_check.py` that takes the filing’s period/accession as input and raises if the map’s vintage is older. Wire this into the definition-of-done gate so the build fails, not just warns.

---

### H-4. The three skills share a doctrine but differ in verification depth — the lightweight variant can inherit the flagship’s credibility without its gates

**Locations:** `big-tech-earnings-postmortem/SKILL.md` lines 6–10 (“lite bundled audits instead of the flagship’s machine-checked fact base”); lines 30–38 (standalone structure: only `note_audit.py` and `note_overflow_audit.mjs`, no `fact_base_audit.py`, no `quant_helpers.py`). `bigtech-equity-research/SKILL.md` lines 9–13 (“bundled lite delivery audits (placeholder, disclosure, render gates)”).

**Evidence:** The postmortem skill executes the same canonical framework as the flagship (`postmortem-framework.md` lines 3–12) but ships **without the fact-base audit** and **without the arithmetic helper**. It relies on “compute, don’t recall” (lines 52–57) but does not bundle `quant_helpers.py`; it says “a scratch script, the sibling skill’s `quant_helpers.py`, or any executed tool” — meaning an agent using the postmortem in isolation must either hand-code arithmetic (violating the skill’s own rule) or skip the helper and risk in-context errors. The lite audit (`note_audit.py`) checks placeholders and disclosure needles but does **not** verify that numbers on the note match a fact base, because there is no fact base.

**Impact:** A PM reading a postmortem note cannot distinguish it from a flagship note at the evidentiary level, yet the postmortem’s gate does not enforce number-to-source traceability. The “lite” label is honest in the SKILL.md, but the delivered artifact — a single-file HTML note with confidence tags and a verification-status line — may look indistinguishable to a non-expert reader. This is a **credibility spillover risk**: the family’s strongest member lends reputational cover to its weakest gate.

**Severity:** High. **Confidence:** Verified.

**Recommended fix:** Either (a) bundle a minimal `fact_base_lite.json` and a `fact_base_lite_audit.py` (placeholder + number-to-source check only) in the postmortem skill, so even the lightweight variant has a machine-checked number registry; or (b) make the verification-status line explicitly state “no fact-base audit performed — numbers verified by human review only,” so the evidentiary gap is visible on the artifact itself. The second option is acceptable but weaker; the first is preferable.

---

## Medium Findings

### M-1. `fact_base_audit.py`’s reverse-check is opt-in, and the default posture leaves unverified numbers unflagged

**Location:** `fact_base_audit.py` lines 13–15, 25–27.

**Evidence:** Numbers found on slides but absent from the fact base are reported as “unverified candidates — a to-review list, not automatic failures” unless `--fail-on-unverified` is passed. The script’s author justifies this (page furniture, years, section numbers), which is reasonable. But in a production IC workflow, an unflagged unverified number is a **latent error**. The default should be strict for decision-critical slides (executive summary, root-cause decomposition) and lenient for furniture. A blanket opt-in strictness means the path of least resistance is the weaker gate.

**Severity:** Medium. **Confidence:** Verified.

**Recommended fix:** Add a `--strict-pages` argument that makes the reverse-check fail for a named list of decision-critical slide IDs while remaining advisory elsewhere. The fact-base schema already has `decision_critical`; extend it to slide-level scoping.

---

### M-2. Disclosure needles are a checklist, not a semantic verification

**Location:** `note_audit.py` (referenced at line 33 of the postmortem SKILL.md; `assets/checks.json` defines needles). The flagship’s `fact_base_audit.py` also has a “disclosure needle” concept (lines 18–19, method-page check).

**Evidence:** The lite audit enforces “disclosure needles” — specific strings that must appear (disclaimer, verification-status line, “Reasoned allocation” label, beta-window disclosure, Data-Gap Ledger presence). This is a **presence check**, not a **correctness check**. A note could include the string “Reasoned allocation — not a measured decomposition” in a footer while the body presents the waterfall as a measured decomposition. The needle passes; the disclosure is inert. Real compliance review requires the disclosure to be **functionally coupled** to the content it qualifies — e.g., the label must appear on the same slide as the waterfall, not just somewhere in the document.

**Severity:** Medium. **Confidence:** Reasoned.

**Recommended fix:** Extend the needle specification to support **scoped needles**: a needle that must appear within N characters of a target token, or on the same slide as a matching pattern. This moves from checklist compliance to contextual disclosure.

---

### M-3. “Options implied move” is used as a positioning proxy without sufficient statistical caveats

**Locations:** `bigtech-equity-research/reference/formulas.md` lines 26–28; `bigtech-equity-research/reference/methodology.md` lines 33–37.

**Evidence:** The formula `implied_move ≈ ATM_straddle_price / spot` is standard, and the interpretation (realized ≈ implied → positioned; realized ≫ implied → surprise) is directionally correct. But the skills do not disclose the **model dependence**: the ATM straddle price embeds a volatility risk premium (IV > realized on average), so “realized ≈ implied” may reflect a normal vol risk premium rather than genuine positioning. The `surprise_ratio = |realized| / implied` is a useful heuristic, but it is not a statistical test and does not account for event-specific variance. A rigorous quant note would state the historical realized-vs-implied relationship for the name and the sample used to calibrate “≈” vs “≫.”

**Severity:** Medium. **Confidence:** Reasoned.

**Recommended fix:** Add a `implied_move_context` field to the fact-base schema and require the note to state the historical average `realized/implied` ratio for the name over a disclosed window, or explicitly tag the interpretation `Assumed` (heuristic). The `sourcing-and-confidence.md` taxonomy already has the right vocabulary; it just is not applied to this specific inference.

---

### M-4. No position, holdings, or mandate disclosure — the buy-side IC memo standard requires it

**Location:** All three SKILL.md files; `sourcing-and-confidence.md` lines 26–31.

**Evidence:** The skills target a “portfolio-manager investment-committee audience” (line 26 of the flagship SKILL.md) and produce IC-ready decks. Yet they contain no mechanism for disclosing whether the fund holds the stock, whether the note is being written to support an existing position, or whether the author has a mandate constraint (e.g., cannot short, cannot hold >5%). IC-memo best practices (search results 5 and 6) emphasize separating “verified facts, external estimates, internal assumptions and judgement” and disclosing conflicts. The skills do the first well; they do the second not at all.

**Severity:** Medium. **Confidence:** Verified.

**Recommended fix:** Add an optional `mandate_context` block to the fact-base schema and a corresponding disclosure section in the template: `fund_position` (long/short/none), `position_size_bucket`, `mandate_constraint`, `author_conflict`. The audit needle can check for presence when the `audience` is IC.

---

### M-5. Render gate (`note_overflow_audit.mjs`) checks layout overflow but not accessibility conformance beyond the template’s claims

**Locations:** `bigtech-equity-research/SKILL.md` lines 111–113; `templates/report-structure.md` lines 3–5 (“WCAG-AA contrast. Print-friendly”).

**Evidence:** The template claims WCAG-AA, but the render gate checks **overflow**, not contrast ratios, keyboard operability, semantic heading hierarchy, or focus states. The skills’ parent document (the coding-agent spec, Section 16) mandates WCAG 2.2 AA for user-facing UI, but the equity-research skills’ own gate does not operationalize it. A note could pass the render gate while failing accessibility conformance. This is a **gap between claimed and enforced quality**.

**Severity:** Medium. **Confidence:** Reasoned.

**Recommended fix:** Extend `note_overflow_audit.mjs` (or add a sibling `a11y_audit.mjs`) to run axe-core or equivalent against the rendered HTML and fail on WCAG-AA violations. At minimum, check contrast, heading order, and image alt text.

---

## Low Findings

### L-1. Version mismatch across the family (`bigtech-equity-research` v1.2.0 vs the siblings’ v1.3.0) — the consistency test should catch this, but the version does not reflect doctrinal equivalence

The equity-research skill is a version behind the other two. The repository’s `test_repo_consistency.py` guards framework wiring (per the postmortem SKILL.md line 29), but the version number suggests it may have missed the latest hardening pass. If the doctrinal content is equivalent, the version should be bumped; if it is not, the inconsistency should be documented.

### L-2. Redundant methodology restatement across `big-tech-earnings-postmortem` and `analyzing-us-bigtech-stocks/references/postmortem-framework.md`

The postmortem SKILL.md reproduces the framework (lines 112–141) while declaring the canonical version lives in the flagship’s references (lines 22–29). This is a deliberate standalone-deployment choice, but duplication creates drift risk. The consistency test mitigates it; a generated-from-canonical build step would be stronger.

### L-3. `quant_helpers.py` covers delta, excess return, capex/OCF, OCF shortfall, and PT cuts — but not segment variance or waterfall sum-check

The helper is well-scoped and its `abnormal_return` beta-window enforcement (lines 21–35) is exemplary. It does not cover segment-level QoQ/YoY variance or the waterfall sum consistency that the skills’ own doctrine demands. Adding these would close the gap between the helper’s coverage and the methodology’s claims.

---

## Informational: What the Skills Do Exceptionally Well

These are not findings but comparative strengths worth naming, because they exceed common sell-side practice:

1. **The confidence taxonomy is mechanically coupled to the fact base.** `Verified` requires ≥2 independent sources *in the fact-base record*; `Assumed` facts must appear on the method page. This is a **schema-level** control, not a prose suggestion. Most sell-side notes have a disclosure page; these skills have a data model.

2. **“Compute, don’t recall” is enforced in code.** `quant_helpers.py` refuses to compute a beta-adjusted excess return without a `beta_window` (lines 21–35). This is a rare example of a methodology rule implemented as a runtime constraint rather than a style guideline.

3. **The two-axis driver classification (durability × evidentiary basis) is a genuinely useful analytical innovation.** It forces the analyst to separate “structural” from “mechanical” and “disclosed” from “inferred,” which is precisely the discipline an IC needs to distinguish a thesis-changing event from a positioning unwind.

4. **The elimination discipline is institutional-grade.** Requiring at least one explicitly rejected hypothesis with its falsifying fact (postmortem SKILL.md lines 136–141) is a control against confirmation bias that many human analysts never apply.

5. **The fact-base schema’s `decision_critical` concept is elegant.** It concentrates the double-sourcing burden on the 5–15 facts the verdict actually turns on, rather than requiring exhaustive cross-checking of every number — a pragmatic allocation of evidentiary effort.

---

## Comparison and Verdict

| Dimension | `analyzing-us-bigtech-stocks` | `big-tech-earnings-postmortem` | `bigtech-equity-research` |
|---|---|---|---|
| **Analytical depth** | Highest (full 0–10 pipeline, hypothesis tree, GAAP bridge, amplifiers) | Medium (compressed 7-step workflow, no fact base) | High (7-phase, segment deep-dive, options math) |
| **Verification rigor** | Highest (fact-base audit, strict modes, cross-check enforcement) | Lite (placeholder + disclosure needles only; no number-to-source audit) | Medium-High (lite audits + `quant_helpers.py`, but no fact-base audit) |
| **Regulatory readiness** | Low (internal-note framing; no certification/conflict module) | Low (same) | Low (same) |
| **Provenance/audit trail** | Point-in-time check, no immutable chain | Point-in-time check, no immutable chain | Point-in-time check, no immutable chain |
| **Quantitative transparency** | High (formulas shown, derived facts labeled) | Medium (arithmetic rule, no bundled helper) | Highest (`quant_helpers.py`, formula reference, beta-window enforcement) |
| **Segment/accounting fidelity** | High (GAAP bridge, fact-base schema) | Medium (GAAP vs non-GAAP split) | High (ASC 280 segment maps, staleness control) |
| **IC-memo suitability** | High evidentiary quality, low conflict disclosure | Medium evidentiary quality, low conflict disclosure | High analytical quality, low conflict disclosure |

**Verdict:** The family is **analytically and epistemically superior to typical LLM-generated equity research** and **materially stronger than many junior sell-side work products** in its treatment of sourcing, confidence, and falsification. It is **not yet at the standard of a major investment bank’s published research** because it lacks the regulatory infrastructure (analyst certification, conflict disclosure, supervisory approval) and the provenance infrastructure (immutable audit chain) that define institutional-grade research in a regulated context. It is **closer to buy-side IC-memo standards**, where the primary obligation is evidentiary rigor rather than public-distribution compliance — but even there, the absence of position/mandate disclosure and the lightweight variant’s verification gap are material.

The single highest-leverage improvement is **C-2 (provenance sealing)**: it is a technical control that would make every other gate defensible. The second is **H-1 (consensus sourcing enforcement)**: it would harden the root-cause input that every delta depends on. The third is **C-1 (conflict/certification module)**: it would determine whether these skills can be used inside a regulated entity at all.

---

**Verification ledger (per Section 13 of the governing spec):**

| Claim | Method | Result |
|---|---|---|
| SKILL.md contents | Fetched raw files, read full text | Verified |
| Reference docs (`postmortem-framework.md`, `methodology.md`, `sourcing-and-confidence.md`, `formulas.md`) | Fetched and read | Verified |
| Script behavior (`fact_base_audit.py`, `quant_helpers.py`) | Read source; did not execute | Reasoned (code inspection) |
| Repository consistency test existence | Referenced in SKILL.md; not independently fetched | Assumed (referenced but not verified) |
| Regulatory standards (Reg AC, FINRA 2241, MiFID II, Rule 17a-4) | Web search; primary sources surfaced | Verified (search results) |
| IC-memo best practices | Web search; multiple sources | Reasoned |
| Absence of conflict/provenance controls | Exhaustive scan of all fetched files | Verified (no such controls found) |

**What could not be verified:** The actual `tests/test_repo_consistency.py` content; the `segment-maps.md` content beyond the SKILL.md description; whether the `note_audit.py` needle implementation includes scoped matching (the SKILL.md says “needles,” not “scoped needles”); whether any external compliance wrapper exists outside the three skill folders. These would require cloning the repository and inspecting the full tree.

---

## Review of the Alternative Comparative Report

This document validates the alternative report's six findings against the repository evidence, evaluates its methodology and framing, and compares it head-to-head with my prior audit. Where the alternative is stronger, I say so explicitly; where it over-credits or misses, I give evidence.

---

## Part A — Validation of the Six Findings

| # | Alternative Finding | Severity (theirs) | My assessment | Evidence check |
|---|---|---|---|---|
| 1 | Consensus sourcing variance (T2-only sufficient) | High | **Agree — substantively correct, and it converges with my H-1.** The alternative adds a useful operational detail I under-specified: news wires often report *rounded* or *median* consensus, not mean, and may be stale by weeks. My report framed this as a schema gap (`consensus_vintage`, `consensus_source_tier`); the alternative frames it as a desk-practice failure. Both are valid; the alternative's framing is more concrete about *why* T2 is insufficient. | Verified in skill text (T2 "may support: Consensus, surprise framing"). The "Verified (Standard institutional desk practice)" tag is a **taxonomy misuse** — it tags the *fix* as verified, not the *finding*. Under the skills' own taxonomy (`sourcing-and-confidence.md`), the finding is "Verified" (observed in text); the practice claim is "Reasoned." Minor calibration error. |
| 2 | Beta estimation window has no canonical default | High | **Agree — and this is a genuine miss in my report.** I noted that `quant_helpers.abnormal_return` *requires* a window (my report, H-2 context and L-3), but I did not flag that the skill provides no canonical *default*. The alternative is right: requiring disclosure without defining a default makes abnormal returns non-comparable across runs. This is a real, sharp catch. | Reasoned from the skill text and helper description; I did not independently fetch `quant_helpers.py` line-by-line. The claim is consistent with the skill's own wording ("estimation window disclosed — refuses to run without it"). |
| 3 | Static segment maps will go stale | Medium (theirs) vs High (mine) | **Partially agree on severity; agree on the mechanism.** The alternative's recommended fix — dynamically extract the segment map from the current 10-Q/10-K segment footnote, using the static file only as a baseline expectation — is **better than my fix** in one dimension: it eliminates staleness at the source rather than detecting it. However, dynamic LLM extraction of a footnote introduces a *new* hallucination surface unless the extraction is itself audited (a point the alternative does not address). I maintain **High** because a stale map produces a confidently wrong variance table that *passes the numeric gate* — the most insidious failure mode. The alternative's Medium underweights this. | Verified that the control is advisory (my H-3). The alternative's fix is sound in principle but incomplete without an extraction audit. |
| 4 | Options-implied move sourced from news articles, not computed | Medium | **Agree with nuance — and this is a complementary angle I missed.** My M-3 flagged the *statistical* caveat (vol risk premium inflates implied move; `realized ≈ implied` may not mean "positioned"). The alternative flags the *sourcing* failure (news quotes stale/rounded/mid figures rather than T-1 ATM straddle close). Both are valid and non-overlapping. One correction: the alternative attributes this to both the flagship Phase 2 *and* `bigtech-equity-research` Step 2 — but the equity-research skill *does* define the formula (`implied_move ≈ ATM_straddle_price / spot` in `formulas.md`). The sourcing critique is strongest for the flagship and postmortem; it is weaker for equity-research, where the gap is input provenance, not absence of a formula. The alternative slightly overgeneralizes across the family. | Verified that the flagship says "only if you have a source"; the formula exists in equity-research. |
| 5 | Peer basket selection is subjective | Medium | **Agree — and this is a complete miss in my report.** The postmortem requires "2–4 closest peers" with no selection criteria. An agent could cherry-pick. My audit did not cover peer selection at all. This is a legitimate finding, correctly rated Medium. | Reasoned from the postmortem Step 4 text. No selection criteria are specified. |
| 6 | FCF ex-SBC should be a mandatory reconciliation row | Low | **Partially agree — the finding is slightly overstated.** The postmortem *does* say "FCF that ignores SBC overstates cash generation" (Step 2) — so the skill is not ignorant of the issue. The gap is that SBC is left as an *optional* add-on rather than a mandatory reconciliation row. The alternative's recommendation (mandatory FCF vs FCF-ex-SBC row for all mega-cap tech) is reasonable desk practice. Low severity is appropriate. | Verified that the skill mentions SBC but does not mandate the reconciliation row. |

**Summary of Part A:** Of six findings, four are solid (1, 2, 5, 6-partial), one is solid-but-mis-rated (3), and one is solid-but-overgeneralized (4). The alternative caught **three things I missed entirely** (beta default, peer selection, FCF-ex-SBC row) and added a useful operational angle on consensus and options sourcing. That is a material contribution, not a minor one.

---

## Part B — Critical Evaluation of the Alternative's Methodology and Framing

### B-1. The extraction method is a disclosed limitation but also a confidence risk

The alternative states it could not `git clone` and extracted from the "live GitHub web interface." This is honest and better than silently pretending to clone. But it has two consequences the report does not acknowledge:

- **Rendered-markdown truncation risk.** The GitHub web UI renders markdown and may collapse or truncate long files (the flagship SKILL.md is ~301 lines, the postmortem ~290). Structural citations ("Hard Rule 03," "Step 1 Source Tiers") are likely reliable; line-level citations are not. The alternative wisely avoids line numbers, but it also does not disclose a line-level verification ledger — so the reader cannot tell whether every file was read in full. The governing spec requires reading files **in full, never from partial or truncated views** (Section 6). The alternative's method does not establish that this was done.
- **Code-file rendering.** `quant_helpers.py` and `fact_base_audit.py` are Python; the web UI renders them with line numbers but may still truncate. The alternative's beta-window finding cites the helper by *function name*, not line, which is structurally verifiable. Good instinct — but the report should state that code was inspected structurally, not line-by-line.

**Verdict:** The method is acceptable for a structural audit but should carry an explicit confidence discount. My report disclosed its own limitation (scripts read but not executed) and produced a verification ledger; the alternative does not.

### B-2. The confidence tags describe the *fix*, not the *finding* — a taxonomy error the skills themselves would flag

Finding 1 is tagged "Verified (Standard institutional desk practice)." Finding 6 is tagged "Verified (Industry standard practice for mega-cap tech)." Under the skills' own taxonomy, `Verified` means "executed and observed directly" about the *claim*. Here the tag is attached to the *recommended practice*, not the finding. The findings themselves (T2-only consensus permitted; FCF-ex-SBC optional) are verifiable from the text; the practice claims are `Reasoned`. This is a small but revealing inconsistency: the alternative report does not apply the skills' own confidence discipline to its own claims. Given that epistemic discipline is the family's signature strength, this is worth flagging as a meta-observation.

### B-3. "Excellent" regulatory posture is over-credited — the central disagreement between the two reports

This is the most consequential divergence. The alternative rates:

- Regulatory & Compliance Posture — **Excellent**
- Epistemic Discipline & Auditability — **Excellent**
- Arithmetic & Execution Integrity — **Excellent**

And concludes: *"Once resolved, this skill family meets the rigorous evidentiary and compliance standards expected by institutional portfolio managers and investment committees."*

I rate the same dimensions:

- Regulatory posture — **Critical gap** (no conflict/position disclosure, no certification module, no supervisory approval; the disclaimer is a scoping choice, not a compliance control).
- Auditability — **Critical gap** (point-in-time check, no immutable provenance chain, no hash/timestamp linking delivered HTML to audited fact base).
- Arithmetic integrity — **Strong but soft in two places** (`fact_base_audit.py` reverse-check is opt-in; waterfall sum consistency is not mechanically enforced).

**Who is right?** Both positions are defensible, but the alternative's "Excellent" is less calibrated.

- The alternative's implicit theory: the skills explicitly disclaim sell-side status ("no rating, no PT, no Reg AC"), therefore they are not research reports, therefore the regulatory regime does not apply. This is a coherent *product-scoping* argument.
- My theory: research-report status is **content- and distribution-based**, not self-labeled. A 12–16 page IC deck that explains why a stock moved 12% and computes a forward-multiple band is functionally research-adjacent; IC distribution triggers fiduciary and CFA Standard I(B) obligations even internally; and the *complete absence* of any position/conflict disclosure mechanism is a gap regardless of regime. "Excellent" overstates a posture that is really "adequately scoped for narrow internal use, with material gaps for broader institutional use."

The alternative's own finding #1 (consensus) and #3 (segment maps) are *correctness* findings. It has **no Critical findings at all** — which, for a suite that produces IC decks and PT-cut analysis, is an under-weighting. A report that finds six issues and rates the compliance posture "Excellent" is not applying the same severity lens to governance that it applies to quant inputs.

### B-4. The report is quant-desk-shaped, not audit-shaped — which is a lens, not a flaw

The alternative's six findings are: consensus, beta, segment maps, options, peers, FCF. That is a **quantitative-review lens** — the things a quant desk would challenge. My findings include those plus provenance, regulatory certification, disclosure-needle semantics, lite-variant credibility spillover, reverse-check defaults, and a11y gates — an **audit/governance lens**. These are complementary, not contradictory. The alternative is *sharper* on quant inputs; mine is *broader* on controls. Neither subsumes the other.

---

## Part C — Head-to-Head Coverage Comparison

| Finding | Alternative | My audit | Net |
|---|---|---|---|
| Consensus sourcing | High (T2 rounded/stale) | High (schema lacks vintage/tier fields) | **Both — complementary** |
| Beta window default | **High (caught)** | Missed | **Alternative wins** |
| Segment map staleness | Medium | High | **Both — severity dispute; alt fix better, my severity better** |
| Options implied move | Medium (sourcing) | Medium (statistical caveat) | **Both — complementary** |
| Peer basket selection | **Medium (caught)** | Missed | **Alternative wins** |
| FCF ex-SBC mandatory row | **Low (caught)** | Missed | **Alternative wins (partial)** |
| Regulatory certification / conflict disclosure | Rated Excellent | Critical | **Mine — alternative over-credits** |
| Immutable provenance chain | Not addressed | Critical | **Mine** |
| "Reasoned" overload / waterfall sum-check | Not addressed | High | **Mine** |
| Lite-variant credibility spillover (postmortem lacks fact base) | Not addressed | High | **Mine** |
| Reverse-check opt-in default | Not addressed | Medium | **Mine** |
| Disclosure needles as presence-check, not semantic | Not addressed | Medium | **Mine** |
| Position/mandate disclosure for IC | Not addressed | Medium | **Mine** |
| WCAG gate scope | Not addressed | Medium | **Mine** |
| MNPI / Reg FD hygiene as a strength | **Credited** | Under-emphasized | **Alternative wins (strength ID)** |
| "Compute, don't recall" as strongest control | **Credited** | Credited | **Tie — both correct** |
| Valuation boundary as strength | **Credited** | Credited | **Tie** |

**Tally of unique catches:** Alternative — 3 (beta, peers, FCF) plus 1 strength (MNPI). Mine — 7 (regulatory, provenance, Reasoned/waterfall, lite-variant spillover, reverse-check, disclosure needles, position/mandate, plus a11y = 8 if counted separately). The alternative's catches are **quant-input** gaps; mine are **control/governance** gaps. A complete audit needs both.

---

## Part D — Reconciled Assessment

**Merged finding set (union of both reports), ordered by severity:**

| Severity | Findings |
|---|---|
| **Critical** | C-1 Regulatory/certification/conflict disclosure absent (mine); C-2 No immutable provenance chain (mine) |
| **High** | H-1 Consensus sourcing unenforced (both); H-2 Beta window has no canonical default (alternative); H-3 Segment map staleness — advisory, not fail-safe (both; severity High per my reasoning); H-4 "Reasoned" overload / waterfall sum not mechanically checked (mine); H-5 Lite variant inherits family credibility without flagship gates (mine) |
| **Medium** | M-1 Reverse-check opt-in default (mine); M-2 Disclosure needles are presence-only (mine); M-3 Options implied move — sourcing + vol-risk-premium caveat (both, merged); M-4 Peer basket subjectivity (alternative); M-5 Position/mandate disclosure for IC (mine); M-6 WCAG gate scope (mine) |
| **Low** | L-1 FCF-ex-SBC mandatory reconciliation row (alternative); L-2 Version mismatch v1.2.0 vs v1.3.0; L-3 Framework restatement drift risk; L-4 `quant_helpers` coverage gap (segment variance, waterfall sum) |

**Reconciled verdict:**

- The alternative is **more rigorous on quantitative inputs** (beta default, peer selection, FCF definition, consensus vintage, options sourcing). These are exactly the questions a quant desk or a PM's risk team would raise, and three of them are genuine gaps I missed.
- My audit is **more rigorous on governance and provenance** (regulatory posture, immutable audit chain, schema-level controls, family-tier credibility spillover). The alternative's "Excellent" compliance rating is an over-credit that a compliance reviewer would push back on.
- **Neither report is complete alone.** The union is a materially stronger audit than either. If I had to choose one for an IC pre-read, I would take the alternative's quant findings plus my provenance and conflict-disclosure findings; if I had to choose one for a compliance sign-off, I would take mine.
- **The alternative's conclusion is over-stated.** "Once resolved, this skill family meets the rigorous evidentiary and compliance standards expected by institutional portfolio managers" is not supported even by its own six fixes — because those fixes do not touch conflict/position disclosure, provenance, or the lite-variant gate gap. A fairer conclusion: *"The family is analytically institutional-grade on quant inputs and evidentiary discipline; it is not yet compliance- or provenance-grade for regulated distribution, and the lightweight variant's gate is materially weaker than the flagship's."*

**One correction to my own prior report, in fairness:** I should have caught the beta-window default gap (H-2 above) and the peer-selection subjectivity (M-4 above). The alternative's findings are correct on both. I also under-emphasized the MNPI/Reg FD hygiene mandate as a strength; the alternative is right to credit it. I maintain my Critical ratings on regulatory posture and provenance, and my High rating on segment-map staleness, for the reasons given in B-3 and A-3.

---

## Verification Ledger

| Claim | Method | Result |
|---|---|---|
| Alternative's six findings map to repo text | Cross-checked against my prior file reads | Verified for findings 1, 3, 4, 5, 6; Reasoned for finding 2 (helper not line-fetched) |
| Alternative extracted via GitHub web UI | Self-reported; not independently verifiable | Assumed |
| Confidence-tag misuse in alternative | Read the tags against the skills' own taxonomy | Verified |
| "Excellent" regulatory rating is over-credited | Compared alternative's rating to absence of conflict/provenance controls in fetched files | Verified (controls absent); Reasoned (severity judgment) |
| My missed findings (beta, peers, FCF) | Re-read the relevant skill text | Verified — alternative is correct on beta and peers; partially correct on FCF |
| Merged severity table | Union of both reports, re-ranked against Section 12 taxonomy | Reasoned |

**What could not be verified:** Whether the alternative actually read every file in full via the web UI; whether `quant_helpers.py` has a hidden default window not visible in the skill prose; whether any external compliance wrapper exists outside the three skill folders. These would require a local clone and full-tree inspection.
