---
name: nextjs16-react19-postgres17
description: Full-stack Next.js 16 + React 19 + PostgreSQL 17 reference app with Drizzle ORM, BullMQ job queues (Redis), Auth.js v5, Vercel AI SDK (Anthropic + OpenAI), RSS/Atom ingestion, web push notifications. 5-layer architecture (proxy → app → features → domain → lib), App Router Server Components, async params, Suspense boundaries, PPR/cacheComponents, TypeScript strict + erasableSyntaxOnly, pnpm, Zod validation, Vitest + Playwright E2E + testcontainers. Editorial design system with CSS Subgrid, WCAG AAA accessibility, 3-layer AI provenance (JSON-LD + HTTP header + meta tag), Docker standalone output. Use for production full-stack SaaS with auth, job queues, AI pipelines, RSS/content ingestion, web push, admin panels, and database patterns."
version: 3.0.0
---

# OneStopNews — Engineering Skill Reference

> **Purpose:** Single-source engineering reference for the OneStopNews codebase. Other coding agents (Claude, Gemini, Codex, etc.) should consult this file when extending, debugging, or replicating this project. Every section is grounded in actual code — exact classNames, color values, configuration flags, and the reasoning behind every non-obvious decision.

> **Authoritative Sources:** This SKILL.md is derived from `AGENTS.md` (the canonical institutional knowledge base post-Phase 19) · `MASTER_EXECUTION_PLAN.md` v7.0 · `CLAUDE.md` · `README.md` · the actual source tree under `src/`. When in doubt, consult AGENTS.md as the source of truth.

---

## Table of Contents

