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
