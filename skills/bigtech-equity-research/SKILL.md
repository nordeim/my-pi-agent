---
name: bigtech-equity-research
version: 1.4.0
description: "Produce institutional-grade, evidence-based equity research notes on US big-tech stocks (GOOGL, MSFT, AMZN, AAPL, META, NVDA, TSLA, and peers). Use when asked to explain a stock-price event (post-earnings move, guidance shock, regulatory action), analyze a multi-quarter price trend, attribute a drawdown to its drivers, or build a ranked driver decomposition of a price move. The quantified single-note member of the big-tech research family — segment deep-dive with a machine-checked ASC 280 segment-map staleness gate, options math, canonical peer baskets, evidence ledger, and bundled lite delivery audits (placeholder, scoped disclosure, render, accessibility gates) with SHA-256 provenance sealing. For a full audited multi-page IC deck use analyzing-us-bigtech-stocks; for a lighter post-earnings note use big-tech-earnings-postmortem. Outputs a self-contained HTML research note with sourced figures, confidence tags, and a ranked root-cause decomposition. Analytical output only — not investment advice."
license: Apache-2.0
compatibility: Requires web search and page-fetch tools for primary-source verification; numeric helpers need Python 3; render and accessibility gates need Node.js with Playwright.
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
│   ├── segment-maps.json             # Machine-readable map — segment_map_check.py input
│   ├── peers.md                      # Canonical peer baskets + selection criteria
│   └── sourcing-and-confidence.md    # Source hierarchy + confidence taxonomy
├── templates/
│   ├── report-structure.md           # 14-section HTML deliverable spec
│   └── evidence-ledger.md             # Verification ledger format
├── assets/
│   └── checks.json                   # Disclosure needles the lite audit enforces (scoped)
└── scripts/
    ├── quant_helpers.py              # Deterministic delta/excess-return/decomposition math
    ├── segment_map_check.py          # ASC 280 staleness gate (fails the build, not warns)
    ├── note_audit.py                 # Placeholder + scoped disclosure-needle gate
    ├── note_overflow_audit.mjs       # Render/overflow gate (Node + Playwright)
    ├── a11y_audit.mjs                # Accessibility gate (lang/heading/alt/WCAG-AA contrast)
    └── provenance_seal.py            # SHA-256 sealing + tamper-evident verification
