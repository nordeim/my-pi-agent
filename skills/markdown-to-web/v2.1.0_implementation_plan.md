# Unified Skill File — Meticulous Implementation Plan
## `markdown-to-web_SKILL.md` v2.1.0

**Date:** 2026-08-06  
**Base:** draft_z.md (Part 1 + Part 2)  
**Merge sources:** original_SKILL.md (v1.0.1), draft_q2.md, draft_k.md, draft_d.md  
**Drop list:** Multi-framework adapters, AST-based processing, PerformanceMonitor, regex-in-config, over-engineered abstractions  
**Target length:** ~2,000–2,200 lines (between draft_z's 1,555 and draft_q2's 2,560)  
**Confidence:** Reasoned (design document; implementation not yet executed)

---

## I. Architectural Decisions (Locked Before Writing)

### 1. Document Structure: Two-Part + Appendices

The unified document follows draft_z's proven two-part structure but integrates draft_q2's testing depth as appendices rather than main flow:

```
FRONT MATTER (YAML metadata block)
├── name, description, version, tags

PART 1 — VALIDATION REVIEW
├── Executive Summary (severity counts, verdict)
├── Methodology (finding format, confidence taxonomy)
├── Section-by-Section Findings (20 findings, severity-ordered)
├── Cross-Cutting Observations (7 systemic issues)
├── Reuse Value Assessment (module-by-module table)

PART 2 — UNIFIED SKILL SPECIFICATION (v2.1.0)
├── §1  Identity & Design Philosophy
├── §2  When to Use / When Not To
├── §3  Inputs Contract
├── §4  Tech Stack & Pinned Versions
├── §5  Project Skeleton
├── §6  Design System (Code-First, Per-Template)
├── §7  Three Templates (Editorial / Technical / Minimal)
├── §8  Tag Registry & Badge Protocol
├── §9  TOC + Navigation Engine
├── §10 Accessibility (WCAG 2.2 AA + AAA Aspirational)
├── §11 Build & Deploy Recipes
├── §12 Anti-Patterns & Pitfalls
├── §13 Pre-Ship Checklist (8 Hard Gates)
├── §14 Debugging Guide
├── §15 Extending the Skill
├── §16 Evidence Contract

APPENDICES
├── A — Migration from react-markdown-report v1.0.1
├── B — Complete TypeScript Reference
├── C — Testing Fixtures (unit + integration + a11y)
├── D — CI/CD Workflow (GitHub Actions)
├── E — Advanced Patterns (optional enhancements)
```

### 2. What to Take from Each Source

| Source | Elements to MERGE | Elements to DROP |
|--------|-------------------|------------------|
| **original_SKILL.md** | Evidence contract (§16), anti-pattern table format (symptom→cause→fix), color reference exhaustiveness, lessons learned discipline, `@theme` code-first approach, z-index layer map discipline | Hardcoded 9 badge keys, single-report scope, `comparative-analysis.md` content path, "WCAG AAA" over-claim |
| **draft_d.md** | Config system concept (but simplified: tag registry JSON, not 8-level nested TS interface), image embedding strategy, dark mode toggle | Over-engineered `MarkdownToWebConfig` schema, "virtual module" hand-waving, regex in config files, `defineConfig` helper |
| **draft_k.md** | Badge registry pattern (generalized to JSON), frontmatter support, error boundaries, syntax highlighting opt-in, H4 TOC depth, migration appendix | Hardcoded TS badge registry (replace with JSON), no lessons learned section, no validation review |
| **draft_q2.md** | Test pyramid structure, unit test fixtures (TOC extraction, badge rendering), a11y test patterns with axe-core, CI/CD workflow file, performance budgets, security hardening checklist | Multi-framework adapters (React/Vue/Svelte), AST-based badge processing, `PerformanceMonitor` class, `ErrorReporter` with external endpoint, `@tanstack/react-virtual`, 2,560-line bloat |
| **draft_z.md** | ENTIRE Part 1 validation review (20 findings), Part 2 structure, three-template system, tag registry (JSON-based, 5-step accent scale), slug parity test, offline build mode, 8-gate pre-ship, honest "AA + AAA aspirational" claim | None — this is the base document |

### 3. Key Design Decisions

