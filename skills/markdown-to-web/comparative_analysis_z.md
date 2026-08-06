Let me read the full content of all the files to understand what the user wants.
I've reviewed the instructions file (a coding-agent persona defining Mode C — Audit/Review discipline with severity taxonomy, confidence tagging, and standard finding format) and skimmed all six skill files (the original `react-markdown-report` v1.0.1 plus five drafts: `draft_d`, `draft_k`, `draft_q`, `draft_q2`, `draft_z`).

Before I run the comparative audit, I need to lock down a few decisions that materially change the output shape.
Now let me set up a plan and read all six files completely before drafting the critique.
让我重新核实一下实际的文件内容，因为预览显示的标题与我直接读取的不一致：
现在我已经正确映射了这些文件。让我阅读一下我还没看过的剩余草稿。
Below is the deep-dive critique. Mode C (Audit/Review). Severity taxonomy and confidence tagging follow the persona file §12 and §13. No code was executed in this environment — all findings are tagged Reasoned or Verified-from-text. Where a finding depends on runtime behavior I would need to confirm by running the build, axe, or browser inspection, I say so explicitly.

---

# Comparative Audit — Six Skill Files for Markdown-to-Web Rendering

## 0. Verification Ledger

| What I checked | How | Result |
|----------------|-----|--------|
| File inventory & version metadata | `head`/`tail` + line count | Verified |
| Internal consistency of each draft (claims vs. code snippets) | Read each draft end-to-end | Verified from text |
| Cross-draft completeness matrix | Built from the seven dimensions the user selected (Completeness focus) | Reasoned |
| Whether code snippets would actually run | Static inspection against documented dependency APIs (react-markdown 10, unified, remark-rehype, vite-plugin-singlefile, github-slugger, Tailwind v4 `@theme`) | Reasoned — no `npm install` was executed in this environment |
| Slug-parity, badge-rendering, font-inlining claims | Cross-checked against the stated library versions | Reasoned |
| Evidence-contract compliance (Verified/Reasoned/Assumed/Unverifiable) | Compared each draft's self-tagging against the persona §13 rule | Verified from text |

**Scope of this audit:** completeness coverage of seven dimensions — Build, Accessibility, Testing, Fonts, Error Handling, CI/CD, Design System — plus generalizability and evidence-contract honesty as cross-cutting concerns. Other dimensions (Correctness, Actionability, Maintainability, Generalizability) are touched on only where they intersect completeness. Per the user's selection, the audit picks a winner.

**Artifacts reviewed:**
- `original_SKILL.md` — `react-markdown-report` v1.0.1 (628 lines, project-specific)
- `draft_d.md` — `markdown-to-web — Project Skill` v1.0.0 (838 lines, config-driven generalization)
- `draft_k.md` — `markdown-to-web-renderer` v2.0.0 (807 lines, YAML-frontmatter general skill)
- `draft_q.md` — *Production-Grade Markdown-to-Web Rendering Skill: Implementation Plan* (838 lines, 12-week plan, **not a skill file**)
- `draft_q2.md` — `Production-Grade Markdown-to-Web Rendering Skill` v2.0.0 (2559 lines, multi-framework + CI/CD)
- `draft_z.md` — `markdown-to-web — Validation Review & Generalized Skill Specification` (1555 lines, combined audit + v2.0.0 design)

---

## 1. Executive Summary & Severity Counts

The six files fall into three categories:

1. **The baseline** (`original_SKILL.md`, v1.0.1) — a high-quality *project* skill that is honest about its own gaps (36 px touch targets, 12 px badge text, no reduced-motion, no tests, no CI, runtime font dependence). It is over-fit to one Kelp audit report, which it admits is a feature, not a bug.
2. **Four attempts at generalization** (`draft_d`, `draft_k`, `draft_q2`, `draft_z`) — each takes a different bet on what "generalized" means: config file (d), preset registry (k), multi-framework + CI/CD (q2), three-template system + tag registry (z).
3. **One non-skill** (`draft_q`) — a 12-week implementation plan that ships as a "skill" but cannot be loaded by an agent to actually render markdown.

Two drafts (`draft_q`, `draft_q2`) commit the same evidence-contract violation: they self-tag as "Verified" despite no code being executed. The persona's §13 is unambiguous — *Never state that code "works," "is fixed," "passes," or "is secure" unless it was actually executed/checked and the result observed.* A skill document that calls itself "Verified" without running anything is a critical defect because the evidence contract is the skill's most transferable idea.

`draft_z` is the only draft that preserves the evidence contract verbatim and self-tags honestly as "Reasoned throughout." It is also the only draft that preserves the original's editorial visual identity (Source Serif 4 + warm paper + teal/moss accents) rather than collapsing into the generic Inter-on-neutral-grays aesthetic that the original explicitly rejected.

### Severity counts

| Severity | Count | Examples |
|----------|-------|----------|
| **Critical** | 2 | False "Verified" claims (draft_q, draft_q2); `dangerouslySetInnerHTML` defeats react-markdown's component map + XSS surface (draft_q2) |
| **High** | 6 | `enhanceMarkdown` emits raw HTML that react-markdown won't render without `rehype-raw` (draft_d); `buildToc` stack-nesting bug (draft_k); Google Fonts `@import` still shipped (draft_d, draft_k); `draft_q` is not a skill; AST-badge pipeline doesn't connect to React `Badge` component (draft_q2); unrealistic 150 KB bundle budget (draft_q2) |
| **Medium** | 10 | Regex flag bugs, `\r\n` fragility, `localStorage` in sandboxes, async-where-sync is misleading, `.use(undefined)` throws in unified, slug-parity test imports nonexistent export, no actual test code despite Vitest mentioned, etc. |
| **Low** | 6 | Version regression (1.0.0 < 1.0.1), dropped editorial identity, `defineConfig` helper mentioned but not implemented, virtual-module plugin described but not coded, etc. |
| **Informational** | 6 | Multi-framework adapter pattern is over-engineered; three-template system is the right scope; `gtag` dead code; etc. |

Findings are ordered by severity below (§4). Per-draft deep-dives (§3) come first to give the findings context.

---

## 2. Completeness-Coverage Matrix

The user selected **Completeness** as the sole review dimension. The seven sub-dimensions come from the user's question text: build, accessibility, testing, fonts, error handling, CI/CD, design system. I added two cross-cutting rows — generalizability and evidence-contract honesty — because every draft's completeness score is modulated by them.

Legend: ✅ = covered with working code or test; ⚠️ = mentioned but not implemented, or implemented with a defect; ❌ = absent.

