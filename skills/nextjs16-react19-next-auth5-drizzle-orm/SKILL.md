---
name: nextjs16-react19-next-auth5-drizzle-orm
description: Full-stack Next.js 16 SaaS with React 19, Tailwind v4 CSS-first @theme, Auth.js v5, Drizzle ORM/Postgres (Neon), Inngest job queue, OpenAI + Replicate + ElevenLabs AI pipeline, Stripe billing, Cloudflare R2 storage, SSE streaming. 5-layer architecture (proxy → app → features → domain → lib), App Router Server Components, TypeScript strict, pnpm, Vitest + Playwright E2E, GitHub Actions CI. Luxury-dark cinematic design system with 13 CSS keyframes, WCAG AAA accessibility, server-side URL signing, env-configurable fail-open moderation. Production engineering reference with anti-patterns, debugging guides, and lessons from 4+ sprints.
version: 3.0.0
---

# StoryIntoVideo — Engineering Skill Reference

> **Purpose:** Single-source engineering reference for the StoryIntoVideo codebase. Other coding agents (Claude, Gemini, Codex, etc.) should consult this file when extending, debugging, or replicating this project. Every section is grounded in actual code — exact classNames, color values, configuration flags, and the reasoning behind every non-obvious decision.
>
> **Authoritative Sources:** This SKILL.md is derived from `CLAUDE.md` · `AGENTS.md` · `README.md` · `PRODUCTION_READINESS_PLAN.md` · `Project_Requirements_Document.md` · the actual source tree under `src/`. When in doubt, consult `CLAUDE.md` as the source of truth.
>
> **v3.0.0 changelog:** Reflects Remediation Sprint 2 (post-review hardening) — `trustHost: true` on NextAuth config (fixes P0 production auth outage), `SignedDownloadWrapper` extracted to its own file, SDXL model IDs moved to env vars with format validation, `moderationSkipped` field + env-configurable fail-open policy, SSE reconnect with exponential backoff + `maxDuration = 900`, `putObject` size guard (`MAX_PUT_OBJECT_BYTES = 500 MB`), GitHub Actions CI workflow, `pnpm-workspace.yaml` `packages:` field fix. Test count 232 → 259. Env var count 23 → 28. App components 7 → 8.

---

## Table of Contents

