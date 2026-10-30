## Review Setup & Evaluation Basis

I cloned the repository and read every listed file in full. The review is anchored to two external benchmarks recovered during research: an adversarial **Research Auditor** specification that treats every figure as "guilty until verified" and audits fabrication, staleness, unit errors, math errors, unsupported causal claims, and citation integrity; and an **Enterprise Research Quality Checklist** that demands ≥2 independent sources for key data points, ≤10% cross-validation deviation, explicit confidence tagging, and traceable conclusion support. I also cross-checked against the structural expectations embedded in the skills themselves — particularly their own "Never fabricate" and "primary sources only" rules — because a Wall Street-grade review must hold the artifact to its own stated standards, not only to an external rubric.

The three skills form a declared **family** with an explicit division of labour: `analyzing-us-bigtech-stocks` is the full-pipeline, audited IC-deck producer; `big-tech-earnings-postmortem` is the lighter single-note member without executable audit tooling; `bigtech-equity-research` is the quantified single-note with segment deep-dive and options math. That self-awareness is itself a point in their favour. The review evaluates each on its own contract and then on the integrity of the family wiring.

---

## Skill 1 — `analyzing-us-bigtech-stocks`: The Strongest Artifact, With One Structural Gap

### What it gets right (Verified)

**A genuinely enforced fact base.** The `fact_base.json` is not advisory — it is the single source of truth: "If a number is not in the fact base, it does not go in the report". Every fact carries `source_tier`, `source_name`, `source_url`, `retrieved_at`, `confidence`, and cross-check fields. The schema distinguishes `market_reaction`, `fundamentals`, `guidance`, `capital_allocation`, `one_off`, `positioning`, `macro`, `peer`, `sell_side`, and `narrative_metric`, and links facts to hypotheses via `supports`. This is more disciplined than many sell-side workbooks, where a number often enters the model without a cell-level provenance trail.

**Real executable audits, not theatrical ones.** `fact_base_audit.py` does four things that matter: (1) it checks every fact's numeric token actually appears on its declared `slide_pages`; (2) it reverse-checks numbers on slides against the fact base and reports "unverified candidates"; (3) it arithmetic-checks derived facts whose `formula` is of the form `LHS = RHS`; and (4) it enforces that `Assumed` facts appear on the method/assumptions page. The matching is **anchored** — `"82.3"` does not match `"$282.32"` — which eliminates the most common false-pass mode in numeric audit tooling. `overflow_audit.mjs` uses headless Chromium to detect any visible element extending beyond the 1280×720 canvas, measuring relative to the `.slide` element rather than the viewport, with explicit conventions for intentional bleed (`data-bleed="intentional"`, `data-decor`, `aria-hidden="true"`) rather than className guessing. These are **Verified by code inspection** as functioning audit tools, not decorative scripts.

**Hypothesis discipline enforced at the schema level.** The template requires every hypothesis to carry `predictions` — falsifiable checks — and a `verdict` drawn from a closed vocabulary (`PRIMARY — narrative`, `PRIMARY — mechanical`, `CONTRIBUTOR`, `AMPLIFIER`, `NOISE`, `EXCLUDED`). The SKILL.md golden rule is equally categorical: "A single explanatory story is a red flag. Enumerate, test, and explicitly exclude at least one". This directly addresses the Research Auditor's "unsupported claims & overreach" failure class.

**Reaction definition is pinned at T+1 close, not the headline number.** The methodology explicitly defines the primary reaction as "first full-session close after the event," labels after-hours and T+0 intraday as secondary, and gives the rationale: after-hours prints are thin and headline writers anchor on them; the close is what clears real size. Share-class basis is pinned before pulling prices (`GOOG` vs `GOOGL`), and split/dividend basis is recorded in the event charter. These are the exact discipline failures that produce unit and class errors in junior sell-side notes.

**The compliance boundary is stated, not fudged.** The sourcing document explicitly disclaims: "Internal analytical note — not for distribution as sell-side research: no rating, no price target, no analyst certification or conflict disclosures". It also flags Reg FD escalation if material non-public information is suspected. This is the correct posture for a non-regulated research artifact and avoids the most dangerous failure mode: dressing up an LLM output as certified sell-side research.

### The material weakness (High severity, Reasoned)