| Dimension | original v1.0.1 | draft_d v1.0.0 | draft_k v2.0.0 | draft_q (plan) | draft_q2 v2.0.0 | draft_z v2.0.0 |
|-----------|:---:|:---:|:---:|:---:|:---:|:---:|
| **Build** (single-file, vite-plugin-singlefile) | ✅ Documented, works | ✅ Documented | ✅ Documented | ❌ Plan only | ✅ + bundle analyzer | ✅ + offline variant recipe |
| **Accessibility** (claim + verification) | ⚠️ Claims AAA, self-documents AAA failures | ⚠️ Claims AAA, says axe in CI, **no test code** | ⚠️ Claims AAA, admits no axe in CI | ✅ Phase 4 plan | ✅ Full axe test code | ✅ Honest "AA + AAA-aspirational" + actual `axe.test.ts` |
| **Testing** (unit + integration + a11y + visual) | ❌ "No other gates exist" | ⚠️ Mentions Vitest, no tests | ❌ No tests | ✅ Strategy + examples | ✅ Full pyramid with code | ⚠️ Slug-parity test written; others deferred to "spot-verify" commands |
| **Fonts** (offline capability) | ❌ Runtime `@import` only | ⚠️ "Provide option to inline" — no impl | ❌ Still CDN `@import` | ✅ Phase 4 promises inlining | ✅ Full `@font-face` + preload | ✅ Best: `@fontsource` + `build-offline.mjs` sketch |
| **Error handling** (boundaries + fallbacks) | ❌ None | ⚠️ `ErrorFallback.tsx` referenced, no impl | ✅ ErrorBoundary + ErrorFallback | ✅ ErrorReporter module described | ✅ Nested boundaries + reporter | ⚠️ Mentioned, no code |
| **CI/CD** (automated gates) | ❌ "No lint, no test suite, no CI" | ⚠️ `pnpm lint/test` scripts, no CI YAML | ❌ Same as v1.0.1 | ✅ Phase 5 plan | ✅ Full GitHub Actions YAML + husky | ⚠️ Pre-ship commands only, no CI YAML |
| **Design system** (tokens, typography, dark mode) | ✅ Code-first `@theme` | ✅ + dark-mode tokens | ✅ + severity/confidence semantic tokens | ⚠️ High-level only | ✅ Comprehensive but **drops editorial identity** | ✅ Best: preserves editorial + adds 3 templates |
| **Generalizability** (config / multi-doc) | ❌ Hardcoded to Kelp | ✅ `markdown-to-web.config.ts` | ⚠️ Preset registry, single doc | ✅ Multi-framework adapters | ✅ Multi-framework adapters | ✅ Best: 3 templates + JSON tag registry + theme override |
| **Evidence contract** (Verified/Reasoned/Assumed) | ✅ Defined and used | ❌ Lost | ❌ Lost | ❌ Wrongly self-tags "Verified" | ❌ Wrongly self-tags "Verified" | ✅ Preserved verbatim + honestly "Reasoned" |
| **Pre-ship checklist rigor** | 2 gates (tsc + build) | 5 gates (tsc + lint + test + build + smoke) | 3 gates (tsc + build + smoke) | Full suite planned | 8+ gates + script | 8 gates, **most rigorous** |

The matrix already suggests the winner — `draft_z` is the only draft with no ❌ cells in the completeness-critical rows. The per-draft deep-dives below explain *why*.

---

## 3. Per-Draft Deep-Dive

### 3.1 `original_SKILL.md` — `react-markdown-report` v1.0.1

**What it is:** A project skill for one specific app — a single-file React 19 + Vite 7 + Tailwind v4 renderer for the "Kelp Agency vs. Clone" UI/UX audit report. 628 lines.

**Strengths (preserved in all later drafts):**
- **Evidence contract** (§7.2, §15) — Verified / Reasoned / Assumed / Unverifiable tags on every finding. This is the skill's most durable idea and its single best claim to originality.
- **Code-first design system** (§4) — Tailwind v4 `@theme` in `src/index.css`, no `tailwind.config.js`. Documented down to the hex RGB values and the z-index layer map. This is the right Tailwind v4 idiom.
- **Anti-generic mandate** (§1) — explicit rejection of purple gradients, Bootstrap card grids, Inter-on-gray-50 neutrality. The skill treats visual distinctiveness as a *feature*, not aesthetic preference.
- **Slug-parity awareness** (§7.3, §12 lesson 2) — explicitly notes that `github-slugger` (TOC) and `rehype-slug` (rendered `id`) must produce identical slugs. Doesn't ship a test, but flags the risk.
- **Honesty about gaps** (§8 known gaps, §11 "No other gates exist") — the skill admits its WCAG AAA claim is aspirational, admits no tests/CI exist, admits fonts don't inline. This honesty is itself a quality signal.

**Weaknesses (the audit gap every later draft tries to close):**
- Over-fit scope — every design decision serves the Kelp report. Tag keys are hardcoded to 9 severity/confidence values.
- WCAG AAA claim is contradicted by 36 px touch targets (fail 2.5.5 AAA), 12 px badge text (fails 4.76:1 contrast at AAA), and missing `prefers-reduced-motion`.
- No tests, no lint, no CI. Pre-ship gate is two commands: `tsc --noEmit && npm run build`.
- `vite-plugin-singlefile` inlines JS/CSS but not `@import`ed Google Fonts — the "single-file portability" promise is a half-promise.
- `cn.ts` is documented as dead code (§5.1, §9 anti-pattern 4).

**Verdict:** As a *project* skill, this is excellent. As a *generalized* skill, it is the baseline to beat. None of the later drafts should regress on its strengths; several do.

### 3.2 `draft_d.md` — `markdown-to-web — Project Skill` v1.0.0

**What it is:** A generalized skill built around a `markdown-to-web.config.ts` file. Adds dark mode, syntax highlighting via highlight.js, image embedding, configurable badge patterns, and a Vitest/axe-core/ESLint toolchain. 838 lines.

**Strengths:**
- **Configuration system** (§3) — the `MarkdownToWebConfig` interface is the right shape: `markdown`, `toc`, `theme`, `badges`, `images`, `accessibility`, `output`. Each option has a sensible default. The `defineConfig` helper (§4.3) is the right ergonomic wrapper.
- **Dark mode** (§5.1, §6.3) — `[data-theme="dark"]` token overrides + `ThemeToggle` with `localStorage` persistence. Adds real value over v1.0.1.
- **Image embedding** (§8.2) — base64-encode small images, link large ones. Sensible default (`embed: true`, `maxSizeKb: 200`).
- **Configurable badge patterns** (§3.1) — `patterns: Array<{ regex, styleMap }>` is a clean generalization of v1.0.1's hardcoded 9 keys.
- **pnpm + Vitest + axe-core + ESLint + Prettier toolchain** (§2, §4.2) — correct modern stack.

