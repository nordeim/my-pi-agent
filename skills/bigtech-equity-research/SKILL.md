---
name: bigtech-equity-research
description: Produce institutional-grade, evidence-based equity research notes on US big-tech stocks (GOOGL, MSFT, AMZN, AAPL, META, NVDA, TSLA, and peers). Use when asked to explain a stock-price event (post-earnings move, guidance shock, regulatory action), analyze a multi-quarter price trend, attribute a drawdown to its drivers, or build a quantified waterfall of a price move. Outputs a self-contained HTML research note with sourced figures, confidence tags, and a ranked root-cause decomposition. Analytical output only — not investment advice.
version: 1.0.0
---

# Big-Tech Equity Research

## Skill folder structure

```
bigtech-equity-research/
├── SKILL.md                          # Entry point: triggers, hard rules, workflow
├── reference/
│   ├── methodology.md                # The 7-phase research process in full
│   ├── formulas.md                   # Quant math: alpha, deltas, waterfall
│   ├── segment-maps.md               # Reportable segments per big-tech company
│   └── sourcing-and-confidence.md    # Source hierarchy + confidence taxonomy
├── templates/
│   ├── report-structure.md           # 13-section HTML deliverable spec
│   └── evidence-ledger.md            # Verification ledger format
└── scripts/
    └── quant_helpers.py              # Deterministic delta/alpha/waterfall math
```
    
Turn "why did GOOGL drop after earnings?" or "what's driving the MSFT trend?" into a
fund-manager-quality, fact-based research note.

## Hard rules (read first)
1. **Never fabricate.** Every number is sourced or tagged `Unverifiable`. If a data tool is
   offline, tag the gap and state the exact pull needed — do not invent a figure.
2. **Beat/miss delta moves price, not the absolute number.** Always compute actual − consensus.
3. **Isolate the idiosyncratic move.** Subtract same-day index/peer return before calling a move
   "company-specific."
4. **Rank root causes** and classify each as *structural* vs *cyclical/accounting*. No flat lists.
5. **Tag every figure** with a confidence label: `Verified` / `Reasoned` / `Assumed` / `Unverifiable`.
6. **Label judgment as judgment.** Waterfall weights and structural-vs-cyclical calls are
   `Reasoned` analysis, not reported facts.
7. **No investment advice.** Forward-looking views are scenarios, not predictions.

## Step 0 — Pick the mode
| Request shape | Mode | Phases |
|---|---|---|
| "Why did X drop/spike after earnings/event?" | **Event post-mortem** | All 7 |
| "What's driving X's trend over recent quarters?" | **Trend analysis** | 1,3,4,5 + trajectory variant of 7 + valuation band |
| "Ahead of X's print, what's priced in?" | **Pre-event setup** | Consensus, positioning, implied move, scenarios |

## Workflow
1. **Ground truth (Phase 1)** — SEC EDGAR 8-K/10-Q/press release, official transcript,
   exchange-sourced price, consensus. Compute beat/miss deltas.
   → `reference/methodology.md#phase-1`
2. **Isolate alpha (Phase 2)** — abnormal return vs QQQ/XLK + direct comps; options implied
   move (ATM straddle) vs realized. → `reference/formulas.md`
3. **Segment attribution (Phase 3)** — variance table: actual vs consensus, QoQ + YoY, per
   segment. Distinguish **miss** from **deceleration**. → `reference/segment-maps.md`
4. **Cost/capex/margin (Phase 4)** — capex vs guidance vs Street; margin trend; depreciation-
   schedule commentary (a stealth margin driver).
5. **Macro/regulatory overlay (Phase 5)** — same-week macro, antitrust confounds, peer read-through.
6. **Sell-side reaction (Phase 6)** — PT/rating changes ≤48h, sourced from wire-service pickup.
7. **Root-cause waterfall (Phase 7)** — allocate the move across beta + idiosyncratic drivers,
   confidence per factor, summing to the realized move. → `reference/methodology.md#phase-7`
8. **Assemble deliverable** — 13-section self-contained HTML note.
   → `templates/report-structure.md`, `templates/evidence-ledger.md`

## Sourcing & confidence
Source hierarchy, confidence taxonomy, and anti-hallucination rules:
→ `reference/sourcing-and-confidence.md`

