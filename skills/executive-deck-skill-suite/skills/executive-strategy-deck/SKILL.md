---
name: building-executive-decks
description: Generates presentation-grade 1280x720 HTML slide decks — annual strategy reviews, business plans, quarterly updates, product launches — in a locked executive design system with deep navy #0A2540 and orange #FF5722 accent, Roboto/MiSans typography, Material Icons, Chart.js doughnut charts, and 10 battle-tested page archetypes (cover, vision+metrics, chart+drivers, persona triptych, dark objectives, pillar matrix, quarterly roadmap, milestone timeline, budget+risk, closing). Each slide is a standalone HTML file that renders pixel-exact in any browser. Use this skill whenever the user asks for slides, a deck, a presentation, PPT, 幻灯片, or 演示文稿 — even a casual "make me a deck about X" — or asks to reproduce, extend, or restyle the navy/orange executive template family. Not for editing existing .pptx binaries or for posters and documents.
version: 1.0.0
---

# Building Executive Decks

## What you build

A deck is a flat directory of standalone HTML pages — one file per slide, each a
fixed 1280×720 canvas, each carrying its own CDN links (Tailwind, Roboto, Material
Icons, Chart.js where needed). No build step, no shared stylesheet, no local assets:
any file opens pixel-exact in a browser, and any slide can be edited or shared alone.

```
<slides_dir>/
├── deck.json          ← the deck manifest (structure + content briefs)
├── slide_01.html      ← cover
├── slide_02.html …    ← content pages
└── slide_NN.html      ← closing
```

**Why this design works** (keep these instincts while generating): the system carries
exactly two hues — navy for structure, orange for emphasis — so every page reads as
one brand; the 85px header bar and title-underline ritual repeat on every content
page, so the deck feels engineered, not decorated; and each page makes ONE argument
with concrete numbers. When a slide feels wrong, the cause is almost always a broken
token: a third color, a missing ritual, or too many messages on one page.

## Skill file map (read on demand — progressive disclosure)

| File | Read it when |
|---|---|
| `references/design-tokens.md` | Before styling any component; whenever unsure of a size, color, or class string |
| `references/layout-catalog.md` | When rendering ANY page — it holds the 10 archetype recipes |
| `references/chart-recipes.md` | Only for chart pages (archetypes 3 and 9) |
| `assets/page_chassis.html` | Copy it as the starting point of each content page |
| `scripts/qa_check.py` | Run in Phase 4. Never edit it to make a slide pass |
| `scripts/geometry_check.js` | Run in Phase 4 when Node + Playwright exist — verifies every page fits 1280×720 |
| `evals/fixtures/*.html` | Canonical reference pages (cover, vision, chart) — open in a browser or diff against them |

## The workflow

Five phases. Skipping Phase 0 produces wrong-topic decks; skipping Phase 4 produces
broken ones. Phases 2–3 may interleave for large decks, but the manifest entry for a
slide is always committed before that slide is rendered.

### Phase 0 — Intake (ask before building)

If any of these is already answered by the request or context, do not re-ask it.
Batch the remaining questions in ONE round (4–6 questions, concrete options each):

1. **Topic & purpose** — what the deck argues, and what the audience should do after.
2. **Audience** — board / exec staff / customers / all-hands (sets formality).
3. **Length** — offer ranges; default 10 pages (the full narrative arc).
4. **Data sourcing** — user-provided facts · researched facts · clearly-labeled
   illustrative demo data. Never present invented numbers as sourced.
5. **Language** — default to the user's language; ALL slide text follows it.
6. **Branding** — company/brand text for the LOGO box and the deck title; the
   classification line (`CONFIDENTIAL & PROPRIETARY` by default).

### Phase 1 — Research and assets

- **Facts.** If the deck needs real-world facts and none were provided, research
  them with the tools available in the environment. If the deck is a demo/template
  run, invent realistic illustrative data and SAY SO in the delivery summary.
- **Images.** Only the cover and closing need photographs — dark, calm, corporate
  (architecture, cityscape at dusk, abstract tech). Resolve BOTH URLs BEFORE
  rendering, using the environment's image-search tool if one exists. Never invent
  an image URL you have not seen returned by a tool. If no image tool is available,
  use the documented no-photo fallback (below) rather than a dead link.

**No-photo fallback** (drop-in replacement for the cover/closing background):
remove the `bg-cover bg-center` + inline `style` from `.ppt-slide`, keep the
overlay, and add decorative circles inside the slide:

