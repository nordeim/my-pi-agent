## Part 2 — `markdown-to-web` v4.0.0 Unified Skill Specification

> Every section in Part 2 cross-references its originating Part 1 finding. Where a
> design decision is *new* (no originating finding), it is tagged **[New in v4.0.0]**
> and justified inline. Every non-trivial claim carries a confidence tag
> (Verified / Reasoned / Assumed) per the evidence contract in §21.

---

### §1 Identity & Design Philosophy

**One-sentence description:** A zero-backend React application that renders any Markdown document as a polished, navigable, single-file web page, where the document's structure drives the UI, a template drives the look, and registered inline annotations render as semantic badges. *(Generalizes Finding 1.1's hardcoded report identity.)*

**Design thesis:** *Content is data; rendering is configuration.* The Markdown file is the input. The template chooses the look. The tag registry chooses which inline annotations become badges. The build produces one self-contained `dist/index.html` that runs anywhere a browser can open a file — online or offline.

**Core tenets:**

1. **Content is sovereign.** The markdown file determines structure. The renderer never invents content. Editing markdown never requires code changes.
2. **One rendering pipeline.** `react-markdown` + components map. No `dangerouslySetInnerHTML`, no HTML-string serialization, no raw-HTML injection into the markdown source *(closes Finding 21.3 — rejects draft_d2's dual-pipeline ambiguity)*.
3. **Tags are registered, not hardcoded.** Badges are data in a registry; the resolver is generic; value collisions fail fast at load *(fixes Findings 7.1 and 21.6)*.
4. **Single-file portability, honestly stated.** JS/CSS are inlined; fonts are a runtime dependency by default, with an opt-in offline build *(fixes Finding 3.2)*.
5. **Accessibility is gated, not claimed.** Conformance claim: **WCAG 2.2 AA, enforced by an axe gate; AAA where feasible, with enumerated exceptions (§10.3).** This document never claims AAA wholesale *(fixes Finding 8.1)*.
6. **No generic UI (per template).** The editorial template uses bespoke editorial design. Other templates may choose a different register — the anti-generic mandate applies per template, not globally *(fixes Finding 1.2)*.

**Anti-generic mandate (editorial template, explicitly rejected):** purple gradients on white; predictable card-grid layouts with left-border accents; generic "Inter + gray-50" neutrality; hero sections with centered H1 + paragraph + CTA; any component droppable into a different project without visual friction.

**[New in v4.0.0] Multi-framework adapters are explicitly rejected.** v4.0.0 is React-only. Vue and Svelte adapters (per draft_q2) are out of scope; no user has requested them, and the skill's trigger surface ("render markdown as web page") expects React in 100% of observed invocations. Adding adapters triples scope without user value. Documented as a non-goal.

### §2 When to Use / When Not To

**Use this skill when:**

- The user provides a Markdown file (`.md`) and asks for a "web version," "HTML rendering," "polished page," or "publishable site."
- The document is long-form (1,000–50,000 words) and benefits from a Table of Contents.
- The document contains structured annotations (`**Severity:** critical`, `**Status:** done`) that should render as visual badges.
- The artifact must run offline or from `file://`.
- Accessibility conformance (AA minimum, AAA aspirational) is a requirement.
- The user wants a single self-contained HTML file with no external runtime dependencies.

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

**Template selection guide:**

| If the document is… | Use template | Why |
|---------------------|--------------|-----|
| Audit report, essay, comparative analysis, design critique | `editorial` (default) | Long-form reading; sticky TOC; bespoke typography |
| API reference, technical spec, RFC, developer guide | `technical` | Three-column layout; code blocks first-class; cool, utilitarian palette |
| Manuscript, legal document, printable report, archival content | `minimal` | Single column; print CSS; no chrome; system fonts |

If unsure, start with `editorial`. The build is identical across templates — switching is a one-flag change, not a fork.

### §3 Inputs Contract

The skill accepts the following inputs. All except the Markdown file are optional with sensible defaults.

| Input | Required | Format | Default | Notes |
|-------|----------|--------|---------|-------|
| Markdown file | Yes | `.md`, UTF-8 | — | GFM extensions supported: tables, strikethrough, task lists, autolinks |
| Template | No | `editorial` \| `technical` \| `minimal` | `editorial` | See §7 |
| Tag registry | No | TS module or JSON | Template's default | See §8 |
| Frontmatter | No | flat `key: value` YAML | — | title/subtitle/author/date/template; §3.4 |
| Theme override | No | Partial Layer-1 variables | None | Merges with template's `:root` tokens |
| Offline fonts | No | build flag | `false` | When `true`, inlines fonts as base64 (§11.3) |
| Syntax highlighting | No | Boolean | `false` | When `true`, enables `rehype-highlight` |

**Markdown features supported:**

- Headings H1–H6 (TOC indexes H2–H4 by default; configurable `maxDepth: 2 | 3 | 4`)
- Paragraphs, bold, italic, strikethrough
- Inline code, fenced code blocks (with language class for syntax highlighting — opt-in via §19.4)
- Blockquotes
- Ordered/unordered lists, task lists
- Tables (GFM)
- Links (external links get `target="_blank" rel="noopener noreferrer"` automatically)
- Horizontal rules
- Inline images (with the §11.8 caveat — local images need `src/assets/` placement)
- YAML frontmatter (parsed for `title`, `subtitle`, `author`, `date`, `template`; remaining keys ignored)

**Markdown features NOT supported (out of scope):**

- Footnotes (`[^1]`) — add via `remark-footnotes` if a template needs it (§19.3)
- Math (`$...$`) — add via `remark-math` + `rehype-katex` if a template needs it (§19.3)
- Mermaid code blocks — add via `rehype-mermaid` if a template needs it (§19.3)
- Setext headings (`Title\n=====`) in TOC — invisible to the line-based extractor but real to `rehype-slug`; content convention is ATX headings only (§9.4)
- Raw HTML pass-through — by default, react-markdown escapes raw HTML. If a template explicitly enables `rehype-raw`, it MUST be paired with `rehype-sanitize` and the security implications documented.
- Multi-document sets — this skill renders one document into one HTML file.

**Explicitly out of scope:** SSR/API routes/databases, slide decks, PDF output, interactive code execution, documents under ~500 words (render inline instead).

#### 3.1 Frontmatter schema

```yaml
---
title: "Document Title"           # overrides first H1
subtitle: "Optional subtitle"     # renders below title in hero
author: "Author Name"             # renders in meta line
date: "2026-08-06"                # renders in meta line, ISO 8601
template: "editorial"             # editorial | technical | minimal
---
```

**Known limitations (disclosed, by design):** flat `key: value` only; no nested YAML, arrays, or multiline values; requires LF line endings and no BOM at file start (CRLF/BOM files fall back to empty frontmatter and still render); malformed frontmatter is silently ignored. If a document needs real YAML semantics, swap in `gray-matter` — it is the one dependency upgrade that preserves every contract in this document.

#### 3.2 Configuration surface (deliberately small)

The configuration surface is **frontmatter (§3.1) + template choice + tag registry**. There is **no** `defineConfig` helper, no `virtual:` module, no build-time config-object plugin. That architecture was considered and rejected: it depends on packaging machinery the skill does not provide, and user-supplied Tailwind class strings inside config files are invisible to Tailwind's scanner unless the file happens to be scanned (dynamic-class hazard — Finding 21.6's cousin). If you need richer build-time configuration, that is an extension project, not a flag.

