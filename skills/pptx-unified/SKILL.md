---
name: pptx-unified
description: >
  Unified practical recipe for generating impressive marketing-grade .pptx
  presentations from scratch. Combines the canonical pptx skill's HTML-first
  4-stage pipeline (Clarify → Research → Plan → Build → Export) with the
  variant skills' distinctive strengths (cyber-ppt's confirmation gates,
  pptx-generator's PptxGenJS templates, codex-ppt's image-based fallback)
  and 20+ real-world lessons/anti-patterns distilled from building a
  12-slide deck for the my-pi-agent repo. Use this skill when ANY coding
  agent needs to produce a polished .pptx — it is the single starting point
  that routes to the right variant only when a specific capability is needed.
  Triggers: "make a presentation", "generate a .pptx", "build a slide deck",
  "marketing deck", "pitch slides", "create slides for this repo/product".
license: MIT
metadata:
  version: "1.0.0"
  category: document-generation
  author: Claw Code (distilled from real build experience)
  sources:
    - "Canonical Z.AI pptx skill (skills/pptx/SKILL.md)"
    - "cyber-ppt skill (3-phase MBB pipeline + confirmation gates)"
    - "pptx-generator skill (PptxGenJS-native 5 page types)"
    - "codex-ppt skill (image-based full-slide deck fallback)"
    - "Real build: my-pi-agent 12-slide marketing deck (2026.07)"
---

# pptx-unified — A Practical Recipe for Impressive .pptx Decks

> **The single starting point for any coding agent that needs to produce a
> polished .pptx.** This skill combines the canonical HTML-first pipeline
> with 20+ lessons distilled from real builds. It routes to variant skills
> only when a specific capability is needed — start here, branch only when
> you must.

---

## When to Use This Skill vs. the Variants

| Scenario | Use |
|----------|-----|
| **Default — most decks** | **This skill (`pptx-unified`)** |
| Need MBB-grade consulting deck with evidence chains + SCR argumentation | `cyber-ppt` |
| Need PptxGenJS-native shapes/charts (not HTML) | `pptx-generator` |
| Need full-slide AI-generated image deck (text-in-image OK) | `codex-ppt` |
| Editing an existing .pptx (text replacement, slide reorder) | `pptx` (Approach A: python-pptx) |
| Need raw OOXML access (animations, comments, speaker notes XML) | `pptx` (Approach B: raw OOXML) |

**Decision rule:** Start with `pptx-unified`. Only branch to a variant when
you hit a specific capability this skill doesn't cover. The variants are
specialized tools; this skill is the general-purpose workhorse.

---

## The 5-Stage Pipeline

```
Stage 1: CLARIFY  → collect user choices (or apply recommended defaults)
Stage 2: RESEARCH → gather facts + image assets (parallel, batched)
Stage 3: PLAN     → commit global.css + slides_brief.json to disk
Stage 4: BUILD    → fan out 3 ppt-expert sub-agents to render slides in parallel
Stage 5: EXPORT   → convert slides/ → .pptx via batch_html2pptx.js
```

**Iron rules (non-negotiable):**
1. Never skip stages. Each stage produces an artifact the next stage depends on.
2. Stage 4 sub-agent fan-out is capped at **3 Agent calls** per deck. More groups = weaker visual consistency + more spin-up overhead.
3. The `slides_brief.json` is the **single source of truth**. If on-disk slides and the brief diverge, the brief wins.
4. Every slide is a standalone 1280×720 HTML page that links `global.css` via relative path. No exceptions.
5. The final .pptx export MUST go through `batch_html2pptx.js` (vector text, selectable, small file). Never screenshot-to-PDF.

---

## Stage 1: CLARIFY

**Goal:** Collect 6 mandatory inputs before writing any code.

**Load `references/stage-1-clarify.md` for the full protocol.** Quick summary:

### The 6 mandatory dimensions

| # | Dimension | Why it matters |
|---|-----------|----------------|
| 1 | **Audience** | Determines tone, density, and which features to highlight |
| 2 | **Deck length** | 8 (lightning) / 12 (standard marketing) / 16+ (comprehensive reference) |
| 3 | **Palette** | bg + primary + accent as a coherent trio — see `references/palette-presets.md` |
| 4 | **Typography** | heading + body + numeric font pairing — see `references/typography-pairings.md` |
| 5 | **Visual reference** | A named style anchor (Linear changelog, Vercel keynote, Stripe Press, etc.) |
| 6 | **Speaker notes** | none / short (3-5 bullet hints) / full (~80-150 word script) |

