## Scope note and verification limitation

I could not run `git clone`: this environment exposes web fetch/search but no shell or workspace. I reviewed the exact `main`-branch files via `raw.githubusercontent.com`; line references below are to those files. The audit is therefore **static**—no script was executed. Where a finding depends on runtime behavior, I label it accordingly.

**Review plan executed**

1. Verify file presence and completeness for all 18 listed files.
2. Audit frontmatter/YAML loading and skill-spec compliance.
3. Review methodology, evidence controls, and confidence taxonomy.
4. Inspect every script for correctness, tests, and failure modes.
5. Compare the three skills for consistency and drift.
6. Map the deliverables against sell-side, buy-side IC, and CFA equity-research standards.
7. Classify findings by severity and provide a verification ledger plus remediation plan.

---

## Executive verdict

**Skill 1, `analyzing-us-bigtech-stocks`, is the strongest and closest to production-grade in evidence design**—but its central numeric audit script is truncated and cannot run. That single defect turns its “audit gate” from a control into a claim.

**Skill 3, `bigtech-equity-research`, has the best formula/template set**, but it contains a core quantitative error: it labels market-adjusted excess return as “alpha” and conflates benchmark return with beta. It also mandates a pseudo-precise waterfall that directly contradicts the other two skills.

**Skill 2, `big-tech-earnings-postmortem`, is the clearest conceptual statement**, but it is essentially a methodology essay: no fact-base schema, no scripts, no audit mechanism, and its frontmatter appears to contain invalid YAML.

As **event-driven RCA briefings**, all three are above typical AI-generated research: primary-source hierarchies, confidence labels, hypothesis trees, counter-cases, and explicit “never fabricate” rules. As **Wall Street equity research or full investment-committee memos**, they are incomplete: no valuation, recommendation, position sizing, expected return, stock-based-compensation analysis, or regulatory disclosures. The labels “institutional-grade equity research” and “fund-manager-quality” overclaim relative to what the files deliver.

---

## Findings by severity

### Critical

#### C1. `fact_base_audit.py` is a truncated stub; the Phase 10 numeric audit gate cannot run

**Location:** `skills/analyzing-us-bigtech-stocks/scripts/fact_base_audit.py`

**Description:** The file is only 24 lines. It ends mid-definition:

```python
def visible_text(html: str) -> str: """Strip
```

The docstring advertises fact-base mode, checks mode, scan-only mode, and `--selftest`, with exit codes 0/1/2—but there is **no `main`, no argument parser, no audit logic, and no implementation of any mode**. The triple-quoted docstring opened on the final line is never closed, so the file cannot parse.

**Evidence:** ``

**Impact:** Phase 10 of Skill 1 requires `python3 scripts/fact_base_audit.py --slides ... --fact-base ...` and states “Both audit scripts exit clean” in the Definition of Done ``. That is impossible. Every Skill 1 report can ship without numeric verification, and the “fact base is the single source of truth” control `` is unenforced. This is the central anti-hallucination control, and it is absent.

**Severity:** Critical.

**Recommended fix:** Restore the complete script from the author’s source, or rewrite it with `argparse`, the three modes, placeholder scanning, and a `--selftest` that asserts expected exit codes and known-good/known-bad fixtures. Add a CI step that runs `python3 -m py_compile` and the selftest. Until then, remove the claim that the audit gate exists.

**Confidence:** Verified by inspection. Dynamic execution was not possible, but an unterminated triple-quoted string is a syntax error.

---

### High

#### H1. Skill 3’s “alpha” is not beta-adjusted; beta is conflated with benchmark return

**Location:** `skills/bigtech-equity-research/reference/formulas.md`, `scripts/quant_helpers.py`, `reference/methodology.md`

**Description:** The formula is:

```text
alpha = stock_return − benchmark_return (same window)
```