1. [Project Identity & Design Philosophy](#1-project-identity--design-philosophy)
2. [Tech Stack & Environment](#2-tech-stack--environment)
3. [Bootstrapping & Configuration](#3-bootstrapping--configuration)
4. [The Design System (Code-First)](#4-the-design-system-code-first)
5. [Component Architecture & Patterns](#5-component-architecture--patterns)
6. [Custom Hooks Deep Dive](#6-custom-hooks-deep-dive)
7. [Content Management: RSS Ingestion Pipeline](#7-content-management-rss-ingestion-pipeline)
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

---

## 1. Project Identity & Design Philosophy

### What OneStopNews Is

**OneStopNews** is a **topic-first news aggregation platform with source-cited AI summaries**. Instead of presenting news by source or chronologically, it reorganises public news content around **subjects** (a two-level topic hierarchy). It collects article metadata from 50–200+ diverse RSS/Atom/JSON feeds, normalises and categorises stories, and pairs every AI-generated summary with a transparent **"Nutrition Label"** disclosing the model, temperature, coverage percentage, and citations.

### The Core Thesis: "Editorial Dispatch"

The design system is called **"Editorial Dispatch"** — a deliberate rejection of the homogenised "AI slop" aesthetic (purple gradients, generic Inter/Roboto typography, predictable card grids). The thesis:

> **A news platform should feel like a well-edited newspaper — calm, authoritative, and unmistakably crafted — not like a generic SaaS dashboard.**

The system has three intentional poles:

1. **Editorial Restraint** — Newsreader serif headlines evoke print journalism; Instrument Sans UI body keeps density legible; Commit Mono metadata mimics wire-service dispatch formatting (`UPPERCASE TRACKING-WIDEST TEXT-[10px]`).
2. **Tactile Confidence** — Micro-interactions are subtle but present: card hover state changes background + adds 1px shadow; button hover scales 1.02%; link underlines animate left-to-right on hover. No bouncy springs, no parallax, no skeuomorphism.
3. **Provenance as Aesthetics** — The "Nutrition Label" sidebar with `border-l-2 border-dispatch-ember` is not just a UI pattern — it's a visible commitment to AI transparency. The aesthetic encodes the ethics.

### Explicit Rejections (Anti-Generic Mandate)

These choices are FORBIDDEN. If you see them in a PR, reject the PR.

| Rejected Choice                                     | Why                                                    | Use Instead                                                                |
| :-------------------------------------------------- | :----------------------------------------------------- | :------------------------------------------------------------------------- |
| Inter / Roboto / Space Grotesk                      | "Safe" generic fonts — every AI-generated UI uses them | Newsreader (headlines), Instrument Sans (UI), Commit Mono (metadata)       |
| Fira Code / JetBrains Mono                          | Generic dev mono fonts                                 | Commit Mono (self-hosted woff2)                                            |
| Purple gradient on white                            | The single most clichéd AI aesthetic                   | `dispatch-ember` (#c7513f) — warm terracotta, evokes print ink             |
| Predictable card grids with rounded-xl + shadow-2xl | "SaaS dashboard" aesthetic                             | CSS Subgrid flat cards with `border-b border-ink-100` dividers             |
| Tailwind default `amber-*` / `red-*` for warnings   | Breaks design system                                   | `dispatch-warning` (#b45309), `dispatch-danger` (#dc2626) — Phase 19 / M15 |
| Raw hex colors in components (`bg-[#1a1a2e]`)       | Bypasses token system                                  | Design tokens only (`bg-ink-900`, `text-paper-50`)                         |
| Fixed pixel heights for cards                       | Breaks responsive, defeats Subgrid                     | CSS Subgrid with `grid-rows-subgrid row-span-3`                            |

### The Three Foundational Pillars

| Pillar                 | What It Means                                   | How It Manifests                                                                                                            |
| :--------------------- | :---------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------- |
| **Topic-first**        | Stories organized by subject, not source        | `categories` + `subcategories` tables; `/topics/[category]` route                                                           |
| **Source-cited AI**    | Every AI summary cites verifiable sources       | `sourcesCited: { url, title }[]` in Zod schema; NutritionLabel renders `[1]`, `[2]` superscript links                       |
| **3-Layer Provenance** | Machine-readable disclosure on every AI summary | JSON-LD `<script>` in body + `X-AI-Provenance` HTTP header + `<meta name="ai-provenance">` — EU AI Act Article 50 compliant |

---

## 2. Tech Stack & Environment

### Exact Versions (verified against `package.json` + `pnpm-lock.yaml`)

| Layer               | Package                                                           | Version                       | Notes                                                                                                                                   |
| :------------------ | :---------------------------------------------------------------- | :---------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| **Runtime**         | Node.js                                                           | `>=24.0.0` (24 LTS "Krypton") | Pinned in `package.json` `engines.node` + Dockerfiles use `node:24-alpine`                                                              |
| **Package Manager** | pnpm                                                              | `>=9.0.0` (9.15.9 installed)  | Pinned via `packageManager: "pnpm@9.15.0"`                                                                                              |
| **Framework**       | next                                                              | `^16.2.9`                     | CVE-2025-55182 mitigated (≥16.0.7 minimum)                                                                                              |
| **UI Library**      | react / react-dom                                                 | `^19.2.7`                     | React 19 stable                                                                                                                         |
| **Language**        | typescript                                                        | `^5.7.0`                      | Strict mode + `erasableSyntaxOnly`                                                                                                      |
| **Styling**         | tailwindcss                                                       | `^4.3.1`                      | CSS-first `@theme` config (no `tailwind.config.js`)                                                                                     |
| **PostCSS**         | `@tailwindcss/postcss`                                            | `^4.3.1`                      | MANDATORY — without it, zero utilities generate                                                                                         |
| **Database**        | PostgreSQL                                                        | 17                            | Run via Docker (`postgres:17` image)                                                                                                    |
| **ORM**             | drizzle-orm                                                       | `^0.45.2`                     | Lazy Proxy connection pattern                                                                                                           |
| **Migrations**      | drizzle-kit                                                       | `^0.31.10`                    | `generate` + `migrate` only — NEVER `push` in prod                                                                                      |
| **DB Driver**       | postgres (postgres.js)                                            | `^3.4.9`                      | NOT `pg` — postgres.js is the driver                                                                                                    |
| **Queue**           | bullmq                                                            | `^5.78.0`                     | 4 workers: ingest(50), summarize(5), score(20), feedSlice(10)                                                                           |
| **Redis Client**    | ioredis                                                           | `^5.11.1`                     | For BullMQ + rate limiting                                                                                                              |
| **Auth**            | next-auth                                                         | `5.0.0-beta.31`               | Auth.js v5 beta — 4 known `as any` casts in `lib/auth/index.ts` (DrizzleAdapter type mismatch)                                          |
| **Auth Adapter**    | @auth/drizzle-adapter                                             | `^1.11.2`                     |                                                                                                                                         |
| **AI SDK**          | ai (Vercel AI SDK v6)                                             | `^6.0.201`                    | `generateObject()` returns `result.object` directly                                                                                     |
| **AI Providers**    | @ai-sdk/anthropic / @ai-sdk/openai                                | `^3.0.85` / `^3.0.73`         | Primary: Claude Haiku 4.5; Fallback: GPT-5 Mini                                                                                         |
| **Validation**      | zod                                                               | `^4.4.3`                      | Used for env vars + AI output schema                                                                                                    |
| **HTML Parsing**    | cheerio                                                           | `^1.2.0`                      | Real HTML parser (replaces regex stripping) — Phase 19 / H9                                                                             |
| **RSS Parsing**     | rss-parser                                                        | `^3.13.0`                     | RSS 2.0 + Atom 1.0                                                                                                                      |
| **Date**            | luxon                                                             | `^3.7.2`                      | DST-safe quiet hours for push notifications                                                                                             |
| **Web Push**        | web-push                                                          | `^3.6.7`                      | VAPID keys + AES-256-GCM encrypted subscription keys                                                                                    |
| **Crypto**          | bcryptjs                                                          | `^3.0.3`                      | Password hashing for Credentials provider                                                                                               |
| **UI Primitives**   | @radix-ui/react-accordion, react-dialog, react-slot               | `^1.2.x`                      | Shadcn-style wrapping                                                                                                                   |
| **Class Utils**     | class-variance-authority, clsx, tailwind-merge                    | `^0.7.1`, `^2.1.1`, `^3.6.0`  | `cn()` utility                                                                                                                          |
| **HTTP**            | undici                                                            | `^8.5.0`                      | Direct dep + pnpm override via `pnpm-workspace.yaml` (Phase 23 / BUG-3 — pnpm 9.15+ requires this, not `package.json` `pnpm.overrides`) |
| **Icons**           | lucide-react                                                      | `^1.18.0`                     |                                                                                                                                         |
| **Testing**         | vitest, @vitest/coverage-v8                                       | `^4.1.9`                      | jsdom env + 80/70/80/80 thresholds                                                                                                      |
| **E2E**             | @playwright/test, @axe-core/playwright                            | `^1.61.0`, `^4.11.3`          | 10 E2E + 4 a11y scans                                                                                                                   |
| **Integration**     | testcontainers, @testcontainers/postgresql, @testcontainers/redis | `^12.0.3`                     | Docker-gapped DB integration tests                                                                                                      |

### Critical TypeScript Flags (`tsconfig.json`)

These flags are **non-negotiable**. Removing any of them will cause either silent bugs or build failures.

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "strict": true, // Master switch — all strict checks
    "noUncheckedIndexedAccess": true, // arr[i] returns T | undefined (catches runtime undefined access)
    "verbatimModuleSyntax": true, // Requires `import type` for type-only imports
    "erasableSyntaxOnly": true, // FORBIDS `enum` and `namespace` — use string unions + ES modules
    "strictNullChecks": true,
    "noImplicitAny": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noImplicitOverride": true,
    "isolatedModules": true,
    "moduleResolution": "bundler",
    "jsx": "react-jsx",
    "paths": { "@/*": ["./src/*"] }
  },
  "exclude": [
    "node_modules",
    ".next",
    "drizzle",
    "e2e",
    "playwright.config.ts",
    "skills"
  ]
}
```

**`erasableSyntaxOnly` is the most important flag.** It forbids TypeScript constructs that emit runtime code (`enum`, `namespace`, parameter properties). This forces all "enums" to be string unions or Drizzle `pgEnum()` (which emits SQL, not TS runtime code). If you write `enum Status { ACTIVE = "active" }`, tsc will fail with `error TS1294: This syntax is not allowed when 'erasableSyntaxOnly' is enabled`.

**`noUncheckedIndexedAccess` is the second most important.** Without it, `arr[0]` returns `T` — but at runtime it might be `undefined`. With it, `arr[0]` returns `T | undefined`, forcing you to handle the empty case. This catches hundreds of bugs that would otherwise only surface in production.

### Environment Variables (17 total: 10 required + 6 optional + 1 with default)

All validated by Zod at module load in `src/lib/env/index.ts`. The app fails fast with a descriptive error if any required var is missing or invalid.

```bash
# Required (10)
DATABASE_URL=postgresql://user:pass@localhost:5432/onestopnews  # must start with postgres:// or postgresql://
REDIS_URL=redis://localhost:6379                                # must start with redis://
AUTH_SECRET=                                                     # min 32 chars; rejects weak values in prod (superRefine)
AUTH_URL=http://localhost:3000
ANTHROPIC_API_KEY=sk-ant-...                                    # must start with sk-ant-
OPENAI_API_KEY=sk-...                                           # must start with sk-
NEXT_PUBLIC_VAPID_PUBLIC_KEY=                                    # npx web-push generate-vapid-keys
VAPID_PRIVATE_KEY=
VAPID_SUBJECT=mailto:admin@onestopnews.com
PUSH_KEY_ENCRYPTION_KEY=                                         # 64 hex chars (32 bytes); openssl rand -hex 32

# Optional (6) — OAuth providers (both ID + SECRET required to enable)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GITHUB_CLIENT_ID=
GITHUB_CLIENT_SECRET=
TRUSTED_PROXY=          # "true" | unset — use rightmost IP behind CDN
TRUSTED_PROXY_CIDRS=    # comma-separated CIDRs for proxy-chain walking

# With default
NODE_ENV=development    # development | production | test (default: development)
```

**CRITICAL RULE:** Never read `process.env.*` directly in production code. Import `env` from `@/lib/env` and access `env.VAR_NAME`. The Zod schema validates everything at module load. Direct `process.env.*` reads bypass validation — typos like `GOOGLE_CLIENTID` (missing underscore) silently return `undefined` and disable OAuth with no error.

**Phase 21 Security:** `.env`, `.env.docker`, `.env.local` are gitignored. Only `.env.example` is tracked (placeholder values). `AUTH_SECRET` rejects known-weak values (`dev-secret`, `test-secret`, `ci-dummy`, `change-me`, `placeholder`, etc.) in production via `superRefine`.

---

## 3. Bootstrapping & Configuration

### From Zero: Recreating This Project

```bash
# 1. Scaffold Next.js 16 + TypeScript + Tailwind v4
pnpm create next-app@latest onestopnews \
  --typescript \
  --tailwind \
  --eslint \
  --app \
  --src-dir \
  --import-alias "@/*" \
  --use-pnpm

cd onestopnews

# 2. Install runtime dependencies (exact versions from package.json)
pnpm add next@^16.2.9 react@^19.2.7 react-dom@^19.2.7
pnpm add drizzle-orm@^0.45.2 postgres@^3.4.9
pnpm add bullmq@^5.78.0 ioredis@^5.11.1
pnpm add next-auth@5.0.0-beta.31 @auth/drizzle-adapter@^1.11.2
pnpm add ai@^6.0.201 @ai-sdk/anthropic@^3.0.85 @ai-sdk/openai@^3.0.73
pnpm add zod@^4.4.3 cheerio@^1.2.0 rss-parser@^3.13.0
pnpm add luxon@^3.7.2 web-push@^3.6.7 bcryptjs@^3.0.3
pnpm add undici@^8.5.0
pnpm add @radix-ui/react-accordion@^1.2.14 @radix-ui/react-dialog@^1.1.16 @radix-ui/react-slot@^1.2.5
pnpm add class-variance-authority@^0.7.1 clsx@^2.1.1 tailwind-merge@^3.6.0
pnpm add lucide-react@^1.18.0

# 3. Install dev dependencies
pnpm add -D drizzle-kit@^0.31.10
pnpm add -D vitest@^4.1.9 @vitest/coverage-v8@^4.1.9
pnpm add -D @playwright/test@^1.61.0 @axe-core/playwright@^4.11.3
pnpm add -D testcontainers@^12.0.3 @testcontainers/postgresql@^12.0.3 @testcontainers/redis@^12.0.3
pnpm add -D @testing-library/react@^16.3.2 @testing-library/dom@^10.4.1 @testing-library/jest-dom@^6.9.1
pnpm add -D jsdom@^29.1.1
pnpm add -D husky@^9.1.7 lint-staged@^17.0.8
pnpm add -D prettier@^3.8.4 prettier-plugin-tailwindcss@^0.8.0
pnpm add -D typescript@^5.7.0 typescript-eslint@^8.61.0
pnpm add -D tsx@^4.22.4
pnpm add -D @types/node@^25.9.3 @types/react@^19.2.17 @types/react-dom@^19.2.3

# 4. Create pnpm-workspace.yaml for the cheerio>undici CVE override (Phase 23 / BUG-3)
#    pnpm 9.15+ no longer reads pnpm.overrides in package.json — MUST be in pnpm-workspace.yaml
cat > pnpm-workspace.yaml << 'EOF'
packages: []
overrides:
  undici: "^8.5.0"
EOF
```

### Critical Configuration Files

#### `next.config.ts` — The 5 Most Important Flags

```typescript
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // 1. OUTPUT: "standalone" — required for Docker deployment
  output: "standalone",

  // 2. CACHE COMPONENTS — TOP-LEVEL (not inside experimental!)
  // Enables "use cache" directive, PPR, opt-in caching model.
  // Replaces ALL of: experimental.ppr + dynamicIO.
  cacheComponents: true,

  // 3. CACHE LIFE PROFILES — TOP-LEVEL alongside cacheComponents
  // MUST be defined here before any cacheLife('profileName') call works.
  cacheLife: {
    feed: { stale: 30, revalidate: 120, expire: 600 },
    topicShell: { stale: 300, revalidate: 900, expire: 86400 },
    reference: { stale: 3600, revalidate: 86400, expire: 604800 },
  },

  // 4. TURBOPACK — TOP-LEVEL in Next.js 16 (graduated from experimental)
  turbopack: {},

  // 5. SECURITY HEADERS — CSP, HSTS, X-Frame-Options, X-Content-Type-Options
  // Phase 22 / H1: 'unsafe-eval' ACTUALLY removed (Phase 21 S4 was a comment-only fix)
  async headers() {
    return [
      {
        source: "/(.*)",
        headers: [
          { key: "X-Content-Type-Options", value: "nosniff" },
          { key: "X-Frame-Options", value: "DENY" },
          { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
          {
            key: "Permissions-Policy",
            value: "geolocation=(), microphone=(), camera=()",
          },
          {
            key: "Strict-Transport-Security",
            value: "max-age=63072000; includeSubDomains; preload",
          },
          {
            key: "Content-Security-Policy",
            value: [
              "default-src 'self'",
              "script-src 'self' 'unsafe-inline'", // NO 'unsafe-eval' — Phase 22 / H1
              "style-src 'self' 'unsafe-inline'",
              "img-src 'self' https: data:",
              "font-src 'self' data:",
              "connect-src 'self'",
              "frame-ancestors 'none'",
              "base-uri 'self'",
              "form-action 'self'",
            ].join("; "),
          },
        ],
      },
    ];
  },

  experimental: {
    viewTransition: true, // MUST be inside experimental: {}
    // DO NOT INCLUDE: experimental.ppr (build error in Next.js 16)
    // DO NOT INCLUDE: experimental.dynamicIO (deprecated)
    // DO NOT INCLUDE: experimental.clientSegmentCache (not in 16.2.9 ExperimentalConfig)
  },
};

export default nextConfig;
```

**Flag Placement Is Critical** (wrong placement = silent breakage):

| Flag                              | Placement                     | What Breaks if Wrong                  |
| :-------------------------------- | :---------------------------- | :------------------------------------ |
| `cacheComponents: true`           | **Top-level**                 | Every `"use cache"` silently ignored  |
| `cacheLife` profiles              | **Top-level**                 | `cacheLife('feed')` throws at runtime |
| `turbopack: {}`                   | **Top-level**                 | Ignored or config warning             |
| `experimental.viewTransition`     | **Inside `experimental: {}`** | Transitions silently disabled         |
| `experimental.ppr`                | **DO NOT INCLUDE**            | Build error in Next.js 16             |
| `experimental.dynamicIO`          | **DO NOT INCLUDE**            | Deprecated                            |
| `experimental.clientSegmentCache` | **DO NOT INCLUDE**            | Not in 16.2.9 type — TS error         |

#### `postcss.config.mjs` — The Tailwind v4 Plugin Is MANDATORY

```javascript
export default {
  plugins: {
    "@tailwindcss/postcss": {},
  },
};
```

**Without this file, zero Tailwind utility classes generate.** The page will load completely unstyled. If you see a page with raw HTML and no styling, this is almost always the cause. Fix: create `postcss.config.mjs`, install `@tailwindcss/postcss`, then `rm -rf .next/` to clear the cache.

#### `eslint.config.mjs` — Domain Layer Purity Rule

```javascript
import tseslint from "typescript-eslint";

export default [
  {
    ignores: [
      ".next/**",
      "node_modules/**",
      "drizzle/**",
      "dist/**",
      "skills/**",
      "docs/**",
      "coverage/**",
    ],
  },
  {
    files: ["**/*.ts", "**/*.tsx"],
    languageOptions: { parser: tseslint.parser },
    plugins: { "@typescript-eslint": tseslint.plugin },
    rules: {
      "@typescript-eslint/no-unused-vars": "error",
      "@typescript-eslint/no-explicit-any": "error",
    },
  },
  // Domain layer purity rule (Phase 20 / H1):
  // src/domain/** may import from @/lib/db ONLY via `import type`
  // (compile-time-only, erased at build — no runtime coupling).
  {
    files: ["src/domain/**/*.ts"],
    rules: {
      "no-restricted-imports": [
        "error",
        {
          paths: [
            {
              name: "@/lib/db",
              message:
                "Runtime imports forbidden in src/domain/**. Use `import type { ... } from '@/lib/db/schema'`.",
              allowTypeImports: true,
            },
            {
              name: "@/lib/db/schema",
              message: "Runtime imports forbidden. Use `import type` instead.",
              allowTypeImports: true,
            },
            {
              name: "@/lib/db/index",
              message:
                "Runtime imports forbidden. The domain layer must be pure.",
              allowTypeImports: true,
            },
          ],
        },
      ],
    },
  },
];
```

#### `.prettierignore` — Scope Format Checks (Phase 22 / N6)

Without this file, `pnpm format:check` scans 226+ markdown files in `skills/`, `docs/`, archived plans — false-positive CI failures.

```gitignore
node_modules/
.next/
dist/
coverage/
pnpm-lock.yaml
drizzle/meta/
skills/
docs/
*.archived
*.backup
*.bak
*.tar.gz
*.tar.bz2
*.tgz
e2e/
playwright-report/
.env
.env.*
!.env.example
.husky/
.github/
*.png
*.jpg
*.jpeg
*.gif
*.svg
*.woff
*.woff2
*.ttf
```

**Active docs at repo root (`README.md`, `AGENTS.md`, `CLAUDE.md`, `MASTER_EXECUTION_PLAN.md`, `Codebase_Review_Validation_Report_*.md`) are NOT excluded** — they should be kept formatted.

---

## 4. The Design System (Code-First)

### The `@theme` Block (in `src/app/globals.css`)

This is the single source of truth for all design tokens. Tailwind v4 reads this block and generates utilities like `bg-ink-900`, `text-dispatch-ember`, `font-editorial`.

```css
@import "tailwindcss";

@theme {
  /* ── Ink Scale (text colors, dark surfaces) ── */
  --color-ink-900: #1a1a18; /* Headlines — WCAG AAA 15:1 on paper-50 */
  --color-ink-700: #2a2a27;
  --color-ink-600: #3d3d3a; /* Body text — WCAG AAA 9.5:1 on paper-50 */
  --color-ink-500: #525250;
  --color-ink-400: #6b6b68;
  --color-ink-300: #8a8a83; /* Muted text, metadata dividers */
  --color-ink-100: #e8e8e4; /* Borders, scrollbar thumb */

  /* ── Paper Scale (backgrounds, card surfaces) ── */
  --color-paper-50: #fafaf8; /* Page background — warm off-white */
  --color-paper-100: #f2f2ee; /* Card hover background, nutrition label bg */
  --color-paper-200: #e6e4de; /* Image placeholders */
  --color-paper-300: #d8d4cc; /* Card borders on dark surfaces */

  /* ── Dispatch Brand Accents ── */
  --color-dispatch-ember: #c7513f; /* PRIMARY ACCENT — breaking/AI badge/focus rings */
  --color-dispatch-ember-light: #fde8e4;
  --color-dispatch-sage: #6b8f71; /* "Active" status indicator */
  --color-dispatch-sage-light: #e4ede5;
  --color-dispatch-slate: #5a6b7a; /* Neutral source attribution */
  --color-dispatch-slate-light: #e2e7ec;
  --color-dispatch-clay: #8b6d5a; /* Warm earth tone (accent) */
  --color-dispatch-clay-light: #ede5df;
  --color-dispatch-violet: #7a6b8f; /* Citation links */
  --color-dispatch-violet-light: #e8e4ef;

  /* ── Semantic State Tokens (Phase 19 / M15) ── */
  --color-dispatch-warning: #b45309; /* amber-700 equivalent — SummaryPanel needs_review */
  --color-dispatch-warning-light: #fef3c7;
  --color-dispatch-danger: #dc2626; /* red-600 equivalent — Button destructive variant */
  --color-dispatch-danger-dark: #b91c1c;

  /* ── Typography Stack ── */
  --font-editorial: "Newsreader", Georgia, "Times New Roman", serif;
  --font-ui: "Instrument Sans", system-ui, -apple-system, sans-serif;
  --font-mono: "Commit Mono", ui-monospace, "Fira Code", monospace;
}
```

### Font Loading (in `src/app/layout.tsx`)

Three fonts loaded via `next/font` — **never via CSS `@font-face` or `@fontsource`** (which broke Commit Mono in Phase 12):

```tsx
import { Newsreader, Instrument_Sans } from "next/font/google";
import localFont from "next/font/local";

const newsreader = Newsreader({
  variable: "--font-editorial",
  subsets: ["latin"],
  weight: ["400", "500", "600", "700", "800"],
  display: "swap",
});

const instrumentSans = Instrument_Sans({
  variable: "--font-ui",
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
  display: "swap",
});

// Commit Mono is SELF-HOSTED via next/font/local — @fontsource/commit-mono broke in Phase 12
const commitMono = localFont({
  src: "../../public/fonts/commit-mono-400.woff2",
  variable: "--font-mono",
  weight: "400",
  style: "normal",
  display: "swap",
});

// Apply all three CSS variables to <html>:
<html lang="en" className={`${newsreader.variable} ${instrumentSans.variable} ${commitMono.variable}`}>
```

### Typography Hierarchy (Exact Usage)

| Role                                                   | Font            | Weight  | Tailwind Class   | Example Usage                                                                     |
| :----------------------------------------------------- | :-------------- | :------ | :--------------- | :-------------------------------------------------------------------------------- |
| **Headlines** (H1, H2, H3)                             | Newsreader      | 800     | `font-editorial` | `<h1 className="font-editorial text-3xl sm:text-4xl text-ink-900">`               |
| **UI / Body**                                          | Instrument Sans | 400–600 | `font-ui`        | `<p className="font-ui text-sm leading-relaxed text-ink-600">`                    |
| **Metadata** (timestamps, source names, status badges) | Commit Mono     | 400     | `font-mono`      | `<span className="font-mono text-[10px] uppercase tracking-widest text-ink-300">` |

### The `.font-editorial` Enhancement Block

Defined in `globals.css` — applies typographic refinements to all editorial headlines:

```css
.font-editorial {
  font-weight: 800;
  line-height: 1.1;
  letter-spacing: -0.02em; /* Tight tracking for large display type */
  text-rendering: optimizeLegibility;
  font-feature-settings: "ss01", "ss02"; /* Newsreader stylistic sets */
}
```

### CSS Subgrid (The Feed Alignment Mechanism)

This is the **defining structural choice** of the feed UI. Instead of fixed heights or flex hacks, articles use CSS Subgrid so headlines/excerpts/metadata align across cards in the same row.

```css
/* In FeedGrid.tsx: */
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-8">
  {articles.map(article => (
    <ArticleCard key={article.id} article={article} />
  ))}
</div>

/* In ArticleCard.tsx: */
<article className="group relative grid grid-rows-subgrid row-span-3 gap-y-3 mb-10 last:mb-0 border-b border-ink-100 pb-6">
  <h3 className="font-editorial text-xl leading-tight text-ink-900">...</h3>  {/* Row 1 */}
  <p className="font-ui text-sm leading-relaxed text-ink-600 line-clamp-3">...</p>  {/* Row 2 */}
  <div className="flex items-center gap-3 font-mono text-[10px] uppercase tracking-wider text-ink-600 mt-auto">...</div>  {/* Row 3 */}
</article>
```

**Why Subgrid:** Headlines are 1–3 lines, excerpts are 0–3 lines, metadata is always 1 line. Without Subgrid, cards in the same row would have jagged bottoms. With Subgrid, all cards align on all 3 row tracks — calm, editorial, no visual noise.

### Custom Utility Classes (in `globals.css`)

| Class                         | Purpose                                | Definition                                                                           |
| :---------------------------- | :------------------------------------- | :----------------------------------------------------------------------------------- |
| `.story-card`                 | Card hover transition                  | `transition: background-color 200ms, box-shadow 200ms;` + hover state                |
| `.nutrition-label`            | AI summary sidebar                     | `border-left: 3px solid dispatch-ember; background: linear-gradient(...);`           |
| `.citation-ref`               | Inline citation links                  | `border-bottom: 1px dashed dispatch-violet;`                                         |
| `.btn-ember`                  | Primary CTA micro-interaction          | hover: `scale(1.02)` + `box-shadow: 0 4px 16px rgba(199, 81, 63, 0.25);`             |
| `.link-underline`             | Animated underline                     | `::after` width 0→100% on hover                                                      |
| `.cta-input`                  | Dark-background input                  | `background: rgba(255, 255, 255, 0.06);`                                             |
| `.cat-label`                  | Category badge                         | `font-mono; font-variant: all-small-caps; letter-spacing: 0.12em;`                   |
| `.cat-label-wide`             | Wide category badge                    | Same but `letter-spacing: 0.25em;`                                                   |
| `.outline-hidden`             | Tailwind v4 `outline-none` replacement | `outline: 2px solid transparent;` (a11y-preserving)                                  |
| `.reveal` + `.reveal.visible` | IntersectionObserver-driven fade-in    | `opacity: 0; transform: translateY(24px);` → `opacity: 1; transform: translateY(0);` |
| `.scroll-progress`            | CSS-only scroll progress bar           | `animation-timeline: scroll(); z-index: 999;`                                        |
| `.ticker-track`               | News ticker scroll                     | `animation: ticker-scroll 80s linear infinite;`                                      |
| `.pulse-dot`                  | Live indicator                         | `animation: pulse-dot 2s ease-in-out infinite;`                                      |
| `.commitment-number`          | Large editorial numerals               | `font-editorial; font-size: 4.5rem; opacity: 0.08;`                                  |

---

## 5. Component Architecture & Patterns

### The 5-Layer Request Model (Golden Rule)

This is the **single most important architectural principle** in the codebase. Deviation from this order creates security and consistency bugs.

```
Layer 0: proxy.ts           — Cookie check, redirect. NO DB. NO logic. NO Edge runtime.
Layer 1: App Router          — Route structure, metadata, PPR, Suspense. Layouts must NOT fetch data.
Layer 2: Feature Modules     — UI composition, data binding, mutations (feed, summaries, search, admin)
Layer 3: Domain Services     — Pure business logic. No Next.js or DB runtime imports (import type only)
Layer 4: Infrastructure      — Drizzle, Auth.js, BullMQ, AI SDK. Side effects only.
```

**Golden Rule:** A lower layer may never import from a higher layer. Domain may import types from Infrastructure but never runtime code. Feature Modules may import from Domain and Infrastructure. App Router may import from Feature Modules.

### Server Components by Default

**Server Components are the default.** Use `'use client'` only for:

- Components with `useState`, `useEffect`, `useReducer`, `useRef`
- Components using browser APIs (`window`, `document`, `localStorage`, `matchMedia`)
- Components using `usePathname`, `useRouter`, `useSearchParams`
- Components wrapped in `'use client'` contexts (`SessionProvider`, etc.)

**Never put `'use client'` on a Server Component.** Never import `'use client'` modules into Server Components beyond the boundary.

### Async `params` / `searchParams` / `cookies()` in Next.js 16

In Next.js 16, all three are `Promise<T>`. Always `await` them:

```tsx
// CORRECT
export async function ArticlePage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  // ...
}

// WRONG — synchronous access causes runtime 500
export function ArticlePage({ params }: { params: { id: string } }) {
  const { id } = params; // TypeError: params is not iterable
}
```

Same for `cookies()`:

```tsx
const cookieStore = await cookies();
const session = cookieStore.get("session");
```

### Suspense + Server Component Pattern (Mandatory for Dynamic Data)

Next.js 16 `cacheComponents: true` requires ALL async data fetching inside `<Suspense>` or `"use cache"`. Direct `await` in a page body triggers a `blocking-route` build error.

```tsx
// CORRECT — page shell is sync, async data is in a Server Component inside Suspense
export default function HomePage() {
  return (
    <div>
      <Header />
      <Suspense fallback={<FeedSkeleton />}>
        <FeedData />
      </Suspense>
      <Footer />
    </div>
  );
}

// FeedData.tsx — async Server Component
export async function FeedData() {
  const { articles, hasMore, nextCursor } = await getFeedArticles({});
  return (
    <FeedContainer
      initialArticles={articles}
      initialHasMore={hasMore}
      initialCursor={nextCursor}
    />
  );
}
```

### The `queries.ts` Boundary

**All DB access goes through feature-level `queries.ts` files.** No raw Drizzle calls in components.

```
src/features/feed/queries.ts         ← getFeedArticles, buildFeedQuery
src/features/articles/queries.ts     ← getArticleWithSummary
src/features/search/queries.ts       ← searchArticles, getSearchSuggestions
src/features/sources/queries.ts      ← getAllSources, getCategoryMap
src/features/summaries/queries.ts    ← summary-related queries
```

### Component Philosophy: "Engineered Soul"

Every component has a clear purpose, documented in a JSDoc header. The pattern:

```tsx
/**
 * ArticleCard — Subgrid child spanning 3 row tracks.
 *
 * Subgrid contract (PRD §4.3):
 *   Row 1: Headline — Editorial serif, weight 800.
 *   Row 2: Excerpt — UI sans, 3-line clamp.
 *   Row 3: Metadata — Mono, uppercase, auto-aligned.
 *
 * Data contract:
 *   `article.source.name` requires a JOIN with the sources table.
 *   Feed queries MUST use getFeedArticles() which includes this JOIN.
 */
export function ArticleCard({ article }: ArticleCardProps) {
  // ...
}
```

### Specific Component Patterns

#### `ArticleCard` — The Subgrid Card

```tsx
<article className="group relative grid grid-rows-subgrid row-span-3 gap-y-3 mb-10 last:mb-0 border-b border-ink-100 pb-6 transition-colors duration-300 hover:bg-paper-100/50">
  <h3 className="font-editorial text-xl leading-tight text-ink-900 group-hover:text-dispatch-ember transition-colors duration-300">
    <Link
      href={`/article/${article.id}`}
      className="after:absolute after:inset-0 focus:outline-none focus-visible:ring-2 focus-visible:ring-dispatch-ember focus-visible:ring-offset-2 focus-visible:ring-offset-paper-50 rounded-sm"
    >
      {article.title}
    </Link>
  </h3>
  <p className="font-ui text-sm leading-relaxed text-ink-600 line-clamp-3">
    {article.excerpt ?? <span className="text-ink-300 italic">No excerpt available.</span>}
  </p>
  <div className="flex items-center gap-3 font-mono text-[10px] uppercase tracking-wider text-ink-600 mt-auto">
    <span className="text-dispatch-slate font-medium truncate max-w-[120px]">{article.source.name}</span>
    <span className="w-1 h-1 rounded-full bg-ink-300 shrink-0" aria-hidden="true" />
    <time dateTime={...} className="shrink-0 tabular-nums">{formatTimeAgo(article.publishedAt)}</time>
    {article.hasSummary && article.summaryStatus === "ok" && (
      <>
        <span className="w-1 h-1 rounded-full bg-ink-300 shrink-0" aria-hidden="true" />
        <span className="text-dispatch-ember font-medium shrink-0 tracking-widest">AI Brief</span>
      </>
    )}
  </div>
</article>
```

**Key patterns:**

- `after:absolute after:inset-0` — makes the entire card clickable via the inner `<Link>` (the pseudo-element stretches over the whole card)
- `group-hover:text-dispatch-ember` — headline color changes when card is hovered
- `line-clamp-3` — excerpt clamped to 3 lines (uses Tailwind v4 built-in)
- `mt-auto` — metadata pinned to bottom of row 3 (Subgrid alignment)
- `tabular-nums` — dates use tabular figures (no width jitter)
- `aria-hidden="true"` on decorative dots (screen readers skip them)

#### `NutritionLabel` — The AI Transparency Sidebar

```tsx
<aside
  aria-label="AI-generated summary transparency label"
  className="border-l-2 border-dispatch-ember bg-paper-100/50 p-6"
>
  <div className="mb-4 flex items-center gap-2">
    <span
      className="h-2 w-2 rounded-full bg-dispatch-ember"
      aria-hidden="true"
    />
    <span className="font-mono text-[10px] uppercase tracking-widest text-ink-300">
      AI-Generated Summary
    </span>
  </div>
  <p className="font-ui text-base leading-relaxed text-ink-900">
    {summary.summaryText}
  </p>
  {/* Key Points + Sources Cited [1] [2] ... + Coverage % + "Verify with original source →" link */}
</aside>
```

#### `Button` — Shadcn-style with CVA Variants

```tsx
const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 rounded-sm font-ui font-medium text-sm transition-all duration-150 ease-out " +
    "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-dispatch-ember focus-visible:ring-offset-2 focus-visible:ring-offset-paper-50 " +
    "disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        primary:
          "bg-dispatch-ember text-paper-50 hover:bg-dispatch-ember/90 active:scale-[0.98]",
        secondary:
          "bg-ink-900 text-paper-50 hover:bg-ink-700 active:scale-[0.98]",
        outline:
          "border border-ink-100 bg-transparent text-ink-900 hover:bg-paper-100 hover:border-ink-300",
        ghost:
          "bg-transparent text-ink-600 hover:bg-paper-100 hover:text-ink-900",
        destructive:
          "bg-dispatch-danger text-paper-50 hover:bg-dispatch-danger-dark active:scale-[0.98]",
      },
      size: {
        sm: "h-8 px-3 text-xs",
        md: "h-10 px-4 text-sm",
        lg: "h-12 px-6 text-base",
        icon: "h-10 w-10 p-2",
      },
    },
    defaultVariants: { variant: "primary", size: "md" },
  },
);
```

**Note `rounded-sm`** (not `rounded-xl` or `rounded-2xl`) — Editorial Dispatch uses minimal radii. The "tactile maximalism" is in the hover micro-interactions, not in aggressive rounding.

### AdminGuard Pattern — Auth at the Layout Boundary

```tsx
// src/shared/components/auth/AdminGuard.tsx
export async function AdminGuard({
  children,
}: AdminGuardProps): Promise<React.ReactElement> {
  await verifyAdminSession(); // Redirects internally on failure; if it returns, user is admin
  return <>{children}</>;
}

// src/app/(admin)/layout.tsx
export default function AdminLayout({ children }) {
  return (
    <div className="min-h-screen bg-ink-900 text-paper-50">
      <Suspense fallback={<AdminGuardSkeleton />}>
        <AdminGuard>{children}</AdminGuard>
      </Suspense>
    </div>
  );
}
```

**This is the only correct admin auth pattern.** Per-page guards are forbidden — any new admin page that forgets the guard would be publicly accessible.

### Server Action Pattern — Every Action Starts with Auth

```tsx
"use server";

export async function requestSummary(
  articleId: string,
): Promise<SummariseResponse> {
  // 1. AUTH FIRST — verifySession() returns session or throws NEXT_REDIRECT
  const session = await verifySession();

  // 2. Rate limit (per user, not per IP — NAT would let one user burn budget for all)
  const rateLimitResult = await checkRateLimit(
    `api:summarize:${session.user.id}`,
    5,
    60,
  );
  if (!rateLimitResult.allowed) {
    return {
      success: false,
      jobId: null,
      error: "Rate limit exceeded. Please retry later.",
    };
  }

  // 3. Input validation (UUID regex)
  const uuidRegex =
    /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
  if (!uuidRegex.test(articleId)) {
    return { success: false, jobId: null, error: "Invalid article ID format" };
  }

  // 4. Content guard (anti-hallucination)
  const article = await db.query.articles.findFirst({
    where: eq(articles.id, articleId),
  });
  if (!article)
    return { success: false, jobId: null, error: "Article not found" };
  if (
    article.contentAvailability === "title_only" ||
    article.contentAvailability === "excerpt"
  ) {
    return {
      success: false,
      jobId: null,
      error: `Cannot summarise articles with only ${article.contentAvailability}.`,
    };
  }

  // 5. Mutation + revalidate
  await db
    .update(articles)
    .set({ summaryStatus: "pending" })
    .where(eq(articles.id, articleId));
  const job = await summarizeQueue.add("summarize", {
    articleId,
    content: article.excerpt ?? article.title,
  });
  return { success: true, jobId: job!.id!, error: null };
}
```

**Never wrap `verifySession()` in try/catch** — it catches the `NEXT_REDIRECT` thrown by `redirect()` and silently swallows it. API routes should use `auth()` directly (returns null → 401 JSON), not `verifySession()` (which redirects).

### JSON-LD Pattern (3-Layer Provenance)

```tsx
// In ArticleData.tsx (Server Component):
const jsonLdScript = article.summary?.status === "ok"
  ? generateProvenanceMetadata({ summary: {...}, articleId, articleUrl, articleTitle, model, generatedAt }).jsonLd
  : null;

return (
  <>
    {jsonLdScript && (
      <script
        type="application/ld+json"
        key={`provenance-jsonld-${article.id}`}
        dangerouslySetInnerHTML={{ __html: jsonLdScript }}
      />
    )}
    {/* Page content */}
  </>
);
```

**JSON-LD MUST be a `<script>` tag in the body** — NOT via `metadata.other`. Next.js 16 `metadata.other` only emits `<meta>` tags, never `<script>` tags. (Phase 17 fix.)

**CRITICAL — Phase 23 / BUG-2 fix:** The HTTP header (`X-AI-Provenance`) MUST be set in `next.config.ts` `headers()`, NOT via `metadata.other`. Next.js 16 `metadata.other` ONLY emits `<meta>` tags, NEVER HTTP headers. Setting `"X-AI-Provenance"` in `metadata.other` creates a useless `<meta name="X-AI-Provenance">` tag, not an HTTP header.

**Layer 2 (HTTP header) — in `next.config.ts`:**

```typescript
// next.config.ts — static header for all article routes
async headers() {
  return [
    // ... other headers (CSP, HSTS, XFO, XCTO) for "/(.*)" ...
    {
      source: "/article/:id*",
      headers: [
        {
          key: "X-AI-Provenance",
          value: "eu-ai-act-art50-compliant; disclosure-in-meta-and-jsonld",
        },
      ],
    },
  ];
}
```

**Layer 3 (meta tag) — in `generateMetadata()`:**

```tsx
export async function generateMetadata({ params }): Promise<Metadata> {
  const { id } = await params;
  const article = await getArticleWithSummary(id);
  if (!article?.summary || article.summary.status !== "ok") return {};

  const provenance = generateProvenanceMetadata({...});
  return {
    other: {
      "ai-provenance": provenance.metaTag,           // Layer 3: <meta name="ai-provenance">
      // DO NOT put "X-AI-Provenance" here — metadata.other only emits <meta> tags, not HTTP headers.
      // The HTTP header is set statically in next.config.ts headers() for /article/:id* routes.
    },
  };
}
```

**Regression test** in `next.config.test.ts` (16 tests covering CSP/HSTS/XFO/XCTO + X-AI-Provenance header):

---

## 6. Custom Hooks Deep Dive

### `useDebounce` — Generic Value Debounce

```tsx
"use client";

import { useState, useEffect } from "react";

export function useDebounce<T>(value: T, delay = 300): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const handler = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(handler); // Cleanup on unmount or value change
  }, [value, delay]);

  return debouncedValue;
}
```

**Why generic `<T>`:** Works for strings (search input), arrays (multi-select), objects (form state), anything. The `delay` default of 300ms is the right balance for search-as-you-type UX — fast enough to feel responsive, slow enough to avoid spamming the API.

**Why `useEffect` cleanup:** Without `clearTimeout`, every keystroke would schedule a timeout — the user would see stale debounced values flash through. Cleanup cancels pending timeouts when the value changes.

### `useReducedMotion` — WCAG AAA Motion Preference

```tsx
"use client";

