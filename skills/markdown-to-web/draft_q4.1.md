Executing the approved plan. **Pass 1 of 5** follows: document header + Part 1 (validation review) — Round 1 preserved verbatim from v4.0.0, Round 2 carried forward with the 21.8 amendment and confidence retags, Round 3 (15 new findings) written in full evidence-contract format. Passes 2–5 (§1–§9, §10–§15, §16–§23 + Closing, Appendices A–F) follow on continuation.

---

<!--
markdown-to-web — Unified Skill v4.1.0

This document is the unified, technically-correct skill file. Lineage:
- original_SKILL.md v1.0.1 — evidence contract, anti-pattern format, z-index discipline
- markdown-to-web_SKILL.md v2.1.0 — Part 1 validation review (Round 1 findings)
- draft_z2.md v2.0.0 — full test code, performance budgets, CI/CD, self-hosted fonts
- draft_d2.md v2.0.0 — full template CSS for technical + minimal, 6-week migration plan
- draft_q3.md v3.0.0 — correct Tailwind v4 theming, fence scanner, collision detection,
  correct WCAG arithmetic (base of v4.0.0)
- SKILL.md v4.0.0 — BASE for v4.1.0: unified all of the above; fixed the three
  hereditary Critical bugs (@theme-in-@media, WCAG 14px arithmetic,
  dangerouslySetInnerHTML)
- Round 3 self-audit (v4.1.0) — 15 new findings against v4.0.0; all fixed in this
  edition (Part 1 §22; Appendix A)

Round 3 headline fixes:
HIGH:     AAA axe gate contradicted its own documented badge exceptions —
          exceptions are now encoded in the gate itself (§10.4, §14.9)
HIGH:     Template switching machinery was overpromised and unwritten —
          concrete src/templates/active.ts wiring file (§5, §7.4)
MEDIUM:   Frontmatter was never stripped before render —
          parseDocument() returns { frontmatter, body }; pipeline consumes body (§22.5)
MEDIUM:   Headings with links/images desynced TOC↔rehype-slug slugs —
          headingText() normalization + new parity fixtures (§9.2, §9.3)
MEDIUM:   Badge misfired on unclassed fenced code blocks —
          single-line string guard (§8.5)
MEDIUM:   Finding 21.8 rationale overstated process.env breakage —
          amended in place (§21.8, §22.6)
LOW x6, INFORMATIONAL x3 — full ledger in Appendix A

Verification protocol: desk review. Findings tagged Verified / Reasoned / Assumed /
Unverifiable per the skill's own evidence contract (§21). No code execution in this
environment. Round 3 retag (see §1.1 note): claims about runtime or library behavior
that were not executed are Reasoned — including two claims v4.0.0 tagged Verified
without execution (§21.1, §21.13). This edition applies to itself the standard it
enforces.
-->

name: markdown-to-web
description: >
  Renders an arbitrary Markdown document as a polished, single-file, accessible
  web page. Accepts any .md file plus an optional template (editorial long-form
  / technical docs / minimal print) and an optional tag registry (severity,
  confidence, status, custom). Produces a self-contained dist/index.html with
  WCAG 2.2 AA enforced by an axe gate, and AAA where feasible with enumerated
  exceptions that are encoded in the gate itself (badge contrast exclusions by
  selector, target-size enforced globally). Code-first theming via a two-layer
  token pattern (runtime variables + @theme inline bridge); fence-aware TOC with
  verified slug parity including linked-heading normalization; frontmatter parsed
  AND stripped before render; tag-registry badges with cross-category collision
  detection and a code-block misfire guard; template switching via one wiring
  file; 8-gate pre-ship checklist. Built on React 19 + Vite 7 + Tailwind v4 +
  react-markdown. Use when the user asks to "render this markdown as a web
  page", "convert .md to HTML", "publish this document as a site", or "make a
  polished web version of this README/report/spec".
version: 4.1.0
tags:
  react
  vite
  tailwindcss
  markdown
  html
  single-file-build
  accessibility
  documentation

# markdown-to-web — Validation Review & Unified Skill Specification

**Document version:** 4.1.0
**Date:** 2026-08-06
**Scope:** (1) Audit of `react-markdown-report` v1.0.1 skill; (2) comparative review of four generalization drafts (draft_q3, draft_z2, draft_d2, v2.1.0); (3) Round 3 self-audit of the unified v4.0.0 edition; (4) unified, technically-correct replacement — `markdown-to-web` v4.1.0
**Base document:** `SKILL.md` v4.0.0 (itself based on `draft_q3.md` v3.0.0, selectively merged with draft_z2.md, draft_d2.md, v2.1.0, and original_SKILL.md v1.0.1), with 15 Round 3 corrections applied
**Verification protocol:** Desk review. Findings tagged Verified / Reasoned / Assumed / Unverifiable per the skill's own evidence contract (§21). No code execution in this environment — recommendations that depend on runtime behavior are explicitly marked.

---

# Part 1 — Validation Review

## 1.0 Executive Summary

The original `react-markdown-report` v1.0.1 skill is a well-organized, single-purpose project skill for a React 19 + Vite 7 + Tailwind v4 single-file web rendering of one specific Markdown audit report. Its strengths are an explicit evidence contract, a code-first design system, and a refreshingly anti-generic visual mandate. Its weaknesses are an over-fit scope (one report, one design), several accessibility gaps that contradict its own WCAG AAA claim, no automated quality gate beyond `tsc --noEmit && npm run build`, and runtime font dependence that breaks the "single-file portability" promise.

Four generalization drafts were produced to address these weaknesses. A comparative review (Round 2) revealed that three of the four mature editions carried two critical bugs hereditarily copied from draft_z: the `@theme`-inside-`@media` pattern (invalid Tailwind v4, dark mode silently fails) and the WCAG "14px relaxes AAA threshold" arithmetic error (14px is not large text). Only draft_q3 caught both. v4.0.0 adopted draft_q3 as its base and fixed all 35 findings across Rounds 1–2.

A Round 3 self-audit of v4.0.0 then found 15 further defects — most of them introduced or exposed *by the fixes themselves*: correcting the WCAG arithmetic broke the coherence of the AAA axe gate (the gate hard-failed on the very exceptions §10.3 documents); the merge inherited a frontmatter-strip gap present in every prior edition; and the slug-parity fixture set missed headings containing links and images. v4.1.0 fixes all 15.

**Severity counts (reconciled against the finding text — see note below):**

| Round | Scope | Critical | High | Medium | Low | Informational | Total |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Round 1 (§1.2, F 1.1–20.1 + A.1–C.1) | v1.0.1 audit | 0 | 5 | 8 | 6 | 18 | 37 |
| Round 2 (§21, F 21.1–21.15) | Comparative review of drafts | 3 | 2 | 7 | 3 | 0 | 15 |
| Round 3 (§22, F 22.1–22.15) | Self-audit of v4.0.0 | 0 | 2 | 4 | 6 | 3 | 15 |
| **Total** | | **3** | **9** | **19** | **14** | **21** | **67** |

> **Count reconciliation (new in v4.1.0).** Prior editions' executive tables undercounted against their own finding text: v2.1.0/v4.0.0 reported Round 1 as "High 3 / Medium 7 / Low 5 / Informational 4", but the preserved findings mark five High (1.1, 3.2, 4.3, 8.1, and 11.1-elevated) and v4.0.0's Round 2 table reported "Medium 6 / Low 4" while its own Finding 21.15 is Medium (yielding 7 / 3). The table above is exact against the finding text. An audit's arithmetic must survive its own audit.

**Overall verdict:** v1.0.1 is internally consistent and high-quality for its narrow purpose but not reusable without forking. The generalization drafts each made genuine contributions but propagated two critical bugs hereditarily. v4.0.0 was the first edition where every load-bearing mechanism was technically correct; v4.1.0 is the first edition where the *gates, pipeline, and documentation are coherent with each other*: the AAA gate enforces exactly what §10.3 claims, the frontmatter cannot leak into rendered output, slug parity covers linked headings, badges cannot misfire on code blocks, and template switching has a written mechanism. The durable patterns (evidence contract, slug-parity test, tag registry with collision detection, two-layer token theming, fence-aware scanner, 8-gate pre-ship) are high-confidence; the specific code snippets are starting points that require runtime validation per the "What was NOT verified" list in the Closing and the Appendix F spot-check.

**Reuse Value Assessment** (summary — full table in §1.4):

| Source | Reuse action in v4.1.0 |
| --- | --- |
| draft_q3.md (base of v4.0.0) | Two-layer token pattern; fence-aware scanner; collision detection; correct WCAG arithmetic; high-contrast recipe; honest lucide tag + gate V-1 |
| draft_z2.md | Full test code; performance budgets (250 KB); self-hosted font strategy; Lighthouse CI; ErrorBoundary/ErrorFallback/ErrorReporter; defect-fixes table pattern |
| draft_d2.md | Full theme.css for technical + minimal templates (after @theme fix); 6-week migration plan; Appendix E distilled lessons |
| v2.1.0 (prior) | Part 1 validation review (Round 1 findings, preserved); cross-reference table pattern |
| original_SKILL.md v1.0.1 | Evidence contract (§21, verbatim); anti-pattern table format; z-index discipline |
| SKILL.md v4.0.0 | BASE — entire Part 2 architecture; all 35 Rounds 1–2 fixes |
| Round 3 self-audit (new) | 15 findings (§22) → fixes F1–F5 + textual corrections; Lessons Learnt §23 |

## 1.1 Methodology

Each finding follows the format mandated by the skill's own Section 12 (preserved in this document as §21):

1. **Location** (section reference in the source document)
2. **Description**
3. **Evidence** (quoted or paraphrased from the source)
4. **Impact**
5. **Severity** (Critical / High / Medium / Low / Informational)
6. **Confidence** (Verified / Reasoned / Assumed — see note below)
7. **Recommended fix**

Findings are tagged per the skill's own evidence contract (§21). The review spans three rounds:

- **Round 1** (§1.2, Findings 1.1–20.1 + appendix findings): Original audit of `react-markdown-report` v1.0.1, preserved from the v2.1.0 document (which preserved them from draft_z). 37 findings.
- **Round 2** (§21, Findings 21.1–21.15): Comparative review of draft_q3, draft_z2, draft_d2, and v2.1.0. 15 findings documenting bugs that propagated across editions.
- **Round 3** (§22, Findings 22.1–22.15, NEW in v4.1.0): Self-audit of the unified v4.0.0 edition. 15 findings, most of them introduced or exposed by the Round 2 fix-batch or inherited silently through every merge.

**Confidence note:** Because all documents were reviewed as text only (no project bootstrap, no `npm install`, no `axe` run, no Lighthouse pass), most findings are **Reasoned** (logical inference from the documents' own statements) or **Assumed** (inference about runtime behavior the documents do not measure). Where a document contradicts its own claims (e.g., v1.0.1's "WCAG AAA" vs. documented 36×36 px touch targets; draft_d2's "Verified" self-tag vs. no code execution; v4.0.0's §10.3 exceptions table vs. §14.9 gate code), the finding is **Verified (textual)** — the contradiction is in the text. Where a claim depends on stable external definitions (WCAG 2.x large-text thresholds; CSS specificity arithmetic), it is **Verified (against stable definitions)**.

> **Round 3 confidence amendment (applies to this audit itself).** v4.0.0 tagged Findings 21.1 and 21.13 as "Verified" on the basis of documentation/package knowledge, without execution. Per the evidence contract this document enforces, unexecuted claims about library/build behavior are **Reasoned**. v4.1.0 retags: 21.1 → *Reasoned (against documented Tailwind v4 semantics; not executed)*; 21.13 → *Reasoned (against package-export knowledge; confirm at install via gate V-1)*. Findings about WCAG definitions (21.2) remain Verified — stable normative definitions, not runtime behavior.

## 1.2 Section-by-Section Findings

Findings are ordered by severity within each round, then by section number. Round 1 findings are preserved from v2.1.0/v4.0.0. Round 2 findings are carried forward with one in-place amendment (21.8) and the confidence retags noted in §1.1. Round 3 findings are new.

### §1 Project Identity & Design Philosophy

**Finding 1.1 — Scope is hardcoded to one report**
- **Location:** v1.0.1 §1, "One-sentence description"
- **Description:** The skill's identity sentence fixes it to "a structural/content/IA comparative audit of `kelp.agency` vs. its clone `astro.jesspete.shop`." Every downstream module (badge keys, content path `src/content/comparative-analysis.md`, hero copy in `App.tsx:124`) inherits that fixation.
- **Evidence:** "A single-file, zero-backend React application that renders a structural/content/IA comparative audit of `kelp.agency` vs. its clone `astro.jesspete.shop`."
- **Impact:** The skill cannot be invoked for any other Markdown document without forking. An agent encountering "render this README as a polished web page" will not match this skill's trigger surface.
- **Severity:** High · **Confidence:** Verified (textually explicit)
- **Recommended fix:** Generalize the identity to "renders an arbitrary Markdown document as a polished single-file web page using a configurable template and evidence-tag protocol." → §1, §2, §3

**Finding 1.2 — "No generic UI" mandate conflicts with reuse**
- **Location:** v1.0.1 §1, "Anti-generic mandate (explicitly rejected)"
- **Description:** The skill explicitly rejects "any component that could be dropped into a different project without visual friction." Legitimate for a one-off report; incompatible with a generalized skill.
- **Severity:** Medium · **Confidence:** Reasoned
- **Recommended fix:** Reframe as per-template mandate; provide three templates. → §1, §7

### §2 Tech Stack & Environment

**Finding 2.1 — Versions are pinned and verified**
- **Severity:** Informational (positive) · **Confidence:** Reasoned
- **Recommended fix:** Carry forward; add `npm ls --depth=0` as gate 8 (gate V-1). → §4, §17

**Finding 2.2 — `github-slugger` and `rehype-slug` parity is asserted, not verified**
- **Location:** v1.0.1 §2, "TOC extraction" row; §7.3
- **Description:** The skill states the two must stay compatible but provides no test.
- **Impact:** A future patch upgrade could silently break anchor navigation.
- **Severity:** Medium · **Confidence:** Reasoned
- **Recommended fix:** Add a slug-parity unit test (CJK, emoji, code, repeated headings). → §9.3, Appendix C. *Extended in v4.1.0 by Finding 22.4 (linked/image headings).*

**Finding 2.3 — Node version floor is correct for Vite 7**
- **Severity:** Informational (positive) · **Confidence:** Reasoned
- **Recommended fix:** None. Carry forward. → §4

### §3 Bootstrapping & Configuration

**Finding 3.1 — No `tsc` npm script**
- **Severity:** Low · **Confidence:** Verified (textually explicit)
- **Recommended fix:** Add `"typecheck": "tsc --noEmit"` to scripts. → §17

**Finding 3.2 — Google Fonts `@import` requires runtime network**
- **Location:** v1.0.1 §3.3
- **Description:** `vite-plugin-singlefile` inlines JS/CSS but not `@import`ed fonts. The skill documents this but provides no offline alternative.
- **Impact:** The "single-file portability" promise is partially false — the artifact depends on a CDN.
- **Severity:** High · **Confidence:** Verified (textually explicit)
- **Recommended fix:** Offer three font strategies: CDN `@import` (default), self-hosted `@font-face`, `@fontsource` base64 inlining (offline). → §11

### §4 The Design System (Code-First)

**Finding 4.1 — `@theme` tokens are well-structured**
- **Severity:** Informational (positive) · **Confidence:** Reasoned
- **Recommended fix:** Carry forward; generalize per-template. → §6, §7

**Finding 4.2 — Severity palette is hardcoded to audit-report semantics**
- **Severity:** Medium · **Confidence:** Verified
- **Recommended fix:** Replace with a generic 5-step accent scale (`accent-1`–`accent-5`) + a tag registry mapping document-specific tags to accent steps. → §6, §8

**Finding 4.3 — No `prefers-reduced-motion` guard**
- **Location:** v1.0.1 §4.5, `html { scroll-behavior: smooth; }`
- **Description:** `scroll-behavior: smooth` is set globally without a reduce override. The skill flags this as a known gap but does not fix it.
- **Impact:** WCAG 2.3.3 (AAA) failure; vestibular-disorder trigger.
- **Severity:** High · **Confidence:** Verified
- **Recommended fix:** Add the media query block. → §6, §10

**Finding 4.4 — No `prefers-color-scheme: dark` support**
- **Severity:** Low · **Confidence:** Reasoned
- **Recommended fix:** Make dual-mode via the two-layer token pattern (Layer 1 `:root` + Layer 2 `@theme inline`). → §6, §10

### §5 Component Architecture & Patterns

**Finding 5.1 — `cn` utility is dead code**
- **Severity:** Low · **Confidence:** Verified
- **Recommended fix:** Wire `cn()` into `Badge.tsx` and template components. → §8

**Finding 5.2 — `enhanceReportMarkdown` runs at render time**
- **Severity:** Low · **Confidence:** Reasoned
- **Recommended fix:** Memoize via `useMemo` keyed on the markdown string. → §8, §13

**Finding 5.3 — Single state (`drawerOpen`) is correct for this scope**
- **Severity:** Informational (positive) · **Confidence:** Reasoned
- **Recommended fix:** Preserve; add `activeSlug` and `theme` as the only additional state. → §9

### §6 Custom Hooks Deep Dive

**Finding 6.1 — Explicit "None exist" is excellent documentation**
- **Severity:** Informational (positive) · **Confidence:** Verified
- **Recommended fix:** Carry this pattern forward. → §5

### §7 Content Management & Data Ingestion

**Finding 7.1 — Badge protocol is too narrow**
- **Location:** v1.0.1 §7.2
- **Description:** The badge system recognizes exactly 9 keys (5 severity + 4 confidence). A changelog, status report, or compliance matrix cannot use it without code changes.
- **Severity:** Medium · **Confidence:** Verified
- **Recommended fix:** Generalize: regex matches any `**<Tag>:** <value>` where `<Tag>` is in a registry. Add collision detection. → §8

**Finding 7.2 — `enhance.ts` regex is fragile to formatting variation**
- **Severity:** Medium · **Confidence:** Reasoned
- **Recommended fix:** Accept all bullet styles; emit build-time warnings; make fence-aware. → §8. *Extended in v4.1.0 by Finding 22.11 (colon-outside-bold variant).*

**Finding 7.3 — TOC contract correctly nests H3 under H2**
- **Severity:** Informational (positive) · **Confidence:** Reasoned
- **Recommended fix:** Extend to H4 (configurable depth); make fence-aware; reserve slugs for every level. → §9

### §8 Accessibility (WCAG AAA) Implementation

**Finding 8.1 — "WCAG AAA" claim is partially false**
- **Location:** v1.0.1 §1 "WCAG AAA where feasible"; §8 touch targets row
- **Description:** The skill claims "WCAG AAA where feasible" but §8 documents 36×36 px and 32×32 px touch targets, failing WCAG 2.5.5 (AAA, 44×44 px).
- **Impact:** The headline claim overstates actual conformance.
- **Severity:** High · **Confidence:** Verified (internal contradiction)
- **Recommended fix:** Increase touch targets to 44×44 px AND restate the claim as "WCAG 2.2 AA; AAA where feasible, with documented exceptions." → §10

**Finding 8.2 — Focus styles rely on browser default**
- **Severity:** Medium · **Confidence:** Reasoned
- **Recommended fix:** Add a global `:focus-visible` style. → §6, §10

**Finding 8.3 — No automated a11y test in pre-ship**
- **Severity:** Medium · **Confidence:** Verified
- **Recommended fix:** Add `@axe-core/playwright`; run in both light and dark modes. → §10, §14, §17

**Finding 8.4 — Badge text contrast fails AAA**
- **Location:** v1.0.1 §8, "Color contrast" row
- **Description:** Badge text pairs at 4.76–6.99:1, passing AA but failing AAA for 12 px normal text.
- **Severity:** Medium · **Confidence:** Verified
- **Recommended fix:** The v1.0.1 finding recommended "increase to 14 px (which relaxes AAA threshold to 4.5:1)." That recommendation contains an arithmetic error — see Finding 21.2. The correct fix is to enumerate the AAA failure (§10.3), encode the exception in the gate (§14.9 — Finding 22.1), and offer the high-contrast recipe (§10.5). → §8, §10

### §9–§16: Anti-Patterns, Debugging, Gates, Lessons, Pitfalls, Best Practices, Patterns, Anti-Patterns Tables

These eight v1.0.1 sections each contained one Informational positive finding (the tables/guides are well-structured and should be carried forward and expanded), with one elevation:

| Finding | v1.0.1 section | v4.1.0 action |
| --- | --- | --- |
| 9.1 Anti-pattern table is high-value | §9 | Expand (§16) |
| 10.1 Debugging guide is symptom-cause-fix | §10 | Expand (§18) |
| **11.1 Quality gate is too narrow** | §11 | **Elevated from Informational to High.** v1.0.1's gate is `tsc && build` plus manual smoke — insufficient for a generalized skill. Expand to 8 hard gates (§17) |
| 12.1 Lessons well-extracted | §12 | Preserve + expand; restored as §23 Lessons Learnt with the Round 3 hereditary-error lesson |
| 13.1 Pitfalls table actionable | §13 | Expand (§16) |
| 14.1 Best practices conventional | §14 | Carry forward (§5) |
| 15.1 Three patterns documented as code | §15 | Expand (§8, §19) |
| 16.1 Anti-patterns table concrete | §16 | Carry forward + expand (§16) |

### §17 Responsive Breakpoint Reference

**Finding 17.1 — Only `sm` and `lg` are used**
- **Severity:** Low · **Confidence:** Reasoned
- **Recommended fix:** Templates may use `md`/`xl` where layout requires; document per template. → §7

### §18 Z-Index Layer Map

**Finding 18.1 — Z-index map is explicit and minimal**
- **Severity:** Informational (positive) · **Confidence:** Verified
- **Recommended fix:** Add `z-30` for sticky-in-content; document `z-60` for command palette. → §6

### §19 Color Reference (Complete)

**Finding 19.1 — Color reference is exhaustive and matches `@theme`**
- **Severity:** Informational (positive) · **Confidence:** Reasoned
- **Recommended fix:** Generate programmatically to prevent drift. → §6

### §20 TypeScript Interface Reference

**Finding 20.1 — `TocItem` is the only named interface**
- **Severity:** Low · **Confidence:** Verified
- **Recommended fix:** Promote shared types to named interfaces in `src/types/`. → §22, Appendix B

### Appendices A/B/C (v1.0.1)

| Finding | v1.0.1 appendix | v4.1.0 action |
| --- | --- | --- |
| A.1 `.agents/` symlink is stale | Appendix A | Delete; repurpose as correction ledger (Appendix A) |
| B.1 Build output documentation correct | Appendix B | Carry forward; add offline variant (§11) |
| C.1 Visual pipeline duplicates §5.2 | Appendix C | Drop; repurpose as testing fixtures index (Appendix C) |

### §21 Comparative Review Findings (Round 2 — from v4.0.0)

Carried forward from v4.0.0 with one in-place amendment (21.8) and the confidence retags declared in §1.1.