The text then says “If benchmark closes are unavailable, bound the beta (e.g. −1.0% to −2.0% during a sector de-rating)” and gives “GOOGL −12.6%, beta −1.5% → idiosyncratic −11.1%” ``. Beta is a unitless sensitivity, not a percentage. `quant_helpers.py` implements `abnormal_return(stock_ret, bench_ret)` and its selftest passes `-1.5` as “beta” ``. Methodology Phase 2 says “Abnormal return = stock return − same-day benchmark return” ``.

**Impact:** This is a market-adjusted excess return, not a market-model abnormal return. For a high-beta name, subtracting the benchmark return without multiplying by beta materially misstates the idiosyncratic move. Calling it “alpha” is technically wrong and can lead to incorrect root-cause attribution. A Wall Street-standard event study would estimate beta over a pre-event window and compute `AR = R_i − (α + βR_m)`, or use a factor model ``.

**Severity:** High.

**Recommended fix:** Either implement a proper market-model abnormal return with an explicit estimation window and beta, or rename the metric to “market-adjusted excess return” and stop calling the benchmark return “beta.” Add unit tests with known beta and known benchmark return.

**Confidence:** Verified by inspection of the formula and code; financial reasoning.

---

#### H2. Skill 3 mandates a pseudo-precise waterfall that Skill 1 and Skill 2 explicitly prohibit

**Location:** Skill 3 `reference/methodology.md` Phase 7, `reference/formulas.md`; Skill 1 `SKILL.md` Phase 8; Skill 2 “Common failure modes.”

**Description:** Skill 3 says the fund-manager output is a “quantified waterfall” where weights sum to the realized move, with weights that are “`Reasoned` allocations” and “not an observed regression” ``. `formulas.md` states `Σ (factor_weights) = realized_move` ``.

Skill 1 says the opposite: publish percentage attribution **only if** it is computable from sourced data; otherwise state that attribution is qualitative, and lists “fake-precision driver attribution percentages” as a top pitfall ``. Skill 2 lists “False precision: inventing a percentage of the move attributable to each driver” as a failure mode and says “Rank, don’t quantify falsely” ``.

**Impact:** The three skills will produce materially different conclusions on the same event. Skill 3’s waterfall creates an illusion of measurement: a judgmental allocation that happens to sum to −12.6% is not evidence that the factors caused −12.6%. An IC reader may treat it as a decomposition. This is exactly the “fake precision” the other skills warn against.

**Severity:** High.

**Recommended fix:** Remove the forced-sum waterfall from Skill 3, or relabel it as a qualitative/ordinal “driver ranking with analytical allocation” and do not claim it sums to the realized move. Align all three skills on one standard: ordinal ranking unless a sourced, reproducible attribution model exists.

**Confidence:** Verified by direct contradiction across the three files.

---

#### H3. Skill 2’s frontmatter appears to be invalid YAML

**Location:** `skills/big-tech-earnings-postmortem/SKILL.md`, line 11

**Description:** The frontmatter contains:

```yaml
license: Apache 2.0 compatibility: Requires web search and page-fetch tools for primary-source verification.
```

A plain YAML scalar cannot contain an unquoted `: ` sequence; a standard parser will reject this as a mapping-value error. `Apache 2.0 compatibility` is also not a valid SPDX license identifier.

**Evidence:** ``

**Impact:** The skill may fail frontmatter validation and not load or index. It is absent from `skills-catalog.md` and `skills-inventory.md`; the catalog was last synced 2026-10-23 ``, while the skill’s examples reference 2026-10-28, so it may simply be newer—but malformed YAML would independently prevent indexing.

**Severity:** High if it blocks loading; otherwise Medium.

**Recommended fix:** Use `license: Apache-2.0` and a separate field such as `compatibility: "Requires web search and page-fetch tools..."`. Add a YAML-lint step to the repo’s skill validation.

**Confidence:** Reasoned; standard YAML parsing rules.

---

#### H4. None of the three skills contains valuation, recommendation, position sizing, or expected return

**Location:** All three skills.

**Description:** The skills explicitly refuse price targets and recommendations: Skill 1 says “price targets on request” are out of scope and “present scenarios and falsifiers instead” ``. Skill 3’s report structure includes “Valuation Impact — forward multiple before/after vs historical band” ``, which is a relative valuation sanity check, not a valuation. Skill 2’s “risk/catalyst matrix” is strong but contains no valuation or recommendation ``.