```

Turn "why did GOOGL drop after earnings?" or "what's driving the MSFT trend?" into a
fund-manager-quality, fact-based research note.

## Hard rules (read first)
1. **Never fabricate.** Every number is sourced or tagged `Unverifiable`. If a data tool is
   offline, tag the gap and state the exact pull needed — do not invent a figure.
2. **Beat/miss delta moves price, not the absolute number.** Always compute actual − consensus,
   with the consensus carrying a named provider, a vintage within ~10 days of the event, and a
   T1/T2 source — never a lone aggregator print (round 3: the consensus is the denominator of
   every delta; see `reference/methodology.md` Phase 1).
3. **Isolate the idiosyncratic move.** Subtract the same-day index/peer return (or a
   beta-scaled benchmark return) before calling a move "company-specific." The canonical
   default beta window is **2-year monthly returns vs QQQ** — `quant_helpers.abnormal_return`
   applies it automatically when no window is passed and echoes it; an alternative window
   must be justified in the note (a corporate event that structurally changed the risk
   profile).
4. **Rank root causes** and classify each as *structural* vs *cyclical/accounting*. No flat lists.
5. **Tag every figure** with a confidence label: `Verified` / `Reasoned (derived)` /
   `Reasoned (judged)` / `Assumed` / `Unverifiable` — deterministic derivations carry a
   formula and are reproducible; judgment allocations are signed and explicitly non-causal
   (round 3: the split is schema-enforced in the flagship's audit).
6. **Label judgment as judgment.** Driver-decomposition weights and structural-vs-cyclical
   calls are `Reasoned (judged)` analysis, not reported facts — and never presented as measured
   decompositions or regression output. The sum-to-move identity is checked in code
   (`quant_helpers.waterfall_check`), which makes it a consistency check, not evidence.
7. **No investment advice.** Forward-looking views are scenarios, not predictions.
8. **Compute, don't recall.** Never do arithmetic in-context. Every delta, ratio, implied
   move, and multiple is executed with `scripts/quant_helpers.py` (or code) and the
   code's output is what goes in the note — in-context arithmetic is where transcription
   and magnitude errors enter.
9. **Pass the segment-map staleness gate before the variance table.** Run
   `python3 scripts/segment_map_check.py --map reference/segment-maps.json
   --filing-date <YYYY-MM-DD> [--company <TICKER>]` against the filing you are actually
   using — it fails the build when the filing postdates the map's `verified_through`.
   The filing's own ASC 280 segment note is the source of truth; the map is the cached
   baseline expectation. A stale map produces a confidently wrong variance table that
   still passes the numeric audit.
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
2. **Isolate the idiosyncratic move (Phase 2)** — market-adjusted (or beta-adjusted,
   canonical 2-year monthly QQQ window) excess return vs QQQ/XLK + direct comps; options
   implied move (ATM straddle from the T-1 closing chain) vs realized, with the
   volatility-risk-premium caveat. → `reference/formulas.md`
3. **Segment attribution (Phase 3)** — pass `scripts/segment_map_check.py` for the filing
   used, then build the variance table (actual vs consensus, QoQ + YoY via
   `quant_helpers.segment_variance`), per reportable segment. Distinguish **miss** from
   **deceleration**. → `reference/segment-maps.md`
4. **Cost/capex/margin (Phase 4)** — capex vs guidance vs Street; margin trend; depreciation-
   schedule commentary (a stealth margin driver); FCF trajectory paired with FCF ex-SBC.
5. **Macro/regulatory overlay (Phase 5)** — same-week macro, antitrust confounds, peer
   read-through from the canonical basket (`reference/peers.md`) or a documented alternative.
6. **Sell-side reaction (Phase 6)** — PT/rating changes ≤48h, sourced from wire-service pickup.
7. **Root-cause driver decomposition (Phase 7)** — rank the move's drivers; if a
   quantified allocation accompanies the ranking, it is a `Reasoned (judged)` signed allocation
   that sums to the realized move as an arithmetic consistency check — never a
   measured decomposition. → `reference/methodology.md#phase-7`
8. **Assemble deliverable** — 14-section self-contained HTML note.
   → `templates/report-structure.md`, `templates/evidence-ledger.md`
9. **Run the delivery gates** (mandatory, bundled — no sibling skill required):
   `python3 scripts/note_audit.py --note <note.html> --checks assets/checks.json`
   (placeholder + scoped disclosure needles: disclaimer, verification-status line, the
   Reasoned-(judged)-allocation label adjacent to any quantified waterfall, beta
   estimation-window disclosure, the volatility-risk-premium caveat near any implied-move
   discussion, the segment-map vintage line near the variance table, the fund-position
   disclosure when the audience is an IC, Data-Gap Ledger presence),
   `node scripts/note_overflow_audit.mjs --note <note.html>` (render/overflow), and
   `node scripts/a11y_audit.mjs --note <note.html>` (lang / heading order / image alt /
   WCAG-AA contrast — the template claims AA, so the claim is enforced). The note's
   verification-status line must state the actual gate results; if a gate cannot run,
   mark the note "Draft — human verification required" with the reason instead of
   shipping silently. Then seal: `python3 scripts/provenance_seal.py --inputs
   <note.html> --out provenance.json`, embed the printed seal line next to the
   verification-status line, and ship the sidecar with the note.

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
- [ ] Beat/miss deltas computed, not just absolutes — via `quant_helpers.py`, never in-context;
      consensus facts carry provider + vintage + T1/T2 tier.
- [ ] Idiosyncratic move isolated from index/peer benchmark (convention stated; if
      beta-adjusted, the window is disclosed — the canonical 2-year monthly QQQ default
      unless a justified override — and echoed by the helper).
- [ ] `segment_map_check.py` exited 0 for the filing used before the variance table was
      built; the table states "Segment map: vintage verified against <filing>".
- [ ] Root causes ranked and classified structural vs cyclical.
- [ ] Driver allocation (if quantified) uses signed weights, is labeled `Reasoned (judged)`
      allocation — not a measured decomposition — adjacent to the chart, and its sum
      matches the realized move within tolerance (`waterfall_check`).
