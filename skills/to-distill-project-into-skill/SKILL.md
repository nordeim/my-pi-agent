---
name: to-distill-project-into-skill
description: >
  Meta-skill for distilling a complete project codebase into a comprehensive,
  maintainable SKILL.md document. Use after a major project update, when
  onboarding a new team, or when you need to create a single-source-of-truth
  reference for future AI coding agents working on this codebase.
version: 1.0.0
tags:
  - documentation
  - knowledge-distillation
  - skill-generation
  - codebase-onboarding
  - meta-skill
  - agent-guidance
---

# Distill Project Into Skill — Meta-SKILL

> **Purpose:** Guide any coding agent to produce a comprehensive, production-grade `SKILL.md` for modern **web application** codebases (React, Vue, Svelte, Angular, etc.) by following a structured, six-phase validation and distillation process.
>
> **When to use:** After completing a major project update, security remediation, architectural overhaul, or whenever the codebase has accumulated enough hard-won knowledge that a single reference document would prevent repeated mistakes.
>
> **Output:** A `PROJECT_NAME_SKILL.md` file (or updated version) containing every design decision, anti-pattern, debugging procedure, and lesson learned that a future agent needs to work effectively with the codebase.

---

## Table of Contents

1. [Preconditions & Scope](#1-preconditions--scope)
2. [The Six-Phase Distillation Process](#2-the-six-phase-distillation-process)
3. [Section Specifications](#3-section-specifications)
4. [Validation Checklist](#4-validation-checklist)
5. [Anti-Patterns for SKILL.md Authors](#5-anti-patterns-for-skillmd-authors)
6. [Skill Maintenance & Evolution](#6-skill-maintenance-and-evolution)
7. [Appendix: Example Section Templates](#7-appendix-example-section-templates)

---

## 1. Preconditions & Scope

### 1.1 When This Meta-SKILL Applies

| Scenario | Trigger |
|---|---|
| **Post-sprint documentation** | Just closed a sprint with fixes, refactors, or new features |
| **Post-audit hardening** | Completed a security audit, code review, or compliance sprint |
| **Team onboarding** | New developers or AI agents need to understand the codebase |
| **Version bump** | Major dependency upgrade (e.g., Next.js 15 → 16) that changes patterns |
| **Architecture drift** | Code and docs have diverged; the SKILL.md no longer reflects reality |

### 1.2 What You Need Before Starting

- [ ] Access to the full codebase (read permissions on all source files)
- [ ] Ability to run the project's test suite (`pnpm test`, `npm test`, etc.)
- [ ] Ability to run the build (`pnpm build`, `npm run build`, etc.)
- [ ] Access to existing documentation (`README.md`, `AGENTS.md`, `CLAUDE.md`, PRD, ADR docs)
- [ ] (Optional) Access to CI/CD logs, deployment runbooks, or incident post-mortems

### 1.3 What This Produces

A single `PROJECT_NAME_SKILL.md` file with roughly 1,500–2,500 lines, comprising **20 core sections + appendices**, organized as:

1. Project Identity & Design Philosophy
2. Tech Stack & Environment
3. Bootstrapping & Configuration
4. The Design System (Code-First)
5. Component Architecture & Patterns
6. Custom Hooks Deep Dive
7. Content Management & Data Ingestion
8. Accessibility (WCAG AAA) Implementation
9. Anti-Patterns & Common Bugs
10. Debugging Guide
11. Pre-Ship Checklist
12. Lessons Learnt & How to Avoid Them
13. Pitfalls to Avoid
14. Best Practices
15. Coding Patterns
16. Coding Anti-Patterns
17. Responsive Breakpoint Reference
18. Z-Index Layer Map
19. Color Reference (Complete)
20. The Complete TypeScript Interface Reference
21. Appendices (ADRs, pipeline costs, audit history, live-site validation)

---

## 2. The Six-Phase Distillation Process

All SKILL.md creation follows this exact workflow. Do not skip phases.

### Phase 1: ANALYZE — Deep Codebase Archaeology

**Goal:** Understand the codebase at a structural and philosophical level before writing anything.

**Tasks:**
1. Read `README.md`, `AGENTS.md`, `CLAUDE.md`, or any existing project docs
2. Read `package.json` / `Cargo.toml` / `pyproject.toml` — extract all dependencies and scripts
3. Read configuration files: `tsconfig.json`, `next.config.ts`, `eslint.config.*`, `vitest.config.*`, `next.config.ts`, `postcss.config.*`
4. Read `.env.example` or the env validation schema (Zod, Joi, etc.)
5. Map the directory structure: `find src -type f | head -100`
6. Identify the framework and version (e.g., "Next.js 16 App Router, not Pages Router")
7. Determine the rendering strategy: static, dynamic, hybrid, edge, etc.
8. Identify the data layer: Drizzle, Prisma, raw SQL, Firebase, etc.
9. Identify the auth layer: Auth.js, Clerk, Firebase Auth, custom JWT, etc.
10. Identify the deployment target: Vercel, AWS, Docker, etc.

**Deliverable:** A one-paragraph "Project Identity" summary and a table of locked versions.

### Phase 2: PLAN — Structured Outline

**Goal:** Create a detailed outline before writing any prose.

**Tasks:**
1. Map each of the 20 sections to actual files in the codebase
2. Identify which sections have **code-specific** content (e.g., §4 Design System maps to `globals.css`) vs. **knowledge-specific** content (e.g., §12 Lessons maps to git history, PR comments, incident docs)
3. For code-specific sections, plan which file(s) to read for each subsection
4. For knowledge-specific sections, plan which issues/PRs/conversations to reference
5. Identify **gaps** — sections where the codebase has implicit knowledge not yet documented anywhere

**Deliverable:** A numbered checklist like the example below.

```
§1  Design Philosophy → Read: README.md, PRD.md, marketing spec
§2  Tech Stack → Read: package.json, root configs
§3  Bootstrapping → Read: package.json scripts, Dockerfile, CI workflows
§4  Design System → Read: globals.css, tailwind.config.*, any @theme block
§5  Components → Read: src/components/**, count client vs server components
§6  Hooks → Read: src/lib/hooks/** or src/hooks/**
§7  Content → Read: src/lib/data/**, CMS config, API integrations
§8  A11y → Read: globals.css (focus styles), components for aria patterns
§9  Anti-Patterns → Synthesize from §10's Issues + git blame on hot files
§10 Debugging → Read: existing issues, error logs, troubleshooting runbooks
§11 Pre-Ship → Read: CI workflows, .husky/pre-commit, package.json scripts
§12 Lessons → Synthesize from git log, PR descriptions, incident post-mortems
§13 Pitfalls → Synthesize from §9 + §12
§14 Best Practices → Synthesize from codebase conventions + lint rules
§15 Patterns → Read: representative files from each feature module
§16 Anti-Patterns → Inverse of §15; read for "don't do this" examples
§17 Breakpoints → Read: tailwind config or media query usage
§18 Z-Index → Read: all z-* class usage, portal components
§19 Colors → Read: globals.css @theme, any design token files
§20 Interfaces → Read: src/types/**, schema definitions, API types
Appendices → Read: ADR docs, architecture diagrams, runbooks
```

### Phase 3: VALIDATE — Explicit Confirmation

**Goal:** Before writing, confirm the plan with the user or your own understanding.

**Tasks:**
1. Summarize the Phase 1 findings in 3–5 sentences
2. Present the Phase 2 outline
3. Highlight any **gaps** where information is missing or ambiguous
4. Ask: "Does this plan cover everything a future agent would need?" (if user is present)
5. If no user, validate against the codebase: can every section be populated with real content?

**Deliverable:** A brief confirmation document. If gaps exist, list them explicitly.

### Phase 4: IMPLEMENT — Modular, Section-by-Section Writing

**Goal:** Write the SKILL.md section by section, validating each against the codebase before moving on.

**Rules:**
- Write **one section at a time**, never the whole document at once
- For each code-specific section, **read the actual source files** before writing
- For each knowledge-specific section, **synthesize from multiple sources** — never fabricate
- Every claim must be **verifiable** by reading a specific file or running a specific command
- Use `interface` for object shapes, `type` for unions/intersections
- Include **exact versions**, not ranges (e.g., `"next": "16.2.0"`, not `"next": "^16.x"`)
- Include **file paths** for every code reference (e.g., `src/lib/env/index.ts`)
- Include **line counts** or **file sizes** where useful for context

**Critical sub-tasks:**

#### 4.1 Verify Test Counts

```bash
# Get exact counts from the test runner
pnpm test 2>&1 | grep -E "(Test Files|Tests|passed|failed)"
# or
npm test -- --reporter=dot 2>&1 | tail -5
```

Record: unit test count (files + total), E2E test count (specs + total), and whether they're all green.

#### 4.2 Verify Key Files Exist

```bash
# Verify critical infrastructure files
ls src/lib/env/index.ts
ls src/app/globals.css
ls next.config.*
ls tsconfig.json
```

#### 4.3 Extract Design Tokens

```bash
# Extract @theme block from globals.css
grep -A 50 "@theme" src/app/globals.css | head -60
```

#### 4.4 Count Components

```bash
# Count client vs server components

grep -r "'use client'" src/components --include="*.tsx" | wc -l
grep -rL "'use client'" src/components --include="*.tsx" | wc -l
```

#### 4.5 Map the 5-Layer Architecture (or equivalent)

Identify the project's architectural layers and verify imports respect the boundaries.

### Phase 5: VERIFY — Rigorous QA

**Goal:** Ensure the SKILL.md is factually correct, complete, and useful.

**Checklist (run in order):**

- [ ] Every version number matches `package.json`
- [ ] Every env var count matches `.env.example` or the env schema
- [ ] Test counts match `pnpm test` output
- [ ] Component counts match `find src/components -type f | wc -l`
- [ ] Every file path referenced exists (spot-check 10 random paths)
- [ ] Every code snippet compiles (copy into a temp file and run `tsc --noEmit`)
- [ ] Every color hex matches the actual `globals.css` `@theme` block
- [ ] No placeholder text remains (grep for "TODO", "FIXME", "placeholder", "example.com")
- [ ] The Table of Contents matches all headings exactly
- [ ] All appendices are referenced from the main body
- [ ] Line count is reasonable (1,500–3,000 lines for a mid-size project)

**Command to sanity-check the document:**

```bash
# Verify no broken internal references
grep -n "see \`" storyintovideo_SKILL.md | wc -l
grep -n "TODO\|FIXME\|placeholder" storyintovideo_SKILL.md | wc -l

# Verify consistent heading levels
awk '/^#{1,3} / {print}' storyintovideo_SKILL.md | head -30
```

### Phase 6: DELIVER — Complete Handoff

**Goal:** Present the final document with clear context.

**Deliverable:**
1. The `PROJECT_NAME_SKILL.md` file, written to disk
2. A summary of what was added vs. what existed before (if updating)
3. A list of intentional omissions (things you chose NOT to include, with rationale)
4. A brief "how to use this document" guide at the top of the file
5. (Optional) A version number and date stamp in the header

---

## 3. Section Specifications

This section prescribes the **exact content** for each of the 20 standard sections. Adapt as needed for your project's domain (e.g., mobile apps, backend services, data pipelines), but maintain the same rigor.

### §1 Project Identity & Design Philosophy

**Purpose:** Set the tone. A future agent needs to know what this project IS before they can extend it correctly.

**Required content:**
- One-sentence project description (what + who + why)
- The design thesis or aesthetic philosophy (e.g., "luxury-dark cinematic")
- Non-negotiable design rules (e.g., "no purple gradients except on example cards")
- The CTA hierarchy (if applicable)
- The anti-generic mandate (what visual clichés are explicitly rejected)

**Verification:** Does this section prevent an agent from adding generic Bootstrap-style components? If yes, it's good.

### §2 Tech Stack & Environment

**Purpose:** Prevent version drift and dependency confusion.

**Required content:**
| Column | Description |
|---|---|
| Layer | Frontend, Backend, Database, AI, etc. |
| Technology | Exact package name |
| Version | Locked version from `package.json` |
| Critical Note | Why this version matters, any gotchas |

**Verification:** Run `npm list --depth=0` or `pnpm list --depth=0` and verify every major dependency appears in the table with the correct version.

### §3 Bootstrapping & Configuration

**Purpose:** Enable rapid environment recreation.

**Required content:**
- `pnpm create next-app@...` or equivalent scaffolding command
- Dependency install commands (runtime + dev)
- Critical configuration files: `tsconfig.json`, `next.config.*`, `eslint.config.*`, `vitest.config.*`, `postcss.config.*`, `drizzle.config.*`
- Environment variable count and critical behavior (e.g., "zod env validation fails fast at boot")
- The `pnpm-workspace.yaml` or equivalent workspace configuration

**Verification:** Can a new developer follow these instructions to get a working dev environment? Test by mentally walking through each step.

### §4 The Design System (Code-First)

**Purpose:** Prevent brand color drift and design inconsistency.

**Required content:**
- The `@theme` block (or equivalent) with all tokens
- Typography hierarchy (font, weight, size, tracking per role)
- All keyframes (count, names, purposes)
- All custom `@utility` classes
- Border radius scale
- Shadow definitions

**Verification:** Compare every hex in this section against the actual CSS. A single wrong hex is a bug.

### §5 Component Architecture & Patterns

**Purpose:** Prevent architecture violations (e.g., importing DB code in client components).

**Required content:**
- The architectural layers (e.g., 5-layer model with Golden Rule)
- Component directory map with file counts and purposes
- Client vs Server component decision tree
- The `queries.ts` boundary pattern
- Auth patterns (`verifySession()` vs `auth()`)
- CTA hierarchy (if applicable)

**Verification:** Can you trace any import from a component back to its layer? If the layering rule is violated, document it as a known issue.

### §6 Custom Hooks Deep Dive

**Purpose:** Prevent hook misuse and enable correct usage.

**Required content:**
- For each custom hook: location, purpose, signature, key implementation details
- Why each detail matters (e.g., "`passive: true` prevents blocking the main thread")
- Cleanup patterns (especially for `EventSource`, `IntersectionObserver`, etc.)
- SSR safety considerations

**Verification:** Read each hook's source file and confirm the SKILL.md description is accurate.

### §7 Content Management & Data Ingestion

**Purpose:** Document where content lives and how it's structured.

**Required content:**
- Static data files (list, location, count per file)
- Locked arrays (e.g., `STYLE_CHIPS`) with regression test references
- How to add new content (procedure with all affected files)
- Why `import.meta.glob` is NOT used (if Next.js, explain the alternative)

**Verification:** Adding a new item to any array should be a 3-step process documented here. If it requires touching 5+ files, document all of them.

### §8 Accessibility (WCAG AAA) Implementation

**Purpose:** Prevent accessibility regressions.

**Required content:**
- Color contrast table (foreground, background, ratio, WCAG level)
- Focus ring specification
- Skip-to-content link pattern
- `prefers-reduced-motion` implementation
- Touch target sizes
- ARIA patterns per component

**Verification:** Run an a11y checker (e.g., axe-core, Lighthouse a11y) and confirm the claims.

### §9 Anti-Patterns & Common Bugs

**Purpose:** Document bugs that have been fixed so they don't recur.

**Required content:**
- Each anti-pattern: symptom, root cause, fix, lesson
- Severity classification (Critical/High/Medium/Low)
- Historical bugs from all remediation sprints (e.g., NF-1 through NF-6)
- Generic framework gotchas (e.g., Vitest mock hoisting, JSX in `.test.ts`)

**Verification:** Every anti-pattern should have a corresponding test or code change that prevents recurrence. If it doesn't, add one.

### §10 Debugging Guide

**Purpose:** Accelerate troubleshooting.

**Required content:**
- Build failures (error message → cause → fix)
- Runtime errors (symptom → cause → fix)
- Test failures (error → cause → fix)
- Visual/styling issues (symptom → cause → fix)
- Live-site verification commands

**Verification:** Every entry should have been encountered at least once in the project's history.

### §11 Pre-Ship Checklist

**Purpose:** Enforce quality gates.

**Required content:**
- Quality gate commands (`pnpm lint`, `pnpm typecheck`, `pnpm test`, `pnpm build`)
- CI guard details
- Pre-deployment env validation
- Post-deployment verification (smoke tests)
- Security verification checklist
- Visual verification checklist

**Verification:** Does running these commands in order actually guarantee a shippable state? Test mentally.

### §12 Lessons Learnt & How to Avoid Them

**Purpose:** Capture institutional knowledge.

**Required content:**
- Numbered lessons from 1 to N (where N depends on project history)
- Each lesson: what happened, why it mattered, how to avoid it
- Group by sprint/phase (e.g., "Sprint 3 Lessons", "Audit-v2 Lessons")
- Cross-references to specific fixes (e.g., "(T1)", "(NF-6)")

**Verification:** Every lesson should trace to a specific code change, test, or architectural decision.

### §13 Pitfalls to Avoid

**Purpose:** Prevent common mistakes.

**Required content:**
- Architecture pitfalls (e.g., "Don't put DB access in middleware")
- TypeScript pitfalls (e.g., "Don't use `any`")
- Testing pitfalls (e.g., "Don't use `vi.fn()` directly in `vi.mock()` factory")
- Design system pitfalls (e.g., "Don't use `amber-400`")
- Security pitfalls (e.g., "Don't read uncleaned user input")
- Performance pitfalls (e.g., "Don't import `@/lib/storage/r2` in client components")

**Verification:** Every pitfall should be demonstrable with a "don't do this / do this instead" code example.

### §14 Best Practices

**Purpose:** Establish conventions.

**Required content:**
- Code organization (directory structure, file naming)
- TypeScript conventions (`interface` vs `type`, `import type`)
- React/Next.js conventions (Server Components by default, named exports)
- Testing conventions (TDD, behavior over implementation)
- Database conventions (parameterized queries, migrations not push)
- Security conventions (Zod at boundaries, no `process.env.*`)
- Design conventions (brand tokens, CSS-only animation)

**Verification:** These should be enforceable by lint rules or code review. If a practice can't be enforced, document how to verify it.

### §15 Coding Patterns

**Purpose:** Provide copy-pasteable templates.

**Required content:**
- Server Action pattern (auth → validate → business → response)
- API route pattern (force-dynamic, auth, owner check)
- Domain function pattern (pure, no framework imports)
- Idempotent operation pattern (ON CONFLICT DO NOTHING + row lock)
- SSE pattern (slot management, reconnect logic)
- Webhook idempotency pattern (pre-check → side effects → INSERT)
- Env module pattern (build-context fallback)
- Source-reading test pattern

**Verification:** Every pattern should compile in the actual project without modification.

### §16 Coding Anti-Patterns

**Purpose:** Show what NOT to do, with correct alternatives.

**Required content:**
- TypeScript anti-patterns (`any` vs `unknown`, default exports)
- React anti-patterns (`<a>` vs `<Link>`, `r2.ts` in client components)
- Tailwind anti-patterns (`amber-400` vs `primary`, `tailwind.config.ts`)
- Pipeline anti-patterns (debit before insert, missing try/catch)

**Verification:** Every anti-pattern should have a corresponding test that fails if violated.

### §17 Responsive Breakpoint Reference

**Purpose:** Prevent breakpoint inconsistency.

**Required content:**
- Tailwind default breakpoints (no custom config)
- Usage patterns per section (Hero, Features, etc.)
- Mobile testing recommendations

### §18 Z-Index Layer Map

**Purpose:** Prevent z-index wars.

**Required content:**
- All z-index layers with element, location, and purpose
- Radix/shadcn portal z-index details
- Conflict resolution rules

### §19 Color Reference (Complete)

**Purpose:** Prevent color drift.

**Required content:**
- All semantic tokens (name, hex, RGB, Tailwind class, usage)
- Chart palette (if applicable)
- Opacity variants (common usage patterns)
- Forbidden colors (enforced by tests)
- The singular exception (if any)

**Verification:** Every hex in this section must EXACTLY match the `@theme` block. A single mismatch is a bug.

### §20 The Complete TypeScript Interface Reference

**Purpose:** Serve as the API contract reference.

**Required content:**
- Marketing interfaces (all from `src/types/index.ts`)
- Pipeline domain interfaces (in `src/features/*/domain/`)
- Billing interfaces (in `src/features/billing/`)
- Pipeline queries interfaces
- Auth interfaces
- SSE/Progress interfaces
- Storage interfaces
- Environment interface (all env vars with descriptions)

**Verification:** Copy-paste each interface into the actual source file and verify it compiles.

### Appendices

**Appendix A: ADRs (Architecture Decision Records)**
- Table of ADRs with decision and rationale

**Appendix B: Pipeline/Workflow Costs**
- If applicable, a table of operations with costs (credits, time, etc.)

**Appendix C: Audit History**
- For each audit: date, findings, fixes, test progression

**Appendix D: Post-Deploy Live-Site Validation**
- Smoke test scripts
- `agent-browser` E2E methodology
- What live-site testing catches that CI cannot

---

## 4. Validation Checklist

Before declaring a SKILL.md complete, verify ALL of the following:

### Accuracy
- [ ] Every version number matches `package.json` exactly
- [ ] Every test count matches `pnpm test` output
- [ ] Every file path exists (spot-check 10 random paths)
- [ ] Every hex color matches the actual CSS
- [ ] Every interface compiles in the actual project

### Completeness
- [ ] All 20 core sections are present
- [ ] Table of Contents matches all headings
- [ ] No "TODO" or "FIXME" remains
- [ ] No placeholder text ("example.com", "placeholder")
- [ ] All appendices are referenced from the main body

### Usability
- [ ] A new agent could recreate the environment from §3 alone
- [ ] A new agent could extend a component correctly from §5
- [ ] A new agent could debug a failed build from §10
- [ ] A new agent could ship safely by following §11

### Anti-Generic Quality
- [ ] No generic advice ("use TypeScript strict mode" without specific flags)
- [ ] No copy-pasted framework docs (only project-specific conventions)
- [ ] Every claim traces to an actual file, test, or command

---

## 5. Anti-Patterns for SKILL.md Authors

### §5.1 What NOT to Include

- **Generic framework tutorials** — Link to official docs instead
- **Speculative future work** — "We might switch to X" — not useful
- **Personal opinions without evidence** — "I think X is better" needs a test or metric
- **Duplicated content** — If the README covers it, reference the README
- **Placeholder version numbers** — `"next": "^16.x"` is useless; lock the exact version
- **Unverifiable claims** — Every claim must be checkable against the codebase

### §5.2 What NOT to Do

- **Don't write the whole document at once** — section by section, with verification between each
- **Don't copy from old docs without re-verifying** — code drifts
- **Don't skip the "why"** — every rule needs a rationale (e.g., "CSS-only animation for Lighthouse ≥95")
- **Don't forget the negative space** — document what you DON'T do (e.g., "no Framer Motion")
- **Don't make non-commitments** — "We might add i18n later" → just say "no i18n currently"

---

## 6. Skill Maintenance & Evolution

A SKILL.md is not "write once, read forever." It must evolve with the codebase. Without maintenance, it becomes a liability — outdated instructions that mislead more than help.

### §6.1 When to Update

| Trigger | Action |
|---|---|
| New sprint completed | Append lessons to §12; add new anti-patterns to §9 if bugs were found |
| Dependency major upgrade | Update §2 versions; document any breaking changes in §3 or §10 |
| New feature shipped | Update §5 component inventory; add any new hooks to §6; update §7 data files |
| Security audit completed | Add findings to §9; remediation steps to §10; hardening to §14 |
| Build/test pipeline changed | Update §11 pre-ship checklist; §3 bootstrapping if commands changed |
| Team member onboarding confusion | If someone asked "how do I...?", that section needs expansion |
| Sprint 3+ without update | Schedule dedicated "doc maintenance" half-day |

### §6.2 Version Numbering

Use semantic versioning for the SKILL.md itself:

```
v1.0.0  Initial release — covers MVP scope
v1.1.0  Minor — added new sections (e.g., Appendix D)
v1.1.1  Patch — corrected test counts, fixed file paths
v2.0.0  Major — dependency upgrade (e.g., Next.js 15 → 16) changed patterns
```

**Rule:** Bump the minor version on every sprint. Bump the major version on framework upgrades.

### §6.3 Drift Detection

Run this monthly to detect when the codebase has outpaced the docs:

```bash
#!/bin/bash
# skill-drift-check.sh — Add to CI or run manually

ERRORS=0

# 1. Verify test counts match
UNIT_TESTS=$(pnpm test 2>&1 | grep "Tests" | awk '{print $2}')
SKILL_UNIT=$(grep "Tests.*pass" docs/SKILL.md | head -1 | grep -oP '\d+(?=\s+unit)')
if [ "$UNIT_TESTS" != "$SKILL_UNIT" ]; then
  echo "⚠  SKILL.md claims $SKILL_UNIT unit tests; actual: $UNIT_TESTS"
  ERRORS=$((ERRORS+1))
fi

# 2. Verify no new components are unlisted
COMPONENT_COUNT=$(find src/components -name "*.tsx" | wc -l)
SKILL_COMPONENTS=$(grep -oP '\d+(?=\s+components)' docs/SKILL.md | head -1)
if [ "$COMPONENT_COUNT" != "$SKILL_COMPONENTS" ]; then
  echo "⚠  SKILL.md claims $SKILL_COMPONENTS components; actual: $COMPONENT_COUNT"
  ERRORS=$((ERRORS+1))
fi

# 3. Verify env var count matches
ENV_COUNT=$(grep -c "^env\." src/lib/env/index.ts 2>/dev/null || echo "0")
SKILL_ENV=$(grep -oP '\d+(?=\s+env vars)' docs/SKILL.md | head -1 || echo "0")
if [ "$ENV_COUNT" != "$SKILL_ENV" ]; then
  echo "⚠  SKILL.md claims $SKILL_ENV env vars; actual: $ENV_COUNT"
  ERRORS=$((ERRORS+1))
fi

# 4. Verify no TODO/FIXME remain
TODO_COUNT=$(grep -c "TODO\|FIXME" docs/SKILL.md || echo "0")
if [ "$TODO_COUNT" -gt 0 ]; then
  echo "⚠  Found $TODO_COUNT TODO/FIXME in SKILL.md"
  ERRORS=$((ERRORS+1))
fi

if [ $ERRORS -eq 0 ]; then
  echo "✅ SKILL.md drift check passed"
else
  echo "❌ Found $ERRORS discrepancy(s). Update SKILL.md."
  exit 1
fi

---

## 7. Appendix: Example Section Templates

### Template: §2 Tech Stack Table

```markdown
| Layer | Technology | Version | Critical Note |
|---|---|---|---|
| Framework | Next.js (App Router, hybrid) | `^16.2.0` | Turbopack dev; `proxy.ts` replaces `middleware.ts` |
| UI Runtime | React (strict TypeScript) | `^19.2.3` | ⚠️ CVE-2025-55182 floor — never downgrade |
| Styling | Tailwind CSS (CSS-first `@theme`) | `^4.3.0` | No `tailwind.config.ts` — all tokens in `globals.css` |
```

### Template: §9 Anti-Pattern Entry

```markdown
### Bug: [Short Name] ([Severity])

**Symptom:** [What the user sees]
**Root cause:** [Technical explanation]
**Fix:** [Link to PR or specific code change]
**Lesson:** [What to do differently next time]
```

### Template: §12 Lesson Entry

```markdown
[##]. **[Lesson title]** — [Context]

[Detailed explanation of what happened, why it mattered, and how to avoid it.
Include the specific fix references like (T1), (NF-6) if applicable.]
```

### Template: §15 Pattern Entry

```typescript
// Pattern: [Name]
// Location: [file path]
// Purpose: [single sentence]

export async function [functionName]() {
  // Step 1: [What and why]
  // Step 2: [What and why]
  // ...
}
```

---

*End of meta-skill. This document itself was produced by following the Six-Phase Distillation Process on a Next.js 16 + React 19 + Tailwind v4 + Drizzle ORM + Inngest codebase. For the resulting skill file, see `storyintovideo_SKILL.md`.*
