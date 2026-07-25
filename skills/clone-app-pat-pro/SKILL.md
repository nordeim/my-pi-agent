---
name: clone-app-pat-pro
description: Clones any web app pixel-for-pixel from a URL. Runs as an IN-CONVERSATION workflow — the live Claude orchestrates Task sub-agents and drives the Claude Chrome extension to recon (every view), extract (computed styles = ground truth), design-spec, build, QA (computed-style assertions), and extend. Guided check-ins, custom features, and an MCP server so an agent can operate the app. Use when cloning a site, replicating a web app, building a clone, copying a website, recreating a UI, or when told "clone this", "replicate this app", "copy this site", "build a clone of", "make a copy of this website", "recreate this UI".
argument-hint: <url> <name>
allowed-tools: Bash, Read, Write, Edit, Agent
---

# Clone App — Pat Pro

Mission: **own the target, pixel for pixel.** Read every value off the live page (never a screenshot guess), rebuild it, prove the match with measured computed-style assertions, then make it yours.

> **The contract is law.** [`references/00-contract.md`](references/00-contract.md) defines the workspace layout, exact artifact filenames, stage I/O, the verification gate, the convergence loop, and the agent-prompt standard. Read it first.

## How this runs — IN-CONVERSATION (read first)

This skill runs as a **workflow inside a live Claude session**, not a background script. When it's invoked, **YOU (the in-session agent) orchestrate it**: spawn Task sub-agents, drive the browser, check in with the user, run the helper scripts.

**Browser tool = the Claude Chrome extension, only** (`mcp__claude-in-chrome__*`). You're already logged in, so it reaches authed sites. There is one Chrome — **one view/tab at a time** (browser stages are sequential). **Code stages fan out in parallel** via Task sub-agents (build each page, fix each file-set concurrently).

| Need | Chrome-extension tool |
|---|---|
| open a route | `mcp__claude-in-chrome__navigate` |
| read computed styles / CSSOM / run JS | `mcp__claude-in-chrome__javascript_tool` (the verification ground truth) |
| read DOM / find elements | `mcp__claude-in-chrome__read_page` / `find` |
| click / hover / focus (interaction sweep) | `mcp__claude-in-chrome__computer` |
| visual reference screenshot | `mcp__claude-in-chrome__computer` (`screenshot`) |
| set viewport | `mcp__claude-in-chrome__resize_window` |

**Screenshots are a VISUAL REFERENCE only.** The extension can't reliably write screenshot files to disk in this environment, so **do not build the gate on saved PNGs / pixel-diff.** Screenshots are for you and the user to eyeball the real site vs the clone. The **objective ground truth is computed styles** read via `javascript_tool` (the contract's own rule: CSSOM/computed values beat screenshots).

**The gate = computed-style assertions.** QA reads the clone's computed styles via `javascript_tool`, writes them to JSON, and `scripts/assert-styles.mjs` compares them to the design tokens (`assertions.json` from the DESIGN.md). PASS = 0 style-assertion failures + the build compiles. Plus a visual eyeball of clone vs real site.

## ⛔ STOP-AND-CHECK-IN GATE — after EVERY stage (the rule agents break)

This is the single most important rule, and the one that gets ignored: **after each stage you MUST stop, report, and WAIT for the user before doing anything else.** Do not "batch through" the pipeline.

After every stage — recon, extraction, design spec, architecture, build-foundation, build-pages, **each** QA cycle, polish, **each** feature, agent-access:
1. Post a short summary of what the stage produced + the exact artifact paths (for visual stages, name the views/screenshots you captured).
2. Ask the user: **approve / revise / stop.**
3. **STOP. Do not call ANY tool. Do not start the next stage. Wait for the user's reply.**

Running stage N+1 before the user has responded to stage N is a **failure**. One stage → stop → wait, every single time. Recon is ONE stage: capture every view, then STOP and check in — do **not** roll straight into extraction. Same for every other stage.

### What "EVERY VIEW" means (recon is not one screenshot)

Recon must reach **every state the app can show** — exhaustive, not a sample. Navigate and capture/extract:
- **every left-hand sidebar item** (click each, go into its view);
- **every tab / top filter** (Active / Backlog / All / …);
- **every filter and layout toggle** (board ↔ list ↔ every layout; sort/group);
- **every menu, dropdown, context menu** (open state);
- **every side panel, detail, modal** (open an issue, settings panels, slide-overs);
- **every interaction-revealed state** (focus the editor → its toolbar; the comment composer; hover states);
- at **every viewport** (desktop, tablet, mobile).

For each view: read its computed styles via `javascript_tool` (the data that matters) and take a visual-reference screenshot. Log each in `interaction-map.json` (contract §8). One view captured = broken recon — keep going.

## Pipeline

```
Recon (EVERY view — Chrome ext, computed styles + visual ref, sequential) → Extraction (per view)
→ Design Spec (DESIGN.md + assertions.json) → Architecture → Build-foundation → Build-pages (‖ Task agents)
→ [QA (read clone computed styles → assert-styles gate) → Fix (‖ Task agents)] loop-until-converged
→ Polish → [guided] Customize (feature loop) → Agent access (API + MCP server)
```

Gate (contract §5): **0 style-assertion failures + build compiles**, plus a visual check. Loop QA↔Fix until it passes, stalls, or hits a hard blocker.

## Stages

| # | Stage | Browser | Parallel | Reference |
|---|-------|---------|----------|-----------|
| 1 | Recon | Chrome ext, every view | sequential | [01-recon.md](references/01-recon.md) |
| 2 | Extraction | Chrome ext (`javascript_tool`) | sequential | [02-extraction.md](references/02-extraction.md) |
| 3 | Design Spec | no | single (fan-in) | [03-design-spec.md](references/03-design-spec.md) |
| 4 | Architecture | no | single | [04-architecture.md](references/04-architecture.md) |
| 5a | Build-foundation | no | single | [05-build.md](references/05-build.md) |
| 5b | Build-page | no | ‖ Task agents | [05-build.md](references/05-build.md) |
| 6 | QA | Chrome ext (read clone styles) | sequential read, ‖ analysis | [06-qa.md](references/06-qa.md) |
| 7 | Fix | no | ‖ Task agents per file-set | [06-qa.md](references/06-qa.md) |
| 9 | Polish | Chrome ext (clone) | sequential | [07-polish.md](references/07-polish.md) |
| 10-11 | Extend (guided) | mixed | — | [08-extend.md](references/08-extend.md) |

## Verification scripts (run via Bash)

- [`scripts/assert-styles.mjs`](scripts/assert-styles.mjs) — compares the clone's computed styles (JSON the QA agent reads via `javascript_tool`) to the DESIGN.md tokens/`assertions.json`. The gate.
- [`scripts/partition_bugs.py`](scripts/partition_bugs.py) — disjoint per-file fix sets for parallel fixers.

## Pat Pro Enhancements

- **In-conversation, Chrome-extension-only** — runs in your session, drives the real browser you're logged into.
- **Click everything** — recon reaches every sidebar item, tab, filter, view, panel, and state (see "EVERY VIEW" + contract §8).
- **Computed styles are ground truth** — the gate is measured style assertions, not eyeballing or fragile screenshots.
- **Autonomous convergence** — loops QA↔Fix until it passes.
- **Customize & extend** — add features matched to `DESIGN.md`, then build an MCP server so an agent can operate the app (contract §10, [08-extend.md](references/08-extend.md)).

## Workspace

All artifacts in `clone-workspace/{name}/` with fixed filenames — contract §1. Stage prompt templates (used as Task sub-agent prompts): [references/stage-prompts.md](references/stage-prompts.md).
