## Executive Summary

The three skills in this repository (`analyzing-us-bigtech-stocks`, `big-tech-earnings-postmortem`, `bigtech-equity-research`) represent an exceptionally high standard for automated financial research. They correctly implement the core tenets of institutional equity research: strict source tiering, separation of idiosyncratic from systematic risk, epistemic honesty (distinguishing reproducible math from analyst judgment), and automated compliance gates (Reg FD, Reg AC, CFA Standard I(B)).

However, a rigorous comparison against the highest standards of major investment banks reveals gaps in **temporal enforcement of Material Non-Public Information (MNPI) embargoes**, **volatility regime handling**, and **market microstructure attribution**. These gaps introduce regulatory and analytical risks that must be addressed before deployment in a live Investment Committee (IC) environment.

---

## Detailed Audit Findings

### 1. MNPI / Pre-Filing Web-Scrape Contamination Risk
- **Location:** All 3 Skills (`SKILL.md` Phase 1 / Step 1 / Workflow Phase 1).
- **Description:** The skills mandate T1 sourcing for fundamentals but lack a temporal enforcement mechanism. An LLM using web search tools can scrape a leak on social media or a financial blog minutes before the 8-K drops, tag it as "News" or "Consensus," and incorporate it into the fact base.
- **Evidence:** The source tiers table defines T1 (SEC/IR) and T2 (Reuters/Bloomberg), but the audit scripts (`fact_base_audit.py`, `fact_base_lite_audit.py`) check for `consensus_vintage` and cross-checks, not a hard temporal embargo against the official T1 filing timestamp.
- **Impact:** Severe regulatory risk. Documenting leaked earnings data in an IC memo prior to the public 8-K filing violates Reg FD principles and risks insider trading liability.
- **Severity:** High
- **Recommended fix:** Implement a `pre_filing_embargo` gate in the fact-base schema and audit scripts. If `meta.event_timestamp` is set, any non-T1 source with a `retrieved_at` time *before* the verified T1 filing time must be automatically flagged as `Unverifiable` and stripped from the fact base.
- **Confidence:** Reasoned

### 2. Static Beta Regime Assumption in Excess Return Calculation
- **Location:** `big-tech-earnings-postmortem` (Step 1) & `bigtech-equity-research` (Phase 2 / Hard Rule 3).
- **Description:** The "canonical default beta window (2-year monthly returns vs QQQ)" is hardcoded as the default for isolating idiosyncratic moves. Big Tech stocks experience massive volatility regime shifts (e.g., 2022 rate shocks, 2023 AI boom). A 24-month window heavily smooths these regime breaks.
- **Evidence:** `scripts/quant_helpers.py` applies the canonical window but lacks a diagnostic for correlation breakdown. The text allows an override "if the company's risk profile structurally changed," but delegates the detection of structural change entirely to the LLM without a quantitative trigger.
- **Impact:** The calculated "idiosyncratic shock" will be mathematically distorted. If the stock's correlation to the market has fundamentally broken down, applying an obsolete beta will attribute market-driven moves to company-specific failures.
- **Severity:** Medium
- **Recommended fix:** Enhance `scripts/quant_helpers.py` to output an `R_squared` and a `volatility_regime_flag`. If R² < 0.30 or if the trailing 3-month realized vol is > 2 standard deviations from the 2-year mean, the script should force the agent to explicitly justify the beta window or use a shorter (e.g., 6-month daily) window.
- **Confidence:** Reasoned

### 3. Survivorship & Corporate Action Blindness in Peer Baskets
- **Location:** `reference/peers.md` and Phase 4 (Peer Context) across all skills.
- **Description:** The skills rely on "canonical peer baskets" for cross-sectional analysis. There is no automated check for corporate actions (M&A, spin-offs, delistings) that may have occurred since the peer map was cached.
- **Evidence:** The peer basket is defined in `reference/peers.md` and used in the cross-section calculation, but no delivery gate verifies the constituent status of the basket against the exchange listing database or index membership API prior to computing the cross-section.
- **Impact:** Comparing a company's FCF yield to a peer basket that recently lost a distressed constituent (survivorship bias) will falsely inflate the peer group's average health, making the target company look worse than it is.
- **Severity:** Medium
- **Recommended fix:** Add a `corporate_action_check` to the delivery gates that verifies the constituent status of the canonical basket against an authoritative index or exchange API prior to computing the cross-section.
- **Confidence:** Reasoned