**The skill does not perform valuation.** Its stated scope is explaining *why* a stock moved and building a source-cited trend narrative. It explicitly excludes price targets, trading signals, and options strategies. That is a defensible scope choice, but it means the artifact **cannot by itself satisfy a Wall Street fund manager's core question**: "Is this name mispriced?" A PM receiving this deck gets an excellent causal explanation of the move, a hypothesis tree, a fact base, and a rank-ordered driver decomposition — but no forward multiple, no DCF, no scenario-weighted fair value, and no position-sizing framework. For an **investment committee** memo, that is a gap. The `bigtech-equity-research` sibling partially fills it with a "Valuation Impact" section (forward multiple before/after vs historical band), but even that stops short of an intrinsic valuation output.

**Severity:** High for IC use, Medium for post-mortem/RCA use. **Confidence:** Reasoned from scope statements and the absence of any valuation formula in `formulas.md` or the methodology.

### Medium-severity observations (Reasoned)

The `source_tier` enum (`T1`/`T2`/`T3`) is defined operationally in the schema but the definitions are not enumerated in the schema file itself; they are implied by the sourcing hierarchy and examples. A production-grade fact base should make the tier boundaries explicit in the schema, because "T2" can otherwise drift between a company press release and a named-reporter secondary summary.

The `cross_checked_with` field on facts is **not enforced by `fact_base_audit.py`** as a minimum-count requirement. The schema says decision-critical numbers should be cross-checked in ≥2 independent sources, but the audit script checks presence, formula arithmetic, and `Assumed` placement — it does not fail a `Verified` fact that has zero or one cross-check. This is a soft spot: the highest-stakes claim could pass the executable gate without meeting the stated cross-check standard. Adding a `--min-cross-checks` mode would close it.

---

## Skill 2 — `big-tech-earnings-postmortem`: Disciplined by Reference, Unguarded by Tooling

### What it gets right (Verified)

The postmortem skill is the clearest articulation of the family's **epistemic stance**: "A stock move is the market's revision of expectations, not a verdict on the company". Its three-question sequence — mechanical trigger → durability filter → falsification test — is exactly the structure a PM wants before debating the name. The two-axis driver classification (durability × evidentiary basis) and the explicit instruction to "Never skip from 'stock fell X%' to 'investors are worried about AI'" are direct antidotes to the narrative-first failure mode that dominates retail-grade and lower-quality sell-side postmortems.

**Event mechanics are pinned before analysis.** The skill requires exact date and session, T+1 close as primary reaction, share-class and split basis in writing, point move and percentage move, and market-cap change in dollars (shares × Δprice). These are the mechanical checks that catch the most common post-earnings errors: mixing GOOG and GOOGL, quoting after-hours as the reaction, or computing a percentage move off the wrong prior close.

**The family wiring is explicit and consistency-tested.** The canonical methodology lives in the sibling skill's `references/postmortem-framework.md`, and the skill states that on divergence, "the canonical copy wins: fix it there and mirror the change here in the same commit," with repository consistency tests (`tests/test_repo_consistency.py`) guarding the wiring. That is a mature maintenance pattern — it prevents the silent drift that plagues multi-file skill families.

### The material weakness (High severity, Reasoned)

**No executable audit and no fact-base schema.** The skill's own description concedes: "no multi-page deck and no executable audit tooling". A postmortem produced under this skill can therefore claim confidence labels without any machine check that a `Verified` figure was actually cross-checked, that a number on the page traces to a source, or that a derived formula balances. The research-auditor benchmark treats exactly this as a finding: "If a claim cannot be traced to any artifact you can read or fetch, that itself is a finding". In a Wall Street context, an un-audited note is acceptable as an *intermediate* artifact but not as a deliverable that goes to an IC without human review. The skill should either (a) state plainly that the deliverable is a draft requiring human verification, or (b) inherit the `fact_base_audit.py` harness from the sibling skill in a lightweight mode. Currently it does neither, and its description ("institutional-grade single-file HTML research note") overstates the verification backing relative to the sibling.

**Severity:** High for standalone delivery; the skill's own framing as "lightweight, fastest-ship" partially mitigates but does not eliminate the gap.

### Medium observation (Reasoned)

The postmortem relies on the canonical framework living in a sibling directory. If deployed standalone without that folder, the operative summary is self-contained — but the canonical framework, including the full failure-mode catalog and risk/catalyst matrix, is not bundled. That is a deliberate tradeoff for lean context, but it means two deployments of the same skill can have materially different methodological depth depending on whether the sibling folder is present. A self-contained copy of the postmortem framework, or a checksum-based assertion that the canonical file is available, would make the deployment contract explicit.