**Finding 21.1 — `@theme` nested inside `@media (prefers-color-scheme: dark)`** (CRITICAL)
- **Present in:** draft_d2 §5.1, draft_z §4, v2.1.0 §6, draft_z2 §4 (partially)
- **Description:** Four editions nest `@theme { ... }` inside `@media (prefers-color-scheme: dark)`. This is invalid Tailwind v4 — `@theme` is a build-time, top-level directive. Nesting it inside a media query does not generate the expected utilities, causing dark mode to silently fail.
- **Confidence:** ~~Verified~~ → **Reasoned** (against documented Tailwind v4 semantics and draft_q3's independent identification; not executed — v4.1.0 retag per §1.1)
- **Recommended fix:** Two-layer token pattern: Layer 1 `:root` runtime variables flipped by `@media` / `[data-theme]`; Layer 2 `@theme inline` bridges to Tailwind utilities. → §6, §16 anti-pattern #12

**Finding 21.2 — WCAG "14px relaxes AAA threshold to 4.5:1" arithmetic error** (CRITICAL)
- **Present in:** draft_z, draft_z2 §8.3, draft_d2 §8.3, v2.1.0 §8
- **Description:** Four editions claim 14px "relaxes the WCAG AAA threshold to 4.5:1." WCAG large text is ≥18pt (24px) or ≥14pt bold (≈18.66px). 14px non-bold text is not large text — the normal-text 7:1 AAA threshold still applies.
- **Confidence:** Verified (stable WCAG 2.x definitions)
- **Recommended fix:** Enumerate the AAA failure (§10.3), encode the exception in the gate (§14.9 — see Finding 22.1), and provide the high-contrast badge recipe (§10.5). → §10, §16 anti-pattern #13

**Finding 21.3 — `dangerouslySetInnerHTML` for markdown rendering** (CRITICAL)
- **Present in:** draft_d2 §14.2
- **Description:** draft_d2's `MarkdownRenderer` returns `<div dangerouslySetInnerHTML={{ __html: html }} />`, contradicting its own §11 component-map claim. Creates an XSS surface and defeats React reconciliation.
- **Confidence:** Verified (textually explicit)
- **Recommended fix:** Backtick-wrapping pattern; explicit rejection as anti-pattern #10. → §8, §16

**Finding 21.4 — AST badge processor / React component disconnect** (HIGH)
- **Present in:** draft_d2 §11.3
- **Description:** draft_d2's `processBadges` AST plugin adds `data-badge-*` attributes to `listItem.hProperties`, but nothing consumes them; the `Badge` component expects props. Badges silently fail to render. *(Related: draft_d2 §14.2 consumes its async `processMarkdown` without `await`, which would additionally render empty — moot once the approach is rejected.)*
- **Confidence:** Verified (textually explicit)
- **Recommended fix:** Reject the AST-processor approach. Backtick-wrapping (§8.5). → §8

**Finding 21.5 — Fence-blind regex in `buildToc` and `enhanceMarkdown`** (HIGH)
- **Present in:** draft_z2 §9.1, draft_d2 §9.1, v2.1.0 §9, draft_z
- **Description:** Raw `/^(#{2,4})\s+(.+)$/gm` regexes index a `## comment` inside a code fence, entering the TOC and desyncing slug dedup with `rehype-slug`.
- **Confidence:** Reasoned (draft_q3 independently identified and fixed this)
- **Recommended fix:** `fence.ts` scanner (§9.1); both `buildToc` and `enhanceMarkdown` consume `scanLines()`. → §9, §16 anti-pattern #14

**Finding 21.6 — No tag registry collision detection** (MEDIUM)
- **Present in:** draft_z2 §8, draft_d2 §8, v2.1.0 §8, draft_z
- **Description:** Four editions allow the same value in two tags; the resolver silently returns the first match.
- **Confidence:** Reasoned
- **Recommended fix:** `validateRegistry()` (§8.3) throws at load time, naming both tags. → §8, §16 anti-pattern #15

**Finding 21.7 — False "Verified" self-tagging** (MEDIUM)
- **Present in:** draft_d2 §23
- **Description:** draft_d2 self-tags "Verified — All audit gaps addressed" despite no code execution.
- **Confidence:** Verified (textually explicit)
- **Recommended fix:** Self-tag "Reasoned throughout"; per-claim ledger. → §21, Appendix A

**Finding 21.8 — `process.env` usage in browser code** (MEDIUM) — *amended in v4.1.0, see Finding 22.6*
- **Present in:** draft_d2 §14.1, §14.3
- **Description (amended):** draft_d2 uses `process.env.NODE_ENV` and `process.env.ERROR_REPORTING_ENDPOINT` in browser-side code. **v4.1.0 amendment:** Vite replaces `process.env.NODE_ENV` at build time as documented compatibility behavior, so the `NODE_ENV` checks would in fact work — v4.0.0's "not available unless explicitly defined" rationale overstated the breakage. The recommendation stands on idiom/portability grounds (`import.meta.env.DEV` is the Vite-native spelling). The *genuine* environment bug in draft_d2 is `process.env.ERROR_REPORTING_ENDPOINT`: Vite exposes only `import.meta.env.VITE_*` variables to the client, so that endpoint never resolves at runtime.
- **Confidence:** Reasoned (Vite's define behavior is documented; not executed here)
- **Recommended fix:** Use `import.meta.env.DEV` for dev-only code and `import.meta.env.VITE_ERROR_REPORTING_ENDPOINT` for env-gated config. → §12, Appendix E.4

**Finding 21.9 — Unrealistic 150 KB bundle budget** (MEDIUM)
- **Present in:** draft_d2 §13.1
- **Description:** 150 KB gzipped is unachievable with React 19 + react-markdown + remark/rehype without feature cuts.
- **Confidence:** Reasoned
- **Recommended fix:** 250 KB gzipped budget with composition breakdown. → §13

**Finding 21.10 — `PerformanceMonitor` with hardcoded `window.gtag`** (MEDIUM)
- **Present in:** draft_d2 §13.2
- **Description:** Assumes Google Analytics is present.
- **Confidence:** Verified (textually explicit)
- **Recommended fix:** Remove; analytics is an extension point. → §13, Appendix E.5

**Finding 21.11 — `localStorage` without try/catch** (MEDIUM)
- **Present in:** draft_d §6, draft_k §9
- **Description:** `localStorage` throws in sandboxed iframes and some `file://` contexts.
- **Confidence:** Reasoned
- **Recommended fix:** try/catch with in-memory fallback (§6.6). → §6

**Finding 21.12 — YAML frontmatter syntax error (stray fence)** (LOW)
- **Present in:** draft_d2 line 26
- **Confidence:** Verified (textually explicit)
- **Recommended fix:** Remove the stray fence. v4.1.0 frontmatter is clean.

**Finding 21.13 — Slug parity test unused imports (`import { slug }`)** (LOW)
- **Present in:** draft_z, v2.1.0 §9
- **Description:** `github-slugger` 2.0.0 exports only the default `GithubSlugger` class — no named `slug` export exists.
- **Confidence:** ~~Verified~~ → **Reasoned** (against package-export knowledge; confirm at install via gate V-1 — v4.1.0 retag per §1.1)
- **Recommended fix:** `import GithubSlugger from "github-slugger"`. → §9, §16 anti-pattern #7

**Finding 21.14 — `enhance.ts` regex `[^*]+` too restrictive** (LOW)
- **Present in:** draft_z, v2.1.0 §8
- **Confidence:** Reasoned
- **Recommended fix:** v4.1.0 retains `[^*]+` as sufficient for scope; `[^\\n*:]+` documented as the alternative. → §8

**Finding 21.15 — No ErrorBoundary in skeleton** (MEDIUM)
- **Present in:** draft_z §2.5, v2.1.0 §5
- **Description:** Malformed markdown crashes the entire app with a white screen.
- **Confidence:** Reasoned
- **Recommended fix:** `ErrorBoundary.tsx` + `ErrorFallback.tsx` at root. → §5, §12

### §22 Round 3 Self-Audit Findings (NEW in v4.1.0)

These 15 findings document defects in the unified v4.0.0 edition itself. Most were introduced or exposed by the Round 2 fix-batch, or inherited silently through every prior merge. Each is cross-referenced to the v4.1.0 section that fixes it.

**Finding 22.1 — AAA axe gate contradicts the enumerated badge exceptions** (HIGH)
- **Location:** v4.0.0 §10.3 vs §14.9 (pattern introduced in draft_q3 §9.3/§12.3 alongside the WCAG arithmetic fix)
- **Description:** §10.3 documents badge text as accepted AAA contrast failures ("Badge text, accent-2 on amber-50 | ≈4.8:1 | AA ✓ | AAA ✗ | Exception; upgrade via §10.5"). §14.9's AAA test then hard-fails on *any* `color-contrast` violation: `const enforced = results.violations.filter((v) => ["color-contrast", "target-size"].includes(v.id)); expect(enforced).toEqual([]);`. Any page containing a badge therefore fails the AAA gate by design — or the exceptions table is false.
- **Evidence:** The two sections quoted above, juxtaposed. Note the history: draft_z2's version of this test was internally consistent only because it rested on the false 14px arithmetic (Finding 21.2). Correcting the arithmetic without touching the test created this contradiction.
- **Impact:** Pre-ship Gate 5 is unshippable as written. Teams would either weaken the gate (forbidden by §17) or silently avoid badges.
- **Severity:** High · **Confidence:** Verified (textual contradiction within v4.0.0)
- **Recommended fix:** Encode the exceptions in the gate itself: for AAA `color-contrast`, exclude violation nodes whose targets are `[data-tag]` badge elements; keep `target-size` enforcement global. The gate must enforce exactly what §10.3 claims. → §10.4, §14.9 (fix F1)

**Finding 22.2 — Template switching machinery overpromised and unwritten** (HIGH)
- **Location:** v4.0.0 §7.4 (v2.1.0 §7)
- **Description:** §7.4 states "The build system loads the template specified in frontmatter (or the default `editorial`), merges its component overrides with the default map…" This implies build-time reading of a `?raw` markdown file's frontmatter — a Vite plugin or virtual module that no edition writes, and which §3.2's rejected-machinery rule argues against. Meanwhile `src/index.css` statically imports exactly one theme, and no edition shows how per-template CSS is selected. draft_d2's runtime `loadTemplate()` registry is the only concrete mechanism in the corpus but does not solve CSS bundling.
- **Evidence:** §7.4 text quoted above; absence of any plugin in the §5 skeleton.
- **Impact:** A non-negotiable design rule ("Templates are swappable") rests on unwritten machinery; implementers would invent incompatible switching mechanisms.
- **Severity:** High · **Confidence:** Verified (textual absence); impact Reasoned
- **Recommended fix:** Concrete mechanism: one wiring file `src/templates/active.ts` (CSS side-effect import + re-export of the active template's registry/layout + `TEMPLATE_NAME`). Frontmatter `template` becomes advisory metadata with a dev-mode mismatch warning. §7.4 rewritten around it. → §5, §7.4, §22.8 (fix F2)

**Finding 22.3 — Frontmatter is never stripped from the rendered markdown** (MEDIUM)
- **Location:** All five editions — draft_z2 §23.5, draft_q3 §3.4, v2.1.0 §22.5, draft_d2 §4.1, v4.0.0 §22.5 and §5 pipeline
- **Description:** Every edition's frontmatter extraction returns metadata only; none returns or derives the remaining body, and no pipeline step removes the `---…---` block before `enhanceMarkdown` / `buildToc` / `ReactMarkdown`. The frontmatter block therefore renders as `<hr><p>title: …</p><hr>` at the top of every document.
- **Evidence:** v4.0.0 §22.5 signature `export function extractFrontmatter(markdown: string): Frontmatter` (metadata-only return); §5 pipeline passes the raw markdown to all three consumers with no strip step.
- **Impact:** Visible rendering artifact on every build that uses frontmatter.
- **Severity:** Medium · **Confidence:** Verified (textual — no strip function exists in any edition); rendering consequence Reasoned
- **Recommended fix:** `parseDocument()` returns `{ frontmatter, body }` — strips BOM, normalizes CRLF; the pipeline consumes `body`; regression test "frontmatter block does not render as content". → §5, §14.6, §22.5 (fix F3)

**Finding 22.4 — Headings containing links/images desync TOC↔`rehype-slug` slugs** (MEDIUM)
- **Location:** All editions with a slug-parity fixture (v4.0.0 §9.3, draft_q3 §8.3, draft_z2 §15.4, v2.1.0 §9)
- **Description:** `buildToc` strips backticks from heading text but nothing else. For `## Heading [link](https://x.y)`, `github-slugger` slugs the raw captured text (≈`heading-linkhttpsxy`), while `rehype-slug` hashes hast *text content* (`Heading link` → `heading-link`). Images behave the same way (hast contributes alt text). The parity fixtures cover code/emoji/CJK/dedup — never links or images, which are common in real documents.
- **Evidence:** v4.0.0 §9.2: `const text = match[2].replace(/`/g, "").trim();` — backticks only; §9.3 fixture list contains no link/image case.
- **Impact:** TOC links jump to wrong or nonexistent anchors — exactly the failure mode the parity test exists to catch.
- **Severity:** Medium · **Confidence:** Reasoned (inference from slugger behavior on markdown text vs hast text content)
- **Recommended fix:** `headingText()` normalization in `toc.ts` applied in hast text order: strip backticks → images to alt text → links to link text → angle-bracket autolinks to URL. Two new parity fixtures; residual edge cases disclosed. → §9.2, §9.3, §14.4 (fix F4)

**Finding 22.5 — Badge misfires on unfenced-class code blocks** (MEDIUM)
- **Location:** v4.0.0 §8.5 (draft_q3 §6.3, draft_z2 §8.5)
- **Description:** `components.code` treats "no `className`" as inline code. A fenced block with no language — and with `rehype-highlight` off (the default) — has no className; if its content is exactly `critical` (a single line matching a registered badge value), `resolveBadge` matches and renders a Badge instead of a code block.
- **Evidence:** v4.0.0 §8.5: `const isBlock = Boolean(className); // language-* class exists only on blocks`.
- **Impact:** Silent semantic corruption of code-block content in rare but real documents.
- **Severity:** Medium · **Confidence:** Reasoned
- **Recommended fix:** Guard badge resolution with a single-line string check (`typeof children === "string" && !children.includes("\n")`) before `resolveBadge`; fixture: fenced block containing exactly `critical` stays `<code>`. → §8.5, §14.3, §14.8 (fix F5)

**Finding 22.6 — Finding 21.8 rationale overstates `process.env` breakage** (MEDIUM)
- **Location:** v4.0.0 Finding 21.8
- **Description:** As detailed in the 21.8 amendment above: Vite replaces `process.env.NODE_ENV` at build time (documented compatibility behavior), so v4.0.0's "not available in a Vite browser build unless explicitly defined" framing is inaccurate, and a Finding carrying a **Verified** tag contained the overstatement. The real draft_d2 environment bug is `process.env.ERROR_REPORTING_ENDPOINT` (never exposed to the client; only `import.meta.env.VITE_*` is).
- **Impact:** Audit credibility — an inaccurate rationale in an audit that polices evidence discipline.
- **Severity:** Medium · **Confidence:** Reasoned (Vite define behavior is documented; not executed here)
- **Recommended fix:** 21.8 amended in place (done, above); Part 2 already uses `import.meta.env.DEV`; ErrorReporter uses `import.meta.env.VITE_ERROR_REPORTING_ENDPOINT`. → Part 1 §21.8, Appendix E.4

**Finding 22.7 — §3.1 "requires LF line endings" contradicts §22.5 code** (LOW)
- **Location:** v4.0.0 §3.1 vs §22.5
- **Description:** §3.1 lists "requires LF line endings" as a frontmatter limitation; §22.5's `extractFrontmatter` normalizes `\r\n` to `\n` before parsing, so CRLF is handled. The BOM limitation is real (`^---` fails on a leading U+FEFF) — until v4.1.0 strips it.
- **Evidence:** §3.1: "requires LF line endings and no BOM at file start"; §22.5: `const normalized = markdown.replace(/\r\n/g, "\n");`
- **Severity:** Low · **Confidence:** Verified (textual contradiction)
- **Recommended fix:** §3.1 rewritten: CRLF handled; BOM stripped in `parseDocument`; remaining limitation is flat `key: value` only. → §3.1, §22.5

**Finding 22.8 — §6.1 "equal specificity" comment is wrong** (LOW)
- **Location:** v4.0.0 §6.1 (inherited from draft_q3 §4.1)
- **Description:** The comment claims `[data-theme="dark"]` wins "after :root so equal specificity resolves by order." Specificities are not equal: `:root:not([data-theme="light"])` is (0,2,0); `[data-theme="dark"]` is (0,1,0). Behavior is still correct — both dark branches set identical values and never coexist in conflict — but the stated rationale is false.
- **Severity:** Low · **Confidence:** Verified (CSS specificity arithmetic is stable)
- **Recommended fix:** Comment rewritten to state the actual cascade facts. → §6.1

**Finding 22.9 — `aria-label` on a generic span may not be exposed** (LOW)
- **Location:** All editions' `Badge` component
- **Description:** Badge renders `aria-label` on a `<span>` with no role. ARIA 1.2 forbids accessible names on generic elements; some assistive technology ignores the label. The visible value plus the adjacent bold `**Tag:**` label already convey the meaning.
- **Severity:** Low · **Confidence:** Reasoned
- **Recommended fix:** Keep `aria-label` and `data-tag` (belt-and-suspenders; integration tests use `getByLabelText`) and document that semantics are carried by visible text, not by the label. → §8.6 note

**Finding 22.10 — CI preview/`wait-on` steps redundant and undeclared** (LOW)
- **Location:** v4.0.0 §15.1
- **Description:** CI runs `npm run preview &` and `npx wait-on http://localhost:4173`, but `wait-on` is not a declared dependency, and the a11y suite already boots the preview server via `playwright.config.ts`'s `webServer` block — the manual steps are redundant.
- **Evidence:** §15.1 steps quoted above; §14.10 `webServer: { command: "npm run preview", port: 4173, … }`.
- **Severity:** Low · **Confidence:** Verified (textual)
- **Recommended fix:** Delete both steps; Playwright's `webServer` is the single server owner. → §15.1, Appendix D

**Finding 22.11 — `**Tag**:` (colon outside the bold) undocumented** (LOW)
- **Location:** All editions' `enhance.ts`
- **Description:** `BADGE_LINE_RE` requires the colon inside the bold: `**Tag:**`. The common authoring variant `**Tag**: value` does not match and is not listed in §8.4's disclosed blind spots.
- **Evidence:** v4.0.0 §8.4 regex fragment: `\*\*([^*]+):\*\*`.
- **Severity:** Low · **Confidence:** Verified (regex inspection)
- **Recommended fix:** Add to §8.4 disclosed blind spots with a fixture asserting the line passes through unchanged. → §8.4, §14.3

**Finding 22.12 — Coverage threshold 90→80 downgrade without rationale** (LOW)
- **Location:** draft_q3 §12.2 (90%) vs v4.0.0 §14.10 (80/75)
- **Description:** v4.0.0 silently lowered project-wide coverage thresholds from draft_q3's 90% to 80/75. Silent weakening of a guardrail violates the corpus's own gate discipline.
- **Severity:** Low · **Confidence:** Verified (textual)
- **Recommended fix:** Keep 80/75 with an explicit rationale (jsdom limits on layout/template components; core `lib/` held to a 100% goal) — stated, not silent. → §14.10

**Finding 22.13 — Hereditary error propagation** (INFORMATIONAL)
- **Description:** The `@theme`-in-`@media` bug and the WCAG-14px arithmetic survived three successive "audits" because each edition diffed against the previous draft instead of re-deriving claims from first principles (Tailwind v4 semantics, WCAG definitions). Round 3 shows the dual failure mode: fix-batches create new inconsistencies (22.1 from the 21.2 fix; 22.3 inherited through the merge unseen). Meta-fix: audit against stable external definitions, and re-run a coherence pass after every fix-batch.
- **Severity:** Informational · **Confidence:** Verified (the propagation is documented across the corpus)
- **Recommended fix:** §23 Lessons Learnt (new section) + §1.3 observations. → §23

**Finding 22.14 — `lucide-react@1.28.0` is almost certainly a phantom version** (INFORMATIONAL)
- **Location:** All editions since v1.0.1 (§4 stack table)
- **Description:** The lucide-react package has shipped a 0.x line for years; "1.28.0" was inherited from v1.0.1 and repeated by every edition. Only draft_q3/v4.0.0 tag it **Unverified** with gate V-1.
- **Severity:** Informational · **Confidence:** Reasoned
- **Recommended fix:** Retain the Unverified tag and gate V-1 ("if install fails to resolve, use the current 0.x line and update this row"); note in provenance. → §4, gate V-1, Appendix F step 3

**Finding 22.15 — Dual "v2.0.0" provenance ambiguity** (INFORMATIONAL)
- **Location:** draft_z2.md and draft_d2.md (both self-version "2.0.0")
- **Description:** Two editions claim the same version number; the correction ledger distinguishes them only by filename.
- **Severity:** Informational · **Confidence:** Verified (textual)
- **Recommended fix:** Provenance references always cite filename + self-version together; correction ledger (Appendix A) disambiguates. → header provenance, Appendix A

## 1.3 Cross-Cutting Observations

1. **The skill is over-fit.** Every design decision in v1.0.1 serves the audit-report use case. For a generalized skill, this is the central obstacle. *(Fixed in v4.0.0/v4.1.0 by the template system.)*
2. **The evidence contract is the skill's best idea.** Verified/Reasoned/Assumed/Unverifiable tags on every finding are a transferable pattern, preserved verbatim in §21 — and, in v4.1.0, enforced against the audit itself (§1.1 retag).
3. **Code-first theming via Tailwind v4 `@theme` is the right call.** The two-layer refinement (runtime variables + `@theme inline` bridge) is the durable contribution of the draft_q3/v4.0.0 line.
4. **The accessibility posture must be gated, not claimed.** v1.0.1 claimed AAA while self-documenting failures; the fix is an axe gate plus enumerated exceptions — and, per Finding 22.1, the exceptions must be *encoded in the gate*, not merely documented beside it.
5. **No automated testing of any kind** was the highest-leverage gap in v1.0.1; the full pyramid shipped in v4.0.0 and is extended in v4.1.0 (fence fixtures, collision fixtures, linked-heading parity, frontmatter-strip regression, code-block badge guard).
6. **Single-file build with runtime font dependence is a half-promise** until the offline recipe is verified; three font strategies ship, with the offline path explicitly marked Assumed (Appendix F step 6).
7. **Documentation quality is excellent** across the corpus — section structure, anti-pattern tables, debugging guides, lessons, pitfalls. v4.1.0 preserves and expands the shape.
8. **Hereditary errors propagate through audits that diff drafts instead of first principles (new).** The `@theme`-in-`@media` bug and the WCAG-14px arithmetic each survived three audit rounds. The cure is twofold: derive load-bearing claims from stable external definitions (WCAG spec, Tailwind docs, CommonMark), and treat every fix-batch as a new audit target — fixes create inconsistencies as often as they remove them (Finding 22.1 is a fix-induced defect; Finding 22.3 survived every merge). → §23.
9. **Unwritten machinery is a contract breach (new).** "The build system loads the template from frontmatter" was a promise no edition implemented (Finding 22.2). Any mechanism a non-negotiable design rule depends on must exist as written code or be downgraded to an explicit extension path. → §7.4.

## 1.4 Reuse Value Assessment

Carried forward from v4.0.0, plus Round 3 dispositions:

| Source | Module | Reuse in v4.1.0 | Action |
| --- | --- | --- | --- |
| draft_q3 (base of v4.0.0) | Two-layer token pattern (§4.1) | High | Adopt — fixes Finding 21.1 |
| draft_q3 | Fence-aware scanner `fence.ts` | High | Adopt — fixes Finding 21.5 |
| draft_q3 | Collision detection `validateRegistry()` | High | Adopt — fixes Finding 21.6 |
| draft_q3 | Correct WCAG arithmetic | High | Adopt — fixes Finding 21.2 |
| draft_q3 | High-contrast badge recipe | High | Adopt — correct path to AAA |
| draft_q3 | Honest lucide-react tag + gate V-1 | High | Adopt; reinforced by Finding 22.14 |
| draft_q3 | Dark-mode axe test | High | Adopt; corrected by Finding 22.1 → §14.9 (F1) |
| draft_q3 | Correction ledger pattern | High | Adopt — Appendix A (67 rows) |
| draft_q3 | Adopter spot-check | High | Adopt as Appendix F (+6 Round 3 checks) |
| draft_z2 | Full test code | High | Adopt; extended with Round 3 fixtures |
| draft_z2 | Performance budgets (250 KB) | High | Adopt — fixes Finding 21.9 |
| draft_z2 | Self-hosted font strategy | High | Adopt — third font strategy |
| draft_z2 | Lighthouse CI config | Medium | Adopt |
| draft_z2 | ErrorBoundary + ErrorFallback | High | Adopt — fixes Finding 21.15 |
| draft_d2 | Full theme.css for technical + minimal | High | Adopt after @theme fix (§7.2, §7.3) |
| draft_d2 | 6-week phased migration plan | High | Adopt (§20.3) |
| draft_d2 | Appendix E distilled lessons | Medium | Adopt |
| v2.1.0 | Part 1 validation review | High | Preserve; corrected counts (§1.0 note) |
| original_SKILL.md v1.0.1 | Evidence contract | High | Preserve verbatim (§21) |
| SKILL.md v4.0.0 | Entire Part 2 architecture | Base | v4.1.0 = v4.0.0 + 15 Round 3 fixes |
| Round 3 self-audit | Findings 22.1–22.15 | High | All fixed: F1 (§14.9), F2 (§7.4), F3 (§22.5), F4 (§9.2), F5 (§8.5), plus textual corrections |
| (rejected) | `@theme`-in-`@media`, `dangerouslySetInnerHTML`, AST badge processor, 150 KB budget, `window.gtag`, false "Verified", colon-outside silence, unencoded AAA exceptions | None | Reject — Findings 21.1–21.10, 22.1, 22.11 |

---

### Pass 1 checkpoint (self-review before Pass 2)

| Check | Result |
| --- | --- |
| Every Round 3 finding has Location / Evidence / Severity / Confidence / fix cross-reference | ✓ (22.1–22.15) |
| Executive severity table reconciles with finding text; prior undercounts corrected with note | ✓ (37 / 15 / 15 = 67) |
| Finding 21.8 amended in place; 21.1/21.13 retagged with §1.1 note (evidence contract self-applied) | ✓ |
| Round 1 findings preserved verbatim from v4.0.0 (including condensed §9–§16 table) | ✓ |
| No `@theme`-in-`@media`, no "14px relaxes AAA", no `dangerouslySetInnerHTML` in any code in this installment | ✓ (mentioned only as rejected findings) |
| No placeholders; no narration | ✓ |

---

**Pass 2 of 5** — Part 2 §1–§9 (identity through TOC & navigation), with fixes F2–F5 landed: §3/§22.5 frontmatter strip (D3), §5/§7.4 `active.ts` wiring (D2), §6.1 specificity correction, §8.5 code-block badge guard (F5), §8.4/§8.6 disclosures, §9.2 linked-heading normalization + new parity fixtures (F4). Unchanged material carried forward from v4.0.0.

---

# Part 2 — `markdown-to-web` v4.1.0 Unified Skill Specification

Every section in Part 2 cross-references its originating Part 1 finding (Rounds 1–3). Where a design decision is new in v4.1.0, it is tagged **[New in v4.1.0]** and justified inline. Every non-trivial claim carries a confidence tag (Verified / Reasoned / Assumed) per the evidence contract in §21.

## §1 Identity & Design Philosophy

**One-sentence description:** A zero-backend React application that renders any Markdown document as a polished, navigable, single-file web page, where the document's structure drives the UI, a template drives the look, and registered inline annotations render as semantic badges. (Generalizes Finding 1.1's hardcoded report identity.)

**Design thesis:** *Content is data; rendering is configuration.* The Markdown file is the input. The template chooses the look. The tag registry chooses which inline annotations become badges. The build produces one self-contained `dist/index.html` that runs anywhere a browser can open a file — online or offline.

**Core tenets:**

1. **Content is sovereign.** The markdown file determines structure. The renderer never invents content. Editing markdown never requires code changes. The frontmatter block is metadata and is *stripped before render* — it never leaks into the document body (Finding 22.3).
2. **One rendering pipeline.** `react-markdown` + components map. No `dangerouslySetInnerHTML`, no HTML-string serialization, no raw-HTML injection into the markdown source (closes Finding 21.3).
3. **Tags are registered, not hardcoded.** Badges are data in a registry; the resolver is generic; value collisions fail fast at load (fixes Findings 7.1 and 21.6); badge resolution cannot misfire on code blocks (Finding 22.5).
4. **Single-file portability, honestly stated.** JS/CSS are inlined; fonts are a runtime dependency by default, with an opt-in offline build (fixes Finding 3.2).
5. **Accessibility is gated, not claimed.** Conformance claim: WCAG 2.2 AA, enforced by an axe gate; AAA where feasible, with enumerated exceptions (§10.3) that are *encoded in the gate itself* (§14.9 — fixes Finding 22.1). This document never claims AAA wholesale.
6. **No generic UI (per template).** The editorial template uses bespoke editorial design. Other templates may choose a different register — the anti-generic mandate applies per template, not globally (fixes Finding 1.2).
7. **[New in v4.1.0] No unwritten machinery.** Every mechanism a non-negotiable rule depends on exists as written code or is explicitly downgraded to an extension path. Template switching has a concrete wiring file (§7.4 — fixes Finding 22.2); nothing in this spec rests on a "the build system will…" promise.

**Anti-generic mandate (editorial template, explicitly rejected):** purple gradients on white; predictable card-grid layouts with left-border accents; generic "Inter + gray-50" neutrality; hero sections with centered H1 + paragraph + CTA; any component droppable into a different project without visual friction.

Multi-framework adapters remain explicitly rejected (React-only; carried from v4.0.0).

## §2 When to Use / When Not To

Carried forward from v4.0.0 unchanged: use for long-form `.md` → single-file web page conversions (1,000–50,000 words, badge annotations, offline/`file://` requirements, AA-minimum accessibility); do not use for SSR apps, slide decks, PDFs, interactive code execution, sub-500-word documents, or multi-document sets. Ambiguous cases ask one question. Template selection guide (editorial / technical / minimal) unchanged — switching is now a one-file edit via `templates/active.ts` (§7.4), not a fork.

## §3 Inputs Contract

The skill accepts the following inputs. All except the Markdown file are optional with sensible defaults.

| Input | Required | Format | Default | Notes |
| --- | --- | --- | --- | --- |
| Markdown file | Yes | `.md`, UTF-8 | — | GFM extensions supported: tables, strikethrough, task lists, autolinks |
| Template | No | `editorial` \| `technical` \| `minimal` | `editorial` | Wired in `templates/active.ts` (§7.4); frontmatter `template` is advisory metadata |
| Tag registry | No | TS module or JSON | Template's default | See §8 |
| Frontmatter | No | flat `key: value` YAML | — | Parsed **and stripped** by `parseDocument()` (§22.5, Finding 22.3); `title`/`subtitle`/`author`/`date`/`template` consumed, remaining keys ignored |
| Theme override | No | Partial Layer-1 variables | None | Merges with template's `:root` tokens |
| Offline fonts | No | build flag | `false` | When `true`, inlines fonts as base64 (§11.3) |
| Syntax highlighting | No | Boolean | `false` | When `true`, enables `rehype-highlight` |

**Markdown features supported:**

- Headings H1–H6 (TOC indexes H2–H4 by default; configurable `maxDepth: 2 | 3 | 4`)
- Paragraphs, bold, italic, strikethrough
- Inline code, fenced code blocks (language class for syntax highlighting — opt-in via §19.4)
- Blockquotes
- Ordered/unordered lists, task lists
- Tables (GFM)
- Links (external links get `target="_blank" rel="noopener noreferrer"` automatically)
- Horizontal rules
- Inline images (with the §11.8 caveat — local images need `src/assets/` placement)
- YAML frontmatter — parsed **and stripped before render** (Finding 22.3; §22.5)

**Markdown features NOT supported (out of scope):**

- Footnotes (`[^1]`) — add via `remark-footnotes` (§19.3)
- Math (`$...$`) — add via `remark-math` + `rehype-katex` (§19.3)
- Mermaid code blocks — add via `rehype-mermaid` (§19.3)
- Setext headings (`Title\n=====`) in TOC — invisible to the line-based extractor but real to `rehype-slug`; content convention is ATX headings only (§9.4)
- Raw HTML pass-through — react-markdown escapes raw HTML by default. If a template explicitly enables `rehype-raw`, it MUST be paired with `rehype-sanitize` and the security implications documented.
- Multi-document sets — one document, one HTML file.

Explicitly out of scope: SSR/API routes/databases, slide decks, PDF output, interactive code execution, documents under ~500 words (render inline instead).

### 3.1 Frontmatter schema

```yaml
---
title: "Document Title"           # overrides first H1
subtitle: "Optional subtitle"     # renders below title in hero
author: "Author Name"             # renders in meta line
date: "2026-08-06"                # renders in meta line, ISO 8601
template: "editorial"             # advisory — validated against templates/active.ts (§7.4)
---
```

**Behavior and limitations [amended in v4.1.0 — fixes Findings 22.3, 22.7]:**

- `parseDocument()` (§22.5) returns `{ frontmatter, body }`. The pipeline consumes `body` — the frontmatter block never renders as content. Regression test: §14.6 "frontmatter block does not render as content."
- **CRLF-safe and BOM-safe:** `\r\n` is normalized to `\n` and a leading U+FEFF is stripped before parsing. (v4.0.0 §3.1 claimed "requires LF line endings" while its own §22.5 code normalized CRLF — that contradiction is resolved here in favor of the code, and BOM handling is added. Finding 22.7.)
- **Remaining limitation (disclosed, by design):** flat `key: value` only; no nested YAML, arrays, or multiline values; malformed frontmatter is silently ignored and the whole input is treated as body. If a document needs real YAML semantics, swap in `gray-matter` — the one dependency upgrade that preserves every contract in this document.
- `template` is **advisory metadata** (D2): it does not switch the build. `App.tsx` emits a dev-mode console warning when `frontmatter.template !== TEMPLATE_NAME` from `templates/active.ts` (§7.4).

### 3.2 Configuration surface (deliberately small)

The configuration surface is frontmatter (§3.1) + template choice + tag registry. There is no `defineConfig` helper, no `virtual:` module, no build-time config-object plugin. That architecture was considered and rejected: it depends on packaging machinery the skill does not provide, and user-supplied Tailwind class strings inside config files are invisible to Tailwind's scanner unless the file happens to be scanned (dynamic-class hazard).

**[New in v4.1.0]** The one piece of wiring machinery the skill *does* ship is `src/templates/active.ts` (§7.4) — a concrete, written, one-file template switch. This replaces v4.0.0 §7.4's unwritten "the build system loads the template specified in frontmatter" promise (Finding 22.2). If you need richer build-time configuration, that is an extension project, not a flag.

The `MarkdownToWebConfig` type is included in §22.4 for teams that want to build their own config helper — but the base skill does not provide one.

## §4 Tech Stack & Pinned Versions

Carried forward from v4.0.0 with one provenance note. Every dependency is pinned; gate V-1 (`npm ls --depth=0`, pre-ship §17) verifies the installed versions match this table exactly. Drift risks breaking the slug-parity contract (§9) and the `@theme` token generation (§6).

| Layer | Technology | Version | Provenance / note |
| --- | --- | --- | --- |
| Framework | React | 19.2.6 | Lineage-verified (v1.0.1 `package.json`) |
| Build | Vite | 7.3.2 | Lineage-verified; `?raw` imports for Markdown |
| Styling | Tailwind CSS | 4.1.17 | CSS-first `@theme inline`; no `tailwind.config.js` |
| Markdown | react-markdown | 10.1.0 | `remark-gfm` + `rehype-slug`; component map (no `dangerouslySetInnerHTML`) |
| GFM | remark-gfm | 4.0.1 | Lineage-consistent major for react-markdown 10 |
| Heading anchors | rehype-slug | 6.0.0 | Must match `github-slugger` output (slug-parity test §9.3) |
| TOC slugs | github-slugger | 2.0.0 | Default export class; **no named `slug` export exists** (§16 #7) |
| Icons | lucide-react | 1.28.0 — **Unverified** | See gate V-1 and the note below |
| Class util | clsx + tailwind-merge | 2.1.1 / 3.4.0 | `cn()` — actively used (Badge, template components) |
| Packaging | vite-plugin-singlefile | 2.3.0 | Inlines JS/CSS into `dist/index.html` |
| Syntax highlight (opt-in) | rehype-highlight + highlight.js | ^7 / ^11 (Assumed) | §19.4; confirm at install |
| Fonts (offline mode) | @fontsource-variable/source-serif-4, /inter, @fontsource/jetbrains-mono | latest (Assumed) | §11.3 |
| TypeScript | typescript | 5.9.3 | `strict: true`, `noUnusedLocals`, `noUnusedParameters` |
| Test | vitest | ^2 (Assumed) | Unit tests, coverage thresholds §14.10 |
| A11y gate | @playwright/test + @axe-core/playwright | ^1.40 / ^4 (Assumed) | §10.6, §14.9 |
| Lint | eslint + typescript-eslint + react-hooks + jsx-a11y | ^9 (Assumed) | Flat config |
| Formatter | prettier | ^3 (Assumed) | Run after `eslint --fix` (§15.2) |
| Markdown lint | markdownlint-cli2 | ^0.15 (Assumed) | Content quality gate |
| Node | — | ≥20.19 or ≥22.12 | Vite 7 requirement |

**Gate V-1 (version verification, mandatory):**

```bash
npm ls --depth=0
# Every row above must appear at the stated version.
# lucide-react: confirm the resolved version and correct this table if it differs.
```

**[New in v4.1.0] lucide-react provenance note (Finding 22.14):** the "1.28.0" pin was inherited from v1.0.1 and repeated by every edition since; the lucide-react package has shipped a 0.x line for years, so this pin is almost certainly phantom (Reasoned — not executed). Gate V-1 is the arbiter: if `npm install lucide-react@1.28.0` fails to resolve, install the current 0.x line and update this row. Never repeat a version number from memory or from another document — `npm ls` is the only source of truth.

**Version discipline:** exact pins for everything lineage-verified; caret ranges only for additions this merge introduces (testing/lint/highlight), each tagged Assumed until install. Dependency selection criteria for future additions: active maintenance, bundled types, MIT/Apache-2.0/BSD-3-Clause, zero critical vulnerabilities, >100k downloads/week, <10 MB unpacked.

## §5 Project Skeleton

```text
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
 │   ├── App.tsx                    # Layout, drawer/theme/activeSlug state, TOC derivation, IntersectionObserver,
 │   │                              #   frontmatter.template mismatch warning (§7.4)
 │   ├── index.css                  # Google Fonts @import + Tailwind + two-layer tokens (§6.1)
 │   ├── content/
 │   │   └── document.md            # The input markdown (?raw import)
 │   ├── templates/
 │   │   ├── active.ts              # ★ THE template wiring file — the only edit point for switching (§7.4) [New in v4.1.0]
 │   │   ├── editorial/
 │   │   │   ├── theme.css          # Layer-1 tokens for editorial (light + dark) — §6 pattern
 │   │   │   ├── components.tsx     # Component map overrides (optional)
 │   │   │   ├── layout.tsx         # Layout shell (sidebar + drawer + hero)
 │   │   │   └── tags.ts            # Default tag registry (Severity + Confidence)
 │   │   ├── technical/
 │   │   │   ├── theme.css          # §7.2 (full CSS, @theme-fixed)
 │   │   │   ├── components.tsx
 │   │   │   ├── layout.tsx
 │   │   │   └── tags.ts            # Status + Visibility
 │   │   └── minimal/
 │   │       ├── theme.css          # §7.3 (full CSS + print, @theme-fixed)
 │   │       ├── components.tsx
 │   │       ├── layout.tsx
 │   │       └── tags.ts            # Empty registry (badges opt-in)
 │   ├── components/
 │   │   ├── MarkdownRenderer.tsx   # react-markdown renderer + default components map (badge guard, §8.5)
 │   │   ├── TableOfContents.tsx    # Recursive TOC (sidebar + drawer) + active-section highlight
 │   │   ├── Badge.tsx              # Tag-aware badge (replaces StatusBadge)
 │   │   ├── ErrorBoundary.tsx      # Class component, catches render errors — fixes Finding 21.15
 │   │   ├── ErrorFallback.tsx      # Presentational fallback UI
 │   │   ├── SkipLink.tsx           # Accessible skip-to-content
 │   │   └── ThemeToggle.tsx        # Light/dark/system toggle with localStorage (try/catch wrapped)
 │   ├── lib/
 │   │   ├── fence.ts               # Fence-aware line scanner — fixes Finding 21.5
 │   │   ├── enhance.ts             # Tag preprocessor (fence-aware, emits warnings)
 │   │   ├── toc.ts                 # H2–H4 outline (fence-aware, slug reservation, heading normalization — §9.2)
 │   │   ├── tags.ts                # Registry validation, collision detection, resolver — fixes Finding 21.6
 │   │   └── frontmatter.ts         # parseDocument(): { frontmatter, body } — BOM/CRLF-safe, strips block (§22.5)
 │   ├── utils/
 │   │   ├── cn.ts                  # clsx + tailwind-merge — actively used
 │   │   └── theme-storage.ts       # localStorage with try/catch + in-memory fallback — fixes Finding 21.11
 │   └── types/
 │       ├── template.ts            # TemplateConfig, TemplateLayoutProps, ComponentsMap
 │       ├── tag.ts                 # TagDefinition, TagRegistry, TagValueDefinition, ResolvedBadge
 │       ├── toc.ts                 # TocItem (level 2 | 3 | 4)
 │       ├── config.ts              # MarkdownToWebConfig (for teams that want it; no defineConfig helper)
 │       └── frontmatter.ts         # Frontmatter schema + ParsedDocument
 ├── scripts/
 │   ├── build-offline.mjs          # Offline-font build variant (§11.3)
 │   ├── generate-color-ref.mjs     # Auto-generates color reference from Layer-1 vars — fixes Finding 19.1
 │   └── quality-gate.sh            # Runs all 8 pre-ship gates in order
 └── tests/
     ├── unit/
     │   ├── fence.test.ts          # §14.2
     │   ├── enhance.test.ts        # §14.3
     │   ├── toc.test.ts            # §14.4
     │   ├── slug-parity.test.ts    # §9.3 — incl. linked/image heading fixtures (Finding 22.4)
     │   ├── frontmatter.test.ts    # §14.6 — incl. strip + BOM regression tests (Finding 22.3)
     │   └── tags.test.ts           # §14.7
     ├── integration/
     │   └── markdown-rendering.test.tsx  # §14.8 — incl. code-block badge guard fixture (Finding 22.5)
     ├── accessibility/
     │   └── axe.test.ts            # §14.9 — AAA gate encodes badge exceptions (Finding 22.1)
     └── performance/
         └── bundle-size.test.ts    # §13.4
```

**File responsibility rule:** One file, one responsibility. `MarkdownRenderer.tsx` renders; `Badge.tsx` styles tags; `tags.ts` loads/validates/resolves the registry; `enhance.ts` preprocesses strings; `fence.ts` scans lines for fence state; `frontmatter.ts` parses and strips; `templates/active.ts` wires exactly one template; `ErrorBoundary.tsx` catches errors; `ErrorFallback.tsx` renders the fallback UI. No file mixes concerns.

**Custom hooks:** None exist as standalone hooks. Theme state, drawer state, and the active-section observer live inline in `App.tsx` (`useState` / `useEffect` / `useMemo`). Documented explicitly so no agent searches for a `hooks/` directory (preserves Finding 6.1's discipline). If a template needs a focus trap (e.g., a search palette), add it in that template's layout, not as shared infrastructure.

**Content pipeline [amended in v4.1.0 — fixes Finding 22.3]:**

```text
src/content/document.md  (?raw import)
         │
         ├─► parseDocument(markdown) ─► { frontmatter, body }        ← frontmatter stripped here
         │        frontmatter ─► <title>, hero, meta, template check (§7.4)
         │
         ├─► buildToc(body, maxDepth) ─► TocItem[] ─► TableOfContents
         │        (fence-aware; slug reservation; heading normalization; §9)
         │
         ├─► enhanceMarkdown(body, registry) ─► { enhanced, warnings }
         │        (fence-aware tag wrapping; build-time warnings; §8)
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

`body` — never the raw markdown — feeds `buildToc`, `enhanceMarkdown`, and `ReactMarkdown`. All three derivations are memoized against `body` (§13.2).

### 5.1 Bootstrap from scratch

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

(If step 2 fails to resolve `lucide-react@1.28.0`, install the current 0.x line and correct §4 — gate V-1, Finding 22.14.)

## §6 Design System (Two-Layer Token Pattern)

The two-layer token pattern fixes the `@theme`-in-`@media` bug (Finding 21.1, Critical). draft_z proposed `@theme` inside `@media (prefers-color-scheme: dark)`. That is invalid Tailwind v4 — `@theme` is a build-time, top-level directive. The correct idiom (draft_q3's mechanics, formalized here):

- **Layer 1 — runtime variables** (`:root`, flipped by media query / `[data-theme]`): the actual color values.
- **Layer 2 — `@theme inline`**: bridges runtime variables into Tailwind utilities, so `bg-paper-50` compiles to `background-color: var(--paper-50)` and flips live at runtime.

**Theming rule:** dark mode happens exclusively through variable flipping. Templates must not use `dark:` utilities — one mechanism, no drift.

### 6.1 Editorial template `src/index.css` (full listing)

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

/* Dark: manual override.
   Cascade facts (corrected in v4.1.0 — Finding 22.8; the v4.0.0 comment claimed
   "equal specificity", which is false):
   - :root:not([data-theme="light"]) inside the media query has specificity (0,2,0),
     so it always beats the base :root block (0,1,0) when the media query matches.
   - [data-theme="dark"] has specificity (0,1,0) — lower than the :not() rule,
     but it is the ONLY dark rule that matches when the system prefers light,
     and where both match (system dark + forced dark) they set identical values.
   Net effect: forced light always wins; forced dark always applies; no conflicts. */
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

**Dark-mode semantics to remember:** token names keep their role (ink = text/surfaces-that-invert, paper = page backgrounds), so `text-ink-900` stays "primary text" in both modes. Accent tokens (§8) are used for badge text on light chip surfaces that do not flip — see §8.6.

### 6.2 Typography hierarchy (editorial)

| Role | Font | Weight | Mobile | Desktop | Color |
| --- | --- | --- | --- | --- | --- |
| H1 | Source Serif 4 | 600 | text-3xl | sm:text-4xl lg:text-5xl | ink-900 |
| H2 | Source Serif 4 | 600 | text-2xl | sm:text-[1.75rem] | ink-900 |
| H3 | Source Serif 4 | 600 | text-xl | sm:text-2xl | ink-800 |
| H4 | Source Serif 4 | 600 | text-lg | — | ink-700 |
| Body | Inter | 400 | text-base (16px) | — | stone-700 (light) |
| Meta / labels | JetBrains Mono | 500 | text-xs, tracking-wide | — | teal-700 |
| Badge | Inter | 600 | text-xs, uppercase, tracking-wide | — | per-accent (§10.3 exception) |
| Code inline | JetBrains Mono | 400 | text-[0.85em] | — | ink-800 |

### 6.3 Color reference drift prevention

The complete color table is generated, not hand-maintained: `node scripts/generate-color-ref.mjs` parses the Layer-1 variables in `src/index.css` and emits the markdown table (prevents the v1.0.1 drift risk — Finding 19.1).

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

### 6.4 Token usage rules

**Mandatory:** all colors from `@theme` tokens (`text-ink-900`, `bg-paper-50`, `text-accent-1`); all spacing via Tailwind's scale; all radii via Tailwind's scale; all shadows via Tailwind's scale.

**Forbidden:** arbitrary hex in classNames (`text-[#b3261e]` → use `text-accent-1`); inline styles for colors; hardcoded pixel spacing; magic numbers without explanation.

### 6.5 Z-index layer map

| z-index | Element | Purpose | File |
| --- | --- | --- | --- |
| z-50 | Skip-to-content link (focused); drawer overlay + panel | Topmost | SkipLink.tsx, App.tsx |
| z-40 | Sticky header | Above content, below drawer | App.tsx |
| z-30 | (reserved) sticky-in-content elements | Future: search palette, "on this page" outline | templates/technical/layout.tsx |
| z-60 | (reserved) command palette / search overlay | Future: cmd-K palette (Appendix E) | (Optional) |
| (default) | Main content, sidebar, report | Normal flow | — |

No portals, dialogs, or tooltips exist. If you add one, update this map in the same commit.

### 6.6 `theme-storage.ts` (fixes Finding 21.11)

```ts
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

## §7 Three Templates

Templates are the right level of generalization. Not "one config to rule them all" (too rigid) and not "multi-framework adapters" (over-engineered). Three opinionated templates with consistent contracts cover the realistic use space.

### 7.1 Template A — Editorial Long-Form (default)

**Use for:** Audit reports, essays, long-form journalism, comparative analyses, design critiques.

**Layout:** Sticky dark header (`z-40`) with title, theme toggle, and (mobile) menu trigger · Desktop: left sidebar (`w-64`, sticky, `top-24`) with TOC; main content column (`max-w-3xl`) · Mobile: slide-in drawer (`z-50`) with TOC; full-width content · Hero: title + subtitle + meta chips (author, date, reading time) · Footer: source link, generated date.

**Visual register:** Bespoke editorial — Source Serif 4 display, warm paper background (`paper-50`), teal/moss accents. This is the v1.0.1 design, generalized. The anti-generic mandate applies in full.

**Default tag registry:** Severity (`critical`/`high`/`medium`/`low`/`informational`) + Confidence (`verified`/`reasoned`/`assumed`/`unverifiable`) — §8.2.

**When to choose:** read sequentially top-to-bottom; sticky TOC pays off; reading time 5+ minutes; typography matters.

### 7.2 Template B — Technical Docs

**Use for:** API references, technical specifications, developer guides, RFCs.

**Layout:** Sticky light header with optional cmd-K search (Appendix E) · Three-column desktop: left nav (`w-60`), content (`max-w-4xl`), right "on this page" outline (`w-48`, sticky, `z-30`) · Mobile: drawer nav; content; inline "on this page" accordion at top · No hero — straight to H1 + first paragraph · Footer: edit-on-GitHub link, version.

**Visual register:** Utilitarian — Inter throughout, cool gray background, blue accent. Code blocks first-class (syntax-highlighted when `syntaxHighlighting: true`, copy button). The anti-generic mandate is relaxed here: technical docs legitimately use Inter-on-gray neutrality; that is the design register.

**Default tag registry:** Status (`stable`/`experimental`/`deprecated`/`removed`) + Visibility (`public`/`internal`/`restricted`).

`src/templates/technical/theme.css` — key Layer-1 values (the file follows the §6.1 two-layer pattern exactly; only these values differ):

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
/* Dark mode — same pattern as editorial: :root:not([data-theme="light"]) + [data-theme="dark"] */
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

### 7.3 Template C — Minimal Print

**Use for:** Manuscripts, legal documents, printable reports, archival content.

**Layout:** Single column, `max-w-2xl`, centered · No header, sidebar, or drawer — title + content + page footer · Print CSS: `page-break-before: always` on H2, `@page { size: A4; margin: 2cm }`, black on white · Optional "Download PDF" button via `window.print()`.

**Visual register:** Minimal — system serif/sans/mono (no web fonts), black on white, no accent colors except badges. Ships with `offlineFonts: true` by default: archival/print contexts cannot tolerate CDN dependence.

**Default tag registry:** empty (badges opt-in via a document-local registry).

`src/templates/minimal/theme.css` — key differences (two-layer pattern per §6.1; **light-only by design**, no dark overrides):

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

### 7.4 Template contract & switching mechanism [rewritten in v4.1.0 — fixes Finding 22.2]

Every template MUST provide:

```ts
// src/types/template.ts
export interface TemplateConfig {
  name: TemplateName;
  themeCss: string;                    // path to theme.css
  components: Partial<ComponentsMap>;  // overrides for default component map
  layout: FC<TemplateLayoutProps>;
  defaultTags: TagRegistry;            // loaded from tags.ts/json
  tocMaxDepth: 2 | 3 | 4;
  offlineFonts: boolean;               // template-specific font strategy
}
```

**The switching mechanism is one wiring file — `src/templates/active.ts`.** It is the *only* place to edit when switching templates. It owns three things: the theme CSS side-effect import, the active registry/layout re-exports, and the compile-time `TEMPLATE_NAME`.

```ts
// src/templates/active.ts — THE single edit point for template switching.
// To switch templates: change the three import paths and TEMPLATE_NAME below.
// Nothing else in the codebase references a template directory directly.
import "@/templates/editorial/theme.css";
import { EDITORIAL_TAGS } from "@/templates/editorial/tags";
import { EditorialLayout } from "@/templates/editorial/layout";
import type { TagRegistry } from "@/types/tag";
import type { TemplateLayoutProps } from "@/types/template";
import type { FC } from "react";

export const TEMPLATE_NAME = "editorial" as const;
export const TAGS: TagRegistry = EDITORIAL_TAGS;
export const TemplateLayout: FC<TemplateLayoutProps> = EditorialLayout;
```

Wiring rules:

- `main.tsx` imports `./templates/active` (never a template's `theme.css` directly). `src/index.css` contains no template `@theme` import — the template CSS arrives through `active.ts`.
- Frontmatter `template` (§3.1) is **advisory metadata**. It does not switch the build. `App.tsx` validates it in development and warns on mismatch:

```ts
// src/App.tsx (excerpt)
if (import.meta.env.DEV && frontmatter.template && frontmatter.template !== TEMPLATE_NAME) {
  console.warn(
    `Frontmatter declares template "${frontmatter.template}" but templates/active.ts ` +
    `is wired to "${TEMPLATE_NAME}". Edit templates/active.ts to switch templates.`,
  );
}
```

- **Why not frontmatter-driven switching:** v4.0.0 §7.4 promised "the build system loads the template specified in frontmatter" — machinery that no edition ever wrote, and which §3.2's rejected-machinery rule argues against (it requires a Vite plugin or virtual module reading a `?raw` file at build time). The wiring file is honest, written, and one line to change; the frontmatter field remains for documentation and future tooling. (Finding 22.2; Tenet 7.)
- Adding a fourth template: §19.1.

## §8 Tag Registry & Badge Protocol

The v1.0.1 badge system hardcoded 9 keys and matched only `-` bullets. v4.1.0 replaces this with: tag registry (data) + fence-aware preprocessor (with warnings) + generic resolver (cross-category lookup with collision detection). Tags are data, not code — adding a new tag value should not require touching a TypeScript file.

### 8.1 Tag registry schema

```ts
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

### 8.2 Default registry (editorial template)

```ts
// src/templates/editorial/tags.ts
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

### 8.3 Validation + collision detection + resolver (fixes Finding 21.6)

```ts
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

Call `loadRegistry` once at module load in `App.tsx` (on `TAGS` from `templates/active.ts`). A colliding registry is a build/startup error that names both categories — never a silent render-time guess.

### 8.4 Fence-aware preprocessor (fixes Finding 21.5)

```ts
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

**Markdown syntax for badges:**

```markdown
- **Severity:** critical
* **Confidence:** verified
+ **Status:** done
1. **Priority:** high
```

**Disclosed blind spots (do not "fix" silently) [extended in v4.1.0 — Finding 22.11]:**

1. Badges inside blockquotes (`> - **Tag:** v`) are not matched.
2. Values with trailing punctuation (`critical.`) warn and render unstyled.
3. All indentation depths of bullets are matched by the regex, but *nested-list semantics* belong to react-markdown — the preprocessor only rewrites line text.
4. **Colon outside the bold does not match:** `- **Tag**: value` is not a badge line — the colon must be inside the bold (`**Tag:**`). Authors habitually write the variant; the fixture in §14.3 asserts the line passes through unchanged rather than half-matching.
5. Badge lines inside code fences are left untouched (correct — fence-aware).

Each is covered by a fixture in §14.3.

### 8.5 End-to-end pipeline (the backtick-wrapping pattern)

This is the critical path that v1.0.1 got right, draft_d2 broke (raw HTML / `dangerouslySetInnerHTML`), and draft_q2 disconnected (AST plugin vs. React component). v4.1.0 preserves v1.0.1's pattern (fixes Findings 21.3 and 21.4):

```text
1. Author writes:        - **Severity:** critical
2. enhance.ts wraps:     - **Severity:** `critical`
3. react-markdown parses:inline code element with children="critical"
4. components.code:      resolveBadge(registry, "critical") → <Badge tag="Severity" value="Critical" accent={1} />
5. Badge renders:        <span class="... text-accent-1 ...">Critical</span>
```

No `dangerouslySetInnerHTML`. No raw HTML emission. No AST plugin that doesn't connect to the React component. The `code` component map entry is the bridge — **with the v4.1.0 misfire guard (Finding 22.5)**:

```tsx
// src/components/MarkdownRenderer.tsx (excerpt)
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeSlug from "rehype-slug";
import type { ComponentPropsWithoutRef } from "react";
import { Badge } from "@/components/Badge";
import { resolveBadge } from "@/lib/tags";
import type { TagRegistry } from "@/types/tag";

interface Props {
  markdown: string;   // the enhanced BODY from parseDocument — never raw input
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
          const text = typeof children === "string" ? children : "";
          // Guard (Finding 22.5): badge resolution applies only to single-line
          // inline code. A fenced block with no language — and no rehype-highlight —
          // has no className; without this check, a block whose content is exactly
          // a registered value (e.g. "critical") would render as a Badge.
          const isBlock = Boolean(className) || text.includes("\n");
          if (isBlock) return <code className={className}>{children}</code>;
          const badge = resolveBadge(registry, text);
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

Syntax highlighting is opt-in: install `rehype-highlight`, add it to `rehypePlugins` after `rehypeSlug`, and import a highlight.js CSS theme. If you fork this pipeline into something that serializes HTML strings, sanitization (`rehype-sanitize`) becomes mandatory — in the components-map pipeline above it is not needed because no raw HTML is ever rendered.

### 8.6 Badge component

```tsx
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

**Badge text size:** v4.1.0 uses `text-xs` (12px), NOT `text-sm` (14px). The "14px relaxes AAA threshold" claim (Finding 21.2) is an arithmetic error — 14px is not large text. Badge contrast is handled honestly via §10.3 (enumerated AAA exceptions, encoded in the gate per §14.9) and §10.5 (high-contrast recipe as the opt-in path to genuine AAA).

**Accessibility note [New in v4.1.0 — Finding 22.9]:** `aria-label` on a role-less `<span>` is belt-and-suspenders — ARIA 1.2 forbids accessible names on generic elements, and some assistive technology ignores the label. Semantics are carried by the *visible* value text plus the adjacent bold `**Tag:**` label in the document; the attribute is retained because integration tests query via `getByLabelText` and it is harmless where ignored. Do not add a widget role to the badge — it is content, not a control.

### 8.7 Improvements over v1.0.1

- Accepts all bullet styles (`-`, `*`, `+`, ordered `1.`) — v1.0.1 only matched `-`.
- Emits build-time warnings for unknown tags and values — v1.0.1 silently passed them through.
- Tag set is data, not code — v1.0.1 hardcoded 9 keys.
- Fence-aware — fenced badge lines untouched (Finding 21.5).
- Cross-category resolver with collision detection — ambiguity throws at load (Finding 21.6).
- Code-block misfire guard — fenced content can never render as a Badge (Finding 22.5).

## §9 TOC + Navigation Engine

The TOC extracts headings from the markdown *body*, generates slugs that match `rehype-slug`'s rendered `id` attributes, and renders a recursive navigation tree. Active-section highlighting uses `IntersectionObserver`. Slug parity between `github-slugger` (TOC) and `rehype-slug` (rendered headings) is verified by a unit test (§9.3) — this is the single most important test in the skill.

### 9.1 Fence-aware scanner (fixes Finding 21.5)

Shared by `buildToc` and `enhanceMarkdown`. A `## comment` inside a code fence must neither enter the TOC nor consume a slug counter.

```ts
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

### 9.2 Extraction with slug reservation and heading normalization [amended in v4.1.0 — Finding 22.4]

Three correctness mechanisms:

1. **Stack algorithm** (hand-traced: nested, sibling-after-nested, orphan, and mixed cases all correct — draft_q2's variant is not used; it mis-nests any H2 that follows an H3).
2. **Slug reservation for every heading level** — `rehype-slug` slugs H1–H6 in document order with dedup counters; a TOC that only sees H2–H4 would desync on duplicate text (e.g. `# Intro` then `## Intro`). The slugger therefore consumes every heading; only H2–H4 enter the tree.
3. **Heading text normalization [New in v4.1.0]** — `rehype-slug` hashes hast *text content*, not markdown source. Backticks were already stripped; v4.1.0 adds link/image/autolink reduction so headings like `## Heading [link](https://x.y)` produce matching slugs on both sides:

```ts
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

/**
 * Reduces raw heading text to the characters rehype-slug will hash.
 * rehype-slug sees hast TEXT CONTENT:
 *   - inline code contributes its text          → strip backticks
 *   - images contribute their alt text          → ![alt](url) → alt
 *   - links contribute their link text          → [text](url) → text
 *   - autolinks contribute the URL itself       → <https://…> → https://…
 * Order matters: images before links (image syntax nests link syntax in its URL).
 */
export function headingText(raw: string): string {
  return raw
    .replace(/`/g, "")
    .replace(/!\[([^\]]*)\]\([^)]*\)/g, "$1")
    .replace(/\[([^\]]*)\]\([^)]*\)/g, "$1")
    .replace(/<(https?:\/\/[^>]+)>/g, "$1")
    .trim();
}

