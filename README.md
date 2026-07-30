# my-pi-agent

An opinionated customization bundle for the [Pi Agent](https://github.com/nordeim/my-pi-agent) — themes, in-tree extensions, a curated 197-skill library, and the supporting docs an agent needs to bootstrap a fresh Pi installation into a productive engineering setup.

This setup is fairly opinionated. It:

- sets up GitHub Dark Default as the theme
- adds Firecrawl tools for searching and scraping
- updates the bottom bar to show the info the maintainer actually cares about
- adds background terminals + UI to manage them
- adds subagents to Pi
- adds workflows to Pi
- adds an ask-user tool that lets the model ask multiple-choice questions
- adds first-class `fd` (file discovery) and `rg` (content search) tools

![Pi setup interface](assets/pi-setup.jpeg)

---

## What's in the box

| Area | Path | Description |
|------|------|-------------|
| Pi setup | `package.json`, `tsconfig.json`, `.env.example` | Runtime config, dependency manifest, env-var template for the Pi shell itself. |
| Extensions | `extensions/` | Twelve TypeScript extensions that plug into the Pi agent loop (see below). |
| Skills | `skills/` | 197 self-contained skill packages across 10 categories — the bulk of the repo by file count. Each skill ships a `SKILL.md` with frontmatter (`name`, `metadata.description`, `license`) plus optional `references/`, `scripts/`, `scenes/`, `routes/`, or `engines/` subdirectories loaded on demand. |
| Themes | `themes/` | `github-dark-default.json` and `brutalist.json` — Pi UI color themes. |
| Git config | `git/` | Project-local gitignore patterns. |
| Assets | `assets/` | Screenshots referenced by this README. |
| Docs | `SETUP.md`, `AGENTS.md`, `APPEND_SYSTEM.md`, `Translation_Engine_v10_APPEND_SYSTEM.md` | Setup runbook, agent-onboarding brief, and system-prompt append layers. |

---

## Skills catalog

The skill library lives under `skills/` and is indexed by [`skills/skills-catalog.md`](skills/skills-catalog.md) — a single-file directory of all 197 skills with a one-line description and "when to use it" hint for each. The catalog is organized into 10 categories:

1. **Frontend Development & UI Engineering** — 31 skills (React 19, Next.js 16, Tailwind v4, Svelte 5, Vue 3/Nuxt 4, Flutter, React Native/Expo, Astro 5, Tauri 2, HTMX, SolidStart, brutalist/avant-garde design systems, full-stack SaaS references, pixel-for-pixel web cloning)
2. **Design Artifacts & Visual Creation** — 11 skills (charts, image generation/edit/understand/search, web-shader extraction, ComfyUI, **podcast-generate** (LLM script + TTS audio synthesis))
3. **Full-Stack & Backend Development** — 23 skills (Laravel 12, Django 6, Rails 8, Go, Rust/Axum, Spring Boot 3, .NET 9, FastAPI, NestJS, Phoenix 1.7, Hono, Fastify, KeystoneJS 6, fullstack-dev, Next.js 16 + Postgres 17, auth library comparison, web-frameworks, API patterns, Python patterns, framework templates, n8n, PowerShell)
4. **AI / ML / Multimodal SDK Skills** — 8 skills (LLM, ASR, TTS, VLM, video generation/understanding, web search/reader)
5. **Testing, QA & Performance** — 14 skills (TDD, webapp testing, Playwright CLI, agent-browser, Chrome DevTools MCP, performance optimization)
6. **Code Quality, Security & Architecture** — 15 skills (code review, security hardening, TrustSkill v3.1 security scanner, vulnerability scanner, clean-code, ponytail minimalism, debugging, lint-and-validate)
7. **Planning, Workflow & Project Management** — 23 skills (spec-driven development, plan-writing, incremental implementation, git workflow, CI/CD, shipping, orchestrator-toolkit, loop-builder, subagents, background terminals, context engineering)
8. **Documentation & Content Creation** — 27 skills (README/CLAUDE/AGENTS.md generation, blog writer, SEO content, content strategy, content analysis, **pptx**, **pptx-unified** (combo recipe: 5-stage pipeline + 20+ lessons + 12-layout catalog + 8 palettes + 6 typography pairings + validate/export scripts), **codex-ppt**, **cyber-ppt**, **pptx-generator**, **docx**, **docx-generation**, **minimax-docx** (.NET OpenXML SDK + 13 style-guide recipes), **kimi-docx** (Moonshot AI C# SDK + native Word charts + Morandi backgrounds + track-changes API), **xlsx**, pdf, **minimax-pdf** (token-based design-system PDF with 14 doc types), **kimi-pdf** (HTML+Paged.js + 11 cover styles + three-line tables + GB/T 7714/APA citations), **minimax-xlsx** (XML direct-edit pipeline), **kimi-xlsx** (KimiXlsx CLI with 6-command validation + PivotTables), cheat-sheet, storyboard manager, **pandoc-docx-template**, **translation-engine**, **qingyan-research** (deep web research → HTML report with Chart.js))
9. **Career, Learning & Personal Development** — 19 skills (resume builder, JD-resume tailor, interview prep, study buddy, quiz mastery, mindfulness, dream interpreter, **gaokao-collect-student-info** / **gaokao-fetch-volunteers** / **gaokao-recommend-majors** / **gaokao-recommend-schools** / **gaokao-generate-report** — 5-step Chinese college-entrance-exam志愿填报 pipeline)
10. **DevOps, Infrastructure & External Integrations** — 27 skills (Cloudflare tunnel, multi-search-engine, finance/stock analysis, market research reports, AMiner academic search, **aminer-free-academic** (free-tier 7-API variant), AI news collectors, **kubernetes-env-setup** (hardened self-managed Kubernetes for agentic AI on Azure Linux), marketing-mode, skill-creator, skill-creator-zai, skill-finder-cn, **how-to-git-push-using-ssh-wrapper**, Microsoft Foundry, Sanity best-practices/migration/deploy, memory architect/architecture, mac-mlx local inference, tools-cli, system-prompt customization)

Each skill folder contains a `SKILL.md` with frontmatter (`name`, `metadata.description`, `license`) and the full workflow instructions. Most skills also ship `references/`, `scripts/`, or `scenes/` subdirectories that the `SKILL.md` loads on demand.

---

## Extensions

Twelve TypeScript extensions under `extensions/` extend the Pi agent loop. Each one is a self-contained package with its own `package.json` and `tsconfig.json`.

| Extension | Purpose |
|-----------|---------|
| `ask-user` | Lets the model ask the user multiple-choice questions instead of guessing. |
| `ava-agent` | Ava autonomous agent harness with session-graph, AST auditor, and reflect-session tooling. |
| `background-terminals` | Run and manage long-lived shell commands (dev servers, watchers, streaming builds) in background terminals. |
| `copy-all` | Bulk-copy agent output to the clipboard. |
| `file-search` | First-class `fd` (file discovery) tool wired into the agent loop. |
| `firecrawl-search` | Firecrawl-powered web search and scraping tool. |
| `git-info` | Surface git status, changed files, and refresh-coordination in the Pi UI. |
| `model-info` | Display model metadata in the bottom bar. |
| `summaries` | Generate and surface session summaries inside the agent transcript. |
| `subagents` | Headless autonomous sub-agents (Pi, Claude, Codex harnesses) with their own context window. |
| `ui-customization` | Customize Pi UI chrome (bottom bar, panels, status indicators). |
| `workflows` | Multi-step workflow runner with sandboxing, artifacts, serialization, and a dashboard view. |

---

## Themes

Two Pi UI themes ship in `themes/`:

- `github-dark-default.json` — the default dark theme modeled on GitHub's dark palette.
- `brutalist.json` — a raw, high-contrast brutalist alternative.

Switch between them via Pi's theme selector.

---

## Setup

### On your own Pi

Instructions for installing this bundle on a fresh Pi are in [`SETUP.md`](SETUP.md). The short version: clone the repo, copy `themes/*.json` into Pi's themes directory, symlink the extensions you want into Pi's `extensions/` directory, and restart Pi.

### For agents

If you are an agent reading this, onboarding instructions are in [`AGENTS.md`](AGENTS.md). System-prompt append layers live in [`APPEND_SYSTEM.md`](APPEND_SYSTEM.md) and [`Translation_Engine_v10_APPEND_SYSTEM.md`](Translation_Engine_v10_APPEND_SYSTEM.md) — read them in order before operating in this repo.

### Skills

Skills are loaded on demand by the Pi agent loop. To make a skill available, ensure its folder is present under `skills/` (it already is, if you cloned this repo) and that Pi's skill discovery is pointed at `skills/`. To find the right skill for a task, start at [`skills/skills-catalog.md`](skills/skills-catalog.md).

---

## Repository layout

```
my-pi-agent/
├── assets/                    # Screenshots and images
├── extensions/                # 12 TypeScript extensions to the Pi agent loop
├── git/                       # Project-local gitignore patterns
├── skills/                    # 197 skill packages (see skills/skills-catalog.md)
├── themes/                    # github-dark-default.json, brutalist.json
├── AGENTS.md                  # Agent onboarding brief
├── APPEND_SYSTEM.md           # System-prompt append layer
├── README.md                  # This file
├── SETUP.md                   # Pi-side installation runbook
├── Translation_Engine_v10_APPEND_SYSTEM.md
├── package.json               # Pi runtime dependencies
├── tsconfig.json              # TypeScript config for extensions
└── .env.example               # Environment variable template
```

---

## License

The Pi setup code in this repo is provided as-is for the maintainer's personal use. Individual skills under `skills/` ship their own licenses — see each skill's `LICENSE.txt` and `SKILL.md` frontmatter for terms.
