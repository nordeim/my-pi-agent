# Skill File Evolution Analysis: Critical Comparative Review

**Date:** 2026-08-06  
**Scope:** Five versions of the markdown-to-web rendering skill, from project-specific (v1.0.1) through four generalization drafts (draft_d, draft_k, draft_q2, draft_z).  
**Methodology:** Desk review against the coding agent's own standards (Section 12 audit discipline, Section 13 evidence contract, Section 19 Definition of Done). No code executed; findings tagged per the evidence contract.

---

## 1. Executive Summary

| Version | Words | Lines | H2 Sections | Purpose | Overall Score |
|---------|-------|-------|-------------|---------|---------------|
| **original_SKILL.md** (v1.0.1) | 4,552 | 629 | 22 | Project-specific audit report renderer | 3.0/5.0 |
| **draft_d.md** | 4,512 | 839 | 22 | First generalization attempt with config system | 2.8/5.0 |
| **draft_k.md** (v2.0.0) | 3,885 | 808 | 19 | Generalized renderer with frontmatter & presets | 3.1/5.0 |
| **draft_q2.md** | 7,638 | 2,560 | 40 | Enterprise-grade production skill | 3.9/5.0 |
| **draft_z.md** (v2.0.0 spec) | 10,748 | 1,555 | 3+28+36 | Validation review + specification | **4.6/5.0** |

**Verdict:** `draft_z.md` is the most effective skill document. It uniquely combines (a) a rigorous validation review of the original with 20+ classified findings, and (b) a concrete v2.0.0 specification that addresses every High/Medium finding. The other drafts generalize without first diagnosing, or over-engineer without grounding in the actual codebase.

---

## 2. Dimensional Scoring Matrix

| Dimension | original | draft_d | draft_k | draft_q2 | draft_z | Winner |
|-----------|----------|---------|---------|----------|---------|--------|
| **Structural Organization** | 5.0 | 4.0 | 4.0 | 3.0 | **5.0** | draft_z / original (tie) |
| **Technical Accuracy** | 4.0 | 3.0 | 4.0 | 4.0 | **4.0** | Three-way tie |
| **Completeness (Coverage)** | 3.0 | 4.0 | 4.0 | **5.0** | **5.0** | draft_q2 / draft_z (tie) |
| **Actionability for Agents** | 4.0 | 3.0 | 4.0 | 3.0 | **5.0** | draft_z |
| **Accessibility Depth** | 3.0 | 3.0 | 4.0 | **5.0** | **5.0** | draft_q2 / draft_z (tie) |
| **Testing Rigor** | 1.0 | 2.0 | 1.0 | **5.0** | 4.0 | draft_q2 |
| **Security Awareness** | 2.0 | 2.0 | 2.0 | **5.0** | 3.0 | draft_q2 |
| **Performance Awareness** | 2.0 | 2.0 | 2.0 | **5.0** | 4.0 | draft_q2 |
| **Honesty / Evidence Contract** | **5.0** | 2.0 | 2.0 | 2.0 | **5.0** | original / draft_z (tie) |
| **Generalization Quality** | 1.0 | 3.0 | 4.0 | 3.0 | **5.0** | draft_z |
| **Maintainability** | 3.0 | 3.0 | 3.0 | 3.0 | **5.0** | draft_z |
| **Overall Effectiveness** | 3.0 | 3.0 | 3.0 | 4.0 | **5.0** | draft_z |
| **Average** | 3.0 | 2.8 | 3.1 | 3.9 | **4.6** | **draft_z** |

---

## 3. Version-by-Version Critical Analysis

### 3.1 original_SKILL.md (v1.0.1) — The Baseline

**What it is:** A project-specific skill for one React app (`react-markdown-report`) that renders a single Markdown audit report. 8 files, 458 LOC.

**Strengths (genuinely excellent):**
- **Evidence contract preserved verbatim.** Every finding in the skill itself is tagged Verified/Reasoned/Assumed/Unverifiable. This is the single most transferable pattern.
- **Design system is code-first and complete.** The `@theme` block, color reference table, z-index map, and typography hierarchy are exhaustive. An agent can reconstruct the visual identity without looking at the code.
- **Anti-patterns and debugging tables are concrete.** Symptom → Cause → Fix, with file:line references. This is exactly what an agent needs at 2 AM.
- **Honest about limitations.** It documents its own WCAG AAA failures, font offline gap, and dead `cn.ts` code. This intellectual honesty is rare.

