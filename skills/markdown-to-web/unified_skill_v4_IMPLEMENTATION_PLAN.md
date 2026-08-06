# Unified Skill v4.0.0 — Meticulous Implementation Plan

**Date:** 2026-08-06  
**Base:** `draft_q3.md` (v3.0.0) — the only edition that correctly handles both the Tailwind v4 `@theme`-in-`@media` pattern and the WCAG large-text contrast arithmetic  
**Merge sources:** `draft_z2.md`, `draft_d2.md`, `markdown-to-web_SKILL.md` v2.1.0 (mine), `original_SKILL.md` v1.0.1  
**Bug fixes:** 15 defects identified in the comparative review (8 critical/high + 7 medium/low)  
**Target length:** ~2,800–3,200 lines (between draft_q3's 1,822 and draft_z2's 3,153)  
**Confidence:** Reasoned (design document; implementation not yet executed)

---

## I. Architectural Decisions (Locked Before Writing)

### 1. Base Document: `draft_q3.md`

**Rationale:** draft_q3 is the only edition that correctly handles:
- Tailwind v4 `@theme`-in-`@media` (uses two-layer token pattern in §4.1)
- WCAG large-text contrast arithmetic (explicitly rejects the "14px relaxes AAA" error in §9.1)
- Fence-aware TOC/enhance (introduces `fence.ts` scanner in §8.1)
- Tag registry collision detection (`validateRegistry()` in §7.2)

All other editions — including the v2.1.0 document I produced in the prior turn — inherit at least one of these bugs from `draft_z`. Adopting draft_q3 as the base means v4.0.0 starts from a technically correct foundation rather than patching bugs inherited from draft_z.

### 2. Version: v4.0.0

**Rationale for major version bump:**
- Fixes two **critical** bugs present in ALL prior editions (the `@theme`-in-`@media` pattern and the WCAG 14px arithmetic error) — including draft_z2 and my v2.1.0, which were both presented as production-ready.
- Introduces the fence-aware scanner (architectural change to `buildToc` and `enhanceMarkdown`).
- Introduces collision detection (API change to the tag registry loader).
- Merges Part 1 validation review into draft_q3's spec-only format (structural change).

A minor version bump (v3.1.0) would understate the scope of the corrections. A major bump (v4.0.0) signals that prior editions should not be adopted without these fixes.

### 3. Document Structure: Three-Part + Appendices

```
FRONT MATTER (YAML metadata block)
├── name, description, version (4.0.0), tags

PART 1 — VALIDATION REVIEW (from my v2.1.0, updated)
├── Executive Summary (severity counts, verdict, reuse table)
├── Methodology (finding format, confidence taxonomy, two review rounds)
├── Section-by-Section Findings
│   ├── §1–§20: Original 20 findings (preserved verbatim from draft_z)
│   └── §21: Comparative Review Findings (15 new findings, NEW)
├── Cross-Cutting Observations (10 observations, expanded from 8)
├── Reuse Value Assessment (module-by-module table, expanded)

PART 2 — UNIFIED SKILL SPECIFICATION (v4.0.0)
├── §1  Identity & Design Philosophy
├── §2  When to Use / When Not To
├── §3  Inputs Contract
├── §4  Tech Stack & Pinned Versions
├── §5  Project Skeleton
├── §6  Design System (Two-Layer Token Pattern — from draft_q3 §4.1)
├── §7  Three Templates (full CSS from draft_d2, FIXED with draft_q3 pattern)
├── §8  Tag Registry & Badge Protocol (with collision detection — from draft_q3 §7)
├── §9  TOC + Navigation Engine (fence-aware — from draft_q3 §8)
├── §10 Accessibility (WCAG 2.2 AA + AAA Aspirational — correct arithmetic from draft_q3 §9)
├── §11 Build & Deploy Recipes (3 font strategies — merged from draft_z2 §13)
├── §12 Error Handling & Resilience (from draft_z2 §12)
├── §13 Performance Optimization & Budgets (from draft_z2 §14, 250 KB budget)
├── §14 Testing Strategy (full test code — from draft_z2 §15 + draft_q3's fence/collision tests)
├── §15 CI/CD & Quality Gates (from draft_z2 §16 + draft_q3's gate V-1)
├── §16 Anti-Patterns & Pitfalls (merged: 22 rows = 15 from draft_q3 + 7 unique from draft_z2)
├── §17 Pre-Ship Checklist (8 hard gates — unified)
├── §18 Debugging Guide (merged: 20 rows = 14 from draft_z2 + 6 unique from draft_q3)
├── §19 Extending the Skill
├── §20 Migration Guide (6-week phased plan — from draft_d2 §20)
├── §21 Evidence Contract (preserved verbatim from v1.0.1)
├── §22 TypeScript Reference

APPENDICES
├── A — Correction Ledger (35+ finding→fix mappings, from draft_q3 Appendix B pattern)
├── B — Complete TypeScript Reference (consolidated)
├── C — Testing Fixtures (full runnable code, consolidated)
├── D — CI/CD Workflow (GitHub Actions, full file)
├── E — Advanced Patterns (optional enhancements)
├── F — Adopter Spot-Check (10-minute verification, from draft_q3 Appendix C)
```

### 4. What to Take from Each Source