import { useState, useEffect } from "react";

export function useReducedMotion(): boolean {
  const [reduced, setReduced] = useState(false); // SSR-safe default: false

  useEffect(() => {
    const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
    setReduced(mq.matches);

    const onChange = (e: MediaQueryListEvent) => setReduced(e.matches);
    mq.addEventListener("change", onChange);
    return () => mq.removeEventListener("change", onChange);
  }, []);

  return reduced;
}
```

**WCAG AAA rule:** When `prefers-reduced-motion: reduce`, **DISABLE all animations entirely** — do NOT just slow them. The CSS override in `globals.css`:

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0ms !important;
    transition-duration: 0ms !important;
  }
  .reveal {
    opacity: 1;
    transform: none;
    transition: none;
  }
}
```

This is a **belt-and-suspenders** approach — the CSS override handles all CSS animations, while the hook lets JS-driven animations (Framer Motion, GSAP) check the preference and skip themselves.

### `verifySession` / `verifyAdminSession` — The DAL Auth Pattern

These are not React hooks but `cache()`-memoized async functions. They are the **only correct way** to verify a session in Server Components and Server Actions.

```tsx
// src/lib/auth/dal.ts
import { cache } from "react";
import { redirect } from "next/navigation";
import { auth } from "./index";

export const verifySession = cache(async () => {
  const session = await auth();
  if (!session?.user?.email) redirect("/sign-in"); // THROWS NEXT_REDIRECT — never returns null

  const user = await db
    .select({ id: users.id, role: users.role, name: users.name })
    .from(users)
    .where(eq(users.email, session.user.email))
    .limit(1)
    .then((rows) => rows[0] ?? null);

  if (!user) redirect("/sign-in");
  return { user, sessionId: session.user.id as string };
});

export const verifyAdminSession = cache(async () => {
  const { user } = await verifySession();
  if (user.role !== "admin") redirect("/");
  return user;
});
```

**Critical behaviors:**

- `cache()` memoizes per-request — multiple components calling `verifySession()` execute one DB query
- `redirect()` THROWS `NEXT_REDIRECT` — never returns null. Any `if (!session)` after it is dead code.
- **Never wrap in try/catch** — catches `NEXT_REDIRECT` and silently swallows the redirect
- API routes use `auth()` directly (returns null → 401 JSON), not `verifySession()` (which redirects)

### `cacheLife` — Next.js 16 Cache Profile Selector

```tsx
"use cache";
import { cacheLife } from "next/cache";

export async function getFeedArticles(
  options: FeedQueryOptions,
): Promise<FeedPage> {
  "use cache";
  cacheLife("feed"); // 30s stale, 120s revalidate, 10-min hard eviction

  const rows = await buildFeedQuery(options);
  // ...
}
```

**Three profiles defined in `next.config.ts`:**

- `"feed"` — 30s stale, 120s revalidate, 10-min expire (news feed — fresh but cached)
- `"topicShell"` — 5-min stale, 15-min revalidate, 1-day expire (topic navigation)
- `"reference"` — 1-hour stale, daily revalidate, weekly expire (search results, categories)

**Testing gotcha:** `cacheLife()` throws `TypeError: cacheLife is not a function` outside Next.js cache context. In vitest, mock it:

```tsx
vi.mock("next/cache", () => ({ cacheLife: vi.fn() }));
```

### `useOptimistic` + `startTransition` — Instant UI for Server Actions

Used in `SummaryPanel` for the "Summarize" button — clicking it shows the loading state instantly without waiting for the server round-trip:

```tsx
"use client";

const [optimisticStatus, startTransition] = useOptimistic(initialStatus);

function handleSummarize() {
  startTransition(async () => {
    setOptimisticStatus("pending"); // UI updates instantly
    await requestSummary(articleId); // Server action runs
  });
}
```

---

## 7. Content Management: RSS Ingestion Pipeline

### The 4-Stage Pipeline

```
RSS Feed → parseFeed (rss-parser + cheerio) → determineContentAvailability → score → store
                                                                ↓
                                          summarize worker (if partial_text or full_text)
                                                                ↓
                                          generateProvenanceMetadata → store summary
```

### `parseFeed.ts` — RSS/Atom/JSON Feed Parser

Three formats supported via the `feedFormatEnum` in the schema:

```typescript
export const feedFormatEnum = pgEnum("feed_format", [
  "rss",
  "atom",
  "json_api",
]);
export type FeedFormat = (typeof feedFormatEnum.enumValues)[number];
```

The parser uses `rss-parser` for XML formats (RSS + Atom) and native `JSON.parse` for JSON Feed. HTML stripping uses `cheerio` (NOT regex — Phase 19 / H9 fix):

```typescript
import * as cheerio from "cheerio";

function stripHtml(html: string): string {
  const $ = cheerio.load(html);
  // Remove non-content tags entirely — their text should NOT appear in stripped output
  // (prevents <script>alert('evil')</script> from leaking "alert('evil')" into AI prompts)
  $("script, style, noscript, iframe, object, embed").remove();
  return $.text().replace(/\s+/g, " ").trim();
}
```

**Why cheerio over regex:** The regex `/<[^>]*>/g` strips TAGS but not their TEXT CONTENT. `<script>alert('evil')</script>` would leak `"alert('evil')"` into AI summaries. cheerio uses parse5 (a real browser-grade HTML parser) and handles all entity types (named, decimal, hex), CDATA sections, nested tags with attributes, and malformed HTML.

### `determineContentAvailability.ts` — Anti-Hallucination Guard

This is the **single most important anti-hallucination mechanism** in the codebase. It classifies each article into one of 4 tiers, and only `partial_text` / `full_text` articles are eligible for AI summarization.

