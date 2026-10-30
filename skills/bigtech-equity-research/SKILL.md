---
name: bigtech-equity-research
version: 1.2.0
description: "Produce institutional-grade, evidence-based equity research notes on US big-tech stocks (GOOGL, MSFT, AMZN, AAPL, META, NVDA, TSLA, and peers). Use when asked to explain a stock-price event (post-earnings move, guidance shock, regulatory action), analyze a multi-quarter price trend, attribute a drawdown to its drivers, or build a ranked driver decomposition of a price move. The quantified single-note member of the big-tech research family — segment deep-dive, options math, evidence ledger, and bundled lite delivery audits (placeholder, disclosure, render gates). For a full audited multi-page IC deck use analyzing-us-bigtech-stocks; for a lighter post-earnings note use big-tech-earnings-postmortem. Outputs a self-contained HTML research note with sourced figures, confidence tags, and a ranked root-cause decomposition. Analytical output only — not investment advice."
license: Apache-2.0
compatibility: Requires web search and page-fetch tools for primary-source verification; numeric helpers need Python 3; render gate needs Node.js with Playwright.
---

# Big-Tech Equity Research

## Skill folder structure

```
bigtech-equity-research/
├── SKILL.md                          # Entry point: triggers, hard rules, workflow
├── reference/
│   ├── methodology.md                # The 7-phase research process in full
│   ├── formulas.md                   # Quant math: excess return, deltas, decomposition
│   ├── segment-maps.md               # Reportable segments per big-tech company (versioned)
│   └── sourcing-and-confidence.md    # Source hierarchy + confidence taxonomy
├── templates/
│   ├── report-structure.md           # 14-section HTML deliverable spec
│   └── evidence-ledger.md             # Verification ledger format
├── assets/
│   └── checks.json                   # Disclosure needles the lite audit enforces
└── scripts/
    ├── quant_helpers.py              # Deterministic delta/excess-return/decomposition math
    ├── note_audit.py                 # Placeholder + disclosure-needle gate
    └── note_overflow_audit.mjs        # Render/overflow gate (Node + Playwright)
```

Turn "why did GOOGL drop after earnings?" or "what's driving the MSFT trend?" into a
fund-manager-quality, fact-based research note.

## Hard rules (read first)
1. **Never fabricate.** Every number is sourced or tagged `Unverifiable`. If a data tool is
   offline, tag the gap and state the exact pull needed — do not invent a figure.
2. **Beat/miss delta moves price, not the absolute number.** Always compute actual − consensus.
3. **Isolate the idiosyncratic move.** Subtract the same-day index/peer return (or a
   beta-scaled benchmark return, with the estimation window disclosed —
   `quant_helpers.abnormal_return` enforces the window by refusing to run without it)
   before calling a move "company-specific."
4. **Rank root causes** and classify each as *structural* vs *cyclical/accounting*. No flat lists.
5. **Tag every figure** with a confidence label: `Verified` / `Reasoned` / `Assumed` / `Unverifiable`.
6. **Label judgment as judgment.** Driver-decomposition weights and structural-vs-cyclical
   calls are `Reasoned` analysis, not reported facts — and never presented as measured
   decompositions or regression output.
7. **No investment advice.** Forward-looking views are scenarios, not predictions.
8. **Compute, don't recall.** Never do arithmetic in-context. Every delta, ratio, implied
   move, and multiple is executed with `scripts/quant_helpers.py` (or code) and the
   code's output is what goes in the note — in-context arithmetic is where transcription
   and magnitude errors enter.
9. **Respect the segment map's vintage.** Check `segment-maps.md`'s
   `last_verified_against_filing` against the filing you are actually using: if the
   filing is newer, re-verify the segment structure against its segment note before
   building the variance table — a stale map silently breaks the tie-out.
10. **State the valuation boundary.** The note explains and quantifies the repricing; it
    does not opine on mispricing. No DCF/SOTP/fair value is produced — say so and log
    the model gap as an open item (see `templates/report-structure.md` §11).

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
2. **Isolate the idiosyncratic move (Phase 2)** — market-adjusted (or beta-adjusted)
   excess return vs QQQ/XLK + direct comps; options implied move (ATM straddle)
   vs realized. → `reference/formulas.md`
3. **Segment attribution (Phase 3)** — variance table: actual vs consensus, QoQ + YoY, per
   segment. Distinguish **miss** from **deceleration**. → `reference/segment-maps.md`