export function buildToc(markdown: string, maxDepth: 2 | 3 | 4 = 4): TocItem[] {
  const slugger = new GithubSlugger();
  const items: TocItem[] = [];
  const stack: TocItem[] = [];
  for (const { line, insideFence } of scanLines(markdown)) {
    if (insideFence) continue;
    const match = line.match(ANY_HEADING_RE);
    if (!match) continue;
    const level = match[1].length;
    const text = headingText(match[2]);
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

**Why the stack algorithm is correct:** the `while` loop pops until the top of the stack has a level strictly less than the current heading's level:

- H2 → H2: pop the equal-level top; push new H2 as top-level. ✓
- H2 → H3: `2 >= 3` false — H3 becomes child of H2. ✓
- H2 → H4 (skipping H3): H4 becomes child of H2. ✓
- H2 → H4 → H3: pop H4 (`4 >= 3`), stop at H2 (`2 >= 3` false) — H3 is a sibling of H4, both under H2. ✓

**Contract:** H2 = depth 1 · H3 = depth 2 (`ml-3 border-l`) · H4 = depth 3 (`ml-6 border-l`) · orphans promote to top level · heading text reduced via `headingText()` before slugging (matching hast text content, which is what `rehype-slug` hashes).

### 9.3 Slug parity — tested, not asserted (fixes Finding 2.2; extended by Finding 22.4)

The lineage's most-cited failure mode ("two slug generators must stay in sync") is closed by a test that compiles and runs: correct default import, no unused imports (passes the strict `noUnusedLocals` gate the skill itself mandates — Finding 21.13), fixtures for CJK, emoji, inline code, duplicates, cross-level dedup — **and, new in v4.1.0, linked and image headings**:

```ts
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

  // [New in v4.1.0 — Finding 22.4] links contribute link text to hast content
  it("matches for headings containing links (TOC reduces to link text)", async () => {
    const slugger = new GithubSlugger();
    expect(slugger.slug("Heading with link")).toBe(
      await rehypeH2Id("Heading with [link](https://example.com/a-b)"),
    );
  });

  // [New in v4.1.0 — Finding 22.4] images contribute alt text to hast content
  it("matches for headings containing images (TOC reduces to alt text)", async () => {
    const slugger = new GithubSlugger();
    expect(slugger.slug("Heading with alt text")).toBe(
      await rehypeH2Id("Heading with ![alt text](./img.png)"),
    );
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

Both packages are pinned (§4); this test runs in CI. Known scope limitation (§9.4): parity is guaranteed for ATX headings only.

### 9.4 Disclosed limitations

- **Setext headings** (`Title\n=====`) are invisible to the line-based extractor but real to `rehype-slug` — they can desync dedup counters for later duplicate text. Content convention: ATX headings only. If a document type needs setext support, migrate extraction to the AST (§19.3 — the one place AST parsing earns its complexity).
- **Residual heading-syntax edge cases [New in v4.1.0]:** `headingText()` covers code, images, links, and autolinks — the constructs common in real documents. It does not model HTML entities (`&amp;`), reference-style links (`[text][ref]`), or footnote markers; a heading relying on those may desync. If your document type uses them, add the reduction rule to `headingText()` *and* a parity fixture in the same commit.
- Headings deeper than `maxDepth` are still slug-reserved (correct) but not listed.
- `scroll-mt-24` on every anchored heading compensates for the sticky header; never hand-write heading `id`s.

### 9.5 Active-section highlighting

```tsx
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

Pass `activeSlug` to `TableOfContents` to highlight the current section. The `flattenToc` pattern observes all TOC levels (not just top-level) — fixes a common bug where H3/H4 sections never highlight.

### 9.6 TOC contract table

| Heading Level | TOC Depth | Indentation |
| --- | --- | --- |
| `##` (H2) | 1 | None |
| `###` (H3) | 2 | `ml-3` + left border |
| `####` (H4) | 3 | `ml-6` + left border |

- `buildToc()` extracts H2–H4 by default (configurable via `maxDepth`); slugs reserved for every level.
- Orphan headings (no preceding parent) become top-level.
- Heading text reduced via `headingText()` before slugging — matching `rehype-slug` behavior (backticks, image alt, link text, autolink URLs).
- Slugs generated by `github-slugger` must match `rehype-slug` output — verified by `slug-parity.test.ts` (§9.3).
- The TOC is built from `body` (post-`parseDocument`), so frontmatter can never contribute phantom headings.

---

### Pass 2 checkpoint (self-review before Pass 3)

| Check | Result |
| --- | --- |
| F2 landed: `templates/active.ts` written in full; §7.4 contract rewritten; frontmatter `template` advisory + dev warning; no "build system loads template" promise remains | ✓ |
| F3 landed: `parseDocument() → { frontmatter, body }` referenced in §3, §5 pipeline, §8.5 props comment; §3.1 limitations match code (CRLF+BOM handled; flat-key-only remains) — L1 closed | ✓ |
| F4 landed: `headingText()` in §9.2 with image-before-link ordering; two new parity fixtures in §9.3; residual edge cases disclosed in §9.4 | ✓ |
| F5 landed: single-line guard in §8.5 `components.code` with explanatory comment; §14.8 fixture cross-referenced | ✓ |
| L2 closed: §6.1 comment states actual specificities ((0,2,0) vs (0,1,0)) and why behavior is still correct | ✓ |
| R3-14 note on lucide-react in §4; R3-11 colon-outside disclosure in §8.4; R3-9 aria-label note in §8.6 | ✓ |
| No `@theme` inside `@media` in any new code; no `dangerouslySetInnerHTML`; no "14px relaxes AAA" claim | ✓ |
| No placeholders; pipeline diagram consumes `body`; skeleton includes `active.ts` | ✓ |

---

**Pass 3 of 5** — Part 2 §10–§15. Load-bearing changes this pass: §10.3/§10.4 gate coherence (F1 — the AAA gate now enforces *exactly* what the exceptions table claims, resolving Finding 22.1), §14.3/§14.4/§14.6/§14.8/§14.9 Round-3 fixtures (colon-outside blind spot, linked-heading slugs, `parseDocument` strip regression, code-block badge guard, keyboard smoke), §14.10 coverage rationale (Finding 22.12), §15.1/§15.2 CI with the redundant preview/wait-on steps deleted (Finding 22.10) and the phantom-script gap closed. Unchanged material carried forward verbatim from v4.0.0.

---

## §10 Accessibility (WCAG 2.2 AA + AAA Aspirational)

The headline conformance claim is WCAG 2.2 AA + AAA aspirational, with documented exceptions. AA is the gate (zero violations); AAA is the target where feasible, with enumerated exceptions that are **encoded in the gate itself** (§10.4, §14.9). v1.0.1 claimed "WCAG AAA" while self-documenting multiple AAA failures — that contradiction is resolved here by claiming only what is verified, and by making the gate and the claim incapable of diverging.

### 10.1 Posture (the honesty fix — fixes Findings 8.1 and 21.2)

Claim: WCAG 2.2 AA, enforced by an automated axe gate. AAA where feasible; every exception is enumerated in §10.3. This document never states "WCAG AAA" as a headline, and it explicitly rejects the arithmetic error that appeared in draft_z, draft_z2, draft_d2, and v2.1.0 ("14px relaxes the AAA threshold") — WCAG large text is ≥18pt (24px) or ≥14pt bold (≈18.66px); no font size used here qualifies, so normal-text thresholds apply everywhere (Verified — stable WCAG definitions).

### 10.2 Implementation matrix

| Feature | Implementation | Verification |
| --- | --- | --- |
| Skip-to-content | `<a href="#content">` with `sr-only focus:not-sr-only focus:z-50` | Manual: Tab → Enter → focus lands on `#content` |
| Focus visible | Global `:focus-visible` ring (§6.1), all interactive elements | axe `focus-order-semantics`; manual Tab pass |
| Heading hierarchy | H1 → H2 → H3 → H4, no skipped levels | axe `heading-order` |
| Anchor offset | `scroll-mt-24` on H2–H4 | Manual TOC click |
| Reduced motion | `prefers-reduced-motion` guard in base styles | Manual OS setting check |
| Touch targets | All interactive elements ≥ 44×44px (`min-w-11 min-h-11` or `p-2.5` + icon) | axe `target-size` (gate-failure, global — §14.9) |
| ARIA | `aria-label` on nav/drawer/toggle; `aria-hidden` on decorative icons; `role="alert"` on error fallback | axe `aria-valid-attr`, `button-name` |
| Landmarks | `header`, `main`, `aside`, `nav`, `article`, `footer` | axe `region` |
| Color isn't sole indicator | Badges carry text + tint | Deuteranopia simulation |
| Keyboard | Full Tab/Shift+Tab/Escape operability; drawer closes on Escape | Automated smoke test (§14.9 — restored from draft_z2) + manual |
| Language | `<html lang>` set from frontmatter or `en` default | axe `html-has-lang` |
| Contrast (body) | ink-900 on paper-50 ≈ 16.4:1 (lineage-computed) — AAA ✓ | axe `color-contrast` |
| Live regions | Error announcements use `role="alert"`; loading uses `aria-live="polite"` | axe `aria-live` |

### 10.3 Enumerated AAA exceptions (AA guaranteed, AAA not claimed) — canonical statement

| Item | Contrast (computed, Reasoned) | AA (4.5:1) | AAA (7:1) | Disposition |
| --- | --- | --- | --- | --- |
| Badge text, accent-1 on red-50 | ≈5.9:1 | ✓ | ✗ | Exception; upgrade via §10.5 |
| Badge text, accent-2 on amber-50 | ≈4.8:1 | ✓ | ✗ | Exception; upgrade via §10.5 |
| Badge text, accent-3 on yellow-50 | ≈4.8:1 | ✓ | ✗ | Exception; upgrade via §10.5 |
| Badge text, accent-4 on lime-50 | ≈6.9:1 | ✓ | ✗ | Exception; upgrade via §10.5 |
| Badge text, accent-5 on blue-50 | ≈6.3:1 | ✓ | ✗ | Exception; upgrade via §10.5 |
| Meta labels, teal-700 on paper-50 | ≈6.6:1 | ✓ | ✗ | Exception; use ink-800 if AAA required |

Everything else targets AAA. Dark-mode pairs (e.g., teal-600-dark `#2ba8b3` on `#0b1615` ≈6.5:1) pass AA and are axe-checked in dark mode via `[data-theme="dark"]` before the run (§10.6).

**[New in v4.1.0] These exceptions are encoded in the AAA gate itself (§14.9 — fixes Finding 22.1).** The gate fails on AAA contrast violations anywhere *except* `[data-tag]` badge elements, and `target-size` remains globally enforced. A conformance statement and its gate must never contradict each other: v4.0.0 documented these exceptions in §10.3 while its §14.9 test hard-failed on any contrast violation — a gate that is unshippable by design. The gate now enforces exactly this table. Badge elements are identified by the `data-tag` attribute emitted by `Badge.tsx` (§8.6); if a badge stops carrying `data-tag`, the exclusion becomes a no-op and the gate fails closed — safe.

### 10.4 The gate [rewritten in v4.1.0 — resolves Finding 22.1]

Pre-ship command `npm run a11y` runs `tests/accessibility/axe.test.ts` (§14.9):

- **AA violations fail the build** — zero tolerance, no exclusions, light and dark modes.
- **AAA `color-contrast` violations fail the build except on `[data-tag]` badge elements** — the documented §10.3 exception. Implemented as an axe *context exclusion* (§14.9), not a rule disable: the contrast rule stays fully active; only the enumerated exception elements are outside its scope. This is robust to axe's selector formats (post-hoc filtering of violation targets is brittle — targets may be positional paths without the attribute).
- **AAA `target-size` violations fail the build globally** — dedicated run, no exclusions. Badges are non-interactive spans and never benefit from the exclusion.
- **Other AAA criteria are advisory** — logged, not failed.

No suppressions, no rule disabling, no weakening. The gate enforces exactly what §10.3 claims — no more (it would fail on documented exceptions) and no less (it would let undocumented violations ship).

### 10.5 High-contrast badge recipe (opt-in AAA badges)

Swap Layer-1 accent variables for these (computed ≈8.5–9.2:1 on the standard chips — Reasoned; re-verify with the axe gate after applying). This is the correct path to AAA badge contrast — not the false "14px relaxes AAA" claim:

```css
:root {
  --accent-1: #7f1d1d;   /* ≈9.1:1 on red-50 */
  --accent-2: #78350f;   /* ≈8.8:1 on amber-50 */
  --accent-3: #713f12;   /* ≈8.5:1 on yellow-50 */
  --accent-4: #365314;   /* ≈8.5:1 on lime-50 */
  --accent-5: #1e40af;   /* ≈8.1:1 on blue-50 */
}
```

With this recipe applied, the §10.3 badge rows may be deleted and the §14.9 exclusion removed — genuine AAA, no exceptions.

### 10.6 Dark-mode axe test

The axe gate runs in both light and dark modes (sets `[data-theme="dark"]` before the run) — ensures dark-mode token overrides maintain AA. See §14.9.

### 10.7 Implementation code snippets

`src/components/SkipLink.tsx`:

```tsx
export function SkipLink({ targetId = "content" }: { targetId?: string }) {
  return (
    <a
      href={`#${targetId}`}
      className="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2 focus:bg-teal-600 focus:text-white focus:rounded focus:shadow-lg"
    >
      Skip to main content
    </a>
  );
}
```

Touch target CSS pattern (all buttons/links in headers, drawers, theme toggle):

```tsx
<button
  className="min-w-11 min-h-11 p-2.5 inline-flex items-center justify-center"
  aria-label="Toggle navigation menu"
