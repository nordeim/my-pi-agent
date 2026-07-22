---
name: nextjs16-react19-tailwind4-full-stack
description: >
  Production-grade Next.js 16 full-stack marketing website building with React 19, TypeScript strict, and Tailwind CSS v4 CSS-first @theme design system. Covers App Router Server Components, the 5-layer golden rule architecture (proxy → app → features → domain → lib), graceful degradation for infrastructure clients, Drizzle ORM with PostgreSQL and static fallback data, Auth.js v5 JWT authentication, Inngest step functions, Stripe Checkout payments, Replicate SDXL AI asset generation, Cloudflare R2 storage, Upstash rate limiting, and Zod 4 validation. Includes CSS-only animations, anti-generic brutalist dark-mode aesthetics, cinematic UI design, WCAG AAA accessibility, OWASP security hardening, Vitest + Playwright testing, and pnpm workspace configuration. Use for luxury marketing sites, membership platforms, booking systems, admin dashboards, e-commerce, fitness studio websites, SaaS applications, or any Next.js 16 production-grade full-stack project.
version: 1.1.2
date: 2026-07-03
tags:
  - nextjs
  - react19
  - tailwind-v4
  - drizzle-orm
  - authjs-v5
  - inngest
  - stripe
  - replicate
  - cloudflare-r2
  - wcag-aaa
  - anti-generic
  - luxury-dark
  - full-stack
---

# IRONFORGE — Project SKILL.md

