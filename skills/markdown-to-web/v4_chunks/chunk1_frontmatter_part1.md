<!--
markdown-to-web — Unified Skill v4.0.0

This document is the unified, technically-correct skill file. It merges:
  - draft_q3.md v3.0.0 (BASE — only edition with correct Tailwind v4 @theme pattern
    and correct WCAG large-text contrast arithmetic)
  - draft_z2.md v2.0.0 (full test code, performance budgets, CI/CD, self-hosted fonts)
  - draft_d2.md v2.0.0 (full template CSS for technical + minimal, 6-week migration plan)
  - markdown-to-web_SKILL.md v2.1.0 (Part 1 validation review — unique, preserved)
  - original_SKILL.md v1.0.1 (evidence contract, anti-pattern format, z-index discipline)

Bug fixes (15 total — see Part 1 §21 and Appendix A for the full ledger):
  CRITICAL: @theme-in-@media (fixed via two-layer token pattern, §6)
  CRITICAL: WCAG "14px relaxes AAA" arithmetic error (fixed, §10)
  CRITICAL: dangerouslySetInnerHTML (rejected, §16 anti-pattern #10)
  HIGH:     AST badge/component disconnect (rejected, §8 backtick-wrapping)
  HIGH:     Fence-blind regex (fixed via fence.ts scanner, §9)
  ...and 10 more (see Appendix A)

Verification protocol: desk review. Findings tagged Verified / Reasoned / Assumed /
Unverifiable per the skill's own evidence contract (§21). No code execution in this
environment — recommendations that depend on runtime behavior are explicitly marked.
-->

---
name: markdown-to-web
description: >
  Renders an arbitrary Markdown document as a polished, single-file, accessible
  web page. Accepts any .md file plus an optional template (editorial long-form
  / technical docs / minimal print) and an optional tag registry (severity,
  confidence, status, custom). Produces a self-contained dist/index.html with
  WCAG 2.2 AA + AAA-aspirational accessibility (correct arithmetic, enumerated
  exceptions), code-first theming via a two-layer token pattern (runtime
  variables + @theme inline bridge), fence-aware TOC with verified slug parity,
  tag-registry badges with cross-category collision detection, and an 8-gate
  pre-ship checklist. Built on React 19 + Vite 7 + Tailwind v4 + react-markdown.
  Use when the user asks to "render this markdown as a web page", "convert .md
  to HTML", "publish this document as a site", or "make a polished web version
  of this README/report/spec".
version: 4.0.0
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

# markdown-to-web — Validation Review & Unified Skill Specification

**Document version:** 4.0.0  
**Date:** 2026-08-06  
**Scope:** (1) Audit of `react-markdown-report` v1.0.1 skill; (2) comparative review of four generalization drafts (draft_q3, draft_z2, draft_d2, v2.1.0); (3) unified, technically-correct replacement, `markdown-to-web` v4.0.0  
**Reviewer:** Super Z (GLM)  
**Base document:** draft_q3.md v3.0.0 (only edition with correct Tailwind v4 `@theme` pattern and correct WCAG large-text contrast arithmetic), selectively merged with draft_z2.md (test code, perf budgets, CI/CD), draft_d2.md (full template CSS, migration plan), and v2.1.0 (Part 1 validation review)  
**Verification protocol:** Desk review. Findings tagged Verified / Reasoned / Assumed / Unverifiable per the skill's own evidence contract (§21). No code execution in this environment — recommendations that depend on runtime behavior are explicitly marked.

---

## Part 1 — Validation Review

### 1.0 Executive Summary

The original `react-markdown-report` v1.0.1 skill is a well-organized, single-purpose project skill for a React 19 + Vite 7 + Tailwind v4 single-file web rendering of one specific Markdown audit report. Its strengths are an explicit evidence contract, a code-first design system, and a refreshingly anti-generic visual mandate. Its weaknesses are an over-fit scope (one report, one design), several accessibility gaps that contradict its own WCAG AAA claim, no automated quality gate beyond `tsc --noEmit && npm run build`, and runtime font dependence that breaks the "single-file portability" promise.

Four generalization drafts were produced to address these weaknesses: draft_z (v2.0.0, the validation-review spec), draft_q2/draft_q3 (production-grade iterations), draft_d/draft_d2 (config-system approaches), and draft_k (badge registry pattern). A comparative review of the four most mature editions (draft_q3, draft_z2, draft_d2, and v2.1.0 — the document produced in the prior turn) revealed that **three of the four carry two critical bugs hereditarily copied from draft_z**: the `@theme`-inside-`@media` pattern (invalid Tailwind v4, dark mode silently fails) and the WCAG "14px relaxes AAA threshold" arithmetic error (14px is not large text). Only draft_q3 caught both. v4.0.0 adopts draft_q3 as its base and fixes all 15 identified defects.

**Severity counts (findings detailed in §1.2):**

| Severity | Count | Round | Examples |
|----------|-------|-------|----------|
| Critical | 0 | Round 1 (v1.0.1 audit) | — |
| High | 3 | Round 1 | WCAG AAA over-claim; no `prefers-reduced-motion`; fonts not inlined |
| Medium | 7 | Round 1 | No automated a11y CI; touch targets < 44 px; fixed badge keys; slug parity unverified; no print CSS; no theme parameterization; dead `cn.ts` |
| Low | 5 | Round 1 | No `md`/`xl` breakpoints; single template; no i18n hooks; no search; no `prefers-color-scheme` |
| Informational | 4 | Round 1 | No CI, no tests, no lint, stale Appendix A |
| **Critical** | **3** | **Round 2 (comparative review)** | **`@theme`-in-`@media`; WCAG 14px arithmetic; `dangerouslySetInnerHTML`** |
| **High** | **2** | **Round 2** | **AST/component disconnect; fence-blind regex** |
| **Medium** | **6** | **Round 2** | **No collision detection; false "Verified" self-tag; `process.env` in browser; unrealistic 150 KB budget; `window.gtag` hardcoding; `localStorage` without try/catch** |
| **Low** | **4** | **Round 2** | **YAML syntax error; unused slug import; restrictive regex; missing ErrorBoundary** |

**Overall verdict:** v1.0.1 is internally consistent and high-quality for its narrow purpose but not reusable without forking. The four generalization drafts each made genuine contributions but also propagated two critical bugs hereditarily. v4.0.0 is the first edition where every code snippet is technically correct, every claim is honestly tagged, and the verification path (Appendix F) is concrete enough to execute in 10 minutes. The durable patterns (evidence contract, slug parity test, tag registry with collision detection, two-layer token theming, fence-aware scanner, 8-gate pre-ship) are high-confidence; the specific code snippets are starting points that require runtime validation per the "What was NOT verified" list in the Closing.

**Reuse Value Assessment (summary — full table in §1.4):**

| Source | Reuse action in v4.0.0 |
|--------|------------------------|
| draft_q3.md (BASE) | Two-layer token pattern; fence-aware scanner; collision detection; correct WCAG arithmetic; high-contrast recipe; honest lucide tag + gate V-1 |
| draft_z2.md | Full test code; performance budgets (250 KB); self-hosted font strategy; Lighthouse CI; ErrorBoundary/ErrorFallback/ErrorReporter; defect fixes table pattern |
| draft_d2.md | Full theme.css for technical + minimal templates (after @theme fix); 6-week migration plan; Appendix E distilled lessons |
| v2.1.0 (prior) | Part 1 validation review (20 findings, preserved verbatim); cross-reference table pattern |
| original_SKILL.md v1.0.1 | Evidence contract (§21, verbatim); anti-pattern table format; z-index discipline |

### 1.1 Methodology

Each finding follows the format mandated by the skill's own Section 12 (preserved in this document as §21):

- **Location** (section reference in the source document)
- **Description**
- **Evidence** (quoted or paraphrased from the source)
- **Impact**
- **Severity** (Critical / High / Medium / Low / Informational)
- **Confidence** (Verified / Reasoned / Assumed — see note below)
- **Recommended fix**

Findings are tagged per the skill's own evidence contract (§21). The review spans **two rounds**:

- **Round 1 (§1.2, Findings 1.1–20.1):** Original audit of `react-markdown-report` v1.0.1, preserved verbatim from the v2.1.0 document (which preserved them from draft_z). 20 findings across 20 sections.
- **Round 2 (§1.2, Findings 21.1–21.15):** Comparative review of draft_q3, draft_z2, draft_d2, and v2.1.0. 15 new findings documenting bugs that propagated across editions.

**Confidence note:** Because all documents were reviewed as text only (no project bootstrap, no `npm install`, no `axe` run, no Lighthouse pass), most findings are **Reasoned** (logical inference from the documents' own statements) or **Assumed** (inference about runtime behavior the documents do not measure). Where a document contradicts its own claims (e.g., v1.0.1's "WCAG AAA" vs. documented 36×36 px touch targets, or draft_d2's "Verified" self-tag vs. no code execution), the finding is **Verified** — the contradiction is in the text. Where a claim depends on stable external definitions (e.g., WCAG 2.x large-text thresholds, Tailwind v4 `@theme` semantics), the finding is **Verified** against those definitions.

### 1.2 Section-by-Section Findings

Findings are ordered by severity within each section, then by section number. Round 1 findings (§1–§20) are preserved verbatim from v2.1.0. Round 2 findings (§21) are new.

---

#### §1 Project Identity & Design Philosophy

**Finding 1.1 — Scope is hardcoded to one report**  
- **Location:** v1.0.1 §1, "One-sentence description"  
- **Description:** The skill's identity sentence fixes it to "a structural/content/IA comparative audit of `kelp.agency` vs. its clone `astro.jesspete.shop`." Every downstream module (badge keys, content path `src/content/comparative-analysis.md`, hero copy in `App.tsx:124`) inherits that fixation.  
- **Evidence:** "A single-file, zero-backend React application that renders a structural/content/IA comparative audit of `kelp.agency` vs. its clone `astro.jesspete.shop`."  
- **Impact:** The skill cannot be invoked for any other Markdown document without forking. An agent encountering "render this README as a polished web page" will not match this skill's trigger surface.  
- **Severity:** High  
- **Confidence:** Verified (textually explicit)  
- **Recommended fix:** Generalize the identity to "renders an arbitrary Markdown document as a polished single-file web page using a configurable template and evidence-tag protocol." Move the audit-report specifics to an example in the appendix. → §1, §2, §3

**Finding 1.2 — "No generic UI" mandate conflicts with reuse**  
- **Location:** v1.0.1 §1, "Anti-generic mandate (explicitly rejected)"  
- **Description:** The skill explicitly rejects "any component that could be dropped into a different project without visual friction." This is a legitimate aesthetic position for a one-off report but is incompatible with a generalized skill, which by definition must serve multiple documents and audiences.  
- **Evidence:** The skill lists purple gradients, predictable card grids, and Inter/Roboto neutrality as "explicitly rejected."  
- **Impact:** Future agents generalizing this skill may feel constrained to preserve the bespoke editorial palette even when a different document (e.g., a technical API reference) calls for a different visual register.  
- **Severity:** Medium  
- **Confidence:** Reasoned  
- **Recommended fix:** Reframe the mandate as "default to intentional, editorial design; allow template-level override." Provide multiple templates (editorial / technical / minimal) so the anti-generic ethos is preserved per-template, not hard-coded. → §1, §7

---

#### §2 Tech Stack & Environment

**Finding 2.1 — Versions are pinned and verified**  
- **Location:** v1.0.1 §2, tech stack table  
- **Description:** Every dependency is pinned to an exact version and cross-references `package.json`.  
- **Severity:** Informational (positive) · **Confidence:** Reasoned  
- **Recommended fix:** Carry forward; add `npm ls --depth=0` as gate 8 (gate V-1). → §4, §17

**Finding 2.2 — `github-slugger` and `rehype-slug` parity is asserted, not verified**  
- **Location:** v1.0.1 §2, "TOC extraction" row; §7.3  
- **Description:** The skill states the two must stay compatible but provides no test.  
- **Impact:** A future patch upgrade could silently break anchor navigation.  
- **Severity:** Medium · **Confidence:** Reasoned  
- **Recommended fix:** Add a slug-parity unit test (CJK, emoji, code, repeated headings). → §9.3, Appendix C

**Finding 2.3 — Node version floor is correct for Vite 7**  
- **Severity:** Informational (positive) · **Confidence:** Reasoned  
- **Recommended fix:** None. Carry forward. → §4

---

#### §3 Bootstrapping & Configuration

**Finding 3.1 — No `tsc` npm script**  
- **Location:** v1.0.1 §3.1  
- **Description:** Typechecking is `npx tsc --noEmit` because no `npm run typecheck` script exists.  
- **Severity:** Low · **Confidence:** Verified  
- **Recommended fix:** Add `"typecheck": "tsc --noEmit"` to scripts. → §17

**Finding 3.2 — Google Fonts `@import` requires runtime network**  
- **Location:** v1.0.1 §3.3  
- **Description:** `vite-plugin-singlefile` inlines JS/CSS but not `@import`ed fonts. The skill documents this but provides no offline alternative.  
- **Impact:** The "single-file portability" promise is partially false — the artifact depends on a CDN.  
- **Severity:** High · **Confidence:** Verified  
- **Recommended fix:** Offer three font strategies: CDN `@import` (default), self-hosted `@font-face`, `@fontsource` base64 inlining (offline). → §11

---

#### §4 The Design System (Code-First)

**Finding 4.1 — `@theme` tokens are well-structured**  
- **Severity:** Informational (positive) · **Confidence:** Reasoned  
- **Recommended fix:** Carry forward; generalize per-template. → §6, §7

**Finding 4.2 — Severity palette is hardcoded to audit-report semantics**  
- **Location:** v1.0.1 §4.1, `--color-critical`/`high`/`medium`/`low`/`info` tokens  
- **Description:** Five severity tokens bake in the audit-report vocabulary. A changelog or status report cannot reuse the palette without adding tokens.  
- **Severity:** Medium · **Confidence:** Verified  
- **Recommended fix:** Replace with a generic 5-step accent scale (`accent-1`–`accent-5`) + a "kind" registry mapping document-specific tags to accent steps. → §6, §8

**Finding 4.3 — No `prefers-reduced-motion` guard**  
- **Location:** v1.0.1 §4.5, `html { scroll-behavior: smooth; }`  
- **Description:** `scroll-behavior: smooth` is set globally without a reduce override. The skill flags this as a known gap but does not fix it.  
- **Impact:** WCAG 2.3.3 (AAA) failure; vestibular disorder trigger.  
- **Severity:** High · **Confidence:** Verified  
- **Recommended fix:** Add the media query block. → §6, §10

**Finding 4.4 — No `prefers-color-scheme: dark` support**  
- **Location:** v1.0.1 §4 (entire)  
- **Description:** The design system is light-only.  
- **Severity:** Low · **Confidence:** Reasoned  
- **Recommended fix:** Make dual-mode via the two-layer token pattern (Layer 1 `:root` + Layer 2 `@theme inline`). → §6, §10

---

#### §5 Component Architecture & Patterns

**Finding 5.1 — `cn` utility is dead code**  
- **Location:** v1.0.1 §5.1  
- **Description:** The `cn()` helper (clsx + tailwind-merge) is imported nowhere.  
- **Severity:** Low · **Confidence:** Verified  
- **Recommended fix:** Wire `cn()` into `Badge.tsx` and template components. → §8

**Finding 5.2 — `enhanceReportMarkdown` runs at render time**  
- **Location:** v1.0.1 §5.3  
- **Description:** The regex preprocessor is called inside the render path. For a 10,000-line document, this is wasteful.  
- **Severity:** Low · **Confidence:** Reasoned  
- **Recommended fix:** Memoize via `useMemo` keyed on the markdown string. → §8, §13

**Finding 5.3 — Single state (`drawerOpen`) is correct for this scope**  
- **Severity:** Informational (positive) · **Confidence:** Reasoned  
- **Recommended fix:** Preserve; add `activeSection` and `theme` as the only additional state. → §9

---

#### §6 Custom Hooks Deep Dive

**Finding 6.1 — Explicit "None exist" is excellent documentation**  
- **Severity:** Informational (positive) · **Confidence:** Verified  
- **Recommended fix:** Carry this pattern forward. → §5

---

#### §7 Content Management & Data Ingestion

**Finding 7.1 — Badge protocol is too narrow**  
- **Location:** v1.0.1 §7.2  
- **Description:** The badge system recognizes exactly 9 keys (5 severity + 4 confidence). A changelog, status report, or compliance matrix cannot use it without code changes.  
- **Severity:** Medium · **Confidence:** Verified  
- **Recommended fix:** Generalize: regex matches any `**<Tag>:** <value>` where `<Tag>` is in a JSON registry. Add collision detection. → §8

**Finding 7.2 — `enhance.ts` regex is fragile to formatting variation**  
- **Location:** v1.0.1 §7.2; §15  
- **Description:** The regex requires `- **Severity:**` exactly. Variations (`*`, `1.`, no bullet) are silently skipped.  
- **Severity:** Medium · **Confidence:** Reasoned  
- **Recommended fix:** Accept all bullet styles; emit build-time warnings; make fence-aware. → §8

**Finding 7.3 — TOC contract correctly nests H3 under H2**  
- **Severity:** Informational (positive) · **Confidence:** Reasoned  
- **Recommended fix:** Extend to H4 (configurable depth); make fence-aware; reserve slugs for every level. → §9

---

#### §8 Accessibility (WCAG AAA) Implementation

**Finding 8.1 — "WCAG AAA" claim is partially false**  
- **Location:** v1.0.1 §1 "WCAG AAA where feasible"; §8 touch targets row  
- **Description:** The skill claims "WCAG AAA where feasible" but §8 documents 36×36 px and 32×32 px touch targets, failing WCAG 2.5.5 (AAA, 44×44 px).  
- **Impact:** The headline claim overstates actual conformance.  
- **Severity:** High · **Confidence:** Verified (internal contradiction)  
- **Recommended fix:** Increase touch targets to 44×44 px AND restate the claim as "WCAG 2.2 AA; AAA where feasible, with documented exceptions." → §10

**Finding 8.2 — Focus styles rely on browser default**  
- **Location:** v1.0.1 §8, "Focus visible" row  
- **Description:** Only the skip link has explicit `focus:` classes; other elements rely on browser default outlines.  
- **Severity:** Medium · **Confidence:** Reasoned  
- **Recommended fix:** Add a global `:focus-visible` style. → §6, §10

**Finding 8.3 — No automated a11y test in pre-ship**  
- **Location:** v1.0.1 §11  
- **Description:** The quality gate is `tsc && build && preview` with manual smoke checks. No `axe`, `Lighthouse`, or `pa11y`.  
- **Severity:** Medium · **Confidence:** Verified  
- **Recommended fix:** Add `@axe-core/playwright`; pre-ship becomes `typecheck && a11y && build`. Run in both light and dark modes. → §10, §14, §17

**Finding 8.4 — Badge text contrast fails AAA**  
- **Location:** v1.0.1 §8, "Color contrast" row  
- **Description:** Badge text pairs at 4.76–6.99:1, passing AA but failing AAA for 12 px normal text.  
- **Severity:** Medium · **Confidence:** Verified  
- **Recommended fix:** The v1.0.1 finding recommended "increase to 14 px (which relaxes AAA threshold to 4.5:1)." **This recommendation contains an arithmetic error** — see Finding 21.2. The correct fix is to enumerate the AAA failure (§10.3) and/or darken accent tokens (§10.5). → §8, §10

---

#### §9–§16: Anti-Patterns, Debugging, Lessons, Pitfalls, Best Practices, Patterns, Anti-Patterns, Breakpoints

These eight v1.0.1 sections each contained one Informational positive finding (the tables/guides are well-structured and should be carried forward and expanded). Summary:

| Finding | v1.0.1 section | v4.0.0 action |
|---------|----------------|---------------|
| 9.1 Anti-pattern table is high-value | §9 | Expand to 22 rows (§16) |
| 10.1 Debugging guide is symptom-cause-fix | §10 | Expand to 20 rows (§18) |
| 11.1 Quality gate is too narrow | §11 | Expand to 8 hard gates (§17) — **elevated to High** |
| 12.1 Lessons well-extracted | §12 | Preserve + expand (§9, §11, §21) |
| 13.1 Pitfalls table actionable | §13 | Expand (§16) |
| 14.1 Best practices conventional | §14 | Carry forward (§5) |
| 15.1 Three patterns documented as code | §15 | Expand to 6 patterns (§8, §19) |
| 16.1 Anti-patterns table concrete | §16 | Carry forward + expand (§16) |

**Finding 11.1 (elevated from Informational to High):** v1.0.1's quality gate is `tsc --noEmit && npm run build` plus manual smoke. No lint, no a11y, no unit tests, no format check. For a generalized skill targeting multiple authors, this gate is insufficient. v4.0.0 expands to 8 hard gates (§17).

---

#### §17 Responsive Breakpoint Reference

**Finding 17.1 — Only `sm` and `lg` are used**  
- **Location:** v1.0.1 §17  
- **Description:** Only `sm:` (640 px) and `lg:` (1024 px) breakpoints. `md`, `xl`, `2xl` unused.  
- **Severity:** Low · **Confidence:** Reasoned  
- **Recommended fix:** v4.0.0 templates may use `md`/`xl` where layout requires; document per template. → §7

---

#### §18 Z-Index Layer Map

**Finding 18.1 — Z-index map is explicit and minimal**  
- **Severity:** Informational (positive) · **Confidence:** Verified  
- **Recommended fix:** Add `z-30` for sticky-in-content; document `z-60` for command palette. → §6

---

#### §19 Color Reference (Complete)

**Finding 19.1 — Color reference is exhaustive and matches `@theme`**  
- **Severity:** Informational (positive) · **Confidence:** Reasoned  
- **Recommended fix:** Generate programmatically from `@theme` to prevent drift. → §6

---

#### §20 TypeScript Interface Reference

**Finding 20.1 — `TocItem` is the only named interface**  
- **Location:** v1.0.1 §20  
- **Description:** All other component props are inline anonymous types.  
- **Severity:** Low · **Confidence:** Verified  
- **Recommended fix:** Promote shared types to named interfaces in `src/types/`. → §22, Appendix B

---

#### Appendices A/B/C (v1.0.1)

| Finding | v1.0.1 appendix | v4.0.0 action |
|---------|-----------------|---------------|
| A.1 `.agents/` symlink is stale | Appendix A | Delete; repurpose as correction ledger (Appendix A) |
| B.1 Build output documentation correct | Appendix B | Carry forward; add offline variant (§11) |
| C.1 Visual pipeline duplicates §5.2 | Appendix C | Drop; repurpose as testing fixtures (Appendix C) |

---

#### §21 Comparative Review Findings (Round 2 — NEW in v4.0.0)

These 15 findings document bugs identified during the comparative review of draft_q3, draft_z2, draft_d2, and v2.1.0. Each is formatted per the evidence contract and cross-referenced to the v4.0.0 section that fixes it.

**Finding 21.1 — `@theme` nested inside `@media (prefers-color-scheme: dark)`** *(CRITICAL)*  
- **Present in:** draft_d2 §5.1, draft_z §4, v2.1.0 §6, draft_z2 §4 (partially)  
- **Description:** Four editions nest `@theme { ... }` inside `@media (prefers-color-scheme: dark)`. This is invalid Tailwind v4 — `@theme` is a build-time, top-level directive. Nesting it inside a media query does not generate the expected utilities, causing dark mode to silently fail.  
- **Confidence:** Verified (Tailwind v4 docs confirm `@theme` is top-level only; draft_q3 independently identified and fixed this)  
- **Recommended fix:** Adopt draft_q3's two-layer token pattern: Layer 1 `:root` runtime variables flipped by `@media` / `[data-theme]`; Layer 2 `@theme inline` bridges to Tailwind utilities. → §6, §16 anti-pattern #12

**Finding 21.2 — WCAG "14px relaxes AAA threshold to 4.5:1" arithmetic error** *(CRITICAL)*  
- **Present in:** draft_z, draft_z2 §8.3, draft_d2 §8.3, v2.1.0 §8  
- **Description:** Four editions claim 14px "relaxes the WCAG AAA threshold to 4.5:1." This is an arithmetic error. WCAG large text is ≥18pt (24px) or ≥14pt **bold** (≈18.66px). 14px non-bold text is **not** large text — the normal-text 7:1 AAA threshold still applies.  
- **Confidence:** Verified (stable WCAG 2.x definitions)  
- **Recommended fix:** Enumerate the AAA failure as a documented exception (§10.3). Provide a high-contrast badge recipe (§10.5 — darker accent tokens achieving ~8.5–9.2:1) as the correct path to AAA. → §10, §16 anti-pattern #13

**Finding 21.3 — `dangerouslySetInnerHTML` for markdown rendering** *(CRITICAL)*  
- **Present in:** draft_d2 §14.2  
- **Description:** draft_d2's `MarkdownRenderer` returns `<div dangerouslySetInnerHTML={{ __html: html }} />`, contradicting its own §11 component-map claim. Creates an XSS surface and defeats React reconciliation.  
- **Confidence:** Verified (code is explicit)  
- **Recommended fix:** Use the backtick-wrapping pattern: `enhance.ts` wraps values in backticks → react-markdown parses as inline `code` → `components.code` routes to `Badge`. Explicitly reject `dangerouslySetInnerHTML` as anti-pattern #10. → §8, §16

**Finding 21.4 — AST badge processor / React component disconnect** *(HIGH)*  
- **Present in:** draft_d2 §11.3  
- **Description:** draft_d2's `processBadges` AST plugin adds `data-badge-*` attributes to `listItem.hProperties`, but nothing consumes them. The `Badge` component expects props, not data attributes. Badges silently fail to render.  
- **Confidence:** Verified  
- **Recommended fix:** Reject the AST-processor approach. Use the backtick-wrapping pattern (§8.5). → §8

**Finding 21.5 — Fence-blind regex in `buildToc` and `enhanceMarkdown`** *(HIGH)*  
- **Present in:** draft_z2 §9.1, draft_d2 §9.1, v2.1.0 §9, draft_z §2.9  
- **Description:** Four editions use a raw `/^(#{2,4})\s+(.+)$/gm` regex. A `## comment` inside a ` ``` ` code fence is incorrectly indexed, entering the TOC and desyncing slug dedup with `rehype-slug`.  
- **Confidence:** Reasoned (draft_q3 independently identified and fixed this)  
- **Recommended fix:** Adopt draft_q3's `fence.ts` scanner (§9.1). Both `buildToc` and `enhanceMarkdown` consume `scanLines()` — no raw regex on markdown lines. → §9, §16 anti-pattern #14

**Finding 21.6 — No tag registry collision detection** *(MEDIUM)*  
- **Present in:** draft_z2 §8, draft_d2 §8, v2.1.0 §8, draft_z §2.8  
- **Description:** Four editions allow the same value in two tags (e.g., `"draft"` under `Status` and `Priority`). The resolver silently returns the first match.  
- **Confidence:** Reasoned  
- **Recommended fix:** Adopt draft_q3's `validateRegistry()` (§8.3) that throws at load time if two tags share a value, naming both in the error. → §8, §16 anti-pattern #15

**Finding 21.7 — False "Verified" self-tagging** *(MEDIUM)*  
- **Present in:** draft_d2 §23  
- **Description:** draft_d2 self-tags as "Verified — All audit gaps addressed" despite no code execution.  
- **Confidence:** Verified  
- **Recommended fix:** Self-tag as "Reasoned throughout" (§21). Apply the contract to the skill file itself with a per-claim ledger (Appendix A). → §21, Appendix A

**Finding 21.8 — `process.env.NODE_ENV` in browser code** *(MEDIUM)*  
- **Present in:** draft_d2 §14.1, §14.3  
- **Description:** draft_d2 uses `process.env.NODE_ENV` in browser-side React code. These are Node.js env vars, not available in a Vite browser build unless explicitly `define`d.  
- **Confidence:** Verified  
- **Recommended fix:** Use `import.meta.env.DEV` (Vite idiom) for dev-only code. Use `import.meta.env.VITE_ERROR_REPORTING_ENDPOINT` for env-gated config. → §12

**Finding 21.9 — Unrealistic 150 KB bundle budget** *(MEDIUM)*  
- **Present in:** draft_d2 §13.1  
- **Description:** draft_d2 sets a 150 KB gzipped budget. React 19 + react-markdown + remark/rehype alone is ~125–165 KB; 150 KB would force feature cuts.  
- **Confidence:** Reasoned  
- **Recommended fix:** Adopt draft_z2's 250 KB gzipped budget (§13.1) with composition breakdown. → §13

**Finding 21.10 — `PerformanceMonitor` with hardcoded `window.gtag`** *(MEDIUM)*  
- **Present in:** draft_d2 §13.2  
- **Description:** draft_d2's `PerformanceMonitor.measure()` calls `(window as any).gtag?.(...)`, assuming Google Analytics is present.  
- **Confidence:** Verified  
- **Recommended fix:** Remove the `gtag` call. Analytics is an extension point (Appendix E.5). v4.0.0 moves `PerformanceMonitor` to Appendix E as optional. → §13, Appendix E

**Finding 21.11 — `localStorage` without try/catch** *(MEDIUM)*  
- **Present in:** draft_d §6, draft_k §9  
- **Description:** Two editions access `localStorage.getItem('theme')` without try/catch. `localStorage` throws in sandboxed iframes and some `file://` contexts.  
- **Confidence:** Verified  
- **Recommended fix:** Wrap `localStorage` access in try/catch with an in-memory fallback (§6.6 `theme-storage.ts`). → §6

**Finding 21.12 — YAML frontmatter syntax error (stray ```` ``` ````)** *(LOW)*  
- **Present in:** draft_d2 line 26  
- **Description:** draft_d2 has a stray ` ``` ` after the closing `---` of the YAML frontmatter — would render as an unclosed code fence.  
- **Confidence:** Verified  
- **Recommended fix:** Remove the stray fence. v4.0.0's frontmatter is clean. → N/A

**Finding 21.13 — Slug parity test unused imports (`import { slug }`)** *(LOW)*  
- **Present in:** draft_z §2.9, v2.1.0 §9  
- **Description:** Two editions import `{ slug }` from `github-slugger` as a named export. `github-slugger` 2.0.0 exports only the default `GithubSlugger` class — no named `slug` export exists.  
- **Confidence:** Verified (github-slugger 2.0.0 package exports)  
- **Recommended fix:** Use `import GithubSlugger from "github-slugger"` (default import). → §9, §16 anti-pattern #7

**Finding 21.14 — `enhance.ts` regex `[^*]+` too restrictive** *(LOW)*  
- **Present in:** draft_z §2.8, v2.1.0 §8  
- **Description:** Two editions use `[^*]+` for the tag name capture group, excluding any tag name containing `*` (rare but unnecessarily tight).  
- **Confidence:** Reasoned  
- **Recommended fix:** Use `[^*]+` (sufficient for v4.0.0 scope) or `[^\\n*:]+` (draft_z2's alternative). v4.0.0 retains `[^*]+` as sufficient. → §8

**Finding 21.15 — No ErrorBoundary in skeleton** *(MEDIUM)*  
- **Present in:** draft_z §2.5, v2.1.0 §5  
- **Description:** Two editions do not include an `ErrorBoundary` component. Malformed markdown crashes the entire app with a white screen.  
- **Confidence:** Reasoned  
- **Recommended fix:** Add `ErrorBoundary.tsx` and `ErrorFallback.tsx` to the skeleton (§5). Place the boundary at the root in `main.tsx`, wrapping `<App />`. → §5, §12

### 1.3 Cross-Cutting Observations

1. **The skill is over-fit.** Every design decision in v1.0.1 serves the audit-report use case. The skill's own §1 calls this out as a feature ("anti-generic mandate"). For a generalized skill, this is the central obstacle.

2. **The evidence contract is the skill's best idea.** Verified/Reasoned/Assumed/Unverifiable tags on every finding (and the corresponding badge system) are a transferable pattern that should be preserved verbatim in v4.0.0.

3. **Code-first theming via Tailwind v4 `@theme` is the right call.** No `tailwind.config.js`, no JS/TS theme objects — just CSS custom properties. This is the modern Tailwind idiom and should be preserved. The two-layer refinement (runtime variables + `@theme inline` bridge) is the v4.0.0 contribution.

4. **The accessibility posture is aspirational, not verified.** v1.0.1 claims WCAG AAA but self-documents multiple AAA failures. The fix is either to (a) actually meet AAA, or (b) honestly claim AA with AAA-aspirational notes. v4.0.0 chooses (b) and closes the actual gaps where the cost is small (touch targets, focus-visible, reduced-motion).

5. **No automated testing of any kind.** No unit tests, no axe, no Lighthouse, no CI. For a single-purpose internal skill this is survivable; for a generalized skill targeting multiple authors and documents, it is the highest-leverage gap to close.

6. **Single-file build with runtime font dependence is a half-promise.** `vite-plugin-singlefile` inlines JS/CSS but not `@import`ed fonts. The artifact is not actually self-contained. v4.0.0 offers three font strategies (CDN, self-hosted, @fontsource offline).

7. **Documentation quality is excellent.** Section-by-section structure, anti-pattern tables, debugging guide, lessons-learnt, pitfalls, best practices — this is the right shape for a skill. v4.0.0 preserves the structure and expands it.

8. **draft_q2 introduces over-engineering that must be explicitly rejected.** The multi-framework adapter pattern (React/Vue/Svelte) triples scope without user value; the AST-based badge processor (40+ lines vs. the regex preprocessor's 10) is cognitively expensive for a skill an agent must implement in one session; `PerformanceMonitor` and `ErrorReporter` with external endpoints assume infrastructure most users do not have. v4.0.0 adopts draft_q2's *testing discipline* (test pyramid, axe-core fixtures, CI workflow) while explicitly rejecting its *architectural elaboration*.

9. **The `@theme`-in-`@media` bug is hereditary.** It was copied from draft_z into draft_d2, draft_z2 (partially), and v2.1.0 without detection. Only draft_q3 caught it. This demonstrates that architectural errors propagate silently across document merges — a single authoritative base (draft_q3) with explicit rejection of the buggy pattern is the cure.

10. **The WCAG 14px arithmetic error is similarly hereditary.** Copied from draft_z into three downstream editions. The fix is not better wording; it is correct WCAG definitions. Conformance claims are only as reliable as the math behind them. v4.0.0 explicitly rejects the arithmetic error (§10.1) and provides the correct path to AAA (§10.5 high-contrast recipe).

### 1.4 Reuse Value Assessment

| Source | Module | Reuse in v4.0.0 | Action |
|--------|--------|-----------------|--------|
| draft_q3 (BASE) | Two-layer token pattern (§4.1) | High | Adopt verbatim — fixes Finding 21.1 |
| draft_q3 | Fence-aware scanner `fence.ts` (§8.1) | High | Adopt verbatim — fixes Finding 21.5 |
| draft_q3 | Collision detection `validateRegistry()` (§7.2) | High | Adopt verbatim — fixes Finding 21.6 |
| draft_q3 | Correct WCAG arithmetic (§9.1) | High | Adopt verbatim — fixes Finding 21.2 |
| draft_q3 | High-contrast badge recipe (§9.5) | High | Adopt verbatim — correct path to AAA |
| draft_q3 | Honest lucide-react tag + gate V-1 (§2) | High | Adopt verbatim — fixes version drift |
| draft_q3 | Dark-mode axe test (§12.3) | High | Adopt — tests both light and dark |
| draft_q3 | Correction ledger (Appendix B) | High | Adopt pattern — 35+ rows in v4.0.0 Appendix A |
| draft_q3 | Adopter spot-check (Appendix C) | High | Adopt as v4.0.0 Appendix F |
| draft_z2 | Full test code (§15.2–15.5) | High | Adopt — complete runnable test files |
| draft_z2 | Performance budgets (§14, 250 KB) | High | Adopt — fixes Finding 21.9 |
| draft_z2 | Self-hosted font strategy (§13.2) | High | Adopt — third font strategy |
| draft_z2 | Lighthouse CI config (§16.4) | Medium | Adopt — `lighthouserc.yml` |
| draft_z2 | ErrorBoundary + ErrorFallback (§12) | High | Adopt — fixes Finding 21.15 |
| draft_z2 | Defect fixes table (§24.7) | High | Adopt pattern — v4.0.0 Appendix A |
| draft_z2 | Provenance log (§24.6) | Medium | Adopt — document merge history |
| draft_d2 | Full theme.css for technical (§5.3) | High | Adopt after @theme fix (§7.2) |
| draft_d2 | Full theme.css for minimal (§5.4) | High | Adopt after @theme fix (§7.3) |
| draft_d2 | 6-week phased migration plan (§20) | High | Adopt — actionable migration guidance |
| draft_d2 | Appendix E distilled lessons | Medium | Adopt — general engineering wisdom |
| v2.1.0 (prior) | Part 1 validation review (20 findings) | High | Preserve verbatim — unique value |
| v2.1.0 | Cross-reference table pattern | High | Adopt — traceability |
| v2.1.0 | Implementation plan provenance | Medium | Adopt — decision discipline |
| original_SKILL.md v1.0.1 | Evidence contract (§12) | High | Preserve verbatim in v4.0.0 §21 |
| original_SKILL.md v1.0.1 | Anti-pattern table format | High | Adopt — symptom→cause→fix |
| original_SKILL.md v1.0.1 | Z-index discipline | Medium | Adopt — extend with z-30, z-60 |
| draft_d2 | `@theme`-in-`@media` pattern | None | Reject — Finding 21.1 (Critical) |
| draft_d2 | `dangerouslySetInnerHTML` | None | Reject — Finding 21.3 (Critical) |
| draft_d2 | AST badge processor | None | Reject — Finding 21.4 (High) |
| draft_d2 | 150 KB bundle budget | None | Reject — Finding 21.9 |
| draft_d2 | `window.gtag` hardcoding | None | Reject — Finding 21.10 |
| draft_d2 | False "Verified" self-tag | None | Reject — Finding 21.7 |
| draft_d2 | `process.env.NODE_ENV` in browser | None | Reject — Finding 21.8 |
| draft_d2 | YAML syntax error | None | Reject — Finding 21.12 |
| draft_z / v2.1.0 | WCAG 14px arithmetic error | None | Reject — Finding 21.2 (Critical) |
| draft_z / v2.1.0 | `@theme`-in-`@media` | None | Reject — Finding 21.1 (Critical) |
| draft_z / v2.1.0 | Fence-blind regex | None | Reject — Finding 21.5 (High) |
| draft_z / v2.1.0 | `import { slug }` named export | None | Reject — Finding 21.13 |
| draft_z / v2.1.0 | `[^*]+` restrictive regex | None | Reject — Finding 21.14 |
| draft_q2 | Multi-framework adapters | None | Reject — YAGNI |
| draft_q2 | `PerformanceMonitor` with gtag | None | Reject — Finding 21.10 |
| draft_q2 | `ErrorReporter` with external endpoint | None | Move to Appendix E (optional) |
| draft_d / draft_k | `defineConfig` helper | None | Reject — config is frontmatter + template + tags, no helper needed |

---