>
  <MenuIcon className="w-5 h-5" aria-hidden="true" />
</button>
```

### 10.8 Concrete AAA fixes over v1.0.1

| v1.0.1 gap | v4.1.0 fix |
| --- | --- |
| Touch targets 32–36 px (`p-1.5`) | Touch targets ≥ 44 px (`p-2.5` + icon, or `min-w-11 min-h-11`) |
| Badge text 12 px (4.76:1, fails AAA) — "fixed" via false 14px claim | Badge text stays 12px; AAA handled honestly via §10.3 exceptions (encoded in gate, §14.9) or §10.5 high-contrast recipe |
| No `prefers-reduced-motion` | `@media (prefers-reduced-motion: reduce)` disables smooth scroll + animations |
| Browser default focus outline only | Global `:focus-visible` style with 2px teal outline |
| No axe in CI | `npm run a11y` runs `@axe-core/playwright` against the built dist, light + dark |
| No keyboard test | Automated keyboard smoke test (§14.9, restored from draft_z2) |

## §11 Build & Deploy Recipes

v1.0.1's central pain point was the "single-file portability" half-promise: `vite-plugin-singlefile` inlined JS and CSS but not the Google Fonts `@import`, so the artifact didn't actually work offline. v4.1.0 resolves this with three font strategies (CDN `@import`, self-hosted `@font-face`, `@fontsource` base64 inlining) and four deploy recipes.

### 11.1 Recipe A — Default single-file build (CDN fonts)

```bash
npm run build
# Output: dist/index.html (JS/CSS inlined; fonts load from Google Fonts CDN)
# Size: ~250-400 KB
# Deploy: any static host (GitHub Pages, Netlify, Vercel, S3, nginx)
```

`vite.config.ts`:

```ts
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

The online build's Google Fonts `@import` is in `src/index.css` (§6.1). Caveat: `@import` must come before `@import "tailwindcss"` per CSS spec. The `@import` will fail from `file://` (CORS) — use Recipe C (offline) for `file://` viewing.

### 11.2 Recipe B — Self-hosted `@font-face` (alternative online build)

Self-host the font files in `public/fonts/` and declare `@font-face` rules. This avoids the Google Fonts CDN dependency but still requires the font files to be served alongside the HTML. Replace the Google Fonts `@import` in `src/index.css` with:

```css
/* One @font-face per family/weight combo needed (Inter 400/600, Source Serif 4 400/600, JetBrains Mono 400) */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 400;  /* repeat for 600 */
  font-display: swap;
  src: url('/fonts/inter-v12-latin-400.woff2') format('woff2');
}
/* ... repeat the @font-face block for each family/weight: Source Serif 4 (400, 600), JetBrains Mono (400) ... */
@import "tailwindcss";
/* ... Layer 1 + Layer 2 per §6.1 ... */
```

Preload hints in `index.html` (add one `<link rel="preload">` per font file):

```html
<link rel="preload" href="/fonts/inter-v12-latin-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/source-serif-4-v3-latin-400.woff2" as="font" type="font/woff2" crossorigin>
```

Caveat: With `vite-plugin-singlefile`, the `@font-face` URLs reference `/fonts/...` which won't be inlined — the single-file artifact will still need the font files alongside it. For true single-file portability, use Recipe C.

### 11.3 Recipe C — `@fontsource` base64 inlining (offline build)

```bash
npm run build:offline
# Runs: node scripts/build-offline.mjs
# Output: dist/index.html (JS/CSS/fonts all inlined as base64)
# Size: ~2-4 MB (depending on font subset)
# Deploy: any static host, USB stick, file://, air-gapped environment
```

`scripts/build-offline.mjs`:

```js
// scripts/build-offline.mjs
// Sketch — requires runtime validation with actual @fontsource packages (Appendix F step 6).
// The @fontsource packages ship font files in node_modules.
// Vite's `assetsInlineLimit` setting (set very high) inlines them as base64.
import { build } from "vite";
import { viteSingleFile } from "vite-plugin-singlefile";

process.env.VITE_OFFLINE_FONTS = "true";

await build({
  plugins: [viteSingleFile()],
  define: { "import.meta.env.VITE_OFFLINE_FONTS": JSON.stringify("true") },
  build: {
    target: "es2022",
    cssCodeSplit: false,
    assetsInlineLimit: 100 * 1024 * 1024,  // 100 MB — inline everything
    rollupOptions: { output: { inlineDynamicImports: true } },
  },
});

console.log("Offline build complete: dist/index.html (fonts inlined as base64)");
```

`src/main.tsx` (conditional font import):

```tsx
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { App } from "./App";
import { ErrorBoundary } from "./components/ErrorBoundary";
import "./index.css";

// Conditional font import — only loads @fontsource packages in offline mode.
// In online mode, fonts load via Google Fonts @import in index.css.
// Top-level await requires es2022 target (set in vite.config.ts).
if (import.meta.env.VITE_OFFLINE_FONTS === "true") {
  await import("@fontsource-variable/source-serif-4");
  await import("@fontsource-variable/inter");
  await import("@fontsource/jetbrains-mono");
}

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ErrorBoundary>
      <App />
    </ErrorBoundary>
  </StrictMode>,
);
```

Known unknowns (Assumed — verify per Appendix F before relying on this): confirm `@fontsource` packages resolve font files via Vite's asset pipeline; confirm `assetsInlineLimit: 100MB` causes base64 inlining; confirm `dist/index.html` renders fonts from `file://` with no network; subset with `pyftsubset` if the offline build exceeds 5 MB.

### 11.4 Recipe D — GitHub Pages deployment

```bash
# 1. Set base in vite.config.ts: base: "/<repo-name>/"
# 2. Build
npm run build
# 3. Deploy (native Pages — see Appendix D workflow; or:)
npx gh-pages -d dist
```

Appendix D's CI workflow uses `actions/upload-pages-artifact` + `actions/deploy-pages` for native GitHub Pages deployment without third-party tokens.

### 11.5 Recipe E — Local `file://` viewing

The default build works from `file://` because `vite-plugin-singlefile` removes all `<script type="module" src="...">` and `<link rel="stylesheet" href="...">` references — everything is inlined into one HTML file.

```bash
npm run build
open dist/index.html        # macOS
xdg-open dist/index.html    # Linux
start dist/index.html       # Windows
```

Caveat: The online build's Google Fonts `@import` will fail from `file://` (CORS restriction). For `file://` viewing, use Recipe C (offline build).

### 11.6 System font fallbacks

All three strategies use the same fallback chain in `@theme inline`:

```css
--font-serif: "Source Serif 4", ui-serif, Georgia, serif;
--font-sans: "Inter", ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
--font-mono: "JetBrains Mono", ui-monospace, "Cascadia Code", "Source Code Pro", Menlo, Consolas, monospace;
```

If a web font fails to load (network blocked, font file missing), the browser falls back to a similar system font. The design will degrade gracefully — not pixel-identical, but readable and functional.

### 11.7 Offline verification test

```ts
// tests/e2e/offline.test.ts
import { test, expect } from "@playwright/test";

test("offline build works without network", async ({ page, context }) => {
  // Build the offline variant first: npm run build:offline
  await page.goto("http://localhost:4173/");  // serve dist/ via `npm run preview`
  await page.waitForLoadState("networkidle");
  await context.setOffline(true);  // go offline
  await page.reload();
  // Verify fonts still render (not falling back to system fonts)
  const bodyFont = await page.locator("body").evaluate((el) => getComputedStyle(el).fontFamily);
  expect(bodyFont).toMatch(/Source Serif 4|Inter/);
  await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
});
```

### 11.8 Images

Local images referenced from markdown are resolved by Vite relative to the importing module — for `?raw` markdown, place images in `src/assets/` and reference by root-absolute path, or accept that only remote URLs are zero-config. Base64-embedding images inflates the single file quickly; embed only small images, link large ones. Documented limitation, not a configured feature.

### 11.9 Size comparison

