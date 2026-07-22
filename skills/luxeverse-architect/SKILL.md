---
name: luxeverse-architect
description: >
  LuxeVerse Architect Skill
  Comprehensive Architectural & Execution Framework for Cinematic, Production-Grade, Anti-Generic Web Platforms
triggers: 
  - "build luxury e-commerce"
  - "cinematic UI architecture"
  - "Next.js 16 phased rollout"
  - "anti-generic design system"
  - "tRPC Zustand commerce"
  - "NextAuth v4 App Router tRPC"
  - "Prisma Decimal service pattern"
  - "RSC factory service"
  - "cookies() Promise Next.js 15"
  - "next-intl v4 configuration"
  - "next-intl defineRouting getRequestConfig"
  - "next-intl Turbopack alias"
  - "next-intl middleware to proxy migration"
  - "app router root layout tags"
  - "locale route groups"
  - "route restructuring hygiene"
  - ".next cache staleness"
  - "Turbopack resolveAlias"
version: 5.0.0
---

**Scope**: Phases 0–5 verified (Foundation, Core Commerce, Cinematic Experience, AI Integration, Scale & Social Remediation, Hardening & Production Data Integration)

- Next.js 16 App Router `root layout.tsx` **must include `<html>` and `<body>` tags** — missing them throws "Missing root layout tags" runtime error for all non-`[locale]` routes
- Route restructuring: **all locale-dependent pages moved to `[locale]/(routes)` groups** to ensure `[locale]/layout.tsx` wraps them with `<html>` `<body>` and i18n providers
- Root `layout.tsx` acts as a **minimal shell** — must not include `<Navbar>` or `<Footer>`; those belong in `[locale]/layout.tsx`
- **Anti-pattern exposed**: Deleting source routes without clearing `.next/types/` cache causes TS2307 "Cannot find module" errors (stale `.d.ts` pointing to deleted files)
- **Staleness risk**: Next.js `.next/types/` auto-generates at build time; always run `rm -rf .next/` after deleting routes or pages
- Moved pages from root-level (`/shop`, `/editorial`, `/checkout`, `/search`, `/loyalty`, `/style-quiz`, `(auth)`) to `app/[locale]/(routes)/` for consistent locale-wrapped routing
- Import path hygiene: moved pages must use path aliases (`@/stores/...` not `../../stores`) to prevent branch-relative breakage after route restructuring
- **Verification pipeline expanded**: `pnpm typecheck && pnpm lint && pnpm test && pnpm build` — all gates must be green before any architectural change is considered complete
- **i18n v4 architecture**: `routing.ts` (Edge) + `request.ts` (Node.js) + `proxy.ts` (middleware) split validated and documented with exact configuration
- **params duality (Next.js 16)**: page `params` typed as `Promise<{...}>` to satisfy `.next/types/` auto-generated types, but at runtime it is a plain object
- **Turbopack alias**: `turbopack.resolveAlias: { "next-intl/config": "./src/i18n/request.ts" }` is mandatory for Turbopack compatibility
- **Dynamic import resolution**: paths inside aliased files resolve from the alias target location, not the source tree — move `messages/` into `src/` and use relative imports in `request.ts`
- **Prisma Decimal**: convert `Decimal` to `Number()` in service layers before passing to client components
- **Service factory pattern**: validated for RSC data flow (`createEditorialService()`, `createProductService()`, etc.)

**Triggers**: `build luxury e-commerce`, `cinematic UI architecture`, `Next.js 16 phased rollout`, `anti-generic design system`, `tRPC Zustand commerce`, `NextAuth v4 App Router tRPC`, `Prisma Decimal service pattern`, `RSC factory service`, `cookies() Promise Next.js 15`, `next-intl v4 configuration`, `next-intl defineRouting getRequestConfig`, `next-intl Turbopack alias`, `next-intl middleware to proxy migration`, `app router root layout tags`, `locale route groups`, `route restructuring hygiene`, `.next cache staleness`, `Turbopack resolveAlias`

---

## 0. Preface: What This Skill Is

This skill encodes every hard-won lesson, every corrected anti-pattern, and every validated architectural decision from the LuxeVerse project — a cinematic luxury e-commerce platform. **It is not a template. It is a field-tested execution manual forged from real implementation, real review cycles, and real corrections.**

Every section below was validated in battle. Skipping any section risks reproducing the exact same mistakes we caught and fixed.

---

## 1. The 6-Phase Execution Framework (Non-Negotiable)

Follow this exact sequence for every task. No code without plan alignment. No "done" without verification.

| Phase | Objective | Gate | Must Pass Before Proceeding |
|---|---|---|---|
| **ANALYZE** | Deep requirement mining, risk assessment, ambiguity identification | PRD/skill section read cover to cover. Existing code audited. Multiple approaches explored. | Never skip |
| **PLAN** | File matrix, success criteria, timeline, effort estimation | Explicit user sign-off. Confirmation question asked. | Gate: no code without documented plan |
| **VALIDATE** | Confirm alignment, address concerns, modify if needed | Documented approval. User explicitly confirms. | Gate: address all concerns |
| **IMPLEMENT** | Modular components, TDD, inline docs | Component tests pass before integration. No error patterns present. | Gate: zero console errors, all states handled |
| **VERIFY** | `tsc --noEmit`, a11y, perf, security | Axe-core ≥ 95, LCP < 2.5s, no critical audit, zero `test.skip` | Gate: all checks green |
| **DELIVER** | Handoff docs, runbook, next steps, knowledge transfer | Complete documentation. Nothing ambiguous. | Gate: future agent can onboard from docs alone |

---

## 2. Complete Architecture Blueprint