```typescript
export const contentAvailabilityEnum = pgEnum("content_availability", [
  "title_only", // Title extracted only. DO NOT summarise.
  "excerpt", // Title + short excerpt (≤300 chars). DO NOT summarise.
  "partial_text", // Title + excerpt + partial body (300–1500 chars). Summarise permitted.
  "full_text", // Title + excerpt + full body (>1500 chars). Summarise preferred.
]);
```

**Enforced at BOTH layers:**

1. **Server Action** (`src/features/summaries/actions.ts:96-105`) — `requestSummary` rejects `title_only` / `excerpt`
2. **API Route** (`src/app/api/summarize/[id]/route.ts:89-99`) — `POST /api/summarize/[id]` rejects `title_only` / `excerpt`

This dual enforcement is intentional — if either layer is bypassed (e.g., a future admin script), the other catches it.

### BullMQ Worker Concurrency

```typescript
// src/workers/index.ts
new Worker("ingest", ingestProcessor, {
  concurrency: 50,
  connection: workerConnection,
});
new Worker("summarize", summarizeProcessor, {
  concurrency: 5,
  connection: workerConnection,
});
new Worker("score", scoreProcessor, {
  concurrency: 20,
  connection: workerConnection,
});
new Worker("feed-slice", feedSliceProcessor, {
  concurrency: 10,
  connection: workerConnection,
});
```

**Why these numbers:**

- `ingest: 50` — RSS parsing is I/O-bound (network fetch + XML parse). High concurrency is safe.
- `summarize: 5` — AI calls are expensive ($0.001–0.01 each) and rate-limited by Anthropic/OpenAI. Low concurrency prevents cost runaway.
- `score: 20` — Importance scoring is CPU-bound but fast (no network). Medium concurrency.
- `feed-slice: 10` — Cache invalidation fan-out. Medium concurrency.

### FlowProducer DAG (Atomic Ingest → Score → Feed-Slice)

```typescript
// src/lib/queue/flows.ts
export const enqueuePostIngestFlow = async (articleIds: string[]) => {
  try {
    await flowProducer.add({
      name: "ingest-complete",
      queueName: "feed-slice",
      data: { articleIds },
      children: articleIds.map((id) => ({
        name: "score-article",
        queueName: "score",
        data: { articleId: id },
      })),
    });
    return { status: "linked" as const, enqueuedCount: articleIds.length };
  } catch (error) {
    // CRITICAL: never re-throw if side effects already landed
    // Fall back to direct scoreQueue.add() per article
    for (const id of articleIds) {
      await scoreQueue.add("score-article", { articleId: id });
    }
    return {
      status: "degraded" as const,
      fallbackUsed: true,
      enqueuedCount: articleIds.length,
    };
  }
};
```

**Why try/catch + fallback:** If Redis is unreachable mid-flow, the articles are already persisted in Postgres (the ingest job completed). Re-throwing would cause BullMQ to retry the flow — but the articles have `xmax != 0` (already committed), so the retry would see them as existing and return empty `newArticleIds`, never re-enqueuing scoring. Silent data loss. The fallback ensures scoring always runs.

### Graceful Shutdown

```typescript
const shutdown = async () => {
  console.log("[worker] Received shutdown signal, closing workers...");
  const timeout = setTimeout(() => {
    console.error("[worker] Force-exit after 25s timeout");
    process.exit(1);
  }, 25000);
  timeout.unref(); // Don't keep the event loop alive for this timer

  await Promise.allSettled([
    ingestWorker.close(),
    summarizeWorker.close(),
    scoreWorker.close(),
    feedSliceWorker.close(),
    flowProducer.close(),
  ]);

  clearTimeout(timeout);
  console.log("[worker] All workers closed gracefully");
  process.exit(0);
};

process.on("SIGTERM", shutdown);
process.on("SIGINT", shutdown);
```

`Promise.allSettled` (not `Promise.all`) — we want to wait for all workers even if some fail. The 25s `unref`'d timeout ensures we don't hang forever on a stuck worker.

---

## 8. Accessibility (WCAG AAA) Implementation

### The 4 Pillars

1. **Skip-to-content link** — first focusable element in `<body>`
2. **Focus-visible rings** — `dispatch-ember` outline on all interactive elements
3. **Reduced motion** — CSS override + `useReducedMotion` hook
4. **Semantic HTML** — `<main>`, `<article>`, `<aside>`, `<time>`, `<nav>`, ARIA labels

### Skip-to-Content Link (`src/app/layout.tsx`)

```tsx
<a
  href="#main-content"
  className="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 focus:z-[9999] focus:px-4 focus:py-2 focus:bg-ink-900 focus:text-paper-50 focus:font-ui focus:text-sm focus:rounded focus:shadow-lg focus:outline-none focus:ring-2 focus:ring-dispatch-ember"
>
  Skip to content
</a>
```

**Every page template must include `<main id="main-content">`** — otherwise the skip link is non-functional. This is verified by axe-core scans in `e2e/a11y.spec.ts`.

### Focus-Visible Rings (`globals.css`)

```css
:focus-visible {
  outline: 2px solid var(--color-dispatch-ember);
  outline-offset: 2px;
  border-radius: 2px;
}
```

**Why `:focus-visible` (not `:focus`):** `:focus-visible` only triggers for keyboard navigation, not mouse clicks. Mouse users see clean UI; keyboard users see clear focus indicators. This is the WCAG-recommended approach.

### Component-Level Focus Rings (ArticleCard example)

```tsx
<Link
  href={`/article/${article.id}`}
  className="after:absolute after:inset-0 focus:outline-none focus-visible:ring-2 focus-visible:ring-dispatch-ember focus-visible:ring-offset-2 focus-visible:ring-offset-paper-50 rounded-sm"
>
```

**`focus:outline-none` + `focus-visible:ring-2`:** Remove the default outline, replace with a Tailwind ring only on keyboard focus. The `ring-offset-paper-50` ensures the ring has a visible gap against the page background.