### 4. Missing Market Microstructure / Options Gamma Hypothesis
- **Location:** `analyzing-us-bigtech-stocks` Phase 3 (Hypothesis Tree lenses).
- **Description:** The 8 lenses for hypothesis generation focus on fundamentals, narrative, and macro. They omit Market Microstructure (e.g., options dealer gamma, systematic trend-following CTA unwinds, index rebalancing flows). In modern Big Tech markets, post-earnings moves are frequently amplified by options hedging flows.
- **Evidence:** The hypothesis tree lenses (a-h) in `SKILL.md` cover revenue, margins, segments, guidance, capex, narrative, positioning, and noise, but lack a dedicated lens for derivatives-driven flows or passive index mechanics.
- **Impact:** The agent may attribute a 15% drop to a "Guidance Cut" when 8% of the drop was actually driven by forced dealer delta-hedging due to massive put open interest.
- **Severity:** Low
- **Recommended fix:** Add a 9th lens to the hypothesis tree: "(i) Market Microstructure & Flow (dealer gamma, CTA unwinds, index rebalances)". Add a required check for Options Open Interest skew in Phase 2.
- **Confidence:** Reasoned

### 5. Lack of Probabilistic Sizing in Scenarios (Expected Value)
- **Location:** All Skills (Phase 8 / Step 6 / Phase 7 - Scenarios).
- **Description:** The skills explicitly and correctly ban "Price Targets" to avoid giving investment advice. However, they only ask for Bull/Base/Bear *narratives* and *falsifiers*. Institutional PMs require Expected Value (EV) weighting of the fundamental outcomes (e.g., FCF in Bull vs Bear) to size positions.
- **Evidence:** Phase 8 mandates 3 scenarios with falsifiers, but the schema and audit gates do not provision for an "Expected Fundamental Value" matrix.
- **Impact:** The output is a rigorous post-mortem but lacks the quantitative asymmetry profile needed for actual portfolio construction.
- **Severity:** Informational
- **Recommended fix:** Allow (but do not mandate) an "Expected Fundamental Value" matrix under the scenarios, where the agent assigns subjective probabilities to the fundamental outcomes, producing an EV-adjusted fundamental range. This remains strictly separated from a "price target."
- **Confidence:** Reasoned

---

## Comparative Analysis of the 3 Skills

### 1. `analyzing-us-bigtech-stocks` (The Flagship)
- **Role:** The gold standard for formal IC presentations.
- **Strengths:** The `CONSENSUS`, `EPISTEMIC`, `WATERFALL`, and `MANDATE` schema gates in `scripts/fact_base_audit.py` are exceptionally well-designed for automated compliance. The requirement to explicitly list `cross_checked_with` sources and the SHA-256 provenance sealing (`provenance_seal.py`) provide an audit trail that rivals manual compliance logs.
- **Weakness:** High friction; overkill for a quick market query.

### 2. `big-tech-earnings-postmortem` (The Fast-Ship Tactical Note)
- **Role:** The optimal tool for morning meetings or rapid PM updates.
- **Strengths:** The "lite" number registry (`fact_base_lite_audit.py`) is a brilliant compromise between speed and rigor. It prevents the "morning meeting hallucination" where an analyst confidently states a wrong EPS beat number, while avoiding the 16-page deck overhead.
- **Weakness:** Lacks the deep segment accounting checks found in the third skill.

