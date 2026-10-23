---
name: web-app-foundation
description: >-
  Generalized engineering skill for scaffolding any production web application
  with authentication, a dashboard shell, and charting. Stack: Next.js 16 App
  Router + React 19 + TypeScript strict + Tailwind CSS 4 (CSS-first) +
  shadcn/Radix + one Zustand store + Prisma (SQLite-dev / PostgreSQL-prod) +
  Zod-validated JSON API + scrypt/HMAC cookie auth + recharts wrappers + a
  three-tier test suite and a single-command quality gate. Distilled from four
  sibling codebases (digma, neo-crm, project-management/ORBITAL, zero-balance).
  Every rule traces to a failure that actually happened in that family.
version: 2.0.0
last_updated: 2026-10-23
provenance: >-
  Union of digma_SKILL.md v1.158, neo-crm_SKILL.md v1.171 (contracts only —
  not the 12k-line session diary), project-management_SKILL.md, and
  zero-balance_SKILL.md, plus the 2026-10-23 four-way ranking report.
---

# Web App Foundation — Complete Engineering Skill

> **How to use this document.** This is the single-source contract for scaffolding, extending, debugging, or auditing any web app built on this skill. §0 is the build order; §1–§16 are the contracts; §17–§20 keep the machine honest. **When code and this document disagree, the code wins — then fix this document in the same commit.**
>
> **Companions (create all five, keep them in lockstep):** `README.md` (humans), `AGENTS.md` (operator card, ≤ 300 lines), `CLAUDE.md` (agent contract, ≤ 600 lines), `Project_Architecture_Document.md` (ADRs), this `SKILL.md`. Stale docs are bugs.

---

## Table of Contents

