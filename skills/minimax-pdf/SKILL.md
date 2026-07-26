---
name: minimax-pdf
description: >
  Use this skill when visual quality and design identity matter for a PDF.
  CREATE (generate from scratch): "make a PDF", "generate a report", "write a proposal",
  "create a resume", "beautiful PDF", "professional document", "cover page",
  "polished PDF", "client-ready document".
  FILL (complete form fields): "fill in the form", "fill out this PDF",
  "complete the form fields", "write values into PDF", "what fields does this PDF have".
  REFORMAT (apply design to an existing doc): "reformat this document", "apply our style",
  "convert this Markdown/text to PDF", "make this doc look good", "re-style this PDF".
  This skill uses a token-based design system: color, typography, and spacing are derived
  from the document type and flow through every page. The output is print-ready.
  Prefer this skill when appearance matters, not just when any PDF output is needed.
license: MIT
metadata:
  version: "1.0"
  category: document-generation
---

# minimax-pdf

Three tasks. One skill.

## Read `design/design.md` before any CREATE or REFORMAT work.

---

## Route table

| User intent | Route | Scripts used |
|---|---|---|
| Generate a new PDF from scratch | **CREATE** | `palette.py` → `cover.py` → `render_cover.js` → `render_body.py` → `merge.py` |
| Fill / complete form fields in an existing PDF | **FILL** | `fill_inspect.py` → `fill_write.py` |
| Reformat / re-style an existing document | **REFORMAT** | `reformat_parse.py` → then full CREATE pipeline |

**Rule:** when in doubt between CREATE and REFORMAT, ask whether the user has an existing document to start from. If yes → REFORMAT. If no → CREATE.

---

## Route A: CREATE

Full pipeline — content → design tokens → cover → body → merged PDF.

```bash
bash scripts/make.sh run \
  --title "Q3 Strategy Review" --type proposal \
  --author "Strategy Team" --date "October 2025" \
  --accent "#2D5F8A" \
  --content content.json --out report.pdf
```

**Doc types:** `report` · `proposal` · `resume` · `portfolio` · `academic` · `general` · `minimal` · `stripe` · `diagonal` · `frame` · `editorial` · `magazine` · `darkroom` · `terminal` · `poster`

| Type | Cover pattern | Visual identity |
|---|---|---|
| `report` | `fullbleed` | Dark bg, dot grid, Playfair Display |
| `proposal` | `split` | Left panel + right geometric, Syne |
| `resume` | `typographic` | Oversized first-word, DM Serif Display |
| `portfolio` | `atmospheric` | Near-black, radial glow, Fraunces |
| `academic` | `typographic` | Light bg, classical serif, EB Garamond |
| `general` | `fullbleed` | Dark slate, Outfit |
| `minimal` | `minimal` | White + single 8px accent bar, Cormorant Garamond |
| `stripe` | `stripe` | 3 bold horizontal color bands, Barlow Condensed |
| `diagonal` | `diagonal` | SVG angled cut, dark/light halves, Montserrat |
| `frame` | `frame` | Inset border, corner ornaments, Cormorant |
| `editorial` | `editorial` | Ghost letter, all-caps title, Bebas Neue |
| `magazine` | `magazine` | Warm cream bg, centered stack, hero image, Playfair Display |
| `darkroom` | `darkroom` | Navy bg, centered stack, grayscale image, Playfair Display |
| `terminal` | `terminal` | Near-black, grid lines, monospace, neon green |
| `poster` | `poster` | White bg, thick sidebar, oversized title, Barlow Condensed |

Cover extras (inject into tokens via `--abstract`, `--cover-image`):
- `--abstract "text"` — abstract text block on the cover (magazine/darkroom)
- `--cover-image "url"` — hero image URL/path (magazine, darkroom, poster)

**Color overrides — always choose these based on document content:**
- `--accent "#HEX"` — override the accent color; `accent_lt` is auto-derived by lightening toward white
- `--cover-bg "#HEX"` — override the cover background color

**Accent color selection guidance:**

You have creative authority over the accent color. Pick it from the document's semantic context — title, industry, purpose, audience — not from generic "safe" choices. The accent appears on section rules, callout bars, table headers, and the cover: it carries the document's visual identity.

| Context | Suggested accent range |
|---|---|
| Legal / compliance / finance | Deep navy `#1C3A5E`, charcoal `#2E3440`, slate `#3D4C5E` |
| Healthcare / medical | Teal-green `#2A6B5A`, cool green `#3A7D6A` |
| Technology / engineering | Steel blue `#2D5F8A`, indigo `#3D4F8A` |
| Environmental / sustainability | Forest `#2E5E3A`, olive `#4A5E2A` |
| Creative / arts / culture | Burgundy `#6B2A35`, plum `#5A2A6B`, terracotta `#8A3A2A` |
| Academic / research | Deep teal `#2A5A6B`, library blue `#2A4A6B` |
| Corporate / neutral | Slate `#3D4A5A`, graphite `#444C56` |
| Luxury / premium | Warm black `#1A1208`, deep bronze `#4A3820` |