### 3. `bigtech-equity-research` (The Deep-Dive / Quant Note)
- **Role:** Specialized for deep fundamental variance analysis.
- **Strengths:** The `segment_map_check.py` is the standout feature of the entire repository. LLMs are notorious for hallucinating segment names or using outdated taxonomies. Tying the segment map to the specific 10-Q filing's vintage via a hard gate prevents massive accounting errors and ensures ASC 280 compliance.
- **Weakness:** The reliance on a static `reference/peers.md` without corporate action checks (Finding #3) introduces survivorship bias risk.

---

## Conclusion

These skills are production-grade and exceed the analytical rigor of most human-generated retail research. To reach the standard required by Tier-1 buy-side compliance departments, the **MNPI temporal embargo (Finding 1)** must be implemented immediately as a hard gate in the audit scripts. The **beta regime diagnostics (Finding 2)** and **corporate action checks (Finding 3)** should follow as high-priority maintenance items to ensure the mathematical isolation of idiosyncratic risk remains accurate across market cycles.

---

### Executive Synthesis

The alternative comparative report is an exceptionally strong, compliance-first audit that correctly identifies the structural and regulatory gaps preventing these skills from meeting Tier-1 institutional standards. While my initial audit focused heavily on **quantitative rigor, market microstructure, and LLM-specific operational risks** (e.g., MNPI ingestion, beta regimes), the alternative report excels in **regulatory compliance, structural completeness, and internal consistency**.

Together, the two reports form a complete picture: the alternative report proves the skills are not yet "investment products," while my report proves they are not yet "quantitatively bulletproof." 

Below is a critical evaluation of the alternative report, highlighting its blind spots, correcting a minor regulatory conflation, and synthesizing both analyses into a unified master audit.

---

### 1. Critical Evaluation of the Alternative Report

#### Where the Alternative Report Excels (My Blind Spots)
The alternative report correctly elevates several findings that I either under-weighted or missed, which are fatal flaws for a buy-side Investment Committee (IC) memo:
*   **The Valuation & Decisioning Void (C-2):** I treated the lack of a DCF/Price Target as an informational design choice. The alternative correctly identifies this as a **Critical** failure. A post-mortem or attribution note is an *input* to an IC decision, not the decision itself. Without a forward-looking variant view, expected value, and sizing framework, the artifact cannot support capital allocation.
*   **Internal Inconsistency in Number Registries (H-2):** The alternative brilliantly caught that `bigtech-equity-research` (the most quantitative skill) lacks the machine-checked number registry (`fact_base_audit.py`) present in the other two. This is a severe internal consistency failure that I missed.
*   **Reg G / Non-GAAP Reconciliation (M-2):** Big Tech relies heavily on Non-GAAP metrics (e.g., Meta's FCF, Amazon's operating income ex-items). The alternative correctly flags the absence of SEC Reg G / Item 10(e) reconciliation framing, which is mandatory for institutional research.
*   **Data Licensing & Redistribution (M-4):** Scraping Yahoo Finance or Stooq for internal use is fine; redistributing that data in a formal IC memo or client note violates vendor terms of service. The alternative correctly flags this legal risk.

#### Where the Alternative Report is Blind (My Strengths)
The alternative report views the skills through a traditional "human analyst" lens, missing the specific operational and mathematical risks introduced by **LLM agents** and **modern market structure**:
*   **MNPI / Pre-Filing Web-Scrape Contamination (Missed entirely):** The alternative mentions "quiet periods" but misses the ingestion-time risk. If an LLM agent uses web search 10 minutes before an 8-K drops, it may scrape a leaked document from a forum and ingest it into the fact base. Without a temporal embargo gate, the agent will launder Material Non-Public Information (MNPI) into the IC memo, creating severe insider trading liability.
*   **Static Beta Regime Assumption (Missed entirely):** The alternative praises the "options math" but misses that the canonical 2-year monthly beta is mathematically flawed for Big Tech stocks undergoing volatility regime shifts (e.g., 2022 rate shocks). Applying an obsolete beta misattributes market-driven moves to idiosyncratic failures.
*   **Survivorship Bias in Peer Baskets (Missed entirely):** The alternative accepts the static `reference/peers.md` without questioning if the basket has suffered from survivorship bias due to recent M&A or delistings, which would distort cross-sectional comparisons.

#### Regulatory Nuance: Sell-Side vs. Buy-Side Conflation (C-1)
The alternative report’s **C-1 (Reg AC / FINRA 2241)** slightly conflates sell-side distribution rules with buy-side IC requirements. 
*   **Reg AC and FINRA 2241** apply to research reports distributed by a *broker-dealer* to clients. 
*   These skills are explicitly scoped for **"Midnight IC" (buy-side internal memos)**. Buy-side IC memos do not require Reg AC certification or FINRA 2241 disclosures. 
*   *Correction:* The true compliance gap for buy-side is not Reg AC, but **CFA Standard VI(A) (Disclosure of Conflicts)** and **fiduciary duty of care** (which requires the valuation/sizing missing in C-2). The alternative is correct that the skills fail as *sell-side* products, but slightly mis-scoped for their intended *buy-side* use case.

---

### 2. The Unified "Wall Street Grade" Master Audit Matrix

To achieve true Tier-1 institutional standards, the repository must address the synthesized findings below, ranked by severity.

#### Critical (Blocks IC / Legal Liability)
1.  **MNPI Temporal Embargo (Operational):** Implement a hard gate in the fact-base schema. If a T1 filing timestamp is set, any non-T1 web source retrieved *prior* to that timestamp must be automatically flagged as `Unverifiable` and purged to prevent MNPI contamination. *(From My Report)*
2.  **Valuation & Decisioning Void (Structural):** Add a forward-looking variant view (independent forecasts vs. consensus), expected fundamental value (scenario-weighted), and a risk/reward sizing framework. A post-mortem cannot be an IC decision document without these. *(From Alternative Report)*
3.  **Number Registry Consistency (Internal):** Port `fact_base_lite_audit.py` to `bigtech-equity-research`. The most quantitative skill cannot ship without machine-checked number traceability. *(From Alternative Report)*

#### High (Material Analytical / Compliance Flaws)
4.  **Static Beta Regime Assumption (Quantitative):** Enhance `quant_helpers.py` to output $R^2$ and volatility regime flags. If the 2-year beta correlation breaks down, force the agent to use a shorter window (e.g., 6-month daily) to accurately isolate idiosyncratic shock. *(From My Report)*
5.  **Reg G / Non-GAAP Reconciliation (Compliance):** Mandate a Reg G / Item 10(e) reconciliation table for any Non-GAAP metric used in the attribution (e.g., Adj. EBITDA, FCF). *(From Alternative Report)*
6.  **Event-Window Mis-specification (Quantitative):** Fix the T+0 vs T+1 logic. Intraday events must use T+0 close; after-hours events must use T+1 close. *(From Alternative Report)*
7.  **Multi-Class Market Cap Delta (Quantitative):** Clarify the market-cap delta formula to handle multi-class structures (e.g., GOOG/GOOGL) by using total diluted shares or class-weighted pricing. *(From Alternative Report)*
8.  **Data Licensing & Redistribution (Legal):** Add a data-licensing gate. Prohibit the redistribution of scraped vendor data (Yahoo, Stooq) in formal deliverables without explicit API rights. *(From Alternative Report)*

#### Medium (Methodological Rigor)
9.  **Survivorship Bias in Peer Baskets (Quantitative):** Add a corporate action check to verify the constituent status of the canonical peer basket against an index API prior to cross-sectional analysis. *(From My Report)*
10. **Market Microstructure / Options Gamma (Methodological):** Add a 9th lens to the hypothesis tree for "Market Microstructure & Flow" to ensure post-earnings moves driven by dealer delta-hedging are not falsely attributed to fundamental guidance cuts. *(From My Report)*
11. **Consensus Vintage & Mean/Median (Methodological):** Tighten the consensus vintage window to 1–3 days and enforce mean vs. median disclosure. *(From Alternative Report)*

---

### 3. Final Verdict

**The Alternative Report** is the superior **compliance and structural audit**. It correctly identifies that these skills, as currently designed, are "causal-attribution engines" rather than "investment products," and highlights the critical missing valuation and decisioning layers required for a buy-side IC.

**My Initial Report** is the superior **quantitative and operational audit**. It identifies the mathematical flaws in the existing implementation (beta regimes, multi-class shares) and the unique, catastrophic risks introduced by giving an LLM web-search capabilities during an earnings blackout (MNPI ingestion).

**Conclusion:** 
The repository is currently a **9/10 for automated data gathering and causal attribution**, but a **4/10 for institutional investment decisioning**. 

To cross the chasm to "Wall Street Grade," the maintainers must first implement the **MNPI Temporal Embargo** (to keep the lawyers happy) and the **Number Registry Consistency fix** (to keep the quants happy). Only then should they tackle the massive architectural lift of adding a **Valuation and Sizing Module** (to keep the PMs happy). Until the valuation module is built, the skills must be strictly firewalled as "Pre-Read Attribution Notes" and never distributed as final IC recommendations.