**Critical Weaknesses:**
- **Finding 1.1 (High): Over-fit scope.** Every module serves one report (`kelp.agency` vs. `astro.jesspete.shop`). The badge system hardcodes 9 keys. The content path is `comparative-analysis.md`. An agent cannot invoke this skill for a different document without forking.
- **Finding 8.1 (High): WCAG AAA claim is contradicted by evidence.** §1 claims "WCAG AAA where feasible" but §8 documents 36×36 px touch targets (fails 2.5.5), browser-default focus outlines (inconsistent), and badge text at 4.76:1 (fails AAA for 12 px text). The skill is honest about the failures in §8 but the headline claim in §1 overstates.
- **Finding 11.1 (High): No automated quality gates.** Pre-ship is `tsc --noEmit && npm run build` plus manual smoke test. No lint, no tests, no axe, no CI. For a skill that documents 8 files and 458 LOC, this is survivable; for any generalized version, it is the highest-leverage gap.
- **Finding 3.2 (High): "Single-file portability" is half-true.** `vite-plugin-singlefile` inlines JS/CSS but not `@import`ed Google Fonts. The artifact requires network at runtime. In air-gapped or archival contexts, the bespoke editorial design degrades to system fallbacks.
- **Finding 7.1 (Medium): Badge protocol is too narrow.** Only `Severity` and `Confidence` bullets are processed. A changelog, status report, or compliance matrix cannot use the badge system.
- **Finding 7.2 (Medium): `enhance.ts` regex is fragile.** Requires exact `- **Severity:**` syntax. `* **Severity:**` (asterisk bullet) or `1. **Severity:**` (ordered list) are silently skipped.
- **Finding 4.3 (High): No `prefers-reduced-motion` guard.** `html { scroll-behavior: smooth; }` is unguarded. The skill acknowledges this as a known gap but does not fix it.
- **Finding 5.1 (Low): `cn.ts` is dead code.** Imported nowhere. Strict `tsc` catches it, but it suggests incomplete scaffolding cleanup.

**Reuse Value Assessment:**
| Module | Reuse | Action |
|--------|-------|--------|
| `@theme` token approach | High | Generalize per-template |
| `enhance.ts` preprocessor pattern | High | Extend regex to registered tags |
| `toc.ts` slugger-sharing pattern | High | Preserve; add unit test |
| `MarkdownReport.tsx` components map | High | Allow template override |
| `StatusBadge` | Medium | Replace with tag registry |
| Evidence contract | **Very High** | Preserve verbatim |
| Severity token palette | Medium | Replace with generic accent scale |
| Anti-pattern tables | High | Expand and link to tests |

---

### 3.2 draft_d.md — First Generalization Attempt

**What it is:** Attempts to turn the single-purpose skill into a configurable `markdown-to-web` system via a `MarkdownToWebConfig` interface.

**Strengths:**
- First to introduce a **configuration schema** (§3.1) with TypeScript interfaces for theme, badges, images, accessibility, and output.
- Adds **custom hooks** (`useTheme`, `useConfig`, `useToc`, `useDrawer`) — good architectural separation.
- Adds **image embedding** (base64 for small files, linked for large) — a practical feature.
- Adds **dark mode** (`'auto' | true | false`) and **theme toggle**.
- Expands pre-ship to include lint, test, and format gates.

**Critical Weaknesses:**
- **Configuration schema is over-engineered.** The `MarkdownToWebConfig` interface has 8 top-level properties with nested objects 3-4 levels deep. For a skill that originally worked with zero config, this is a significant complexity increase. The `defineConfig` helper is mentioned but not shown in implementation detail.
- **§3.3 "Loading the Configuration" is vague.** States that "a Vite plugin reads the config file and creates a virtual module `virtual:config`" but provides no code for this plugin. This is a hand-wavy abstraction that an agent cannot implement from the skill alone.
- **Badge patterns use regex in config.** The `badges.patterns` array accepts `RegExp` objects in a JSON/TS config. This is powerful but dangerous — regex in config files is a common source of runtime errors that are hard to debug.
- **No actual test code.** Mentions Vitest + RTL + axe-core but shows zero test fixtures, zero test files, zero assertions. The testing section is aspirational, not actionable.
- **No validation of the original skill.** draft_d generalizes without first reviewing what was broken in v1.0.1. The WCAG AAA over-claim, font offline gap, and badge fragility are carried forward unexamined.
- **Template system is absent.** The config approach implies one design system per project. There is no concept of swappable templates (editorial vs. technical vs. minimal).