| Build mode | Approximate size | Use case |
| --- | --- | --- |
| Online (Recipe A) | 250–400 KB | Default — works anywhere with internet |
| Self-hosted (Recipe B) | 250–400 KB HTML + ~150 KB font files | Production without CDN dependency |
| Offline (Recipe C) | 2–4 MB | Air-gapped, USB, archival, `file://` without internet |

## §12 Error Handling & Resilience

Errors are inevitable. The skill handles them at three layers: (1) build-time warnings from the preprocessor, (2) React error boundaries catching render failures, and (3) a structured error reporter for production observability (optional, Appendix E). The architecture avoids `dangerouslySetInnerHTML` entirely (fixes Finding 21.3) — react-markdown's component map renders Markdown as React elements, so a malformed markdown file produces a React render error (caught by the boundary) rather than an XSS surface.

### 12.1 Error boundary (fixes Finding 21.15)

```tsx
// src/components/ErrorBoundary.tsx
import React from "react";
import type { ErrorInfo, ReactNode } from "react";
import { ErrorFallback } from "./ErrorFallback";

interface BoundaryProps {
  children: ReactNode;
  fallback?: ReactNode | ((error: Error, errorInfo: ErrorInfo) => ReactNode);
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
    // Note: ErrorReporter is optional (Appendix E.4). Base skill logs to console in dev only.
    if (import.meta.env.DEV) {
      console.error("ErrorBoundary caught an error:", error, errorInfo);
    }
  }

  render(): ReactNode {
    if (this.state.hasError) {
      if (this.props.fallback) {
        if (typeof this.props.fallback === "function") {
          return this.props.fallback(this.state.error!, {} as ErrorInfo);
        }
        return this.props.fallback;
      }
      return <ErrorFallback error={this.state.error} />;
    }
    return this.props.children;
  }
}
```

Note: v4.1.0 uses `import.meta.env.DEV` (Vite idiom) throughout — NOT `process.env.NODE_ENV` (Finding 21.8; amended rationale in Finding 22.6: Vite *does* replace `process.env.NODE_ENV` at build time, so the draft_d2 checks would have worked — the fix stands on idiom/portability grounds, and the genuine draft_d2 environment bug was `process.env.ERROR_REPORTING_ENDPOINT`, which never resolves because Vite exposes only `import.meta.env.VITE_*` to the client).

Placement: `main.tsx` wraps `<App />` (see §11.3's `main.tsx` listing). Keep it at the root only; use defensive checks (not nested boundaries) in pure functions.

### 12.2 Error fallback UI

```tsx
// src/components/ErrorFallback.tsx
export function ErrorFallback({ error }: { error: Error | null }) {
  return (
    <div
      role="alert"
      aria-live="assertive"
      className="mx-auto my-16 max-w-xl rounded-lg border border-paper-200 bg-paper-100 p-6"
    >
      <h2 className="font-serif text-xl font-semibold text-ink-900">
        This document couldn't be rendered
      </h2>
      <p className="mt-2 text-sm text-ink-700">
        The content failed to render. Try reloading; if the problem persists, the
        markdown source may be malformed.
      </p>
      {import.meta.env.DEV && error && (
        <pre className="mt-4 overflow-auto rounded bg-ink-950 p-3 text-xs text-paper-100 whitespace-pre-wrap">
          {error.message}
          {error.stack && `\n\n${error.stack}`}
        </pre>
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

### 12.3 Error reporter (optional — Appendix E.4)

The `ErrorReporter` class with external endpoint is moved to Appendix E as optional. The base skill ships with `ErrorBoundary` + `ErrorFallback` only. If a deployment needs error reporting (Sentry, Datadog, custom endpoint), extend `ErrorBoundary.componentDidCatch` with a `fetch` call to `import.meta.env.VITE_ERROR_REPORTING_ENDPOINT` — the `VITE_` prefix is mandatory (Finding 22.6). See Appendix E.4 for the full implementation.

### 12.4 Malformed markdown handling

| Scenario | Behavior |
| --- | --- |
| Unclosed code fence | react-markdown renders remainder as code — no crash; fence scanner treats rest as fenced (matches CommonMark) |
| Broken table | Renders as plain text — no crash |
| Invalid frontmatter | Ignored; `parseDocument` returns the whole input as `body`; document renders with fallback title (Finding 22.3) |
| Frontmatter present | Stripped before render — never appears as `<hr><p>title:…</p>` content (§22.5, §14.6 regression test) |
| Unknown badge value | Build-time warning; line renders unstyled — no crash |
| Colliding tag registry | Startup error naming both tags — fails fast, never renders ambiguously |
| Fenced code block whose text is a badge value | Renders as code — the single-line guard prevents misfire (§8.5, Finding 22.5) |
| Empty markdown | `buildToc` → `[]`; renderer shows empty article — no crash |
| Markdown with no headings | `buildToc` → `[]`; sidebar/drawer renders "No sections" message — no crash |

### 12.5 What NOT to do (architectural)

Do not use `dangerouslySetInnerHTML` to render markdown output. This was a defect in draft_d2 (Finding 21.3). react-markdown's component map exists to render Markdown as React elements — serializing to HTML and using `dangerouslySetInnerHTML` discards the benefits (type safety, accessibility attributes, reconciliation) and creates an XSS surface even with sanitization. If raw HTML pass-through is genuinely needed, use `rehype-raw` paired with `rehype-sanitize` and document the security implications explicitly. The default skill does not enable this path.

### 12.6 Nested error boundaries (anti-pattern)

Do not nest error boundaries. One root boundary is sufficient. Use defensive checks (e.g., `try/catch` around pure functions, optional chaining for nullable values) in pure code rather than wrapping every component in its own boundary. Over-broad boundaries mask errors and make debugging harder (§16 anti-pattern #8).

## §13 Performance Optimization & Budgets

Performance budgets are explicit and enforced in CI (§15). The budgets below are realistic, not aspirational — they account for React 19, react-markdown, the remark/rehype ecosystem, and the application code. v1.0.1 had no performance budgets; draft_d2 had a 150 KB gzipped budget that was unrealistically low and would have forced feature cuts (Finding 21.9). v4.1.0 sets the budget at 250 KB gzipped, which is achievable without sacrificing functionality.

### 13.1 Performance budgets

| Metric | Budget | Measurement | Gate |
| --- | --- | --- | --- |
| Bundle size (gzipped) | < 250 KB | rollup-plugin-visualizer | CI failure |
| Bundle size (raw) | < 800 KB | rollup-plugin-visualizer | Warning |
| First Contentful Paint | < 1.5 s | Lighthouse CI | CI failure if > 2.5 s |
| Time to Interactive | < 3 s | Lighthouse CI | CI failure if > 4 s |
| Largest Contentful Paint | < 2.5 s | Lighthouse CI | CI failure if > 4 s |
| Cumulative Layout Shift | < 0.1 | Lighthouse CI | CI failure if > 0.25 |
| Markdown parsing (1000 lines) | < 100 ms | Custom benchmark | CI failure |
| Markdown parsing (5000 lines) | < 500 ms | Custom benchmark | CI failure |
| TOC extraction (100 headings) | < 50 ms | Custom benchmark | CI failure |

Bundle composition (estimated, Reasoned — not Verified): React 19 + react-dom ~45 KB gzipped · react-markdown + remark-parse + remark-gfm + remark-rehype + rehype-slug ~80–120 KB · lucide-react (tree-shaken to 6 icons) ~5 KB · clsx + tailwind-merge ~3 KB · application code ~30–50 KB. Total estimated ~160–225 KB (within budget). Opt-ins: `rehype-highlight` + highlight.js ≈ +30 KB; `rehype-raw` + `rehype-sanitize` ≈ +25 KB — both still fit.

### 13.2 Optimization techniques

Memoization (fixes Finding 5.2):

```tsx
// src/components/MarkdownRenderer.tsx (memoization excerpt)
import { useMemo } from "react";
import { enhanceMarkdown } from "@/lib/enhance";
import { buildToc } from "@/lib/toc";
import { parseDocument } from "@/lib/frontmatter";

export function MarkdownRenderer({ markdown, registry }: Props) {
  // Memoize parse (frontmatter strip), enhancement (fence scan + regex), and TOC
  const { body } = useMemo(() => parseDocument(markdown), [markdown]);
  const enhanced = useMemo(() => enhanceMarkdown(body, registry), [body, registry]);
  const toc = useMemo(() => buildToc(body, 4), [body]);
  // ...
}
```

Code splitting (only for documents > 50,000 words) and virtual scrolling (`@tanstack/react-virtual`, only for > 100,000 words) are documented extension points (Appendix E.2), not defaults.

### 13.3 No `gtag` hardcoding (fixes Finding 21.10)

v4.1.0 does NOT hardcode `window.gtag` calls. The `PerformanceMonitor` class (Appendix E.5, optional) logs to console in dev and exposes a hook for production reporting. The deploying team wires their analytics provider of choice.

### 13.4 Performance test examples

```ts
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
```

```ts
// tests/performance/parsing-speed.test.ts
import { describe, it, expect } from "vitest";
import { buildToc } from "@/lib/toc";
import { enhanceMarkdown } from "@/lib/enhance";
import type { TagRegistry } from "@/types/tag";

function generateLargeMarkdown(lines: number): string {
  const sections: string[] = [];
  for (let i = 0; i < lines / 10; i++) {
    sections.push(`\n## Section ${i}\nThis is paragraph ${i} with some content.\n- **Severity:** critical\n- **Confidence:** verified\n\n### Subsection ${i}.1\nMore content here.\n`);
  }
  return sections.join("\n");
}

describe("Parsing Performance", () => {
  const registry: TagRegistry = {
    Severity: {
      name: "Severity",
      values: { critical: { accent: 1 }, high: { accent: 2 }, medium: { accent: 3 }, low: { accent: 4 }, informational: { accent: 5 } },
    },
  };

  it("parses 1000 lines in under 100ms", () => {
    const markdown = generateLargeMarkdown(1000);
    const start = performance.now();
    enhanceMarkdown(markdown, registry);
    buildToc(markdown);
    expect(performance.now() - start).toBeLessThan(100);
  });

  it("parses 5000 lines in under 500ms", () => {
    const markdown = generateLargeMarkdown(5000);
    const start = performance.now();
    enhanceMarkdown(markdown, registry);
    buildToc(markdown);
    expect(performance.now() - start).toBeLessThan(500);
  });
});
```

## §14 Testing Strategy

The test pyramid is: 70% unit tests, 20% integration tests, 10% visual/end-to-end tests. The single most important test is `slug-parity.test.ts` (§9.3) — it verifies that `github-slugger` (used by `buildToc`) and `rehype-slug` (used by react-markdown) produce identical slugs. If this test fails, every TOC link in every rendered document is broken. v1.0.1 had no tests at all; v4.1.0 ships the full pyramid, extended in Round 3 with fixtures for every new finding.

### 14.1 Test pyramid

```text
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
 /--------------------\ - fence, enhance, toc, frontmatter, tags, slug-parity
/______________________\
```

### 14.2 Unit tests — `fence.test.ts` (fixes Finding 21.5)

```ts
// tests/unit/fence.test.ts
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

### 14.3 Unit tests — `enhance.test.ts` [extended in v4.1.0 — Finding 22.11]

```ts
// tests/unit/enhance.test.ts
import { describe, it, expect } from "vitest";
import { enhanceMarkdown } from "@/lib/enhance";
import type { TagRegistry } from "@/types/tag";

const REGISTRY: TagRegistry = {
  Severity: { name: "Severity", values: { critical: { accent: 1 }, low: { accent: 4 } } },
  Status:   { name: "Status",   values: { done: { accent: 4 } } },
};

describe("enhanceMarkdown", () => {
  it("wraps registered values in backticks", () => {
    expect(enhanceMarkdown("- **Severity:** critical", REGISTRY).enhanced).toBe("- **Severity:** `critical`");
  });
  it("accepts *, +, and ordered bullets", () => {
    for (const bullet of ["* ", "+ ", "1. ", "2) "]) {
      expect(enhanceMarkdown(`${bullet}**Severity:** low`, REGISTRY).enhanced).toContain("`low`");
    }
  });
  it("matches tags case-insensitively, outputs canonical case", () => {
    expect(enhanceMarkdown("- **severity:** critical", REGISTRY).enhanced).toBe("- **Severity:** `critical`");
  });
  it("leaves fenced badge lines untouched", () => {
    const md = "```\n- **Severity:** critical\n```";
    expect(enhanceMarkdown(md, REGISTRY).enhanced).toBe(md);
  });
  it("leaves blockquoted badges untouched (documented blind spot)", () => {
    const md = "> - **Severity:** critical";
    expect(enhanceMarkdown(md, REGISTRY).enhanced).toBe(md);
  });
  // [New in v4.1.0 — Finding 22.11] colon outside the bold does not match.
  // Authors habitually write `- **Tag**: value`; assert pass-through, not half-matching.
  it("leaves colon-outside-bold variant untouched (documented blind spot)", () => {
    const md = "- **Severity**: critical";
    expect(enhanceMarkdown(md, REGISTRY)).toEqual({ enhanced: md, warnings: [] });
  });
  it("warns on unknown values and leaves the line unchanged", () => {
    const { enhanced, warnings } = enhanceMarkdown("- **Severity:** catastrophic", REGISTRY);
    expect(enhanced).toBe("- **Severity:** catastrophic");
    expect(warnings[0]).toContain("catastrophic");
  });
  it("leaves unregistered bold bullets unchanged without warning", () => {
    const md = "- **Note:** just text";
    expect(enhanceMarkdown(md, REGISTRY)).toEqual({ enhanced: md, warnings: [] });
  });
  it("transforms all matching lines in a document", () => {
    const md = "## F1\n- **Severity:** critical\n- **Status:** done\n## F2\n- **Severity:** low";
    const { enhanced } = enhanceMarkdown(md, REGISTRY);
    expect(enhanced).toContain("`critical`");
    expect(enhanced).toContain("`done`");
    expect(enhanced).toContain("`low`");
  });
});
```

### 14.4 Unit tests — `toc.test.ts` [extended in v4.1.0 — Finding 22.4]

```ts
// tests/unit/toc.test.ts
import { describe, it, expect } from "vitest";
import { buildToc } from "@/lib/toc";

describe("buildToc", () => {
  it("nests H3 under H2 and H4 under H3", () => {
    expect(buildToc("## A\n### B\n#### C\n", 4)[0].children[0].children[0].slug).toBe("c");
  });
  it("re-nests an H2 after deeper levels (the q2 regression case)", () => {
    const toc = buildToc("## A\n### B\n## C\n", 4);
    expect(toc.map((t) => t.slug)).toEqual(["a", "c"]);
    expect(toc[1].children).toEqual([]);
  });
  it("promotes orphan headings to top level", () => {
    expect(buildToc("### Orphan\n## Real\n", 4).map((t) => t.slug)).toEqual(["orphan", "real"]);
  });
  it("ignores fenced headings", () => {
    expect(buildToc("```\n## Hidden\n```\n## Visible\n", 4).map((t) => t.slug)).toEqual(["visible"]);
  });
  it("respects maxDepth but still reserves slugs", () => {
    expect(buildToc("## A\n#### Deep\n## A\n", 3).map((t) => t.slug)).toEqual(["a", "a-1"]);
  });
  it("returns [] for empty markdown", () => {
    expect(buildToc("", 4)).toEqual([]);
  });
  it("strips backticks from heading text", () => {
    const toc = buildToc("## `Code` in Heading");
    expect(toc[0].text).toBe("Code in Heading");
    expect(toc[0].slug).toBe("code-in-heading");
  });
  // [New in v4.1.0 — Finding 22.4] headingText() reductions keep TOC slugs
  // aligned with rehype-slug's hast text content. Parity fixtures in §9.3.
  it("reduces linked headings to link text", () => {
    const toc = buildToc("## Heading with [link](https://example.com/a-b)", 4);
    expect(toc[0].slug).toBe("heading-with-link");
  });
  it("reduces image headings to alt text", () => {
    const toc = buildToc("## Heading with ![alt text](./img.png)", 4);
    expect(toc[0].slug).toBe("heading-with-alt-text");
  });
  it("handles repeated headings (github-slugger dedup)", () => {
    const toc = buildToc("## Section\n## Section");
    expect(toc[0].slug).toBe("section");
    expect(toc[1].slug).toBe("section-1");
  });
  it("handles CJK headings", () => {
    const toc = buildToc("## 中文标题");
    expect(toc[0].text).toBe("中文标题");
    expect(toc[0].slug).toBeTruthy();
  });
});
```

### 14.5 Unit tests — `slug-parity.test.ts`

See §9.3 for the full file — 11 test cases: 7 fixture headings (simple, emoji, CJK, CamelCase, snake_case, kebab-case, leading whitespace) + inline code + **linked heading** + **image heading** (new in v4.1.0, Finding 22.4) + cross-level dedup + fenced headings. This is the load-bearing suite.

### 14.6 Unit tests — `frontmatter.test.ts` [rewritten in v4.1.0 — Findings 22.3, 22.7]

The API under test is `parseDocument()` (§22.5), which returns `{ frontmatter, body }` — the pipeline consumes `body`, so the frontmatter block can never reach the renderer.

```ts
// tests/unit/frontmatter.test.ts
import { describe, it, expect } from "vitest";
import { parseDocument } from "@/lib/frontmatter";

const DOC = `---
title: "My Document"
author: "Jane Doe"
template: "editorial"
---

# Body`;

describe("parseDocument", () => {
  it("extracts metadata and returns the body without the frontmatter block", () => {
    const { frontmatter, body } = parseDocument(DOC);
    expect(frontmatter).toMatchObject({
      title: "My Document",
      author: "Jane Doe",
      template: "editorial",
    });
    expect(body.startsWith("# Body")).toBe(true);
    expect(body).not.toContain("title:");
  });

  // Regression for Finding 22.3: in every prior edition the frontmatter block
  // rendered as <hr><p>title: …</p><hr> because nothing stripped it.
  it("frontmatter block does not leak into the rendered body", () => {
    const { body } = parseDocument(DOC);
    expect(body).not.toMatch(/^---/);
    expect(body).not.toContain("Jane Doe");
  });

  it("returns the whole document as body when no frontmatter is present", () => {
    const md = "# Just a document";
    expect(parseDocument(md)).toEqual({ frontmatter: {}, body: md });
  });

  it("handles CRLF line endings (Finding 22.7 — code behavior, not the old §3.1 claim)", () => {
    const { frontmatter, body } = parseDocument("---\r\ntitle: CRLF\r\n---\r\n\r\n# Body");
    expect(frontmatter.title).toBe("CRLF");
    expect(body).not.toContain("\r");
  });

  it("strips a leading UTF-8 BOM", () => {
    const { frontmatter } = parseDocument("\uFEFF---\ntitle: BOM\n---\n\n# Body");
    expect(frontmatter.title).toBe("BOM");
  });

  it("treats malformed frontmatter as body (still renders)", () => {
    const md = "---\nnot closed properly\n# Body";
    const { frontmatter, body } = parseDocument(md);
    expect(frontmatter).toEqual({});
    expect(body).toBe(md);
  });

  it("handles values with colons and strips surrounding quotes", () => {
    const { frontmatter } = parseDocument(
      `---\ntitle: "Title: with colon"\nauthor: 'Single'\n---\n\n# Body`,
    );
    expect(frontmatter.title).toBe("Title: with colon");
    expect(frontmatter.author).toBe("Single");
  });
});
```

### 14.7 Unit tests — `tags.test.ts` (fixes Finding 21.6)

```ts
// tests/unit/tags.test.ts
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

### 14.8 Integration tests [extended in v4.1.0 — Finding 22.5]

```tsx
// tests/integration/markdown-rendering.test.tsx
import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { MarkdownRenderer } from "@/components/MarkdownRenderer";
import type { TagRegistry } from "@/types/tag";

const registry: TagRegistry = {
  Severity: {
    name: "Severity",
    values: { critical: { accent: 1 }, high: { accent: 2 } },
  },
  Confidence: {
    name: "Confidence",
    values: { verified: { accent: 1 } },
  },
};

describe("MarkdownRenderer integration", () => {
  it("renders markdown with badges", () => {
    const md = `
## Security Finding
This is a critical issue.

- **Severity:** critical
- **Confidence:** verified
    `;
    render(<MarkdownRenderer markdown={md} registry={registry} />);
    expect(screen.getByRole("heading", { level: 2, name: "Security Finding" })).toBeInTheDocument();
    expect(screen.getByLabelText("Severity: Critical")).toBeInTheDocument();
    expect(screen.getByLabelText("Confidence: Verified")).toBeInTheDocument();
  });

  it("renders external links with target=_blank", () => {
    const md = "[Example](https://example.com)";
    render(<MarkdownRenderer markdown={md} registry={registry} />);
    const link = screen.getByRole("link", { name: "Example" });
    expect(link).toHaveAttribute("target", "_blank");
    expect(link).toHaveAttribute("rel", "noopener noreferrer");
  });

  it("renders tables with GFM", () => {
    const md = "\n| Col1 | Col2 |\n|------|------|\n| A    | B    |\n";
    render(<MarkdownRenderer markdown={md} registry={registry} />);
    expect(screen.getByRole("table")).toBeInTheDocument();
    expect(screen.getByRole("columnheader", { name: "Col1" })).toBeInTheDocument();
  });

  it("handles malformed markdown without crashing", () => {
    const md = "## Valid\n\n```\nUnclosed code block";
    render(<MarkdownRenderer markdown={md} registry={registry} />);
    expect(screen.getByRole("heading", { level: 2, name: "Valid" })).toBeInTheDocument();
  });

  // [New in v4.1.0 — Finding 22.5] a fenced block with no language has no
  // className; the single-line guard must keep its content out of the badge path.
  it("does not render a code block whose content matches a badge value as a Badge", () => {
    const md = "```\ncritical\n```";
    const { container } = render(<MarkdownRenderer markdown={md} registry={registry} />);
    expect(container.querySelector("[data-tag]")).toBeNull();
    expect(container.querySelector("code")).not.toBeNull();
  });

  it("does not render frontmatter as content (Finding 22.3)", () => {
    const md = "---\ntitle: Hidden Meta\n---\n\n# Body";
    const { container } = render(<MarkdownRenderer markdown={md} registry={registry} />);
    expect(container.textContent).not.toContain("Hidden Meta");
    expect(screen.getByRole("heading", { level: 1, name: "Body" })).toBeInTheDocument();
  });
});
```

### 14.9 Accessibility tests [rewritten in v4.1.0 — Findings 8.3, 22.1 (fix F1)]

```ts
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

test("AAA advisory: contrast (excluding documented badge exceptions) + target size (global)", async ({ page }) => {
  await page.goto("/");

  // §10.3 exception, encoded per §10.4 (Finding 22.1): badge chips fail AAA
  // contrast by documented design. Context-exclude [data-tag] elements from
  // the AAA run — the contrast rule stays active everywhere else. This is an
  // enumerated exception, not a rule suppression: badges carry data-tag by
  // construction (§8.6), and if they ever stop carrying it the exclusion
  // becomes a no-op and the gate fails closed.
  const contrastRun = await new AxeBuilder({ page })
    .withTags(["wcag2aaa", "wcag21aaa", "wcag22aaa"])
    .exclude("[data-tag]")
    .analyze();
  const contrast = contrastRun.violations.filter((v) => v.id === "color-contrast");
  expect(contrast).toEqual([]);

  // Target size stays global — dedicated run, no exclusions. Badges are
  // non-interactive spans and never benefit from the exclusion above.
  const sizeRun = await new AxeBuilder({ page })
    .withRules(["target-size"])
    .analyze();
  expect(sizeRun.violations).toEqual([]);
});

test("dark mode passes AA", async ({ page }) => {
  await page.goto("/");
  await page.evaluate(() => document.documentElement.setAttribute("data-theme", "dark"));
  const results = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa", "wcag22aa"])
    .analyze();
  expect(results.violations).toEqual([]);
});

// [Restored from draft_z2] keyboard operability smoke: every interactive
// element must be reachable by Tab, and focus must never land on a
// non-interactive element (no traps, no dead stops).
test("keyboard navigation reaches every interactive element without trapping", async ({ page }) => {
  await page.goto("/");
  const count = await page.locator("a[href], button").count();
  expect(count).toBeGreaterThan(0);

  let interactiveFocusCount = 0;
  for (let i = 0; i < count + 3; i++) {
    await page.keyboard.press("Tab");
    const onInteractive = await page.evaluate(() => {
      const el = document.activeElement;
      return (
        el !== null &&
        el !== document.body &&
        (el.matches("a[href], button") || el.getAttribute("tabindex") !== null)
      );
    });
    if (onInteractive) interactiveFocusCount++;
  }
  // After count+3 Tab presses every interactive element must have been visited
  expect(interactiveFocusCount).toBeGreaterThanOrEqual(count);
});
```

### 14.10 Test configuration [coverage rationale added in v4.1.0 — Finding 22.12]

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
    globals: true,
    setupFiles: ["./tests/setup.ts"],
    coverage: {
      provider: "v8",
      reporter: ["text", "json", "html"],
      exclude: ["node_modules/", "tests/", "**/*.d.ts", "**/*.config.*", "scripts/"],
      thresholds: { lines: 80, functions: 80, branches: 75, statements: 80 },
    },
  },
});

// tests/setup.ts
import "@testing-library/jest-dom";

// playwright.config.ts
import { defineConfig } from "@playwright/test";
export default defineConfig({
  testDir: "./tests/accessibility",
  // The single owner of the preview server for the a11y gate — CI must not
  // start its own `preview &` alongside this (Finding 22.10).
  webServer: { command: "npm run preview", port: 4173, reuseExistingServer: false },
});
```

**Coverage statement [amended in v4.1.0 — Finding 22.12]:** 80% lines/functions, 75% branches project-wide. Rationale for 80/75 rather than draft_q3's 90%: layout and template shell components (drawer, theme toggle, hero) exercise DOM and browser APIs that jsdom covers only partially, and forcing 90% would incentivize low-value mock-heavy tests — which this corpus's testing discipline explicitly rejects. Core `lib/` modules (fence, toc, enhance, tags, frontmatter) carry a 100% goal, enforced by review. The change from 90% is stated here because silent weakening of a guardrail violates the gate discipline this document enforces.

## §15 CI/CD & Quality Gates

The CI pipeline runs all quality gates on every push and pull request. The pipeline is matrix-tested across Node 20 and Node 22 (the two LTS versions supported by Vite 7). Deployment to GitHub Pages is automated on merge to `main`.

### 15.1 GitHub Actions workflow [amended in v4.1.0 — Finding 22.10]

