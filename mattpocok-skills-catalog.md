# Skills Catalog

> **36 skills** organized into 10 categories. Each entry shows the skill name and a concise description of what it does and when to use it. This catalog mirrors the format of `/home/pete/.pi/agent/skills/skills-catalog.md` for merge compatibility with the main agent skills collection.

---

## 1. Frontend Development & UI Engineering

> Skills for building, styling, and shipping production-grade web interfaces.

| Skill | Description |
|-------|-------------|
| **prototype** | Build a throwaway prototype to answer a design question. Use when you want to sanity-check whether a state model or logic feels right, or explore what a UI should look like. Two branches: logic prototype (single shareable HTML file with free-play and guided walkthrough) and UI prototype (toggleable visual variations via URL param). |

---

## 2. Design Artifacts & Visual Creation

> Skills that produce visual artifacts, structured documents, and writing journeys.

| Skill | Description |
|-------|-------------|
| **writing-beats** | Writing, exploit: assemble raw material into a journey of beats, grounding each term before a beat leans on it. Choose-your-own-adventure flow where each beat is written one at a time and only reachable beats are offered next. |
| **writing-fragments** | Writing, explore: mine raw fragments, no structure yet. Grilling session that mines heterogeneous nuggets of writing and appends them to a single markdown file as raw material for a future article. |
| **writing-shape** | Writing, exploit: shape raw material into an article, paragraph by paragraph. Takes a markdown pile of raw material and grows the article one paragraph at a time, arguing format choices at each step. |

---

## 3. Full-Stack & Backend Development

> Skills for server-side workflows, provisioning, and backend patterns.

| Skill | Description |
|-------|-------------|
| **wizard** | Generate an interactive bash wizard that walks a human through steps only they can perform. Use when provisioning infrastructure, setting up credentials or CI secrets, walking an unfamiliar third-party dashboard, or running a one-off migration or cutover. |

---

## 4. AI / ML / Multimodal SDK Skills

> Skills that wrap LLM clients or multimodal model workflows.

| Skill | Description |
|-------|-------------|
| _No skills in this category_ | This repo does not ship LLM SDK wrapper skills. AI leverage is delivered through workflow skills (grilling, research, teaching) rather than model client bindings. |

---

## 5. Testing, QA & Performance

> Skills for test design, end-to-end testing, code review, and diagnosis.

