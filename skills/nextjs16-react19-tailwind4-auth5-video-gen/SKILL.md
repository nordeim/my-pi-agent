---
name: nextjs16-react19-tailwind4-auth5-video-gen
description: Production-grade Next.js 16 + React 19 + Tailwind CSS v4 full-stack SaaS. Covers App Router Server Components, TypeScript strict, CSS-first @theme design system, Drizzle ORM + PostgreSQL, Auth.js v5 authentication, job queue orchestration (Inngest/BullMQ), AI pipeline integration (OpenAI, Replicate, ElevenLabs), credit-based Stripe billing, Cloudflare R2 storage, SSE streaming, idempotent transactions, WCAG AAA accessibility, OWASP 2025 security hardening, Docker deployment, Vitest + Playwright testing, CI/CD, and live-site validation. Comprehensive engineering reference with audit history, ADRs, 60+ lessons learned, z-index maps, color tokens, and debugging guides for AI media generation, content platforms, or any full-stack Next.js SaaS.
version: 9.0
---

# StoryIntoVideo — Complete Project Skill

This skill file distills the complete knowledge of the StoryIntoVideo codebase — design philosophy, tech stack, architecture, component patterns, hooks, accessibility, anti-patterns, debugging, lessons learned, and the exact tokens/interfaces/z-index map that a coding agent needs to replicate or extend this project with the same quality bar.

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
21. [Appendix A: ADRs (Architecture Decision Records)](#appendix-a-adrs)
22. [Appendix B: 6-Step Pipeline Credit Costs](#appendix-b-6-step-pipeline-credit-costs)
23. [Appendix C: Audit History (v1 + v2)](#appendix-c-audit-history)

---

## 1. Project Identity & Design Philosophy

### 1.1 What Is StoryIntoVideo?

StoryIntoVideo is a **production SaaS** that transforms a written story into a finished MP4 video via a 6-step async AI pipeline (moderate → analyze → characters → scenes → voiceover → subtitles → video assembly). It began as a pixel-accurate static marketing clone of `storyintovideo.com` (luxury-dark, cinematic) and evolved into a hybrid Next.js app with a full backend: Auth.js v5, Drizzle/PostgreSQL, Inngest, Stripe, Cloudflare R2, OpenAI/Replicate/ElevenLabs.

**Live site:** `https://storyintovideo.jesspete.shop/`

### 1.2 The Design Philosophy: "Luxury-Dark Cinematic" + "Anti-Generic"

The aesthetic is **luxury-dark cinematic** — not brutalist, not minimal, not corporate. It's the visual language of a high-end film studio's landing page: near-black backgrounds, a single rationed amber accent, cinematic typography, and CSS-only animation that feels like film transitions.

**Anti-Generic Rules (non-negotiable):**
- **No purple gradients** — the ONLY permitted purple on the entire site is the example-card hover gradient (`bg-gradient-to-r from-yellow-500 to-purple-500`). Every other use of purple is a bug.
- **No "Inter/Roboto safety"** — body uses Geist Sans, display headings use Outfit weight 820 (NOT available from Google Fonts API — must self-host).
- **No Framer Motion / GSAP** — all 13 animations are CSS `@keyframes`. This is critical for Lighthouse ≥95 and bundle size.
- **Amber is rationed** — `#febf00` is the only hue permitted to assert itself. It appears on CTAs, active states, focus rings, and the eyebrow badge. It does NOT appear in body text, borders, or backgrounds (except the eyebrow glow).
- **No template card grids** — the Features section uses a hairline grid, not shadow cards. The Examples section uses a portrait carousel, not a 3-column grid.
- **No `amber-400`** — Tailwind's `amber-400` is `#fbbf24`, which is a DIFFERENT color from `#febf00`. Always use the custom `--color-primary` token. `brand-tokens.test.ts` enforces 0 violations.

### 1.3 The "Engineered Soul" Component Philosophy

Every component has a purpose beyond aesthetics. The hierarchy is:

1. **Purpose** — what problem does this solve? (e.g., Hero: capture the story input + communicate the value prop in 3 seconds)
2. **Tone** — luxury-dark cinematic (not playful, not corporate, not minimal)
3. **Differentiation** — what makes this UNFORGETTABLE? (e.g., the Hero's glass-input widget with backdrop-blur + amber focus glow)
4. **Conceptual Direction** — execute with precision. Every pixel serves the cinematic direction.

### 1.4 CTA Hierarchy (4 Tiers — Deliberate)

| Tier | Component | Visual | Use Case |
|---|---|---|---|
| 1 (most restrained) | `CtaGhost` | Ghost link with animated arrow | Secondary navigation, "Sign in" |
| 2 | Glass pill | Frosted glass with border | (used inline in Hero) |
| 3 | `CtaGradient` | Amber gradient pill | Mid-priority conversion |
| 4 (conversion crescendo) | `CtaAmber` | Solid amber pill with hover scale + glow | Primary CTA ("Start Creating") |

---

## 2. Tech Stack & Environment

### 2.1 Locked Versions (Never Downgrade Without Explicit Approval)

| Layer | Technology | Version | Critical Constraint |
|---|---|---|---|
| Framework | Next.js (App Router, hybrid) | `^16.2.0` | Turbopack dev; `proxy.ts` (renamed from `middleware.ts` in Next.js 16) |
| UI Runtime | React (strict TypeScript) | `^19.2.3` | ⚠️ **CVE-2025-55182 floor — never downgrade below 19.2.3** ("React2Shell" RCE, CVSS 10.0) |
| Language | TypeScript | `^5.9.0` | `strict: true`, `noUncheckedIndexedAccess`, `verbatimModuleSyntax`, `noImplicitOverride`, `noUnusedLocals`, `noUnusedParameters` |
| Styling | Tailwind CSS (CSS-first `@theme`) | `^4.3.0` | **No `tailwind.config.ts`** — all tokens in `globals.css` `@theme` block |
| Components | shadcn/ui (Radix, hand-written) | — | 4 primitives only (button, accordion, sheet, dropdown-menu) — CLI timed out |
| Fonts | Geist Sans + Geist Mono + Outfit 820 | self-hosted | Outfit 820 NOT available via `next/font/google` — must use `next/font/local` |
| Icons | Lucide React | `^0.460.0` | Tree-shakable, consistent stroke width |
| Auth | Auth.js v5 (NextAuth) + `@auth/drizzle-adapter` | `5.0.0-beta.31` / `^1.11.2` | `trustHost: true` for reverse-proxy; JWT sessions |
| Database | PostgreSQL (Neon) + Drizzle ORM | `drizzle-orm ^0.45.2` / `postgres ^3.4.9` | Pooled `DATABASE_URL` + unpooled `DATABASE_URL_UNPOOLED` for migrations |
| Job Queue | Inngest | `^4.11.0` | v4 `createFunction` uses `triggers` array in config (not 2nd arg) |
| AI — LLM | OpenAI GPT-4o + Whisper + Moderation | `openai ^6.45.0` | JSON mode analysis, Whisper ASR, content moderation |
| AI — Image | Replicate SDXL + IP-Adapter | `replicate ^1.4.0` | ⚠️ `REPLICATE_SDXL_IPADAPTER_MODEL` must be set to `lucataco/sdxl-ipadapter:<sha>` (default is placeholder) |
| AI — TTS | ElevenLabs | `^1.59.0` | Returns `Readable`, not `ReadableStream`; chunk text at 4500 chars |
| Storage | Cloudflare R2 (S3-compatible) | `@aws-sdk/client-s3 ^3.1075.0` | 3 buckets (`siv-uploads`, `siv-generated`, `siv-videos`); `MAX_PUT_OBJECT_BYTES = 500 MB` |
| Billing | Stripe | `^22.3.0` | "Basil" API (2025-03-31) — `current_period_end` moved to `items.data[0]` |
| Validation | Zod (env + Server Action inputs) | `^4.4.3` | Zod v4 `.url()` accepts any scheme → compose with `.refine()` for protocol restriction |
| Video | FFmpeg (system binary) | `fluent-ffmpeg ^2.1.3` | `FFMPEG_PATH` env var (default `/usr/bin/ffmpeg`); `@ffmpeg-installer/ffmpeg` REMOVED (Turbopack-incompatible) |
| Rate Limiting | Upstash Ratelimit + Redis | `@upstash/ratelimit ^2.0.8`, `@upstash/redis ^1.38.0` | 3 limiters: auth 10/15min/IP, pipeline 5/min/user, SSE slot pattern |
| Hashing | bcryptjs | `^3.0.3` | Cost factor 12 |
| Testing (unit) | Vitest + jsdom | `vitest ^4.0.0` | 524 tests across 58 files |
| Testing (E2E) | Playwright | `^1.61.0` | Chromium only; 48 tests across 9 spec files |
| Quality | ESLint (flat config) | `^9.0.0` | `@typescript-eslint/no-explicit-any: error`; zero warnings before commit |
| Package Manager | pnpm | `>=10.26.0` | `allowBuilds` syntax floor |
| Node | — | `>=20.0.0` | |
| CI/CD | GitHub Actions | `.github/workflows/ci.yml` | `quality-gate` job + `e2e` job (Postgres 17 service container) |

### 2.2 Known Dependency Notes

- **`next-auth@5.0.0-beta.31`** — Auth.js v5 is technically beta. Pin the exact version; test on every upgrade.
- **`postcss <8.5.10`** — moderate vuln (GHSA-qx2v-qp2m-jg93, transitive via `next`). Not exploitable. `pnpm audit --audit-level=high` passes clean.
- **`@aws-sdk/lib-storage`** — NOT installed (NF-5 corrected the docs that claimed it was). The H5 FFmpeg streaming refactor requires `pnpm add @aws-sdk/lib-storage` first.
- **`@sentry/nextjs`** — NOT installed. `SENTRY_DSN` is in the env schema only.

---

## 3. Bootstrapping & Configuration

### 3.1 From Scratch (Recreating the Environment)

```bash
# 1. Create the Next.js 16 app with src/ directory
pnpm create next-app@latest story-into-video \
  --typescript \
  --tailwind \
  --eslint \
  --app \
  --src-dir \
  --import-alias "@/*" \
  --use-pnpm

cd story-into-video

# 2. Install runtime dependencies
pnpm add next-auth@5.0.0-beta.31 @auth/drizzle-adapter \
  drizzle-orm postgres \
  inngest \
  openai replicate elevenlabs \
  @aws-sdk/client-s3 @aws-sdk/s3-request-presigner \
  stripe \
  zod \
  bcryptjs \
  fluent-ffmpeg \
  @upstash/ratelimit @upstash/redis \
  geist lucide-react \
  class-variance-authority clsx tailwind-merge \
  @radix-ui/react-accordion @radix-ui/react-dialog @radix-ui/react-dropdown-menu @radix-ui/react-slot \
  react@^19.2.3 react-dom@^19.2.3

# 3. Install dev dependencies
pnpm add -D drizzle-kit tsx \
  vitest @vitejs/plugin-react jsdom \
  @testing-library/react @testing-library/jest-dom @testing-library/user-event \
  @playwright/test \
  eslint-config-next typescript-eslint eslint-plugin-react eslint-plugin-react-hooks \
  prettier prettier-plugin-tailwindcss \
  husky lint-staged \
  @types/bcryptjs @types/fluent-ffmpeg @types/node @types/react @types/react-dom \
  dotenv dotenv-cli

# 4. Configure pnpm workspace (pnpm 10.26+ syntax)
cat > pnpm-workspace.yaml << 'EOF'
packages: ['.']
allowBuilds:
  esbuild: true
  protobufjs: true
  sharp: true
  unrs-resolver: true
EOF

# 5. Install Playwright browsers
pnpm exec playwright install --with-deps chromium

# 6. Activate husky
pnpm install  # runs `prepare: husky || true`
```

### 3.2 Critical Configuration Files

#### `tsconfig.json` (strict mode — maximum)
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "esnext",
    "moduleResolution": "bundler",
    "jsx": "react-jsx",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "noFallthroughCasesInSwitch": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "verbatimModuleSyntax": true,
    "forceConsistentCasingInFileNames": true,
    "isolatedModules": true,
    "incremental": true,
    "paths": { "@/*": ["./src/*"] }
  },
  "include": ["next-env.d.ts", "**/*.{ts,tsx}", ".next/types/**/*.ts"],
  "exclude": ["node_modules", "skills", "docs"]
}
```

#### `drizzle.config.ts` (CRITICAL: never use `db push` in production)

```typescript
import 'dotenv/config';
import { defineConfig } from 'drizzle-kit';

export default defineConfig({
  schema: './src/lib/db/schema/index.ts',
  out: './drizzle',
  dialect: 'postgresql',
  dbCredentials: {
    url: process.env.DATABASE_URL_UNPOOLED!, // Direct Neon connection (NOT pooled)
  },
  verbose: true,
  strict: true,
});
```

**CRITICAL RULES:**
- **Never use `drizzle-kit push` in production** — always `drizzle-kit generate` + `drizzle-kit migrate`
- **Migrations need `DATABASE_URL_UNPOOLED`** — pooled connections + DDL is unreliable
- **All FKs from `users` are `onDelete: 'cascade'`** — GDPR deletion relies on this

#### `pnpm-workspace.yaml` (pnpm 10.26+ required)

```yaml
packages:
  - '.'
allowBuilds:
  esbuild: true
  protobufjs: true
  sharp: true
  unrs-resolver: true
```

**Critical notes:**
- `packages: ['.']` is **required** even for single-package repos (pnpm 9+ enforces this)
- `allowBuilds` (pnpm 10.26+) replaced `onlyBuiltDependencies` (removed in pnpm 11)
- The engine floor is `>=10.26.0` to match the `allowBuilds` syntax
- `esbuild` must be approved or `drizzle-kit`, `vitest`, and `tsx` won't build

#### `next.config.ts` (6 security headers — NF-2)
```typescript
import type { NextConfig } from 'next';

const CSP_POLICY = [
  "default-src 'self'",
  "script-src 'self' 'unsafe-inline'",   // Next.js App Router requires inline
  "style-src 'self' 'unsafe-inline'",     // Tailwind v4
  "img-src 'self' data: https:",
  "font-src 'self'",
  "connect-src 'self'",
  "media-src 'self'",
  "frame-ancestors 'none'",
  "base-uri 'self'",
  "form-action 'self'",
  "object-src 'none'",
].join('; ');

const nextConfig: NextConfig = {
  reactStrictMode: true,
  poweredByHeader: false,
  allowedDevOrigins: ['storyintovideo.jesspete.shop'],
  images: { formats: ['image/avif', 'image/webp'] },
  async headers() {
    return [{
      source: '/(.*)',
      headers: [
        { key: 'X-Frame-Options', value: 'DENY' },
        { key: 'X-Content-Type-Options', value: 'nosniff' },
        { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
        { key: 'Permissions-Policy', value: 'camera=(), microphone=(), geolocation=()' },
        { key: 'Content-Security-Policy', value: CSP_POLICY },        // NF-2
        { key: 'Strict-Transport-Security', value: 'max-age=63072000; includeSubDomains; preload' }, // NF-2
      ],
    }];
  },
};
export default nextConfig;
```

#### `eslint.config.mjs` (flat config — direct plugin imports, no FlatCompat)
```javascript
// Key rules:
// @typescript-eslint/no-explicit-any: error
// @typescript-eslint/consistent-type-imports: error
// react/react-in-jsx-scope: off
// react-hooks/exhaustive-deps: warn
// Ignores: node_modules, .next, skills, docs, scripts
```

#### `postcss.config.mjs` (Tailwind v4 — single plugin)
```javascript
export default { plugins: { '@tailwindcss/postcss': {} } };
```

#### `vitest.config.ts`
```typescript
export default defineConfig({
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/tests/setup.ts'],
    include: ['src/tests/unit/**/*.test.{ts,tsx}'],
    coverage: { provider: 'v8', include: ['src/lib/**/*.{ts,tsx}', 'src/components/**/*.{ts,tsx}'] },
  },
  resolve: { alias: { '@': './src' } },
});
```

### 3.3 Environment Variables (30 total — 20 required, 5 with defaults, 2 optional)

All env vars are validated by a Zod schema in `src/lib/env/index.ts`. **Never read `process.env.*` directly** — always import `env` from `@/lib/env`.

**Critical env behavior:**
- **Build-context fallback:** When `NEXT_PHASE=phase-production-build` or `NODE_ENV=test`, the schema returns placeholder values so `next build` succeeds without real secrets.
- **T1 host-mismatch throw:** In production runtime, if `AUTH_URL` host ≠ `NEXT_PUBLIC_APP_URL` host, the app **REFUSES TO BOOT** with a thrown error. In dev/test, it only `console.warn`s.
- **`IMAGE_MODERATION_FAIL_OPEN`** defaults to `'false'` (fail-closed) in production, `'true'` in dev/test (H8 fix).

See `.env.example` for the full list with format validation rules.

---

## 4. The Design System (Code-First)

### 4.1 The `@theme` Block (Tailwind v4 CSS-First)

All design tokens live in `src/app/globals.css` inside a single `@theme { ... }` block. There is **no `tailwind.config.ts`**. The `@source` directives handle content scanning:

```css
@import 'tailwindcss';

@source '../components/**/*.{ts,tsx}';
@source '../lib/**/*.{ts,tsx}';

@theme {
  /* Colors, typography, radius, shadows, animations, keyframes — all here */
}
```

### 4.2 Color Tokens (Field-Verified from Live DOM)

| Token | Hex | Usage | WCAG Contrast |
|---|---|---|---|
| `--color-background` | `#020202` | Page background (near-black, warm-neutral — NOT pure #000) | — |
| `--color-foreground` | `#f8f8f8` | Default foreground (headings) | 18.1:1 on background (AAA) |
| `--color-card` | `#060607` | Card surfaces | — |
| `--color-card-foreground` | `#f8f8f8` | Text on cards | 18.0:1 on card (AAA) |
| `--color-popover` | `#0b0b0d` | Dropdown/sheet backgrounds | — |
| `--color-primary` (amber) | `#febf00` | CTAs, active states, focus rings, eyebrow | 14.5:1 on background (AAA) |
| `--color-primary-foreground` | `#020202` | Text on amber CTAs | 14.5:1 on primary (AAA) |
| `--color-secondary` | `#111114` | Secondary surfaces | — |
| `--color-muted` | `#1a1a1d` | Muted backgrounds | — |
| `--color-muted-foreground` | `#8e8e95` | Secondary text (zinc-400 equivalent) | 6.4:1 on background (AA) |
| `--color-accent` | `#febf00` | Same as primary (alias) | — |
| `--color-destructive` | `#ff2d39` | Error states | — |
| `--color-border` | `#1a1a1d` | Default borders | — |
| `--color-input` | `#0b0b0d` | Input backgrounds | — |
| `--color-ring` | `#febf0080` | Focus ring (50% opacity amber) | — |

**Body text** uses `#d4d4d8` (zinc-300) — **12.6:1 contrast on `#020202`** (WCAG AAA).

⚠️ **`#febf00` ≠ Tailwind's `amber-400` (`#fbbf24`)** — these are different colors. Always use the custom `--color-primary` token. `brand-tokens.test.ts` enforces 0 violations of `amber-300/400/500/600` or `bg-zinc-950/900/black` in non-test source.

### 4.3 Typography Hierarchy

| Role | Font | Weight | Class | Tracking |
|---|---|---|---|---|
| Display H1 (hero desktop) | Outfit | **820** | `font-heading text-[4.5rem]` | `-0.04em` |
| Display H1 (hero mobile) | Outfit | 820 | `text-4xl` | scales with `em` |
| H2 (sections) | Outfit | 700 | `font-heading text-4xl lg:text-6xl` | `-0.03em` |
| Body / UI | Geist Sans | 400–600 | `font-sans text-lg` | normal |
| Accents / toggles | Geist Mono | 400 | `font-mono text-[10px]` | — |

**Why Outfit weight 820 via `next/font/local`:** Google Fonts API only serves discrete weights (100, 200, ..., 900); weight 820 is NOT one of them. Self-hosting the variable font woff2 (`public/fonts/Outfit-VariableFont.woff2`, 45KB) is the ONLY way to access weight 820.

**Font wiring (`src/lib/fonts.ts`):**
```typescript
import { GeistSans } from 'geist/font/sans';
import { GeistMono } from 'geist/font/mono';
import localFont from 'next/font/local';

const outfit = localFont({
  src: '../../public/fonts/Outfit-VariableFont.woff2',
  weight: '100 900',           // variable font range
  variable: '--font-outfit',
  display: 'swap',
});

export const fontVariables: string = [GeistSans.variable, GeistMono.variable, outfit.variable].join(' ');
```

Applied in `layout.tsx`: `<html lang="en" className={fontVariables} suppressHydrationWarning>`

### 4.4 The 13 Keyframes (All Kebab-Case)

All animation is CSS `@keyframes` only — **no Framer Motion, no GSAP**. Keyframes live INSIDE the `@theme` block so Tailwind v4 picks them up.

| # | Keyframe | Purpose | Duration |
|---|---|---|---|
| 1 | `fade-in-up` | Entrance: opacity 0→1, translateY 20px→0 | 0.6s ease-out both |
| 2 | `float` | Ambient: translateY 0→-12px→0 | 6s ease-in-out infinite |
| 3 | `glow-pulse` | Amber box-shadow pulse | 3s ease-in-out infinite |
| 4 | `border-glow` | Border color pulse (0.08→0.2 opacity) | 4s ease-in-out infinite |
| 5 | `composite-pulse-text` | Text opacity pulse (0.7→1) | 2s ease-in-out infinite |
| 6 | `shimmer` | Background-position sweep (200%→-200%) | 3s linear infinite |
| 7 | `btn-shimmer` | Button highlight sweep (translate -100%→100%) | 1.5s ease-in-out infinite |
| 8 | `grid-shimmer` | Grid texture drift | 8s ease-in-out infinite |
| 9 | `grid-sweep-h` | Horizontal light sweep (translate -600px→100vw) | 8s linear infinite |
| 10 | `grid-sweep-v` | Vertical light sweep | 10s linear infinite |
| 11 | `scanline-scroll` | Scanline background-position-x (0→30px) | 1s linear infinite |
| 12 | `lang-dropdown-in` | Dropdown entrance (opacity+scale+translateY) | 0.15s ease-out |
| 13 | `marquee-scroll` | Style chip marquee (translateX 0→-50%) | 40s linear infinite (30s on mobile) |

### 4.5 Custom `@utility` Classes (7)

Tailwind v4 uses `@utility` (single-purpose helpers) instead of v3's `@layer components` + `@layer utilities`:

| Utility | Purpose |
|---|---|
| `scrollbar-hide` | Hide scrollbar for carousels (cross-browser) |
| `marquee-mask` | Edge fade mask for style chip marquee |
| `marquee-track` | Infinite horizontal scroll, pauses on hover, 30s on mobile |
| `glass-input` | Hero textarea wrapper — backdrop-blur(16px) + amber focus-within glow |
| `eyebrow` | Amber pill badge with ambient glow (uppercase, 11px, 0.1em tracking) |
| `section-heading` | H2 with Outfit + fluid `clamp(2rem, 5vw, 3rem)` size |
| `cta-amber` | Tier-4 CTA — solid amber pill with hover scale(1.02) + glow |

### 4.6 Border Radius Scale

| Token | Value | Usage |
|---|---|---|
| `--radius` | `0.75rem` (12px) | Default |
| `--radius-sm` | `calc(0.75rem - 4px)` = 8px | Small elements |
| `--radius-md` | `calc(0.75rem - 2px)` = 10px | Medium elements |
| `--radius-lg` | `0.75rem` = 12px | Large elements |
| `--radius-xl` | `1rem` = 16px | Extra large |
| `--radius-2xl` | `1.25rem` = 20px | Glass input, cards |

### 4.7 Shadows

| Token | Value |
|---|---|
| `--shadow-hero-input` | `0 20px 80px rgba(0, 0, 0, 0.6)` |
| `--shadow-eyebrow-glow` | `0 0 30px rgba(234, 179, 8, 0.1)` |
| `--shadow-cta-glow` | `0 0 40px rgba(251, 191, 36, 0.3)` |

---

## 5. Component Architecture & Patterns

### 5.1 The 5-Layer Architecture (Golden Rule)

```
Layer 0: src/proxy.ts             — Cookie check, redirect. NO DB. NO logic. Edge runtime.
                                    (Renamed from middleware.ts in Next.js 16.)
Layer 1: src/app/                 — Route structure, metadata, Suspense. Layouts must NOT fetch data.
Layer 2: src/features/            — UI composition, data binding, mutations
                                    (auth, projects, pipeline, billing)
Layer 3: src/features/*/domain/   — Pure business logic. No Next.js or DB runtime imports
                                    (import type only).
Layer 4: src/lib/                 — Infrastructure: Drizzle, Auth.js, Inngest, R2, Stripe,
                                    AI providers. Side effects only.
```

**Golden Rule:** A lower layer may never import from a higher layer. Domain may import *types* from Infrastructure but never runtime code.

### 5.2 Component Inventory

#### `src/components/ui/` (4 shadcn primitives — Radix-based, hand-written)
| File | Lines | Purpose |
|---|---|---|
| `button.tsx` | 55 | CVA-styled Button — 6 variants × 4 sizes, `asChild` slot support |
| `accordion.tsx` | 63 | Radix Accordion wrapper (Root/Item/Trigger/Content) |
| `sheet.tsx` | 131 | Radix Dialog-based Sheet (top/right/bottom/left slide-in) |
| `dropdown-menu.tsx` | 224 | Radix DropdownMenu full wrapper (14 sub-components) |

#### `src/components/primitives/` (7 hand-written marketing primitives)
| File | Lines | Purpose | CTA Tier |
|---|---|---|---|
| `cta-amber.tsx` | 41 | Solid amber pill CTA with hover scale + glow | 4 (conversion crescendo) |
| `cta-gradient.tsx` | 35 | Amber gradient pill CTA | 3 |
| `cta-ghost.tsx` | 38 | Ghost link CTA with animated arrow | 1 (most restrained) |
| `eyebrow.tsx` | 17 | Amber eyebrow badge (uses `@utility eyebrow`) |
| `section-heading.tsx` | 24 | Outfit-font H2 with tracking |
| `scroll-reveal.tsx` | 42 | Client component wrapping `useReveal` for IntersectionObserver-driven reveal |
| `style-chip.tsx` | 44 | Marquee chip — `<button>` (interactive) or `<div>` (decorative) |

#### `src/components/sections/` (10 marketing sections)
| File | Lines | Type | Purpose |
|---|---|---|---|
| `navbar.tsx` | 177 | Client | Sticky nav with scroll-aware bg (`useScrolled`), mobile Sheet, language dropdown (decorative) |
| `hero.tsx` | 202 | Client | Story textarea, style chip marquee, ratio toggle, character counter |
| `examples.tsx` | 127 | Client | 6-card portrait carousel |
| `workflow.tsx` | 99 | Client | 4 alternating media/text rows with looping MP4s |
| `features.tsx` | 86 | Server | 8-feature 4×2 hairline grid |
| `testimonials.tsx` | 64 | Server | 6 testimonial cards in 3×2 grid |
| `use-cases.tsx` | 72 | Server | 4 use-case cards in 2×2 grid |
| `faq.tsx` | 65 | Client | Radix Accordion with 6 items |
| `final-cta.tsx` | 56 | Server | Conversion section using `CtaAmber` |
| `footer.tsx` | 92 | Server | 3-column footer with brand + copyright |

#### `src/components/app/` (8 app components)
| File | Lines | Purpose |
|---|---|---|
| `providers.tsx` | 11 | Client `SessionProvider` wrapper |
| `cookie-banner.tsx` | 127 | GDPR banner using `useSyncExternalStore` (SSR-safe) |
| `auth-form.tsx` | 177 | Sign-in/sign-up form, calls `signUpAction` for sign-up |
| `create-wizard.tsx` | 208 | Story textarea + style chips + ratio toggle + character counter |
| `empty-state.tsx` | 53 | Reusable presentational empty-list state |
| `project-progress-panel.tsx` | 82 | Subscribes to SSE via `useProjectProgress`, shows progress bar |
| `project-download-button.tsx` | 127 | Click-time URL signing via fetch to `/api/projects/[id]/download` |
| `project-share-button.tsx` | 57 | Web Share API with clipboard fallback |

### 5.3 Component Patterns

**Pattern 1: Server Components by default**
- Add `'use client'` ONLY when using `useState`, `useEffect`, event handlers, or browser APIs.
- Server components: Features, Testimonials, UseCases, FinalCta, Footer, all legal pages, dashboard, billing.

**Pattern 2: Named function exports (never default)**
```typescript
// ✅ Correct
export function Hero() { ... }

// ❌ Wrong — default export
export default function Hero() { ... }
```

**Pattern 3: `interface` for all props**
- Object shapes: `interface`
- Unions/intersections: `type`
- Props interfaces in `src/types/index.ts` or co-located

**Pattern 4: `cn()` utility for conditional classes**
```typescript
import { cn } from '@/lib/utils';
<div className={cn('base-classes', condition && 'conditional-class')} />
```

**Pattern 5: `suppressHydrationWarning` on `<html>` AND `<body>`**
- Browser extensions (Grammarly) inject attributes before React hydrates.
- `<html>` alone is insufficient — must also be on `<body>`.

**Pattern 6: Scroll reveal via data attributes**
```tsx
<ScrollReveal data-reveal delay={200}>
  <div data-revealed={revealed ? 'true' : 'false'}>...</div>
</ScrollReveal>
```
CSS handles the transition: `[data-reveal] { opacity: 0; }` → `[data-revealed='true'] { opacity: 1; }`

**Pattern 7: Radix accordion animation (grid-template-rows trick)**
```css
.radix-accordion-content {
  display: grid;
  grid-template-rows: 0fr;
  transition: grid-template-rows 300ms ease-out;
}
.radix-accordion-content[data-state='open'] { grid-template-rows: 1fr; }
```
Modern GPU-accelerated alternative to `max-height` animation. Supported in Chrome 117+, Firefox 118+, Safari 17.4+.

---

## 6. Custom Hooks Deep Dive

### 6.1 `useScrolled(threshold = 10): boolean`

**Location:** `src/lib/hooks/use-scrolled.ts` (23 lines)
**Purpose:** Returns `true` when `window.scrollY` exceeds the threshold. Used by the Navbar to toggle its scroll-aware background.

```typescript
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

**Key details:**
- `passive: true` on the scroll listener — prevents `preventDefault()` blocking.
- Initializes on mount (`onScroll()` called immediately) — avoids a flash of the unscrolled state if the user lands mid-page.
- Cleanup removes the listener on unmount.

### 6.2 `useReveal<T extends HTMLElement>(options): { ref, revealed }`

**Location:** `src/lib/hooks/use-reveal.ts` (57 lines)
**Purpose:** Wraps `IntersectionObserver` to trigger a one-shot reveal flag when an element enters the viewport. The `data-reveal` / `data-revealed` CSS attributes handle the visual transition.

```typescript
interface UseRevealOptions {
  threshold?: number;      // default 0.15
  rootMargin?: string;     // default '0px 0px -50px 0px' (triggers 50px before entering)
  once?: boolean;          // default true (disconnect after first intersection)
}
```

**Key details:**
- Generic `<T extends HTMLElement>` — caller specifies the element type (default `HTMLDivElement`).
- `once: true` (default) disconnects the observer after first intersection — one-shot reveal.
- `once: false` toggles `revealed` back to `false` when the element leaves the viewport — repeating reveal.
- `rootMargin: '0px 0px -50px 0px'` — triggers 50px BEFORE the element enters the bottom of the viewport (feels more natural than exact intersection).
- Cleanup disconnects the observer on unmount.

### 6.3 `useReducedMotion(): boolean`

**Location:** `src/lib/hooks/use-reduced-motion.ts` (27 lines)
**Purpose:** Returns `true` when the user has OS-level reduced-motion preference enabled. For cases where JS needs to know the preference (e.g., skipping a video autoplay).

```typescript
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

**Key details:**
- The global CSS `@media (prefers-reduced-motion: reduce)` block in `globals.css` handles most cases declaratively (disables all animations). This hook is for JS-level decisions.
- Initializes on mount (`onChange()` called immediately).
- Listens for `change` events so the hook updates if the user toggles the preference while the page is open.
- SSR-safe: starts as `false` on the server (no `window`), updates on mount.

### 6.4 `useProjectProgress(projectId): ProjectProgressState`

**Location:** `src/lib/hooks/use-project-progress.ts` (138 lines)
**Purpose:** Subscribes to the SSE progress stream for a project. Opens an `EventSource` on `/api/projects/[id]/progress`, parses JSON events, and exposes the latest status/progress.

```typescript
export interface ProjectProgressState {
  status: string | null;
  progressPercent: number | null;
  progressDetail: string | null;
  errorMessage: string | null;
  connectionState: 'connecting' | 'open' | 'closed' | 'error' | 'reconnecting';
}
```

**Key details:**
- **Exponential backoff reconnect** (T6 fix): on error, waits 1s → 2s → 4s (3 attempts max), then shows "error" state.
- **Terminal status auto-close:** when `status ∈ {completed, failed}`, the EventSource is closed and set to `null` (T12/L-2 fix: prevents double-close in cleanup).
- **`isCancelled` flag:** prevents reconnect after unmount (cleanup sets `isCancelled = true`).
- **`reconnectAttempt` reset on successful open** — if the stream drops and reconnects, the counter resets.
- Vercel Fluid Compute caps SSE at 300s (Hobby) or 800s (Pro/Enterprise GA). The pipeline runs 5-15min, so reconnect is essential.

**Reconnect backoff formula:**
```typescript
const BASE_BACKOFF_MS = 1000;
function backoffDelay(attempt: number): number {
  return BASE_BACKOFF_MS * Math.pow(2, attempt);  // 1000, 2000, 4000
}
```

---

## 7. Content Management & Data Ingestion

### 7.1 Static Data Files (10 files in `src/lib/data/`)

Unlike Vite-based projects that use `import.meta.glob`, Next.js uses direct TypeScript imports. All marketing content lives in typed data files:

| File | Export | Type | Count |
|---|---|---|---|
| `nav-links.ts` | `NAV_LINKS`, `NAV_LANGUAGES` | `NavLink[]`, decorative | 4 links, 3 languages |
| `footer-links.ts` | `FOOTER_COLUMNS`, `FOOTER_BRAND`, `FOOTER_COPYRIGHT` | `FooterColumn[]` | 3 columns |
| `story-seeds.ts` | `STORY_SEEDS`, `DEFAULT_STORY_EXAMPLES` | `Map<string, StoryExample>`, derived array | 4 seeds |
| `style-chips.ts` | `STYLE_CHIPS` | `StyleChip[]` | **8 chips (locked by spec)** |
| `features.ts` | `FEATURES` | `Feature[]` | 8 features (4×2 grid) |
| `examples.ts` | `EXAMPLE_CARDS` | `ExampleCard[]` | 6 portrait cards |
| `use-cases.ts` | `USE_CASES` | `UseCase[]` | 4 cards (2×2 grid) |
| `workflow-steps.ts` | `WORKFLOW_STEPS` | `WorkflowStep[]` | 4 alternating rows |
| `testimonials.ts` | `TESTIMONIALS` | `Testimonial[]` | 6 cards (3×2 grid) |
| `faq-items.ts` | `FAQ_ITEMS` | `FAQItem[]` | 6 Q&A items |

### 7.2 The `STYLE_CHIPS` Spec Lock (Critical)

The 8-chip set is **locked by spec** and protected by regression tests. Do NOT add `Comic` or `Futuristic neon` — they were a prior drift that was deliberately removed.

```typescript
export const STYLE_CHIPS: StyleChip[] = [
  { label: 'Ghibli' },
  { label: 'Medieval' },
  { label: 'Oil Painting' },
  { label: 'Anime' },
  { label: 'Japanese animation' },
  { label: 'Realistic' },
  { label: 'Cyberpunk' },
  { label: 'Watercolor' },
];
```

**Regression tests (`style-chips.test.ts`):**
- Asserts exactly 8 chips.
- Asserts verbatim labels in order.
- Asserts `Comic` and `Futuristic neon` are NOT present.
- **NF-3 fix:** `faq-style-consistency.test.ts` asserts the FAQ answer count matches `STYLE_CHIPS.length` and all labels appear.

### 7.3 Adding New Content

To add a new testimonial:
1. Add the entry to `TESTIMONIALS` in `src/lib/data/testimonials.ts`.
2. The `Testimonials` component (`src/components/sections/testimonials.tsx`) maps over the array — no component changes needed.
3. Run `pnpm test` — the existing tests verify the array shape.

To add a new style chip:
1. ⚠️ **Do NOT add to `STYLE_CHIPS`** without updating: the DB enum (`visual_style`), the Zod schema in `createProjectAction`, the `STYLE_PROMPTS` maps in `generate-character.ts` and `generate-scene.ts`, AND the `style-chips.test.ts` (which asserts the exact 8-label set).
2. The DB enum currently has 9 values (includes `comic` which is NOT in `STYLE_CHIPS`). This is intentional — `comic` is a valid enum value the UI doesn't expose.

### 7.4 Media Assets

| Directory | Contents |
|---|---|
| `public/examples/` | 6 WebP thumbnails (520×924 portrait) for the Examples carousel |
| `public/workflow/` | 4 MP4 demos + 4 WebP posters for the Workflow section |
| `public/fonts/` | `Outfit-VariableFont.woff2` (45KB, weight 100-900) |
| `public/og-image.png` | Open Graph image (1200×630) |
| `public/hero-bg.mp4` | Hero background video (46KB, 10s, 1920×1080, H.264) |
| `public/hero-poster.webp` | Hero video poster |

**Asset scripts:**
- `scripts/download-assets.sh` — downloads workflow MP4s + posters from R2 (idempotent).
- `scripts/generate-thumbnails.sh` — generates example thumbnails via z-ai CLI + ffmpeg (idempotent).

---

## 8. Accessibility (WCAG AAA) Implementation

### 8.1 Color Contrast (AAA Where Possible)

| Text | Color | Background | Ratio | Level |
|---|---|---|---|---|
| Body text | `#d4d4d8` (zinc-300) | `#020202` | 12.6:1 | **AAA** |
| Headings | `#f8f8f8` | `#020202` | 18.1:1 | **AAA** |
| Primary CTA text | `#020202` | `#febf00` (amber) | 14.5:1 | **AAA** |
| Muted text | `#8e8e95` | `#020202` | 6.4:1 | AA (AAA requires 7:1 for normal text) |

### 8.2 Skip-to-Content Link

The first focusable element in `layout.tsx`:
```tsx
<a
  href="#main"
  className="focus:bg-primary sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:rounded-md focus:px-4 focus:py-2 focus:font-medium focus:text-zinc-950 focus:shadow-lg"
>
  Skip to content
</a>
```
- `sr-only` by default (visually hidden).
- `focus:not-sr-only` makes it visible when focused via keyboard.
- `focus:z-50` ensures it's above all other content.

### 8.3 Focus Rings

Global `:focus-visible` style in `globals.css`:
```css
:focus-visible {
  outline: 2px solid var(--color-primary);  /* #febf00 */
  outline-offset: 2px;
}
```
- Uses `:focus-visible` (not `:focus`) — only shows for keyboard navigation, not mouse clicks.
- Amber outline matches the brand.

### 8.4 Reduced Motion (`prefers-reduced-motion: reduce`)

Global CSS block in `globals.css` disables ALL animations:
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

The `useReducedMotion()` hook is for JS-level decisions (e.g., conditionally rendering a video vs. a poster).

### 8.5 FAQ Accordion Accessibility

The Radix Accordion (`src/components/ui/accordion.tsx`) provides:
- `aria-expanded` on the trigger button.
- `aria-controls` linking trigger to content.
- `data-state="open|closed"` for CSS styling.
- Keyboard: Enter/Space to toggle, Tab to navigate.

### 8.6 Mobile Sheet (Navbar) Accessibility

The Radix Dialog-based Sheet (`src/components/ui/sheet.tsx`) provides:
- Focus trap (focus stays inside the sheet while open).
- `aria-modal="true"`.
- Focus restored to the trigger button on close.
- Escape key closes the sheet.

### 8.7 Cookie Banner Accessibility

- `role="region"` with `aria-label`.
- Dismissible via keyboard (Enter/Space on the "Got it" button).
- `useSyncExternalStore` for SSR-safe localStorage read (no hydration mismatch).

---

## 9. Anti-Patterns & Common Bugs

### 9.1 NF-1: Deploying with `next dev` Instead of `next start` (🔴 CRITICAL)

**Symptom:** Live site shows `[HMR] connected`, `[Fast Refresh]` in browser console; JS chunk names are source-path-based (`src_app_layout_tsx_*`); `/sign-up` takes 18s (cold compile); `cache-control: no-cache`.

**Root cause:** Only `Dockerfile.dev` existed (runs `pnpm dev`). No production Dockerfile.

**Fix:** Created production `Dockerfile` (multi-stage, `pnpm start`). Added CI guard in `.github/workflows/ci.yml` that greps `.next/` for `hmr-client` (dev-only chunk). See `docs/DEPLOYMENT_RUNBOOK.md`.

**Lesson:** Always ship a production Dockerfile separate from `Dockerfile.dev`. Add a CI guard that checks build output for dev-only chunks.

### 9.2 NF-2: Missing CSP + HSTS Headers (🟠 HIGH)

**Symptom:** `curl -I` shows only 4 security headers (no `Content-Security-Policy`, no `Strict-Transport-Security`).

**Root cause:** `next.config.ts` `headers()` returned 4 headers but omitted CSP + HSTS.

**Fix:** Added CSP (`default-src 'self'`, `frame-ancestors 'none'`, etc.) + HSTS (`max-age=63072000; includeSubDomains; preload`). 8 new tests in `security-headers.test.ts`.

**Lesson:** CSP `'unsafe-inline'` is required for Next.js App Router (inline `<script>` chunks for router state). Ship it first, upgrade to nonce-based later.

### 9.3 NF-3: Three-Way Drift (DB Enum / UI Array / FAQ Copy) (🟡 MEDIUM)

**Symptom:** FAQ says "7+ visual styles including Ghibli, Oil Painting, Anime, Realistic, Cyberpunk, Watercolor, and Comic" but the marquee directly above shows 8 chips (no Comic, includes Medieval + Japanese animation).

**Root cause:** Three independent sources of truth (DB enum, `STYLE_CHIPS` array, FAQ copy) were never reconciled.

**Fix:** Updated FAQ to match `STYLE_CHIPS` exactly. Added `faq-style-consistency.test.ts` regression test.

**Lesson:** When a user-facing count appears in copy, derive it from the source-of-truth array OR add a regression test that asserts the copy matches the array.

### 9.4 NF-4: Dead/Unused Exports (🟡 MEDIUM)

**Symptom:** `getProjectVideo` exported but only in a test mock; `WHISPER_MODEL` exported but the call site hardcoded `'whisper-1'`.

**Fix:** Removed `getProjectVideo` + `export` on `r2Client`/`BUCKET_MAP`. Kept `WHISPER_MODEL` and made it actually used in `align-subtitles.ts`.

**Lesson:** Every export should have at least one importer. If a constant is declared, USE it at the call site.

### 9.5 NF-6: Pipeline Steps Without try/catch → Ghost Projects (🟡 MEDIUM)

**Symptom:** Projects stuck at "Synthesizing voiceover… 65%" forever — never complete, never fail.

**Root cause:** Steps 1, 4, 5, 6 had no try/catch. If Inngest exhausted retries, the project row stayed in a non-terminal status.

**Fix:** Wrapped steps 1, 4, 5, 6 in try/catch with `setProjectFailed` + re-throw. The `complete` step logs-only (video is already in R2).

**Lesson:** Every pipeline step that can throw must (a) catch, (b) call `setProjectFailed`, (c) re-throw. Exception: the final "mark complete" step — if that fails, the work is done, don't mark it failed.

### 9.6 Historical Bugs (Audit-v1 T1–T12, All Closed)

| ID | Bug | Fix |
|---|---|---|
| C-1 | Billing buttons POST to non-existent route | T1: `billingCheckoutAction` Server Action |
| C-2 | Protected routes ERR_CONNECTION_REFUSED | T2: proxy uses `env.NEXT_PUBLIC_APP_URL` |
| H-1 | Orphan project rows on insufficient credits | T3: `db.transaction()` via `debitCreditsTx` |
| H-2 | Stripe webhook idempotency lost updates | T4: INSERT after side effects + pre-check SELECT |
| H-3 | SSE rate limit never released on disconnect | T5: `claimSseSlot`/`releaseSseSlot` Redis slot pattern |
| M-1 | Download route generic 500 | T6: error classification 502/504/500 |
| M-2 | `inngest.send()` failure orphaned projects | T7: try/catch → `setProjectFailed()` |
| M-3 | `appendVideo` set `status='completed'` before MP4 | T8: `status='rendering'` at insert |
| M-4 | `FAIL_OPEN` read at module load | T9: `getFailOpen()` reads per-call |
| M-5 | Dead `buildFfmpegCommand` export | T10: deleted |
| M-6 | Brand color bypassed 122+ times | T11: `sed` sweep + `brand-tokens.test.ts` enforces 0 |
| L-2/3/4 | Double-close + `Date.now()` collisions + hardcoded `metadataBase` | T12: `eventSource=null` guard, `crypto.randomUUID()`, `env.NEXT_PUBLIC_APP_URL` |

### 9.7 Common React/Next.js Anti-Patterns Avoided

- **`suppressHydrationWarning` on `<body>`, not just `<html>`** — Grammarly injects `<body>` attributes.
- **Workflow is `'use client'`** — uses `useState` for video loading choreography. Don't assume server components for "mostly static" sections.
- **`verifySession()` never wrapped in try/catch** — it throws `NEXT_REDIRECT` which must propagate.
- **Client components never import `r2.ts`** — env validation crashes in the browser.
- **`next/font/google` can't serve Outfit 820** — must use `next/font/local`.
- **`@ffmpeg-installer/ffmpeg` is Turbopack-incompatible** — use system FFmpeg via `FFMPEG_PATH`.
- **`next lint` is deprecated in Next.js 16** — use `eslint .` directly.

---

## 10. Debugging Guide

### 10.1 Build Failures

| Error | Cause | Fix |
|---|---|---|
| `Invalid environment variables` | Real env vars not in `.env.local` | Copy `.env.example` → `.env.local`, fill in real values |
| `Failed to collect page data for /api/auth/[...nextauth]` | Auth route tries to prerender DrizzleAdapter | Ensure `export const dynamic = 'force-dynamic'` in the route handler |
| `Functions cannot be passed directly to Client Components` | Server Action defined inline in a Server Component | Move to a `"use server"` module (e.g., `src/features/billing/actions.ts`) |
| `ERR_PNPM_INVALID_WORKSPACE_CONFIGURATION packages field missing` | `pnpm-workspace.yaml` missing `packages:` | Add `packages: ['.']` (already done) |
| CI guard fails: `hmr-client chunks found` | Build output contains dev-only chunks | Ensure `NODE_ENV=production` + `NEXT_PHASE=phase-production-build` in the build step |

### 10.2 Runtime Errors

| Error | Cause | Fix |
|---|---|---|
| Auth redirects to `http://localhost:3000` in production | `AUTH_URL` or `NEXT_PUBLIC_APP_URL` set to localhost | Set both to the production HTTPS URL. T1 now throws at boot if hosts differ. |
| `/dashboard` returns ERR_CONNECTION_REFUSED | Proxy used `nextUrl.origin` (resolves to `http://` behind reverse proxy) | Fixed (T2): proxy uses `env.NEXT_PUBLIC_APP_URL`. Verify the env var is set correctly. |
| `putObject` throws `PayloadTooLargeError` | Body exceeds 500 MB | Use multipart upload (`CreateMultipartUploadCommand`) for larger files |
| Replicate scene generation 404s | `REPLICATE_SDXL_IPADAPTER_MODEL` is the placeholder | Set to a real `lucataco/sdxl-ipadapter:<sha>` hash |
| `assemble-video` can't find FFmpeg | System FFmpeg not installed | `sudo apt install ffmpeg` (Ubuntu) or `brew install ffmpeg` (macOS). Set `FFMPEG_PATH`. |
| Project stuck at "Synthesizing… 65%" forever | Pre-NF-6: step threw but didn't call `setProjectFailed` | Fixed (NF-6). To clean up ghosts: `UPDATE projects SET status='failed' WHERE status NOT IN ('completed','failed') AND created_at < '2026-07-02';` |

### 10.3 Test Failures

| Error | Cause | Fix |
|---|---|---|
| `Cannot find module 'next/server'` | jsdom can't load Next.js server modules | Mock `next-auth`, `next/navigation`, `@/lib/db` in tests |
| `Cannot access 'X' before initialization` | `vi.mock()` factory references outer `vi.fn()` | Use `vi.hoisted()`: `const { mockFn } = vi.hoisted(() => ({ mockFn: vi.fn() }))` |
| `X is not a constructor` | Mock factory returns arrow fn, real code does `new X()` | Use `class` syntax: `class MockS3Client { send = sendMock; }` |
| `Expected '>' but found 'Identifier'` | Test file has JSX but `.test.ts` extension | Rename to `*.test.tsx` |
| `fetch failed: ENOTFOUND r2.example.com` | Steps 5 & 6 use `fetch()` for R2 downloads | `vi.stubGlobal('fetch', fetchMock)` |
| SSE route returns 307 instead of 401 JSON | Used `verifySession()` (redirects) instead of `auth()` | API routes use `auth()` directly: returns null → 401 JSON |

### 10.4 Visual / Styling Issues

| Issue | Cause | Fix |
|---|---|---|
| Tailwind classes not applying | Missing `@source` directives | Check `globals.css` has `@source '../components/**/*.{ts,tsx}'` |
| Outfit weight 820 not rendering | Used `next/font/google` (only serves discrete weights) | Must use `next/font/local` with the woff2 file |
| Amber color looks wrong | Used Tailwind's `amber-400` (`#fbbf24`) instead of `#febf00` | Use `bg-primary` / `text-primary` tokens. `brand-tokens.test.ts` catches this. |
| Cross-origin dev resource blocked | Next.js blocks `/_next/webpack-hmr` from non-localhost | Add origin to `allowedDevOrigins` in `next.config.ts` |
| Hydration mismatch console error | Grammarly extension injects `<body>` attributes | `suppressHydrationWarning` on both `<html>` and `<body>` (already applied) |

### 10.5 Live-Site Verification Commands

```bash
# Health check (DB + FFmpeg + config)
curl -s https://storyintovideo.jesspete.shop/api/health | jq

# Security headers (should show 6 headers incl. CSP + HSTS)
curl -I https://storyintovideo.jesspete.shop/ | grep -iE "x-frame|x-content|referrer|permissions|content-security|strict-transport"

# Protected route redirect (should 307 to same-host /sign-in)
curl -sI https://storyintovideo.jesspete.shop/dashboard | grep -i location

# Custom 404 (should return 404, not 200)
curl -sI https://storyintovideo.jesspete.shop/nonexistent | head -1

# Verify production mode (no dev chunks)
# In browser console: should NOT see [HMR] connected or [Fast Refresh]
# JS chunk names should be content-hashed, not source-path names
```

---

## 11. Pre-Ship Checklist

Before claiming any task is complete, verify ALL of the following:

### 11.1 Quality Gate (must pass clean)
```bash
pnpm lint           # 0 warnings (ESLint flat config)
pnpm typecheck      # 0 errors (tsc --noEmit, strict + noUncheckedIndexedAccess)
pnpm test           # 524 unit tests pass (58 files)
pnpm test:e2e       # 48 E2E tests pass (10 spec files, requires Playwright browsers)
pnpm format:check   # All files pass Prettier
pnpm build          # 0 errors (hybrid: static + dynamic)
```

### 11.2 CI Guard
- The `quality-gate` job in `.github/workflows/ci.yml` runs all 6 commands above.
- The CI guard step "Verify build output contains no dev-only chunks (hmr-client)" must pass — greps `.next/` for `hmr-client`.

### 11.3 Pre-Deployment Env Validation
```bash
node scripts/check-env.js
# Checks: host-mismatch, AUTH_SECRET ≥32 chars, placeholder API keys, missing required vars
```

### 11.4 Post-Deploy Live-Site Smoke Test (30-Second Check)

After every deploy, run this shell script to catch operational misconfigurations that unit tests cannot detect (the `NEXT_PUBLIC_APP_URL=localhost` failure on 2026-06-29 was discovered exactly this way):

```bash
#!/bin/bash
set -e

HOST="https://storyintovideo.jesspete.shop"
REDIRECT=$(curl -sI "$HOST/dashboard" | grep -i location | tr -d '\r')

# 1. Verify auth redirect stays on same host (catches NEXT_PUBLIC_APP_URL misconfig)
if echo "$REDIRECT" | grep -q "localhost"; then
  echo "FAIL: Redirects to localhost — env NEXT_PUBLIC_APP_URL is wrong"
  exit 1
fi

# 2. Verify /api/health returns healthy DB + FFmpeg + configHealthy (H9 + T2)
curl -s "$HOST/api/health" | jq '.status == "healthy" and .config.healthy' | grep true

# 3. Verify known routes return 200
for path in / /pricing /blog /contact /privacy /terms; do
  code=$(curl -s -o /dev/null -w "%{http_code}" "$HOST$path")
  [[ "$code" == "200" ]] || { echo "FAIL: $path returned $code"; exit 1; }
done

# 4. Verify 404 page returns proper 404 (not 200 with marketing title)
code=$(curl -s -o /dev/null -w "%{http_code}" "$HOST/nonexistent")
[[ "$code" == "404" ]] || { echo "FAIL: 404 returned $code"; exit 1; }

echo "✅ Smoke test passed"
```

### 11.5 Post-Deployment Verification
```bash
node scripts/verify-deployment.js
# 9 checks: /api/health, /dashboard redirect, /pricing+/blog+/contact 200, /sign-in, 404, /privacy+/terms
```

### 11.5 Visual Verification
- [ ] Marketing page visually indistinguishable from `storyintovideo.com` at 1440×900
- [ ] Lighthouse ≥95 across Performance, Accessibility, Best Practices, SEO (marketing page)
- [ ] All 14 marketing CTAs wired to real routes
- [ ] FAQ accordion single-open behavior works
- [ ] Mobile hamburger Sheet opens with 6 links
- [ ] Cookie banner is dismissible via keyboard
- [ ] Skip-to-content link appears on first Tab press

### 11.6 Security Verification
- [ ] `curl -I` shows 6 security headers (incl. CSP + HSTS)
- [ ] Browser console does NOT show `[HMR] connected` or `[Fast Refresh]` (production mode)
- [ ] JS chunk names are content-hashed (not source-path names)
- [ ] No `amber-300/400/500/600` or `bg-zinc-950/900/black` violations (`brand-tokens.test.ts` passes)

### 11.7 Pre-Launch External Services
- [ ] Neon database provisioned + migrations applied
- [ ] Google OAuth credentials configured (optional)
- [ ] OpenAI / Replicate / ElevenLabs API keys set
- [ ] `REPLICATE_SDXL_IPADAPTER_MODEL` set to real `lucataco/sdxl-ipadapter:<sha>`
- [ ] Stripe products created + `PRICE_IDS` updated (currently placeholders)
- [ ] Cloudflare R2 (3 buckets) provisioned
- [ ] Inngest + Upstash + Resend accounts configured
- [ ] `AUTH_URL` and `NEXT_PUBLIC_APP_URL` both set to the production HTTPS URL (T1 will throw if they differ)

---

## 12. Lessons Learnt & How to Avoid Them

### Marketing Layer (Inherited)

1. **`suppressHydrationWarning` on `<body>`, not just `<html>`** — Browser extensions inject attributes before React hydrates. `<html>` alone is insufficient.
2. **Workflow is `'use client'`** — Uses `useState` for video loading choreography. Don't assume server components for "mostly static" sections.
3. **Test counts drift from plans** — MEP planned 6+3, actual is 524 unit + 48 E2E. Always verify against `pnpm test` output.
4. **File structure evolves** — `features/`, `lib/db/`, `lib/ai/`, `lib/auth/`, `lib/storage/`, `lib/inngest/`, `lib/stripe/`, `lib/env/` were created during production build. Update docs as you build.
5. **Playwright needs separate install** — `pnpm install` doesn't install browser binaries.
6. **Zod v4 `.url()` accepts any scheme** — compose `.url()` with `.refine()` for protocol restriction.
7. **Env validation needs build-context fallback** — without it, `next build` fails during page-data collection.
8. **`postgres()` defers connection until first query** — allows eager db instantiation without breaking the build.
9. **DrizzleAdapter validates db object structure** — a Proxy-based lazy db was rejected; use a real Drizzle client.
10. **Inngest v4 changed `createFunction` signature** — trigger is now in the config object, not a second argument.
11. **Auth unit tests must mock `next-auth` + `next/navigation`** — jsdom can't load `next/server`.
12. **Source-reading tests are valid** for server-only modules (auth config, middleware, route handlers) that can't be rendered in jsdom.

### Production App Layer

13. **`verifySession()` throws `NEXT_REDIRECT`** — never wrap in try/catch; the redirect must propagate.
14. **API routes use `auth()`, not `verifySession()`** — `auth()` returns null → 401 JSON. `verifySession()` redirects (wrong for JSON responses).
15. **Client components never import `r2.ts`** — env validation crashes in the browser.
16. **`trustHost: true` is required for reverse-proxy deployments** — Auth.js v5 uses the request's Host header instead of `AUTH_URL`.
17. **Stripe "Basil" API (2025-03-31) moved `current_period_end`** — from top-level to `items.data[0].current_period_end`. The `extractSubscriptionPeriodEnd()` helper handles both shapes.
18. **`debitCredits()` must be idempotent** — uses `ON CONFLICT (idempotency_key) DO NOTHING` + `.for('update')` row lock. Returns `DebitResult { idempotent, eventId, creditsRemaining }`.
19. **`createProjectAction` must insert BEFORE debiting** — if the insert fails, the user loses nothing. The INSERT + debit are wrapped in `db.transaction()` via `debitCreditsTx`.
20. **`IMAGE_MODERATION_FAIL_OPEN` defaults to `'false'` in production** (H8) — fail-closed is the secure default. `'true'` in dev/test for convenience.

### Audit-v2 Lessons (2026-07-02)

21. **`next dev` in production is a silent failure mode** (NF-1) — symptoms: 5-10× slower, source paths leak, HMR WebSocket exposed, `cache-control: no-cache`. Unit tests can't catch this — it's operational. Lesson: always ship a production Dockerfile + CI guard that greps for `hmr-client`.
22. **CSP `'unsafe-inline'` is required for Next.js App Router** (NF-2) — Next.js injects inline `<script>` chunks for router state. Ship `'unsafe-inline'` first (better than no CSP), upgrade to nonce-based later.
23. **Three-way drift between DB enum, UI array, and marketing copy is easy to miss** (NF-3) — derive user-facing counts from the source-of-truth array OR add a regression test.
24. **Dead exports accumulate silently across sprints** (NF-4) — every export should have at least one importer. If a constant is declared, USE it at the call site.
25. **Docs claiming "dep installed" when it isn't is a real bug** (NF-5) — verify doc claims against `package.json` at doc-writing time.
26. **Pipeline steps without try/catch create ghost "in progress" projects** (NF-6) — every step that can throw must catch + `setProjectFailed` + re-throw. Exception: the final "mark complete" step (work is done, don't mark it failed).

### Audit-v1 Remediation Lessons (27–50, condensed)

27. **Server Action forms must live in a `"use server"` module** — defining inline in a Server Component page causes build failure (T1).
28. **Behind a TLS-terminating reverse proxy, `nextUrl.origin` lies** — always use `env.NEXT_PUBLIC_APP_URL` for redirects (T2).
29. **Idempotency-key-too-early is a silent data-loss anti-pattern** — INSERT the idempotency row **AFTER** side effects succeed (T4).
30. **Upstash `fixedWindow` rate limiters can't release on disconnect** — use Redis `SET NX EX` + `DEL` for connection-counting (T5).
31. **Drizzle transactions can't be nested** — extract a `*Tx(tx, ...)` variant that accepts the transaction handle (T3).
32. **Source-reading tests must search for `.method()` not `db.method()`** — multiline chains break `indexOf` on the receiver (T4 test).
33. **TypeScript doesn't preserve `session.user.id` narrowing inside closures** — capture `const userId: string = session.user.id` before the closure (T5).
34. **`appendVideo` setting `status='completed'` at insert time is a state-machine lie** — use `'rendering'` at insert, `'completed'` on completion (T8).
35. **Module-load constants make env-configurable behavior untestable per-call** — move the read into a function body (T9).
36. **Dead exports accumulate silently across sprints** — every export should have at least one importer (NF-4).
37. **Large mechanical sweeps need scripted `sed`, not manual edits** — Rule of 500: use automation for >500-line refactors (T11).
38. **`metadataBase` hardcoded to a placeholder breaks social sharing** — use `env.NEXT_PUBLIC_APP_URL` (T12/L-4).
39. **`Date.now()` temp file names collide under concurrency** — use `crypto.randomUUID()` (T12/L-3).
40. **`EventSource.close()` is idempotent but sloppy** — set `eventSource = null` after close to guard against double-close (T12/L-2).
41. **R2 error classification matters for operators** — 502/504/500 lets operators distinguish transient from permanent failures (T6).
42. **Payment failure should not silently zero-out credits** — return `InsufficientCreditsError` so the user sees why the pipeline didn't start (T3).
43. **The `complete` step must NOT call `setProjectFailed`** — the video is already in R2; marking failed would contradict reality (NF-6).
44. **Every `debitCredits` call MUST pass an `idempotencyKey`** — no exceptions. Deterministic per (project, step, entity) (C5).
45. **Replicate scene generation 404s silently if IP-Adapter model is a placeholder** — validate model format in env schema (T4).
46. **Client component imports of `r2.ts` crash the browser** — `env` module validates 30 vars at load; only `NEXT_PUBLIC_*` exist client-side (H4).
47. **`FFMPEG_PATH` must go through the Zod env schema** — `process.env.FFMPEG_PATH` bypasses validation (H1).
48. **Host Header Injection is a real attack vector** — validate Host header in proxy against whitelist (H6).
49. **Stripe webhook TOCTOU race was a silent revenue leak** — concurrent webhooks could double-charge; `ON CONFLICT DO NOTHING` + pre-check SELECT prevents it (H7).
50. **Production env misconfigurations should fail-fast** — `console.warn` is insufficient; throw at module load in production (T1).

### Sprint 3 Lessons (51–55)

51. **Legal pages must not promise features the code doesn't implement** — every right promised in legal copy must trace to a working endpoint (T3/T4).
52. **`<a href>` vs `<Link>` drift is easy to miss in source-reading tests** — assert both the route AND the component type (T5).
53. **Next.js default 404 inherits root layout metadata** — always ship a custom `not-found.tsx` (T7).
54. **`useSyncExternalStore` is the SSR-safe way to read `localStorage`** — avoids the `react-hooks/set-state-in-effect` lint rule (T8).
55. **R2 cleanup on account deletion is best-effort** — DB cascade always succeeds; R2 errors are logged but don't fail the GDPR request (T4).

### Audit-v2 Lessons (2026-07-02)

56. **`next dev` in production is a silent failure mode** (NF-1) — symptoms: 5-10× slower, source paths leak, HMR WebSocket exposed, `cache-control: no-cache`. Unit tests can't catch this — it's operational. Lesson: always ship a production Dockerfile + CI guard that greps for `hmr-client`.
57. **CSP `'unsafe-inline'` is required for Next.js App Router** (NF-2) — Next.js injects inline `<script>` chunks for router state. Ship `'unsafe-inline'` first (better than no CSP), upgrade to nonce-based later.
58. **Three-way drift between DB enum, UI array, and marketing copy is easy to miss** (NF-3) — derive user-facing counts from the source-of-truth array OR add a regression test.
59. **Docs claiming "dep installed" when it isn't is a real bug** (NF-5) — verify doc claims against `package.json` at doc-writing time.
60. **Pipeline steps without try/catch create ghost "in progress" projects** (NF-6) — every step that can throw must catch + `setProjectFailed` + re-throw. Exception: the final "mark complete" step.

---

## 13. Pitfalls to Avoid

### 13.1 Architecture Pitfalls

- **Do NOT add `tailwind.config.ts`** — all tokens belong in `globals.css` `@theme`.
- **Do NOT use `next/font/google` for Outfit** — it can't serve weight 820.
- **Do NOT use Framer Motion or GSAP** — all animation is CSS-only.
- **Do NOT use camelCase keyframes** — kebab-case is the modern convention.
- **Do NOT read `process.env.*` directly** — use the Zod-validated `env` module.
- **Do NOT wrap `verifySession()` in try/catch** — it throws `NEXT_REDIRECT` which must propagate.
- **Do NOT put DB access in components** — use the `queries.ts` boundary.
- **Do NOT put DB access in middleware/proxy** — Edge runtime can't access DB.
- **Do NOT make R2 buckets public** — use signed URLs.
- **Do NOT skip content moderation** — every story input must be moderated (ADR-011).
- **Do NOT use `force-static` on app routes** — only the marketing page can be static.
- **Do NOT use `any`** — ESLint will error. Use `unknown` or proper types.
- **Do NOT add CDN links** — all assets are self-hosted.
- **Do NOT use default exports for components** — use named exports.
- **Do NOT skip the verification chain** — `pnpm lint && pnpm typecheck && pnpm test && pnpm build`.
- **Do NOT use `db push` in production** — always `drizzle-kit generate` + `migrate`.
- **Do NOT deploy with `next dev`** — always use the production `Dockerfile` (`next start`). (NF-1)
- **Do NOT ship a pipeline step without try/catch** — every step must call `setProjectFailed` on error. Exception: the `complete` step. (NF-6)

### 13.2 Dependency Pitfalls

- **Do NOT install `@ffmpeg-installer/ffmpeg`** — Turbopack-incompatible. Use system FFmpeg.
- **Do NOT claim `@aws-sdk/lib-storage` is installed** — it is NOT in `package.json`. (NF-5)
- **Do NOT claim `@sentry/nextjs` is installed** — it is NOT. `SENTRY_DSN` is env-schema-only. (NF-5)
- **Do NOT downgrade React below 19.2.3** — CVE-2025-55182 (React2Shell RCE).
- **Do NOT use `onlyBuiltDependencies` in `pnpm-workspace.yaml`** — use `allowBuilds` (pnpm 10.26+ syntax).

### 13.3 Testing Pitfalls

- **Do NOT use `vi.fn()` directly in `vi.mock()` factory** — use `vi.hoisted()` to avoid "Cannot access X before initialization".
- **Do NOT return arrow functions from mock factories** when the real code does `new X()` — use `class` syntax.
- **Do NOT forget to add `WHISPER_MODEL` to `@/lib/ai/openai` mocks** — `align-subtitles.ts` imports it. (NF-4)
- **Do NOT forget `vi.stubGlobal('fetch', fetchMock)`** — Steps 5 & 6 use `fetch()` for R2 downloads.
- **Do NOT use `.test.ts` for files with JSX** — rename to `.test.tsx`.

---

## 14. Best Practices

### 14.1 TypeScript
- `strict: true` + `noUncheckedIndexedAccess` + `verbatimModuleSyntax` + `noImplicitOverride`
- `interface` for object shapes, `type` for unions/intersections
- Explicit `type` imports: `import type { Metadata } from 'next'`
- Early returns over deeply nested conditionals
- Composition over inheritance
- Never use `any` — use `unknown` if the type is truly unknown

### 14.2 React / Next.js
- Server Components by default; `'use client'` only when needed
- Named function exports (never default)
- `interface` for all props
- `cn()` utility for conditional class merging
- `suppressHydrationWarning` on `<html>` AND `<body>`
- Handle all UI states: loading, error, empty, success
- `next/link` for all internal navigation (never `<a>`)
- `next/image` for all raster images
- `next/font` for all fonts
- Async `params` / `searchParams` / `cookies()` — always `await` them (Next.js 16)

### 14.3 Tailwind CSS v4
- CSS-first `@theme` block in `globals.css` (no `tailwind.config.ts`)
- `@source` directives for content scanning
- `@utility` for single-purpose helpers (replaces v3 `@layer components`)
- Kebab-case keyframes
- Hex color tokens preserved verbatim (no OKLCH conversion)
- Custom `--color-primary: #febf00` (NOT Tailwind's `amber-400`)

### 14.4 Security
- Zod env validation (never `process.env.*` directly)
- `verifySession()` first in every Server Action
- `auth()` in API routes (returns null → 401 JSON)
- Stripe webhook signature verification
- R2 buckets private; signed URLs only
- bcrypt cost factor 12
- Rate limiting on auth (10/15min/IP), pipeline (5/min/user), SSE (slot pattern)
- 6 security headers incl. CSP + HSTS (NF-2)
- Host header validation in proxy (H6)

### 14.5 Testing (TDD)
- RED (failing test) → GREEN (minimum fix) → REFACTOR → VERIFY
- Source-reading tests for server-only modules (strip comments before regex)
- Factory pattern for test data: `getMockX(overrides)`
- `vi.hoisted()` for mock functions referenced in `vi.mock()` factories
- Test behavior, not implementation
- Run `pnpm test` before every commit

### 14.6 Pipeline (Inngest)
- Every step is idempotent (deterministic idempotency keys)
- `debitCredits` uses `ON CONFLICT DO NOTHING` + `.for('update')` row lock
- `append*` queries use `onConflictDoNothing` on unique indexes
- Every step wraps in try/catch with `setProjectFailed` + re-throw (NF-6)
- The `complete` step logs-only (video is already in R2)
- `createProjectAction` wraps INSERT + debit in `db.transaction()`

---

## 15. Coding Patterns

### 15.1 Complete `createProjectAction` Walkthrough (7 Steps — T3/C3/C4/T7)

```typescript
// src/features/projects/actions.ts
'use server';

import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';
import { z } from 'zod';
import { db } from '@/lib/db';
import { projects } from '@/lib/db/schema';
import { verifySession } from '@/features/auth/domain/verify-session';
import { moderateContent } from '@/features/pipeline/domain/moderate-content';
import {
  debitCreditsTx,
  getOrCreateSubscription,
  InsufficientCreditsError,
} from '@/features/billing/queries';
import { CREDIT_COSTS } from '@/features/billing/domain/tier-limits';
import { inngest, PIPELINE_EVENT } from '@/lib/inngest/client';
import { pipelineRateLimit } from '@/lib/rate-limit';
import { setProjectFailed } from '@/features/pipeline/queries';

export async function createProjectAction(
  input: z.infer<typeof CreateProjectSchema>,
): Promise<CreateProjectResult> {

  // ── 1. AUTH FIRST ──
  const session = await verifySession({ redirectTo: '/create' });
  const userId = session.user?.id;
  if (!userId) {
    return { success: false, error: 'Not authenticated', code: 'UNAUTHORIZED' };
  }

  // ── 2. RATE LIMIT (C3: 5/min/user) ──
  const { success: rateLimitOk } = await pipelineRateLimit.limit(userId);
  if (!rateLimitOk) {
    return { success: false, error: 'You are creating projects too quickly.', code: 'RATE_LIMITED' };
  }

  // ── 3. ZOD VALIDATE ──
  const parsed = CreateProjectSchema.safeParse(input);
  if (!parsed.success) { /* return VALIDATION */ }

  // ── 4. CONTENT MODERATION ──
  const moderation = await moderateContent(parsed.data.story);
  if (moderation.flagged) { /* return FLAGGED */ }

  // ── 5. ENSURE SUBSCRIPTION EXISTS ──
  await getOrCreateSubscription(userId);

  // ── 6. INSERT + DEBIT IN A SINGLE TRANSACTION (T3/H-1) ──
  // If debit throws InsufficientCreditsError, the transaction rolls back
  // and NO orphan project row is committed. The user sees a clean error.
  let projectId: string;
  try {
    projectId = await db.transaction(async (tx) => {
      const [project] = await tx
        .insert(projects)
        .values({ /* ... */ })
        .returning({ id: projects.id });

      await debitCreditsTx(
        tx, userId, CREDIT_COSTS.analysis, 'analysis',
        `${project.id}:analysis`,
        project.id,
      );

      return project.id;
    });
  } catch (err) {
    if (err instanceof InsufficientCreditsError) {
      return { success: false, error: err.message, code: 'INSUFFICIENT_CREDITS' };
    }
    throw err;
  }

  // ── 7. TRIGGER INNGEST (T7: try/catch → setProjectFailed) ──
  try {
    await inngest.send({ name: PIPELINE_EVENT, data: { projectId } });
  } catch (err) {
    await setProjectFailed(projectId, 'Failed to queue the AI pipeline.');
    return { success: false, error: 'Failed to queue the AI pipeline.', code: 'INTERNAL' };
  }

  revalidatePath('/dashboard');
  redirect(`/projects/${projectId}`);
}
```

### 15.2 API Route Pattern (force-dynamic)
```typescript
// src/app/api/projects/[id]/download/route.ts
export const dynamic = 'force-dynamic';

export async function GET(
  request: Request,
  { params }: { params: Promise<{ id: string }> },  // Next.js 16: params is Promise
) {
  const session = await auth();  // NOT verifySession() — returns null → 401 JSON
  if (!session) return Response.json({ error: 'Unauthorized' }, { status: 401 });
  
  const { id } = await params;  // await the Promise
  
  // Owner check, business logic...
  return Response.json({ url: signedUrl });
}
```

### 15.3 Domain Function Pattern (Pure)
```typescript
// src/features/pipeline/domain/align-subtitles.ts
import { openai, WHISPER_MODEL } from '@/lib/ai/openai';

export interface AlignSubtitlesInput {
  audioBuffer: Buffer;
  language?: string;
}

export async function alignSubtitles(input: AlignSubtitlesInput) {
  // Pure function — no Next.js imports, no DB imports
  // Can import types from @/lib/ai/openai but not runtime code
  const language = input.language ?? 'en';
  const transcription = await openai.audio.transcriptions.create({
    file: new File([new Uint8Array(input.audioBuffer)], 'voiceover.mp3', { type: 'audio/mp3' }),
    model: WHISPER_MODEL,  // NF-4: use the constant, don't hardcode
    language,
    response_format: 'verbose_json',
    timestamp_granularities: ['word'],
  });
  // ... pure logic
}
```

### 15.4 Idempotent Credit Debit Pattern
```typescript
// C5 fix: ON CONFLICT DO NOTHING + SELECT FOR UPDATE
export async function debitCreditsTx(
  tx: db, // transaction handle from caller
  userId: string,
  amount: number,
  operationType: UsageEventType,
  idempotencyKey: string,
  projectId?: string,
): Promise<DebitResult> {
  // 1. Insert idempotency row FIRST (ON CONFLICT DO NOTHING)
  const [idempotencyRow] = await tx.insert(usageEvents)
    .values({ userId, projectId, type: operationType, cost: amount, idempotencyKey })
    .onConflictDoNothing({ target: usageEvents.idempotencyKey })
    .returning();
  
  if (!idempotencyRow) return { idempotent: true, eventId: null, creditsRemaining: null };
  
  // 2. SELECT FOR UPDATE on the subscription row (row lock)
  const [subscription] = await tx.select().from(subscriptions)
    .where(eq(subscriptions.userId, userId)).for('update');
  
  if (subscription.creditsRemaining < amount) {
    throw new InsufficientCreditsError(amount, subscription.creditsRemaining);
  }
  
  // 3. Update the balance
  await tx.update(subscriptions).set({
    creditsRemaining: subscription.creditsRemaining - amount,
  }).where(eq(subscriptions.userId, userId));
  
  return { idempotent: false, eventId: idempotencyRow.id, creditsRemaining: subscription.creditsRemaining - amount };
}
```

### 15.5 SSE Slot Pattern (T5 fix)
```typescript
// claimSseSlot / releaseSseSlot / refreshSseSlot
// Uses Redis SET NX EX 30 (exclusive lock with 30s TTL)
// On disconnect: DEL the key (immediate release)
// On poll: EXPIRE the key (refresh TTL)
// If server crashes: key auto-expires after 30s
```

### 15.6 Pipeline Step with Error Handling (NF-6)
```typescript
await step.run('synthesize-voiceover', async () => {
  await updateProjectProgress(projectId, 'synthesizing_voice', 'Synthesizing voiceover…', 65);
  try {
    // ... step logic ...
  } catch (err) {
    const message = err instanceof Error ? err.message : String(err);
    await setProjectFailed(projectId, `Voiceover synthesis failed: ${message}`);
    throw err;  // Re-throw so Inngest still retries
  }
});

// The complete step is special — logs-only, NO setProjectFailed
await step.run('complete', async () => {
  try {
    await updateProjectProgress(projectId, 'completed', 'Your video is ready!', 100);
  } catch (err) {
    console.error(`[pipeline] Failed to mark project ${projectId} as completed (video is in R2):`, err);
    // Do NOT call setProjectFailed — the video is already in R2, user can still download
  }
});
```

---

## 16. Coding Anti-Patterns

### 16.1 TypeScript Anti-Patterns
```typescript
// ❌ DON'T: use any
function process(data: any) { ... }

// ✅ DO: use unknown + narrow
function process(data: unknown) {
  if (typeof data === 'string') { ... }
}

// ❌ DON'T: default export for components
export default function Hero() { ... }

// ✅ DO: named export
export function Hero() { ... }

// ❌ DON'T: type for object shapes
type User = { id: string; name: string };

// ✅ DO: interface for object shapes
interface User { id: string; name: string }
```

### 16.2 React Anti-Patterns
```tsx
// ❌ DON'T: wrap verifySession in try/catch
try {
  await verifySession();
} catch (e) {
  // This swallows the NEXT_REDIRECT — breaks auth!
}

// ❌ DON'T: import r2.ts in client components
'use client';
import { getSignedDownloadUrl } from '@/lib/storage/r2'; // Crashes in browser!

// ❌ DON'T: use <a> for internal routes
<a href="/dashboard">Dashboard</a>  // Full-page reload

// ✅ DO: use <Link>
<Link href="/dashboard">Dashboard</Link>  // Client-side nav

// ❌ DON'T: forget suppressHydrationWarning
<html lang="en" className={fontVariables}>  // Grammarly causes hydration mismatch

// ✅ DO: add to both html and body
<html lang="en" className={fontVariables} suppressHydrationWarning>
  <body suppressHydrationWarning>
```

### 16.3 Tailwind Anti-Patterns
```tsx
// ❌ DON'T: use Tailwind's amber-400 (it's #fbbf24, not #febf00)
<button className="bg-amber-400 text-black">

// ✅ DO: use the custom primary token
<button className="bg-primary text-primary-foreground">

// ❌ DON'T: add tailwind.config.ts
// ✅ DO: use @theme block in globals.css

// ❌ DON'T: use camelCase keyframes
@keyframes fadeInUp { ... }

// ✅ DO: use kebab-case
@keyframes fade-in-up { ... }
```

### 16.4 Pipeline Anti-Patterns
```typescript
// ❌ DON'T: debit before insert (orphan rows on failure)
await debitCredits(userId, 5, 'analysis', key);
await db.insert(projects).values({...});  // If this fails, user lost credits

// ✅ DO: insert + debit in a transaction
await db.transaction(async (tx) => {
  const [project] = await tx.insert(projects).values({...}).returning();
  await debitCreditsTx(tx, userId, 5, 'analysis', `${project.id}:analysis`);
});

// ❌ DON'T: ship a step without try/catch (ghost projects)
await step.run('analyze-story', async () => {
  return analyzeStory(project.story);  // If this throws, project stuck at 10% forever
});

// ✅ DO: wrap in try/catch with setProjectFailed (NF-6)
await step.run('analyze-story', async () => {
  try {
    return await analyzeStory(project.story);
  } catch (err) {
    await setProjectFailed(projectId, `Analysis failed: ${err.message}`);
    throw err;
  }
});
```

---

## 17. Responsive Breakpoint Reference

The project uses Tailwind's default breakpoints (no custom config):

| Prefix | Min-width | Usage in this project |
|---|---|---|
| (default) | 0px | Mobile-first base styles |
| `sm:` | 640px | Hero padding increase, hero margin-top increase |
| `md:` | 768px | (rarely used — jump from sm to lg) |
| `lg:` | 1024px | H2 font-size jump (`text-4xl lg:text-6xl`), grid column changes |
| `xl:` | 1280px | Max-width containers |
| `2xl:` | 1536px | (rarely used) |

**Key responsive patterns:**
- **Hero H1:** `text-4xl` on mobile → `text-[4.5rem]` on desktop (inline style for the 820 weight)
- **Section H2:** `text-4xl lg:text-6xl` with `clamp(2rem, 5vw, 3rem)` via `@utility section-heading`
- **Marquee speed:** 40s on desktop → 30s on mobile (`@media (max-width: 640px)` in `@utility marquee-track`)
- **Navbar:** Desktop shows inline links; mobile shows hamburger → Sheet
- **Glass input padding:** `1.25rem` on mobile → `1.5rem` on `sm:` (`@utility glass-input`)
- **Workflow section:** Desktop alternates media left/right; mobile always stacks media-above-text

**Mobile testing:** Use `agent-browser set device "iPhone 14"` for consistent mobile verification.

---

## 18. Z-Index Layer Map

| Z-Index | Element | Location | Purpose |
|---|---|---|---|
| `z-50` | Navbar (fixed) | `navbar.tsx:39` | Stays above page content on scroll |
| `z-50` | Skip-to-content link (on focus) | `layout.tsx:71` | Visible above all content when focused |
| `z-50` | Sheet overlay (Radix Dialog backdrop) | `sheet.tsx:29` | Mobile nav backdrop |
| `z-50` | Sheet content (Radix Dialog panel) | `sheet.tsx:53` | Mobile nav panel |
| `z-50` | Dropdown menu content (Radix) | `dropdown-menu.tsx:30,200` | Language dropdown |
| `z-40` | Cookie banner (fixed bottom) | `cookie-banner.tsx:93` | Above page content, below nav/sheets |
| `z-10` | Hero content (relative to bg video) | `hero.tsx:63,180` | Above the hero background video |
| `z-10` | Final CTA content | `final-cta.tsx:40` | Above background effects |
| `-z-10` | Example card hover gradient | `examples.tsx:88` | Behind the card content |

**Radix portal elements** (rendered to `document.body`, so they're above everything):
- Sheet overlay + content
- Dropdown menu content
- (Radix manages z-index internally for these)

**Rule of thumb:** `z-50` for fixed/sticky UI (nav, sheets, dropdowns, skip-link), `z-40` for banners, `z-10` for content above background media, `-z-10` for decorative backgrounds.

---

## 19. Color Reference (Complete)

### 19.1 Semantic Tokens (from `@theme` in `globals.css`)

| Token | Hex | RGB | Tailwind Class | Usage |
|---|---|---|---|---|
| `--color-background` | `#020202` | `2, 2, 2` | `bg-background` | Page background |
| `--color-foreground` | `#f8f8f8` | `248, 248, 248` | `text-foreground` | Default foreground (headings) |
| `--color-card` | `#060607` | `6, 6, 7` | `bg-card` | Card surfaces |
| `--color-card-foreground` | `#f8f8f8` | `248, 248, 248` | `text-card-foreground` | Text on cards |
| `--color-popover` | `#0b0b0d` | `11, 11, 13` | `bg-popover` | Dropdown/sheet backgrounds |
| `--color-popover-foreground` | `#f8f8f8` | `248, 248, 248` | `text-popover-foreground` | Text in popovers |
| `--color-primary` | `#febf00` | `254, 191, 0` | `bg-primary` / `text-primary` | CTAs, active states, focus rings |
| `--color-primary-foreground` | `#020202` | `2, 2, 2` | `text-primary-foreground` | Text on amber CTAs |
| `--color-secondary` | `#111114` | `17, 17, 20` | `bg-secondary` | Secondary surfaces |
| `--color-secondary-foreground` | `#f8f8f8` | `248, 248, 248` | `text-secondary-foreground` | Text on secondary |
| `--color-muted` | `#1a1a1d` | `26, 26, 29` | `bg-muted` | Muted backgrounds |
| `--color-muted-foreground` | `#8e8e95` | `142, 142, 149` | `text-muted-foreground` | Secondary text |
| `--color-accent` | `#febf00` | `254, 191, 0` | `bg-accent` | Same as primary (alias) |
| `--color-accent-foreground` | `#020202` | `2, 2, 2` | `text-accent-foreground` | Text on accent |
| `--color-destructive` | `#ff2d39` | `255, 45, 57` | `bg-destructive` | Error states |
| `--color-destructive-foreground` | `#f8f8f8` | `248, 248, 248` | `text-destructive-foreground` | Text on destructive |
| `--color-border` | `#1a1a1d` | `26, 26, 29` | `border-border` | Default borders |
| `--color-input` | `#0b0b0d` | `11, 11, 13` | `bg-input` | Input backgrounds |
| `--color-ring` | `#febf0080` | `254, 191, 0, 50%` | `ring-ring` | Focus ring (50% opacity amber) |

### 19.2 Chart Palette (Reserved for Future Dashboard)

| Token | Hex |
|---|---|
| `--color-chart-1` | `#febf00` (amber) |
| `--color-chart-2` | `#00aa6f` (green) |
| `--color-chart-3` | `#8d92f9` (periwinkle) |
| `--color-chart-4` | `#f14d4c` (red) |
| `--color-chart-5` | `#7bc27e` (light green) |

### 19.3 Body Text Color (Not a Token — Hardcoded)

Body paragraph text uses `#d4d4d8` (zinc-300) — **NOT** `--color-foreground` (`#f8f8f8`). This gives **12.6:1 contrast on `#020202`** (WCAG AAA). Applied via `text-zinc-300` class in component JSX.

### 19.4 The ONLY Permitted Purple

The example-card hover gradient in `examples.tsx:88`:
```tsx
<div className="absolute inset-0 -z-10 rounded-[20px] bg-gradient-to-r from-yellow-500 to-purple-500 opacity-50 blur-md transition-opacity duration-300 group-hover:opacity-80" />
```
This is the **ONLY** purple on the entire site. Any other purple is a bug.

### 19.5 Forbidden Colors (Enforced by `brand-tokens.test.ts`)

The following Tailwind classes are **FORBIDDEN** in non-test source:
- `amber-300`, `amber-400`, `amber-500`, `amber-600` (use `primary` instead)
- `bg-zinc-950`, `bg-zinc-900`, `bg-black` (use `bg-background` or `bg-card` instead)

`brand-tokens.test.ts` enforces 0 violations via source-reading regex.

---

## 20. The Complete TypeScript Interface Reference

All marketing interfaces live in `src/types/index.ts` (12 interfaces). All use `interface` (not `type` for object shapes) per project convention.

### 20.1 Marketing Interfaces

```typescript
import type { LucideIcon } from 'lucide-react';

/** Navigation link in the Navbar (desktop + mobile Sheet). */
export interface NavLink {
  label: string;
  href: string;
}

/** Story example chip in the Hero — clicking populates the textarea. */
export interface StoryExample {
  label: string;
  /** The multi-paragraph seed text injected into the textarea on click. */
  seed: string;
}

/** Aspect ratio toggle button in the Hero (9:16 portrait or 16:9 landscape). */
export interface AspectRatio {
  label: '9:16' | '16:9';
  value: 'portrait' | 'landscape';
}

/** Portrait example card in the Examples carousel. */
export interface ExampleCard {
  id: string;
  title: string;
  /** Style tag shown below the title (e.g., "Anime · Romance"). */
  styleTag: string;
  /** Path to the 9:16 WebP thumbnail in /public/examples/. */
  thumbnail: string;
  href: string;
}

/** One of the 4 alternating media/text rows in the Workflow section. */
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

/** One of the 8 items in the Features 4×2 hairline grid. */
export interface Feature {
  id: string;
  title: string;
  description: string;
  icon: LucideIcon;
}

/** One of the 6 testimonial cards in the Testimonials 3×2 grid. */
export interface Testimonial {
  id: string;
  quote: string;
  authorName: string;
  authorRole: string;
  /** 2-letter initials rendered in the amber gradient avatar (e.g., "SK"). */
  initials: string;
}

/** One of the 4 use case cards in the UseCases 2×2 grid. */
export interface UseCase {
  id: string;
  title: string;
  description: string;
  icon: LucideIcon;
  href: string;
}

/** One of the 6 items in the FAQ Radix Accordion. */
export interface FAQItem {
  id: string;
  question: string;
  answer: string;
}

/** A single link in the Footer. */
export interface FooterLink {
  label: string;
  href: string;
}

/** A titled column of links in the Footer. */
export interface FooterColumn {
  title: string;
  links: FooterLink[];
}

/** A chip in the Hero style tags marquee. */
export interface StyleChip {
  label: string;
  /** Optional smaller sublabel (only "Cyberpunk" uses this: "Futuristic neon"). */
  sublabel?: string;
}
```

### 20.2 Pipeline Interfaces (in `src/features/pipeline/domain/`)

```typescript
// analyze-story.ts
export interface AnalyzedStory {
  title: string;
  summary: string;
  characters: { name: string; description: string }[];
  scenes: { order: number; description: string; characters: string[]; duration_sec: number }[];
}

// synthesize-voice.ts
export interface SynthesizeVoiceInput {
  text: string;
  voiceId: string;
}
export interface SynthesizeVoiceOutput {
  audioBuffer: Buffer;
  duration: number;
}

// align-subtitles.ts
export interface AlignSubtitlesInput {
  audioBuffer: Buffer;
  language?: string;  // ISO 639-1, defaults to 'en'
}
export interface AlignSubtitlesOutput {
  cues: SubtitleCue[];
  srt: string;
}

// assemble-video.ts
export interface AssembleVideoInput {
  sceneImageUrls: string[];
  sceneDurations: number[];
  audioUrl: string;
  subtitlesSrt: string;
  aspectRatio: 'portrait' | 'landscape';
  resolution: '720p' | '1080p' | '4k';
}
export interface AssembleVideoOutput {
  videoBuffer: Buffer;
  duration: number;
}
```

### 20.3 Billing Interfaces (in `src/features/billing/`)

```typescript
// queries.ts
export interface DebitResult {
  idempotent: boolean;      // true if this idempotency key was already processed
  eventId: string | null;   // the usageEvents.id (null if idempotent)
  creditsRemaining: number | null;  // remaining balance (null if idempotent)
}

export class InsufficientCreditsError extends Error {
  constructor(
    public readonly required: number,
    public readonly available: number,
  ) {
    super(`Insufficient credits: need ${required}, have ${available}`);
    this.name = 'InsufficientCreditsError';
  }
}

// domain/tier-limits.ts
export interface TierLimit {
  monthlyCredits: number;
  maxResolution: '720p' | '1080p' | '4k';
  maxVideoDurationSec: number;
  watermark: boolean;
  priorityQueue: 'standard' | 'priority';
}
export const TIER_LIMITS: Record<'free' | 'creator' | 'pro' | 'studio', TierLimit>;
export const CREDIT_COSTS: Record<string, number>;
export const FULL_PIPELINE_COST = 131;  // 5 + 3×10 + 6×8 + 15 + 3 + 30
```

### 20.4 Pipeline Queries Interfaces (in `src/features/pipeline/queries.ts`)

```typescript
export interface AppendResult<T> {
  inserted: boolean;  // false if onConflictDoNothing hit
  row: T | null;      // null if not inserted
}
export type ProjectStatus = 'draft' | 'pending' | 'analyzing' | 'generating_characters' |
  'generating_scenes' | 'synthesizing_voice' | 'aligning_subtitles' | 'assembling_video' |
  'completed' | 'failed';
```

### 20.5 SSE / Progress Interfaces (in `src/lib/hooks/use-project-progress.ts`)

```typescript
export interface ProjectProgressState {
  status: string | null;
  progressPercent: number | null;
  progressDetail: string | null;
  errorMessage: string | null;
  connectionState: 'connecting' | 'open' | 'closed' | 'error' | 'reconnecting';
}
```

### 20.6 Auth Interfaces (in `src/features/auth/`)

```typescript
// actions.ts
export type SignUpResult =
  | { success: true; userId: string }
  | { success: false; code: 'VALIDATION' | 'EMAIL_EXISTS' | 'INTERNAL' | 'RATE_LIMITED' };

// domain/verify-session.ts
export interface VerifySessionOptions {
  redirectTo?: string;
}
```

### 20.7 Storage Interfaces (in `src/lib/storage/r2.ts`)

```typescript
export type BucketName = 'uploads' | 'generated' | 'videos';

export class PayloadTooLargeError extends Error {
  constructor(
    public readonly actualBytes: number,
    public readonly maxBytes: number,
  ) {
    super(`putObject payload exceeds size limit: ${actualBytes} bytes (max ${maxBytes} bytes)`);
    this.name = 'PayloadTooLargeError';
  }
}

export const MAX_PUT_OBJECT_BYTES = 500 * 1024 * 1024;  // 500 MB
```

---

## Appendix A: ADRs (Architecture Decision Records)

| ADR | Decision | Rationale |
|---|---|---|
| ADR-001 | 5-Layer Architecture with Golden Rule | Isolates business logic from Next.js + DB; enables independent testing |
| ADR-002 | Hybrid Rendering (Static Marketing + Dynamic App) | Static marketing = Lighthouse ≥95; dynamic app = auth/DB access |
| ADR-003 | Stripe "Basil" API Period-End Extraction | Handles 2025-03-31 shape change (`items.data[0].current_period_end`) |
| ADR-004 | Credit-Based Billing (prepaid, not metered) | Simplest for AI products; no overage risk; predictable revenue |
| ADR-005 | Click-Time R2 URL Signing | Eliminates 1h signed-URL expiry trap (stale tabs get 403) |
| ADR-006 | FFmpeg for Video Assembly (with Shotstack fallback) | Self-hosted; ADR-006 specifies Shotstack if serverless FFmpeg is unreliable |
| ADR-007 | Inngest for Pipeline Orchestration | Serverless-native step functions; no Redis needed |
| ADR-008 | Vercel Deployment | Fluid Compute; 800s SSE cap on Pro/Enterprise GA |
| ADR-009 | Drizzle ORM (not Prisma) | SQL-first; lighter runtime; matches Neon serverless |
| ADR-010 | System FFmpeg (not `@ffmpeg-installer/ffmpeg`) | Turbopack-incompatible; `FFMPEG_PATH` env var |
| ADR-011 | Image Moderation on Every AI-Generated Image | Parses Replicate `safety_concept`; fail-closed by default in production |

---

## Appendix B: 6-Step Pipeline Credit Costs

| Step | Operation | Credit Cost | Idempotency Key Pattern |
|---|---|---|---|
| 0 | Moderate story (OpenAI Moderation) | 0 (gate) | — |
| 1 | Analyze story (GPT-4o JSON mode) | 5 | `${projectId}:analysis` |
| 2 | Generate characters (Replicate SDXL) | 10 × N chars | `${projectId}:character:${name}` |
| 3 | Generate scenes (Replicate SDXL + IP-Adapter) | 8 × N scenes | `${projectId}:scene:${order}` |
| 4 | Synthesize voiceover (ElevenLabs TTS) | 15 | `${projectId}:voiceover` |
| 5 | Align subtitles (Whisper ASR) | 3 | `${projectId}:subtitle_alignment` |
| 6 | Assemble video (FFmpeg) | 30 | `${projectId}:video_assembly` |

**Full pipeline cost (3 chars + 6 scenes):** 5 + (10×3) + (8×6) + 15 + 3 + 30 = **131 credits**

Free tier gives 50 credits/month (~0 full videos). Creator tier ($19/mo) gives 500 credits (~3 full videos).

---

## Appendix C: Audit History

### Audit-v1 (2026-06-29) — 16 findings, all closed via T1–T12
See `AUDIT_REPORT_v1.md` + `REMEDIATION_PLAN_v1.md`.

### Audit-v2 (2026-07-02) — 6 findings, all closed via NF-1 through NF-6
See `REMEDIATION_PLAN_v2.md` + `status_13.md`.

| ID | Severity | Finding | Fix |
|---|---|---|---|
| NF-1 | 🔴 Critical | Live site runs `next dev` instead of `next start` | Production Dockerfile + CI guard |
| NF-2 | 🟠 High | Missing CSP + HSTS headers | Added to `next.config.ts` `headers()` |
| NF-3 | 🟡 Medium | FAQ "7+ styles" copy drift | Updated to match `STYLE_CHIPS` (8 styles) |
| NF-4 | 🟡 Medium | Dead/unused exports | Removed `getProjectVideo`, wired `WHISPER_MODEL` |
| NF-5 | 🟡 Medium | Doc inaccuracy (H5/Sentry deps) | Corrected CLAUDE.md/AGENTS.md |
| NF-6 | 🟡 Medium | Pipeline steps lack try/catch | Wrapped steps 1/4/5/6 in try/catch with `setProjectFailed` |

**Test progression:** 479 (Sprint 3) → 524 (audit-v2, +45 new across 5 new test files)

---

---

## Appendix D: Post-Deploy Live-Site Validation

The following methodology complements unit tests and CI — it validates the **live deployment** against operational misconfigurations that automated tests cannot catch (e.g., env var misconfigurations on the production server, DNS issues, reverse-proxy misconfigurations).

### The 2026-06-29 Failure

The `storyintovideo.jesspete.shop` deployment was **fully passing CI** (lint, typecheck, test, build) but **broken in production**:
- `/dashboard` redirected to `http://localhost:3000/sign-in` → `ERR_CONNECTION_REFUSED`
- Root cause: `NEXT_PUBLIC_APP_URL=http://localhost:3000` was set on the production server
- The code was correct; the env var was wrong
- **Unit tests cannot catch this — only a live smoke test can**

### 30-Second Smoke Test Script

Run this after every deploy:

```bash
#!/bin/bash
set -e

HOST="https://storyintovideo.jesspete.shop"
REDIRECT=$(curl -sI "$HOST/dashboard" | grep -i location | tr -d '\r')

# 1. Verify auth redirect stays on same host
echo "$REDIRECT" | grep -q "localhost" && { echo "FAIL: Redirects to localhost"; exit 1; }

# 2. Verify /api/health (DB + FFmpeg + configHealthy)
curl -s "$HOST/api/health" | jq '.status == "healthy" and .config.healthy' | grep true

# 3. Verify known routes return 200
for path in / /pricing /blog /contact /privacy /terms; do
  code=$(curl -s -o /dev/null -w "%{http_code}" "$HOST$path")
  [[ "$code" == "200" ]] || { echo "FAIL: $path returned $code"; exit 1; }
done

# 4. Verify 404 page returns proper 404
code=$(curl -s -o /dev/null -w "%{http_code}" "$HOST/nonexistent")
[[ "$code" == "404" ]] || { echo "FAIL: 404 returned $code"; exit 1; }

echo "✅ Smoke test passed"
```

### `agent-browser` E2E on Live Site

Use the `agent-browser` CLI for deeper validation (navigation, screenshots, DOM inspection):

```bash
# Verify marketing page renders with correct title
agent-browser open https://storyintovideo.jesspete.shop/
agent-browser get title
# Expected: "StoryIntoVideo - Turn Stories Into Videos with AI"

# Verify redirect host matches (not localhost)
agent-browser open https://storyintovideo.jesspete.shop/dashboard
agent-browser get url
# Expected: "https://storyintovideo.jesspete.shop/sign-in?callbackUrl=%2Fdashboard"
# Forbidden: "http://localhost:3000/sign-in?..."
```

### What This Catches (That CI Cannot)

| Failure | CI Can Catch? | Smoke Test Catches? |
|---|---|---|
| Missing env var (build works, runtime fails) | No | Yes — `/api/health` returns 503 |
| `NEXT_PUBLIC_APP_URL=localhost` on prod | No | Yes — redirect points to localhost |
| DNS not propagated to CDN | No | Yes — `curl` fails with NXDOMAIN |
| HSTS not applied | No | Yes — `curl -I` inspects headers |
| Stale assets from previous deploy | No | Yes — if cache headers misconfigured |
| Database migrations not applied | Build passes | Yes — `SELECT 1` returns error → 503 |

### Lessons from Live-Site Validation

1. **CI passing ≠ production working** — CI validates code; smoke tests validate deployment
2. **Env var misconfigurations are the #1 production killer** — they pass CI (placeholders) but break runtime
3. **Always verify the Host header matches the public domain** — `curl -I /dashboard` reveals the redirect target
4. **Run smoke tests from outside the production VPC** — catches DNS, CDN, and TLS issues that internal health checks miss

---

*End of skill file. This document is the canonical reference for the StoryIntoVideo codebase. For the latest status, see `status_13.md`. For the full audit history, see `AUDIT_REPORT_v1.md` + `REMEDIATION_PLAN_v2.md`.*