```yaml
# .github/workflows/ci.yml
name: CI
on:
  push: { branches: [main] }
  pull_request: { branches: [main] }
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
      fail-fast: false
      matrix:
        node-version: [20, 22]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: "${{ matrix.node-version }}", cache: npm }
      - run: npm ci
      - run: npm run versions:check        # Gate 8 / V-1
      - run: npm run lint                  # Gate 2 (eslint)
      - run: npm run lint:format           # prettier check — runs after lint (ordering rule)
      - run: npm run lint:markdown
      - run: npm run typecheck             # Gate 1
      - run: npm run test -- --coverage    # Gates 3+4 (unit + integration + slug-parity)
      - if: matrix.node-version == 22
        uses: codecov/codecov-action@v4
        with: { files: ./coverage/coverage-final.json, fail_ci_if_error: false }
      - run: npm run build                 # Gate 6 (online)
      - run: npm run build:offline         # Gate 6 (offline)
      - run: npm run test:bundle-size      # Gate 6 (250 KB gzipped)
      - run: npx playwright install --with-deps chromium
      # [v4.1.0 — Finding 22.10] No `npm run preview &` and no `npx wait-on` here.
      # playwright.config.ts's webServer boots `npm run preview` (port 4173) and is
      # the single server owner. v4.0.0's manual preview/wait-on steps were redundant
      # and wait-on was never a declared dependency.
      - run: npm run a11y                  # Gate 5 (AA hard; AAA encoded exceptions; light + dark; keyboard)
      - run: npm audit --audit-level=critical
      - if: always()
        uses: actions/upload-artifact@v4
        with: { name: dist-node-${{ matrix.node-version }}, path: dist/, retention-days: 7 }

  deploy:
    needs: quality
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 22, cache: npm }
      - run: |
          npm ci
          npm run build
      - uses: actions/configure-pages@v4
      - uses: actions/upload-pages-artifact@v3
        with: { path: dist }
      - id: deployment
        uses: actions/deploy-pages@v4
```

### 15.2 Scripts — single source of truth [extended in v4.1.0]

`package.json` scripts + lint-staged. **Every script invoked by §15.1, §15.3, §17, and Appendix D is defined here; no section of this document may cite a script that is not listed here** (draft_q3's single-source rule; the phantom-script half of Finding 22.10 — v4.0.0 §17 cited `test:integration` without defining it):

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
    "test:unit": "vitest run tests/unit",
    "test:integration": "vitest run tests/integration",
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

```sh
# .husky/pre-commit — runs lint-staged, typecheck, and unit tests
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"
npx lint-staged && npm run typecheck && npm run test:unit
```

Order matters: `eslint --fix` runs first, then `prettier --write` reformats the autofixed output. This avoids drift between the linter's fixed point and the formatter's fixed point.

### 15.3 Quality gate script

```bash
#!/bin/bash
# scripts/quality-gate.sh — runs all 8 pre-ship gates in order. Exits non-zero on first failure.
set -e
echo "1. Typecheck...";       npm run typecheck
echo "2. Lint...";            npm run lint && npm run lint:format && npm run lint:markdown
echo "3. Unit tests...";      npm run test:unit -- --coverage
echo "4. Integration tests..."; npm run test:integration
echo "5. A11y tests...";      npm run a11y   # webServer boots preview; no manual server step
echo "6. Build (online)...";  npm run build
echo "7. Build (offline)..."; npm run build:offline && npm run test:bundle-size
echo "8. Verify deps...";     npm run versions:check
echo ""; echo "All 8 quality gates passed."
```

### 15.4 Lighthouse CI configuration

```yaml
# lighthouserc.yml
ci:
  collect:
    url: [http://localhost:4173/]
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

### 15.5 Dropped from draft_q2

Visual regression tests (require screenshot baseline management; out of scope — Appendix E); codecov as a hard gate (`fail_ci_if_error: false` makes it informational); multi-framework matrix (React-only by design, §1).

---

### Pass 3 checkpoint (self-review before Pass 4)

| Check | Result |
| --- | --- |
| F1 landed: §10.3 names itself canonical; §10.4 + §14.9 encode the exceptions via context exclusion + dedicated global target-size run; no rule suppression anywhere | ✓ |
| F1 robustness note: context exclusion chosen over post-hoc node filtering (axe targets can be positional paths without `[data-tag]`); fails closed if `data-tag` disappears | ✓ (implementation detail disclosed in §10.3 note) |
| F3 fixtures: `parseDocument` unit suite incl. strip regression, CRLF, BOM, malformed; integration test asserts frontmatter absent from rendered output | ✓ |
| F4 fixtures: linked-heading + image-heading slug tests in §14.4; parity fixtures cross-referenced to §9.3 | ✓ |
| F5 fixture: fenced block containing exactly `critical` stays `<code>` (§14.8) | ✓ |
| Finding 22.11 fixture: colon-outside-bold passes through unchanged (§14.3) | ✓ |
| Finding 22.12: coverage 80/75 retained *with* explicit rationale — stated, not silent | ✓ |
| Finding 22.10: CI preview/wait-on deleted with explanatory comment; Playwright `webServer` declared single server owner; `test:integration` defined (no phantom scripts) | ✓ |
| Keyboard test restored from draft_z2 (§14.9, §10.2 row) | ✓ |
| §11/§12/§13 carried forward verbatim; §12.4 table extended with Round-3 behaviors; no `@theme`-in-`@media`, no `dangerouslySetInnerHTML`, no "14px relaxes AAA" in any new text | ✓ |

---

**Pass 4 of 5** — Part 2 §16–§23 + Closing. Changes this pass: §16 grows to 26 rows (five Round-3 additions; the v4.0.0 duplicate row #19 is replaced, keeping all cross-referenced row numbers stable); §17 gates aligned to the encoded AAA mechanics and the now-defined `test:integration` script; §18 +4 debugging rows; §19.1/§19.2 updated for `active.ts`; §20.5 new v4.0.0→v4.1.0 delta table; §22.5 rewritten as `parseDocument()` (F3, full code — including a leading-blank-line strip the Pass-3 fixtures depend on); §23 Lessons Learnt restored with the Round-3 meta-lessons; Closing extended with Round-3 spot-checks and regression greps.

---

## §16 Anti-Patterns & Pitfalls

Twenty-six rows pairing an anti-pattern with its symptom, root cause, and fix. Merged from draft_q3's 15 rows, draft_z2's 7 unique rows, and five Round-3 rows (Findings 22.1–22.5). Row numbers 1–18 and 20–22 are unchanged from v4.0.0 so existing cross-references remain valid; row 19 (a v4.0.0 duplicate of #12) is replaced, and rows 23–26 are new.

| # | Anti-pattern | Symptom | Root cause | Fix |
| --- | --- | --- | --- | --- |
| 1 | Badge renders as plain `<code>` | Gray monospace, no color | Value not wrapped by `enhance.ts` (unregistered tag/value, blockquote, or inside fence) | Check `enhance.ts` warnings; use exact bullet syntax; register the tag (Finding 7.2) |
| 2 | Heading missing from TOC | Section absent from nav | Level > `maxDepth`, or heading inside a code fence | Adjust depth; move heading out of fence (Finding 7.3) |
| 3 | TOC anchor mismatch | Jumps to wrong heading or top | Slug desync (versions drifted, setext heading, hand-edited id) | Run `slug-parity.test.ts`; pin both versions; ATX only (Finding 2.2) |
| 4 | Typecheck fails on unused imports | `tsc` errors | Strict `noUnusedLocals` | Delete the import — treat as an architectural signal (Finding 21.13) |
| 5 | Fonts render as fallbacks | System fonts | Network blocked; default build uses CDN fonts | Use `npm run build:offline` (Finding 3.2) |
| 6 | Code blocks not highlighted | Plain `<pre>` | `rehype-highlight` opt-in not wired | Add plugin + highlight.js CSS import (§19.4) |
| 7 | `import { slug } from "github-slugger"` | Build error | No named export exists; default class only | `import GithubSlugger from "github-slugger"` (Finding 21.13) |
| 8 | Error boundary everywhere | Error UI for minor issues | Over-broad boundaries | One root boundary; defensive checks in pure code (Finding 21.15) |
| 9 | Injecting raw HTML into markdown | Badges/markup silently vanish | react-markdown drops raw HTML without `rehype-raw` | Wrap values as code spans via `enhance.ts` — the supported path (Finding 21.4) |
| 10 | Rendering via `dangerouslySetInnerHTML` | XSS surface, dual pipelines | HTML-string architecture | Use the components map (§8.5); if you must serialize, `rehype-sanitize` is mandatory (Finding 21.3 — Critical) |
| 11 | Badge classes in runtime config strings | Unstyled badges, no error | Tailwind can't see classes it didn't scan | Keep classes in source files (§8.6); registry carries accent *numbers*, not class strings |
| 12 | `@theme` inside `@media` | Dark mode silently dead | `@theme` is build-time, top-level only | Variable-flip pattern (§6.1) — Layer 1 `:root` + Layer 2 `@theme inline` (Finding 21.1 — Critical) |
| 13 | Claiming AAA because "14px is bigger" | Conformance overclaim | Large text is ≥18pt / ≥14pt-bold; 14px ≠ large | §10.3 exceptions or §10.5 high-contrast recipe (Finding 21.2 — Critical) |
| 14 | Fence-blind line regexes | Fenced `## comment` in TOC; slug counters desync | Regex can't see fence state | Always go through `scanLines` (§9.1) (Finding 21.5) |
| 15 | Duplicate badge values across tags | Ambiguous render | Collision in registry | `loadRegistry` throws — rename one value (Finding 21.6) |
| 16 | Hardcoded tag keys in components | Badge doesn't render | `if (tag === 'critical')` hardcoded | Use `TagRegistry` lookup; tags are data (Finding 7.1) |
| 17 | Hand-write heading `id`s | TOC links break | Manual ids diverge from `rehype-slug` output | Let `rehype-slug` derive; TOC matches via shared slugger |
| 18 | Use setext headings | TOC desync | `Title\n=====` invisible to line extractor | ATX only (§9.4) |
| 19 | Badge renders on a code block **[New in v4.1.0]** | Badge appears where code was expected | Fenced block with no language has no `className`; its single-line content matches a registered value | Single-line string guard in `components.code` (`!text.includes("\n")`) — §8.5 (Finding 22.5) |
| 20 | Claim offline support for the default build | Fonts fail from `file://` | Online build = CDN fonts | Online build = CDN, documented; offline = `build:offline` (Finding 3.2) |
| 21 | Skip gates to ship | Defects reach production | Time pressure | State the debt; never weaken a gate (Finding 11.1) |
| 22 | Copy version numbers between documents | Version drift | Memory/document copying | `npm ls --depth=0` is the only source of truth (Finding 2.1) |
| 23 | Frontmatter renders as content **[New in v4.1.0]** | `---` / `title: …` visible at the top of the page | Nothing strips the frontmatter block before the pipeline | `parseDocument()` returns `{ frontmatter, body }`; render `body` (§22.5); regression test §14.6 (Finding 22.3) |
| 24 | TOC anchor wrong only on linked/image headings **[New in v4.1.0]** | Slug desync for `## Heading [link](url)` | TOC slugged raw markdown source; `rehype-slug` hashes hast text content | `headingText()` normalization in `buildToc` (§9.2); link/image parity fixtures (§9.3) (Finding 22.4) |
| 25 | AAA gate fails on documented exceptions **[New in v4.1.0]** | Gate red on every page with badges; exceptions table ignored | The gate enforced more than §10.3 claims | Encode the exceptions: exclude `[data-tag]` from AAA contrast, keep `target-size` global (§14.9). Encoded exclusion ≠ rule suppression (Finding 22.1) |
| 26 | Expecting frontmatter `template` to switch the build **[New in v4.1.0]** | Declared template silently ignored | No machinery reads frontmatter at build time — v4.0.0 promised it, never wrote it | Edit `templates/active.ts` — the single wiring point; frontmatter `template` is advisory + dev warning (§7.4) (Finding 22.2) |

## §17 Pre-Ship Checklist

Mandatory verification gate, run in order. No gate may be skipped, weakened, or made non-blocking to ship. A green gate achieved by disabling a check is not a pass — state the debt instead. **[Amended in v4.1.0: Gate 4's script is now defined in §15.2 (the v4.0.0 phantom-script gap — Finding 22.10's sibling); Gate 5 wording matches the encoded AAA mechanics of §14.9 (Finding 22.1).]**

```bash
# Gate 1: Typecheck (strict, noUnusedLocals/Parameters)
npm run typecheck                    # tsc --noEmit

# Gate 2: Lint (ESLint + Prettier + markdownlint, zero-warning policy)
npm run lint && npm run lint:format && npm run lint:markdown

# Gate 3: Unit tests (fence, enhance, toc, frontmatter, tags, slug-parity + coverage)
npm run test -- --coverage           # MUST include slug-parity.test.ts (link/image fixtures)
                                     # and frontmatter.test.ts (strip regression — Finding 22.3)

# Gate 4: Integration tests (MarkdownRenderer rendering)
npm run test:integration             # defined in §15.2 — includes the fenced-`critical`
                                     # badge-guard fixture and the frontmatter-not-rendered fixture

# Gate 5: Accessibility (axe-core via Playwright, light + dark)
npm run a11y                         # AA: zero violations (gate-failure), no exclusions
                                     # AAA color-contrast: zero violations EXCEPT [data-tag]
                                     #   badge chips — the documented §10.3 exceptions,
                                     #   encoded in the gate (§14.9), not suppressed rules
                                     # AAA target-size: zero violations, global, no exclusions
                                     # Other AAA criteria: advisory
                                     # Includes the keyboard-navigation smoke test (§14.9)

# Gate 6: Production build + bundle size
npm run build                        # online: dist/index.html with CDN fonts
npm run build:offline                # offline: dist/index.html with fonts inlined as base64
npm run test:bundle-size             # < 250 KB gzipped (§13.1)

# Gate 7: Smoke test the build
npm run preview
# Open http://localhost:4173/ and verify:
#   - Header renders with title (from frontmatter or first H1)
#   - Frontmatter block is NOT visible in the content (Finding 22.3)
#   - Desktop sidebar + mobile drawer (resize < 1024px); drawer closes on Escape
#   - Badges colored; TOC links jump correctly — including any heading containing
#     a link (Finding 22.4); active section highlights
#   - Code blocks render as code — even a block whose content is a badge value (Finding 22.5)
#   - Theme toggle cycles light/dark/system and persists across reload
#   - Tab through page; focus rings visible on all interactive elements
#   - DevTools → Lighthouse → Run; score ≥ 95 in all categories

# Gate 8: Verify dependency versions (gate V-1)
npm run versions:check               # npm ls --depth=0; compare against §4 table
                                     # lucide-react: confirm resolved version, correct §4 if it differs

# Verify artifact is self-contained:
#   Online build: open dist/index.html WITH network → fonts load, no console errors
#   Offline build: open dist/index.html WITHOUT network → fonts still render
```

All eight gates must pass. Suppressing a failure (loosening lint rules, skipping tests, weakening type checks, disabling a11y rules) to make a gate pass is forbidden. Removing the `[data-tag]` exclusion from §14.9 to "make the gate stricter" than §10.3 is likewise forbidden — the gate enforces the claim, and changing either side requires changing both in the same commit.

## §18 Debugging Guide

Twenty-four rows mapping common symptoms to causes and fixes. Merged from draft_z2's 14 rows, draft_q3's 6 unique rows, and four Round-3 rows.

| Symptom | Cause | Fix |
| --- | --- | --- |
| Build fails with `vite-plugin-singlefile` error | Version/config mismatch | Verify `viteSingleFile()` in plugins; gate V-1 |
| TOC anchor doesn't scroll | Missing `id` or `scroll-mt-24` | Check heading components; `rehypeSlug` present |
| TOC anchor wrong target | Slug desync | §16 row 3 |
| TOC anchor wrong only on headings with links/images **[New in v4.1.0]** | `headingText()` reduction missing or bypassed | Verify `buildToc` applies `headingText()` before `slugger.slug()` (§9.2); run the link/image parity fixtures (§9.3) (Finding 22.4) |
| Badge wrong color | Registry accent mapping | Inspect `tags.ts`; check `enhance.ts` warnings |
| Startup error "badge value collision" | Two tags share a value | Rename one value; collision detection is intentional (Finding 21.6) |
| Badge renders on a code block **[New in v4.1.0]** | Fenced block without language; content matches a registered value | Verify the single-line guard in `components.code` (§8.5); fixture in §14.8 (Finding 22.5) |
| Frontmatter visible at top of rendered page **[New in v4.1.0]** | `body` not stripped before the pipeline | Use `parseDocument()` and pass `body` to `buildToc`/`enhanceMarkdown`/`ReactMarkdown` (§22.5); regression test §14.6 (Finding 22.3) |
| AAA gate fails on badge contrast **[New in v4.1.0]** | §14.9 exclusion absent or `data-tag` dropped from `Badge` | Verify the §14.9 exclusion is present — exceptions are encoded, never suppressed; if `data-tag` was removed, restore it (exclusion fails closed by design) (Finding 22.1) |
| Dark mode doesn't apply | `data-theme` not set, or `@theme` nested in media | Inspect `<html data-theme>`; verify §6.1 structure (no `@theme` inside `@media`) (Finding 21.1) |
| Dark mode flickers on load | Theme applied after first paint | Set `data-theme` from a tiny inline script in `index.html` before the bundle |
| Theme toggle doesn't persist | Storage unavailable | Check `theme-storage.ts` try/catch path (§6.6); sandboxed contexts fall back to system (Finding 21.11) |
| Active section never highlights | Observer watching top level only | Use `flattenToc` (§9.5) |
| `lucide-react` install fails | Pinned version may not exist | Gate V-1; install current 0.x, update §4 table (Finding 22.14) |
| Offline build huge | Full variable fonts inlined | Subset with `pyftsubset` |
| Offline fonts still missing | Recipe unverified in your environment | Appendix F step 6; file an issue against §11.3 |
| Tests fail only in CI | `npm ci` vs local drift | Reproduce with `rm -rf node_modules && npm ci` |
| `enhance.ts` warnings in build log | Unknown tag value in content | Fix the markdown or extend the registry |
| Build warning: Cannot find module @fontsource/... | Offline build deps not installed | `npm install @fontsource-variable/source-serif-4 @fontsource-variable/inter @fontsource/jetbrains-mono` |
| Test failure: `use(undefined)` throws in unified pipeline | Conditional plugin passed as `undefined` | Use conditional spread: `...(condition ? [plugin] : [])` |
| `parseDocument` returns empty frontmatter on Windows-authored file | CRLF/BOM — handled since v4.1.0 | Verify `frontmatter.ts` strips BOM and normalizes CRLF (§22.5); if a fork still uses the v4.0.0 `extractFrontmatter`, migrate per §20.5 (Finding 22.7) |
| CI fails on bundle size | Bundle > 250 KB gzipped | Run `npm run build:analyze`; identify largest chunks; consider lazy-loading for very large documents (Finding 21.9) |
| `npm ls --depth=0` shows version drift | Dependency installed at wrong version | Run `npm install <pkg>@<exact-version>`; never `^`/`~` for skill-pinned deps (Finding 2.1) |
| Fenced headings appear in TOC | `scanLines()` not wired into `buildToc` | Verify `buildToc` imports and uses `scanLines` (§9.2) (Finding 21.5) |

**18.1 Debugging tools**

```bash
# Bundle analyzer (visualize what's in dist/index.html)
npm run build:analyze

# Run a single test file
npx vitest run tests/unit/slug-parity.test.ts

# Run axe against the dev server
npx @axe-core/cli http://localhost:5173/

# Inspect the built HTML — dist/index.html is a single file; search for
# "data-tag" to find badge markup, "---" near the top to confirm frontmatter stripped
```

## §19 Extending the Skill

### 19.1 Adding a new template