### 2.1 Monorepo Structure (Exact)
```
/
├── apps/
│   └── web/                          # Next.js 16 application (RSC-first, App Router)
│       ├── next.config.ts             # Next.js 16 + Turbopack + next-intl
│       ├── src/
│       │   ├── app/
│       │   │   ├── globals.css            # Tailwind v4 @theme inline (OKLCH, fluid type, golden ratio)
│       │   │   ├── layout.tsx             # Root layout: MUST contain <html> and <body> (even if minimal)
│       │   │   ├── page.tsx               # Redirects to /{defaultLocale} (or homepage if no i18n)
│       │   │   └── [locale]/
│       │   │       ├── layout.tsx         # Locale layout: Providers, Fonts, Navbar, Footer, <html> <body>
│       │   │       ├── page.tsx           # Homepage (Hero, Marquee, etc.)
│       │   │       ├── account/page.tsx
│       │   │       ├── pwa-test/page.tsx
│       │   │       └── (routes)/          # All locale-dependent pages moved here
│       │   │           ├── shop/               # /{locale}/shop
│       │   │           │   ├── page.tsx
│       │   │           │   └── [category]/[slug]/page.tsx
│       │   │           ├── editorial/          # /{locale}/editorial
│       │   │           │   ├── page.tsx
│       │   │           │   └── [slug]/page.tsx
│       │   │           ├── checkout/           # /{locale}/checkout
│       │   │           ├── search/             # /{locale}/search
│       │   │           ├── loyalty/            # /{locale}/loyalty
│       │   │           ├── style-quiz/         # /{locale}/style-quiz
│       │   │           ├── login/              # /{locale}/login
│       │   │           └── register/           # /{locale}/register
│       │   ├── components/
│       │   │   ├── layout/
│       │   │   │   ├── Navbar.tsx              # RSC (no "use client")
│       │   │   │   └── Footer.tsx              # RSC (no "use client")
│       │   │   ├── shared/
│       │   │   │   ├── SkipLink.tsx            # First child in <body>, focus-visible ring
│       │   │   │   ├── ErrorBoundary.tsx       # Client component
│       │   │   │   └── ScrollReveal.tsx        # IntersectionObserver for .reveal animations
│       │   │   ├── product/
│       │   │   │   ├── ProductCard.tsx   # RSC
│       │   │   │   ├── ProductGallery.tsx # "use client"
│       │   │   │   ├── VariantSelector.tsx     # "use client"
│       │   │   │   ├── StickyAddToBar.tsx      # "use client"
│       │   │   │   ├── QuickAddButton.tsx      # "use client"
│       │   │   │   ├── PriceDisplay.tsx        # RSC
│       │   │   │   ├── ProductGridSkeleton.tsx
│       │   │   │   └── PDPSkeleton.tsx
│       │   │   └── sections/
│       │   │       ├── HeroSection.tsx         # Asymmetric left-aligned cinematic hero
│       │   │       ├── CollectionSpread.tsx    # Oblique grid with clip-path hover
│       │   │       ├── AIStylistSection.tsx     # Conversational chat bubble UI
│       │   │       ├── SustainabilityMetrics.tsx# Full-bleed dark floating stats
│       │   │       ├── NewsletterSignup.tsx    # "Request Access" invitation
│       │   │       ├── MarqueeBand.tsx
│       │   │       ├── ProductScroll.tsx
│       │   │       ├── CraftsmanshipSection.tsx
│       │   │       └── EditorialSection.tsx
│       │   ├── hooks/
│       │   │   ├── useFocusTrap.ts        # Zero dependencies
│       │   │   ├── useReducedMotion.ts    # window.matchMedia("prefers-reduced-motion")
│       │   │   └── useCart.ts             # Zustand selector hook
│       │   ├── lib/
│       │   │   ├── prisma.ts              # Singleton PrismaClient
│       │   │   ├── schemas.ts             # Zod v4 schemas
│       │   │   ├── auth.ts                # NextAuth v5 universal `auth()`
│       │   │   ├── sentry.ts              # Error tracking stub
│       │   │   ├── crypto.ts              # @node-rs/bcrypt wrapper
│       │   │   └── utils.ts               # cn(), formatCurrency(), etc.
│       │   ├── server/
│       │   │   ├── trpc.ts                # createTRPCContext, createCaller
│       │   │   ├── context.ts             # Context builder
│       │   │   ├── index.ts               # App router
│       │   │   ├── routers/
│       │   │   │   ├── product.ts         # getBySlug, listByCategory, search
│       │   │   │   ├── cart.ts            # get, addItem, removeItem, updateQuantity
│       │   │   │   ├── visualSearch.ts    # AI visual search
│       │   │   │   ├── newsletter.ts      # Newsletter subscription
│       │   │   │   ├── order.ts           # create, get, list for user
│       │   │   │   └── ...
│       │   │   └── services/
│       │   │       ├── editorial.service.ts       # Factory: createEditorialService()
│       │   │       ├── featuredCollections.service.ts # Factory
│       │   │       ├── newArrivals.service.ts       # Factory
│       │   │       ├── newsletter.service.ts        # Factory
│       │   │       ├── product.service.ts           # Factory
│       │   │       └── cart.service.ts              # Factory, typed mapCart()
│       │   ├── stores/
│       │   │   ├── cart.ts                # Zustand: items[], isOpen, isLoading (partialize items ONLY)
│       │   │   └── auth.ts                # Ephemeral (NO persist), tracks auth status
│       │   ├── types/
│       │   │   └── index.ts               # Type unions (not enums)
│       │   ├── test/
│       │   │   ├── setup.ts               # rAF mock, crypto mock, vi globals
│       │   │   └── factories.ts           # getMockProduct(), getMockUser()
│       │   └── proxy.ts                   # Next.js 16 middleware (formerly middleware.ts)
├── packages/
│   ├── config/
│   │   ├── tsconfig/
│   │   │   ├── base.json                  # strict, erasableSyntaxOnly, verbatimModuleSyntax
│   │   │   └── next.json                  # extends base.json + next-specific
│   │   ├── eslint/
│   │   │   └── base.js                    # Flat config: no-any, no-enum, no-namespace
│   │   └── tsconfig/package.json          # exports base.json
│   ├── ui/
│   │   ├── src/
│   │   │   ├── button.tsx                 # CVA: default, outline, ghost, luxury
│   │   │   ├── input.tsx
│   │   │   ├── badge.tsx
│   │   │   ├── avatar.tsx
│   │   │   ├── skeleton.tsx
│   │   │   └── index.ts                   # Barrel export
│   │   ├── tsconfig.json
│   │   └── package.json
│   └── utils/
│       ├── src/
│       │   ├── cn.ts                      # clsx + tailwind-merge
│       │   └── index.ts
│       └── package.json
├── .github/workflows/ci.yml               # typecheck → lint → test → build
├── scripts/
│   ├── validate-colors.sh                 # Block raw hex in className
│   └── validate-deprecated-twind.sh     # Block v3 utilities
├── turbo.json                             # Pipeline with caching
└── pnpm-workspace.yaml
```

### 2.2 `next.config.ts` — Next.js 16 + Turbopack + next-intl v4

