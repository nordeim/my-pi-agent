# Cover Layout Legacy Templates (Archived from V3.0 → V2.1 Migration)

> **Source:** Archived from `typesetting/cover.md` during the V3.0→V2.1 consolidation (April 2026).
> These templates were removed from the active cover system to streamline to 5 core templates (01 HUD, 03/04 Academic, 06 Institutional, 07 Crystal Blue).
>
> **Use case:** Reference only. For projects requiring the original 11-template system, or when matching legacy documents that used these templates.
>
> **Active templates** are in `typesetting/cover.md`. This file is read-only for historical preservation.

---

# Template 02: Corporate Editorial - Top Bar with Bottom Accent

**Design intent:** Top-bottom symmetry. Top bar provides structural weight, bottom-right info block creates diagonal balance. Solves the "empty edges" problem.

### Layer 1 - Background
- **Background giant year watermark:** Text = current year (e.g. "2026"), **Max font size = 180pt**, measure rendered width - if it exceeds `W * 0.85`, scale down proportionally. Position: `X = W - 20pt` (right edge), `Y = 0.15*H`. Color = primary at **4% opacity**. Font weight = Black. ⚠️ **Full-display iron rule: watermark text must be 100% within the visible page area - cropping is strictly forbidden. Prefer reducing font size over truncation.**

### Layer 2 - Structure
- **Top bar (skyline):** Rectangle at `(0, 0)`, width = `W`, height = **15pt**, primary color fill. Edge-to-edge.
- **Right info accent line (edge seal):** Vertical line at `X = 0.88*W`, from `Y = 0.75*H` to `Y = 0.88*H`. Line width = **4pt**, primary color.

### Layer 3 - Content

| Drawer | Position | Content | Constraints |
|--------|----------|---------|-------------|
| **Left upper - Title group** | `X = 0.12*W`, `Y = 0.15*H` | Kicker (report type/subtitle, 16pt) → Hero Title (company/entity name, 45-65pt / CJK 50-80pt, Heavy) | Stack downward from anchor |
| **Mid-left - Summary** 🆕 | `X = 0.12*W`, `Y = 0.50*H` | Descriptive paragraph | 16-18pt, Regular, line-height 1.6. **Width limit: `W * 0.5`** |
| **Right lower - Meta** | Right-aligned at `X = 0.88*W - 20pt`, `Y = 0.70*H` | Date, version, author | **Right-aligned**, 16-20pt. Must hug the 4pt accent line |

### Best For
Annual reports, financial summaries, investor documents, corporate governance reports

---

# Template 03: The Monolith - Hard-Left Alignment + Right-Side Giant Watermark Counterweight

**Design intent:** Everything hard-left. Right-side watermark counterbalances the asymmetry. Solves the "right half is empty" bug.

### Layer 1 - Background
- **Right-side vertical watermark (load-bearing wall):** Extract a short English word (e.g. "REPORT"). **Auto-scaling font size:** `Max_Font_Size = 180pt`, measure total height after rotation - if it exceeds `H * 0.85`, scale down proportionally. **Rotate 90° clockwise** (or use vertical text mode). Anchor at `X = 0.85*W`, vertically centered: `Y = (H - rendered_text_width) / 2`. Color = primary at **3% opacity**. ⚠️ **Full-display iron rule: watermark text must be 100% within the visible page area - cropping is strictly forbidden. Prefer reducing font size over truncation.**

### Layer 2 - Structure
- **Color dash (visual guide line):** At `(0.12*W, 0.15*H)`, draw a horizontal bar: width = **50pt**, height = **5pt**, primary color.
- **Meta accent line:** At `(0.12*W, Y_meta)`, vertical line: height = meta text block height, width = **2pt**, primary color at 50% opacity.

### Layer 3 - Content

**Unified left edge: `X = 0.12*W`**

| Drawer | Y-Anchor | Content | Constraints |
|--------|----------|---------|-------------|
| **A - Color dash** | `0.15 * H` | Structure element (not text) | 50pt × 5pt bar |
| **B - Kicker** | `0.20 * H` | Report type / subtitle | 16pt, Regular, letter-spacing 3pt, uppercase, opacity 60% |
| **C - Hero Title** | `0.28 * H` | **Company/entity name** | 45-65pt (CJK: 50-80pt), Heavy |
| **D - Summary** 🆕 | `0.45 * H` | Descriptive paragraph (key anti-void element) | 16-18pt, Regular, line-height 1.6. **Width limit: `W * 0.55`** (must not collide with right watermark) |
| **E - Meta** | `0.70 * H` | Author, org, version | 20pt, Regular, line-height 2.0. Left of the 2pt accent line |
| **F - Footer** | `0.90 * H` | Date + doc number, right-aligned at `X = 0.88*W` | 16pt, Regular, opacity 60% |

