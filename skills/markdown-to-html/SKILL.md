---
name: markdown-to-html
description: Renders an arbitrary Markdown document as a polished, single-file, accessible web page. Accepts any .md file plus an optional template (technical three-column / editorial long-form) and an optional tag registry (severity, confidence, status, custom). Built on React 19 + Vite 8 + Tailwind v4 + react-markdown + lucide-react. Includes mobile TOC drawer, back-to-top, code-block copy buttons, reading-time estimation (Latin + CJK-aware), print stylesheet, build-time title injection, source-markdown validation gate, CI workflow, and Husky pre-commit hook.
triggers:
  - render this markdown as a web page
  - convert .md to HTML
  - publish this document as a site
  - make a polished web version of this README/report/spec
version: 2.1.0
tags:
  - react
  - vite
  - tailwindcss
  - markdown
  - html
  - single-file-build
  - accessibility
  - documentation
  - tdd
  - ci
---

# markdown-to-web — Pipeline Skill v2.1.0

**Document version:** 2.1.0
**Date:** 2026-08-08
**Scope:** Unified, technically-correct replacement for `markdown-html-pipeline_SKILL-v2.md` v2.0.0, distilled from a full TDD remediation of the `nordeim/markdown-to-html` codebase. Captures every lesson, pattern, and anti-pattern encountered across the v2.0 53-finding audit, the v2.0→v2.1 outstanding-issues remediation, and the spec-vs-spec audit (`docs/v2_rendering_comparison_3.md`).
**Reviewer:** Super Z (GLM)
**Base document:** `markdown-html-pipeline_SKILL-v2.md` v2.0.0 (itself based on `original_SKILL.md` v4.1.1 → v1.0.0 → v2.0.0)
**Verification protocol:** Desk review + executed commands. Findings tagged Verified / Reasoned / Assumed per the evidence contract in §17. Every claim about the codebase traces to an executed command (`npm run typecheck`, `npm run lint`, `npm run lint:source`, `npm run lint:format`, `npm run lint:markdown`, `npm run test`, `npm run test:coverage`, `npm run build`, `npm run test:bundle-size`) — see the verification ledger in Appendix B.

---

## What's New in v2.1

v2.1.0 is a **focused delta** on v2.0.0 — not a rewrite. It fixes 3 bugs, adds 1 new quality gate, and removes 1 source of build noise. The v2.0.0 content is preserved intact; this section is the map of what changed.

| Category | Change | Where |
|----------|--------|-------|
| **New gate** | Gate 0: `lint:source` — validates source-markdown internal consistency (intro claim == summary table == actual rows) | §13, §9.2 |
| **Bug fix** | `IntersectionObserver` partial-callback bug — active section flickered/cleared while visible. Fixed with stateful `Map<id, boolean>` reducer | §20 Pattern 16, §17 Lesson 25 |
| **Bug fix** | CJK reading-time overestimate (~25%) — single 200 wpm rate applied to CJK. Fixed with separate Latin 200 wpm + CJK 300 cpm, max-of | §9.3, §20 Pattern 19, §17 Lesson 27 |
| **Bug fix** | Pre-hydration `<title>` flash — static placeholder shown until React hydrates. Fixed with build-time `transformIndexHtml` plugin | §9.4, §20 Pattern 17, §17 Lesson 28 |
| **Cleanup** | Redundant `inlineDynamicImports` build warning removed | §17 Lesson 29 |
| **New modules** | `src/lib/active-section.ts`, `src/lib/extract-title.ts`, `src/lib/validate-source.ts` | §5, §9.2, §9.4 |
| **New tests** | +21 unit tests (validate-source: 6, active-section: 6, extract-title: 7, reading-time: +2) | §27 |
| **New ADRs** | ADR-9 (why a gate not a test), ADR-10 (Map vs Set), ADR-11 (max vs sum), ADR-12 (build-time plugin) | §28 Appendix A |

**Unchanged from v2.0:** §6 (design system), §7 (component architecture), §10 (accessibility), §11 (config surface), §12 (template system), §22 (breakpoints), §23 (z-index), §24 (colors), §26 (component props).

---

## Part 1 — Remediation Context (Why v2.1 Exists)

v2.0.0 of this skill was technically correct in its patterns and the codebase it described passed all 8 documented quality gates. However, a subsequent spec-vs-spec audit (`docs/v2_rendering_comparison_3.md`) identified 10 outstanding issues that the v2.0 remediation had not addressed — issues that were either inherited from v1, introduced by the v2.0 remediation itself, or newly discoverable by examining the built artifacts against the spec.

The most consequential of these was the **source-markdown count mismatch**: the catalog's intro said "202 skills", the Category Summary table totaled 208, and the actual row count was 202. This defect had persisted across v1→v2.0 because no gate checked source-document internal consistency. The v2.0→v2.1 remediation closes this and 9 other issues, adds a new `lint:source` quality gate (Gate 0), and brings the test count from 124 to 145.

**What changed from v2.0.0:**

| Area | v2.0.0 | v2.1.0 |
|------|--------|--------|
| Tests | 124 vitest + 2 Playwright | 145 vitest + 2 Playwright (+21) |
| Quality gates | 8 | 9 (added `lint:source`) |
| Source-markdown validation | none | `src/lib/validate-source.ts` + `scripts/validate-source.mjs` + Gate 0 |
| Active-section tracking | naive `entries.every(!isIntersecting)` | stateful `Map<id, boolean>` reducer (`src/lib/active-section.ts`) |
| Reading-time for CJK | single 200 wpm rate (underestimated CJK by ~25%) | separate Latin 200 wpm + CJK 300 cpm, max-of |
| `<title>` in built HTML | static "Skills Catalog" + runtime `useEffect` | build-time `transformIndexHtml` plugin + runtime `useEffect` (no flash) |
| Build warnings | `inlineDynamicImports` ignored warning | warning eliminated (redundant option removed) |
| `CLAUDE.md` format | failed prettier | formatted |
| markdownlint in `docs/` | 130 errors across 5 files | 0 errors (globs exclude reference/audit docs) |
| Bundle size | 171.33 KB gzip | 171.40 KB gzip (+0.07 KB for new logic; 78.6 KB under budget) |
| Coverage | 87.5% / 77.11% / 85.32% / 90.09% | 89.84% / 81.15% / 85.84% / 91.8% |

---

## Part 2 — Skill Specification

### §1 Identity & Design Philosophy

**One-sentence description:** A zero-backend React application that renders any Markdown document as a polished, navigable, single-file web page, where the document's structure drives the UI, a swappable template drives the look, registered inline annotations render as semantic badges, a nine-gate quality pipeline (source-validation → typecheck → lint → format → markdownlint → test → coverage → build → bundle-size → a11y) enforces production-grade correctness, and the source document itself is validated for internal consistency at build time.

**Design thesis:** *Content is data; rendering is configuration; gates are real; source is sovereign.* The Markdown file is the input. The template chooses the look. The tag registry chooses which inline annotations become badges. The build produces one self-contained `dist/index.html` that runs anywhere a browser can open a file — online or offline. Every quality claim is backed by a config file and a CI job, not by documentation alone. The source markdown is treated as a first-class artifact: if its internal counts don't agree, the build fails.

**Core tenets:**

1. **Content is sovereign.** The markdown file determines structure. The renderer never invents content. Editing markdown never requires code changes. The frontmatter block is metadata and is *stripped before render* — it never leaks into the document body.
2. **One rendering pipeline.** `react-markdown` + components map. No `dangerouslySetInnerHTML`, no HTML-string serialization, no raw-HTML injection into the markdown source.
3. **Tags are registered, not hardcoded.** Badges are data in a registry; the resolver is generic; value collisions fail fast at load; badge resolution cannot misfire on code blocks.
4. **Single-file portability, honestly stated.** JS/CSS are inlined; fonts are a runtime dependency by default, with an opt-in offline build path documented. The inactive template's utility-class CSS leaks into the bundle (~1–2 KB) — this is an accepted trade-off of single-file portability, documented as a known limitation.
5. **Accessibility is gated, not claimed.** Conformance claim: **WCAG 2.2 AA, enforced by an axe gate; AAA where feasible.** The gate runs in both light and dark modes.
6. **No generic UI (per template).** The technical template uses a utilitarian cool-gray palette. The editorial template uses a warm cream-and-serif palette. The anti-generic mandate applies per template, not globally.
7. **Gates are real, not claimed.** Every documented quality gate has a config file, an npm script, and (where applicable) a CI job. A documented gate that cannot run is worse than no gate — it misleads maintainers.
8. **Types are canonical, not duplicated.** Every interface lives in `src/types/` exactly once. `lib/` modules import from `types/` and may re-export for convenience, but never redefine.
9. **TDD is the default.** New behavior gets a failing test first. Bug fixes get a regression test first. The test count is a first-class metric — a feature without tests is incomplete.
10. **Source data is validated.** (New in v2.1.) The source markdown is a first-class artifact. If its intro claim, summary table, and actual row counts don't agree, the build fails. A gate that checks rendered output but not source data will inherit source defects silently.

**Anti-generic mandate (per template):**

- **Technical:** rejects purple gradients, card grids, generic Inter-on-white neutrality. Embraces cool gray + blue, three-column density, monospace code.
- **Editorial:** rejects the same generic patterns but embraces warm cream + serif, single-column measure, drop-cap-ready hero.

---

### §2 When to Use / When Not To

**Use this skill when:**

- The user provides a Markdown file (`.md`) and asks for a "web version," "HTML rendering," "polished page," or "publishable site."
- The document is long-form (1,000–50,000 words) and benefits from a Table of Contents.
- The document contains structured annotations (`**Severity:** critical`, `**Status:** done`) that should render as visual badges.
- The artifact must run offline or from `file://`.
- Accessibility conformance (AA minimum, AAA aspirational) is a requirement.
- The user wants a single self-contained HTML file with no external runtime dependencies.
- The user wants a second template (editorial vs technical) without forking the codebase.
- The document has an internal count structure (intro claim + summary table + per-section rows) that must stay consistent.

**Do NOT use this skill when:**

- The user wants a full Next.js application with server-side rendering, API routes, or database. Use `fullstack-dev` instead.
- The user wants a slide deck / presentation. Use `pptx` instead.
- The user wants a PDF. Use `pdf` instead.
- The document is a code project README that needs interactive code execution.
- The document is shorter than ~500 words; a styled HTML page is overkill — render inline.
- The user needs multi-page navigation, search across documents, or user accounts. This skill renders one document into one HTML file.

**Template selection guide:**