### Reduced Motion (`globals.css`)

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0ms !important;
    transition-duration: 0ms !important;
  }
  .reveal {
    opacity: 1;
    transform: none;
    transition: none;
  }
  .reveal-delay-1,
  .reveal-delay-2,
  .reveal-delay-3,
  .reveal-delay-4 {
    transition-delay: 0ms;
  }
}
```

**WCAG AAA rule:** DISABLE animations entirely (duration: 0ms), do NOT slow them. Slowed animations can cause vestibular disorders.

### ARIA Patterns

| Element                    | Pattern                                                                |
| :------------------------- | :--------------------------------------------------------------------- |
| Decorative dots / dividers | `aria-hidden="true"` (screen readers skip them)                        |
| Icon-only buttons          | `aria-label="..."` (e.g., `<button aria-label="Close"><X /></button>`) |
| AI summary sidebar         | `aria-label="AI-generated summary transparency label"` on `<aside>`    |
| Loading skeletons          | `aria-busy="true"` on the container                                    |
| Live regions               | `aria-live="polite"` for status updates (e.g., "Summary generated")    |
| Status badges              | `role="status"` for non-critical updates                               |

### axe-core Scans (`e2e/a11y.spec.ts`)

4 WCAG AAA scans run against:

- `/` (home page)
- `/search` (search results)
- `/sign-in` (auth page)
- `/auth-error` (error page)

The `color-contrast` rule is filtered out — `dispatch-ember` (#c7513f) and `dispatch-sage` (#6b8f71) are manually verified at 9.5:1 contrast on `paper-50` (#fafaf8), but axe sometimes flags them in the test environment.

---

## 9. Anti-Patterns & Common Bugs

This is the complete catalog of 34 anti-patterns documented across Phases 1–22. Each entry has been validated against actual code. **If you see any of these in a PR, reject the PR.**

### TypeScript Anti-Patterns

| #   | Anti-Pattern                       | Why Forbidden                                                            | Fix                                                                                           |
| :-- | :--------------------------------- | :----------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------- |
| 1   | `any` in TypeScript                | Breaks strict mode + type inference                                      | `unknown` + type guards. ESLint `@typescript-eslint/no-explicit-any` is `error` (not `warn`). |
| 2   | `enum` / `namespace`               | Compile to runtime IIFE/closure; violate `erasableSyntaxOnly`            | String unions (`type Status = "ACTIVE" \| "DRAFT"`) or Drizzle `pgEnum()`.                    |
| 3   | Hand-written enum unions           | Violate Single Source of Truth — schema changes silently break consumers | `export type X = (typeof enum.enumValues)[number]` from `schema.ts` (Phase 17)                |
| 4   | Missing `noUncheckedIndexedAccess` | `arr[i]` returns `T` instead of `T \| undefined`, hiding runtime errors  | Enable in `tsconfig.json` (it IS enabled).                                                    |

### Next.js 16 Anti-Patterns

| #   | Anti-Pattern                                                    | Why Forbidden                                                               | Fix                                                                                     |
| :-- | :-------------------------------------------------------------- | :-------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------- |
| 5   | `experimental.ppr` / `experimental.dynamicIO`                   | Build error / deprecated in Next.js 16                                      | Use top-level `cacheComponents: true` instead.                                          |
| 6   | `experimental.clientSegmentCache`                               | Not in 16.2.9 `ExperimentalConfig` — TS error                               | Do not enable.                                                                          |
| 7   | `cacheComponents` inside `experimental`                         | Silently ignored — every `"use cache"` is dead                              | Top-level only.                                                                         |
| 8   | `cacheLife` profiles inside `experimental`                      | Runtime throws `cacheLife is not a function`                                | Top-level only.                                                                         |
| 9   | Synchronous `params` / `searchParams` / `cookies()`             | Runtime 500 in Next.js 16 App Router                                        | Always `await` (they're `Promise<T>`).                                                  |
| 10  | `await` in page body without `<Suspense>`                       | `blocking-route` build error                                                | Wrap async data in `<Suspense fallback={<Skeleton />}>`.                                |
| 11  | `export const dynamic = "force-dynamic"` with `cacheComponents` | Incompatible — build error                                                  | Use `<Suspense>` + Server Component pattern.                                            |
| 12  | `throw new Error()` in RSC auth                                 | Triggers full-page error boundary. Bad UX.                                  | `redirect('/sign-in')` from `next/navigation`.                                          |
| 13  | `verifySession()` wrapped in try/catch                          | Catches `NEXT_REDIRECT`, silently swallows redirect                         | Remove try/catch — let it throw. API routes use `auth()` directly.                      |
| 14  | Dead code `if (!session)` after `verifySession()`               | `verifySession()` NEVER returns null — it returns or throws                 | Remove the dead check.                                                                  |
| 15  | Layouts that fetch data                                         | Layouts cause re-renders; data fetches belong in Pages                      | Fetch in page-level Server Components.                                                  |
| 16  | `new Date()` in Server Components                               | `next-prerender-current-time` build error                                   | Move to Client Component with `useEffect`.                                              |
| 17  | JSON-LD via `metadata.other`                                    | Next.js 16 only emits `<meta>` tags from `metadata.other`, never `<script>` | Render `<script type="application/ld+json">` directly in page body (Phase 17).          |
| 18  | Route group `(admin)/` expected to produce `/admin/` URLs       | Route groups don't affect URL structure                                     | Add `admin/` subfolder: `(admin)/admin/sources/page.tsx` → `/admin/sources` (Phase 21). |

### Architecture Anti-Patterns

| #   | Anti-Pattern                                                      | Why Forbidden                                                                  | Fix                                                                                                          |
| :-- | :---------------------------------------------------------------- | :----------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------- |
| 19  | Runtime imports from `@/lib/db*` in `src/domain/**`               | Creates runtime coupling to DB; domain must be pure + unit-testable            | `import type` only. Enforced by ESLint `no-restricted-imports` with `allowTypeImports: true` (Phase 20).     |
| 20  | Raw Drizzle calls in components                                   | Bypasses the `queries.ts` boundary; hard to test                               | All DB access via feature-level `queries.ts`.                                                                |
| 21  | `drizzle-kit push` in production                                  | Overwrites schema without migration history — irreversible                     | `generate` + `migrate` only.                                                                                 |
| 22  | Custom components over Shadcn/Radix                               | Violates Library Discipline; wastes engineering time                           | Wrap the library primitive for bespoke styling.                                                              |
| 23  | Server Actions without `verifySession()` / `verifyAdminSession()` | Server Actions bypass layout guards — unauthenticated clients can trigger them | Every Server Action's first line must be auth.                                                               |
| 24  | Server Actions tested but not wired to UI                         | Dead code from user's perspective — TDD on action alone is insufficient        | Add a UI integration test that renders the consuming component and asserts the form binding (Phase 22 / N5). |
| 25  | Inert `<button type="button">` for server actions                 | No `onClick` / `form action` — button does nothing                             | `<form action={...}><button type="submit">` (Phase 19 / C5).                                                 |
| 26  | AdminGuard per-page (not at layout boundary)                      | New admin pages that forget the guard are publicly accessible                  | `<AdminGuard>` in `(admin)/layout.tsx` (Phase 16).                                                           |

### Security Anti-Patterns

| #   | Anti-Pattern                                            | Why Forbidden                                                        | Fix                                                                                                                                   |
| :-- | :------------------------------------------------------ | :------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------ |
| 27  | `process.env.*` outside `src/lib/env/`                  | Bypasses Zod schema — typos silently return `undefined`              | Import `env` from `@/lib/env` and access `env.VAR_NAME`.                                                                              |
| 28  | `.env*` files committed to git                          | Real secrets (VAPID keys, API keys) in git history forever           | `.env`, `.env.*`, `!.env.example` in `.gitignore`. Rotate exposed secrets. (Phase 21)                                                 |
| 29  | `AUTH_SECRET` accepts known-weak values                 | Publicly known dev secrets allow JWT session forgery                 | `superRefine` rejecting weak patterns (`dev-secret`, `test-secret`, `ci-dummy`, `change-me`, `placeholder`) in production (Phase 21). |
| 30  | AES-256-GCM IV of 16 bytes                              | Non-NIST-compliant — requires additional GHASH computation           | Use 12-byte IV per NIST SP 800-38D (Phase 21).                                                                                        |
| 31  | Rate limiter fails-closed (500) on Redis outage         | Monitoring outage takes down the API                                 | Wrap in try/catch, fail OPEN (200 + warning) (Phase 21 + Phase 22 / N1).                                                              |
| 32  | Asymmetric rate-limiter protection across routes        | One route fails-open, another fails-closed — inconsistent resilience | When applying fail-open to one route, audit ALL rate-limited routes (Phase 22 / N1).                                                  |
| 33  | CSP with `'unsafe-eval'`                                | Allows `eval()` / `new Function()` — XSS enabler                     | Remove `'unsafe-eval'`. Run `grep -rn "eval(\|new Function(" src/` to verify no usage (Phase 22 / H1).                                |
| 34  | Comment claims directive removed but value never edited | Visual review misses it because the comment claims success           | Add a regression test asserting the absence (Phase 22 / H1).                                                                          |

### Testing Anti-Patterns

| #   | Anti-Pattern                                                | Why Forbidden                                                                             | Fix                                                                                                                              |
| :-- | :---------------------------------------------------------- | :---------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------- |
| 35  | `vi.mock()` factory referencing `let`/`const` below it      | `ReferenceError: Cannot access 'mockEnv' before initialization` — Vitest hoists factories | Use `vi.hoisted()` to declare mutable mock objects BEFORE the factory (Phase 19).                                                |
| 36  | `vi.hoisted()` factory referencing module-top `const`       | Same TDZ issue — `vi.hoisted()` runs first                                                | Inline literal values directly into the factory body (Phase 20).                                                                 |
| 37  | `vi.clearAllMocks()` on structural mock chains              | Breaks the `db.select().from().where()` chain — `db.select()` returns `undefined`         | Set up structural chains ONCE in `vi.mock()` factory; per-test overrides via `mockResolvedValueOnce()` on leaf mocks (Phase 20). |
| 38  | `cacheLife()` in tests without `next/cache` mock            | `TypeError: cacheLife is not a function` — test env has no Next.js cache context          | `vi.mock("next/cache", () => ({ cacheLife: vi.fn() }))` (Phase 19).                                                              |
| 39  | Missing `SessionProvider` in tests using `useSession()`     | Throws "useSession must be wrapped in a <SessionProvider>"                                | Mock `next-auth/react` with passthrough `SessionProvider` (Phase 19).                                                            |
| 40  | `window.matchMedia()` without `typeof === "function"` guard | Crashes in jsdom (vitest) + older browsers                                                | `typeof window !== "undefined" && typeof window.matchMedia === "function" && window.matchMedia(...).matches` (Phase 20).         |
| 41  | Security module relying solely on upstream Zod validation   | When `@/lib/env` is mocked, Zod is bypassed — confusing error messages                    | Belt-and-suspenders: security-critical modules validate their own inputs (Phase 20).                                             |

### CSS / Tailwind Anti-Patterns

| #   | Anti-Pattern                                                | Why Forbidden                                         | Fix                                                                         |
| :-- | :---------------------------------------------------------- | :---------------------------------------------------- | :-------------------------------------------------------------------------- |
| 42  | Missing `@tailwindcss/postcss` plugin                       | Zero utility classes generate — page loads unstyled   | Install + create `postcss.config.mjs` + `rm -rf .next/` (Phase 12).         |
| 43  | Raw hex colors in Tailwind (`bg-[#1a1a2e]`)                 | Bypasses design token system                          | Use tokens: `bg-ink-900`, `text-paper-50`, `text-dispatch-ember`.           |
| 44  | Generic fonts (Inter, Roboto, Space Grotesk, Fira Code)     | Violates Editorial Dispatch anti-generic mandate      | Newsreader, Instrument Sans, Commit Mono only.                              |
| 45  | `@fontsource/commit-mono`                                   | Broken in Phase 12 — font doesn't load                | Self-host via `next/font/local` with woff2 in `public/fonts/`.              |
| 46  | Tailwind v4 merge artifacts in `@theme` (e.g., ` INCLUDED`) | Corrupts the `@theme` block — all custom colors break | Review CSS diffs after merges; run `pnpm build` before pushing.             |
| 47  | Default `amber-*` / `red-*` for warnings/danger             | Breaks design system                                  | `dispatch-warning` (#b45309), `dispatch-danger` (#dc2626) — Phase 19 / M15. |

### Worker / Queue Anti-Patterns

| #   | Anti-Pattern                                  | Why Forbidden                                                                                                        | Fix                                                                                               |
| :-- | :-------------------------------------------- | :------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------ |
| 48  | `flowProducer.add()` without try/catch        | Redis failure → BullMQ retries → articles already persisted (`xmax != 0`) → empty `newArticleIds` → silent data loss | Wrap in try/catch; on failure fall back to direct `scoreQueue.add()` per article (Phase 19 / C4). |
| 49  | FNV-1a hash for `contentHash`                 | 8-char hash not collision-resistant; doesn't match SHA-256 spec                                                      | `node:crypto` `createHash("sha256")` returning 64-char hex (Phase 13).                            |
| 50  | Regex HTML stripping (`/<[^>]*>/g`)           | Strips tags but not text content — `<script>alert('evil')</script>` leaks into AI prompts                            | Use `cheerio` (Phase 19 / H9).                                                                    |
| 51  | Summarising `title_only` / `excerpt` articles | AI hallucination — fabricating content from insufficient input                                                       | Content availability guard at BOTH action and route layers (Phase 5).                             |

### Repo Hygiene Anti-Patterns

| #   | Anti-Pattern                                                       | Why Forbidden                                                                                                                               | Fix                                                                                                                                      |
| :-- | :----------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------ | :--------------------------------------------------------------------------------------------------------------------------------------- |
| 52  | Vendored `skills/` not excluded from tsc/eslint                    | 64 tsc errors + 43 lint warnings from skills' own deps make `pnpm check` red                                                                | Add `"skills"` to `tsconfig.json` `exclude`; `"skills/**"` to eslint ignores (Phase 19).                                                 |
| 53  | Tarball remediation archives in repo root                          | 119MB of bloat; confuses with live source tree                                                                                              | Add `*.tar.gz`, `*.tar.bz2`, `*.tgz` to `.gitignore` (Phase 22 / N2).                                                                    |
| 54  | No `.prettierignore` — `format:check` scans 226+ markdown files    | False-positive CI failures on vendored/historical docs                                                                                      | Create `.prettierignore` excluding `skills/`, `docs/`, `*.archived`, lockfiles, binary assets (Phase 22 / N6).                           |
| 55  | `pnpm audit \|\| true` never promoted to hard gate                 | "Non-blocking initially" without scheduled promotion is compounding debt                                                                    | After mitigation, immediately verify gate can be promoted; remove `\|\| true` (Phase 22 / F4).                                           |
| 56  | `metadata.other` used for HTTP headers (Phase 23 / BUG-2)          | Next.js 16 `metadata.other` ONLY emits `<meta>` tags, NEVER HTTP headers. Setting `"X-AI-Provenance"` creates a `<meta>` tag, not a header. | Use `next.config.ts` `headers()` function for HTTP headers. Use `metadata.other` only for `<meta>` tags.                                 |
| 57  | `pnpm.overrides` in `package.json` (pnpm 9.15+) (Phase 23 / BUG-3) | pnpm 9.15+ no longer reads the `pnpm` field — overrides silently ignored, CVEs remain unmitigated.                                          | Move overrides to `pnpm-workspace.yaml` with `packages: []` + `overrides:` block. Delete `pnpm-lock.yaml` + `node_modules/` + reinstall. |
| 58  | Missing `data-scroll-behavior` on `<html>` (Phase 23 / F5)         | Next.js 16 view transitions warn: "Detected `scroll-behavior: smooth`". Transitions may interfere with smooth scroll.                       | Add `data-scroll-behavior="smooth"` to `<html>` in `layout.tsx`.                                                                         |

### Phase 25 Anti-Patterns (Security & Correctness)

| #   | Anti-Pattern                                                               | Why Forbidden                                                                                                                                                                    | Fix                                                                                                                                                                                                           |
| :-- | :------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 59  | `JSON.stringify` output in `dangerouslySetInnerHTML` without HTML escaping | `JSON.stringify` does NOT escape `<`, `>`, `&`, U+2028, U+2029. Embedding in `<script type="application/ld+json">` allows `</script>` injection from untrusted RSS titles (XSS). | `escapeForScriptContext()` after `JSON.stringify` — escapes as JSON-compatible `\u003c`, `\u003e`, `\u0026`, `\u2028`, `\u2029`. `JSON.parse()` reverses them automatically (Phase 25 / F2).                  |
| 60  | Application-level uniqueness check + post-hoc filter (race condition)      | Querying by a subset of the uniqueness key + post-hoc `if (existing.userId === user.id)` check is racy — two concurrent calls can both pass the check.                           | Query by the FULL tuple `and(eq(a, x), eq(b, y))` AND enforce uniqueness at the DB level with a unique index. The post-hoc check is a code smell (Phase 25 / F3).                                             |
| 61  | Composite `ORDER BY` with single-column cursor                             | `ORDER BY (rank, publishedAt)` with cursor `publishedAt < cursor` skips/duplicates rows when multiple rows share the same rank.                                                  | Add a deterministic tiebreaker (e.g., UUID `id`) to ORDER BY + composite cursor `(publishedAt, id) < (cursor.publishedAt, cursor.id)`. Design cursors as opaque tokens (Phase 25 / F6).                       |
| 62  | Dead code surviving refactors                                              | When refactoring a function out of use, the function itself often survives because tests keep it "alive" from a coverage perspective.                                            | Always `grep` for ALL consumers before considering a refactor complete. Delete immediately or add a regression test asserting the absence (Phase 25 / F4).                                                    |
| 63  | `.gitignore` rules added but `git rm --cached` never run                   | `.gitignore` only prevents FUTURE files from being tracked — it does NOT untrack files already in the index. Secrets remain in history.                                          | After adding `.gitignore` rules for sensitive files, run `git ls-files \| grep <pattern>` to verify, and `git rm --cached <file>` for any matches. Add `scripts/check-env-leaks.sh` CI guard (Phase 25 / F1). |
| 64  | `as any` casts on library generic types                                    | `eslint-disable` comments are an admitted violation of `no-explicit-any`. Library union generics (pg/mysql/sqlite) prevent direct type-safe casts.                               | Wrap the library call in a helper function that pins the generic to the specific variant: `Parameters<typeof LibraryFn<SpecificType>>` (Phase 25 / F5 — `createPgAdapter()`).                                 |

---

## 10. Debugging Guide

### Common Symptoms → Causes → Fixes

| Symptom                                                         | Cause                                                                                     | Fix                                                                                                                            |
| :-------------------------------------------------------------- | :---------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------- |
| Page completely unstyled                                        | Missing `@tailwindcss/postcss` plugin                                                     | Install plugin + create `postcss.config.mjs` + `rm -rf .next/`                                                                 |
| `blocking-route` error                                          | Uncached data fetch outside `<Suspense>`                                                  | Wrap in `<Suspense fallback={<Skeleton />}>`                                                                                   |
| `next-prerender-current-time`                                   | `new Date()` in Server Component                                                          | Move to Client Component with `useEffect`                                                                                      |
| Commit Mono not loading                                         | Using `@fontsource/commit-mono`                                                           | Self-host via `next/font/local` with woff2                                                                                     |
| 64 tsc errors in `skills/`                                      | Vendored code not excluded                                                                | Add `"skills"` to `tsconfig.json` `exclude`                                                                                    |
| `cacheLife is not a function` in tests                          | No Next.js cache context                                                                  | `vi.mock("next/cache", () => ({ cacheLife: vi.fn() }))`                                                                        |
| `useSession` requires `SessionProvider`                         | Test doesn't go through layout                                                            | Mock `next-auth/react`                                                                                                         |
| Rate limit 429 behind CDN                                       | Leftmost XFF IP spoofable                                                                 | Set `TRUSTED_PROXY=true` + `TRUSTED_PROXY_CIDRS`                                                                               |
| Admin sidebar links 404                                         | Route group `(admin)/` doesn't affect URLs                                                | Add `admin/` subfolder: `(admin)/admin/sources/` (Phase 21)                                                                    |
| `revalidatePath("/admin/sources")` no-op                        | Same route group issue                                                                    | Fixed by Phase 21 admin folder restructure                                                                                     |
| API returns 500 instead of 401 (auth)                           | `verifySession()` redirect caught by try/catch                                            | Use `auth()` directly in API routes; remove try/catch (Phase 21)                                                               |
| Redis outage takes down `/api/articles`                         | Rate limiter throws uncaught                                                              | Fail-open try/catch around `checkRateLimit()` (Phase 21 S7)                                                                    |
| Redis outage takes down `/api/summarize/[id]`                   | Same as above but asymmetric                                                              | Same fail-open try/catch (Phase 22 / N1)                                                                                       |
| `pnpm build` fails: weak AUTH_SECRET                            | Production rejects placeholder values                                                     | Generate strong secret: `openssl rand -base64 33` (Phase 21)                                                                   |
| `.env.local` with real keys in git history                      | `.gitignore` didn't exclude `.env*`                                                       | Untrack + rotate exposed secrets (Phase 21)                                                                                    |
| CSP `'unsafe-eval'` "removed" but still present                 | Comment claimed removal but value never edited                                            | Actually remove it + add `next.config.test.ts` regression guard (Phase 22 / H1)                                                |
| Admin sources page has no Pause button                          | `pauseSource` action existed but no UI consumed it                                        | Wire `<form action={pauseSourceAction}>` (Phase 22 / N5)                                                                       |
| `pnpm format:check` fails on 226+ markdown files                | No `.prettierignore`                                                                      | Create `.prettierignore` (Phase 22 / N6)                                                                                       |
| `pnpm audit` now fails CI                                       | Hard gate promoted (Phase 22 / F4)                                                        | Apply `pnpm.overrides` or upgrade; if no fix, temporarily re-add `\|\| true` with TODO                                         |
| Hydration mismatch (date rendering)                             | `new Date()` in Server Component                                                          | Use Client Component wrapper or pass pre-formatted strings                                                                     |
| Saved HTML snapshots misleading                                 | Stale snapshots during active dev                                                         | Always `curl` the live server for current state                                                                                |
| External images fail to load                                    | Missing `remotePatterns` in `next.config.ts`                                              | Add `{ protocol: "https", hostname: "picsum.photos", pathname: "/**" }`                                                        |
| `pnpm test` fails with "Environment variable validation failed" | CI env vars not set                                                                       | Set all 10 required vars in `ci.yml` `env:` block                                                                              |
| `searchArticles()` returns empty                                | `websearch_to_tsquery` parses differently                                                 | Check `searchVector` weights; ensure `pg_trgm` extension enabled                                                               |
| `</script>` appearing in rendered JSON-LD `<script>`            | `JSON.stringify` doesn't escape HTML delimiters; untrusted RSS title contains `</script>` | `escapeForScriptContext()` in `provenance.ts` escapes `<>&` + U+2028/2029 (Phase 25 / F2)                                      |
| Duplicate "pending" rows in `accounts` table                    | `linkOAuthProvider` race condition: query by `provider` only + post-hoc `userId` check    | Query by `(userId, provider)` tuple + DB unique index `accounts_user_provider_idx` (Phase 25 / F3)                             |
| Search results skip/duplicate across pages                      | Composite `ORDER BY (rank, publishedAt)` with single-column cursor                        | Add `id` tiebreaker to ORDER BY + compound cursor `publishedAt\|articleId` (Phase 25 / F6)                                     |
| CI fails with "Real .env files are tracked by git"              | `.env*` file accidentally `git add`ed despite `.gitignore`                                | `git rm --cached <file>` + verify `bash scripts/check-env-leaks.sh` passes (Phase 25 / F1)                                     |
| `tsc` error: `as any` on DrizzleAdapter tables                  | Adapter's union generic (pg/mysql/sqlite) prevents direct type-safe cast                  | Use `createPgAdapter()` wrapper specializing generic to `PgDatabase<PgQueryResultHKT>` (Phase 25 / F5)                         |
| Migration `0007` fails: "could not create unique index"         | Duplicate `(userId, provider)` rows exist from pre-F3 race condition                      | Run cleanup query in migration file first (deletes "pending-" placeholder rows), then re-run `pnpm db:migrate` (Phase 25 / F3) |
| `JSON.parse(result.httpHeader)` throws                          | `httpHeader` field was removed in Phase 25 / F4 (dead code)                               | Remove the test — the field no longer exists. Layer 2 is now a static header in `next.config.ts` (Phase 25 / F4)               |

### Debugging Workflow

1. **Read the error message** — Next.js error messages are descriptive. `blocking-route` means uncached data; `next-prerender-current-time` means `new Date()` in RSC.
2. **Check `git blame`** — If a line looks wrong, `git blame -L <line>` shows when it was last touched. The H1 finding was caught this way (line 115 was touched in Phase 13, not Phase 21 as the comment claimed).
3. **Check the anti-patterns catalog** — Most bugs map to a documented anti-pattern. Search this file first.
4. **Run `pnpm check && pnpm test`** — Verify the baseline is green before investigating.
5. **Add a failing test** — If you can't reproduce the bug in a test, you don't understand it yet. TDD: RED first.
6. **Check Phase docs** — `AGENTS.md` has detailed gotchas per phase. Search for the symptom.

---

## 11. Pre-Ship Checklist

Before claiming any task is complete, verify ALL of these:

### Code Quality

```bash
# 1. TypeScript strict + ESLint
pnpm check
# Expected: 0 errors, 0 warnings

# 2. All tests pass
pnpm test
# Expected: 525 tests / 69 suites pass

# 3. Coverage above thresholds (80/70/80/80)
pnpm test -- --coverage
# Expected: statements ≥80%, branches ≥70%, functions ≥80%, lines ≥80%

# 4. Prettier formatting
pnpm run format:check
# Expected: "All matched files use Prettier code style!"

# 5. Security audit (HARD GATE as of Phase 22 / F4)
pnpm audit --audit-level=high --prod
# Expected: exit 0 (1 moderate vuln is acceptable; 0 high/critical required)

# 6. Env leak guard (Phase 25 / F1)
bash scripts/check-env-leaks.sh
# Expected: "✅ No .env leaks detected. Only .env.example is tracked."

# 7. Database migrations applied (Phase 25 / F3)
pnpm db:migrate
# Expected: All migrations applied (including 0007_accounts_user_provider_unique.sql)
```

### Manual Verification

- [ ] All UI states handled: loading, error, empty, success
- [ ] Every list has an empty state
- [ ] Loading state shows ONLY when no data exists (not on every refetch)
- [ ] Buttons disabled during async operations
- [ ] Loading indicator on async buttons
- [ ] `onError` handler with user feedback
- [ ] Skip-to-content link works (Tab from URL bar)
- [ ] Focus rings visible on all interactive elements
- [ ] `prefers-reduced-motion` honored
- [ ] ARIA labels on icon-only buttons
- [ ] `<main id="main-content">` on every page template
- [ ] No raw hex colors in components (design tokens only)
- [ ] No `eval()` / `new Function()` / `dangerouslySetInnerHTML` (except JSON-LD which is sanitized)

### Architecture

- [ ] No DB calls in `proxy.ts`
- [ ] No data fetching in layouts
- [ ] All async data inside `<Suspense>` or `"use cache"`
- [ ] Server Actions start with `verifySession()` / `verifyAdminSession()`
- [ ] API routes use `auth()` (not `verifySession()`)
- [ ] `verifySession()` NOT wrapped in try/catch
- [ ] All DB access via feature-level `queries.ts`
- [ ] Domain layer has no runtime imports from `@/lib/db*`
- [ ] All env vars accessed via `env` export (not `process.env.*`)
- [ ] Rate-limited routes have fail-open try/catch

### Security

- [ ] `.env*` files NOT committed (only `.env.example`) — verify with `bash scripts/check-env-leaks.sh`
- [ ] `AUTH_SECRET` is a strong random value (≥32 chars, not in weak-patterns list)
- [ ] VAPID keys rotated if previously committed (Phase 25 / F1 — see `SECURITY_REMEDIATION.md`)
- [ ] CSP does NOT contain `'unsafe-eval'` (regression test in `next.config.test.ts`)
- [ ] AES-256-GCM IV is 12 bytes (NIST SP 800-38D)
- [ ] Content availability guard enforced at BOTH action and route layers
- [ ] Per-user rate limiting on AI-cost endpoints (`/api/summarize`, `requestSummary`)
- [ ] JSON-LD output escaped via `escapeForScriptContext()` when rendered via `dangerouslySetInnerHTML` (Phase 25 / F2)
- [ ] OAuth account-linking uses `(userId, provider)` tuple query + DB unique index (Phase 25 / F3)
- [ ] Search cursor uses compound format with deterministic tiebreaker (Phase 25 / F6)
- [ ] No `as any` / `eslint-disable` comments in auth adapter (Phase 25 / F5 — `createPgAdapter()`)
- [ ] No dead code from prior refactors (grep for all consumers before deleting — Phase 25 / F4)

### Documentation

- [ ] JSDoc on all exported functions/components
- [ ] Comments explain WHY, not WHAT
- [ ] `AGENTS.md` updated if new gotcha discovered
- [ ] `MASTER_EXECUTION_PLAN.md` updated if new phase
- [ ] Anti-patterns catalog updated if new pattern identified

---

## 12. Lessons Learnt & How to Avoid Them

### Top 10 Most Critical Lessons (Across 22 Phases)

#### 1. Claims in Comments Are NOT Verification (Phase 22 / H1)

Phase 21 S4 comment said "'unsafe-eval' was removed" but the actual CSP value still contained it. The regression survived 2 phases because no test verified the claim.

**How to avoid:** When a comment says "X was removed/added/fixed", grep for X immediately. Add a regression test that asserts the desired state. Comments are documentation, not verification.

#### 2. Audit ALL Similar Call Sites When Applying a Pattern (Phase 22 / N1)

Phase 21 S7 added fail-open to `/api/articles` but missed `/api/summarize/[id]` — same pattern, different route, asymmetric protection.

**How to avoid:** When applying a resilience pattern (fail-open, retry, circuit-breaker) to one call site, grep for all similar call sites. Add tests that assert the same pattern across all of them.

#### 3. Server Actions Are Dead Code Without UI Wiring (Phase 22 / N5)

`pauseSource` action existed, was tested, but no UI called it. TDD on the action alone was insufficient.

**How to avoid:** Add a UI integration test that renders the consuming component and asserts the form binding. Server Actions are RPCs — they need a client to call them.

#### 4. `verifySession()` Throws, Never Returns Null (Phase 21 / S3)

`redirect()` throws `NEXT_REDIRECT`. Standard try/catch catches it, silently swallowing the redirect. Server Actions returned JSON errors instead of redirecting; API routes returned 500 instead of 401.

**How to avoid:** Never wrap `verifySession()` / `verifyAdminSession()` in try/catch. API routes use `auth()` directly (returns null → 401 JSON). The `if (!session)` check after `verifySession()` is dead code.

#### 5. Next.js 16 `cacheComponents` Requires Suspense (Phase 9)

`cacheComponents: true` makes caching opt-in. ALL async data fetching outside `<Suspense>` or `"use cache"` triggers a `blocking-route` build error.

**How to avoid:** Page shells are synchronous. Async data fetching lives in Server Components wrapped in `<Suspense fallback={<Skeleton />}>`.

#### 6. `vi.hoisted()` Factories Run First (Phase 20)

`vi.hoisted()` factories are hoisted to the very top of the file and run BEFORE any other top-level declarations. Referencing a module-top `const` throws a TDZ `ReferenceError`.

**How to avoid:** Inline literal values directly into the `vi.hoisted()` factory body. If reused, declare a separate `const` AFTER the `vi.hoisted()` call.

#### 7. Security Modules Need Belt-and-Suspenders Validation (Phase 20)

`encrypt.ts` relied solely on the Zod env schema. When `@/lib/env` was mocked in tests, Zod was bypassed — `Buffer.from(undefined, "hex")` threw a confusing error.

**How to avoid:** Security-critical modules (encryption, auth, rate limiting) validate their own inputs even when an upstream layer exists. The redundancy catches mock-bypass in tests and protects against future code paths.

#### 8. FlowProducer Must Never Re-Throw (Phase 19 / C4)

`flowProducer.add()` failure → BullMQ retries → articles already persisted (`xmax != 0`) → empty `newArticleIds` → silent data loss.

**How to avoid:** Wrap `flowProducer.add()` in try/catch. On failure, fall back to direct `scoreQueue.add()` per article. Return a status object `{ status: "ok" | "degraded", ... }` — never re-throw.

#### 9. JSON-LD Must Be in the Body, Not `metadata.other` (Phase 17)

Next.js 16 `metadata.other` only emits `<meta>` tags, never `<script>` tags. JSON-LD via `metadata.other` was silently dropped.

**How to avoid:** Render `<script type="application/ld+json" dangerouslySetInnerHTML={{ __html: jsonLdString }} />` directly in the page body. The `key` prop deduplicates across renders.

#### 10. Cheerio Over Regex for HTML Stripping (Phase 19 / H9)

Regex `/<[^>]*>/g` strips tags but not text content. `<script>alert('evil')</script>` leaked "alert('evil')" into AI summaries.

**How to avoid:** Always use `cheerio` for HTML parsing. The regex approach misses numeric character references, CDATA sections, and `<script>`/`<style>` content.

#### 11. `.gitignore` Doesn't Untrack Already-Tracked Files (Phase 25 / F1)

Phase 21 added `.gitignore` rules for `.env*` files, but three real env files (`.env`, `.env.local`, `.env.docker`) remained tracked in git — including a real 64-hex `AUTH_SECRET` and real VAPID keypair. The `.gitignore` rules only prevent FUTURE files from being tracked; they do NOT untrack files already in the index.

**How to avoid:** After adding `.gitignore` rules for sensitive files, ALWAYS run `git ls-files | grep <pattern>` to verify no tracked files match. Run `git rm --cached <file>` for any that do. Add a CI guard (`scripts/check-env-leaks.sh`) that fails if any `.env*` file (except `.env.example`) is tracked. Rotate ALL exposed secrets — git history is forever.

#### 12. `JSON.stringify` Is NOT Safe for `<script>` Contexts (Phase 25 / F2)

The JSON-LD provenance was rendered via `dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}`. `JSON.stringify` does NOT escape `<`, `>`, `&`, U+2028, or U+2029. A malicious RSS feed with `title="</script><script>alert(1)</script>"` would break out of the script tag and execute arbitrary JavaScript (XSS). The HTML parser operates BEFORE JavaScript parsing — `</script>` terminates the script tag regardless of being inside a JSON string.

**How to avoid:** When embedding JSON in a `<script>` tag via `dangerouslySetInnerHTML`, ALWAYS escape HTML delimiters after `JSON.stringify`. Use `escapeForScriptContext()` which escapes `<`, `>`, `&` as `\u003c`, `\u003e`, `\u0026` and U+2028/U+2029. These are JSON-compatible escapes — `JSON.parse()` reverses them automatically. See OWASP XSS Prevention Cheat Sheet §Rule 3.1.

#### 13. Application-Level Uniqueness Checks Are Racy (Phase 25 / F3)

`linkOAuthProvider` queried `findFirst({ where: eq(provider, x) })` then did a post-hoc `if (existing.userId === user.id)` check. Two concurrent calls by the same user could both pass the `existing === undefined` check before either insert ran, producing duplicate "pending" account rows.

**How to avoid:** Always enforce uniqueness at the DB level with a unique index. Query by the FULL tuple `and(eq(a, x), eq(b, y))` — don't query by a subset + post-hoc filter. The post-hoc check is a code smell: if you find yourself checking a field after a query, ask why the query didn't filter on it in the first place. Add a DB migration creating the unique index as defense-in-depth.

#### 14. Dead Code Survives Refactors When Tests Keep It "Alive" (Phase 25 / F4)

Phase 23 / BUG-2 moved the `X-AI-Provenance` header from dynamic `metadata.other` to a static value in `next.config.ts`. The fix removed the caller (`page.tsx`) but not the `generateHttpHeader()` function itself. The function survived 2 phases as dead code because the test file kept calling `result.httpHeader` — from a coverage perspective, it looked "used."

**How to avoid:** When refactoring a function out of use, always `grep` for ALL consumers (including test files) before considering the refactor complete. Delete the function immediately, OR add a regression test asserting the absence (a test that verifies the function/export does NOT exist). Add a `// DEAD CODE — safe to remove?` comment to surface it in code review if you're unsure.

#### 15. Library Union Generics Prevent Direct Type-Safe Casts (Phase 25 / F5)

`DrizzleAdapter<SqlFlavor extends SqlFlavorOptions>` is generic over a union of pg/mysql/sqlite flavors. Even though `authDb` is a `PgDatabase` at runtime, `Parameters<typeof DrizzleAdapter>[1]` extracts the parameter type WITHOUT the generic bound — it resolves to the union of all 3 schema types. Per-table `as unknown as UnionType` casts fail because the union includes MySQL/SQLite table types that aren't assignable to the postgres-specific parameter.

**How to avoid:** Wrap the library call in a helper function that explicitly specializes the generic to the specific variant: `function createPgAdapter(db: unknown, config: ...): ReturnType<typeof DrizzleAdapter> { return DrizzleAdapter(db as PgDatabase<PgQueryResultHKT>, config as unknown as Parameters<typeof DrizzleAdapter<PgDatabase<PgQueryResultHKT>>>[1]); }`. This centralizes the escape hatch, eliminates per-field `as any` casts, and self-documents the type-system limitation.

#### 16. Composite ORDER BY Requires a Composite Cursor (Phase 25 / F6)

`searchArticles` used `ORDER BY (rank DESC, publishedAt DESC)` with a single-column cursor `publishedAt < cursor`. When multiple rows shared the same `rank` (common for short queries), the cursor would skip/duplicate rows across pages — articles with the same rank but a later `publishedAt` would be incorrectly included or excluded.

**How to avoid:** If the sort key isn't unique, add a deterministic tiebreaker (like a UUID primary key) to ORDER BY and include it in the cursor. Use a compound cursor format like `"publishedAt|articleId"` with composite filter `(publishedAt < cursor.publishedAt) OR (publishedAt = cursor.publishedAt AND id < cursor.articleId)`. Design cursors as opaque tokens encoding the full sort key. When changing cursor format, provide a backward-compat path for existing clients.

---

## 13. Pitfalls to Avoid

### Next.js 16-Specific Pitfalls

1. **Don't enable `experimental.ppr`** — it's a build error in Next.js 16. `cacheComponents: true` implements PPR as default.
2. **Don't enable `experimental.dynamicIO`** — deprecated/removed.
3. **Don't enable `experimental.clientSegmentCache`** — not in 16.2.9 `ExperimentalConfig`, causes TS error.
4. **Don't put `cacheComponents` or `cacheLife` inside `experimental`** — they must be top-level.
5. **Don't access `params` / `searchParams` / `cookies()` synchronously** — they're `Promise<T>` in Next.js 16.
6. **Don't use `export const dynamic = "force-dynamic"`** with `cacheComponents: true` — incompatible.
7. **Don't fetch data in layouts** — layouts re-render; fetch in pages.
8. **Don't render JSON-LD via `metadata.other`** — use a `<script>` tag in the body.

### TypeScript Pitfalls

1. **Don't use `enum` or `namespace`** — `erasableSyntaxOnly` forbids them.
2. **Don't use `any`** — use `unknown` + type guards. ESLint `no-explicit-any` is `error`.
3. **Don't disable `noUncheckedIndexedAccess`** — it catches runtime `undefined` access.
4. **Don't write explicit return types** unless on public API boundaries — prefer inference.
5. **Don't use `import { Type }`** — use `import type { Type }` (required by `verbatimModuleSyntax`).

### Testing Pitfalls

1. **Don't use `vi.fn(() => mockInstance)` for constructors** — use real `class` in mock factory.
2. **Don't `vi.clearAllMocks()` on structural mock chains** — only reset leaf mocks via `mockResolvedValueOnce()`.
3. **Don't reference `let`/`const` below `vi.mock()` factory** — use `vi.hoisted()`.
4. **Don't reference module-top `const` in `vi.hoisted()` factory** — inline literals.
5. **Don't use `??=` for test env vars** — use direct `=` assignment in `src/test/setup.ts`.
6. **Don't forget to mock `next/cache`** when testing modules that call `cacheLife()`.
7. **Don't use integration tests with `vi.mock()`** — let real modules load against testcontainers.

### Drizzle / Database Pitfalls

1. **Don't use `drizzle-kit push` in production** — `generate` + `migrate` only.
2. **Don't write raw SQL string concatenation** — use Drizzle parameterized queries.
3. **Don't forget `onDelete: "cascade"`** on foreign keys if you want cascade deletes.
4. **Don't use lazy proxy for DrizzleAdapter** — use eager instance (`db/auth.ts`).
5. **Don't forget to add new env vars to CI** — `src/lib/env/index.ts` validates at module load.

### BullMQ / Worker Pitfalls

1. **Don't re-throw from `flowProducer.add()`** — wrap in try/catch + fallback.
2. **Don't use `new Redis()` per call** — module-level singleton.
3. **Don't set `maxRetriesPerRequest: null` on Queue producer** — only on Worker connection.
4. **Don't forget graceful shutdown** — `SIGTERM`/`SIGINT` handlers + `Promise.allSettled`.
5. **Don't summarize `title_only` / `excerpt` articles** — content availability guard.

### Security & Type-Safety Pitfalls (Phase 25)

1. **Don't assume `.gitignore` untracks already-tracked files** — always run `git rm --cached` after adding rules for sensitive files. Verify with `git ls-files | grep <pattern>`.
2. **Don't embed `JSON.stringify` output in `<script>` via `dangerouslySetInnerHTML` without escaping** — `</script>` terminates the script tag. Use `escapeForScriptContext()`.
3. **Don't rely on application-level uniqueness checks** — they're racy. Always add a DB unique index as defense-in-depth.
4. **Don't use `as any` on library generic types** — wrap in a helper function that pins the generic. `eslint-disable` comments are technical debt.
5. **Don't use single-column cursors with composite ORDER BY** — add a deterministic tiebreaker (UUID `id`) to both ORDER BY and the cursor.
6. **Don't leave dead code after refactors** — grep for ALL consumers (including tests) before considering a refactor complete.
7. **Don't forget to rotate secrets after a leak** — `git filter-repo` purges history, but rotation is the actual mitigation. See `SECURITY_REMEDIATION.md`.

---

## 14. Best Practices

### Code Organization

- **Feature-folder structure:** `src/features/{feed,articles,summaries,search,sources}/` — each has `queries.ts`, `actions.ts`, `components/`, `lib/`, `types.ts`
- **Domain layer is pure:** `src/domain/{articles,ranking}/` — no runtime DB imports (enforced by ESLint)
- **Infrastructure is isolated:** `src/lib/{db,auth,queue,env,security,network,ai,rateLimit}/`
- **Shared UI:** `src/shared/{components,hooks,lib}/` — primitives used across features
- **App Router:** `src/app/{(public),(admin),api,account,article,auth-error,sign-in}/`

### Naming Conventions

- **Components:** PascalCase (`ArticleCard.tsx`)
- **Utilities/hooks:** camelCase (`useDebounce.ts`, `formatTimeAgo`)
- **Feature folders:** kebab-case (`/features/feed/`)
- **Database tables:** snake_case in Drizzle (`pgTable("articles", ...)`), camelCase in TS (`articles`)
- **Files:** match the default export name (`ArticleCard.tsx` exports `ArticleCard`)

### Comment Discipline

- **Explain WHY, not WHAT** — self-documenting code is the goal
- **JSDoc on all exports** — purpose, params, return type, side effects
- **Reference the spec** — `PRD §4.3`, `PAD §5.5`, `Phase 19 / H9`
- **Document gotchas inline** — future readers need to know why a non-obvious choice was made

### Git Discipline

- **Atomic commits** — one logical change per commit
- **TDD cycle** — one Red-Green-Refactor cycle per commit
- **Pre-commit hooks** — husky + lint-staged runs eslint + prettier on staged `.ts`/`.tsx`
- **No `db:push` script** — removed from `package.json`. Use `db:generate` + `db:migrate`.

### Performance Best Practices

- **`<Image>` component for all images** — optimization, lazy loading, CLS prevention
- **External domains in `remotePatterns`** — security requirement
- **`tabular-nums`** for dates/numbers — no width jitter
- **CSS Subgrid** for feed alignment — no fixed heights, no JS measurement
- **`cacheLife("feed")`** for news feed — 30s stale, 120s revalidate
- **Lazy DB proxy** — defers connection until first query, prevents build-time crashes

### Security & Type-Safety Best Practices (Phase 25)

- **Escape JSON for script contexts** — `escapeForScriptContext()` after `JSON.stringify` when embedding via `dangerouslySetInnerHTML`. Escapes `<>&` + U+2028/2029 as JSON-compatible `\u00XX` sequences.
- **Enforce uniqueness at the DB level** — application-level checks are racy. Add unique indexes via Drizzle migrations. Use `onConflictDoNothing()` / `onConflictDoUpdate()` to handle conflicts gracefully.
- **Wrap library generic calls in helper functions** — when a library's generic type prevents direct type-safe usage (e.g., `DrizzleAdapter<SqlFlavor>` union), create a wrapper that pins the generic to the specific variant. Eliminates `as any` + `eslint-disable` comments.
- **Use compound cursors with deterministic tiebreakers** — `ORDER BY (rank, publishedAt, id)` with cursor `publishedAt|articleId`. Prevents skip/duplicate on tied sort keys.
- **Add CI guards for secret hygiene** — `scripts/check-env-leaks.sh` fails CI if `.env*` files are tracked. Catches the root cause of secret leaks (`.gitignore` without `git rm --cached`).
- **Provide backward-compat paths when changing API contracts** — legacy cursors (bare ISO date) fall back to date-only filtering. New format (`publishedAt|articleId`) is preferred but old clients don't break.
- **Grep for ALL consumers before deleting code** — `grep -rn "functionName\|\.fieldName" src/` includes test files. Dead code survives when tests keep it "alive" from a coverage perspective.

---

## 15. Coding Patterns

### The "queries.ts Boundary" Pattern

Every feature has a `queries.ts` that encapsulates all DB access. Components never call Drizzle directly.

```typescript
// src/features/feed/queries.ts
export function buildFeedQuery(
  options: FeedQueryOptions = {},
): Promise<ArticleWithSource[]> {
  // Pure query builder — no "use cache", unit-testable in vitest
  // ...
}

export async function getFeedArticles(
  options: FeedQueryOptions = {},
): Promise<FeedPage> {
  "use cache";
  cacheLife("feed");
  const rows = await buildFeedQuery(options);
  // Slice + compute hasMore + nextCursor
  // ...
}
```

**Why split:** `"use cache"` + `cacheLife()` are Next.js compiler directives that throw in vitest. The pure `buildFeedQuery` helper is testable; the cached `getFeedArticles` wrapper is the public API.

### The "Server Action Wrapper" Pattern

Server Actions that need to be called from `<form action={...}>` require a FormData wrapper.

```typescript
// The "pure" action takes a typed argument
export async function pauseSource(id: string) {
  await verifyAdminSession();
  // ...
}

// The FormData wrapper for form binding
export async function pauseSourceAction(formData: FormData): Promise<void> {
  const id = formData.get("id");
  if (typeof id !== "string" || id.length === 0) {
    throw new Error("id field is required and must be a non-empty string");
  }
  await pauseSource(id);
}
```

### The "Fail-Open Rate Limiter" Pattern

```typescript
let rateLimitResult;
try {
  rateLimitResult = await checkRateLimit(`api:articles:${ip}`, 20, 1);
} catch (rateLimitError) {
  console.warn("[API /articles] Rate limiter unavailable (Redis down?), failing open:", rateLimitError);
  rateLimitResult = null;  // Skip the 429 check
}

if (rateLimitResult && !rateLimitResult.allowed) {
  return NextResponse.json({ error: "Rate limit exceeded." }, { status: 429, headers: { "Retry-After": ... } });
}

// ... continue processing
```

**Applied symmetrically to `/api/articles` (Phase 21 S7) AND `/api/summarize/[id]` (Phase 22 / N1).**

### The "3-Layer Provenance" Pattern

```typescript
// All 3 layers generated from a single input via pure function
const provenance = generateProvenanceMetadata({
  summary: { summaryText, keyPoints, sourcesCited, aiStatement, coveragePercentage },
  articleId, articleUrl, articleTitle, model, generatedAt,
});

// Layer 1: JSON-LD <script> in body (NOT via metadata.other)
<script type="application/ld+json" dangerouslySetInnerHTML={{ __html: provenance.jsonLd }} />

// Layer 2: HTTP header via next.config.ts headers() (NOT via metadata.other — Phase 23 / BUG-2)
// next.config.ts:
//   { source: "/article/:id*", headers: [{ key: "X-AI-Provenance", value: "eu-ai-act-art50-compliant; disclosure-in-meta-and-jsonld" }] }

// Layer 3: meta tag via metadata.other in generateMetadata()
return { other: { "ai-provenance": provenance.metaTag } };
// DO NOT put "X-AI-Provenance" in metadata.other — it only emits <meta> tags, not HTTP headers.
```

### The "Belt-and-Suspenders Validation" Pattern

Security-critical modules validate their own inputs even when an upstream Zod layer exists.

```typescript
// src/lib/security/encrypt.ts
const HEX_64_REGEX = /^[0-9a-fA-F]{64}$/;
function validatePushKeyEncryptionKey(value: string | undefined): string {
  if (!value)
    throw new Error("PUSH_KEY_ENCRYPTION_KEY is required (64 hex chars)...");
  if (!HEX_64_REGEX.test(value))
    throw new Error("PUSH_KEY_ENCRYPTION_KEY must be 64 hex chars...");
  return value;
}

const KEY_BUFFER = Buffer.from(
  validatePushKeyEncryptionKey(env.PUSH_KEY_ENCRYPTION_KEY),
  "hex",
);
```

**Why:** When `@/lib/env` is mocked in tests, Zod validation is bypassed. The belt-and-suspenders check ensures consistent error messages regardless of whether the upstream layer ran.

### The "Content Availability Guard" Pattern

```typescript
// Enforced at BOTH Server Action AND API Route layers
if (
  article.contentAvailability === "title_only" ||
  article.contentAvailability === "excerpt"
) {
  return {
    success: false,
    error: `Cannot summarise articles with only ${article.contentAvailability}.`,
  };
}
```

**Why both:** Server Actions and API routes are separate entry points. Either could be bypassed (e.g., a future admin script). Dual enforcement is defense-in-depth.

### The "escapeForScriptContext" Pattern (Phase 25 / F2)

When embedding JSON in a `<script>` tag via `dangerouslySetInnerHTML`, `JSON.stringify` alone is NOT safe — `</script>` terminates the script tag regardless of being inside a JSON string.

```typescript
// src/lib/ai/provenance.ts
function escapeForScriptContext(json: string): string {
  return json
    .replace(/</g, "\\u003c")
    .replace(/>/g, "\\u003e")
    .replace(/&/g, "\\u0026")
    .replace(/\u2028/g, "\\u2028")
    .replace(/\u2029/g, "\\u2029");
}

function generateJsonLd(input: ProvenanceInput): string {
  const jsonLd = {
    /* ... */
  };
  return escapeForScriptContext(JSON.stringify(jsonLd, null, 2));
}
```

**Why this works:** The `\u003c` escape is JSON-compatible — `JSON.parse()` reverses it automatically. Downstream consumers see the original `<`, `>`, `&` characters. But the HTML parser sees `\u003c/script\u003e` (not `</script>`), so it can't break out of the script tag.

### The "createPgAdapter Wrapper" Pattern (Phase 25 / F5)

When a library's generic type prevents direct type-safe usage, wrap it in a helper that pins the generic.

```typescript
// src/lib/auth/index.ts
function createPgAdapter(
  db: unknown,
  config: { usersTable: typeof schema.users /* ... */ },
): ReturnType<typeof DrizzleAdapter> {
  const pgDb = db as PgDatabase<PgQueryResultHKT>;
  return DrizzleAdapter(
    pgDb,
    config as unknown as Parameters<
      typeof DrizzleAdapter<PgDatabase<PgQueryResultHKT>>
    >[1],
  );
}
```

**Why this works:** `DrizzleAdapter<SqlFlavor>` is generic over a union (pg/mysql/sqlite). `Parameters<typeof DrizzleAdapter>[1]` extracts the parameter type WITHOUT the generic bound — resolves to the union. By explicitly specializing `<PgDatabase<PgQueryResultHKT>>` inside the wrapper, `Parameters` resolves to `DefaultPostgresSchema` (not the union), and the cast compiles.

### The "Compound Cursor" Pattern (Phase 25 / F6)

Composite `ORDER BY` requires a composite cursor to prevent skip/duplicate on tied sort keys.

```typescript
// src/features/search/queries.ts
function encodeSearchCursor(publishedAt: Date, articleId: string): string {
  return `${publishedAt.toISOString()}|${articleId}`;
}

