# Stage 3: Design Spec Agent Reference

> Obeys `00-contract.md`. Where this file and the contract disagree, **the contract wins** (§4 design system, §1 paths, §5 the gate). This stage is the **single author** of the design system — it runs ALONE (fan-in) after every extraction fragment exists. No other agent writes tokens.

**ROLE** — You are the Design Spec agent in a pixel-perfect cloning pipeline. You read everything under `02-extraction/`, infer ONE token system by **usage frequency + confidence**, and emit two files. You do **not** browse, do **not** capture screenshots, do **not** write code. You only read JSON/HTML artifacts and write Markdown + JSON.

---

## 1. Inputs (exact paths — contract §1)

Read ALL of these before writing a single line. Missing any source produces an incomplete system.

| File | What it contains | Primary use here |
|------|------------------|------------------|
| `02-extraction/fragments/{page}.computed.json` | Deduped computed-style **archetypes**, each with a `count`, sample selector, and `getBoundingClientRect` | The frequency signal — rank tokens by `count` summed across pages |
| `02-extraction/fragments/{page}.pseudo.json` | `::before/::after/::placeholder/::marker/::selection/::first-letter/::first-line/::backdrop` | Gradient text, overlay glyphs, selection color, custom markers |
| `02-extraction/fragments/{page}.states.json` | Forced `:hover/:focus/:focus-visible/:active` **deltas** (CDP) | States section deltas |
| `02-extraction/fragments/{page}.layout.json` | flex/grid, stacking contexts, **real `@media`/`@container` `conditionText`**, per-archetype rects | Measured breakpoints + layout patterns |
| `02-extraction/fragments/{page}.dom.html` | Cleaned `outerHTML` | Resolve which selectors actually exist (for assertions.json) and inline-SVG icon source |
| `02-extraction/css-variables.json` | `{ "themes": { "light": {...}, "dark": {...} } }` — resolved var union per theme | Theme tokens; original var names |
| `02-extraction/all-styles.json` | Full CSSOM rule dump (style + `@media`/`@container`/`@font-face`/`@keyframes`/`@supports`), incl. refetched cross-origin sheets | **Authored** rule values + `@keyframes` definitions (highest authority) |
| `02-extraction/fonts.json` | `@font-face` + `document.fonts` loaded set + variable-font **`fvar` axes** | Typography font stacks, weights, axes, self-hosted paths |
| `02-extraction/assets.json` | Manifest of DOWNLOADED bytes (hash, ext, intrinsic `naturalWidth/Height`, srcset) | Assets table (downloaded paths only — never picsum/pravatar) |

There are **no** `computed-styles.json`, `animations.json`, or screenshot reads in this stage — those were prior-version inputs and are gone. Keyframes live in `all-styles.json`; states live in `{page}.states.json`; computed archetypes live in `{page}.computed.json`.

---

## 2. The authoritative-source order (contract §3, §4)

When two artifacts disagree about a value, take the higher one and **cite which artifact won**:

```
1. CSSOM authored rule        (all-styles.json)         ← highest authority
2. forced-state computed      ({page}.states.json)      ← only for :hover/:focus/:active
3. computed archetype         ({page}.computed.json)    ← the rendered ground truth for static props
4. screenshot estimate        (N/A here — mark ~ only if truly nothing else exists)
```

A computed archetype reflects what the browser actually painted, so it beats nothing except an authored rule (authored rules name the *intent*, e.g. a `var(--accent)` token name, and survive theme toggles). For interaction deltas, the forced-state read beats the static archetype. **Every token cites its artifact** in an `evidence` column (e.g. `all-styles.json :root`, `home.computed.json #count=58`, `light theme`).

---

## 3. Inference methodology — frequency + confidence

You are NOT dumping per-element CSS. You are inferring the **canonical value for each role**. Method:

### 3.1 Build a frequency table per role
For each design role (a given color slot, a font size, a radius, a shadow, a gap), gather every candidate value from the computed archetypes and tally `count`:

1. **Sum the archetype `count` fields.** Each archetype in `{page}.computed.json` already represents N deduped elements via its `count`. The role's token = the value with the **highest total `count`** across all pages. Example: if `borderRadius: 8px` appears in archetypes totaling `count` 240 and `borderRadius: 12px` totals 30, the `--radius-md` token is `8px` and `12px` becomes `--radius-lg` (a less-frequent but distinct rung).
2. **Cross-route confidence boost.** A value seen on **multiple route slugs** is more canonical than one seen on a single page, even at equal raw count. Rank: `confidence = total_count × (routes_seen)`. A color on 3/3 routes with count 80 outranks a color on 1 route with count 120.
3. **Authored-rule override.** If `all-styles.json` declares the value as a CSS variable on `:root`/`[data-theme]` (e.g. `--color-accent: #0969da`), adopt that as the token **and keep the original variable name** so Build can reuse it. The authored declaration outranks the frequency winner even if some elements override it locally.
4. **Distinct-rung detection for scales** (spacing, radius, type, shadow): cluster candidate values, collapse near-duplicates (±1px), and emit each cluster center as one scale rung ordered ascending. Label the most-frequent rung as the "base" (`--space-4`, `--radius-md`, `--text-base`).

### 3.2 Confidence label
Tag every token with a confidence so Build and the gate know what to trust:

| Confidence | Criteria |
|-----------|----------|
| **high** | authored CSS variable, OR computed value with high total count seen on ≥2 routes |
| **med** | computed value, single route, moderate count |
| **low** | inferred/estimated; mark the value with a leading `~` |

Never leave a value blank. If nothing supports it, write `~` + best estimate and confidence `low`.

---

## 4. Output File 1 — `03-design-spec/DESIGN.md`