The `MarkdownToWebConfig` type is included in §22 for teams that want to build their own config helper — but the base skill does not provide one.

### §4 Tech Stack & Pinned Versions

Every dependency below is pinned to a specific version. The pre-ship checklist (§17) includes `npm ls --depth=0` (gate 8 / gate V-1) to verify the installed versions match this table exactly. Drift from these versions risks breaking the slug-parity contract (§9) and the `@theme` token generation (§6).

| Layer | Technology | Version | Provenance / note |
|-------|------------|---------|-------------------|
| Framework | React | **19.2.6** | Lineage-verified (v1.0.1 `package.json`) |
| Build | Vite | **7.3.2** | Lineage-verified; `?raw` imports for Markdown |
| Styling | Tailwind CSS | **4.1.17** | CSS-first `@theme inline`; **no `tailwind.config.js`** |
| Markdown | react-markdown | **10.1.0** | `remark-gfm` + `rehype-slug`; component map renders Markdown as React elements (no `dangerouslySetInnerHTML`) |
| GFM | remark-gfm | **4.0.1** | Lineage-consistent major for react-markdown 10 |
| Heading anchors | rehype-slug | **6.0.0** | Must match `github-slugger` output (verified by `slug-parity.test.ts`, §9.3) |
| TOC slugs | github-slugger | **2.0.0** | Default export class; **no named `slug` export exists** (§16 anti-pattern #7) |
| Icons | lucide-react | **1.28.0 — Unverified** | See gate V-1 below. If install fails to resolve, use the current 0.x line and update this row |
| Class util | clsx + tailwind-merge | **2.1.1 / 3.4.0** | `cn()` — actively used (in `Badge`, template components) |
| Packaging | vite-plugin-singlefile | **2.3.0** | Inlines JS/CSS into `dist/index.html` |
| Syntax highlight (opt-in) | rehype-highlight + highlight.js | ^7 / ^11 (Assumed) | **Opt-in** (§19.4); confirm at install |
| Fonts (offline mode) | @fontsource-variable/source-serif-4, @fontsource-variable/inter, @fontsource/jetbrains-mono | latest (Assumed) | §11.3 |
| TypeScript | typescript | **5.9.3** | `strict: true`, `noUnusedLocals`, `noUnusedParameters` |
| Test | vitest | ^2 (Assumed) | Unit tests, coverage thresholds §14.10 |
| A11y gate | @playwright/test + @axe-core/playwright | ^1.40 / ^4 (Assumed) | §10.6, §14.9 |
| Lint | eslint + typescript-eslint + eslint-plugin-react-hooks + eslint-plugin-jsx-a11y | ^9 (Assumed) | Flat config |
| Formatter | prettier | ^3 (Assumed) | Run after `eslint --fix` to avoid drift (§15.2) |
| Markdown lint | markdownlint-cli2 | ^0.15 (Assumed) | Content quality gate |
| Node | — | **≥20.19 or ≥22.12** | Vite 7 requirement |

**Version discipline:** exact pins for everything lineage-verified; caret ranges only for additions this merge introduces (testing/lint/highlight), each tagged *Assumed* until install.

**Gate V-1 (version verification, mandatory):**

```bash
npm ls --depth=0
# Every row above must appear at the stated version.
# lucide-react: confirm the resolved version and correct this table if it differs.
```

Never repeat a version number from memory or from another document. `npm ls` is the only source of truth (closes the lucide-react 1.28.0-vs-0.400.0 drift across drafts).

**Dependency selection criteria (for any future addition):**

- Active maintenance (commit within 6 months)
- TypeScript types included or `@types/*` available
- MIT, Apache-2.0, or BSD-3-Clause license (no copyleft)
- Zero known critical vulnerabilities (`npm audit`)
- Download count > 100k/week (indicates adoption)
- < 10 MB unpacked size

### §5 Project Skeleton

```
markdown-to-web/
├── package.json
├── package-lock.json              # committed — never hand-edit
├── vite.config.ts
├── tsconfig.json
├── eslint.config.js
├── .prettierrc
├── vitest.config.ts
├── playwright.config.ts
├── index.html                     # <div id="root"> + module script
├── .husky/
│   └── pre-commit                 # lint-staged + typecheck + unit tests
├── .github/
│   └── workflows/
│       └── ci.yml                 # Appendix D
├── src/
│   ├── main.tsx                   # Entry: StrictMode + ErrorBoundary + createRoot + offline-font conditional
│   ├── App.tsx                    # Layout, drawer/theme/activeSlug state, TOC derivation, IntersectionObserver
│   ├── index.css                  # Tailwind v4 @import + Google Fonts + template @theme import
│   ├── content/
│   │   └── document.md            # The input markdown (?raw import)
│   ├── templates/
│   │   ├── editorial/
│   │   │   ├── theme.css          # @theme tokens for editorial (light + dark) — §6 pattern
│   │   │   ├── components.tsx     # Component map overrides (optional)
│   │   │   ├── layout.tsx         # Layout shell (sidebar + drawer + hero)
│   │   │   └── tags.json          # Default tag registry (Severity + Confidence)
│   │   ├── technical/
│   │   │   ├── theme.css          # §7.2 (full CSS, @theme-fixed)
│   │   │   ├── components.tsx
│   │   │   ├── layout.tsx
│   │   │   └── tags.json          # Status + Visibility
│   │   └── minimal/
│   │       ├── theme.css          # §7.3 (full CSS + print, @theme-fixed)
│   │       ├── components.tsx
│   │       ├── layout.tsx
│   │       └── tags.json          # Empty (badges opt-in)
│   ├── components/
│   │   ├── MarkdownRenderer.tsx   # react-markdown renderer + default components map
│   │   ├── TableOfContents.tsx    # Recursive TOC (sidebar + drawer) + active-section highlight
│   │   ├── Badge.tsx              # Tag-aware badge (replaces StatusBadge)
│   │   ├── ErrorBoundary.tsx      # Class component, catches render errors — fixes Finding 21.15
│   │   ├── ErrorFallback.tsx      # Presentational fallback UI
│   │   ├── SkipLink.tsx           # Accessible skip-to-content
│   │   └── ThemeToggle.tsx        # Light/dark/system toggle with localStorage (try/catch wrapped)
│   ├── lib/
│   │   ├── fence.ts               # Fence-aware line scanner — fixes Finding 21.5 (NEW from draft_q3)
│   │   ├── enhance.ts             # Tag-aware regex preprocessor (fence-aware, emits warnings)
│   │   ├── toc.ts                 # H2–H4 outline extraction (fence-aware, slug reservation)
│   │   ├── tags.ts                # Registry validation, collision detection, resolver — fixes Finding 21.6
│   │   ├── frontmatter.ts         # YAML frontmatter extraction (CRLF-safe)
│   │   └── slug-parity.test.ts    # Unit test: github-slugger vs rehype-slug
│   ├── utils/
│   │   ├── cn.ts                  # clsx + tailwind-merge — actively used
│   │   └── theme-storage.ts       # localStorage with try/catch + in-memory fallback — fixes Finding 21.11
│   └── types/
│       ├── template.ts            # TemplateConfig, TemplateLayoutProps, ComponentsMap
│       ├── tag.ts                 # TagDefinition, TagRegistry, TagValueDefinition, ResolvedBadge
│       ├── toc.ts                 # TocItem (level 2 | 3 | 4)
│       ├── config.ts              # MarkdownToWebConfig (for teams that want it; no defineConfig helper)
│       └── frontmatter.ts         # Frontmatter schema
├── scripts/
│   ├── build-offline.mjs          # Offline-font build variant (§11.3)
│   ├── generate-color-ref.mjs     # Auto-generates §color reference from @theme — fixes Finding 19.1
│   └── quality-gate.sh            # Runs all 8 pre-ship gates in order
└── tests/
    ├── unit/
    │   ├── fence.test.ts          # Fence scanner unit tests — §14.2 (NEW)
    │   ├── enhance.test.ts        # Tag preprocessor unit tests — §14.3
    │   ├── toc.test.ts            # TOC extraction unit tests — §14.4
    │   ├── slug-parity.test.ts    # github-slugger === rehype-slug — §14.5
    │   ├── frontmatter.test.ts    # Frontmatter parsing tests — §14.6
    │   └── tags.test.ts           # Registry validation + resolver tests — §14.7 (NEW)
    ├── integration/
    │   └── markdown-rendering.test.tsx  # Full pipeline: badges, TOC, headings — §14.8
    ├── accessibility/
    │   └── axe.test.ts            # Playwright + axe: WCAG 2.2 AA + AAA aspirational, light + dark — §14.9
    └── performance/
        └── bundle-size.test.ts    # Bundle size budgets — §13.4
```

**File responsibility rule:** One file, one responsibility. `MarkdownRenderer.tsx` renders; `Badge.tsx` styles tags; `tags.ts` loads/validates/resolves the registry; `enhance.ts` preprocesses strings; `fence.ts` scans lines for fence state; `ErrorBoundary.tsx` catches errors; `ErrorFallback.tsx` renders the fallback UI. No file mixes concerns.

**Custom hooks: None exist as standalone hooks.** Theme state, drawer state, and the active-section observer live inline in `App.tsx` (`useState` / `useEffect` / `useMemo`). Documented explicitly so no agent searches for a `hooks/` directory *(preserves Finding 6.1's discipline)*. If a template needs a focus trap (e.g., a search palette), add it in that template's layout, not as shared infrastructure.

#### 5.1 Bootstrap from scratch

No starter repository ships with this document. To instantiate:

```bash
# 1. Scaffold
npm create vite@latest markdown-to-web -- --template react-ts
cd markdown-to-web

# 2. Install runtime deps (exact pins from §4)
npm install react-markdown@10.1.0 remark-gfm@4.0.1 rehype-slug@6.0.0 \
  github-slugger@2.0.0 lucide-react@1.28.0 clsx@2.1.1 tailwind-merge@3.4.0 \
  vite-plugin-singlefile@2.3.0

# 3. Install dev deps
npm install -D tailwindcss@4.1.17 @tailwindcss/vite@4.1.17 \
  vitest@2.x @vitest/coverage-v8 \
  @playwright/test@1.40.0 @axe-core/playwright@4.10.0 \
  eslint@9.x typescript-eslint@8.x eslint-plugin-react-hooks@5.x \
  eslint-plugin-jsx-a11y@6.x prettier@3.x markdownlint-cli2@0.15.x \
  husky lint-staged

# 4. Opt-in syntax highlighting
npm install rehype-highlight highlight.js

# 5. Opt-in offline fonts
npm install @fontsource-variable/source-serif-4 @fontsource-variable/inter \
  @fontsource/jetbrains-mono

# 6. Create the file tree in §5 and run gate V-1 before anything else
npm ls --depth=0   # Compare against §4 table
```

### §6 Design System (Two-Layer Token Pattern)

The two-layer token pattern is the v4.0.0 contribution that fixes the `@theme`-in-`@media` bug (Finding 21.1, Critical). draft_z proposed `@theme` inside `@media (prefers-color-scheme: dark)`. **That is invalid Tailwind v4** — `@theme` is a build-time, top-level directive. The correct idiom (draft_q3's mechanics, formalized here):

- **Layer 1 — runtime variables** (`:root`, flipped by media query / `[data-theme]`): the actual color values.
- **Layer 2 — `@theme inline`**: bridges runtime variables into Tailwind utilities, so `bg-paper-50` compiles to `background-color: var(--paper-50)` and flips live at runtime.

**Theming rule:** dark mode happens exclusively through variable flipping. Templates must not use `dark:` utilities — one mechanism, no drift.

#### 6.1 Editorial template `src/index.css` (full listing)

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

:focus:not(:focus-visible) {
  outline: none;
}

/* Code blocks (with opt-in rehype-highlight) */
pre code.hljs {
  border-radius: 0.5rem;
  padding: 1.25rem;
  font-size: 0.875rem;
  line-height: 1.7;
}
```

**Dark-mode semantics to remember:** token *names* keep their role (ink = text/surfaces-that-invert, paper = page backgrounds), so `text-ink-900` stays "primary text" in both modes. Accent tokens (§8) are used for badge text on *light chip surfaces that do not flip* — see §8.6.

#### 6.2 Typography hierarchy (editorial)

| Role | Font | Weight | Mobile | Desktop | Color |
|------|------|--------|--------|---------|-------|
| H1 | Source Serif 4 | 600 | `text-3xl` | `sm:text-4xl lg:text-5xl` | ink-900 |
| H2 | Source Serif 4 | 600 | `text-2xl` | `sm:text-[1.75rem]` | ink-900 |
| H3 | Source Serif 4 | 600 | `text-xl` | `sm:text-2xl` | ink-800 |
| H4 | Source Serif 4 | 600 | `text-lg` | — | ink-700 |
| Body | Inter | 400 | `text-base` (16px) | — | stone-700 (light) |
| Meta / labels | JetBrains Mono | 500 | `text-xs`, tracking-wide | — | teal-700 |
| Badge | Inter | 600 | `text-xs`, uppercase, tracking-wide | — | per-accent (§10.3 exception) |
| Code inline | JetBrains Mono | 400 | `text-[0.85em]` | — | ink-800 |

#### 6.3 Color reference drift prevention

The complete color table is **generated, not hand-maintained**: `node scripts/generate-color-ref.mjs` parses the Layer-1 variables in `src/index.css` and emits the markdown table below (prevents the v1.0.1 drift risk — Finding 19.1).

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

#### 6.4 Token usage rules

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

#### 6.5 Z-index layer map

| z-index | Element | Purpose | File |
|---------|---------|---------|------|
| `z-50` | Skip-to-content link (focused); drawer overlay + panel | Topmost | `SkipLink.tsx`, `App.tsx` |
| `z-40` | Sticky header | Above content, below drawer | `App.tsx` |
| `z-30` | (reserved) sticky-in-content elements | Future: search palette, "on this page" outline | `templates/technical/layout.tsx` |
| `z-60` | (reserved) command palette / search overlay | Future: cmd-K palette (Appendix E) | (Optional) |
| (default) | Main content, sidebar, report | Normal flow | — |

No portals, dialogs, or tooltips exist. If you add one, update this map in the same commit.

#### 6.6 `theme-storage.ts` (fixes Finding 21.11)

```typescript
// src/utils/theme-storage.ts
const STORAGE_KEY = "theme";
const fallbackStore = new Map<string, string>();

export function readTheme(): string | null {
  try {
    return localStorage.getItem(STORAGE_KEY);
  } catch {
    // localStorage unavailable (sandboxed iframe, file:// in some browsers)
    return fallbackStore.get(STORAGE_KEY) ?? null;
  }
}

export function writeTheme(theme: string): void {
  try {
    localStorage.setItem(STORAGE_KEY, theme);
  } catch {
    fallbackStore.set(STORAGE_KEY, theme);
  }
}
```

### §7 Three Templates

Templates are the right level of generalization. Not "one config to rule them all" (too rigid) and not "multi-framework adapters" (over-engineered). Three opinionated templates with consistent contracts cover the realistic use space.

#### 7.1 Template A — Editorial Long-Form (default)

**Use for:** Audit reports, essays, long-form journalism, comparative analyses, design critiques.

**Layout:**
- Sticky dark header (`z-40`) with title, theme toggle, and (mobile) menu trigger
- Desktop: left sidebar (`w-64`, sticky, `top-24`) with TOC; main content column (`max-w-3xl`)
- Mobile: slide-in drawer (`z-50`) with TOC; full-width content
- Hero: title + subtitle + meta chips (author, date, reading time)
- Footer: source link, generated date

**Visual register:** Bespoke editorial — Source Serif 4 display, warm paper background (`paper-50`), teal/moss accents. This is the v1.0.1 design, generalized. The anti-generic mandate applies in full: no purple gradients, no Bootstrap card grids, no Inter-on-gray-50 neutrality.

**Default tag registry:** Severity (`critical`/`high`/`medium`/`low`/`informational`) + Confidence (`verified`/`reasoned`/`assumed`/`unverifiable`). Loaded from `templates/editorial/tags.json` (see §8.2).

**When to choose this template:** The document is read sequentially, top-to-bottom, and benefits from a sticky TOC. Reading time is 5+ minutes. Typography matters (it's a published artifact, not a reference).

#### 7.2 Template B — Technical Docs

**Use for:** API references, technical specifications, developer guides, RFCs.

**Layout:**
- Sticky light header with search box (cmd-K palette, optional — Appendix E)
- Three-column desktop: left nav (`w-60`), content (`max-w-4xl`), right "on this page" outline (`w-48`, sticky, `z-30`)
- Mobile: drawer nav; content; inline "on this page" accordion at top
- No hero — jump straight to H1 + first paragraph
- Footer: edit-on-GitHub link, version

**Visual register:** Utilitarian — Inter throughout (display + body), cool gray background, blue accent. Code blocks are first-class (syntax-highlighted when `syntaxHighlighting: true`, copy button). The anti-generic mandate is relaxed here: technical docs legitimately use Inter-on-gray neutrality; that is the design register for this template.

**Default tag registry:** Status (`stable`/`experimental`/`deprecated`/`removed`) + Visibility (`public`/`internal`/`restricted`).

**When to choose this template:** The document is read non-linearly — users jump to specific sections via search or TOC. Code blocks are frequent. Reading time is variable; the user may read one section and leave.

**`src/templates/technical/theme.css` — key differences from editorial (full file uses the §6.1 two-layer pattern):**

```css
/* Layer 1 :root — cool gray scale + blue accent (light) */
:root {
  --bg: #ffffff;  --bg-secondary: #f8fafc;  --bg-tertiary: #f1f5f9;
  --text: #0f172a;  --text-secondary: #475569;  --text-tertiary: #94a3b8;
  --border: #e2e8f0;
  --accent: #2563eb;  --accent-bg: #eff6ff;  --accent-ring: #bfdbfe;  --accent-dark: #1d4ed8;
  --accent-1: #dc2626;  --accent-2: #f59e0b;  --accent-3: #2563eb;
  --accent-4: #10b981;  --accent-5: #8b5cf6;
  --accent-1-bg: #fef2f2;  --accent-2-bg: #fffbeb;  --accent-3-bg: #eff6ff;
  --accent-4-bg: #ecfdf5;  --accent-5-bg: #f5f3ff;
}

/* Dark mode (same pattern as editorial — :root:not([data-theme="light"]) + [data-theme="dark"]) */
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg: #0f172a;  --bg-secondary: #1e293b;  --bg-tertiary: #334155;
    --text: #f8fafc;  --text-secondary: #cbd5e1;  --text-tertiary: #64748b;
    --border: #334155;  --accent: #60a5fa;  --accent-dark: #3b82f6;
  }
}
[data-theme="dark"] { /* same overrides as above */ }

/* Layer 2 @theme inline — bridges Layer 1 variables into Tailwind utilities */
@theme inline {
  --font-serif: "Inter", ui-sans-serif, system-ui, sans-serif;  /* all Inter for technical */
  --font-sans: "Inter", ui-sans-serif, system-ui, sans-serif;
  --font-mono: "JetBrains Mono", ui-monospace, monospace;
  --color-bg: var(--bg);  --color-bg-secondary: var(--bg-secondary);
  /* ... all color tokens bridged per §6.1 pattern ... */
}

/* Reduced motion, focus-visible, base — identical to editorial (§6.1) */
```

The full file follows the §6.1 two-layer pattern exactly — only the Layer-1 color values differ (cool gray + blue instead of ink/paper + teal). The `@theme inline` block, reduced-motion media query, and `:focus-visible` rule are identical to editorial.

#### 7.3 Template C — Minimal Print

**Use for:** Manuscripts, legal documents, printable reports, archival content.

**Layout:**
- Single column, `max-w-2xl`, centered
- No header, no sidebar, no drawer — just title + content + page footer
- Print CSS: `page-break-before: always` on H2, `@page { size: A4; margin: 2cm }`, no color in print (black on white)
- Optional "Download PDF" button using `window.print()`

**Visual register:** Minimal — system serif/sans/mono (no web fonts), black on white, no accent colors except for badges. This template ships with `offlineFonts: true` by default because it is designed for archival and print contexts where CDN dependence is unacceptable.

**Default tag registry:** None (badges disabled by default; opt-in via frontmatter `badgeConfig`).

**When to choose this template:** The document is intended for print or archival reading. Typography should be unobtrusive. No interactive chrome is needed.

**`src/templates/minimal/theme.css` — key differences from editorial (full file uses the §6.1 two-layer pattern):**

```css
/* Layer 1 :root — system fonts, high contrast, print-ready */
:root {
  --font-sans: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-serif: ui-serif, Georgia, "Times New Roman", serif;
  --font-mono: ui-monospace, "Cascadia Code", "Source Code Pro", Menlo, Consolas, monospace;
  --bg: #ffffff;  --text: #000000;  --border: #d1d5db;
  --accent: #1a56db;
  --accent-1: #dc2626;  --accent-2: #f59e0b;  --accent-3: #2563eb;
  --accent-4: #059669;  --accent-5: #7c3aed;
}

/* Minimal template is light-only by design — no dark mode overrides */

/* Layer 2 @theme inline — bridges per §6.1 pattern (system fonts, no web fonts) */
@theme inline {
  --font-serif: var(--font-serif);
  --font-sans: var(--font-sans);
  --font-mono: var(--font-mono);
  --color-bg: var(--bg);  --color-text: var(--text);
  /* ... accent tokens bridged ... */
}

/* Print styles (unique to minimal template) */
@media print {
  .no-print { display: none !important; }
  body { font-size: 12pt; line-height: 1.5; }
  h1 { font-size: 24pt; }
  h2 { font-size: 18pt; page-break-before: always; }
  h2:first-of-type { page-break-before: avoid; }
  h3 { font-size: 14pt; }
  a { text-decoration: underline; color: #000; }
  a[href^="http"]::after { content: " (" attr(href) ")"; font-size: 0.9em; }
  .badge { border: 1px solid #000; background: #fff !important; color: #000 !important; }
  pre, code { background: #f5f5f5 !important; }
  pre, blockquote { page-break-inside: avoid; }
  * { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  @page { size: A4; margin: 2cm; }
}

/* Reduced motion, focus-visible, base — identical to editorial (§6.1) */
```

The minimal template is light-only (no dark mode overrides). The print CSS is unique to this template — page breaks before H2, full URLs printed after links, `print-color-adjust: exact` so badges retain semantic color in print.

#### 7.4 Template contract

Every template MUST provide:

```typescript
// src/types/template.ts
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

The build system loads the template specified in frontmatter (or the default `editorial`), merges its component overrides with the default map, and renders the layout shell with the markdown content as children.

### §8 Tag Registry & Badge Protocol

The v1.0.1 badge system hardcoded 9 keys and matched only `-` bullets. v4.0.0 replaces this with: **tag registry (data) + fence-aware preprocessor (with warnings) + generic resolver (cross-category lookup with collision detection).** Tags are data (JSON or TS), not code — adding a new tag value should not require touching a TypeScript file.

#### 8.1 Tag registry schema

```typescript
// src/types/tag.ts
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

#### 8.2 Default registry (editorial template)

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

#### 8.3 Validation + collision detection + resolver (fixes Finding 21.6)

```typescript
// src/lib/tags.ts
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

#### 8.4 Fence-aware preprocessor (fixes Finding 21.5)

```typescript
// src/lib/enhance.ts
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

**Disclosed blind spots (do not "fix" silently):** badges inside blockquotes (`> - **Tag:** v`) are not matched; values with trailing punctuation (`critical.`) warn and render unstyled; only first-level bullets are targeted. Each is covered by a fixture in §14.3.

#### 8.5 End-to-end pipeline (the backtick-wrapping pattern)

This is the critical path that v1.0.1 got right, draft_d2 broke (raw HTML / `dangerouslySetInnerHTML`), and draft_q2 disconnected (AST plugin vs. React component). v4.0.0 preserves v1.0.1's pattern *(fixes Findings 21.3 and 21.4)*:

```
1. Author writes:        - **Severity:** critical
2. enhance.ts wraps:     - **Severity:** `critical`
3. react-markdown parses:inline code element with children="critical"
4. components.code:      resolveBadge(registry, "critical") → <Badge tag="Severity" value="Critical" accent={1} />
5. Badge renders:        <span class="... text-accent-1 ...">Critical</span>
```

No `dangerouslySetInnerHTML`. No raw HTML emission. No AST plugin that doesn't connect to the React component. The `code` component map entry is the bridge between react-markdown's parsing and the `Badge` component:

```typescript
// src/components/MarkdownRenderer.tsx (excerpt)
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

Syntax highlighting is **opt-in**: install `rehype-highlight`, add it to `rehypePlugins` after `rehypeSlug`, and import a highlight.js CSS theme. If you fork this pipeline into something that serializes HTML strings, sanitization (`rehype-sanitize`) becomes mandatory — in the components-map pipeline above it is not needed because no raw HTML is ever rendered.

#### 8.6 Badge component

```typescript
// src/components/Badge.tsx
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
      aria-label={`${tag}: ${value}`}
    >
      {value}
    </span>
  );
}
```

**Dark-mode note (deliberate):** chip backgrounds/rings use the static Tailwind default palette, so chips stay light-surface in both modes. Accent text contrast is therefore identical in light and dark — computed against the chip, not the page (§10.3). All badge classes live in source files Tailwind scans; never move them into runtime-provided strings (§16 anti-pattern #11).

**Note on badge text size:** v4.0.0 uses `text-xs` (12px) for badges, NOT `text-sm` (14px). The "14px relaxes AAA threshold" claim (Finding 21.2) is an arithmetic error — 14px is not large text. Badge text contrast is handled honestly via §10.3 (enumerated AAA exceptions) and §10.5 (high-contrast recipe as opt-in).

#### 8.7 Improvements over v1.0.1

1. Accepts all bullet styles (`-`, `*`, `+`, ordered `1.`) — v1.0.1 only matched `-`.
2. Emits build-time warnings for unknown tags and values — v1.0.1 silently passed them through as plain text.
3. Tag set is data (JSON), not code — v1.0.1 hardcoded 9 keys.
4. Fence-aware — fenced badge lines are left untouched (fixes Finding 21.5).
5. Cross-category resolver with collision detection — ambiguity throws at load, never renders wrong (fixes Finding 21.6).

### §9 TOC + Navigation Engine

The TOC extracts headings from the markdown, generates slugs that match `rehype-slug`'s rendered `id` attributes, and renders a recursive navigation tree. Active-section highlighting uses `IntersectionObserver`. Slug parity between `github-slugger` (TOC) and `rehype-slug` (rendered headings) is verified by a unit test (§9.3) — this is the single most important test in the skill.

#### 9.1 Fence-aware scanner (fixes Finding 21.5)

Shared by `buildToc` and `enhanceMarkdown`. Fixes the fence-blind line regexes of v1.0.1/draft_k/draft_z/draft_z2/draft_d2/v2.1.0 — a `## comment` inside a code fence must neither enter the TOC nor consume a slug counter.

```typescript
// src/lib/fence.ts
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

#### 9.2 Extraction with slug reservation

Two correctness mechanisms:

1. **Stack algorithm** (hand-traced: nested, sibling-after-nested, orphan, and mixed cases all correct — draft_q2's variant is *not* used; it mis-nests any H2 that follows an H3).
2. **Slug reservation for every heading level** — `rehype-slug` slugs H1–H6 in document order with dedup counters; a TOC that only sees H2–H4 would desync on duplicate text (e.g. `# Intro` then `## Intro`). The slugger therefore consumes every heading; only H2–H4 enter the tree.

```typescript
// src/lib/toc.ts
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

**Why the stack algorithm is correct:** The `while` loop pops until the top of the stack has a level *strictly less than* the current heading's level. This means:
- H2 → H2: stack has `[H2]`. New H2's level (2) is `>=` top's level (2), so pop. Stack is empty. Push new H2 as top-level. ✓
- H2 → H3: stack has `[H2]`. New H3's level (3). `2 >= 3` is false, so don't pop. H3 becomes child of H2. ✓
- H2 → H4 (skipping H3): stack has `[H2]`. `2 >= 4` is false, so don't pop. H4 becomes child of H2. ✓
- H2 → H4 → H3: After H4, stack is `[H2, H4]`. New H3's level (3). Pop while top's level `>= 3`: top is H4 (level 4), `4 >= 3` true, pop. Top is now H2 (level 2), `2 >= 3` false, stop. H3 becomes child of H2. ✓

Contract: H2 = depth 1 · H3 = depth 2 (`ml-3 border-l`) · H4 = depth 3 (`ml-6 border-l`) · orphans promote to top level · backticks stripped from display text (matching hast text content, which is what `rehype-slug` hashes).

#### 9.3 Slug parity — tested, not asserted (fixes Finding 2.2)

The lineage's most-cited failure mode ("two slug generators must stay in sync") is closed by a test that **compiles and runs**: correct default import, no unused imports (passes the strict `noUnusedLocals` gate the skill itself mandates — fixes Finding 21.13), fixtures for CJK, emoji, inline code, duplicates, and cross-level dedup.

```typescript
// tests/slug-parity.test.ts
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

Both packages are pinned (§4); this test runs in CI. **Known scope limitation (§9.4):** parity is guaranteed for ATX headings only.

#### 9.4 Disclosed limitations

- **Setext headings** (`Title\n=====`) are invisible to the line-based extractor but real to `rehype-slug` — they can desync dedup counters for later duplicate text. Content convention: **ATX headings only.** If a document type needs setext support, migrate extraction to the AST (the extension path in §19.3 — this is the one place AST parsing earns its complexity).
- Headings deeper than `maxDepth` are still slug-reserved (correct) but not listed.
- `scroll-mt-24` on every anchored heading compensates for the sticky header; never hand-write heading `id`s.

#### 9.5 Active-section highlighting

```typescript
// src/App.tsx (excerpt)
function flattenToc(items: TocItem[]): TocItem[] {
  return items.flatMap((i) => [i, ...flattenToc(i.children)]);
}

const [activeSlug, setActiveSlug] = useState<string>("");

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

Pass `activeSlug` to `TableOfContents` to highlight the current section. The `flattenToc` pattern observes **all** TOC levels (not just top-level) — fixes a common bug where H3/H4 sections never highlight.

#### 9.6 TOC contract table

| Heading Level | TOC Depth | Indentation |
|---------------|-----------|-------------|
| `##` (H2) | 1 | None |
| `###` (H3) | 2 | `ml-3` + left border |
| `####` (H4) | 3 | `ml-6` + left border |

- `buildToc()` extracts **H2, H3, and H4** headings by default (configurable via `maxDepth`)
- Orphan headings (no preceding parent) become top-level
- Backticks in heading text are stripped for display but the slug is generated from the stripped text (matching `rehype-slug` behavior)
- Slugs generated by `github-slugger` **must match `rehype-slug` output** — verified by `slug-parity.test.ts` (§9.3)

---