function parseSearchCursor(raw: string): ParsedCursor | undefined {
  const pipeIdx = raw.indexOf("|");
  if (pipeIdx === -1) {
    // Legacy format: bare ISO date — backward compat
    const date = new Date(raw);
    return isNaN(date.getTime())
      ? undefined
      : { publishedAt: date, articleId: "" };
  }
  const [dateStr, articleId] = [raw.slice(0, pipeIdx), raw.slice(pipeIdx + 1)];
  const date = new Date(dateStr);
  return isNaN(date.getTime()) || !articleId
    ? undefined
    : { publishedAt: date, articleId };
}

// Composite filter: (publishedAt < cursor) OR (publishedAt = cursor AND id < cursor.id)
cursorClause = sql`(${articles.publishedAt} < ${parsedCursor.publishedAt}
  OR (${articles.publishedAt} = ${parsedCursor.publishedAt}
      AND ${articles.id} < ${parsedCursor.articleId}))`;
```

**Why this works:** The `id` UUID is a deterministic tiebreaker — no two rows share the same `(publishedAt, id)` tuple. The cursor encodes the full sort key, so pagination is deterministic regardless of DB internals (page splits, index scan order). The backward-compat path (no `|` separator) accepts legacy bare-ISO-date cursors and falls back to date-only filtering.

---

## 16. Coding Anti-Patterns

(See [Section 9: Anti-Patterns & Common Bugs](#9-anti-patterns--common-bugs) for the complete catalog of 55 anti-patterns.)

The most critical to remember:

1. **`any` in TypeScript** → use `unknown` + type guards
2. **`enum` / `namespace`** → string unions + ES modules (violates `erasableSyntaxOnly`)
3. **`throw new Error()` in RSC auth** → `redirect('/sign-in')`
4. **`verifySession()` in try/catch** → remove try/catch (catches `NEXT_REDIRECT`)
5. **CSP with `'unsafe-eval'`** → remove (with regression test)
6. **Rate limiter without fail-open** → wrap in try/catch
7. **Server Actions without auth** → every action starts with `verifySession()`
8. **`process.env.*` outside `lib/env/`** → import `env` from `@/lib/env`
9. **Raw hex colors** → use design tokens
10. **Regex HTML stripping** → use `cheerio`

---

## 17. Responsive Breakpoint Reference

### Tailwind v4 Default Breakpoints

| Prefix | Min Width | Typical Device                  |
| :----- | :-------- | :------------------------------ |
| (none) | 0px       | Mobile portrait                 |
| `sm:`  | 640px     | Mobile landscape / small tablet |
| `md:`  | 768px     | Tablet portrait                 |
| `lg:`  | 1024px    | Tablet landscape / small laptop |
| `xl:`  | 1280px    | Desktop                         |
| `2xl:` | 1536px    | Large desktop                   |

### Container Pattern

The standard content container is `max-w-[1440px] mx-auto px-4 sm:px-6 lg:px-8`:

```tsx
<section className="max-w-[1440px] mx-auto px-4 sm:px-6 lg:px-8 pt-10 pb-8">
  {/* Content */}
