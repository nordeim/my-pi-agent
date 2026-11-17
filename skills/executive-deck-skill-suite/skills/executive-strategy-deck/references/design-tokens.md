# Design Tokens — Navy/Orange Executive System

Every value below is **locked**. The visual quality of this deck family comes from
disciplined repetition of a small token set — when you invent new colors, sizes, or
shadows, the deck stops looking like the reference. Treat this file as the law; the
QA script (`scripts/qa_check.py`) enforces the color subset mechanically.

The Tailwind syntax shown is arbitrary-value notation (`bg-[#0A2540]`, `text-[13px]`,
`h-[85px]`) because every slide loads Tailwind from CDN with no config file.

## Color system

Two hues carry the entire brand. Everything else is an opacity derivative.

| Token | Hex | Role | Tailwind |
|---|---|---|---|
| `navy` | `#0A2540` | Primary. Header bar, titles, body text, chart segments, dark page background | `bg-[#0A2540]`, `text-[#0A2540]`, `border-[#0A2540]` |
| `accent` | `#FF5722` | Emphasis ONLY: metric numbers, icons, underlines, hero chips, key phrases | `text-[#FF5722]`, `bg-[#FF5722]`, `border-[#FF5722]` |
| `accent-light` | `#FF7043` | Gradient partner of accent (never used alone) | `to-[#FF7043]` |
| `surface` | `#FEFEFE` | Content page background | `bg-[#FEFEFE]` |
| `page-mat` | `#F4F4F4` | Browser body behind the slide (never inside the slide) | `background: #f4f4f4` in CSS |
| `white` | `#FFFFFF` | Text/icons on dark, card surfaces on light pages | `bg-white`, `text-white` |

**Rules**

- Orange occupies ~10% of visual weight per slide. If a slide feels "orange-heavy",
  you have converted structure into emphasis — revert structure to navy.
- Never introduce a third hue (no blues, greens, reds, purples — severity chips use
  navy/orange tints only; see Chips).
- Neutrals are opacity derivatives of navy or white, never standalone grays.

### Opacity derivatives (the only allowed neutrals)

| On light surfaces | On dark surfaces |
|---|---|
| `text-[#0A2540]/70` — body copy | `text-white/80` — body copy |
| `text-[#0A2540]/60` — subtitles, secondary text | `text-white/70` — subtitles |
| `text-[#0A2540]/50` — section labels | `text-white/60` — eyebrows, secondary |
| `text-[#0A2540]/40` — disabled/decorative | `text-white/50` — labels on glass cards |
| `bg-[#0A2540]/5 → /10` — card gradient | `bg-white/5` — dark cards |
| `bg-[#0A2540]/10` — card borders, tracks | `border-white/10` — dark card borders |
| `bg-[#0A2540]/10` + `text-[#0A2540]` — navy chips | `border-white/30` — LOGO box frame |

### Chart ramp (fixed order, max 4 segments)

```
['#FF5722', '#FF7043', '#0A2540', '#0A2540B3']
```

The hero (largest / most important) segment is always first, in accent orange.
In HTML legend rows the 4th stop renders as `bg-[#0A2540]/70`.
Chart borders use `borderColor: '#FEFEFE'` on light cards.

## Typography

Single family: **Roboto** (weights 300, 400, 500, 700, 900), with MiSans/Noto Sans SC
fallback so CJK content renders consistently. One `@font-face` for MiSans ships in the
page chassis. Never add a second Latin family.

```css
@font-face {
    font-family: 'MiSans';
    src: local('MiSans'), url('fonts/MiSans-Regular.ttf') format('truetype');
    font-weight: 400;
    font-display: swap;
}
body { font-family: 'Roboto', 'MiSans', 'Noto Sans SC', sans-serif; }
```

### Size scale (exhaustive — no intermediate sizes)

| Size | Class | Where used |
|---|---|---|
| 54px black | `text-[54px] font-black` | Cover title only |
| 44px bold | `text-[44px] font-bold` | Closing title |
| 52px bold | `text-[52px] font-bold` | Dark-page metric numbers |
| 44px bold | `text-[44px] font-bold` | Light-page metric numbers (metric cards) |
| 40px bold | `text-[40px] font-bold` | Content page titles |
| 36px bold | `text-[36px] font-bold` | Timeline month metric |
| 28px | `text-[28px]` | Icon glyphs in 56px tiles; chart center number (`bold 28px Roboto`) |
| 24px | `text-2xl` (icons) / `text-3xl` (avatar icon) | Small icon tiles, avatar |
| 20–22px | `text-xl font-bold` | Header-bar deck title, card titles (2xl personas) |
| 17px bold | `text-[17px] font-bold` | Pillar card titles |
| 18px bold | `text-lg font-bold` | Card titles, legend values |
| 15px | `text-[15px]` | Subtitles, driver/risk titles, highlight headlines |
| 14px | `text-[14px]` | Metric labels, persona quotes (`text-sm`) |
| 13px | `text-[13px]` | Body copy in cards, chart sub-labels, highlight body |
| 12px | `text-[12px]` | Driver/risk/timeline descriptions |
| 11px | `text-[11px]` | Header eyebrow, severity chips, glass-card mini labels |