| If the document is… | Use template | Why |
|---------------------|--------------|-----|
| API reference, technical spec, RFC, developer guide, skills catalog | `technical` (default) | Three-column layout; code blocks first-class; cool, utilitarian palette; persistent TOC sidebar |
| Audit report, essay, comparative analysis, design critique, long-form article | `editorial` | Single-column reading; narrow measure; warm serif; hero with subtitle + meta line |
| Manuscript, legal document, printable report, archival content | `minimal` (not yet implemented — deferred) | Single column; print CSS; no chrome; system fonts |

If unsure, start with `technical`. The build is identical across templates — switching is a one-file edit, not a fork.

---

### §3 Inputs Contract

The skill accepts the following inputs. All except the Markdown file are optional with sensible defaults.

| Input | Required | Format | Default | Notes |
|-------|----------|--------|---------|-------|
| Markdown file | Yes | `.md`, UTF-8 | — | GFM extensions supported: tables, strikethrough, task lists, autolinks |
| Template | No | `technical` \| `editorial` \| `minimal` | `technical` | See §12 |
| Tag registry | No | TS module or JSON | Template's default | See §11 |
| Frontmatter | No | flat `key: value` YAML | — | title/subtitle/author/date/template; §3.1 |
| Theme override | No | Partial Layer-1 variables | None | Merges with template's `:root` tokens |
| Offline fonts | No | build flag | `false` | When `true`, inlines fonts as base64 (extension path) |
| Syntax highlighting | No | Boolean | `false` | When `true`, enables `rehype-highlight` (extension path; not in base build) |

**Source-document internal consistency (NEW in v2.1):**

If the markdown document contains a "**N skills**" intro claim and a "## Category Summary" table, the `lint:source` gate (§13) asserts that:

1. `intro_count` (the N in `**N skills**`) matches `actual_rows` (count of `| **name** |` rows across all `## n. ...` sections).
2. Each per-category row in the summary table matches the actual row count for that section.
3. The summary table's `**Total**` row matches the sum of per-category rows.
4. The summary table's `**Total**` row matches `intro_count`.

A mismatch fails the build with a diagnostic listing every discrepancy. This prevents the 198/208/202 mismatch that persisted across v1→v2.0.

#### 3.1 Frontmatter schema

```yaml
---
title: "Document Title"           # overrides first H1; also sets document.title (build-time + runtime)
subtitle: "Optional subtitle"     # renders below title in hero (editorial) or meta line (technical)
author: "Author Name"             # renders in meta line
date: "2026-08-08"                # renders in meta line, ISO 8601
template: "technical"             # technical | editorial | minimal
---
```

**Known limitations (disclosed, by design):** flat `key: value` only; no nested YAML, arrays, or multiline values; malformed frontmatter is silently ignored and the whole input is treated as body (still renders). CRLF line endings are normalized; BOM is stripped. If a document needs real YAML semantics, swap in `gray-matter` — it is the one dependency upgrade that preserves every contract in this document.

---

### §4 Tech Stack & Pinned Versions

Every dependency below is pinned. The pre-ship checklist (§16) includes `npm ls --depth=0` to verify the installed versions match this table.

| Layer | Technology | Version | Provenance / note |
|-------|------------|---------|-------------------|
| Framework | React | `^19.2.8` | StrictMode + createRoot |
| Build | Vite | `^8.2.0` | `?raw` imports for Markdown; **Vite 8 deprecates `__dirname`** — use `import.meta.dirname` |
| Styling | Tailwind CSS | `^4.3.3` | CSS-first `@theme inline`; **no `tailwind.config.js`** |
| Tailwind Vite plugin | @tailwindcss/vite | `^4.3.3` | Must be ≥4.3.3 for Vite 8 compatibility |
| Markdown | react-markdown | `10.1.0` | `remark-gfm` + `rehype-slug`; component map renders Markdown as React elements (no `dangerouslySetInnerHTML`) |
| GFM | remark-gfm | `4.0.1` | Tables, strikethrough, task lists, autolinks |
| Heading anchors | rehype-slug | `6.0.0` | Must match `github-slugger` output (verified by `slug-parity.test.ts`) |
| TOC slugs | github-slugger | `2.0.0` | **Default export class only — no named `{ slug }` export exists** |
| Icons | lucide-react | `1.29.0` | Tree-shaken SVG icons: `Sun`, `Moon`, `Monitor`, `ArrowUp`, `Menu`, `X`, `Copy`, `Check` |
| Class util | clsx | `2.1.1` | Combined with tailwind-merge as `cn()` |
| Merge util | tailwind-merge | `3.4.0` | Prevents Tailwind class conflicts |
| Packaging | vite-plugin-singlefile | `2.3.3` | Must be ≥2.3.3 for Vite 8 compatibility; inlines JS/CSS into `dist/index.html` |
| TypeScript | typescript | `~6.0.2` | `strict: true`, `noUnusedLocals`, `noUnusedParameters`, `noUncheckedIndexedAccess`; **TS 6 deprecates `baseUrl`** — use `paths` with `./` prefix |
| Node types | @types/node | `^26.1.2` | Required for `process`, `fs`, `path`, `zlib` in tests |
| Test runner | vitest | `^4.1.10` | Unit + integration + bundle-size + coverage; **requires explicit `jsdom` package** |
| DOM testing | jsdom | `^30.0.1` | Peer of vitest, NOT bundled |
| Testing library | @testing-library/react | `^16.0.0` | `render`, `screen`, `fireEvent` |
| jest-dom | @testing-library/jest-dom | `^6.0.0` | `toBeInTheDocument()` and other matchers |
| Coverage | @vitest/coverage-v8 | `^4.1.10` | v8 provider; thresholds 80/75/80/80 |
| A11y gate | @axe-core/playwright | `^4.12.1` | Runs against built dist |
| E2E runner | @playwright/test | `^1.40.0` | **Browsers must be installed via `npx playwright install`** |
| Lint | eslint | `^9.39.5` | Flat config (`eslint.config.js`); zero-warning policy |
| TypeScript ESLint | typescript-eslint | `^8.66.0` | Recommended rules; `consistent-type-imports`; `no-explicit-any` |
| React hooks lint | eslint-plugin-react-hooks | `^5.2.0` | Catches hook misuse; `rules-of-hooks` + `exhaustive-deps` |
| JSX a11y lint | eslint-plugin-jsx-a11y | `^6.10.2` | Catches a11y anti-patterns |
| Formatter | prettier | `^3.0.0` | 100-char print width, double quotes, trailing comma all; run AFTER `eslint --fix` |
| Markdown lint | markdownlint-cli2 | `^0.14.0` | **v0.14+ requires `.markdownlint-cli2.jsonc` with explicit globs** (not `.markdownlint.json`) |
| Pre-commit | husky | `^9.0.0` | `.husky/pre-commit` runs lint-staged + typecheck |
| Staged lint | lint-staged | `^15.0.0` | ESLint --fix + Prettier --write + markdownlint --fix on staged files |

**Node requirement:** ≥20.19 or ≥22.12 (Vite 8 requirement).

**Version discipline:** exact pins for everything lineage-verified; caret ranges only for additions, each tagged *Assumed* until install.

**Gate V-1 (version verification, mandatory):**

```bash
npm ls --depth=0
# Every row above must appear at the stated version.
# lucide-react: confirm the resolved version (1.x line is correct; 0.x is the old line).
```

Never repeat a version number from memory or from another document. `npm ls` is the only source of truth.

---

### §5 Project Skeleton

