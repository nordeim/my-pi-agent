---
name: verification-and-review-protocol
description: "Governs the protocol for receiving feedback, requesting subagent reviews, and enforcing verification gates. Contains the 'Iron Law' preventing false completion claims. Use when receiving PR feedback, finishing tasks, or before claiming work is 'done'."
version: 2.0.0
---

# Verification & Review Protocol

## Overview

Guide proper code review practices emphasizing technical rigor, evidence-based claims, and verification over performative responses.

Code review requires three distinct practices:

1. **Receiving feedback** - Technical evaluation over performative agreement
2. **Requesting reviews** - Systematic review via code-reviewer subagent
3. **Verification gates** - Evidence before any completion claims

Each practice has specific triggers and protocols detailed in reference files.

## Core Principle

**Technical correctness over social comfort.** Verify before implementing. Ask before assuming. Evidence before claims.

## When to Use This Skill

### Receiving Feedback
Trigger when:
- Receiving code review comments from any source
- Feedback seems unclear or technically questionable
- Multiple review items need prioritization
- External reviewer lacks full context
- Suggestion conflicts with existing decisions

**Reference:** `references/code-review-reception.md`

### Requesting Review
Trigger when:
- Completing tasks in subagent-driven development (after EACH task)
- Finishing major features or refactor
- Before merging to main branch
- Stuck and need fresh perspective
- After fixing complex bugs

**Reference:** `references/requesting-code-review.md`

### Verification Gates
Trigger when:
- About to claim tests pass, build succeeds, or work is complete
- Before committing, pushing, or creating PRs
- Moving to next task
- Any statement suggesting success/completion
- Expressing satisfaction with work

**Reference:** `references/verification-before-completion.md`

## Quick Decision Tree

```
SITUATION?
│
├─ Received feedback
│  ├─ Unclear items? → STOP, ask for clarification first
│  ├─ From human partner? → Understand, then implement
│  └─ From external reviewer? → Verify technically before implementing
│
├─ Completed work
│  ├─ Major feature/task? → Request code-reviewer subagent review
│  └─ Before merge? → Request code-reviewer subagent review
│
└─ About to claim status
   ├─ Have fresh verification? → State claim WITH evidence
   └─ No fresh verification? → RUN verification command first
```

## Receiving Feedback Protocol

### Response Pattern
READ → UNDERSTAND → VERIFY → EVALUATE → RESPOND → IMPLEMENT

### Key Rules
- ❌ **No performative agreement:** Never say "You're absolutely right!", "Great point!", "Thanks for catching that."
- ❌ **No implementation before verification:** Do not blindly apply suggestions.
- ✅ **Push back with technical reasoning:** If a suggestion is wrong, state why using engineering principles.
- ✅ **YAGNI check:** `grep` for usage before implementing suggested "proper" features that aren't currently needed.

### Source Handling
- **Human Partner:** Trusted. Implement after understanding. No performative fluff.
- **External/AI Reviewer:** Verify technically correct, check for breakage, push back if it violates `code-quality-standards`.

**Full protocol:** `references/code-review-reception.md`

## Requesting Review Protocol

### When to Request
- After each task in subagent-driven development
- After major feature completion
- Before merge to main

### Process
1. Get git SHAs: `BASE_SHA=$(git rev-parse HEAD~1)` and `HEAD_SHA=$(git rev-parse HEAD)`
2. Dispatch `code-reviewer` subagent via Task tool with:
   - `WHAT_WAS_IMPLEMENTED`: Summary of changes
   - `PLAN_OR_REQUIREMENTS`: What the code should do
   - `BASE_SHA`, `HEAD_SHA`: Diff range
   - `DESCRIPTION`: Context for the review
3. Act on feedback:
   - **Critical:** Fix immediately before proceeding
   - **Important:** Fix before merge
   - **Minor:** Note for later, document in PR comments

**Full protocol:** `references/requesting-code-review.md`

## Verification Gates Protocol

### The Iron Law
**🔴 THE IRON LAW: NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE.**

### Gate Function
`IDENTIFY command` → `RUN full command` → `READ output` → `VERIFY confirms claim` → `THEN claim`

*Skipping any step is lying, not verifying.*

### Requirements for Claims
- **Tests pass:** Terminal output explicitly shows 0 failures.
- **Build succeeds:** Build command exits with code 0.
- **Bug fixed:** A regression test targeting the original symptom passes.
- **UI works:** Visual verification or Playwright/Cypress test passes.

### Red Flags (STOP IMMEDIATELY)
- Using words like "should", "probably", "seems to".
- Expressing satisfaction ("Looks good to me") before running verification.
- Committing or pushing without verification.
- Trusting another agent's report without reading the raw logs yourself.

**Full protocol:** `references/verification-before-completion.md`

## Integration with Workflows

- **Subagent-Driven:** Review after EACH task, verify before moving to next
- **Pull Requests:** Verify tests pass, request code-reviewer review before merge
- **General:** Apply verification gates before any status claims, push back on invalid feedback

## Integration with Other Skills

- **`code-quality-standards`**: The quality constitution — six axes of review criteria
- **`code-review-and-audit`**: The orchestrator — dispatches this skill for Phase 6 expert review
- **`code-review-checklist`**: Quick-reference tactical checklist for Phase 3

## Bottom Line

1. **Technical rigor over social performance** — No performative agreement
2. **Systematic review processes** — Use code-reviewer subagent
3. **Evidence before claims** — Verification gates always

**Verify. Question. Then implement. Evidence. Then claim.**
