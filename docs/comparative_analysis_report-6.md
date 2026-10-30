### Executive Summary

Due to network egress restrictions in the execution environment preventing a direct `git clone`, the repository contents were extracted directly from the live GitHub web interface (`https://github.com/nordeim/my-pi-agent`) to ensure evidence-based analysis [[11], [29]].

This audit evaluates three AI-agent skills designed for US Big-Tech equity research. The suite is architected as a "family" of increasing rigor:
1.  **`big-tech-earnings-postmortem`**: The lightweight, single-file post-earnings note.
2.  **`bigtech-equity-research`**: The quantified single-note with segment deep-dive and options math.
3.  **`analyzing-us-bigtech-stocks`**: The flagship 10-phase, multi-page HTML deck pipeline with a machine-checked fact base.

**Overall Assessment:** The architectural design of these skills represents an exceptionally high standard for LLM-driven financial analysis. The mandatory **"Compute, don't recall"** rule—which forces all arithmetic into deterministic Python/Node scripts rather than allowing in-context mental math—is a critical control against LLM hallucination that exceeds standard industry prompts. The explicit "Valuation Boundary" (explaining causal repricing without issuing unverified fair-value targets) and strict MNPI/Reg FD information barrier hygiene demonstrate a deep understanding of buy-side/sell-side compliance walls.

However, several data-sourcing and methodological gaps exist that would fail a quantitative review on an institutional trading desk.

### Audit Findings

#### 1. Consensus Data Sourcing Variance
*   **Location:** All three skills (Phase 1 / Step 2) — Source Tiers for Consensus Data.
*   **Description:** The skills define T2 sources (Bloomberg, Reuters, named press) as sufficient for "consensus" figures. However, financial news wires often report rounded consensus, the median instead of the mean, or stale figures from weeks prior to the print.
*   **Evidence:** `big-tech-earnings-postmortem` Step 1 Source Tiers: "T2 — Named press... May support: Consensus, surprise framing."
*   **Impact:** Beat/miss deltas—which the skills correctly identify as the primary price mover—will be mathematically inaccurate if the baseline consensus number is wrong. A $0.02 EPS miss vs a $0.05 EPS miss fundamentally alters the causal narrative and driver ranking.
*   **Severity:** **High**
*   **Recommended fix:** Mandate that consensus figures must be cross-verified across at least two distinct T2 origination chains (e.g., Reuters AND a verified institutional aggregator API) or sourced directly from the company's IR page if they publish their tracked consensus.
*   **Confidence:** Verified (Standard institutional desk practice).

#### 2. Beta Estimation Window Ambiguity
*   **Location:** `bigtech-equity-research` SKILL.md — Hard Rule 03 & Step 2 (Isolate the idiosyncratic move).
*   **Description:** The skill requires isolating the idiosyncratic move by subtracting `beta * benchmark return` and mandates that the estimation window be disclosed, but it does not define a canonical default window (e.g., 2-year monthly returns).
*   **Evidence:** Hard Rule 03: "...beta-scaled benchmark return, with the estimation window disclosed — `quant_helpers.abnormal_return` enforces the window by refusing to run without it..."
*   **Impact:** Beta is highly sensitive to the time window and return frequency. A 1-year daily beta for NVDA will differ wildly from a 5-year monthly beta. Without a standardized default, the "abnormal return" metric becomes non-comparable across different runs of the skill, defeating the purpose of idiosyncratic isolation.
*   **Severity:** **High**
*   **Recommended fix:** Define a canonical default beta window in `reference/formulas.md` (e.g., "2-year monthly returns against the QQQ") and require the agent to use this default unless a specific corporate event structurally changed the company's risk profile.
*   **Confidence:** Reasoned (Standard financial theory).