---

## Skill 3 — `bigtech-equity-research`: The Most Quantitatively Transparent, With a Labelling Triumph

### What it gets right (Verified)

**The "Reasoned allocation" label is the single best epistemic move in the family.** `formulas.md` states, in bold, that the root-cause driver decomposition weights "are `Reasoned` analytical allocations — a judgmental attribution that happens to sum to the move — **not** an observed regression, not evidence of causation, and not a measurement. The sum-to-move identity is an arithmetic consistency check, not evidence of causation". `quant_helpers.py` repeats the same caveat in `waterfall_check`: "this checks arithmetic consistency of a `Reasoned` allocation; it is **NOT** evidence of causation". And `report-structure.md` requires the label "Reasoned allocation — not a measured decomposition" to be prominent on the chart itself, not buried in a footnote. This is precisely the discipline that separates credible attribution from the "implied precision" failure mode. Very few sell-side notes are this explicit about the epistemic status of their own waterfall.

**Formulas are concrete, worked, and directionally correct.** Beat/miss delta, market-adjusted and beta-adjusted excess return, options implied move / surprise ratio, capex/OCF ratio, OCF shortfall, average price-target cut, and the waterfall consistency check are all given with worked Alphabet Q3 2026 numbers and explicit sign conventions. The treatment of excess return is notably careful: it distinguishes the market-adjusted form (implicit beta = 1) from the beta-adjusted form, warns against calling the benchmark return "beta," and instructs disclosure of the beta estimation window. `quant_helpers.py` implements exactly these formulas, raises on zero consensus/OCF, and runs an asserting self-test on the worked example. This is **Verified by code inspection** as deterministic, testable math — not hand-waving.

**Segment maps distinguish ASC 280 reportable segments from disclosed revenue lines.** The file explicitly warns: "Do not present a disclosed revenue line as a 'segment' — the variance table must mirror the filing's own segment note or the auditor cannot tie it out". It correctly maps Alphabet, Microsoft, Amazon, Apple, Meta, Nvidia, and Tesla, and flags the Apple unit-volume trap (unit sales ceased in FY2019; third-party estimates are `Unverifiable` unless a named report is sourced) and the Nvidia ASC 280 vs market-platform distinction. This is genuinely institutional-grade taxonomy discipline.

**The evidence ledger and Data-Gap Ledger are operational, not decorative.** Two tables: an evidence ledger (claim, sources, confidence, verification method) and a Data-Gap Ledger listing every `Assumed`/`Unverifiable` item with the exact source/action needed to close it. The method note requires stating the source hierarchy, disclaiming "executed verification" for price targets and forward guidance, and reaffirming that root-cause weights are `Reasoned` judgment. This is a real verification trail.

### The material weakness (High severity, Reasoned)

**No executable audit script for the single-note deliverable.** `quant_helpers.py` is a math library with a self-test, not an audit of the report. There is no equivalent of `fact_base_audit.py` that verifies every number in the 13-section HTML note traces to a sourced fact, nor an overflow/render audit for the single-file deliverable. The `evidence-ledger.md` template exists, but its population is manual. In a Wall Street workflow, a research note that has not been mechanically checked against its own evidence ledger is a draft, not a publishable artifact. The skill's hard rules are strong (“Never fabricate”, “Every number is sourced or tagged `Unverifiable`”), but hard rules without executable enforcement depend entirely on the operator's discipline — the same failure mode the sibling skill's `fact_base_audit.py` exists to prevent.

**Severity:** High for production delivery; partially mitigated by the fact that the sibling skill provides the audit harness, so the family as a whole has a path to audited output.

### Medium observations (Reasoned)

The `segment-maps.md` structures are pinned to "FY2025/FY2026 10-Ks" and the file itself warns: "Segment structures change (divestitures, reorganizations, new GAAP segment rules) — re-verify against the latest filing before use". That is honest, but a stale segment map is a high-impact failure: if the map is used without re-verification, the variance table will not tie to the current filing. A schema-level "segment_map_version" and "last_verified_against" field, analogous to the fact base's `retrieved_at`, would make staleness visible.