```
markdown-to-web/
├── package.json                     # Dependencies + scripts + lint-staged config
├── package-lock.json                # Committed — never hand-edit
├── vite.config.ts                   # Build pipeline (uses import.meta.dirname; documentTitlePlugin)
├── tsconfig.json                    # Strict TypeScript (TS 6 compatible; no baseUrl)
├── eslint.config.js                 # ESLint 9 flat config (src + tests + scripts layers)
├── .prettierrc.json                 # Prettier config
├── .prettierignore                  # Excludes dist/, node_modules/, coverage/, docs/
├── .markdownlint-cli2.jsonc         # markdownlint config (excludes reference/audit docs)
├── vitest.config.ts                 # Test runner config (uses import.meta.dirname)
├── playwright.config.ts             # Accessibility test runner config
├── index.html                       # <div id="root"> + module script; <title> rewritten at build time
├── scripts/
│   └── validate-source.mjs          # CLI for `lint:source` gate (NEW in v2.1)
├── .husky/
│   └── pre-commit                   # lint-staged + typecheck
├── .github/
│   └── workflows/
│       └── ci.yml                   # Quality + accessibility CI jobs
├── src/
│   ├── main.tsx                     # Entry: StrictMode + ErrorBoundary + createRoot
│   ├── App.tsx                      # Layout, memoized pipeline, Map-based active-section observer
│   ├── index.css                    # Tailwind v4 @import + Google Fonts (NO template @theme)
│   ├── vite-env.d.ts                # Vite client types + *.md?raw declaration
│   ├── content/
│   │   └── document.md              # The input markdown (?raw import)
│   ├── templates/
│   │   ├── active.ts                # THE single edit point for template switching
│   │   ├── technical/               # Three-column technical docs template (default)
│   │   │   ├── theme.css            # @theme tokens + print styles
│   │   │   ├── components.tsx       # Component map overrides (h2, h3, h4, a)
│   │   │   ├── layout.tsx           # Three-column shell + meta line + MobileNav + BackToTop
│   │   │   └── tags.json            # Status + Visibility registry
│   │   └── editorial/               # Single-column long-form reading template
│   │       ├── theme.css            # Warm cream-and-serif palette + print styles
│   │       ├── components.tsx       # Larger headings, italic H3
│   │       ├── layout.tsx           # Hero + single-column shell
│   │       └── tags.json            # Severity + Confidence registry
│   ├── components/
│   │   ├── MarkdownRenderer.tsx     # react-markdown renderer + components map + CodeBlockWrapper
│   │   ├── TableOfContents.tsx      # Recursive TOC with active-section styling + aria-label
│   │   ├── Badge.tsx                # Tag-aware badge chip (5 accent steps)
│   │   ├── ErrorBoundary.tsx        # Class component render error catcher (stores errorInfo)
│   │   ├── ErrorFallback.tsx        # Presentational fallback UI with reload
│   │   ├── SkipLink.tsx             # Accessible skip-to-content
│   │   ├── ThemeToggle.tsx          # Light/dark/system toggle (lucide icons + aria-live + matchMedia)
│   │   ├── BackToTop.tsx            # Floating scroll-to-top button
│   │   ├── MobileNav.tsx            # Mobile TOC drawer (dialog + focus trap)
│   │   └── CopyButton.tsx           # Clipboard copy with execCommand fallback
│   ├── lib/
│   │   ├── fence.ts                 # Fence-aware line scanner (CommonMark subset)
│   │   ├── enhance.ts               # Tag-aware regex preprocessor (3-space indent rule)
│   │   ├── toc.ts                   # H2–H4 outline extraction with slug reservation
│   │   ├── tags.ts                  # Registry validation + collision detection + resolver
│   │   ├── frontmatter.ts           # YAML frontmatter parse + strip (BOM-safe, CRLF-safe)
│   │   ├── reading-time.ts          # Latin 200 wpm + CJK 300 cpm reading-time estimator
│   │   ├── config.ts                # Optional MarkdownToWebConfig validator
│   │   ├── active-section.ts        # Pure reducer for IntersectionObserver tracking (NEW v2.1)
│   │   ├── extract-title.ts         # Build-time document-title extractor (NEW v2.1)
│   │   └── validate-source.ts       # Source-markdown count-consistency validator (NEW v2.1)
│   ├── types/
│   │   ├── tag.ts                   # TagDefinition, TagRegistry, ResolvedBadge (canonical)
│   │   ├── toc.ts                   # TocItem (canonical)
│   │   ├── frontmatter.ts           # Frontmatter, ParsedDocument
│   │   ├── template.ts              # TemplateConfig, TemplateLayoutProps, ComponentsMap
│   │   ├── config.ts                # MarkdownToWebConfig
│   │   └── enhance.ts               # EnhanceResult
│   └── utils/
│       ├── cn.ts                    # clsx + tailwind-merge
│       └── theme-storage.ts         # localStorage with try/catch + in-memory fallback
├── tests/
│   ├── setup.ts                     # jest-dom + IntersectionObserver mock + matchMedia mock
│   ├── unit/                        # 89 tests across 11 files
│   │   ├── fence.test.ts            # 5
│   │   ├── enhance.test.ts          # 10
│   │   ├── toc.test.ts              # 9
│   │   ├── frontmatter.test.ts      # 7
│   │   ├── tags.test.ts             # 6
│   │   ├── slug-parity.test.ts      # 9
│   │   ├── config.test.ts           # 14
│   │   ├── reading-time.test.ts     # 10
│   │   ├── validate-source.test.ts  # 6 (NEW v2.1)
│   │   ├── active-section.test.ts   # 6 (NEW v2.1)
│   │   └── extract-title.test.ts    # 7 (NEW v2.1)
│   ├── integration/                 # 55 tests across 10 files
│   │   └── (same as v2.0)
│   ├── accessibility/
│   │   └── axe.test.ts              # 2 (Playwright)
│   └── performance/
│       └── bundle-size.test.ts      # 1
└── docs/
    ├── markdown-html-pipeline_SKILL-v2.1.md  # This file
    ├── markdown-html-pipeline_SKILL-v2.md    # v2.0 (superseded; banner at top)
    ├── markdown-html-pipeline_SKILL-v1.md    # v1.0 (archived)
    ├── original_SKILL.md                     # v4.1.1 base spec
    ├── audit/
    │   ├── AUDIT.md                          # v2.0 53-finding audit
    │   ├── IMPLEMENTATION_PLAN.md            # v2.0 10-phase plan
    │   ├── REMEDIATION_LOG.md                # v2.0 execution log
    │   ├── IMPLEMENTATION_PLAN_v2.1.md       # v2.1 outstanding-issues plan (NEW)
    │   └── REMEDIATION_LOG_v2.1.md           # v2.1 execution log (NEW)
    └── v2_rendering_comparison_3.md          # spec-vs-spec audit (v1 vs v2)
```

**File counts (v2.1):** 42 source files, 23 test files, 145 vitest tests + 2 Playwright tests = 147 total.

---

### §6 The Design System (Code-First)

The two-layer token pattern (Layer 1 runtime variables + Layer 2 `@theme inline` bridge) is the only correct way to do dark mode in Tailwind v4. **Never nest `@theme` inside `@media`** — it silently breaks.

#### 6.1 Technical template `src/templates/technical/theme.css`

(Same as v2.0 — see the file directly. Key points:)

- **Layer 1:** `:root` defines light-mode tokens. `@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { ... } }` flips them for system dark. `[data-theme="dark"] { ... }` flips them for manual override.
- **Layer 2:** `@theme inline` bridges the runtime variables into Tailwind utilities (`--color-bg: var(--bg)`, etc.).
- **Base:** `html { scroll-behavior: smooth; }` with `@media (prefers-reduced-motion: reduce)` guard. `body` uses `var(--font-sans)`. `:focus-visible` ring. `::selection` accent.
- **Print (§6.3):** force light tokens, hide chrome, append href after links, avoid page-breaks inside code/tables.

#### 6.2 Editorial template `src/templates/editorial/theme.css`

Same two-layer structure, different values — warm cream-and-ink palette (`--bg: #fdfbf7`, `--text: #1c1814`, `--accent: #8b4513`) suited to long-form reading. Uses `"Source Serif 4", "Georgia", ui-serif, serif` as `--font-sans`.

#### 6.3 Print stylesheet (both templates)

Both templates include a `@media print` block that:

1. **Forces light-mode color tokens** regardless of OS / user preference (paper is always light).
2. **Hides chrome**: `header`, `aside`, `[aria-label="Back to top"]`, `[aria-label="Open table of contents"]`, `[aria-label="Copy code"]` all get `display: none !important`.
3. **Expands content** to full width.
4. **Appends href after links** via `a[href]::after { content: " (" attr(href) ")"; }` so printed links are usable.
5. **Avoids page-breaks inside** `pre`, `table`, `figure`, `blockquote`.
6. **Avoids page-breaks after** headings (`h1`–`h6`).

#### 6.4 Color contrast verification

| Token | Hex | Background | Ratio | WCAG AA |
|-------|-----|------------|-------|---------|
| `--text` (technical, light) | `#0f172a` | `#ffffff` | 18.1:1 | ✅ AAA |
| `--text-secondary` (technical, light) | `#475569` | `#ffffff` | 5.9:1 | ✅ AA |
| `--text-tertiary` (technical, light) | `#475569` | `#ffffff` | 5.9:1 | ✅ AA |
| `--text` (technical, dark) | `#f8fafc` | `#0f172a` | 18.1:1 | ✅ AAA |
| `--text-secondary` (technical, dark) | `#cbd5e1` | `#0f172a` | 11.6:1 | ✅ AAA |
| `--text-tertiary` (technical, dark) | `#94a3b8` | `#0f172a` | 5.3:1 | ✅ AA |
| `--text` (editorial, light) | `#1c1814` | `#fdfbf7` | 16.2:1 | ✅ AAA |
| `--text-secondary` (editorial, light) | `#3a342c` | `#fdfbf7` | 9.1:1 | ✅ AAA |
| `--text-tertiary` (editorial, light) | `#5e5448` | `#fdfbf7` | 6.4:1 | ✅ AA |

#### 6.5 Typography hierarchy

| Role | Font | Weight | Size | Color |
|------|------|--------|------|-------|
| H1 (technical) | Inter | 700 | `text-3xl sm:text-4xl` | text |
| H2 (technical) | Inter | 600 | `text-2xl` | text |
| H3 (technical) | Inter | 600 | `text-xl` | text |
| H4 (technical) | Inter | 600 | `text-lg` | text-secondary |
| H1 (editorial) | Source Serif 4 | 700 | `text-4xl sm:text-5xl` | text |
| H2 (editorial) | Source Serif 4 | 700 | `text-3xl` | text |
| H3 (editorial) | Source Serif 4 | 600 | `text-2xl italic` | text |
| Body | Inter / Source Serif 4 | 400 | `text-base` (16px) | text-secondary |
| Code | JetBrains Mono | 400 | `text-sm` | text |
| Badge | Inter | 600 | `text-xs` uppercase | per-accent |

---

### §7 Component Architecture & Patterns

#### 7.1 The rendering pipeline (data flow)

```
┌─────────────────────────────────────────────────────────────────┐
│  src/content/document.md                                         │
│  (raw Markdown with optional YAML frontmatter)                   │
└──────────────────────────────┬──────────────────────────────────┘
                               │ import via ?raw
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│  parseDocument(markdown) → { frontmatter, body }                │
│  Strips YAML frontmatter block from body (BOM-safe, CRLF-safe)  │
└──────────────────────────────┬──────────────────────────────────┘
                               │
              ┌────────────────┼────────────────┬────────────────┬────────────────┐
              ▼                ▼                ▼                ▼                ▼
┌──────────────────┐ ┌─────────────────┐ ┌─────────────┐ ┌──────────────┐ ┌─────────────┐
│ enhanceMarkdown  │ │ buildToc        │ │ estimate    │ │ extractDoc   │ │ validate    │
│ (body, registry) │ │ (body, 4)       │ │ ReadingTime │ │ Title(md)    │ │ SourceDoc   │
│ → { enhanced,    │ │ → TocItem[]     │ │ (body)      │ │ → <title>    │ │ (md) → ok   │
│   warnings }     │ │                 │ │ → "N min"   │ │ (build-time) │ │ (lint:source│
└────────┬─────────┘ └────────┬────────┘ └─────────────┘ └──────────────┘ └─────────────┘
         │                    │
         ▼                    ▼
┌─────────────────────────────────────────────────────────────────┐
│  MarkdownRenderer                                               │
│  react-markdown( enhanced )                                     │
│    remarkPlugins: [remarkGfm]                                   │
│    rehypePlugins: [rehypeSlug]                                  │
│    components: { h2, h3, h4, a, code→Badge, img, input,         │
│                  pre→CodeBlockWrapper+CopyButton, ... }         │
└─────────────────────────────────────────────────────────────────┘
```

#### 7.2 Memoization strategy

Every derived value is memoized to prevent re-computation on re-render:

```typescript
// App.tsx — the memoization points
const { frontmatter, body } = useMemo(() => parseDocument(documentMd), []);
const registry = useMemo(() => loadRegistry(TAGS), []);
const enhanced = useMemo(() => enhanceMarkdown(body, registry), [body, registry]);
const toc = useMemo(() => buildToc(body, 4), [body]);
const readingTime = useMemo(() => estimateReadingTime(body), [body]);
```

> **Critical:** `buildToc` consumes `body` (not `enhanced`). The TOC doesn't need badge wrapping — only the rendered markdown does. This prevents the TOC from re-computing when the badge registry changes.

