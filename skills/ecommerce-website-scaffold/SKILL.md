---
name: ecommerce-website-scaffold
description: >-
  Production-grade engineering skill for building, extending, rebranding, or
  auditing any e-commerce website codebase on the Next.js 16 App Router +
  React 19 + Prisma + Tailwind v4 stack. Covers the full commerce domain:
  catalog, cart, checkout, payments, orders, admin, auth, security, testing,
  and deployment. Every pattern below was distilled from three independently
  audited production-grade storefront codebases (860+ unit tests and 700+ e2e
  cases of combined verification culture).
version: 1.0.0
created: 2026-10-21
license: accompany with an explicit LICENSE when used as a template
provenance: >-
  Synthesized and generalized from ecommerce-store_SKILL.md (v1.62.0, 32 traps,
  66 ADRs), homenest-store-s_SKILL.md (v1.56.0, 18-model commerce schema,
  real-engine harnesses), and luxury-fashion-store_SKILL.md (v1.47.0, 42 traps,
  wire-level security gates), cross-checked against the October 2026
  comparative template-suitability audit of all three repositories.
---

## How to Use This Skill

| If you are... | Read first |
|---|---|
| Scaffolding a new store from zero | §1 → §2 → §3 → §7 → §19, then work section by section |
| Extending an existing store built on this skill | §5 → §6 → §15, then the §13 trap log for your area |
| Debugging something broken | §14 (symptom table) → §13 (trap log) → §8/§9 for the domain |
| preparing to ship | §19 (pre-ship checklist) — the full gate chain, no exceptions |
| Rebranding / re-theming a store | §4 → §18 |
| Auditing a codebase for production readiness | §18 → §8 → §9 → §11 |

**The prime directive:** when any section of this skill conflicts with the code and its tests, the code and its tests win — then fix this skill in the same change. A skill that drifts from the codebase is worse than no skill, because it teaches lies with confidence.

---

## §1. Purpose, Philosophy & Non-Negotiables

This skill builds a self-hosted, database-backed e-commerce web application: storefront, cart, checkout, payments, order management, and an admin back office. It is stack-opinionated (Next.js 16 App Router, React 19, TypeScript strict, Prisma, Tailwind v4, Zod, Vitest, Playwright) and domain-complete: every commerce concept below is load-bearing and backed by a tested pattern.

### The five laws

1. **Server truth is the only truth.** The client mirrors state for display; the server re-derives every price, total, discount, and stock count inside the transaction that writes the order. A client that sends an amount is a client under attack.
2. **One mutation seam.** All writes flow through server actions (or a tightly-whitelisted set of route handlers — health, search, newsletter, and the payment webhook). No REST mutation sprawl, no client-side optimistic math as the source of record.
3. **Evidence over assertion.** A change is done when lint, typecheck, unit, build, and e2e gates are green — not when it looks right. A gate is only trusted after a mutation has deliberately failed it. Measure, never eyeball.
4. **Traps are institutional memory.** Every framework or domain trap encountered is recorded in §13 with symptom, root cause, and fix — at the point of temptation (in-file comments) and here (the canonical registry). Never work around a trap silently; never "simplify" a pin whose reason you don't know.
5. **The repository is a product.** A codebase meant to be reused ships a LICENSE, carries no unrelated baggage, and keeps its documentation truthful in the same commit as the code change. (§18 exists because all three source repositories failed at least one of these.)

### Operating philosophy

- **Vertical slices**: one seam, one test, one implementation per change. Never a "big refactor" commit.
- **TDD order**: failing test → minimal fix → full gate chain. Tests encode contracts (db-path, money math, rate-limit floors, access control); extend them first.
- **`main` only**: no feature branches; Conventional Commits, atomic. Every commit passes the full gate chain.
- **Demo honesty**: a payment step that is not real must say so in the UI and store only what a demo needs (card last-4 at most). Never wire a fake success that looks real.
- **Documentation as a system**: README (operations manual), AGENTS.md (agent cheat-sheet: commands, traps, invariants), CLAUDE.md (working standards and workflow), Project_Architecture_Document.md (ADRs, threat model, known issues), SKILL.md (this distilled skill). Update the affected documents in the same commit as the change.

---

## §2. Reference Stack & Version Discipline

| Layer | Choice | Notes |
|---|---|---|
| Framework | Next.js 16 (App Router only, `output: "standalone"`) | `src/proxy.ts` replaces `middleware.ts` in Next 16. `params` and `cookies()` are async. |
| UI runtime | React 19 | Compiler-era lint rules; `react-hooks/set-state-in-effect` configured as an **error**. |
| Language | TypeScript 5.9 strict | `strict: true`, `noImplicitAny` stays **on**, `noUncheckedIndexedAccess` recommended (strongest posture audited). `tsc --noEmit` is the gate — never `ignoreBuildErrors`. |
| Styling | Tailwind CSS 4 (CSS-first `@theme inline` in `globals.css`) | **No `tailwind.config.js` — adding one is a bug.** Pin migrated defaults explicitly (§4). |
| Components | Radix primitives (dialog, select, tabs, label, radio-group, slot) + shadcn-style wrappers | CVA + clsx + tailwind-merge (`cn()` helper); lucide-react for icons. |
| Database | Prisma 6 + SQLite (single file, schema-relative URL) | Portable to PostgreSQL when scaling (§18.5). No Prisma enums under SQLite — string vocabularies + Zod. |
| Validation | Zod at every boundary | One `validation.ts` module; reuse shared `emailSchema` / `passwordSchema`. |
| Unit tests | Vitest (node env, `*.test.ts`) | Tests type-checked as their own gate (`tsconfig.tests.json`). |
| E2E tests | Playwright, Chromium | Against the **production standalone build** on a dedicated port (:3100), never the dev server. |
| Package manager | npm (Node >= 20) or Bun >= 1.3 | npm + committed lockfile is the safest default; Bun works but walks up parent directories loading `.env` (§13.C1). |
| Fonts | Self-hosted woff2 via `@font-face` in `public/fonts/` | Hermetic builds, no CDN. Do not use `next/font` if pixel-measured font parity matters (§13.G8). |

**Version discipline:** pin exact versions in the stack table of the project's own SKILL.md and update it in the same commit as any bump. Assume every framework major moves defaults (shadows, radii, palette, spacing semantics, serialization) — see the Tailwind pin families in §4 and the trap log before upgrading.

**Runtime facts to verify on a new machine:** Node >= 20; sandbox/CI environments may export a `DATABASE_URL` that silently overrides `.env` (§13.C1 — diagnose with `node -e "console.log(process.env.DATABASE_URL)"`); a long-lived dev server must be restarted after any reseed (§13.C3).

---

## §3. Project Scaffold & Environment Contract

### 3.1 Directory layout

```
<repo>/
  src/
    app/
      layout.tsx              # fonts + globals only — chrome-free root
      globals.css             # ALL design tokens + engine pins (§4)
      not-found.tsx           # chrome-less platform 404
      error.tsx               # segment boundary (dependency-free)
      global-error.tsx        # ROOT boundary; renders own <html>/<body>, imports globals.css
      icon.svg / favicon.ico / apple-icon.png / opengraph-image.png   # metadata file convention
      manifest.ts             # STATIC, origin-independent, DB-free
      robots.ts / sitemap.ts  # force-dynamic, reads catalog
      (storefront)/           # chrome + StoreProvider composition point
        layout.tsx            # header, footer, overlays, provider hydration, ONE <main>
        page.tsx  shop/  product/[slug]/  cart/  checkout/(+success)
        account/(+orders/[id])  wishlist/  track-order/  admin/*
      (auth)/                 # chrome-less centered cards; layout awaits connection()
        login/  register/  forgot-password/  verify-email/  reset-password/
      api/
        health/               # liveness + DB round-trip (SELECT 1)
        search/  newsletter/  # read or idempotent-write whitelist
        checkout/             # (route-handler variant of the money seam, if used)
        webhooks/stripe/      # the ONLY signature-verified external write surface
    components/
      ui/                     # shadcn-style primitives (button, input, dialog, select, sheet, tabs, toast)
      store/                  # storefront chrome + islands (header, footer, mobile-nav, cart-drawer,
                              #   search-overlay, product-card, store-provider, quantity-stepper)
      account/  checkout/     # domain islands
    lib/
      db.ts                   # the ONLY Prisma instantiation (globalThis HMR-safe singleton)
      db-path.ts              # schema-relative URL contract (test-pinned — do not simplify)
      auth.ts password.ts auth-secret.ts session.ts
      cart.ts cart-dto.ts wishlist.ts money.ts order-money.ts coupons.ts
      order-status.ts order-tracking.ts order-access.ts order-token.ts
      rate-limit.ts client-ip.ts csp.ts proxy support
      validation.ts           # EVERY Zod schema, one module
      stripe.ts stripe-config.ts stripe-payment.ts   # when payments are wired (§9)
      actions/                # "use server" — the ONLY mutation seam
        auth.ts checkout.ts admin.ts reviews.ts newsletter.ts stripe.ts
    proxy.ts                  # Next 16 middleware: per-request CSP nonce (request AND response headers)
    instrumentation.ts        # boot-time guards (AUTH_SECRET) + sweeper wiring
  prisma/
    schema.prisma             # §7 blueprint
    seed.ts                   # idempotent catalog + demo fixtures
  db/                         # git-ignored SQLite home (custom.db, e2e.db)
  public/  fonts/  robots is a ROUTE not a file (§13.B7)
  tests/
    unit/                     # Vitest contracts
    e2e/                      # Playwright specs + helpers.ts (gotoHydrated) + .auth/ storageState
  scripts/                    # assemble-standalone.mjs, e2e-reset, capture-screenshots
  .env.example  LICENSE  README.md  AGENTS.md  CLAUDE.md
  Project_Architecture_Document.md  SKILL.md   # this document, project-specific instance
```

### 3.2 Environment contract

| Variable | Required | Purpose |
|---|---|---|
| `DATABASE_URL` | yes | `file:../db/custom.db` — **relative to `prisma/schema.prisma`**, resolved identically by CLI and runtime through `db-path.ts`. Absolute `file:` URLs and non-SQLite URLs pass through untouched. |
| `AUTH_SECRET` | **production: yes** | HMAC key for session cookies and capability tokens. A boot-time guard (`auth-secret.ts`, wired via `instrumentation.ts`) **refuses to start** in production if missing or equal to the dev constant. Dev may fall back to a documented insecure constant — production must never. |
| `NEXT_PUBLIC_SITE_URL` | recommended | Canonical origin for metadata, sitemap, robots, OG tags. |
| `TRUST_PROXY` | behind proxy only | Set `=1` only when behind a trusted reverse proxy, to trust `x-forwarded-for` for rate limiting. |
| `NEXT_PUBLIC_DEMO_MODE` | optional | `false` hides demo-credential helper UI. |
| `STRIPE_SECRET_KEY`, `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY`, `STRIPE_WEBHOOK_SECRET` | when payments on | §9. Demo checkout when absent — clearly labeled, never a fake success. |
| `EMAIL_*` | when email on | Transactional provider credentials. Until wired, verification/reset codes log to a **console seam** tagged `[email:stub]` and the flows stay env-gated OFF. |

`.env.example` is the tracked contract; `.env`, `db/*.db`, `*.key`, logs, and `tests/e2e/.auth/` are git-ignored. **Never commit any key material — not even partially redacted (see §18.3).**