</section>
```

- Mobile: `px-4` (16px padding)
- Tablet: `sm:px-6` (24px padding)
- Desktop: `lg:px-8` (32px padding)
- Max width: 1440px (centered with `mx-auto`)

### Feed Grid Breakpoints

```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-8">
  {/* ArticleCard with grid-rows-subgrid row-span-3 */}
</div>
```

- Mobile: 1 column
- Tablet (`md:`): 2 columns
- Desktop (`lg:`): 3 columns

### LeadStory Breakpoints

```tsx
<div className="grid grid-cols-1 lg:grid-cols-12 gap-6 lg:gap-12">
  <div className="lg:col-span-7">{/* Image */}</div>
  <div className="lg:col-span-5 flex flex-col justify-center">
    {/* Headline + excerpt */}
  </div>
</div>
```

- Mobile: stacked (image above headline)
- Desktop (`lg:`): 12-column grid, image takes 7 cols, headline takes 5 cols

### Headline Size Progression

```tsx
<h1 className="font-editorial text-3xl sm:text-4xl lg:text-[46px] leading-[1.05] text-ink-900">
```

- Mobile: `text-3xl` (30px)
- Tablet: `sm:text-4xl` (36px)
- Desktop: `lg:text-[46px]` (arbitrary value for precise editorial scaling)

---

## 18. Z-Index Layer Map

| Z-Index | Element                         | Class                           | Purpose                                       |
| :------ | :------------------------------ | :------------------------------ | :-------------------------------------------- |
| `9999`  | Skip-to-content link (on focus) | `focus:z-[9999]`                | Always visible above all content when focused |
| `999`   | Scroll progress bar             | `z-999` (in `.scroll-progress`) | Fixed top bar showing scroll position         |
| `50`    | Admin sidebar nav               | `z-50` (when sticky)            | Stays above main content on scroll            |
| `40`    | Header (Masthead)               | `z-40`                          | Stays above page content                      |
| `30`    | News ticker                     | `z-30`                          | Below header, above content                   |
| `20`    | Mobile menu overlay             | `z-20`                          | Above content, below header                   |
| `10`    | Card hover overlays             | `z-10`                          | Above sibling cards                           |
| (none)  | Default content                 | (default `z-auto`)              | Normal flow                                   |

**Rules:**

- Skip link is always highest (a11y requirement)
- Fixed/sticky UI elements (`z-30` to `z-50`) sit above content
- Hover overlays use `z-10`
- Never use `z-[9999]` except for skip link (it's a reserved a11y z-index)

---

## 19. Color Reference (Complete)

### Ink Scale (Text + Dark Surfaces)

| Token             | Hex       | WCAG AAA Contrast on paper-50 | Usage                                      |
| :---------------- | :-------- | :---------------------------- | :----------------------------------------- |
| `--color-ink-900` | `#1a1a18` | 15.8:1 ✅                     | Headlines, admin sidebar bg                |
| `--color-ink-700` | `#2a2a27` | 12.5:1 ✅                     | Hover states on dark surfaces              |
| `--color-ink-600` | `#3d3d3a` | 9.5:1 ✅                      | Body text (primary)                        |
| `--color-ink-500` | `#525250` | 7.2:1 ✅                      | Secondary text                             |
| `--color-ink-400` | `#6b6b68` | 5.1:1 ✅ (AA)                 | Muted text                                 |
| `--color-ink-300` | `#8a8a83` | 3.4:1 ⚠ (AA Large only)       | Metadata, dividers, decorative dots        |
| `--color-ink-100` | `#e8e8e4` | 1.2:1 ❌                      | Borders, scrollbar thumb (decorative only) |

### Paper Scale (Backgrounds + Light Surfaces)

| Token               | Hex       | Usage                            |
| :------------------ | :-------- | :------------------------------- |
| `--color-paper-50`  | `#fafaf8` | Page background (warm off-white) |
| `--color-paper-100` | `#f2f2ee` | Card hover bg, NutritionLabel bg |
| `--color-paper-200` | `#e6e4de` | Image placeholders               |
| `--color-paper-300` | `#d8d4cc` | Card borders on dark surfaces    |

### Dispatch Brand Accents

| Token                           | Hex       | Usage                                                          |
| :------------------------------ | :-------- | :------------------------------------------------------------- |
| `--color-dispatch-ember`        | `#c7513f` | **PRIMARY ACCENT** — breaking/AI badge/focus rings/CTA buttons |
| `--color-dispatch-ember-light`  | `#fde8e4` | Ember tinted backgrounds                                       |
| `--color-dispatch-sage`         | `#6b8f71` | "Active" status indicator                                      |
| `--color-dispatch-sage-light`   | `#e4ede5` | Sage tinted backgrounds                                        |
| `--color-dispatch-slate`        | `#5a6b7a` | Source attribution text                                        |
| `--color-dispatch-slate-light`  | `#e2e7ec` | Slate tinted backgrounds                                       |
| `--color-dispatch-clay`         | `#8b6d5a` | Warm earth tone (accent)                                       |
| `--color-dispatch-clay-light`   | `#ede5df` | Clay tinted backgrounds                                        |
| `--color-dispatch-violet`       | `#7a6b8f` | Citation links                                                 |
| `--color-dispatch-violet-light` | `#e8e4ef` | Violet tinted backgrounds                                      |

### Semantic State Tokens (Phase 19 / M15)

| Token                            | Hex       | Tailwind Default Equivalent | Usage                             |
| :------------------------------- | :-------- | :-------------------------- | :-------------------------------- |
| `--color-dispatch-warning`       | `#b45309` | `amber-700`                 | SummaryPanel `needs_review` state |
| `--color-dispatch-warning-light` | `#fef3c7` | `amber-50`                  | Warning tinted backgrounds        |
| `--color-dispatch-danger`        | `#dc2626` | `red-600`                   | Button `destructive` variant      |
| `--color-dispatch-danger-dark`   | `#b91c1c` | `red-700`                   | Destructive hover state           |

### Color Usage Rules

