---
name: project-architecture-document-md
description: Create a comprehensive Project Architecture Document (PAD) for any codebase. Use when the user asks to generate a PAD, architecture document, system design document, or technical blueprint for a project. Also triggers on "document this codebase", "create architecture reference", "generate system overview", "write ADR", "document the architecture of this project". Covers executive summary, tech stack with version pinning, Architecture Decision Records (ADRs), system topology diagrams, layer models, annotated directory structures, critical code patterns with invariants, database schemas, security architecture, testing strategy, build/deployment, developer handbook, and known issues. Produces a single source-of-truth markdown document that serves as the definitive engineering reference for onboarding, debugging, and replication.
---

# Project Architecture Document (PAD) Generator

> **Purpose:** Generate a comprehensive, production-grade Project Architecture Document (PAD) that serves as the single source of truth for any codebase. The PAD captures not just _what_ the system is, but _why_ every decision was made and _how_ every component fits together.
>
> **Audience:** Senior engineers, tech leads, DevOps, onboarding engineers, and AI coding agents who need to understand, extend, debug, or replicate the project.
>
> **Methodology:** Distilled from 14 production PADs across Next.js, React/Vite, Django, Python CLI, and SPA architectures. Every section is grounded in the principle that **every architectural decision traces to a specific rationale** — nothing is here "because it's popular."

---

## When to Use This Skill

- User requests a "PAD", "architecture document", "system design document", or "technical blueprint" for a project
- User says "document this codebase" or "create an architecture reference"
- User wants to generate ADRs (Architecture Decision Records) for key technical choices
- User needs a system overview for onboarding new engineers or AI agents
- User wants to produce a "single source of truth" document for an existing codebase
- After completing a major project milestone, security remediation, or architectural overhaul

---

## The PAD Structure — Canonical Section Order

Every PAD MUST follow this section order. Sections marked with `[MANDATORY]` are required. Sections marked with `[CONDITIONAL]` are included only when applicable to the project.

### Document Header

```markdown
# <Project Name> — Master Project Architecture Document (PAD) v<version>

**Classification:** Internal Engineering Reference
**Status:** DEFINITIVE, PRODUCTION-LOCKED BLUEPRINT
**Companion Document:** <Link to PRD/Spec if exists>
**Last Updated:** <Date in YYYY-MM-DD format>
**Audience:** Senior Engineers, Tech Leads, DevOps, and Onboarding Engineers
**Rule:** Every architectural decision in this document traces to a specific rationale.
           Nothing is here "because it's popular."
```

### Revision Block (for iterative updates)

```markdown
#### Revision Block — v<version> (Tracked Changes)

Every change is tagged with its source: `[RES]` = validated by web research,
`[SR]` = self-review, `[CA]` = critical analysis, `[SYN]` = synthesis,
`[SAN]` = sanitization pass, `[AUTH]` = auth alignment.

- `[TAG, SOURCE]` <Change description with rationale>
```

### Table of Contents

Numbered sections with deep links. Typically 10–15 sections.

### Section 1: System Overview & Decisions `[MANDATORY]`

**1.1 Document Metadata & Purpose** — What this PAD is, relationship to PRD/spec, how to use it (by audience: new engineer, debugging, reviewing tech choices).

**1.2 Technology Stack Summary** — Definitive table. NO speculative "e.g." language. Every choice is locked.

| Column | Description |
|--------|-------------|
| **Layer** | Category (Web Framework, UI Runtime, Language, ORM, etc.) |
| **Technology** | Exact package/project name |
| **Version** | Pinned version with rationale (e.g., "≥16.2.6 for CVE-2025-55182 mitigation") |
| **Key Rationale** | Why this over alternatives |

**1.3 Architecture Decision Records (ADRs)** `[MANDATORY]`

Each ADR follows this structure:

```markdown
**ADR-NNN: <Decision Title>**

- **Context:** <What problem does this solve? What constraints exist?>
- **Decision:** <What was chosen? Be specific — exact versions, exact patterns.>
- **Rationale:** <Why this decision? What evidence supports it?>
- **Consequences:** Positive and negative trade-offs.
- **Alternatives Rejected:** What was considered and why it was rejected.
```

Generate 3–7 ADRs covering the most consequential technical choices. Prioritize:
- Framework selection
- Database / ORM
- Authentication strategy
- Deployment architecture
- Build tooling
- State management approach

