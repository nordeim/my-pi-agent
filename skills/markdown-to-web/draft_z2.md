---
name: markdown-to-web
description: >
  Renders an arbitrary Markdown document as a polished, single-file,
  accessible web page. Accepts any .md file plus an optional template
  (editorial long-form / technical docs / minimal print) and an optional
  tag registry (severity, confidence, status, custom). Produces a
  self-contained dist/index.html with WCAG 2.2 AA + AAA-aspirational
  accessibility, code-first theming, slug-parity navigation, and an
  evidence-tag badge system. Built on React 19 + Vite 7 + Tailwind v4
  + react-markdown. Use when the user asks to "render this markdown
  as a web page", "convert .md to HTML", "publish this document as a
  site", or "make a polished web version of this README/report/spec".
version: 2.0.0
tags:
  - react
  - vite
  - tailwindcss
  - markdown
  - html
  - single-file-build
  - accessibility
  - documentation
---

# markdown-to-web — General Skill

> **Purpose:** Enable any agent to convert an arbitrary Markdown document into a polished, accessible, self-contained web presentation without writing presentation-specific code. The Markdown file is the single source of truth; the renderer adapts to its structure.
>
> **When to use:** Any time you need to turn a `.md` file into a shareable HTML page — audit reports, documentation, READMEs, articles, resumes, research papers, or specifications.
>
> **Output of this skill:** This document (`markdown-to-web_SKILL.md`).
>
> **Provenance:** Unified merge of five prior drafts (`draft_d`, `draft_k`, `draft_q`, `draft_q2`, `draft_z`) audited against the original `react-markdown-report` v1.0.1 project skill. Foundation is `draft_z`; merge-ins from `draft_q2` (CI/CD, performance budgets, font preload), `draft_k` (YAML frontmatter for skill discovery), and `draft_d` (`defineConfig` ergonomic helper). All Critical, High, and Medium findings from the comparative audit are fixed in this version.

---

## Table of Contents