**Verdict:** A step in the right direction but adds complexity without solving the core structural problems. The configuration schema is more detailed than the implementation it describes.

---

### 3.3 draft_k.md (v2.0.0) — The Generalized Renderer

**What it is:** A cleaner generalization than draft_d, with frontmatter support, badge presets, error boundaries, and syntax highlighting.

**Strengths:**
- **Badge registry is a genuine improvement.** Replaces hardcoded 9 keys with a `BADGE_REGISTRY` object where presets ("audit", "docs") define their own categories and values. This is the right abstraction — badges are data, not code.
- **Frontmatter support** (§5.2) with YAML parsing via regex. Extracts title, subtitle, author, date, badgeConfig, theme. Falls back gracefully.
- **Error boundaries** (§10) with `ErrorFallback` component. Catches Markdown parse errors, React render errors, runtime exceptions.
- **Syntax highlighting** via `rehype-highlight` + `highlight.js`. Light/dark theme support.
- **`prefers-reduced-motion` is finally implemented** (§4.3). Fixes the v1.0.1 gap.
- **TOC depth extended to H4** (configurable). Fixes the v1.0.1 limitation.
- **Migration appendix** (Appendix C) maps v1 → v2 changes explicitly.

**Critical Weaknesses:**
- **Still no actual test code.** Like draft_d, it mentions testing but provides no fixtures, no assertions, no test files. The "Pre-Ship Checklist" is `tsc --noEmit && npm run build && npm run preview` — identical to v1.0.1's gate, just with more smoke-test items.
- **No lessons learned section.** v1.0.1's §12 was one of its best features — five concrete lessons with "how to avoid." draft_k drops this entirely.
- **No validation review.** Like draft_d, it generalizes without critiquing. The WCAG AAA over-claim is softened to "AAA where feasible" but the same contradictions (touch targets, badge contrast) are not addressed.
- **Frontmatter parser is regex-based.** The YAML frontmatter extraction uses `markdown.match(/^---\n([\s\S]*?)\n---\n/)` and manual line splitting. This is fragile for nested YAML, quoted strings with colons, and multi-line values. `gray-matter` is the correct dependency but not mentioned.
- **Badge registry is hardcoded in TS.** The `BADGE_REGISTRY` is a TypeScript object in `src/lib/badges.ts`. Adding a new preset requires editing source code. A JSON-based registry (per template) would be more flexible.
- **No offline font strategy.** Still relies on Google Fonts `@import` with the same runtime network dependency as v1.0.1.

**Verdict:** A solid v2.0.0 design document. The badge registry and frontmatter are genuine architectural improvements. But it lacks the critical review discipline that would make it trustworthy, and it still has no testing infrastructure.

---

### 3.4 draft_q2.md — The Enterprise Over-Engineering

**What it is:** A comprehensive "production-grade" skill document targeting enterprise standards with multi-framework adapters, AST-based processing, exhaustive testing, CI/CD, performance budgets, and security hardening.

**Strengths (genuinely impressive):**
- **Most comprehensive testing strategy.** Unit tests with 100% coverage targets, integration tests, accessibility tests with axe-core, visual regression with Playwright, performance tests with bundle-size budgets. This is the only draft that shows actual test code.
- **AST-based badge processing** (§5.3) using `unist-util-visit`. This is technically superior to regex preprocessing — it operates on the Markdown AST, not raw strings, making it robust against formatting variations.
- **Performance budgets** (§9.1) with explicit thresholds: < 150 KB gzipped bundle, < 1.5s FCP, < 100ms for 1000-line parse.
- **Security hardening:** DOMPurify for XSS prevention, CSP headers, dependency auditing, license compatibility checks.
- **CI/CD pipeline** (§12.1) with GitHub Actions workflow covering lint, typecheck, test (unit + integration + a11y), build, bundle analysis, E2E, visual regression, Lighthouse, and security audit.
- **Multi-framework adapter pattern** (§2.2) with React, Vue, and Svelte adapters.
- **Error boundaries at every layer** (§10.1) — nested boundaries for granular error handling.

