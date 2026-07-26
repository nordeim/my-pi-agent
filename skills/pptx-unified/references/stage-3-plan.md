# Stage 3: PLAN

> Commit `global.css` + `slides_brief.json` to disk BEFORE any sub-agent fan-out. This is the contract that every sub-agent will read.

---

## Directory layout (MANDATORY)

```
<work_dir>/slides/
├── global.css              ← deck-wide stylesheet
├── slides_brief.json       ← dispatch manifest
├── slide_01.html           ← written in Stage 4 by sub-agents
├── slide_02.html
└── ...
```

### `<work_dir>` definition

`<work_dir>` IS the user's `download/` directory itself. Do NOT create an intermediate themed subdirectory.

- ✅ `/home/z/my-project/download/slides/`
- ❌ `/home/z/my-project/download/my-pi-agent-deck/slides/`
- ❌ `/home/z/my-project/download/marketing/slides/`

Every `<work_dir>/...` path in this skill resolves under `download/` directly.

### Why flat?
Sub-agents resolve `<link rel="stylesheet" href="global.css">` relative to the slide HTML's location. If global.css and slides are siblings in the same directory, the relative path works regardless of the sub-agent's cwd. Nesting breaks this.

---

## Writing `global.css`

**Load `global-css-template.md` for the canonical scaffold.** Key rules:

### 1. Typography TOKENS, not classes

✅ CORRECT — define tokens on `:root`:
```css
:root {
  --font-heading: 'Inter', system-ui, sans-serif;
  --font-body: 'Inter', system-ui, sans-serif;
  --font-num: 'JetBrains Mono', monospace;
  --fs-display: 120px;
  --fs-h1: 56px;
  --fs-h2: 40px;
  --fs-h3: 28px;
  --fs-body: 18px;
  --fs-small: 15px;
  --fs-micro: 13px;
}
```

❌ FORBIDDEN — pre-baked typography classes:
```css
.h-display { font-family: var(--font-heading); font-size: 120px; font-weight: 800; line-height: 1.1; }
.h-1 { font-family: var(--font-heading); font-size: 56px; font-weight: 700; }
/* Sub-agents will fight these and the cascade breaks */
```

**Why:** Sub-agents apply per-slide inline styles using the tokens. If you ship pre-baked classes, sub-agents either (a) ignore them and redefine inline (cascade conflict) or (b) use them and lose per-slide flexibility.

### 2. CSS variables for palette

```css
:root {
  --bg: #0D1117;
  --bg-elevated: #161B22;
  --bg-surface: #1C2128;
  --border: #30363D;
  --border-muted: #21262D;
  --primary: #E6EDF3;
  --primary-muted: #8B949E;
  --primary-subtle: #6E7681;
  --accent: #58A6FF;
  --accent-soft: rgba(88, 166, 255, 0.12);
  --accent-glow: rgba(88, 166, 255, 0.25);
}
```

Include tonal stops (`--bg-elevated`, `--border`, `--primary-muted`) — sub-agents need them for card surfaces and hierarchy.

### 3. `@import` Google Fonts

One line at the top:
```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');
```

### 4. Reusable utility classes (OK)

```css
.slide { width: 1280px; height: 720px; background: var(--bg); color: var(--primary); overflow: hidden; position: relative; padding: 64px 72px; display: flex; flex-direction: column; }
.card { background: var(--bg-elevated); border: 1px solid var(--border); border-radius: 12px; padding: 28px; }
.card-accent { border-left: 3px solid var(--accent); }
.eyebrow { font-family: var(--font-num); font-size: var(--fs-label); font-weight: 500; color: var(--accent); text-transform: uppercase; letter-spacing: 0.08em; }
.footer { position: absolute; bottom: 28px; left: 72px; right: 72px; display: flex; justify-content: space-between; ... }
.tag { display: inline-flex; align-items: center; gap: 6px; padding: 4px 10px; background: var(--accent-soft); border: 1px solid rgba(88, 166, 255, 0.3); border-radius: 6px; font-family: var(--font-num); font-size: var(--fs-micro); color: var(--accent); font-weight: 500; }
.mono { font-family: var(--font-num); font-feature-settings: 'tnum' 1; }
.accent { color: var(--accent); }
.muted { color: var(--primary-muted); }
.subtle { color: var(--primary-subtle); }
.accent-dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: var(--accent); box-shadow: 0 0 12px var(--accent-glow); }
.grid-bg { background-image: linear-gradient(rgba(88, 166, 255, 0.04) 1px, transparent 1px), linear-gradient(90deg, rgba(88, 166, 255, 0.04) 1px, transparent 1px); background-size: 48px 48px; }
```