### Section 2: High-Level System Topology `[MANDATORY]`

ASCII art or Mermaid diagram showing the full system from client to external services. Include:
- Client layer (browser, mobile, admin)
- CDN / Edge layer
- Application layer (web app, worker, API)
- Data layer (database, cache, storage)
- External services (APIs, third-party)

Annotate each layer with its runtime, scaling characteristics, and key constraints.

### Section 3: Application Architecture `[MANDATORY]`

**3.1 The Layer Model** — Numbered layers with strict rules. The "Golden Rule" of the architecture.

```
Layer 0: <Name> — <Role>. <Rule.>
Layer 1: <Name> — <Role>. <Rule.>
...
```

**3.2 Annotated Directory Structure** — Full tree with inline comments explaining each file/directory's purpose. Use `←` annotations or inline comments.

**3.3 Critical Code Patterns** — 3–5 annotated code blocks showing the most important patterns. Each code block MUST include:
- A JSDoc/docstring header explaining the pattern's purpose
- Inline comments explaining non-obvious decisions
- A "Why this pattern" explanation after the code

### Section 4: Data Architecture `[CONDITIONAL]`

Include if the project has a database.

**4.1 Database Schema** — Mermaid ER diagram + table definitions
**4.2 Data Models** — Key entity schemas with types
**4.3 Persistence Strategy** — Connection pooling, caching, migration patterns

### Section 5: Design System Reference `[CONDITIONAL]`

Include if the project has a non-trivial UI.

**5.1 Typographic System** — Typefaces, weights, usage rules
**5.2 Color Tokens** — Semantic color scale with hex values and WCAG contrast ratios
**5.3 Component Primitives** — UI library choices and customization approach
**5.4 Motion / Animation** — Keyframe library, transition rules, reduced-motion handling

### Section 6: Security Architecture `[MANDATORY]**

**6.1 Security Rules** — Mandatory rules table with enforcement mechanisms
**6.2 Security Utilities** — Inventory of security-critical code
**6.3 Authentication & Authorization** — Session model, RBAC, token strategy
**6.4 Threat Model** — Key attack vectors and mitigations

### Section 7: Worker / Background Service Architecture `[CONDITIONAL]`

Include if the project has background jobs, queues, or async processing.

**7.1 Worker Directory Structure**
**7.2 Job Queue Configuration** — Queue names, concurrency limits, retry policies
**7.3 Flow / Pipeline Patterns** — DAG definitions, parent-child relationships

### Section 8: Testing Strategy `[MANDATORY]`

**8.1 Test Distribution** — Table: category, file count, test count, location, framework
**8.2 Test Patterns** — Source-level tests, reducer tests, integration tests
**8.3 Coverage Thresholds** — Minimum coverage percentages by module
**8.4 Pre-PR / Pre-Deploy Checklist** — Bullet list of required checks

### Section 9: Build & Deployment `[MANDATORY]`

**9.1 Production Build** — Build commands, output structure
**9.2 Environment Variables** — Table: name, required/optional, description, default
**9.3 Docker Configuration** — Base image, size, security hardening
**9.4 CI/CD Pipeline** — Stages, quality gates, deployment targets

### Section 10: Developer Handbook `[MANDATORY]`

**10.1 Local Setup** — Step-by-step for minimal and full setup
**10.2 Common Commands** — Table: command, location, purpose
**10.3 Code Style Rules** — Enforcement mechanisms
**10.4 Git Workflow** — Branching, PR process, commit conventions

### Section 11: Known Issues & Outstanding Tasks `[MANDATORY]`

Use a priority table:

```markdown
| Priority | Issue | Impact | Status |
|----------|-------|--------|--------|
| CRITICAL | <description> | <impact> | Open/Blocked |
| HIGH | <description> | <impact> | In Progress |
```

### Section 12: Key Files Reference `[MANDATORY]`

Quick-reference table of the most important files:

```markdown
| File | Lines | Purpose |
|------|-------|---------|
| <path> | ~N | <One-line description> |
```

### Section 13: Glossary `[CONDITIONAL]`

Domain-specific terms, acronyms, and project-specific jargon.

---

## Generation Methodology

### Phase 1: Codebase Investigation

Before writing any section, investigate the project:

1. **Read the root configuration files:** `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Makefile`, `Dockerfile`, `docker-compose.yml`, CI configs
2. **Read the entry points:** `main.ts`, `index.ts`, `App.tsx`, `app/layout.tsx`, `src/index.ts`
3. **Map the directory structure:** Run `find . -type f -not -path './node_modules/*' -not -path './.git/*' -not -path './dist/*' -not -path './.next/*' | head -200`
4. **Identify the layer model:** Look for `src/app/`, `src/features/`, `src/domain/`, `src/lib/`, `src/server/`, `src/client/` patterns
5. **Read the database schema:** Look for `schema.ts`, `models.py`, `migrations/`, `*.sql` files
6. **Read the auth configuration:** Look for `auth.ts`, `auth.config.ts`, middleware, session handling
7. **Read the build/config:** `next.config.ts`, `vite.config.ts`, `tsconfig.json`, `tailwind.config.*`
8. **Read the PRD or spec if it exists:** `PRD.md`, `README.md`, `AGENTS.md`, `CLAUDE.md`

### Phase 2: Section Generation

Generate sections in this order, because later sections depend on earlier ones:

1. **Header + Metadata** — From project name, current date, git status
2. **Tech Stack** — From `package.json` / `pyproject.toml` / `Cargo.toml` + config files
3. **ADRs** — From the most consequential choices found in Phase 1
4. **System Topology** — From the infrastructure and deployment files
5. **Application Architecture** — From the directory structure and code patterns
6. **Data Architecture** — From schema files and ORM models
7. **Design System** — From CSS files, theme tokens, component library usage
8. **Security** — From auth, middleware, validation, and security utility files
9. **Testing** — From test files, coverage configs, CI pipeline
10. **Build & Deployment** — From Docker, CI, env configs
11. **Developer Handbook** — From scripts, Makefile, README
12. **Known Issues** — From TODO comments, issue trackers, incomplete implementations
13. **Key Files Reference** — From the most important files identified in Phase 1

### Phase 3: Validation

Before delivering the PAD:

- [ ] Every technology has a pinned version
- [ ] Every ADR has Context, Decision, Rationale, Consequences, Alternatives Rejected
- [ ] The directory structure is complete (no major directories missing)
- [ ] Code patterns include inline comments explaining the "why"
- [ ] Security rules have enforcement mechanisms documented
- [ ] Environment variables are complete with required/optional markers
- [ ] The document is navigable (TOC links work, sections are numbered)
- [ ] No placeholder text remains (`TODO`, `TBD`, `<insert here>`)

---

## Writing Standards

### Tone & Voice

- **Definitive, not speculative.** "Use Next.js 16" not "Consider using Next.js or perhaps Next.js 16."
- **Rationale-driven.** Every choice explains WHY. "Pinned to ≥16.2.6 as mitigation for CVE-2025-55182" not "Using 16.2.6."
- **Anti-generic.** Reject template aesthetics. The PAD should reflect the project's unique architectural identity.
- **Copy-paste ready.** All code blocks must be executable. No spacing artifacts. No placeholder values in configuration.

### Formatting Rules

- Use `###` for sections, `####` for subsections
- Code blocks must specify the language: `typescript`, `python`, `bash`, `text`, `mermaid`, `css`
- Tables must have alignment markers
- Directory trees use `├──` / `└──` / `│` characters
- File annotations use `←` or inline `# comment` style
- ADRs are numbered sequentially: ADR-001, ADR-002, etc.

### What NOT to Include

- **No tutorial content.** The PAD assumes the reader is a competent engineer. Don't explain what React is.
- **No API reference.** Link to API docs; don't reproduce endpoint signatures.
- **No changelog.** That's what git log and release notes are for.
- **No personal opinions.** Every claim is grounded in code evidence or documented rationale.
- **No future roadmap.** Current state only. Link to the PRD or roadmap doc for future plans.

---

## Output

The skill produces a single markdown file at the project root (or specified path):

```
<project-root>/Project_Architecture_Document.md
```

The file is self-contained, requires no external references beyond linked companion documents (PRD, API docs), and serves as the definitive engineering reference for the project.

---

## Companion Skills

- **`claude-md`** — Generate CLAUDE.md for the same codebase (tighter scope, AI agent instructions)
- **`readme-md`** — Generate README.md (user-facing, not architecture-focused)
- **`distill-codebase-skill`** — Capture lessons learned as a reusable SKILL.md (post-remediation)
- **`documentation-and-adrs`** — Record individual ADRs for incremental decision tracking
