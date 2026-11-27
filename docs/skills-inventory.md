# Skills Inventory — my-pi-agent

> Generated 2026-11-27 by `tools/skills_docs.py` from a live scan (`tools/skills_audit.py`). **Consistent with `skills/skills-catalog.md`.**
> **343 valid skills** (each in its own folder with a spec- and Claude-compliant `SKILL.md`), 92 unique bundled sub-skills merged from 138 copies, 7 excluded folders.

---

## How to read this inventory

- **Path / SKILL.md** — location of the skill folder and its manifest
- **Title** — first H1 in `SKILL.md` (falls back to the folder name)
- **Files** — total files in the skill folder (recursive)
- **Structure** — standard sub-directories present (`flat` when none)
- **Flags** — validator warnings that do not exclude the skill (see Validation & exclusions)
- **Duplicate** — a top-level skill whose body is essentially identical to another

## Category Index

1. **Frontend Development & UI Engineering** — 70 skills — [jump](#1-frontend-development--ui-engineering)
2. **Design Artifacts & Visual Creation** — 21 skills — [jump](#2-design-artifacts--visual-creation)
3. **Full-Stack & Backend Development** — 22 skills — [jump](#3-full-stack--backend-development)
4. **AI / ML / Multimodal SDK Skills** — 17 skills — [jump](#4-ai--ml--multimodal-sdk-skills)
5. **Testing, QA & Performance** — 39 skills — [jump](#5-testing-qa--performance)
6. **Code Quality, Security & Architecture** — 54 skills — [jump](#6-code-quality-security--architecture)
7. **Planning, Workflow & Project Management** — 54 skills — [jump](#7-planning-workflow--project-management)
8. **Documentation & Content Creation** — 38 skills — [jump](#8-documentation--content-creation)
9. **Career, Learning & Personal Development** — 13 skills — [jump](#9-career-learning--personal-development)
10. **DevOps, Infrastructure & External Integrations** — 15 skills — [jump](#10-devops-infrastructure--external-integrations)

---

## 1. Frontend Development & UI Engineering

> **70 skills** in this category.

### `agent-browser`

- **Path**: `skills/agent-browser`
- **SKILL.md**: [`skills/agent-browser/SKILL.md`](/skills/agent-browser/SKILL.md)
- **Title**: Browser Automation with agent-browser
- **Files**: 1
- **Structure**: flat
- **Flags**: `METADATA_NON_STRING`, `UNKNOWN_KEYS`, `BODY_LENGTH`

> A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands. Is a better choice for AI agent workflows - compact snapshots save tokens, the auth vault handles credentials securely, and React DevTools integration is valuable for frontend debugging.

### `animate`

- **Path**: `skills/animate`
- **SKILL.md**: [`skills/animate/SKILL.md`](/skills/animate/SKILL.md)
- **Title**: Building Animations
- **Files**: 2
- **Structure**: flat

> Build an animation from scratch, making the decisions in the order that determines whether it feels right — should it animate at all, what purpose, which tool, which properties, which curve and duration, how it interrupts, how it exits. Writes the implementation. Use when asked to animate something, add motion, make a component feel alive, or build a transition. For critiquing existing motion use review-animations; for auditing a whole codebase use improve-animations.

### `animate-expo`

- **Path**: `skills/animate-expo`
- **SKILL.md**: [`skills/animate-expo/SKILL.md`](/skills/animate-expo/SKILL.md)
- **Title**: Building Animations in Expo
- **Files**: 2
- **Structure**: flat

> Build animations in React Native and Expo, making the decisions in the order that determines whether they feel right — should it animate, which thread it runs on, which properties, spring or timing, how the gesture hands off, how it degrades. Writes the implementation with Reanimated, Gesture Handler, Expo Router and expo-haptics. Use when animating anything in an Expo app, adding gestures, sheets, screen transitions, press feedback or haptics, or fixing motion that stutters on device. For web animation use `animate`.

### `animation-vocabulary`

- **Path**: `skills/animation-vocabulary`
- **SKILL.md**: [`skills/animation-vocabulary/SKILL.md`](/skills/animation-vocabulary/SKILL.md)
- **Title**: Animation Vocabulary
- **Files**: 1
- **Structure**: flat

> Reverse-lookup glossary that turns a vague description of a web animation or motion effect into its exact term ("the bouncy thing when a popover opens" → Pop in; "the iOS rubber-band scroll" → Rubber-banding). Use when the user asks "what's it called when…", or describes a motion effect without knowing its name and wants the right word to prompt an AI or designer with. For naming an effect, not designing or building one.

### `api-and-interface-design`

- **Path**: `skills/api-and-interface-design`
- **SKILL.md**: [`skills/api-and-interface-design/SKILL.md`](/skills/api-and-interface-design/SKILL.md)
- **Title**: API and Interface Design
- **Files**: 1
- **Structure**: flat

> Guides stable API and interface design. Use when designing APIs, module boundaries, or any public interface. Use when creating REST or GraphQL endpoints, defining type contracts between modules, or establishing boundaries between frontend and backend.

### `apple-design`

- **Path**: `skills/apple-design`
- **SKILL.md**: [`skills/apple-design/SKILL.md`](/skills/apple-design/SKILL.md)
- **Title**: Apple Design
- **Files**: 1
- **Structure**: flat

> Apple's approach to interface design and fluid, physical motion, translated for the web. Use when building or reviewing gesture-driven UI, spring animations, drag/swipe/sheet interactions, momentum and interruptible transitions, translucent materials and depth, typography (optical sizing, tracking, leading), reduced-motion, or the design foundations (feedback, spatial consistency, restraint) behind Apple-style interfaces.

### `ask-sonner`

- **Path**: `skills/ask-sonner`
- **SKILL.md**: [`skills/ask-sonner/SKILL.md`](/skills/ask-sonner/SKILL.md)
- **Title**: Working With Sonner
- **Files**: 2
- **Structure**: flat

> Guide to Sonner, the React toast library — install and wire up the Toaster, pick the right toast() call, promise and loading toasts, updating, dismissing and persisting toasts, styling, theming and icons, positioning and multiple toasters. Use when working with Sonner or troubleshooting it — toasts that don't appear, appear twice, lose their styles, ignore Tailwind classes, sit behind a modal, or don't follow dark mode.

### `astro-7`

- **Path**: `skills/astro-7`
- **SKILL.md**: [`skills/astro-7/SKILL.md`](/skills/astro-7/SKILL.md)
- **Title**: Astro 5/6/7 — Content-Focused Web Framework (Islands Architecture)
- **Files**: 7
- **Structure**: flat
- **License**: Proprietary. LICENSE.txt has complete terms
- **Flags**: `BODY_LENGTH`

> Astro — content-focused web framework (islands architecture). Server-first, zero JS by default — Astro components render to static HTML at build time, hydration opt-in per island via client:load/client:idle/client:visible/client:only/client:media. Covers multi-framework islands (React, Vue, Svelte, Preact, Solid via @astrojs/*), Content Layer API & Live Content Collections (glob/file/external loaders, Zod schemas), file-based routing + layouts + View Transitions + Server Islands, middleware/Endpoints/Sessions/Actions, astro:env + astro:assets (Image/Picture/Font) + i18n + route caching, and deployment via static hosts (Netlify/Vercel/Cloudflare/GH Pages) or SSR adapters. Use when building any content site — blog, docs, marketing site, portfolio, e-commerce catalog — especially for content collections, hydration strategy, mixing frameworks, or where Astro's zero-JS approach differs from Next.js/Nuxt/SvelteKit.

### `astro-7-patterns`

- **Path**: `skills/astro-7-patterns`
- **SKILL.md**: [`skills/astro-7-patterns/SKILL.md`](/skills/astro-7-patterns/SKILL.md)
- **Title**: Astro 7 Patterns — Field Notes from a Production Clone Build
- **Files**: 1
- **Structure**: flat
- **Version**: 1.4
- **Flags**: `UNKNOWN_KEYS`, `BODY_LENGTH`

> Astro 7 supplement skill — distilled patterns, anti-patterns, troubleshooting playbooks, and hard-won lessons from a production clone build. Covers the Astro 7 Rust compiler's strict apostrophe handling, Content Layer + Zod 4 imports, View Transitions script re-initialization, Fonts API + Tailwind 4 @theme integration, headroom sticky headers, vanilla JS carousels, mobile menu accessibility, dark/light section systems, and design extraction via agent-browser. Use when building a real Astro 7 site (not just reading docs) — every pattern below was debugged in a live build. Pairs with the canonical `astro-7` skill.

### `authjs-vs-better-auth`

- **Path**: `skills/authjs-vs-better-auth`
- **SKILL.md**: [`skills/authjs-vs-better-auth/SKILL.md`](/skills/authjs-vs-better-auth/SKILL.md)
- **Title**: authjs-vs-better-auth
- **Files**: 1
- **Structure**: flat
- **Version**: 1.0.0
- **Flags**: `UNKNOWN_KEYS`

> Compares Auth.js v5 and Better Auth for Next.js 16 projects. Side-by-side code for instance setup, route handlers, client auth, and server sessions. Database schema mapping for migration. Proxy.ts route protection pattern. Use when choosing an auth library, migrating from Auth.js to Better Auth, implementing proxy.ts checks, or debugging Next.js 16 auth issues.

### `avant-garde-design-v4`

- **Path**: `skills/avant-garde-design-v4`
- **SKILL.md**: [`skills/avant-garde-design-v4/SKILL.md`](/skills/avant-garde-design-v4/SKILL.md)
- **Title**: Avant-Garde Web Design Skill v4.0
- **Files**: 21
- **Structure**: references
- **Flags**: `BODY_LENGTH`

> Elite web design skill for producing distinctive, production-grade frontend interfaces. Use when: (1) Building new web UI from scratch, (2) Creating luxury/premium brand experiences, (3) Designing landing pages, marketing sites, or product showcases, (4) Reviewing UI designs for Anti-Generic compliance, (5) Establishing design direction for a project, (6) Migrating from Tailwind v3 to v4, (7) Debugging mobile navigation issues, (8) User asks for "avant-garde", "distinctive", "non-generic", "luxury", or "premium" design. Triggers on phrases like "create a beautiful website", "design a landing page", "build a luxury UI", "make it distinctive", "avoid generic design", "mobile nav not working", "tailwind v4 migration".

### `brutalist-portfolio-nextjs`

- **Path**: `skills/brutalist-portfolio-nextjs`
- **SKILL.md**: [`skills/brutalist-portfolio-nextjs/SKILL.md`](/skills/brutalist-portfolio-nextjs/SKILL.md)
- **Title**: Nicholas Yun — The Engineered Soul: Complete Skill Reference (v6)
- **Files**: 2
- **Structure**: flat
- **Flags**: `BODY_LENGTH`

> Complete Next.js 16 + React 19 + TypeScript strict brutalist portfolio reference. App Router, Server Components, 16 components, design system with Tailwind v4 CSS-first @theme, 8+ remediation phases, 52 lessons learned. Covers WCAG AAA accessibility, custom hooks, anti-pattern debugging, before/after debugging, mobile nav debugging. Use when building brutalist/avant-garde portfolio sites or reconstructing a production-grade Next.js portfolio from scratch.

### `charts`

- **Path**: `skills/charts`
- **SKILL.md**: [`skills/charts/SKILL.md`](/skills/charts/SKILL.md)
- **Title**: Beautiful Charts
- **Files**: 12
- **Structure**: references
- **License**: Proprietary. LICENSE.txt has complete terms
- **Author**: Z.AI
- **Version**: 1.0

> Professional chart and diagram creation skill. Covers all types of visual data representation and structural diagrams: - **Data charts**: bar charts, line charts, pie charts, scatter plots, heatmaps, radar charts, candlestick charts, boxplots, histograms, area charts, waterfall charts, regression plots, distribution plots, and statistical visualizations. - **Structural diagrams**: flowcharts, mind maps, tree diagrams, org charts, architecture diagrams, network/relationship graphs, ER diagrams, class diagrams, Gantt charts, swimlane diagrams, and sequence diagrams. - **Dashboards**: data dashboards, KPI panels, multi-chart compositions, and interactive visualizations. - **Design quality**: professional color systems, anti-overlap rules, layout optimization, scene-based framework routing (matplotlib, seaborn, ECharts, D3.js, Mermaid, Playwright+CSS), and publication-ready output.

### `clone-app-pat-pro`

- **Path**: `skills/clone-app-pat-pro`
- **SKILL.md**: [`skills/clone-app-pat-pro/SKILL.md`](/skills/clone-app-pat-pro/SKILL.md)
- **Title**: Clone App — Pat Pro
- **Files**: 16
- **Structure**: references, scripts
- **Flags**: `UNKNOWN_KEYS`

> Clones any web app pixel-for-pixel from a URL. Runs as an IN-CONVERSATION workflow — the live Claude orchestrates Task sub-agents and drives the Claude Chrome extension to recon (every view), extract (computed styles = ground truth), design-spec, build, QA (computed-style assertions), and extend. Guided check-ins, custom features, and an MCP server so an agent can operate the app. Use when cloning a site, replicating a web app, building a clone, copying a website, recreating a UI, or when told "clone this", "replicate this app", "copy this site", "build a clone of", "make a copy of this website", "recreate this UI".

### `cloudflare-tunnel`

- **Path**: `skills/cloudflare-tunnel`
- **SKILL.md**: [`skills/cloudflare-tunnel/SKILL.md`](/skills/cloudflare-tunnel/SKILL.md)
- **Title**: Cloudflare Tunnel Service Management
- **Files**: 1
- **Structure**: flat
- **Flags**: `BODY_LENGTH`

> Add new local services to an existing Cloudflare Tunnel for secure public access. Use when you need to expose a local development server, web application, or service running on localhost to the public internet via Cloudflare's tunnel infrastructure. Prerequisites: cloudflared installed and authenticated, existing tunnel created. Triggers: "add tunnel", "expose local service", "cloudflare tunnel", "port forward", "public access to localhost", "expose localhost".

### `design`

- **Path**: `skills/design`
- **SKILL.md**: [`skills/design/SKILL.md`](/skills/design/SKILL.md)
- **Title**: Design Skill（设计技能）
- **Files**: 543
- **Structure**: flat
- **Flags**: `UNKNOWN_KEYS`

> Route design-related HTML artifact tasks (landing pages, portfolios, prototypes, decks, content pages, web tools, social cards, info-interactive) to the right artifact skill, and decide whether to use design-system-reference, design-system-generation, or export. Use for any UI/visual/HTML design work.

### `e-commerce-nextjs16-monorepo`

- **Path**: `skills/e-commerce-nextjs16-monorepo`
- **SKILL.md**: [`skills/e-commerce-nextjs16-monorepo/SKILL.md`](/skills/e-commerce-nextjs16-monorepo/SKILL.md)
- **Title**: Scandi Haven — Master Engineering Skill
- **Files**: 1
- **Structure**: flat
- **Version**: 1.0.0
- **Flags**: `UNKNOWN_KEYS`, `BODY_LENGTH`

> Production-grade reference for building DTC e-commerce and storefront platforms on Next.js 16 + React 19 + Tailwind CSS v4 (CSS-first @theme) + Drizzle ORM + PostgreSQL 17 in a pnpm + Turborepo monorepo with TypeScript strict. Covers App Router RSC/Server Actions, proxy.ts, Better Auth with RBAC, Stripe SAQ-A payments and webhooks, Zod validation, Zustand client islands, shadcn/Radix UI, and end-to-end commerce engine (catalog, cart, pricing, promotions, inventory, orders, shipping, tax, search FTS, jobs). Includes reusable patterns for monorepo layering (transpilePackages), security hardening, WCAG AAA, editorial design tokens, and operational workflows. Applicable to any full-stack TypeScript e-commerce, marketplace, booking, or content-driven SaaS using this stack.

### `ecommerce-website-scaffold`

- **Path**: `skills/ecommerce-website-scaffold`
- **SKILL.md**: [`skills/ecommerce-website-scaffold/SKILL.md`](/skills/ecommerce-website-scaffold/SKILL.md)
- **Title**: ecommerce-website-scaffold
- **Files**: 1
- **Structure**: flat
- **License**: accompany with an explicit LICENSE when used as a template
- **Version**: 1.0.0
- **Flags**: `UNKNOWN_KEYS`, `BODY_LENGTH`

> Production-grade engineering skill for building, extending, rebranding, or auditing any e-commerce website codebase on the Next.js 16 App Router + React 19 + Prisma + Tailwind v4 stack. Covers the full commerce domain: catalog, cart, checkout, payments, orders, admin, auth, security, testing, and deployment. Every pattern below was distilled from three independently audited production-grade storefront codebases (860+ unit tests and 700+ e2e cases of combined verification culture).

### `emil-design-eng`

- **Path**: `skills/emil-design-eng`
- **SKILL.md**: [`skills/emil-design-eng/SKILL.md`](/skills/emil-design-eng/SKILL.md)
- **Title**: Design Engineering
- **Files**: 1
- **Structure**: flat
- **Flags**: `BODY_LENGTH`

> This skill encodes Emil Kowalski's philosophy on UI polish, component design, animation decisions, and the invisible details that make software feel great.

### `finance`

- **Path**: `skills/finance`
- **SKILL.md**: [`skills/finance/SKILL.md`](/skills/finance/SKILL.md)
- **Title**: Finance Skill
- **Files**: 2
- **Structure**: flat

> Comprehensive Finance API integration skill for real-time and historical financial data analysis, market research, and investment decision-making. Priority use cases: stock price queries, market data analysis, company financial information, portfolio tracking, market news retrieval, stock screening, technical analysis, and any financial market-related requests. This skill should be the primary choice for all Finance API interactions and financial data needs.

### `find-animation-opportunities`

- **Path**: `skills/find-animation-opportunities`
- **SKILL.md**: [`skills/find-animation-opportunities/SKILL.md`](/skills/find-animation-opportunities/SKILL.md)
- **Title**: Finding Animation Opportunities
- **Files**: 1
- **Structure**: flat

> Search a codebase or UI for places that don't animate but should, and reject everything that shouldn't. Read-only; it proposes motion with exact values, it does not implement it. Use when the user asks "what could be animated here?" or wants to "make this feel more alive". For fixing existing animations, use improve-animations or review-animations instead.

### `flutter`

- **Path**: `skills/flutter`
- **SKILL.md**: [`skills/flutter/SKILL.md`](/skills/flutter/SKILL.md)
- **Title**: Flutter — Cross-Platform UI Toolkit Workflow Skill
- **Files**: 1
- **Structure**: flat
- **License**: Proprietary. LICENSE.txt has complete terms
- **Flags**: `BODY_LENGTH`

> Flutter (Dart 3) cross-platform UI toolkit workflow skill — build iOS, Android, web, and desktop apps from a single codebase. Covers the widget-tree mental model (StatelessWidget vs StatefulWidget vs InheritedWidget), BuildContext and rebuilds, layout primitives (Row, Column, Stack, Container, Expanded/Flexible), the state management decision tree (setState → InheritedWidget → Provider → Riverpod → Bloc → GetX), Navigation 2.0 router vs Navigation 1.0, HTTP & JSON (http package + json_serializable codegen), forms and validation, the testing pyramid (widget, integration, golden tests), platform channels for native code, and the per-platform deployment flows (iOS via Xcode + App Store Connect, Android via Gradle + Play Store, web, desktop). Use when building any mobile, desktop, or web app with Flutter — especially when the task involves state management choice, navigation patterns, or platform-specific deployment where idiomatic Flutter differs from web framework patterns.

### `frontend-design`

- **Path**: `skills/frontend-design`
- **SKILL.md**: [`skills/frontend-design/SKILL.md`](/skills/frontend-design/SKILL.md)
- **Title**: Frontend Design System
- **Files**: 12
- **Structure**: references, scripts

> Design thinking and decision-making for web UI. Use when designing components, layouts, color schemes, typography, or creating aesthetic interfaces. Teaches principles, not fixed values.

### `frontend-development`

- **Path**: `skills/frontend-development`
- **SKILL.md**: [`skills/frontend-development/SKILL.md`](/skills/frontend-development/SKILL.md)
- **Title**: Frontend Development Guidelines
- **Files**: 11
- **Structure**: flat

> Frontend development guidelines for React/TypeScript applications. Modern patterns including Suspense, lazy loading, useSuspenseQuery, file organization with features directory, MUI v7 styling, TanStack Router, performance optimization, and TypeScript best practices. Use when creating components, pages, features, fetching data, styling, routing, or working with frontend code.

### `frontend-ui-engineering`

- **Path**: `skills/frontend-ui-engineering`
- **SKILL.md**: [`skills/frontend-ui-engineering/SKILL.md`](/skills/frontend-ui-engineering/SKILL.md)
- **Title**: Frontend UI Engineering
- **Files**: 1
- **Structure**: flat

> Builds production-quality UIs. Use when building or modifying user-facing interfaces. Use when creating components, implementing layouts, managing state, or when the output needs to look and feel production-quality rather than AI-generated.

### `frontend-ui-testing-journey`

- **Path**: `skills/frontend-ui-testing-journey`
- **SKILL.md**: [`skills/frontend-ui-testing-journey/SKILL.md`](/skills/frontend-ui-testing-journey/SKILL.md)
- **Title**: Frontend UI Testing Journey
- **Files**: 2
- **Structure**: references
- **Flags**: `UNKNOWN_KEYS`, `BODY_LENGTH`

> Complete frontend UI testing, verification, troubleshooting, and resolution journey. Covers testing methodology, browser automation with four tools (OpenClaw browser, agent-browser CLI, chrome-devtools-mcp, @playwright/mcp), common patterns, troubleshooting guides, and lessons learned from real-world testing.

### `fullstack-dev`

- **Path**: `skills/fullstack-dev`
- **SKILL.md**: [`skills/fullstack-dev/SKILL.md`](/skills/fullstack-dev/SKILL.md)
- **Title**: Fullstack Web Development Skill
- **Files**: 1
- **Structure**: flat
- **Flags**: `UNKNOWN_KEYS`

> Full-stack Next.js 16 + React 19 + TypeScript strict with Tailwind CSS v4, shadcn/ui, Prisma ORM. Covers App Router, Server Components, API routes, WebSocket/Socket.io, database schemas, full project scaffolding. Use when building web apps, creating UI components, setting up databases, or implementing full-stack TypeScript with Next.js and Prisma.

### `htmx`

- **Path**: `skills/htmx`
- **SKILL.md**: [`skills/htmx/SKILL.md`](/skills/htmx/SKILL.md)
- **Title**: HTMX 2 — Hypermedia-Driven Web Frontend
- **Files**: 1
- **Structure**: flat
- **License**: Proprietary. LICENSE.txt has complete terms
- **Flags**: `BODY_LENGTH`

> HTMX 2 (released 2024) hypermedia-driven web frontend workflow skill — HTML over the wire. Covers the core mental model (HTML attributes drive AJAX, WebSocket, SSE, and DOM updates — hx-get, hx-post, hx-swap, hx-target, hx-trigger, and friends), the swap modes (innerHTML, outerHTML, before/after variants, none — plus hx-swap-oob out-of-band updates), triggers (standard + custom events, polling, and timing modifiers), the extensions ecosystem (json-enc, multi-swap, response-targets, idiomorph), and the backend-agnostic design (any backend that returns HTML fragments). Use when building any server-rendered web app where React/Vue/Svelte would be overkill — CRUD apps, admin panels, content sites, dashboards — especially when the task involves hx-swap selection, hx-trigger composition, partial template rendering on the backend, or deciding between HTMX and a SPA framework where idiomatic HTMX (hypermedia over the wire) differs fundamentally from React/Vue (JSON API + client-side rendering).

### `image-search`

- **Path**: `skills/image-search`
- **SKILL.md**: [`skills/image-search/SKILL.md`](/skills/image-search/SKILL.md)
- **Title**: image-search (ZAI in-house, via z-ai SDK)
- **Files**: 1
- **Structure**: flat
- **Version**: 1.0.0
- **Flags**: `UNKNOWN_KEYS`

> ZAI in-house image search service, exposed through the z-ai-web-dev-sdk CLI. Retrieve real images from the web for any text query, with optional short captions, and get back OSS-hosted direct URLs that are guaranteed reachable. Use when the user wants to find, fetch, illustrate, or embed images — e.g. "search for images of X", "find a picture of Y", "I need cover art for Z", "give me reference photos of W", "插图", "配图", "找图", "找张图", "搜张图", "搜图".

### `laravel-12`

- **Path**: `skills/laravel-12`
- **SKILL.md**: [`skills/laravel-12/SKILL.md`](/skills/laravel-12/SKILL.md)
- **Title**: Laravel 12 — Full-Stack PHP Workflow Skill
- **Files**: 1
- **Structure**: flat
- **License**: Proprietary. LICENSE.txt has complete terms
- **Flags**: `BODY_LENGTH`

> Laravel 12 (PHP 8.3+) full-stack workflow skill. Covers the streamlined 11+/12 app structure (no Kernel.php, bootstrap/app.php config), Eloquent ORM with factories/seeders, Artisan CLI, Blade + Livewire + Inertia frontend options, Sanctum API tokens, Breeze/Jetstream auth scaffolding, Queues with Redis/database, Pest testing, Vite asset build, Filament admin, Forge/Vapor deployment. Use when building any PHP web application, API, or console workload on Laravel 12 — especially when the task involves migrations, Eloquent queries, queued jobs, or auth flows where idiomatic Laravel differs from generic PHP patterns.

### `mobile-native`

- **Path**: `skills/mobile-native`
- **SKILL.md**: [`skills/mobile-native/SKILL.md`](/skills/mobile-native/SKILL.md)
- **Title**: Feeling Native On Mobile
- **Files**: 1
- **Structure**: flat

> Make a web app feel native on a phone — the small CSS and meta-tag fixes that separate "a website in a browser" from something that feels installed. Covers sticky hover states, tap highlight flashes, the 100vh bug, inputs that zoom the page, laggy taps, pull-to-refresh hijacking scroll, content under the notch, long-press selecting button text, carousels that scroll the wrong way, mismatched status bars, and the rule that you test on real hardware. Use when a web app is being built for or reviewed on mobile, when something "works in Chrome but feels wrong on my phone", when building a PWA, a bottom sheet, a carousel, a full-screen layout, or any touch interaction. For motion itself use animate; for React Native use animate-expo.

### `nextjs-postgresql-single-app`

- **Path**: `skills/nextjs-postgresql-single-app`
- **SKILL.md**: [`skills/nextjs-postgresql-single-app/SKILL.md`](/skills/nextjs-postgresql-single-app/SKILL.md)
- **Title**: home-financing (ModFii) — Production Web App Skill
- **Files**: 1
- **Structure**: flat
- **Version**: 1.8.0
- **Flags**: `UNKNOWN_KEYS`, `BODY_LENGTH`

> Production-grade reference for building content-driven marketing sites and transactional funnel apps on Next.js 16 + React 19 + Tailwind CSS v4 (CSS-first @theme) + Drizzle ORM + PostgreSQL 17 in a single-app (npm, no monorepo) with TypeScript strict. Covers App Router RSC (force-dynamic), file corpus → catalog → idempotent ensureSeeded() projection → Pool singleton (globalThis), Drizzle pgTable migrations, 43 static/dynamic pages, lead-capture funnel (validate → match → persist), rate limiting, health/sitemap/redirects, editorial design tokens, and WCAG AAA. Includes reusable patterns for single-Pool persistence, file-backed seeding, content ingestion, and pre-ship gates (lint/typecheck/test/build/e2e). Applicable to any full-stack TypeScript marketing, funnel, lead-gen, or content-driven SaaS using this stack.

### `nextjs-react-expert`

- **Path**: `skills/nextjs-react-expert`
- **SKILL.md**: [`skills/nextjs-react-expert/SKILL.md`](/skills/nextjs-react-expert/SKILL.md)
- **Title**: Next.js & React Performance Expert
- **Files**: 11
- **Structure**: scripts

> React 19 and Next.js 16 performance optimization from Vercel Engineering. 57 rules prioritized by impact - eliminate waterfalls, reduce bundle size, server/client-side optimizations. Covers App Router, Server Components, RSC streaming, Turbopack, React Compiler, Core Web Vitals (LCP/INP/CLS), bundle analysis. Use when profiling, reviewing code for perf issues, or optimizing production React/Next.js apps.

### `nextjs-typescript-patterns`

- **Path**: `skills/nextjs-typescript-patterns`
- **SKILL.md**: [`skills/nextjs-typescript-patterns/SKILL.md`](/skills/nextjs-typescript-patterns/SKILL.md)
- **Title**: Consolidated Agent Briefing Document and Programming Handbook
- **Files**: 4
- **Structure**: flat
- **Version**: 1.6
- **Flags**: `UNKNOWN_KEYS`, `BODY_LENGTH`

> Monorepo web projects using pnpm, Turborepo, TypeScript, Next.js, React, ESLint, Prettier, Drizzle ORM, Postgres, and third-party SDKs (tRPC, Trigger.dev, Stripe, Better Auth, Sanity, React Email, Vitest)

### `nextjs16-full-stack`

- **Path**: `skills/nextjs16-full-stack`
- **SKILL.md**: [`skills/nextjs16-full-stack/SKILL.md`](/skills/nextjs16-full-stack/SKILL.md)
- **Title**: Skills Knowledge Base — IRONFORGE Fitness Studio
- **Files**: 1
- **Structure**: flat
- **Version**: 1.0
- **Flags**: `UNKNOWN_KEYS`, `BODY_LENGTH`

> IRONFORGE Fitness Studio — Brutalist/Raw + Retro-Futuristic Design System & Next.js 16 Full-Stack Engineering Reference Production-grade skill for building IRONFORGE Fitness Studio from any AI agent. Covers - Avant-garde brutalist/raw design system with neon orange (#FF5400) on pure black (#0a0a0a) - Tailwind CSS v4 CSS-first @theme block, custom utilities, and v3→v4 migration rules - Anti-generic UI, typography scale (Bebas Neue / Oswald / Archivo / JetBrains Mono), and motion standards - Next.js 16 + React 19 App Router, Server Components, and 5-layer architecture (proxy → app → features → domain → lib) - Auth.js v5 + Drizzle ORM authentication, SSE streaming, and env validation - shadcn/ui + Radix patterns and CVA component variants - Accessibility (WCAG AAA) and performance budgets - Vitest, Playwright, and brand-token testing This skill ensures any coding agent can match to the IRONFORGE fitness-studio project and implement aligned with the master execution plan.

### `nextjs16-react19-next-auth5-drizzle-orm`

- **Path**: `skills/nextjs16-react19-next-auth5-drizzle-orm`
- **SKILL.md**: [`skills/nextjs16-react19-next-auth5-drizzle-orm/SKILL.md`](/skills/nextjs16-react19-next-auth5-drizzle-orm/SKILL.md)
- **Title**: StoryIntoVideo — Engineering Skill Reference
- **Files**: 1
- **Structure**: flat
- **Version**: 3.0.0
- **Flags**: `UNKNOWN_KEYS`, `BODY_LENGTH`

> Full-stack Next.js 16 SaaS with React 19, Tailwind v4 CSS-first @theme, Auth.js v5, Drizzle ORM/Postgres (Neon), Inngest job queue, OpenAI + Replicate + ElevenLabs AI pipeline, Stripe billing, Cloudflare R2 storage, SSE streaming. 5-layer architecture (proxy → app → features → domain → lib), App Router Server Components, TypeScript strict, pnpm, Vitest + Playwright E2E, GitHub Actions CI. Luxury-dark cinematic design system with 13 CSS keyframes, WCAG AAA accessibility, server-side URL signing, env-configurable fail-open moderation. Production engineering reference with anti-patterns, debugging guides, and lessons from 4+ sprints.

### `nextjs16-react19-postgres17`

- **Path**: `skills/nextjs16-react19-postgres17`
- **SKILL.md**: [`skills/nextjs16-react19-postgres17/SKILL.md`](/skills/nextjs16-react19-postgres17/SKILL.md)
- **Title**: OneStopNews — Engineering Skill Reference
- **Files**: 1
- **Structure**: flat
- **Version**: 3.0.0
- **Flags**: `UNKNOWN_KEYS`, `BODY_LENGTH`

> Full-stack Next.js 16 + React 19 + PostgreSQL 17 reference app with Drizzle ORM, BullMQ job queues (Redis), Auth.js v5, Vercel AI SDK (Anthropic + OpenAI), RSS/Atom ingestion, web push notifications. 5-layer architecture (proxy → app → features → domain → lib), App Router Server Components, async params, Suspense boundaries, PPR/cacheComponents, TypeScript strict + erasableSyntaxOnly, pnpm, Zod validation, Vitest + Playwright E2E + testcontainers. Editorial design system with CSS Subgrid, WCAG AAA accessibility, 3-layer AI provenance (JSON-LD + HTTP header + meta tag), Docker standalone output. Use for production full-stack SaaS with auth, job queues, AI pipelines, RSS/content ingestion, web push, admin panels, and database patterns."

### `nextjs16-react19-tailwind4-auth5-video-gen`

- **Path**: `skills/nextjs16-react19-tailwind4-auth5-video-gen`
- **SKILL.md**: [`skills/nextjs16-react19-tailwind4-auth5-video-gen/SKILL.md`](/skills/nextjs16-react19-tailwind4-auth5-video-gen/SKILL.md)
- **Title**: StoryIntoVideo — Complete Project Skill
- **Files**: 2
- **Structure**: flat
- **Version**: 9.0
- **Flags**: `UNKNOWN_KEYS`, `BODY_LENGTH`

> Production-grade Next.js 16 + React 19 + Tailwind CSS v4 full-stack SaaS. Covers App Router Server Components, TypeScript strict, CSS-first @theme design system, Drizzle ORM + PostgreSQL, Auth.js v5 authentication, job queue orchestration (Inngest/BullMQ), AI pipeline integration (OpenAI, Replicate, ElevenLabs), credit-based Stripe billing, Cloudflare R2 storage, SSE streaming, idempotent transactions, WCAG AAA accessibility, OWASP 2025 security hardening, Docker deployment, Vitest + Playwright testing, CI/CD, and live-site validation. Comprehensive engineering reference with audit history, ADRs, 60+ lessons learned, z-index maps, color tokens, and debugging guides for AI media generation, content platforms, or any full-stack Next.js SaaS.

### `nextjs16-react19-tailwind4-better-auth-monorepo`

- **Path**: `skills/nextjs16-react19-tailwind4-better-auth-monorepo`
- **SKILL.md**: [`skills/nextjs16-react19-tailwind4-better-auth-monorepo/SKILL.md`](/skills/nextjs16-react19-tailwind4-better-auth-monorepo/SKILL.md)
- **Title**: Stillwater — Project Skill File
- **Files**: 1
- **Structure**: flat
- **Version**: 1.0.0
- **Flags**: `UNKNOWN_KEYS`, `BODY_LENGTH`

> Turborepo monorepo, Next.js 16.2, React 19, Tailwind v4.3, tRPC v11, Drizzle ORM 0.45, Better Auth 1.6.23, Stripe 22.3 (Dahlia), Trigger.dev v4, React Email 6.6, Resend, Sanity CMS v6. 651 tests, 11 ADRs, 93 lessons learned across 13 build phases.

### `nextjs16-react19-tailwind4-drizzle-orm-postgres17-rsc`

- **Path**: `skills/nextjs16-react19-tailwind4-drizzle-orm-postgres17-rsc`
- **SKILL.md**: [`skills/nextjs16-react19-tailwind4-drizzle-orm-postgres17-rsc/SKILL.md`](/skills/nextjs16-react19-tailwind4-drizzle-orm-postgres17-rsc/SKILL.md)
- **Title**: Nave & Spire — SKILL.md
- **Files**: 1
- **Structure**: flat
- **Version**: 1.2.0
- **Flags**: `UNKNOWN_KEYS`, `BODY_LENGTH`

> Production-grade Next.js 16 + React 19 + Tailwind CSS v4 + Drizzle ORM + PostgreSQL 17 reference with App Router RSC (force-dynamic) — 3-layer architecture (App/RSC pages + Client islands + Domain/DB). Covers CSS-first @theme design system, editorial motion + a11y floor, file-backed typed seeds → idempotent ensureSeeded() → Drizzle pgTable (6-table pattern, Pool globalThis singleton, parallel queries + in-memory joins), manual validation, per-IP rate limiting, security headers/CSP, and hybrid CI + Vitest + live-DB verification. Use when building any content-driven, editorial, audit-journal, or data-projection app on Next.js 16 with Postgres/Drizzle, needing RSC production patterns, DB seeding lifecycle, or Tailwind v4/CSS-first hardening beyond a minimal starter.

### `nextjs16-react19-tailwind4-full-stack`

- **Path**: `skills/nextjs16-react19-tailwind4-full-stack`
- **SKILL.md**: [`skills/nextjs16-react19-tailwind4-full-stack/SKILL.md`](/skills/nextjs16-react19-tailwind4-full-stack/SKILL.md)
- **Title**: IRONFORGE — Project SKILL.md
- **Files**: 1
- **Structure**: flat
- **Version**: 1.1.2
- **Flags**: `UNKNOWN_KEYS`, `BODY_LENGTH`

> Production-grade Next.js 16 full-stack marketing website building with React 19, TypeScript strict, and Tailwind CSS v4 CSS-first @theme design system. Covers App Router Server Components, the 5-layer golden rule architecture (proxy → app → features → domain → lib), graceful degradation for infrastructure clients, Drizzle ORM with PostgreSQL and static fallback data, Auth.js v5 JWT authentication, Inngest step functions, Stripe Checkout payments, Replicate SDXL AI asset generation, Cloudflare R2 storage, Upstash rate limiting, and Zod 4 validation. Includes CSS-only animations, anti-generic brutalist dark-mode aesthetics, cinematic UI design, WCAG AAA accessibility, OWASP security hardening, Vitest + Playwright testing, and pnpm workspace configuration. Use for luxury marketing sites, membership platforms, booking systems, admin dashboards, e-commerce, fitness studio websites, SaaS applications, or any Next.js 16 production-grade full-stack project.

### `nextjs16-react19-tailwindv4-trpcv11-drizzle-better-auth`

- **Path**: `skills/nextjs16-react19-tailwindv4-trpcv11-drizzle-better-auth`
- **SKILL.md**: [`skills/nextjs16-react19-tailwindv4-trpcv11-drizzle-better-auth/SKILL.md`](/skills/nextjs16-react19-tailwindv4-trpcv11-drizzle-better-auth/SKILL.md)
- **Title**: Stillwater — Project Skill File
- **Files**: 1
- **Structure**: flat
- **Version**: 1.4.0
- **Flags**: `UNKNOWN_KEYS`, `BODY_LENGTH`

> Production-grade reference for Next.js 16 + React 19 + Tailwind CSS v4 + tRPC v11 + Drizzle ORM + Better Auth in a Turborepo monorepo. Covers App Router Server Components, proxy.ts (replaces middleware.ts), RSC streaming, CSS-first @theme design tokens, 5-layer architecture, and async params. Includes 50+ documented anti-patterns and gotchas across Next.js 16 breaking changes, React 19 API shifts, Tailwind v4 migration, Better Auth vs Auth.js v5, Drizzle ORM pitfalls, Stripe webhook idempotency, and Vitest mocking. Features production patterns for advisory-lock booking concurrency, SSE streaming, idempotent webhooks, fail-open rate limiting, env module build-context fallback, and server-side URL signing. Documents WCAG AAA accessibility, OWASP 2025 hardening, TDD regression verification cycle, implementation lessons learned, and TypeScript interface reference. Applicable to any full-stack Next.js 16 SaaS with authentication, payments, background jobs, CMS integration, and PostgreSQL.

### `nextjs16-tailwind4`

- **Path**: `skills/nextjs16-tailwind4`
- **SKILL.md**: [`skills/nextjs16-tailwind4/SKILL.md`](/skills/nextjs16-tailwind4/SKILL.md)
- **Title**: Next.js + Tailwind CSS v4 Luxury Web Development
- **Files**: 1
- **Structure**: flat
- **Flags**: `BODY_LENGTH`

> Luxury-grade Next.js 16 + React 19 + TypeScript strict with Tailwind CSS v4 CSS-first @theme, Radix UI (shadcn), and Framer Motion. Covers App Router, Server Components, avant-garde anti-generic UI design, OWASP 2025 security audits, Core Web Vitals performance optimization, WCAG AAA accessibility, mobile navigation debugging, and code review for high-end production web experiences.

### `personal-portfolio`

- **Path**: `skills/personal-portfolio`
- **SKILL.md**: [`skills/personal-portfolio/SKILL.md`](/skills/personal-portfolio/SKILL.md)
- **Title**: The Engineered Soul — Portfolio Master Skill (v3.0.0)
- **Files**: 1
- **Structure**: flat
- **License**: MIT
- **Version**: 3.0.0
- **Flags**: `UNKNOWN_KEYS`

> Tactile Brutalist + High-End Editorial personal portfolio SPA with React 19, TypeScript 6 strict, Vite 6, Tailwind CSS v4 CSS-first @theme, pnpm. Covers complete lifecycle from scaffold to shipping: kinetic typography, hash-based routing, import.meta.glob content ingestion, dual-theme (night/day) design system, WCAG AAA accessibility, component-driven digital installation. Use when building a distinctive, anti-generic portfolio or personal site with React + Vite + Tailwind v4.

### `pick-ui-library`

- **Path**: `skills/pick-ui-library`
- **SKILL.md**: [`skills/pick-ui-library/SKILL.md`](/skills/pick-ui-library/SKILL.md)
- **Title**: Picking The Right Library
- **Files**: 1
- **Structure**: flat
- **Flags**: `UNKNOWN_KEYS`

> Pick the right library for a given frontend task from a curated, opinionated list — numbers, OTP inputs, charts, command menus, virtualization, drag and drop, toasts, state, styling, and more. Only runs when explicitly invoked; it does not trigger on its own.

### `pptx-unified`

- **Path**: `skills/pptx-unified`
- **SKILL.md**: [`skills/pptx-unified/SKILL.md`](/skills/pptx-unified/SKILL.md)
- **Title**: pptx-unified — A Practical Recipe for Impressive .pptx Decks
- **Files**: 13
- **Structure**: references, scripts
- **License**: MIT
- **Author**: Claw Code (distilled from real build experience)
- **Version**: 1.0.0
- **Flags**: `METADATA_NON_STRING`

> Unified practical recipe for generating impressive marketing-grade .pptx presentations from scratch. Combines the canonical pptx skill's HTML-first 4-stage pipeline (Clarify → Research → Plan → Build → Export) with the variant skills' distinctive strengths (cyber-ppt's confirmation gates, pptx-generator's PptxGenJS templates, codex-ppt's image-based fallback) and 20+ real-world lessons/anti-patterns distilled from building a 12-slide deck for the my-pi-agent repo. Use this skill when ANY coding agent needs to produce a polished .pptx — it is the single starting point that routes to the right variant only when a specific capability is needed. Triggers: "make a presentation", "generate a .pptx", "build a slide deck", "marketing deck", "pitch slides", "create slides for this repo/product".

### `prototype`

- **Path**: `skills/prototype`
- **SKILL.md**: [`skills/prototype/SKILL.md`](/skills/prototype/SKILL.md)
- **Title**: Prototype
- **Files**: 4
- **Structure**: flat

> Build a throwaway prototype to answer a design question. Use when the user wants to sanity-check whether a state model or logic feels right, or explore what a UI should look like.

### `react-native-expo`

- **Path**: `skills/react-native-expo`
- **SKILL.md**: [`skills/react-native-expo/SKILL.md`](/skills/react-native-expo/SKILL.md)
- **Title**: React Native + Expo — Cross-Platform Mobile Workflow Skill
- **Files**: 1
- **Structure**: flat
- **License**: Proprietary. LICENSE.txt has complete terms
- **Flags**: `BODY_LENGTH`

> React Native (0.76+ with New Architecture: Fabric + TurboModules) + Expo (SDK 52+ with Expo Router v4) cross-platform mobile app workflow skill. Covers the New Architecture (Fabric renderer, TurboModules), Expo Application Services (EAS Build, EAS Submit, EAS Update), Expo Router v4 (file-based routing for native apps), the React mental model in native context (View/Text/Pressable/FlatList vs DOM elements; Zustand, TanStack Query, Context for state), navigation choices (Expo Router vs React Navigation), native module access via expo-* packages (camera, location, notifications, storage), testing (Jest + RNTL, Maestro or Detox for E2E), and the deployment story (EAS Build + Submit, EAS Update hotfixes). Use when building any iOS/Android/mobile web app with React Native + Expo — especially when the task involves New Architecture migration, Expo Router conventions, EAS setup, native module permissions, or OTA update strategy where idiomatic React Native differs from web React or from Flutter.

### `react19-ts6-vite8-tailwindv4-mvp`

- **Path**: `skills/react19-ts6-vite8-tailwindv4-mvp`
- **SKILL.md**: [`skills/react19-ts6-vite8-tailwindv4-mvp/SKILL.md`](/skills/react19-ts6-vite8-tailwindv4-mvp/SKILL.md)
- **Title**: React 19 + TypeScript 6 + Vite 8 MVP — Production-Ready Web App Skill
- **Files**: 7
- **Structure**: flat
- **License**: MIT
- **Version**: 3.0.0
- **Flags**: `UNKNOWN_KEYS`, `BODY_LENGTH`

> MVP/production React 19 + TypeScript 6 strict + Vite 8 (Rolldown) + Tailwind CSS v4 CSS-first @theme. File-based routing, pnpm, Vitest + Playwright E2E. Covers complete lifecycle from scaffold to shipping tested, type-safe, WCAG AAA, production-grade code. Use when building new greenfield web apps with modern React + Vite + Tailwind v4.

### `replicate-web-app`

- **Path**: `skills/replicate-web-app`
- **SKILL.md**: [`skills/replicate-web-app/SKILL.md`](/skills/replicate-web-app/SKILL.md)
- **Title**: Authorized Web Application Investigation and Reconstruction
- **Files**: 5
- **Structure**: flat
- **License**: MIT
- **Version**: 5.1.0
- **Flags**: `BODY_LENGTH`

> Investigate an authorized web application (clone, copy, migrate, replicate, rebuild, make a copy of; supports no-code platforms like Base44, Lovable, Bolt, Replit) using REA and browser evidence, then build and verify a production-quality, behaviorally similar web application in the current codebase. Use when asked to clone, replicate, migrate, or rebuild a web app.

### `sanity-best-practices`

- **Path**: `skills/sanity-best-practices`
- **SKILL.md**: [`skills/sanity-best-practices/SKILL.md`](/skills/sanity-best-practices/SKILL.md)
- **Title**: Sanity Best Practices
- **Files**: 25
- **Structure**: references

> Sanity development best practices for schema design, GROQ queries, TypeGen, Visual Editing, images, Portable Text, Studio structure, localization, migrations, Sanity Functions, Blueprints, and framework integrations such as Next.js, Nuxt, Astro, Remix, SvelteKit, Angular, Hydrogen, and the App SDK. Use this skill whenever working with Sanity schemas, defineType or defineField, GROQ or defineQuery, content modeling, Presentation or preview setups, Sanity-powered frontend integrations, Sanity Functions, documentEventHandler, defineDocumentFunction, defineMediaLibraryAssetFunction, @sanity/functions, @sanity/blueprints, sanity.blueprint.ts, event-driven content automation, or when reviewing and fixing a Sanity codebase.

### `sanity-io-deploy`

- **Path**: `skills/sanity-io-deploy`
- **SKILL.md**: [`skills/sanity-io-deploy/SKILL.md`](/skills/sanity-io-deploy/SKILL.md)
- **Title**: Sanity Studio: Setup, Configuration, Deployment & Verification (expanded, field-tested)
- **Files**: 1
- **Structure**: flat

> Sanity CMS + Next.js integration — end-to-end setup, deployment, and verification for a standalone Sanity Studio (sibling folder, never embedded) wired to an existing Next.js App Router app. Handles Sanity project auth and provider selection, schema validation and dangling-reference fixes, sanity schema deploy vs sanity deploy (Schema/Content Lake vs Studio UI at *.sanity.studio), viewer token and webhook secret minting, env wiring (NEXT_PUBLIC_SANITY_*), CORS origins, ISR webhook for revalidation, and live verification via Content Lake GROQ query + fresh headless-browser check. Use when connecting Sanity to Next.js, setting up/installing/configuring Sanity Studio, deploying Sanity schema or Studio, or working with sanity login/projects/datasets/tokens/cors/hooks, Sanity Content Lake API, GROQ, Sanity Cloud hosting, headless CMS, sanity.studio URL, or Sanity onboarding docs. Companion to sanity-best-practices; field-tested with production gotchas and fixes.

### `sanity-migration`

- **Path**: `skills/sanity-migration`
- **SKILL.md**: [`skills/sanity-migration/SKILL.md`](/skills/sanity-migration/SKILL.md)
- **Title**: Sanity Migration
- **Files**: 10
- **Structure**: references

> Plans, implements, and reviews migrations from other CMSes and content systems into Sanity. Use when migrating or replatforming to Sanity from AEM, Adobe Experience Manager, Contentful, Strapi, Webflow, WordPress, Payload, Drupal, Markdown/MDX/frontmatter files, WXR/XML exports, CMS APIs, database dumps, static HTML, or when designing extraction, transformation, Portable Text conversion, asset migration, redirects, validation, and cutover workflows.

### `scaffold-ui`

- **Path**: `skills/scaffold-ui`
- **SKILL.md**: [`skills/scaffold-ui/SKILL.md`](/skills/scaffold-ui/SKILL.md)
- **Title**: scaffold-ui
- **Files**: 1
- **Structure**: flat

> Generates an anti-generic React component with brutalist styling and strict DOM hygiene.

### `solidstart`

- **Path**: `skills/solidstart`
- **SKILL.md**: [`skills/solidstart/SKILL.md`](/skills/solidstart/SKILL.md)
- **Title**: SolidStart 1 (SolidJS) — Signals-Based Full-Stack TypeScript
- **Files**: 1
- **Structure**: flat
- **License**: Proprietary. LICENSE.txt has complete terms
- **Flags**: `BODY_LENGTH`

> SolidStart 1 (SolidJS 1.9+, released 2024) full-stack TypeScript framework workflow skill — signals-based reactivity without a virtual DOM. Covers the fine-grained reactivity mental model (createSignal's getter tracks dependencies; its setter triggers only the effects that read it — no re-renders, no virtual DOM), the SolidJS primitives (createSignal, createMemo, createEffect, createResource, createStore), JSX compiled to direct DOM operations, conventions (file-based routing, server functions 'use server', load functions), Vinxi (Vite-based) build tool, and the React comparison (same JSX, different execution model). Use when building any full-stack TypeScript web app where React's re-render model is a performance bottleneck — especially when the task involves signal/effect patterns, server functions ('use server'), file-based routing, or migrating from React where idiomatic Solid (fine-grained signals, no virtual DOM) differs fundamentally from React (re-renders, virtual DOM, hooks rules).

### `static-spa-parish-site`

- **Path**: `skills/static-spa-parish-site`
- **SKILL.md**: [`skills/static-spa-parish-site/SKILL.md`](/skills/static-spa-parish-site/SKILL.md)
- **Title**: Parish Site Engineering Skill — Unified v3 (Church of the Risen Christ, Toa Payoh — canonical instance)
- **Files**: 15
- **Structure**: flat
- **Version**: 3.0.0
- **Flags**: `UNKNOWN_KEYS`, `BODY_LENGTH`

> Complete engineering reference for static SPA parish/church/nonprofit/community brochure sites — React 19 + Vite 7 + Tailwind CSS v4 CSS-first @theme + TypeScript + HashRouter + vite-plugin-singlefile (single dist/index.html for GH Pages/S3, no SSR/CMS). Covers design system, component architecture, file-backed typed content, routing alias/anchor contracts, WCAG AAA, and pre-ship gates. Use when building, extending, debugging, onboarding, cloning, replicating, re-porting this parish-site family or scaffolding any static content-driven marketing/brochure/landing site template.

### `super-frontend-design`

- **Path**: `skills/super-frontend-design`
- **SKILL.md**: [`skills/super-frontend-design/SKILL.md`](/skills/super-frontend-design/SKILL.md)
- **Title**: Super Frontend Design (Master Skill)
- **Files**: 18
- **Structure**: assets, references, scripts
- **License**: MIT
- **Version**: 1.0.0
- **Flags**: `UNKNOWN_KEYS`

> Master frontend UI/UX design and development skill combining the top 10 validated skills. Covers anti-generic strategy, Next.js 16 + React 19 + Tailwind v4 CSS-first @theme tech stack, design systems, component architecture, App Router Server Components, Vercel-grade performance, WCAG AAA accessibility, visual storytelling, and end-to-end quality assurance for production-grade web experiences.

### `svelte-5-sveltekit`

- **Path**: `skills/svelte-5-sveltekit`
- **SKILL.md**: [`skills/svelte-5-sveltekit/SKILL.md`](/skills/svelte-5-sveltekit/SKILL.md)
- **Title**: Svelte 5 + SvelteKit 2 — Full-Stack TypeScript Workflow Skill
- **Files**: 1
- **Structure**: flat
- **License**: Proprietary. LICENSE.txt has complete terms
- **Flags**: `BODY_LENGTH`

> Svelte 5 + SvelteKit 2 full-stack TypeScript workflow skill. Covers the runes reactivity model ($state, $derived, $effect, $props, $bindable) which is fundamentally different from React hooks, file-based routing with +page.svelte / +layout.svelte / +page.server.ts / +page.ts, form actions as the idiomatic mutation pattern (progressive enhancement), load functions (server vs universal), hooks.server.ts for request-level interception, $env modules for typed environment variables (static vs dynamic, private vs public), adapters for deployment targets (auto / node / static / cloudflare / vercel). Use when building any web app on Svelte 5 or SvelteKit 2 — especially when the task involves migrating Svelte 4 store-based code to runes, choosing between server load and universal load, or wiring form actions with validation.

### `tailwind-patterns`

- **Path**: `skills/tailwind-patterns`
- **SKILL.md**: [`skills/tailwind-patterns/SKILL.md`](/skills/tailwind-patterns/SKILL.md)
- **Title**: Tailwind CSS Patterns (v4 - 2025)
- **Files**: 1
- **Structure**: flat

> Tailwind CSS v4 principles. CSS-first configuration, container queries, modern patterns, design token architecture.

### `tauri-2`

- **Path**: `skills/tauri-2`
- **SKILL.md**: [`skills/tauri-2/SKILL.md`](/skills/tauri-2/SKILL.md)
- **Title**: Tauri 2 — Cross-Platform Desktop & Mobile App Framework
- **Files**: 1
- **Structure**: flat
- **License**: Proprietary. LICENSE.txt has complete terms
- **Flags**: `BODY_LENGTH`

> Tauri 2 (Rust backend + system webview frontend, released October 2024) cross-platform desktop and mobile app workflow skill — the Electron alternative. Covers the architecture (Rust core + system webview — NOT bundled Chromium, so binaries are 3-10 MB vs Electron's 80-150 MB), the IPC model (#[tauri::command] functions invoked via invoke(), serde-serialized), the plugin system (filesystem, dialog, notification, http, shell, updater, tray; mobile: camera, biometrics), frontend-agnostic design (any web framework), mobile support (iOS + Android, same Rust core), capability-based permissions, the build pipeline (cargo + frontend build → platform bundles), and the signature-verified auto-updater. Use when building any desktop or mobile app with a web frontend — especially when the task involves Tauri commands, plugin configuration, mobile migration, the permission system, or comparing Tauri vs Electron where idiomatic Tauri (Rust + system webview) differs fundamentally from Electron (bundled Chromium).

### `tools-cli`

- **Path**: `skills/tools-cli`
- **SKILL.md**: [`skills/tools-cli/SKILL.md`](/skills/tools-cli/SKILL.md)
- **Title**: Tools CLI - Standalone file operation wrapper
- **Files**: 2
- **Structure**: flat

> Standalone CLI wrapper exposing Claude Code's core file operations (read, glob, grep, edit, write) as command-line utilities. Use for scripting and automation without requiring a full Claude session.

### `ui-styling`

- **Path**: `skills/ui-styling`
- **SKILL.md**: [`skills/ui-styling/SKILL.md`](/skills/ui-styling/SKILL.md)
- **Title**: UI Styling Skill
- **Files**: 97
- **Structure**: references, scripts
- **License**: MIT
- **Version**: 1.0.0
- **Flags**: `UNKNOWN_KEYS`

> Create beautiful, accessible user interfaces with shadcn/ui components (built on Radix UI + Tailwind), Tailwind CSS utility-first styling, and canvas-based visual designs. Use when building user interfaces, implementing design systems, creating responsive layouts, adding accessible components (dialogs, dropdowns, forms, tables), customizing themes and colors, implementing dark mode, generating visual designs and posters, or establishing consistent styling patterns across applications.

### `ui-ux-pro-max`

- **Path**: `skills/ui-ux-pro-max`
- **SKILL.md**: [`skills/ui-ux-pro-max/SKILL.md`](/skills/ui-ux-pro-max/SKILL.md)
- **Title**: ui-ux-pro-max
- **Files**: 55
- **Structure**: assets, references, scripts

> UI/UX design intelligence and implementation guidance for building polished interfaces. Use when the user asks for UI design, UX flows, information architecture, visual style direction, design systems/tokens, component specs, copy/microcopy, accessibility, or to generate/critique/refine frontend UI (HTML/CSS/JS, React, Next.js, Vue, Svelte, Tailwind). Includes workflows for (1) generating new UI layouts and styling, (2) improving existing UI/UX, (3) producing design-system tokens and component guidelines, and (4) turning UX recommendations into concrete code changes.

### `version-management`

- **Path**: `skills/version-management`
- **SKILL.md**: [`skills/version-management/SKILL.md`](/skills/version-management/SKILL.md)
- **Title**: 版本管理
- **Files**: 1
- **Structure**: flat
- **Flags**: `BODY_LENGTH`

> 独立通用 Skill：管理前端项目全生命周期。只要任务**可能**写出 .html/.jsx/.tsx/.vue 入口文件，就必须在写出第一个文件**之前**读取并遵循本 Skill（用于确定落盘路径与项目目录），而不是产出之后才补救；即使用户没有提到"项目"或"版本"也要使用。同时响应用户的版本相关操作（查看历史、恢复版本、切换项目等）。

### `web-app-foundation`

- **Path**: `skills/web-app-foundation`
- **SKILL.md**: [`skills/web-app-foundation/SKILL.md`](/skills/web-app-foundation/SKILL.md)
- **Title**: Web App Foundation — Master Engineering Skill
- **Files**: 5
- **Structure**: flat
- **Version**: 1.1.0
- **Flags**: `UNKNOWN_KEYS`, `BODY_LENGTH`

> Master engineering skill for scaffolding, extending, or remediating ANY production web application with authentication, a dashboard, and charting on Next.js 16 App Router + React 19 + TypeScript strict + Tailwind CSS v4 (CSS-first) + Prisma + SQLite/PostgreSQL + Zustand + recharts. Distilled and generalized from four sibling production codebases (digma, neo-crm, project-management, zero-balance — 1,508 commits of build/remediation history, re-validated 2026-10-25). Covers the full stack: env contract, db-path seam, scrypt+HMAC auth with verification/reset/revocation, zod-validated API envelope, per-user tenancy, KPI dashboard shell, 7-family chart layer, race-guarded store, degrade-never-fail AI, three-tier testing, quality gates, and the documentation contract. Use whenever creating a new web app codebase, adding auth/dashboard/charts to an existing one, or auditing one built from this skill.

### `web-application`

- **Path**: `skills/web-application`
- **SKILL.md**: [`skills/web-application/SKILL.md`](/skills/web-application/SKILL.md)
- **Title**: Web Application — Complete Engineering Skill (Generalized)
- **Files**: 2
- **Structure**: flat
- **Version**: 1.2.0
- **Flags**: `UNKNOWN_KEYS`, `BODY_LENGTH`

> Complete, generalized engineering skill for building any web application codebase: Next.js 16 App Router + React 19 + TypeScript (strict) + Tailwind CSS 4 (CSS-first) + shadcn/Radix + one Zustand store + Prisma/SQLite-dev (PostgreSQL-prod) + Zod-validated API + scrypt/HMAC cookie auth + recharts dashboards + a three-tier test suite and a single-command quality gate. Distilled from four production-remediated sibling codebases (digma, neo-crm, project-management, zero-balance); every rule traces to a failure that actually happened.

### `web-application-engineering`

- **Path**: `skills/web-application-engineering`
- **SKILL.md**: [`skills/web-application-engineering/SKILL.md`](/skills/web-application-engineering/SKILL.md)
- **Title**: Generalized Web Application Engineering Skill (The "ORBITAL-ZB" Standard)
- **Files**: 2
- **Structure**: flat
- **Version**: 1.1.0
- **Flags**: `UNKNOWN_KEYS`

> condensed engineering reference for scaffolding, extending, and maintaining production-grade web applications. It synthesizes the hardest lessons from building high-parity, test-heavy Next.js 16 applications. Next.js 16 (App Router, Standalone Output) + React 19 + TypeScript (Strict) + Tailwind CSS v4 (CSS-First) + Shadcn/UI (Radix Primitives) + ONE Zustand store + Zod-validated API + Prisma/SQLite (or Postgres). Validated against the four source repos (digma, neo-crm, project-management, zero-balance); the fuller distillation is web-application_SKILL.md.

### `web-frameworks`

- **Path**: `skills/web-frameworks`
- **SKILL.md**: [`skills/web-frameworks/SKILL.md`](/skills/web-frameworks/SKILL.md)
- **Title**: Web Frameworks Skill Group
- **Files**: 16
- **Structure**: references, scripts
- **License**: MIT
- **Version**: 1.0.0
- **Flags**: `UNKNOWN_KEYS`

> Build modern full-stack web applications with Next.js 16 + React 19 (App Router, Server Components, RSC, PPR, cacheComponents, async params, SSR, SSG, ISR, standalone output), Turborepo (monorepo, task pipelines, remote caching, parallel execution), and RemixIcon (3100+ SVG icons). Use when creating React applications, implementing server-side rendering, setting up monorepos, optimizing build performance and caching, or working with TypeScript full-stack projects.

### `webapp-testing-journey`

- **Path**: `skills/webapp-testing-journey`
- **SKILL.md**: [`skills/webapp-testing-journey/SKILL.md`](/skills/webapp-testing-journey/SKILL.md)
- **Title**: Webapp Testing Journey
- **Files**: 2
- **Structure**: references
- **Flags**: `BODY_LENGTH`

> Systematic web application testing methodology using OpenClaw browser tools, agent-browser CLI, and chrome-devtools-mcp. Use when testing web application user journeys, validating bug fixes, performing QA verification, or debugging frontend issues. Covers URL journey testing, accessibility tree analysis, DOM inspection, network request debugging, performance tracing, visual regression, and comprehensive issue verification. Triggers on phrases like "test this application", "verify the fix", "check if it works", "test the user journey", "debug this issue".

### `write-swift`

- **Path**: `skills/write-swift`
- **SKILL.md**: [`skills/write-swift/SKILL.md`](/skills/write-swift/SKILL.md)
- **Title**: Write Swift
- **Files**: 1
- **Structure**: flat

> How to write modern Swift well — modeling with value types, Swift 6 data-race safety and approachable concurrency (@concurrent, main-actor-by-default, actors, task groups), protocols and generics (some vs any), API design, performance and ARC, Swift Testing, macros, and the modern language features agents don't know about yet. Use when writing, reviewing, or migrating Swift, or when a concurrency error, a hang, a data race, a retain cycle, or a performance problem needs fixing.

## 2. Design Artifacts & Visual Creation

> **21 skills** in this category.

### `aesthetic`

- **Path**: `skills/aesthetic`
- **SKILL.md**: [`skills/aesthetic/SKILL.md`](/skills/aesthetic/SKILL.md)
- **Title**: Aesthetic
- **Files**: 7
- **Structure**: assets, references

> Create aesthetically beautiful interfaces following proven design principles. Use when building UI/UX, analyzing designs from inspiration sites, generating design images with ai-multimodal, implementing visual hierarchy and color theory, adding micro-interactions, or creating design documentation. Includes workflows for capturing and analyzing inspiration screenshots with chrome-devtools and ai-multimodal, iterative design image generation until aesthetic standards are met, and comprehensive design system guidance covering BEAUTIFUL (aesthetic principles), RIGHT (functionality/accessibility), SATISFYING (micro-interactions), and PEAK (storytelling) stages. Integrates with chrome-devtools, ai-multimodal, media-processing, ui-styling, and web-frameworks skills.

### `code-quality-standards`

- **Path**: `skills/code-quality-standards`
- **SKILL.md**: [`skills/code-quality-standards/SKILL.md`](/skills/code-quality-standards/SKILL.md)
- **Title**: Code Quality & Design Standards
- **Files**: 1
- **Structure**: flat
- **Version**: 2.0.0
- **Flags**: `UNKNOWN_KEYS`

> The absolute constitution for code quality and design rigor. Enforces a Six-Axis review (Correctness, Readability, Architecture, Security, Performance, and Aesthetic/UX Rigor). Use before merging any change, evaluating AI-generated code, or assessing technical debt. Rejects generic 'AI slop' aesthetics and enforces intentional, bespoke design.

### `comfyui-workflow-scaffold`

- **Path**: `skills/comfyui-workflow-scaffold`
- **SKILL.md**: [`skills/comfyui-workflow-scaffold/SKILL.md`](/skills/comfyui-workflow-scaffold/SKILL.md)
- **Title**: ComfyUI Workflow Scaffold
- **Files**: 4
- **Structure**: references

> Create valid ComfyUI workflow JSON templates for Apple Silicon image generation. Use when: (1) Building a new ComfyUI workflow from scratch, (2) Converting a prompt-API format workflow to saved-graph format, (3) Adding Mac-compatible model loading nodes (Z-Image, FLUX.1/2, Krea 2, Ideogram 4, Qwen-Image, FIBO, ERNIE-Image), (4) Scaffolding LoRA/ControlNet/VAE nodes correctly, (5) Validating a workflow will run on Mac MPS/MLX backend, (6) User asks "create a workflow", "scaffold a ComfyUI template", "workflow JSON", "ComfyUI node graph", or "image generation workflow". Triggers on keywords: comfyui, workflow, node graph, json template, scaffold, image pipeline.

### `design-consultation`

- **Path**: `skills/design-consultation`
- **SKILL.md**: [`skills/design-consultation/SKILL.md`](/skills/design-consultation/SKILL.md)
- **Title**: /design-consultation: Your Design System, Built Together
- **Files**: 5
- **Structure**: flat
- **Version**: 1.0.0
- **Flags**: `ALLOWED_TOOLS_LIST`, `UNKNOWN_KEYS`, `BODY_LENGTH`

> Design consultation: understands your product, researches the landscape, proposes a complete design system (aesthetic, typography, color, layout, spacing, motion), and generates font+color preview... (gstack)

### `design-review`

- **Path**: `skills/design-review`
- **SKILL.md**: [`skills/design-review/SKILL.md`](/skills/design-review/SKILL.md)
- **Title**: /design-review: Design Audit → Fix → Verify
- **Files**: 2
- **Structure**: flat
- **Version**: 2.0.0
- **Flags**: `ALLOWED_TOOLS_LIST`, `UNKNOWN_KEYS`, `BODY_LENGTH`

> Designer's eye QA: finds visual inconsistency, spacing issues, hierarchy problems, AI slop patterns, and slow interactions — then fixes them. (gstack)

### `design-shotgun`

- **Path**: `skills/design-shotgun`
- **SKILL.md**: [`skills/design-shotgun/SKILL.md`](/skills/design-shotgun/SKILL.md)
- **Title**: /design-shotgun: Visual Design Exploration
- **Files**: 5
- **Structure**: flat
- **Version**: 1.0.0
- **Flags**: `ALLOWED_TOOLS_LIST`, `UNKNOWN_KEYS`, `BODY_LENGTH`

> Design shotgun: generate multiple AI design variants, open a comparison board, collect structured feedback, and iterate. (gstack)

### `diagram`

- **Path**: `skills/diagram`
- **SKILL.md**: [`skills/diagram/SKILL.md`](/skills/diagram/SKILL.md)
- **Title**: /diagram — English in, editable diagram out
- **Files**: 2
- **Structure**: flat
- **Version**: 1.0.0
- **Flags**: `ALLOWED_TOOLS_LIST`, `UNKNOWN_KEYS`

> Turn an English description (or mermaid source) into a diagram triplet: the source, an editable .excalidraw file you can open on excalidraw.com, and rendered SVG + PNG. (gstack)

### `image-edit`

- **Path**: `skills/image-edit`
- **SKILL.md**: [`skills/image-edit/SKILL.md`](/skills/image-edit/SKILL.md)
- **Title**: Image Edit Skill
- **Files**: 3
- **Structure**: scripts
- **License**: MIT
- **Flags**: `BODY_LENGTH`

> Implement AI image editing and modification capabilities using the z-ai-web-dev-sdk. Use this skill when the user needs to edit existing images, create variations, modify visual content, redesign assets, or transform images based on text descriptions. Supports multiple image sizes and returns base64 encoded results. Also includes CLI tool for quick image editing.

### `image-generation`

- **Path**: `skills/image-generation`
- **SKILL.md**: [`skills/image-generation/SKILL.md`](/skills/image-generation/SKILL.md)
- **Title**: Image Generation Skill
- **Files**: 3
- **Structure**: scripts
- **License**: MIT
- **Flags**: `BODY_LENGTH`

> Implement AI image generation capabilities using the z-ai-web-dev-sdk. Use this skill when the user needs to create images from text descriptions, generate visual content, create artwork, design assets, or build applications with AI-powered image creation. Supports multiple image sizes and returns base64 encoded images. Also includes CLI tool for quick image generation.

### `image-understand`

- **Path**: `skills/image-understand`
- **SKILL.md**: [`skills/image-understand/SKILL.md`](/skills/image-understand/SKILL.md)
- **Title**: Image Understanding Skill
- **Files**: 3
- **Structure**: scripts
- **License**: MIT
- **Flags**: `BODY_LENGTH`

> Implement specialized image understanding capabilities using the z-ai-web-dev-sdk. Use this skill when the user needs to analyze static images, extract visual information, perform OCR, detect objects, classify images, or understand visual content. Optimized for PNG, JPEG, GIF, WebP, and BMP formats.

### `kimi-docx`

- **Path**: `skills/kimi-docx`
- **SKILL.md**: [`skills/kimi-docx/SKILL.md`](/skills/kimi-docx/SKILL.md)
- **Title**: Part 1: Goals
- **Files**: 27
- **Structure**: assets, references, scripts
- **Flags**: `BODY_LENGTH`

> Generate and edit Word documents (.docx). Supports professional documents including covers, charts, track-changes editing, and more. Suitable for any .docx creation or modification task.

### `kimi-pdf`

- **Path**: `skills/kimi-pdf`
- **SKILL.md**: [`skills/kimi-pdf/SKILL.md`](/skills/kimi-pdf/SKILL.md)
- **Title**: Check environment (JSON output, exit code 0=ok, 2=missing deps)
- **Files**: 18
- **Structure**: routes, scripts

> Professional PDF solution. Create PDFs using HTML+Paged.js (academic papers, reports, documents). Process existing PDFs using Python (read, extract, merge, split, fill forms). Supports KaTeX math formulas, Mermaid diagrams, three-line tables, citations, and other academic elements. Also use this skill when user explicitly requests LaTeX (.tex) or native LaTeX compilation.

### `kimi-xlsx`

- **Path**: `skills/kimi-xlsx`
- **SKILL.md**: [`skills/kimi-xlsx/SKILL.md`](/skills/kimi-xlsx/SKILL.md)
- **Title**: Create workbook
- **Files**: 2
- **Structure**: flat
- **Flags**: `BODY_LENGTH`

> Specialized utility for advanced manipulation, analysis, and creation of spreadsheet files, including (but not limited to) XLSX, XLSM, CSV formats. Core functionalities include formula deployment, complex formatting (including automatic currency formatting for financial tasks), data visualization, and mandatory post-processing recalculation.

### `pdf-old-20260806`

- **Path**: `skills/pdf-old-20260806`
- **SKILL.md**: [`skills/pdf-old-20260806/SKILL.md`](/skills/pdf-old-20260806/SKILL.md)
- **Title**: PDF - Document Production Workbench
- **Files**: 39
- **Structure**: references, scripts
- **License**: Proprietary. LICENSE.txt has complete terms
- **Flags**: `BODY_LENGTH`
- **Duplicate**: essentially identical to `pdf`

> Professional PDF toolkit with four production lines: Report - structured documents via ReportLab (reports, proposals, contracts, white papers) Creative - visual design via JSON Blueprint → design_engine.py → Playwright snapshot (posters, infographics, invitations, dashboards). Academic - scholarly work via LaTeX/Tectonic (papers, theses, math-heavy documents) Process - manipulate existing PDFs (extract, merge, split, fill forms, convert) Auto-routes based on document type. Includes ATS/creative/academic resume sub-paths.

### `podcast-generate`

- **Path**: `skills/podcast-generate`
- **SKILL.md**: [`skills/podcast-generate/SKILL.md`](/skills/podcast-generate/SKILL.md)
- **Title**: Podcast Generate Skill（TypeScript 版本）
- **Files**: 7
- **Structure**: flat
- **License**: MIT

> Generate podcast episodes from user-provided content or by searching the web for specified topics. If user uploads a text file/article, creates a dual-host dialogue podcast (or single-host upon request). If no content is provided, searches the web for information about the user-specified topic and generates a podcast. Duration scales with content size (3-20 minutes, ~240 chars/min). Uses z-ai-web-dev-sdk for LLM script generation and TTS audio synthesis. Outputs both a podcast script (Markdown) and a complete audio file (WAV).

### `project-architecture-document-md`

- **Path**: `skills/project-architecture-document-md`
- **SKILL.md**: [`skills/project-architecture-document-md/SKILL.md`](/skills/project-architecture-document-md/SKILL.md)
- **Title**: Project Architecture Document (PAD) Generator
- **Files**: 1
- **Structure**: flat

> Create a comprehensive Project Architecture Document (PAD) for any codebase. Use when the user asks to generate a PAD, architecture document, system design document, or technical blueprint for a project. Also triggers on "document this codebase", "create architecture reference", "generate system overview", "write ADR", "document the architecture of this project". Covers executive summary, tech stack with version pinning, Architecture Decision Records (ADRs), system topology diagrams, layer models, annotated directory structures, critical code patterns with invariants, database schemas, security architecture, testing strategy, build/deployment, developer handbook, and known issues. Produces a single source-of-truth markdown document that serves as the definitive engineering reference for onboarding, debugging, and replication.

### `stock-analysis`

- **Path**: `skills/stock-analysis`
- **SKILL.md**: [`skills/stock-analysis/SKILL.md`](/skills/stock-analysis/SKILL.md)
- **Title**: Stock Analysis Skill
- **Files**: 10
- **Structure**: flat

> Comprehensive stock market analysis skill covering A-share (China), Hong Kong, and US equities. Priority use cases: stock analysis and buy/sell/hold recommendations by ticker code, generating decision dashboards and research reports with technical/fundamental/sentiment analysis, position-aware investment strategies based on user's cost price, dividend income scoring and safety analysis, rumor and early market signal scanning (M&A, insider activity, analyst actions), watchlist management with price target and stop-loss alerts, and K-line chart pattern recognition from images. This skill should be the primary choice whenever users mention a stock ticker, ask whether to buy or sell a stock, reference their holding cost or position, request dividend analysis, ask about market rumors or early signals, want to add/check/manage a watchlist, or upload a chart image for technical analysis.

### `video-generation`

- **Path**: `skills/video-generation`
- **SKILL.md**: [`skills/video-generation/SKILL.md`](/skills/video-generation/SKILL.md)
- **Title**: Video Generation Skill
- **Files**: 3
- **Structure**: scripts
- **License**: MIT
- **Flags**: `BODY_LENGTH`

> Implement AI-powered video generation capabilities using the z-ai-web-dev-sdk. Use this skill when the user needs to generate videos from text prompts or images, create video content programmatically, or build applications that produce video outputs. Supports asynchronous task management with status polling and result retrieval.

### `video-understand`

- **Path**: `skills/video-understand`
- **SKILL.md**: [`skills/video-understand/SKILL.md`](/skills/video-understand/SKILL.md)
- **Title**: Video Understanding Skill
- **Files**: 3
- **Structure**: scripts
- **License**: MIT
- **Flags**: `BODY_LENGTH`

> Implement specialized video understanding capabilities using the z-ai-web-dev-sdk. Use this skill when the user needs to analyze video content, understand motion and temporal sequences, extract information from video frames, describe video scenes, or perform video-based AI analysis. Optimized for MP4, AVI, MOV, and other common video formats.

### `web-shader-extractor`

- **Path**: `skills/web-shader-extractor`
- **SKILL.md**: [`skills/web-shader-extractor/SKILL.md`](/skills/web-shader-extractor/SKILL.md)
- **Title**: Web Shader Extractor
- **Files**: 12
- **Structure**: references, scripts

> 从网页中提取 WebGL/Canvas/Shader 视觉特效代码，反混淆后移植为独立原生 JS 项目。 触发条件：用户提供网址并要求提取 shader、提取特效、提取动画效果、提取 canvas 效果、 复刻某网站的视觉效果、"把这个网站的背景效果扒下来" 等。

### `xlsx`

- **Path**: `skills/xlsx`
- **SKILL.md**: [`skills/xlsx/SKILL.md`](/skills/xlsx/SKILL.md)
- **Title**: XLSX — Scene-Driven Spreadsheet Workbench
- **Files**: 21
- **Structure**: engines, scenes, templates
- **License**: Proprietary. LICENSE.txt has complete terms
- **Author**: Z.AI
- **Version**: 1.0

> Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xlsx, .xlsm, .csv, or .tsv file; create a new spreadsheet from scratch or from other data sources; analyze data and output results as an Excel file with charts; convert between tabular file formats (CSV/JSON/PDF → XLSX or vice versa); clean, merge, pivot, or transform tabular data. Trigger especially when the user references a spreadsheet file by name or path, says 'make a table/report/model', mentions Excel/CSV/数据分析/报表/汇总, or wants data visualization inside a spreadsheet.

## 3. Full-Stack & Backend Development

> **22 skills** in this category.

### `api-patterns`

- **Path**: `skills/api-patterns`
- **SKILL.md**: [`skills/api-patterns/SKILL.md`](/skills/api-patterns/SKILL.md)
- **Title**: API Patterns
- **Files**: 12
- **Structure**: scripts

> API design principles and decision-making. REST vs GraphQL vs tRPC selection, response formats, versioning, pagination.

### `context7-docs`

- **Path**: `skills/context7-docs`
- **SKILL.md**: [`skills/context7-docs/SKILL.md`](/skills/context7-docs/SKILL.md)
- **Title**: Context7 Documentation Search
- **Files**: 1
- **Structure**: flat

> Search and retrieve up-to-date curated documentation from Context7 for any software, library, or package. Use when: (1) Need latest documentation for a specific library or tool, (2) Looking for code examples and patterns, (3) Need accurate API reference information, (4) Building workflows with specific tools like n8n, (5) Want to avoid hallucinated or outdated documentation. Triggers on phrases like "search Context7 for", "get documentation for", "find latest docs", "n8n workflow", "package documentation".

### `django-6`

- **Path**: `skills/django-6`
- **SKILL.md**: [`skills/django-6/SKILL.md`](/skills/django-6/SKILL.md)
- **Title**: Django 6 — Full-Stack Python Workflow Skill
- **Files**: 1
- **Structure**: flat
- **License**: Proprietary. LICENSE.txt has complete terms
- **Flags**: `BODY_LENGTH`

> Django 6.x (Python 3.12+, released August 2025 LTS) full-stack workflow skill. Covers the ORM with migrations (write Python, not SQL), Class-Based Views vs Function-Based Views decision, Django REST Framework (DRF) for APIs (Serializers, ViewSets, Routers), Django admin for free CRUD, async views with full async ORM support, Celery + Redis for background tasks, django-allauth for social auth, pytest-django for modern testing, split settings (base/dev/prod), ASGI deployment via Daphne/Uvicorn, WhiteNoise for static files, psycopg3 for PostgreSQL. Use when building any Python web application, API, or service on Django 6 — especially when the task involves migrations, ORM queries, DRF serializers/viewsets, async views, Celery tasks, or admin customization where idiomatic Django differs from generic Python patterns.

### `dotnet-9`

- **Path**: `skills/dotnet-9`
- **SKILL.md**: [`skills/dotnet-9/SKILL.md`](/skills/dotnet-9/SKILL.md)
- **Title**: .NET 9 + ASP.NET Core — Enterprise C# Backend Workflow Skill
- **Files**: 1
- **Structure**: flat
- **License**: Proprietary. LICENSE.txt has complete terms
- **Flags**: `BODY_LENGTH`

> .NET 9 (C# 13, LTS) + ASP.NET Core enterprise backend workflow skill. Covers the IoC container (constructor injection, AddScoped/AddTransient/AddSingleton lifetimes), minimal APIs (MapGet/MapPost/MapPut/MapDelete with lambda handlers) vs controller-based APIs, Entity Framework Core 9 (DbContext, LINQ queries, migrations via dotnet ef, AsNoTracking, N+1 detection), ASP.NET Core Identity + JWT auth + built-in OpenAPI support, Kestrel web server, configuration via appsettings.json + environment variables, C# 13 records, pattern matching, and nullable reference types, xUnit + Moq for testing, and the canonical deployment story (self-contained single-file publish on Linux, Docker multi-stage build). Use when building any C# / .NET enterprise web app, REST API, or microservice on .NET 9 — especially when the task involves EF Core entity design, LINQ queries, DI lifetime choice, JWT auth, or self-contained deployment where idiomatic .NET differs from Java Spring Boot or other web frameworks.

### `fastapi-sqlalchemy`

- **Path**: `skills/fastapi-sqlalchemy`
- **SKILL.md**: [`skills/fastapi-sqlalchemy/SKILL.md`](/skills/fastapi-sqlalchemy/SKILL.md)
- **Title**: FastAPI + SQLAlchemy 2.0 + Pydantic v2 — Modern Python Async API Workflow
- **Files**: 1
- **Structure**: flat
- **License**: Proprietary. LICENSE.txt has complete terms
- **Flags**: `BODY_LENGTH`

> FastAPI (0.115+) + SQLAlchemy 2.0 (async with asyncpg) + Pydantic v2 + Alembic modern Python async API workflow skill. Covers the async-first mental model (async def endpoints, AsyncSession, asyncpg driver), Pydantic v2 validation (Annotated types, model_validator, field_validator, computed_field), SQLAlchemy 2.0 unified API (sync Session, async AsyncSession, Mapped[] annotations, DeclarativeBase, select() statement API), dependency injection via Depends() for DB sessions and auth, the lifespan context manager, Alembic async migrations, OpenAPI/Swagger auto-generation, tooling (uv, Ruff, pytest), and deployment via Uvicorn/Gunicorn workers or serverless. Use when building any Python async REST API, microservice, or modern backend with FastAPI — especially when the task involves async DB sessions, Pydantic v2 validation patterns, SQLAlchemy 2.0 Mapped[] types, dependency injection design, or async migrations where idiomatic FastAPI differs from Django sync patterns or SQLAlchemy 1.x code.

### `fastify`

- **Path**: `skills/fastify`
- **SKILL.md**: [`skills/fastify/SKILL.md`](/skills/fastify/SKILL.md)
- **Title**: Fastify 5 — High-Performance Node.js Web Framework
- **Files**: 1
- **Structure**: flat
- **License**: Proprietary. LICENSE.txt has complete terms
- **Flags**: `BODY_LENGTH`

> Fastify 5 (Node.js 20+, released 2024) high-performance web framework workflow skill. Covers the schema-first design (JSON Schema for request validation + response serialization, compiled for 2-3x faster serialization), the plugin encapsulation model (fastify.register() creates isolated scopes with their own decorators/hooks), the hook lifecycle (onRequest through onResponse), decorators, the TypeBox type provider for TypeScript, the official plugin ecosystem (cors, helmet, rate-limit, jwt, static, swagger), the @fastify/cli, pino logging by default, and deployment via standard Node.js (PM2, Docker). Use when building any Node.js HTTP API, microservice, or high-throughput backend — especially when the task involves schema validation, plugin encapsulation, migrating from Express, performance optimization, or comparing Fastify vs Express vs Hono vs NestJS where idiomatic Fastify (schema-first, encapsulated plugins, pino logging) differs from Express (global middleware, no schema) or NestJS (IoC, decorators).

### `framework-templates`

- **Path**: `skills/framework-templates`
- **SKILL.md**: [`skills/framework-templates/SKILL.md`](/skills/framework-templates/SKILL.md)
- **Title**: Framework Templates
- **Files**: 2
- **Structure**: flat
- **Version**: 2.0.0
- **Flags**: `UNKNOWN_KEYS`, `BODY_LENGTH`

> Deep reference library for framework-specific CLAUDE.md sections. Contains production-ready templates for Next.js, Laravel, Rails, Django, React Native, Flutter, Go, Rust, and more. Use alongside the claude-md skill for complete CLAUDE.md generation.

### `go-web`

- **Path**: `skills/go-web`
- **SKILL.md**: [`skills/go-web/SKILL.md`](/skills/go-web/SKILL.md)
- **Title**: Go Web — Backend Workflow Skill
- **Files**: 1
- **Structure**: flat
- **License**: Proprietary. LICENSE.txt has complete terms
- **Flags**: `BODY_LENGTH`

> Go (Golang 1.23+) web backend workflow skill. Covers the stdlib-first philosophy (net/http is production-grade — frameworks are optional thin wrappers), router choices (net/http ServeMux with Go 1.22+ pattern routing, chi, Echo, Gin), sqlc for type-safe SQL codegen (preferred over ORM for most projects), pgx for native PostgreSQL access, the interface satisfaction model (implicit), error-as-values (no exceptions), goroutines + channels for concurrency, context.Context for cancellation/timeouts, testify table-driven tests, embedding assets via go:embed, and the unique Go deployment story (single static binary — no runtime dependencies). Use when building any HTTP API, microservice, CLI with HTTP features, or backend service in Go — especially when the task involves choosing between stdlib and a framework, designing context-aware handlers, writing type-safe database access, or shipping a single-binary deployment where idiomatic Go differs from Node.js/Python/Ruby patterns.

### `keystonejs-6`

- **Path**: `skills/keystonejs-6`
- **SKILL.md**: [`skills/keystonejs-6/SKILL.md`](/skills/keystonejs-6/SKILL.md)
- **Title**: KeystoneJS 6 — Schema-as-Code Headless CMS + Admin + GraphQL API
- **Files**: 1
- **Structure**: flat
- **License**: Proprietary. LICENSE.txt has complete terms
- **Flags**: `BODY_LENGTH`

> KeystoneJS 6 (TypeScript, Node.js 20+) schema-as-code headless CMS + admin panel generator + GraphQL API workflow skill. Covers the schema-as-code paradigm (define lists with fields in keystone.ts → Keystone auto-generates the admin UI, GraphQL schema, and Prisma schema — no manual CRUD, admin, or resolvers), typed field types with their own admin UI widgets, access control (list-level operation access + item-level filters), session management (email/password or custom strategies), CRUD hooks for business logic, Prisma under the hood (you never write Prisma code), and the auto-generated Admin UI. Use when building any content-heavy app — blog, CMS, e-commerce catalog, admin panel, internal tool — especially when the task involves schema design, access control, hooks for business logic, or auto-generated admin UI where idiomatic Keystone (schema-as-code → auto-generated everything) differs fundamentally from building CRUD manually with Express/Fastify/NestJS plus a separate admin library.

### `kubernetes-env-setup`

- **Path**: `skills/kubernetes-env-setup`
- **SKILL.md**: [`skills/kubernetes-env-setup/SKILL.md`](/skills/kubernetes-env-setup/SKILL.md)
- **Title**: Hardened Kubernetes on Azure Linux 3.0
- **Files**: 8
- **Structure**: flat
- **Version**: 1.0
- **Flags**: `UNKNOWN_KEYS`, `BODY_LENGTH`

> Production-grade self-managed Kubernetes cluster on Azure Linux 3.0 (kubeadm) with CIS/NSA/CISA-aligned hardening for agentic AI and LLM workloads. Covers host hardening (SELinux, Trusted Launch, OS Guard IPE), containerd, Cilium eBPF CNI, Kyverno policy-as-code, gVisor/Kata Containers sandboxing, cosign/Sigstore supply chain security, Falco runtime detection, Pod Security Admission, RBAC, secrets management, network segmentation, high availability (multi-AZ), backup with Velero, and compliance validation (kube-bench, Kubescape). Includes OWASP LLM Top 10 and MITRE ATLAS threat modeling for prompt injection defense.

### `minimax-docx`

- **Path**: `skills/minimax-docx`
- **SKILL.md**: [`skills/minimax-docx/SKILL.md`](/skills/minimax-docx/SKILL.md)
- **Title**: minimax-docx
- **Files**: 75
- **Structure**: assets, references, scripts
- **License**: MIT
- **Author**: MiniMaxAI
- **Version**: 1.0.0
- **Flags**: `METADATA_NON_STRING`, `UNKNOWN_KEYS`

> Professional DOCX document creation, editing, and formatting using OpenXML SDK (.NET). Three pipelines: (A) create new documents from scratch, (B) fill/edit content in existing documents, (C) apply template formatting with XSD validation gate-check. MUST use this skill whenever the user wants to produce, modify, or format a Word document — including when they say "write a report", "draft a proposal", "make a contract", "fill in this form", "reformat to match this template", or any task whose final output is a .docx file. Even if the user doesn't mention "docx" explicitly, if the task implies a printable/formal document, use this skill.

### `n8n-workflow-automation`

- **Path**: `skills/n8n-workflow-automation`
- **SKILL.md**: [`skills/n8n-workflow-automation/SKILL.md`](/skills/n8n-workflow-automation/SKILL.md)
- **Title**: n8n Workflow Automation
- **Files**: 6
- **Structure**: references

> Build and automate n8n workflows using JSON specification. Use when: (1) Creating n8n workflows programmatically, (2) Converting workflows to/from JSON, (3) Understanding n8n node types and connections, (4) Writing n8n expressions, (5) Debugging workflow JSON structure, (6) Building workflow templates. Triggers on phrases like "n8n workflow", "n8n JSON", "n8n expression", "webhook workflow", "n8n automation".

### `nestjs`

- **Path**: `skills/nestjs`
- **SKILL.md**: [`skills/nestjs/SKILL.md`](/skills/nestjs/SKILL.md)
- **Title**: NestJS — Enterprise TypeScript Backend Workflow Skill
- **Files**: 1
- **Structure**: flat
- **License**: Proprietary. LICENSE.txt has complete terms
- **Flags**: `BODY_LENGTH`

> NestJS 10+ (TypeScript, Node.js 20+) enterprise backend workflow skill. Covers the Angular-inspired architecture (modules, controllers, providers with decorators), the IoC container (constructor injection, DI tokens, custom providers, scopes), DTOs with class-validator + class-transformer (ValidationPipe), exception filters, guards (@CanActivate) for authz, interceptors, pipes, middleware, TypeORM/Prisma/Drizzle integration, Passport-based auth (JwtStrategy, LocalStrategy), testing utilities (Test.createTestingModule, Supertest), Swagger/OpenAPI via @nestjs/swagger, and the Fastify adapter as a faster alternative to Express. Use when building any TypeScript enterprise backend, REST API, GraphQL API, or microservice on NestJS — especially when the task involves module organization, DI provider configuration, custom decorators, interceptor/guard/pipe composition, or testing with the testing module where idiomatic NestJS differs from Express/Fastify or from other IoC frameworks like Spring Boot.

### `phoenix-1-7`

- **Path**: `skills/phoenix-1-7`
- **SKILL.md**: [`skills/phoenix-1-7/SKILL.md`](/skills/phoenix-1-7/SKILL.md)
- **Title**: Phoenix 1.7 (Elixir) — Functional Real-Time Web Framework
- **Files**: 1
- **Structure**: flat
- **License**: Proprietary. LICENSE.txt has complete terms
- **Flags**: `BODY_LENGTH`

> Phoenix 1.7 (Elixir 1.16+ on the BEAM VM) full-stack functional web framework workflow skill. Covers the OTP supervision tree mental model (processes, GenServers, Supervisors), Ecto 3 (migrations, changesets, Repo, schemas), LiveView (the SPA-less real-time UI paradigm — server-rendered HTML updated via WebSocket, no JS framework needed for most interactions), HEEx templates (~H sigil and <.component> syntax), verified routes (~p sigil), Presence (track connected users), PubSub (powers LiveView and real-time features), ETS caching, Mnesia, ExUnit testing, and deployment via Elixir releases + Fly.io. Use when building any Elixir/Phoenix web app, real-time app, or distributed system — especially when the task involves LiveView state management, Ecto changesets, OTP supervision, PubSub broadcasting, or release deployment where idiomatic Phoenix (functional + actor model + BEAM concurrency) differs fundamentally from object-oriented frameworks like Rails/Django/Spring Boot.

### `powershell-windows`

- **Path**: `skills/powershell-windows`
- **SKILL.md**: [`skills/powershell-windows/SKILL.md`](/skills/powershell-windows/SKILL.md)
- **Title**: PowerShell Windows Patterns
- **Files**: 1
- **Structure**: flat

> PowerShell Windows patterns. Critical pitfalls, operator syntax, error handling.

### `python-patterns`

- **Path**: `skills/python-patterns`
- **SKILL.md**: [`skills/python-patterns/SKILL.md`](/skills/python-patterns/SKILL.md)
- **Title**: Python Patterns
- **Files**: 1
- **Structure**: flat

> Python development principles and decision-making. Framework selection, async patterns, type hints, project structure. Teaches thinking, not copying.

### `rails-8`

- **Path**: `skills/rails-8`
- **SKILL.md**: [`skills/rails-8/SKILL.md`](/skills/rails-8/SKILL.md)
- **Title**: Ruby on Rails 8 — Full-Stack Ruby Workflow Skill
- **Files**: 1
- **Structure**: flat
- **License**: Proprietary. LICENSE.txt has complete terms
- **Flags**: `BODY_LENGTH`

> Ruby on Rails 8 (Ruby 3.2+) full-stack workflow skill. Covers Rails 8 new defaults: Solid Queue / Solid Cache / Solid Cable (Redis-free by default — backed by SQLite/Postgres/MySQL), Propshaft (replaces Sprockets), Kamal 2 (Docker-based deploys to any cloud), Thruster (Puma HTTP/2 proxy with TLS). MVC structure (Active Record models, controllers, ERB + Hotwire views), Active Record (migrations, validations, associations, callbacks — and when NOT to use callbacks), routing (resources, nested routes, member/collection, concerns), strong parameters, Hotwire (Turbo Drive, Turbo Frames, Turbo Streams, Stimulus.js), Solid Queue (default) or Sidekiq for background jobs, Minitest or RSpec, Devise / bcrypt / has_secure_password for auth, Action Mailer, Active Storage. Use when building any Ruby web app on Rails 8 — especially when the task involves migrations, Active Record queries, Hotwire/Turbo, background jobs, or Kamal deployment where idiomatic Rails differs from generic Ruby or from other web frameworks.

### `react19-vite-spa-fastify-drizzle-sqlite`

- **Path**: `skills/react19-vite-spa-fastify-drizzle-sqlite`
- **SKILL.md**: [`skills/react19-vite-spa-fastify-drizzle-sqlite/SKILL.md`](/skills/react19-vite-spa-fastify-drizzle-sqlite/SKILL.md)
- **Title**: reddit-clone SKILL — Engineering Reference for Full-Stack TypeScript Monorepos
- **Files**: 1
- **Structure**: flat
- **Version**: 1.1.0
- **Flags**: `UNKNOWN_KEYS`, `BODY_LENGTH`

> npm-workspaces monorepo reference for reddit-clone (embers): React 19 + Vite 7 SPA with HashRouter and vite-plugin-singlefile (single HTML deploy to GitHub Pages or S3), Tailwind CSS v4 CSS-first, Zustand overlay pattern, Fastify 5 composition-root buildApp, Drizzle ORM 0.36 + SQLite + better-sqlite3 + FTS5, Zod schemas at every boundary, JWT HS256 via jose + argon2id, pino logging, TypeScript 5.9 strict, ESLint 9 flat, Vitest and Playwright. Use when building a full-stack TypeScript monorepo, a deploy-anywhere static SPA with deterministic PRNG client data and a real Fastify backend, a community feed or forum with atomic voting and branded IDs, or when you need schema-versioned persistence, pure selectors, or SQLite online backup patterns.

### `security-and-hardening`

- **Path**: `skills/security-and-hardening`
- **SKILL.md**: [`skills/security-and-hardening/SKILL.md`](/skills/security-and-hardening/SKILL.md)
- **Title**: Security and Hardening
- **Files**: 1
- **Structure**: flat

> Hardens code against vulnerabilities. Use when handling user input, authentication, data storage, or external integrations. Use when building any feature that accepts untrusted data, manages user sessions, or interacts with third-party services.

### `spring-boot-3`

- **Path**: `skills/spring-boot-3`
- **SKILL.md**: [`skills/spring-boot-3/SKILL.md`](/skills/spring-boot-3/SKILL.md)
- **Title**: Spring Boot 3 — Enterprise Java Backend Workflow Skill
- **Files**: 1
- **Structure**: flat
- **License**: Proprietary. LICENSE.txt has complete terms
- **Flags**: `BODY_LENGTH`

> Spring Boot 3.x (Java 21+ with virtual threads, released November 2023) enterprise backend workflow skill. Covers the IoC container (constructor injection, stereotype annotations, @Configuration, @Bean), Spring Data JPA with Hibernate (JpaRepository, @Entity, JPQL, @Transactional, N+1 detection), Spring MVC @RestController with mapping annotations, Spring Security 6 (SecurityFilterChain DSL, @PreAuthorize, OAuth2 JWT), Spring Boot Actuator for production observability (/health, /metrics), Maven vs Gradle, the Java 21 virtual threads story (spring.threads.virtual.enabled=true), JUnit 5 + Mockito, and the canonical deployment story (fat JAR, Docker, JVM tuning). Use when building any Java enterprise web app, REST API, or microservice on Spring Boot 3 — especially when the task involves JPA entity design, repository methods, @Transactional boundaries, Spring Security filter chains, or Actuator endpoint configuration where idiomatic Spring differs from generic Java or other web frameworks.

### `trustskill`

- **Path**: `skills/trustskill`
- **SKILL.md**: [`skills/trustskill/SKILL.md`](/skills/trustskill/SKILL.md)
- **Title**: TrustSkill v3.1 - Advanced Skill Security Scanner
- **Files**: 56
- **Structure**: references, scripts
- **Version**: 3.1.0
- **Flags**: `UNKNOWN_KEYS`

> TrustSkill v3.1 - Advanced security scanner for OpenClaw skills with 99% false positive reduction. Detects malicious code, hardcoded secrets, vulnerable dependencies, tainted data flows, backdoors, credential theft, privacy file access, command injection, file system risks, network exfiltration, and sensitive data leaks. Features entropy-based secret detection, OSV vulnerability database integration, taint analysis, smart data flow detection, context-aware documentation scanning, and flexible YAML configuration.

### `wizard`

- **Path**: `skills/wizard`
- **SKILL.md**: [`skills/wizard/SKILL.md`](/skills/wizard/SKILL.md)
- **Title**: Wizard
- **Files**: 3
- **Structure**: flat

> Generate an interactive bash wizard that walks a human through steps only they can perform. Use when provisioning infrastructure, setting up credentials or CI secrets, walking an unfamiliar third-party dashboard, or running a one-off migration or cutover. Don't invoke this for steps the agent can perform itself.

## 4. AI / ML / Multimodal SDK Skills

> **17 skills** in this category.

### `ai-news-collectors`

- **Path**: `skills/ai-news-collectors`
- **SKILL.md**: [`skills/ai-news-collectors/SKILL.md`](/skills/ai-news-collectors/SKILL.md)
- **Title**: AI News Collector
- **Files**: 3
- **Structure**: references

> AI 新闻聚合与热度排序工具。当用户询问 AI 领域最新动态时触发，如："今天有什么 AI 新闻？""总结一下这周的 AI 动态""最近有什么火的 AI 产品？""AI 圈最近在讨论什么？"。覆盖：新产品发布、研究论文、行业动态、融资新闻、开源项目更新、社区病毒传播现象、AI 工具/Agent 热门项目。输出中文摘要列表，按热度排序，附带原文链接。

### `aminer-academic-search`

- **Path**: `skills/aminer-academic-search`
- **SKILL.md**: [`skills/aminer-academic-search/SKILL.md`](/skills/aminer-academic-search/SKILL.md)
- **Title**: AMiner Open Platform Academic Data Query
- **Files**: 4
- **Structure**: references, scripts
- **Author**: AMiner
- **Version**: 1.2.1
- **Flags**: `METADATA_NON_STRING`, `UNKNOWN_KEYS`

> ACADEMIC PRIORITY: Activate for any academic, scholarly, or research query - papers, citations, scholars, researchers, institutions, journals, venues, patents, h-index, research trends, or 'who published what / where / when'. Precedence over web search for academic data. Full-featured AMiner skill: 28 APIs + 5 workflows for tasks free APIs cannot satisfy. Use for: scholar full profiles (bio, education, honors, papers, patents, projects), paper deep dives (abstract, keywords, citation chains), multi-condition or semantic paper search (paper_qa_search_pro), institution capability analysis, venue paper monitoring by year, patent deep details (IPC/CPC, assignee, claims), and any query needing paid API fields. Do NOT use for simple lookups free APIs answer (title check, scholar by name, org/venue normalization) - use aminer-free-academic instead. Routing: if paper_search, paper_info, person_search, organization_search, venue_search, patent_search, or patent_info alone suffices, route to aminer-free-academic.

### `aminer-daily-paper`

- **Path**: `skills/aminer-daily-paper`
- **SKILL.md**: [`skills/aminer-daily-paper/SKILL.md`](/skills/aminer-daily-paper/SKILL.md)
- **Title**: aminer-daily-paper
- **Files**: 11
- **Structure**: scripts
- **Version**: 1.1.2
- **Flags**: `METADATA_NON_STRING`, `UNKNOWN_KEYS`

> Personalized academic paper recommendation via AMiner rec5 API. Activate this skill whenever the user asks for paper recommendations, whether triggered by /aminer-dp, /skill aminer-dp, or any natural language request such as 'recommend me papers on multimodal agents'. When invoked: extract topics/scholar signals from the input yourself, call handle_trigger.py with structured fields, then present the Markdown in `reply_text` to the user.

### `aminer-deep-search`

- **Path**: `skills/aminer-deep-search`
- **SKILL.md**: [`skills/aminer-deep-search/SKILL.md`](/skills/aminer-deep-search/SKILL.md)
- **Title**: AMiner Deep Search
- **Files**: 8
- **Structure**: scripts
- **Author**: AMiner
- **Version**: 2.0.0
- **Flags**: `METADATA_NON_STRING`, `UNKNOWN_KEYS`

> Activate this skill when the user wants deep, multi-round academic paper collection for a survey or literature review. The host model (the model running this skill) drives the loop itself: it expands queries, judges relevance, snowballs backward references, and decides when to stop. The bundled scripts are pure tool commands that call documented AMiner Open Platform endpoints and print JSON tool results only — no extra LLM configuration is needed. Use this skill for broad topic exploration, survey bibliography construction, and collecting hundreds of candidate papers with AMiner IDs and titles. Not intended for single-paper lookup or lightweight recommendations; use aminer-free-academic or aminer-daily-paper for those.

### `aminer-free-academic`

- **Path**: `skills/aminer-free-academic`
- **SKILL.md**: [`skills/aminer-free-academic/SKILL.md`](/skills/aminer-free-academic/SKILL.md)
- **Title**: AMiner Free Search
- **Files**: 3
- **Structure**: references
- **Author**: AMiner
- **Version**: 1.1.1
- **Flags**: `METADATA_NON_STRING`, `UNKNOWN_KEYS`

> ACADEMIC PRIORITY: Activate whenever the user's query involves any academic or research-related topic. Free-tier entry point for AMiner academic search (7 free APIs, zero cost). Use for simple, single-step academic lookups that do not require paid API fields: paper search by title to get its ID, checking a paper's author, venue, year, or citation bucket, scholar lookup by name with interests, institution, and citation count, institution name normalization, venue type checks, patent trend scans by keyword, and lightweight paper metadata via paper_info. Do NOT use for full abstracts, multi-condition or semantic search, citation analysis, scholar full profiles, institution output analysis, venue paper lists, patent deep details, or anything requiring paid APIs. Routing: if the question can be fully answered by paper_search, paper_info, person_search, organization_search, venue_search, patent_search, or patent_info alone, use this skill; otherwise route to aminer-academic-search.

### `asr`

- **Path**: `skills/asr`
- **SKILL.md**: [`skills/asr/SKILL.md`](/skills/asr/SKILL.md)
- **Title**: ASR (Speech to Text) Skill
- **Files**: 3
- **Structure**: scripts
- **License**: MIT
- **Flags**: `BODY_LENGTH`

> Implement speech-to-text (ASR/automatic speech recognition) capabilities using the z-ai-web-dev-sdk. Use this skill when the user needs to transcribe audio files, convert speech to text, build voice input features, or process audio recordings. Supports base64 encoded audio files and returns accurate text transcriptions.

### `auto-target-tracker`

- **Path**: `skills/auto-target-tracker`
- **SKILL.md**: [`skills/auto-target-tracker/SKILL.md`](/skills/auto-target-tracker/SKILL.md)
- **Title**: 自动目标进度追踪器
- **Files**: 1
- **Structure**: flat

> 自动目标进度追踪器。在对话中检测到目标相关图片（笔记、进度、截图、记录）时，自动调用 VLM 识别关键信息并记录到目标日记。适用于学习管理、健身追踪、工作进度、习惯养成、创作记录等所有目标管理场景。

### `browser-automation`

- **Path**: `skills/browser-automation`
- **SKILL.md**: [`skills/browser-automation/SKILL.md`](/skills/browser-automation/SKILL.md)
- **Title**: browser-automation
- **Files**: 1
- **Structure**: flat

> Fast browser automation CLI for AI agents using Chrome/Chromium via CDP. Use when automating web interactions, taking snapshots, filling forms, navigating pages, or testing web applications without Playwright/Puppeteer dependency.

### `llm`

- **Path**: `skills/llm`
- **SKILL.md**: [`skills/llm/SKILL.md`](/skills/llm/SKILL.md)
- **Title**: LLM (Large Language Model) Skill
- **Files**: 3
- **Structure**: scripts
- **License**: MIT
- **Flags**: `BODY_LENGTH`

> Implement large language model (LLM) chat completions using the z-ai-web-dev-sdk. Use this skill when the user needs to build conversational AI applications, chatbots, AI assistants, or any text generation features. Supports multi-turn conversations, system prompts, and context management.

### `mac-mlx-local-inference`

- **Path**: `skills/mac-mlx-local-inference`
- **SKILL.md**: [`skills/mac-mlx-local-inference/SKILL.md`](/skills/mac-mlx-local-inference/SKILL.md)
- **Title**: 🚀 Complete Guide: OpenAI-Compatible MLX Endpoint on Apple Silicon
- **Files**: 1
- **Structure**: flat
- **Version**: 1.0
- **Flags**: `UNKNOWN_KEYS`, `BODY_LENGTH`

> Local LLM inference on Apple Silicon (M1-M5) using mlx-optiq with OpenAI/Anthropic-compatible API endpoints. Covers Qwen3.6-27B setup, mixed-precision KV cache, MTP speculative decoding, and coding agent integrations (OpenCode, Kilo Code, Pi Agent, Claude Code, Codex, Cursor). Fully offline, zero cloud dependency.

### `microsoft-foundry`

- **Path**: `skills/microsoft-foundry`
- **SKILL.md**: [`skills/microsoft-foundry/SKILL.md`](/skills/microsoft-foundry/SKILL.md)
- **Title**: Microsoft Foundry Skill
- **Files**: 163
- **Structure**: references
- **License**: MIT
- **Author**: Microsoft
- **Version**: 1.1.44

> Deploy, evaluate, fine-tune, and manage Foundry agents end-to-end with azd: hosted agent scaffold/run/deploy, prompt agent create, batch eval, continuous eval, prompt optimizer, Agent Optimizer scaffold, agent.yaml, dataset curation from traces, model fine-tuning (SFT/DPO/RFT). USE FOR: azd ai agent, azd provision/deploy, deploy agent, hosted agent, create agent, add tool to agent, invoke agent, evaluate agent, continuous eval, continuous monitoring, agent CI/CD, optimize prompt, improve prompt, optimize agent instructions, agent optimizer, deploy model, Foundry project, RBAC, role assignment, permissions, quota, capacity, region, troubleshoot agent, deployment failure, AI Services, create Foundry resource, provision, knowledge index, customize deployment, onboard, availability, fine-tune, SFT, DPO, RFT, training-data, grader, distillation, fine-tuned model, large file upload. DO NOT USE FOR: Azure Functions, App Service, general Azure deploy (use azure-deploy), general Azure prep (use azure-prepare).

### `minimax-pdf`

- **Path**: `skills/minimax-pdf`
- **SKILL.md**: [`skills/minimax-pdf/SKILL.md`](/skills/minimax-pdf/SKILL.md)
- **Title**: minimax-pdf
- **Files**: 12
- **Structure**: scripts
- **License**: MIT
- **Version**: 1.0

> Use this skill when visual quality and design identity matter for a PDF. CREATE (generate from scratch): "make a PDF", "generate a report", "write a proposal", "create a resume", "beautiful PDF", "professional document", "cover page", "polished PDF", "client-ready document". FILL (complete form fields): "fill in the form", "fill out this PDF", "complete the form fields", "write values into PDF", "what fields does this PDF have". REFORMAT (apply design to an existing doc): "reformat this document", "apply our style", "convert this Markdown/text to PDF", "make this doc look good", "re-style this PDF". This skill uses a token-based design system: color, typography, and spacing are derived from the document type and flow through every page. The output is print-ready. Prefer this skill when appearance matters, not just when any PDF output is needed.

### `minimax-xlsx`

- **Path**: `skills/minimax-xlsx`
- **SKILL.md**: [`skills/minimax-xlsx/SKILL.md`](/skills/minimax-xlsx/SKILL.md)
- **Title**: MiniMax XLSX Skill
- **Files**: 25
- **Structure**: references, scripts, templates
- **License**: MIT
- **Version**: 1.0
- **Flags**: `METADATA_NON_STRING`

> Open, create, read, analyze, edit, or validate Excel/spreadsheet files (.xlsx, .xlsm, .csv, .tsv). Use when the user asks to create, build, modify, analyze, read, validate, or format any Excel spreadsheet, financial model, pivot table, or tabular data file. Covers: creating new xlsx from scratch, reading and analyzing existing files, editing existing xlsx with zero format loss, formula recalculation and validation, and applying professional financial formatting standards. Triggers on 'spreadsheet', 'Excel', '.xlsx', '.csv', 'pivot table', 'financial model', 'formula', or any request to produce tabular data in Excel format.

### `tts`

- **Path**: `skills/tts`
- **SKILL.md**: [`skills/tts/SKILL.md`](/skills/tts/SKILL.md)
- **Title**: TTS (Text to Speech) Skill
- **Files**: 3
- **Structure**: flat
- **License**: MIT
- **Flags**: `BODY_LENGTH`

> Implement text-to-speech (TTS) capabilities using the z-ai-web-dev-sdk. Use this skill when the user needs to convert text into natural-sounding speech, create audio content, build voice-enabled applications, or generate spoken audio files. Supports multiple voices, adjustable speed, and various audio formats.

### `vlm`

- **Path**: `skills/vlm`
- **SKILL.md**: [`skills/vlm/SKILL.md`](/skills/vlm/SKILL.md)
- **Title**: VLM(Vision Chat) Skill
- **Files**: 3
- **Structure**: scripts
- **License**: MIT
- **Flags**: `BODY_LENGTH`

> Implement vision-based AI chat capabilities using the z-ai-web-dev-sdk. Use this skill when the user needs to analyze images, describe visual content, or create applications that combine image understanding with conversational AI. Supports image URLs and base64 encoded images for multimodal interactions.

### `web-reader`

- **Path**: `skills/web-reader`
- **SKILL.md**: [`skills/web-reader/SKILL.md`](/skills/web-reader/SKILL.md)
- **Title**: Web Reader Skill
- **Files**: 3
- **Structure**: scripts
- **License**: MIT
- **Flags**: `BODY_LENGTH`

> Implement web page content extraction capabilities using the z-ai-web-dev-sdk. Use this skill when the user needs to scrape web pages, extract article content, retrieve page metadata, or build applications that process web content. Supports automatic content extraction with title, HTML, and publication time retrieval.

### `web-search`

- **Path**: `skills/web-search`
- **SKILL.md**: [`skills/web-search/SKILL.md`](/skills/web-search/SKILL.md)
- **Title**: Web Search Skill
- **Files**: 3
- **Structure**: scripts
- **License**: MIT
- **Flags**: `BODY_LENGTH`

> Implement web search capabilities using the z-ai-web-dev-sdk. Use this skill when the user needs to search for real-time information from the web, retrieve up-to-date content beyond the knowledge cutoff, or find the latest news and data. Returns structured search results with URLs, snippets, and metadata.

## 5. Testing, QA & Performance

> **39 skills** in this category.

### `animation-performance`

- **Path**: `skills/animation-performance`
- **SKILL.md**: [`skills/animation-performance/SKILL.md`](/skills/animation-performance/SKILL.md)
- **Title**: Animation Performance
- **Files**: 1
- **Structure**: flat

> Keep web animations inside the frame budget — animate composite-only properties, keep motion off the main thread when the page is busy, and find the cause when an animation drops frames. Covers the layout/paint/composite pipeline, cheaper property swaps, CSS vs WAAPI vs requestAnimationFrame, Framer Motion's hardware-accelerated path, React re-rendering per frame, inherited CSS variable recalculation, blur cost, and when `will-change` actually helps. Use when an animation is janky, choppy, stutters, or drops frames; when choosing which property to animate; when deciding between CSS and JS animation on performance grounds; or when reaching for `will-change` or GPU layers. For choosing easing, duration, or whether to animate at all use animate; for reviewing motion as a whole use review-animations.

### `before-and-after`

- **Path**: `skills/before-and-after`
- **SKILL.md**: [`skills/before-and-after/SKILL.md`](/skills/before-and-after/SKILL.md)
- **Title**: Before-After Screenshot Skill
- **Files**: 7
- **Structure**: scripts
- **Flags**: `ALLOWED_TOOLS_LIST`

> Captures before/after screenshots of web pages or elements for visual comparison. Use when user says "take before and after", "screenshot comparison", "visual diff", "PR screenshots", "compare old and new", or needs to document UI changes. Accepts two URLs (file://, http://, https://) or two image paths.

### `benchmark-checklist`

- **Path**: `skills/benchmark-checklist`
- **SKILL.md**: [`skills/benchmark-checklist/SKILL.md`](/skills/benchmark-checklist/SKILL.md)
- **Title**: Benchmark checklist
- **Files**: 1
- **Structure**: flat

> Vet a perf measurement (limiter, tuning, limits, errors, repeatability, relevance, and whether the work happened) before you report or act on it. Use when you run a benchmark or report a speedup or regression you measured.

### `break-ui`

- **Path**: `skills/break-ui`
- **SKILL.md**: [`skills/break-ui/SKILL.md`](/skills/break-ui/SKILL.md)
- **Title**: Breaking UI
- **Files**: 2
- **Structure**: flat

> Try to break a piece of UI by feeding it worst-case data — long names, unbreakable emails, one-letter names, missing fields, huge counts, zero items, long labels, non-Latin text, emoji, extreme numbers — then render it behind a "Demo data / Worst case" toggle and report everything that broke, with the fix for each. Use when the user asks to stress-test, break, or find edge cases in a component or screen, or to "try the worst case". For visual design critique use emil-design-eng; for motion use review-animations.

### `browser-testing-with-devtools`

- **Path**: `skills/browser-testing-with-devtools`
- **SKILL.md**: [`skills/browser-testing-with-devtools/SKILL.md`](/skills/browser-testing-with-devtools/SKILL.md)
- **Title**: Browser Testing with DevTools
- **Files**: 1
- **Structure**: flat

> Tests in real browsers. Use when building or debugging anything that runs in a browser. Use when you need to inspect the DOM, capture console errors, analyze network requests, profile performance, or verify visual output with real runtime data via Chrome DevTools MCP.

### `chrome-devtools-mcp`

- **Path**: `skills/chrome-devtools-mcp`
- **SKILL.md**: [`skills/chrome-devtools-mcp/SKILL.md`](/skills/chrome-devtools-mcp/SKILL.md)
- **Title**: chrome-devtools-mcp
- **Files**: 1
- **Structure**: flat

> Google-official MCP server providing full Chrome DevTools Protocol access (29 tools). Use for Lighthouse audits, performance traces, network inspection, console log access, JavaScript evaluation, mobile emulation, and memory snapshots.

### `ci-cd-and-automation`

- **Path**: `skills/ci-cd-and-automation`
- **SKILL.md**: [`skills/ci-cd-and-automation/SKILL.md`](/skills/ci-cd-and-automation/SKILL.md)
- **Title**: CI/CD and Automation
- **Files**: 1
- **Structure**: flat

> Automates CI/CD pipeline setup. Use when setting up or modifying build and deployment pipelines. Use when you need to automate quality gates, configure test runners in CI, or establish deployment strategies.

### `code-review`

- **Path**: `skills/code-review`
- **SKILL.md**: [`skills/code-review/SKILL.md`](/skills/code-review/SKILL.md)
- **Title**: code-review
- **Files**: 2
- **Structure**: flat

> Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes: Standards (does the code follow this repo's documented coding standards?) and Spec (does the code match what the originating issue/spec asked for?). Runs both reviews in parallel sub-agents and reports them side by side. Use when the user wants to review a branch, a PR, work-in-progress changes, or asks to "review since X".

### `code-review-checklist`

- **Path**: `skills/code-review-checklist`
- **SKILL.md**: [`skills/code-review-checklist/SKILL.md`](/skills/code-review-checklist/SKILL.md)
- **Title**: Code Review Checklist
- **Files**: 1
- **Structure**: flat
- **Version**: 2.0.0
- **Flags**: `UNKNOWN_KEYS`

> Lightweight quick-reference checklist for code review. Tactical 12-category scan used by the Orchestrator's Phase 3. For the comprehensive quality constitution (Six-Axis review), see `code-quality-standards`. For verification gates and the Iron Law, see `verification-and-review-protocol`.

### `coding-agent`

- **Path**: `skills/coding-agent`
- **SKILL.md**: [`skills/coding-agent/SKILL.md`](/skills/coding-agent/SKILL.md)
- **Title**: coding-agent
- **Files**: 8
- **Structure**: flat
- **Version**: 1.0.4
- **Flags**: `METADATA_NON_STRING`, `UNKNOWN_KEYS`

> Coding workflow with planning, implementation, verification, and testing for clean software development.

### `content-strategy`

- **Path**: `skills/content-strategy`
- **SKILL.md**: [`skills/content-strategy/SKILL.md`](/skills/content-strategy/SKILL.md)
- **Title**: Content Strategy
- **Files**: 2
- **Structure**: flat

> Build and execute a content marketing strategy for a solopreneur business. Use when planning what content to create, deciding on content formats and channels, building a content calendar, measuring content performance, or systematizing content production. Covers audience research for content, content pillars, distribution strategy, repurposing workflows, and metrics. Trigger on "content strategy", "content marketing", "what content should I create", "content plan", "content calendar", "content ideas", "content distribution", "grow through content".

### `context-engineering`

- **Path**: `skills/context-engineering`
- **SKILL.md**: [`skills/context-engineering/SKILL.md`](/skills/context-engineering/SKILL.md)
- **Title**: Context Engineering
- **Files**: 1
- **Structure**: flat

> Optimizes agent context setup. Use when starting a new session, when agent output quality degrades, when switching between tasks, or when you need to configure rules files and context for a project.

### `context7-mcp`

- **Path**: `skills/context7-mcp`
- **SKILL.md**: [`skills/context7-mcp/SKILL.md`](/skills/context7-mcp/SKILL.md)
- **Title**: Context7 MCP/API Document Lookup
- **Files**: 1
- **Structure**: flat

> Programmatic document lookup via Context7 API and MCP server. Use when: (1) Need structured documentation for any library/package/framework, (2) Want code examples without browser automation, (3) Building with specific tools and need accurate API references, (4) Avoiding hallucinated or outdated docs. Priority: API (fastest) → MCP Server → Browser (fallback) Triggers: "lookup docs for", "get Context7 docs", "find documentation", "API reference for", "code examples for [library]"

### `create-verification-skill`

- **Path**: `skills/create-verification-skill`
- **SKILL.md**: [`skills/create-verification-skill/SKILL.md`](/skills/create-verification-skill/SKILL.md)
- **Title**: Create a verification skill
- **Files**: 4
- **Structure**: references

> Generate a project-local verification skill that drives your app the way a user does — any language, framework, or platform. Use for /create-verification-skill, "make a control skill for this repo", "make a driver skill for this repo", or when a project has no scripted way to prove UI/CLI/service behavior.

### `debugging-and-error-recovery`

- **Path**: `skills/debugging-and-error-recovery`
- **SKILL.md**: [`skills/debugging-and-error-recovery/SKILL.md`](/skills/debugging-and-error-recovery/SKILL.md)
- **Title**: Debugging and Error Recovery
- **Files**: 1
- **Structure**: flat

> Guides systematic root-cause debugging. Use when tests fail, builds break, behavior doesn't match expectations, or you encounter any unexpected error. Use when you need a systematic approach to finding and fixing the root cause rather than guessing.

### `diagnosing-bugs`

- **Path**: `skills/diagnosing-bugs`
- **SKILL.md**: [`skills/diagnosing-bugs/SKILL.md`](/skills/diagnosing-bugs/SKILL.md)
- **Title**: Diagnosing Bugs
- **Files**: 3
- **Structure**: scripts

> Diagnosis loop for hard bugs and performance regressions. Use when the user says "diagnose"/"debug this", or reports something broken/throwing/failing/slow.

### `e2e-testing-lessons`

- **Path**: `skills/e2e-testing-lessons`
- **SKILL.md**: [`skills/e2e-testing-lessons/SKILL.md`](/skills/e2e-testing-lessons/SKILL.md)
- **Title**: E2E Testing Lessons Learned
- **Files**: 1
- **Structure**: flat

> Condensed experience from 15-phase E2E testing initiative covering authentication, API contracts, tool selection, and hybrid testing methodology. Use when planning E2E tests, selecting testing tools, or debugging test failures.

### `eval-plan`

- **Path**: `skills/eval-plan`
- **SKILL.md**: [`skills/eval-plan/SKILL.md`](/skills/eval-plan/SKILL.md)
- **Title**: /eval-plan: Preregistered, paid evals
- **Files**: 2
- **Structure**: flat
- **Version**: 1.0.0
- **Flags**: `ALLOWED_TOOLS_LIST`, `UNKNOWN_KEYS`, `BODY_LENGTH`

> Preregister a paid eval (bars, arms, decoys, stop rules), dry-run it at zero cost, then run a three-item priced pilot whose spend table gates approval. (gstack)

### `full-page-screenshot`

- **Path**: `skills/full-page-screenshot`
- **SKILL.md**: [`skills/full-page-screenshot/SKILL.md`](/skills/full-page-screenshot/SKILL.md)
- **Title**: Full-Page Website Screenshot — Quality-Gated Capture Methodology
- **Files**: 6
- **Structure**: scripts
- **Flags**: `UNKNOWN_KEYS`

> Capture pixel-perfect, full-page PNG screenshots of any website, landing page, or web app using the agent-browser CLI, with load verification, lazy-content scroll triggering, and post-capture integrity checks. Use this skill whenever the user asks to screenshot, screen-capture, or snapshot a webpage, save a page/site/landing page as a PNG or image file, document how a rendered page looks, or visually verify a built page — even if they only say "grab the page", "capture the landing page", or "save this site as an image" and never literally say "full page" or "screenshot".

### `improve-animations`

- **Path**: `skills/improve-animations`
- **SKILL.md**: [`skills/improve-animations/SKILL.md`](/skills/improve-animations/SKILL.md)
- **Title**: Improving Animations
- **Files**: 3
- **Structure**: flat

> Survey a codebase's animation and motion code as a senior motion advisor, then produce a prioritized audit and self-contained implementation plans for other agents (or cheaper models) to execute. Read-only on source code — it plans improvements, it does not apply them. Use when the user asks to "improve the animations", "audit the motion", "make this app feel better", or wants a roadmap of animation fixes rather than a review of a single diff.

### `interview-designer`

- **Path**: `skills/interview-designer`
- **SKILL.md**: [`skills/interview-designer/SKILL.md`](/skills/interview-designer/SKILL.md)
- **Title**: Interview Designer Skill
- **Files**: 5
- **Structure**: references, templates

> Analyze resumes and design interview strategies using evidence-based methodology. Transforms interview prep from "read resume → ask questions" into "define standard → forensic evidence → future simulation". Combines Geoff Smart's Topgrading, Lou Adler's performance-based hiring, and Daniel Kahneman's bias control. Use when preparing for interviews, creating structured interview guides, or designing questions to validate candidate competencies.

### `lint-and-validate`

- **Path**: `skills/lint-and-validate`
- **SKILL.md**: [`skills/lint-and-validate/SKILL.md`](/skills/lint-and-validate/SKILL.md)
- **Title**: Lint and Validate Skill
- **Files**: 3
- **Structure**: scripts

> Automatic quality control, linting, and static analysis procedures. Use after every code modification to ensure syntax correctness and project standards. Triggers on keywords: lint, format, check, validate, types, static analysis.

### `pdf`

- **Path**: `skills/pdf`
- **SKILL.md**: [`skills/pdf/SKILL.md`](/skills/pdf/SKILL.md)
- **Title**: PDF - Document Production Workbench
- **Files**: 41
- **Structure**: references, scripts
- **License**: Proprietary. LICENSE.txt has complete terms
- **Author**: Z.AI
- **Version**: 1.0
- **Flags**: `BODY_LENGTH`
- **Duplicate**: essentially identical to `pdf-old-20260806`

> Professional PDF toolkit with four production lines:(1) Report - structured documents via ReportLab (reports, proposals, contracts, white papers); (2) Creative - visual design via JSON Blueprint → design_engine.py → Playwright snapshot (posters, infographics, invitations, dashboards). The LLM acts as Art Director outputting ONLY JSON spatial blueprints; convert.blueprint compiles to pixel-perfect PDF. (3) Academic - scholarly work via LaTeX/Tectonic (papers, theses, math-heavy documents); (4) Process - manipulate existing PDFs (extract, merge, split, fill forms, convert);Auto-routes based on document type. Includes ATS/creative/academic resume sub-paths.

### `performance-optimization`

- **Path**: `skills/performance-optimization`
- **SKILL.md**: [`skills/performance-optimization/SKILL.md`](/skills/performance-optimization/SKILL.md)
- **Title**: Performance Optimization
- **Files**: 1
- **Structure**: flat

> Optimizes application performance. Use when performance requirements exist, when you suspect performance regressions, or when Core Web Vitals or load times need improvement. Use when profiling reveals bottlenecks that need fixing.

### `playwright-cli`

- **Path**: `skills/playwright-cli`
- **SKILL.md**: [`skills/playwright-cli/SKILL.md`](/skills/playwright-cli/SKILL.md)
- **Title**: Browser Automation with playwright-cli
- **Files**: 11
- **Structure**: references
- **Flags**: `BODY_LENGTH`

> Automate browser interactions, test web pages and work with Playwright tests. Is a better choice for traditional browser testing - multi-browser support (Firefox, WebKit), Playwright-native locators, and the run-code command for custom Playwright snippets.

### `principle-explain-the-number`

- **Path**: `skills/principle-explain-the-number`
- **SKILL.md**: [`skills/principle-explain-the-number/SKILL.md`](/skills/principle-explain-the-number/SKILL.md)
- **Title**: Explain the Number
- **Files**: 1
- **Structure**: flat
- **Flags**: `UNKNOWN_KEYS`

> Apply before you trust, report, or act on a number you measured: a speedup, a regression, a throughput, a latency, or an eval result. Find what limits it, and rule out that it measured something other than the work you think.

### `principle-prove-it-works`

- **Path**: `skills/principle-prove-it-works`
- **SKILL.md**: [`skills/principle-prove-it-works/SKILL.md`](/skills/principle-prove-it-works/SKILL.md)
- **Title**: Prove It Works
- **Files**: 1
- **Structure**: flat
- **Flags**: `UNKNOWN_KEYS`

> Apply after completing a task, before declaring done. Verify against the real artifact (run the feature, read the actual value, inspect the diff), not a proxy, self-report, or 'it compiles.'

### `principle-test-behavior-not-implementation`

- **Path**: `skills/principle-test-behavior-not-implementation`
- **SKILL.md**: [`skills/principle-test-behavior-not-implementation/SKILL.md`](/skills/principle-test-behavior-not-implementation/SKILL.md)
- **Title**: Test Behavior, Not Implementation
- **Files**: 1
- **Structure**: flat
- **Flags**: `UNKNOWN_KEYS`

> Apply when you write, change, or keep a test. Assert what the code's users can observe, so that the test fails when that behavior breaks and keeps passing when only the internals change.

### `qa`

- **Path**: `skills/qa`
- **SKILL.md**: [`skills/qa/SKILL.md`](/skills/qa/SKILL.md)
- **Title**: /qa: Test → Fix → Verify
- **Files**: 20
- **Structure**: references, templates
- **Version**: 2.0.0
- **Flags**: `ALLOWED_TOOLS_LIST`, `UNKNOWN_KEYS`, `BODY_LENGTH`

> Fix browser/API/CLI/job/worker/webhook bugs. (gstack)

### `readme-md`

- **Path**: `skills/readme-md`
- **SKILL.md**: [`skills/readme-md/SKILL.md`](/skills/readme-md/SKILL.md)
- **Title**: readme-md
- **Files**: 1
- **Structure**: flat
- **Version**: 1.0.0
- **Flags**: `UNKNOWN_KEYS`

> Creates a professional, high-signal README.md for a repository by investigating the codebase and following battle-tested conventions distilled from production open-source projects.

### `seo-content-writer`

- **Path**: `skills/seo-content-writer`
- **SKILL.md**: [`skills/seo-content-writer/SKILL.md`](/skills/seo-content-writer/SKILL.md)
- **Title**: SEO Content Writer
- **Files**: 4
- **Structure**: references
- **License**: Apache-2.0
- **Author**: aaron-he-zhu
- **Version**: 2.0.0
- **Flags**: `METADATA_NON_STRING`, `BODY_LENGTH`

> Use when the user asks to "write SEO content", "create a blog post", "write an article", "content writing", "draft optimized content", "write me an article", "create a blog post about", "help me write SEO content", or "draft content for". Creates high-quality, SEO-optimized content that ranks in search engines. Applies on-page SEO best practices, keyword optimization, and content structure for maximum visibility and engagement. For AI citation optimization, see geo-content-optimizer. For updating existing content, see content-refresher.

### `skill-creator`

- **Path**: `skills/skill-creator`
- **SKILL.md**: [`skills/skill-creator/SKILL.md`](/skills/skill-creator/SKILL.md)
- **Title**: Skill Creator
- **Files**: 20
- **Structure**: assets, references, scripts
- **License**: Complete terms in LICENSE.txt
- **Duplicate**: essentially identical to `skill-creator-zai`

> Create new skills, modify and improve existing skills, and evaluate skill quality. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, optimize a skill's description for better triggering accuracy, or package a skill for distribution.

### `skill-creator-zai`

- **Path**: `skills/skill-creator-zai`
- **SKILL.md**: [`skills/skill-creator-zai/SKILL.md`](/skills/skill-creator-zai/SKILL.md)
- **Title**: Skill Creator
- **Files**: 17
- **Structure**: assets, references, scripts
- **Duplicate**: essentially identical to `skill-creator`

> Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, or optimize a skill's description for better triggering accuracy.

### `tdd`

- **Path**: `skills/tdd`
- **SKILL.md**: [`skills/tdd/SKILL.md`](/skills/tdd/SKILL.md)
- **Title**: Test-Driven Development
- **Files**: 4
- **Structure**: flat

> Test-driven development. Use when the user wants to build features or fix bugs test-first, mentions "red-green-refactor", or wants integration tests.

### `tdd-workflow`

- **Path**: `skills/tdd-workflow`
- **SKILL.md**: [`skills/tdd-workflow/SKILL.md`](/skills/tdd-workflow/SKILL.md)
- **Title**: TDD Workflow
- **Files**: 1
- **Structure**: flat

> Test-Driven Development workflow principles. RED-GREEN-REFACTOR cycle.

### `test-audit`

- **Path**: `skills/test-audit`
- **SKILL.md**: [`skills/test-audit/SKILL.md`](/skills/test-audit/SKILL.md)
- **Title**: /test-audit: Test value sweep
- **Files**: 2
- **Structure**: flat
- **Version**: 1.0.0
- **Flags**: `ALLOWED_TOOLS_LIST`, `UNKNOWN_KEYS`

> Find low-value or duplicate tests and the test-only code they keep alive. (gstack)

### `test-driven-development`

- **Path**: `skills/test-driven-development`
- **SKILL.md**: [`skills/test-driven-development/SKILL.md`](/skills/test-driven-development/SKILL.md)
- **Title**: Test-Driven Development
- **Files**: 1
- **Structure**: flat

> Drives development with tests. Use when implementing any logic, fixing any bug, or changing any behavior. Use when you need to prove that code works, when a bug report arrives, or when you're about to modify existing functionality.

### `testing-patterns`

- **Path**: `skills/testing-patterns`
- **SKILL.md**: [`skills/testing-patterns/SKILL.md`](/skills/testing-patterns/SKILL.md)
- **Title**: Testing Patterns
- **Files**: 2
- **Structure**: scripts

> Testing patterns and principles. Unit, integration, mocking strategies.

### `webapp-testing`

- **Path**: `skills/webapp-testing`
- **SKILL.md**: [`skills/webapp-testing/SKILL.md`](/skills/webapp-testing/SKILL.md)
- **Title**: Web App Testing
- **Files**: 7
- **Structure**: examples, scripts

> Web application testing principles. E2E, Playwright, deep audit strategies.

## 6. Code Quality, Security & Architecture

> **54 skills** in this category.

### `anti-pua`

- **Path**: `skills/anti-pua`
- **SKILL.md**: [`skills/anti-pua/SKILL.md`](/skills/anti-pua/SKILL.md)
- **Title**: 反PUA大师 - 情感操纵识别与心理分析
- **Files**: 1
- **Structure**: flat

> 识别和分析PUA（Pickup Artist）及情感操纵行为的专业心理分析工具。具备人格分析、心理侧写、情感分析能力，能够识别情感操纵、煤气灯操纵、虐待等有毒关系模式，评估人格特质（如黑暗三人格、脆弱型自恋等），预测对方行为并给出具体的相处建议。当用户需要：分析对方言行动机、识别PUA/情感操纵行为、评估NPD（自恋型人格障碍）倾向、识别操纵行为、预测对方未来行为、寻求健康关系建议、分析黑暗三人格或光明三人格时使用此skill。

### `architect`

- **Path**: `skills/architect`
- **SKILL.md**: [`skills/architect/SKILL.md`](/skills/architect/SKILL.md)
- **Title**: Architect
- **Files**: 4
- **Structure**: references

> Sketch types, signatures, and module structure before code, then stay in the loop while implementation fills in. Use for /architect, 'architect this', 'design this', or non-trivial work where jumping to code would lock in the wrong shape.

### `blast-radius`

- **Path**: `skills/blast-radius`
- **SKILL.md**: [`skills/blast-radius/SKILL.md`](/skills/blast-radius/SKILL.md)
- **Title**: Blast radius
- **Files**: 1
- **Structure**: flat

> Find what a change could break somewhere else before it ships, beyond the diff, and prove the one fact it's safe because of by running real code instead of writing it up. Use for 'blast radius of X', 'what could this break', reviewing a small diff you don't trust, or a brief that asserts something about existing code ('make X public', 'X already handles Y') before you design against that assertion.

### `careful`

- **Path**: `skills/careful`
- **SKILL.md**: [`skills/careful/SKILL.md`](/skills/careful/SKILL.md)
- **Title**: /careful — Destructive Command Guardrails
- **Files**: 4
- **Structure**: flat
- **Version**: 0.1.0
- **Flags**: `ALLOWED_TOOLS_LIST`, `UNKNOWN_KEYS`

> Safety guardrails for destructive commands. (gstack)

### `clean-code`

- **Path**: `skills/clean-code`
- **SKILL.md**: [`skills/clean-code/SKILL.md`](/skills/clean-code/SKILL.md)
- **Title**: Clean Code - Pragmatic AI Coding Standards
- **Files**: 1
- **Structure**: flat
- **Version**: 2.0
- **Flags**: `UNKNOWN_KEYS`

> Pragmatic coding standards - concise, direct, no over-engineering, no unnecessary comments

### `code-review-and-audit`

- **Path**: `skills/code-review-and-audit`
- **SKILL.md**: [`skills/code-review-and-audit/SKILL.md`](/skills/code-review-and-audit/SKILL.md)
- **Title**: Code Review & Audit Orchestration Skill
- **Files**: 6
- **Structure**: references, scripts
- **Version**: 2.0.0
- **Flags**: `UNKNOWN_KEYS`, `BODY_LENGTH`

> Unified code review and security audit orchestration skill. Coordinates static analysis, security scanning, code quality checks, test coverage, performance profiling, and expert review into a single tiered pipeline. Use when reviewing code, preparing for release, conducting security audits, or running pre-merge gates. Triggers on: review, audit, code review, security scan, quality gate, pre-merge, checklist, lint, vulnerability.

### `code-simplification`

- **Path**: `skills/code-simplification`
- **SKILL.md**: [`skills/code-simplification/SKILL.md`](/skills/code-simplification/SKILL.md)
- **Title**: Code Simplification
- **Files**: 1
- **Structure**: flat

> Simplifies code for clarity. Use when refactoring code for clarity without changing behavior. Use when code works but is harder to read, maintain, or extend than it should be. Use when reviewing code that has accumulated unnecessary complexity.

### `code-structure`

- **Path**: `skills/code-structure`
- **SKILL.md**: [`skills/code-structure/SKILL.md`](/skills/code-structure/SKILL.md)
- **Title**: Service Layer Architecture
- **Files**: 1
- **Structure**: flat

> Use when multiple workflows duplicate the same operational logic, when deciding what belongs in actions vs shared services, or when refactoring repeated operational blocks across domain flows. Use when adding new features that share mechanics with existing ones.

### `codebase-design`

- **Path**: `skills/codebase-design`
- **SKILL.md**: [`skills/codebase-design/SKILL.md`](/skills/codebase-design/SKILL.md)
- **Title**: Codebase Design
- **Files**: 4
- **Structure**: flat

> Shared vocabulary for designing deep modules. Use when the user wants to design or improve a module's interface, find deepening opportunities, decide where a seam goes, make code more testable or AI-navigable, or when another skill needs the deep-module vocabulary.

### `context-anchor`

- **Path**: `skills/context-anchor`
- **SKILL.md**: [`skills/context-anchor/SKILL.md`](/skills/context-anchor/SKILL.md)
- **Title**: Context Anchor Skill
- **Files**: 6
- **Structure**: scripts
- **Version**: 1.1.0
- **Flags**: `UNKNOWN_KEYS`

> Recover from context compaction by scanning memory files and surfacing where you left off. Use when waking up fresh, after compaction, or when you feel lost about what you were doing. Now supports both flat (YYYY-MM-DD.md) and QMD hierarchical (daily/YYYY/MM/DD.md) memory structures.

### `correct`

- **Path**: `skills/correct`
- **SKILL.md**: [`skills/correct/SKILL.md`](/skills/correct/SKILL.md)
- **Title**: Correct
- **Files**: 1
- **Structure**: flat

> Find the mistakes agents keep repeating in this repo and make each one impossible. Try architecture first, then types, then a lint whose error names the fix, then a test, and write docs last. Prove each check fails on a real past mistake. Repeat this each time the operator corrects you. Use for /correct.

### `cso`

- **Path**: `skills/cso`
- **SKILL.md**: [`skills/cso/SKILL.md`](/skills/cso/SKILL.md)
- **Title**: /cso — evidence before assurance
- **Files**: 6
- **Structure**: flat
- **Version**: 3.0.0
- **Flags**: `ALLOWED_TOOLS_LIST`, `UNKNOWN_KEYS`

> Security audit: supported static findings; qualified profiles add reproduction and repair candidates. (gstack)

### `deprecation-and-migration`

- **Path**: `skills/deprecation-and-migration`
- **SKILL.md**: [`skills/deprecation-and-migration/SKILL.md`](/skills/deprecation-and-migration/SKILL.md)
- **Title**: Deprecation and Migration
- **Files**: 1
- **Structure**: flat

> Manages deprecation and migration. Use when removing old systems, APIs, or features. Use when migrating users from one implementation to another. Use when deciding whether to maintain or sunset existing code.

### `deslop`

- **Path**: `skills/deslop`
- **SKILL.md**: [`skills/deslop/SKILL.md`](/skills/deslop/SKILL.md)
- **Title**: Remove AI code slop
- **Files**: 1
- **Structure**: flat

> Remove AI-generated code slop and clean up code style

### `deslop-shared-libs`

- **Path**: `skills/deslop-shared-libs`
- **SKILL.md**: [`skills/deslop-shared-libs/SKILL.md`](/skills/deslop-shared-libs/SKILL.md)
- **Title**: Find code worth sharing
- **Files**: 2
- **Structure**: flat
- **Version**: 1.0.0
- **Flags**: `ALLOWED_TOOLS_LIST`, `UNKNOWN_KEYS`

> Find worthwhile shared-code extractions in recent work. (gstack)

### `devex-review`

- **Path**: `skills/devex-review`
- **SKILL.md**: [`skills/devex-review/SKILL.md`](/skills/devex-review/SKILL.md)
- **Title**: /devex-review: Live Developer Experience Audit
- **Files**: 2
- **Structure**: flat
- **Version**: 1.0.0
- **Flags**: `ALLOWED_TOOLS_LIST`, `UNKNOWN_KEYS`, `BODY_LENGTH`

> Live developer experience audit. (gstack)

### `distill-codebase-skill`

- **Path**: `skills/distill-codebase-skill`
- **SKILL.md**: [`skills/distill-codebase-skill/SKILL.md`](/skills/distill-codebase-skill/SKILL.md)
- **Title**: This is just a reference template for distilling the knowledge and expertise and experiences after completing updating a project codebase
- **Files**: 1
- **Structure**: flat

> Reference template for distilling codebase knowledge into a comprehensive engineering skill document. Use after completing a major project update, security remediation, or architectural overhaul to create a reusable SKILL.md that captures lessons learned, anti-patterns, debugging guides, and best practices for future agents.

### `encrypt-decrypt`

- **Path**: `skills/encrypt-decrypt`
- **SKILL.md**: [`skills/encrypt-decrypt/SKILL.md`](/skills/encrypt-decrypt/SKILL.md)
- **Title**: Output: report.pdf.enc (original unchanged)
- **Files**: 6
- **Structure**: references, scripts
- **Version**: 1.2
- **Flags**: `UNKNOWN_KEYS`

> Encrypt and decrypt files and folders from the CLI. Single-file Python script using AES-256-GCM with Scrypt key derivation. Supports recursive folder processing, atomic writes, authenticated streaming for large files, and non-destructive defaults.

### `freeze`

- **Path**: `skills/freeze`
- **SKILL.md**: [`skills/freeze/SKILL.md`](/skills/freeze/SKILL.md)
- **Title**: /freeze — Restrict Edits to a Directory
- **Files**: 4
- **Structure**: flat
- **Version**: 0.1.0
- **Flags**: `ALLOWED_TOOLS_LIST`, `UNKNOWN_KEYS`

> Restrict file edits to a specific directory for the session. (gstack)

### `greploop`

- **Path**: `skills/greploop`
- **SKILL.md**: [`skills/greploop/SKILL.md`](/skills/greploop/SKILL.md)
- **Title**: Greploop
- **Files**: 4
- **Structure**: references
- **License**: MIT
- **Author**: greptileai
- **Version**: 1.3
- **Duplicate**: essentially identical to `greploop-apps`

> Iteratively improves a PR (GitHub), MR (GitLab), or shelved changelist (Perforce) until Greptile gives it a 5/5 confidence score with zero unresolved comments. Triggers Greptile review, fixes all actionable comments, pushes/re-shelves, re-triggers review, and repeats. Use when the user wants to fully optimize a PR/MR/CL against Greptile's code review standards.

### `greploop-apps`

- **Path**: `skills/greploop-apps`
- **SKILL.md**: [`skills/greploop-apps/SKILL.md`](/skills/greploop-apps/SKILL.md)
- **Title**: Greploop Apps
- **Files**: 4
- **Structure**: references
- **License**: MIT
- **Author**: greptileai
- **Version**: 1.3
- **Duplicate**: essentially identical to `greploop`

> Iteratively improves a PR (GitHub), MR (GitLab), or shelved changelist (Perforce) until Greptile gives it a 5/5 confidence score with zero unresolved comments. Identical to greploop, but triggers reviews by tagging @greptile-apps, which bypasses Greptile's file-count limit on huge PRs that the plain @greptile mention refuses to review. Use when the user wants to fully optimize a large PR/MR/CL against Greptile's code review standards.

### `guard`

- **Path**: `skills/guard`
- **SKILL.md**: [`skills/guard/SKILL.md`](/skills/guard/SKILL.md)
- **Title**: /guard — Full Safety Mode
- **Files**: 2
- **Structure**: flat
- **Version**: 0.1.0
- **Flags**: `ALLOWED_TOOLS_LIST`, `UNKNOWN_KEYS`

> Full safety mode: destructive command warnings + directory-scoped edits. (gstack)

### `how`

- **Path**: `skills/how`
- **SKILL.md**: [`skills/how/SKILL.md`](/skills/how/SKILL.md)
- **Title**: How
- **Files**: 3
- **Structure**: references

> Use for "how does X work", code walkthroughs before changing something, and placement / ownership / layering questions ("where should this live", "which package owns this", "is this the right layer"). Explains subsystem architecture, runtime flow, onboarding mental models. Use why for motivation.

### `improve-codebase-architecture`

- **Path**: `skills/improve-codebase-architecture`
- **SKILL.md**: [`skills/improve-codebase-architecture/SKILL.md`](/skills/improve-codebase-architecture/SKILL.md)
- **Title**: Improve Codebase Architecture
- **Files**: 3
- **Structure**: flat
- **Flags**: `UNKNOWN_KEYS`

> Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick.

### `incremental-implementation`

- **Path**: `skills/incremental-implementation`
- **SKILL.md**: [`skills/incremental-implementation/SKILL.md`](/skills/incremental-implementation/SKILL.md)
- **Title**: Incremental Implementation
- **Files**: 1
- **Structure**: flat

> Delivers changes incrementally. Use when implementing any feature or change that touches more than one file. Use when you're about to write a large amount of code at once, or when a task feels too big to land in one step.

### `investigate`

- **Path**: `skills/investigate`
- **SKILL.md**: [`skills/investigate/SKILL.md`](/skills/investigate/SKILL.md)
- **Title**: Systematic Debugging
- **Files**: 13
- **Structure**: flat
- **Version**: 1.0.0
- **Flags**: `ALLOWED_TOOLS_LIST`, `UNKNOWN_KEYS`, `BODY_LENGTH`

> Systematic debugging with root cause investigation. (gstack)

### `memory-architect`

- **Path**: `skills/memory-architect`
- **SKILL.md**: [`skills/memory-architect/SKILL.md`](/skills/memory-architect/SKILL.md)
- **Title**: Memory Architect
- **Files**: 8
- **Structure**: assets, references, scripts

> Bootstrap, audit, and recover the OpenClaw 3-layer memory architecture (workspace files, LCM database, QMD semantic index). Use when: (1) Setting up memory on a new OpenClaw instance, (2) Auditing existing memory health, (3) Recovering from corruption or system crash, (4) Migrating or restructuring memory layout, (5) User asks about memory architecture setup or health. Triggers on phrases like 'bootstrap memory', 'audit memory', 'memory architecture', 'memory setup', 'LCM configuration', 'QMD setup', 'memory recovery', 'check memory health'.

### `memory-architecture`

- **Path**: `skills/memory-architecture`
- **SKILL.md**: [`skills/memory-architecture/SKILL.md`](/skills/memory-architecture/SKILL.md)
- **Title**: OpenClaw Memory Architecture
- **Files**: 2
- **Structure**: flat
- **Author**: trusty-pal
- **Version**: 1.0.0
- **Flags**: `UNKNOWN_KEYS`, `BODY_LENGTH`

> OpenClaw memory system architecture, setup guide, and troubleshooting reference. Use when configuring memory on a new machine, diagnosing memory issues after updates, or understanding how workspace files, LCM, and QMD work together.

### `migrate-to-shoehorn`

- **Path**: `skills/migrate-to-shoehorn`
- **SKILL.md**: [`skills/migrate-to-shoehorn/SKILL.md`](/skills/migrate-to-shoehorn/SKILL.md)
- **Title**: Migrate to Shoehorn
- **Files**: 2
- **Structure**: flat

> Migrate test files from `as` type assertions to @total-typescript/shoehorn. Use when user mentions shoehorn, wants to replace `as` in tests, or needs partial test data.

### `plan-writing`

- **Path**: `skills/plan-writing`
- **SKILL.md**: [`skills/plan-writing/SKILL.md`](/skills/plan-writing/SKILL.md)
- **Title**: Plan Writing
- **Files**: 1
- **Structure**: flat

> Structured task planning with clear breakdowns, dependencies, and verification criteria. Use when implementing features, refactoring, or any multi-step work.

### `ponytail`

- **Path**: `skills/ponytail`
- **SKILL.md**: [`skills/ponytail/SKILL.md`](/skills/ponytail/SKILL.md)
- **Title**: Senior Dev Key Rules / Instructions
- **Files**: 1
- **Structure**: flat
- **Version**: 1.0
- **Flags**: `UNKNOWN_KEYS`, `BODY_LENGTH`

> Minimalism-as-discipline coding methodology: understand the task and real flow first, then climb an ordered implementation ladder (skip speculative need → reuse → stdlib → platform features → installed deps → minimum working code) for the shortest correct diff. Enforces YAGNI and no unrequested abstractions — prefer deletion over addition and boring over clever code. Bug fixes target root cause, not symptom. Mark deliberate shortcuts with a ponytail comment naming the ceiling and upgrade path. Non-trivial logic leaves a minimal runnable self-check; no heavy test frameworks unless requested. Hard safety rails: never simplify away input validation, data-loss error handling, security, or accessibility basics. Supports lite, full (default), and ultra intensity modes. Use when writing or refactoring code, fixing bugs, reviewing patches for over-engineering, minimizing diffs, or choosing stdlib vs new dependencies. Triggers on: minimal code, shortest diff, YAGNI, over-engineering, root cause, simplify.

### `principle-attack-the-premise`

- **Path**: `skills/principle-attack-the-premise`
- **SKILL.md**: [`skills/principle-attack-the-premise/SKILL.md`](/skills/principle-attack-the-premise/SKILL.md)
- **Title**: Attack the Premise
- **Files**: 1
- **Structure**: flat
- **Flags**: `UNKNOWN_KEYS`

> Apply when two or more fixes that share one premise have failed the same gate. Write the premise down and test it directly before you write another fix that assumes it.

### `principle-boundary-discipline`

- **Path**: `skills/principle-boundary-discipline`
- **SKILL.md**: [`skills/principle-boundary-discipline/SKILL.md`](/skills/principle-boundary-discipline/SKILL.md)
- **Title**: Boundary Discipline
- **Files**: 1
- **Structure**: flat
- **Flags**: `UNKNOWN_KEYS`

> Apply when wiring validation, error handling, or framework adapters. Concentrate guards at system boundaries (CLI, config, network, external APIs); trust internal types and keep business logic in pure functions.

### `principle-build-the-lever`

- **Path**: `skills/principle-build-the-lever`
- **SKILL.md**: [`skills/principle-build-the-lever/SKILL.md`](/skills/principle-build-the-lever/SKILL.md)
- **Title**: Build the Lever
- **Files**: 1
- **Structure**: flat
- **Flags**: `UNKNOWN_KEYS`

> Apply to any non-trivial work, not just bulk work: edits, migrations, analyses, checks. Build the tool that does it or proves it (codemod, script, generator, or a skill your subagents follow) instead of working by hand. The tool is the artifact a reviewer can rerun.

### `principle-fix-root-causes`

- **Path**: `skills/principle-fix-root-causes`
- **SKILL.md**: [`skills/principle-fix-root-causes/SKILL.md`](/skills/principle-fix-root-causes/SKILL.md)
- **Title**: Fix Root Causes
- **Files**: 1
- **Structure**: flat
- **Flags**: `UNKNOWN_KEYS`

> Apply when debugging. Trace each symptom back to the first place the system went wrong and fix it there. A guard is a fix only when the state it handles is legitimate.

### `principle-foundational-thinking`

- **Path**: `skills/principle-foundational-thinking`
- **SKILL.md**: [`skills/principle-foundational-thinking/SKILL.md`](/skills/principle-foundational-thinking/SKILL.md)
- **Title**: Foundational Thinking
- **Files**: 1
- **Structure**: flat
- **Flags**: `UNKNOWN_KEYS`

> Apply before writing logic: choosing core types and data structures, sequencing scaffold-vs-feature work, asking what concurrent actors share. Get the data structures right so downstream code becomes obvious.

### `principle-guard-the-context-window`

- **Path**: `skills/principle-guard-the-context-window`
- **SKILL.md**: [`skills/principle-guard-the-context-window/SKILL.md`](/skills/principle-guard-the-context-window/SKILL.md)
- **Title**: Guard the Context Window
- **Files**: 1
- **Structure**: flat
- **Flags**: `UNKNOWN_KEYS`

> Apply when context is filling up: large outputs, long files, repeated reads, fan-out planning. Route bulk to subagents; keep summaries in the main thread, not raw payloads.

### `principle-laziness-protocol`

- **Path**: `skills/principle-laziness-protocol`
- **SKILL.md**: [`skills/principle-laziness-protocol/SKILL.md`](/skills/principle-laziness-protocol/SKILL.md)
- **Title**: Laziness Protocol
- **Files**: 1
- **Structure**: flat
- **Flags**: `UNKNOWN_KEYS`

> Apply when refactoring, evaluating diff size, or tempted to add abstractions, layers, or signal threading. Bias toward deletion and the smallest change that solves the problem.

### `principle-make-operations-idempotent`

- **Path**: `skills/principle-make-operations-idempotent`
- **SKILL.md**: [`skills/principle-make-operations-idempotent/SKILL.md`](/skills/principle-make-operations-idempotent/SKILL.md)
- **Title**: Make Operations Idempotent
- **Files**: 1
- **Structure**: flat
- **Flags**: `UNKNOWN_KEYS`

> Apply when designing commands, lifecycle steps, or processing loops that run amid crashes, restarts, and retries. Converge to the same end state regardless of partial prior runs.

### `principle-minimize-reader-load`

- **Path**: `skills/principle-minimize-reader-load`
- **SKILL.md**: [`skills/principle-minimize-reader-load/SKILL.md`](/skills/principle-minimize-reader-load/SKILL.md)
- **Title**: Minimize Reader Load
- **Files**: 1
- **Structure**: flat
- **Flags**: `UNKNOWN_KEYS`

> Apply when reviewing or shaping code that's hard to trace. Count layers between question and answer, and hidden state in the reader's head; collapse one-caller wrappers and shrink mutable scope.

### `principle-model-the-domain`

- **Path**: `skills/principle-model-the-domain`
- **SKILL.md**: [`skills/principle-model-the-domain/SKILL.md`](/skills/principle-model-the-domain/SKILL.md)
- **Title**: Model the Domain
- **Files**: 1
- **Structure**: flat
- **Flags**: `UNKNOWN_KEYS`

> Apply when writing stateful logic, or when code branches a lot or repeats a shape assumption across files.

### `principle-never-block-on-the-human`

- **Path**: `skills/principle-never-block-on-the-human`
- **SKILL.md**: [`skills/principle-never-block-on-the-human/SKILL.md`](/skills/principle-never-block-on-the-human/SKILL.md)
- **Title**: Never Block on the Human
- **Files**: 1
- **Structure**: flat
- **Flags**: `UNKNOWN_KEYS`

> Apply when tempted to ask 'should I do X?' on reversible work.

### `principle-sequence-verifiable-units`

- **Path**: `skills/principle-sequence-verifiable-units`
- **SKILL.md**: [`skills/principle-sequence-verifiable-units/SKILL.md`](/skills/principle-sequence-verifiable-units/SKILL.md)
- **Title**: Sequence work into verifiable units
- **Files**: 1
- **Structure**: flat
- **Flags**: `UNKNOWN_KEYS`

> Apply to multi-step work (sweeps, migrations, runs of similar edits) and to how you stack commits and PRs. Break work into small units that each end in a verifiable state, check each before the next, and order delivery so the sequence proves itself to a reviewer.

### `principle-subtract-before-you-add`

- **Path**: `skills/principle-subtract-before-you-add`
- **SKILL.md**: [`skills/principle-subtract-before-you-add/SKILL.md`](/skills/principle-subtract-before-you-add/SKILL.md)
- **Title**: Subtract Before You Add
- **Files**: 1
- **Structure**: flat
- **Flags**: `UNKNOWN_KEYS`

> Apply when sequencing an addition, refactor, or rewrite. Remove dead code, redundant validators, and stub references first, then build on the simpler base.

### `review`

- **Path**: `skills/review`
- **SKILL.md**: [`skills/review/SKILL.md`](/skills/review/SKILL.md)
- **Title**: Pre-Landing PR Review
- **Files**: 25
- **Structure**: flat
- **Version**: 1.0.0
- **Flags**: `ALLOWED_TOOLS_LIST`, `UNKNOWN_KEYS`, `BODY_LENGTH`

> Pre-landing PR review. (gstack)

### `review-animations`

- **Path**: `skills/review-animations`
- **SKILL.md**: [`skills/review-animations/SKILL.md`](/skills/review-animations/SKILL.md)
- **Title**: Reviewing Animations
- **Files**: 2
- **Structure**: flat
- **Flags**: `UNKNOWN_KEYS`

> Reviews animation and motion code against a high craft bar derived from Emil Kowalski's design engineering philosophy. Default to flagging; approval is earned.

### `scaffold-exercises`

- **Path**: `skills/scaffold-exercises`
- **SKILL.md**: [`skills/scaffold-exercises/SKILL.md`](/skills/scaffold-exercises/SKILL.md)
- **Title**: Scaffold Exercises
- **Files**: 2
- **Structure**: flat

> Create exercise directory structures with sections, problems, solutions, and explainers that pass linting. Use when user wants to scaffold exercises, create exercise stubs, or set up a new course section.

### `setup-pre-commit`

- **Path**: `skills/setup-pre-commit`
- **SKILL.md**: [`skills/setup-pre-commit/SKILL.md`](/skills/setup-pre-commit/SKILL.md)
- **Title**: Setup Pre-Commit Hooks
- **Files**: 2
- **Structure**: flat

> Set up Husky pre-commit hooks with lint-staged (Prettier), type checking, and tests in the current repo. Use when user wants to add pre-commit hooks, set up Husky, configure lint-staged, or add commit-time formatting/typechecking/testing.

### `setup-ts-deep-modules`

- **Path**: `skills/setup-ts-deep-modules`
- **SKILL.md**: [`skills/setup-ts-deep-modules/SKILL.md`](/skills/setup-ts-deep-modules/SKILL.md)
- **Title**: Setup TS Deep Modules
- **Files**: 3
- **Structure**: flat
- **Flags**: `UNKNOWN_KEYS`

> Wire dependency-cruiser into a TypeScript repo so each package is a deep module, with implementation hidden in subfolders and reachable only through its entry-point files. User-invoked.

### `thermo-nuclear-code-quality-review`

- **Path**: `skills/thermo-nuclear-code-quality-review`
- **SKILL.md**: [`skills/thermo-nuclear-code-quality-review/SKILL.md`](/skills/thermo-nuclear-code-quality-review/SKILL.md)
- **Title**: Thermo-Nuclear Code Quality Review
- **Files**: 1
- **Structure**: flat

> Run an extremely strict maintainability review for abstraction quality, giant files, and spaghetti-condition growth. Use for a thermo-nuclear code quality review, thermonuclear review, deep code quality audit, or especially harsh maintainability review.

### `thermo-nuclear-review`

- **Path**: `skills/thermo-nuclear-review`
- **SKILL.md**: [`skills/thermo-nuclear-review/SKILL.md`](/skills/thermo-nuclear-review/SKILL.md)
- **Title**: Thermo Nuclear Review
- **Files**: 1
- **Structure**: flat

> Comprehensive security and correctness audit of a branch's changes. Use for thermo nuclear, thermonuclear, or deep review requests, or branch/PR diff audits focused on bugs, breaking changes, security issues, devex regressions, and feature-gate leaks.

### `unfreeze`

- **Path**: `skills/unfreeze`
- **SKILL.md**: [`skills/unfreeze/SKILL.md`](/skills/unfreeze/SKILL.md)
- **Title**: /unfreeze — Clear Freeze Boundary
- **Files**: 2
- **Structure**: flat
- **Version**: 0.1.0
- **Flags**: `ALLOWED_TOOLS_LIST`, `UNKNOWN_KEYS`

> Clear the freeze boundary set by /freeze, allowing edits to all directories again. (gstack)

### `vulnerability-scanner`

- **Path**: `skills/vulnerability-scanner`
- **SKILL.md**: [`skills/vulnerability-scanner/SKILL.md`](/skills/vulnerability-scanner/SKILL.md)
- **Title**: Vulnerability Scanner
- **Files**: 3
- **Structure**: scripts

> Advanced vulnerability analysis principles. OWASP 2025, Supply Chain Security, attack surface mapping, risk prioritization.

### `why`

- **Path**: `skills/why`
- **SKILL.md**: [`skills/why/SKILL.md`](/skills/why/SKILL.md)
- **Title**: Why
- **Files**: 13
- **Structure**: references

> Use for 'why does X work this way', 'why we picked Y', design rationale, regressions, postmortems, or data-backed thresholds. Discovers available MCPs and queries each evidence category (source control, issue tracker, long-form docs, real-time chat, infrastructure observability, error tracking, product analytics warehouse) in parallel, then returns a cited read on decisions and tradeoffs. Use how for runtime behavior.

## 7. Planning, Workflow & Project Management

> **54 skills** in this category.

### `ask-matt`

- **Path**: `skills/ask-matt`
- **SKILL.md**: [`skills/ask-matt/SKILL.md`](/skills/ask-matt/SKILL.md)
- **Title**: Ask Matt
- **Files**: 3
- **Structure**: flat
- **Flags**: `UNKNOWN_KEYS`

> Ask which skill or flow fits your situation. A router over the skills in this repo.

### `background-terminals`

- **Path**: `skills/background-terminals`
- **SKILL.md**: [`skills/background-terminals/SKILL.md`](/skills/background-terminals/SKILL.md)
- **Title**: Background Terminals
- **Files**: 1
- **Structure**: flat

> Run and manage long-lived shell commands in background terminals. Use for dev servers, watchers, streaming builds, and other commands that should keep running while the agent continues working.

### `blog-writer`

- **Path**: `skills/blog-writer`
- **SKILL.md**: [`skills/blog-writer/SKILL.md`](/skills/blog-writer/SKILL.md)
- **Title**: Blog Writer
- **Files**: 12
- **Structure**: flat

> This skill should be used when writing blog posts, articles, or long-form content in the writer's distinctive writing style. It produces authentic, opinionated content that matches the writer's voice—direct, conversational, and grounded in personal experience. The skill handles the complete workflow from research review through Notion publication. Use this skill for drafting blog posts, thought leadership pieces, or any writing meant to reflect the writer's perspective on AI, productivity, sales, marketing, or technology topics.

### `chief-of-staff`

- **Path**: `skills/chief-of-staff`
- **SKILL.md**: [`skills/chief-of-staff/SKILL.md`](/skills/chief-of-staff/SKILL.md)
- **Title**: chief-of-staff
- **Files**: 2
- **Structure**: flat
- **Flags**: `UNKNOWN_KEYS`

> Pursue a long-running goal in a single session by co-ordinating subagents.

### `context-restore`

- **Path**: `skills/context-restore`
- **SKILL.md**: [`skills/context-restore/SKILL.md`](/skills/context-restore/SKILL.md)
- **Title**: /context-restore — Restore Saved Working Context
- **Files**: 2
- **Structure**: flat
- **Version**: 1.0.0
- **Flags**: `ALLOWED_TOOLS_LIST`, `UNKNOWN_KEYS`, `BODY_LENGTH`

> Restore working context saved earlier by /context-save. (gstack)

### `context-save`

- **Path**: `skills/context-save`
- **SKILL.md**: [`skills/context-save/SKILL.md`](/skills/context-save/SKILL.md)
- **Title**: /context-save — Save Working Context
- **Files**: 2
- **Structure**: flat
- **Version**: 1.0.0
- **Flags**: `ALLOWED_TOOLS_LIST`, `UNKNOWN_KEYS`, `BODY_LENGTH`

> Save working context. (gstack)

### `documentation-and-adrs`

- **Path**: `skills/documentation-and-adrs`
- **SKILL.md**: [`skills/documentation-and-adrs/SKILL.md`](/skills/documentation-and-adrs/SKILL.md)
- **Title**: Documentation and ADRs
- **Files**: 1
- **Structure**: flat

> Records decisions and documentation. Use when making architectural decisions, changing public APIs, shipping features, or when you need to record context that future engineers and agents will need to understand the codebase.

### `figure-it-out`

- **Path**: `skills/figure-it-out`
- **SKILL.md**: [`skills/figure-it-out/SKILL.md`](/skills/figure-it-out/SKILL.md)
- **Title**: Figure it out
- **Files**: 1
- **Structure**: flat

> Design an auditable playbook when no narrower one fits: a large migration, an ambitious multi-part change, or work a human reviews after stepping away. Scales rigor to the task, runs a hypothesis loop, and logs decisions. Use for /figure-it-out or 'figure it out'.

### `fix-ci`

- **Path**: `skills/fix-ci`
- **SKILL.md**: [`skills/fix-ci/SKILL.md`](/skills/fix-ci/SKILL.md)
- **Title**: Fix CI
- **Files**: 1
- **Structure**: flat

> Find failing PR checks, inspect logs or external check links, and apply focused fixes

### `fix-merge-conflicts`

- **Path**: `skills/fix-merge-conflicts`
- **SKILL.md**: [`skills/fix-merge-conflicts/SKILL.md`](/skills/fix-merge-conflicts/SKILL.md)
- **Title**: Fix merge conflicts
- **Files**: 1
- **Structure**: flat

> Resolve merge conflicts non-interactively, validate build and tests, and finalize conflict resolution

### `get-pr-comments`

- **Path**: `skills/get-pr-comments`
- **SKILL.md**: [`skills/get-pr-comments/SKILL.md`](/skills/get-pr-comments/SKILL.md)
- **Title**: Get PR comments
- **Files**: 1
- **Structure**: flat

> Fetch and summarize review comments from the active pull request

### `git-workflow-and-versioning`

- **Path**: `skills/git-workflow-and-versioning`
- **SKILL.md**: [`skills/git-workflow-and-versioning/SKILL.md`](/skills/git-workflow-and-versioning/SKILL.md)
- **Title**: Git Workflow and Versioning
- **Files**: 1
- **Structure**: flat

> Structures git workflow practices. Use when making any code change. Use when committing, branching, resolving conflicts, or when you need to organize work across multiple parallel streams.

### `grill-me`

- **Path**: `skills/grill-me`
- **SKILL.md**: [`skills/grill-me/SKILL.md`](/skills/grill-me/SKILL.md)
- **Title**: grill-me
- **Files**: 2
- **Structure**: flat
- **Flags**: `UNKNOWN_KEYS`

> A relentless interview to sharpen a plan or design.

### `grill-with-docs`

- **Path**: `skills/grill-with-docs`
- **SKILL.md**: [`skills/grill-with-docs/SKILL.md`](/skills/grill-with-docs/SKILL.md)
- **Title**: grill-with-docs
- **Files**: 2
- **Structure**: flat
- **Flags**: `UNKNOWN_KEYS`

> A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go.

### `grilling`

- **Path**: `skills/grilling`
- **SKILL.md**: [`skills/grilling/SKILL.md`](/skills/grilling/SKILL.md)
- **Title**: grilling
- **Files**: 2
- **Structure**: flat

> Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.

### `implement`

- **Path**: `skills/implement`
- **SKILL.md**: [`skills/implement/SKILL.md`](/skills/implement/SKILL.md)
- **Title**: implement
- **Files**: 2
- **Structure**: flat
- **Flags**: `UNKNOWN_KEYS`

> Implement a piece of work based on a spec or set of tickets.

### `implement-spec`

- **Path**: `skills/implement-spec`
- **SKILL.md**: [`skills/implement-spec/SKILL.md`](/skills/implement-spec/SKILL.md)
- **Title**: implement-spec
- **Files**: 2
- **Structure**: flat
- **Flags**: `UNKNOWN_KEYS`

> Implement the result of /to-spec and /to-tickets in code.

### `interview-prep`

- **Path**: `skills/interview-prep`
- **SKILL.md**: [`skills/interview-prep/SKILL.md`](/skills/interview-prep/SKILL.md)
- **Title**: Interview Prep（面试准备）
- **Files**: 11
- **Structure**: references, scripts

> 帮用户准备面试。基于目标 JD、公司、岗位方向，生成"高频面试题 + 参考回答 + 行为面 / 技术面 / Case 面分类题库"，并产出可打印的『面试备战手册』。当用户说"帮我准备面试""明天有面试 / 后天面试""面试题""面经""模拟面试""我要面 X 公司 Y 岗位""帮我准备 STAR 故事""怎么回答这道面试题""自我介绍 / 离职原因 / 优缺点 怎么答"，必须触发本 skill。请勿用本 skill 改简历（去 jd-resume-tailor / resume-builder）或推荐方向（去 job-intent-tracker）。

### `job-intent-tracker`

- **Path**: `skills/job-intent-tracker`
- **SKILL.md**: [`skills/job-intent-tracker/SKILL.md`](/skills/job-intent-tracker/SKILL.md)
- **Title**: Job Intent Tracker（求职意向 + 岗位追踪）
- **Files**: 8
- **Structure**: references, scripts

> 帮助用户梳理求职意向、生成目标岗位画像，并维护一份结构化的"岗位投递追踪表"。当用户说"我想换工作 / 不知道投什么岗 / 帮我看看我适合什么岗位 / 帮我管理投递进度 / 我投了好几家但记不住状态了 / 想做一个求职 OKR / 整理一下求职方向"，或上传简历但没说要改简历时，应该主动触发本 skill。本 skill 也适用于实习生、应届生、转行候选人在求职启动阶段做"自我盘点 + 目标画像 + 投递管理"三件事。

### `learn`

- **Path**: `skills/learn`
- **SKILL.md**: [`skills/learn/SKILL.md`](/skills/learn/SKILL.md)
- **Title**: Project Learnings Manager
- **Files**: 2
- **Structure**: flat
- **Version**: 1.0.0
- **Flags**: `ALLOWED_TOOLS_LIST`, `UNKNOWN_KEYS`, `BODY_LENGTH`

> Manage project learnings.

### `loop-builder`

- **Path**: `skills/loop-builder`
- **SKILL.md**: [`skills/loop-builder/SKILL.md`](/skills/loop-builder/SKILL.md)
- **Title**: Loop Builder
- **Files**: 75
- **Structure**: references, scripts

> Design and scaffold an agent "loop" — an unattended, scheduled, self-verifying agent workflow. Use this whenever the user wants to automate a recurring task, schedule an agent, run an agent unattended or overnight, set up monitoring, triage, or alerting, poll something on a cadence, or turn a manual repeated workflow into a self-running one — even if they never say the word "loop." If a request implies "do this every day / on a schedule / until some condition holds, without me typing each time," reach for this skill. It walks the seven-question blueprint, picks the simplest loop pattern, and scaffolds the six building blocks (schedule, isolation, skill, connectors, verifier, state) with a human-gate list and a budget.

### `make-pr-easy-to-review`

- **Path**: `skills/make-pr-easy-to-review`
- **SKILL.md**: [`skills/make-pr-easy-to-review/SKILL.md`](/skills/make-pr-easy-to-review/SKILL.md)
- **Title**: Make PR Easy to Review
- **Files**: 1
- **Structure**: flat

> Prepare PRs for review by cleaning noisy history, improving PR descriptions, and adding reviewer guidance without changing code behavior. Use for "make this easy to review", "tidy this PR", "clean up commits", or "annotate the diff".

### `marketing-mode`

- **Path**: `skills/marketing-mode`
- **SKILL.md**: [`skills/marketing-mode/SKILL.md`](/skills/marketing-mode/SKILL.md)
- **Title**: Marketing Mode - Complete Marketing Knowledge Base
- **Files**: 5
- **Structure**: flat
- **Version**: 1.0.0
- **Flags**: `METADATA_NON_STRING`, `BODY_LENGTH`

> Marketing Mode combines 23 comprehensive marketing skills covering strategy, psychology, content, SEO, conversion optimization, and paid growth. Use when users need marketing strategy, copywriting, SEO help, conversion optimization, paid advertising, or any marketing tactic.

### `mindfulness-meditation`

- **Path**: `skills/mindfulness-meditation`
- **SKILL.md**: [`skills/mindfulness-meditation/SKILL.md`](/skills/mindfulness-meditation/SKILL.md)
- **Title**: Mindfulness & Meditation
- **Files**: 2
- **Structure**: flat
- **Author**: clawd-team
- **Version**: 1.0.0
- **Flags**: `UNKNOWN_KEYS`

> Build a meditation practice with guided sessions, streaks, and mindfulness reminders

### `new-feature`

- **Path**: `skills/new-feature`
- **SKILL.md**: [`skills/new-feature/SKILL.md`](/skills/new-feature/SKILL.md)
- **Title**: New Feature
- **Files**: 1
- **Structure**: flat

> Start a new task in an isolated Git worktree branched from origin/main so multiple agents can work on the same repo in parallel without conflicts. Use at the beginning of every new feature, fix, or task — before writing any code.

### `office-hours`

- **Path**: `skills/office-hours`
- **SKILL.md**: [`skills/office-hours/SKILL.md`](/skills/office-hours/SKILL.md)
- **Title**: YC Office Hours
- **Files**: 9
- **Structure**: flat
- **Version**: 2.0.0
- **Flags**: `ALLOWED_TOOLS_LIST`, `UNKNOWN_KEYS`, `BODY_LENGTH`

> YC Office Hours — two modes. (gstack)

### `orchestrator-toolkit`

- **Path**: `skills/orchestrator-toolkit`
- **SKILL.md**: [`skills/orchestrator-toolkit/SKILL.md`](/skills/orchestrator-toolkit/SKILL.md)
- **Title**: Orchestrator Toolkit Skill
- **Files**: 1
- **Structure**: flat

> Pure-Python orchestration toolkit for task management, complexity analysis, decomposition, persistence, and recovery. Use when breaking down complex projects, tracking progress, or building lightweight orchestration systems.

### `pandoc-docx-template`

- **Path**: `skills/pandoc-docx-template`
- **SKILL.md**: [`skills/pandoc-docx-template/SKILL.md`](/skills/pandoc-docx-template/SKILL.md)
- **Title**: Pandoc DOCX Template
- **Files**: 12
- **Structure**: scripts

> Use this skill when converting Markdown to Word DOCX or DOCX back to Markdown with Pandoc, especially when the output should use the bundled Chinese Word reference templates, heading numbering variants, list indentation variants, SCI paper templates, and Lua filters for HTML tags, image captions, font color, and inline code styles.

### `pi-agent-customize-system-prompt`

- **Path**: `skills/pi-agent-customize-system-prompt`
- **SKILL.md**: [`skills/pi-agent-customize-system-prompt/SKILL.md`](/skills/pi-agent-customize-system-prompt/SKILL.md)
- **Title**: Customizing the Pi Coding Agent System Prompt
- **Files**: 1
- **Structure**: flat
- **Version**: 1.0.0
- **Flags**: `UNKNOWN_KEYS`

> guide for customizing the Pi Agent system prompt to add custom tools and workflow instructions

### `plan-ceo-review`

- **Path**: `skills/plan-ceo-review`
- **SKILL.md**: [`skills/plan-ceo-review/SKILL.md`](/skills/plan-ceo-review/SKILL.md)
- **Title**: Mega Plan Review Mode
- **Files**: 9
- **Structure**: flat
- **Version**: 1.0.0
- **Flags**: `ALLOWED_TOOLS_LIST`, `UNKNOWN_KEYS`, `BODY_LENGTH`

> CEO/founder-mode plan review. (gstack)

### `plan-design-review`

- **Path**: `skills/plan-design-review`
- **SKILL.md**: [`skills/plan-design-review/SKILL.md`](/skills/plan-design-review/SKILL.md)
- **Title**: /plan-design-review: Designer's Eye Plan Review
- **Files**: 7
- **Structure**: flat
- **Version**: 2.0.0
- **Flags**: `ALLOWED_TOOLS_LIST`, `UNKNOWN_KEYS`, `BODY_LENGTH`

> Designer's eye plan review — interactive, like CEO and Eng review. (gstack)

### `plan-devex-review`

- **Path**: `skills/plan-devex-review`
- **SKILL.md**: [`skills/plan-devex-review/SKILL.md`](/skills/plan-devex-review/SKILL.md)
- **Title**: /plan-devex-review: Developer Experience Plan Review
- **Files**: 8
- **Structure**: flat
- **Version**: 2.0.0
- **Flags**: `ALLOWED_TOOLS_LIST`, `UNKNOWN_KEYS`, `BODY_LENGTH`

> Interactive developer experience plan review. (gstack)

### `plan-eng-review`

- **Path**: `skills/plan-eng-review`
- **SKILL.md**: [`skills/plan-eng-review/SKILL.md`](/skills/plan-eng-review/SKILL.md)
- **Title**: Plan Review Mode
- **Files**: 7
- **Structure**: flat
- **Version**: 1.0.0
- **Flags**: `ALLOWED_TOOLS_LIST`, `UNKNOWN_KEYS`, `BODY_LENGTH`

> Eng manager-mode plan review. (gstack)

### `planning-and-task-breakdown`

- **Path**: `skills/planning-and-task-breakdown`
- **SKILL.md**: [`skills/planning-and-task-breakdown/SKILL.md`](/skills/planning-and-task-breakdown/SKILL.md)
- **Title**: Planning and Task Breakdown
- **Files**: 1
- **Structure**: flat

> Breaks work into ordered tasks. Use when you have a spec or clear requirements and need to break work into implementable tasks. Use when a task feels too large to start, when you need to estimate scope, or when parallel work is possible.

### `poteto-mode`

- **Path**: `skills/poteto-mode`
- **SKILL.md**: [`skills/poteto-mode/SKILL.md`](/skills/poteto-mode/SKILL.md)
- **Title**: Poteto mode
- **Files**: 74
- **Structure**: references, scripts

> poteto's agent style for concise, detailed responses, deliberate subagents, unslopped prose, simple code, and verified work. Use for poteto, /poteto-mode, or requests to work in this style.

### `pptx-generator`

- **Path**: `skills/pptx-generator`
- **SKILL.md**: [`skills/pptx-generator/SKILL.md`](/skills/pptx-generator/SKILL.md)
- **Title**: PPTX Generator & Editor
- **Files**: 6
- **Structure**: references
- **License**: MIT
- **Version**: 1.0
- **Flags**: `METADATA_NON_STRING`

> Generate, edit, and read PowerPoint presentations. Create from scratch with PptxGenJS (cover, TOC, content, section divider, summary slides), edit existing PPTX via XML workflows, or extract text with markitdown. Triggers: PPT, PPTX, PowerPoint, presentation, slide, deck, slides.

### `pr`

- **Path**: `skills/pr`
- **SKILL.md**: [`skills/pr/SKILL.md`](/skills/pr/SKILL.md)
- **Title**: pr
- **Files**: 3
- **Structure**: flat
- **Flags**: `METADATA_NON_STRING`

> Use when writing a PR body.

### `recall`

- **Path**: `skills/recall`
- **SKILL.md**: [`skills/recall/SKILL.md`](/skills/recall/SKILL.md)
- **Title**: Recall
- **Files**: 1
- **Structure**: flat

> Reconstruct your recent working context from your own chat history, live state, and the shared record (user reports, prior fixes, incidents), then hand back a tight current-state brief. Use for 'recall my work on X', 'catch me up', 'what have I been working on', 'where did I leave off', before starting or resuming work, and before telling the user that something was never recorded.

### `retro`

- **Path**: `skills/retro`
- **SKILL.md**: [`skills/retro/SKILL.md`](/skills/retro/SKILL.md)
- **Title**: retro
- **Files**: 2
- **Structure**: flat
- **Flags**: `UNKNOWN_KEYS`

> Conduct a retrospective on a coding session.

### `ship`

- **Path**: `skills/ship`
- **SKILL.md**: [`skills/ship/SKILL.md`](/skills/ship/SKILL.md)
- **Title**: Ship: Fully Automated Ship Workflow
- **Files**: 33
- **Structure**: flat
- **Version**: 1.0.0
- **Flags**: `ALLOWED_TOOLS_LIST`, `UNKNOWN_KEYS`, `BODY_LENGTH`

> Ship workflow: detect + merge base branch, run tests, review diff, bump VERSION, update CHANGELOG, commit, push, create PR. (gstack)

### `shipping-and-launch`

- **Path**: `skills/shipping-and-launch`
- **SKILL.md**: [`skills/shipping-and-launch/SKILL.md`](/skills/shipping-and-launch/SKILL.md)
- **Title**: Shipping and Launch
- **Files**: 1
- **Structure**: flat

> Prepares production launches. Use when preparing to deploy to production. Use when you need a pre-launch checklist, when setting up monitoring, when planning a staged rollout, or when you need a rollback strategy.

### `show-me-your-work`

- **Path**: `skills/show-me-your-work`
- **SKILL.md**: [`skills/show-me-your-work/SKILL.md`](/skills/show-me-your-work/SKILL.md)
- **Title**: Show me your work
- **Files**: 3
- **Structure**: references, scripts

> Keep a reviewable decision trail for long-running or unattended work: a TSV log with one row per decision (what, why, evidence, result). Local by default; commit it when a reviewer needs the trail to trust the result. Use for /show-me-your-work, autonomous or multi-phase runs, or work a human reviews after stepping away.

### `spec`

- **Path**: `skills/spec`
- **SKILL.md**: [`skills/spec/SKILL.md`](/skills/spec/SKILL.md)
- **Title**: /spec — Author a Backlog-Ready Spec (issue + optional agent spawn)
- **Files**: 5
- **Structure**: flat
- **Version**: 0.1.0
- **Flags**: `ALLOWED_TOOLS_LIST`, `UNKNOWN_KEYS`, `BODY_LENGTH`

> Turn vague intent into a precise, executable spec in five phases. (gstack)

### `spec-driven-development`

- **Path**: `skills/spec-driven-development`
- **SKILL.md**: [`skills/spec-driven-development/SKILL.md`](/skills/spec-driven-development/SKILL.md)
- **Title**: Spec-Driven Development
- **Files**: 1
- **Structure**: flat

> Creates specs before coding. Use when starting a new project, feature, or significant change and no specification exists yet. Use when requirements are unclear, ambiguous, or only exist as a vague idea.

### `storyboard-manager`

- **Path**: `skills/storyboard-manager`
- **SKILL.md**: [`skills/storyboard-manager/SKILL.md`](/skills/storyboard-manager/SKILL.md)
- **Title**: Storyboard Manager
- **Files**: 7
- **Structure**: references, scripts
- **Flags**: `BODY_LENGTH`

> Assist writers with story planning, character development, plot structuring, chapter writing, timeline tracking, and consistency checking. Use this skill when working with creative writing projects organized in folders containing characters, chapters, story planning documents, and summaries. Trigger this skill for tasks like "Help me develop this character," "Write the next chapter," "Check consistency across my story," or "Track the timeline of events."

### `subagents`

- **Path**: `skills/subagents`
- **SKILL.md**: [`skills/subagents/SKILL.md`](/skills/subagents/SKILL.md)
- **Title**: Subagents
- **Files**: 1
- **Structure**: flat

> invoke this skill when the user asks you to use subagents

### `to-questionnaire`

- **Path**: `skills/to-questionnaire`
- **SKILL.md**: [`skills/to-questionnaire/SKILL.md`](/skills/to-questionnaire/SKILL.md)
- **Title**: <Questionnaire title>
- **Files**: 2
- **Structure**: flat
- **Flags**: `UNKNOWN_KEYS`

> Turn a decision you can't fully answer into a questionnaire for someone else to fill in.

### `to-spec`

- **Path**: `skills/to-spec`
- **SKILL.md**: [`skills/to-spec/SKILL.md`](/skills/to-spec/SKILL.md)
- **Title**: to-spec
- **Files**: 2
- **Structure**: flat
- **Flags**: `UNKNOWN_KEYS`

> Turn the current conversation into a spec and publish it to the project issue tracker: no interview, just synthesis of what you've already discussed.

### `to-tickets`

- **Path**: `skills/to-tickets`
- **SKILL.md**: [`skills/to-tickets/SKILL.md`](/skills/to-tickets/SKILL.md)
- **Title**: To Tickets
- **Files**: 2
- **Structure**: flat
- **Flags**: `UNKNOWN_KEYS`

> Break a plan, spec, or the current conversation into a set of tracer-bullet tickets, each declaring its blocking edges, published to the configured tracker (edges as text in one file per ticket locally, or native blocking links on a real tracker).

### `triage`

- **Path**: `skills/triage`
- **SKILL.md**: [`skills/triage/SKILL.md`](/skills/triage/SKILL.md)
- **Title**: Triage
- **Files**: 4
- **Structure**: flat
- **Flags**: `UNKNOWN_KEYS`

> Move issues and external PRs through a state machine of triage roles, categorise, verify, grill if needed, and write agent-ready briefs.

### `verification-and-review-protocol`

- **Path**: `skills/verification-and-review-protocol`
- **SKILL.md**: [`skills/verification-and-review-protocol/SKILL.md`](/skills/verification-and-review-protocol/SKILL.md)
- **Title**: Verification & Review Protocol
- **Files**: 4
- **Structure**: references
- **Version**: 2.0.0
- **Flags**: `UNKNOWN_KEYS`

> Governs the protocol for receiving feedback, requesting subagent reviews, and enforcing verification gates. Contains the 'Iron Law' preventing false completion claims. Use when receiving PR feedback, finishing tasks, or before claiming work is 'done'.

### `wait-what`

- **Path**: `skills/wait-what`
- **SKILL.md**: [`skills/wait-what/SKILL.md`](/skills/wait-what/SKILL.md)
- **Title**: wait-what
- **Files**: 2
- **Structure**: flat
- **Flags**: `UNKNOWN_KEYS`

> Stop. That last message did not land: re-pitch it.

### `wayfinder`

- **Path**: `skills/wayfinder`
- **SKILL.md**: [`skills/wayfinder/SKILL.md`](/skills/wayfinder/SKILL.md)
- **Title**: wayfinder
- **Files**: 2
- **Structure**: flat
- **Flags**: `UNKNOWN_KEYS`

> Plan a huge chunk of work (more than one agent session can hold) as a shared map of decision tickets on your issue tracker, and resolve them one at a time until the way to the destination is clear.

### `writing-plans`

- **Path**: `skills/writing-plans`
- **SKILL.md**: [`skills/writing-plans/SKILL.md`](/skills/writing-plans/SKILL.md)
- **Title**: Writing Plans
- **Files**: 2
- **Structure**: flat

> Use when you have a spec or requirements for a multi-step task, before touching code

## 8. Documentation & Content Creation

> **38 skills** in this category.

### `agents-md`

- **Path**: `skills/agents-md`
- **SKILL.md**: [`skills/agents-md/SKILL.md`](/skills/agents-md/SKILL.md)
- **Title**: agents-md
- **Files**: 1
- **Structure**: flat
- **Version**: 1.1.0
- **Flags**: `UNKNOWN_KEYS`

> Creates or updates a compact, high-signal AGENTS.md instruction file for a repository, helping future AI coding agents avoid mistakes and onboard faster.

### `analyzing-us-bigtech-stocks`

- **Path**: `skills/analyzing-us-bigtech-stocks`
- **SKILL.md**: [`skills/analyzing-us-bigtech-stocks/SKILL.md`](/skills/analyzing-us-bigtech-stocks/SKILL.md)
- **Title**: Analyzing US Big-Tech Stocks — Event RCA & Trend Reports
- **Files**: 14
- **Structure**: assets, references, scripts
- **License**: Apache-2.0
- **Version**: 1.6.0
- **Flags**: `UNKNOWN_KEYS`

> Produces institutional-grade, fact-based market research reports explaining US-listed big-tech stock price performance and trends — earnings reactions, guidance shocks, AI-narrative repricing, drawdowns and rallies — for companies such as GOOGL, MSFT, META, AMZN, AAPL, NVDA, TSLA. Use when asked why a stock moved, to run a root-cause analysis (RCA) on a price event, or to build a source-cited, evidence-based stock research report or multi-page deck. The full-pipeline skill of the big-tech research family: nine-lens hypothesis tree, GAAP bridge, machine-checked fact base, numeric + render + accessibility audits with consensus/epistemic/waterfall/mandate/temporal/snapshot schema gates, source-snapshot verification, SHA-256 provenance sealing, and --json CI output. For a lighter single-file post-earnings note use big-tech-earnings-postmortem; for a quantified single-note with segment deep-dive use bigtech-equity-research. Enforces primary-source verification, confidence labels, and audit gates before delivery.

### `big-tech-earnings-postmortem`

- **Path**: `skills/big-tech-earnings-postmortem`
- **SKILL.md**: [`skills/big-tech-earnings-postmortem/SKILL.md`](/skills/big-tech-earnings-postmortem/SKILL.md)
- **Title**: Big-Tech Earnings Post-Mortem & Trend Analysis
- **Files**: 10
- **Structure**: assets, scripts
- **License**: Apache-2.0
- **Version**: 1.6.0
- **Flags**: `UNKNOWN_KEYS`, `BODY_LENGTH`

> Conduct fact-based, evidence-disciplined root-cause analysis of a US-listed big-tech stock's price move around earnings, and produce a single-file HTML note passing bundled lite delivery gates (number registry with consensus + temporal-order + snapshot-linkage checks, placeholder, scoped disclosure, render, accessibility audits) with provenance sealing and source snapshots. The lightweight, fastest-ship member of the big-tech research family: layered driver attribution (durability × evidence axes), a machine-checked lite number registry instead of the flagship's full fact base — use analyzing-us-bigtech-stocks for a full audited IC deck and bigtech-equity-research for a quantified single-note with segment deep-dive and options math. Trigger when the user asks why a big-tech stock moved sharply after earnings, or requests a post-earnings deep dive — phrases like "post-earnings analysis", "why did X drop after earnings", "earnings post-mortem", "stock price drop root cause", or "big tech earnings deep dive".

### `bigtech-equity-research`

- **Path**: `skills/bigtech-equity-research`
- **SKILL.md**: [`skills/bigtech-equity-research/SKILL.md`](/skills/bigtech-equity-research/SKILL.md)
- **Title**: Big-Tech Equity Research
- **Files**: 19
- **Structure**: assets, scripts, templates
- **License**: Apache-2.0
- **Version**: 1.6.0
- **Flags**: `UNKNOWN_KEYS`

> Produce institutional-grade, evidence-based equity research notes on US big-tech stocks (GOOGL, MSFT, AMZN, AAPL, META, NVDA, TSLA, and peers). Use when asked to explain a stock-price event (post-earnings move, guidance shock, regulatory action), analyze a multi-quarter price trend, attribute a drawdown to its drivers, or build a ranked driver decomposition of a price move. The quantified single-note member of the big-tech research family — segment deep-dive with a machine-checked ASC 280 segment-map staleness gate, options math, canonical peer baskets, machine-checked lite number registry with consensus, temporal-order and snapshot-linkage gates, and bundled lite delivery audits with SHA-256 provenance sealing and --json CI output. For a full audited multi-page IC deck use analyzing-us-bigtech-stocks; for a lighter post-earnings note use big-tech-earnings-postmortem. Outputs a self-contained HTML note with a ranked root-cause decomposition. Analytical output only — not investment advice.

### `cheat-sheet`

- **Path**: `skills/cheat-sheet`
- **SKILL.md**: [`skills/cheat-sheet/SKILL.md`](/skills/cheat-sheet/SKILL.md)
- **Title**: Cheatsheet 生成器
- **Files**: 1
- **Structure**: flat

> 将 PDF/Word/Markdown 学习资料转化为精炼的知识浓缩卡文档。支持三种风格（知识点速查卡/思维导图式/Q&A式），输出双栏小字 PDF。当用户说"生成知识浓缩卡"、"生成 Cheatsheet"、"帮我做个速查表"、"把这个资料整理成一页纸"、"做个知识卡片"时触发。**不处理**：基于材料出题（→ quiz-mastery）、长期学习项目（→ study-buddy）。

### `codex-ppt`

- **Path**: `skills/codex-ppt`
- **SKILL.md**: [`skills/codex-ppt/SKILL.md`](/skills/codex-ppt/SKILL.md)
- **Title**: Codex PPT
- **Files**: 40
- **Structure**: references, scripts
- **Flags**: `METADATA_NON_STRING`

> Generate visually unified image-based PPT/PPTX decks from articles, reports, papers, notes, or outlines.

### `content-analysis`

- **Path**: `skills/content-analysis`
- **SKILL.md**: [`skills/content-analysis/SKILL.md`](/skills/content-analysis/SKILL.md)
- **Title**: ContentAnalysis
- **Files**: 3
- **Structure**: flat

> Content extraction and analysis — wisdom extraction from videos, podcasts, articles, and YouTube. USE WHEN extract wisdom, content analysis, analyze content, insight report, analyze video, analyze podcast, extract insights, key takeaways, what did I miss, extract from YouTube.

### `cyber-ppt`

- **Path**: `skills/cyber-ppt`
- **SKILL.md**: [`skills/cyber-ppt/SKILL.md`](/skills/cyber-ppt/SKILL.md)
- **Title**: CyberPPT
- **Files**: 11673
- **Structure**: assets, references, scripts
- **Flags**: `BODY_LENGTH`

> 当用户需要把 DOCX、PDF、TXT、XLSX、研究报告、业务材料或原始数据转成高密度、可编辑、咨询风格 PPTX 时使用；也适用于需要 SCR 论证、视觉风格探索、详细图表和渲染质检的 PPT。

### `document-generate`

- **Path**: `skills/document-generate`
- **SKILL.md**: [`skills/document-generate/SKILL.md`](/skills/document-generate/SKILL.md)
- **Title**: Document Generate: Diataxis Documentation Writer
- **Files**: 2
- **Structure**: flat
- **Version**: 1.0.0
- **Flags**: `ALLOWED_TOOLS_LIST`, `UNKNOWN_KEYS`, `BODY_LENGTH`

> Generate missing documentation from scratch for a feature, module, or entire project. (gstack)

### `document-release`

- **Path**: `skills/document-release`
- **SKILL.md**: [`skills/document-release/SKILL.md`](/skills/document-release/SKILL.md)
- **Title**: Document Release: Documentation Audit and Update
- **Files**: 7
- **Structure**: flat
- **Version**: 1.0.0
- **Flags**: `ALLOWED_TOOLS_LIST`, `UNKNOWN_KEYS`, `BODY_LENGTH`

> Release documentation audit. (gstack)

### `docx`

- **Path**: `skills/docx`
- **SKILL.md**: [`skills/docx/SKILL.md`](/skills/docx/SKILL.md)
- **Title**: DOCX Creation, Editing, and Analysis
- **Files**: 35
- **Structure**: references, routes, scenes, scripts
- **License**: Proprietary. LICENSE.txt has complete terms
- **Author**: Z.AI
- **Version**: 1.0

> Comprehensive document creation, editing, and analysis with support for tracked changes, comments, formatting preservation, and text extraction. When GLM needs to work with professional documents (.docx files) for: (1) Creating new documents, (2) Modifying or editing content, (3) Working with tracked changes, (4) Adding comments, or any other document tasks

### `docx-generation`

- **Path**: `skills/docx-generation`
- **SKILL.md**: [`skills/docx-generation/SKILL.md`](/skills/docx-generation/SKILL.md)
- **Title**: Comprehensive DOCX Generation & Conversion Skill
- **Files**: 1
- **Structure**: flat
- **Version**: 1.0
- **Flags**: `UNKNOWN_KEYS`, `BODY_LENGTH`

> Comprehensive DOCX Generation & Conversion Skill

### `domain-modeling`

- **Path**: `skills/domain-modeling`
- **SKILL.md**: [`skills/domain-modeling/SKILL.md`](/skills/domain-modeling/SKILL.md)
- **Title**: Domain Modeling
- **Files**: 4
- **Structure**: flat

> Build and sharpen a project's domain model. Use when discussing codebase terminology, writing or editing a GLOSSARY.md, or recording or editing an ADR.

### `experiment-suite`

- **Path**: `skills/experiment-suite`
- **SKILL.md**: [`skills/experiment-suite/SKILL.md`](/skills/experiment-suite/SKILL.md)
- **Title**: Experiment Suite
- **Files**: 18
- **Structure**: references

> Use when the user has a research question and needs a complete experiment package — design document, runnable code, results (measured or simulated with honest provenance), publication-grade figures, structured report. Single-stage, no Python runtime.

### `handoff`

- **Path**: `skills/handoff`
- **SKILL.md**: [`skills/handoff/SKILL.md`](/skills/handoff/SKILL.md)
- **Title**: Handoff
- **Files**: 2
- **Structure**: flat
- **Flags**: `UNKNOWN_KEYS`

> Compact the current conversation into a single, detailed handoff message — everything that happened, why it happened, and what's left — output in a code block so it can be copy-pasted into a fresh agent session. Use when hitting context limits, switching focus, ending a work session, or partitioning a task across fresh contexts.

### `humanizer`

- **Path**: `skills/humanizer`
- **SKILL.md**: [`skills/humanizer/SKILL.md`](/skills/humanizer/SKILL.md)
- **Title**: HUMANIZER v7.0.0 — Ultimate Edition
- **Files**: 18
- **Structure**: flat
- **License**: MIT
- **Version**: 7.0.0
- **Flags**: `METADATA_NON_STRING`

> Remove signs of AI-generated writing and restore natural human voice. Archetype-based detection with heuristic triage, genre-gated positive humanization, forensic artifact scanning, and a dedicated fiction protocol. Synthesizes all prior editions (v1–v6) into a single operational system. Resilient to model evolution; safe for token-constrained environments.

### `literature-survey`

- **Path**: `skills/literature-survey`
- **SKILL.md**: [`skills/literature-survey/SKILL.md`](/skills/literature-survey/SKILL.md)
- **Title**: Literature Survey
- **Files**: 9
- **Structure**: references, templates

> Use when the user wants a comprehensive literature survey on a specific research topic. Outputs a complete PDF survey (6–20 pages, 60+ real citations, 100+ recommended) with LaTeX source, taxonomy figures, and a classified literature table. Single-stage, no Python runtime.

### `make-pdf`

- **Path**: `skills/make-pdf`
- **SKILL.md**: [`skills/make-pdf/SKILL.md`](/skills/make-pdf/SKILL.md)
- **Title**: make-pdf: publication-quality PDFs from markdown
- **Files**: 52
- **Structure**: flat
- **Version**: 1.0.0
- **Flags**: `ALLOWED_TOOLS_LIST`, `UNKNOWN_KEYS`

> Turn any markdown file into a publication-quality PDF. (gstack)

### `markdown-to-html`

- **Path**: `skills/markdown-to-html`
- **SKILL.md**: [`skills/markdown-to-html/SKILL.md`](/skills/markdown-to-html/SKILL.md)
- **Title**: markdown-to-web — Pipeline Skill v2.1.0
- **Files**: 1
- **Structure**: flat
- **Version**: 2.1.0
- **Flags**: `UNKNOWN_KEYS`, `BODY_LENGTH`

> Renders an arbitrary Markdown document as a polished, single-file, accessible web page. Accepts any .md file plus an optional template (technical three-column / editorial long-form) and an optional tag registry (severity, confidence, status, custom). Built on React 19 + Vite 8 + Tailwind v4 + react-markdown + lucide-react. Includes mobile TOC drawer, back-to-top, code-block copy buttons, reading-time estimation (Latin + CJK-aware), print stylesheet, build-time title injection, source-markdown validation gate, CI workflow, and Husky pre-commit hook.

### `markdown-to-web`

- **Path**: `skills/markdown-to-web`
- **SKILL.md**: [`skills/markdown-to-web/SKILL.md`](/skills/markdown-to-web/SKILL.md)
- **Title**: markdown-to-web — Validation Review & Unified Skill Specification
- **Files**: 35
- **Structure**: flat
- **Version**: 4.1.1
- **Flags**: `UNKNOWN_KEYS`, `BODY_LENGTH`

> Renders an arbitrary Markdown document as a polished, single-file, accessible web page. Accepts any .md file plus an optional template (editorial long-form / technical docs / minimal print) and an optional tag registry (severity, confidence, status, custom). Built on React 19 + Vite 7 + Tailwind v4 + react-markdown.

### `market-research-reports`

- **Path**: `skills/market-research-reports`
- **SKILL.md**: [`skills/market-research-reports/SKILL.md`](/skills/market-research-reports/SKILL.md)
- **Title**: Market Research Reports
- **Files**: 8
- **Structure**: assets, references, scripts
- **Flags**: `ALLOWED_TOOLS_LIST`, `BODY_LENGTH`

> Generate comprehensive market research reports (50+ pages) in the style of top consulting firms (McKinsey, BCG, Gartner). Features professional LaTeX formatting, extensive visual generation with scientific-schematics and generate-image, deep integration with research-lookup for data gathering, and multi-framework strategic analysis including Porter's Five Forces, PESTLE, SWOT, TAM/SAM/SOM, and BCG Matrix.

### `officecli`

- **Path**: `skills/officecli`
- **SKILL.md**: [`skills/officecli/SKILL.md`](/skills/officecli/SKILL.md)
- **Title**: officecli
- **Files**: 1
- **Structure**: flat

> Create, analyze, proofread, and modify Office documents (.docx, .xlsx, .pptx) using the officecli CLI tool. Use when the user wants to create, inspect, check formatting, find issues, add charts, or modify Office documents.

### `pptx`

- **Path**: `skills/pptx`
- **SKILL.md**: [`skills/pptx/SKILL.md`](/skills/pptx/SKILL.md)
- **Title**: PPT creation, editing, and analysis
- **Files**: 14
- **Structure**: scripts
- **License**: Proprietary. LICENSE.txt has complete terms
- **Author**: Z.AI
- **Version**: 1.0
- **Flags**: `BODY_LENGTH`

> Presentation creation, editing, and analysis for .pptx files: (1) Creating new presentations, (2) Modifying or editing content, (3) Working with layouts, (4) Adding comments or speaker notes. Academic/paper-based presentations use the embedded Beamer module at end of this file (PDF output only).

### `qingyan-research`

- **Path**: `skills/qingyan-research`
- **SKILL.md**: [`skills/qingyan-research/SKILL.md`](/skills/qingyan-research/SKILL.md)
- **Title**: qingyan-research
- **Files**: 2
- **Structure**: flat

> Deep web research and HTML report generation. When GLM needs to conduct systematic information gathering and analysis for: (1) Exploring open-ended questions through multi-step search, deep reading, and logical reasoning, (2) Applying critical thinking and dynamic reflection to optimize search strategies and ensure information coverage, (3) Generating publication-quality HTML research reports with specific UI/UX standards (typography, colors, layout), (4) Creating interactive data visualizations (Chart.js) based on extracted statistical data, (5) Producing structured documents with automatic Table of Contents and responsive design.

### `quiz-mastery`

- **Path**: `skills/quiz-mastery`
- **SKILL.md**: [`skills/quiz-mastery/SKILL.md`](/skills/quiz-mastery/SKILL.md)
- **Title**: 测验大师 (Quiz Mastery)
- **Files**: 18
- **Structure**: scripts

> 出题、测验、复习、掌握度追踪工具。**用户说"复习"、"巩固"、"回顾"任一关键词时优先触发本 skill**。当用户的请求与"题目/复习"相关时触发：把学习资料/PDF/材料转成题目练习（"给这个 PDF 出几道题"）、导入题目文件做练习（"我有一份题目文件，帮我做"）、复习已学内容（"复习一下昨天的"、"巩固一下"、"回顾下昨天"、"用艾宾浩斯帮我安排"）、遗忘曲线追踪、掌握度评分。**🔴 强制规则**：每次出题/导入题目成功后，**首轮展示题目前必须问一句**"要不要生成网页练习页？"，用户说要 → 调用 quiz-html skill。**不处理**：长期学习项目的进度管理、计划制定（→ study-buddy）。

### `research`

- **Path**: `skills/research`
- **SKILL.md**: [`skills/research/SKILL.md`](/skills/research/SKILL.md)
- **Title**: research
- **Files**: 2
- **Structure**: flat

> Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo. Use when the user wants a topic researched, docs or API facts gathered, or reading legwork delegated to a background agent.

### `research-explorer`

- **Path**: `skills/research-explorer`
- **SKILL.md**: [`skills/research-explorer/SKILL.md`](/skills/research-explorer/SKILL.md)
- **Title**: Research Explorer
- **Files**: 1
- **Structure**: flat

> Use when the user has a vague research direction and wants to explore feasible specific topics. Outputs a structured analysis with candidate topics, innovation/feasibility scoring, and a pre-survey of 20–30 representative works. Single-stage, no Python runtime.

### `resume-builder`

- **Path**: `skills/resume-builder`
- **SKILL.md**: [`skills/resume-builder/SKILL.md`](/skills/resume-builder/SKILL.md)
- **Title**: Resume Builder（简历生成与优化）
- **Files**: 13
- **Structure**: references, scripts

> 从零生成或全面优化一份中文简历，并导出 docx / pdf / markdown 多种格式。用 STAR 法则改写经历、做 ATS 关键词覆盖率检查、根据行业（互联网产品 / 技术 / 金融 / 通用）选模板。当用户说"帮我写简历 / 优化简历 / 简历不会写 / 我的简历太弱了 / 简历看起来不专业 / 简历改一改 / 给我做个简历模板 / 简历导出 / 简历加点关键词"，或者上传 .pdf/.docx 简历后说"看看怎么改"时，必须触发本 skill。即使用户只问"我的简历有什么问题"也要触发。

### `source-driven-development`

- **Path**: `skills/source-driven-development`
- **SKILL.md**: [`skills/source-driven-development/SKILL.md`](/skills/source-driven-development/SKILL.md)
- **Title**: Source-Driven Development
- **Files**: 1
- **Structure**: flat

> Grounds every implementation decision in official documentation. Use when you want authoritative, source-cited code free from outdated patterns. Use when building with any framework or library where correctness matters.

### `study-buddy`

- **Path**: `skills/study-buddy`
- **SKILL.md**: [`skills/study-buddy/SKILL.md`](/skills/study-buddy/SKILL.md)
- **Title**: 督学助手 (Study Buddy)
- **Files**: 1
- **Structure**: flat
- **Flags**: `BODY_LENGTH`

> 智能督学助手，管理用户的长期学习项目工作流。当用户表达学习项目相关意图时触发：创建/制定学习计划（"我想学X"、"帮我制定计划"）、汇报学习进度（"学完了"、"今天搞定了"、"完成今日任务"）、查询计划状态（"我学到哪了"、"看下进度"）、查看学习报告（"日报""周报""月报""项目总结""5月10号到15号的报告"）、晨间/晚间打卡复盘、督促、动态调整计划、抱怨学不下去时（情绪支持）。**🔴 项目生成流程铁律**：项目生成成功后**必须一口气走完"项目→知识点→计划表"**，禁止只汇报"项目已生成 / X 个知识点 / X 个模块"就停下，必须**立即**输出"DAY / 项目 / 知识点 / 时长 / 难度"表格供用户确认 DAY 安排，否则视为流程失败。**🔴 报告查询铁律**：用户表达查看学习报告意图时（日报/周报/月报/项目总结/任意时间段），必须从 USER.md 取**对应时间段**的 `project_id` + `knowledge_id`，传给 `study_buddy_supervise` 工具的 `study_check` action 拿原始数据，按"模块3 主动报告查询"输出，**全程只读不写 USER.md**。**不处理**：单次出题（→ quiz-mastery）、Cheatsheet 生成（→ cheat-sheet）、把题目文件导入做练习（→ quiz-mastery）。

### `technical-writing`

- **Path**: `skills/technical-writing`
- **SKILL.md**: [`skills/technical-writing/SKILL.md`](/skills/technical-writing/SKILL.md)
- **Title**: Technical writing
- **Files**: 1
- **Structure**: flat

> Layered technical-writing standard: Diátaxis structure, Google developer style sentences, STE instruction rules, Global English syntax. Use for /technical-writing or when writing or reviewing docs, RFCs, readmes, PR descriptions, or commit messages.

### `to-distill-project-into-skill`

- **Path**: `skills/to-distill-project-into-skill`
- **SKILL.md**: [`skills/to-distill-project-into-skill/SKILL.md`](/skills/to-distill-project-into-skill/SKILL.md)
- **Title**: Distill Project Into Skill — Meta-SKILL
- **Files**: 9
- **Structure**: flat
- **Version**: 1.0.0
- **Flags**: `UNKNOWN_KEYS`, `BODY_LENGTH`

> Meta-skill for distilling a complete project codebase into a comprehensive, maintainable SKILL.md document. Use after a major project update, when onboarding a new team, or when you need to create a single-source-of-truth reference for future AI coding agents working on this codebase.

### `translation-engine`

- **Path**: `skills/translation-engine`
- **SKILL.md**: [`skills/translation-engine/SKILL.md`](/skills/translation-engine/SKILL.md)
- **Title**: System Prompt: Deterministic Forensic Translation Engine (v10.1 — Successive Draft & Source-Preservation Hardened)
- **Files**: 9
- **Structure**: flat
- **Flags**: `BODY_LENGTH`

> Deterministic Forensic Translation Engine v10.1 — bilingual (Chinese ↔ English) translation with L4 (Forensic Grade) precision and L3 (Strict Grade) professional publishing. Covers the 6-phase scratchpad protocol (IU definition, domain pack selection, draft-lock via successive versioning, audit, targeted repair, output), 5 pluggable domain packs (Engineering, Legal, Medical, Financial, Academic — each with domain-specific modality markers), anti-enhancement protocol, code-fence cryptographic seal, glossary management with 3-tier certainty levels, few-shot calibration with 10 examples, size-aware draft-lock tiers, and a minimal Python wrapper. Use when translating between Chinese and English — especially for legal, medical, financial, engineering, or academic documents where L3/L4 precision is required, or when the user says 'translate', '翻译', 'forensic translation', 'strict translation', or references the Translation Engine.

### `unslop`

- **Path**: `skills/unslop`
- **SKILL.md**: [`skills/unslop/SKILL.md`](/skills/unslop/SKILL.md)
- **Title**: Unslop
- **Files**: 2
- **Structure**: flat

> Cut AI tells from text you write or edit for a human reader (commit messages, PR titles and bodies, docs, code comments, replies). Apply before committing, posting, or sending; leave prose you didn't touch alone.

### `writing-beats`

- **Path**: `skills/writing-beats`
- **SKILL.md**: [`skills/writing-beats/SKILL.md`](/skills/writing-beats/SKILL.md)
- **Title**: writing-beats
- **Files**: 2
- **Structure**: flat
- **Flags**: `UNKNOWN_KEYS`

> Writing, exploit; assemble raw material into a journey of beats, grounding each term before a beat leans on it.

### `writing-for-agents`

- **Path**: `skills/writing-for-agents`
- **SKILL.md**: [`skills/writing-for-agents/SKILL.md`](/skills/writing-for-agents/SKILL.md)
- **Title**: writing-for-agents
- **Files**: 3
- **Structure**: flat

> Writing documents for agents. Use when creating or editing skills, or modifying AGENTS.md or CLAUDE.md.

### `writing-fragments`

- **Path**: `skills/writing-fragments`
- **SKILL.md**: [`skills/writing-fragments/SKILL.md`](/skills/writing-fragments/SKILL.md)
- **Title**: Working title
- **Files**: 2
- **Structure**: flat
- **Flags**: `UNKNOWN_KEYS`

> Writing, explore: mine raw fragments, no structure yet.

### `writing-shape`

- **Path**: `skills/writing-shape`
- **SKILL.md**: [`skills/writing-shape/SKILL.md`](/skills/writing-shape/SKILL.md)
- **Title**: writing-shape
- **Files**: 2
- **Structure**: flat
- **Flags**: `UNKNOWN_KEYS`

> Writing, exploit: shape raw material into an article, paragraph by paragraph.

## 9. Career, Learning & Personal Development

> **13 skills** in this category.

### `dream-interpreter`

- **Path**: `skills/dream-interpreter`
- **SKILL.md**: [`skills/dream-interpreter/SKILL.md`](/skills/dream-interpreter/SKILL.md)
- **Title**: dream-interpreter
- **Files**: 9
- **Structure**: assets, references, scripts

> AI 解梦大师。用户描述梦境，智能追问关键细节后，从三个视角（周公解梦/心理分析/赛博神棍）生成解读，输出结构化 JSON 供前端渲染"梦境解析卡"。

### `gaokao-collect-student-info`

- **Path**: `skills/gaokao-collect-student-info`
- **SKILL.md**: [`skills/gaokao-collect-student-info/SKILL.md`](/skills/gaokao-collect-student-info/SKILL.md)
- **Title**: 高考考生信息采集
- **Files**: 4
- **Structure**: examples

> 高考志愿填报信息采集：以考生原生表述为准，收集省份、分数、选科等 API 必填项及兴趣、 家庭、就业方向等辅助信息，尽量不做改写与过度归纳，输出结构化 student.json。 适用于高考志愿咨询开场、考生信息登记、志愿填报前的信息收集。

### `gaokao-fetch-volunteers`

- **Path**: `skills/gaokao-fetch-volunteers`
- **SKILL.md**: [`skills/gaokao-fetch-volunteers/SKILL.md`](/skills/gaokao-fetch-volunteers/SKILL.md)
- **Title**: 获取推荐志愿表
- **Files**: 10
- **Structure**: examples, scripts

> 调用高考智能推荐志愿表 API，根据考生基本信息及专业/城市/院校倾向（映射为 API 选填参数） 获取冲稳保志愿列表，解析为 parsed.json。适用于获取推荐院校、冲稳保志愿表、志愿 API 调用。

### `gaokao-generate-report`

- **Path**: `skills/gaokao-generate-report`
- **SKILL.md**: [`skills/gaokao-generate-report/SKILL.md`](/skills/gaokao-generate-report/SKILL.md)
- **Title**: 生成志愿填报报告
- **Files**: 6
- **Structure**: examples, scripts, templates

> 合并考生信息、志愿列表、专业推荐与院校推荐，生成融合分析与冲稳保志愿列表的 HTML 志愿填报报告。 适用于高考志愿报告生成、志愿填报方案输出、志愿表可视化。

### `gaokao-recommend-majors`

- **Path**: `skills/gaokao-recommend-majors`
- **SKILL.md**: [`skills/gaokao-recommend-majors/SKILL.md`](/skills/gaokao-recommend-majors/SKILL.md)
- **Title**: 推荐专业与就业方向
- **Files**: 3
- **Structure**: examples

> 基于考生画像与 API 志愿列表，由 Agent 分析推荐适合的专业方向、就业出口与具体专业清单， 输出结构化 major_recommendation.json。适用于高考专业推荐、选专业、就业方向分析。

### `gaokao-recommend-schools`

- **Path**: `skills/gaokao-recommend-schools`
- **SKILL.md**: [`skills/gaokao-recommend-schools/SKILL.md`](/skills/gaokao-recommend-schools/SKILL.md)
- **Title**: 推荐院校与理由
- **Files**: 3
- **Structure**: examples

> 基于推荐专业列表、考生画像与志愿列表，由 Agent 分析推荐院校并给出个性化理由， 输出结构化 school_recommendation.json。适用于高考院校推荐、选大学、冲稳保院校布局。

### `get-fortune-analysis`

- **Path**: `skills/get-fortune-analysis`
- **SKILL.md**: [`skills/get-fortune-analysis/SKILL.md`](/skills/get-fortune-analysis/SKILL.md)
- **Title**: Skill Name: get-fortune-analysis
- **Files**: 2
- **Structure**: flat

> 生成视觉华丽、内容详实、具有仪式感的流年运势报告（流金星象风格）。

### `gift-evaluator`

- **Path**: `skills/gift-evaluator`
- **SKILL.md**: [`skills/gift-evaluator/SKILL.md`](/skills/gift-evaluator/SKILL.md)
- **Title**: gift-evaluator
- **Files**: 2
- **Structure**: flat
- **License**: Internal Tool

> The PRIMARY tool for Spring Festival gift analysis and social interaction generation. Use this skill when users upload photos of gifts (alcohol, tea, supplements, etc.) to inquire about their value, authenticity, or how to respond socially. Integrates visual perception, market valuation, and HTML card generation.

### `idea-refine`

- **Path**: `skills/idea-refine`
- **SKILL.md**: [`skills/idea-refine/SKILL.md`](/skills/idea-refine/SKILL.md)
- **Title**: Idea Refine
- **Files**: 5
- **Structure**: scripts

> Refines ideas iteratively. Refine ideas through structured divergent and convergent thinking. Use "idea-refine" or "ideate" to trigger.

### `jd-resume-tailor`

- **Path**: `skills/jd-resume-tailor`
- **SKILL.md**: [`skills/jd-resume-tailor/SKILL.md`](/skills/jd-resume-tailor/SKILL.md)
- **Title**: JD ⇄ Resume Tailor（JD 拆解 + 简历定向改写）
- **Files**: 5
- **Structure**: references, scripts

> 给定一份 JD 和一份现有简历，做"JD 拆解 + 简历定向改写"。拆 JD 抽出硬技能、软技能、加分项；对照简历做 gap 分析；产出针对该岗位重写后的简历，突出相关经验、补齐关键词缺口、并保留候选人真实经历不编造。当用户说"针对这个岗位 / 这家公司改简历""帮我对一下这个 JD""我想投这个职位你看怎么改""把这份简历针对 X 公司优化""做一份定向版简历"，或同时给出 JD 文本 + 简历文件时，必须触发本 skill。**请勿用本 skill 做"从零写简历"**——那是 resume-builder 的事。

### `quiz-html`

- **Path**: `skills/quiz-html`
- **SKILL.md**: [`skills/quiz-html/SKILL.md`](/skills/quiz-html/SKILL.md)
- **Title**: 网页题库生成器 (Quiz HTML Builder)
- **Files**: 6
- **Structure**: examples, scripts, templates

> 把题目数组生成一个**可独立运行的网页练习页**（HTML 文件）。当用户完成 quiz-mastery 的「从资料出题」或「从文件提取题目」流程后，应主动询问是否需要"在网页里练习"，确认后调用本 skill 把题目注入模板，生成 HTML 给用户。也支持用户直接说"把这些题做成网页/HTML/练习页"时触发。**不处理**：出题（→ quiz-mastery）、评分（→ quiz-mastery）、长期复习计划（→ study-buddy）。

### `solving-a-level-exam-papers`

- **Path**: `skills/solving-a-level-exam-papers`
- **SKILL.md**: [`skills/solving-a-level-exam-papers/SKILL.md`](/skills/solving-a-level-exam-papers/SKILL.md)
- **Title**: Solving A-Level Exam Papers (PDF → examiner-standard solution)
- **Files**: 38
- **Structure**: assets, references, scripts
- **Version**: 2.0.1

> Produces examiner-standard, verified worked solutions to questions from Singapore-Cambridge GCE A-Level examination papers (H1/H2/H3 Mathematics, Further Mathematics and other quantitative subjects) supplied as PDF. Use when a user shares an exam paper PDF and asks to solve, check, audit or upgrade an answer to a numbered question, wants mark-scheme-quality working, exact answers or a model answer, or pastes OCR-garbled question text. Handles fail-closed PDF ingestion, reconstruction of symbols lost in extraction, mark-aware planning, exam presentation conventions, sandboxed symbolic verification with an evidence ledger, and severity-classified audits of existing answers.

### `teach`

- **Path**: `skills/teach`
- **SKILL.md**: [`skills/teach/SKILL.md`](/skills/teach/SKILL.md)
- **Title**: teach
- **Files**: 6
- **Structure**: flat
- **Flags**: `UNKNOWN_KEYS`

> Teach the user a new skill or concept, within this workspace.

## 10. DevOps, Infrastructure & External Integrations

> **15 skills** in this category.

### `agent-dev-sandbox`

- **Path**: `skills/agent-dev-sandbox`
- **SKILL.md**: [`skills/agent-dev-sandbox/SKILL.md`](/skills/agent-dev-sandbox/SKILL.md)
- **Title**: Agent Dev Sandbox — build & operate
- **Files**: 39
- **Structure**: references, scripts
- **Flags**: `METADATA_NON_STRING`, `UNKNOWN_KEYS`

> Build and operate a secure, egress-restricted development environment for AI coding agents on a Debian 13 host — hardened rootless Podman workspaces behind an allowlist Squid gateway, an optional KVM micro-VM tier for untrusted code, with Python 3.13, Node.js 24, Bun, pnpm, uv, Playwright, Chromium, agent-browser, Claude Code, Codex, and OpenCode preinstalled. Use when asked to set up, build, verify, or troubleshoot an isolated agent sandbox / hardened dev environment on Debian 13.

### `composio-cli`

- **Path**: `skills/composio-cli`
- **SKILL.md**: [`skills/composio-cli/SKILL.md`](/skills/composio-cli/SKILL.md)
- **Title**: Composio CLI
- **Files**: 6
- **Structure**: references

> Help users operate the published Composio CLI to find the right tool, connect accounts, inspect schemas, execute tools, subscribe to trigger events with `composio listen`, script workflows with `composio run`, and call authenticated app APIs with `composio proxy`. Use when the user asks how to do something with `composio`, wants to run a known tool slug, needs to discover a slug with `composio search`, fix a missing connection with `composio link`, inspect tool inputs with `--get-schema` or `--dry-run`, troubleshoot top-level CLI flows, or explicitly needs `composio dev` guidance.

### `deploy-nod-from-source`

- **Path**: `skills/deploy-nod-from-source`
- **SKILL.md**: [`skills/deploy-nod-from-source/SKILL.md`](/skills/deploy-nod-from-source/SKILL.md)
- **Title**: Deploy Nod from source (Ubuntu 24.04 LTS / Debian 13 Trixie)
- **Files**: 2
- **Structure**: flat
- **Version**: 1.0.0

> Deploy Nod (github.com/n8n-io/nod), the open-source personal AI agent from n8n, from source on Ubuntu 24.04 LTS or Debian 13 (Trixie). Builds the official self-host Docker stack from a pinned release tag (Node.js/Fastify server, PostgreSQL, firewalled workspace sandbox, Chromium browser container, optional Caddy HTTPS), generates secrets, configures SSH-tunnel or public-HTTPS access, and covers verification, hardening, backup, restore, updates, and token rotation. Use when asked to install, deploy, self-host, update, back up, restore, or troubleshoot Nod from source on a Linux server.

### `github-folder-downloader`

- **Path**: `skills/github-folder-downloader`
- **SKILL.md**: [`skills/github-folder-downloader/SKILL.md`](/skills/github-folder-downloader/SKILL.md)
- **Title**: GitHub Folder Downloader
- **Files**: 16
- **Structure**: scripts

> Download and mirror a single GitHub repository folder (subdirectory) to a local path without cloning the whole repository. Uses a targeted GitHub API/raw tier with ZIP and TAR.GZ archive fallback, atomic commits, and rollback. Use when the user asks to fetch, download, sync, mirror, or update a specific GitHub folder, directory, subfolder, or skills folder, or provides a URL like https://github.com/OWNER/REPO/tree/REF/PATH and wants only that path. Supports ref/commit pinning, slash-branch disambiguation, dry-run planning, JSON summaries, size/file/depth limits, symlink/LFS policies, and an offline self-test. Requires Python 3.10+; standard library only.

### `how-to-git-push-using-ssh-wrapper`

- **Path**: `skills/how-to-git-push-using-ssh-wrapper`
- **SKILL.md**: [`skills/how-to-git-push-using-ssh-wrapper/SKILL.md`](/skills/how-to-git-push-using-ssh-wrapper/SKILL.md)
- **Title**: How-To: Git Push Using the SSH Wrapper (`ssh_git_wrapper_v3.py`)
- **Files**: 5
- **Structure**: scripts
- **License**: MIT

> Push commits from this checkout to the GitHub SSH remote using ssh_git_wrapper_v3.py and an externally-supplied deploy key that is never stored in the repository. Use when pushing main to GitHub over SSH from a sandbox or CI environment without a resident ~/.ssh identity, when authenticating git push with a pasted or ephemeral ed25519 key, when a post-push remote-ref verification is required, or when no OpenSSH binary exists and a paramiko-backed ssh shim must be deployed.

### `land-and-deploy`

- **Path**: `skills/land-and-deploy`
- **SKILL.md**: [`skills/land-and-deploy/SKILL.md`](/skills/land-and-deploy/SKILL.md)
- **Title**: /land-and-deploy — Merge, Deploy, Verify
- **Files**: 9
- **Structure**: flat
- **Version**: 1.0.0
- **Flags**: `ALLOWED_TOOLS_LIST`, `UNKNOWN_KEYS`, `BODY_LENGTH`

> Land and deploy workflow. (gstack)

### `luxeverse-architect`

- **Path**: `skills/luxeverse-architect`
- **SKILL.md**: [`skills/luxeverse-architect/SKILL.md`](/skills/luxeverse-architect/SKILL.md)
- **Title**: Then re-run typecheck to regenerate from the new source tree
- **Files**: 10
- **Structure**: flat
- **Version**: 5.0.0
- **Flags**: `UNKNOWN_KEYS`, `BODY_LENGTH`

> LuxeVerse Architect Skill Comprehensive Architectural & Execution Framework for Cinematic, Production-Grade, Anti-Generic Web Platforms

### `multi-search-engine`

- **Path**: `skills/multi-search-engine`
- **SKILL.md**: [`skills/multi-search-engine/SKILL.md`](/skills/multi-search-engine/SKILL.md)
- **Title**: Multi Search Engine v2.0.1
- **Files**: 7
- **Structure**: references

> Multi search engine integration with 8 domestic (CN) search engines. Supports advanced search operators, time filters, site search, and WeChat article search. No API keys required.

### `rootless-postgresql`

- **Path**: `skills/rootless-postgresql`
- **SKILL.md**: [`skills/rootless-postgresql/SKILL.md`](/skills/rootless-postgresql/SKILL.md)
- **Title**: Rootless PostgreSQL — User-Space Install & Run (Debian, No Root)
- **Files**: 2
- **Structure**: flat
- **Flags**: `BODY_LENGTH`

> Install, initialize, and run a PostgreSQL server and client locally without root on Debian (trixie/sid), for a non-root user with a writable /home/project directory. Use when asked to install or start PostgreSQL without sudo, without systemd, or when apt install fails with permission errors. Resolves the major version dynamically, extracts .debs into a user-owned prefix, and provides idempotent start/stop/status scripts.

### `skill-finder-cn`

- **Path**: `skills/skill-finder-cn`
- **SKILL.md**: [`skills/skill-finder-cn/SKILL.md`](/skills/skill-finder-cn/SKILL.md)
- **Title**: Skill 查找器
- **Files**: 4
- **Structure**: scripts
- **Author**: 赚钱小能手
- **Flags**: `METADATA_NON_STRING`, `UNKNOWN_KEYS`

> Skill 查找器 \| Skill Finder. 帮助发现和安装 ClawHub Skills \| Discover and install ClawHub Skills. 回答'有什么技能可以X'、'找一个技能' \| Answers 'what skill can X', 'find a skill'. 触发词：找 skill、find skill、搜索 skill.

### `task-review`

- **Path**: `skills/task-review`
- **SKILL.md**: [`skills/task-review/SKILL.md`](/skills/task-review/SKILL.md)
- **Title**: task-review
- **Files**: 1
- **Structure**: flat

> 当用户指令为高复杂度任务时触发，用于将刚完成的任务路径保存为可复用技能，生成相关的SKILL.md文档。

### `template-skill`

- **Path**: `skills/template-skill`
- **SKILL.md**: [`skills/template-skill/SKILL.md`](/skills/template-skill/SKILL.md)
- **Title**: Insert instructions below
- **Files**: 1
- **Structure**: flat

> Replace with description of the skill and when Claude should use it.

### `using-agent-skills`

- **Path**: `skills/using-agent-skills`
- **SKILL.md**: [`skills/using-agent-skills/SKILL.md`](/skills/using-agent-skills/SKILL.md)
- **Title**: Using Agent Skills
- **Files**: 1
- **Structure**: flat

> Discovers and invokes agent skills. Use when starting a session or when you need to discover which skill applies to the current task. This is the meta-skill that governs how all other skills are discovered and invoked.

### `visual-design-foundations`

- **Path**: `skills/visual-design-foundations`
- **SKILL.md**: [`skills/visual-design-foundations/SKILL.md`](/skills/visual-design-foundations/SKILL.md)
- **Title**: Visual Design Foundations
- **Files**: 4
- **Structure**: references

> Apply typography, color theory, spacing systems, and iconography principles to create cohesive visual designs. Use when establishing design tokens, building style guides, or improving visual hierarchy and consistency.

### `web-design-guidelines`

- **Path**: `skills/web-design-guidelines`
- **SKILL.md**: [`skills/web-design-guidelines/SKILL.md`](/skills/web-design-guidelines/SKILL.md)
- **Title**: Web Interface Guidelines
- **Files**: 1
- **Structure**: flat
- **Author**: vercel
- **Version**: 1.0.0

> Review UI code for Web Interface Guidelines compliance. Use when asked to "review my UI", "check accessibility", "audit design", "review UX", or "check my site against best practices".

---

## Duplicating skills

> **Detected automatically** by `tools/skills_audit.py`; two skills are *duplicates* when they share a `name` and an essentially identical `SKILL.md` body (5-word-shingle Jaccard >= 0.8). No folder was deleted; entries are merged in this document only.

**Same name, different folders: 27 names** (26 byte-identical, 0 near-identical, 1 divergent).

| Skill name | Verdict | Copies | Locations |
|---|---|---|---|
| `3-statement-model` | DUPLICATE (identical) | 3 | `skills/financial-analysis/skills/3-statement-model`<br>`skills/model-builder/skills/3-statement-model`<br>`skills/pitch-agent/skills/3-statement-model` |
| `accrual-schedule` | DUPLICATE (identical) | 2 | `skills/fund-admin/skills/accrual-schedule`<br>`skills/month-end-closer/skills/accrual-schedule` |
| `audit-xls` | DUPLICATE (identical) | 7 | `skills/earnings-reviewer/skills/audit-xls`<br>`skills/financial-analysis/skills/audit-xls`<br>`skills/gl-reconciler/skills/audit-xls`<br>`skills/model-builder/skills/audit-xls`<br>`skills/month-end-closer/skills/audit-xls`<br>`skills/pitch-agent/skills/audit-xls`<br>`skills/statement-auditor/skills/audit-xls` |
| `break-trace` | DUPLICATE (identical) | 2 | `skills/fund-admin/skills/break-trace`<br>`skills/gl-reconciler/skills/break-trace` |
| `competitive-analysis` | DUPLICATE (identical) | 2 | `skills/financial-analysis/skills/competitive-analysis`<br>`skills/market-researcher/skills/competitive-analysis` |
| `comps-analysis` | DUPLICATE (identical) | 4 | `skills/financial-analysis/skills/comps-analysis`<br>`skills/market-researcher/skills/comps-analysis`<br>`skills/model-builder/skills/comps-analysis`<br>`skills/pitch-agent/skills/comps-analysis` |
| `dcf-model` | DUPLICATE (identical) | 3 | `skills/financial-analysis/skills/dcf-model`<br>`skills/model-builder/skills/dcf-model`<br>`skills/pitch-agent/skills/dcf-model` |
| `deck-refresh` | DUPLICATE (identical) | 2 | `skills/financial-analysis/skills/deck-refresh`<br>`skills/pitch-agent/skills/deck-refresh` |
| `earnings-analysis` | DUPLICATE (identical) | 2 | `skills/earnings-reviewer/skills/earnings-analysis`<br>`skills/equity-research/skills/earnings-analysis` |
| `earnings-preview` | DUPLICATE (identical) | 2 | `skills/earnings-reviewer/skills/earnings-preview`<br>`skills/equity-research/skills/earnings-preview` |
| `gl-recon` | DUPLICATE (identical) | 2 | `skills/fund-admin/skills/gl-recon`<br>`skills/gl-reconciler/skills/gl-recon` |
| `ib-check-deck` | DUPLICATE (identical) | 2 | `skills/financial-analysis/skills/ib-check-deck`<br>`skills/pitch-agent/skills/ib-check-deck` |
| `ic-memo` | DUPLICATE (identical) | 2 | `skills/private-equity/skills/ic-memo`<br>`skills/valuation-reviewer/skills/ic-memo` |
| `idea-generation` | DUPLICATE (identical) | 2 | `skills/equity-research/skills/idea-generation`<br>`skills/market-researcher/skills/idea-generation` |
| `lbo-model` | DUPLICATE (identical) | 3 | `skills/financial-analysis/skills/lbo-model`<br>`skills/model-builder/skills/lbo-model`<br>`skills/pitch-agent/skills/lbo-model` |
| `model-update` | DUPLICATE (identical) | 2 | `skills/earnings-reviewer/skills/model-update`<br>`skills/equity-research/skills/model-update` |
| `morning-note` | DUPLICATE (identical) | 2 | `skills/earnings-reviewer/skills/morning-note`<br>`skills/equity-research/skills/morning-note` |
| `nav-tieout` | DUPLICATE (identical) | 2 | `skills/fund-admin/skills/nav-tieout`<br>`skills/statement-auditor/skills/nav-tieout` |
| `pitch-deck` | DUPLICATE (identical) | 2 | `skills/investment-banking/skills/pitch-deck`<br>`skills/pitch-agent/skills/pitch-deck` |
| `portfolio-monitoring` | DUPLICATE (identical) | 2 | `skills/private-equity/skills/portfolio-monitoring`<br>`skills/valuation-reviewer/skills/portfolio-monitoring` |
| `pptx-author` | DUPLICATE (identical) | 4 | `skills/financial-analysis/skills/pptx-author`<br>`skills/market-researcher/skills/pptx-author`<br>`skills/meeting-prep-agent/skills/pptx-author`<br>`skills/pitch-agent/skills/pptx-author` |
| `returns-analysis` | DUPLICATE (identical) | 2 | `skills/private-equity/skills/returns-analysis`<br>`skills/valuation-reviewer/skills/returns-analysis` |
| `roll-forward` | DUPLICATE (identical) | 2 | `skills/fund-admin/skills/roll-forward`<br>`skills/month-end-closer/skills/roll-forward` |
| `sector-overview` | DUPLICATE (identical) | 3 | `skills/equity-research/skills/sector-overview`<br>`skills/market-researcher/skills/sector-overview`<br>`skills/pitch-agent/skills/sector-overview` |
| `skill-creator` | NAME COLLISION - content differs; do not merge | 3 | `skills/executive-deck-skill-suite/skills/skill-creator`<br>`skills/financial-analysis/skills/skill-creator`<br>`skills/skill-creator` |
| `variance-commentary` | DUPLICATE (identical) | 2 | `skills/fund-admin/skills/variance-commentary`<br>`skills/month-end-closer/skills/variance-commentary` |
| `xlsx-author` | DUPLICATE (identical) | 8 | `skills/earnings-reviewer/skills/xlsx-author`<br>`skills/financial-analysis/skills/xlsx-author`<br>`skills/gl-reconciler/skills/xlsx-author`<br>`skills/model-builder/skills/xlsx-author`<br>`skills/month-end-closer/skills/xlsx-author`<br>`skills/pitch-agent/skills/xlsx-author`<br>`skills/statement-auditor/skills/xlsx-author`<br>`skills/valuation-reviewer/skills/xlsx-author` |

**Different names, essentially the same content (top-level skills):**

| Skills | Body similarity | Note |
|---|---|---|
| `greploop` ↔ `greploop-apps` | 90.3% | per its description, `greploop-apps` is identical except it tags `@greptile-apps` (bypasses the file-count limit on huge PRs) |
| `pdf` ↔ `pdf-old-20260806` | 97.7% | archived dated snapshot of `pdf`; prefer `pdf` |
| `skill-creator` ↔ `skill-creator-zai` | 99.6% | same scope and content; keep one |

### Curated overlap notes

Every spec-compliant skill is indexed above, including several that overlap heavily or have been superseded. They are flagged here so you pick deliberately rather than by accident.

#### Obsolete — superseded, kept only as archive

| Skill | Note |
|-------|------|
| `pdf-old-20260806` | Legacy snapshot of the `pdf` toolkit (the same four production lines), archived under a dated name. Use `pdf`. |

#### Direct near-duplicates — overlapping scope

| Cluster | Overlap |
|---------|---------|
| `web-app-foundation` ↔ `web-application` ↔ `web-application-engineering` | Three distillations of the same four source codebases (digma, neo-crm, project-management, zero-balance). `web-application` v1.2.0 is the newer, fuller line; `web-application-engineering` is its self-described condensed companion ("the fuller distillation is web-application_SKILL.md"); `web-app-foundation` is the earlier foundation variant (v1.1.0). |
| `skill-creator` ↔ `skill-creator-zai` | Near-identical scope — create/improve skills, run evals, benchmark with variance analysis, optimize descriptions. |
| `memory-architect` ↔ `memory-architecture` | Both cover the OpenClaw 3-layer memory system — bootstrap/audit/recover vs setup guide/troubleshooting. |
| `tdd` ↔ `tdd-workflow` ↔ `test-driven-development` | Three overlapping test-first skills with overlapping trigger conditions. |
| `spec` ↔ `spec-driven-development` | Both turn vague intent into a spec before coding (adjacent stages: `to-spec`, `implement-spec`). |
| `ship` ↔ `land-and-deploy` ↔ `shipping-and-launch` | Three overlapping ship/deploy workflow skills. |
| `webapp-testing-journey` ↔ `frontend-ui-testing-journey` | Both walk the same browser-testing toolset (OpenClaw browser, agent-browser CLI, chrome-devtools-mcp, @playwright/mcp). |
| `thermo-nuclear-review` ↔ `thermo-nuclear-code-quality-review` | Same "thermonuclear review" trigger phrase; security/correctness vs maintainability focus. |
| `docx-generation` ↔ `docx` | `docx-generation` is a one-line scoped subset of the canonical `docx` skill. |

#### Overlapping families — deliberate variants, check descriptions before choosing

- **Document formats** — `docx` / `kimi-docx` / `minimax-docx` / `pandoc-docx-template`; `pdf` / `kimi-pdf` / `minimax-pdf` / `make-pdf`; `xlsx` / `kimi-xlsx` / `minimax-xlsx`; `pptx` / `pptx-generator` / `pptx-unified` (combines the canonical `pptx` pipeline with `cyber-ppt` and `pptx-generator` strengths) / `codex-ppt` / `cyber-ppt`.
- **Next.js 16 stack references** — `web-application`, `web-app-foundation`, `fullstack-dev`, `web-frameworks`, `nextjs16-tailwind4`, and the eight `nextjs16-react19-*` variants share the same core stack (Next.js 16 + React 19 + TypeScript strict + Tailwind v4 + Prisma/Drizzle); each variant adds app-specific lessons.
- **Code review** — `code-review` / `code-review-and-audit` / `code-review-checklist` / `code-quality-standards` form a differentiated family; the checklist explicitly defers to the others.
- **Grilling** — `grilling` (primitive) / `grill-me` (stateless) / `grill-with-docs` (stateful, captures ADRs) — one family, three modes.
- **De-slopping** — `deslop` (code slop) vs `unslop` / `humanizer` (prose) — split by target, with the prose pair overlapping.

**Repo hygiene note** — `skills/brutalist-portfolio-nextjs/rutalist-portfolio-nextjs/` is a stray, typo-named nested copy containing only a `SKILL.md`; it is tracked in git and is safe to delete.

---

## Bundled sub-skills (merged by name)

138 valid `SKILL.md` files sit inside grouping folders (agent bundles with no `SKILL.md` of their own). Merged by `name` they are **92 unique skills**; each row lists every bundle that carries a copy.

| Sub-skill | Copies | Found in bundles | Merge verdict | Description |
|---|---|---|---|---|
| `3-statement-model` | 3 | `financial-analysis`, `model-builder`, `pitch-agent` | DUPLICATE - merged | Complete, populate and fill out 3-statement financial model templates (Income Statement, Balance Sheet, Cash Flow Statement) . Use when asked to fill out model templates, complete existing model frameworks, populate financial models with data, complete a partially filled IS/BS/CF framework, or link integrated financial statements within an existing template structure. Triggers include requests to fill in, complete, or populate a 3-statement model template |
| `accrual-schedule` | 2 | `fund-admin`, `month-end-closer` | DUPLICATE - merged | Build the period-end accrual schedule — for each accrual, compute the entry, cite the support, and draft the JE. Use during month-end close; the JE is a draft for controller approval, not a posting. |
| `agent-self-scheduling` | 1 | `agent-orchestration` | unique | Make an AI agent run on a schedule, loop, or interval — cron, heartbeats, recurring autonomous checks. Use for "run every N minutes", "schedule a task", "run on a loop", "heartbeat". Covers external clocks (Claude Code, Codex, Pi) vs Hermes' built-in scheduler. |
| `ai-readiness` | 1 | `private-equity` | unique | Scan the portfolio for the highest-leverage AI opportunities and rank where to deploy operating-partner time. Ingests quarterly updates and financials across multiple portfolio companies, identifies quick wins at each, and stacks them into a single ranked action list. Use during quarterly portfolio reviews, annual planning, or when deciding which companies get AI investment first. Triggers on "AI readiness", "AI opportunity scan", "where should we deploy AI", "AI across the portfolio", "AI quick wins", or "which portcos are ready for AI". |
| `anti-sleep` | 1 | `ops-and-setup` | unique | Keep the user's MacBook awake reliably with macOS caffeinate for a set duration or while a process runs. Use for "don't let my Mac sleep", "keep the screen on", "anti-sleep", "caffeinate", overnight work, or long builds. Unlike a normal background job, it survives temporary agent-shell cleanup. |
| `audit-xls` | 7 | `earnings-reviewer`, `financial-analysis`, `gl-reconciler`, `model-builder`, `month-end-closer`, `pitch-agent`, `statement-auditor` | DUPLICATE - merged | Audit a spreadsheet for formula accuracy, errors, and common mistakes. Scopes to a selected range, a single sheet, or the entire model (including financial-model integrity checks like BS balance, cash tie-out, and logic sanity). Triggers on "audit this sheet", "check my formulas", "find formula errors", "QA this spreadsheet", "sanity check this", "debug model", "model check", "model won't balance", "something's off in my model", "model review". |
| `before-building` | 1 | `thinking-and-docs` | unique | Fire the moment the user proposes a build. Instantly surface the 1-3 consequential choices hidden in their idea. Can also be invoked with /before-building. |
| `brain-to-docs` | 1 | `thinking-and-docs` | unique | Use when the user wants to extract project vision, decisions, and preferences from his head into clear documentation (README + ADRs) through a back-and-forth Q&A loop. Triggers on "brain-to-docs", "build out the docs", "extract the vision", "let's document this project". |
| `break-trace` | 2 | `fund-admin`, `gl-reconciler` | DUPLICATE - merged | Root-cause a reconciliation break to its source transaction or posting — follow the audit trail from the break row back to the originating entry on each side and state what differs and why. Use after gl-recon has classified a break. |
| `browser-harness` | 1 | `research-and-web` | unique | Direct browser control via CDP. Use when the user wants to automate, scrape, test, or interact with web pages. Connects to the user's already-running Chrome. |
| `buyer-list` | 1 | `investment-banking` | unique | Build and organize a universe of potential acquirers for sell-side M&A processes. Identifies strategic and financial buyers, assesses fit, and prioritizes outreach. Use when preparing for a sell-side mandate, building a buyer universe, or evaluating potential partners. Triggers on "buyer list", "buyer universe", "potential acquirers", "who would buy this", "strategic buyers", or "financial sponsors". |
| `catalyst-calendar` | 1 | `equity-research` | unique | Build and maintain a calendar of upcoming catalysts across a coverage universe — earnings dates, conferences, product launches, regulatory decisions, and macro events. Helps prioritize attention and position ahead of events. Triggers on "catalyst calendar", "upcoming events", "what's coming up", "earnings calendar", "event calendar", or "catalyst tracker". |
| `cim-builder` | 1 | `investment-banking` | unique | Structure and draft a Confidential Information Memorandum for sell-side M&A processes. Organizes company information into a professional, investor-ready document with consistent formatting and narrative flow. Use when preparing sell-side materials, drafting a CIM, or organizing company data for a sale process. Triggers on "CIM", "confidential information memorandum", "offering memorandum", "info memo", "draft CIM", or "sell-side materials". |
| `clean-data-xls` | 1 | `financial-analysis` | unique | Clean up messy spreadsheet data — trim whitespace, fix inconsistent casing, convert numbers-stored-as-text, standardize dates, remove duplicates, and flag mixed-type columns. Use when data is messy, inconsistent, or needs prep before analysis. Triggers on "clean this data", "clean up this sheet", "normalize this data", "fix formatting", "dedupe", "standardize this column", "this data is messy". |
| `client-report` | 1 | `meeting-prep-agent` | unique | Generate professional client-facing performance reports with portfolio returns, allocation breakdowns, and market commentary. Suitable for quarterly or annual distribution. Triggers on "client report", "performance report", "quarterly report for [client]", "generate reports", or "client statement". |
| `client-review` | 1 | `meeting-prep-agent` | unique | Prepare for client review meetings with portfolio performance summary, allocation analysis, talking points, and action items. Pulls together account data into a concise meeting-ready format. Use before quarterly reviews, annual checkups, or ad-hoc client meetings. Triggers on "client review", "meeting prep for [client]", "quarterly review", "prep for [client name]", or "client meeting". |
| `cmux` | 1 | `agent-orchestration` | unique | Control the cmux macOS terminal app (CLI + socket API) — cmux workspaces, panes, surfaces, browser automation, notifications, settings, hooks. MUST be read before running any `cmux` command. Trigger ONLY when the user explicitly says "cmux" — a cmux pane, cmux workspace, cmux surface, or an agent running in cmux. Do NOT trigger on generic mentions of "workspace", "pane", "the other agent", or "delegate" when cmux is not named — workspaces in tmux, Ghostty, herdr, VS Code, etc. are NOT cmux. macOS only (14.0+). |
| `codex-subagent` | 1 | `agent-orchestration` | unique | Launch OpenAI Codex CLI as a subagent (ChatGPT subscription auth, no API key). Use when delegating a self-contained coding task to Codex from another agent — parallel implementation work, a second opinion, or an independent verification pass. |
| `competitive-analysis` | 2 | `financial-analysis`, `market-researcher` | DUPLICATE - merged | Framework for building competitive landscape decks — market positioning, competitor deep-dives, comparative analysis, strategic synthesis. Use when the user asks for a competitive landscape, competitor analysis, peer comparison, market positioning assessment, strategic review, or investment memo deck. Also triggers on "who are the competitors to X", "benchmark X against peers", "build a market map", or any request to systematically evaluate competitive dynamics across an industry. |
| `comps-analysis` | 4 | `financial-analysis`, `market-researcher`, `model-builder`, `pitch-agent` | DUPLICATE - merged | Build institutional-grade comparable company analyses with operating metrics, valuation multiples, and statistical benchmarking in Excel/spreadsheet format. **Perfect for:** - Public company valuation (M&A, investment analysis) - Benchmarking performance vs. industry peers - Pricing IPOs or funding rounds - Identifying valuation outliers (over/under-valued) - Supporting investment committee presentations - Creating sector overview reports **Not ideal for:** - Private companies without comparable public peers - Highly diversified conglomerates - Distressed/bankrupt companies - Pre-revenue startups - Companies with unique business models |
| `create-readonly-db-role` | 1 | `ops-and-setup` | unique | Provision a hardened SELECT-only Postgres role so AI agents can safely read a production database. Works on Supabase and any Postgres. Use when the user wants agents to query prod data, says "read-only role", "safe prod DB access for agents", or is tired of running SQL by hand for agents. Differentiator: this skill CREATES the role and wiring; day-to-day querying belongs in a project-local skill. |
| `datapack-builder` | 1 | `investment-banking` | unique | Build professional financial services data packs from various sources including CIMs, offering memorandums, SEC filings, web search, or MCP servers. Extract, normalize, and standardize financial data into investment committee-ready Excel workbooks with consistent structure, proper formatting, and documented assumptions. Use for M&A due diligence, private equity analysis, investment committee materials, and standardizing financial reporting across portfolio companies. Do not use for simple financial calculations or working with already-completed data packs. |
| `dcf-model` | 3 | `financial-analysis`, `model-builder`, `pitch-agent` | DUPLICATE - merged | Real DCF (Discounted Cash Flow) model creation for equity valuation. Retrieves financial data from SEC filings and analyst reports, builds comprehensive cash flow projections with proper WACC calculations, performs sensitivity analysis, and outputs professional Excel models with executive summaries. Use when users need to value a company using DCF methodology, request intrinsic value analysis, or ask for detailed financial modeling with growth projections and terminal value calculations. |
| `dd-checklist` | 1 | `private-equity` | unique | Generate and track comprehensive due diligence checklists tailored to the target company's sector, deal type, and complexity. Covers all major workstreams with request lists, status tracking, and red flag escalation. Use when kicking off diligence, organizing a data room review, or tracking outstanding items. Triggers on "dd checklist", "due diligence tracker", "diligence request list", "what do we still need", or "data room review". |
| `dd-meeting-prep` | 1 | `private-equity` | unique | Prepare for due diligence meetings — management presentations, expert network calls, customer references, and advisor sessions. Generates targeted question lists, benchmarks to reference, and red flags to probe. Use before any diligence meeting or call. Triggers on "prep for management meeting", "diligence call prep", "expert call questions", "customer reference questions", or "meeting prep for [company]". |
| `deal-screening` | 1 | `private-equity` | unique | Quickly screen inbound deal flow — CIMs, teasers, and broker materials — against the fund's investment criteria. Extracts key deal metrics, runs a pass/fail framework, and outputs a one-page screening memo. Use when reviewing new deal flow, triaging inbound materials, or deciding whether to take a first call. Triggers on "screen this deal", "review this CIM", "should we look at this", "triage this teaser", or "deal screening". |
| `deal-sourcing` | 1 | `private-equity` | unique | PE deal sourcing workflow — discover target companies, check CRM for existing relationships, and draft personalized founder outreach emails. Use when sourcing new deals, prospecting companies in a sector, or reaching out to founders. Triggers on "find companies", "source deals", "draft founder email", "check if we've seen this company", or "outreach to founder". |
| `deal-tracker` | 1 | `investment-banking` | unique | Track multiple live deals with milestones, deadlines, action items, and status updates. Maintains a deal pipeline view and surfaces upcoming deadlines and overdue items. Use when managing a book of business, tracking process milestones, or preparing for weekly deal reviews. Triggers on "deal tracker", "deal status", "where are we on", "process update", "deal pipeline", or "weekly deal review". |
| `decisions` | 1 | `thinking-and-docs` | unique | Ask the agent to list all choices it made during the current work that it is not confident of. Manual-only; invoke with /decisions. |
| `deck-refresh` | 2 | `financial-analysis`, `pitch-agent` | DUPLICATE - merged | Updates a presentation with new numbers — quarterly refreshes, earnings updates, comp rolls, rebased market data. Use whenever the user asks to "update the deck with Q4 numbers", "refresh the comps", "roll this forward", "swap in the new earnings", "change all the $485M to $512M", or any request to swap figures across an existing deck without rebuilding it. |
| `deep-research` | 1 | `research-and-web` | unique | Run a deep, source-backed research query via DeepAPI (go to deepapi.co to get an API key) POST /v1/research/deep. Builds a rigorous one-paragraph research prompt (per research-prompt rules), fires it, and saves a cited markdown report. Use when the user asks for "deep research", "deepapi research", "perplexity deep research" (legacy trigger), or any deep source-backed research run. Differentiator vs the deepapi skill: this is the full research workflow (prompt + run + report file), not raw endpoint access. |
| `deepapi` | 1 | `research-and-web` | unique | Use DeepAPI for all regular web searches (POST /v1/search/web) and for any deep research you perform (POST /v1/research/deep), instead of built-in search or research tools. Use it for all scraping of the web (websites, LinkedIn, GitHub, X/Twitter, YouTube — POST /v1/scrape/*) instead of built-in fetch or browser tools. Platform lookups (GitHub, YouTube, X/Twitter, LinkedIn, Instagram) have dedicated search endpoints — prefer them over web search. Also use it to draft and send safe email, and generate images with DEEPAPI_API_BASE_URL and DEEPAPI_API_KEY. |
| `distribute-skill-to-all-agents` | 1 | `skill-authoring` | unique | Distribute a skill across the 4 agent skill folders (Codex, Claude Code, Pi, Hermes) so all agents see it. Use when the user says "distribute this skill", "sync skills across agents", or after creating/updating a skill that should be global. Covers the symlink layout and the ~/.pi/agent/skills trap. |
| `earnings-analysis` | 2 | `earnings-reviewer`, `equity-research` | DUPLICATE - merged | Create professional equity research earnings update reports (8-12 pages, 3,000-5,000 words) analyzing quarterly results for companies already under coverage. Fast-turnaround format focusing on beat/miss analysis, key metrics, updated estimates, and revised thesis. Includes 1-3 summary tables and 8-12 charts. Use when user requests "earnings update", "quarterly update", "earnings analysis", "Q1/Q2/Q3/Q4 results", or post-earnings report. |
| `earnings-preview` | 2 | `earnings-reviewer`, `equity-research` | DUPLICATE - merged | Build pre-earnings analysis with estimate models, scenario frameworks, and key metrics to watch. Use before a company reports quarterly earnings to prepare positioning notes, set up bull/bear scenarios, and identify what will move the stock. Triggers on "earnings preview", "what to watch for [company] earnings", "pre-earnings", "earnings setup", or "preview Q[X] for [company]". |
| `effective-agent-skills` | 1 | `skill-authoring` | unique | How to write effective agent skills — what to do, what not to do, anatomy, progressive disclosure, design patterns, anti-patterns, testing, security. Read this whenever a skill (Claude Skill, Agent Skill, SKILL.md) is being created, edited, reviewed, or debugged. Use when the user says "create a skill", "new skill", "update this skill", "improve a skill", "why isn't my skill triggering", or anything else involving authoring or editing SKILL.md files. |
| `fable-review` | 1 | `agent-orchestration` | unique | Launch a Fable 5 Max 1M subagent to do a deep, neutral senior-developer review of the current work and report its findings back verbatim. Use when the user says "/fable-review", "fable review", or asks for Fable to review the code. Differentiator: reviewer model is Fable 5 Max 1M — for a GPT reviewer use gpt-review. |
| `fable-safe-prompt` | 1 | `agent-orchestration` | unique | Rewrite a user's prompt to reduce the chance it trips Claude Fable 5's server-side safety classifiers (cyber/bio guardrails that force-route to Opus 4.8 or return stop_reason "refusal"). Use when the user hands you a prompt that touches cybersecurity, auth, exploits, malware, pentesting, or other dual-use topics and asks to make it "Fable-safe", "guardrail-safe", "won't get flagged/refused/downgraded", or to rewrite it so Fable 5 won't block it. |
| `fireflies-transcript` | 1 | `research-and-web` | unique | Pull raw meeting transcripts from the user's Fireflies.ai notetaker via its GraphQL API, using the key saved globally on this machine. Use when the user wants a call transcript, meeting notes, "what was said on the call", onboarding-call transcripts, or Fireflies data. Differentiator: Fireflies meeting recordings only — for YouTube videos use youtube-transcript. |
| `git-worktree` | 1 | `agent-orchestration` | unique | Use git worktrees to run multiple coding agents in parallel on one repo without collisions. Use when starting a task in a shared repo, when the user says "worktree", "parallel agents", "one worktree per task", or when agents keep overwriting each other's changes. Covers creating worktrees, making them as complete as the main checkout (.env files, dependencies, databases, ports), merging back, and cleanup. |
| `gl-recon` | 2 | `fund-admin`, `gl-reconciler` | DUPLICATE - merged | Reconcile general ledger to subledger for a trade date or period — match at the position or transaction level, surface breaks, and classify each break by likely cause. Use for daily or month-end recon runs across asset classes. |
| `global-agent-guardrails` | 1 | `ops-and-setup` | unique | One shared denylist of catastrophic shell commands (rm -rf on / or ~, dd/mkfs, sudo rm, fork bombs, curl\|sh, git push --force, gh repo delete) enforced as a PreToolUse/pre-exec guard across every AI coding agent on the machine — Cursor, Claude Code, Codex, OpenCode, Pi, Hermes, Grok, Droid, Devin. Use when adding or tuning blocked-command patterns, wiring the guard into a new agent or a new machine, debugging why a command was (or was not) blocked, or when the user mentions command guard, guardrails, dangerous command hook, or PreToolUse safety. |
| `goal-loop` | 1 | `agent-orchestration` | unique | Explain and write effective instructions for the `/goal` feature — the persistent self-checking agent loop (plan → act → test → review → iterate), available in agents like Codex, Claude Code, and Hermes Agent. Use when the user mentions `/goal`, "goal loop", "Ralph loop", wants to kick off a long-running autonomous agent run, asks how to write a goal prompt, or wants a one-paragraph goal instruction drafted. |
| `google-safe-browsing` | 1 | `ops-and-setup` | unique | Prevent and fix Google Safe Browsing "Dangerous site" flags. Use when launching a public web app, buying/picking a domain, building a login or signup page, or when any site shows a red "Dangerous site" / "Deceptive site" warning in Chrome, Brave, Safari, Firefox, or Edge. Triggers on "dangerous site", "deceptive site", "site blocked", "safe browsing", "phishing flag", "red warning screen". |
| `gpt-review` | 1 | `agent-orchestration` | unique | Launch a GPT 5.6 Sol Max subagent to do a deep, neutral senior-developer review of the current work and report its findings back verbatim. Use when the user says "/gpt-review", "gpt review", or asks for GPT to review the code. Differentiator: reviewer model is GPT 5.6 Sol Max — for a Fable reviewer use fable-review. |
| `ib-check-deck` | 2 | `financial-analysis`, `pitch-agent` | DUPLICATE - merged | Investment banking presentation quality checker. Reviews a pitch deck or client-ready presentation for (1) number consistency across slides, (2) data-narrative alignment, (3) language polish against IB standards, (4) visual and formatting QC. Use whenever the user asks to review, check, QC, proof, or do a final pass on a deck, pitch, or client materials — including requests like "check my numbers", "reconcile figures across slides", "is this client-ready", or "what am I missing before I send this out". |
| `ic-memo` | 2 | `private-equity`, `valuation-reviewer` | DUPLICATE - merged | Draft a structured investment committee memo for PE deal approval. Synthesizes due diligence findings, financial analysis, and deal terms into a professional IC-ready document. Use when preparing for investment committee, writing up a deal, or creating a formal recommendation. Triggers on "write IC memo", "investment committee memo", "deal write-up", "prepare IC materials", or "recommendation memo". |
| `idea-generation` | 2 | `equity-research`, `market-researcher` | DUPLICATE - merged | Systematic stock screening and investment idea sourcing. Combines quantitative screens, thematic research, and pattern recognition to surface new long and short ideas. Use when looking for new ideas, running screens, or conducting thematic sweeps. Triggers on "idea generation", "stock screen", "find ideas", "what looks interesting", "screen for", "new ideas", or "pitch me something". |
| `initiating-coverage` | 1 | `equity-research` | unique | Create institutional-quality equity research initiation reports through a 5-task workflow. Tasks must be executed individually with verified prerequisites - (1) company research, (2) financial modeling, (3) valuation analysis, (4) chart generation, (5) final report assembly. Each task produces specific deliverables (markdown docs, Excel models, charts, or DOCX reports). Tasks 3-5 have dependencies on earlier tasks. |
| `investment-proposal` | 1 | `meeting-prep-agent` | unique | Create professional investment proposals for prospective clients. Covers the firm's approach, proposed allocation, expected outcomes, and fee structure. Use when pitching new clients or presenting a new investment strategy. Triggers on "investment proposal", "prospect presentation", "pitch new client", "proposal for [client]", or "new client presentation". |
| `kyc-doc-parse` | 1 | `operations` | unique | Parse an investor or client onboarding packet into structured KYC fields — identity, ownership, control, source of funds, and document inventory. Use as the first step of KYC screening; output feeds the rules engine. |
| `kyc-rules` | 1 | `operations` | unique | Apply the firm's KYC/AML rules grid to a parsed onboarding record — assign a risk rating, list every rule outcome with the rule cited, and flag what's missing or escalation-worthy. Use after kyc-doc-parse; this skill decides nothing, it scores and routes. |
| `launch-subagent` | 1 | `agent-orchestration` | unique | Read this BEFORE launching any subagent (Task tool, background agents, parallel agents, best-of-N, delegating work to another agent). Hard model rules for subagents plus consensus principles for using them well. Triggers: launch a subagent, spawn agents, run agents in parallel, delegate to a subagent. |
| `lbo-model` | 3 | `financial-analysis`, `model-builder`, `pitch-agent` | DUPLICATE - merged | This skill should be used when completing LBO (Leveraged Buyout) model templates in Excel for private equity transactions, deal materials, or investment committee presentations. The skill fills in formulas, validates calculations, and ensures professional formatting standards that adapt to any template structure. |
| `level-up` | 1 | `thinking-and-docs` | unique | Gauge the user's technical + product knowledge through 7 adaptive questions, log verbatim answers with honest ratings, and grow a learning plan from the gaps found. Use when the user says "level up", "level-up session", "quiz me", "gauge my knowledge", or wants a new assessment round. Differentiator: this finds and maps gaps; the `teach` skill delivers lessons on them. |
| `macbook-metrics-setup` | 1 | `ops-and-setup` | unique | Replicate the macbook-metrics setup on any Mac — a local, always-on system-metrics collector (CPU, GPU, RAM, disk, network, battery, thermals) built as a Swift CLI, run by launchd every 60s, stored in SQLite, and backed up to a private GitHub repo. Use when someone wants long-term Mac performance tracking, asks how macbook-metrics works, or wants to set up the same monitoring on a new machine. Differentiator: covers the full architecture and setup ideology, not day-to-day querying of an existing install. |
| `merger-model` | 1 | `investment-banking` | unique | Build accretion/dilution analysis for M&A transactions. Models pro forma EPS impact, synergy sensitivities, and purchase price allocation. Use when evaluating a potential acquisition, preparing merger consequences analysis for a pitch, or advising on deal terms. Triggers on "merger model", "accretion dilution", "M&A model", "pro forma EPS", "merger consequences", or "deal impact analysis". |
| `model-update` | 2 | `earnings-reviewer`, `equity-research` | DUPLICATE - merged | Update financial models with new data — quarterly earnings, management guidance, macro changes, or revised assumptions. Adjusts estimates, recalculates valuation, and flags material changes. Use after earnings, guidance updates, or when assumptions need refreshing. Triggers on "update model", "plug earnings", "refresh estimates", "update numbers for [company]", "new guidance", or "revise estimates". |
| `morning-note` | 2 | `earnings-reviewer`, `equity-research` | DUPLICATE - merged | Draft concise morning meeting notes summarizing overnight developments, trade ideas, and key events for coverage stocks. Designed for the 7am morning meeting format — tight, opinionated, actionable. Triggers on "morning note", "morning meeting", "what happened overnight", "trade idea", "morning call prep", or "daily note". |
| `nav-tieout` | 2 | `fund-admin`, `statement-auditor` | DUPLICATE - merged | Tie an LP statement to the fund's NAV pack — recompute the LP's capital account from the NAV components and flag any line that doesn't agree. Use before LP statements are distributed. |
| `next-decision` | 1 | `thinking-and-docs` | unique | Drill open decisions one at a time — present the most important decision not yet clarified, give the top four choices, state a preference, ask the user. Use when the user says "next decision", "one decision at a time", or a plan has several unresolved choices. Differentiator: forward-looking; the decisions skill is retrospective (choices already made). Can be invoked with /next-decision. |
| `nuke-cursor-app` | 1 | `ops-and-setup` | unique | Safely quit and kill ALL Cursor IDE processes on the user's MacBook to recover from the known renderer memory leak that makes Cursor lag. Manual-only — run ONLY when the user explicitly invokes it (/nuke-cursor-app, "nuke cursor"). Differentiator: kills the Cursor desktop app; cursor-cli sessions are unrelated. |
| `online-shopping` | 1 | `research-and-web` | unique | Research any online purchase with DeepAPI — fair-price checks, best deals, where to buy, shop trust. Load whenever the user is shopping or buying anything online: mentions buying a product, comparing prices, "is this a good price", "where can I get X", or attaches a product photo or listing screenshot. Research only — never places orders. |
| `pi-custom-model` | 1 | `ops-and-setup` | unique | Register a custom or variant model (e.g. an OpenRouter ":nitro" / ":floor" / ":exacto" slug) in the Pi Agent so it can be set as the global default. Use when Pi silently falls back to a different model (e.g. moonshotai/kimi-k2.6) after setting defaultModel, or when a model slug isn't in Pi's bundled list. Triggers on "Pi reset my model", "Pi won't use this model", "add a model to Pi", "Pi default keeps reverting". |
| `pi-web-search` | 1 | `research-and-web` | unique | ONLY for Pi Agents — all other agents have their own web tools. How Pi accesses the web via the pi-web-access package — search, fetch URLs/PDFs/YouTube/GitHub. Use whenever a Pi task needs current info, docs, news, prices, or content from a specific URL. |
| `pitch-deck` | 2 | `investment-banking`, `pitch-agent` | DUPLICATE - merged | Populates investment banking pitch deck templates with data from source files. Use when: user provides a PowerPoint template to fill in, user has source data (Excel/CSV) to populate into slides, user mentions populating or filling a pitch deck template, or user needs to transfer data into existing slide layouts. Not for creating presentations from scratch. |
| `portfolio-monitoring` | 2 | `private-equity`, `valuation-reviewer` | DUPLICATE - merged | Track and analyze portfolio company performance against plan. Ingests monthly/quarterly financial packages (Excel, PDF), extracts KPIs, flags variances to budget, and produces summary dashboards. Use when reviewing portfolio company financials, preparing board materials, or monitoring covenant compliance. Triggers on "review portfolio company", "monthly financials", "how is [company] performing", "covenant check", or "portfolio update". |
| `ppt-template-creator` | 1 | `financial-analysis` | unique | Creates self-contained PPT template SKILLS (not presentations) from user-provided PowerPoint templates. Use ONLY when a user wants to create a reusable skill from their template. For creating actual presentations, use the pptx skill instead. |
| `pptx-author` | 4 | `financial-analysis`, `market-researcher`, `meeting-prep-agent`, `pitch-agent` | DUPLICATE - merged | Produce a .pptx file on disk (headless) instead of driving a live PowerPoint document — for managed-agent sessions with no open Office app. |
| `process-letter` | 1 | `investment-banking` | unique | Draft process letters and bid instructions for sell-side M&A processes. Covers initial indication of interest (IOI) instructions, final bid procedures, and management meeting logistics. Triggers on "process letter", "bid instructions", "IOI letter", "bid procedures", "final round letter", or "management meeting invite". |
| `prod-push` | 1 | `ops-and-setup` | unique | Push to GitHub main and babysit the change until it is verifiably live in production, fixing CI and deploy failures along the way. Use when the user says "push", "push to github", "push to prod", "ship it", or "deploy". Differentiator: pushing requires the user's explicit go-ahead; this is the procedure for AFTER the user gives it (this repo's CI gate + Vercel promotion). |
| `prompt-me` | 1 | `thinking-and-docs` | unique | Prompt the user with pointed questions to extract what is in his head about a project — remaining work, what is being avoided, what really matters, what does not. Use when the user says "prompt me", "ask me questions", or wants the agent to figure out priorities by questioning him. |
| `push-skill-to-github` | 1 | `skill-authoring` | unique | Commit and push agent-skill changes to the user's private skills GitHub repo (rooted at ~/.agents). Use after creating or updating any skill, when the user says "push the skill", "push skills to github", "save the skill to my repo", or "update the skills repo". Handles staging, committing, and pushing directly in the current shell — works in any agent, no cmux needed. |
| `read-all-adrs` | 1 | `thinking-and-docs` | unique | Read every ADR markdown file in the project's docs/adr/ folder so you have full context on past decisions. Use only when the user explicitly calls it. |
| `remind` | 1 | `thinking-and-docs` | unique | Rewrite the last response simpler and shorter in plain English, prefixed with a 3-5 sentence TLDR of the conversation so far. Manual-only, invoked as /remind. |
| `research-prompt` | 1 | `research-and-web` | unique | Write a single-paragraph Deep Research prompt to hand to a human researcher (or a deep-research AI). Use when the user wants a research brief, a "deep research prompt", a one-paragraph task for a researcher, or asks "what should our researcher look for". Produces ONE tight paragraph with full context, numbered sub-questions, and per-finding output format. |
| `returns-analysis` | 2 | `private-equity`, `valuation-reviewer` | DUPLICATE - merged | Build quick IRR/MOIC sensitivity tables for PE deal evaluation. Models returns across entry multiple, leverage, exit multiple, growth, and hold period scenarios. Use when sizing up a deal, stress-testing assumptions, or preparing IC returns exhibits. Triggers on "returns analysis", "IRR sensitivity", "MOIC table", "what's the return at", "model the returns", or "back of the envelope". |
| `roll-forward` | 2 | `fund-admin`, `month-end-closer` | DUPLICATE - merged | Build a roll-forward schedule for a balance-sheet account — beginning balance plus activity less reversals equals ending balance, with each component tied to GL. Use for month-end close packages and audit support. |
| `run-deep-swe` | 1 | `agent-orchestration` | unique | Score any AI model on the DeepSWE coding-agent benchmark via the OpenRouter API. Use when the user wants an independent, reproducible coding-agent eval — "run DeepSWE", "benchmark this model on DeepSWE", "score model X on the coding benchmark", "test a model via OpenRouter on DeepSWE", or to verify vendor-reported coding scores. Covers setup, the OpenRouter wiring for mini-swe-agent, single-task / subset / full 113-task runs, and leaderboard submission. |
| `save-idea` | 1 | `thinking-and-docs` | unique | Quickly capture a content idea into ~/code/content from any repo or chat. Video ideas go to VIDEO-IDEAS.md; smaller podcast topics, guest ideas, questions, and AI observations go to TOPICS.md. Every entry gets a source line referencing the chat and repo it came from. Use when the user says "/save-idea", "save this idea", "video idea", "add a topic", "write this down for a video/podcast". Differentiator: appends to the user's content backlog — not a reminder, task, or general note tool. |
| `sector-overview` | 3 | `equity-research`, `market-researcher`, `pitch-agent` | DUPLICATE - merged | Create comprehensive industry and sector landscape reports covering market dynamics, competitive positioning, key players, and thematic trends. Use for client requests, sector initiations, thematic research pieces, or internal knowledge building. Triggers on "sector overview", "industry report", "market landscape", "sector analysis", "industry deep dive", or "thematic research". |
| `setup-help` | 1 | `ops-and-setup` | unique | Walk the user through setting up anything step by step. Use when the user asks for help setting up, configuring, installing, or getting something working — "help me set up X", "walk me through this", "setup-help". Differentiator: gives one current step at a time, then always lists every remaining setup step after each response. |
| `short` | 1 | `thinking-and-docs` | unique | Manually-invoked skill that forces the agent to compress its current answer — strip filler, simplify wording, and cut length while keeping the substance. Use when the user says "short", "shorter", "simpler", "too long", "tl;dr", or wants a more concise version of the previous response. |
| `skill-creator` | 2 | `executive-deck-skill-suite`, `financial-analysis` | COLLISION - kept separate | Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, or optimize a skill's description for better triggering accuracy. |
| `teaser` | 1 | `investment-banking` | unique | Draft anonymous one-page company teasers for sell-side M&A processes. Creates a compelling summary without revealing the company's identity, designed to gauge buyer interest before NDA execution. Triggers on "teaser", "blind teaser", "anonymous profile", "one-pager for process", or "draft teaser for sell-side". |
| `thesis-tracker` | 1 | `equity-research` | unique | Maintain and update investment theses for portfolio positions and watchlist names. Track key data points, catalysts, and thesis milestones over time. Use when updating a thesis with new information, reviewing position rationale, or checking if a thesis is still intact. Triggers on "update thesis for [company]", "is my thesis still intact", "thesis check", "add data point to [company]", or "review my positions". |
| `unit-economics` | 1 | `private-equity` | unique | Analyze unit economics for PE targets — ARR cohorts, LTV/CAC, net retention, payback periods, revenue quality, and margin waterfall. Essential for software/SaaS, recurring revenue, and subscription businesses. Use when evaluating revenue quality, building a cohort analysis, or assessing customer economics. Triggers on "unit economics", "cohort analysis", "ARR analysis", "LTV CAC", "net retention", "revenue quality", or "customer economics". |
| `value-creation-plan` | 1 | `private-equity` | unique | Structure post-acquisition value creation plans with revenue, cost, and operational levers mapped to an EBITDA bridge. Includes 100-day priorities, KPI targets, and accountability frameworks. Use when planning post-close execution, preparing operating partner materials, or building a board-ready value creation roadmap. Triggers on "value creation plan", "100-day plan", "post-close plan", "EBITDA bridge", "operating plan", or "value creation levers". |
| `variance-commentary` | 2 | `fund-admin`, `month-end-closer` | DUPLICATE - merged | Write flux commentary for every P&L and balance-sheet line over threshold — current vs prior period and vs budget, with the driver explained from underlying activity. Use for the month-end close package and management reporting. |
| `vps-server-management` | 1 | `ops-and-setup` | unique | Use when the user wants to manage their VPS servers and the AI agents running inside them — connecting, deploying, monitoring, restarting, and operating remote hosts and their agents. Triggers on VPS, server management, remote host, SSH into server, manage my servers, agents on the server. |
| `xlsx-author` | 8 | `earnings-reviewer`, `financial-analysis`, `gl-reconciler`, `model-builder`, `month-end-closer`, `pitch-agent`, `statement-auditor`, `valuation-reviewer` | DUPLICATE - merged | Produce a .xlsx file on disk (headless) instead of driving a live Excel workbook — for managed-agent sessions with no open Office app. |
| `youtube-transcript` | 1 | `research-and-web` | unique | Use whenever the user needs the transcript of a YouTube video — fetching, extracting, downloading, or pulling captions/subtitles/transcript text from a YouTube URL. Triggers on "get the transcript", "transcript of this video", "pull the captions", "download subtitles", "what does this YouTube video say". Primary path is DeepAPI (go to deepapi.co to get an API key); yt-dlp is the local fallback. |

---

## Validation & exclusions

A folder is indexed only if `skills/<folder>/SKILL.md` exists and passes both rule sets audited by `tools/skills_audit.py`:

- **Agent Skills specification** (<https://agentskills.io/specification>): `name` 1-64 chars, lowercase letters/digits/single hyphens, not starting or ending with a hyphen, equal to the folder name; `description` 1-1024 chars; `compatibility` <= 500 chars; well-formed YAML frontmatter.
- **Claude platform rules**: no `anthropic`/`claude` in `name`; no XML tags in `name` or `description`.

Spec deviations that Claude Code accepts are *warnings*, not exclusions (YAML-list `allowed-tools`, non-string `metadata` values, non-spec top-level keys such as `author`/`version`, bodies over 500 lines). Warning counts across indexed skills: `ALLOWED_TOOLS_LIST` x32, `BODY_LENGTH` x104, `METADATA_NON_STRING` x17, `UNKNOWN_KEYS` x132.

Result: **343 valid top-level skills** of 350 folders with a `SKILL.md`; 7 excluded; 22 grouping folders; 125 nested `SKILL.md` files inside valid skills are parts of those skills and are not indexed separately.

### Excluded: top-level folders with an invalid `SKILL.md` (7)

| Folder | Rule broken | Detail | Suggested fix |
|---|---|---|---|
| `claude-design` | `NAME_RESERVED_WORD` | name contains reserved word 'claude' (rejected by Claude skill upload) | rename the folder and `name` (drop the reserved word) before uploading to Claude |
| `claude-md` | `NAME_RESERVED_WORD` | name contains reserved word 'claude' (rejected by Claude skill upload) | rename the folder and `name` (drop the reserved word) before uploading to Claude |
| `evidence-driven-testing` | `COMPAT_INVALID` | compatibility must be a string of 1-500 chars | shorten `compatibility` to <= 500 characters |
| `git-guardrails-claude-code` | `NAME_RESERVED_WORD` | name contains reserved word 'claude' (rejected by Claude skill upload) | rename the folder and `name` (drop the reserved word) before uploading to Claude |
| `hono` | `DESC_XML_TAG` | description contains an XML tag | remove angle-bracket tags from `description` (use plain words or backticks) |
| `rust-web` | `DESC_XML_TAG` | description contains an XML tag | remove angle-bracket tags from `description` (use plain words or backticks) |
| `vue-3-nuxt` | `DESC_XML_TAG` | description contains an XML tag | remove angle-bracket tags from `description` (use plain words or backticks) |

These were **not modified**; fixing them is a separate, reviewable change.

### Excluded: invalid bundled sub-skills (4)

| Path | Rule broken | Detail |
|---|---|---|
| `skills/executive-deck-skill-suite/skills/executive-strategy-deck` | `NAME_FOLDER_MISMATCH` | name 'building-executive-decks' does not match folder 'executive-strategy-deck' |
| `skills/executive-deck-skill-suite/skills/pptx` | `NAME_FOLDER_MISMATCH` | name 'ppt' does not match folder 'pptx' |
| `skills/investment-banking/skills/strip-profile` | `NAME_FOLDER_MISMATCH` | name 'fsi-strip-profile' does not match folder 'strip-profile' |
| `skills/skill-authoring/folder-specific-claude-and-agents-md` | `NAME_RESERVED_WORD` | name contains reserved word 'claude' (rejected by Claude skill upload) |

### Grouping folders without a top-level `SKILL.md` (22)

`agent-orchestration`, `docs`, `earnings-reviewer`, `equity-research`, `executive-deck-skill-suite`, `financial-analysis`, `fund-admin`, `gl-reconciler`, `investment-banking`, `market-researcher`, `meeting-prep-agent`, `model-builder`, `month-end-closer`, `operations`, `ops-and-setup`, `pitch-agent`, `private-equity`, `research-and-web`, `skill-authoring`, `statement-auditor`, `thinking-and-docs`, `valuation-reviewer`.

### Loose files in `skills/` (not skills: no sub-folder)

`CODE_REVIEW_CONSOLIDATION_SUMMARY.txt`, `INVENTORY.txt`, `agents-skill.md`, `bundled_skills_selection_for_modern_web_project.md`, `droid-skills-list.md`, `prompt-to-add-description.txt`, `proposed_consolidation_code_review_audit.txt`, `proposed_consolidation_execution_feedback.txt`, `skill-creator-selector.md`, `skills-catalog.md`.