```typescript
import type { NextConfig } from "next";
import createNextIntlPlugin from "next-intl/plugin";

// --- next-intl v4 (CRITICAL: must point to request.ts, NOT routing.ts) ---
const withNextIntl = createNextIntlPlugin("./src/i18n/request.ts");

const nextConfig: NextConfig = {
  // Next.js 16: cacheComponents enables Partial Prerendering (PPR)
  cacheComponents: true,

  turbopack: {
    // Resolve aliased `next-intl/config` to the Node.js-side `request.ts`
    resolveAlias: {
      "next-intl/config": "./src/i18n/request.ts",
    },
  },

  i18n: {
    locales: ["en", "de", "fr", "zh"],
    defaultLocale: "en",
  },

  images: {
    remotePatterns: [
      { protocol: "https", hostname: "images.unsplash.com" },
    ],
  },

  // Next.js 16: Enforce strict handling for cookies & headers
  experimental: {},

  // Note: `eslint` key removed in Next.js 16 — use .eslintrc only
};

export default withNextIntl(nextConfig);
```

---

## 3. Tailwind CSS v4 — CSS-First Configuration

### 3.1 No `tailwind.config.ts` (Migrated to `globals.css`)

Since Tailwind v4, `tailwind.config.js|ts` is **deprecated**. All configuration lives in `@theme inline` inside `src/app/globals.css`.

```css
@theme inline {
  /* Semantic color palette (OKLCH) */
  --color-obsidian-50: #fafafb;
  --color-obsidian-100: #f0f0f2;
  --color-obsidian-200: #e1e1e5;
  --color-obsidian-300: #d1d1d7;
  --color-obsidian-400: #a9a9b1;
  --color-obsidian-500: #7c7c89;
  --color-obsidian-600: #525260;
  --color-obsidian-700: #3a3a47;
  --color-obsidian-800: #24242e;
  --color-obsidian-900: #1a1a24;
  --color-obsidian-950: #111119;

  --color-neon-cyan: #00e1d9;
  --color-neon-pink: #e6004d;

  --color-metallic-champagne: #d4af37;
  --color-metallic-gold: #bca13f;
}

@utility glass {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

@utility btn-primary {
  background: linear-gradient(to right, #d4af37, #bca13f);
  color: #111119;
  padding: 0.75rem 1.25rem;
  border-radius: 0.25rem;
  font-weight: 600;
}

/* ... additional cinematic utilities ... */
```

### 3.2 v4 Utility Migrations (Before → After)

| Deprecated (v3) | Modern (v4) |
|---|---|
| `bg-gradient-to-r` | `bg-linear-to-r` |
| `outline-none` | `outline-hidden` |
| `flex-shrink-0` | `shrink-0` |

---

## 4. i18n — next-intl v4 Split Architecture

### 4.1 Mandatory File Split (v4)

| File | Runtime | Purpose | Consumed By |
|------|---------|---------|-------------|
| `routing.ts` | Edge | Routing rules, locale matching | `proxy.ts` (`createMiddleware`), `Navigation` APIs |
| `request.ts` | Node.js | Per-request message loading | `createNextIntlPlugin`, Server Components (`getTranslations`) |

**Anti-pattern**: Keeping a monolithic `i18n.ts` causes `TypeError: Cannot read property 'get' of undefined` because `createNextIntlPlugin` expects the Node.js `getRequestConfig` factory, while `createMiddleware` expects the Edge `defineRouting`.

### 4.2 `routing.ts` — Edge Runtime

```typescript
// src/i18n/routing.ts
import { defineRouting } from "next-intl/routing";
import { locales, defaultLocale } from "./config";

export const routing = defineRouting({
  // Cast required: TypeScript readonly tuple → Array<string>
  locales: locales as unknown as Array<string>,
  defaultLocale,
  localePrefix: "always",
});

export { locales, defaultLocale };
export type { Locale } from "./config";
```

### 4.3 `request.ts` — Node.js Runtime

```typescript
// src/i18n/request.ts
import { getRequestConfig } from "next-intl/server";
import { routing } from "./routing";

export default getRequestConfig(async ({ requestLocale }) => {
  const requested = await requestLocale;
  const locale =
    requested && routing.locales.includes(requested)
      ? (requested as Locale)
      : routing.defaultLocale;

  // Dynamic import: path relative to THIS file's location in the build output
  const messages = (await import(`../messages/${String(locale)}.json`)).default;

  return { locale, messages };
});
```

---

## 5. next-intl v4 / Turbopack Traps

### 5.1 Alias Mismatch → `Error: Couldn't find next-intl config file`

**Cause**: `createNextIntlPlugin("./src/i18n/routing.ts")` points to the Edge file (defining routing rules), but the plugin needs the Node.js file (`request.ts`) that provides `getRequestConfig()`.

**Fix**:
```typescript
const withNextIntl = createNextIntlPlugin("./src/i18n/request.ts");
```

**Also required**: Turbopack must alias `next-intl/config` to the **same** file used by `createNextIntlPlugin`:
```typescript
turbopack: {
  resolveAlias: {
    "next-intl/config": "./src/i18n/request.ts",
  },
},
```

### 5.2 Dynamic `import()` in Aliased Files → "Module not found"

**Cause**: When `next-intl` aliases `request.ts` at build time, dynamic `import()` paths resolve from the **alias target location**, not the source tree.

**Before (broken)**:
```
/home/project/LuxeVerse/apps/web/
├── messages/              ← at root
├── src/
│   └── i18n/
│       └── request.ts     ← import("../../../messages/...") → FAILS
```

**After (fixed)**:
```
/home/project/LuxeVerse/apps/web/
├── src/
│   ├── messages/          ← moved into src/
│   └── i18n/
│       └── request.ts     ← import("../messages/...") → WORKS
```

**Rule of thumb**: Place any directory dynamically imported by an aliased file **at the same level or below** the aliased file in the source tree.

---

## 6. Next.js 16 `params` Duality

**CRITICAL**: Next.js 16's `.next/types/` generator types `params` as `Promise<any>` for page components, even though at runtime `params` is a plain object.

| Layer | Type | Must Use |
|-------|------|---------|
| **Runtime** | Plain object `{}` | `const { slug } = params` (direct destructuring) |
| **Generated Types** (`.next/types/`) | `Promise<{ ... }>` | `params: Promise<{...}>` + `await` to satisfy tsc |

### 6.1 Pages
```tsx
// ✅ CORRECT — satisfies both runtime and generated types
interface PageProps {
  params: Promise<{ slug: string }>;
}
export default async function Page({ params }: PageProps) {
  const { slug } = await params; // Required by .next/types/ Promise<T>
}
```

### 6.2 Layouts
```tsx
// ✅ CORRECT — layouts always receive a real Promise
export default async function Layout({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
}
```