**Critical Weaknesses:**
- **Multi-framework support is YAGNI.** The skill document is for an AI agent generating a React + Vite + Tailwind project. Adding Vue and Svelte adapters triples the scope without a clear use case. No user has asked for this; it bloats the skill and distracts from the React implementation.
- **AST-based processing adds significant complexity.** The `processBadges` plugin (§5.3) requires understanding `unified`, `remark`, `mdast`, `unist-util-visit`, and the hProperties API. For an agent that needs to generate a working renderer in one session, this is a high cognitive load. The regex approach (v1.0.1, draft_k, draft_z) is simpler and sufficient for 99% of cases.
- **The document is 2,560 lines long.** This is 4× the original skill. An agent reading this skill will spend more time navigating the document than implementing the code. The signal-to-noise ratio degrades.
- **No validation of the original skill.** Despite being the most comprehensive document, it does not review or critique v1.0.1. It presents itself as a greenfield specification rather than an evolution.
- **Commands are scattered throughout.** Build commands appear in §3, §11, §12, and §17. There is no single "quickstart" path.
- **Some code is speculative.** The `PerformanceMonitor` class (§9.3) and `ErrorReporter` class (§10.3) are well-designed but add dependencies (`gtag`, `ERROR_REPORTING_ENDPOINT`) that are not in the dependency list. The `LargeDocumentViewer` with `@tanstack/react-virtual` is a nice-to-have, not a must-have.
- **No migration path from v1.0.1.** Despite being positioned as the "production-grade" successor, there is no appendix mapping v1 → v2 changes.

**Verdict:** An excellent reference for "what does production-grade look like" but too heavy for a skill file. It reads like an architecture decision record (ADR) combined with a coding standard, not a concise skill an agent can execute. The multi-framework adapters and AST-based processing should be extracted into an "advanced patterns" appendix, not the main flow.

---

### 3.5 draft_z.md — The Validation Review + v2.0.0 Spec

**What it is:** Two documents in one: (1) a rigorous validation review of `react-markdown-report` v1.0.1 with 20+ classified findings, and (2) a concrete `markdown-to-web` v2.0.0 specification that addresses every finding.

**Strengths (exceptional):**
- **Part 1: Validation Review is the single most valuable artifact across all five documents.** It applies the skill's own audit discipline (Section 12) to the skill itself. Every finding has: Location, Description, Evidence, Impact, Severity, Confidence, Recommended Fix. This is meta-quality at its finest.
- **Findings are honest and self-aware.** It identifies the WCAG AAA over-claim (Finding 8.1), the font offline gap (Finding 3.2), the badge fragility (Finding 7.2), and the dead `cn.ts` code (Finding 5.1). It does not shy away from calling the original's scope "over-fit" (Finding 1.1).
- **Part 2: v2.0.0 specification is grounded in the findings.** Every recommendation in Part 2 maps to a specific finding in Part 1. For example, the `prefers-reduced-motion` media query (§2.6) fixes Finding 4.3; the 44 px touch targets (§2.10) fix Finding 8.1; the tag registry (§2.8) fixes Findings 7.1 and 7.2.
- **Three-template system is practical.** Editorial (default, v1.0.1 design), Technical (API docs), Minimal (print). Each template has its own `@theme`, component map, layout, and default tag registry. This solves the over-fit problem without over-engineering.
- **Tag registry is elegant.** JSON-based, per-template, with a 5-step accent scale (`accent-1` through `accent-5`) replacing hardcoded severity tokens. The `enhance.ts` regex accepts all bullet styles (`-`, `*`, `+`, `1.`) and emits build-time warnings for unknown tags/values.
- **Slug parity test** (§2.9) is a concrete, runnable test fixture with 11 edge cases (emoji, CJK, backticks, repeated headings, whitespace). This fixes Finding 2.2.
- **Offline build mode** (§2.11, Recipe B) uses `@fontsource` packages and `assetsInlineLimit` to produce a truly self-contained artifact. This fixes Finding 3.2.
- **Pre-ship checklist has 8 hard gates** (§2.13): typecheck → lint → test → a11y → build → smoke → verify deps → verify offline. No gate may be skipped.
- **Evidence contract is preserved verbatim.** §2.16 restates the Verified/Reasoned/Assumed/Unverifiable tags and adds the critical rule: "Never upgrade a tag."
- **Honest about unverified code.** The "Verification Ledger" at the end explicitly states: "No project was bootstrapped; no `npm install` was executed." The `build-offline.mjs` script is labeled a "sketch." This intellectual honesty is exactly what the coding agent instructions demand.