**Impact:** CFA Institute’s equity-research report essentials include business description, industry analysis, financial analysis, valuation, risks, recommendation, and disclosures. A buy-side IC memo typically includes a recommendation, valuation, expected return, position sizing, and portfolio fit. These skills provide event attribution, not an investment decision. That is a legitimate scope choice—but then the output should not be called “equity research” or a “fund-manager-quality” IC artifact.

**Severity:** High relative to the claimed standard; Medium if the intended scope is strictly event RCA.

**Recommended fix:** Either add a valuation module (DCF, comps, reverse DCF, scenario-weighted value), a recommendation/position-sizing section, and expected-return math—or explicitly reframe the skills as “event-RCA pre-reads for IC discussion, not investment recommendations.” Remove “equity research” from the trigger language if the latter.

**Confidence:** Verified by absence.

---

#### H5. No stock-based-compensation, dilution, or cash-flow-quality analysis

**Location:** All three, especially Skill 1 Phase 6 and Skill 3 Phase 4.

**Description:** Skill 1 reconciles GAAP vs adjusted results and one-offs ``, but never requires an SBC schedule or FCF ex-SBC. Skill 3 computes capex/OCF and FCF trajectory ``, but not SBC. Skill 2 mentions diluted share count ``, but not SBC as an expense or FCF adjustment.

**Impact:** For big tech, SBC is a material economic cost and a central Street debate. FCF that ignores SBC overstates cash generation. Dilution from SBC also affects per-share value. A Wall Street-standard big-tech note would show SBC/revenue, SBC growth, diluted share count, and FCF ex-SBC. It would also examine working capital, deferred revenue, and capitalized costs—none of which these skills require.

**Severity:** High.

**Recommended fix:** Add a mandatory “SBC and dilution” block to the scorecard and FCF bridge: SBC expense, SBC/revenue, diluted share count QoQ/YoY, FCF ex-SBC, and a cash-flow-quality table covering working capital, deferred revenue, and capitalized costs.

**Confidence:** Verified by omission.

---

#### H6. The render audit checks canvas overflow but not internal clipping, font failure, or accessibility

**Location:** `skills/analyzing-us-bigtech-stocks/scripts/overflow_audit.mjs`

**Description:** The script opens each slide in headless Chromium and flags elements whose bounding boxes extend beyond the 1280×720 canvas by more than 2px ``. It does **not** check whether text is clipped inside a card while the card itself remains within the canvas. It does not verify that webfonts actually loaded, does not run an accessibility audit, and skips any element whose class contains “bleed” (`/bleed/.test(String(el.className))`) ``, which could hide real content in a class like `bleeding-edge-text`.

**Impact:** A dense IC deck can pass the audit while text is visually clipped or overlapping inside cards. Skill 1 claims “no overflow or clipping at 1280×720” ``, but the audit only proves canvas containment, not readability. It also does not detect font-load failure, even though the design imports Google Fonts externally ``.

**Severity:** High, because this is the only render gate and its coverage is narrower than the claim.

**Recommended fix:** Add `scrollHeight > clientHeight` and `scrollWidth > clientWidth` checks for text containers; await `document.fonts.ready` and assert required fonts with `document.fonts.check`; add axe-core for WCAG checks; replace the broad `bleed` class regex with the explicit `data-bleed="intentional"` / `data-decor` / `aria-hidden` markers only.

**Confidence:** Verified by inspection of the script.

---

#### H7. No regulatory compliance package for sell-side use; disclaimers are not sufficient

**Location:** All three, especially Skill 1 `methodology.md` §14 and Skill 3 `sourcing-and-confidence.md`.

