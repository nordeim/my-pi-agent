---
name: readme-md
description: Creates a professional, high-signal README.md for a repository by investigating the codebase and following battle-tested conventions distilled from production open-source projects.
version: 1.0.0
tags:
  - documentation
  - readme
  - onboarding
  - repository-setup
  - project-readme
---

When asked to create or update a README.md for a repository, follow the procedure below.

## Goal
Create or update `README.md` for this repository.
The goal is a professional, scannable document that gives every visitor — developer, user, or AI agent — exactly what they need in under 60 seconds.

## How to investigate
Read sources in this order, preferring executable truth over prose:
1. **Existing README.md** — understand what's already covered, identify gaps
2. **`pyproject.toml`, `package.json`, `Cargo.toml`, `go.mod`** — name, version, entry points, dependencies
3. **Build/test/lint config** — `Makefile`, `justfile`, CI workflows, pre-commit config — extract real commands
4. **Root manifests** — `docker-compose.yml`, `Dockerfile`, `.env.example` — extract setup steps, env vars, services
5. **Existing instruction files** — `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/` — project conventions
6. **`docs/` directory** — architecture docs, API docs, runbooks
7. **Representative source files** — entrypoints, key models, router files — only if architecture is still unclear
8. **Changelog / `CHANGELOG.md`** — recent changes, version history for "What's New" section

Prefer executable sources over prose. If docs conflict with config or scripts, trust the executable source.

## Section chooser
Not every README needs every section. Choose based on project type:

### Must-have (every project)
- **Title + Badges** — name, version, CI status, license, key dependencies
- **One-line tagline** — what it does, who it's for
- **Quick overview** — problem it solves + how it solves it (3–5 sentences)
- **Quick Start** — the shortest path from clone to running, with verification
- **License**

### Include if applicable
| If the project has… | Add this section |
|---------------------|-----------------|
| Multiple services or complex architecture | **Architecture** (tech stack table + mermaid diagram) |
| Non-trivial directory layout | **File Hierarchy** (annotated tree) |
| APIs or CLI tools | **API Reference / Tool Catalog** (endpoint/command table) |
| Environment variables | **Environment Variables** (table or `.env` example) |
| A test suite | **Testing** (exact commands, coverage targets) |
| A design system or UI | **Design System** (color tokens, typography, animation names) |
| Production deployment | **Deployment** (architecture diagram + steps) |
| Security/compliance requirements | **Security & Compliance** (posture table) |
| Multi-phase implementation | **Project Status** (phase completion table) |
| Known rough edges | **Troubleshooting** (issue → solution table) |
| Local/regional context | **Local Context** (GST, address formats, payment methods — keep it short) |
| Contributing guidelines | **Contributing** (TDD flow, conventions, pre-commit hooks) |

### Skip entirely
- Don't add a section just because other READMEs have it. Every section must earn its place with repo-specific content.
- If the project is simple (single script, small library), keep the README proportional. A 50-line README is better than a 500-line one padded with generic filler.

## Section writing rules

### Title + Badges
- Use the project name exactly as it appears in the package manifest.
- Badge row: version, CI status, coverage, license, key dependency versions. Use shields.io badges.
- Badges must be verifiable — don't fabricate a passing CI badge if no CI exists.
- For projects with regional context, add context badges (e.g., GST rate, currency, timezone).

### Overview
- Start with **what** the project is (one sentence).
- Follow with **why** it exists — the problem it solves.
- End with **how** — the solution approach.
- Keep to 3–5 sentences. No paragraphs of backstory.

### Key Features
- Use a table with emoji + feature name + one-line description.
- Only include features that are actually implemented. Never list planned features as if they exist.
- Derive features from source code, not from wishlists in docs.

### Architecture
- **Tech stack table**: Layer, Technology, Version, Purpose. Versions must match lockfiles or manifests.
- **Architectural principles**: Numbered list only if the project has documented principles. Skip if generic.
- **Mermaid diagrams**: Add only if they clarify something not obvious from the tech stack table. Use `flowchart TB` for system architecture, `sequenceDiagram` for request flows. Keep diagrams compact — no more than 15–20 nodes.

### File Hierarchy
- Use emoji-prefixed tree format: `📂` for directories, `📄` for files.
- Annotate only key files with short descriptions (10–20 words).
- Skip leaf files that are obvious from their names.
- Skip `.gitignore`, `LICENSE`, and other boilerplate files.
- Prefer the real directory structure over idealised plans.