#### 7.3 Component inventory (10 components)

| Component | File | Purpose |
|-----------|------|---------|
| `MarkdownRenderer` | `MarkdownRenderer.tsx` | react-markdown renderer + components map + CodeBlockWrapper |
| `TableOfContents` | `TableOfContents.tsx` | Recursive TOC with active-section styling + `aria-label` |
| `Badge` | `Badge.tsx` | Tag-aware badge chip (5 accent steps) |
| `ErrorBoundary` | `ErrorBoundary.tsx` | Class component render error catcher (stores `errorInfo`) |
| `ErrorFallback` | `ErrorFallback.tsx` | Presentational fallback UI with reload button |
| `SkipLink` | `SkipLink.tsx` | Accessible skip-to-content link |
| `ThemeToggle` | `ThemeToggle.tsx` | Light/dark/system toggle (lucide icons + aria-live + matchMedia subscription) |
| `BackToTop` | `BackToTop.tsx` | Floating scroll-to-top button (respects reduced motion) |
| `MobileNav` | `MobileNav.tsx` | Mobile TOC drawer (dialog + focus trap + body scroll lock) |
| `CopyButton` | `CopyButton.tsx` | Clipboard copy with execCommand fallback |

---

### §8 Custom Hooks Deep Dive

**No custom hooks exist.** Theme state, drawer state, scroll state, clipboard state, and the active-section observer live inline in their respective components (`useState` / `useEffect` / `useMemo`). This is deliberate — document it explicitly so no agent searches for a `hooks/` directory.

The only reusable stateful logic is the `localStorage` wrapper in `src/utils/theme-storage.ts`, which is a pure utility (not a hook) because it doesn't use any React primitives.

**Why no hooks?** Each stateful concern is local to one component. Extracting a `useTheme` or `useActiveSection` hook would add a layer of indirection without enabling reuse. The active-section *logic* is extracted into `src/lib/active-section.ts` as a pure reducer (not a hook) so it can be unit-tested without rendering React.

---

### §9 Content Management & Data Ingestion

#### 9.1 Markdown content

- **Location:** `src/content/document.md`
- **Import mechanism:** Vite `?raw` suffix imports the file as a string: `import documentMd from "@/content/document.md?raw";`
- **Frontmatter:** Optional YAML block at the top. Parsed by `parseDocument()` which returns `{ frontmatter, body }`. The frontmatter block is **stripped** from the body before rendering.
- **Supported features:** Headings H1–H6, tables (GFM), links, inline code, fenced code blocks, blockquotes, lists, task lists, horizontal rules, images, YAML frontmatter.
- **Not supported:** Footnotes, math, Mermaid, raw HTML pass-through, multi-document sets.

#### 9.2 Source-document validation (NEW in v2.1)

`validateSourceDocument(markdown)` in `src/lib/validate-source.ts` parses the markdown and asserts:

1. `introCount` (the N in `**N skills**`) matches `actualRows` (count of `| **name** |` rows).
2. Each per-category summary row matches the actual row count for that section.
3. The summary table's `**Total**` row matches the sum of per-category rows.
4. The summary table's `**Total**` row matches `introCount`.

Returns `{ ok, errors, introCount, summaryTotal, summarySum, actualRows }`. Used by:

- `scripts/validate-source.mjs` — CLI invoked by `npm run lint:source` (Gate 0).
- `tests/unit/validate-source.test.ts` — 6 unit tests covering consistent / intro-wrong / summary-wrong / total-missing / no-intro cases.

The validator is intentionally tolerant: if there's no intro claim, it skips the intro check; if there's no summary table, it skips summary checks. It only fails when the document *has* the structure and the structure is internally inconsistent.

#### 9.3 Reading-time estimation (UPDATED in v2.1)

`estimateReadingTime(body)` returns a string like `"5 min read"`. The estimator:

1. Strips fenced code blocks (via `scanLines` — code is read slower, not as prose words).
2. Strips markdown syntax (headers, bold, italic, links, images, list markers, blockquotes, horizontal rules, HTML tags).
3. Counts Latin words (sequences of Latin letters/digits/apostrophes).
4. Counts CJK characters individually (each CJK char = 1 word).
5. Computes `latinMinutes = ceil(latinCount / 200)` and `cjkMinutes = ceil(cjkCount / 300)`.
6. Returns `max(1, latinMinutes, cjkMinutes)` as the reading time.

**Why two rates?** Native Chinese reading speed is ~250–300 characters per minute for prose, while English is ~200 wpm. Under v2.0's single 200-wpm rate, a 900-character Chinese document estimated 5 min read but actually took ~3 min — an overestimate that made the reading-time feature misleading for CJK-heavy content. The v2.1 fix uses a separate 300 cpm rate for CJK and takes the max of the two estimates (so a mixed Latin+CJK document doesn't double-count).

```typescript
const LATIN_WORDS_PER_MINUTE = 200;
const CJK_CHARS_PER_MINUTE = 300;

// ...
const latinMinutes = Math.ceil(latinCount / LATIN_WORDS_PER_MINUTE);
const cjkMinutes = Math.ceil(cjkCount / CJK_CHARS_PER_MINUTE);
const minutes = Math.max(1, latinMinutes, cjkMinutes);
return `${minutes} min read`;
```

#### 9.4 Build-time document-title extraction (NEW in v2.1)

`extractDocumentTitle(markdown)` in `src/lib/extract-title.ts` returns the document title for use as `<title>` in `index.html`. Priority:

1. Frontmatter `title:` field (if present and non-empty).
2. First non-fenced ATX H1 in the body.
3. `null` — caller falls back to a default.

Markdown emphasis (`**bold**`, `_italic_`) is stripped from H1 text so the browser tab title reads as plain text. Fenced code blocks are skipped so a `# comment` line inside a code fence is not mistaken for a heading.

