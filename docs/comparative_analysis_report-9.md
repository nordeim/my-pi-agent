## Audit verdict

**The three skills are a genuinely rigorous evidence architecture — likely best-in-class among LLM research tooling — but none is “Wall Street investment-bank-grade” as shipped.** The flagship (`analyzing-us-bigtech-stocks`) is closest on auditability and evidence discipline. All three fail the sell-side regulatory standard (Reg AC, FINRA 2241, supervisory review) and the buy-side IC standard (valuation, recommendation, position sizing, independent forecasts). The repository’s own Mode C audit reaches the same conclusion: **skill 1 = 4.45/5, skill 2 = 2.85/5, skill 3 = 3.00/5; “none of the three passes a full bulge-bracket research-controls review.”**

**Findings summary: 2 Critical / 5 High / 5 Medium / 3 Low.** The critical findings are structural, not bugs: they cannot be fixed by tightening a script; they require either an explicit scope limitation enforced operationally, or a new valuation-and-compliance module.

---

## Scope and verification

| Checked | How | Result |
|---|---|---|
| All three `SKILL.md` files | Read in full from GitHub raw | Complete |
| Supporting references | Read methodology, postmortem framework, fact-base schema, report design, segment maps, peers, sourcing, formulas, templates | Complete |
| Script inventory | Read folder structures and key scripts (`fact_base_audit.py`, `fact_base_lite_audit.py`, `note_audit.py`, `quant_helpers.py`, `segment_map_check.py`, `provenance_seal.py`, `audit_all.sh`) | Substantive, with tests present |
| Repository tests and self-audit | Read `tests/test_repo_consistency.py`, `test_note_audit.py`, `docs/skills-audit/README.md`, comparative reports | Strong CI/consistency discipline; self-audit corroborates gaps |
| Runtime execution | Not executed — no local clone or runner in this environment | **`Unverifiable`** for script pass/fail |
| Local `git clone` | Not possible in this environment | Audit based on public GitHub content |

Some raw script views truncated at a `TODO` sentinel (notably `note_audit.py`), but the repository also ships tests for that script. I therefore did **not** treat the truncation as proof the gate is broken; I treat runtime status as unverified rather than defective.

---

## Cross-skill comparison

| Dimension | `analyzing-us-bigtech-stocks` | `big-tech-earnings-postmortem` | `bigtech-equity-research` |
|---|---|---|---|
| Role | Full pipeline, 12–16-page IC deck | Fast single-file post-earnings note | Quantified single note with segment/options math |
| Depth | 348-line SKILL + 420-line methodology; deepest doctrine | 371-line SKILL; strong prose, lite tooling | 191-line SKILL; relies heavily on 170-line methodology + references |
| Numeric gate | Full `fact_base_audit.py` with consensus, epistemic, waterfall, mandate schema gates | Lite `fact_base_lite_audit.py` number registry | **No machine-checked number registry**; only placeholder/disclosure, render, a11y, provenance |
| Segment deep-dive | Limited | Limited | Strong: ASC 280 segment map + staleness gate |
| Options math | Limited | Limited | Yes: implied move, surprise ratio, VRP caveat |
| Valuation / PT / rating | None; explicit boundary | None; explicit boundary | None; forward multiple band only |
| Compliance | Scoping disclaimer + fund-position disclosure | Scoping disclaimer + fund-position disclosure | Scoping disclaimer + fund-position disclosure |
| Best use | Full RCA / IC pre-read where audit trail matters | Fast event postmortem | Quantified single-note with segment/options work |
| Main risk | Heavy, slow; still not an investment recommendation | “Lite” artifact can inherit flagship credibility without flagship gates | Most quantitative but weakest numeric traceability |

**Ranking by rigour:** flagship > equity-research > postmortem.  
**Ranking by speed:** postmortem > equity-research > flagship.  
**Ranking by Wall Street compliance:** none pass; flagship is closest only on audit trail.

---

## Critical findings

### C-1. Not compliant as sell-side research; no Reg AC, FINRA 2241, or supervisory controls

**Location:** `analyzing-us-bigtech-stocks/SKILL.md` §Distribution & compliance (lines 307–321); `big-tech-earnings-postmortem/SKILL.md` final compliance block (lines 348–359); `bigtech-equity-research/reference/sourcing-and-confidence.md` disclaimer (lines 42–47).

**Description:** All three explicitly disclaim sell-side status: “no rating, no price target, no analyst certification (Reg AC) or FINRA 2241 disclosure package.” That is a scoping choice, not a compliance substitute. Under Reg AC and FINRA 2241, whether a document is a “research report” turns on content and distribution, not on the author’s self-label. These artifacts contain price-move attribution, forward multiple bands, implied moves, and segment analysis — content a reader could reasonably treat as research.

**Evidence:** No analyst certification; no rating or price-target definitions; no rating distribution; no investment-banking-client disclosure; no ownership/market-making disclosure; no compensation disclosure; no supervisory-analyst approval; no quiet-period or restricted-list controls. The only conflict disclosure is the fund-position field for IC audiences.

**Impact:** If produced inside a broker-dealer or distributed to clients, the artifacts may trigger recordkeeping, certification, and disclosure obligations the skills do not satisfy. Even internally, conflict disclosure is incomplete for a fiduciary IC memo.

**Severity:** Critical.

**Recommended fix:** Either (a) harden the scope operationally — legal review, internal-use-only distribution controls, a prominent “not a research report” legend, and a block on client distribution — or (b) add a sell-side compliance module with Reg AC certification, FINRA 2241 disclosures, rating/PT framework, and supervisory sign-off. For buy-side use, add full conflict declarations (personal holdings, compensation, outside interests) and compliance approval.

**Confidence:** `Verified` (omissions visible); regulatory consequence `Reasoned`.

---

### C-2. No valuation, recommendation, or position sizing — cannot support an IC investment decision

**Location:** `analyzing-us-bigtech-stocks/SKILL.md` §Phase 8 (lines 201–205); `big-tech-earnings-postmortem/SKILL.md` §Step 7 (lines 203–206); `bigtech-equity-research/SKILL.md` hard rule 10 (lines 71–74); `bigtech-equity-research/templates/report-structure.md` §11 (lines 42–47).

**Description:** All three explicitly refuse to produce DCF, SOTP, scenario-weighted fair value, a rating, a price target, or a recommendation. They define themselves as causal-attribution products, not full equity research. That is honest, but it means they stop before the decision a fund manager actually needs to make: *what is it worth, what should we do, how large should the position be, and what is the risk/reward?*

**Evidence:** “No DCF / SOTP / scenario-weighted fair value is produced” appears in every skill. The equity-research template includes a forward-multiple band as “context, not intrinsic valuation.” There is no recommendation section, no expected-return calculation, no position-sizing framework, and no downside/upside ratio.

**Impact:** A PM must commission a separate valuation and decision memo. The artifact can inform an IC discussion but cannot be the IC decision document. This is the largest analytical gap against “fund-manager-quality.”

**Severity:** Critical.

**Recommended fix:** Add a valuation module — DCF, SOTP, reverse DCF, comps, and scenario-weighted fair value — plus a recommendation/position-sizing section with expected return, downside, and risk budget. Or integrate a dedicated valuation skill and require its output before IC delivery.

**Confidence:** `Verified`.