1. **Never use raw hex in components** — always reference tokens (`bg-ink-900`, not `bg-[#1a1a18]`)
2. **Never use Tailwind's default `amber-*` / `red-*`** — use `dispatch-warning` / `dispatch-danger` (Phase 19 / M15)
3. **Body text uses `ink-600`** (9.5:1 contrast — WCAG AAA)
4. **Headlines use `ink-900`** (15.8:1 contrast — WCAG AAA)
5. **Metadata uses `ink-300`** (3.4:1 — AA Large only, acceptable for `text-[10px] uppercase` decorative text)
6. **Primary accent is `dispatch-ember`** — used for focus rings, CTAs, AI badges, breaking news indicators
7. **Citation links use `dispatch-violet`** — distinct from navigation links (which use `dispatch-ember` on hover)

---

## 20. The Complete TypeScript Interface Reference

### Domain Types (`src/domain/articles/types.ts`)

```typescript
import type { InferSelectModel } from "drizzle-orm";
import type { articles, sources, categories, summaries } from "@/lib/db/schema";

// Base table types (from Drizzle schema)
export type Article = InferSelectModel<typeof articles>;
export type Source = InferSelectModel<typeof sources>;
export type Category = InferSelectModel<typeof categories>;
export type Summary = InferSelectModel<typeof summaries>;

// Article with its source information (requires JOIN)
export interface ArticleWithSource extends Article {
  source: Pick<Source, "id" | "name" | "url">;
}

// Article with source, category, and optional summary (article detail page)
export interface ArticleWithSummary extends ArticleWithSource {
  category: Pick<Category, "id" | "name" | "slug"> | null;
  summary: Summary | null;
}

// Paginated feed result
export interface FeedPage {
  articles: ArticleWithSource[];
  nextCursor: string | null;
  hasMore: boolean;
}
```

### Schema-Derived Types (`src/lib/db/schema.ts`)

```typescript
// All derived via `typeof enum.enumValues)[number]` — Single Source of Truth
export type UserRole = (typeof userRoleEnum.enumValues)[number]; // "reader" | "admin"
export type FeedFormat = (typeof feedFormatEnum.enumValues)[number]; // "rss" | "atom" | "json_api"
export type ContentAvailability =
  (typeof contentAvailabilityEnum.enumValues)[number];
// "title_only" | "excerpt" | "partial_text" | "full_text"
export type SummaryStatus = (typeof summaryStatusEnum.enumValues)[number];
// "none" | "pending" | "ok" | "needs_review" | "disabled"
```

### AI Summarisation Schema (`src/features/summaries/lib/summariseSchema.ts`)

```typescript
export const sourceCitationSchema = z.object({
  url: z.string().url("Source URL must be a valid URL"),
  title: z.string().trim().min(1, "Source title cannot be empty"),
});

export const summarisationOutputSchema = z.object({
  summaryText: z.string().min(50).max(800),
  keyPoints: z.array(z.string().trim().min(1).max(120)).min(1).max(5),
  sourcesCited: z.array(sourceCitationSchema).min(1),
  aiStatement: z.string().min(20).max(200),
  coveragePercentage: z.number().int().min(0).max(100),
});

export type SummarisationOutput = z.infer<typeof summarisationOutputSchema>;
export type SourceCitation = z.infer<typeof sourceCitationSchema>;

export function validateSummarisationOutput(
  raw: unknown,
):
  | { success: true; data: SummarisationOutput }
  | { success: false; error: string };
```

### Provenance Types (`src/lib/ai/provenance.ts`)

```typescript
export interface ProvenanceInput {
  summary: SummarisationOutput;
  articleId: string;
  articleUrl: string;
  articleTitle: string;
  model: string;
  generatedAt: string; // ISO timestamp
}

export interface ProvenanceResult {
  jsonLd: string; // Layer 1: JSON-LD <script> content
  httpHeader: string; // Layer 2: Base64-encoded JSON for X-AI-Provenance header
  metaTag: string; // Layer 3: Semicolon-delimited string for <meta name="ai-provenance">
}

export function generateProvenanceMetadata(
  input: ProvenanceInput,
): ProvenanceResult;
```

### Auth Types (`types/next-auth.d.ts`)

```typescript
import { DefaultSession } from "next-auth";
import "next-auth/jwt";

declare module "next-auth" {
  interface Session {
    user: {
      id: string;
      role: "reader" | "admin";
    } & DefaultSession["user"]; // Merge to preserve name, email, image
  }

  interface User {
    role: "reader" | "admin";
  }
}

declare module "next-auth/jwt" {
  interface JWT {
    id?: string;
    role?: "reader" | "admin";
  }
}
```

### Feed Query Types (`src/features/feed/queries.ts`)

```typescript
export interface FeedQueryOptions {
  category?: string; // Category slug (resolved to categoryId internally)
  cursor?: Date; // Cursor for pagination (NOT a string — callers parse ISO 8601 first)
  limit?: number; // Default: 30 (FEED_PAGE_SIZE)
}

export interface FeedPage {
  articles: ArticleWithSource[];
  nextCursor: string | null; // ISO 8601 string of last article's publishedAt
  hasMore: boolean;
}
```

### Search Types (`src/features/search/types.ts`)

```typescript
export interface SearchParams {
  query: string;
  cursor?: Date;
  limit?: number; // Default: 31 (SEARCH_PAGE_SIZE — fetches limit+1 to detect hasMore)
}

export interface SearchResult {
  article: ArticleWithSource;
  rank: number; // ts_rank_cd BM25 relevance score
}

export interface SearchPage {
  results: SearchResult[];
  nextCursor: string | null;
  hasMore: boolean;
}
```

### Server Action Return Types

```typescript
// src/features/summaries/actions.ts
export interface SummariseResponse {
  success: boolean;
  jobId: string | null;
  error: string | null;
}

// src/app/(admin)/admin/sources/actions.ts
// pauseSource(id: string) → Source | undefined
// pauseSourceAction(formData: FormData) → Promise<void>  (form-bound wrapper)
// deleteSource(id: string) → Source | undefined  (HARD delete with cascade)
// addSource(data: unknown) → Source
// updateSource(id: string, data: unknown) → Source | undefined
```

### Rate Limit Types (`src/lib/rateLimit.ts`)

```typescript
export interface RateLimitResult {
  allowed: boolean;
  remaining: number; // Never negative
  resetAt: number; // Epoch milliseconds when window resets
}

export async function checkRateLimit(
  identifier: string,
  limit: number,
  windowSec: number,
): Promise<RateLimitResult>;
```

### Worker Job Types (BullMQ)

```typescript
// Ingest job data
interface IngestJobData {
  sourceId: string;
  feedUrl: string;
  feedFormat: FeedFormat;
}

// Summarize job data
interface SummarizeJobData {
  articleId: string;
  content: string; // article.excerpt ?? article.title
}

// Score job data
interface ScoreJobData {
  articleId: string;
}

// Feed-slice job data
interface FeedSliceJobData {
  articleIds: string[];
}

// FlowProducer status (never re-throws)
type PostIngestFlowStatus =
  | { status: "linked"; enqueuedCount: number }
  | {
      status: "degraded";
      fallbackUsed: true;
      fallbackFailures: number;
      enqueuedCount: number;
    }
  | { status: "skipped"; reason: string };
```

### Component Prop Interfaces (Commonly Used)

```typescript
// ArticleCard
interface ArticleCardProps {
  article: ArticleWithSource;
}

// NutritionLabel
interface NutritionLabelProps {
  summary: SummarisationOutput;
}

// SummaryPanel (Client Component — handles 5 states)
interface SummaryPanelProps {
  articleId: string;
  initialStatus: SummaryStatus; // "none" | "pending" | "ok" | "needs_review" | "disabled"
  summary: {
    summaryText: string;
    keyPoints: string[];
    sourcesCited: { url: string; title: string }[];
    aiStatement: string;
    coveragePercentage: number;
  } | null;
}

// AdminGuard (async Server Component)
interface AdminGuardProps {
  children: React.ReactNode;
}

// Button (Shadcn-style with CVA)
interface ButtonProps
  extends
    React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
  isLoading?: boolean;
}

// PageTransition (Client Component — view transitions)
interface PageTransitionProps {
  children: ReactNode;
}
```

### Phase 25 Interfaces (Provenance, Search Cursor, Auth)

```typescript
// src/lib/ai/provenance.ts — Phase 25 / F2 + F4
// NOTE: httpHeader field was REMOVED in Phase 25 / F4 (dead code).
// Layer 2 (X-AI-Provenance HTTP header) is now a static value in next.config.ts.

export interface ProvenanceInput {
  summary: SummarisationOutput;
  articleId: string;
  articleUrl: string;
  articleTitle: string;
  model: string;
  generatedAt: string;
}

export interface ProvenanceResult {
  /** Layer 1: JSON-LD structured data (escaped for safe <script> embedding via escapeForScriptContext) */
  jsonLd: string;
  /** Layer 3: Semicolon-delimited string for HTML <meta name="ai-provenance"> tag */
  metaTag: string;
}

// src/features/search/types.ts — Phase 25 / F6
// NOTE: cursor type changed from `Date` to `string` (compound format).

export interface SearchParams {
  query: string;
  categorySlug?: string;
  /**
   * Cursor for pagination — a string token produced by a previous SearchPage.nextCursor.
   * Format: "publishedAt|articleId" (e.g., "2024-06-01T12:00:00.000Z|art-031").
   * Backward compat: bare ISO date (pre-F6) falls back to date-only filtering.
   */
  cursor?: string;
  limit?: number;
}

// src/features/search/queries.ts — Phase 25 / F6 (internal, not exported)

interface ParsedCursor {
  publishedAt: Date;
  articleId: string; // "" for legacy cursors (date-only)
}

// src/app/account/actions.ts — Phase 25 / F3
// NOTE: linkOAuthProvider now queries by (userId, provider) tuple.

export type LinkResult =
  | { status: "linked"; provider: string }
  | { status: "already_linked"; provider: string }
  | { status: "error"; message: string };

// src/lib/db/schema.ts — Phase 25 / F3
// NOTE: accounts table now has a unique index on (userId, provider).
// Migration: drizzle/0007_accounts_user_provider_unique.sql

export const accounts = pgTable(
  "accounts",
  {
    /* ... existing columns ... */
  },
  (table) => ({
    providerAccountIdx: uniqueIndex("accounts_provider_account_idx").on(
      table.provider,
      table.providerAccountId,
    ),
    // Phase 25 / F3: Enforces (userId, provider) uniqueness at the DB level.
    userProviderIdx: uniqueIndex("accounts_user_provider_idx").on(
      table.userId,
      table.provider,
    ),
  }),
);
```

---

## Appendix: The Meticulous Approach (Mandatory 6-Phase Workflow)

All work on this codebase follows this workflow. **Non-negotiable.**

1. **ANALYZE** — Deep requirement mining. Read actual source files (never assume). Identify explicit, implicit, and edge-case needs. Explore multiple approaches. Assess risks.
2. **PLAN** — Structured execution roadmap. Present for explicit user confirmation before writing code.
3. **VALIDATE** — Obtain user approval. Address concerns. Never proceed without alignment.
4. **IMPLEMENT** — Modular, tested, documented builds. TDD: RED → GREEN → REFACTOR → COMMIT. Use library components before custom ones.
5. **VERIFY** — Rigorous QA against success criteria. Test edge cases, accessibility (WCAG AAA), and performance.
6. **DELIVER** — Complete handoff with instructions, documentation, and next steps.

**Never write code without completing ANALYZE and PLAN. Never skip VALIDATE.**

---

## Appendix: Quick Reference Card

| What                            | Where                                                                                              |
| :------------------------------ | :------------------------------------------------------------------------------------------------- |
| Next.js config                  | `next.config.ts`                                                                                   |
| Next.js config regression tests | `next.config.test.ts` (Phase 22 — CSP/HSTS/XFO/XCTO guards)                                        |
| TypeScript config               | `tsconfig.json`                                                                                    |
| ESLint config                   | `eslint.config.mjs`                                                                                |
| Vitest config (unit)            | `vitest.config.ts`                                                                                 |
| Vitest config (integration)     | `vitest.integration.config.ts`                                                                     |
| Playwright config               | `playwright.config.ts`                                                                             |
| PostCSS config                  | `postcss.config.mjs`                                                                               |
| Prettier ignore                 | `.prettierignore` (Phase 22 / N6)                                                                  |
| Global CSS + design tokens      | `src/app/globals.css`                                                                              |
| Root layout                     | `src/app/layout.tsx`                                                                               |
| Network boundary                | `proxy.ts` (repo root)                                                                             |
| DB schema                       | `src/lib/db/schema.ts`                                                                             |
| Lazy DB proxy                   | `src/lib/db/index.ts`                                                                              |
| Env validation (Zod)            | `src/lib/env/index.ts`                                                                             |
| Auth config                     | `src/lib/auth/index.ts`                                                                            |
| Auth DAL                        | `src/lib/auth/dal.ts`                                                                              |
| Auth providers                  | `src/lib/auth/providers.ts`                                                                        |
| BullMQ queues                   | `src/lib/queue/index.ts`                                                                           |
| FlowProducer DAG                | `src/lib/queue/flows.ts`                                                                           |
| Rate limiter                    | `src/lib/rateLimit.ts`                                                                             |
| Trusted proxy CIDR walker       | `src/lib/network/getClientIp.ts`                                                                   |
| Push key encryption             | `src/lib/security/encrypt.ts`                                                                      |
| AI prompts                      | `src/lib/ai/prompts.ts`                                                                            |
| 3-layer provenance              | `src/lib/ai/provenance.ts`                                                                         |
| Worker entry                    | `src/workers/index.ts`                                                                             |
| RSS parser                      | `src/workers/jobs/parseFeed.ts`                                                                    |
| AI summarizer                   | `src/workers/jobs/summarize.ts`                                                                    |
| Content guard                   | `src/workers/jobs/determineContentAvailability.ts`                                                 |
| Cache invalidation              | `src/workers/lib/cacheInvalidation.ts`                                                             |
| Feed queries                    | `src/features/feed/queries.ts`                                                                     |
| ArticleCard                     | `src/features/feed/components/ArticleCard.tsx`                                                     |
| Summary actions                 | `src/features/summaries/actions.ts`                                                                |
| NutritionLabel                  | `src/features/summaries/components/NutritionLabel.tsx`                                             |
| Account page                    | `src/app/account/page.tsx`                                                                         |
| Admin sources actions           | `src/app/(admin)/admin/sources/actions.ts`                                                         |
| Admin summaries page            | `src/app/(admin)/admin/summaries/page.tsx`                                                         |
| Domain types                    | `src/domain/articles/types.ts`                                                                     |
| Domain normalize                | `src/domain/articles/normalize.ts`                                                                 |
| Importance scoring              | `src/domain/ranking/score.ts`                                                                      |
| `cn()` utility                  | `src/shared/lib/utils.ts`                                                                          |
| Button                          | `src/shared/components/ui/Button.tsx`                                                              |
| useDebounce                     | `src/shared/hooks/useDebounce.ts`                                                                  |
| useReducedMotion                | `src/shared/hooks/useReducedMotion.ts`                                                             |
| PageTransition                  | `src/components/primitives/PageTransition.tsx`                                                     |
| CI pipeline                     | `.github/workflows/ci.yml`                                                                         |
| E2E pipeline                    | `.github/workflows/e2e.yml`                                                                        |
| Pre-commit hook                 | `.husky/pre-commit`                                                                                |
| Env leak CI guard               | `scripts/check-env-leaks.sh` (Phase 25 / F1)                                                       |
| Security remediation runbook    | `SECURITY_REMEDIATION.md` (Phase 25 / F1)                                                          |
| Accounts unique index migration | `drizzle/0007_accounts_user_provider_unique.sql` (Phase 25 / F3)                                   |
| XSS escape helper               | `escapeForScriptContext()` in `src/lib/ai/provenance.ts` (Phase 25 / F2)                           |
| Type-safe auth adapter wrapper  | `createPgAdapter()` in `src/lib/auth/index.ts` (Phase 25 / F5)                                     |
| Compound cursor helpers         | `parseSearchCursor()` / `encodeSearchCursor()` in `src/features/search/queries.ts` (Phase 25 / F6) |

---

**End of `onestopnews_SKILL.md` v3.0.0**

_This skill file is derived from `AGENTS.md` (canonical institutional knowledge), `MASTER_EXECUTION_PLAN.md` v7.0, `CLAUDE.md`, `README.md`, and the actual source tree. For exhaustive per-phase gotchas, consult `AGENTS.md` §Phase N directly. For the engineering blueprint, consult `MASTER_EXECUTION_PLAN.md` v7.0. Phase 25 additions cover the F1-F6 independent code audit & TDD remediation (secret hygiene, XSS prevention, race condition fix, dead code removal, type-safe adapter, compound cursor pagination)._

**Last Updated:** June 25, 2026 (Phase 25 — Independent Code Audit & TDD Remediation complete. 525 tests / 69 suites. All quality gates green. 6 deployment actions outstanding: rotate `AUTH_SECRET` + VAPID keys [F1], apply migration `0007` [F3], wire `check-env-leaks.sh` into CI + pre-commit [F1], switch `pnpm dev` → `pnpm start` [BUG-1], start Redis [BUG-4], set `TRUSTED_PROXY=true` + Cloudflare CIDRs [BUG-5].)
