### Audit Report: Big-Tech Equity Research Skill Family

**Scope:** Critical evaluation of three skills (`analyzing-us-bigtech-stocks`, `big-tech-earnings-postmortem`, `bigtech-equity-research`) against the rigorousness and compliance standards expected of major investment banks (e.g., Goldman Sachs, Morgan Stanley) and institutional asset managers.

---

### 1. Executive Summary
The architecture of this "big-tech research family" demonstrates a rare level of engineering and analytical discipline for LLM-driven financial workflows. The separation of canonical doctrine (methodology), execution skills, and machine-verifiable audit gates aligns closely with the "four-eyes" principle and automated QA requirements of Tier-1 financial institutions. 

The full-pipeline skill (`analyzing-us-bigtech-stocks`) meets the highest standards for Investment Committee (IC) readiness. However, the lightweight variants introduce significant compliance and QA gaps—specifically the removal of automated numeric and render audits—that would block deployment in a regulated institutional environment without remediation.

---

### 2. Comparative Analysis: The Research Family

| Skill | Institutional Equivalent | Rigor & Compliance Profile |
| :--- | :--- | :--- |
| **`analyzing-us-bigtech-stocks`** | **Formal IC Memo** | **Gold Standard.** Enforces machine-checked numeric and render audits. Suitable for formal Investment Committee distribution and external research. |
| **`big-tech-earnings-postmortem`** | **Morning Note / Sales-Triage** | **High Risk.** Fast, narrative-driven, but sacrifices automated audit gates. Suitable for internal desk triage, but lacks the compliance traceability for formal IC distribution. |
| **`bigtech-equity-research`** | **Sector Deep-Dive** | **High Quant Rigor, QA Gap.** Excellent mathematical sophistication (options math, segment waterfalls), but lacks the automated numeric and UI verification of the full pipeline. |

---

### 3. Audit Findings

#### Critical (Blocks Institutional Deployment)
*   **C1. Absence of Automated Audit Gates in Lightweight Variants**
    *   **Location:** `big-tech-earnings-postmortem/SKILL.md`, `bigtech-equity-research/SKILL.md`
    *   **Description:** Wall Street compliance mandates strict audit trails for all quantitative claims in research notes. Both lightweight skills explicitly state they have "no executable audit tooling" and do not bundle the numeric audit script (`fact_base_audit.py`) or a render audit script.
    *   **Impact:** High risk of hallucinated or mis-transcribed financial figures reaching portfolio managers without automated validation. Violates institutional QA principles.
    *   **Recommended Fix:** Bundle a lightweight version of the numeric audit script that parses the single HTML file and checks inline figures against an embedded or linked JSON fact base. Alternatively, mandate that the full fact-base pipeline is run before generating the note.

#### High (Severe Reliability/Architecture Risks)
*   **H1. Hard Dependency on Sibling Skill Files (Architectural Fragility)**
    *   **Location:** `big-tech-earnings-postmortem/SKILL.md`
    *   **Description:** The skill relies entirely on `analyzing-us-bigtech-stocks/references/postmortem-framework.md` for its canonical methodology. If deployed in isolation (common for lightweight agents), the methodology is missing, leading to degraded output.
    *   **Impact:** Loss of analytical rigor if the repository consistency test is not run during deployment.
    *   **Recommended Fix:** Ensure the deployment script strictly bundles required shared reference files, or accept the maintenance overhead to bundle a local copy of the core doctrine.
