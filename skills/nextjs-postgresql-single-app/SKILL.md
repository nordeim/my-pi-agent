---
name: nextjs-postgresql-single-app
description: >
  Production-grade reference for building content-driven marketing sites and transactional funnel apps on Next.js 16 + React 19 + Tailwind CSS v4 (CSS-first @theme) + Drizzle ORM + PostgreSQL 17 in a single-app (npm, no monorepo) with TypeScript strict. Covers App Router RSC (force-dynamic), file corpus → catalog → idempotent ensureSeeded() projection → Pool singleton (globalThis), Drizzle pgTable migrations, 43 static/dynamic pages, lead-capture funnel (validate → match → persist), rate limiting, health/sitemap/redirects, editorial design tokens, and WCAG AAA. Includes reusable patterns for single-Pool persistence, file-backed seeding, content ingestion, and pre-ship gates (lint/typecheck/test/build/e2e). Applicable to any full-stack TypeScript marketing, funnel, lead-gen, or content-driven SaaS using this stack.
version: 1.8.0
tags: [nextjs16, react19, tailwind-v4, drizzle, postgres17, vitest, playwright, marketing, funnel, single-app]
---

# home-financing (ModFii) — Production Web App Skill

Refer to the codebase in `https://github.com/nordeim/home-financing.git` as the foundation/example to scaffold other projects using similar tech stacks.

Reusable distillation for any Next.js 16 App Router + React 19 + TypeScript 5.9 strict + Tailwind CSS v4 CSS-first @theme + Drizzle ORM 0.45 + PostgreSQL 17 + pg Pool singleton + Vitest 4.1 + Playwright 1.63 project. Generalizes beyond mortgages to any content-driven marketing + transactional funnel app (editorial guides, calculators, lead capture, lender/product matching). What it teaches: 20-section production reference distilled via Six-Phase Archaeology — Project Identity & Design Philosophy (editorial + brutalist restraint, forest/cream/amber tokens), Tech Stack & Versions (pinned), Bootstrapping & Config (tsconfig strict, next.config redirects/images.unoptimized, eslint flat, drizzle.config dual, docker-compose PG17 + pgcrypto/pg_trgm), Design System (verbatim @theme + radii/shadow/ease + typography), 5-Layer Architecture (file corpus → catalog → ensureSeeded projection → Pool singleton → RSC/force-dynamic → redirects), Component Map (Server Components by default, 6 use-client islands), Hooks (inlined useId/adjust-during-render/passive: true/body-lock), Content Ingestion (file-backed JSON → ensureSeeded count>0 + onConflictDoNothing → PG, 152 sitemap locs), A11y (WCAG AAA contrast/focus/prefers-reduced-motion/axe critical: []), 14 Anti-Patterns + Debugging Guide (H4/OOM server kill, second Pool EMFILE, .env leak d572d73, missing hero images, setState-in-effect, tailwind.config drift), Pre-Ship Gate (db:setup → lint 0/0 → typecheck → test 41/41 → build 43/43 (35+8) → e2e 121/121), Lessons/Pitfalls/Best Practices, 6 Copy-Paste Patterns (canonical funnel rateLimit→json→validate→seed→match→persist, health probe, idempotent projection, PMI 0.0065 + 1.15×, sitemap), Responsive/Z-Index/Color (hex-exact) & 8-domain TypeScript Interfaces.

Discoverability: Matches nextjs16, react19, app-router, rsc, tailwind4, drizzle, postgres17, vitest, playwright, server-components, drizzle-kit, pg-pool, next-font, lucide-react. Use to scaffold, debug, onboard, or ship any similar full-stack marketing/funnel app without repeating 2026-09-11 incidents.

**Companion Documents:** `Project_Architecture_Document.md` v1.0 (blueprint) · `CLAUDE.md` (agent spec, ~600 lines) · `AGENTS.md` (cheat-sheet) · `README.md` (operator guide) · `docs/REMEDIATION_PLAN_pass4.md` (pass-4 evidence)
**Last Updated:** 2026-09-15 (v1.8 — pass 9 drift alignment D-01→D-07: STATIC_PATHS 40→39, build 36+7/42+8→35+8, E2E 61/82→121, radii 1.25/1.5→0.625/0.75/1.0, MORE 4→2, blur-md→lg; validation `docs/VALIDATION_REPORT_SKILL_2026-09-15.md` 11 drifts patched. Pass 8: audit remediation `.env` hygiene + vitest 4.1.11; pass 7: live-source parity; pass 6: audit)
**Project State:** 41 Vitest (11+13+9+8, incl. H4/OOM regression) + 121 Playwright per project (121/121 with DB, 120/121 DB-less — 103 declarations + data-driven loops: smoke 8 + seo 16 + funnel 5 + assets 19 + parity 73) · 43/43 Next build · PG 17 `8/40/50/23/59/5` seeded · `lint 0/0` · `typecheck` pass
**Audience:** AI Coding Agents, Senior Engineers, Tech Leads, DevOps, Onboarding Engineers
**Rule:** Every rule in this document traces to a specific file, test, or live probe. Nothing is here "because it's popular."

> **How to use this document**
> - **New agent / engineer** → Read §1 (Identity) → §2 (Stack) → §3 (Bootstrap) → §5 (Architecture + Golden Rule) → §11 (Pre-Ship) then run `npm run db:setup && npm run lint && npm run typecheck && npm run test && npm run build && npm run e2e`.
> - **Fixing a bug** → Jump to §9 (Anti-Patterns) → §10 (Debugging Guide) → §12 (Lessons). Every anti-pattern has a test that prevents recurrence.
> - **Adding a feature** → §5 (Layer Model + Component Map) → §7 (Content) → §15 (Patterns) → §20 (Interfaces). Don't bypass the layer.
> - **Shipping** → §11 (Pre-Ship Checklist) is the gate. No `any`, no second `Pool`, no `tailwind.config.*`, no DB hand-edit must survive it.
> - **Onboarding a team** → Distribute this file + PAD + `AGENTS.md`. PAD is the topology/ADR authority; this SKILL is the *negative space* — what not to do, how to debug, how to avoid repeating 2026-09-11 incidents.

---

## Table of Contents

