# Skills Inventory — my-pi-agent

> Auto-generated comprehensive inventory of the spec-compliant skill packages under `skills/`. **Synced with `skills/skills-catalog.md` (2026-10-02) — catalog is source of truth.**
> **218 skills** listed (13920 files, 4 nested sub-skills/templates inside entries). A skill is listed only when its top-level folder under `skills/` contains a `SKILL.md` with a skill-spec-compliant YAML header — `name` (lowercase letters, digits, hyphens; max 64 chars; matches the folder name) and `description` (non-empty; max 1024 chars). 21 grouping folders without a top-level `SKILL.md` and 28 folders whose frontmatter fails validation are excluded — full list in [Validation & Exclusions](#validation--exclusions) below.

---

## How to read this inventory

Each entry below describes one top-level skill folder. For every skill we capture:

- **Folder** — the directory name under `skills/`
- **Path** — repo-relative path to the skill folder
- **SKILL.md** — whether the skill ships a top-level `SKILL.md` and its location
- **Title** — the first H1 in `SKILL.md` (falls back to the skill name)
- **Description** — parsed from the YAML frontmatter `description` field
- **License / Author / Version** — when declared in the frontmatter
- **Structure** — which standard subdirectories (`scripts/`, `references/`, `scenes/`, `routes/`, `engines/`) are present
- **File count** — total files in the skill folder (recursive)
- **Sub-skills / templates** — nested directories that themselves contain a `SKILL.md`
- **Category** — auto-classified into one of the 10 catalog categories

Skills are listed alphabetically within each category. Use the category index below to jump to a category.

## Category Index

1. **Frontend Development & UI Engineering** — 50 skills — [jump](#1-frontend-development--ui-engineering)
2. **Design Artifacts & Visual Creation** — 16 skills — [jump](#2-design-artifacts--visual-creation)
3. **Full-Stack & Backend Development** — 13 skills — [jump](#3-full-stack--backend-development)
4. **AI / ML / Multimodal SDK Skills** — 11 skills — [jump](#4-ai--ml--multimodal-sdk-skills)
5. **Testing, QA & Performance** — 28 skills — [jump](#5-testing-qa--performance)
6. **Code Quality, Security & Architecture** — 23 skills — [jump](#6-code-quality-security--architecture)
7. **Planning, Workflow & Project Management** — 32 skills — [jump](#7-planning-workflow--project-management)
8. **Documentation & Content Creation** — 24 skills — [jump](#8-documentation--content-creation)
9. **Career, Learning & Personal Development** — 12 skills — [jump](#9-career-learning--personal-development)
10. **DevOps, Infrastructure & External Integrations** — 9 skills — [jump](#10-devops-infrastructure--external-integrations)

---

## 1. Frontend Development & UI Engineering

> Skills for building, styling, and shipping production-grade web interfaces.
> **50 skills** in this category.

### `agent-browser`

- **Path**: `skills/agent-browser`
- **SKILL.md**: [`skills/agent-browser/SKILL.md`](skills/agent-browser/SKILL.md)
- **Title**: Browser Automation with agent-browser
- **Files**: 1
- **Structure**: flat

> A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands. Is a better choice for AI agent workflows - compact snapshots save tokens, the auth vault handles credentials securely, and React DevTools integration is valuable for frontend debugging.

### `api-and-interface-design`

- **Path**: `skills/api-and-interface-design`
- **SKILL.md**: [`skills/api-and-interface-design/SKILL.md`](skills/api-and-interface-design/SKILL.md)
- **Title**: API and Interface Design
- **Files**: 1
- **Structure**: flat

> Guides stable API and interface design. Use when designing APIs, module boundaries, or any public interface. Use when creating REST or GraphQL endpoints, defining type contracts between modules, or establishing boundaries between frontend and backend.

### `astro-7`

- **Path**: `skills/astro-7`
- **SKILL.md**: [`skills/astro-7/SKILL.md`](skills/astro-7/SKILL.md)
- **Title**: Astro 5/6/7 — Content-Focused Web Framework (Islands Architecture)
- **License**: Proprietary. LICENSE.txt has complete terms
- **Files**: 8
- **Structure**: flat

> Astro — content-focused web framework (islands architecture). Server-first, zero JS by default — Astro components render to static HTML at build time, hydration opt-in per island via client:load/client:idle/client:visible/client:only/client:media. Covers multi-framework islands (React, Vue, Svelte, Preact, Solid via @astrojs/*), Content Layer API & Live Content Collections (glob/file/external loaders, Zod schemas), file-based routing + layouts + View Transitions + Server Islands, middleware/Endpoints/Sessions/Actions, astro:env + astro:assets (Image/Picture/Font) + i18n + route caching, and...

### `astro-7-patterns`

- **Path**: `skills/astro-7-patterns`
- **SKILL.md**: [`skills/astro-7-patterns/SKILL.md`](skills/astro-7-patterns/SKILL.md)
- **Title**: Astro 7 Patterns — Field Notes from a Production Clone Build
- **Version**: 1.4
- **Files**: 1
- **Structure**: flat

> Astro 7 supplement skill — distilled patterns, anti-patterns, troubleshooting playbooks, and hard-won lessons from a production clone build. Covers the Astro 7 Rust compiler's strict apostrophe handling, Content Layer + Zod 4 imports, View Transitions script re-initialization, Fonts API + Tailwind 4 @theme integration, headroom sticky headers, vanilla JS carousels, mobile menu accessibility, dark/light section systems, and design extraction via agent-browser. Use when building a real Astro 7 site (not just reading docs) — every pattern below was debugged in a live build. Pairs with the cano...

### `authjs-vs-better-auth`

- **Path**: `skills/authjs-vs-better-auth`
- **SKILL.md**: [`skills/authjs-vs-better-auth/SKILL.md`](skills/authjs-vs-better-auth/SKILL.md)
- **Title**: authjs-vs-better-auth
- **Version**: 1.0.0
- **Files**: 1
- **Structure**: flat

> Compares Auth.js v5 and Better Auth for Next.js 16 projects. Side-by-side code for instance setup, route handlers, client auth, and server sessions. Database schema mapping for migration. Proxy.ts route protection pattern. Use when choosing an auth library, migrating from Auth.js to Better Auth, implementing proxy.ts checks, or debugging Next.js 16 auth issues.

### `avant-garde-design-v4`

- **Path**: `skills/avant-garde-design-v4`
- **SKILL.md**: [`skills/avant-garde-design-v4/SKILL.md`](skills/avant-garde-design-v4/SKILL.md)
- **Title**: Avant-Garde Web Design Skill v4.0
- **Files**: 21
- **Structure**: `references/`

> Elite web design skill for producing distinctive, production-grade frontend interfaces. Use when: (1) Building new web UI from scratch, (2) Creating luxury/premium brand experiences, (3) Designing landing pages, marketing sites, or product showcases, (4) Reviewing UI designs for Anti-Generic compliance, (5) Establishing design direction for a project, (6) Migrating from Tailwind v3 to v4, (7) Debugging mobile navigation issues, (8) User asks for "avant-garde", "distinctive", "non-generic", "luxury", or "premium" design. Triggers on phrases like "create a beautiful website", "design a landin...

### `brutalist-portfolio-nextjs`

- **Path**: `skills/brutalist-portfolio-nextjs`
- **SKILL.md**: [`skills/brutalist-portfolio-nextjs/SKILL.md`](skills/brutalist-portfolio-nextjs/SKILL.md)
- **Title**: Nicholas Yun — The Engineered Soul: Complete Skill Reference (v6)
- **Files**: 2
- **Structure**: flat

> Complete Next.js 16 + React 19 + TypeScript strict brutalist portfolio reference. App Router, Server Components, 16 components, design system with Tailwind v4 CSS-first @theme, 8+ remediation phases, 52 lessons learned. Covers WCAG AAA accessibility, custom hooks, anti-pattern debugging, before/after debugging, mobile nav debugging. Use when building brutalist/avant-garde portfolio sites or reconstructing a production-grade Next.js portfolio from scratch.

**Sub-skills / templates (1):**

| Name | Path | Description |
|------|------|-------------|
| `rutalist-portfolio-nextjs` | `skills/brutalist-portfolio-nextjs/rutalist-portfolio-nextjs` | Build, port, or remediate an avant-garde, anti-generic personal portfolio using Next.js 16 App Router with a Tactile Brutalism + High-End Editorial design system. Covers the complete architectural lifecycle from Vite SPA migration through four remediation phases to production: CSS-first design tokens with dual-theme (Night/Day), client-side SPA orchestrator embedded in Next.js, hash-based routing with keyboard focus management, lazy-loaded sections with ErrorBoundary + Suspense, optional database with graceful null handling, WCAG AAA accessibility (discriminated union API responses, ARIA, r... |

### `charts`

- **Path**: `skills/charts`
- **SKILL.md**: [`skills/charts/SKILL.md`](skills/charts/SKILL.md)
- **Title**: Beautiful Charts
- **Author**: Z.AI
- **Version**: 1.0
- **License**: Proprietary. LICENSE.txt has complete terms
- **Files**: 12
- **Structure**: `references/`, `setup.sh`

> Professional chart and diagram creation skill. Covers all types of visual data representation and structural diagrams: - **Data charts**: bar charts, line charts, pie charts, scatter plots, heatmaps, radar charts, candlestick charts, boxplots, histograms, area charts, waterfall charts, regression plots, distribution plots, and statistical visualizations. - **Structural diagrams**: flowcharts, mind maps, tree diagrams, org charts, architecture diagrams, network/relationship graphs, ER diagrams, class diagrams, Gantt charts, swimlane diagrams, and sequence diagrams. - **Dashboards**: data das...

### `clone-app-pat-pro`

- **Path**: `skills/clone-app-pat-pro`
- **SKILL.md**: [`skills/clone-app-pat-pro/SKILL.md`](skills/clone-app-pat-pro/SKILL.md)
- **Title**: Clone App — Pat Pro
- **Files**: 16
- **Structure**: `scripts/`, `references/`

> Clones any web app pixel-for-pixel from a URL. Runs as an IN-CONVERSATION workflow — the live Claude orchestrates Task sub-agents and drives the Claude Chrome extension to recon (every view), extract (computed styles = ground truth), design-spec, build, QA (computed-style assertions), and extend. Guided check-ins, custom features, and an MCP server so an agent can operate the app. Use when cloning a site, replicating a web app, building a clone, copying a website, recreating a UI, or when told "clone this", "replicate this app", "copy this site", "build a clone of", "make a copy of this web...

### `cloudflare-tunnel`

- **Path**: `skills/cloudflare-tunnel`
- **SKILL.md**: [`skills/cloudflare-tunnel/SKILL.md`](skills/cloudflare-tunnel/SKILL.md)
- **Title**: Cloudflare Tunnel Service Management
- **Files**: 1
- **Structure**: flat

> Add new local services to an existing Cloudflare Tunnel for secure public access. Use when you need to expose a local development server, web application, or service running on localhost to the public internet via Cloudflare's tunnel infrastructure. Prerequisites: cloudflared installed and authenticated, existing tunnel created. Triggers: "add tunnel", "expose local service", "cloudflare tunnel", "port forward", "public access to localhost", "expose localhost".

### `design`

- **Path**: `skills/design`
- **SKILL.md**: [`skills/design/SKILL.md`](skills/design/SKILL.md)
- **Title**: Design Skill
- **Files**: 561
- **Structure**: flat

> Route design-related HTML artifact tasks to the right artifact skill, reference, design system generation, or export skill.

### `e-commerce-nextjs16-monorepo`

- **Path**: `skills/e-commerce-nextjs16-monorepo`
- **SKILL.md**: [`skills/e-commerce-nextjs16-monorepo/SKILL.md`](skills/e-commerce-nextjs16-monorepo/SKILL.md)
- **Title**: Scandi Haven — Master Engineering Skill
- **Version**: 1.0.0
- **Files**: 1
- **Structure**: flat

> Production-grade reference for building DTC e-commerce and storefront platforms on Next.js 16 + React 19 + Tailwind CSS v4 (CSS-first @theme) + Drizzle ORM + PostgreSQL 17 in a pnpm + Turborepo monorepo with TypeScript strict. Covers App Router RSC/Server Actions, proxy.ts, Better Auth with RBAC, Stripe SAQ-A payments and webhooks, Zod validation, Zustand client islands, shadcn/Radix UI, and end-to-end commerce engine (catalog, cart, pricing, promotions, inventory, orders, shipping, tax, search FTS, jobs). Includes reusable patterns for monorepo layering (transpilePackages), security harden...

### `finance`

- **Path**: `skills/finance`
- **SKILL.md**: [`skills/finance/SKILL.md`](skills/finance/SKILL.md)
- **Title**: Finance Skill
- **Files**: 2
- **Structure**: flat

> Comprehensive Finance API integration skill for real-time and historical financial data analysis, market research, and investment decision-making. Priority use cases: stock price queries, market data analysis, company financial information, portfolio tracking, market news retrieval, stock screening, technical analysis, and any financial market-related requests. This skill should be the primary choice for all Finance API interactions and financial data needs.

### `frontend-design`

- **Path**: `skills/frontend-design`
- **SKILL.md**: [`skills/frontend-design/SKILL.md`](skills/frontend-design/SKILL.md)
- **Title**: Frontend Design System
- **Files**: 12
- **Structure**: `scripts/`, `references/`

> Design thinking and decision-making for web UI. Use when designing components, layouts, color schemes, typography, or creating aesthetic interfaces. Teaches principles, not fixed values.

### `frontend-development`

- **Path**: `skills/frontend-development`
- **SKILL.md**: [`skills/frontend-development/SKILL.md`](skills/frontend-development/SKILL.md)
- **Title**: Frontend Development Guidelines
- **Files**: 11
- **Structure**: flat

> Frontend development guidelines for React/TypeScript applications. Modern patterns including Suspense, lazy loading, useSuspenseQuery, file organization with features directory, MUI v7 styling, TanStack Router, performance optimization, and TypeScript best practices. Use when creating components, pages, features, fetching data, styling, routing, or working with frontend code.

### `frontend-ui-engineering`

- **Path**: `skills/frontend-ui-engineering`
- **SKILL.md**: [`skills/frontend-ui-engineering/SKILL.md`](skills/frontend-ui-engineering/SKILL.md)
- **Title**: Frontend UI Engineering
- **Files**: 1
- **Structure**: flat

> Builds production-quality UIs. Use when building or modifying user-facing interfaces. Use when creating components, implementing layouts, managing state, or when the output needs to look and feel production-quality rather than AI-generated.

### `frontend-ui-testing-journey`

- **Path**: `skills/frontend-ui-testing-journey`
- **SKILL.md**: [`skills/frontend-ui-testing-journey/SKILL.md`](skills/frontend-ui-testing-journey/SKILL.md)
- **Title**: Frontend UI Testing Journey
- **Files**: 2
- **Structure**: `references/`

> Complete frontend UI testing, verification, troubleshooting, and resolution journey. Covers testing methodology, browser automation with four tools (OpenClaw browser, agent-browser CLI, chrome-devtools-mcp, @playwright/mcp), common patterns, troubleshooting guides, and lessons learned from real-world testing.

### `fullstack-dev`

- **Path**: `skills/fullstack-dev`
- **SKILL.md**: [`skills/fullstack-dev/SKILL.md`](skills/fullstack-dev/SKILL.md)
- **Title**: Fullstack Web Development Skill
- **Files**: 1
- **Structure**: flat

> Full-stack Next.js 16 + React 19 + TypeScript strict with Tailwind CSS v4, shadcn/ui, Prisma ORM. Covers App Router, Server Components, API routes, WebSocket/Socket.io, database schemas, full project scaffolding. Use when building web apps, creating UI components, setting up databases, or implementing full-stack TypeScript with Next.js and Prisma.

### `image-search`

- **Path**: `skills/image-search`
- **SKILL.md**: [`skills/image-search/SKILL.md`](skills/image-search/SKILL.md)
- **Title**: image-search (ZAI in-house, via z-ai SDK)
- **Version**: 1.0.0
- **Files**: 1
- **Structure**: flat

> ZAI in-house image search service, exposed through the z-ai-web-dev-sdk CLI. Retrieve real images from the web for any text query, with optional short captions, and get back OSS-hosted direct URLs that are guaranteed reachable. Use when the user wants to find, fetch, illustrate, or embed images — e.g. "search for images of X", "find a picture of Y", "I need cover art for Z", "give me reference photos of W", "插图", "配图", "找图", "找张图", "搜张图", "搜图".

### `laravel-12`

- **Path**: `skills/laravel-12`
- **SKILL.md**: [`skills/laravel-12/SKILL.md`](skills/laravel-12/SKILL.md)
- **Title**: Laravel 12 — Full-Stack PHP Workflow Skill
- **License**: Proprietary. LICENSE.txt has complete terms
- **Files**: 1
- **Structure**: flat

> Laravel 12 (PHP 8.3+) full-stack workflow skill. Covers the streamlined 11+/12 app structure (no Kernel.php, bootstrap/app.php config), Eloquent ORM with factories/seeders, Artisan CLI, Blade + Livewire + Inertia frontend options, Sanctum API tokens, Breeze/Jetstream auth scaffolding, Queues with Redis/database, Pest testing, Vite asset build, Filament admin, Forge/Vapor deployment. Use when building any PHP web application, API, or console workload on Laravel 12 — especially when the task involves migrations, Eloquent queries, queued jobs, or auth flows where idiomatic Laravel differs from...

### `nextjs-postgresql-single-app`

- **Path**: `skills/nextjs-postgresql-single-app`
- **SKILL.md**: [`skills/nextjs-postgresql-single-app/SKILL.md`](skills/nextjs-postgresql-single-app/SKILL.md)
- **Title**: home-financing (ModFii) — Production Web App Skill
- **Version**: 1.8.0
- **Files**: 1
- **Structure**: flat

> Production-grade reference for building content-driven marketing sites and transactional funnel apps on Next.js 16 + React 19 + Tailwind CSS v4 (CSS-first @theme) + Drizzle ORM + PostgreSQL 17 in a single-app (npm, no monorepo) with TypeScript strict. Covers App Router RSC (force-dynamic), file corpus → catalog → idempotent ensureSeeded() projection → Pool singleton (globalThis), Drizzle pgTable migrations, 43 static/dynamic pages, lead-capture funnel (validate → match → persist), rate limiting, health/sitemap/redirects, editorial design tokens, and WCAG AAA. Includes reusable patterns for ...

### `nextjs-react-expert`

- **Path**: `skills/nextjs-react-expert`
- **SKILL.md**: [`skills/nextjs-react-expert/SKILL.md`](skills/nextjs-react-expert/SKILL.md)
- **Title**: Next.js & React Performance Expert
- **Files**: 11
- **Structure**: `scripts/`

> React 19 and Next.js 16 performance optimization from Vercel Engineering. 57 rules prioritized by impact - eliminate waterfalls, reduce bundle size, server/client-side optimizations. Covers App Router, Server Components, RSC streaming, Turbopack, React Compiler, Core Web Vitals (LCP/INP/CLS), bundle analysis. Use when profiling, reviewing code for perf issues, or optimizing production React/Next.js apps.

### `nextjs-typescript-patterns`

- **Path**: `skills/nextjs-typescript-patterns`
- **SKILL.md**: [`skills/nextjs-typescript-patterns/SKILL.md`](skills/nextjs-typescript-patterns/SKILL.md)
- **Title**: Consolidated Agent Briefing Document and Programming Handbook
- **Version**: 1.6
- **Files**: 4
- **Structure**: flat

> Monorepo web projects using pnpm, Turborepo, TypeScript, Next.js, React, ESLint, Prettier, Drizzle ORM, Postgres, and third-party SDKs (tRPC, Trigger.dev, Stripe, Better Auth, Sanity, React Email, Vitest)

### `nextjs16-full-stack`

- **Path**: `skills/nextjs16-full-stack`
- **SKILL.md**: [`skills/nextjs16-full-stack/SKILL.md`](skills/nextjs16-full-stack/SKILL.md)
- **Title**: Skills Knowledge Base — IRONFORGE Fitness Studio
- **Version**: 1.0
- **Files**: 1
- **Structure**: flat

> IRONFORGE Fitness Studio — Brutalist/Raw + Retro-Futuristic Design System & Next.js 16 Full-Stack Engineering Reference Production-grade skill for building IRONFORGE Fitness Studio from any AI agent. Covers - Avant-garde brutalist/raw design system with neon orange (#FF5400) on pure black (#0a0a0a) - Tailwind CSS v4 CSS-first @theme block, custom utilities, and v3→v4 migration rules - Anti-generic UI, typography scale (Bebas Neue / Oswald / Archivo / JetBrains Mono), and motion standards - Next.js 16 + React 19 App Router, Server Components, and 5-layer architecture (proxy → app → features ...

### `nextjs16-react19-next-auth5-drizzle-orm`

- **Path**: `skills/nextjs16-react19-next-auth5-drizzle-orm`
- **SKILL.md**: [`skills/nextjs16-react19-next-auth5-drizzle-orm/SKILL.md`](skills/nextjs16-react19-next-auth5-drizzle-orm/SKILL.md)
- **Title**: StoryIntoVideo — Engineering Skill Reference
- **Version**: 3.0.0
- **Files**: 1
- **Structure**: flat

> Full-stack Next.js 16 SaaS with React 19, Tailwind v4 CSS-first @theme, Auth.js v5, Drizzle ORM/Postgres (Neon), Inngest job queue, OpenAI + Replicate + ElevenLabs AI pipeline, Stripe billing, Cloudflare R2 storage, SSE streaming. 5-layer architecture (proxy → app → features → domain → lib), App Router Server Components, TypeScript strict, pnpm, Vitest + Playwright E2E, GitHub Actions CI. Luxury-dark cinematic design system with 13 CSS keyframes, WCAG AAA accessibility, server-side URL signing, env-configurable fail-open moderation. Production engineering reference with anti-patterns, debug...

### `nextjs16-react19-postgres17`

- **Path**: `skills/nextjs16-react19-postgres17`
- **SKILL.md**: [`skills/nextjs16-react19-postgres17/SKILL.md`](skills/nextjs16-react19-postgres17/SKILL.md)
- **Title**: OneStopNews — Engineering Skill Reference
- **Version**: 3.0.0
- **Files**: 1
- **Structure**: flat

> Full-stack Next.js 16 + React 19 + PostgreSQL 17 reference app with Drizzle ORM, BullMQ job queues (Redis), Auth.js v5, Vercel AI SDK (Anthropic + OpenAI), RSS/Atom ingestion, web push notifications. 5-layer architecture (proxy → app → features → domain → lib), App Router Server Components, async params, Suspense boundaries, PPR/cacheComponents, TypeScript strict + erasableSyntaxOnly, pnpm, Zod validation, Vitest + Playwright E2E + testcontainers. Editorial design system with CSS Subgrid, WCAG AAA accessibility, 3-layer AI provenance (JSON-LD + HTTP header + meta tag), Docker standalone out...

### `nextjs16-react19-tailwind4-auth5-video-gen`

- **Path**: `skills/nextjs16-react19-tailwind4-auth5-video-gen`
- **SKILL.md**: [`skills/nextjs16-react19-tailwind4-auth5-video-gen/SKILL.md`](skills/nextjs16-react19-tailwind4-auth5-video-gen/SKILL.md)
- **Title**: StoryIntoVideo — Complete Project Skill
- **Version**: 9.0
- **Files**: 2
- **Structure**: flat

> Production-grade Next.js 16 + React 19 + Tailwind CSS v4 full-stack SaaS. Covers App Router Server Components, TypeScript strict, CSS-first @theme design system, Drizzle ORM + PostgreSQL, Auth.js v5 authentication, job queue orchestration (Inngest/BullMQ), AI pipeline integration (OpenAI, Replicate, ElevenLabs), credit-based Stripe billing, Cloudflare R2 storage, SSE streaming, idempotent transactions, WCAG AAA accessibility, OWASP 2025 security hardening, Docker deployment, Vitest + Playwright testing, CI/CD, and live-site validation. Comprehensive engineering reference with audit history,...

### `nextjs16-react19-tailwind4-better-auth-monorepo`

- **Path**: `skills/nextjs16-react19-tailwind4-better-auth-monorepo`
- **SKILL.md**: [`skills/nextjs16-react19-tailwind4-better-auth-monorepo/SKILL.md`](skills/nextjs16-react19-tailwind4-better-auth-monorepo/SKILL.md)
- **Title**: Stillwater — Project Skill File
- **Version**: 1.0.0
- **Files**: 1
- **Structure**: flat

> Turborepo monorepo, Next.js 16.2, React 19, Tailwind v4.3, tRPC v11, Drizzle ORM 0.45, Better Auth 1.6.23, Stripe 22.3 (Dahlia), Trigger.dev v4, React Email 6.6, Resend, Sanity CMS v6. 651 tests, 11 ADRs, 93 lessons learned across 13 build phases.

### `nextjs16-react19-tailwind4-drizzle-orm-postgres17-rsc`

- **Path**: `skills/nextjs16-react19-tailwind4-drizzle-orm-postgres17-rsc`
- **SKILL.md**: [`skills/nextjs16-react19-tailwind4-drizzle-orm-postgres17-rsc/SKILL.md`](skills/nextjs16-react19-tailwind4-drizzle-orm-postgres17-rsc/SKILL.md)
- **Title**: Nave & Spire — SKILL.md
- **Version**: 1.2.0
- **Files**: 1
- **Structure**: flat

> Production-grade Next.js 16 + React 19 + Tailwind CSS v4 + Drizzle ORM + PostgreSQL 17 reference with App Router RSC (force-dynamic) — 3-layer architecture (App/RSC pages + Client islands + Domain/DB). Covers CSS-first @theme design system, editorial motion + a11y floor, file-backed typed seeds → idempotent ensureSeeded() → Drizzle pgTable (6-table pattern, Pool globalThis singleton, parallel queries + in-memory joins), manual validation, per-IP rate limiting, security headers/CSP, and hybrid CI + Vitest + live-DB verification. Use when building any content-driven, editorial, audit-journal,...

### `nextjs16-react19-tailwind4-full-stack`

- **Path**: `skills/nextjs16-react19-tailwind4-full-stack`
- **SKILL.md**: [`skills/nextjs16-react19-tailwind4-full-stack/SKILL.md`](skills/nextjs16-react19-tailwind4-full-stack/SKILL.md)
- **Title**: IRONFORGE — Project SKILL.md
- **Version**: 1.1.2
- **Files**: 1
- **Structure**: flat

> Production-grade Next.js 16 full-stack marketing website building with React 19, TypeScript strict, and Tailwind CSS v4 CSS-first @theme design system. Covers App Router Server Components, the 5-layer golden rule architecture (proxy → app → features → domain → lib), graceful degradation for infrastructure clients, Drizzle ORM with PostgreSQL and static fallback data, Auth.js v5 JWT authentication, Inngest step functions, Stripe Checkout payments, Replicate SDXL AI asset generation, Cloudflare R2 storage, Upstash rate limiting, and Zod 4 validation. Includes CSS-only animations, anti-generic...

### `nextjs16-tailwind4`

- **Path**: `skills/nextjs16-tailwind4`
- **SKILL.md**: [`skills/nextjs16-tailwind4/SKILL.md`](skills/nextjs16-tailwind4/SKILL.md)
- **Title**: Next.js + Tailwind CSS v4 Luxury Web Development
- **Files**: 1
- **Structure**: flat

> Luxury-grade Next.js 16 + React 19 + TypeScript strict with Tailwind CSS v4 CSS-first @theme, Radix UI (shadcn), and Framer Motion. Covers App Router, Server Components, avant-garde anti-generic UI design, OWASP 2025 security audits, Core Web Vitals performance optimization, WCAG AAA accessibility, mobile navigation debugging, and code review for high-end production web experiences.

### `personal-portfolio`

- **Path**: `skills/personal-portfolio`
- **SKILL.md**: [`skills/personal-portfolio/SKILL.md`](skills/personal-portfolio/SKILL.md)
- **Title**: The Engineered Soul — Portfolio Master Skill (v3.0.0)
- **License**: MIT
- **Version**: 3.0.0
- **Files**: 1
- **Structure**: flat

> Tactile Brutalist + High-End Editorial personal portfolio SPA with React 19, TypeScript 6 strict, Vite 6, Tailwind CSS v4 CSS-first @theme, pnpm. Covers complete lifecycle from scaffold to shipping: kinetic typography, hash-based routing, import.meta.glob content ingestion, dual-theme (night/day) design system, WCAG AAA accessibility, component-driven digital installation. Use when building a distinctive, anti-generic portfolio or personal site with React + Vite + Tailwind v4.

### `pptx-unified`

- **Path**: `skills/pptx-unified`
- **SKILL.md**: [`skills/pptx-unified/SKILL.md`](skills/pptx-unified/SKILL.md)
- **Title**: pptx-unified — A Practical Recipe for Impressive .pptx Decks
- **License**: MIT
- **Version**: 1.0.0
- **Author**: Claw Code (distilled from real build experience)
- **Files**: 13
- **Structure**: `scripts/`, `references/`

> Unified practical recipe for generating impressive marketing-grade .pptx presentations from scratch. Combines the canonical pptx skill's HTML-first 4-stage pipeline (Clarify → Research → Plan → Build → Export) with the variant skills' distinctive strengths (cyber-ppt's confirmation gates, pptx-generator's PptxGenJS templates, codex-ppt's image-based fallback) and 20+ real-world lessons/anti-patterns distilled from building a 12-slide deck for the my-pi-agent repo. Use this skill when ANY coding agent needs to produce a polished .pptx — it is the single starting point that routes to the righ...

### `prototype`

- **Path**: `skills/prototype`
- **SKILL.md**: [`skills/prototype/SKILL.md`](skills/prototype/SKILL.md)
- **Title**: Prototype
- **Files**: 4
- **Structure**: flat

> Build a throwaway prototype to answer a design question. Use when the user wants to sanity-check whether a state model or logic feels right, or explore what a UI should look like.

### `react19-ts6-vite8-tailwindv4-mvp`

- **Path**: `skills/react19-ts6-vite8-tailwindv4-mvp`
- **SKILL.md**: [`skills/react19-ts6-vite8-tailwindv4-mvp/SKILL.md`](skills/react19-ts6-vite8-tailwindv4-mvp/SKILL.md)
- **Title**: React 19 + TypeScript 6 + Vite 8 MVP — Production-Ready Web App Skill
- **License**: MIT
- **Version**: 3.0.0
- **Files**: 7
- **Structure**: flat

> MVP/production React 19 + TypeScript 6 strict + Vite 8 (Rolldown) + Tailwind CSS v4 CSS-first @theme. File-based routing, pnpm, Vitest + Playwright E2E. Covers complete lifecycle from scaffold to shipping tested, type-safe, WCAG AAA, production-grade code. Use when building new greenfield web apps with modern React + Vite + Tailwind v4.

### `sanity-best-practices`

- **Path**: `skills/sanity-best-practices`
- **SKILL.md**: [`skills/sanity-best-practices/SKILL.md`](skills/sanity-best-practices/SKILL.md)
- **Title**: Sanity Best Practices
- **Files**: 25
- **Structure**: `references/`

> Sanity development best practices for schema design, GROQ queries, TypeGen, Visual Editing, images, Portable Text, Studio structure, localization, migrations, Sanity Functions, Blueprints, and framework integrations such as Next.js, Nuxt, Astro, Remix, SvelteKit, Angular, Hydrogen, and the App SDK. Use this skill whenever working with Sanity schemas, defineType or defineField, GROQ or defineQuery, content modeling, Presentation or preview setups, Sanity-powered frontend integrations, Sanity Functions, documentEventHandler, defineDocumentFunction, defineMediaLibraryAssetFunction, @sanity/fun...

### `sanity-io-deploy`

- **Path**: `skills/sanity-io-deploy`
- **SKILL.md**: [`skills/sanity-io-deploy/SKILL.md`](skills/sanity-io-deploy/SKILL.md)
- **Title**: Sanity Studio: Setup, Configuration, Deployment & Verification (expanded, field-tested)
- **Files**: 1
- **Structure**: flat

> Sanity CMS + Next.js integration — end-to-end setup, deployment, and verification for a standalone Sanity Studio (sibling folder, never embedded) wired to an existing Next.js App Router app. Handles Sanity project auth and provider selection, schema validation and dangling-reference fixes, sanity schema deploy vs sanity deploy (Schema/Content Lake vs Studio UI at *.sanity.studio), viewer token and webhook secret minting, env wiring (NEXT_PUBLIC_SANITY_*), CORS origins, ISR webhook for revalidation, and live verification via Content Lake GROQ query + fresh headless-browser check. Use when co...

### `sanity-migration`

- **Path**: `skills/sanity-migration`
- **SKILL.md**: [`skills/sanity-migration/SKILL.md`](skills/sanity-migration/SKILL.md)
- **Title**: Sanity Migration
- **Files**: 10
- **Structure**: `references/`

> Plans, implements, and reviews migrations from other CMSes and content systems into Sanity. Use when migrating or replatforming to Sanity from AEM, Adobe Experience Manager, Contentful, Strapi, Webflow, WordPress, Payload, Drupal, Markdown/MDX/frontmatter files, WXR/XML exports, CMS APIs, database dumps, static HTML, or when designing extraction, transformation, Portable Text conversion, asset migration, redirects, validation, and cutover workflows.

### `scaffold-ui`

- **Path**: `skills/scaffold-ui`
- **SKILL.md**: [`skills/scaffold-ui/SKILL.md`](skills/scaffold-ui/SKILL.md)
- **Title**: scaffold-ui
- **Files**: 1
- **Structure**: flat

> Generates an anti-generic React component with brutalist styling and strict DOM hygiene.

### `static-spa-parish-site`

- **Path**: `skills/static-spa-parish-site`
- **SKILL.md**: [`skills/static-spa-parish-site/SKILL.md`](skills/static-spa-parish-site/SKILL.md)
- **Title**: Parish Site Engineering Skill — Unified v3 (Church of the Risen Christ, Toa Payoh — canonical instance)
- **Version**: 3.0.0
- **Files**: 15
- **Structure**: flat

> Complete engineering reference for static SPA parish/church/nonprofit/community brochure sites — React 19 + Vite 7 + Tailwind CSS v4 CSS-first @theme + TypeScript + HashRouter + vite-plugin-singlefile (single dist/index.html for GH Pages/S3, no SSR/CMS). Covers design system, component architecture, file-backed typed content, routing alias/anchor contracts, WCAG AAA, and pre-ship gates. Use when building, extending, debugging, onboarding, cloning, replicating, re-porting this parish-site family or scaffolding any static content-driven marketing/brochure/landing site template.

### `super-frontend-design`

- **Path**: `skills/super-frontend-design`
- **SKILL.md**: [`skills/super-frontend-design/SKILL.md`](skills/super-frontend-design/SKILL.md)
- **Title**: Super Frontend Design (Master Skill)
- **License**: MIT
- **Version**: 1.0.0
- **Files**: 18
- **Structure**: `scripts/`, `references/`

> Master frontend UI/UX design and development skill combining the top 10 validated skills. Covers anti-generic strategy, Next.js 16 + React 19 + Tailwind v4 CSS-first @theme tech stack, design systems, component architecture, App Router Server Components, Vercel-grade performance, WCAG AAA accessibility, visual storytelling, and end-to-end quality assurance for production-grade web experiences.

### `svelte-5-sveltekit`

- **Path**: `skills/svelte-5-sveltekit`
- **SKILL.md**: [`skills/svelte-5-sveltekit/SKILL.md`](skills/svelte-5-sveltekit/SKILL.md)
- **Title**: Svelte 5 + SvelteKit 2 — Full-Stack TypeScript Workflow Skill
- **License**: Proprietary. LICENSE.txt has complete terms
- **Files**: 1
- **Structure**: flat

> Svelte 5 + SvelteKit 2 full-stack TypeScript workflow skill. Covers the runes reactivity model ($state, $derived, $effect, $props, $bindable) which is fundamentally different from React hooks, file-based routing with +page.svelte / +layout.svelte / +page.server.ts / +page.ts, form actions as the idiomatic mutation pattern (progressive enhancement), load functions (server vs universal), hooks.server.ts for request-level interception, $env modules for typed environment variables (static vs dynamic, private vs public), adapters for deployment targets (auto / node / static / cloudflare / vercel...

### `tailwind-patterns`

- **Path**: `skills/tailwind-patterns`
- **SKILL.md**: [`skills/tailwind-patterns/SKILL.md`](skills/tailwind-patterns/SKILL.md)
- **Title**: Tailwind CSS Patterns (v4 - 2025)
- **Files**: 1
- **Structure**: flat

> Tailwind CSS v4 principles. CSS-first configuration, container queries, modern patterns, design token architecture.

### `tools-cli`

- **Path**: `skills/tools-cli`
- **SKILL.md**: [`skills/tools-cli/SKILL.md`](skills/tools-cli/SKILL.md)
- **Title**: Tools CLI - Standalone file operation wrapper
- **Files**: 2
- **Structure**: flat

> Standalone CLI wrapper exposing Claude Code's core file operations (read, glob, grep, edit, write) as command-line utilities. Use for scripting and automation without requiring a full Claude session.

### `ui-styling`

- **Path**: `skills/ui-styling`
- **SKILL.md**: [`skills/ui-styling/SKILL.md`](skills/ui-styling/SKILL.md)
- **Title**: UI Styling Skill
- **License**: MIT
- **Version**: 1.0.0
- **Files**: 98
- **Structure**: `scripts/`, `references/`

> Create beautiful, accessible user interfaces with shadcn/ui components (built on Radix UI + Tailwind), Tailwind CSS utility-first styling, and canvas-based visual designs. Use when building user interfaces, implementing design systems, creating responsive layouts, adding accessible components (dialogs, dropdowns, forms, tables), customizing themes and colors, implementing dark mode, generating visual designs and posters, or establishing consistent styling patterns across applications.

### `ui-ux-pro-max`

- **Path**: `skills/ui-ux-pro-max`
- **SKILL.md**: [`skills/ui-ux-pro-max/SKILL.md`](skills/ui-ux-pro-max/SKILL.md)
- **Title**: ui-ux-pro-max
- **Files**: 56
- **Structure**: `scripts/`, `references/`

> UI/UX design intelligence and implementation guidance for building polished interfaces. Use when the user asks for UI design, UX flows, information architecture, visual style direction, design systems/tokens, component specs, copy/microcopy, accessibility, or to generate/critique/refine frontend UI (HTML/CSS/JS, React, Next.js, Vue, Svelte, Tailwind). Includes workflows for (1) generating new UI layouts and styling, (2) improving existing UI/UX, (3) producing design-system tokens and component guidelines, and (4) turning UX recommendations into concrete code changes.

### `version-management`

- **Path**: `skills/version-management`
- **SKILL.md**: [`skills/version-management/SKILL.md`](skills/version-management/SKILL.md)
- **Title**: 版本管理
- **Files**: 1
- **Structure**: flat

> 独立通用 Skill：管理前端项目全生命周期。只要任务**可能**写出 .html/.jsx/.tsx/.vue 入口文件，就必须在写出第一个文件**之前**读取并遵循本 Skill（用于确定落盘路径与项目目录），而不是产出之后才补救；即使用户没有提到"项目"或"版本"也要使用。同时响应用户的版本相关操作（查看历史、恢复版本、切换项目等）。

### `vue-3-nuxt`

- **Path**: `skills/vue-3-nuxt`
- **SKILL.md**: [`skills/vue-3-nuxt/SKILL.md`](skills/vue-3-nuxt/SKILL.md)
- **Title**: Vue 3 + Nuxt 4 — Full-Stack TypeScript Workflow Skill
- **License**: Proprietary. LICENSE.txt has complete terms
- **Files**: 1
- **Structure**: flat

> Vue 3.5+ (Composition API) + Nuxt 4 full-stack TypeScript workflow skill. Covers the reactivity system (ref vs reactive, computed, watch vs watchEffect, automatic dependency tracking — fundamentally different from React hooks' manual dependency arrays), Single File Components (.vue with <script setup>), Nuxt 4 project structure (app/ directory, server/api/, nuxt.config.ts), file-based routing with definePageMeta, layout system, data fetching (useFetch, useAsyncData, $fetch), server routes via Nitro engine, Pinia for state management (the modern Vuex successor), nuxt-auth (Auth.js wrapper) o...

### `web-frameworks`

- **Path**: `skills/web-frameworks`
- **SKILL.md**: [`skills/web-frameworks/SKILL.md`](skills/web-frameworks/SKILL.md)
- **Title**: Web Frameworks Skill Group
- **License**: MIT
- **Version**: 1.0.0
- **Files**: 18
- **Structure**: `scripts/`, `references/`

> Build modern full-stack web applications with Next.js 16 + React 19 (App Router, Server Components, RSC, PPR, cacheComponents, async params, SSR, SSG, ISR, standalone output), Turborepo (monorepo, task pipelines, remote caching, parallel execution), and RemixIcon (3100+ SVG icons). Use when creating React applications, implementing server-side rendering, setting up monorepos, optimizing build performance and caching, or working with TypeScript full-stack projects.

### `webapp-testing-journey`

- **Path**: `skills/webapp-testing-journey`
- **SKILL.md**: [`skills/webapp-testing-journey/SKILL.md`](skills/webapp-testing-journey/SKILL.md)
- **Title**: Webapp Testing Journey
- **Files**: 2
- **Structure**: `references/`

> Systematic web application testing methodology using OpenClaw browser tools, agent-browser CLI, and chrome-devtools-mcp. Use when testing web application user journeys, validating bug fixes, performing QA verification, or debugging frontend issues. Covers URL journey testing, accessibility tree analysis, DOM inspection, network request debugging, performance tracing, visual regression, and comprehensive issue verification. Triggers on phrases like "test this application", "verify the fix", "check if it works", "test the user journey", "debug this issue".

---

## 2. Design Artifacts & Visual Creation

> Skills that produce visual artifacts: charts, images, diagrams, design systems, and media.
> **16 skills** in this category.

### `aesthetic`

- **Path**: `skills/aesthetic`
- **SKILL.md**: [`skills/aesthetic/SKILL.md`](skills/aesthetic/SKILL.md)
- **Title**: Aesthetic
- **Files**: 7
- **Structure**: `references/`

> Create aesthetically beautiful interfaces following proven design principles. Use when building UI/UX, analyzing designs from inspiration sites, generating design images with ai-multimodal, implementing visual hierarchy and color theory, adding micro-interactions, or creating design documentation. Includes workflows for capturing and analyzing inspiration screenshots with chrome-devtools and ai-multimodal, iterative design image generation until aesthetic standards are met, and comprehensive design system guidance covering BEAUTIFUL (aesthetic principles), RIGHT (functionality/accessibility...

### `claude-design`

- **Path**: `skills/claude-design`
- **SKILL.md**: [`skills/claude-design/SKILL.md`](skills/claude-design/SKILL.md)
- **Title**: Claude Design
- **Files**: 40
- **Structure**: `references/`

> Produce thoughtful, high-fidelity design artifacts in HTML — landing pages, slide decks, interactive prototypes, animated videos, posters, wireframes, and visual explorations. Use for tasks like "design a landing page," "make a deck," "prototype this flow," "visualize this idea," or "create a poster." Enforces fact verification (WebSearch before assuming product details), Core Asset Protocol for branded work (logo/product shots/UI screenshots are first-class), Design Direction Advisor offering 3 directions when briefs are vague, and avoids AI-design tropes (aggressive gradients, emoji bulle...

### `code-quality-standards`

- **Path**: `skills/code-quality-standards`
- **SKILL.md**: [`skills/code-quality-standards/SKILL.md`](skills/code-quality-standards/SKILL.md)
- **Title**: Code Quality & Design Standards
- **Version**: 2.0.0
- **Files**: 1
- **Structure**: flat

> The absolute constitution for code quality and design rigor. Enforces a Six-Axis review (Correctness, Readability, Architecture, Security, Performance, and Aesthetic/UX Rigor). Use before merging any change, evaluating AI-generated code, or assessing technical debt. Rejects generic 'AI slop' aesthetics and enforces intentional, bespoke design.

### `comfyui-workflow-scaffold`

- **Path**: `skills/comfyui-workflow-scaffold`
- **SKILL.md**: [`skills/comfyui-workflow-scaffold/SKILL.md`](skills/comfyui-workflow-scaffold/SKILL.md)
- **Title**: ComfyUI Workflow Scaffold
- **Files**: 4
- **Structure**: `references/`

> Create valid ComfyUI workflow JSON templates for Apple Silicon image generation. Use when: (1) Building a new ComfyUI workflow from scratch, (2) Converting a prompt-API format workflow to saved-graph format, (3) Adding Mac-compatible model loading nodes (Z-Image, FLUX.1/2, Krea 2, Ideogram 4, Qwen-Image, FIBO, ERNIE-Image), (4) Scaffolding LoRA/ControlNet/VAE nodes correctly, (5) Validating a workflow will run on Mac MPS/MLX backend, (6) User asks "create a workflow", "scaffold a ComfyUI template", "workflow JSON", "ComfyUI node graph", or "image generation workflow". Triggers on keywords: ...

### `image-edit`

- **Path**: `skills/image-edit`
- **SKILL.md**: [`skills/image-edit/SKILL.md`](skills/image-edit/SKILL.md)
- **Title**: Image Edit Skill
- **License**: MIT
- **Files**: 3
- **Structure**: `scripts/`

> Implement AI image editing and modification capabilities using the z-ai-web-dev-sdk. Use this skill when the user needs to edit existing images, create variations, modify visual content, redesign assets, or transform images based on text descriptions. Supports multiple image sizes and returns base64 encoded results. Also includes CLI tool for quick image editing.

### `image-generation`

- **Path**: `skills/image-generation`
- **SKILL.md**: [`skills/image-generation/SKILL.md`](skills/image-generation/SKILL.md)
- **Title**: Image Generation Skill
- **License**: MIT
- **Files**: 3
- **Structure**: `scripts/`

> Implement AI image generation capabilities using the z-ai-web-dev-sdk. Use this skill when the user needs to create images from text descriptions, generate visual content, create artwork, design assets, or build applications with AI-powered image creation. Supports multiple image sizes and returns base64 encoded images. Also includes CLI tool for quick image generation.

### `image-understand`

- **Path**: `skills/image-understand`
- **SKILL.md**: [`skills/image-understand/SKILL.md`](skills/image-understand/SKILL.md)
- **Title**: Image Understanding Skill
- **License**: MIT
- **Files**: 3
- **Structure**: `scripts/`

> Implement specialized image understanding capabilities using the z-ai-web-dev-sdk. Use this skill when the user needs to analyze static images, extract visual information, perform OCR, detect objects, classify images, or understand visual content. Optimized for PNG, JPEG, GIF, WebP, and BMP formats.

### `kimi-docx`

- **Path**: `skills/kimi-docx`
- **SKILL.md**: [`skills/kimi-docx/SKILL.md`](skills/kimi-docx/SKILL.md)
- **Title**: Part 1: Goals
- **Files**: 29
- **Structure**: `scripts/`, `references/`

> Generate and edit Word documents (.docx). Supports professional documents including covers, charts, track-changes editing, and more. Suitable for any .docx creation or modification task.

### `kimi-pdf`

- **Path**: `skills/kimi-pdf`
- **SKILL.md**: [`skills/kimi-pdf/SKILL.md`](skills/kimi-pdf/SKILL.md)
- **Title**: Check environment (JSON output, exit code 0=ok, 2=missing deps)
- **Files**: 18
- **Structure**: `scripts/`, `routes/`

> Professional PDF solution. Create PDFs using HTML+Paged.js (academic papers, reports, documents). Process existing PDFs using Python (read, extract, merge, split, fill forms). Supports KaTeX math formulas, Mermaid diagrams, three-line tables, citations, and other academic elements. Also use this skill when user explicitly requests LaTeX (.tex) or native LaTeX compilation.

### `kimi-xlsx`

- **Path**: `skills/kimi-xlsx`
- **SKILL.md**: [`skills/kimi-xlsx/SKILL.md`](skills/kimi-xlsx/SKILL.md)
- **Title**: Create workbook
- **Files**: 3
- **Structure**: `scripts/`

> Specialized utility for advanced manipulation, analysis, and creation of spreadsheet files, including (but not limited to) XLSX, XLSM, CSV formats. Core functionalities include formula deployment, complex formatting (including automatic currency formatting for financial tasks), data visualization, and mandatory post-processing recalculation.

### `project-architecture-document-md`

- **Path**: `skills/project-architecture-document-md`
- **SKILL.md**: [`skills/project-architecture-document-md/SKILL.md`](skills/project-architecture-document-md/SKILL.md)
- **Title**: Project Architecture Document (PAD) Generator
- **Files**: 1
- **Structure**: flat

> Create a comprehensive Project Architecture Document (PAD) for any codebase. Use when the user asks to generate a PAD, architecture document, system design document, or technical blueprint for a project. Also triggers on "document this codebase", "create architecture reference", "generate system overview", "write ADR", "document the architecture of this project". Covers executive summary, tech stack with version pinning, Architecture Decision Records (ADRs), system topology diagrams, layer models, annotated directory structures, critical code patterns with invariants, database schemas, secu...

### `stock-analysis`

- **Path**: `skills/stock-analysis`
- **SKILL.md**: [`skills/stock-analysis/SKILL.md`](skills/stock-analysis/SKILL.md)
- **Title**: Stock Analysis Skill
- **Files**: 10
- **Structure**: flat

> Comprehensive stock market analysis skill covering A-share (China), Hong Kong, and US equities. Priority use cases: stock analysis and buy/sell/hold recommendations by ticker code, generating decision dashboards and research reports with technical/fundamental/sentiment analysis, position-aware investment strategies based on user's cost price, dividend income scoring and safety analysis, rumor and early market signal scanning (M&A, insider activity, analyst actions), watchlist management with price target and stop-loss alerts, and K-line chart pattern recognition from images. This skill shou...

### `video-generation`

- **Path**: `skills/video-generation`
- **SKILL.md**: [`skills/video-generation/SKILL.md`](skills/video-generation/SKILL.md)
- **Title**: Video Generation Skill
- **License**: MIT
- **Files**: 3
- **Structure**: `scripts/`

> Implement AI-powered video generation capabilities using the z-ai-web-dev-sdk. Use this skill when the user needs to generate videos from text prompts or images, create video content programmatically, or build applications that produce video outputs. Supports asynchronous task management with status polling and result retrieval.

### `video-understand`

- **Path**: `skills/video-understand`
- **SKILL.md**: [`skills/video-understand/SKILL.md`](skills/video-understand/SKILL.md)
- **Title**: Video Understanding Skill
- **License**: MIT
- **Files**: 3
- **Structure**: `scripts/`

> Implement specialized video understanding capabilities using the z-ai-web-dev-sdk. Use this skill when the user needs to analyze video content, understand motion and temporal sequences, extract information from video frames, describe video scenes, or perform video-based AI analysis. Optimized for MP4, AVI, MOV, and other common video formats.

### `web-shader-extractor`

- **Path**: `skills/web-shader-extractor`
- **SKILL.md**: [`skills/web-shader-extractor/SKILL.md`](skills/web-shader-extractor/SKILL.md)
- **Title**: Web Shader Extractor
- **Files**: 12
- **Structure**: `scripts/`, `references/`

> 从网页中提取 WebGL/Canvas/Shader 视觉特效代码，反混淆后移植为独立原生 JS 项目。 触发条件：用户提供网址并要求提取 shader、提取特效、提取动画效果、提取 canvas 效果、 复刻某网站的视觉效果、"把这个网站的背景效果扒下来" 等。

### `xlsx`

- **Path**: `skills/xlsx`
- **SKILL.md**: [`skills/xlsx/SKILL.md`](skills/xlsx/SKILL.md)
- **Title**: XLSX — Scene-Driven Spreadsheet Workbench
- **Author**: Z.AI
- **Version**: 1.0
- **License**: Proprietary. LICENSE.txt has complete terms
- **Files**: 21
- **Structure**: `scenes/`, `engines/`, `setup.sh`

> Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xlsx, .xlsm, .csv, or .tsv file; create a new spreadsheet from scratch or from other data sources; analyze data and output results as an Excel file with charts; convert between tabular file formats (CSV/JSON/PDF → XLSX or vice versa); clean, merge, pivot, or transform tabular data. Trigger especially when the user references a spreadsheet file by name or path, says 'make a table/report/model', mentions Excel/CSV/数据分析/报表/汇总, or wants da...

---

## 3. Full-Stack & Backend Development

> Skills for server-side frameworks, ORMs, API design, and full-stack patterns.
> **13 skills** in this category.

### `api-patterns`

- **Path**: `skills/api-patterns`
- **SKILL.md**: [`skills/api-patterns/SKILL.md`](skills/api-patterns/SKILL.md)
- **Title**: API Patterns
- **Files**: 12
- **Structure**: `scripts/`

> API design principles and decision-making. REST vs GraphQL vs tRPC selection, response formats, versioning, pagination.

### `context7-docs`

- **Path**: `skills/context7-docs`
- **SKILL.md**: [`skills/context7-docs/SKILL.md`](skills/context7-docs/SKILL.md)
- **Title**: Context7 Documentation Search
- **Files**: 1
- **Structure**: flat

> Search and retrieve up-to-date curated documentation from Context7 for any software, library, or package. Use when: (1) Need latest documentation for a specific library or tool, (2) Looking for code examples and patterns, (3) Need accurate API reference information, (4) Building workflows with specific tools like n8n, (5) Want to avoid hallucinated or outdated documentation. Triggers on phrases like "search Context7 for", "get documentation for", "find latest docs", "n8n workflow", "package documentation".

### `django-6`

- **Path**: `skills/django-6`
- **SKILL.md**: [`skills/django-6/SKILL.md`](skills/django-6/SKILL.md)
- **Title**: Django 6 — Full-Stack Python Workflow Skill
- **License**: Proprietary. LICENSE.txt has complete terms
- **Files**: 1
- **Structure**: flat

> Django 6.x (Python 3.12+, released August 2025 LTS) full-stack workflow skill. Covers the ORM with migrations (write Python, not SQL), Class-Based Views vs Function-Based Views decision, Django REST Framework (DRF) for APIs (Serializers, ViewSets, Routers), Django admin for free CRUD, async views with full async ORM support, Celery + Redis for background tasks, django-allauth for social auth, pytest-django for modern testing, split settings (base/dev/prod), ASGI deployment via Daphne/Uvicorn, WhiteNoise for static files, psycopg3 for PostgreSQL. Use when building any Python web application,...

### `framework-templates`

- **Path**: `skills/framework-templates`
- **SKILL.md**: [`skills/framework-templates/SKILL.md`](skills/framework-templates/SKILL.md)
- **Title**: Framework Templates
- **Version**: 2.0.0
- **Files**: 2
- **Structure**: flat

> Deep reference library for framework-specific CLAUDE.md sections. Contains production-ready templates for Next.js, Laravel, Rails, Django, React Native, Flutter, Go, Rust, and more. Use alongside the claude-md skill for complete CLAUDE.md generation.

### `kubernetes-env-setup`

- **Path**: `skills/kubernetes-env-setup`
- **SKILL.md**: [`skills/kubernetes-env-setup/SKILL.md`](skills/kubernetes-env-setup/SKILL.md)
- **Title**: Hardened Kubernetes on Azure Linux 3.0
- **Version**: 1.0
- **Files**: 8
- **Structure**: flat

> Production-grade self-managed Kubernetes cluster on Azure Linux 3.0 (kubeadm) with CIS/NSA/CISA-aligned hardening for agentic AI and LLM workloads. Covers host hardening (SELinux, Trusted Launch, OS Guard IPE), containerd, Cilium eBPF CNI, Kyverno policy-as-code, gVisor/Kata Containers sandboxing, cosign/Sigstore supply chain security, Falco runtime detection, Pod Security Admission, RBAC, secrets management, network segmentation, high availability (multi-AZ), backup with Velero, and compliance validation (kube-bench, Kubescape). Includes OWASP LLM Top 10 and MITRE ATLAS threat modeling for...

### `minimax-docx`

- **Path**: `skills/minimax-docx`
- **SKILL.md**: [`skills/minimax-docx/SKILL.md`](skills/minimax-docx/SKILL.md)
- **Title**: minimax-docx
- **License**: MIT
- **Version**: 1.0.0
- **Author**: MiniMaxAI
- **Files**: 75
- **Structure**: `scripts/`, `references/`

> Professional DOCX document creation, editing, and formatting using OpenXML SDK (.NET). Three pipelines: (A) create new documents from scratch, (B) fill/edit content in existing documents, (C) apply template formatting with XSD validation gate-check. MUST use this skill whenever the user wants to produce, modify, or format a Word document — including when they say "write a report", "draft a proposal", "make a contract", "fill in this form", "reformat to match this template", or any task whose final output is a .docx file. Even if the user doesn't mention "docx" explicitly, if the task implie...

### `n8n-workflow-automation`

- **Path**: `skills/n8n-workflow-automation`
- **SKILL.md**: [`skills/n8n-workflow-automation/SKILL.md`](skills/n8n-workflow-automation/SKILL.md)
- **Title**: n8n Workflow Automation
- **Files**: 6
- **Structure**: `references/`

> Build and automate n8n workflows using JSON specification. Use when: (1) Creating n8n workflows programmatically, (2) Converting workflows to/from JSON, (3) Understanding n8n node types and connections, (4) Writing n8n expressions, (5) Debugging workflow JSON structure, (6) Building workflow templates. Triggers on phrases like "n8n workflow", "n8n JSON", "n8n expression", "webhook workflow", "n8n automation".

### `powershell-windows`

- **Path**: `skills/powershell-windows`
- **SKILL.md**: [`skills/powershell-windows/SKILL.md`](skills/powershell-windows/SKILL.md)
- **Title**: PowerShell Windows Patterns
- **Files**: 1
- **Structure**: flat

> PowerShell Windows patterns. Critical pitfalls, operator syntax, error handling.

### `python-patterns`

- **Path**: `skills/python-patterns`
- **SKILL.md**: [`skills/python-patterns/SKILL.md`](skills/python-patterns/SKILL.md)
- **Title**: Python Patterns
- **Files**: 1
- **Structure**: flat

> Python development principles and decision-making. Framework selection, async patterns, type hints, project structure. Teaches thinking, not copying.

### `react19-vite-spa-fastify-drizzle-sqlite`

- **Path**: `skills/react19-vite-spa-fastify-drizzle-sqlite`
- **SKILL.md**: [`skills/react19-vite-spa-fastify-drizzle-sqlite/SKILL.md`](skills/react19-vite-spa-fastify-drizzle-sqlite/SKILL.md)
- **Title**: reddit-clone SKILL — Engineering Reference for Full-Stack TypeScript Monorepos
- **Version**: 1.1.0
- **Files**: 1
- **Structure**: flat

> npm-workspaces monorepo reference for reddit-clone (embers): React 19 + Vite 7 SPA with HashRouter and vite-plugin-singlefile (single HTML deploy to GitHub Pages or S3), Tailwind CSS v4 CSS-first, Zustand overlay pattern, Fastify 5 composition-root buildApp, Drizzle ORM 0.36 + SQLite + better-sqlite3 + FTS5, Zod schemas at every boundary, JWT HS256 via jose + argon2id, pino logging, TypeScript 5.9 strict, ESLint 9 flat, Vitest and Playwright. Use when building a full-stack TypeScript monorepo, a deploy-anywhere static SPA with deterministic PRNG client data and a real Fastify backend, a com...

### `security-and-hardening`

- **Path**: `skills/security-and-hardening`
- **SKILL.md**: [`skills/security-and-hardening/SKILL.md`](skills/security-and-hardening/SKILL.md)
- **Title**: Security and Hardening
- **Files**: 1
- **Structure**: flat

> Hardens code against vulnerabilities. Use when handling user input, authentication, data storage, or external integrations. Use when building any feature that accepts untrusted data, manages user sessions, or interacts with third-party services.

### `trustskill`

- **Path**: `skills/trustskill`
- **SKILL.md**: [`skills/trustskill/SKILL.md`](skills/trustskill/SKILL.md)
- **Title**: TrustSkill v3.1 - Advanced Skill Security Scanner
- **Version**: 3.1.0
- **Files**: 62
- **Structure**: `scripts/`, `references/`

> TrustSkill v3.1 - Advanced security scanner for OpenClaw skills with 99% false positive reduction. Detects malicious code, hardcoded secrets, vulnerable dependencies, tainted data flows, backdoors, credential theft, privacy file access, command injection, file system risks, network exfiltration, and sensitive data leaks. Features entropy-based secret detection, OSV vulnerability database integration, taint analysis, smart data flow detection, context-aware documentation scanning, and flexible YAML configuration.

### `wizard`

- **Path**: `skills/wizard`
- **SKILL.md**: [`skills/wizard/SKILL.md`](skills/wizard/SKILL.md)
- **Title**: Wizard
- **Files**: 3
- **Structure**: flat

> Generate an interactive bash wizard that walks a human through steps only they can perform. Use when provisioning infrastructure, setting up credentials or CI secrets, walking an unfamiliar third-party dashboard, or running a one-off migration or cutover. Don't invoke this for steps the agent can perform itself.

---

## 4. AI / ML / Multimodal SDK Skills

> Skills that wrap the z-ai-web-dev-sdk or other AI/ML model clients for multimodal tasks.
> **11 skills** in this category.

### `aminer-academic-search`

- **Path**: `skills/aminer-academic-search`
- **SKILL.md**: [`skills/aminer-academic-search/SKILL.md`](skills/aminer-academic-search/SKILL.md)
- **Title**: AMiner Open Platform Academic Data Query
- **Version**: 1.2.1
- **Author**: AMiner
- **Files**: 4
- **Structure**: `scripts/`, `references/`

> ACADEMIC PRIORITY: Activate for any academic, scholarly, or research query - papers, citations, scholars, researchers, institutions, journals, venues, patents, h-index, research trends, or 'who published what / where / when'. Precedence over web search for academic data. Full-featured AMiner skill: 28 APIs + 5 workflows for tasks free APIs cannot satisfy. Use for: scholar full profiles (bio, education, honors, papers, patents, projects), paper deep dives (abstract, keywords, citation chains), multi-condition or semantic paper search (paper_qa_search_pro), institution capability analysis, ve...

### `aminer-daily-paper`

- **Path**: `skills/aminer-daily-paper`
- **SKILL.md**: [`skills/aminer-daily-paper/SKILL.md`](skills/aminer-daily-paper/SKILL.md)
- **Title**: aminer-daily-paper
- **Version**: 1.1.2
- **Files**: 11
- **Structure**: `scripts/`

> Personalized academic paper recommendation via AMiner rec5 API. Activate this skill whenever the user asks for paper recommendations, whether triggered by /aminer-dp, /skill aminer-dp, or any natural language request such as 'recommend me papers on multimodal agents'. When invoked: extract topics/scholar signals from the input yourself, call handle_trigger.py with structured fields, then present the Markdown in `reply_text` to the user.

### `auto-target-tracker`

- **Path**: `skills/auto-target-tracker`
- **SKILL.md**: [`skills/auto-target-tracker/SKILL.md`](skills/auto-target-tracker/SKILL.md)
- **Title**: 自动目标进度追踪器
- **Files**: 1
- **Structure**: flat

> 自动目标进度追踪器。在对话中检测到目标相关图片（笔记、进度、截图、记录）时，自动调用 VLM 识别关键信息并记录到目标日记。适用于学习管理、健身追踪、工作进度、习惯养成、创作记录等所有目标管理场景。

### `browser-automation`

- **Path**: `skills/browser-automation`
- **SKILL.md**: [`skills/browser-automation/SKILL.md`](skills/browser-automation/SKILL.md)
- **Title**: browser-automation
- **Files**: 1
- **Structure**: flat

> Fast browser automation CLI for AI agents using Chrome/Chromium via CDP. Use when automating web interactions, taking snapshots, filling forms, navigating pages, or testing web applications without Playwright/Puppeteer dependency.

### `llm`

- **Path**: `skills/llm`
- **SKILL.md**: [`skills/llm/SKILL.md`](skills/llm/SKILL.md)
- **Title**: LLM (Large Language Model) Skill
- **License**: MIT
- **Files**: 3
- **Structure**: `scripts/`

> Implement large language model (LLM) chat completions using the z-ai-web-dev-sdk. Use this skill when the user needs to build conversational AI applications, chatbots, AI assistants, or any text generation features. Supports multi-turn conversations, system prompts, and context management.

### `mac-mlx-local-inference`

- **Path**: `skills/mac-mlx-local-inference`
- **SKILL.md**: [`skills/mac-mlx-local-inference/SKILL.md`](skills/mac-mlx-local-inference/SKILL.md)
- **Title**: 🚀 Complete Guide: OpenAI-Compatible MLX Endpoint on Apple Silicon
- **Version**: 1.0
- **Files**: 1
- **Structure**: flat

> Local LLM inference on Apple Silicon (M1-M5) using mlx-optiq with OpenAI/Anthropic-compatible API endpoints. Covers Qwen3.6-27B setup, mixed-precision KV cache, MTP speculative decoding, and coding agent integrations (OpenCode, Kilo Code, Pi Agent, Claude Code, Codex, Cursor). Fully offline, zero cloud dependency.

### `microsoft-foundry`

- **Path**: `skills/microsoft-foundry`
- **SKILL.md**: [`skills/microsoft-foundry/SKILL.md`](skills/microsoft-foundry/SKILL.md)
- **Title**: Microsoft Foundry Skill
- **License**: MIT
- **Author**: Microsoft
- **Version**: 1.1.44
- **Files**: 164
- **Structure**: `references/`

> Deploy, evaluate, fine-tune, and manage Foundry agents end-to-end with azd: hosted agent scaffold/run/deploy, prompt agent create, batch eval, continuous eval, prompt optimizer, Agent Optimizer scaffold, agent.yaml, dataset curation from traces, model fine-tuning (SFT/DPO/RFT). USE FOR: azd ai agent, azd provision/deploy, deploy agent, hosted agent, create agent, add tool to agent, invoke agent, evaluate agent, continuous eval, continuous monitoring, agent CI/CD, optimize prompt, improve prompt, optimize agent instructions, agent optimizer, deploy model, Foundry project, RBAC, role assignme...

**Sub-skills / templates (1):**

| Name | Path | Description |
|------|------|-------------|
| `finetuning` | `skills/microsoft-foundry/finetuning` | Fine-tune models on Azure AI Foundry using SFT (supervised), DPO (preference), or RFT (reinforcement with graders). Covers dataset preparation, training job submission, deployment, and evaluation. USE FOR: fine-tune, SFT, DPO, RFT, training data, grader, distillation, fine-tuned model, training job, large file upload, calibrate grader, deploy fine-tuned model, evaluate fine-tuned model. DO NOT USE FOR: general model deployment without fine-tuning (use deploy-model), agent creation (use agents), prompt optimization without training (use prompt-optimizer). |

### `minimax-pdf`

- **Path**: `skills/minimax-pdf`
- **SKILL.md**: [`skills/minimax-pdf/SKILL.md`](skills/minimax-pdf/SKILL.md)
- **Title**: minimax-pdf
- **License**: MIT
- **Version**: 1.0
- **Files**: 12
- **Structure**: `scripts/`

> Use this skill when visual quality and design identity matter for a PDF. CREATE (generate from scratch): "make a PDF", "generate a report", "write a proposal", "create a resume", "beautiful PDF", "professional document", "cover page", "polished PDF", "client-ready document". FILL (complete form fields): "fill in the form", "fill out this PDF", "complete the form fields", "write values into PDF", "what fields does this PDF have". REFORMAT (apply design to an existing doc): "reformat this document", "apply our style", "convert this Markdown/text to PDF", "make this doc look good", "re-style t...

### `minimax-xlsx`

- **Path**: `skills/minimax-xlsx`
- **SKILL.md**: [`skills/minimax-xlsx/SKILL.md`](skills/minimax-xlsx/SKILL.md)
- **Title**: MiniMax XLSX Skill
- **License**: MIT
- **Version**: 1.0
- **Files**: 25
- **Structure**: `scripts/`, `references/`

> Open, create, read, analyze, edit, or validate Excel/spreadsheet files (.xlsx, .xlsm, .csv, .tsv). Use when the user asks to create, build, modify, analyze, read, validate, or format any Excel spreadsheet, financial model, pivot table, or tabular data file. Covers: creating new xlsx from scratch, reading and analyzing existing files, editing existing xlsx with zero format loss, formula recalculation and validation, and applying professional financial formatting standards. Triggers on 'spreadsheet', 'Excel', '.xlsx', '.csv', 'pivot table', 'financial model', 'formula', or any request to prod...

### `web-reader`

- **Path**: `skills/web-reader`
- **SKILL.md**: [`skills/web-reader/SKILL.md`](skills/web-reader/SKILL.md)
- **Title**: Web Reader Skill
- **License**: MIT
- **Files**: 3
- **Structure**: `scripts/`

> Implement web page content extraction capabilities using the z-ai-web-dev-sdk. Use this skill when the user needs to scrape web pages, extract article content, retrieve page metadata, or build applications that process web content. Supports automatic content extraction with title, HTML, and publication time retrieval.

### `web-search`

- **Path**: `skills/web-search`
- **SKILL.md**: [`skills/web-search/SKILL.md`](skills/web-search/SKILL.md)
- **Title**: Web Search Skill
- **License**: MIT
- **Files**: 3
- **Structure**: `scripts/`

> Implement web search capabilities using the z-ai-web-dev-sdk. Use this skill when the user needs to search for real-time information from the web, retrieve up-to-date content beyond the knowledge cutoff, or find the latest news and data. Returns structured search results with URLs, snippets, and metadata.

---

## 5. Testing, QA & Performance

> Skills for test design, end-to-end testing, performance work, and quality assurance.
> **28 skills** in this category.

### `before-and-after`

- **Path**: `skills/before-and-after`
- **SKILL.md**: [`skills/before-and-after/SKILL.md`](skills/before-and-after/SKILL.md)
- **Title**: Before-After Screenshot Skill
- **Files**: 7
- **Structure**: `scripts/`

> Captures before/after screenshots of web pages or elements for visual comparison. Use when user says "take before and after", "screenshot comparison", "visual diff", "PR screenshots", "compare old and new", or needs to document UI changes. Accepts two URLs (file://, http://, https://) or two image paths.

### `browser-testing-with-devtools`

- **Path**: `skills/browser-testing-with-devtools`
- **SKILL.md**: [`skills/browser-testing-with-devtools/SKILL.md`](skills/browser-testing-with-devtools/SKILL.md)
- **Title**: Browser Testing with DevTools
- **Files**: 1
- **Structure**: flat

> Tests in real browsers. Use when building or debugging anything that runs in a browser. Use when you need to inspect the DOM, capture console errors, analyze network requests, profile performance, or verify visual output with real runtime data via Chrome DevTools MCP.

### `chrome-devtools-mcp`

- **Path**: `skills/chrome-devtools-mcp`
- **SKILL.md**: [`skills/chrome-devtools-mcp/SKILL.md`](skills/chrome-devtools-mcp/SKILL.md)
- **Title**: chrome-devtools-mcp
- **Files**: 1
- **Structure**: flat

> Google-official MCP server providing full Chrome DevTools Protocol access (29 tools). Use for Lighthouse audits, performance traces, network inspection, console log access, JavaScript evaluation, mobile emulation, and memory snapshots.

### `ci-cd-and-automation`

- **Path**: `skills/ci-cd-and-automation`
- **SKILL.md**: [`skills/ci-cd-and-automation/SKILL.md`](skills/ci-cd-and-automation/SKILL.md)
- **Title**: CI/CD and Automation
- **Files**: 1
- **Structure**: flat

> Automates CI/CD pipeline setup. Use when setting up or modifying build and deployment pipelines. Use when you need to automate quality gates, configure test runners in CI, or establish deployment strategies.

### `code-review`

- **Path**: `skills/code-review`
- **SKILL.md**: [`skills/code-review/SKILL.md`](skills/code-review/SKILL.md)
- **Title**: code-review
- **Files**: 2
- **Structure**: flat

> Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes: Standards (does the code follow this repo's documented coding standards?) and Spec (does the code match what the originating issue/spec asked for?). Runs both reviews in parallel sub-agents and reports them side by side. Use when the user wants to review a branch, a PR, work-in-progress changes, or asks to "review since X".

### `code-review-checklist`

- **Path**: `skills/code-review-checklist`
- **SKILL.md**: [`skills/code-review-checklist/SKILL.md`](skills/code-review-checklist/SKILL.md)
- **Title**: Code Review Checklist
- **Version**: 2.0.0
- **Files**: 1
- **Structure**: flat

> Lightweight quick-reference checklist for code review. Tactical 12-category scan used by the Orchestrator's Phase 3. For the comprehensive quality constitution (Six-Axis review), see `code-quality-standards`. For verification gates and the Iron Law, see `verification-and-review-protocol`.

### `coding-agent`

- **Path**: `skills/coding-agent`
- **SKILL.md**: [`skills/coding-agent/SKILL.md`](skills/coding-agent/SKILL.md)
- **Title**: coding-agent
- **Version**: 1.0.4
- **Files**: 8
- **Structure**: flat

> Coding workflow with planning, implementation, verification, and testing for clean software development.

### `content-strategy`

- **Path**: `skills/content-strategy`
- **SKILL.md**: [`skills/content-strategy/SKILL.md`](skills/content-strategy/SKILL.md)
- **Title**: Content Strategy
- **Files**: 2
- **Structure**: flat

> Build and execute a content marketing strategy for a solopreneur business. Use when planning what content to create, deciding on content formats and channels, building a content calendar, measuring content performance, or systematizing content production. Covers audience research for content, content pillars, distribution strategy, repurposing workflows, and metrics. Trigger on "content strategy", "content marketing", "what content should I create", "content plan", "content calendar", "content ideas", "content distribution", "grow through content".

### `context-engineering`

- **Path**: `skills/context-engineering`
- **SKILL.md**: [`skills/context-engineering/SKILL.md`](skills/context-engineering/SKILL.md)
- **Title**: Context Engineering
- **Files**: 1
- **Structure**: flat

> Optimizes agent context setup. Use when starting a new session, when agent output quality degrades, when switching between tasks, or when you need to configure rules files and context for a project.

### `context7-mcp`

- **Path**: `skills/context7-mcp`
- **SKILL.md**: [`skills/context7-mcp/SKILL.md`](skills/context7-mcp/SKILL.md)
- **Title**: Context7 MCP/API Document Lookup
- **Files**: 1
- **Structure**: flat

> Programmatic document lookup via Context7 API and MCP server. Use when: (1) Need structured documentation for any library/package/framework, (2) Want code examples without browser automation, (3) Building with specific tools and need accurate API references, (4) Avoiding hallucinated or outdated docs. Priority: API (fastest) → MCP Server → Browser (fallback) Triggers: "lookup docs for", "get Context7 docs", "find documentation", "API reference for", "code examples for [library]"

### `debugging-and-error-recovery`

- **Path**: `skills/debugging-and-error-recovery`
- **SKILL.md**: [`skills/debugging-and-error-recovery/SKILL.md`](skills/debugging-and-error-recovery/SKILL.md)
- **Title**: Debugging and Error Recovery
- **Files**: 1
- **Structure**: flat

> Guides systematic root-cause debugging. Use when tests fail, builds break, behavior doesn't match expectations, or you encounter any unexpected error. Use when you need a systematic approach to finding and fixing the root cause rather than guessing.

### `diagnosing-bugs`

- **Path**: `skills/diagnosing-bugs`
- **SKILL.md**: [`skills/diagnosing-bugs/SKILL.md`](skills/diagnosing-bugs/SKILL.md)
- **Title**: Diagnosing Bugs
- **Files**: 3
- **Structure**: `scripts/`

> Diagnosis loop for hard bugs and performance regressions. Use when the user says "diagnose"/"debug this", or reports something broken/throwing/failing/slow.

### `e2e-testing-lessons`

- **Path**: `skills/e2e-testing-lessons`
- **SKILL.md**: [`skills/e2e-testing-lessons/SKILL.md`](skills/e2e-testing-lessons/SKILL.md)
- **Title**: E2E Testing Lessons Learned
- **Files**: 1
- **Structure**: flat

> Condensed experience from 15-phase E2E testing initiative covering authentication, API contracts, tool selection, and hybrid testing methodology. Use when planning E2E tests, selecting testing tools, or debugging test failures.

### `evidence-driven-testing`

- **Path**: `skills/evidence-driven-testing`
- **SKILL.md**: [`skills/evidence-driven-testing/SKILL.md`](skills/evidence-driven-testing/SKILL.md)
- **Title**: Evidence-Driven Testing
- **Version**: 1.2
- **Files**: 2
- **Structure**: `scripts/`

> Records visual proof while testing UI behavior — the agent tests the app hands-on via computer use while a screen recording with structured test/assertion annotations captures the session — then posts the video and a results summary to the PR and tracker issue. Use whenever a change needs verifiable evidence that it works, instead of prose claims — including headless environments (scripted screenshots and probes) and non-UI changes (measured numbers, output pairs).

### `interview-designer`

- **Path**: `skills/interview-designer`
- **SKILL.md**: [`skills/interview-designer/SKILL.md`](skills/interview-designer/SKILL.md)
- **Title**: Interview Designer Skill
- **Files**: 5
- **Structure**: `references/`

> Analyze resumes and design interview strategies using evidence-based methodology. Transforms interview prep from "read resume → ask questions" into "define standard → forensic evidence → future simulation". Combines Geoff Smart's Topgrading, Lou Adler's performance-based hiring, and Daniel Kahneman's bias control. Use when preparing for interviews, creating structured interview guides, or designing questions to validate candidate competencies.

### `lint-and-validate`

- **Path**: `skills/lint-and-validate`
- **SKILL.md**: [`skills/lint-and-validate/SKILL.md`](skills/lint-and-validate/SKILL.md)
- **Title**: Lint and Validate Skill
- **Files**: 3
- **Structure**: `scripts/`

> Automatic quality control, linting, and static analysis procedures. Use after every code modification to ensure syntax correctness and project standards. Triggers on keywords: lint, format, check, validate, types, static analysis.

### `pdf`

- **Path**: `skills/pdf`
- **SKILL.md**: [`skills/pdf/SKILL.md`](skills/pdf/SKILL.md)
- **Title**: PDF - Document Production Workbench
- **Author**: Z.AI
- **Version**: 1.0
- **License**: Proprietary. LICENSE.txt has complete terms
- **Files**: 41
- **Structure**: `scripts/`, `references/`

> Professional PDF toolkit with four production lines:(1) Report - structured documents via ReportLab (reports, proposals, contracts, white papers); (2) Creative - visual design via JSON Blueprint → design_engine.py → Playwright snapshot (posters, infographics, invitations, dashboards). The LLM acts as Art Director outputting ONLY JSON spatial blueprints; convert.blueprint compiles to pixel-perfect PDF. (3) Academic - scholarly work via LaTeX/Tectonic (papers, theses, math-heavy documents); (4) Process - manipulate existing PDFs (extract, merge, split, fill forms, convert);Auto-routes based o...

### `performance-optimization`

- **Path**: `skills/performance-optimization`
- **SKILL.md**: [`skills/performance-optimization/SKILL.md`](skills/performance-optimization/SKILL.md)
- **Title**: Performance Optimization
- **Files**: 1
- **Structure**: flat

> Optimizes application performance. Use when performance requirements exist, when you suspect performance regressions, or when Core Web Vitals or load times need improvement. Use when profiling reveals bottlenecks that need fixing.

### `playwright-cli`

- **Path**: `skills/playwright-cli`
- **SKILL.md**: [`skills/playwright-cli/SKILL.md`](skills/playwright-cli/SKILL.md)
- **Title**: Browser Automation with playwright-cli
- **Files**: 11
- **Structure**: `references/`

> Automate browser interactions, test web pages and work with Playwright tests. Is a better choice for traditional browser testing - multi-browser support (Firefox, WebKit), Playwright-native locators, and the run-code command for custom Playwright snippets.

### `readme-md`

- **Path**: `skills/readme-md`
- **SKILL.md**: [`skills/readme-md/SKILL.md`](skills/readme-md/SKILL.md)
- **Title**: readme-md
- **Version**: 1.0.0
- **Files**: 1
- **Structure**: flat

> Creates a professional, high-signal README.md for a repository by investigating the codebase and following battle-tested conventions distilled from production open-source projects.

### `seo-content-writer`

- **Path**: `skills/seo-content-writer`
- **SKILL.md**: [`skills/seo-content-writer/SKILL.md`](skills/seo-content-writer/SKILL.md)
- **Title**: SEO Content Writer
- **License**: Apache-2.0
- **Author**: aaron-he-zhu
- **Version**: 2.0.0
- **Files**: 4
- **Structure**: `references/`

> Use when the user asks to "write SEO content", "create a blog post", "write an article", "content writing", "draft optimized content", "write me an article", "create a blog post about", "help me write SEO content", or "draft content for". Creates high-quality, SEO-optimized content that ranks in search engines. Applies on-page SEO best practices, keyword optimization, and content structure for maximum visibility and engagement. For AI citation optimization, see geo-content-optimizer. For updating existing content, see content-refresher.

### `skill-creator`

- **Path**: `skills/skill-creator`
- **SKILL.md**: [`skills/skill-creator/SKILL.md`](skills/skill-creator/SKILL.md)
- **Title**: Skill Creator
- **License**: Complete terms in LICENSE.txt
- **Files**: 21
- **Structure**: `scripts/`, `references/`

> Create new skills, modify and improve existing skills, and evaluate skill quality. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, optimize a skill's description for better triggering accuracy, or package a skill for distribution.

### `skill-creator-zai`

- **Path**: `skills/skill-creator-zai`
- **SKILL.md**: [`skills/skill-creator-zai/SKILL.md`](skills/skill-creator-zai/SKILL.md)
- **Title**: Skill Creator
- **Files**: 18
- **Structure**: `scripts/`, `references/`

> Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, or optimize a skill's description for better triggering accuracy.

### `tdd`

- **Path**: `skills/tdd`
- **SKILL.md**: [`skills/tdd/SKILL.md`](skills/tdd/SKILL.md)
- **Title**: Test-Driven Development
- **Files**: 4
- **Structure**: flat

> Test-driven development. Use when the user wants to build features or fix bugs test-first, mentions "red-green-refactor", or wants integration tests.

### `tdd-workflow`

- **Path**: `skills/tdd-workflow`
- **SKILL.md**: [`skills/tdd-workflow/SKILL.md`](skills/tdd-workflow/SKILL.md)
- **Title**: TDD Workflow
- **Files**: 1
- **Structure**: flat

> Test-Driven Development workflow principles. RED-GREEN-REFACTOR cycle.

### `test-driven-development`

- **Path**: `skills/test-driven-development`
- **SKILL.md**: [`skills/test-driven-development/SKILL.md`](skills/test-driven-development/SKILL.md)
- **Title**: Test-Driven Development
- **Files**: 1
- **Structure**: flat

> Drives development with tests. Use when implementing any logic, fixing any bug, or changing any behavior. Use when you need to prove that code works, when a bug report arrives, or when you're about to modify existing functionality.

### `testing-patterns`

- **Path**: `skills/testing-patterns`
- **SKILL.md**: [`skills/testing-patterns/SKILL.md`](skills/testing-patterns/SKILL.md)
- **Title**: Testing Patterns
- **Files**: 2
- **Structure**: `scripts/`

> Testing patterns and principles. Unit, integration, mocking strategies.

### `webapp-testing`

- **Path**: `skills/webapp-testing`
- **SKILL.md**: [`skills/webapp-testing/SKILL.md`](skills/webapp-testing/SKILL.md)
- **Title**: Web App Testing
- **Files**: 7
- **Structure**: `scripts/`

> Web application testing principles. E2E, Playwright, deep audit strategies.

---

## 6. Code Quality, Security & Architecture

> Skills for code review, security hardening, architecture decisions, and refactoring.
> **23 skills** in this category.

### `anti-pua`

- **Path**: `skills/anti-pua`
- **SKILL.md**: [`skills/anti-pua/SKILL.md`](skills/anti-pua/SKILL.md)
- **Title**: 反PUA大师 - 情感操纵识别与心理分析
- **Files**: 1
- **Structure**: flat

> 识别和分析PUA（Pickup Artist）及情感操纵行为的专业心理分析工具。具备人格分析、心理侧写、情感分析能力，能够识别情感操纵、煤气灯操纵、虐待等有毒关系模式，评估人格特质（如黑暗三人格、脆弱型自恋等），预测对方行为并给出具体的相处建议。当用户需要：分析对方言行动机、识别PUA/情感操纵行为、评估NPD（自恋型人格障碍）倾向、识别操纵行为、预测对方未来行为、寻求健康关系建议、分析黑暗三人格或光明三人格时使用此skill。

### `clean-code`

- **Path**: `skills/clean-code`
- **SKILL.md**: [`skills/clean-code/SKILL.md`](skills/clean-code/SKILL.md)
- **Title**: Clean Code - Pragmatic AI Coding Standards
- **Version**: 2.0
- **Files**: 1
- **Structure**: flat

> Pragmatic coding standards - concise, direct, no over-engineering, no unnecessary comments

### `code-review-and-audit`

- **Path**: `skills/code-review-and-audit`
- **SKILL.md**: [`skills/code-review-and-audit/SKILL.md`](skills/code-review-and-audit/SKILL.md)
- **Title**: Code Review & Audit Orchestration Skill
- **Version**: 2.0.0
- **Files**: 6
- **Structure**: `scripts/`, `references/`

> Unified code review and security audit orchestration skill. Coordinates static analysis, security scanning, code quality checks, test coverage, performance profiling, and expert review into a single tiered pipeline. Use when reviewing code, preparing for release, conducting security audits, or running pre-merge gates. Triggers on: review, audit, code review, security scan, quality gate, pre-merge, checklist, lint, vulnerability.

### `code-simplification`

- **Path**: `skills/code-simplification`
- **SKILL.md**: [`skills/code-simplification/SKILL.md`](skills/code-simplification/SKILL.md)
- **Title**: Code Simplification
- **Files**: 1
- **Structure**: flat

> Simplifies code for clarity. Use when refactoring code for clarity without changing behavior. Use when code works but is harder to read, maintain, or extend than it should be. Use when reviewing code that has accumulated unnecessary complexity.

### `code-structure`

- **Path**: `skills/code-structure`
- **SKILL.md**: [`skills/code-structure/SKILL.md`](skills/code-structure/SKILL.md)
- **Title**: Service Layer Architecture
- **Files**: 1
- **Structure**: flat

> Use when multiple workflows duplicate the same operational logic, when deciding what belongs in actions vs shared services, or when refactoring repeated operational blocks across domain flows. Use when adding new features that share mechanics with existing ones.

### `codebase-design`

- **Path**: `skills/codebase-design`
- **SKILL.md**: [`skills/codebase-design/SKILL.md`](skills/codebase-design/SKILL.md)
- **Title**: Codebase Design
- **Files**: 4
- **Structure**: flat

> Shared vocabulary for designing deep modules. Use when the user wants to design or improve a module's interface, find deepening opportunities, decide where a seam goes, make code more testable or AI-navigable, or when another skill needs the deep-module vocabulary.

### `context-anchor`

- **Path**: `skills/context-anchor`
- **SKILL.md**: [`skills/context-anchor/SKILL.md`](skills/context-anchor/SKILL.md)
- **Title**: Context Anchor Skill
- **Version**: 1.1.0
- **Files**: 6
- **Structure**: `scripts/`

> Recover from context compaction by scanning memory files and surfacing where you left off. Use when waking up fresh, after compaction, or when you feel lost about what you were doing. Now supports both flat (YYYY-MM-DD.md) and QMD hierarchical (daily/YYYY/MM/DD.md) memory structures.

### `deprecation-and-migration`

- **Path**: `skills/deprecation-and-migration`
- **SKILL.md**: [`skills/deprecation-and-migration/SKILL.md`](skills/deprecation-and-migration/SKILL.md)
- **Title**: Deprecation and Migration
- **Files**: 1
- **Structure**: flat

> Manages deprecation and migration. Use when removing old systems, APIs, or features. Use when migrating users from one implementation to another. Use when deciding whether to maintain or sunset existing code.

### `distill-codebase-skill`

- **Path**: `skills/distill-codebase-skill`
- **SKILL.md**: [`skills/distill-codebase-skill/SKILL.md`](skills/distill-codebase-skill/SKILL.md)
- **Title**: This is just a reference template for distilling the knowledge and expertise and experiences after completing updating a project codebase
- **Files**: 1
- **Structure**: flat

> Reference template for distilling codebase knowledge into a comprehensive engineering skill document. Use after completing a major project update, security remediation, or architectural overhaul to create a reusable SKILL.md that captures lessons learned, anti-patterns, debugging guides, and best practices for future agents.

### `encrypt-decrypt`

- **Path**: `skills/encrypt-decrypt`
- **SKILL.md**: [`skills/encrypt-decrypt/SKILL.md`](skills/encrypt-decrypt/SKILL.md)
- **Title**: Output: report.pdf.enc (original unchanged)
- **Version**: 1.2
- **Files**: 8
- **Structure**: `scripts/`, `references/`

> Encrypt and decrypt files and folders from the CLI. Single-file Python script using AES-256-GCM with Scrypt key derivation. Supports recursive folder processing, atomic writes, authenticated streaming for large files, and non-destructive defaults.

### `git-guardrails-claude-code`

- **Path**: `skills/git-guardrails-claude-code`
- **SKILL.md**: [`skills/git-guardrails-claude-code/SKILL.md`](skills/git-guardrails-claude-code/SKILL.md)
- **Title**: Setup Git Guardrails
- **Files**: 3
- **Structure**: `scripts/`

> Set up Claude Code hooks to block dangerous git commands (push, reset --hard, clean, branch -D, etc.) before they execute. Use when user wants to prevent destructive git operations, add git safety hooks, or block git push/reset in Claude Code.

### `greploop`

- **Path**: `skills/greploop`
- **SKILL.md**: [`skills/greploop/SKILL.md`](skills/greploop/SKILL.md)
- **Title**: Greploop
- **License**: MIT
- **Author**: greptileai
- **Version**: 1.3
- **Files**: 4
- **Structure**: `references/`

> Iteratively improves a PR (GitHub), MR (GitLab), or shelved changelist (Perforce) until Greptile gives it a 5/5 confidence score with zero unresolved comments. Triggers Greptile review, fixes all actionable comments, pushes/re-shelves, re-triggers review, and repeats. Use when the user wants to fully optimize a PR/MR/CL against Greptile's code review standards.

### `greploop-apps`

- **Path**: `skills/greploop-apps`
- **SKILL.md**: [`skills/greploop-apps/SKILL.md`](skills/greploop-apps/SKILL.md)
- **Title**: Greploop Apps
- **License**: MIT
- **Author**: greptileai
- **Version**: 1.3
- **Files**: 4
- **Structure**: `references/`

> Iteratively improves a PR (GitHub), MR (GitLab), or shelved changelist (Perforce) until Greptile gives it a 5/5 confidence score with zero unresolved comments. Identical to greploop, but triggers reviews by tagging @greptile-apps, which bypasses Greptile's file-count limit on huge PRs that the plain @greptile mention refuses to review. Use when the user wants to fully optimize a large PR/MR/CL against Greptile's code review standards.

### `improve-codebase-architecture`

- **Path**: `skills/improve-codebase-architecture`
- **SKILL.md**: [`skills/improve-codebase-architecture/SKILL.md`](skills/improve-codebase-architecture/SKILL.md)
- **Title**: Improve Codebase Architecture
- **Files**: 3
- **Structure**: flat

> Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick.

### `incremental-implementation`

- **Path**: `skills/incremental-implementation`
- **SKILL.md**: [`skills/incremental-implementation/SKILL.md`](skills/incremental-implementation/SKILL.md)
- **Title**: Incremental Implementation
- **Files**: 1
- **Structure**: flat

> Delivers changes incrementally. Use when implementing any feature or change that touches more than one file. Use when you're about to write a large amount of code at once, or when a task feels too big to land in one step.

### `memory-architect`

- **Path**: `skills/memory-architect`
- **SKILL.md**: [`skills/memory-architect/SKILL.md`](skills/memory-architect/SKILL.md)
- **Title**: Memory Architect
- **Files**: 8
- **Structure**: `scripts/`, `references/`

> Bootstrap, audit, and recover the OpenClaw 3-layer memory architecture (workspace files, LCM database, QMD semantic index). Use when: (1) Setting up memory on a new OpenClaw instance, (2) Auditing existing memory health, (3) Recovering from corruption or system crash, (4) Migrating or restructuring memory layout, (5) User asks about memory architecture setup or health. Triggers on phrases like 'bootstrap memory', 'audit memory', 'memory architecture', 'memory setup', 'LCM configuration', 'QMD setup', 'memory recovery', 'check memory health'.

### `memory-architecture`

- **Path**: `skills/memory-architecture`
- **SKILL.md**: [`skills/memory-architecture/SKILL.md`](skills/memory-architecture/SKILL.md)
- **Title**: OpenClaw Memory Architecture
- **Version**: 1.0.0
- **Author**: trusty-pal
- **Files**: 2
- **Structure**: flat

> OpenClaw memory system architecture, setup guide, and troubleshooting reference. Use when configuring memory on a new machine, diagnosing memory issues after updates, or understanding how workspace files, LCM, and QMD work together.

### `migrate-to-shoehorn`

- **Path**: `skills/migrate-to-shoehorn`
- **SKILL.md**: [`skills/migrate-to-shoehorn/SKILL.md`](skills/migrate-to-shoehorn/SKILL.md)
- **Title**: Migrate to Shoehorn
- **Files**: 2
- **Structure**: flat

> Migrate test files from `as` type assertions to @total-typescript/shoehorn. Use when user mentions shoehorn, wants to replace `as` in tests, or needs partial test data.

### `plan-writing`

- **Path**: `skills/plan-writing`
- **SKILL.md**: [`skills/plan-writing/SKILL.md`](skills/plan-writing/SKILL.md)
- **Title**: Plan Writing
- **Files**: 1
- **Structure**: flat

> Structured task planning with clear breakdowns, dependencies, and verification criteria. Use when implementing features, refactoring, or any multi-step work.

### `scaffold-exercises`

- **Path**: `skills/scaffold-exercises`
- **SKILL.md**: [`skills/scaffold-exercises/SKILL.md`](skills/scaffold-exercises/SKILL.md)
- **Title**: Scaffold Exercises
- **Files**: 2
- **Structure**: flat

> Create exercise directory structures with sections, problems, solutions, and explainers that pass linting. Use when user wants to scaffold exercises, create exercise stubs, or set up a new course section.

### `setup-pre-commit`

- **Path**: `skills/setup-pre-commit`
- **SKILL.md**: [`skills/setup-pre-commit/SKILL.md`](skills/setup-pre-commit/SKILL.md)
- **Title**: Setup Pre-Commit Hooks
- **Files**: 2
- **Structure**: flat

> Set up Husky pre-commit hooks with lint-staged (Prettier), type checking, and tests in the current repo. Use when user wants to add pre-commit hooks, set up Husky, configure lint-staged, or add commit-time formatting/typechecking/testing.

### `setup-ts-deep-modules`

- **Path**: `skills/setup-ts-deep-modules`
- **SKILL.md**: [`skills/setup-ts-deep-modules/SKILL.md`](skills/setup-ts-deep-modules/SKILL.md)
- **Title**: Setup TS Deep Modules
- **Files**: 3
- **Structure**: flat

> Wire dependency-cruiser into a TypeScript repo so each package is a deep module, with implementation hidden in subfolders and reachable only through its entry-point files. User-invoked.

### `vulnerability-scanner`

- **Path**: `skills/vulnerability-scanner`
- **SKILL.md**: [`skills/vulnerability-scanner/SKILL.md`](skills/vulnerability-scanner/SKILL.md)
- **Title**: Vulnerability Scanner
- **Files**: 3
- **Structure**: `scripts/`

> Advanced vulnerability analysis principles. OWASP 2025, Supply Chain Security, attack surface mapping, risk prioritization.

---

## 7. Planning, Workflow & Project Management

> Skills for planning work, managing projects, orchestrating sub-agents, and shipping.
> **32 skills** in this category.

### `ask-matt`

- **Path**: `skills/ask-matt`
- **SKILL.md**: [`skills/ask-matt/SKILL.md`](skills/ask-matt/SKILL.md)
- **Title**: Ask Matt
- **Files**: 3
- **Structure**: flat

> Ask which skill or flow fits your situation. A router over the skills in this repo.

### `background-terminals`

- **Path**: `skills/background-terminals`
- **SKILL.md**: [`skills/background-terminals/SKILL.md`](skills/background-terminals/SKILL.md)
- **Title**: Background Terminals
- **Files**: 1
- **Structure**: flat

> Run and manage long-lived shell commands in background terminals. Use for dev servers, watchers, streaming builds, and other commands that should keep running while the agent continues working.

### `blog-writer`

- **Path**: `skills/blog-writer`
- **SKILL.md**: [`skills/blog-writer/SKILL.md`](skills/blog-writer/SKILL.md)
- **Title**: Blog Writer
- **Files**: 12
- **Structure**: flat

> This skill should be used when writing blog posts, articles, or long-form content in the writer's distinctive writing style. It produces authentic, opinionated content that matches the writer's voice—direct, conversational, and grounded in personal experience. The skill handles the complete workflow from research review through Notion publication. Use this skill for drafting blog posts, thought leadership pieces, or any writing meant to reflect the writer's perspective on AI, productivity, sales, marketing, or technology topics.

### `documentation-and-adrs`

- **Path**: `skills/documentation-and-adrs`
- **SKILL.md**: [`skills/documentation-and-adrs/SKILL.md`](skills/documentation-and-adrs/SKILL.md)
- **Title**: Documentation and ADRs
- **Files**: 1
- **Structure**: flat

> Records decisions and documentation. Use when making architectural decisions, changing public APIs, shipping features, or when you need to record context that future engineers and agents will need to understand the codebase.

### `git-workflow-and-versioning`

- **Path**: `skills/git-workflow-and-versioning`
- **SKILL.md**: [`skills/git-workflow-and-versioning/SKILL.md`](skills/git-workflow-and-versioning/SKILL.md)
- **Title**: Git Workflow and Versioning
- **Files**: 1
- **Structure**: flat

> Structures git workflow practices. Use when making any code change. Use when committing, branching, resolving conflicts, or when you need to organize work across multiple parallel streams.

### `grill-me`

- **Path**: `skills/grill-me`
- **SKILL.md**: [`skills/grill-me/SKILL.md`](skills/grill-me/SKILL.md)
- **Title**: grill-me
- **Files**: 2
- **Structure**: flat

> A relentless interview to sharpen a plan or design.

### `grill-with-docs`

- **Path**: `skills/grill-with-docs`
- **SKILL.md**: [`skills/grill-with-docs/SKILL.md`](skills/grill-with-docs/SKILL.md)
- **Title**: grill-with-docs
- **Files**: 2
- **Structure**: flat

> A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go.

### `grilling`

- **Path**: `skills/grilling`
- **SKILL.md**: [`skills/grilling/SKILL.md`](skills/grilling/SKILL.md)
- **Title**: grilling
- **Files**: 2
- **Structure**: flat

> Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.

### `implement`

- **Path**: `skills/implement`
- **SKILL.md**: [`skills/implement/SKILL.md`](skills/implement/SKILL.md)
- **Title**: implement
- **Files**: 2
- **Structure**: flat

> Implement a piece of work based on a spec or set of tickets.

### `interview-prep`

- **Path**: `skills/interview-prep`
- **SKILL.md**: [`skills/interview-prep/SKILL.md`](skills/interview-prep/SKILL.md)
- **Title**: Interview Prep（面试准备）
- **Files**: 11
- **Structure**: `scripts/`, `references/`

> 帮用户准备面试。基于目标 JD、公司、岗位方向，生成"高频面试题 + 参考回答 + 行为面 / 技术面 / Case 面分类题库"，并产出可打印的『面试备战手册』。当用户说"帮我准备面试""明天有面试 / 后天面试""面试题""面经""模拟面试""我要面 X 公司 Y 岗位""帮我准备 STAR 故事""怎么回答这道面试题""自我介绍 / 离职原因 / 优缺点 怎么答"，必须触发本 skill。请勿用本 skill 改简历（去 jd-resume-tailor / resume-builder）或推荐方向（去 job-intent-tracker）。

### `job-intent-tracker`

- **Path**: `skills/job-intent-tracker`
- **SKILL.md**: [`skills/job-intent-tracker/SKILL.md`](skills/job-intent-tracker/SKILL.md)
- **Title**: Job Intent Tracker（求职意向 + 岗位追踪）
- **Files**: 8
- **Structure**: `scripts/`, `references/`

> 帮助用户梳理求职意向、生成目标岗位画像，并维护一份结构化的"岗位投递追踪表"。当用户说"我想换工作 / 不知道投什么岗 / 帮我看看我适合什么岗位 / 帮我管理投递进度 / 我投了好几家但记不住状态了 / 想做一个求职 OKR / 整理一下求职方向"，或上传简历但没说要改简历时，应该主动触发本 skill。本 skill 也适用于实习生、应届生、转行候选人在求职启动阶段做"自我盘点 + 目标画像 + 投递管理"三件事。

### `loop-builder`

- **Path**: `skills/loop-builder`
- **SKILL.md**: [`skills/loop-builder/SKILL.md`](skills/loop-builder/SKILL.md)
- **Title**: Loop Builder
- **Files**: 75
- **Structure**: `scripts/`, `references/`

> Design and scaffold an agent "loop" — an unattended, scheduled, self-verifying agent workflow. Use this whenever the user wants to automate a recurring task, schedule an agent, run an agent unattended or overnight, set up monitoring, triage, or alerting, poll something on a cadence, or turn a manual repeated workflow into a self-running one — even if they never say the word "loop." If a request implies "do this every day / on a schedule / until some condition holds, without me typing each time," reach for this skill. It walks the seven-question blueprint, picks the simplest loop pattern, an...

### `marketing-mode`

- **Path**: `skills/marketing-mode`
- **SKILL.md**: [`skills/marketing-mode/SKILL.md`](skills/marketing-mode/SKILL.md)
- **Title**: Marketing Mode - Complete Marketing Knowledge Base
- **Version**: 1.0.0
- **Files**: 5
- **Structure**: flat

> Marketing Mode combines 23 comprehensive marketing skills covering strategy, psychology, content, SEO, conversion optimization, and paid growth. Use when users need marketing strategy, copywriting, SEO help, conversion optimization, paid advertising, or any marketing tactic.

### `mindfulness-meditation`

- **Path**: `skills/mindfulness-meditation`
- **SKILL.md**: [`skills/mindfulness-meditation/SKILL.md`](skills/mindfulness-meditation/SKILL.md)
- **Title**: Mindfulness & Meditation
- **Author**: clawd-team
- **Version**: 1.0.0
- **Files**: 2
- **Structure**: flat

> Build a meditation practice with guided sessions, streaks, and mindfulness reminders

### `new-feature`

- **Path**: `skills/new-feature`
- **SKILL.md**: [`skills/new-feature/SKILL.md`](skills/new-feature/SKILL.md)
- **Title**: New Feature
- **Files**: 1
- **Structure**: flat

> Start a new task in an isolated Git worktree branched from origin/main so multiple agents can work on the same repo in parallel without conflicts. Use at the beginning of every new feature, fix, or task — before writing any code.

### `orchestrator-toolkit`

- **Path**: `skills/orchestrator-toolkit`
- **SKILL.md**: [`skills/orchestrator-toolkit/SKILL.md`](skills/orchestrator-toolkit/SKILL.md)
- **Title**: Orchestrator Toolkit Skill
- **Files**: 1
- **Structure**: flat

> Pure-Python orchestration toolkit for task management, complexity analysis, decomposition, persistence, and recovery. Use when breaking down complex projects, tracking progress, or building lightweight orchestration systems.

### `pandoc-docx-template`

- **Path**: `skills/pandoc-docx-template`
- **SKILL.md**: [`skills/pandoc-docx-template/SKILL.md`](skills/pandoc-docx-template/SKILL.md)
- **Title**: Pandoc DOCX Template
- **Files**: 19
- **Structure**: `scripts/`

> Use this skill when converting Markdown to Word DOCX or DOCX back to Markdown with Pandoc, especially when the output should use the bundled Chinese Word reference templates, heading numbering variants, list indentation variants, SCI paper templates, and Lua filters for HTML tags, image captions, font color, and inline code styles.

### `pi-agent-customize-system-prompt`

- **Path**: `skills/pi-agent-customize-system-prompt`
- **SKILL.md**: [`skills/pi-agent-customize-system-prompt/SKILL.md`](skills/pi-agent-customize-system-prompt/SKILL.md)
- **Title**: Customizing the Pi Coding Agent System Prompt
- **Version**: 1.0.0
- **Files**: 1
- **Structure**: flat

> guide for customizing the Pi Agent system prompt to add custom tools and workflow instructions

### `planning-and-task-breakdown`

- **Path**: `skills/planning-and-task-breakdown`
- **SKILL.md**: [`skills/planning-and-task-breakdown/SKILL.md`](skills/planning-and-task-breakdown/SKILL.md)
- **Title**: Planning and Task Breakdown
- **Files**: 1
- **Structure**: flat

> Breaks work into ordered tasks. Use when you have a spec or clear requirements and need to break work into implementable tasks. Use when a task feels too large to start, when you need to estimate scope, or when parallel work is possible.

### `pptx-generator`

- **Path**: `skills/pptx-generator`
- **SKILL.md**: [`skills/pptx-generator/SKILL.md`](skills/pptx-generator/SKILL.md)
- **Title**: PPTX Generator & Editor
- **License**: MIT
- **Version**: 1.0
- **Files**: 6
- **Structure**: `references/`

> Generate, edit, and read PowerPoint presentations. Create from scratch with PptxGenJS (cover, TOC, content, section divider, summary slides), edit existing PPTX via XML workflows, or extract text with markitdown. Triggers: PPT, PPTX, PowerPoint, presentation, slide, deck, slides.

### `shipping-and-launch`

- **Path**: `skills/shipping-and-launch`
- **SKILL.md**: [`skills/shipping-and-launch/SKILL.md`](skills/shipping-and-launch/SKILL.md)
- **Title**: Shipping and Launch
- **Files**: 1
- **Structure**: flat

> Prepares production launches. Use when preparing to deploy to production. Use when you need a pre-launch checklist, when setting up monitoring, when planning a staged rollout, or when you need a rollback strategy.

### `spec-driven-development`

- **Path**: `skills/spec-driven-development`
- **SKILL.md**: [`skills/spec-driven-development/SKILL.md`](skills/spec-driven-development/SKILL.md)
- **Title**: Spec-Driven Development
- **Files**: 1
- **Structure**: flat

> Creates specs before coding. Use when starting a new project, feature, or significant change and no specification exists yet. Use when requirements are unclear, ambiguous, or only exist as a vague idea.

### `storyboard-manager`

- **Path**: `skills/storyboard-manager`
- **SKILL.md**: [`skills/storyboard-manager/SKILL.md`](skills/storyboard-manager/SKILL.md)
- **Title**: Storyboard Manager
- **Files**: 7
- **Structure**: `scripts/`, `references/`

> Assist writers with story planning, character development, plot structuring, chapter writing, timeline tracking, and consistency checking. Use this skill when working with creative writing projects organized in folders containing characters, chapters, story planning documents, and summaries. Trigger this skill for tasks like "Help me develop this character," "Write the next chapter," "Check consistency across my story," or "Track the timeline of events."

### `subagents`

- **Path**: `skills/subagents`
- **SKILL.md**: [`skills/subagents/SKILL.md`](skills/subagents/SKILL.md)
- **Title**: Subagents
- **Files**: 1
- **Structure**: flat

> invoke this skill when the user asks you to use subagents

### `to-questionnaire`

- **Path**: `skills/to-questionnaire`
- **SKILL.md**: [`skills/to-questionnaire/SKILL.md`](skills/to-questionnaire/SKILL.md)
- **Title**: <Questionnaire title>
- **Files**: 2
- **Structure**: flat

> Turn a decision you can't fully answer into a questionnaire for someone else to fill in.

### `to-spec`

- **Path**: `skills/to-spec`
- **SKILL.md**: [`skills/to-spec/SKILL.md`](skills/to-spec/SKILL.md)
- **Title**: to-spec
- **Files**: 2
- **Structure**: flat

> Turn the current conversation into a spec and publish it to the project issue tracker: no interview, just synthesis of what you've already discussed.

### `to-tickets`

- **Path**: `skills/to-tickets`
- **SKILL.md**: [`skills/to-tickets/SKILL.md`](skills/to-tickets/SKILL.md)
- **Title**: To Tickets
- **Files**: 2
- **Structure**: flat

> Break a plan, spec, or the current conversation into a set of tracer-bullet tickets, each declaring its blocking edges, published to the configured tracker (edges as text in one file per ticket locally, or native blocking links on a real tracker).

### `triage`

- **Path**: `skills/triage`
- **SKILL.md**: [`skills/triage/SKILL.md`](skills/triage/SKILL.md)
- **Title**: Triage
- **Files**: 4
- **Structure**: flat

> Move issues and external PRs through a state machine of triage roles, categorise, verify, grill if needed, and write agent-ready briefs.

### `verification-and-review-protocol`

- **Path**: `skills/verification-and-review-protocol`
- **SKILL.md**: [`skills/verification-and-review-protocol/SKILL.md`](skills/verification-and-review-protocol/SKILL.md)
- **Title**: Verification & Review Protocol
- **Version**: 2.0.0
- **Files**: 4
- **Structure**: `references/`

> Governs the protocol for receiving feedback, requesting subagent reviews, and enforcing verification gates. Contains the 'Iron Law' preventing false completion claims. Use when receiving PR feedback, finishing tasks, or before claiming work is 'done'.

### `wait-what`

- **Path**: `skills/wait-what`
- **SKILL.md**: [`skills/wait-what/SKILL.md`](skills/wait-what/SKILL.md)
- **Title**: wait-what
- **Files**: 2
- **Structure**: flat

> Stop. That last message did not land: re-pitch it.

### `wayfinder`

- **Path**: `skills/wayfinder`
- **SKILL.md**: [`skills/wayfinder/SKILL.md`](skills/wayfinder/SKILL.md)
- **Title**: wayfinder
- **Files**: 2
- **Structure**: flat

> Plan a huge chunk of work (more than one agent session can hold) as a shared map of decision tickets on your issue tracker, and resolve them one at a time until the way to the destination is clear.

### `writing-plans`

- **Path**: `skills/writing-plans`
- **SKILL.md**: [`skills/writing-plans/SKILL.md`](skills/writing-plans/SKILL.md)
- **Title**: Writing Plans
- **Files**: 2
- **Structure**: flat

> Use when you have a spec or requirements for a multi-step task, before touching code

---

## 8. Documentation & Content Creation

> Skills that produce documents, presentations, spreadsheets, PDFs, or written content.
> **24 skills** in this category.

### `agents-md`

- **Path**: `skills/agents-md`
- **SKILL.md**: [`skills/agents-md/SKILL.md`](skills/agents-md/SKILL.md)
- **Title**: agents-md
- **Version**: 1.1.0
- **Files**: 1
- **Structure**: flat

> Creates or updates a compact, high-signal AGENTS.md instruction file for a repository, helping future AI coding agents avoid mistakes and onboard faster.

### `cheat-sheet`

- **Path**: `skills/cheat-sheet`
- **SKILL.md**: [`skills/cheat-sheet/SKILL.md`](skills/cheat-sheet/SKILL.md)
- **Title**: Cheatsheet 生成器
- **Files**: 1
- **Structure**: flat

> 将 PDF/Word/Markdown 学习资料转化为精炼的知识浓缩卡文档。支持三种风格（知识点速查卡/思维导图式/Q&A式），输出双栏小字 PDF。当用户说"生成知识浓缩卡"、"生成 Cheatsheet"、"帮我做个速查表"、"把这个资料整理成一页纸"、"做个知识卡片"时触发。**不处理**：基于材料出题（→ quiz-mastery）、长期学习项目（→ study-buddy）。

### `claude-md`

- **Path**: `skills/claude-md`
- **SKILL.md**: [`skills/claude-md/SKILL.md`](skills/claude-md/SKILL.md)
- **Title**: Claude MD Generator
- **Version**: 1.1.0
- **Files**: 1
- **Structure**: flat

> Generate proper CLAUDE.md files for any codebase. Analyzes codebase structure, detects frameworks and languages, and produces a comprehensive CLAUDE.md following the Meticulous Approach framework.

### `codex-ppt`

- **Path**: `skills/codex-ppt`
- **SKILL.md**: [`skills/codex-ppt/SKILL.md`](skills/codex-ppt/SKILL.md)
- **Title**: Codex PPT
- **Files**: 40
- **Structure**: `scripts/`, `references/`

> Generate visually unified image-based PPT/PPTX decks from articles, reports, papers, notes, or outlines.

### `content-analysis`

- **Path**: `skills/content-analysis`
- **SKILL.md**: [`skills/content-analysis/SKILL.md`](skills/content-analysis/SKILL.md)
- **Title**: ContentAnalysis
- **Files**: 3
- **Structure**: flat

> Content extraction and analysis — wisdom extraction from videos, podcasts, articles, and YouTube. USE WHEN extract wisdom, content analysis, analyze content, insight report, analyze video, analyze podcast, extract insights, key takeaways, what did I miss, extract from YouTube.

**Sub-skills / templates (1):**

| Name | Path | Description |
|------|------|-------------|
| `ExtractWisdom` | `skills/content-analysis/ExtractWisdom` | Content-adaptive wisdom extraction — detects what domains exist in content and builds custom sections (not static IDEAS/QUOTES). Produces tailored insight reports from videos, podcasts, articles. USE WHEN extract wisdom, analyze video, analyze podcast, extract insights, what's interesting, extract from YouTube, what did I miss, key takeaways. |

### `cyber-ppt`

- **Path**: `skills/cyber-ppt`
- **SKILL.md**: [`skills/cyber-ppt/SKILL.md`](skills/cyber-ppt/SKILL.md)
- **Title**: CyberPPT
- **Files**: 11673
- **Structure**: `scripts/`, `references/`

> 当用户需要把 DOCX、PDF、TXT、XLSX、研究报告、业务材料或原始数据转成高密度、可编辑、咨询风格 PPTX 时使用；也适用于需要 SCR 论证、视觉风格探索、详细图表和渲染质检的 PPT。

### `docx`

- **Path**: `skills/docx`
- **SKILL.md**: [`skills/docx/SKILL.md`](skills/docx/SKILL.md)
- **Title**: DOCX Creation, Editing, and Analysis
- **Author**: Z.AI
- **Version**: 1.0
- **License**: Proprietary. LICENSE.txt has complete terms
- **Files**: 35
- **Structure**: `scripts/`, `references/`, `scenes/`, `routes/`, `setup.sh`

> Comprehensive document creation, editing, and analysis with support for tracked changes, comments, formatting preservation, and text extraction. When GLM needs to work with professional documents (.docx files) for: (1) Creating new documents, (2) Modifying or editing content, (3) Working with tracked changes, (4) Adding comments, or any other document tasks

### `docx-generation`

- **Path**: `skills/docx-generation`
- **SKILL.md**: [`skills/docx-generation/SKILL.md`](skills/docx-generation/SKILL.md)
- **Title**: Comprehensive DOCX Generation & Conversion Skill
- **Version**: 1.0
- **Files**: 1
- **Structure**: flat

> Comprehensive DOCX Generation & Conversion Skill

### `domain-modeling`

- **Path**: `skills/domain-modeling`
- **SKILL.md**: [`skills/domain-modeling/SKILL.md`](skills/domain-modeling/SKILL.md)
- **Title**: Domain Modeling
- **Files**: 4
- **Structure**: flat

> Build and sharpen a project's domain model. Use when discussing codebase terminology, writing or editing a CONTEXT.md, or recording or editing an ADR.

### `handoff`

- **Path**: `skills/handoff`
- **SKILL.md**: [`skills/handoff/SKILL.md`](skills/handoff/SKILL.md)
- **Title**: Handoff
- **Files**: 2
- **Structure**: flat

> Compact the current conversation into a single, detailed handoff message — everything that happened, why it happened, and what's left — output in a code block so it can be copy-pasted into a fresh agent session. Use when hitting context limits, switching focus, ending a work session, or partitioning a task across fresh contexts.

### `humanizer`

- **Path**: `skills/humanizer`
- **SKILL.md**: [`skills/humanizer/SKILL.md`](skills/humanizer/SKILL.md)
- **Title**: HUMANIZER v7.0.0 — Ultimate Edition
- **License**: MIT
- **Version**: 7.0.0
- **Files**: 18
- **Structure**: flat

> Remove signs of AI-generated writing and restore natural human voice. Archetype-based detection with heuristic triage, genre-gated positive humanization, forensic artifact scanning, and a dedicated fiction protocol. Synthesizes all prior editions (v1–v6) into a single operational system. Resilient to model evolution; safe for token-constrained environments.

### `markdown-to-html`

- **Path**: `skills/markdown-to-html`
- **SKILL.md**: [`skills/markdown-to-html/SKILL.md`](skills/markdown-to-html/SKILL.md)
- **Title**: markdown-to-web — Pipeline Skill v2.1.0
- **Version**: 2.1.0
- **Files**: 1
- **Structure**: flat

> Renders an arbitrary Markdown document as a polished, single-file, accessible web page. Accepts any .md file plus an optional template (technical three-column / editorial long-form) and an optional tag registry (severity, confidence, status, custom). Built on React 19 + Vite 8 + Tailwind v4 + react-markdown + lucide-react. Includes mobile TOC drawer, back-to-top, code-block copy buttons, reading-time estimation (Latin + CJK-aware), print stylesheet, build-time title injection, source-markdown validation gate, CI workflow, and Husky pre-commit hook.

### `markdown-to-web`

- **Path**: `skills/markdown-to-web`
- **SKILL.md**: [`skills/markdown-to-web/SKILL.md`](skills/markdown-to-web/SKILL.md)
- **Title**: markdown-to-web — Validation Review & Unified Skill Specification
- **Version**: 4.1.1
- **Files**: 37
- **Structure**: flat

> Renders an arbitrary Markdown document as a polished, single-file, accessible web page. Accepts any .md file plus an optional template (editorial long-form / technical docs / minimal print) and an optional tag registry (severity, confidence, status, custom). Built on React 19 + Vite 7 + Tailwind v4 + react-markdown.

### `market-research-reports`

- **Path**: `skills/market-research-reports`
- **SKILL.md**: [`skills/market-research-reports/SKILL.md`](skills/market-research-reports/SKILL.md)
- **Title**: Market Research Reports
- **Files**: 8
- **Structure**: `scripts/`, `references/`

> Generate comprehensive market research reports (50+ pages) in the style of top consulting firms (McKinsey, BCG, Gartner). Features professional LaTeX formatting, extensive visual generation with scientific-schematics and generate-image, deep integration with research-lookup for data gathering, and multi-framework strategic analysis including Porter's Five Forces, PESTLE, SWOT, TAM/SAM/SOM, and BCG Matrix.

### `officecli`

- **Path**: `skills/officecli`
- **SKILL.md**: [`skills/officecli/SKILL.md`](skills/officecli/SKILL.md)
- **Title**: officecli
- **Files**: 1
- **Structure**: flat

> Create, analyze, proofread, and modify Office documents (.docx, .xlsx, .pptx) using the officecli CLI tool. Use when the user wants to create, inspect, check formatting, find issues, add charts, or modify Office documents.

### `pptx`

- **Path**: `skills/pptx`
- **SKILL.md**: [`skills/pptx/SKILL.md`](skills/pptx/SKILL.md)
- **Title**: PPT creation, editing, and analysis
- **Author**: Z.AI
- **Version**: 1.0
- **License**: Proprietary. LICENSE.txt has complete terms
- **Files**: 14
- **Structure**: `scripts/`

> Presentation creation, editing, and analysis for .pptx files: (1) Creating new presentations, (2) Modifying or editing content, (3) Working with layouts, (4) Adding comments or speaker notes. Academic/paper-based presentations use the embedded Beamer module at end of this file (PDF output only).

### `quiz-mastery`

- **Path**: `skills/quiz-mastery`
- **SKILL.md**: [`skills/quiz-mastery/SKILL.md`](skills/quiz-mastery/SKILL.md)
- **Title**: 测验大师 (Quiz Mastery)
- **Files**: 28
- **Structure**: `scripts/`

> 出题、测验、复习、掌握度追踪工具。**用户说"复习"、"巩固"、"回顾"任一关键词时优先触发本 skill**。当用户的请求与"题目/复习"相关时触发：把学习资料/PDF/材料转成题目练习（"给这个 PDF 出几道题"）、导入题目文件做练习（"我有一份题目文件，帮我做"）、复习已学内容（"复习一下昨天的"、"巩固一下"、"回顾下昨天"、"用艾宾浩斯帮我安排"）、遗忘曲线追踪、掌握度评分。**🔴 强制规则**：每次出题/导入题目成功后，**首轮展示题目前必须问一句**"要不要生成网页练习页？"，用户说要 → 调用 quiz-html skill。**不处理**：长期学习项目的进度管理、计划制定（→ study-buddy）。

### `research`

- **Path**: `skills/research`
- **SKILL.md**: [`skills/research/SKILL.md`](skills/research/SKILL.md)
- **Title**: research
- **Files**: 2
- **Structure**: flat

> Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo. Use when the user wants a topic researched, docs or API facts gathered, or reading legwork delegated to a background agent.

### `resume-builder`

- **Path**: `skills/resume-builder`
- **SKILL.md**: [`skills/resume-builder/SKILL.md`](skills/resume-builder/SKILL.md)
- **Title**: Resume Builder（简历生成与优化）
- **Files**: 13
- **Structure**: `scripts/`, `references/`

> 从零生成或全面优化一份中文简历，并导出 docx / pdf / markdown 多种格式。用 STAR 法则改写经历、做 ATS 关键词覆盖率检查、根据行业（互联网产品 / 技术 / 金融 / 通用）选模板。当用户说"帮我写简历 / 优化简历 / 简历不会写 / 我的简历太弱了 / 简历看起来不专业 / 简历改一改 / 给我做个简历模板 / 简历导出 / 简历加点关键词"，或者上传 .pdf/.docx 简历后说"看看怎么改"时，必须触发本 skill。即使用户只问"我的简历有什么问题"也要触发。

### `source-driven-development`

- **Path**: `skills/source-driven-development`
- **SKILL.md**: [`skills/source-driven-development/SKILL.md`](skills/source-driven-development/SKILL.md)
- **Title**: Source-Driven Development
- **Files**: 1
- **Structure**: flat

> Grounds every implementation decision in official documentation. Use when you want authoritative, source-cited code free from outdated patterns. Use when building with any framework or library where correctness matters.

### `study-buddy`

- **Path**: `skills/study-buddy`
- **SKILL.md**: [`skills/study-buddy/SKILL.md`](skills/study-buddy/SKILL.md)
- **Title**: 督学助手 (Study Buddy)
- **Files**: 1
- **Structure**: flat

> 智能督学助手，管理用户的长期学习项目工作流。当用户表达学习项目相关意图时触发：创建/制定学习计划（"我想学X"、"帮我制定计划"）、汇报学习进度（"学完了"、"今天搞定了"、"完成今日任务"）、查询计划状态（"我学到哪了"、"看下进度"）、查看学习报告（"日报""周报""月报""项目总结""5月10号到15号的报告"）、晨间/晚间打卡复盘、督促、动态调整计划、抱怨学不下去时（情绪支持）。**🔴 项目生成流程铁律**：项目生成成功后**必须一口气走完"项目→知识点→计划表"**，禁止只汇报"项目已生成 / X 个知识点 / X 个模块"就停下，必须**立即**输出"DAY / 项目 / 知识点 / 时长 / 难度"表格供用户确认 DAY 安排，否则视为流程失败。**🔴 报告查询铁律**：用户表达查看学习报告意图时（日报/周报/月报/项目总结/任意时间段），必须从 USER.md 取**对应时间段**的 `project_id` + `knowledge_id`，传给 `study_buddy_supervise` 工具的 `study_check` action 拿原始数据，按"模块3 主动报告查询"输出，**全程只读不写 USER.md**。**不处理**：单次出题（→ quiz-mastery）、Cheatsheet 生成（→ cheat-sheet）、把题目文件导入做练习...

### `to-distill-project-into-skill`

- **Path**: `skills/to-distill-project-into-skill`
- **SKILL.md**: [`skills/to-distill-project-into-skill/SKILL.md`](skills/to-distill-project-into-skill/SKILL.md)
- **Title**: Distill Project Into Skill — Meta-SKILL
- **Version**: 1.0.0
- **Files**: 9
- **Structure**: flat

> Meta-skill for distilling a complete project codebase into a comprehensive, maintainable SKILL.md document. Use after a major project update, when onboarding a new team, or when you need to create a single-source-of-truth reference for future AI coding agents working on this codebase.

### `unslop`

- **Path**: `skills/unslop`
- **SKILL.md**: [`skills/unslop/SKILL.md`](skills/unslop/SKILL.md)
- **Title**: Unslop
- **Files**: 2
- **Structure**: flat

> Cut AI tells from text you write or edit for a human reader (commit messages, PR titles and bodies, docs, code comments, replies). Apply before committing, posting, or sending; leave prose you didn't touch alone.

### `writing-for-agents`

- **Path**: `skills/writing-for-agents`
- **SKILL.md**: [`skills/writing-for-agents/SKILL.md`](skills/writing-for-agents/SKILL.md)
- **Title**: writing-for-agents
- **Files**: 3
- **Structure**: flat

> Writing documents for agents. Use when creating or editing skills, or modifying AGENTS.md or CLAUDE.md.

---

## 9. Career, Learning & Personal Development

> Skills for resumes, interviews, study aids, mindfulness, and personal growth.
> **12 skills** in this category.

### `dream-interpreter`

- **Path**: `skills/dream-interpreter`
- **SKILL.md**: [`skills/dream-interpreter/SKILL.md`](skills/dream-interpreter/SKILL.md)
- **Title**: dream-interpreter
- **Files**: 9
- **Structure**: `scripts/`, `references/`

> AI 解梦大师。用户描述梦境，智能追问关键细节后，从三个视角（周公解梦/心理分析/赛博神棍）生成解读，输出结构化 JSON 供前端渲染"梦境解析卡"。

### `gaokao-collect-student-info`

- **Path**: `skills/gaokao-collect-student-info`
- **SKILL.md**: [`skills/gaokao-collect-student-info/SKILL.md`](skills/gaokao-collect-student-info/SKILL.md)
- **Title**: 高考考生信息采集
- **Files**: 4
- **Structure**: flat

> 高考志愿填报信息采集：以考生原生表述为准，收集省份、分数、选科等 API 必填项及兴趣、 家庭、就业方向等辅助信息，尽量不做改写与过度归纳，输出结构化 student.json。 适用于高考志愿咨询开场、考生信息登记、志愿填报前的信息收集。

### `gaokao-fetch-volunteers`

- **Path**: `skills/gaokao-fetch-volunteers`
- **SKILL.md**: [`skills/gaokao-fetch-volunteers/SKILL.md`](skills/gaokao-fetch-volunteers/SKILL.md)
- **Title**: 获取推荐志愿表
- **Files**: 13
- **Structure**: `scripts/`

> 调用高考智能推荐志愿表 API，根据考生基本信息及专业/城市/院校倾向（映射为 API 选填参数） 获取冲稳保志愿列表，解析为 parsed.json。适用于获取推荐院校、冲稳保志愿表、志愿 API 调用。

### `gaokao-generate-report`

- **Path**: `skills/gaokao-generate-report`
- **SKILL.md**: [`skills/gaokao-generate-report/SKILL.md`](skills/gaokao-generate-report/SKILL.md)
- **Title**: 生成志愿填报报告
- **Files**: 6
- **Structure**: `scripts/`

> 合并考生信息、志愿列表、专业推荐与院校推荐，生成融合分析与冲稳保志愿列表的 HTML 志愿填报报告。 适用于高考志愿报告生成、志愿填报方案输出、志愿表可视化。

### `gaokao-recommend-majors`

- **Path**: `skills/gaokao-recommend-majors`
- **SKILL.md**: [`skills/gaokao-recommend-majors/SKILL.md`](skills/gaokao-recommend-majors/SKILL.md)
- **Title**: 推荐专业与就业方向
- **Files**: 3
- **Structure**: flat

> 基于考生画像与 API 志愿列表，由 Agent 分析推荐适合的专业方向、就业出口与具体专业清单， 输出结构化 major_recommendation.json。适用于高考专业推荐、选专业、就业方向分析。

### `gaokao-recommend-schools`

- **Path**: `skills/gaokao-recommend-schools`
- **SKILL.md**: [`skills/gaokao-recommend-schools/SKILL.md`](skills/gaokao-recommend-schools/SKILL.md)
- **Title**: 推荐院校与理由
- **Files**: 3
- **Structure**: flat

> 基于推荐专业列表、考生画像与志愿列表，由 Agent 分析推荐院校并给出个性化理由， 输出结构化 school_recommendation.json。适用于高考院校推荐、选大学、冲稳保院校布局。

### `get-fortune-analysis`

- **Path**: `skills/get-fortune-analysis`
- **SKILL.md**: [`skills/get-fortune-analysis/SKILL.md`](skills/get-fortune-analysis/SKILL.md)
- **Title**: Skill Name: get-fortune-analysis
- **Files**: 2
- **Structure**: flat

> 生成视觉华丽、内容详实、具有仪式感的流年运势报告（流金星象风格）。

### `gift-evaluator`

- **Path**: `skills/gift-evaluator`
- **SKILL.md**: [`skills/gift-evaluator/SKILL.md`](skills/gift-evaluator/SKILL.md)
- **Title**: gift-evaluator
- **License**: Internal Tool
- **Files**: 2
- **Structure**: flat

> The PRIMARY tool for Spring Festival gift analysis and social interaction generation. Use this skill when users upload photos of gifts (alcohol, tea, supplements, etc.) to inquire about their value, authenticity, or how to respond socially. Integrates visual perception, market valuation, and HTML card generation.

### `idea-refine`

- **Path**: `skills/idea-refine`
- **SKILL.md**: [`skills/idea-refine/SKILL.md`](skills/idea-refine/SKILL.md)
- **Title**: Idea Refine
- **Files**: 5
- **Structure**: `scripts/`

> Refines ideas iteratively. Refine ideas through structured divergent and convergent thinking. Use "idea-refine" or "ideate" to trigger.

### `jd-resume-tailor`

- **Path**: `skills/jd-resume-tailor`
- **SKILL.md**: [`skills/jd-resume-tailor/SKILL.md`](skills/jd-resume-tailor/SKILL.md)
- **Title**: JD ⇄ Resume Tailor（JD 拆解 + 简历定向改写）
- **Files**: 5
- **Structure**: `scripts/`, `references/`

> 给定一份 JD 和一份现有简历，做"JD 拆解 + 简历定向改写"。拆 JD 抽出硬技能、软技能、加分项；对照简历做 gap 分析；产出针对该岗位重写后的简历，突出相关经验、补齐关键词缺口、并保留候选人真实经历不编造。当用户说"针对这个岗位 / 这家公司改简历""帮我对一下这个 JD""我想投这个职位你看怎么改""把这份简历针对 X 公司优化""做一份定向版简历"，或同时给出 JD 文本 + 简历文件时，必须触发本 skill。**请勿用本 skill 做"从零写简历"**——那是 resume-builder 的事。

### `quiz-html`

- **Path**: `skills/quiz-html`
- **SKILL.md**: [`skills/quiz-html/SKILL.md`](skills/quiz-html/SKILL.md)
- **Title**: 网页题库生成器 (Quiz HTML Builder)
- **Files**: 6
- **Structure**: `scripts/`

> 把题目数组生成一个**可独立运行的网页练习页**（HTML 文件）。当用户完成 quiz-mastery 的「从资料出题」或「从文件提取题目」流程后，应主动询问是否需要"在网页里练习"，确认后调用本 skill 把题目注入模板，生成 HTML 给用户。也支持用户直接说"把这些题做成网页/HTML/练习页"时触发。**不处理**：出题（→ quiz-mastery）、评分（→ quiz-mastery）、长期复习计划（→ study-buddy）。

### `teach`

- **Path**: `skills/teach`
- **SKILL.md**: [`skills/teach/SKILL.md`](skills/teach/SKILL.md)
- **Title**: teach
- **Files**: 6
- **Structure**: flat

> Teach the user a new skill or concept, within this workspace.

---

## 10. DevOps, Infrastructure & External Integrations

> Skills for cloud, deployment, external services, search, research, and tooling.
> **9 skills** in this category.

### `luxeverse-architect`

- **Path**: `skills/luxeverse-architect`
- **SKILL.md**: [`skills/luxeverse-architect/SKILL.md`](skills/luxeverse-architect/SKILL.md)
- **Title**: Then re-run typecheck to regenerate from the new source tree
- **Version**: 5.0.0
- **Files**: 10
- **Structure**: flat

> LuxeVerse Architect Skill Comprehensive Architectural & Execution Framework for Cinematic, Production-Grade, Anti-Generic Web Platforms

**Sub-skills / templates (1):**

| Name | Path | Description |
|------|------|-------------|
| `luxeverse-architect-skill` | `skills/luxeverse-architect/luxeverse-architect-skill` | Comprehensive Architectural & Execution Framework for Cinematic, Production-Grade, Anti-Generic Web Platforms |

### `multi-search-engine`

- **Path**: `skills/multi-search-engine`
- **SKILL.md**: [`skills/multi-search-engine/SKILL.md`](skills/multi-search-engine/SKILL.md)
- **Title**: Multi Search Engine v2.0.1
- **Files**: 7
- **Structure**: `references/`

> Multi search engine integration with 8 domestic (CN) search engines. Supports advanced search operators, time filters, site search, and WeChat article search. No API keys required.

### `rootless-postgresql`

- **Path**: `skills/rootless-postgresql`
- **SKILL.md**: [`skills/rootless-postgresql/SKILL.md`](skills/rootless-postgresql/SKILL.md)
- **Title**: Rootless PostgreSQL — User-Space Install & Run (Debian, No Root)
- **Files**: 2
- **Structure**: flat

> Install, initialize, and run a PostgreSQL server and client locally without root on Debian (trixie/sid), for a non-root user with a writable /home/project directory. Use when asked to install or start PostgreSQL without sudo, without systemd, or when apt install fails with permission errors. Resolves the major version dynamically, extracts .debs into a user-owned prefix, and provides idempotent start/stop/status scripts.

### `skill-finder-cn`

- **Path**: `skills/skill-finder-cn`
- **SKILL.md**: [`skills/skill-finder-cn/SKILL.md`](skills/skill-finder-cn/SKILL.md)
- **Title**: Skill 查找器
- **Author**: 赚钱小能手
- **Files**: 4
- **Structure**: `scripts/`

> Skill 查找器 | Skill Finder. 帮助发现和安装 ClawHub Skills | Discover and install ClawHub Skills. 回答'有什么技能可以X'、'找一个技能' | Answers 'what skill can X', 'find a skill'. 触发词：找 skill、find skill、搜索 skill.

### `task-review`

- **Path**: `skills/task-review`
- **SKILL.md**: [`skills/task-review/SKILL.md`](skills/task-review/SKILL.md)
- **Title**: task-review
- **Files**: 1
- **Structure**: flat

> 当用户指令为高复杂度任务时触发，用于将刚完成的任务路径保存为可复用技能，生成相关的SKILL.md文档。

### `template-skill`

- **Path**: `skills/template-skill`
- **SKILL.md**: [`skills/template-skill/SKILL.md`](skills/template-skill/SKILL.md)
- **Title**: Insert instructions below
- **Files**: 1
- **Structure**: flat

> Replace with description of the skill and when Claude should use it.

### `using-agent-skills`

- **Path**: `skills/using-agent-skills`
- **SKILL.md**: [`skills/using-agent-skills/SKILL.md`](skills/using-agent-skills/SKILL.md)
- **Title**: Using Agent Skills
- **Files**: 1
- **Structure**: flat

> Discovers and invokes agent skills. Use when starting a session or when you need to discover which skill applies to the current task. This is the meta-skill that governs how all other skills are discovered and invoked.

### `visual-design-foundations`

- **Path**: `skills/visual-design-foundations`
- **SKILL.md**: [`skills/visual-design-foundations/SKILL.md`](skills/visual-design-foundations/SKILL.md)
- **Title**: Visual Design Foundations
- **Files**: 4
- **Structure**: `references/`

> Apply typography, color theory, spacing systems, and iconography principles to create cohesive visual designs. Use when establishing design tokens, building style guides, or improving visual hierarchy and consistency.

### `web-design-guidelines`

- **Path**: `skills/web-design-guidelines`
- **SKILL.md**: [`skills/web-design-guidelines/SKILL.md`](skills/web-design-guidelines/SKILL.md)
- **Title**: Web Interface Guidelines
- **Author**: vercel
- **Version**: 1.0.0
- **Files**: 1
- **Structure**: flat

> Review UI code for Web Interface Guidelines compliance. Use when asked to "review my UI", "check accessibility", "audit design", "review UX", or "check my site against best practices".

---

## Summary Statistics

- **Spec-compliant skills listed**: 218
- **Top-level folders under `skills/` scanned**: 267
- **Folders with a top-level `SKILL.md`**: 246
- **Grouping folders without a top-level `SKILL.md` (excluded)**: 21
- **Folders whose `SKILL.md` frontmatter fails skill-spec validation (excluded)**: 28
- **Total files across listed skills**: 13920
- **Listed skills with nested sub-skills / templates**: 4 (4 nested sub-skills total)
- **Listed skills with `scripts/`**: 61
- **Listed skills with `references/`**: 50
- **Listed skills with `scenes/`**: 2
- **Listed skills with `routes/`**: 2
- **Listed skills with `engines/`**: 1
- **Listed skills with `setup.sh`**: 3

### Per-category counts

| # | Category | Skills |
|---|----------|--------|
| 1 | Frontend Development & UI Engineering | 50 |
| 2 | Design Artifacts & Visual Creation | 16 |
| 3 | Full-Stack & Backend Development | 13 |
| 4 | AI / ML / Multimodal SDK Skills | 11 |
| 5 | Testing, QA & Performance | 28 |
| 6 | Code Quality, Security & Architecture | 23 |
| 7 | Planning, Workflow & Project Management | 32 |
| 8 | Documentation & Content Creation | 24 |
| 9 | Career, Learning & Personal Development | 12 |
| 10 | DevOps, Infrastructure & External Integrations | 9 |
| | **Total** | **218** |

---

## Validation & Exclusions

A folder under `skills/` is listed in this inventory only when it passes skill-spec validation: it contains a top-level `SKILL.md` whose YAML frontmatter declares a spec-compliant header — `name` (lowercase letters, digits, and hyphens only; max 64 characters; must match the folder name) and `description` (non-empty; max 1024 characters). Everything else under `skills/` is excluded from the listings above.

### Grouping folders without a top-level `SKILL.md` (21)

These folders hold nested sub-skills or auxiliary content but are not skills themselves (nested sub-skills listed at any depth):

| Folder | Nested sub-skills |
|--------|-------------------|
| `agent-orchestration` | `agent-self-scheduling`, `cmux`, `codex-subagent`, `fable-review`, `fable-safe-prompt`, `git-worktree`, `goal-loop`, `gpt-review`, `launch-subagent`, `run-deep-swe` |
| `docs` | _none_ |
| `earnings-reviewer` | `skills/audit-xls`, `skills/earnings-analysis`, `skills/earnings-preview`, `skills/model-update`, `skills/morning-note`, `skills/xlsx-author` |
| `equity-research` | `skills/catalyst-calendar`, `skills/earnings-analysis`, `skills/earnings-preview`, `skills/idea-generation`, `skills/initiating-coverage`, `skills/model-update`, `skills/morning-note`, `skills/sector-overview`, `skills/thesis-tracker` |
| `financial-analysis` | `skills/3-statement-model`, `skills/audit-xls`, `skills/clean-data-xls`, `skills/competitive-analysis`, `skills/comps-analysis`, `skills/dcf-model`, `skills/deck-refresh`, `skills/ib-check-deck`, `skills/lbo-model`, `skills/ppt-template-creator`, `skills/pptx-author`, `skills/skill-creator`, `skills/xlsx-author` |
| `fund-admin` | `skills/accrual-schedule`, `skills/break-trace`, `skills/gl-recon`, `skills/nav-tieout`, `skills/roll-forward`, `skills/variance-commentary` |
| `gl-reconciler` | `skills/audit-xls`, `skills/break-trace`, `skills/gl-recon`, `skills/xlsx-author` |
| `investment-banking` | `skills/buyer-list`, `skills/cim-builder`, `skills/datapack-builder`, `skills/deal-tracker`, `skills/merger-model`, `skills/pitch-deck`, `skills/process-letter`, `skills/strip-profile`, `skills/teaser` |
| `market-researcher` | `skills/competitive-analysis`, `skills/comps-analysis`, `skills/idea-generation`, `skills/pptx-author`, `skills/sector-overview` |
| `meeting-prep-agent` | `skills/client-report`, `skills/client-review`, `skills/investment-proposal`, `skills/pptx-author` |
| `model-builder` | `skills/3-statement-model`, `skills/audit-xls`, `skills/comps-analysis`, `skills/dcf-model`, `skills/lbo-model`, `skills/xlsx-author` |
| `month-end-closer` | `skills/accrual-schedule`, `skills/audit-xls`, `skills/roll-forward`, `skills/variance-commentary`, `skills/xlsx-author` |
| `operations` | `skills/kyc-doc-parse`, `skills/kyc-rules` |
| `ops-and-setup` | `anti-sleep`, `create-readonly-db-role`, `global-agent-guardrails`, `google-safe-browsing`, `macbook-metrics-setup`, `nuke-cursor-app`, `pi-custom-model`, `prod-push`, `setup-help`, `vps-server-management` |
| `pitch-agent` | `skills/3-statement-model`, `skills/audit-xls`, `skills/comps-analysis`, `skills/dcf-model`, `skills/deck-refresh`, `skills/ib-check-deck`, `skills/lbo-model`, `skills/pitch-deck`, `skills/pptx-author`, `skills/sector-overview`, `skills/xlsx-author` |
| `private-equity` | `skills/ai-readiness`, `skills/dd-checklist`, `skills/dd-meeting-prep`, `skills/deal-screening`, `skills/deal-sourcing`, `skills/ic-memo`, `skills/portfolio-monitoring`, `skills/returns-analysis`, `skills/unit-economics`, `skills/value-creation-plan` |
| `research-and-web` | `browser-harness`, `deep-research`, `deepapi`, `fireflies-transcript`, `online-shopping`, `pi-web-search`, `research-prompt`, `youtube-transcript` |
| `skill-authoring` | `distribute-skill-to-all-agents`, `effective-agent-skills`, `folder-specific-claude-and-agents-md`, `push-skill-to-github` |
| `statement-auditor` | `skills/audit-xls`, `skills/nav-tieout`, `skills/xlsx-author` |
| `thinking-and-docs` | `before-building`, `brain-to-docs`, `decisions`, `level-up`, `next-decision`, `prompt-me`, `read-all-adrs`, `remind`, `save-idea`, `short` |
| `valuation-reviewer` | `skills/ic-memo`, `skills/portfolio-monitoring`, `skills/returns-analysis`, `skills/xlsx-author` |

### `SKILL.md` frontmatter not spec-compliant (28)

These folders contain a `SKILL.md`, but its YAML header violates the skill spec (fix the frontmatter to have the skill included in the next sync):

| Folder | Reason |
|--------|--------|
| `ASR` | `name: ASR` — lowercase letters, digits and hyphens only |
| `TTS` | `name: TTS` — lowercase letters, digits and hyphens only |
| `VLM` | `name: VLM` — lowercase letters, digits and hyphens only |
| `ai-news-collectors` | `name: ai-news-collector` does not match folder name `ai-news-collectors` |
| `aminer-free-academic` | `description` is 1477 chars — exceeds 1024-char limit |
| `dotnet-9` | `description` is 1322 chars — exceeds 1024-char limit |
| `fastapi-sqlalchemy` | `description` is 1326 chars — exceeds 1024-char limit |
| `fastify` | `description` is 1773 chars — exceeds 1024-char limit |
| `flutter` | `description` is 1101 chars — exceeds 1024-char limit |
| `go-web` | `description` is 1118 chars — exceeds 1024-char limit |
| `hono` | `description` is 1780 chars — exceeds 1024-char limit |
| `how-to-git-push-using-ssh-wrapper` | no YAML frontmatter |
| `htmx` | `description` is 1777 chars — exceeds 1024-char limit |
| `keystonejs-6` | `description` is 2168 chars — exceeds 1024-char limit |
| `nestjs` | `description` is 1502 chars — exceeds 1024-char limit |
| `nextjs16-react19-tailwindv4-trpcv11-drizzle-better-auth` | `description` is 1130 chars — exceeds 1024-char limit |
| `pdf-old-20260806` | `name: pdf` does not match folder name `pdf-old-20260806` |
| `phoenix-1-7` | `description` is 1456 chars — exceeds 1024-char limit |
| `podcast-generate` | `name: Podcast Generate` — lowercase letters, digits and hyphens only; `name: Podcast Generate` does not match folder name `podcast-generate` |
| `ponytail` | `description` is 1723 chars — exceeds 1024-char limit |
| `qingyan-research` | `name: qingyan_research_report` — lowercase letters, digits and hyphens only; `name: qingyan_research_report` does not match folder name `qingyan-research` |
| `rails-8` | `description` is 1174 chars — exceeds 1024-char limit |
| `react-native-expo` | `description` is 1439 chars — exceeds 1024-char limit |
| `rust-web` | `description` is 1226 chars — exceeds 1024-char limit |
| `solidstart` | `description` is 1733 chars — exceeds 1024-char limit |
| `spring-boot-3` | `description` is 1504 chars — exceeds 1024-char limit |
| `tauri-2` | `description` is 1705 chars — exceeds 1024-char limit |
| `translation-engine` | `description` is 1057 chars — exceeds 1024-char limit |