### 3.3 Scripts — what each really does

| Script | Reality |
|---|---|
| `dev` | `next dev` on :3000, logs tee'd to `dev.log`. |
| `build` | `next build` **then** `node scripts/assemble-standalone.mjs` which copies `.next/static` + `public/` into `.next/standalone/`. **Never remove the assemble step** — without it the standalone server serves zero-hydration pages (§13.B1). Also `mkdir -p public` (fresh-clone trap). |
| `start` | `NODE_ENV=production node .next/standalone/server.js`. Reads `PORT`. Note `.env` is copied into `standalone/` **at build time** — env changes require a rebuild. |
| `db:setup` | `prisma db push` + `tsx prisma/seed.ts` (idempotent upserts). |
| `db:reset` | Delete DB file(s) + `db:setup`. Restart any long-lived dev server afterwards (§13.C3). |
| `lint` / `typecheck` / `typecheck:tests` | ESLint 9 flat / `tsc --noEmit` / tests' own tsconfig — all must exit 0. |
| `test` / `test:e2e` | Vitest / Playwright. `test:e2e` boots the **standalone build** on :3100 with an isolated `DATABASE_URL=file:../db/e2e.db` — run `build` first or you test stale code (§13.F1). |
| `verify` | The chain: `typecheck && lint && test && build` — one command, the pre-e2e gate. |

### 3.4 Bootstrap sequence (fresh clone)

```bash
npm install
cp .env.example .env          # set AUTH_SECRET for anything production-like
npm run db:setup              # push + idempotent seed
npm run dev                   # http://localhost:3000
curl localhost:3000/api/health   # {"status":"ok","db":"up"} — the DB round-trip must be true
```

Seed provides: one admin + one demo customer account, a small catalog, and a few canonical orders with timeline events. Seeded passwords use fixed scrypt salts so hashes are deterministic across machines. `e2e-reset` (or global-setup) restores canonical fixtures between e2e runs.

**CI requirement (non-negotiable, §18):** a pipeline running `verify` + `test:e2e` on every push, plus a Dockerfile for the standalone deployment. The source repositories shipped 500+ case suites with **no CI to run them** — do not repeat that: an unexecuted gate is a rumor, not a gate.

---

## §4. The Design System (Code-First, Tokens-First)

### 4.1 Token taxonomy

All tokens live in `src/app/globals.css` under `@theme inline` — as **full `hsl()` literals** (bare `H S% L%` triplets silently resolve to transparent under v4; §13.A1):

```css
@theme inline {
  --color-background: hsl(30 25% 98%);      /* page paper */
  --color-foreground: hsl(240 10% 10%);     /* ink, footer */
  --color-card: hsl(0 0% 100%);
  --color-primary: hsl(24 80% 50%);         /* ONE saturated brand color */
  --color-primary-foreground: hsl(0 0% 100%);
  --color-secondary: hsl(30 15% 94%);       /* chips, placeholders */
  --color-muted-foreground: hsl(240 5% 46%);
  --color-accent: hsl(24 80% 96%);
  --color-destructive: hsl(0 84% 60%);      /* errors, discount badges ONLY */
  --color-border: hsl(30 15% 90%);
  --color-ring: hsl(24 80% 50%);
}
```

Rules that survive any brand:

- **One saturated primary**, used sparingly: announcement bar, primary CTAs, active states. Everything else is neutral.
- **Semantic reservation**: `destructive` is for errors and discount badges — never decoration. `muted-foreground` carries all secondary text.
- **CTA hierarchy**: primary pill for the one main action per view → outline secondary → text links tertiary. Never two filled buttons of equal weight.
- **Radii**: pick 2–3 (e.g. cards 16, buttons 12, inputs 10) and pin them (§4.2).
- **Motion budget**: hover 150–200ms `transition-colors`; overlays 300–500ms; no spring physics, no parallax. Respect `prefers-reduced-motion` globally (§12.2).
- **Anti-generic mandate**: no purple/blue gradients, no glassmorphism, no shadows heavier than `shadow-sm`, no icon-only buttons without `aria-label`, no default-font laziness. One accent font may carry the typographic identity; body stays a workhorse sans.

### 4.2 Engine pins — when porting a design across engine versions

The source family ported Tailwind-v3-measured designs onto v4. The general law: **the engine is part of the design system — assume an engine migration moves every default.** Pin, don't re-eyeball:

| Pin | Why |
|---|---|
| `--shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05)` | v4 shifted the whole shadow scale up one notch. |
| Radius scale (`--radius-xl: .75rem; --radius-2xl: 1rem; --radius-3xl: 1.5rem`) | v4 `2xl` = 20px ≠ v3's 16px. |
| `@custom-variant hover (&:hover);` | v4 gates hover behind `@media (hover:hover)`; un-gate so touch/hybrid contexts render hover styles. |
| `@keyframes` at **top level** of globals.css | `@theme inline` does not emit nested keyframes — `animation-name` computes `none` (§13.A5). |
| Palette hexes if migrating measured v3 colors | v4 serializes its default palette in oklab; pin v3 hexes or assert token identity, not strings (§13.A6). |
| Stacking: `flex gap-N` over `space-y-*` | v4 `space-y` emits `margin-block-end` on non-last children via `:where()` — inert when the first child is inline; geometry differs (§13.A2). |

When there is **no reference design** (greenfield build), author the tokens first, screenshot, and treat your own measured values as the contract — the "measure, then pin" ritual is identical; the reference is just your own first render.

### 4.3 Typography & fonts

Self-host woff2 files in `public/fonts/`, declared with plain `@font-face` under your family names. Keep `-webkit-font-smoothing` off the body unless the design demands it (subpixel AA is the browser default; `antialiased` measurably changes rasterization). If pixel parity with an existing site matters, font parity is **file parity** — never let a subsetting pipeline repackage your woff2 (§13.G8).

---

## §5. Component Architecture & Layering

**The golden rule: imports point downward only.**

```
app (routes)  →  components (ui / store / account / checkout)  →  lib (domains + actions)  →  db (Prisma)
```

| Layer | Contents | Rules |
|---|---|---|
| 0 — Data | `lib/db.ts` | The ONLY Prisma instantiation; globalThis HMR-safe singleton; sets `DATABASE_URL` via `db-path.ts` at import time. Never imported from a client file. |
| 1 — Domains | `lib/*.ts` server modules (auth, cart, money, coupons, order-*, rate-limit, csp, validation...) | **No React imports.** Pure seams here let a client island and a server page share one source — but split pure DTOs into `-dto.ts` files; a client component must never import a module that pulls `next/headers` or Prisma (§13.B8 class). |
| 2 — Mutations | `lib/actions/*.ts` | `"use server"` + Zod + `ActionResult<T>` + authz + transaction. The only write seam. |
| 3 — Rendering | RSC pages + client islands | Pages fetch via Prisma directly; islands receive **serialized DTOs, never Prisma objects**. |
| 4 — Chrome | `(storefront)/layout.tsx` | Owns header/footer/overlays, hydrates StoreProvider, renders exactly ONE `<main>`. The root layout stays chrome-free. |

### Route groups (URL-neutral)

| Group | Layout owns | Contains |
|---|---|---|
| root | html/body/fonts/metadata only | chrome-less 404, `api/*`, sitemap, robots |
| `(storefront)` | chrome + provider | home, shop, PDP, cart, checkout, account, wishlist, admin |
| `(auth)` | bare centered card | login, register, forgot/verify/reset |

Consequences: chrome-less surfaces (auth, 404) render **without** the store context — never import store-dependent chrome there. The StoreProvider instance **survives client navigation inside the group** — logout MUST call `setUser(null)` (§13.D6). Admin lives inside `(storefront)` so it shares chrome, but every admin page wraps its content in a plain `<div class="flex-1">`; only the layout owns `<main>` (nested `<main>` is invalid HTML and breaks `getByRole("main")`).

### Server/client decision tree

- Event handler / browser API / animation → `"use client"` island. Everything else stays RSC.
- A page is per-request (`force-dynamic` equivalent) if it reads cookies/DB — and per-request CSP nonces require it **anyway**; in Next 16.4 `force-dynamic` alone did NOT de-prerender — `await connection()` in the layout is the reliable pin (§13.B3).
- `dangerouslySetInnerHTML` is allowed **only** for JSON-LD, through an HTML-escaping serializer (§12.1).

---

## §6. Client State Discipline (the StoreProvider Contract)

**One React context. No state library. No custom hooks by design.** All client state lives in a single `store-provider.tsx`:

- **Server-truth domain state**: `cart: CartDto`, `user: SessionUser | null`, `wishlist: Set<string>`, `hydrated: boolean`. Initialized from server props, and **re-derived after every mutation** — `addToCart`/`updateQuantity` set the server's response, never optimistic local math.
- **UI state**: `cartOpen`, `mobileNavOpen`, `searchOpen` + setters — any surface can open the overlays.
- **`setUser`**: exposed for logout (the provider outlives client-side navigation).

### The three React 19 patterns (instead of effects)

`react-hooks/set-state-in-effect` is configured as an **error**. If you feel the need for setState-in-effect, the answer is one of these:

```tsx
// 1. Adjust-state-during-render (last-seen-props re-sync)
const [lastSynced, setLastSynced] = useState(serverCart);
if (serverCart !== lastSynced) {   // during render — no effect
  setLastSynced(serverCart);
  setCart(serverCart);
}

// 2. Derived state — compute at render
const visibleHits = useMemo(() => hits.filter(h => h.name.includes(q)), [hits, q]);

// 3. useActionState + startTransition for async dispatch
const [state, submit, pending] = useActionState(action, initialState);
```