1. [Project Identity & Design Philosophy](#1-project-identity--design-philosophy)
2. [Tech Stack & Environment](#2-tech-stack--environment)
3. [Bootstrapping & Configuration](#3-bootstrapping--configuration)
4. [The Design System (Code-First)](#4-the-design-system-code-first)
5. [Component Architecture & Patterns](#5-component-architecture--patterns)
6. [Custom Hooks Deep Dive](#6-custom-hooks-deep-dive)
7. [Content Management: Static Data Files](#7-content-management-static-data-files)
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
21. [Validation Matrix](#21-validation-matrix)

---

## 1. Project Identity & Design Philosophy

### What StoryIntoVideo Is

StoryIntoVideo is a production SaaS application that transforms written stories into fully produced video content via a 6-step AI pipeline (story analysis → character generation → scene generation → voiceover → subtitle alignment → video assembly). The codebase has two layers:

1. **Marketing front end** — a pixel-accurate clone of `storyintovideo.com`, a luxury-dark, cinematic SaaS landing page. Every color token, keyframe, and hover micro-interaction was field-verified from the live production DOM.
2. **Production backend** — auth, database, AI pipeline, billing, and storage built behind the marketing facade using a 5-layer architecture (proxy → app → features → domain → lib).

### The Core Thesis: "Luxury-Dark Cinematic"

The design philosophy is **luxury-dark cinematic** — not brutalist, not minimal, not generic SaaS. The page treats the viewport like a screening room:

- A near-black canvas (`#020202`, NOT pure `#000`) interrupted by a single dominant accent of warm amber-gold (`#febf00`).
- The H1 is set in **Outfit weight 820** — an extra-bold display weight rarely seen in SaaS, giving the headline a cinematic title-card quality.
- A full-bleed background video plays behind the hero under three stacked overlays (vertical scrim + radial amber glow + bottom fade).
- The entire experience runs on a **13-keyframe CSS motion library** — shimmer sweeps, grid pulses, scanlines, border glows — with zero JavaScript animation libraries.

### The Three Foundational Pillars

1. **Amber is rationed.** `#febf00` is the only hue permitted to assert itself. It appears on CTAs, active states, focus rings, and the eyebrow badges — nowhere else. The CTA hierarchy is deliberate: ghost link → glass pill → gradient pill → solid amber, rationing the accent from least to most prominent.

2. **The singular purple exception.** The yellow→purple gradient (`bg-gradient-to-r from-yellow-500 to-purple-500`) on example-card hover is the **only purple on the entire site**. It exists as a deliberate surprise — a moment of color rebellion in an otherwise monochrome+amber palette. Do not add purple anywhere else.

3. **CSS-only animation.** No Framer Motion. No GSAP. No anime.js. All 13 keyframes are `@keyframes` in `globals.css`. Scroll reveal uses `IntersectionObserver` → `data-revealed` attribute → CSS transition. This is critical for the Lighthouse ≥95 performance budget.

### Explicit Rejections (Anti-Generic Mandate)

- **No Inter/Roboto safety.** Geist Sans (body) + Outfit (headings) + Geist Mono (accents) — all self-hosted, no Google Fonts CDN.
- **No purple-gradient-on-white clichés.** The background is near-black, not white.
- **No predictable Bootstrap-style card grids.** The Features section uses a continuous hairline grid (shared surface with `border-neutral-800` dividers), not boxed cards.
- **No `tailwind.config.ts`.** Tailwind v4 CSS-first `@theme` block in `globals.css` only.
- **No `force-static` on app routes.** The marketing page is static; all app routes are dynamic.
- **No `any` type.** ESLint enforces `@typescript-eslint/no-explicit-any: error`. Use `unknown` instead.
- **No `process.env.*` direct access.** Always import `env` from `@/lib/env` (Zod-validated at module load).

### The Meticulous Six-Phase Workflow

All implementation work follows this mandatory workflow (per `CLAUDE.md`):

1. **ANALYZE** — Deep requirement mining. Never assume. Check existing patterns before writing new code.
2. **PLAN** — Structured roadmap. Present plan for confirmation before coding.
3. **VALIDATE** — Get explicit approval before implementation.
4. **IMPLEMENT** — Modular, tested components. Test each before integration. TDD: RED → GREEN → REFACTOR, one cycle per logical change.
5. **VERIFY** — Run full quality gate: `pnpm lint && pnpm typecheck && pnpm test && pnpm build`.
6. **DELIVER** — Confirm all checks pass. Document deviations.

---

## 2. Tech Stack & Environment

### Exact Versions (verified against `package.json`)

**Runtime dependencies:**

| Package | Version | Purpose |
|---|---|---|
| `next` | ^16.2.0 | Framework (App Router, hybrid rendering, Turbopack dev) |
| `react` | ^19.2.0 | UI |
| `react-dom` | ^19.2.0 | UI |
| `tailwindcss` | ^4.3.0 | Styling (CSS-first `@theme`) |
| `@tailwindcss/postcss` | ^4.3.0 | PostCSS plugin (mandatory for Tailwind v4) |
| `next-auth` | 5.0.0-beta.31 | Auth.js v5 (Google OAuth + Credentials) |
| `@auth/drizzle-adapter` | ^1.11.2 | Auth.js ↔ Drizzle adapter |
| `drizzle-orm` | ^0.45.2 | ORM (SQL-first, type-safe) |
| `postgres` | ^3.4.9 | PostgreSQL driver (Neon pooled connection) |
| `inngest` | ^4.11.0 | Job queue (6-step AI pipeline) |
| `openai` | ^6.45.0 | GPT-4o + Whisper + Moderation |
| `replicate` | ^1.4.0 | SDXL + IP-Adapter image generation |
| `elevenlabs` | ^1.59.0 | TTS voiceover |
| `stripe` | ^22.3.0 | Billing (Checkout + Portal + Webhooks) |
| `@aws-sdk/client-s3` | ^3.1075.0 | Cloudflare R2 storage (S3-compatible) |
| `@aws-sdk/s3-request-presigner` | ^3.1075.0 | R2 signed URLs |
| `fluent-ffmpeg` | ^2.1.3 | Video assembly (MP4 composition) |
| *(none)* | — | FFmpeg binary — system-installed, path via `FFMPEG_PATH` env var (default `/usr/bin/ffmpeg`). `@ffmpeg-installer/ffmpeg` was removed (Turbopack-incompatible). |
| `@radix-ui/react-accordion` | ^1.2.0 | FAQ accordion primitive |
| `@radix-ui/react-dialog` | ^1.1.0 | Mobile nav Sheet primitive |
| `@radix-ui/react-dropdown-menu` | ^2.1.0 | Language switcher primitive |
| `@radix-ui/react-slot` | ^1.3.0 | Button asChild pattern |
| `bcryptjs` | ^3.0.3 | Password hashing (credentials provider) |
| `class-variance-authority` | ^0.7.1 | Button variants |
| `clsx` | ^2.1.1 | Conditional className |
| `tailwind-merge` | ^3.0.0 | Tailwind class dedup |
| `geist` | ^1.7.0 | Geist Sans + Geist Mono fonts |
| `lucide-react` | ^0.460.0 | Icons |
| `zod` | ^4.4.3 | Env + Server Action input validation |

**Dev dependencies (notable):**

| Package | Version | Purpose |
|---|---|---|
| `typescript` | ^5.9.0 | Type checking |
| `vitest` | ^4.0.0 | Unit test runner (jsdom env) |
| `@testing-library/react` | ^16.0.0 | Component testing |
| `@testing-library/jest-dom` | ^6.9.0 | DOM matchers |
| `@playwright/test` | ^1.61.0 | E2E tests (Chromium) |
| `jsdom` | ^29.0.0 | DOM simulation for Vitest |
| `eslint` | ^9.0.0 | Linting (flat config) |
| `typescript-eslint` | ^8.62.0 | TS ESLint rules |
| `eslint-plugin-react` | ^7.37.5 | React rules |
| `eslint-plugin-react-hooks` | ^7.1.1 | Hooks rules |
| `@next/eslint-plugin-next` | ^16.2.9 | Next.js rules |
| `prettier` | ^3.8.0 | Code formatting |
| `prettier-plugin-tailwindcss` | ^0.8.0 | Tailwind class sorting |
| `drizzle-kit` | ^0.31.10 | Migration generator |
| `tsx` | ^4.22.4 | TypeScript execution (seed script) |
| `dotenv-cli` | ^11.0.0 | Load .env.local for CLI scripts |
| `husky` | ^9.1.7 | Git pre-commit hooks |
| `lint-staged` | ^17.0.8 | Run linters on staged files |

### Engine Requirements

```json
"engines": {
  "node": ">=20.0.0",
  "pnpm": ">=9.0.0"
}
```

### TypeScript Strict Mode (Critical Flags)

`tsconfig.json` enables maximum strictness. These flags are non-negotiable:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["dom", "dom.iterable", "ES2022"],
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "noFallthroughCasesInSwitch": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "verbatimModuleSyntax": true,
    "forceConsistentCasingInFileNames": true,
    "isolatedModules": true,
    "moduleResolution": "bundler",
    "jsx": "react-jsx",
    "paths": { "@/*": ["./src/*"] }
  },
  "exclude": ["node_modules", "skills", "docs"]
}
```

**Critical flag explanations:**

- **`verbatimModuleSyntax: true`** — requires `import type` for type-only imports. `import { Foo }` where `Foo` is a type errors. Must use `import type { Foo }` or `import { type Foo }`.
- **`noUncheckedIndexedAccess: true`** — array/object access returns `T | undefined`. `arr[0]` is `T | undefined`, not `T`. Forces null checks.
- **`isolatedModules: true`** — each file must be independently transpilable. Affects re-exports: `export { Foo } from './foo'` works, but type re-exports need `export type { Foo }`.
- **`strict: true`** — enables `noImplicitAny`, `strictNullChecks`, `strictFunctionTypes`, `strictBindCallApply`, `strictPropertyInitialization`, `noImplicitThis`, `alwaysStrict`.

### Package Manager

**pnpm** is the only supported package manager. `pnpm-lock.yaml` is the source of truth. `pnpm-workspace.yaml` MUST contain `packages: ['.']` (even for single-package repos) or pnpm 9+ will fail with `ERR_PNPM_INVALID_WORKSPACE_CONFIGURATION`.

```bash
pnpm install          # Install deps (activates husky via `prepare` script)
pnpm dev              # Start dev server (Turbopack, port 3000)
pnpm lint             # ESLint flat config
pnpm typecheck        # tsc --noEmit
pnpm test             # Vitest (259 unit tests across 33 files)
pnpm test:e2e         # Playwright (48 E2E tests across 9 spec files, requires `pnpm exec playwright install`)
pnpm build            # Production build
pnpm drizzle-kit generate   # Create migration SQL from schema diff
pnpm drizzle-kit migrate    # Apply migrations (needs DATABASE_URL_UNPOOLED)
pnpm db:seed                # Run seed script (dev@storyintovideo.com / password123)
pnpm db:reset               # Migrate + seed in one command
```

---

## 3. Bootstrapping & Configuration

### From Zero (Recreating This Project)

This is **not** a Vite project. It uses Next.js 16 App Router. To bootstrap a similar project from scratch:

```bash
# 1. Create Next.js 16 app
pnpm create next-app@latest story-into-video \
  --typescript \
  --tailwind \
  --eslint \
  --app \
  --src-dir \
  --import-alias "@/*" \
  --use-pnpm

# 2. Install runtime deps
pnpm add next-auth@5.0.0-beta.31 @auth/drizzle-adapter drizzle-orm postgres
pnpm add inngest openai replicate elevenlabs stripe
pnpm add @aws-sdk/client-s3 @aws-sdk/s3-request-presigner
pnpm add fluent-ffmpeg
# System FFmpeg — install via apt/brew, set FFMPEG_PATH env var if non-standard
# sudo apt install ffmpeg  (Ubuntu)  or  brew install ffmpeg  (macOS)
pnpm add @radix-ui/react-accordion @radix-ui/react-dialog @radix-ui/react-dropdown-menu @radix-ui/react-slot
pnpm add bcryptjs class-variance-authority clsx tailwind-merge geist lucide-react zod

# 3. Install dev deps
pnpm add -D drizzle-kit tsx dotenv-cli
pnpm add -D vitest @testing-library/react @testing-library/jest-dom @testing-library/user-event jsdom
pnpm add -D @playwright/test
pnpm add -D husky lint-staged prettier prettier-plugin-tailwindcss
pnpm add -D @types/bcryptjs @types/fluent-ffmpeg @types/node @types/react @types/react-dom

# 4. Install Playwright browsers
pnpm exec playwright install chromium

# 5. Initialize husky
pnpm exec husky init
echo "pnpm lint-staged" > .husky/pre-commit
chmod +x .husky/pre-commit

# 6. Download Outfit variable font (for weight 820 access)
# Source: https://github.com/google/fonts/raw/main/ofl/outfit/Outfit%5Bwght%5D.ttf
# Convert to woff2 via fonttools, place at public/fonts/Outfit-VariableFont.woff2

# 7. Create pnpm-workspace.yaml (CRITICAL — pnpm 9+ requires this even for single-package repos)
cat > pnpm-workspace.yaml << 'EOF'
packages:
  - '.'

onlyBuiltDependencies:
  - sharp
  - unrs-resolver
  - esbuild
EOF
```

### `next.config.ts`

```typescript
import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  reactStrictMode: true,
  poweredByHeader: false,
  allowedDevOrigins: ['storyintovideo.jesspete.shop', '192.168.2.132'],
  images: {
    formats: ['image/avif', 'image/webp'],
  },
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          { key: 'X-Frame-Options', value: 'DENY' },
          { key: 'X-Content-Type-Options', value: 'nosniff' },
          { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
          { key: 'Permissions-Policy', value: 'camera=(), microphone=(), geolocation=()' },
        ],
      },
    ];
  },
};

export default nextConfig;
```

**Notes:**
- `reactStrictMode: true` — surfaces side-effect bugs in dev.
- `poweredByHeader: false` — removes `X-Powered-By: Next.js` header (security).
- `allowedDevOrigins` — needed when dev server is accessed from non-localhost (LAN IP or tunnel).
- Security headers (X-Frame-Options DENY, nosniff, strict referrer) are applied to all routes.

### `postcss.config.mjs` (Tailwind v4 — Critical)

```javascript
/** @type {import('postcss-load-config').Config} */
const config = {
  plugins: {
    '@tailwindcss/postcss': {},
  },
};

export default config;
```

**⚠️ Critical:** Tailwind v4 uses `@tailwindcss/postcss`, NOT the old `tailwindcss` PostCSS plugin. If you write `plugins: { tailwindcss: {} }` (v3 syntax), Tailwind classes won't apply.

### `eslint.config.mjs` (ESLint 9 Flat Config)

```javascript
import js from '@eslint/js';
import tseslint from 'typescript-eslint';
import reactPlugin from 'eslint-plugin-react';
import reactHooksPlugin from 'eslint-plugin-react-hooks';
import nextPlugin from '@next/eslint-plugin-next';
import globals from 'globals';

export default tseslint.config(
  {
    ignores: [
      'node_modules/**', '.next/**', 'out/**', 'build/**', 'coverage/**',
      'playwright-report/**', 'test-results/**', 'public/**',
      'skills/**', 'docs/**', 'scripts/**', 'next-env.d.ts',
    ],
  },
  js.configs.recommended,
  ...tseslint.configs.recommended,
  {
    files: ['**/*.{ts,tsx,js,jsx,mjs,cjs}'],
    plugins: {
      react: reactPlugin,
      'react-hooks': reactHooksPlugin,
      '@next/next': nextPlugin,
    },
    languageOptions: {
      globals: { ...globals.browser, ...globals.node },
      parserOptions: { ecmaFeatures: { jsx: true } },
    },
    settings: { react: { version: 'detect' } },
    rules: {
      ...reactPlugin.configs.recommended.rules,
      ...reactHooksPlugin.configs.recommended.rules,
      ...nextPlugin.configs.recommended.rules,
      'react/react-in-jsx-scope': 'off',
      'react/prop-types': 'off',
      '@typescript-eslint/no-explicit-any': 'error',
      '@typescript-eslint/consistent-type-imports': 'error',
      'react/no-unescaped-entities': 'off',
      'react-hooks/exhaustive-deps': 'warn',
    },
  },
);
```

**Key rules:**
- `@typescript-eslint/no-explicit-any: error` — zero `any` allowed. Use `unknown`.
- `@typescript-eslint/consistent-type-imports: error` — enforces `import type` for type-only imports (required by `verbatimModuleSyntax`).
- `react-hooks/exhaustive-deps: warn` — warns on missing deps in useEffect/useMemo.

### `pnpm-workspace.yaml` (Critical — T0 fix)

```yaml
# pnpm configuration
# The `packages` field is required by pnpm 9+ even for single-package repos
# when this file exists. Listing '.' declares the repo root as the only
# workspace package. Without it, `pnpm install` fails with:
#   ERR_PNPM_INVALID_WORKSPACE_CONFIGURATION  packages field missing or empty
packages:
  - '.'

# Allow specific native build scripts to run during install (pnpm 9 default
# is to skip them unless explicitly approved).
allowBuilds:
  '@ffmpeg-installer/linux-x64': true
  esbuild: true
  protobufjs: true
  sharp: true
  unrs-resolver: true

# Only run postinstall scripts for these packages (security hardening —
# prevents malicious packages from running arbitrary code on install).
onlyBuiltDependencies:
  - sharp
  - unrs-resolver
  - esbuild
```

### `.github/workflows/ci.yml` (T8 — GitHub Actions CI)

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true

jobs:
  quality-gate:
    name: Lint + Typecheck + Test + Build
    runs-on: ubuntu-latest
    timeout-minutes: 15

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Install pnpm
        uses: pnpm/action-setup@v4
        with:
          version: 9

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: pnpm

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Lint (eslint .)
        run: pnpm lint

      - name: Typecheck (tsc --noEmit)
        run: pnpm typecheck

      - name: Unit tests (vitest run)
        run: pnpm test

      - name: Build (next build)
        run: pnpm build
        env:
          NEXT_PHASE: phase-production-build
          NODE_ENV: production
```

**Notes:**
- E2E tests are NOT in CI yet — they require a Postgres service container + Playwright browser binaries + seeded data.
- The build step uses `NEXT_PHASE=phase-production-build` to trigger the env module's build-context fallback (placeholders instead of real env vars).

### Environment Variables (28 in Zod schema + 1 via process.env)

The env module (`src/lib/env/index.ts`) validates all env vars at module load via Zod. **Never read `process.env.*` directly** — always import `env` from `@/lib/env`.

**Required (28 in Zod schema):**

| Category | Vars |
|---|---|
| Database (Neon) | `DATABASE_URL`, `DATABASE_URL_UNPOOLED` |
| Auth (Auth.js v5) | `AUTH_SECRET` (≥32 chars, no weak values), `AUTH_URL` |
| AI Providers | `OPENAI_API_KEY` (`sk-*`), `REPLICATE_API_TOKEN` (`r8_*`), `ELEVENLABS_API_KEY` |
| Replicate Models (T4) | `REPLICATE_SDXL_MODEL` (optional, format-validated), `REPLICATE_SDXL_IPADAPTER_MODEL` (optional, format-validated) |
| Stripe | `STRIPE_SECRET_KEY` (`sk_*`), `STRIPE_WEBHOOK_SECRET` (`whsec_*`), `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` (`pk_*`) |
| Cloudflare R2 | `R2_ACCOUNT_ID`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_BUCKET_UPLOADS`, `R2_BUCKET_GENERATED`, `R2_BUCKET_VIDEOS` |
| Inngest | `INNGEST_EVENT_KEY`, `INNGEST_SIGNING_KEY` |
| Email (Resend) | `RESEND_API_KEY` (`re_*`) |
| Rate Limiting (Upstash) | `UPSTASH_REDIS_REST_URL`, `UPSTASH_REDIS_REST_TOKEN` |
| Monitoring (Sentry) | `SENTRY_DSN` |
| App | `NEXT_PUBLIC_APP_URL`, `NODE_ENV` |
| Google OAuth (optional) | `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` (both required to enable) |

**Optional (read via `process.env` directly, not in Zod schema):**

| Var | Default | Purpose |
|---|---|---|
| `IMAGE_MODERATION_FAIL_OPEN` | `true` | When `false`, `moderateImage` fails CLOSED on unknown output shapes (T5) |
| `FFMPEG_PATH` | `/usr/bin/ffmpeg` | Path to system FFmpeg binary |

**Build-context fallback:** When `NEXT_PHASE=phase-production-build` or `NODE_ENV=test`, the env module returns placeholder values instead of throwing. This allows `next build` to succeed without real env vars.

**AUTH_URL host-mismatch warning (T2):** The env module emits a `console.warn` at module load when `AUTH_URL` and `NEXT_PUBLIC_APP_URL` resolve to different hosts. With `trustHost: true` on the NextAuth config, this is no longer fatal, but it should still be fixed.

---

## 4. The Design System (Code-First)

### The `@theme` Block (Complete — from `src/app/globals.css`)

Tailwind v4 uses a CSS-first `@theme` block instead of `tailwind.config.ts`. All design tokens live here:

```css
@import 'tailwindcss';

/* Explicit content scanning (Tailwind v4 best practice) */
@source '../components/**/*.{ts,tsx}';
@source '../lib/**/*.{ts,tsx}';

@theme {
  /* ── Color Palette (verified from live site :root) ── */
  --color-background: #020202;
  --color-foreground: #f8f8f8;
  --color-card: #060607;
  --color-card-foreground: #f8f8f8;
  --color-popover: #0b0b0d;
  --color-popover-foreground: #f8f8f8;
  --color-primary: #febf00;
  --color-primary-foreground: #020202;
  --color-secondary: #111114;
  --color-secondary-foreground: #f8f8f8;
  --color-muted: #1a1a1d;
  --color-muted-foreground: #8e8e95;
  --color-accent: #febf00;
  --color-accent-foreground: #020202;
  --color-destructive: #ff2d39;
  --color-destructive-foreground: #f8f8f8;
  --color-border: #1a1a1d;
  --color-input: #0b0b0d;
  --color-ring: #febf0080;

  /* Chart palette (reserved for future dashboard use) */
  --color-chart-1: #febf00;
  --color-chart-2: #00aa6f;
  --color-chart-3: #8d92f9;
  --color-chart-4: #f14d4c;
  --color-chart-5: #7bc27e;

  /* ── Typography ── */
  --font-sans: var(--font-geist-sans), ui-sans-serif, system-ui, sans-serif;
  --font-mono: var(--font-geist-mono), ui-monospace, SFMono-Regular, monospace;
  --font-heading: var(--font-outfit), ui-sans-serif, system-ui, sans-serif;

  /* ── Border Radius ── */
  --radius: 0.75rem;
  --radius-sm: calc(0.75rem - 4px);
  --radius-md: calc(0.75rem - 2px);
  --radius-lg: 0.75rem;
  --radius-xl: 1rem;
  --radius-2xl: 1.25rem;

  /* ── Shadows ── */
  --shadow-hero-input: 0 20px 80px rgba(0, 0, 0, 0.6);
  --shadow-eyebrow-glow: 0 0 30px rgba(234, 179, 8, 0.1);
  --shadow-cta-glow: 0 0 40px rgba(251, 191, 36, 0.3);

  /* ── Animations (13 keyframes, all kebab-case) ── */
  --animate-fade-in-up: fade-in-up 0.6s ease-out both;
  --animate-float: float 6s ease-in-out infinite;
  --animate-glow-pulse: glow-pulse 3s ease-in-out infinite;
  --animate-border-glow: border-glow 4s ease-in-out infinite;
  --animate-composite-pulse-text: composite-pulse-text 2s ease-in-out infinite;
  --animate-shimmer: shimmer 3s linear infinite;
  --animate-btn-shimmer: btn-shimmer 1.5s ease-in-out infinite;
  --animate-grid-shimmer: grid-shimmer 8s ease-in-out infinite;
  --animate-grid-sweep-h: grid-sweep-h 8s linear infinite;
  --animate-grid-sweep-v: grid-sweep-v 10s linear infinite;
  --animate-scanline-scroll: scanline-scroll 1s linear infinite;
  --animate-lang-dropdown-in: lang-dropdown-in 0.15s ease-out;
  --animate-marquee-scroll: marquee-scroll 40s linear infinite;

  /* ── Keyframes (inside @theme so Tailwind v4 picks them up) ── */
  @keyframes fade-in-up { 0% { opacity: 0; transform: translateY(20px); } 100% { opacity: 1; transform: translateY(0); } }
  @keyframes float { 0%, 100% { transform: translateY(0) rotate(var(--card-rotate, 0deg)); } 50% { transform: translateY(-12px) rotate(var(--card-rotate, 0deg)); } }
  @keyframes glow-pulse { 0%, 100% { box-shadow: 0 0 20px rgba(251, 191, 36, 0.3); } 50% { box-shadow: 0 0 40px rgba(251, 191, 36, 0.5); } }
  @keyframes border-glow { 0%, 100% { border-color: rgba(245, 184, 0, 0.08); } 50% { border-color: rgba(245, 184, 0, 0.2); } }
  @keyframes composite-pulse-text { 0%, 100% { opacity: 0.7; } 50% { opacity: 1; } }
  @keyframes shimmer { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }
  @keyframes btn-shimmer { 0% { transform: translate(-100%); } 100% { transform: translate(100%); } }
  @keyframes grid-shimmer { 0% { transform: translate(-20%, -30%); } 50% { transform: translate(70%, 40%); } 100% { transform: translate(-20%, -30%); } }
  @keyframes grid-sweep-h { 0% { transform: translate(-600px); } 100% { transform: translate(calc(600px + 100vw)); } }
  @keyframes grid-sweep-v { 0% { transform: translateY(-500px); } 100% { transform: translateY(calc(500px + 100vh)); } }
  @keyframes scanline-scroll { 0% { background-position-x: 0; } 100% { background-position-x: 30px; } }
  @keyframes lang-dropdown-in { 0% { opacity: 0; transform: translateY(-4px) scale(0.96); } 100% { opacity: 1; transform: translateY(0) scale(1); } }
  @keyframes marquee-scroll { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }
}
```

### The 13 Keyframes (Complete List)

All keyframes are kebab-case (Decision B — PRD §9 camelCase and §8.1 kebab conflict; kebab wins):

| # | Keyframe | Purpose | Duration |
|---|---|---|---|
| 1 | `fade-in-up` | Entrance: opacity 0→1 + translateY 20px→0 | 0.6s ease-out |
| 2 | `float` | Ambient: translateY 0→-12px→0 (cards) | 6s ease-in-out infinite |
| 3 | `glow-pulse` | Ambient: box-shadow 20px→40px amber | 3s ease-in-out infinite |
| 4 | `border-glow` | Ambient: border-color 0.08→0.2 amber | 4s ease-in-out infinite |
| 5 | `composite-pulse-text` | Ambient: opacity 0.7→1 | 2s ease-in-out infinite |
| 6 | `shimmer` | Shimmer: background-position 200%→-200% | 3s linear infinite |
| 7 | `btn-shimmer` | Shimmer: translate -100%→100% | 1.5s ease-in-out infinite |
| 8 | `grid-shimmer` | Grid: translate(-20%,-30%)→(70%,40%) | 8s ease-in-out infinite |
| 9 | `grid-sweep-h` | Grid: translate -600px→calc(600px+100vw) | 8s linear infinite |
| 10 | `grid-sweep-v` | Grid: translateY -500px→calc(500px+100vh) | 10s linear infinite |
| 11 | `scanline-scroll` | Scanline: background-position-x 0→30px | 1s linear infinite |
| 12 | `lang-dropdown-in` | Dropdown: opacity 0→1 + translateY -4px→0 + scale 0.96→1 | 0.15s ease-out |
| 13 | `marquee-scroll` | Marquee: translateX 0→-50% | 40s linear infinite |

### Custom `@utility` Classes (7 total)

Tailwind v4 uses `@utility` instead of `@layer components` + `@layer utilities`:

| Utility | Purpose | Key CSS |
|---|---|---|
| `scrollbar-hide` | Hide scrollbar (carousels) | `scrollbar-width: none; &::-webkit-scrollbar { display: none; }` |
| `marquee-mask` | Fade marquee edges | `mask-image: linear-gradient(to right, transparent, black 8%, black 92%, transparent)` |
| `marquee-track` | Infinite horizontal scroll, pauses on hover | `animation: var(--animate-marquee-scroll); &:hover { animation-play-state: paused; }` |
| `glass-input` | Hero story textarea wrapper | `backdrop-filter: blur(16px); border: 1px solid rgb(255 255 255 / 0.08); &:focus-within { border-color: rgb(251 191 36 / 0.3); }` |
| `eyebrow` | Amber pill badge with ambient glow | `background-color: rgb(251 191 36 / 0.1); border: 1px solid rgb(251 191 36 / 0.25); font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em;` |
| `section-heading` | H2 fluid clamp size | `font-family: var(--font-heading); font-weight: 700; letter-spacing: -0.03em; font-size: clamp(2rem, 5vw, 3rem);` |
| `cta-amber` | Tier-4 CTA: solid amber pill | `background-color: var(--color-primary); &:hover { background-color: rgb(252 211 77); transform: scale(1.02); }` |

### Typography Hierarchy

| Element | Font | Weight | Key Class |
|---|---|---|---|
| H1 (hero desktop) | Outfit | **820** | `font-heading text-[4.5rem] tracking-[-0.04em]` + `style={{ fontWeight: 820 }}` |
| H1 (hero mobile) | Outfit | 820 | `text-4xl` (scales with `em`) |
| H2 (sections) | Outfit | 700 | `font-heading text-4xl lg:text-6xl tracking-[-0.03em]` |
| Body | Geist Sans | 400 | `font-sans text-lg` |
| Ratio toggles | Geist Mono | 400 | `font-mono text-[10px]` |
| Character counter | Geist Mono | 400 | `font-mono text-[10px] tabular-nums` |

**Outfit weight 820** is self-hosted via `next/font/local` (Google Fonts API only serves discrete weights). The font file is at `public/fonts/Outfit-VariableFont.woff2` (45KB, weight range 100-900).

### Font Configuration (`src/lib/fonts.ts`)

```typescript
import { GeistSans } from 'geist/font/sans';
import { GeistMono } from 'geist/font/mono';
import localFont from 'next/font/local';

const outfit = localFont({
  src: '../../public/fonts/Outfit-VariableFont.woff2',
  weight: '100 900',
  variable: '--font-outfit',
  display: 'swap',
});

export const fonts = {
  sans: GeistSans,
  mono: GeistMono,
  heading: outfit,
};

export const fontVariables: string = [GeistSans.variable, GeistMono.variable, outfit.variable].join(' ');
```

The `fontVariables` string is applied to `<html>` in `layout.tsx` via `className={fontVariables}`.

### CTA Hierarchy (4 Tiers — Amber Rationed)

| Tier | Component | Class Pattern | Usage |
|---|---|---|---|
| 1 (ghost) | Footer links | `text-zinc-400 hover:text-amber-400` | Least prominent |
| 2 (glass pill) | Hero "Start Creating" | `rounded-full bg-gradient-to-r from-zinc-800 to-zinc-900 text-amber-300` | Mid prominence |
| 3 (gradient pill) | Workflow CTAs | `rounded-full border border-amber-400/30 bg-amber-400/10 text-amber-300` | High prominence |
| 4 (solid amber) | Final CTA | `cta-amber` utility class | Maximum prominence |

### Scroll Reveal Pattern (CSS-Only)

```css
/* In globals.css */
[data-reveal] {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.6s ease-out, transform 0.6s ease-out;
  transition-delay: var(--reveal-delay, 0s);
}

[data-reveal][data-revealed='true'] {
  opacity: 1;
  transform: translateY(0);
}
```

The `useReveal` hook flips `data-revealed` from `'false'` to `'true'` via `IntersectionObserver`. The `ScrollReveal` primitive wraps this in a reusable component with a `delay` prop (sets `--reveal-delay` CSS var).

### Reduced Motion Override (Global)

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
  .marquee-track { animation: none !important; }
  video[autoplay] { display: none; }
  [data-reveal] { opacity: 1 !important; transform: none !important; }
}
```

This is the global safety net. The `useReducedMotion` hook is for JS-level decisions (e.g., skipping a video autoplay).

---

## 5. Component Architecture & Patterns

### The 5-Layer Architecture (Golden Rule)

```
Layer 0: src/proxy.ts             — Cookie check, redirect. NO DB. NO logic. Edge runtime.
Layer 1: src/app/                 — Route structure, metadata, Suspense. Layouts must NOT fetch data.
Layer 2: src/features/            — UI composition, data binding, mutations (auth, projects, pipeline, billing)
Layer 3: src/features/*/domain/   — Pure business logic. No Next.js or DB runtime imports (import type only)
Layer 4: src/lib/                 — Infrastructure: Drizzle, Auth.js, Inngest, R2, Stripe, AI providers. Side effects only.
```

**Golden Rule:** A lower layer may never import from a higher layer. Domain may import types from Infrastructure but never runtime code.

### Component Directory Structure

```
src/components/
├── primitives/               # Marketing presentational (7 files)
│   ├── scroll-reveal.tsx     # 'use client' — IntersectionObserver wrapper
│   ├── eyebrow.tsx           # Server — amber pill badge
│   ├── section-heading.tsx   # Server — H2 fluid clamp
│   ├── cta-amber.tsx         # Server — Tier-4 solid amber CTA
│   ├── cta-gradient.tsx      # Server — Tier-3 gradient pill CTA
│   ├── cta-ghost.tsx         # Server — Tier-1 ghost link CTA
│   └── style-chip.tsx        # Server — Hero marquee chip
├── sections/                 # Marketing page sections (10 files)
│   ├── navbar.tsx            # 'use client' — scroll-aware + mobile Sheet
│   ├── hero.tsx              # 'use client' — video bg + glass input + chips + counter
│   ├── examples.tsx          # 'use client' — carousel with arrow handlers
│   ├── workflow.tsx          # 'use client' — video loading state + 4 alternating rows
│   ├── features.tsx          # Server — 4×2 hairline grid
│   ├── testimonials.tsx      # Server — 3×2 grid, initials avatars
│   ├── use-cases.tsx         # Server — 2×2 grid, corner glow on hover
│   ├── faq.tsx               # 'use client' — Radix Accordion
│   ├── final-cta.tsx         # Server — dot-grid bg, amber CTA pill
│   └── footer.tsx            # Server — 3 link columns + copyright
├── ui/                       # Hand-written shadcn primitives (4 files)
│   ├── button.tsx            # CVA variants + Radix Slot
│   ├── accordion.tsx         # Radix Accordion (grid-template-rows animation)
│   ├── sheet.tsx             # Radix Dialog (mobile nav)
│   └── dropdown-menu.tsx     # Radix DropdownMenu (language switcher)
└── app/                      # App-specific components (8 files)
    ├── auth-form.tsx         # 'use client' — Google OAuth + email/password
    ├── create-wizard.tsx     # 'use client' — story input + style + ratio + counter
    ├── empty-state.tsx       # Reusable empty-state primitive
    ├── providers.tsx         # 'use client' — SessionProvider wrapper
    ├── project-progress-panel.tsx  # 'use client' — SSE subscriber + progress bar
    ├── signed-download-wrapper.tsx # Server — signs R2 URL, passes as prop (T1)
    ├── project-download-button.tsx # 'use client' — receives downloadUrl prop (NO r2.ts import)
    └── project-share-button.tsx    # 'use client' — Web Share API + clipboard fallback
```

### Marketing Section Order (Fixed, Top → Bottom)

1. Navbar (fixed overlay, `z-50`)
2. Hero (video bg + glass input + style marquee)
3. Examples carousel
4. 4-Step Workflow
5. Features grid (4×2 hairline)
6. Testimonials (3×2 grid)
7. Use Cases (2×2 grid)
8. FAQ (Radix Accordion)
9. Final CTA (dot-grid bg, amber pill)
10. Footer (3 link columns + copyright)

### Component Rendering Strategy

| Component | Type | Reason |
|---|---|---|
| Navbar | `'use client'` | Scroll state, mobile Sheet toggle |
| Hero | `'use client'` | Textarea, chip click, ratio toggle, character counter |
| Examples | `'use client'` | Carousel arrow click handlers |
| Faq | `'use client'` | Radix Accordion (stateful) |
| Workflow | `'use client'` | `useState` for poster→video fade-in choreography |
| Features, Testimonials, UseCases, FinalCTA, Footer | Server | Pure static HTML/CSS |

### Key Component Patterns

#### Hero — 4-Layer Composition

The Hero is the most complex marketing component. It has 4 stacked layers:

```tsx
<section className="relative flex flex-col overflow-hidden bg-zinc-950">
  {/* Layer 1: Background video + overlays (z-0) */}
  <div className="absolute inset-0 z-0" aria-hidden="true">
    <video autoPlay muted loop playsInline preload="metadata" poster="/hero-poster.webp">
      <source src="/hero-bg.mp4" type="video/mp4" />
    </video>
    {/* Vertical scrim */}
    <div className="absolute inset-0 bg-gradient-to-b from-zinc-950/85 via-zinc-950/70 to-zinc-950/80" />
    {/* Radial amber glow */}
    <div
      className="absolute top-[20%] left-1/2 h-[500px] w-[800px] -translate-x-1/2 rounded-full opacity-30 blur-[60px]"
      style={{ background: 'radial-gradient(rgba(251,191,36,0.12),rgba(0,0,0,0) 65%)' }}
    />
  </div>

  {/* Layer 2: Content (z-10) */}
  <div className="relative z-10 mx-auto flex w-full max-w-3xl flex-col items-center px-6 pt-32 pb-6 text-center sm:pt-40 sm:pb-8">
    {/* Eyebrow + H1 (Outfit 820) + Subtitle + Glass input widget */}
  </div>

  {/* Layer 3: Style tags marquee (z-10) */}
  <div className="relative z-10 mt-10 sm:mt-16">
    <div className="marquee-mask overflow-hidden py-4">
      <div className="marquee-track">
        {[...STYLE_CHIPS, ...STYLE_CHIPS].map((chip, idx) => (
          <StyleChipComponent key={`${chip.label}-${idx}`} label={chip.label} sublabel={chip.sublabel} />
        ))}
      </div>
    </div>
  </div>

  {/* Layer 4: Bottom fade (z-0) */}
  <div className="relative z-0 h-8 bg-gradient-to-b from-transparent to-zinc-950 sm:h-12" aria-hidden="true" />
</section>
```

**Key details:**
- H1 uses `style={{ fontWeight: 820 }}` (inline) because Tailwind doesn't have a `font-weight-820` utility.
- Marquee duplicates the chip array (`[...STYLE_CHIPS, ...STYLE_CHIPS]`) for seamless infinite loop (`translateX -50%`).
- Aspect ratio toggle uses `aria-pressed={isActive}` for accessibility.
- Character counter uses `font-mono text-[10px] tabular-nums` and turns amber at ≥450 chars.

#### Glass Input Widget (`@utility glass-input`)

The Hero's story textarea is wrapped in a glass-morphism container:

```css
@utility glass-input {
  position: relative;
  border-radius: var(--radius-2xl);  /* 1.25rem */
  background-color: rgb(9 9 11 / 0.6);
  backdrop-filter: blur(16px);
  padding: 1.25rem;
  border: 1px solid rgb(255 255 255 / 0.08);
  transition-property: border-color, box-shadow;
  transition-duration: 500ms;
  box-shadow: var(--shadow-hero-input);

  &:hover { border-color: rgb(255 255 255 / 0.12); }
  &:focus-within {
    border-color: rgb(251 191 36 / 0.3);
    box-shadow: var(--shadow-hero-input), 0 0 30px rgb(251 191 36 / 0.1);
  }
}
```

#### ScrollReveal Primitive

```tsx
'use client';

export function ScrollReveal({ children, delay = 0, className, as = 'div' }: ScrollRevealProps) {
  const { ref, revealed } = useReveal<HTMLElement>();
  const Tag = as as ElementType;

  return (
    <Tag
      ref={ref}
      data-reveal=""
      data-revealed={revealed ? 'true' : 'false'}
      style={{ '--reveal-delay': `${delay}ms` } as React.CSSProperties}
      className={cn(className)}
    >
      {children}
    </Tag>
  );
}
```

**Key details:**
- `data-reveal=""` (empty string) marks the element as reveal-eligible.
- `data-revealed` flips from `'false'` to `'true'` when the element enters the viewport.
- The `--reveal-delay` CSS var enables staggered entrance (e.g., `delay={100}` for a 100ms delay).

#### Button (shadcn/ui — Hand-Written)

```tsx
const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-all disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg:not([class*='size-'])]:size-4 [&_svg]:shrink-0 outline-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-amber-400",
  {
    variants: {
      variant: {
        default: 'bg-primary text-primary-foreground hover:bg-primary/90',
        destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90',
        outline: 'border border-white/10 bg-transparent hover:bg-white/[0.04] hover:text-foreground',
        secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/80',
        ghost: 'hover:bg-white/[0.04] hover:text-foreground',
        link: 'text-primary underline-offset-4 hover:underline',
      },
      size: {
        default: 'h-9 px-4 py-2 has-[>svg]:px-3',
        sm: 'h-8 rounded-md gap-1.5 px-3 has-[>svg]:px-2.5',
        lg: 'h-10 rounded-md px-6 has-[>svg]:px-4',
        icon: 'size-9',
      },
    },
    defaultVariants: { variant: 'default', size: 'default' },
  },
);
```

**Key detail:** The focus ring uses `outline-amber-400` (NOT `outline-primary`) because Tailwind v4's `amber-400` is `#fbbf24`, which is close enough to our `--color-primary: #febf00` for focus ring purposes. The difference is invisible to the eye.

#### Server-Side URL Signing Pattern (T1 — SignedDownloadWrapper)

```tsx
// src/components/app/signed-download-wrapper.tsx (Server Component — NO 'use client')
import { getSignedDownloadUrl } from '@/lib/storage/r2';
import { ProjectDownloadButton } from '@/components/app/project-download-button';

export async function SignedDownloadWrapper({ videoKey, children }: SignedDownloadWrapperProps) {
  const downloadUrl = await getSignedDownloadUrl('videos', videoKey);

  return (
    <div className="mt-6 flex flex-wrap items-center gap-3">
      <ProjectDownloadButton videoKey={videoKey} downloadUrl={downloadUrl} />
      {children}
    </div>
  );
}
```

```tsx
// src/components/app/project-download-button.tsx ('use client' — receives downloadUrl as prop)
'use client';

export function ProjectDownloadButton({ downloadUrl }: ProjectDownloadButtonProps) {
  return (
    <a href={downloadUrl} download className="...">
      <Download className="h-4 w-4" />
      Download Video
    </a>
  );
}
```

**Why this pattern:** Client components must NEVER import `@/lib/storage/r2` at module level — `r2.ts` imports `env` which validates all 28 env vars at module load. In the browser, only `NEXT_PUBLIC_*` vars exist — all server-only vars are `undefined`, causing "Invalid environment variables" crash. The Server Component signs the URL and passes it as a prop.

#### ProjectProgressPanel — SSE Subscriber with Reconnect (T6)

```tsx
'use client';

export function ProjectProgressPanel({ projectId, initialStatus, ... }: ProjectProgressPanelProps) {
  const progress = useProjectProgress(projectId);

  const status = progress.status ?? initialStatus;
  const progressPercent = progress.progressPercent ?? 0;

  return (
    <div className="rounded-2xl border border-white/[0.06] bg-white/[0.02] p-6">
      <h2 className="font-heading mb-3 text-lg font-bold text-white">Pipeline Status</h2>
      <p className="text-sm text-zinc-400">{label}</p>

      {/* Progress bar */}
      <div className="mt-4 h-2 w-full overflow-hidden rounded-full bg-white/[0.04]">
        <div
          className="h-full rounded-full bg-amber-400 transition-all duration-500"
          style={{ width: `${progressPercent}%` }}
          role="progressbar"
          aria-valuenow={progressPercent}
          aria-valuemin={0}
          aria-valuemax={100}
        />
      </div>

      {progress.connectionState === 'reconnecting' && (
        <p className="mt-2 text-xs text-zinc-500">Reconnecting to live updates…</p>
      )}
      {progress.connectionState === 'error' && (
        <p className="mt-2 text-xs text-amber-400">Live updates disconnected. Refresh the page to retry.</p>
      )}
    </div>
  );
}
```

---

## 6. Custom Hooks Deep Dive

The project has 4 custom hooks in `src/lib/hooks/`:

### `useScrolled(threshold)` — Scroll-Aware Navbar

```typescript
'use client';

import { useEffect, useState } from 'react';

export function useScrolled(threshold = 10): boolean {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > threshold);
    onScroll(); // Initialize on mount
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, [threshold]);

  return scrolled;
}
```

**Usage:** Navbar toggles `bg-zinc-950/70 backdrop-blur-[24px] border-b border-white/10` when `scrolled` is true.

**Key details:**
- `{ passive: true }` — tells the browser the handler won't call `preventDefault()`, enabling scroll optimization.
- `onScroll()` called on mount to initialize the correct state (in case the page loads scrolled).
- Default threshold is 10px (avoids flicker on tiny scrolls).

### `useReveal<T>(options)` — IntersectionObserver Reveal

```typescript
'use client';

import { useEffect, useRef, useState } from 'react';

interface UseRevealOptions {
  threshold?: number;      // Intersection ratio (0-1). Default 0.15.
  rootMargin?: string;     // Default '0px 0px -50px 0px' (triggers 50px before entering).
  once?: boolean;          // If true (default), disconnect after first intersection.
}

export function useReveal<T extends HTMLElement = HTMLDivElement>(
  options: UseRevealOptions = {},
): { ref: React.RefObject<T | null>; revealed: boolean } {
  const { threshold = 0.15, rootMargin = '0px 0px -50px 0px', once = true } = options;
  const ref = useRef<T>(null);
  const [revealed, setRevealed] = useState(false);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    const observer = new IntersectionObserver(
      (entries) => {
        const [entry] = entries;
        if (!entry) return;
        if (entry.isIntersecting) {
          setRevealed(true);
          if (once) observer.disconnect();
        } else if (!once) {
          setRevealed(false);
        }
      },
      { threshold, rootMargin },
    );

    observer.observe(el);
    return () => observer.disconnect();
  }, [threshold, rootMargin, once]);

  return { ref, revealed };
}
```

**Usage:** `ScrollReveal` primitive wraps this. The `data-revealed` attribute drives the CSS transition.

**Key details:**
- `rootMargin: '0px 0px -50px 0px'` — triggers reveal 50px BEFORE the element enters the viewport (feels more responsive).
- `once: true` (default) — observer disconnects after first intersection (perf optimization).
- `once: false` — re-triggers on scroll up/down (useful for elements that should animate every time).
- Returns `RefObject<T | null>` (not `RefObject<T>`) because `useRef<T>(null)` returns `null` initially.

### `useReducedMotion()` — OS-Level Motion Preference

```typescript
'use client';

import { useEffect, useState } from 'react';

export function useReducedMotion(): boolean {
  const [reduced, setReduced] = useState(false);

  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    const onChange = () => setReduced(mediaQuery.matches);

    onChange(); // Initialize on mount
    mediaQuery.addEventListener('change', onChange);
    return () => mediaQuery.removeEventListener('change', onChange);
  }, []);

  return reduced;
}
```

**Usage:** Used in JS-level decisions (e.g., skipping a video autoplay, disabling a JS-driven animation).

**Key details:**
- The global CSS `@media (prefers-reduced-motion: reduce)` block in `globals.css` handles most cases declaratively.
- This hook is for cases where JS needs to know the preference (e.g., conditionally rendering a `<video>` element).
- Uses `addEventListener('change', ...)` (NOT the deprecated `addListener`).

### `useProjectProgress(projectId)` — SSE Subscriber with Reconnect (T6)

```typescript
'use client';

import { useEffect, useState } from 'react';

export interface ProjectProgressState {
  status: string | null;
  progressPercent: number | null;
  progressDetail: string | null;
  errorMessage: string | null;
  connectionState: 'connecting' | 'open' | 'closed' | 'error' | 'reconnecting';
}

const MAX_RECONNECT_ATTEMPTS = 3;
const BASE_BACKOFF_MS = 1000;

function backoffDelay(attempt: number): number {
  return BASE_BACKOFF_MS * Math.pow(2, attempt);  // 1s → 2s → 4s
}

export function useProjectProgress(projectId: string): ProjectProgressState {
  const [state, setState] = useState<ProjectProgressState>(INITIAL_STATE);

  useEffect(() => {
    if (!projectId) return;

    let eventSource: EventSource | null = null;
    let reconnectTimer: ReturnType<typeof setTimeout> | null = null;
    let reconnectAttempt = 0;
    let isCancelled = false;

    const openStream = () => {
      if (isCancelled) return;

      eventSource = new EventSource(`/api/projects/${projectId}/progress`);

      eventSource.onopen = () => {
        reconnectAttempt = 0;  // Reset on successful open
        setState((prev) => ({ ...prev, connectionState: 'open' }));
      };

      eventSource.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          setState({ ...data, connectionState: 'open' });
          if (TERMINAL_STATUSES.has(data.status)) {
            eventSource?.close();
            setState((prev) => ({ ...prev, connectionState: 'closed' }));
          }
        } catch { /* Malformed JSON */ }
      };

      eventSource.onerror = () => {
        if (!eventSource) return;
        eventSource.close();
        eventSource = null;

        if (isCancelled) return;
        if (reconnectAttempt >= MAX_RECONNECT_ATTEMPTS) {
          setState((prev) => ({ ...prev, connectionState: 'error' }));
          return;
        }

        const delay = backoffDelay(reconnectAttempt);
        reconnectAttempt += 1;
        setState((prev) => ({ ...prev, connectionState: 'reconnecting' }));
        reconnectTimer = setTimeout(() => {
          if (!isCancelled) openStream();
        }, delay);
      };
    };

    openStream();

    return () => {
      isCancelled = true;
      if (reconnectTimer) clearTimeout(reconnectTimer);
      if (eventSource) eventSource.close();
    };
  }, [projectId]);

  return state;
}
```

**Usage:** `ProjectProgressPanel` subscribes to live pipeline status via SSE.

**Key details (T6 remediation):**
- **Exponential backoff:** 1s → 2s → 4s (3 attempts max). After max attempts, `connectionState` becomes `'error'`.
- **`isCancelled` flag** — prevents reconnect after unmount (race condition guard).
- **`reconnectAttempt = 0` on `onopen`** — resets counter on successful reconnect.
- **Cleanup** — `useEffect` return clears the reconnect timer + closes the EventSource.
- **`eventSource?.close()`** (optional chaining) — TypeScript strict mode requires this because `eventSource` can be null inside the closure.

---

## 7. Content Management: Static Data Files

### No `import.meta.glob` — This Is Next.js, Not Vite

**⚠️ Critical:** This project uses Next.js 16, NOT Vite. There is no `import.meta.glob`. Content is managed via **static TypeScript data files** in `src/lib/data/`.

### The 10 Data Files

```
src/lib/data/
├── nav-links.ts          # NAV_LINKS (4 links) + NAV_LANGUAGES (['EN', '中文', '日本語'])
├── story-seeds.ts        # STORY_SEEDS (4 chip → seed text mappings) + DEFAULT_STORY_EXAMPLES
├── style-chips.ts        # STYLE_CHIPS (7 chips, "Cyberpunk" has sublabel)
├── examples.ts           # EXAMPLE_CARDS (6 portrait cards)
├── workflow-steps.ts     # WORKFLOW_STEPS (4 alternating media/text rows)
├── features.ts           # FEATURES (8 items in 4×2 hairline grid)
├── testimonials.ts       # TESTIMONIALS (6 cards in 3×2 grid)
├── use-cases.ts          # USE_CASES (4 cards in 2×2 grid)
├── faq-items.ts          # FAQ_ITEMS (6 accordion items)
└── footer-links.ts      # FOOTER_COLUMNS (3 link columns)
```

### Pattern: How to Add New Content

To add a new feature card, edit `src/lib/data/features.ts`:

```typescript
import { Captions, Download, FileText, Film, Mic, Plus, Sparkles, Users } from 'lucide-react';
import type { Feature } from '@/types';

export const FEATURES: Feature[] = [
  { id: 'script-analysis', title: 'AI Script Analysis', description: '...', icon: FileText },
  { id: 'character-consistency', title: 'Character Consistency', description: '...', icon: Users },
  // ... add new entry here
  { id: 'new-feature', title: 'New Feature', description: '...', icon: Sparkles },
];
```

**Key details:**
- Each data file imports its TypeScript interface from `src/types/index.ts` (typed end-to-end).
- Icons are `LucideIcon` from `lucide-react` (NOT string names — direct component references).
- The array is immutable at runtime (const assertion not needed because the interface enforces the shape).

### Asset Pipeline (Media Files)

Media assets are NOT version-controlled in source form. They're downloaded/generated via scripts:

```bash
./scripts/download-assets.sh        # Download R2 workflow videos + posters (idempotent)
./scripts/generate-thumbnails.sh    # Generate 6 example thumbnails via z-ai CLI
```

**Asset locations:**
- `public/hero-bg.mp4` (46KB) — generated from `hero-poster.webp` via ffmpeg `zoompan`
- `public/hero-poster.webp` — poster for hero video
- `public/workflow/showcase-step{1-4}.mp4` + `showcase-step{1-4}-poster.webp` — workflow demo videos
- `public/examples/example-{1-6}.webp` (9:16 portrait) — example thumbnails
- `public/fonts/Outfit-VariableFont.woff2` (45KB) — self-hosted Outfit variable font
- `public/og-image.png` — Open Graph image (1200×630)

---

## 8. Accessibility (WCAG AAA) Implementation

### The 6 Accessibility Requirements

1. **Focus rings:** `focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-amber-400` on all interactive elements.

2. **Skip-to-content link** at page top (in `layout.tsx`):
   ```tsx
   <a
     href="#main"
     className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:rounded-md focus:bg-amber-400 focus:px-4 focus:py-2 focus:font-medium focus:text-zinc-950 focus:shadow-lg"
   >
     Skip to content
   </a>
   ```

3. **Hero video:** `aria-hidden="true"` (decorative, no audio). The `<video>` element has `muted` attribute.

4. **`prefers-reduced-motion: reduce`** — global CSS override disables ALL animations (see Section 4).

5. **Touch targets ≥ 44×44px** on mobile (WCAG 2.5.5). The ratio toggle buttons use `min-h-[44px] min-w-[44px]`.

6. **Color contrast:** zinc-300 on zinc-950 = 12.6:1 (WCAG AAA). Body text uses `text-zinc-300` (NOT `text-zinc-400` which is only 8.4:1).

### The `useReducedMotion` Hook

See Section 6 for implementation. Used in JS-level decisions:
- Skipping video autoplay
- Disabling JS-driven animations
- Conditionally rendering animation-heavy components

### Global CSS Reduced Motion Override

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
  .marquee-track { animation: none !important; }
  video[autoplay] { display: none; }
  [data-reveal] { opacity: 1 !important; transform: none !important; }
}
```

**Key detail:** `animation-duration: 0.01ms` (NOT `0ms`) — some browsers treat `0ms` as "use default". `0.01ms` is effectively instant but unambiguous.

### Semantic HTML Structure

```tsx
<html lang="en" suppressHydrationWarning>
  <body suppressHydrationWarning>
    <a href="#main" className="sr-only focus:not-sr-only ...">Skip to content</a>
    <Providers>
      <main id="main">
        {/* Page content */}
      </main>
    </Providers>
  </body>
</html>
```

**Key details:**
- `suppressHydrationWarning` on BOTH `<html>` and `<body>` — Grammarly extension injects attributes into `<body>` before React hydrates.
- `<main id="main">` — the skip-to-content link targets this.
- `lang="en"` on `<html>` — required for screen readers.

### ARIA Patterns Used

| Component | ARIA | Purpose |
|---|---|---|
| Aspect ratio toggle | `role="group" aria-label="Aspect ratio"` + `aria-pressed={isActive}` on each button | Toggle button group |
| FAQ accordion | Radix Accordion (handles `aria-expanded`, `aria-controls`, `role="region"` automatically) | Expand/collapse |
| Progress bar | `role="progressbar" aria-valuenow={percent} aria-valuemin={0} aria-valuemax={100}` | Live progress |
| Navbar | `<nav aria-label="Main">` | Navigation landmark |
| Hero video | `aria-hidden="true"` on wrapper `<div>` | Decorative |
| Carousel arrows | `aria-label="Previous examples"` / `aria-label="Next examples"` | Button purpose |

---

## 9. Anti-Patterns & Common Bugs

### Marketing Layer (Inherited from Clone)

1. **Pure black vs near-black:** Background is `#020202`, NOT `#000` or `#0a0a0a`. Using pure black breaks the luxury-dark aesthetic.

2. **Amber shade mismatch:** PRD amber `#febf00` ≠ Tailwind `amber-400` (`#fbbf24`). Use the custom `--color-primary` token, NOT `bg-amber-400`. The difference is visible — `#fbbf24` is slightly more orange.

3. **Outfit 820 unavailable from Google Fonts API:** Must self-host via `next/font/local`. `next/font/google` only serves discrete weights (100, 200, ..., 900).

4. **Feature grid uses hairline borders, not cards:** Continuous surface separated by `border-neutral-800`. Do NOT add `rounded-2xl` or `bg-card` to feature items — it breaks the design.

5. **Examples hover gradient is the ONLY purple:** `bg-gradient-to-r from-yellow-500 to-purple-500` on card hover. Do not add purple anywhere else.

6. **CTA hierarchy is deliberate:** Ghost link → glass pill → gradient pill → solid amber. Ration the accent — don't make every CTA solid amber.

7. **Geist Mono for ratio toggles, NOT Geist Sans:** `font-mono text-[10px]` for 9:16/16:9 buttons. This is a deliberate typographic contrast.

8. **`next lint` deprecated in Next.js 16:** Use `eslint .` directly. The `lint` script in `package.json` runs `eslint .`.

9. **shadcn CLI times out:** Primitives are hand-written in `src/components/ui/`, NOT CLI-generated. The CLI timed out during initial setup.

10. **Grammarly extension:** `suppressHydrationWarning` required on both `<html>` and `<body>`. Grammarly injects attributes into `<body>` before React hydrates.

11. **Workflow is `'use client'`:** Uses `useState` for poster→video fade-in choreography. Don't assume server components for "mostly static" sections.

12. **Playwright browsers:** `pnpm install` doesn't install browser binaries. Run `pnpm exec playwright install` separately.

### Production App Layer (Sprint 1-4)

13. **`verifySession()` must not be wrapped in try/catch:** It throws `NEXT_REDIRECT` which must propagate. Wrapping it silently swallows the redirect.

14. **`process.env.*` is forbidden:** Always import `env` from `@/lib/env`. The Zod schema validates at module load; typos like `GOOGLE_CLIENTID` (missing underscore) silently return `undefined` and disable OAuth.

15. **Zod `.url()` rejects `postgresql://`:** Use `.refine()` with a postgres scheme check for `DATABASE_URL`. Zod's URL validator rejects non-standard schemes.

16. **Build fails without env vars:** The env module has a build-context fallback (returns placeholders when `NEXT_PHASE === 'phase-production-build'` or `NODE_ENV === 'test'`). At runtime, real env vars MUST be set.

17. **DrizzleAdapter rejects Proxy-based db:** `DrizzleAdapter(db)` validates the db object's structure. Use a real Drizzle client, not a Proxy.

18. **Auth route handler must be `force-dynamic`:** Prevents prerender failure (DrizzleAdapter needs env vars at module load).

19. **Inngest v4 `createFunction` signature changed:** Trigger is in config object (`triggers: [{ event: '...' }]`), NOT a second argument.

20. **Stripe SDK v22+ uses camelCase:** `subscription.current_period_end` is now `subscription.currentPeriodEnd`. The webhook handler uses a fallback cast to support both.

21. **ElevenLabs `textToSpeech.convert()` returns a `Readable`:** NOT a `ReadableStream`. The `streamToBuffer` helper duck-types the input.

22. **Buffer → Blob requires `new Uint8Array(buffer)`:** `new File([audioBuffer], ...)` fails TypeScript strict types.

23. **`NODE_ENV` is read-only in tests:** Use `vi.stubEnv('NODE_ENV', 'test')` instead of direct assignment.

24. **Middleware runs on Edge runtime:** No Node.js APIs, no DB access. Only checks cookie presence.

25. **esbuild build scripts need approval:** `pnpm-workspace.yaml` must list `esbuild` under `onlyBuiltDependencies`.

### Remediation Sprint 1 (Pipeline Wiring + UX + Compliance)

26. **Vitest mock factories are hoisted above imports:** Use `vi.hoisted()` for any `vi.fn()` referenced inside the factory. Symptom: `Cannot access 'X' before initialization`.

27. **Mocked SDK constructors need `class` syntax:** `vi.fn().mockImplementation(() => ({ ... }))` returns an arrow function that cannot be `new`-ed. Use `class MockS3Client { send = sendMock; }`.

28. **`.tsx` extension is mandatory for test files containing JSX:** `render(<Component />)` in a `*.test.ts` file produces `[PARSE_ERROR]`. Rename to `*.test.tsx`.

29. **`fetch()` in the Inngest pipeline hits real DNS in tests:** Steps 5 and 6 download audio/SRT from R2 via `fetch()`. Stub globally: `vi.stubGlobal('fetch', fetchMock)`.

30. **SSE routes use `auth()` not `verifySession()`:** `verifySession()` throws redirect (wrong for JSON/SSE). API routes use `auth()` → null → 401 JSON.

31. **SSE polling vs. Postgres LISTEN/NOTIFY:** Serverless SSE can't hold a long-lived Postgres connection. Poll DB every 2s; close on terminal status.

32. **`EventSource` cleanup is critical:** `useEffect` must return a cleanup function that calls `eventSource.close()`.

33. **`getProject()` LEFT JOINs videos:** Returns `videoKey`, `subtitleKey` (nullable). Don't add a second DB round-trip.

34. **`putObject` for pipeline vs. `getSignedUploadUrl` for client uploads:** Pipeline steps have Buffer in memory → direct PUT. Client uploads use presigned URL.

35. **`assemble-video.ts` temp file lifecycle:** Writes SRT to `/tmp/siv-srt-<ts>.srt`, runs FFmpeg, reads MP4 into Buffer, `unlink`s both. Never leak temp files.

36. **`moderateImage` fail-open policy (T5):** Unknown Replicate output shapes return `flagged:false` with `moderationSkipped:true`. Env-configurable via `IMAGE_MODERATION_FAIL_OPEN` (default `true`; set to `false` for production fail-closed). A `console.warn` is emitted on every skip.

37. **husky `prepare` script uses `|| true`:** Prevents `pnpm install` from failing on first install. Don't remove.

38. **`lint-staged` runs on staged files only:** Not the whole codebase. Run the full quality gate manually before pushing.

39. **Source-reading tests must strip comments before regex:** `src.replace(/\/\*[\s\S]*?\*\//g, '').replace(/\/\/.*$/gm, '')` before regex-matching, else docblocks trigger false positives.

40. **Client components must NEVER import `@/lib/storage/r2` at module level:** The `r2.ts` module imports `env` which validates all 28 env vars at module load. In the browser, only `NEXT_PUBLIC_*` vars are available — all server-only vars are `undefined`, causing "Invalid environment variables" crash. Pattern: Server Component signs the URL via `getSignedDownloadUrl()`, passes as prop.

41. **`@ffmpeg-installer/ffmpeg` is incompatible with Turbopack:** Uses dynamic `require()` with runtime-constructed paths. Replaced with system FFmpeg binary via `getFfmpegPath()` helper.

### Remediation Sprint 2 (Post-Review Hardening)

42. **`trustHost: true` is mandatory for reverse-proxy deployments (T2):** Without it, Auth.js v5 falls back to `AUTH_URL` for callback URLs. If `AUTH_URL=http://localhost:3000` leaks to production, auth redirects resolve to localhost → `ERR_CONNECTION_REFUSED`. This was a P0 production outage.

43. **AUTH_URL ↔ NEXT_PUBLIC_APP_URL host-mismatch warning (T2):** The env module emits a `console.warn` at module load when the two hosts differ. With `trustHost: true` it's no longer fatal, but it should still be fixed.

44. **`OPENAI_API_KEY.startsWith('sk-')` is NOT too strict (T3):** Investigation revealed `sk-proj-*`, `sk-svcacct-*`, `sk-admin-*` all literally start with `sk-`. The original concern was unfounded. 5 regression-guard tests added.

45. **Hardcoded third-party model IDs are an operational liability (T4):** The placeholder `SDXL_IPADAPTER_MODEL` hash (`6f288a8d-7e5e-4f0c-8b3f-3e1f3e6e3e3e`) was a UUID-format string, not Replicate's 64-char hex SHA. Scene generation would have 404'd. Moving model IDs to env vars with format validation catches this class of bug at module load.

46. **Silent fail-open policies are dangerous (T5):** The original `moderateImage` returned `flagged:false` with no log when the output shape was unknown. Operators had no way to detect the bypass. Adding the `moderationSkipped` field + `console.warn` makes the bypass observable.

47. **SSE on Vercel needs both server-side and client-side resilience (T6):** Raising `maxDuration` from 300 → 900 covers Vercel Pro, but Vercel Hobby still caps at 300s. The client-side reconnect with exponential backoff (1s → 2s → 4s, max 3 attempts) handles the Hobby case gracefully. Both layers are needed.

48. **`putObject` needs a size guard (T7):** R2's hard limit is 5 GB, but function memory is the real constraint (typically 1-8 GB). A 4K FFmpeg output (~4 GB) would OOM the function before reaching R2. The `MAX_PUT_OBJECT_BYTES = 500 MB` cap fails fast with a clear `PayloadTooLargeError` instead of an opaque OOM.

49. **`pnpm-workspace.yaml` requires `packages:` field even for single-package repos (T0):** pnpm 9+ enforces this. Fresh clones fail with `ERR_PNPM_INVALID_WORKSPACE_CONFIGURATION  packages field missing or empty`. The fix is `packages: ['.']`.

50. **CI should run the full quality gate, not just lint-staged (T8):** lint-staged only checks staged files. A bad commit to `main` can pass locally and break production. The GitHub Actions workflow runs `pnpm lint && pnpm typecheck && pnpm test && pnpm build` on every PR.

---

## 10. Debugging Guide

### Step-by-Step Verification for Common Issues

#### Issue: Tailwind classes not applying

**Symptom:** Custom classes like `bg-primary` or `text-foreground` don't work. Elements appear unstyled.

**Verification steps:**
1. Check `postcss.config.mjs` uses `@tailwindcss/postcss` (NOT `tailwindcss`):
   ```bash
   cat postcss.config.mjs
   # Must show: '@tailwindcss/postcss': {}
   ```
2. Check `globals.css` has `@import 'tailwindcss';` at the top.
3. Check `globals.css` has `@source` directives for components/lib:
   ```bash
   grep '@source' src/app/globals.css
   # Must show:
   # @source '../components/**/*.{ts,tsx}';
   # @source '../lib/**/*.{ts,tsx}';
   ```
4. Check `@theme` block is present with all color tokens.

**Fix:** If any of the above are missing, restore from the canonical `globals.css`.

#### Issue: Build fails with "Invalid environment variables"

**Symptom:** `pnpm build` fails with a Zod error listing all 28 env vars as undefined.

**Verification steps:**
1. Check `.env.local` exists and has all required vars:
   ```bash
   test -f .env.local && echo "exists" || echo "missing"
   ```
2. Check `NEXT_PHASE` is set during build:
   ```bash
   NEXT_PHASE=phase-production-build pnpm build
   ```
3. The build-context fallback only activates when `NEXT_PHASE=phase-production-build` OR `NODE_ENV=test`.

**Fix:** Copy `.env.example` → `.env.local`, fill in real values. For build-only, set `NEXT_PHASE=phase-production-build`.

#### Issue: Auth redirects to `http://localhost:3000` in production

**Symptom:** Visiting `/dashboard` on the live site redirects to `http://localhost:3000/sign-in` → `ERR_CONNECTION_REFUSED`.

**Verification steps:**
1. Check `AUTH_URL` in production `.env.local`:
   ```bash
   grep AUTH_URL .env.local
   # Must show the production URL, not localhost
   ```
2. Check `trustHost: true` in `src/lib/auth/config.ts`:
   ```bash
   grep trustHost src/lib/auth/config.ts
   ```
3. Check the server log for the host-mismatch warning:
   ```bash
   # Should NOT see: [env] AUTH_URL host ("localhost:3000") differs from NEXT_PUBLIC_APP_URL host
   ```

**Fix (T2):** Set `AUTH_URL` to the production URL. The `trustHost: true` config makes Auth.js use the request's Host header as a fallback.

#### Issue: `pnpm install` fails with `ERR_PNPM_INVALID_WORKSPACE_CONFIGURATION`

**Symptom:** Fresh clone fails to install dependencies.

**Verification:**
```bash
cat pnpm-workspace.yaml
# Must contain: packages:
#   - '.'
```

**Fix (T0):** Add `packages: ['.']` to `pnpm-workspace.yaml`.

#### Issue: Project detail page shows "This page couldn't load"

**Symptom:** `/projects/[id]` crashes in the browser with "Invalid environment variables" in the console.

**Verification:**
```bash
# Check if any client component imports r2.ts at module level
grep -r "from '@/lib/storage/r2'" src/components/app/
# Should only return: src/components/app/signed-download-wrapper.tsx (Server Component)
```

**Fix:** Ensure client components (`'use client'`) never import `@/lib/storage/r2`. Use the `SignedDownloadWrapper` Server Component pattern instead.

#### Issue: `putObject` throws `PayloadTooLargeError`

**Symptom:** Pipeline fails at video assembly with "payload exceeds size limit".

**Verification:**
```bash
grep MAX_PUT_OBJECT_BYTES src/lib/storage/r2.ts
# Must show: export const MAX_PUT_OBJECT_BYTES = 500 * 1024 * 1024; // 500 MB
```

**Fix (T7):** If the video exceeds 500 MB, use multipart upload via `CreateMultipartUploadCommand` instead of `putObject`. The 500 MB cap is intentional — function memory is the real constraint.

#### Issue: SSE stream disconnects after 300s (Vercel Hobby)

**Symptom:** Progress bar stops updating mid-pipeline; "Live updates disconnected" message.

**Verification:**
```bash
grep maxDuration src/app/api/projects/\[id\]/progress/route.ts
# Must show: export const maxDuration = 900;
```

**Fix (T6):** Upgrade to Vercel Pro (cap = 900s) OR rely on client-side reconnect (1s/2s/4s backoff, max 3 attempts). The UI shows "Reconnecting to live updates…" during reconnect.

#### Issue: Replicate scene generation 404s

**Symptom:** Pipeline fails at Step 3 (scene generation) with a Replicate 404 error.

**Verification:**
```bash
grep REPLICATE_SDXL_IPADAPTER_MODEL .env.local
# If empty, the default is the SDXL base model (NOT IP-Adapter)
```

**Fix (T4):** Set `REPLICATE_SDXL_IPADAPTER_MODEL` env var to a real `lucataco/sdxl-ipadapter:<sha>` hash from replicate.com/explorer.

#### Issue: Tests fail with "Cannot access 'X' before initialization"

**Symptom:** Vitest throws `ReferenceError: Cannot access 'mockFn' before initialization`.

**Fix:** Use `vi.hoisted()`:
```typescript
const { mockFn } = vi.hoisted(() => ({ mockFn: vi.fn() }));
vi.mock('module', () => ({ x: mockFn }));
```

#### Issue: Tests fail with "X is not a constructor"

**Symptom:** `TypeError: () => ({...}) is not a constructor` when mocking SDK clients.

**Fix:** Use `class` syntax in the mock factory:
```typescript
vi.mock('@aws-sdk/client-s3', () => {
  class MockS3Client { send = sendMock; }
  return { S3Client: MockS3Client };
});
```

---

## 11. Pre-Ship Checklist

### Before Every Commit

```bash
# 1. Lint — zero warnings
pnpm lint

# 2. Typecheck — zero errors
pnpm typecheck

# 3. Unit tests — 259 tests pass
pnpm test

# 4. E2E tests — 48 tests pass (requires Playwright browsers)
pnpm test:e2e

# 5. Format check — all files use Prettier code style
pnpm format:check

# 6. Production build — zero errors
pnpm build
```

**Pre-commit hook:** husky + lint-staged automatically runs ESLint + Prettier on staged `.ts/.tsx` files via `.husky/pre-commit`. Run `pnpm install` to activate.

### Before Every Deploy

1. **Provision all external services** — Neon, Google OAuth, OpenAI, Replicate, ElevenLabs, R2 (3 buckets), Stripe, Inngest, Resend, Upstash, Sentry.

2. **Set `AUTH_URL` to the production URL** — e.g., `https://storyintovideo.jesspete.shop`. The `trustHost: true` config (T2) makes Auth.js use the request's Host header as a fallback, but AUTH_URL is still used for email magic links.

3. **Set `REPLICATE_SDXL_IPADAPTER_MODEL`** — the default is the SDXL base placeholder. Without a real `lucataco/sdxl-ipadapter:<sha>` hash, scene generation won't apply character consistency. (T4)

4. **Set `IMAGE_MODERATION_FAIL_OPEN=false` for production** — fail-closed is the recommended setting once the model output shape is known and stable. (T5)

5. **Run `pnpm drizzle-kit generate && pnpm drizzle-kit migrate`** — create the database schema.

6. **Configure Stripe products** — create 4 tiers (Free/Creator/Pro/Studio), update `PRICE_IDS` in `src/lib/stripe/client.ts`.

7. **Test the AI pipeline end-to-end** — sign up, paste a story, verify characters/scenes/video generate. This is the highest-risk validation.

8. **Run `pnpm install` to activate husky** — the `prepare` script sets up `.husky/pre-commit`. Verify the hook fires on your first commit.

### CI Verification (GitHub Actions)

The `.github/workflows/ci.yml` workflow runs on every PR and push to `main`:
- `pnpm lint`
- `pnpm typecheck`
- `pnpm test`
- `pnpm build` (with `NEXT_PHASE=phase-production-build`)

**If CI fails:** DO NOT merge the PR. Fix the issue locally, re-run the full quality gate, then push the fix.

### Visual Verification

1. **Marketing page** — visually indistinguishable from `storyintovideo.com` at 1440×900.
2. **Lighthouse scores** — ≥95 across Performance, Accessibility, Best Practices, SEO (marketing page).
3. **Mobile viewport** — layout correct at 375×812 (iPhone 12 mini).
4. **Reduced motion** — all animations disable when `prefers-reduced-motion: reduce` is set.
5. **Focus rings** — visible on all interactive elements when navigating via keyboard.

### Pre-Launch Checklist (from `PRODUCTION_READINESS_PLAN.md` §8)

- [ ] All 28+1 env vars set in `.env.local`
- [ ] Database migrations applied (`pnpm drizzle-kit migrate`)
- [ ] Stripe products configured (`PRICE_IDS` updated)
- [ ] Replicate IP-Adapter model hash set (`REPLICATE_SDXL_IPADAPTER_MODEL`)
- [ ] `AUTH_URL` matches `NEXT_PUBLIC_APP_URL` host
- [ ] `IMAGE_MODERATION_FAIL_OPEN=false` for production
- [ ] `FFMPEG_PATH` set (or default `/usr/bin/ffmpeg` works)
- [ ] R2 buckets created (`siv-uploads`, `siv-generated`, `siv-videos`)
- [ ] Google OAuth redirect URIs configured
- [ ] Stripe webhook endpoint configured
- [ ] Inngest webhook endpoint configured
- [ ] Playwright browsers installed (`pnpm exec playwright install`)
- [ ] All 4 quality gates pass (`pnpm lint && pnpm typecheck && pnpm test && pnpm build`)
- [ ] Visual verification of marketing page against live site
- [ ] Lighthouse ≥95 across all categories

---

## 12. Lessons Learnt & How to Avoid Them

### Marketing Layer (Inherited)

1. **`suppressHydrationWarning` belongs on `<body>`, not just `<html>`** — Browser extensions like Grammarly inject attributes into `<body>` before React hydrates.

2. **Workflow component needs `'use client'`** — Uses `useState` for poster→video fade-in choreography. Don't assume server components for "mostly static" sections.

3. **Test counts drift from plans** — MEP planned 6+3, actual is now 259 unit + 48 E2E. Always verify against `pnpm test` output.

4. **File structure evolves** — `components/primitives/`, `lib/hooks/`, `lib/data/` were created during build. Update docs as you build.

5. **Playwright needs separate install** — `pnpm install` doesn't install browser binaries.

### Production App Layer

6. **Zod `.url()` rejects `postgresql://`** — use `.refine()` for non-standard URL schemes.

7. **Env validation needs build-context fallback** — without it, `next build` fails during page-data collection.

8. **`postgres()` defers connection until first query** — allows eager db instantiation without breaking the build.

9. **DrizzleAdapter validates db object structure** — a Proxy-based lazy db was rejected; use a real Drizzle client.

10. **Inngest v4 changed `createFunction` signature** — trigger is now in the config object, not a second argument.

11. **Auth unit tests must mock `next-auth` + `next/navigation`** — jsdom can't load `next/server`.

12. **Source-reading tests are valid** for server-only modules (auth config, middleware, route handlers) that can't be rendered in jsdom.

13. **Stripe SDK v22 camelCase breaking change** — `currentPeriodEnd` not `current_period_end`.

14. **ElevenLabs returns `Readable`, not `ReadableStream`** — duck-type the input in `streamToBuffer`.

15. **TDD with mocked AI providers works well** — all 8 pipeline domain functions are fully unit-tested; real API calls only needed for manual E2E validation.

### Remediation Sprint 1 (Pipeline Wiring + UX + Compliance)

16. **Vitest mock hoisting is the #1 test bug** — `vi.mock()` factories are hoisted above imports. Use `vi.hoisted()` for shared `vi.fn()` state.

17. **Mock constructors must be `class`, not arrow fns** — `new S3Client(...)` requires `new`-able mock. Arrow fns throw `"X is not a constructor"`.

18. **`.tsx` extension is mandatory for JSX tests** — oxc throws parse error for JSX in `*.test.ts`. Rename to `*.test.tsx`.

19. **SSE in Next.js 16** — `ReadableStream` + `text/event-stream` content-type + 2s DB polling. Simpler than Postgres LISTEN/NOTIFY for serverless.

20. **`auth()` vs `verifySession()` for API routes** — `verifySession()` throws redirect (wrong for JSON). API routes use `auth()` → null → 401 JSON.

21. **`EventSource` cleanup is non-negotiable** — `useEffect` must return `() => eventSource.close()`.

22. **Image moderation via Replicate safety output is preferred** — parsing `safety_concept` / `api_safety_concept` adds zero latency/cost vs. a second OpenAI vision moderation API call.

23. **`getProject()` LEFT JOIN videos is cheaper than two queries** — LEFT JOIN adds <1ms; second query adds 5-15ms.

24. **`putObject` (pipeline) vs `getSignedUploadUrl` (client)** — pipeline has Buffer in memory → direct PUT. Client uploads use presigned URL.

25. **TDD exposed 4 latent defects in `assemble-video.ts`** — placeholder Buffer, missing SRT write, missing input options, brittle filter extraction. All discoverable only by writing tests first.

26. **Source-reading tests must strip comments** — `src.replace(/\/\*[\s\S]*?\*\//g, '').replace(/\/\/.*$/gm, '')` before regex, else docblocks trigger false positives.

27. **husky `prepare` script with `|| true` is intentional** — prevents `pnpm install` failure on first install.

28. **Client components must NEVER import `r2.ts` at module level** — the `r2.ts` module imports `env` which validates all 28 env vars at module load. In the browser, only `NEXT_PUBLIC_*` vars exist.

29. **Server-side URL signing pattern** — for any client component that needs data from server-only env vars, the Server Component should fetch/compute the value and pass it as a prop.

30. **`@ffmpeg-installer/ffmpeg` is incompatible with Turbopack** — replaced with system FFmpeg binary via `getFfmpegPath()`.

31. **`middleware.ts` renamed to `proxy.ts` in Next.js 16** — functionality identical, only filename changes.

### Remediation Sprint 2 (Post-Review Hardening)

32. **`trustHost: true` is mandatory for reverse-proxy deployments** — without it, Auth.js v5 falls back to `AUTH_URL` for callback URLs. This was a P0 production outage. (T2)

33. **AUTH_URL ↔ NEXT_PUBLIC_APP_URL host-mismatch is a leading indicator of misconfiguration** — the env module emits a `console.warn` at module load when the two hosts differ. (T2)

34. **`OPENAI_API_KEY.startsWith('sk-')` is NOT too strict** — `sk-proj-*`, `sk-svcacct-*`, `sk-admin-*` all literally start with `sk-`. The original concern was unfounded. 5 regression-guard tests added. (T3)

35. **Hardcoded third-party model IDs are an operational liability** — the placeholder `SDXL_IPADAPTER_MODEL` hash was a UUID-format string, not Replicate's 64-char hex SHA. Scene generation would have 404'd. (T4)

36. **Silent fail-open policies are dangerous** — the original `moderateImage` returned `flagged:false` with no log when the output shape was unknown. Adding the `moderationSkipped` field + `console.warn` makes the bypass observable. (T5)

37. **SSE on Vercel needs both server-side and client-side resilience** — raising `maxDuration` from 300 → 900 covers Vercel Pro. The client-side reconnect handles Vercel Hobby's 300s cap. Both layers are needed. (T6)

38. **`putObject` needs a size guard** — R2's limit is 5 GB, but function memory is the real constraint. The `MAX_PUT_OBJECT_BYTES = 500 MB` cap fails fast with a clear error. (T7)

39. **`pnpm-workspace.yaml` requires `packages:` field even for single-package repos** — pnpm 9+ enforces this. (T0)

40. **CI should run the full quality gate, not just lint-staged** — lint-staged only checks staged files. The GitHub Actions workflow runs the full quality gate on every PR. (T8)

---

## 13. Pitfalls to Avoid

### Architecture Pitfalls

- **Do not add `tailwind.config.ts`** — all tokens belong in `globals.css` `@theme` block.
- **Do not use `force-static` on app routes** — only the marketing page can be static.
- **Do not use `any`** — ESLint will error. Use `unknown` or proper types.
- **Do not add CDN links** — all assets are self-hosted.
- **Do not use default exports for components** — use named exports.
- **Do not skip the verification chain** — `pnpm lint && pnpm typecheck && pnpm test && pnpm build`.
- **Do not use `db push` in production** — always `drizzle-kit generate` + `migrate`.
- **Do not make R2 buckets public** — use signed URLs.
- **Do not skip content moderation** — every story input must be moderated (ADR-011).

### TypeScript Pitfalls

- **Do not use `any`** — use `unknown` instead. ESLint enforces `@typescript-eslint/no-explicit-any: error`.
- **Do not forget `import type`** — `verbatimModuleSyntax: true` requires it for type-only imports.
- **Do not access arrays without null checks** — `noUncheckedIndexedAccess: true` means `arr[0]` is `T | undefined`.
- **Do not use `as any`** — use `as unknown as Type` if you must cast (last resort).

### React/Next.js Pitfalls

- **Do not import `r2.ts` in client components** — env validation throws in browser. Use server-side URL signing.
- **Do not wrap `verifySession()` in try/catch** — it throws `NEXT_REDIRECT` which must propagate.
- **Do not use `verifySession()` in API routes** — use `auth()` directly (returns null → 401 JSON).
- **Do not forget `suppressHydrationWarning`** — on both `<html>` and `<body>` (Grammarly compatibility).
- **Do not use `<a>` for internal navigation** — use `next/link`.
- **Do not use `process.env.*` directly** — always import `env` from `@/lib/env`.

### Testing Pitfalls

- **Do not write JSX in `*.test.ts` files** — rename to `*.test.tsx` (oxc requires it).
- **Do not reference outer `vi.fn()` in `vi.mock()` factories** — use `vi.hoisted()`.
- **Do not mock SDK constructors with arrow functions** — use `class` syntax.
- **Do not forget to stub `fetch` in pipeline tests** — Steps 5 & 6 use `fetch()` for R2 downloads.
- **Do not forget to strip comments in source-reading tests** — docblocks trigger false positives.

### Deployment Pitfalls

- **Do not deploy without `AUTH_URL` set to the production URL** — `trustHost: true` is a fallback, not a replacement.
- **Do not deploy without `REPLICATE_SDXL_IPADAPTER_MODEL`** — the default is a placeholder; scene generation won't apply character consistency.
- **Do not deploy with `IMAGE_MODERATION_FAIL_OPEN=true`** — set to `false` for production fail-closed.
- **Do not deploy without running the full quality gate** — CI catches what lint-staged misses.

---

## 14. Best Practices

### Code Organization

1. **5-layer architecture** — proxy → app → features → domain → lib. Lower layers never import from higher layers.
2. **`queries.ts` boundary** — all DB access through feature-level `queries.ts` files. Components never call `db` directly.
3. **Domain isolation** — pure business logic in `src/features/*/domain/` (no Next.js or DB runtime imports, `import type` only).
4. **Server Actions start with `verifySession()`** — before any other logic.
5. **API routes use `auth()` directly** — returns null → 401 JSON (NOT `verifySession()` which redirects).

### TypeScript

6. **`interface` for object shapes, `type` for unions/intersections.**
7. **Explicit `import type`** for type-only imports (required by `verbatimModuleSyntax`).
8. **Early returns** over deeply nested conditionals.
9. **Composition over inheritance.**
10. **`unknown` instead of `any`** — always.

### React/Next.js

11. **Server Components by default** — add `'use client'` only when using `useState`, `useEffect`, event handlers, or browser APIs.
12. **Named function exports** — `export function ComponentName()`, never default exports.
13. **`next/image` for all raster images** — enables optimization.
14. **`next/font` for all fonts** — no CDN links.
15. **`next/link` for all internal navigation** — never `<a>`.

### Testing

16. **TDD: RED → GREEN → REFACTOR** — one cycle per logical change.
17. **Mock AI provider SDKs** — never make real API calls in tests.
18. **Mock `@/lib/db`** — jsdom can't reach Postgres.
19. **Mock `next-auth`, `next/navigation`** — jsdom can't load `next/server`.
20. **Source-reading tests for server-only modules** — auth config, proxy, route handlers.
21. **Strip comments before regex** — `src.replace(/\/\*[\s\S]*?\*\//g, '').replace(/\/\/.*$/gm, '')`.

### Performance

22. **CSS-only animations** — no Framer Motion, no GSAP. All 13 keyframes in `globals.css`.
23. **`prefers-reduced-motion: reduce`** — global override disables all animation.
24. **Videos preload `metadata` only** — not `auto`.
25. **Lighthouse ≥95** — Performance, Accessibility, Best Practices, SEO (marketing page).
26. **JS bundle <150KB gzipped** — app adds auth/db/ai client code on top of marketing.
27. **CSS bundle <30KB gzipped**.

### Security

28. **Zod env validation** — never `process.env.*` directly.
29. **Auth-first Server Actions** — `verifySession()` before any logic.
30. **Owner-checked queries** — `getProject()` returns null if not owner.
31. **Signed URLs** — R2 buckets are private; 1-hour signed URLs for access.
32. **Security headers** — X-Frame-Options DENY, nosniff, strict referrer, Permissions-Policy.
33. **`trustHost: true`** — Auth.js uses request's Host header (prevents localhost redirect in production).
34. **`MAX_PUT_OBJECT_BYTES = 500 MB`** — putObject size guard prevents OOM.

---

## 15. Coding Patterns

### Pattern: Server-Side URL Signing (T1)

**Problem:** Client components need data from server-only env vars (R2 signed URLs, Stripe secrets).

**Solution:** Server Component fetches/computes the value, passes as prop to Client Component.

```tsx
// Server Component (NO 'use client')
import { getSignedDownloadUrl } from '@/lib/storage/r2';

export async function SignedDownloadWrapper({ videoKey }: Props) {
  const downloadUrl = await getSignedDownloadUrl('videos', videoKey);
  return <ClientComponent downloadUrl={downloadUrl} />;
}

// Client Component ('use client')
'use client';
export function ClientComponent({ downloadUrl }: { downloadUrl: string }) {
  return <a href={downloadUrl}>Download</a>;
}
```

### Pattern: Auth-First Server Action

```typescript
'use server';

export async function createProjectAction(input: z.infer<typeof Schema>) {
  // 1. AUTH FIRST
  const session = await verifySession({ redirectTo: '/create' });
  const userId = session.user?.id;
  if (!userId) return { success: false, code: 'UNAUTHORIZED' };

  // 2. ZOD VALIDATE
  const parsed = Schema.safeParse(input);
  if (!parsed.success) return { success: false, code: 'VALIDATION' };

  // 3. BUSINESS LOGIC
  // ...
}
```

### Pattern: API Route with `auth()` (NOT `verifySession()`)

```typescript
export async function GET(req: NextRequest) {
  const session = await auth();
  if (!session?.user?.id) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }
  // ...
}
```

### Pattern: `queries.ts` Boundary

```typescript
// src/features/projects/queries.ts
export async function getProject(projectId: string, userId: string) {
  const [row] = await db
    .select({ ... })
    .from(projects)
    .leftJoin(videos, eq(videos.projectId, projects.id))
    .where(eq(projects.id, projectId))
    .limit(1);

  // Owner check — returns null if not owner
  if (row && row.userId !== userId) return null;
  return row;
}
```

### Pattern: Domain Isolation (Pure Functions)

```typescript
// src/features/pipeline/domain/analyze-story.ts
// NO Next.js imports, NO DB imports — only types
import type { Project } from '@/lib/db/schema';

export async function analyzeStory(story: string): Promise<AnalysisResult> {
  // Pure business logic — no side effects
}
```

### Pattern: SSE with Polling + Reconnect (T6)

```typescript
// Server: poll DB every 2s, close on terminal status
const interval = setInterval(async () => {
  const current = await readProjectProgress(projectId);
  controller.enqueue(encoder.encode(formatSseMessage(current)));
  if (TERMINAL_STATUSES.has(current.status)) {
    controller.close();
    clearInterval(interval);
  }
}, 2000);

// Client: reconnect with exponential backoff
eventSource.onerror = () => {
  eventSource?.close();
  if (reconnectAttempt >= MAX_RECONNECT_ATTEMPTS) {
    setState((prev) => ({ ...prev, connectionState: 'error' }));
    return;
  }
  const delay = backoffDelay(reconnectAttempt); // 1s → 2s → 4s
  reconnectAttempt += 1;
  setState((prev) => ({ ...prev, connectionState: 'reconnecting' }));
  reconnectTimer = setTimeout(() => openStream(), delay);
};
```

### Pattern: Env-Configurable Constants with Format Validation (T4)

```typescript
// In src/lib/env/index.ts
REPLICATE_SDXL_MODEL: z
  .string()
  .regex(/^[a-z0-9-]+\/[a-z0-9-]+:[a-f0-9]{8,}$/, 'Must match owner/model:sha format')
  .default('stability-ai/sdxl:39ed52f2...'),

// In src/lib/ai/replicate.ts
export const SDXL_MODEL = env.REPLICATE_SDXL_MODEL as `${string}/${string}:${string}`;
```

### Pattern: Observable Fail-Open Policy (T5)

```typescript
const FAIL_OPEN = (process.env.IMAGE_MODERATION_FAIL_OPEN ?? 'true').toLowerCase() !== 'false';

if (moderationSkipped && !FAIL_OPEN) {
  console.warn(`[moderate-image] FAIL-CLOSED: unknown output shape for ${input.imageUrl}`);
  return { flagged: true, categories: ['unknown-output-shape'], moderationSkipped: true };
}

if (moderationSkipped) {
  console.warn(`[moderate-image] Skipped: unknown output shape for ${input.imageUrl}`);
}

return { flagged: categories.length > 0, categories, moderationSkipped };
```

### Pattern: `cn()` Utility for Conditional Classes

```typescript
import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}

// Usage:
<div className={cn('base classes', isActive && 'active classes', className)} />
```

### Pattern: ScrollReveal with Stagger Delay

```tsx
<ScrollReveal delay={100}>
  <Card />
</ScrollReveal>
<ScrollReveal delay={200}>
  <Card />
</ScrollReveal>
<ScrollReveal delay={300}>
  <Card />
</ScrollReveal>
```

---

## 16. Coding Anti-Patterns

### Anti-Pattern: Importing `r2.ts` in Client Components

```tsx
// ❌ WRONG — crashes in browser
'use client';
import { getSignedDownloadUrl } from '@/lib/storage/r2'; // env validation throws

export function DownloadButton({ videoKey }: { videoKey: string }) {
  const [url, setUrl] = useState('');
  useEffect(() => {
    getSignedDownloadUrl('videos', videoKey).then(setUrl); // 💥 CRASH
  }, [videoKey]);
  return <a href={url}>Download</a>;
}
```

```tsx
// ✅ CORRECT — server-side signing
// Server Component
import { getSignedDownloadUrl } from '@/lib/storage/r2';
export async function Wrapper({ videoKey }: { videoKey: string }) {
  const url = await getSignedDownloadUrl('videos', videoKey);
  return <DownloadButton downloadUrl={url} />;
}

// Client Component
'use client';
export function DownloadButton({ downloadUrl }: { downloadUrl: string }) {
  return <a href={downloadUrl}>Download</a>;
}
```

### Anti-Pattern: Wrapping `verifySession()` in try/catch

```typescript
// ❌ WRONG — swallows the redirect
'use server';
export async function action() {
  try {
    const session = await verifySession();
    // ...
  } catch (e) {
    // NEXT_REDIRECT is caught here — user stays on page, no redirect happens
  }
}
```

```typescript
// ✅ CORRECT — let it propagate
'use server';
export async function action() {
  const session = await verifySession(); // throws NEXT_REDIRECT if unauthenticated
  // ...
}
```

### Anti-Pattern: Using `verifySession()` in API Routes

```typescript
// ❌ WRONG — throws redirect (wrong for JSON)
export async function GET() {
  const session = await verifySession(); // throws NEXT_REDIRECT
  return NextResponse.json({ data });
}
```

```typescript
// ✅ CORRECT — use auth() directly
export async function GET() {
  const session = await auth();
  if (!session?.user?.id) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }
  return NextResponse.json({ data });
}
```

### Anti-Pattern: `process.env.*` Direct Access

```typescript
// ❌ WRONG — typos silently return undefined
const apiKey = process.env.OPENAI_APIKEY; // Missing underscore — undefined!
```

```typescript
// ✅ CORRECT — Zod-validated env module
import { env } from '@/lib/env';
const apiKey = env.OPENAI_API_KEY; // Typos fail at module load
```

### Anti-Pattern: Arrow Function Mock Constructors

```typescript
// ❌ WRONG — throws "X is not a constructor"
vi.mock('@aws-sdk/client-s3', () => ({
  S3Client: vi.fn(() => ({ send: vi.fn() })), // arrow fn can't be `new`-ed
}));
```

```typescript
// ✅ CORRECT — use class syntax
vi.mock('@aws-sdk/client-s3', () => {
  class MockS3Client { send = vi.fn(); }
  return { S3Client: MockS3Client };
});
```

### Anti-Pattern: Missing `vi.hoisted()` for Mock Factories

```typescript
// ❌ WRONG — "Cannot access 'mockFn' before initialization"
const mockFn = vi.fn();
vi.mock('module', () => ({ x: mockFn })); // mockFn is undefined here (hoisted)
```

```typescript
// ✅ CORRECT — use vi.hoisted()
const { mockFn } = vi.hoisted(() => ({ mockFn: vi.fn() }));
vi.mock('module', () => ({ x: mockFn }));
```

### Anti-Pattern: JSX in `.test.ts` Files

```typescript
// ❌ WRONG — oxc parse error in *.test.ts
import { render } from '@testing-library/react';
render(<Component />); // [PARSE_ERROR] Expected '>' but found 'Identifier'
```

```typescript
// ✅ CORRECT — rename to *.test.tsx
// File: src/tests/unit/component.test.tsx
import { render } from '@testing-library/react';
render(<Component />); // Works!
```

### Anti-Pattern: `any` Type

```typescript
// ❌ WRONG — ESLint error
function process(data: any) { // error: Unexpected any
  return data.foo;
}
```

```typescript
// ✅ CORRECT — use unknown
function process(data: unknown) {
  if (typeof data === 'object' && data !== null && 'foo' in data) {
    return (data as { foo: string }).foo;
  }
  return null;
}
```

---

## 17. Responsive Breakpoint Reference

### Tailwind v4 Default Breakpoints

| Token | Min Width | Target Device |
|---|---|---|
| (default) | 0 | Mobile portrait 375px |
| `sm` | 640px | Mobile landscape / small tablet |
| `md` | 768px | Tablet portrait (iPad) |
| `lg` | 1024px | Tablet landscape / laptop |
| `xl` | 1280px | Desktop (matches `max-w-7xl`) |
| `2xl` | 1536px | Large desktop |

### Breakpoint Usage Patterns

```tsx
// H1 — fluid scaling
<h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-[4.5rem]">

// Section padding — mobile-first
<section className="px-6 py-16 sm:px-8 lg:px-12 lg:py-24">

// Grid — responsive columns
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4">

// Hide/show — mobile vs desktop
<div className="hidden sm:flex">Desktop nav</div>
<button className="sm:hidden">Mobile hamburger</button>

// Max width — content container
<div className="mx-auto max-w-3xl">Narrow content</div>
<div className="mx-auto max-w-7xl">Wide content</div>
```

### Mobile-First Rules

1. **Default (no prefix) = mobile styles.** Add `sm:`, `md:`, etc. for larger screens.
2. **Touch targets ≥ 44×44px** on mobile (WCAG 2.5.5). Use `min-h-[44px] min-w-[44px]`.
3. **Mobile nav uses Sheet** (right-side drawer), NOT a hamburger menu.
4. **Marquee speed increases on mobile** (`animation-duration: 30s` in `@media (max-width: 640px)`).

---

## 18. Z-Index Layer Map

| Z-Index | Element | Context |
|---|---|---|
| `z-0` | Hero background video + overlays | Behind hero content |
| `z-0` | Hero bottom fade | Behind next section |
| `z-10` | Hero content (eyebrow, H1, glass input, marquee) | Above background video |
| `z-50` | Navbar (fixed) | Above all page content |
| `z-50` | Skip-to-content link (when focused) | Above navbar |
| `z-50` | Mobile Sheet (Radix Dialog) | Above navbar |
| `z-50` | Dropdown menu (Radix DropdownMenu) | Above navbar |

### Rules

1. **`z-50` is the maximum** — reserved for fixed/sticky elements (navbar, modals, dropdowns).
2. **`z-10` is for content above backgrounds** — hero content above hero video.
3. **`z-0` is for backgrounds** — hero video, bottom fades.
4. **Do NOT use `z-[100]` or arbitrary z-index values** — stick to the scale.
5. **Radix components manage their own z-index** — Sheet and DropdownMenu use `z-50` internally.

---

## 19. Color Reference (Complete)

### Primary Palette (from `@theme` block)

| Token | Hex | RGB | Usage |
|---|---|---|---|
| `--color-background` | `#020202` | `rgb(2, 2, 2)` | Page background (near-black, NOT pure #000) |
| `--color-foreground` | `#f8f8f8` | `rgb(248, 248, 248)` | Default foreground text |
| `--color-card` | `#060607` | `rgb(6, 6, 7)` | Card surfaces |
| `--color-card-foreground` | `#f8f8f8` | `rgb(248, 248, 248)` | Text on cards |
| `--color-popover` | `#0b0b0d` | `rgb(11, 11, 13)` | Popover backgrounds |
| `--color-popover-foreground` | `#f8f8f8` | `rgb(248, 248, 248)` | Text on popovers |
| `--color-primary` | `#febf00` | `rgb(254, 191, 0)` | CTAs, active states, focus rings, accents |
| `--color-primary-foreground` | `#020202` | `rgb(2, 2, 2)` | Text on primary (near-black) |
| `--color-secondary` | `#111114` | `rgb(17, 17, 20)` | Secondary surfaces |
| `--color-secondary-foreground` | `#f8f8f8` | `rgb(248, 248, 248)` | Text on secondary |
| `--color-muted` | `#1a1a1d` | `rgb(26, 26, 29)` | Muted backgrounds |
| `--color-muted-foreground` | `#8e8e95` | `rgb(142, 142, 149)` | Muted text (zinc-400 equivalent) |
| `--color-accent` | `#febf00` | `rgb(254, 191, 0)` | Accent (same as primary) |
| `--color-accent-foreground` | `#020202` | `rgb(2, 2, 2)` | Text on accent |
| `--color-destructive` | `#ff2d39` | `rgb(255, 45, 57)` | Error/destructive states |
| `--color-destructive-foreground` | `#f8f8f8` | `rgb(248, 248, 248)` | Text on destructive |
| `--color-border` | `#1a1a1d` | `rgb(26, 26, 29)` | Default borders |
| `--color-input` | `#0b0b0d` | `rgb(11, 11, 13)` | Input backgrounds |
| `--color-ring` | `#febf0080` | `rgba(254, 191, 0, 0.5)` | Focus ring (semi-transparent amber) |

### Chart Palette (Reserved for Future Dashboard)

| Token | Hex | Usage |
|---|---|---|
| `--color-chart-1` | `#febf00` | Amber (matches primary) |
| `--color-chart-2` | `#00aa6f` | Green |
| `--color-chart-3` | `#8d92f9` | Periwinkle |
| `--color-chart-4` | `#f14d4c` | Red |
| `--color-chart-5` | `#7bc27e` | Light green |

### Zinc Grayscale (Tailwind Built-in — Used Extensively)

| Token | Hex | Usage |
|---|---|---|
| `zinc-300` | `#d4d4d8` | Body text (12.6:1 contrast on zinc-950 = WCAG AAA) |
| `zinc-400` | `#a1a1aa` | Secondary text (8.4:1 contrast = WCAG AAA) |
| `zinc-500` | `#71717a` | Tertiary text, metadata |
| `zinc-600` | `#52525b` | Inactive states |
| `zinc-800` | `#27272a` | Glass gradient start |
| `zinc-900` | `#18181b` | Glass gradient end |
| `zinc-950` | `#09090b` | Section backgrounds (used interchangeably with `#020202`) |

### The Singular Purple Exception

| Context | Class | Hex Values |
|---|---|---|
| Examples card hover | `bg-gradient-to-r from-yellow-500 to-purple-500` | `#eab308` → `#a855f7` |

**This is the ONLY purple on the entire site.** Do not add purple anywhere else.

### Amber Shade Comparison (Critical)

| Name | Hex | Source |
|---|---|---|
| PRD amber (CORRECT) | `#febf00` | `--color-primary` in `@theme` |
| Tailwind `amber-400` (WRONG) | `#fbbf24` | Tailwind built-in |

**These are different colors.** `#fbbf24` is slightly more orange than `#febf00`. Always use `bg-primary` / `text-primary` / `outline-primary`, NOT `bg-amber-400` / `text-amber-400` / `outline-amber-400`.

**Exception:** Focus rings use `outline-amber-400` in the Button component because the difference is invisible to the eye at focus-ring scale.

### Opacity Variants (Used in Components)

| Pattern | Example | Purpose |
|---|---|---|
| `bg-white/[0.06]` | Hero story chips | Subtle white overlay |
| `bg-white/[0.08]` | Glass input border | Subtle border |
| `bg-white/[0.1]` | Active ratio toggle | Active state |
| `bg-amber-400/10` | Eyebrow badge | Amber tint |
| `bg-amber-400/30` | Radial glow | Amber glow |
| `bg-zinc-950/70` | Navbar scrolled | Semi-transparent dark |
| `bg-zinc-950/85` | Hero scrim | Dark overlay on video |

---

## 20. The Complete TypeScript Interface Reference

All 12 marketing interfaces live in `src/types/index.ts`:

### `NavLink`

```typescript
export interface NavLink {
  label: string;
  href: string;
}
```

### `StoryExample`

```typescript
export interface StoryExample {
  label: string;
  /** The multi-paragraph seed text injected into the textarea on click. */
  seed: string;
}
```

### `AspectRatio`

```typescript
export interface AspectRatio {
  label: '9:16' | '16:9';
  value: 'portrait' | 'landscape';
}
```

### `ExampleCard`

```typescript
export interface ExampleCard {
  id: string;
  title: string;
  /** Style tag shown below the title (e.g., "Anime · Romance"). */
  styleTag: string;
  /** Path to the 9:16 WebP thumbnail in /public/examples/. */
  thumbnail: string;
  href: string;
}
```

### `WorkflowStep`

```typescript
export interface WorkflowStep {
  number: 1 | 2 | 3 | 4;
  title: string;
  description: string;
  ctaLabel: string;
  ctaHref: string;
  /** Path to the looping MP4 demo in /public/workflow/. */
  videoSrc: string;
  /** Path to the WebP poster shown before the video loads. */
  videoPoster: string;
  /** Desktop layout: which side the media sits on. Mobile always stacks media-above-text. */
  mediaPosition: 'left' | 'right';
}
```

### `Feature`

```typescript
import type { LucideIcon } from 'lucide-react';

export interface Feature {
  id: string;
  title: string;
  description: string;
  icon: LucideIcon;
}
```

### `Testimonial`

```typescript
export interface Testimonial {
  id: string;
  quote: string;
  authorName: string;
  authorRole: string;
  /** 2-letter initials rendered in the amber gradient avatar (e.g., "SK"). */
  initials: string;
}
```

### `UseCase`

```typescript
export interface UseCase {
  id: string;
  title: string;
  description: string;
  icon: LucideIcon;
  href: string;
}
```

### `FAQItem`

```typescript
export interface FAQItem {
  id: string;
  question: string;
  answer: string;
}
```

### `FooterLink`

```typescript
export interface FooterLink {
  label: string;
  href: string;
}
```

### `FooterColumn`

```typescript
export interface FooterColumn {
  title: string;
  links: FooterLink[];
}
```

### `StyleChip`

```typescript
export interface StyleChip {
  label: string;
  /** Optional smaller sublabel (only "Cyberpunk" uses this: "Futuristic neon"). */
  sublabel?: string;
}
```

### Production App Interfaces (Key Ones)

#### `ProjectProgressState` (T6 — with `reconnecting`)

```typescript
export interface ProjectProgressState {
  status: string | null;
  progressPercent: number | null;
  progressDetail: string | null;
  errorMessage: string | null;
  connectionState: 'connecting' | 'open' | 'closed' | 'error' | 'reconnecting';
}
```

#### `ImageModerationResult` (T5 — with `moderationSkipped`)

```typescript
export interface ImageModerationResult {
  flagged: boolean;
  categories: string[];
  /**
   * true when moderation could not run because the output shape was unknown.
   * Operators should monitor this — a high rate indicates the model is
   * bypassing moderation entirely.
   */
  moderationSkipped: boolean;
}
```

#### `TierLimit` (Billing)

```typescript
export type Plan = 'free' | 'creator' | 'pro' | 'studio';

export interface TierLimit {
  plan: Plan;
  monthlyCredits: number;
  maxResolution: '720p' | '1080p' | '4k';
  maxVideoDurationSec: number;
  watermark: boolean;
  priorityQueue: boolean;
}
```

#### `CreateProjectResult` (Server Action)

```typescript
export type CreateProjectResult =
  | { success: true; projectId: string }
  | {
      success: false;
      error: string;
      code: 'UNAUTHORIZED' | 'VALIDATION' | 'FLAGGED' | 'INSUFFICIENT_CREDITS' | 'INTERNAL';
    };
```

#### `AssembleVideoInput` (Pipeline)

```typescript
export interface AssembleVideoInput {
  sceneImageUrls: string[];
  sceneDurations: number[]; // seconds per scene
  audioUrl: string;
  subtitlesSrt: string;
  aspectRatio: 'portrait' | 'landscape';
  resolution: '720p' | '1080p' | '4k';
}
```

---

## 21. Validation Matrix

This matrix verifies that this SKILL.md matches the actual codebase. Run these checks after any update.

| # | Validation Point | How to Verify | Expected Result |
|---|---|---|---|
| 1 | **Tech stack versions match** | `rg '"(next\|react\|tailwindcss\|next-auth\|drizzle-orm\|inngest\|openai\|replicate\|elevenlabs\|stripe)":' package.json` | Versions match Section 2 table |
| 2 | **Configuration files match** | `test -f next.config.ts postcss.config.mjs eslint.config.mjs tsconfig.json pnpm-workspace.yaml .github/workflows/ci.yml` | All 6 files exist |
| 3 | **Design system tokens match** | `rg '^\s+--color-(background\|primary\|card\|muted\|accent\|destructive\|border\|input\|ring):' src/app/globals.css` | 10 color tokens match Section 4 |
| 4 | **Component architecture matches** | `ls src/components/primitives/ src/components/sections/ src/components/ui/ src/components/app/` | 7 + 10 + 4 + 8 = 29 components |
| 5 | **Hooks implementation matches** | `ls src/lib/hooks/` | 4 hooks: use-scrolled, use-reveal, use-reduced-motion, use-project-progress |
| 6 | **Content ingestion patterns match** | `ls src/lib/data/` | 10 data files (NOT import.meta.glob — this is Next.js) |
| 7 | **Accessibility implementation matches** | `rg 'suppressHydrationWarning' src/app/layout.tsx` + `rg 'prefers-reduced-motion' src/app/globals.css` | Both present |
| 8 | **Anti-patterns are documented correctly** | `rg 'trustHost\|MAX_PUT_OBJECT_BYTES\|MAX_RECONNECT_ATTEMPTS\|IMAGE_MODERATION_FAIL_OPEN' storyintovideo_SKILL.md` | All 4 Sprint 2 fixes mentioned |
| 9 | **Color references match** | `rg '#febf00\|#020202\|#060607\|#8e8e95\|#f8f8f8\|#d4d4d8' storyintovideo_SKILL.md` | All 6 core hex values present |
| 10 | **TypeScript interfaces match** | `rg '^export interface' src/types/index.ts \| wc -l` | 12 interfaces |

### Automated Validation Script

```bash
#!/bin/bash
# Run this after updating SKILL.md to verify accuracy

set -e

echo "=== 1. Tech stack versions ==="
rg '"(next|react|tailwindcss|next-auth|drizzle-orm|inngest|openai|replicate|elevenlabs|stripe)":' package.json

echo ""
echo "=== 2. Config files ==="
for f in next.config.ts postcss.config.mjs eslint.config.mjs tsconfig.json pnpm-workspace.yaml .github/workflows/ci.yml; do
  test -f "$f" && echo "  ✓ $f" || echo "  ✗ $f MISSING"
done

echo ""
echo "=== 3. Design tokens ==="
rg '^\s+--color-(background|primary|card|muted|accent|destructive|border|input|ring):' src/app/globals.css

echo ""
echo "=== 4. Component counts ==="
echo "  primitives: $(ls src/components/primitives/ | wc -l) (expected 7)"
echo "  sections: $(ls src/components/sections/ | wc -l) (expected 10)"
echo "  ui: $(ls src/components/ui/ | wc -l) (expected 4)"
echo "  app: $(ls src/components/app/ | wc -l) (expected 8)"

echo ""
echo "=== 5. Hooks ==="
ls src/lib/hooks/

echo ""
echo "=== 6. Data files ==="
ls src/lib/data/ | wc -l
echo "(expected 10)"

echo ""
echo "=== 7. Accessibility ==="
rg 'suppressHydrationWarning' src/app/layout.tsx | head -2
rg 'prefers-reduced-motion' src/app/globals.css | head -1

echo ""
echo "=== 8. Sprint 2 fixes in SKILL.md ==="
rg -c 'trustHost|MAX_PUT_OBJECT_BYTES|MAX_RECONNECT_ATTEMPTS|IMAGE_MODERATION_FAIL_OPEN' storyintovideo_SKILL.md

echo ""
echo "=== 9. Color references ==="
rg -c '#febf00|#020202|#060607|#8e8e95|#f8f8f8|#d4d4d8' storyintovideo_SKILL.md

echo ""
echo "=== 10. TypeScript interfaces ==="
rg '^export interface' src/types/index.ts | wc -l
echo "(expected 12)"

echo ""
echo "=== Test count ==="
pnpm test 2>&1 | grep -E "Test Files|Tests " | tail -2
```

---

## Reference Documents

| Document | Role |
|---|---|
| `Project_Requirements_Document.md` | Canonical marketing spec (v2.0, 2718 lines, field-verified) |
| `PRODUCTION_READINESS_PLAN.md` | Engineering blueprint (11 ADRs, 27 TDD task cards, risk register, pre-launch checklist) |
| `MASTER_EXECUTION_PLAN.md` | Marketing clone execution record (8 phases, 15 decisions, 20 risks) |
| `CLAUDE.md` | Agent briefing document (stack, conventions, pitfalls, anti-patterns) |
| `AGENTS.md` | Compact agent instructions |
| `README.md` | Quick start + architecture + build state |
| `storyintovideo_SKILL.md` | This file — complete engineering reference (v3.0.0) |

---

## Success Criteria

You are successful when:

- `pnpm lint` exits with 0 warnings
- `pnpm typecheck` exits with 0 errors
- `pnpm test` passes all 259 unit tests
- `pnpm test:e2e` passes all 48 E2E tests (requires Playwright browsers installed)
- `pnpm build` exits with 0 errors
- Lighthouse scores ≥95 across Performance, Accessibility, Best Practices, SEO (marketing page)
- The marketing page is visually indistinguishable from `storyintovideo.com` at 1440×900
- The full pipeline works end-to-end: signup → paste story → AI generates video → download
- All external services are provisioned and `.env.local` is complete
- The pre-launch checklist (`PRODUCTION_READINESS_PLAN.md` §8) is fully checked
- CI passes on every PR (`.github/workflows/ci.yml`)
- `AUTH_URL` matches `NEXT_PUBLIC_APP_URL` host in production
- `REPLICATE_SDXL_IPADAPTER_MODEL` is set to a real IP-Adapter version hash
- `IMAGE_MODERATION_FAIL_OPEN=false` in production

---

**End of `storyintovideo_SKILL.md` v3.0.0**