- [ ] Every figure carries citation + confidence tag; derived vs judged is explicit.
- [ ] FCF figures paired with FCF ex-SBC in the capex/margin section; basis of the
      beat/miss stated.
- [ ] Peer comparison uses the canonical basket or a documented, criteria-based
      alternative (`reference/peers.md`).
- [ ] Segment table separates miss from deceleration and mirrors the filing's ASC 280
      segment note (reportable segments ≠ disclosed revenue lines).
- [ ] Regulatory/macro confounds checked.
- [ ] Deliverable is self-contained HTML, semantic, WCAG-AA (enforced by
      `a11y_audit.mjs`), print-friendly.
- [ ] Valuation boundary stated (§11): forward-multiple band is context, not an
      intrinsic valuation; the model gap is named as an open item.
- [ ] IC-facing deliverables carry the fund-position disclosure ("Fund position: … as of
      <date>").
- [ ] All `Assumed`/`Unverifiable` items listed in the Data-Gap Ledger.
- [ ] `python3 scripts/quant_helpers.py` self-test exits 0 after any helper change.
- [ ] `python3 scripts/segment_map_check.py --selftest` and
      `python3 scripts/provenance_seal.py --selftest` exit 0 after any change to those gates.
- [ ] `python3 scripts/note_audit.py --note <note.html> --checks assets/checks.json`
      exits 0 (placeholder + scoped disclosure gates).
- [ ] `node scripts/note_overflow_audit.mjs --note <note.html>` exits 0 (render gate),
      or the verification-status line says "Draft — human verification required" with
      the reason.
- [ ] Verification-status line present and matches the actual gate results; provenance
      seal line embedded and `provenance.json` shipped when sealed.
- [ ] No fabricated numbers; no investment advice; disclaimer and internal-use framing
      present on the deliverable.

## Supporting files
- `reference/methodology.md` — the 7-phase process in full.
- `reference/formulas.md` — market-adjusted excess return, implied move, deltas, driver decomposition, PT math.
- `reference/segment-maps.md` — reportable segments (ASC 280) per big-tech company, with `segment_map_version` / `last_verified_against_filing` staleness control.
- `reference/segment-maps.json` — machine-readable mirror; input to `segment_map_check.py`.
- `reference/peers.md` — canonical peer baskets and the selection criteria that make a peer legitimate.
- `reference/sourcing-and-confidence.md` — source hierarchy + confidence taxonomy.
- `templates/report-structure.md` — 14-section HTML deliverable spec.
- `templates/evidence-ledger.md` — verification ledger format.
- `assets/checks.json` — scoped disclosure needles enforced by the lite audit.
- `scripts/quant_helpers.py` — deterministic delta/excess-return/decomposition math (canonical beta window, FCF ex-SBC, segment variance).
- `scripts/segment_map_check.py` — mechanical segment-map staleness gate.
- `scripts/note_audit.py` — placeholder + scoped disclosure-needle delivery gate.
- `scripts/note_overflow_audit.mjs` — single-file render/overflow delivery gate.
- `scripts/a11y_audit.mjs` — accessibility delivery gate (WCAG-AA claim enforcement).
- `scripts/provenance_seal.py` — SHA-256 provenance sealing and tamper-evident verification.

---

## How an agent uses this skill

1. **Trigger** — the `description` matches any request to explain a big-tech move or trend.
2. **Route** — Step 0 picks Event / Trend / Pre-event mode.
3. **Execute** — run Phases 1–7 from `reference/methodology.md`, using `segment-maps.md` for
   the company's accounting, `formulas.md` + `quant_helpers.py` for the math, and
   `sourcing-and-confidence.md` for tagging.
4. **Render** — assemble via `templates/report-structure.md` and `evidence-ledger.md`.
5. **Gate** — the Definition-of-Done checklist in `SKILL.md` must pass before delivery.

The hard-won lessons from our sessions are baked in: **never fabricate when tools are offline**
(tag and ledger the gap instead), and **the fund-manager deliverable is a ranked,
confidence-tagged driver decomposition** — quantified allocations are clearly-labeled
`Reasoned (judged)` signed allocations whose sum-to-move identity is a code-checked
consistency test, not a claim of measurement. Round 3 added the machine-checked layer
the prose used to promise: the segment-map staleness gate, scoped disclosure needles,
the a11y gate, the canonical beta window, and provenance sealing.