**Description:** The skills include “Informational only — not investment advice” `` and “Analysis only. Not investment advice” ``. They do not include Reg AC analyst certification, FINRA Rule 2241 conflict/compensation disclosures, rating/price-target definitions, price charts, or a valuation-method explanation for a rating or target. Reg AC requires a certification that the views are the analyst’s personal views and disclosure of whether compensation is tied to the specific recommendation ``. FINRA Rule 2241 requires a reasonable basis and clear explanation of valuation method and risks for any rating or price target ``.

**Impact:** If these outputs are used internally at a buy-side firm as event-RCA pre-reads, most of these requirements are not applicable. If they are distributed as “equity research” by a broker-dealer or marketed as sell-side research, they are non-compliant. The “not investment advice” disclaimer does not cure missing analyst certification and conflict disclosures.

**Severity:** High conditionally; Medium if scoped strictly to internal use.

**Recommended fix:** Add an explicit distribution gate: “Internal analytical note. Not for distribution as sell-side research. No rating or price target.” If sell-side use is intended, add Reg AC certification, FINRA 2241 disclosures, rating/PT definitions, price charts, and legal review.

**Confidence:** Verified by absence; regulatory applicability is conditional.

---

### Medium

#### M1. `quant_helpers.py` has no assertions, a sign inconsistency, and a waterfall check that masks sign errors

**Location:** `skills/bigtech-equity-research/scripts/quant_helpers.py`; `reference/formulas.md`

**Description:** The “self-test” only prints values; it never asserts them ``. If a formula regresses, the script still exits 0. The OCF shortfall example in `formulas.md` says `−10.10B` ``, while the script prints `+10.10B` ``—one of the two is wrong. `waterfall_check` compares `abs(total - abs(realized_move)) < 0.05` ``, so a decomposition summing to +12.6 and one summing to −12.6 both “match” a −12.6 move. It cannot catch sign errors.

**Impact:** Arithmetic and sign errors can pass the “self-test.” The helper is a library with a hardcoded example, not a CLI that accepts real data.

**Severity:** Medium.

**Recommended fix:** Replace prints with `assert`-based pytest tests; make the waterfall signed; fix the OCF sign convention; validate zero/empty inputs explicitly; add a CLI that reads JSON/CSV inputs.

**Confidence:** Verified by inspection.

---

#### M2. Skill 1’s own worked example violates its “resolvable URL” rule

**Location:** `skills/analyzing-us-bigtech-stocks/references/fact-base-schema.md`

**Description:** The schema requires a “Resolvable URL; archived link if paywalled” ``, but the worked example uses `"source_url": "https://finance.yahoo.com/news/..."` ``. That is not resolvable and cannot be audited. The template also uses `https://...` placeholders, which is acceptable for a template, but the “worked example” is presented as real evidence.

**Impact:** The example teaches a placeholder pattern that violates the skill’s own standard. A fact base built from such URLs cannot be independently checked, undermining the “every number traceable” claim.

**Severity:** Medium.

**Recommended fix:** Use real archived URLs in worked examples, or mark them explicitly as illustrative and not audit-ready. Add a schema validation rule that rejects `...` and `example.com` in `source_url`.

**Confidence:** Verified by inspection.

---

#### M3. No automated tests or CI for any script

**Location:** All script folders.

**Description:** `fact_base_audit.py` has no tests and is truncated. `quant_helpers.py` has no assertions. `overflow_audit.mjs` has no test fixture deck. There is no `pytest`, `vitest`, or CI workflow in the skill folders. The coding-agent standard requires new logic to include automated tests or explicitly state that no test infrastructure exists.

**Impact:** There is no regression protection. A future edit can silently break the audit or the math.

**Severity:** Medium.

**Recommended fix:** Add a minimal `tests/` folder with pytest for Python and Playwright for the render audit, plus a GitHub Actions workflow that runs `py_compile`, `pytest`, and the selftest. At minimum, state in each SKILL.md that tests were not run and provide the commands.

**Confidence:** Verified by absence.

---

#### M4. External Google Fonts dependency breaks offline/air-gapped use and can make the render audit flaky

**Location:** `skills/analyzing-us-bigtech-stocks/references/report-design.md`

