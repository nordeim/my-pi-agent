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

**Compute the beat/miss delta** for every headline metric — `actual − consensus` and the
percentage. The delta, not the absolute, is what moves price.
Formula: `reference/formulas.md#beatmiss-delta`.

**Tag:** `Verified` when a figure is consistent across ≥2 independent primary/near-primary
sources to the reported precision.

## Phase 2 — Isolate idiosyncratic vs market-wide move
**Goal:** separate the company-specific move from the market/sector component.

1. **Market-adjusted excess return** = stock return − same-day benchmark return. Use
   QQQ or XLK as the broad benchmark and the direct comps as a cross-check. If the
   Nasdaq fell 2% that day, the "company-specific" story is ~2pp smaller than
   headlines suggest. This is the *market-adjusted* form (implicitly beta = 1); for a
   high-beta name prefer the **beta-adjusted** form — stock return − `beta` × benchmark
   return — with a beta estimated over a stated pre-event window (e.g. 250 sessions
   vs QQQ) and the window disclosed. Do not call the benchmark return "beta": beta is
   a unitless sensitivity, not a percentage. Formula:
   `reference/formulas.md#market-adjusted-excess-return-not-alpha`.
2. **Options implied move** — the pre-print ATM straddle price vs the realized move.
   - Realized ≈ implied → market was already positioned; likely de-grossing, not surprise.
   - Realized ≫ implied → genuine surprise; the information content is higher.
3. Report the idiosyncratic residual as the number the root-cause analysis must explain.

**Tag:** benchmark closes and implied move are `Verified` only if pulled; otherwise `Assumed`
with a stated bound, and routed to the Data-Gap Ledger.

## Phase 3 — Segment-level attribution
**Goal:** find which segment(s) actually caused the delta.

Build a variance table across all reportable segments (map: `reference/segment-maps.md`):
columns = actual, consensus, Δ, YoY, QoQ trend, result.

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
  Consecutive negative-FCF quarters is a psychologically important threshold.
- Operating-margin trend and stated drivers (AI-infra depreciation, buildout, hiring).
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
  sector, not this company's print.

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
  accompany it only as a `Reasoned` analytical allocation: signed weights,
  disclosed method, confidence tag per factor — and labeled on the deliverable as
  an allocation, not a measurement. The weights summing to the realized move is an
  **arithmetic consistency check**, not evidence the factors caused the move.
  Never publish a quantified decomposition that pretends to be an observed
  regression or an event-study residual; if you want a real residual, compute one
  (Phase 2 beta-adjusted form) and disclose the model.
- Classify each driver **structural** (permanent to the franchise) vs **cyclical/accounting**
  (timing, non-cash, reversible). This classification is the single most important judgment and
  is always `Reasoned`, never presented as a reported fact.
- State explicitly when a weight is an analytical allocation rather than an observed regression.

Formula and worked example: `reference/formulas.md#root-cause-driver-decomposition-the-waterfall`.

## Pre-event mode ("what's priced in?")

When the request precedes the print, the deliverable is a setup note, not a
post-mortem:

1. **Consensus vs whisper**: published consensus (revenue, EPS, segment growth,
   capex) plus any sourced whisper/positioning color — labeled by tier.
2. **Implied move**: ATM straddle price / spot for the nearest expiry → the move
   the options market is pricing; compare to the realized moves of the last 4–8
   prints.
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