## Anti-fabrication protocol (tools offline)
If market-data or web tools are unavailable:
1. Proceed only on figures already in context and previously verified.
2. Tag every gap `Unverifiable` or `Assumed` (with stated bounds).
3. Add each gap to the **Data-Gap Ledger** with the exact source/pull needed to close it.
4. Never invent an index return, implied move, valuation multiple, or filing figure.

## Definition of done (self-check before delivering)
- [ ] Beat/miss deltas computed, not just absolutes.
- [ ] Idiosyncratic move isolated from index/peer beta.
- [ ] Root causes ranked and classified structural vs cyclical.
- [ ] Waterfall quantified, sums to the realized move, confidence per factor.
- [ ] Every figure carries citation + confidence tag.
- [ ] Segment table separates miss from deceleration.
- [ ] Regulatory/macro confounds checked.
- [ ] Deliverable is self-contained HTML, semantic, WCAG-AA, print-friendly.
- [ ] All `Assumed`/`Unverifiable` items listed in the Data-Gap Ledger.
- [ ] No fabricated numbers; no investment advice.

## Supporting files
- `reference/methodology.md` — the 7-phase process in full.
- `reference/formulas.md` — abnormal return, implied move, deltas, waterfall, PT math.
- `reference/segment-maps.md` — reportable segments per big-tech company.
- `reference/sourcing-and-confidence.md` — source hierarchy + confidence taxonomy.
- `templates/report-structure.md` — 13-section HTML deliverable spec.
- `templates/evidence-ledger.md` — verification ledger format.
- `scripts/quant_helpers.py` — deterministic delta/alpha/waterfall math.
```

---

## `reference/methodology.md`

```markdown
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
   FactSet/Visible Alpha-referencing notes or aggregators (Zacks, Bloomberg consensus).

**Compute the beat/miss delta** for every headline metric — `actual − consensus` and the
percentage. The delta, not the absolute, is what moves price.
Formula: `reference/formulas.md#beatmiss-delta`.

**Tag:** `Verified` when a figure is consistent across ≥2 independent primary/near-primary
sources to the reported precision.

## Phase 2 — Isolate idiosyncratic vs market-wide move
**Goal:** separate the company-specific move (alpha) from sector beta.

1. **Abnormal return** = stock return − same-day benchmark return. Use QQQ or XLK as the broad
   benchmark and the direct comps as a cross-check. If the Nasdaq fell 2% that day, the
   "company-specific" story is ~2pp smaller than headlines suggest.
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
**Goal:** a quantified waterfall, not a narrative.

Allocate the realized move across:
- **(a) market-wide beta** — from Phase 2.
- **(b) growth-segment deceleration** — e.g. cloud.
- **(c) capex/margin/FCF guidance.**
- **(d) one-time items** — legal charge, FX, portfolio mark-to-market, dilution.
- **(e) sentiment/positioning** — de-grossing, high implied move already priced.

Rules:
- Weights sum to the realized move.
- Each factor gets a confidence tag and a stated basis.
- Classify each driver **structural** (permanent to the franchise) vs **cyclical/accounting**
  (timing, non-cash, reversible). This classification is the single most important judgment and
  is always `Reasoned`, never presented as a reported fact.
- State explicitly when a weight is an analytical allocation rather than an observed regression.

## Trend-mode variant
For multi-quarter trend analysis (no single event), run Phases 1,3,4,5 and a trajectory version
of Phase 7: chart revenue/FCF/margin/multiple across 4–8 quarters, identify the inflection point,
and attribute the trend to (i) fundamental trajectory, (ii) multiple re-rating, (iii) sentiment/
flows. Add a **valuation-band** section (forward P/E and EV/FCF vs 3–5yr band).
```

---

## `reference/formulas.md`

```markdown
# Quant Formulas

Worked examples use Alphabet Q3 2026 for concreteness.

## Beat/miss delta
```
delta_abs = actual − consensus
delta_pct = delta_abs / consensus
```
Example (revenue): 127.58 − 128.22 = −0.64B; −0.64/128.22 = **−0.50%**.
Example (EPS): 2.12 − 3.02 = −0.90; −0.90/3.02 = **−29.8%**.

## Abnormal return (alpha)
```
alpha = stock_return − benchmark_return     (same window)
```
If benchmark closes are unavailable, bound the beta (e.g. −1.0% to −2.0% during a sector
de-rating) and report alpha as a range, tagged `Assumed`.
Example: GOOGL −12.6%, beta −1.5% → idiosyncratic **−11.1%**.