---

## High findings

### H-1. No proprietary forecasts or earnings model

**Location:** `bigtech-equity-research/reference/methodology.md` Phase 1 (lines 13–33); `big-tech-earnings-postmortem/SKILL.md` Step 2 (lines 100–134); flagship Phase 1 (lines 103–127).

**Description:** The skills compute beat/miss against consensus but do not build independent revenue, margin, EPS, capex, or FCF forecasts. Consensus is the denominator, not a forecast. Sell-side and buy-side standards expect the analyst’s own estimates and a variant view versus consensus.

**Impact:** The analysis is reactive, not forward-looking. It cannot identify where the analyst differs from the Street — the core of alpha generation.

**Severity:** High. **Fix:** require a forward model with explicit assumptions and a consensus bridge showing the variant view. **Confidence:** `Verified`.

---

### H-2. `bigtech-equity-research` has no machine-checked number registry

**Location:** `bigtech-equity-research/SKILL.md` folder structure (lines 20–35) and delivery gates (lines 101–115).

**Description:** The skill bundles `note_audit.py` (placeholders/disclosures), render, a11y, provenance, `segment_map_check.py`, and `quant_helpers.py`, but **no `fact_base_audit.py` or `fact_base_lite_audit.py`**. Its Definition of Done says every figure carries a citation and confidence tag, but nothing machine-checks that the printed numbers trace to a registry.

The less quantitative `big-tech-earnings-postmortem` actually has the stronger numeric gate: it bundles `fact_base_lite_audit.py` and a lite number registry.

**Impact:** A quantitative note with segment tables and options math can ship with untraceable numbers. The audit checks disclosures and rendering, not number-to-source integrity. This is the most surprising inconsistency in the family.

**Severity:** High. **Fix:** port `fact_base_lite_audit.py` from the postmortem, or the flagship’s `fact_base_audit.py`, and require every money/percentage figure to be registered. **Confidence:** `Verified`.

---

### H-3. Event-window convention can mis-specify T+0 vs T+1

**Location:** flagship Phase 0 (lines 95–96); postmortem Step 1 (lines 67–69).

**Description:** Both define the primary reaction as “the first full-session close after the event (T+1 close).” That is correct for after-close earnings, but wrong for events during market hours (guidance shock, regulatory ruling, product launch). For an intraday event, the first full session close is T+0, not T+1.

**Impact:** Using T+1 for an intraday event adds an extra day, contaminating the event return, the benchmark excess return, and the attribution.

**Severity:** High. **Fix:** define the window by event timestamp relative to market hours: pre-market → T+0 close; intraday → T+0 close; after-close → T+1 close. State the rule in the event charter. **Confidence:** `Reasoned`.

---

### H-4. Market-cap delta formula is ambiguous for multi-class shares

**Location:** flagship Phase 2 (lines 129–130); postmortem Step 1 (lines 73–74).

**Description:** “Shares outstanding × Δprice” does not specify total shares across classes or per-class prices. For GOOG/GOOGL, META Class A/B, and other multi-class names, using one class’s shares and price can misstate the market-cap change.

**Impact:** Market-cap loss/gain figures can be materially wrong, especially when share classes diverge.

**Severity:** High. **Fix:** require total diluted shares across all classes and a class-weighted price, or compute each class separately and sum. Disclose the method. **Confidence:** `Reasoned`.

---

### H-5. No model validation, backtest, or accuracy track record

**Location:** all three skills; no validation file or backtest in the repository.

**Description:** The attribution methodology — hypothesis tree, two-axis classification, ranking heuristic — is a model. There is no out-of-sample validation, no accuracy track record, and no sensitivity analysis. For bank model-risk standards (SR 11-7-style governance), this is a gap.

**Impact:** The framework’s correctness rests on face validity. A PM cannot see how often the RCA correctly identifies the dominant driver.

**Severity:** High. **Fix:** build a validation set of historical events with known outcomes; measure attribution accuracy; publish a methodology validation note. **Confidence:** `Reasoned`.

---

## Medium findings

| # | Finding | Location | Why it matters | Fix | Confidence |
|---|---|---|---|---|---|
| M-1 | Consensus vintage window of ~10 days is too loose; mean-vs-median not enforced by the audit | flagship Phase 1 (lines 118–119); postmortem Step 2 (lines 119–122) | Stale or incomparable consensus makes every beat/miss delta wrong | Default to 1–3 trading days; require mean vs median disclosure | `Reasoned` |
| M-2 | No SEC Reg G / Item 10(e) non-GAAP reconciliation framing | flagship Phase 6; postmortem Step 2 | Non-GAAP analysis may not meet regulated-research disclosure standards | Add a Reg G/Item 10(e) checklist and require the reconciliation table | `Reasoned` |
| M-3 | Public-source-only; no channel checks, expert calls, surveys, or management access | source-tier tables in all three | Limits differentiated insight; the artifact is a sophisticated public-source synthesis | Add an optional primary-research module; or state “public-source-only” as a hard limitation | `Verified` |
| M-4 | Data licensing and vendor redistribution rights not addressed | source tiers list Yahoo, Stooq, Macrotrends, TIKR, FactSet/Visible Alpha via outlets | Banks/funds have strict data governance; redistributing vendor data in deliverables is a legal risk | Add a data-licensing checklist; prefer licensed feeds; prohibit redistribution without rights | `Reasoned` |
| M-5 | Postmortem claims “standalone” but depends on external `quant_helpers.py` for arithmetic | postmortem lines 59–65 | If the sibling skill is absent, the agent may hand-code arithmetic, violating compute-don’t-recall | Bundle a minimal arithmetic helper | `Verified` |

---

## Low findings

| # | Finding | Why it matters | Fix | Confidence |
|---|---|---|---|---|
| L-1 | Long `SKILL.md` files (348 and 371 lines) increase context load and instruction-following risk | Agents under pressure may skip sections | Keep `SKILL.md` as a router; move detail to references | `Reasoned` |
| L-2 | “Midnight IC” design is stylized; it omits the conventional page-1 rating/PT/valuation box | Standard research readers expect a rating, PT, valuation summary, and disclosures on the cover | Add a conventional cover variant if a compliance/valuation module is added | `Reasoned` |
| L-3 | Node/Playwright/Python dependency versions are not pinned | Audit results may vary across environments | Add pinned versions/lockfile | `Reasoned` |

---

## What is genuinely strong

These should not be buried under the gaps:

- **Source-tier discipline:** T1/T2/T3 sourcing, primary-source-first, no aggregators for fundamentals.
- **Confidence taxonomy:** `Verified` / `Reasoned (derived)` / `Reasoned (judged)` / `Assumed` / `Unverifiable` — better than most sell-side junior work.
- **Machine gates:** anchored number matching, consensus schema gate, epistemic split, waterfall sum check, segment-map staleness gate, provenance seal.
- **Anti-hallucination and degraded mode:** tools offline → shrink scope, tag `Unverifiable`, log the exact pull needed — never backfill from memory.
- **Cross-skill consistency tests and CI:** guards doctrine drift and byte-identical vendoring.
- **Explicit scoping disclaimers:** no price targets, no investment advice, fund-position disclosure for IC audiences.

---

## Wall Street standards gap matrix