Used by the `documentTitlePlugin` in `vite.config.ts` (a `transformIndexHtml` hook) to rewrite the static `<title>` at build time. This eliminates the pre-hydration flash of the wrong title that the runtime `useEffect` in `App.tsx` cannot prevent — the static HTML now ships with the correct title, and the `useEffect` only needs to handle the edge case where frontmatter changes after hydration (which doesn't happen in practice for a static markdown import).

#### 9.5 Adding new content

1. Replace `src/content/document.md` with any markdown file.
2. Run `npm run lint:source` — if the document has an intro claim + summary table, the gate asserts they agree.
3. Run `npm run build` — the pipeline handles frontmatter, tables, headings, images, task lists, code blocks, reading time, and `<title>` injection automatically.
4. If the content uses badge annotations (`**Tag:** value`), add the tag to the active template's `tags.json`.

---

### §10 Accessibility (WCAG 2.2 AA) Implementation

#### 10.1 Conformance claim

**WCAG 2.2 AA, enforced by an automated axe gate.** The gate runs in both light and dark modes. Zero `color-contrast`, `target-size`, or other AA violations are allowed.

#### 10.2 Implementation matrix

| Feature | Implementation | Verification |
|---------|----------------|--------------|
| Skip-to-content | `<a href="#content">` with `sr-only focus:not-sr-only focus:z-50` | Manual: Tab → Enter → focus lands |
| Focus visible | Global `:focus-visible` ring (2px accent outline) | Manual Tab pass |
| Heading hierarchy | H1 → H2 → H3 → H4, no skipped levels | axe `heading-order` |
| Reduced motion | `prefers-reduced-motion` guard in base styles; `BackToTop` uses instant scroll | Manual OS setting check |
| Touch targets | All interactive elements ≥ 44×44px (`min-h-11 min-w-11`) | axe `target-size` |
| ARIA | `aria-label` on nav/toggle/drawer/copy button; `aria-hidden` on decorative icons; `aria-live` on theme announcements | axe `aria-valid-attr` |
| Landmarks | `header`, `main`, `nav`, `article` | axe `region` |
| Color contrast | All text tokens ≥ 4.5:1 on their backgrounds | axe `color-contrast` |
| Keyboard | Full Tab/Shift+Tab operability; drawer closes on Escape; focus trap while open | Manual |
| Language | `<html lang="en">` | axe `html-has-lang` |
| Mobile drawer | `role="dialog"` + `aria-modal="true"` + `aria-label`; closes on Escape / link click / backdrop click; focus moves to close button on open, back to trigger on close; body scroll locked while open | Manual + axe |
| Theme announcements | Visually-hidden `aria-live="polite"` region announces "Theme changed to {theme}" | Manual screen reader pass |
| Code copy buttons | `aria-label` reflects state ("Copy code" vs "Copied!"); `aria-live="polite"` for state change | Manual + axe |
| Back-to-top | `aria-hidden` and `tabIndex` reflect visibility; `aria-label="Back to top"` | Manual + axe |
| Task list checkboxes | `disabled` + `readOnly` (not toggleable); `aria-label="Task list item"` | axe |
| Images | `loading="lazy"` + `decoding="async"` + alt text (empty string if decorative) | axe `image-alt` |

#### 10.3 The accessibility test

```typescript
// tests/accessibility/axe.test.ts
import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

test("document passes WCAG 2.2 AA (hard gate)", async ({ page }) => {
  await page.goto("/");
  const results = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa", "wcag22aa"])
    .analyze();
  expect(results.violations).toEqual([]);
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

> **Run with:** `npx playwright test` (NOT `npm run test` — vitest can't run Playwright tests).

---

### §11 The Configuration Surface

The configuration surface is **frontmatter (§3.1) + template choice + tag registry**. There is **no** `defineConfig` helper, no `virtual:` module, no build-time config-object plugin.

The `MarkdownToWebConfig` type is included for teams that want to build their own config helper. v2 provides `resolveConfig(input: unknown): MarkdownToWebConfig` — a validator that throws on invalid fields. This is the team-extension surface; the base pipeline does not require it.

---

### §12 Template System

#### 12.1 Template switching mechanism

The `src/templates/active.ts` file is the **only** place to edit when switching templates:

```typescript
import "@/templates/technical/theme.css";
import { technicalComponents } from "@/templates/technical/components";
import { TechnicalLayout } from "@/templates/technical/layout";
import tagsJson from "@/templates/technical/tags.json";

export const TEMPLATE_NAME = "technical" as const;
export const TAGS: TagRegistry = tagsJson as TagRegistry;
export const TEMPLATE_COMPONENTS = technicalComponents;
export const TemplateLayout: FC<TemplateLayoutProps> = TechnicalLayout;
```

To switch to editorial, change the four import paths and `TEMPLATE_NAME`.

#### 12.2 Known trade-off: inactive template's utility CSS leaks (NEW in v2.1, documented)

When the `technical` template is active, Tailwind v4's content scanner still sees `text-5xl` (used by `editorial/layout.tsx` line 45) and generates the CSS rule (~1–2 KB). Editorial color tokens (`--bg`, `--accent`, etc.) do NOT leak — only utility class definitions do.

**Why not exclude `editorial/**` from the Tailwind scan?** That would break template switching — the moment someone changes `active.ts` to editorial, the build would silently produce a broken page with no `text-5xl` rule.

**Accepted resolution:** Document the trade-off. The ~1–2 KB overhead is the cost of single-file portability with swappable templates. If a future version needs to eliminate it, the path is dynamic-importing the active template's `theme.css` (so the other isn't bundled), but that requires `cssCodeSplit: true` which conflicts with `vite-plugin-singlefile`.

---

### §13 Quality Gates (9 gates, all real)

v2.0 documented 8 gates. v2.1 adds Gate 0 (`lint:source`) and renumbers.

#### 13.1 The 9 gates

```bash
# Gate 0: Source-markdown internal consistency (NEW in v2.1)
npm run lint:source      # node scripts/validate-source.mjs
# Asserts: intro count == sum of summary rows == count of | **name** | rows

# Gate 1: Typecheck (strict, noUnusedLocals/Parameters/noUncheckedIndexedAccess)
npm run typecheck        # tsc --noEmit

# Gate 2: Lint (ESLint flat config, zero-warning policy)
npm run lint             # eslint . --max-warnings 0

# Gate 3: Format (Prettier check)
npm run lint:format      # prettier --check .

# Gate 4: Markdown lint (markdownlint-cli2)
npm run lint:markdown    # markdownlint-cli2

# Gate 5: Tests (unit + integration + bundle-size)
npm run test             # vitest run

# Gate 6: Coverage (enforces 80/75/80/80 thresholds)
npm run test:coverage    # vitest run --coverage

# Gate 7: Production build
npm run build            # vite build → dist/index.html

# Gate 8: Bundle size (dist/index.html < 250 KB gzipped)
npm run test:bundle-size # vitest run tests/performance

# Gate 9: Accessibility (axe-core via Playwright, light + dark)
npm run a11y             # playwright test (requires `npx playwright install chromium` first)
```

#### 13.2 CI workflow (`.github/workflows/ci.yml`)

Two jobs run on every push and PR to `main`/`master`:

- **quality**: Node 22, `npm ci`, lint:source → typecheck → lint → lint:format → lint:markdown → test:coverage → build → test:bundle-size. Uploads coverage + dist artifacts.
- **accessibility**: Node 22, `npm ci`, build, `npx playwright install chromium --with-deps`, `npm run a11y`. Uploads Playwright report.

#### 13.3 Pre-commit hook (`.husky/pre-commit`)

Runs `npx lint-staged` (ESLint --fix + Prettier --write + markdownlint --fix on staged files) followed by `npm run typecheck`. A failure blocks the commit.

> **Per project policy, no guardrail is weakened to make a commit pass — fix the cause, not the symptom.**

#### 13.4 Coverage thresholds

```typescript
// vitest.config.ts
coverage: {
  thresholds: { lines: 80, functions: 80, branches: 75, statements: 80 },
},
```

v2.1 actual coverage: 89.84% lines / 81.15% branches / 85.84% functions / 91.8% statements — all above thresholds (improved from v2.0's 87.5% / 77.11% / 85.32% / 90.09%).

---

### §14 Anti-Patterns & Common Bugs

#### 14.1 The original 12 anti-patterns (from v1.0.0, still apply)

| # | Anti-Pattern | Symptom | Root Cause | Fix |
|---|---|---|---|---|
| 1 | Nesting `@theme` inside `@media` | Dark mode silently fails | `@theme` is build-time, top-level only | Variable-flip pattern (§6) |
| 2 | `dangerouslySetInnerHTML` for markdown | XSS surface, dual pipelines | HTML-string architecture | Use the components map |
| 3 | `import { slug } from "github-slugger"` | Build error | No named export exists | `import GithubSlugger from "github-slugger"` |
| 4 | Using `baseUrl` in TS 6 tsconfig | Hard error: "Option baseUrl is deprecated" | TS 6 deprecation | Remove `baseUrl`; use `paths` with `./` prefix |
| 5 | Forgetting `jsdom` for vitest | "Cannot find package 'jsdom'" | jsdom not bundled with vitest | `npm install -D jsdom` |
| 6 | Running Playwright tests under vitest | "calling test() from async test.describe()" | Wrong runner | `npx playwright test` for accessibility |
| 7 | Not installing Playwright browsers | "Executable doesn't exist" | Browsers not bundled | `npx playwright install chromium` |
| 8 | Badge test registry with collisions | Wrong tag assigned | `resolveBadge` returns first match | Unique values across registry |
| 9 | Testing slug parity with untrimmed fixtures | Whitespace mismatch | `buildToc` trims heading text | Compare against `slugger.slug(text.trim())` |
| 10 | `--text-tertiary` too light for AA | 2.56:1 contrast failure | Default slate-400 too bright | Darken to slate-600 (`#475569`) |
| 11 | Using exact-pinned deps without checking Vite 8 compatibility | Peer dependency conflicts | Pinned versions predate Vite 8 | Check peer ranges; use latest patch |
| 12 | `noUncheckedIndexedAccess` without null checks | `TocItem possibly undefined` | Strict array access | Use optional chaining (`toc[0]?.slug`) |

#### 14.2 v2.0 anti-patterns (13, still apply)

| # | Anti-Pattern | Symptom | Root Cause | Fix |
|---|---|---|---|---|
| 13 | Missing `eslint.config.js` | `npm run lint` errors | ESLint 9 requires flat config | Create `eslint.config.js` |
| 14 | Missing `.prettierrc.json` | `npm run lint:format` fails | No Prettier config | Create `.prettierrc.json` + `.prettierignore` |
| 15 | Missing `.markdownlint-cli2.jsonc` | `npm run lint:markdown` errors | v0.14+ needs its own format | Create `.markdownlint-cli2.jsonc` with `config` + `globs` |
| 16 | Dead types | Misleading API surface | Type defined but never imported | Either delete or consume |
| 17 | Duplicate type definitions | Risk of drift | Copy-paste | `types/` is canonical; `lib/` imports + re-exports |
| 18 | Orphaned tsconfig files | Misleading structure | Vite scaffold generated them | Delete or wire `references` |
| 19 | Tracked build artifacts | Repo bloat | Committed before `.gitignore` | `git rm -r --cached dist test-results` |
| 20 | Orphaned config files | Misleading | Tool considered then dropped | Delete the config |
| 21 | Emoji icons instead of SVG | Inconsistent rendering | Quick-and-dirty impl | Use `lucide-react` SVG icons |
| 22 | Missing system-theme subscription | OS theme change doesn't update | No `matchMedia` listener | Add `useEffect` subscribing to `change` events |
| 23 | Missing `img` component override | No lazy loading | Components map gap | Add `img` override with `loading="lazy"` |
| 24 | Missing `input` component override | Task list checkboxes toggleable | Default `<input>` is interactive | Add `input` override with `disabled` + `readOnly` |
| 25 | `ErrorBoundary` function fallback loses `errorInfo` | Passes `{} as ErrorInfo` | `componentDidCatch` discarded it | Store `errorInfo` in state |

#### 14.3 v2.1 anti-patterns (5 new)

| # | Anti-Pattern | Symptom | Root Cause | Fix |
|---|---|---|---|---|
| 26 | **Source-markdown count mismatch undetected** | Intro says N, summary totals M, actual rows K — all three rendered | No gate validates source-document internal consistency | Add `lint:source` gate (§13) with `validateSourceDocument()` (§9.2). The 198/208/202 mismatch persisted across v1→v2.0 because no gate checked. |
| 27 | **`IntersectionObserver` partial-callback bug** | Active section flickers / clears while section is visible | `entries.every(!isIntersecting)` assumes `entries` is the full observed set; it's only the *changed* entries | Maintain a `Map<id, boolean>` of visibility state; derive `activeSlug` from the map. See `src/lib/active-section.ts`. |
| 28 | **Single reading rate for mixed scripts** | CJK content reading-time overestimated by ~25% | Latin 200 wpm applied to CJK chars, which are read slower per char | Separate rates: Latin 200 wpm, CJK 300 cpm. Take `max(latinMinutes, cjkMinutes)` to avoid double-counting. See `src/lib/reading-time.ts`. |
| 29 | **Pre-hydration `<title>` flash** | Browser tab shows static "Skills Catalog" until React hydrates | `index.html` title hardcoded; runtime `useEffect` can't fire before hydration | Build-time `transformIndexHtml` plugin reads the markdown and rewrites `<title>` before the HTML is emitted. See `vite.config.ts` `documentTitlePlugin`. |
| 30 | **Redundant `inlineDynamicImports` build warning** | `WARN inlineDynamicImports option is ignored because codeSplitting: false is set.` | `vite-plugin-singlefile` sets the option; Vite 8 ignores it when `cssCodeSplit: false` | Remove `rollupOptions.output.inlineDynamicImports` from `vite.config.ts`. `cssCodeSplit: false` + `vite-plugin-singlefile` already enforce single-file output. |

---

### §15 Debugging Guide

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Cannot find module 'jsdom'` | jsdom not installed | `npm install -D jsdom` |
| `Option baseUrl is deprecated` | TS 6 deprecation | Remove from tsconfig; use `paths` |
| `peer vite@"^5\|^6\|^7"` conflict | Plugin predates Vite 8 | Use `@tailwindcss/vite@4.3.3+`, `vite-plugin-singlefile@2.3.3+` |
| `Executable doesn't exist` (Playwright) | Browsers not installed | `npx playwright install chromium` |
| Badge renders as plain `<code>` | Markdown not run through `enhanceMarkdown` | Pipeline: `enhanceMarkdown` → `MarkdownRenderer` |
| `getByLabelText` finds wrong badge | Value collision across tags | Ensure unique values in registry |
| Slug parity test fails on whitespace | `buildToc` trims heading text | Compare against `slugger.slug(text.trim())` |
| `color-contrast` AA violation on tertiary text | Text token too light | Darken token (§6.4) |
| Dark mode doesn't apply on toggle | `data-theme` not set on `<html>` | `document.documentElement.setAttribute("data-theme", "dark")` |
| `Property 'env' does not exist on type 'ImportMeta'` | Missing Vite client types | `/// <reference types="vite/client" />` |
| `Cannot find name 'fs'/'path'/'process'` in tests | Missing `@types/node` | `npm install -D @types/node` |
| Build exceeds 250 KB gzipped | Large markdown or un-tree-shaken icons | Subset lucide-react imports; check bundle |
| `ESLint couldn't find an eslint.config.(js\|mjs\|cjs) file` | Missing `eslint.config.js` | Create it at repo root |
| `npm run lint:format` fails on N files | Missing `.prettierrc.json` or drift | Create config; run `npx prettier --write .` |
| `npm run lint:markdown` prints usage and exits | Missing `.markdownlint-cli2.jsonc` | Create with `config` + `globs` keys |
| Prettier drift after `eslint --fix` | Autofixers drift the formatter | Run `prettier --write` AFTER `eslint --fix` (lint-staged orders this) |
| `__dirname` deprecation warning in Vite 8 | Vite 8 deprecates `__dirname` | Use `import.meta.dirname` |
| `IntersectionObserver is not defined` in vitest | jsdom doesn't implement it | Mock in `tests/setup.ts` |
| `matchMedia is not a function` in vitest | jsdom doesn't implement it | Mock in `tests/setup.ts` |
| `navigator.clipboard is undefined` in insecure context | Clipboard API requires HTTPS | Use `document.execCommand("copy")` fallback |
| GFM task list checkboxes toggleable | Default `<input>` is interactive | Add `input` override with `disabled` + `readOnly` |
| Theme toggle doesn't update when OS theme changes | No `matchMedia` change listener | Add `useEffect` subscribing to `change` events |
| `document.title` doesn't reflect frontmatter | `index.html` title hardcoded | Build-time `documentTitlePlugin` + runtime `useEffect` (§9.4) |
| TOC highlights a section the user scrolled past (intermittent) | Partial `IntersectionObserver` callback | Use `Map<id, boolean>` reducer (§9.4, `src/lib/active-section.ts`) |
| **`lint:source` fails with "Intro claim (N) does not match actual row count (M)"** (NEW v2.1) | Source markdown's intro count disagrees with actual `| **name** |` rows | Fix the intro claim OR add/remove rows so they agree |
| **`lint:source` fails with "Category N: summary count (X) does not match actual rows (Y)"** (NEW v2.1) | Summary table's per-category count disagrees with actual rows | Fix the summary table row to match the actual count |
| **`lint:source` fails with "Summary table is missing the Total row"** (NEW v2.1) | No `\| \| **Total** \| **N** \|` row in the summary table | Add the Total row with the correct sum |
| **Build warning: `inlineDynamicImports option is ignored`** (FIXED v2.1) | `vite.config.ts` had redundant `rollupOptions.output.inlineDynamicImports` | Remove the option (already done in v2.1) |

---

### §16 Pre-Ship Checklist

Run in order. All must pass.

```bash
# Gate 0: Source-markdown internal consistency (NEW v2.1)
npm run lint:source

# Gate 1: Typecheck
npm run typecheck

# Gate 2: Lint
npm run lint

# Gate 3: Format
npm run lint:format

# Gate 4: Markdown lint
npm run lint:markdown

# Gate 5: Tests
npm run test

# Gate 6: Coverage
npm run test:coverage

# Gate 7: Production build
npm run build
# Verify: dist/index.html exists, JS/CSS inlined, < 250 KB gzipped, no warnings

# Gate 8: Bundle size
npm run test:bundle-size

# Gate 9: Accessibility (requires one-time browser install)
npm run a11y

# Gate V-1: Verify dependency versions
npm ls --depth=0
```

**Test counts (v2.1, verified):**

| Suite | Count |
|-------|-------|
| Unit | 89 (fence: 5, enhance: 10, toc: 9, frontmatter: 7, tags: 6, slug-parity: 9, config: 14, reading-time: 10, validate-source: 6, active-section: 6, extract-title: 7) |
| Integration | 55 (across 10 files) |
| Accessibility | 2 (Playwright) |
| Performance | 1 (bundle-size) |
| **Total** | **145 vitest + 2 Playwright = 147** |

**Build output:** `dist/index.html` — 600.19 kB raw, 171.40 kB gzipped (78.6 kB under the 250 kB budget).

---

### §17 Lessons Learnt & How to Avoid Them

#### Lessons 1–24 (from v1.0.0 and v2.0 — summarized, see v2.0 spec for full text)

1. Vite 8 requires updated plugin versions.
2. TypeScript 6 deprecates `baseUrl`.
3. `jsdom` must be explicitly installed for vitest.
4. The badge pipeline requires `enhanceMarkdown` BEFORE `MarkdownRenderer`.
5. Badge test registries must have unique values across tags.
6. `buildToc` trims heading text before slugging.
7. Playwright browsers must be explicitly installed.
8. The `--text-tertiary` token was too light for WCAG AA.
9. Playwright tests must run under Playwright, not vitest.
10. `@types/node` is required for Node.js APIs in test files.
11. A documented gate that doesn't run is worse than no gate.
12. Dead types mislead maintainers.
13. Duplicate type definitions drift.
14. Orphaned config files silently rot.
15. Emojis render inconsistently across platforms.
16. System theme changes don't fire React state updates without a `matchMedia` listener.
17. GFM task list checkboxes are interactive by default — disable them.
18. `ErrorBoundary` function fallbacks lose `errorInfo` without explicit storage.
19. `IntersectionObserver` only fires on positive intersection — clear state explicitly. *(Updated in v2.1 — see Lesson 25 for the partial-callback refinement.)*
20. `document.title` is not reactive — sync it via `useEffect`.
21. `navigator.clipboard` is unavailable in insecure contexts — keep the `execCommand` fallback.
22. jsdom doesn't implement `IntersectionObserver` or `matchMedia` — mock them in `tests/setup.ts`.
23. `markdownlint-cli2` v0.14+ requires its own config format with explicit globs.
24. The `__dirname` deprecation in Vite 8 — use `import.meta.dirname`.

#### Lessons 25–29 (NEW in v2.1)

**Lesson 25: `IntersectionObserver` callbacks fire with partial entry lists — track state across callbacks.**

v2.0's Lesson 19 said "clear `activeSlug` when every observed entry reports `!isIntersecting`." That's correct in spirit but wrong in implementation: the `entries` array passed to the callback contains only the entries whose intersection state *changed* since the last callback, not every observed element. So `entries.every((e) => !e.isIntersecting)` can be true even when other (unchanged) entries are still intersecting — causing `activeSlug` to incorrectly clear.

*Fix:* Maintain a `Map<string, boolean>` of element-id → isIntersecting. Update it on every callback from the incoming `entries`. Derive `activeSlug` as the first entry in the map with `true`. This is a pure function (`reduceActiveSlug` in `src/lib/active-section.ts`) that can be unit-tested without rendering React.

*Why this matters:* On a long page with many sections, the active-section highlight would occasionally flicker or jump to the wrong section when the user scrolled quickly. The fix is invisible to users but eliminates a real UX defect.

**Lesson 26: Source-data defects persist when no gate checks source data.**

The 198/208/202 count mismatch in the skills catalog persisted across v1→v2.0 — two full remediation rounds — because no gate validated the source markdown's internal consistency. Every gate checked rendered output or code quality, but the source markdown was treated as an opaque input.

*Fix:* Add a `lint:source` gate that parses the source markdown and asserts `intro_count == sum(summary_rows) == count(actual_rows)`. The gate is intentionally tolerant — it only fires when the document *has* the structure (intro claim + summary table) and the structure is inconsistent.

*Why this matters:* For a catalog whose primary purpose is enumeration, three different totals in the same document erode reader trust. The gate prevents recurrence; the source fix (correcting the summary table) closes the existing defect.

**Lesson 27: Reading-speed estimators must account for script differences.**

v2.0's `estimateReadingTime` used a single 200 wpm rate for both Latin words and CJK characters. This overestimated CJK reading time by ~25% (native Chinese reading speed is ~250–300 chars/min, not 200). A 900-character Chinese document estimated 5 min read but actually took ~3 min.

*Fix:* Use separate rates: `LATIN_WORDS_PER_MINUTE = 200`, `CJK_CHARS_PER_MINUTE = 300`. Compute `latinMinutes` and `cjkMinutes` independently. Take `max(1, latinMinutes, cjkMinutes)` — the max (not the sum) avoids double-counting mixed-script content (a 1000-word English doc with a 100-char Chinese appendix reads as 5 min, not 5.5 min).

*Why this matters:* Reading-time estimates are a UX feature. An estimate that's 25% off for a quarter of the world's languages is a real defect, not a cosmetic one.

**Lesson 28: Build-time fixes can eliminate runtime work — prefer them when the data is static.**

v2.0's `App.tsx` had a `useEffect` that synced `document.title` from frontmatter after hydration. This was correct but incomplete: the static `<title>` in `index.html` ("Skills Catalog") flashed in the browser tab and bookmarks before React hydrated. For the skills catalog itself this was harmless (the static title happened to match), but for any other document it would be wrong.

*Fix:* Add a `transformIndexHtml` Vite plugin that reads the markdown source, extracts the title (frontmatter `title:` or first H1), and rewrites `<title>` at build time. The runtime `useEffect` stays as a safety net for the edge case where frontmatter changes after hydration (which doesn't happen for a static `?raw` import, but the safety net is cheap).

*Why this matters:* The build-time fix is strictly better than the runtime fix — it produces correct HTML on first paint, requires no JavaScript to run, and works for crawlers and screen readers that don't execute JS. The general principle: when the data is static (known at build time), fix it at build time.

**Lesson 29: Redundant config options generate noise — remove them, don't silence them.**

v2.0's `vite.config.ts` had `build.rollupOptions.output.inlineDynamicImports: true`, which `vite-plugin-singlefile` sets. Vite 8 emits a warning: *"inlineDynamicImports option is ignored because codeSplitting: false is set."* The option is redundant — `cssCodeSplit: false` + `vite-plugin-singlefile` already enforce single-file output.

*Fix:* Remove the redundant `rollupOptions.output.inlineDynamicImports` from `vite.config.ts`. The warning disappears. The build output is unchanged (single-file, inlined).

*Why this matters:* Build warnings are noise that desensitizes developers to real problems. A green build with zero warnings is a signal that everything is intentional. A green build with N warnings is a signal that someone stopped reading the output.

---

### §18 Pitfalls to Avoid (v2.1 additions)

(Items 1–24 from v2.0 still apply. New in v2.1:)

25. **Don't trust `IntersectionObserver` callbacks to contain every observed element.** (NEW v2.1) They contain only *changed* entries. Track per-element state in a `Map` and derive the active slug from the map.
26. **Don't apply a single reading rate to mixed-script content.** (NEW v2.1) Latin and CJK have different per-unit reading speeds. Use separate rates and take the max.
27. **Don't rely on runtime `useEffect` to fix static HTML.** (NEW v2.1) If the data is known at build time, fix it at build time. Use `transformIndexHtml` for `<title>`, meta tags, etc.
28. **Don't keep redundant config options that generate warnings.** (NEW v2.1) Remove them. A warning that's "expected" is still noise.
29. **Don't lint reference/audit docs as if they were source.** (NEW v2.1) `docs/original_SKILL.md`, `docs/v2_rendering_comparison*.md`, etc. are archived artifacts. Exclude them from markdownlint via `.markdownlint-cli2.jsonc` globs. Linting them produces hundreds of errors that can't be fixed without rewriting the archive.

---

### §19 Best Practices (v2.1 additions)

(Items from v2.0 still apply. New in v2.1:)

- **Validate source data at build time.** If the source has internal structure (counts, cross-references, schema), add a gate that checks it. A renderer that faithfully pipes source defects to output is not "correct" — it's a defect multiplier.
- **Extract impure callback logic into pure functions.** The `IntersectionObserver` callback in `App.tsx` was hard to test because it was inline React state logic. Extracting `reduceActiveSlug(state, entries) → string` into `src/lib/active-section.ts` made it unit-testable without rendering React, without a DOM, and without a mock observer.
- **Prefer build-time fixes over runtime fixes for static data.** The `<title>` is known at build time. Fixing it at build time eliminates the pre-hydration flash and works without JavaScript.
- **Document accepted trade-offs explicitly.** The `text-5xl` CSS leak (§12.2) is a trade-off of single-file portability. Documenting it as a known limitation is better than silently accepting it or fragile-excluding it from the scan.

---

### §20 Coding Patterns (v2.1 additions)

#### Pattern 16: Stateful IntersectionObserver reducer (NEW in v2.1)

```typescript
// src/lib/active-section.ts
export interface CallbackEntry {
  target: { id: string };
  isIntersecting: boolean;
}

export function reduceActiveSlug(
  state: Map<string, boolean>,
  entries: CallbackEntry[],
): string {
  // Apply incoming deltas to the visibility map.
  for (const entry of entries) {
    state.set(entry.target.id, entry.isIntersecting);
  }
  // Derive the active slug from the map's current state.
  for (const [id, visible] of state) {
    if (visible) return id;
  }
  return "";
}
```

```typescript
// src/App.tsx — usage
const visible = new Map<string, boolean>();
const observer = new IntersectionObserver(
  (entries) => {
    const next = reduceActiveSlug(
      visible,
      entries.map((e) => ({
        target: { id: e.target.id },
        isIntersecting: e.isIntersecting,
      })),
    );
    setActiveSlug(next);
  },
  { rootMargin: "-80px 0px -80% 0px" },
);
```

#### Pattern 17: Build-time `transformIndexHtml` plugin (NEW in v2.1)

```typescript
// vite.config.ts
function documentTitlePlugin(): Plugin {
  const docPath = resolve(import.meta.dirname, "src", "content", "document.md");
  return {
    name: "markdown-to-web:document-title",
    transformIndexHtml(html: string) {
      let title: string | null = null;
      try {
        const md = readFileSync(docPath, "utf8");
        title = extractTitleFromMarkdown(md);
      } catch {
        // Markdown not readable — leave static title alone.
      }
      if (!title) return html;
      return html.replace(/<title>[^<]*<\/title>/, `<title>${escapeHtml(title)}</title>`);
    },
  };
}
```

#### Pattern 18: Source-document validator (NEW in v2.1)

```typescript
// src/lib/validate-source.ts
export function validateSourceDocument(markdown: string): ValidationResult {
  const errors: string[] = [];
  const introCount = /* parse **N skills** */;
  const { perCategory, summaryTotal, summarySum } = /* parse summary table */;
  const actualRows = /* count | **name** | rows per ## n. section */;

  if (introCount !== null && introCount !== actualRows) {
    errors.push(`Intro claim (${introCount}) does not match actual row count (${actualRows}).`);
  }
  // ... per-category, summary-total checks ...
  return { ok: errors.length === 0, errors, introCount, summaryTotal, summarySum, actualRows };
}
```

#### Pattern 19: Dual-rate reading-time estimator (NEW in v2.1)

```typescript
// src/lib/reading-time.ts
const LATIN_WORDS_PER_MINUTE = 200;
const CJK_CHARS_PER_MINUTE = 300;