Keep the "last seen props" in **state, not a ref** (React Compiler `refs` rule forbids ref access during render), and never in an effect (it's an error).

### Hydration sentinel

The provider sets `document.documentElement.dataset.hydrated = "true"` on mount. Every e2e helper waits for it:

```ts
export async function gotoHydrated(page: Page, path: string) {
  await page.goto(path);
  await page.waitForSelector('html[data-hydrated="true"]');
}
```

Clicks that land in the pre-hydration window fall back to native form GETs — that race produced real bugs in every source repo. For maximum robustness, poll for the React fiber before interacting (§13.F2).

### Optimistic updates (the one legal pattern)

Mirror, don't originate: snapshot `prev` → optimistic `setState` → `setPendingId(id)` (per-line lock) → fetch → on error roll back to `prev` → `finally` clear pending. Buttons `disabled={pendingId === line.id}`. The server response is always the new state; the server-clamped quantity in the response wins over the optimistic guess.

---

## §7. Data Layer: Schema Blueprint, Money & Identity

### 7.1 The core schema (18 models — the complete commerce domain)

| Model | Key fields & relations | Contract notes |
|---|---|---|
| `User` | `email @unique`, `passwordHash String?`, name, `role String @default("customer")` | Roles validated by Zod vocabulary (SQLite has no enums). |
| `Session` | `token @unique` (**SHA-256 hash of the cookie token — plaintext never stored**), `userId` Cascade, `expiresAt` | DB rows = revocable sessions. |
| `Address` | `userId` Cascade, full postal fields, `isDefault` | Default-address exclusivity enforced in the action. |
| `Category` | `slug @unique`, name, `sortOrder`, `isActive` | Guarded delete: refuse while products reference it. |
| `Product` | `slug @unique`, `categoryId`, `price Int` (cents), `compareAtPrice Int?`, `sku @unique`, `stock Int`, `images/tags/specs` (JSON strings), `rating Float`, `reviewCount`, `isFeatured`, `isActive` | `isActive: false` = archived/draft — filtered from storefront, preserved in order history. |
| `Review` | `productId` Cascade, `userId?` SetNull, `rating Int` (1..5), `verified` | Aggregates recomputed transactionally on write. |
| `Cart` / `CartItem` | `token @unique` (guest cookie), `userId? @unique`, composite unique `(cartId, productId)` | Reads never mint rows; creation only in mutation contexts. |
| `Wishlist` / `WishlistItem` | same identity pattern | Bounded (e.g. 100 items) with one-request add-all. |
| `Order` | `number @unique` (`ORD-YYYY-NNNN`), `idempotencyKey @unique?`, `cartToken`, `userId?`, email, `status`, **all money columns Int cents** (`subtotal, shipping, tax, discount, total`), `couponCode?`, `shippingMethod`, `shippingAddress String` (JSON snapshot), `carrier?`, `trackingNumber?` | Status vocabulary: `pending \| processing \| shipped \| delivered \| cancelled` — cancelled/delivered terminal. |
| `OrderItem` | `orderId` Cascade, `productId?` (optional — snapshot survives product deletion), **`nameSnapshot`, `imageSnapshot`, `unitPrice Int` (cents at purchase)**, quantity | **Snapshots at purchase time; catalog edits never rewrite history.** |
| `OrderEvent` | `orderId` Cascade, `type` (`placed \| status_changed \| tracking_added`), `actor` (`system \| admin`) | The order timeline; admin notes never reach customer views (filter by actor). |
| `Coupon` | `code @unique`, `type` (`percent \| fixed \| free_shipping`), `value Int`, `minSubtotal Int?`, `maxRedemptions?`, `timesUsed`, `expiresAt?`, `isActive` | Redemption guard is atomic (§7.4). |
| `CarouselSlide` | title, image, `ctaText/ctaLink` (internal-or-https validated), `sortOrder`, `isActive` | |
| `StoreSetting` | `key @id`, value | Settings KV: shipping rates, tax rate, free-shipping threshold, legal contact. |
| `NewsletterSubscriber` | `email @unique` | Idempotent subscribe. |
| `ContactMessage` | name, email, subject, message, `handled` | |
| `StripeEvent` *(when payments on)* | `eventId @unique`, type, payload, resolvedAt | Webhook dedup row — commits **inside** the placement transaction (§9.4). |

**Indexing rule:** every FK used in a lookup gets an index (unique constraints give you some; add explicit `@@index` for the rest — e.g. `OrderItem.orderId`, `CartItem.cartId`). Invisible at demo scale, costly after a Postgres port.

### 7.2 The money seam

- **Integer cents everywhere.** Money columns are `Int`; thresholds in settings are cents; coupons' fixed values are cents.
- Exactly two helpers in `lib/money.ts`: `formatMoney(cents)` (display) and `parseDollarsToCents(input)` (admin input) — **the only place dollars→cents conversion happens**.
- One pure function computes totals: `computeOrderMoney({ subtotal, discount, shippingMethod, freeShippingThresholdCents, standardShippingCents, expressShippingCents, taxRatePercent })` — integer math, unit-tested (threshold pins, tax rounding pins).
- JSON-LD `offers.price` is **decimal USD** (`price / 100`), never cents.
- The client never sends an amount. The only payment detail a demo checkout may persist is `cardLast4`.

### 7.3 The db-path contract

`DATABASE_URL="file:../db/custom.db"` resolves against the directory owning `prisma/schema.prisma` — for the CLI **and** at runtime via `lib/db-path.ts` — so `db:push`, `db:seed`, `dev`, `build`, and the standalone server all open ONE file regardless of CWD. Absolute `file:` URLs pass through untouched (the e2e webServer deliberately uses an absolute path because standalone file-tracing copies `schema.prisma` into the bundle; §13.B2). This module is pinned by unit tests — **do not simplify it**.

### 7.4 The four data invariants

1. **Conditional atomic writes.** Any "validate then write" pair becomes ONE statement with the guard in the `where`:
   ```ts
   const reserved = await tx.product.updateMany({
     where: { id: item.productId, stock: { gte: item.quantity } },
     data: { stock: { decrement: item.quantity } },
   });
   if (reserved.count === 0) throw new CheckoutError(409, "Stock just ran out...");
   ```
   Applies to stock, coupon-cap increments (`timesUsed` guard), address caps — every race-prone seam. Check-then-act across an `await` is a bug (§13.C7).
2. **Idempotent placement.** One `idempotencyKey` per checkout visit; a replay returns the already-placed order; `P2002` on the key resolves to the winner; the retry loop only retries order-number collisions.
3. **Snapshot at write time** — never join back to live products for receipts.
4. **Idempotent seeds.** Upserts by natural keys (slug/email/code); extend `seed.ts`, never hand-edit the DB. `createdAt` is create-only — re-ordering the seeded catalog requires a fresh DB.

### 7.5 Guest identity

Carts/wishlists key on **192-bit random cookie tokens** (`randomBytes(24).toString("hex")`, httpOnly). Reads never mint rows; mutations resolve the guest token from the cookie **inside** the action (passing an unresolved token minted a fresh cart per request in one source repo — §13.E4 family). Login MERGES the guest rows into the user's rows: the merge is planned by a pure function (quantity-max union, stock-clamped) and applied as ONE transaction with idempotent final-quantity upserts — a retried merge can never double-count.

---

## §8. Security Architecture

### 8.1 Auth & sessions

- **Passwords**: scrypt (N=16384, r=8, p=1, 64-byte key — OWASP interactive baseline), stored as `scrypt$N$r$p$saltB64$hashB64`.
- **Hash selection rule**: scrypt for low-entropy passwords; **SHA-256 for high-entropy token lookups**. A salted scrypt digest can NEVER be a lookup key (same input → different digest every call — one source repo proved this the hard way).
- **Sessions are DB rows.** Cookie = `<token>.<hmac>`: 256-bit random token, stored **hashed (SHA-256)**; HMAC (keyed by `AUTH_SECRET`) is integrity-in-depth; comparisons via `timingSafeEqual`. httpOnly, SameSite=Lax, Secure in production.
- **Rotation**: password change revokes all other sessions; logout deletes the row; expired sessions swept opportunistically on login plus a scheduled sweeper.
- **Anti-enumeration is a UX contract, not just a crypto one**: login failures return ONE uniform message ("Invalid email or password."), and an unknown account **burns a dummy scrypt verify so timing matches** a real check. Password reset never reveals whether the email exists.

### 8.2 Rate limiting — inventory + the clientIp rule

In-memory fixed-window limiter: `rateLimit(key, limit, windowMs) → { ok, retryAfterSec }` with TTL eviction (an un-evicting Map is an unbounded leak), `Retry-After` on 429s, and a **swap point for a shared store** documented for scale-out.

**The clientIp rule (learned from a real High-severity defect):** server actions CAN read request headers — `await headers()` from `next/headers` works in actions. **Never** derive the client identity from `clientIp(new Headers())`: an empty Headers object collapses every visitor into ONE bucket per key, turning guest checkout limits into a site-wide cap (~10 orders / 10 min for everyone) and login limits into a per-email global lockout any attacker can trigger. Route handlers pass the real `request.headers`; server actions read `await headers()`. Behind a proxy, gate `x-forwarded-for` trust on `TRUST_PROXY`.

**Metered-surface inventory** (key on BOTH attacker-choosable identity and IP; size so humans and the e2e suite are unaffected):

| Surface | Floor (shape) |
|---|---|
| `loginAction` | 10/min per email **plus** 30/min per IP (email key alone is attacker-chosen; every attempt burns real scrypt CPU) |
| `registerAction` | 5/min per email + 30/min per IP |
| password-reset request | 10 / 15 min per email+IP |
| `submitReviewAction` | 5/min per IP+product+author |
| checkout placement | 10–20 / 10 min per IP |
| payment-intent creation | 10 / 10 min per IP |
| newsletter, contact | 5/min per IP |
| coupon apply | 30/min per IP |
| cart/wishlist writes (guest-reachable) | 60/min per IP |
| search typeahead | 60–120/min per IP |
| order tracking lookup | 30/min per IP |

Every unauthenticated write seam is metered. Registration included — an un-metered register action was a real finding.

### 8.3 CSP & platform headers

- **Per-request nonce CSP** via `src/proxy.ts` (Next 16's middleware): stamp the nonce on REQUEST headers (Next applies it to the scripts it renders) AND on the response (browser enforcement). Pure directives in `lib/csp.ts`, unit-pinned; env-conditional `'unsafe-eval'` for dev only; production stays byte-identical.
- **Prerender trap**: a prerendered page bakes no/build-time nonces → browser silently refuses scripts → **silent non-hydration with zero console errors**. Fix: `await connection()` in the layout (§13.B3).
- Platform headers from `next.config.ts`: Referrer-Policy, `X-Content-Type-Options: nosniff`, HSTS (includeSubDomains), `X-Frame-Options: DENY`, Permissions-Policy (disable camera/mic/geo/payment), COOP; `poweredByHeader: false`.
- `img-src` must list only origins you control — pinning it to an external CDN couples your availability to someone else's (§18.4).

### 8.4 Access control — the wall inventory

| Wall | Rule |
|---|---|
| IDOR owner-walls | Addresses, cart lines, wishlist, order detail: every query filtered by `session.user.id` — re-checked **inside the action**, never only in the page guard. |
| Admin role-wall | `requireAdmin()` is the FIRST line of every admin action + the admin layout check. Client checks are UX only. |
| Guest order access | Sequential order numbers are **identifiers, not capability tokens**. Public tracking requires number + purchase email (same "not found" shell for wrong-email/unknown-number — no enumeration oracle). Receipt pages render full PII only for a valid `order` + **HMAC capability token** pair; everything else renders the same locked shell; page is `noindex`. |
| Enumerable IDs | Any sequentially-numbered public object needs a second unguessable factor or an ownership check — the general law. |

### 8.5 Boundary discipline

- **Zod at every boundary** — all server actions, all POST/PATCH bodies. Malformed JSON → **400**, never 500. The two documented read-only exceptions (query-string search, ownership-scoped delete params) must be justified in place.
- **Error surfaces**: `error.tsx` + `global-error.tsx` render the branded error card; keep them dependency-free. Actions never throw across the seam — they return `ActionResult` failures with generic user messages and tagged server logs (`console.error("[actionName]", e)`).
- **Output safety**: zero `dangerouslySetInnerHTML` except JSON-LD through the escaping serializer; admin-supplied links accept only internal paths or `https:` URLs.
- **Secrets**: boot-time guard refuses production start without a real `AUTH_SECRET`; `.env` never committed; **no key material in docs, ever** (§18.3).

---

## §9. Checkout, Payments & Order Lifecycle

### 9.1 The money path (one transaction, everything re-derived)

`placeOrder` (server action or `/api/checkout`) executes, inside ONE Prisma interactive transaction:

1. **Re-read the cart** from the DB by resolved identity (guest cookie token or user).
2. **Re-read prices from live `Product` rows** — never trust what the cart page displayed.
3. **Re-validate the coupon** (active, unexpired, under `maxRedemptions`); increment `timesUsed` atomically with the guard in the `where`.
4. **Reserve stock atomically** per line: conditional `updateMany` with `stock: { gte: qty }`; `count === 0` → 409 with the live cap (rollback on any later failure).
5. **Derive totals** via pure `computeOrderMoney` from the re-read snapshots.
6. **Write Order + OrderItems (snapshots) + `placed` OrderEvent + idempotency row** — all in the same transaction.
7. **Empty the cart** in the same transaction; respond `{ orderNumber, token }`; mint the HMAC receipt token.

Zero-quantity ghost lines can never reach checkout: clamping to 0 **deletes the line**; the checkout re-filter backstops with 409. The client never sends an amount — the demo variant accepts only `cardLast4`.

### 9.2 Payment gateway blueprint (Stripe reference implementation)

Env-gated: absent keys → clearly-labeled demo step (§1 demo honesty). Present keys → the full stack below. All of it was production-audited in the strongest-payments source repo:

1. **Payment Element island** (client) created from a **server-minted PaymentIntent** with a deterministic idempotency key (`order.<orderNumber>.<attempt>`). The client SDK imports its **lazy entry** (`@stripe/stripe-js/pure`) — the default entry eagerly injects `js.stripe.com` at module scope, turning "off" into a lie.
2. **Verify-then-place gate**: the place-order seam re-retrieves the PaymentIntent server-side, confirms `status === "succeeded"` and **amount === server-derived total**, and only then writes the order. The webhook is the backstop, not the trigger.
3. **Webhook route** (`api/webhooks/stripe`): raw-body HMAC signature verification **before any DB write**; event classification (duplicate / permanent failure / transient failure); the **dedup row commits in the SAME transaction as the side effects it guards** — a pre-committed dedup row + always-200 permanently orphans a captured payment (real defect class, mutation-proven in source).
4. **Failure policy**: deterministic events → record + 200 (stop retries, leave an audit trail); transient → rollback + 500 (let Stripe retry).
5. **Refunds**: full + partial, intent-scoped idempotency keys, **the webhook is the single writer of refund state**; admin payments-ops console lists the StripeEvent log with deep-linkable filters; a refund-needed family filter surfaces at-risk payments.
6. **CSP additions**: `script-src https://js.stripe.com`, `frame-src https://hooks.stripe.com`, `connect-src https://api.stripe.com` — added only when payments are enabled.
7. **Integration tests drive the REAL webhook handler with REAL HMAC-signed events against a scratch DB** (18 cases in the source: placement, refund reflection, dedup, signature rejection). Mocks cannot catch this class of defect.

### 9.3 Order lifecycle

- Statuses: `pending → processing → shipped → delivered`; `cancelled` reachable while not terminal; **cancelled + delivered are terminal** (pure `canTransitionOrderStatus`, unit-tested).
- Moving a live order to `cancelled` **restocks every item inside the same admin transaction, exactly once** (`shouldRestockOnStatusChange`).
- Every status change mints an `OrderEvent`; admin notes carry `actor: "admin"` and never render in customer timelines.
- Carrier + tracking number are admin-gated writes with a discriminated-union view; tracking lookups are rate-limited and anti-enumerated (§8.4).

### 9.4 Email — the console seam

Until a provider is wired, every outbound message (order confirmation, verification code, reset link) logs through one tagged seam (`[email:stub]`), and verification-gated flows stay env-OFF. The seam is the designed extension point: swap the seam's transport, flip the env flag, enable the flows — in that order. **Do not enable email-verification gates before the provider exists** (users would be stranded) and do not let legal pages promise emails the system cannot send.

---

## §10. Admin Back Office

The admin is a complete back office, not a viewer — a store without product CRUD is not operable (this exact gap sank a source repo's template score):

- **Products**: full CRUD + visibility toggle + stock adjust + featured/new flags. Image URLs validated (`imageUrlSchema`); an upload pipeline is the documented next step (object storage + signed uploads).
- **Categories**: CRUD with guarded delete (refuse while products reference it).
- **Coupons**: CRUD + activation + redemption counters (atomic-cap reads).
- **Carousel / content**: slide CRUD with internal-or-https link validation.
- **Orders**: status transitions (terminal-state rules), tracking writes, cancel-restock, refunds (via the PSP seam when wired).
- **Analytics**: SQL day-bucket revenue, top products, **true-count low-stock KPI** (a real `count`, not a `take`-capped list — a take-capped list under-reports exactly when it matters).
- **Settings**: the KV store (shipping rates, tax rate, thresholds, legal contact) with a schema-checked admin form.

Every admin action starts with `requireAdmin()`. URL-deep-linkable filters on list views (`?status=refund-needed&range=7d`) — operators live in bookmarks. Admin pages share the storefront chrome but never nest a second `<main>`.

---

## §11. Testing Strategy — the Spec, Not an Afterthought

### 11.1 The three layers

| Layer | Tool | What it pins |
|---|---|---|
| Unit / contract | Vitest (node) | Pure seams: money math, db-path resolution, rate-limit floors, auth-secret guard, coupon eligibility, status transitions, tracking access, validators. Tests are type-checked as their own gate. |
| Real-engine integration | Vitest + temp SQLite files | The actual checkout transaction, stock decrements, coupon-cap increments, guest merges, address caps — against the real Prisma engine on scratch DBs (money-path defects mocks cannot catch). With payments: the real webhook handler + real HMAC events. |
| E2E | Playwright vs the **standalone build** | Behavioral flows, a11y gates, security headers, SEO surfaces, limiter floors. Never the dev server — you must test what you ship. |

### 11.2 E2E discipline (hard-won rules)

1. **E2E validates the last BUILD, not the last edit.** `build` before `test:e2e`, always. After any rebuild, verify the served content actually changed (a renamed `next-server` child process can keep serving the stale bundle; §13.B9).
2. **Hydration-gated navigation** (`gotoHydrated`) — or poll for the React fiber — before interacting.
3. **One login in setup → storageState**; never per-test logins. The rate budget is exactly consumed: failed attempts count too (the limiter consumes on call, before password verification).
4. **Admin-side test state via SQL-minted sessions** (insert a session row + offline HMAC cookie through `prisma db execute`), never extra admin logins.
5. **One worker + shared DB reset discipline**: per-spec clears + global-setup wipe of non-canonical data; **delta assertions, never absolute counts**, on shared fixtures.
6. **Cookie jars are per-host**: `localhost` ≠ `127.0.0.1`; pick one host for the whole run. The Playwright `request` fixture does NOT share the browser context's cookies — use `page.request` or an explicit `Cookie` header.
7. **Assert server truth, not toasts** — the toast-blind silent-failure class is real; after admin writes, re-read from the DB or reload and assert the rendered state.
8. **Exercise every mutation seam** — page-visit tests prove nothing about actions. (A 100%-broken admin action once shipped through typecheck + lint + unit + e2e because no test visited it; §13.F14.)
9. **Scope locators**: `getByRole("main")` on chrome pages; state-stable locators or `aria-pressed` (names that describe state orphan you when state flips); `exact: true` when names collide (substring matching is the default).
10. **Design-contract gates** (if parity pins exist): computed styles as ground truth, geometry bands not pixels-where-animated, font-family census per heading rank, structure-vs-content drift classification.

### 11.3 The mutation-check doctrine

**A gate is only trusted once a mutation has deliberately failed it.** For every new gate: (1) run the zero-violation form first so the baseline is a deliberate contract; (2) re-introduce a real past defect and watch the gate go red; (3) calibrate pinned counts under the gate's own runtime conditions; (4) restore via **inverse edits, never `git checkout`** (§13.F13) and verify the restoration before moving on. Record the red-run in the commit message or session log.

### 11.4 CI

`.github/workflows/ci.yml` runs: `verify` (typecheck, lint, unit, build) + `test:e2e` + the standalone smoke (`start` + `/api/health`). Cache node_modules and the Playwright browser. Every push. No gate exists until it runs somewhere you don't control.

---

## §12. SEO, Accessibility & Performance

### 12.1 SEO surfaces

- `sitemap.ts` + `robots.ts` as dynamic routes reading the live catalog; canonical origin from `NEXT_PUBLIC_SITE_URL`.
- **Metadata merges SHALLOWLY per segment** — a child `openGraph`/`twitter` object REPLACES the root's wholesale. Symptom family: "one page's share card missing fields every other page has." Re-declare site-level fields in per-page overrides (§13.B8).
- **`public/` statics shadow app routes**: a scaffolded `public/robots.txt` answers before `robots.ts` forever. Assert route **bodies** (origin, shape, counts), never just status codes; `git rm` stale statics (§13.B7).
- JSON-LD (Organization, WebSite, Product with `offers.price` in **decimal USD**, BreadcrumbList) through an HTML-safe serializer escaping `<`, `>` and U+2028/2029. Render site-level data blocks **outside `<main>`**.
- Per-product OG images; `opengraph-image.png` file convention for the default card. Receipt/tracking pages: `noindex`.

### 12.2 Accessibility (the load-bearing rules)

- Semantic landmarks; exactly one `<main>` per page, owned by the layout. Skip-to-content link as the first chrome element, revealed on focus, targeting `<main id tabIndex={-1}>`.
- Radix primitives carry the ARIA weight for dialogs/selects/tabs — don't hand-roll; every hand-rolled dialog installs the focus trap on open and returns focus on close.
- Icon-only buttons: `aria-label` **composed from the same state the badge renders** (`Cart, 3 items` — an empty-cart audit can never see the badge-count failure; audit stateful surfaces with self-cleaning fixtures).
- `aria-hidden` does NOT remove descendants from tab order — pair with `inert`.
- `prefers-reduced-motion` global media query pinning every animation/transition to 0.01ms.
- Form errors in `p[role=alert]` scoped per field (Next's route announcer also carries `role=alert` — never query it bare).
- axe gates over the real surfaces, both viewports: placeholders can mask label defects (axe accepts placeholder as last-resort name — label mutations must also strip the placeholder); visible state words must fold into accessible names (WCAG 2.5.3 Label-in-Name).

### 12.3 Performance

- The motion budget (§4.1) is the performance policy at this scale; self-hosted fonts with preload (`crossorigin` even same-origin); optimized images from origins you control.
- Everything data-touching is per-request (nonce CSP requires it anyway). If you later add caching/ISR, reconcile it with the nonce contract explicitly — that tension is a known open design point of this architecture family.
- If you add CWV/INP gates: PerformanceObservers must be injected pre-paint (`page.addInitScript`); interaction metrics require **trusted clicks only** (synthetic `el.click()` generates zero interaction entries); pin observer thresholds explicitly (`durationThreshold: 0` — the 16ms default hides fast interactions).

---

## §13. The Trap Log (consolidated registry)

Distilled from ~82 raw entries across the three source skills, deduplicated and generalized. Format: **name — symptom / root cause / fix.** Add every new trap here (and in an in-file comment at the point of temptation) when you hit it. Severity markers reflect observed blast radius in the source repos.

### 13.A Tailwind v4

| # | Trap |
|---|---|
| A1 | **Bare HSL triplets in `@theme inline`** — elements invisible, colors render transparent / v3-style `30 15% 97%` tokens silently resolve to transparent under v4 / always write full `hsl(...)` literals. Hit independently in all three source repos. |
| A2 | **`space-y-*` geometry changes** — auth cards a few px short per field; mobile menu rows collapse / v4 emits `margin-block-end` on non-last children via `:where()` — inert when the first child is inline; selector specificity dropped / stack with `flex flex-col gap-N`; give the first block wrapper `mt-2`; Tabs roots carry no `space-y-*`. |
| A3 | **Display-utility JS toggle** ("THE mobile-nav bug") — menu opens once then never again, or flashes / v4 changed display-utility generation order; preflight `[hidden]` is `!important` / never JS-toggle `hidden`/`flex` on the same element — **mount overlays conditionally via React state** (`if (!open) return null`). |
| A4 | **Shadow + radius scale shift** — cards/buttons 4px-off radii, heavier shadows / v4 moved both scales one notch / pin `--shadow-sm` and the radius scale in `@theme`. Never "fix" toward v4 defaults. |
| A5 | **Nested `@keyframes` never ship** — `animate-*` applies but `animation-name` computes `none` / `@theme inline` does not emit nested keyframes / keyframes live at the TOP LEVEL of globals.css; only `--animate-*` mappings belong in the theme. |
| A6 | **Default palette serializes oklab** — a pin like `backgroundColor === "rgb(239,68,68)"` fails with `lab(...)` though the paint is right; `rounded-full` computes `calc(infinity*1px)` not `9999px` / v4 serializes its default palette in oklab / assert TOKEN identity via probe elements, never serialization strings. Own `hsl()` tokens are unaffected. |
| A7 | **Hover gated behind `(hover:hover)`** — hover styles don't render in touch/hybrid contexts / v4 media-gates the variant / add `@custom-variant hover (&:hover);`. |
| A8 | **Grid items stretch by default** — a button that's `sm:w-fit` goes full-width on mobile / grid stretch semantics + a desktop-only constraint / reproduce the real anatomy: the button is a flow child OUTSIDE the grid with `mt-4`; audit mobile viewports separately from desktop. |
| A9 | **Base `leading-*` beats responsive `text-*`** — hero line-heights wrong at breakpoints / cascade order / pin responsive line-heights explicitly (`sm:leading-[2.5rem] lg:leading-none`). |
| A10 | **A `tailwind.config.js` appears** — behavior diverges from the CSS-first theme / someone "helpfully" added it / v4 is CSS-first; adding the config file is a bug. Remove it. |
| A11 | **Fresh arbitrary utility doesn't apply in dev** — the new class silently does nothing / dev-server CSS staleness after adding utilities / restart dev; when debugging markup, rebuild before concluding anything. |

### 13.B Next.js 16 / standalone

| # | Trap |
|---|---|
| B1 | **Standalone serves zero-hydration pages** — perfect SSR HTML, clicks inert, `Unexpected token '<'` / `output: "standalone"` does NOT copy `.next/static` + `public/` into the bundle / the build script must run the assemble step (copy both dirs); verify `.next/standalone/.next/static` exists; always build through the wrapper. |
| B2 | **Relative `DATABASE_URL` re-anchored inside the standalone bundle** — e2e webServer Prisma can't open the DB / file tracing copies `schema.prisma` into `.next/standalone`, re-anchoring `file:../db/…` to a nonexistent path / use an absolute `file:` path in the e2e webServer env (absolute URLs pass through db-path untouched). |
| B3 | **Prerendered page + per-request nonce = silent non-hydration** — page loads, paints, never hydrates, ZERO console errors / prerendered pages bake no (or build-time) CSP nonces; the browser silently refuses scripts / `await connection()` in the layout — `force-dynamic` alone did NOT de-prerender in Next 16.4. Debug the rendering mode (`x-nextjs-prerender` header), not the JS. |
| B4 | **`revalidatePath` racing a checkout redirect** — freshly-emptied cart bounces back to /cart / broad revalidation races the success navigation on all-dynamic routes / redirect-returning actions omit `revalidatePath`; the client store resets from the action response. |
| B5 | **CSP not env-conditional** — console CSP violations, half-hydrated dev pages / React dev builds need `'unsafe-eval'`; production must never carry it / build the policy from `NODE_ENV`, production byte-identical. |
| B6 | **Auth actions must `redirect()` server-side** — `?redirect=X` logins flakily land on /account or /login / the action response re-renders the CURRENT route; a client `router.push` races the server guard redirect riding in the payload / success paths call `redirect(...)` in the action; failure paths return the envelope. |
| B7 | **`public/` statics shadow app routes** — `/robots.txt` answers with a foreign body while the whole suite stays green / static files win over route handlers / `git rm` stale statics; assert route BODIES, never just 200s. |
| B8 | **Shallow metadata merge + engine gap-filling** — one page's OG card missing site fields; surprise `twitter:card` / PWA meta appears / child `openGraph`/`twitter` objects REPLACE the root's wholesale; the metadata engine force-defaults fields it can derive / re-declare site-level fields per page; use the typed twitter field deliberately; inexpressible shapes render plain `<meta>` in the page body (React 19 hoists them). |
| B9 | **Standalone server renames itself + stale adoption** — killing by original name fails; EADDRINUSE after rebuild; tests validate a pre-rebuild bundle / the process becomes `next-server (vN)`; `reuseExistingServer` adopts ANY listener / kill by port or PID (`ss -ltnp`); after any rebuild, verify the SERVED CONTENT changed, not just that the port answers. |
| B10 | **`middleware.ts` → `proxy.ts`** — middleware never runs / Next 16 renamed the convention / file is `src/proxy.ts`, exported function `proxy`; set the CSP nonce on request AND response headers. |
| B11 | **Dev-origin protection blocks the app on 127.0.0.1** — native form fallbacks, unhydrated pages / Next 16 dev-origin allowlist / `allowedDevOrigins: ["127.0.0.1", "localhost"]` in next.config. |
| B12 | **`.env` copied into standalone at build time** — prod server ignores your env edits / the build snapshots `.env` into the bundle / rebuild after env changes. |
| B13 | **Client component imports a server-only module** — Turbopack build failure / `lib/cart.ts` pulls `next/headers` + Prisma / split pure DTOs into `-dto.ts`; the client imports types from the pure file only. |

### 13.C Prisma / SQLite / data

| # | Trap |
|---|---|
| C1 | **Environment shadowing of `DATABASE_URL`** — DB never appears at the repo root; rows survive "fresh" reseeds / a `DATABASE_URL` already in process env (shell export, CI inject, parent `.env` — Bun walks up) WINS over the repo `.env`; Prisma never overrides existing env / diagnose empirically: `node -e "console.log(process.env.DATABASE_URL)"`; run DB commands as `env -u DATABASE_URL <cmd>`; converge stray paths with symlinks. Hit in all three source repos. |
| C2 | **Simplifying `db-path.ts`** — CLI and runtime open different DB files / the schema-relative resolution rule is subtle and load-bearing / the module is pinned by unit tests; do not simplify it. |
| C3 | **Stale dev server after reseed** — every write fails `SQLITE_READONLY` (code 1032) / `db:setup` replaced the DB file; the long-lived process holds the old inode / restart the server; remove orphaned `-journal`/`-wal`/`-shm` first. |
| C4 | **Prisma 6 SQLite DateTime = INTEGER epoch ms** — raw-SQL `datetime()`/`strftime()` fixtures are INVISIBLE to Prisma `lt/gte` DateTime filters (SQLite cross-storage-class ordering puts INTEGER < TEXT always) / every raw-SQL fixture datetime writes `strftime('%s','now',±N)*1000` — integer ms, Prisma's own format. |
| C5 | **P2002 handling** — registration crashes on duplicate email; order placement loses the race / unique-constraint violations are signals, not errors / map `P2002` to the friendly message (register); on `idempotencyKey` collisions, fetch and return the winner. |
| C6 | **P2025 on racing writes** — double-tap remove/± throws a raw 500 / the record vanished between pre-check and write / write atomic `{ increment: delta }` with post-corrections (delete ≤ 0, clamp to stock); catch record-not-found → re-read DTO → return `ok` (the desired end-state already holds). |
| C7 | **Check-then-act across an await** — stock oversell, coupon over-redemption / the race window between validation and write / fold the guard into the WHERE of a single conditional write (`updateMany` + count check). Applies to every "validate then write" pair. |
| C8 | **Zero-quantity ghost lines** — checkout "buys" a $0 line / clamping `Math.min(qty, stock)` to 0 and persisting it; the `stock < quantity` guard passes for `0 < 0` / clamp-to-0 means DELETE the line; checkout backstops with a 409 filter. |
| C9 | **`createdAt` is create-only** — re-ordering the seeded catalog does nothing / idempotent upserts never rewrite existing rows / fresh DB (`db:reset`) to re-order; never hand-edit. |
| C10 | **SQLite has no enums** — schema drift between DB vocabulary and code / string columns + `as const` vocabulary arrays in `validation.ts`, Zod-checked at every seam. |

### 13.D Server actions / React 19

| # | Trap |
|---|---|
| D1 | **Throwing across the seam** — unhandled 500s in production paths / actions are RPC, not exceptions / every action returns `ActionResult<T>`; failures carry `error.message` (+ `fieldErrors`); the catch logs with a `[tag]`. |
| D2 | **`FormData.get()` returns `null`; `z.optional()` rejects `null`** — every optional-field order fails Zod / absent form fields are `null`, not `undefined` / coerce `?? undefined` at the seam for every optional key. |
| D3 | **Wizard state held in the DOM** — step-2 validation can never see step-1 values / the step's inputs unmounted; `getElementById` returns null / values needed across steps live in React state. |
| D4 | **`setState` inside effects** — lint error, re-render churn / `react-hooks/set-state-in-effect` is an ERROR under React Compiler-era rules / adjust-state-during-render, derived state, or `useActionState` (§6). |
| D5 | **`useSyncExternalStore` snapshot not cached** — "getSnapshot should be cached" warning, render loops / re-deriving from a clock on every call can cross a boundary between React's reads / cache the snapshot per tick; invalidate on interval fan-out. |
| D6 | **`useState` props are initial values only** — stale cart badge after `router.refresh()` delivers new props / the component never re-reads the fresh prop identity / last-seen-props re-sync in render (state, not ref, not effect). Logout must call `setUser(null)` — the provider outlives client navigation. |
| D7 | **`clientIp(new Headers())` in server actions** *(real High-severity defect)* — every visitor shares one rate-limit bucket: guest checkout capped site-wide (~10 orders/10 min for ALL customers), login lockout per-email triggerable by anyone / an empty Headers object always yields the fallback identity; the in-code myth "actions can't read headers" is FALSE — `await headers()` works / read `await headers()` in actions; pass `request.headers` in route handlers; pin limiter floors with wire-level tests. |
| D8 | **Un-metered write seams** — register action (or any new unauthenticated write) becomes an abuse vector / rate-limit inventory wasn't extended with the feature / every unauthenticated write seam is metered, keyed on both identity and IP (§8.2 table). |
| D9 | **React 19 resets action-submitted forms** — uncontrolled inputs clear after every submission / React 19 form-reset semantics / make action-affected inputs controlled, or accept and re-fill in tests. |
| D10 | **`session` persistence across navigation** — logged-in header after logout / route-group layout keeps the provider mounted / expose and call `setUser(null)` in the logout action path. |

### 13.E Security & commerce domain

| # | Trap |
|---|---|
| E1 | **Sequential IDs as an authz decision** — PII leak via guessable order numbers / a public identifier is not a capability / number + purchase email for public tracking; HMAC capability token for receipts; identical locked shells for every failure mode (no existence oracle). |
| E2 | **Anti-enumeration without timing parity** — attackers time the login response / uniform messages alone leak via scrypt-vs-nothing / burn a dummy scrypt verify for unknown accounts. |
| E3 | **scrypt as a lookup key** — `findUnique({ where: { tokenHash: scryptHash(t) } })` never matches / scrypt salts per call → same input, different digest / SHA-256 for high-entropy token lookups; scrypt only for low-entropy passwords. |
| E4 | **Client-trusted totals or unresolved guest tokens** — forged prices; a fresh guest cart per add / the boundary trusted the client / re-derive all money server-side in the transaction; resolve guest identity inside the mutation. |
| E5 | **Single-seam stock enforcement** — orders succeed against zeroed stock / UI-only enforcement / three seams: PDP stepper cap → `clampToStock` on cart mutations → in-transaction rejection + atomic decrement. Each layer catches what the ones above cannot. |
| E6 | **Dedup row committed before side effects** — a captured payment is permanently orphaned / pre-committed dedup + always-200 stops retries while the write never lands / the dedup row lives in the SAME transaction as the side effects; failure policy separates deterministic (record + 200) from transient (rollback + 500). |
| E7 | **Password rotation leaves sessions alive** — compromised sessions survive a password change / no revocation rule / revoke all other sessions on password change. |
| E8 | **Rate-limit Map never evicts** — unbounded memory growth / fixed-window buckets accumulate forever / opportunistic stale-bucket sweep on each call; design the shared-store swap point. |
| E9 | **JSON-LD injection + price format** — `</script>` breakouts; `offers.price` in cents / unescaped serialization; unit confusion / escaping serializer (`<`, `>`, U+2028/29); decimal USD via `price/100`. |
| E10 | **CSP `img-src` pinned to an external CDN** — product imagery availability depends on a third party (and rebranding breaks it) / seed URLs point at the cloned reference's CDN / self-host assets; update CSP and seed together. |

### 13.F Playwright / test harness

| # | Trap |
|---|---|
| F1 | **E2E validates the last BUILD, not the last edit** — a verified fix "doesn't work" under e2e / the webServer serves the standalone bundle; source edits are invisible until rebuild (and `reuseExistingServer` keeps serving the stale one) / ritual: build → then e2e; after rebuild, verify served content changed. |
| F2 | **Pre-hydration clicks do nothing** — clicks "succeed" but state never changes (flaky, passes on retry) / the click landed before hydration; the SSR node has no fiber / `gotoHydrated`; or poll `__reactFiber$` expanders before interacting; `waitForLoadState("networkidle")` after `goto` into islands. |
| F3 | **Per-test logins** — mid-suite 429s; later specs see "Sign in" / the auth rate budget is exactly consumed (failed attempts count too); a logout spec destroyed the shared session / ONE login in setup → storageState; per-project auth files; logged-out specs opt out explicitly. |
| F4 | **Shared-DB drift** — spec A's orders push fixtures out of take-capped lists; run 2 fails where run 1 passed / shared SQLite + accumulating writes / 1 worker; per-spec clears; global-setup wipes non-canonical data; assert canonical fixtures only after reset; **delta assertions, not absolute counts**. |
| F5 | **Cookie jars are per-host; `request` fixture is identity-isolated** — large pixel diffs on authed routes (auth failed, not drift); API fixtures carry no session / cookies don't cross `localhost`↔`127.0.0.1`; the `request` fixture creates a fresh context (it DOES apply project storageState — but not the browser context's runtime cookies) / pick ONE host; read the session cookie from `context.cookies()` and send it explicitly, or use `page.request`. |
| F6 | **Name matching is substring by default** — strict-mode 2-element resolution on "plausible" names / Playwright's default matcher / `exact: true`; scope to region (`getByRole("main").getByRole(...)`) because exit animations leave portal remnants ~500ms in the DOM. |
| F7 | **`getByText` matches DOM text** — locator on visually-uppercase "SIZE" finds nothing / CSS `text-transform` is invisible to locators / case-insensitive regex (`/^size$/i`) when casing comes from CSS. |
| F8 | **`toBeVisible()` is clipping-blind; aria-hidden keeps tab order** — hidden interactive content passes visibility checks and stays tabbable / visibility ≠ hit-testing; `aria-hidden` removes from a11y tree, not tab order / assert rect + hit-test; pair `aria-hidden` with `inert`. |
| F9 | **axe blind spots** — placeholder masks label defects; badge-count and state-word label mismatches invisible in empty/unstateful audits / axe accepts placeholder as last-resort name; Label-in-Name needs visible text folded in / audit STATEFUL surfaces with self-cleaning fixtures; scroll before scanning (axe skips invisible text). |
| F10 | **CSP nonce hidden after parsing** — `getAttribute("nonce")` returns null though the page works / browsers move parser-created nonces into an internal slot / assert the SERVED BYTES (`response.text()` matching `nonce="<headerNonce>"`); harness script injection needs `bypassCSP: true`. |
| F11 | **Mutation-demo restore hazards** — the "restored" file goes RED or the mutation survives unnoticed / `git checkout <file>` reverts ALL uncommitted work in it; on untracked files it's a SILENT NO-OP (pathspec error swallowed by `\|\| true`) / restore via INVERSE edits (sed/patch); `rg` the original value and re-run the touched test before moving on. |
| F12 | **Synthetic events don't count** — INP protocol shows zero interactions; CSS `:hover`/`onMouseEnter` never fire / `interactionId` and CSS state activate only on trusted input-pipeline events / Playwright locator clicks/keyboard only; script `.focus()` never trips `:focus-visible` (use real Tab). |
| F13 | **Vacuous pins** — `getByText("FREE")` matches "Free shipping" case-insensitively; a passing test proves its assertion, not the feature / loose matching; asserting intermediates / scope pins to the actual row/element; assert the OBSERVABLE. |
| F14 | **DOM globals shadow server code** — a server action compiles clean, then 500s `ReferenceError: status is not defined` (shipped 100%-broken through typecheck+lint+unit+e2e) / TS `lib: ["dom"]` declares legacy globals (`status`, `name`, `origin`, `event`, `close`...) so bare identifiers COMPILE in server code and throw in Node / ESLint `no-restricted-globals` errors on the DOM globals; an e2e must exercise EVERY mutation seam — page-visit tests prove nothing about actions. |
| F15 | **`getComputedStyle` lies by omission** — `flexDirection` returns "row" (the initial value) for every element; `scale-*` sets the `scale` property not `transform` / initial values and renamed properties / locate the STRUCTURAL container (the testid's parent); assert the property that actually changed. |
| F16 | **Viewports are exact** — `devices["iPhone 14"]` is 390×664 not 844; desktop-only a11y gates skip `display:none` content / descriptor assumptions; axe skips invisible elements / calibrate at the exact descriptor; engineer viewport-specific mutations for viewport-specific gates. |

### 13.G Tooling & process

| # | Trap |
|---|---|
| G1 | **Gates must run on the FINAL tree** — every fresh clone fails `verify`; the author never saw it / a tool script was committed after the last lint run / re-run the full gate chain as the LAST step before commit whenever a session adds a committed file mid-flight. |
| G2 | **`execSync` shell-expands `$`** — child dies `SyntaxError: Unexpected token '('` on `p.$disconnect()` looking like a Prisma bug / the command string went through a shell; `$disconnect` expanded to empty / `spawnSync(cmd, [args-array])` — ARGV, not shell text. |
| G3 | **Health-green is not liveness** — a dead child + a foreign 200 passed the health check / the death event (~50ms) lost the race to the foreign response (~10ms) / race a death-promise against a grace window; every retry loop needs a per-request deadline. Same family: "measure the wrong thing confidently." |
| G4 | **Long-lived dev server across `db:setup`** — SQLITE_READONLY on every write / inode replacement (C3) / restart the server after reseeding. |
| G5 | **`import.meta` in Playwright global-setup** — "Cannot use import statement outside a module" / TS compiled as CJS / `process.cwd()`-based paths. |
| G6 | **Network-dependent builds** — hermetic CI breaks on Google Fonts / runtime font CDN / self-hosted woff2 in `public/fonts/`. |
| G7 | **Font parity is file parity** — measurable rasterization drift between "same" fonts / `next/font` repackaging strips the `prep` hinting table / self-host the exact woff2 bytes under your family name via plain `@font-face`. |
| G8 | **Docs drift = code drift** — docs claim gates the config disabled; counts stale / docs updated "later" / same-commit doc updates for every pinned-contract change; docs counts must match the suites (a 27-vs-19 e2e-file drift was a real finding). |
| G9 | **Committed baggage & secrets** — 192 MB of unrelated skills + a restorable SSH key + reference-site credentials in one source family; 86% of tracked files were not the app / personal tooling and session archives committed alongside the product; a "redacted" key body is still a key / §18 exists for this: LICENSE, slim tree, no key material, history hygiene. |
| G10 | **Working around a pin whose reason you don't know** — a "cleanup" silently regresses a measured contract / pins encode forgotten evidence / read §13 first; if a pin blocks you, re-measure and update the pin IN A COMMIT — never delete it quietly. |

---

## §14. Debugging Guide (symptom → cause → fix)

| Symptom | Likely cause | Play |
|---|---|---|
| Page paints but never hydrates, zero console errors | Prerendered shell vs per-request CSP nonce (B3) | Check `x-nextjs-prerender` header; add `await connection()` to the layout. |
| SSR HTML perfect, clicks inert, `Unexpected token '<'` | Standalone bundle missing client assets (B1) | Run the real `build` (assemble step); verify `.next/standalone/.next/static`. |
| Mobile menu unreliably opens/closes | Display-utility JS toggle (A3) | Conditional mount; run the mobile-nav regression spec. |
| Elements invisible / transparent backgrounds | Bare HSL triplet (A1) | Full `hsl()` literals in `@theme inline`. |
| Auth cards a few px short per field | `space-y-*` inline-first-child (A2) | `flex gap` stacks; `mt-2` on the first block wrapper. |
| DB file never appears / reseeds keep old rows | Env shadowing (C1) | `node -e "console.log(process.env.DATABASE_URL)"`; `env -u DATABASE_URL`. |
| Every write fails `SQLITE_READONLY` 1032 | Stale process over a reseeded inode (C3) | Kill server, remove `-journal/-wal/-shm`, restart. |
| E2E clicks do nothing; native GET in URL | Pre-hydration click race (F2) | `gotoHydrated`; fiber poll; `networkidle`. |
| Fix verified in dev but e2e still fails | Stale standalone bundle (F1/B9) | Rebuild; verify served content changed. |
| COD/optional-field orders always fail Zod | `FormData.get()` null vs `optional()` (D2) | `?? undefined` coercion at the seam. |
| Card payment can never pass Luhn | Wizard state held in the DOM (D3) | Move step values into React state. |
| Login flakily lands on /account or /login | Client push racing action re-render (B6) | Server-side `redirect()` on success paths. |
| Double-tap remove/± throws P2025 | Line vanished mid-flight (C6) | Atomic increment + record-not-found catch → `ok` + fresh DTO. |
| Orders succeed against zeroed stock | Single-seam enforcement (E5) | Three-seam stock discipline; in-tx rejection. |
| Guest cart empties / fresh cart per add | Identity resolved outside the mutation (E4) | Resolve the guest token inside the action. |
| Rapid stepper clicks land +1 not +2 | Absolute-quantity lost-update race | Post **deltas** to a transactional `changeQuantityBy`. |
| Cart badge stale after order | Props-are-initial-values (D6) | Last-seen-props re-sync in render. |
| Logged-in header after logout | Provider survives navigation (D10) | `setUser(null)` in the logout path. |
| Toast throws during SSR / no toasts render | Toaster is a sibling of `{children}` | Toaster must be an ANCESTOR in the root layout. |
| Mid-suite 429s on login | Per-test logins (F3) | One setup login → storageState; SQL-minted admin sessions. |
| E2E run 2 fails where run 1 passed | Shared-DB drift (F4) | Global reset; per-spec clears; delta assertions. |
| Large pixel diffs on ALL authed routes | Cross-host cookie jar (F5) | Pick one host for the whole run. |
| Server action compiles clean, 500s `ReferenceError` | DOM global shadowing in server code (F14) | `no-restricted-globals` lint; destructure/import explicitly. |
| `animation-name` computes `none` | Keyframes nested in `@theme inline` (A5) | Move `@keyframes` to top level. |
| New admin-login test starves later logins | Exactly-consumed rate budget (F3) | SQL fixtures; never log in canonical users per-test. |
| Wrong-email and unknown-number tracking differ | Enumeration oracle (E1) | Identical "not found" shells; case-insensitive email match. |
| Prod server ignores env changes | `.env` snapshotted into standalone (B12) | Rebuild. |
| One page's OG card missing site fields | Shallow metadata merge (B8) | Re-declare site-level fields in the child override. |
| `/robots.txt` serves a foreign body | `public/` static shadows the route (B7) | `git rm` the static; assert route bodies. |
| Fresh clone build exits 1 (`cp: public`) | Untracked `public/` artifact | `mkdir -p public` in build + committed `.gitkeep`. |
| Prod boot refuses to start (AUTH_SECRET) | The secret guard | Set a real `AUTH_SECRET`; that's the guard working. |
| Sweeper deletes nothing after SQL fixtures | DateTime storage-class mismatch (C4) | Integer epoch-ms fixtures. |

---

## §15. Coding Patterns (canonical, with code)

### 15.1 The ActionResult envelope

```ts
export type ActionResult<T> =
  | { ok: true; data: T }
  | { ok: false; error: { message: string; fieldErrors?: Record<string, string> } };
```

### 15.2 The server-action shape (EVERY mutation)

```ts
export async function someAction(input: unknown): Promise<ActionResult<Thing>> {
  const parsed = schema.safeParse(input);            // 1. Zod at the boundary
  if (!parsed.success) {
    return { ok: false, error: { message: "...", fieldErrors: zFieldErrors(parsed.error) } };
  }
  try {
    const data = await domainOperation(parsed.data); // 2. domain layer (authz + tx inside)
    revalidatePath("/wherever");                     // 3. targeted revalidation (skip if redirecting)
    return { ok: true, data };
  } catch (e) {
    console.error("[someAction]", e);                // 4. tagged log + never throw
    return { ok: false, error: { message: "Something went wrong. Please try again." } };
  }
}
```

### 15.3 Conditional-mount overlay (the v4-safe pattern)

```tsx
export function MobileNav() {
  const { mobileNavOpen } = useStore();
  if (!mobileNavOpen) return null;   // the whole trick — never toggle `hidden`
  return <div data-testid="mobile-menu">…</div>;
}
```

### 15.4 Zod boundary + FormData null coercion + rate limit

```ts
const parsed = schema.safeParse({
  email: fd.get("email"),
  cardNumber: fd.get("cardNumber") ?? undefined,   // null → undefined for optional keys
});
if (!parsed.success) return { error: firstError(parsed.error) };

const limit = rateLimit(`login:${parsed.data.email}`, 10, 60_000);
if (!limit.ok) return { error: `Too many attempts. Try again in ${limit.retryAfterSec}s.` };
// uniform failure + dummy scrypt burn for unknown accounts (timing parity)
```

### 15.5 Atomic stock reservation (guard in the WHERE)

```ts
const reserved = await tx.product.updateMany({
  where: { id: item.productId, isActive: true, stock: { gte: item.quantity } },
  data:  { stock: { decrement: item.quantity } },
});
if (reserved.count === 0) throw new CheckoutError(409, `Only ${liveStock} left in stock.`);
```

### 15.6 Optimistic update with per-line lock and rollback

```tsx
const prev = lines;
setLines(optimistic); setPendingId(line.id);
try {
  const res = await fetch("/api/cart", { method: "PATCH", body });
  if (!res.ok) throw new Error(data.error ?? "Could not update your cart.");
  if (typeof data.itemCount === "number") setCartCount(data.itemCount);  // server truth wins
} catch { setLines(prev); } finally { setPendingId(null); }
```

### 15.7 Identity-token minting (guests and users alike)

```ts
const token = randomBytes(24).toString("hex");           // 192-bit
await db.cart.create({ data: { token } });
store.set(CART_COOKIE, token, { httpOnly: true, sameSite: "lax", secure: isProd, path: "/" });
```

### 15.8 HMAC capability token (guest order views)

```ts
export function orderViewToken(orderNumber: string): string {
  return createHmac("sha256", authSecret())
    .update(`order-view:${orderNumber}`)                 // domain separation
    .digest("hex").slice(0, 40);
}
export function verifyOrderViewToken(n: string, t: string): boolean {
  const expected = orderViewToken(n);
  return t.length === expected.length && timingSafeEqual(Buffer.from(t), Buffer.from(expected));
}
```

### 15.9 Money helpers

```ts
formatMoney(29999)              // "$299.99" — display only
parseDollarsToCents("299.99")   // 29999     — the ONLY dollars→cents conversion
discountPercent(29999, 39999)   // 25        // for -25% badges
computeOrderMoney({...})        // pure totals; unit-pinned (threshold, tax rounding)
```

### 15.10 Hydration-gated e2e helper

```ts
export async function gotoHydrated(page: Page, path: string) {
  await page.goto(path);
  await page.waitForSelector('html[data-hydrated="true"]');
}
```

### 15.11 Session sweeper (pure plan + executor)

```ts
export function buildSweepPlan(now: Date) {              // pure, unit-pinnable
  return { sessionCutoff: new Date(now.getTime() - SESSION_TTL_MS),
           guestCartCutoff: new Date(now.getTime() - GUEST_TTL_MS) };
}
export async function runSweep(db: PrismaClient, plan: SweepPlan) {
  await db.session.deleteMany({ where: { expiresAt: { lt: plan.sessionCutoff } } });
  await db.cart.deleteMany({ where: { userId: null, updatedAt: { lt: plan.guestCartCutoff } } });
}
// wired in instrumentation.ts: run at boot + hourly; P2021 (schema not ready) → one soft line
```

### 15.12 Webhook handler skeleton (dedop-in-tx)

```ts
export async function POST(req: Request) {
  const sig = req.headers.get("stripe-signature");
  const raw = await req.text();                          // raw body — required for HMAC
  let event: Stripe.Event;
  try { event = stripe.webhooks.constructEvent(raw, sig!, WEBHOOK_SECRET); }
  catch { return new Response("Bad signature", { status: 400 }); }

  return db.$transaction(async (tx) => {
    const dup = await tx.stripeEvent.findUnique({ where: { eventId: event.id } });
    if (dup) return Response.json({ received: true });  // idempotent replay
    await applySideEffects(tx, event);                   // placement / refund reflection
    await tx.stripeEvent.create({ data: { eventId: event.id, type: event.type } });
    return Response.json({ received: true });            // dedup row commits WITH effects (E6)
  });
}
```

---

## §16. Coding Anti-Patterns

```tsx
// ❌ client-trusted totals                  ✅ server re-derivation
const total = items.reduce(...);              const res = await placeOrderAction(payload);

// ❌ optimistic cart math as truth           ✅ the server response IS the new state
setCart(prev => prev + 1);                    setCart(res.data);

// ❌ throw across the seam                   ✅ ActionResult failure
throw new Error("oops");                      return { ok: false, error: { message } };

// ❌ absolute stepper quantity               ✅ post the delta
updateQuantity(id, qty + 1);                  adjustQuantity(id, +1);   // transactional

// ❌ JS-toggle `hidden` on overlays          ✅ conditional mount
setHidden(false);                             {open && <MobileNav />}

// ❌ per-test logins                         ✅ one setup login + storageState

// ❌ setState in an effect                   ✅ adjust-during-render / derived / useActionState

// ❌ check-then-act across await             ✅ guard in the WHERE, one conditional write
if (p.stock >= qty) await update(...);        updateMany({ where: { stock: { gte: qty } }, ... });

// ❌ scrypt hash as a lookup key             ✅ sha256 for high-entropy token lookups

// ❌ `: any` / `as any` / @ts-ignore         ✅ fix the type — the gates stay strict

// ❌ bare `status`/`name`/`origin` in server code   ✅ destructure or import explicitly (F14)

// ❌ second state library / custom hook layer ✅ one StoreProvider context
```

---

## §17. Documentation & Process Standards

### 17.1 The document system

| Document | Role | Update rule |
|---|---|---|
| `README.md` | Operations manual: features, setup, commands, env. Feature tables state WHAT, not session history. | Same commit as user-visible changes. |
| `AGENTS.md` | Agent cheat-sheet: commands, environment traps, architecture invariants, the compact trap log. | Same commit as any trap/invariant change. |
| `CLAUDE.md` | Working standards: the six-phase workflow, non-negotiables per area. | Same commit as process changes. |
| `Project_Architecture_Document.md` | ADRs with full rationale, threat model, ERD, known-issues ledger. | New ADR per architecturally significant decision. |
| `SKILL.md` (this file, project instance) | The distilled, self-contained onboarding skill: everything above in teaching order. | Version-bumped with the change. |

**The conflict rule:** code and tests win over every document — then the documents are fixed **in the same change**. A false claim in a doc ("React Compiler rules are ON") is a defect with a reader, not just a reader.

### 17.2 The six-phase working method (per change)

1. **Reproduce / read first** — browser or failing test before code; read the nearest surface + action seam completely.
2. **Plan the seam** — page (RSC) → component → action → validation → schema. One vertical slice.
3. **Implement minimal + typed** — strict TS, no `any`, DTOs as props.
4. **Gate locally** — `verify` (typecheck, lint, unit, build), then `test:e2e` against the fresh build.
5. **Verify in the browser** — dev server + real interaction; screenshots when design contracts are touched.
6. **Document drift** — update AGENTS/CLAUDE/PAD/SKILL + the trap log in the same commit; Conventional Commit to `main`.

### 17.3 Session discipline (for AI-assisted development)

Numbered sessions; each session ends with a remediation pass and a recorded entry: scope, findings (severity + class), fixes, gate receipts (unit/e2e counts), docs updated, deferred items with precedent citations. **A "fully-empty remediation cycle" (zero findings) is a milestone worth naming.** Never defer silently — record deferrals with their acceptance rationale. Mutation demos are recorded as: rebuild → predicted-runs-red → restore (inverse edit) → green.

---

## §18. Template Hygiene, Rebranding & Production Readiness

> This section exists because the October 2026 audit of the three source repositories found that **all three failed template adoption on repository-level grounds, not code-level grounds**: no LICENSE anywhere, 192 MB of unrelated baggage in each, one committed restorable SSH key, zero CI pipelines. The application cores were production-minded; the repositories around them were not reusable artifacts. Do not repeat the pattern.

### 18.1 The template hygiene checklist (day zero)

- [ ] **LICENSE committed** — decide MIT/Apache-2.0/proprietary and commit the file. A README claim ("MIT — see repository settings") grants nothing; the default is all-rights-reserved.
- [ ] **The repo contains the product and only the product.** No personal skill libraries, no session archives, no screenshots, no committed zips, no one-off probe scripts. Target: the repo IS the app (source + docs + tests + configs). If your app source is 1 MB, a 300 MB clone is a bug.
- [ ] **`.gitignore` covers** `.env`, `db/*.db*`, logs, `tests/e2e/.auth/`, `node_modules`, keys (`*.key`, `*.pem`).
- [ ] **CI runs on every push** (§11.4) and a **Dockerfile** builds the standalone output.
- [ ] **`.env.example` is the complete, documented env contract.**
- [ ] **Secrets scan passes**: no key material, credentials, or tokens anywhere in history — including "redacted" bodies (a redacted BEGIN line over an intact base64 body is still a key; if it happened: rotate, then `git filter-repo`).

### 18.2 Branding: keep it a variable, not a scar

Single brand constant (name, logo, og-card, favicon) referenced from one config; tokens + fonts + seed catalog + copy are the rebrand surface. The audit's cautionary tales: one repo was triple-named (package ≠ metadata ≠ deployment docs); another pinned its test suite to a third-party prototype's measured pixels, so rebranding invalidated the tests. **Design-contract tests should pin YOUR OWN measured tokens** — then rebrand = re-measure once, update the pin, suite stays green.

### 18.3 Secrets & credentials discipline

- Never commit keys — not in docs, not in prompt archives, not "temporarily", not redacted-but-intact.
- Reference-site / third-party credentials never enter the repo (docs included).
- If a secret lands in history: **rotate first** (the exposed key must die), then rewrite history, then audit access logs. Rotation after rewrite is too late — the key is public from the push.

### 18.4 Asset ownership

Self-host imagery, favicon, and fonts from origins you control; `img-src 'self' data:` in CSP. Hot-linking a cloned reference's CDN couples your availability and your rebrand to a third party, and your CSP to their domain.

### 18.5 The scaling path (documented, not built)

The default deployment shape is honest for a small store: one Node process, one SQLite file, in-memory rate limiting, all-dynamic rendering. When scale demands more: (1) Prisma schema ports to PostgreSQL (keep the schema provider-agnostic; add the FK indexes you skipped); (2) externalize the rate limiter to the shared store (the swap point is the `rateLimit` signature); (3) move the sweeper to a scheduled job; (4) revisit caching/ISR against the nonce CSP contract. Write the path down in the PAD — the source repos did, and it aged well.

### 18.6 Production readiness gaps to close deliberately

Email provider (§9.4), image upload pipeline (object storage + signed uploads), real full-text search beyond `contains`, tax/jurisdiction logic, i18n/multi-currency, observability beyond tagged console errors, returns/RMA flows. Each has a designed seam or a documented deferral — close them in that order of business need, and keep the docs truthful about which are closed.

---

## §19. Pre-Ship Checklist

The full gate chain — it is the only gate:

```bash
npm run verify        # typecheck → typecheck:tests → lint → unit → build (+assemble)
npm run test:e2e      # against the fresh standalone build (§13.F1)
curl -sI localhost:3000/ | grep -i content-security    # CSP present, nonce'd, no unsafe-* in prod
```

Contract pins (fail the ship if any regresses):

```bash
rg -n "space-y-" src/components/store || echo "OK: flex-gap stacking on overlay surfaces"
rg -n "hsl\(" src/app/globals.css | wc -l            # tokens are hsl() literals
rg -n "new Headers\(\)" src/lib                      # must be ZERO hits (§13.D7)
rg -n "next/font" src                                # self-hosted fonts only (or deliberate)
ls .next/standalone/.next/static >/dev/null && echo "OK: standalone assets assembled"
git ls-files .env.example | grep -q . && echo "OK: .env.example tracked"
```

Human checks:

- [ ] Mobile menu opens/closes **twice in a row** (the A3 regression)
- [ ] Login wrong-password **and** unknown-email show the SAME message
- [ ] Order tracking with a valid number but wrong email shows only the alert shell — no PII, no existence oracle
- [ ] A guest can add to cart, check out, and see the order number; the badge empties after success
- [ ] Admin console loads every section; a save actually persists (reload + assert, not toast)
- [ ] Zero-quantity lines cannot be ordered; stock shows the live cap on 409
- [ ] `git status` clean of `.env`, `db/*.db`, keys, logs
- [ ] New external inputs all pass through a Zod schema; new money math has a unit-test counterpart
- [ ] Docs counts match the suites (unit/e2e numbers in README/CLAUDE are not stale)
- [ ] No new `console.log` (`console.error("[tag]", e)` is the pattern)
- [ ] If this session added a committed script AFTER the last lint: re-run the gate chain as the LAST step (§13.G1)
- [ ] Fresh-clone experience: `rm -rf node_modules db && npm install && npm run db:setup && npm run dev` works from zero

---

## §20. Quick Reference Card

```bash
npm run dev            # :3000, logs → dev.log
npm run db:setup       # push + idempotent seed
npm run verify         # typecheck + tests-typecheck + lint + unit + build
npm run test:e2e       # standalone :3100 (build FIRST)
npx playwright test tests/e2e/<spec>.ts               # one spec
npx vitest run tests/unit/<file>.test.ts              # one unit file
node -e "console.log(process.env.DATABASE_URL)"       # env-shadowing probe
env -u DATABASE_URL npm run db:setup                  # sandbox-safe DB command
curl localhost:3000/api/health                        # {"status":"ok","db":"up"}
```

| Need | Path |
|---|---|
| Design tokens + engine pins | `src/app/globals.css` |
| The mutation seam | `src/lib/actions/*.ts` |
| Action envelope | `src/lib/action-result.ts` |
| Client DTO contract (pure) | `src/lib/cart-dto.ts` |
| DB resolver (do not simplify) | `src/lib/db-path.ts` |
| Money math | `src/lib/money.ts`, `src/lib/order-money.ts` |
| Rate limiting + client IP | `src/lib/rate-limit.ts`, `src/lib/client-ip.ts` |
| Guest order access | `src/lib/order-token.ts`, `src/lib/order-tracking.ts` |
| Order state machine | `src/lib/order-status.ts` |
| Validation schemas | `src/lib/validation.ts` |
| CSP policy | `src/lib/csp.ts` + `src/proxy.ts` |
| Stripe stack | `src/lib/stripe*.ts` + `src/app/api/webhooks/stripe/` |
| Catalog source | `prisma/seed.ts` |
| E2E helpers | `tests/e2e/helpers.ts` (`gotoHydrated`) |
| Standalone assembly | `scripts/assemble-standalone.mjs` |

---

## Appendix A — ADR Starter Set

The twenty decisions every build on this skill must record (copy into the PAD with project-specific rationale; each gets a one-paragraph "why" and a "consequences" note):

| ADR | Decision |
|---|---|
| 001 | Single Next.js app: storefront + admin in one deployment; no monorepo, no separate API service. |
| 002 | App Router, RSC by default, `output: "standalone"` with an explicit asset-assembly build step. |
| 003 | SQLite via Prisma with the schema-relative `file:` URL contract (`db-path.ts`); Postgres path documented for scale. |
| 004 | Server actions as the only mutation seam; route-handler whitelist (health, search, newsletter, payment webhook). |
| 005 | `ActionResult<T>` envelope + Zod at every boundary; malformed input is 400, never 500. |
| 006 | Integer-cent money; one conversion seam; one pure totals function; server-side re-derivation in the order transaction. |
| 007 | scrypt passwords + DB-backed sessions (SHA-256 token hashes) + HMAC cookies; no JWT, no third-party auth. |
| 008 | Guest identity via 192-bit cookie tokens; quantity-max merge into user rows at login, in one transaction. |
| 009 | Per-request nonce CSP via `proxy.ts`; `connection()` pin against the prerender trap; env-conditional dev carve-out. |
| 010 | Tailwind v4 CSS-first theme with pinned measured tokens; the trap log as a first-class artifact. |
| 011 | Route groups: chrome-less root, `(storefront)` chrome + provider, `(auth)` bare cards. |
| 012 | Order-item snapshots; terminal statuses; transactional cancel-restock; OrderEvent timeline with actor filtering. |
| 013 | Idempotency keys on order placement; webhook dedup rows commit with side effects. |
| 014 | Payments env-gated (demo default; Stripe stack per §9.2 when keys present); verify-then-place; webhook as backstop. |
| 015 | Email behind a console seam until a provider is wired; verification flows stay OFF until then. |
| 016 | E2E runs against the standalone production build; one worker; storageState auth; SQL-minted admin sessions. |
| 017 | Mutation-check doctrine: no gate is trusted until a mutation has failed it. |
| 018 | Layered docs (README/AGENTS/CLAUDE/PAD/SKILL) updated in the same commit; code-and-tests-win conflict rule. |
| 019 | `main`-only, atomic Conventional Commits; every commit passes the gate chain. |
| 020 | Template hygiene: LICENSE, slim tree, no secrets in history, CI + Dockerfile from day one. |

---

## Appendix B — Coverage Map: Every Declared Contract Owns a Gate

The doctrine generalized from the source family's seam registry: **a contract without a gate is a wish.** Minimum coverage for a store built on this skill:

| Contract | Gate |
|---|---|
| DB-path resolution | Unit: relative/absolute/pass-through cases |
| Money math (thresholds, tax rounding, discount %) | Unit: `computeOrderMoney` pins |
| Rate-limit floors + keys (incl. server-action IP) | Wire-level e2e: burst → 429; per-IP control |
| Auth anti-enumeration | E2E: uniform message + timing parity (dummy burn) |
| Session lifecycle (rotate-revoke, logout delete, expiry deny) | E2E + unit |
| Guest order access (HMAC token) | E2E matrix: valid pair / flipped / cross-order / unknown → identical 404-shell |
| IDOR walls (addresses, cart lines, order detail) | Action-seam e2e: hostile writes fail closed, zero DB writes |
| Admin role walls | Action-seam e2e with SQL-minted sessions |
| Checkout transaction write-set (stock decrement, event mint, cart purge) | Real-engine integration + post-render re-read |
| Stock enforcement (3 seams) | Unit (clamp) + integration (in-tx rejection) |
| Coupon redemption caps | Real-engine integration (atomic increment) |
| Payment webhook (signature, dedup, refund reflection) | Integration: real handler + real HMAC events + scratch DB |
| CSP (nonce per request, prod vs dev) | Served-bytes e2e |
| Security headers | E2E: exact values on route classes |
| SEO surfaces (sitemap, robots, JSON-LD, OG) | Body-asserting e2e (not status codes) |
| a11y (axe, both viewports, stateful surfaces) | Standing axe spec with self-cleaning fixtures |
| Mobile-nav conditional mount | Regression spec with double-open/close cycles |
| Email seam | Unit (stub called with right payload) until provider e2e exists |
| Design tokens (if pinned) | Computed-style / token-identity probes |
| Fresh-clone bootstrap | CI job from clean checkout |

When you add a capability, add its row. When you weaken a gate to make a test pass, you are fixing the wrong thing — fix the product.