### Quick Start
- Use numbered steps.
- Every command must be copy-pasteable and tested against the actual setup flow.
- Include a "Verify Setup" subsection with expected outputs.
- Specify required runtimes with version constraints (e.g., "Python ≥3.12", "Node.js ≥20").
- If Docker is available, offer it as the simpler path.

### Environment Variables
- If the project has `.env.example`, reproduce the key variables with inline comments.
- If the project has many env vars, group them by purpose (Database, Redis, Django, Frontend).
- Include the `DJANGO_SETTINGS_MODULE` or equivalent — agents frequently guess this wrong.
- Mark optional variables clearly.

### Testing
- List exact test commands per package/monorepo component.
- Include coverage targets if they exist in config.
- Include CI pipeline structure if it affects how tests should be run locally.
- Note any special test prerequisites (e.g., "requires Redis running", "use `-p no:xdist` for sequential execution").

### API Reference / Tool Catalog
- Use a table: Endpoint/Tool, Method, Description.
- Group by resource or capability.
- Mark authenticated vs public endpoints.
- Mark destructive operations (⚠️) that require tokens or approval.
- For CLI tools, include exit code semantics if non-standard.

### Design System
- Only include if the project has a custom design system beyond framework defaults.
- Color table: Token, Hex, Usage.
- Typography: font name, usage, fallback.
- Animation names if defined in CSS globals.

### Deployment
- Production architecture diagram (ASCII art or mermaid).
- Step-by-step deployment commands.
- Scaling considerations only if the project documents them.
- Skip if the project has no production deployment configuration.

### Contributing
- Include TDD flow if the project uses it (RED → GREEN → REFACTOR).
- List framework-specific conventions that differ from defaults (e.g., "React 19: no `forwardRef`", "Tailwind v4: CSS-first config, no `tailwind.config.js`").
- List pre-commit hooks if configured.
- Skip if the project is proprietary and doesn't accept contributions.

### Project Status
- Use a phase completion table: Phase, Status, Completion Date, Key Deliverables.
- Include overall progress percentage if measurable.
- Include latest audit/review status if documented.
- Skip if the project is a simple library or tool.

### Troubleshooting
- Use an issue → solution table.
- Only include issues that are project-specific, not generic framework errors.
- Derive from actual bug fixes documented in the repo.

### What's New / Recent Changes
- If `CHANGELOG.md` or audit reports exist, summarise the most recent changes in a compact table.
- Group by severity if from a security audit.
- Include migration notes if recent changes added migrations.
- Skip if the README is for a new project with no history.

## What to exclude
- **Generic software advice** — no "make sure to write tests" platitudes
- **Placeholder content** — no lorem ipsum, no "coming soon" features listed as if real
- **Duplicated information** — if it's in `docs/DEPLOYMENT.md`, link, don't repeat
- **Exhaustive file trees** — annotate only key files; skip boilerplate
- **Speculative claims** — don't claim "99.9% uptime" or "blazing fast" without benchmarks
- **Long tutorials** — Quick Start is a Quick Start, not a workshop
- **Copy-pasted framework docs** — assume the reader knows their framework
- **Content better stored in `AGENTS.md`** — agent instructions belong there, not in README

## Project-type quick reference

### Full-stack web app (Django + Next.js, Rails + React, etc.)
Focus on: Architecture (both sides), BFF/API flow, File Hierarchy, Quick Start for both back and front, Environment Variables, Testing for both, Deployment.

### CLI tool / library (Python package, npm package, etc.)
Focus on: Why (problem statement), Quick Start (pip/npm install + 3-step flow), Tool/API Catalog, Standardized Interfaces (JSON envelopes, exit codes), Governance/Security, Troubleshooting.

### E-commerce / SaaS platform
Focus on: Overview (problem/solution), Features, Architecture (payment flow, BFF), Design System, Local Context (GST, address formats, payment methods), API Documentation.

### Single-purpose library
Keep it minimal: Title + Badges, One-line description, Quick Start, API Reference, License. Don't add architecture diagrams or file trees for a 3-file library.

## Quality checklist
Before finalising the README, verify:
- [ ] Every command in Quick Start is copy-pasteable and tested
- [ ] Every badge link is correct (CI, coverage, PyPI/npm)
- [ ] Tech stack versions match lockfiles/manifests
- [ ] File hierarchy reflects actual directory structure
- [ ] Mermaid diagrams render correctly (no syntax errors)
- [ ] No placeholder or speculative content
- [ ] License matches the repo's actual license file
- [ ] All referenced docs/links exist in the repo
- [ ] Sections are proportional to project complexity
