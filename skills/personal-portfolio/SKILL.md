---
name: personal-portfolio
description: >
  Tactile Brutalist + High-End Editorial personal portfolio SPA with React 19,
  TypeScript 6 strict, Vite 6, Tailwind CSS v4 CSS-first @theme, pnpm.
  Covers complete lifecycle from scaffold to shipping: kinetic typography, hash-based
  routing, import.meta.glob content ingestion, dual-theme (night/day) design system,
  WCAG AAA accessibility, component-driven digital installation. Use when building
  a distinctive, anti-generic portfolio or personal site with React + Vite + Tailwind v4.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
license: MIT
version: 3.0.0
---

# The Engineered Soul — Portfolio Master Skill (v3.0.0)

**One-Shot Prevention:** This skill was distilled from a real build cycle that migrated a 1265-line JSX + 4411-line CSS monolith into a clean, component-driven TypeScript + Tailwind v4 installation. It encodes both the deep architectural thinking (the "why") and the practical remediation lessons (the "what went wrong and how we fixed it"). Skipping any section creates rework, visual regression, or accessibility failure. This document is the absolute single source of truth.

---

## 1. Project Identity & Non-Negotiables

### The Dual-Thesis
The aesthetic is a deliberate collision of two extremes. Every design decision must answer: *"Does this serve the tension between the mathematical and the emotional, or does it safely retreat to the middle?"*
- **Tactile Brutalism (The Machine):** Visible structure, 1px borders, `0px` border-radius, mono utility type, high contrast, no decoration without function, raw terminal aesthetics.
- **High-End Editorial (The Soul):** Cormorant Garamond serif headlines, extreme whitespace, cinematic motion, asymmetric spreads, human textures, kinetic typography.

### The "AI Slop" Rejection List (Strictly Forbidden)
- Purple gradients on white backgrounds or safe neutral palettes.
- Safe Inter/Roboto-only font pairings without distinct typographical hierarchy.
- Predictable card grids, hero sections, Bootstrap-like aesthetics, or template UI.
- **Any border radius other than `0px`** (See Section 3.3).
- Generic stock photography, placeholder aesthetics, or uncurated layouts.
- External UI libraries (No shadcn/ui, No Radix, No Framer Motion, No React Router). All components are bespoke.

### Mandatory Six-Phase Workflow
Every change to this codebase MUST follow:
1. **ANALYZE**: Deep requirement mining; trace component tree, data flow, and CSS cascade. Never assume.
2. **PLAN**: Write down every file change before touching code.
3. **VALIDATE**: Present the plan for explicit user approval before implementing.
4. **IMPLEMENT**: Write code following the patterns in this document. Touch only what is necessary.
5. **VERIFY**: Run `pnpm typecheck && pnpm build` after every change. Verify visually and functionally.
6. **DELIVER**: Confirm zero errors, zero warnings, and provide complete handoff documentation.
No phase can be skipped. No code is written without explicit user confirmation.

---

## 2. Tech Stack & Environment

| Layer | Technology | Version | Purpose |
|---|---|---|---|
| Framework | React | ^19.0.0 | Concurrent rendering, StrictMode |
| Language | TypeScript | ^6.0.0 | Strict typing, erasable syntax only |
| Build Tool | Vite | ^6.3.0 | Zero-config HMR, `import.meta.glob` |
| Styling | Tailwind CSS | ^4.1.0 | CSS-first `@theme`, no JS config |
| Package Manager | pnpm | >= 9 | Workspace support, strict resolution |
| Fonts | Google Fonts | — | Cormorant Garamond, IBM Plex Mono, Inter |

### Critical TypeScript Settings (`tsconfig.json`)
- `strict: true`
- `erasableSyntaxOnly: true` — **NON-NEGOTIABLE**. Rejects `enum`, `namespace`, and parameter properties. Always use union types (e.g., `icon: 'mail' | 'linkedin' | 'github'`).
- `noUncheckedIndexedAccess: true` — Makes array/object index access return `T | undefined`. You must handle the `undefined` case explicitly, or use a non-null assertion (`!`) *only* when logically guaranteed by bounds checking (e.g., `if (index < arr.length) arr[index]!`).
- Path alias: `@/*` → `./src/*`

### Vite Configuration (`vite.config.ts`)
- `base: './'` — Required for GitHub Pages relative path resolution.
- `@tailwindcss/vite` plugin must be present in `plugins: []`.
- Do not inject legacy PostCSS or `tailwind.config.js`. All tokens are in `src/styles/index.css`.