*   **H2. Missing Render/Overflow Audit for Multi-Section HTML**
    *   **Location:** `bigtech-equity-research/templates/report-structure.md`
    *   **Description:** Mandates a "13-Section Self-Contained HTML Research Note" with complex layouts (stat bands, callout boxes, horizontal stacked bars) but provides no automated render/overflow audit (unlike Skill 1's `overflow_audit.mjs`).
    *   **Impact:** High probability of UI breakage, text clipping, or unreadable charts on standard institutional displays or when printed to PDF.
    *   **Recommended Fix:** Reuse or adapt `overflow_audit.mjs` for the single-file HTML note to verify that no section exceeds its container bounds.

#### Medium (Methodological & Edge-Case Rigor)
*   **M1. Beta Estimation Window Disclosure is Unenforced**
    *   **Location:** `bigtech-equity-research/reference/formulas.md`, `quant_helpers.py`
    *   **Description:** Correctly distinguishes between market-adjusted (beta=1) and market-model (estimated beta) excess returns, requiring disclosure of the beta estimation window. However, `quant_helpers.py` does not enforce this disclosure in code.
    *   **Impact:** Analysts/LLMs may compute beta-adjusted returns without documenting the estimation window, reducing reproducibility.
    *   **Recommended Fix:** Update `abnormal_return` in `quant_helpers.py` to optionally accept a `window_disclosure` string and print it, or add a strict linting rule in the skill instructions.
*   **M2. Unverified Candidates vs. Hard Failures**
    *   **Location:** `analyzing-us-bigtech-stocks/scripts/fact_base_audit.py`
    *   **Description:** Reports numbers found on slides but absent from the fact base as "unverified candidates" rather than hard failures.
    *   **Impact:** A lazy agent could pass the audit gate with a wall of warnings instead of a clean build.
    *   **Recommended Fix:** Add a `--strict` flag to `fact_base_audit.py` that promotes "unverified candidates" to hard failures (exit code 1), ensuring institutional builds can enforce zero-tolerance for unsourced numbers.

#### Low (Maintainability & UX)
*   **L1. Playwright Dependency Check UX:** The `overflow_audit.mjs` script relies on `playwright` being installed but only provides instructions in the docstring. If it fails to load, the error is generic. Catch the module import error and output a clean, actionable error message with the exact install commands.
*   **L2. Magic Numbers in Python Tolerance:** In `quant_helpers.py`, the tolerance `TOL = 0.05` is defined, but the magic number `100.0` is used repeatedly for percentage conversions. Define a `PERCENT_MULTIPLIER` constant for clarity.

---

### 4. Wall Street Compliance & Rigor Assessment

#### Strengths (Institutional Best Practices)
1.  **ASC 280 Segment Rigor:** The distinction between **reportable segments** (ASC 280) and **disclosed revenue lines** in `segment-maps.md` is sophisticated and prevents a common junior analyst error. Variance tables must mirror the filing's own segment note.
2.  **Alpha vs. Excess Return:** The strict separation of "market-adjusted excess return" from "market-model alpha" in `formulas.md` is mathematically precise. It correctly flags that "beta is a unitless sensitivity, not a percentage move."
3.  **Reaction Definition:** Defining the primary reaction as the **T+1 full-session close** (`methodology.md`) is a hallmark of institutional rigor, avoiding the noise and liquidity gaps of after-hours trading.
4.  **Reg FD & MNPI:** The explicit warning about Material Non-Public Information (MNPI) in `sourcing-and-confidence.md` meets strict compliance standards.

#### Gaps (Compliance Risks)
1.  **Audit Trail Continuity:** As noted in C1, the lack of machine-verified audit trails in the lightweight variants is a compliance failure. Wall Street firms require "four-eyes" or automated verification for all published research.
2.  **Forward-Looking Statements:** While the skills correctly label scenarios as "Assumed" and avoid "predictions," the automated check for forward-looking statement disclaimers on every page (a standard SEC/FINRA requirement for public research) is not explicitly enforced in the audit scripts.

---

### 5. Final Recommendations

To elevate the entire skill family to a unified "Tier-1 Investment Bank" standard:

1.  **Unify the Audit Gates:** Refactor `fact_base_audit.py` into a core library that can be imported by all three skills. The lightweight variants should run a "Lite" version of the audit against their single-file HTML output to ensure numeric integrity is never optional.
2.  **Enforce Render Verification:** Mandate that any HTML output (whether 15 slides or 13 sections) passes `overflow_audit.mjs` before delivery to prevent layout breakage.
3.  **Strict Mode by Default:** Change the default behavior of `fact_base_audit.py` to fail the build if "unverified candidates" are found. Institutional QA should not tolerate warnings.

**Verdict:** The repository is exceptionally well-engineered. The primary gap is the inconsistent application of automated verification gates across the skill variants. Addressing C1 and H2 will make this a production-grade standard for AI-assisted equity research.

---

### Evaluation of the Alternative Comparative Report

The alternative report is an exceptionally strong piece of domain-specific analysis. While my initial audit evaluated the skills primarily through the lens of **software engineering, automated QA, and system architecture**, the alternative report evaluated them through the lens of **institutional finance, epistemic rigor, and portfolio management utility**. 

The alternative report successfully identified critical domain-level gaps that my engineering-focused review underweighted, most notably the **absence of intrinsic valuation models** and the brilliant epistemic caveat regarding **"Reasoned allocation" vs. measured decomposition**. However, it missed several operational and software-delivery risks that would cause these tools to fail in a continuous integration (CI) pipeline.

Below is a critical comparison of the two reports, followed by a unified remediation roadmap.

---

### Head-to-Head Comparison

| Dimension | My Initial Report (Engineering/QA Lens) | Alternative Report (Finance/Domain Lens) | Winner / Synthesis |
| :--- | :--- | :--- | :--- |
| **Core Value Proposition** | Evaluated the skills as automated data-pipelines and HTML generators. Focused on audit trails, UI rendering, and code hygiene. | Evaluated the skills as financial research products. Focused on epistemic honesty, causal attribution, and PM utility. | **Alternative.** A Wall Street audience cares more about the financial logic than the Python code style. |
| **Epistemic Rigor** | Noted the confidence taxonomy (Verified/Assumed) and ASC 280 segment discipline. | Caught the **"Reasoned allocation, not measured decomposition"** label in Skill 3. Recognized this as a best-in-class defense against implied precision. | **Alternative.** This is a profound quantitative finance insight that prevents the LLM from hallucinating causal R-squared values. |
| **Business Logic Gaps** | Focused on the lack of automated audits in the lightweight variants. | Identified the **Valuation Gap** (no DCF, SOTP, or reverse-DCF). Correctly noted that RCA without valuation is "half a research product." | **Alternative.** An Investment Committee cannot act on a post-mortem without a forward-looking valuation context. |
| **Software & QA Mechanics** | Caught the `Playwright` dependency UX flaw in `overflow_audit.mjs`, magic numbers in Python, and the need for a `--strict` CLI flag. | Noted the lack of render audits for Skill 3, but did not evaluate the execution mechanics or CI/CD integration of the existing scripts. | **My Report.** The alternative report assumes the scripts work flawlessly; my report identified how they will break in a real deployment. |
| **Audit Enforcement** | Recommended promoting "unverified candidates" to hard failures via a `--strict` flag. | Noted that the $\ge 2$ cross-check requirement for `Verified` facts is soft and not enforced by the script. | **Tie.** Both identified the same gap; I provided the CLI implementation, they provided the compliance rationale. |

---

### Synthesized Gap Analysis: What Both Reports Should Address

While both reports are highly rigorous, combining them reveals a few blind spots that a true "Tier-1 Investment Bank" deployment would require:

1.  **The "Hallucinated Math" Vector in LLMs:** 
    Both reports praise the math in `quant_helpers.py`. However, neither report addressed *how* the LLM integrates this library. If the LLM is prompted to calculate a beat/miss delta, does it strictly call the Python helper, or does it attempt to do the math in-context (which LLMs notoriously fail at)? A Wall Street-grade skill must explicitly forbid in-context arithmetic and enforce tool-use for all calculations.
2.  **Market Data Latency & API Rate Limits:**
    Neither report evaluated how the skills fetch the T+1 close or consensus estimates. If the skill relies on scraping Yahoo Finance or unauthenticated APIs, it will fail in a production environment due to rate limits or IP bans. Institutional tools must integrate with authenticated, licensed data vendors (e.g., FactSet, Bloomberg B-PIPE, or Refinitiv) via secure MCP (Model Context Protocol) servers.
3.  **Regulatory Archiving (WORM Storage):**
    The alternative report correctly notes the compliance boundary (no ratings, no price targets). However, if these notes are distributed internally to PMs, FINRA/SEC rules (like Rule 17a-4) often require that all electronic communications and research notes be archived in Write-Once-Read-Many (WORM) storage. The skills currently output to local HTML/JSON without an archiving hook.

---

### Unified Remediation Roadmap (The "Wall Street Standard" Patch)

To elevate this repository from "excellent open-source project" to "production-grade institutional infrastructure," the maintainer should execute the following merged roadmap:

#### Phase 1: Epistemic & Domain Hardening (Finance)
*   **Mandate Valuation Context:** Add a mandatory "Valuation & Scenario Weighting" section to all three skills. Even if a full DCF is out of scope, the skill must output a "Reverse-DCF Implied Growth" metric (e.g., "The current price implies X% CAGR over 5 years, vs historical Y%").
*   **Enforce Tool-Use for Math:** Update all `SKILL.md` files with a hard rule: *"Never perform arithmetic in-context. All calculations (deltas, percentages, multiples) must be executed via the bundled Python/JS helpers."*
*   **Version-Control Segment Maps:** Implement a `segment_map_version` and `last_verified_filing_date` in the schema. Add a pre-flight check that warns the user if the current date is >90 days past the last verified 10-K/10-Q.

#### Phase 2: Automated QA & CI/CD Hardening (Engineering)
*   **Unify the Audit Harness:** Extract `fact_base_audit.py` and `overflow_audit.mjs` into a shared `_core/audit` directory. Force Skills 2 and 3 to run a "Lite" version of these audits against their single-file HTML outputs before delivery.
*   **Implement Strict Compliance Modes:** Add `--strict-verified` (enforces $\ge 2$ cross-checks) and `--fail-on-unverified` (promotes warnings to exit code 1) to the audit script. This allows the CI pipeline to block unverified notes from being merged or published.
*   **Fix Playwright UX:** Wrap the `playwright` import in `overflow_audit.mjs` in a `try/catch` block that outputs a clean, copy-pasteable installation command (`npm i -D playwright && npx playwright install chromium`) if the module is missing.

#### Phase 3: Institutional Integration (Operations)
*   **Add Archiving Hooks:** Include a post-generation hook in the pipeline that pushes the final HTML/JSON artifact to an internal S3 bucket or compliance archive with a cryptographic hash of the fact base.
*   **Standardize Data Ingestion:** Replace any web-scraping logic with explicit MCP tool definitions for institutional data providers, ensuring the LLM only interacts with licensed, audited data streams.

### Final Verdict

The alternative report is the superior **financial critique**, correctly identifying that causal attribution without valuation is an incomplete product for a portfolio manager. My report is the superior **engineering critique**, identifying the exact CI/CD and rendering failures that will occur when these scripts are run at scale. 

Together, they prove that the repository's architecture is fundamentally sound and highly sophisticated. The path to production is not a rewrite, but the rigorous enforcement of the rules the author has already written.