const latinMinutes = Math.ceil(latinCount / LATIN_WORDS_PER_MINUTE);
const cjkMinutes = Math.ceil(cjkCount / CJK_CHARS_PER_MINUTE);
const minutes = Math.max(1, latinMinutes, cjkMinutes);
return `${minutes} min read`;
```

---

### §21 Coding Anti-Patterns (v2.1 additions)

#### ❌ Partial-callback `IntersectionObserver` logic (NEW v2.1)

```typescript
// WRONG — entries only contains CHANGED entries, not all observed
if (entries.length > 0 && entries.every((e) => !e.isIntersecting)) {
  setActiveSlug("");
  return;
}

// CORRECT — track per-element state in a Map; derive active from the map
const next = reduceActiveSlug(visible, entries);
setActiveSlug(next);
```

#### ❌ Single reading rate for mixed scripts (NEW v2.1)

```typescript
// WRONG — CJK overestimated by ~25%
const totalWords = latinCount + cjkCount;
const minutes = Math.ceil(totalWords / 200);

// CORRECT — separate rates; max avoids double-counting
const latinMinutes = Math.ceil(latinCount / 200);
const cjkMinutes = Math.ceil(cjkCount / 300);
const minutes = Math.max(1, latinMinutes, cjkMinutes);
```

#### ❌ Runtime-only fix for static HTML (NEW v2.1)

```typescript
// WRONG — flashes static title before hydration
// index.html: <title>Skills Catalog</title>
// App.tsx: useEffect(() => { document.title = frontmatter.title ?? "Skills Catalog"; }, []);