---

## 3. The Design System (Complete Code-First)

There is NO `tailwind.config.js`. All design tokens live in `src/styles/index.css` inside `@theme`. Do not deviate.

### 3.1 Full Tailwind v4 `@theme` Block
```css
@import "tailwindcss";

@theme {
  /* Grid Unit — the mathematical backbone */
  --unit: 28px;
  --spacing-grid: 28px;
  --spacing-section: 104px;

  /* Colors — Dark Theme (default) */
  --color-ink: #07080d;
  --color-ink-light: #15151b;
  --color-surface: #11131d;
  --color-surface-elevated: #1a1c2e;
  --color-text: #ffffff;
  --color-text-secondary: rgba(255, 255, 255, 0.68);
  --color-text-muted: rgba(255, 255, 255, 0.52);
  --color-text-faint: rgba(255, 255, 255, 0.38);
  --color-border: rgba(255, 255, 255, 0.13);
  --color-border-strong: rgba(255, 255, 255, 0.24);
  --color-border-accent: rgba(255, 255, 255, 0.18);

  /* Colors — Light Theme */
  --color-day-bg: #fff8e8;
  --color-day-surface: #ffffff;
  --color-day-text: #15151b;
  --color-day-text-secondary: rgba(21, 21, 27, 0.64);
  --color-day-border: rgba(21, 21, 27, 0.1);
  --color-day-border-strong: rgba(21, 21, 27, 0.18);

  /* Accent Colors — One per creative category */
  --color-accent-code: #2457ff;
  --color-accent-design: #ff5c35;
  --color-accent-art: #00a77f;
  --color-accent-photo: #f2b705;
  --color-accent-poetry: #8f55ff;
  --color-accent-story: #e5488b;
  --color-accent-experiments: #16a3b8;

  /* Fonts — Three-tier hierarchy */
  --font-editorial: 'Cormorant Garamond', 'Noto Serif SC', Georgia, serif;
  --font-utility: 'IBM Plex Mono', 'JetBrains Mono', monospace;
  --font-body: 'Inter', system-ui, -apple-system, sans-serif;

  /* Border Radius — Brutalist defaults */
  --radius-brutal: 0px;
}
```

### 3.2 The 28px Grid
Every layout must align with the 28px rhythm. This is defined via a visible background grid:
```css
.theme-night::before, .theme-day::before {
  content: ''; position: fixed; inset: 0; z-index: 0; pointer-events: none;
  background-image: 
    linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
  background-size: 28px 28px;
}
```
**Rule:** All padding, margins, and grid gaps should be multiples of 28px (or exact fractions like `14px`, `7px`) unless there is a specific micro-justification.

### 3.3 Brutalist Borders (Absolute `rounded-none` Mandate)
**GROUND TRUTH:** Every single element must use `rounded-none`. This includes structural containers, interactive elements (buttons, badges), images, inputs, and overlays.
- **Verification:** `grep -r "rounded-full\|rounded-md\|rounded-lg\|rounded-xl\|rounded-sm" src/` must return **zero matches**. Any documentation suggesting exceptions is obsolete.
- **Known Deviation:** Legacy code may contain `rounded-sm` on `MachineOverlay.tsx` lines 48, 58, and `rounded` on line 25. **Purge these. Replace with `rounded-none`.**

### 3.4 Light Theme Override Specificity
Light theme overrides must use Tailwind v4's arbitrary variant syntax with `&` to ensure specificity.
```css
/* CORRECT */
[.theme-day_&]:bg-day-bg
[.theme-day_&]:text-day-text

/* WRONG — missing &, uses space instead of underscore */
.theme-day & 
[.theme-day &] 
```

### 3.5 Z-Index Layer Map
Prevent modal/overlay collisions by strictly adhering to this map:

| Layer | Z-Index | Element |
|---|---|---|
| Grid background | `0` | `::before` pseudo on theme classes |
| Hero content | `1` | `z-1` class on hero main content |
| Hero prev/next buttons | `2` | `z-2` on navigation arrows |
| Skip-to-content link | `20` | `z-20` |
| Sticky navigation | `30` | `z-30` on header |
| Mobile backdrop | `35` | `z-35` |
| Mobile drawer | `40` | `z-40` on aside |
| Machine overlay | `50` | `z-50` on dialog |
| Grain overlay | `9999` | `z-[9999]` on grain div (must always be on top, `pointer-events: none`) |

