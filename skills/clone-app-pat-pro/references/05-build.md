# Stage 5: Build Reference (5a Foundation + 5b Page)

Build is **split into two sub-stages** with a hard sequencing rule (see contract §2):

- **5a — Build Foundation** runs **alone**, before any page agent. It is the **SOLE author** of the global design tokens / CSS custom properties, the layout shell, the nav, and the shared components. Nothing else writes those files.
- **5b — Build Page** runs **in parallel, one agent per route**. Each page agent **consumes** the foundation tokens and **never redefines** them. It implements a single route to match its extracted fragment.

You have never seen the live app. Work strictly from the artifacts below — never generate UI from memory. The mission is pixel-for-pixel ownership of the target, proven later by a measured pixel diff (contract §3 fidelity targets, §5 gate). Build to be measured, not eyeballed.

**Hard rule for BOTH sub-stages: `npm run build` must exit 0.** The orchestrator runs it as a regression gate after foundation, after pages, and after every fix cycle (contract §5, §6). A build that does not compile is a `HARD-BLOCKER` — emit `<promise>BLOCKED: build error — {message}</promise>` and stop. Never leave the tree in a non-compiling state.

---

## Inputs (read ALL before writing a line of code)

| File | What it gives you |
|------|-------------------|
| `03-design-spec/DESIGN.md` | Authoritative tokens: colors, **Gradients table**, typography (incl. variable-font axes), spacing scale, radius scale, layered/inset shadows, **Effects/backdrop-filter**, motion (durations/easings/keyframes), states (hover/focus/active), measured breakpoints, asset paths, light/dark theme tokens |
| `04-architecture/file-tree.md` | Every file you must create, and where |
| `04-architecture/component-map.md` | Component hierarchy and nesting |
| `02-extraction/css-variables.json` | Theme scopes (`:root`, `[data-theme]`, `.dark`, `prefers-color-scheme`) — the raw var union per theme |
| `02-extraction/fonts.json` | `@font-face` rules + loaded-font set + variable-font `fvar` axes |
| `02-extraction/assets.json` | Manifest of DOWNLOADED bytes (hash, ext, intrinsic dims, srcset) |
| `02-extraction/assets/` | The actual downloaded files: `img/`, `svg/`, `fonts/` |
| `02-extraction/fragments/{page}.*` | **5b only:** per-route `.computed.json`, `.pseudo.json`, `.states.json`, `.layout.json`, `.dom.html` |
| `01-recon/screenshots/{page}--{viewport}.png` | Visual reference (the diff baseline). Open before building each page |

Page slug rule and viewport keys are in contract §1 (`/` → `home`; viewports `desktop` 1920×1080, `tablet` 768×1024, `mobile` 375×667).

---

# Stage 5a — BUILD FOUNDATION (runs alone, sole author of global tokens)

You are the **BUILD-FOUNDATION** agent. You run **before** any page agent and you are the **only** agent that writes the global token file, the layout shell, the nav, and the shared components. Page agents read what you produce. Get this exactly right — every page inherits your foundation.

Build in this exact order. Skipping ahead creates broken dependencies.

## 5a.1 — Scaffold the project

Create the project skeleton in `OUTPUT_DIR` per `04-architecture/file-tree.md`, matching the stack detected in recon (`recon.json` framework fingerprint, contract §3-I).

- **Next.js + Tailwind:** App Router. `app/layout.tsx`, `app/globals.css`, `tailwind.config.ts`, `next.config.js`. Use `next/font/local` for self-hosted fonts (NOT `next/font/google` — fonts are self-hosted from extracted bytes). Server components by default; add `"use client"` only where interaction needs it.
- **Vite + CSS:** `index.html`, `src/main.{ts,tsx}`, `src/styles/globals.css` imported once at entry, `public/` for assets and fonts. Whatever component layer the architecture specifies (React/Vue/vanilla), tokens live in one global stylesheet.

Confirm the scaffold compiles (`npm install && npm run build`) before adding anything.

## 5a.2 — Design tokens / CSS custom properties (THE SINGLE SOURCE OF TRUTH)

Author **every** token from `DESIGN.md` as a CSS custom property in the global stylesheet (`app/globals.css` or `src/styles/globals.css`). This file is the **single source of truth** for all values. Page agents reference these variables — they never declare new ones.

