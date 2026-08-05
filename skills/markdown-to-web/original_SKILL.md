---
name: react-markdown-report
description: >
  Single-file React 19 + Vite 7 + Tailwind CSS v4 app that renders a static
  Markdown UI/UX audit report ("Kelp Agency vs. Clone") with evidence-tagged
  findings, a status-badge system, and a responsive Table of Contents.
version: 1.0.1
tags:
  - react
  - vite
  - tailwindcss
  - markdown
  - audit-report
  - single-file-build
---

# react-markdown-report — Project Skill

> **Purpose:** Enable any future agent to understand, maintain, extend, or rebuild this static Markdown audit report application without re-discovering its conventions, pitfalls, or evidence-contract requirements.
>
> **When to use:** After any change to the report content, renderer, TOC extraction, badge styling, or build pipeline; when onboarding a new agent; when the codebase has drifted from docs.
>
> **Output of this skill:** This document (`react-markdown_SKILL.md`) itself.

---

## Table of Contents

1. [Project Identity & Design Philosophy](#1-project-identity--design-philosophy)
2. [Tech Stack & Environment](#2-tech-stack--environment)
3. [Bootstrapping & Configuration](#3-bootstrapping--configuration)
4. [The Design System (Code-First)](#4-the-design-system-code-first)
5. [Component Architecture & Patterns](#5-component-architecture--patterns)
6. [Custom Hooks Deep Dive](#6-custom-hooks-deep-dive)
7. [Content Management & Data Ingestion](#7-content-management--data-ingestion)
8. [Accessibility (WCAG AAA) Implementation](#8-accessibility-wcag-aaa-implementation)
9. [Anti-Patterns & Common Bugs](#9-anti-patterns--common-bugs)
10. [Debugging Guide](#10-debugging-guide)
11. [Pre-Ship Checklist](#11-pre-ship-checklist)
12. [Lessons Learnt & How to Avoid Them](#12-lessons-learnt--how-to-avoid-them)
13. [Pitfalls to Avoid](#13-pitfalls-to-avoid)
14. [Best Practices](#14-best-practices)
15. [Coding Patterns](#15-coding-patterns)
16. [Coding Anti-Patterns](#16-coding-anti-patterns)
17. [Responsive Breakpoint Reference](#17-responsive-breakpoint-reference)
18. [Z-Index Layer Map](#18-z-index-layer-map)
19. [Color Reference (Complete)](#19-color-reference-complete)
20. [The Complete TypeScript Interface Reference](#20-the-complete-typescript-interface-reference)
21. [Appendices](#appendices)

---

## 1. Project Identity & Design Philosophy

**One-sentence description:** A single-file, zero-backend React application that renders a structural/content/IA comparative audit of `kelp.agency` vs. its clone `astro.jesspete.shop`, with every finding tagged by verification confidence (Verified / Reasoned / Assumed / Unverifiable) and severity (Critical / High / Medium / Low / Informational), bundled into one portable `dist/index.html`.

**Design thesis:** *Evidence over assertion; content is data.* The report is plain Markdown bundled at build time — editing it is a content change, not a UI change. The renderer (`react-markdown` + `remark-gfm` + `rehype-slug`) needs no code edits for new sections. Inline code in Markdown (`Severity: critical`, `Confidence: verified`) renders as color-coded badges, not monospace snippets.

**Non-negotiable design rules:**
- **No invented confidence:** Every finding carries an explicit evidence tag. Never upgrade "Unverifiable" to "Verified" or "Reasoned" without live-site retrieval.
- **No generic UI:** The report uses a bespoke editorial design system (Source Serif 4 display, Inter body, JetBrains Mono meta) with warm off-white (`paper-50`) backgrounds, teal/moss accents, and semantic ink scales — no purple gradients, no Bootstrap card grids, no Inter/Roboto safety.
- **Single-file portability:** The build artifact is one self-contained `dist/index.html` with all CSS/JS inlined (via `vite-plugin-singlefile`). It must run anywhere a browser can open an HTML file.
- **Responsive without JS bloat:** Desktop sidebar + mobile slide-in drawer for TOC; drawer state is the only client-side state in the entire app.
- **WCAG AAA where feasible:** Skip-to-content link, `scroll-mt-24` on anchored headings, focus-visible rings. `prefers-reduced-motion` not yet implemented (known gap).

**Anti-generic mandate (explicitly rejected):**
- Purple gradients on white
- Predictable rounded-card grids with left-border accents
- Generic "Inter/Roboto + gray-50" neutrality
- Hero sections with centered H1 + paragraph + CTA button
- Any component that could be dropped into a different project without visual friction

---

## 2. Tech Stack & Environment

| Layer | Technology | Version | Critical Note |
|-------|------------|---------|---------------|
| Framework | React | `19.2.6` | Strict TypeScript; functional components only |
| Build | Vite | `7.3.2` | Turbopack not used; `vite-plugin-singlefile` for one-file output |
| Styling | Tailwind CSS | `4.1.17` | **CSS-first `@theme` in `src/index.css`** — no `tailwind.config.js` exists |
| Markdown | react-markdown | `10.1.0` | `remark-gfm` (tables, strikethrough, task lists) + `rehype-slug` (heading anchors) |
| Heading anchors | rehype-slug | `6.0.0` | Adds `id` to headings; slugs must match `toc.ts`'s `github-slugger` output |
| TOC extraction | github-slugger | `2.0.0` | Must stay compatible with `rehype-slug`'s output or anchor links break |
| Icons | lucide-react | `1.28.0` | Menu, X, ExternalLink only |
| Class util | clsx + tailwind-merge | `2.1.1` / `3.4.0` | `cn()` helper in `src/utils/cn.ts` (currently unused in render paths) |
| Packaging | vite-plugin-singlefile | `2.3.0` | Inlines all assets into `dist/index.html` |
| TypeScript | typescript | `5.9.3` | `strict: true`, `noUnusedLocals`, `noUnusedParameters` |
| Node | — | `≥20.19` or `≥22.12` | Vite 7 requirement |

**Verification:** `cat package.json` → every row above matches `dependencies`/`devDependencies` exactly.

---

## 3. Bootstrapping & Configuration

### 3.1 Commands

```bash
# Install (package-lock.json is committed)
npm install

# Dev server (Vite)
npm run dev

# Production build → ONE self-contained dist/index.html
npm run build

# Serve the build
npm run preview

# Typecheck (no npm script exists — run directly)
npx tsc --noEmit
```

### 3.2 Configuration Files

| File | Purpose | Critical Settings |
|------|---------|-------------------|
| `vite.config.ts` | Vite plugins + `@/*` alias | `react()`, `tailwindcss()`, `viteSingleFile()`, `alias: { "@": "src" }` |
| `tsconfig.json` | TypeScript strict mode | `strict: true`, `noUnusedLocals/Parameters: true`, `moduleResolution: "bundler"`, `baseUrl: ".", paths: { "@/*": ["src/*"] }` |
| `index.html` | Entry point | `<div id="root">` + `<script type="module" src="/src/main.tsx">` |
| `src/index.css` | Tailwind v4 `@theme` + Google Fonts `@import` | All design tokens; `@import` **before** `@import "tailwindcss"` |

### 3.3 Environment

- No `.env` / `.env.example` — no runtime env vars needed (no API keys, no DB, no auth)
- Google Fonts loaded via `@import` in CSS — requires network at runtime; single-file build does **not** inline fonts
- `dist/` is build output — never edit manually

---

## 4. The Design System (Code-First)

### 4.1 `@theme` Tokens (`src/index.css:4-28`)

```css
@theme {
  --font-serif: "Source Serif 4", ui-serif, Georgia, serif;
  --font-sans: "Inter", ui-sans-serif, system-ui, sans-serif;
  --font-mono: "JetBrains Mono", ui-monospace, monospace;

  --color-ink-950: #0b1615;
  --color-ink-900: #0f1e1c;
  --color-ink-800: #16302c;
  --color-ink-700: #204640;

  --color-paper-50: #fbfaf7;
  --color-paper-100: #f4f2ec;
  --color-paper-200: #e9e5da;

  --color-teal-600: #0e7c86;
  --color-teal-700: #0b626a;
  --color-moss-500: #6fa661;
  --color-moss-600: #588650;

  --color-critical: #b3261e;
  --color-high: #b45309;
  --color-medium: #a16207;
  --color-low: #3f6212;
  --color-info: #1d4ed8;
}
```

**Tailwind classes derived:** `font-serif`, `font-sans`, `font-mono`; `bg-ink-950` through `ink-700`; `bg-paper-50` through `paper-200`; `text-teal-600`/`teal-700`; `text-moss-500`/`moss-600`; `text-critical`, `text-high`, `text-medium`, `text-low`, `text-info`; matching `bg-`, `border-`, `ring-` utilities auto-generated.

### 4.2 Typography Hierarchy

| Role | Font | Weight | Size (mobile) | Size (sm+) | Tracking | Color |
|------|------|--------|---------------|------------|----------|-------|
| H1 (report title) | Source Serif 4 | 600 | `text-3xl` | `sm:text-4xl` | normal | `ink-900` |
| H2 (section) | Source Serif 4 | 600 | `text-2xl` | `sm:text-[1.75rem]` | normal | `ink-900` |
| H3 (subsection) | Source Serif 4 | 600 | `text-xl` | — | normal | `ink-800` |
| Body (report paragraphs) | Inter | 400 | base (16px) | — | normal | `stone-700` |
| Meta / labels | JetBrains Mono | 500/600 | `text-xs` / `text-[0.7rem]` | — | `tracking-widest` / `tracking-wide` | `teal-700` / `teal-300/90` |
| Badge text | Inter (via `font-sans`) | 600 | `text-xs` | — | `tracking-wide` `uppercase` | per-severity token |

*The App-level page title ("Does the clone hold up against the original?", `App.tsx:124`) is separate: `font-bold` (700), `text-2xl` → `sm:text-3xl`. The hero intro paragraph uses `text-sm` → `sm:text-base`, `text-stone-600` (`App.tsx:127`).*

### 4.3 Keyframes & Custom Utilities

**None defined.** All animation is CSS-only via Tailwind utilities (`transition`, `hover:`, `focus:`). No `@keyframes` in `index.css`. No custom `@utility` classes.

### 4.4 Border Radius & Shadows

- Radius: `rounded` (4px), `rounded-md` (6px), `rounded-lg` (8px), `rounded-xl` (12px), `rounded-2xl` (16px), `rounded-full` (9999px) — all Tailwind defaults
- Shadows: `shadow-sm`, `shadow-xl` only — no custom shadow tokens

### 4.5 Global Base Styles (`src/index.css:30-42`)

```css
html { scroll-behavior: smooth; }
body { font-family: var(--font-sans); background-color: var(--color-paper-50); }
::selection { background-color: var(--color-teal-600); color: white; }
```

---

## 5. Component Architecture & Patterns

### 5.1 File Inventory (8 files, 458 LOC)

| File | LOC | Purpose | Client/Server |
|------|-----|---------|---------------|
| `src/main.tsx` | 10 | Entry: `StrictMode` + `createRoot` + render `App` | Client |
| `src/App.tsx` | 162 | Layout, header, drawer state, TOC data derivation | Client |
| `src/components/MarkdownReport.tsx` | 138 | `react-markdown` renderer + bespoke `components` map + `StatusBadge` | Client |
| `src/components/TableOfContents.tsx` | 51 | Recursive TOC nav (sidebar + drawer) | Client |
| `src/lib/toc.ts` | 38 | H2/H3 outline extraction via `github-slugger` | Shared (pure) |
| `src/lib/enhance.ts` | 11 | Regex preprocessor: wraps `Severity`/`Confidence` values in inline code | Shared (pure) |
| `src/utils/cn.ts` | 6 | `clsx` + `tailwind-merge` helper (currently unused) | Shared (pure) |
| `src/index.css` | 42 | Tailwind v4 `@theme` + Google Fonts + base styles | — |

### 5.2 Data Flow

```
comparative-analysis.md (?raw import)
        │
        ├─► buildToc() ──► toc: TocItem[] ──► TableOfContents (sidebar + drawer)
        │
        └─► enhanceReportMarkdown() ──► processed markdown
                │
                └─► ReactMarkdown (remark-gfm + rehype-slug)
                        │
                        ├─► Custom components map (h1–h3, p, a, strong, em, ul, ol, li, hr, blockquote, code, pre, table, thead, tbody, tr, th, td)
                        │
                        └─► code inline ──► StatusBadge (renders as badge or fallback <code>)
```

### 5.3 Component Patterns

**`App.tsx` — Single state, composed layout:**
- `useState(false)` for mobile drawer (`drawerOpen`)
- `useMemo(() => buildToc(reportMarkdown), [])` — TOC derived once
- Header: sticky `z-40`, dark `ink-950`; site links render in the header nav (`hidden sm:flex`), the mobile drawer, and hero chips (`sm:hidden`)
- Mobile drawer: `fixed inset-0 z-50 lg:hidden`, overlay + slide-in panel
- Desktop sidebar: `hidden w-64 lg:block`, `sticky top-24 max-h-[calc(100vh-7rem)]`
- Skip link: `sr-only focus:not-sr-only focus:z-50` — accessible

**`MarkdownReport.tsx` — Renderer as configuration:**
- Single export, takes `markdown: string` prop
- `enhanceReportMarkdown()` called at render time (pure, cheap)
- `components` map: every HTML element has bespoke Tailwind classes
- `code` component delegates to `StatusBadge` — **this is the badge system entry point**
- `pre` renders as dark `ink-900` code block (not badge)
- External links: `target="_blank" rel="noopener noreferrer"` auto-applied

**`TableOfContents.tsx` — Pure recursion:**
- `TocLink` renders `item` + nested `children` with `ml-3 border-l` indent
- `onNavigate` callback closes mobile drawer (passed from `App`)
- No internal state; fully controlled by props

**`toc.ts` / `enhance.ts` — Pure functions:**
- Zero dependencies beyond `github-slugger` / none
- `buildToc()`: extracts `##` / `###` only, strips backticks from heading text, nests H3 under preceding H2
- `enhanceReportMarkdown()`: regex `/^(\s*-\s*\*\*(?:Severity|Confidence):\*\*)\s+(.+)$/gm` wraps value in backticks

---

## 6. Custom Hooks Deep Dive

**None exist.** The app uses zero custom hooks. Only `useState` and `useMemo` from React in `App.tsx`. Documented here explicitly so future agents don't search for a `hooks/` directory.

---

## 7. Content Management & Data Ingestion

### 7.1 Single Source: `src/content/comparative-analysis.md`

- **244 lines**, bundled at build time via `import reportMarkdown from "./content/comparative-analysis.md?raw"` (Vite `?raw` import)
- **Entire report is this file** — no CMS, no API, no database
- Content changes = edit this Markdown file only; no code changes needed

### 7.2 Badge Protocol (Evidence Contract)

**Badge keys recognized (case-insensitive, matched in `StatusBadge`):**

| Category | Keys | Colors (severity: `@theme` tokens; confidence: Tailwind default palette) |
|----------|------|------------------------|
| Severity | `critical`, `high`, `medium`, `low`, `informational` | `critical`/`high`/`medium`/`low`/`info` |
| Confidence | `verified`, `reasoned`, `assumed`, `unverifiable` | `teal-700`/`violet-700`/`orange-700`/`stone-600` |

**Markdown syntax for badges (enforced by `enhance.ts` regex):**
```markdown
- **Severity:** critical
- **Confidence:** verified
```
Only lines matching exactly `- **Severity:** X` or `- **Confidence:** X` (with optional leading whitespace) are transformed. The value `X` is wrapped in backticks → becomes inline `code` → `StatusBadge` styles it.

**Unknown keys:** Fall back to plain `<code class="rounded bg-stone-100 px-1.5 py-0.5 font-mono text-[0.8em] text-stone-700">` — no badge styling.

### 7.3 TOC Contract

- `buildToc()` extracts **only `##` (H2) and `###` (H3)** headings
- H3 items nest under the most recent H2; orphan H3s (no preceding H2) become top-level
- Backticks in heading text are stripped (`text.replace(/`/g, "")`)
- Slugs generated by `github-slugger` — **must match `rehype-slug` output** (both use same algorithm) or anchor links break

### 7.4 Adding Content Procedure

1. Edit `src/content/comparative-analysis.md`
2. Use H2 (`##`) for major sections, H3 (`###`) for subsections
3. Add badge lines as `- **Severity:** X` / `- **Confidence:** X` immediately after relevant findings
4. Run `npx tsc --noEmit && npm run build` to verify
5. No other files touched

---

## 8. Accessibility (WCAG AAA) Implementation

| Feature | Implementation | Location |
|---------|----------------|----------|
| Skip-to-content | `<a href="#report-start" class="sr-only focus:not-sr-only focus:z-50 …">` | `App.tsx:19-24` |
| Focus visible | Skip link has explicit `focus:` styles; other interactive elements rely on the browser default focus outline (no `focus:` classes present) | `App.tsx:21` only |
| Heading hierarchy | H1 → H2 → H3 only; no skipped levels | `MarkdownReport.tsx` + report content |
| Anchor offset | `scroll-mt-24` on H2/H3 compensates for sticky header (`z-40`) | `MarkdownReport.tsx:54,60` |
| Reduced motion | Not implemented — `html { scroll-behavior: smooth; }` does NOT auto-respect `prefers-reduced-motion`; add `@media (prefers-reduced-motion: reduce) { html { scroll-behavior: auto; } }` to enable | `index.css:30` (gap) |
| Touch targets | Drawer buttons: menu 36×36px (`p-2` + 20px icon), close 32×32px (`p-1.5`) — pass WCAG 2.5.8 min (24px), **fail 2.5.5 AAA (44px)** | `App.tsx:30-33, 86-89` |
| ARIA labels | `aria-label` on nav + drawer trigger/close; `aria-hidden="true"` on decorative icons | `App.tsx:32, 54, 75, 88` |
| Semantic landmarks | `<header>`, `<main>`, `<aside>`, `<nav>`, `<article>`, `<footer>` | `App.tsx` |
| Color contrast | `ink-900` on `paper-50`/`white` = 16.4–17.2:1; `stone-700` = 9.9–10.3:1 (AAA ✓). Badge text pairs = **4.76–6.99:1 (AA ✓, AAA ✗)** — badges are 12px normal text | Computed (WCAG relative luminance) |

**Gaps (known):** No automated axe/Lighthouse run in CI (no CI exists). Manual verification recommended before major releases. Focus styles rely on the browser default outline (only the skip link has `focus:` classes); drawer buttons are 36×36 / 32×32px, below the 44px AAA target.

---

## 9. Anti-Patterns & Common Bugs

| # | Anti-Pattern | Symptom | Root Cause | Fix / Prevention |
|---|--------------|---------|------------|------------------|
| 1 | **Badge renders as plain `<code>`** | Inline code looks like gray monospace, not colored badge | Value not wrapped in backticks by `enhance.ts` (only `Severity`/`Confidence` bullets processed) OR lowercase key not in `BADGE_STYLES` | Use exact bullet syntax; ensure value is one of 9 recognized keys |
| 2 | **Heading missing from TOC** | New section appears in report but not in sidebar/drawer | Heading level is not `##` or `###` (e.g., `#`, `####`) | Only H2/H3 are indexed; use correct level |
| 3 | **Anchor link mismatch** | Clicking TOC entry jumps to wrong heading or top of page | TOC slug (`github-slugger`) diverged from rendered `id` (`rehype-slug`) | Both derive from same Markdown text; never hand-edit slugs; changing heading text re-derives both |
| 4 | **Typecheck fails on unused imports** | `npx tsc --noEmit` errors with `noUnusedLocals`/`noUnusedParameters` | Imported but never used (e.g., `cn` from `utils/cn.ts`) | Remove unused imports; `cn.ts` currently dead code |
| 5 | **Fonts render as fallbacks** | UI shows system serif/sans/mono instead of Source Serif 4 / Inter / JetBrains Mono | Google Fonts `@import` requires network; offline or blocked loads fall back | Known limitation; single-file build does not inline fonts |

---

## 10. Debugging Guide

| Symptom | Cause | Fix |
|---------|-------|-----|
| Build fails with `vite-plugin-singlefile` error | Plugin version mismatch or config | Verify `vite.config.ts` has `viteSingleFile()` in plugins array; `package.json` has `^2.3.0` |
| TOC anchor doesn't scroll | Heading `id` missing or `scroll-mt-24` absent | Check `MarkdownReport.tsx` H2/H3 components have `id={id}` and `scroll-mt-24`; `rehype-slug` plugin present |
| Badge shows wrong color | `BADGE_STYLES` key mismatch | `StatusBadge` does `children.trim().toLowerCase()` — ensure Markdown value matches one of 9 keys exactly (case-insensitive) |
| TypeScript error: unused local/param | Strict tsconfig | Delete or prefix with `_` (but prefer deletion); run `npx tsc --noEmit` after every edit |
| Dev server won't start | Port 5173 occupied or Node version < 20.19 | `lsof -i :5173`; `node --version` |
| Fonts look wrong in `dist/index.html` | Single-file build doesn't inline `@import` fonts | Expected behavior; requires network at runtime |

---

## 11. Pre-Ship Checklist

**Mandatory verification gate (run in order):**

```bash
# 1. Typecheck (strict, noUnusedLocals/Parameters)
npx tsc --noEmit

# 2. Production build (single-file)
npm run build

# 3. Smoke test the build
npm run preview
# Open printed URL; verify:
# - Header with both site links
# - Desktop sidebar + mobile drawer (resize < 1024px)
# - Full report renders with badges colored
# - TOC links jump to correct sections
```

**No other gates exist.** No lint, no test suite, no CI. The two commands above are the complete quality bar.

---

## 12. Lessons Learnt & How to Avoid Them

1. **Inline code ≠ badge without preprocessing** — The initial design assumed `react-markdown` could style inline code contextually. Reality: `code` component receives no parent context. Solution: `enhance.ts` regex preprocessor wraps values in backticks *before* markdown parsing. **Lesson:** Preprocess at the string level when the renderer lacks context.

2. **Two slug generators must stay in sync** — `toc.ts` uses `github-slugger` directly; `rehype-slug` uses it internally. They produce identical slugs *only if* the source text is identical. **Lesson:** Never maintain parallel slug logic; derive both from the same Markdown AST or source text.

3. **Strict TypeScript catches real bugs** — `noUnusedLocals` caught the dead `cn.ts` import immediately. **Lesson:** Keep strict mode on; treat unused-import errors as architectural signals (code not wired up).

4. **Single-file build ≠ offline fonts** — `vite-plugin-singlefile` inlines JS/CSS but not `@import`ed fonts. **Lesson:** Document font loading as a runtime dependency; don't assume the build artifact is fully self-contained.

5. **Symlinks in repo root confuse agents** — `.agents/` looked like a project doc directory but is a personal tooling symlink. **Lesson:** Explicitly document symlink nature in `AGENTS.md`/`CLAUDE.md`; never assume a directory at repo root is project-owned.

---

## 13. Pitfalls to Avoid

| Area | Don't Do This | Do This Instead |
|------|---------------|-----------------|
| Badges | Write `- **Severity:** Critical` (capitalized) | Use lowercase: `- **Severity:** critical` (case-insensitive match but convention is lowercase) |
| TOC | Add `####` sub-subsection expecting it in TOC | Only `##`/`###` are extracted; restructure or accept no TOC entry |
| Anchors | Manually set `id` on headings in Markdown | Let `rehype-slug` derive from heading text; TOC auto-matches |
| Styling | Add `tailwind.config.js` for new colors | Extend `@theme` in `src/index.css`; CSS-first is the v4 contract |
| Imports | Use relative paths like `../../components/X` | Use `@/components/X` (alias configured in tsconfig + vite) |
| State | Add global state (Context, Zustand, Redux) | Only state is `drawerOpen` in `App.tsx`; keep it that way |
| Fonts | Assume `dist/index.html` works offline | Test with network; fonts load at runtime via Google Fonts CDN |

---

## 14. Best Practices

**Code Organization:**
- One component per file; colocated with its types (inline interfaces in same file)
- Pure functions (`toc.ts`, `enhance.ts`, `cn.ts`) have no side effects, no React deps
- Path alias `@/*` → `src/*` used everywhere (no relative `../../`)

**TypeScript:**
- `strict: true` — never `any`; use `unknown` if truly unknown
- `interface` for object shapes (`TocItem`), `type` for unions (none currently)
- `ComponentPropsWithoutRef<"element">` for forwarding native props in renderer components

**React:**
- Functional components + hooks only
- Composition over inheritance (no class components, no HOCs)
- Handle all UI states where dynamic UI exists (loading/error/empty/success) — though this app has only `drawerOpen` boolean

**Tailwind v4:**
- CSS-first: all tokens in `@theme`; no `tailwind.config.js`
- Use semantic tokens (`ink-900`, `teal-600`) not arbitrary values (`#[hex]`)
- `scroll-mt-24` on all anchored headings (compensates for `sticky top-0 z-40` header)

**Content:**
- Evidence tags are part of the content, not metadata — edit in Markdown
- Never invent or upgrade confidence levels; the report's credibility depends on honesty

---

## 15. Coding Patterns

### Pattern: Pure Markdown Preprocessor (`enhance.ts`)
```typescript
// Location: src/lib/enhance.ts
// Purpose: Transform specific bullet lines so markdown renderer can style them
export function enhanceReportMarkdown(markdown: string): string {
  return markdown.replace(
    /^(\s*-\s*\*\*(?:Severity|Confidence):\*\*)\s+(.+)$/gm,
    (_match, label: string, value: string) => `${label} \`${value.trim()}\``,
  );
}
```
**Why:** React-markdown's `code` component has no access to parent/line context. Preprocessing at string level lets the existing `code`→`StatusBadge` pipeline handle styling.

### Pattern: TOC Extraction with Shared Slugger (`toc.ts`)
```typescript
// Location: src/lib/toc.ts
// Purpose: Build H2/H3 outline with slugs matching rehype-slug output
export function buildToc(markdown: string): TocItem[] {
  const slugger = new GithubSlugger(); // same algorithm as rehype-slug
  // ... extract ## and ###, nest H3 under H2, strip backticks from text
}
```
**Why:** Anchor links break if TOC slug ≠ rendered `id`. Single `GithubSlugger` instance for both ensures parity.

### Pattern: Renderer as Configuration Map (`MarkdownReport.tsx`)
```typescript
// Location: src/components/MarkdownReport.tsx
// Purpose: Every HTML element gets bespoke styling via components prop
components: {
  h2: ({ id, children }) => <h2 id={id} className="… scroll-mt-24 …">{children}</h2>,
  code: ({ children }) => <StatusBadge>{String(children)}</StatusBadge>,
  // ...
}
```
**Why:** Centralizes all markdown styling in one place; no scattered CSS or wrapper components.

---

## 16. Coding Anti-Patterns

| Anti-Pattern | Example (Don't) | Correct |
|--------------|-----------------|---------|
| **Arbitrary color values** | `className="text-[#b3261e]"` | `className="text-critical"` (token from `@theme`) |
| **Relative imports across features** | `import { x } from "../../../lib/y"` | `import { x } from "@/lib/y"` |
| **Unused imports** | `import { cn } from "@/utils/cn"` then never call `cn()` | Delete the import; `tsc --noEmit` will catch it |
| **`any` type** | `const data: any = fetch()` | `const data: unknown = fetch()` then narrow |
| **Hand-written slugs** | `id="my-custom-slug"` in Markdown | Let `rehype-slug` derive; TOC matches automatically |
| **Inline styles for dynamic values** | `style={{ color: severityColor }}` | Map severity → token class: `text-critical`, `text-high`, etc. |

---

## 17. Responsive Breakpoint Reference

**Tailwind defaults (no custom config):**
- `sm`: 640px
- `md`: 768px (used: **never** in codebase)
- `lg`: 1024px
- `xl`: 1280px (used: **never**)
- `2xl`: 1536px (used: **never**)

**Actual usage (`App.tsx` + `MarkdownReport.tsx`):**
| Breakpoint | Elements |
|------------|----------|
| `sm:` | Header padding (`sm:px-6`), logo show (`sm:flex`), title size (`sm:text-lg`), nav show (`sm:flex`), page padding (`sm:px-6`, `sm:p-6`), article padding (`sm:p-8`), report H1/H2 sizes (`sm:text-4xl`, `sm:text-[1.75rem]`), hero paragraph (`sm:text-base`), mobile-only chips (`sm:hidden`) |
| `lg:` | Sidebar show (`lg:block`), drawer hide (`lg:hidden`), page vertical padding (`lg:py-12`), article padding (`lg:p-10`) |
| `hidden sm:flex` / `lg:hidden` | Responsive show/hide patterns for desktop vs mobile nav |

**No `md:`/`xl:`/`2xl:` classes anywhere.** Design targets mobile-first → `sm` → `lg` only.

---

## 18. Z-Index Layer Map

| z-index | Element | Purpose | File:Line |
|---------|---------|---------|-----------|
| `z-50` | Skip-to-content link (focused) | Must overlay everything | `App.tsx:21` |
| `z-50` | Mobile drawer overlay + panel | Topmost on mobile | `App.tsx:72` |
| `z-40` | Sticky header | Stays above content, below drawer/skip | `App.tsx:26` |
| (default) | Main content, sidebar, report | Normal flow | — |

**No other `z-*` classes used.** Radix/shadcn portals not present (no dialogs, dropdowns, tooltips).

---

## 19. Color Reference (Complete)

Every hex **exactly matches** `src/index.css:4-28` `@theme` block.

| Token | Hex | RGB | Tailwind Class | Usage |
|-------|-----|-----|----------------|-------|
| `ink-950` | `#0b1615` | 11, 22, 21 | `bg-ink-950`, `text-ink-950` | Header bg, darkest surfaces |
| `ink-900` | `#0f1e1c` | 15, 30, 28 | `bg-ink-900`, `text-ink-900` | H1/H2 text, code block bg |
| `ink-800` | `#16302c` | 22, 48, 44 | `bg-ink-800`, `text-ink-800` | H3 text, header border |
| `ink-700` | `#204640` | 32, 70, 64 | `bg-ink-700`, `text-ink-700` | — (defined; unused in components) |
| `paper-50` | `#fbfaf7` | 251, 250, 247 | `bg-paper-50`, `text-paper-50` | Page bg, drawer bg, mobile chips, table stripe |
| `paper-100` | `#f4f2ec` | 244, 242, 236 | `bg-paper-100`, `text-paper-100` | Blockquote bg, header/menu text, code-block text |
| `paper-200` | `#e9e5da` | 233, 229, 218 | `bg-paper-200`, `border-paper-200` | Borders, dividers, table row dividers |
| `teal-600` | `#0e7c86` | 14, 124, 134 | `text-teal-600`, `bg-teal-600` | Primary accent, list markers, logo gradient, TOC hover tint |
| `teal-700` | `#0b626a` | 11, 98, 106 | `text-teal-700`, `bg-teal-700` | Body links, TOC link hover, meta labels |
| `moss-500` | `#6fa661` | 111, 166, 97 | `text-moss-500`, `bg-moss-500` | Secondary accent, blockquote border |
| `moss-600` | `#588650` | 88, 134, 80 | `text-moss-600`, `bg-moss-600` | Logo gradient end (`to-moss-600`) |
| `critical` | `#b3261e` | 179, 38, 30 | `text-critical`, `bg-critical` | Severity badge (highest) |
| `high` | `#b45309` | 180, 83, 9 | `text-high`, `bg-high` | Severity badge |
| `medium` | `#a16207` | 161, 98, 7 | `text-medium`, `bg-medium` | Severity badge |
| `low` | `#3f6212` | 63, 98, 18 | `text-low`, `bg-low` | Severity badge |
| `info` | `#1d4ed8` | 29, 78, 216 | `text-info`, `bg-info` | Severity badge (informational) |

**Badge background tints & text tokens (from `BADGE_STYLES` in `MarkdownReport.tsx:8-17`):**
- `critical` → `bg-red-50` + `ring-red-200` · `text-critical`
- `high` → `bg-amber-50` + `ring-amber-200` · `text-high`
- `medium` → `bg-yellow-50` + `ring-yellow-200` · `text-medium`
- `low` → `bg-lime-50` + `ring-lime-200` · `text-low`
- `informational` → `bg-blue-50` + `ring-blue-200` · `text-info`
- `verified` → `bg-teal-50` + `ring-teal-200` · `text-teal-700`
- `reasoned` → `bg-violet-50` + `ring-violet-200` · `text-violet-700`
- `assumed` → `bg-orange-50` + `ring-orange-200` · `text-orange-700`
- `unverifiable` → `bg-stone-100` + `ring-stone-300` · `text-stone-600`

---

## 20. The Complete TypeScript Interface Reference

### `TocItem` (`src/lib/toc.ts:3-8`)
```typescript
export interface TocItem {
  level: 2 | 3;
  text: string;
  slug: string;
  children: TocItem[];
}
```

### React Markdown Component Props (from `MarkdownReport.tsx`)
All components use `ComponentPropsWithoutRef<"element">` from React:
- `h1` / `h2` / `h3` — receive `id` (from `rehype-slug`) + `children`
- `a` — receives `href` + `children` (external link logic applied)
- `code` — receives `children` (string) → passed to `StatusBadge`
- `pre` / `table` / `thead` / `tbody` / `tr` / `th` / `td` / `ul` / `ol` / `li` / `blockquote` / `hr` / `p` / `strong` / `em` — standard props

### `App` Props
None — default export, no props.

### `TableOfContents` Props (inline type, `TableOfContents.tsx:32-38`)
```typescript
{
  items: TocItem[];
  onNavigate?: () => void;
}
```

### `MarkdownReport` Props (inline type, `MarkdownReport.tsx:38`)
```typescript
{
  markdown: string;
}
```

**Note:** No named `Props` interfaces exist — all component props are inline anonymous types; `TocItem` (`toc.ts:3-8`) is the only named interface in the codebase.

---

## Appendices

### Appendix A: `.agents/` (Removed)
- **Status:** No longer exists at repo root. Previously was a symlink to personal tooling (`/home/pete/.pi/agent/`).
- **Current status:** Absent from repo root (verified via `ls -la`); entry remains in `.gitignore` as template leftover.
- **Instruction:** Ignore `.gitignore` entry; no project documentation lives at `.agents/`.

### Appendix B: Build Output
- **Command:** `npm run build`
- **Output:** `dist/index.html` (single file, all CSS/JS inlined via `vite-plugin-singlefile`)
- **Assets:** None — fully self-contained
- **Serve:** `npm run preview` or any static host
- **Fonts:** NOT inlined — Google Fonts `@import` requires network at runtime

### Appendix C: Report Content Pipeline (Visual)

```
comparative-analysis.md (244 lines, ?raw import)
         │
         ├─ buildToc() ───► TocItem[] ───► TableOfContents (sidebar | drawer)
         │
         └─ enhanceReportMarkdown() ───► processed markdown
                  │
                  └─ ReactMarkdown (remark-gfm + rehype-slug)
                           │
                           ├─ components map (h1–h3, p, a, code, pre, table, …)
                           │
                           └─ code inline ───► StatusBadge (9 keys + fallback)
```

---

**Skill version:** `1.0.1` — created 2026-08-05 (v1.0.1 2026-08-06 validated & corrected against codebase; see `SKILL_VALIDATION_REPORT.md`)
**Generated by:** Following the `to-distill-project-into-skill` meta-skill (Six-Phase Distillation Process)
**Scope:** Complete codebase coverage for `react-markdown-report` — all 8 source files, 458 LOC, 244-line report, build pipeline, design system, accessibility, and evidence contract.