# Report Design — Midnight IC System & Page Architecture

The default deliverable is a 12–16 page HTML slide deck at a fixed 1280×720 canvas, styled
as an institutional IC memo. This file is the complete visual spec; `assets/slides_brief.template.json`
is the content plan that precedes any page.

## Table of contents

1. [Design tokens](#1-design-tokens)
2. [Component library](#2-component-library)
3. [Citation & confidence conventions](#3-citation--confidence-conventions)
4. [The 15-page archetype map](#4-the-15-page-archetype-map)
5. [Layout & the overflow budget](#5-layout--the-overflow-budget)
6. [Charts](#6-charts)
7. [Viewer & delivery packaging](#7-viewer--delivery-packaging)

---

## 1. Design tokens

Aesthetic reference: classic institutional IC memo — deep navy canvas, ivory serif body,
gold accents, mono numerals, hairline borders, generous data density (style inspiration
only; no affiliation with any firm). No photos, no emoji, no gradients beyond the tokens below.

```css
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Serif:ital,wght@0,400;0,500;0,600;1,400&family=IBM+Plex+Mono:wght@400;500;600&display=swap');
/* The @import is progressive enhancement. For offline/air-gapped environments
   the local fallbacks in the stacks below carry the deck (metrics differ slightly —
   the render audit tolerates both). To make a deck fully self-contained, download
   the IBM Plex families into the deck folder and swap the @import for @font-face. */

:root {
  /* Midnight IC palette — all text tokens below clear WCAG 2.2 AA (4.5:1)
     against both --bg and --card; see the contrast table in §1.1. */
  --bg: #0A1628;            /* slide canvas */
  --bg-2: #0E1D33;          /* secondary zones */
  --card: #10233E;          /* standard card */
  --card-2: #142A4A;        /* elevated card */
  --ink: #F2EDE4;           /* primary text (ivory) */
  --muted: #9DA9BC;         /* secondary text */
  --faint: #8493A8;         /* tertiary text (AA on bg and card) */
  --accent: #C9A227;        /* gold — kickers, key numbers, verdict bands */
  --accent-soft: rgba(201, 162, 39, 0.13);
  --gold-line: rgba(201, 162, 39, 0.38);
  --line: rgba(242, 237, 228, 0.14);   /* hairlines & card borders */
  --neg: #E66A5F;  --neg-soft: rgba(230, 106, 95, 0.13);   /* misses / evidence FOR (AA on bg and card) */
  --pos: #4CA97A;  --pos-soft: rgba(76, 169, 122, 0.13);  /* beats / evidence AGAINST */

  /* Typography */
  --font-heading: 'IBM Plex Sans', 'Segoe UI', sans-serif;
  --font-body: 'IBM Plex Serif', Georgia, serif;
  --font-num: 'IBM Plex Mono', 'Courier New', monospace;
  --fs-display: 52px; --fs-h1: 33px; --fs-h2: 21px; --fs-h3: 16.5px;
  --fs-body: 14px; --fs-small: 12px; --fs-micro: 10.5px;
}
.slide { position: relative; width: 1280px; height: 720px; overflow: hidden;
         background: var(--bg); color: var(--ink); font-family: var(--font-body); }
```

### 1.1 Text-contrast budget (WCAG 2.2 AA — 4.5:1 for normal-size text)

Computed with the standard WCAG relative-luminance formula; verify again after any
palette change, and treat a token swap without a re-check as a defect:

| Token | On `--bg` #0A1628 | On `--card` #10233E |
|---|---|---|
| `--ink` #F2EDE4 | 15.55:1 ✓ | 13.52:1 ✓ |
| `--muted` #9DA9BC | 7.63:1 ✓ | 6.63:1 ✓ |
| `--faint` #8493A8 | 5.80:1 ✓ | 5.05:1 ✓ |
| `--accent` #C9A227 | 7.49:1 ✓ | 6.52:1 ✓ |
| `--neg` #E66A5F | 5.69:1 ✓ | 4.95:1 ✓ |
| `--pos` #4CA97A | 6.27:1 ✓ | 5.45:1 ✓ |

`--fs-micro` (10.5px) text must still use a token from this table — it is normal-size
for contrast purposes (AA large-text is ≥18pt/24px or 14pt bold), so the 3:1 large-text
threshold never applies to chips and kickers.

Semantic mapping (used consistently across all pages):

- **Red (`--neg`)** = misses, "Evidence FOR the bear case", bear scenario.
- **Green (`--pos`)** = beats, "Evidence AGAINST the bear case", bull scenario.
- **Gold (`--accent`)** = the analysis itself: kickers, verdict bands, key numbers, hypothesis-tree geometry. Gold is reserved for conclusions and structure, never for raw data.
- Mono font (`--font-num`) for every numeral, table cell, date chip and watchlist item; serif for prose; sans for headlines and labels.

## 2. Component library

| Class | Purpose |
|---|---|
| `.card` / `.card-2` | Standard / elevated content card |
| `.card-gold` | Verdict bands, takeaways, "what the panic missed" |
| `.card-neg` / `.card-pos` | Evidence-FOR / evidence-AGAINST panels; bear/bull scenarios |
| `.kicker` | 10.5px letter-spaced uppercase gold label at top of every page ("HYPOTHESIS 2 · PRIMARY — THE MECHANICAL DRIVER") |
| `.num` | Mono numerals with `font-variant-numeric: tabular-nums` — apply to all figures |
| `.src-chip` | Inline source tag at the end of a row/bullet ("Reuters · Oct 28") |
| `.bar-track` / `.bar-fill` | Pure-CSS bars for drawdown ladders, capex stacks, growth comparisons |
| `.hairline` | 1px `--line` divider |

Confidence chips (micro badges after any claim): `VERIFIED` (gold border), `REASONED`
(muted border), `ASSUMED` (red border — must not appear on headline stats),
`UNVERIFIED` (dashed muted border — links to the data-gap list). Build as
`.src-chip` variants; keep text uppercase at `--fs-micro`.

Verdict chips for the hypothesis system: `PRIMARY — NARRATIVE`, `PRIMARY — MECHANICAL`,
`CONTRIBUTOR`, `AMPLIFIER`, `NOISE`, `EXCLUDED`.

## 3. Citation & confidence conventions

- Every page footer (or per-block chip) names its sources: "Yahoo Finance (Sozzi, Oct 29) · Reuters (Oct 28) · Q3 2026 call transcript. Confidence: Verified."
- Derived numbers carry their arithmetic on the page (dotted-leader stack): `FCF −$9.1B → minus EU fine $5.2B → ≈ −$3.9B ex-fine (Reasoned)`.
- Quotes: verbatim, in serif italic, with name + role + shop: "Pivotal Research CEO Jeffrey Wlodarczak: …".
- Final page = full sources ledger: one row per source (mono name + serif description of what it verified), confidence legend, method note, disclaimer ("Informational only — not investment advice…").

## 4. The 15-page archetype map

Compress or extend to 12–16 pages; keep the order — it is the argument itself.

| # | Page | Archetype | Must contain |
|---|---|---|---|
| 01 | Cover | `cover` | Kicker, display title, serif-italic subtitle, 4-card stat strip (move / mkt-cap delta / headline miss / ignored beat), verification-status line ("Verification status: full fact-base + render audits passed", or "Draft — human verification required" + reason), fund-position disclosure + provenance seal line when sealed (round 3), scope legends "Internal analytical pre-read — not a research report" + "Public-source-only" (round 4, reports 8/9 C-1/M-3), data-cutoff + disclaimer footer |
| 02 | The Verdict | `three verdict cards` | PRIMARY-structural, PRIMARY-mechanical, AMPLIFIER cards + gold "what the panic missed" band |
| 03 | Event Timeline | `vertical event rows` | Date-chip rows: priming events → print → AH → T+1 close → peer prints → follow-through; source chip per row |
| 04 | The Scorecard | `data table` | METRIC / ACTUAL / CONSENSUS / VS EST / Y/Y with red-green cells; optical-miss + real-damage footnote cards |
| 05 | The Move | `stats + drawdown ladder` | 2×2 stat cards + CSS ladder ATH → pre-print → post-print → AH; setup paragraph on positioning |
| 06 | Section divider | `section header` | "The Hypothesis Tree" + method note (enumeration discipline, confidence tags) |
| 07 | H1 evidence | `split for/against` | card-neg FOR vs card-pos AGAINST + gold verdict band |
| 08 | H2 evidence | `split + nuance panel` | Wide FOR panel + gold nuance panel with on-slide arithmetic + verdict band |
| 09 | H3+H4 contributors | `two panels` | Each: tag, title, bullets, verification chip; force-multiplier band |
| 10 | H5 amplifier | `three stat zones` | Crowding / macro / sector-tape zones; direction-vs-magnitude confidence split |
| 11 | Evidence Matrix | `matrix table` | All hypotheses × evidence × classification × confidence; EXCLUDED row shows falsifying fact; one-sentence root cause in gold band |
| 12 | Overlooked case | `bento grid` | Verified counter-evidence cards + takeaway band |
| 13 | Street reaction | `actions table + quotes` | Named downgrades/PT moves, consensus PT delta, quote cards, stock-vs-PT read-through (Reasoned) |
| 14 | Scenarios & falsifiers | `three scenario cards` | BULL/BASE/BEAR with conditions + Watch signposts; dated watchlist chips; "analytic frames, not price targets" |
| 15 | Sources ledger | `closing ledger` | Every named source + what it verified; confidence legend; method + disclaimer |

## 5. Layout & the overflow budget

The canvas never scrolls. Content that does not fit is cut, not shrunk into illegibility.
Budgets validated on real decks:

- Page padding 44–56px; content area ≈ 1180×620 after header/footer.
- Max bullets per evidence panel: **5**, each ≤ 2 lines at 14px.
- Table rows: ≤ 9 including header; `--fs-small` for body cells, mono for numbers.
- One headline per page at `--fs-h1` 33px; hero stat per zone at 40–56px mono.
- Stat cards: value + 2-line label max. Bento grids: 4 cards + 1 band maximum.
- Decorative bleed elements (ghost numerals, edge geometry) must be non-content and marked — `data-bleed="intentional"`, or the common `data-decor` / `aria-hidden="true"` conventions — so the overflow audit skips them. Marking by class **name** alone (e.g. a `.bleed` class) is not recognized: the audit only honors the three explicit attributes.
- After building, run `scripts/overflow_audit.mjs` — treat any non-bleed flag as a failure and fix by restructuring the page, not by nudging pixels. Measurement is relative to the `.slide` element, so page margins never mask or fake overflow.

## 6. Charts

- Default to pure-CSS bars/ladders (deterministic, offline, no library): drawdown ladder, capex vs FCF stack, growth comparisons.
- If a chart library is used, it must render fully offline from local data and be verified in the render audit.
- Every chart needs a title, unit labels, and a source line. Annotate the event on time series (vertical hairline + label "Print · Oct 28").
- Never chart a number that is not in the fact base.

## 7. Viewer & delivery packaging

- Build one `viewer.html` next to the pages: an index that iframes each slide full-window with keyboard navigation (←/→, Home/End), a page counter, and direct links. Keep it dependency-free (vanilla JS).
- Delivery set: `slide_NN.html` pages + `global.css` + `viewer.html` + `fact_base.json` + audit reports (numeric + render console output saved as text). The cover's verification-status line must state what the saved reports prove — "Verification status: full fact-base + render audits passed" — or say "Draft — human verification required" with the reason; never leave the audit state implicit.
- If the user requests PPTX/PDF: keep the HTML originals, state that confidence chips and hover interactivity may degrade, and re-run the render audit on the exported artifact.
