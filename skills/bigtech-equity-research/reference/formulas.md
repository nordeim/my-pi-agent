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
window (e.g. 250 sessions vs QQQ); disclose the window and the beta. Either way,
never call the benchmark return "beta" — beta is a unitless sensitivity, not a
percentage move.

If benchmark closes are unavailable, bound the benchmark return (e.g. −1.0% to
−2.0% during a sector de-rating) and report the excess return as a range, tagged
`Assumed`.
Example (market-adjusted, beta=1 convention): GOOG −12.29%, benchmark −1.5% →
idiosyncratic **−10.79pp**.

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
**What this is and is not.** The weights are `Reasoned` analytical allocations —
a judgmental attribution that happens to sum to the move — **not** an observed
regression, not evidence of causation, and not a measurement. The sum-to-move
identity is an **arithmetic consistency check**, nothing more. Disclose the method,
tag each factor, and present the ordinal ranking as the primary output. A
quantified decomposition may be published **only** as (a) an accounting identity
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
market_cap_erased = shares_outstanding × |Δprice|
cross-check:  market_cap_erased ≈ pre_print_market_cap × |move %|   (approximation)
```
Compute the erased value from **shares outstanding × price change** (shares from the
latest 10-Q/10-K cover page) — it is independent of any market-cap quote. The
percentage form needs the pre-print market cap and is labeled an approximation; the
two methods agreeing is itself a cross-check, not a derivation of one from the other.
Example: ≈12.1B GOOG shares × $39.57 ≈ **−$479B**, consistent with the ≈$482B the
press reported.
```
Run the math with `scripts/quant_helpers.py` to avoid arithmetic errors.
```