### Eyebrow & chip conventions

- Eyebrows: UPPERCASE, `tracking-[0.2em]` (header) or `tracking-[3px]` (cover chip),
  `text-white/60` on dark / `text-[#0A2540]/50` on light, `font-medium`.
- Lead a content zone with a micro-label when the zone needs one:
  `<p class="text-[13px] font-semibold text-[#0A2540]/50 tracking-wider uppercase mb-4">…</p>`
- Line-height: `leading-tight` on titles, `leading-relaxed` on body, never default.

## Spacing & layout frame

| Token | Value |
|---|---|
| Canvas | `1280 × 720`, `.ppt-slide { overflow: hidden; position: relative; margin: 0 auto; }` |
| Header bar | `h-[85px]` + `px-12`, flex, justify-between |
| Page padding | `p-12 pb-8` on `<main>` (cover/closing use `p-12` full-bleed) |
| Content-zone budget | ~455px after header + title block — verify with `scripts/geometry_check.js` |
| Grid | 12 columns; `gap-6` (3–4 col rows) or `gap-8` (chart splits) |
| Common splits | `col-span-4` ×3 · `col-span-5` + `col-span-7` · `grid-cols-4` |
| Title block | first grid sits `mt-4`–`mt-8` below the title (per-archetype values in the layout catalog are pre-budgeted — do not loosen them); second row `mt-6` |
| Card padding | `p-6` (standard cards, roadmap/timeline columns) · `px-6 py-5` (chart cards) · `p-5` (risk cards) · `p-4` (dense grids: pillars) · `p-8` (persona card) |

## Radius, border, shadow

| Token | Value | Used on |
|---|---|---|
| `rounded` | 4px | Cover eyebrow chip, LOGO box |
| `rounded-lg` | 8px | Compact cards (drivers, risks, highlight bar edges via `rounded-r-lg`) |
| `rounded-xl` | 12px | Standard cards, icon tiles, glass cards, chart cards |
| `rounded-2xl` | 16px | Persona card |
| `rounded-full` | — | Status chips, quarter chips, dots, numbered circles, avatar |
| Card border | `border-2 border-[#0A2540]/10` (light) · `border border-white/10` (dark) | |
| Accent border | `border-l-4 border-[#FF5722]` | Driver/risk/pain cards, highlight bars |
| Shadow | `shadow-sm` — ONLY on white `bg-white` cards; gradient-tint cards carry no shadow | |

## Component library

Copy these class strings verbatim; they are tuned to fit the 720px height budget.

### Brand header bar (every content page)
```html
<header class="h-[85px] bg-[#0A2540] flex items-center justify-between px-12">
    <div>
        <p class="text-white/60 text-[11px] tracking-[0.2em] font-medium">CONFIDENTIAL &amp; PROPRIETARY</p>
        <h2 class="text-white text-xl font-bold mt-1">[Deck Title]</h2>
    </div>
    <div class="border border-white/30 rounded px-3 py-1.5 text-white/80 text-sm tracking-widest">[BRAND]</div>
</header>
```

### Title ritual (every content page)
```html
<h1 class="text-[40px] font-bold text-[#0A2540] leading-tight">[Page Title]</h1>
<div class="w-20 h-1 bg-[#FF5722] mt-4"></div>
<p class="text-[15px] text-[#0A2540]/60 mt-3 max-w-3xl">[One-sentence subtitle.]</p>
```
Dark variant: `text-white` title, `text-white/60` subtitle. Cover variant:
`w-24 h-1.5` underline; closing variant: `w-20 h-1.5` centered (`mx-auto`).

### Gradient card (default surface on light pages)
```html
<div class="bg-gradient-to-br from-[#0A2540]/5 to-[#0A2540]/10 rounded-xl p-6 border-2 border-[#0A2540]/10">
```