> **How to use this document:** This is the single-source-of-truth reference for any AI coding
> agent working on the IRONFORGE fitness studio codebase. Read §1–§3 before making any changes.
> Consult §9 (Anti-Patterns) and §10 (Debugging Guide) when stuck. Run §11 (Pre-Ship Checklist)
> before every commit.

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
20. [TypeScript Interface Reference](#20-typescript-interface-reference)
21. [Appendices](#21-appendices)

---

## 1. Project Identity & Design Philosophy

### What

IRONFORGE is a production-grade marketing + booking + memberships + admin website for a high-end strength & conditioning studio in NYC. Built with Next.js 16, React 19, Tailwind CSS v4, Drizzle ORM, Auth.js v5, Inngest, Stripe, and Replicate.

### Design Thesis

**"FORGED IN IRON."** Editorial noir meets industrial telemetry. A brand site that looks like a private strength studio at 5:43 AM — dark, sweaty, focused, and unapologetically hardcore.

### Non-Negotiable Design Rules

1. **Pure black canvas** (`#0a0a0a`) — never use white or light backgrounds
2. **Single neon orange accent** (`#ff5400`) — rationed, the ONLY hue that asserts itself
3. **Metallic silver chrome** (`#c8c8c8`) — secondary CTA, equipment reference
4. **B&W noir photography** — `grayscale(100%) contrast(1.55) brightness(0.42)` on all images
5. **Bebas Neue display** at massive sizes (up to 14vw) for hero headlines only
6. **CSS-only animations** — no Framer Motion, no GSAP, no Lottie
7. **`prefers-reduced-motion` disables ALL motion** — not just slows

### Anti-Generic Mandate

**Rejected:**

- Bento grids, hero splits, mesh gradients, glassmorphism
- Inter/Roboto default typography
- Purple/indigo blur, default Tailwind blue, amber-100/200
- Bootstrap-style predictable grids

### CTA Hierarchy

1. **Primary:** `bg-[var(--color-accent)] text-black` — pulsing glow, used once per section
2. **Secondary:** `bg-[var(--color-silver)] text-black` — non-pulsing, used for secondary actions
3. **Outline:** `border border-[var(--color-border-light)]` — tertiary actions
4. **Link:** `text-[var(--color-accent)] underline-offset-4` — inline links

---

## 2. Tech Stack & Environment

| Layer         | Technology               | Version            | Critical Note                                                                                   |
| ------------- | ------------------------ | ------------------ | ----------------------------------------------------------------------------------------------- |
| Framework     | Next.js (App Router)     | `16.2.10`          | Turbopack dev; `proxy.ts` replaces `middleware.ts`                                              |
| UI Runtime    | React                    | `19.2.7`           | `react-hooks/set-state-in-effect` rule is `error`                                               |
| Language      | TypeScript               | `5.9.3`            | `strict`, `noUncheckedIndexedAccess`, `verbatimModuleSyntax`                                    |
| Styling       | Tailwind CSS             | `4.3.2`            | CSS-first `@theme` — NO `tailwind.config.js`                                                    |
| UI Primitives | Radix UI + shadcn/ui     | —                  | Dialog, Accordion, Dropdown, Slot (custom-wrapped)                                              |
| Database      | PostgreSQL + Drizzle ORM | `0.45.2`           | 11 tables, 3 migrations, `ON CONFLICT DO NOTHING`, `.notNull()` on `published`/`order` (H4 fix) |
| Auth          | Auth.js v5 (next-auth)   | `5.0.0-beta.31`    | JWT strategy, no DrizzleAdapter, `trustHost: true`                                              |
| Job Queue     | Inngest                  | `4.11.0`           | v4 `createFunction` uses `triggers` in config object                                            |
| Payments      | Stripe                   | `22.3.0`           | Checkout redirect model, webhook signature verification                                         |
| AI            | Replicate                | `1.4.0`            | SDXL, env-configurable model ID (T4 lesson)                                                     |
| Storage       | Cloudflare R2 (S3)       | —                  | `MAX_PUT_OBJECT_BYTES = 500 MB` (T7 lesson)                                                     |
| Rate Limit    | Upstash Ratelimit        | `2.0.8`            | Sliding window, no-op fallback when not configured                                              |
| Validation    | Zod                      | `4.4.3`            | Enum `{ message }` not `{ errorMap }`; strict UUID v4                                           |
| Testing       | Vitest + Playwright      | `4.1.9` / `1.61.0` | 183 unit tests (16 files) + 9 E2E spec files                                                    |
| Pkg Manager   | pnpm                     | `≥10.26.0`         | `packageManager` field pinned in `package.json`                                                 |
| Node.js       | —                        | `≥20.0.0`          | `≥20.0.0` (engines); `20.18.0` pinned in `.nvmrc`                                               |
| Toasts        | sonner                   | `2.0.7`            | Server action success/error feedback                                                            |
| Icons         | lucide-react             | `0.460.0`          | Tree-shaken per-icon                                                                            |

**Environment variables:** 26 total (see `.env.example`). Build-context fallback returns placeholders when `NEXT_PHASE=phase-production-build` or `NODE_ENV=test`. **⚠️ Production-critical:** `NEXT_PUBLIC_APP_URL` MUST be set to the production domain — without it, `sitemap.xml`, `robots.txt`, `metadataBase`, and OG `url` publish `localhost` URLs (M1 fix).

---

## 3. Bootstrapping & Configuration

### Initial Setup

```bash
pnpm install
cp .env.example .env.local
# Fill in DATABASE_URL, DATABASE_URL_UNPOOLED, AUTH_SECRET at minimum
openssl rand -base64 32  # Generate AUTH_SECRET
pnpm db:reset            # Migrate + seed
pnpm dev                 # Start dev server on :3000
```

### Quality Gate (run before every commit)

```bash
pnpm typecheck && pnpm lint && pnpm test && pnpm build
```

### All Commands

| Command                      | Purpose                                              |
| ---------------------------- | ---------------------------------------------------- |
| `pnpm dev`                   | Dev server (Turbopack) on :3000                      |
| `pnpm build`                 | Production build                                     |
| `pnpm start`                 | Start production server                              |
| `pnpm typecheck`             | `tsc --noEmit`                                       |
| `pnpm lint`                  | ESLint flat config                                   |
| `pnpm test`                  | Vitest (183 unit tests, 16 files)                    |
| `pnpm test:e2e`              | Playwright (requires dev server)                     |
| `pnpm format`                | Prettier write                                       |
| `pnpm drizzle:generate`      | Generate migration from schema diff                  |
| `pnpm drizzle:migrate`       | Apply migrations                                     |
| `pnpm db:seed`               | Seed (8 coaches + 9 programs + 6 stories + 48 slots) |
| `pnpm db:reset`              | Migrate + seed in one command                        |
| `bash scripts/smoke-test.sh` | Post-deploy smoke test                               |

### Critical Configuration Files

| File                  | Purpose                                                                   | Key Setting                                                      |
| --------------------- | ------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| `next.config.ts`      | CSP, HSTS, security headers, image remotePatterns, serverExternalPackages | `serverExternalPackages` is top-level (NOT under `experimental`) |
| `tsconfig.json`       | TypeScript strict                                                         | `strict`, `noUncheckedIndexedAccess`, `verbatimModuleSyntax`     |
| `eslint.config.mjs`   | Flat config, 9.x                                                          | `no-restricted-imports` on `src/features/*/domain/**`            |
| `vitest.config.ts`    | Test runner                                                               | Includes `src/tests/unit/**` + `src/features/**/*.test.*`        |
| `postcss.config.mjs`  | Tailwind v4                                                               | `@tailwindcss/postcss` plugin only                               |
| `drizzle.config.ts`   | Drizzle Kit                                                               | `dialect: 'postgresql'`, uses `DATABASE_URL_UNPOOLED`            |
| `src/app/globals.css` | Design tokens                                                             | `@theme` block — all colors, fonts, motion, z-index              |
| `src/proxy.ts`        | Edge middleware                                                           | Next.js 16 — export `proxy` not `middleware`                     |
| `src/lib/env.ts`      | Zod env validation                                                        | Build-context fallback for `next build`                          |

### pnpm-workspace.yaml (T0 lesson)

```yaml
packages:
  - '.'
allowBuilds:
  esbuild: true
  sharp: true
  unrs-resolver: true
onlyBuiltDependencies:
  - sharp
  - unrs-resolver
  - esbuild
```

Required by pnpm 9+ even for single-package repos. Without it, `pnpm install` fails with `ERR_PNPM_INVALID_WORKSPACE_CONFIGURATION`.

---

## 4. The Design System (Code-First)

### `@theme` Block (in `src/app/globals.css`)

```css
@theme {
  /* Surface (60%) */
  --color-bg: #0a0a0a;
  --color-bg-darker: #050505;
  --color-bg-card: #141414;
  --color-bg-card-hover: #1a1a1a;

  /* Foreground (30%) */
  --color-fg: #f5f5f5; /* 18.16:1 on bg — AAA */
  --color-fg-dim: #c0c0c0; /* 10.88:1 — AAA */
  --color-muted: #8a8a8a; /* 5.5:1 — AA (v2: raised from #6a6a6a) */

  /* Accent (10%) */
  --color-accent: #ff5400;
  --color-accent-bright: #ff7a33;
  --color-accent-dim: #b33a00;
  --color-accent-glow: rgba(255, 84, 0, 0.45);

  /* Chrome */
  --color-silver: #c8c8c8;
  --color-silver-dim: #5a5a5a;

  /* Lines */
  --color-border: #1f1f1f;
  --color-border-light: #2a2a2a;

  /* Typography */
  --font-display: var(--font-bebas-neue), 'Arial Narrow', sans-serif;
  --font-heading: var(--font-oswald), 'Inter Tight', sans-serif;
  --font-body: var(--font-archivo), 'Inter', system-ui, sans-serif;
  --font-mono: var(--font-jetbrains-mono), 'Geist Mono', monospace;

  /* Motion */
  --ease-premium: cubic-bezier(0.22, 1, 0.36, 1);
  --ease-snap: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-flip: cubic-bezier(0.4, 0.2, 0.2, 1);
  --dur-reveal: 900ms;
  --dur-flip: 900ms;
  --dur-sticky: 600ms;
  --dur-carousel-snap: 700ms;
  --dur-micro: 150ms;
  --dur-standard: 300ms;
  --dur-dramatic: 500ms;

  /* Layout */
  --container-max: 1600px;
  --gutter: 1.5rem;
  --gutter-lg: 2.5rem;

  /* Z-Index */
  --z-behind: -1;
  --z-base: 0;
  --z-raised: 10;
  --z-dropdown: 200;
  --z-sticky: 300;
  --z-overlay: 400;
  --z-modal: 500;
  --z-popover: 600;
  --z-tooltip: 700;
  --z-toast: 800;
  --z-max: 999;

  /* Animations (backed by @keyframes in the same @theme block) */
  --animate-pulse-cta: pulse-cta 2.4s ease-out infinite;
  --animate-marquee: marquee 38s linear infinite;
  --animate-ken-burns: ken-burns 9s ease-out forwards;
  --animate-wave: wave 0.7s ease-in-out infinite;
  --animate-rec-blink: rec-blink 1.5s ease-in-out infinite;
}
```

### Typography Hierarchy

| Role      | Font           | Weight | Size              | Tracking    | Line-height |
| --------- | -------------- | ------ | ----------------- | ----------- | ----------- |
| Display   | Bebas Neue     | 400    | 8.5vw / 14vw      | 0.005em     | 0.85        |
| Heading 1 | Oswald         | 600    | 4rem / 2.5rem     | 0.01em      | 1.1         |
| Heading 2 | Oswald         | 500    | 2.25rem / 1.75rem | 0.02em      | 1.1         |
| Body      | Archivo        | 400    | 1.0625rem         | 0           | 1.5         |
| Telemetry | JetBrains Mono | 400    | 0.6875rem         | 0.2em upper | 1.5         |
| CTA       | Oswald         | 600    | 0.85rem           | 0.2em upper | 1.1         |

### Keyframes (6 total)

| Name            | Duration                          | Use                                                                                                |
| --------------- | --------------------------------- | -------------------------------------------------------------------------------------------------- |
| `pulse-cta`     | 2.4s infinite                     | Primary CTA radial glow                                                                            |
| `marquee`       | 38s linear infinite               | Hero bottom ticker                                                                                 |
| `ken-burns`     | 9s forwards                       | Active hero reel frame                                                                             |
| `wave`          | 0.7s infinite                     | Mute toggle equalizer bars                                                                         |
| `rec-blink`     | 1.5s infinite                     | "REEL · LIVE" indicator                                                                            |
| `progress-fill` | `frameDurationMs` linear forwards | Hero reel progress bar (M8 fix — CSS-driven, zero React re-renders; restarted via `key={current}`) |

### Custom Utilities (`@utility`)

`text-stroke`, `text-stroke-accent`, `vertical-text`, `bg-textured`, `scan-line`, `notch-corner`, `img-noir`

### Forbidden Colors (enforced by `src/tests/unit/brand-tokens.test.ts`)

`#7c3aed`, `#a855f7`, `#8b5cf6`, `#3b82f6`, `#6366f1`, `#fde68a`, `#fcd34d`

---

## 5. Component Architecture & Patterns

### 5-Layer Golden Rule

```
Layer 0  src/proxy.ts            → Edge cookie check. NO DB.
Layer 1  src/app/                → Routes, metadata, Suspense. Layouts must NOT fetch data.
Layer 2  src/features/           → UI composition, data binding, mutations
Layer 3  src/features/*/domain/  → Pure Zod schemas. NO runtime imports (import type only)
Layer 4  src/lib/                → Infrastructure: Drizzle, Auth, Inngest, R2, Stripe, AI
```

**Enforcement:** ESLint `no-restricted-imports` on `src/features/*/domain/**/*.ts` blocks React, Next.js, Drizzle, and all infrastructure. `allowTypeImports: true`.

### Component Inventory

| Category      | Count  | Key Files                                                                                             |
| ------------- | ------ | ----------------------------------------------------------------------------------------------------- |
| Layout        | 8      | Container, Section, SectionMarker, SiteHeader, MobileNavSheet, SiteFooter, GrainOverlay, StickyCTABar |
| Hero          | 7      | HeroReel, ReelFrame, ReelControl, ReelProgress, HeroHeadline, CoachStrip, Marquee                     |
| Programs      | 4      | ProgramsSection, ProgramGrid, ProgramCard, GoalSelector                                               |
| Coaches       | 3      | CoachesSection, CoachFlipGrid, CoachFlipCard                                                          |
| Stories       | 3      | StoriesSection, StoriesCarousel, StoryCard                                                            |
| Booking       | 3      | BookingSection, BookingCTA, StatBlock                                                                 |
| Memberships   | 2      | MembershipsSection, MembershipTierComparison                                                          |
| UI Primitives | 4      | button, input, textarea, label (shadcn-wrapped)                                                       |
| Other         | 3      | ScrollReveal, AdminSessionProvider, JsonLd                                                            |
| **Total**     | **37** |                                                                                                       |

_Note: This count covers `src/components/` only. Additional components exist in feature modules (e.g., `BookingForm` in `src/features/booking/BookingForm.tsx`) per the 5-layer architecture._

### Client vs Server Component Decision Tree

```
Does the component need:
  - useState/useEffect/useRef?     → Client ('use client')
  - Event handlers (onClick)?      → Client
  - Browser APIs (window, matchMedia)? → Client
  - next-auth signIn/signOut?      → Client
  - next/navigation useSearchParams? → Client (+ Suspense wrapper)

Otherwise: Server Component (default — no directive needed)
```

### Queries Pattern (DB-first with static fallback + published filter)

```typescript
// src/features/programs/queries.ts — H2 + H4 fix: published filter, no casts, Zod validation
export async function getPrograms(goal?: string): Promise<Program[]> {
  try {
    const { db } = await import('@/lib/db/client'); // dynamic import
    const { programs } = await import('@/lib/db/schema');
    const result = await db
      .select()
      .from(programs)
      .where(and(eq(programs.published, true), goal ? eq(programs.goal, goal) : undefined))
      .orderBy(programs.order);
    if (result.length > 0) {
      const validated = ProgramArraySchema.safeParse(result); // Zod validation (defense-in-depth)
      if (validated.success) return validated.data;
    }
    return goal
      ? STATIC_PROGRAMS.filter((p) => p.published && p.goal === goal)
      : STATIC_PROGRAMS.filter((p) => p.published);
  } catch {
    return goal
      ? STATIC_PROGRAMS.filter((p) => p.published && p.goal === goal)
      : STATIC_PROGRAMS.filter((p) => p.published);
  }
}
```

**Key changes (audit remediation):**

- `.where(eq(programs.published, true))` — unpublished records never reach the API (H2 fix)
- `ProgramArraySchema.safeParse(result)` — Zod validates DB results before returning (defense-in-depth for varchar→enum narrowing)
- No `as unknown as Program[]` casts — Drizzle `.notNull()` on `published`/`order` columns makes inferred types match Zod schemas (H4 fix)
- Static fallback also filters by `published: true`

**Zod validation scope:** Programs module validates DB results via `ProgramArraySchema.safeParse()` (defense-in-depth for `varchar→enum` narrowing on `goal`). Coaches and stories modules validate at the API route layer (`CoachArraySchema.safeParse()` in `/api/coaches/route.ts`, `StoryArraySchema.safeParse()` in `/api/stories/route.ts`) — not in the query files themselves.

### Server Action Pattern (Auth-First + UUID validation)

```typescript
// src/features/coaches/actions.ts — M5 fix: UUID validation on id params
'use server';
import { z } from 'zod';

const IdSchema = z.string().uuid('Invalid ID format');

async function requireAdmin() {
  const session = await auth();
  if (!session?.user || (session.user as { role?: string }).role !== 'admin') {
    return {
      success: false as const,
      code: 'UNAUTHORIZED' as const,
      message: 'Admin access required',
    };
  }
  return { success: true as const };
}

export async function updateCoach(id: string, input: unknown) {
  const authCheck = await requireAdmin();
  if (!authCheck.success) return authCheck;

  // M5 fix: validate id as UUID BEFORE any DB call
  const idResult = IdSchema.safeParse(id);
  if (!idResult.success) {
    return {
      success: false as const,
      code: 'VALIDATION' as const,
      message: idResult.error.issues[0]?.message ?? 'Invalid ID',
    };
  }

  const parsed = CoachFormSchema.safeParse(input);
  if (!parsed.success)
    return { success: false, code: 'VALIDATION', message: parsed.error.issues[0]?.message };
  // ... DB update + revalidatePath
}
```

---

## 6. Custom Hooks Deep Dive

### `useHeroReel` (`src/hooks/useHeroReel.ts`)

**Purpose:** Cinematic hero reel state machine — frame cycling, mute toggle.

**Signature:** `useHeroReel({ frameCount, frameDurationMs?, autoAdvance? }): { currentFrame, muted, isPlaying, goTo, next, toggleMute, containerRef, frameDurationMs }`

**Key details:**

- `isPlaying` is DERIVED from `shouldPlay` (not `setState` in effect — React 19 compliant)
- Pauses when: `prefers-reduced-motion`, off-screen (IntersectionObserver threshold 0.25), `autoAdvance=false`, `frameCount<=1`
- **M8 fix:** Progress bar is now CSS-driven (`@keyframes progress-fill` in `globals.css` + `key={current}` on the fill div in `ReelProgress.tsx`). The hook NO LONGER calls `setProgress` every 100ms — only `setCurrentFrame` on frame advance. This eliminates 10 re-renders per second.
- `frameDurationMs` is returned so `ReelProgress` can set the CSS animation duration
- `containerRef` for IntersectionObserver attachment

### `useStoriesCarousel` (`src/hooks/useStoriesCarousel.ts`)

**Purpose:** Drag-to-swipe carousel with rubber-band physics.

**Signature:** `useStoriesCarousel({ cardCount, autoAdvanceMs?, pauseOnHover? }): { currentIndex, trackX, isDragging, trackRef, viewportRef, goTo, next, prev, isPaused }`

**Key details:**

- Pointer Events unified API (mouse + touch)
- Rubber-band at edges: 0.35× resistance past bounds
- Momentum on release: velocity × 300ms, then snap to nearest card (700ms ease-snap)
- Auto-advance every 4.5s (pauses on hover, drag, reduced-motion, cardCount<=1)
- `touch-action: pan-y` on track (vertical scroll passes through)
- Keyboard: ArrowLeft/Right when viewport is focused
- All `setState` calls happen inside event callbacks (not effect body — React 19 compliant)

### `useReveal` (`src/hooks/useReveal.ts`)

**Purpose:** IntersectionObserver-based scroll reveal.

**Signature:** `useReveal<T>({ threshold?, rootMargin?, once? }): { ref, revealed }`

**Defaults:** `threshold: 0.15`, `rootMargin: '0px 0px -50px 0px'`, `once: true`

### `useReducedMotion` (`src/hooks/useReducedMotion.ts`)

**Purpose:** Mirrors `prefers-reduced-motion` media query. Returns `boolean`.

**Used by:** HeroReel, StoriesCarousel, GrainOverlay, StickyCTABar, StatBlock.

### `useScrolled` (`src/hooks/useScrolled.ts`)

**Purpose:** Boolean state for "user has scrolled past threshold". Used by SiteHeader.

**Signature:** `useScrolled(threshold?: number): boolean` (default threshold: 10px)

---

## 7. Content Management & Data Ingestion

### Static Data Files

| File                               | Count            | Content                                                                                            |
| ---------------------------------- | ---------------- | -------------------------------------------------------------------------------------------------- |
| `src/features/coaches/data.ts`     | 8 coaches        | slug, name, title, bio, certifications[], specialties[], signatureWorkout, portraitKey, yearsExp   |
| `src/features/programs/data.ts`    | 9 programs       | slug, goal, title, description, duration, sessionsPerWeek, intensity, heroKey, priceCents, coachId |
| `src/features/stories/data.ts`     | 6 stories        | slug, memberName, memberAge, programSlug, weeks, beforeKey, afterKey, quote                        |
| `src/features/memberships/data.ts` | 3 tiers + 1 pack | id, name, priceMonthly, priceCents, stripePriceId, features[], limitations[], cta                  |

### How to Add a New Coach

1. Add entry to `src/features/coaches/data.ts` (STATIC_COACHES array)
2. Add entry to `src/lib/db/seed.ts` (mirror the data for DB seeding)
3. The coach automatically appears on the home page + `/api/coaches` + admin list
4. No other files need to be touched — the queries module falls back to static data

### How to Add a New Program

1. Add entry to `src/features/programs/data.ts` (STATIC_PROGRAMS array)
2. Add entry to `src/lib/db/seed.ts`
3. The program appears in the goal-filtered grid automatically

### How to Add a New Membership Tier

1. Add entry to `src/features/memberships/data.ts` (MEMBERSHIP_TIERS array)
2. Update `src/features/memberships/data.test.ts` if changing the count
3. Create the Stripe product and set `stripePriceId`

---

## 8. Accessibility (WCAG AAA) Implementation

### Color Contrast Table

| Foreground                | Background         | Ratio   | WCAG Level                      |
| ------------------------- | ------------------ | ------- | ------------------------------- |
| `#f5f5f5` (fg)            | `#0a0a0a` (bg)     | 18.16:1 | AAA normal                      |
| `#c0c0c0` (fg-dim)        | `#0a0a0a` (bg)     | 10.88:1 | AAA normal                      |
| `#8a8a8a` (muted)         | `#0a0a0a` (bg)     | 5.5:1   | AA normal (v2 fix)              |
| `#ff5400` (accent)        | `#0a0a0a` (bg)     | 6.15:1  | AAA large (≥18px only)          |
| `#ff7a33` (accent-bright) | `#0a0a0a` (bg)     | 7.62:1  | AAA normal                      |
| black                     | `#ff5400` (accent) | 6.52:1  | AAA large (button text — small) |

### Focus Ring Specification

Global CSS rule in `globals.css`:

```css
a[href]:focus-visible,
button:focus-visible,
input:focus-visible,
select:focus-visible,
textarea:focus-visible,
[tabindex]:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}
```

### `prefers-reduced-motion` Implementation

Global CSS in `globals.css`:

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
  [data-reveal] {
    opacity: 1 !important;
    transform: none !important;
  }
}
```

JS-side: `useReducedMotion()` hook disables parallax, auto-advance, grain overlay.

### Touch Target Sizes

All icon buttons: `h-11 w-11` (44×44). Carousel dots: wrapped in `min-h-11 min-w-11` tap target containers.

### ARIA Patterns

| Component          | ARIA                                                                                |
| ------------------ | ----------------------------------------------------------------------------------- |
| GoalSelector       | `role="radiogroup"` + `role="radio"` + `aria-checked`                               |
| StoriesCarousel    | `aria-roledescription="carousel"` + `role="group"` per slide + `role="tab"` per dot |
| CoachFlipCard      | `role="button"` + `tabIndex={0}` + `aria-expanded` + descriptive `aria-label`       |
| ReelControl        | `aria-pressed` + `aria-label`                                                       |
| MobileNavSheet     | Radix Dialog (auto focus trap, Esc, focus restore)                                  |
| BookingForm errors | `role="alert"` + `aria-invalid` + `aria-describedby`                                |

---

## 9. Anti-Patterns & Common Bugs

### Bug: Zod 4 UUID Validation Rejects Placeholder IDs (Critical)

**Symptom:** API routes return 500 with "Internal data shape mismatch"
**Root cause:** Zod 4's `z.string().uuid()` requires proper v4 format (version digit `4`, variant `8/9/a/b`). IDs like `00000000-0000-0000-0000-000000000001` fail.
**Fix:** Use valid v4 format: `a1000000-0000-4000-8000-000000000001` (coaches), `b1...` (programs), `c1...` (stories).

### Bug: Next.js 16 `middleware.ts` → `proxy.ts` (Critical)

**Symptom:** Build fails with "Proxy is missing expected function export name"
**Root cause:** Next.js 16 renamed the middleware file convention.
**Fix:** Rename `src/middleware.ts` → `src/proxy.ts`. Export `function proxy()` not `function middleware()`.

### Bug: `useSearchParams()` Requires Suspense (High)

**Symptom:** Build fails with "useSearchParams() should be wrapped in a suspense boundary"
**Root cause:** Next.js 16 requires Suspense for static prerendering when using `useSearchParams()`.
**Fix:** Wrap the component in `<Suspense fallback={<Loading />}>`.

### Bug: React 19 `set-state-in-effect` Rule (High)

**Symptom:** ESLint error: "Avoid calling setState() directly within an effect"
**Root cause:** React 19's stricter hooks rules prevent cascading renders.
**Fix:** Derive state from computed values, or only call `setState` inside event callbacks (setInterval, pointer events, IntersectionObserver).

### Bug: Inngest v4 `createFunction` Signature (High)

**Symptom:** TypeScript error: "Expected 2 arguments, but got 3"
**Root cause:** Inngest v4 moved the trigger into the config object.
**Fix:** `inngest.createFunction({ id, name, triggers: [{ event: '...' }] }, handler)` — NOT 3 separate args.

### Bug: Zod 4 Enum Syntax (Medium)

**Symptom:** TypeScript error on `z.enum([...], { errorMap: ... })`
**Root cause:** Zod 4 changed enum error configuration.
**Fix:** Use `{ message: '...' }` instead of `{ errorMap: () => ({ message }) }`.

### Bug: Infrastructure Client Crashes in Dev Without `.env.local` (Medium)

**Symptom:** API routes return 500; server console shows "Invalid environment variables"
**Root cause:** Infrastructure clients (`lib/stripe.ts`, `lib/r2.ts`, `lib/ai/replicate.ts`, `lib/inngest/client.ts`) originally imported `env` from `@/lib/env`, which throws in dev without `.env.local`.
**Fix:** Use `process.env` directly in infrastructure clients (not the Zod `env` module). The `env` module is for app-level code only.

### Bug: DrizzleAdapter Type Mismatch (Medium)

**Symptom:** TypeScript error: sessions table type not assignable to DefaultPostgresSessionsTable
**Root cause:** DrizzleAdapter expects `sessionToken` as PK; our schema uses `id` as PK + `sessionToken` unique.
**Fix:** Don't use DrizzleAdapter. JWT strategy doesn't need it.

### Audit Remediation Bugs (2026-07-03)

The following bugs were found in the post-audit code review and fixed via TDD. Each has a regression test preventing recurrence.

### Bug: CSP Included `'unsafe-eval'` Despite Comment Claiming Absence (Critical — H1)

**Symptom:** Live CSP header showed `script-src 'self' 'unsafe-inline' 'unsafe-eval'` but the inline comment in `next.config.ts` said "'unsafe-eval' is intentionally absent."
**Root cause:** Documentation/implementation contradiction. The CSP string included `'unsafe-eval'` but the comment claimed it didn't.
**Fix:** Removed `'unsafe-eval'` from `CSP_POLICY` in `next.config.ts`. Updated the comment. Next.js 16 production builds do NOT require `'unsafe-eval'`.
**Lesson:** Grep the actual config string, don't trust the comment.

### Bug: Public Queries Did Not Filter by `published: true` (Critical — H2)

**Symptom:** `/api/coaches`, `/api/programs`, `/api/stories` would return unpublished records once the admin CRUD UI was used.
**Root cause:** All 3 query modules called `.select().from().orderBy()` without `.where(eq(*.published, true))`. The API doc comment claimed "Returns all published coaches" but the query didn't enforce it.
**Fix:** Added `.where(eq(*.published, true))` (and `and(eq(slug, ...), eq(published, true))` for detail-by-slug) to all public queries. Static fallback also filters by `published: true`.
**Regression test:** `src/tests/unit/queries-published-filter.test.ts` (11 tests — mocks DB to return mixed published/unpublished rows, asserts only published rows are returned).

### Bug: 23 Sitemap URLs Returned 404 (Critical — C3)

**Symptom:** `/coaches/marcus-steel`, `/programs/muscle-gain`, `/stories/james-r` all returned 404 on the live site. The sitemap promised 30 URLs but 23 had no corresponding page route.
**Root cause:** `sitemap.ts` generated URLs for `/programs/[slug]`, `/coaches/[slug]`, `/stories/[slug]` detail pages, but no `page.tsx` files existed (only API routes at `/api/{programs,coaches,stories}/[slug]`).
**Fix:** Created 3 new detail page routes: `src/app/coaches/[slug]/page.tsx`, `src/app/programs/[slug]/page.tsx`, `src/app/stories/[slug]/page.tsx`. Each uses `generateStaticParams` + `generateMetadata` + `notFound()` and follows the IRONFORGE design system.

### Bug: Dev Mode Healthcheck Referenced Nonexistent `/api/health` (Critical — C1 partial)

**Symptom:** Dockerfile `HEALTHCHECK` referenced `/api/health` which returned 404. Container marked unhealthy.
**Root cause:** The Dockerfile (copied from another project) assumed a health endpoint existed, but it was never created.
**Fix:** Created `src/app/api/health/route.ts` — lightweight 200 OK endpoint returning `{ status: 'ok', timestamp, uptime }`. No DB call (the healthcheck just needs a 200).

### Bug: `as unknown as` Casts Defeated TypeScript Safety (High — H4)

**Symptom:** 20 `as unknown as Coach[]` / `Program[]` / `Story[]` casts in query modules. ESLint `no-explicit-any` passed but runtime safety was gone.
**Root cause:** Drizzle schema declared `published: boolean('published').default(false)` without `.notNull()`, so Drizzle inferred `boolean | null`. Zod schema declared `z.boolean()` (inferred `boolean`). The structural mismatch forced casts. Additionally, `StaticProgram.goal` was typed as `string` while Zod expected an enum union.
**Fix:** Added `.notNull()` to 5 Drizzle columns (`coaches.published`, `coaches.order`, `programs.published`, `programs.order`, `stories.published`). Created migration `0002_enforce_published_notnull.sql`. Removed all 20 casts. Changed `StaticProgram.goal` to the enum union. Added Zod runtime validation in `programs/queries.ts` (defense-in-depth for varchar→enum narrowing).
**Lesson:** If you need a cast, the schema is wrong. Fix the schema.

### Bug: Hardcoded `localhost` in Metadata (Medium — M1)

**Symptom:** Production OG/canonical URLs pointed to `http://localhost:3000` instead of the real domain.
**Root cause:** `metadataBase` and OG `url` in `src/app/layout.tsx` were hardcoded to `http://localhost:3000`.
**Fix:** Changed to `process.env.NEXT_PUBLIC_APP_URL ?? 'http://localhost:3000'`.

### Bug: Brittle Substring Matching for Form Error Routing (Medium — M4)

**Symptom:** BookingForm routed errors to fields via `message.includes('email')` — broke if Zod message text changed.
**Root cause:** `TrialRequestResponse` type had no `field` property; the client reverse-engineered intent from natural language.
**Fix:** Added `field: z.string().nullable().optional()` to `TrialRequestResponseSchema`. Server action populates `field` from `parsed.error.issues[0]?.path[0]`. `BookingForm.tsx` now routes via `result.field`.

### Bug: Server Action `id` Params Not UUID-Validated (Medium — M5)

**Symptom:** `updateCoach('not-a-uuid', ...)` accepted any string, hitting the DB before rejection.
**Root cause:** `updateCoach(id: string, ...)`, `deleteCoach(id: string)`, `toggleCoachPublished(id: string, ...)` accepted `id` as raw `string` without Zod validation — inconsistent with the "Zod on every public input" pattern.
**Fix:** Added `const IdSchema = z.string().uuid()` and `IdSchema.safeParse(id)` validation to all 3 coach actions. Invalid UUIDs return `VALIDATION` error before any DB call.
**Regression test:** `src/features/coaches/actions.test.ts` (18 tests — 5 invalid IDs × 3 actions + 3 valid UUID tests).

### Bug: `@ts-expect-error` in R2 Stream Handling (Medium — M7)

**Symptom:** `@ts-expect-error` suppressed a type error in `lib/storage/r2.ts` stream handling — silent type-safety escape.
**Root cause:** AWS SDK types `response.Body` as `StreamingBlobPayload` which is not directly iterable. The code used `@ts-expect-error` to suppress the mismatch.
**Fix:** Replaced with `import { Readable } from 'stream'` + `if (!(response.Body instanceof Readable)) { return null; }` — proper type narrowing with a fail-loud fallback.

### Bug: Hero Reel Progress Bar Caused 10 Re-renders/Second (Medium — M8)

**Symptom:** `agent-browser vitals` showed continuous Render+Commit cycles every 100ms for 3+ seconds. Hero subtree re-rendered 10 times per second.
**Root cause:** `useHeroReel.ts` called `setProgress` every 100ms via `setInterval` to update the progress bar.
**Fix:** Added `@keyframes progress-fill` to `globals.css`. Updated `ReelProgress.tsx` to use CSS animation with `key={current}` (restarts on frame change). Removed `setProgress` from `useHeroReel.ts` — only `setCurrentFrame` on frame advance. Zero React re-renders for the progress bar.

### Bug: `toLocaleString()` Without Explicit Locale Caused SSR Hydration Mismatch (Medium — H5)

**Symptom:** Hydration error: `Hydration failed because the server rendered text didn't match the client. -2,400 +2.400`
**Root cause:** `StatBlock.tsx` called `displayValue.toLocaleString()` without an explicit locale. Server used Node's default (en-US → `2,400`), client used browser locale (e.g., de-DE → `2.400`). The component is a Client Component (`'use client'`), so it renders on both server (SSR) and client (hydration).
**Why `suppressHydrationWarning` is wrong here:** React docs explicitly state: "React will **not** attempt to patch mismatched text content" when `suppressHydrationWarning={true}`. This leaves the server-rendered text permanently in the DOM. Additionally, `animate={false}` during SSR (because `useReveal` initializes `revealed=false` on the server), so there is no animation to "mask" the visual difference.
**Fix:** Use `displayValue.toLocaleString('en-US')` — deterministic output eliminates the mismatch at the source. Server and client both produce `2,400`.
**Regression:** Hydration guard test (`src/tests/unit/hydration-guard.test.tsx`).

---

## 10. Debugging Guide

### Build Failures

| Error                                                        | Cause                                                | Fix                                                   |
| ------------------------------------------------------------ | ---------------------------------------------------- | ----------------------------------------------------- |
| `INNGEST_SIGNING_KEY is required in production`              | The production check fires during `next build`       | Gate behind `NEXT_PHASE !== 'phase-production-build'` |
| `Proxy is missing expected function export name`             | Using `middleware.ts` instead of `proxy.ts`          | Rename file + export `proxy`                          |
| `useSearchParams() should be wrapped in a suspense boundary` | Login page uses `useSearchParams()` without Suspense | Wrap in `<Suspense>`                                  |
| `Cannot find module '../../src/app/page.js'`                 | Stale `.next/types` cache after moving page          | `rm -rf .next`                                        |

### Runtime Errors

| Error                                                                   | Cause                                                                      | Fix                                                                                                                                             |
| ----------------------------------------------------------------------- | -------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| API returns `NOT_CONFIGURED`                                            | Infrastructure env vars are placeholders                                   | Set real values in `.env.local`                                                                                                                 |
| Admin redirects in a loop                                               | `AUTH_URL` doesn't match deployment URL                                    | Set `AUTH_URL` to match `NEXT_PUBLIC_APP_URL`                                                                                                   |
| `/api/auth/session` returns error                                       | `AUTH_SECRET` is placeholder                                               | Generate with `openssl rand -base64 32`                                                                                                         |
| Hydration: server rendered text didn't match (e.g., `2,400` vs `2.400`) | `toLocaleString()` uses server locale for SSR, client locale for hydration | Use `toLocaleString('en-US')` for deterministic output. Never use `suppressHydrationWarning` on text nodes — React will not patch the mismatch. |

### Test Failures

| Error                                          | Cause                                 | Fix                                            |
| ---------------------------------------------- | ------------------------------------- | ---------------------------------------------- |
| `Cannot access 'mockFn' before initialization` | Mock factory hoisting                 | Use `vi.hoisted()`                             |
| `X is not a constructor`                       | Arrow function mock can't be `new`-ed | Use `class` syntax                             |
| `[PARSE_ERROR] Expected '>'`                   | JSX in `.test.ts` file                | Rename to `.test.tsx`                          |
| `expected 18.73 to be close to 18.16`          | Incorrect contrast ratio assertion    | Update expected value to actual computed ratio |

### Audit Remediation Debugging Scenarios (2026-07-03)

| Symptom                                                    | Cause                                                                                                                        | Fix                                                                                                                                                                       |
| ---------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Site is slow / TTFB 350ms+                                 | Deployment running `pnpm dev` instead of `pnpm start` (browser console shows `[HMR] connected`, `[Fast Refresh] rebuilding`) | Deploy with `docker compose -f docker-compose.prod.yml up -d` (Dockerfile is correct — `pnpm build` → `pnpm start`)                                                       |
| Sitemap shows `localhost` URLs                             | `NEXT_PUBLIC_APP_URL` not set in deployment env                                                                              | Set `NEXT_PUBLIC_APP_URL=https://your-domain.com` and redeploy                                                                                                            |
| Checkout returns 503 NOT_CONFIGURED                        | Stripe env vars not set                                                                                                      | Set `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` + create 4 products/prices + update `MEMBERSHIP_TIERS`/`DROP_IN_PACK` in `data.ts` |
| TS error: `Type 'string' is not assignable to type 'enum'` | Drizzle `varchar` column vs Zod `z.enum()` mismatch                                                                          | Zod-validate DB results at runtime (see `programs/queries.ts`) OR change column to `pgEnum`                                                                               |
| TS error on `response.Body` in R2 getObject                | AWS SDK types `response.Body` as `StreamingBlobPayload` (not iterable)                                                       | Use `instanceof Readable` type narrowing (see `lib/storage/r2.ts`). Never `@ts-expect-error`.                                                                             |
| Hero reel progress bar stutters / causes re-renders        | `setProgress` called every 100ms via `setInterval`                                                                           | Use CSS `@keyframes progress-fill` + `key={current}` (see `ReelProgress.tsx` + `globals.css`)                                                                             |
| `/coaches/[slug]` returns 404                              | Detail page route missing (was only API route)                                                                               | Detail pages now exist at `src/app/{coaches,programs,stories}/[slug]/page.tsx` (added in audit remediation)                                                               |
| Dockerfile HEALTHCHECK fails                               | `/api/health` route was missing                                                                                              | Now exists at `src/app/api/health/route.ts` (returns 200 OK)                                                                                                              |

---

## 11. Pre-Ship Checklist

### Quality Gate Commands (must all pass)

```bash
pnpm typecheck    # tsc --noEmit — 0 errors
pnpm lint         # eslint . — 0 errors, 0 warnings
pnpm test         # vitest run — 183/183 pass (16 files)
pnpm build        # next build — 0 errors, 24+ routes
pnpm audit        # 0 vulnerabilities
```

### Pre-commit Hooks (automatic)

- **pre-commit:** `pnpm lint-staged` (ESLint + Prettier on staged files)
- **pre-push:** `pnpm typecheck && pnpm test`

### CI Pipeline (GitHub Actions)

```yaml
# .github/workflows/ci.yml
- pnpm install --frozen-lockfile
- pnpm lint
- pnpm typecheck
- pnpm test
- pnpm format:check
- pnpm build (NEXT_PHASE=phase-production-build)
```

### Post-Deploy Smoke Test

```bash
IRONFORGE_LIVE_URL=https://yourdomain.com bash scripts/smoke-test.sh
```

### Security Verification

- [ ] `pnpm audit` returns 0 vulnerabilities
- [ ] CSP header present in response
- [ ] HSTS header present (max-age=63072000)
- [ ] Admin routes redirect unauthenticated users
- [ ] API admin routes require admin role
- [ ] Rate limiting active (booking 5/min, checkout 10/min, auth 5/10min)
- [ ] Stripe webhook signature verification active
- [ ] No secrets in `.env.local` committed to git

---

## 12. Lessons Learnt & How to Avoid Them

### Architecture Lessons

1. **Graceful degradation is the cornerstone.** Every infrastructure client (DB, Stripe, R2, Replicate, Inngest) uses `process.env` directly with `null` fallback. The marketing site renders in dev, build, and CI without any external services.
2. **5-layer architecture needs ESLint enforcement.** Without `no-restricted-imports` on domain files, schemas accumulate runtime imports.
3. **Dynamic imports for DB in queries/actions.** `await import('@/lib/db/client')` inside try/catch defers connection until called.

### Framework Lessons

4. **Next.js 16 renamed `middleware.ts` → `proxy.ts`.** Export `proxy` not `middleware`.
5. **`useSearchParams()` requires `<Suspense>`** for static prerendering.
6. **`serverExternalPackages` is top-level** in `next.config.ts` (not under `experimental`).
7. **Tailwind v4 is CSS-first.** No `tailwind.config.js`. All tokens in `@theme` block.
8. **Zod 4 enum uses `{ message }`** not `{ errorMap }`.
9. **Zod 4 UUID validation is strict** — requires proper v4 format.
10. **Inngest v4 `createFunction` uses 2 args** (triggers in config object, not separate arg).

### React 19 Lessons

11. **`react-hooks/set-state-in-effect` is `error`.** Derive state instead, or call `setState` only in event callbacks.
12. **`react-hooks/exhaustive-deps` is `error`** (not `warn`).
13. **`toLocaleString()` without explicit locale causes SSR hydration mismatch.** Server uses Node's default locale (en-US), client uses browser locale. For Client Components that render formatted numbers, always use `toLocaleString('en-US')` for deterministic output. `suppressHydrationWarning` is an anti-pattern for text nodes — React docs state it will "not attempt to patch mismatched text content", leaving server-rendered text permanently in the DOM. (H5 fix)

### Security Lessons

13. **Inngest dev mode must be gated behind `NODE_ENV !== 'production'`.** Otherwise signature verification is silently disabled.
14. **Login rate limiting must be wired (not just defined).** `rateLimitAuth` was defined but unused until Phase 10.
15. **Stripe checkout needs `idempotencyKey`.** Prevents duplicate sessions on double-click.
16. **`downloadImage()` needs SSRF allowlist.** Validate hostname before fetching Replicate output URLs.
17. **Admin API routes need defense in depth.** Edge proxy → layout session check → action role check.

### Accessibility Lessons

18. **`--color-muted` must pass AA-normal.** Raised from `#6a6a6a` (3.66:1) to `#8a8a8a` (5.5:1).
19. **Global `focus-visible` CSS rule** catches all interactive elements site-wide.
20. **Touch targets must be ≥44×44px.** Bumped all icon buttons from 40px to 44px.

### Testing Lessons

21. **JSX tests must use `.test.tsx`** extension (oxc parser limitation).
22. **`vi.hoisted()`** for mock factories when a hoisted `vi.mock()` factory references variables declared above it. Current tests avoid this by using `await import()` after `vi.mock()` or inline values.
23. **Class syntax** for SDK constructor mocks when a test needs to instantiate a mock with `new` (arrow functions can't be `new`-ed). Currently no tests mock SDK constructors directly.
24. **DB mock pattern:** `vi.mock('@/lib/db/client', () => { throw new Error('DB unavailable'); })` tests the fallback path.

### Audit Remediation Lessons (2026-07-03)

25. **`.default()` without `.notNull()` creates `T | null` in Drizzle inference.** This forced 20 `as unknown as` casts in the queries modules. Fix: always pair `.default(X)` with `.notNull()` when the column is semantically non-nullable. Migration 0002 backfills this for `published` and `order` columns. (H4 fix)
26. **Casts hide bugs.** `as unknown as` satisfied ESLint's `no-explicit-any` but defeated TypeScript runtime safety — it hid BOTH the `published: boolean | null` mismatch AND the `goal: string vs enum` mismatch. Lesson: if you need a cast, the schema is wrong. Fix the schema. (H4 fix)
27. **CSP `'unsafe-eval'` is NOT required for Next.js 16 production.** The inline comment claimed it was "intentionally absent" but the actual CSP string included it. Lesson: grep the actual config string, don't trust the comment. (H1 fix)
28. **`NEXT_PUBLIC_APP_URL` must be set in production.** Without it, `sitemap.xml` and `robots.txt` publish `localhost` URLs (verified on the live site). The code now reads `process.env.NEXT_PUBLIC_APP_URL` for `metadataBase`, OG `url`, sitemap, and robots. (M1 fix)
29. **`setProgress` every 100ms = 10 re-renders/sec.** Drive progress bars with CSS `@keyframes` + `key={current}` to restart on frame change. Zero React re-renders. (M8 fix)
30. **TDD catches missing filters.** Existing query tests only tested the static-fallback path (DB throws). New `queries-published-filter.test.ts` mocks the DB to RETURN data — catches the missing `published: true` filter. (H2 fix)
31. **`@ts-expect-error` is a silent escape hatch.** Use `instanceof Readable` type narrowing instead. Never suppress type errors. (M7 fix)
32. **Substring matching for error routing is brittle.** Server actions return a `field` property (from Zod `issues[0].path[0]`); clients route via `result.field`. (M4 fix)
33. **Server action `id` params need UUID validation.** Always `z.string().uuid().safeParse(id)` before any DB call. (M5 fix)
34. **Sitemap URLs must have corresponding page routes.** The sitemap generated 23 detail-page URLs with no `page.tsx` files — all 404'd. Created 3 new detail page routes (`/coaches/[slug]`, `/programs/[slug]`, `/stories/[slug]`). (C3 fix)

---

## 13. Pitfalls to Avoid

| #   | Pitfall                                                                 | Correct Approach                                                                          |
| --- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| 1   | Using `tailwind.config.js`                                              | All tokens in `globals.css` `@theme` block                                                |
| 2   | Using `DrizzleAdapter` with JWT                                         | JWT doesn't need it; type mismatch with our schema                                        |
| 3   | Using `{ errorMap }` in Zod 4                                           | Use `{ message }`                                                                         |
| 4   | Importing `lib/storage/r2.ts` in client components                      | Server Component signs URL, passes as prop                                                |
| 5   | `setState` in `useEffect` body                                          | Derive state or use event callbacks                                                       |
| 6   | Using `middleware.ts`                                                   | Rename to `proxy.ts`, export `proxy`                                                      |
| 7   | Placeholder UUIDs                                                       | Use valid v4 format (`a1000000-0000-4000-8000-...`)                                       |
| 8   | Dynamic class interpolation in Tailwind                                 | Use mapping objects with full class strings                                               |
| 9   | Importing `env` module in infrastructure clients                        | Use `process.env` directly                                                                |
| 10  | Forgetting `INNGEST_DEV=1` gate behind `NODE_ENV`                       | Production throws if signing key missing                                                  |
| 11  | Using `as unknown as` casts in queries                                  | Fix the schema (add `.notNull()`) instead — casts hide type mismatches (H4 fix)           |
| 12  | Using `@ts-expect-error` / `@ts-ignore` / `@ts-nocheck`                 | Use proper type narrowing (`instanceof`, type guards) (M7 fix)                            |
| 13  | Substring matching (`message.includes('email')`) for form error routing | Use the `field` property from the server response (M4 fix)                                |
| 14  | Including `'unsafe-eval'` in the CSP                                    | Next.js 16 production builds don't need it (H1 fix)                                       |
| 15  | Hardcoding `localhost:3000` in metadata                                 | Use `process.env.NEXT_PUBLIC_APP_URL ?? 'http://localhost:3000'` (M1 fix)                 |
| 16  | Using `setProgress` in `setInterval` for progress bars                  | Use CSS `@keyframes` + `key={current}` (M8 fix)                                           |
| 17  | Writing public queries without `.where(eq(*.published, true))`          | Unpublished records would leak via the public API (H2 fix)                                |
| 18  | Accepting `id: string` in server actions without UUID validation        | Always `z.string().uuid().safeParse(id)` before any DB call (M5 fix)                      |
| 19  | `toLocaleString()` without explicit locale in Client Components         | Use `toLocaleString('en-US')` — SSR uses Node locale, client uses browser locale (H5 fix) |
| 20  | `suppressHydrationWarning` on text nodes as a hydration fix             | React will not patch the mismatch — fix the source instead (H5 fix)                       |

---

## 14. Best Practices

- **Server Components by default.** `"use client"` only at leaves.
- **Zod validation on every public input.** Booking, checkout, admin, API responses.
- **Rate limit every mutation endpoint.** Booking 5/min, checkout 10/min, auth 5/10min.
- **Honeypot + idempotency on forms.** `company_website` field + UUID idempotency key.
- **`ON CONFLICT DO NOTHING` for idempotent seeds.** Safe to re-run.
- **Dynamic imports for all infrastructure.** `await import('@/lib/db/client')` pattern.
- **CSS-only animations.** No Framer Motion/GSAP — 5 keyframes in `@theme`.
- **`prefers-reduced-motion` disables ALL motion.** Global CSS + JS hook.
- **`next/image` with `priority` on hero.** First frame is LCP candidate.
- **`next/font/google` with `variable` strategy.** Zero layout shift.
- **Brand-token test enforces forbidden colors.** 7 colors rejected by Vitest.
- **`pnpm-workspace.yaml` with `packages: ['.']`.** Required by pnpm 9+.

---

## 15. Coding Patterns

### Graceful Degradation Pattern

```typescript
// src/lib/stripe.ts (same pattern for r2.ts, replicate.ts, inngest/client.ts)
function getStripe(): Stripe | null {
  const key = process.env.STRIPE_SECRET_KEY;
  if (!key || key.includes('placeholder')) return null;
  if (!stripeClient) stripeClient = new Stripe(key, { typescript: true });
  return stripeClient;
}
// Caller: if (!stripe) return 503 NOT_CONFIGURED;
```

### Server Action Pattern (with UUID validation + field-aware errors)

```typescript
// src/features/coaches/actions.ts — M5 + M4 fix
'use server';
import { z } from 'zod';

const IdSchema = z.string().uuid('Invalid ID format');

async function requireAdmin() {
  const session = await auth();
  if (!session?.user || (session.user as { role?: string }).role !== 'admin')
    return {
      success: false as const,
      code: 'UNAUTHORIZED' as const,
      message: 'Admin access required',
    };
  return { success: true as const };
}

export async function updateCoach(id: string, input: unknown) {
  const authCheck = await requireAdmin();
  if (!authCheck.success) return authCheck;

  // M5 fix: validate id as UUID BEFORE any DB call
  const idResult = IdSchema.safeParse(id);
  if (!idResult.success)
    return {
      success: false as const,
      code: 'VALIDATION' as const,
      message: idResult.error.issues[0]?.message ?? 'Invalid ID',
    };

  const parsed = CoachFormSchema.safeParse(input);
  if (!parsed.success)
    return { success: false, code: 'VALIDATION', message: parsed.error.issues[0]?.message };
  // ... DB update + revalidatePath
}
```

### Field-Aware Error Response Pattern (M4 fix)

```typescript
// src/features/booking/actions.ts — populate `field` from Zod error path
const parsed = TrialRequestSchema.safeParse(input);
if (!parsed.success) {
  const firstError = parsed.error.issues[0];
  const fieldPath = firstError?.path[0];
  return {
    success: false,
    code: 'VALIDATION',
    message: firstError?.message ?? 'Invalid input',
    requestId: null,
    field: typeof fieldPath === 'string' ? fieldPath : null, // client routes via result.field
  };
}

// src/features/booking/BookingForm.tsx — client uses result.field (NOT substring matching)
if (result.code === 'VALIDATION' && result.field) {
  const fieldName = result.field as keyof FormState;
  if (fieldName in INITIAL_STATE) {
    setErrors({ [fieldName]: result.message });
  }
}
```

### CSS Progress Bar Pattern (M8 fix — zero React re-renders)

```css
/* src/app/globals.css — @theme block */
@keyframes progress-fill {
  from {
    width: 0%;
  }
  to {
    width: 100%;
  }
}
```

```tsx
// src/components/sections/hero/ReelProgress.tsx
// key={current} restarts the CSS animation on each frame change
<div
  key={current}
  className="h-full bg-[var(--color-accent)]"
  style={{ animation: `progress-fill ${frameDurationMs}ms linear forwards` }}
/>
```

### instanceof Readable Pattern (M7 fix — no @ts-expect-error)

```typescript
// src/lib/storage/r2.ts — proper type narrowing for AWS SDK stream
import { Readable } from 'stream';

if (!response.Body) return null;
if (!(response.Body instanceof Readable)) {
  console.error('[r2:getObject] Unexpected body type:', typeof response.Body);
  return null;
}
const chunks: Uint8Array[] = [];
for await (const chunk of response.Body) {
  chunks.push(typeof chunk === 'string' ? Buffer.from(chunk) : chunk);
}
```

### API Route Pattern (Next.js 16 async params)

```typescript
export async function GET(_request: Request, { params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params; // must await!
  // ...
}
```

### Env Module Pattern (build-context fallback)

```typescript
function isBuildContext(): boolean {
  return process.env.NEXT_PHASE === 'phase-production-build' || process.env.NODE_ENV === 'test';
}
function loadEnv(): Env {
  if (isBuildContext()) return { ...placeholders }; // don't throw
  const parsed = envSchema.safeParse(process.env);
  if (!parsed.success) throw new Error('Invalid environment variables');
  return parsed.data;
}
```

---

## 16. Coding Anti-Patterns

```typescript
// ❌ WRONG — env module crashes in dev without .env.local
import { env } from '@/lib/env';
const stripe = new Stripe(env.STRIPE_SECRET_KEY);

// ✅ CORRECT — process.env directly with null fallback
function getStripe(): Stripe | null {
  const key = process.env.STRIPE_SECRET_KEY;
  if (!key || key.includes('placeholder')) return null;
  return new Stripe(key);
}
```

```typescript
// ❌ WRONG — setState in effect body (React 19 rule)
useEffect(() => {
  setIsPlaying(shouldPlay);
}, [shouldPlay]);

// ✅ CORRECT — derive state
const isPlaying = shouldPlay; // computed, not state
```

```typescript
// ❌ WRONG — arrow function mock can't be new-ed
vi.mock('@aws-sdk/client-s3', () => ({ S3Client: vi.fn(() => ({ send: vi.fn() })) }));

// ✅ CORRECT — class syntax
vi.mock('@aws-sdk/client-s3', () => {
  class MockS3 {
    send = vi.fn();
  }
  return { S3Client: MockS3 };
});
```

```typescript
// ❌ WRONG — as unknown as casts hide type mismatches (H4 fix)
return result as unknown as Coach[];

// ✅ CORRECT — fix the schema (add .notNull()) so Drizzle inferred types match Zod
// schema: published: boolean('published').default(false).notNull()
return result; // no cast needed
```

```typescript
// ❌ WRONG — @ts-expect-error suppresses type errors silently (M7 fix)
// @ts-expect-error — response.Body is a Readable stream in Node
for await (const chunk of response.Body) { ... }

// ✅ CORRECT — instanceof type narrowing
import { Readable } from 'stream';
if (!(response.Body instanceof Readable)) return null;
for await (const chunk of response.Body) { ... }
```

```typescript
// ❌ WRONG — substring matching for form error routing (M4 fix)
const message = result.message.toLowerCase();
if (message.includes('email')) setErrors({ email: result.message });

// ✅ CORRECT — use the field property from the server response
if (result.code === 'VALIDATION' && result.field) {
  setErrors({ [result.field]: result.message });
}
```

```typescript
// ❌ WRONG — setProgress in setInterval causes 10 re-renders/sec (M8 fix)
const progressTimer = setInterval(() => {
  setProgress(progressAccumulator);  // re-renders entire subtree
}, 100);

// ✅ CORRECT — CSS @keyframes animation + key={current} to restart on frame change
<div key={current} style={{ animation: `progress-fill ${frameDurationMs}ms linear forwards` }} />
```

```typescript
// ❌ WRONG — public query without published filter (H2 fix)
const result = await db.select().from(coaches).orderBy(coaches.order);

// ✅ CORRECT — filter by published: true
const result = await db
  .select()
  .from(coaches)
  .where(eq(coaches.published, true))
  .orderBy(coaches.order);
```

```typescript
// ❌ WRONG — server action accepts id without validation (M5 fix)
export async function deleteCoach(id: string) {
  // id hits the DB without validation
  await db.delete(coaches).where(eq(coaches.id, id));
}

// ✅ CORRECT — validate id as UUID before any DB call
const IdSchema = z.string().uuid();
export async function deleteCoach(id: string) {
  const idResult = IdSchema.safeParse(id);
  if (!idResult.success) return { success: false, code: 'VALIDATION', message: 'Invalid ID' };
  await db.delete(coaches).where(eq(coaches.id, idResult.data));
}
```

```typescript
// ❌ WRONG — toLocaleString() without locale causes hydration mismatch (H5 fix)
// Server: 2,400 (en-US) vs Client: 2.400 (de-DE)
<div>{displayValue.toLocaleString()}</div>

// ❌ ALSO WRONG — suppressHydrationWarning on text nodes
// React will NOT patch the mismatch — server text stays permanently in DOM
<div suppressHydrationWarning>{displayValue.toLocaleString()}</div>

// ✅ CORRECT — explicit locale for deterministic output
<div>{displayValue.toLocaleString('en-US')}</div>
```

---

## 17. Responsive Breakpoint Reference

Tailwind v4 default breakpoints (no custom config):

| Prefix | Min-width | Usage                                 |
| ------ | --------- | ------------------------------------- |
| (none) | 0px       | Mobile base styles                    |
| `sm:`  | 640px     | Small tablets                         |
| `md:`  | 768px     | Tablets (nav switches desktop/mobile) |
| `lg:`  | 1024px    | Desktop                               |
| `xl:`  | 1280px    | Large desktop                         |
| `2xl:` | 1536px    | Extra large                           |

**Symmetrical breakpoints rule:** Desktop nav uses `hidden md:flex`, mobile trigger uses `md:hidden`. Never use different breakpoints — causes "ghost menu" bug.

---

## 18. Z-Index Layer Map

| Token          | Value | Element                              | Location       |
| -------------- | ----- | ------------------------------------ | -------------- |
| `--z-behind`   | -1    | Decorative elements                  | Hero overlay   |
| `--z-base`     | 0     | Default content                      | All sections   |
| `--z-raised`   | 10    | Sticky within section                | Reel controls  |
| `--z-dropdown` | 200   | Dropdown menus                       | (future)       |
| `--z-sticky`   | 300   | SiteHeader, StickyCTABar             | Fixed headers  |
| `--z-overlay`  | 400   | MobileNavSheet overlay, GrainOverlay | Modal backdrop |
| `--z-modal`    | 500   | MobileNavSheet content, Radix Dialog | Sheet panel    |
| `--z-popover`  | 600   | Popover content                      | (future)       |
| `--z-tooltip`  | 700   | Tooltips                             | (future)       |
| `--z-toast`    | 800   | Sonner Toaster                       | Top-right      |
| `--z-max`      | 999   | Escape hatches                       | (future)       |

**Rule:** Always use the `--z-*` tokens, never raw `z-[999]` values.

---

## 19. Color Reference (Complete)

| Token                   | Hex                   | RGB         | Tailwind Class                       | Usage                   |
| ----------------------- | --------------------- | ----------- | ------------------------------------ | ----------------------- |
| `--color-bg`            | `#0a0a0a`             | 10,10,10    | `bg-[var(--color-bg)]`               | Primary canvas          |
| `--color-bg-darker`     | `#050505`             | 5,5,5       | `bg-[var(--color-bg-darker)]`        | Sticky bar, nav         |
| `--color-bg-card`       | `#141414`             | 20,20,20    | `bg-[var(--color-bg-card)]`          | Cards                   |
| `--color-bg-card-hover` | `#1a1a1a`             | 26,26,26    | —                                    | Card hover              |
| `--color-fg`            | `#f5f5f5`             | 245,245,245 | `text-[var(--color-fg)]`             | Body text               |
| `--color-fg-dim`        | `#c0c0c0`             | 192,192,192 | `text-[var(--color-fg-dim)]`         | Secondary text          |
| `--color-muted`         | `#8a8a8a`             | 138,138,138 | `text-[var(--color-muted)]`          | Telemetry labels        |
| `--color-accent`        | `#ff5400`             | 255,84,0    | `bg-[var(--color-accent)]`           | Primary CTA, large text |
| `--color-accent-bright` | `#ff7a33`             | 255,122,51  | —                                    | Hover state             |
| `--color-accent-dim`    | `#b33a00`             | 179,58,0    | —                                    | Scrollbar               |
| `--color-accent-glow`   | `rgba(255,84,0,0.45)` | —           | —                                    | Pulse glow              |
| `--color-silver`        | `#c8c8c8`             | 200,200,200 | `bg-[var(--color-silver)]`           | Secondary CTA           |
| `--color-silver-dim`    | `#5a5a5a`             | 90,90,90    | —                                    | Text stroke             |
| `--color-border`        | `#1f1f1f`             | 31,31,31    | `border-[var(--color-border)]`       | Default borders         |
| `--color-border-light`  | `#2a2a2a`             | 42,42,42    | `border-[var(--color-border-light)]` | Input borders           |

**Forbidden (enforced by brand-token test):** `#7c3aed`, `#a855f7`, `#8b5cf6`, `#3b82f6`, `#6366f1`, `#fde68a`, `#fcd34d`

---

## 20. TypeScript Interface Reference

### Program

```typescript
interface Program {
  id: string; // UUID v4
  slug: string;
  goal: 'muscle' | 'fat' | 'fitness' | 'athletic' | 'rehab';
  title: string;
  subtitle: string | null;
  description: string;
  duration: string | null;
  sessionsPerWeek: number | null;
  intensity: string | null;
  heroKey: string | null;
  priceCents: number | null;
  stripePriceId: string | null;
  coachId: string | null; // UUID v4
  order: number;
  published: boolean;
  createdAt: Date;
  updatedAt: Date;
}
```

### Coach

```typescript
interface Coach {
  id: string;
  slug: string;
  name: string;
  title: string;
  bio: string;
  certifications: string[] | null;
  specialties: string[] | null;
  signatureWorkout: string | null;
  portraitKey: string | null;
  yearsExp: number | null;
  order: number;
  published: boolean;
  createdAt: Date;
  updatedAt: Date;
}
```

### TrialRequestInput

```typescript
interface TrialRequestInput {
  name: string; // 2-80 chars
  email: string; // valid email, max 160
  phone: string; // optional, max 40
  goal: 'muscle' | 'fat' | 'fitness' | 'athletic' | 'rehab';
  preferredTime: 'early' | 'mid' | 'evening' | 'weekend';
  preferredCoachId: string | null; // UUID v4
  notes: string; // optional, max 500
  consent: boolean; // must be true
  company_website: string; // honeypot — must be empty
}
```

### TrialRequestResponse

```typescript
interface TrialRequestResponse {
  success: boolean;
  code: 'SUCCESS' | 'VALIDATION' | 'RATE_LIMITED' | 'SPAM_DETECTED' | 'DUPLICATE' | 'INTERNAL';
  message: string;
  requestId: string | null;
  field?: string | null; // M4 fix: field name for validation errors (from Zod issues[0].path[0])
}
```

### CheckoutRequest

```typescript
interface CheckoutRequest {
  priceId: string;
  tier: 'forge' | 'forge_plus' | 'forge_private' | 'drop_in';
}
```

### AssetGenerationRequest

```typescript
interface AssetGenerationRequest {
  type: 'coach_portrait' | 'program_hero' | 'story_before' | 'story_after';
  entitySlug: string; // 1-80 chars
  promptOverride?: string; // max 500
}
```

---

## 21. Appendices

### Appendix A: ADRs

| ADR | Decision                                                       | File                                            |
| --- | -------------------------------------------------------------- | ----------------------------------------------- |
| 001 | 5-Layer Golden Rule Architecture                               | `docs/adr/001-5-layer-architecture.md`          |
| 002 | CSP `'unsafe-inline'` for Styles — NO `'unsafe-eval'` (H1 fix) | `docs/adr/002-csp-unsafe-inline.md`             |
| 003 | Auth.js v5 Beta Pin + JWT                                      | `docs/adr/003-authjs-v5-beta-pin.md`            |
| 004 | Drizzle ORM over Prisma                                        | `docs/adr/004-drizzle-over-prisma.md`           |
| 005 | Inngest over BullMQ                                            | `docs/adr/005-inngest-over-bullmq.md`           |
| 006 | Replicate for AI Assets                                        | `docs/adr/006-replicate-for-ai-assets.md`       |
| 007 | Stripe Checkout over Embedded                                  | `docs/adr/007-stripe-checkout-over-embedded.md` |
| 008 | Image Ken Burns over MP4                                       | `docs/adr/008-image-ken-burns-over-mp4.md`      |
| 009 | English-Only for v1                                            | `docs/adr/009-english-only-v1.md`               |
| 010 | Dark-Mode Only for v1                                          | `docs/adr/010-dark-mode-only-v1.md`             |

### Appendix B: API Costs

| Service       | Operation             | Cost                         |
| ------------- | --------------------- | ---------------------------- |
| Replicate     | SDXL image generation | ~$0.01 per image             |
| Stripe        | Checkout Session      | 2.9% + $0.30 per transaction |
| Inngest       | Function run          | Free tier: 10K/month         |
| Upstash       | Redis command         | Free tier: 10K/day           |
| Neon          | Database              | Free tier: 0.5 GB            |
| Cloudflare R2 | Storage               | Free tier: 10 GB             |
| Resend        | Email                 | Free tier: 100/day           |
| Vercel        | Hosting               | Free tier: 100GB bandwidth   |

### Appendix C: Audit History

| Audit                            | Date           | Findings                                   | Fixes                                                                     | Tests                              |
| -------------------------------- | -------------- | ------------------------------------------ | ------------------------------------------------------------------------- | ---------------------------------- |
| `pnpm audit`                     | Phase 10       | 2 moderate (esbuild, postcss)              | pnpm.overrides                                                            | 0 vulnerabilities                  |
| OWASP Top 10                     | Phase 10       | 4 P1 + 4 P2 + 5 P3                         | All P1+P2 fixed                                                           | —                                  |
| WCAG AAA                         | Phase 10       | 3 P1 + 2 P2 + 5 P3                         | All P1 fixed                                                              | 19 brand-token tests               |
| **Code Review & Security Audit** | **2026-07-03** | **3 Critical + 4 High + 8 Medium + 7 Low** | **11 code-fixable items applied via TDD; 5 operational items documented** | **154→183 tests (+29 regression)** |

**Post-remediation quality gate:** `pnpm typecheck` ✅ | `pnpm lint` ✅ (0 warnings) | `pnpm test` 183/183 ✅ | `pnpm audit` 0 vulns ✅

See `.audit-report.md` for the full audit report with per-finding details, root causes, and remediation status.

### Appendix D: Post-Deploy Live-Site Validation

**Smoke test script:** `scripts/smoke-test.sh`

```bash
IRONFORGE_LIVE_URL=https://yourdomain.com bash scripts/smoke-test.sh
```

**What it checks (35+ assertions):**

- Home page HTTP 200 + all 6 sections present + JSON-LD
- robots.txt + sitemap.xml + manifest.webmanifest + icon.svg
- API routes (programs, coaches, stories) return correct counts
- Program detail API (200 + 404 + 400)
- Admin redirect (307) + login form
- 404 page with brand styling
- Security headers (CSP, HSTS, X-Frame-Options, nosniff)

**What live-site testing catches that CI cannot:**

- Real CDN behavior (image optimization, edge caching)
- Real SSL/TLS configuration
- Real DNS resolution
- Real Stripe webhook delivery
- Real Inngest Cloud function execution
- Real Upstash Redis connectivity
- **Dev mode in production** (C1 — browser console shows `[HMR] connected`, `[Fast Refresh] rebuilding`)
- **`NEXT_PUBLIC_APP_URL` not set** (C2 — sitemap/robots publish `localhost` URLs)
- **23 sitemap URLs 404** (C3 — detail page routes missing; now fixed)
- **Stripe not configured** (H3 — checkout returns 503 NOT_CONFIGURED)

### Appendix E: Outstanding Operational Items (Post-Remediation)

These items were identified in the code audit but require deployment environment access — they cannot be fixed in code:

| #   | Item                                  | Action Required                                                                                                                                                                                                  | Impact if Unfixed                                                                                                      |
| --- | ------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| 1   | **Deploy with production build** (C1) | Use `docker compose -f docker-compose.prod.yml up -d` (NOT `pnpm dev`). The Dockerfile is correct; the deployment pipeline must use it. The new `/api/health` route makes the Dockerfile HEALTHCHECK functional. | Site runs in dev mode (5-10× slower, source maps exposed, TTFB 350ms vs <100ms)                                        |
| 2   | **Set `NEXT_PUBLIC_APP_URL`** (C2)    | Set to `https://your-domain.com` in the deployment environment.                                                                                                                                                  | Sitemap + robots publish `localhost` URLs; Google indexes wrong URLs                                                   |
| 3   | **Configure Stripe** (H3)             | Set `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` + create 4 products/prices + update `MEMBERSHIP_TIERS`/`DROP_IN_PACK` in `data.ts`.                                       | Checkout returns 503 NOT_CONFIGURED; memberships non-functional                                                        |
| 4   | **Apply migration 0002**              | Run `pnpm drizzle:migrate` in the deployment environment.                                                                                                                                                        | `published`/`order` columns remain nullable at DB level (queries still work, but type safety not enforced at DB level) |
| 5   | **Cloudflare robots.txt** (M6)        | Move `Disallow: /admin/` into the Cloudflare-managed block, or disable CF managed robots.                                                                                                                        | Some crawlers may ignore the app's `Disallow: /admin/` directive                                                       |

---

_End of IRONFORGE SKILL.md v1.1.2. Produced by following the Six-Phase Distillation Process from the `to-distill-project-into-skill` meta-skill. Last updated 2026-07-03 (post-audit remediation: 3 Critical + 4 High + 8 Medium findings addressed; 183/183 tests passing; 0 vulnerabilities; v1.1.1 documentation accuracy patch: 11 findings corrected; v1.1.2 hydration fix documentation: toLocaleString() H5 lesson, anti-pattern, and debugging entry added)._