**Rule:** choose a color that a thoughtful designer would select for this specific document — not the type's default. Muted, desaturated tones work best; avoid vivid primaries. When in doubt, go darker and more neutral.

**content.json block types:**

| Block | Usage | Key fields |
|---|---|---|
| `h1` | Section heading + accent rule | `text` |
| `h2` | Subsection heading | `text` |
| `h3` | Sub-subsection (bold) | `text` |
| `body` | Justified paragraph; supports `<b>` `<i>` markup | `text` |
| `bullet` | Unordered list item (• prefix) | `text` |
| `numbered` | Ordered list item — counter auto-resets on non-numbered blocks | `text` |
| `callout` | Highlighted insight box with accent left bar | `text` |
| `table` | Data table — accent header, alternating row tints | `headers`, `rows`, `col_widths`?, `caption`? |
| `image` | Embedded image scaled to column width | `path`/`src`, `caption`? |
| `figure` | Image with auto-numbered "Figure N:" caption | `path`/`src`, `caption`? |
| `code` | Monospace code block with accent left border | `text`, `language`? |
| `math` | Display math — LaTeX syntax via matplotlib mathtext | `text`, `label`?, `caption`? |
| `chart` | Bar / line / pie chart rendered with matplotlib | `chart_type`, `labels`, `datasets`, `title`?, `x_label`?, `y_label`?, `caption`?, `figure`? |
| `flowchart` | Process diagram with nodes + edges via matplotlib | `nodes`, `edges`, `caption`?, `figure`? |
| `bibliography` | Numbered reference list with hanging indent | `items` [{id, text}], `title`? |
| `divider` | Accent-colored full-width rule | — |
| `caption` | Small muted label | `text` |
| `pagebreak` | Force a new page | — |
| `spacer` | Vertical whitespace | `pt` (default 12) |

**chart / flowchart schemas:**
```json
{"type":"chart","chart_type":"bar","labels":["Q1","Q2","Q3","Q4"],
 "datasets":[{"label":"Revenue","values":[120,145,132,178]}],"caption":"Q results"}

{"type":"flowchart",
 "nodes":[{"id":"s","label":"Start","shape":"oval"},
          {"id":"p","label":"Process","shape":"rect"},
          {"id":"d","label":"Valid?","shape":"diamond"},
          {"id":"e","label":"End","shape":"oval"}],
 "edges":[{"from":"s","to":"p"},{"from":"p","to":"d"},
          {"from":"d","to":"e","label":"Yes"},{"from":"d","to":"p","label":"No"}]}

{"type":"bibliography","items":[
  {"id":"1","text":"Author (Year). Title. Publisher."}]}
```

---

## Route B: FILL

Fill form fields in an existing PDF without altering layout or design.

```bash
# Step 1: inspect
python3 scripts/fill_inspect.py --input form.pdf

# Step 2: fill
python3 scripts/fill_write.py --input form.pdf --out filled.pdf \
  --values '{"FirstName": "Jane", "Agree": "true", "Country": "US"}'
```

| Field type | Value format |
|---|---|
| `text` | Any string |
| `checkbox` | `"true"` or `"false"` |
| `dropdown` | Must match a choice value from inspect output |
| `radio` | Must match a radio value (often starts with `/`) |

Always run `fill_inspect.py` first to get exact field names.

---

## Route C: REFORMAT

Parse an existing document → content.json → CREATE pipeline.

```bash
bash scripts/make.sh reformat \
  --input source.md --title "My Report" --type report --out output.pdf
```

**Supported input formats:** `.md` `.txt` `.pdf` `.json`

---

## Environment

```bash
bash scripts/make.sh check   # verify all deps
bash scripts/make.sh fix     # auto-install missing deps
bash scripts/make.sh demo    # build a sample PDF
```

| Tool | Used by | Install |
|---|---|---|
| Python 3.9+ | all `.py` scripts | system |
| `reportlab` | `render_body.py` | `pip install reportlab` |
| `pypdf` | fill, merge, reformat | `pip install pypdf` |
| Node.js 18+ | `render_cover.js` | system |
| `playwright` + Chromium | `render_cover.js` | `npm install -g playwright && npx playwright install chromium` |

---

## Cross-References & Best Practices

### Related skills

