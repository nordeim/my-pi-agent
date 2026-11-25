---
name: coding-agent
slug: code
version: 1.0.4
homepage: https://clawic.com/skills/code
description: Coding workflow with planning, implementation, verification, and testing for clean software development.
changelog: Improved description for better discoverability
metadata: {"clawdbot":{"emoji":"💻","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---

## When to Use

User explicitly requests code implementation. Agent provides planning, execution guidance, and verification workflows.

## Architecture

User preferences stored in `~/code/` when user explicitly requests.

```
~/code/
  - memory.md    # User-provided preferences only
```

Create on first use: `mkdir -p ~/code`

## Quick Reference

| Topic | File |
|-------|------|
| Memory setup | `memory-template.md` |
| Task breakdown | `planning.md` |
| Execution flow | `execution.md` |
| Verification | `verification.md` |
| Multi-task state | `state.md` |
| User criteria | `criteria.md` |

## Scope

This skill ONLY:
- Provides coding workflow guidance
- Stores preferences user explicitly provides in `~/code/`
- Reads included reference files

This skill NEVER:
- Executes code automatically
- Makes network requests
- Accesses files outside `~/code/` and the user's project
- Modifies its own SKILL.md or auxiliary files
- Takes autonomous action without user awareness

## Core Rules

### 1. Check Memory First
Read `~/code/memory.md` for user's stated preferences if it exists.

### 2. User Controls Execution
- This skill provides GUIDANCE, not autonomous execution
- User decides when to proceed to next step
- Sub-agent delegation requires user's explicit request

### 3. Plan Before Code
- Break requests into testable steps
- Each step independently verifiable
- See `planning.md` for patterns

### 4. Verify Everything
| After | Do |
|-------|-----|
| Each function | Suggest running tests |
| UI changes | Suggest taking screenshot |
| Before delivery | Suggest full test suite |

### 5. Store Preferences on Request
| User says | Action |
|-----------|--------|
| "Remember I prefer X" | Add to memory.md |
| "Never do Y again" | Add to memory.md Never section |

Only store what user explicitly asks to save.

## Workflow

```
Request -> Plan -> Execute -> Verify -> Deliver
```

## Common Traps

- **Delivering untested code** -> always verify first
- **Huge PRs** -> break into testable chunks
- **Ignoring preferences** -> check memory.md first

## Self-Modification

This skill NEVER modifies its own SKILL.md or auxiliary files.
User data stored only in `~/code/memory.md` after explicit request.

## External Endpoints

This skill makes NO network requests.

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| None | None | N/A |

## Security & Privacy

**Data that stays local:**
- Only preferences user explicitly asks to save
- Stored in `~/code/memory.md`

**Data that leaves your machine:**
- None. This skill makes no network requests.

**This skill does NOT:**
- Execute code automatically
- Access network or external services  
- Access files outside `~/code/` and user's project
- Take autonomous actions without user awareness
- Delegate to sub-agents without user's explicit request

---

## Cross-References

| Skill | When to use it together |
|---|---|
| [`../tdd-workflow/`](../tdd-workflow/SKILL.md) | Red → Green → Refactor → Commit cycle. One cycle per commit. For bugs: write failing regression test first, then fix. |
| [`../test-driven-development/`](../test-driven-development/SKILL.md) | Broader TDD methodology and test-first thinking patterns. |
| [`../code-review-and-audit/`](../code-review-and-audit/SKILL.md) | Pre-merge code review checklist and audit patterns. |
| [`../code-quality-standards/`](../code-quality-standards/SKILL.md) | Language-specific quality bar (TypeScript strict, no `any`, early returns, composition over inheritance). |
| [`../clean-code/`](../clean-code/SKILL.md) | Refactoring patterns for reducing complexity — extract function, rename, inline, etc. |
| [`../debugging-and-error-recovery/`](../debugging-and-error-recovery/SKILL.md) | Systematic diagnosis: symptoms → potential causes → root cause → solution → validation. |
| [`../incremental-implementation/`](../incremental-implementation/SKILL.md) | Small-step delivery: each step leaves the codebase in a working state. |
| [`../planning-and-task-breakdown/`](../planning-and-task-breakdown/SKILL.md) | Multi-step task decomposition with verifiable checkpoints. |
| [`../verification-and-review-protocol/`](../verification-and-review-protocol/SKILL.md) | QA gate before delivery — success criteria, edge cases, accessibility, performance. |

### Shared best practices (apply across all coding-workflow skills)

- **State file discipline**: The `state.md` file is the single source of truth for session progress. Update it after every meaningful step, not at the end. A stale state file is worse than no state file.
- **Planning before coding**: Read `planning.md` and produce a written plan before writing any code. The plan is a commitment device — it forces you to confront unknowns before they become bugs.
- **Verification is not optional**: "It compiles" is never sufficient evidence of completion. Browser-verified interactivity (for web) or test-verified behavior (for libraries) is the required standard of done.
- **Criteria-driven work**: Read `criteria.md` at the start of every task. If success criteria are ambiguous, ask the user before coding. Ambiguous criteria guarantee rework.
- **Memory file for cross-session continuity**: Use `memory-template.md` to record decisions, rationale, and gotchas. This is how a coding agent becomes more effective over time rather than resetting each session.