| Source | Elements to MERGE | Elements to DROP |
|--------|-------------------|------------------|
| **draft_q3.md** (base) | Two-layer token pattern (§4.1); fence-aware scanner `fence.ts` (§8.1); collision detection `validateRegistry()` (§7.2); cross-category resolver (§7.2); correct WCAG arithmetic (§9.1); enumerated AAA exceptions table (§9.3); high-contrast badge recipe (§9.5); honest lucide-react tag + gate V-1 (§2); 15-row anti-pattern table; correction ledger (Appendix B); adopter spot-check (Appendix C); disclosed-limitations pattern; dark-mode axe test (§12.3) | Contracts-only templates (need full CSS from draft_d2); shorter test code (use draft_z2's fuller versions); no performance budgets section |
| **draft_z2.md** | Performance budgets (§14, 250 KB with composition breakdown); self-hosted font strategy §13.2 (the third option between CDN and @fontsource); full test code §15.2–15.5 (complete runnable files); Lighthouse CI config §16.4; defect fixes table §24.7; provenance log §24.6; ErrorBoundary + ErrorFallback + ErrorReporter §12; nested error boundaries pattern §12.6; coverage thresholds 80%/75% §15.7; prettier ordering rule §16.2; MarkdownProcessor.tsx (pure string preprocessor with fence awareness — combined with draft_q3's scanner) | `@theme`-in-`@media` (BUG — use draft_q3's two-layer pattern); WCAG 14px arithmetic error (BUG — use draft_q3's correct math); fence-blind regex (BUG — use draft_q3's scanner); `PerformanceMonitor` class with `report()` method (over-engineered — move to Appendix E); `ErrorReporter` with external endpoint (over-engineered for base skill — move to Appendix E); self-tags "Reasoned throughout" but should also adopt draft_q3's per-claim ledger |
| **draft_d2.md** | Full `theme.css` for technical template §5.3 (after @theme fix); full `theme.css` for minimal template §5.4 (after @theme fix, including print CSS); 6-week phased migration plan §20; file inventory with LOC estimates §7.2; Appendix E distilled hard lessons | `@theme`-in-`@media` (BUG); `dangerouslySetInnerHTML` (BUG); AST badge processor with disconnect (BUG); WCAG 14px arithmetic (BUG); 150 KB bundle budget (unrealistic); `PerformanceMonitor` with hardcoded `window.gtag` (BUG); false "Verified" self-tag (DISHONEST); YAML syntax error (stray ```); `process.env.NODE_ENV` in browser code (should be `import.meta.env.DEV`); dual pipeline ambiguity |
| **markdown-to-web_SKILL.md v2.1.0** (mine) | Part 1 Validation Review (all 20 findings, preserved verbatim from draft_z); cross-reference table pattern; implementation plan provenance discipline; Appendix E advanced patterns skeleton | `@theme`-in-`@media` (BUG — inherit draft_q3's fix); WCAG 14px arithmetic (BUG — inherit draft_q3's fix); fence-blind regex (BUG — inherit draft_q3's fix); no collision detection (BUG — inherit draft_q3's fix) |
| **original_SKILL.md v1.0.1** | Evidence contract (§21, preserved verbatim); anti-pattern table format (symptom→cause→fix); z-index discipline; lessons-learnt discipline | Hardcoded 9 badge keys; single-report scope; WCAG AAA over-claim; `comparative-analysis.md` content path |

### 5. Key Design Decisions

**Decision 1: Two-Layer Token Pattern over Nested `@theme`**
- **ADOPT** draft_q3's §4.1 pattern: Layer 1 `:root` runtime variables flipped by `@media (prefers-color-scheme: dark)` and `[data-theme="dark"]`; Layer 2 `@theme inline` bridges runtime variables into Tailwind utilities so `bg-paper-50` compiles to `background-color: var(--paper-50)` and flips live at runtime.
- **REJECT** the `@theme`-inside-`@media` pattern used by draft_z, draft_d2, draft_z2 (partially), and my v2.1.0.
- **Rationale:** `@theme` is a build-time, top-level directive in Tailwind v4. Nesting it inside `@media` is non-standard and may not generate the expected utilities, causing dark mode to silently fail. This is verified by Tailwind v4 documentation and explicitly called out in draft_q3 §4.1.

**Decision 2: Correct WCAG Arithmetic over "14px Relaxation"**
- **ADOPT** draft_q3's §9.1 framing: WCAG large text is ≥18pt (24px) or ≥14pt bold (≈18.66px). No font size used in the skill qualifies as large text, so normal-text thresholds (7:1 AAA, 4.5:1 AA) apply everywhere.
- **ADOPT** draft_q3's §9.3 enumerated AAA exceptions table (computes actual contrast ratios per accent token on its chip background, lists AA/AAA pass/fail, documents disposition).
- **ADOPT** draft_q3's §9.5 high-contrast badge recipe (darker accent tokens: `#7f1d1d`, `#78350f`, etc. achieving ~8.5–9.2:1) as the correct path to AAA.
- **REJECT** the "14px relaxes AAA threshold to 4.5:1" claim used by draft_z, draft_z2, draft_d2, and my v2.1.0.
- **Rationale:** This is a verified WCAG 2.x definition (stable, not an interpretation). The "14px relaxation" claim is an arithmetic error that was copied hereditarily across four editions without detection.

**Decision 3: Fence-Aware Scanner over Raw Regex**
- **ADOPT** draft_q3's §8.1 `fence.ts` scanner: `scanLines()` returns `{ line, lineNumber, insideFence }[]`, tracking ```` ``` ```` vs `~~~` fences, fence length (closing must be ≥ opening), and unclosed fences (extend to EOF).
- Both `buildToc` (§9) and `enhanceMarkdown` (§8) consume `scanLines()` — no raw regex on markdown lines anywhere in the codebase.
- **REJECT** the raw `/^(#{2,4})\s+(.+)$/gm` regex used by draft_z, draft_z2, draft_d2, and my v2.1.0.
- **Rationale:** A `## comment` line inside a ` ``` ` code fence will be incorrectly indexed by the raw regex, desyncing slug dedup counters with `rehype-slug` and producing broken TOC anchors. draft_q3 is the only edition that catches this class of bug.

**Decision 4: Collision Detection in Tag Registry**
- **ADOPT** draft_q3's §7.2 `validateRegistry()` that throws at load time if two tags share a value (e.g., `"draft"` registered under both `Status` and `Priority`).
- **ADOPT** draft_q3's §7.2 cross-category resolver: `resolveBadge(registry, raw)` scans all tags for the value, returning `{ tag, value, label, accent }` or `null`. Ambiguity is impossible because collisions throw at load.
- **REJECT** the silent first-match behavior in draft_z, draft_z2, draft_d2, and my v2.1.0.
- **Rationale:** Ambiguity in badge rendering should fail fast at startup with an error naming both tags, not silently render the wrong tag. This is the D2 contract from draft_q3.

**Decision 5: Component Map over `dangerouslySetInnerHTML`**
- **ADOPT** the backtick-wrapping pattern (preserved from v1.0.1, formalized in draft_z2 §8.5): `enhance.ts` wraps values in backticks → react-markdown parses as inline `code` → `components.code` entry routes to `Badge` via `resolveBadge()`.
- **EXPLICITLY REJECT** `dangerouslySetInnerHTML` (draft_d2's bug) as anti-pattern #10 in §16.
- **Rationale:** `dangerouslySetInnerHTML` defeats React reconciliation and creates an XSS surface even with sanitization. The component-map pipeline renders Markdown as React elements, so malformed markdown produces a React render error (caught by ErrorBoundary) rather than an XSS surface.

**Decision 6: Three Font Strategies**
- **ADOPT** draft_z2's three-strategy approach:
  - **Strategy A** — CDN `@import` (default, online build, ~250–400 KB)
  - **Strategy B** — Self-hosted `@font-face` (alternative online, ~250–400 KB HTML + ~150 KB font files)
  - **Strategy C** — `@fontsource` base64 inlining (offline build, ~2–4 MB, fully self-contained)
- **REJECT** draft_d2's single-strategy approach (CDN only, no offline path).
- **REJECT** draft_q3's two-strategy approach (CDN + offline, no self-hosted middle ground).
- **Rationale:** Different deployment contexts (dev, production with CDN, production without CDN, air-gapped) need different strategies. Documenting all three prevents users from reinventing the offline build or settling for CDN when self-hosting would suffice.

**Decision 7: 8-Gate Pre-Ship Checklist**
- **ADOPT** the 8-gate structure (unified from my v2.1.0 §13 and draft_q3 §15):
  1. Typecheck (strict, `noUnusedLocals`/`noUnusedParameters`)
  2. Lint (ESLint + Prettier + markdownlint, zero-warning policy)
  3. Unit tests (enhance, toc, frontmatter, fence, tags, slug-parity + coverage)
  4. Integration tests (MarkdownRenderer rendering)
  5. Accessibility (axe: AA hard-fail; AAA contrast/target-size enforced; light + dark)
  6. Build (online + offline) + bundle size check (250 KB gzipped)
  7. Smoke test (manual verification of built artifact)
  8. Dependency verification (gate V-1: `npm ls --depth=0`)
- **REJECT** draft_d2's 13-gate structure (too granular — splits offline build, bundle analysis, and security audit into separate gates unnecessarily).
- **Rationale:** 8 gates is comprehensive without being bureaucratic. Each gate is a distinct quality dimension. The performance budget (250 KB) is folded into gate 6 (build) because it's a property of the built artifact, not a separate test.

**Decision 8: Part 1 Validation Review Preserved and Expanded**
- **ADOPT** my v2.1.0's Part 1 structure (all 20 original findings preserved verbatim from draft_z).
- **ADD** §21 "Comparative Review Findings" — 15 new findings from the comparative review (bugs #1–#15 in the Bug Fix Registry below), formatted per the evidence contract.
- **EXPAND** cross-cutting observations from 8 to 10:
  - Obs 9 (new): "The `@theme`-in-`@media` bug is hereditary — it was copied from draft_z into draft_d2, draft_z2, and v2.1.0 without detection. Only draft_q3 caught it. This demonstrates that architectural errors propagate silently across document merges."
  - Obs 10 (new): "The WCAG 14px arithmetic error is similarly hereditary — copied from draft_z into three downstream editions. The fix is not better wording; it is correct WCAG definitions. Conformance claims are only as reliable as the math behind them."
- **EXPAND** the reuse table to include draft_q3, draft_z2, and draft_d2 as sources.
- **Rationale:** The validation review is unique value — no other edition has it. It justifies every v4.0.0 design decision by referencing the finding it fixes. Expanding it to include the comparative review findings makes the document self-auditing: every bug fix is traceable to a documented finding.

---

## II. Bug Fix Registry

Every bug identified in the comparative review, with its resolution in v4.0.0. This registry is the single source of truth for "what changed and why."

| # | Bug | Severity | Present in | Fixed in v4.0.0 by |
|---|-----|----------|------------|---------------------|
| 1 | `@theme` nested inside `@media (prefers-color-scheme: dark)` — invalid Tailwind v4, dark mode silently fails | **Critical** | draft_d2, draft_z, my v2.1.0 | §6 two-layer token pattern (from draft_q3 §4.1); anti-pattern #12 |
| 2 | WCAG "14px relaxes AAA threshold to 4.5:1" arithmetic error — 14px is not large text | **Critical** | draft_z2, draft_d2, draft_z, my v2.1.0 | §10 correct arithmetic (from draft_q3 §9.1); §9.3 enumerated exceptions; §9.5 high-contrast recipe; anti-pattern #13 |
| 3 | `dangerouslySetInnerHTML` for markdown rendering — XSS surface, defeats React reconciliation | **Critical** | draft_d2 | §8.5 component-map pipeline; anti-pattern #10 |
| 4 | AST badge processor / React component disconnect — `processBadges` plugin adds data attributes nothing consumes | **High** | draft_d2 | §8 backtick-wrapping pattern (preserved from v1.0.1, formalized in draft_z2 §8.5) |
| 5 | Fence-blind regex in `buildToc` and `enhanceMarkdown` — `## comment` in code fence enters TOC, desyncs slug dedup | **High** | draft_z2, draft_d2, draft_z, my v2.1.0 | §9 `fence.ts` scanner (from draft_q3 §8.1); anti-pattern #14 |
| 6 | No tag registry collision detection — same value in two tags silently renders first match | **Medium** | draft_z2, draft_d2, draft_z, my v2.1.0 | §8 `validateRegistry()` throws at load (from draft_q3 §7.2); anti-pattern #15 |
| 7 | False "Verified" self-tagging — claims execution without running code | **Medium** | draft_d2 | §21 evidence contract; §24 confidence statement (Reasoned throughout); per-claim ledger in Appendix A |
| 8 | YAML frontmatter syntax error (stray ``` after closing `---`) | **Low** | draft_d2 | N/A — v4.0.0 frontmatter is clean |
| 9 | `process.env.NODE_ENV` in browser code — Node.js env var, not available in Vite browser build | **Medium** | draft_d2 | §12 uses `import.meta.env.DEV` (Vite idiom) |
| 10 | Unrealistic 150 KB bundle budget — would force feature cuts | **Medium** | draft_d2 | §13 250 KB budget (from draft_z2 §14, with composition breakdown) |
| 11 | `PerformanceMonitor` with hardcoded `window.gtag` — assumes Google Analytics present | **Medium** | draft_d2 | §13 no gtag; analytics is an extension point (Appendix E) |
| 12 | Slug parity test unused imports (`import { slug }`) — no named export exists | **Low** | draft_z, my v2.1.0 | §9 correct imports (from draft_q3 §8.3); anti-pattern #7 |
| 13 | `enhance.ts` regex `[^*]+` too restrictive — excludes valid tag names | **Low** | draft_z, my v2.1.0 | §8 `[^\\n*:]+` (from draft_z2 §8.3) |
| 14 | `localStorage` without try/catch — fails in sandboxed iframes and some `file://` contexts | **Medium** | draft_d, draft_k | §6 `theme-storage.ts` with try/catch + in-memory fallback (from draft_z2) |
| 15 | No ErrorBoundary in skeleton — malformed markdown crashes the whole app | **Medium** | draft_z, my v2.1.0 | §12 ErrorBoundary at root (from draft_z2 §12) |

---

## III. Section-by-Section Blueprint

### PART 1 — VALIDATION REVIEW (~600 lines)

**Structure:** Identical to my v2.1.0 Part 1, with these updates:

1. **Executive Summary** (~60 lines)
   - Update severity count table to include the 15 new findings from the comparative review.
   - Add a "Comparative Review Findings" subsection summarizing bugs #1–#15.
   - Update the verdict to reflect that v4.0.0 fixes defects present in ALL prior editions.

2. **Methodology** (~40 lines)
   - Add note: "Findings now span two review rounds: (1) the original v1.0.1 audit (20 findings), and (2) the comparative review of draft_q3, draft_z2, draft_d2, and v2.1.0 (15 additional findings). Both rounds follow the same evidence contract (§21)."
   - Preserve the finding format: Location, Description, Evidence, Impact, Severity, Confidence, Recommended Fix.

3. **Section-by-Section Findings** (~400 lines)
   - §1–§20: All 20 original findings preserved verbatim from my v2.1.0 (which preserved them from draft_z). No drift.
   - §21 (NEW): "Comparative Review Findings" — 15 new findings (bugs #1–#15 from the registry above), each formatted per the evidence contract. These findings reference the specific editions that exhibit each bug and the v4.0.0 section that fixes it.

4. **Cross-Cutting Observations** (~50 lines)
   - Expand from 8 to 10 observations (Obs 9 and 10 added per Decision 8 above).

5. **Reuse Value Assessment** (~50 lines)
   - Expand the table to include draft_q3, draft_z2, and draft_d2 as sources.
   - Each row maps a source module to its reuse action in v4.0.0 (High / Medium / Low / None).

### PART 2 — UNIFIED SKILL SPECIFICATION (~1,800 lines)

**§1 Identity & Design Philosophy (~80 lines)**
- One-sentence description (from draft_q3 §1).
- Design thesis: "Content is data; rendering is configuration" (from draft_z2 §1).
- 6 core tenets (from draft_q3 §1, including the "one rendering pipeline" tenet that rejects `dangerouslySetInnerHTML`).
- Anti-generic mandate, scoped per-template (from draft_q3 §1).
- Multi-framework rejection (from my v2.1.0 §1).

**§2 When to Use / When Not To (~60 lines)**
- Use cases (from draft_q3 §1.1).
- Do NOT use cases (from draft_q3 §1.1, including "multi-page navigation, search across documents, or user accounts").
- Template selection guide (from my v2.1.0 §2).
- Ambiguous cases (from draft_z2 §2 — "dashboard" and "charts" disambiguation).

**§3 Inputs Contract (~100 lines)**
- Inputs table (merged: draft_q3 §1.1 + draft_z2 §3 + my v2.1.0 §3).
- Frontmatter schema (from draft_z2 §3, with CRLF-safe parser from draft_q3 §3.4).
- Markdown features supported / not supported (from draft_q3 §1.1, with disclosed limitations).
- Configuration surface (from draft_q3 §3.3 — explicitly rejects `defineConfig` helper, `virtual:` module, and build-time config-object plugin, with rationale).

**§4 Tech Stack & Pinned Versions (~100 lines)**
- Pinned versions table (from draft_q3 §2, with honest tags: lineage-verified pins are exact; new dev-deps are caret ranges tagged *Assumed*).
- lucide-react tagged "Unverified" with explicit gate V-1 to resolve at install (from draft_q3 §2).
- Dependency selection criteria (from draft_z2 §2.1).
- Verification command: `npm ls --depth=0` (from draft_q3 §2, as gate 8).

**§5 Project Skeleton (~120 lines)**
- File tree (merged: draft_q3 §6.1 + draft_z2 §5 + my v2.1.0 §5).
  - Add `src/lib/fence.ts` (from draft_q3 §8.1).
  - Add `src/components/ErrorBoundary.tsx` and `ErrorFallback.tsx` (from draft_z2 §5).
  - Add `src/utils/theme-storage.ts` (from draft_z2 §5).
  - Add `src/lib/frontmatter.ts` (from draft_q3 §3.4).
- File responsibility rule (from my v2.1.0 §5).
- Bootstrap commands (from draft_z2 §5, with exact version pins).

**§6 Design System (Two-Layer Token Pattern) (~200 lines)**
- **§6.1 Two-layer architecture** (from draft_q3 §4.1): Layer 1 `:root` runtime variables flipped by `@media` / `[data-theme]`; Layer 2 `@theme inline` bridges to Tailwind utilities. Full `src/index.css` listing.
- **§6.2 Dark-mode semantics** (from draft_q3 §4.1): token names keep their role (ink = text/surfaces-that-invert, paper = page backgrounds); `:root:not([data-theme="light"])` allows forcing light when OS prefers dark.
- **§6.3 Typography hierarchy** (merged: draft_q3 §4.2 + draft_z2 §6.2).
- **§6.4 Color reference auto-generation** (from draft_q3 §4.3, with the compact script).
- **§6.5 Token usage rules** (from draft_z2 §6.3): mandatory (all colors from tokens) and forbidden (arbitrary hex, inline styles, magic numbers).
- **§6.6 Z-index layer map** (from draft_q3 §21).
- **§6.7 `theme-storage.ts`** (from draft_z2): `localStorage` with try/catch + in-memory fallback for sandboxed contexts.

**§7 Three Templates (~280 lines)**
- **§7.1 Template A — Editorial** (from draft_q3 §1 + draft_z2 §7.1): full layout description, visual register, default registry, "when to choose" guide.
- **§7.2 Template B — Technical** (from draft_d2 §5.3, **FIXED** with draft_q3's two-layer pattern): full `theme.css` listing with `:root` variables + `@theme inline` bridge, cool gray scale, blue accent.
- **§7.3 Template C — Minimal** (from draft_d2 §5.4, **FIXED**): full `theme.css` listing + print CSS (`@page`, page breaks, black-on-white, `print-color-adjust: exact` for badges).
- **§7.4 Template contract** (from draft_q3 §22): `TemplateConfig` interface, `TemplateLayoutProps`, `ComponentsMap`.
- **§7.5 Template selection procedure** (from draft_q3 §20.3): 4 steps to add a new template.

**§8 Tag Registry & Badge Protocol (~220 lines)**
- **§8.1 Tag registry schema** (from draft_q3 §7.2): `TagValueDefinition`, `TagDefinition`, `TagRegistry` types.
- **§8.2 Validation + collision detection** (from draft_q3 §7.2): `validateRegistry()` throws on duplicate values across tags, uppercase-registered values, out-of-range accents. Full code.
- **§8.3 Cross-category resolver** (from draft_q3 §7.2): `resolveBadge(registry, raw)` scans all tags, returns `{ tag, value, label, accent }` or `null`. Full code.
- **§8.4 Fence-aware preprocessor** (from draft_q3 §7.3): `enhanceMarkdown()` uses `scanLines()`, emits warnings for unknown values, leaves unmatched lines byte-identical. Full code.
- **§8.5 Disclosed blind spots** (from draft_q3 §7.3): badges inside blockquotes are not matched; values with trailing punctuation warn and render unstyled; only first-level bullets are targeted. Each covered by a fixture in §14.
- **§8.6 Badge component** (from draft_q3 §7.4): static chip surfaces (Tailwind default palette, do not flip in dark mode), accent text from `@theme` tokens. Full code.
- **§8.7 End-to-end pipeline** (from draft_z2 §8.5): the 5-step backtick-wrapping flow diagram (author writes → enhance wraps → react-markdown parses → components.code routes → Badge renders).
- **§8.8 Improvements over v1.0.1** (5 points, from draft_z2 §8.3): all bullet styles, warnings, data-not-code, CRLF-safe, regex character class.

**§9 TOC + Navigation Engine (~160 lines)**
- **§9.1 Fence-aware scanner** (from draft_q3 §8.1): `scanLines()` with full code. CommonMark-subset fence tracking (```` ``` ```` and `~~~`, up to 3 leading spaces, closing must be ≥ opening, unclosed extends to EOF).
- **§9.2 Extraction with slug reservation** (from draft_q3 §8.2): `buildToc()` consumes every heading level for slug dedup (matching `rehype-slug`), only H2–H4 enter the tree. Stack algorithm with `while (stack.length > 0 && stack[stack.length - 1].level >= level) stack.pop()`. Full code.
- **§9.3 Slug parity test** (from draft_q3 §8.3): correct default import (`GithubSlugger`), no unused imports (passes strict `noUnusedLocals`), 16 fixtures + full-document test + cross-level dedup test + fenced-heading test. Full code.
- **§9.4 Disclosed limitations** (from draft_q3 §8.4): setext headings invisible to line-based extractor (content convention: ATX only); headings deeper than `maxDepth` still slug-reserved; `scroll-mt-24` on every anchored heading.
- **§9.5 Active-section highlighting** (from draft_z2 §9.3 + draft_q3 §6.3): `flattenToc()` pattern that observes ALL TOC levels (not just top-level), `IntersectionObserver` with `rootMargin: "-80px 0px -80% 0px"`. Full code.
- **§9.6 TOC contract table** (from draft_q3 §8.2): H2 = depth 1, H3 = depth 2 (`ml-3 border-l`), H4 = depth 3 (`ml-6 border-l`), orphans promote to top.

**§10 Accessibility (WCAG 2.2 AA + AAA Aspirational) (~200 lines)**
- **§10.1 Posture** (from draft_q3 §9.1): "WCAG 2.2 AA, enforced by an axe gate. AAA where feasible; every exception is enumerated in §10.3." Explicitly rejects the "14px relaxes AAA" arithmetic error (Verified — stable WCAG definitions).
- **§10.2 Implementation matrix** (merged: draft_q3 §9.2 + draft_z2 §10.1): skip-to-content, focus visible, heading hierarchy, anchor offset, reduced motion, touch targets (≥44px), ARIA, landmarks, color contrast, color-not-sole-indicator, keyboard nav, language, live regions.
- **§10.3 Enumerated AAA exceptions** (from draft_q3 §9.3): per-token contrast ratios computed via WCAG relative-luminance formula, AA/AAA pass/fail, disposition. 6 rows (5 accent tokens + meta labels).
- **§10.4 The gate** (from draft_q3 §9.4): AA violations fail the build; AAA violations are advisory except `color-contrast` and `target-size` (gate-failures). No suppressions.
- **§10.5 High-contrast badge recipe** (from draft_q3 §9.5): darker accent tokens (`#7f1d1d`, `#78350f`, `#713f12`, `#365314`, `#1e40af`) achieving ~8.5–9.2:1. Opt-in via Layer-1 variable override.
- **§10.6 Dark-mode axe test** (from draft_q3 §12.3): tests both light and dark modes (sets `[data-theme="dark"]` before the run).
- **§10.7 Implementation code snippets** (from draft_z2 §10.2): `SkipLink.tsx`, `:focus-visible` CSS, touch target pattern, reduced-motion media query.

**§11 Build & Deploy Recipes (~200 lines)**
- **§11.1 Recipe A — CDN `@import`** (from draft_z2 §13.1): default online build, ~250–400 KB.
- **§11.2 Recipe B — Self-hosted `@font-face`** (from draft_z2 §13.2): alternative online build, full `@font-face` declarations + preload hints.
- **§11.3 Recipe C — `@fontsource` base64 inlining** (from draft_q3 §11.2): offline build, ~2–4 MB. `build-offline.mjs` script + conditional `main.tsx` import.
- **§11.4 Recipe D — GitHub Pages** (from draft_z2 §11.3): `base` config + `gh-pages` or `actions/upload-pages-artifact`.
- **§11.5 Recipe E — Local `file://` viewing** (from draft_q3 §11.1): default build works from `file://` (JS/CSS inlined); caveat that online build's `@import` fails from `file://` (CORS) — use Recipe C.
- **§11.6 System font fallbacks** (from draft_z2 §13.4): fallback chains for serif, sans, mono.
- **§11.7 Offline verification test** (from draft_z2 §13.5): Playwright test that goes offline and verifies fonts still render.
- **§11.8 Images** (from draft_q3 §11.3): documented limitation — local images resolved by Vite relative to importing module; for `?raw` markdown, place in `src/assets/` and reference by root-absolute path, or accept that only remote URLs are zero-config.
- **§11.9 Size comparison table** (from my v2.1.0 §11): online ~250–400 KB, self-hosted ~250–400 KB + fonts, offline ~2–4 MB.

**§12 Error Handling & Resilience (~140 lines)**
- **§12.1 Error boundary** (from draft_z2 §12.1): class component with `getDerivedStateFromError` + `componentDidCatch`. Full code.
- **§12.2 Error fallback UI** (from draft_z2 §12.2): presentational component with `role="alert"`, dev-only error details, reload button. Full code.
- **§12.3 Error reporter** (from draft_z2 §12.3, **SIMPLIFIED**): optional, env-gated via `import.meta.env.VITE_ERROR_REPORTING_ENDPOINT` (not `process.env`). Uses `fetch` with try/catch. Full code. **Moved to Appendix E as optional** — base skill ships without external reporting.
- **§12.4 Malformed markdown handling** (from draft_q3 §10.2): table of 6 scenarios (unclosed fence, broken table, invalid frontmatter, unknown badge value, colliding registry, empty markdown).
- **§12.5 What NOT to do** (from draft_z2 §12.5): no `dangerouslySetInnerHTML` (anti-pattern #10).
- **§12.6 Nested boundaries** (from draft_z2 §12.6): root-only boundary; defensive checks in pure functions, not nested boundaries.

**§13 Performance Optimization & Budgets (~120 lines)**
- **§13.1 Performance budgets** (from draft_z2 §14.1): 250 KB gzipped (corrected from draft_q2's unrealistic 150 KB), with bundle composition breakdown (React ~45KB, react-markdown ~80–120KB, etc.).
- **§13.2 Optimization techniques** (from draft_z2 §14.2): memoization (`useMemo` for enhance + toc + components map), code splitting (lazy load `MarkdownReport` for very large docs), virtual scrolling (Appendix E).
- **§13.3 No `gtag` hardcoding** (from draft_z2 §14.3 note): analytics is an extension point (Appendix E). The deploying team wires their provider of choice.
- **§13.4 Performance test examples** (from draft_z2 §14.4): `bundle-size.test.ts` (250 KB gzipped assertion) + `parsing-speed.test.ts` (1000 lines < 100ms, 5000 lines < 500ms). Full code.

**§14 Testing Strategy (~280 lines)**
- **§14.1 Test pyramid** (from draft_z2 §15.1): 70% unit, 20% integration, 10% visual/E2E.
- **§14.2 Unit tests — `fence.test.ts`** (from draft_q3 §12.1, NEW): 5 test cases (fence delimiters, tilde fences, unclosed, cross-character, length requirement). Full code.
- **§14.3 Unit tests — `enhance.test.ts`** (merged: draft_z2 §15.2 + draft_q3 §12.1): 12 test cases (bullet styles, multiple matches, CRLF, warnings, case sensitivity, fence-aware, blockquote blind spot). Full code.
- **§14.4 Unit tests — `toc.test.ts`** (merged: draft_z2 §15.3 + draft_q3 §12.1): 10 test cases (basic extraction, level jumps, orphan headings, slug generation, edge cases, fence-aware). Full code.
- **§14.5 Unit tests — `slug-parity.test.ts`** (from draft_q3 §8.3): correct imports, 16 fixtures + full-document test + cross-level dedup + fenced-heading. Full code.
- **§14.6 Unit tests — `frontmatter.test.ts`** (from draft_z2 §15.5): 7 test cases (extraction, absent, malformed, CRLF, colons, quotes, template/badgeConfig). Full code.
- **§14.7 Unit tests — `tags.test.ts`** (from draft_q3 §12.1, NEW): 5 test cases (clean registry, collision detection, uppercase rejection, out-of-range accent, resolver). Full code.
- **§14.8 Integration tests** (from draft_z2 §15.6): 4 test cases (badges, external links, tables, malformed markdown). Full code.
- **§14.9 Accessibility tests** (from draft_q3 §12.3): AA hard gate, AAA advisory (contrast + target-size enforced), dark-mode AA. Full code.
- **§14.10 Test configuration** (from draft_z2 §15.7): `vitest.config.ts` (90% thresholds, v8 coverage), `playwright.config.ts`, `tests/setup.ts`.
- **§14.11 Coverage statement** (from draft_q3 §12.2): 90% project-wide; 100% aspiration for core `lib/` modules (fence, toc, enhance, tags) — stated as aspiration enforced by review, not mislabeled as verified.

**§15 CI/CD & Quality Gates (~120 lines)**
- **§15.1 GitHub Actions workflow** (merged: draft_z2 §16.1 + draft_q3 §12.4): matrix Node 20/22, all gates in order, `actions/upload-pages-artifact` + `actions/deploy-pages` for native GitHub Pages deployment.
- **§15.2 Pre-commit hooks** (from draft_z2 §16.2): husky + lint-staged, prettier ordering rule (eslint --fix first, then prettier --write).
- **§15.3 Quality gate script** (from draft_z2 §16.3): `scripts/quality-gate.sh` runs all 8 gates in order.
- **§15.4 Lighthouse CI configuration** (from draft_z2 §16.4): `lighthouserc.yml` with score thresholds (a11y ≥ 0.95 error, performance ≥ 0.9 warn).
- **§15.5 Version gate V-1** (from draft_q3 §2): `npm run versions:check` = `npm ls --depth=0`. Resolves the lucide-react version question.
- **§15.6 Dropped from draft_q2** (from my v2.1.0 Appendix D): visual regression (requires baseline management), codecov upload (nice-to-have).

**§16 Anti-Patterns & Pitfalls (~120 lines)**
- **Merged table: 22 rows** (15 from draft_q3 §13 + 7 unique from draft_z2 §17).
- Rows include (numbered per draft_q3's pattern):
  1. Badge renders as plain `<code>` (enhance didn't wrap)
  2. Heading missing from TOC (level > maxDepth or inside fence)
  3. TOC anchor mismatch (slug desync)
  4. Typecheck fails on unused imports
  5. Fonts render as fallbacks (network blocked)
  6. Code blocks not highlighted (rehype-highlight opt-in)
  7. `import { slug }` from github-slugger (no named export)
  8. Error boundary everywhere (over-broad)
  9. Injecting raw HTML into markdown (react-markdown drops it)
  10. `dangerouslySetInnerHTML` (XSS surface, dual pipelines) — **from draft_q3, rejects draft_d2's bug**
  11. Badge classes in runtime config strings (Tailwind can't scan)
  12. `@theme` inside `@media` (dark mode silently dead) — **from draft_q3, rejects draft_z/d2/z2/my v2.1.0 bug**
  13. Claiming AAA because "14px is bigger" (WCAG large text is ≥18pt/≥14pt-bold) — **from draft_q3, rejects draft_z/d2/z2/my v2.1.0 bug**
  14. Fence-blind line regexes (fenced `## comment` in TOC) — **from draft_q3**
  15. Duplicate badge values across tags (collision) — **from draft_q3**
  16. Hardcoded tag keys in components — **from draft_z2**
  17. Hand-write heading `id`s — **from draft_z2**
  18. Use setext headings — **from draft_q3**
  19. Nest `@theme` in `@media` — **from draft_q3 (duplicate of #12, but kept for emphasis)**
  20. Claim offline support for default build — **from draft_z2**
  21. Skip gates to ship — **from draft_z2**
  22. Copy version numbers between documents — **from draft_q3**

**§17 Pre-Ship Checklist (~90 lines)**
- **8 hard gates** (unified per Decision 7):
  1. Typecheck (`npm run typecheck`)
  2. Lint (`npm run lint` + `lint:format` + `lint:markdown`)
  3. Unit tests (`npm run test -- --coverage`, includes slug-parity — the single most important test)
  4. Integration tests (`npm run test:integration`)
  5. Accessibility (`npm run a11y` — AA hard-fail, AAA contrast/target-size enforced, light + dark)
  6. Build (`npm run build` + `npm run build:offline` + bundle size check < 250 KB gzipped)
  7. Smoke test (`npm run preview` — manual verification checklist)
  8. Dependency verification (`npm run versions:check` = gate V-1)
- "All eight gates must pass. No gate may be skipped, weakened, or made non-blocking to ship."

**§18 Debugging Guide (~90 lines)**
- **Merged table: 20 rows** (14 from draft_z2 §19 + 6 unique from draft_q3 §14).
- Rows include (additions from draft_q3 marked NEW):
  - Build fails with vite-plugin-singlefile error
  - TOC anchor doesn't scroll
  - TOC anchor wrong target
  - Badge wrong color
  - Badge renders as plain `<code>`
  - Badge pipeline emits raw HTML that renders as text
  - Heading missing from TOC
  - TOC tree malformed on H2 → H4 jump
  - TypeScript error: unused local/param
  - Dev server won't start
  - Fonts look wrong (online build)
  - Offline build is huge (>5 MB)
  - Lighthouse a11y score < 95
  - Theme toggle doesn't persist
  - Active section doesn't highlight
  - `enhance.ts` warnings in build
  - Build warning: Cannot find module @fontsource/...
  - Test failure: `use(undefined)` throws
  - `extractFrontmatter` returns empty on Windows-authored file
  - CI fails on bundle size
  - **NEW: Dark mode doesn't apply** (`data-theme` not set, or `@theme` nested in media — verify §6.1 structure)
  - **NEW: Dark mode flickers on load** (theme applied after first paint — set `data-theme` from inline script in `index.html` before the bundle)
  - **NEW: Startup error "badge value collision"** (two tags share a value — rename one; collision detection is intentional)
  - **NEW: `lucide-react` install fails** (pinned version may not exist — gate V-1; install current 0.x, update §4 table)
  - **NEW: Fenced headings appear in TOC** (verify `scanLines()` is wired into `buildToc`)
  - **NEW: `npm ls --depth=0` shows version drift** (run `npm install <pkg>@<exact-version>` to pin)

**§19 Extending the Skill (~90 lines)**
- **§19.1 Adding a new template** (from draft_q3 §20.3): 4 steps.
- **§19.2 Adding a new tag** (from draft_q3 §20.2, with collision detection note): 4 steps + run `npm run test` to verify no collision.
- **§19.3 Adding a markdown extension** (from draft_z2 §20.3): footnotes, math, mermaid — 5 steps each.
- **§19.4 Adding syntax highlighting** (from draft_z2 §20.4): `rehype-highlight` + highlight.js CSS theme + copy button.
- **§19.5 Adding search** (from draft_z2 §20.5): `lunr` or `flexsearch`, cmd-K palette at `z-30`.
- **§19.6 Multi-framework rejection** (from draft_z2 §20.6): React-only by design; Vue/Svelte users adapt the patterns, not the code.

**§20 Migration Guide (~140 lines)**
- **§20.1 From v1.0.1** (from draft_q3 §23.1): table mapping every v1.0.1 pattern to its v4.0.0 replacement.
- **§20.2 From the drafts** (from draft_q3 §23.2): what to keep/drop from draft_k, draft_d, draft_q2, draft_z, draft_q3, draft_z2, draft_d2.
- **§20.3 6-week phased migration plan** (from draft_d2 §20, **preserved**):
  - Week 1: Add tests
  - Week 2: Fix accessibility
  - Week 3: Design token consistency
  - Week 4: Generalize badge system
  - Week 5: Offline font strategy
  - Week 6: CI/CD
- **§20.4 Migration procedure** (10 steps, from draft_z2 §21.1): backup → rename → add skeleton → install deps → copy editorial template → copy tag registry → run slug-parity test → run full pre-ship gate → visually compare → commit.

**§21 Evidence Contract (~50 lines)**
- Preserved verbatim from v1.0.1 (from my v2.1.0 §16).
- Four tags: Verified, Reasoned, Assumed, Unverifiable.
- Rule: "Never upgrade a tag. If a claim is Reasoned, do not present it as Verified."
- Verification ledger: what was checked, how, and the result.
- Applied to the skill file itself (every non-trivial claim carries a tag).

**§22 TypeScript Reference (~120 lines)**
- **§22.1 `src/types/template.ts`** (from draft_z2 §23.1): `TemplateName`, `TemplateLayoutProps`, `ComponentsMap`, `TemplateConfig`.
- **§22.2 `src/types/tag.ts`** (from draft_q3 §7.2): `TagValueDefinition`, `TagDefinition`, `TagRegistry`.
- **§22.3 `src/types/toc.ts`** (from draft_q3 §8.2): `TocItem`.
- **§22.4 `src/types/config.ts`** (from draft_z2 §23.4): `MarkdownToWebConfig` type included for teams that want it; `defineConfig` helper explicitly rejected per §3.3.
- **§22.5 `src/lib/frontmatter.ts`** (from draft_q3 §3.4): CRLF-safe `extractFrontmatter()`. Full code.
- **§22.6 Additional named types**: `ResolvedBadge` (§8.3), `EnhanceResult` (§8.4), `MarkdownRegion` (§9.1), `Frontmatter` (§22.5).
- **§22.7 Component props summary**: `App`, `MarkdownRenderer`, `TableOfContents`, `Badge`, `ErrorBoundary`, `ErrorFallback`, `SkipLink`, `ThemeToggle`.

### APPENDICES (~400 lines)

**Appendix A — Correction Ledger (~120 lines)**
- Every finding from Part 1 + comparative review, mapped to its v4.0.0 fix.
- 35+ rows (20 original findings + 15 comparative review findings).
- Format: `| Finding | Severity | Resolution in v4.0.0 |` (from draft_q3 Appendix B pattern).
- This is the single source of truth for traceability.

**Appendix B — Complete TypeScript Reference (~80 lines)**
- Full type definitions consolidated from §22 (all types in one place for easy reference).

**Appendix C — Testing Fixtures (~150 lines)**
- All test files in one place (consolidated from §14):
  - `tests/unit/fence.test.ts`
  - `tests/unit/enhance.test.ts`
  - `tests/unit/toc.test.ts`
  - `tests/unit/slug-parity.test.ts`
  - `tests/unit/frontmatter.test.ts`
  - `tests/unit/tags.test.ts`
  - `tests/integration/markdown-rendering.test.tsx`
  - `tests/accessibility/axe.test.ts`
- Note: "These fixtures are starting points. Run `npm run test` after implementation to verify."

**Appendix D — CI/CD Workflow (~60 lines)**
- `.github/workflows/ci.yml` (full file, from §15.1).
- `.husky/pre-commit` (from §15.2).
- `package.json` scripts excerpt (from §15.2).
- `lighthouserc.yml` (from §15.4).

**Appendix E — Advanced Patterns (~60 lines)**
- **E.1 AST-based badge processing** (from my v2.1.0 Appendix E): for future enhancement if regex proves insufficient. Tradeoff documented.
- **E.2 Virtual scrolling for 10,000+ line documents** (from my v2.1.0 Appendix E): `@tanstack/react-virtual`. Tradeoff: breaks IntersectionObserver.
- **E.3 Search functionality** (from my v2.1.0 Appendix E): `useSearch` hook, cmd-K palette.
- **E.4 Error reporting to external endpoint** (from draft_z2 §12.3, moved here as optional): `ErrorReporter` class with `fetch` to `import.meta.env.VITE_ERROR_REPORTING_ENDPOINT`.
- **E.5 Performance monitoring** (from draft_z2 §14.3, **SIMPLIFIED**): `PerformanceMonitor` class without `window.gtag` hardcoding. Analytics is an extension point.
- **E.6 Footnotes, math, mermaid** (from my v2.1.0 Appendix E): one-line `remarkPlugins` additions with size costs.

**Appendix F — Adopter Spot-Check (~40 lines)**
- 10-minute verification procedure (from draft_q3 Appendix C):
  1. Scaffold: `npm create vite@latest mdw-spotcheck -- --template react-ts`
  2. Install runtime deps (exact pins from §4)
  3. Gate V-1 — resolve the lucide-react question
  4. Copy `src/lib/{fence,toc,enhance,tags,frontmatter}.ts`, `src/types/`, and `tests/` from this document
  5. Run core suites: `npx vitest run`
  6. Single-file + offline sanity: `npm run build` + `npm run build:offline`
  7. Tailwind dark pattern sanity: build with §6.1 `index.css`, toggle OS dark mode — utilities must flip live
- "Record the outcomes in a copy of the §21 ledger; upgrade only the rows your run actually proved."

---

## IV. Quality Gates for the Merged Document Itself

Before the document is declared complete, verify:

1. **Every bug in the Bug Fix Registry (§II) has a corresponding fix in Part 2.** Cross-reference check via Appendix A (Correction Ledger).

2. **No `@theme` appears inside `@media`.** Grep verification:
   ```bash
   grep -A2 "@media.*prefers-color-scheme" markdown-to-web_SKILL_v4.md | grep "@theme"
   # Must return nothing (except in §16 anti-pattern #12 documenting the rejection)
   ```

3. **No "14px relaxes AAA" claim.** Grep verification:
   ```bash
   grep -i "14px.*relax\|relaxes.*AAA\|14 px.*relax" markdown-to-web_SKILL_v4.md
   # Must return nothing (except in Part 1 Finding 21.2 documenting the bug, 
   # and §10.1 explicitly rejecting it)
   ```

4. **No `dangerouslySetInnerHTML` in v4.0.0 code.** Grep verification:
   ```bash
   grep "dangerouslySetInnerHTML" markdown-to-web_SKILL_v4.md
   # Must return only §16 anti-pattern #10 documenting the rejection
   ```

5. **Fence-aware scanner present.** Grep verification:
   ```bash
   grep -c "scanLines\|fence.ts\|insideFence" markdown-to-web_SKILL_v4.md
   # Must return ≥ 10 hits across §5, §8, §9, §14, Appendix A
   ```

6. **Collision detection present.** Grep verification:
   ```bash
   grep -c "validateRegistry\|collision" markdown-to-web_SKILL_v4.md
   # Must return ≥ 5 hits across §8, §14, §16, Appendix A
   ```

7. **Evidence contract applied to the skill document itself.** Every non-trivial claim carries a confidence tag (Verified / Reasoned / Assumed / Unverifiable). The §21 contract is applied to the document itself, not just documented.

8. **Code snippets are syntactically valid TypeScript.** No unclosed braces, no undefined variables, no hallucinated APIs. (Reasoned — not re-verified by `tsc` at authoring time.)

9. **No placeholder values.** Every token, color, version number, file path is concrete and correct. No `TODO`, `FIXME`, `XXX`, `TBD`, `placeholder`, `lorem ipsum`.

10. **No contradictions.** The "AA + AAA aspirational" framing is used consistently; no claim of "WCAG AAA" without qualification; no "14px relaxes" anywhere; no `@theme`-in-`@media` in code blocks.

11. **Length check:** Target 2,800–3,200 lines. If exceeding 3,400, trim Appendix E and condense §7 template descriptions. If below 2,600, expand test code in §14 and Appendix C.

12. **Self-check against Definition of Done:**
    - Every part of the request addressed? Yes — unified merged skill file incorporating all recommendations.
    - Syntactically valid? Yes — markdown with TypeScript code blocks.
    - No secrets, placeholders, commented-out code? Yes.
    - All claims backed by evidence or labeled? Yes — §21 applied.
    - Relevant documentation updated? N/A — this IS the documentation.
    - Final artifact in correct location? Yes — `/home/z/my-project/download/markdown-to-web_SKILL_v4.md`.

---

## V. Implementation Order

**Phase 1: Skeleton & Front Matter** (~15 min)
1. YAML front matter block (v4.0.0)
2. Part 1 heading structure with all 20 original findings + 15 new comparative findings as section stubs
3. Part 2 heading structure with all §1–§22 as section stubs
4. Appendix heading structure (A–F)

**Phase 2: Part 1 — Validation Review** (~45 min)
5. Executive Summary (updated severity table + comparative review subsection)
6. Methodology (updated for two review rounds)
7. All 20 original findings (copy from my v2.1.0, verify no drift)
8. §21 Comparative Review Findings (15 new findings, formatted per evidence contract)
9. Cross-cutting observations (expanded to 10)
10. Reuse value assessment (expanded table)

**Phase 3: Part 2 — Core Specification** (~90 min)
11. §1–§3 (Identity, When to Use, Inputs) — from draft_q3 + draft_z2
12. §4–§5 (Tech Stack, Project Skeleton) — from draft_q3 + draft_z2
13. §6 (Design System — two-layer token pattern) — from draft_q3 §4.1, **CRITICAL**
14. §7 (Three Templates — full CSS) — from draft_d2, **FIXED** with draft_q3 pattern
15. §8 (Tag Registry — with collision detection) — from draft_q3 §7
16. §9 (TOC — fence-aware) — from draft_q3 §8

**Phase 4: Part 2 — Advanced Sections** (~75 min)
17. §10 (Accessibility — correct arithmetic) — from draft_q3 §9, **CRITICAL**
18. §11 (Build Recipes — 3 font strategies) — from draft_z2 §13
19. §12 (Error Handling) — from draft_z2 §12
20. §13 (Performance) — from draft_z2 §14
21. §14 (Testing — full code) — from draft_z2 §15 + draft_q3 tests
22. §15 (CI/CD) — from draft_z2 §16

**Phase 5: Part 2 — Reference Sections** (~45 min)
23. §16 (Anti-Patterns — merged 22-row table)
24. §17 (Pre-Ship — 8 gates)
25. §18 (Debugging — merged 20-row table)
26. §19 (Extending)
27. §20 (Migration — 6-week plan from draft_d2)
28. §21 (Evidence Contract — preserved verbatim)
29. §22 (TypeScript Reference)

**Phase 6: Appendices** (~45 min)
30. Appendix A (Correction Ledger — 35+ rows)
31. Appendix B (TypeScript Reference — consolidated)
32. Appendix C (Testing Fixtures — consolidated)
33. Appendix D (CI/CD Workflow — full file)
34. Appendix E (Advanced Patterns — optional)
35. Appendix F (Adopter Spot-Check — 10-min procedure)

**Phase 7: Cross-Reference Verification** (~30 min)
36. Verify every Part 1 finding has a Part 2 fix (Appendix A cross-reference table)
37. Verify every bug in the Bug Fix Registry (§II) is resolved
38. Run grep checks (Quality Gates #2–#6 above)
39. Verify evidence contract tags on all non-trivial claims
40. Verify no placeholder values (grep for `TODO|FIXME|XXX|TBD|placeholder`)
41. Verify line count target (2,800–3,200)
42. Save to `/home/z/my-project/download/markdown-to-web_SKILL_v4.md`

**Estimated total:** ~5.5 hours of focused composition.

---

## VI. Explicit Assumptions

1. The user wants a single markdown file, not a zip archive or multi-file project.
2. The v4.0.0 skill replaces all prior editions (v1.0.1, draft_z, draft_q3, draft_z2, draft_d2, my v2.1.0); no backward compatibility with v1.0.1 naming is required beyond Appendix A (Correction Ledger) and §20 (Migration Guide).
3. Version numbering: v4.0.0 (major bump — fixes two critical bugs present in all prior editions, including those presented as production-ready).
4. The skill file itself does not need to be buildable or runnable — it is documentation. Code snippets within it are illustrative but should be syntactically valid TypeScript.
5. English-only (no CJK content in the skill file itself, though CJK heading support is tested in §14.5).
6. The Part 1 validation review is preserved because it provides unique value (no other edition has it) and justifies every v4.0.0 design decision by referencing the finding it fixes.
7. The 6-week phased migration plan (from draft_d2 §20) is included because it provides actionable guidance for teams migrating from v1.0.1, even though the plan is more conservative than the v4.0.0 spec requires (a team can migrate faster by copying the starter project and running the 8-gate pre-ship).
8. `defineConfig` is rejected (per draft_q3 §3.3) but the `MarkdownToWebConfig` type is included in §22 for teams that want to build their own config helper.
9. The `ErrorReporter` with external endpoint is moved to Appendix E (optional) because it assumes infrastructure most users don't have. The base skill ships with `ErrorBoundary` + `ErrorFallback` only.
10. The `PerformanceMonitor` class is moved to Appendix E (optional) and stripped of the hardcoded `window.gtag` calls. Analytics is an extension point.
11. All four source documents (draft_q3, draft_z2, draft_d2, my v2.1.0) are treated as prior art to be merged selectively, not as competing specifications. The provenance of each merged element is documented in the §1.4 reuse table and Appendix A.

---

## VII. Confirmation Request

**Please confirm the following before I proceed to implementation:**

1. ✅ **Adopt draft_q3.md as the canonical base** with selective merges from draft_z2, draft_d2, and my v2.1.0?
2. ✅ **Fix all 15 bugs in the Bug Fix Registry** (3 critical + 2 high + 6 medium + 4 low)?
3. ✅ **Use the two-layer token pattern** (draft_q3 §4.1) for dark mode, rejecting the `@theme`-in-`@media` pattern?
4. ✅ **Use the correct WCAG arithmetic** (draft_q3 §9.1) + high-contrast recipe (§9.5), rejecting the "14px relaxes AAA" claim?
5. ✅ **Include the fence-aware scanner** (draft_q3 §8.1) and collision detection (§7.2)?
6. ✅ **Preserve and expand Part 1 Validation Review** (20 original + 15 comparative findings)?
7. ✅ **Merge three font strategies** (CDN, self-hosted, @fontsource offline) from draft_z2?
8. ✅ **Include full test code** (fence, enhance, toc, slug-parity, frontmatter, tags, integration, a11y) from draft_z2 + draft_q3?
9. ✅ **Include the 6-week phased migration plan** from draft_d2?
10. ✅ **Target ~2,800–3,200 lines** for the final document?
11. ✅ **Version as v4.0.0**?
12. ✅ **Save to `/home/z/my-project/download/markdown-to-web_SKILL_v4.md`**?
13. Any **specific additions, removals, or modifications** to the plan above?

Awaiting your go-ahead to begin Phase 1.