4. **Cost/capex/margin (Phase 4)** — capex vs guidance vs Street; margin trend; depreciation-
   schedule commentary (a stealth margin driver).
5. **Macro/regulatory overlay (Phase 5)** — same-week macro, antitrust confounds, peer read-through.
6. **Sell-side reaction (Phase 6)** — PT/rating changes ≤48h, sourced from wire-service pickup.
7. **Root-cause driver decomposition (Phase 7)** — rank the move's drivers; if a
   quantified allocation accompanies the ranking, it is a `Reasoned` signed allocation
   that sums to the realized move as an arithmetic consistency check — never a
   measured decomposition. → `reference/methodology.md#phase-7`
8. **Assemble deliverable** — 14-section self-contained HTML note.
   → `templates/report-structure.md`, `templates/evidence-ledger.md`
9. **Run the delivery gates** (mandatory, bundled — no sibling skill required):
   `python3 scripts/note_audit.py --note <note.html> --checks assets/checks.json`
   (placeholder + disclosure needles: disclaimer, verification-status line, the
   Reasoned-allocation label when a quantified waterfall is present, beta
   estimation-window disclosure, Data-Gap Ledger presence) and
   `node scripts/note_overflow_audit.mjs --note <note.html>` (single-file render/
   overflow audit). The note's verification-status line must state the actual gate
   results; if the render gate cannot run, mark the note "Draft — human verification
   required" with the reason instead of shipping silently.

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
- [ ] Beat/miss deltas computed, not just absolutes — via `quant_helpers.py`, never in-context.
- [ ] Idiosyncratic move isolated from index/peer benchmark (convention stated; if beta-adjusted, the estimation window is disclosed and echoed by the helper).
- [ ] Root causes ranked and classified structural vs cyclical.
- [ ] Driver allocation (if quantified) uses signed weights, is labeled `Reasoned`
      allocation — not a measured decomposition — and its sum matches the realized
      move within tolerance.
- [ ] Every figure carries citation + confidence tag.
- [ ] Segment table separates miss from deceleration and mirrors the filing's ASC 280
      segment note (reportable segments ≠ disclosed revenue lines); the segment map's
      `last_verified_against_filing` is not older than the filing used.
- [ ] Regulatory/macro confounds checked.
- [ ] Deliverable is self-contained HTML, semantic, WCAG-AA, print-friendly.
- [ ] Valuation boundary stated (§11): forward-multiple band is context, not an
      intrinsic valuation; the model gap is named as an open item.
- [ ] All `Assumed`/`Unverifiable` items listed in the Data-Gap Ledger.
- [ ] `python3 scripts/quant_helpers.py` self-test exits 0 after any helper change.
- [ ] `python3 scripts/note_audit.py --note <note.html> --checks assets/checks.json`
      exits 0 (placeholder + disclosure gates).
- [ ] `node scripts/note_overflow_audit.mjs --note <note.html>` exits 0 (render gate),
      or the verification-status line says "Draft — human verification required" with
      the reason.
- [ ] Verification-status line present and matches the actual gate results.
- [ ] No fabricated numbers; no investment advice; disclaimer and internal-use framing
      present on the deliverable.

## Supporting files
- `reference/methodology.md` — the 7-phase process in full.
- `reference/formulas.md` — market-adjusted excess return, implied move, deltas, driver decomposition, PT math.
- `reference/segment-maps.md` — reportable segments (ASC 280) per big-tech company, with `segment_map_version` / `last_verified_against_filing` staleness control.
- `reference/sourcing-and-confidence.md` — source hierarchy + confidence taxonomy.
- `templates/report-structure.md` — 14-section HTML deliverable spec.
- `templates/evidence-ledger.md` — verification ledger format.
- `assets/checks.json` — disclosure needles enforced by the lite audit.
- `scripts/quant_helpers.py` — deterministic delta/excess-return/decomposition math.
- `scripts/note_audit.py` — placeholder + disclosure-needle delivery gate.
- `scripts/note_overflow_audit.mjs` — single-file render/overflow delivery gate.

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
(tag and ledger the gap instead), and **the fund-manager deliverable is a ranked,
confidence-tagged driver decomposition** — quantified allocations are clearly-labeled
`Reasoned` judgment whose sum-to-move identity is a consistency check, not a claim of
measurement.