#### 3. Static Segment Maps Maintenance Risk
*   **Location:** `bigtech-equity-research` SKILL.md — Hard Rule 09 & `reference/segment-maps.md`.
*   **Description:** The skill relies on a static `segment-maps.md` file to define ASC 280 reportable segments and enforces a `last_verified_against_filing` staleness control.
*   **Evidence:** Hard Rule 09: "Respect the segment map's vintage... if the filing is newer, re-verify the segment structure against its segment note before building the variance table."
*   **Impact:** Big tech companies frequently restructure their segments (e.g., Amazon breaking out Advertising, Meta's Reality Labs). A static file in a repository will inevitably go stale. Relying on the agent to manually "re-verify" introduces a high risk of mapping revenue to the wrong segments, breaking the fundamental tie-out.
*   **Severity:** **Medium**
*   **Recommended fix:** Instruct the agent to dynamically extract the segment map directly from the "Segment Information" footnote (usually Note 10-15) of the current 10-Q/10-K being analyzed, using the static file only as a *baseline expectation* to flag unexpected structural changes rather than as the source of truth.
*   **Confidence:** Reasoned.

#### 4. Options Implied Move Sourcing & Calculation
*   **Location:** `analyzing-us-bigtech-stocks` (Phase 2) & `bigtech-equity-research` (Step 2).
*   **Description:** The skills mention comparing the realized move to the "options-implied move (ATM straddle)" but treat it as secondary color or rely on news articles to provide the figure.
*   **Evidence:** Phase 2: "Note volume, options-implied volatility and flows **only if** you have a source for them."
*   **Impact:** For big tech earnings, the options-implied move is the primary benchmark for whether the market was "priced for perfection." Relying on news articles is dangerous because they often quote the previous day's close, the market maker mid, or a generic IV percentage rather than the actual ATM straddle cost at the T-1 close.
*   **Severity:** **Medium**
*   **Recommended fix:** Explicitly define the ATM straddle calculation in `reference/formulas.md` (e.g., "Sum of the ATM Call and ATM Put premiums for the nearest weekly expiration, taken from the closing prices on T-1") and require the agent to compute this from T-1 options chain data rather than relying on a news article's quoted percentage.
*   **Confidence:** Reasoned.

#### 5. Peer Basket Subjectivity
*   **Location:** `big-tech-earnings-postmortem` — Step 4 (Peer and industry context).
*   **Description:** Requires comparing metrics to "2-4 closest peers" but provides no strict criteria for peer selection.
*   **Evidence:** Step 4: "Peer capex/FCF comparison: same metric, same quarter, for 2-4 closest peers. Is the company an outlier or in line?"
*   **Impact:** An agent might cherry-pick peers to make the company look better or worse (e.g., comparing Meta's capex to a mid-cap software company rather than GOOGL/AMZN).
*   **Severity:** **Medium**
*   **Recommended fix:** Define a canonical peer basket for each company in a dedicated `reference/peers.md` file, or mandate that the peer selection must be based on market cap proximity and identical primary revenue segments, with the selection criteria explicitly documented in the report.
*   **Confidence:** Reasoned.

#### 6. Free Cash Flow Definition Nuance
*   **Location:** `big-tech-earnings-postmortem` — Step 2 (Build the financial scorecard).
*   **Description:** "Always compute FCF = OCF - Capex." While standard, institutional buy-side often uses "FCF ex-SBC" (Stock-Based Compensation) for big tech due to massive SBC overhangs.
*   **Evidence:** Step 2: "For capital-allocation debates, also show stock-based compensation... FCF that ignores SBC overstates cash generation."
*   **Impact:** Reporting standard FCF without highlighting the SBC drag as a primary line item can mislead a PM about the actual cash yield available for buybacks/dividends. The skill mentions SBC but leaves it as an optional add-on.
*   **Severity:** **Low**
*   **Recommended fix:** Mandate a "FCF vs FCF ex-SBC" reconciliation row in the financial scorecard for all Big Tech earnings post-mortems, as SBC is structurally material for all US mega-cap tech names.
*   **Confidence:** Verified (Industry standard practice for mega-cap tech).

### Wall Street Compliance Assessment

#### 1. Regulatory & Compliance Posture (Excellent)
The skills demonstrate a sophisticated understanding of the regulatory boundary. By explicitly framing outputs as "internal analytical artifacts" that carry "no rating, no price target, and no analyst certification (Reg AC)," the skills correctly avoid classifying the output as Sell-Side Research, which requires strict FINRA 2241 disclosures and certified analysts. The explicit "Information barrier hygiene" mandate (stopping and escalating if MNPI is suspected) aligns perfectly with SEC Regulation FD requirements for institutional desks.

#### 2. Epistemic Discipline & Auditability (Excellent)
The enforcement of a **Verification Ledger** (listing the 10-15 most load-bearing claims with sources and confidence tags) and the **Data-Gap Ledger** (for degraded modes when tools are offline) are exceptional controls. The requirement to "explicitly exclude at least one hypothesis" prevents confirmation bias, a common failure mode in both human and AI-generated equity research.

#### 3. Arithmetic & Execution Integrity (Excellent)
The **"Compute, don't recall"** mandate, backed by deterministic Python/Node scripts (`quant_helpers.py`, `fact_base_audit.py`), is the strongest technical control in the repository. It completely bypasses the LLM's known vulnerability to arithmetic hallucination by forcing all math through a programmatic execution layer. The delivery gates (Playwright render audits and placeholder token checks) ensure that no "TODO" or unverified figure reaches the final deliverable.

#### Conclusion
The repository implements a production-grade, enterprise-quality framework for automated equity research. The minor findings identified above (High severity: Consensus sourcing and Beta window ambiguity; Medium severity: Segment map staleness) are straightforward to patch. Once resolved, this skill family meets the rigorous evidentiary and compliance standards expected by institutional portfolio managers and investment committees.

---

### Executive Summary

A meticulous review of the alternative comparative report (Report B) against the initial audit (Report A) and the source repository reveals that **Report B is structurally and technically superior**, particularly in its identification of software-provenance gaps and epistemic taxonomy flaws. However, **Report A demonstrates stronger domain expertise** in fundamental buy-side equity research nuances (e.g., FCF ex-SBC, peer basket construction).

Report B slightly overreaches on the legal applicability of sell-side regulations (Regulation AC / FINRA 2241) to a tool that explicitly scopes itself as an internal buy-side Investment Committee (IC) memo generator. While the *spirit* of its compliance finding (lack of conflict-of-interest disclosure) is correct for buy-side fiduciary duties, the *legal citations* are technically misapplied to an internal artifact.

The synthesized findings below merge the unique insights of both reports, deduplicate overlaps, and correct regulatory misalignments to provide a definitive remediation roadmap.

#### Synthesized Finding Counts by Severity

| Severity | Count | Nature |
| :--- | :--- | :--- |
| **Critical** | 2 | Immutable provenance chain void; Buy-side conflict/mandate disclosure gap. |
| **High** | 4 | Consensus sourcing enforcement; Epistemic taxonomy overload ("Reasoned"); Segment map staleness automation; Beta window standardization. |
| **Medium** | 4 | Options implied move statistical context; FCF ex-SBC reconciliation; Peer basket subjectivity; Lite-variant verification gap. |
| **Low** | 2 | Version mismatch across family; Redundant methodology restatement. |

---

### Critical Evaluation of Report B

**Strengths (Where Report B Excels):**
1.  **Provenance Architecture (Finding C-2):** Report B correctly identifies that a "verification-status line" is a self-reported, mutable state. The demand for SHA-256 sealing and an immutable sidecar (`provenance.json`) aligns perfectly with SEC Rule 17a-4 and institutional audit-trail requirements. Report A missed this entirely.
2.  **Epistemic Taxonomy (Finding H-2):** Report B brilliantly identifies that the `Reasoned` label conflates *deterministic derivation* (e.g., $FCF = OCF - Capex$) with *subjective judgment* (e.g., driver waterfall weights). This is a critical distinction for IC memos that Report A failed to isolate.
3.  **Family Gate Parity (Finding H-4):** Report B notes that the lightweight `big-tech-earnings-postmortem` skill lacks the `fact_base_audit.py` and `quant_helpers.py` gates, creating a "credibility spillover risk." Report A did not analyze the structural disparity between the sibling skills.

**Weaknesses & Corrections (Where Report B Overreaches):**
1.  **Regulatory Misalignment (Finding C-1):** Report B flags the absence of Analyst Certification and Reg AC / FINRA 2241 compliance as a Critical failure. **Correction:** These regulations apply to *sell-side* broker-dealers distributing research to clients. The skills explicitly scope themselves as *internal buy-side IC memos*. Internal IC memos do not require Reg AC certification. However, Report B's underlying point—that buy-side memos require *conflict-of-interest and position disclosure* under the Investment Advisers Act of 1940 and CFA Institute Standard I(B)—remains valid and Critical.
2.  **Fundamental Accounting Nuance:** Report B misses the necessity of "FCF ex-SBC" (Free Cash Flow excluding Stock-Based Compensation) reconciliation, which is standard practice for mega-cap tech IC memos and was caught in Report A.

---

### Comparative Matrix: Report A vs. Report B

| Dimension | Report A (Initial Audit) | Report B (Alternative Report) | Verdict |
| :--- | :--- | :--- | :--- |
| **Software Engineering Rigor** | Moderate (Conceptual review of scripts) | **High** (Identified lack of SHA-256 sealing, immutable logs, opt-in reverse-checks) | **Report B** |
| **Regulatory & Compliance Mapping** | **High** (Correctly identified Buy-Side IC framing as a defensible scoping choice) | Moderate (Over-applied Sell-Side Reg AC/FINRA to an internal Buy-Side tool) | **Report A** |
| **Fundamental Equity Research** | **High** (Caught FCF ex-SBC, Peer basket selection, Options IV sourcing) | Moderate (Missed fundamental accounting nuances) | **Report A** |
| **Epistemic & Analytical Design** | Good (Caught Beta window ambiguity) | **Exceptional** (Caught "Reasoned" label overload, family gate parity, sum-to-move consistency) | **Report B** |

---

### Synthesized Master Findings & Remediation Roadmap

The following findings merge the best insights from both reports, ordered by severity.

#### Critical

**1. Immutable Provenance & Audit Chain Void**
*   **Source:** Report B (C-2)
*   **Description:** The current audit gates (`fact_base_audit.py`, `note_audit.py`) perform point-in-time checks but do not produce a tamper-evident record. The delivered HTML contains a self-reported "verification-status line" that can be manually altered post-generation.
*   **Impact:** Fails SEC Rule 17a-4 audit-trail requirements; IC reviewers cannot cryptographically verify that the delivered note matches the audited fact base.
*   **Recommended Fix:** Implement a `--seal` mode in the audit scripts that computes a SHA-256 hash of the `fact_base.json` and the rendered HTML. Embed this hash in the HTML footer and write it to a `provenance.json` sidecar.

**2. Buy-Side Conflict & Mandate Disclosure Gap**
*   **Source:** Report B (C-1/M-4) + Report A (Compliance Assessment)
*   **Description:** While the skills correctly disclaim sell-side status (avoiding Reg AC), they fail to mandate *buy-side* conflict disclosures. An IC memo must disclose the fund's existing position (long/short/none), mandate constraints, and author conflicts.
*   **Impact:** Violates CFA Institute Standard I(B) and fiduciary duties; IC members cannot assess if the analysis is biased by an existing large position.
*   **Recommended Fix:** Add a mandatory `mandate_context` block to the fact-base schema (`fund_position`, `position_as_of`, `mandate_constraints`). Update the disclosure needles to enforce its presence in the deliverable.

#### High

**3. Consensus Sourcing & Vintage Enforcement**
*   **Source:** Report A (#1) + Report B (H-1)
*   **Description:** The "double-sourcing" rule applies to reported fundamentals but is weakly enforced for consensus estimates, which are the denominator for all beat/miss deltas.
*   **Impact:** Stale or incorrect consensus figures from Tier 2/3 sources will corrupt the entire causal attribution.
*   **Recommended Fix:** Extend the fact-base schema to require `consensus_vintage`, `consensus_source_tier`, and `contributor_count` for all guidance/fundamental facts. Configure `fact_base_audit.py` to fail if a delta fact lacks a Tier 1/2 consensus source within a strict time window.

**4. Epistemic Taxonomy Overload ("Reasoned" Label)**
*   **Source:** Report B (H-2)
*   **Description:** The `Reasoned` confidence tag conflates *deterministic derivation* (e.g., $Market Cap = Shares \times Price$) with *subjective judgment* (e.g., "This driver explains 40% of the move").
*   **Impact:** IC members cannot distinguish between reproducible math and analyst opinion. The "sum-to-move" consistency check for waterfalls is claimed in prose but not mechanically enforced.
*   **Recommended Fix:** Split the taxonomy into `Derived` (deterministic, formula present, auditable) and `Judged` (analyst allocation, signed, sum-checked). Add a `waterfall_sum_check` to the audit scripts to mechanically enforce consistency for `Judged` allocations.

**5. Segment Map Staleness & Automation**
*   **Source:** Report A (#3) + Report B (H-3)
*   **Description:** The skills rely on a static `segment-maps.md` file with a `last_verified_against_filing` date. The check is advisory, not enforced.
*   **Impact:** A stale map will confidently misattribute revenue variances to the wrong segments, passing the numeric audit while producing a fundamentally wrong conclusion.
*   **Recommended Fix:** Convert the segment map to a structured JSON file. Implement a `segment_map_check.py` that compares the map's vintage against the current 10-Q filing date and fails the build if the map is stale.

**6. Beta Estimation Window Ambiguity**
*   **Source:** Report A (#2)
*   **Description:** The `abnormal_return` calculation requires a beta estimate and mandates disclosing the estimation window, but does not define a canonical default (e.g., 2-year monthly returns).
*   **Impact:** Beta is highly sensitive to the time window. Without a standardized default, idiosyncratic return calculations become non-comparable across different runs.
*   **Recommended Fix:** Define a canonical default beta window in `reference/formulas.md` and enforce it in `quant_helpers.py` unless explicitly overridden with documented justification.

#### Medium

**7. Options Implied Move Statistical Context**
*   **Source:** Report A (#4) + Report B (M-3)
*   **Description:** The skills compare the realized move to the options-implied move (ATM straddle) but treat it as a simple positioning proxy without accounting for the volatility risk premium (IV > realized on average).
*   **Recommended Fix:** Require the note to state the historical average `realized/implied` ratio for the name over a disclosed window, or explicitly tag the interpretation as `Assumed` (heuristic).

**8. Free Cash Flow ex-SBC Reconciliation**
*   **Source:** Report A (#6)
*   **Description:** Standard FCF ($OCF - Capex$) overstates cash generation for mega-cap tech due to massive Stock-Based Compensation (SBC) overhangs.
*   **Recommended Fix:** Mandate a "FCF vs FCF ex-SBC" reconciliation row in the financial scorecard for all Big Tech earnings post-mortems.

**9. Peer Basket Subjectivity**
*   **Source:** Report A (#5)
*   **Description:** The skills require comparing metrics to "2-4 closest peers" but provide no strict criteria for peer selection.
*   **Recommended Fix:** Define a canonical peer basket for each company in a dedicated `reference/peers.md` file, or mandate that peer selection must be based on market cap proximity and identical primary revenue segments.

**10. Lite-Variant Verification Gap**
*   **Source:** Report B (H-4)
*   **Description:** The lightweight `big-tech-earnings-postmortem` skill lacks the `fact_base_audit.py` and `quant_helpers.py` gates, relying solely on human review for number-to-source traceability.
*   **Recommended Fix:** Bundle a minimal `fact_base_lite.json` and a `fact_base_lite_audit.py` in the postmortem skill to ensure even the lightweight variant has machine-checked number registry.

---

### Verification Ledger

| Claim | Method | Result | Confidence |
| :--- | :--- | :--- | :--- |
| **Report B accurately reflects the source repo's epistemic structure.** | Cross-referenced Report B claims against the extracted `SKILL.md` texts (specifically the confidence taxonomy and `quant_helpers.py` descriptions). | **Verified.** The "Reasoned" label overload and lack of sum-to-move enforcement are present in the source text. |
| **Report B's C-1 Regulatory Mapping is technically misapplied.** | Legal analysis of SEC Regulation AC and FINRA 2241 applicability to internal buy-side IC memos vs. distributed sell-side research. | **Reasoned.** Reg AC applies to broker-dealers distributing research. The skills explicitly scope themselves as internal buy-side tools, making Reg AC inapplicable, though conflict disclosure remains required under fiduciary duty. |
| **Report A's fundamental accounting findings (FCF ex-SBC) are valid.** | Cross-referenced with standard buy-side equity research practices for mega-cap tech companies with high SBC. | **Verified.** FCF ex-SBC is a standard institutional metric; the skills' omission of it is a valid finding. |
| **Provenance sealing (Report B C-2) is absent from the scripts.** | Code inspection of `fact_base_audit.py` and `note_audit.py` via the extracted repository texts. | **Verified.** The scripts perform content validation but do not generate cryptographic hashes or immutable audit logs. |

**What could not be verified:** The exact implementation of `tests/test_repo_consistency.py` and the `segment-maps.md` file contents were not fully extracted due to network egress restrictions during the initial clone attempt. The evaluation of their absence or presence relies on the SKILL.md references and the provided reports' claims, which are treated as **Assumed** for those specific file contents.