### The "no-approvals" shortcut

If the user has explicitly said "no need to ask for my approvals" or "proceed with your best recommendations", skip the `AskUserQuestion` call and apply recommended defaults:

- **Audience:** infer from the source material (a repo README → "developers/power users")
- **Length:** 12 slides (the marketing sweet spot)
- **Palette:** GitHub Dark (`#0D1117` / `#E6EDF3` / `#58A6FF`) — matches most dev-tool repos
- **Typography:** Inter + JetBrains Mono — clean, modern, developer-native
- **Visual reference:** Linear changelog — dark, generous whitespace, big stats
- **Speaker notes:** short (3-5 bullet hints)

**Document the chosen defaults in the `slides_brief.json` `design` block** so downstream sub-agents have a single source of truth.

### Anti-pattern: skipping clarify "because the request is clear"

Even when the user says "make a deck about X", you still need to confirm audience + length + palette. A 20-slide comprehensive reference deck and an 8-slide lightning talk are completely different artifacts. Skipping clarify is the #1 cause of full-deck re-renders.

---

## Stage 2: RESEARCH

**Goal:** Gather facts and image assets in parallel.

**Load `references/stage-2-research.md` for the full protocol.** Quick summary:

### Fact gathering
- If the source material is a repo, read the README, package.json, and key directory listings.
- If facts need web verification, batch 2-3 `web_search` calls in a single turn (parallel).
- **Anti-pattern:** fabricating stats. If you can't verify a number, say so explicitly in the slide rather than inventing one.

### Image search (when photos are needed)
- Use `z-ai image-search --query "<natural-language sentence>" --count 3` via the `z-ai` CLI.
- **HARD LIMIT: 6 image-search calls per deck trajectory.** Plan image needs up front.
- The sub-agent that renders the slide has NO access to search results — bake the picked `original_url` directly into the slide's `task_brief` in `slides_brief.json`.
- **Photo-free decks are valid.** The my-pi-agent marketing deck (the reference build) used zero photos by design — Linear-style decks rely on typography + whitespace, not imagery.

### Anti-pattern: serial research calls
Never emit one `web_search` call per turn. Batch 2-3 queries in a single turn — they run concurrently and save 30-60 seconds of wall time.

---

## Stage 3: PLAN

**Goal:** Commit `global.css` + `slides_brief.json` to disk BEFORE any sub-agent fan-out.

**Load `references/stage-3-plan.md` for the full protocol + `references/global-css-template.md` for the canonical CSS scaffold.** Quick summary:

### Directory layout (MANDATORY)

```
<work_dir>/slides/
├── global.css              ← deck-wide stylesheet (CSS variables + utilities, NO typography classes)
├── slides_brief.json       ← dispatch manifest (design block + slides[] array)
├── slide_01.html           ← written in Stage 4 by sub-agents
├── slide_02.html
└── ...
```

`<work_dir>` IS the user's `download/` directory itself. Do NOT create an intermediate themed subdirectory. The slides folder must end up at `download/slides/`, NOT `download/<topic>/slides/`.

### global.css rules

1. **Define typography TOKENS on `:root`, not pre-baked classes.** Use `--font-heading`, `--font-body`, `--font-num`, `--fs-display`, `--fs-h1`, etc. Do NOT ship `.h-display` / `.h-1` / `.h-2` classes that bundle font-family + size + weight — sub-agents will re-define them per-slide and the cascade breaks.
2. **CSS variables for palette:** `--bg`, `--primary`, `--accent`, plus tonal stops (`--bg-elevated`, `--border`, `--primary-muted`).
3. **`@import` Google Fonts at the top** — one line, both font families.
4. **Reusable utility classes are OK:** `.slide` (1280×720 canvas), `.card`, `.eyebrow`, `.footer`, `.tag`, `.mono`, `.accent`, `.muted`.
5. **Keep under ~150 lines.** Per-slide layout CSS lives in each slide's HTML, not here.
6. **Avoid Tailwind class collisions:** never name a custom class `.h-1` / `.h-2` / `.h-3` (Tailwind height utilities), `.hidden` (Tailwind display utility), etc.

### slides_brief.json schema

