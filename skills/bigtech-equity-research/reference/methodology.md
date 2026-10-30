# The 7-Phase Research Methodology

Company-agnostic. Apply to any US-listed big-tech name. Every phase ends with sourced,
confidence-tagged figures.

## Phase 1 — Ground truth (primary sources only)
**Goal:** establish the facts from primary sources, then compute the price-moving deltas.

Pull, in order of preference:
1. **SEC EDGAR** — the 8-K, earnings press release, and 10-Q (segment tables live here).
   Never rely on secondary summaries for segment splits.
2. **Official earnings-call transcript** — from the company's IR site, or a verified transcript
   provider (Motley Fool / Seeking Alpha / Investing.com) cross-checked against the audio.
3. **Exchange-sourced price data** — closing/after-hours/next-day from Nasdaq or a data vendor
   (Stooq, Yahoo Finance API) pulled programmatically, not eyeballed.
4. **Consensus estimates** — pre-print revenue, EPS, segment growth, capex from
   FactSet/Visible Alpha/Refinitiv (LSEG)-referencing notes or Bloomberg consensus
   **as reported by a named outlet**.

   **Consensus sourcing protocol (round 3, reports 6/7 H-1; tightened in round 4,
   reports 8/9 M-1):** the consensus is the
   denominator of every beat/miss delta, so it gets the same evidentiary rigor as
   the reported figures, not less. Wire copy rounds, prints the median instead of
   the mean, or carries a weeks-stale number — a $0.02 vs $0.05 miss is a different
   causal narrative. For every consensus figure:
   - record the **provider** (FactSet / Visible Alpha / LSEG / Bloomberg as
     reported), the **vintage** (the as-of date of the estimate set, **within 1–3
     trading days of the event** — the CONSENSUS gate default is 5 calendar days
     ≈ 3 trading days, tightened from 10), the **statistic**
     (`consensus_statistic`: mean / median / undisclosed — the recorded
     mean-vs-median disclosure; a $0.02-vs-$0.05 miss flips on which statistic the
     wire printed), and the **contributor count** when the provider discloses
     it;
   - source it from **T1/T2 only** — never a lone T3 aggregator print; when only a
     T2 chain is available, cross-verify across **two distinct origination chains**
     (e.g. Reuters AND a second outlet carrying a different provider's set), or the
     company's own IR page when it publishes tracked consensus;
   - state mean vs median on the note when the outlet discloses which it is printing.
   The flagship's `fact_base_audit.py` enforces this at the schema level
   (consensus facts without provider/vintage/statistic/T1-T2 tier fail the build),
   and the lite registry's `fact_base_lite_audit.py` checks provider + vintage +
   statistic on consensus-side entries.

**Temporal embargo discipline (round 4, reports 8/9 M-6).** Pin the verified T1
filing/publication time (8-K acceptance stamp, IR press-release timestamp) as
`meta.t1_filing_timestamp` in the number registry, and classify every entry
`data_type`: `pre_event_input` (consensus, positioning, prior guidance, options
OI — legitimately pre-event) or `post_event_fact` (anything the event itself made
knowable). A post-event fact retrieved before the filing time is pre-filing
contamination — flag it `Unverifiable` and strip it from the registry; the lite
audit's TEMPORAL check fails the build on it. A data-integrity control (never
launder unconfirmed pre-filing chatter into a confirmed fact), not a Reg FD
control.

**Compute the beat/miss delta** for every headline metric — `actual − consensus` and the
percentage. The delta, not the absolute, is what moves price.
Formula: `reference/formulas.md#beatmiss-delta`.

**Tag:** `Verified` when a figure is consistent across ≥2 independent primary/near-primary
sources to the reported precision.

## Phase 2 — Isolate idiosyncratic vs market-wide move
**Goal:** separate the company-specific move from the market/sector component.

**Event-window rule (round 4, reports 8/9 H-3)**: set the primary reaction by the
event's timestamp relative to market hours — after-close event → T+1 full-session
close; pre-market/intraday event (guidance shock, regulatory ruling, product
launch) → T+0 close. Applying T+1 to an intraday event contaminates the event
return and the benchmark excess return with an extra session. State the rule
applied in the note.