**Weaknesses (minor):**
- **Part 2 is a specification, not an implementation.** The code snippets are starting points that require runtime validation. This is acknowledged, but an agent implementing from this skill will need to iterate.
- **No actual test files are provided.** The slug-parity test and enhance test are shown as code blocks but not as committed files. An agent would need to create these.
- **CI/CD is conceptual, not a complete workflow file.** §2.11 describes build recipes but does not provide a full `.github/workflows/ci.yml` like draft_q2 does.
- **The document is 1,555 lines but dense.** The two-part structure (review + spec) requires the reader to cross-reference findings. A single integrated document might be easier to follow.

**Verdict:** The most effective skill document. It combines critical review with constructive specification, maintains intellectual honesty throughout, and produces a design that is generalized without being over-engineered. The three-template system and tag registry are the right abstractions.

---

## 4. Comparative Gap Analysis

### 4.1 What Each Version Adds (Evolution Chain)

```
original (v1.0.1)
    ├───> draft_d: +Config system, +Custom hooks, +Image embedding, +Dark mode
    │           ──: No critique, no tests, over-engineered config
    │
    ├───> draft_k: +Badge registry, +Frontmatter, +Error boundaries, +Syntax highlighting
    │           ──: No critique, no tests, no offline fonts
    │
    ├───> draft_q2: +AST processing, +Multi-framework, +Full testing pyramid, +CI/CD
    │           ──: No critique, over-engineered, YAGNI adapters, 2560 lines
    │
    └───> draft_z: +Validation review (20 findings), +3 templates, +Tag registry
                +Slug parity test, +Offline build, +8-gate pre-ship
                ──: Spec not implementation, no committed test files
```

### 4.2 Topic Coverage Matrix

| Topic | original | draft_d | draft_k | draft_q2 | draft_z |
|-------|----------|---------|---------|----------|---------|
| Project Identity | Specific | Generalized | Generalized | Enterprise | Generalized + templates |
| Tech Stack | Pinned exact | Pinned exact | Semver ranges | Semver ranges | **Pinned exact** |
| Config System | ❌ | Full TS schema | Frontmatter only | ❌ | **Tag registry JSON** |
| Design System | Complete | CSS variables | Extended tokens | Comprehensive | **Per-template @theme** |
| Badge System | 9 hardcoded keys | Configurable regex | Registry presets | AST-based | **Tag registry (data-driven)** |
| TOC | H2/H3 only | Configurable levels | H2/H3/H4 | Configurable depth | **H2-H4 + slug parity test** |
| Accessibility | Claims AAA, documents failures | AA claimed | AAA claimed | AAA checklist | **AA + AAA aspirational (honest)** |
| Testing | ❌ | Mentioned only | ❌ | Comprehensive pyramid | **Vitest + axe + Playwright** |
| CI/CD | ❌ | ❌ | ❌ | GitHub Actions | **Conceptual workflow** |
| Error Boundaries | ❌ | ❌ | ✅ | Nested | **Root + content** |
| Syntax Highlighting | ❌ | highlight.js | rehype-highlight | rehype-prism | **rehype-highlight opt-in** |
| Dark Mode | ❌ | `'auto'|true|false` | ❌ | Dark tokens | **Light/dark/system toggle** |
| Reduced Motion | ❌ (acknowledged gap) | Configurable | ✅ | Full media query | **Full media query** |
| Offline Fonts | ❌ (acknowledged gap) | Embed or link | ❌ | Self-hosted strategy | **Online + offline modes** |
| Validation Review | ❌ | ❌ | ❌ | ❌ | **20 classified findings** |
| Migration Guide | ❌ | Appendix A | Appendix C | ❌ | **Detailed migration table** |
| Evidence Contract | ✅ | ❌ | ❌ | ❌ | **Preserved verbatim** |