`DESIGN.md` is a **portable, drop-in design file** authored in the widely-used `design.md` best-practice structure (à la `github.com/VoltAgent/awesome-design-md`). It is written so a human or a coding agent can reference it to **build a new page, customize the app, or drop it into a different project** — not just so this pipeline can consume it internally. So on top of the rigorous token tables, it opens with the overall *feel*, ends with an agent prompt guide, and stays self-contained (no references to `02-extraction/` paths a reader of the standalone file wouldn't have — those belong in the `Evidence` column only).

Header line: `# Design System: {App Name}` then the **mandatory sections below in this order**. Section 4.0 (Visual theme) comes FIRST, the existing detailed token sections (4.1–4.12) in the middle, and Design guardrails + Agent Prompt Guide LAST (§4.13–4.14). Each token section uses the table template given. Every color carries hex AND `rgb()` (Build needs the rgb triplet for `rgba(var(--x-rgb), α)`). Every numeric carries its unit. Every row carries an `Evidence` column citing the source artifact.

> **Portability note.** DESIGN.md must read as a self-standing design language, not pipeline scratch. A reader who has *only* this file — in another repo, a new project, or a fresh agent session — should be able to reproduce the look from it alone. Keep the artifact citations in the `Evidence` column (they prove the values are measured, not invented) but write the prose sections (4.0 theme, 4.13 guardrails, 4.14 agent guide) so they make sense with no access to `02-extraction/`.

### 4.0 Visual theme / atmosphere (FIRST — the feel before the values)

Open DESIGN.md with ONE short paragraph (2–4 sentences) capturing the overall feel — the atmosphere an agent must reproduce before any single value. Distill it from the dominant tokens you inferred (background lightness, contrast, density, accent restraint, corner softness, motion energy), not from imagination. Examples of the register: *"Dark, dense, keyboard-first, high-contrast — near-black surfaces, a single electric-indigo accent, tight 4px spacing rhythm, crisp 6–8px corners, and fast 150ms transitions. Feels like a pro developer tool: quiet chrome, loud focus states."* Name the **mood**, the **density** (airy vs. dense), the **contrast level**, the **accent discipline** (one accent vs. many), the **corner/shadow softness**, and the **motion energy**. This paragraph is the single most-quoted line when an agent builds a new page, so make it accurate and concrete.

```markdown
## Visual Theme

{App Name} is **{1–4 sentence atmosphere}**. Surfaces: {…}. Contrast: {…}. Density: {…}. Accent discipline: {…}. Corners/shadows: {…}. Motion: {…}.
```

### 4.1 Colors

```markdown
## Colors

| Token | Hex | RGB | Role / Usage | Confidence | Evidence |
|-------|-----|-----|--------------|-----------|----------|
| --bg-primary | #ffffff | rgb(255,255,255) | Page background | high | css-variables.json light --background |
| --bg-secondary | … | … | Card/section bg | … | home.computed.json count=… |
| --text-primary | … | … | Body + headings | … | … |
| --text-secondary | … | … | Muted text/labels | … | … |
| --accent | … | … | Links, primary button fill | … | … |
| --accent-hover | … | … | Accent :hover | … | pricing.states.json |
| --border | … | … | Card borders, dividers | … | … |
| --success / --error / --warning | … | … | Status | … | … |
| --overlay | … | … | Modal backdrop (incl. α) | … | … |
| --selection | … | … | ::selection background | … | home.pseudo.json ::selection |
```
Add every distinct color appearing more than once. Resolve `currentColor`/`inherit` to the concrete painted value from the archetype.

### 4.2 Gradients (MANDATORY — sourced from `backgroundImage`)

Gradients live in the `backgroundImage` property of computed archetypes (and authored rules). Parse each `linear-gradient(...)`, `radial-gradient(...)`, `conic-gradient(...)` into type + geometry + ordered stops. Capture gradient **text** (`-webkit-background-clip:text` + `-webkit-text-fill-color:transparent`) here too.

```markdown
## Gradients

| Token | Type | Angle / Shape | Color Stops (color @pos) | Applied to | Confidence | Evidence |
|-------|------|---------------|--------------------------|-----------|-----------|----------|
| --grad-primary-btn | linear | 135deg | #6366f1 @0%, #8b5cf6 @100% | primary button fill | high | home.computed.json button count=… backgroundImage |
| --grad-hero | radial | circle at 50% 0% | rgba(99,102,241,.4) @0%, transparent @60% | hero glow | med | home.computed.json |
| --grad-text-headline | linear (clip:text) | 90deg | #fff @0%, #94a3b8 @100% | gradient headline text | … | home.computed.json -webkit-background-clip |
```
Preserve stop order and explicit positions exactly as authored. If a button's fill is a gradient, this token feeds an assertions.json `backgroundImage` check (§5).

### 4.3 Typography (incl. variable-font axes)

```markdown
## Typography

| Level | Font Stack | Size | Weight | Line-Height | Letter-Spacing | Other | Color token | Evidence |
|-------|-----------|------|--------|-------------|----------------|-------|-------------|----------|
| Display | "Inter", system-ui, sans-serif | 64px | 800 | 1.05 | -0.02em | — | --text-primary | home.computed.json count=… |
| H1 | … | … | … | … | … | textTransform/textShadow | … | … |
| H2 / H3 / H4 | … | … | … | … | … | … | … | … |
| Body / Body Small / Caption / Label | … | … | … | … | … | … | … | … |
| Button / Nav Link | … | … | … | … | … | … | … | … |
| Code | "…mono…" | … | … | … | … | fontFeatureSettings | … | fonts.json |

### Font families (source + delivery)
| Family | Weights observed | Style(s) | Source | Self-hosted path |
|--------|------------------|----------|--------|------------------|
| Inter | 400,500,600,700,800 | normal | self-hosted woff2 | 02-extraction/assets/fonts/inter-*.woff2 |

### Variable-font axes (fvar)
| Family | Axis tag | Range | Default | Used values (fontVariationSettings) | Evidence |
|--------|----------|-------|---------|--------------------------------------|----------|
| Inter | wght | 100..900 | 400 | 'wght' 620 (nav), 'wght' 800 (display) | fonts.json fvar + home.computed.json |
| … | opsz / slnt / GRAD | … | … | … | … |
```
Cross-reference each rendered `fontFamily` (archetype) against `fonts.json` to confirm the actual loaded family and to capture `fontVariationSettings`, `fontOpticalSizing`, `fontFeatureSettings`.

### 4.4 Spacing scale

```markdown
## Spacing Scale

| Token | Value | Frequency (Σcount) | Routes | Where observed | Confidence | Evidence |
|-------|-------|--------------------|--------|----------------|-----------|----------|
| --space-1 | 4px | … | … | icon↔label gap | … | …gap/padding archetypes |
| --space-2 | 8px | … | … | inline gap | … | … |
| --space-4 | 16px | … | … | card padding (base rung) | high | … |
| … | … | … | … | … | … | … |
```
Derive rungs by clustering per-side `padding*`/`margin*`/`rowGap`/`columnGap` values from the archetypes; the highest-Σcount rung is the base.

### 4.5 Border-radius scale

```markdown
## Border-Radius Scale

| Token | Value | Σcount | Where used | Confidence | Evidence |
|-------|-------|--------|-----------|-----------|----------|
| --radius-sm | 6px | … | chips/badges | … | … |
| --radius-md | 8px | … | buttons/inputs (base) | high | … |
| --radius-lg | 16px | … | cards/panels | … | … |
| --radius-full | 9999px | … | avatars/pills | … | … |
```
Note asymmetric radii (`borderTopLeftRadius` ≠ others) as their own row with the full 4-value syntax.

### 4.6 Shadows (layered + inset)

```markdown
## Shadows

| Token | Full box-shadow value (all layers) | Inset? | Where used | Confidence | Evidence |
|-------|------------------------------------|--------|-----------|-----------|----------|
| --shadow-sm | 0 1px 2px rgba(0,0,0,.06) | no | buttons/badges | … | … |
| --shadow-md | 0 1px 3px rgba(0,0,0,.12), 0 1px 2px rgba(0,0,0,.24) | no | cards (base) | high | … |
| --shadow-lg | 0 10px 25px -5px rgba(0,0,0,.2), 0 8px 10px -6px rgba(0,0,0,.1) | no | hover/modal | … | … |
| --shadow-inset | inset 0 1px 0 rgba(255,255,255,.1) | yes | input top-edge | … | … |
```
Preserve every comma-separated layer and `inset` keyword verbatim from the computed `boxShadow`. Capture `textShadow` here too if present (separate row labeled text).

### 4.7 Effects / backdrop-filter

```markdown
## Effects & Backdrop-Filter

| Token | Property | Value | Where used | Confidence | Evidence |
|-------|----------|-------|-----------|-----------|----------|
| --blur-glass | backdropFilter | blur(12px) saturate(180%) | sticky nav glass | … | home.computed.json backdropFilter |
| --filter-img | filter | grayscale(1) contrast(1.1) | logo cloud | … | … |
| — | mixBlendMode / isolation | … | overlay blend | … | … |
| — | clipPath / maskImage | … | shaped section | … | … |
```

### 4.8 Motion (durations / easings / @keyframes)

```markdown
## Motion

### Transitions
| Token | Property | Duration | Easing (resolved cubic-bezier) | Delay | Where | Evidence |
|-------|----------|----------|--------------------------------|-------|-------|----------|
| --t-fast | background-color,color | 150ms | cubic-bezier(.4,0,.2,1) | 0ms | button/link hover | …states/computed |
| --t-card | transform,box-shadow | 250ms | cubic-bezier(.16,1,.3,1) | 0ms | card hover lift | … |

### @keyframes (from all-styles.json)
| Name | Stops → declarations | Used by (animationName / duration / iteration / direction / fill) | Evidence |
|------|----------------------|-------------------------------------------------------------------|----------|
| fadeUp | 0%{opacity:0;transform:translateY(8px)} 100%{opacity:1;transform:none} | .reveal — 600ms ease-out 1 forwards | all-styles.json @keyframes |
```
Resolve named easings to explicit `cubic-bezier(...)` (e.g. `ease` → `cubic-bezier(.25,.1,.25,1)`). Pull `@keyframes` bodies verbatim from `all-styles.json`.

### 4.9 States (hover / focus / active deltas)

```markdown
## States

| Element | State | Property → delta (base → state) | Evidence |
|---------|-------|----------------------------------|----------|
| Primary button | :hover | backgroundImage --grad-primary-btn → brighter stops; transform none → translateY(-1px) | home.states.json |
| Primary button | :active | transform → translateY(0) scale(.98) | … |
| Text link | :hover | color --accent → --accent-hover; text-decoration none → underline | … |
| Input | :focus-visible | boxShadow none → 0 0 0 3px rgba(accent,.4); border → --accent | … |
```
Source from `{page}.states.json` deltas first; fall back to authored `:hover/:focus/:active` rules in `all-styles.json` when no forced-state delta exists. Emit **only the properties that changed**.

### 4.10 Layout + measured breakpoints

```markdown
## Layout

| Pattern | Value | Evidence |
|---------|-------|----------|
| Max content width | … | layout.json rect of main container |
| Grid system | e.g. CSS grid 12-col / flex | layout.json gridTemplateColumns |
| Nav height / position | … / sticky | layout.json + computed |
| Sidebar width / position | … | … |
| Content padding (desktop/mobile) | … / … | … |
| Card grid cols (desktop/tablet/mobile) | … / … / … | layout.json @media |

## Breakpoints (MEASURED — real conditionText, not 768/375 guesses)

| Name | Real condition | Source | Key layout changes |
|------|----------------|--------|--------------------|
| mobile | (max-width: 640px) | layout.json @media conditionText | grid 3→1, nav→hamburger |
| tablet | (min-width: 641px) and (max-width: 1024px) | … | grid 3→2 |
| desktop | (min-width: 1025px) | … | full grid |
```
Use the **actual `@media`/`@container` `conditionText`** from `{page}.layout.json` — never the viewport-key guesses.

### 4.11 Assets (downloaded paths)

```markdown
## Assets

| Asset | Type | Intrinsic dims | Downloaded path | srcset / variants | Evidence |
|-------|------|----------------|-----------------|-------------------|----------|
| logo | svg (inline) | 120×32 | 02-extraction/assets/svg/logo.svg | — | assets.json hash=… |
| hero | img | 1600×900 | 02-extraction/assets/img/hero-<hash>.webp | 800w,1600w | assets.json |
| favicon | ico | 32×32 | 02-extraction/assets/img/favicon.ico | — | … |
```
Reference ONLY downloaded files from `assets.json`. Never list picsum/pravatar/placeholder URLs — if a download failed, mark the row `~MISSING (download failed)` and note it.

### 4.12 Theme tokens (light / dark)

```markdown
## Theme Tokens

| Token (original var name) | Light | Dark | Evidence |
|---------------------------|-------|------|----------|
| --background | #ffffff | #0a0a0a | css-variables.json themes.light / themes.dark |
| --foreground | #0a0a0a | #ededed | … |
| --accent | #6366f1 | #818cf8 | … |
```
Take both columns straight from `css-variables.json` `themes.light` / `themes.dark`. Preserve the **original variable names** verbatim so Build wires the same theme switch (`[data-theme="dark"]` / `prefers-color-scheme`). State which theme is the default (matched to the recon `recon.json` theme order).

### 4.13 Design guardrails / do's-and-don'ts (reproduce the FEEL, not just the values)

A short bullet list of the rules that keep a new page on-brand — the constraints an agent must respect so it reproduces the *feel*, not just pastes token values. **Derive each rule from the tokens you actually inferred** (do not template generic advice): if there is one dominant accent, the rule is "max one accent color"; if text is `#0a0a0a` not `#000000`, the rule is "near-black text, never pure `#000`"; cap shadow opacity at the largest α you actually saw; etc. Aim for 6–12 concrete do/don't lines.

```markdown
## Design Guardrails

**Do**
- Use exactly **one** accent (`--accent`) for primary actions and links; everything else is neutral.
- Text is **near-black** `#0a0a0a` / near-white `#ededed` — never pure `#000` or `#fff` on a colored surface.
- Snap all spacing to the scale ({list rungs}); never hand-pick off-scale gaps.
- Corners follow the radius scale ({rungs}); pills use `--radius-full` only.
- Keep shadow opacity ≤ {max α observed}; layer at most {N} shadow layers.
- Transitions stay ≤ {max ms observed} on `{properties}`; respect `prefers-reduced-motion`.

**Don't**
- Don't introduce a second accent hue or a gradient not in the Gradients table.
- Don't use drop shadows on flat/dense surfaces if the source uses borders for separation.
- Don't add border-radius to elements the source kept square.
- Don't invent type sizes/weights outside the Typography scale.
```

### 4.14 Agent Prompt Guide (END — how to USE this file)

Close DESIGN.md with a short, self-contained block that tells a coding agent how to build a new page or component **in this design language using only this file**. This makes DESIGN.md portable: paste it (or `@DESIGN.md` it) into any agent session and the agent knows the rules of engagement. Keep it ~8–14 lines, concrete, and grounded in the sections above.

```markdown
## Agent Prompt Guide

You are building a new page/component in **{App Name}**'s design language. Use ONLY this file as the source of truth.

1. **Set the mood first.** Re-read **Visual Theme** — match that atmosphere before picking any value.
2. **Use tokens, not raw values.** Pull every color/space/radius/shadow/type value from the token tables by its semantic role (e.g. primary button → `--accent` fill + `--radius-md` + `--shadow-sm`). Reuse the **original variable names** so theming keeps working.
3. **Honor the guardrails.** Apply every Do/Don't in Design Guardrails — they encode the feel.
4. **Type with the scale.** Headings/body/buttons use the Typography levels and the variable-font axes exactly as listed.
5. **Theme-aware.** Wire light/dark from the Theme Tokens table (`[data-theme]` / `prefers-color-scheme`); never hardcode a single theme's hex.
6. **Motion + states.** Add hover/focus/active per the States table and durations/easings per Motion; respect `prefers-reduced-motion`.
7. **Responsive.** Use the MEASURED breakpoints (real `conditionText`), not 768/375 guesses.
8. **Assets.** Reference only the listed asset paths; never substitute placeholder services.
9. **Stay in lane.** If a value you need isn't here, pick the nearest token rung and the closest semantic role — do NOT invent a new color, size, or radius outside the scales.
```

---

## 5. Output File 2 — `03-design-spec/assertions.json`

This is the **style-assertion half of the gate** (contract §5). `scripts/assert-styles.mjs` loads this array, opens the built clone, and for each entry runs `getComputedStyle(document.querySelector(selector))[camelCaseProp]` and compares to `expected` (colors normalized to `rgb()`; numerics ±1px / ±0.01em). **Any mismatch fails the gate** — so every entry must be both *real* (selector exists in the built clone) and *measurable* (prop is one `getComputedStyle` returns concretely).

### 5.1 Shape (exactly this — consumed verbatim)

```json
[
  { "selector": ".btn-primary", "prop": "backgroundImage", "expected": "linear-gradient(135deg, rgb(99,102,241) 0%, rgb(139,92,246) 100%)" },
  { "selector": ".btn-primary", "prop": "color", "expected": "rgb(255,255,255)" },
  { "selector": ".btn-primary", "prop": "cursor", "expected": "pointer" },
  { "selector": "h1", "prop": "fontSize", "expected": "64px" },
  { "selector": "h1", "prop": "fontWeight", "expected": "800" },
  { "selector": ".card", "prop": "borderRadius", "expected": "16px" },
  { "selector": ".card", "prop": "boxShadow", "expected": "rgba(0, 0, 0, 0.12) 0px 1px 3px 0px, rgba(0, 0, 0, 0.24) 0px 1px 2px 0px" },
  { "selector": "body", "prop": "backgroundColor", "expected": "rgb(255,255,255)" }
]
```

Each object has EXACTLY three keys: `selector`, `prop`, `expected`. No comments, no extra keys — `assert-styles.mjs` reads them positionally.

### 5.2 How to pick **selectors** that exist in the built clone
- Prefer **stable, structural selectors** that the architecture/build will reproduce: element tags (`body`, `h1`, `h2`, `a`), and the semantic class names you saw in `{page}.dom.html` that Build is told to keep (e.g. `.btn-primary`, `.card`, `.nav`). Read `{page}.dom.html` to confirm the class/tag actually appears.
- **Avoid** framework-hashed classes (`.css-1ab2c3`, `._next_xyz`, Tailwind atomic stacks) — the clone won't reproduce those exact names. If the original only has hashed classes, assert on the **tag or role** instead (`button`, `nav a`, `header`).
- Use selectors that resolve to **exactly one well-defined archetype** so the computed value is unambiguous. One representative element per token.
- Keep the list to the **highest-signal tokens** (~20–60 entries), not every value. Cover: key brand colors (bg, text-primary, accent), primary/secondary **button gradient via `backgroundImage`**, headline + body `fontSize`/`fontWeight`, the base + card `borderRadius`, the card `boxShadow`, and the primary interactive `cursor: pointer`.

### 5.3 How to pick **props** `getComputedStyle` returns concretely
Use the camelCase property names the gate already checks (contract §5): `color`, `backgroundColor`, `backgroundImage`, `fontSize`, `fontWeight`, `letterSpacing`, `lineHeight`, `borderRadius`, `boxShadow`, `cursor`, `transition`.
- **Colors** → write `expected` as `rgb(r,g,b)` or `rgba(r,g,b,a)` (the asserter normalizes, but matching the returned form avoids ambiguity).
- **`backgroundImage` (gradients)** → write the value in the **computed serialization** the browser returns: `linear-gradient(135deg, rgb(99, 102, 241) 0%, rgb(139, 92, 246) 100%)` — angle first, rgb stops, explicit `%`. Do NOT use hex inside `backgroundImage` (getComputedStyle returns rgb). If a button fill is a gradient, assert `backgroundImage`, not `backgroundColor`.
- **`boxShadow`** → use the computed order the engine returns (`color offset-x offset-y blur spread`, e.g. `rgba(0, 0, 0, 0.12) 0px 1px 3px 0px`), comma-joining each layer.
- **Numerics** (`fontSize`, `borderRadius`, `letterSpacing`, `lineHeight`) → `px`/`em` strings; the gate tolerances are ±1px / ±0.01em, so round to the rendered value.
- Pull each `expected` from the **same artifact the token cited** (authoritative order §2): authored CSSOM value if present, else the computed archetype value. Never invent an `expected` you didn't read.

---

## 6. Evidence & anti-hallucination rules (contract §7.5–7.6)

- Every token row cites the artifact it derived from in its `Evidence` column. No citation = not allowed.
- When sources conflict, take the higher per §2 and say which won.
- Never invent a value. If a value cannot be read from any artifact, write `~` + estimate, set confidence `low`, and note "no artifact — estimated."
- Do not editorialize, do not recommend. This is a specification, not advice.
- Do not invent components or tokens not present in the extraction data.
- If `02-extraction/` is empty or unreadable (extraction never ran), do not fabricate a design system — emit `<promise>BLOCKED: 02-extraction artifacts missing</promise>` and stop.

---

## 7. Outputs (exact paths — contract §1) and completion

Write EXACTLY these two files, nothing else:

- `03-design-spec/DESIGN.md` — the portable best-practice design file (§4): opens with **Visual Theme** (§4.0), then all twelve mandatory token sections (§4.1–4.12) filled with no blank cells, hex+rgb for every color, units on every numeric, evidence on every row, and closes with **Design Guardrails** (§4.13) + **Agent Prompt Guide** (§4.14). Self-contained — readable in another repo with no access to `02-extraction/`.
- `03-design-spec/assertions.json` — valid JSON array of `{selector, prop, expected}` objects covering the highest-signal tokens (§5).

### Completion checklist
- [ ] Read ALL of `02-extraction/` (every fragment + the 4 shared files) before writing.
- [ ] DESIGN.md opens with a concrete **Visual Theme** paragraph and closes with **Design Guardrails** + **Agent Prompt Guide** (portable, self-contained).
- [ ] Tokens inferred by Σ`count` + cross-route confidence, not per-element dumps.
- [ ] Colors: hex AND rgb. Gradients: type + angle/shape + ordered stops from `backgroundImage`.
- [ ] Typography includes variable-font `fvar` axes from `fonts.json`.
- [ ] Shadows preserve every layer + `inset`. Effects include `backdropFilter`.
- [ ] Motion easings resolved to `cubic-bezier(...)`; `@keyframes` copied from `all-styles.json`.
- [ ] Breakpoints use real `conditionText`, not 768/375 guesses.
- [ ] Assets reference only downloaded paths from `assets.json`.
- [ ] Theme tokens keep original variable names; light + dark both filled.
- [ ] `assertions.json` selectors exist in `{page}.dom.html` (no hashed classes); props are `getComputedStyle`-returnable; button gradients assert `backgroundImage` in computed rgb serialization.
- [ ] Set this task's flag in `status.json`.

End with `<promise>CONTINUE</promise>` (or `<promise>BLOCKED: reason</promise>` if extraction artifacts are missing).