0. [Scaffolding workflow](#0-scaffolding-workflow-any-app-this-order)
1. [Product identity & philosophy](#1-product-identity--philosophy)
2. [Canonical stack](#2-canonical-stack)
3. [Bootstrapping, config, database path](#3-bootstrapping-config-database-path)
4. [Design system (Tailwind v4)](#4-design-system-tailwind-v4)
5. [Authentication & security](#5-authentication--security)
6. [API layer](#6-api-layer)
7. [Data layer, tenancy, validation](#7-data-layer-tenancy-validation)
8. [App shell, navigation, dashboard](#8-app-shell-navigation-dashboard)
9. [Charting](#9-charting)
10. [State management](#10-state-management)
11. [Component architecture](#11-component-architecture)
12. [Accessibility](#12-accessibility)
13. [Testing](#13-testing)
14. [Quality gate](#14-quality-gate)
15. [Deployment & production](#15-deployment--production)
16. [AI features (optional)](#16-ai-features-optional)
17. [Anti-patterns & hard-won bugs](#17-anti-patterns--hard-won-bugs)
18. [Debugging guide](#18-debugging-guide)
19. [Documentation contract](#19-documentation-contract)
20. [Pre-ship checklist](#20-pre-ship-checklist)
- [Appendix A — Six-phase workflow](#appendix-a--six-phase-workflow)
- [Appendix B — Donor matrix](#appendix-b--donor-matrix)
- [Appendix C — Quick reference card](#appendix-c--quick-reference-card)
- [Appendix D — Production gaps this skill does not close](#appendix-d--production-gaps-this-skill-does-not-close)

---

## 0. Scaffolding workflow (any app, this order)

1. **DEFINE** — one-sentence identity; 3–7 core entities; non-negotiables (what this app will *never* do). Write the README skeleton first.
2. **SCAFFOLD** — Next.js App Router standalone, strict TS, Tailwind 4 CSS-first, Prisma, the config files in §3, and lint/typecheck/test/build scripts *before* features.
3. **DATA** — `prisma/schema.prisma` first (models, `userId`, indexes, cascades), then an idempotent seed. Money is integer minor units.
4. **AUTH** — the full family in §5 before any domain feature. Auth is the template's most valuable inheritance — port it, do not rewrite it.
5. **API** — one route per resource, handler idiom §6: session → bounded body → Zod → ownership → Prisma → envelope.
6. **UI SHELL** — sidebar + topbar + mobile nav, then feature views. Empty/loading/error are part of every surface, not polish.
7. **DASHBOARD + CHARTS** — KPI cards, then wrappers from §9. Every chart ships an empty-state fallback.
8. **TEST AS YOU GO** — every pure seam gets a Vitest spec when written; every user-visible surface gets an e2e pin before it ships.
9. **GATE + DOCS** — run §14; update all five docs in the same commit. The gate is the definition of done.

Do not skip steps. A dashboard built before auth becomes an unauthenticated prototype that never grows a real session.

---

## 1. Product identity & philosophy

- **One deployable unit.** No microservices, no Redis, no external auth provider to start. `next build` produces a standalone server. Scale *up* only when a measured limit demands it (Appendix D).
- **Degrade, never fail.** Optional integrations (AI, PDF, mail) carry deterministic fallbacks. The app must not 500 because an optional dependency is down.
- **Pure seams, tested.** Path resolution, validation, money, rate limiting, date grouping, KPI math live in `src/lib/*.ts` with a Vitest spec. Handlers and views stay thin.
- **Superset, never silent regression.** When cloning a reference UI, match it deliberately and *fix its bugs*. Record every deviation in the PAD. A deviation nobody wrote down is a bug nobody can defend.
- **Anti-generic mandate.** No glassmorphism-by-default, no purple-gradient-on-white cliché, no `rounded-2xl` on everything. Brand color comes only from tokens (§4). Every page should look *authored*.
- **Count the things.** Env vars, models, routes, tests — know the numbers. When one changes, search the old number across the doc set in the same commit.
- **Code wins.** Documentation is a product surface. If they drift, the code is the source of truth *and* the docs are now a bug.

---

## 2. Canonical stack

| Layer | Technology | Version floor | Notes |
|---|---|---|---|
| Framework | Next.js App Router | 16.4 | `output: "standalone"`; `outputFileTracingRoot` pinned to repo root |
| UI runtime | React | 19.3 | `"use client"` explicit; no `forwardRef` needed |
| Language | TypeScript | 5.9 | `strict: true`. **Do not set `ignoreBuildErrors`.** The build is the type gate |
| Styling | Tailwind CSS | 4.3 | CSS-first: `@theme inline` in `globals.css`. **No `tailwind.config.js`** |
| PostCSS | `@tailwindcss/postcss` | ^4 | The only plugin; missing it = unstyled pages |
| Primitives | shadcn/ui on Radix | per-pkg | dialog, select, popover, dropdown, sheet, tabs, label; bespoke only when primitives cannot |
| State | Zustand | 5.0 | **ONE store**; derived selectors use `useShallow` |
| ORM / DB | Prisma | 6.19 | SQLite in dev; PostgreSQL in prod (documented *and*, before launch, tested) |
| Validation | Zod | 4.6 | At every API boundary |
| Charts | recharts | 2.15 or 3.x | Wrapped, never raw in pages |
| Icons | lucide-react | 0.525 | Library defaults (stroke 2) unless a measured reason exists |
| Unit tests | Vitest | 5.0 | Node env; `*.test.ts` only |
| E2E | Playwright | 1.64 | Against the **production** standalone build |
| A11y | axe-core (Playwright) | 4.x | At least one e2e spec |
| Runtime | Bun 1.3 or Node ≥ 20 | | Scripts run from **repo root** — this matters (§3) |

**Dependency discipline.** Every dependency must have a live import within one commit of being added. Periodically census zero-import packages and delete them. Prefer library defaults over bespoke micro-styling.

**Environment contract** (add a variable only with an ADR):

| Variable | Required | Purpose |
|---|---|---|
| `DATABASE_URL` | yes | `file:../db/custom.db` (SQLite dev) or `postgresql://…` (prod). Relative `file:` URLs resolve against `prisma/schema.prisma`, never against CWD |
| `AUTH_SECRET` | **production hard-fail** | HMAC key, ≥ 16 chars (`openssl rand -hex 32`). Dev may warn-and-fallback; production **throws at boot** |
| `NEXT_PUBLIC_SITE_URL` | recommended | Canonical origin for metadata, OG, sitemap, robots. Inlined at **build** time |
| `<APP>_PROXY_HOPS` | prod-behind-proxy | Trusted appending-proxy depth for rate-limit IP keying. Unset = 1. Unparsable **fails closed** onto 1 |
| `<APP>_DISABLE_IN_APP_OTP` | prod | Stop putting verification codes in JSON once a mailer owns delivery |
| `<APP>_DISABLE_IN_APP_RESET` | prod | Stop putting reset URLs in JSON once a mailer owns delivery |

`.env` is untracked. `.env.example` is committed and matches the contract exactly.

---

## 3. Bootstrapping, config, database path

### 3.1 Files that carry non-obvious weight

| File | Locks in |
|---|---|
| `next.config.ts` | `output: "standalone"`; `outputFileTracingRoot` pinned (prevents nested standalone paths under a parent workspace lockfile); **`outputFileTracingExcludes`** so `.env`, `.git`, `skills/`, `docs/`, `db/` never ship; **do not set `ignoreBuildErrors`**; `headers()` for `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, HSTS; `reactStrictMode` **on** |
| `tsconfig.json` | strict; `@/*` → `src/*`; exclude `skills/`, `docs/` |
| `eslint.config.mjs` | next/core-web-vitals + next/typescript; React 19 hook rules (incl. `set-state-in-effect`) as **errors**; `--max-warnings 0` in the lint script |
| `vitest.config.ts` | `src/**/*.test.ts` + `tests/**/*.test.ts`; never match Playwright `*.spec.ts` |
| `playwright.config.ts` | setup project (one login → `storageState`); webServer = standalone on its own port with its **own** `DATABASE_URL` (`db/e2e.db`); `workers: 1` |
| `postcss.config.mjs` | `@tailwindcss/postcss` only |
| `src/instrumentation.ts` | Calls `boot-env.ts` so a missing prod secret refuses to serve |

Build script must copy `.next/static` + `public` into standalone **and** `rm -f .next/standalone/.env` (Next copies `.env` into the artifact even when tracing excludes it).

### 3.2 The DATABASE_URL contract (read twice — it bit all four donors)

A relative `file:` URL resolves differently per reader:

- Prisma CLI reading `.env` anchors at `prisma/schema.prisma`.
- A **shell-inherited** `DATABASE_URL` anchors at CWD (unpredictable). `dotenv` never overrides an existing process env.
- Next standalone `server.js` runs `process.chdir()` before app code loads.
- The Prisma engine also anchors beside the **traced** `schema.prisma` inside the standalone output.

Therefore:

1. `src/lib/db-path.ts` is the **only** sanctioned source of the runtime URL. `db.ts` never reads `process.env.DATABASE_URL` directly.
2. Anchor chain: explicit repo-root env override → standalone-repo-root detector → module anchor validated **on disk** → CWD with existence guard.
3. Anchors are collected via **side-effect** `roots.push(...)`. Helper functions whose return values look unused get inlined-and-dropped by the production minifier — the detector then silently dies in the shipped bundle.
4. `db-path.ts` is a pure seam with fixture tests. This is the most-tested module in the donor family, for good reason.
5. npm/bun scripts pin the environment: runtime scripts inline `DATABASE_URL=…`; Prisma CLI scripts strip it (`env -u DATABASE_URL prisma …`) so a polluted parent shell cannot redirect the database.

**Symptom to memorize:** `Error code 14: Unable to open the database file` = wrong anchor or a shell env override. Check `env | grep DATABASE` and the `[db] DATABASE_URL -> …` startup log before touching code.

### 3.3 First-run sequence

```bash
bun install                          # or npm ci
cp .env.example .env                 # then set AUTH_SECRET in prod
bun run db:push                      # schema → db/custom.db
bun run db:seed                      # idempotent demo data
bun run dev                          # :3000
# Fast gates:
bun run lint && bun run typecheck && bun run test
# Full gates:
bun run build && ./scripts/smoke-test.sh && bun run test:e2e
```

---

## 4. Design system (Tailwind v4)

### 4.1 Tokens

All color, radius, shadow, and font tokens live in `src/app/globals.css` inside `@theme inline`. **Literal hex and literal font names.** Never:

- a `tailwind.config.js` / `tailwind.config.ts` (reintroduces the v4 “flat/minimal look” bug);
- `var(--font-inter)` (or any next/font CSS variable) **inside `@theme`** — next/font scopes the var to `<body>`, so the chain is invalid at `:root` and the whole app silently renders in the UA serif;
- `@layer utilities` for one-off utilities — use v4 `@utility`.

Pin consumed palette steps to the brand hex. Tailwind v4's default oklch scale is visibly off from v3 hex.

### 4.2 Anti-generic visual rules

- One brand accent, used for CTAs and focus rings. Secondary actions are quiet.
- Status colors (success/warn/danger/info) are a closed vocabulary in `constants.ts` with label + token together.
- Shadows are a 2–3 step scale, not per-card invention.
- Motion is short (150–200 ms) and never the only means of conveying state.

### 4.3 Typography

A small hierarchy (display / title / body / caption / numeric) declared as utilities or components. Tabular nums on KPIs (`tabular-nums`). Do not mix more than two families.

### 4.4 Z-index map (keep it short and named)

| Layer | z | Used by |
|---|---|---|
| base | auto | pages |
| sticky chrome | 30 | topbar / sidebar |
| dropdown | 40 | menus |
| overlay | 50 | sheet / dialog backdrop |
| modal | 50 | dialog |
| toast | 60 | toasts |
| max | 70 | skip-link target / present mode |

Never scatter `z-[9999]`.

---

## 5. Authentication & security

Hand-rolled on Node `crypto`. No NextAuth, no JWT library, no Redis session store to start. Auditable, copyable, testable.

### 5.1 Passwords — `src/lib/password.ts`

Pure module: **node:crypto only**. The seed script must import this file, not `auth.ts` (which pulls `next/headers` + Prisma and cannot run in a bare seed).

- `hashPassword`: scrypt, 16-byte salt, 64-byte key, stored `scrypt:salt:hash` (version prefix lets you rotate later).
- `verifyPassword`: split, length-check, `timingSafeEqual`.
- `timingEqualizerHash`: lazy scrypt of a throwaway constant so unknown-email logins pay the same cost as known ones.
- `generateVerifyCode`: `randomInt`, six digits. Not `Math.random()`.
- `hashResetToken`: SHA-256 hex of the raw token. The DB stores the hash; the raw token lives only in the delivery URL. (A DB read must not mint live reset links.)

### 5.2 Sessions — `src/lib/auth.ts`

- Cookie name: `<app>_session`. httpOnly, `sameSite: "lax"`, `secure` in production, `path: "/"`, TTL **7 days** (not 30).
- Payload: signed structure carrying `uid`, `exp`, and **`v` (tokenVersion)**. HMAC-SHA256. Compare signatures with `timingSafeEqual` after equal-length checks. Reject non-finite expiry.
- `getSessionUser()`: parse → load user → **reject if `user.tokenVersion !== payload.v`**.
- Password reset increments `tokenVersion` in the same transaction as the hash update — every previously minted cookie dies.
- `AUTH_SECRET`: production missing or `< 16` chars **throws**. `boot-env.ts` runs at process start so the first request is not the first failure. Dev warns once and uses a named insecure constant.

### 5.3 Auth routes (all of these, before domain features)

| Route | Limit | Notes |
|---|---|---|
| `POST /api/auth/register` (or signup) | 10 / 15 min / IP | Create unverified user; never session yet |
| `POST /api/auth/verify` | 20 / 15 min / IP | 6-digit code, attempt cap (5), expiry |
| `POST /api/auth/resend` | 5 / 15 min / IP | Rotate code, reset attempts |
| `POST /api/auth/login` | 10 / 15 min / IP | Timing-equalized; unverified → verify prompt, no session |
| `POST /api/auth/logout` | — | Clear cookie |
| `GET  /api/auth/me` | — | **Not** `requireSession` — logged-out returns `{ user: null }` |
| `POST /api/auth/forgot-password` | 10 / 15 min / IP | **No enumeration**: always 200. Store hashed token, 60-min TTL |
| `POST /api/auth/reset-password` | 10 / 15 min / IP | Atomic `updateMany` WHERE hash+live expiry; increment `tokenVersion`; single-use |

Kill-switches: in production without a mailer, `<APP>_DISABLE_IN_APP_OTP=1` and `_RESET=1` so secrets never ride the JSON. The demo-mode in-response delivery is a documented self-hosted deviation, not a feature.

### 5.4 Rate limiting — `src/lib/rate-limit.ts`

Fixed-window, in-process `Map`. Per-route buckets (table above). 429 envelope + `Retry-After`. Sweep watermark so unused keys are reclaimed without O(n) on every hit. Injectable `now` for tests.

`<APP>_PROXY_HOPS`: unset = 1 (last XFF hop). `0` = ignore client-supplied XFF entirely (shared bucket — honest self-throttle). `N≥2` = N trusted appending proxies. Unparsable → fail closed onto 1.

**Documented limitation:** per-process. Restarts clear it; N instances split it. Before horizontal scale, replace with Redis/Upstash. Do not pretend the Map is distributed.

### 5.5 Route and page protection

- Every data route's **first** statement is `requireSession()`. Failure → 401 envelope, never a thrown error.
- Every authed page is a server component that `getSessionUser()` + `redirect("/login?from=…")`.
- Client `require-session` is a complement (avoid flash), not the security boundary.
- Public: `/api/health`, `/api/auth/*`, marketing pages. Nothing else.

### 5.6 RBAC and tenancy (do not skip)

- If you store `role`, **enforce it** on the route or delete the column. A column that UI implies and API ignores is a vulnerability.
- Tenancy is §7. Auth without tenancy is a locked front door on an open plan.

### 5.7 Headers and CSRF

JSON APIs + `sameSite=lax` cookies are the CSRF posture. Add:

```
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
Strict-Transport-Security: max-age=31536000   /* inert on HTTP, correct behind HTTPS */
```

A full CSP is optional; inline-style Tailwind often forces `style-src 'unsafe-inline'`, which is theater. If you add CSP, measure it.

---

## 6. API layer

### 6.1 Envelope

```ts
type ApiResult<T> =
  | { ok: true; data: T }
  | { ok: false; error: { code: string; message: string } };
```

Never throw across the handler boundary. Named helpers: `ok`, `fail`, `ERR.UNAUTHORIZED`, `ERR.FORBIDDEN`, `ERR.NOT_FOUND`, `ERR.BAD_REQUEST`, `ERR.RATE_LIMITED(retryAfterSec?)`, `ERR.INTERNAL`. DB exceptions become 500 envelopes.

`error: string` (zero-balance) is too weak — use `{ code, message }`.

### 6.2 Handler idiom (memorize)

```
1. requireSession()            → 401
2. bounded-body pre-gate       → 413/400  (declared Content-Length ceiling, e.g. 16 KB for JSON)
3. parseBody(schema)           → 400 field message (first Zod issue)
4. ownership / FK checks       → 404 (do not leak existence across tenants)
5. mutation in a transaction
6. serialize                   → never return a raw Prisma row
7. ok(data)
```

GET list: session → parse query → `where: { userId }` → serialize.

### 6.3 Client seam

One `call()` helper unwraps the envelope, types the data, and maps `ok: false` to a thrown `ApiError` the store/UI can toast. Pages never `fetch` + `res.json()` ad hoc.

### 6.4 Import/export

If CSV exists: formula-injection guard (prefix `'`, `=`, `+`, `-`, `@`). Filename from the server. Cap upload size. Validate path anchors (no `..`). PDF is optional and degrade-never-fail.

---

## 7. Data layer, tenancy, validation

### 7.1 Prisma schema rules

- `User` holds auth fields only: email unique, passwordHash, tokenVersion, verify/reset hashes + expiries, timestamps. Profile fields that are not auth may live here if small.
- **Every tenant-owned row:** `userId String` (or `orgId` if you introduce orgs) + relation `onDelete: Cascade` + `@@index([userId, …])`.
- Lookups: `findFirst({ where: { id, userId } })`. Miss → 404, same as a truly missing row (no cross-tenant oracle).
- Enums in the DB may be strings; **membership is enforced in Zod against `constants.ts`**, not by hope.
- Money: store integer minor units (cents). If a reference API forces floats on the wire, convert at the boundary (`money.ts`) and sum only integers.
- Indexes: compound beats a redundant single-column prefix. Don't double-index `userId` and `[userId, createdAt]` unless both query shapes exist.

### 7.2 Zod at every boundary

- One `src/lib/schemas.ts`. Field builders (email, password, id, money, isoDate) shared. Per-route objects compose them.
- Email: trim, lowercase, max 160–254, honest reject (do not silently truncate).
- Password: min 8, max 128 on set; login may only require non-empty + max.
- ISO dates: regex `YYYY-MM-DD` **and** a round-trip calendar check (`2026-02-30` must fail).
- PUT three-state: absent → no write; `null`/empty → clear; value → trimmed value.
- FK *existence* stays in the handler (it needs the DB). Zod does shape, not joins.

### 7.3 Serializers

`src/lib/serializers.ts` maps Prisma rows to public DTOs. Strip password hashes, tokens, internal counters. Pages and clients never see `passwordHash`.

### 7.4 Seed

Idempotent. Creates a demo user (documented in README) **pre-verified**. Enough rows that the dashboard and at least one chart are non-empty. Seed imports `hashPassword` from `password.ts`, never a duplicated scrypt.

### 7.5 Migrations

`db push` is for local throwaway SQLite. Production PostgreSQL uses `prisma migrate`. Document the provider swap in `.env.example` **and test it once** before claiming Postgres support.

---

## 8. App shell, navigation, dashboard

### 8.1 Layout

Use route groups:

- `(marketing)` — landing, about, contact, legal. No session required.
- `(app)` — dashboard and all product pages, wrapped in the shell.

Shell pieces (separate files, layout imports them):

- `sidebar.tsx` — desktop nav from `nav-config.ts`
- `topbar.tsx` — title, search, user menu
- `mobile-nav.tsx` — Sheet/drawer, focus-trapped, Escape-closes, scroll-locked, tap navigates **and** closes
- `app-shell.tsx` — composes the three

**Three responsive states:** phone (drawer), tablet (collapsed rail or drawer), desktop (persistent sidebar). A control whose target is `hidden md:flex` must itself be `hidden md:flex` — chips that flip `aria-pressed` with no visible effect lie.

**Do not** rewrite all product paths onto `/` and route in Zustand. That is an SPA inside the App Router (ORBITAL). Real folders, real layouts.

**One URL casing.** Prefer lowercase `/dashboard`. If you must redirect legacy paths, do it in `src/proxy.ts` (Next 16.3+ convention) with **exact** pathname matching. `next.config` `redirects()` sources are case-insensitive and will self-loop.

### 8.2 KPI cards

One presentational family (label, value, delta, hint). Grid: `grid-cols-1 sm:grid-cols-2 lg:grid-cols-N`. Values use `tabular-nums`. Data comes from a **pure derivation** in `src/lib/dashboard.ts`, unit-tested, not from ad-hoc `reduce` in the component.

### 8.3 States (non-negotiable)

Every surface has explicit:

- **loading** — skeleton or labeled pending, not a blank hole;
- **empty** — what to do next, not “No data”;
- **error** — what failed + retry;
- **success / seeded**.

Disable submit buttons while in-flight. Remount dialogs via `key={open}` so stale form state cannot survive.

### 8.4 Login card

Walk **every** mode (sign-in, sign-up, verify, forgot, reset) before declaring the card done. Modes often restructure chrome (logo present on sign-in only, etc.). `window.location` redirects break the server-component header swap — use `router.push` + `router.refresh()`.

---

## 9. Charting

### 9.1 One module, typed wrappers

`src/components/charts/charts.tsx` is the only file that imports `recharts`. Pages pass `data` + keys + tokens.

Minimum family (port from neo-crm, restyle):

| Wrapper | Use |
|---|---|
| `SingleBarChart` | one series, vertical bars |
| `GroupedBarsChart` | two series + Legend |
| `TrendLineChart` | 1–2 lines |
| `RevenueLineChart` / area | filled trend |
| `LabelPieChart` | distribution |
| `HorizontalBarChart` | ranking / funnel-like |
| `Sparkline` | KPI card inset (CSS bars are acceptable for 8–12 points) |

Formatters (`dollarFormatter`, `numberFormatter`, `percentFormatter`) live next to the wrappers.

### 9.2 Rules that prevent week-long chart bugs

- Derivations are **pure functions** in `src/lib/*-data.ts`. Components do not group/filter.
- Empty and all-zero data still render axes (or an explicit empty state — pick one and test both).
- `isAnimationActive={false}` in tests/e2e; animation fights screenshots and tooltip probes.
- Do not pass `tick={undefined}` explicitly — recharts spreads defaultProps and an explicit undefined **kills** ticks, collapsing the grid to a frame.
- Tooltips: prefer stock Tooltip + a formatter. Custom `content` is a drift magnet.
- Colors come from tokens, not magic hex in the page.
- Accessible name: the wrapping figure/card has a heading; the SVG is `aria-hidden` if the numbers are also in text.

### 9.3 Chart testing ladder

1. Unit-test the derivation (golden totals).
2. Unit-test wrapper props (grid on/off, formatter wired, height).
3. E2E: seeded dashboard shows the expected KPI text; empty dashboard does not crash.

Do not pin 300 class strings from a reference DOM unless you are cloning that reference.

---

## 10. State management

**ONE Zustand store.** Additional stores require an ADR.

- All server reads/writes go through `call()`.
- Session user lives in the store, hydrated from `/api/auth/me` on shell mount.
- Race token: a slow list fetch must not overwrite a newer one. Increment a generation on each request; ignore stale responses.
- Derived selectors: `useShallow`. Without it, returning a new object from a selector re-renders always.
- Dialog forms: remount via `key`. Do not reset fields in `useEffect`.
- Toast infrastructure: if a module-level singleton, park it on `globalThis` and subscribe with `useSyncExternalStore`. Turbopack code-splitting otherwise hands **two** copies to two chunks and toasts fire into the void.
- The store does **not** own routing.

---

## 11. Component architecture

**Golden rule: imports point down only.**

```
app/pages  →  domain components  →  layout  →  ui primitives  →  lib
```

- `components/ui/*` wrap Radix. No domain names in ui.
- Domain components do not import from `app/`.
- Server Components by default. `"use client"` only where state, effects, or browser APIs exist.
- Colocate a component with its tests only if the seam is pure (`lib`). Keep Playwright in `tests/e2e`.

---

## 12. Accessibility

WCAG 2.2 AA is the floor.

- Semantic headings, one `h1` per page.
- Visible focus rings (tokenized).
- Icon-only buttons have `aria-label`.
- Drawer: focus trap, Escape, return focus, `aria-hidden` on the rest of the app (Radix does this — **Playwright role locators go blind while it is open**; use `aria-controls` or testids).
- Tabs: keyboard contract (arrows, Home/End) if you roll your own; prefer Radix Tabs.
- Contrast: pin brand/accent against surface with a unit test if you have been burned (the donors were).
- `axe-core` in at least one Playwright spec (login + dashboard).
- Do not disable zoom.

---

## 13. Testing

### 13.1 Three tiers

| Tier | Tool | What it pins |
|---|---|---|
| Unit | Vitest, node env | Pure seams: db-path, password, rate-limit, schemas, money, dashboard math, chart derivations, serializers |
| Smoke | bash + curl against standalone | Health (DB up), unauth 401, register→verify→login, CRUD, 11th login 429, pages return 200 |
| E2E | Playwright vs **production** standalone | Auth walk, mobile nav, empty+seeded dashboard, a11y, one chart, one destructive confirm |

**The dev server lies about production.** Standalone has different CWD, traced schema, minifier, and env. E2E that hits `next dev` will not catch the db-path trap.

### 13.2 Hermeticity

- E2E uses its **own** SQLite file (`db/e2e.db`). Never the dev DB.
- Setup project logs in **once**, saves `storageState`. Per-test logins trip the rate limiter.
- `workers: 1` for suites that share a DB or a limiter.
- Kill squatters on the e2e port before boot (`reuseExistingServer` will happily reuse a stale standalone).
- `CI=1` for Playwright in the gate.

### 13.3 Test-quality doctrine

- Assert observable behavior, not that a mock was called.
- Auth, tenancy (user B cannot read user A's row), validation, and money are mandatory.
- Do not copy 2,000 reference-parity class-string pins into a greenfield app.
- Never delete, skip, or weaken a test to make a gate pass.

---

## 14. Quality gate

```bash
bun run lint          # --max-warnings 0
bun run typecheck     # tsc --noEmit
bun run test          # vitest run
bun run build         # next build (types ON) + standalone copy + rm .env
./scripts/smoke-test.sh
CI=1 bun run test:e2e
```

Package this as `"gate"`. There is no hosted CI until you add one — the local gate is the only gate, and skipping it is how the donors shipped forgeable sessions.

Order is load-bearing: lint before typecheck before tests before build before e2e. Autofixers can drift formatters; if you add a formatter, run it after lint.

---

## 15. Deployment & production

### 15.1 Artifact

`.next/standalone/server.js` + `.next/static` + `public` + `prisma/` (schema + client). Confirm with `ls` that `.env`, `.git`, `db/*.db`, and `skills/` are **absent**.

### 15.2 Runbook (`docs/DEPLOYMENT.md`)

Must include: generating `AUTH_SECRET`, absolute `DATABASE_URL` for prod, proxy hop count, kill-switches, health URL, how to seed, how to rotate the secret (it logs everyone out), backup of SQLite / Postgres.

### 15.3 Health

`GET /api/health` runs `SELECT 1`. Success `{ ok: true, data: { status: "healthy", db: "up" } }`. Failure **503**. A 200 with `db: "down"` is a lie — monitoring will not page.

### 15.4 Scale-up path (documented, not built)

| When | What |
|---|---|
| Second node | Move rate limits and (if you add them) jobs to Redis |
| Bigger-than-SQLite | Postgres + `prisma migrate` (test this *before* the incident) |
| Real email | Mailer + kill-switches on |
| Org/SaaS | `orgId` + membership table + RBAC |
| Observability | Structured logs, request id, metrics on 5xx/429/latency |

---

## 16. AI features (optional)

If the app has an assistant:

- Server-side only. Dynamic import the SDK.
- **Degrade, never fail.** Deterministic parser fallback when the SDK is missing, times out, or `DISABLE_AI_LLM=1` (e2e uses this).
- Sanitize model output before it hits Prisma (enums, numeric clamps, ownership). Never execute raw SQL from a model.
- Rate-limit separately (e.g. 20 / 5 min).
- If you do not have an assistant, **do not depend on `z-ai-web-dev-sdk`**.

---

## 17. Anti-patterns & hard-won bugs

Each item happened in at least one donor.

1. **`tailwind.config.js` in v4** → flat/minimal look. Tokens in `@theme` only.
2. **`var(--font-*)` inside `@theme`** → silent UA serif. Literal font names.
3. **`ignoreBuildErrors: true`** → deployable artifact with type errors. Retire it.
4. **`reactStrictMode: false`** to hide double-effect bugs. Fix the effects.
5. **SPA rewrites onto `/`** → fights the App Router. Real routes.
6. **Module-level client singletons** under Turbopack → split copies. `globalThis` + `useSyncExternalStore`.
7. **`next.config` redirects for casing** → self-loop. `src/proxy.ts` exact match.
8. **React 19 `set-state-in-effect`** is a lint **error**. Adjust during render or fetch in an effect without sync setState, or remount via key.
9. **`window.location` auth redirects** → lost Set-Cookie. `router.push` + `refresh`.
10. **Shell-inherited `DATABASE_URL`** → Error 14 / wrong file. `db-path.ts` + `env -u`.
11. **Minifier-dropped db-path helpers** → production opens the wrong DB. Side-effect `roots.push`.
12. **Unknown-email login skips scrypt** → user-oracle. Timing equalizer.
13. **Reset without `tokenVersion`** → stolen cookies survive a reset.
14. **Raw reset token in DB** → DB read mints URLs. Hash at rest.
15. **Verification code in JSON in production** → not email ownership. Kill-switch + mailer.
16. **`requireSession` without `userId` on the query** → any user sees all rows.
17. **`role` column unused** → implied authz. Enforce or delete.
18. **Auth `AUTH_SECRET` fallback in production** → forgeable sessions. Throw at boot.
19. **Health 200 when DB down** → monitoring theater. 503.
20. **Standalone ships `.env`** → tracing excludes + `rm -f .next/standalone/.env`.
21. **Per-test e2e logins** → 429 flake. `storageState`.
22. **E2E against `next dev`** → misses standalone traps.
23. **`tick={undefined}` on recharts** → grid collapses. Omit the prop.
24. **Silent CSV formula injection** → `=` cells become formulas. Prefix.
25. **Testing or compiling `skills/`** → exclude it everywhere.
26. **Inventing UI the spec does not have.** Measure, then build.
27. **Dead controls below a breakpoint.** Hide the control with its target.
28. **Duplicating scrypt in `seed.ts`.** Import `password.ts`.
29. **Returning Prisma rows.** Serialize.
30. **Summing money as floats.** Integer cents.

---

## 18. Debugging guide

| Symptom | First check | Likely cause |
|---|---|---|
| `Error code 14: Unable to open the database file` | `[db] DATABASE_URL ->` log; `env \| grep DATABASE` | Env shadowing / wrong db-path anchor |
| Prod uses a different DB than CLI | Which anchor won in db-path | Standalone traced-schema / chdir |
| `ERR_TOO_MANY_REDIRECTS` | `redirects()` touching that path | Next 16 case-insensitive sources |
| Toast fires, never shows | Two module instances? | Turbopack singleton split |
| E2E cannot see mobile-nav | Role locator while sheet open | Radix `aria-hidden` on the app |
| E2E uses stale build | `pkill -f standalone/server.js` | `reuseExistingServer: true` |
| Rate limiter blocks the suite | Setup project / storageState | Per-test logins |
| Pages unstyled | `postcss.config.mjs`, no `tailwind.config.js` | Missing `@tailwindcss/postcss` |
| Whole app in serif | `@theme` font-sans | `var(--font-inter)` trap |
| Login 401 after reset | tokenVersion | Expected — old cookie is dead |
| Chart has a frame, no grid | `tick` prop | Explicit `undefined` |
| Build green, tsc red | `ignoreBuildErrors` | Retire it |
| Artifact contains secrets | `.next/standalone/.env` | Tracing copy; `rm` in build script |
| 11th login not 429 | Proxy hops / XFF | Limiter keying on the wrong hop |

---

## 19. Documentation contract

| Doc | Audience | Hard cap | Contains |
|---|---|---|---|
| `README.md` | Humans | — | What it is, features, boot, demo login, license |
| `AGENTS.md` | Operators / agents | ~300 lines | Commands, traps you'd guess wrong, conventions |
| `CLAUDE.md` | Agents | ~600 lines | Principles, stack, anti-patterns, success metrics |
| `PAD` | Architects | — | ADRs, threat model, schema, deploy |
| `SKILL.md` | This file's descendant | ~1,200 lines | Contracts. **No session diary** |

Session logs, if you keep them, live under `docs/sessions/` and are **not** appended into SKILL.md. neo-crm's 12,378-line skill is the existence proof that a skill can drown its own contracts.

Count lockstep: when a check count or route count changes, `rg` the old number.

---

## 20. Pre-ship checklist

```bash
bun run lint && bun run typecheck && bun run test
bun run build && ./scripts/smoke-test.sh && CI=1 bun run test:e2e
git status          # no .env, *.key, db/*.db, dev.log, server.log
```

Manual / automated must-haves:

- [ ] Missing `AUTH_SECRET` in production → process exits
- [ ] Unauthenticated API → 401 envelope
- [ ] User A cannot read User B's rows (test)
- [ ] 11th login / 15 min → 429 + Retry-After
- [ ] Dashboard: empty, loading, error, seeded
- [ ] At least one chart family renders zero-data and seeded
- [ ] Mobile 390×844: hamburger → drawer → navigate AND close
- [ ] Security headers present
- [ ] Health 503 when DB is down
- [ ] `.next/standalone` has no `.env`
- [ ] Kill-switches documented; mailer or in-app delivery named honestly
- [ ] Five docs updated in the same commit

---

## Appendix A — Six-phase workflow

Inherited from the donor family's “meticulous approach.” Use it on every non-trivial change.

1. **Recon** — read the files you will touch, in full. Confirm versions.
2. **Plan** — smallest path that preserves correctness and security. List failure modes (bad input, empty data, stale fetch, missing secret).
3. **Implement** — seams first (lib + tests), then handlers, then UI.
4. **Prove** — unit → typecheck → lint → build → smoke → e2e. If a gate is red, fix the cause, do not weaken the gate.
5. **Document** — SKILL/PAD/AGENTS/README as needed, same commit.
6. **Pre-mortem** — malicious input, concurrency, missing env, empty seed. Either handled or explicitly out of scope.

---

## Appendix B — Donor matrix

| Concern | Canonical donor | Do not copy |
|---|---|---|
| App shell, charts, gate, boot-env, Zod API, tracing excludes | **neo-crm** | CRM entities, 90 KB `page-layout.ts`, 12k-line SKILL, capitalized duplicate routes |
| Tenancy, money, serializers, small store | **zero-balance** | 30-day cookies, no reset, `reactStrictMode: false`, `error: string` envelope |
| Auth threat model, X-Frame-Options, proxy hops, SKILL *shape* | **digma** | Canvas editor, `ignoreBuildErrors`, global (non-tenant) data |
| Process, four-doc contract, smoke skeleton, compact AGENTS | **project-management** | SPA rewrites, `src/lib/router.ts`, incomplete auth |

Full keep/strip/port lists: `docs/hybrid-assembly-guide.md`. Ranking: `docs/codebase-evaluation-ranking-report.md`.

---

## Appendix C — Quick reference card

```
Boot       bun install && cp .env.example .env && bun run db:push && bun run db:seed && bun run dev
Fast gate  bun run lint && bun run typecheck && bun run test
Full gate  bun run build && ./scripts/smoke-test.sh && CI=1 bun run test:e2e
Schema     env -u DATABASE_URL prisma db push   # CLI; runtime uses db-path.ts
E2E env    own port · DATABASE_URL=file:../db/e2e.db · workers:1 · storageState · DISABLE_AI_LLM=1

Sessions   scrypt(16B salt, 64B key, prefix scrypt:) · HMAC-SHA256 · 7d
           httpOnly/lax/secure · tokenVersion revocation · hashed reset tokens
Limits     login 10/15m · register 10/15m · resend 5/15m · verify 20/15m
           forgot 10/15m · reset 10/15m · 429+Retry-After · PROXY_HOPS fail-closed
Envelope   {ok:true,data} | {ok:false,error:{code,message}} · requireSession() first line
Tenancy    every model: userId + cascade + @@index([userId,…]) · findFirst({id,userId}) → 404
Charts     one charts.tsx · wrappers only · pure derivations in lib · isAnimationActive={false}
Store      ONE Zustand store · call() only · useShallow · no routing in the store
Tokens     literal hex in @theme inline · NO tailwind.config.js · font NAMES not vars
Build      no ignoreBuildErrors · tracing excludes · rm standalone/.env · health SELECT 1 → 503
```

---

## Appendix D — Production gaps this skill does not close

Close these explicitly before calling a deployment production. None of the four donors solved them.

| Gap | Why it matters | Direction |
|---|---|---|
| Real email transport | OTP/reset in JSON is not ownership proof | SES/Resend/SMTP + kill-switches on |
| Enforced RBAC | A `role` column is not authorization | Gate routes or omit the column |
| Org-level tenancy | `userId` is not a company | `orgId` + membership |
| Hosted CI | Local `gate` is skippable | GitHub Actions (or equivalent) on PR |
| Containers | “It works on my Bun” | One-process Dockerfile, read-only FS, secrets via env |
| Distributed rate limit | Second node doubles the budget | Redis/Upstash |
| Observability | You cannot diagnose what you do not log | Structured logs, request id, 5xx metrics |
| Tested Postgres | Documented ≠ tested | One CI job against Postgres |
| License on forks | Only neo-crm shipped MIT in-tree | Confirm before publishing |

---

*Skill v2.0.0 — 2026-10-23. Distilled from four clones; ranking report is the evidence trail.*
