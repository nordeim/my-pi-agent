---
name: analyzing-us-bigtech-stocks
version: 1.2.0
description: "Produces institutional-grade, fact-based market research reports explaining US-listed big-tech stock price performance and trends — earnings reactions, guidance shocks, AI-narrative repricing, drawdowns and rallies — for companies such as GOOGL, MSFT, META, AMZN, AAPL, NVDA, TSLA. Use when asked why a stock moved, to run a root-cause analysis (RCA) on a price event, or to build a source-cited, evidence-based stock research report or multi-page deck with audit gates. This is the full-pipeline skill of the big-tech research family: hypothesis tree, GAAP bridge, machine-checked fact base, numeric + render audits. For a lighter single-file post-earnings note use big-tech-earnings-postmortem; for a quantified single-note with segment deep-dive use bigtech-equity-research. Enforces primary-source verification, confidence labels (Verified / Reasoned / Assumed / Unverifiable), and audit gates before delivery."
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
| `Reasoned` | Logical inference or computation from `Verified` inputs | The inference chain or formula is stated on the slide or in the fact base |
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
3. Define the reaction window: primary reaction = **first full-session close after the event (T+1 close)**; after-hours and T+0 intraday are secondary color.
4. Stamp the data cutoff ("prices as of close YYYY-MM-DD; analysis reflects information through YYYY-MM-DD HH:MM TZ") — it goes on the cover.
5. Agree the deliverable spec with the user (default: 12–16 page HTML deck, Midnight IC, no speaker notes, inline citations) and the audience (default: institutional PM/IC).
6. Write the one-page event charter before collecting data.

*Full checklist and worked examples: `references/methodology.md` §1.*

### Phase 1 — Build the fact base

1. Collect from **Tier 1** sources first: SEC filings (10-Q/10-K/8-K), company IR press release / shareholder letter, the earnings-call transcript, official company blogs. Tier 2 (Reuters, CNBC, Bloomberg, FT, WSJ, AP) supports consensus figures and market color. Tier 3 (Yahoo Finance, Macrotrends, TIKR, Stooq) supports price/market data only — never fundamental claims.
2. Log every fact as a structured record (metric, value, period, source, URL, retrieval time, confidence, cross-checks) in `fact_base.json` — schema in `assets/fact_base.template.json`, rules in `references/fact-base-schema.md`.
3. Cross-check every decision-critical number across ≥2 independent sources; if sources conflict, record both and flag the conflict — never silently pick one.
4. Derived numbers (percent moves, ex-item figures, market-cap deltas) are computed in code with the formula shown; they are labeled `Reasoned (derived)`.
5. Quote the exact source sentence for any judgment you plan to paraphrase (analyst quotes, guidance language) — paraphrase must not strengthen the claim.

*Source-tier table, price-data hygiene (share class, splits, adjusted closes), transcript protocol: `references/methodology.md` §2; schema: `references/fact-base-schema.md`.*

### Phase 2 — Quantify the market reaction

1. Compute the move: % change to T+1 close, after-hours print, absolute market-cap delta (shares outstanding × Δprice), distance from the 52-week/all-time high, YTD and 1-year context.
2. Build the same-day cross-section: S&P 500, Nasdaq-100, peer basket (for big tech: MSFT, META, AMZN, AAPL, NVDA at minimum) — this is what separates idiosyncratic repricing from systematic risk-off.
3. Verify any "worst day since IPO", "record wipeout", "biggest since" claim against a named source; if unverifiable, drop the ranking and state the plain numbers.
4. Note volume, options-implied volatility and flows **only if** you have a source for them.

*Formulas and the historical-ranking protocol: `references/methodology.md` §3.*

### Phase 3 — Construct the hypothesis tree

1. Generate 5–8 competing hypotheses using the eight lenses: (a) revenue miss, (b) margin/EPS miss, (c) segment-level deterioration, (d) guidance cut — explicit or hidden in call language, (e) capital-allocation regime break (capex/FCF), (f) structural narrative threat (e.g. AI cannibalizing the core product), (g) positioning/crowding unwind + macro tape, (h) one-off noise masquerading as a miss (impairments, fines, tax items).
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
2. Recompute "organic" figures with the one-offs removed and show the arithmetic on the slide (e.g. "FCF −$9.1B, of which a $5.2B one-off fine payment → ex-fine ≈ −$3.9B, in line with Street").
3. State which basis the market actually trades on (usually the consensus basis) — explaining the *wrong* miss is the most common RCA failure.
4. Label every recomputed figure `Reasoned (derived)` with the formula.

*One-off inventory and reconciliation procedure: `references/methodology.md` §7.*

### Phase 7 — Amplifiers & the overlooked case

1. Amplifiers explain the **depth**, never the **trigger**: pre-event run-up and crowding, macro backdrop on the day (rates, inflation prints, Fed path), sector tape (did peers fall too, or rotate?), same-week peer prints that primed the anxiety.
2. Build the counter-case on its own page: the 2–4 strongest verified datapoints the selloff ignored. Present as "what the market may be underweighting" — counter-evidence, not advocacy.
3. Every amplifier and every counter-case item needs its own source; two-sidedness is what makes the report credible.

*Amplifier checklist: `references/methodology.md` §8.*

### Phase 8 — Synthesis & forward frame

1. Compress the RCA into one sentence of the form: *"the market repriced [mechanism] when [evidence] arrived in the same print as [second evidence]"* — if you cannot, the analysis is not done.
2. Present a ranked driver table (ordinal ranks only; publish percentage attribution only if it is computable from sourced data — otherwise say attribution is qualitative).
3. Forward frame: 3 scenarios (bull/base/bear) each with "what would have to be true", explicit falsifiers, and a dated watchlist mapped to the hypotheses they would confirm or refute. Scenarios are analytic frames, not price targets — say so on the slide.
4. Do not publish price targets; do not use unsourced forecasts; mark all forward-looking statements `Reasoned`.