```json
{
  "design": {
    "title": "(ppt title)",
    "style_name": "...",
    "palette": {"background": "#...", "primary": "#...", "accent": "#..."},
    "typography": {"heading": "xx", "body": "xx", "numeric": "xx"},
    "reference": "Linear changelog / Vercel keynote / ..."
  },
  "global_css_path": "<absolute path to slides/global.css>",
  "slides_dir": "<absolute path to slides/>",
  "language": "en|zh|bilingual",
  "speaker_notes": "none|short|full",
  "slides": [
    {
      "title": "...",
      "layout": "cover|stat_block|bento_grid|stats_grid|section_divider|split_text_features|comparison_card|three_column_spotlight|timeline|step_guide|closing",
      "output_path": "<absolute path to slides/slide_XX.html>",
      "task_brief": "Self-contained brief — verbatim slide content + image URLs + speaker notes hint."
    }
  ]
}
```

### task_brief rules (CRITICAL — the sub-agent sees ONLY this)

1. **Restate every text element verbatim** — headline, body, bullets, stats, quotes. Do not paraphrase.
2. **Inline every image URL** from `z-ai image-search` results. The sub-agent has no search access.
3. **Specify layout structure** — "left 55% for title, right 45% for 3 stat cards" gives the sub-agent a concrete grid.
4. **No meta-reminders** — don't repeat "diversify layouts" or "verify contrast" per slide. Those live once in the sub-agent dispatch prompt.
5. **Speaker notes hint** — if `speaker_notes` is `short`/`full`, append `Speaker notes: short hints — '<guidance>'` at the end. The sub-agent generates the actual notes.

### Layout catalog (12 patterns)

**Load `references/layout-catalog.md` for full specs.** Index:

| Layout | When to use |
|--------|-------------|
| `cover` | Slide 1 — repo/product name + tagline + 3 stat cards |
| `stat_block` | One massive number dominates the slide (hero stat) |
| `bento_grid` | 2×2 or 3×2 grid of equal cards (component overview) |
| `stats_grid` | 5×2 dense grid of small stat cards (category map) |
| `section_divider` | Chapter break — "01 / 03" marker + title + tagline |
| `split_text_features` | Left = item list, right = "why this matters" card |
| `comparison_card` | 3 vertical cards side-by-side (variant comparison) |
| `three_column_spotlight` | 3 columns with big number + tag cloud |
| `timeline` | Horizontal N-step pipeline (skill composition proof) |
| `step_guide` | N numbered steps with monospace code blocks |
| `closing` | Big URL + tagline + 3 takeaway cards |

**Diversify layouts across consecutive slides.** Never repeat the same layout back-to-back. A 12-slide deck should use 8+ distinct layouts.

### Anti-pattern: writing slides_brief.json without absolute paths

Sub-agents receive the brief path as a string. If `global_css_path` is relative (`global.css`), the sub-agent may resolve it against its own cwd, not the slides/ directory. **Always use absolute paths** in `slides_brief.json` fields.

---

## Stage 4: BUILD

**Goal:** Fan out 3 `ppt-expert` sub-agents to render all slides in parallel.

**Load `references/stage-4-build.md` for the full dispatch prompt template.** Quick summary:

### The 3-call cap

**HARD CAP: at most 3 `Agent` calls per deck.** If the deck has more sections than 3 groups, MERGE adjacent sections rather than spawning a 4th group. More groups = more sub-agent spin-up overhead AND weaker visual consistency.

### Grouping strategy

For a 12-slide deck, 3 groups of 4 slides each is ideal:

| Group | Slides | Narrative section |
|-------|--------|-------------------|
| Agent 1 | slides[0:4] | Opening (Cover + Hook + Bento + Category Map) |
| Agent 2 | slides[4:8] | Middle (Section Divider + 3 family deep-dives) |
| Agent 3 | slides[8:12] | Closing (Beyond + Timeline + Setup + CTA) |

Groups should follow narrative sections, not arbitrary index ranges. A group rendering 4 contiguous slides locks in consistent layout language across that section.

### Dispatch in a SINGLE turn

Emit ALL 3 `Agent` calls in ONE assistant turn. They run concurrently — this is 3-5× faster than sequential iteration.

### The dispatch prompt (use this exact shape)