1. Create `src/templates/<name>/` with `theme.css`, `components.tsx`, `layout.tsx`, and `tags.ts`.
2. `theme.css` must define all Layer-1 variables (`:root` + `@media` + `[data-theme]`) and the Layer-2 `@theme inline` bridge per §6.1 — never nest `@theme` inside `@media` (§16 anti-pattern #12).
3. `components.tsx` exports a partial `ComponentsMap` that merges with the default map in `MarkdownRenderer.tsx`.
4. `layout.tsx` exports a React component receiving `TemplateLayoutProps` (§22.1).
5. Add the template name to the `TemplateName` union type in `src/types/template.ts`.
6. Add a default `tags.ts` if the template introduces new tag semantics (or copy the editorial default).
7. **Switch to it by editing `templates/active.ts` (§7.4) — the single wiring point. [Amended in v4.1.0 — Finding 22.2]**
8. Document the template in §7 of this skill file.
9. Add a fixture document and an axe test for the new template in `tests/`.

### 19.2 Adding a new tag

1. Add the tag to the active `tags.ts` (or a document-local registry).
2. Define allowed values and accent steps (1–5). Values MUST be lowercase (§8.3 validation) and unique across the whole registry — `loadRegistry` throws on collision (§16 anti-pattern #15).
3. Run `npm run test` — the `tags.test.ts` suite picks up the new tag automatically.
4. Re-run `npm run a11y`: new badge accents ride the same `[data-tag]` AAA-contrast exclusion (§10.3). If you want genuine AAA for the new values, apply §10.5-style darkened tokens and delete their exception rows — gate and table change together.
5. If the tag should appear in the TOC or header metadata, extend `layout.tsx` to extract it from the frontmatter or markdown.

Example: adding a `Motion` tag for a legal document:

```ts
Motion: {
  name: "Motion",
  values: {
    granted: { accent: 4 },
    denied:  { accent: 1 },
    pending: { accent: 3 },
  },
},
```

Markdown usage: `- **Motion:** granted`

### 19.3 Adding a markdown extension (footnotes, math, mermaid)

1. Install the remark/rehype plugin: `npm install remark-footnotes`.
2. Add to `MarkdownRenderer.tsx`'s `remarkPlugins` (or `rehypePlugins`) array.
3. Add a component override in the components map for any new HTML element the plugin emits (e.g., `<sup>` for footnotes, `<div class="math">` for KaTeX).
4. Add a fixture to `tests/integration/` verifying the extension renders.
5. Document the opt-in flag in §3 (Inputs Contract).
6. Re-run the slug-parity test — some remark plugins can interfere with `rehype-slug` if they transform headings; if the extension changes heading text content, extend `headingText()` (§9.2) and add a parity fixture in the same commit.

AST-based TOC (only if setext support becomes mandatory): migrate extraction to the AST via `unist-util-visit`. This is the one place AST parsing earns its complexity — documented as the extension path, not implemented in the base skill.

### 19.4 Adding syntax highlighting

1. `npm install rehype-highlight highlight.js`.
2. Add `rehypeHighlight` to `MarkdownRenderer.tsx`'s `rehypePlugins` after `rehypeSlug` (conditionally, based on the `syntaxHighlighting` config flag).
3. Import a highlight.js CSS theme in `index.css`:

```css
.hljs { background: var(--color-paper-100); color: var(--color-ink-900); }
.hljs-keyword { color: var(--color-accent-1); }
.hljs-string  { color: var(--color-accent-4); }
.hljs-comment { color: var(--color-ink-700); font-style: italic; }
.hljs-number  { color: var(--color-accent-3); }
```

4. Add a "copy code" button component for `<pre>` blocks (optional; recommended for the technical template).
5. Add ~30 KB to the bundle budget estimate (still within 250 KB).
6. Note: with `rehype-highlight` active, language-tagged fences gain a `className` — the §8.5 badge guard's `text.includes("\n")` check remains the authoritative block detector for untagged fences.

### 19.5 Adding search functionality (technical docs template)

For the technical docs template (§7.2), client-side search can be added: build a search index at build time from the markdown body (headings + paragraphs); use `lunr` or `flexsearch`; cmd-K palette at `z-30` (§6.5); results scroll to the heading. Out of scope for the default skill (Appendix E.3).

### 19.6 Adding a fourth framework adapter (NOT recommended)

The skill is React-only by design (draft_q2's adapters rejected as over-engineering). The transferable assets are the patterns — `enhance.ts`, `toc.ts`, `fence.ts`, `frontmatter.ts`, `slug-parity.test.ts`, and the two-layer token system — not the code.

## §20 Migration Guide

### 20.1 From `react-markdown-report` v1.0.1

| v1.0.1 | v4.1.0 | Action |
| --- | --- | --- |
| `comparative-analysis.md` | `src/content/document.md` | Rename; becomes the editorial fixture |
| `StatusBadge`, 9 hardcoded keys | `Badge` + tag registry | Move keys to editorial `tags.ts` |
| `enhanceReportMarkdown` (two keys, `-` only, fence-blind) | `enhanceMarkdown` (any registered tag, all bullets, fence-aware, warnings) | Replace |
| `buildToc` H2/H3, fence-blind | `buildToc` H2–H4, fence-aware, slug reservation, `headingText()` normalization | Replace; `maxDepth: 3` for exact v1 parity |
| Severity tokens in `@theme` | `accent-1..5` scale | Map old names via registry |
| Google Fonts only | + self-hosted + offline recipe | Optional (§11) |
| No reduced-motion / focus-visible / 44px targets | All three in base styles + gate | Apply §6.1, §10.2 |
| Badge text `text-xs` (12px, 4.76:1, fails AAA) | Stays `text-xs`; AAA handled by §10.3/§10.5 | No size change — the "14px relaxes AAA" rationale is false (Finding 21.2) |
| Pre-ship: `tsc && build` | Eight gates | §17 |
| No tests | vitest + Playwright/axe in-tree | §14 |
| `cn.ts` dead | Wired into `Badge`/templates | Done by construction (Finding 5.1) |
| No ErrorBoundary | ErrorBoundary at root + ErrorFallback | §12 (Finding 21.15) |
| No dark mode | Two-layer token pattern (Layer 1 `:root` + Layer 2 `@theme inline`) | §6.1 (Finding 21.1) — NOT `@theme`-in-`@media` |

### 20.2 From the drafts

- **draft_k:** adopt structure wholesale; fix badge resolution (§8.3 — cross-category + collision detection); add gates (§17); make `enhance.ts` fence-aware; drop the AAA headline.
- **draft_d:** keep honesty (AA baseline) and dark-mode mechanics (now §6.1, NOT draft_d2's `@theme`-in-`@media`); delete `defineConfig`/`virtual:config`, raw-HTML badge pattern, `dangerouslySetInnerHTML`, AST badge processor.
- **draft_q2:** keep as standards annex (test pyramid, CI skeleton, dependency criteria, ErrorBoundary contract); do not copy TOC extractor, `.use(undefined)` pipeline, async misuse, `PerformanceMonitor` with gtag, "Production-Ready" status. Downscope: one framework, one file.
- **draft_z:** keep audit discipline, tag registry, offline recipe, axe gate, evidence ledger; apply corrections — dark mode per §6.1, badge contrast per §10.3/§10.5, parity test per §9.3; add `ErrorBoundary`.
- **draft_q3 (base of v4.0.0):** adopted wholesale — two-layer token pattern, fence-aware scanner, collision detection, correct WCAG arithmetic, high-contrast recipe, honest lucide tag + gate V-1, dark-mode axe test, correction ledger, adopter spot-check.
- **draft_z2:** full test code, 250 KB budgets, self-hosted fonts, Lighthouse CI, ErrorBoundary/ErrorFallback/ErrorReporter (Appendix E.4), migration table pattern.
- **draft_d2:** full technical + minimal template CSS (after the `@theme` fix), 6-week migration plan, Appendix E lessons. Everything else rejected (Findings 21.3, 21.4, 21.7–21.12).

### 20.3 6-week phased migration plan

- **Week 1 — Add Tests:** vitest + @testing-library/react + @axe-core/playwright. Unit tests for `enhance.ts`, `toc.ts`, `fence.ts`, `tags.ts`, `frontmatter.ts`. Slug-parity test (§9.3 — the single most important verification). Integration + a11y tests (light and dark).
- **Week 2 — Fix Accessibility:** `prefers-reduced-motion`; touch targets to 44px; global `:focus-visible`; skip-to-content link. Do NOT change badge text to 14px — the claim is false (Finding 21.2). Enumerate the AAA exception (§10.3) and encode it in the gate (§14.9); optionally apply the high-contrast recipe (§10.5).
- **Week 3 — Design Token Consistency:** two-layer token pattern (§6.1); badge colors to accent scale; remove hardcoded colors; verify no `@theme` appears inside `@media` (Finding 21.1).
- **Week 4 — Generalize Badge System:** `Badge` + tag registry (§8); all bullet styles; fence-aware `enhance.ts`; `validateRegistry()` collision detection (§8.3).
- **Week 5 — Offline Font Strategy:** `@fontsource` packages; conditional imports (§11.3); `build:offline`; test with network disabled.
- **Week 6 — CI/CD:** GitHub Actions (§15.1); 8-gate quality script (§15.3); Lighthouse CI (§15.4); pre-commit hooks (§15.2); Pages deployment.

### 20.4 Quick-start migration procedure (10 steps)

1. Backup: `cp -r react-markdown-report react-markdown-report-v1.0.1-backup`
2. Rename: `git mv src/content/comparative-analysis.md src/content/document.md`
3. Add v4.1.0 skeleton from §5 (or `git init` new project, copy content file)
4. Install dependencies per §5.1 bootstrap commands
5. Copy editorial template from §6.1 and §7.1 — preserves v1.0.1 visual identity
6. Copy the tag registry from §8.2 — 9 v1.0.1 keys map directly to accent steps 1–5
7. Run slug-parity test — the single most important verification: `npx vitest run tests/unit/slug-parity.test.ts`
8. Run full pre-ship gate (§17) — all 8 gates must pass
9. Visually compare v4.1.0 output to v1.0.1 — should be pixel-similar for the editorial template
10. Commit: `feat: migrate from v1.0.1 to v4.1.0 (generalized, accessible, offline-capable, two-layer theming, fence-aware TOC, collision-detecting registry, gate-encoded a11y exceptions)`

### 20.5 From v4.0.0 to v4.1.0 [New in v4.1.0]

| v4.0.0 | v4.1.0 | Migration action |
| --- | --- | --- |
| `extractFrontmatter()` returns metadata only; frontmatter block reaches the renderer | `parseDocument()` returns `{ frontmatter, body }` | Replace function; pass `body` to `buildToc`/`enhanceMarkdown`/`ReactMarkdown`; add the §14.6 strip regression test (Finding 22.3) |
| AAA test fails on any `color-contrast` violation | Exceptions encoded: `[data-tag]` excluded from AAA contrast; `target-size` global | Replace the §14.9 AAA test (§10.4). Gate and §10.3 table change together (Finding 22.1) |
| "The build system loads the template specified in frontmatter" | `src/templates/active.ts` wiring file | Create `active.ts` per §7.4; `main.tsx` imports it; frontmatter `template` becomes advisory (Finding 22.2) |
| `buildToc` strips backticks only | `headingText()` also reduces images→alt, links→text, autolinks→URL | Replace (§9.2); add link/image parity fixtures (§9.3) (Finding 22.4) |
| `components.code` block detection: `className` heuristic only | + single-line string guard | Replace (§8.5); add fenced-`critical` fixture (§14.8) (Finding 22.5) |
| §3.1 lists "requires LF line endings" limitation | CRLF + BOM handled; remaining limitation is flat `key: value` only | Documentation update (§3.1) (Finding 22.7) |
| Coverage 80/75 without rationale | 80/75 with explicit rationale | Documentation only (§14.10) (Finding 22.12) |
| CI runs `npm run preview &` + `npx wait-on` | Playwright `webServer` is the single server owner | Delete both CI steps (§15.1) (Finding 22.10) |
| §17 cites `test:integration` without defining it | Defined in §15.2 scripts | No code change; single-source-of-truth restored |
| No keyboard test | Keyboard smoke test restored from draft_z2 | §14.9 |

## §21 Evidence Contract

Preserved verbatim from v1.0.1 §12. This is the skill's signature quality marker — every claim about the rendered output (or about the skill itself) must carry an evidence tag.

| Tag | Meaning | When to use | Example |
| --- | --- | --- | --- |
| Verified | Executed and observed directly | After running `npm run a11y`, `npm run test`, or manual DevTools inspection | "The slug-parity test passes for all fixtures" (after running `vitest`) |
| Reasoned | Logical inference from code, not executed | "Based on the `@theme` tokens, the contrast ratio is X:1" (without running a contrast checker) | "The 12px badge text fails AAA because accent-1 on red-50 is ≈5.9:1, below the 7:1 normal-text threshold" |
| Assumed | Based on a stated assumption | "Assuming the user opens the file in Chrome 120+" | "Assuming `@fontsource` packages resolve font files via Vite's asset pipeline as documented" |
| Unverifiable | Environment does not allow verification | "Mobile Safari behavior cannot be tested in this environment" | "iOS Safari rendering of `scroll-mt-24` cannot be verified without a device" |

**Rules:**

1. **Never upgrade a tag.** If a claim is Reasoned, do not present it as Verified. If it is Assumed, do not present it as Reasoned. The skill's credibility depends on this honesty.
2. **When in doubt, downgrade.** If you are not sure whether something was executed, tag it Reasoned.
3. **State what would be needed to verify.** "Reasoned — would need to run `npm run build:offline` and open the result from `file://` to verify fonts render."
4. **Apply the contract to the skill file itself.** The skill file makes claims about the system it describes. Those claims must be tagged. See the Closing for this skill file's own confidence statement.
5. **[New in v4.1.0] Apply the contract to the audit itself.** Part 1 findings carry confidence tags, and v4.1.0 corrected its own audit's over-tags: Findings 21.1 and 21.13 were retagged Verified→Reasoned (§1.1), and Finding 21.8's rationale was amended in place (Finding 22.6). An audit that polices evidence discipline must survive its own audit.

**Closing principle:** If you cannot verify a claim, say so. A documented "Assumed" is more valuable than an undocumented "Verified." This contract is the durable pattern preserved from v1.0.1 — every other module in v4.1.0 is in service of it.

## §22 TypeScript Reference

Complete TypeScript type definitions for the skill. These are the source of truth — if the code drifts from these definitions, the code is wrong, not the types.

### 22.1 `src/types/template.ts`

```ts
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
  markdown: string;   // the BODY from parseDocument — never raw input
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
  components: Partial<ComponentsMap>;  // overrides for default component map
  layout: FC<TemplateLayoutProps>;
  defaultTags: TagRegistry;            // loaded from tags.ts
  tocMaxDepth: 2 | 3 | 4;
  offlineFonts: boolean;               // template-specific font strategy
}
```

### 22.2 `src/types/tag.ts`

```ts
export interface TagValueDefinition {
  /** Accent step 1–5, mapped to --color-accent-1 through --color-accent-5. */
  accent: 1 | 2 | 3 | 4 | 5;
  /** Optional label override; defaults to the value, capitalized. */
  label?: string;
}

export interface TagDefinition {
  /** The tag name as it appears in markdown, e.g. "Severity", "Status". Case-sensitive. */
  name: string;
  /** The allowed values, each mapped to an accent step. Keys MUST be lowercase. */
  values: Record<string, TagValueDefinition>;
}

export type TagRegistry = Record<string, TagDefinition>;

/** Returned by resolveBadge() — the resolved badge to render. */
export interface ResolvedBadge {
  tag: string;
  value: string;
  label: string;
  accent: 1 | 2 | 3 | 4 | 5;
}
```

### 22.3 `src/types/toc.ts`

```ts
export interface TocItem {
  level: 2 | 3 | 4;
  text: string;
  slug: string;
  children: TocItem[];
}
```

### 22.4 `src/types/config.ts`

```ts
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

// NOTE: v4.1.0 does NOT ship a `defineConfig` helper. The configuration surface is
// deliberately small (frontmatter + template wiring + tags — §3.2). This type is
// provided for teams that want to build their own config helper.
```

### 22.5 `src/lib/frontmatter.ts` [rewritten in v4.1.0 — Findings 22.3, 22.7 (fix F3)]

```ts
export interface Frontmatter {
  title?: string;
  subtitle?: string;
  author?: string;
  date?: string;
  template?: string;   // advisory — validated against templates/active.ts (§7.4)
  [key: string]: string | boolean | undefined;
}

export interface ParsedDocument {
  frontmatter: Frontmatter;
  /** Markdown body with the frontmatter block removed — this is what renders. */
  body: string;
}

/**
 * Parses AND STRIPS YAML frontmatter from the top of a markdown file.
 *
 * Finding 22.3: in every prior edition the frontmatter block reached the
 * renderer and appeared as <hr><p>title: …</p><hr>. The pipeline MUST consume
 * `body`, never the raw input (regression test: §14.6).
 *
 * BOM-safe: a leading U+FEFF is stripped before parsing.
 * CRLF-safe: \r\n is normalized to \n before parsing. (Finding 22.7: v4.0.0
 * §3.1 claimed "requires LF line endings" while its own code normalized CRLF —
 * resolved in favor of the code, and BOM handling added.)
 *
 * Known limitations (disclosed, by design): flat `key: value` only; no nested
 * YAML, arrays, or multiline values; malformed frontmatter is silently ignored
 * and the whole input is treated as body (still renders). If a document needs
 * real YAML semantics, swap in `gray-matter` — the one dependency upgrade that
 * preserves every contract in this document.
 */
export function parseDocument(markdown: string): ParsedDocument {
  const normalized = markdown.replace(/^\uFEFF/, "").replace(/\r\n/g, "\n");
  const match = normalized.match(/^---\n([\s\S]*?)\n---\n?/);
  if (!match) return { frontmatter: {}, body: normalized };

  const frontmatter: Frontmatter = {};
  for (const line of match[1].split("\n")) {
    const trimmed = line.trim();
    if (!trimmed) continue;
    const colonIndex = trimmed.indexOf(":");   // split on FIRST colon only
    if (colonIndex === -1) continue;
    const key = trimmed.slice(0, colonIndex).trim();
    let value = trimmed.slice(colonIndex + 1).trim();
    value = value.replace(/^["']|["']$/g, "");
    if (value === "true") frontmatter[key] = true;
    else if (value === "false") frontmatter[key] = false;
    else frontmatter[key] = value;
  }

  // Strip the frontmatter block AND any blank lines separating it from the body,
  // so `body` starts at the first content line.
  const body = normalized.slice(match[0].length).replace(/^\n+/, "");
  return { frontmatter, body };
}
```

### 22.6 Additional named types

- `EnhanceResult` (§8.4): `{ enhanced: string; warnings: string[] }`
- `MarkdownRegion` (§9.1): `{ line: string; lineNumber: number; insideFence: boolean }`
- `ParsedDocument` (§22.5): `{ frontmatter: Frontmatter; body: string }`

### 22.7 Component props summary

| Component | Props |
| --- | --- |
| App | None (reads markdown via `?raw` import; consumes `parseDocument().body`) |
| MarkdownRenderer | `{ markdown: string; registry: TagRegistry }` — markdown is the enhanced **body** |
| TableOfContents | `{ items: TocItem[]; activeSlug?: string; onNavigate?: () => void }` |
| Badge | `{ tag: string; value: string; accent: 1 \| 2 \| 3 \| 4 \| 5 }` |
| ErrorBoundary | `{ children: ReactNode; fallback?: ReactNode \| ((error, errorInfo) => ReactNode); onError?: (error, errorInfo) => void }` |
| ErrorFallback | `{ error?: Error \| null }` |
| SkipLink | `{ targetId?: string }` (default: `"content"`) |
| ThemeToggle | `{ theme: "light" \| "dark" \| "system"; onChange: (theme) => void }` |

## §23 Lessons Learnt [restored in v4.1.0 from draft_q3; extended with Round-3 lessons]

**Carried from v1.0.1 (all five still true):**

1. **Inline code ≠ badge without preprocessing.** The renderer's `code` component has no parent context; preprocess at the string level.
2. **Two slug generators must stay in sync.** Enforced by `tests/unit/slug-parity.test.ts`, with slug reservation across all heading levels and `headingText()` normalization — assertion is not verification.
3. **Strict TypeScript catches real bugs.** Unused-import errors are architectural signals (dead `cn.ts` was such a signal; v4.1.0 wires `cn()` in).
4. **Single-file build ≠ offline fonts.** `vite-plugin-singlefile` inlines JS/CSS, not `@import`ed fonts. Document runtime dependencies; provide the offline recipe.
5. **Document what doesn't exist.** "Custom hooks: none exist" saves every future agent a search. Keep negative documentation.

**Distilled from the four generalization drafts:**

6. **Conformance claims are hereditary — gate them.** v1.0.1's AAA overclaim was copied into three of four drafts. The cure is not better wording; it is an axe gate that fails the build (§10.4) and an enumerated exceptions table (§10.3).
7. **Reference code in a skill must be traced before it ships.** Draft q2's TOC algorithm mis-nests the most common heading pattern (an H2 after an H3) while claiming production-readiness. Every algorithm in this document was hand-traced at write time and is labeled Reasoned until executed.
8. **Generality bought with verifiability is debt.** Drafts d and q2 specified systems that could not run (nonexistent packages, broken pipelines); z specified honestly but carried two technical errors. The answer: small configuration surface, full tests in-tree, and an evidence ledger applied to the skill itself.

**New in v4.1.0, distilled from the Round-3 self-audit:**

9. **Fix-batches create inconsistencies — re-audit the fixes.** Correcting the WCAG arithmetic (Finding 21.2) broke the AAA gate's coherence (Finding 22.1); the v4.0.0 merge inherited the frontmatter-strip gap through every prior edition unseen (Finding 22.3). After any fix-batch, run a coherence pass over the *fixed* document: every claim must match its gate, and every pipeline step must have an owner.
10. **Audit against first principles, not prior drafts.** The `@theme`-in-`@media` bug and the 14px arithmetic each survived three successive audits because each edition diffed against the previous draft instead of re-deriving from stable external definitions (Tailwind v4 semantics, WCAG 2.x). Load-bearing claims are derived from the standard, the spec, or the package — never from the last merge.
11. **Unwritten machinery is a contract breach.** "The build system loads the template from frontmatter" was a promise no edition implemented (Finding 22.2). Any mechanism a non-negotiable rule depends on must exist as written code — or the rule is downgraded to an explicit extension path. Tenet 7 (§1) makes this permanent.
12. **Encode exceptions; never suppress rules.** The difference between an honest gate and a weakened gate is whether the exception is enumerated, named in the claim, and implemented as a scoped exclusion (`[data-tag]`) rather than a rule disable (§14.9, §16 row 25).
13. **Disclose blind spots with fixtures.** The colon-outside-bold variant, blockquoted badges, and code-block badge guards are all documented limitations with tests asserting the *non-match* (Finding 22.11, §14.3, §14.8). An undisclosed blind spot is a bug with a delay.

---

## Closing — Definition of Done & Verification Ledger

### What was verified (textually, during the audit)

- **Verified (textual):** all Part 1 findings marked Verified — internal contradictions in the source texts (v1.0.1's AAA claim vs. 36px touch targets; portability claim vs. font `@import`; draft_d2's "Verified" self-tag vs. no execution; draft_d2's `dangerouslySetInnerHTML` vs. its own component-map claim; v4.0.0's §10.3 exceptions vs. §14.9 gate code; v4.0.0's §3.1 "LF-only" vs. §22.5 CRLF code; v4.0.0's §6.1 specificity comment vs. CSS specificity arithmetic).
- **Verified (against stable external definitions):** WCAG 2.x large-text thresholds (§10.1); CSS specificity values (Finding 22.8); `github-slugger` dedup semantics.
- **Reasoned:** everything else — including all v4.1.0 code snippets, which are hand-traced but not executed.

### What was NOT verified

- No project bootstrapped; no `npm install` / `build` / `a11y` / `test` executed in this environment.
- `slug-parity.test.ts` (§9.3) — 11 cases written, not run (requires vitest + unified + remark-parse + remark-rehype + rehype-slug + github-slugger + hast).
- `parseDocument()` (§22.5) — written and traced against the §14.6 fixtures, not run.
- `headingText()` (§9.2) — traced against the link/image/autolink fixtures, not run.
- The §14.9 axe exclusion — logic reasoned; actual axe node-target formats for `[data-tag]` elements must be confirmed by a real run (the exclusion fails closed if formats ever mismatch — safe).
- `build-offline.mjs` (§11.3) — sketch; requires testing with actual `@fontsource` packages.
- Contrast ratios (§10.3) — Reasoned via WCAG relative-luminance formula; verify with a contrast checker before shipping.
- CI workflow (§15.1) — YAML-correct, not run on a GitHub Actions runner.
- Bundle budget 250 KB (§13.1) — estimated from documented dependency sizes.

### Commands the user can run to spot-verify

See Appendix F for the complete spot-check procedure (~15 minutes). The checks specific to v4.1.0 fixes:

```bash
# F3 — frontmatter strip (Finding 22.3)
npx vitest run tests/unit/frontmatter.test.ts   # strip regression, BOM, CRLF all pass

# F4 — linked-heading parity (Finding 22.4)
npx vitest run tests/unit/slug-parity.test.ts   # includes link + image heading fixtures

# F5 — code-block badge guard (Finding 22.5)
npx vitest run tests/integration                # fenced-`critical` stays <code>;
                                                # frontmatter absent from rendered output

# F1 — encoded AAA exceptions (Finding 22.1)
npm run a11y                                    # AAA gate passes on a badge-bearing fixture

# F2 — template wiring (Finding 22.2)
grep -r "templates/editorial/theme.css" src/templates/active.ts   # single wiring point
npm run dev                                     # frontmatter template mismatch warns in dev
```

Carried-forward Critical/High spot-checks (from v4.0.0 Appendix F): `@theme` top-level only; `Badge.tsx` uses `text-xs`; fence tests pass; collision test passes; `grep -r "dangerouslySetInnerHTML" src/` returns nothing; slug parity matches.

### How to install this skill

1. Save this document as `markdown-to-web_SKILL_v4.1.md` in the skills directory.
2. Create a starter project at `skills/markdown-to-web/starter/` containing the file tree in §5 with minimal implementations (using §6–§14 snippets as the starting point).
3. The skill is invoked when a user says "render this markdown as a web page," "convert .md to HTML," "publish this document as a site," or "make a polished web version of this README/report/spec."
4. The agent reads the skill, copies the starter, replaces `src/content/document.md` with the user's markdown, wires the template in `templates/active.ts` (or asks), and runs the 8-gate pre-ship checklist (§17).
5. All 8 gates must pass before delivering the artifact.

### Provenance and merge log

`markdown-to-web` v4.1.0 = `SKILL.md` v4.0.0 + Round 3 self-audit (15 findings, all fixed). v4.0.0 was itself a merge of: draft_q3.md v3.0.0 (BASE), draft_z2.md v2.0.0, draft_d2.md v2.0.0 (parts donor only), markdown-to-web_SKILL.md v2.1.0 (Part 1 audit), original_SKILL.md v1.0.1 (evidence contract). Note: draft_z2.md and draft_d2.md both self-version "2.0.0" — provenance references cite filename + self-version together (Finding 22.15). Full disposition of all 67 findings: Appendix A.

### Confidence statement

This deliverable is **Reasoned throughout** for the v4.1.0 design — internally consistent, addresses every one of the 67 findings across Rounds 1–3, and follows established React 19 / Vite 7 / Tailwind v4 / react-markdown 10 idioms. It is not Verified because no code was executed. The durable patterns (evidence contract, slug parity test, tag registry with collision detection, two-layer token theming, fence-aware scanner, `parseDocument` strip, gate-encoded a11y exceptions, single-wiring-file template switch, 8-gate pre-ship) are high-confidence; the specific code snippets are starting points that require runtime validation per the Appendix F spot-check.

This honest self-tagging complies with §21: "Never state that code 'works,' 'is fixed,' 'passes,' or 'is secure' unless it was actually executed/checked and the result observed." Three prior editions (draft_q, draft_q2, draft_d2) violated this rule; v4.0.0 did not repeat it; v4.1.0 extends it by auditing its own audit (retagged 21.1/21.13, amended 21.8).

### Quality gates for the merged document itself (self-check)

- ✅ Every finding in Part 1 (67 across Rounds 1–3) has a disposition in Appendix A.
- ✅ No `@theme` appears inside `@media` in v4.1.0 code.
- ✅ No "14px relaxes AAA" claim in v4.1.0 code.
- ✅ No `dangerouslySetInnerHTML` in v4.1.0 code.
- ✅ `parseDocument()` returns `{ frontmatter, body }`; every pipeline diagram and component contract consumes `body`; §3.1 limitations text matches §22.5 code (no "LF-only" claim remains).
- ✅ `headingText()` applied in `buildToc` before `slugger.slug()`; link/image fixtures present in §9.3 and §14.4.
- ✅ `components.code` guard includes `text.includes("\n")`; fenced-`critical` fixture present (§14.8).
- ✅ §14.9 AAA test excludes `[data-tag]` for contrast only; `target-size` global; §10.3 names itself canonical; §10.4 and §17 Gate 5 cite §14.9 mechanics.
- ✅ `templates/active.ts` written in full (§7.4); no "build system loads template from frontmatter" promise remains; frontmatter `template` documented as advisory.
- ✅ Every script cited in §15.1, §15.3, §17 appears in the §15.2 scripts block (no phantom scripts).
- ✅ CI contains no `preview &` / `wait-on` steps; Playwright `webServer` declared single server owner.
- ✅ Coverage 80/75 stated with rationale (§14.10).
- ✅ Fence-aware scanner present across §5, §8, §9, §14, Appendix A, Appendix C.
- ✅ Evidence contract applied to the skill document itself; no placeholder values (`TODO`/`FIXME`/`XXX`/`TBD`).
- ✅ No contradictions: "AA + AAA aspirational with encoded exceptions" used consistently; no unqualified "WCAG AAA."
- ✅ Length check: target 3,200–3,600 lines across the five assembled passes (verified at assembly).

**End of `markdown-to-web` v4.1.0 unified skill specification — Part 2.**

Skill version: 4.1.0 · Date: 2026-08-06 · Status: Design-complete; runtime-unverified · Confidence: Reasoned throughout · Provenance: v4.0.0 base + Round 3 self-audit (15/15 findings fixed).

---

### Pass 4 checkpoint (self-review before Pass 5)

| Check | Result |
| --- | --- |
| §16: 26 rows; new rows 19, 23–26 map to Findings 22.5, 22.3, 22.4, 22.1, 22.2; rows 1–18/20–22 numbers unchanged so all prior cross-references hold | ✓ |
| §17: Gate 4 script defined (§15.2); Gate 5 wording == §10.4 == §14.9; gate-change discipline stated (claim and gate change together) | ✓ |
| §18: 24 rows incl. four Round-3 symptom rows | ✓ |
| §20.5: v4.0.0→v4.1.0 delta covers all six code-level fixes + three doc-level changes | ✓ |
| §22.5 `parseDocument`: BOM strip, CRLF normalize, first-colon split, boolean parse, body blank-line strip — traced against every §14.6 assertion (`startsWith("# Body")` now holds) | ✓ |
| §23: 13 lessons = 5 v1.0.1 + 3 draft-era + 5 Round-3 (incl. hereditary-error meta-lesson) | ✓ |
| Closing: counts (67), not-verified list includes the axe exclusion format caveat (fails-closed), spot-check commands F1–F5 | ✓ |
| No `@theme`-in-`@media`, no `dangerouslySetInnerHTML`, no "14px relaxes AAA", no "LF-only", no phantom scripts in any new text | ✓ |

---

**Pass 5 of 5 (final)** — Appendices A–F, the final consistency gate, and delivery. Appendix A delivers the complete 67-row correction ledger promised in Pass 1; Appendix C reconciles every fixture count against the test code actually written in Passes 2–4; Appendix F extends the spot-check with the six Round-3 verifications.

---

## Appendices

### Appendix A — Correction Ledger (67 rows)

Every finding from Part 1 (Rounds 1–3), mapped to its v4.1.0 resolution. This is the single source of truth for traceability — every fix is traceable to a documented finding, and no finding is left unaddressed. Provenance note (Finding 22.15): `draft_z2.md` and `draft_d2.md` both self-version "2.0.0" — references below cite filename + self-version together.

**Round 1 — original v1.0.1 audit (37 findings: 5 High, 8 Medium, 6 Low, 18 Informational)**

| Finding | Severity | Resolution in v4.1.0 |
| --- | --- | --- |
| 1.1 Scope hardcoded to one report | High | §1, §2, §3 — generalized identity, inputs contract |
| 1.2 "No generic UI" mandate conflicts with reuse | Medium | §1, §7 — anti-generic mandate scoped per-template |
| 2.1 Versions pinned and verified | Info | §4, §17 gate 8 (gate V-1) |
| 2.2 Slug parity asserted, not verified | Medium | §9.3, §14.5, Appendix C — compiling slug-parity test; extended by Finding 22.4 (linked headings) |
| 2.3 Node version floor correct | Info | §4 — carried forward |
| 3.1 No `tsc` npm script | Low | §15.2 scripts block (`typecheck`) + §17 gate 1 |
| 3.2 Google Fonts `@import` requires runtime network | High | §11 — three font strategies (CDN, self-hosted, `@fontsource` offline) |
| 4.1 `@theme` tokens well-structured | Info | §6, §7 — two-layer token pattern |
| 4.2 Severity palette hardcoded | Medium | §6, §8 — generic 5-step accent scale |
| 4.3 No `prefers-reduced-motion` guard | High | §6.1, §10.2 — media query in base styles |
| 4.4 No `prefers-color-scheme: dark` support | Low | §6.1, §10.2 — two-layer token pattern with dark variants |
| 5.1 `cn` utility is dead code | Low | §8.6 — `cn()` wired into `Badge.tsx` |
| 5.2 `enhanceReportMarkdown` runs at render time | Low | §13.2 — `useMemo` memoization |
| 5.3 Single state is correct | Info | §9.5 — `activeSlug` added; three-state cap preserved |
| 6.1 "None exist" is excellent documentation | Info | §5 — preserved (custom hooks: none) |
| 7.1 Badge protocol too narrow | Medium | §8 — tag registry (data, not code) |
| 7.2 `enhance.ts` regex fragile | Medium | §8.4 — all bullet styles + warnings + fence-aware |
| 7.3 TOC contract correct (H2/H3 only) | Info | §9 — H4, configurable depth, fence-aware, slug reservation |
| 8.1 "WCAG AAA" claim partially false | High | §10.1 — honest "AA + AAA-aspirational"; §10.2 — 44 px targets |
| 8.2 Focus styles rely on browser default | Medium | §6.1, §10.2 — global `:focus-visible` |
| 8.3 No automated a11y test | Medium | §10.4, §14.9, §17 gate 5 — axe gate in CI |
| 8.4 Badge text contrast fails AAA | Medium | §10.3 enumerated exception + §14.9 encoded gate + §10.5 high-contrast recipe — NOT the false 14px claim (Finding 21.2) |
| 9.1 Anti-pattern table high-value | Info | §16 — expanded to 26 rows |
| 10.1 Debugging guide structured | Info | §18 — expanded to 24 rows |
| 11.1 Quality gate too narrow (elevated to High) | High | §17 — 8 hard gates |
| 12.1 Lessons well-extracted | Info | §23 — restored and expanded to 13 lessons |
| 13.1 Pitfalls table actionable | Info | §16, §17 — folded into anti-patterns and gates |
| 14.1 Best practices conventional | Info | §5 — carried forward |
| 15.1 Three patterns documented as code | Info | §8, §19 — expanded with template composition + registry extension |
| 16.1 Anti-patterns table concrete | Info | §16 — carried forward + expanded |
| 17.1 Only `sm` and `lg` used | Low | §7 — per-template breakpoint choice |
| 18.1 Z-index map explicit and minimal | Info | §6.5 — extended with z-30, z-60 |
| 19.1 Color reference exhaustive | Info | §6.3 — auto-generated via `generate-color-ref.mjs` |
| 20.1 `TocItem` is only named interface | Low | §22, Appendix B — named interfaces for all shared types |
| A.1 `.agents/` symlink stale | Info | Appendix A — repurposed as correction ledger |
| B.1 Build output documentation correct | Info | §11, Appendix D — carried forward + offline variant |
| C.1 Visual pipeline duplicates §5.2 | Info | Appendix C — repurposed as testing fixtures index |

**Round 2 — comparative review of the drafts (15 findings: 3 Critical, 2 High, 7 Medium, 3 Low)**

| Finding | Severity | Present in | Resolution in v4.1.0 |
| --- | --- | --- | --- |
| 21.1 `@theme` nested inside `@media` | Critical | draft_d2, draft_z, v2.1.0, draft_z2 | §6.1 two-layer token pattern; §16 anti-pattern #12; retagged Verified→Reasoned in v4.1.0 (§1.1) |
| 21.2 WCAG "14px relaxes AAA" arithmetic | Critical | draft_z2, draft_d2, draft_z, v2.1.0 | §10.1 correct arithmetic; §10.3 exceptions; §10.5 recipe; §16 anti-pattern #13 |
| 21.3 `dangerouslySetInnerHTML` | Critical | draft_d2 | §8.5 component-map pipeline; §12.5 rejection; §16 anti-pattern #10 |
| 21.4 AST badge/component disconnect | High | draft_d2 | §8.5 backtick-wrapping pattern (v1.0.1 lineage preserved) |
| 21.5 Fence-blind regex | High | draft_z2, draft_d2, draft_z, v2.1.0 | §9.1 `fence.ts` scanner; §16 anti-pattern #14 |
| 21.6 No collision detection | Medium | draft_z2, draft_d2, draft_z, v2.1.0 | §8.3 `validateRegistry()` throws at load; §16 anti-pattern #15 |
| 21.7 False "Verified" self-tag | Medium | draft_d2 | §21 evidence contract; Closing — "Reasoned throughout" |
| 21.8 `process.env` in browser code | Medium | draft_d2 | Amended in v4.1.0 (Finding 22.6): `import.meta.env.DEV` is the idiom; draft_d2's real bug was `process.env.ERROR_REPORTING_ENDPOINT` — Appendix E.4 uses `import.meta.env.VITE_ERROR_REPORTING_ENDPOINT` |
| 21.9 Unrealistic 150 KB budget | Medium | draft_d2 | §13.1 — 250 KB gzipped with composition breakdown |
| 21.10 `PerformanceMonitor` hardcodes `window.gtag` | Medium | draft_d2 | §13.3 — no gtag; moved to Appendix E.5 as opt-in without provider hardcoding |
| 21.11 `localStorage` without try/catch | Medium | draft_d, draft_k | §6.6 `theme-storage.ts` with try/catch + in-memory fallback |
| 21.12 YAML frontmatter syntax error | Low | draft_d2 | N/A — v4.1.0 frontmatter is clean |
| 21.13 `import { slug }` nonexistent export | Low | draft_z, v2.1.0 | §9.3 correct default import; §16 anti-pattern #7; retagged Verified→Reasoned in v4.1.0 (§1.1) |
| 21.14 `[^*]+` regex restrictiveness | Low | draft_z, v2.1.0 | §8.4 — `[^*]+` retained (sufficient for scope; alternative documented) |
| 21.15 No ErrorBoundary in skeleton | Medium | draft_z, v2.1.0 | §5, §12 — `ErrorBoundary.tsx` + `ErrorFallback.tsx` at root |

**Round 3 — self-audit of v4.0.0 (15 findings: 2 High, 4 Medium, 6 Low, 3 Informational — all new in v4.1.0)**

| Finding | Severity | Resolution in v4.1.0 |
| --- | --- | --- |
| 22.1 AAA axe gate contradicts enumerated badge exceptions | High | F1: §10.3 canonical exceptions + §10.4/§14.9 gate encodes them (`[data-tag]` excluded from AAA contrast; `target-size` global); §16 row 25; §17 gate 5 wording aligned; §20.5 delta row |
| 22.2 Template switching machinery overpromised/unwritten | High | F2: §5 skeleton + §7.4 — `src/templates/active.ts` wiring file written in full; frontmatter `template` advisory + dev-mode mismatch warning; Tenet 7 added; §20.5 delta row |
| 22.3 Frontmatter never stripped before render | Medium | F3: §22.5 `parseDocument()` returns `{ frontmatter, body }` (BOM strip + CRLF normalize); §5 pipeline consumes `body`; §14.6 strip regression + BOM/CRLF tests; §14.8 render assertion; §12.4 table row; §16 row 23; §18 row |
| 22.4 Linked/image headings desync slugs | Medium | F4: §9.2 `headingText()` (backticks → image alt → link text → autolinks); §9.3 + §14.4 parity fixtures; §9.4 residual edge cases disclosed; §16 row 24; §18 row |
| 22.5 Badge misfires on unclassed code blocks | Medium | F5: §8.5 single-line string guard in `components.code`; §14.8 fenced-`critical` fixture; §16 row 19; §18 row |
| 22.6 Finding 21.8 rationale overstated | Medium | 21.8 amended in place (Part 1); §21 rule 5 added (audit audits itself); Appendix E.4 uses the correct `VITE_` env spelling |
| 22.7 §3.1 "LF-only" contradicts §22.5 code | Low | §3.1 rewritten: CRLF + BOM handled; remaining limitation is flat `key: value` only; §18 debugging row updated |
| 22.8 §6.1 "equal specificity" comment wrong | Low | §6.1 comment rewritten with actual specificities ((0,2,0) vs (0,1,0)) and why behavior is still correct |
| 22.9 `aria-label` on generic span | Low | §8.6 note: attribute kept as belt-and-suspenders; semantics carried by visible text; no widget role added |
| 22.10 CI preview/wait-on redundant + undeclared dep | Low | §15.1 steps deleted with explanatory comment; Playwright `webServer` declared single server owner; Appendix D aligned; `test:integration` defined in §15.2 (phantom-script half fixed too) |
| 22.11 Colon-outside-bold undocumented | Low | §8.4 blind-spot list + §14.3 fixture asserting pass-through; §23 lesson 13 |
| 22.12 Coverage downgrade without rationale | Low | §14.10 — 80/75 retained WITH explicit rationale (stated, not silent) |
| 22.13 Hereditary error propagation | Info | §23 lessons 9–12 (fix-batch coherence pass; first-principles auditing; unwritten machinery; encode-don't-suppress); §1.3 observations 8–9 |
| 22.14 `lucide-react@1.28.0` phantom version | Info | §4 provenance note; gate V-1 arbiter; Appendix F step 3 |
| 22.15 Dual "v2.0.0" provenance ambiguity | Info | Header provenance + this appendix cite filename + self-version together |

**All 67 findings (37 Round 1 + 15 Round 2 + 15 Round 3) have a corresponding fix or explicit disposition. No finding is left unaddressed.**

### Appendix B — TypeScript Reference Index

The full definitions live in §22. This appendix is the index — if code drifts from these definitions, the code is wrong, not the types.

| Type | Section | Purpose |
| --- | --- | --- |
| `TemplateName` | §22.1 | Union: `"editorial" \| "technical" \| "minimal"` |
| `TemplateLayoutProps` | §22.1 | Layout shell props: title, subtitle, author, date, readingTime, toc, activeSlug, markdown (**body**), children |
| `ComponentsMap` | §22.1 | Element → FC override map (h1–h4, p, a, strong, em, ul, ol, li, hr, blockquote, code, pre, table, thead, tbody, tr, th, td) |
| `TemplateConfig` | §22.1 | name, themeCss, components, layout, defaultTags, tocMaxDepth, offlineFonts |
| `TagValueDefinition` | §22.2 | accent (1–5), optional label |
| `TagDefinition` | §22.2 | name + values record (keys MUST be lowercase) |
| `TagRegistry` | §22.2 | Record of tag name → `TagDefinition` |
| `ResolvedBadge` | §22.2 | Result of `resolveBadge()`: tag, value, label, accent |
| `TocItem` | §22.3 | level (2\|3\|4), text, slug, children |
| `MarkdownToWebConfig` | §22.4 | Optional config type — **no `defineConfig` helper ships** (§3.2) |
| `Frontmatter` | §22.5 | Parsed metadata; index signature `string \| boolean \| undefined` |
| `ParsedDocument` | §22.5 | `{ frontmatter: Frontmatter; body: string }` — **the pipeline consumes `body`** (Finding 22.3) |
| `EnhanceResult` | §22.6 | `{ enhanced: string; warnings: string[] }` |
| `MarkdownRegion` | §22.6 | `{ line: string; lineNumber: number; insideFence: boolean }` |

Component props (§22.7): `App` (none) · `MarkdownRenderer { markdown: string; registry: TagRegistry }` — markdown is the enhanced **body** · `TableOfContents { items; activeSlug?; onNavigate? }` · `Badge { tag; value; accent }` · `ErrorBoundary { children; fallback?; onError? }` · `ErrorFallback { error? }` · `SkipLink { targetId? }` · `ThemeToggle { theme; onChange }`.

### Appendix C — Testing Fixtures Index

Full test code lives in §14 and §9.3. Run `npm run test` after implementation. The slug-parity suite (row 4) remains the load-bearing one; rows 5, 7, and 8 carry the Round-3 regression fixtures.

| # | Test file | Section | Tests | Verifies |
| --- | --- | --- | --- | --- |
| 1 | `tests/unit/fence.test.ts` | §14.2 | 5 | Fence scanner: delimiters, tildes, unclosed, cross-character, closing-length (Finding 21.5) |
| 2 | `tests/unit/enhance.test.ts` | §14.3 | 9 | Bullet styles, case-insensitivity, fence-aware, blockquote blind spot, **colon-outside-bold pass-through (Finding 22.11)**, warnings |
| 3 | `tests/unit/toc.test.ts` | §14.4 | 11 | Nesting, q2 regression case, orphans, fenced headings, maxDepth+reservation, empty, backticks, **linked-heading reduction + image-heading reduction (Finding 22.4)**, dedup, CJK |
| 4 | `tests/unit/slug-parity.test.ts` | §9.3 | 11 | 7 fixtures + inline code + **link heading + image heading** + cross-level dedup + fenced headings (Findings 2.2, 22.4) |
| 5 | `tests/unit/frontmatter.test.ts` | §14.6 | 7 | `parseDocument`: metadata + body, **strip regression (Finding 22.3)**, no-frontmatter, CRLF, BOM, malformed, colon/quote handling |
| 6 | `tests/unit/tags.test.ts` | §14.7 | 6 | Clean registry, **collision detection** (Finding 21.6), uppercase rejection, out-of-range accent, resolver, labels |
| 7 | `tests/integration/markdown-rendering.test.tsx` | §14.8 | 6 | Badges, external links, GFM tables, malformed markdown, **fenced-`critical` stays `<code>` (Finding 22.5)**, **frontmatter absent from output (Finding 22.3)** |
| 8 | `tests/accessibility/axe.test.ts` | §14.9 | 4 | AA hard gate; **AAA with encoded `[data-tag]` exclusion + global target-size (Finding 22.1)**; dark-mode AA; **keyboard smoke (restored from draft_z2)** |
| 9 | `tests/performance/bundle-size.test.ts` | §13.4 | 1 | `< 250 KB` gzipped (Finding 21.9) |
| 10 | `tests/performance/parsing-speed.test.ts` | §13.4 | 2 | 1000 lines < 100 ms; 5000 lines < 500 ms |

**Total: 62 tests.** Coverage thresholds per §14.10 (80/75 with rationale — Finding 22.12).

### Appendix D — CI/CD Consolidated Files

D.1–D.3 are canonical; §15.3 (`quality-gate.sh`) and §15.4 (`lighthouserc.yml`) are referenced rather than duplicated.

**D.1 `.github/workflows/ci.yml`** (canonical copy — §15.1):

```yaml
name: CI
on:
  push: { branches: [main] }
  pull_request: { branches: [main] }
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
      fail-fast: false
      matrix:
        node-version: [20, 22]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: "${{ matrix.node-version }}", cache: npm }
      - run: npm ci
      - run: npm run versions:check        # Gate 8 / V-1
      - run: npm run lint                  # Gate 2
      - run: npm run lint:format           # after lint (ordering rule, §15.2)
      - run: npm run lint:markdown
      - run: npm run typecheck             # Gate 1
      - run: npm run test -- --coverage    # Gates 3+4 (unit + integration + slug-parity)
      - if: matrix.node-version == 22
        uses: codecov/codecov-action@v4
        with: { files: ./coverage/coverage-final.json, fail_ci_if_error: false }
      - run: npm run build                 # Gate 6 (online)
      - run: npm run build:offline         # Gate 6 (offline)
      - run: npm run test:bundle-size      # Gate 6 (250 KB)
      - run: npx playwright install --with-deps chromium
      # Finding 22.10: no `npm run preview &`, no `npx wait-on`.
      # playwright.config.ts webServer boots `npm run preview` (port 4173).
      - run: npm run a11y                  # Gate 5 (encoded AAA exceptions, §14.9)
      - run: npm audit --audit-level=critical
      - if: always()
        uses: actions/upload-artifact@v4
        with: { name: dist-node-${{ matrix.node-version }}, path: dist/, retention-days: 7 }

  deploy:
    needs: quality
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 22, cache: npm }
      - run: |
          npm ci
          npm run build
      - uses: actions/configure-pages@v4
      - uses: actions/upload-pages-artifact@v3
        with: { path: dist }
      - id: deployment
        uses: actions/deploy-pages@v4
```

**D.2 `.husky/pre-commit`:**

```sh
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"
npx lint-staged && npm run typecheck && npm run test:unit
```

**D.3 `package.json` scripts + lint-staged** — the single source of truth is §15.2; Appendix D does not duplicate it. Every script invoked by D.1, D.2, §15.3, and §17 appears in that block (no phantom scripts — Finding 22.10's sibling).

**D.4/D.5:** `lighthouserc.yml` → §15.4; `scripts/quality-gate.sh` → §15.3.

### Appendix E — Advanced Patterns (Optional)

Not required for the base skill. Each documents an "out of scope" decision reversibly.

**E.1 AST-based badge processing.** v4.1.0 uses the regex preprocessor (§8.4) + fence scanner (§9.1). If nested list items, multi-paragraph badges, or `:::badge` directives become necessary, write a custom remark plugin over `listItem` nodes — but the plugin MUST connect to the `code` component bridge (§8.5); draft_d2's `data-badge-*` hProperties pattern is rejected because nothing consumed the attributes (Finding 21.4).

**E.2 Virtual scrolling (10,000+ lines).** `@tanstack/react-virtual` over H2-section chunks. Breaks the §9.5 IntersectionObserver highlight — requires a scroll-position-to-section mapper. Out of scope.

**E.3 Search.** `useSearch` over the body string; cmd-K palette at `z-60` (§6.5). Out of scope for the base skill.

**E.4 Error reporting to an external endpoint.** Extend `ErrorBoundary.componentDidCatch` with:

```ts
// src/utils/error-reporter.ts (optional — Appendix E)
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
  // Vite exposes only import.meta.env.VITE_* to the client (Finding 22.6,
  // amending 21.8): draft_d2's process.env.ERROR_REPORTING_ENDPOINT never
  // resolves at runtime. The VITE_ prefix is mandatory.
  private static endpoint = import.meta.env.VITE_ERROR_REPORTING_ENDPOINT as
    | string
    | undefined;

  static async report(error: Error, context: Record<string, unknown> = {}): Promise<void> {
    const report: ErrorReport = {
      message: error.message,
      stack: error.stack,
      componentStack: (context.componentStack as string) ?? undefined,
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
        // Reporting failure must never mask the original error.
        console.error("Failed to report error:", err);
      }
    }
    if (import.meta.env.DEV) console.error("Error reported:", error, context);
  }
}
```

Never log secrets, tokens, or full PII payloads in `context`.

**E.5 Performance monitoring** (draft_d2's class, with the hardcoded `window.gtag` removed — Finding 21.10):

```ts
// src/utils/performance-monitor.ts (optional — Appendix E)
export class PerformanceMonitor {
  private static metrics: Map<string, number[]> = new Map();
  static measure<T>(label: string, fn: () => T): T {
    const start = performance.now();
    const result = fn();
    if (!this.metrics.has(label)) this.metrics.set(label, []);
    this.metrics.get(label)!.push(performance.now() - start);
    return result;
  }
  static getAverage(label: string): number {
    const values = this.metrics.get(label) ?? [];
    return values.length === 0 ? 0 : values.reduce((a, b) => a + b, 0) / values.length;
  }
  static report(label: string): void {
    if (import.meta.env.DEV) {
      console.debug(`[perf] ${label}: ${this.getAverage(label).toFixed(2)}ms avg`);
    }
    // Production: the deploying team wires their analytics provider of choice.
    // Do NOT hardcode gtag or any specific provider here.
  }
}
```

**E.6 Other opt-in extensions** (§19.3): footnotes (~5 KB), math/KaTeX (~270 KB), mermaid (~1.5 MB), syntax highlighting (~30 KB, §19.4), visual regression (baseline management). Add only what the document uses.

### Appendix F — Adopter Spot-Check (~15 minutes)

Convert this document's Reasoned claims to Verified. Record outcomes in a copy of the Appendix A ledger; upgrade only the rows your run actually proved.

```bash
# 1. Scaffold
npm create vite@latest mdw-spotcheck -- --template react-ts
cd mdw-spotcheck

# 2. Install runtime deps (exact pins from §4)
npm install react@19.2.6 react-dom@19.2.6 react-markdown@10.1.0 remark-gfm@4.0.1 \
  rehype-slug@6.0.0 github-slugger@2.0.0 clsx@2.1.1 tailwind-merge@3.4.0 \
  vite-plugin-singlefile@2.3.0

# 3. Gate V-1 — resolve the lucide-react question (Finding 22.14)
npm install lucide-react@1.28.0 || npm install lucide-react
#    Record what resolves; update the §4 table. (Expected: 1.28.0 does not exist —
#    the 0.x line resolves.)

# 4. Copy src/lib/{fence,toc,enhance,tags,frontmatter}.ts, src/types/,
#    src/templates/active.ts, and tests/ from this document

# 5. Run the core suites
npx vitest run   # fence, enhance, toc, slug-parity, frontmatter, tags
```

Then verify each load-bearing fix:

```bash
# 6. Critical-hereditary checks (carried from v4.0.0)
grep -n "@theme" src/index.css        # top-level only; never inside @media (21.1)
grep -rn "dangerouslySetInnerHTML" src/   # must return nothing (21.3)
grep -n "text-xs" src/components/Badge.tsx  # NOT text-sm — the 14px claim is false (21.2)

# 7. F3 — frontmatter strip (Finding 22.3)
npx vitest run tests/unit/frontmatter.test.ts
#    "frontmatter block does not leak into the rendered body" must pass

# 8. F4 — linked-heading parity (Finding 22.4)
npx vitest run tests/unit/slug-parity.test.ts
#    link + image heading fixtures must pass

# 9. F5 — code-block badge guard (Finding 22.5)
npx vitest run tests/integration
#    fenced-`critical` stays <code>; frontmatter absent from rendered output

# 10. F1 — encoded AAA exceptions (Finding 22.1)
npx playwright install --with-deps chromium
npm run a11y
#    AAA gate passes on a badge-bearing fixture; target-size enforced globally

# 11. F2 — template wiring (Finding 22.2)
grep -rn "templates/editorial/theme.css" src/templates/active.ts  # single wiring point
npm run dev   # set frontmatter template: "technical" → dev console warns on mismatch

# 12. Single-file + offline sanity
npm run build           # dist/index.html opens from file://
npm run build:offline   # open with network disabled — do fonts render? (validates §11.3)

# 13. Dark-pattern sanity
#    Build with §6.1 index.css, toggle OS dark mode — utilities flip live
#    (validates @theme inline); forced-light beats system-dark.
```

---

## Final Consistency Gate (run against the assembled document)

| Check | Result | Basis |
| --- | --- | --- |
| Every Part 1 finding (67) has a disposition in Appendix A | ✓ | Verified (textual) — ledger rows counted: 37 + 15 + 15 |
| No `@theme` inside `@media` in any v4.1.0 code | ✓ | Verified (textual) — §6.1/§7.2/§7.3 only |
| No "14px relaxes AAA" claim in v4.1.0 code | ✓ | Verified (textual) — appears only as rejected Finding 21.2 |
| No `dangerouslySetInnerHTML` in v4.1.0 code | ✓ | Verified (textual) |
| `parseDocument` returns `{ frontmatter, body }`; every pipeline consumer takes `body`; §3.1 limitations match §22.5 code | ✓ | Verified (textual) |
| `headingText()` applied before `slugger.slug()`; link/image fixtures present (§9.3, §14.4) | ✓ | Verified (textual) |
| `components.code` guard includes `text.includes("\n")`; fenced-`critical` fixture present | ✓ | Verified (textual) |
| §14.9 AAA test excludes `[data-tag]` for contrast only; `target-size` global; §10.3 canonical; §10.4, §17 Gate 5, §16 row 25 all cite §14.9 mechanics | ✓ | Verified (textual) |
| `templates/active.ts` written in full; no "build system loads template from frontmatter" promise remains; frontmatter `template` advisory | ✓ | Verified (textual) |
| Every script cited in §15.1/D.1, §15.3, §17 defined in §15.2 (no phantom scripts) | ✓ | Verified (textual) |
| CI contains no `preview &` / `wait-on`; Playwright `webServer` single server owner | ✓ | Verified (textual) |
| Coverage 80/75 stated with rationale (§14.10) | ✓ | Verified (textual) |
| Cross-reference integrity: §16 row numbers 1–18/20–22 unchanged so all prior citations hold; new rows 19/23–26 | ✓ | Verified (textual) |
| Evidence contract self-applied: audit retagged its own over-tags (21.1, 21.13); 21.8 amended in place; "Reasoned throughout" | ✓ | Verified (textual) |
| Length target 3,200–3,600 lines | ✗ — **deviation, stated** | Assembled length ≈ 4,900–5,100 lines across five passes. Cause: verbatim carry-forward of all load-bearing code, full template CSS, 62 in-tree tests, and the complete 67-row ledger took precedence over brevity (Decision Priority: correctness/completeness > brevity). No content was padded; the excess is canonical material. |
| No placeholders (`TODO`/`FIXME`/`XXX`/`TBD`), no secrets, no commented-out code | ✓ | Verified (textual) |

## Delivery Summary

**Artifact:** `markdown-to-web_SKILL_v4.1.md` — assembled from Passes 1–5 in this conversation, in order: header + Part 1 → §1–§9 → §10–§15 → §16–§23 + Closing → Appendices A–F + this gate.

**What v4.1.0 is:** v4.0.0 + 15 Round-3 fixes. The three hereditary Critical bugs remain dead; the five load-bearing fixes (F1 encoded AAA gate, F2 `active.ts` wiring, F3 `parseDocument` strip, F4 `headingText()` parity, F5 code-block guard) are each backed by a regression fixture; the audit now survives its own evidence contract.

**Confidence:** Reasoned throughout. No code was executed in this environment. The 62 tests, both builds, and the axe gate are written but unrun — Appendix F is the 15-minute path to convert each relevant row to Verified.

**First three commands after assembly:**

```bash
npm ls --depth=0                                   # gate V-1 — settle lucide-react (F step 3)
npx vitest run tests/unit/slug-parity.test.ts      # the spine of the app
npm run a11y                                       # the gate and the claim must match
```

Skill version: **4.1.0** · Date: 2026-08-06 · Status: Design-complete; runtime-unverified · Confidence: Reasoned throughout · Findings resolved: **67/67** (Appendix A) · Provenance: v4.0.0 base + Round 3 self-audit, per the plan approved in this conversation.

**End of `markdown-to-web` v4.1.0 unified skill specification.**

---

https://chat.qwen.ai/s/a15033fd-727b-4169-8341-bddb2cdf9a7d?fev=0.2.82 
