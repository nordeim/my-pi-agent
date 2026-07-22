# to-distill-project-into-skill

> **Meta-skill for distilling a complete project codebase into a comprehensive, maintainable `SKILL.md` document.**

## Overview

This meta-skill guides any coding agent to produce a production-grade project-specific `SKILL.md` by following a structured **Six-Phase Distillation Process**:

1. **ANALYZE** — Deep codebase archaeology
2. **PLAN** — Structured 20-section outline
3. **VALIDATE** — Explicit confirmation before writing
4. **IMPLEMENT** — Section-by-section writing with verification
5. **VERIFY** — Rigorous QA against the codebase
6. **DELIVER** — Complete handoff with context

## Scope

**Optimized for:** Modern **web application** codebases (React, Vue, Svelte, Angular, etc.)

**For non-web projects:** Adapt web-specific sections (§4 Design System, §6 Hooks, §8 Accessibility, §17 Breakpoints, §18 Z-Index, §19 Colors) to your domain. Replace React/Next.js examples with your language's equivalents (Python `TypedDict`, Go `struct`, Rust `struct`/`trait`).

## Documents

| File | Purpose |
|---|---|
| `SKILL.md` (698 lines) | Full meta-skill specification: 6 phases, 20 section specs, validation checklist, anti-patterns, evolution guidance |
| `QUICKSTART.md` (117 lines) | Fast-start guide with concrete commands, time estimates (6-10h), and troubleshooting |
| `info.md` (48 lines) | Summary, stats, and actionable questions for users |
| `PLAN_21.md` | Future enhancement plan (21-section roadmap) |
| `META_SKILL_VALIDATION_REPORT.md` | Validation report from first review |
| `META_SKILL_FIXES_APPLIED.md` | Summary of fixes applied |

## Example Output

- **`storyintovideo_SKILL.md`** (v9.0, 2,041 lines): Produced for a Next.js 16 + React 19 + Tailwind v4 + Drizzle ORM + Inngest SaaS. Contains 24 dependency versions, 13 keyframes, 8 style chips, 524 test-validated claims, and 60+ documented anti-patterns. Verified 97.3% accuracy against live codebase.

## Key Features

- **Verification-first:** Every claim must be verifiable against the codebase
- **Anti-generic enforcement:** No generic framework tutorials, lock exact versions, file paths in every reference
- **Drift detection:** Built-in `skill-drift-check.sh` script for monthly validation
- **Scoped honesty:** Acknowledges web-specific assumptions, provides adaptation guidance

## Usage

```bash
# 1. Read the meta-skill
cat ~/.pi/agent/skills/to-distill-project-into-skill/SKILL.md

# 2. Quick-start if you want to jump in
cat ~/.pi/agent/skills/to-distill-project-into-skill/QUICKSTART.md

# 3. Review info before asking questions
cat ~/.pi/agent/skills/to-distill-project-into-skill/info.md
```

## Time Investment

- **Mid-size project (500-2,000 source files):** 6-10 hours
- **Per code-specific section:** 15-20 minutes
- **Per knowledge-specific section:** 10 minutes

## Maintenance

- **Bump minor version** on every sprint update
- **Bump major version** on framework upgrades
- **Run drift check monthly** to detect when codebase outpaces docs

---

*For the full specification, see `SKILL.md`.*