---

## 4. Component Architecture & Logic Patterns

### 4.1 File Organization
```text
src/
├── App.tsx                    # Thin orchestrator, state lifted here
├── main.tsx                   # React entry point with StrictMode
├── components/
│   ├── Navigation.tsx         # Sticky nav + mobile drawer + MX toggle
│   ├── HeroKinetic.tsx        # Viewport-scaled hero with pointer parallax
│   ├── AboutFlow.tsx          # Asymmetric editorial about section
│   ├── BentoGrid.tsx          # Portfolio gateway grid
│   ├── BentoTile.tsx          # Individual project tile with category texture
│   ├── ArchiveSpread.tsx      # Collection detail + item detail views
│   ├── ContactSection.tsx     # Contact + social links
│   ├── ContentBody.tsx        # Poem/prose body renderer
│   ├── GrainOverlay.tsx       # Fixed noise overlay
│   ├── MachineOverlay.tsx     # Terminal-style data overlay (MX)
│   ├── BrandMark.tsx          # SVG brand mark
│   ├── SocialIcon.tsx         # Inline SVG social icons
│   └── ThemeToggle.tsx        # Day/nightqal toggle button
├── hooks/
│   ├── useWeightedScroll.ts   # Scroll velocity -> font-weight mapping
│   ├── useRouteHash.ts        # Hash-based routing
│   └── useReducedMotion.ts    # prefers-reduced-motion hook
├── lib/
│   ├── types.ts               # All TypeScript interfaces
│   ├── content.ts             # import.meta.glob ingestion + parsing
│   └── data.ts                # Static data, collection definitions, builders
├── styles/
│   └── index.css              # Tailwind + @theme + base + animations + grain
└── content/                   # File-system content (not in src/ build)
```

### 4.2 The "Thin Orchestrator" Pattern (`App.tsx`)
`App.tsx` is the single source of truth for all application state. It lifts state up and passes it down via props. No context providers, no state management libraries. Max prop drilling depth is 2 (e.g., App → Navigation → ThemeToggle). If you find yourself passing a prop through 3+ layers, lift state closer or restructure.
- State owned: `activeHeroIndex`, `isNightMode`, `isMenuOpen`, `isMachineOpen`, `routeHash`.
- Conditional rendering: `{activeCollection ? <ArchiveSpread ... /> : <HomePageSections />}`

### 4.3 Detailed Component Logic Patterns
- **`HeroKinetic`**: Uses pointer parallax (`onMouseMove` → `--slide-x`/`--slide-y` CSS vars). Auto-rotates slides every 10s. Injects `--slide-accent` for dynamic category coloring.
- **`AboutFlow`**: "Stable Height Swap" pattern. Uses a hidden sizer div to prevent layout shift during tab/content swaps. Applies 900ms calm fade transitions (`transition-opacity duration-900 ease-out`).
- **`BentoGrid` / `BentoTile`**: Maps category to texture (mono for tech/code, serif for art/poetry). Uses accent color injection via inline CSS vars or Tailwind arbitrary properties.
- **`ArchiveSpread`**: Dual-view router. Switches between collection grid and item detail based on `hash` path. Shares a persistent header.
- **`ContentBody`**: Category-aware rendering. Splits `<pre>` for poetry, wraps prose in `<p>` tags, handles markdown parsing safely.
- **ClassName Concatenation Rule**: ALWAYS use template literals. Never string concatenation.
  ```tsx
  // BAD
  className={"base " + (isActive ? "active" : "inactive")}
  // GOOD
  className={`base ${isActive ? 'active' : 'inactive'}`}
  ```

---

## 5. Data & Content Architecture

### 5.1 The Definitive `import.meta.glob` Pattern
**CRITICAL:** `import.meta.glob` paths are relative to the **source file that calls it**, NOT the project root. Since `content.ts` lives in `src/lib/`, paths **MUST** start with `../content/` (pointing to `src/content/`). Using `./content/` is a fatal error that results in empty content arrays.

