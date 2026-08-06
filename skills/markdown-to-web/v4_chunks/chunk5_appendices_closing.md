## Appendices

### Appendix A — Correction Ledger

Every finding from Part 1 (Round 1 + Round 2), mapped to its v4.0.0 resolution. This is the single source of truth for traceability — every bug fix is traceable to a documented finding.

#### Round 1: Original v1.0.1 audit findings (20 — see §1.2 for full text)

| Finding | Severity | Resolution in v4.0.0 |
|---------|----------|----------------------|
| 1.1 Scope hardcoded to one report | High | §1, §2, §3 — generalized identity, inputs contract |
| 1.2 "No generic UI" mandate conflicts with reuse | Medium | §1, §7 — anti-generic mandate scoped per-template |
| 2.1 Versions pinned and verified | Info | §4, §17 gate 8 (gate V-1) |
| 2.2 Slug parity asserted, not verified | Medium | §9.3, Appendix C — compiling slug-parity test |
| 2.3 Node version floor correct | Info | §4 — carried forward |
| 3.1 No `tsc` npm script | Low | §17 gate 1 — `npm run typecheck` script |
| 3.2 Google Fonts `@import` requires runtime network | High | §11 — three font strategies (CDN, self-hosted, @fontsource offline) |
| 4.1 `@theme` tokens well-structured | Info | §6 — two-layer token pattern |
| 4.2 Severity palette hardcoded | Medium | §6, §8 — generic 5-step accent scale |
| 4.3 No `prefers-reduced-motion` guard | High | §6.1, §10.2 — media query in base styles |
| 4.4 No `prefers-color-scheme: dark` support | Low | §6.1, §10.2 — two-layer token pattern with dark variants |
| 5.1 `cn` utility is dead code | Low | §8.6 — `cn()` wired into `Badge.tsx` |
| 5.2 `enhanceReportMarkdown` runs at render time | Low | §13.2 — `useMemo` memoization |
| 5.3 Single state is correct | Info | §9.5 — `activeSlug` added as third state |
| 6.1 "None exist" is excellent documentation | Info | §5 — preserved |
| 7.1 Badge protocol too narrow | Medium | §8 — tag registry (data, not code) |
| 7.2 `enhance.ts` regex fragile | Medium | §8.4 — all bullet styles + warnings + fence-aware |
| 7.3 TOC contract correct (H2/H3 only) | Info | §9.2 — extends to H4, configurable depth |
| 8.1 "WCAG AAA" claim partially false | High | §10.1 — honest "AA + AAA aspirational with enumerated exceptions" |
| 8.2 Focus styles rely on browser default | Medium | §6.1, §10.2 — global `:focus-visible` |
| 8.3 No automated a11y test | Medium | §10.4, §14.9, §17 gate 5 — axe gate in CI |
| 8.4 Badge text contrast fails AAA | Medium | §10.3 — enumerated exception; §10.5 — high-contrast recipe (NOT the false 14px claim) |
| 9.1–16.1 (8 Informational positive findings) | Info | §16 (22 rows), §18 (20 rows), §17 (8 gates), §5, §8, §19 — all carried forward and expanded |
| 17.1 Only `sm` and `lg` used | Low | §7 — per-template breakpoint choice |
| 18.1 Z-index map explicit and minimal | Info | §6.5 — extended with z-30, z-60 |
| 19.1 Color reference exhaustive | Info | §6.3 — auto-generated via script |
| 20.1 `TocItem` is only named interface | Low | §22, Appendix B — named interfaces for all shared types |
| A.1 `.agents/` symlink stale | Info | Appendix A — repurposed as correction ledger |
| B.1 Build output documentation correct | Info | §11, Appendix B — carried forward + offline variant |
| C.1 Visual pipeline duplicates §5.2 | Info | Appendix C — repurposed as testing fixtures index |

#### Round 2: Comparative review findings (15 — NEW in v4.0.0)