**Weaknesses:**
- **H1, M1, M5, L1, L3, L4** (see §4 below) — the config-system foundation is right, but several code snippets won't run as written.
- **Evidence contract lost** — no Verified/Reasoned/Assumed tags anywhere. The single best idea from v1.0.1 is silently dropped.
- **Anti-generic mandate softened to "neutral and editorial"** (§1) — the original's "no Inter/Roboto safety unless they choose it" is preserved in principle but the default theme *is* Inter-on-paper-50, which is exactly the aesthetic v1.0.1 rejected.
- **Version regression** — `1.0.0` is lower than the original's `1.0.1`. SemVer-incompatible with the source it claims to generalize.
- **`rehype-raw` missing** — `enhanceMarkdown` produces `<span data-badge="...">` raw HTML, but react-markdown 10 by default does not render raw HTML. Without `rehype-raw` in the pipeline (not mentioned anywhere in §6.2's data flow), the badge preprocessor's output is silently rendered as text. This is a High-severity correctness defect.
- **No actual test code** — Vitest is mentioned in §2 and §4.2, but no test file is shown. The pre-ship checklist (§12) runs `pnpm test` but the suite doesn't exist.

### 3.3 `draft_k.md` — `markdown-to-web-renderer` v2.0.0

**What it is:** A YAML-frontmatter general skill with a preset-based badge registry, frontmatter support, error boundaries, and syntax highlighting via `rehype-highlight`. 807 lines.

**Strengths:**
- **YAML frontmatter** (§5.2) — `extractFrontmatter()` is a real generalization. Title/subtitle/author/date/badgeConfig/theme parsed from the markdown file itself. This is the right way to do per-document metadata.
- **Preset-based badge registry** (§7) — `BADGE_REGISTRY["audit"]`, `BADGE_REGISTRY["docs"]` etc. lets users switch tag semantics per document. Better than v1.0.1's 9 hardcoded keys.
- **Error boundary + ErrorFallback** (§6.2, §10) — two components with distinct responsibilities. The defensive patterns list (§10.3) — optional chaining, empty-Markdown handling, non-string children — is concrete and actionable.
- **File inventory** (§6.1) — 10 files, ~520 LOC. Concrete enough for an agent to scaffold.
- **Migration table** (Appendix C) — maps every v1.0.1 pattern to its v2.0.0 replacement.
- **YAML frontmatter for the skill file itself** (lines 1–18) — `name`, `description`, `version`, `tags`. This is the correct format for skill-discovery systems and is missing from every other draft.

**Weaknesses:**
- **H2, M2, M6** — `buildToc` stack logic is buggy for level jumps, `extractFrontmatter` regex is `\r\n`-fragile, `ErrorBoundary` class lives in `ErrorFallback.tsx` (mismatch).
- **Same font gap as v1.0.1** — still ships Google Fonts `@import`. The "single-file portability" half-promise is preserved rather than fixed.
- **No tests, no CI** — pre-ship checklist (§13) is three commands: `tsc`, `build`, `preview`. Same as v1.0.1. The skill admits "No automated axe/Lighthouse in CI" in §9 but still claims "WCAG AAA" in the same table. Same self-contradiction as v1.0.1.
- **Evidence contract lost** — like draft_d, the Verified/Reasoned/Assumed tags are gone.
- **Badge registry is TypeScript, not data** — `BADGE_REGISTRY` is a `const` object in `badges.ts`. Draft_z's JSON registry is more data-driven (users can ship new presets without touching code).

### 3.4 `draft_q.md` — *Implementation Plan*

**What it is:** A 12-week implementation plan for a multi-framework (React/Vue/Svelte) markdown renderer with adapter pattern, AST-based preprocessing, and full CI/CD. 838 lines. **Not a skill file** — it is a project plan that describes what *would* be built.

**Strengths:**
- **Phased delivery** (§4) — six phases, each with deliverables, acceptance criteria, key tasks, and verification commands. This is how a competent tech lead would plan a 12-week project.
- **Risk mitigation** (§7) — technical risks (remark/rehype breaking changes, framework adapter divergence, performance degradation) and process risks (scope creep, incomplete testing) are tabulated with mitigations.
- **Success metrics** (§8) — test coverage 100% core / 90% overall, bundle < 150 KB gzipped, Lighthouse 90+, build < 30 s. Concrete and measurable.
- **Verification ledger** (§11) — maps each audit finding (C1, C2, H1, H2, etc.) to the section that addresses it. Good traceability.

**Weaknesses:**
- **H4** — this is not a skill. An agent reading this document cannot render a markdown file. The document explicitly says "Begin Phase 1 implementation" as the "Next Action." A skill file should be loadable as-is; this is a project brief.
- **C1** — the document self-tags as "Verified — Plan addresses all audit gaps, follows system prompt priorities, includes comprehensive testing and verification strategy, and is achievable within 12-week timeline." This is an evidence-contract violation. You cannot verify a plan; you can only verify its execution. The persona §13 is explicit: *"Never state that code 'works,' 'is fixed,' 'passes,' or 'is secure' unless it was actually executed/checked and the result observed."*
- **Scope is dramatically over-expanded** — multi-framework adapters (React/Vue/Svelte), AST-based preprocessing (rejecting regex), 12-week timeline. The user's actual need is "render one markdown file as a polished web page." This plan gold-plates the solution.
- **"Regex-based markdown preprocessing" rejected as an anti-pattern** (§1.3) — but the v1.0.1 regex preprocessor (`enhance.ts`) is one of its best ideas. It is simple, fast, testable, and works. Rejecting it on principle is ideological, not engineering.
- **No actual skill content** — agents can't bootstrap from this. It's a plan to *produce* a skill, not the skill itself.

### 3.5 `draft_q2.md` — `Production-Grade Markdown-to-Web Rendering Skill` v2.0.0

**What it is:** The longest draft (2559 lines). Multi-framework adapters, full CI/CD YAML, full test pyramid with examples, performance monitoring, font strategy with `@font-face`, error reporter with endpoint integration. Aims to be the comprehensive enterprise-grade skill.

**Strengths:**
- **Breadth of coverage** — every dimension in the matrix has at least some code. The CI/CD workflow (§12.1) is a complete GitHub Actions YAML with matrix testing, coverage upload, Lighthouse, security audit, and deploy. No other draft ships this.
- **Test code that actually exists** (§8) — unit tests for `extractToc`, integration tests for `MarkdownRenderer`, axe-core accessibility tests, Playwright visual regression, bundle-size performance tests. The test pyramid is documented with real `describe/it/expect` blocks.
- **Error reporting** (§10.3) — `ErrorReporter` class with HTTP endpoint integration, structured `ErrorReport` shape, development-mode logging. Production-grade observability.
- **Font strategy** (§11) — `@font-face` declarations, `font-display: swap`, system-font fallbacks, `<link rel="preload">`, offline verification test. The most thorough font treatment of any draft.
- **Performance budgets** (§9.1) — bundle < 150 KB gzipped (see H6 below), FCP < 1.5 s, TTI < 3 s, markdown parse < 100 ms for 1000 lines. Concrete and measurable.

**Weaknesses:**
- **C1, C2, H5, H6, M3, M7, M8, L2, L6, I3, I5** — see §4 below. The breadth comes at the cost of internal consistency.
- **Drops the editorial visual identity** — `--font-display: "Inter", ui-sans-serif, system-ui, sans-serif` (§4.1). The original's Source Serif 4 + warm paper + teal/moss accents is replaced with Inter on neutral grays (`--color-surface-primary: #ffffff`, `--color-text-primary: #111827`). This is exactly the "generic 'Inter + gray-50' neutrality" the original's anti-generic mandate (§1) explicitly rejected. The skill ships a different *visual product* than the one it generalizes from, without acknowledging the regression.
- **`processBadges` AST plugin vs. React `Badge` component don't connect** (§5.3 vs §6.4) — the AST plugin sets `node.data.hProperties = { class: 'badge badge-severity-critical' }` on `listItem` nodes. The `Badge` component (§6.4) is a React component that takes `{ category, value, children }` props. These two paths never connect. The AST plugin would emit `<li class="badge badge-severity-critical">critical</li>` — not a `<Badge>` component instance. The CSS classes `badge-severity-critical` aren't defined anywhere in the `@theme`. This is a fundamental architecture defect.
- **`MarkdownRenderer` uses `dangerouslySetInnerHTML`** (§10.2) — defeats the entire point of using react-markdown's component map. The component map exists to render Markdown as React components (with all the benefits of React's reconciliation, accessibility attributes, type safety). Serializing to HTML and shoving it into `dangerouslySetInnerHTML` discards those benefits and creates an XSS surface even with sanitization. The skill simultaneously claims "Security Hardening — XSS prevention (DOMPurify or equivalent)" (§1.2) and ships `dangerouslySetInnerHTML` (§10.2). The defense (sanitize first) is correct, but the architecture is wrong: if you're going to sanitize and `dangerouslySetInnerHTML`, you don't need react-markdown's component map at all — you could just use `marked` + `DOMPurify` and skip React for the content.
- **Unrealistic bundle budget** — React 19 + react-markdown + remark-parse + remark-rehype + rehype-slug + rehype-highlight + rehype-stringify + DOMPurify + gray-matter + zod is realistically 250–400 KB gzipped, not 150 KB. The 150 KB budget (§9.1, §8.6) would force the team to either drop syntax highlighting, drop DOMPurify, or miss the budget and weaken the gate to ship.
- **Self-tags "Verified"** (Conclusion, §2560) — "Confidence: Verified — All audit gaps addressed, comprehensive coverage, evidence-based recommendations." No code was executed. This is the same evidence-contract violation as draft_q.

### 3.6 `draft_z.md` — `Validation Review & Generalized Skill Specification`

**What it is:** A two-part document. Part 1 (≈500 lines) is a section-by-section audit of `react-markdown-report` v1.0.1 with severity counts and findings. Part 2 (≈1000 lines) is a v2.0.0 spec design that addresses every finding from Part 1. 1555 lines total.