```
You are a slide-rendering sub-agent. Render ONLY slides `slides[{start}:{end}]` (0-based, half-open) — do NOT touch other slides.

First Read these absolute paths:
  • Brief manifest:    {absolute path to slides/slides_brief.json}
  • Global stylesheet: {absolute path to slides/global.css}
Both live in the SAME directory ({absolute path to slides/}); write each slide HTML there as a sibling.

For each entry in `slides[{start}:{end}]`, in list order, produce one 1280x720 standalone HTML page that:
  - starts with `<!DOCTYPE html>`, ends with `</html>`, and links `global.css` via `<link rel="stylesheet" href="global.css">` in `<head>`
  - loads Tailwind via `<script src="https://cdn.tailwindcss.com"></script>` and Material Icons via `<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">`
  - uses ONLY the palette/typography in `design`, and renders EVERY fact/headline/bullet/stat/quote in `task_brief` verbatim
  - obeys every constraint in the SLIDE QUALITY BAR (exact 1280×720 canvas, overflow-hidden, WCAG AA contrast, diversified layouts, no fabricated image URLs, no graphical timelines/SVG flowcharts/code-drawn maps/base64 images/Reveal.js)
  - speaker notes: since `speaker_notes` is `{none|short|full}`, generate notes as the LAST `<body>` child `<aside data-notes class="hidden">…</aside>` (visually hidden via Tailwind's `hidden` class). Match the deck language. {If short: "3-5 bullet hints"} {If full: "~80-150 word script"} {If none: "omit entirely"}

Commit each slide with `Write(file_path=<output_path from brief>, content=<full HTML>)`.

The {N} slides you are responsible for:
  - slides[{i}]: "{title}" → {output_path}
  - slides[{i+1}]: "{title}" → {output_path}
  ...

Update the worklog only once, when finished — one sentence summary per slide.
```

**Pass `subagent_type: ppt-expert`.** If unavailable, fall back to `general-purpose` and prepend the rendering rules from this skill.

### Anti-pattern: the main agent writes slide HTML

The main agent NEVER calls `Write` to commit slide HTML. This serializes work and removes the parallelism benefit. Every slide — cover, body, closing — is committed by a sub-agent.

---

## Stage 5: EXPORT

**Goal:** Convert `slides/` → single `.pptx` via `batch_html2pptx.js`.

**Load `references/stage-5-export.md` for the full path-resolution + warning-triage protocol.** Quick summary:

### The path-resolution trap (LESSON #1 from real build)

The canonical `pptx` skill's SKILL.md says the script is at:
```
/home/z/my-project/skills/ppt/batch_html2pptx.js    ← WRONG (skill doc typo)
```

The actual location is:
```
/home/z/my-project/skills/pptx/batch_html2pptx.js   ← CORRECT
```

**Always resolve the script path dynamically** rather than hard-coding:
```bash
SCRIPT=$(find /home/z/my-project/skills -name "batch_html2pptx.js" -type f | head -1)
NODE_PATH=/usr/local/lib/node_modules node "$SCRIPT" /path/to/slides /path/to/output.pptx
```

Or use the bundled wrapper:
```bash
bash /home/z/my-project/my-pi-agent/skills/pptx-unified/scripts/export_pptx.sh /path/to/slides /path/to/output.pptx
```

### Export command

```bash
cd /home/z/my-project && \
NODE_PATH=/usr/local/lib/node_modules node \
  /home/z/my-project/skills/pptx/batch_html2pptx.js \
  /home/z/my-project/download/slides \
  /home/z/my-project/download/<deck-name>.pptx
```

- `NODE_PATH=/usr/local/lib/node_modules` is REQUIRED so `pptxgenjs` / `playwright` / `sharp` resolve.
- Arg 1: slides directory. Arg 2 (optional): output path; defaults to `<work_dir>/<basename>.pptx`.

### Warning triage

Per-slide warnings from the converter:

| Warning | Severity | Action |
|---------|----------|--------|
| `🚨 CRITICAL OVERFLOW` | Hard blocker | Fix the source HTML and re-run (the .pptx is overwritten in place) |
| `⚠ BOUNDS` | Soft warning | Review — likely a shape slightly outside the 1280×720 canvas |
| `⚠ FONT` | Soft warning | Review — font may not have loaded; check Google Fonts `@import` |
| `⚠ OVERLAP` | Soft warning | Review — two elements may be touching; adjust spacing |
| `⚠ LAYOUT` | Soft warning | Review — layout heuristic flagged something unusual |
| `Browser console: cdn.tailwindcss.com should not be used in production` | Ignore | Tailwind CDN is fine for slide rendering (not production web) |

### Anti-pattern: trusting "Done." without checking exit code

The converter prints `Done.` even when some slides had `🚨 CRITICAL` warnings. Always scan the full output for `🚨` and fix any critical issues before delivering the .pptx.

---

## SLIDE QUALITY BAR (applies to every page)

Every slide MUST:

- [ ] Be exactly 1280 × 720 pixels, `overflow: hidden`, no scroll
- [ ] Carry 60-120 words of substantive text (no placeholders, no lorem ipsum)
- [ ] Use ONLY the committed palette (bg / primary / accent from `slides_brief.json.design.palette`)
- [ ] Pass WCAG AA contrast on every text-on-background combination (4.5:1 minimum)
- [ ] Load Tailwind via CDN + link `global.css` via relative path
- [ ] Load Material Icons via the Google Fonts CDN (`<i class="material-icons">name</i>`)
- [ ] Diversify layouts — never repeat the same layout on consecutive slides
- [ ] Never fabricate image URLs — only use URLs from real `z-ai image-search` results
- [ ] Render numbers/dates/code in the numeric font (JetBrains Mono or equivalent)
- [ ] Embed speaker notes as the LAST `<body>` child: `<aside data-notes class="hidden">…</aside>`

Every slide MUST NOT:

- [ ] Use graphical timelines, SVG/connector flowcharts, or code-drawn maps
- [ ] Embed base64 images
- [ ] Use Reveal.js or any slideshow framework
- [ ] Add headers/footers unless the user explicitly asked for them
- [ ] Exceed the canvas — if content overflows, the sub-agent must shrink font (last resort) or trim content (preferred)

---

## Post-Build Verification Checklist

After Stage 5 export, verify:

- [ ] `ls -lh <output.pptx>` — file exists, size > 0
- [ ] `file <output.pptx>` — reports "Zip archive data" (valid OOXML)
- [ ] Converter output had ZERO `🚨 CRITICAL` warnings
- [ ] Slide count in .pptx matches `slides_brief.json.slides[]` length
- [ ] Source HTML + global.css + slides_brief.json preserved at `<work_dir>/slides/` for future edits

---

## Multi-Round Editing Protocol

When the user asks for revisions after the initial build:

### In-place content tweak (typo, single bullet)
1. Edit the specific `slide_NN.html` directly.
2. Re-run Stage 5 export (overwrites the .pptx in place).
3. Do NOT update `slides_brief.json` for trivial fixes.

### Layout-level change (different layout, new image, restructured content)
1. Update the slide's `task_brief` in `slides_brief.json` FIRST.
2. Edit the `slide_NN.html` to match the new brief.
3. Re-run Stage 5 export.

### Adding a slide
1. Insert a new entry into `slides_brief.json.slides[]` at the desired position.
2. Create the new HTML file (any stable filename like `slide_NEW1.html`).
3. Update the brief's `output_path` fields if filenames need to sort alphabetically into list order.
4. Re-run Stage 5 export.

### Removing a slide
1. Delete the entry from `slides_brief.json.slides[]`.
2. Delete the HTML file.
3. Re-run Stage 5 export.

### Reordering slides
1. Move entries within `slides_brief.json.slides[]` (the list order IS the slide order — no `position` field).
2. Do NOT rename files — keep filenames stable.
3. Before Stage 5 export, ensure filenames sort alphabetically into the same order as the list. If not, rename to `slide_{NN:02d}.html` matching list index AND update each entry's `output_path`.

**Iron rule:** `slides_brief.json` is the single source of truth. If on-disk slides and the brief diverge, the brief wins. Update the brief in the SAME turn as any structural change — never let them diverge.

---

## Cross-References

| Skill | When to branch to it |
|---|---|
| [`../pptx/`](../pptx/SKILL.md) | The canonical Z.AI pptx skill — this skill's primary source. Branch here for: (a) editing existing .pptx files via `python-pptx` text replacement (Approach A), (b) raw OOXML access for animations/comments/speaker-notes XML (Approach B), (c) academic presentations using the embedded Beamer module (PDF output). |
| [`../cyber-ppt/`](../cyber-ppt/SKILL.md) | When the deck needs MBB-grade consulting rigor: evidence-chain tables, SCR argumentation, issue/hypothesis trees, 8 fixed visual styles, 3 mandatory confirmation gates. Use for evidence-driven consulting decks from DOCX/PDF/XLSX source material where the audience expects MBB-grade analysis. |
| [`../pptx-generator/`](../pptx-generator/SKILL.md) | When you want PptxGenJS-native shapes/charts (not HTML) — 5 page types (Cover/TOC/Section Divider/Content/Summary), 4 style recipes (Sharp/Soft/Rounded/Pill), 18 curated color palettes. Also supports XML-based editing of existing template PPTX files. |
| [`../codex-ppt/`](../codex-ppt/SKILL.md) | When visual unity matters more than per-shape editability — each slide is a complete 16:9 AI-generated image, assembled via `assemble_ppt.py`. Use for "final form" decks where text-in-image is acceptable. |
| [`../charts/`](../charts/SKILL.md) | When a slide needs a data chart — generate a PNG via the charts skill and embed it via `<img>` in the slide HTML. Render at 2× device scale factor for 300dpi print quality. |
| [`../image-search/`](../image-search/SKILL.md) | When a slide needs a photo — `z-ai image-search --query "<natural-language sentence>" --count 3`. Hard limit: 6 calls per deck trajectory. |
| [`../docx/`](../docx/SKILL.md) / [`../pdf/`](../pdf/SKILL.md) | When the deck needs a companion handout document — generate the .docx/.pdf with the canonical skills, then reference it from a closing slide. |

---

## File Map

```
pptx-unified/
├── SKILL.md                          ← You are here (5-stage recipe + quality bar)
├── references/
│   ├── stage-1-clarify.md            ← Question design + default-recommendation protocol
│   ├── stage-2-research.md           ← Image search (6-call limit) + fact gathering
│   ├── stage-3-plan.md               ← global.css + slides_brief.json schema + layout catalog
│   ├── stage-4-build.md              ← Sub-agent fan-out (3-call cap) + dispatch prompt
│   ├── stage-5-export.md             ← batch_html2pptx.js path resolution + warning triage
│   ├── layout-catalog.md             ← 12 layout patterns with structural rules
│   ├── global-css-template.md        ← Canonical CSS scaffold (tokens, utilities, no classes)
│   ├── palette-presets.md            ← 8 curated palettes with use-case fit
│   ├── typography-pairings.md        ← 6 font pairings with use-case fit
│   └── anti-patterns.md              ← 20+ lessons/anti-patterns from real builds
└── scripts/
    ├── validate_brief.py             ← Validate slides_brief.json schema + path checks
    └── export_pptx.sh                ← Wrapper that finds batch_html2pptx.js + runs export
```

### Loading protocol

> **⚠️ DO NOT SKIP FILES. DO NOT SKIM.**

**Step 1 — ALWAYS read (every task):**
- This file (SKILL.md) — the 5-stage recipe + quality bar

**Step 2 — Read the stage file matching your current phase:**
- Starting Stage 1? Read `references/stage-1-clarify.md`
- Starting Stage 2? Read `references/stage-2-research.md`
- etc.

**Step 3 — Read every file the stage file references:**
- Stage 3 references `layout-catalog.md`, `global-css-template.md`, `palette-presets.md`, `typography-pairings.md` — read them all before writing `global.css` or `slides_brief.json`.

**Step 4 — Before delivery, read `references/anti-patterns.md`:**
- 20+ real-world lessons. Skim the titles; read any that match your current build context.

**Checkpoint before export:** Can you name the exact `batch_html2pptx.js` path, the 3-call sub-agent cap, the 6-call image-search limit, and the WCAG AA contrast threshold? If not, re-read this SKILL.md.

---

## Lessons Learned (Distilled from the Reference Build)

The my-pi-agent 12-slide marketing deck (2026.07) was the reference build for this skill. Key lessons that shaped this recipe:

1. **Path-resolution trap:** The canonical `pptx` skill's SKILL.md contains a typo (`skills/ppt/` instead of `skills/pptx/`). Always `find` the script dynamically.
2. **Sub-agent fidelity notes:** Sub-agents will make small fidelity compromises (e.g., setting a title at 110px instead of 120px to fit the column). This is acceptable — document it in the worklog but don't force a re-render.
3. **Photo-free decks are valid:** The reference build used zero photos. Linear-style dark decks rely on typography + whitespace + accent color, not imagery. Don't force image searches when the visual reference doesn't call for them.
4. **`AskUserQuestion` can be skipped** when the user has explicitly delegated decisions — apply recommended defaults and document them in the brief.
5. **The 3-call sub-agent cap is real.** A 12-slide deck → 3 groups of 4. A 16-slide deck → 3 groups of 5-6. Never 4 groups.
6. **`slides_brief.json` is the contract.** Sub-agents see ONLY the brief — every text element, image URL, and layout instruction must be inlined verbatim. Paraphrasing produces drift.

**Load `references/anti-patterns.md` for the full 20+ lesson catalog.**