**Decision 1: Tag Registry over Config Schema**
- REJECT draft_d's `MarkdownToWebConfig` interface (8 nested properties, over-engineered).
- ADOPT draft_z's JSON-based tag registry: each template ships a `tags.json` that maps `**Tag:** value` bullets to accent steps (1–5).
- Rationale: Simpler, data-driven, no TypeScript compilation required to add a new badge type. An agent can hand-edit JSON faster than refactoring interfaces.

**Decision 2: Regex Preprocessor over AST Processing**
- REJECT draft_q2's `unist-util-visit` AST-based badge processing.
- ADOPT draft_z's regex preprocessor (enhanced to accept all bullet styles: `-`, `*`, `+`, `1.`).
- Rationale: The regex approach is 10 lines of code vs. 40+ lines of AST traversal. For a skill file that an agent must implement in one session, simplicity wins. The AST approach is technically superior but cognitively expensive. Document it in Appendix E as an "advanced pattern" for future enhancement.

**Decision 3: React-Only (No Multi-Framework)**
- REJECT draft_q2's React/Vue/Svelte adapter pattern.
- ADOPT React 19 + Vite 7 + Tailwind v4 as the sole stack.
- Rationale: YAGNI. No user has requested Vue or Svelte support. The skill's trigger surface is "render markdown as web page" — 100% of requests in this context expect React. Adding adapters triples scope without user value.

**Decision 4: Three Templates, Not One Config System**
- REJECT draft_d's single configurable system with deep nested objects.
- ADOPT draft_z's three-template approach: Editorial (default), Technical, Minimal. Each template is a self-contained directory with its own `@theme`, component map, layout, and `tags.json`.
- Rationale: Templates are copy-paste friendly for agents. A "config system" requires runtime merging logic that adds bugs. Templates are declarative and inspectable.

**Decision 5: Evidence Contract Preserved Verbatim**
- From original_SKILL.md §12 and draft_z §2.16.
- Every claim in the skill document itself must carry a confidence tag: Verified, Reasoned, Assumed, Unverifiable.
- This is non-negotiable. It is the skill's signature quality marker.

**Decision 6: Pre-Ship Checklist Has 8 Hard Gates**
- From draft_z §2.13, enhanced with draft_q2's testing fixtures.
- Gates: typecheck → lint → unit test → integration test → a11y test → build → smoke test → dependency verification.
- No gate may be skipped, weakened, or made non-blocking.

---

## II. Section-by-Section Blueprint

### PART 1 — VALIDATION REVIEW (~400 lines)

**Structure:** Identical to draft_z Part 1, with these refinements:

1. **Executive Summary** — Keep severity count table (0 Critical, 3 High, 7 Medium, 5 Low, 4 Informational). Add a "Reuse Value Assessment" summary table.

2. **Methodology** — Keep the finding format (Location, Description, Evidence, Impact, Severity, Confidence, Recommended Fix). Add a note: "Findings tagged per the skill's own evidence contract (§16)."

3. **Section-by-Section Findings** — All 20 findings from draft_z, preserved verbatim. These are the load-bearing critique. No findings are dropped or softened.

4. **Cross-Cutting Observations** — 7 observations from draft_z, preserved. Add an 8th: "draft_q2 introduces over-engineering that must be explicitly rejected in the unified skill (see §II.3)."

5. **Reuse Value Assessment** — Module-by-module table mapping each v1.0.1 module to its reuse action in v2.1.0.

### PART 2 — UNIFIED SKILL SPECIFICATION (~1,200 lines)

**§1 Identity & Design Philosophy (~80 lines)**
- One-sentence description: generalized, template-driven, single-file, accessible.
- Core tenets: Content is sovereign, Convention over configuration, Single-file portability, Accessibility by default, No generic UI (per-template).
- Anti-generic mandate: explicitly rejected patterns (purple gradients, card grids, etc.) — scoped per-template, not global.
- Evidence contract reminder: every finding in any rendered document carries explicit confidence tag.

**§2 When to Use / When Not To (~60 lines)**
- Use: markdown → web page, long-form documents, badge annotations, offline requirement, accessibility requirement.
- Do NOT use: full Next.js app, slide deck, PDF, interactive code execution, <500 words.
- Template selection guide: Editorial (reports/essays), Technical (API docs), Minimal (print/manuscripts).