```html
<div class="ppt-slide bg-[#0A2540]">
    <div class="absolute inset-0 bg-gradient-to-br from-[#0A2540] via-[#0A2540] to-[#0A2540]/80"></div>
    <div class="absolute -top-20 -right-20 w-96 h-96 bg-[#FF5722]/10 rounded-full"></div>
    <div class="absolute -bottom-16 -left-16 w-72 h-72 bg-[#FF5722]/10 rounded-full"></div>
    <!-- content unchanged -->
```

### Phase 2 — Content plan (commit deck.json BEFORE rendering)

The manifest is the single source of truth for deck structure. Slide order is the
order of the `slides` array — never of filenames.

```json
{
  "deck": {
    "title": "2026 Platform Strategy Review",
    "brand": "ATLAS AI",
    "classification": "CONFIDENTIAL & PROPRIETARY",
    "language": "en",
    "slides_dir": "/absolute/path/to/slides",
    "images": { "cover": "https://…", "closing": "https://…" }
  },
  "slides": [
    {
      "file": "slide_01.html",
      "archetype": "cover",
      "title": "The Agentic Era",
      "brief": "Self-contained verbatim content: eyebrow chip text, title, subtitle (~20 words), meta card 4× label/value, background image key 'cover'."
    }
  ]
}
```

**Brief rules** (a brief is the ONLY input a renderer can rely on):
- Carry exact text, numbers, icon names, chart data, and image URLs — verbatim,
  not paraphrased. If it is not in the brief, it does not exist.
- One message per slide. If a brief needs an "and also", split the slide.
- Keep meta-noise OUT of briefs (no "make it pop", no style reminders) — the design
  system is fixed and lives in the references, not in briefs.

**Archetype selection table** (content shape → archetype):

| The content is… | Use archetype |
|---|---|
| The deck's opening statement | 1 Cover |
| 4 principles + 4 proof numbers | 2 Vision & Metrics |
| A split story: "why it grows" + "how big" | 3 Chart + Drivers |
| One buyer, her pains, her buying process | 4 Persona Triptych |
| 3 audacious targets (rhythm break) | 5 Dark Objectives |
| 6 coordinated programs | 6 Pillar Matrix |
| Phased execution over a year | 7 Quarterly Roadmap |
| Month-by-month delivery calendar | 8 Milestone Timeline |
| Where money goes + what could go wrong | 9 Budget + Risk |
| The closing mandate + contact | 10 Closing |

Canonical 10-page arc: 1-2-3-4-5-6-7-8-9-10. Shorter decks keep 1 and 10 and select
the middle by content shape. Never sequence two grid-heavy pages (2, 6, 7, 8)
without a split (3, 4, 9) or the dark page (5) between them.

### Phase 3 — Render

For each slide, in manifest order:

1. Start from `assets/page_chassis.html` (content pages) or the cover/closing
   recipe in `references/layout-catalog.md` (which replace the body).
2. Insert the archetype's content-zone recipe, filling every `[SLOT]` from the
   brief. Copy class strings EXACTLY — they encode the design system.
3. Chart pages: follow `references/chart-recipes.md` for CDN tag, plugin, config,
   and the custom legend.
4. Update `<title>` to `[Deck Title] — [Page Title]`, `lang`, the header-bar deck
   title, and the brand box text.
5. Verify every `material-icons` name is a real Material Icons name (filled set).

**Language rule:** every rendered word matches `deck.language`. The classification
line may stay English (`CONFIDENTIAL & PROPRIETARY`) when that is the brand
convention — but whatever you choose, use the SAME line on every page.

**Parallel rendering** (optional): if the environment provides subagents, dispatch
contiguous slide ranges (e.g. slides 1–5, 6–10) in one turn; each renderer reads
this SKILL.md, `references/layout-catalog.md`, and the manifest, and writes only
its own files. Solo agents render sequentially — the result is identical.

### Phase 4 — QA gate (never skip)

```bash
python scripts/qa_check.py <slides_dir>
```

If Node and Playwright are available, also run the geometry gate:

```bash
NODE_PATH=/usr/local/lib/node_modules node scripts/geometry_check.js <slides_dir>
```

Every page must report FITS. Overflow is silent in this system — `overflow: hidden`
clips content that exceeds the canvas, so a broken page still LOOKS rendered. The
layout catalog's rhythm values are pre-budgeted to fit; if a page overflows, the fix
is shorter content or the catalog's compact variants — never smaller fonts and
never looser spacing.