### Icon tile
```html
<div class="w-14 h-14 bg-gradient-to-br from-[#FF5722] to-[#FF7043] rounded-xl flex items-center justify-center">
    <i class="material-icons text-white text-[28px]">rocket_launch</i>
</div>
```
Sizes: `w-14 h-14` (standard) · `w-12 h-12` + `text-2xl` (chart-card header) ·
`w-16 h-16` + `text-3xl` (dark objective cards) · `w-10 h-10` (highlight bar).
Icons are filled Material Icons; verify every icon name exists in the set.

### Left-border accent card (drivers, risks, pain points)
```html
<div class="bg-white rounded-lg p-4 border-l-4 border-[#FF5722] shadow-sm">
```
Dark-page/tinted variant swaps `bg-white shadow-sm` for
`bg-gradient-to-br from-[#0A2540]/5 to-[#0A2540]/10`.

### Metric block
```html
<p class="text-[44px] font-bold text-[#FF5722]">220%</p>
<p class="text-[14px] text-[#0A2540]/70 mt-2">Cloud Revenue Growth</p>
```
Dark pages: `text-[52px]`, label `text-white/60 text-sm`, inside `bg-white/5` cards.

### Chip / badge (three semantic variants)
```html
<!-- orange-tint: emphasis, ON TRACK, hero tags -->
<span class="bg-[#FF5722]/10 text-[#FF5722] text-xs font-bold px-3 py-1.5 rounded-full">ON TRACK</span>
<!-- navy-tint: neutral status, AT RISK, MEDIUM severity, quarter tags -->
<span class="bg-[#0A2540]/10 text-[#0A2540] text-xs font-bold px-3 py-1.5 rounded-full">AT RISK</span>
<!-- solid navy: quarter headers, meta -->
<span class="bg-[#0A2540] text-white text-sm font-bold px-4 py-1.5 rounded-full">Q1 2026</span>
<!-- tag chips on pillar cards -->
<span class="bg-[#FF5722]/10 text-[#FF5722] text-[11px] px-3 py-1 rounded-full font-medium">Reliability</span>
```

### Numbered step (decision chains, drivers)
```html
<div class="flex items-start gap-4">
    <div class="w-10 h-10 bg-[#FF5722] rounded-full flex-shrink-0 flex items-center justify-center text-white font-bold">1</div>
    <div>
        <h4 class="text-[15px] font-bold text-[#0A2540]">[Step title]</h4>
        <p class="text-[12px] text-[#0A2540]/60 leading-relaxed mt-1">[One-line description.]</p>
    </div>
</div>
```

### Bottom highlight bar
```html
<div class="bg-gradient-to-r from-[#FF5722]/10 to-transparent border-l-4 border-[#FF5722] rounded-r-lg p-5 mt-8 flex items-center gap-4">
    <i class="material-icons text-[#FF5722] text-2xl">flag</i>
    <div>
        <p class="text-[15px] font-bold text-[#0A2540]">[Takeaway headline]</p>
        <p class="text-[13px] text-[#0A2540]/70 mt-1">[One-line supporting detail.]</p>
    </div>
</div>
```
Dark variant: headline `text-white/90`, body `text-white/60`, icon tile `w-10 h-10 bg-[#FF5722] rounded-lg`.

### Glass info card (cover meta, closing highlights)
```html
<div class="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20">
```

### Cover/closing overlay formulas
```html
<!-- Cover: directional, keeps left text legible, lets photo breathe on the right -->
<div class="absolute inset-0 bg-gradient-to-r from-[#0A2540]/95 via-[#0A2540]/85 to-[#0A2540]/40"></div>
<!-- Closing: uniform, centered content -->
<div class="absolute inset-0 bg-gradient-to-br from-[#0A2540]/95 via-[#0A2540]/90 to-[#0A2540]/80"></div>
```
Background photo via inline style on `.ppt-slide`:
`class="ppt-slide bg-cover bg-center" style="background-image: url('https://…')"`.
Photo choice matters: dark, calm, corporate (architecture, cityscapes, abstract tech).

### Progress bar
```html
<div class="w-full h-3 bg-[#0A2540]/10 rounded-full mt-3">
    <div class="w-[78%] h-full bg-gradient-to-r from-[#FF5722] to-[#FF7043] rounded-full"></div>
</div>
```

### Legend row (custom chart legend)
```html
<div class="flex items-center justify-between">
    <div class="flex items-center gap-3">
        <div class="w-3 h-3 rounded-full bg-[#FF5722]"></div>
        <span class="text-[13px] text-[#0A2540]/80 font-medium">[Segment label]</span>
    </div>
    <span class="text-[13px] font-bold text-[#0A2540]">38%</span>
</div>
```
Wrap the rows in `<div class="mt-6 space-y-3">` inside the chart card.