1. **Market-adjusted excess return** = stock return − same-day benchmark return. Use
   QQQ or XLK as the broad benchmark and the direct comps as a cross-check. If the
   Nasdaq fell 2% that day, the "company-specific" story is ~2pp smaller than
   headlines suggest. This is the *market-adjusted* form (implicitly beta = 1); for a
   high-beta name prefer the **beta-adjusted** form — stock return − `beta` × benchmark
   return — with a beta estimated over a stated pre-event window and the window
   disclosed. Do not call the benchmark return "beta": beta is a unitless sensitivity,
   not a percentage. `scripts/quant_helpers.py::abnormal_return` enforces the window
   discipline in code: a beta supplied without a window gets the **canonical default**
   (2-year monthly returns vs QQQ, `DEFAULT_BETA_WINDOW`) and echoes it; an explicit
   non-default window must be justified in the note (a corporate event that
   structurally changed the risk profile) — comparability across runs is the point.
   **Beta regime diagnostics (round 4, reports 8/9 M-7)**: before trusting the
   canonical window, run `quant_helpers.beta_diagnostics` (OLS beta, R²,
   correlation-breakdown flag) and `volatility_regime_flag` (trailing 3-month
   realized vol vs its 2-year mean, z-score). If R² < 0.30 or |z| > 2, the window is
   fitting a broken regime (2022 rate shock, 2023 AI re-rating) — justify it
   explicitly or re-estimate over a shorter (e.g. 6-month daily) window and disclose
   it. "Structurally changed" is a quantitative trigger now, not a vibe.
   Formula:
   `reference/formulas.md#market-adjusted-excess-return-not-alpha`.
2. **Options implied move** — the pre-print ATM straddle price vs the realized move.
   - Compute the straddle cost from the **T-1 closing options chain** (ATM call +
     ATM put closes for the nearest post-event expiry, over the T-1 close) — never
     a news article's quoted implied-move percentage; a wire figure may only
     cross-check, tagged `Assumed` with the outlet named.
   - Realized ≈ implied → market was already positioned; likely de-grossing, not
     surprise. Realized ≫ implied → genuine surprise; the information content is
     higher. **Volatility risk premium caveat:** implied exceeds realized on
     average, so "realized ≈ implied" can be a normal premium rather than
     positioning — state the name's historical average `realized/implied` ratio
     over a disclosed window (≥8 prior prints) or tag the read `Assumed`
     (heuristic). The lite audit's scoped needle fails the note when the implied-
     move discussion lacks this caveat.
   Formula: `reference/formulas.md#options-implied-move-vs-realized`.
3. Report the idiosyncratic residual as the number the root-cause analysis must explain.

**Tag:** benchmark closes and implied move are `Verified` only if pulled; otherwise `Assumed`
with a stated bound, and routed to the Data-Gap Ledger.

## Phase 3 — Segment-level attribution
**Goal:** find which segment(s) actually caused the delta.

Build a variance table across all reportable segments (map: `reference/segment-maps.md`;
compute each row with `scripts/quant_helpers.py::segment_variance`):
columns = actual, consensus, Δ, YoY, QoQ trend, result.

**Staleness gate (mechanical, round 3 — reports 6/7 H-3):** before building the
table, run
`python3 scripts/segment_map_check.py --map reference/segment-maps.json --filing-date <YYYY-MM-DD> [--company <TICKER>]`
against the filing you are actually using. It **fails the build** when the filing
postdates the map's `verified_through` — a stale map produces a confidently wrong
variance table that still passes the numeric audit, because nothing downstream
catches a misattributed segment. Doctrine: **the filing's own segment note (ASC 280,
usually Note 10–15) is the source of truth; the map is the cached baseline
expectation.** On a stale/unknown result, extract the segment structure from that
filing's segment note directly, update `segment-maps.md` AND `segment-maps.json`
(bump `segment_map_version`), then re-run the gate. Cite the filing (form type +
fiscal period) on the table, and print "Segment map: vintage verified against
<filing>" so the lite audit's scoped needle can check it.

Critical distinction:
- **Miss** = below consensus.
- **Deceleration** = above or at consensus but slower growth than prior period. The market
  often punishes deceleration even when a segment beats. Flag it explicitly.