### Best For
White papers, project proposals, government documents, technical standards

---

# Template 04: Museum Minimal - Refined Corner Crop Marks

**Design intent:** Abandon all-over scattered layout. Four corner crop marks form an invisible "force field box" that concentrates all content dead center.

### Layer 2 - Structure
- Set safety margin `M = 0.08 * W`
- **Four corner marks** at inner corners: `(M, M)`, `(W-M, M)`, `(M, H-M)`, `(W-M, H-M)`
- Each mark: L-shaped, arm length = **30pt**, line width = **2pt**, primary color at 60% opacity
- Marks point **inward** (top-left: right arm + down arm)

### Layer 3 - Content

**This template FORBIDS hardcoded absolute Y coordinates.**

**Centering algorithm (mandatory):**
1. Pre-compose ALL text elements (kicker + title + summary + meta) into a single virtual Text Block
2. Calculate the block's total rendered height `Block_H`
3. Position block: `X = 0` (full width, center-aligned text), `Y = (H - Block_H) / 2`
4. **This guarantees the content group is vertically centered regardless of how much content there is**

**Internal spacing within the centered block:**
- Kicker → Title: `24pt`
- Title → Summary: `20pt`
- Summary → Meta: `40pt`

### Type Scale
| Role | Size | Notes |
|------|------|-------|
| Kicker | 16pt | Uppercase, letter-spacing 4pt, opacity 50%. Bound to report type/subtitle |
| Hero Title | 48-60pt | Heavy - slightly smaller than other templates to fit center composition. **Bound to company/entity name** |
| Summary 🆕 | 16-18pt | Regular, line-height 1.6, center-aligned, width ≤ `W * 0.6` |
| Meta | 16pt | Regular, opacity 60%, at bottom of group |

### Best For
Gallery catalogs, design portfolios, exhibition materials, luxury brand documents

---

# Template 05: Floating Diagonal - Premium Whitespace with Binding Line

**Design intent:** "Left-upper to right-lower" diagonal visual flow. The two text groups create tension across whitespace. The gap IS the design.