| Skill | When to prefer it |
|---|---|
| [`../pdf/`](../pdf/SKILL.md) | Canonical Z.AI PDF skill — four production lines (Report via ReportLab, Creative via JSON Blueprint + Playwright, Academic via Tectonic/LaTeX, Process for manipulate-existing). Use when you need LaTeX academic typesetting, the JSON Blueprint creative pipeline, or `pdf_qa.py` 12-rule automated QA. |
| [`../kimi-pdf/`](../kimi-pdf/SKILL.md) | Kimi (Moonshot AI) HTML+Paged.js (default) or LaTeX/Tectonic PDF pipeline with 11 cover styles, KaTeX math, Mermaid diagrams, three-line tables (三线表), GB/T 7714 + APA citation standards with per-language split, clickable cross-references, and search-before-write enforcement. Use when you want HTML-first pagination, academic three-line tables, or the unified `pdf.sh` CLI. |
| [`../resume-builder/`](../resume-builder/SKILL.md) | Resume-specific PDF generation with ATS keyword checks. |
| [`../charts/`](../charts/SKILL.md) | Standalone chart/diagram generation when the PDF is just a chart carrier. |

### Best practices cross-pollinated from the canonical `pdf` skill

These rules are universal to PDF production regardless of pipeline. Apply them on top of the route-specific guidance above.

**Pre-routing checks (run BEFORE matching route)**
1. **Emoji check** — Scan user content for intentional emoji (📊🎯🔥, not OS-level input). If found, force Creative pipeline (Playwright); ReportLab renders emoji as `□` squares and LaTeX drops them entirely.
2. **CJK check** — Chinese/Japanese/Korean content needs explicit font coverage. Probe with `ls /usr/share/fonts/truetype/chinese/` (Linux) before registering; prefer Noto Serif SC > Noto Sans SC. Never hardcode a font name without verifying it exists.
3. **Size check** — Non-standard page sizes (not A4/Letter/A3) → prefer Playwright (handles any dimension natively); ReportLab requires manual pagination math.
4. **Character safety check** — Scan content strings for Japanese kana (の、が、は) or unusual Unicode that may corrupt during heredoc/base64/LLM transit. Replace with plain CJK equivalents unless Japanese is required.

**Vector rendering iron rule**
The final PDF MUST be generated via `page.pdf()` (Playwright) or ReportLab/LaTeX native output — NEVER via screenshot-to-PDF. Screenshot PDFs are raster, blurry when zoomed, unsearchable, and 3–5× larger. The ONLY acceptable screenshot use is for diagrams/charts embedded as sub-elements inside a larger vector document.

**HTML→PDF engine selection**
- **Posters / single-page long-image / cover pages** → `html2poster.js` (auto `overflow:hidden`, dynamic height, zero margin).
- **Multi-page documents / reports / academic** → `html2pdf-next.js` (Paged.js pagination, A4/custom size, pdf-lib metadata).
- **Cover pages use absolute positioning** — ALWAYS use `html2poster.js`. `html2pdf-next.js` + Paged.js would re-layout absolute-positioned elements into flow and destroy the cover.

**Full-bleed rule (no white margins)**
Mandatory CSS for any HTML→PDF:
```css
@page { size: <width> <height>; margin: 0; }
html, body { margin: 0; padding: 0; }
```
Common white-margin causes: missing `@page { margin: 0 }`, content width ≠ page width, missing `@page { size }`, content `max-width` narrower than page.

**Background color consistency**
`html` / `body` background MUST match the content canvas background. For multi-page docs with mixed dark/light pages, set `html, body { background }` to the darkest page's background so sub-pixel gaps at page edges stay invisible.

**No `overflow: hidden` on fixed-size pages**
Never set `overflow: hidden` on `html`, `body`, `.page`, or the main content container — it silently clips content that exceeds bounds and hides layout bugs. Paged.js handles pagination natively. (Exception: posters rendered via `html2poster.js` — that script auto-adds it to clip decorative overflow.)

**Figures are block-level**
Figures, diagrams, charts MUST be independent block elements at full width. NEVER float/wrap figures alongside body text — it causes text-diagram overlap. In ReportLab: `story.append(Image(...))` as standalone Flowable. In Playwright: `<figure style="display:block; width:100%; margin:2em auto">`.

**Table overflow prevention (ReportLab)**
Before building any `Table`: (1) calculate `available_width = page_width - left_margin - right_margin`, (2) use proportional `colWidths` summing to ≤ `available_width`, (3) long-text columns MUST use `Paragraph()` wrapping (plain strings don't wrap), (4) CJK text is wider — budget ~12pt per character at 10pt font size.

**Quality checklist (mandatory after every PDF)**
- Run `pdf_qa.py` — auto-detects metadata completeness, page size consistency, blank pages, CJK punctuation, color count, font embedding, content overflow, fill ratio, cover full-bleed, margin symmetry, table centering, formula overflow. PASS → deliver; WARN → evaluate; FAIL → must fix and regenerate.
- For HTML→PDF paths, also run `poster_validate.py check-html <file>.html` BEFORE rendering — catches `overflow:hidden` containers, missing font fallbacks, contrast issues, background mismatches.
- **Output cleanliness**: NEVER include version numbers, "DRAFT"/"CONFIDENTIAL" stamps, "Generated by AI", or any watermark the user didn't ask for. PDF metadata should reflect document content, not the generation process.