## Options implied move vs realized
```
implied_move ≈ ATM_straddle_price / spot     (as %)
surprise_ratio = |realized_move| / implied_move
```
surprise_ratio ≫ 1 → genuine surprise; ≈ 1 → positioning overshoot.

## Capex / operating-cash-flow ratio
```
capex_ocf_ratio = capex / operating_cash_flow
```
Example: 51.36 / 42.29 = **121.4%** (>100% means capex exceeds cash generation).

## FCF trajectory
List FCF for the last 4 quarters. Flag consecutive negative quarters.
Example: +24.55 → +10.12 → −5.86 → −9.07.

## OCF shortfall (derived)
When capex beats Street but FCF misses, the gap is in operating cash flow:
```
implied_consensus_OCF = consensus_FCF + consensus_capex
ocf_shortfall = implied_consensus_OCF − actual_OCF
```
Example: (−2.70 + 55.09) − 42.29 = **−10.10B** OCF shortfall.

## Average price-target cut
```
cut_i = (new_PT_i − old_PT_i) / old_PT_i
avg_cut = mean(cut_i)
```
Example (5 desks): ≈ **−13.7%**, closely tracking the −12.6% move.

## Waterfall
```
Σ (factor_weights) = realized_move
idiosyncratic_sum = realized_move − beta
```
Weights are `Reasoned` allocations; disclose the method and tag each factor.
Example: beta −1.5, FCF/capex −4.0, EPS quality −2.8, Search −2.5, positioning −1.8 = **−12.6**.

## Forward multiple (trend mode)
```
forward_PE = price / forward_consensus_EPS
```
Chart vs the 3–5yr band to show de-rating/re-rating.

## Market cap
```
market_cap_erased = pre_print_market_cap × |move|
pre_print_market_cap ≈ market_cap_erased / |move|
```
```
Run the math with `scripts/quant_helpers.py` to avoid arithmetic errors.
```

---

## `reference/segment-maps.md`

```markdown
# Reportable Segments — US Big Tech

Use the EDGAR 10-Q segment table as the source of truth. This map tells you what each company
reports and which lines typically move the stock.

| Company | Reportable segments | Primary price movers |
|---|---|---|
| **Alphabet (GOOGL)** | Google Services: Search & other · YouTube ads · Google Network · Subscriptions/Platforms/Devices; Google Cloud; Other Bets | Search growth; Cloud growth + margin; capex/FCF |
| **Microsoft (MSFT)** | Productivity & Business Processes (Office/LinkedIn/Dynamics); Intelligent Cloud (Azure/server); More Personal Computing (Windows/gaming/search ads) | Azure growth; capex; AI run-rate |
| **Amazon (AMZN)** | North America; International; AWS; Advertising | AWS growth + margin; ad growth; capex; retail margin |
| **Apple (AAPL)** | iPhone; Mac; iPad; Wearables/Home/Accessories; Services | iPhone units/ASP; Services growth + margin; China |
| **Meta (META)** | Family of Apps (advertising + other); Reality Labs | Ad revenue; DAP; Reality Labs losses; capex |
| **Nvidia (NVDA)** | Data Center; Gaming; Professional Visualization; Automotive; OEM | Data Center growth; guidance; gross margin; export limits |
| **Tesla (TSLA)** | Automotive; Energy Generation & Storage; Services & Other | Deliveries; auto margin; energy growth |

## Usage notes
- Identify the **cash-cow** segment (funds investment) and the **growth** segment (the story).
- For trend mode, pull 4–8 quarters of each segment to spot inflections.
- "Subscriptions/Devices" and "Other Bets"-style residual lines often require the 10-Q to split;
  if only the aggregate is available, report the residual and tag it `Unverifiable`.
```

---

## `reference/sourcing-and-confidence.md`