```css
:root {
  /* Colors — every color token from DESIGN.md */
  --color-bg: #ffffff;
  --color-text: #1a1a1a;
  /* ... */

  /* Gradients — from the design-system Gradients table / backgroundImage tokens */
  --gradient-hero: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
  /* preserve EXACT type (linear/radial/conic), angle/shape, and every stop+position */

  /* Typography — incl. variable-font axes */
  --font-body: "InterVar", sans-serif;
  --font-size-base: 16px;
  --line-height-base: 1.5;
  --letter-spacing-tight: -0.02em;

  /* Spacing scale (per-side values come from fragments at build time, not here) */
  --space-2: 8px;

  /* Radius scale (asymmetric corners stay asymmetric) */
  --radius-md: 8px;

  /* Shadows — layered and inset preserved verbatim */
  --shadow-card: 0 1px 2px rgba(0,0,0,.06), 0 8px 24px rgba(0,0,0,.10);
  --shadow-inset: inset 0 1px 0 rgba(255,255,255,.08);

  /* Effects */
  --backdrop-blur: blur(12px) saturate(1.4);

  /* Motion */
  --transition-base: 200ms cubic-bezier(.4,0,.2,1);
}
```

Token rules:
- **Gradients are tokens.** They come from the `backgroundImage` values in extraction. Copy the full stop list, exact angle/shape, color-space, and stop positions. Do not approximate a multi-stop gradient with two stops.
- **Shadows stay layered/inset.** A comma-separated multi-shadow keeps every layer. Inset shadows keep `inset`.
- **Themes.** Reproduce every theme scope from `css-variables.json`: `:root` (light), plus `.dark` / `[data-theme="dark"]` and/or `@media (prefers-color-scheme: dark)`. Same variable names, theme-specific values — page code is theme-agnostic because it only reads var names.
- **Variable fonts.** Expose axes (e.g. `--wght: 600;`) and apply via `font-variation-settings` where the design uses non-named weights/optical sizing.
- **Tailwind:** ALSO map every token into `tailwind.config.ts` `theme.extend` (colors, fontFamily, fontSize, spacing, borderRadius, boxShadow, backgroundImage, transitionTimingFunction) — referencing the CSS vars (`colors: { bg: "var(--color-bg)" }`) so the vars remain the source of truth. Use utility classes in JSX; reach for `@layer utilities` / arbitrary values only for one-off extracted values.
- **Vite/CSS:** reference `var(--token)` exclusively. Never hardcode a hex or px in component code.

## 5a.3 — Self-host the real fonts

Fonts are **self-hosted** from the downloaded bytes — never a Google Fonts CDN link, never a system fallback substitution.

1. Copy the woff2/woff/ttf files from `02-extraction/assets/fonts/` into the project (`public/fonts/` for Vite; `app/fonts/` or `public/fonts/` for Next).
2. Write `@font-face` rules in the global stylesheet matching `fonts.json` exactly: `font-family`, `font-weight` (use the real range for variable fonts, e.g. `100 900`), `font-style`, `font-display: swap`, and `src: url(...) format("woff2")`.
3. **Next.js:** prefer `next/font/local` pointing at the copied files (it self-hosts and gives a stable class), or hand-written `@font-face` in `globals.css`. Either way the bytes ship from the repo.
4. Reference families only through the `--font-*` tokens.

## 5a.4 — Copy in the downloaded assets

Copy `02-extraction/assets/img/`, `svg/` into the project's static dir (`public/` for both Next and Vite). Reference real files by their extracted paths. Record intrinsic dimensions from `assets.json` and set width/height (or aspect-ratio) to prevent layout shift. **Inline SVGs** from extraction keep their full `outerHTML` — do not redraw or simplify them. **Never use picsum/pravatar or any placeholder** when a real asset exists; the only exception is a download that genuinely failed (log it in `05-build/build-log.md`).

## 5a.5 — Layout shell

Build the root layout: outer wrapper, nav slot, `<main>`, footer slot — using semantic HTML (`<nav> <main> <header> <footer> <section>`). Apply the correct background, text color, and body font from tokens. Structure only, no page content. Set the stacking context / z-index baseline per `{page}.layout.json` so positioned children layer correctly later.

## 5a.6 — Navigation

Build the TopNav and/or Sidebar that appear on every route. These establish the visual frame and must be exact before pages depend on them. Apply backdrop-filter / blur, gradients, and shadows from tokens. Implement nav hover/focus/active states (see 5a.8).

## 5a.7 — Shared components

Build every reusable component used across multiple pages: buttons, cards, inputs, badges, avatars, modals, dropdowns, etc., per `component-map.md`. Each consumes tokens only. Give each its documented variants and states.

## 5a.8 — States and effects (foundation-level)

