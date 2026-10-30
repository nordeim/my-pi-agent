# Deliverable: 14-Section Self-Contained HTML Research Note

Single file. Semantic HTML. CSS-variable palette (no hardcoded colors outside `:root`).
Responsive. WCAG-AA contrast. Print-friendly. Confidence tag inline on every figure.

1. **Cover** — ticker, event/trend date, headline move, one-line thesis, confidence
   legend, and a **verification-status line** stating which delivery gates the
   finished note passed: "Verification status: lite audit gates passed — disclosure
   needles + render audit", or "Draft — human verification required" with the reason
   when a gate could not run. Keep the wording free of the audit scan tokens
   (`todo`, `tbd`, `xxx`, `nan`, `undefined`, `placeholder`, `lorem`,
   `insert data/numbers`, `foo bar`, `【`) so the gate does not flag the line itself.
2. **Executive Summary** — 4–6 bullet root-cause thesis, ranked by contribution; key stat band.
3. **Price Reaction Timeline** — annotated chart (pre-market → intraday → next sessions) with an
   abnormal-return overlay vs QQQ/XLK. *(Trend mode: multi-quarter price chart instead.)*
4. **Pre-Print Setup** — consensus, implied move, positioning context. *(Trend mode: valuation
   band.)*
5. **Segment Variance Table** — actual vs consensus, Δ, QoQ/YoY, color-coded beat/miss/decel;
   cites the filing (form type + fiscal period) it ties to, checked against
   `reference/segment-maps.md`'s `last_verified_against_filing`.
6. **Capex & Margin Deep-Dive** — guidance vs prior vs Street; depreciation commentary; FCF
   trajectory; OCF-shortfall insight if applicable.
7. **Management Commentary** — verbatim, sourced quotes (CEO/CFO/CBO) tied to each root cause.
8. **Sell-Side Reaction Table** — firm, analyst, old/new rating, old/new PT, date, rationale.
9. **Macro/Regulatory Overlay** — concurrent confounds (antitrust, rates, peer read-through).
10. **Root-Cause Driver Decomposition** — ranked drivers with optional analytical
    allocation: any quantified waterfall is labeled "Reasoned allocation — not a
    measured decomposition", uses signed weights, and sums to the realized move as
    an arithmetic consistency check only; beta/benchmark component separated from
    idiosyncratic; confidence tag per factor. (The lite audit's disclosure needle
    fails the build if a quantified waterfall ships without the label.)
11. **Valuation Impact & Boundary** — forward multiple before/after vs historical band,
    then the explicit boundary statement: the band is context, not an intrinsic
    valuation; no DCF/SOTP/scenario-weighted fair value is produced; the valuation
    model gap is named as an open item (forward estimates, discount-rate framework,
    scenario weights).
12. **Bull/Bear Forward View** — what would confirm vs invalidate the market's reaction,
    as scenario frames (never predictions).
13. **Risk Factors & Falsification Conditions** — the note's own falsifiers (what
    evidence would flip each root-cause verdict), the key risk factors to the thesis
    with observable, dated triggers, and the explicitly excluded hypotheses with
    their falsifying facts (the family's elimination discipline — an EXCLUDED
    driver with its falsifying fact belongs here, not buried in §10's prose).
14. **Sources & Methodology Appendix** — full citation list with access dates, methodology
    compliance scorecard, and the **Data-Gap Ledger** (`templates/evidence-ledger.md`).

## Rendering rules
- Headline stats in a responsive stat band.
- Use `callout` boxes for read-throughs, data boundaries, and insights.
- Driver decomposition as a labeled horizontal stacked bar + per-factor table, with
  the "Reasoned allocation — not a measured decomposition" label prominent on the
  chart itself, plus the ordinal ranking table above it.
- Every `Assumed`/`Unverifiable` item links to the Data-Gap Ledger.
- No horizontal scrolling, no element spilling past the viewport width, no
  overflow:hidden box clipping its content: run
  `node scripts/note_overflow_audit.mjs --note <note.html>` before delivery and fix
  the layout (not the audit) until it exits 0. Decorative bleed elements are marked
  `data-bleed="intentional"`, `data-decor`, or `aria-hidden="true"` so the render
  gate skips them.
- Final gate before delivery: `python3 scripts/note_audit.py --note <note.html>
  --checks assets/checks.json` (placeholder + disclosure needles) must exit 0; the
  cover's verification-status line must state the actual results of both gates.