```markdown
# Sourcing Standards & Confidence Taxonomy

## Source hierarchy (best → acceptable)
1. SEC EDGAR filings (8-K, 10-Q, press release) — segment splits, balance sheet.
2. Official IR transcript / earnings-call audio.
3. Exchange-sourced or vendor price feeds (programmatic).
4. Named consensus source (FactSet, Visible Alpha, Bloomberg, Zacks).
5. Wire services (Reuters, Bloomberg) and major outlets (CNBC) — for sell-side reactions,
   management quotes, and cross-checks.
6. Aggregators (TipRanks, Investing.com, Motley Fool) — acceptable for analyst PT changes and
   transcript cross-checks; verify the underlying number elsewhere.

**Never** present a figure reconstructed from memory. If the only source is a model's prior
knowledge, tag it `Assumed` and flag it.

## Confidence taxonomy (tag every figure)
- **Verified** — observed in ≥2 independent primary/near-primary sources, consistent to the
  reported precision.
- **Reasoned** — logical inference/derivation from verified inputs (e.g. waterfall weights,
  implied consensus OCF, structural-vs-cyclical classification). Method disclosed.
- **Assumed** — based on a stated assumption with explicit bounds (e.g. beta estimate when index
  closes are unavailable).
- **Unverifiable** — the environment cannot retrieve the source; listed in the Data-Gap Ledger
  with the exact pull needed.

## Anti-hallucination rules
- No invented API figures, index returns, implied moves, multiples, or filing numbers.
- No "executed verification" claims for price targets or forward guidance — those are reported
  third-party actions, not observable outcomes.
- Forward-looking statements are scenarios, never predictions.
- When tools are offline, shrink scope to verified-in-context data and expand the Data-Gap
  Ledger; never backfill with invented numbers.

## Disclaimer
Analysis only. Not investment advice. All investments involve risk.
```

---

## `templates/report-structure.md`

```markdown
# Deliverable: 13-Section Self-Contained HTML Research Note

Single file. Semantic HTML. CSS-variable palette (no hardcoded colors outside `:root`).
Responsive. WCAG-AA contrast. Print-friendly. Confidence tag inline on every figure.

1. **Cover** — ticker, event/trend date, headline move, one-line thesis, confidence legend.
2. **Executive Summary** — 4–6 bullet root-cause thesis, ranked by contribution; key stat band.
3. **Price Reaction Timeline** — annotated chart (pre-market → intraday → next sessions) with an
   abnormal-return overlay vs QQQ/XLK. *(Trend mode: multi-quarter price chart instead.)*
4. **Pre-Print Setup** — consensus, implied move, positioning context. *(Trend mode: valuation
   band.)*
5. **Segment Variance Table** — actual vs consensus, Δ, QoQ/YoY, color-coded beat/miss/decel.
6. **Capex & Margin Deep-Dive** — guidance vs prior vs Street; depreciation commentary; FCF
   trajectory; OCF-shortfall insight if applicable.
7. **Management Commentary** — verbatim, sourced quotes (CEO/CFO/CBO) tied to each root cause.
8. **Sell-Side Reaction Table** — firm, analyst, old/new rating, old/new PT, date, rationale.
9. **Macro/Regulatory Overlay** — concurrent confounds (antitrust, rates, peer read-through).
10. **Root-Cause Waterfall** — quantified decomposition summing to the realized move, confidence
    per factor, beta separated from idiosyncratic.
11. **Valuation Impact** — forward multiple before/after vs historical band.
12. **Bull/Bear Forward View** — what would confirm vs invalidate the market's reaction.
13. **Sources & Methodology Appendix** — full citation list with access dates, methodology
    compliance scorecard, and the **Data-Gap Ledger** (`templates/evidence-ledger.md`).

## Rendering rules
- Headline stats in a responsive stat band.
- Use `callout` boxes for read-throughs, data boundaries, and insights.
- Waterfall as a labeled horizontal stacked bar + per-factor table.
- Every `Assumed`/`Unverifiable` item links to the Data-Gap Ledger.
```

---

## `templates/evidence-ledger.md`

