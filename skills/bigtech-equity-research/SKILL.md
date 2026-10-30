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