The 13-section report structure is comprehensive and PM-facing, but it does **not** include a dedicated **risk factors / falsification conditions** section separate from the Bull/Bear Forward View. For a Wall Street IC, the bear case and explicit falsifiers deserve their own section, not a subsection of the forward view. The sibling skill's hypothesis-tree verdict vocabulary (`EXCLUDED`, `NOISE`) provides a model for how to make that rigorous.

---

## Cross-Skill Comparison and Family Integrity

| Dimension | `analyzing-us-bigtech-stocks` | `big-tech-earnings-postmortem` | `bigtech-equity-research` |
|---|---|---|---|
| Fact-base schema | **Yes** (explicit, enforced) | No | No (evidence ledger template only) |
| Executable numeric audit | **Yes** (`fact_base_audit.py`, anchored matching, formula checks) | No | No (math library only) |
| Render/overflow audit | **Yes** (`overflow_audit.mjs`, headless Chromium) | No | No |
| Hypothesis falsification enforced | **Yes** (schema-level `predictions` + closed verdict set) | Reasoned, not schema-enforced | Reasoned, not schema-enforced |
| Valuation output | No (explicitly out of scope) | No | Partial (forward multiple band, no DCF/fair value) |
| Segment taxonomy discipline | Strong (methodology references segments) | Not covered | **Strongest** (ASC 280 vs disclosed lines, company-by-company) |
| Confidence labelling | **Yes** (4-level taxonomy, schema-enforced) | Yes (stated, not enforced) | **Yes, with the strongest causal caveat** |
| Compliance boundary | Disclaimed as internal, not sell-side | Disclaimed | Disclaimed (no rating, no PT, Reg FD escalation) |
| Explicit family role | Full pipeline, audited IC deck | Lightweight single note | Quantified single note, segment deep-dive |

**The family is coherent in its division of labour but uneven in enforcement.** The strongest artifact (`analyzing-us-bigtech-stocks`) is the only one with a machine-checked fact base and render audit. The other two rely on operator discipline for the same guarantees. For a Wall Street audience, the correct deployment posture is: **use the full-pipeline skill as the production vehicle, and treat the other two as drafting/lite modes that must be upgraded to the full pipeline before any IC-facing delivery.** The skills themselves say this, but the descriptions of the lite skills ("institutional-grade") do not sufficiently caveat the verification deficit relative to the flagship.

**The canonical-example discipline is a genuine strength.** All three skills teach from the same Alphabet Q3 2026 print (GOOG $282.32 close, −12.29% from $321.89, $482B market-cap erosion). This is not just a pedagogical convenience: it means the family's formulas, worked examples, and expected outputs are cross-checkable against one another, and a regression in one skill's math can be detected against the canonical numbers. That is a real quality-control mechanism.

---

## Verdict Against Wall Street Institutional Standards

### What is genuinely institutional-grade (Verified or strongly Reasoned)

The flagship skill's **fact-base-to-slide audit chain** is better than much of what circulates as sell-side model documentation. The **primary-source hierarchy** (EDGAR → IR transcript → exchange/vendor prices → named consensus → wire services → aggregators) matches the Research Auditor's preference for primary sources and its warning against secondary summaries for segment splits. The **confidence taxonomy** (Verified / Reasoned / Assumed / Unverifiable) with hard requirements is exactly the right schema; the explicit **"Reasoned allocation, not measured decomposition"** label on the waterfall is a level of epistemic honesty that many professional notes lack. The **Data-Gap Ledger** is a real institutional control — it turns missing data into an auditable work item rather than a silent assumption.

### Where it falls short of the highest institutional bar (High severity)

**1. The family does not produce a valuation.** For a fund manager, causal attribution without a forward valuation is half a research product. The `Valuation Impact` section in the single-note skill (forward multiple before/after vs historical band) is a start, but there is no DCF, no reverse-DCF, no SOTP, no scenario-weighted fair value, and no explicit cost-of-capital framework. The skills are honest about this — they are RCA and trend-analysis tools, not valuation models — but the "institutional-grade equity research" framing in the descriptions invites a comparison the artifacts cannot fully satisfy. **Recommendation:** either add a sibling `bigtech-valuation` skill, or add a mandatory "Valuation Context" section to every deliverable that explicitly states the note is pre-valuation and names the model gap as an open item.