---

## 7. Next.js 16 App Router — Root Layout Requirements

### 7.1 The "Missing Root Layout Tags" Error

**Error from Next.js**: `Missing <html> and <body> tags in the root layout.`

**When it happens**: Any page that does not match a `[locale]` route falls through to the **root `layout.tsx`**. If that root layout does not return `<html>` and `<body>`, Next.js throws.

```
app/layout.tsx -> returns only <>{children}</>  ❌  (throws)
  ↳ app/[locale]/layout.tsx -> returns <html><body>...</body></html> ✅
  ↳ app/[locale]/page.tsx                    ✅  (inherits locale layout)
  ↳ app/shop/page.tsx                         ❌  (inherits ROOT layout. no <html><body>)
```

**Fix**: Every `app/layout.tsx` MUST return `<html>` and `<body>`:

```tsx
// app/layout.tsx (ROOT layout — minimal shell)
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
```

**BUT**: When using `[locale]/layout.tsx` that also renders `<html>`/`<body>`, you MUST remove them from the root layout to prevent a **hydration mismatch** (see §7.3).

**Root layout anti-patterns**:
- ❌ Do NOT put `<Navbar>` or `<Footer>` in the root layout. Those are locale-dependent and belong in `[locale]/layout.tsx`.
- ❌ Do NOT put `<NextIntlClientProvider>` or any i18n context in the root layout. Put it in `[locale]/layout.tsx`.
- ✅ Root layout is a **structural shell only** — fonts, metadata, and `children`.

### 7.2 Locale Route Groups (`app/[locale]/(routes)/`)

When all pages depend on `locale` (i18n), move them into a `(routes)` group inside `[locale]`:

```
app/
├── layout.tsx                           # Root shell: <html> <body> {children}
├── page.tsx                             # → redirect to /{defaultLocale}
└── [locale]/
    ├── layout.tsx                       # Locale shell: Fonts, i18n, Navbar, Footer
    ├── page.tsx                          # Homepage
    └── (routes)/                         # Group: all pages inherit [locale]/layout.tsx
        ├── shop/
        │   ├── page.tsx
        │   └── [category]/[slug]/page.tsx
        ├── editorial/
        │   ├── page.tsx
        │   └── [slug]/page.tsx
        ├── checkout/page.tsx
        ├── search/page.tsx
        ├── loyalty/page.tsx
        ├── style-quiz/page.tsx
        ├── login/page.tsx
        └── register/page.tsx
```

**Benefits**:
- Every route automatically gets `locale` from the parent layout.
- No duplicate `<html>`/`<body>` definitions across pages.
- i18n context, fonts, and layout elements (Navbar/Footer) are injected once at the group level.
- `(routes)` is a **route group** — it does not affect the URL path.

**Migration steps** (Option B from status_18.md):
1. Create `app/[locale]/(routes)/` directory.
2. Move all root-level pages (`shop`, `editorial`, `checkout`, `search`, `loyalty`, `style-quiz`, `(auth)`) into `app/[locale]/(routes)/`.
3. Update all **relative imports** (`../../stores/`) in moved pages to **path aliases** (`@/stores/`) to prevent breakage.
4. Delete old root-level directories to avoid duplicate routes.
5. **Clear `.next/` cache**: `rm -rf .next/` (stale generated types will crash tsc).
6. Run `pnpm typecheck` — if TS2307 "Cannot find module" appears, it means stale `.d.ts` still references the deleted routes. Re-clear `.next/` and repeat.
7. Verify `pnpm typecheck && pnpm lint &&pnpm test` all pass.

### 7.3 Hydration Mismatch: Root Layout vs. Locale Layout

**Error from Next.js**: `A tree hydrated but some attributes of the server rendered HTML didn't match the client properties. This won't be patched up.`

**When it happens**: Both `app/layout.tsx` AND `app/[locale]/layout.tsx` render `<html>` and `<body>` tags with conflicting attributes (e.g., `lang="en"` vs `lang={locale}`).

Result: Next.js server-renders one set of attributes on `<html>`/`<body>`, but the React client expects a different set from the locale layout, causing a hydration mismatch.

**Root cause analysis**: The error trace from `error.txt` shows the exact conflict:
```
<html lang="en" dir="ltr" className="font-variables...">
  <body className="bg-obsidian-50 text-obsidian-900 antialiased">
```
However, `app/[locale]/layout.tsx` renders:
```
<html lang={locale} dir={isRTL(locale) ? "rtl" : "ltr"} className={fontVars}>
  <body className="bg-obsidian-50 text-obsidian-900 antialiased">
```
The server might render from the root layout, then the client re-hydrates with the locale layout, producing different attribute values for the same `<html>` and `<body>` DOM elements.

**Fix**: Remove `<html>` and `<body>` from the root layout. Render them **only** in `app/[locale]/layout.tsx`.

```tsx
// app/layout.tsx (ROOT layout — should NOT render <html>/<body>)
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "LuxeVerse | Cinematic Luxury Commerce",
  description: "...",
};

// ❌ DO NOT render <html> or <body> here if [locale]/layout.tsx renders them
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
```

```tsx
// app/[locale]/layout.tsx (LOCALE layout — MUST render <html>/<body>)
export default async function LocaleLayout({ children, params }: LocaleLayoutProps) {
  const { locale } = await params;

  return (
    <html lang={locale} dir={isRTL(locale) ? "rtl" : "ltr"} className={fontVars}>
      <body className="bg-obsidian-50 text-obsidian-900 antialiased">
        {children}
      </body>
    </html>
  );
}
```

**Why this works**: Next.js uses the innermost layout that renders `<html>`/`<body>` as the effective root layout. When the root layout removes them, the locale layout becomes the sole owner of these tags, eliminating the conflict.

### 7.4 tRPC Provider Must Be Mounted in Layout

**Error**: `Unable to find tRPC Context. Did you forget to wrap your App inside TRPCProvider HoC?`

**Root cause**: The tRPC React hooks (like `trpc.cart.addItem.useMutation()`) require a `<TRPCProvider>` context to be present in the component tree. If the `TRPCProvider` is defined but never included in any layout, the hooks will throw at runtime.

**Pattern**: Create a single `ClientProviders` component (marked with `"use client"`) that wraps both `NextIntlClientProvider` and `TRPCProvider`, then use it in your locale layout.