**§3 Inputs Contract (~50 lines)**
- Table: Markdown file (required), Template (default: editorial), Tag registry (default: template's), Theme override (optional), Title (default: first H1), Author (optional), Offline fonts (default: false).
- Supported markdown features list (GFM: tables, strikethrough, task lists, autolinks).
- Out-of-scope features list (footnotes, math, mermaid — with "add via remark plugin" note).

**§4 Tech Stack & Pinned Versions (~60 lines)**
- Table identical to draft_z §2.4: React 19.2.6, Vite 7.3.2, Tailwind 4.1.17, react-markdown 10.1.0, rehype-slug 6.0.0, github-slugger 2.0.0, lucide-react 1.28.0, clsx 2.1.1, tailwind-merge 3.4.0, vite-plugin-singlefile 2.3.0.
- NEW: Add testing dependencies from draft_q2: vitest 2.x, @testing-library/react 16.x, @axe-core/playwright 4.10.0.
- NEW: Add offline font dependencies: @fontsource-variable/source-serif-4 5.0.0, @fontsource-variable/inter 5.0.0, @fontsource/jetbrains-mono 5.0.0.
- Verification command: `npm ls --depth=0`.

**§5 Project Skeleton (~80 lines)**
- File tree from draft_z §2.5, with additions:
  - `tests/` directory: `enhance.test.ts`, `toc.test.ts`, `slug-parity.test.ts`, `axe.test.ts`.
  - `.github/workflows/ci.yml` (Appendix D reference).
- File responsibility rule: one file, one responsibility.

**§6 Design System (Code-First, Per-Template) (~120 lines)**
- Editorial template `@theme` block (light + dark + reduced-motion + focus-visible) from draft_z §2.6.
- Typography hierarchy table (H1–H4, Body, Lead, Meta, Badge, Code block) with mobile/desktop sizes.
- Color reference: auto-generated note ("Run `node scripts/generate-color-ref.mjs`").
- Token usage rules: mandatory (all colors from tokens) and forbidden (arbitrary hex, inline styles, magic numbers).

**§7 Three Templates (~200 lines)**
- **Template A — Editorial Long-Form** (default): Use cases, layout description (sticky dark header, sidebar TOC, hero, footer), visual register (Source Serif 4, warm paper, teal/moss), default tag registry (Severity + Confidence).
- **Template B — Technical Docs**: Use cases, layout (three-column desktop with search, two-column mobile), visual register (Inter throughout, cool gray, blue accent), default tag registry (Status + Visibility).
- **Template C — Minimal Print**: Use cases, layout (single column, no header/sidebar, print CSS), visual register (system fonts, black on white), default tag registry (none, badges disabled).
- Each template section includes a "When to choose this template" decision guide.

**§8 Tag Registry & Badge Protocol (~150 lines)**
- Tag registry schema (`TagDefinition`, `TagRegistry` interfaces).
- Default editorial `tags.json` example.
- `enhance.ts` preprocessor code (from draft_z §2.8): accepts all bullet styles, emits build-time warnings for unknown tags/values.
- `Badge.tsx` component code: 5-step accent scale, 14 px text (fixes AAA contrast), `cn()` helper usage.
- Improvements over v1.0.1: four bullet points mapping each fix to its original finding number.

**§9 TOC + Navigation Engine (~100 lines)**
- `buildToc()` function code (H2–H4, configurable depth, stack-based nesting).
- Slug parity test code: 11 fixture headings (emoji, CJK, backticks, repeated, whitespace).
- Active-section highlighting: `IntersectionObserver` setup in `App.tsx`.
- TOC contract table: heading level → TOC depth → indentation.

**§10 Accessibility (WCAG 2.2 AA + AAA Aspirational) (~150 lines)**
- Feature table: Skip-to-content, Focus visible, Heading hierarchy, Anchor offset, Reduced motion, Touch targets (≥44 px), ARIA labels, Semantic landmarks, Color contrast (body ≥7:1, badges ≥4.5:1 at 14 px), Color-not-sole-indicator, Keyboard nav, Language.
- Implementation code snippets: `SkipLink.tsx`, `:focus-visible` CSS, touch target CSS, reduced-motion media query.
- Pre-ship a11y command: `npm run a11y` (Playwright + axe-core).
- `tests/axe.test.ts` code: WCAG 2.2 AA pass assertion + AAA aspirational with critical filter.
- Honest statement: "Headline claim is 'WCAG 2.2 AA; AAA where feasible, with documented exceptions.'"

**§11 Build & Deploy Recipes (~120 lines)**
- Recipe A: Default single-file build (CDN fonts). `vite.config.ts` code.
- Recipe B: Offline single-file build (fonts inlined as base64). `scripts/build-offline.mjs` code. `main.tsx` conditional import.
- Recipe C: GitHub Pages deployment.
- Recipe D: Local `file://` viewing.
- Size notes: online ~250–400 KB, offline ~2–4 MB.

**§12 Anti-Patterns & Pitfalls (~80 lines)**
- Table: Don't / Do, 12 rows.
- Covers: hardcoded tag keys, manual slugs, slug parity assumptions, offline font assumptions, `tailwind.config.js` for colors, relative imports, global state for document data, claiming AAA without verification, 12 px badge text, small touch targets, unguarded smooth-scroll, skipping pre-ship gates, editing components for content changes, forking to switch templates.

**§13 Pre-Ship Checklist (8 Hard Gates) (~60 lines)**
- 8 numbered commands with verification criteria.
- Gate 1: typecheck. Gate 2: lint. Gate 3: unit tests. Gate 4: integration tests. Gate 5: a11y tests. Gate 6: build. Gate 7: smoke test. Gate 8: dependency verification.
- "All eight gates must pass. No gate may be skipped, weakened, or made non-blocking to ship."

**§14 Debugging Guide (~60 lines)**
- Symptom / Cause / Fix table, 14 rows.
- Covers all common issues from original §10 + draft_z §2.14 + new issues (offline build size, theme toggle persistence, active section highlighting).

**§15 Extending the Skill (~80 lines)**
- Adding a new template (5 steps).
- Adding a new tag (4 steps).
- Adding a markdown extension (footnotes, math, mermaid — 5 steps).
- Adding syntax highlighting (4 steps).

**§16 Evidence Contract (~40 lines)**
- Preserved verbatim from original §12 + draft_z §2.16.
- Four tags: Verified, Reasoned, Assumed, Unverifiable.
- Rule: "Never upgrade a tag. If a claim is Reasoned, do not present it as Verified."
- Verification ledger: what was checked, how, and the result.

### APPENDICES (~300 lines)

**Appendix A — Migration from react-markdown-report v1.0.1 (~60 lines)**
- Table: v1.0.1 element → v2.1.0 element → migration action.
- 15 rows covering every changed module.

**Appendix B — Complete TypeScript Reference (~80 lines)**
- `TemplateConfig`, `TemplateLayoutProps`, `ComponentsMap` (from draft_z Appendix B).
- `TagDefinition`, `TagValueDefinition`, `TagRegistry` (from draft_z Appendix B).
- `TocItem` (from draft_z).
- Component props: `MarkdownReport`, `TableOfContents`, `Badge`, `SkipLink`, `ThemeToggle`.

**Appendix C — Testing Fixtures (NEW from draft_q2) (~80 lines)**
- `tests/unit/toc-extractor.test.ts`: 6 test cases (basic extraction, nesting, orphan headings, slug consistency, backtick stripping, empty markdown, depth range).
- `tests/unit/enhance.test.ts`: 4 test cases (registered tag match, unknown tag warning, unknown value warning, all bullet styles).
- `tests/integration/markdown-rendering.test.tsx`: 3 test cases (badges render, TOC renders, malformed markdown graceful).
- `tests/accessibility/axe.test.tsx`: 3 test cases (WCAG 2.2 AA pass, heading hierarchy, color contrast).
- Note: "These fixtures are starting points. Run `npm run test` after implementation to verify."

**Appendix D — CI/CD Workflow (NEW from draft_q2) (~50 lines)**
- `.github/workflows/ci.yml`: Complete GitHub Actions workflow.
- Jobs: test (matrix Node 20/22), lint, typecheck, unit tests, integration tests, a11y tests, build, bundle analysis, E2E, visual regression, Lighthouse, security audit.
- Pre-commit hooks: husky + lint-staged configuration.

**Appendix E — Advanced Patterns (NEW, optional) (~30 lines)**
- AST-based badge processing (draft_q2 §5.3) — for future enhancement if regex proves insufficient.
- Virtual scrolling for 10,000+ line documents — `@tanstack/react-virtual` pattern.
- Search functionality — `useSearch` hook for in-document search.
- Note: "These patterns are not required for the base skill. Add only if a template or document specifically needs them."

---

## III. Quality Gates for the Unified Document Itself

Before the document is declared complete, verify:

1. **Every claim in Part 2 maps to a finding in Part 1.** Cross-reference check: each §2–§16 improvement must cite its originating finding number (e.g., "This fixes Finding 4.3 from Part 1").
2. **No finding in Part 1 is left unaddressed.** All 20 findings must have a corresponding fix in Part 2 or an explicit "Won't fix — out of scope" with justification.
3. **Evidence contract is applied to the skill document itself.** Every non-trivial claim in the unified skill carries a confidence tag.
4. **Code snippets are syntactically valid TypeScript.** No unclosed braces, no undefined variables, no hallucinated APIs.
5. **No placeholder values.** Every token, color, version number, and file path is concrete and correct.
6. **No contradictions.** The document must not claim "WCAG AAA" while documenting AAA failures. The honest "AA + AAA aspirational" framing is used throughout.
7. **Length check:** Target 2,000–2,200 lines. If exceeding 2,400, trim Appendix E and condense §7 template descriptions.
8. **Self-check against Definition of Done (from coding agent instructions):**
   - Every part of the request addressed? Yes — unified skill file.
   - Syntactically valid? Yes — markdown with TypeScript code blocks.
   - No secrets, placeholders, commented-out code? Yes.
   - All claims backed by evidence or labeled? Yes — §16 applied.
   - Relevant documentation updated? N/A — this IS the documentation.
   - Final artifact in correct location? Yes — `/mnt/agents/output/markdown-to-web_SKILL.md`.

---

## IV. Implementation Order

If confirmed, I will produce the document in this sequence:

**Phase 1: Skeleton & Front Matter** (~15 min)
1. YAML front matter block
2. Part 1 heading structure with all 20 findings as section stubs
3. Part 2 heading structure with all §1–§16 as section stubs
4. Appendix heading structure

**Phase 2: Part 1 — Validation Review** (~30 min)
5. Executive Summary (severity table)
6. Methodology paragraph
7. All 20 findings (copy from draft_z, verify no drift)
8. Cross-cutting observations
9. Reuse value assessment table

**Phase 3: Part 2 — Core Specification** (~60 min)
10. §1–§3 (Identity, When to Use, Inputs)
11. §4–§5 (Tech Stack, Project Skeleton)
12. §6–§7 (Design System, Three Templates)
13. §8–§9 (Tag Registry, TOC Engine)
14. §10 (Accessibility — most critical section)
15. §11 (Build Recipes)
16. §12–§16 (Anti-patterns, Pre-ship, Debugging, Extending, Evidence Contract)

**Phase 4: Appendices** (~30 min)
17. Appendix A (Migration)
18. Appendix B (TypeScript Reference)
19. Appendix C (Testing Fixtures — adapted from draft_q2, React-only)
20. Appendix D (CI/CD Workflow — adapted from draft_q2)
21. Appendix E (Advanced Patterns — condensed)

**Phase 5: Cross-Reference Verification** (~15 min)
22. Verify every Part 1 finding has a Part 2 fix
23. Verify evidence contract tags on all non-trivial claims
24. Verify no placeholder values
25. Verify line count target
26. Save to `/mnt/agents/output/markdown-to-web_SKILL.md`

**Estimated total:** ~2.5 hours of focused composition.

---

## V. Explicit Assumptions

1. The user wants a single markdown file, not a zip archive or multi-file project.
2. The unified skill replaces all five source documents; no backward compatibility with v1.0.1 naming is required beyond Appendix A.
3. Version numbering: v2.1.0 (not v2.0.0) to indicate this is an iteration beyond draft_z's v2.0.0 spec.
4. The skill file itself does not need to be buildable or runnable — it is documentation. Code snippets within it are illustrative but should be syntactically valid.
5. Chinese language support is not required in this iteration (the user's past conversations show occasional Chinese, but the skill file is English-first).

---

## VI. Confirmation Request

**Please confirm the following before I proceed to implementation:**

1. ✅ **Adopt the two-part structure** (Part 1: Validation Review + Part 2: Unified Spec + Appendices)?
2. ✅ **Use draft_z as the canonical base** with selective merges from other drafts?
3. ✅ **Drop multi-framework adapters and AST-based processing** as over-engineered?
4. ✅ **Target ~2,000–2,200 lines** for the final document?
5. ✅ **Version as v2.1.0**?
6. ✅ **Save to `/mnt/agents/output/markdown-to-web_SKILL.md`**?
7. Any **specific additions, removals, or modifications** to the plan above?

Awaiting your go-ahead to begin Phase 1.