// CORRECT — build-time fix + runtime safety net
// vite.config.ts: documentTitlePlugin() rewrites <title> at build time
// App.tsx: useEffect stays as a safety net (cheap, handles edge case)
```

---

### §22 Responsive Breakpoint Reference

(Same as v2.0.)

| Breakpoint | Min Width | Usage |
|------------|-----------|-------|
| `sm` | 640px | H1 sizing; meta line subtitle visibility |
| `md` | 768px | (unused) |
| `lg` | 1024px | TOC sidebar appears; mobile nav hamburger hides |
| `xl` | 1280px | Right "on this page" outline appears (technical only) |
| `2xl` | 1536px | (unused) |

---

### §23 Z-Index Layer Map

(Same as v2.0.)

| z-index | Element | Purpose | File |
|---------|---------|---------|------|
| `z-50` | Skip-to-content link (focused) | Topmost | `SkipLink.tsx` |
| `z-50` | MobileNav drawer + backdrop | Above sticky header when open | `MobileNav.tsx` |
| `z-40` | Sticky header | Above content, below drawer | `layout.tsx` |
| `z-30` | BackToTop button | Above content, below header | `BackToTop.tsx` |
| `z-10` | CopyButton inside CodeBlockWrapper | Above `<pre>` content | `MarkdownRenderer.tsx` |

---

### §24 Color Reference (Complete)

(Same as v2.0 — see `src/templates/{technical,editorial}/theme.css` for the canonical source. The full tables are in v2.0 §24.)

---

### §25 The Complete TypeScript Interface Reference

(Same as v2.0, plus:)

#### `src/lib/active-section.ts` (NEW v2.1)

```typescript
export interface CallbackEntry {
  target: { id: string };
  isIntersecting: boolean;
}

export function reduceActiveSlug(
  state: Map<string, boolean>,
  entries: CallbackEntry[],
): string;
```

#### `src/lib/validate-source.ts` (NEW v2.1)

```typescript
export interface ValidationResult {
  ok: boolean;
  errors: string[];
  introCount: number | null;
  summaryTotal: number | null;
  summarySum: number;
  actualRows: number;
}

export function validateSourceDocument(markdown: string): ValidationResult;
```

#### `src/lib/extract-title.ts` (NEW v2.1)

```typescript
export function extractDocumentTitle(markdown: string): string | null;
```

---

### §26 Component Props Summary

(Same as v2.0 — 10 components, no prop changes.)

---

### §27 Testing Strategy

#### 27.1 Test pyramid

| Layer | Count | What it covers |
|-------|-------|----------------|
| Unit | 89 | Pure functions in `lib/` — fence, enhance, toc, frontmatter, tags, slug-parity, config, reading-time, validate-source, active-section, extract-title |
| Integration | 55 | Full pipeline rendering with `react-markdown` — badges, code blocks, images, task lists, theme toggle, error boundary, back-to-top, mobile nav, copy button, editorial template, dev warnings |
| Accessibility | 2 | axe-core via Playwright — WCAG 2.2 AA in light and dark modes |
| Performance | 1 | Bundle size gate (< 250 KB gzipped) |
| **Total** | **147** | |

#### 27.2 TDD workflow

Every new feature or bug fix follows red → green → refactor:

1. **Write the failing test first.** Run it — it should fail because the implementation doesn't exist.
2. **Write the minimum implementation to make the test pass.** Don't add anything not covered by a test.
3. **Refactor.** Clean up. Tests stay green.

Example (from the v2.1 remediation — `active-section.ts`):

```typescript
// 1. Write failing test
// tests/unit/active-section.test.ts
it("does NOT clear activeSlug when a non-intersecting entry leaves but another is still visible", () => {
  const state = new Map([["s1", true], ["s2", true]]);
  const result = reduceActiveSlug(state, [{ target: { id: "s1" }, isIntersecting: false }]);
  expect(result).toBe("s2");
});