| Standard / expectation | Sell-side bank | Buy-side fund manager | These skills |
|---|---|---|---|
| Analyst certification (Reg AC) | Required | Not typically required | **Absent** |
| Rating, price target, valuation method (FINRA 2241) | Required, with reasonable basis and clear valuation explanation | Expected in IC memo | **Absent** |
| Price chart with rating/PT history | Required for rated securities | Expected | **Absent** |
| Rating distribution, IB-client disclosure, ownership, market-making, compensation | Required | Not applicable / different | **Absent** |
| Conflict disclosure | Required | Required (CFA Standard VI(A)) | Partial: fund position only |
| Supervisory analyst / compliance approval | Required | PM/IC review | **Absent** |
| Recordkeeping / WORM / audit trail | SEC 17a-4 | Firm policy | SHA-256 seal, but no WORM/firm-key signing |
| Independent forecasts / earnings model | Expected | Expected | **Absent** — consensus only |
| Intrinsic valuation / scenario-weighted fair value | Expected | Expected | **Explicitly out of scope** |
| Recommendation, position sizing, risk/reward | Required | Required | **Absent** |
| Primary research / channel checks | Differentiator | Differentiator | **Absent** — public sources only |

---

## Bottom line

- **As an internal, public-source analytical pre-read:** these skills are **excellent** — the evidence discipline is stronger than most human junior-analyst workflows, and the audit gates are unusually mature for an LLM skill family.
- **As sell-side research:** they are **not compliant** and should not be distributed as such. The disclaimer is a scope statement, not a control.
- **As a buy-side IC decision document:** they are **incomplete** — no valuation, no recommendation, no position sizing, no independent forecasts. They are an input to the IC memo, not the memo.
- **If the goal is true Wall Street-grade:** the highest-value additions are (1) a valuation/recommendation module, (2) independent forecasts, (3) a compliance/supervisory wrapper or an operationally enforced internal-only scope, and (4) a machine-checked number registry in `bigtech-equity-research` to match the postmortem.

---

## Validation of the alternative report

### Approach and limits

I validated the alternative against the same evidence base as my audit: the three `SKILL.md` files, their reference docs, the script inventory, and the repo's self-audit. I could not execute `quant_helpers.py` or the audit scripts here, so any claim about their internal behavior is `Reasoned` from source, not `Verified` by execution. Where the two reports disagree, I state which one the evidence favors and why.

---

### Finding-by-finding

| Alt. finding | Alt. severity | My validation | Corrected severity | Confidence |
|---|---|---|---|---|
| 1. MNPI / pre-filing temporal gate | High | **Gap real; legal framing overstated; fix has a design flaw** | Medium–High (hygiene) | Reasoned |
| 2. Static beta regime | Medium | **Valid and genuinely new** | Medium | Reasoned |
| 3. Survivorship / corporate actions in peers | Medium | **Valid; fix partially mis-scoped** | Medium | Reasoned |
| 4. Missing microstructure lens | Low | **Valid for the flagship; feasibility caveat** | Low | Reasoned |
| 5. No probabilistic EV sizing | **Informational** | **Valid gap, badly under-rated** | High (arguably Critical for IC use) | Reasoned |

**Finding 1 — MNPI temporal gate.** The underlying observation is sound: the audit gates check `consensus_vintage` and `cross_checked_with`, not a hard temporal ordering against the verified T1 filing timestamp. A provenance gate is good practice. But the legal characterization is wrong in two ways. Reg FD (17 CFR 243) binds *issuers and persons acting on their behalf* against selective disclosure; it does not impose liability on an analyst for *receiving* or *documenting* a leak — the issuer is the potential violator. Insider-trading liability (SEA §10(b)/Rule 10b-5) attaches to *trading* on MNPI in breach of duty, not to writing an IC memo. So "violates Reg FD principles and risks insider trading liability" conflates three different regimes. The realistic risk here is **data-integrity contamination** (treating unconfirmed pre-filing chatter as confirmed fact), which is real but is not "severe regulatory risk." Also, the proposed fix — "any non-T1 source with `retrieved_at` before the T1 filing time must be stripped" — would wrongly strip **legitimate pre-event inputs**: consensus, positioning, prior guidance, and options OI are *supposed* to predate the event. The gate needs a `data_type` discriminator (pre-event input vs post-event fact) and should compare only post-event claims against the T1 timestamp.

**Finding 2 — Beta regime.** Strong finding, and one I missed. A 24-month monthly beta window does smooth regime breaks (2022 rate shock, 2023 AI re-rating), and delegating "structural change" detection to the LLM with no quantitative trigger is exactly the kind of unguarded judgment call the skills otherwise avoid. R² and realized-vol regime flags are the right diagnostics. Valid at Medium.

**Finding 3 — Corporate actions / survivorship.** Valid. A static `peers.md` with no constituent-status check is a real staleness/bias vector, and the direction of the bias in the example is correct (removing a distressed constituent flatters the basket, making the target look worse). One scoping issue: the fix says "verify against an authoritative index or exchange API," but these are **bespoke analyst baskets** (e.g., hyperscalers), not index constituents — an index-membership API is the wrong control. The right control is a corporate-action/news check on each *named* constituent, plus a cache-age gate.

**Finding 4 — Microstructure lens.** Valid and correctly scoped to the flagship's Phase 3. Note the third skill already has options math (implied move, VRP), so this is specifically a hypothesis-tree gap in `analyzing-us-bigtech-stocks`. Feasibility caveat: OI/skew data is vendor-grade and may be T3 or unavailable under the public-source constraint, so the "required check" should be conditional on data availability.

**Finding 5 — EV sizing.** The gap is real and important — it overlaps my Critical C-2 (no valuation, recommendation, or position sizing). But rating it **Informational** is a serious calibration error. The report itself says the output "lacks the quantitative asymmetry profile needed for actual portfolio construction" — that is a *core* buy-side requirement, not a suggestion. For "fund-manager-quality," this belongs at High or Critical, not Informational.

---

### Factual errors and internal inconsistencies

These are the most damaging issues in the alternative, because an audit report's credibility rests on internal consistency:

1. **The executive summary claims the skills "correctly implement … Reg AC."** They do the opposite: all three explicitly disclaim analyst certification under Reg AC ("no rating, no price target, no analyst certification (Reg AC) or FINRA 2241 disclosure package"). This is a direct factual error, and it is contradicted by the report's own Finding 1 (which alleges severe regulatory risk). `Verified`.

2. **The summary claims "separation of idiosyncratic from systematic risk" is correctly implemented**, while Finding 2 says the beta isolation is mathematically distorted. Internal tension the report never reconciles. `Verified`.

3. **The summary claims "automated compliance gates (Reg FD …)"**, while Finding 1 says the skills lack any temporal MNPI enforcement — i.e., no Reg FD gate exists. The two statements cannot both be true. `Verified`.

4. **"Production-grade"** in the conclusion is overclaimed given no valuation, no PT/rating framework, no supervisory wrapper, and the missing numeric gate in the third skill (below).

These inconsistencies suggest the executive summary was written independently of the findings and not reconciled against them — the opposite of the "lead with a summary that reflects the findings" discipline an audit should follow.

---

### Coverage versus my audit

**What the alternative adds that mine missed (real value):**
- Beta regime / R² diagnostic (Finding 2)
- Survivorship and corporate-action staleness in peer baskets (Finding 3)
- A microstructure/flow lens for the flagship (Finding 4)
- A temporal provenance gate concept, even if legally mis-framed (Finding 1)

