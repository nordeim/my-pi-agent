---
name: web-app-foundation
description: >
  Master engineering skill for scaffolding, extending, or remediating ANY production
  web application with authentication, a dashboard, and charting on Next.js 16 App
  Router + React 19 + TypeScript strict + Tailwind CSS v4 (CSS-first) + Prisma +
  SQLite/PostgreSQL + Zustand + recharts. Distilled and generalized from four
  sibling production codebases (digma, neo-crm, project-management, zero-balance —
  1,177 commits of build/remediation history). Covers the full stack: env contract,
  db-path seam, scrypt+HMAC auth with verification/reset/revocation, zod-validated
  API envelope, per-user tenancy, KPI dashboard shell, 7-family chart layer,
  race-guarded store, degrade-never-fail AI, three-tier testing, quality gates,
  and the documentation contract. Use whenever creating a new web app codebase,
  adding auth/dashboard/charts to an existing one, or auditing one built from
  this skill.
version: 1.0.0
last_updated: 2026-10-22
audience: "engineers + AI agents building, extending, debugging, onboarding, or replicating a production web application"
provenance: "Generalized from digma_SKILL.md v1.148, neo-crm_SKILL.md v1.158, project-management_SKILL.md v1.0, zero-balance_SKILL.md v1.0 and their four codebases"
---

# Web App Foundation — Master Engineering Skill

> **How to use this document.** You are an engineer or agent about to build, extend, or repair a web application. **Do not guess** — this file is the single source of every hard-won lesson the stack will not tell you by reading one file.
>
> | If you are… | Read first |
> |---|---|
> | Starting a new app from zero | §1 Pre-Flight → §19 Scaffolding Workflow, then §2–§4 |
> | Wiring auth | §6 (the whole section) + §12 |
> | Building a dashboard or charts | §8 + §9 |
> | Adding an API route | §7 + §5.3 |
> | Debugging styles/layout breakage | §18 Tailwind v4 Trap Register |
> | Debugging DB "unable to open database file" | §5.2 db-path seam |
> | About to ship | §14 Pre-Ship Checklist (gates as commands, in order) |
> | Writing or updating docs | §15 Documentation Contract |
>
> Every prescription below was proven in at least one of the four source codebases; where they disagreed, this skill takes the best implementation and says so. When code and this document disagree, **the code wins — update the doc in the same commit.**

## Table of Contents

- §0 Scope, Trigger & Operating Contract
- §1 Pre-Flight Intake
- §2 Golden-Path Stack
- §3 Project Structure Blueprint
- §4 Bootstrapping & Configuration
- §5 Data Layer Standard
- §6 Authentication Standard
- §7 API Layer Standard
- §8 Dashboard Shell Standard
- §9 Charting Standard
- §10 State Management Standard
- §11 AI Feature Standard (optional module)
- §12 Security Hardening Checklist
- §13 Testing Strategy
- §14 Quality Gates & Pre-Ship Checklist
- §15 Documentation Contract
- §16 Production Deployment
- §17 Anti-Patterns & Hard-Won Lessons
- §18 Tailwind CSS v4 Trap Register
- §19 Scaffolding Workflow (Phases 0–9)
- Appendix A: Quick Reference Card
- Appendix B: Production Gap Closure List

---

## §0 Scope, Trigger & Operating Contract

**In scope:** single-deployable web applications — SaaS products, admin panels, internal tools, dashboards, clones — that need (a) cookie-session auth, (b) an authenticated dashboard shell, (c) data visualization, (d) a validated JSON API, (e) a relational store.