```tsx
// src/components/providers/ClientProviders.tsx
"use client";
import { NextIntlClientProvider } from "next-intl";
import { TRPCProvider } from "@/trpc/provider";

export function ClientProviders({ locale, messages, children }) {
  return (
    <NextIntlClientProvider locale={locale} messages={messages}>
      <TRPCProvider>{children}</TRPCProvider>
    </NextIntlClientProvider>
  );
}
```

```tsx
// src/app/[locale]/layout.tsx
import { ClientProviders } from "@/components/providers/ClientProviders";

export default async function LocaleLayout({ children, params }) {
  const { locale } = await params;
  const messages = (await import(`../../messages/${locale}.json`)).default;

  return (
    <html lang={locale} dir={isRTL(locale) ? "rtl" : "ltr"} className={fontVars}>
      <body className="bg-obsidian-50 text-obsidian-900 antialiased">
        <ClientProviders locale={locale} messages={messages}>
          {children}
        </ClientProviders>
      </body>
    </html>
  );
}
```

**Why this is necessary**: In the Next.js App Router, layouts are Server Components by default. Client-side providers like tRPC and next-intl require React Context, which is only available in client components. A dedicated `ClientProviders` component is the idiomatic bridge between the server layout and the client-side context.

**Anti-pattern**: Importing `trpc` hooks in a component that is NOT wrapped in `TRPCProvider` (either directly or via a parent layout) will cause the context error. Always ensure the provider is mounted at the layout level.

---

## 8. Post-Route-Restructure Hygiene

### 8.1 Stale `.next/types/` Cache

**Symptom after deleting routes/pages**:
```
TS2307: Cannot find module '../../../.../old-route/page' or its corresponding type declarations.
```

**Cause**: Next.js auto-generates `.next/types/` `.d.ts` files that point to old route locations. These are **not** deleted when you remove the source files.

**Fix**:
```bash
rm -rf apps/web/.next/
# Then re-run typecheck to regenerate from the new source tree
pnpm typecheck
```

### 8.2 Import Path Breakage

After moving pages deeper into `app/[locale]/(routes)/`, relative imports like `../../stores/style-quiz` will fail because the relative tree changed.

**Before (broken after move)**:
```typescript
// Was in: app/style-quiz/page.tsx
import { useQuizStore } from "../../stores/style-quiz";
```

**After (stable via alias)**:
```typescript
// Now in: app/[locale]/(routes)/style-quiz/page.tsx
import { useQuizStore } from "@/stores/style-quiz";
```

**Rule**: Always use path aliases (`@/...`) for cross-module imports. Use relative paths only within the same feature folder.

---

## 9. Prisma & tRPC — Data Flow & Service Factories

### 9.1 Service Factory Pattern (RSC-First)

Use a factory function to return typed Prisma queries from Server Components. Never call Prisma directly in a page/server action.

```typescript
// server/services/featuredCollections.service.ts
import prisma from "@/lib/prisma";
import type { Prisma } from "@/prisma/client";

export type FeaturedCollectionsInclude = Prisma.FeaturedCollectionInclude;

export function createFeaturedCollectionsService() {
  return {
    getAll: (args?: { include?: FeaturedCollectionsInclude }) =>
      prisma.featuredCollection.findMany({ include: args?.include }),
    getById: (id: string, args?: { include?: FeaturedCollectionsInclude }) =>
      prisma.featuredCollection.findUnique({ where: { id }, include: args?.include }),
  };
}
```

### 9.2 Prisma `Decimal` Conversion

Prisma returns `Decimal` for monetary fields (`@db.Decimal(10,2)`). Convert to `Number` in the **service layer** before passing to Client Components.

```typescript
// ❌ Anti-pattern: passing Decimal to client
return prisma.product.findMany();

// ✅ Correct: convert in service
return prisma.product.findMany().then((products) =>
  products.map((p) => ({
    ...p,
    price: Number(p.price), // Decimal → number
  }))
);
```

---

## 10. Zustand — State Discipline

### 10.1 Selector Rules

```typescript
// ❌ Anti-pattern: object return causes re-render loops
const { items, count } = useCartStore((s) => ({ items: s.items, count: s.count }));

// ✅ Correct: use useShallow for stable object selectors
import { useShallow } from "zustand/react/shallow";
const { items, count } = useCartStore(useShallow((s) => ({ items: s.items, count: s.count })));

// ✅ Also correct: single primitive selector
const count = useCartStore((s) => s.count);
```

### 10.2 Persistence Rules

Persist **only data state**, never UI state (`isOpen`, `isLoading`):

```typescript
// zustand/middleware
persist(store, {
  name: "cart",
  partialize: (state) => ({
    items: state.items, // ✅ persist data
    // isOpen: state.isOpen, ❌ NEVER persist UI state
  }),
});
```

---

## 11. Accessibility & Performance

### 11.1 `useReducedMotion`