**Description:** The CSS imports IBM Plex from `fonts.googleapis.com` ``. In an air-gapped IC environment, the fonts will not load; fallback fonts change metrics and can cause overflow or underflow. `overflow_audit.mjs` uses `waitUntil: 'networkidle'` and a 400ms wait, which may time out or behave inconsistently when external fonts are slow.

**Impact:** The deck is not fully self-contained. The audit may pass with fallback fonts and fail (or look different) on a machine with the fonts available.

**Severity:** Medium.

**Recommended fix:** Self-host the IBM Plex font files inside the skill folder, or use a system font stack. Remove the external `@import`. Make the render audit assert that required fonts loaded.

**Confidence:** Verified by inspection; runtime effect Reasoned.

---

#### M5. Fixed 1280×720 canvas with 10.5px micro text; accessibility is not audited

**Location:** Skill 1 `report-design.md`; Skill 3 `templates/report-structure.md`

**Description:** Skill 1’s canvas is fixed at 1280×720 and uses 10.5px micro text for kickers and confidence chips ``. It does not state a WCAG requirement. Skill 3 says “Responsive. WCAG-AA contrast” ``, but provides no CSS, no focus states, and no accessibility audit.

**Impact:** The deck is not responsive and may be difficult to read at small sizes. If these are user-facing research artifacts, WCAG 2.2 AA is the baseline expected of enterprise-quality UI.

**Severity:** Medium.

**Recommended fix:** Either declare the deck a fixed-canvas IC artifact with a PDF export and a minimum readable font size, or add responsive HTML plus an axe-core accessibility audit. Do not claim WCAG-AA without testing it.

**Confidence:** Verified by inspection.

---

#### M6. The three skills are absent from the catalog and inventory

**Location:** `skills-catalog.md`, `skills-inventory.md`

**Description:** Searches for `analyzing-us-bigtech-stocks`, `big-tech-earnings-postmortem`, and `bigtech-equity-research` returned no matches. The catalog says it was synced 2026-10-23 ``, while the skills’ worked example uses an event dated 2026-10-28. They may simply be newer than the last sync, or they may be excluded by validation.

**Impact:** An agent browsing the repo may not discover them. If they are excluded due to frontmatter failure (see H3), that is a functional defect. If they are merely unindexed, it is a documentation/traceability gap.

**Severity:** Medium.

**Recommended fix:** Update the catalog/inventory after adding new skills, and add a CI check that every `skills/*/SKILL.md` with valid frontmatter appears in the catalog.

**Confidence:** Verified by search.

---

#### M7. Skill 2 has no fact-base, no scripts, no audit, and no templates

**Location:** `skills/big-tech-earnings-postmortem/SKILL.md`

**Description:** Skill 2 is a single 173-line file. It has strong conceptual controls—layered attribution, structural vs mechanical, verification ledger ``—but no fact-base schema, no numeric audit, no render audit, no formula sheet, and no HTML template. It relies entirely on the agent’s manual discipline.

**Impact:** It is the least reproducible of the three. The same event analyzed with Skill 1 vs Skill 2 will produce different levels of evidence traceability.

**Severity:** Medium.

**Recommended fix:** Either merge Skill 2’s conceptual framework into Skill 1 as its “methodology overview,” or give Skill 2 the same fact-base schema and audit tooling. Maintaining three independent implementations is a drift risk.

**Confidence:** Verified by file inventory.

---

### Low

- **L1. Brand imitation:** Skill 1’s design reference explicitly names “Goldman Sachs / BlackRock IC-memo aesthetic” ``. This is a style reference, not a compliance issue, but a production skill should avoid implying affiliation with named banks.
- **L2. License clarity:** Skill 1 and Skill 3 declare no license; Skill 2’s license line is malformed. Enterprise legal review may block use. Add SPDX identifiers.
- **L3. Silent `nan`:** `quant_helpers.py` returns `float("nan")` for zero consensus/OCF `` instead of raising or returning a typed error. This can propagate silently into a report.
- **L4. Playwright flakiness:** `overflow_audit.mjs` uses `networkidle` and a fixed 400ms wait ``; slow CI or external fonts can cause false timeouts. Add retries and `document.fonts.ready`.
- **L5. Template hygiene:** `fact_base.template.json` places `_example_1` and `_example_2` keys inside fact objects ``, which is confusing for a schema that otherwise enforces strict fields. Use a separate `examples` array.
- **L6. Versioning:** Skill 1 and Skill 2 have no `version`; Skill 3 is `1.0.0`. Add semantic versions and a changelog so methodology changes are traceable.