### 5. Avoid Tailwind class collisions

When the slide loads Tailwind via CDN, Tailwind injects its utilities into `<head>` AFTER your `<link rel="stylesheet">`. Custom classes sharing a name with a Tailwind utility lose the cascade.

**Critical collisions to avoid:**
- `.h-1`, `.h-2`, `.h-3` — Tailwind height utilities (4px / 8px / 12px). Applied to a heading, the box collapses to a few pixels.
- `.hidden` — Tailwind `display: none`. We USE this for speaker notes (`<aside data-notes class="hidden">`), so don't redefine it.
- `.block`, `.flex`, `.grid` — Tailwind display utilities.
- `.container` — Tailwind max-width utility.

### 6. Keep under ~150 lines

Per-slide layout CSS lives in each slide's HTML via inline styles or a `<style>` block. `global.css` ships ONLY tokens + utilities.

---

## Writing `slides_brief.json`

### Full schema

```json
{
  "design": {
    "title": "(ppt title — appears in .pptx metadata)",
    "style_name": "Linear Changelog Dark",
    "palette": {"background": "#0D1117", "primary": "#E6EDF3", "accent": "#58A6FF"},
    "typography": {"heading": "Inter", "body": "Inter", "numeric": "JetBrains Mono"},
    "reference": "Linear.app changelog pages"
  },
  "global_css_path": "/home/z/my-project/download/slides/global.css",
  "slides_dir": "/home/z/my-project/download/slides",
  "language": "en",
  "speaker_notes": "short",
  "slides": [
    {
      "title": "Cover — my-pi-agent",
      "layout": "cover",
      "output_path": "/home/z/my-project/download/slides/slide_01.html",
      "task_brief": "..."
    }
  ]
}
```

### Field rules

| Field | Rule |
|-------|------|
| `global_css_path` | ABSOLUTE path. Never relative. |
| `slides_dir` | ABSOLUTE path. Never relative. |
| `language` | `en` / `zh` / `bilingual` — determines speaker-note language. |
| `speaker_notes` | `none` / `short` / `full` — applies to ALL slides uniformly. |
| `slides[].output_path` | ABSOLUTE path. Filenames sort alphabetically into list order for Stage 5 export. |
| `slides[].layout` | One of the 12 patterns from `layout-catalog.md`. |
| `slides[].task_brief` | Self-contained — see rules below. |

### `task_brief` rules (CRITICAL)