- Fix every **FAIL** at the root cause — the fix is almost always copying the
  canonical class string or removing an off-palette color, never editing the
  checker.
- Review every **WARN**; fix it or consciously accept it (cover pages legitimately
  carry fewer words).
- Walk the manual checklist:
  - [ ] Every content page: 85px header bar + title ritual + orange underline
  - [ ] No unintended same-archetype pages back-to-back
  - [ ] Orange ≤ ~10% of visual weight on any page
  - [ ] Content pages carry 60–120 visible words
  - [ ] Chart legend values/units match the dataset exactly
  - [ ] Progress-bar width matches its printed percent
  - [ ] Cover and closing photos differ; both dark and calm
  - [ ] Contrast: white-on-navy and navy-on-white for text; orange only for
        large numbers, icons, and headings — never small orange body text
  - [ ] Every number/fact traces to the brief (and the brief to a source, or is
        labeled illustrative)
- If a browser/screenshot tool is available, visually verify the cover and one
  chart page at 1280×720 before delivering.

## Non-negotiable rules (the quality bar)

These apply to every slide, no exceptions. The QA script enforces the mechanical
subset; you enforce the rest.

1. **Canvas** — exactly 1280×720, `.ppt-slide`, `overflow: hidden`. Nothing may
   scroll, clip, or spill: after the 85px header, 48px top padding, and ~100px
   title block, the content zone has ~455px — the catalog's rhythm values are
   pre-budgeted for it. If content does not fit, cut content — never font sizes,
   never spacing.
2. **Self-containment** — each file carries its own CDN links. No `global.css`, no
   local images, no base64, no `<img>` tags (photographs load via CSS
   `background-image` with an https URL).
3. **Palette lock** — only `#0A2540`, `#FF5722`, `#FF7043`, `#FEFEFE`, `#F4F4F4`
   (page mat), `#FFFFFF`, and their opacity derivatives. No third hue anywhere,
   including charts, severity chips, and icon tints.
4. **Typography lock** — Roboto (+MiSans/Noto Sans SC fallback) only, sizes only
   from the scale in `references/design-tokens.md`.
5. **Rituals** — 85px header bar on every content page (never on cover/closing);
   orange underline under every title; one sentence subtitles.
6. **Icons** — Material Icons (filled), real names, in the canonical tile/chip
   patterns. No emoji, no other icon fonts.
7. **Density** — 60–120 visible words on content pages; every list exactly 4 items
   (3 on Dark Objectives); descriptions one line plus a wrap at most.
8. **No placeholders** — no lorem, TODO, "insert here", or unfilled `[SLOT]`s in
   delivered files. The `LOGO` box carries the actual brand text.
9. **Numbers are honest** — every figure comes from the brief; the brief cites a
   source or the deck is explicitly labeled illustrative.
10. **One message per slide** — if a page argues two things, it is two pages.

## Editing an existing deck built with this skill

- **In-place tweaks** — edit the slide's HTML directly; update its `brief` in
  `deck.json` only when the change alters what the slide says (new headline,
  different data), not for typo fixes.
- **Add a page** — create the HTML file (any stable name) AND insert its entry at
  the right position in `slides[]` in the same edit.
- **Remove a page** — delete the file AND its manifest entry together.
- **Reorder** — move entries within `slides[]`; never rename files.
- Keep exactly one version of each slide on disk — no `slide_04_v2.html` alongside
  `slide_04.html`.
- Re-run the QA gate after structural edits.

## Deliverables and handoff

Deliver the slides directory + `deck.json`. In the handoff summary, state plainly:
deck length, archetype sequence, which numbers are sourced vs illustrative, which
images came from where, and the QA result (e.g. "10 files, 0 FAIL, 1 WARN accepted:
cover carries 42 words"). If the user asked for a `.pptx` and the environment has
an HTML→PPTX converter, run it AFTER the QA gate passes and report its warnings —
but do not invent a converter when none exists; the HTML files are the deliverable.

## Definition of done

- [ ] `deck.json` exists, is valid JSON, and its `slides[]` matches the files on disk
- [ ] `python scripts/qa_check.py <slides_dir>` exits 0 (zero FAIL)
- [ ] `scripts/geometry_check.js` reports FITS on every page (when Node + Playwright available)
- [ ] Manual checklist walked; every WARN fixed or explicitly accepted
- [ ] Cover + one chart page visually verified in a browser (when available)
- [ ] Handoff summary distinguishes Verified / Reasoned / Assumed content and
      sourced vs illustrative data