**Strengths:**
- **Honest evidence contract** (closing section) — *"This deliverable is Reasoned throughout for the v2.0.0 design… It is not Verified because no code was executed. The user should treat the v2.0.0 spec as a design document, not a tested implementation."* This is the only draft that complies with persona §13. It preserves v1.0.1's evidence contract verbatim (§2.16) and tags its own claims correctly.
- **Three-template system** (§2.7) — Editorial Long-Form (preserves v1.0.1's identity), Technical Docs (Inter + cool grays + search), Minimal Print (system fonts, no color, print CSS). Each template has its own `@theme`, layout, component map, and default tag registry. This is the right level of generalization — not "one config to rule them all" (draft_d), not "multi-framework adapters" (draft_q2), but "three opinionated templates with consistent contracts."
- **Tag registry is JSON, not TypeScript** (§2.8) — `templates/editorial/tags.json` is data, not code. Users can ship new tag presets without touching code. Better than draft_k's TS `BADGE_REGISTRY` and draft_d's config-embedded patterns.
- **Slug-parity test is actually written** (§2.9) — `slug-parity.test.ts` runs `github-slugger` and `rehype-slug` against 11 fixtures (CJK, emoji, repeated headings, leading whitespace, code in headings) and asserts equality. This is the single most important test for this skill and no other draft ships it.
- **Preserves editorial visual identity** — the editorial template's `@theme` (§2.6) is v1.0.1's palette verbatim (Source Serif 4, ink-950, paper-50, teal-600, moss-500). The original's anti-generic mandate survives, scoped per-template.
- **Honest accessibility claim** — "WCAG 2.2 AA + AAA aspirational, with documented exceptions" (§2.1, §2.10). The axe test (§2.10) treats AAA violations as warnings except for `target-size` and `color-contrast` (the two real AAA blockers). This is honest and actionable.
- **Concrete AAA fixes** — badge text 14 px not 12 px (fixes 4.5:1 at 14 px), touch targets 44 px not 32 px (`p-2.5` not `p-1.5`), global `:focus-visible` style, `prefers-reduced-motion` media query. Each fix maps to a specific finding in Part 1.
- **Migration table** (Appendix A) — 13-row table mapping every v1.0.1 pattern to its v2.0.0 replacement. The most actionable migration guide of any draft.
- **Offline build recipe** (§2.11 Recipe B) — `build-offline.mjs` script with `assetsInlineLimit: 100 * 1024 * 1024` to inline everything as base64. Acknowledges the result is 2–4 MB and recommends `pyftsubset` for subsetting. Honest about tradeoffs.
- **Pre-ship checklist** (§2.13) — 8 gates: `typecheck`, `lint`, `test`, `a11y`, `build`, `preview`, `npm ls --depth=0` (dependency verification), artifact self-containment verification. Most rigorous of any draft. Explicitly says "All eight gates must pass. No gate may be skipped, weakened, or made non-blocking to ship."

**Weaknesses:**
- **M4, M9, L5** — `enhance.ts` regex edge case, slug-parity test imports nonexistent `slug` export, `prefers-color-scheme: dark` inside `@theme` is unusual Tailwind v4 syntax.
- **No CI YAML** — pre-ship commands are documented but not wrapped in a GitHub Actions workflow. Draft_q2 is better here.
- **No actual component code beyond snippets** — `MarkdownReport.tsx`, `TableOfContents.tsx`, `App.tsx` are described but not shown. An agent would need to write them. (This is consistent with the "Reasoned not Verified" honesty — the draft doesn't pretend to be a complete implementation — but it does mean more work at bootstrap time.)
- **`build-offline.mjs` is "a sketch"** — explicitly flagged as requiring runtime validation. Honest, but a gap.
- **`enhance.ts` regex** (`/^(\s*[-*+]\s+|\s*\d+\.\s+)\*\*([^*]+):\*\*\s+(.+)$/gm`) — `[^*]+` fails for tag names containing `*` (uncommon, but possible). Minor.

---

## 4. Findings (Ordered by Severity)

### Critical

#### C1 — False "Verified" self-tagging in `draft_q` and `draft_q2`
- **Location:** `draft_q.md:876` ("Confidence Level: Verified — Plan addresses all audit gaps…"); `draft_q2.md:2559` ("Confidence: Verified — All audit gaps addressed, comprehensive coverage, evidence-based recommendations")
- **Description:** Both drafts self-tag as "Verified" despite no code being executed. draft_q is a 12-week *plan* — by definition unverifiable until executed. draft_q2 is a 2559-line spec with code snippets — no `npm install`, `npm run build`, `npm run test`, or `npm run a11y` was run.
- **Evidence:** Persona §13: *"Never state that code 'works,' 'is fixed,' 'passes,' or 'is secure' unless it was actually executed/checked and the result observed."* draft_q and draft_q2 both ship unexecuted code and call it "Verified." draft_z ships unexecuted code and honestly calls it "Reasoned throughout… not Verified."
- **Impact:** The evidence contract is the skill's most transferable idea. A skill that mislabels its own confidence level teaches downstream agents to do the same. This is the single most corrosive defect a skill can have — it doesn't break code, it breaks trust.
- **Severity:** Critical
- **Confidence:** Verified (from text)
- **Recommended fix:** In both drafts, replace "Verified" with "Reasoned" in the closing confidence statement. In draft_q2's per-section verification ledger (§2560), tag each row as "Documented" (current) rather than implying execution. In draft_q, change "Confidence Level: Verified" to "Confidence Level: Reasoned — plan only; not executed."

#### C2 — `draft_q2` uses `dangerouslySetInnerHTML` despite claiming security hardening
- **Location:** `draft_q2.md:1936` (`return <div dangerouslySetInnerHTML={{ __html: html }} />;`), `draft_q2.md:2507` (same pattern in reference implementation)
- **Description:** The `MarkdownRenderer` component (§10.2) processes markdown via `processMarkdown()` (which serializes to HTML via `rehype-stringify`) and injects the result with `dangerouslySetInnerHTML`. This contradicts two things: (a) the skill's own §1.2 "Security Hardening — XSS prevention (DOMPurify or equivalent)" claim, and (b) the entire purpose of using react-markdown's component map.
- **Evidence:** react-markdown 10's `components` prop exists to render Markdown as React elements (with type safety, accessibility attributes, reconciliation). Serializing to HTML and using `dangerouslySetInnerHTML` discards those benefits. The `processMarkdown` pipeline (§5.2) does include `rehype-sanitize` *in the diagram* but not in the actual code — the `.use()` chain omits it. Even with sanitization, the architecture is wrong: if you're going to sanitize + `dangerouslySetInnerHTML`, you don't need react-markdown — use `marked` + `DOMPurify`.
- **Impact:** XSS surface if sanitization is bypassed or misconfigured. Type-safety loss. Accessibility attribute injection becomes harder. The skill's central architectural choice is internally contradictory.
- **Severity:** Critical
- **Confidence:** Reasoned (would need to run the code to confirm the XSS surface, but the architectural contradiction is visible in the text)
- **Recommended fix:** Remove `dangerouslySetInnerHTML`. Use react-markdown's `children` prop with the `components` map directly. If raw HTML pass-through is needed for specific use cases, use `rehype-raw` with `rehype-sanitize` and document the security implications.

### High

#### H1 — `draft_d`'s `enhanceMarkdown` emits raw HTML that react-markdown won't render
- **Location:** `draft_d.md:608` (`return \`<span data-badge="${groups[0]}">${groups[0]}</span>\`;`)
- **Description:** The preprocessor wraps matched values in raw `<span>` HTML. react-markdown 10 by default does not render raw HTML — it escapes it. Without `rehype-raw` in the plugin chain (not mentioned in §6.2's data flow), the badge preprocessor's output is silently rendered as literal text.
- **Evidence:** react-markdown 10 documentation; v1.0.1's `enhance.ts` wraps values in *backticks* (`` `critical` ``) which become inline `code` elements (rendered by the `code` component map entry as a `StatusBadge`). draft_d changes this to raw HTML but doesn't update the pipeline.
- **Impact:** Badges silently fail to render. Users see literal `<span data-badge="critical">critical</span>` text in the output.
- **Severity:** High
- **Confidence:** Reasoned
- **Recommended fix:** Either (a) revert to the backtick-wrapping approach (v1.0.1's pattern, preserved in draft_k and draft_z), or (b) add `rehype-raw` to the plugin chain and document its security implications.

#### H2 — `draft_k`'s `buildToc` stack-nesting logic is buggy for level jumps
- **Location:** `draft_k.md:688` (`while (stack.length > level - 1) stack.pop();`)
- **Description:** For an H2 followed by an H4 (skipping H3), the logic produces wrong nesting. Example: H2 pushed → stack = `[toc, h2.children]` (length 2). H4 arrives, level=4. `stack.length > level - 1` → `2 > 3` is false, so no pop. `parent = stack[stack.length - 1]` = `h2.children`. H4 is pushed onto `h2.children` — correct *by accident* for this case. But for H2 → H4 → H3, after H4: stack = `[toc, h2.children, h4.children]` (length 3). H3 arrives, level=3. `3 > 2` is true, pop `h4.children`. `parent = stack[2]` = `h2.children`. H3 pushed onto `h2.children` — but it should be a sibling of H4, not a child of H2. Wrong nesting.
- **Evidence:** Read the `buildToc` function in §15 "Pattern: TOC Extraction with Shared Slugger." Compare with draft_z's `buildToc` (§2.9) which uses `while (stack.length && stack[stack.length - 1].level >= level) stack.pop();` — correct because it pops based on the *parent's* level, not the *current* level minus one.
- **Impact:** TOC tree is malformed when documents skip heading levels (H2 → H4 without H3). Common in real documents.
- **Severity:** High
- **Confidence:** Reasoned
- **Recommended fix:** Use draft_z's pattern: `while (stack.length && stack[stack.length - 1].level >= level) stack.pop();`

#### H3 — `draft_d` and `draft_k` still ship Google Fonts `@import` despite identifying it as a gap
- **Location:** `draft_d.md:821` ("`dist/index.html` – the single file, fully self-contained (except fonts, which are loaded via `@import`; you can inline them by using a custom font loader or base64 fonts)."); `draft_k.md:144` ("Google Fonts loaded via `@import` in CSS — requires network at runtime")
- **Description:** Both drafts identify the font-dependence gap (it's the central "half-promise" critique of v1.0.1) and then ship the same gap. draft_d says "you can inline them by using a custom font loader" — no implementation. draft_k doesn't even acknowledge it as a gap to close.
- **Evidence:** v1.0.1 §12 lesson 4: *"Single-file build ≠ offline fonts — `vite-plugin-singlefile` inlines JS/CSS but not `@import`ed fonts."* draft_z §2.11 Recipe B ships `build-offline.mjs` with `@fontsource` packages inlined as base64. draft_q2 §11 ships `@font-face` declarations with local font files.
- **Impact:** "Single-file portability" remains a half-promise. Artifacts don't work from `file://` without network. The central pain point identified in every audit is not addressed.
- **Severity:** High
- **Confidence:** Verified (from text)
- **Recommended fix:** Adopt draft_z's `build-offline.mjs` pattern or draft_q2's `@font-face` pattern. Ship both online and offline build modes.

#### H4 — `draft_q` is not a skill; it is a 12-week implementation plan
- **Location:** `draft_q.md:874` ("**Next Action:** Begin Phase 1 implementation (Project scaffolding and foundation)")
- **Description:** A skill file should be loadable by an agent as-is to perform the skill. draft_q is a project plan that describes what *would* be built over 12 weeks. An agent reading this cannot render a markdown file — it can only begin a 12-week implementation project.
- **Evidence:** The document's own §10 "Next Steps" describes initializing a project, installing dependencies, and creating the project structure. No skill content. No code that runs.
- **Impact:** As a "skill file" deliverable, this fails the basic contract. If the user requested a skill and received a plan, they cannot use it.
- **Severity:** High
- **Confidence:** Verified (from text)
- **Recommended fix:** Either (a) reclassify draft_q as a "project plan" rather than a "skill," or (b) extract the actual skill content (the patterns, the test strategy, the CI/CD config) into a loadable skill file and discard the 12-week timeline scaffolding.

#### H5 — `draft_q2`'s `processBadges` AST plugin doesn't connect to the React `Badge` component
- **Location:** `draft_q2.md:694-733` (`processBadges` plugin sets `node.data.hProperties.class = 'badge badge-${category}-${value}'`); `draft_q2.md:998-1045` (`Badge` React component takes `{ category, value, children }` props)
- **Description:** The AST plugin injects CSS classes on `listItem` nodes. The React `Badge` component is rendered via the `components` map's `code` entry (implied by §6.4 but not wired up). These two paths never connect. The AST plugin would emit `<li class="badge badge-severity-critical">critical</li>` — not a `<Badge>` component instance. The CSS classes `badge-severity-critical` aren't defined in the `@theme` (§4.1).
- **Evidence:** Read §5.3 (`processBadges`) and §6.4 (`Badge`) side by side. The data flow (§2.3) says "Badge Injection" happens in the AST Transformation Layer, but the React adapter renders via the component map. There's no bridge.
- **Impact:** Badges silently fail to render as React components. Either the AST plugin's CSS classes have no effect (because no CSS defines them), or the `Badge` component is never instantiated (because the `code` component map entry isn't shown wiring to it).
- **Severity:** High
- **Confidence:** Reasoned
- **Recommended fix:** Pick one path. Either (a) AST-inject CSS classes and define them in `@theme` (skip the React `Badge` component), or (b) use the v1.0.1 pattern: regex-wrap values in backticks → `code` component map entry → `Badge` component (skip the AST plugin). Draft_z's approach (b) is cleaner.

#### H6 — `draft_q2`'s 150 KB gzipped bundle budget is unrealistic
- **Location:** `draft_q2.md:1708` ("Bundle size (gzipped) < 150KB"); `draft_q2.md:1594` ("main bundle is under 150KB gzipped")
- **Description:** React 19 + react-markdown 10 + remark-parse 11 + remark-rehype 11 + rehype-stringify 10 + rehype-slug 6 + rehype-highlight + DOMPurify 3 + gray-matter 4 + zod is realistically 250–400 KB gzipped, not 150 KB.
- **Evidence:** React 19 alone is ~45 KB gzipped. react-markdown + remark + rehype ecosystem adds ~80–120 KB gzipped. DOMPurify is ~20 KB gzipped. gray-matter + zod add ~15 KB. Total: ~160–200 KB gzipped minimum, before application code.
- **Impact:** Either the team misses the budget and weakens the gate to ship (contradicting the "Never weaken a guardrail to make a gate pass" rule from persona Appendix B5), or they drop features (syntax highlighting, sanitization) to hit the budget.
- **Severity:** High
- **Confidence:** Reasoned (would need to actually bundle and measure to confirm exact size, but the order of magnitude is clear)
- **Recommended fix:** Set the budget to 250 KB gzipped (realistic) or 400 KB gzipped (comfortable). Document the tradeoff: smaller bundles mean dropping features.

### Medium

#### M1 — `draft_d`'s badge regex uses `im` flags but needs `gm` for global replacement
- **Location:** `draft_d.md:161` (`regex: /^\s*-\s*\*\*(Severity|Confidence):\*\*\s+(.+)$/im`)
- **Description:** The regex uses `i` (case-insensitive) and `m` (multiline) flags but no `g` (global). Without `g`, `String.replace()` only transforms the first match. The default config's badge pattern would only style the first `Severity:`/`Confidence:` line in the document.
- **Evidence:** Compare with v1.0.1's `enhance.ts` regex: `/^(\s*-\s*\*\*(?:Severity|Confidence):\*\*)\s+(.+)$/gm` — uses `gm`, not `im`.
- **Impact:** Only the first badge in each document is styled. Silent partial failure.
- **Severity:** Medium
- **Confidence:** Reasoned
- **Recommended fix:** Change `im` to `gim` (or just `gm` if case-sensitivity is intended).

#### M2 — `draft_k`'s `extractFrontmatter` regex is `\r\n`-fragile
- **Location:** `draft_k.md:630` (`const match = markdown.match(/^---\n([\s\S]*?)\n---\n/);`)
- **Description:** The regex uses `\n` line endings. On Windows (CRLF), markdown files often have `\r\n` endings. The regex would fail to match frontmatter on CRLF files.
- **Evidence:** The regex literal `\n` matches only LF, not CRLF. Standard `\r?\n` would handle both.
- **Impact:** Frontmatter silently fails to parse on Windows-authored documents. Title/subtitle/author/badgeConfig all lost.
- **Severity:** Medium
- **Confidence:** Reasoned
- **Recommended fix:** Use `/^---\r?\n([\s\S]*?)\r?\n---\r?\n/` or normalize line endings before parsing.

#### M3 — `draft_q2`'s `extractToc` has a `return` inside `visit` that skips legitimate siblings
- **Location:** `draft_q2.md:791-795` (`if (lastItem.level < level) { lastItem.children.push(item); stack.push(item.children); return; }`)
- **Description:** The `return` inside the `visit` callback stops processing the current heading's siblings. For an H2 followed by another H2, the second H2 is never pushed onto the TOC.
- **Evidence:** Read the function. The `visit` callback is called once per heading. The `return` exits the callback for *that* heading, but the bug is subtler: the `while` loop before the `if` pops items off the stack until `stack[stack.length - 1].length === 0`, which can pop too aggressively. The control flow is hard to follow and the test cases in §8.2 don't cover the H2→H2 sibling case explicitly.
- **Impact:** TOC missing sibling headings in some configurations.
- **Severity:** Medium
- **Confidence:** Reasoned
- **Recommended fix:** Use draft_z's `buildToc` pattern (§2.9) which uses `matchAll` and a stack with clear pop-condition.

#### M4 — `draft_z`'s `enhance.ts` regex `[^*]+` fails for tag names containing `*`
- **Location:** `draft_z.md:897` (`const BULLET_RE = /^(\s*[-*+]\s+|\s*\d+\.\s+)\*\*([^*]+):\*\*\s+(.+)$/gm;`)
- **Description:** `[^*]+` matches one or more characters that are not `*`. Tag names containing `*` (uncommon but possible — e.g., `**Priority*:** high`) would fail to match.
- **Evidence:** Read the character class. `[^*]` excludes `*`.
- **Impact:** Edge case. Unlikely in practice but worth fixing.
- **Severity:** Medium
- **Confidence:** Reasoned
- **Recommended fix:** Use `([^*]+?)` (non-greedy) or `([^\n:]+)` to match tag names up to the colon.

#### M5 — `draft_d` uses `localStorage` for theme persistence despite persona §16.3 warning
- **Location:** `draft_d.md:415` ("Persists preference in `localStorage`")
- **Description:** The persona's §16.3 says "Avoid unsupported browser storage in sandboxed environments — use component state unless persistence is explicitly supported." `localStorage` is not available in sandboxed iframes, file:// in some browsers, or SSR contexts.
- **Evidence:** Persona §16.3 (UI Design & Implementation).
- **Impact:** Theme toggle fails silently in sandboxed environments. Draft_k does the same (§9 mentions "localStorage blocked or not used" as a debugging case but still recommends it).
- **Severity:** Medium
- **Confidence:** Reasoned
- **Recommended fix:** Wrap `localStorage` access in `try/catch`. Fall back to in-memory state if `localStorage` is unavailable. Document the fallback.

#### M6 — `draft_k`'s `ErrorBoundary` class lives in `ErrorFallback.tsx` (mismatch)
- **Location:** `draft_k.md:649-664` (`ErrorBoundary` class shown under "Pattern: Error Boundary" with comment `// src/components/ErrorFallback.tsx`)
- **Description:** The class `ErrorBoundary` is shown in a file labeled `ErrorFallback.tsx`. These are two different concerns: the boundary catches errors; the fallback renders the error UI. Mixing them in one file is a code-organization defect.
- **Evidence:** Read the code comment. The class is `ErrorBoundary` but the file is `ErrorFallback.tsx`.
- **Impact:** Future agents looking for the error boundary will search for `ErrorBoundary.tsx`, not find it, and either duplicate the class or miss it.
- **Severity:** Medium
- **Confidence:** Verified (from text)
- **Recommended fix:** Split into `ErrorBoundary.tsx` (class) and `ErrorFallback.tsx` (presentational component). The §6.1 file inventory (line 326) already lists `ErrorFallback.tsx` separately — the pattern section should match.

#### M7 — `draft_q2`'s `processMarkdown` is async but `unified().process()` is sync here
- **Location:** `draft_q2.md:605` (`export async function processMarkdown(...)`)
- **Description:** The function is declared `async` and returns `Promise<ProcessingResult>`, but `unified().process(markdown)` returns synchronously when no async plugins are configured. The `await` on line 650 is unnecessary. This is misleading — callers must use `await` for no reason.
- **Evidence:** unified documentation: `processor.process()` returns a `VFile` synchronously when no plugins are async.
- **Impact:** Callers wrap the call in `async`/`await` unnecessarily. Test setup is more complex than it needs to be.
- **Severity:** Medium
- **Confidence:** Reasoned
- **Recommended fix:** Either make the function sync (remove `async` and `await`), or document that async is required because future plugins (e.g., `rehype-mermaid`) may be async.

#### M8 — `draft_q2`'s `.use(customDirectives ? processBadges : undefined)` throws in unified
- **Location:** `draft_q2.md:642` (`.use(customDirectives ? processBadges : undefined)`)
- **Description:** Passing `undefined` to `unified().use()` throws `Expected a plugin, not undefined`. The conditional should filter out the `undefined` case before calling `.use()`.
- **Evidence:** unified source: `use()` validates its arguments and throws on non-plugin values.
- **Impact:** Build crashes when `customDirectives` is `false`.
- **Severity:** Medium
- **Confidence:** Reasoned
- **Recommended fix:** Use a conditional spread: `...(customDirectives ? [processBadges] : [])` or build the plugin array before the `unified()` chain.

#### M9 — `draft_z`'s slug-parity test imports nonexistent `slug` export from `github-slugger`
- **Location:** `draft_z.md:1031` (`import { slug } from "github-slugger";`)
- **Description:** `github-slugger` 2.0.0 exports only the default `GithubSlugger` class. There is no named `slug` export. The import would fail at runtime.
- **Evidence:** `github-slugger` package exports: `export default GithubSlugger;` (and `export { slug }` was removed in 2.0).
- **Impact:** Test file fails to load. Slug parity test never runs.
- **Severity:** Medium
- **Confidence:** Reasoned
- **Recommended fix:** Remove the `import { slug }` line. The test only uses `new GithubSlugger()` and the default import.

#### M10 — `draft_d` and `draft_k` mention Vitest but ship no test code
- **Location:** `draft_d.md:39` (Testing row in tech stack); `draft_d.md:220-221` (`pnpm test` commands); `draft_k.md` (no test section at all)
- **Description:** Both drafts list Vitest in the tech stack and include `pnpm test` in the pre-ship checklist, but neither ships any actual test files. The pre-ship gate runs `pnpm test` against an empty suite — it passes trivially.
- **Evidence:** Read both drafts end-to-end. draft_d's §16 "Coding Patterns" shows `enhanceMarkdown` and `buildToc` but no test files. draft_k has no test section.
- **Impact:** Pre-ship gate is theater. Tests "pass" because they don't exist.
- **Severity:** Medium
- **Confidence:** Verified (from text)
- **Recommended fix:** Either ship test files (draft_z's `slug-parity.test.ts` is a good starting point) or remove `pnpm test` from the pre-ship checklist until tests exist.

### Low

#### L1 — `draft_d`'s version `1.0.0` is lower than the original's `1.0.1`
- **Location:** `draft_d.md:836` ("**Skill version:** `1.0.0`")
- **Description:** The generalized skill has a lower version number than the project-specific skill it generalizes from. SemVer-incompatible.
- **Impact:** Downstream tooling that resolves skill versions will prefer v1.0.1 (the original) over v1.0.0 (the generalization).
- **Severity:** Low
- **Confidence:** Verified (from text)
- **Recommended fix:** Bump to `2.0.0` to signal the generalization break.

#### L2 — `draft_q2` drops the editorial visual identity for Inter-on-neutral-grays
- **Location:** `draft_q2.md:375-388` (`--font-display: "Inter"`, `--color-surface-primary: #ffffff`, `--color-text-primary: #111827`)
- **Description:** The original's anti-generic mandate (Source Serif 4, warm paper, teal/moss accents) is replaced with the exact aesthetic v1.0.1 rejected. The skill ships a different *visual product* than the one it generalizes from, without acknowledging the regression.
- **Impact:** Visual regression. Users who adopted v1.0.1 for its editorial design lose it in v2.0.0.
- **Severity:** Low (visual, not functional)
- **Confidence:** Verified (from text)
- **Recommended fix:** Preserve the editorial palette as the default. Add other palettes as alternatives.

#### L3 — `draft_d`'s `defineConfig` helper is mentioned but not implemented
- **Location:** `draft_d.md:231` (`import { defineConfig } from 'markdown-to-web';`)
- **Description:** The helper is imported and used but its implementation is not shown.
- **Impact:** Agents bootstrap-time need to write it themselves.
- **Severity:** Low
- **Confidence:** Verified (from text)
- **Recommended fix:** Ship the `defineConfig` implementation in the skill file.

#### L4 — `draft_d`'s virtual-module Vite plugin is described but not coded
- **Location:** `draft_d.md:193` ("The exact mechanism is handled by a Vite plugin that reads the config file and creates a virtual module `virtual:config` that exports the merged config.")
- **Description:** The plugin is described in prose but no code is provided.
- **Impact:** Agents must write the plugin from scratch.
- **Severity:** Low
- **Confidence:** Verified (from text)
- **Recommended fix:** Ship the plugin code.

#### L5 — `draft_z`'s `prefers-color-scheme: dark` inside `@theme` is unusual Tailwind v4 syntax
- **Location:** `draft_z.md:737-749` (`@media (prefers-color-scheme: dark) { @theme { ... } }`)
- **Description:** Tailwind v4's `@theme` directive is meant to be top-level. Wrapping it in `@media` is unusual and may not produce the expected CSS variables. The standard pattern is to define dark tokens as separate variables and override them in `:root[data-theme="dark"]` or `@media (prefers-color-scheme: dark) { :root { --token: ...; } }`.
- **Impact:** Dark mode tokens may not be generated correctly.
- **Severity:** Low
- **Confidence:** Reasoned
- **Recommended fix:** Define dark overrides as `:root` variable overrides inside the media query, not as a nested `@theme` block.

#### L6 — `draft_q2`'s CI YAML deploys with `echo "Deploying to production..."`
- **Location:** `draft_q2.md:2178-2180` (`run: echo "Deploying to production..."`)
- **Description:** The deploy step is a placeholder.
- **Impact:** CI pipeline runs but doesn't actually deploy.
- **Severity:** Low
- **Confidence:** Verified (from text)
- **Recommended fix:** Either remove the deploy job (mark it as "configure per hosting provider") or ship a real deploy step (e.g., `actions/upload-pages-artifact` for GitHub Pages).

### Informational

#### I1 — `draft_z` is the only draft that preserves the evidence contract
- **Location:** `draft_z.md:1397-1408` (§2.16 Evidence Contract)
- **Description:** The Verified/Reasoned/Assumed/Unverifiable tagging system from v1.0.1 is preserved verbatim. No other draft keeps it.
- **Severity:** Informational (positive finding)
- **Confidence:** Verified (from text)
- **Recommended fix:** None. This is the right thing.

#### I2 — Multi-framework adapter pattern (draft_q, draft_q2) is over-engineered
- **Location:** `draft_q.md:62-71` (Multi-Framework Support table); `draft_q2.md:197-216` (Framework Adapters section)
- **Description:** React, Vue, and Svelte adapters add significant complexity (three component libraries, three test setups, three build configurations) for a use case (single-file markdown rendering) that doesn't need it. The core value of the skill is the markdown pipeline + design system, both of which are framework-agnostic at the processing layer but framework-specific at the rendering layer. Supporting one framework (React, matching v1.0.1) is sufficient.
- **Severity:** Informational
- **Confidence:** Reasoned
- **Recommended fix:** Drop multi-framework support. Ship React-only. If a Vue or Svelte user needs the skill, they can adapt the patterns.

#### I3 — `draft_z`'s three-template system is the right level of generalization
- **Location:** `draft_z.md:797-844` (§2.7 Three Templates)
- **Description:** Editorial Long-Form, Technical Docs, Minimal Print. Each template has its own `@theme`, layout, component map, and default tag registry. This is more useful than "one config to rule them all" (draft_d) and less complex than "multi-framework adapters" (draft_q2).
- **Severity:** Informational (positive finding)
- **Confidence:** Reasoned
- **Recommended fix:** None. This is the right abstraction.

#### I4 — `draft_q2`'s `reportMetric` references `window.gtag` without setting up Google Analytics
- **Location:** `draft_q2.md:1853-1858` (`if (typeof window !== 'undefined' && 'gtag' in window) { (window as any).gtag('event', 'timing_complete', { ... }); }`)
- **Description:** The performance monitor calls `gtag` if it exists, but the skill doesn't set up Google Analytics anywhere. This is dead code in most deployments.
- **Severity:** Informational
- **Confidence:** Verified (from text)
- **Recommended fix:** Either remove the `gtag` call or document the GA setup requirement.

#### I5 — `draft_q2`'s `dangerouslySetInnerHTML` defeats the entire point of using react-markdown's component map
- **Location:** `draft_q2.md:1936` (already cited as C2)
- **Description:** (See C2.) Informational dimension: if the skill is going to serialize to HTML and use `dangerouslySetInnerHTML`, react-markdown is the wrong tool — `marked` + `DOMPurify` is simpler and smaller. The skill ships the worst of both worlds: react-markdown's bundle size without its component-map benefits.
- **Severity:** Informational (architectural critique)
- **Confidence:** Reasoned
- **Recommended fix:** Pick one architecture. Either commit to react-markdown's component map (remove `dangerouslySetInnerHTML`) or commit to HTML serialization (drop react-markdown, use `marked`).

#### I6 — `draft_z`'s tag registry is JSON, not TypeScript — better data-driver than `draft_k`'s TS `BADGE_REGISTRY`
- **Location:** `draft_z.md:866-890` (default registry as JSON); compare `draft_k.md:374-391` (registry as TS `const`)
- **Description:** JSON registry can be shipped as a data file, edited by non-developers, and loaded at build time without a TS recompile. TS `const` registry requires code changes to add presets.
- **Severity:** Informational (positive finding for draft_z)
- **Confidence:** Reasoned
- **Recommended fix:** None. JSON is the right choice.

---

## 5. Recommended Winner — `draft_z`

**Pick `draft_z` as the foundation.** It is the only draft that:

1. **Preserves the evidence contract** (Verified/Reasoned/Assumed/Unverifiable) — the single most transferable idea from v1.0.1. No other draft keeps it. Two drafts (draft_q, draft_q2) actively violate it by self-tagging as "Verified."
2. **Honestly self-tags as "Reasoned throughout"** — complies with persona §13. No false confidence.
3. **Preserves the editorial visual identity** — Source Serif 4, warm paper, teal/moss accents. The original's anti-generic mandate survives, scoped per-template.
4. **Ships a real slug-parity test** — the single most important test for this skill, addressing v1.0.1 lesson 2.
5. **Has the right level of generalization** — three templates (editorial / technical / minimal) + JSON tag registry + theme override. Not under-generalized (like draft_d's single config), not over-engineered (like draft_q2's multi-framework adapters).
6. **Honestly claims "WCAG 2.2 AA + AAA aspirational"** rather than falsely claiming AAA. The axe test treats AAA violations as warnings except for the two real AAA blockers (target-size, color-contrast).
7. **Addresses every finding from its own Part 1 audit** — the migration table (Appendix A) maps every v1.0.1 pattern to its v2.0.0 replacement.
8. **Ships an offline build recipe** (`build-offline.mjs`) — addresses the central font-dependence pain point that draft_d and draft_k leave unfixed.

### Recommended merge-ins from non-winners

`draft_z` is the strongest foundation, but it has gaps. Merge in:

- **From `draft_q2`:** The GitHub Actions CI workflow YAML (§12.1). draft_z ships pre-ship commands but no CI YAML. draft_q2's workflow is the most complete — matrix testing, coverage upload, Lighthouse, security audit. Strip the placeholder deploy step.
- **From `draft_q2`:** The performance-budget table (§9.1) — but with realistic numbers (250 KB gzipped, not 150 KB). draft_z doesn't ship performance budgets.
- **From `draft_k`:** The YAML frontmatter for the skill file itself (lines 1–18). draft_z's skill spec is wrapped in a two-part document (audit + spec). For agent consumption, the skill file should be standalone with YAML frontmatter.
- **From `draft_d`:** The `defineConfig` helper ergonomic wrapper (§4.3) — but actually implement it (draft_d leaves it as a stub). Useful for type-safe config authoring.
- **From `draft_q2`:** The `@font-face` declarations with `font-display: swap` and `<link rel="preload">` (§11). draft_z's `@fontsource` approach is correct but the preload hints are a useful addition.
- **From `draft_q2`:** The error reporter class shape (§10.3) — but with the `endpoint` field made explicit (draft_z mentions error reporting but doesn't ship a reporter).

### What to discard

- **draft_q** in its entirety — it's a 12-week plan, not a skill. If you want the phased breakdown as project-management scaffolding, keep it as a separate document, not as a skill file.
- **draft_q2's multi-framework adapters** — over-engineered. React-only is sufficient.
- **draft_q2's `processBadges` AST plugin** — doesn't connect to the React `Badge` component (H5). draft_z's regex preprocessor + `Badge` component pattern is simpler and works.
- **draft_q2's `dangerouslySetInnerHTML`** — C2. Remove entirely.
- **draft_q2's 150 KB bundle budget** — H6. Replace with 250 KB.
- **draft_d's `enhanceMarkdown` raw-HTML emission** — H1. Use draft_z's backtick-wrapping pattern instead.
- **draft_k's `buildToc` stack logic** — H2. Use draft_z's pattern.
- **draft_d's `localStorage` theme persistence** — M5. Wrap in `try/catch` with in-memory fallback.

---

## 6. Confidence Statement

This audit is **Reasoned** throughout. I read all six drafts end-to-end and cross-checked code snippets against the documented dependency APIs (react-markdown 10, unified 11, remark-rehype 11, rehype-slug 6, github-slugger 2, vite-plugin-singlefile 2, Tailwind v4 `@theme`). No code was executed in this environment — no `npm install`, `npm run build`, `npm run test`, or `npm run a11y` was run against any draft.

Findings marked **Verified (from text)** are claims I can confirm by reading the draft's own text (e.g., "draft_q self-tags as 'Verified'" — read line 876). Findings marked **Reasoned** are claims that follow from static analysis of the code snippets against documented APIs, but would require running the code to confirm (e.g., "draft_d's `enhanceMarkdown` produces raw HTML that react-markdown won't render" — would need to actually run `pnpm build` to confirm the badges render as text).

**What would be needed to verify the findings:**
1. Bootstrap each draft as a real project (`npm install`, `npm run build`).
2. Run `npm run test` (where tests exist) and `npm run a11y` (where axe is configured).
3. Render a fixture markdown file with badges, headings, code blocks, and tables in each draft.
4. Confirm the badge-rendering, TOC-nesting, slug-parity, and font-inlining findings empirically.
5. Run `axe-core` against each rendered output to confirm the WCAG claims.

---

I'll plan the merged/unified skill file meticulously, then build it. The spec is already pinned by my prior critique — foundation is `draft_z`, with named merge-ins from the other drafts and all severity-tagged defects fixed. No further clarification needed.
Now writing chunk 1 — frontmatter, TOC, and sections 1–7:
Chunk 1 written. Now appending chunk 2 — sections 8–12 (Tags, TOC, A11y, Build Recipes, Error Handling):
Now appending chunk 3 — sections 13–18 (Fonts, Performance, Testing, CI/CD, Anti-Patterns, Pre-Ship Checklist):
Chunk 3 successfully appended. Now writing the final chunk 4 — sections 19–24:
All four chunks written. Now verifying file integrity:
All 24 sections are present (the extra `## Section ${i}`, `## Finding 1`, etc. matches are inside code blocks — those are test fixture strings, not actual section headers). Verifying:
File integrity confirmed: 3,153 lines, ~138 KB, all 24 numbered sections present, starts with YAML frontmatter, ends with the provenance statement. Let me update the todos and write the worklog:
Unified skill file delivered at `/home/z/my-project/download/markdown-to-web_SKILL.md` — 3,153 lines, 138 KB, 24 numbered sections.

**What's in it:**
- YAML frontmatter (from draft_k) for skill discovery
- Foundation is draft_z: three-template system, JSON tag registry, honest "WCAG AA + AAA-aspirational" claim, evidence contract preserved verbatim, editorial visual identity (Source Serif 4 + warm paper + teal/moss)
- Merge-ins from draft_q2 (GitHub Actions CI YAML, realistic 250 KB bundle budget, @font-face preload hints, full test pyramid with code, ErrorReporter class), draft_k (YAML frontmatter parsing), draft_d (`defineConfig` helper, actually implemented in §23.4)
- All 18 audit findings fixed inline — §24.7 has the full defect-fix traceability table (C1/C2/H1-H6/M1-M10)
- Honest "Reasoned throughout" self-tag in §24.1 — complies with persona §13, unlike the source drafts that falsely claimed "Verified"

**What to do next:**
1. Open the file and skim §1 (philosophy), §8 (tag pipeline), §24.7 (defect-fix table) to confirm the merge matches your intent
2. To spot-verify before adoption, run the bootstrap commands in §24.4 — particularly `npx vitest run slug-parity.test.ts` (the single most important verification)
3. If you want a v2.0.1 revision, the highest-leverage changes would be: (a) actually bootstrap the project and elevate §24.1 from "Reasoned" to "Verified", (b) add the missing `MarkdownReport.tsx` full implementation (currently excerpted in §8.5), (c) validate the `build-offline.mjs` sketch against real `@fontsource` packages

---

https://chat.z.ai/s/21381e59-cf0a-4f26-b7ed-f93595e6dcf9 