Identify the cash-cow segment and the growth segment; the market reprices when the cash cow
decelerates because it funds the growth investment.

## Phase 4 — Cost structure / capex / margin
**Goal:** assess the investment intensity and its margin impact.

- Capex: actual vs prior guidance vs Street. Compute **capex/operating-cash-flow ratio**.
- **Free-cash-flow trajectory** across the last 4 quarters — the slope matters as much as level.
  Consecutive negative-FCF quarters is a psychologically important threshold. Pair
  every FCF figure with its **FCF ex-SBC companion** (OCF − capex − SBC, SBC from the
  cash-flow statement, T1): SBC is structurally material for US mega-cap tech, and
  FCF that ignores it overstates the cash generation available for buybacks and
  dividends. State which basis the beat/miss is computed on
  (`reference/formulas.md#fcf-trajectory`; `quant_helpers.fcf` / `fcf_ex_sbc`).
- Operating-margin trend and stated drivers (AI-infra depreciation, buildout, hiring).
- **Reg G / Item 10(e) discipline (round 4, reports 8/9 M-2)**: every non-GAAP metric
  presented (Adj. EPS, FCF, FCF ex-SBC) is reconciled to its most directly comparable
  GAAP measure — show the bridge or cite the issuer's own reconciliation table from
  the press release / 10-Q — and state which basis (GAAP vs non-GAAP) each beat/miss
  is computed on. Non-GAAP commentary without a reconciliation trail does not meet
  institutional disclosure standards.
- **Depreciation-schedule changes** — a frequent "stealth" driver of margin-compression fears.
  Check the CFO remarks / 10-Q MD&A explicitly.
- Derived insight to test: if capex beat Street but FCF still missed, the shortfall is in
  **operating cash flow**, not capex. Compute implied consensus OCF = consensus FCF + consensus
  capex, then compare to actual OCF. (`reference/formulas.md#ocf-shortfall`)

## Phase 5 — Qualitative / regulatory / macro overlay
**Goal:** rule out confounds that could be mistaken for an earnings reaction.

- **Antitrust/regulatory** — any DOJ/FTC/EU remedies or fines concurrent with the print. The
  company's ongoing docket (search, ad-tech, app-store) is a standing confound.
- **Macro same week** — rate moves, dollar, AI-capex sentiment across megacaps, any
  competitive-AI-cost shocks applicable to the date.
- **Peer read-through** — if comps reported the same week, their commentary may be driving the
  sector, not this company's print. Use the canonical basket for the name
  (`reference/peers.md`) or a documented alternative — same primary revenue driver,
  market-cap proximity, 2–4 names, basket and criteria stated in the note. Peer
  cherry-picking (a mega-cap's capex vs a mid-cap's) is a construction artifact, not
  a finding. **Constituent hygiene (round 4, reports 8/9 M-8)**: before the read-through,
  run a corporate-action check on each named constituent (M&A, spin-off, delisting,
  bankruptcy — a T2 news check per name; these are bespoke analyst baskets, not index
  constituents, so an index-membership API is the wrong control) and a cache-age gate
  (re-verify when basket facts are >90 days old or undated) — a basket that silently
  lost a distressed constituent flatters the peer average and misprices the target's
  relative position.

## Phase 6 — Sell-side reaction
**Goal:** capture how the Street repriced within 48 hours.

Compile rating/price-target changes from major desks (Goldman, Morgan Stanley, JPMorgan,
Evercore ISI, Wedbush, BofA, etc.), sourced from public research summaries picked up by wire
services (Reuters/Bloomberg/CNBC/TipRanks) — **not reconstructed from memory**. Record firm,
analyst, old/new rating, old/new PT, date, and stated rationale. Compute the average PT cut.
Note the pattern: *target cuts without downgrades* signals a time-horizon debate, not a
viability debate.

## Phase 7 — Root-cause attribution & synthesis (the "fund-manager output")
**Goal:** a ranked, confidence-tagged driver decomposition — judgment labeled as
judgment, never measurement dressed up as regression.