---

## Comparison of the three skills

| Dimension | Skill 1 `analyzing-us-bigtech-stocks` | Skill 2 `big-tech-earnings-postmortem` | Skill 3 `bigtech-equity-research` |
|---|---|---|---|
| **Evidence architecture** | Strongest: fact-base schema, source tiers, conflicts, derived facts with parent IDs and formulas `` | Weakest: verification ledger concept, but no schema or tooling `` | Medium: evidence ledger template, sourcing hierarchy, data-gap ledger `` |
| **Causal method** | Strongest: 5–8 falsifiable hypotheses, evidence for/against, at least one exclusion `` | Strong conceptual: layered attribution, structural vs mechanical, risk/catalyst matrix `` | Medium: 7-phase process, but less explicit hypothesis testing `` |
| **Quantitative rigor** | Medium: price decomposition, no beta-adjusted alpha; no valuation model `` | Low: no formulas; explicitly prefers ordinal ranks `` | Medium but flawed: formula sheet, but “alpha” is not beta-adjusted and waterfall is pseudo-precise `` |
| **Tooling / reproducibility** | Numeric audit broken; render audit works but narrow `` | None | Helper library works but no assertions/CLI; no fact-base audit `` |
| **Deliverable spec** | Strong: 15-page archetype map, design tokens, overflow budget `` | Thin: seven-slide sequence and visual bullets `` | Medium: 13-section outline, WCAG intent, but no CSS/template `` |
| **Wall Street completeness** | Low/Medium: RCA strong; no valuation/recommendation/position sizing | Low: RCA strong; no valuation/quant | Low/Medium: more formulas, but no full valuation/recommendation |
| **Key defect** | Audit script truncated → verification claim false | Malformed YAML, no tooling | Alpha/beta error + contradictory waterfall |

---

## Wall Street standards assessment

| Standard | What it expects | How the skills measure |
|---|---|---|
| **Sell-side equity research** (Reg AC, FINRA 2241, CFA report essentials) | Analyst certification; conflict/compensation disclosure; rating and price target with valuation method; risk factors; price chart; business/industry/financial analysis; valuation; recommendation | Strong on financial event analysis and risks; missing certification, conflicts, rating/PT, valuation, price chart. Not compliant as sell-side research. |
| **Buy-side IC memo** | Recommendation, thesis, valuation, expected return, position sizing, risks, catalysts, portfolio fit, downside | Strong on thesis/root cause, catalysts, risks; missing valuation, expected return, position sizing, portfolio fit, recommendation. Not a complete IC memo. |
| **Event-driven hedge fund pre-read** | Catalyst path, positioning, implied move, probability-weighted scenarios, risk/reward, falsifiers | Strong fit. Skill 1 and Skill 3 cover event path, positioning, implied move, scenarios, falsifiers. Missing probability-weighted expected value and risk/reward sizing. Best-fit use case. |
| **CFA Institute equity research report** | Business description, industry analysis, financial analysis, valuation, risks, recommendation, disclosures | Partial. Financial analysis and risks are present; valuation, recommendation, and disclosures are absent. |
| **Auditability / reproducibility** | Every number traceable; scripts tested; outputs reproducible | Intent is strong; execution is broken in Skill 1 and untested in Skill 3. Skill 2 has no mechanism. |

**Bottom line on compliance:** If these are internal, buy-side, event-RCA pre-reads, most regulatory gaps are not applicable and the evidence discipline is genuinely good. If they are presented as “institutional-grade equity research” or distributed by a regulated firm, they fall short of sell-side standards and should not be labeled that way.

