---
name: markdown-to-web
description: >
  Renders an arbitrary Markdown document as a polished, single-file,
  accessible web page. Template-driven theming (editorial default),
  tag-registry badges, fence-aware TOC with verified slug parity,
  error boundaries, dark mode via runtime CSS variables, and an
  eight-gate pre-ship checklist. Conformance: WCAG 2.2 AA enforced
  by axe gate; AAA where feasible with enumerated exceptions (§9.3).
  Built on React 19 + Vite 7 + Tailwind CSS v4 + react-markdown.
version: 3.0.0
---

**Purpose:** Enable any agent to convert an arbitrary `.md` file into a beautiful, accessible, self-contained web page — and to understand, maintain, extend, or rebuild the renderer without rediscovering its conventions, pitfalls, or evidence contract.

**When to use:** Audit reports, documentation, READMEs, articles, specifications, research notes — any long-form markdown that needs a shareable `index.html`.

**Output of this skill:** This document (`markdown-to-web_SKILL.md`), the reference code embedded in it, and the build artifact `dist/index.html`.

**Supersedes:** `react-markdown-report` v1.0.1 (original), drafts `markdown-to-web-renderer` v2.0.0 ("k"), `markdown-to-web` v1.0.0 ("d"), "Production-Grade…" v2.0.0 ("q2"), and the validation-review spec ("z"). Migration paths: §23.

---

## Table of Contents

