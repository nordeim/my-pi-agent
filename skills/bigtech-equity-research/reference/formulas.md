# Quant Formulas

Worked examples use Alphabet Q3 2026 (GOOG class: close $282.32 on 2026-10-29,
−12.29% from the $321.89 prior close) for concreteness — the same canonical
print the sibling skill `analyzing-us-bigtech-stocks` teaches from. One event,
one set of verified headline numbers across the family.

## Beat/miss delta
```
delta_abs = actual − consensus
delta_pct = delta_abs / consensus
```
Example (revenue): 127.58 − 128.22 = −0.64B; −0.64/128.22 = **−0.50%**.
Example (EPS): 2.12 − 3.02 = −0.90; −0.90/3.02 = **−29.8%**.

## Market-adjusted excess return (not "alpha")
```
excess_return = stock_return − benchmark_return        (same window)
beta_adjusted_excess = stock_return − beta × benchmark_return   (if beta is estimated)
```
This is a **market-adjusted** excess return, not a market-model abnormal return:
subtracting the raw benchmark return implicitly assumes beta = 1. For a high-beta
name, prefer the beta-adjusted form with a beta estimated over a stated pre-event
window; disclose the window and the beta. Either way, never call the benchmark
return "beta" — beta is a unitless sensitivity, not a percentage move.

**Canonical default beta window** (round 3, reports 6/7 H-2): when a beta-adjusted
return is computed, estimate beta over **2-year monthly returns vs QQQ (24
observations, through the last full month-end before the event)** unless a
corporate event structurally changed the company's risk profile (a segment mix
shift, a leverage change) — and then justify the alternative window in the note.
A beta without a standardized window makes abnormal returns non-comparable
across runs.

**Code contract** (`scripts/quant_helpers.py::abnormal_return`): the helper
returns `{excess, convention, beta, beta_window, beta_window_source}`. When a
beta is supplied without a window it **applies the canonical default**
(`DEFAULT_BETA_WINDOW`) and echoes it with `beta_window_source: "canonical
default"`; an explicitly passed window is echoed as `"explicit"`; a blank or
non-string window raises. Print the echoed `beta_window` next to the figure in
the note either way — the disclosure is the point.

**Beta regime diagnostics (round 4, reports 8/9 M-7)**: the canonical window is
only trustworthy while the stock/benchmark correlation holds and realized vol is
in its historical regime. Run `quant_helpers.beta_diagnostics(stock_rets,
bench_rets)` → `{beta, r_squared, correlation, r_squared_floor,
correlation_breakdown}` and `quant_helpers.volatility_regime_flag(monthly_rets)` →
`{recent_vol, baseline_vol, z_score, regime_shift}` on the estimation window
before trusting the beta. **If R² < 0.30 (`R_SQUARED_FLOOR`) or |z| > 2
(`VOL_REGIME_Z_THRESHOLD`), the 2-year monthly beta is fitting a broken regime**
(2022 rate shock, 2023 AI re-rating): either explicitly justify the window or
re-estimate over a shorter (e.g. 6-month daily) window and disclose it.
"Structurally changed" is a quantitative trigger now, not a judgment call the
LLM makes unaided — applying an obsolete beta misattributes market-driven moves
to company-specific failures.

If benchmark closes are unavailable, bound the benchmark return (e.g. −1.0% to
−2.0% during a sector de-rating) and report the excess return as a range, tagged
`Assumed`.
Example (market-adjusted, beta=1 convention): GOOG −12.29%, benchmark −1.5% →
idiosyncratic **−10.79pp**.

## Options implied move vs realized
```
implied_move = (ATM_call_close + ATM_put_close) / spot_at_T-1   (as %)
surprise_ratio = |realized_move| / implied_move
```
surprise_ratio ≫ 1 → genuine surprise; ≈ 1 → positioning overshoot.

**Sourcing (round 3, reports 6/7 M-3):** compute the straddle cost from the
**T-1 closing options chain** — the ATM call and ATM put closing premiums for
the nearest post-event expiry, divided by the T-1 close. Never quote a news
article's rounded implied-move percentage as the figure itself: wire copy often
prints the prior session's level, a mid quote, or a generic IV percentage. A
news-sourced figure may appear only as a cross-check, tagged `Assumed` with the
outlet named.

**Statistical caveat (volatility risk premium):** the ATM straddle embeds a
volatility risk premium — implied moves exceed realized moves on average — so
"realized ≈ implied" can reflect a normal premium rather than genuine
positioning. When the note interprets the ratio, either state the name's
historical average `realized/implied` ratio over a disclosed window (≥8 prior
prints) or tag the read `Assumed` (heuristic). The lite audit's scoped needle
fails a note that discusses the implied move without the volatility-risk-premium
caveat near it.