**2. Enforcement is concentrated in one skill, not the family.** The flagship's `fact_base_audit.py` is the only executable gate. The postmortem and single-note skills can produce confidence-labelled figures without machine verification. For a Wall Street production pipeline, every skill that emits a client-facing or IC-facing number should pass through the same fact-base audit. **Recommendation:** factor the fact-base schema and audit script into a shared `_shared/` module and make all three skills depend on it, with the lite skills using a reduced `--mode lite` that still checks number traceability and `Assumed` placement.

**3. Cross-check enforcement is soft.** `Verified` is defined as "observed in ≥2 independent primary/near-primary sources," but the audit script does not fail a `Verified` fact with fewer than two independent cross-checks. **Recommendation:** add a `--strict-verified` mode that enforces the ≥2 rule for facts tagged `Verified`, and a `--decision-critical` list that requires cross-checks for named headline metrics.

**4. Segment-map staleness is unguarded.** The map is a static file pinned to FY2025/FY2026 10-Ks. There is no version field, no last-verified date, and no check that the map matches the current filing. **Recommendation:** add `segment_map_version`, `last_verified_against_filing`, and a hard warning in the variance-table workflow if the filing date is after the map's verification date.

**5. The lite skills' descriptions overstate verification relative to the flagship.** "Institutional-grade" appears in the postmortem and single-note descriptions without the "no executable audit tooling" caveat that the postmortem body contains. **Recommendation:** align the descriptions with the actual verification backing, and add a one-line "Verification status" field to every deliverable cover: "Full fact-base audit passed" vs "Draft — human verification required."

### What is clean or near-clean

The **compliance boundary** is correctly drawn: no rating, no price target, no analyst certification, no conflict disclosures, Reg FD escalation. This is the right posture for a non-regulated research artifact and avoids the most serious regulatory failure mode. The **security and data-safety posture** in the scripts is unremarkable in a good way: no hardcoded secrets, environment-based configuration, no logging of sensitive payloads. The **anti-slop discipline** is visible: no placeholder `TODO` values in final templates, no speculative configuration options, no padding.

### Verification ledger for this review

| Check | Method | Result |
|---|---|---|
| All listed files read in full | Direct raw fetch from `raw.githubusercontent.com` | **Verified** — 17 files read end-to-end |
| `fact_base_audit.py` logic inspected | Line-by-line read of the script | **Verified** — anchored matching, formula eval, `Assumed` placement check |
| `overflow_audit.mjs` logic inspected | Line-by-line read of the script | **Verified** — headless Chromium, `.slide`-relative measurement, explicit bleed conventions |
| `quant_helpers.py` math inspected | Read of formulas + self-test | **Verified** — deterministic, raises on zero denominators, worked-example self-test |
| External benchmarks recovered | Web search + page fetch | **Verified** — research-auditor spec and enterprise checklist read |
| Scripts **executed** | Not possible in this review environment | **Unverifiable** — code inspection only; the user should run `python3 fact_base_audit.py --selftest`, `node overflow_audit.mjs --selftest`, and `python3 quant_helpers.py` to confirm runtime behaviour |
| Valuation gap | Absence of DCF/fair-value formulas in all listed files | **Reasoned** — no valuation formula exists in `formulas.md` or any methodology file |

---

## Bottom Line

These are **serious, thoughtfully engineered research skills** — not generic prompt wrappers. The flagship `analyzing-us-bigtech-stocks` is the standout: its fact-base schema, anchored numeric audit, render audit, hypothesis falsification schema, and confidence taxonomy constitute a genuinely institutional-quality control chain for **causal attribution and post-event explanation**. The `bigtech-equity-research` skill's "Reasoned allocation, not measured decomposition" label and its ASC 280 segment discipline are best-in-class epistemic hygiene. The family's compliance boundary is correctly drawn.

The gap to the **highest** Wall Street bar is threefold: **(1) no valuation output**, so the family explains moves but does not opine on mispricing; **(2) enforcement is concentrated in one skill**, so the lite members can emit confidence-labelled figures without machine verification; and **(3) cross-check and segment-map staleness controls are soft**. None of these is a fatal flaw — they are the difference between a very good internal research tool and a fully audited production research pipeline. The fastest path to closing the gap is to factor the fact-base schema and audit script into a shared module, add a `--strict-verified` and `--decision-critical` mode, add segment-map versioning, and require every deliverable to state its verification status on the cover.