// 2. Run — fails because @/lib/active-section doesn't exist
// 3. Implement src/lib/active-section.ts (reduceActiveSlug with Map state)
// 4. Run — passes
```

#### 27.3 Test setup — mocking jsdom gaps

(Same as v2.0 — `IntersectionObserver` and `matchMedia` mocked in `tests/setup.ts`.)

#### 27.4 Coverage thresholds

v2.1 actual: 89.84% / 81.15% / 85.84% / 91.8% — all above the 80/75/80/80 thresholds.

#### 27.5 Test inventory (145 vitest + 2 Playwright)

| Suite | File | Tests |
|-------|------|-------|
| Unit | `fence.test.ts` | 5 |
| Unit | `enhance.test.ts` | 10 |
| Unit | `toc.test.ts` | 9 |
| Unit | `frontmatter.test.ts` | 7 |
| Unit | `tags.test.ts` | 6 |
| Unit | `slug-parity.test.ts` | 9 |
| Unit | `config.test.ts` | 14 |
| Unit | `reading-time.test.ts` | 10 |
| Unit | `validate-source.test.ts` | 6 (NEW v2.1) |
| Unit | `active-section.test.ts` | 6 (NEW v2.1) |
| Unit | `extract-title.test.ts` | 7 (NEW v2.1) |
| Integration | `markdown-rendering.test.tsx` | 4 |
| Integration | `code-block.test.tsx` | 5 |
| Integration | `images.test.tsx` | 5 |
| Integration | `task-lists.test.tsx` | 4 |
| Integration | `dev-warnings.test.tsx` | 1 |
| Integration | `theme-toggle.test.tsx` | 9 |
| Integration | `error-boundary.test.tsx` | 4 |
| Integration | `back-to-top.test.tsx` | 5 |
| Integration | `mobile-nav.test.tsx` | 9 |
| Integration | `copy-button.test.tsx` | 4 |
| Integration | `editorial-template.test.tsx` | 5 |
| Performance | `bundle-size.test.ts` | 1 |
| **vitest total** | | **145** |
| Accessibility | `axe.test.ts` | 2 (Playwright) |

---

### §28 Appendices

#### Appendix A: ADRs (v2.1 additions)

**ADR-9 — Why a separate `lint:source` gate instead of a unit test?** (NEW v2.1)
A unit test runs in vitest and is part of `npm run test`. A gate runs as its own npm script and can be invoked independently (e.g., in CI before any other gate). The source-document validator needs to run *before* typecheck (so a broken source doesn't waste time typechecking) and *before* build (so a broken source doesn't produce a broken artifact). A separate gate makes this ordering explicit and lets CI fail fast.

**ADR-10 — Why a `Map<id, boolean>` instead of a `Set<id>` for active-section tracking?** (NEW v2.1)
A `Set` of "currently visible ids" would work, but it can't distinguish "not observed" from "observed and not intersecting." The `Map` makes the state explicit: every observed element has an entry, and the value is its current intersection state. This matters for the reducer's `for (const [id, visible] of state) { if (visible) return id; }` loop — it iterates in insertion order (the order elements were observed), so the "first visible" is deterministic.

**ADR-11 — Why `max(latinMinutes, cjkMinutes)` instead of `latinMinutes + cjkMinutes` for mixed content?** (NEW v2.1)
Summing would double-count: a reader doesn't read the Latin part at 200 wpm and *then* the CJK part at 300 cpm sequentially — they read the whole document at whatever rate the dominant script dictates. Taking the max models this: if the document is mostly Latin, the Latin rate dominates; if mostly CJK, the CJK rate dominates; if balanced, the larger of the two wins (conservative).

**ADR-12 — Why a build-time `transformIndexHtml` plugin instead of a post-build script?** (NEW v2.1)
A post-build script (`node scripts/rewrite-title.mjs` after `vite build`) would work but adds a step to the build pipeline. A `transformIndexHtml` plugin runs *during* the Vite build, between HTML generation and file emission. It's atomic — the build either produces a correct artifact or fails. No ordering risk, no separate script to forget.

#### Appendix B: Build metrics (v2.1)

| Metric | Value |
|--------|-------|
| Source files | 42 |
| Test files | 23 |
| Total tests | 145 vitest + 2 Playwright = 147 |
| Build output | `dist/index.html` (600.19 kB raw, 171.40 kB gzipped) |
| Bundle budget | 250 kB gzipped |
| Margin | 78.6 kB under budget |
| Build time | ~518 ms |
| Build warnings | 0 (was 1 in v2.0) |
| Coverage (lines) | 89.84% (threshold: 80%) |
| Coverage (branches) | 81.15% (threshold: 75%) |
| Coverage (functions) | 85.84% (threshold: 80%) |
| Coverage (statements) | 91.8% (threshold: 80%) |

#### Appendix C: Verification ledger (v2.1)

Every claim in this document traces to an executed command:

| Claim | Command | Observed |
|-------|---------|----------|
| `lint:source` passes | `npm run lint:source` | "Source document is internally consistent." exit 0 |
| Typecheck passes | `npm run typecheck` | exit 0, zero errors |
| ESLint passes | `npm run lint` | exit 0, zero warnings |
| Prettier passes | `npm run lint:format` | "All matched files use Prettier code style!" |
| markdownlint passes | `npm run lint:markdown` | "Summary: 0 error(s)" |
| 145 tests pass | `npm run test` | "Test Files 23 passed (23) / Tests 145 passed (145)" |
| Coverage passes | `npm run test:coverage` | exit 0; 89.84% / 81.15% / 85.84% / 91.8% |
| Build passes (no warnings) | `npm run build` | "✓ built in 518ms"; 171.40 kB gzipped; zero warnings |
| Bundle size passes | `npm run test:bundle-size` | exit 0 |
| `reduceActiveSlug` exists | `rg "export function reduceActiveSlug"` | 1 match (in `src/lib/active-section.ts`) |
| `validateSourceDocument` exists | `rg "export function validateSourceDocument"` | 1 match (in `src/lib/validate-source.ts`) |
| `extractDocumentTitle` exists | `rg "export function extractDocumentTitle"` | 1 match (in `src/lib/extract-title.ts`) |
| `documentTitlePlugin` wired | `rg "documentTitlePlugin" vite.config.ts` | 2 matches (definition + plugins array) |
| `inlineDynamicImports` removed | `rg "inlineDynamicImports" vite.config.ts` | 0 matches |
| Source counts consistent | `node scripts/validate-source.mjs` | 202 / 202 / 202 |
| Built `<title>` is correct | `grep -o '<title>[^<]*</title>' dist/index.html` | `<title>Skills Catalog</title>` (the document's H1 — provably different from the static `<title>Document</title>` placeholder in `index.html`, confirming the build-time plugin ran) |

#### Appendix D: Remediation summary (v2.1)

The v2.1 skill captures the result of a 10-issue remediation (see `docs/audit/IMPLEMENTATION_PLAN_v2.1.md` and `docs/audit/REMEDIATION_LOG_v2.1.md` for full details).

**What was fixed:**

- O-1: Source-markdown count mismatch (198/208/202 → 202/202/202). New `lint:source` gate prevents recurrence.
- O-2: `IntersectionObserver` partial-callback bug. Fixed with stateful `Map<id, boolean>` reducer.
- O-3: CJK reading-time underestimation. Fixed with separate 300 cpm rate (max-of with Latin 200 wpm).
- O-4: Editorial `text-5xl` CSS leak. Documented as accepted trade-off (§12.2).
- O-5: Pre-hydration `<title>` flash. Fixed with build-time `transformIndexHtml` plugin.
- O-6: `CLAUDE.md` prettier drift. Formatted.
- O-7: 130 markdownlint errors in `docs/`. Fixed by excluding reference/audit docs from globs.
- O-8: Redundant `inlineDynamicImports` build warning. Removed.
- O-9: v2 spec build-size claim drift. v2.1 Appendix B uses actual verified byte counts.
- O-10: No source-validation gate. Added `lint:source` (Gate 0). CI workflow updated to invoke it as the first step in the `quality` job.

**What was deferred (with justification):**

- AAA contrast for tertiary text — documented limitation (ADR-4).
- Third (`minimal`) template — editorial + technical exercises the machinery.
- Syntax highlighting — adds runtime dep + CSS theme work; better as a follow-up.
- `gray-matter` swap for real YAML — current flat-YAML parser is sufficient.
- Offline font bundling — documented as an extension path.
- `theme-storage.ts` storage key hardcoded — single-instance deployment is the documented use case.
- ~~CI workflow update to invoke `lint:source`~~ — **done**. The `quality` job now runs `npm run lint:source` as its first step (immediately after `npm ci`, before typecheck).

#### Appendix E: Glossary

| Term | Definition |
|------|------------|
| **Two-layer token pattern** | Layer 1: `:root` runtime variables flipped by `@media` / `[data-theme]`. Layer 2: `@theme inline` bridges variables into Tailwind utilities. The only correct way to do dark mode in Tailwind v4. |
| **Fence-aware scanning** | Line-by-line scanning that tracks whether the current line is inside a fenced code block. Used by `buildToc`, `enhanceMarkdown`, `estimateReadingTime`, and `extractDocumentTitle`. |
| **Backtick-wrapping pipeline** | `enhanceMarkdown` wraps badge values in backticks → react-markdown parses as inline code → `code` component calls `resolveBadge` → renders `<Badge>`. |
| **Slug parity** | `github-slugger` (used by `buildToc`) and `rehype-slug` (used by react-markdown) must produce identical slugs for the same heading text. Verified by `slug-parity.test.ts`. |
| **Gate** | A quality check that must pass before code ships. v2.1 has 9: lint:source, typecheck, lint, lint:format, lint:markdown, test, coverage, build, bundle-size, a11y. |
| **Gate V-1** | Version verification gate: `npm ls --depth=0` confirms installed deps match the pinned versions in §4. |
| **Partial-callback bug** | (NEW v2.1) The `IntersectionObserver` callback receives only *changed* entries, not every observed element. A naive `entries.every(!isIntersecting)` check incorrectly clears state. Fixed by tracking per-element visibility in a `Map`. |
| **Dual-rate reading time** | (NEW v2.1) Latin words at 200 wpm, CJK characters at 300 cpm, max-of. Avoids the ~25% overestimate that a single 200-wpm rate produces for CJK-heavy content. |
| **Build-time title injection** | (NEW v2.1) A `transformIndexHtml` Vite plugin reads the markdown source and rewrites `<title>` at build time, eliminating the pre-hydration flash of the wrong static title. |

---

*This skill file was distilled from a full TDD remediation of the `nordeim/markdown-to-html` codebase on 2026-08-08. Every claim is verifiable against the actual codebase. Version 2.1.0. Companion documents: `docs/audit/IMPLEMENTATION_PLAN_v2.1.md`, `docs/audit/REMEDIATION_LOG_v2.1.md`, `docs/v2_rendering_comparison_3.md` (spec-vs-spec audit that motivated this remediation).*