**What my audit caught that the alternative misses:**
- **C-2 / Finding 5 under-rated:** no valuation (DCF/SOTP/fair value), no recommendation, no position sizing — the alternative's own EV point is the thin edge of this, but it never addresses intrinsic valuation and rates the visible part Informational.
- **No independent forecasts / earnings model** (H-1) — consensus is a denominator, not a forecast; no variant view. The alternative doesn't mention this at all.
- **No machine-checked number registry in `bigtech-equity-research`** (H-2). The alternative *praises* that skill and its `segment_map_check.py` but never notices it lacks a `fact_base_audit`/`fact_base_lite_audit` equivalent — the single most surprising inconsistency in the family.
- **Event-window T+0/T+1 convention bug** (H-3) — intraday events get an extra day of contamination.
- **Multi-class market-cap formula ambiguity** (H-4) — GOOG/GOOGL, META A/B.
- **No model validation/backtest** (H-5).
- **No supervisory/compliance wrapper, no WORM/recordkeeping, incomplete conflict disclosure** (C-1) — the alternative substitutes a legally inaccurate Reg FD claim for this.
- **Data licensing / vendor redistribution** (M-4).
- **Postmortem's "standalone" dependency on external `quant_helpers.py`** (M-5).
- No verification ledger; all five findings tagged only "Reasoned," with no `Verified` items and no statement of what was executed vs inspected.

Net: the alternative is a good **quant/market-microstructure supplement**; it is not a substitute for a standards-and-compliance audit. It misses both Criticals and roughly ten Medium/Low items.

---

### Severity calibration

| Issue | Alt. severity | Mine | Assessment |
|---|---|---|---|
| No valuation / EV / sizing | Informational | Critical | **Alternative is wrong**; this is the core buy-side gap |
| MNPI temporal gate | High | — (missed) | Real but over-rated; Medium–High after correcting legal framing |
| Beta regime | Medium | — (missed) | Fair |
| Corporate actions | Medium | — (missed) | Fair |
| Microstructure lens | Low | — (partial) | Fair |
| No independent forecasts | — | High | Alternative misses |
| No numeric gate in skill 3 | — | High | Alternative misses |

The alternative inflates one finding (MNPI → High) and deflates the most consequential one (EV/sizing → Informational). That is the inverse of the correct ordering.

---

### Methodological quality

| Criterion | My audit | Alternative |
|---|---|---|
| Verification ledger | Yes (checked vs not-run, labeled) | No |
| Confidence tagging | Mixed Verified/Reasoned | All Reasoned |
| Severity taxonomy applied consistently | Yes | No (Informational for a structural gap) |
| Internal consistency | Yes | **No** (exec summary contradicts findings) |
| Coverage breadth | Broad (2 Critical, 5 High, 5 Medium, 3 Low) | Narrow (5 findings) |
| Standards-gap matrix | Yes (bank vs buy-side) | Partial (narrative only) |
| Comparative section | Dimension table + ranking | Qualitative paragraph |
| Legal/regulatory accuracy | Careful (Reg AC/FINRA disclaimers) | **Imprecise** (Reg FD/insider-trading conflation; false Reg AC claim) |

---

### Verdict

**The alternative is a competent, useful technical supplement with three genuinely valuable findings I missed — beta regime, corporate-action staleness, and the microstructure lens — but it is not a stronger audit overall.** Its executive summary is internally inconsistent and contains a material factual error (Reg AC "implemented"), its MNPI finding conflates three legal regimes and proposes a gate that would strip legitimate pre-event data, it mis-scopes the peer-basket fix (index API for bespoke baskets), and it buries the single most important buy-side gap (EV/valuation/sizing) at Informational while missing both Criticals and most of the High findings.

**The strongest position is a merge, not a choice.** Priority order for remediation:

1. **Critical (mine):** valuation + recommendation + position-sizing module; compliance/supervisory wrapper or operationally enforced internal-only scope.
2. **High (merged):** independent forecasts (H-1); numeric gate in `bigtech-equity-research` (H-2); beta-regime diagnostic (Alt-2); corporate-action/staleness gate (Alt-3); event-window convention (H-3); multi-class market-cap formula (H-4); model validation (H-5); and elevate Alt-5 (EV matrix) to High.
3. **Medium:** temporal provenance gate with a `data_type` discriminator (Alt-1, corrected); consensus vintage tightening (M-1); Reg G/Item 10(e) checklist (M-2); primary-research scope statement (M-3); data licensing (M-4); postmortem standalone helper (M-5).
4. **Low:** microstructure lens (Alt-4, data-availability conditional); SKILL.md length; cover-page conventions; dependency pinning.

If you want, I can produce a single reconciled audit document that merges both sets of findings under one severity taxonomy and one verification ledger — that would be the deliverable a compliance or IC reviewer would actually want to see.

---

## Plan for the reconciled audit document

**Assumptions (stated, not asked):** deliverable is a single Markdown file for a compliance/IC reviewer; target location `docs/skills-audit/reconciled-audit-v1.md` in the cloned repo; audience is a supervisory analyst, compliance officer, or IC chair — not the skill authors. If any of these are wrong, the structure still holds; only the metadata header changes.

**Reconciliation rules applied:**
1. One severity taxonomy (Section 12), with an explicit escalation rule for firm-policy-dependent items.
2. One verification ledger covering every class of claim; nothing claimed as executed that was not.
3. Conflicts between the two audits resolved on evidence, and every resolution logged in an appendix so the reviewer can see *why* a severity moved.
4. The alternative's factual errors are corrected in-place, not silently — with a corrections appendix so the reviewer can trace the change.
5. Alt-5 (EV sizing) is elevated and kept as its own High finding rather than buried inside C-2, because it is a distinct, tractable deliverable; C-2 remains the umbrella for valuation + recommendation + sizing.
6. Alt-1 (MNPI gate) is corrected on legal framing and re-scoped as a data-integrity control, not a Reg FD control; severity made firm-policy-dependent.

**Resulting count: 2 Critical / 6 High / 8 Medium / 4 Low = 20 findings.**

The document follows.

---

