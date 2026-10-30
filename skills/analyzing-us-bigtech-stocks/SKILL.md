---
name: analyzing-us-bigtech-stocks
version: 1.6.0
description: "Produces institutional-grade, fact-based market research reports explaining US-listed big-tech stock price performance and trends — earnings reactions, guidance shocks, AI-narrative repricing, drawdowns and rallies — for companies such as GOOGL, MSFT, META, AMZN, AAPL, NVDA, TSLA. Use when asked why a stock moved, to run a root-cause analysis (RCA) on a price event, or to build a source-cited, evidence-based stock research report or multi-page deck. The full-pipeline skill of the big-tech research family: nine-lens hypothesis tree, GAAP bridge, machine-checked fact base, numeric + render + accessibility audits with consensus/epistemic/waterfall/mandate/temporal/snapshot schema gates, source-snapshot verification, SHA-256 provenance sealing, and --json CI output. For a lighter single-file post-earnings note use big-tech-earnings-postmortem; for a quantified single-note with segment deep-dive use bigtech-equity-research. Enforces primary-source verification, confidence labels, and audit gates before delivery."
license: Apache-2.0
compatibility: Requires web search and page-fetch tools for primary-source verification; Python >= 3.9 for the audit/quant scripts; render and accessibility audits need Node.js >= 18 with Playwright >= 1.40.
---

# Analyzing US Big-Tech Stocks — Event RCA & Trend Reports

## How to install and use this skill

Copy this folder into your agent's skill directory (e.g. `.claude/skills/analyzing-us-bigtech-stocks/`).
Read `SKILL.md` first; it is self-sufficient for the full pipeline. Open the reference files only
at the phase where the table in **Bundled resources** tells you to — this keeps context lean.

## Overview

This skill turns a stock-price question ("why did GOOG just drop 12%?") into an
institutional-grade root-cause analysis (RCA) report suitable for a portfolio-manager
investment-committee audience. The default deliverable is a 12–16 page HTML slide deck
(1280×720, "Midnight IC" design system) with inline source citations and confidence badges
on every claim, plus a keyboard-navigable viewer.

The method in one sentence: **build a verified fact base, quantify the move against
benchmarks, enumerate competing hypotheses, test each against the evidence, separate noise
from signal, and only then write the narrative — with every number traceable and every
claim confidence-labeled.**

Golden rules, in priority order (they override speed and word-count pressure):

1. **Numbers before narrative.** Never write a causal sentence you cannot attach numbers to.
2. **Primary sources only.** Every figure comes from a named, retrievable source (URL + retrieval date).
3. **Never fabricate.** If a number cannot be sourced, it is either found, computed (with formula shown), or marked `Assumed` — never invented, never recalled from memory.
4. **Competing hypotheses.** A single explanatory story is a red flag. Enumerate, test, and explicitly exclude at least one.
5. **Audit before delivery.** A report that has not passed the numeric and render audits is not finished.
6. **Compute, don't recall.** Never do arithmetic in-context (mentally, in the running text). Every delta, percentage, ratio, and multiple is executed in code — the fact base's formula fields, the bundled `scripts/quant_helpers.py` (byte-identical family copy), or a scratch script — and the code's output is what goes on the slide. In-context arithmetic is where transcription and magnitude errors enter.

## When to use / not use

**Use when the user asks to:**
- Explain a stock move (post-earnings, guidance shock, product/regulatory event, crash or rally)
- Produce a research report or deck on a stock's price performance and trend
- Run RCA on a repricing event ("what actually caused this?")
- Build an evidence-based bull/bear/counter-case for a big-tech name

**Not for:** trading signals, options strategies, intraday calls, price targets on request
(present scenarios and falsifiers instead and say why), or informal chat about markets
(for a quick question, answer directly without the full pipeline).

## The confidence system

Every quantitative or causal claim in the report carries exactly one label:

| Label | Meaning | Hard requirement |
|---|---|---|
| `Verified` | Observed directly in ≥1 named primary source; decision-critical numbers cross-checked in ≥2 independent sources | Source name + URL + retrieval date in the fact base |
| `Reasoned` | Inference or computation from `Verified` inputs — split into `Reasoned (derived)` (deterministic: formula + parents, reproducible) and `Reasoned (judged)` (analytical allocation, signed, non-causal) | The inference chain or formula is stated on the slide or in the fact base; `epistemic_kind` records which kind (audit-enforced) |
| `Assumed` | Stated assumption used because data was unavailable | Isolated, listed on the method page, minimized toward zero |
| `Unverifiable` | Source could not be retrieved with the tools at hand | Logged in the fact base with the exact pull needed to close the gap; never used in headline statistics |