```typescript
// CORRECT (in src/lib/content.ts)
const portraitImages = import.meta.glob(
  ['../content/portrait/*.{jpg,jpeg,png,webp,avif}', '../content/portrait/**/*.{jpg,jpeg,png,webp,avif}'],
  { eager: true, import: 'default', query: '?url' }
) as Record<string, string>;

const portfolioImages = import.meta.glob(
  '../content/portfolio/**/*.{jpg,jpeg,png,webp,avif}',
  { eager: true, import: 'default', query: '?url' }
) as Record<string, string>;

// Portfolio & Collection markdown/text files
const portfolioTextFiles = import.meta.glob(
  '../content/portfolio/**/*.{md,txt}',
  { eager: true, import: 'default', query: '?raw' }
) as Record<string, string>;

const collectionTextFiles = import.meta.glob(
  '../content/collections/**/*.{md,txt}',
  { eager: true, import: 'default', query: '?raw' }
) as Record<string, string>;

// Collection documents/PDFs
const collectionDocuments = import.meta.glob(
  '../content/collections/**/*.{pdf,docx}',
  { eager: true, import: 'default', query: '?url' }
) as Record<string, string>;
```

### 5.2 Directory Structure & Sibling Resolution
```text
src/content/
├── portrait/          # Hero slide photos
├── portfolio/         # Project markdown + sibling images (project.md + project.jpg)
└── collections/       # Archive items (markdown + images + PDFs)
```
**Rule:** If a markdown file and an image share the same folder and base filename, they are "siblings" and the image is automatically associated as the visual. Path manipulation utilities in `lib/content.ts` handle this matching.

### 5.3 Frontmatter Parsing & Guide Filtering
- Lightweight YAML-like parser extracts `title`, `category`, `accent`, `status`, `description`, `link`, etc.
- **Guide File Filtering:** `PUT_*_HERE.md` files are explicitly excluded from production data using `isCollectionGuideFile()` logic to prevent placeholder content from rendering.
- **Eager Loading Rationale:** `eager: true` is correct for this portfolio (~20 files, ~4MB images). For >500 items, switch to `{ eager: false }` and implement on-demand loading.

---

## 6. Custom Hooks (Implementation Patterns)

### 6.1 SSR Guard Mandate
ALL hooks interacting with `window`, `document`, or `matchMedia` MUST include:
```typescript
const isClient = typeof window !== 'undefined';
if (!isClient) return defaultValue;
```

### 6.2 `useRouteHash`
- Listens to `hashchange` and `load` events.
- Parses `#collection/item` or `#portfolio/slug`.
- Returns `{ route, params }` object.
- Cleanup: `window.removeEventListener('hashchange', handler)`.

### 6.3 `useWeightedScroll`
- Maps scroll velocity to `font-weight` (200–950) using `requestAnimationFrame` throttling.
- Uses a state-hack (`_timestamp`, `_scrollY`) to calculate delta without triggering re-renders on every tick.
- Returns static `950` if `prefers-reduced-motion` is true.
- Cleanup: `cancelAnimationFrame(id)`.

### 6.4 `useReducedMotion`
- Double-layer defense:
  1. **React Hook:** `window.matchMedia('(prefers-reduced-motion: reduce)').matches`
  2. **Global CSS:** `@media (prefers-reduced-motion: reduce) { * { transition: none !important; animation: none !important; } }`
- MUST gate ALL motion behind this hook.

---

## 7. Accessibility (WCAG AAA)

### 7.1 Mandatory Checks
- [ ] **Meaningful Alt Text:** All content images MUST have meaningful `alt` text (e.g., `alt={item.title}`, `alt="Nicholas Yun"`).
- [ ] **No Empty Alt for Content:** `alt=""` is strictly reserved for purely decorative UI elements (e.g., `GrainOverlay`, `BrandMark`).
- [ ] **Motion Gating:** All animations check `useReducedMotion()`. Global CSS disables ALL transitions.
- [ ] **Focus Visible:** All interactive elements have visible focus indicators: `outline: 3px solid rgba(36, 87, 255, 0.35); outline-offset: 3px;`.
- [ ] **Skip Link:** A "Skip to main content" link is present (`App.tsx:88`) using off-screen `-translate-y-[160%]` to `focus:translate-y-0`.
- [ ] **ARIA Patterns:**
  - Mobile drawer: `aria-expanded`, `aria-controls`
  - Hero dots: `aria-pressed="true/false"`, `role="tab"`
  - Machine overlay: `role="dialog"`, `aria-modal="true"`
  - Live regions: `aria-live="polite"` for dynamic content swaps
- [ ] **High Contrast:** Maintained in both `.theme-night` and `.theme-day`.

---

## 8. Complete TypeScript Interface Reference

