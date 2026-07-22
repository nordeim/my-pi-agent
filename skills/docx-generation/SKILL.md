---
name: docx-generation
description: Comprehensive DOCX Generation & Conversion Skill
version: 1.0
---

# Comprehensive DOCX Generation & Conversion Skill

## Purpose

This skill enables **bidirectional conversion between Markdown and DOCX** with professional-quality output. It encodes all knowledge from the Z.AI docx skill system (design system, common rules, cover recipes, post-check scripts, TOC handling) plus practical patterns proven in real document generation (the Consolidated Remediation Plan Report 5).

**Core capabilities:**
1. **Markdown → DOCX**: Parse a Markdown file and generate a professionally formatted .docx with cover page, TOC, styled headings, tables, and proper typography
2. **DOCX → Markdown**: Extract structured content from a .docx file into clean Markdown with metadata preservation
3. **Standalone DOCX generation**: Build documents programmatically using the `docx` npm package with all design-system rules enforced

---

## Table of Contents

1. [Dependencies & Setup](#1-dependencies--setup)
2. [Architecture Overview](#2-architecture-overview)
3. [Markdown → DOCX Conversion](#3-markdown--docx-conversion)
4. [DOCX → Markdown Conversion](#4-docx--markdown-conversion)
5. [Design System Reference](#5-design-system-reference)
6. [Common Formatting Rules](#6-common-formatting-rules)
7. [Cover Page System](#7-cover-page-system)
8. [Table of Contents (TOC)](#8-table-of-contents-toc)
9. [Table Styling](#9-table-styling)
10. [Post-Generation Verification](#10-post-generation-verification)
11. [Source Scripts Reference](#11-source-scripts-reference)
12. [Known Pitfalls & Solutions](#12-known-pitfalls--solutions)

---

## 1. Dependencies & Setup

### Required Packages

```bash
# Node.js (primary generation engine)
npm install docx image-size

# Python (post-processing, TOC, validation)
pip install python-docx lxml Pillow

# System tools (optional, for PDF conversion)
# LibreOffice, Poppler (pdftoppm), pandoc
```

### Script Paths

All post-processing scripts are located in the Z.AI docx skill directory:

```bash
DOCX_SKILL_DIR="/home/z/my-project/skills/docx"
DOCX_SCRIPTS="$DOCX_SKILL_DIR/scripts"

# Post-check validation
python3 "$DOCX_SCRIPTS/postcheck.py" output.docx

# TOC placeholder injection
python3 "$DOCX_SCRIPTS/add_toc_placeholders.py" output.docx --auto
```

### Source Skill Files

| File | Purpose |
|------|---------|
| `skills/docx/SKILL.md` | Main skill entry point, task router, post-generation checklist |
| `skills/docx/routes/create.md` | Create-route workflow, cover recipe router, outline rules |
| `skills/docx/references/design-system.md` | Color palettes, cover recipes R1-R7, table styles, font specs |
| `skills/docx/references/common-rules.md` | Page layout, font profiles, WPS/Office compatibility, prohibitions |
| `skills/docx/references/docx-js-core.md` | docx npm package API reference |
| `skills/docx/references/docx-js-advanced.md` | TOC, footnotes, multi-section, quotes escaping |
| `skills/docx/references/toc.md` | TOC 3-step process, page numbering, common bugs |
| `skills/docx/scripts/postcheck.py` | 14-rule automated document validation |
| `skills/docx/scripts/add_toc_placeholders.py` | TOC bookmark injection and placeholder generation |

---

## 2. Architecture Overview

### Document Structure (3-Section Pattern)

```
┌─────────────────────────────────┐
│ Section 1: Cover Page           │  ← margin: 0, no page numbers
│ (16838 twips exact-height table) │
├─────────────────────────────────┤
│ Section 2: TOC + Body Content   │  ← normal margins, page numbers start at 1
│ (Headings, paragraphs, tables)  │
└─────────────────────────────────┘
```

### Core Builder Pattern

```javascript
const { Document, Packer, Paragraph, TextRun, Header, Footer,
        AlignmentType, HeadingLevel, PageNumber, Table, TableRow, TableCell,
        WidthType, BorderStyle, ShadingType, TableOfContents, PageBreak,
        SectionType } = require("docx");
const fs = require("fs");

// 1. Palette selection (see Section 5)
const P = { primary: "#0A1628", body: "#1A2B40", secondary: "#6878A0", accent: "#5B8DB8", surface: "#F4F8FC" };
const c = (hex) => hex.replace("#", "");

// 2. Component builders (see Section 6)
function h1(text) { /* ... */ }
function h2(text) { /* ... */ }
function h3(text) { /* ... */ }
function body(text) { /* ... */ }
function bullet(text) { /* ... */ }

// 3. Document assembly
const doc = new Document({
  styles: { default: { document: {
    run: { font: { ascii: "Times New Roman", eastAsia: "SimSun" }, size: 24, color: c(P.body) },
    paragraph: { spacing: { line: 312 } },
  }}},
  sections: [
    { properties: { page: { margin: { top: 0, bottom: 0, left: 0, right: 0 } } },
      children: buildCover(config) },
    { properties: { page: { margin: { top: 1440, bottom: 1440, left: 1701, right: 1417 },
        pageNumbers: { start: 1 } } },
      footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER,
        children: [new TextRun({ children: [PageNumber.CURRENT], size: 18, color: c(P.secondary) })] })] }) },
      children: bodyChildren },
  ],
});

// 4. Generate and post-process
const OUTPUT = "/path/to/output.docx";
Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(OUTPUT, buf);
  // Then run: postcheck.py and add_toc_placeholders.py
});
```

---

## 3. Markdown → DOCX Conversion

### Markdown Parser Specification

The converter maps Markdown elements to docx-js components as follows:

| Markdown Element | docx-js Component | Notes |
|-----------------|-------------------|-------|
| `# H1` | `Paragraph({ heading: HeadingLevel.HEADING_1 })` | Size 32, bold, primary color |
| `## H2` | `Paragraph({ heading: HeadingLevel.HEADING_2 })` | Size 30, bold, primary color |
| `### H3` | `Paragraph({ heading: HeadingLevel.HEADING_3 })` | Size 28, bold, primary color |
| Plain paragraph | `Paragraph({ alignment: JUSTIFIED, indent: { firstLine: 480 }, spacing: { line: 312 } })` | 12pt body |
| `**bold**` | `TextRun({ bold: true })` | Inline within paragraph |
| `*italic*` | `TextRun({ italics: true })` | Inline within paragraph |
| `` `code` `` | `TextRun({ font: { ascii: "Courier New" }, size: 21 })` | Monospace, smaller |
| `- bullet` | `Paragraph({ indent: { left: 480 } })` | With bullet character |
| `> blockquote` | `Paragraph({ indent: { left: 720 }, border: { left: ... } })` | Left border accent |
| `---` (hr) | `Paragraph({ border: { bottom: { style: SINGLE, size: 2, color: accent } } })` | Accent line |
| Table (pipe) | `Table({ width: { size: 100, type: PERCENTAGE } })` | See Section 9 |
| `[link](url)` | `ExternalHyperlink({ children: [...], link: url })` | Blue, underlined |
| `![alt](path)` | `ImageRun({ data, transformation, type })` | Preserve aspect ratio |
| `1. ordered` | `Paragraph({ numbering: { reference: "ordered-list" } })` | Unique reference per list |

### Conversion Algorithm

```
INPUT:  Markdown file (.md)
OUTPUT: DOCX file (.docx)

1. Parse Markdown into AST (headings, paragraphs, lists, tables, code blocks, etc.)
2. Extract frontmatter metadata (title, subtitle, date, author) → cover config
3. Determine palette from content domain (tech, academic, business, etc.)
4. Build cover page section (see Section 7)
5. Convert AST nodes to docx-js components:
   - Headings → HeadingLevel paragraphs
   - Paragraphs → justified body text with CJK indent
   - Tables → docx Table with header row styling
   - Lists → bulleted/numbered paragraphs
   - Code blocks → monospace font, shaded background
   - Images → ImageRun with aspect ratio preservation
6. Add TOC if ≥3 H1 headings
7. Add headers/footers with page numbers
8. Assemble Document with sections
9. Run Packer.toBuffer() → write file
10. Run postcheck.py → fix errors
11. Run add_toc_placeholders.py → inject TOC bookmarks
```

### Key Conversion Rules

1. **CJK text detection**: If text contains CJK Unicode ranges (`\u4e00-\u9fff`), apply justified alignment + 480-twip first-line indent. English text: left-aligned, no indent.
2. **Table header detection**: First row of Markdown pipe table → styled as header row (accent background, white text, bold).
3. **Code blocks**: Wrap in single-cell table with monospace font and light grey background.
4. **Image handling**: Use `image-size` package to read dimensions, calculate display height proportionally. Never hardcode both width and height.
5. **Frontmatter**: YAML frontmatter maps to cover config: `title`, `subtitle`, `date`, `author`, `palette` (optional override).

---

## 4. DOCX → Markdown Conversion

### Extraction Algorithm

```
INPUT:  DOCX file (.docx)
OUTPUT: Markdown file (.md)

1. Unzip .docx → read word/document.xml
2. Parse paragraphs sequentially:
   - Heading1-6 → # / ## / ### / etc.
   - Body paragraphs → plain text (detect bold/italic runs)
   - Tables → pipe-delimited Markdown tables
   - Bullet lists → - item
   - Numbered lists → 1. item
   - Images → ![alt](extracted_path) + extract to output dir
3. Extract metadata from document properties or first-section cover
4. Generate YAML frontmatter from metadata
5. Write clean Markdown with consistent formatting
```

### Extraction Rules

1. **Run-level formatting**: Check `w:rPr` for `w:b` (bold) → `**text**`, `w:i` (italic) → `*text*`, `w:u` (underline) → skip in MD.
2. **Table extraction**: Parse `w:tbl` → build 2D array → format as pipe table with `|---|` separator row.
3. **Image extraction**: Read relationship IDs → extract binary from zip → save to `images/` directory.
4. **TOC sections**: Skip TOC field content (regenerate from headings).
5. **Section breaks**: Insert `---` horizontal rules between major sections.

---

## 5. Design System Reference

### Color Palettes (Mood-Driven)

Select palette based on document domain:

| Domain | Palette Name | Colors |
|--------|-------------|--------|
| Tech / Digital | Dawn Mist Tech | `primary: #0A1628, body: #1A2B40, secondary: #6878A0, accent: #5B8DB8, surface: #F4F8FC` |
| Academic / Research | Deep Sea Academic | `primary: #162032, body: #1C2A3D, secondary: #5B6B7D, accent: #8B7E5A, surface: #F5F7FA` |
| Legal / Compliance | Legal Wood | `primary: #28201C, body: #36302C, secondary: #6E6560, accent: #7A5C3A, surface: #FBF9F7` |
| General Business | Plain Paper | `primary: #101820, body: #182030, secondary: #506070, accent: #8090A0, surface: #F2F4F6` |
| Consulting | Terracotta | `primary: #241E1A, body: #3A3430, secondary: #68605A, accent: #B08050, surface: #FDFBF9` |
| Medical | Mint Medical | `primary: #0E2030, body: #1E2E40, secondary: #4A6580, accent: #3888A8, surface: #F0F6FA` |
| Minimalist | White Porcelain | `primary: #303030, body: #484848, secondary: #808080, accent: #B89870, surface: #FAFAF8` |
| AI / Innovation | Lapis Tech | `primary: #1A1F36, body: #000000, secondary: #5A6080, accent: #667eea, surface: #F8F9FF` |
| Finance / Premium | Deep Blue-Gold | `primary: #0F2027, body: #000000, secondary: #4A6575, accent: #D4AF37, surface: #F5F7FA` |

### Cover Palettes (for cover backgrounds)

| ID | Name | Background | Use Case |
|----|------|-----------|----------|
| DS-1 | Deep Sea | `#0B1C2C` | Annual reports, general business |
| IG-1 | Ink Gold | `#1A1A1A` | Finance, luxury |
| DM-1 | Deep Cyan | `#162235` | AI, tech proposals |
| FG-1 | Forest Mint | `#0C1F1A` | ESG, sustainability |
| GO-1 | Graphite Orange | `#1A2330` | Proposals, PRD |
| CM-2 | Blue Orange | `#FEFEFE` (light) | Tech, corporate, whitepaper |
| MIN-1 | Warm Gold | `#F3F1ED` (light) | Consulting, minimalist |
| WM-1 | Warm Teal | `#F4F1E9` (light) | Education, training |
| ACADEMIC | Pure Black | `#FFFFFF` | Thesis, standards |

### Font Specifications

**English documents:**

| Element | Font | Size (half-points) |
|---------|------|-------------------|
| Headings | Times New Roman Bold | H1: 32, H2: 30, H3: 28 |
| Body | Times New Roman | 24 (12pt) |
| Captions | Times New Roman | 21 (10.5pt) |

**Chinese documents:**

| Element | Font | Size |
|---------|------|------|
| Headings | SimHei | H1: 32, H2: 30, H3: 28 |
| Body | SimSun (Formal) / Microsoft YaHei (Visual) | 24 (12pt) |

**Monospace:** IBM Plex Mono, Courier New — for code blocks and technical content.

---

## 6. Common Formatting Rules

### Page Layout (A4)

```javascript
const PAGE = {
  width: 11906,   // 21.0 cm
  height: 16838,  // 29.7 cm
  margin: { top: 1440, bottom: 1440, left: 1701, right: 1417 },
  // top/bottom: 2.54cm, left: 3.0cm, right: 2.5cm
};
```

### Line Spacing

**1.3x (`line: 312`) is MANDATORY** for all body text. No exceptions unless a scene explicitly overrides.

### First-Line Indent

- **Profile A (Formal)**: `firstLine: 480` (2 chars at SimSun 12pt) — for reports, academic, contracts
- **Profile B (Visual)**: `firstLine: 420` (2 chars at YaHei) — for resumes, copywriting
- **English text**: No first-line indent. Left-aligned.

### Component Builders (Proven Pattern)

```javascript
// Color helper
const c = (hex) => hex.replace("#", "");

// Severity/status color helpers
function severityColor(sev) {
  const map = { CRITICAL: "#CC0000", HIGH: "#E67300", MODERATE: "#D4A030", LOW: "#8090A0" };
  return map[sev] || "#8090A0";
}

// Heading builders
function h1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 360, after: 120 },
    children: [new TextRun({ text, bold: true, color: c(P.primary),
      font: { ascii: "Times New Roman", eastAsia: "SimHei" }, size: 32 })],
  });
}

function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 280, after: 100 },
    children: [new TextRun({ text, bold: true, color: c(P.primary),
      font: { ascii: "Times New Roman", eastAsia: "SimHei" }, size: 30 })],
  });
}

function h3(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_3,
    spacing: { before: 220, after: 80 },
    children: [new TextRun({ text, bold: true, color: c(P.primary),
      font: { ascii: "Times New Roman", eastAsia: "SimHei" }, size: 28 })],
  });
}

// Body text
function body(text) {
  return new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    spacing: { line: 312, after: 80 },
    children: [new TextRun({ text, size: 24, color: c(P.body),
      font: { ascii: "Times New Roman", eastAsia: "SimSun" } })],
  });
}

// Bold body text
function bodyBold(text) {
  return new Paragraph({
    spacing: { line: 312, after: 80 },
    children: [new TextRun({ text, size: 24, color: c(P.body), bold: true,
      font: { ascii: "Times New Roman", eastAsia: "SimHei" } })],
  });
}

// Body with mixed formatting (bold segments, colored segments)
function bodyRuns(runs) {
  return new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    spacing: { line: 312, after: 80 },
    children: runs.map(r => new TextRun({ size: 24, color: c(P.body),
      font: { ascii: "Times New Roman", eastAsia: "SimSun" }, ...r })),
  });
}

// Bullet point
function bullet(text, level = 0) {
  return new Paragraph({
    alignment: AlignmentType.LEFT,
    indent: { left: 480 + level * 240 },
    spacing: { line: 312, after: 60 },
    children: [new TextRun({ text: `\u2022 ${text}`, size: 24, color: c(P.body),
      font: { ascii: "Times New Roman", eastAsia: "SimSun" } })],
  });
}
```

### WPS/Office Compatibility Rules (CRITICAL)

| Rule | Why | How |
|------|-----|-----|
| Always use `ShadingType.CLEAR` | `SOLID` renders as black in WPS | Search code for "SOLID" and replace |
| Never use `verticalAlign: "center"` in exact-height rows | WPS ignores it | Use `spacing.before` instead |
| Cover wrapper must use `allNoBorders` | Default borders add ~8tw/edge → blank page 2 in MS Office | Define and use `allNoBorders` constant |
| Use `WidthType.PERCENTAGE` for table columns | DXA widths cause WPS tblGrid bug | Never use DXA for column widths |
| No text-character decorative lines (`───`) | Render inconsistently across engines | Use paragraph borders instead |
| Large fonts need explicit `spacing.line` | Inherited small line spacing clips characters | Set `line: fontPt * 23, lineRule: "atLeast"` |

---

## 7. Cover Page System

### Simplified Cover Builder (Non-Recipe)

For Markdown-to-DOCX conversion, use this proven cover pattern:

```javascript
function buildCover(config) {
  // config: { title, subtitle, metaLines: [{label, value}], palette }
  const P = config.palette;
  const children = [];

  // Top spacing
  children.push(new Paragraph({ spacing: { before: 3600 }, children: [] }));

  // Title
  children.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 200 },
    children: [new TextRun({ text: config.title, bold: true, color: c(P.primary),
      size: 52, font: { ascii: "Times New Roman", eastAsia: "SimHei" } })],
  }));

  // Subtitle
  if (config.subtitle) {
    children.push(new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 100 },
      children: [new TextRun({ text: config.subtitle, color: c(P.secondary), size: 28,
        font: { ascii: "Times New Roman", eastAsia: "SimHei" } })],
    }));
  }

  // Divider
  children.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 600 },
    children: [new TextRun({ text: "\u2500".repeat(40), color: c(P.accent), size: 24 })],
  }));

  // Meta lines
  (config.metaLines || []).forEach(({ label, value }) => {
    children.push(new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 80 },
      children: [
        new TextRun({ text: `${label}:  `, bold: true, color: c(P.primary), size: 22,
          font: { ascii: "Times New Roman", eastAsia: "SimHei" } }),
        new TextRun({ text: value, color: c(P.body), size: 22,
          font: { ascii: "Times New Roman", eastAsia: "SimSun" } }),
      ],
    }));
  });

  return children;
}
```

### Full Recipe System (R1-R7)

For production documents requiring exact visual fidelity, the source skill provides 7 validated cover recipes. See `skills/docx/references/design-system.md` for complete code. Quick reference:

| Recipe | Visual | Use Case |
|--------|--------|----------|
| R1 | Full-page dark bg, left-aligned text | Reports, proposals |
| R2 | Full-page dark bg, double-rule frame, centered | Whitepapers, finance |
| R3 | Full-page dark bg, centered card frame | Creative, branding |
| R4 | Top dark block + bottom white + accent divider | Proposals, plans |
| R5 | Pure white, academic meta table | Thesis, standards |
| R6 | Light editorial, warm tones | Lesson plans, cultural |
| R7 | Swiss minimalist, slate grey, Klein blue | Trend reports, research |

**Cover non-negotiables:**
1. Cover section margin MUST be `{ top: 0, bottom: 0, left: 0, right: 0 }`
2. Use 16838 exact-height wrapper table
3. Set `borders: allNoBorders` on wrapper table
4. Use `calcTitleLayout()` for dynamic font sizing
5. Use `calcCoverSpacing()` for dynamic spacing
6. No trailing PageBreak in cover section

---

## 8. Table of Contents (TOC)

### 3-Step TOC Process

**Step 1: Add TOC element in code**

```javascript
bodyChildren.push(new Paragraph({
  heading: HeadingLevel.HEADING_1,
  children: [new TextRun({ text: "Table of Contents", ... })],
}));
bodyChildren.push(new TableOfContents("Table of Contents", {
  hyperlink: true,
  headingStyleRange: "1-3",
}));
// MANDATORY: Refresh hint
bodyChildren.push(new Paragraph({
  spacing: { after: 120 },
  children: [new TextRun({ text: "Right-click the TOC and select \u201cUpdate Field\u201d to refresh page numbers.",
    italics: true, color: c(P.secondary), size: 20 })],
}));
// MANDATORY: PageBreak after TOC
bodyChildren.push(new Paragraph({ children: [new PageBreak()] }));
```

**Step 2: Run postcheck.py**

```bash
python3 "$DOCX_SCRIPTS/postcheck.py" output.docx
```

**Step 3: Run add_toc_placeholders.py**

```bash
python3 "$DOCX_SCRIPTS/add_toc_placeholders.py" output.docx --auto
```

### TOC Common Bugs

| Bug | Cause | Fix |
|-----|-------|-----|
| Empty TOC after Word update | Heading styles missing `outlineLvl` | Run `add_toc_placeholders.py` which fixes this |
| TOC and body on same page | Missing PageBreak after `TableOfContents` | Add `Paragraph({ children: [new PageBreak()] })` after TOC |
| Page numbers show "1decimal" | Used `\* decimal` in instrText | Use `\* arabic` instead |
| Word doesn't prompt TOC update | Missing `updateFields=true` in settings.xml | Run `add_toc_placeholders.py` |

---

## 9. Table Styling

### Proven Table Helper Pattern

```javascript
const CELL_MARGINS = { top: 40, bottom: 40, left: 80, right: 80 };
const TABLE_BORDER = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const BORDERS = { top: TABLE_BORDER, bottom: TABLE_BORDER, left: TABLE_BORDER, right: TABLE_BORDER };

function headerCell(text, widthPct) {
  return new TableCell({
    width: { size: widthPct, type: WidthType.PERCENTAGE },
    margins: CELL_MARGINS,
    shading: { fill: c(P.primary), type: ShadingType.CLEAR },
    borders: BORDERS,
    children: [new Paragraph({ alignment: AlignmentType.CENTER,
      children: [new TextRun({ text, bold: true, color: "FFFFFF", size: 20,
        font: { ascii: "Times New Roman", eastAsia: "SimHei" } })] })],
  });
}

function dataCell(text, widthPct, opts = {}) {
  const shade = opts.shade ? { fill: c(P.surface), type: ShadingType.CLEAR } : undefined;
  return new TableCell({
    width: { size: widthPct, type: WidthType.PERCENTAGE },
    margins: CELL_MARGINS,
    shading: shade,
    borders: BORDERS,
    children: [new Paragraph({
      alignment: opts.center ? AlignmentType.CENTER : AlignmentType.LEFT,
      children: [new TextRun({ text, size: 20, color: opts.color ? c(opts.color) : c(P.body),
        bold: opts.bold || false,
        font: { ascii: "Times New Roman", eastAsia: "SimSun" } })],
    })],
  });
}
```

### Table Style Selection

- **Formal (report, academic, contract)**: Horizontal-only borders, accent header row
- **Visual (resume, copywriting)**: Zebra stripe with surface color
- **Academic**: Three-line table (top, header-bottom, bottom only)

---

## 10. Post-Generation Verification

### Layer 1: Manual Checklist

- [ ] Line spacing is 1.3x (`line: 312`)
- [ ] CJK body has 2-char indent (`firstLine: 480`)
- [ ] Tables have margins set
- [ ] `ShadingType.CLEAR` used everywhere (never `SOLID`)
- [ ] Heading styles use `heading: HeadingLevel.HEADING_X`
- [ ] Cover section has `margin: { top: 0, bottom: 0, left: 0, right: 0 }`
- [ ] Cover wrapper uses `allNoBorders`
- [ ] No text-character decorative lines
- [ ] PageBreak after TOC element
- [ ] Chinese curly quotes escaped: `""` → `\u201c \u201d`
- [ ] All TextRun on dark backgrounds have explicit `color`
- [ ] No undefined/null/NaN in any TextRun text

### Layer 2: Automated Post-Check

```bash
python3 "$DOCX_SCRIPTS/postcheck.py" output.docx
```

Checks 14 rules: blank pages, cover overflow, line spacing, table margins, table pagination, image overflow, font fallback, CJK indent, heading hierarchy, ShadingType misuse, TOC quality, image aspect ratio, document cleanliness, report content quality.

**MUST fix all ❌ errors before delivery.**

### Layer 3: TOC Post-Processing

```bash
python3 "$DOCX_SCRIPTS/add_toc_placeholders.py" output.docx --auto
```

This script:
1. Extracts headings from the document
2. Adds `outlineLvl` to Heading styles in styles.xml
3. Adds `updateFields=true` to settings.xml
4. Fixes malformed fldChar structure (splits merged begin+instrText+separate)
5. Inserts TOC placeholder entries with hyperlinks and bookmarks
6. Adds TOC 1/2/3 styles and Hyperlink style if missing

---

## 11. Source Scripts Reference

### postcheck.py

**Location:** `skills/docx/scripts/postcheck.py`

**Checks performed:**
1. `blank-pages` — Detects trailing page breaks, consecutive empty paragraphs, double section breaks
2. `cover-overflow` — Detects oversized fonts (>44pt), excessive spacing (>5000tw), trailing empty content
3. `line-spacing` — Validates body paragraph line spacing consistency
4. `image-overflow` — Checks image width vs page usable area
5. `font-fallback` — Flags potentially missing fonts
6. `heading-levels` — Detects heading level skips (H1→H3)
7. `shading-type` — Flags `ShadingType.SOLID` misuse
8. `toc` — Validates TOC field presence, heading outlineLvl, updateFields setting
9. `image-aspect-ratio` — Detects stretched/distorted images (>10% drift)

**Usage:**
```bash
python3 postcheck.py output.docx           # Text report
python3 postcheck.py output.docx --json    # JSON output
python3 postcheck.py output.docx --strict  # Warnings = failure
```

**Exit codes:** 0 = pass, 1 = warnings only (with --strict), 2 = errors

### add_toc_placeholders.py

**Location:** `skills/docx/scripts/add_toc_placeholders.py`

**Key functions:**
- `_extract_headings_from_docx()` — Uses python-docx to read headings
- `_fix_update_fields()` — Adds `updateFields=true` to settings.xml
- `_fix_heading_outline_levels()` — Adds `outlineLvl` to Heading styles
- `_fix_fld_char_structure()` — Splits merged fldChar runs
- `_ensure_toc_styles()` — Creates TOC 1/2/3 styles if missing
- `_insert_toc_placeholders()` — Inserts hyperlinked TOC entries with PAGEREF

**Usage:**
```bash
python3 add_toc_placeholders.py output.docx --auto
```

### utilities.py

**Location:** `skills/docx/scripts/utilities.py`

Shared utilities for XML manipulation, namespace handling, and color conversion.

### document.py

**Location:** `skills/docx/scripts/document.py`

Python `Document` class for editing existing .docx files — handles tracked changes, comments, RSIDs, relationships, and content types.

---

## 12. Known Pitfalls & Solutions

### #1: Chinese Curly Quotes Break JS Syntax

**Problem:** `""` and `''` in JS string literals cause syntax errors.
**Solution:** Always escape: `\u201c` `\u201d` `\u2018` `\u2019`

```javascript
// WRONG
new TextRun({ text: "呈现\u201c前低后高\u201d态势" })  // ← This is actually CORRECT
new TextRun({ text: "呈现"前低后高"态势" })  // ← WRONG: bare curly quotes

// CORRECT
new TextRun({ text: "呈现\u201c前低后高\u201d态势" })
```

### #2: Blank Page After Cover in MS Office

**Problem:** MS Office includes border thickness in exact-height calculation.
**Solution:** Always set `borders: allNoBorders` on cover wrapper table.

```javascript
const NB = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const allNoBorders = { top: NB, bottom: NB, left: NB, right: NB,
                       insideHorizontal: NB, insideVertical: NB };
```

### #3: TOC Empty After Word Update

**Problem:** Heading styles missing `outlineLvl` in styles.xml.
**Solution:** Run `add_toc_placeholders.py --auto` which fixes outlineLvl.

### #4: Images Stretched (Aspect Ratio Distortion)

**Problem:** Hardcoding both width and height for images.
**Solution:** Use `image-size` to read actual dimensions, calculate height proportionally.

```javascript
const sizeOf = require("image-size");
const dims = sizeOf(imageBuffer);
const displayWidth = 500;
const displayHeight = Math.round(displayWidth * (dims.height / dims.width));
```

### #5: WPS Shows Black Cells

**Problem:** Using `ShadingType.SOLID` instead of `ShadingType.CLEAR`.
**Solution:** Always use `ShadingType.CLEAR` with `fill` property.

### #6: Page Numbers Show "1decimal"

**Problem:** Using `\* decimal` in footer instrText (it's a docx-js API enum, not a Word field switch).
**Solution:** Use `\* arabic` for Arabic numeral page numbers.

### #7: Cover Content Overflows to Page 2

**Problem:** Fixed spacing values assume specific title length.
**Solution:** Use `calcTitleLayout()` for dynamic font sizing and `calcCoverSpacing()` for dynamic spacing.

### #8: DOCX Module Not Found

**Problem:** `docx` npm package not installed.
**Solution:** `npm install docx` before running generation scripts.

### #9: Large Font Characters Clipped at Top

**Problem:** Paragraph inherits small line spacing from document default.
**Solution:** Set explicit `spacing: { line: fontPt * 23, lineRule: "atLeast" }` on paragraphs with font size > body text.

### #10: Column Widths Broken in WPS

**Problem:** Using DXA width values.
**Solution:** Always use `WidthType.PERCENTAGE` for table column widths.

---

## Appendix A: Markdown → DOCX Quick Reference

```markdown
# Document Title           →  Cover page title
## Section Heading         →  H1 (HeadingLevel.HEADING_1)
### Subsection Heading     →  H2 (HeadingLevel.HEADING_2)
#### Sub-subsection        →  H3 (HeadingLevel.HEADING_3)

Body paragraph text.       →  Justified body, 12pt, 1.3x line spacing
**Bold text**              →  TextRun({ bold: true })
*Italic text*              →  TextRun({ italics: true })
`Code text`                →  TextRun({ font: "Courier New", size: 21 })

- Bullet item              →  Paragraph with \u2022 prefix
1. Numbered item           →  Paragraph with numbering reference

| Header 1 | Header 2 |    →  Table with styled header row
|----------|----------|    →  Border separator
| Cell 1   | Cell 2   |    →  Data cells

> Blockquote text          →  Indented paragraph with left border accent

---                        →  Paragraph with bottom border (horizontal rule)

![Alt text](image.png)     →  ImageRun with aspect ratio preservation
[Link text](url)           →  ExternalHyperlink
```

## Appendix B: DOCX → Markdown Quick Reference

```
Heading1                   →  # Heading Text
Heading2                   →  ## Heading Text
Heading3                   →  ### Heading Text
Body paragraph             →  Plain text paragraph
Bold run                   →  **bold text**
Italic run                 →  *italic text*
Underline run              →  (skip in Markdown)
Table                      →  | col1 | col2 | format
Bullet list                →  - item
Numbered list              →  1. item
Image                      →  ![alt](path)
Hyperlink                  →  [text](url)
Section break              →  ---
```

## Appendix C: Complete Generation Script Template

```javascript
#!/usr/bin/env node
/**
 * Markdown → DOCX converter
 * Usage: node convert.js input.md output.docx
 */
const { Document, Packer, Paragraph, TextRun, Header, Footer,
        AlignmentType, HeadingLevel, PageNumber, Table, TableRow, TableCell,
        WidthType, BorderStyle, ShadingType, TableOfContents, PageBreak,
        SectionType } = require("docx");
const fs = require("fs");

// ── Palette ──
const P = { primary: "#0A1628", body: "#1A2B40", secondary: "#6878A0",
            accent: "#5B8DB8", surface: "#F4F8FC" };
const c = (hex) => hex.replace("#", "");

// ── Builders (copy from Section 6) ──
// h1, h2, h3, body, bodyBold, bodyRuns, bullet, headerCell, dataCell

// ── Markdown Parser (simplified) ──
function parseMarkdown(mdText) {
  // Split into lines, identify headings, paragraphs, tables, lists
  // Return array of { type: "heading"|"paragraph"|"table"|"bullet", content, level }
  // ... (implement based on Section 3 specification)
}

// ── Cover Builder ──
function buildCover(config) { /* See Section 7 */ }

// ── Main ──
const inputFile = process.argv[2];
const outputFile = process.argv[3] || "output.docx";

const mdContent = fs.readFileSync(inputFile, "utf-8");
const parsed = parseMarkdown(mdContent);

// Extract frontmatter, build cover config
// Convert parsed nodes to docx components
// Assemble Document with sections

// const doc = new Document({ ... });
// Packer.toBuffer(doc).then(buf => { fs.writeFileSync(outputFile, buf); });
```

---

*This skill file consolidates knowledge from: Z.AI docx skill system (SKILL.md, design-system.md, common-rules.md, create.md, docx-js-core.md, docx-js-advanced.md, toc.md), postcheck.py, add_toc_placeholders.py, and real-world document generation experience from the Consolidated Remediation Plan Report 5.*