Never present a `Reasoned` number as `Verified`, and never let an `Assumed` value into a
headline statistic. The final page of every report carries a confidence legend and lists
remaining assumptions and open data gaps.

## Pipeline (Phases 0–10)

```
0 Scope → 1 Fact base → 2 Reaction → 3 Hypotheses → 4 Test & classify
        → 5 Quantify mechanisms → 6 Noise exclusion → 7 Amplifiers & overlooked
        → 8 Synthesis → 9 Report production → 10 Audit & deliver
```

Phases 4–7 loop back to Phase 1 whenever testing exposes a missing fact. Do not start
Phase 9 until every hypothesis has a verdict.

| # | Phase | Key output | Exit gate |
|---|---|---|---|
| 0 | Scope & event definition | Event charter (trigger, ticker, window, deliverable spec, data cutoff) | Ticker class and reaction definition pinned in writing |
| 1 | Fact base | `fact_base.json` — every number sourced | All decision-critical numbers double-sourced |
| 2 | Reaction decomposition | Move size + benchmark cross-section | "Record/worst-since" claims verified, not recalled |
| 3 | Hypothesis tree | 5–8 hypotheses with falsifiable predictions | Tree covers fundamentals, capital allocation, narrative, positioning, macro, noise |
| 4 | Test & classify | Verdict per hypothesis | Every verdict cites ≥2 evidence items, for and against |
| 5 | Quantify mechanisms | 2–4 carrying numbers per surviving hypothesis | All derived numbers show their formula |
| 6 | Noise exclusion | GAAP↔adjusted reconciliation | Headline miss restated on a comparable basis |
| 7 | Amplifiers & overlooked case | Amplifier list + bull counter-case | Both sides sourced; report is two-sided |
| 8 | Synthesis | One-sentence root cause, scenarios, falsifiers, watchlist | No unsourced attribution percentages |
| 9 | Report production | `slides_brief.json` → HTML pages | Brief written before any page is built |
| 10 | Audit & deliver | Audit reports, viewer, handoff | Both audit scripts exit clean |

### Phase 0 — Scope & event definition

1. Pin the trigger event and its exact timestamp (e.g. "Q3 FY26 earnings + call, Oct 28 16:30 ET").
2. Pin the ticker **and share class** (GOOG vs GOOGL; pre/post-split basis) and the comparison indexes.
3. Define the reaction window by the **event-window rule (round 4, reports 8/9 H-3)**: an event after the close → primary reaction = **T+1 full-session close**; an event pre-market or intraday (guidance shock, regulatory ruling, product launch) → primary reaction = **T+0 close** — using T+1 for an intraday event contaminates the event return, the benchmark excess return, and the attribution with an extra session. State the rule and the chosen window in the event charter (`meta.reaction_definition`). After-hours and intraday prints are secondary color, always labeled as such.
4. Stamp the data cutoff ("prices as of close YYYY-MM-DD; analysis reflects information through YYYY-MM-DD HH:MM TZ") — it goes on the cover.
5. Agree the deliverable spec with the user (default: 12–16 page HTML deck, Midnight IC, no speaker notes, inline citations) and the audience (default: institutional PM/IC).
6. Write the one-page event charter before collecting data.

*Full checklist and worked examples: `references/methodology.md` §1.*

### Phase 1 — Build the fact base