```typescript
// hooks/useReducedMotion.ts
import { useEffect, useState } from "react";

export function useReducedMotion() {
  const [reduced, setReduced] = useState(false);
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

### 11.2 Scroll Reveal (`IntersectionObserver`)

Toggle `.reveal.visible` class based on intersection:
```tsx
// components/shared/ScrollReveal.tsx
export default function ScrollReveal({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  const ref = useRef<HTMLDivElement>(null);
  const [isVisible, setIsVisible] = useState(false);
  useEffect(() => {
    const observer = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) setIsVisible(true);
    });
    ref.current && observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);
  return (
    <div ref={ref} className={clsx("reveal", isVisible && "visible", className)}>
      {children}
    </div>
  );
}
```

---

## 12. Verification Pipeline

Always run the full pipeline before declaring "done":

```bash
# Full verification pipeline
pnpm typecheck && pnpm lint && pnpm test && pnpm build
```

| Check | Command | Target |
|---|---|---|
| TypeScript | `pnpm typecheck` | Zero errors |
| Lint | `pnpm lint` | Tailwind v3 scan, raw hex scan, no `any`, no `enum` |
| Test | `pnpm test` | All tests pass, zero `test.skip` |
| Build | `pnpm build` | Production build succeeds |
| Prisma Sync | `cd apps/web && pnpm db:generate` | Fresh client after schema changes |

---

## 13. Anti-Patterns Index

| Anti-Pattern | Why It Breaks | The Fix |
|---|---|---|
| `enum` (TypeScript) | Violates `erasableSyntaxOnly` — compiles to runtime IIFE | `type Status = "ACTIVE" \| "DRAFT"` |
| `namespace` | Violates `erasableSyntaxOnly` — compiles to runtime closure | Use ES modules |
| `any` | Subverts strict mode and tRPC end-to-end safety | `unknown` or typed interface |
| `bg-[#hex]` in className | Bypasses design system, breaks theming | `bg-obsidian-950` |
| `bg-gradient-to-r` (v3) | Deprecated in Tailwind v4 | `bg-linear-to-r` |
| `outline-none` | Deprecated in Tailwind v4 | `outline-hidden` |
| `flex-shrink-0` | Deprecated in Tailwind v4 | `shrink-0` |
| `getServerSession` | Deprecated in Auth.js v5 — returns `undefined` in Server Actions | `auth()` universal function |
| Monolithic `i18n.ts` | Runtime crash in next-intl v4 | Split into `routing.ts` + `request.ts` |
| Stale `.next/` after route changes | TS2307 "Cannot find module" from old generated types | `rm -rf .next/` |
| Root `layout.tsx` without `<html>`/`<body>` | `/missing-root-layout-tags` runtime error | Always include `<html><body>{children}</body></html>` |
| Root `layout.tsx` WITH `<html>`/`<body>` when `[locale]/layout.tsx` also has them | Hydration mismatch: conflicting `lang`, `dir`, `className` attributes | Remove `<html>`/`<body>` from root layout; let locale layout own them exclusively |
| Relative imports (`../../`) in moved pages | Breaks after route restructuring | Use path aliases (`@/...`) |
| Persisting UI state in Zustand | `isOpen` restored to `true` on page load, causing jarring popups | `partialize` to data fields only |
| Direct Prisma in pages | Tight coupling, hard to test, no typed boundaries | **Service factory** (`createXxxService()`) |
| tRPC hooks used without `TRPCProvider` | `Unable to find tRPC Context` runtime error | Mount `<TRPCProvider>` in a `'use client'` component inside your layout |

---

## 14. Design System & Choreography

### 14.1 Color Palette (OKLCH)
| Token | Hex | Purpose |
|---|---|---|
| `obsidian-50` | `#fafafb` | Lightest background |
| `obsidian-900` | `#1a1a24` | Primary text |
| `obsidian-950` | `#111119` | Button/dark surfaces |
| `neon-cyan` | `#00e1d9` | Focus indicators |
| `neon-pink` | `#e6004d` | Errors/callouts |
| `metallic-champagne` | `#d4af37` | Primary CTAs |
| `metallic-gold` | `#bca13f` | Hover states |

### 14.2 Cinematic Animation System (`globals.css`)
- **Hero reveal**: Staggered `opacity` + `translateY` (0.8s, `cubic-bezier(0.16, 1, 0.3, 1)`).
- **Marquee**: `translateX(-50%)` infinite linear loop (30s).
- **Scroll reveal**: `IntersectionObserver` toggles `.reveal.visible`.
- **Clip-path hover**: `polygon()` morph on hover (0.6s ease).

---

## 15. Final Directive

**Every element must justify its existence.** Reject generic AI tropes. Prioritize intentionality over trends. Accessibility is non-negotiable. Performance is luxury. Deliver nothing less than production-grade, meticulously verified, and architecturally sound.

---

## 16. Phase 5 Hardening: Server-Side Auth, Real Data & Service Factories

### 16.1 Server-Side Auth in Server Actions (Auth.js v5)

**Problem**: `getServerSession` is Pages Router-only. In App Router Server Actions, it throws `TypeError: Cannot read properties of undefined (reading 'headers')`.

**Solution**: Use the universal `auth()` function from `src/auth.ts` (Auth.js v5). It natively handles session extraction in Server Components, Server Actions, and Route Handlers without manual cookie assembly.

```typescript
// src/app/actions/checkout.actions.ts
import { auth } from "@/auth";

export async function createCheckoutAction(prevState: CheckoutState, formData: FormData) {
  const session = await auth();
  if (!session?.user?.id) {
    return { status: "error", message: "Authentication required." };
  }
  const userId = session.user.id;
  // ... proceed with checkout
}
```

**Deprecated (v4 pattern — do not use)**:
```typescript
// ❌ WRONG — getToken and getServerSession are deprecated in v5
import { getToken } from "next-auth/jwt"; // BANNED
import { getServerSession } from "next-auth"; // BANNED
```

**Critical Gotchas**
| Issue | Root Cause | Fix |
|---|---|---|
| `Property 'get' does not exist on type Promise<ReadonlyRequestCookies>` | Next.js 15+ `cookies()` is async | `const cookieStore = await cookies();` |
| `TypeError: Cannot read properties of undefined (reading 'headers')` | `getServerSession` is Pages Router only | Use `auth()` from `src/auth.ts` |
| `User not authenticated` | `auth()` returns null for unauthenticated users | Guard with `if (!session) { redirect("/login") }` |

---

### 16.2 Service Factory Pattern for Reproducible Data

**Problem**: Components hardcode mock data arrays instead of fetching from Prisma
**Solution**: `create*Service()` factory functions with typed `map*` helper, Decimal conversion

```typescript
// src/server/services/newArrivals.service.ts
import { prisma } from "@/lib/prisma";

export interface NewArrival { id: string; ... }

export function createNewArrivalsService() {
  return {
    async list() {
      const products = await prisma.product.findMany({
        where: { status: "ACTIVE", newArrival: true },
        orderBy: { createdAt: "desc" },
        take: 8,
        select: {
          id: true, slug: true, name: true, price: true, compareAtPrice: true,
          images: { where: { isPrimary: true }, select: { url: true }, take: 1 },
          category: { select: { name: true } },
          newArrival: true,
        },
      });
      // Map Decimal to number to avoid toJSON serialization issues
      return products.map(p => ({
        ...p,
        price: Number(p.price),
        compareAtPrice: p.compareAtPrice ? Number(p.compareAtPrice) : null,
        image: p.images[0]?.url ?? null,
        category: p.category.name,
      }));
    },
  };
}
```

**Key Insight**: Prisma `Decimal` (PostgreSQL `@db.Decimal(10, 2)`) serializes as string over JSON, breaking client-side math. Always convert to `Number()` in service layer.

---

### 16.3 RSC → Client Component Data Boundaries

```tsx
// src/components/sections/NewArrivals.tsx (Server Component)
import { createNewArrivalsService } from "@/server/services/newArrivals.service";
import { NewArrivalsClient } from "./NewArrivalsClient";

export async function NewArrivals() {
  const service = createNewArrivalsService();
  const products = await service.list(); // Fetches on server
  return <NewArrivalsClient products={products} />; // Passes to client
}
```

**Rationale**: RSC fetches data (zero client waterfall). Client Component receives data via props (handles scroll, interactivity). tRPC is for mutations, not initial page data.

---

### 16.4 Next.js 15+ `cookies()` API: `Promise<ReadonlyRequestCookies>`

| Next.js Version | API | Code |
|---|---|---|
| **Next.js 14** | `cookies()` returns `ReadonlyRequestCookies` | `cookies().get("key")` |
| **Next.js 15+** | `cookies()` returns `Promise<ReadonlyRequestCookies>` | `(await cookies()).get("key")` |

**Fix**: Always `await cookies()` in App Router Server Actions, Route Handlers, and Server Components.

---

### 16.5 Error Tracking with Zero Hard Dependencies

**Problem**: `@sentry/nextjs` adds ~100KB to bundle and requires complex Webpack/Vite configuration
**Solution**: Dynamic import with fallback stub

```typescript
// src/lib/sentry.ts
export function captureException(error: Error, _context?: { extra: Record<string, unknown> }): void {
  console.error("[Telemetry] Captured exception:", error);
}

// src/app/global-error.tsx
export default function GlobalError({ error }: { error: Error & { digest?: string } }) {
  useEffect(() => {
    if (process.env.NEXT_PUBLIC_SENTRY_DSN) {
      import("@sentry/nextjs")
        .then((Sentry) => Sentry.captureException(error))
        .catch(() => import("@/lib/sentry").then(({ captureException }) => captureException(error)));
    }
  }, [error]);
  // ...
}
```

---

### 16.6 Testing Mock Patterns for Server Actions

```typescript
import { vi } from "vitest";

// Mock next/headers (Next.js 15+ returns a Promise)
vi.mock("next/headers", () => ({
  cookies: vi.fn(() => Promise.resolve({ get: vi.fn().mockReturnValue(undefined) })),
}));

// Mock next-auth/jwt
vi.mock("next-auth/jwt", () => ({
  getToken: vi.fn(() => Promise.resolve(null)),
}));

// Mock prisma
vi.mock("@/lib/prisma", () => ({
  prisma: {
    order: { create: vi.fn().mockResolvedValue({ id: "order-test-123" }) },
  },
}));
```


---

## 17. TypeScript & React 19 Strict Mode (Non-Negotiable)

### 17.1 `erasableSyntaxOnly` — Zero Enums or Namespaces

```typescript
// ❌ WRONG — erasableSyntaxOnly rejects these
enum Status { ACTIVE = "ACTIVE", DRAFT = "DRAFT" }
namespace MyNamespace { export const x = 1; }

// ✅ CORRECT — string unions and ES modules only
type Status = "ACTIVE" | "DRAFT";
```

### 17.2 `verbatimModuleSyntax` — `import type` for Type-Only

```typescript
// ❌ WRONG — imported as module, not type
import { User } from "@/types";
const user: User = { ... };

// ✅ CORRECT — type-only import
import type { User } from "@/types";
```

### 17.3 React 19 Return Types

React 19 removes the global `JSX.Element` type. **Always prefer inferred return types** — explicit `ReactElement` or `JSX.Element` annotations are legacy patterns.

```typescript
// ❌ WRONG — JSX.Element banned in React 19; ReactElement is legacy
function Component(): JSX.Element { ... }
function Component(): ReactElement { ... }

// ✅ CORRECT — inferred return type (preferred for all components)
function Component() { ... }

// ✅ ALSO ACCEPTABLE — if you must annotate, use the element type enum
import type { ReactElement } from "react";
function Component(): ReactElement { ... } // Legacy, do not use in new code
```

**Migration path**: Remove ALL `import type { ReactElement }` and `: ReactElement` / `: Promise<ReactElement>` annotations from existing components. Use inferred return types exclusively.


---

## 18. Zustand v5 Selector Best Practices

### 18.1 Selector Subscription in JSX

```typescript
// ✅ CORRECT — reactive, re-renders on state change
const items = useCartStore((s) => s.items);

// ❌ WRONG — no reactivity, stale data
const items = useCartStore.getState().items; // Never in JSX
```

### 18.2 `useShallow` — Recommended for Object Selectors

Zustand v5 uses strict equality (`Object.is`) for comparisons. When selecting multiple properties in an object, **always use `useShallow`** to prevent unnecessary re-renders and potential infinite loops.

```typescript
import { useShallow } from "zustand/react/shallow";

// ✅ CORRECT — useShallow with object selectors
const { cart, user } = useCartStore(
  useShallow((s) => ({ cart: s.cart, user: s.user }))
);

// ❌ WRONG — object selector returns a new object reference every render
const { cart, user } = useCartStore((s) => ({ cart: s.cart, user: s.user }));
// Triggers infinite re-render loop in v5
```

**Note**: `useShallow` is strongly recommended (not a hard mandate) for object/array selectors. Atomic selectors (single primitive values) do not need it.

### 18.3 `partialize` — Persist Data Only

```typescript
persist(
  (set, get) => ({ ... }),
  {
    name: "luxeverse-cart",
    partialize: (state) => ({ items: state.items }), // Only persist domain data
  }
)
```


---

## 19. Prisma Zero-Enum Pattern

### 19.1 Schema: `String` + TypeScript Unions

```prisma
model Product {
  id     String @id @default(cuid())
  status String @default("ACTIVE") // TypeScript: type Status = "ACTIVE" | "DRAFT" | "ARCHIVED"
}
```

### 19.2 Service Factory with Typed Includes

```typescript
type CartWithItems = Prisma.CartGetPayload<{
  include: { items: { include: { product: true } } }
}>;
```


---

## 20. next-intl v4 Deep-Dive

### 20.1 The Mandatory Split: `routing.ts` vs. `request.ts`

Since `next-intl@3.22` / `v4.0`, the monolithic `i18n.ts` config is **deprecated** and **will cause runtime crashes**. You **must** split into two files:

| File | Purpose | Consumed By | Required Export |
|------|---------|-------------|---------------|
| `src/i18n/routing.ts` | Routing rules (locales, defaultLocale, localePrefix) | `proxy.ts` (`createMiddleware`), `Navigation` APIs | `defineRouting()` |
| `src/i18n/request.ts` | Per-request message loading | `createNextIntlPlugin`, Server Components (`getTranslations`) | `getRequestConfig()` |

**Why the split matters**: `routing.ts` runs in the **Edge runtime** (middleware), while `request.ts` runs in **Node.js** (Server Components). Mixing them causes bundler errors and runtime crashes.

### 20.2 `routing.ts` — Routing Configuration

```typescript
// src/i18n/routing.ts
import { defineRouting } from "next-intl/routing";
import { locales, defaultLocale } from "./config";

export const routing = defineRouting({
  // Cast required: TypeScript readonly tuple → Array<string>
  locales: locales as unknown as Array<string>,
  defaultLocale,
  localePrefix: "always",
});

// Keep backward-compatible re-exports for existing consumers
export { locales, defaultLocale };
export type { Locale } from "./config";
```

**Critical**: `defineRouting` expects `Array<string>`. If your `locales` is a readonly tuple (`as const`), TypeScript will error. Cast through `unknown` → `Array<string>` or use `as unknown as Array<string>`.

### 20.3 `request.ts` — Request Configuration

```typescript
// src/i18n/request.ts
import { getRequestConfig } from "next-intl/server";
import { routing } from "./routing";

export default getRequestConfig(async ({ requestLocale }) => {
  const requested = await requestLocale;
  const locale =
    requested && routing.locales.includes(requested)
      ? (requested as Locale)
      : routing.defaultLocale;

  // Dynamic import path: relative to THIS file's location in the build output
  const messages = (await import(`../messages/${String(locale)}.json`)).default;

  return {
    locale,
    messages,
  };
});
```

**Critical**: The `request.ts` file is aliased by `next-intl/config` at build time. Dynamic import paths are resolved from the **aliased file's location**, not from the source tree. This means:
- If `messages/` is at the project root, but `request.ts` is aliased from `node_modules/next-intl/`, the relative path will resolve to `node_modules/next-intl/messages/` (which doesn't exist).
- **Fix**: Move `messages/` into `src/` so it's in the same directory tree as the aliased file, OR use a path alias.

#### 20.3.1 Dynamic Import Path Resolution in Aliased Files

**Problem**: When `next-intl/config` is aliased, dynamic `import()` paths inside `request.ts` are resolved from the **alias target location** (inside `node_modules/next-intl/`), not from the source tree.

**Example** (broken):
```
/home/project/LuxeVerse/apps/web/
├── messages/              ← at root
├── src/
│   └── i18n/
│       └── request.ts     ← does import("../../../messages/...") → FAILS
```

**Example** (fixed):
```
/home/project/LuxeVerse/apps/web/
├── src/
│   ├── messages/          ← moved into src/
│   └── i18n/
│       └── request.ts     ← does import("../messages/...") → WORKS
```

**Rule of thumb**: Place any directory dynamically imported by an aliased file **at the same level or below** the aliased file in the source tree.

### 20.4 `next.config.ts` — Plugin & Turbopack Alias

```typescript
// next.config.ts
import withPWA from "@ducanh2912/next-pwa";
import createNextIntlPlugin from "next-intl/plugin";

// CRITICAL: Plugin must point to request.ts, NOT routing.ts
const withNextIntl = createNextIntlPlugin("./src/i18n/request.ts");

const nextConfig = {
  // ... other config ...

  // Next.js 16 stable Turbopack config
  turbopack: {
    resolveAlias: {
      // Forces Turbopack to resolve next-intl's internal alias correctly
      "next-intl/config": "./src/i18n/request.ts",
    },
  },
};

// Compose plugins: next-intl wraps config, then PWA wraps the result
export default withPWA({
  dest: "public",
  disable: process.env.NODE_ENV === "development",
})(withNextIntl(nextConfig));
```

**Troubleshooting**: If you see `Error: Couldn't find next-intl config file`, check:
1. `createNextIntlPlugin` points to `request.ts` (not `routing.ts`)
2. `turbopack.resolveAlias` has `"next-intl/config": "./src/i18n/request.ts"`
3. `request.ts` exports a `getRequestConfig()` factory, not a plain object
4. The path in `createNextIntlPlugin` is relative to `next.config.ts`

### 20.5 `proxy.ts` — Next.js 16 Middleware

```typescript
// src/proxy.ts (formerly middleware.ts — Next.js 16 convention)
import createMiddleware from "next-intl/middleware";
import { routing } from "./i18n/routing";

export default createMiddleware(routing);

export const config = {
  matcher: "/((?!api|trpc|_next|_vercel|.*\\..*).*)",
};
```

**Warning**: Next.js 16 deprecates `middleware.ts` in favor of `proxy.ts`. The `createMiddleware` function works identically; only the filename changes.


---

## 21. Next.js 16 `params` Duality (Original Deep-Dive)

**CRITICAL**: Next.js 16's `.next/types/` generator types `params` as `Promise<any>` for page components, even though at runtime `params` is a plain object.

| Layer | Type | Must Use |
|-------|------|---------|
| **Runtime** | Plain object `{}` | `const { slug } = params` (direct destructuring) |
| **Generated Types** (`.next/types/`) | `Promise<{ ... }>` | `params: Promise<{...}>` + `await` to satisfy tsc |

**For Pages (Updated for Next.js 16.2+)**:
```tsx
// ✅ CORRECT — satisfies both runtime and generated types
interface PageProps {
  params: Promise<{ slug: string }>;
}
export default async function Page({ params }: PageProps) {
  const { slug } = await params; // Required by .next/types/ Promise<T>
}
```

**For Layouts** (always a real Promise):
```tsx
// ✅ CORRECT — layouts always receive a Promise
export default async function Layout({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params; // Always correct for layouts
}
```

**Why the duality**: `.next/types/` generates `Promise<any>` to enable async prop resolution. At runtime, `await` on a non-Promise returns the same value (no runtime bug). TypeScript just needs the `Promise<T>` annotation to pass `tsc --noEmit`.


---

## 22. Verification Commands Cheat Sheet

```bash
# Full verification pipeline
pnpm typecheck && pnpm lint && pnpm test && pnpm build

# Prisma type sync check
cd apps/web && pnpm db:generate && pnpm typecheck

# Tailwind v3 utility scan
grep -rEn 'bg-gradient-to-(r|l|t|b)|outline-none[^-]|flex-shrink-0' src/ packages/ apps/

# Raw hex color scan
grep -rEn 'text-\[#[0-9A-Fa-f]{3,6}\]|bg-\[#[0-9A-Fa-f]{3,6}\]' src/ packages/ apps/

# `getServerSession` / `getToken` usage check
grep -rn 'getServerSession' src/ --include="*.ts" --include="*.tsx"

# `enum` / `namespace` scan
grep -rn 'enum ' src/ packages/ apps/ --include="*.ts" --include="*.tsx"

# next-intl config file scan (should find request.ts, NOT i18n.ts monolith)
grep -rn "createNextIntlPlugin" next.config.ts
```