| Skill | Description |
|-------|-------------|
| **code-review** | Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes: Standards (does the code follow this repo's documented coding standards) and Spec (does the code match what the originating issue or spec asked for). Runs both reviews in parallel sub-agents and reports them side by side. |
| **diagnosing-bugs** | Diagnosis loop for hard bugs and performance regressions. Use when you say diagnose or debug this, or report something broken, throwing, failing, or slow. Build a tight red feedback loop first, then minimise, hypothesise, instrument, fix, and add a regression test. |
| **tdd** | Test-driven development. Use when you want to build features or fix bugs test-first, mentions red-green-refactor, or wants integration tests. Tests verify behavior through public interfaces at pre-agreed seams, one slice at a time. |

---

## 6. Code Quality, Security & Architecture

> Skills for architecture decisions, module design, boundary enforcement, and refactoring.

| Skill | Description |
|-------|-------------|
| **codebase-design** | Shared vocabulary for designing deep modules. Use when you want to design or improve a module's interface, find deepening opportunities, decide where a seam goes, make code more testable or AI-navigable, or when another skill needs the deep-module vocabulary. |
| **improve-codebase-architecture** | Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick. Informed by CONTEXT.md domain language and ADRs, uses the deep module vocabulary to surface shallow modules and propose deepening refactors. |
| **migrate-to-shoehorn** | Migrate test files from `as` type assertions to @total-typescript/shoehorn. Use when you mention shoehorn, want to replace `as` in tests, or need partial test data. Replaces `as Type` with `fromPartial()` and `as unknown as Type` with `fromAny()`. |
| **resolving-merge-conflicts** | Use when you need to resolve an in-progress git merge or rebase conflict. Trace each hunk to its primary source and intent, preserve both where possible, run automated checks, and finish the operation without aborting. |
| **setup-ts-deep-modules** | Wire dependency-cruiser into a TypeScript repo so each package is a deep module, with implementation hidden in subfolders and reachable only through its entry-point files. Enforces four rules: entry-point boundary, intra-package freedom, tests through entry points, and no cycles. |

---

## 7. Planning, Workflow & Project Management

> Skills for planning work, managing projects, orchestrating sub-agents, and shipping.

| Skill | Description |
|-------|-------------|
| **ask-matt** | Ask which skill or flow fits your situation. A router over the skills in this repo that maps the main flow (idea to ship) and its on-ramps, so you do not need to remember every skill. |
| **grill-with-docs** | A relentless interview to sharpen a plan or design, which also creates docs (ADRs and glossary) as you go. The stateful variant of grilling that leaves a paper trail in CONTEXT.md and docs/adr/. |
| **grill-me** | A relentless interview to sharpen a plan or design. The stateless variant for when there is no working directory to leave docs in. Both grilling variants run the same primitive with relentless questioning and recommended answers. |
| **grilling** | Grill the user relentlessly about a plan, decision, or idea. Use when you want to stress-test thinking or you hear any grill trigger phrase. The shared primitive that powers grill-me and grill-with-docs. |
| **implement** | Implement a piece of work based on a spec or set of tickets. Drives tdd at pre-agreed seams internally and closes out with code-review before committing. |
| **implement-spec** | Implement a specification in code. Works the tickets as a task graph with blocking edges, running implementer subagents across the ready frontier for maximum concurrency and landing the result as a single PR. |
| **loop-me** | Grill me about specs for the workflows you want to build, within this workspace. Stateful grilling session whose only output is workflow specs for loops (recurring patterns in life and work). |
| **to-spec** | Turn the current conversation into a spec and publish it to the project issue tracker: no interview, just synthesis of what you already discussed. Applies the ready-for-agent triage label. |
| **to-tickets** | Break a plan, spec, or the current conversation into a set of tracer-bullet tickets, each declaring its blocking edges, published to the configured tracker. Edges become text in a file locally or native blocking links on a real tracker. |
| **triage** | Move issues and external PRs through a state machine of triage roles, categorise, verify, grill if needed, and write agent-ready briefs. Every tracker comment starts with the AI-generated disclaimer. |
| **wayfinder** | Plan a huge chunk of work (more than one agent session can hold) as a shared map of decision tickets on your issue tracker, and resolve them one at a time until the way to the destination is clear. Planning by default, not doing. |

---

## 8. Documentation & Content Creation

> Skills that produce documents, research notes, domain models, and agent-facing writing.

| Skill | Description |
|-------|-------------|
| **claude-handoff** | Hand the current conversation off to a fresh background agent that picks up the work immediately. Writes a handoff summary and launches `claude --bg --name` seeded with it, with a suggested skills section for the next agent. |
| **domain-modeling** | Build and sharpen a project's domain model. Use when discussing codebase terminology, writing or editing a CONTEXT.md, or recording or editing an ADR. Active discipline that challenges terms and writes the glossary down the moment it crystallises. |
| **handoff** | Compact the current conversation into a handoff document for another agent to pick up. Preserves hard-won context across sessions or worktrees with pointers to specs, ADRs, and issues rather than duplicated content. |
| **research** | Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo. Use when you want a topic researched, docs or API facts gathered, or reading legwork delegated to a background agent. |
| **teach** | Teach the user a new skill or concept, within this workspace. Multi-session teaching flow that uses the current directory as a stateful workspace with exercises and checkpoints. |
| **to-questionnaire** | Turn a decision you cannot fully answer into a questionnaire for someone else to fill in. Generates a markdown questionnaire with themed sections, one idea per question, and a why-this-matters note where needed. |
| **wait-what** | Stop. That last message did not land: re-pitch it. The agent re-pitches the prior message in plain language using the ubiquitous language from CONTEXT.md. |
| **writing-for-agents** | Writing documents for agents. Use when creating or editing skills, or modifying AGENTS.md or CLAUDE.md. Covers context pointers, the two loads (context and cognitive), information hierarchy with progressive disclosure, and completion criteria. |

---

## 9. Career, Learning & Personal Development

> Skills for teaching, exercises, and learning workflows.

| Skill | Description |
|-------|-------------|
| **scaffold-exercises** | Create exercise directory structures with sections, problems, solutions, and explainers that pass linting. Use when you want to scaffold exercises, create exercise stubs, or set up a new course section with `XX-section-name` and `XX.YY-exercise-name` conventions. |

---

## 10. DevOps, Infrastructure & External Integrations

> Skills for repo setup, pre-commit hooks, guardrails, and tooling.

| Skill | Description |
|-------|-------------|
| **git-guardrails-claude-code** | Set up Claude Code hooks to block dangerous git commands (push, reset --hard, clean, branch -D, etc.) before they execute. Use when you want to prevent destructive git operations or add git safety hooks in Claude Code. |
| **setup-matt-pocock-skills** | Configure this repo for the engineering skills: set up its issue tracker, triage label vocabulary, and domain doc layout. Run once before first use of the other engineering skills. Prompt-driven, explores remotes, AGENTS.md, CONTEXT.md, and docs/adr/ before scaffolding. |
| **setup-pre-commit** | Set up Husky pre-commit hooks with lint-staged (Prettier), type checking, and tests in the current repo. Use when you want to add pre-commit hooks, set up Husky, configure lint-staged, or add commit-time formatting, typechecking, and testing. |

---

## Category Summary

| # | Category | Count |
|---|----------|-------|
| 1 | Frontend Development & UI Engineering | 1 |
| 2 | Design Artifacts & Visual Creation | 3 |
| 3 | Full-Stack & Backend Development | 1 |
| 4 | AI / ML / Multimodal SDK Skills | 0 |
| 5 | Testing, QA & Performance | 3 |
| 6 | Code Quality, Security & Architecture | 5 |
| 7 | Planning, Workflow & Project Management | 11 |
| 8 | Documentation & Content Creation | 8 |
| 9 | Career, Learning & Personal Development | 1 |
| 10 | DevOps, Infrastructure & External Integrations | 3 |
| | **Total** | **36** |

> Deprecated bucket is currently empty. A retired skill is deleted and the changeset that removes it names whatever replaced it.

---

## How to Use This Catalog

1. Identify the category that matches your task.
2. Scan the skill names in that category, the description tells you when to use each one.
3. Open `skills/<bucket>/<skill-name>/SKILL.md` for the full workflow. Bucket is `engineering`, `productivity`, `misc`, or `in-progress` per the table below.
4. Most skills also ship `scripts/`, `references/`, `scenes/`, `routes/`, or `engines/` subdirectories, the SKILL.md will tell you which to load.
5. If you are new to this repo, start with `/ask-matt` (router), then `/grill-with-docs` when you are in a working directory or `/grill-me` when you are not. That is the on-ramp to the main flow.

### Bucket map for this repo

| Bucket | Skills | Plugin shipped | Docs page at `docs/<bucket>/` | Invocation |
|--------|--------|---------------|-------------------------------|------------|
| `engineering` | 18 | yes, in `.claude-plugin/plugin.json` | yes | 9 user-invoked, 9 model-invoked |
| `productivity` | 7 | yes, in `.claude-plugin/plugin.json` | yes | 5 user-invoked, 2 model-invoked |
| `misc` | 4 | no (kept locally) | no | model-invoked |
| `in-progress` | 7 | no (beta, gated) | no | user-invoked |
| `deprecated` | 0 | n/a | n/a | n/a |

### Main flow this catalog enables

`grill-with-docs` or `grill-me` → optional `prototype` detour via `handoff` → `to-spec` → `to-tickets` (tracer-bullet tickets with blocking edges) → `implement` per ticket (drives `tdd` internally, closes with `code-review`) → `wayfinder` when the effort is larger than one session. `triage` feeds the tracker that `implement` works from. `domain-modeling` and `codebase-design` run underneath as vocabulary layers.

---

## Merge Shortlist: 20 Candidates for the Main Collection

> **Intent:** merge the 20 most relevant skills from this repo into `/home/pete/.pi/agent/skills/` (currently 221 entries). Every skill name below is unique against the main collection, zero collisions detected on 2026-05-13, so the merge is purely additive. This section is an appendix to the catalog, not part of the 10-category table.

### Scoring rubric

| Axis | Weight | What it measures |
|------|--------|-----------------|
| Differentiation | x3 | Main collection has no equivalent capability |
| Cross-stack reusability | x2 | Works for any language or framework, not Total TypeScript specific |
| Composability | x2 | Plugs into the main flow or fills a gap between existing main skills |
| Maturity and maintenance | x1 | Promoted bucket, 30+ lines, has docs, no external dep, stable API |
| Demand signal | x1 | Described as daily-use or most popular in this repo's README |

### Ranked 20

| Rank | Skill | Bucket | Invocation | Scores (Diff/Reuse/Compose/Mat/Demand) | Why now | Main collection gap filled |
|------|-------|--------|------------|----------------------------------------|---------|----------------------------|
| 1 | **grilling** | productivity | model | 5/5/5/4/5 | The primitive that powers the entire repo. Single most differentiating idea: relentless interview with recommended answers until every branch of the decision tree is resolved. | No equivalent relentless interview skill; closest is `spec-driven-development` which writes specs but does not grill. |
| 2 | **grill-with-docs** | engineering | user | 5/5/5/4/5 | Stateful variant that leaves a paper trail in CONTEXT.md and ADRs. The documented most popular skill. | Main has `brain-to-docs` for vision extraction but nothing that couples grilling to domain modeling and ADR capture inline. |
| 3 | **diagnosing-bugs** | engineering | model | 5/5/4/5/4 | Tight red feedback loop methodology with minimise, hypothesise, instrument, fix, regression test. Redact discipline built in. | `debugging-and-error-recovery` is general; this is a specific gated loop with a completion criterion. |
| 4 | **codebase-design** | engineering | model | 5/5/5/4/4 | Deep modules vocabulary (module, interface, depth, seam, adapter, leverage, locality) that other skills reference as a shared language. | Main has no deep-module vocabulary skill; complements `clean-code` and `code-quality-standards`. |
| 5 | **domain-modeling** | engineering | model | 5/5/4/4/4 | Active discipline for building CONTEXT.md and ADRs as you design, not just reading them. | Main has `context-engineering` for setup but nothing for active domain model sharpening. |
| 6 | **tdd** | engineering | model | 4/5/4/4/4 | Seam-based TDD with pre-agreed seams, one red-green slice at a time. Sharper than generic TDD. | Main has `tdd-workflow` and `test-driven-development` but both are generic; this adds seam agreement and anti-pattern guidance. |
| 7 | **code-review** | engineering | model | 5/4/5/4/4 | Two-axis parallel sub-agent review (Standards and Spec) since a fixed point, aggregated side by side. | `code-review-checklist` is a lightweight 12-category scan; `code-review-and-audit` is an orchestration shell. This is the thorough gated review. |
| 8 | **to-spec** | engineering | user | 5/5/5/4/4 | Synthesis of the current conversation into a publishable spec with seam selection and ready-for-agent label. | `spec-driven-development` creates specs from scratch; this synthesises from conversation context. |
| 9 | **to-tickets** | engineering | user | 5/5/5/4/4 | Tracer-bullet tickets with explicit blocking edges, tracker-native where possible. Turns a spec into a concurrent work graph. | Main has `planning-and-task-breakdown` and `writing-plans` but no tracer-bullet with blocking edges model. |
| 10 | **wayfinder** | engineering | user | 5/5/5/4/3 | Decision tickets for efforts larger than one session, shared map on the tracker, frontier query, planning by default. | Nothing in main handles multi-session fog-of-war planning with decision tickets. |
| 11 | **grill-me** | productivity | user | 4/5/4/4/5 | Stateless counterpart to grill-with-docs for when there is no working directory. Same primitive, different boundary. | Pairs with grill-with-docs to cover both contexts. |
| 12 | **implement** | engineering | user | 4/5/5/4/4 | Per-ticket implement that drives tdd internally and closes with code-review before committing. The execution edge of the main flow. | `spec-driven-development` describes the idea; this is the gated build and commit flow. |
| 13 | **triage** | engineering | user | 5/4/4/4/3 | Five-role state machine for issues and external PRs, with grilling and agent-ready briefs, and the AI-generated disclaimer discipline. | Main has `planner` style skills but no triage state machine. |
| 14 | **improve-codebase-architecture** | engineering | user | 5/5/4/4/3 | Visual HTML report of deepening opportunities, then grill-through of the chosen one. YAGNI-weighted hot-spot scan. | `clean-code` and `refactor` are tactical; this is the report and grill flow. |
| 15 | **prototype** | engineering | model | 4/5/4/3/4 | Throwaway prototype with hard branching: logic (single HTML file with walkthroughs) versus UI (toggleable variations via URL param). | Main has no prototype-to-answer-a-question skill with that branching. |
| 16 | **research** | engineering | model | 4/5/3/3/3 | Background agent that cites primary sources (official docs, specs, first-party APIs) and writes a single cited markdown file. | Main has `context7-docs` for doc retrieval; this is the cited research capture workflow. |
| 17 | **writing-for-agents** | productivity | model | 5/5/4/4/3 | Levers for writing agent-facing documents: context pointers, the two loads, information hierarchy with progressive disclosure, completion criteria, leading words. | `agents-md` and `claude-md` create files; this teaches how to write them predictably. |
| 18 | **wizard** | engineering | model | 4/4/4/3/3 | Generates an interactive bash wizard from a template with stage progress, secret entry, and idempotent env upserts. Never hand-edits the library above the STAGES marker. | No equivalent wizard scaffolding in main; complements `polyglot` infra skills. |
| 19 | **handoff** | productivity | user | 4/5/3/3/3 | Compacts conversation into a handoff document with pointers, not duplicated content, for cross-session and cross-worktree continuation. | Main has `continuation` hints but no dedicated handoff skill. |
| 20 | **setup-ts-deep-modules** | in-progress | user | 4/4/3/4/2 | Wires dependency-cruiser so each TypeScript package is a deep module with four enforced rules and a prove-it-bites check. | Main does deep-module vocabulary only via codebase-design; this is the enforceable wiring. Chosen despite beta because demand is high and the config is self-contained. |

### Explicitly deferred (16) and why

| Skill | Bucket | Reason deferred |
|-------|--------|-----------------|
| **ask-matt** | engineering | Router meta skill for this repo. Not portable until the 20 land and a new router makes sense in main. Reassess after merge. |
| **setup-matt-pocock-skills** | engineering | Installer for this repo's tracker and CONTEXT conventions. Useful as reference but main has its own setup conventions; extract patterns manually instead. |
| **resolving-merge-conflicts** | engineering | Valuable but narrow trigger (active merge or rebase conflict). Keep locally, pull on demand. |
| **teach** | productivity | Strong skill but longer-form teaching workspace overlaps with `teach` patterns in main learning skills. Reassess after grilling primitives land. |
| **to-questionnaire** | productivity | Useful for async decisions but niche versus the core flow. Keep for second merge window. |
| **wait-what** | productivity | One-line re-pitch skill. Pull individually if CONTEXT.md adoption spreads to main. |
| **scaffold-exercises** | misc | Total TypeScript course scaffolding. Keep in misc, narrow audience for main. |
| **migrate-to-shoehorn** | misc | Total TypeScript test migration. Keep in misc, shoehorn-specific. |
| **setup-pre-commit** | misc | Husky and lint-staged setup. Main already covers `lint-and-validate` and `ci-cd` flows; defer. |
| **git-guardrails-claude-code** | misc | Claude Code hook setup. Main guardrail skill already exists at `global-agent-guardrails`; patterns overlap. |
| **claude-handoff** | in-progress | Beta variant of handoff that launches `claude --bg`. Defer until beta graduates and handoff lands first. |
| **implement-spec** | in-progress | Beta task-graph implement with worktree concurrency. Defer until wayfinder and implement land and concurrency patterns are proven in main. |
| **loop-me** | in-progress | Beta workflow grilling for loops. Defer until grilling primitives land. |
| **writing-beats** | in-progress | Beta exploit assembly for beats. Defer until writing-for-agents establishes grounding conventions in main. |
| **writing-fragments** | in-progress | Beta explore mining for fragments. Same dependency as beats. |
| **writing-shape** | in-progress | Beta exploit shaping paragraph by paragraph. Same dependency as beats. |

### Merge mechanics (to run after you approve the shortlist)

1. Copy each of the 20 skill folders verbatim to `/home/pete/.pi/agent/skills/<skill-name>/` (preserve `SKILL.md`, `scripts/`, `references/` where present).
2. No `.claude-plugin/plugin.json` change in the first pass, these 20 are added to the file mirror, not the Claude Code managed bundle, so no validation gate is triggered. Promote to the plugin manifest only after a bake period.
3. Run `scripts/link-skills.sh` to relink `~/.claude/skills` and `~/.agents/skills` symlinks per AGENTS.md.
4. Verify: `ls -1 /home/pete/.pi/agent/skills/ | wc -l` shows 241 (221 plus 20), `rg "em dash" skills-catalog.md` is empty, and each new `SKILL.md` passes `rg "^name:"` and `rg "^description:"`.
5. Update main collection's `skills-catalog.md` to append the 20 in their 10 categories, keeping the existing 208 rows intact and bumping the header and Category Summary.

---

## Inventory Source

Generated from live reads of every `SKILL.md` frontmatter on 2026-05-13. Bucket counts: `engineering 18`, `productivity 7`, `misc 4`, `in-progress 7`, `deprecated 0` (empty). Plugin manifest lists 25 promoted skills. Docs pages exist for all 25 promoted skills at `docs/<bucket>/<skill>.md` and for none in `misc` or `in-progress`, consistent with `.agents/writing-docs.md` and `.claude-plugin/marketplace.json` conventions.

For the raw TSV, see the build artifact at `/tmp/mattpocok-inventory.tsv` (transient, gitignored).