1. Collect from **Tier 1** sources first: SEC filings (10-Q/10-K/8-K), company IR press release / shareholder letter, the earnings-call transcript, official company blogs. Tier 2 (Reuters, CNBC, Bloomberg, FT, WSJ, AP) supports consensus figures and market color. Tier 3 (Yahoo Finance, Macrotrends, TIKR, Stooq) supports price/market data only — never fundamental claims.
2. Log every fact as a structured record (metric, value, period, source, URL, retrieval time, confidence, cross-checks) in `fact_base.json` — schema in `assets/fact_base.template.json`, rules in `references/fact-base-schema.md`.
3. **Temporal embargo discipline (round 4, reports 8/9 M-6)**: pin the verified T1 filing/publication time as `meta.t1_filing_timestamp`, and classify every fact `data_type: pre_event_input` (consensus, positioning, prior guidance, options OI — legitimately pre-event) or `post_event_fact` (anything the event itself made knowable). A post-event fact retrieved before the filing time is pre-filing contamination — never launder unconfirmed pre-filing chatter into a confirmed fact: flag it `Unverifiable` and strip it. The audit's TEMPORAL gate enforces this mechanically. This is a data-integrity control, not a Reg FD control.
4. Cross-check every decision-critical number across ≥2 independent sources; if sources conflict, record both and flag the conflict — never silently pick one.
5. Derived numbers (percent moves, ex-item figures, market-cap deltas) are computed in code with the formula shown; they are labeled `Reasoned (derived)`; judgment allocations are `Reasoned (judged)` — the audit enforces the split (`epistemic_kind`).
6. Consensus figures carry a named provider, a fresh vintage, a recorded statistic, and a T1/T2 source: record `consensus_provider`, `consensus_vintage` (as-of date of the estimate set, within **1–3 trading days** of the event — the CONSENSUS gate's default is 5 calendar days ≈ 3 trading days, tightened from 10 in round 4, reports 8/9 M-1), `consensus_statistic` (`mean` / `median` / `undisclosed` — mean-vs-median is a recorded disclosure, not a courtesy; when the outlet does not say, the audit prints a NOTE and the licensed-feed pull goes in the Data-Gap Ledger, round 5 reports 10/11 §5.7), and `contributor_count` when disclosed; cross-verify a single T2 chain against a second distinct origination chain. The audit's CONSENSUS gate fails a consensus fact without them — the consensus is the denominator of every beat/miss delta (see `references/methodology.md` §2.3).
7. **Source snapshots — pin what was actually fetched (round 5, reports 10/11 §3.4/§6.9)**: the audit gates certify that the deck matches the fact base — internal consistency — not that the fact base matches the cited source. Close the ingestion-error gap on decision-critical pulls: save the fetched source content (press release, 8-K, transcript page) as a file, record it with `scripts/source_snapshot.py --record --url <url> --content <file> --out source_snapshots.json`, and reference the printed SHA-256 in the fact's `source_snapshot` field. The audit's SNAPSHOT gate (`--snapshots source_snapshots.json`) then fails the build if the fact base and the snapshot archive drift apart; `--strict-snapshots` requires every `Verified` fact to carry one; `source_snapshot.py --verify` re-hashes the saved content (tamper evidence); seal the snapshots with the deck via `provenance_seal.py --inputs`. Before delivery, re-open each decision-critical T1 snapshot and re-check the number against the raw text — the snapshot makes the re-verification pass possible; the pass itself is the analyst's checklist.
8. Quote the exact source sentence for any judgment you plan to paraphrase (analyst quotes, guidance language) — paraphrase must not strengthen the claim.

*Source-tier table, price-data hygiene (share class, splits, adjusted closes), transcript protocol: `references/methodology.md` §2; schema: `references/fact-base-schema.md`.*

### Phase 2 — Quantify the market reaction

1. Compute the move: % change to the primary-reaction close (per the Phase 0 event-window rule), after-hours print, absolute market-cap delta, distance from the 52-week/all-time high, YTD and 1-year context. **Market-cap delta for multi-class names (round 4, reports 8/9 H-4)**: compute each share class separately and sum — `quant_helpers.market_cap_delta` — never one class's shares with another class's price (GOOG/GOOGL, META A/B are the classics); disclose the method on the slide. For single-class names the per-class sum reduces to shares × Δprice.
2. Build the same-day cross-section: S&P 500, Nasdaq-100, peer basket (for big tech: MSFT, META, AMZN, AAPL, NVDA at minimum) — this is what separates idiosyncratic repricing from systematic risk-off. **Peer-basket hygiene (round 4, reports 8/9 M-8)**: before computing any cross-section or peer metric, run a corporate-action check on each named constituent (M&A, spin-off, delisting, bankruptcy — a T2 news check per name) and a cache-age gate (re-verify when the basket's facts are >90 days old or undated); a basket that silently lost a distressed constituent flatters the peer average and misprices the target's relative position.
3. Verify any "worst day since IPO", "record wipeout", "biggest since" claim against a named source; if unverifiable, drop the ranking and state the plain numbers.
4. Note volume, options-implied volatility and flows **only if** you have a source for them — and compute the options-implied move from the T-1 closing chain (ATM call + put closes for the nearest post-event expiry, over the T-1 close), never a news article's quoted percentage (a wire figure may only cross-check, tagged `Assumed`); carry the volatility-risk-premium caveat when interpreting realized vs implied (sibling skill's `reference/formulas.md#options-implied-move-vs-realized`). **Options open-interest skew (round 4, reports 8/9 L-4)**: when a source for pre-event OI/put-call skew is available (vendor-grade, often T3), record it as an amplifier input — if unavailable, log the pull in the Data-Gap ledger instead of guessing.
5. **Beta regime diagnostics when beta-adjusting (round 4, reports 8/9 M-7)**: run `quant_helpers.beta_diagnostics` (R² + correlation-breakdown flag) and `volatility_regime_flag` (trailing-vol z-score) on the estimation window. If R² < 0.30 or |z| > 2, the canonical 2-year monthly beta is fitting a broken regime — either explicitly justify the window or re-estimate over a shorter (e.g. 6-month daily) window and disclose it. Detection is quantitative, not a vibe.

*Formulas and the historical-ranking protocol: `references/methodology.md` §3.*

### Phase 3 — Construct the hypothesis tree

1. Generate 5–8 competing hypotheses using the nine lenses: (a) revenue miss, (b) margin/EPS miss, (c) segment-level deterioration, (d) guidance cut — explicit or hidden in call language, (e) capital-allocation regime break (capex/FCF), (f) structural narrative threat (e.g. AI cannibalizing the core product), (g) positioning/crowding unwind + macro tape, (h) one-off noise masquerading as a miss (impairments, fines, tax items), (i) **market microstructure & flow (round 4, reports 8/9 L-4)** — dealer gamma hedging, systematic CTA/trend-follower unwinds, index rebalancing flows: post-earnings moves are frequently amplified by forced flows, and attributing a flow-driven depth to a guidance cut misreads the event.
2. Write each hypothesis as a card: **statement → causal mechanism (event → belief change → flow → price) → 3+ predicted observables** that would confirm or falsify it.
3. Predictions must be falsifiable and checkable against the fact base ("if H2 is true, FCF should print below −$3.5B consensus").
4. The tree is the centerpiece of the report — build it before testing, and resist narrating a single story.

*Hypothesis card template and lens details: `references/methodology.md` §4.*

### Phase 4 — Test & classify hypotheses

1. For each hypothesis, list evidence FOR and evidence AGAINST, each item tied to fact-base entries; target ≥2 items per side.
2. Read the call transcript Q&A — guidance and tone shifts usually live there, not in the press release.
3. Assign each hypothesis exactly one verdict: `PRIMARY — narrative`, `PRIMARY — mechanical`, `CONTRIBUTOR`, `AMPLIFIER`, `NOISE`, or `EXCLUDED`.
4. Elimination is a finding, not a failure: at least one hypothesis must be explicitly excluded with evidence (e.g. "Cloud demand failure — excluded: Cloud beat at +103% with $561B backlog").
5. Separate what the market *said* (call language, analyst notes) from what the numbers *did*; both matter, but they are different evidence classes.

*Verdict definitions and elimination criteria: `references/methodology.md` §5. The two-axis durability × evidentiary-basis classification and the big-tech ranking heuristic: `references/postmortem-framework.md`.*

### Phase 5 — Quantify surviving mechanisms

1. For each surviving hypothesis, attach the 2–4 numbers that carry it (e.g. capex regime: Q3 capex, FY guide vs prior, next-year signal, FCF vs consensus).
2. Decompose the price move: ΔPrice ≈ ΔEPS × PE₀ + EPS₁ × ΔPE — state whether the move was estimate-cut or multiple-compression, using consensus EPS and implied forward multiples.
3. Track the Street's response: rating changes, price-target moves (before → after, named shops), consensus PT delta — and compare it with the stock's move (the gap is itself a finding).
4. Positioning evidence (pre-event run-up, index weight, ownership) only with sources.

*Mechanism templates per driver type and the valuation decomposition: `references/methodology.md` §6.*

### Phase 6 — Separate noise from signal

1. Reconcile GAAP vs adjusted results line by line; inventory every one-off: unrealized gains/losses on equity stakes, fines (paid **and** accrued), restructuring, tax items, legal reserves.
2. **Reg G / Item 10(e) discipline (round 4, reports 8/9 M-2)**: every non-GAAP metric presented (Adj. EPS, FCF, ex-SBC FCF) is reconciled to the most directly comparable GAAP measure — show the reconciliation on the slide, or cite the issuer's own Reg G reconciliation table from the press release/10-Q — and state which basis (GAAP vs non-GAAP) each beat/miss is computed on. Non-GAAP commentary without a reconciliation trail does not meet institutional disclosure standards.
3. Recompute "organic" figures with the one-offs removed and show the arithmetic on the slide (e.g. "FCF −$9.1B, of which a $5.2B one-off fine payment → ex-fine ≈ −$3.9B, in line with Street").
4. State which basis the market actually trades on (usually the consensus basis) — explaining the *wrong* miss is the most common RCA failure.
5. Label every recomputed figure `Reasoned (derived)` with the formula.

*One-off inventory and reconciliation procedure: `references/methodology.md` §7.*

### Phase 7 — Amplifiers & the overlooked case

1. Amplifiers explain the **depth**, never the **trigger**: pre-event run-up and crowding, macro backdrop on the day (rates, inflation prints, Fed path), sector tape (did peers fall too, or rotate?), same-week peer prints that primed the anxiety.
2. Build the counter-case on its own page: the 2–4 strongest verified datapoints the selloff ignored. Present as "what the market may be underweighting" — counter-evidence, not advocacy.
3. Every amplifier and every counter-case item needs its own source; two-sidedness is what makes the report credible.

*Amplifier checklist: `references/methodology.md` §8.*

### Phase 8 — Synthesis & forward frame

1. Compress the RCA into one sentence of the form: *"the market repriced [mechanism] when [evidence] arrived in the same print as [second evidence]"* — if you cannot, the analysis is not done.
2. Present a ranked driver table (ordinal ranks only; publish percentage attribution only if it is computable from sourced data — otherwise say attribution is qualitative).
3. State the **valuation boundary**: this is a causal-attribution product — it explains why the price moved and does **not** opine on whether the name is now mispriced. Say so in one line on the synthesis page and name the model gap as an open item ("no DCF / SOTP / scenario-weighted fair value is produced; a valuation pass would require forward estimates, a discount-rate framework, and scenario weights — logged as the open valuation item"). Until a valuation module exists, the deck is firewalled as an IC **pre-read attribution note** — an input to the IC memo, never the memo itself (round 4, reports 8/9 C-2).
4. Forward frame: 3 scenarios (bull/base/bear) each with "what would have to be true", explicit falsifiers, and a dated watchlist mapped to the hypotheses they would confirm or refute. Scenarios are analytic frames, not price targets — say so on the slide.
5. **Expected Fundamental Value matrix (round 4, reports 8/9 H-6 — optional, recommended for IC-facing builds)**: weight the *fundamental* outcomes across the scenarios with subjective probabilities (e.g. FY+1 FCF path in bull/base/bear at 25/50/25) and compute the EV-adjusted fundamental range in code — `Reasoned (judged)` probabilities, method disclosed, strictly a fundamental-expectation construct, **never a price target or a fair-value claim**. An unweighted scenario triptych cannot feed sizing; the EV matrix is the minimum quantitative asymmetry profile the family ships while the valuation module stays out of scope.
6. **Variant-view annex (round 4, reports 8/9 H-1 — optional)**: when the engagement asks for a forward view, build the analyst's own estimates (revenue/EPS/capex/FCF) with an explicit assumption table and a consensus bridge (own − consensus per line — where and why you differ from the Street); every input `Assumed`/`Reasoned (judged)` and labeled, never presented as verified. When not commissioned, name the gap in the open-items list alongside the valuation boundary.
7. Do not publish price targets; do not use unsourced forecasts; mark all forward-looking statements `Reasoned`.

*Synthesis formulas and scenario rules: `references/methodology.md` §9.*

### Phase 9 — Produce the report

1. Write `slides_brief.json` **first** (per-page title, layout archetype, task brief with the exact figures and sources) — never build pages while inventing content. Skeleton: `assets/slides_brief.template.json`.
2. Follow the 15-page archetype map (cover → verdict → event timeline → scorecard → price action → hypothesis tree section → evidence pages → evidence matrix → overlooked case → Street reaction → scenarios → sources ledger). Spec and CSS tokens: `references/report-design.md`.
3. Every page carries: kicker, headline, source line, confidence chips. One idea per page; budget content to fit 1280×720 without overflow.
4. The cover carries a **verification-status line** stating which gates the deliverable passed — e.g. "Verification status: full fact-base + render audits passed" (or "Draft — human verification required" with the reason if a gate could not run). Never leave it implicit.
5. Build the page set plus a single keyboard-navigable viewer (`←`/`→`) linking all pages.
6. Use pure CSS for bars/ladders where possible; any chart library must render offline.

*Design system, archetypes, overflow-prevention budget: `references/report-design.md`.*

### Phase 10 — Audit & deliver

1. Run both gates with one command (the wrapper fails the build if either gate fails):
   `bash scripts/audit_all.sh <slides_dir> <fact_base.json> [<checks.json>]`
2. The numeric audit — every critical figure in the deck must match the fact base / checks file, derived-fact formulas must compute, `Assumed` facts must be listed on the method page, and placeholder tokens must be absent:
   `python3 scripts/fact_base_audit.py --slides <slides_dir> --fact-base <fact_base.json>`
   (designate the assumptions page via `meta.method_page` in the fact base or `--method-page`; `--checks checks.json` for the simple per-slide needle format; `--selftest` proves the script works).
3. Opt-in strict compliance modes for institutional builds — `--strict-verified` (every `Verified` fact must carry ≥2 `cross_checked_with` entries), `--fail-on-unverified` (reverse-check "unverified candidates" become failures instead of a review list), `--decision-critical F-001,F-014` (named facts must be double-sourced; same effect as `meta.decision_critical` in the fact base), and `--strict-pages slide_02.html,slide_07.html` (unverified candidates on the decision-critical pages — executive summary, root-cause decomposition — become failures while page furniture elsewhere stays advisory). They are opt-in because the reverse-check is heuristic — default-strict would flag benign page furniture and invite disabling the gate. `STRICT=1 bash scripts/audit_all.sh …` turns the strict flags on.
3a. Always-on schema gates (round 3, reports 6/7): CONSENSUS (consensus-side facts need provider + vintage + T1/T2 tier, vintage within `--consensus-max-age-days` of the event — round 4 tightened the default to 5 calendar days ≈ 3 trading days and added the required `consensus_statistic` mean/median/undisclosed field, reports 8/9 M-1; a `undisclosed` statistic prints a NOTE pointing at the Data-Gap Ledger, round 5 reports 10/11 §5.7), EPISTEMIC (`Reasoned` facts declare `epistemic_kind: derived|judged`; derived requires a formula), WATERFALL (facts with a signed `weights` dict must sum to their `realized_move`), MANDATE (an IC-named `meta.audience` requires `meta.mandate_context` with `fund_position` + `position_as_of` — and, round 5 reports 10/11 §3.5, a declared `mandate_context` must be complete whatever the audience: the position disclosure is unconditional once a position exists), TEMPORAL (round 4, reports 8/9 M-6: when `meta.t1_filing_timestamp` is set, every fact declares `data_type` pre_event_input/post_event_fact and post-event facts must be retrieved at/after the verified filing time — pre-filing contamination fails the build), and SNAPSHOT (round 5, reports 10/11 §3.4: with `--snapshots source_snapshots.json`, a fact's declared `source_snapshot` hash must exist in the manifest — registry↔archive linkage; `--strict-snapshots` requires every `Verified` fact to carry one).
3b. **What the gates do NOT check (round 5, reports 10/11 §2.4/§3.4/§5.5 — say so, don't imply otherwise)**: a green gate run certifies *internal consistency* (deck ↔ fact base) and schema discipline — it does not certify source truth (the registry matching the cited filing; snapshots + the re-verification pass are the mitigation), the economic correctness of formula assumptions (arithmetic identity, not model validity), or the empirical calibration of the methodology (face validity only until the validation harness lands — see the methodology-status line). The verification-status line states which gates ran; it is not a track record.
3c. Round-5 audit flags: `--strict-temporal` (a date-only `retrieved_at` on the filing date fails instead of NOTE — for intraday-sensitive engagements), `--snapshots <manifest>` / `--strict-snapshots` (the SNAPSHOT gate), and `--json` (machine-readable summary on stdout, diagnostics on stderr — for CI pipelines consuming the gate directly).
4. Run the render audit — no overflow or clipping at 1280×720 measured against the slide element itself, fonts render, decorative bleeds marked `data-bleed`:
   `node scripts/overflow_audit.mjs --dir <slides_dir>` (`--selftest` proves the script works)
5. Fix the **generator/brief**, not the rendered page, when an audit fails; re-run until clean. Document any remaining false positives explicitly.
6. Accessibility gate (run alongside the render audit when the deck claims WCAG-AA): `node scripts/a11y_audit.mjs --dir <slides_dir>` checks `lang`, heading order, image alt text and AA text contrast per page.
7. Deliver: pages + viewer + fact base + audit reports. Refresh data if the market has moved since the cutoff, or restate the cutoff. The cover's verification-status line must reflect the final gate results.
8. Seal the deliverable (round 3, reports 6/7 C-2): `python3 scripts/provenance_seal.py --inputs <slides_dir>/slide_01.html … <fact_base.json> --out provenance.json` — embed the printed seal line on the cover next to the verification-status line and ship the sidecar with the deck; re-verify later with `--verify` (tamper evidence). When source snapshots are on record (Phase 1 step 7), include the manifest and the saved content files in `--inputs` so the seal covers the evidence trail end to end (round 5, reports 10/11 §6.9), and run `python3 scripts/source_snapshot.py --verify source_snapshots.json` first so the sealed snapshots are the verified ones.
9. The method page carries the **methodology-status line** (round 5, reports 10/11 §3.6): "Methodology status: empirically unvalidated — face validity only (validation harness pending)" — per `references/methodology.md` §15. A green gate run is not a track record; the reader must not have to guess that.

*Audit protocol and refresh rules: `references/methodology.md` §10–11.*

## Bundled resources

| File | Read when |
|---|---|
| `references/methodology.md` | Starting any engagement — full phase-by-phase playbook, source tiers, formulas, pitfall catalog |
| `references/postmortem-framework.md` | Canonical driver-attribution doctrine — two-axis classification (durability × evidentiary basis), ranking heuristic, risk/catalyst matrix, failure modes; read for lightweight post-mortem mode or when a family skill needs the shared framework |
| `references/fact-base-schema.md` | Phase 1 — fact record fields, confidence rules, worked examples |
| `references/report-design.md` | Phase 9 — Midnight IC tokens, 15-page archetype map, overflow budget |
| `assets/fact_base.template.json` | Phase 1 — starting skeleton with worked examples |
| `assets/slides_brief.template.json` | Phase 9 — deck-plan skeleton |
| `scripts/fact_base_audit.py` | Phase 10 — numeric + placeholder audit; always-on CONSENSUS / EPISTEMIC / WATERFALL / MANDATE / TEMPORAL / SNAPSHOT schema gates; opt-in `--strict-verified` / `--fail-on-unverified` / `--decision-critical` / `--strict-pages` / `--strict-temporal` / `--snapshots` / `--strict-snapshots`; `--json` for CI (`--selftest` to verify) |
| `scripts/quant_helpers.py` | Phases 2/5/6 — deterministic quant math (beat/miss deltas, beta-adjusted excess returns with the canonical window, beta regime diagnostics R²/vol-z, multi-class market-cap delta, FCF/ex-SBC, segment variance, waterfall checks); byte-identical family copy (`--selftest` via `python3 scripts/quant_helpers.py`) |
| `scripts/overflow_audit.mjs` | Phase 10 — Playwright render/overflow audit |
| `scripts/source_snapshot.py` | Phase 1 — source-truth snapshots: `--record` hashes the fetched source content into `source_snapshots.json` (the fact's `source_snapshot` references it), `--verify` re-hashes for tamper evidence (`--selftest` to verify); round 5, reports 10/11 §3.4/§6.9 |
| `scripts/a11y_audit.mjs` | Phase 10 — accessibility audit (lang / heading order / image alt / WCAG-AA contrast) |
| `scripts/provenance_seal.py` | Phase 10 — SHA-256 sealing of the fact base + rendered pages, `provenance.json` sidecar, `--verify` tamper check |
| `scripts/audit_all.sh` | Phase 10 — one-command wrapper running both gates with a combined exit code (`STRICT=1` adds the strict flags) |

## Definition of done

- [ ] Event charter with data cutoff stamped on the cover; event-window rule applied (after-close → T+1 close; pre-market/intraday → T+0 close) and stated in the charter
- [ ] `fact_base.json` complete; decision-critical numbers double-sourced (listed in `meta.decision_critical` and/or audited under `--strict-verified`)
- [ ] Decision-critical T1 pulls carry `source_snapshot` hashes; `--snapshots` linkage clean (or the no-snapshots NOTE is consciously accepted); `source_snapshot.py --verify` clean when snapshots exist (round 5)
- [ ] Facts classified `data_type` and temporally clean when `meta.t1_filing_timestamp` is set (TEMPORAL gate clean)
- [ ] ≥5 hypotheses tested; ≥1 explicitly excluded with evidence
- [ ] Every quantitative claim carries a confidence label; assumptions listed; `Unverifiable` gaps logged with the exact pull needed
- [ ] GAAP↔adjusted reconciliation shown (Reg G / Item 10(e) discipline); headline miss restated on comparable basis
- [ ] Benchmark/peer cross-section included; amplifier layer separated from trigger; peer-basket corporate-action check run
- [ ] Market-cap delta computed per-class and summed for multi-class names (method disclosed)
- [ ] Counter-case ("what the market ignored") present and sourced
- [ ] One-sentence root cause + scenarios + falsifiers + dated watchlist; no price targets; EV fundamental matrix (if included) labeled `Reasoned (judged)` — never a price target
- [ ] Valuation boundary stated (pre-valuation causal-attribution product; valuation model gap named as an open item; IC pre-read firewall)
- [ ] Sources & confidence ledger page with named sources and dates
- [ ] Verification-status line on the cover reflecting the final gate results; "not a research report" + "Public-source-only" legends on the cover
- [ ] Consensus facts carry provider + vintage + statistic + T1/T2 tier (CONSENSUS gate clean); an `undisclosed` statistic has its licensed-feed pull logged in the Data-Gap Ledger
- [ ] IC-facing builds disclose fund position via `meta.mandate_context` (MANDATE gate clean); a declared `mandate_context` is complete whatever the audience (round 5)
- [ ] Method page carries the methodology-status line: empirically unvalidated — face validity only (round 5)
- [ ] Provenance sealed: seal line on the cover, `provenance.json` shipped with the deck (snapshots included in `--inputs` when on record)
- [ ] `bash scripts/audit_all.sh …` exits clean (false positives documented if any)
- [ ] Disclaimer present: informational only, not investment advice

## Distribution & compliance

- **Information barrier hygiene**: these reports are built exclusively from public
  sources (filings, transcripts, press). Never incorporate material non-public
  information (MNPI); if any input is suspected to be MNPI, stop and escalate —
  see SEC Regulation FD. The temporal embargo (Phase 1) is the data-integrity
  control that keeps pre-filing chatter out of the fact base.
- **Internal analytical artifact — operational scope control (round 4, reports 8/9 C-1)**:
  the output is an internal research pre-read for discussion, **not a research report** —
  every deliverable carries that legend on the cover — and it is for internal use only:
  do not distribute to clients or outside the firm; any wider distribution requires
  compliance sign-off first. It carries no rating, no price target, and no analyst
  certification (Reg AC) or FINRA 2241 disclosure package — do not distribute it as
  if it did. Until a valuation module exists, firewalled as an IC pre-read attribution
  note (an input to the IC memo, not the memo).
- **Public-source-only limitation (round 4, reports 8/9 M-3)**: every deliverable
  states "Public-source-only" — no channel checks, expert calls, surveys, or
  management access inform the analysis. That is a stated limitation, not an
  aspiration.
- **Data licensing & redistribution (round 4, reports 8/9 M-4)**: figures quoted from
  vendors (Yahoo Finance, Stooq, Macrotrends, TIKR, consensus providers) are cited
  with attribution for internal analytical use; do not reproduce vendor tables or
  charts at scale in the deliverable, and do not redistribute the deliverable
  externally — redistribution rights belong to the licensed feeds, not to this
  artifact. Prefer licensed API access when the engagement has it.
- **Position & mandate disclosure (buy-side)**: when the deliverable is for an
  investment-committee audience, the fact base carries `meta.mandate_context`
  (`fund_position`, `position_as_of`, plus mandate constraints and author
  conflicts that could bear on independence — personal holdings in the covered
  name, compensation ties, outside interests, or an explicit "none declared") and
  the cover discloses the fund's position — CFA Institute Standard I(B) /
  CFA Standard VI(A) disclosure of conflicts, the buy-side counterpart of
  sell-side conflict disclosure. The audit's MANDATE gate enforces its presence;
  **round 5 (reports 10/11 §3.5): once any mandate context is declared — any
  position in the covered name — the disclosure is unconditional**: complete it
  (fund_position AND position_as_of) and disclose it on the deliverable whatever
  the audience, because a position does not stop being a conflict when the
  reader is not a committee. The sell-side certification package stays
  inapplicable by the family's standing scoping position.
- **Methodology validation status (round 5, reports 10/11 §3.6)**: the
  attribution methodology is empirically unvalidated — face validity only —
  until the validation harness lands (`references/methodology.md` §15). The
  method page says so; a green gate run is internal consistency, not a track
  record.
- Every deliverable carries: "Informational only — not investment advice, not a
  solicitation. No price targets published."

## Top pitfalls (full catalog: `references/methodology.md` §13)

1. Explaining the wrong miss — GAAP vs adjusted basis confusion.
2. Attributing one-off noise (impairments, fines, tax) to narrative.
3. Quoting consensus estimates from memory instead of sourcing them.
4. Mixing the after-hours print with the close — the reaction is the primary-reaction close per the event-window rule (T+1 for after-close events, T+0 for intraday).
5. Wrong share class or split-basis prices (GOOG vs GOOGL is the classic) — and one class's shares multiplied by another class's price in the market-cap delta.
6. Blaming macro when peers moved idiosyncratically the same day.
7. Fake-precision driver attribution percentages that no data supports.
8. Skipping call-transcript Q&A, where the real guidance signal lives.
9. "Worst since / record" claims recalled from memory instead of verified.
10. Shipping without the numeric and render audits.
11. In-context arithmetic — computing a delta or ratio mentally instead of in code (transcription and magnitude errors enter exactly here).
12. Applying a stale beta across a regime break (2022 rate shock, 2023 AI re-rating) without the R²/vol-z diagnostics — market moves get attributed to company failure.

## Adaptations

- **Lightweight post-mortem mode** (single-file note instead of the full deck): run Phases 0–8 at compressed depth following `references/postmortem-framework.md` §11 — the seven-section note sequence — and still pass both Phase 10 audit gates on the file. This is the mode the sibling skill `big-tech-earnings-postmortem` executes standalone.
- **Non-earnings events** (antitrust rulings, product launches, pre-announcements, executive changes): identical pipeline; swap the Phase 3 lenses for event-specific ones and keep the ≥1-exclusion rule.
- **Other US-listed large caps** (non-tech): the pipeline is identical; swap segment templates and peer baskets.
- **Language**: produce the report in the user's language; keep tickers, metric names and source titles in English.
- **Format**: default is the HTML deck + viewer; on request, convert to PDF or PPTX and state that badges/interactivity may degrade. Keep the HTML originals.
- **Data freshness**: if markets are open, timestamp the cutoff prominently and refresh before delivery.