All interfaces live in `src/lib/types.ts`. Key design decisions: `Project` and `CollectionItem` share fields via `extends`. Optional fields use `?`. `SocialLink.icon` uses a union type (not `enum`) due to `erasableSyntaxOnly`.

```typescript
export interface HeroSlide {
  label: string;
  portraitKey: string;
  headline: string;
  subtitle: string;
  artifactTitle: string;
  artifactMeta: string;
  signature: string;
  accent: string;
  secondaryAccent: string;
  tags: string[];
}

export interface AboutPillar {
  title: string;
  paragraphs: string[]; // CORRECT: body would be 'body: string[]'
}

export interface Project {
  title: string;
  category: string;
  accent: string;
  medium?: string;
  status: string;
  description: string;
  link?: string;
  linkLabel: string;
  slug: string;
  image?: string;
  body?: string;
}

export interface CollectionItem extends Project {
  collectionSlug: string;
  document?: string;
}

export interface Collection {
  slug: string;
  title: string;
  category: string;
  accent: string;
  description: string;
  status: string;
}

export interface ArchiveRoute {
  collectionSlug: string;
  itemSlug: string | null;
}

export interface SocialLink {
  label: string;
  icon: 'mail' | 'linkedin' | 'instagram' | 'github';
  href: string;
  description: string;
}

export interface MachineOverlayData {
  buildVersion: string;
  route: string;
  collections: Record<string, number>;
  activeData: unknown; // Not 'any'
}
```

**Handling Indexed Access:** Because `noUncheckedIndexedAccess: true`, always handle `T | undefined`:
```typescript
// SAFE
const slide = slides[index];
if (slide) { console.log(slide.title); }

// SAFE (if bounds checked)
if (index < slides.length) { console.log(slides[index]!.title); }
```

---

## 9. Anti-Patterns & Common Bugs

### Bug 1: The "Rounding Leak"
- **Symptom:** Components contain `rounded-md`, `rounded-lg`, or `rounded-sm`, violating the brutalist aesthetic.
- **Fix:** `sed -i 's/rounded-full/rounded-none/g; s/rounded-md/rounded-none/g; s/rounded-lg/rounded-none/g; s/rounded-sm/rounded-none/g' src/components/*.tsx`
- **Verify:** `grep -r "rounded-full\|rounded-md\|rounded-lg\|rounded-sm" src/` returns empty.
**Note on Line 25 of `MachineOverlay.tsx`:** This file may contain `rounded` (without a size suffix). Replace with `rounded-none` as well.

### Bug 2: Incorrect `import.meta.glob` Paths
- **Symptom:** All content images fail to load; browser shows "NY" placeholder text.
- **Root Cause:** Paths were `./content/...` (pointing to non-existent `src/lib/content/`).
- **Fix:** Update all glob paths in `content.ts` to `../content/...`.

### Bug 3: Unstable React Keys
- **Symptom:** React warnings about duplicate keys or unexpected re-rendering.
- **Root Cause:** Using paragraph strings or dynamic content as `key` props.
- **Fix:** Use a stable, unique identifier. If no ID exists, use a stable hash or the array index as a last resort.
  ```tsx
  // WRONG: <p key={paragraph}>{paragraph}</p>
  // CORRECT: <p key={`para-${index}`}>{paragraph}</p>
  ```

### Bug 4: Light Theme Override Specificity Failures
- **Symptom:** Light theme styles don't apply.
- **Root Cause:** Using `[.theme-day &]` or missing `&`.
- **Fix:** Use `[.theme-day_&]:` arbitrary variant.

### Bug 5: Body Scroll Lock Cleanup Failures
- **Symptom:** Page remains unscrollable after closing the mobile menu.
- **Fix:** Ensure `useEffect` cleanup always resets: `return () => { document.body.style.overflow = ''; }`

### Bug 6: `erasableSyntaxOnly` Rejecting Enums
- **Symptom:** TS build fails with "This syntax is not allowed when 'erasableSyntaxOnly' is enabled".
- **Fix:** Replace `enum` with union types (e.g., `type Icon = 'mail' | 'linkedin';`).

---

## 10. Debugging Guide