---

## 5. Critical Findings Summary

### 5.1 Findings in original_SKILL.md (from draft_z's Part 1)

| # | Finding | Severity | Status in draft_z |
|---|---------|----------|-------------------|
| 1.1 | Over-fit scope (one report only) | High | Fixed: 3 templates |
| 1.2 | Anti-generic mandate conflicts with reuse | Medium | Fixed: Per-template mandate |
| 2.2 | Slug parity asserted, not verified | Medium | Fixed: `slug-parity.test.ts` |
| 3.2 | Fonts require runtime network | High | Fixed: Offline build mode |
| 4.2 | Severity palette hardcoded | Medium | Fixed: 5-step accent scale |
| 4.3 | No `prefers-reduced-motion` | High | Fixed: Media query in CSS |
| 4.4 | No dark mode | Low | Fixed: Light/dark/system toggle |
| 5.1 | `cn.ts` dead code | Low | Fixed: Used in `Badge.tsx` |
| 5.2 | `enhanceReportMarkdown` at render time | Low | Fixed: Memoized or module-load |
| 7.1 | Badge protocol too narrow | Medium | Fixed: Tag registry |
| 7.2 | Regex fragile to bullet variation | Medium | Fixed: Accepts all bullet styles |
| 8.1 | WCAG AAA claim contradicted | High | Fixed: Honest "AA + AAA aspirational" |
| 8.2 | Focus styles rely on browser default | Medium | Fixed: Global `:focus-visible` |
| 8.3 | No automated a11y test | Medium | Fixed: `npm run a11y` gate |
| 8.4 | Badge text contrast fails AAA | Medium | Fixed: 14 px badge text |
| 11.1 | Quality gate too narrow | High | Fixed: 8 hard gates |
| 17.1 | Only `sm`/`lg` breakpoints | Low | Fixed: Template-dependent |
| 19.1 | Color reference manual (drift risk) | Low | Fixed: Auto-generate script |
| 20.1 | Only `TocItem` is named interface | Low | Fixed: `types/` directory |
| A.1 | Appendix A (`.agents/`) is stale | Info | Fixed: Deleted |

### 5.2 New Issues Introduced by Drafts

| Draft | Issue | Severity |
|-------|-------|----------|
| draft_d | Config schema over-engineered (8 nested properties) | Medium |
| draft_d | "Virtual module" loading is hand-wavy | Medium |
| draft_d | Regex in config files is dangerous | Medium |
| draft_k | Frontmatter parser is regex-based (fragile) | Medium |
| draft_k | No lessons learned section (dropped from v1) | Low |
| draft_q2 | Multi-framework adapters are YAGNI | High |
| draft_q2 | AST-based processing is overkill for skill context | Medium |
| draft_q2 | 2,560 lines — too long for a skill file | Medium |
| draft_q2 | No migration path from v1.0.1 | Medium |
| draft_z | Spec code not runtime-verified | Low |
| draft_z | No committed test files | Low |
| draft_z | CI/CD is conceptual, not a complete workflow | Low |

---

## 6. Recommendations

### 6.1 Immediate Action: Adopt draft_z as the Canonical Skill

**draft_z.md** should be the canonical `markdown-to-web_SKILL.md`. It is the only document that:
1. Critically reviews the original before generalizing
2. Addresses every High and Medium finding with a concrete fix
3. Maintains the evidence contract (Verified/Reasoned/Assumed/Unverifiable)
4. Balances completeness with practicality (not over-engineered)
5. Provides a clear migration path from v1.0.1

### 6.2 Merge Select Elements from draft_q2