### Layer 2 - Structure
- **Binding dashed line:** At `X = 0.08*W`, from `Y = 0.05*H` to `Y = 0.95*H`. Line width = **1pt**, dashed (dash 6pt, gap 8pt), color = light gray (#d0d0d0, 40% opacity).

### Layer 3 - Content

| Group | Position | Content | Constraints |
|-------|----------|---------|-------------|
| **Upper-left group** | Anchor: `X = 0.15*W`, `Y = 0.20*H` | Kicker (report type/subtitle, 16pt gap) → Hero Title (company/entity name, 45-65pt / CJK 50-80pt, Heavy) | Left-aligned. Width limit: `W * 0.7` |
| **Lower-right group** 🆕 | Anchor: `X = 0.45*W`, `Y = 0.60*H` | Summary + Meta + Footer | **Left-aligned** (NOT right-aligned - intentional asymmetry). A **3pt vertical accent line** of height = group text height is drawn at `X = 0.45*W - 12pt` as a visual anchor. Line-height 2.0 for meta, 24pt gap before footer |

**Visual effect:** Upper-left and lower-right groups are "pulled apart" across the diagonal. The empty top-right and bottom-left create tension, not emptiness.

### Best For
Creative reports, editorial layouts, art direction documents, brand guidelines

---

# Template 06: Swiss Grid - Ultimate Precision, Curing All Misalignment

**Design intent:** The typographic "multiplication table." Thick lines physically slice the page into cells. Content fills its assigned cell. Impossible to misalign.

### Layer 2 - Structure (ABSOLUTE - non-negotiable)

```
Horizontal line 1: (0.1*W, 0.25*H) → (0.9*W, 0.25*H), width 2pt, primary
Horizontal line 2: (0.1*W, 0.75*H) → (0.9*W, 0.75*H), width 2pt, primary
Vertical line 1:   (0.45*W, 0.25*H) → (0.45*W, 0.75*H), width 2pt, primary
```

These create 4 zones:

```
┌──────────────────────────────────────┐
│         Zone A - Top Strip           │  ← Kicker / report type
├──────────────────┬───────────────────┤
│   Zone B         │   Zone C          │
│   (left cell)    │   (right cell)    │  ← B: Hero Title (MUST fill)
│   X: 0.1W-0.43W │   X: 0.48W-0.9W  │  ← C: Summary text (MUST fill)
├──────────────────┴───────────────────┤
│         Zone D - Bottom Strip        │  ← Footer / year / doc number
└──────────────────────────────────────┘
```

### Layer 3 - Content (STRICT zone containment)

| Zone | Content | X Range | Y Range | Notes |
|------|---------|---------|---------|-------|
| **A** | Kicker / report type | `0.10*W` - `0.90*W` | `0.15*H` - `0.23*H` | Left-aligned at `X = 0.12*W` |
| **B** | **Hero Title (company/entity name)** | `0.10*W` - `0.43*W` | `0.28*H` - `0.70*H` | **Width = `0.33*W`**. Font must be large enough to physically fill the cell. Text wraps at boundary. |
| **C** | **Summary text** 🆕 | `0.48*W` - `0.90*W` | `0.28*H` - `0.70*H` | **Must contain substantial descriptive text** - this zone MUST be filled. 16-18pt, Regular, line-height 1.6. This is the primary anti-empty-page mechanism. |
| **D** | Footer / date / number | `0.10*W` - `0.90*W` | `0.78*H` - `0.88*H` | Can split: left part + right-aligned part |

### Zone Overflow Protection (MANDATORY)

If text in Zone B or C exceeds the vertical boundary (Y > `0.70*H`):
1. **Step 1:** Reduce font size by 2pt increments (minimum: 16pt for summary, 40pt for title)
2. **Step 2:** If still overflows, truncate with `...` ellipsis
3. **NEVER** let text cross a grid line - the grid is sacred

**Hard width enforcement:**
```python
# Zone B: title MUST wrap within its cell width
zone_b_max_width = 0.33 * W
# If title renders wider → word-wrap, NEVER let it bleed into Zone C

# Zone C: summary MUST wrap within its cell width
zone_c_max_width = 0.42 * W  # (0.90 - 0.48) * W
# Wrap at boundary, add lines, NEVER cross the vertical grid line
```

### Best For
Swiss-style design, data-heavy reports, structured corporate documents, annual reports

---

# Template 07: Solid Sidebar - Massive Pillar Anchoring the Page

**Design intent:** A massive solid-color sidebar provides gravitas. The right side can be loosely arranged - the pillar holds everything together.

### Layer 1 - Background
- **Left sidebar block (giant sidebar pillar):** Rectangle at `(0, 0)`, width = **`0.1*W`** (~80pt on A4), height = `H`. Primary color fill.
- **Sidebar watermark:** Inside the sidebar, render a short word (doc type or year) rotated **-90°**, white at **15% opacity**, vertically centered within the sidebar. **Auto-scaling font size:** `Max_Font_Size = H * 0.5`, measure total height after rotation - if it exceeds `H * 0.85`, scale down proportionally. ⚠️ **Full-display iron rule: watermark text must be 100% within the visible page area - cropping is strictly forbidden.**

### Layer 2 - Structure
- **Bottom horizontal line:** At `Y = 0.90*H`, from `X = Left_Edge` to `X = 0.90*W`. Line width = **1pt**, primary color at 30% opacity.

### Layer 3 - Content

**Safety boundary: `Left_Edge = 0.1*W + 40pt`** - ALL text must start at or right of this line. Zero tolerance for collision with sidebar.

**Layout uses relative vertical centering:**
1. Compose full text group: Kicker + Hero Title + Summary + Meta
2. Calculate total group height
3. Position group at `X = Left_Edge`, `Y = (H - group_height) / 2` (vertically centered)

| Element | Notes |
|---------|-------|
| Kicker | 16pt, Regular, uppercase, letter-spacing 3pt, opacity 60%. Bound to report type/subtitle |
| Hero Title | 45-65pt, Heavy. **Bound to company/entity name** |
| Summary 🆕 | 16-18pt, Regular, line-height 1.6. Width ≤ `0.90*W - Left_Edge` |
| Meta | 20pt, Regular, line-height 1.8 |

**Footer (separate from centered group):**
- On/just above the bottom horizontal line at `Y = 0.90*H - 10pt`
- Left-aligned date at `X = Left_Edge`, right-aligned org name at `X = 0.90*W`
- 16pt, Regular, opacity 60%

### Best For
Government/institutional reports, legal documents, formal project deliverables, bidding documents

---

# Template 10: Academic Journal - Dark bg + Top/bottom lines + Centered + Keywords

**Design intent:** Extended version of Template 09, with dedicated keyword block. Matches the layout of top-tier Chinese journal submissions and thesis covers.

```
┌─────────────────────────────┐
│                             │
│   ══════════════════════    │  ← Top rule
│                             │
│        LABEL (centered)     │
│                             │
│        Title (34pt)         │
│                             │
│        Subtitle             │
│                             │
│          ───                │  ← Thin divider
│                             │
│        Keywords             │
│                             │
│   ══════════════════════    │  ← Bottom rule
│         Footer              │
└─────────────────────────────┘
```

**Best for:** Chinese journal submissions, theses with keywords, formal academic reports

**HTML structure:**
```html
<!DOCTYPE html>
<html lang="zh">
<head>
  <meta charset="UTF-8">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700;900&family=Noto+Sans+SC:wght@300;400;500;700&display=swap" rel="stylesheet">
  <style>
    @page { size: 794px 1123px; margin: 0; }
    :root {
      --c-bg: #162032;
      --c-accent: #4A90C4;
      --c-text: #FFFFFF;
      --c-muted: #90A8C0;
    }
    html, body { margin: 0; padding: 0; width: 794px; height: 1123px; background: var(--c-bg); color: var(--c-text); font-family: 'Noto Sans SC', 'Inter', sans-serif; }
    .cover { width: 794px; height: 1123px; position: relative; display: flex; flex-direction: column; align-items: center; box-sizing: border-box; }
    .rule-top, .rule-bottom { position: absolute; left: 114px; right: 114px; height: 2px; background: var(--c-accent); }
    .rule-top { top: 114px; }
    .rule-bottom { bottom: 114px; }
    .center-block { position: absolute; top: 0; bottom: 0; left: 114px; right: 114px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; }
    .label { font-size: 9pt; color: var(--c-accent); letter-spacing: 3px; text-transform: uppercase; margin-bottom: 40px; }
    .title { font-size: 34pt; font-weight: 700; line-height: 1.3; font-family: 'Noto Serif SC', serif; margin-bottom: 20px; max-width: 500px; }
    .subtitle { font-size: 14pt; color: var(--c-muted); margin-bottom: 40px; max-width: 450px; line-height: 1.5; }
    .divider { width: 152px; height: 0.5px; background: var(--c-accent); margin-bottom: 40px; }
    .keywords { font-size: 11pt; color: var(--c-muted); line-height: 1.8; max-width: 400px; }
    .footer { position: absolute; bottom: 57px; left: 114px; right: 114px; text-align: center; font-size: 9pt; color: var(--c-muted); }
  </style>
</head>
<body>
  <div class="cover">
    <div class="rule-top"></div>
    <div class="rule-bottom"></div>
    <div class="center-block">
      <div class="label"><!-- LABEL --></div>
      <div class="title"><!-- TITLE --></div>
      <div class="subtitle"><!-- SUBTITLE --></div>
      <div class="divider"></div>
      <div class="keywords">
        <!-- KEYWORD 1 --><br>
        <!-- KEYWORD 2 --><br>
        <!-- KEYWORD 3 -->
      </div>
    </div>
    <div class="footer"><!-- FOOTER --></div>
  </div>
</body>
</html>
```

**Recommended palettes:** Same as Template 09.

---

# Template 11: Institutional - White bg + Black border frame + Structured field slots

**Design intent:** The universal institutional cover. White background with a thick black border frame, all content centered, structured field slots with underline placeholders. Matches the style required by most universities worldwide for thesis proposals, dissertations, and formal institutional documents. Also suitable for government reports and official submissions. Zero decorative elements - the formality IS the design.

**⚠️ This template is exempt from PART 4 Academic Cover Color Rules (dark backgrounds).** It uses a white/light background by design, aligning with institutional formatting requirements.

```
┌─────────────────────────────────┐
│  ┌─────────────────────────────┐  │
│  │                             │  │
│  │   INSTITUTION NAME           │  │  ← y = 12%, serif 28-34pt Bold
│  │   (校名/机构名)                │  │
│  │                             │  │
│  │   ━━━━━━━━━━━━━━━━━━━━  │  │  ← thick divider (2pt)
│  │                             │  │
│  │   DOCUMENT TYPE              │  │  ← y = 30%, 20-24pt
│  │   (开题报告/毕业论文/申报书)    │  │
│  │                             │  │
│  │   TITLE                     │  │  ← y = 40%, serif 26-30pt Bold
│  │   (论文题目)                   │  │    max 3 lines, centered
│  │                             │  │
│  │   Field: _______________    │  │  ← y = 58-78%, structured fields
│  │   Field: _______________    │  │    left-label + underline value
│  │   Field: _______________    │  │    e.g. 姓名、学号、导师、院系、日期
│  │   Field: _______________    │  │
│  │   Field: _______________    │  │
│  │                             │  │
│  │   DATE                      │  │  ← y = 88%, centered, 14pt
│  │                             │  │
│  └─────────────────────────────┘  │
└─────────────────────────────────┘
││ = 2.5pt black border, inset 5% from page edge
```

**Best for:** Thesis proposals (开题报告), dissertations, institutional reports, government documents, any formal submission with structured metadata fields

**Content slots:**
| Slot | Required | Example |
|------|----------|---------|
| `institution` | **Required** | "北京大学", "Massachusetts Institute of Technology" |
| `doc_type` | Optional | "开题报告", "Thesis Proposal", "毕业设计" |
| `title` | **Required** | Paper/document title (auto-wrap, max 3 lines) |
| `fields` | Optional | Array of `{label, value}` pairs. Common: 姓名/Name, 学号/ID, 导师/Advisor, 院系/Department, 专业/Major |
| `date` | Optional | "2026年4月", "April 2026" |

**HTML structure:**
```html
<!DOCTYPE html>
<html lang="zh">
<head>
  <meta charset="UTF-8">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700;900&family=Noto+Sans+SC:wght@300;400;500;700&family=Playfair+Display:wght@400;700;900&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
  <style>
    @page { size: 794px 1123px; margin: 0; }
    :root {
      --c-bg: #ffffff;
      --c-text: #1a1a1a;
      --c-accent: #1a1a1a;
      --c-muted: #4a4a4a;
      --c-line: #333333;
    }
    html, body { margin: 0; padding: 0; width: 794px; height: 1123px; background: var(--c-bg); color: var(--c-text); font-family: 'Noto Sans SC', 'Inter', sans-serif; }
    @media screen {
      html { height: auto; display: flex; justify-content: center; min-height: 100vh; background: #e8e8e8; }
      body { transform-origin: top center; scale: min(1, calc(100vw / 794), calc(100vh / 1123)); margin: 0 auto; box-shadow: 0 0 60px rgba(0,0,0,0.15); }
    }
    .cover {
      width: 794px; height: 1123px; position: relative; box-sizing: border-box;
    }
    /* Black border frame - inset 5% from page edge */
    .border-frame {
      position: absolute;
      top: 56px; left: 40px; right: 40px; bottom: 56px;
      border: 2.5px solid var(--c-accent);
      pointer-events: none;
    }
    /* Content area inside frame */
    .content {
      position: absolute;
      top: 56px; left: 40px; right: 40px; bottom: 56px;
      display: flex; flex-direction: column; align-items: center;
      padding: 60px 50px;
      box-sizing: border-box;
    }
    .institution {
      font-size: 30pt; font-weight: 700; letter-spacing: 6px;
      font-family: 'Noto Serif SC', 'Playfair Display', serif;
      text-align: center; margin-bottom: 30px;
      max-width: 580px;
    }
    .thick-divider {
      width: 70%; height: 2px; background: var(--c-accent);
      margin-bottom: 40px;
    }
    .doc-type {
      font-size: 22pt; font-weight: 400; letter-spacing: 4px;
      text-align: center; margin-bottom: 50px;
      color: var(--c-text);
    }
    .title {
      font-size: 26pt; font-weight: 700; line-height: 1.4;
      font-family: 'Noto Serif SC', 'Playfair Display', serif;
      text-align: center; margin-bottom: 60px;
      max-width: 520px;
    }
    .fields-block {
      width: 400px; margin-bottom: auto;
    }
    .field-row {
      display: flex; align-items: baseline;
      margin-bottom: 28px; font-size: 14pt;
    }
    .field-label {
      white-space: nowrap; margin-right: 12px;
      color: var(--c-text); font-weight: 400;
      letter-spacing: 2px;
    }
    .field-value {
      flex: 1; text-align: center;
      border-bottom: 1px solid var(--c-line);
      padding-bottom: 4px; min-height: 24px;
      font-family: 'Noto Sans SC', 'Inter', sans-serif;
    }
    .date-block {
      font-size: 14pt; color: var(--c-muted);
      text-align: center; letter-spacing: 2px;
      margin-top: auto; padding-top: 30px;
    }
  </style>
</head>
<body>
  <div class="cover">
    <div class="border-frame"></div>
    <div class="content">
      <div class="institution"><!-- INSTITUTION NAME --></div>
      <div class="thick-divider"></div>
      <div class="doc-type"><!-- DOCUMENT TYPE --></div>
      <div class="title"><!-- TITLE --></div>
      <div class="fields-block">
        <!-- .field-row -->
        <div class="field-row">
          <span class="field-label">姓名 / Name:</span>
          <span class="field-value"><!-- NAME --></span>
        </div>
        <div class="field-row">
          <span class="field-label">学号 / ID:</span>
          <span class="field-value"><!-- STUDENT ID --></span>
        </div>
        <div class="field-row">
          <span class="field-label">导师 / Advisor:</span>
          <span class="field-value"><!-- ADVISOR --></span>
        </div>
        <div class="field-row">
          <span class="field-label">院系 / Department:</span>
          <span class="field-value"><!-- DEPARTMENT --></span>
        </div>
        <div class="field-row">
          <span class="field-label">专业 / Major:</span>
          <span class="field-value"><!-- MAJOR --></span>
        </div>
      </div>
      <div class="date-block"><!-- DATE --></div>
    </div>
  </div>
</body>
</html>
```

---

# Legacy PART 2: Template Selection Guide (V2.2 Intent System)

> The active cover.md uses a simplified 5-template system with updated intent mappings. This is the V2.2 matrix for reference.

Template selection uses a two-dimensional matrix: **Intent** (from `visual_framework.md` 5-intent system) × **Document Type**. This replaces the old "Document Tone" classification and aligns with the Intent Mapping Table in `creative-fixed-canvas.md`.

| Intent | Document Type | Recommended Templates | Default |
|--------|---------------|----------------------|---------|
| **Calm** | Healthcare / Wellness / Minimalist | 04 Museum, 01 HUD | **04** |
| **Calm** | Academic / Research | 06 Swiss Grid, 03 Monolith | **06** |
| **Tension** | Crisis / Alert / Disruption | 01 HUD, 05 Diagonal | **01** |
| **Energy** | Marketing / Creative / Design | 05 Diagonal, 06 Swiss Grid | **05** |
| **Energy** | Technology / Data | 01 HUD, 06 Swiss Grid | **01** |
| **Authority** | Formal / Corporate / Financial | 02 Corporate, 03 Monolith | **03** |
| **Authority** | Government / Bidding | 07 Sidebar, 03 Monolith, **11 Institutional** | **07** |
| **Authority** | Thesis proposal / Dissertation cover | **11 Institutional** | **11** |
| **Authority** | Luxury / Editorial | 03 Monolith, 05 Diagonal | **03** |
| **Warmth** | Food / Lifestyle / Home | 04 Museum, 05 Diagonal | **04** |

> **Legacy mapping:** "Formal/Corporate" tone → Authority intent, "Minimalist" tone → Calm intent, "Luxurious/Editorial" tone → Authority intent.

**⚠️ No Global Default.** When no specific style is explicitly requested, the LLM MUST analyze the document's content, tone, and audience to autonomously select the most fitting template. Cross-reference the Intent (derived from content via `design_engine.py derive` or manual judgment) with the Document Type to find the best match. Every cover selection must be a deliberate design decision.

---

# Archived Code-Level Safety Helpers (Removed from Active cover.md)

These helper functions were in V3.0 but consolidated into prose rules in V2.1.

## S3.4 - Hard Width Boundary Enforcement (Legacy Code Reference)

**Every drawer/zone has a maximum width. Text wrapping MUST respect this width exactly.**

```python
# WRONG - text bleeds past boundary
draw_text(x=0.12*W, text=long_title, width=None)  # width unconstrained!

# RIGHT - hard clamp
max_width = 0.6 * W  # or zone-specific value
wrapped_lines = word_wrap(text, font, size, max_width)
for i, line in enumerate(wrapped_lines):
    draw_text(x=x_anchor, y=y_anchor + i * line_height, text=line)
```

**Rule:** It is acceptable for text to add extra lines (grow vertically). It is NEVER acceptable for text to exceed its horizontal boundary (grow horizontally). Vertical overflow triggers S3.2; horizontal overflow is a critical bug.

## S3.5 - Mandatory Summary Auto-Generation (Legacy Code Reference)

**If the user provides only a title and no description/summary, the system MUST generate placeholder text.**

```python
if not summary_text or summary_text.strip() == "":
    if lang == "zh":
        summary_text = f"本报告由{org_name or '系统'}自动生成,包含了综合数据分析与洞察结论。"
    else:
        summary_text = f"This report presents comprehensive analysis and key insights prepared by {org_name or 'the organization'}."
```

**Why:** A title-only cover looks barren. The Summary drawer physically occupies 2-4 lines, filling mid-page void and making the cover look intentionally designed rather than half-finished.

## S3.6 - Background Watermark Full-Display Enforcement (Legacy Code Reference)

**All watermark text in the background layer (Layer 1) must be 100% within the visible page area. Cropping, truncation, or extending beyond page boundaries is strictly forbidden.**

**Templates affected:**
- Template 02 giant year watermark
- Template 03 right-side vertical watermark
- Template 07 sidebar watermark

**Adaptive algorithm (mandatory):**

```python
def safe_watermark_size(text, font, max_size, available_space):
    """
    Ensure watermark text is fully displayed within available space.
    available_space: available width/height (depending on text direction)
    """
    rendered = measure_text(text, font, max_size)
    if rendered > available_space:
        return max_size * (available_space / rendered)
    return max_size
```

1. Horizontal text: rendered width must not exceed `W * 0.90` (5% safety margin on each side)
2. Vertical/rotated text: rendered height must not exceed `H * 0.85` (7.5% safety margin top and bottom)
3. If exceeded, scale down font size proportionally - never truncate
4. **Anchor coordinates must never exceed page boundaries** (no negative X/Y values or values exceeding W/H)

**This is a visual quality red line: a truncated "REPO" is worse than no watermark at all. A complete "REPORT" is the design.**

## S3.7 - Line-Length Alignment (Legacy Code Reference)

**Problem:** Decorative lines (vertical accent lines, horizontal dividers, underlines) are arbitrary lengths that don't relate to the text they accompany, creating visual disconnect.

**Iron Rule:** Lines must be sized relative to the text they serve:

### Vertical Lines (e.g., Template 01 thick line, Template 08 accent line)

**Vertical line height = text block height** (from first text element to last text element in the same column).

```python
# WRONG - arbitrary fixed height
vline_top = 0.1 * H
vline_bottom = 0.9 * H  # ← line runs full page regardless of content

# RIGHT - measure text block, then draw line
text_top = first_element_y        # e.g., label at 0.12*H
text_bottom = last_element_y + last_element_height  # e.g., footer at 0.88*H
vline_top = text_top - U           # 1U padding above first element
vline_bottom = text_bottom + U     # 1U padding below last element
```

### Horizontal Lines (e.g., Template 08 hline, dividers)

**Horizontal line width ≥ text width of the widest text element in its zone.** Lines may be slightly longer (up to 120% of text width) but NEVER shorter.

```python
# WRONG - fixed short line
hline_width = 200  # ← might be shorter than the title

# RIGHT - measure, then draw
max_text_width = max(measure(title), measure(subtitle), measure(authors))
hline_width = max(max_text_width, max_text_width * 1.1)  # at least as wide, up to 110%
# Clamp to available space
hline_width = min(hline_width, available_width)
```

### HTML/CSS Implementation

For HTML/Playwright covers, use relative sizing:

```css
/* Vertical line spans the content block */
.vertical-accent {
  position: absolute;
  top: var(--text-top);
  bottom: var(--text-bottom);
  width: 4px; /* or var(--line-width) */
  background: var(--c-accent);
}

/* Horizontal divider: min-width matches text container */
.divider {
  min-width: max(var(--title-width), var(--subtitle-width), var(--author-width));
  height: 0.5px;
  background: var(--c-accent);
}
```

**Checklist:**
- [ ] Every vertical line's height matches its adjacent text block span (± 1U padding)
- [ ] Every horizontal line's width ≥ widest text element in its zone

## S3.8 - Vertical Balance (Legacy Code Reference)

**Problem:** Content clusters at the top of the page, leaving the bottom 40%+ as dead whitespace. This happens when anchor points are set too high and don't adapt to content volume.

**Root cause:** Fixed anchor grid with `ANCHOR_TITLE_Y = 0.20*H` pushes everything upward regardless of how much content there is.

### Solution: Adaptive Vertical Centering

**When total content height < 50% of page height, switch to centered distribution mode:**

```python
# Step 1: Calculate total content height
content_elements = [title, subtitle, summary, meta, footer]
total_content_h = sum(elem.height for elem in content_elements) + total_gaps

# Step 2: Check fill ratio
fill_ratio = total_content_h / (H * 0.80)  # usable height (excluding margins)

if fill_ratio < 0.50:
    # LOW CONTENT MODE - vertically center the entire block
    start_y = (H - total_content_h) / 2
    # Distribute elements from start_y downward with standard gaps
else:
    # NORMAL MODE - use anchor grid
    # But shift anchors down: title at H*0.30-0.35 (not 0.20-0.25)
    pass
```

### Anchor Adjustment Rules

**CJK Title Size Compensation**

CJK characters at the same pt size as Latin characters appear visually smaller due to denser stroke structure. Compensate:

```
CJK Hero Title:    50-80pt (Latin: 45-65pt) - increase by 15-20%
CJK Kicker:        11-12pt (Latin: 9pt)
CJK Summary:       17-20pt (Latin: 16-18pt)
```

**Detection:** If title string contains CJK characters (`\u4e00-\u9fff`), apply CJK size multiplier.

### HTML/CSS Implementation

```css
/* Vertical centering mode for sparse content */
.cover.sparse-content .center-block {
  justify-content: center;  /* flexbox vertical center */
}

/* CJK title size bump */
.title:lang(zh), .title:lang(ja), .title:ko {
  font-size: clamp(50pt, 8vw, 80pt);  /* larger than Latin range */
}
```

**Checklist:**
- [ ] Content is visually centered on the page (optical center, not mathematical)
- [ ] Sparse-content covers use centered distribution, not fixed anchors
- [ ] CJK titles use appropriate size bump (50-80pt vs 45-65pt)

---

# Anti-Pattern: Percentage Top on Heightless Containers (Legacy Reference)

**Problem:** `top: XX%` resolves against containing block's height. If height is undefined (all children absolutely positioned), percentages collapse and elements stack.

**Iron rule:** Container with `top: XX%` children MUST have deterministic height (`height: 100%`, `inset: 0`, or `top` + `bottom` pair).

```css
/* ❌ BANNED: wrapper without height, percentage is undefined */
.content-left {
  position: absolute;
  left: 0; right: 0;
  /* NO height, NO bottom → height = 0 */
}
.kicker   { position: absolute; top: 20%; }  /* 20% of 0 = 0 → stacks at top */
.title    { position: absolute; top: 26%; }  /* stacks on top of kicker */
.summary  { position: absolute; top: 48%; }  /* stacks on top of title */

/* ✅ Safest: flat structure with px values */
.kicker   { position: absolute; top: 225px;  left: 95px; }
.title    { position: absolute; top: 292px;  left: 95px; }
.summary  { position: absolute; top: 539px;  left: 95px; }
.meta     { position: absolute; top: 786px;  left: 95px; }

/* ✅ OK: wrapper with inset:0 gives it known height */
.content-left { position: absolute; inset: 0; }
.title   { position: absolute; top: 26%; }  /* 26% of 1123px ✓ */
```

**Quick self-check before writing cover CSS:**
1. For every element with `top: XX%` — trace upward: does the containing block have a known height?
2. If unsure → use `px` values instead (calculate from `var(--h)` manually: `26% × 1123 = 292px`)
3. If using a grouping wrapper → give it `inset: 0` or explicit `height: 100%`

---

# Legacy CHANGELOG (V1.0 → V3.0)

| Version | Date | Changes |
|---------|------|---------|
| V1.0 | - | Initial 7 layouts (Diagonal Tension, Vertical Axis, etc.) |
| V2.0 | 2026-04-03 | Complete rewrite. Absolute Anchor Grid; Z-index layers; Typography Weight System; 7 new templates with percentage coordinates; Code-level safety. |
| **V2.1** | **2026-04-03** | **Summary Block upgrade.** Added mandatory Summary/Description drawer to all 7 templates (anti-void iron rule). Introduced base spacing unit `U = W * 0.05`. Refined Hero Title range to 45-65pt. Added S3.4 Hard Width Boundary Enforcement + S3.5 Mandatory Summary Auto-Generation. Template 01: added Summary drawer at Y=0.45*H. Template 02: added Summary at Y=0.45*H + refined watermark to 180pt. Template 03: added Summary at Y=0.40*H with W*0.55 width guard. Template 04: Summary included in center-calculated block. Template 05: lower-right group expanded with Summary + 3pt accent line. Template 06: Zone C explicitly designated for substantial summary text. Template 07: sidebar width changed to `0.1*W` (~80pt), content uses relative vertical centering. |
| **V2.2** | **2026-04-07** | **Intent system unification + Template 11.** Part 2 Template Selection Guide migrated from "Document Tone" to Intent × Document Type matrix (aligned with `visual_framework.md` 5-intent system and `creative.md` Intent Mapping Table). Added Template 11 (Institutional) - white bg + black border frame + structured field slots for thesis proposals, dissertations, and institutional documents. Academic Template Selection Guide updated. |
| **V3.0** | **2026-04-07** | **Color unification + Layout balance overhaul.** (1) All template CSS variables renamed to `--c-` prefix (`--c-bg`, `--c-accent`, `--c-text`, `--c-muted`) for palette system alignment. Hardcoded hex values replaced with CSS variables. Palette tables marked as fallback defaults with `palette.cascade` as canonical source. (2) Added S3.7 Line-Length Alignment - vertical/horizontal lines must match text span. (3) Added S3.8 Vertical Balance - adaptive centering for sparse content, CJK title size compensation (50-80pt vs Latin 45-65pt), anchor points shifted down (title H*0.30, summary H*0.50, meta H*0.70). (4) Output cleanliness rules - no version numbers, draft labels, or process artifacts in final PDF. |