**Out of scope (use different foundations):** static sites, heavy realtime/multiplayer, content sites needing a CMS, monorepos with multiple deployables, apps requiring OAuth-first identity (this skill's auth is email+password with verification/reset; OAuth is an add-on).

**Operating contract:**

1. **One deployable unit.** No microservices, no external auth service, no Redis in v1. SQLite file + cookie sessions + optional LLM SDK. `bun run build` produces a standalone server. (Proven: all four source apps. ADR-style rationale: single artifact, one lockfile, one test runner; scale-up paths documented in §16.3.)
2. **Seams over frameworks.** Logic that could break silently (auth crypto, rate limiting, path resolution, validation, domain math, chart derivations) lives in pure, framework-free modules under `src/lib/` with unit tests. Route handlers are thin orchestration only.
3. **Degrade, never fail.** Optional subsystems (AI, emails in dev, enrichments) fall back to deterministic outputs; the app never 500s on an optional dependency outage.
4. **Evidence over assertion.** Visual claims come from computed-style probes, not screenshots. Behavior claims come from executed tests. Counts in docs come from the tools' own census.
5. **Tenancy is not optional.** Every domain row is owned by a user. A template without per-user data scoping is a demo, not a foundation (this was digma's and project-management's highest-severity gap — do not repeat it).

---

## §1 Pre-Flight Intake

Before writing any code, collect these from the requester. If more than one is unanswerable, ask the single highest-impact question first; otherwise proceed on stated assumptions.

| # | Question | Why it changes the build |
|---|---|---|
| 1 | **Domain entities & relations** (the 3–8 nouns the app manages) | Drives the Prisma schema (§5.1); everything else hangs off it |
| 2 | **Auth depth**: open signup vs invite, email verification required?, password reset needed?, roles? | §6 has modular tiers; skipping reset/verify halves auth work but forfeits production |
| 3 | **Dashboard KPIs**: which 4–8 numbers matter, and their time windows | Drives stats routes + derivation seams (§8, §9.4) |
| 4 | **Charts**: which types (bar/line/pie/funnel/area)? | §9 wrapper families are pre-built; pick from the menu |
| 5 | **Scale envelope**: expected users, single-node acceptable? | Confirms SQLite + in-memory limiter (default) vs Postgres + Redis (§16.3) |
| 6 | **Email**: real transport (SMTP/Resend) in production? | Without it, verification/reset codes stay dev-only (Appendix B) |
| 7 | **AI features**: any LLM-assisted generation/planning? | Adds §11 module; must ship sanitizer + fallback |
| 8 | **Brand/design direction**: palette, light/dark, typography | §4.4 token system needs literal hexes before components exist |

**Definition of Ready to start building:** 1–3 answered (rest can default). **Definition of Ready to ship:** all 8 answered or explicitly deferred.

---

## §2 Golden-Path Stack

| Layer | Technology | Version floor | Rationale (proven in source repos) |
|---|---|---|---|
| Web framework | Next.js, App Router, `output:"standalone"` | 16.4 | Single-process RSC + route handlers as the API; async `cookies()`/`params` |
| UI runtime | React | 19.3 | `useSyncExternalStore` for cross-chunk stores; `inert` boolean prop; no `forwardRef` needed |
| Language | TypeScript, `strict:true` | 5.9 | Prefer full strict incl. `noImplicitAny`; if sandbox-forced off, the `typecheck` gate compensates |
| Styling | Tailwind CSS v4 CSS-first (`@theme` in `globals.css`) | 4.3 | Zero JS config; literal-hex tokens; see §18 traps before touching gradients or config files |
| Animation | `tw-animate-css` (vendored if Turbopack drops the export) | 1.4 | Radix enter/exit classes; add `prefers-reduced-motion` collapse |
| Primitives | Radix UI (dialog, dropdown-menu, select, sheet, tabs, label, slot, popover) via shadcn-style wrappers | per-package | Never hand-roll focus management; wrap and style |
| Icons | lucide-react | 0.525 | One icon set; two-class stroke system (nav 1.8 / content 2.0) |
| State | Zustand | 5.0.15 | ONE store; race guards (§10); `useShallow` discipline |
| ORM / DB | Prisma + SQLite (dev) / PostgreSQL (prod option) | 6.11+ | `db push` dev loop; migrate to `prisma migrate` when data matters (§5.4) |
| Validation | zod | 4.6 | At EVERY API boundary (§7.2) — zero-balance's decisive advantage |
| Charts | recharts | 3.x (2.15 acceptable) | Wrapper families in §9; React-19 compatible |
| Auth | Node `crypto` (scrypt + HMAC-SHA256) | built-in | No auth library — §6 mechanics are smaller than the integration surface of next-auth/better-auth for this shape (ADR-tested across all four repos) |
| AI (optional) | `z-ai-web-dev-sdk` (or any SDK) | latest | Server-side only, dynamic import, §11 discipline |
| Unit tests | Vitest | 5.0 | Pure-seam tests, node env |
| E2E tests | Playwright | 1.63 | Against the production standalone build (§13.3) |
| Runtime | Bun (dev + prod) or Node ≥ 20 | 1.3 | Scripts assume repo-root execution (§5.2) |

**Deliberately absent:** React Query/SWR (one store + explicit refresh; a second cache layer is a sync bug factory at this scale), auth libraries (§6 rationale), Redux, Axios, moment, CSS-in-JS, dark-mode-by-default (add via §4.4 if the brand requires).

---

## §3 Project Structure Blueprint

```
<repo>/
├── src/
│   ├── app/                        # Next.js App Router
│   │   ├── layout.tsx              # root layout, metadata, fonts, Toaster
│   │   ├── page.tsx                # landing OR the authenticated shell entry
│   │   ├── globals.css             # THE token file (@theme, §4.4)
│   │   ├── login/page.tsx          # real route (never rewritten)
│   │   ├── (app)/                  # route group — layout guard calls getSessionUser()
│   │   │   ├── layout.tsx          # redirects to /login?from_url=… when null
│   │   │   └── dashboard/page.tsx  # one real route per top-level view
│   │   ├── api/
│   │   │   ├── health/route.ts     # bare probe (the one unguarded route + auth family)
│   │   │   ├── auth/               # register, login, logout, me, verify-otp,
│   │   │   │                       # resend-otp, forgot-password, reset-password
│   │   │   ├── stats/route.ts      # dashboard KPIs
│   │   │   └── <entity>/…          # thin CRUD wrappers (§7)
│   │   ├── robots.ts / sitemap.ts  # force-dynamic metadata routes
│   │   └── not-found.tsx           # custom 404 (test it)
│   ├── components/
│   │   ├── ui/                     # shadcn-style Radix wrappers ONLY
│   │   ├── charts/charts.tsx       # §9 wrapper families (one file)
│   │   ├── layout/                 # app-shell, sidebar, topbar, mobile-nav
│   │   └── <domain>/               # views, dialogs, cards per domain entity
│   ├── lib/                        # THE SEAMS — pure, tested, framework-free
│   │   ├── auth.ts                 # §6 session mint/verify/cookie
│   │   ├── password.ts             # scrypt hash/verify + timing equalizer
│   │   ├── rate-limit.ts           # §6.6 fixed-window limiter + client-IP
│   │   ├── validation.ts           # zod schemas + parseBody + bounded reader
│   │   ├── api.ts                  # ok()/fail() envelope + requireSession()
│   │   ├── api-helpers.ts          # parseBody discriminated result, ownership helpers
│   │   ├── db.ts                   # single sanctioned PrismaClient
│   │   ├── db-path.ts              # §5.2 SQLite URL resolution seam
│   │   ├── serializers.ts          # row→DTO translation (the ONLY such place)
│   │   ├── money.ts                # (if quantifiable domain) integer-minor-unit firewall
│   │   ├── csv.ts                  # §7.5 RFC-4180 + formula-injection guard
│   │   └── <domain>-data.ts        # pure chart/KPI derivation seams (§9.4)
│   ├── stores/<app>-store.ts       # ONE Zustand store (§10)
│   └── hooks/                      # use-media-query, use-toast
├── prisma/
│   ├── schema.prisma
│   └── seed.ts                     # idempotent; drives every chart/KPI (§5.5)
├── tests/
│   ├── <seam>.test.ts              # unit (Vitest, node env)
│   └── e2e/                        # Playwright specs + auth.setup + global-setup
├── scripts/
│   └── smoke-test.sh               # §13.4 env-pinned HTTP gate
├── .env.example                    # complete env contract, commented
├── AGENTS.md / CLAUDE.md / README.md / Project_Architecture_Document.md / <app>_SKILL.md
└── package.json                    # gates: lint, typecheck, test, build, smoke, e2e
```

**Rules:** (1) nothing in `src/lib/` imports React; (2) nothing outside `serializers.ts` shapes API payloads; (3) route handlers do orchestration only — parse → authorize → query → serialize → envelope; (4) one chart file; (5) exclude any non-app catalogs (`skills/`-style) from tsconfig/eslint/vitest or don't commit them.

---

## §4 Bootstrapping & Configuration

### 4.1 First-run sequence (canonical)

```bash
bun install
cp .env.example .env            # DATABASE_URL="file:../db/custom.db", AUTH_SECRET=$(openssl rand -hex 32)
bun run db:push                 # schema → db/custom.db
bun run db:seed                 # idempotent demo data
bun run dev                     # :3000 — demo login from seed
```

### 4.2 next.config.ts — the load-bearing lines

```ts
const nextConfig: NextConfig = {
  output: "standalone",
  outputFileTracingRoot: __dirname,   // prevents nested standalone paths when a parent lockfile exists
  typescript: { ignoreBuildErrors: true },  // ONLY if a typecheck gate exists; prefer omitting (zero-balance posture)
  headers: async () => [ /* X-Frame-Options: DENY, X-Content-Type-Options: nosniff, Referrer-Policy */ ],
};
```

If you set `ignoreBuildErrors`, then **`bun run typecheck` (tsc --noEmit) is a mandatory pre-ship gate** — it is the only thing catching type errors. Zero-balance proves you can omit it entirely; prefer that.

### 4.3 tsconfig / eslint / vitest / playwright contracts

- `tsconfig.json`: `strict: true`, `@/* → src/*`, **exclude non-app catalogs**.
- `eslint.config.mjs`: next/core-web-vitals + next/typescript. Do not disable `no-explicit-any`/`no-unused-vars`/`exhaustive-deps` unless you substitute a hygiene test (§13.5) — three of four source repos disabled them and relied on discipline; the fourth (neo-crm) replaced them with dead-code-hygiene tests that work.
- `vitest.config.ts`: include `src/**/*.test.ts` + `tests/**/*.test.ts` ONLY (never `.spec.ts`); node environment; `@` alias.
- `playwright.config.ts`: testDir `tests/e2e`; webServer = production standalone on **:3100** with **its own `db/e2e.db`**; `workers: 1`; a `setup` project that logs in once and saves `storageState` (coexists with the rate limiter); `retries: 0`, trace retain-on-failure.

### 4.4 The token file (globals.css)

All brand/semantic tokens in **one** `@theme` block with **literal values** (the v4 build drops `var()` chains in a plain `@theme`; §18-T1):

```css
@import "tailwindcss";
@import "tw-animate-css";

@theme {
  --color-background: #ffffff;      /* literal hex, never var(--x) */
  --color-foreground: #0f172a;
  --color-primary: #8b5cf6;         /* brand accent */
  --color-muted: #f9fafb;
  --color-border: #e5e7eb;
  --color-chart-1: …; --color-chart-2: …;   /* chart palette as named tokens */
  --font-sans: "Inter", "Inter Fallback", ui-sans-serif, system-ui;  /* NAMES, not var(--font-x) */
  --radius: 0.5rem;
}
```

Rules proven across all four repos: **never** a Tailwind default-palette class for brand color; gradients as inline `style="background: linear-gradient(135deg, var(--a), var(--b))"` (§18-T2); `prefers-reduced-motion: reduce { * { animation-duration: .01ms !important; transition-duration: .01ms !important } }`; a global `:focus-visible` ring; THREE card tiers max (canvas / raised / well) with at most two shadow pairs each.

### 4.5 Environment contract (`.env.example` — complete, commented)

| Variable | Required | Purpose |
|---|---|---|
| `DATABASE_URL` | yes | `file:../db/custom.db` (resolves against `prisma/` — §5.2). Postgres: `postgresql://…` |
| `AUTH_SECRET` | production | HMAC key, `openssl rand -hex 32`. **Fail hard in prod if missing/short** — do NOT ship a silent dev fallback (§12) |
| `NEXT_PUBLIC_SITE_URL` | recommended | `metadataBase`, sitemap origin |
| `APP_REPO_ROOT` | no | Explicit repo-root anchor for the db-path seam (container escape hatch) |
| `PROXY_HOPS` | no | XFF trust depth for client-IP resolution (§6.6); `0` = ignore headers |
| `DISABLE_IN_APP_OTP` / `DISABLE_AI_LLM` | no | Dev/e2e determinism knobs |

---

## §5 Data Layer Standard

### 5.1 Schema rules (Prisma)

1. **Every domain model carries `userId` with `onDelete: Cascade`** and an index leading on it (`@@index([userId, createdAt])`). This is the tenancy firewall — zero-balance is the reference implementation; digma/project-management's omission was their highest-severity defect.
2. `User` model auth columns: `email @unique`, `passwordHash`, `emailVerifiedAt DateTime?`, `verificationCodeHash String?` (**hashed**, neo-crm's improvement), `verificationAttempts Int @default(0)`, `resetTokenHash String?` (**hashed**), `resetTokenExpiresAt DateTime?`, `tokenVersion Int @default(0)` (§6.5 revocation).
3. **Strings + zod enums, not Prisma enums** (SQLite parity; the zod schema in §7.2 is the single vocabulary source; keep a `constants.ts` for UI-facing lists).
4. **Quantifiable money/quantities:** decide the unit at the boundary. Either store integer minor units (`Int`, zero-balance's documented intent) or store `Float` and enforce an **integer-cents aggregation firewall** (`money.ts: toCents/fromCents/sumAmounts`) — floats live only at the format boundary. Never `parseFloat` two user amounts and add them.
5. Indexes: composite `[userId, <filter column>]` beats single-column multiples; delete redundant singles deliberately and record why.
6. Soft deletes: skip (YAGNI at this scale); audit trails: add an `ActivityLog` model (type, entity, meta JSON, `@@index([createdAt])`) only if the domain narrates mutations.

### 5.2 The db-path seam (mandatory, universal trap-solver)

**The trap:** relative SQLite URLs resolve against different directories per runner — Prisma CLI resolves `file:../db/custom.db` against `prisma/`, but the **Next standalone server `chdir`s into `.next/standalone`** at boot, so the same URL silently points somewhere else ("Error code 14: Unable to open the database file"). Parent-workspace `.env` or an exported shell `DATABASE_URL` shadows the repo's own — the failure bit two source repos twice.

**The seam** (`src/lib/db-path.ts`, ~110 lines + fixture tests — port from any source repo):
1. If `DATABASE_URL` is absolute or non-SQLite → pass through.
2. Resolve relative against the first **anchor directory containing `prisma/schema.prisma`**, tried in order: (a) CWD detecting the standalone layout (basename `.next/standalone` + `server.js` + grandparent schema → walk two levels up), (b) module root via `import.meta.url` **disk-validated** (bundlers rewrite it), (c) `process.cwd()`.
3. Honor an explicit `APP_REPO_ROOT` override; log the resolved path (redacted) at startup — that log line is the diagnostic.

**Also:** scripts pin their own URL (`DATABASE_URL=file:../db/e2e.db next dev`) or scrub the environment (`env -u DATABASE_URL prisma db push`) — never trust an inherited shell. `db.ts` constructs the one sanctioned `PrismaClient` (globalThis singleton in dev, query logging in dev only).

### 5.3 Query discipline

- **Ownership in the WHERE, not after:** `findFirst({ where: { id, userId } })` → 404 when absent. Never `findUnique({id})` then check ownership in JS (leaks existence; invites drift).
- Handlers never shape rows — `serializers.ts` is the only row→DTO translator (dates→ISO, null→undefined elision), unit-tested.
- Mutations that must be single-use or race-safe use **atomic conditional writes**: `updateMany({ where: { id, resetTokenHash, resetTokenExpiresAt: { gt: now } }, data: … })` and check `count === 1` — not read-then-write.
- Recalculated aggregates: when child rows change, re-sum server-side in the same request and return the parent's new total (`recalcParentAmount` pattern) — no client-side math on money.

### 5.4 Migrations

Dev: `prisma db push` (fast loop; schema is source of truth). **The moment real data exists in any shared environment:** `prisma migrate dev` + committed `migrations/` — `--accept-data-loss` must never appear in a production path. Postgres switch = change `DATABASE_URL` + regenerate; document in `.env.example`.

### 5.5 Seed (make the dashboard real on first boot)

Idempotent (wipe domain tables in a transaction, keep users or re-create the demo user). Volume target: enough rows that **every KPI and every chart shows non-zero, varied data** (neo-crm: 10 accounts / 15 contacts / 24 leads across stages/months — drives all ~20 charts). Use date offsets relative to `new Date()` so time-window KPIs never rot. Assert one load-bearing aggregate in a test (zero-balance freezes its net-zero arithmetic) so seed drift is caught by CI, not users.

---

## §6 Authentication Standard

Hand-rolled on Node `crypto`. No library. **Tier 0** is the floor; **Tier 1** is the default for any production app; Tier 2 optional.

### 6.1 Passwords (`src/lib/password.ts`)

- Hash: `scryptSync(password, salt, 64)` with a fresh 16-byte hex salt per hash; store `salt:hash`; compare with `timingSafeEqual` after length guard.
- **Timing equalization:** on login with an unknown email, burn equivalent scrypt work against a lazily-computed dummy hash before returning the generic 401 — otherwise unknown-email logins answer in ~0ms and enumerate the user table (digma's `timingEqualizerHash`).
- Policy: length ≥ 8 minimum; document that complexity rules are deliberately not enforced.
- Registration returns a generic conflict only if you accept enumeration (digma documents the tradeoff); login and resend are always non-leaking.

### 6.2 Sessions (`src/lib/auth.ts`)

- Token: `userId.tokenVersion.expiry` dot-joined, HMAC-SHA256-signed with `AUTH_SECRET` — **stateless**.
- TTL: 7 days (30 acceptable; pick one and document).
- Cookie: `httpOnly; SameSite=Lax; Secure=(NODE_ENV==="production"); Path=/; MaxAge=TTL`. Custom app name in the cookie (`<app>_session`).
- Verify: `timingSafeEqual` on the digest (fixed length), integer/finite guards on `expiry`; then `getSessionUser` loads the user and **re-checks `tokenVersion`** at the DB seam — this is what makes revocation work (§6.5).
- `AUTH_SECRET`: **fail hard in production when missing or < 32 hex chars.** A console.warn + insecure fallback (three of four source repos) ships forgeable sessions silently — this skill hardens that posture.

### 6.3 Email verification (Tier 1)

- 6-digit code from CSPRNG (`crypto.randomInt`), stored **hashed** (scrypt, like passwords), **15-minute TTL column**, 5-wrong-attempt lockout with the counter incremented **atomically** (`updateMany({ where: { id }, data: { verificationAttempts: { increment: 1 } } })`) — never read-increment-write.
- Resend regenerates + resets the ladder, own rate bucket.
- Verified users skip the gate; unverified login → 403 with a verify prompt (do not open the session).
- Transport: a `Mailer` interface with two adapters — `DevCodeMailer` (logs / returns code in response **only when explicitly enabled by env knob**) and `SmtpMailer`/`ResendMailer` (Appendix B). The route code never knows which.

### 6.4 Password reset (Tier 1 — three of four source repos faked this in the UI; never ship a "reset link sent" toast without an endpoint)

- Forgot: issue a 32-byte hex crypto-random token, store **hashed** + 60-minute expiry; respond 200 with a byte-identical body for known and unknown emails (no enumeration; the ~10ms timing residual is documented and acceptable).
- Reset: consume via **atomic conditional update** carrying `resetTokenHash` AND live expiry in the WHERE (`count === 1` or reject) — single-use and replay-race-safe by construction; clear the token; **increment `tokenVersion`**; do not open a session.
- Transport: same Mailer interface.

### 6.5 Revocation

`tokenVersion` is the mechanism: any "log out everywhere" / password-change / reset bumps it; the DB-seam check in `getSessionUser` invalidates every previously minted cookie. Logout itself clears the cookie (stateless); document that per-session revocation lists are out of scope for v1.

### 6.6 Rate limiting (`src/lib/rate-limit.ts`)

- Fixed-window, per-IP, in-process Map with opportunistic expired-bucket sweep. Buckets: `login:10/15min`, `register:10/15min`, `resend:5/15min`, `verify:20/15min`, `ai:20/5min` (own bucket), heavy-create: `60/5min`. 429 + `Retry-After`.
- **Client IP with declared trust depth** (digma's `PROXY_HOPS`): `0` = ignore XFF entirely (direct exposure); `N≥2` = take the Nth-from-right hop; unparsable → fail closed. Never blindly trust `x-forwarded-for[0]` (zero-balance's documented defect).
- Single-process contract is deliberate; document the Redis upgrade path (§16.3).

### 6.7 Route & page protection

- API: **`requireSession()` is the first line of every handler** except `health` and the auth family. It returns the user or throws the 401 envelope — no route ships without it (a forgotten call is a silent hole; the smoke suite probes every route for 401).
- Pages: a `(app)` route-group `layout.tsx` calls `getSessionUser()` and redirects to `/login?from_url=<path>`; sanitize `from_url` to same-origin paths (`safeFromUrl`).
- RBAC (Tier 2, optional): `role` column + a `requireRole()` helper wrapping `requireSession()`; enforce on routes, not just in UI. If the column exists but nothing checks it, you have documentation, not authorization (neo-crm's gap).

### 6.8 Verification battery (unit tests that must exist)

scrypt round-trip; HMAC verify/expiry/tamper-reject; unknown-email timing equalization; atomic counter race (concurrent increments); reset token single-use (second attempt fails); `tokenVersion` eviction; limiter window reset/block/isolation/sweep; client-IP hop parsing incl. fail-closed; cookie flag symmetry (set vs clear).

---

## §7 API Layer Standard

### 7.1 The envelope (never throw across a handler boundary)

```ts
// src/lib/api.ts
export function ok<T>(data: T, status = 200) { return NextResponse.json({ ok: true, data }, { status }); }
export function fail(code: string, message: string, status: number, headers?: Record<string,string>) { … }
```

`{ ok: true, data } | { ok: false, error: { code, message } }` with **stable codes**: `UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, BAD_REQUEST, VALIDATION, CONFLICT, RATE_LIMITED, VERIFY_EMAIL, VERIFY_LOCKED, UNAVAILABLE, INTERNAL`. Every handler ends in `ok(...)`/`fail(...)` or a typed catch → 500 envelope. All routes `export const dynamic = "force-dynamic"`.

### 7.2 Validation — zod at every boundary (zero-balance's standard)

```ts
const CreateItem = z.object({
  title: z.string().trim().min(1).max(200),
  amount: z.number().finite().min(0).max(1e9),
  dueDate: z.string().regex(/^\d{4}-\d{2}-\d{2}$/).refine(calendarRoundTrip),  // rejects 2026-02-30
  status: z.enum(STATUSES),                       // vocabulary from constants.ts
  note: preprocessEmptyToUndefined(z.string().trim().max(500).optional()),
});
```

`parseBody(req, schema)` returns a discriminated result; the **first zod issue's message becomes the 400**. Bodies are read through a **bounded reader**: check `content-length` fast-path, count streamed chunks, hard-cap (e.g. 32MB generic / 16KB JSON forms), and **reject non-JSON content types on mutating routes** (closes the text/plain login-CSRF class — digma's `readBoundedJson`). Never truncate-and-accept silently; reject.

### 7.3 Handler shape (memorize)

```
rateLimit → requireSession → parseBody(zod) → ownership/FK checks (404)
  → prisma mutation (atomic where applicable) → serialize → ok(...)
```

Status discipline: 200/201 success; 400 validation; 401 unauthenticated; 403 forbidden/unverified; 404 absent-or-not-owned; 409 conflict; 429 limited (+Retry-After); 503 dependency (Prisma connection errors mapped, e.g. P2024/P2028).

### 7.4 Client seam

One `call<T>(url, init)` wrapper unwraps the envelope; network/API failures become **destructive toasts + `null` return** — actions treat null as "abort silently, never re-throw into render." A tiny `ApiError` class carries code+message. No axios.

### 7.5 Import/export hardening (when CSV exists)

RFC-4180 quoting (double the quotes); **formula-injection guard**: prefix `'` on cells starting with `= + @ \t \r` (document the `-` exclusion decision); BOM-tolerant parser; ISO-date filenames. Byte-exact behavioral tests including a HYPERLINK payload. Uploads: session → rate → declared-length pre-gate → `formData()` → MIME allowlist (`image/*`) → size cap → `randomUUID` filename → serve via a **regex-pinned `[name]` route** (32-hex + extension — no traversal surface), immutable cache headers.

---

## §8 Dashboard Shell Standard

### 8.1 Layout (sidebar-first, three responsive states)

- **Desktop ≥1024:** fixed sidebar 240–256px (`--sidebar-width` token) + topbar (search with AbortController + debounce, user dropdown); `main` is the only scroller (`flex h-screen overflow-hidden` structure — the window never scrolls).
- **Tablet 768–1023:** either a collapsed 64px rail or a centered pill nav — pick one, test it.
- **Mobile <768:** top bar + **hamburger → Radix Sheet drawer** with the non-negotiable supersets: focus-trapped, Escape-closable, body-scroll-locked, closes on route change, closes on resize-past-md (matchMedia listener), 44px touch targets. Pinned by a 390×844 e2e spec.
- KPI grid ladders: `grid-cols-1 sm:2 lg:3 xl:6` (per-card, not global).

### 8.2 KPI card family (build once, in `page-parts.tsx`)

`KpiCard` (value, delta badge, `Sparkline`), `BarStatCard`, `IconStatCard`, `CircleStatCard`, `TrendStatCard`, `PageHeader`, `TableEmptyRow`. Deltas/sparklines take **real derived arrays** — never ship static literal KPI numbers (the reference-parity shortcut two source repos inherited; rewire before launch). Every list/table has an explicit `EMPTY_STATE` token.

### 8.3 A11y floor (non-negotiable, e2e-pinned)

Real `<table>` markup; `<label htmlFor>`; `aria-current="page"` on active nav; `aria-expanded/controls` on the hamburger; `role="dialog"/"alert"/"status"` where applicable; full tabs contract (id/aria-controls wiring, ArrowLeft/Right wrap, Home/End); focus-visible ring from the token file; `prefers-reduced-motion` collapse. Best-in-class add-on: **axe-core two-gate** (structural violations must be zero; color-contrast nodes must cite the sanctioned palette) + keyboard walks of dashboard and drawer (zero-balance's pattern).

### 8.4 Loading/error doctrine

Skeletons only where content truly awaits; full-page spinner gated on `booted` is acceptable for the shell. Boot/API failure keeps the user in-app with a one-shot honest toast + retry affordance — never a blank screen, never a silent zero-state (dedicated e2e specs: boot-failure, per-route error injection, empty-states, loading-state with artificial delay).

---

## §9 Charting Standard

### 9.1 One chart module, seven wrapper families (`src/components/charts/charts.tsx`, recharts)

| Wrapper | recharts core | Use for |
|---|---|---|
| `SingleBarChart` | vertical `<Bar>` | pipeline counts, per-entity totals |
| `GroupedBarsChart` | grouped `<Bar>` series (+optional stock `<Legend/>`) | won-vs-lost, comparisons |
| `TrendLineChart` | `<Line>` ×1–2 | time series |
| `LabelPieChart` | `<Pie>` + per-slice `Cell` + label callback | shares/composition |
| `HorizontalBarChart` | `layout="vertical"` + YAxis width | funnels, top-N lists |
| `AreaTrendChart` | `<ComposedChart>` + `<Area>` (fillOpacity .6/.3) | cumulative volume |
| `FunnelChart` | `<FunnelChart>` + right `<LabelList>` | conversion stages |
| `Sparkline` (custom SVG) | — | KPI-card micro-charts (line/area/bar variants) |

Wrappers are typed, prop-driven (`series`, `fill`, `tickFontSize`, `grid`, `formatter`), and are the **only** recharts import site in the app. Set explicit `strokeDasharray="3 3"` grid dashes, `isAnimationActive={false}` for deterministic e2e, and explicit tooltip `contentStyle` (library defaults drift across majors — pin them).

### 9.2 Data flow (the derivation-seam rule)

```
route handler → prisma aggregate → serialize → store slice
  → PURE derivation fn in src/lib/<domain>-data.ts → chart props
```

Derivations (`pipelineStageCounts`, `revenueByMonth`, `wonLostByMonth`, …) are **pure functions, independently unit-tested**, never inline in components. Client-side filtering recomputes via the same pure fn (memoized) — never a second implementation.

### 9.3 States & a11y

Explicit empty state per chart card (icon + "No data yet" + primary CTA) — decide deliberately whether zero-data renders axes or the empty state (choose the empty state for a new product). Charts get `role="img"` + aria-label or a custom roving keyboard contract for pies (ArrowLeft/Right wrap, Escape blur — zero-balance's `usePieKeyboardParity` is the reference). Respect `prefers-reduced-motion` (disable chart animation).

### 9.4 Chart testing ladder

1. Unit: derivation seams against seed literals (freeze aggregates).
2. Contract: grid-dash, single-fill, legend-placement, no-hidden-axes source pins (cheap drift nets).
3. E2E: chart card titles + at least one seeded-value assertion per family; optionally sector-fill order (`["rgb(a)","rgb(b)","rgb(c)"]` value-DESC) and tooltip chrome via synthetic `mouseover` (Playwright `.hover()` misses mouse-following tooltips — dispatch the event).

---

## §10 State Management Standard

**ONE Zustand store.** Slices: `user/booted/bootError` + one slice per domain entity + view state. No React Query/SWR (documented ADR: a second server-cache layer is a sync-bug factory at this scale).

Mandatory patterns (all proven, all test-pinned):

1. **`call()` is the only fetch seam** (§7.4). Views never fetch; the store owns hydration.
2. **`hydrate()`**: `/api/auth/me` → then fan out slice fetches in parallel; on data-failure keep the user in-app + one-shot `bootError` toast.
3. **Mutation → refetch affected slices** (`Promise.all`), never manual local truth-rebuilds except deliberate optimistic apply **with unconditional refetch rollback**.
4. **Race guards:** module-level tokens — `sessionWriteToken` (logout bumps it; in-flight fetches check-and-discard so cleared slices cannot repopulate) and a last-call-wins token for any month/tab/flip-driven fetch. This is the logout-leak fix class; pin with a store test.
5. **`useShallow` on every derived-array selector** (Zustand v5 + React `useSyncExternalStore` — missing it caused production crashes, React issue #185; document the invariant in the store header).
6. **Modal machine:** discriminated-union `modal` state (one slot per dialog kind) with scoped close helpers that preserve parent dialogs.
7. Serial imports (CSV): batch POSTs serially, **one refetch at the end** (O(N²) refetch otherwise).

---

## §11 AI Feature Standard (optional module)

The **degrade-never-fail** pipeline (project-management's ADR, hardened by digma):

1. Compute the **deterministic fallback FIRST** (keyword parser or template plan) — it is the guaranteed floor.
2. Attempt the SDK via **dynamic `import()`** inside try/catch, raced against a **25s timeout**.
3. Treat LLM output as **untrusted input**: extract JSON defensively (tolerate markdown fences), then run a **sanitizer** — op/enum whitelist, numeric clamps, length caps, count caps (e.g. ≤10 items), drop title-less entries — before anything touches the DB (PAD security rule: "LLM output is untrusted").
4. Any failure → warn + serve the fallback. The app never 500s on an AI outage.
5. Own rate-limit bucket (`ai:`), server-side only, `DISABLE_AI_LLM=1` knob for deterministic e2e/smoke.
6. Unit-test the sanitizer's clamp/drop edges explicitly (900→160 chars, 9999→40 hours class).

---

## §12 Security Hardening Checklist

Run this list before any deployment; each item cites its section:

- [ ] `AUTH_SECRET` present, ≥ 32 hex chars, **fails hard** in production (§6.2)
- [ ] All cookies `httpOnly; SameSite=Lax; Secure` in prod; set/clear flag symmetry tested (§6.2)
- [ ] `timingSafeEqual` on every secret comparison (password, HMAC, token) (§6)
- [ ] Login timing equalization on unknown emails (§6.1)
- [ ] No-enumeration responses on login/forgot; documented decision on register (§6.1, §6.4)
- [ ] Verification + reset tokens stored **hashed**; TTL columns; consumed atomically (§6.3–6.4)
- [ ] `tokenVersion` revocation wired into `getSessionUser` (§6.5)
- [ ] Rate limiting on every auth/AI/upload route; `PROXY_HOPS` set to the real topology (§6.6)
- [ ] `requireSession()` first-line on every non-public handler; smoke test probes 401s (§6.7, §13.4)
- [ ] Ownership in every query WHERE; serializers are the only payload shapers (§5.3)
- [ ] zod at every body boundary; bounded reader; JSON content-type gate on mutations (§7.2)
- [ ] Security headers: `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy` (add HSTS at the edge or in `next.config.ts`) (§4.2)
- [ ] Open-redirect guard on `from_url` (§6.7)
- [ ] LLM output sanitized before persistence (§11)
- [ ] CSV formula-injection guard if exporting (§7.5)
- [ ] Upload MIME allowlist + randomUUID names + regex-pinned serving route (§7.5)
- [ ] No secrets/PII in logs; dev-only query logging (§5.2)
- [ ] `.env` gitignored; `.env.example` complete and current (§4.5)
- [ ] Dependency audit (`bun audit` / `npm audit`) in the gate (§14)

---

## §13 Testing Strategy

### 13.1 The three tiers

| Tier | Tool | What it covers | Runtime budget |
|---|---|---|---|
| Unit | Vitest, node env, `*.test.ts` | Every `src/lib/` seam: auth crypto, limiter (injected clock), validation, db-path (fixtures), serializers, money, derivations, sanitizers, store actions | seconds |
| E2E | Playwright, `.spec.ts` | Real Chromium vs the **production standalone build**; auth journeys, CRUD round-trips, responsive walks at 390×844, a11y, chart seeded values | minutes |
| Smoke | bash + curl | Boot the standalone artifact; auth round-trip incl. post-logout 401; every route's 401; rate-limit engagement (429 on 11th); invalid-payload 400s; health | ~1 min |

### 13.2 Hermeticity rules (all proven the hard way)

- E2E webServer: `PORT=3100`, **`DATABASE_URL=file:../db/e2e.db`** (own DB), `AUTH_SECRET` test value, determinism knobs on (`DISABLE_AI_LLM=1`), **`env -u DATABASE_URL`** style scrubbing of inherited shell vars.
- **`global-setup` reseeds in place** (delete rows, not the file — deleting the DB file under a live server hands out deleted-inode errors).
- A `setup` project logs in **once** and saves `storageState` — per-test logins would trip the 10/15min rate limiter (self-destruction); logged-out specs opt out with an empty storageState.
- `workers: 1`, `fullyParallel: false` (shared SQLite), `retries: 0`, trace retain-on-failure.
- Smoke script **pins its own `DATABASE_URL`**, kills port squatters, health-waits before assertions.

### 13.3 What every e2e suite must include

Auth journey (register→verify→login→logout→401); one full CRUD round-trip per entity; invalid-input 400; the mobile drawer contract; at least one seeded KPI/chart assertion; empty-state and error-injection specs (route-abort; boot-failure); custom 404. Optional best-in-class: axe two-gate a11y; computed-style assertions (never pixel-diff screenshots as the only evidence).

### 13.4 Smoke-test skeleton (`scripts/smoke-test.sh`)

```bash
#!/usr/bin/env bash
set -euo pipefail
export DATABASE_URL="file:../db/smoke.db"      # immune to shell-env override trap
# boot standalone on :3210 (kill squatters first), health-wait, then:
# 1) unauthenticated reads → 401   2) register → verify(devCode) → session
# 3) login/logout/post-logout-401  4) CRUD round-trip + invalid → 400
# 5) 11th login attempt → 429      6) pages render (grep <title>)
# every assertion: ok "NN — description" || { fail "NN"; exit 1; }
```

### 13.5 Test-quality doctrine

- **Behavior tests > source-pin tests.** A test that `readFileSync`s a source file and regexes it is a drift net, not a test — acceptable sparingly for architecture invariants (envelope presence, dead-code hygiene), never counted as coverage of behavior. (digma's 223/232 source-pin ratio is the cautionary tale; its headline count includes tests that pin *documentation phrasings*.)
- **No test may read `.env`** or any unbootstrapped file (digma's fresh-clone failure).
- Freeze seed-derived aggregates in unit tests (DB-free determinism).
- A hygiene test may substitute for disabled lint rules (neo-crm's dead-code-hygiene pattern) — but prefer just enabling the rules.

---

## §14 Quality Gates & Pre-Ship Checklist

**The gate order (run from repo root, in order, every time):**

```bash
bun run lint          # eslint . --max-warnings 0
bun run typecheck     # tsc --noEmit        ← the real type gate if ignoreBuildErrors is set
bun run test          # vitest run
bun run build         # next build (+ copy static/public into standalone)
./scripts/smoke-test.sh
bun run test:e2e      # playwright (boots the standalone artifact)
bun audit             # dependency vulnerabilities
```

**Wire the same order into CI the day the repo exists** (all four source repos deferred CI to local discipline and it is their single most portable weakness — Appendix B).

**Pre-ship checklist (beyond gates):** §12 security list complete; `.env.example` matches actual `process.env` reads; seed runs clean on a fresh DB; docs updated in the same commit (§15); changelog/version bumped; fresh-clone verification executed (install → generate → typecheck → test, from a clean checkout — the four source repos all pass this; keep it that way).

---

## §15 Documentation Contract

Five artifacts, updated **in the same commit** as the code change ("code wins — update the doc immediately, or the doc becomes an enemy"):

| Doc | Audience | Contains |
|---|---|---|
| `README.md` | users/onboarding | What it is, quickstart, demo login, scripts table, troubleshooting |
| `AGENTS.md` | coding agents | Commands, gate order, one-minute architecture, conventions, env contract |
| `CLAUDE.md` | agent workflow | The phased working method, scope rules, "do not introduce X halfway" rules |
| `Project_Architecture_Document.md` | engineers | **ADRs with context/decision/rationale/rejected-alternatives**, topology, security threat model, test distribution, known-issues ledger |
| `<app>_SKILL.md` | future builders | The distilled engineering knowledge: this document's per-app twin — stack, seams, traps, debugging symptom→cause→fix table, numbered lessons |

Rules: every doc claim must be verifiable against a file path or command; **counts come from the tools' own census** (vitest prints the truth — grep undercounts `test.each`); optional innovation — a `docs-counts.test.ts` that fails when documented counts drift (neo-crm); keep a `docs/session_NN.md` + remediation-plan trail during AI-driven builds, but treat it as history, not documentation — an adopter should need ≤ 10% of it.

---

## §16 Production Deployment

### 16.1 The artifact

`bun run build` → `.next/standalone/server.js` (+ copied `static/` and `public/`). Run with `NODE_ENV=production bun .next/standalone/server.js` **from the repo root** (the db-path seam handles the chdir trap, but root execution is the documented posture). One process, one SQLite file, one port.

### 16.2 Required runbook (DEPLOYMENT.md)

Build & run commands; env vars incl. `PROXY_HOPS` for the real proxy topology; DB location + the three `DATABASE_URL` forms (relative/absolute/Postgres); backup = stop + file copy (SQLite); update procedure (pull → `db push`/`migrate` → build → restart → verify via `/api/health`); troubleshooting (the `Error code 14` env-shadowing diagnosis via the startup log line; the Secure-cookie-behind-HTTP-proxy login-loop caveat).

### 16.3 Scale-up path (documented, not built)

Single-node is the v1 contract. When exceeded, in order: Postgres (`DATABASE_URL` swap — already documented), Redis-backed rate limiting (replace the in-process Map behind the same `checkRate` interface), object storage for uploads, and only then consider horizontal session state (stateless HMAC cookies already survive multi-instance; the limiter is the blocker).

### 16.4 The closing gaps (do not launch without reviewing Appendix B)

Email transport, RBAC enforcement (if the product needs roles), hosted CI, containerization, observability. None of these are in the source repos; all are scheduled work for any real deployment.

---

## §17 Anti-Patterns & Hard-Won Lessons

1. **Never trust an inherited environment.** A parent `.env` or exported `DATABASE_URL` shadows the repo's relative URL → "Error code 14: Unable to open the database file." Diagnose with the startup `[db] DATABASE_URL -> …` log; fix with `env -u` in scripts and the db-path seam (§5.2).
2. **`ignoreBuildErrors` without a typecheck gate is an unguarded cliff.** The explicit `tsc --noEmit` step is the only thing standing between you and shipping type errors — or omit `ignoreBuildErrors` entirely (zero-balance's posture).
3. **Read-then-write auth state invites races.** OTP attempts, reset consumption, lockout counters: always atomic conditional `updateMany` with the precondition in the WHERE (§6.3–6.4).
4. **A "reset link sent" toast without an endpoint is a lie.** Three of four source repos shipped this UI stub (inherited from their reference apps). Build the endpoint or remove the affordance.
5. **Unknown-email logins that answer instantly enumerate your users.** Burn the scrypt work (§6.1).
6. **Zustand v5 derived-array selectors without `useShallow` crash React 19 in production** (issue #185) — one-line fix, catastrophic omission (§10.5).
7. **VLM screenshots lie; computed styles don't.** 15+ visual misreads across the source family were disproven by `getComputedStyle` probes. When verifying parity or theming, measure (§13.3).
8. **Logout is a race, not a click.** Bump a session token; make in-flight fetches check-and-discard (§10.4) — otherwise cleared slices silently repopulate.
9. **Static KPI literals leak into production dashboards.** Reference apps hardcode their demo numbers; a clone inherits them. Rewire every delta/sparkline to the derivation seam before launch (§8.2).
10. **Test counts drift from docs unless the tool prints them.** Use vitest's own census; optionally pin with `docs-counts.test.ts` (§15).
11. **Never hand-edit lockfiles; add deps through the package manager** and let the gate re-run.
12. **Per-route auth discipline needs a mechanical backstop.** A forgotten `requireSession()` is invisible in review — the smoke suite's 401-probe over every route is the net (§13.4).
13. **Docs are coupling.** If a test pins doc phrasings, every doc edit breaks the gate (digma's lows-sNN class). Pin behavior, not prose.
14. **One fetch seam, one payload shaper, one chart module.** Every "second implementation" of any of these became drift within sessions in the source family.
15. **Money floats only at the format boundary.** `0.1 + 0.2 !== 0.3` took down real calculators; cents firewall (§5.1.4) with an epsilon (`<0.005`) at equality boundaries.

---

## §18 Tailwind CSS v4 Trap Register

| # | Trap | Rule |
|---|---|---|
| T1 | **`var()` chains in a plain `@theme` are dropped** by the v4 build — colors silently vanish | Literal hex in `@theme`; the only sanctioned `var()` use is `@theme inline` referencing `:root` custom props |
| T2 | **Gradient utilities (`bg-gradient-to-*`) render differently** (oklab interpolation vs v3) | Inline `style="background: linear-gradient(135deg, var(--a), var(--b))"` for every brand gradient |
| T3 | **A leftover `tailwind.config.js` silently flattens the design** — the #1 "generic look" bug | v4 = CSS-first; NO JS config file (delete legacy shadcn configs) |
| T4 | **`--font-sans: var(--font-inter), …` computes to invalid** at `:root` because next/font scopes the variable to `<body>` → whole app falls back to UA serif | Font-family **names** in `@theme` (`"Inter", "Inter Fallback", ui-sans-serif`), never the next/font CSS variable |
| T5 | **v4 default palette is oklch-tuned** and visibly off from v3 hexes consumers expect | Pin every consumed default scale to its exact hex in the `@theme` reference-palette block |
| T6 | **Custom `@layer utilities` classes outrank arbitrary utilities** (cascade order) | Document sanctioned override paths; don't fight it ad hoc |
| T7 | `tw-animate-css` npm export breaks under Turbopack (style condition unsupported) | Vendor the dist CSS |
| T8 | v4 serializes some shorthands differently (e.g. `rounded-full` on large radii) | Assert geometry via computed styles in e2e, not class names |

---

## §19 Scaffolding Workflow (Phases 0–9)

Each phase ends at a **gate** — do not proceed on red. (This is the six-phase "Meticulous Approach" of the source family, expanded for generic use.)

| Phase | Build | Gate / acceptance |
|:---:|---|---|
| **0** | Intake (§1); name the app; pick auth tier; choose palette + chart menu | §1 checklist answered; repo created |
| **1** | Scaffold: `next.config.ts` (§4.2), tsconfig/eslint/vitest/playwright contracts (§4.3), `globals.css` tokens (§4.4), `.env.example` (§4.5), folder skeleton (§3) | `bun run lint` + `typecheck` green on the empty shell |
| **2** | Data layer: schema with **userId tenancy** (§5.1), db-path seam + `db.ts` (§5.2), serializers, seed (§5.5) | `db:push` + `db:seed` clean; db-path fixture tests pass |
| **3** | Auth: password/session libs (§6.1–6.2), register/login/logout/me, rate limiter (§6.6), page guards (§6.7) — Tier 0 floor | §6.8 battery green; smoke 401-probes green |
| **4** | Auth completion (Tier 1): verify-otp + resend (§6.3), forgot/reset (§6.4), `tokenVersion` (§6.5), Mailer interface | Atomicity + single-use + eviction tests green |
| **5** | Domain: entities/routes per §7 (zod, envelope, ownership), derivation seams (§9.2), domain math (money if applicable) | Unit tests on every seam; invalid-payload 400s in smoke |
| **6** | Shell: app-shell/sidebar/topbar/mobile-nav (§8.1), KPI card family (§8.2), stats route | 390×844 drawer e2e green; a11y floor assertions green |
| **7** | Charts: `charts.tsx` families (§9.1), wire derivations, empty states | Seeded-value e2e per chart family green |
| **8** | Hardening + polish: §12 checklist, custom 404, resilience specs (§13.3), CSV/upload if needed (§7.5) | Full §14 gate order green, twice, from a fresh clone |
| **9** | Distill: write/refresh the five docs (§15), record ADRs, tag v0.1.0 | Fresh-clone verification: install → generate → typecheck → test green |

**Optional module insertion:** AI features between phases 5 and 6 (build the sanitizer before the prompt — §11).

---

## Appendix A: Quick Reference Card

```bash
# Boot          bun install && cp .env.example .env && bun run db:push && bun run db:seed && bun run dev
# Fast gates    bun run lint && bun run typecheck && bun run test
# Full gates    bun run build && ./scripts/smoke-test.sh && bun run test:e2e
# Schema        bunx prisma generate && bun run db:push
# E2E env       PORT=3100 · DATABASE_URL=file:../db/e2e.db · DISABLE_AI_LLM=1 · workers:1 · storageState
# Sessions      scrypt(16B salt, 64B key) · HMAC-SHA256 · 7d · httpOnly/lax/secure · tokenVersion revocation
# Limits        login 10/15m · register 10/15m · resend 5/15m · verify 20/15m · ai 20/5m · 429+Retry-After
# Envelope      {ok:true,data} | {ok:false,error:{code,message}} · requireSession() first line
# Tenancy       every model: userId + cascade + @@index([userId,…]) · findFirst({id,userId}) → 404
# Charts        one charts.tsx · 8 families · pure derivations in lib · isAnimationActive={false}
# Store         ONE Zustand store · call() only · useShallow everywhere · session race token
# Tokens        literal hex in @theme · inline gradients · NO tailwind.config.js · font NAMES not vars
```

## Appendix B: Production Gap Closure List

Everything this skill deliberately does NOT ship (inherited gaps from all four source codebases — schedule explicitly):

1. **Email transport** — implement the `Mailer` adapters (SMTP via nodemailer, or Resend/Postmark API). Without it, §6.3/§6.4 stay dev-gated.
2. **RBAC enforcement** — `requireRole()` + role checks on routes (§6.7 Tier 2), plus an admin UI surface.
3. **Hosted CI** — port the §14 gate order to GitHub Actions (or equivalent) on push + PR; include the fresh-clone verification as a scheduled job.
4. **Containerization** — multi-stage Dockerfile (install → build → standalone runtime + prisma engines), `.dockerignore`, compose file with a Postgres profile.
5. **Observability** — structured logging (pino), an error tracker (Sentry), `/api/health` extended with DB + version payload, uptime checks.
6. **OAuth** — if required: add a provider table + code-flow routes; keep the email+password core as the fallback identity.
7. **Multi-instance** — Redis-backed rate limiting behind the same interface (§16.3); session cookies already survive (stateless).
8. **Backups & migrations** — switch to `prisma migrate` before the first shared-environment deploy; document restore drills.

---

*Distilled from 1,177 commits across four production codebases (digma · neo-crm · project-management · zero-balance) and their engineering skills, 2026-09-17 → 2026-10-22. When this document and the code disagree, fix whichever is wrong, in the same commit.*

