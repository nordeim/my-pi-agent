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