The sub-agent sees ONLY the `task_brief`. It has no access to:
- The conversation history
- Other slides' briefs
- Image search results
- The design block (it's in `slides_brief.json.design`, not in the brief)

Therefore the brief MUST:

1. **Restate every text element verbatim** — headline, body, bullets, stats, quotes, tag pills, footer text. Copy-paste, don't paraphrase.
2. **Specify layout structure** — "left 55% for title block, right 45% for 3 stat cards stacked with 16px gap". Give the sub-agent a concrete grid to implement.
3. **Inline every image URL** from `z-ai image-search` results as a full `https://...` URL. If a slide has no image, simply don't mention images.
4. **Specify font sizes** for hero elements — "massive '195' in JetBrains Mono 700, ~280px, color var(--accent), with text-shadow 0 0 60px var(--accent-glow)".
5. **No meta-reminders** — don't repeat "diversify layouts" or "verify contrast" per slide. Those live once in the sub-agent dispatch prompt.
6. **Speaker notes hint** — if `speaker_notes` is `short`/`full`, append at the end: `Speaker notes: short hints — '<guidance on what to emphasize>'`. The sub-agent generates the actual notes.

### Brief example (from the reference build)

```
COVER SLIDE. Linear-style dark cover with subtle accent grid background (use the .grid-bg utility from global.css).

Content (render verbatim):
- Top-left eyebrow: 'GITHUB REPO · nordeim/my-pi-agent' (use .eyebrow class, with a leading .accent-dot)
- Center-left massive title: 'my-pi-agent' in Inter 800, ~120px, color var(--primary)
- Immediately below title, tagline in Inter 500, ~28px, color var(--primary-muted): '195 skills. 12 extensions. 1 opinionated Pi bundle.'
- Below tagline, a row of 3 .tag pills: 'Pi Agent customization', 'MIT-licensed skills', 'Load-on-demand'
- Bottom-left footer (use .footer class): left side 'github.com/nordeim/my-pi-agent' in mono; right side 'v2026.07 · main branch' in mono
- Right side of slide: a vertical stack of 3 monospace stat blocks (each in a .card .card-accent surface, ~280px wide), stacked with 16px gap. Each card shows a big mono number and a small muted label below:
  Card 1: '195' (72px, accent color) / 'skills'
  Card 2: '12' (72px, accent color) / 'extensions'
  Card 3: '10' (72px, accent color) / 'categories'

Layout: left 55% for title block, right 45% for the 3 stat cards. Vertically center both columns. No images.

Speaker notes: short hints — 'Open with the repo name and the three big numbers. Emphasize this is a customization bundle for Pi Agent, not a standalone app. Mention the 195 skills load on-demand.'
```

---

## Choosing layouts

**Load `layout-catalog.md` for the full 12-pattern catalog.** Quick selection guide:

| Slide purpose | Layout |
|---------------|--------|
| Slide 1 — title + tagline | `cover` |
| One massive stat | `stat_block` |
| Component overview (3-4 equal items) | `bento_grid` |
| Dense category map (8-10 items) | `stats_grid` |
| Chapter break | `section_divider` |
| Item list + "why it matters" | `split_text_features` |
| 3 variants compared | `comparison_card` |
| 3 categories with tag clouds | `three_column_spotlight` |
| N-step pipeline | `timeline` |
| Setup instructions with code | `step_guide` |
| Final CTA | `closing` |

**Diversify across consecutive slides.** Never repeat the same layout back-to-back. A 12-slide deck should use 8+ distinct layouts.

---

## Section structure for long decks

For decks ≥10 slides, split the body into 2-5 named chapters with a `section_divider` page at the start of each.

- 3-6 content pages per chapter
- If a stretch goes past 7 pages without a break, add another section divider
- Section-divider `task_brief` carries: chapter number ("01 / 03"), chapter title, one short tagline. No body bullets, no images.

For 8-slide decks, only add a section divider if the content has a strong narrative break.

---

## Anti-patterns

### Anti-pattern: relative paths in slides_brief.json
Sub-agents receive paths as strings. If `global_css_path` is `global.css`, the sub-agent may resolve it against its own cwd. Always use absolute paths.

### Anti-pattern: paraphrasing slide content in the brief
"Make a slide about the 10 categories" is a failure. The sub-agent will invent the category names. Restate verbatim: "5×2 grid of small category cards. Row 1: 1. mono '30' / 'Frontend & UI' / 'React 19, Next.js 16...'; 2. mono '11' / ..."

### Anti-pattern: meta-reminders per slide
"Remember to diversify layouts and verify WCAG AA contrast" repeated in every brief is noise. Put those reminders ONCE in the sub-agent dispatch prompt.

### Anti-pattern: shipping pre-baked typography classes
`.h-1`, `.h-display`, `.cn-sub` etc. in global.css cause cascade conflicts with Tailwind. Define tokens only; let sub-agents apply per-slide inline styles.

### Anti-pattern: writing slides_brief.json without absolute output_paths
`output_path: "slide_01.html"` will break — the sub-agent writes to its cwd, not the slides/ directory. Always `output_path: "/home/z/my-project/download/slides/slide_01.html"`.

---

## Output of Stage 3

Two files on disk:
- `<work_dir>/slides/global.css`
- `<work_dir>/slides/slides_brief.json`

Both with absolute paths, valid JSON, and self-contained briefs.

Proceed to Stage 4: BUILD.