For nav and every shared component, implement `:hover`, `:focus-visible`, and `:active` **exactly** per the States section of `DESIGN.md` (which derives from the extracted `.states.json` deltas):
- Apply only the properties that actually change in the state delta (e.g. hover changes `background` and `box-shadow` only — don't invent a transform).
- Every clickable element gets `cursor: pointer`.
- Focus rings must be visible for keyboard nav (`:focus-visible`).
- Use the exact transition tokens on the exact properties that animate.
- Implement gradients (from `backgroundImage` tokens), layered/inset shadows, and `backdrop-filter` here so shared surfaces match before pages compose them.

## 5a.9 — Verify and complete (5a)

```bash
npm run build   # MUST exit 0
```

Fix all errors (warnings OK). Write `05-build/build-log.md` listing every file created with a one-line description. Set the foundation flag in `status.json`. End with `<promise>CONTINUE</promise>` (or `<promise>BLOCKED: …</promise>` if the build will not compile).

---

# Stage 5b — BUILD PAGE (runs in parallel, one agent per route)

You are a **BUILD-PAGE** agent for **ONE** route, `PAGE={PAGE}`. The foundation (tokens, layout, nav, shared components) **already exists**. Your job is to implement this single route so it matches its extracted fragment pixel-for-pixel.

**Consume foundation tokens ONLY. Never redefine a token, never edit the global stylesheet, never touch another route's file.** If you need a value that is genuinely missing from the tokens, log it in `05-build/build-log.md` and use the closest existing token — do not add a new global var (that would race with sibling page agents and with 5a's sole-author rule).

## 5b.1 — Study the fragment

Read this route's `02-extraction/fragments/{page-slug}.*`:
- `{page}.dom.html` — the cleaned structure to reproduce.
- `{page}.computed.json` — per-archetype computed styles incl. **per-side** padding/margin, asymmetric border-radius, exact `getBoundingClientRect` pixel geometry.
- `{page}.pseudo.json` — `::before` / `::after` / `::placeholder` / `::marker` / `::selection` content and styles.
- `{page}.states.json` — `:hover` / `:focus` / `:active` deltas for this route's elements.
- `{page}.layout.json` — flex/grid, real breakpoints (`@media`/`@container` conditionText), stacking contexts.
- Open `01-recon/screenshots/{page-slug}--desktop.png` (and tablet/mobile) as the visual reference.

## 5b.2 — Build the route

Compose the page from foundation layout + shared components, section by section, top to bottom, matching the fragment:

- **Spacing per-side.** Apply the exact paddingTop/Right/Bottom/Left and margins from `.computed.json`. Never collapse a per-side value into a symmetric shorthand if the original is asymmetric. Match measured rects.
- **Gradients.** Use the gradient tokens for backgrounds that have one; for a page-unique gradient present only in this fragment's `backgroundImage`, apply it inline on the element (still reference color tokens for stops where they map) — do NOT create a global token.
- **Pseudo-elements.** Implement every `::before`/`::after` etc. from `.pseudo.json` with their exact content, geometry, transform, mask, clip-path.
- **States.** Implement this route's `:hover`/`:focus-visible`/`:active` deltas exactly; apply only properties that change; correct transition token on the correct property; `cursor: pointer` on every interactive element.
- **Real assets.** Use the downloaded files copied in by 5a (and `assets.json` intrinsic dims). **Never picsum/pravatar/placeholder.**
- **Responsive.** Use the **measured** breakpoints from `.layout.json` (not the 768/375 guess) for tablet/mobile layout changes.
- **Mock data:** if the route needs content, hardcode realistic data matching the app type in one file (`lib/mock-data.ts` or similar) — do not scatter arrays.

## 5b.3 — Periodic visual check

Every few sections:

```bash
$BROWSER_CMD open http://localhost:3000/{route}
$BROWSER_CMD screenshot
```

Compare against `01-recon/screenshots/{page-slug}--{viewport}.png`. Fix obvious drift now.

## 5b.4 — Verify and complete (5b)

```bash
npm run build   # MUST exit 0
```

The build must compile — your route cannot be the file that breaks the regression gate. Append your files to `05-build/build-log.md`, set this page's flag in `status.json`, end with `<promise>CONTINUE</promise>` (or `<promise>BLOCKED: …</promise>`).

---

## Rules (non-negotiable, BOTH sub-stages)

- Match `DESIGN.md` and the fragment values **EXACTLY**. No rounding 14px→16px, no `ease` for `ease-in-out`, no 2-stop approximation of a 5-stop gradient.
- **5a owns tokens; 5b consumes tokens.** Page agents never write the global stylesheet or `tailwind.config.ts` token map.
- Fonts are **self-hosted** from `02-extraction/assets/fonts/`. No CDN, no system-font substitution.
- Assets are the **real downloaded files**. Never picsum/pravatar/placeholder (log a genuine download failure instead).
- Gradients come from `backgroundImage` tokens; layered/inset shadows and `backdrop-filter` reproduced verbatim.
- Every clickable element: `cursor: pointer`. Every documented hover/focus/active state implemented, on the right property, with the right transition token.
- Semantic HTML throughout.
- **`npm run build` must exit 0.** The orchestrator runs it as a regression gate (contract §5, §6). Never commit a non-compiling tree.
- Never leave a TODO in code — document blockers in `05-build/build-log.md`. Never invent UI from memory.

## Output

- All code written into `OUTPUT_DIR` per `file-tree.md`.
- `05-build/build-log.md` — every file created/edited + one-line description; any logged asset/token gaps.

<promise>CONTINUE</promise>
