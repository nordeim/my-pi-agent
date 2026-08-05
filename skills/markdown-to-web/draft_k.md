---
name: markdown-to-web-renderer
description: >
  General-purpose skill for converting any Markdown document into a
  production-grade, single-file web presentation. Supports configurable
  badge systems, multiple design themes, responsive TOC, syntax highlighting,
  and WCAG AAA accessibility. Built on React 19 + Vite 7 + Tailwind CSS v4.
version: 2.0.0
tags:
  - react
  - vite
  - tailwindcss
  - markdown
  - static-site
  - single-file-build
  - presentation
  - renderer
---

# markdown-to-web-renderer — General Skill

> **Purpose:** Enable any agent to convert an arbitrary Markdown document into a
> beautiful, accessible, self-contained web presentation without writing
> presentation-specific code. The Markdown file is the single source of truth;
> the renderer adapts to its structure.
>
> **When to use:** Any time you need to turn a `.md` file into a shareable
> HTML page — audit reports, documentation, READMEs, articles, resumes,
> research papers, or specifications.
>
> **Output of this skill:** This document (`markdown-to-web-renderer_SKILL.md`).

---

## Table of Contents

1. [Design Philosophy](#1-design-philosophy)
2. [Tech Stack & Environment](#2-tech-stack--environment)
3. [Bootstrapping & Configuration](#3-bootstrapping--configuration)
4. [The Design System](#4-the-design-system)
5. [Content Pipeline & Extensibility](#5-content-pipeline--extensibility)
6. [Component Architecture](#6-component-architecture)
7. [Badge System (Configurable)](#7-badge-system-configurable)
8. [Table of Contents Engine](#8-table-of-contents-engine)
9. [Accessibility (WCAG AAA)](#9-accessibility-wcag-aaa)
10. [Error Handling & Resilience](#10-error-handling--resilience)
11. [Anti-Patterns & Common Bugs](#11-anti-patterns--common-bugs)
12. [Debugging Guide](#12-debugging-guide)
13. [Pre-Ship Checklist](#13-pre-ship-checklist)
14. [Best Practices](#14-best-practices)
15. [Coding Patterns](#15-coding-patterns)
16. [Responsive Reference](#16-responsive-reference)
17. [Complete TypeScript Reference](#17-complete-typescript-reference)
18. [Appendices](#18-appendices)

---

## 1. Design Philosophy

**One-sentence description:** A zero-backend React application that renders any
Markdown document as a beautiful, navigable, single-file web page, where the
document's structure drives the UI and optional inline metadata renders as
semantic badges.

**Core tenets:**

1. **Content is sovereign.** The Markdown file determines the page structure,
   headings, sections, and metadata. The renderer never invents content.
2. **Convention over configuration.** Sensible defaults for typography, spacing,
   and color work out of the box. Optional configuration layers on top.
3. **Single-file portability.** The build artifact is one `index.html` that runs
   anywhere — email it, host it, open it from disk.
4. **Accessibility by default.** WCAG 2.2 AA minimum, AAA where feasible. No
   accessibility retrofit needed.
5. **No generic UI.** Every design token is intentional. Editorial typography,
   warm neutrals, and semantic color — never Bootstrap card grids or purple
   gradients.

**Anti-generic mandate (explicitly rejected):**
- Purple gradients on white backgrounds
- Predictable card-grid layouts with left-border accents
- Generic "Inter + gray-50" neutrality
- Hero sections with centered H1 + paragraph + CTA button
- Any component that could be dropped into a different project without visual
  friction

---

## 2. Tech Stack & Environment

| Layer | Technology | Version | Critical Note |
|-------|------------|---------|---------------|
| Framework | React | `^19.0.0` | Strict TypeScript; functional components only |
| Build | Vite | `^7.0.0` | `vite-plugin-singlefile` for one-file output |
| Styling | Tailwind CSS | `^4.0.0` | **CSS-first `@theme`** — no `tailwind.config.js` |
| Markdown | react-markdown | `^10.0.0` | `remark-gfm` + `rehype-slug` + `rehype-highlight` |
| Syntax Highlight | highlight.js | `^11.0.0` | Language auto-detection; theme loaded via CSS |
| Heading anchors | rehype-slug | `^6.0.0` | Adds `id` to headings |
| TOC slugs | github-slugger | `^2.0.0` | Must match `rehype-slug` output |
| Icons | lucide-react | `^0.400.0` | Tree-shaken; only used icons bundled |
| Class util | clsx + tailwind-merge | `^2.0.0` / `^3.0.0` | `cn()` helper for conditional classes |
| Packaging | vite-plugin-singlefile | `^2.0.0` | Inlines all assets into `dist/index.html` |
| TypeScript | typescript | `^5.7.0` | `strict: true`, `noUnusedLocals`, `noUnusedParameters` |
| Node | — | `≥20.19` or `≥22.12` | Vite 7 requirement |

**Verification:** `cat package.json` → every row above matches
`dependencies`/`devDependencies` exactly.

---

## 3. Bootstrapping & Configuration

### 3.1 Commands

```bash
# Install dependencies
npm install

# Development server (hot reload)
npm run dev

# Production build → single dist/index.html
npm run build

# Preview production build locally
npm run preview

# Type-check (strict)
npx tsc --noEmit
```

### 3.2 Configuration Files

| File | Purpose | Critical Settings |
|------|---------|-------------------|
| `vite.config.ts` | Vite plugins + path aliases | `react()`, `tailwindcss()`, `viteSingleFile()`, `alias: { "@": "src" }` |
| `tsconfig.json` | TypeScript strict mode | `strict: true`, `noUnusedLocals/Parameters: true`, `moduleResolution: "bundler"` |
| `index.html` | Entry point | `<div id="root">` + `<script type="module" src="/src/main.tsx">` |
| `src/index.css` | Tailwind v4 `@theme` + Google Fonts + highlight.js theme | All design tokens; `@import` **before** `@import "tailwindcss"` |

### 3.3 Environment

- No `.env` required — no runtime env vars, API keys, or secrets
- Google Fonts loaded via `@import` in CSS — requires network at runtime
- `dist/` is build output — never edit manually

---

## 4. The Design System

### 4.1 `@theme` Tokens (`src/index.css`)

```css
@theme {
  /* Typography */
  --font-serif: "Source Serif 4", ui-serif, Georgia, serif;
  --font-sans: "Inter", ui-sans-serif, system-ui, sans-serif;
  --font-mono: "JetBrains Mono", ui-monospace, monospace;

  /* Ink scale (dark surfaces & text) */
  --color-ink-950: #0b1615;
  --color-ink-900: #0f1e1c;
  --color-ink-800: #16302c;
  --color-ink-700: #204640;
  --color-ink-600: #2d5f57;

  /* Paper scale (light backgrounds) */
  --color-paper-50: #fbfaf7;
  --color-paper-100: #f4f2ec;
  --color-paper-200: #e9e5da;
  --color-paper-300: #ddd9cc;

  /* Accent: Teal */
  --color-teal-500: #1199a3;
  --color-teal-600: #0e7c86;
  --color-teal-700: #0b626a;

  /* Accent: Moss */
  --color-moss-400: #8bc47f;
  --color-moss-500: #6fa661;
  --color-moss-600: #588650;

  /* Semantic severity (configurable badge palette) */
  --color-severity-critical: #b3261e;
  --color-severity-high: #b45309;
  --color-severity-medium: #a16207;
  --color-severity-low: #3f6212;
  --color-severity-info: #1d4ed8;

  /* Semantic confidence (configurable badge palette) */
  --color-confidence-verified: #0b626a;
  --color-confidence-reasoned: #6d28d9;
  --color-confidence-assumed: #c2410c;
  --color-confidence-unverifiable: #57534e;
}
```

**Tailwind classes derived:** `font-serif`, `font-sans`, `font-mono`;
`bg-ink-950` through `ink-600`; `bg-paper-50` through `paper-300`;
`text-teal-500` through `teal-700`; `text-moss-400` through `moss-600`;
`text-severity-critical` through `severity-info`;
`text-confidence-verified` through `confidence-unverifiable`;
matching `bg-`, `border-`, `ring-` utilities auto-generated.

### 4.2 Typography Hierarchy

| Role | Font | Weight | Mobile | Desktop | Tracking | Color |
|------|------|--------|--------|---------|----------|-------|
| H1 | Source Serif 4 | 600 | `text-3xl` | `sm:text-4xl lg:text-5xl` | `tight` | `ink-900` |
| H2 | Source Serif 4 | 600 | `text-2xl` | `sm:text-[1.75rem]` | `tight` | `ink-900` |
| H3 | Source Serif 4 | 600 | `text-xl` | `sm:text-2xl` | `tight` | `ink-800` |
| H4 | Inter | 600 | `text-lg` | — | `tight` | `ink-800` |
| Body | Inter | 400 | `text-base` (16px) | — | `normal` | `stone-700` |
| Lead | Inter | 400 | `text-sm` | `sm:text-base` | `normal` | `stone-600` |
| Meta / labels | JetBrains Mono | 500 | `text-xs` | — | `wide` | `teal-700` |
| Code inline | JetBrains Mono | 400 | `text-[0.85em]` | — | `normal` | `ink-800` |
| Badge | Inter | 600 | `text-xs` | — | `wide uppercase` | per-token |

### 4.3 Global Base Styles

```css
html { scroll-behavior: smooth; }

@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

body {
  font-family: var(--font-sans);
  background-color: var(--color-paper-50);
  color: var(--color-ink-900);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

::selection {
  background-color: var(--color-teal-600);
  color: white;
}

/* Code block styling (highlight.js theme override) */
pre code.hljs {
  border-radius: 0.5rem;
  padding: 1.25rem;
  font-size: 0.875rem;
  line-height: 1.7;
}
```

---

## 5. Content Pipeline & Extensibility

### 5.1 Data Flow

```
src/content/document.md (?raw import)
        │
        ├─► buildToc(markdown) ──► TocItem[] ──► TableOfContents
        │
        ├─► extractFrontmatter(markdown) ──► Frontmatter ──► PageMeta
        │
        ├─► enhanceMarkdown(markdown, config) ──► processed markdown
        │       │
        │       └─► ReactMarkdown (remark-gfm + rehype-slug + rehype-highlight)
        │               │
        │               ├─► Custom components map
        │               │       (h1–h4, p, a, strong, em, ul, ol, li, hr,
        │               │        blockquote, code, pre, table, thead, tbody,
        │               │        tr, th, td)
        │               │
        │               └─► code inline ──► BadgeRenderer (configurable)
        │
        └─► ErrorBoundary ──► graceful fallback on render failure
```

### 5.2 Frontmatter Support

The renderer recognizes YAML frontmatter at the top of the Markdown file:

```markdown
---
title: "Document Title"
subtitle: "Optional subtitle"
author: "Author Name"
date: "2026-08-06"
badgeConfig: "audit"   # or "custom" or null
theme: "default"       # reserved for future theme variants
---
```

**Extraction:** `src/lib/frontmatter.ts` — uses regex to parse `---` delimited
YAML. Falls back gracefully if frontmatter is absent or malformed.

**Usage:**
- `title` → `<title>` tag + hero H1
- `subtitle` → hero paragraph
- `author` / `date` → meta line below hero
- `badgeConfig` → selects which badge keys are active (see §7)

### 5.3 Adding Content Procedure

1. Place your `.md` file in `src/content/document.md`
2. (Optional) Add YAML frontmatter for title, subtitle, etc.
3. (Optional) Add badge lines as `- **Key:** value` for automatic badge styling
4. Run `npx tsc --noEmit && npm run build`
5. No other files touched — the renderer adapts to your content

---

## 6. Component Architecture

### 6.1 File Inventory (10 files, ~520 LOC)

| File | LOC | Purpose | Client/Server |
|------|-----|---------|---------------|
| `src/main.tsx` | 14 | Entry: `StrictMode` + `ErrorBoundary` + `createRoot` | Client |
| `src/App.tsx` | 145 | Layout, header, drawer state, TOC + frontmatter derivation | Client |
| `src/components/MarkdownRenderer.tsx` | 155 | `react-markdown` renderer + components map + `BadgeRenderer` | Client |
| `src/components/TableOfContents.tsx` | 55 | Recursive TOC nav (sidebar + mobile drawer) | Client |
| `src/components/ErrorFallback.tsx` | 28 | Graceful error UI when rendering fails | Client |
| `src/lib/toc.ts` | 42 | H2/H3/H4 outline extraction via `github-slugger` | Shared (pure) |
| `src/lib/frontmatter.ts` | 35 | YAML frontmatter extraction | Shared (pure) |
| `src/lib/enhance.ts` | 18 | Configurable regex preprocessor for badge wrapping | Shared (pure) |
| `src/lib/badges.ts` | 48 | Badge configuration registry + style resolver | Shared (pure) |
| `src/utils/cn.ts` | 6 | `clsx` + `tailwind-merge` helper | Shared (pure) |

### 6.2 Key Patterns

**`App.tsx` — Single state, composed layout:**
- `useState(false)` for mobile drawer
- `useMemo(() => buildToc(markdown), [markdown])` — TOC re-derives if content changes
- `useMemo(() => extractFrontmatter(markdown), [markdown])` — metadata extraction
- Header: sticky `z-40`, dark `ink-950`
- Skip link: `sr-only focus:not-sr-only focus:z-50`
- Mobile drawer: `fixed inset-0 z-50 lg:hidden`
- Desktop sidebar: `hidden w-64 lg:block`, `sticky top-24`

**`MarkdownRenderer.tsx` — Renderer as configuration:**
- Accepts `markdown: string` + optional `badgeConfig: string` props
- Calls `enhanceMarkdown()` at render time (pure, cheap)
- `components` map: every HTML element has bespoke Tailwind classes
- `code` component delegates to `BadgeRenderer` — entry point for badge system
- `pre` renders as dark `ink-900` code block with `hljs` class for highlight.js
- External links: `target="_blank" rel="noopener noreferrer"` auto-applied

**`TableOfContents.tsx` — Pure recursion:**
- `TocLink` renders `item` + nested `children` with `ml-3 border-l` indent
- `onNavigate` callback closes mobile drawer
- No internal state; fully controlled by props

**`ErrorFallback.tsx` — Graceful degradation:**
- Displays error message + stack trace in a styled container
- Includes "Reload page" button
- Prevents white-screen crashes from malformed Markdown

---

## 7. Badge System (Configurable)

### 7.1 Badge Registry (`src/lib/badges.ts`)

The badge system is **fully configurable** via a registry pattern. Instead of
hardcoding Severity/Confidence, you define badge categories and their valid
values:

```typescript
// Default configuration — "audit" preset
export const BADGE_REGISTRY: BadgeRegistry = {
  audit: {
    severity: {
      critical:  { bg: "bg-red-50",    ring: "ring-red-200",    text: "text-severity-critical" },
      high:      { bg: "bg-amber-50",  ring: "ring-amber-200",  text: "text-severity-high" },
      medium:    { bg: "bg-yellow-50", ring: "ring-yellow-200", text: "text-severity-medium" },
      low:       { bg: "bg-lime-50",   ring: "ring-lime-200",   text: "text-severity-low" },
      informational: { bg: "bg-blue-50", ring: "ring-blue-200", text: "text-severity-info" },
    },
    confidence: {
      verified:     { bg: "bg-teal-50",   ring: "ring-teal-200",   text: "text-confidence-verified" },
      reasoned:     { bg: "bg-violet-50", ring: "ring-violet-200", text: "text-confidence-reasoned" },
      assumed:      { bg: "bg-orange-50", ring: "ring-orange-200", text: "text-confidence-assumed" },
      unverifiable: { bg: "bg-stone-100", ring: "ring-stone-300",  text: "text-confidence-unverifiable" },
    },
  },
  // Add your own presets here...
};
```

### 7.2 Markdown Syntax for Badges

Any bullet line matching the pattern `- **Category:** value` is transformed:

```markdown
- **Severity:** critical
- **Confidence:** verified
- **Priority:** high
- **Status:** in-review
```

The `enhance.ts` preprocessor wraps the value in backticks, which the
`code` component then styles via `BadgeRenderer`.

### 7.3 Custom Badge Presets

To add a new preset (e.g., for documentation status):

```typescript
// In src/lib/badges.ts
export const BADGE_REGISTRY: BadgeRegistry = {
  // ... existing presets ...
  docs: {
    status: {
      draft:     { bg: "bg-stone-100", ring: "ring-stone-300", text: "text-stone-600" },
      review:    { bg: "bg-amber-50",  ring: "ring-amber-200", text: "text-amber-700" },
      approved:  { bg: "bg-lime-50",   ring: "ring-lime-200",  text: "text-lime-700" },
      published: { bg: "bg-teal-50",   ring: "ring-teal-200",  text: "text-teal-700" },
    },
  },
};
```

Then set frontmatter: `badgeConfig: "docs"` or pass `badgeConfig="docs"` to
`<MarkdownRenderer />`.

### 7.4 Unknown Keys

Unknown values fall back to a neutral `<code>` style:
`rounded bg-stone-100 px-1.5 py-0.5 font-mono text-[0.8em] text-stone-700`

---

## 8. Table of Contents Engine

### 8.1 Extraction Rules

- `buildToc()` extracts **H2, H3, and H4** headings (configurable depth)
- H3 nests under the most recent H2; H4 nests under the most recent H3
- Orphan headings (no preceding parent) become top-level
- Backticks in heading text are stripped for display but preserved in slugs
- Slugs generated by `github-slugger` — **must match `rehype-slug` output**

### 8.2 TOC Contract

| Heading Level | TOC Depth | Indentation |
|---------------|-----------|-------------|
| `##` (H2) | 1 | None |
| `###` (H3) | 2 | `ml-3` + left border |
| `####` (H4) | 3 | `ml-6` + left border |

### 8.3 Adding Content

1. Use `##` for major sections, `###` for subsections, `####` for details
2. Only these levels appear in the TOC
3. Let `rehype-slug` derive heading `id`s automatically — never hand-write them

---

## 9. Accessibility (WCAG AAA)

| Feature | Implementation | Location |
|---------|----------------|----------|
| Skip-to-content | `<a href="#main-content">` with `sr-only focus:not-sr-only` | `App.tsx` |
| Focus visible | Skip link + all interactive elements have visible focus rings | `App.tsx`, `TableOfContents.tsx` |
| Heading hierarchy | H1 → H2 → H3 → H4; no skipped levels | `MarkdownRenderer.tsx` + content |
| Anchor offset | `scroll-mt-24` on H2/H3/H4 compensates for sticky header | `MarkdownRenderer.tsx` |
| Reduced motion | `prefers-reduced-motion` disables smooth scroll + animations | `index.css` |
| Touch targets | All buttons ≥ 44×44px (AAA target) | `App.tsx` |
| ARIA labels | `aria-label` on nav, drawer triggers; `aria-hidden` on decorative icons | `App.tsx`, `TableOfContents.tsx` |
| Semantic landmarks | `<header>`, `<main>`, `<aside>`, `<nav>`, `<article>`, `<footer>` | `App.tsx` |
| Color contrast | `ink-900` on `paper-50` = 16.4:1 (AAA ✓); badge text ≥ 4.5:1 (AA ✓) | Verified |
| Error messaging | `ErrorFallback` provides accessible error announcements | `ErrorFallback.tsx` |

**Gaps (known):** No automated axe/Lighthouse in CI. Manual verification
recommended before major releases.

---

## 10. Error Handling & Resilience

### 10.1 Error Boundaries

`main.tsx` wraps `<App />` in an `<ErrorBoundary>` that catches:
- Markdown parse errors
- React render errors
- Runtime exceptions in components

Fallback UI (`ErrorFallback.tsx`) shows:
- User-friendly error message
- Technical details (collapsed)
- "Reload page" button

### 10.2 Malformed Markdown Handling

| Scenario | Behavior |
|----------|----------|
| Unclosed code fence | `react-markdown` renders as plain text — no crash |
| Broken table syntax | Table renders as plain text — no crash |
| Invalid frontmatter YAML | Falls back to empty frontmatter; document still renders |
| Missing `?raw` import | Build-time Vite error — caught before runtime |
| Badge value not in registry | Renders as neutral inline code — no crash |

### 10.3 Defensive Patterns

- All array operations use optional chaining (`items?.map`)
- All string operations validate input before regex
- `BadgeRenderer` handles non-string children gracefully
- `buildToc()` handles empty Markdown gracefully (returns `[]`)

---

## 11. Anti-Patterns & Common Bugs

| # | Anti-Pattern | Symptom | Root Cause | Fix |
|---|--------------|---------|------------|-----|
| 1 | **Badge renders as plain `<code>`** | Gray monospace instead of colored badge | Value not wrapped by `enhance.ts` OR key not in active badge registry | Use exact `- **Key:** value` syntax; ensure value exists in registry |
| 2 | **Heading missing from TOC** | Section not in sidebar/drawer | Heading level > max depth or not `##`/`###`/`####` | Only H2–H4 are indexed by default |
| 3 | **Anchor link mismatch** | TOC jumps to wrong heading | TOC slug diverged from rendered `id` | Both derive from same text; never hand-edit slugs |
| 4 | **Typecheck fails on unused imports** | `tsc` errors with `noUnusedLocals` | Imported but never used | Remove unused imports; run `tsc --noEmit` after edits |
| 5 | **Fonts render as fallbacks** | System fonts instead of custom | Google Fonts `@import` requires network | Known limitation; single-file build doesn't inline fonts |
| 6 | **Code blocks not highlighted** | Plain text in `<pre>` | `rehype-highlight` not configured or language not detected | Ensure `hljs` class is present; check highlight.js CSS import |
| 7 | **Error boundary catches everything** | App shows error UI for minor issues | Overly broad error boundary | Only wrap top-level; keep granular try/catch in data processing |

---

## 12. Debugging Guide

| Symptom | Cause | Fix |
|---------|-------|-----|
| Build fails with `vite-plugin-singlefile` error | Plugin version mismatch | Verify `vite.config.ts` has `viteSingleFile()` in plugins array |
| TOC anchor doesn't scroll | Missing `id` or `scroll-mt-24` | Check `MarkdownRenderer.tsx` heading components have both |
| Badge shows wrong color | Badge registry key mismatch | `BadgeRenderer` does `trim().toLowerCase()` — ensure exact match |
| TypeScript error: unused local/param | Strict tsconfig | Delete or use the import; run `npx tsc --noEmit` |
| Dev server won't start | Port 5173 occupied or Node < 20.19 | `lsof -i :5173`; `node --version` |
| Fonts wrong in `dist/index.html` | Single-file doesn't inline `@import` fonts | Expected; requires network at runtime |
| Code blocks lack syntax highlighting | Missing highlight.js CSS theme | Verify `@import "highlight.js/styles/github-dark.css"` in `index.css` |
| Frontmatter not parsed | Missing `---` delimiters or malformed YAML | Check frontmatter is at very top of file; validate YAML syntax |

---

## 13. Pre-Ship Checklist

```bash
# 1. Typecheck (strict, noUnusedLocals/Parameters)
npx tsc --noEmit

# 2. Production build (single-file)
npm run build

# 3. Smoke test the build
npm run preview
# Verify:
# - Header renders with title from frontmatter (or fallback)
# - Desktop sidebar + mobile drawer (resize < 1024px)
# - Full document renders with badges colored correctly
# - TOC links jump to correct sections
# - Code blocks have syntax highlighting
# - Error boundary not triggered
# - No console errors
```

---

## 14. Best Practices

**Code Organization:**
- One component per file; colocated with inline types
- Pure functions (`toc.ts`, `enhance.ts`, `badges.ts`, `frontmatter.ts`) have no side effects
- Path alias `@/*` → `src/*` used everywhere

**TypeScript:**
- `strict: true` — never `any`; use `unknown` if truly unknown
- `interface` for object shapes, `type` for unions
- `ComponentPropsWithoutRef<"element">` for forwarding native props

**React:**
- Functional components + hooks only
- Composition over inheritance
- Error boundaries at app root; defensive checks in pure functions

**Tailwind v4:**
- CSS-first: all tokens in `@theme`; no `tailwind.config.js`
- Use semantic tokens (`ink-900`, `teal-600`) not arbitrary values
- `scroll-mt-24` on all anchored headings

**Content:**
- Edit Markdown only; no code changes needed for content updates
- Use frontmatter for metadata; never hardcode page titles in components
- Badge values are content, not code — add new values to registry, not renderer

---

## 15. Coding Patterns

### Pattern: Configurable Badge Registry
```typescript
// src/lib/badges.ts
export interface BadgeStyle {
  bg: string;
  ring: string;
  text: string;
}

export interface BadgeCategory {
  [value: string]: BadgeStyle;
}

export interface BadgeRegistry {
  [preset: string]: BadgeCategory;
}

export function resolveBadgeStyle(
  preset: string,
  category: string,
  value: string
): BadgeStyle | null {
  const normalized = value.trim().toLowerCase();
  return BADGE_REGISTRY[preset]?.[category]?.[normalized] ?? null;
}
```

### Pattern: Frontmatter Extraction
```typescript
// src/lib/frontmatter.ts
export function extractFrontmatter(markdown: string): Frontmatter {
  const match = markdown.match(/^---\n([\s\S]*?)\n---\n/);
  if (!match) return {};
  
  const lines = match[1].split("\n");
  const frontmatter: Record<string, string> = {};
  
  for (const line of lines) {
    const [key, ...rest] = line.split(":");
    if (key && rest.length > 0) {
      frontmatter[key.trim()] = rest.join(":").trim().replace(/^["']|["']$/g, "");
    }
  }
  
  return frontmatter;
}
```

### Pattern: Error Boundary
```typescript
// src/components/ErrorFallback.tsx
export class ErrorBoundary extends React.Component<
  { children: React.ReactNode },
  { hasError: boolean; error?: Error }
> {
  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }
  
  render() {
    if (this.state.hasError) {
      return <ErrorFallback error={this.state.error} />;
    }
    return this.props.children;
  }
}
```

### Pattern: TOC Extraction with Shared Slugger
```typescript
// src/lib/toc.ts
export function buildToc(markdown: string, maxDepth = 4): TocItem[] {
  const slugger = new GithubSlugger();
  const lines = markdown.split("\n");
  const toc: TocItem[] = [];
  const stack: TocItem[][] = [toc];
  
  for (const line of lines) {
    const match = line.match(/^(#{2,4})\s+(.+)$/);
    if (!match) continue;
    
    const level = match[1].length; // 2, 3, or 4
    if (level > maxDepth) continue;
    
    const text = match[2].replace(/`/g, "").trim();
    const slug = slugger.slug(text);
    const item: TocItem = { level, text, slug, children: [] };
    
    // Adjust stack to correct parent level
    while (stack.length > level - 1) stack.pop();
    const parent = stack[stack.length - 1];
    parent.push(item);
    stack.push(item.children);
  }
  
  return toc;
}
```

---

## 16. Responsive Reference

**Tailwind defaults (no custom config):**
- `sm`: 640px
- `md`: 768px
- `lg`: 1024px
- `xl`: 1280px
- `2xl`: 1536px

**Usage patterns:**
| Breakpoint | Elements |
|------------|----------|
| `sm:` | Header padding, logo visibility, title sizes, nav visibility, page padding, article padding, heading sizes, hero text |
| `lg:` | Sidebar show/hide, drawer show/hide, page vertical padding, max-width adjustments |
| `xl:` | Max-width constraints for readability (`max-w-4xl`) |

---

## 17. Complete TypeScript Reference

### `TocItem`
```typescript
export interface TocItem {
  level: 2 | 3 | 4;
  text: string;
  slug: string;
  children: TocItem[];
}
```

### `Frontmatter`
```typescript
export interface Frontmatter {
  title?: string;
  subtitle?: string;
  author?: string;
  date?: string;
  badgeConfig?: string;
  theme?: string;
  [key: string]: string | undefined;
}
```

### `BadgeStyle`
```typescript
export interface BadgeStyle {
  bg: string;
  ring: string;
  text: string;
}
```

### Component Props
- `MarkdownRenderer`: `{ markdown: string; badgeConfig?: string }`
- `TableOfContents`: `{ items: TocItem[]; onNavigate?: () => void }`
- `ErrorFallback`: `{ error?: Error }`
- `App`: No props

---

## 18. Appendices

### Appendix A: Build Output
- **Command:** `npm run build`
- **Output:** `dist/index.html` (single file, all CSS/JS inlined)
- **Assets:** None — fully self-contained except Google Fonts
- **Serve:** `npm run preview` or any static host

### Appendix B: Content Pipeline (Visual)

```
document.md (?raw import)
    │
    ├─ extractFrontmatter() ──► Frontmatter ──► Hero / <title>
    │
    ├─ buildToc() ──► TocItem[] ──► TableOfContents (sidebar | drawer)
    │
    ├─ enhanceMarkdown(config) ──► processed markdown
    │       │
    │       └─ ReactMarkdown (remark-gfm + rehype-slug + rehype-highlight)
    │               │
    │               ├─ components map (h1–h4, p, a, code, pre, table, …)
    │               │
    │               └─ code inline ──► BadgeRenderer (configurable registry)
    │
    └─ ErrorBoundary ──► ErrorFallback (on failure)
```

### Appendix C: Migration from `react-markdown-report`

| From (v1) | To (v2) |
|-----------|---------|
| `comparative-analysis.md` | `src/content/document.md` (generic name) |
| `enhanceReportMarkdown()` | `enhanceMarkdown(markdown, config)` (configurable) |
| Hardcoded `Severity`/`Confidence` | `BADGE_REGISTRY` with configurable presets |
| `StatusBadge` component | `BadgeRenderer` with registry lookup |
| H2/H3 only TOC | H2/H3/H4 TOC (configurable depth) |
| No frontmatter | YAML frontmatter support |
| No error boundary | `<ErrorBoundary>` at root |
| `cn.ts` dead code | `cn()` actively used for conditional classes |
| No `prefers-reduced-motion` | Full reduced-motion support |

---

**Skill version:** `2.0.0` — generalized from `react-markdown-report` v1.0.1
**Scope:** Complete codebase specification for a general-purpose Markdown-to-web
renderer — all 10 source files, ~520 LOC, configurable badge system,
frontmatter support, error boundaries, and full accessibility compliance.