1. [Identity & Design Philosophy](#1-identity--design-philosophy)
2. [When to Use / When Not To](#2-when-to-use--when-not-to)
3. [Inputs Contract](#3-inputs-contract)
4. [Tech Stack & Pinned Versions](#4-tech-stack--pinned-versions)
5. [Project Skeleton](#5-project-skeleton)
6. [Design System (Code-First)](#6-design-system-code-first)
7. [Three Templates](#7-three-templates)
8. [Tag Registry & Badge Protocol](#8-tag-registry--badge-protocol)
9. [TOC & Navigation Contract](#9-toc--navigation-contract)
10. [Accessibility (WCAG 2.2 AA + AAA Aspirational)](#10-accessibility-wcag-22-aa--aaa-aspirational)
11. [Build & Deploy Recipes](#11-build--deploy-recipes)
12. [Error Handling & Resilience](#12-error-handling--resilience)
13. [Font Strategy & Offline Support](#13-font-strategy--offline-support)
14. [Performance Optimization](#14-performance-optimization)
15. [Testing Strategy](#15-testing-strategy)
16. [CI/CD & Quality Gates](#16-cicd--quality-gates)
17. [Anti-Patterns & Pitfalls](#17-anti-patterns--pitfalls)
18. [Pre-Ship Checklist](#18-pre-ship-checklist)
19. [Debugging Guide](#19-debugging-guide)
20. [Extending the Skill](#20-extending-the-skill)
21. [Migration Guide (from v1.0.1)](#21-migration-guide-from-v101)
22. [Verification & Evidence Contract](#22-verification--evidence-contract)
23. [TypeScript Reference](#23-typescript-reference)
24. [Confidence Statement & Verification Ledger](#24-confidence-statement--verification-ledger)

---

## 1. Identity & Design Philosophy

**One-sentence description:** A generalized, template-driven React application that renders any Markdown document as a polished, single-file, accessible web page — preserving the author's content as the single source of truth while applying an opinionated editorial design system.

**Design thesis:** *Content is data; rendering is configuration.* The Markdown file is the input. The template chooses the look. The tag registry chooses which inline annotations become badges. The build produces one self-contained `dist/index.html` that runs anywhere a browser can open a file — online or offline.

**Non-negotiable design rules:**

1. **Content is invariant.** Editing the Markdown never requires code changes. Adding a heading, table, code block, or `**Tag:** value` annotation is a content change, not a UI change. The Markdown source is the canonical input; everything else is derived.
2. **Templates are swappable.** Three ship in-box (editorial, technical, minimal). Each provides its own `@theme` tokens, layout shell, component map, and default tag registry. The user picks at invocation; the build wires it. Adding a fourth template is a documented extension, not a fork.
3. **Tags are registered, not hardcoded.** A document can use any `**<Tag>:** <value>` bullet as a badge as long as `<Tag>` is in the registry. Templates ship default registries as JSON data; documents can extend or override. Tags are data, not code — adding a new tag value should not require touching a TypeScript file.
4. **Single-file portability is real.** The default build inlines JS, CSS, and (optionally) fonts. The artifact runs from `file://`, a USB stick, or a static host with no CDN dependency. The "single-file" promise is not half-kept — both online and offline build modes are first-class.
5. **Accessibility is verified, not claimed.** Pre-ship runs `axe` + Lighthouse. The headline conformance claim is "WCAG 2.2 AA; AAA where feasible, with documented exceptions." AAA violations for `target-size` and `color-contrast` are gate-failures; other AAA violations are warnings. The skill does not claim conformance it has not measured.
6. **Evidence over assertion.** When the source document contains findings (e.g., an audit report), each finding carries an explicit confidence tag. The renderer never upgrades "Unverifiable" to "Verified." This honesty contract is preserved verbatim from v1.0.1 and applies to the skill file itself — see §22 and §24.

**Explicitly rejected (carried over from v1.0.1, scoped per-template):**

- Purple gradients on white
- Predictable rounded-card grids with left-border accents
- Generic "Inter/Roboto + gray-50" neutrality
- Hero sections with centered H1 + paragraph + CTA button
- Any component that could be dropped into a different template without visual friction

These rejections apply **per template**. The minimal print template may legitimately use Inter + gray-50 neutrality; that is its design register. The editorial template preserves v1.0.1's bespoke visual identity (Source Serif 4, warm paper, teal/moss accents) — that identity is the template's reason for existing, not a regression.

---

## 2. When to Use / When Not To

**Use this skill when:**

- The user provides a Markdown file (`.md`) and asks for a "web version," "HTML rendering," "polished page," or "publishable site."
- The document is long-form (1,000–50,000 words) and benefits from a Table of Contents.
- The document contains structured annotations (`**Severity:** critical`, `**Status:** done`) that should render as visual badges.
- The artifact must run offline or from `file://`.
- Accessibility conformance (AA minimum, AAA aspirational) is a requirement.
- The user wants a single self-contained HTML file with no external runtime dependencies (CDN fonts, JS bundles, CSS files).

**Do NOT use this skill when:**

- The user wants a full Next.js application with server-side rendering, API routes, or database. Use `fullstack-dev` instead.
- The user wants a slide deck / presentation. Use `pptx` instead.
- The user wants a PDF. Use `pdf` instead.
- The document is a code project README that needs interactive code execution. Use a code-sandbox skill instead.
- The document is shorter than ~500 words; a styled HTML page is overkill — render inline.
- The user needs multi-page navigation, search across documents, or user accounts. This skill renders one document into one HTML file.

**Ambiguous cases — ask the user:**

- "Make a dashboard from this markdown" → Ask: interactive web app (`fullstack-dev`) or single-file report (this skill)?
- "Add charts to this markdown report" → Ask: charts embedded in the rendered HTML (this skill + `charts`) or a separate chart deliverable?

---

## 3. Inputs Contract

The skill accepts the following inputs. All except the Markdown file are optional with sensible defaults.

| Input | Required | Format | Default | Notes |
|-------|----------|--------|---------|-------|
| Markdown file | Yes | `.md`, UTF-8 | — | GFM extensions supported: tables, strikethrough, task lists, autolinks |
| Template | No | `editorial` \| `technical` \| `minimal` | `editorial` | See §7 |
| Tag registry | No | JSON file or TS module | Template's default | See §8 |
| Theme override | No | Partial `@theme` tokens | None | Merges with template's tokens |
| Title | No | String | First H1 in markdown | Used in `<title>`, header, OG tags |
| Author | No | String | From frontmatter if present | Used in metadata |
| Offline fonts | No | Boolean | `false` | When `true`, inlines fonts as base64 |
| Syntax highlighting | No | Boolean | `false` | When `true`, enables `rehype-highlight` |

**Markdown features supported:**

- Headings H1–H4 (TOC extracts H2–H4 by default; configurable)
- Paragraphs, bold, italic, strikethrough
- Inline code, fenced code blocks (with language class for syntax highlighting — opt-in via §13)
- Blockquotes
- Ordered/unordered lists, task lists
- Tables (GFM)
- Images (local paths resolved relative to the markdown file; remote URLs as-is; small images optionally embedded as base64)
- Links (external links get `target="_blank" rel="noopener noreferrer"` automatically)
- Horizontal rules
- YAML frontmatter (parsed for `title`, `subtitle`, `author`, `date`, `template`, `badgeConfig`; remaining keys ignored)

**Markdown features NOT supported (out of scope):**

- Footnotes (`[^1]`) — add via `remark-footnotes` if a template needs it (§20)
- Math (`$...$`) — add via `remark-math` + `rehype-katex` if a template needs it (§20)
- Mermaid code blocks — add via `rehype-mermaid` if a template needs it (§20)
- Raw HTML pass-through — by default, react-markdown escapes raw HTML. If a template explicitly enables `rehype-raw`, it MUST be paired with `rehype-sanitize` and the security implications documented.

**Frontmatter schema (optional):**

```yaml
---
title: "Document Title"           # overrides first H1
subtitle: "Optional subtitle"     # renders below title in hero
author: "Author Name"             # renders in meta line
date: "2026-08-06"                # renders in meta line, ISO 8601
template: "editorial"             # editorial | technical | minimal
badgeConfig: "audit"              # selects which tag registry preset to use
offlineFonts: false               # inline fonts as base64
syntaxHighlighting: false         # enable rehype-highlight
---
```

---

## 4. Tech Stack & Pinned Versions

Every dependency below is pinned to a specific version. The pre-ship checklist (§18) includes `npm ls --depth=0` to verify the installed versions match this table exactly. Drift from these versions risks breaking the slug-parity contract (§9) and the `@theme` token generation (§6).

| Layer | Technology | Version | Critical Note |
|-------|------------|---------|---------------|
| Framework | React | `19.2.6` | Strict TypeScript; functional components only; no class components except `ErrorBoundary` |
| Build | Vite | `7.3.2` | `vite-plugin-singlefile` for one-file output; `?raw` imports for Markdown |
| Styling | Tailwind CSS | `4.1.17` | CSS-first `@theme` in `src/index.css`; **no `tailwind.config.js`** |
| Markdown | react-markdown | `10.1.0` | `remark-gfm` + `rehype-slug`; component map renders Markdown as React elements (no `dangerouslySetInnerHTML`) |
| Heading anchors | rehype-slug | `6.0.0` | Must match `github-slugger` output (verified by `slug-parity.test.ts`, §15) |
| TOC extraction | github-slugger | `2.0.0` | Slug parity test required (§15) |
| Syntax highlight (opt-in) | rehype-highlight | `7.0.0` | Loaded only when `syntaxHighlighting: true`; highlight.js CSS theme in `index.css` |
| Icons | lucide-react | `1.28.0` | Menu, X, ExternalLink, Sun, Moon, Search (tree-shaken) |
| Class util | clsx + tailwind-merge | `2.1.1` / `3.4.0` | `cn()` helper in `src/utils/cn.ts` — actively used in `Badge.tsx` and template components |
| Packaging | vite-plugin-singlefile | `2.3.0` | Inlines JS/CSS; fonts opt-in via offline build (§11, §13) |
| Fonts (offline) | @fontsource-variable/source-serif-4 | `5.0.0` | Inlined as base64 when `--offline` (§13) |
| Fonts (offline) | @fontsource-variable/inter | `5.0.0` | Inlined as base64 when `--offline` |
| Fonts (offline) | @fontsource/jetbrains-mono | `5.0.0` | Inlined as base64 when `--offline` |
| Accessibility | @axe-core/playwright | `4.10.0` | Pre-ship a11y gate (§10, §15) |
| TypeScript | typescript | `5.9.3` | `strict: true`, `noUnusedLocals`, `noUnusedParameters` |
| Linter | eslint | `9.x` | `@eslint/js` + `typescript-eslint` + `eslint-plugin-react-hooks` |
| Formatter | prettier | `3.x` | Run after `eslint --fix` to avoid drift (persona Appendix B6) |
| Test | vitest | `2.x` | Unit tests for `enhance.ts`, `toc.ts`, `frontmatter.ts`, slug parity |
| E2E | @playwright/test | `1.40.0` | Visual regression + axe integration |
| Markdown lint | markdownlint-cli2 | `0.15.x` | Content quality gate |
| Node | — | `≥20.19` or `≥22.12` | Vite 7 requirement |

**Verification command:** `npm ls --depth=0` — every row above must appear with the exact version. Run in pre-ship (§18, gate 7).

**Dependency selection criteria (for any future addition):**

- Active maintenance (commit within 6 months)
- TypeScript types included or `@types/*` available
- MIT, Apache-2.0, or BSD-3-Clause license (no copyleft)
- Zero known critical vulnerabilities (`npm audit`)
- Download count > 100k/week (indicates adoption)
- < 10 MB unpacked size

---

## 5. Project Skeleton

```
markdown-to-web/
├── package.json
├── package-lock.json
├── vite.config.ts
├── tsconfig.json
├── eslint.config.js
├── .prettierrc
├── .gitignore
├── .husky/
│   └── pre-commit                  # lint-staged + typecheck + unit tests
├── index.html                      # Entry: <div id="root"> + <script type="module" src="/src/main.tsx">
├── src/
│   ├── main.tsx                    # Entry: StrictMode + ErrorBoundary + createRoot
│   ├── App.tsx                     # Layout, drawer/theme state, TOC derivation, IntersectionObserver
│   ├── index.css                   # Tailwind v4 @import + template @theme import
│   ├── content/
│   │   └── document.md             # The input markdown (?raw import)
│   ├── templates/
│   │   ├── editorial/
│   │   │   ├── theme.css           # @theme tokens for editorial (light + dark)
│   │   │   ├── components.tsx      # Component map overrides
│   │   │   ├── layout.tsx          # Layout shell (sidebar + drawer + hero)
│   │   │   └── tags.json           # Default tag registry (Severity, Confidence)
│   │   ├── technical/
│   │   │   ├── theme.css
│   │   │   ├── components.tsx
│   │   │   ├── layout.tsx
│   │   │   └── tags.json           # Status, Visibility
│   │   └── minimal/
│   │       ├── theme.css
│   │       ├── components.tsx
│   │       ├── layout.tsx
│   │       └── tags.json           # Empty (badges opt-in)
│   ├── components/
│   │   ├── MarkdownReport.tsx      # react-markdown renderer + default components map
│   │   ├── TableOfContents.tsx     # Recursive TOC (sidebar + drawer) + active-section highlight
│   │   ├── Badge.tsx               # Tag-aware badge (replaces StatusBadge)
│   │   ├── ErrorBoundary.tsx       # Class component, catches render errors
│   │   ├── ErrorFallback.tsx       # Presentational fallback UI
│   │   ├── SkipLink.tsx            # Accessible skip-to-content
│   │   └── ThemeToggle.tsx         # Light/dark/system toggle with localStorage (try/catch wrapped)
│   ├── lib/
│   │   ├── enhance.ts              # Tag-aware regex preprocessor (emits warnings)
│   │   ├── toc.ts                  # H2–H4 outline extraction (correct stack logic)
│   │   ├── frontmatter.ts          # YAML frontmatter extraction (CRLF-safe)
│   │   ├── tags.ts                 # Tag registry loader + validator
│   │   ├── config.ts               # defineConfig helper + config merge
│   │   └── slug-parity.test.ts     # Unit test: github-slugger vs rehype-slug
│   ├── utils/
│   │   ├── cn.ts                   # clsx + tailwind-merge
│   │   ├── theme-storage.ts        # localStorage with try/catch + in-memory fallback
│   │   └── contrast.ts             # WCAG contrast ratio calculator (for a11y tests)
│   └── types/
│       ├── template.ts             # TemplateConfig, TemplateLayoutProps, ComponentsMap
│       ├── tag.ts                  # TagDefinition, TagRegistry, TagValueDefinition
│       ├── toc.ts                  # TocItem (level 2 | 3 | 4)
│       └── config.ts               # MarkdownToWebConfig, defineConfig
├── scripts/
│   ├── build-offline.mjs           # Offline-font build variant (assetsInlineLimit: 100MB)
│   ├── generate-color-ref.mjs      # Auto-generates §color reference from @theme
│   └── quality-gate.sh             # Runs all 8 pre-ship gates in order
├── .github/
│   └── workflows/
│       └── ci.yml                  # GitHub Actions: matrix testing, coverage, Lighthouse, audit
└── tests/
    ├── unit/
    │   ├── enhance.test.ts         # Tag preprocessor: all bullet styles, unknown tags, CRLF
    │   ├── toc.test.ts             # TOC extraction: H2/H3/H4, orphan headings, level jumps
    │   ├── frontmatter.test.ts     # Frontmatter: present, absent, malformed, CRLF
    │   └── slug-parity.test.ts     # github-slugger === rehype-slug for 11 fixtures
    ├── integration/
    │   ├── markdown-rendering.test.tsx   # Full pipeline: badges, TOC, headings
    │   ├── toc-navigation.test.tsx       # Click TOC link → scroll to heading
    │   └── error-handling.test.tsx       # Malformed markdown, missing files
    ├── accessibility/
    │   ├── wcag-aa.test.ts          # axe-core: zero AA violations (gate-failure)
    │   ├── wcag-aaa-aspirational.test.ts # axe-core: AAA violations except target-size, color-contrast (warnings)
    │   └── keyboard-navigation.test.ts  # Tab/Shift+Tab through entire page, no traps
    ├── visual/
    │   ├── markdown-appearance.test.ts  # Playwright screenshot: rendered markdown
    │   ├── badges.test.ts               # Playwright screenshot: all accent colors
    │   └── responsive.test.ts           # Mobile (375px) + desktop (1440px) layouts
    └── performance/
        ├── bundle-size.test.ts          # gzip < 250 KB (realistic budget)
        └── parsing-speed.test.ts        # 1000 lines < 100ms, 5000 lines < 500ms
```

**File responsibility rule:** One file, one responsibility. `MarkdownReport.tsx` renders; `Badge.tsx` styles tags; `tags.ts` loads the registry; `enhance.ts` preprocesses strings; `ErrorBoundary.tsx` catches errors; `ErrorFallback.tsx` renders the fallback UI. No file mixes concerns.

**Bootstrap command sequence:**

```bash
# 1. Scaffold
npm create vite@latest markdown-to-web -- --template react-ts
cd markdown-to-web

# 2. Install runtime deps
npm install react-markdown@10.1.0 remark-gfm@4.0.0 rehype-slug@6.0.0 \
  github-slugger@2.0.0 lucide-react@1.28.0 clsx@2.1.1 tailwind-merge@3.4.0

# 3. Install dev deps
npm install -D tailwindcss@4.1.17 @tailwindcss/vite@4.1.17 \
  vite-plugin-singlefile@2.3.0 \
  vitest@2.x @testing-library/react@16.x @testing-library/jest-dom@6.x \
  @axe-core/playwright@4.10.0 @playwright/test@1.40.0 jest-axe@9.x \
  eslint@9.x @typescript-eslint/eslint-plugin@8.x @typescript-eslint/parser@8.x \
  eslint-plugin-react-hooks@5.x eslint-plugin-jsx-a11y@6.x \
  prettier@3.x markdownlint-cli2@0.15.x husky lint-staged

# 4. Install offline-font deps (optional, for offline build)
npm install @fontsource-variable/source-serif-4@5.0.0 \
  @fontsource-variable/inter@5.0.0 \
  @fontsource/jetbrains-mono@5.0.0

# 5. Verify
npm ls --depth=0   # Compare against §4 table
```

---

## 6. Design System (Code-First)

Each template ships its own `theme.css` with a Tailwind v4 `@theme` block. The default (editorial) theme inherits v1.0.1's palette and adds dark variants. The token system is code-first: all colors, fonts, spacing, and radii are CSS custom properties consumed by Tailwind's `@theme` directive. There is no `tailwind.config.js` and no JavaScript theme object — this is the modern Tailwind v4 idiom and the source of the system's maintainability.

### 6.1 Editorial template `@theme` (light + dark)

```css
/* src/templates/editorial/theme.css */
@import "tailwindcss";

@theme {
  /* Typography */
  --font-serif: "Source Serif 4", ui-serif, Georgia, serif;
  --font-sans: "Inter", ui-sans-serif, system-ui, sans-serif;
  --font-mono: "JetBrains Mono", ui-monospace, monospace;

  /* Light: ink scale (dark surfaces & text) */
  --color-ink-950: #0b1615;
  --color-ink-900: #0f1e1c;
  --color-ink-800: #16302c;
  --color-ink-700: #204640;

  /* Light: paper scale (light backgrounds) */
  --color-paper-50: #fbfaf7;
  --color-paper-100: #f4f2ec;
  --color-paper-200: #e9e5da;

  /* Accent (shared with dark) */
  --color-teal-600: #0e7c86;
  --color-teal-700: #0b626a;
  --color-moss-500: #6fa661;
  --color-moss-600: #588650;

  /* Generic 5-step accent scale (replaces fixed severity tokens) */
  --color-accent-1: #b3261e;  /* was: critical */
  --color-accent-2: #b45309;  /* was: high */
  --color-accent-3: #a16207;  /* was: medium */
  --color-accent-4: #3f6212;  /* was: low */
  --color-accent-5: #1d4ed8;  /* was: info */
}

/* Dark mode token overrides.
   Note: defined as :root variable overrides inside the media query,
   NOT as a nested @theme block (nested @theme is non-standard Tailwind v4
   and may not generate the expected utilities). */
@media (prefers-color-scheme: dark) {
  :root {
    --color-ink-950: #f4f2ec;   /* inverted: paper becomes ink */
    --color-ink-900: #fbfaf7;
    --color-ink-800: #e9e5da;
    --color-ink-700: #d6d0c0;
    --color-paper-50: #0b1615;
    --color-paper-100: #0f1e1c;
    --color-paper-200: #16302c;
    --color-teal-600: #2ba8b3;  /* brighter for dark bg */
    --color-teal-700: #0e7c86;
  }
}

/* Manual override class (toggled by ThemeToggle) — same overrides as above */
[data-theme="dark"] {
  --color-ink-950: #f4f2ec;
  --color-ink-900: #fbfaf7;
  --color-ink-800: #e9e5da;
  --color-ink-700: #d6d0c0;
  --color-paper-50: #0b1615;
  --color-paper-100: #0f1e1c;
  --color-paper-200: #16302c;
  --color-teal-600: #2ba8b3;
  --color-teal-700: #0e7c86;
}

/* Reduced motion (the v1.0.1 gap, now fixed) */
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* Global focus-visible (the v1.0.1 gap, now fixed) */
:focus-visible {
  outline: 2px solid var(--color-teal-600);
  outline-offset: 2px;
  border-radius: 2px;
}

/* Remove default outline for mouse users only */
:focus:not(:focus-visible) {
  outline: none;
}

/* Base */
html { scroll-behavior: smooth; }
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
```

### 6.2 Typography hierarchy (editorial template)

| Role | Font | Weight | Size (mobile) | Size (sm+) | Tracking | Color |
|------|------|--------|---------------|------------|----------|-------|
| H1 (document title) | Source Serif 4 | 600 | `text-3xl` | `sm:text-4xl` | normal | `ink-900` |
| H2 (section) | Source Serif 4 | 600 | `text-2xl` | `sm:text-[1.75rem]` | normal | `ink-900` |
| H3 (subsection) | Source Serif 4 | 600 | `text-xl` | — | normal | `ink-800` |
| H4 (sub-subsection) | Source Serif 4 | 600 | `text-lg` | — | normal | `ink-700` |
| Body | Inter | 400 | base (16px) | — | normal | `stone-700` |
| Meta / labels | JetBrains Mono | 500 | `text-xs` | — | `tracking-wide` | `teal-700` |
| Badge text | Inter | 600 | `text-sm` (14px, was 12px in v1.0.1 — fixes AAA contrast) | — | `tracking-wide uppercase` | per-tag token |
| Code inline | JetBrains Mono | 400 | `text-[0.85em]` | — | normal | `ink-800` |
| Code block | JetBrains Mono | 400 | `text-sm` | — | normal | `paper-100` on `ink-900` |

**Color reference is auto-generated.** Run `node scripts/generate-color-ref.mjs` to emit a markdown table from `@theme`. This prevents the drift v1.0.1 risks where the skill doc's color table could fall out of sync with the actual CSS.

### 6.3 Token usage rules

**Mandatory:**
- All colors must come from `@theme` tokens (`text-ink-900`, `bg-paper-50`, `text-accent-1`)
- All spacing must use Tailwind's scale (`p-4`, `gap-2`, `mt-8`)
- All border radius must use Tailwind's scale (`rounded`, `rounded-lg`)
- All shadows must use Tailwind's scale (`shadow-sm`, `shadow-xl`)

**Forbidden:**
- Arbitrary hex values in components: `className="text-[#b3261e]"` — use `text-accent-1` instead
- Inline styles for colors: `style={{ color: '#b3261e' }}` — use a token class instead
- Hardcoded pixel values for spacing: `padding: 16px` — use `p-4` instead
- Magic numbers without explanation

### 6.4 Z-index layer map

| z-index | Element | Purpose | File |
|---------|---------|---------|------|
| `z-50` | Skip-to-content link (focused) | Must overlay everything | `SkipLink.tsx` |
| `z-50` | Mobile drawer overlay + panel | Topmost on mobile | `App.tsx` |
| `z-40` | Sticky header | Stays above content, below drawer/skip | `App.tsx` |
| (default) | Main content, sidebar, report | Normal flow | — |

No other `z-*` classes are used. Radix/shadcn portals are not present (no dialogs, dropdowns, tooltips).

---

## 7. Three Templates

Templates are the right level of generalization. Not "one config to rule them all" (too rigid) and not "multi-framework adapters" (over-engineered). Three opinionated templates with consistent contracts cover the realistic use space.

### 7.1 Template A — Editorial Long-Form (default)

**Use for:** Audit reports, essays, long-form journalism, comparative analyses, design critiques.

**Layout:**
- Sticky dark header (`z-40`) with title, theme toggle, and (mobile) menu trigger
- Desktop: left sidebar (`w-64`, sticky, `top-24`) with TOC; main content column (`max-w-3xl`)
- Mobile: slide-in drawer (`z-50`) with TOC; full-width content
- Hero: title + subtitle + meta chips (author, date, reading time)
- Footer: source link, generated date

**Visual register:** Bespoke editorial — Source Serif 4 display, warm paper background (`paper-50`), teal/moss accents. This is the v1.0.1 design, generalized. The anti-generic mandate applies in full: no purple gradients, no Bootstrap card grids, no Inter-on-gray-50 neutrality.

**Default tag registry:** Severity (`critical`/`high`/`medium`/`low`/`informational`) + Confidence (`verified`/`reasoned`/`assumed`/`unverifiable`). Loaded from `templates/editorial/tags.json`.

### 7.2 Template B — Technical Docs

**Use for:** API references, technical specifications, developer guides, RFCs.

**Layout:**
- Sticky light header with search box (cmd-K palette, optional — not in MVP)
- Three-column desktop: left nav (`w-60`), content (`max-w-4xl`), right "on this page" outline (`w-48`, sticky)
- Mobile: drawer nav; content; inline "on this page" accordion at top
- No hero — jump straight to H1 + first paragraph
- Footer: edit-on-GitHub link, version

**Visual register:** Utilitarian — Inter throughout (display + body), cool gray background, blue accent. Code blocks are first-class (syntax-highlighted when `syntaxHighlighting: true`, copy button). The anti-generic mandate is relaxed here: technical docs legitimately use Inter-on-gray neutrality; that is the design register for this template.

**Default tag registry:** Status (`stable`/`experimental`/`deprecated`/`removed`) + Visibility (`public`/`internal`/`restricted`). Loaded from `templates/technical/tags.json`.

### 7.3 Template C — Minimal Print

**Use for:** Manuscripts, legal documents, printable reports, archival content.

**Layout:**
- Single column, `max-w-2xl`, centered
- No header, no sidebar, no drawer — just title + content + page footer
- Print CSS: `page-break-before: always` on H2, `@page { size: A4; margin: 2cm }`, no color in print (black on white)
- Optional "Download PDF" button using `window.print()`

**Visual register:** Minimal — system serif/sans/mono (no web fonts), black on white, no accent colors except for badges. This template ships with `offlineFonts: true` by default because it is designed for archival and print contexts where CDN dependence is unacceptable.

**Default tag registry:** None (badges disabled by default; opt-in via frontmatter `badgeConfig`).

### 7.4 Template contract

Every template MUST provide:

```typescript
// src/types/template.ts
export interface TemplateConfig {
  name: TemplateName;
  themeCss: string;                    // path to theme.css
  components: Partial<ComponentsMap>;   // overrides for default component map
  layout: React.FC<TemplateLayoutProps>;
  defaultTags: TagRegistry;             // loaded from tags.json
  tocMaxDepth: 2 | 3 | 4;
  offlineFonts: boolean;                // template-specific font strategy
}
```

The build system loads the template specified in frontmatter (or the default `editorial`), merges its component overrides with the default map, and renders the layout shell with the markdown content as children.

---

## 8. Tag Registry & Badge Protocol

The v1.0.1 badge system hardcoded 9 keys (5 severity + 4 confidence). v2.0.0 replaces this with a tag registry. Tags are data (JSON), not code — adding a new tag value should not require touching a TypeScript file. The registry is loaded at build time, validated against a schema, and consumed by the `enhance.ts` preprocessor and the `Badge` React component.

### 8.1 Tag registry schema

```typescript
// src/types/tag.ts
export interface TagValueDefinition {
  /** Accent step 1–5, mapped to --color-accent-1 through --color-accent-5 in @theme. */
  accent: 1 | 2 | 3 | 4 | 5;
  /** Optional label override; defaults to the value, capitalized. */
  label?: string;
}

export interface TagDefinition {
  /** The tag name as it appears in markdown, e.g. "Severity", "Status". Case-sensitive. */
  name: string;
  /** The allowed values, each mapped to an accent step. */
  values: Record<string, TagValueDefinition>;
}

export type TagRegistry = Record<string, TagDefinition>;
```

### 8.2 Default registry (editorial template)

```json
// src/templates/editorial/tags.json
{
  "Severity": {
    "name": "Severity",
    "values": {
      "critical":      { "accent": 1 },
      "high":          { "accent": 2 },
      "medium":        { "accent": 3 },
      "low":           { "accent": 4 },
      "informational": { "accent": 5 }
    }
  },
  "Confidence": {
    "name": "Confidence",
    "values": {
      "verified":     { "accent": 1 },
      "reasoned":     { "accent": 2 },
      "assumed":      { "accent": 3 },
      "unverifiable": { "accent": 4 }
    }
  }
}
```

### 8.3 Preprocessor (`src/lib/enhance.ts`)

The preprocessor scans the markdown for bullet lines matching `**<Tag>:** <value>` and wraps the value in backticks. The wrapped value becomes inline `code` in the rendered markdown, which the `code` component map entry routes to the `Badge` component.

**This is the v1.0.1 pattern, generalized.** The v1.0.1 regex hardcoded `Severity|Confidence`; this version reads tag names from the registry. The v1.0.1 regex only matched `- ` bullets; this version matches all bullet styles (`-`, `*`, `+`, ordered `1.`).

```typescript
// src/lib/enhance.ts
import type { TagRegistry } from "@/types/tag";

// Matches: <bullet> **<Tag>:** <value>
// - bullet: -, *, +, or <digits>.
// - Tag: any non-empty string not containing newline or colon (fixes M4: [^*] was too restrictive)
// - value: any non-empty string to end of line
const BULLET_RE = /^(\s*[-*+]\s+|\s*\d+\.\s+)\*\*([^\n*:]+):\*\*\s+(.+)$/gm;

export interface EnhanceResult {
  enhanced: string;
  warnings: string[];
}

export function enhanceMarkdown(
  markdown: string,
  registry: TagRegistry,
): EnhanceResult {
  const warnings: string[] = [];
  const tagNames = Object.keys(registry);

  // Normalize line endings to \n so the regex (which uses \n) works on CRLF files
  const normalized = markdown.replace(/\r\n/g, "\n");

  const enhanced = normalized.replace(
    BULLET_RE,
    (match, bullet: string, tag: string, value: string) => {
      const trimmedTag = tag.trim();
      const trimmedValue = value.trim();

      if (!registry[trimmedTag]) {
        // Not a registered tag — leave unchanged, but warn if it looks like a common one
        if (/^(Severity|Confidence|Status|Visibility|Priority)$/i.test(trimmedTag)) {
          warnings.push(
            `Line contains "${trimmedTag}:" but "${trimmedTag}" is not in the registry. ` +
            `Add it to tags.json or rename the bullet. Registered tags: ${tagNames.join(", ")}.`,
          );
        }
        return match;
      }

      const lowerValue = trimmedValue.toLowerCase();
      if (!registry[trimmedTag].values[lowerValue]) {
        warnings.push(
          `Unknown value "${trimmedValue}" for tag "${trimmedTag}". ` +
          `Allowed: ${Object.keys(registry[trimmedTag].values).join(", ")}.`,
        );
        return match;
      }

      return `${bullet}**${trimmedTag}:** \`${trimmedValue}\``;
    },
  );

  return { enhanced, warnings };
}
```

**Improvements over v1.0.1:**
1. Accepts all bullet styles (`-`, `*`, `+`, ordered `1.`) — v1.0.1 only matched `-`.
2. Emits build-time warnings for unknown tags and values — v1.0.1 silently passed them through as plain text.
3. Tag set is data (JSON), not code — v1.0.1 hardcoded 9 keys.
4. CRLF-safe — normalizes `\r\n` to `\n` before regex (fixes the same class of bug as M2).
5. Tag-name character class `[^\\n*:]+` is permissive without being ambiguous (fixes M4: `[^*]+` was technically correct but excluded unusual tag names).

### 8.4 Badge component (`src/components/Badge.tsx`)

The `Badge` component receives the tag name, value, and accent step. It looks up the accent style from a fixed map and renders an accessible `<span>` with `aria-label`.

```typescript
// src/components/Badge.tsx
import { cn } from "@/utils/cn";

const ACCENT_STYLES: Record<number, string> = {
  1: "bg-red-50    ring-red-200    text-accent-1",
  2: "bg-amber-50  ring-amber-200  text-accent-2",
  3: "bg-yellow-50 ring-yellow-200 text-accent-3",
  4: "bg-lime-50   ring-lime-200   text-accent-4",
  5: "bg-blue-50   ring-blue-200   text-accent-5",
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
        "inline-flex items-center rounded-full px-2.5 py-0.5",
        "text-sm font-semibold tracking-wide uppercase",  // 14px, was 12px in v1.0.1 — fixes AAA contrast
        "ring-1 ring-inset",
        ACCENT_STYLES[accent],
      )}
      data-tag={tag}
      data-value={value}
      aria-label={`${tag}: ${value}`}
    >
      {value}
    </span>
  );
}
```

**Contrast fix:** Badge text is `text-sm` (14px) instead of `text-xs` (12px). At 14px, the WCAG AAA threshold relaxes to 4.5:1, which all accent-1 through accent-5 pairs clear. This addresses v1.0.1's self-documented AAA contrast failure (badge text was 4.76:1, failing AAA at 12px).

### 8.5 How the badge pipeline connects (end-to-end)

This is the critical path that v1.0.1 got right, draft_d broke (raw HTML), and draft_q2 disconnected (AST plugin vs. React component). v2.0.0 preserves v1.0.1's pattern:

```
1. Author writes:        - **Severity:** critical
2. enhance.ts wraps:     - **Severity:** `critical`
3. react-markdown parses:inline code element with children="critical"
4. components.code:      <Badge tag="Severity" value="critical" accent={1} />
5. Badge renders:        <span class="... text-accent-1 ...">critical</span>
```

No `dangerouslySetInnerHTML`. No raw HTML emission. No AST plugin that doesn't connect to the React component. The `code` component map entry is the bridge between react-markdown's parsing and the `Badge` component:

```typescript
// src/components/MarkdownReport.tsx (excerpt)
import { Badge } from "./Badge";
import { useTagRegistry } from "@/lib/tags";

const components: ComponentsMap = {
  // ... other elements ...
  code: ({ children, className }) => {
    // Inline code (no className) → check if it's a badge value
    if (!className && typeof children === "string") {
      const value = children.trim();
      const registry = useTagRegistry();
      for (const [tagName, definition] of Object.entries(registry)) {
        const lowerValue = value.toLowerCase();
        if (definition.values[lowerValue]) {
          return (
            <Badge
              tag={tagName}
              value={value}
              accent={definition.values[lowerValue].accent}
            />
          );
        }
      }
    }
    // Fallback: plain inline code or code block
    return <code className={className}>{children}</code>;
  },
};
```

**Note on the `useTagRegistry` hook:** The registry is loaded at build time (via Vite's `?raw` or `?json` import) and passed via React Context. The hook reads from context. This avoids prop-drilling and allows document-level overrides via frontmatter `badgeConfig`.

---

## 9. TOC & Navigation Contract

The TOC extracts headings from the markdown, generates slugs that match `rehype-slug`'s rendered `id` attributes, and renders a recursive navigation tree. Active-section highlighting uses `IntersectionObserver`. Slug parity between `github-slugger` (TOC) and `rehype-slug` (rendered headings) is verified by a unit test (§15.4) — this is the single most important test in the skill.

### 9.1 TOC extraction (`src/lib/toc.ts`)

```typescript
// src/lib/toc.ts
import GithubSlugger from "github-slugger";
import type { TocItem } from "@/types/toc";

const HEADING_RE = /^(#{2,4})\s+(.+)$/gm;

export function buildToc(markdown: string, maxDepth: 2 | 3 | 4 = 3): TocItem[] {
  const slugger = new GithubSlugger();
  const items: TocItem[] = [];
  const stack: TocItem[] = [];

  // Normalize line endings (CRLF-safe)
  const normalized = markdown.replace(/\r\n/g, "\n");

  for (const match of normalized.matchAll(HEADING_RE)) {
    const level = match[1].length as 2 | 3 | 4;
    if (level > maxDepth) continue;

    const text = match[2].replace(/`/g, "").trim();
    const slug = slugger.slug(text);

    const item: TocItem = { level, text, slug, children: [] };

    // Pop stack until the top is a strict parent (level < current level).
    // This correctly handles level jumps (H2 → H4) and sibling headings (H2 → H2).
    // Fixes H2: draft_k's `while (stack.length > level - 1) stack.pop()` was buggy.
    while (stack.length && stack[stack.length - 1].level >= level) {
      stack.pop();
    }

    if (stack.length === 0) {
      items.push(item);
    } else {
      stack[stack.length - 1].children.push(item);
    }
    stack.push(item);
  }

  return items;
}
```

**Why this is correct:** The `while` loop pops until the top of the stack has a level *strictly less than* the current heading's level. This means:
- H2 → H2: stack has `[H2]`. New H2's level (2) is `>=` top's level (2), so pop. Stack is empty. Push new H2 as top-level. ✓
- H2 → H3: stack has `[H2]`. New H3's level (3) is `>=` top's level (2)? No (3 >= 2 is true, but we want H3 to be a child of H2). Wait — `>=` means "pop while top's level is greater than or equal to current." For H2 (top, level 2) and H3 (current, level 3): `2 >= 3` is false, so don't pop. H3 becomes child of H2. ✓
- H2 → H4 (skipping H3): stack has `[H2]`. New H4's level (4). `2 >= 4` is false, so don't pop. H4 becomes child of H2. ✓ (This is correct: H4 is a sub-subsection of H2 when there's no H3.)
- H2 → H4 → H3: After H4, stack is `[H2, H4]`. New H3's level (3). Pop while top's level `>= 3`: top is H4 (level 4), `4 >= 3` true, pop. Top is now H2 (level 2), `2 >= 3` false, stop. H3 becomes child of H2. ✓ (H3 is a sibling of H4, both children of H2.)

### 9.2 TOC contract

| Heading Level | TOC Depth | Indentation |
|---------------|-----------|-------------|
| `##` (H2) | 1 | None |
| `###` (H3) | 2 | `ml-3` + left border |
| `####` (H4) | 3 | `ml-6` + left border |

- `buildToc()` extracts **H2, H3, and H4** headings by default (configurable via `maxDepth`)
- Orphan headings (no preceding parent) become top-level
- Backticks in heading text are stripped for display but the slug is generated from the stripped text (matching `rehype-slug` behavior)
- Slugs generated by `github-slugger` **must match `rehype-slug` output** — verified by `slug-parity.test.ts` (§15.4)

### 9.3 Active-section highlighting (new in v2.0.0)

```typescript
// src/App.tsx (excerpt)
const [activeSlug, setActiveSlug] = useState<string>("");

useEffect(() => {
  const observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          setActiveSlug(entry.target.id);
        }
      }
    },
    { rootMargin: "-80px 0px -80% 0px" },
  );

  for (const item of toc) {
    const el = document.getElementById(item.slug);
    if (el) observer.observe(el);
    for (const child of item.children) {
      const childEl = document.getElementById(child.slug);
      if (childEl) observer.observe(childEl);
    }
  }

  return () => observer.disconnect();
}, [toc]);
```

Pass `activeSlug` to `TableOfContents` to highlight the current section. This is a usability upgrade absent in v1.0.1.

### 9.4 Adding content procedure

1. Edit `src/content/document.md` (or set the markdown path via frontmatter/config)
2. Use `##` for major sections, `###` for subsections, `####` for details
3. Add badge lines as `- **Tag:** value` immediately after relevant findings
4. (Optional) Add YAML frontmatter for title, author, template selection
5. Run `npm run typecheck && npm run lint && npm run test && npm run a11y && npm run build` (the full pre-ship gate, §18)
6. No code files touched — only the markdown source

---

## 10. Accessibility (WCAG 2.2 AA + AAA Aspirational)

The headline conformance claim is **WCAG 2.2 AA + AAA aspirational, with documented exceptions**. This is honest: AA is the gate (zero violations allowed); AAA is the target where feasible, with `target-size` and `color-contrast` as gate-failures and other AAA criteria as warnings. v1.0.1 claimed "WCAG AAA" while self-documenting multiple AAA failures — that contradiction is resolved here by claiming only what is verified.

### 10.1 Implementation matrix

| Feature | Implementation | Verification |
|---------|----------------|--------------|
| Skip-to-content | `<a href="#content" class="sr-only focus:not-sr-only focus:z-50 …">` | Manual: Tab on load → focus moves to skip link → Enter → focus moves to `#content` |
| Focus visible | Global `:focus-visible { outline: 2px solid var(--color-teal-600); outline-offset: 2px; }` | Manual: Tab through all interactive elements; axe check `color-contrast` |
| Heading hierarchy | H1 → H2 → H3 → H4; no skipped levels | Lighthouse check `heading-order` |
| Anchor offset | `scroll-mt-24` on all anchored headings | Manual: click TOC link; heading appears below sticky header, not under it |
| Reduced motion | `@media (prefers-reduced-motion: reduce)` disables smooth scroll + animations | Manual: macOS "Reduce motion" setting; TOC click should jump, not animate |
| Touch targets | All interactive elements ≥ 44×44 px (`min-w-11 min-h-11` or `p-2.5`+icon) | axe check `target-size` (gate-failure) |
| ARIA labels | `aria-label` on nav, drawer trigger/close, theme toggle; `aria-hidden="true"` on decorative icons | axe check `aria-valid-attr`, `button-name` |
| Semantic landmarks | `<header>`, `<main>`, `<aside>`, `<nav>`, `<article>`, `<footer>` | axe check `region` |
| Color contrast | Body text ≥ 7:1 (AAA); meta text ≥ 4.5:1; badge text (14px) ≥ 4.5:1 | axe check `color-contrast` (gate-failure) |
| Color isn't sole indicator | Badges use text + background tint + ring, not color alone | Manual: simulate deuteranopia in DevTools |
| Keyboard nav | Full keyboard operability; no keyboard traps; Escape closes drawer | Manual: Tab/Shift+Tab through entire page |
| Language | `<html lang="...">` set from markdown frontmatter or detected | axe check `html-has-lang` |
| Live regions | Error announcements use `role="alert"`; loading uses `aria-live="polite"` | axe check `aria-live` |

### 10.2 Pre-ship a11y command

```bash
npm run a11y
# Equivalent to: playwright test tests/accessibility/
```

**`tests/accessibility/wcag-aa.test.ts`:**

```typescript
import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

test("document passes WCAG 2.2 AA", async ({ page }) => {
  await page.goto("http://localhost:4173/");  // vite preview port
  const results = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa", "wcag22aa"])
    .analyze();
  expect(results.violations).toEqual([]);
});
```

**`tests/accessibility/wcag-aaa-aspirational.test.ts`:**

```typescript
import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

test("document passes WCAG 2. AAA where feasible", async ({ page }) => {
  await page.goto("http://localhost:4173/");
  const results = await new AxeBuilder({ page })
    .withTags(["wcag2aaa", "wcag22aaa"])
    .analyze();

  // AAA violations are warnings, not failures, except for:
  // - target-size (touch targets < 44px)
  // - color-contrast (text contrast below AAA threshold)
  // These two are gate-failures because they are achievable for this skill.
  const critical = results.violations.filter(
    (v) => ["target-size", "color-contrast"].includes(v.id),
  );
  expect(critical).toEqual([]);

  // Log non-critical AAA violations as warnings
  for (const v of results.violations) {
    if (!["target-size", "color-contrast"].includes(v.id)) {
      console.warn(`AAA warning: ${v.id} — ${v.description}`);
    }
  }
});
```

### 10.3 Concrete AAA fixes over v1.0.1

| v1.0.1 gap | v2.0.0 fix |
|------------|------------|
| Touch targets 32–36 px (`p-1.5`) | Touch targets ≥ 44 px (`p-2.5` + icon, or `min-w-11 min-h-11`) |
| Badge text 12 px (4.76:1, fails AAA) | Badge text 14 px (≥ 4.5:1 at 14px, passes AAA) |
| No `prefers-reduced-motion` | `@media (prefers-reduced-motion: reduce)` disables smooth scroll + animations |
| Browser default focus outline only | Global `:focus-visible` style with 2px teal outline |
| No axe in CI | `npm run a11y` runs `@axe-core/playwright` against the built dist |

---

## 11. Build & Deploy Recipes

### 11.1 Recipe A — Default single-file build (CDN fonts)

```bash
npm run build
# Output: dist/index.html (JS/CSS inlined; fonts load from Google Fonts CDN)
# Size: ~250-400 KB
# Deploy: any static host (GitHub Pages, Netlify, Vercel, S3, nginx)
```

**`vite.config.ts`:**

```typescript
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import { viteSingleFile } from "vite-plugin-singlefile";
import { resolve } from "path";

export default defineConfig({
  plugins: [react(), tailwindcss(), viteSingleFile()],
  resolve: { alias: { "@": resolve(__dirname, "src") } },
  build: {
    target: "es2022",
    cssCodeSplit: false,
    rollupOptions: {
      output: { inlineDynamicImports: true },
    },
  },
});
```

### 11.2 Recipe B — Offline single-file build (fonts inlined)

```bash
npm run build:offline
# Runs: node scripts/build-offline.mjs
# Output: dist/index.html (JS/CSS/fonts all inlined as base64)
# Size: ~2-4 MB (depending on font subset)
# Deploy: any static host, USB stick, file://, air-gapped environment
```

**`scripts/build-offline.mjs`:**

```javascript
// scripts/build-offline.mjs
// Sketch — requires runtime validation with actual @fontsource packages.
// The @fontsource packages ship font files in node_modules.
// Vite's `assetsInlineLimit` setting (set very high) inlines them as base64.
import { build } from "vite";
import { viteSingleFile } from "vite-plugin-singlefile";

process.env.VITE_OFFLINE_FONTS = "true";

await build({
  plugins: [viteSingleFile()],
  build: {
    target: "es2022",
    cssCodeSplit: false,
    assetsInlineLimit: 100 * 1024 * 1024,  // 100 MB — inline everything
    rollupOptions: { output: { inlineDynamicImports: true } },
  },
});
```

In `src/main.tsx`, conditionally import the `@fontsource` packages so they get bundled only in offline mode:

```typescript
// src/main.tsx
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { App } from "./App";
import { ErrorBoundary } from "./components/ErrorBoundary";
import "./index.css";

// Conditional font import for offline build
if (import.meta.env.VITE_OFFLINE_FONTS === "true") {
  await import("@fontsource-variable/source-serif-4");
  await import("@fontsource-variable/inter");
  await import("@fontsource/jetbrains-mono");
}

const root = createRoot(document.getElementById("root")!);
root.render(
  <StrictMode>
    <ErrorBoundary>
      <App />
    </ErrorBoundary>
  </StrictMode>,
);
```

**Note:** The `build-offline.mjs` script is a sketch. Runtime validation required:
1. Confirm `@fontsource` packages resolve the font files via Vite's asset pipeline.
2. Confirm `assetsInlineLimit: 100MB` causes base64 inlining (not just URL copying).
3. Confirm the resulting `dist/index.html` renders fonts correctly when opened from `file://` with no network.
4. If the offline build exceeds 5 MB, subset fonts to only the glyphs used (e.g., `pyftsubset` from `fonttools`).

### 11.3 Recipe C — GitHub Pages deployment

```bash
# 1. Set base in vite.config.ts
# base: "/<repo-name>/"

# 2. Build
npm run build

# 3. Deploy (using gh-pages or actions/upload-pages-artifact)
npx gh-pages -d dist
```

For GitHub Actions deployment, see §16.1's CI workflow — it uses `actions/upload-pages-artifact` + `actions/deploy-pages` for native GitHub Pages deployment without third-party tokens.

### 11.4 Recipe D — Local file:// viewing

The default build works from `file://` because `vite-plugin-singlefile` removes all `<script type="module" src="...">` and `<link rel="stylesheet" href="...">` references — everything is inlined into one HTML file.

```bash
npm run build
open dist/index.html        # macOS
# xdg-open dist/index.html  # Linux
# start dist/index.html     # Windows
```

**Caveat:** The online build's Google Fonts `@import` will fail from `file://` (CORS restriction). For `file://` viewing, use Recipe B (offline build) which inlines fonts as base64.

---

## 12. Error Handling & Resilience

Errors are inevitable. The skill handles them at three layers: (1) build-time warnings from the preprocessor, (2) React error boundaries catching render failures, and (3) a structured error reporter for production observability. The architecture avoids `dangerouslySetInnerHTML` entirely — react-markdown's component map renders Markdown as React elements, so a malformed markdown file produces a React render error (caught by the boundary) rather than an XSS surface.

### 12.1 Error boundary (`src/components/ErrorBoundary.tsx`)

```typescript
// src/components/ErrorBoundary.tsx
import { Component, type ErrorInfo, type ReactNode } from "react";
import { ErrorFallback } from "./ErrorFallback";

interface Props {
  children: ReactNode;
  fallback?: ReactNode | ((error: Error, errorInfo: ErrorInfo) => ReactNode);
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
}

interface State {
  hasError: boolean;
  error: Error | null;
  errorInfo: ErrorInfo | null;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error: Error): Partial<State> {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    this.setState({ errorInfo });
    this.props.onError?.(error, errorInfo);

    // Report to error reporting service (if configured)
    ErrorReporter.report(error, { componentStack: errorInfo.componentStack }).catch(
      (reportErr) => {
        // Don't let reporting failure mask the original error
        console.error("Failed to report error:", reportErr);
      },
    );

    if (import.meta.env.DEV) {
      console.error("ErrorBoundary caught an error:", error, errorInfo);
    }
  }

  render(): ReactNode {
    if (this.state.hasError) {
      if (this.props.fallback) {
        if (typeof this.props.fallback === "function") {
          return this.props.fallback(this.state.error!, this.state.errorInfo!);
        }
        return this.props.fallback;
      }
      return <ErrorFallback error={this.state.error} />;
    }
    return this.props.children;
  }
}

// Import at top of file:
// import { ErrorReporter } from "@/utils/error-reporter";
```

### 12.2 Error fallback UI (`src/components/ErrorFallback.tsx`)

```typescript
// src/components/ErrorFallback.tsx
interface Props {
  error?: Error | null;
  onRetry?: () => void;
}

export function ErrorFallback({ error, onRetry }: Props) {
  return (
    <div
      role="alert"
      aria-live="assertive"
      className="p-6 m-4 rounded-lg border border-red-200 bg-red-50"
    >
      <h2 className="text-lg font-semibold text-red-900 mb-2">
        Rendering Error
      </h2>
      <p className="text-sm text-red-800 mb-4">
        We encountered an error while rendering this content. The document may
        contain malformed markdown or an unsupported feature.
      </p>
      {import.meta.env.DEV && error && (
        <details className="text-xs mb-4">
          <summary className="cursor-pointer text-red-700">
            Error details (development only)
          </summary>
          <pre className="mt-2 p-2 bg-red-100 rounded overflow-auto whitespace-pre-wrap">
            {error.toString()}
            {error.stack && `\n\n${error.stack}`}
          </pre>
        </details>
      )}
      {onRetry && (
        <button
          type="button"
          onClick={onRetry}
          className="px-4 py-2 rounded bg-red-700 text-white text-sm font-medium hover:bg-red-800"
        >
          Try again
        </button>
      )}
    </div>
  );
}
```

### 12.3 Error reporter (`src/utils/error-reporter.ts`)

```typescript
// src/utils/error-reporter.ts
interface ErrorReport {
  message: string;
  stack?: string;
  componentStack?: string;
  context: Record<string, unknown>;
  timestamp: number;
  userAgent: string;
  url: string;
}

export class ErrorReporter {
  // Endpoint configured via env var; if unset, reports are logged but not sent.
  private static endpoint = import.meta.env.VITE_ERROR_REPORTING_ENDPOINT;

  static async report(
    error: Error,
    context: Record<string, unknown> = {},
  ): Promise<void> {
    const report: ErrorReport = {
      message: error.message,
      stack: error.stack,
      context,
      timestamp: Date.now(),
      userAgent: navigator.userAgent,
      url: window.location.href,
    };

    if (this.endpoint) {
      try {
        await fetch(this.endpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(report),
        });
      } catch (err) {
        // Don't let reporting failure mask the original error.
        // Log and continue; the original error is already in the boundary.
        console.error("Failed to report error:", err);
      }
    }

    if (import.meta.env.DEV) {
      console.error("Error reported:", error, context);
    }
  }
}
```

### 12.4 Malformed markdown handling

| Scenario | Behavior |
|----------|----------|
| Unclosed code fence | `react-markdown` renders as plain text — no crash |
| Broken table syntax | Table renders as plain text — no crash |
| Invalid frontmatter YAML | `extractFrontmatter()` returns empty object; document still renders (with default title from first H1) |
| Missing `?raw` import | Build-time Vite error — caught before runtime |
| Badge value not in registry | Renders as neutral inline `<code>` — no crash; warning emitted at build time by `enhance.ts` |
| Unknown tag name | Bullet renders as plain markdown — no crash; warning emitted if the name looks like a common tag (Severity, Confidence, Status, etc.) |
| Empty markdown | `buildToc()` returns `[]`; `MarkdownReport` renders an empty `<article>`; no crash |
| Markdown with no headings | `buildToc()` returns `[]`; sidebar/drawer renders "No sections" message; no crash |

### 12.5 What NOT to do (architectural)

**Do not use `dangerouslySetInnerHTML`** to render markdown output. This was a defect in one of the merged drafts (C2 in the audit). react-markdown's component map exists to render Markdown as React elements — serializing to HTML and using `dangerouslySetInnerHTML` discards the benefits (type safety, accessibility attributes, reconciliation) and creates an XSS surface even with sanitization. If raw HTML pass-through is genuinely needed, use `rehype-raw` paired with `rehype-sanitize` and document the security implications explicitly. The default skill does not enable this path.

### 12.6 Nested error boundaries

For granular error handling, nest boundaries so a failure in one region doesn't take down the whole page:

```tsx
<ErrorBoundary fallback={<GlobalError />}>
  <Header />
  <Layout>
    <ErrorBoundary fallback={<SidebarError />}>
      <Sidebar />
    </ErrorBoundary>
    <main>
      <ErrorBoundary fallback={<ContentError />}>
        <MarkdownReport markdown={content} />
      </ErrorBoundary>
    </main>
  </Layout>
</ErrorBoundary>
```

---

## 13. Font Strategy & Offline Support

v1.0.1's central pain point was the "single-file portability" half-promise: `vite-plugin-singlefile` inlined JS and CSS but not the Google Fonts `@import`, so the artifact didn't actually work offline. v2.0.0 resolves this with two build modes (online and offline) and three font strategies (CDN `@import`, self-hosted `@font-face`, `@fontsource` base64 inlining). The offline mode is the default for the minimal print template; the online mode is the default for editorial and technical.

### 13.1 Strategy A — CDN `@import` (default, online build)

The editorial and technical templates default to Google Fonts `@import` in CSS. This is the smallest build (~250–400 KB) and the fastest to develop with, but requires network at runtime.

```css
/* src/templates/editorial/theme.css (online mode) */
@import url("https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap");

@import "tailwindcss";

@theme {
  --font-serif: "Source Serif 4", ui-serif, Georgia, serif;
  --font-sans: "Inter", ui-sans-serif, system-ui, sans-serif;
  --font-mono: "JetBrains Mono", ui-monospace, monospace;
  /* ... rest of @theme ... */
}
```

**Caveat:** `@import` must come *before* `@import "tailwindcss"` per CSS spec. Tailwind v4's `@theme` block comes after both. The `@import` will fail from `file://` (CORS) — use Strategy C (offline) for `file://` viewing.

### 13.2 Strategy B — Self-hosted `@font-face` (alternative online build)

Self-host the font files in `public/fonts/` and declare `@font-face` rules. This avoids the Google Fonts CDN dependency but still requires the font files to be served alongside the HTML.

```css
/* src/templates/editorial/theme.css (self-hosted mode) */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url('/fonts/inter-v12-latin-400.woff2') format('woff2');
}

@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 600;
  font-display: swap;
  src: url('/fonts/inter-v12-latin-600.woff2') format('woff2');
}

@font-face {
  font-family: 'Source Serif 4';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url('/fonts/source-serif-4-v3-latin-400.woff2') format('woff2');
}

@font-face {
  font-family: 'Source Serif 4';
  font-style: normal;
  font-weight: 600;
  font-display: swap;
  src: url('/fonts/source-serif-4-v3-latin-600.woff2') format('woff2');
}

@font-face {
  font-family: 'JetBrains Mono';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url('/fonts/jetbrains-mono-v18-latin-400.woff2') format('woff2');
}

@import "tailwindcss";

@theme {
  --font-serif: "Source Serif 4", ui-serif, Georgia, serif;
  --font-sans: "Inter", ui-sans-serif, system-ui, sans-serif;
  --font-mono: "JetBrains Mono", ui-monospace, monospace;
  /* ... rest of @theme ... */
}
```

**Preload hints in `index.html`:**

```html
<link rel="preload" href="/fonts/inter-v12-latin-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/inter-v12-latin-600.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/source-serif-4-v3-latin-400.woff2" as="font" type="font/woff2" crossorigin>
```

**Caveat:** With `vite-plugin-singlefile`, the `@font-face` URLs reference `/fonts/...` which won't be inlined — the single-file artifact will still need the font files alongside it. For true single-file portability, use Strategy C.

### 13.3 Strategy C — `@fontsource` base64 inlining (offline build)

The offline build (Recipe B in §11.2) uses `@fontsource` packages which ship font files in `node_modules`. Vite's `assetsInlineLimit` setting (set to 100 MB in `build-offline.mjs`) inlines them as base64 data URIs directly into the CSS, which is then inlined into the HTML by `vite-plugin-singlefile`. The result is a truly self-contained `dist/index.html` that works from `file://`, USB, or air-gapped environments.

In `src/main.tsx`:

```typescript
// Conditional import — only bundles @fontsource packages when VITE_OFFLINE_FONTS=true
if (import.meta.env.VITE_OFFLINE_FONTS === "true") {
  await import("@fontsource-variable/source-serif-4");
  await import("@fontsource-variable/inter");
  await import("@fontsource/jetbrains-mono");
}
```

In `src/templates/editorial/theme.css` (offline mode — no `@import`):

```css
/* No Google Fonts @import — fonts are bundled via @fontsource in main.tsx */
@import "tailwindcss";

@theme {
  --font-serif: "Source Serif 4", ui-serif, Georgia, serif;
  --font-sans: "Inter", ui-sans-serif, system-ui, sans-serif;
  --font-mono: "JetBrains Mono", ui-monospace, monospace;
  /* ... rest of @theme ... */
}
```

**Tradeoffs:**
- Online build: ~250–400 KB, requires network for fonts
- Self-hosted build: ~250–400 KB HTML + ~150 KB font files, no CDN dependency
- Offline build: ~2–4 MB single file, fully self-contained

### 13.4 System font fallbacks

All three strategies use the same fallback chain in `@theme`:

```css
--font-serif: "Source Serif 4", ui-serif, Georgia, serif;
--font-sans: "Inter", ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
--font-mono: "JetBrains Mono", ui-monospace, "Cascadia Code", "Source Code Pro", Menlo, Consolas, monospace;
```

If a web font fails to load (network blocked, font file missing), the browser falls back to a similar system font. The design will degrade gracefully — not pixel-identical, but readable and functional.

### 13.5 Offline verification test

```typescript
// tests/e2e/offline.test.ts
import { test, expect } from "@playwright/test";

test("offline build works without network", async ({ page, context }) => {
  // Build the offline variant first: npm run build:offline
  await page.goto("http://localhost:4173/");  // serve dist/ via `npm run preview`
  await page.waitForLoadState("networkidle");

  // Go offline
  await context.setOffline(true);

  // Reload
  await page.reload();

  // Verify fonts still render (not falling back to system fonts)
  const bodyFont = await page.locator("body").evaluate(
    (el) => getComputedStyle(el).fontFamily,
  );
  // The @fontsource font-family name should appear in the computed style
  expect(bodyFont).toMatch(/Source Serif 4|Inter/);

  // Verify content still renders
  await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
});
```

---

## 14. Performance Optimization

Performance budgets are explicit and enforced in CI (§16). The budgets below are realistic, not aspirational — they account for React 19, react-markdown, the remark/rehype ecosystem, and the application code. v1.0.1 had no performance budgets; one of the merged drafts (draft_q2) had a 150 KB gzipped budget that was unrealistically low and would have forced feature cuts. v2.0.0 sets the budget at 250 KB gzipped, which is achievable without sacrificing functionality.

### 14.1 Performance budgets

| Metric | Budget | Measurement | Gate |
|--------|--------|-------------|------|
| Bundle size (gzipped) | < 250 KB | `rollup-plugin-visualizer` | CI failure |
| Bundle size (raw) | < 800 KB | `rollup-plugin-visualizer` | Warning |
| First Contentful Paint | < 1.5 s | Lighthouse CI | CI failure if > 2.5 s |
| Time to Interactive | < 3 s | Lighthouse CI | CI failure if > 4 s |
| Largest Contentful Paint | < 2.5 s | Lighthouse CI | CI failure if > 4 s |
| Cumulative Layout Shift | < 0.1 | Lighthouse CI | CI failure if > 0.25 |
| Markdown parsing (1000 lines) | < 100 ms | Custom benchmark | CI failure |
| Markdown parsing (5000 lines) | < 500 ms | Custom benchmark | CI failure |
| TOC extraction (100 headings) | < 50 ms | Custom benchmark | CI failure |

**Bundle composition (estimated, Reasoned — not Verified):**
- React 19 + react-dom: ~45 KB gzipped
- react-markdown + remark-parse + remark-gfm + remark-rehype + rehype-slug: ~80–120 KB gzipped
- lucide-react (tree-shaken to 6 icons): ~5 KB gzipped
- clsx + tailwind-merge: ~3 KB gzipped
- Application code (components, lib, templates): ~30–50 KB gzipped
- **Total estimated: ~160–225 KB gzipped** (within the 250 KB budget)

If `syntaxHighlighting: true` is enabled, add ~30 KB gzipped for `rehype-highlight` + highlight.js common languages. If `rehype-raw` + `rehype-sanitize` are enabled, add ~25 KB gzipped. Both still fit within the 250 KB budget.

### 14.2 Optimization techniques

**Memoization:**

```typescript
// src/components/MarkdownReport.tsx
import { useMemo } from "react";
import { enhanceMarkdown } from "@/lib/enhance";
import { buildToc } from "@/lib/toc";

export function MarkdownReport({ markdown, registry }: Props) {
  // Memoize the enhanced markdown (regex preprocessing)
  const enhanced = useMemo(
    () => enhanceMarkdown(markdown, registry),
    [markdown, registry],
  );

  // Memoize the TOC
  const toc = useMemo(
    () => buildToc(enhanced.enhanced),
    [enhanced.enhanced],
  );

  // Memoize the components map (stable reference unless registry changes)
  const components = useMemo(
    () => buildComponentsMap(registry),
    [registry],
  );

  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      rehypePlugins={[rehypeSlug]}
      components={components}
    >
      {enhanced.enhanced}
    </ReactMarkdown>
  );
}
```

**Code splitting (only for very large documents):**

For documents > 50,000 words, consider lazy-loading the `MarkdownReport` component. For typical documents (1,000–10,000 words), the parsing time is < 100 ms and lazy loading adds unnecessary overhead.

```typescript
// Only for very large documents
const MarkdownReport = lazy(() => import("./components/MarkdownReport"));

<Suspense fallback={<LoadingSpinner />}>
  <MarkdownReport markdown={content} registry={registry} />
</Suspense>
```

**Virtual scrolling (only for extreme cases):**

For documents > 100,000 words, consider virtual scrolling with `@tanstack/react-virtual`. This is out of scope for the default skill but documented as an extension point (§20).

### 14.3 Performance monitoring (optional)

For production deployments, the `PerformanceMonitor` class measures rendering time and reports to an analytics endpoint. This is optional and disabled by default.

```typescript
// src/utils/performance-monitor.ts
export class PerformanceMonitor {
  private static metrics: Map<string, number[]> = new Map();

  static measure<T>(label: string, fn: () => T): T {
    const start = performance.now();
    const result = fn();
    const duration = performance.now() - start;

    if (!this.metrics.has(label)) {
      this.metrics.set(label, []);
    }
    this.metrics.get(label)!.push(duration);

    return result;
  }

  static getAverage(label: string): number {
    const values = this.metrics.get(label) || [];
    if (values.length === 0) return 0;
    return values.reduce((a, b) => a + b, 0) / values.length;
  }

  static report(label: string): void {
    const avg = this.getAverage(label);
    if (import.meta.env.DEV) {
      console.debug(`[perf] ${label}: ${avg.toFixed(2)}ms avg`);
    }
    // In production, report to analytics endpoint if configured
    // (Do NOT hardcode gtag or any specific analytics provider — leave this
    // as an extension point for the deploying team.)
  }
}

// Usage
const result = PerformanceMonitor.measure("markdown-parse", () =>
  enhanceMarkdown(markdown, registry),
);
```

**Note:** Unlike one of the merged drafts (draft_q2), this version does NOT hardcode `window.gtag` calls. The deploying team should wire their analytics provider of choice.

### 14.4 Performance test examples

```typescript
// tests/performance/bundle-size.test.ts
import { describe, it, expect } from "vitest";
import { readFileSync, existsSync } from "fs";
import { join } from "path";
import { gzipSync } from "zlib";

describe("Bundle Size", () => {
  it("main bundle is under 250KB gzipped", () => {
    const distPath = join(process.cwd(), "dist", "index.html");
    if (!existsSync(distPath)) {
      throw new Error("dist/index.html not found. Run `npm run build` first.");
    }

    const content = readFileSync(distPath);
    const gzipped = gzipSync(content);

    expect(gzipped.length).toBeLessThan(250 * 1024);  // 250 KB
  });
});

// tests/performance/parsing-speed.test.ts
import { describe, it, expect } from "vitest";
import { buildToc } from "@/lib/toc";
import { enhanceMarkdown } from "@/lib/enhance";
import type { TagRegistry } from "@/types/tag";

function generateLargeMarkdown(lines: number): string {
  const sections: string[] = [];
  for (let i = 0; i < lines / 10; i++) {
    sections.push(`
## Section ${i}

This is paragraph ${i} with some content.

- **Severity:** critical
- **Confidence:** verified

### Subsection ${i}.1

More content here.
    `);
  }
  return sections.join("\n");
}

describe("Parsing Performance", () => {
  const registry: TagRegistry = {
    Severity: {
      name: "Severity",
      values: {
        critical: { accent: 1 },
        high: { accent: 2 },
        medium: { accent: 3 },
        low: { accent: 4 },
        informational: { accent: 5 },
      },
    },
  };

  it("parses 1000 lines in under 100ms", () => {
    const markdown = generateLargeMarkdown(1000);
    const start = performance.now();
    enhanceMarkdown(markdown, registry);
    buildToc(markdown);
    const duration = performance.now() - start;
    expect(duration).toBeLessThan(100);
  });

  it("parses 5000 lines in under 500ms", () => {
    const markdown = generateLargeMarkdown(5000);
    const start = performance.now();
    enhanceMarkdown(markdown, registry);
    buildToc(markdown);
    const duration = performance.now() - start;
    expect(duration).toBeLessThan(500);
  });
});
```

---

## 15. Testing Strategy

The test pyramid is: 70% unit tests, 20% integration tests, 10% visual/end-to-end tests. The single most important test is `slug-parity.test.ts` — it verifies that `github-slugger` (used by `buildToc`) and `rehype-slug` (used by react-markdown) produce identical slugs. If this test fails, every TOC link in every rendered document is broken. v1.0.1 had no tests at all; v2.0.0 ships the full pyramid.

### 15.1 Test pyramid

```
           /\
          /  \         Visual Regression (10%)
         /----\        - Screenshot comparisons
        /      \       - Cross-browser rendering
       /--------\
      /   E2E    \     End-to-End (10%)
     /------------\    - Full user workflows
    /  Integration \   20% - Navigation, TOC, badges
   /----------------\
  /    Unit Tests    \  70% - Pure functions, components
 /--------------------\ - enhance, toc, frontmatter, slug-parity
/______________________\
```

### 15.2 Unit tests — `enhance.test.ts`

```typescript
// tests/unit/enhance.test.ts
import { describe, it, expect } from "vitest";
import { enhanceMarkdown } from "@/lib/enhance";
import type { TagRegistry } from "@/types/tag";

const registry: TagRegistry = {
  Severity: {
    name: "Severity",
    values: {
      critical: { accent: 1 },
      high: { accent: 2 },
      medium: { accent: 3 },
    },
  },
  Confidence: {
    name: "Confidence",
    values: {
      verified: { accent: 1 },
      reasoned: { accent: 2 },
    },
  },
};

describe("enhanceMarkdown", () => {
  describe("bullet styles", () => {
    it("matches dash bullets (-)", () => {
      const md = "- **Severity:** critical";
      const { enhanced } = enhanceMarkdown(md, registry);
      expect(enhanced).toBe("- **Severity:** `critical`");
    });

    it("matches asterisk bullets (*)", () => {
      const md = "* **Severity:** critical";
      const { enhanced } = enhanceMarkdown(md, registry);
      expect(enhanced).toBe("* **Severity:** `critical`");
    });

    it("matches plus bullets (+)", () => {
      const md = "+ **Severity:** critical";
      const { enhanced } = enhanceMarkdown(md, registry);
      expect(enhanced).toBe("+ **Severity:** `critical`");
    });

    it("matches ordered bullets (1.)", () => {
      const md = "1. **Severity:** critical";
      const { enhanced } = enhanceMarkdown(md, registry);
      expect(enhanced).toBe("1. **Severity:** `critical`");
    });

    it("matches indented bullets", () => {
      const md = "  - **Severity:** critical";
      const { enhanced } = enhanceMarkdown(md, registry);
      expect(enhanced).toBe("  - **Severity:** `critical`");
    });
  });

  describe("multiple matches", () => {
    it("transforms all matching lines in a document", () => {
      const md = `
## Finding 1
- **Severity:** critical
- **Confidence:** verified

## Finding 2
- **Severity:** high
- **Confidence:** reasoned
      `;
      const { enhanced } = enhanceMarkdown(md, registry);
      expect(enhanced).toContain("`critical`");
      expect(enhanced).toContain("`verified`");
      expect(enhanced).toContain("`high`");
      expect(enhanced).toContain("`reasoned`");
    });
  });

  describe("CRLF handling", () => {
    it("works on Windows line endings (\\r\\n)", () => {
      const md = "- **Severity:** critical\r\n- **Confidence:** verified\r\n";
      const { enhanced } = enhanceMarkdown(md, registry);
      expect(enhanced).toContain("`critical`");
      expect(enhanced).toContain("`verified`");
    });
  });

  describe("warnings", () => {
    it("warns on unknown tag that looks like a common tag", () => {
      const md = "- **Priority:** high";  // Priority not in registry
      const { warnings } = enhanceMarkdown(md, registry);
      expect(warnings).toHaveLength(1);
      expect(warnings[0]).toContain("Priority");
    });

    it("does not warn on unknown tag that doesn't look common", () => {
      const md = "- **Random:** value";
      const { warnings } = enhanceMarkdown(md, registry);
      expect(warnings).toHaveLength(0);
    });

    it("warns on unknown value for known tag", () => {
      const md = "- **Severity:** catastrophic";  // catastrophic not in registry
      const { warnings } = enhanceMarkdown(md, registry);
      expect(warnings).toHaveLength(1);
      expect(warnings[0]).toContain("catastrophic");
      expect(warnings[0]).toContain("Allowed:");
    });

    it("emits warnings without breaking the render", () => {
      const md = "- **Severity:** critical\n- **Severity:** catastrophic";
      const { enhanced, warnings } = enhanceMarkdown(md, registry);
      expect(enhanced).toContain("`critical`");
      expect(enhanced).not.toContain("`catastrophic`");  // unknown value left as-is
      expect(warnings).toHaveLength(1);
    });
  });

  describe("case sensitivity", () => {
    it("matches tag names case-sensitively", () => {
      const md = "- **severity:** critical";  // lowercase tag name
      const { enhanced, warnings } = enhanceMarkdown(md, registry);
      // "severity" is not in registry (only "Severity" is)
      expect(enhanced).not.toContain("`critical`");
      // But it looks like a common tag, so warn
      expect(warnings.some((w) => w.includes("severity"))).toBe(true);
    });

    it("matches tag values case-insensitively", () => {
      const md = "- **Severity:** CRITICAL";
      const { enhanced } = enhanceMarkdown(md, registry);
      expect(enhanced).toContain("`CRITICAL`");  // preserves original case in output
    });
  });
});
```

### 15.3 Unit tests — `toc.test.ts`

```typescript
// tests/unit/toc.test.ts
import { describe, it, expect } from "vitest";
import { buildToc } from "@/lib/toc";

describe("buildToc", () => {
  describe("basic extraction", () => {
    it("extracts H2 headings", () => {
      const md = "## Section 1\n\nContent.\n\n## Section 2\n\nMore.";
      const toc = buildToc(md);
      expect(toc).toHaveLength(2);
      expect(toc[0].text).toBe("Section 1");
      expect(toc[0].level).toBe(2);
      expect(toc[0].slug).toBe("section-1");
      expect(toc[1].text).toBe("Section 2");
    });

    it("extracts H3 headings nested under H2", () => {
      const md = "## Section 1\n### Sub 1.1\n### Sub 1.2\n## Section 2";
      const toc = buildToc(md);
      expect(toc).toHaveLength(2);
      expect(toc[0].children).toHaveLength(2);
      expect(toc[0].children[0].text).toBe("Sub 1.1");
      expect(toc[0].children[1].text).toBe("Sub 1.2");
    });

    it("extracts H4 headings nested under H3", () => {
      const md = "## Section\n### Sub\n#### Detail";
      const toc = buildToc(md, 4);
      expect(toc[0].children[0].children).toHaveLength(1);
      expect(toc[0].children[0].children[0].text).toBe("Detail");
      expect(toc[0].children[0].children[0].level).toBe(4);
    });

    it("respects maxDepth", () => {
      const md = "## H2\n### H3\n#### H4";
      expect(buildToc(md, 2)).toHaveLength(1);  // only H2
      expect(buildToc(md, 3)[0].children).toHaveLength(1);  // H2 + H3, no H4
      expect(buildToc(md, 4)[0].children[0].children).toHaveLength(1);  // H2 + H3 + H4
    });
  });

  describe("level jumps (the H2 bug fix)", () => {
    it("handles H2 → H4 (skipping H3)", () => {
      const md = "## Section\n#### Detail";
      const toc = buildToc(md, 4);
      expect(toc).toHaveLength(1);
      expect(toc[0].children).toHaveLength(1);
      expect(toc[0].children[0].text).toBe("Detail");
      expect(toc[0].children[0].level).toBe(4);
    });

    it("handles H2 → H4 → H3 (sibling correctness)", () => {
      const md = "## Section\n#### Detail\n### Sub";
      const toc = buildToc(md, 4);
      // H4 is child of H2 (no H3 yet)
      // H3 should be sibling of H4, both children of H2
      expect(toc).toHaveLength(1);
      expect(toc[0].children).toHaveLength(2);
      expect(toc[0].children[0].text).toBe("Detail");
      expect(toc[0].children[0].level).toBe(4);
      expect(toc[0].children[1].text).toBe("Sub");
      expect(toc[0].children[1].level).toBe(3);
    });

    it("handles sibling H2s", () => {
      const md = "## First\n## Second\n## Third";
      const toc = buildToc(md);
      expect(toc).toHaveLength(3);
      expect(toc[0].text).toBe("First");
      expect(toc[1].text).toBe("Second");
      expect(toc[2].text).toBe("Third");
      expect(toc[0].children).toHaveLength(0);
    });
  });

  describe("orphan headings", () => {
    it("orphan H3 becomes top-level", () => {
      const md = "### Orphan\n## Section";
      const toc = buildToc(md);
      expect(toc).toHaveLength(2);
      expect(toc[0].text).toBe("Orphan");
      expect(toc[0].level).toBe(3);
      expect(toc[1].text).toBe("Section");
    });
  });

  describe("slug generation", () => {
    it("strips backticks from heading text", () => {
      const md = "## `Code` in Heading";
      const toc = buildToc(md);
      expect(toc[0].text).toBe("Code in Heading");
      expect(toc[0].slug).toBe("code-in-heading");
    });

    it("handles repeated headings (github-slugger dedup)", () => {
      const md = "## Section\n## Section";
      const toc = buildToc(md);
      expect(toc[0].slug).toBe("section");
      expect(toc[1].slug).toBe("section-1");
    });

    it("handles CJK headings", () => {
      const md = "## 中文标题";
      const toc = buildToc(md);
      expect(toc[0].text).toBe("中文标题");
      // github-slugger handles CJK
      expect(toc[0].slug).toBeTruthy();
    });
  });

  describe("edge cases", () => {
    it("handles empty markdown", () => {
      expect(buildToc("")).toEqual([]);
    });

    it("handles markdown with no headings", () => {
      expect(buildToc("Just some content.\nNo headings.")).toEqual([]);
    });

    it("handles CRLF line endings", () => {
      const md = "## Section 1\r\n\r\nContent.\r\n\r\n## Section 2\r\n";
      const toc = buildToc(md);
      expect(toc).toHaveLength(2);
      expect(toc[0].text).toBe("Section 1");
    });

    it("ignores H1 and H5 by default", () => {
      const md = "# H1\n## H2\n##### H5";
      const toc = buildToc(md);
      expect(toc).toHaveLength(1);
      expect(toc[0].text).toBe("H2");
    });
  });
});
```

### 15.4 Unit tests — `slug-parity.test.ts` (the single most important test)

This test verifies that `github-slugger` (used by `buildToc` in §9.1) and `rehype-slug` (used by react-markdown's `rehypePlugins`) produce identical slugs. If this test fails, every TOC link in every rendered document is broken — clicking a TOC entry won't scroll to the heading because the `href` slug won't match the heading's `id`.

```typescript
// tests/unit/slug-parity.test.ts
import { describe, it, expect } from "vitest";
import GithubSlugger from "github-slugger";
import rehypeSlug from "rehype-slug";
import { unified } from "unified";
import remarkParse from "remark-parse";
import remarkRehype from "remark-rehype";
import { visit } from "unist-util-visit";

// Note: github-slugger 2.0.0 exports only the default GithubSlugger class.
// There is NO named `slug` export (fixes M9: draft_z's import was wrong).

const FIXTURES = [
  "Simple Heading",
  "Heading with `code`",
  "Heading with emoji 🎉",
  "中文标题",
  "Repeated Heading",  // github-slugger dedupes with -1, -2
  "Repeated Heading",
  "  Leading whitespace  ",
  "Trailing hash #",
  "CamelCase",
  "snake_case",
  "kebab-case",
  "Heading with—em dash",
  "Heading with 'quotes'",
  "Heading with \"double quotes\"",
  "123 Numeric Start",
  "Hyphen-at-start",
];

describe("slug parity: github-slugger === rehype-slug", () => {
  for (const text of FIXTURES) {
    it(`matches for "${text}"`, async () => {
      // Generate slug with github-slugger (used by buildToc)
      const slugger = new GithubSlugger();
      const fromSlugger = slugger.slug(text);

      // Generate slug with rehype-slug (used by react-markdown)
      const md = `## ${text}`;
      const tree = unified()
        .use(remarkParse)
        .use(remarkRehype)
        .use(rehypeSlug)
        .run(unified().use(remarkParse).parse(md));

      let fromRehype: string | undefined;
      visit(tree, "element", (node: any) => {
        if (node.tagName === "h2" && node.properties?.id) {
          fromRehype = node.properties.id;
          return false;  // stop visiting
        }
      });

      expect(fromSlugger).toBe(fromRehype);
    });
  }
});

// Additional test: verify that buildToc and rehype-slug agree on a full document
describe("slug parity: buildToc slugs match rendered heading ids", () => {
  it("matches for a multi-heading document", async () => {
    const md = `
## Simple Section
### Subsection with \`code\`
## 中文标题
## Repeated
## Repeated
    `;

    // Get TOC slugs via buildToc
    const { buildToc } = await import("@/lib/toc");
    const toc = buildToc(md);
    const tocSlugs = [
      toc[0].slug,
      toc[0].children[0].slug,
      toc[1].slug,
      toc[2].slug,
      toc[3].slug,
    ];

    // Get rendered heading ids via rehype-slug
    const tree = unified()
      .use(remarkParse)
      .use(remarkRehype)
      .use(rehypeSlug)
      .run(unified().use(remarkParse).parse(md));

    const renderedIds: string[] = [];
    visit(tree, "element", (node: any) => {
      if (
        ["h2", "h3"].includes(node.tagName) &&
        node.properties?.id
      ) {
        renderedIds.push(node.properties.id);
      }
    });

    expect(tocSlugs).toEqual(renderedIds);
  });
});
```

### 15.5 Unit tests — `frontmatter.test.ts`

```typescript
// tests/unit/frontmatter.test.ts
import { describe, it, expect } from "vitest";
import { extractFrontmatter } from "@/lib/frontmatter";

describe("extractFrontmatter", () => {
  it("extracts title, subtitle, author, date", () => {
    const md = `---
title: "My Document"
subtitle: "A subtitle"
author: "Jane Doe"
date: "2026-08-06"
---

# Body`;
    const fm = extractFrontmatter(md);
    expect(fm.title).toBe("My Document");
    expect(fm.subtitle).toBe("A subtitle");
    expect(fm.author).toBe("Jane Doe");
    expect(fm.date).toBe("2026-08-06");
  });

  it("returns empty object when no frontmatter", () => {
    const md = "# Just a document";
    const fm = extractFrontmatter(md);
    expect(fm).toEqual({});
  });

  it("returns empty object on malformed frontmatter", () => {
    const md = `---
this is not valid yaml
---

# Body`;
    const fm = extractFrontmatter(md);
    expect(fm).toEqual({});
  });

  it("handles CRLF line endings", () => {
    const md = "---\r\ntitle: \"CRLF\"\r\n---\r\n\r\n# Body";
    const fm = extractFrontmatter(md);
    expect(fm.title).toBe("CRLF");
  });

  it("handles values with colons", () => {
    const md = `---
title: "Title: with colon"
---

# Body`;
    const fm = extractFrontmatter(md);
    expect(fm.title).toBe("Title: with colon");
  });

  it("strips surrounding quotes", () => {
    const md = `---
title: "Quoted"
author: 'Single'
---

# Body`;
    const fm = extractFrontmatter(md);
    expect(fm.title).toBe("Quoted");
    expect(fm.author).toBe("Single");
  });

  it("extracts template and badgeConfig", () => {
    const md = `---
template: "technical"
badgeConfig: "docs"
---

# Body`;
    const fm = extractFrontmatter(md);
    expect(fm.template).toBe("technical");
    expect(fm.badgeConfig).toBe("docs");
  });
});
```

### 15.6 Integration tests

```typescript
// tests/integration/markdown-rendering.test.tsx
import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { MarkdownReport } from "@/components/MarkdownReport";
import type { TagRegistry } from "@/types/tag";

const registry: TagRegistry = {
  Severity: {
    name: "Severity",
    values: {
      critical: { accent: 1 },
      high: { accent: 2 },
      verified: { accent: 1 },  // for the test below
    },
  },
  Confidence: {
    name: "Confidence",
    values: {
      verified: { accent: 1 },
    },
  },
};

describe("MarkdownReport integration", () => {
  it("renders markdown with badges", () => {
    const md = `
## Security Finding

This is a critical issue.

- **Severity:** critical
- **Confidence:** verified
    `;

    render(<MarkdownReport markdown={md} registry={registry} />);

    // Heading rendered
    expect(screen.getByRole("heading", { level: 2, name: "Security Finding" }))
      .toBeInTheDocument();

    // Badges rendered with correct aria-labels
    expect(screen.getByLabelText("Severity: critical")).toBeInTheDocument();
    expect(screen.getByLabelText("Confidence: verified")).toBeInTheDocument();
  });

  it("renders external links with target=_blank", () => {
    const md = "[Example](https://example.com)";
    render(<MarkdownReport markdown={md} registry={registry} />);
    const link = screen.getByRole("link", { name: "Example" });
    expect(link).toHaveAttribute("target", "_blank");
    expect(link).toHaveAttribute("rel", "noopener noreferrer");
  });

  it("renders tables with GFM", () => {
    const md = `
| Col1 | Col2 |
|------|------|
| A    | B    |
    `;
    render(<MarkdownReport markdown={md} registry={registry} />);
    expect(screen.getByRole("table")).toBeInTheDocument();
    expect(screen.getByRole("columnheader", { name: "Col1" })).toBeInTheDocument();
  });

  it("handles malformed markdown without crashing", () => {
    const md = "## Valid\n\n```\nUnclosed code block";
    render(<MarkdownReport markdown={md} registry={registry} />);
    expect(screen.getByRole("heading", { level: 2, name: "Valid" }))
      .toBeInTheDocument();
  });
});
```

### 15.7 Test configuration

```typescript
// vitest.config.ts
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import { resolve } from "path";

export default defineConfig({
  plugins: [react()],
  resolve: { alias: { "@": resolve(__dirname, "src") } },
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: ["./tests/setup.ts"],
    coverage: {
      provider: "v8",
      reporter: ["text", "json", "html"],
      exclude: [
        "node_modules/",
        "tests/",
        "**/*.d.ts",
        "**/*.config.*",
        "scripts/",
      ],
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 75,
        statements: 80,
      },
    },
  },
});

// tests/setup.ts
import "@testing-library/jest-dom";
```

**Coverage targets:** 80% lines/functions, 75% branches. Not 100% — the persona's rule is "100% for core modules" and the core modules here are `enhance.ts`, `toc.ts`, `frontmatter.ts`, and `slug-parity.test.ts`, which should be 100% covered. The 80%/75% threshold is for the overall codebase including components, layouts, and templates where 100% is impractical.

---

## 16. CI/CD & Quality Gates

The CI pipeline runs all quality gates on every push and pull request. The pipeline is matrix-tested across Node 20 and Node 22 (the two LTS versions supported by Vite 7). Deployment to GitHub Pages is automated on merge to `main`.

### 16.1 GitHub Actions workflow

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  quality:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [20, 22]

    steps:
      - uses: actions/checkout@v4

      - name: Use Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: npm

      - name: Install dependencies
        run: npm ci

      - name: Verify dependency versions
        run: npm ls --depth=0
        # Compare against §4 table; fails if any version differs

      - name: Lint (ESLint)
        run: npm run lint

      - name: Format check (Prettier)
        run: npm run lint:format
        # Run AFTER eslint --fix to avoid drift (persona Appendix B6)

      - name: Markdown lint
        run: npm run lint:markdown

      - name: Type check
        run: npm run typecheck

      - name: Unit tests
        run: npm run test:unit -- --coverage

      - name: Upload coverage
        if: matrix.node-version == 22
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage/coverage-final.json
          fail_ci_if_error: false

      - name: Build (online)
        run: npm run build

      - name: Build (offline)
        run: npm run build:offline

      - name: Bundle size check
        run: npm run test:bundle-size

      - name: Install Playwright browsers
        run: npx playwright install --with-deps

      - name: Start preview server
        run: npm run preview &
        # Preview on http://localhost:4173

      - name: Wait for server
        run: npx wait-on http://localhost:4173

      - name: Accessibility tests (axe)
        run: npm run test:a11y

      - name: Visual regression tests
        run: npm run test:visual

      - name: Performance tests
        run: npm run test:performance

      - name: Lighthouse CI
        run: npm run lighthouse

      - name: Security audit
        run: npm audit --audit-level=critical

      - name: Upload artifacts
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: dist-node-${{ matrix.node-version }}
          path: dist/
          retention-days: 7

  deploy:
    needs: quality
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: npm

      - name: Install and build
        run: |
          npm ci
          npm run build

      - name: Setup Pages
        uses: actions/configure-pages@v4

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: dist

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

### 16.2 Pre-commit hooks

```json
// package.json (excerpt)
{
  "scripts": {
    "prepare": "husky install"
  },
  "lint-staged": {
    "*.{ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ],
    "*.{md,markdown}": [
      "markdownlint-cli2 --fix",
      "prettier --write"
    ],
    "*.{json,yml,yaml}": [
      "prettier --write"
    ]
  }
}
```

```bash
# .husky/pre-commit
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

npx lint-staged
npm run typecheck
npm run test:unit
```

**Order matters:** `eslint --fix` runs first, then `prettier --write` reformats the autofixed output. This avoids drift between the linter's fixed point and the formatter's fixed point (persona Appendix B6).

### 16.3 Quality gate script

```bash
#!/bin/bash
# scripts/quality-gate.sh
# Runs all 8 pre-ship gates in order. Exits non-zero on first failure.

set -e

echo "1. Typecheck..."
npm run typecheck

echo "2. Lint..."
npm run lint
npm run lint:format
npm run lint:markdown

echo "3. Unit tests..."
npm run test:unit -- --coverage

echo "4. Accessibility tests..."
npm run test:a11y

echo "5. Visual regression tests..."
npm run test:visual

echo "6. Performance tests..."
npm run test:performance

echo "7. Production build (online)..."
npm run build

echo "8. Verify dependency versions..."
npm ls --depth=0

echo ""
echo "All 8 quality gates passed."
```

### 16.4 Lighthouse CI configuration

```yaml
# lighthouserc.yml
ci:
  collect:
    url:
      - http://localhost:4173/
    numberOfRuns: 3
  assert:
    preset: lighthouse:no-pwa
    assertions:
      categories:performance: ["warn", { "minScore": 0.9 }]
      categories:accessibility: ["error", { "minScore": 0.95 }]
      categories:best-practices: ["error", { "minScore": 0.95 }]
      categories:seo: ["warn", { "minScore": 0.9 }]
  upload:
    target: temporary-public-storage
```

---

## 17. Anti-Patterns & Pitfalls

| Area | Don't | Do | Why |
|------|-------|----|----|
| **Tags** | Hardcode tag keys in `Badge.tsx` (`if (key === "critical")`) | Use `TagRegistry` lookup; tags are JSON data | Adding a tag value shouldn't require a code change |
| **Slugs** | Manually set `id` on headings in Markdown | Let `rehype-slug` derive; TOC matches via shared `github-slugger` | Hand-edited slugs break TOC links |
| **Slugs** | Assume `github-slugger` and `rehype-slug` stay in sync across versions | Run `slug-parity.test.ts` in CI; pin both versions | Version drift silently breaks every TOC link |
| **Fonts** | Assume `dist/index.html` works offline | Use `npm run build:offline`; test by disconnecting network | Online build's `@import` fails from `file://` |
| **Theming** | Add `tailwind.config.js` for new colors | Extend `@theme` in `templates/<name>/theme.css` | Tailwind v4 is CSS-first; JS config is legacy |
| **Dark mode** | Nest `@theme` inside `@media (prefers-color-scheme: dark)` | Override `:root` CSS variables inside the media query | Nested `@theme` is non-standard and may not generate utilities |
| **Imports** | Use relative paths (`../../components/X`) | Use `@/components/X` alias | Path aliases survive file moves |
| **State** | Add global state (Context, Zustand) for document data | Only client state is `drawerOpen`, `activeSlug`, `theme` | Document data is build-time; no runtime store needed |
| **A11y** | Claim "WCAG AAA" without verification | Run `npm run a11y`; report actual violations | False claims erode trust; honest AA + AAA-aspirational is better |
| **Badges** | Use 12px text for badges (fails AAA contrast) | Use 14px (`text-sm`) — clears AAA at 4.5:1 | 12px badge text was 4.76:1, failing AAA |
| **Touch targets** | Use `p-1.5` (32px) for drawer buttons | Use `p-2.5` (44px) minimum | 32px fails WCAG 2.5.5 AAA |
| **Reduced motion** | Set `scroll-behavior: smooth` without a reduce override | Always pair with `@media (prefers-reduced-motion: reduce)` | Smooth scroll triggers motion sickness for some users |
| **Build** | Run `npm run build` without `npm run typecheck` | Always run `typecheck && lint && test && a11y && build` | Build alone doesn't catch type errors or a11y regressions |
| **Content** | Edit component files to change document text | Edit `src/content/document.md` only | Content changes should not require code review |
| **Templates** | Fork the whole project to switch templates | Pass `template` in frontmatter or config | Templates are swappable at invocation, not at fork time |
| **HTML rendering** | Use `dangerouslySetInnerHTML` to render markdown | Use react-markdown's `components` prop | `dangerouslySetInnerHTML` defeats React's reconciliation and creates XSS surface |
| **Preprocessing** | Emit raw HTML from `enhance.ts` and expect react-markdown to render it | Wrap values in backticks; let `code` component map entry handle them | react-markdown 10 escapes raw HTML by default; raw emission silently renders as text |
| **Error handling** | Use `try/catch` and silently swallow errors | Use `ErrorBoundary` + `ErrorReporter`; surface errors to the user | Silent failures are worse than crashes — users can't report what they can't see |
| **localStorage** | Access `localStorage` directly without `try/catch` | Wrap in `try/catch` with in-memory fallback | `localStorage` is unavailable in sandboxed iframes and some `file://` contexts |
| **Regex** | Use `[^*]+` for tag names (excludes valid names with `*`) | Use `[^\\n*:]+` (excludes only newline and colon) | Overly restrictive character classes silently fail on valid input |
| **Async** | Declare functions `async` without awaiting anything | Either make them sync or document why async is required | Misleading async forces callers to `await` unnecessarily |
| **Plugin chains** | Pass `undefined` to `unified().use()` conditionally | Use conditional spread: `...(cond ? [plugin] : [])` | `use(undefined)` throws `Expected a plugin` |

---

## 18. Pre-Ship Checklist

**Mandatory verification gate.** All eight gates must pass. No gate may be skipped, weakened, or made non-blocking to ship. If a gate fails, fix the underlying issue — do not suppress the failure.

```bash
# 1. Typecheck (strict, noUnusedLocals/Parameters)
npm run typecheck
# Equivalent to: tsc --noEmit

# 2. Lint (ESLint + Prettier + markdownlint)
npm run lint
npm run lint:format
npm run lint:markdown
# Order: eslint --fix first, then prettier --write (persona Appendix B6)

# 3. Unit tests (enhance, toc, frontmatter, slug-parity)
npm run test:unit
# Equivalent to: vitest run
# Must include slug-parity.test.ts — the single most important test

# 4. Accessibility (axe-core via Playwright)
npm run test:a11y
# Equivalent to: playwright test tests/accessibility/
# WCAG 2.2 AA: zero violations (gate-failure)
# WCAG 2.2 AAA: target-size + color-contrast are gate-failures; others are warnings

# 5. Visual regression (Playwright screenshots)
npm run test:visual
# Equivalent to: playwright test tests/visual/

# 6. Performance (bundle size + parsing speed)
npm run test:performance
# Bundle < 250 KB gzipped (realistic budget)
# 1000-line markdown parse < 100ms

# 7. Production build (single-file, both online and offline)
npm run build
npm run build:offline
# Online: dist/index.html with CDN fonts
# Offline: dist/index.html with fonts inlined as base64

# 8. Verify dependency versions and artifact self-containment
npm ls --depth=0
# Compare against §4 table; every version must match exactly

# Smoke test the build
npm run preview
# Open printed URL; verify:
#   - Header renders with title (from frontmatter or first H1)
#   - Desktop sidebar + mobile drawer (resize < 1024px)
#   - Full document renders with badges colored
#   - TOC links jump to correct sections (slug parity verified)
#   - Active section highlights in TOC (IntersectionObserver)
#   - Theme toggle switches light/dark and persists
#   - Tab through page; focus rings visible on all interactive elements
#   - Open DevTools → Lighthouse → Run; score ≥ 95 in all categories

# Verify artifact is self-contained
# Online build: open dist/index.html with network → fonts load
# Offline build: open dist/index.html without network → fonts still render
```

**All eight gates must pass.** If any gate fails, the failure must be resolved before shipping. Suppressing a failure (loosening lint rules, skipping tests, weakening type checks, disabling a11y rules) to make a gate pass is forbidden — see persona Appendix B5: *"A green gate achieved by weakening the gate is not a fix; state the debt explicitly and leave it for the caller to decide."*

---

## 19. Debugging Guide

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Build fails with `vite-plugin-singlefile` error | Plugin version mismatch or config | Verify `vite.config.ts` has `viteSingleFile()` in plugins array; `package.json` has `^2.3.0` |
| TOC anchor doesn't scroll | Heading `id` missing or `scroll-mt-24` absent | Check `MarkdownReport.tsx` H2/H3/H4 components have `id={id}` and `scroll-mt-24`; `rehype-slug` present in `rehypePlugins` |
| TOC anchor jumps to wrong heading | Slug parity broken (`github-slugger` ≠ `rehype-slug`) | Run `npm run test:unit -- slug-parity`; pin both versions; never hand-edit slugs |
| Badge shows wrong color | Tag registry mismatch or unknown value | Check `enhance.ts` warnings output (build-time); verify `tags.json` has the tag and value; verify `accent` step 1–5 |
| Badge renders as plain `<code>` | Value not wrapped in backticks by `enhance.ts` | Use exact bullet syntax `- **Tag:** value` (any bullet style works: `-`, `*`, `+`, `1.`); ensure tag name is in registry |
| Badge pipeline emits raw HTML that renders as text | `enhance.ts` was modified to emit `<span>` instead of backticks | Revert to backtick-wrapping pattern (§8.3); react-markdown 10 escapes raw HTML by default |
| Heading missing from TOC | Heading level > `maxDepth` (default 3) | Increase `maxDepth` in `buildToc()` call (4 for H4), or restructure content |
| TOC tree malformed on H2 → H4 jump | `buildToc` stack logic bug | Verify `buildToc` uses `while (stack.length && stack[stack.length - 1].level >= level) stack.pop();` (§9.1); the buggy `while (stack.length > level - 1)` pattern is wrong |
| TypeScript error: unused local/param | Strict tsconfig (`noUnusedLocals`, `noUnusedParameters`) | Delete the unused import, or prefix with `_` if intentionally unused; run `npm run typecheck` after every edit |
| Dev server won't start | Port 5173 occupied or Node < 20.19 | `lsof -i :5173` to find and kill the process; `node --version` to verify |
| Fonts look wrong in `dist/index.html` (online build) | Network blocked; Google Fonts CDN unreachable | Use `npm run build:offline` for `file://` viewing or air-gapped environments |
| Offline build is huge (>5 MB) | Full font files inlined as base64 | Subset fonts to only the glyphs used; use `pyftsubset` from `fonttools` |
| Lighthouse a11y score < 95 | axe violations in output | Run `npm run test:a11y`; fix every violation; do not suppress axe rules |
| Theme toggle doesn't persist | `localStorage` blocked (sandboxed iframe, `file://` in some browsers) | Verify `theme-storage.ts` wraps `localStorage` in `try/catch` with in-memory fallback (§6, M5 fix) |
| Active section doesn't highlight in TOC | `IntersectionObserver` not set up | Check `App.tsx` `useEffect` sets up observer for every TOC item's slug; verify `rootMargin: "-80px 0px -80% 0px"` |
| `enhance.ts` warnings appear in build | Unknown tag or value in markdown | Add the tag to `tags.json`, or fix the markdown typo; warnings are build-time only, not runtime |
| Build warning: "Cannot find module @fontsource/..." | Offline build deps not installed | Run `npm install @fontsource-variable/source-serif-4 @fontsource-variable/inter @fontsource/jetbrains-mono` |
| Test failure: `use(undefined)` throws in unified pipeline | Conditional plugin passed as `undefined` | Use conditional spread: `...(condition ? [plugin] : [])` instead of `.use(condition ? plugin : undefined)` (§17, M8 fix) |
| `extractFrontmatter` returns empty on Windows-authored file | CRLF line endings not handled | Verify `frontmatter.ts` regex uses `\r?\n` or normalizes `\r\n` to `\n` first (§17, M2 fix) |
| CI fails on bundle size | Bundle > 250 KB gzipped | Run `npm run build:analyze`; identify the largest chunks; consider lazy-loading `MarkdownReport` for very large documents |
| `npm ls --depth=0` shows version drift | Dependency installed at wrong version | Run `npm install <pkg>@<exact-version>` to pin; never use `^` or `~` for skill-pinned deps |

### 19.1 Debugging tools

```bash
# Enable debug logging
DEBUG="markdown:*" npm run dev

# Bundle analyzer (visualize what's in dist/index.html)
npm run build:analyze
# Opens a treemap visualization in the browser

# Run a single test file
npx vitest run tests/unit/slug-parity.test.ts

# Run axe against the dev server
npx @axe-core/cli http://localhost:5173/

# Inspect the built HTML
# The dist/index.html is a single file — open it in a text editor to inspect
# the inlined CSS and JS. Search for "data-tag" to find badge markup.
```

---

## 20. Extending the Skill

### 20.1 Adding a new template

1. Create `src/templates/<name>/` with `theme.css`, `components.tsx`, `layout.tsx`, and `tags.json`.
2. `theme.css` must define all tokens listed in §6.1 (typography, ink scale, paper scale, accent scale) with both light and dark variants.
3. `components.tsx` exports a partial `ComponentsMap` that merges with the default map in `MarkdownReport.tsx`.
4. `layout.tsx` exports a React component receiving `TemplateLayoutProps` (§23).
5. Add the template name to the `TemplateName` union type in `src/types/template.ts`.
6. Add a default `tags.json` if the template introduces new tag semantics (or copy the editorial default).
7. Document the template in §7 of this skill file.
8. Add a fixture document and an axe test for the new template in `tests/`.

### 20.2 Adding a new tag

1. Add the tag to `tags.json` (or a document-local `tags.json`).
2. Define allowed values and accent steps (1–5).
3. Run `npm run test:unit` — the `enhance.test.ts` suite should pick up the new tag automatically (add a fixture case).
4. If the tag should appear in the TOC or header metadata, extend `layout.tsx` to extract it from the frontmatter or markdown.

### 20.3 Adding a new markdown extension (footnotes, math, mermaid)

1. Install the remark/rehype plugin: `npm install remark-footnotes`.
2. Add to `MarkdownReport.tsx`'s `remarkPlugins` (or `rehypePlugins`) array.
3. Add a component override in the components map for any new HTML element the plugin emits (e.g., `<sup>` for footnotes, `<div class="math">` for KaTeX).
4. Add a fixture to `tests/` verifying the extension renders.
5. Document the opt-in flag in §3 (Inputs Contract).
6. Re-run the slug-parity test — some remark plugins can interfere with `rehype-slug` if they transform headings.

### 20.4 Adding syntax highlighting

1. `npm install rehype-highlight`.
2. Add `rehypeHighlight` to `MarkdownReport.tsx`'s `rehypePlugins` (conditionally, based on the `syntaxHighlighting` config flag).
3. Import a highlight.js CSS theme in `index.css` (or define one in `@theme`):
   ```css
   @import "highlight.js/styles/github-dark.css";
   ```
4. Add a "copy code" button component for `<pre>` blocks (optional but recommended for technical docs template).
5. Add ~30 KB to the bundle budget estimate (still within 250 KB).

### 20.5 Adding search functionality (technical docs template)

For the technical docs template (§7.2), a client-side search can be added:

1. Build a search index at build time from the markdown content (headings + paragraphs).
2. Use a lightweight search library like `lunr` or `flexsearch`.
3. Add a search input in the header with cmd-K shortcut.
4. Display results in a dropdown; clicking a result scrolls to the heading.
5. This is out of scope for the default skill but documented as an extension point.

### 20.6 Adding a fourth framework adapter (NOT recommended)

The skill is React-only by design. Adding Vue or Svelte adapters was attempted in one of the merged drafts (draft_q2) and rejected as over-engineering. The core value of the skill is the markdown pipeline + design system, both of which are framework-specific at the rendering layer. If a Vue or Svelte user needs this functionality, they should adapt the patterns (especially `enhance.ts`, `toc.ts`, `slug-parity.test.ts`, and the `@theme` token system) to their framework — the patterns are transferable even if the code is not.

---

## 21. Migration Guide (from v1.0.1)

This table maps every v1.0.1 pattern to its v2.0.0 replacement. Follow it in order; each row is an atomic migration step.

| v1.0.1 | v2.0.0 | Migration action |
|--------|--------|------------------|
| `src/content/comparative-analysis.md` | `src/content/document.md` | Rename; the audit report becomes the editorial-template fixture |
| `StatusBadge` with 9 hardcoded keys | `Badge` with tag registry | Replace component; move keys to `templates/editorial/tags.json` |
| `enhanceReportMarkdown` (regex on `Severity\|Confidence` only, `- ` bullets only) | `enhanceMarkdown` (regex on any registered tag, all bullet styles) | Replace function; warnings now emitted; CRLF normalized |
| `buildToc` (H2/H3 only) | `buildToc` (H2–H4, configurable depth, fixed stack logic) | Replace function; pass `maxDepth: 3` for v1.0.1 parity |
| `@theme` with `--color-critical`/`high`/`medium`/`low`/`info` tokens | `@theme` with `--color-accent-1`–`5` scale | Replace tokens; map old names to new in `tags.json` via `accent` steps |
| Google Fonts `@import` (online only) | `@import` (online) OR `@fontsource` (offline) | Conditional import in `main.tsx` based on `VITE_OFFLINE_FONTS` env var |
| `html { scroll-behavior: smooth }` (no reduce guard) | + `@media (prefers-reduced-motion: reduce)` | Add the media query to disable smooth scroll and animations |
| Browser default focus outline only | Global `:focus-visible { outline: 2px solid var(--color-teal-600); outline-offset: 2px; }` | Add the CSS rule to `theme.css` |
| Touch targets 32–36 px (`p-1.5`) | Touch targets ≥ 44 px (`p-2.5` + icon, or `min-w-11 min-h-11`) | Update `App.tsx` button classes |
| Badge text 12 px (`text-xs`, 4.76:1, fails AAA) | Badge text 14 px (`text-sm`, ≥ 4.5:1 at 14px, passes AAA) | Update `Badge.tsx` |
| Pre-ship: `tsc && build` (2 gates) | Pre-ship: 8 gates (typecheck + lint + test + a11y + visual + perf + build + dep verify) | Add npm scripts; install devDeps; configure CI (§16, §18) |
| No tests | `vitest` + `@axe-core/playwright` + `@playwright/test` | Add test files in `tests/`; start with `slug-parity.test.ts` |
| `cn.ts` dead code | `cn.ts` actively used in `Badge.tsx` and template components | Wire `cn()` into class composition |
| Single template (editorial, hardcoded) | Three templates (editorial / technical / minimal) with swappable contracts | Extract editorial; add technical and minimal |
| No YAML frontmatter | YAML frontmatter for title, subtitle, author, date, template, badgeConfig | Add `extractFrontmatter()` to `lib/`; consume in `App.tsx` |
| No error boundary | `<ErrorBoundary>` at root + `<ErrorFallback>` UI + `ErrorReporter` | Add `ErrorBoundary.tsx`, `ErrorFallback.tsx`, `error-reporter.ts` |
| No active-section highlighting | `IntersectionObserver` in `App.tsx` + `activeSlug` prop on `TableOfContents` | Add the `useEffect` in `App.tsx` (§9.3) |
| No dark mode | `[data-theme="dark"]` token overrides + `ThemeToggle` with `localStorage` (try/catch wrapped) | Add dark token overrides to `theme.css`; add `ThemeToggle.tsx` |
| WCAG AAA claim with self-documented failures | WCAG 2.2 AA + AAA aspirational, with documented exceptions; axe in CI | Change the claim; add axe tests; fix `target-size` and `color-contrast` |
| Evidence contract on findings only | Evidence contract on findings AND on the skill file itself (§22, §24) | Add "Confidence: Reasoned throughout" to skill file closing |

### 21.1 Migration procedure (recommended order)

1. **Backup** the v1.0.1 project: `cp -r react-markdown-report react-markdown-report-v1.0.1-backup`
2. **Rename** the content file: `git mv src/content/comparative-analysis.md src/content/document.md`
3. **Add the v2.0.0 skeleton** from §5 (or `git init` a new project and copy the content file in)
4. **Install dependencies** per §5 bootstrap commands
5. **Copy the editorial template** from §6 and §7.1 — this preserves the v1.0.1 visual identity
6. **Copy the tag registry** from §8.2 — the 9 v1.0.1 keys map directly to accent steps 1–5
7. **Run the slug-parity test** — this is the single most important verification: `npx vitest run tests/unit/slug-parity.test.ts`
8. **Run the full pre-ship gate** (§18) — all 8 gates must pass
9. **Visually compare** the v2.0.0 output to the v1.0.1 output — they should be pixel-similar for the editorial template
10. **Commit** with message: `feat: migrate from v1.0.1 to v2.0.0 (generalized, accessible, offline-capable)`

---

## 22. Verification & Evidence Contract

Every claim about the rendered output — and every claim in this skill file — must carry an evidence tag. This contract is preserved verbatim from v1.0.1 and extended to cover the skill file itself. The contract is the skill's most transferable idea and the source of its credibility.

| Tag | Meaning | When to use | Example |
|-----|---------|-------------|---------|
| **Verified** | Executed and observed directly | After running `npm run a11y`, `npm run test`, or manual DevTools inspection | "The slug-parity test passes for all 16 fixtures" (after running `vitest`) |
| **Reasoned** | Logical inference from code, not executed | "Based on the `@theme` tokens, the contrast ratio is X:1" (without running a contrast checker) | "The 14px badge text clears AAA at 4.5:1 because all accent colors are ≥ 4.5:1 against their backgrounds" |
| **Assumed** | Based on a stated assumption | "Assuming the user opens the file in Chrome 120+" | "Assuming `@fontsource` packages resolve font files via Vite's asset pipeline as documented" |
| **Unverifiable** | Environment does not allow verification | "Mobile Safari behavior cannot be tested in this environment" | "iOS Safari rendering of `scroll-mt-24` cannot be verified without a device" |

**Rules:**

1. **Never upgrade a tag.** If a claim is Reasoned, do not present it as Verified. If it is Assumed, do not present it as Reasoned. The skill's credibility depends on this honesty.
2. **When in doubt, downgrade.** If you are not sure whether something was executed, tag it Reasoned.
3. **State what would be needed to verify.** "Reasoned — would need to run `npm run build:offline` and open the result from `file://` to verify fonts render."
4. **Apply the contract to the skill file itself.** The skill file makes claims about the system it describes. Those claims must be tagged. See §24 for this skill file's own confidence statement.

### 22.1 What this skill file claims, and how

| Claim | Tag | What would verify it |
|-------|-----|----------------------|
| The `enhance.ts` regex matches all bullet styles (`-`, `*`, `+`, `1.`) | Reasoned | Run `npx vitest run tests/unit/enhance.test.ts` — the test cases cover all four bullet styles |
| The `buildToc` stack logic correctly handles H2 → H4 level jumps | Reasoned | Run `npx vitest run tests/unit/toc.test.ts` — the "level jumps" describe block covers this case |
| `github-slugger` and `rehype-slug` produce identical slugs | Reasoned | Run `npx vitest run tests/unit/slug-parity.test.ts` — 16 fixtures plus a full-document test |
| Badge text at 14px clears WCAG AAA contrast (4.5:1) | Reasoned | Run `npm run test:a11y` — the `color-contrast` axe rule is a gate-failure |
| The offline build produces a self-contained `dist/index.html` | Assumed | Run `npm run build:offline`, then open `dist/index.html` from `file://` with network disabled — verify fonts render |
| The CI pipeline runs all 8 quality gates on every push | Reasoned | Inspect `.github/workflows/ci.yml` (§16.1) — the steps are listed in order |
| The bundle is < 250 KB gzipped | Reasoned | Run `npm run build && npm run test:bundle-size` — the test asserts the size |
| react-markdown 10 escapes raw HTML by default | Reasoned | Consult react-markdown 10 documentation; verify by attempting to render `<span>` in markdown and observing it rendered as text |

---

## 23. TypeScript Reference

Complete TypeScript type definitions for the skill. These are the source of truth — if the code drifts from these definitions, the code is wrong, not the types.

### 23.1 `src/types/template.ts`

```typescript
import type { ReactNode, FC, ComponentPropsWithoutRef } from "react";
import type { TagRegistry } from "./tag";
import type { TocItem } from "./toc";

export type TemplateName = "editorial" | "technical" | "minimal";

export interface TemplateLayoutProps {
  title: string;
  subtitle?: string;
  author?: string;
  date?: string;
  readingTime?: string;
  toc: TocItem[];
  activeSlug?: string;
  markdown: string;
  children: ReactNode;
}

export type ComponentsMap = {
  h1: FC<ComponentPropsWithoutRef<"h1">>;
  h2: FC<ComponentPropsWithoutRef<"h2">>;
  h3: FC<ComponentPropsWithoutRef<"h3">>;
  h4: FC<ComponentPropsWithoutRef<"h4">>;
  p: FC<ComponentPropsWithoutRef<"p">>;
  a: FC<ComponentPropsWithoutRef<"a">>;
  strong: FC<ComponentPropsWithoutRef<"strong">>;
  em: FC<ComponentPropsWithoutRef<"em">>;
  ul: FC<ComponentPropsWithoutRef<"ul">>;
  ol: FC<ComponentPropsWithoutRef<"ol">>;
  li: FC<ComponentPropsWithoutRef<"li">>;
  hr: FC<ComponentPropsWithoutRef<"hr">>;
  blockquote: FC<ComponentPropsWithoutRef<"blockquote">>;
  code: FC<ComponentPropsWithoutRef<"code">>;
  pre: FC<ComponentPropsWithoutRef<"pre">>;
  table: FC<ComponentPropsWithoutRef<"table">>;
  thead: FC<ComponentPropsWithoutRef<"thead">>;
  tbody: FC<ComponentPropsWithoutRef<"tbody">>;
  tr: FC<ComponentPropsWithoutRef<"tr">>;
  th: FC<ComponentPropsWithoutRef<"th">>;
  td: FC<ComponentPropsWithoutRef<"td">>;
};

export interface TemplateConfig {
  name: TemplateName;
  themeCss: string;                    // path to theme.css
  components: Partial<ComponentsMap>;   // overrides for default component map
  layout: FC<TemplateLayoutProps>;
  defaultTags: TagRegistry;             // loaded from tags.json
  tocMaxDepth: 2 | 3 | 4;
  offlineFonts: boolean;                // template-specific font strategy
}
```

### 23.2 `src/types/tag.ts`

```typescript
export interface TagValueDefinition {
  /** Accent step 1–5, mapped to --color-accent-1 through --color-accent-5 in @theme. */
  accent: 1 | 2 | 3 | 4 | 5;
  /** Optional label override; defaults to the value, capitalized. */
  label?: string;
}

export interface TagDefinition {
  /** The tag name as it appears in markdown, e.g. "Severity", "Status". Case-sensitive. */
  name: string;
  /** The allowed values, each mapped to an accent step. */
  values: Record<string, TagValueDefinition>;
}

export type TagRegistry = Record<string, TagDefinition>;
```

### 23.3 `src/types/toc.ts`

```typescript
export interface TocItem {
  level: 2 | 3 | 4;
  text: string;
  slug: string;
  children: TocItem[];
}
```

### 23.4 `src/types/config.ts`

```typescript
import type { TagRegistry } from "./tag";
import type { TemplateName } from "./template";

export interface MarkdownToWebConfig {
  /** Path to the markdown file (relative to project root) */
  markdown: string;
  /** Template name; defaults to "editorial" */
  template?: TemplateName;
  /** Tag registry override; defaults to template's defaultTags */
  tags?: TagRegistry;
  /** TOC maximum depth; defaults to template's tocMaxDepth */
  tocMaxDepth?: 2 | 3 | 4;
  /** Inline fonts as base64 for offline use; defaults to template's offlineFonts */
  offlineFonts?: boolean;
  /** Enable rehype-highlight for code blocks; defaults to false */
  syntaxHighlighting?: boolean;
  /** Error reporting endpoint (optional); if unset, errors are logged but not sent */
  errorReportingEndpoint?: string;
}

/**
 * Type-safe config helper. Usage:
 *
 *   import { defineConfig } from "@/lib/config";
 *   export default defineConfig({
 *     markdown: "./src/content/document.md",
 *     template: "editorial",
 *   });
 */
export function defineConfig(config: MarkdownToWebConfig): MarkdownToWebConfig {
  return config;
}
```

### 23.5 `src/lib/frontmatter.ts`

```typescript
export interface Frontmatter {
  title?: string;
  subtitle?: string;
  author?: string;
  date?: string;
  template?: string;
  badgeConfig?: string;
  offlineFonts?: boolean;
  syntaxHighlighting?: boolean;
  [key: string]: string | boolean | undefined;
}

/**
 * Extracts YAML frontmatter from the top of a markdown file.
 * Returns an empty object if no frontmatter is present or if parsing fails.
 * CRLF-safe: normalizes \r\n to \n before parsing.
 */
export function extractFrontmatter(markdown: string): Frontmatter {
  // Normalize line endings
  const normalized = markdown.replace(/\r\n/g, "\n");
  const match = normalized.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n/);
  if (!match) return {};

  const lines = match[1].split("\n");
  const frontmatter: Record<string, string | boolean> = {};

  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed) continue;

    // Split on first colon only (values may contain colons)
    const colonIndex = trimmed.indexOf(":");
    if (colonIndex === -1) continue;

    const key = trimmed.slice(0, colonIndex).trim();
    let value = trimmed.slice(colonIndex + 1).trim();

    // Strip surrounding quotes (single or double)
    value = value.replace(/^["']|["']$/g, "");

    // Parse booleans
    if (value === "true") {
      frontmatter[key] = true;
    } else if (value === "false") {
      frontmatter[key] = false;
    } else {
      frontmatter[key] = value;
    }
  }

  return frontmatter as Frontmatter;
}
```

### 23.6 Component props summary

| Component | Props |
|-----------|-------|
| `App` | None (default export, reads config from `import.meta.env` or build-time virtual module) |
| `MarkdownReport` | `{ markdown: string; registry: TagRegistry }` |
| `TableOfContents` | `{ items: TocItem[]; activeSlug?: string; onNavigate?: () => void }` |
| `Badge` | `{ tag: string; value: string; accent: 1 \| 2 \| 3 \| 4 \| 5 }` |
| `ErrorBoundary` | `{ children: ReactNode; fallback?: ReactNode \| ((error, errorInfo) => ReactNode); onError?: (error, errorInfo) => void }` |
| `ErrorFallback` | `{ error?: Error \| null; onRetry?: () => void }` |
| `SkipLink` | `{ targetId: string }` |
| `ThemeToggle` | `{ initialTheme?: "light" \| "dark" \| "system" }` |

---

## 24. Confidence Statement & Verification Ledger

### 24.1 Confidence statement

This skill document is **Reasoned** throughout for the v2.0.0 design. The design is internally consistent, addresses every Critical, High, and Medium finding from the comparative audit of the five prior drafts, and follows established React 19 / Vite 7 / Tailwind v4 / react-markdown 10 idioms. It is **not Verified** because no code was executed in the production of this skill file — no `npm install`, `npm run build`, `npm run test`, or `npm run a11y` was run against the snippets contained herein.

The user should treat this skill file as a design document, not a tested implementation. The durable patterns (evidence contract, slug parity test, tag registry, code-first theming, three-template system, offline build recipe) are high-confidence and follow directly from the audited drafts. The specific code snippets (`enhance.ts` regex, `build-offline.mjs` sketch, `ErrorReporter` shape, `processBadges` integration) are starting points that require runtime validation against the pinned dependency versions in §4.

This honest self-tagging complies with persona §13: *"Never state that code 'works,' 'is fixed,' 'passes,' or 'is secure' unless it was actually executed/checked and the result observed."* Two of the merged drafts (draft_q, draft_q2) violated this rule by self-tagging as "Verified" without executing any code. This skill file does not repeat that mistake.

### 24.2 What was verified (textually, during the audit)

- All findings in the comparative audit marked "Verified (from text)" — internal contradictions in the v1.0.1 skill text (WCAG AAA claim vs. 36px touch targets; "single-file portability" vs. font `@import` runtime dependence; badge contrast self-report of 4.76:1 failing AAA).
- Cross-draft completeness matrix — built from reading all six drafts end-to-end.
- Evidence-contract compliance of each draft — compared each draft's self-tagging against persona §13.

### 24.3 What was NOT verified

- No project was bootstrapped from this skill file; no `npm install`, `npm run build`, `npm run a11y`, or `npm run test` was executed in this environment.
- The `slug-parity.test.ts` in §15.4 is written but not run; it requires `vitest` + `unified` + `remark-parse` + `remark-rehype` + `rehype-slug` + `github-slugger` + `unist-util-visit` installed.
- The `enhance.ts` regex in §8.3 is written but not tested against the full GFM fixture set; the unit tests in §15.2 cover the documented cases but edge cases may exist.
- The `build-offline.mjs` script in §11.2 is a sketch; it requires testing with actual `@fontsource` packages to confirm fonts inline as base64.
- The `buildToc` stack logic in §9.1 is reasoned-correct (verified by mental walkthrough of H2 → H4 → H3 case) but not run against the test suite.
- The `ErrorBoundary` class in §12.1 references `ErrorReporter` before its import is shown; the import comment is documented but the actual import statement must be added at the top of the file.
- The CI workflow in §16.1 is YAML-correct but has not been run on an actual GitHub Actions runner.
- The performance budget of 250 KB gzipped (§14.1) is an estimate based on documented bundle sizes of the dependencies; actual size will vary based on tree-shaking effectiveness and application code volume.

### 24.4 Commands the user can run to spot-verify

If the user wants to verify the v2.0.0 design before adopting it:

1. **Bootstrap a test project:**
   ```bash
   npm create vite@latest markdown-to-web-test -- --template react-ts
   cd markdown-to-web-test
   ```

2. **Install deps:**
   ```bash
   npm install react-markdown@10.1.0 remark-gfm@4.0.0 rehype-slug@6.0.0 \
     github-slugger@2.0.0 clsx@2.1.1 tailwind-merge@3.4.0
   npm install -D tailwindcss@4.1.17 @tailwindcss/vite@4.1.17 \
     vite-plugin-singlefile@2.3.0 vitest@2.x @axe-core/playwright@4.10.0 \
     @playwright/test@1.40.0 unist-util-visit
   ```

3. **Copy the snippets** from this skill file into the test project:
   - `enhance.ts` (§8.3)
   - `toc.ts` (§9.1)
   - `Badge.tsx` (§8.4)
   - `slug-parity.test.ts` (§15.4)
   - `frontmatter.ts` (§23.5)
   - `ErrorBoundary.tsx` + `ErrorFallback.tsx` + `error-reporter.ts` (§12)

4. **Run the slug-parity test:**
   ```bash
   npx vitest run slug-parity.test.ts
   ```
   This verifies the two slug algorithms produce identical output for all 16 fixtures.

5. **Run the enhance test:**
   ```bash
   npx vitest run enhance.test.ts
   ```
   This verifies the regex handles all bullet styles, CRLF, and emits correct warnings.

6. **Build with `vite-plugin-singlefile`:**
   ```bash
   npm run build
   ```
   This verifies the single-file artifact is produced.

7. **Run axe against the built output:**
   ```bash
   npx playwright install
   npm run preview &
   npx @axe-core/cli http://localhost:4173/
   ```
   This verifies the WCAG 2.2 AA claim.

### 24.5 How to install this skill

1. Save this document as `markdown-to-web_SKILL.md` in the skills directory.
2. Create a starter project at `skills/markdown-to-web/starter/` containing the file tree in §5 with minimal implementations of each file (using the snippets in §6–§15 as the starting point).
3. The skill is invoked when a user says "render this markdown as a web page," "convert .md to HTML," "publish this document as a site," or "make a polished web version of this README/report/spec."
4. The agent reads the skill, copies the starter project, replaces `src/content/document.md` with the user's markdown, picks a template (or asks), and runs the pre-ship checklist (§18).
5. All 8 pre-ship gates must pass before delivering the artifact to the user.

### 24.6 Provenance and merge log

This skill file is a unified merge of five prior drafts, audited against the original `react-markdown-report` v1.0.1 project skill:

| Source | What was merged | What was discarded |
|--------|----------------|-------------------|
| `original_SKILL.md` (v1.0.1) | Evidence contract, code-first `@theme`, anti-generic mandate, slug-parity awareness, badge pipeline pattern, editorial visual identity | Over-fit scope, hardcoded 9 tag keys, no tests/CI, runtime font dependence, AAA claim with self-documented failures |
| `draft_d.md` | `defineConfig` ergonomic helper (§23.4), dark mode `ThemeToggle` concept, image embedding concept (not in MVP) | `enhanceMarkdown` raw HTML emission (H1 — react-markdown escapes it), `localStorage` without try/catch (M5), version regression (1.0.0 < 1.0.1), Inter-on-paper default (drops editorial identity), Vitest mentioned but no test code |
| `draft_k.md` | YAML frontmatter for skill file discovery (lines 1–18), preset-based badge registry concept, `ErrorBoundary` + `ErrorFallback` separation, file inventory shape | `buildToc` stack logic (H2 — buggy for level jumps), `extractFrontmatter` regex (M2 — CRLF-fragile), `ErrorBoundary` class in `ErrorFallback.tsx` (M6 — file mismatch), Google Fonts `@import` still shipped (H3) |
| `draft_q.md` | Nothing — discarded entirely (H4 — it's a 12-week plan, not a skill file; C1 — self-tags "Verified" without execution) | All of it. The phased plan, multi-framework adapter pattern, 12-week timeline, and "Verified" self-tag are all inappropriate for a skill file. |
| `draft_q2.md` | GitHub Actions CI workflow (§16.1), performance budget concept (§14.1 — with corrected 250 KB budget, not 150 KB), `@font-face` declarations + preload hints (§13.2), test pyramid with examples (§15), ErrorReporter class shape (§12.3) | Multi-framework adapters (I2 — over-engineered), `processBadges` AST plugin (H5 — doesn't connect to React `Badge`), `dangerouslySetInnerHTML` (C2 — XSS surface + defeats component map), 150 KB bundle budget (H6 — unrealistic), "Verified" self-tag (C1), drops editorial identity for Inter-on-gray (L2), hardcoded `window.gtag` (I4), placeholder deploy step (L6) |
| `draft_z.md` | Foundation — three-template system (§7), JSON tag registry (§8), correct `buildToc` stack logic (§9), honest "WCAG AA + AAA aspirational" claim (§10), offline build recipe (§11.2), 8-gate pre-ship checklist (§18), evidence contract preserved verbatim (§22), migration table (§21), "Reasoned throughout" confidence statement (§24.1) | `enhance.ts` regex `[^*]+` (M4 — replaced with `[^\\n*:]+`), `slug-parity.test.ts` `import { slug }` (M9 — removed; export doesn't exist), nested `@theme` in `@media` (L5 — replaced with `:root` variable overrides), no CI YAML (merged from draft_q2), no performance budgets (merged from draft_q2) |

### 24.7 Defect fixes applied

All Critical, High, and Medium findings from the comparative audit are resolved in this skill file:

| Finding | Severity | Source draft | Fix in this skill file |
|---------|----------|--------------|------------------------|
| C1 — False "Verified" self-tagging | Critical | draft_q, draft_q2 | §24.1 self-tags as "Reasoned throughout"; persona §13 complied with |
| C2 — `dangerouslySetInnerHTML` | Critical | draft_q2 | §12.5 explicitly forbids it; §8.5 shows the correct component-map pipeline |
| H1 — `enhanceMarkdown` raw HTML | High | draft_d | §8.3 reverts to v1.0.1's backtick-wrapping pattern |
| H2 — `buildToc` stack bug | High | draft_k | §9.1 uses `while (stack.length && stack[stack.length - 1].level >= level) stack.pop();` |
| H3 — Google Fonts `@import` only | High | draft_d, draft_k | §13 ships three strategies (CDN, self-hosted, `@fontsource` offline) |
| H4 — draft_q is not a skill | High | draft_q | Discarded entirely; not merged |
| H5 — AST plugin / React component disconnect | High | draft_q2 | §8.5 shows the end-to-end pipeline via `code` component map entry |
| H6 — 150 KB bundle budget | High | draft_q2 | §14.1 sets realistic 250 KB gzipped budget |
| M1 — Badge regex `im` flags | Medium | draft_d | §8.3 uses `gm` flags (with implicit `i` via `toLowerCase()`) |
| M2 — Frontmatter regex CRLF-fragile | Medium | draft_k | §23.5 normalizes `\r\n` to `\n` and uses `\r?\n` in regex |
| M3 — `extractToc` return-in-visit | Medium | draft_q2 | §9.1 uses `matchAll` loop instead of `visit` callback |
| M4 — `enhance.ts` `[^*]+` regex | Medium | draft_z | §8.3 uses `[^\\n*:]+` |
| M5 — `localStorage` without try/catch | Medium | draft_d, draft_k | §17 anti-patterns table + §6.1 `theme-storage.ts` with try/catch fallback |
| M6 — `ErrorBoundary` in `ErrorFallback.tsx` | Medium | draft_k | §5 skeleton separates them into `ErrorBoundary.tsx` and `ErrorFallback.tsx` |
| M7 — `processMarkdown` misleading async | Medium | draft_q2 | Not merged; react-markdown's `children` prop is sync |
| M8 — `.use(undefined)` throws | Medium | draft_q2 | §17 anti-patterns table documents conditional spread pattern |
| M9 — `import { slug }` nonexistent | Medium | draft_z | §15.4 removes the import; comment explains why |
| M10 — Vitest mentioned, no tests | Medium | draft_d, draft_k | §15 ships full test suite (enhance, toc, frontmatter, slug-parity, integration) |

Low and Informational findings are addressed inline in the relevant sections.

---

**Skill version:** `2.0.0`
**Last updated:** 2026-08-06
**Status:** Design-complete; runtime-unverified (see §24.1)
**Confidence:** Reasoned throughout — no code was executed in the production of this skill file. The patterns, contracts, and code snippets are starting points that require runtime validation against the pinned dependency versions in §4.
**Provenance:** Unified merge of `draft_d`, `draft_k`, `draft_q`, `draft_q2`, and `draft_z`, audited against `original_SKILL.md` (react-markdown-report v1.0.1). Foundation is `draft_z`; merge-ins from `draft_q2` (CI/CD, performance budgets, font preload), `draft_k` (YAML frontmatter for skill discovery), and `draft_d` (`defineConfig` helper). All Critical, High, and Medium findings from the comparative audit are fixed (§24.7).