## Capex / operating-cash-flow ratio
```
capex_ocf_ratio = capex / operating_cash_flow
```
Example: 51.36 / 42.29 = **121.4%** (>100% means capex exceeds cash generation).

## FCF trajectory
List FCF for the last 4 quarters. Flag consecutive negative quarters.
Example: +24.55 → +10.12 → −5.86 → −9.07.

**FCF ex-SBC companion (round 3, reports 6/7):** for US mega-cap tech the
scorecard pairs every FCF figure with **FCF ex-SBC = OCF − capex − SBC**
(SBC from the quarter's cash-flow statement, T1). SBC is structurally material
for every name in coverage; FCF that ignores it overstates the cash generation
available for buybacks and dividends. State which basis (reported FCF or ex-SBC)
the beat/miss is computed on. `scripts/quant_helpers.py::fcf` and `fcf_ex_sbc`
compute both.

## OCF shortfall (derived)
When capex beats Street but FCF misses, the gap is in operating cash flow:
```
implied_consensus_OCF = consensus_FCF + consensus_capex
ocf_shortfall = implied_consensus_OCF − actual_OCF
```
Sign convention: **positive shortfall = actual OCF below what consensus FCF + capex
implied** (the cash-generation miss).
Example: (−2.70 + 55.09) − 42.29 = 52.39 − 42.29 = **+10.10B** OCF shortfall —
actual OCF ran $10.10B below the consensus-implied level.

## Average price-target cut
```
cut_i = (new_PT_i − old_PT_i) / old_PT_i
avg_cut = mean(cut_i)
```
Example (5 desks): ≈ **−13.7%**, closely tracking the −12.29% move.

## Root-cause driver decomposition (the "waterfall")
```
Σ (driver_weights) ≈ realized_move        (signed, within tolerance)
idiosyncratic_sum = realized_move − benchmark_component
```
**What this is and is not.** The weights are `Reasoned (judged)` analytical
allocations — a judgmental attribution that happens to sum to the move — **not**
an observed regression, not evidence of causation, and not a measurement.
Deterministic derivations (GAAP bridges, options math, delta arithmetic) are the
other half of the `Reasoned` family: `Reasoned (derived)` facts carry a formula
and are reproducible — judgment allocations are not. The sum-to-move identity
is an **arithmetic consistency check**, nothing more — enforced mechanically by
`quant_helpers.waterfall_check` and, in the flagship, by `fact_base_audit.py`'s
WATERFALL gate on facts that carry `weights` + `realized_move`. Disclose the
method, tag each factor, and present the ordinal ranking as the primary output.
A quantified decomposition may be published **only** as (a) an accounting identity
(GAAP bridge, options math) or (b) a disclosed-model event-study residual — never
as invented precision (see the family rule: rank, don't fabricate percentages).
Example (signed weights, GOOG basis): benchmark −1.5, FCF/capex −3.9, EPS quality
−2.7, Search −2.4, positioning −1.8 → sum **−12.3** vs realized −12.29 — consistent
within the ±0.05 tolerance. Positive weights mean tailwind, negative mean headwind;
a decomposition whose signs disagree with the realized move's sign is wrong, full stop.

## Forward multiple (trend mode)
```
forward_PE = price / forward_consensus_EPS
```
Chart vs the 3–5yr band to show de-rating/re-rating.

## Market cap
```
market_cap_delta_class = shares_class × (price_after − price_before)
market_cap_delta_total = Σ over share classes                       (round 4: multi-class method)
cross-check:  market_cap_delta_total ≈ pre_print_market_cap × move %   (approximation)
```
Compute the market-cap change **per share class and sum** (round 4, reports 8/9
H-4: `quant_helpers.market_cap_delta` takes the per-class {label, shares,
price_before, price_after} list) — shares from the latest 10-Q/10-K cover page
(T1). One class's shares must **never** be multiplied by another class's price
(GOOG/GOOGL, META A/B are the classics); when classes diverge, the single-class
shortcut materially misstates the cap change. Disclose the method on the note.
The percentage form needs the pre-print market cap and is labeled an
approximation; the two methods agreeing is itself a cross-check, not a
derivation of one from the other.
Example: ≈12.1B GOOG shares × −$39.57 ≈ **−$479B**, consistent with the ≈$482B the
press reported.
```
Run the math with `scripts/quant_helpers.py` to avoid arithmetic errors.
```