1. [Identity and Purpose](#1-identity-and-purpose)
2. [Tech Stack and Environment](#2-tech-stack-and-environment)
3. [Bootstrapping and Configuration](#3-bootstrapping-and-configuration)
4. [The Design System](#4-the-design-system)
5. [Content Pipeline](#5-content-pipeline)
6. [Component Architecture](#6-component-architecture)
7. [Badge and Annotation System](#7-badge-and-annotation-system)
8. [TOC and Navigation](#8-toc-and-navigation)
9. [Accessibility](#9-accessibility)
10. [Error Handling and Resilience](#10-error-handling-and-resilience)
11. [Fonts and Offline Support](#11-fonts-and-offline-support)
12. [Testing and Quality Gates](#12-testing-and-quality-gates)
13. [Anti-Patterns and Common Bugs](#13-anti-patterns-and-common-bugs)
14. [Debugging Guide](#14-debugging-guide)
15. [Pre-Ship Checklist](#15-pre-ship-checklist)
16. [Lessons Learnt](#16-lessons-learnt)
17. [Pitfalls to Avoid](#17-pitfalls-to-avoid)
18. [Best Practices](#18-best-practices)
19. [Coding Patterns](#19-coding-patterns)
20. [Templates Beyond Editorial](#20-templates-beyond-editorial)
21. [Responsive and Z-Index Reference](#21-responsive-and-z-index-reference)
22. [TypeScript Reference](#22-typescript-reference)
23. [Migration Guide](#23-migration-guide)
24. [Verification and Evidence Ledger](#24-verification-and-evidence-ledger)

Appendices: [A — Build Output](#appendix-a--build-output) · [B — Correction Ledger](#appendix-b--correction-ledger) · [C — Adopter Spot-Check](#appendix-c--adopter-spot-check)

---

## 1. Identity and Purpose

**One-sentence description:** A zero-backend React application that renders any Markdown document as a polished, navigable, single-file web page, where the document's structure drives the UI, a template drives the look, and registered inline annotations render as semantic badges.

**Core tenets:**

1. **Content is sovereign.** The markdown file determines structure. The renderer never invents content. Editing markdown never requires code changes.
2. **One rendering pipeline.** `react-markdown` + components map. No `dangerouslySetInnerHTML`, no HTML-string serialization, no raw-HTML injection into the markdown source (closes q2's dual-pipeline ambiguity and d's dead raw-HTML pattern — §13 rows 9–10).
3. **Tags are registered, not hardcoded.** Badges are data in a registry; the resolver is generic; value collisions fail fast at load (§7).
4. **Single-file portability, honestly stated.** JS/CSS are inlined; fonts are a runtime dependency by default, with an opt-in offline build (§11).
5. **Accessibility is gated, not claimed.** Conformance claim: **WCAG 2.2 AA, enforced by an axe gate; AAA where feasible, with enumerated exceptions (§9.3).** This document never claims AAA wholesale.
6. **No generic UI (per template).** The editorial template uses bespoke editorial design. Other templates may choose a different register — the anti-generic mandate applies per template, not globally.

**Anti-generic mandate (editorial template, explicitly rejected):** purple gradients on white; predictable card-grid layouts with left-border accents; generic "Inter + gray-50" neutrality; hero sections with centered H1 + paragraph + CTA; any component droppable into a different project without visual friction.

### 1.1 Inputs contract

| Input | Required | Format | Notes |
|---|---|---|---|
| Markdown file | Yes | `.md`, UTF-8 | GFM supported: tables, strikethrough, task lists, autolinks |
| Template | No (default `editorial`) | `editorial` \| `technical` \| `minimal` | §4, §20 |
| Tag registry | No (template default) | TS module or JSON | §7 |
| Frontmatter | No | flat `key: value` YAML | title/subtitle/author/date/template; §3.4 |
| Offline fonts | No (default off) | build flag | §11 |

**Supported:** headings H1–H6 (TOC indexes H2–H4), paragraphs, emphasis, inline code, fenced code blocks, blockquotes, lists, task lists, GFM tables, links, horizontal rules, inline images (with the §11.3 caveat).

**Not supported (opt-in extensions, §20.4):** footnotes, math/KaTeX, mermaid, setext headings in TOC (§8.4 limitation), multi-document sets.

**Explicitly out of scope:** SSR/API routes/databases, slide decks, PDF output, interactive code execution, documents under ~500 words (render inline instead).

---

## 2. Tech Stack and Environment

| Layer | Technology | Version | Provenance / note |
|---|---|---|---|
| Framework | React | **19.2.6** | Lineage-verified (v1.0.1 `package.json`) |
| Build | Vite | **7.3.2** | Lineage-verified |
| Styling | Tailwind CSS | **4.1.17** | CSS-first `@theme inline`; no `tailwind.config.js` |
| Markdown | react-markdown | **10.1.0** | + `remark-gfm`, `rehype-slug` |
| GFM | remark-gfm | **4.0.1** | Lineage-consistent major for react-markdown 10 |
| Heading anchors | rehype-slug | **6.0.0** | Must match `github-slugger` output (§8.3 test) |
| TOC slugs | github-slugger | **2.0.0** | Default export class; **no named `slug` export exists** (§13 row 7) |
| Icons | lucide-react | **1.28.0 — Unverified** | See gate V-1 below. If install fails to resolve, use the current 0.x line and update this row |
| Class util | clsx + tailwind-merge | **2.1.1 / 3.4.0** | `cn()` — actively used (in `Badge`, template components) |
| Packaging | vite-plugin-singlefile | **2.3.0** | Inlines JS/CSS into `dist/index.html` |
| Syntax highlight | rehype-highlight + highlight.js | ^7 / ^11 (Assumed) | **Opt-in** (§11 of the pipeline); confirm at install |
| Fonts (offline mode) | @fontsource-variable/source-serif-4, @fontsource-variable/inter, @fontsource/jetbrains-mono | latest (Assumed) | §11.2 |
| TypeScript | typescript | **5.9.3** | `strict: true`, `noUnusedLocals`, `noUnusedParameters` |
| Test | vitest | ^2 (Assumed) | Unit tests, coverage thresholds §12.5 |
| A11y gate | @playwright/test + @axe-core/playwright | ^1.40 / ^4 (Assumed) | §9.4, §12.3 |
| Lint | eslint + typescript-eslint + eslint-plugin-react-hooks + eslint-plugin-jsx-a11y | ^9 (Assumed) | Flat config |
| Node | — | **≥20.19 or ≥22.12** | Vite 7 requirement |

**Version discipline:** exact pins for everything lineage-verified; caret ranges only for additions this merge introduces (testing/lint/highlight), each tagged *Assumed* until install.

**Gate V-1 (version verification, mandatory):**

```bash
npm ls --depth=0
# Every row above must appear at the stated version.
# lucide-react: confirm the resolved version and correct this table if it differs.
```

Never repeat a version number from memory or from another document. `npm ls` is the only source of truth (closes the lucide-react 1.28.0-vs-0.400.0 drift across drafts).

---

## 3. Bootstrapping and Configuration

### 3.1 Commands

```bash
# Install (package-lock.json is committed — never hand-edit it or package.json)
npm install

# Development server
npm run dev

# Typecheck (strict) — a real npm script, not npx improvisation
npm run typecheck

# Lint (zero-warning policy)
npm run lint

# Unit tests (enhance, toc, tags, slug parity)
npm run test

# Accessibility gate (Playwright + axe against vite preview)
npm run a11y

# Production build → single dist/index.html
npm run build

# Offline build (fonts inlined — §11.2, Reasoned sketch)
npm run build:offline

# Serve the build
npm run preview

# Version gate V-1
npm run versions:check
```

`package.json` scripts (the single definition every other section references — no section may cite a script not listed here):

```json
{
  "scripts": {
    "dev": "vite",
    "typecheck": "tsc --noEmit",
    "lint": "eslint . --max-warnings 0",
    "test": "vitest run",
    "test:watch": "vitest",
    "a11y": "playwright test",
    "build": "vite build",
    "build:offline": "node scripts/build-offline.mjs",
    "preview": "vite preview",
    "versions:check": "npm ls --depth=0"
  }
}
```

### 3.2 Bootstrap from scratch

No starter repository ships with this document. To instantiate:

```bash
npm create vite@latest markdown-to-web -- --template react-ts
cd markdown-to-web
npm install react-markdown remark-gfm rehype-slug github-slugger \
  clsx tailwind-merge lucide-react vite-plugin-singlefile
npm install -D tailwindcss @tailwindcss/vite vitest @vitest/coverage-v8 \
  @playwright/test @axe-core/playwright eslint typescript-eslint \
  eslint-plugin-react-hooks eslint-plugin-jsx-a11y
# Opt-in syntax highlighting:
npm install rehype-highlight highlight.js
# Opt-in offline fonts:
npm install @fontsource-variable/source-serif-4 @fontsource-variable/inter @fontsource/jetbrains-mono
```

Then create the file tree in §6.1 and run gate V-1 before anything else.

### 3.3 Configuration files

| File | Purpose | Critical settings |
|---|---|---|
| `vite.config.ts` | Plugins + alias | `react()`, `tailwindcss()`, `viteSingleFile()`, `alias: { "@": "src" }`, `build.target: "es2022"` |
| `tsconfig.json` | Strict TS | `strict`, `noUnusedLocals`, `noUnusedParameters`, `moduleResolution: "bundler"`, `paths: { "@/*": ["src/*"] }` |
| `eslint.config.js` | Flat config | typescript-eslint + react-hooks + jsx-a11y |
| `vitest.config.ts` | Tests + coverage | §12.5 |
| `playwright.config.ts` | A11y gate server | §12.3 |
| `index.html` | Entry | `<div id="root">` + module script |
| `src/index.css` | Tailwind entry + theme | §4 — all `@import` statements before `@import "tailwindcss"` |

**Configuration surface (deliberately small):** frontmatter (§3.4) + template choice + `tags` module. There is **no** `defineConfig` helper, no `virtual:` module, no build-time config-object plugin. That architecture was considered and rejected: it depends on packaging machinery the skill does not provide, and user-supplied Tailwind class strings inside config files are invisible to Tailwind's scanner unless the file happens to be scanned (dynamic-class hazard). If you need richer build-time configuration, that is an extension project, not a flag.

### 3.4 Frontmatter

```yaml
---
title: "Document Title"
subtitle: "Optional subtitle"
author: "Author Name"
date: "2026-08-06"
template: "editorial"
---
```

Parser (`src/lib/frontmatter.ts`) — carried from draft k with limitations disclosed:

```ts
export interface Frontmatter {
  title?: string;
  subtitle?: string;
  author?: string;
  date?: string;
  template?: string;
  [key: string]: string | undefined;
}

export function extractFrontmatter(markdown: string): Frontmatter {
  const match = markdown.match(/^---\n([\s\S]*?)\n---\n/);
  if (!match) return {};
  const out: Frontmatter = {};
  for (const line of match[1].split("\n")) {
    const [key, ...rest] = line.split(":");
    if (key && rest.length > 0) {
      out[key.trim()] = rest.join(":").trim().replace(/^["']|["']$/g, "");
    }
  }
  return out;
}
```

**Known limitations (disclosed, by design):** flat `key: value` only; no nested YAML, arrays, or multiline values; requires LF line endings and no BOM at file start (CRLF/BOM files fall back to empty frontmatter and still render); malformed frontmatter is silently ignored. If a document needs real YAML semantics, swap in `gray-matter` — it is the one dependency upgrade that preserves every contract in this document.

Usage: `title` → `<title>` + hero H1 · `subtitle` → hero paragraph · `author`/`date` → meta line · `template` → template selection.

---

## 4. The Design System

### 4.1 Architecture: two-layer tokens (the dark-mode fix)

Draft z proposed `@theme` inside `@media (prefers-color-scheme: dark)`. **That is invalid Tailwind v4** — `@theme` is a build-time, top-level directive. The correct idiom (draft d's mechanics, corrected and formalized):

- **Layer 1 — runtime variables** (`:root`, flipped by media query / `[data-theme]`): the actual color values.
- **Layer 2 — `@theme inline`**: bridges runtime variables into Tailwind utilities, so `bg-paper-50` compiles to `background-color: var(--paper-50)` and flips live at runtime.

**Theming rule:** dark mode happens exclusively through variable flipping. Templates must not use `dark:` utilities — one mechanism, no drift.

`src/index.css` (editorial template; full listing):

```css
@import url("https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap");
@import "tailwindcss";

/* ---------- Layer 1: runtime palette (the only values that flip) ---------- */
:root {
  --ink-950: #0b1615;
  --ink-900: #0f1e1c;
  --ink-800: #16302c;
  --ink-700: #204640;
  --paper-50: #fbfaf7;
  --paper-100: #f4f2ec;
  --paper-200: #e9e5da;
  --teal-600: #0e7c86;
  --teal-700: #0b626a;
  --moss-500: #6fa661;
  --moss-600: #588650;
  /* Generic 5-step accent scale (replaces v1.0.1's audit-specific tokens) */
  --accent-1: #b3261e;
  --accent-2: #b45309;
  --accent-3: #a16207;
  --accent-4: #3f6212;
  --accent-5: #1d4ed8;
}

/* Dark: system preference — unless the user forced light */
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --ink-950: #f4f2ec;
    --ink-900: #fbfaf7;
    --ink-800: #e9e5da;
    --ink-700: #d6d0c0;
    --paper-50: #0b1615;
    --paper-100: #101f1d;
    --paper-200: #16302c;
    --teal-600: #2ba8b3;
    --teal-700: #4cc2cc;   /* brightened: meta text must stay ≥ 4.5:1 on dark */
    --moss-500: #8bc47f;
    --moss-600: #6fa661;
  }
}

/* Dark: manual override (after :root so equal specificity resolves by order) */
[data-theme="dark"] {
  --ink-950: #f4f2ec;
  --ink-900: #fbfaf7;
  --ink-800: #e9e5da;
  --ink-700: #d6d0c0;
  --paper-50: #0b1615;
  --paper-100: #101f1d;
  --paper-200: #16302c;
  --teal-600: #2ba8b3;
  --teal-700: #4cc2cc;
  --moss-500: #8bc47f;
  --moss-600: #6fa661;
}

/* ---------- Layer 2: bridge into Tailwind utilities ---------- */
@theme inline {
  --font-serif: "Source Serif 4", ui-serif, Georgia, serif;
  --font-sans: "Inter", ui-sans-serif, system-ui, sans-serif;
  --font-mono: "JetBrains Mono", ui-monospace, monospace;

  --color-ink-950: var(--ink-950);
  --color-ink-900: var(--ink-900);
  --color-ink-800: var(--ink-800);
  --color-ink-700: var(--ink-700);
  --color-paper-50: var(--paper-50);
  --color-paper-100: var(--paper-100);
  --color-paper-200: var(--paper-200);
  --color-teal-600: var(--teal-600);
  --color-teal-700: var(--teal-700);
  --color-moss-500: var(--moss-500);
  --color-moss-600: var(--moss-600);
  --color-accent-1: var(--accent-1);
  --color-accent-2: var(--accent-2);
  --color-accent-3: var(--accent-3);
  --color-accent-4: var(--accent-4);
  --color-accent-5: var(--accent-5);
}

/* ---------- Base ---------- */
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
}

::selection { background-color: var(--color-teal-600); color: white; }

:focus-visible {
  outline: 2px solid var(--color-teal-600);
  outline-offset: 2px;
  border-radius: 2px;
}

/* Code blocks (with opt-in rehype-highlight) */
pre code.hljs {
  border-radius: 0.5rem;
  padding: 1.25rem;
  font-size: 0.875rem;
  line-height: 1.7;
}
```

**Dark-mode semantics to remember:** token *names* keep their role (ink = text/surfaces-that-invert, paper = page backgrounds), so `text-ink-900` stays "primary text" in both modes. Accent tokens (§7) are used for badge text on *light chip surfaces that do not flip* — see §7.4.

### 4.2 Typography hierarchy (editorial)

| Role | Font | Weight | Mobile | Desktop | Color |
|---|---|---|---|---|---|
| H1 | Source Serif 4 | 600 | `text-3xl` | `sm:text-4xl lg:text-5xl` | ink-900 |
| H2 | Source Serif 4 | 600 | `text-2xl` | `sm:text-[1.75rem]` | ink-900 |
| H3 | Source Serif 4 | 600 | `text-xl` | `sm:text-2xl` | ink-800 |
| H4 | Source Serif 4 | 600 | `text-lg` | — | ink-700 |
| Body | Inter | 400 | `text-base` (16px) | — | stone-700 (light) |
| Meta / labels | JetBrains Mono | 500 | `text-xs`, tracking-wide | — | teal-700 |
| Badge | Inter | 600 | `text-xs`, uppercase, tracking-wide | — | per-accent (§9.3 exception) |
| Code inline | JetBrains Mono | 400 | `text-[0.85em]` | — | ink-800 |

### 4.3 Color reference drift prevention

The complete color table is **generated, not hand-maintained**: `node scripts/generate-color-ref.mjs` parses the Layer-1 variables in `src/index.css` and emits the markdown table below (prevents the v1.0.1 drift risk).

Compact script:

```js
// scripts/generate-color-ref.mjs
import { readFileSync } from "node:fs";
const css = readFileSync("src/index.css", "utf8");
const lightBlock = css.match(/:root\s*{([^}]*)}/)?.[1] ?? "";
for (const m of lightBlock.matchAll(/--([\w-]+):\s*(#[0-9a-fA-F]{6});/g)) {
  const hex = m[2].toLowerCase();
  const rgb = [1, 3, 5].map((i) => parseInt(hex.slice(i, i + 2), 16)).join(", ");
  console.log(`| \`${m[1]}\` | ${hex} | ${rgb} |`);
}
```

Current generated values (light mode): ink-950 `#0b1615` · ink-900 `#0f1e1c` · ink-800 `#16302c` · ink-700 `#204640` · paper-50 `#fbfaf7` · paper-100 `#f4f2ec` · paper-200 `#e9e5da` · teal-600 `#0e7c86` · teal-700 `#0b626a` · moss-500 `#6fa661` · moss-600 `#588650` · accent-1 `#b3261e` · accent-2 `#b45309` · accent-3 `#a16207` · accent-4 `#3f6212` · accent-5 `#1d4ed8`.

---

## 5. Content Pipeline

**One pipeline. No alternatives in core.** (Draft q2's HTML-string + `dangerouslySetInnerHTML` path and draft d's raw-HTML-injection path are both rejected — §13 rows 9–10.)

```
src/content/document.md  (?raw import)
        │
        ├─► extractFrontmatter(markdown) ─► Frontmatter ─► <title>, hero, meta
        │
        ├─► buildToc(markdown, maxDepth) ─► TocItem[] ─► TableOfContents
        │        (fence-aware; slug reservation; §8)
        │
        ├─► enhanceMarkdown(markdown, registry) ─► { enhanced, warnings }
        │        (fence-aware tag wrapping; build-time warnings; §7)
        │
        └─► ErrorBoundary ─► MarkdownRenderer
                 │
                 └─► ReactMarkdown (remark-gfm + rehype-slug [+ rehype-highlight, opt-in])
                          │
                          ├─► components map (h1–h4, p, a, strong, em, ul, ol, li,
                          │    hr, blockquote, code, pre, table, thead, tbody, tr, th, td)
                          │
                          └─► inline code ─► resolveBadge() ─► Badge | neutral <code>
```

Adding content: put the `.md` at `src/content/document.md` → optional frontmatter → optional `- **Tag:** value` bullets → `npm run typecheck && npm run test && npm run build`. No code changes.

---

## 6. Component Architecture

### 6.1 File inventory (~14 files, est. ~700 LOC — estimates are Reasoned, not measured)

| File | Purpose |
|---|---|
| `src/main.tsx` | Entry: `StrictMode` + `createRoot`; conditional offline-font imports (§11.2) |
| `src/App.tsx` | Layout shell: header, sidebar/drawer, hero, theme state, active-section observer |
| `src/index.css` | §4 in full |
| `src/content/document.md` | The input document |
| `src/components/MarkdownRenderer.tsx` | react-markdown + components map |
| `src/components/TableOfContents.tsx` | Recursive TOC nav (sidebar + drawer), pure props |
| `src/components/Badge.tsx` | Accent-styled badge |
| `src/components/ErrorBoundary.tsx` | Boundary + `ErrorFallback` (§10) |
| `src/components/SkipLink.tsx` | Skip-to-content |
| `src/components/ThemeToggle.tsx` | Light / dark / system |
| `src/lib/fence.ts` | Fence-aware line scanner (§8.1) |
| `src/lib/toc.ts` | `buildToc` (§8.2) |
| `src/lib/enhance.ts` | Tag preprocessor (§7.3) |
| `src/lib/tags.ts` | Registry validation, collision detection, resolver (§7.2) |
| `src/lib/frontmatter.ts` | §3.4 |
| `src/types/{tag,toc,template}.ts` | Named interfaces (§22) |
| `src/utils/cn.ts` | `clsx` + `tailwind-merge` — **actively used** in `Badge` and template components |
| `tests/*.test.ts`, `tests/e2e/axe.test.ts` | §12 |

### 6.2 Custom hooks

**None exist as standalone hooks.** Theme state, drawer state, and the active-section observer live inline in `App.tsx` (`useState` / `useEffect` / `useMemo`). Documented explicitly so no agent searches for a `hooks/` directory. If a template needs a focus trap (e.g., a search palette), add it in that template's layout, not as shared infrastructure.

### 6.3 Key patterns

`App.tsx` — single-purpose state: `drawerOpen`, `theme`, `activeSlug`. Nothing else. No global stores.

```tsx
// Theme handling (inline, not a hook)
const [theme, setTheme] = useState<"system" | "light" | "dark">(() => {
  try {
    const stored = localStorage.getItem("theme");
    if (stored === "light" || stored === "dark") return stored;
  } catch { /* storage unavailable (sandboxed iframe/file://) — fall through */ }
  return "system";
});

useEffect(() => {
  const root = document.documentElement;
  if (theme === "system") root.removeAttribute("data-theme");
  else root.setAttribute("data-theme", theme);
  try { localStorage.setItem("theme", theme); } catch { /* ignore */ }
}, [theme]);
```

Derived data is memoized against the raw markdown string:

```tsx
const frontmatter = useMemo(() => extractFrontmatter(markdown), [markdown]);
const toc = useMemo(() => buildToc(markdown, 4), [markdown]);
const { enhanced, warnings } = useMemo(
  () => enhanceMarkdown(markdown, registry),
  [markdown, registry],
);
// Surface warnings during development:
if (import.meta.env.DEV && warnings.length > 0) console.warn(warnings.join("\n"));
```

Active-section highlight (flattened — observes **all** TOC levels, not just top-level):

```tsx
function flattenToc(items: TocItem[]): TocItem[] {
  return items.flatMap((i) => [i, ...flattenToc(i.children)]);
}

useEffect(() => {
  const observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting) setActiveSlug(entry.target.id);
      }
    },
    { rootMargin: "-80px 0px -80% 0px" },
  );
  for (const item of flattenToc(toc)) {
    const el = document.getElementById(item.slug);
    if (el) observer.observe(el);
  }
  return () => observer.disconnect();
}, [toc]);
```

`MarkdownRenderer.tsx` — renderer as configuration (load-bearing entries shown; every other element follows the same bespoke-class pattern):

```tsx
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeSlug from "rehype-slug";
import type { ComponentPropsWithoutRef } from "react";
import { Badge } from "@/components/Badge";
import { resolveBadge } from "@/lib/tags";
import type { TagRegistry } from "@/types/tag";

interface Props {
  markdown: string;
  registry: TagRegistry;
}

export function MarkdownRenderer({ markdown, registry }: Props) {
  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      rehypePlugins={[rehypeSlug]}
      components={{
        h2: ({ id, children }: ComponentPropsWithoutRef<"h2">) => (
          <h2 id={id} className="mt-12 scroll-mt-24 font-serif text-2xl font-semibold tracking-tight text-ink-900 sm:text-[1.75rem]">
            {children}
          </h2>
        ),
        // h3, h4: same shape, smaller sizes, scroll-mt-24 on every anchored heading
        code: ({ className, children }: ComponentPropsWithoutRef<"code">) => {
          const isBlock = Boolean(className); // language-* class exists only on blocks
          if (isBlock) return <code className={className}>{children}</code>;
          const badge = resolveBadge(registry, String(children));
          return badge
            ? <Badge tag={badge.tag} value={badge.label} accent={badge.accent} />
            : <code className="rounded bg-paper-100 px-1.5 py-0.5 font-mono text-[0.85em] text-ink-800">{children}</code>;
        },
        a: ({ href, children }: ComponentPropsWithoutRef<"a">) => {
          const external = href?.startsWith("http");
          return (
            <a
              href={href}
              className="text-teal-700 underline decoration-teal-600/40 hover:decoration-teal-600"
              {...(external ? { target: "_blank", rel: "noopener noreferrer" } : {})}
            >
              {children}
            </a>
          );
        },
      }}
    >
      {markdown}
    </ReactMarkdown>
  );
}
```

Syntax highlighting is **opt-in**: install `rehype-highlight`, add it to `rehypePlugins` after `rehypeSlug`, and import a highlight.js theme CSS. If you fork this pipeline into something that serializes HTML strings, sanitization (`rehype-sanitize`) becomes mandatory — in the components-map pipeline above it is not needed because no raw HTML is ever rendered.

`TableOfContents.tsx` — pure recursion, no internal state:

```tsx
interface Props {
  items: TocItem[];
  activeSlug?: string;
  onNavigate?: () => void;
}
// TocLink renders item + nested children with ml-3 border-l indent;
// activeSlug === item.slug gets the highlight classes.
```

---

## 7. Badge and Annotation System

### 7.1 Design

v1.0.1 hardcoded 9 keys and matched only `-` bullets. v3 replaces this with: **tag registry (data) + fence-aware preprocessor (with warnings) + generic resolver (cross-category lookup with collision detection).**

### 7.2 Registry, validation, resolver (`src/lib/tags.ts`)

Types (`src/types/tag.ts`):

```ts
export interface TagValueDefinition {
  accent: 1 | 2 | 3 | 4 | 5;
  label?: string;          // defaults to the value, capitalized
}
export interface TagDefinition {
  name: string;            // canonical, as written in markdown: "Severity"
  values: Record<string, TagValueDefinition>;  // keys MUST be lowercase
}
export type TagRegistry = Record<string, TagDefinition>;
```

Editorial default registry (`src/templates/editorial/tags.ts`):

```ts
import type { TagRegistry } from "@/types/tag";

export const EDITORIAL_TAGS: TagRegistry = {
  Severity: {
    name: "Severity",
    values: {
      critical:      { accent: 1 },
      high:          { accent: 2 },
      medium:        { accent: 3 },
      low:           { accent: 4 },
      informational: { accent: 5 },
    },
  },
  Confidence: {
    name: "Confidence",
    values: {
      verified:     { accent: 1 },
      reasoned:     { accent: 2 },
      assumed:      { accent: 3 },
      unverifiable: { accent: 4 },
    },
  },
};
```

Validation + resolution — **this is the D2 contract**: the inline `code` element carries only the value, so the resolver scans all categories; ambiguity is impossible because collisions throw at load time.

```ts
import type { TagDefinition, TagRegistry } from "@/types/tag";

export interface ResolvedBadge {
  tag: string;                        // canonical tag name
  value: string;                      // normalized lowercase key
  label: string;                      // display label
  accent: 1 | 2 | 3 | 4 | 5;
}

export function validateRegistry(registry: TagRegistry): string[] {
  const errors: string[] = [];
  const owners = new Map<string, string>();
  for (const def of Object.values(registry)) {
    if (!def.name) errors.push("tag definition missing name");
    for (const [value, v] of Object.entries(def.values)) {
      if (value !== value.toLowerCase()) {
        errors.push(`tag "${def.name}": value "${value}" must be registered lowercase`);
      }
      if (v.accent < 1 || v.accent > 5) {
        errors.push(`tag "${def.name}", value "${value}": accent must be 1–5`);
      }
      const owner = owners.get(value);
      if (owner !== undefined) {
        errors.push(
          `badge value collision: "${value}" is registered in both "${owner}" and "${def.name}" — values must be unique across the preset`,
        );
      } else {
        owners.set(value, def.name);
      }
    }
  }
  return errors;
}

export function loadRegistry(registry: TagRegistry): TagRegistry {
  const errors = validateRegistry(registry);
  if (errors.length > 0) {
    throw new Error(`Invalid tag registry:\n${errors.map((e) => `  - ${e}`).join("\n")}`);
  }
  return registry;
}

export function resolveBadge(registry: TagRegistry, raw: string): ResolvedBadge | null {
  const value = raw.trim().toLowerCase();
  if (value === "") return null;
  for (const def of Object.values(registry)) {
    const v = def.values[value];
    if (v) {
      return {
        tag: def.name,
        value,
        label: v.label ?? value.charAt(0).toUpperCase() + value.slice(1),
        accent: v.accent,
      };
    }
  }
  return null;
}
```

Call `loadRegistry` once at module load in `App.tsx`. A colliding registry is a build/startup error that names both categories — never a silent render-time guess.

### 7.3 Preprocessor (`src/lib/enhance.ts`)

Fence-aware, accepts all bullet styles, emits warnings, leaves unmatched lines byte-identical:

```ts
import { scanLines } from "@/lib/fence";
import type { TagDefinition, TagRegistry } from "@/types/tag";

const BADGE_LINE_RE = /^(\s*(?:[-*+]\s+|\d{1,9}[.)]\s+))\*\*([^*]+):\*\*\s+(.+)$/;

export interface EnhanceResult {
  enhanced: string;
  warnings: string[];
}

function findTag(registry: TagRegistry, raw: string): TagDefinition | undefined {
  const lower = raw.toLowerCase();
  return Object.values(registry).find((d) => d.name.toLowerCase() === lower);
}

export function enhanceMarkdown(markdown: string, registry: TagRegistry): EnhanceResult {
  const warnings: string[] = [];
  const out: string[] = [];
  for (const { line, lineNumber, insideFence } of scanLines(markdown)) {
    if (insideFence) { out.push(line); continue; }
    const match = line.match(BADGE_LINE_RE);
    if (!match) { out.push(line); continue; }
    const [, bullet, rawTag, rawValue] = match;
    const def = findTag(registry, rawTag.trim());
    if (!def) { out.push(line); continue; }   // bold bullet, unregistered tag → untouched
    const value = rawValue.trim();
    if (!def.values[value.toLowerCase()]) {
      warnings.push(
        `line ${lineNumber}: unknown value "${value}" for tag "${def.name}". ` +
        `Allowed: ${Object.keys(def.values).join(", ")}`,
      );
      out.push(line);
      continue;
    }
    out.push(`${bullet}**${def.name}:** \`${value}\``);
  }
  return { enhanced: out.join("\n"), warnings };
}
```

Markdown syntax for badges:

```markdown
- **Severity:** critical
* **Confidence:** verified
+ **Status:** done
1. **Priority:** high
```

**Disclosed blind spots (do not "fix" silently):** badges inside blockquotes (`> - **Tag:** v`) are not matched; values with trailing punctuation (`critical.`) warn and render unstyled; only first-level bullets are targeted. Each is covered by a fixture in §12.1.

### 7.4 Badge component

```tsx
import { cn } from "@/utils/cn";

const ACCENT_STYLES: Record<1 | 2 | 3 | 4 | 5, string> = {
  1: "bg-red-50 ring-red-200 text-accent-1",
  2: "bg-amber-50 ring-amber-200 text-accent-2",
  3: "bg-yellow-50 ring-yellow-200 text-accent-3",
  4: "bg-lime-50 ring-lime-200 text-accent-4",
  5: "bg-blue-50 ring-blue-200 text-accent-5",
};

interface BadgeProps {
  tag: string;
  value: string;
  accent: 1 | 2 | 3 | 4 | 5;
}

export function Badge({ tag, value, accent }: BadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full px-2 py-0.5",
        "font-sans text-xs font-semibold uppercase tracking-wide",
        "ring-1 ring-inset",
        ACCENT_STYLES[accent],
      )}
      data-tag={tag}
    >
      {value}
    </span>
  );
}
```

**Dark-mode note (deliberate):** chip backgrounds/rings use the static Tailwind default palette, so chips stay light-surface in both modes. Accent text contrast is therefore identical in light and dark — computed against the chip, not the page (§9.3). All badge classes live in source files Tailwind scans; never move them into runtime-provided strings (§13 row 11).

---

## 8. TOC and Navigation

### 8.1 Fence-aware scanner (`src/lib/fence.ts`)

Shared by `buildToc` and `enhanceMarkdown`. Fixes the fence-blind line regexes of v1.0.1/k/z — a `## comment` inside a code fence must neither enter the TOC nor consume a slug counter:

```ts
export interface MarkdownRegion {
  line: string;
  lineNumber: number;   // 1-based
  insideFence: boolean;
}

/**
 * CommonMark-subset fence tracking: opening fence is ``` or ~~~ (up to 3
 * leading spaces); closing fence is the same character, at least as long,
 * with no other content. Unclosed fences extend to end of document.
 * Both delimiter lines are reported as insideFence: true.
 */
export function scanLines(markdown: string): MarkdownRegion[] {
  const regions: MarkdownRegion[] = [];
  let inFence = false;
  let fenceChar = "";
  let fenceLen = 0;

  const lines = markdown.split("\n");
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const m = line.match(/^ {0,3}(`{3,}|~{3,})(.*)$/);
    if (m) {
      const marker = m[1];
      const rest = m[2];
      if (!inFence) {
        inFence = true;
        fenceChar = marker.charAt(0);
        fenceLen = marker.length;
        regions.push({ line, lineNumber: i + 1, insideFence: true });
        continue;
      }
      if (marker.charAt(0) === fenceChar && marker.length >= fenceLen && rest.trim() === "") {
        inFence = false;
        fenceChar = "";
        fenceLen = 0;
        regions.push({ line, lineNumber: i + 1, insideFence: true });
        continue;
      }
    }
    regions.push({ line, lineNumber: i + 1, insideFence: inFence });
  }
  return regions;
}
```

### 8.2 Extraction with slug reservation (`src/lib/toc.ts`)

Two correctness mechanisms:

1. **Stack algorithm** (hand-traced: nested, sibling-after-nested, orphan, and mixed cases all correct — draft q2's variant is *not* used; it mis-nests any H2 that follows an H3).
2. **Slug reservation for every heading level** — `rehype-slug` slugs H1–H6 in document order with dedup counters; a TOC that only sees H2–H4 would desync on duplicate text (e.g. `# Intro` then `## Intro`). The slugger therefore consumes every heading; only H2–H4 enter the tree.

```ts
import GithubSlugger from "github-slugger";   // default export — there is no named { slug }
import { scanLines } from "@/lib/fence";

export interface TocItem {
  level: 2 | 3 | 4;
  text: string;
  slug: string;
  children: TocItem[];
}

const ANY_HEADING_RE = /^(#{1,6})\s+(.+)$/;

export function buildToc(markdown: string, maxDepth: 2 | 3 | 4 = 4): TocItem[] {
  const slugger = new GithubSlugger();
  const items: TocItem[] = [];
  const stack: TocItem[] = [];

  for (const { line, insideFence } of scanLines(markdown)) {
    if (insideFence) continue;
    const match = line.match(ANY_HEADING_RE);
    if (!match) continue;

    const level = match[1].length;
    const text = match[2].replace(/`/g, "").trim();
    const slug = slugger.slug(text);          // reserve the slug at EVERY level

    if (level < 2 || level > maxDepth) continue;

    const item: TocItem = { level: level as 2 | 3 | 4, text, slug, children: [] };
    while (stack.length > 0 && stack[stack.length - 1].level >= level) {
      stack.pop();
    }
    if (stack.length === 0) items.push(item);
    else stack[stack.length - 1].children.push(item);
    stack.push(item);
  }
  return items;
}
```

Contract: H2 = depth 1 · H3 = depth 2 (`ml-3 border-l`) · H4 = depth 3 (`ml-6 border-l`) · orphans promote to top level · backticks stripped from display text (matching hast text content, which is what `rehype-slug` hashes).

### 8.3 Slug parity — tested, not asserted

The lineage's most-cited failure mode ("two slug generators must stay in sync") is closed by a test that **compiles and runs**: correct default import, no unused imports (passes the strict `noUnusedLocals` gate the skill itself mandates), fixtures for CJK, emoji, inline code, duplicates, and cross-level dedup.

`tests/slug-parity.test.ts`:

```ts
import { describe, it, expect } from "vitest";
import GithubSlugger from "github-slugger";
import rehypeSlug from "rehype-slug";
import { unified } from "unified";
import remarkParse from "remark-parse";
import remarkRehype from "remark-rehype";
import type { Root as HastRoot } from "hast";
import { buildToc } from "@/lib/toc";

/** Slug that rehype-slug assigns to a lone H2 with the given markdown content. */
async function rehypeH2Id(headingMarkdown: string): Promise<string | undefined> {
  const mdast = unified().use(remarkParse).parse(`## ${headingMarkdown}`);
  const hast = (await unified()
    .use(remarkRehype)
    .use(rehypeSlug)
    .run(mdast)) as unknown as HastRoot;
  for (const child of hast.children) {
    if (child.type === "element" && child.tagName === "h2") {
      const id = child.properties?.id;
      return typeof id === "string" ? id : undefined;
    }
  }
  return undefined;
}

const FIXTURES = [
  "Simple Heading",
  "Heading with emoji 🎉",
  "中文标题",
  "CamelCase",
  "snake_case",
  "kebab-case",
  "  Leading whitespace  ",
];

describe("slug parity: github-slugger === rehype-slug", () => {
  for (const text of FIXTURES) {
    it(`matches for "${text}"`, async () => {
      const slugger = new GithubSlugger();
      expect(slugger.slug(text)).toBe(await rehypeH2Id(text));
    });
  }

  it("matches for headings containing inline code (TOC strips backticks)", async () => {
    const slugger = new GithubSlugger();
    // rehype-slug hashes hast text content, where inline code contributes its text
    expect(slugger.slug("Code in Heading")).toBe(await rehypeH2Id("`Code` in Heading"));
  });

  it("buildToc dedup counters stay in sync across heading levels", () => {
    // rehype-slug sees ALL headings: # dup → "dup", ## dup → "dup-1", ## dup → "dup-2"
    const toc = buildToc("# Dup\n\n## Dup\n\n## Dup\n", 4);
    expect(toc.map((t) => t.slug)).toEqual(["dup-1", "dup-2"]);
  });

  it("fenced headings consume no slugs anywhere", () => {
    const toc = buildToc("```\n## Not Indexed\n```\n\n## Real\n", 4);
    expect(toc.map((t) => t.slug)).toEqual(["real"]);
  });
});
```

Both packages are pinned (§2); this test runs in CI. **Known scope limitation (§8.4):** parity is guaranteed for ATX headings only.

### 8.4 Disclosed limitations

- **Setext headings** (`Title\n=====`) are invisible to the line-based extractor but real to `rehype-slug` — they can desync dedup counters for later duplicate text. Content convention: **ATX headings only.** If a document type needs setext support, migrate extraction to the AST (the extension path in §20.4 — this is the one place AST parsing earns its complexity).
- Headings deeper than `maxDepth` are still slug-reserved (correct) but not listed.
- `scroll-mt-24` on every anchored heading compensates for the sticky header; never hand-write heading `id`s.

---

## 9. Accessibility

### 9.1 Posture (the honesty fix)

**Claim: WCAG 2.2 AA, enforced by an automated axe gate. AAA where feasible; every exception is enumerated in §9.3.** This document never states "WCAG AAA" as a headline, and it explicitly rejects the arithmetic error that appeared in draft z ("14px relaxes the AAA threshold") — WCAG large text is ≥18pt (24px) or ≥14pt bold (≈18.66px); no font size used here qualifies, so normal-text thresholds apply everywhere (Verified — stable WCAG definitions).

### 9.2 Implementation

| Feature | Implementation | Verification |
|---|---|---|
| Skip-to-content | `<a href="#content">` with `sr-only focus:not-sr-only focus:z-50` | Manual: Tab → Enter → focus lands on `#content` |
| Focus visible | Global `:focus-visible` ring (§4.1), all interactive elements | axe `focus-order-semantics`; manual Tab pass |
| Heading hierarchy | H1 → H2 → H3 → H4, no skipped levels | axe `heading-order` |
| Anchor offset | `scroll-mt-24` on H2–H4 | Manual TOC click |
| Reduced motion | `prefers-reduced-motion` guard in base styles | Manual OS setting check |
| Touch targets | All interactive elements ≥ 44×44px (`min-w-11 min-h-11` or `p-2.5` + icon) — drawer, theme toggle, menu, close | axe; DevTools measurement |
| ARIA | `aria-label` on nav/drawer/toggle; `aria-hidden` on decorative icons; `role="alert"` on error fallback | axe `button-name`, `aria-valid-attr` |
| Landmarks | `header`, `main`, `aside`, `nav`, `article`, `footer` | axe `region` |
| Color isn't sole indicator | Badges carry text + tint | Deuteranopia simulation |
| Keyboard | Full Tab/Shift+Tab/Escape operability; drawer closes on Escape | Manual |
| Language | `<html lang>` set from frontmatter or `en` default | axe `html-has-lang` |
| Contrast (body) | ink-900 on paper-50 ≈ 16.4:1 (lineage-computed) — AAA ✓ | axe `color-contrast` |

### 9.3 Enumerated AAA exceptions (AA guaranteed, AAA not claimed)

| Item | Contrast (computed, Reasoned) | AA (4.5:1) | AAA (7:1) | Disposition |
|---|---|---|---|---|
| Badge text, accent-1 on red-50 | ≈5.9:1 | ✓ | ✗ | Exception; upgrade via §9.5 |
| Badge text, accent-2 on amber-50 | ≈4.8:1 | ✓ | ✗ | Exception; upgrade via §9.5 |
| Badge text, accent-3 on yellow-50 | ≈4.8:1 | ✓ | ✗ | Exception; upgrade via §9.5 |
| Badge text, accent-4 on lime-50 | ≈6.9:1 | ✓ | ✗ | Exception; upgrade via §9.5 |
| Badge text, accent-5 on blue-50 | ≈6.3:1 | ✓ | ✗ | Exception; upgrade via §9.5 |
| Meta labels, teal-700 on paper-50 | ≈6.6:1 | ✓ | ✗ | Exception; use ink-800 if AAA required |

Everything else targets AAA. Dark-mode pairs (e.g., teal-600-dark `#2ba8b3` on `#0b1615` ≈6.5:1) pass AA and are axe-checked in dark mode via `[data-theme="dark"]` before the run (§12.3).

### 9.4 The gate

Pre-ship command `npm run a11y` runs `tests/e2e/axe.test.ts` (§12.3): **AA violations fail the build; AAA violations are advisory except contrast and target-size.** No suppressions.

### 9.5 High-contrast badge recipe (opt-in AAA badges)

Swap Layer-1 accent variables for these (computed ≈8.5–9.2:1 on the standard chips — Reasoned; re-verify with the axe gate after applying):

```css
:root {
  --accent-1: #7f1d1d;   /* ≈9.1:1 on red-50 */
  --accent-2: #78350f;   /* ≈8.8:1 on amber-50 */
  --accent-3: #713f12;   /* ≈8.5:1 on yellow-50 */
  --accent-4: #365314;   /* ≈8.5:1 on lime-50 */
  --accent-5: #1e40af;   /* ≈8.1:1 on blue-50 */
}
```

---

## 10. Error Handling and Resilience

### 10.1 Error boundary (present in the skeleton — closes z's omission and d's absence)

```tsx
import React from "react";
import type { ErrorInfo, ReactNode } from "react";

interface BoundaryProps {
  children: ReactNode;
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
}
interface BoundaryState {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends React.Component<BoundaryProps, BoundaryState> {
  state: BoundaryState = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error): BoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    this.props.onError?.(error, errorInfo);
  }

  render(): ReactNode {
    if (this.state.hasError) return <ErrorFallback error={this.state.error} />;
    return this.props.children;
  }
}

export function ErrorFallback({ error }: { error: Error | null }) {
  return (
    <div role="alert" className="mx-auto my-16 max-w-xl rounded-lg border border-paper-200 bg-paper-100 p-6">
      <h2 className="font-serif text-xl font-semibold text-ink-900">This document couldn't be rendered</h2>
      <p className="mt-2 text-sm text-ink-700">
        The content failed to render. Try reloading; if the problem persists, the markdown source is shown below.
      </p>
      {import.meta.env.DEV && error && (
        <pre className="mt-4 overflow-auto rounded bg-ink-950 p-3 text-xs text-paper-100">{error.message}</pre>
      )}
      <button
        type="button"
        onClick={() => window.location.reload()}
        className="mt-4 min-h-11 min-w-11 rounded-md bg-teal-700 px-4 py-2 text-sm font-semibold text-white"
      >
        Reload page
      </button>
    </div>
  );
}
```

Placement: `main.tsx` wraps `<App />`. Keep it at the root only; use defensive checks (not nested boundaries) in pure functions.

### 10.2 Malformed markdown behavior

| Scenario | Behavior |
|---|---|
| Unclosed code fence | react-markdown renders remainder as code — no crash; fence scanner treats rest as fenced (matches CommonMark) |
| Broken table | Renders as plain text — no crash |
| Invalid frontmatter | Ignored; document renders with fallback title |
| Unknown badge value | Build-time warning; line renders unstyled — no crash |
| Colliding tag registry | Startup error naming both tags — fails fast, never renders ambiguously |
| Empty markdown | `buildToc` → `[]`; renderer shows empty article — no crash |

---

## 11. Fonts and Offline Support

### 11.1 Default (online) — honestly scoped

Google Fonts `@import` in `index.css`. **The single-file build does not inline these fonts.** `dist/index.html` therefore requires network for correct typography and falls back to system serif/sans/mono offline. This is documented in the build artifact's contract — never claim full self-containment for the default build.

### 11.2 Offline build (Reasoned sketch — untested; verify per Appendix C before relying on it)

Recipe: `@fontsource` packages imported conditionally in `main.tsx`, inlined by a high `assetsInlineLimit`.

```tsx
// main.tsx
if (import.meta.env.VITE_OFFLINE_FONTS === "true") {
  await import("@fontsource-variable/source-serif-4");
  await import("@fontsource-variable/inter");
  await import("@fontsource/jetbrains-mono");
}
```

```js
// scripts/build-offline.mjs
import { build } from "vite";
import { viteSingleFile } from "vite-plugin-singlefile";

await build({
  plugins: [viteSingleFile()],
  define: { "import.meta.env.VITE_OFFLINE_FONTS": JSON.stringify("true") },
  build: {
    target: "es2022",
    cssCodeSplit: false,
    assetsInlineLimit: 100 * 1024 * 1024,
    rollupOptions: { output: { inlineDynamicImports: true } },
  },
});
```

Expect 2–4 MB output (variable fonts); subset with `pyftsubset` if that matters. Top-level `await` in `main.tsx` requires the es2022 target already set. **Known unknowns:** exact interaction of `vite-plugin-singlefile` with font assets, and fontsource variable-font CSS order — both must be confirmed by a real offline build (Appendix C, step 6).

### 11.3 Images

Local images referenced from markdown are resolved by Vite relative to the importing module — for `?raw` markdown, place images in `src/assets/` and reference by root-absolute path, or accept that only remote URLs are zero-config. Base64-embedding images inflates the single file quickly; embed only small images, link large ones. This is a documented limitation, not a configured feature.

---

## 12. Testing and Quality Gates

### 12.1 Unit tests — complete, written against the actual implementations

`tests/fence.test.ts`:

```ts
import { describe, it, expect } from "vitest";
import { scanLines } from "@/lib/fence";

const flags = (md: string) => scanLines(md).map((r) => r.insideFence);

describe("scanLines fence tracking", () => {
  it("marks fence delimiters and body as inside", () => {
    expect(flags("before\n```\ninside\n```\nafter")).toEqual([false, true, true, true, false]);
  });
  it("handles tilde fences and longer closing markers", () => {
    expect(flags("~~~\nx\n~~~~\nafter")).toEqual([true, true, true, false]);
  });
  it("unclosed fence extends to end of document", () => {
    expect(flags("```\nstill\nstill")).toEqual([true, true, true]);
  });
  it("does not close a backtick fence with tildes", () => {
    expect(flags("```\n~~~\nx\n```")).toEqual([true, true, true, true]);
  });
  it("requires closing fence at least as long", () => {
    expect(flags("````\nx\n```\ny\n````")).toEqual([true, true, true, true, true]);
  });
});
```

`tests/enhance.test.ts`:

```ts
import { describe, it, expect } from "vitest";
import { enhanceMarkdown } from "@/lib/enhance";
import type { TagRegistry } from "@/types/tag";

const REGISTRY: TagRegistry = {
  Severity: { name: "Severity", values: { critical: { accent: 1 }, low: { accent: 4 } } },
  Status:   { name: "Status",   values: { done: { accent: 4 } } },
};

describe("enhanceMarkdown", () => {
  it("wraps registered values in backticks", () => {
    const { enhanced, warnings } = enhanceMarkdown("- **Severity:** critical", REGISTRY);
    expect(enhanced).toBe("- **Severity:** `critical`");
    expect(warnings).toEqual([]);
  });
  it("accepts *, +, and ordered bullets", () => {
    for (const bullet of ["* ", "+ ", "1. ", "2) "]) {
      const { enhanced } = enhanceMarkdown(`${bullet}**Severity:** low`, REGISTRY);
      expect(enhanced).toContain("`low`");
    }
  });
  it("matches tags case-insensitively, outputs canonical case", () => {
    const { enhanced } = enhanceMarkdown("- **severity:** critical", REGISTRY);
    expect(enhanced).toBe("- **Severity:** `critical`");
  });
  it("leaves fenced badge lines untouched", () => {
    const md = "```\n- **Severity:** critical\n```";
    expect(enhanceMarkdown(md, REGISTRY).enhanced).toBe(md);
  });
  it("leaves blockquoted badges untouched (documented blind spot)", () => {
    const md = "> - **Severity:** critical";
    expect(enhanceMarkdown(md, REGISTRY).enhanced).toBe(md);
  });
  it("warns on unknown values and leaves the line unchanged", () => {
    const md = "- **Severity:** catastrophic";
    const { enhanced, warnings } = enhanceMarkdown(md, REGISTRY);
    expect(enhanced).toBe(md);
    expect(warnings).toHaveLength(1);
    expect(warnings[0]).toContain("catastrophic");
  });
  it("leaves unregistered bold bullets unchanged without warning", () => {
    const md = "- **Note:** just text";
    const { enhanced, warnings } = enhanceMarkdown(md, REGISTRY);
    expect(enhanced).toBe(md);
    expect(warnings).toEqual([]);
  });
});
```

`tests/toc.test.ts`:

```ts
import { describe, it, expect } from "vitest";
import { buildToc } from "@/lib/toc";

describe("buildToc", () => {
  it("nests H3 under H2 and H4 under H3", () => {
    const toc = buildToc("## A\n### B\n#### C\n", 4);
    expect(toc).toHaveLength(1);
    expect(toc[0].children[0].children[0].slug).toBe("c");
  });
  it("re-nests an H2 after deeper levels (the q2 regression case)", () => {
    const toc = buildToc("## A\n### B\n## C\n", 4);
    expect(toc.map((t) => t.slug)).toEqual(["a", "c"]);
    expect(toc[1].children).toEqual([]);
  });
  it("promotes orphan headings to top level", () => {
    const toc = buildToc("### Orphan\n## Real\n", 4);
    expect(toc.map((t) => t.slug)).toEqual(["orphan", "real"]);
  });
  it("ignores fenced headings", () => {
    const toc = buildToc("```\n## Hidden\n```\n## Visible\n", 4);
    expect(toc.map((t) => t.slug)).toEqual(["visible"]);
  });
  it("respects maxDepth but still reserves slugs", () => {
    const toc = buildToc("## A\n#### Deep\n## A\n", 3);
    expect(toc.map((t) => t.slug)).toEqual(["a", "a-1"]);
  });
  it("returns [] for empty markdown", () => {
    expect(buildToc("", 4)).toEqual([]);
  });
});
```

`tests/tags.test.ts`:

```ts
import { describe, it, expect } from "vitest";
import { loadRegistry, resolveBadge, validateRegistry } from "@/lib/tags";
import type { TagRegistry } from "@/types/tag";

const OK: TagRegistry = {
  Severity: { name: "Severity", values: { critical: { accent: 1 } } },
  Confidence: { name: "Confidence", values: { verified: { accent: 1 } } },
};

describe("registry validation", () => {
  it("accepts a clean registry", () => {
    expect(validateRegistry(OK)).toEqual([]);
    expect(() => loadRegistry(OK)).not.toThrow();
  });
  it("detects cross-category value collisions", () => {
    const bad: TagRegistry = {
      Status: { name: "Status", values: { draft: { accent: 3 } } },
      Priority: { name: "Priority", values: { draft: { accent: 2 } } },
    };
    const errors = validateRegistry(bad);
    expect(errors.some((e) => e.includes("collision") && e.includes("Status") && e.includes("Priority"))).toBe(true);
    expect(() => loadRegistry(bad)).toThrow(/collision/);
  });
  it("rejects uppercase-registered values and out-of-range accents", () => {
    const bad: TagRegistry = {
      S: { name: "S", values: { Critical: { accent: 1 }, ok: { accent: 9 as 1 } } },
    };
    expect(validateRegistry(bad)).toHaveLength(2);
  });
});

describe("resolveBadge", () => {
  it("resolves across categories from value alone", () => {
    expect(resolveBadge(OK, "verified")?.tag).toBe("Confidence");
    expect(resolveBadge(OK, "  CRITICAL  ")?.tag).toBe("Severity");
  });
  it("returns null for unknown or empty values", () => {
    expect(resolveBadge(OK, "nope")).toBeNull();
    expect(resolveBadge(OK, "   ")).toBeNull();
  });
  it("capitalizes default labels", () => {
    expect(resolveBadge(OK, "critical")?.label).toBe("Critical");
  });
});
```

### 12.2 Coverage statement

Thresholds: 90% lines/functions/branches/statements project-wide (`vitest.config.ts` below). Core `lib/` modules (fence, toc, enhance, tags) carry a **goal** of 100% — stated as an aspiration enforced by review, not mislabeled as a verified fact.

```ts
// vitest.config.ts
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import { resolve } from "node:path";

export default defineConfig({
  plugins: [react()],
  resolve: { alias: { "@": resolve(__dirname, "src") } },
  test: {
    environment: "jsdom",
    setupFiles: ["./tests/setup.ts"],   // import "@testing-library/jest-dom" if component tests are added
    coverage: {
      provider: "v8",
      reporter: ["text", "json", "html"],
      exclude: ["node_modules/", "tests/", "**/*.d.ts", "**/*.config.*", "scripts/"],
      thresholds: { lines: 90, functions: 90, branches: 90, statements: 90 },
    },
  },
});
```

### 12.3 Accessibility gate

```ts
// playwright.config.ts
import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./tests/e2e",
  webServer: { command: "npm run preview", port: 4173, reuseExistingServer: false },
});
```

```ts
// tests/e2e/axe.test.ts
import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

test("document passes WCAG 2.2 AA (hard gate)", async ({ page }) => {
  await page.goto("/");
  const results = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa", "wcag22aa"])
    .analyze();
  expect(results.violations).toEqual([]);
});

test("AAA advisory: contrast and target size must still pass", async ({ page }) => {
  await page.goto("/");
  const results = await new AxeBuilder({ page })
    .withTags(["wcag2aaa", "wcag21aaa", "wcag22aaa"])
    .analyze();
  const enforced = results.violations.filter((v) =>
    ["color-contrast", "target-size"].includes(v.id),
  );
  expect(enforced).toEqual([]);
});

test("dark mode passes AA", async ({ page }) => {
  await page.goto("/");
  await page.evaluate(() => document.documentElement.setAttribute("data-theme", "dark"));
  const results = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa", "wcag22aa"])
    .analyze();
  expect(results.violations).toEqual([]);
});
```

### 12.4 CI (every script invoked here is defined in §3.1 — no phantom scripts)

```yaml
# .github/workflows/ci.yml
name: CI
on:
  push: { branches: [main] }
  pull_request: { branches: [main] }
jobs:
  quality:
    runs-on: ubuntu-latest
    strategy:
      matrix: { node-version: [20, 22] }
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: "${{ matrix.node-version }}", cache: npm }
      - run: npm ci
      - run: npm run versions:check
      - run: npm run lint
      - run: npm run typecheck
      - run: npm run test -- --coverage
      - run: npm run build
      - run: npx playwright install --with-deps chromium
      - run: npm run a11y
      - run: npm audit --audit-level=critical
```

---

## 13. Anti-Patterns and Common Bugs

| # | Anti-pattern | Symptom | Root cause | Fix |
|---|---|---|---|---|
| 1 | Badge renders as plain `<code>` | Gray monospace, no color | Value not wrapped by `enhance.ts` (unregistered tag/value, blockquote, or inside fence) | Check `enhance.ts` warnings; use exact bullet syntax; register the tag |
| 2 | Heading missing from TOC | Section absent from nav | Level > `maxDepth`, or heading inside a code fence | Adjust depth; move heading out of fence |
| 3 | TOC anchor mismatch | Jumps to wrong heading or top | Slug desync (versions drifted, setext heading, hand-edited id) | Run `tests/slug-parity.test.ts`; pin both slug packages; ATX only |
| 4 | Typecheck fails on unused imports | `tsc` errors | Strict `noUnusedLocals` | Delete the import — treat as an architectural signal |
| 5 | Fonts render as fallbacks | System fonts | Network blocked; default build uses CDN fonts | Use `npm run build:offline` |
| 6 | Code blocks not highlighted | Plain `<pre>` | `rehype-highlight` opt-in not wired | Add plugin + highlight.js CSS import |
| 7 | `import { slug } from "github-slugger"` | Build error | No named export exists; default class only | `import GithubSlugger from "github-slugger"` |
| 8 | Error boundary everywhere | Error UI for minor issues | Over-broad boundaries | One root boundary; defensive checks in pure code |
| 9 | Injecting raw HTML into markdown | Badges/markup silently vanish | react-markdown drops raw HTML without `rehype-raw` | Wrap values as code spans via `enhance.ts` — the supported path |
| 10 | Rendering via `dangerouslySetInnerHTML` | XSS surface, dual pipelines | HTML-string architecture | Use the components map (§5); if you must serialize, `rehype-sanitize` is mandatory |
| 11 | Badge classes in runtime config strings | Unstyled badges, no error | Tailwind can't see classes it didn't scan | Keep classes in source files (§7.4); registry carries accent *numbers*, not class strings |
| 12 | `@theme` inside `@media` | Dark mode silently dead | `@theme` is build-time, top-level only | Variable-flip pattern (§4.1) |
| 13 | Claiming AAA because "14px is bigger" | Conformance overclaim | Large text is ≥18pt / ≥14pt-bold; 14px ≠ large | §9.3 exceptions or §9.5 high-contrast recipe |
| 14 | Fence-blind line regexes | Fenced `## comment` in TOC; slug counters desync | Regex can't see fence state | Always go through `scanLines` |
| 15 | Duplicate badge values across tags | Ambiguous render | Collision in registry | `loadRegistry` throws — rename one value |

---

## 14. Debugging Guide

| Symptom | Cause | Fix |
|---|---|---|
| Build fails with `vite-plugin-singlefile` error | Version/config mismatch | Verify `viteSingleFile()` in plugins; gate V-1 |
| TOC anchor doesn't scroll | Missing `id` or `scroll-mt-24` | Check heading components; `rehypeSlug` present |
| TOC anchor wrong target | Slug desync | §13 row 3 |
| Badge wrong color | Registry accent mapping | Inspect `tags.ts`; check `enhance.ts` warnings |
| Startup error "badge value collision" | Two tags share a value | Rename one value; collision detection is intentional |
| Dark mode doesn't apply | `data-theme` not set, or `@theme` nested in media | Inspect `<html data-theme>`; verify §4.1 structure (no `@theme` inside `@media`) |
| Dark mode flickers on load | Theme applied after first paint | Set `data-theme` from a tiny inline script in `index.html` before the bundle |
| Theme toggle doesn't persist | Storage unavailable | Check `localStorage` try/catch path (§6.3); sandboxed contexts fall back to system |
| Active section never highlights | Observer watching top level only | Use `flattenToc` (§6.3) |
| `lucide-react` install fails | Pinned version may not exist | Gate V-1; install current 0.x, update §2 table |
| Offline build huge | Full variable fonts inlined | Subset with `pyftsubset` |
| Offline fonts still missing | Recipe unverified in your environment | Appendix C step 6; file an issue against §11.2 |
| Tests fail only in CI | `npm ci` vs local drift | Reproduce with `rm -rf node_modules && npm ci` |
| `enhance.ts` warnings in build log | Unknown tag value in content | Fix the markdown or extend the registry |

---

## 15. Pre-Ship Checklist

Mandatory verification gate, run in order. **No gate may be skipped, weakened, or made non-blocking to ship.** A green gate achieved by disabling a check is not a pass — state the debt instead.

```bash
# 1. Typecheck (strict, noUnusedLocals/Parameters)
npm run typecheck

# 2. Lint (zero-warning policy)
npm run lint

# 3. Unit tests: fence, enhance, toc, tags, slug parity + coverage
npm run test -- --coverage

# 4. Accessibility gate (AA hard-fail; AAA contrast/target-size enforced; light + dark)
npm run a11y

# 5. Production build (single-file)
npm run build          # or: npm run build:offline

# 6. Version gate V-1
npm run versions:check

# 7. Self-containment check
#    Online build: open dist/index.html WITH network → fonts load, no console errors
#    Offline build: open dist/index.html WITHOUT network → fonts still render

# 8. Manual smoke (npm run preview):
#    - Header: title, theme toggle, mobile menu trigger
#    - Desktop sidebar + mobile drawer (resize < 1024px); drawer closes on Escape
#    - Badges colored; unknown values warned in dev console
#    - TOC links jump correctly; active section highlights; fenced headings absent
#    - Theme toggle cycles light/dark/system and persists across reload
#    - Tab through page: focus rings visible; skip link works
#    - Error boundary not triggered; no console errors
```

---

## 16. Lessons Learnt

**Carried from v1.0.1 (all five still true):**

1. **Inline code ≠ badge without preprocessing.** The renderer's `code` component has no parent context; preprocess at the string level.
2. **Two slug generators must stay in sync.** Now enforced by `tests/slug-parity.test.ts`, with slug reservation across all heading levels — assertion is not verification.
3. **Strict TypeScript catches real bugs.** Unused-import errors are architectural signals (dead `cn.ts` was such a signal; v3 wires `cn()` in).
4. **Single-file build ≠ offline fonts.** `vite-plugin-singlefile` inlines JS/CSS, not `@import`ed fonts. Document runtime dependencies; provide the offline recipe.
5. **Document what doesn't exist.** "Custom hooks: none exist" saves every future agent a search. Keep negative documentation.

**New, distilled from the four generalization drafts:**

6. **Conformance claims are hereditary — gate them.** v1.0.1's AAA overclaim was copied into three of four drafts. The cure is not better wording; it is an axe gate that fails the build (§9.4) and an enumerated exceptions table (§9.3).
7. **Reference code in a skill must be traced before it ships.** Draft q2's TOC algorithm mis-nests the most common heading pattern (an H2 after an H3) while claiming production-readiness. Every algorithm in this document was hand-traced at write time and is labeled Reasoned until executed.
8. **Generality bought with verifiability is debt.** Drafts d and q2 specified systems that could not run (nonexistent packages, broken pipelines); z specified honestly but carried two technical errors. This document's answer: small configuration surface, full tests in-tree, and an evidence ledger (§24) applied to the skill itself.

---

## 17. Pitfalls to Avoid

| Area | Don't | Do |
|---|---|---|
| Tags | Hardcode tag keys in components | Registry lookup; tags are data (§7) |
| Tags | Register the same value under two tags | Unique values per preset; collision detection throws |
| Slugs | Hand-write heading `id`s | `rehype-slug` derives; TOC matches via shared slugger |
| Slugs | Assume parity across upgrades | Pin both packages; parity test runs in CI |
| Slugs | Use setext headings | ATX only (§8.4) |
| Fences | Run line regexes raw | Always via `scanLines` |
| Theming | Use `dark:` utilities in templates | Variable flipping only — one mechanism (§4.1) |
| Theming | Nest `@theme` in `@media` | Top-level `@theme inline` + runtime variables |
| Fonts | Claim offline support for the default build | Online build = CDN fonts, documented; offline = `build:offline` |
| A11y | Claim AAA without the axe gate | Run `npm run a11y`; report actual results |
| A11y | "Fix" contrast by enlarging font size below 18pt/14pt-bold | Darken tokens (§9.5) or enumerate the exception |
| Badges | Move badge classes into config/data strings | Classes live in scanned source files |
| Build | Skip gates to ship | State the debt; never weaken a gate |
| Content | Edit components to change text | Edit `src/content/document.md` |
| Versions | Copy version numbers between documents | `npm ls --depth=0` is the only source of truth |

---

## 18. Best Practices

**Code organization:** one component per file; pure functions in `lib/` with no side effects; `@/*` alias everywhere; named interfaces for shared types (§22), inline props only for leaf components.

**TypeScript:** `strict: true`; never `any` (`unknown` + narrowing); `interface` for object shapes, `type` for unions; `ComponentPropsWithoutRef<"element">` for forwarded native props.

**React:** functional components only; composition over inheritance; memoize derivations against the raw markdown string; client state limited to `drawerOpen`, `theme`, `activeSlug`.

**Tailwind v4:** CSS-first; all tokens in `@theme inline`; semantic tokens, never arbitrary hex; `scroll-mt-24` on anchored headings; classes only in scanned source files.

**Content:** edit markdown only; frontmatter for metadata; badge values are content, not code; ATX headings; register new tags in data.

**Evidence:** every claim about rendered behavior carries a tag (Verified / Reasoned / Assumed / Unverifiable); never upgrade a tag without execution.

---

## 19. Coding Patterns

1. **Pure string preprocessor with fence awareness** — `enhance.ts` (§7.3). Why: the renderer lacks line context; string-level is simple, testable, and cheap when memoized.
2. **Shared slugger with cross-level reservation** — `buildToc` (§8.2). Why: anchor parity is the app's spine; the test makes it a fact (§8.3).
3. **Renderer as configuration map** — `MarkdownRenderer` (§6.3). Why: all styling centralized; no scattered CSS; no raw HTML.
4. **Variable-flip theming** — `index.css` (§4.1). Why: runtime dark mode with zero `dark:` utility drift; one mechanism for system + manual.
5. **Registry as data with fail-fast validation** — `tags.ts` (§7.2). Why: extension without code changes; ambiguity resolved at load time, not render time.
6. **Template composition** — a template = `theme.css` (Layer-1 variables) + component-map overrides + layout shell + default registry. The editorial template is the reference implementation (§20 for the others).

---

## 20. Templates Beyond Editorial

Contracts only — **no fabricated code ships for these**; implement per §6/§19 when first needed.

### 20.1 Template B — Technical docs

- **Use for:** API references, specs, developer guides, RFCs.
- **Layout:** sticky light header with optional search; three-column desktop (left nav `w-60`, content `max-w-4xl`, right "on this page" `w-48`); drawer on mobile; no hero; footer with edit link + version.
- **Register:** utilitarian — Inter throughout, cool gray surfaces, blue accent. Code blocks first-class: `rehype-highlight` on by default, copy button.
- **Default registry:** Status (`stable`/`experimental`/`deprecated`/`removed`) + Visibility (`public`/`internal`/`restricted`).
- **Notes:** `md:` breakpoint is permitted here; `tocMaxDepth: 4`; this template may legitimately use the "generic" register — the anti-generic mandate is per-template.

### 20.2 Template C — Minimal print

- **Use for:** manuscripts, legal documents, printable/archival content.
- **Layout:** single centered column `max-w-2xl`; no header/sidebar/drawer; print CSS: `@page { size: A4; margin: 2cm }`, page break before H2, black-on-white in print.
- **Register:** system fonts only (no web fonts — this template is offline by construction), no accents except badges.
- **Default registry:** none (badges opt-in via frontmatter).

### 20.3 Adding a template (procedure)

1. Create `src/templates/<name>/` with `theme.css` (all Layer-1 variables, light + dark), `components.tsx` (partial map merged over defaults), `layout.tsx` (receives `{ title, toc, markdown, children }`), and `tags.ts`.
2. Add the name to the `TemplateName` union (§22) and the frontmatter `template` switch.
3. Add a fixture document + the full axe gate for the new template.
4. Document it here.

### 20.4 Markdown extensions (opt-in)

Install the plugin → add to `remarkPlugins`/`rehypePlugins` → add component overrides for new elements → add a fixture test → document the flag here. Known candidates: `remark-footnotes`, `remark-math` + `rehype-katex`, `rehype-mermaid`, AST-based TOC (only if setext support becomes mandatory — §8.4).

---

## 21. Responsive and Z-Index Reference

**Breakpoints (Tailwind defaults):** `sm` 640 · `md` 768 · `lg` 1024 · `xl` 1280 · `2xl` 1536.

Editorial usage: `sm:` header/page/article padding, heading sizes, hero text · `lg:` sidebar show, drawer hide, vertical padding · `xl:` readability max-width. `md:` unused in editorial, available to technical template. Mobile-first: base → `sm` → `lg`.

**Z-index map:**

| z | Element | Purpose |
|---|---|---|
| z-50 | Skip link (focused); drawer overlay + panel | Topmost |
| z-40 | Sticky header | Above content, below drawer |
| z-30 | (reserved) sticky-in-content elements | Future: search palette |
| default | Content, sidebar | Flow |

No portals, dialogs, or tooltips exist. If you add one, update this map in the same commit.

---

## 22. TypeScript Reference

```ts
// src/types/toc.ts
export interface TocItem {
  level: 2 | 3 | 4;
  text: string;
  slug: string;
  children: TocItem[];
}

// src/types/tag.ts — see §7.2 (TagValueDefinition, TagDefinition, TagRegistry)

// src/types/template.ts
export type TemplateName = "editorial" | "technical" | "minimal";

export interface TemplateLayoutProps {
  title: string;
  subtitle?: string;
  author?: string;
  date?: string;
  toc: TocItem[];
  markdown: string;
  children: React.ReactNode;
}
```

Additional named types introduced by this merge: `ResolvedBadge` (§7.2), `EnhanceResult` (§7.3), `MarkdownRegion` (§8.1), `Frontmatter` (§3.4).

Component props: `MarkdownRenderer { markdown: string; registry: TagRegistry }` · `TableOfContents { items: TocItem[]; activeSlug?: string; onNavigate?: () => void }` · `Badge { tag: string; value: string; accent: 1|2|3|4|5 }` · `SkipLink { targetId: string }` · `ThemeToggle { theme; onChange }` · `ErrorFallback { error: Error | null }` · `App` none.

---

## 23. Migration Guide

### 23.1 From `react-markdown-report` v1.0.1

| v1.0.1 | v3.0.0 | Action |
|---|---|---|
| `comparative-analysis.md` | `src/content/document.md` | Rename; becomes the editorial fixture |
| `StatusBadge`, 9 hardcoded keys | `Badge` + tag registry | Move keys to editorial `tags.ts` |
| `enhanceReportMarkdown` (two keys, `-` only) | `enhanceMarkdown` (any registered tag, all bullets, fence-aware, warnings) | Replace |
| `buildToc` H2/H3, fence-blind | `buildToc` H2–H4, fence-aware, slug reservation | Replace; `maxDepth: 3` for exact v1 parity |
| Severity tokens in `@theme` | accent-1..5 scale | Map old names via registry |
| Google Fonts only | + offline recipe | Optional |
| No reduced-motion / focus-visible / 44px targets | All three in base styles + gate | Apply §4.1, §9.2 |
| Badge text `text-xs` | Stays `text-xs`; AAA handled by §9.3/§9.5 | No size change — the "14px relaxes AAA" rationale is false |
| Pre-ship: `tsc && build` | Eight gates | §15 |
| No tests | vitest + Playwright/axe in-tree | §12 |
| `cn.ts` dead | Wired into `Badge`/templates | Done by construction |

### 23.2 From the drafts

- **From draft k:** adopt its structure wholesale; then fix badge resolution (§7.2 — cross-category + collision detection), add the gates (§15), make `enhance.ts` fence-aware and fully specified, drop the AAA headline.
- **From draft d:** keep the honesty (AA baseline), the dark-mode mechanics (now formalized in §4.1), focus-trap requirement, and image caveats; **delete** `defineConfig`/`virtual:config`, the raw-HTML badge pattern, and `theme.css`-in-`src/`.
- **From draft q2:** keep as a *standards annex*: test pyramid shape, CI skeleton, dependency-selection criteria, ErrorBoundary prop contract. **Do not copy** its TOC extractor, `.use(undefined)` pipeline, sync-consumed async examples, or "Production-Ready" status. Downscope: one framework, one file, no Vue/Svelte adapters.
- **From draft z:** keep the audit discipline, tag registry, offline recipe, axe gate, and evidence ledger; **apply three corrections** — dark mode per §4.1 (not `@theme`-in-`@media`), badge contrast per §9.3/§9.5 (not the 14px arithmetic), parity test per §8.3 (default import, no unused symbols); add `ErrorBoundary` to the skeleton.

---

## 24. Verification and Evidence Ledger

This document applies its own contract to itself.

| Claim | Tag | Basis |
|---|---|---|
| TOC stack algorithm + slug reservation (§8.2) | **Reasoned** | Hand-traced: nested, sibling-after-nested, orphan, maxDepth-reservation, dedup cases |
| Fence scanner (§8.1) | **Reasoned** | Traced against CommonMark-subset rules; fixtures in §12.1 |
| `enhance.ts` regex + warnings (§7.3) | **Reasoned** | Fixtures in §12.1 incl. blind spots |
| Collision detection semantics (§7.2) | **Reasoned** | Tests in §12.1 |
| Slug parity test compiles & passes (§8.3) | **Reasoned** | Not executed; imports/exports per package knowledge — verify at install |
| Dark-mode variable-flip pattern (§4.1) | **Reasoned** | Matches documented Tailwind v4 idiom; verify against current v4 docs |
| Contrast ratios (§9.3, §9.5) | **Reasoned** | Computed via WCAG relative-luminance formula, not a checker |
| WCAG large-text thresholds (§9.1) | **Verified** | Stable WCAG 2.x definitions |
| Lineage dependency pins (§2) | **Verified** | Per v1.0.1's own `package.json` verification claim |
| New dev-dependency versions (§2) | **Assumed** | Confirm at install; gate V-1 |
| `lucide-react` 1.28.0 (§2) | **Unverifiable** | Conflicting claims across sources; gate V-1 decides |
| Offline font recipe (§11.2) | **Reasoned** | Explicitly a sketch; Appendix C step 6 |
| react-markdown drops raw HTML by default (§13 row 9) | **Reasoned** | Established library behavior |

**What was NOT done:** no install, build, test, or axe run happened at authoring time. Nothing in this document may be quoted as "verified" or "passing" until Appendix C (or the full §15 gate) has been executed.

---

## Appendix A — Build Output

`npm run build` → `dist/index.html`: single file, JS/CSS inlined, fonts via CDN (default) or inlined (`build:offline`). Serve with `npm run preview` or any static host; the default build also opens from `file://`. Never edit `dist/` by hand.

---

## Appendix B — Correction Ledger

Every audit finding from the comparative review, resolved in this document.

| Finding | Resolution |
|---|---|
| O-F1 AAA overclaim vs own measurements | §9.1 posture, §9.3 exceptions, §9.4 gate |
| O-F2 portability vs CDN fonts | §11 honest split + offline recipe |
| O-F3 no reduced motion | §4.1 base styles |
| O-F4 slug parity asserted only | §8.3 compiling test in CI |
| O-F5 nine hardcoded keys, `-`-only regex | §7 registry + all bullet styles + warnings |
| O-F6 gate = tsc+build | §15 eight gates |
| O-F7 dead `cn.ts` | §6.1 wired; §16 lesson 3 |
| O-low lucide version doubt | §2 Unverified tag + gate V-1 |
| K1 badge category ambiguity | §7.2 cross-category resolver + collision throw |
| K2 AAA repeat | §9.1; frontmatter claims AA only |
| K3 no gates | §12, §15 |
| K4 unspecified enhance regex | §7.3 full code + fixtures |
| K5 fence-blind TOC | §8.1/§8.2 |
| K6 exact-vs-caret inconsistency; malformed TOC links | §2 pin policy; ToC above uses clean, verified-shape anchors |
| D1 raw-HTML badges | Rejected — §13 row 9 |
| D2 nonexistent config infra | §3.3 explicit rejection |
| D3 dynamic class hazard | §13 row 11, §7.4 |
| D4 no error boundary | §6.1, §10.1 |
| D5 palette-vs-token contradiction | §7.4 accent tokens + static chips, documented |
| D6 generated artifact in src/ | §6.1 tree — scripts in `scripts/`, no generated files in `src/` |
| Q1 TOC mis-nests H2-after-H3 | §8.2 traced algorithm; regression fixture in §12.1 |
| Q2 "Production-Ready" vs ledger | Frontmatter status field; §24 ledger |
| Q3 `.use(undefined)` | §5 single components-map pipeline; no unified `.use` chain in core |
| Q4 async misuse | §5/§6 synchronous pipeline; no async core API |
| Q5 test/impl mismatch | §12.1 tests written against §7–§8 implementations |
| Q6 DOMPurify claim unwired | Claim removed; sanitization only mentioned where the serialization path is chosen (§6.3 note) |
| Q7 dual pipelines | §5 one pipeline, stated as a tenet |
| Q8 coverage drift, phantom scripts | §12.2 single threshold statement; §12.4 scripts all defined in §3.1 |
| Q9 unflagged Inter+gray default | §1: anti-generic mandate is per-template; §20.1 declares the technical register |
| Z1 WCAG arithmetic error | §9.1 explicit rejection + §9.3 correct math |
| Z2 `@theme` in `@media` | §4.1 corrected pattern + §13 row 12 |
| Z3 parity test imports | §8.3 fixed imports, no unused symbols |
| Z4 fence-blind TOC | §8.1 |
| Z5 skeleton missing ErrorBoundary | §6.1, §10.1 |
| Z6 enhance blind spots undisclosed | §7.3 disclosed + fixtures |
| Z7 unverified-yet-executable framing | Frontmatter status banner + §24 + Appendix C |
| C1 generality-vs-verifiability | §24 ledger + Appendix C spot-check |
| C2 hereditary overclaim | §9.1, §16 lesson 6 |
| C3 slug parity universal/unverified | §8.3 |
| C4 regex-vs-AST schism | §8.4: tested regex in core; AST scoped to the one case that needs it |
| C5 version drift | §2 policy + gate V-1 |
| C6 fence-blindness shared bug | §8.1 shared scanner |

---

## Appendix C — Adopter Spot-Check

Convert this document's Reasoned claims to Verified in roughly ten minutes:

```bash
# 1. Scaffold
npm create vite@latest mdw-spotcheck -- --template react-ts
cd mdw-spotcheck

# 2. Install runtime deps (exact pins from §2)
npm install react@19.2.6 react-dom@19.2.6 react-markdown@10.1.0 remark-gfm \
  rehype-slug@6.0.0 github-slugger@2.0.0 clsx@2.1.1 tailwind-merge@3.4.0 \
  vite-plugin-singlefile@2.3.0
npm install -D tailwindcss@4.1.17 @tailwindcss/vite vitest

# 3. Gate V-1 — resolve the lucide-react question
npm install lucide-react@1.28.0 || npm install lucide-react   # record what resolves; update §2

# 4. Copy src/lib/{fence,toc,enhance,tags}.ts, src/types/, and tests/ from this document

# 5. Run the core suites
npx vitest run            # fence, enhance, toc, tags, slug parity

# 6. Single-file + offline sanity
npm run build             # dist/index.html exists, opens from file://
npm run build:offline     # open with network disabled — do fonts render? (validates §11.2)

# 7. Tailwind dark pattern sanity
#    Build with §4.1 index.css, toggle OS dark mode — utilities must flip live (validates @theme inline)
```

Record the outcomes in a copy of the §24 ledger; upgrade only the rows your run actually proved.

---

*Skill version 3.0.0 — unified from v1.0.1 and drafts k/d/q2/z. Every section traceable via Appendix B. Confidence posture: Reasoned throughout until §15 or Appendix C has been executed.*
