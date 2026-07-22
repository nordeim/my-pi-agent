---
name: luxeverse-architect
description: Comprehensive Architectural & Execution Framework for Cinematic, Production-Grade, Anti-Generic Web Platforms
---

# LuxeVerse Architect Skill

## Comprehensive Architectural & Execution Framework for Cinematic, Production-Grade, Anti-Generic Web Platforms

**Version**: 3.3.0
**Date**: 2026-05-20
**Scope**: Phases 0–3 verified (Foundation, Core Commerce, Cinematic Experience, AI Integration)
**New Since v3.2.0**: AI component integration (OutfitCard, SizeRecommendation, StyleChat) into real pages (Account, PDP), `generateOutfit` wired to real product catalog via ProductService, test cleanup for Vitest + jsdom, monorepo lint script fix (exclude build artifacts), RSC-first "Client Island Dashboard" pattern for multi-widget interactive regions
**Source**: Distilled from full Phase 0–1 execution on LuxeVerse v3.0, plus cross-skill synthesis from claude-md, super-frontend-design, react19-ts6-vite8-tailwindv4-mvp, nextjs16-tailwind4, frontend-ui-engineering, clean-code, framework-templates
**Triggers**: `build luxury e-commerce`, `cinematic UI architecture`, `Next.js 16 phased rollout`, `anti-generic design system`, `tRPC Zustand commerce`
**When to Use**: Any project requiring Next.js 16, React 19, TypeScript 6, Tailwind v4, Prisma, tRPC, Zustand, NextAuth v5, or any subset thereof. The phased approach, RSC/Client split, and design system are universally applicable.

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

```
ANALYZE → PLAN → VALIDATE → IMPLEMENT → VERIFY → DELIVER
   ↑______________________________________________↓
              (loop back if verify fails)
```

---

## 2. Complete Architecture Blueprint

### 2.1 Monorepo Structure (Exact)
```
/
├── apps/
│   └── web/                          # Next.js 16 application (RSC-first)
│       ├── app/                      # App Router (RSC default, "use client" for islands)
│       │   ├── globals.css           # Tailwind v4 @theme inline (OKLCH, fluid type, golden ratio)
│       │   ├── layout.tsx            # Root layout: Providers, SkipLink, Navbar, Footer
│       │   ├── page.tsx              # Homepage
│       │   ├── (auth)/               # Auth route group
│       │   │   ├── login/page.tsx
│       │   │   └── register/page.tsx
│       │   ├── shop/
│       │   │   ├── loading.tsx       # ProductGridSkeleton
│       │   │   ├── page.tsx          # PLP (RSC)
│       │   │   └── [category]/[slug]/
│       │   │       └── page.tsx      # PDP (RSC, params as plain object)
│       │   ├── checkout/
│       │   │   └── page.tsx          # Multi-step checkout shell
│       │   └── api/
│       │       └── trpc/
│       │           └── route.ts      # tRPC app handler
│       ├── components/
│       │   ├── layout/
│       │   │   ├── Navbar.tsx        # RSC (no "use client" — scroll via CSS only)
│       │   │   └── Footer.tsx        # RSC
│       │   ├── shared/
│       │   │   ├── SkipLink.tsx      # First child in <body>, focus-visible ring
│       │   │   └── ErrorBoundary.tsx # Client component for error catching
│       │   ├── product/
│       │   │   ├── ProductCard.tsx     # RSC (image + link + price display)
│       │   │   ├── ProductGallery.tsx  # "use client" — interactive carousel
│       │   │   ├── VariantSelector.tsx # "use client" — stateful size/color picker
│       │   │   ├── StickyAddToBar.tsx  # "use client" — IntersectionObserver
│       │   │   ├── QuickAddButton.tsx  # "use client" — optimistic add to cart
│       │   │   ├── PriceDisplay.tsx    # RSC (formatted price)
│       │   │   ├── ProductGridSkeleton.tsx
│       │   │   └── PDPSkeleton.tsx
│       │   ├── cart/
│       │   │   ├── CartDrawer.tsx      # "use client" — focus trap, ESC dismiss
│       │   │   ├── CartItem.tsx        # "use client" — optimistic quantity update
│       │   │   └── FreeShippingProgress.tsx
│       │   ├── auth/
│       │   │   ├── AuthForm.tsx        # "use client" — login/register toggle
│       │   │   └── ProtectedRoute.tsx  # "use client" — guards routes
│       │   └── checkout/
│       │       ├── ShippingStep.tsx   # "use client" — avoid race conditions (see §8)
│       │       ├── PaymentStep.tsx    # "use client" — Stripe PaymentElement
│       │       ├── ReviewStep.tsx     # "use client"
│       │       └── ConfirmationStep.tsx # "use client" — useRouter.push()
│       ├── hooks/
│       │   ├── useFocusTrap.ts        # Zero dependencies
│       │   └── useCart.ts             # Zustand selector hook
│       ├── lib/
│       │   ├── prisma.ts              # Singleton PrismaClient
│       │   ├── schemas.ts             # Zod v4 schemas (flat for FormData)
│       │   ├── auth.ts                # NextAuth v5 config (JWT, roles, bcrypt)
│       │   ├── crypto.ts              # @node-rs/bcrypt wrapper
│       │   └── utils.ts               # cn(), formatCurrency(), etc.
│       ├── server/
│       │   ├── trpc.ts                # createTRPCContext, createCaller
│       │   ├── context.ts             # Context builder (req, res, DB)
│       │   ├── index.ts               # App router
│       │   ├── routers/
│       │   │   ├── product.ts         # getBySlug, listByCategory, search
│       │   │   ├── cart.ts            # get, addItem, removeItem, updateQuantity
│       │   │   └── order.ts           # create, get by id, list for user
│       │   └── services/
│       │       ├── product.service.ts   # Factory: createProductService()
│       │       └── cart.service.ts      # Factory: createCartService(), typed mapCart()
│       ├── stores/
│       │   ├── cart.ts                # Zustand: items[], isOpen, isLoading (partialize items ONLY)
│       │   └── auth.ts                # Zustand: ephemeral (NO persist), tracks auth status
│       ├── types/
│       │   └── index.ts               # UserRole, Product, CartItem, Order, etc. (not enums — unions)
│       ├── test/
│       │   ├── setup.ts               # rAF mock, crypto mock, vi globals
│       │   └── factories.ts           # getMockProduct(), getMockUser()
│       ├── trpc/
│       │   ├── provider.tsx           # TRPCProvider (React Query + tRPC)
│       │   ├── server.ts            # createCaller for RSC
│       │   └── index.ts             # createTRPCReact, utility type exports
│       ├── actions/
│       │   ├── checkout.actions.ts  # useActionState + Zod + Stripe
│       │   └── auth.actions.ts      # useActionState + Zod + bcrypt
│       └── prisma/
│           └── schema.prisma          # ZERO enums, String for status/pricingType/orderStatus
├── packages/
│   ├── config/
│   │   ├── tsconfig/
│   │   │   ├── base.json              # strict, erasableSyntaxOnly, verbatimModuleSyntax
│   │   │   └── next.json              # extends base.json + next-specific
│   │   ├── eslint/
│   │   │   └── base.js                # Flat config: no-any, no-enum, no-namespace, no-console-except-error
│   │   └── tsconfig/package.json      # exports base.json as dependency
│   ├── ui/
│   │   ├── src/
│   │   │   ├── button.tsx             # CVA: default, outline, ghost, luxury
│   │   │   ├── input.tsx              # Label, error state, helperText, ARIA
│   │   │   ├── badge.tsx              # product, status, sustainability variants
│   │   │   ├── avatar.tsx             # Image + initials fallback, square/round
│   │   │   ├── skeleton.tsx           # aria-busy + pulse animation
│   │   │   └── index.ts               # Barrel export
│   │   ├── tsconfig.json              # MUST exist — extends ../config/tsconfig/base.json
│   │   └── package.json               # Side-effect free, shared deps
│   └── utils/
│       ├── src/
│       │   ├── cn.ts                  # clsx + tailwind-merge wrapper
│       │   └── index.ts               # Barrel export
│       └── package.json
├── .github/
│   └── workflows/
│       └── ci.yml                     # typecheck → lint → test → build
├── docs/
│   ├── architecture.md              # Monorepo, RSC/Client, data flow
│   ├── design-tokens.md             # Color, type, spacing, easing
│   ├── runbook.md                   # Commands, common errors, onboarding
│   └── phase-completion.md          # Current phase, checklist, next steps
├── scripts/
│   ├── validate-colors.sh           # Block raw hex in className
│   └── validate-deprecated-twind.sh # Block v3 utilities (bg-gradient-to-*, etc.)
├── turbo.json                       # Pipeline: typecheck → lint → test → build (cached)
├── pnpm-workspace.yaml              # App + packages
└── CLAUDE.md                        # Full project conventions (corollary to this skill)
```

### 2.2 Dependency Matrix (Exact Rationale)
| Technology | Version | Purpose | Why, Not (Bayesian Reasoning) |
|---|---|---|---|
| next | ^16.0.0 | Framework | App Router + RSC + Turbopack + PPR. No Vite — SSR required for SEO + auth. |
| react | ^19.2.0 | UI library | useActionState, useOptimistic, useId. No Vue/Svelte — team React expertise. |
| @types/react | ^19.2.0 | Types | Required even for React 19 (not self-published yet). |
| @types/react-dom | ^19.2.0 | Types | Required even for React 19. |
| typescript | ^6.0.0 | Language | erasableSyntaxOnly, verbatimModuleSyntax, no-inferrable-return. No tsc v5 — v6 has necessary strictness. |
| tailwindcss | ^4.2.0 | Styling | CSS-first @theme inline, Oxide engine, no config file. No v3 — Oxide requires v4. |
| zustand | ^5.0.0 | Client state | Minimal, no boilerplate, persist middleware. No Redux — overkill for this scope. |
| zod | ^4.4.0 | Validation | Runtime validation at boundaries. schemas.ts single source of truth. No Yup — type inference weaker. |
| @trpc/server, @trpc/react-query | ^11.0.0 | API | End-to-end typesafe. No REST — manual TypeScript defense impossible to maintain at this schema size. |
| @auth/prisma-adapter | ^2.0.0 | Auth bridge | Links NextAuth to Prisma schema. |
| next-auth | ^5.0.0 | Authentication | JWT strategy, edge-compatible, role-based. No Auth0 SDK — vendor lock-in, we control schema. |
| @node-rs/bcrypt | ^1.0.0 | Password hashing | Binary (not native) — node_modules install <5s on M1. No bcryptjs — pure JS is 15x slower. |
| stripe | ^17.0.0 | Payments | PaymentElement (PCI SAQ-A). No custom card inputs — violates PCI. |
| vitest | ^4.1.0 | Testing | jsdom, Vite-native config. |
| @testing-library/react | ^16.3.0 | Testing | User-centric component testing. |
| playwright | ^1.51.0 | E2E | Critical flow testing (checkout, auth). |
| turbo | ^2.5.0 | Monorepo | Parallel dev builds, shared cache, task orchestration. |