```markdown
# Reconciled Audit — BigTech Equity Research Skill Family

| Field | Value |
|---|---|
| Document | Reconciled audit of three agent skills |
| Scope | `analyzing-us-bigtech-stocks`, `big-tech-earnings-postmortem`, `bigtech-equity-research` |
| Source material | Two independent prior audits (Audit A = standards/compliance; Audit B = quant/microstructure) |
| Status | For compliance / IC review. Not a certification. |
| Version | 1.0 (reconciled) |
| Issued | ____ (fill at sign-off) |
| Reviewer | ____ |

---

## 1. Executive summary

The three skills implement an evidence architecture — source tiering, an epistemic
confidence taxonomy, machine-checked number registries (two of three skills),
provenance sealing, and cross-skill consistency tests — that is stronger than most
manual junior-analyst workflows. They are honest about what they are not: none
claims to be sell-side research, and each carries a scoping disclaimer.

They are nonetheless **not deployable as an IC decision document or as sell-side
research** in their current form. The gaps are structural, not defects:

1. **No compliance/supervisory wrapper.** No Reg AC certification, no FINRA 2241
   disclosure package, no supervisory-analyst approval, no recordkeeping/WORM
   control, incomplete conflict disclosure. The disclaimers are scope statements,
   not controls.
2. **No valuation, recommendation, or position sizing.** All three explicitly
   refuse DCF/SOTP/fair value, rating, price target, and sizing. They stop before
   the decision a PM must make.
3. **No independent forecasts.** Consensus is the denominator, not a forecast;
   there is no variant view versus the Street.

### Findings by severity

| Severity | Count | Blocks |
|---|---|---|
| Critical | 2 | Any client distribution; any IC use as the decision document |
| High | 6 | IC use as a decision input without a separate valuation/forecast memo |
| Medium | 8 | Enterprise deployment; cross-cycle accuracy |
| Low | 4 | Housekeeping |
| **Total** | **20** | |

### Three actions required before any IC deployment

1. **C-1** — Either implement a compliance/supervisory wrapper, or enforce
   internal-use-only scope operationally (distribution controls + legal sign-off).
2. **C-2** — Commission the valuation/recommendation/position-sizing module;
   these skills become an input to the IC memo, not the memo.
3. **H-2 + H-1** — Port a number registry into `bigtech-equity-research`, and add
   an independent forecast with a consensus bridge.

Everything else is maintenance-grade and can follow.

---

## 2. Scope, method, and verification ledger

### 2.1 Evidence base

- All three `SKILL.md` files, read in full.
- Reference documents: methodology, postmortem framework, fact-base schema,
  report design, segment maps, peers, sourcing and confidence, formulas, templates.
- Script inventory and key scripts: `fact_base_audit.py`, `fact_base_lite_audit.py`,
  `note_audit.py`, `quant_helpers.py`, `segment_map_check.py`, `provenance_seal.py`,
  `audit_all.sh`.
- Repository tests and self-audit: `tests/test_repo_consistency.py`,
  `tests/test_note_audit.py`, `docs/skills-audit/`.

### 2.2 Verification ledger

| Claim class | Method | Result | Confidence |
|---|---|---|---|
| Skill text, references, templates read | Full-text inspection | Complete | Verified |
| Script source inspected | Read from repository | Inventory complete; some views truncated at a sentinel | Verified (inventory) / partial (body) |
| Scripts executed | Not run — no runner in this environment | Not executed | **Unverifiable** |
| Test suite executed | Not run | Not executed | **Unverifiable** |
| Local clone / `git` state | Not performed | — | **Unverifiable** |
| Absence of DCF / rating / PT / Reg AC / supervisory approval | Full-text inspection of all three skills and templates | Absence confirmed | Verified |
| Internal script behavior (beta window, gate coverage) | Source reading | Inferred, not executed | Reasoned |
| Regulatory conclusions (Reg AC, FINRA 2241, Reg FD, 10b-5) | Doctrine reading + source inspection | Legal characterization only; not legal advice | Reasoned |
| Market-regime claims (beta smoothing across 2022/2023) | Domain reasoning | Plausible, not measured | Reasoned / Assumed |
| Third-skill gate inventory (which scripts ship) | Folder + SKILL gate list inspection | Confirmed no `fact_base_audit*` equivalent | Verified |

**Statement for the reviewer:** no script, test, linter, or build was executed in
this review. Any statement about script *pass/fail* is absent by design. Statements
about script *content and coverage* are Verified by reading; statements about
runtime behavior are Reasoned. The exact commands a reviewer should run to close
the Unverifiable gaps are in §7.4.

### 2.3 Confidence taxonomy (applied to every finding)

- **Verified** — inspected directly in the repository text.
- **Reasoned** — logical inference from inspected code/text; not executed.
- **Assumed** — rests on a stated assumption.
- **Unverifiable** — environment did not permit checking.

### 2.4 Severity taxonomy and escalation rule

| Severity | Definition | Release impact |
|---|---|---|
| Critical | Security, regulatory, data-integrity, or decision-integrity risk that invalidates the artifact's stated use. | Blocks release / blocks IC use. |
| High | Incorrect or unverifiable behavior in a common path; missing control on a critical flow. | Blocks IC use as sole input. |
| Medium | Edge-case defect, cross-cycle accuracy risk, or enterprise-deployment gap. | Fix within a maintenance cycle. |
| Low | Style, convention, housekeeping. | Backlog. |

**Escalation rule:** any Medium whose severity depends on firm policy is marked
`Policy-dependent` and carries an explicit note stating the condition under which
it becomes High. One finding (M-6) is so marked.

### 2.5 Limitations

- This is a **desk audit of public repository content**, not a live-system review.
- No runtime evidence; the Unverifiable rows above must be closed before sign-off.
- Legal characterizations are descriptive, not legal advice; counsel must confirm
  the Reg AC / FINRA 2241 / Reg FD positions.
- Two prior audits were merged; their individual limitations carry forward.

---

## 3. Findings — Critical

### C-1. No compliance or supervisory wrapper; disclaimers are not controls

- **Location:** `analyzing-us-bigtech-stocks/SKILL.md` §Distribution & compliance;
  `big-tech-earnings-postmortem/SKILL.md` final compliance block;
  `bigtech-equity-research/reference/sourcing-and-confidence.md` disclaimer.
- **Description:** All three explicitly disclaim sell-side status ("no rating, no
  price target, no analyst certification (Reg AC) or FINRA 2241 disclosure
  package"). That is a scope choice, not a compliance substitute: whether a
  document is a research report turns on content and distribution, not the
  author's self-label. The artifacts contain price-move attribution, forward
  multiple bands, implied moves, and segment analysis a reader could reasonably
  treat as research.
- **Evidence:** No analyst certification; no rating/PT definitions; no rating
  distribution; no investment-banking-client disclosure; no ownership or
  market-making disclosure; no compensation disclosure; no supervisory-analyst
  approval; no quiet-period or restricted-list control. The only conflict
  disclosure is a fund-position field for IC audiences.
- **Impact:** If produced inside a broker-dealer or distributed to clients, the
  artifacts may trigger recordkeeping, certification, and disclosure obligations
  they do not satisfy. Even internally, conflict disclosure is incomplete for a
  fiduciary IC memo.
- **Severity:** Critical.
- **Recommended fix:** Choose one: (a) harden scope operationally — legal review,
  internal-use-only distribution controls, a prominent "not a research report"
  legend, and a block on client distribution; or (b) add a sell-side compliance
  module: Reg AC certification, FINRA 2241 disclosure package, rating/PT
  framework, supervisory sign-off, WORM-style recordkeeping. For buy-side use,
  add full conflict declarations (personal holdings, compensation, outside
  interests) and compliance approval.
- **Confidence:** Verified (omissions visible); regulatory consequence Reasoned.

---

### C-2. No valuation, recommendation, or position sizing; cannot support an IC decision

- **Location:** `analyzing-us-bigtech-stocks` Phase 8; `big-tech-earnings-postmortem`
  Step 7; `bigtech-equity-research` hard rule 10 and `templates/report-structure.md` §11.
- **Description:** All three refuse DCF, SOTP, scenario-weighted fair value, a
  rating, a price target, and position sizing. They define themselves as
  causal-attribution products. That is honest, but they stop before the decision
  a fund manager needs: *what is it worth, what should we do, how large, and what
  is the risk/reward?* The alternative audit's "no EV sizing" point (its Finding 5)
  is a component of this gap and is tracked separately as **H-6** because it is a
  distinct, tractable deliverable.
- **Evidence:** "No DCF / SOTP / scenario-weighted fair value is produced" appears
  in every skill. The equity-research template includes a forward-multiple band
  explicitly framed as "context, not intrinsic valuation." No recommendation
  section, no expected return, no position-sizing framework, no downside/upside
  ratio.
- **Impact:** A PM must commission a separate valuation and decision memo. The
  artifact informs an IC discussion but cannot be the IC decision document.
- **Severity:** Critical.
- **Recommended fix:** Add a valuation module (DCF, SOTP, reverse DCF, comps,
  scenario-weighted fair value) and a recommendation/position-sizing section with
  expected return, downside, and risk budget — or integrate a dedicated valuation
  skill and require its output before IC delivery. H-6 is the minimum viable
  subset.
- **Confidence:** Verified.

---

## 4. Findings — High

### H-1. No proprietary forecasts, earnings model, or variant view

- **Location:** `bigtech-equity-research/reference/methodology.md` Phase 1;
  `big-tech-earnings-postmortem` Step 2; flagship Phase 1.
- **Description:** The skills compute beat/miss against consensus but build no
  independent revenue, margin, EPS, capex, or FCF forecasts. Consensus is a
  denominator, not a forecast. Institutional standard expects the analyst's own
  estimates and an explicit variant view versus the Street.
- **Evidence:** No model file, no assumption table, no consensus bridge, no
  estimate-revision tracking.
- **Impact:** Reactive rather than forward-looking; cannot identify where the
  analyst differs from the Street — the core of alpha generation.
- **Severity:** High.
- **Recommended fix:** Require a forward model with explicit assumptions and a
  consensus bridge showing the variant view.
- **Confidence:** Verified.

### H-2. `bigtech-equity-research` ships no machine-checked number registry

- **Location:** `bigtech-equity-research/SKILL.md` folder structure and delivery gates.
- **Description:** The skill bundles `note_audit.py` (placeholders/disclosures),
  render, a11y, provenance, `segment_map_check.py`, `quant_helpers.py` — but **no
  `fact_base_audit.py` or `fact_base_lite_audit.py`**. Its Definition of Done
  requires every figure to carry a citation and confidence tag, but nothing
  machine-checks that printed numbers trace to a registry. The less quantitative
  postmortem has the *stronger* numeric gate.
- **Evidence:** Folder inventory and gate list; compare to postmortem which
  bundles `fact_base_lite_audit.py`.
- **Impact:** A quantitative note with segment tables and options math can ship
  with untraceable numbers. The audit checks disclosures and rendering, not
  number-to-source integrity. This is the most surprising inconsistency in the family.
- **Severity:** High.
- **Recommended fix:** Port `fact_base_lite_audit.py` (or the flagship's full
  `fact_base_audit.py`) and require every money/percentage figure to be registered.
- **Confidence:** Verified.

### H-3. Event-window convention can mis-specify T+0 vs T+1

- **Location:** flagship Phase 0; postmortem Step 1.
- **Description:** Both define the primary reaction as "the first full-session
  close after the event (T+1 close)." Correct for after-close earnings; wrong for
  intraday events (guidance shock, regulatory ruling, product launch), where the
  first full-session close is T+0.
- **Evidence:** Stated rule applies a single convention across all event types.
- **Impact:** Using T+1 for an intraday event adds an extra day, contaminating the
  event return, benchmark excess return, and attribution.
- **Severity:** High.
- **Recommended fix:** Define the window by event timestamp relative to market
  hours: pre-market → T+0 close; intraday → T+0 close; after-close → T+1 close.
  State the rule in the event charter.
- **Confidence:** Reasoned.

### H-4. Market-cap delta formula ambiguous for multi-class share structures

- **Location:** flagship Phase 2; postmortem Step 1.
- **Description:** "Shares outstanding × Δprice" does not specify total shares
  across classes or per-class prices.
- **Evidence:** For GOOG/GOOGL, META Class A/B and similar, using one class's
  shares and price can misstate the market-cap change.
- **Impact:** Market-cap loss/gain figures can be materially wrong when share
  classes diverge.
- **Severity:** High.
- **Recommended fix:** Require total diluted shares across all classes and a
  class-weighted price, or compute each class separately and sum. Disclose method.
- **Confidence:** Reasoned.

### H-5. No model validation, backtest, or accuracy track record

- **Location:** All three skills; no validation file or backtest in the repository.
- **Description:** The attribution methodology (hypothesis tree, two-axis
  classification, ranking heuristic) is a model. No out-of-sample validation, no
  accuracy record, no sensitivity analysis. Against bank model-risk standards
  (SR 11-7-style governance), this is a gap.
- **Evidence:** No validation set, no benchmark of attribution accuracy, no
  documented false-positive rate.
- **Impact:** Correctness rests on face validity. A PM cannot see how often the
  RCA correctly identifies the dominant driver.
- **Severity:** High.
- **Recommended fix:** Build a validation set of historical events with known
  outcomes; measure attribution accuracy; publish a methodology validation note.
- **Confidence:** Reasoned.

### H-6. No probabilistic scenario weighting / expected-value framework

- **Location:** All skills — Phase 8 / Step 6 / Phase 7 (scenarios).
- **Description:** The skills correctly ban price targets but ask only for
  Bull/Base/Bear *narratives* and *falsifiers*. There is no requirement to weight
  fundamental outcomes (e.g., FCF in Bull vs Bear) or to produce an
  expected-value-adjusted fundamental range. Originates in the alternative audit
  as "Finding 5," there rated Informational; **this audit elevates it to High**
  because unweighted scenarios are unfalsifiable narratives that cannot feed
  sizing, and because it is the minimum viable subset of C-2.
- **Evidence:** Phase 8 mandates three scenarios with falsifiers; the schema and
  audit gates provide no Expected Fundamental Value matrix.
- **Impact:** The output is a rigorous post-mortem without the quantitative
  asymmetry profile portfolio construction requires.
- **Severity:** High (elevated from Informational — see §8.2).
- **Recommended fix:** Permit (and for IC use, require) an "Expected Fundamental
  Value" matrix assigning subjective probabilities to fundamental outcomes,
  producing an EV-adjusted fundamental range. Keep it strictly separate from a
  "price target."
- **Confidence:** Reasoned.

---

## 5. Findings — Medium

### M-1. Consensus vintage window too loose; mean-vs-median not enforced

- **Location:** flagship Phase 1; postmortem Step 2.
- **Description:** ~10-day consensus vintage window; the audit checks presence of
  `consensus_vintage` but does not enforce mean-vs-median disclosure.
- **Impact:** Stale or incomparable consensus makes every beat/miss delta wrong.
- **Severity:** Medium.
- **Fix:** Default to 1–3 trading days; require mean vs median disclosure.
- **Confidence:** Reasoned.

### M-2. No SEC Reg G / Item 10(e) non-GAAP reconciliation framing

- **Location:** flagship Phase 6; postmortem Step 2.
- **Description:** Non-GAAP analysis without a reconciliation checklist.
- **Impact:** Non-GAAP commentary may not meet regulated-research disclosure standards.
- **Severity:** Medium.
- **Fix:** Add a Reg G/Item 10(e) checklist; require the reconciliation table.
- **Confidence:** Reasoned.

### M-3. Public-source-only; no primary research

- **Location:** Source-tier tables in all three skills.
- **Description:** No channel checks, expert calls, surveys, or management access.
- **Impact:** Limits differentiated insight; the artifact is a sophisticated
  public-source synthesis.
- **Severity:** Medium.
- **Fix:** Add an optional primary-research module, or state "public-source-only"
  as a hard limitation in every deliverable.
- **Confidence:** Verified.

### M-4. Data licensing and vendor redistribution rights not addressed

- **Location:** Source tiers (Yahoo, Stooq, Macrotrends, TIKR, FactSet/Visible
  Alpha via outlets).
- **Description:** No data-governance checklist for redistribution of vendor data
  in deliverables.
- **Impact:** Legal and licensing risk in enterprise deployment; redistribution
  without rights is a compliance exposure.
- **Severity:** Medium.
- **Fix:** Add a data-licensing checklist; prefer licensed feeds; prohibit
  redistribution without rights.
- **Confidence:** Reasoned.

### M-5. Postmortem claims "standalone" but depends on external `quant_helpers.py`

- **Location:** `big-tech-earnings-postmortem` (bundle/standalone statement).
- **Description:** Arithmetic helper lives in a sibling skill. If absent, the agent
  may hand-code arithmetic, violating compute-don't-recall.
- **Impact:** Silent integrity failure in isolation.
- **Severity:** Medium.
- **Fix:** Bundle a minimal arithmetic helper.
- **Confidence:** Verified.

### M-6. No temporal provenance gate against pre-filing contamination — *Policy-dependent*

- **Location:** All three skills, Phase 1 / Step 1 / Workflow Phase 1.
- **Description:** The skills mandate T1 sourcing for fundamentals but do not
  enforce a temporal ordering that separates *pre-event inputs* (consensus,
  positioning, prior guidance, options OI) from *post-event facts*. An agent can
  ingest leaked or unconfirmed pre-filing chatter and tag it as "News" or
  "Consensus." The audit scripts check `consensus_vintage` and `cross_checked_with`,
  not a hard temporal ordering against the verified T1 filing timestamp.
  **Correction to the alternative audit:** the original finding characterized this
  as "violates Reg FD principles and risks insider trading liability." That conflates
  three regimes — Reg FD binds issuers/persons acting on their behalf against
  selective disclosure (not an analyst documenting a leak); 10b-5 liability attaches
  to *trading* on MNPI in breach of duty, not to writing a memo; and the realistic
  risk here is **data-integrity contamination**, not issuer disclosure liability.
  The **original fix is also flawed**: stripping any non-T1 source retrieved before
  the T1 filing time would strip legitimate pre-event inputs. The corrected control
  is a `data_type` discriminator (pre-event input vs post-event fact) plus temporal
  ordering applied only to post-event claims.
- **Impact:** An IC memo can cite unconfirmed pre-filing information as fact.
  Data-integrity and market-abuse-adjacent exposure.
- **Severity:** Medium. **Policy-dependent:** escalates to High under any firm
  policy that treats pre-filing information handling as a controlled process.
- **Fix:** Implement `pre_filing_embargo` in the fact-base schema and audit
  scripts: tag each entry `pre_event_input` or `post_event_fact`; for
  `post_event_fact`, require `retrieved_at ≥ verified T1 filing time`, else flag
  `Unverifiable` and exclude.
- **Confidence:** Reasoned.

### M-7. Static beta regime assumption with no quantitative trigger

- **Location:** `big-tech-earnings-postmortem` Step 1; `bigtech-equity-research`
  Phase 2 / Hard Rule 3.
- **Description:** The canonical default (2-year monthly returns vs QQQ) is
  hardcoded. Big Tech experienced regime shifts (2022 rate shock, 2023 AI
  re-rating); a 24-month window smooths breaks. The text permits override "if the
  company's risk profile structurally changed" but delegates detection entirely
  to the LLM with no quantitative trigger.
- **Impact:** The "idiosyncratic shock" is mathematically distorted when
  correlation has broken down; market-driven moves can be attributed to company
  specifics.
- **Severity:** Medium.
- **Fix:** Enhance `scripts/quant_helpers.py` to emit `R_squared` and a
  `volatility_regime_flag`; if R² < 0.30 or trailing 3-month realized vol > 2σ
  from the 2-year mean, force explicit justification of the beta window or use a
  shorter (e.g., 6-month daily) window.
- **Confidence:** Reasoned.

### M-8. Survivorship and corporate-action blindness in peer baskets

- **Location:** `reference/peers.md` and Phase 4 (Peer Context) across all skills.
- **Description:** Canonical peer baskets are static; no automated check for M&A,
  spin-offs, delistings, or index changes since the cache. **Correction to the
  alternative audit's fix:** it proposed verifying basket constituents against "an
  authoritative index or exchange API." These are *bespoke analyst baskets* (e.g.,
  hyperscalers), not index constituents, so an index-membership API is the wrong
  control. The correct control is a corporate-action/news check on each named
  constituent plus a cache-age gate.
- **Impact:** Comparing FCF yield to a basket that lost a distressed constituent
  flatters the basket and makes the target look worse than it is.
- **Severity:** Medium.
- **Fix:** Add a `corporate_action_check` over each named constituent and a
  cache-age gate before computing the cross-section.
- **Confidence:** Reasoned.

---

## 6. Findings — Low

| ID | Finding | Location | Fix | Confidence |
|---|---|---|---|---|
| L-1 | Long `SKILL.md` files (~348 and ~371 lines) increase context load and instruction-following risk | Both long SKILL.md files | Keep `SKILL.md` as a router; move detail to references | Reasoned |
| L-2 | Stylized "Midnight IC" cover omits the conventional page-1 rating/PT/valuation box | flagship template | Add a conventional cover variant if C-1 and C-2 are implemented | Reasoned |
| L-3 | Node/Playwright/Python dependency versions not pinned | All skills | Add pinned versions/lockfile | Reasoned |
| L-4 | No microstructure/flow lens in the flagship hypothesis tree | `analyzing-us-bigtech-stocks` Phase 3 (lenses a–h) | Add lens (i) Market Microstructure & Flow (dealer gamma, CTA unwinds, index rebalances); require options OI skew check *when data is available* (T3/conditional given public-source constraint) | Reasoned |

---

## 7. Per-skill scorecard and remediation roadmap

### 7.1 Scorecard

Scale: **Strong / Adequate / Weak / Absent.**

| Dimension | `analyzing-us-bigtech-stocks` | `big-tech-earnings-postmortem` | `bigtech-equity-research` |
|---|---|---|---|
| Source discipline | Strong | Strong | Strong |
| Numeric traceability (machine gate) | Strong | Adequate | **Weak** (H-2) |
| Epistemic honesty | Strong | Strong | Strong |
| Segment/accounting rigour | Adequate | Adequate | Strong |
| Compliance wrapper | **Absent** (C-1) | **Absent** (C-1) | **Absent** (C-1) |
| Valuation / decision support | **Absent** (C-2) | **Absent** (C-2) | **Absent** (C-2) |
| Independent forecasts | **Absent** (H-1) | **Absent** (H-1) | **Absent** (H-1) |
| Model validation | Weak (H-5) | Weak (H-5) | Weak (H-5) |
| Maintainability / CI | Adequate | Adequate | Adequate |

Ranking by rigour: flagship > equity-research > postmortem.
Ranking by speed: postmortem > equity-research > flagship.
Ranking by Wall Street compliance: **none pass**; flagship closest only on audit trail.

### 7.2 Remediation roadmap

| Phase | When | Items | Effort |
|---|---|---|---|
| **0 — Blockers** | Before any IC use | C-1 (scope hardening or compliance wrapper), C-2 (valuation/recommendation/sizing module) | L |
| **1 — 30 days** | Before IC use as sole input | H-2 (port registry), H-1 (forecast + consensus bridge), H-6 (EV matrix), H-3 (event-window rule), H-4 (multi-class cap formula) | M |
| **2 — 90 days** | Before enterprise rollout | M-6 (temporal gate), M-7 (beta diagnostics), M-8 (corporate-action gate), M-1 (consensus vintage), M-5 (bundle helper), H-5 (validation harness) | M |
| **3 — Backlog** | Maintenance | M-2, M-3, M-4, L-1…L-4 | S |

Effort: S < 1 day, M 1–5 days, L > 5 days (module-level).

### 7.3 Sequencing note

H-6 is intentionally placed before full valuation work: an EV matrix over
fundamental outcomes is a low-cost, high-signal step that converts the existing
scenarios from narrative to quantitative and is a prerequisite input to the
C-2 valuation module.

### 7.4 Commands a reviewer should run to close the Unverifiable rows

```
git clone https://github.com/nordeim/my-pi-agent.git && cd my-pi-agent
# per skill:
python skills/<skill>/scripts/fact_base_audit.py --help     # confirm CLI
pytest -q tests/                                            # consistency + note audit
bash skills/<skill>/scripts/audit_all.sh                    # or equivalent runner
python -m compileall skills/<skill>/scripts                 # syntax
```
Record exit codes and output; attach to the sign-off. Until then, all script
pass/fail statements remain **Unverifiable**.

---

## 8. Reconciliation appendix

### 8.1 Source map

| Finding | Origin | Note |
|---|---|---|
| C-1, C-2 | Audit A | — |
| H-1, H-2, H-3, H-4, H-5 | Audit A | — |
| H-6 | Audit B (its Finding 5) | **Severity elevated** Informational → High |
| M-1…M-5 | Audit A | — |
| M-6 | Audit B (its Finding 1) | **Legal framing corrected; fix re-scoped; severity made Policy-dependent** |
| M-7 | Audit B (its Finding 2) | Severity retained Medium |
| M-8 | Audit B (its Finding 3) | **Fix re-scoped** (index API → per-constituent corporate-action check) |
| L-1…L-3 | Audit A | — |
| L-4 | Audit B (its Finding 4) | Severity retained Low; data-availability caveat added |

### 8.2 Corrections applied to Audit B

1. **"Correctly implements Reg AC" (executive summary)** — factually wrong. All
   three skills explicitly disclaim analyst certification under Reg AC. Corrected.
2. **"Correctly implements Reg FD gates" (executive summary)** — internally
   contradicted by Audit B's own Finding 1 (no temporal MNPI control). Corrected.
3. **"Separation of idiosyncratic from systematic risk correctly implemented"** —
   contradicted by Audit B's own Finding 2 (beta distortion). Reconciled as
   "implemented, accuracy regime-dependent" (M-7).
4. **MNPI / Reg FD / insider-trading conflation** — three regimes collapsed into
   one. Corrected in M-6; severity reduced High → Medium with a policy-dependent
   escalation clause.
5. **MNPI fix would strip legitimate pre-event inputs** — corrected via
   `data_type` discriminator in M-6.
6. **Peer-basket fix mis-scoped to index APIs** — corrected in M-8.
7. **EV sizing rated Informational** — elevated to High (H-6); the alternative's
   own impact statement ("lacks the profile needed for portfolio construction")
   is inconsistent with Informational.
8. **"Production-grade" conclusion** — overclaimed given C-1, C-2, H-1, H-2. Not
   carried into this document.

### 8.3 What is genuinely strong — do not regress

- T1/T2/T3 source tiering; primary-source-first; no aggregators for fundamentals.
- Confidence taxonomy: Verified / Reasoned (derived) / Reasoned (judged) / Assumed / Unverifiable.
- Machine gates: anchored number matching, consensus schema, epistemic split,
  waterfall sum check, segment-map staleness gate, provenance seal.
- Degraded mode: tools offline → shrink scope, tag Unverifiable, log the exact
  pull needed; never backfill from memory.
- Cross-skill consistency tests and CI guarding doctrine drift.
- Explicit scoping disclaimers and fund-position disclosure for IC audiences.

### 8.4 Standards gap matrix

| Standard | Sell-side bank | Buy-side fund manager | These skills |
|---|---|---|---|
| Analyst certification (Reg AC) | Required | Not typically | Absent (C-1) |
| Rating/PT + valuation method (FINRA 2241) | Required | Expected in IC memo | Absent (C-2) |
| Price chart with rating/PT history | Required | Expected | Absent |
| Rating distribution, IB-client, ownership, MM, compensation disclosures | Required | N/A / different | Absent (C-1) |
| Conflict disclosure | Required | Required (CFA VI(A)) | Partial — fund position only |
| Supervisory analyst / compliance approval | Required | PM/IC review | Absent (C-1) |
| Recordkeeping / WORM / audit trail | SEC 17a-4 | Firm policy | SHA-256 seal only; no WORM / firm-key signing |
| Independent forecasts / earnings model | Expected | Expected | Absent (H-1) |
| Intrinsic valuation / scenario-weighted fair value | Expected | Expected | Out of scope (C-2) |
| Recommendation, sizing, risk/reward | Required | Required | Absent (C-2) |
| Primary research / channel checks | Differentiator | Differentiator | Absent (M-3) |
| Data licensing / redistribution rights | Governed | Governed | Not addressed (M-4) |
| Model validation | Governed (SR 11-7-style) | Governed | Absent (H-5) |

---

## 9. Sign-off

| Role | Name | Date | Decision |
|---|---|---|---|
| Reviewer | ____ | ____ | ☐ Approved for internal research pre-read only ☐ Approved for IC input (with separate valuation memo) ☐ Blocked |
| Compliance | ____ | ____ | ☐ Scope limitation accepted ☐ Compliance wrapper required (C-1) |
| Model risk | ____ | ____ | ☐ Validation plan accepted (H-5) |

**Conditions of any approval:** Unverifiable rows in §2.2 closed by executed
commands (§7.4); C-1 and C-2 disposition recorded; H-1, H-2, H-6 scheduled.

---

*End of document.*
```

---

**Notes for when you save it:**

- Put it at `docs/skills-audit/reconciled-audit-v1.md` alongside the existing self-audit so version history stays co-located.
- The three `☐` decisions in §9 are deliberate: a compliance reviewer needs a recorded disposition, not just a findings list, or the document gets filed and forgotten.
- If you want, next step I can produce a **remediation ticket set** — one ticket per High/Critical finding with acceptance criteria and a test to prove closure — which is what turns this audit into an executable backlog.