*Synthesis formulas and scenario rules: `references/methodology.md` §9.*

### Phase 9 — Produce the report

1. Write `slides_brief.json` **first** (per-page title, layout archetype, task brief with the exact figures and sources) — never build pages while inventing content. Skeleton: `assets/slides_brief.template.json`.
2. Follow the 15-page archetype map (cover → verdict → event timeline → scorecard → price action → hypothesis tree section → evidence pages → evidence matrix → overlooked case → Street reaction → scenarios → sources ledger). Spec and CSS tokens: `references/report-design.md`.
3. Every page carries: kicker, headline, source line, confidence chips. One idea per page; budget content to fit 1280×720 without overflow.
4. Build the page set plus a single keyboard-navigable viewer (`←`/`→`) linking all pages.
5. Use pure CSS for bars/ladders where possible; any chart library must render offline.

*Design system, archetypes, overflow-prevention budget: `references/report-design.md`.*

### Phase 10 — Audit & deliver

1. Run the numeric audit — every critical figure in the deck must match the fact base / checks file, derived-fact formulas must compute, `Assumed` facts must be listed on the method page, and placeholder tokens must be absent:
   `python3 scripts/fact_base_audit.py --slides <slides_dir> --fact-base <fact_base.json>`
   (designate the assumptions page via `meta.method_page` in the fact base or `--method-page`; `--checks checks.json` for the simple per-slide needle format; `--selftest` proves the script works).
2. Run the render audit — no overflow or clipping at 1280×720 measured against the slide element itself, fonts render, decorative bleeds marked `data-bleed`:
   `node scripts/overflow_audit.mjs --dir <slides_dir>` (`--selftest` proves the script works)
3. Fix the **generator/brief**, not the rendered page, when an audit fails; re-run until clean. Document any remaining false positives explicitly.
4. Deliver: pages + viewer + fact base + audit reports. Refresh data if the market has moved since the cutoff, or restate the cutoff.

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
| `scripts/fact_base_audit.py` | Phase 10 — numeric + placeholder audit (`--selftest` to verify) |
| `scripts/overflow_audit.mjs` | Phase 10 — Playwright render/overflow audit |

## Definition of done

- [ ] Event charter with data cutoff stamped on the cover
- [ ] `fact_base.json` complete; decision-critical numbers double-sourced
- [ ] ≥5 hypotheses tested; ≥1 explicitly excluded with evidence
- [ ] Every quantitative claim carries a confidence label; assumptions listed; `Unverifiable` gaps logged with the exact pull needed
- [ ] GAAP↔adjusted reconciliation shown; headline miss restated on comparable basis
- [ ] Benchmark/peer cross-section included; amplifier layer separated from trigger
- [ ] Counter-case ("what the market ignored") present and sourced
- [ ] One-sentence root cause + scenarios + falsifiers + dated watchlist; no price targets
- [ ] Sources & confidence ledger page with named sources and dates
- [ ] `fact_base_audit.py` exits clean (false positives documented if any)
- [ ] `overflow_audit.mjs` exits clean
- [ ] Disclaimer present: informational only, not investment advice

## Distribution & compliance

- **Information barrier hygiene**: these reports are built exclusively from public
  sources (filings, transcripts, press). Never incorporate material non-public
  information (MNPI); if any input is suspected to be MNPI, stop and escalate —
  see SEC Regulation FD.
- **Internal analytical artifact**: the output is an internal research pre-read for
  discussion, not sell-side research. It carries no rating, no price target, and no
  analyst certification (Reg AC) or FINRA 2241 disclosure package — do not
  distribute it as if it did.
- Every deliverable carries: "Informational only — not investment advice, not a
  solicitation. No price targets published."

## Top pitfalls (full catalog: `references/methodology.md` §13)

1. Explaining the wrong miss — GAAP vs adjusted basis confusion.
2. Attributing one-off noise (impairments, fines, tax) to narrative.
3. Quoting consensus estimates from memory instead of sourcing them.
4. Mixing the after-hours print with the close — the reaction is the T+1 close.
5. Wrong share class or split-basis prices (GOOG vs GOOGL is the classic).
6. Blaming macro when peers moved idiosyncratically the same day.
7. Fake-precision driver attribution percentages that no data supports.
8. Skipping call-transcript Q&A, where the real guidance signal lives.
9. "Worst since / record" claims recalled from memory instead of verified.
10. Shipping without the numeric and render audits.

## Adaptations

- **Lightweight post-mortem mode** (single-file note instead of the full deck): run Phases 0–8 at compressed depth following `references/postmortem-framework.md` §11 — the seven-section note sequence — and still pass both Phase 10 audit gates on the file. This is the mode the sibling skill `big-tech-earnings-postmortem` executes standalone.
- **Non-earnings events** (antitrust rulings, product launches, pre-announcements, executive changes): identical pipeline; swap the Phase 3 lenses for event-specific ones and keep the ≥1-exclusion rule.
- **Other US-listed large caps** (non-tech): the pipeline is identical; swap segment templates and peer baskets.
- **Language**: produce the report in the user's language; keep tickers, metric names and source titles in English.
- **Format**: default is the HTML deck + viewer; on request, convert to PDF or PPTX and state that badges/interactivity may degrade. Keep the HTML originals.
- **Data freshness**: if markets are open, timestamp the cutoff prominently and refresh before delivery.