Extract these high-value sections from draft_q2 and append them to draft_z as "Advanced Patterns" appendices:
- **§8 Testing Strategy** (test pyramid, unit test fixtures, integration tests, a11y tests, visual regression) — but keep it React-only, drop Vue/Svelte.
- **§9 Performance Optimization** (performance budgets, bundle size checks, parsing speed benchmarks) — lightweight, no `PerformanceMonitor` class unless requested.
- **§12 CI/CD** (GitHub Actions workflow) — as a complete `.github/workflows/ci.yml` file, not scattered commands.
- **§10 Error Handling** (nested error boundaries, error reporter) — but simplify; no external endpoint dependency.

### 6.3 Retain from original_SKILL.md

These sections from v1.0.1 are superior to all drafts and should be preserved verbatim:
- **§1 Design Philosophy** (anti-generic mandate, evidence contract)
- **§4 Design System** (code-first `@theme`, color reference completeness)
- **§9 Anti-Patterns & Common Bugs** (symptom-cause-fix format)
- **§12 Lessons Learnt** (5 lessons with "how to avoid")
- **§19 Color Reference (Complete)** (exhaustive token-to-class mapping)

### 6.4 Drop from All Drafts

| Element | Reason |
|---------|--------|
| Multi-framework adapters (draft_q2) | YAGNI; skill is React-specific |
| AST-based badge processing (draft_q2) | Overkill; regex + tag registry is sufficient |
| `PerformanceMonitor` class (draft_q2) | Adds complexity without clear benefit for static renderer |
| `ErrorReporter` with external endpoint (draft_q2) | Requires runtime env vars; breaks single-file portability |
| `@tanstack/react-virtual` (draft_q2) | YAGNI for typical document lengths |
| `defineConfig` helper (draft_d) | Adds abstraction layer not justified by complexity |
| Regex in config `badges.patterns` (draft_d) | Dangerous; tag registry (draft_z) is safer |

### 6.5 Proposed Unified Structure

The final skill should follow draft_z's two-part structure but integrate the best of draft_q2's testing depth:

```
Part 1 — Validation Review (retain from draft_z)
  → 20 classified findings with severity/confidence/fix

Part 2 — markdown-to-web v2.0.0 Specification (retain from draft_z, enhance)
  §1  Identity & Design Philosophy (from original + draft_z)
  §2  When to Use / When Not To (from draft_z)
  §3  Inputs Contract (from draft_z)
  §4  Tech Stack & Pinned Versions (from original + draft_z)
  §5  Project Skeleton (from draft_z)
  §6  Design System (from original + draft_z per-template)
  §7  Three Templates (from draft_z)
  §8  Tag Registry & Badge Protocol (from draft_z)
  §9  TOC + Navigation (from draft_z + slug parity test)
  §10 Accessibility (from draft_z + draft_q2 depth)
  §11 Build & Deploy Recipes (from draft_z)
  §12 Anti-Patterns & Pitfalls (from original + draft_z)
  §13 Pre-Ship Checklist (from draft_z + draft_q2 testing)
  §14 Debugging Guide (from original + draft_z)
  §15 Extending the Skill (from draft_z)
  §16 Evidence Contract (from original, preserved)
  Appendix A — Migration from v1.0.1 (from draft_z)
  Appendix B — Complete TypeScript Reference (from draft_z)
  Appendix C — Testing Fixtures (NEW: from draft_q2, React-only)
  Appendix D — CI/CD Workflow (NEW: from draft_q2)
  Appendix E — Advanced Patterns (NEW: from draft_q2, optional)
```

---

## 7. Verification Ledger

| Claim | Basis | Confidence |
|-------|-------|------------|
| draft_z is the most effective skill | Scoring matrix: 4.6/5.0 average | Reasoned |
| original has 20+ findings | draft_z Part 1 enumerates 20 | Verified (from draft_z text) |
| draft_q2 is over-engineered | Multi-framework adapters, 2560 lines, no user request | Reasoned |
| draft_d config is over-engineered | 8 nested properties, vague "virtual module" | Reasoned |
| draft_k drops lessons learned | Absence of §12 equivalent | Verified (from draft_k text) |
| No draft except draft_z validates the original | Absence of critique sections in d/k/q2 | Verified |
| Proposed unified structure is feasible | All sections exist across the five documents | Reasoned |

---

*Analysis produced following the coding agent's Section 12 (Audit Discipline) and Section 13 (Evidence-Based Verification) protocols. All findings are classified by severity and confidence. Recommendations are concrete, not vague.*
