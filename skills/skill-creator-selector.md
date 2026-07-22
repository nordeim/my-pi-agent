---
name: skill-creator-selector
description: how to decide which skill-creator skill to choose from
---

Summary of the differences:

1. **skill-creator** - The foundational/anatomy-focused skill. It's about the structure of skills: the directory layout, file organization (`SKILL.md`, `scripts/`, `references/`, `assets/`), the progressive disclosure principle, and packaging. It's more about the "what is a skill" and "how do I structure one" — a reference/guide for skill creation.
2. **skill-creator-zai** - The full iterative development lifecycle skill. It covers the complete workflow from intent capture → interview → draft → test case creation → parallel subagent runs (with-skill vs baseline) → eval viewer → feedback loop → iteration → description optimization → packaging. It's much more process-oriented, with specific tools and scripts for the development loop.
3. **task-review** - A lightweight automatic skill extraction skill. It runs at the end of complex tasks to check if the task path is worth saving as a new skill. It's automatic/simple — just checks if a task was complex enough and saves the experience. It's in Chinese.

### Key differences:
- **skill-creator**: Reference/structural — teaches the anatomy of a skill, the file structure, and how to organize resources. More of a design document. No eval or iteration workflow.
- **skill-creator-zai**: Full development pipeline — intent → draft → test → eval → iterate → optimize → package. Has scripts for running eval comparisons, generating review viewers, and optimizing descriptions. Much more comprehensive and process-heavy.
- **task-review**: Automatic post-hoc extraction — runs silently after complex tasks to save the experience as a skill. Very lightweight, no testing or iteration.

---

Here are three related skills, each with its own distinct positioning and depth:

### 1. skill-creator — Skill Structure Reference Guide

**Positioning:** An "anatomical" reference for skills. It teaches you how to organize a skill's directory structure, file layout, and content principles.

**Core Content:**
- Skill directory structure (`SKILL.md` + `scripts/`, `references/`, `assets/`)
- Progressive Disclosure principle: three-tier loading via metadata → body → resources
- Skill writing standards (YAML frontmatter, description writing, line count limits)
- When to use scripts vs. references vs. assets
- Packaging tool `package_skill.py`

**No evaluation/iteration workflow** — It does not involve test cases or require running sub-agents for comparative evaluation. It is more akin to a design document.

**Use Case:** When you want to understand "what a skill should look like," or need a reference for the correct file structure of a skill.

---

### 2. skill-creator-zai — Complete Skill Development Workflow

**Positioning:** A complete pipeline for creating and refining a skill from scratch (0 to 1). Much deeper than `skill-creator`.

**Core Workflow (Strictly Sequential):**
1. **Intent Capture & Interview** — Clarify the skill's goals, trigger conditions, and output formats.
2. **Draft `SKILL.md`** — Write it according to the standards.
3. **Write Test Cases** — Save to `evals/evals.json`.
4. **Run Parallel Evaluations** — Launch two sub-agents simultaneously: with-skill vs. without-skill (baseline), to compare the results.
5. **Qualitative + Quantitative Assessment** — Use `eval-viewer/generate_review.py` to generate an evaluation viewer, allowing users to provide feedback directly in the browser.
6. **Iteration Loop** — Improve based on feedback → re-run evaluations → repeat until the user is satisfied.
7. **Description Optimization** — Use `run_loop.py` to automatically optimize the trigger descriptions.
8. **Package and Deliver**

**Key Technologies:**
- Sub-agent parallel testing (with-skill vs. baseline)
- Structured assertions (`grading.json`)
- Quantitative benchmark aggregation (`aggregate_benchmark.py`)
- Blind comparative analysis (`comparator.md` / `analyzer.md`)
- Description trigger rate optimization (trigger/don't-trigger test sets, automatic iterative optimization)

**Use Case:** When you want to create a high-quality skill from scratch, or significantly improve an existing one, requiring a rigorous testing, evaluation, and iteration workflow. Requires sub-agent support.

---

### 3. task-review — Lightweight Automatic Skill Extraction

**Positioning:** Automatically checks after the completion of every complex task to see if the execution path is worth preserving as a skill. Completely passively triggered, requiring no active request from the user.

**Trigger Conditions:** Triggered when the task meets any of the following conditions:
- Made 5 or more tool calls
- Encountered errors during execution and found the correct path
- The task contains 3 or more distinct steps

**Behavior:**
- Determines if the task is reusable → If so, automatically generates or updates `SKILL.md` under `skills/`
- Quietly adds a note at the end of the response: "This experience has been consolidated into a new skill: [xxx]"

**No testing, no iteration, no evaluation** — It simply records the execution path for future reuse.

**Use Case:** When you are doing a complex coding task and want to save the pitfalls encountered and the workflow for future reference.

---

## Comparison Summary

| Dimension | skill-creator | skill-creator-zai | task-review |
| :--- | :--- | :--- | :--- |
| **Purpose** | Educational reference | Complete development pipeline | Automatic experience preservation |
| **Trigger Method** | Actively invoked by user | Actively invoked by user | Automatically after task completion |
| **Has Test Cases?** | ❌ | ✅ (Parallel sub-agent comparison) | ❌ |
| **Has Quantitative Evaluation?** | ❌ | ✅ (Benchmark, grading, blind comparison) | ❌ |
| **Has Iteration Loop?** | ❌ | ✅ (Feedback → Improvement → Retest) | ❌ |
| **Has Description Optimization?** | ❌ | ✅ (Trigger rate optimization) | ❌ |
| **Complexity** | Low | High | Extremely Low |
| **Best Use Case** | Learning skill structure | Refining high-quality skills from scratch | Saving experiences at the end of a task |

---

**TL;DR:** Use `skill-creator` to learn skill structure, `skill-creator-zai` to craft high-quality skills, and `task-review` to effortlessly save the experience from complex tasks.