| Symptom | Diagnosis | Step-by-Step Fix |
|---|---|---|
| **Broken Images / "NY" Fallback** | Glob path mismatch or missing asset. | 1. Network tab: Check 404.<br>2. `content.ts`: Add `console.log('Portrait:', Object.keys(portraitImages));`<br>3. Verify paths start with `../content/`. |
| **TypeScript: "Object is possibly 'undefined'"** | `noUncheckedIndexedAccess` violation. | 1. Add explicit `if (arr[index])` check.<br>2. Use optional chaining `arr[index]?.prop`.<br>3. Assert with `!` only if bounds-checked. |
| **Build Failures (GitHub Pages)** | Incorrect base path or plugin order. | 1. Ensure `vite.config.ts` has `base: './'`.<br>2. Verify `@tailwindcss/vite` is in `plugins`.<br>3. Run `pnpm typecheck` first to isolate TS vs Build errors. |
| **Content Not Appearing** | Guide file leak or frontmatter parse fail. | 1. Verify `isCollectionGuideFile` filters `PUT_*_HERE.md`.<br>2. Check frontmatter syntax (no trailing commas, correct YAML-like structure). |
| **Theme Toggle Not Working** | Root class not applied or CSS specificity clash. | 1. Check `document.documentElement.classList.toggle('theme-day')`.<br>2. Verify `[.theme-day_&]:` syntax in CSS.<br>3. Clear browser cache; Tailwind JIT may need hard refresh. |
| **Mobile Menu Lockup** | Scroll lock not cleaned up or drawer transform off. | 1. Check `document.body.style.overflow` in `useEffect` cleanup.<br>2. Verify drawer uses `translate-x-[105%]` (closed) vs `translate-x-0` (open). |

---

## 11. Pre-Ship Checklist & Verification

Run EVERY item before claiming completion. No exceptions.

### Build Verification
```bash
# 1. Type Safety
pnpm typecheck

# 2. Production Build
pnpm build

# 3. Asset Verification
ls -la dist/assets/
```

### Responsive Breakpoint Behavior Table
| Viewport | Expected Behavior |
|---|---|
| `360px` | Single column, compressed hero, mobile nav active |
| `430px` | Standard mobile, bento grid stacks vertically |
| `620px` | Tablet-ish, slight grid expansion |
| `760px` | **Major Mobile Breakpoint** — dual-column bento, nav adapts |
| `900px` | Tablet landscape, full editorial spacing returns |
| `1200px` | Desktop baseline, 3-4 column grids, parallax enabled |
| `1536px` | Max container width, extreme whitespace utilization |

### Functional & Accessibility Checklist
- [ ] `grep -r "rounded-full\|rounded-md\|rounded-lg\|rounded-sm" src/` returns **empty**.
- [ ] No purple gradients or generic card grids anywhere.
- [ ] All `<img>` tags have meaningful `alt` text (not `alt=""` unless truly decorative).
- [ ] All animations check `useReducedMotion()`.
- [ ] `pnpm typecheck` passes with zero errors.
- [ ] No `any`, `enum`, or `namespace` keywords in the codebase.
- [ ] All React `key` props are stable and unique.
- [ ] `import.meta.glob` paths in `content.ts` are correct (`../content/...`).
- [ ] Mobile drawer scroll lock cleans up properly.
- [ ] Theme toggle persists or respects `prefers-color-scheme` fallback.
- [ ] Skip-to-content link focuses main content on activation.
- [ ] Focus visible states are present on all interactive elements.

---

## 12. Summary: The Non-Negotiables

| Domain | Absolute Rule | Verification Command |
|---|---|---|
| **Aesthetic** | Zero border radius. No template UI. Brutalist + Editorial only. | `grep -r "rounded-full\|rounded-md\|rounded-lg\|rounded-sm" src/` (must be empty) |
| **Grid** | All spacing multiples of `28px`. Visible background grid. | Visual QA + CSS inspection |
| **Accessibility** | WCAG AAA. Meaningful `alt` text. Motion gating. Skip link. | `grep 'alt=""' src/` (must be 0 for content) |
| **TypeScript** | `erasableSyntaxOnly`, `noUncheckedIndexedAccess`. Union types > enums. | `pnpm typecheck` |
| **Content** | `import.meta.glob` uses `../content/...`. Eager loading for current scale. | `console.log(Object.keys(...))` |
| **Typography** | Cormorant (Headlines), Plex Mono (Utility), Inter (Body). | Visual inspection |
| **Installation** | Bespoke only. No external UI libs. State lifted to `App.tsx`. | `package.json` scan + `App.tsx` review |

*Built from the ground up to be a digital installation, not a generic portfolio. Every line of code serves the "Engineered Soul" thesis. This document is the constitution. Deviations are regressions.*