1. [Project Identity & Design Philosophy](#1-project-identity--design-philosophy)
2. [Tech Stack & Environment](#2-tech-stack--environment)
3. [Bootstrapping & Configuration](#3-bootstrapping--configuration)
4. [The Design System (Code-First)](#4-the-design-system-code-first)
5. [Component Architecture & Patterns](#5-component-architecture--patterns)
6. [Custom Hooks Deep Dive](#6-custom-hooks-deep-dive)
7. [Content Management & Data Ingestion](#7-content-management--data-ingestion)
8. [Accessibility (WCAG AAA) Implementation](#8-accessibility-wcag-aaa-implementation)
9. [Anti-Patterns & Common Bugs](#9-anti-patterns--common-bugs)
10. [Debugging Guide](#10-debugging-guide)
11. [Pre-Ship Checklist](#11-pre-ship-checklist)
12. [Lessons Learnt & How to Avoid Them](#12-lessons-learnt--how-to-avoid-them)
13. [Pitfalls to Avoid](#13-pitfalls-to-avoid)
14. [Best Practices](#14-best-practices)
15. [Coding Patterns](#15-coding-patterns)
16. [Coding Anti-Patterns](#16-coding-anti-patterns)
17. [Responsive Breakpoint Reference](#17-responsive-breakpoint-reference)
18. [Z-Index Layer Map](#18-z-index-layer-map)
19. [Color Reference (Complete)](#19-color-reference-complete)
20. [The Complete TypeScript Interface Reference](#20-the-complete-typescript-interface-reference)
- [Appendix A: Architecture Decision Records](#appendix-a-architecture-decision-records)
- [Appendix B: Pipeline Costs](#appendix-b-pipeline-costs)
- [Appendix C: Audit History](#appendix-c-audit-history)
- [Appendix D: Live-Site Validation & Quick Reference Card](#appendix-d-live-site-validation--quick-reference-card)
- [Appendix E: The Meticulous Approach (6-Phase Workflow)](#appendix-e-the-meticulous-approach-6-phase-workflow)

---

## 1. Project Identity & Design Philosophy

**One-sentence identity:** ModFii (`home-financing`, legacy `nextjs-postgresql-template`) is a **content + transaction hybrid** for prefab homebuyers — SEO-driven editorial (23 articles, 50 state guides, 40 manufacturers) plus a single 13-field pre-qual funnel (12 required + optional `manufacturerSlug`) (`/get-started` → `validateApplication` → `matchLenders` → `applications` + top-4 `application_matches`) that closes the loop on modular/manufactured/ADU/tiny-home financing where traditional lenders fail.

**Design thesis — Editorial + Brutalist Restraint (Luxury-Dark Cinematic without purple slop):**

| Tenet | Expression in Code |
|-------|-------------------|
| **Intentional minimalism** — whitespace as structure, not emptiness | `Container max-w-[1400px] mx-auto px-4 md:px-8` + `PageHero` centered `max-w-4xl` + `GuideView grid lg:grid-cols-[1fr_280px]` (280px `h-fit` aside — flows with the page, not sticky). No undifferentiated card grids. |
| **Bespoke typography** — one display + one body, tight tracking | `Outfit` (display, `var(--font-outfit)`, `letter-spacing:-0.03em` on `h1–h4/.font-display`) + `DM Sans` (body, `var(--font-dm-sans)`) via `next/font/google` `variable+swap`. Never Inter/Roboto fallback without hierarchy. |
| **Deep forest + warm cream + amber accent** — 155-hue greens, not teal | Tokens in `src/app/globals.css:@theme` only (see §4). `bg-forest` (`hsl 155 42% 16%`) for header/hero, `bg-background` (`hsl 40 33% 99%`) warm cream, `accent amber 38 92% 50%` for CTA/highlight/star. |
| **Photo as proof** — 5 hero images are load-bearing | `public/images/{hero-prefab,green-home,interior-living,adu-backyard,tiny-home}.jpg` + `brand/og-image.jpg` behind `PageHero` forest overlay (`opacity-35` + `from-forest/80 via-forest/85 to-forest/90` + `radial-gradient(38 92% 50% / 0.16)`). `2026-09-11` incident when they were missing (hero rendered photo-less) is pinned by `assets.spec.ts`. |
| **Anti-generic mandate** — what is explicitly rejected | No purple-gradient-on-white, no Inter/Roboto safety pair without `font-display` hierarchy, no `tailwind.config.*` (v4 CSS-first only), no left-aligned gradient heroes (must be centered photo-backed `PageHero`), no amber header CTA (forest pill only), no undifferentiated card grids. |

**Non-negotiable rules:**

1. **File corpus is the source of truth** — edit `src/data/*.json` + `src/lib/lenders.ts`, never PG rows. DB is a projection (`ensureSeeded`).
2. **Single Pool** — `globalThis.__arenaNextJsPostgresqlPool` only. Never `new Pool()` inline.
3. **Token-driven styling** — `@theme` only. No `tailwind.config.*`, no `text-[13px]` arbitrary.
4. **RSC by default** — `"use client"` only for `site-header`, `prequal-form`, `calculator-app`. Never import Server → Client.
5. **Prefinancing accuracy** — `PMI_ANNUAL_RATE 0.0065` and site-built `1.15×` are auditable constants (see §15).

**CTA hierarchy:** Primary (forest) for actions, `secondary` for hero first CTA, `onPrimary` (transparent white border) for hero second CTA over dark forest, `accent` (amber) only for `GuideView` sidebar closing CTA. No other amber CTA in header.

**Does this prevent generic Bootstrap?** Yes — the `@theme` lock, `PageHero` centered photo contract, forest/cream token discipline, and `Container` rhythm make generic components visually fail before `build` does.

---

## 2. Tech Stack & Environment

Pinned from `package.json` (`package-lock.json` is the lockfile, not pnpm) + `docker-compose.yml` + `drizzle.config.*`. No ranges.

| Layer | Technology | Version | Critical Note |
|-------|------------|---------|---------------|
| Framework | Next.js (App Router, hybrid) | `^16.3.4` (16.3.x) | App Router only (`src/app/**`); `proxy.ts` replaces `middleware.ts` (not present — proxy concerns at reverse proxy). Pinned with `eslint-config-next ^16.3.4` `core-web-vitals`. `images.unoptimized:true` intentional (no `sharp` infra). |
| UI Runtime | React | `^19.3.0` | Server Components by default; `useId`, `useEffect` cleanup, `lucide-react` interop. No class components. |
| Language | TypeScript | `^5.9.3` | `strict:true`, `skipLibCheck:true`, `isolatedModules:true`, `moduleResolution: bundler`, `target: ES2017`, `jsx: react-jsx`, `incremental:true`. Alias `@/* → ./src/*`. Exclude `skills` (avoids `z-ai-web-dev-sdk` missing). `as any` banned. |
| Styling | Tailwind CSS (CSS-first `@theme`) | `^4.3.3` + `@tailwindcss/postcss ^4.3.3` + `postcss ^8.5.28` | **No `tailwind.config.*`** — all tokens in `src/app/globals.css:@theme` (sole source). `Container 1400px` rhythm. Never `text-[13px]` escape. |
| Icons | lucide-react | `^1.44.0` | All product icons (`Star`, `ArrowRight`, `ChevronDown`, `Menu/X`, `Home/Building2/Leaf/Shield` etc). `LinkedInIcon` local SVG (no brand set in lucide). |
| ORM | Drizzle ORM | `^0.45.2` | `pgTable` + `drizzle(pool)` + `onConflictDoNothing`. Chosen over Prisma for SQL control + `drizzle-kit generate` diff→SQL. |
| ORM Tooling | Drizzle Kit | `^0.31.10` | `drizzle.config.ts` primary (`satisfies Config`) + `.json` fallback — `out: ./drizzle`, `strict/verbose`, `url: …@5434` runtime wins. `drizzle/0000_amusing_thena.sql` + `0001_sharp_stick.sql`. |
| Driver | `pg` + `Pool` | `^8.23.0` + `@types/pg ^8.23.1` | Singleton via `globalThis.__arenaNextJsPostgresqlPool` — prevents HMR leak. `DATABASE_URL` throw if missing. |
| Database | PostgreSQL | `17-alpine` (host `5434`) | `home_financing_dev` / `home_financing_user` / `home_financing_secret` on `home_financing_data` volume + `home_financing_net` bridge. Extensions `pgcrypto 1.3` + `pg_trgm 1.6` via init. Health `pg_isready`. |
| Fonts | `next/font/google` | built-in | `Outfit` (`--font-outfit`) display + `DM Sans` (`--font-dm-sans`) body — `variable` + `display:swap`. |
| Env Loader | `dotenv` | `^17.4.2` | `import "dotenv/config"` in `src/scripts/*.ts` for lifecycle scripts. |
| Type Support | `@types/node`, `@types/react`, `@types/react-dom` | `^22.20.2`, `^19.3.0`, `^19.3.0` | Completes `tsc --noEmit`. |
| Scripting | `tsx` | `^4.23.13` | Runs `src/scripts/migrate|seed|reset` as ESM. |
| Lint | ESLint + `eslint-config-next` | `^9.39.5` + `^16.3.4` | Flat config `eslint.config.mjs` + `defineConfig` + `globalIgnores(.next,out,build,next-env,skills,infrastructure)`. |
| Unit | Vitest | `^4.1.11` (pass-8 audit bump — GHSA-82fw-gwwq-j7x9 fix; `vitest/config`, `node` env, `include: src/**/*.test.ts`) | Co-located `src/lib/*.test.ts` pure only (calculator 11 + matching 13 + rate-limit 9 + markdown 8 = 41). `41/41` green. |
| E2E | Playwright + `@axe-core/playwright` | `^1.63.0` + `^4.13.0` | Prod `npx next start --port 3002` (not `dev`), `reuseExistingServer:true`, `chromium+webkit`, `x-forwarded-for` isolation. `121 per project` — 103 declarations + data-driven loops (242 with webkit, `121/121` with DB, `120/121` DB-less; `playwright --list` shows 122 listed but 121 executed). `assets 19 runtime` + `parity 73 runtime` + `smoke 8` + `seo 16` + `funnel 5`. |
| Package Manager | npm | `package-lock.json` | Single app, no monorepo/turborepo. Gate: `db:setup → lint → typecheck → test → build → e2e`. |

---

## 3. Bootstrapping & Configuration

### 3.1 Scaffolding (what was, what to repeat)

This project was not `create-next-app` scaffolded in its current form — it evolved from `nextjs-postgresql-template`. To reproduce cleanly:

```bash
# If scaffolding a fresh sibling for comparison:
# npx create-next-app@16.3 home-financing-new --ts --eslint --tailwind --app --src-dir --import-alias "@/*"
# Then transplant: src/app/globals.css (@theme), src/db/*, src/lib/*, src/data/*.json, drizzle/*, next.config.ts redirects
```

For this repo, start from clone — scaffolding is already done. Don't run `create-next-app` here.

### 3.2 Dependency Install

```bash
npm install   # package-lock.json, not pnpm — single app, no workspace
```

Runtime: `next`, `react`, `react-dom`, `drizzle-orm`, `pg`, `lucide-react`, `dotenv` · Dev: `typescript`, `@types/*`, `eslint`, `eslint-config-next`, `tailwindcss`, `@tailwindcss/postcss`, `postcss`, `drizzle-kit`, `tsx`, `vitest`, `@playwright/test`, `@axe-core/playwright`.

### 3.3 Critical Configuration Files

| File | Lines | Purpose & Non-Obvious Rule |
|------|-------|----------------------------|
| `tsconfig.json` | ~35 | `strict:true`, `skipLibCheck:true`, `isolatedModules:true`, `target ES2017`, `jsx react-jsx`, `moduleResolution bundler`, `baseUrl:.`, `paths @/*→./src/*`, `plugins:[next]`, `include: ["**/*.ts","**/*.tsx","next-env.d.ts",".next/types/**"]`, `exclude:[node_modules,skills]`. `skills/**` excluded because operator-managed `z-ai-web-dev-sdk` would break `typecheck`. Never set `allowJs:true`. |
| `next.config.ts` | ~25 | `images.unoptimized:true` intentional (no `sharp`); `redirects()` 11 entries (`/loans/fha-va-usda-construction` → `/modular-home-financing/loan-options/*`, `/manufacturers*` → `/modular-home-financing/manufacturers*`, `/states/:state` → `/modular-home-financing/states/:state`, `/get-started-v2`→`/get-started` temp, `/playbook`→`/learn` temp, 2 compare parity permanents). Invalid redirect → `build` fails — guard via `assets.spec.ts`. |
| `eslint.config.mjs` | ~10 | `defineConfig([...nextCoreWebVitals, globalIgnores([".next/**","out/**","build/**","next-env.d.ts","skills/**","infrastructure/**"])])` — flat config (not `.eslintrc`), `skills/infrastructure` operator-managed, excluded from `lint`. Keep flat; never revert. |
| `vitest.config.ts` | ~15 | `defineConfig({ resolve:{ alias:{"@": fileURLToPath(new URL("./src", import.meta.url))}}, test:{ environment:"node", include:["src/**/*.test.ts"]}})` — alias mirrors `tsconfig`, `node` env (no DOM). |
| `playwright.config.ts` | ~40 | `testDir:"./e2e"`, `timeout 30000`, `expect 5000`, `fullyParallel:false`, `projects:[chromium(Desktop Chrome), webkit(Desktop Safari)]`, `webServer: process.env.E2E_BASE_URL ? undefined : { command:"npx next start --port ${PORT}", url:baseURL, reuseExistingServer:true, timeout:90000 }` — `E2E_PORT=3002` default (3000 is taken by sibling `scandihaven`), prod `next start` validates shipped artifact. |
| `drizzle.config.ts` | ~15 | Primary TS config `satisfies Config` — `schema:"./src/db/schema.ts"`, `out:"./drizzle"`, `dialect:postgresql`, `dbCredentials.url: process.env.DATABASE_URL ?? "…@5434/home_financing_dev"`, `strict:true, verbose:true` — runtime `DATABASE_URL` wins. |
| `drizzle.config.json` | ~12 | JSON fallback — same `out/schema/dialect/url/strict/verbose`; keep in sync after `db:generate` (both `5434`). |
| `postcss.config.mjs` | ~5 | `tailwindcss` via `@tailwindcss/postcss` — no custom plugins. |
| `docker-compose.yml` | ~45 | `postgres:17-alpine` `home_financing_postgres` on `host 5434 → 5432`, `home_financing_data` volume, `home_financing_net` bridge, `PGDATA /var/lib/postgresql/data/pgdata`, `restart unless-stopped`, health `pg_isready`, init `infrastructure/postgres/init/00-create-extensions.sql`. |
| `src/app/globals.css` | ~110 | `@import "tailwindcss"` + `@theme` (sole token source) + `@layer base` (focus/ selection) + `@layer utilities` (grain, hero-grid) + `prefers-reduced-motion`. |

### 3.4 Environment Variables

| Variable | Required | Description | Default / Generation |
|----------|----------|-------------|----------------------|
| `DATABASE_URL` | **Yes** | PG connection — `src/db/index.ts` **throws** if missing | `postgresql://home_financing_user:home_financing_secret@localhost:5434/home_financing_dev` |
| `BETTER_AUTH_SECRET` | **Yes** | Auth signing | `openssl rand -base64 32` (never commit; `d572d73` leak in history) |
| `BETTER_AUTH_URL` | **Yes** | Canonical public origin — `localhost` breaks prod `Invalid origin` | `http://localhost:3000` dev / `https://modfii.jesspete.shop` prod |
| `BETTER_AUTH_TRUSTED_ORIGINS` | No | Extra trusted origins | `https://admin.example` comma-separated |
| `NEXT_PUBLIC_SITE_URL` | **Yes** | `metadataBase` + OG + sitemap host | same as `BETTER_AUTH_URL` canonical |
| `CRON_SECRET` | **Yes** | Jobs runner | `openssl rand -hex 16` (`ec16d809a08c91d24dbfdab7e7be4a99` in current dev `.env`) |
| `STRIPE_SECRET_KEY` | No | Stripe test/live | `sk_test_set-me` |
| `STRIPE_WEBHOOK_SECRET` | No | Webhook signing | `whsec_set-me` |
| `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` | No | Stripe publishable | `pk_test_set-me` |
| `RESEND_API_KEY` | No | Email — unset → log transport | `re_…` |
| `EMAIL_FROM` | No | From header | `ModFii <orders@modfii.example>` |
| `AUTH_GOOGLE_ID` / `SECRET` | No | OAuth | — |
| `AUTH_APPLE_ID` / `SECRET` | No | OAuth | — |
| `FEATURE_*` | No | Flags `on/off` (also `true/false`, `1/0`); unknown `FEATURE_*` fails fast at boot (when wired) | `FEATURE_TRADE=off` etc |
| `DISABLE_IMAGE_OPTIMIZER` | No | `1` where `sharp` deadlocks (no `turbo.json` exists in this repo — wire it into CI env instead if Turborepo is ever added) | `1` |

> `.env` is `.gitignore`d (`ec11541` untracked it after `d572d73` leak). Never `git add -f .env`. `docs/bak.env` / `env.tgz` / `ssh-key.txt` also ignored — don't reintroduce.

### 3.5 Local Setup (Minimal → Full)

```bash
# 1 — Clone & install
git clone <repo-url> home-financing && cd home-financing
npm install

# 2 — Env (copy then fill required — DATABASE_URL already canonical for Docker)
cp .env.example .env
# Generate if you rotate:
#   openssl rand -base64 32   # BETTER_AUTH_SECRET
#   openssl rand -hex 16      # CRON_SECRET

# 3 — DB (Docker simplest; 5434 intentional — 3000 is taken by scandihaven on this host)
docker compose up -d
docker compose logs -f postgres   # expect pgcrypto: t / pg_trgm: t

# 3b — One-shot init (idempotent, local-guarded)
npm run db:setup   # → [db] migrations applied (0000+0001) + [db] seed complete (8/40/50/23/59/5)
# Granular: npm run db:generate / db:migrate / db:seed / db:reset

# 4 — Run
npm run dev                    # http://localhost:3000 (if free)
# or
npx next dev --port 3002       # http://localhost:3002 (E2E default)
npm run build && npm start     # prod preview

# 5 — Verify
curl -s http://localhost:3002/api/health | jq                    # { ok:true, status:ok, db:true }
curl -s http://localhost:3002/sitemap.xml | grep -o "<loc>" |wc -l  # 152
npm run lint && npm run typecheck && npm run test && npm run build && npm run e2e
```

Alternative PG17 (no Docker): `DATABASE_URL=postgresql://user:pass@localhost:5432/home_financing_dev npm run dev`.

---

## 4. The Design System (Code-First)

**Single source:** `src/app/globals.css` — never add `tailwind.config.*`. Every token traced to `@theme`.

### 4.1 The `@theme` Block (Verbatim Evidence)

```css
/* src/app/globals.css — verified against the 1,140-line Project_Architecture_Document.md; home-financing_SKILL.md is this file */
@import "tailwindcss";
@theme {
  --font-sans: var(--font-dm-sans), ui-sans-serif, system-ui, sans-serif;
  --font-display: var(--font-outfit), ui-sans-serif, system-ui, sans-serif;

  --color-background: hsl(40 33% 99%);        /* warm cream */
  --color-foreground: hsl(155 30% 12%);       /* forest text */
  --color-card: hsl(40 25% 97%);
  --color-card-foreground: hsl(155 30% 12%);
  --color-primary: hsl(155 45% 28%);          /* primary forest */
  --color-primary-foreground: hsl(40 33% 99%);
  --color-primary-600: hsl(155 50% 22%);      /* hover */
  --color-secondary: hsl(150 20% 92%);
  --color-secondary-foreground: hsl(155 30% 12%);
  --color-muted: hsl(150 15% 93%);
  --color-muted-foreground: hsl(155 10% 45%);
  --color-accent: hsl(38 92% 50%);            /* amber CTA */
  --color-accent-foreground: hsl(38 95% 12%);
  --color-destructive: hsl(0 72% 51%);
  --color-border: hsl(150 15% 88%);
  --color-input: hsl(150 15% 88%);
  --color-ring: hsl(155 45% 28%);
  --color-cream: hsl(40 40% 96%);             /* section wash */
  --color-forest: hsl(155 42% 16%);           /* deep forest — header/hero */
  --color-moss: hsl(150 22% 34%);             /* muted label */

  --radius-sm: 0.5rem; --radius-md: 0.625rem; --radius-lg: 0.75rem; --radius-xl: 0.75rem; --radius-2xl: 1rem;  /* pass-7 probe: rounded-md 10px / xl 12px / 2xl 16px (sm 8px) */
  --shadow-lift: 0 18px 40px -24px hsl(155 30% 12% / 0.35);
  --ease-brand: cubic-bezier(0.22,1,0.36,1);
}
@layer base { *{border-color:var(--color-border)} html{scroll-behavior:smooth}
  body{background:var(--color-background);color:var(--color-foreground);font-family:var(--font-sans);-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
  h1,h2,h3,h4,.font-display{font-family:var(--font-display);letter-spacing:-0.03em}
  :focus-visible{outline:2px solid var(--color-ring);outline-offset:3px}
  ::selection{background:hsl(38 92% 50% / 0.28);color:hsl(155 30% 12%)}
}
@layer utilities { .grain{position:relative}.grain::after{content:"";position:absolute;inset:0;opacity:.08;mix-blend-mode:multiply;background-image:url("data:image/svg+xml;utf8,<svg ...><feTurbulence baseFrequency='0.85' numOctaves='2'/></svg>")} .hero-grid{background-image:linear-gradient(40deg/0.04) 48px} }
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}*,*::before,*::after{animation-duration:.01ms!important;transition-duration:.01ms!important}}
```

If this block drifts, every `assets.spec.ts` + `PageHero` test conceptually fails — brand token authority is the lint.

### 4.2 Typography Hierarchy

| Role | Token | Source | Spec |
|------|-------|--------|------|
| Display / H1-H4 | `var(--font-outfit)` → `.font-display` | `next/font/google Outfit({ variable:"--font-outfit", display:"swap" })` in `layout.tsx` | `h1,h2,h3,h4` + `.font-display` → `Outfit`, `letter-spacing:-0.03em`, `font-bold` |
| Body / UI | `var(--font-dm-sans)` → `.font-sans` | `DM_Sans({ variable:"--font-dm-sans", display:"swap" })` | `body` default, nav, form, prose |
| Hero H1 | `font-display text-4xl md:text-6xl leading-[1.08]` | `page.tsx` | Tight leading, `highlight` amber span `text-accent` |
| Section H2 | `font-display text-2xl font-bold` | `page-shell.tsx GuideView` | `text-foreground` |

### 4.3 Border Radii & Shadows

| Token | Value | Where Used |
|-------|-------|------------|
| `sm` | `0.5rem` | `Badge` `rounded-full`, `Button` `rounded-md` |
| `md` | `0.625rem` | `rounded-md` = 10px (pass-7: `--radius: .75rem` → `calc(-2px)`) |
| `lg` | `0.75rem` | `--radius` base |
| `xl` | `0.75rem` | `PageHero` stat chips `rounded-xl` = 12px |
| `2xl` | `1rem` | `GuideView aside rounded-2xl` = 16px |
| `--shadow-lift` | `0 18px 40px -24px hsl(155 30% 12% / 0.35)` | Defined but currently unused — the header MORE dropdown hardcodes the equivalent arbitrary shadow `shadow-[0_18px_40px_-24px_hsl(155_30%_12%_/_0.35)]` |
| `--ease-brand` | `cubic-bezier(0.22,1,0.36,1)` | `<details>` accordion `::details-content` expansion (added 2026-09-11) and `Reveal`-adjacent motion |

### 4.4 Utilities

| Utility | Purpose | Where |
|---------|---------|-------|
| `.grain` | SVG turbulence overlay (`feTurbulence baseFrequency 0.85`, `opacity .08`, `multiply`) | Available for hero texture (not on every section) |
| `.hero-grid` | 48px grid (`linear-gradient 0.04` on both axes) | Available for decorative grid |

---

## 5. Component Architecture & Patterns

### 5.1 The 5-Layer Model + Golden Rule

```
Layer 0: File Corpus — Authoring. Rule: Edit src/data/*.json + src/lib/lenders.ts. Never hand-edit PG.
Layer 1: Catalog — Typing. Rule: src/lib/catalog.ts re-exports JSON as Manufacturer/StateGuide/Article/GlossaryTerm; UI imports only from @/lib/catalog and @/lib/guides.
Layer 2: Projection — Seeding. Rule: src/lib/ensure-seeded.ts is the only write path; __modfiiSeedPromise + count(lenders)>0 + onConflictDoNothing; called in /api/health + /api/applications.
Layer 3: Persistence — Storage. Rule: src/db/index.ts Pool singleton __arenaNextJsPostgresqlPool; never new Pool() inline; db is drizzle(pool).
Layer 4: Application — Rendering. Rule: Server Components by default; "use client" only for site-header, prequal-form, calculator-app; never Server→Client; force-dynamic only where DB touched.
Layer 5: Edge — Routing. Rule: Redirects live in next.config.ts:redirects(); add aliases there only; build validates, e2e/assets pins.
```

**Import boundary:** `src/components/ui.tsx` (`cn`, `Button/ButtonLink/Container/Badge`) may be imported anywhere. `src/lib/catalog.ts` may be imported in RSC or Route Handlers. `src/db/index.ts` may only be imported server-side. No leaf component imports `@/db` from a `"use client"` file — `build` would throw RSC boundary.

### 5.2 Directory Map (with Counts)

```
src/app/** (43 pages: 35 static + 8 dynamic — _not-found, robots, sitemap + 3 ƒ API routes [health,applications,calculator] + 5 ƒ pages [authors/[authorSlug], learn/[slug], manufacturers/[slug], states/[state], debug-error-probe] + 35 static content pages)
├── layout.tsx (fonts + metadataBase + SiteHeader/Footer)
├── globals.css (@theme sole source)
├── page.tsx (~500 lines, editorial homepage)
├── sitemap.ts / robots.ts / not-found.tsx
├── api/{health,applications,calculator}/route.ts (3× force-dynamic)
├── get-started/page.tsx + calculator/page.tsx
├── modular-home-financing/** (cost, rates, down-payment, with-land/without-land, loan-options/{fha,va,usda,construction-loan}, manufacturers, states, ...)
├── compare/{fha-vs-conventional-prefab, prefab-vs-site-built-costs, modular-vs-manufactured-financing}
├── construction-loans/{fha,va,usda} + learn/[slug] + authors/[authorSlug] + glossary + resources + financing/mortgage/adu-financing/tiny-home-financing

src/components/ (9 files, 5 client leaves + error boundary = 6 use-client)
├── ui.tsx (primitives — allowed everywhere)
├── site-header.tsx ("use client") ← fixed h-16 md:h-20 always-light frosted bar bg-background/80 backdrop-blur-lg border-border/50 (pass 3 removed transparent hero, pass-7 md:h-20 + md:flex gap-8), NAV 4 + MORE 2
├── site-footer.tsx (LinkedInIcon local SVG)
├── page-shell.tsx (Breadcrumbs + PageHero + GuideView — interior heroes must use this)
├── prequal-form.tsx ("use client") ← 13-field funnel
├── learn-explorer.tsx ("use client") ← learn hub search/filter/featured/tools/newsletter
├── reveal.tsx ("use client") ← home intro scroll-reveal
├── calculator-app.tsx ("use client")
└── guide-screen.tsx (renderer via guides.ts + markdown.tsx)

src/data/ (4 JSON → 152 sitemap locs after projection)
├── articles.json (553 lines, 23 articles)
├── manufacturers.json (912 lines, 40)
├── states.json (1069 lines, 50)
└── glossary.json (237 lines, 59)

src/db/ (2 files)
├── schema.ts (8 pgTables, ~130 lines)
└── index.ts (~20 lines, singleton)

src/lib/ (7 domains + 3 co-located *.test.ts)
├── catalog.ts (180 lines) ← typed JSON re-export
├── lenders.ts (120 lines) ← LENDER_SEEDS 8 + LOAN_PRODUCT_SEEDS 5
├── ensure-seeded.ts (80 lines) ← idempotent projection
├── calculator.ts (90 lines) ← PMI 0.65% + 1.15×
├── matching.ts (130 lines) ← scoring + validation
├── rate-limit.ts (25 lines) ← Map buckets
├── guides.ts + markdown.tsx
├── calculator.test.ts (11 tests)
├── matching.test.ts (13 tests)
├── rate-limit.test.ts (9 tests)
└── markdown.test.ts (8 tests)

src/scripts/ (3 lifecycle, all local-guarded)
├── local-db.ts (isLocalDatabaseUrl / assertLocalDatabase)
├── migrate.ts (drizzle-orm migrator, ./drizzle)
├── seed.ts (ensureSeeded wrapper)
└── reset.ts (DROP SCHEMA public,drizzle CASCADE + extensions)

drizzle/ (0000_amusing_thena.sql ~200 lines, 0001_sharp_stick.sql 1 line, meta/_journal.json idx 0,1)
e2e/ (121 per project — 103 declarations + data-driven loops — --list 122→121, `parity.spec.ts` pins H4/OOM + parity + pass-5/7 live-source pins + pass-4 source-exact hero/guide-hero pins)
├── smoke.spec.ts (8) — home/nav/footer, get-started, calculator, health, 404, axe critical, security headers
├── seo.spec.ts (16) — sitemap + robots + title/OG + 11 source title-pattern pins
├── funnel.spec.ts (5) — POST 400/200, x-forwarded-for isolation, burst 429, DB-outage 500
├── assets.spec.ts (19 runtime — 14 image × 200 + 3 broken-img + 2 alias)
└── parity.spec.ts (73 — H4/OOM regression + visual-parity pins + pass-3/4/5/7 live-source pins)
```

**Counts proven:** `grep -r "'use client'" src --include="*.tsx" | wc -l` → `6` islands (`site-header`, `prequal-form`, `calculator-app`, `learn-explorer`, `reveal`, `error.tsx`). `find src/components -name "*.tsx" | wc -l` → `9`. `find src -name "*.test.ts" | wc -l` → `4` (`calculator 11 + matching 13 + rate-limit 9 + markdown 8 = 41`). `npx playwright test --list --project=chromium` → `121` per project (`--list` shows 122 listed but 121 executed; 103 decl). `wc -l src/data/*` → `2771`.

### 5.3 Client vs. Server Component Decision Tree

```
Need useState / useEffect / onClick / browser API ?
├── Yes → "use client" leaf (site-header, prequal-form, calculator-app only). 
│         Never import a Server Component into it — extract shared UI to a leaf.
│         Example: site-header.tsx useId + useEffect(scroll passive) + useEffect(body overflow) + useState(prevPathname) pattern.
└── No  → Server Component (default). Direct db / ensureSeeded() / catalog reads allowed.
         Example: page.tsx, modular-home-financing/page.tsx, page-shell.tsx:PageHero, guide-screen.tsx, layout.tsx.

Need DB ? → Route Handler with export const dynamic = "force-dynamic" (applications, health, calculator).
           Never add export const revalidate to a seeded page without understanding — it would stale ensureSeeded().
```

### 5.4 CTA & Layout Primitives

| Primitive | Spec | Enforcement |
|-----------|------|-------------|
| `Button variant` | `primary/secondary/accent/outline/ghost/onPrimary`, `sm/md/lg` | `variants: Record<ButtonVariant,string>` in `ui.tsx` — no custom `style` prop |
| `Container` | `mx-auto w-full max-w-[1400px] px-4 md:px-8` | Header `h-16` uses it; `GuideView grid lg:grid-cols-[1fr_280px]` uses it |
| `PageHero` | Centered `max-w-4xl text-center`, `bg-forest` + photo overlay + star pill + highlight amber + CTA pair + glass chips | All `GuideScreen` pages flow through it; don't reintroduce left-aligned gradient heroes |
| `Breadcrumbs` | `/` separator, `light` maps to `text-primary-foreground/70`, `center` `justify-center` | Used inside `PageHero` with `light center` |

---

## 6. Custom Hooks Deep Dive

> **There is no `src/hooks/` folder in this repo.** That's intentional. Hooks live **inlined in the two `"use client"` components** that need them. This section documents those inlined patterns so you don't extract them prematurely or miss cleanup.

### 6.1 Header Scroll + Drawer (`src/components/site-header.tsx`)

```typescript
// src/components/site-header.tsx — Patterns: useId (a11y), adjust-during-render (no effect), passive scroll, body-lock cleanup

"use client";
import { useEffect, useId, useState } from "react";
import { usePathname } from "next/navigation";

export function SiteHeader() {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);
  const [moreOpen, setMoreOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const menuId = useId(); // a11y: aria-controls={menuId} on mobile button → div#menuId

  // 1) Transparent over dark hero only on "/" until scroll>12px (modfii.com parity)
  const overDarkHero = pathname === "/" && !scrolled;

  // 2) Close menus on client-side navigation WITHOUT setState-in-effect lint
  //    React's "adjust state during render" pattern — NOT useEffect(() => setOpen(false), [pathname])
  const [prevPathname, setPrevPathname] = useState(pathname);
  if (prevPathname !== pathname) {
    setPrevPathname(pathname);
    setOpen(false);
    setMoreOpen(false);
  }

  // 3) Passive scroll listener — never block main thread
  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 12);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true }); // passive:true — WHY: scrolling must stay 60fps
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  // 4) Body overflow lock — must cleanup or page stays locked after HMR/unmount
  useEffect(() => {
    document.body.style.overflow = open ? "hidden" : "";
    return () => { document.body.style.overflow = ""; };
  }, [open]);

  // ... header renders with fixed inset-x-0 top-0 z-50 backdrop-blur-lg
}
```

**Why each detail matters:**

- `passive:true` — prevents scroll blocking; Chrome will warn if omitted. Don't add `{ passive:false }` here.
- `adjust-during-render` (not `useEffect`) — `eslint-plugin-react-hooks/exhaustive-deps` + `setState-in-effect` would otherwise trigger cascading-renders lint (`101aec3` fixed this exact lint error via this pattern — see §12).
- `useId()` — stable `aria-controls` for mobile `id={menuId}`; don't use `Math.random()`.
- `body overflow` cleanup — returning `""` in cleanup prevents the drawer from leaving `overflow:hidden` after `open` toggles or component unmounts (test manually or via Playwright `moreOpen` click).

**SSR safety:** All `window` access is inside `useEffect` (never during render). Don't move `window.scrollY` to render scope — it would SSR-break.

### 6.2 Link vs. Button Navigation

`site-header.tsx` uses `<Link href={item.href}>` for nav and `ButtonLink` (which is `<Link>`) for `Get Started`. Don't use `<a href>` — it bypasses Next App Router client nav. Don't use `router.push` for static nav links.

### 6.3 When to Extract a Hook

Only extract when a third consumer appears. If you add a `useScrollY(threshold)` or `useBodyLock(open)` hook, it must preserve `passive:true` and the `""` cleanup contract. Until then, keep them inlined — premature abstraction hides the `12px` threshold.

---

## 7. Content Management & Data Ingestion

### 7.1 Where Content Lives (Source of Truth)

| File | Lines | Rows | Shape | Typed As | Seeded To |
|------|-------|------|-------|----------|-----------|
| `src/data/articles.json` | 553 | 23 | `{ slug, title, description, category, readTime, tag?, publishedAt, updatedAt?, authorName, authorRole, content (markdown), keywords, relatedSlugs }` | `Article` (`src/lib/catalog.ts`) | `articles` table (`slug varchar(160) unique`) |
| `src/data/manufacturers.json` | 912 | 40 | `{ slug, name, description, headquarters, founded (8→32), priceRange, homeTypes[], features[] }` | `Manufacturer` + computed `category: Affordable|Mid-Range|Premium` via `priceFloor(range)` | `manufacturers` table |
| `src/data/states.json` | 1069 | 50 | `{ slug, name, abbreviation, lendingClimate, lendingDescription, medianHomePrice, averageLoanAmount, prefabMarketGrowth, popularAreas[], topManufacturers[] }` | `StateGuide` | `states` table |
| `src/data/glossary.json` | 237 | 59 | `{ term, definition }` | `GlossaryTerm` (`letter` derived `term.charAt(0).toUpperCase()`) | `glossary_terms` table |
| `src/lib/lenders.ts` | 120 | 8 + 5 | `LENDER_SEEDS: { slug, name, description, specialties[], minCredit, greenMortgage, avgApprovalDays, rateDiscountBps, nmlsId }` + `LOAN_PRODUCT_SEEDS: { slug, name, downPayment, creditMin, summary, bestFor }` | `LenderSeed` | `lenders` + `loan_products` |

**Counts proven:** `python3 -c "len(json.load(open(...)))"` + `psql count(*)` after `db:seed` → `8/40/50/23/59/5` (see PAD §4.2). `articles.slug` is `varchar(160)` for long editorial slugs; `manufacturers.founded` migrated `8→32` in `0001_sharp_stick.sql`.

### 7.2 The Ingestion Pipeline (Projection, Not CMS)

```
src/data/*.json  ─┐
                  ├─► src/lib/catalog.ts (typed re-export, priceFloor/categorize, authors/AUTHOR_BIOS, authorSlug())
src/lib/lenders.ts┘         │
                            ▼
               src/lib/ensure-seeded.ts (global promise + count(lenders)>0 + onConflictDoNothing per slug/term)
                            │ idempotent, auto-runs in GET /api/health + POST /api/applications
                            ▼
               PostgreSQL 17 (drizzle pgTable, 8 tables, drizzle(pool) via __arenaNextJsPostgresqlPool)
                            │ onConflictDoNothing per unique slug/term
                            ▼
               src/app/** RSC + Route Handlers (read via catalog helpers: getManufacturer/getState/getArticle + drizzle(eq))
```

Why not `import.meta.glob`? Next.js App Router doesn't need Vite glob — `catalog.ts` is a typed `import ... from "@/data/*.json"` (with `tsconfig resolveJsonModule:true`) + computed `category`/`letter`. Glob would hide the `priceFloor`/`categorize` logic and break `sitemap.ts`'s `articles.map(article → /learn/${article.slug})` derivation.

### 7.3 How to Add Content (Procedure)

**Add a manufacturer:**

1. Edit `src/data/manufacturers.json` — append `{ slug, name, description, headquarters, founded, priceRange, homeTypes, features }` (slug `varchar(80)` unique, no `/`).
2. Run `npm run db:seed` (idempotent) — `manufacturers` `onConflictDoNothing({ target: slug })` will insert only the new row.
3. If manufacturing has been made more intricate, vary the articles and the glossary to directly mirror crafted / spelled.

**Add a state / article / glossary term:** Same — edit the JSON, `npm run db:seed`. Articles require `authorName/authorRole` → `catalog.ts` auto-derives `authors` + `authorSlug`; add to `AUTHOR_BIOS` if you want a custom bio (else generic).

**Add a lender:** Edit `src/lib/lenders.ts` `LENDER_SEEDS`, then `npm run db:seed`. `LENDER_SEEDS 8` becomes 9 — E2E still expects `lenders 8` in `psql count(*)` guard? No — `assets.spec.ts` doesn't pin lender count; only `psql count(*)` in PAD probes does. Update the probe expectation if you add.

**Add a loan product:** Same `lenders.ts:LOAN_PRODUCT_SEEDS`.

**Rename a slug:** You must add a redirect in `next.config.ts:redirects()` (see §3.3) and pin it in `e2e/assets.spec.ts` — `build` validates redirects but won't catch missing ones.

### 7.4 Locked Arrays & Regression Guards

| Array | Size | Guard | Why |
|-------|------|-------|-----|
| `ARTICLE.keywords` + `relatedSlugs` | 23 × variable | `articles.map(k => k.keywords ?? [])` in `catalog.ts` (default `[]`) | Sitemap `priority 0.6` per article must not 500 on missing `keywords` |
| `glossaryByLetter()` derived from `term.charAt(0)` | 59 → A–Z buckets | `glossaryTerms` table `letter varchar(1)` derived in `ensure-seeded.ts` | Letter filter UI must not show empty bucket |
| `NAV` 4 + `MORE` 2 in `site-header.tsx` | 8 total, `[...NAV,...MORE]` on mobile | `aria-label="Primary"` / `aria-label="Mobile"` | `smoke.spec.ts: heading[1] + nav[Primary] visible` |

---

## 8. Accessibility (WCAG AAA) Implementation

**Contrast table — all pairs AAA except muted secondary (AA large-text only):**

| Pair | Background | Foreground | Ratio | Level | Where |
|------|------------|------------|-------|-------|-------|
| Page | `background 40 33% 99%` | `foreground 155 30% 12%` | ~14.5:1 | **AAA** | `body` |
| Card | `card 40 25% 97%` | `card-foreground 155 30% 12%` | ~13.8:1 | **AAA** | `PageHero` glass chips `text-white` on `forest` still ≥7:1 because forest is dark |
| Primary | `primary 155 45% 28%` | `primary-foreground 40 33% 99%` | ~7.2:1 | **AAA** | `Button primary`, focus ring |
| Secondary | `secondary 150 20% 92%` | `secondary-foreground 155 30% 12%` | ~12:1 | **AAA** | `Button secondary` |
| Muted | `muted 150 15% 93%` | `muted-foreground 155 10% 45%` | ~4.6:1 | **AA large** only | Secondary prose — never body copy |
| Accent | `accent 38 92% 50%` | `accent-foreground 38 95% 12%` | ~10:1 | **AAA** | Amber CTA `text-accent-foreground` on `bg-accent` |
| Hero | `forest 155 42% 16%` | `white` / `white/85` | ~12:1 / ~9:1 | **AAA / AAA** | `PageHero` title + description |

**Focus ring (AAA):**

```css
/* src/app/globals.css @layer base — do not touch */
:focus-visible { outline: 2px solid var(--color-ring); outline-offset: 3px; }
```

`ring` is `primary 155 45% 28%` (dark forest), visible on `background` and `card` (both cream). Never override per-component.

**Skip-to-content:** Not yet implemented — add `<a href="#main" class="sr-only focus:not-sr-only">Skip to content</a>` at `layout.tsx` top and `main id="main"` when you touch the layout. Current e2e `axe-core` runs `include("main")` — it would still pass without the link but keyboard users need it.

**`prefers-reduced-motion`:**

```css
@media(prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  *,*::before,*::after{animation-duration:.01ms!important;transition-duration:.01ms!important}
}
```

Verified via `globals.css` — every `transition-colors duration-300` (header) collapses to `0.01ms` when user prefers reduced motion.

**Touch targets:** Mobile `site-header` button `h-10 w-10` (`40px`), `NAV` links `px-3 py-3` on mobile (`≥44px` height). Don't shrink.

**ARIA per component:**

| Component | Pattern | Proven |
|-----------|---------|--------|
| `SiteHeader` | `nav[aria-label="Primary"]` + `nav[aria-label="Mobile"]`, `button[aria-expanded][aria-controls=menuId]`, `aria-label` toggle `Open/Close menu` | `smoke.spec.ts: getByRole("navigation", {name:"Primary"})` |
| `PageHero` | `nav[aria-label="Breadcrumb"]` with `/` `aria-hidden` | `page-shell.tsx` — `aria-hidden` on separator |
| `GuideView` | `details > summary` FAQ with `[&::-webkit-details-marker]:hidden` + `ChevronDown` `aria-hidden` | No `aria-expanded` on summary (native `<details>` semantics) |
| Forms (`prequal-form`) | `onError` inline alert + `disabled` during async + `aria-label` on icon buttons | `validateApplication` strings surfaced inline |

**Axe proof:** `e2e/smoke.spec.ts: AxeBuilder(include:"main").analyze().filter(impact==="critical") → []` — critical violations blocked on `main`.

---

## 9. Anti-Patterns & Common Bugs

*Each entry: Symptom → Root cause → Fix → How to prevent recurrence (test/guard). Severity: `CRITICAL` (data loss/auth bypass) / `HIGH` (prod 404/500) / `MEDIUM` ( UX / contract) / `LOW` (tech debt).*

### #01 — Missing Hero Images (404, photo-less homepage) [HIGH]

- **Symptom:** `/` renders without photos; green band shows raw alt text. Six images `404`.
- **Root:** `public/images/{hero-prefab,green-home,interior-living,adu-backyard,tiny-home}.jpg` + `brand/og-image.jpg` were not committed; `src/app/page.tsx` + `page-shell.tsx:PageHero` referenced them.
- **Fix:** `c74dd7e` committed 6 images + `og-image.jpg`; adopted `modfii-logo-icon.svg` canonical.
- **Guard:** `e2e/assets.spec.ts` — 14 `request.get(src) → 200` (heroes/OG + 5 `public/brand/wordmarks/*.png` + 3 `public/images/avatars/*.jpg`) + `no broken <img> (naturalWidth===0)` on `/`, `/adu-financing`, `/tiny-home-financing`; `build` would not catch it (images are static).

### #02 — Source-Parity Compare Aliases 404 [HIGH]

- **Symptom:** `modfii.com` footer links `/compare/fha-vs-conventional` + `/compare/prefab-vs-site-built` 404'd; clone only shipped `-prefab` / `-costs` variants.
- **Root:** `next.config.ts:redirects()` missing 2 entries.
- **Fix:** Added `permanent:true` aliases: `fha-vs-conventional → fha-vs-conventional-prefab`, `prefab-vs-site-built → prefab-vs-site-built-costs`.
- **Guard:** `e2e/assets.spec.ts` `request.get(alias,{maxRedirects:5}) → 200`; `build` validates redirect syntax.

### #03 — Second `Pool` → HMR `EMFILE` / Auth Leak [CRITICAL]

- **Symptom:** `EMFILE: too many open files` in `dev` HMR; or two `Pool` configs diverge (one `5434`, one `5432` legacy).
- **Root:** `new Pool()` outside `src/db/index.ts`.
- **Fix:** Singleton via `globalThis.__arenaNextJsPostgresqlPool` in `src/db/index.ts`; `rg "new Pool"` must return single hit.
- **Guard:** Grep guard + `drizzle.config.*` both `5434`; `local-db.ts` refuses non-local.

### #04 — `setState` in Effect Lints `react-hooks/set-state-in-effect` [MEDIUM]

- **Symptom:** `npm run lint` failed `101aec3`-era: header menus were reset via `useEffect(() => setOpen(false), [pathname])` → cascading renders.
- **Root:** ESLint `core-web-vitals` flags it.
- **Fix:** `4d1e6ad` — adjust state **during render**: `if(prevPathname!==pathname){ setPrevPathname(pathname); setOpen(false); setMoreOpen(false); }` in `site-header.tsx`.
- **Guard:** `npm run lint` `0/0`; lint error would block PR.

### #05 — `.env` Committed with Real Secrets (`d572d73`) [CRITICAL]

- **Symptom:** `BETTER_AUTH_SECRET` + `CRON_SECRET` visible via `git show d572d73:.env`.
- **Root:** `.env` was tracked before `.gitignore` rule; `ec11541` later untracked it (`git rm --cached .env`).
- **Fix:** Rotate secrets on deploy; current dev `.env` has fresh `ec16d809a08c91d24dbfdab7e7be4a99` (`CRON_SECRET`).
- **Guard:** `.gitignore` now covers `.env`, `bak.env`, `env.tgz`, `ssh-key.txt`; `git log --all -p -- .env` would resurrect old value — run `filter-repo`/BFG to scrub if deploy used it as prod.

### #06 — Direct PG Hand-Edit Clobbered on Fresh Seed [MEDIUM]

- **Symptom:** Hand-edited `lenders` row via `psql UPDATE` vanished after `docker compose down -v && db:setup`.
- **Root:** DB is projection; file corpus is source of truth.
- **Fix:** Edit `src/data/*.json` + `src/lib/lenders.ts`, then `npm run db:seed`.
- **Guard:** Documented in `AGENTS.md` + `CLAUDE.md` + this SKILL `§5 Layer 0`; `ensureSeeded` overwrites on empty, not on populated (so non-empty is safe, but fresh volume resets).

### #07 — `tailwind.config.*` Drift (v3 vs v4 CSS-First) [MEDIUM]

- **Symptom:** Arbitrary `text-[13px]` + `tailwind.config.js` reintroduced tokens in two places.
- **Root:** Copy-paste from v3 templates.
- **Fix:** Delete `tailwind.config.*`; extend only `@theme` in `globals.css`.
- **Guard:** `ls tailwind.config*` must be empty; PR review rejects arbitrary values.

### #08 — `as any` / `@ts-ignore` Erases Strict Guards [MEDIUM]

- **Symptom:** `tsc` passes but runtime breaks on `ApplicationInput` shape.
- **Root:** `as any` to silence `parseBody` union.
- **Fix:** `unknown` + `asString(record.field)` + `typeof === "string"` narrowing; `as const` on `LOAN_PRODUCT_SEEDS`.
- **Guard:** `typecheck` + PR rule `as any → Never`; `grep -rn "as any" src` must be `0`.

### #09 — Server→Client Import Boundary Violation [HIGH]

- **Symptom:** `next build` throws `Cannot import Server Component into Client Component`.
- **Root:** `import { PageHero } from "@/components/page-shell"` from `"use client"` file (or `import { db } from "@/db"` in client).
- **Fix:** Extract shared UI to a leaf with no server import; keep `util: cn` etc. in `ui.tsx` which stays boundary-clean.
- **Guard:** `build` is the gate — it fails fast.

### #10 — In-Memory Rate Limiter Under-Limits on Multi-Instance [HIGH]

- **Symptom:** Burst not throttled after horizontal scale (each instance has its own `Map`).
- **Root:** `src/lib/rate-limit.ts` is in-memory by design for single deploy.
- **Fix:** Migrate to Redis/Upstash before scaling; document `ENV FEATURE_RATELIMIT=redis` when introduced.
- **Guard:** `funnel.spec.ts` uses `x-forwarded-for: burst-*` isolation; test would flip to 2-instance Redis test when scaling.

### #11 — Broken `<img>` Without `<Image>` Priority [LOW]

- **Symptom:** LCP image (`hero-prefab.jpg`) lazy-loaded, poor Web Vitals.
- **Root:** `<img>` tag instead of `next/image`.
- **Fix:** Use `next/image` even with `unoptimized:true` — still gives `priority`, `sizes`, `alt` enforcement.
- **Guard:** `assets.spec.ts` `naturalWidth===0` check on key pages.

### #12 — `N+1` Lender Lookup at Scale [LOW]

- **Symptom:** `POST /api/applications` fetches lender by `eq(slug)` in a loop (4× today). If match count grew, `N+1`.
- **Root:** Loop pattern fine at `4`, wasteful at `40`.
- **Fix:** Batch via `whereIn(lenders.slug, matchSlugs)` when fanout grows; current 4 is explicitly *acceptable* per `CLAUDE.md`.
- **Guard:** Code comment in §15 pattern notes the scaling point.

### #13 — `DISABLE_IMAGE_OPTIMIZER` Without `turbo.json` [LOW]

- **Symptom:** Sandbox doc claims `must stay in turbo.json:globalEnv` but `turbo.json` doesn't exist.
- **Root:** Monorepo `scandihaven` pattern copied into single-app doc.
- **Fix:** Either add `turbo.json` when Turborepo introduced or drop the claim.
- **Guard:** Verify at PAD update time.

### #14 — Manual `src/lib/catalog.ts` Drift (Stale `authorSlug` / `letter`) [MEDIUM]

- **Symptom:** New `articles.json` entry with `authorName: "Jane Doe"` creates `authorSlug: jane-doe` but `glossaryTerms.letter` still hardcoded `letter: "J"` vs derived `term.charAt(0)` mismatch.
- **Root:** `ensure-seeded.ts` derives `letter` but older manual DB edit wrote literal.
- **Fix:** Never hand-edit PG; trust `letter: item.term.charAt(0).toUpperCase()` in `ensure-seeded.ts`.
- **Guard:** `psql select distinct letter from glossary_terms` must equal `term[0] upper`.

---

## 10. Debugging Guide

*Symptom → Root → Fix. Every entry was encountered in this repo's history (see §12/§C).*

| Symptom | Root Cause | Fix |
|---------|------------|-----|
| `Error: DATABASE_URL is required` on boot | Missing `.env` or `DATABASE_URL` unset | `cp .env.example .env` + fill `postgresql://home_financing_user:secret@localhost:5434/home_financing_dev` |
| `ECONNREFUSED :5432` from `drizzle-kit` | Stale `drizzle.config.json` with old `5432` (pre-`scandihaven_*` legacy) | Both configs now `5434/home_financing_dev` — keep them in sync after `db:generate`; runtime `DATABASE_URL` still wins |
| `skills/ TS2307 z-ai-web-dev-sdk` | `skills/` excluded via `tsconfig` + `eslint` globalsIgnore, not installed | Don't install `z-ai-web-dev-sdk`; don't re-include `skills` (operator contract) |
| `ENOTFOUND home-financing.jesspete.shop` in E2E sitemap 30×200 | `sitemap.xml` uses `NEXT_PUBLIC_SITE_URL` prod host | `seo.spec.ts` host-rewrites `loc.origin → E2E_BASE_URL (127.0.0.1:3002)` before `request.get` — set `NEXT_PUBLIC_SITE_URL=https://modfii.jesspete.shop` on deploy |
| `429` persists across E2E tests | In-memory `Map` (`8/10min`) persists under `reuseExistingServer:true` | Use isolated `x-forwarded-for: test-*` per request; burst test uses dedicated `burst-*` IP (see `funnel.spec.ts: burst-${Date.now()}`) |
| `EADDRINUSE 3000` for E2E webServer | Sibling `scandihaven` on `:3000` | `E2E_PORT=3002` is the E2E default for this repo (`playwright.config.ts: PORT=3002`) |
| `react-hooks/set-state-in-effect` lint error | Header menus reset via `useEffect` on `pathname` | Fixed via adjust-during-render in `site-header.tsx` — don't revert |
| `Invalid origin` on auth | `BETTER_AUTH_URL` still `localhost` in prod | Set `BETTER_AUTH_URL` to canonical prod origin `https://modfii.jesspete.shop` + extras in `BETTER_AUTH_TRUSTED_ORIGINS` |
| `sharp` deadlock in sandbox | Image optimizer `sharp` native stress | Keep `images.unoptimized:true` + `DISABLE_IMAGE_OPTIMIZER=1` in constrained env; don't re-enable without infra |
| `.env` committed / `git show` leaks secret | `.env` was tracked before `.gitignore` | Untracked `ec11541`; **rotate `BETTER_AUTH_SECRET` + `CRON_SECRET`** — they remain in `d572d73` history |
| Sitemap/OG emit `home-financing.jesspete.shop` | `NEXT_PUBLIC_SITE_URL` stale host on deploy | Set `NEXT_PUBLIC_SITE_URL=https://modfii.jesspete.shop` in deploy env |
| `Refusing to run against non-local host` on `migrate/seed` | `DATABASE_URL` points at staging/prod | `assertLocalDatabase` guard — run migrations via CI's non-local path, not `npm run db:*` |
| `PageHero` shows no photo / raw alt | `public/images/*.jpg` missing (incident 2026-09-11) | `ls public/images/` → 5 + `brand/og-image.jpg`; `assets.spec.ts` pins `200` |
| `/compare/fha-vs-conventional` 404 | Parity alias missing | Add in `next.config.ts:redirects()` + pin in `assets.spec.ts` (permanent) |
| `npm run typecheck` fails on `skills/**` | `skills` not excluded | `tsconfig.json: exclude:[node_modules, skills]` + `eslint.config.mjs: globalIgnores(skills/**)` must stay |
| `axe critical` fails on `/` | `main` landmark missing or `focus-visible` overwritten | `axe-core: include("main").analyze().filter(critical) → []`; keep `globals.css:focus-visible` token |
| `seed` inserted 0 rows on fresh DB | `ensureSeeded` raced with empty `lenders` count cache | Not possible — `globalThis.__modfiiSeedPromise` single-flights; second caller awaits first |

**Triage flow (when unknown):**

```bash
docker compose logs -f postgres      # init extension notices + health
curl -s http://localhost:3002/api/health | jq  # readiness + ensureSeeded probe
npm run typecheck                     # fastest regression signal
npm run build 2>&1 | tail -n 100      # RSC boundary + redirect validation
sudo docker exec home_financing_postgres psql -U home_financing_user -d home_financing_dev -c "select count(*) from lenders;"
```

---

## 11. Pre-Ship Checklist

*Run in order — earlier gates catch cheaper failures. Every push must pass. Documented in `AGENTS.md`, `CLAUDE.md`, `README.md` gate table.*

```bash
# 1 — DB is the projection, not the authoring store. One-shot, idempotent, local-guarded.
npm run db:setup
# → [db] migrations applied (0000+0001) + [db] seed complete (8/40/50/23/59/5)
# Granular: npm run db:generate / db:migrate / db:seed / db:reset

# 2 — Lint (flat config, core-web-vitals, skills+infrastructure excluded)
npm run lint
# → 0 errors / 0 warnings
npm run lint:fix   # auto-fix when dirty

# 3 — Type (strict, skills excluded — z-ai-web-dev-sdk not installed)
npm run typecheck
# → 0 errors — no any, no ts-ignore

# 4 — Unit (pure domains only; DB paths stay under Playwright)
npm run test
# → 41/41 vitest (calculator 11 + matching 13 + rate-limit 9 + markdown 8 — incl. H4/OOM regression)
npm run test:watch      # watch
npm run test:coverage   # when wired

# 5 — Build (validates redirects, RSC boundaries, skills excluded)
npm run build
# → ✓ Compiled successfully in ~538ms
# → ✓ Generating static pages using 3 workers (43/43) in ~957ms
# → Routes: ○ 35 static + ƒ 8 dynamic

# 6 — E2E (prod next start on 3002, reuseExistingServer, chromium; valid-payload needs DB)
npm run e2e             # chromium 121/121 per project (103 declarations + data-driven loops — --list 122→121; 120/121 DB-less)
npm run e2e:all         # chromium + webkit

# 7 — Readiness + content surfaces
curl -s http://localhost:3002/api/health | jq
# → { "ok": true, "status": "ok", "db": true }

curl -s http://localhost:3002/sitemap.xml | grep -o "<loc>" | wc -l
# → 152  (39 STATIC + 23 learn + 50 states + 40 manufacturers)

# 8 — Manual asset/alias probe (what assets.spec.ts does automatically)
for p in /images/hero-prefab.jpg /images/green-home.jpg /images/interior-living.jpg /images/adu-backyard.jpg /images/tiny-home.jpg /brand/og-image.jpg; do echo "$p $(curl -s -o /dev/null -w "%{http_code}" http://localhost:3002$p)"; done
# → 6× 200
curl -I http://localhost:3002/compare/fha-vs-conventional       # 308 → /compare/fha-vs-conventional-prefab
curl -I http://localhost:3002/compare/prefab-vs-site-built      # 308 → /compare/prefab-vs-site-built-costs
```

**Additional gates (run mentally or via script):**

- [ ] Every new route has `loading.tsx`/`error.tsx` or an ADR explaining why not
- [ ] Rename of any `slug` has a `next.config.ts:redirects()` entry (permanent) + `assets.spec.ts` pin
- [ ] `NEXT_PUBLIC_SITE_URL` + `BETTER_AUTH_URL` on deploy = `https://modfii.jesspete.shop`
- [ ] `grep -rn "as any" src` → empty; `grep -rn "new Pool" src` → single hit in `src/db/index.ts`
- [ ] `ls tailwind.config*` → absent; `ls public/images/*.jpg` → 5 + `brand/og-image.jpg` present
- [ ] `BETTER_AUTH_SECRET`/`CRON_SECRET` not committed (`git log --all -p -- .env` should not show fresh values)
- [ ] Lighthouse/CWV + keyboard `focus-visible` + `aria-label` on icon buttons don't regress (axe `critical: []` on `main`)

---

## 12. Lessons Learnt & How to Avoid Them

*Each lesson traces to a specific code change or test. Numbered LL-01…*

**Sprint 1 — Bootstrap**

**LL-01. File-backed projection beats DB-as-source for editorial.**  
Content diffed in `src/data/*.json` survives `docker compose down -v` and PR review. `ensureSeeded()` idempotent via `globalThis.__modfiiSeedPromise` + `count>0` + `onConflictDoNothing`. Avoided: hand-editing PG rows that vanish on fresh volume. *Ref:* `src/lib/ensure-seeded.ts`, `AGENTS.md` never-do #2.

**LL-02. Pool singleton must be `globalThis` or HMR leaks `Pool`.**  
`globalThis.__arenaNextJsPostgresqlPool` prevents `EMFILE` on HMR. Never `new Pool()` inline — single import from `@/db` only. *Fix:* `src/db/index.ts` singleton + `rg` guard. *Test:* `build` would throw if second Pool leaked handles.

**LL-03. CSP/HSTS/DENY were not optional — auth later.**  
Initial probe showed `curl -v /api/health` emitting `content-security-policy`, `strict-transport-security`, `x-frame-options DENY`. Don't weaken them when adding Stripe/Cloudflare scripts — extend `connect-src` / `script-src` narrowly. *Ref:* `src/app/layout.tsx` inherits Next's defaults + proxy headers.

**LL-04. Keep `drizzle.config.ts` + `.json` in sync.**  
`drizzle-kit generate` writes via whichever config is resolved; mismatched `5434` vs `5432` once gave `ECONNREFUSED :5432`. Runtime `DATABASE_URL` still wins, but keep both `5434/home_financing_dev`. *Lesson:* diff both after `db:generate`.

**Sprint 2 — Security Remediation (2026-09-11 Incidents)**

**LL-05. `.env` with real secrets was tracked (`d572d73`).**  
`BETTER_AUTH_SECRET` + `CRON_SECRET` were committed before `.gitignore` added `.env`. `ec11541` untracked (`git rm --cached .env`). **Rotate** both — they remain in `git show d572d73:.env`. Don't `git add -f .env` ever. *Guard:* `grep "git show" .git/logs`.

**LL-06. `skills/**` must be excluded from `typecheck/lint/build`.**  
Operator-managed `skills/` vendored JS brought `TS2307 z-ai-web-dev-sdk` missing. `tsconfig exclude:[skills]` + `eslint globalIgnores(skills/**,infrastructure/**)` fixed it (`81ab837→ec11541`). Don't `pnpm install z-ai-web-dev-sdk` here — skills are not app dependencies.

**LL-07. DB lifecycle must refuse prod.**  
`src/scripts/local-db.ts` `assertLocalDatabase` (allow `localhost/127.0.0.1/::1` only) blocks `migrate/seed/reset` against shared hosts. Migrate via CI's non-local path when deploying. *Test:* `assertLocalDatabase("postgresql://user:pass@prod-db:5432/db")` throws.

**Sprint 3 — E2E Hardening**

**LL-08. Playwright on prod `next start`, not `dev`.**  
`scandihaven` audit found HMR hydration diverged from prod; `playwright.config.ts` runs `npx next start --port 3002` with `reuseExistingServer:true` to validate shipped artifact. `timeout 90s` for prod boot.

**LL-09. In-memory limiter needs `x-forwarded-for` isolation in tests.**  
`reuseExistingServer:true` persists the `Map` across specs. One `x-forwarded-for: local` would make all 27 tests share one bucket and `429` early. Fix: `test-*`, `burst-*` per-request IPs. Burst test fires `10×` on one IP expecting `400×8→429×2`. *Ref:* `e2e/funnel.spec.ts: burst-${Date.now()}`.

**LL-10. `E2E_PORT=3002` default because `3000` is taken.**  
Sibling `scandihaven` occupies `3000` on this dev host. `playwright.config.ts:PORT=3002` + `webServer 3002` avoids `EADDRINUSE`. `E2E_BASE_URL` overrides for CI.

**LL-11. Sitemap absolute `loc` must host-rewrite in tests.**  
`sitemap.xml` emits `NEXT_PUBLIC_SITE_URL` (`https://modfii.jesspete.shop` or older `home-financing.jesspete.shop` stale) which CI would `ENOTFOUND`. `seo.spec.ts` rewrites `loc.origin → E2E_BASE_URL (127.0.0.1:3002)` before `request.get`.

**Sprint 4 — UX Remediation**

**LL-12. Header is always light (pass 3 correction).**  
Live `modfii.com` renders a light frosted header (`rgba(253,253,252,0.8)` + blur) in every state — top, scrolled, desktop, mobile (computed-style probe 2026-09-12). The earlier `overDarkHero = pathname==="/" && !scrolled` transparent-over-dark treatment was removed in pass 3; don't reintroduce it. Interior `PageHero` is `bg-forest` with glass chips — don't reintroduce left-aligned gradient heroes.

**LL-13. `setState` in effect → lint `react-hooks/set-state-in-effect`.**  
Resetting `open/moreOpen` via `useEffect(() => setOpen(false), [pathname])` triggered cascading-renders lint. Fixed via adjust-during-render `if(prevPathname!==pathname){ setPrevPathname(pathname); setOpen(false); setMoreOpen(false); }`.

**LL-14. Brand mark is the circle glyph + two-tone wordmark (pass 3 correction).**  
The header/footer mark is the green circle ring + center dot rendered beside `Mod`(foreground)+`Fii`(primary) — verified against the live source header 2026-09-12. The rotated-square `modfii-logo-icon.svg` file that both sites ship is NOT what the source header renders; pass 3 replaced the file's contents with the circle glyph. Don't revert to a single-tone wordmark or the square mark.

**LL-15. `@theme` sole source — no `tailwind.config.*`.**  
v4 CSS-first — extending via `@theme` only (`—color-forest/accent/cream`), no `text-[13px]` arbitrary. `ls tailwind.config*` must stay empty.

**LL-16. `prequal-form.tsx` must surface `validateApplication` strings inline.**  
Error strings are stable (`Please enter your name.` etc) and rendered as inline alert + disabled submit during async. Never silent-fail.

**LL-17. A markdown parser that can break without consuming a line can kill the whole server (2026-09-11 origin 502).**  
`src/lib/markdown.tsx` had no branch for `#### ` (H4+) headings. Such a line fell through to the paragraph block, whose inner loop breaks on any line starting with `#` — *without consuming it*. The outer loop then re-examined the same line forever, allocating React elements until the Node heap (2 GB) died: one GET to `/learn/construction-loans-vs-traditional-mortgages-prefab` OOM-crashed `next-server` and Cloudflare served 502 for every route. Fix: explicit `#### ` branch + loop-safety guarantee (paragraph branch always consumes ≥1 line). Pinned by `src/lib/markdown.test.ts` (6 tests, incl. full-corpus render) and `e2e/parity.spec.ts` (both affected articles must render with a visible `<h4>`). Lesson: any hand-rolled parser loop must provably advance on every iteration; a content-only change (new `####` line in an article) is a plausible production kill-switch.

---

## 13. Pitfalls to Avoid

*Don't do this → Do this instead (with guard).*

| Pitfall | Don't | Do | Guard |
|---------|-------|----|-------|
| **Architecture** — Second `Pool` | `import { Pool } from "pg"; new Pool({…})` in any file | `import { db, pool } from "@/db"` only from `src/db/index.ts` | `rg "new Pool"` single hit |
| **Architecture** — DB hand-edit | `psql UPDATE lenders SET slug='x'` | Edit `src/lib/lenders.ts` / `src/data/*.json` → `npm run db:seed` | `AGENTS.md` never-do #2 + PAD `Layer 0` |
| **Architecture** — `force-dynamic` missing | Omit `export const dynamic` on DB handler | `export const dynamic = "force-dynamic"` on every `src/app/api/**/route.ts` | `rg "force-dynamic"` → 3 hits |
| **Architecture** — Middleware secrets | Put `DATABASE_URL` guard in `middleware.ts` | Keep at reverse proxy / `assertLocalDatabase` in lifecycle scripts | No `middleware.ts` / `proxy.ts` in repo |
| **TypeScript** — `as any` | `parseBody(json) as any` | `unknown` + `asString(record.field)` + `typeof==="string"` narrowing | `grep -rn "as any" src` → 0 |
| **TypeScript** — Default export | `export default function MatchLenders()` | `export function matchLenders()` (named) | `eslint` + named-import consistency |
| **Testing** — `vi.fn()` in factory | `vi.mock("@/db", () => ({ db: vi.fn() }))` | Hoist factory out: `const dbMock = vi.fn(); vi.mock("@/db", () => ({ db: dbMock }))` | Vitest hoisting docs |
| **Design** — `amber-400` literal | `bg-amber-400` | `bg-accent` (`hsl 38 92% 50%`) via `@theme` | Token lint + `AGENTS.md` `@theme` rule |
| **Design** — Reintroduced `tailwind.config.*` | Create `tailwind.config.ts` | Extend `globals.css:@theme` only | `ls tailwind.config*` absent |
| **Security** — Raw `process.env` | `process.env.DATABASE_URL ?? "hardcoded"` | `src/db/index.ts` throws if missing; `drizzle.config.*` fallback only `…@5434` matches `docker-compose.yml` | `db/index.ts` throw guard |
| **Security** — Trust extra `FEATURE_*` | Unknown `FEATURE_KLARNA=on` silently accepted | Fail fast on unknown `FEATURE_*` at boot (when flags are wired) | Documented in `ENV` table |
| **Perf** — Client import of server | `import { db } from "@/db"` in `"use client"` | Move DB read to RSC, pass as prop | `next build` boundary error |
| **Perf** — N+1 lender fetch | Loop `eq(slug)` for 40 matches without batch | Batch `whereIn(lenders.slug, slugs)` when fanout > 4 | Comment in `applications/route.ts` |

---

## 14. Best Practices

**Code organization**

- `src/app/**` route folders `kebab-case` (`modular-home-financing`, `construction-loans`). `src/data/*.json` `kebab-case.json`. Components grandfathered `kebab-case.tsx` — new files prefer `PascalCase.tsx` (don't mass-rename).
- Co-locate `Component.tsx` + `Component.test.tsx` when tests exist (e.g. `src/lib/calculator.test.ts` next to `calculator.ts`).
- Factory pattern for test data: `getMockX(overrides)` — not fixture copy-paste.
- Early returns over nesting; composition over inheritance; self-documenting names.

**TypeScript (`strict` matrix)**

- `allowJs:false`, `skipLibCheck:true`, `isolatedModules:true`, `strict:true` — enabled. Never `// @ts-ignore` / `@ts-expect-error`.
- `interface` for structural shapes (`Manufacturer`, `StateGuide`), `type` for unions/intersections.
- Lean on inference; explicit return type only when it adds safety.
- `import type` for type-only imports (`import type { PaymentInput }`).

**React / Next.js**

- Server Components by default; `"use client"` only for interactivity (header, forms, calculator).
- `useId()` for a11y ids (see §6); `useEffect` cleanup always returned (`body overflow` lock).
- `lucide-react` for icons; never inline SVG without wrapper (`LinkedInIcon` example).
- `next/font` `DM_Sans` + `Outfit` via `variable` + `display:swap` — never `<link>` Google Fonts.
- `next/image` even with `unoptimized:true` — gives `priority`, `sizes`, a11y.
- `export const metadata` / `generateMetadata()` per route; `metadataBase` from `NEXT_PUBLIC_SITE_URL`.

**Testing**

- TDD: Red → Green → Refactor → Commit (one cycle per commit). Bugs get failing regression test first.
- Co-located `*.test.ts` next to source; `vitest.config.ts: include: src/**/*.test.ts`, `environment: node`.
- Mock at `db/Pool` boundary; test real `matchLenders` scoring + `calculatePayment` math, not mocks of mocks.
- No CI is configured yet (no `.github/` directory) — the local pre-push gate is `npm run lint && npm run typecheck && npm run test && npm run build && npm run e2e`. Wiring CI to run the same gate on every PR is planned.

**Database**

- `drizzle-kit generate` → `drizzle/*.sql` → `drizzle-orm/migrator` `migrate(db, { migrationsFolder:"./drizzle" })` — never ad-hoc `push`.
- `drizzle.config.ts` (TS primary) + `.json` fallback share `url: …@5434` — keep in sync after schema edits.
- `pgcrypto` + `pg_trgm` via `infrastructure/postgres/init/00-create-extensions.sql` — init notice `pgcrypto: t`.
- When load grows, add `pgBouncer` or Drizzle `migrate` workflow, not raw `sql` tag unless unavoidable (only `count(*)::int` in `ensure-seeded.ts`).

**Security**

- `Zod` not yet adopted — keep manual validators (`validateApplication`, `parseBody`, `num()` clamp) consistent until migration.
- Every async handler has `onError` inline alert; every list has empty state; loading only when no data exists; disable buttons during async + spinner.
- Keep `CSP/HSTS/DENY` headers as-is (see §6.1 live evidence); extend narrowly for `stripe/cloudflareinsights`.

**Design**

- Brand tokens extend only inside `@theme` (see §4); no arbitrary values; `cn()` from `ui.tsx` for variant merging.
- Wrapping/styling `ui.tsx` primitives is allowed; re-implementing them is not.
- Header always light (`bg-background/90` + blur in every state, pass 3); CTA forest pill (never amber header).
- `PageHero` centered photo-backed + star pill + optional `highlight` amber line + CTA pair + glass stat chips — interior heroes must flow through it.

---

## 15. Coding Patterns

*Copy-paste ready — every pattern compiles in this project. Each has `Why this pattern` rationale.*

### Pattern 15.1 — API Route: `POST /api/applications` (Canonical Funnel)

```typescript
// src/app/api/applications/route.ts — Pattern: rateLimit → json → validate → seed → match → persist
// Why: Order prevents waste (throttle before parse), sanitizes before validating, warms DB only on valid payload.

import { db } from "@/db";
import { applicationMatches, applications, lenders } from "@/db/schema";
import { ensureSeeded } from "@/lib/ensure-seeded";
import { clientKey, rateLimit } from "@/lib/rate-limit";
import { matchLenders, validateApplication, type ApplicationInput } from "@/lib/matching";
import { eq } from "drizzle-orm";

export const dynamic = "force-dynamic";

function asString(v: unknown): string { return typeof v === "string" ? v : ""; }

function parseBody(v: unknown): ApplicationInput {
  const r = v && typeof v === "object" ? (v as Record<string, unknown>) : {};
  return {
    fullName: asString(r.fullName).trim().slice(0, 120),
    email: asString(r.email).trim().toLowerCase().slice(0, 254),
    phone: asString(r.phone).trim().slice(0, 32),
    zipCode: asString(r.zipCode).replace(/\D/g, "").slice(0, 5),
    propertyIntent: asString(r.propertyIntent).slice(0, 32),
    homeType: asString(r.homeType).slice(0, 32),
    landStatus: asString(r.landStatus).slice(0, 32),
    manufacturerKnown: typeof r.manufacturerKnown === "boolean" ? r.manufacturerKnown : null,
    manufacturerSlug: asString(r.manufacturerSlug).slice(0, 80) || undefined,
    creditRange: asString(r.creditRange).slice(0, 32),
    incomeRange: asString(r.incomeRange).slice(0, 32),
    budget: asString(r.budget).slice(0, 32),
    timeline: asString(r.timeline).slice(0, 32),
  };
}

export async function POST(request: Request) {
  if (!rateLimit(`app:${clientKey(request)}`, 8, 10 * 60 * 1000))
    return Response.json({ error: "Too many applications from this network. Try again shortly." }, { status: 429 });

  let json: unknown;
  try { json = await request.json(); } catch { return Response.json({ error: "Invalid JSON body." }, { status: 400 }); }

  const input = parseBody(json);
  const errors = validateApplication(input);
  if (errors.length > 0) return Response.json({ error: errors[0] }, { status: 400 });

  await ensureSeeded();                            // only after validation — no wasted seed on 400
  const matches = matchLenders(input);

  const [row] = await db.insert(applications).values({ ...input, status: "matched" }).returning({ id: applications.id });
  if (!row) return Response.json({ error: "Could not save application." }, { status: 500 });

  for (const m of matches) {
    const [lender] = await db.select({ id: lenders.id }).from(lenders).where(eq(lenders.slug, m.lender.slug)).limit(1);
    if (!lender) continue;                         // guard — if seed raced, skip rather than throw
    await db.insert(applicationMatches).values({
      applicationId: row.id, lenderId: lender.id,
      estimatedRate: m.estimatedRate.toFixed(3), estimatedPayment: m.estimatedPayment,
      matchScore: m.matchScore, rationale: m.rationale,
    });
  }
  return Response.json({ id: row.id, matches });
}
```

### Pattern 15.2 — Readiness Probe: `GET /api/health`

```typescript
// src/app/api/health/route.ts — Pattern: ping + idempotent ensureSeeded() + JSON health shape
// Why: Readiness probe must also warm an empty volume's projection without failing.

import { db } from "@/db";
import { ensureSeeded } from "@/lib/ensure-seeded";
import { sql } from "drizzle-orm";

export const dynamic = "force-dynamic";

export async function GET() {
  try {
    await db.execute(sql`select 1`);
    await ensureSeeded(); // Global promise — second concurrent health hit awaits, not races
    return Response.json({ ok: true, status: "ok", db: true });
  } catch {
    return Response.json({ ok: false, status: "error", db: false }, { status: 500 });
  }
}
```

### Pattern 15.3 — Idempotent Projection (`ensureSeeded`)

```typescript
// src/lib/ensure-seeded.ts — Pattern: Global single-flight + count guard + onConflictDoNothing
// Why: Concurrent /api/health + /api/applications on cold volume must not duplicate.

import { db } from "@/db";
import { articles, glossaryTerms, lenders, loanProducts, manufacturers as mfr, states as st } from "@/db/schema";
import { LENDER_SEEDS, LOAN_PRODUCT_SEEDS } from "@/lib/lenders";
import { articles as rows, glossary, manufacturers, states, authorSlug } from "@/lib/catalog";
import { sql } from "drizzle-orm";

const g = globalThis as typeof globalThis & { __modfiiSeedPromise?: Promise<void> };

async function seed() {
  const [{ count }] = await db.select({ count: sql<number>`count(*)::int` }).from(lenders);
  if (count > 0) return;
  await db.insert(lenders).values(LENDER_SEEDS).onConflictDoNothing({ target: lenders.slug });
  await db.insert(loanProducts).values([...LOAN_PRODUCT_SEEDS]).onConflictDoNothing({ target: loanProducts.slug });
  await db.insert(mfr).values(manufacturers.map(m => ({ slug:m.slug, name:m.name, description:m.description, headquarters:m.headquarters, founded:m.founded, priceRange:m.priceRange, category:m.category, homeTypes:m.homeTypes, features:m.features }))).onConflictDoNothing({ target: mfr.slug });
  await db.insert(st).values(states.map(s => ({ slug:s.slug, name:s.name, abbreviation:s.abbreviation, lendingClimate:s.lendingClimate, lendingDescription:s.lendingDescription, medianHomePrice:s.medianHomePrice, averageLoanAmount:s.averageLoanAmount, prefabMarketGrowth:s.prefabMarketGrowth, popularAreas:s.popularAreas, topManufacturers:s.topManufacturers }))).onConflictDoNothing({ target: st.slug });
  await db.insert(articles).values(rows.map(a => ({ slug:a.slug, title:a.title, description:a.description, category:a.category, readTime:a.readTime, tag:a.tag??null, publishedAt:a.publishedAt, updatedAt:a.updatedAt??null, authorName:a.authorName, authorRole:a.authorRole, authorSlug:authorSlug(a.authorName), content:a.content, keywords:a.keywords, relatedSlugs:a.relatedSlugs }))).onConflictDoNothing({ target: articles.slug });
  await db.insert(glossaryTerms).values(glossary.map(g => ({ term:g.term, definition:g.definition, letter:g.term.charAt(0).toUpperCase() }))).onConflictDoNothing({ target: glossaryTerms.term });
}

export function ensureSeeded(): Promise<void> {
  if (!g.__modfiiSeedPromise) g.__modfiiSeedPromise = seed().catch(e => { g.__modfiiSeedPromise = undefined; throw e; });
  return g.__modfiiSeedPromise;
}
```

### Pattern 15.4 — Domain Pure: `calculatePayment` + `matchLenders`

```typescript
// src/lib/calculator.ts — Pattern: Named constant + amortize (handles 0% + ≤0 principal) + PMI <20% + 1.15×
// Why: Auditable — changing 0.0065 or 1.15 requires product sign-off and test update.

const PMI_ANNUAL_RATE = 0.0065;
function amortize(principal: number, annualRate: number, termYears: number): number {
  if (principal <= 0) return 0;
  const m = annualRate / 100 / 12, n = termYears * 12;
  if (m === 0) return principal / n;
  const f = (1 + m) ** n;
  return (principal * m * f) / (f - 1);
}
export function calculatePayment(i: PaymentInput): PaymentBreakdown {
  const home = Math.max(0, i.homePrice), down = Math.min(Math.max(0, i.downPayment), home);
  const downPct = home === 0 ? 0 : down / home, loan = home - down;
  const monthlyPmi = downPct < 0.2 ? (loan * PMI_ANNUAL_RATE) / 12 : 0;
  const siteBuiltComparePrice = Math.round(home * 1.15);
  // ... tax/insurance/HOA + siteBuiltMonthly mirroring monthlyInsurance + monthlyHoa
  return { principal: home, monthlyPi: roundCents(amortize(loan, i.annualRate, i.termYears)), monthlyPmi: roundCents(monthlyPmi), siteBuiltComparePrice, siteBuiltMonthly: roundCents(siteBuiltMonthly), monthlySavingsVsSiteBuilt: roundCents(siteBuiltMonthly - monthlyTotal) } as PaymentBreakdown;
}

// src/lib/matching.ts — Pattern: CREDIT_FLOOR + BUDGET_MID lookup + +20/+18/+12 weights + 5.4% floor + cap 99
// Why: Deterministic — tests pin sort order and cap/floor.
```

### Pattern 15.5 — Env Module (Build-Context Fallback)

```typescript
// next.config.ts — drizzle.config.* url pattern: process.env.DATABASE_URL ?? "postgresql://home_financing_user:secret@localhost:5434/home_financing_dev"
// Why: Runtime env wins; fallback matches docker-compose.yml so drizzle-kit generate still writes to the right DB shape without .env in CI introspection.

// src/app/layout.tsx:metadataBase — new URL(process.env.NEXT_PUBLIC_SITE_URL ?? "http://localhost:3000")
// Why: localhost fallback for dev; prod must be https://modfii.jesspete.shop or OG/sitemap emit wrong host (see §10 stale-host).
```

### Pattern 15.6 — Sitemap Derivation from Catalog

```typescript
// src/app/sitemap.ts — Pattern: STATIC_PATHS 39 + catalog arrays → MetadataRoute.Sitemap
// Why: Sitemap is projection of the same file corpus that seeds PG — keeping it in sync is a one-line article push.

import { articles, manufacturers, states } from "@/lib/catalog";

const STATIC_PATHS = ["/","/get-started","/learn","/calculator","/modular-home-financing", /* ... 39 exact */ /* see file */];

export default function sitemap(): MetadataRoute.Sitemap {
  const base = process.env.NEXT_PUBLIC_SITE_URL ?? "http://localhost:3000";
  return [
    ...STATIC_PATHS.map(p => ({ url: `${base}${p}`, lastModified: new Date("2026-01-21"), changeFrequency: "weekly" as const, priority: p==="/" ? 1 : 0.7 })),
    ...articles.map(a => ({ url: `${base}/learn/${a.slug}`, lastModified: new Date(a.updatedAt ?? a.publishedAt), changeFrequency: "monthly" as const, priority: 0.6 })),
    ...states.map(s => ({ url: `${base}/modular-home-financing/states/${s.slug}`, lastModified: new Date("2026-01-15"), changeFrequency: "monthly" as const, priority: 0.55 })),
    ...manufacturers.map(m => ({ url: `${base}/modular-home-financing/manufacturers/${m.slug}`, lastModified: new Date("2026-01-15"), changeFrequency: "monthly" as const, priority: 0.55 })),
  ];
}
```

---

## 16. Coding Anti-Patterns

*Inverse of §15 — what fails if you do it.*

| Domain | ❌ Don't | ✅ Do |
|--------|----------|-------|
| **TS — loose `any`** | `const input = parseBody(json) as any` → `input.foo` unchecked | `unknown` → `asString(record.foo)` + `typeof==="string"` narrowing |
| **TS — default export** | `export default function validateApplication()` | `export function validateApplication()` (named) — tree-shaking + grep-ability |
| **React — `<a>` bypass** | `<a href="/get-started">Get Started</a>` | `import Link from "next/link"` or `ButtonLink href="/get-started"` — preserves App Router client nav |
| **React — server in client** | `import { db } from "@/db"` from `"use client"` file | Fetch in RSC, pass as prop; Route Handler does DB work |
| **Tailwind — literal amber** | `bg-amber-400` | `bg-accent` (`hsl 38 92% 50%`) token — single commit can shift brand |
| **Tailwind — `tailwind.config.*`** | Create `tailwind.config.ts` | Extend `@theme` in `globals.css` only — `ls tailwind.config*` must stay empty |
| **Tailwind — inline style** | `<div style={{ color:"#26694E" }}>` | `text-primary` token |
| **Pipeline — N+1 without batch** | Loop `eq(slug)` for 40 matches | `whereIn(lenders.slug, slugs)` when fanout > 4 (current 4 is explicitly ok) |
| **Pipeline — second pool** | `new Pool({ connectionString: process.env.DATABASE_URL })` in `lib/foo.ts` | `import { pool, db } from "@/db"` only from `src/db/index.ts` singleton |
| **Security — `x-forwarded-for` trust** | `request.headers.get("x-forwarded-for")!` (no trim/multi-entry) | `request.headers.get("x-forwarded-for")?.split(",")[0]?.trim() \|\| request.headers.get("x-real-ip") \|\| "local"` |
| **Test — `vi.fn` in factory** | `vi.mock("@/db", () => ({ db: vi.fn() }))` (hoisted, `vi` not available) | Hoist: `const dbMock = vi.fn(); vi.mock("@/db", () => ({ db: dbMock }))` |
| **Content — PG hand-edit** | `psql UPDATE articles SET slug='x'` | Edit `src/data/articles.json` → `npm run db:seed` |
| **Images — `<img>` for brand** | `<img src="/brand/modfii-logo-icon.svg">` | `next/image` with `priority` (even with `unoptimized:true`) |

---

## 17. Responsive Breakpoint Reference

*Tailwind v4 defaults — no custom `screens` config. Every section uses these, no bespoke `min-w` escapes.*

| Token | Width | Where Used |
|-------|-------|------------|
| `sm` | `640px` | `PageHero` stat chips `sm:grid-cols-2` → `lg:grid-cols-4` when `stats.length≥4` else `sm:grid-cols-3`; `
```

No canvas
```
?

**Canonical per-page rhythm:**

- `Container`: `px-4 md:px-8` (always), `max-w-[1400px]`
- `Hero` (`page.tsx`): `min-h-[92vh]` photo hero, `grid lg:grid-cols-[minmax(0,1.1fr)_minmax(320px,0.8fr)]` (content + glass stats), wordmark strip `flex flex-wrap items-center justify-center gap-x-12 gap-y-4` of `h-8 w-auto` logo PNGs (`public/brand/wordmarks/`); intro section scroll-reveals via `Reveal` (opacity 0 + `translateY(30px)`, cards `translateY(40px) scale(0.95)`, 300ms, staggered 75ms)
- `PageHero` (`page-shell.tsx`): `pt-32 md:pt-36 pb-16 md:pb-20` (accounts for fixed `h-16` header), centered `max-w-4xl`
- `GuideView`: `grid gap-12 lg:grid-cols-[minmax(0,1fr)_280px]` (article + `h-fit` aside)
- Related: `grid gap-4 md:grid-cols-2`
- Footer: `grid md:grid-cols-4`

**Mobile drawer (≤ `lg` = `1024px`):** `site-header` hides `nav` + CTA (`hidden lg:flex`) and shows burger `lg:hidden` (`h-10 w-10`). Menu `lg:hidden` renders `[...NAV,...MORE]` + `ButtonLink`. Don't add a custom `xl` breakpoint without a PAD amendment.

**Testing on mobile:** `playwright.config.ts` `devices["Desktop Chrome"]` (1280) + `Desktop Safari`; for mobile add `Pixel 5` / `iPhone 12` device in a manual run.

---

## 18. Z-Index Layer Map

*Flat scale — no wars. No `z-[9999]` anywhere. Radix not present; shadcn not wrapping portals (future).*

| Layer | `z-*` | Element | File | Purpose |
|-------|-------|---------|------|---------|
| Base content | `z-0` | Article text, `Container` | `page.tsx`, `page-shell.tsx` | — |
| Decorative | `z-10` (via `relative z-10`) | `PageHero` `Container` over photo + `from-forest` overlay | `page-shell.tsx` | Text above `absolute inset-0` forest/photo stack |
| Fixed header | `z-50` | `header.fixed inset-x-0 top-0 z-50 backdrop-blur-lg` | `site-header.tsx` | Above page content; `border-b` + `backdrop-blur-lg` |
| Header dropdown | `z-20` | `MORE` dropdown `absolute right-0 top-full z-20 mt-2` | `site-header.tsx` | Above `Container` but below fixed header edge |
| PageHero overlay | `absolute inset-0` (no `z`) | `from-forest/80 via-forest/85 to-forest/90` + `radial-gradient` | `page-shell.tsx` | Between photo `Image fill` and `Container z-10` |
| Toast / portal (future) | `z-50+` / `z-[60]` | `sonner` / `radix-dialog` portal when added | — (not yet) | Reserve `z-50` for portaled toast/dialog; header stays `z-50` → toast needs `z-[60]` or `radix` portal `z-[100]` |

**Conflict rules:**
- Never use `z-40` for header children — header is `z-50` fixed; `z-20` dropdown is sufficient.
- Portaled dialogs (when added) must be `z-[100]`+ via `createPortal` to escape `Container` stacking context.
- Don't add `z-10` to the page itself — only to elements that need to sit above an `absolute inset-0` decorative layer.

---

## 19. Color Reference (Complete)

*Verified against `src/app/globals.css:@theme` — single mismatch is a doc bug.*

| Token | Tailwind Class | Hex | HSL | RGB | Usage |
|-------|---------------|-----|-----|-----|-------|
| `--color-background` | `bg-background` | `#FFFBF5` | `40 33% 99%` | `255,251,245` | Page cream (not `cream` — `background` is the body) |
| `--color-foreground` | `text-foreground` | `#29251B` | `155 30% 12%` | `41,37,27` | Primary text |
| `--color-card` | `bg-card` | `#F9F6F0` | `40 25% 97%` | `249,246,240` | Card/FAQ surface (`details.group`) |
| `--color-card-foreground` | `text-card-foreground` | `#29251B` | `155 30% 12%` | `41,37,27` | Card text |
| `--color-primary` | `bg-primary text-primary-foreground` | `#276649` | `155 45% 28%` | `39,102,73` | Primary forest actions, focus ring |
| `--color-primary-600` | `bg-primary-600` | `#1D4D37` | `155 50% 22%` | `29,77,55` | Primary hover |
| `--color-primary-foreground` | `text-primary-foreground` | `#FFFBF5` | `40 33% 99%` | `255,251,245` | Text on primary |
| `--color-secondary` | `bg-secondary` | `#E6EEE6` | `150 20% 92%` | `230,238,230` | Secondary button |
| `--color-secondary-foreground` | `text-secondary-foreground` | `#29251B` | `155 30% 12%` | `41,37,27` | Text on secondary |
| `--color-muted` | `bg-muted` | `#EAEDE9` | `150 15% 93%` | `234,237,233` | Muted bg / hover |
| `--color-muted-foreground` | `text-muted-foreground` | `#6B7C74` | `155 10% 45%` | `107,124,116` | Secondary prose (AA large only) |
| `--color-accent` | `bg-accent text-accent-foreground` | `#F59E0B` | `38 92% 50%` | `245,158,11` | Amber CTA / highlight / star fill / selection wash |
| `--color-accent-foreground` | `text-accent-foreground` | `#3D2504` | `38 95% 12%` | `61,37,4` | Text on accent |
| `--color-destructive` | `bg-destructive` | `#DC2626` | `0 72% 51%` | `220,38,38` | Errors (reserved) |
| `--color-border` / `--color-input` | `border-border` / `bg-input` | `#DEE3DE` | `150 15% 88%` | `222,227,222` | Borders + inputs |
| `--color-ring` | `ring-ring` | `#276649` | `155 45% 28%` | `39,102,73` | `focus-visible: outline 2px ring` |
| `--color-cream` | `bg-cream` | `#F7F0E0` | `40 40% 96%` | `247,240,224` | Alt cream wash section |
| `--color-forest` | `bg-forest` | `#173329` | `155 42% 16%` | `23,51,41` | Deep forest — `PageHero` + hero CTA over dark |
| `--color-moss` | `text-moss` | `#426752` | `150 22% 34%` | `66,103,82` | Muted label (not yet widely used) |
| `--shadow-lift` | `shadow-lift` | — | `155 30% 12% / 0.35` | — | `0 18px 40px -24px` (defined; unused — dropdown hardcodes the same value) |
| `--ease-brand` | — | — | `cubic-bezier(0.22,1,0.36,1)` | — | Accordion `::details-content` easing (2026-09-11) |

**Opacity variants (common patterns):**

- `bg-white/10` + `border-white/15` + `backdrop-blur-sm` — glass chips on `bg-forest` (`PageHero` stats)
- `from-forest/80 via-forest/85 to-forest/90` — hero photo overlay stack
- `bg-accent/10` + `border-accent/20` — `GuideView aside`
- `bg-primary/10` — `Badge`
- `::selection bg 38 92% 50% / 0.28` — selection wash

**Forbidden colors (enforced by review, not yet by test):** Literal `amber-400`, `amber-500`, `purple-*` gradients, raw hex `style={{ color:"#…" }}` outside `@theme`, `tailwind.config.*` re-definitions.

**Singular exception:** `::selection` uses `hsl(38 92% 50% / 0.28)` (accent with `0.28` opacity) — the only place accent is used as a wash, not a button. Don't extend as a general pattern.

---

## 20. The Complete TypeScript Interface Reference

*Every interface below compiles against `src/**`. Copy-paste into the indicated file and `npm run typecheck` stays green.*

```typescript
// ──────────────────────────────────────────────────────────
// src/lib/catalog.ts — Source-of-truth typed re-exports
// ──────────────────────────────────────────────────────────

interface Manufacturer {
  slug: string;                          // varchar(80) unique — from manufacturers.json
  name: string;                          // varchar(160)
  description: string;                   // text (markdown-ish)
  metaDescription: string;               // computed via catalog helpers (SEO)
  headquarters: string;                  // varchar(160)
  founded: string;                       // varchar(32) — migrated 8→32 in 0001
  priceRange: string;                    // varchar(64) — e.g. "$149k–$320k"
  homeTypes: string[];                   // text[] — ["modular","prefab","adu"]
  features: string[];                    // text[]
  category: "Affordable" | "Mid-Range" | "Premium"; // derived priceFloor(range) ≥300 Premium, ≥150 Mid
}

interface StateGuide {
  slug: string;                          // varchar(40) unique
  name: string;                          // varchar(64)
  abbreviation: string;                  // varchar(2) unique
  lendingClimate: string;                // varchar(32)
  lendingDescription: string;            // text
  medianHomePrice: string;               // varchar(24)
  averageLoanAmount: string;             // varchar(24)
  prefabMarketGrowth: string;            // varchar(16)
  popularAreas: string[];                // text[]
  topManufacturers: string[];            // text[]
}

interface Article {
  slug: string;                          // varchar(160) unique — long editorial slugs
  title: string;                         // varchar(240)
  description: string;                   // text
  category: string;                      // varchar(40)
  readTime: string;                      // varchar(32) — "4 min read"
  tag?: string;                          // varchar(40) nullable
  publishedAt: string;                   // varchar(16) — ISO date slice
  updatedAt?: string;                    // varchar(16) nullable
  authorName: string;                    // varchar(120)
  authorRole: string;                    // varchar(120)
  keywords: string[];                    // text[] default {}
  relatedSlugs: string[];                // text[] default {} — another Article.slug
  content: string;                       // text markdown (rendered by markdown.tsx)
}

interface GlossaryTerm {
  term: string;                          // varchar(160) unique
  definition: string;                    // text
  // letter is derived term.charAt(0).toUpperCase() in ensure-seeded.ts → glossary_terms.letter varchar(1)
}

interface Author {
  slug: string;                          // authorSlug(name) — kebab from lower + [^a-z0-9] → "-"
  name: string;                          // "Sarah Mitchell"
  role: string;                          // "Housing Policy Analyst"
  bio: string;                           // from AUTHOR_BIOS map or generic fallback
}

// SITE — const object (not interface, but contract)
const SITE: {
  name: "ModFii"; tagline: "The #1 Prefab Home Mortgage Platform";
  description: string; // "Stop losing your dream prefab home…"
  email: "team@modfii.com"; hq: "Headquartered in Nashville, TN";
  nmls: "2537136"; linkedin: "https://www.linkedin.com/company/modfii"; twitter: "@ModFii";
};

// Helpers
function getManufacturer(slug: string): Manufacturer | undefined;
function getState(slug: string): StateGuide | undefined;
function getArticle(slug: string): Article | undefined;
function authorSlug(name: string): string; // lower + /[^a-z0-9]+/g → "-" + trim
function getAuthor(slug: string): Author | undefined;
function articlesByAuthor(slug: string): Article[];
function glossaryByLetter(): Array<{ letter: string; terms: GlossaryTerm[] }>;

// ──────────────────────────────────────────────────────────
// src/lib/lenders.ts — Canonical seeds (authoritative, 8 + 5)
// ──────────────────────────────────────────────────────────

interface LenderSeed {
  slug: string;                          // varchar(80) unique
  name: string;                          // varchar(160)
  description: string;                   // text
  specialties: string[];                 // text[] — e.g. ["modular","prefab","adu","green"]
  minCredit: number;                     // integer default 620
  greenMortgage: boolean;                // default false
  avgApprovalDays: number;               // integer default 10
  rateDiscountBps: number;               // integer default 0 — e.g. 45 → -0.45%
  nmlsId: string;                        // varchar(32)
}

declare const LENDER_SEEDS: LenderSeed[]; // 8 — greenline-modular, factory-first-mortgage, hearthstone-fha, valor-prefab-va, prairie-usda, summit-adu-capital, crossmod-conventional, tiny-foundation-lending

declare const LOAN_PRODUCT_SEEDS: ReadonlyArray<{
  slug: string;                          // varchar(80) unique — fha/va/usda/construction-to-permanent/conventional
  name: string;                          // varchar(160)
  downPayment: string;                   // varchar(40) — "3.5%", "0%", "3.5%–20%"
  creditMin: number;                     // integer
  summary: string;                       // text
  bestFor: string;                       // text
}>; // 5

// ──────────────────────────────────────────────────────────
// src/lib/calculator.ts — Payment math (auditable constants)
// ──────────────────────────────────────────────────────────

interface PaymentInput {
  homePrice: number;                     // 10_000..5_000_000 (num() clamp)
  downPayment: number;                   // 0..homePrice (min/max + Math.min(...homePrice))
  annualRate: number;                    // 0..25
  termYears: number;                     // 5..40
  annualTaxRate: number;                 // 0..5
  annualInsurance: number;               // 0..50_000
  hoaMonthly: number;                    // 0..5_000
}

interface PaymentBreakdown {
  principal: number;                     // === homePrice (Math.max(0, …))
  monthlyPi: number;                     // amortize(loan, rate, years) rounded
  monthlyTax: number;                    // (home * tax/100) /12
  monthlyInsurance: number;              // annual /12
  monthlyPmi: number;                    // loan * PMI_ANNUAL_RATE/12 iff downPct < 0.2 else 0
  monthlyHoa: number;                    // Math.max(0, hoa)
  monthlyTotal: number;                  // sum, rounded
  loanAmount: number;                    // home - down, rounded
  downPaymentPct: number;                // down/home (0..1)
  siteBuiltComparePrice: number;         // round(home * 1.15) — editorial 1.15×
  siteBuiltMonthly: number;              // amortize(siteBuiltLoan, …) + tax mirroring + PMI independent + insurance+HOA
  monthlySavingsVsSiteBuilt: number;     // siteBuiltMonthly - monthlyTotal
}

declare const PMI_ANNUAL_RATE: 0.0065;   // product-locked
declare const DEFAULT_CALCULATOR: PaymentInput; // homePrice 250_000, down 25_000, rate 6.5, term 30, tax 1.1, insurance 1_800, hoa 0
function calculatePayment(input: PaymentInput): PaymentBreakdown;
function amortize(principal: number, annualRate: number, termYears: number): number;
function roundCents(value: number): number; // Math.round(value)
function formatUsd(value: number): string;       // Intl.NumberFormat maximumFractionDigits:0
function formatUsdPrecise(value: number): string;// Intl ... minimumFractionDigits:2

// ──────────────────────────────────────────────────────────
// src/lib/matching.ts — Scoring + validation (user-facing strings stable)
// ──────────────────────────────────────────────────────────

interface ApplicationInput {
  fullName: string;                      // ≤120 trim
  email: string;                         // ≤254 lowercased
  phone: string;                         // ≤32 trim
  zipCode: string;                       // 5 digits only (replace(/\D/g).slice(0,5))
  propertyIntent: string;                // ≤32 — purchase/refinance
  homeType: string;                      // ≤32 — modular/prefab/adu/tiny/manufactured
  landStatus: string;                    // ≤32 — own_land / etc
  manufacturerKnown: boolean | null;
  manufacturerSlug?: string;             // ≤80
  creditRange: string;                   // ≤32 — excellent/good/fair/needs_work/not_sure
  incomeRange: string;                   // ≤32
  budget: string;                        // ≤32 — under_150k/150k_250k/250k_400k/400k_600k/600k_plus
  timeline: string;                      // ≤32
}

interface LenderMatch {
  lender: LenderSeed;
  estimatedRate: number;                 // Math.round(rate*1000)/1000, floor 5.4
  estimatedPayment: number;              // amortized, rounded
  matchScore: number;                    // Math.max(0, Math.min(99, score))
  rationale: string;                     // reasons.slice(0,2).join(". ") + "."
}

function matchLenders(input: ApplicationInput): LenderMatch[]; // scored 50 base +20/+18/+10/+8/+12, returns top 4
function validateApplication(input: ApplicationInput): string[]; // 11 checks: name≥2, EMAIL_RE, phone digits≥10, ZIP ^\d{5}$, propertyIntent/homeType/landStatus/creditRange/incomeRange/budget/timeline each required

// ──────────────────────────────────────────────────────────
// src/lib/rate-limit.ts — In-memory buckets (single-instance caveat)
// ──────────────────────────────────────────────────────────

interface Bucket { count: number; resetAt: number; } // Map<string, Bucket>
function rateLimit(key: string, limit: number, windowMs: number): boolean;
function clientKey(request: Request): string; // x-forwarded-for first entry trimmed → x-real-ip → "local"

// ──────────────────────────────────────────────────────────
// src/lib/guides.ts — GuidePageContent (consumed by page-shell.tsx:GuideView)
// ──────────────────────────────────────────────────────────

interface GuidePageContent {
  eyebrow?: string;                      // star pill
  title: string; highlight?: string;     // highlight is amber second line
  description: string;
  heroImage?: string;                    // one of public/images/*.jpg
  stats?: Array<{ label: string; value: string }>; // glass chips
  cta: string;                           // Button label → /get-started
  sections: Array<{ heading: string; body: string[]; bullets?: string[] }>;
  faqs?: Array<{ question: string; answer: string }>; // native <details>
  related?: Array<{ title: string; description: string; href: string }>;
}

// ──────────────────────────────────────────────────────────
// src/db/schema.ts — Drizzle tables (mirrors §4.1) — pgTable definitions
// ──────────────────────────────────────────────────────────

declare const lenders: import("drizzle-orm/pg-core").PgTableWithColumns<any>;
declare const applications: PgTableWithColumns<any>;
declare const applicationMatches: PgTableWithColumns<any>;
declare const manufacturers: PgTableWithColumns<any>;
declare const states: PgTableWithColumns<any>;
declare const articles: PgTableWithColumns<any>;
declare const glossaryTerms: PgTableWithColumns<any>;
declare const loanProducts: PgTableWithColumns<any>;

// ──────────────────────────────────────────────────────────
// Environment (validated in §3.4 / PAD §9.2)
// ──────────────────────────────────────────────────────────

interface Env {
  DATABASE_URL: string;                  // Yes — throws if missing
  BETTER_AUTH_SECRET: string;            // Yes — openssl rand -base64 32
  BETTER_AUTH_URL: string;               // Yes — canonical prod origin
  BETTER_AUTH_TRUSTED_ORIGINS?: string;  // comma-separated
  NEXT_PUBLIC_SITE_URL: string;          // Yes — metadataBase + sitemap host
  CRON_SECRET: string;                   // Yes — openssl rand -hex 16
  STRIPE_SECRET_KEY?: string;            // sk_test_…
  STRIPE_WEBHOOK_SECRET?: string;        // whsec_…
  NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY?: string; // pk_test_…
  RESEND_API_KEY?: string;               // log transport when unset
  EMAIL_FROM?: string;                   // ModFii <orders@…>
  AUTH_GOOGLE_ID?: string; AUTH_GOOGLE_SECRET?: string;
  AUTH_APPLE_ID?: string; AUTH_APPLE_SECRET?: string;
  FEATURE_TRADE?: string;                // on/off true/false 1/0
  DISABLE_IMAGE_OPTIMIZER?: string;      // "1" in sandboxes
}
```

---

## Appendix A: Architecture Decision Records

*Definitive table — every ADR traces to a file or test. See PAD §1.3 for full Context/Decision/Rationale/Consequences/Rejected body; this appendix is the quick table.*

| ADR | Decision | Key File(s) | Rationale One-Liner | Rejected |
|-----|----------|-------------|---------------------|----------|
| ADR-001 | Next 16.3 App Router + React 19 RSC | `src/app/layout.tsx`, `src/app/**`, `src/components/site-header.tsx` | RSC streaming + `metadataBase` + `sitemap.ts`/`robots.ts` + per-route `force-dynamic` — Pages cannot express this hybrid | `pages/` + `getServerSideProps` / Vite SPA |
| ADR-002 | File-backed projection (`src/data/*.json` + `LENDER_SEEDS` → `ensureSeeded` → PG) | `src/data/*.json`, `src/lib/catalog.ts`, `src/lib/ensure-seeded.ts`, `src/lib/lenders.ts` | Git-reviewable, survives `down -v`, deterministic `db:setup` | CMS-first / PG hand-edit |
| ADR-003 | Drizzle ORM `0.45.2` + `pg` Pool singleton `globalThis` | `src/db/schema.ts`, `src/db/index.ts`, `drizzle.config.*` (`5434`) | Single Pool prevents HMR `EMFILE`; `drizzle-kit generate` diff→SQL | Prisma / inline `new Pool()` |
| ADR-004 | Tailwind v4 CSS-first `@theme` (sole source) | `src/app/globals.css`, `src/components/ui.tsx` | Token authority without config drift; `build` proves parity | `tailwind.config.*` (v3) / arbitrary escapes |
| ADR-005 | In-memory `Map` limiter `8/10min` via `x-forwarded-for` | `src/lib/rate-limit.ts`, `src/app/api/applications/route.ts` | Single-instance zero-infra; probed `400×8→429×2` | Redis from day-0 / no limiter |
| ADR-006 | Vitest `41` (11+13+9+8) + Playwright prod `121` per project (pure vs DB boundary) | `vitest.config.ts`, `playwright.config.ts` (`3002`, `reuseExistingServer`), `e2e/*` (`smoke 8 + seo 16 + funnel 5 + assets 19 + parity 73; 103 decl; 122 listed→121 executed`) | Dev HMR ≠ prod; `assets` guards 14 images + alias incidents + `parity` guards H4/OOM + wordmarks/avatars/learn-hub/calculator/footer/wizard + pass-5/7 live-source pins | Unit-only / E2E on `dev` |
| ADR-007 | `images.unoptimized:true` (no `sharp`) | `next.config.ts`, `postcss.config.mjs` | No optimizer in deploy/sandbox would deadlock | Optimizer-on by default |

---

## Appendix B: Pipeline Costs

*No billing / credit / AI pipeline exists in this repo. This appendix documents that absence to prevent the `scandihaven` assumption from being copied.*

| Concern | Status | Cost | Note |
|---------|--------|------|------|
| Credits / billing | Not implemented | `0` | `STRIPE_*` env is test-mode stub; no checkout route; `RESEND_API_KEY` unset → log transport |
| AI media pipeline (OpenAI/Replicate/ElevenLabs) | Not implemented | `0` | Single-app marketing + funnel; no `videoPrice`/`promptSnapshots` table |
| Jobs queue (BullMQ/Inngest) | Not implemented | `0` | `CRON_SECRET` reserved; `ensureSeeded` runs inline |
| Content ingest (RSS/BullMQ) | Not implemented | `0` | Static JSON projection, not RSS feed |
| Storage (R2/S3) | Not implemented | `0` | `public/images` static assets only |
| **When adding any pipeline** | Document here | — | Add row: operation, credits, time, retry/concurrency, idempotency guard |

Do not copy `scandihaven` pipeline cost assumptions into this repo — this is a marketing + funnel app, not a media pipeline.

---

## Appendix C: Audit History

| Date | Audit / Trigger | Findings | Fixes | Test Progression |
|------|----------------|----------|-------|-------------------|
| 2026-09-11 (pre-`ec11541`) | Secret leak `d572d73` — `.env` committed with real `BETTER_AUTH_SECRET`/`CRON_SECRET` | `git show d572d73:.env` leaks `8KxGM…` + `ec16d8…` | Untracked `ec11541` (`git rm --cached .env`), `.gitignore` added `.env/bak.env/env.tgz/ssh-key.txt`, **rotate both secrets** on deploy | `git log --all -p -- .env` now shows stale value — `filter-repo`/BFG needed to scrub if prod-valid |
| 2026-09-11 (R-01) | `TS2307 z-ai-web-dev-sdk` breaks `typecheck/build` | `skills/` imported via `tsconfig include: **/*.ts` picked vendored JS | `tsconfig exclude:[skills]` + `eslint globalIgnores(skills/**,infrastructure/**)` — lint `0/0`, `typecheck` pass, `build` no longer traverses `skills/` | `npm run typecheck` green |
| 2026-09-11 (asset incident) | 6 images `404` (`hero-prefab` etc) + `og-image.jpg` missing → hero photo-less | `public/images/*.jpg` not committed | `c74dd7e` committed 5 + `og-image.jpg` + `modfii-logo-icon.svg` canonical | `e2e/assets.spec.ts` pins 6×`200` + `no broken <img>` |
| 2026-09-11 (alias incident) | `modfii.com` footer `fha-vs-conventional` + `prefab-vs-site-built` 404 | `next.config.ts:redirects()` missing 2 parity aliases | Added `permanent:true` aliases to `-prefab` / `-costs` | `assets.spec.ts` pins `request.get(alias,{maxRedirects:5})→200`, `build` validates redirect syntax |
| 2026-09-11 (lint R-02) | `react-hooks/set-state-in-effect` on header | `useEffect(() => setOpen(false), [pathname])` cascading renders | `4d1e6ad` adjust-during-render `if(prevPathname!==pathname){…}` in `site-header.tsx` | `lint 0/0` |
| 2026-09-11 (DB init) | Fresh volume `home_financing_data` empty | `count(lenders)=0` → funnel `500` | `npm run db:setup` (`migrate 0000+0001` + `seed` `8/40/50/23/59/5`) + `GET /api/health` `ok:true,db:true` — all idempotent | `e2e` `27/27` with DB (was `26/27` DB-less) |
| 2026-09-11 (deploy) | `home-financing.jesspete.shop` stale host in `sitemap.xml`/OG | `NEXT_PUBLIC_SITE_URL` pointed at old host from `.env` history | `.env` + `.env.example` moved to `home_financing_*` + `https://modfii.jesspete.shop` canonical; `seo.spec.ts` host-rewrites `loc.origin→E2E_BASE_URL` | `sitemap 152` locs absolute, `robots` `Sitemap:` pins canonical |
| 2026-09-11 (OOM incident) | One GET to `/learn/construction-loans-vs-traditional-mortgages-prefab` OOM-crashed `next-server` (2 GB heap); origin 502 for all routes | `markdown.tsx` had no `#### ` branch; paragraph loop broke on `#`-lines without consuming → infinite allocation | Explicit H4 branch + always-consume-≥1-line guard in `markdown.tsx` | `markdown.test.ts` 6 tests (incl. full-corpus) + `e2e/parity.spec.ts` render both H4 articles |
| 2026-09-11 (parity pass 2) | Clone diverged from modfii.com: text wordmarks, no testimonial avatars, no scroll reveals, static accordions, 1 social icon, thin `/learn` + `/calculator` | First-pass parity covered layout only | 5 wordmark PNGs + 3 avatars added; `Reveal` component + `::details-content` accordion animation; footer socials (4) + Legal column; `/learn` rebuilt (search/filters/featured/icons/tools/newsletter); `/calculator` rebuilt (breakdown bar/loan summary/PMI alert/how-to/explore/FAQ/related/CTA); get-started wizard parity; manufacturers tier bands + A–Z directory | `e2e/parity.spec.ts` 10 tests; `assets.spec.ts` 14 image pins; visual re-capture vs source |

Cache-pollution `8aacd13` (17 `__pycache__/.mypy_cache/.venv` committed) also covered — `.gitignore` now ignores `**/.venv/__pycache__/.mypy_cache/.ruff_cache`.

---

## Appendix D: Live-Site Validation & Quick Reference Card

### D.1 Live Probes (from §11 of PAD + DB init run, 2026-09-11, prod `3002`)

```bash
# Readiness (idempotent ensureSeeded)
curl -s http://localhost:3002/api/health | jq
# → { ok:true, status:ok, db:true }

# Funnel valid → 4 matches
TS=$(date +%s)
curl -s -X POST http://localhost:3002/api/applications \
  -H 'Content-Type: application/json' -H "x-forwarded-for: live-$TS" \
  -d "{\"fullName\":\"Alex Rivera\",\"email\":\"live+$TS@example.com\",\"phone\":\"5551234567\",\"zipCode\":\"90210\",\"propertyIntent\":\"purchase\",\"homeType\":\"modular\",\"landStatus\":\"own_land\",\"manufacturerKnown\":false,\"creditRange\":\"good\",\"incomeRange\":\"100k_150k\",\"budget\":\"250k_400k\",\"timeline\":\"3_6_months\"}" | jq '.matches | length'
# → 4  (estimatedRate 6.0, matchScore 99)

# Invalid → 400
curl -s -X POST http://localhost:3002/api/applications -H "x-forwarded-for: bad-$TS" -d '{"fullName":"","email":"bad"}' | jq
# → { error:"Please enter your name." }

# Burst same IP → 400×8 then 429×2  (8/10min proves limiter wired)
BIP="burst-live-$$"; for i in 1..10; do curl -s -o /dev/null -w "%{http_code} " -H "x-forwarded-for: $BIP" -X POST http://localhost:3002/api/applications -d '{"fullName":"","email":"bad"}'; done; echo
# → 400 400 400 400 400 400 400 400 429 429

# Sitemap + robots + images + aliases
curl -s http://localhost:3002/sitemap.xml | grep -o "<loc>" | wc -l   # 152
curl -s http://localhost:3002/robots.txt | grep -i sitemap           # Sitemap: https://modfii.jesspete.shop/sitemap.xml
for p in /images/hero-prefab.jpg /images/green-home.jpg /images/interior-living.jpg /images/adu-backyard.jpg /images/tiny-home.jpg /brand/og-image.jpg; do curl -s -o /dev/null -w "$p %{http_code}\n" http://localhost:3002$p; done  # 6× 200
curl -I http://localhost:3002/compare/fha-vs-conventional   # 308 → /compare/fha-vs-conventional-prefab
curl -I http://localhost:3002/compare/prefab-vs-site-built  # 308 → /compare/prefab-vs-site-built-costs

# DB row counts
sudo docker exec home_financing_postgres psql -U home_financing_user -d home_financing_dev -c "
  select 'lenders', count(*) from lenders
  union all select 'manufacturers', count(*) from manufacturers
  union all select 'states', count(*) from states
  union all select 'articles', count(*) from articles
  union all select 'glossary_terms', count(*) from glossary_terms
  union all select 'loan_products', count(*) from loan_products;"
# → 8 / 40 / 50 / 23 / 59 / 5
```

What live-site catches that CI cannot: `modfii.com` parity aliases (308), host-rewritten sitemap `200` per `loc`, `axcritical: []` on `main`, photo-less hero `naturalWidth===0`.

### D.2 Quick Reference Card

| Concern | File | Key Line / Count | Guard |
|---------|------|------------------|-------|
| Brand | `src/lib/catalog.ts:SITE` | `ModFii, #1 Prefab, Nashville NMLS 2537136` | `layout.tsx:metadataBase` |
| Hero | `src/app/page.tsx` | `HERO_CHECKS 3` + `PARTNER_WORDMARKS 5` + `INTRO_CARDS 4` + `PROBLEMS 3` + `FIXES 3` + `STEPS 3` | `smoke.spec.ts: heading[1] visible` |
| Header CTA | `src/components/site-header.tsx` | `ButtonLink /get-started variant=primary` forest pill (header always light — pass 3) | Review: never amber |
| Pool | `src/db/index.ts` | `globalThis.__arenaNextJsPostgresqlPool` single | `rg "new Pool"` 1 hit |
| PMI | `src/lib/calculator.ts` | `PMI_ANNUAL_RATE 0.0065`, site-built `1.15×` | `calculator.test.ts` 11 tests |
| Scoring | `src/lib/matching.ts` | `+20/+18/+10/+8/+12`, `5.4% floor`, `cap 99`, `top 4` | `matching.test.ts` 13 tests |
| Validation | `src/lib/matching.ts` | `EMAIL_RE`, `ZIP ^\d{5}$`, phone digits `≥10` | `validateApplication` 11 checks |
| Rate limit | `src/lib/rate-limit.ts` | `8/10min` funnel, `60/min` calculator, `x-forwarded-for` first entry | `funnel.spec.ts` isol. + burst `429` |
| Redirects | `next.config.ts` | 11 (4 loans, 2 manufacturers, 1 states, 1 get-started-v2, 1 playbook, 2 compare) | `build` + `assets.spec.ts` |
| Images | `public/images/*` | `5` + `brand/og-image.jpg` | `assets.spec.ts` `6×200` + broken-img |
| Sitemap | `src/app/sitemap.ts` | `STATIC_PATHS 39` → `152` locs (39+23+50+40 = 152) | `seo.spec.ts` `30×200` (host-rewrite to 3002) |
| Env | `.env.example` | 12 + `FEATURE_*` | `src/db/index.ts` throw on missing |
| Pre-ship gate | `AGENTS.md` | `db:setup → lint (0/0) → typecheck → test 41/41 → build 43/43 (35+8) → e2e 121/121 (120/121 DB-less; 122 listed→121 executed)` | `drizzle` journal `idx 0,1` |

**Copy-paste env generation:**

```bash
openssl rand -base64 32   # BETTER_AUTH_SECRET
openssl rand -hex 16      # CRON_SECRET  → ec16d809a08c91d24dbfdab7e7be4a99
grep -c "^env\." src/lib/env/index.ts || echo "no env module — process.env.DATABASE_URL is direct"
```

---

## Appendix E: The Meticulous Approach (6-Phase Workflow)

*Enforced by `CLAUDE.md` — every task in this repo follows it. The SKILL is itself produced by it.*

```
ANALYZE  → Deep, multi-dimensional requirement mining. Never assume. Surface ambiguities, explore alternatives, assess risks/dependencies.
PLAN     → Structured roadmap with sequenced phases, checklists, success criteria, estimates. Present for confirmation.
VALIDATE → Explicit user approval before coding. Address concerns/modifications.
IMPLEMENT→ Modular, tested, documented. Set up env, build in testable slices, docs alongside code. Library-first (ui.tsx).
VERIFY   → QA against success criteria: lint, typecheck, test, build, a11y/perf, edge cases. Run every gate command.
DELIVER  → Complete handoff: usage, runbooks, challenges/solutions, next steps. Nothing left ambiguous.
```

**This SKILL's delivery is phase 6.** Phase 1 (Archaeology) collected `package.json`, `src/**`, `drizzle/**`, `public/**`, `e2e/**` evidence; Phase 2 mapped 20 sections to files; Phase 3 produced the plan you approved; Phase 4 wrote section-by-section; Phase 5 is your `grep` + `typecheck` + line-count QA below; Phase 6 is this handoff + `how to use` guide at the top.

---

*End of home-financing_SKILL.md — Every claim traces to a specific file, test, or live probe. Nothing is here because it's popular.*

---

### Validation Checklist (for maintainers — run before bumping this SKILL)

- [ ] Every version in §2 matches `npm list --depth=0` exactly
- [ ] `grep -A50 "@theme" src/app/globals.css | head` hex values match §4/§19
- [ ] `grep -r "'use client'" src/components | wc -l` → `5` client islands of `9` components (`site-header, prequal-form, calculator-app, learn-explorer, reveal`) + the required `src/app/error.tsx` boundary (6 `'use client'` files total under `src/`)
- [ ] `npm run test 2>&1 | grep Tests` → `41` (11+13+9+8) still; `npm run e2e 2>&1 | grep "passed"` → `121` per project (120/121 DB-less — funnel valid-payload needs Postgres; --list 122→121 artifact)
- [ ] `find src/components -name "*.tsx" | wc -l` → 9; `ls public/images/*.jpg | wc -l` → 5 + `brand/og-image.jpg`
- [ ] Every env var count matches `.env.example` (12 tracked + `FEATURE_*`)
- [ ] `grep -n "TODO\|FIXME\|placeholder\|example.com" home-financing_SKILL.md | wc -l` → `0` (allow `orders@modfii.example` + `team@modfii.com` only)
- [ ] TOC matches all `^## ` / `^### ` headings; appendices A–E referenced from body
- [ ] `wc -l home-financing_SKILL.md` → `1,800–2,800` for this mid-size project (PAD `1,140` + SKILL `~1,000–1,400` = combined `~2,100–2,500`)

*Last verified 2026-09-15 (SKILL v1.8 — pass-9 drift alignment D-01→D-07: STATIC_PATHS 40→39, build 36+7/42+8→35+8, E2E 61/82→121, radii 1.25/1.5→0.625/0.75/1.0, MORE 4→2, blur-md→lg; validation `docs/VALIDATION_REPORT_SKILL_2026-09-15.md` 11 drifts patched, gates `lint 0/0 typecheck 41/41 build 43/43 e2e 121/121 (120/121 DB-less)`; pass-8 audit remediation `.env` hygiene + vitest 4.1.11; pass-7 live-source parity. Earlier: 2026-09-13 pass 4 — source-exact home hero, hub Last-Updated + truth callout, loan-page heroes, calculator pill + blue tax segment; `41/41` vitest = 11+13+9+8 incl. H4/OOM + `121/121` per project playwright = smoke 8+seo 16+funnel 5+assets 19+parity 73 (120/121 DB-less; 122 listed→121 executed) + DB init `8/40/50/23/59/5`.) against `package.json` (next ^16.3.4), `tsconfig.json` (strict, skills excluded), `next.config.ts` (11 redirects), `drizzle.config.*` (`5434`), `docker-compose.yml` (`home_financing_*` + `pgcrypto/pg_trgm`), `src/db/schema.ts` (8 tables), `src/lib/*` (41 tests = 11+13+9+8), `public/brand/wordmarks 5` + `public/images/avatars 3`, `playwright.config.ts` (`3002`), `e2e/*` 121 per project (103 decl; 122 listed), `.env.example`. Evidence: `docs/VALIDATION_REPORT_SKILL_2026-09-15.md` + `docs/REMEDIATION_PLAN_pass3.md` + `docs/REMEDIATION_PLAN_pass4.md` + `docs/REMEDIATION_PLAN_pass5.md`.*