```markdown
# Evidence & Verification Ledger (Section 13)

Two tables in the deliverable appendix.

## Table 1 — Evidence ledger
| Claim | Source(s) | Confidence | Verification method |
|---|---|---|---|
| e.g. Revenue $127.58B | Earnings release; transcript; CNBC | Verified | Cross-checked ≥3 outlets, consistent to decimal |
| e.g. Beta −1.5% | Index closes unavailable | Assumed | Bounded −1.0 to −2.0; see Data-Gap Ledger |

## Table 2 — Data-Gap Ledger (everything Assumed/Unverifiable)
| Gap | Phase | Exact source / action to close |
|---|---|---|
| QQQ/XLK + comp closes | 2 (alpha) | Pull daily OHLC from exchange/vendor feed for event window |
| Pre-print ATM straddle | 2 (positioning) | Options chain for nearest expiry; implied vs realized |
| EDGAR segment split | 1 & 3 | EDGAR CIK → 8-K/10-Q → segment tables |
| Forward P/E vs band | 11 | Valuation feed + forward consensus EPS |

## Method note (always include)
State the source hierarchy used, that no "executed verification" is claimed for price targets or
forward guidance, and that root-cause weights are `Reasoned` judgment, not reported fact.
```

---

## `scripts/quant_helpers.py`

```python
#!/usr/bin/env python3
"""Deterministic quant math for big-tech equity research. Avoids hand-arithmetic errors.

Usage:  python3 quant_helpers.py            # runs a self-test on the worked example
        import quant_helpers as qh          # or import individual functions
"""
from statistics import mean


def beat_miss_delta(actual, consensus):
    """Return (abs_delta, pct_delta)."""
    d = actual - consensus
    return d, (d / consensus * 100.0) if consensus else float("nan")


def abnormal_return(stock_ret, bench_ret):
    """Alpha = stock return minus benchmark return (same window), in pct points."""
    return stock_ret - bench_ret


def capex_ocf_ratio(capex, ocf):
    return capex / ocf * 100.0 if ocf else float("nan")


def ocf_shortfall(consensus_fcf, consensus_capex, actual_ocf):
    """When capex beats Street but FCF misses, the gap is operating cash flow."""
    implied_ocf = consensus_fcf + consensus_capex
    return implied_ocf - actual_ocf


def avg_pt_cut(pt_pairs):
    """pt_pairs = [(new_pt, old_pt), ...]. Returns mean % cut."""
    cuts = [(new - old) / old * 100.0 for new, old in pt_pairs]
    return mean(cuts)


def waterfall_check(weights, realized_move):
    """Validate that factor weights sum to the realized move."""
    total = sum(weights.values())
    return {"sum": round(total, 2), "matches": abs(total - abs(realized_move)) < 0.05}


if __name__ == "__main__":
    # Worked example: Alphabet Q3 2026
    rev_d, rev_p = beat_miss_delta(127.58, 128.22)
    eps_d, eps_p = beat_miss_delta(2.12, 3.02)
    print(f"Revenue delta: {rev_d:+.2f}B ({rev_p:+.2f}%)")      # −0.64B (−0.50%)
    print(f"EPS delta:     {eps_d:+.2f} ({eps_p:+.2f}%)")        # −0.90 (−29.80%)
    print(f"Alpha vs −1.5% beta: {abnormal_return(-12.6, -1.5):+.1f}pp")  # −11.1
    print(f"Capex/OCF: {capex_ocf_ratio(51.36, 42.29):.1f}%")    # 121.4%
    print(f"OCF shortfall: {ocf_shortfall(-2.70, 55.09, 42.29):+.2f}B")  # +10.10B
    pts = [(375, 425), (385, 435), (300, 350), (380, 430), (355, 440)]
    print(f"Avg PT cut: {avg_pt_cut(pts):+.1f}%")                # −13.7%
    wf = {"beta": 1.5, "fcf": 4.0, "eps": 2.8, "search": 2.5, "positioning": 1.8}
    print(f"Waterfall: {waterfall_check(wf, -12.6)}")            # sum 12.6, matches True
```

---

## How an agent uses this skill

1. **Trigger** — the `description` matches any request to explain a big-tech move or trend.
2. **Route** — Step 0 picks Event / Trend / Pre-event mode.
3. **Execute** — run Phases 1–7 from `reference/methodology.md`, using `segment-maps.md` for
   the company's accounting, `formulas.md` + `quant_helpers.py` for the math, and
   `sourcing-and-confidence.md` for tagging.
4. **Render** — assemble via `templates/report-structure.md` and `evidence-ledger.md`.
5. **Gate** — the Definition-of-Done checklist in `SKILL.md` must pass before delivery.

The two hard-won lessons from our session are baked in: **never fabricate when tools are offline**
(tag and ledger the gap instead), and **the quantified waterfall with confidence tags is the actual
fund-manager deliverable**, not a narrative.