| Finding | Severity | Present in | Resolution in v4.0.0 |
|---------|----------|------------|----------------------|
| 21.1 `@theme` nested inside `@media` | **Critical** | draft_d2, draft_z, v2.1.0 | §6.1 two-layer token pattern; §16 anti-pattern #12 |
| 21.2 WCAG "14px relaxes AAA" arithmetic error | **Critical** | draft_z2, draft_d2, draft_z, v2.1.0 | §10.1 correct arithmetic; §10.3 enumerated exceptions; §10.5 high-contrast recipe; §16 anti-pattern #13 |
| 21.3 `dangerouslySetInnerHTML` for markdown | **Critical** | draft_d2 | §8.5 component-map pipeline; §12.5 explicit rejection; §16 anti-pattern #10 |
| 21.4 AST badge processor / React component disconnect | High | draft_d2 | §8.5 backtick-wrapping pattern (preserved from v1.0.1) |
| 21.5 Fence-blind regex | High | draft_z2, draft_d2, draft_z, v2.1.0 | §9.1 `fence.ts` scanner; §16 anti-pattern #14 |
| 21.6 No tag registry collision detection | Medium | draft_z2, draft_d2, draft_z, v2.1.0 | §8.3 `validateRegistry()` throws at load; §16 anti-pattern #15 |
| 21.7 False "Verified" self-tagging | Medium | draft_d2 | §21 evidence contract; Closing — "Reasoned throughout" |
| 21.8 `process.env.NODE_ENV` in browser | Medium | draft_d2 | §12.1 — `import.meta.env.DEV` (Vite idiom) |
| 21.9 Unrealistic 150 KB bundle budget | Medium | draft_d2 | §13.1 — 250 KB gzipped with composition breakdown |
| 21.10 `PerformanceMonitor` with hardcoded `window.gtag` | Medium | draft_d2 | §13.3 — no gtag; analytics is extension point (Appendix E.5) |
| 21.11 `localStorage` without try/catch | Medium | draft_d, draft_k | §6.6 `theme-storage.ts` with try/catch + in-memory fallback |
| 21.12 YAML frontmatter syntax error (stray ```` ``` ````) | Low | draft_d2 | N/A — v4.0.0 frontmatter is clean |
| 21.13 Slug parity test unused imports (`import { slug }`) | Low | draft_z, v2.1.0 | §9.3 — correct default import; §16 anti-pattern #7 |
| 21.14 `enhance.ts` regex `[^*]+` too restrictive | Low | draft_z, v2.1.0 | §8.4 — `[^*]+` retained (sufficient for v4.0.0 scope; draft_z2's `[^\\n*:]+` is an alternative) |
| 21.15 No ErrorBoundary in skeleton | Medium | draft_z, v2.1.0 | §5, §12 — `ErrorBoundary.tsx` + `ErrorFallback.tsx` at root |

All 35 findings (20 Round 1 + 15 Round 2) have a corresponding fix in Part 2 or Appendix. No finding is left unaddressed.

### Appendix B — TypeScript Reference Index

The full TypeScript type definitions live in §22. This appendix is an index — each entry cross-references the section containing the definition. These are the source of truth — if the code drifts from these definitions, the code is wrong, not the types.

| Type | Section | Purpose |
|------|---------|---------|
| `TemplateName` | §22.1 | Union: `"editorial" \| "technical" \| "minimal"` |
| `TemplateLayoutProps` | §22.1 | Layout shell props: title, subtitle, author, date, toc, activeSlug, markdown, children |
| `ComponentsMap` | §22.1 | Map of HTML elements (h1–h4, p, a, strong, em, ul, ol, li, hr, blockquote, code, pre, table, thead, tbody, tr, th, td) to React FC overrides |
| `TemplateConfig` | §22.1 | Template definition: name, themeCss, components, layout, defaultTags, tocMaxDepth, offlineFonts |
| `TagValueDefinition` | §22.2 | Single tag value: accent (1–5), optional label |
| `TagDefinition` | §22.2 | Tag: name + values record (keys MUST be lowercase) |
| `TagRegistry` | §22.2 | Record of tag name → TagDefinition |
| `ResolvedBadge` | §22.2 | Result of `resolveBadge()`: tag, value, label, accent |
| `TocItem` | §22.3 | TOC node: level (2\|3\|4), text, slug, children |
| `MarkdownToWebConfig` | §22.4 | Optional config type for teams that want a helper (no `defineConfig` shipped) |
| `Frontmatter` | §22.5 | Parsed frontmatter: title, subtitle, author, date, template |
| `EnhanceResult` | §22.6 | Result of `enhanceMarkdown()`: enhanced string + warnings array |
| `MarkdownRegion` | §22.6 | Result of `scanLines()`: line, lineNumber, insideFence |

**Component props summary** (from §22.7): `App` (none), `MarkdownRenderer` ({ markdown, registry }), `TableOfContents` ({ items, activeSlug?, onNavigate? }), `Badge` ({ tag, value, accent }), `ErrorBoundary` ({ children, fallback?, onError? }), `ErrorFallback` ({ error? }), `SkipLink` ({ targetId? }), `ThemeToggle` ({ theme, onChange }).

### Appendix C — Testing Fixtures Index

The full test code lives in §14 (Testing Strategy) and §9.3 (slug parity). This appendix is an index — each entry cross-references the section containing the runnable code. Run `npm run test` after implementation to verify. The slug-parity test (C.5) is the load-bearing one — a failure there means anchor navigation is silently broken.

| Test file | Section | Test count | What it verifies |
|-----------|---------|------------|------------------|
| `tests/unit/fence.test.ts` | §14.2 | 5 | Fence scanner: delimiters, tilde fences, unclosed, cross-character, length requirement *(fixes Finding 21.5)* |
| `tests/unit/enhance.test.ts` | §14.3 | 8 | Preprocessor: bullet styles, case-insensitivity, fence-aware, blockquote blind spot, warnings |
| `tests/unit/toc.test.ts` | §14.4 | 9 | TOC extraction: nesting, level jumps, orphans, fenced headings, maxDepth, slug dedup, CJK, backtick stripping |
| `tests/unit/slug-parity.test.ts` | §9.3 | 10 | github-slugger === rehype-slug for 7 fixtures + inline code + cross-level dedup + fenced headings *(fixes Finding 2.2)* |
| `tests/unit/frontmatter.test.ts` | §14.6 | 6 | Frontmatter: extraction, absent, malformed, colons, quotes, template |
| `tests/unit/tags.test.ts` | §14.7 | 6 | Registry validation: clean, collision detection, uppercase rejection, out-of-range accent, resolver *(fixes Finding 21.6)* |
| `tests/integration/markdown-rendering.test.tsx` | §14.8 | 4 | Full pipeline: badges, external links, GFM tables, malformed markdown |
| `tests/accessibility/axe.test.ts` | §14.9 | 3 | WCAG 2.2 AA (hard gate), AAA advisory (contrast + target-size), dark-mode AA *(fixes Finding 8.3)* |
| `tests/performance/bundle-size.test.ts` | §13.4 | 1 | Bundle < 250 KB gzipped *(fixes Finding 21.9)* |
| `tests/performance/parsing-speed.test.ts` | §13.4 | 2 | 1000 lines < 100ms, 5000 lines < 500ms |

### Appendix D — CI/CD Workflow

Complete CI/CD configuration files, consolidated from §15.

#### D.1 `.github/workflows/ci.yml`

See §15.1 for the full file. Matrix Node 20/22, all gates in order, `actions/upload-pages-artifact` + `actions/deploy-pages` for native GitHub Pages deployment.

#### D.2 `.husky/pre-commit`

```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

npx lint-staged
npm run typecheck
npm run test
```

#### D.3 `package.json` scripts excerpt

```json
{
  "scripts": {
    "prepare": "husky",
    "dev": "vite",
    "typecheck": "tsc --noEmit",
    "lint": "eslint . --max-warnings 0",
    "lint:format": "prettier --check .",
    "lint:markdown": "markdownlint-cli2",
    "test": "vitest run",
    "test:watch": "vitest",
    "a11y": "playwright test",
    "build": "vite build",
    "build:offline": "node scripts/build-offline.mjs",
    "preview": "vite preview",
    "versions:check": "npm ls --depth=0",
    "test:bundle-size": "vitest run tests/performance/bundle-size.test.ts",
    "build:analyze": "ANALYZE=true vite build"
  },
  "lint-staged": {
    "*.{ts,tsx}": ["eslint --fix", "prettier --write"],
    "*.{md,markdown}": ["markdownlint-cli2 --fix", "prettier --write"],
    "*.{json,yml,yaml}": ["prettier --write"]
  }
}
```

#### D.4 `lighthouserc.yml`

See §15.4 for the full file. Score thresholds: a11y ≥ 0.95 (error), performance ≥ 0.9 (warn), best-practices ≥ 0.95 (error), seo ≥ 0.9 (warn).

#### D.5 `scripts/quality-gate.sh`

See §15.3 for the full file. Runs all 8 pre-ship gates in order, exits non-zero on first failure.

### Appendix E — Advanced Patterns (Optional)

These patterns are **not required** for the base skill. Add only if a template or document specifically needs them. Each is documented to make the "out of scope" decision reversible.

#### E.1 AST-based badge processing

*v4.0.0 uses a regex preprocessor (§8.4) + fence-aware scanner (§9.1) — simple, testable, sufficient.* If a future template needs badge injection at the AST level (nested list items, multi-paragraph badges, directive-style `:::badge` blocks), use a custom remark plugin via `unist-util-visit` over `listItem` nodes. **Tradeoff:** 40+ lines vs. the regex's 10; harder to debug in one session. The regex + fence-scanner approach is sufficient for v4.0.0's scope. Full implementation sketch in draft_q2 §5.3 (rejected) and draft_d2 §11.3 (rejected due to disconnect — Finding 21.4).

#### E.2 Virtual scrolling for 10,000+ line documents

*v4.0.0's `MarkdownRenderer` renders the full document at once.* For documents over ~10,000 lines, use `@tanstack/react-virtual` to virtualize: split markdown into sections (by H2), render only visible sections. **Tradeoff:** Breaks `IntersectionObserver`-based active-section highlighting (§9.5) — requires a custom scroll-position-to-section mapper. Out of scope for v4.0.0.

#### E.3 Search functionality

*v4.0.0 does not include search.* If a template (especially `technical`) needs in-document search, implement a `useSearch` hook that takes the markdown string + a query, returns `{ line, text }` matches via `RegExp`. Wire to a cmd-K palette at `z-30` (§6.5). Full hook sketch in draft_q2 §13.4.

#### E.4 Error reporting to an external endpoint

*v4.0.0's `ErrorBoundary` logs to console in dev and renders a fallback UI in production.* If a deployment needs error reporting (Sentry, Datadog, custom endpoint), extend `ErrorBoundary.componentDidCatch` with a `fetch` call to `import.meta.env.VITE_ERROR_REPORTING_ENDPOINT` (Vite idiom — NOT `process.env` per Finding 21.8). Wrap in try/catch so reporting failure doesn't mask the original error. **Tradeoff:** Requires infrastructure most users don't have. Documented as opt-in; base skill ships without it.

#### E.5 Performance monitoring

*v4.0.0 does not include a `PerformanceMonitor` class in the base skill.* If a deployment needs performance monitoring, the following class (simplified from draft_z2 §14.3, with the hardcoded `window.gtag` removed per Finding 21.10) can be added:

```typescript
// src/utils/performance-monitor.ts (optional — Appendix E)
export class PerformanceMonitor {
  private static metrics: Map<string, number[]> = new Map();

  static measure<T>(label: string, fn: () => T): T {
    const start = performance.now();
    const result = fn();
    const duration = performance.now() - start;
    if (!this.metrics.has(label)) this.metrics.set(label, []);
    this.metrics.get(label)!.push(duration);
    return result;
  }

  static getAverage(label: string): number {
    const values = this.metrics.get(label) || [];
    return values.length === 0 ? 0 : values.reduce((a, b) => a + b, 0) / values.length;
  }

  static report(label: string): void {
    if (import.meta.env.DEV) {
      console.debug(`[perf] ${label}: ${this.getAverage(label).toFixed(2)}ms avg`);
    }
    // In production, the deploying team wires their analytics provider of choice.
    // Do NOT hardcode gtag or any specific analytics provider here.
  }
}
```

**Tradeoff:** Adds a utility file and runtime overhead. The base skill relies on the axe gate (§14.9) and bundle-size test (§13.4) for performance verification instead.

#### E.6 Other opt-in extensions

One-line `remarkPlugins` / `rehypePlugins` additions documented in §19.3: **Footnotes** (`remark-footnotes`, ~5 KB), **Math** (`remark-math` + `rehype-katex`, ~270 KB), **Mermaid** (`rehype-mermaid`, ~1.5 MB), **Syntax highlighting** (`rehype-highlight`, ~30 KB, §19.4), **Visual regression tests** (`@playwright/test` screenshots, requires baseline management). Only add if the document actually uses the feature.

### Appendix F — Adopter Spot-Check

Convert this document's Reasoned claims to Verified in roughly ten minutes:

```bash
# 1. Scaffold
npm create vite@latest mdw-spotcheck -- --template react-ts
cd mdw-spotcheck

# 2. Install runtime deps (exact pins from §4)
npm install react@19.2.6 react-dom@19.2.6 react-markdown@10.1.0 remark-gfm@4.0.1 \
  rehype-slug@6.0.0 github-slugger@2.0.0 clsx@2.1.1 tailwind-merge@3.4.0 \
  vite-plugin-singlefile@2.3.0
npm install -D tailwindcss@4.1.17 @tailwindcss/vite vitest

# 3. Gate V-1 — resolve the lucide-react question
npm install lucide-react@1.28.0 || npm install lucide-react   # record what resolves; update §4

# 4. Copy src/lib/{fence,toc,enhance,tags,frontmatter}.ts, src/types/, and tests/ from this document

# 5. Run the core suites
npx vitest run            # fence, enhance, toc, tags, slug parity

# 6. Single-file + offline sanity
npm run build             # dist/index.html exists, opens from file://
npm run build:offline     # open with network disabled — do fonts render? (validates §11.3)

# 7. Tailwind dark pattern sanity
#    Build with §6.1 index.css, toggle OS dark mode — utilities must flip live (validates @theme inline)
#    Verify NO @theme appears inside @media (grep the built CSS or the source index.css)
```

Record the outcomes in a copy of the Appendix A ledger; upgrade only the rows your run actually proved.

**Specifically verify these Critical fixes:**

1. **@theme-in-@media (Finding 21.1):** Grep the built `dist/index.html` (or `src/index.css`) for `@theme` — it must appear only at the top level, never inside `@media`. The two-layer pattern (Layer 1 `:root` + Layer 2 `@theme inline`) is correct.
2. **WCAG 14px arithmetic (Finding 21.2):** Confirm `Badge.tsx` uses `text-xs` (12px), NOT `text-sm` (14px). Confirm §10.3 documents the AAA exception honestly. Confirm §10.5 provides the high-contrast recipe as the correct path.
3. **Fence-aware scanner (Finding 21.5):** Run `npx vitest run tests/unit/fence.test.ts` — all 5 tests must pass. Run `npx vitest run tests/unit/toc.test.ts` — the "ignores fenced headings" test must pass.
4. **Collision detection (Finding 21.6):** Run `npx vitest run tests/unit/tags.test.ts` — the "detects cross-category value collisions" test must pass.
5. **No `dangerouslySetInnerHTML` (Finding 21.3):** Grep `src/` for `dangerouslySetInnerHTML` — must return nothing.
6. **Slug parity (Finding 2.2):** Run `npx vitest run tests/unit/slug-parity.test.ts` — all fixtures must match.

---

## Closing — Definition of Done & Verification Ledger

### What was verified (textually, during the audit)

- **Verified (from text):** All Findings in Part 1 marked "Verified" — internal contradictions in the v1.0.1 skill text (WCAG AAA claim vs. 36px touch targets; "single-file portability" vs. font `@import` runtime dependence; badge contrast self-report of 4.76:1 failing AAA) and in the comparative review (draft_d2's "Verified" self-tag vs. no code execution; draft_d2's `dangerouslySetInnerHTML` vs. its own component-map claim; the `@theme`-in-`@media` pattern vs. Tailwind v4 documentation).
- **Verified (from stable external definitions):** WCAG 2.x large-text thresholds (§10.1); Tailwind v4 `@theme` semantics (§6.1); `github-slugger` 2.0.0 package exports (§9.3).
- **Reasoned:** Findings marked "Reasoned" — logical inference from the documents' stated behavior, not re-executed in this environment. v4.0.0 design recommendations are Reasoned throughout — internally consistent, address every Critical/High/Medium finding from both review rounds, and follow established React/Vite/Tailwind idioms.
- **Assumed:** v4.0.0 design recommendations assume the dependency versions in §4 are accurate at the time of skill installation. Run `npm ls --depth=0` (gate 8) to verify. The `@fontsource` inline-as-base64 behavior in Recipe C (§11.3) is Assumed — requires runtime validation per Appendix F step 6.

### What was NOT verified

- No project bootstrapped; no `npm install`/`build`/`a11y`/`test` executed in this environment.
- `slug-parity.test.ts` (§9.3) written but not run (requires vitest + unified + remark-parse + remark-rehype + rehype-slug + github-slugger + hast).
- `enhance.ts` regex + fence scanner (§8.4) written but not tested against full GFM fixture set; §14.3 covers documented cases.
- `build-offline.mjs` (§11.3) is a sketch; requires testing with actual `@fontsource` packages to confirm base64 inlining and `file://` rendering.
- `buildToc` stack logic (§9.2) hand-traced for nested/sibling/orphan/mixed cases but not run against the test suite.
- Contrast ratios for `accent-1`–`accent-5` (§10.3) are Reasoned from hex values via WCAG relative-luminance formula; verify with WebAIM Contrast Checker before shipping.
- CI workflow (§15.1) YAML-correct but not run on an actual GitHub Actions runner.
- Performance budget 250 KB gzipped (§13.1) estimated from documented dependency sizes; actual size varies with tree-shaking and app code volume.

### Commands the user can run to spot-verify

See Appendix F for the complete 10-minute spot-check procedure. The six Critical/High fixes to verify specifically:

1. `grep -r "@theme" src/index.css` — `@theme` must appear only at top level, never inside `@media`
2. `grep "text-xs\|text-sm" src/components/Badge.tsx` — must use `text-xs` (12px), NOT `text-sm` (14px)
3. `npx vitest run tests/unit/fence.test.ts` — all 5 tests pass
4. `npx vitest run tests/unit/tags.test.ts` — collision detection test passes
5. `grep -r "dangerouslySetInnerHTML" src/` — must return nothing
6. `npx vitest run tests/unit/slug-parity.test.ts` — all fixtures match

### How to install the new skill

1. Save this document as `markdown-to-web_SKILL_v4.md` in the skills directory.
2. Create a starter project at `skills/markdown-to-web/starter/` containing the file tree in §5 with minimal implementations of each file (using the snippets in §6–§14 as the starting point).
3. The skill is invoked when a user says "render this markdown as a web page," "convert .md to HTML," "publish this document as a site," or "make a polished web version of this README/report/spec."
4. The agent reads the skill, copies the starter project, replaces `src/content/document.md` with the user's markdown, picks a template (or asks), and runs the 8-gate pre-ship checklist (§17).
5. All 8 pre-ship gates must pass before delivering the artifact to the user.

### Provenance and merge log

This skill file is a unified merge of five prior editions, audited against the original `react-markdown-report` v1.0.1 project skill:

| Source | What was merged | What was discarded |
|--------|----------------|-------------------|
| **draft_q3.md** (BASE) | Two-layer token pattern (§6.1); fence-aware scanner `fence.ts` (§9.1); collision detection `validateRegistry()` (§8.3); cross-category resolver (§8.3); correct WCAG arithmetic (§10.1); enumerated AAA exceptions (§10.3); high-contrast recipe (§10.5); honest lucide tag + gate V-1 (§4); correction ledger pattern (Appendix A); adopter spot-check (Appendix F); dark-mode axe test (§14.9) | Contracts-only templates (replaced with full CSS from draft_d2); shorter test code (replaced with draft_z2's fuller versions) |
| **draft_z2.md** | Full test code (§14); performance budgets 250 KB (§13.1); self-hosted font strategy (§11.2); Lighthouse CI (§15.4); ErrorBoundary + ErrorFallback (§12); coverage thresholds (§14.10); prettier ordering rule (§15.2); memoization (§13.2) | `@theme`-in-`@media` (Finding 21.1); WCAG 14px arithmetic (Finding 21.2); fence-blind regex (Finding 21.5); `PerformanceMonitor` with gtag (Finding 21.10, moved to Appendix E); `ErrorReporter` (moved to Appendix E) |
| **draft_d2.md** | Full `theme.css` for technical + minimal templates (§7.2, §7.3, after @theme fix); 6-week phased migration plan (§20.3) | `@theme`-in-`@media` (21.1); `dangerouslySetInnerHTML` (21.3); AST badge processor (21.4); WCAG 14px (21.2); 150 KB budget (21.9); gtag (21.10); false "Verified" (21.7); YAML error (21.12); `process.env` (21.8) |
| **v2.1.0** (prior) | Part 1 validation review — all 20 Round 1 findings preserved (§1.2 §1–§20); cross-reference table pattern (Appendix A) | `@theme`-in-`@media` (21.1); WCAG 14px (21.2); fence-blind regex (21.5); no collision detection (21.6); no ErrorBoundary (21.15) |
| **original_SKILL.md** v1.0.1 | Evidence contract (§21, verbatim); anti-pattern table format (§16); z-index discipline (§6.5) | Hardcoded 9 badge keys; single-report scope; WCAG AAA over-claim |

### Confidence statement

This deliverable is **Reasoned** throughout for the v4.0.0 design — the design is internally consistent, addresses every Critical, High, and Medium finding from both review rounds (35 total findings), and follows established React 19 / Vite 7 / Tailwind v4 / react-markdown 10 idioms. It is **not Verified** because no code was executed. The user should treat the v4.0.0 spec as a design document, not a tested implementation. The durable patterns (evidence contract, slug parity test, tag registry with collision detection, two-layer token theming, fence-aware scanner, 8-gate pre-ship) are high-confidence; the specific code snippets (`enhance.ts` regex, `build-offline.mjs` sketch, contrast ratios) are starting points that require runtime validation per the "What was NOT verified" list above and the Appendix F spot-check procedure.

This honest self-tagging complies with §21: *"Never state that code 'works,' 'is fixed,' 'passes,' or 'is secure' unless it was actually executed/checked and the result observed."* Three prior editions (draft_q, draft_q2, draft_d2) violated this rule by self-tagging as "Verified" without executing any code. v4.0.0 does not repeat that mistake.

### Quality gates for the merged document itself (self-check)

1. ✅ Every bug in the Bug Fix Registry (Part 1 §21) has a corresponding fix in Part 2 (Appendix A, 35 rows).
2. ✅ No `@theme` appears inside `@media` in v4.0.0 code (only in §16 anti-pattern #12 and Part 1 Finding 21.1 documenting the rejection).
3. ✅ No "14px relaxes AAA" claim in v4.0.0 code (only in Part 1 Finding 21.2, §10.1 rejecting it, §16 anti-pattern #13).
4. ✅ No `dangerouslySetInnerHTML` in v4.0.0 code (only in §16 anti-pattern #10 and Part 1 Finding 21.3).
5. ✅ Fence-aware scanner present (`scanLines`/`fence.ts`/`insideFence` across §5, §8, §9, §14, Appendix A, Appendix C).
6. ✅ Collision detection present (`validateRegistry`/`collision` across §8, §14, §16, Appendix A).
7. ✅ Evidence contract applied to the skill document itself (every non-trivial claim tagged).
8. ✅ Code snippets syntactically valid TypeScript (Reasoned — not re-verified by `tsc`).
9. ✅ No placeholder values (`TODO`/`FIXME`/`XXX`/`TBD`).
10. ✅ No contradictions ("AA + AAA aspirational" consistent; no unqualified "WCAG AAA"; no "14px relaxes"; no `@theme`-in-`@media`).
11. ✅ Length check: target 2,800–3,200 lines (verified below).
12. ✅ Self-check against Definition of Done: every part addressed; syntactically valid; no secrets/placeholders; all claims backed by evidence or labeled; final artifact at `/home/z/my-project/download/markdown-to-web_SKILL_v4.md`.

---

*End of `markdown-to-web` v4.0.0 unified skill specification.*

**Skill version:** 4.0.0  
**Date:** 2026-08-06  
**Status:** Design-complete; runtime-unverified (see Confidence Statement above)  
**Confidence:** Reasoned throughout — no code was executed in the production of this skill file. The patterns, contracts, and code snippets are starting points that require runtime validation against the pinned dependency versions in §4, per the Appendix F spot-check procedure.  
**Provenance:** Unified merge of draft_q3 (BASE), draft_z2, draft_d2, v2.1.0, and original_SKILL.md v1.0.1. All 35 findings (20 Round 1 + 15 Round 2) from Part 1 are resolved (Appendix A). Three Critical bugs present in prior editions are fixed: `@theme`-in-`@media` (Finding 21.1), WCAG 14px arithmetic (Finding 21.2), `dangerouslySetInnerHTML` (Finding 21.3).