---

## 3. Phase 0: Foundation & Design System (Exact Execution)

### 3.1 TypeScript Configuration (Non-Negotiable)
```json
// packages/config/tsconfig/base.json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "erasableSyntaxOnly": true,
    "verbatimModuleSyntax": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "esModuleInterop": true
  }
}
```
**`erasableSyntaxOnly: true` — This BANS `enum` and `namespace`. Zero exceptions.**
**`verbatimModuleSyntax: true` — Forces `import type` for type-only imports.**

### 3.2 Tailwind CSS v4 — CSS-First ONLY
```css
/* apps/web/src/app/globals.css */
@import "tailwindcss";

@theme inline {
  --color-obsidian-50: oklch(0.98 0.002 260);
  --color-obsidian-100: oklch(0.95 0.005 260);
  --color-obsidian-200: oklch(0.88 0.008 260);
  --color-obsidian-300: oklch(0.76 0.012 260);
  --color-obsidian-400: oklch(0.64 0.016 260);
  --color-obsidian-500: oklch(0.52 0.020 260);
  --color-obsidian-600: oklch(0.40 0.018 260);
  --color-obsidian-700: oklch(0.30 0.015 260);
  --color-obsidian-800: oklch(0.20 0.010 260);
  --color-obsidian-900: oklch(0.12 0.005 260);
  --color-obsidian-950: oklch(0.08 0.003 260);
  --color-neon-pink: oklch(0.65 0.28 350);
  --color-neon-cyan: oklch(0.85 0.18 190);
  --color-neon-lime: oklch(0.88 0.22 130);
  --color-metallic-gold: oklch(0.78 0.14 85);
  --color-metallic-silver: oklch(0.82 0.02 260);
  --color-metallic-champagne: oklch(0.88 0.06 75);
  --color-atmosphere-deep: oklch(0.15 0.04 280);
  --color-atmosphere-midnight: oklch(0.18 0.03 240);
  --color-error: oklch(0.55 0.22 25);
  --color-error-light: oklch(0.95 0.05 25);
  --color-success: oklch(0.60 0.18 145);
  --color-success-light: oklch(0.95 0.05 145);

  --text-xs: clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem);
  --text-sm: clamp(0.875rem, 0.8rem + 0.375vw, 1rem);
  --text-base: clamp(1rem, 0.9rem + 0.5vw, 1.125rem);
  --text-lg: clamp(1.125rem, 1rem + 0.625vw, 1.25rem);
  --text-xl: clamp(1.25rem, 1.1rem + 0.75vw, 1.5rem);
  --text-2xl: clamp(1.5rem, 1.3rem + 1vw, 2rem);
  --text-3xl: clamp(2rem, 1.7rem + 1.5vw, 3rem);
  --text-4xl: clamp(2.5rem, 2rem + 2.5vw, 4rem);
  --text-hero: clamp(3.5rem, 2.5rem + 5vw, 8rem);

  --font-display: "Cormorant Garamond", Georgia, serif;
  --font-body: "DM Sans", system-ui, sans-serif;
  --font-mono: "JetBrains Mono", monospace;

  --space-3xs: 0.236rem;
  --space-2xs: 0.382rem;
  --space-xs: 0.618rem;
  --space-sm: 1.000rem;
  --space-md: 1.618rem;
  --space-lg: 2.618rem;
  --space-xl: 4.236rem;
  --space-2xl: 6.854rem;

  --ease-out-expo: cubic-bezier(0.19, 1, 0.22, 1);
  --ease-in-out-expo: cubic-bezier(0.87, 0, 0.13, 1);
  --ease-spring: cubic-bezier(0.175, 0.885, 0.32, 1.275);
  --ease-luxe: cubic-bezier(0.25, 0.1, 0.25, 1);
  --ease-dramatic: cubic-bezier(0.77, 0, 0.175, 1);

  --navbar-height: 64px;
}

@layer base {
  html { scroll-behavior: smooth; }
  body {
    font-family: var(--font-body);
    color: var(--color-obsidian-900);
    background-color: var(--color-obsidian-50);
    -webkit-font-smoothing: antialiased;
  }
  h1, h2, h3, h4, h5, h6 { font-family: var(--font-display); }
  :focus-visible {
    outline: 2px solid var(--color-neon-cyan);
    outline-offset: 2px;
  }
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

**Critical Rules Governing This File**:
1. **NO `tailwind.config.js` anywhere.** v4 reads ALL tokens from CSS.
2. **No arbitrary values in className**: `w-[37px]` is BANNED. Add to `--space-*` tokens.
3. **No raw hex in className**: `bg-[#1a1a2e]` is BANNED. Use `bg-obsidian-900`.
4. **v3 utility migrations**:
   - `bg-gradient-to-r` → `bg-linear-to-r`
   - `outline-none` → `outline-hidden`
   - `flex-shrink-0` → `shrink-0`
5. **Prefer `cn()` to raw `className` string assembly** for toggleable state classes.

---

## 4. Phase 1: Core Commerce (Exact Execution)

### 4.1 Prisma Zero-Enum Pattern
```prisma
// apps/web/prisma/schema.prisma
model Product {
  id           String   @id @default(cuid())
  name         String
  slug         String   @unique
  description  String?
  price        Decimal  @db.Decimal(10, 2)
  // ❌ WRONG: enum Genre { ... }
  genre        String   // TypeScript: type Genre = "ROMANCE" | "THRILLER" | "DRAMA"
  // ❌ WRONG: enum ProductStatus { ... }
  status       String   @default("ACTIVE") // "ACTIVE" | "DRAFT" | "ARCHIVED"
  createdAt    DateTime @default(now())
  updatedAt    DateTime @updatedAt
  images       ProductImage[]
  variants     ProductVariant[]
  cartItems    CartItem[]
  orderItems   OrderItem[]
}

model ProductVariant {
  id        String  @id @default(cuid())
  productId String
  name      String
  sku       String  @unique
  price     Decimal @db.Decimal(10, 2)
  product   Product @relation(fields: [productId], references: [id])
  cartItems CartItem[]
}

model CarItem {
  id        String  @id @default(cuid())
  cartId    String
  productId String
  variantId String?
  quantity  Int     @default(1)
  unitPrice Decimal @db.Decimal(10, 2)
  // ...
}

// String, NOT enum, for status
model Order {
  id       String @id @default(cuid())
  status   String @default("PENDING") // "PENDING" | "PROCESSING" | "SHIPPED" | "DELIVERED" | "CANCELLED" | "REFUNDED"
  // ...
}
```
**Rationale**: `erasableSyntaxOnly` rejects `enum`. Prisma enums compile to TypeScript enums, which are erased at compile time but still fail the constraint. Using `String` + union types in TypeScript gives the same runtime safety with `strict` + SAUCE.

### 4.2 Service Factory Pattern (Zero `any`)
```typescript
// server/services/cart.service.ts
import { prisma } from "@/lib/prisma";
import type { Prisma } from "@prisma/client";
import type { CartData, CartItem } from "@/types";

// ✅ Typed Prisma include — NEVER use `any`
type CartWithItems = Prisma.CartGetPayload<{
  include: {
    items: {
      include: {
        product: { select: { name: true; images: { where: { isPrimary: true }; select: { url: true }; take: 1 } } };
        variant: { select: { name: true } };
      };
    };
  };
}>;

// Zero `any` — all Prisma shape fully typed
function mapCart(cart: CartWithItems): CartData {
  const items: CartItem[] = cart.items.map((item) => ({
    id: item.id,
    productId: item.productId,
    productName: item.product.name,
    variantId: item.variantId,
    variantName: item.variant?.name ?? null,
    quantity: item.quantity,
    unitPrice: Number(item.unitPrice),
    totalPrice: Number(item.unitPrice) * item.quantity,
    imageUrl: item.product.images[0]?.url ?? null,
  }));
  return {
    id: cart.id,
    items,
    subtotal: items.reduce((sum, i) => sum + i.totalPrice, 0),
    itemCount: items.reduce((sum, i) => sum + i.quantity, 0),
    currency: "USD",
  };
}

export interface CartService {
  getOrCreate(userId: string | null, sessionId: string): Promise<CartData>;
  addItem(cartId: string, productId: string, variantId: string | null, quantity: number): Promise<CartData>;
  updateItem(itemId: string, quantity: number): Promise<CartData>;
  removeItem(itemId: string): Promise<CartData>;
  clearCart(cartId: string): Promise<CartData>;
}

// Factory — injectable, mockable, testable
export function createCartService(): CartService {
  return {
    async getOrCreate(userId, sessionId) { /* ...prisma... */ },
    async addItem(cartId, productId, variantId, quantity) { /* ...prisma... */ },
    // ...
  };
}
```

### 4.3 Zod v4 Boundary Validation
```typescript
// lib/schemas.ts
import { z } from "zod";

export const loginSchema = z.object({
  email: z.string().min(1, "Email is required.").email("Invalid email format."),
  password: z.string().min(8, "Password must be at least 8 characters."),
});

export const registerSchema = loginSchema.extend({
  name: z.string().min(2, "Name must be at least 2 characters."),
  confirmPassword: z.string().min(8, "Password confirmation is required."),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords do not match.",
  path: ["confirmPassword"],
});

// ✅ Flat schema for flat FormData
export const checkoutSchema = z.object({
  firstName: z.string().min(1, "First name is required."),
  lastName: z.string().min(1, "Last name is required."),
  line1: z.string().min(5, "Address line is required."),
  line2: z.string().optional(),
  city: z.string().min(1, "City is required."),
  state: z.string().min(1, "State is required."),
  postalCode: z.string().min(1, "Postal code is required."),
  country: z.string().min(2, "Country is required."),
  email: z.string().email("Valid email is required."),
  saveAddress: z.boolean().optional(),
  createAccount: z.boolean().optional(),
});
```
**ZOD V4 API**: `result.error.issues[0].message` (not `.errors[0].message` from v3).

### 4.4 Server Actions with `useActionState`
```typescript
// app/actions/checkout.actions.ts
"use server";
import { z } from "zod";
import { checkoutSchema } from "@/lib/schemas";

export interface CheckoutState { status: "initial" | "error" | "success"; message?: string; }

export async function checkoutAction(
  _prev: CheckoutState,
  formData: FormData
): Promise<CheckoutState> {
  const rawData = Object.fromEntries(formData.entries());
  const parsed = checkoutSchema.safeParse(rawData);
  if (!parsed.success) {
    return { status: "error", message: parsed.error.issues[0].message };
  }
  // ... process checkout ...
  return { status: "success" };
}
```

```tsx
// Client component
const [checkoutState, formAction, isPending] = useActionState(checkoutAction, { status: "initial" });

<form action={formAction}>
  <input name="firstName" />
  <button disabled={isPending}>{isPending ? "Processing..." : "Submit"}</button>
  {checkoutState.status === "error" && <p role="alert">{checkoutState.message}</p>}
</form>
```

**Critical**: `Object.fromEntries(formData.entries())` returns flat key-value pairs. If your Zod schema expects `{ address: { firstName: ... } }`, it will ALWAYS fail because FormData is flat.

### 4.5 Zustand — Selector Discipline Is Law
```typescript
// stores/cart.ts
import { create } from "zustand";
import { persist } from "zustand/middleware";

export interface CartItem { /* ... */ }

export interface CartState {
  items: CartItem[];
  isOpen: boolean;
  isLoading: boolean;
  // actions
  addItem: (item: CartItem) => void;
  updateQuantity: (id: string, quantity: number) => void;
  removeItem: (id: string) => void;
}

export const useCartStore = create<CartState>()(
  persist(
    (set, get) => ({
      items: [],
      isOpen: false,
      isLoading: false,
      addItem: (item) => {
        const { items } = get(); // ✅ .getState() OK inside action
        const existing = items.find((i) => i.id === item.id);
        if (existing) {
          set({
            items: items.map((i) =>
              i.id === item.id ? { ...i, quantity: i.quantity + item.quantity } : i
            ),
          });
        } else {
          set({ items: [...items, item] });
        }
      },
      updateQuantity: (id, quantity) => {
        const { items } = get();
        set({ items: items.map((i) => (i.id === id ? { ...i, quantity } : i)) });
      },
      removeItem: (id) => {
        const { items } = get();
        set({ items: items.filter((i) => i.id !== id) });
      },
    }),
    {
      name: "luxeverse-cart",
      // CRITICAL: Persist ONLY domain data. UI state is ephemeral.
      partialize: (state) => ({ items: state.items }),
    }
  )
);

// Use in components — ALWAYS use selector
// ✅ Correct: reactive subscription
const items = useCartStore((s) => s.items);
const addItem = useCartStore((s) => s.addItem);

// ❌ Wrong: no re-renders, stale data
const items = useCartStore.getState().items; // Never in JSX
```

### 4.6 NextAuth v5 with JWT & Role-Based Access
```typescript
// lib/auth.ts
import NextAuth from "next-auth";
import { PrismaAdapter } from "@auth/prisma-adapter";
import CredentialsProvider from "next-auth/providers/credentials";
import { prisma } from "@/lib/prisma";
import { comparePassword } from "@/lib/crypto";
import type { Adapter } from "next-auth/adapters";
import type { Session, User, NextAuthOptions } from "next-auth";

export interface AuthenticatedSession extends Session{
  user: {
    id: string;
    email: string;
    name: string | null;
    image: string | null;
    role: "USER" | "ADMIN";
  };
}

export const authOptions: NextAuthOptions = {
  adapter: PrismaAdapter(prisma) as Adapter,
  session: { strategy: "jwt" },
  providers: [
    CredentialsProvider({
      name: "credentials",
      credentials: {
        email: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) return null;
        const user = await prisma.user.findUnique({
          where: { email: credentials.email },
        });
        if (!user || !user.passwordHash) return null;
        const isValid = await comparePassword(credentials.password as string, user.passwordHash);
        if (!isValid) return null;
        return { id: user.id, email: user.email, name: user.name, role: user.role };
      },
    }),
  ],
  callbacks: {
    async jwt({ token, user }) {
      if (user) { token.role = user.role; }
      return token;
    },
    async session({ session, token }) {
      if (session.user && token.role) {
        (session.user as AuthenticatedSession["user"]).role = token.role as "USER" | "ADMIN";
      }
      return session;
    },
  },
  pages: { signIn: "/login", error: "/login" },
};

export const { handlers, auth } = NextAuth(authOptions);
```

### 4.7 tRPC with React Query Provider
```typescript
// lib/server/trpc.ts
import { initTRPC } from "@trpc/server";
import type { NextRequest } from "next/server";
import { createContext } from "./context";

const t = initTRPC.create();

export const router = t.router;
export const publicProcedure = t.procedure;
export const protectedProcedure = t.procedure.use(t.middleware(({ ctx, next }) => {
  if (!ctx.session) throw new Error("UNAUTHORIZED");
  return next({ ctx: { ...ctx, session: ctx.session } });
}));

// app/api/trpc/route.ts
import { fetchRequestHandler } from "@trpc/server/adapters/fetch";
import { appRouter } from "@/server/routers";

export async function GET(req: NextRequest) {
  return fetchRequestHandler({ req, router: appRouter, createContext: () => createContext(req) });
}
export async function POST(req: NextRequest) { /* same */ }

// trpc/provider.tsx
"use client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { httpBatchLink } from "@trpc/react-query";
import { useState } from "react";
import { trpc } from "./index";

export function TRPCProvider({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient());
  const [trpcClient] = useState(() =>
    trpc.createClient({ links: [httpBatchLink({ url: "/api/trpc" })] })
  );
  return (
    <trpc.Provider client={trpcClient} queryClient={queryClient}>
      <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
    </trpc.Provider>
  );
}
```

### 4.8 Middleware — Auth, CSP, HSTS, Rate Limiting, Nonce
```typescript
// middleware.ts
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const RATE_LIMIT = new Map<string, { count: number; resetAt: number }>();
const RATE_LIMIT_MAX = 30; // per minute per IP

function getClientIP(req: NextRequest): string {
  return req.headers.get("x-forwarded-for")?.split(",")[0]?.trim() ?? "127.0.0.1";
}

function generateNonce(): string {
  return crypto.randomUUID();
}

export async function middleware(req: NextRequest) {
  const nonce = generateNonce();
  const ip = getClientIP(req);
  const now = Date.now();
  const entry = RATE_LIMIT.get(ip);

  if (!entry || now > entry.resetAt) {
    RATE_LIMIT.set(ip, { count: 1, resetAt: now + 60_000 });
  } else if (entry.count >= RATE_LIMIT_MAX) {
    return NextResponse.json({ error: "Too many requests" }, { status: 429 });
  } else {
    entry.count++;
  }

  const response = NextResponse.next();

  // CSP with nonce
  response.headers.set("Content-Security-Policy",
    `default-src 'self'; script-src 'nonce-${nonce}' 'self'; style-src 'nonce-${nonce}' 'self' 'unsafe-inline'; frame-ancestors 'none';`);
  response.headers.set("Strict-Transport-Security", "max-age=63072000; includeSubDomains; preload");
  response.headers.set("X-Frame-Options", "DENY");
  response.headers.set("X-Content-Type-Options", "nosniff");
  response.headers.set("Referrer-Policy", "strict-origin-when-cross-origin");

  return response;
}

export const config = { matcher: ["/((?!_next|api|static|.*\\.).*)", "/api/:path*"] };
```

---

## 5. The 15 Critical Agent Mistakes (Field-Tested Fixes)

### Mistake #1: `any` in Service Layer
**Fix**: See §4.2. Use `Prisma.CartGetPayload<IncludeShape>`.

### Mistake #2: `document.getElementById` / `window.scrollTo` in RSC
**Fix**: Wrap in Client Component or use native CSS `scroll-behavior: smooth`.

### Mistake #3: Stripe `elements.on("ready")` Null Deref
**Fix**: Use `onReady` prop only. Never both.
```tsx
// ❌ WRONG: elements can be null initially
const handleReady = () => setIsReady(true);
// ❌ WRONG
if (elements) elements.on("ready", handleReady);
// ✅ CORRECT: onReady prop is safe
<PaymentElement onReady={() => setIsReady(true)} />
```

### Mistake #4: `ShippingStep` Race Condition
**Fix**: `useEffect` watches state, not synchronous check after action.
```tsx
// ❌ WRONG
if (state.status !== "error") onNext();
// ✅ CORRECT
useEffect(() => { if (state.status === "success") onNext(); }, [state.status, onNext]);
```

### Mistake #5: Checkout Schema Doesn't Match FormData
**Fix**: Flat schema matching flat FormData keys exactly. See §4.3.

### Mistake #6: `<a href>` for Internal Navigation
**Fix**: `import Link from "next/link"`. `<Link href="/shop">` for all internal routing.

### Mistake #7: `window.location.href` in Next.js
**Fix**: `import { useRouter } from "next/navigation"; router.push("/path")`.

### Mistake #8: `useOptimistic` Type Mismatch
**Fix**: Match state type exactly. `useOptimistic(false, () => true)` → update with `true` not `null`.

### Mistake #9: Tailwind v3 Utilities in v4 Project
**Fix**: `bg-gradient-to-r` → `bg-linear-to-r`, `outline-none` → `outline-hidden`, `flex-shrink-0` → `shrink-0`.

### Mistake #10: `enum` or `namespace` in TypeScript
**Fix**: `type Status = "ACTIVE" | "DRAFT"`. `erasableSyntaxOnly` rejects these.

### Mistake #11: `.getState()` in JSX
**Fix**: Always use selector: `useCartStore((s) => s.items)`. `.getState()` only inside store actions.

### Mistake #12: Persisting UI State in Zustand
**Fix**: `partialize: (state) => ({ items: state.items })` — data only, never `isOpen`/`isLoading`.

### Mistake #13: Using `<button>` Without `type="button"`
**Fix**: Default is `submit`. Always add `type="button"` for non-form buttons.

### Mistake #14: Forgetting `useCallback` for Stable Props
**Fix**: Wrap event handlers and callbacks in `useCallback` to prevent unnecessary re-renders of child components. Especially critical for `onClick`, `onSubmit`, `onChange` passed to memoized children.

### Mistake #15: Ignoring `useId()` for ARIA Pairs
**Fix**: `const id = useId();` then `<label htmlFor={id}>` + `<input id={id} />`. Never hardcode IDs in reusable components.

### Mistake #16: `await params` in Next.js 16 App Router
**Fix**: `params` is a **plain object** in Next.js 16, NOT a Promise. Direct destructuring only.
```tsx
// ❌ WRONG (Next.js 16)
export default async function Page({ params }: Props) {
  const { slug } = await params; // ❌ params is NOT a Promise
  // ...
}

// ✅ CORRECT
export default function Page({ params }: Props) {
  const { slug } = params; // ✅ Direct destructuring
  // ...
}
```
**Why**: Next.js 16 App Router changed `params` from a resolved Promise to a plain object at runtime. `await` on a plain object throws no error but is semantically wrong and can cause subtle hydration mismatches.

### Mistake #17: `JSX.Element` Return Type in React 19
**Fix**: Remove explicit `: JSX.Element` / `: ReactElement` return types entirely. TypeScript infers them.
```tsx
// ❌ WRONG (React 19)
export function HeroSection(): JSX.Element { ... }

// ✅ CORRECT (inferred return type)
export function HeroSection() { ... }
```
**Why**: React 19 removed the global `JSX` namespace. Explicit `JSX.Element` triggers `TS2307: Cannot find namespace 'JSX'`. If you absolutely need an explicit type, use `import type { ReactElement } from "react"`, but inferred is preferred.

### Mistake #18: `useOptimistic` for Simple Boolean Toggles
**Fix**: Use `useState` instead. `useOptimistic` is for complex state where you need a separate "optimistic" branch from the server-confirmed branch.
```tsx
// ❌ WRONG — overcomplicated for a simple toggle
const [optimisticAdded, setOptimisticAdded] = useOptimistic(false, () => true);
setOptimisticAdded(null); // ❌ Type error: null !== boolean

// ✅ CORRECT
const [isAdded, setIsAdded] = useState(false);
setIsAdded(true);
```
**When to use `useOptimistic`**: Multi-step forms, cart quantity updates, message sending — where the server response will eventually confirm/reject the optimistic state. NOT for simple boolean toggles.

### Mistake #19: Emojis in UI
**Fix**: Replace ALL emojis with Lucide icons (or custom SVGs).
```tsx
// ❌ WRONG (emoji)
<button>📷</button>

// ✅ CORRECT (Lucide)
import { Camera } from "lucide-react";
<button><Camera className="h-5 w-5" /></button>
```
**Why**: Emojis render inconsistently across platforms, break accessibility (screen readers may read them as "camera with flash" or not at all), and violate the anti-generic mandate.

### Mistake #20: `async` / `Promise<>` on Components Without Data Fetch
**Fix**: Remove `async` and return type when a component only renders static/mock data.
```tsx
// ❌ WRONG — async without any await inside
export async function FeaturedCollections(): Promise<JSX.Element> { ... }

// ✅ CORRECT
export function FeaturedCollections() { ... }
```
**Why**: Marking a component `async` when it doesn't fetch data is misleading to other developers and can cause subtle TypeScript errors. Only use `async` when you truly `await` a server-side fetch.

### Mistake #21: `window.location.href` for Internal Navigation in Client Islands
**Fix**: Use `useRouter().push()` from `next/navigation` for all internal navigation.
```tsx
// ❌ WRONG (full page reload!)
window.location.href = `/search?q=${query}`;

// ✅ CORRECT (SPA navigation)
const router = useRouter();
router.push(`/search?q=${query}`);
```
**Why**: `window.location.href` causes a full page reload, losing all client-side state (Zustand, React Query, scroll position). `useRouter().push()` preserves the SPA experience.

### Mistake #22: `notFound()` Import When Building Static Pages Without DB
**Fix**: If a page calls Prisma during build time (static generation) and the DB isn't available, the build will crash. Either:
1. Add `export const dynamic = "force-dynamic"` to skip static generation, OR
2. Provide mock data fallback in the component.
```tsx
// ✅ Option 1: Force dynamic (server-rendered on demand)
export const dynamic = "force-dynamic";

// ✅ Option 2: Try/catch with mock fallback
async function SearchResults() {
  let products;
  try {
    products = await createProductService().list({ limit: 12 });
  } catch {
    products = MOCK_PRODUCTS; // Fallback for static builds
  }
  // ...
}
```

### Mistake #23: Missing `@types/three` for R3F Components
**Fix**: Install `@types/three` as a dev dependency when using `@react-three/fiber` and `@react-three/drei`.
```bash
pnpm add -D @types/three
```
**Why**: `@react-three/fiber` and `@react-three/drei` use Three.js types internally. Without `@types/three`, TypeScript will fail with `Cannot find module 'three' or its corresponding type declarations`.

### Mistake #24: Assuming `prisma generate` is Automatic After Schema Changes
**Fix**: Always run `prisma generate` (or `pnpm db:generate`) immediately after modifying `prisma/schema.prisma`.
**Why**: Prisma Client types are code-generated from the schema. If the schema changes but the types aren't regenerated, TypeScript will fail with `TS2339: Property 'X' does not exist on type 'Y'`. The Prisma Client package in `node_modules` is stale.
**Symptoms**:
```
error TS2339: Property 'password' does not exist on type '{ ... }'.
error TS2322: Property 'totalPrice' is missing in type '{ ... }'.
```
**Prevention**:
```bash
# Add this precommit hook or alias
alias pgg="cd apps/web && pnpm db:generate && cd ../.."
```

### Mistake #25: Forgetting to Update `prisma.model.create()` Calls After Schema Changes
**Fix**: When adding a new required field to a Prisma model, every `prisma.model.create()` in the codebase must be updated to include that field. Run `tsc --noEmit` to find all occurrences.
**Why**: Prisma makes new required fields non-optional at the TypeScript level. A model with a new `totalPrice Decimal @db.Decimal(10, 2)` field will fail at `prisma.cartItem.create({ data: { ... } })` unless `totalPrice` is provided.
**Example**:
```ts
// After adding 'totalPrice' to CartItem model:
await prisma.cartItem.create({
  data: {
    cartId, productId, variantId, quantity, unitPrice,
    // ❌ Missing 'totalPrice' - TS2322
  }
});

// ✅ Correct:
await prisma.cartItem.create({
  data: {
    cartId, productId, variantId, quantity, unitPrice,
    totalPrice: Number(unitPrice) * quantity,
  }
});
```
**Prevention**: Add a CI step that runs `pnpm typecheck` before any migration or build step. This catches type mismatches between code and schema before they reach production.

### Mistake #26: Treating `trending` or `rating` as Standard Prisma Fields Without Schema Verification
**Fix**: Before using Prisma aggregations like `viewCount`, `rating`, or `trending`, verify the field exists in `schema.prisma`.
**Why**: These are often business-logic fields that sound like schema fields but may not be implemented yet. If `viewCount` is not in the schema, `prisma.product.findMany({ orderBy: { viewCount: "desc" } })` will throw a runtime error: "Unknown field `viewCount`".
**Prevention**: When implementing a feature that relies on schema fields, always check the schema first. Don't assume a common-sounding field like `rating` or `viewCount` exists just because the product domain implies it.

### Mistake #27: Using Raw `<a>` Tags for Internal Navigation
**Fix**: Always use Next.js `<Link>` for internal app navigation.
```tsx
// ❌ WRONG - Triggers full page reload
<a href="/shop">Shop</a>

// ✅ CORRECT - Client-side navigation with prefetch
import Link from "next/link";
<Link href="/shop">Shop</Link>
```
**Why**: Raw `<a>` tags bypass the Next.js router, causing a full page reload. This destroys client-side state (Zustand stores, React Query cache, scroll position) and negates the SPA benefits. Use `<Link>` for all internal navigation and `<a>` only for external URLs.

### Mistake #28: Assuming a Component Exists Just Because It's Documented
**Fix**: Always verify component existence with `ls` or `glob` before claiming a component is "missing."
**Why**: Documentation like `phase-2_gap_analysis.md` may claim 34 files are missing when in fact most of them exist. The gap between docs and code is real. Verify before planning remediation.
**Verification Command**:
```bash
glob "src/components/**/*.tsx"
glob "src/hooks/*.ts"
glob "src/stores/*.ts"
```

### Mistake #29: Using `z-[400]` or Arbitrary `z-index` Values in Tailwind v4
**Fix**: Use Tailwind v4's `z-<number>` tokens. If `z-[400]` is needed, add `--z-400: 400` to `@theme inline`.
**Why**: Arbitrary values in brackets are harder to manage and may be accidentally overridden. Using tokens ensures a single source of truth for z-index values.
**Example**:
```css
@theme inline {
  --z-overlay: 400;
  --z-modal: 500;
}
```
```tsx
<div className="z-overlay">...</div>
```

---

## 6. Component Architecture (RSC-First, Client Islands)

### The "Islands" Model
Next.js App Router renders Server Components by default. Client Components are opt-in islands.

**Server Component (default)**:
- Fetch data directly: `const products = await prisma.product.findMany();`
- Generate metadata: `export async function generateMetadata() { ... }`
- Access Node.js APIs: `fs`, `path`, `crypto` (server-side)
- **Cannot**: `useState`, `useEffect`, `useRef`, browser APIs (`window`, `document`, `localStorage`)

**Client Component (`"use client"`)**:
- All React hooks: `useState`, `useEffect`, `useId`, `useCallback`, `useMemo`
- All browser APIs: `IntersectionObserver`, `ResizeObserver`, `fetch` (use `useSWR` or tRPC instead)
- Zustand, tRPC React Query, Formik, React Hook Form
- **Cannot**: `async function`, data fetching at module level, `generateMetadata`

### The Pattern
```tsx
// app/shop/page.tsx — RSC, fetches data
import { ProductGrid } from "@/components/product/ProductGrid";
import { prisma } from "@/lib/prisma";
export default async function ShopPage() {
  const products = await prisma.product.findMany({ where: { status: "ACTIVE" } });
  return <ProductGrid products={products} />;
}

// components/product/ProductGrid.tsx — RSC, renders data
export function ProductGrid({ products }: ProductGridProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6">
      {products.map((product) => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  );
}

// components/product/ProductCard.tsx — RSC, link to PDP
import Link from "next/link";
export function ProductCard({ product }: ProductCardProps) {
  return (
    <Link href={`/shop/${product.category}/${product.slug}`} className="group">
      <ProductImage src={product.images[0]?.url} alt={product.name} />
      <h3 className="font-display">{product.name}</h3>
      <PriceDisplay price={product.price} />
    </Link>
  );
}

// components/product/QuickAddButton.tsx — Client Component
"use client";
export function QuickAddButton({ productId, variantId }: QuickAddButtonProps) {
  const [isAdding, setIsAdding] = useState(false);
  const addToCart = useCartStore((s) => s.addItem);

  const handleClick = useCallback(async () => {
    setIsAdding(true);
    try {
      await addToCart({ productId, variantId, quantity: 1 });
    } finally {
      setIsAdding(false);
    }
  }, [productId, variantId, addToCart]);

  return (
    <button type="button" onClick={handleClick} disabled={isAdding}>
      {isAdding ? "Adding..." : "Quick Add"}
    </button>
  );
}
```

---

## 7. Testing & QA

### Vitest Setup
```typescript
// src/test/setup.ts
import "@testing-library/jest-dom/vitest";
import { vi, beforeEach, afterEach } from "vitest";

beforeEach(() => {
  vi.useFakeTimers({ shouldAdvanceTime: true });
  vi.stubGlobal("requestAnimationFrame", (cb: FrameRequestCallback) => {
    return window.setTimeout(cb, 16) as unknown as number;
  });
  vi.stubGlobal("cancelAnimationFrame", (id: number) => {
    window.clearTimeout(id);
  });
  Object.defineProperty(window, "crypto", {
    value: { randomUUID: () => "test-uuid-" + Math.random().toString(36).slice(2) },
  });
});

afterEach(() => {
  vi.unstubAllGlobals();
  vi.useRealTimers();
});
```

### Factory Mocks
```typescript
// src/test/factories.ts
import type { Product, User } from "@/types";

export function getMockProduct(overrides?: Partial<Product>): Product {
  return {
    id: "prod-" + crypto.randomUUID(),
    name: "Test Product",
    slug: "test-product",
    price: 10000,
    images: [],
    category: "APPAREL",
    status: "ACTIVE",
    ...overrides,
  };
}

export function getMockUser(overrides?: Partial<User>): User {
  return {
    id: "user-" + crypto.randomUUID(),
    email: "test@example.com",
    name: "Test User",
    role: "USER",
    ...overrides,
  };
}
```

### Key Testing Rules
- **Mock services, not implementation**: `vi.mock("@/server/services/cart.service")` not `vi.spyOn(prisma, "findMany")`.
- **Test behavior, not structure**: `expect(screen.getByText("Quick Add")).toBeInTheDocument()` not `expect(container.querySelector("button")).toHaveClass("...")`.
- **Factory pattern**: `getMockProduct({ name: "Custom" })` for deterministic, isolated tests.
- **Never skip tests**: Zero `test.skip` or `describe.skip` in committed code.

---

## 8. CI/CD & Quality Gates

### GitHub Actions Pipeline
```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - run: pnpm typecheck   # tsc --noEmit — must pass zero errors
      - run: pnpm lint        # Next.js lint + Prettier
      - run: pnpm test        # Vitest — must pass zero failures
      - run: pnpm build       # Production build — must succeed
      - run: npm audit --audit-level moderate  # Zero high/critical
      # Optional: Lighthouse CI
      # - run: npx lhci autorun
```

### Pre-Commit Checklist (Run Before Every Commit)
| # | Check | Command |
|---|---|---|
| 1 | TypeScript zero errors | `pnpm typecheck` |
| 2 | ESLint with Prettier | `pnpm lint` |
| 3 | Tests pass | `pnpm test` |
| 4 | Build succeeds | `pnpm build` |
| 5 | No `any`, `enum`, `namespace` | `grep -rn "enum\\|namespace\\|: any" src/` |
| 6 | No `tailwind.config.js` | `find . -name "tailwind.config.*"` |
| 7 | No v3 utilities | `grep -rn "bg-gradient-to-\\|outline-none\\b\\|flex-shrink-0" src/` |
| 8 | No raw hex in className | `grep -rn "#[0-9A-Fa-f]\\{3,6\\}" src/ --include="*.tsx"` |
| 9 | No emojis | `grep -rn "[😀-🿿]" src/` |
| 10 | All internal nav uses `<Link>` | `grep "<a " src/ -rl | xargs grep 'href="/'` |
| 11 | No `document`/`window` in RSC | `grep "window\\.,document\\." src/ --include="*.tsx"` |

### Shell Validation Scripts
```bash
# scripts/validate-colors.sh
#!/bin/bash
echo "Checking for raw hex in className..."
grep -rn "#[0-9A-Fa-f]\{3,6\}" src/ --include="*.tsx" && echo "❌ Found raw hex. Use design tokens." || echo "✅ No raw hex."

# scripts/validate-deprecated-twind.sh
#!/bin/bash
echo "Checking for deprecated Tailwind v3 utilities..."
grep -rn "bg-gradient-to-\|outline-none\b\|flex-shrink-0" src/ && echo "❌ Found deprecated utilities." || echo "✅ Clean."
```

---

## 9. Design System & Anti-Generic Mandate

### Color Palette (OKLCH — Perceptually Uniform)
| Token | OKLCH Value | Usage |
|-------|-------------|-------|
| `obsidian-50` | `oklch(0.98 0.002 260)` | Lightest background |
| `obsidian-900` | `oklch(0.12 0.005 260)` | Primary text |
| `obsidian-950` | `oklch(0.08 0.003 260)` | Button/dark surfaces |
| `neon-cyan` | `oklch(0.85 0.18 190)` | Focus indicators |
| `neon-pink` | `oklch(0.65 0.28 350)` | Errors/callouts |
| `metallic-champagne` | `oklch(0.88 0.06 75)` | Primary CTAs |
| `metallic-gold` | `oklch(0.78 0.14 85)` | Hover states |

### Typography (Fluid Scale)
```
hero:  clamp(3.5rem, 2.5rem + 5vw, 8rem)  — Page hero
h1:    clamp(2.5rem, 2rem + 2.5vw, 4rem)   — Page titles
h2:    clamp(2rem, 1.7rem + 1.5vw, 3rem)    — Section headers
h3:    clamp(1.5rem, 1.3rem + 1vw, 2rem)    — Card titles
body:  clamp(1rem, 0.9rem + 0.5vw, 1.125rem)
small: clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem)
```

### Spacing (Golden Ratio)
```
--space-3xs: 0.236rem
--space-2xs: 0.382rem
--space-xs:  0.618rem
--space-sm:  1.000rem
--space-md:  1.618rem
--space-lg:  2.618rem
--space-xl:  4.236rem
--space-2xl: 6.854rem
```

---

## 10. Troubleshooting Encyclopedia

### Zod v4 API Changes
**Error**: `zodErrors.map is not a function`
**Root**: Zod v4 changed the error structure.
**Fix**: Use `result.error.issues[0].message` instead of `result.error.errors[0].message`.

### Tailwind v4: `No config file found`
**Root**: `tailwind.config.js` exists but v4 doesn't read it.
**Fix**: Delete `tailwind.config.js` and move all tokens to `globals.css` using `@theme inline`.

### NextAuth v4 ❌ → v5 ✅
**Migrating to Auth.js (NextAuth v5) from v4**
**Critical Differences**:
1. **Environment variables**: `NEXTAUTH_SECRET` → `AUTH_SECRET`, `NEXTAUTH_URL` → `AUTH_TRUST_HOST` (or remove `NEXTAUTH_URL` if using `trustHost: true`).
2. **Imports**: `import NextAuth from "next-auth"` → `import NextAuth from "next-auth"` is the same, but the return is different. In v5, `NextAuth()` doesn't export `GET`/`POST` directly in the same way.
3. **API Route**: In v5, auth is mounted differently. The `api/auth/[...nextauth]/route.ts` is handled automatically by the framework, and you don't manually create it for App Router.
4. **Session**: `getServerSession` is deprecated in favor of `auth()` from `next-auth`.
5. **Config**: The `authOptions` structure is different. In v5, you define a `config` and pass it to `NextAuth`.

### Next.js 16: `params` is a Plain Object (Not a Promise)
**Error**: `await params` compiles but produces undefined at runtime,or causes hydration mismatches.
**Fix**: Directly destructure `params` without `await`.
```tsx
// ❌ WRONG
export default async function Page({ params }: { params: { slug: string } }) {
  const { slug } = await params;
}

// ✅ CORRECT
export default function Page({ params }: { params: { slug: string } }) {
  const { slug } = params;
}
```
**See**: Mistake #16 for full explanation.

### Next.js 16: `searchParams` is NOT a Promise
**Error**: Treating `searchParams` as a Promise in `page.tsx` props.
**Fix**: `searchParams` is a read-only plain object. Do not `await` it.
```tsx
// ❌ WRONG
export default async function Page({ searchParams }: Props) {
  const resolved = await searchParams; // ❌ No! searchParams is already resolved
}

// ✅ CORRECT
export default function Page({ searchParams }: { searchParams: { [key: string]: string | string[] | undefined } }) {
  const query = searchParams.q ?? "";
}
```

### Next.js 16: `experimental.ppr` Merged into `cacheComponents`
**Error**: `experimental.ppr: "incremental"` causes build failure.
**Fix**: In Next.js 16+, `experimental.ppr` has been merged into `cacheComponents`. Remove `ppr` from `next.config.ts`.
```ts
// ❌ WRONG (Next.js 16+)
const nextConfig = {
  experimental: { ppr: "incremental" } // ❌ Removed in v16
};

// ✅ CORRECT
const nextConfig = {
  // Remove `ppr` entirely — the feature is now enabled by default
  // via `cacheComponents` behavior
};
```
**Next.js Lint Deprecated in Config**: v16 removed `eslint` key from `next.config.ts`. Remove:
```ts
// ❌ WRONG (Next.js 16+)
eslint: { ignoreDuringBuilds: false },

// ✅ CORRECT — configure eslint separately
```
**Note**: The `eslint` configuration is now in `.eslintrc.*` or `eslint.config.mjs` only. The `next.config.ts` key is unrecognized and causes a warning at build time.

### React 19: `Cannot find namespace 'JSX'`
**Root**: React 19 removed the global `JSX` namespace.
**Fix 1**: Import types for ReactElement: `import type { ReactElement } from "react"`.
**Fix 2**: Prefer inferred return types over explicit `JSX.Element` / `React.ReactElement` for simple components.

### TypeScript `noUnusedLocals` / `noUnusedParameters`
**Issue**: `error TS6133: 'X' is declared but its value is never read.`
**Root**: Strict TypeScript settings. The `_` prefix convention used by some linters does NOT suppress TypeScript's `noUnusedLocals` or `noUnusedParameters` errors.
**Fix**:
1. **Remove the variable/parameter entirely** (if truly not needed).
2. **Use the variable** (e.g., `_input.amount` instead of ignoring it).
3. **Rename to `_[name]`**: While not suppressing the compiler, it indicates intent. However, the compiler may still flag it depending on the exact configuration. The standard approach is to either use it or remove it.
4. **Don't disable**: Keep `noUnusedLocals: true` and `noUnusedParameters: true` in `tsconfig.json` — they catch real bugs. Only disable if you are in a quick prototype and willing to pay the tech debt later.

### Monorepo: `Cannot find module '@luxeverse/utils'`
**Root**: Workspace dependency is linked, but TypeScript can't resolve its types.
**Fix 1**: Ensure `packages/utils/tsconfig.json` exists and has `"compilerOptions"` set up for declaration generation if needed.
**Fix 2**: In `packages/utils/package.json`, make sure `main` and `types` point to the built files or source files.
**Fix 3**: In root `tsconfig.json`, add the workspace to `references` or ensure `baseUrl` + `paths` are configured.
**Fix 4**: If the package has no build step, point `main` to the source: `"main": "./src/index.ts"` and `"types": "./src/index.ts"`.

### `window` / `document` in RSC
**Error**: `ReferenceError: window is not defined`
**Fix 1**: Add `"use client"` to the top of the file.
**Fix 2**: If it's just a small logical check (not an API call), replace with:
```tsx
if (typeof window !== "undefined") { ... }
```

### Stripe `onReady` vs `elements.on("ready")`
**Error**: `Cannot read properties of undefined (reading 'on')` or Null Deref.
**Fix**: Stripe's `PaymentElement` has an `onReady` prop. Use that instead of `elements.on("ready")` which can fail during initial render. If using `useStripe()` + `useElements()`, the `elements` object might not be ready when the hook first runs.

---

## 11. Environment Variables

| Variable | Purpose | Example |
|---|---|---|
| `DATABASE_URL` | Prisma/PostgreSQL | `postgresql://localhost:5432/luxeverse` |
| `NEXTAUTH_SECRET` | JWT signing | `a-256-bit-secret-key` |
| `NEXTAUTH_URL` | Auth callbacks | `http://localhost:3000` |
| `STRIPE_SECRET_KEY` | Server-side Stripe | `sk_test_...` |
| `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` | Client-side Stripe | `pk_test_...` |
| `AUTH_SECRET` | NextAuth v5 | `a-256-bit-secret-key` |
| `REDIS_URL` | Production cache | `redis://localhost:6379` |

---

## 12. Lessons Learned (Phase 0–1 Deep Dive)

### Phase 0
1. **Tailwind v4 CSS-first is non-negotiable**: `tailwind.config.js` causes Oxide engine failure. All tokens in `@theme inline`.
2. **RSC/Client boundaries must be declared**: Every interactive component needs `"use client"`. Server Components cannot use `document`, `window`, or `localStorage`.
3. **Zustand `partialize` is a foot-gun**: `isOpen`, `isLoading`, `toasts` must NOT be persisted. Only domain data.
4. **Focus rings are non-negotiable**: `outline: 2px solid var(--color-neon-cyan)` with 2px offset.
5. **Lucide icons only**: No emojis. No inline SVGs without `aria-hidden`.

### Phase 2 (Cinematic Experience & Advanced Discovery)
17. **`params` / `searchParams` are NOT Promises in Next.js 16**: Direct destructuring only. `await params` is a silent bug that compiles but causes runtime failures.
18. **`JSX.Element` is BANNED in React 19**: Remove all explicit `: JSX.Element` return types. TypeScript infers them. If you must be explicit, use `ReactElement` (imported).
19. **`useOptimistic` is NOT for simple boolean toggles**: React 19 `useOptimistic` requires `(state, optimisticValue)` reducer signature. For simple toggles, `useState` is simpler and safer.
20. **No emojis in UI, ever**: Use Lucide icons exclusively. Emojis break a11y and violate the anti-generic mandate.
21. **`async` on components without data fetch is misleading**: If a component only renders mock/static data, removing `async` prevents TypeScript errors and confusion.
22. **`useRouter().push()` replaces ALL `window.location.href`**: In Client Islands, ALL internal navigation must use `useRouter().push()`. Never `window.location.href`.
23. **Static builds crash when Prisma pages lack DB**: Add `export const dynamic = "force-dynamic"` to all pages that call Prisma during static generation. Or provide a mock data fallback in try/catch.
24. **`@types/three` is REQUIRED for R3F**: When using `@react-three/fiber` and `@react-three/drei`, install `@types/three` as a dev dependency.
25. **`useReducedMotion` from Framer Motion is the source of truth**: Check `useReducedMotion()` at the component level for all animated elements. Do NOT rely solely on CSS `@media (prefers-reduced-motion: reduce)` for JS-driven animations.
26. **`"use client"` must be the VERY FIRST LINE in the file**: Even before `import type`. Any expression before the directive invalidates it.
27. **`next/image` must have explicit `width` and `height`** (or `fill`): Omitting dimensions causes CLS (Cumulative Layout Shift) and TypeScript errors in Next.js 16.
28. **`next/dynamic` with `ssr: false` for Three.js/WebGL**: R3F + Drei must be dynamically imported with `{ ssr: false, loading: <Skeleton /> }`. Never import them directly in a page that is statically rendered.
29. **`startTransition` wraps all URL state mutations**: When updating `searchParams` from Client Islands, wrap the mutation in `startTransition()` to prevent UI blocking.
30. **`skipLibCheck: true` is MANDATORY for R3F + Framer Motion**: Both libraries have complex internal types that can conflict with strict TS settings. Do NOT remove `skipLibCheck`.

### Phase 1
1. **Never persist UI state in Zustand**: `partialize: (state) => ({ items: state.items })` only.
2. **Zod v4 `.issues[0].message` not `.errors[0]`**: API changed between v3 and v4.
3. **Flat `checkoutSchema` for flat `FormData`**: Match `name` attribute to schema key exactly.
4. **Stripe `PaymentElement` uses `onReady` prop**: `elements.on("ready")` can null-deref.
5. **ShippingStep race**: `useEffect` watches state transition, never synchronous `if (state.status !== "error")`.
6. **Always use `<Link>` for internal nav**: `<a href="/shop">` triggers full page reload.
7. **Always use `useRouter().push()` not `window.location.href`**: Preserves SPA state.
8. **Service factories not singletons**: `createCartService()` for testability.
9. **`params` is plain object in Next.js 16**: No `await params`. Direct destructuring.
10. **TypeScript `paths` are compile-time only**: Vite/Next.js config must also define runtime aliases.
11. **`useCallback` for stable props passed to memoized children**: Prevents re-render cascades.
12. **`useId()` for all ARIA pairs**: Never hardcode IDs in reusable components.
13. **`noUnusedLocals` catches dead code early**: Disabled underscore prefix convention — TypeScript ignores `_` prefixes by default in modern versions, but `noUnusedLocals` still catches them. Remove or use the variable.
14. **`React.ReactElement` / `ReactElement` vs `JSX.Element`**: React 19 removed the global `JSX` namespace. Always `import type { ReactElement } from 'react'` and use `ReactElement`.
15. **Prisma types after schema change**: Run `pnpm db:generate` to update types before `tsc --noEmit`.
16. **Workspace packages need explicit build/export**: Returning `PaymentIntentResult` from `createPaymentService` requires the interface to be exported. If `payment.service.ts` adds a new export, update `index.ts` or `package.json` exports map.

---

## 13. Quick Reference Card

### TypeScript
```
❌ enum, namespace                     → ✅ union type
❌ function(x: any)                   → ✅ function(x: unknown)
❌ import { UIState } from '...'       → ✅ import type { UIState } from '...'
❌ : Props (generic names)              → ✅ interface ProductCardProps
```

### Tailwind v4
```
❌ tailwind.config.js                   → ✅ @theme inline in globals.css
❌ bg-gradient-to-r                    → ✅ bg-linear-to-r
❌ outline-none                        → ✅ outline-hidden
❌ flex-shrink-0                       → ✅ shrink-0
❌ w-[37px]                            → ✅ extend @theme inline
❌ bg-[#1a1a2e]                        → ✅ bg-obsidian-900
```

### Zustand
```
❌ useCartStore.getState().items       → ✅ useCartStore((s) => s.items)
❌ partialize: (s) => s               → ✅ partialize: (s) => ({ items: s.items })
```

### Next.js App Router (Next.js 16+)
```
❌ async function Page({ params }) { const p = await params }  → ✅ const { slug } = params
❌ <a href="/shop">                     → ✅ <Link href="/shop">
❌ window.location.href                → ✅ router.push("/path")
❌ searchParams is Promise             → ✅ searchParams is plain object
❌ JSX.Element return type             → ✅ inferred return type (or ReactElement)
❌ experimental.ppr: "incremental"     → ✅ remove ppr key entirely (merged into cacheComponents)
❌ next.config.ts: eslint key           → ✅ remove eslint key (separate .eslintrc only)
```

### React 19
```
❌ JSX.Element return type               → ✅ inferred return type (no explicit type)
❌ useOptimistic for simple toggles       → ✅ useState for simple, useOptimistic for complex server-confirmed state
❌ Emoji icons (📷, 🎉, ✕)               → ✅ Lucide icons only
❌ sync `if (state.status) navigate()`   → ✅ `useEffect(() => { if (state.status) navigate() }, [state])`
```

### Next.js Build / Static Generation
```
❌ Prisma pages without DB at build time           → ✅ export const dynamic = "force-dynamic"
❌ R3F directly imported (ssr)                     → ✅ next/dynamic with ssr: false
❌ `use client` after `import type`                → ✅ `use client` MUST be the very first line
❌ next.config.ts: eslint key                      → ✅ remove, use .eslintrc or eslint.config.mjs only
❌ experimental.ppr key                            → ✅ removed in Next.js 16, now via cacheComponents
```

### Framer Motion v12 + R3F
```
❌ useScroll without useReducedMotion fallback         → ✅ always check useReducedMotion()
❌ Direct R3F import in page                           → ✅ next/dynamic with ssr: false, loading skeleton
❌ Missing @types/three                                 → ✅ pnpm add -D @types/three
```

### Prisma
```
❌ enum Genre                           → ✅ genre String  // type Genre = "ROMANCE" | "THRILLER"
❌ cart: any                            → ✅ type CartWithItems = Prisma.CartGetPayload<{ include: {...} }>
```

---

## 16. Phase 3 Remediation Learnings (2026-05-22)

**Version**: 3.3.0  
**Status**: Phase 3 AI integration & component wiring verified; all gates green

This section captures the architectural and implementation details, troubleshooting tips, and anti-patterns discovered while integrating AI components (OutfitCard, SizeRecommendation, StyleChat) into real pages (Account, PDP) and wiring `generateOutfit` to the real product catalog.

### 16.1 AI Component Integration Architecture

#### The "Client Island Dashboard" Pattern
When integrating multiple interactive AI components (`OutfitCard`, `StyleChat`, `SizeRecommendation`) into a server-rendered page, **extract the entire interactive region into a single Client Component**.

```tsx
// app/account/page.tsx — RSC (remains a Server Component!)
import { AIStylistDashboard } from "@/components/account/AIStylistDashboard";

export default function AccountPage() {
  return (
    <main className="...">
      {/* ... other server-rendered sections ... */}
      <AIStylistDashboard userId={userId} />
    </main>
  );
}
```

```tsx
// components/account/AIStylistDashboard.tsx — Single "use client" island
"use client";
export function AIStylistDashboard({ userId }: AIStylistDashboardProps) {
  const [activeTab, setActiveTab] = useState<Tab>("outfits");
  // All AI component state lives here
  return ( ... );
}
```

**Why this matters**:
- RSC pages cannot use `useState`, `useEffect`, or event handlers.
- A single `"use client"` wrapper component **preserves SSR for the rest of the page**.
- Multiple isolated `"use client"` islands cause hydration boundary overhead.

### 16.2 Product Actions Client Component Pattern

The **Product Detail Page (PDP)** requires interactive elements (variant selectors, size recommendation, add to cart). These must live in a Client Component.

```tsx
// app/shop/[category]/[slug]/page.tsx (RSC — no state, no hooks)
import { ProductActions } from "@/components/product/ProductActions";

export default async function ProductPage({ params }: PDPProps) {
  const product = await createProductService().getBySlug(params.slug);
  // ... fetch variants, images ...
  return (
    <ProductActions
      productId={product.id}
      productName={product.name}
      colorOptions={colorOptions}
      sizeOptions={sizeOptions}
      imageUrl={primaryImage?.url ?? null}
    />
  );
}
```

```tsx
// components/product/ProductActions.tsx — Single client component for ALL interactive elements
"use client";
export function ProductActions({ colorOptions, sizeOptions, ... }: ProductActionsProps) {
  const [selectedColor, setSelectedColor] = useState<string | null>(null);
  const [selectedSize, setSelectedSize] = useState<string | null>(null);
  const [sizeRecommendation, setSizeRecommendation] = useState<SizeRecommendationType | null>(null);
  const addToCart = useCartStore((s) => s.addItem);
  // ... variant selection, size advice, add to cart logic
}
```

**Key insight**: Combine ALL interactive elements (variant selectors, size recommendation, add to bag) into **one** Client Component. Do not create separate client components for each — it multiplies hydration boundaries and complicates shared state (e.g., deriving the selected variant from both color and size).

### 16.3 Wiring `generateOutfit` to Real Product Catalog

The `generateOutfit` tRPC procedure previously used only mock data. To wire it to the real catalog, the **router enriches the request with real product IDs before passing it to the AI service**.

```tsx
// server/routers/ai.ts
.generateOutfit: publicProcedure
  .input(z.object({ ... }))
  .mutation(async ({ input }) => {
    const productService = createProductService();
    const products = await productService.list({
      category: input.category ?? undefined,
      limit: 50,
    });

    const enrichedInput: OutfitRequest = {
      ...input,
      productIds: products.map((p) => p.id),
    };

    return aiService.generateOutfit(enrichedInput);
  }),
```

**Why this works**:
- The `ai.service.ts` expects `productIds` in `OutfitRequest` — a field already defined in the type.
- The AI prompt includes `productIds`, so the LLM knows which real products exist in the inventory.
- The service still falls back to mock data if no `OPENAI_API_KEY` is provided.
- **No changes to `ai.service.ts` were needed** — the router is the composition layer.

### 16.4 Testing Learnings: Vitest, jsdom, and DOM Cleanup

#### The "document is not defined" Error
When running component tests with `@testing-library/react` and `vitest`, the `render` function may fail with:
```
ReferenceError: document is not defined
```

**Root Cause**: `vitest` v4.x (installed at the monorepo root) was being used, which did not load the `jsdom` environment from `vitest.config.ts`. The `apps/web` package has `vitest` v3.2.4 configured with `environment: "jsdom"`.

**Fix**: Always run tests from the workspace package, not the monorepo root.
```bash
# ❌ WRONG: Uses monorepo root vitest (v4.x), ignores local config
cd /monorepo-root && npx vitest run

# ✅ CORRECT: Uses apps/web vitest (v3.2.4), loads vitest.config.ts
cd apps/web && npx vitest run
```

#### DOM Cleanup Between Tests
`@testing-library/react` does **not** auto-cleanup between tests in Vitest. Without explicit cleanup, queries from a previous test will match elements from the current test.

```tsx
// src/test/setup.ts
import { cleanup } from "@testing-library/react";

afterEach(() => {
  cleanup(); // ⬅️ REQUIRED in Vitest + testing-library/react
  vi.unstubAllGlobals();
  vi.useRealTimers();
});
```

**Symptom**: `screen.getByText("...")` returns an element from a previous test, or `Found multiple elements with the text: ...`.

### 16.5 Monorepo Version Mismatch Pitfall

When multiple versions of a tool exist in a monorepo (e.g., `vitest` v3.2.4 in `apps/web` and v4.1.7 in the monorepo root), running the command from the wrong directory causes silent behavior differences.

**Prevention**: Use `turbo` to run commands from the correct workspace.
```json
// package.json (root)
{
  "scripts": {
    "test": "turbo test"  // Runs pnpm test in each workspace
  }
}
```
```json
// apps/web/package.json
{
  "scripts": {
    "test": "vitest run"  // Uses the local vitest version
  }
}
```

### 16.6 Lint Script Improvement: Exclude Build Artifacts

The `validate-deprecated-twind.sh` script was flagging `.next/` build artifacts (e.g., `.next/dev/static/chunks/*.css` containing `.flex-shrink-0`). These are generated files, not source code.

```bash
# scripts/validate-deprecated-twind.sh
# ✅ CORRECT: Exclude build directories
grep -rEn --exclude-dir=.next --exclude-dir=node_modules --exclude-dir=dist 'bg-gradient-to-(r|l|t|b)|outline-none[^-]|flex-shrink-0' src/ packages/ apps/
```

### 16.7 Size Recommendation Component Test Coverage

`SizeRecommendation` has two distinct UI states:
1. **Empty state**: CTA button (`recommendation={null}`)
2. **Recommendation state**: Card with confidence bar (`recommendation={...}`)

Tests must cover both states, the click callback, and the optional `alternative` text.

```tsx
// SizeRecommendation.test.tsx
// Tests: empty state CTA, onGetAdvice click, recommendation card,
//        confidence bar width, alternative text presence/absence
```

**Key testing rules applied**:
- Use `vi.fn()` for mock callbacks from `vitest` (not `jest.fn()`).
- Query by text, not by role, when the role is ambiguous (e.g., multiple `<button>` elements).
- Test for the **absence** of elements (e.g., no alternative text when not provided) using `expect(...).not.toBeInTheDocument()`.

---

## 14. Phase 2 Verification & Critical Learnings (2026-05-20)

**Version**: 3.2.0  
**Status**: Phase 0–2 verified; all gates green

This section captures the hard-won knowledge from the full Phase 2 verification cycle — a comprehensive audit, remediation, and validation of the entire codebase against all six foundational documents (`AGENTS_2.md`, `CLAUDE.md`, `PRD`, `MASTER_EXECUTION_PLAN.md`, `status.md`, `SKILL.md`).

### 14.1 Complete Tooling Version Matrix (Verified)

| Technology | Version | Verification Status | Key Notes |
|------------|---------|----------------------|-----------|
| **Next.js** | `16.2.6` | ✅ Verified | `next lint` **removed from CLI**. Use `eslint` directly or shell scripts. |
| **React** | `19.2.6` | ✅ Verified | Global `JSX` namespace removed. `JSX.Element` triggers TS2307. |
| **TypeScript** | `6.0.3` | ✅ Verified | `erasableSyntaxOnly: true`, `verbatimModuleSyntax: true` enforced. |
| **Tailwind CSS** | `4.3.0` | ✅ Verified | `@tailwindcss/postcss` v4.3.0. CSS-first only. |
| **Prisma** | `6.19.3` | ✅ Verified | Client auto-generated on postinstall. Zero enums. |
| **Zod** | `4.4.3` | ✅ Verified | `result.error.issues[0].message` API stable. |
| **Zustand** | `5.0.13` | ✅ Verified | Selectors in JSX work correctly. |
| **NextAuth** | `4.24.14` | ✅ Verified | v4 API stable. `signIn("credentials", ...)` from `next-auth/react`. |
| **Framer Motion** | `12.39.0` | ✅ Verified | `useReducedMotion()` works. SSR safe with `ssr: false`. |
| **Three.js / R3F** | `0.184.0` / `9.6.1` | ✅ Verified | `@types/three` required. Dynamic import with `ssr: false`. |

### 14.2 Next.js 16 CLI Deprecations (CRITICAL)

**`next lint` is NOT AVAILABLE in Next.js v16 CLI.**

| Command | Next.js 15 | Next.js 16.2.6+ | Fix |
|---------|-----------|-------------------|-----|
| `next lint` | ✅ Available | ❌ **Removed** | Use `eslint` directly or shell validation scripts |
| `next --help` | Shows `lint` subcommand | Missing `lint` entirely | Verify with `npx next --help` |

**Root Cause**: Next.js v16 streamlined the CLI. Linting is now expected to be handled by the project's ESLint setup directly, not via a Next.js wrapper.

**Verified Fix for Monorepo**:
```json
// apps/web/package.json
{
  "scripts": {
    "lint": "cd ../../ && bash scripts/validate-deprecated-twind.sh && bash scripts/validate-colors.sh"
  }
}
```

**Shell Validation Scripts** (must be at repository root):
```bash
# scripts/validate-deprecated-twind.sh
#!/bin/bash
if grep -rEn 'bg-gradient-to-(r|l|t|b)|outline-none[^-]|flex-shrink-0' src/ packages/ apps/; then
  echo "Deprecated Tailwind v3 utilities found. Update to v4 names."
  exit 1
fi
echo "No deprecated Tailwind v3 utilities."

# scripts/validate-colors.sh
#!/bin/bash
if grep -rEn 'text-\[#[0-9A-Fa-f]{3,6}\]|bg-\[#[0-9A-Fa-f]{3,6}\]|border-\[#[0-9A-Fa-f]{3,6}\]' src/ packages/ apps/; then
  echo "Raw hex colors found in className. Use @theme tokens instead."
  exit 1
fi
echo "No raw hex colors in className."
```

### 14.3 Tailwind v4 Utility Migration (Complete Mapping)

The following v3 → v4 utility mappings were **verified in production code** during Phase 2 remediation:

| v3 Utility | v4 Utility | Files Found & Fixed | Risk Level |
|------------|-----------|---------------------|------------|
| `bg-gradient-to-r` | `bg-linear-to-r` | `HeroSection.tsx` | 🔴 High (breaks build) |
| `bg-gradient-to-b` | `bg-linear-to-b` | `HeroSection.tsx` | 🔴 High |
| `bg-gradient-to-t` | `bg-linear-to-t` | `CategoryShowcase.tsx`, `FeaturedCollections.tsx` | 🔴 High |
| `flex-shrink-0` | `shrink-0` | `ProductEmbed.tsx`, `NewArrivals.tsx` | 🟡 Medium ( silent) |
| `outline-none` | `outline-hidden` | *(none found)* | 🟢 Low (prevention) |

**Detection Command** (run before every commit):
```bash
grep -rEn 'bg-gradient-to-(r|l|t|b)|outline-none[^-]|flex-shrink-0' src/ packages/ apps/
```

### 14.4 Next.js 16 Configuration Cleanup

**Verified removals from `next.config.ts` for Next.js 16.2.6**:

```ts
// ❌ WRONG — all removed in Next.js 16
const nextConfig = {
  experimental: {
    ppr: "incremental"  // ❌ Removed — now via cacheComponents
  },
  eslint: {
    ignoreDuringBuilds: false  // ❌ Removed — use .eslintrc or eslint.config.mjs only
  }
};

// ✅ CORRECT — minimal Next.js 16 config
const nextConfig = {
  reactStrictMode: true,
  // Add other non-experimental config here
};
export default nextConfig;
```

### 14.5 Monorepo Lint Task Fix (Turborepo Integration)

**Problem**: `turbo lint` failed because `next lint` doesn't exist.
**Solution**: Use the shell validation scripts in the web app `lint` script.

```json
// apps/web/package.json
{
  "scripts": {
    "lint": "cd ../../ && bash scripts/validate-deprecated-twind.sh && bash scripts/validate-colors.sh && echo 'All lint checks passed'"
  }
}
```

**Packages without a Next.js app** (e.g., `packages/ui`, `packages/utils`): Do NOT need a `lint` script, or can use `echo "No lint required for package"`.

### 14.6 New Mistakes (#24–#28)

#### Mistake #24: `next lint` Still Used in Next.js 16
**Fix**: Replace `next lint` with `eslint .` or shell validation scripts.
```json
// ❌ WRONG
"lint": "next lint"

// ✅ CORRECT
"lint": "cd ../../ && bash scripts/validate-deprecated-twind.sh && bash scripts/validate-colors.sh"
```

#### Mistake #25: Forgetting to Run Validation Scripts Before Commit
**Fix**: Add to pre-commit hook or CI pipeline.
```bash
# .github/workflows/ci.yml
- run: bash scripts/validate-deprecated-twind.sh
- run: bash scripts/validate-colors.sh
```

#### Mistake #26: Assuming `params` is a Typed Object
**Fix**: In Next.js 16, `params` is a plain object but **NOT** strongly typed by default. Add your own type.
```tsx
// ❌ WRONG — params might not have the type you expect
export default function Page({ params }) {
  const { slug } = params; // slug might be string | string[] | undefined
}

// ✅ CORRECT — explicit typing
interface PageProps {
  params: { slug: string };
}
export default function Page({ params }: PageProps) {
  const { slug } = params; // slug is string
}
```

#### Mistake #27: Missing `@types/three` in Dev Dependencies
**Fix**: Always install `@types/three` when using R3F.
```bash
pnpm add -D @types/three
```

#### Mistake #28: Using `flex-shrink-0` Instead of `shrink-0` in Tailwind v4
**Fix**: `flex-shrink-0` is a v3 utility. In v4, use `shrink-0`.
```html
<!-- ❌ WRONG -->
<div class="flex-shrink-0">...</div>

<!-- ✅ CORRECT -->
<div class="shrink-0">...</div>
```

### 14.7 Verification Checklist (Updated)

Before declaring any phase complete, run this exact sequence:

```bash
# 1. TypeScript strict check
pnpm typecheck  # tsc --noEmit — zero errors

# 2. Lint (now shell scripts)
pnpm lint  # validate-deprecated-twind.sh + validate-colors.sh

# 3. Tests
pnpm test  # vitest run — zero failures

# 4. Production build
pnpm build  # next build — zero errors
```

**Expected Output**:
```
Tasks: 2 successful, 2 total   # typecheck
Tasks: 1 successful, 1 total   # lint
Tasks: 1 successful, 1 total   # test
Tasks: 2 successful, 2 total   # build
```

### 14.8 Quick Reference: Next.js 16 Gotchas

| Gotcha | v15 | v16 Fix |
|--------|-----|---------|
| `experimental.ppr` | `"incremental"` | Remove entirely |
| `next.config.ts` `eslint` key | `ignoreDuringBuilds` | Remove; use `.eslintrc` only |
| `next lint` CLI | Available | **NOT available**; use `eslint` or scripts |
| `params` type | `Promise<{ slug: string }>` | Plain object; add explicit interface |
| `next --help` | Shows `lint` | Missing `lint` subcommand |

### 14.9 Prisma Schema/Type Synchronization (New)

| Symptom | Cause | Fix |
|---------|-------|-----|
| `TS2339: Property 'X' does not exist on type 'Y'` | Prisma types stale after schema change | Run `pnpm db:generate` after every schema change |
| `TS2322: Property 'totalPrice' missing in type '{ ... }'` | New required field added to model, not to code | Add field to every `prisma.model.create()` call |
| `Unknown field \`viewCount\`` | Field not in schema; assumed from domain logic | Check `schema.prisma` before using field |

**Prevention**:
```bash
# Add to pre-commit hook
pnpm db:generate && pnpm typecheck
```

### 14.10 Search tRPC Implementation (Phase 2)

**Router**: `src/server/routers/search.ts`
- `search.query({ q, limit, category, minPrice, maxPrice, sort })` — Full-text product search
- `search.suggestions({ q, limit })` — Quick autocomplete results
- `search.facets({ q })` — Faceted search metadata (categories, brands, price range)
- `search.trending()` — Popular search terms (mock until analytics)

**Client Wiring**:
| Component | tRPC Hook | Notes |
|-----------|-----------|-------|
| `SearchInput.tsx` | `trpc.search.suggestions.useQuery` | Debounced by 300ms |
| `SearchOverlay.tsx` | `trpc.search.trending.useQuery` | Mock data until analytics |
| `app/search/page.tsx` | `trpc.search.query.useQuery` | Reads `?q=` from URL params |
| `FacetFilter.tsx` | URL params only | Fully wired to `router.replace` with `startTransition` |

**Key Gotchas**:
1. **Client Component required**: `app/search/page.tsx` must be `"use client"` because it uses `useSearchParams()`. Wrap in `<Suspense>` for SSR safety.
2. **Empty `q` parameter**: Disable query with `enabled: query.length > 0` to prevent tRPC from firing on initial mount.
3. **Prisma `relevance` sort**: Not a real field. Fallback to `createdAt: "desc"` if `sort` is not provided.

### 14.11 Tailwind v4 Upgrade Patterns (Field-Tested)

| v3 Utility | v4 Utility | Files Found & Fixed | Risk Level |
|------------|-----------|---------------------|------------|
| `bg-gradient-to-r` | `bg-linear-to-r` | `HeroSection.tsx` | 🔴 High (breaks build) |
| `bg-gradient-to-b` | `bg-linear-to-b` | `HeroSection.tsx` | 🔴 High |
| `bg-gradient-to-t` | `bg-linear-to-t` | `CategoryShowcase.tsx`, `FeaturedCollections.tsx` | 🔴 High |
| `flex-shrink-0` | `shrink-0` | `ProductEmbed.tsx`, `NewArrivals.tsx` | 🟡 Medium ( silent) |
| `outline-none` | `outline-hidden` | *(none found)* | 🟢 Low (prevention) |

**CSS Detection** (run before every commit):
```bash
grep -rEn 'bg-gradient-to-(r|l|t|b)|outline-none[^-]|flex-shrink-0' src/ packages/ apps/
```

---

> **Final Directive**: Every element must justify its existence. Reject generic AI tropes. Prioritize intentionality over trends. Accessibility is non-negotiable. Performance is luxury. Deliver nothing less than production-grade, meticulously verified, and architecturally sound.

---

## 17. Anti-Pattern Prevention Matrix (All Phases)

| Anti-Pattern | Symptom | Prevention |
|-------------|---------|------------|
| Stale Prisma types | `TS2339` after schema change | `prisma generate` hook after every schema edit |
| Missing `create()` fields | `TS2322` on `prisma.model.create()` | Run `tsc --noEmit` before committing |
| `<a>` for internal nav | Full page reloads | Enforce `next/link` via ESLint rule |
| `window.location.href` | Lost state | Use `useRouter().push()` |
| `useOptimistic` for booleans | Type mismatch, overcomplexity | `useState` for simple toggles; `useOptimistic` for server-confirmed only |
| `enum` or `namespace` | `erasableSyntaxOnly` error | String unions only |
| `.getState()` in JSX | No reactivity, stale data | Selectors: `useStore(s => s.items)` |
| Persisted UI state | Leaks to localStorage, crashes on rehydrate | `partialize: (s) => ({ items: s.items })` |
| `async` on non-fetching components | Misleading, TypeScript confusion | Remove `async` when no `await` |
| Missing `useId()` | Duplicate IDs, broken ARIA | Always use `useId()` for label/input pairs |
| `bg-gradient-to-*` | Build error in Tailwind v4 | Use `bg-linear-to-*` |
| `outline-none` | Missing focus indicators | Use `outline-hidden` |
| `flex-shrink-0` | Silent utility failure | Use `shrink-0` |

---

## 18. Verification Commands Cheat Sheet

```bash
# Full verification pipeline
pnpm typecheck && pnpm lint && pnpm test && pnpm build

# Prisma type sync check
cd apps/web && pnpm db:generate && pnpm typecheck

# Tailwind v3 utility scan
grep -rEn 'bg-gradient-to-(r|l|t|b)|outline-none[^-]|flex-shrink-0' src/ packages/ apps/

# Raw hex color scan
grep -rEn 'text-\[#[0-9A-Fa-f]{3,6}\]|bg-\[#[0-9A-Fa-f]{3,6}\]' src/ packages/ apps/

# `<a>` tag internal nav scan
grep -rn '<a href="/' src/ packages/ apps/ --include="*.tsx"

# `window.location` usage scan
grep -rn 'window.location' src/ packages/ apps/ --include="*.tsx"

# `any` type scan
grep -rn ': any' src/ packages/ apps/ --include="*.ts" --include="*.tsx"

# `enum` / `namespace` scan
grep -rn 'enum ' src/ packages/ apps/ --include="*.ts" --include="*.tsx"
```