Rank the drivers of the realized move across:
- **(a) market-wide benchmark component** — from Phase 2.
- **(b) growth-segment deceleration** — e.g. cloud.
- **(c) capex/margin/FCF guidance.**
- **(d) one-time items** — legal charge, FX, portfolio mark-to-market, dilution.
- **(e) sentiment/positioning** — de-grossing, high implied move already priced.
- **(f) other / company-specific event, named** — executive departures, product
  recalls, idiosyncratic adverse rulings: anything that has no natural home in
  (a)–(e) gets its own named bucket, never force-fit into a canonical one.

Rules:
- The **ordinal ranking is the primary output.** A quantified allocation may
  accompany it only as a `Reasoned (judged)` analytical allocation: signed weights,
  disclosed method, confidence tag per factor — and labeled on the deliverable as
  an allocation, not a measurement. The weights summing to the realized move is an
  **arithmetic consistency check** (enforced by `quant_helpers.waterfall_check` and,
  in the flagship, by the WATERFALL schema gate), not evidence the factors caused
  the move. Deterministic derivations — GAAP bridges, delta arithmetic, options
  math — are `Reasoned (derived)` facts: they carry a formula and are reproducible;
  judgment allocations are not. Never publish a quantified decomposition that
  pretends to be an observed regression or an event-study residual; if you want a
  real residual, compute one (Phase 2 beta-adjusted form) and disclose the model.
- Classify each driver **structural** (permanent to the franchise) vs **cyclical/accounting**
  (timing, non-cash, reversible). This classification is the single most important judgment and
  is always `Reasoned`, never presented as a reported fact.
- State explicitly when a weight is an analytical allocation rather than an observed regression.

Formula and worked example: `reference/formulas.md#root-cause-driver-decomposition-the-waterfall`.

**Expected Fundamental Value matrix (round 4, reports 8/9 H-6 — optional, recommended
for IC-facing notes)**: weight the *fundamental* outcomes of the forward scenarios
with subjective probabilities (e.g. FY+1 FCF path bull/base/bear at 25/50/25) and
compute the EV-adjusted fundamental range in code — `Reasoned (judged)`
probabilities, method disclosed, strictly a fundamental-expectation construct,
**never a price target or a fair-value claim** (labeled adjacent to the matrix). An
unweighted scenario triptych cannot feed position sizing; the EV matrix is the
minimum quantitative asymmetry profile the family ships while the valuation module
stays out of scope.

**Variant-view annex (round 4, reports 8/9 H-1 — optional)**: when the engagement
asks for a forward view, build the analyst's own estimates (revenue / EPS / capex /
FCF) with an explicit assumption table and a **consensus bridge** (own − consensus
per line — where and why you differ from the Street); every input
`Assumed`/`Reasoned (judged)` and labeled, never presented as verified. When not
commissioned, name the forecast gap in the open-items list alongside the valuation
boundary.

## Pre-event mode ("what's priced in?")

When the request precedes the print, the deliverable is a setup note, not a
post-mortem:

1. **Consensus vs whisper**: published consensus (revenue, EPS, segment growth,
   capex) plus any sourced whisper/positioning color — labeled by tier, with
   provider + vintage per the Phase 1 consensus protocol.
2. **Implied move**: ATM straddle price / spot for the nearest expiry → the move
   the options market is pricing; compare to the realized moves of the last 4–8
   prints. Compute from the T-1 closing chain, and carry the volatility-risk-
   premium caveat (formula reference: `formulas.md#options-implied-move-vs-realized`).
3. **Positioning**: run-up into the print, distance from highs, index weight,
   ownership — only with sources.
4. **Scenario matrix**: bull/in-line/bear outcomes, each with "what would have to
   be true" and observable, dated confirmations. Probabilities, if assigned, are
   `Assumed` with stated reasoning — never presented as market-implied unless
   derived from options prices with the method shown.
5. **No prediction**: state falsifiers and the data that would confirm each
   scenario; the note says what is priced in, not what will happen.

## Trend-mode variant
For multi-quarter trend analysis (no single event), run Phases 1,3,4,5 and a trajectory version
of Phase 7: chart revenue/FCF/margin/multiple across 4–8 quarters, identify the inflection point,
and attribute the trend to (i) fundamental trajectory, (ii) multiple re-rating, (iii) sentiment/
flows. Add a **valuation-band** section (forward P/E and EV/FCF vs 3–5yr band).