---

## Verification ledger

| Check | Method | Result | Confidence |
|---|---|---|---|
| All 18 listed files fetched | Raw GitHub `main` URLs | Present and reviewed | Verified |
| `git clone` / execution | No shell available | Not performed | Unverifiable dynamically |
| `fact_base_audit.py` completeness | Inspected raw file, 24 lines | Ends mid-docstring; no `main`; cannot parse | Verified by inspection |
| `quant_helpers.py` self-test | Inspected code | Prints values; no assertions; sign inconsistency | Verified by inspection |
| Skill 2 YAML | Inspected frontmatter | Unquoted colon in `license` value; likely invalid | Reasoned |
| Test/CI presence | Searched skill folders | No tests or CI found | Verified by absence |
| Catalog/inventory presence | Searched both files | No matches for the three skills | Verified by search |
| `overflow_audit.mjs` runtime | Not executed | Appears complete; requires Playwright/Chromium | Reasoned |
| `fact_base_audit.py` runtime | Not executed | Expected `SyntaxError` on import/run | Reasoned |

---

## Prioritized remediation

1. **Fix C1 first.** Restore or rewrite `fact_base_audit.py` and add a pytest that runs `--selftest` and fails on a known-bad deck. Until then, remove the “audit gate” claim from Skill 1.
2. **Fix H1.** Implement a proper market-model abnormal return or rename the metric. Add unit tests with known beta and benchmark return.
3. **Resolve H2.** Remove Skill 3’s forced-sum waterfall or relabel it as a qualitative allocation. Align all three skills on ordinal attribution unless a sourced model exists.
4. **Fix H3.** Correct Skill 2’s YAML and add YAML validation to the repo’s skill indexing.
5. **Decide the product.** If the target is a full IC memo, add valuation, recommendation, position sizing, expected return, and SBC/cash-flow quality. If the target is event RCA, remove “equity research” and “fund-manager-quality” from the claims and state the scope explicitly.
6. **Add compliance gating.** If sell-side distribution is possible, add Reg AC/FINRA 2241 disclosures and legal review. Otherwise add a prominent “internal analytical note—not for distribution as sell-side research” notice.
7. **Extend the render audit.** Check intra-card clipping, font loading, and accessibility, not just canvas overflow.
8. **Self-host fonts and remove external dependencies** to make the deck offline/air-gapped reproducible.
9. **Add tests and CI** for every script, with concrete fixtures.
10. **Update the catalog/inventory** and add license/version metadata.

---

## Reproduction commands (for a machine with a shell)

```bash
git clone https://github.com/nordeim/my-pi-agent.git
cd my-pi-agent

# C1: should fail with SyntaxError (unterminated triple-quoted string)
python3 -m py_compile skills/analyzing-us-bigtech-stocks/scripts/fact_base_audit.py
python3 skills/analyzing-us-bigtech-stocks/scripts/fact_base_audit.py --selftest

# M1: prints values but has no assertions; inspect for sign consistency
python3 skills/bigtech-equity-research/scripts/quant_helpers.py

# H6: requires Playwright + Chromium
node skills/analyzing-us-bigtech-stocks/scripts/overflow_audit.mjs --dir <deck-dir>
```

---

## Final assessment

**Skill 1 is the best-designed of the three** and would be genuinely strong if its numeric audit script were complete. Its fact-base schema, hypothesis tree, exclusion rule, confidence system, and two-sidedness are better than much human-produced event commentary.

**Skill 3 is the best-supported analytically**—formula sheet, segment maps, evidence ledger, 13-section structure—but its “alpha” formula and forced waterfall are serious enough to undermine its claim of fund-manager quality. It needs a quant rewrite, not a cosmetic fix.

**Skill 2 is the clearest read** but is not a production skill: no tooling, no schema, no audit, and a frontmatter defect.

**None of the three is a Wall Street-grade equity research report or IC memo** as written. They are strong **event-RCA pre-reads**. That is a valuable product—but the labeling should match the deliverable, and the verification controls should actually run.
