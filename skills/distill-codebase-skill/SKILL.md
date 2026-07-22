---
name: distill-codebase-skill
description: "Reference template for distilling codebase knowledge into a comprehensive engineering skill document. Use after completing a major project update, security remediation, or architectural overhaul to create a reusable SKILL.md that captures lessons learned, anti-patterns, debugging guides, and best practices for future agents."
---

# This is just a reference template for distilling the knowledge and expertise and experiences after completing updating a project codebase

### What Was Updated

**File**: `/home/project/onestopnews/onestopnews_SKILL.md` (2404 → 2646 lines, +242 lines of Phase 25 content)

| Section | Update | Content Added |
|---------|--------|---------------|
| **Frontmatter** | Updated | v2.0.0→v3.0.0, last_updated 6/24→6/25, project_state (525 tests, env leak guard active) |
| **§9 Anti-Patterns** | +6 entries (#59-64) | XSS JSON.stringify, race condition, composite cursor, dead code, gitignore-untrack, as-any generics |
| **§10 Debugging Guide** | +7 scenarios | XSS symptoms, OAuth duplicates, search skip, env leak CI, as-any tsc, migration failure, dead httpHeader |
| **§11 Pre-Ship Checklist** | +2 bash steps + 6 security items | env leak guard, migration check, JSON-LD escape, OAuth invariant, compound cursor, no-as-any, no-dead-code |
| **§12 Lessons Learnt** | +6 lessons (#11-16) | F1 gitignore-untrack, F2 JSON.stringify XSS, F3 race condition, F4 dead code, F5 union generics, F6 composite cursor |
| **§13 Pitfalls** | +7 security pitfalls | Phase 25-specific "don't" list |
| **§14 Best Practices** | +7 security practices | escapeForScriptContext, DB unique indexes, wrapper functions, compound cursors, CI guards, backward-compat, grep-before-delete |
| **§15 Coding Patterns** | +3 patterns with code | escapeForScriptContext, createPgAdapter wrapper, compound cursor encode/decode |
| **§20 TypeScript Interfaces** | +Phase 25 interfaces | Updated ProvenanceResult (no httpHeader), SearchParams (cursor: string), ParsedCursor, LinkResult, accounts schema with unique index |
| **Quick Reference Card** | +6 file paths | check-env-leaks.sh, SECURITY_REMEDIATION.md, migration 0007, escapeForScriptContext, createPgAdapter, compound cursor helpers |

### Validation Results (all 10 checks pass)

1. ✅ **Tech stack versions match** — Next 16.2.9, React 19.2.7, Drizzle 0.45.2, BullMQ 5.78.0, Auth 5.0.0-beta.31, TS 5.7.0, Tailwind 4.3.1
2. ✅ **Configuration files match** — next.config.ts, tsconfig.json, eslint.config.mjs, vitest.config.ts, postcss.config.mjs all verified
3. ✅ **Design system tokens match** — ink-900 #1a1a18, paper-50 #fafaf8, dispatch-ember #c7513f (verified against globals.css)
4. ✅ **Component architecture matches** — 5-layer model, feature-folder structure, queries.ts boundary
5. ✅ **Hooks implementation matches** — useReducedMotion + useDebounce verified in src/shared/hooks/
6. ✅ **Content ingestion patterns match** — RSS pipeline via parseFeed.ts, content availability guard
7. ✅ **Accessibility implementation matches** — WCAG AAA focus states, prefers-reduced-motion CSS, skip-to-content link
8. ✅ **Anti-patterns documented correctly** — 64 total (#1-64), including 6 new Phase 25 entries (#59-64)
9. ✅ **Color references match** — All 20+ design tokens verified against globals.css
10. ✅ **TypeScript interfaces match** — ProvenanceResult, SearchParams, ParsedCursor, LinkResult, accounts schema all verified against source

### Structure Coverage (all 20 requested sections present)

1. Project Identity & Design Philosophy ✅
2. Tech Stack & Environment ✅
3. Bootstrapping & Configuration ✅
4. The Design System (Code-First) ✅
5. Component Architecture & Patterns ✅
6. Custom Hooks Deep Dive ✅
7. Content Management: RSS Ingestion Pipeline ✅
8. Accessibility (WCAG AAA) Implementation ✅
9. Anti-Patterns & Common Bugs ✅ (64 entries)
10. Debugging Guide ✅
11. Pre-Ship Checklist ✅ (7 bash commands + 4 verification categories)
12. Lessons Learnt & How to Avoid Them ✅ (16 lessons)
13. Pitfalls to Avoid ✅
14. Best Practices ✅
15. Coding Patterns ✅ (with code examples)
16. Coding Anti-Patterns ✅
17. Responsive Breakpoint Reference ✅
18. Z-Index Layer Map ✅
19. Color Reference (Complete) ✅
20. The Complete TypeScript Interface Reference ✅ (with Phase 25 additions)

Plus 2 appendices: The Meticulous Approach (6-Phase Workflow) + Quick Reference Card.

The skill file is now a complete, codebase-verified engineering reference that any coding agent can use to extend, debug, onboard, or replicate the OneStopNews architecture — including all Phase 25 security and correctness remediation knowledge.

