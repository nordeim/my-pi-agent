---
name: web-application
description: "Complete, generalized engineering skill for building any web application codebase: Next.js 16 App Router + React 19 + TypeScript (strict) + Tailwind CSS 4 (CSS-first) + shadcn/Radix + one Zustand store + Prisma/SQLite-dev (PostgreSQL-prod) + Zod-validated API + scrypt/HMAC cookie auth + recharts dashboards + a three-tier test suite and a single-command quality gate. Distilled from four production-remediated sibling codebases (digma, neo-crm, project-management, zero-balance); every rule traces to a failure that actually happened."
version: 1.2.0
last_updated: 2026-10-25
provenance: "Distilled from digma_SKILL.md (v1.158.0 at the 10-23 pin; v1.164.0 at the 2026-10-25 re-validation), neo-crm_SKILL.md (v1.171.0 at pin; v1.180.0), project-management_SKILL.md (v1.0.0 — distilled at app remediation v2.15), and zero-balance_SKILL.md (v1.0.0) — four sibling codebases, 1,226 combined commits of build-and-remediate history at distillation, 1,244 at the 10-23 re-validation, 1,508 at the 10-25 re-validation (HEADs digma 2fa13d7e, neo-crm 02ac27eb, project-management 9ff03bc, zero-balance 1a3553da; pm unchanged). The v1.1.0 generation is the copy vendored at skills/web-application/SKILL.md in digma/neo-crm/zero-balance; the family keeps adopting it — neo-crm's session-174 (build-as-type-gate, full strictness, single lockfile) and session-176 (recharts 3.x migration, ADR-021) both cite it by name, and digma's session-181 auth hardening cites 'the master skill §5 contract' in its own code."
---

# Web Application — Complete Engineering Skill (Generalized)

> **How to use this document:** this is the single-source engineering reference for scaffolding, extending, debugging, or auditing any web application built on this skill. §0 is the build order; §1–§17 are the contracts; §18–§20 keep the machine honest. **When code and this document disagree, the code wins — then fix this document in the same commit.**
>
> **Companion documents (create all four, keep them in lockstep):** `README.md` (user-facing), `AGENTS.md` (operator quick-reference, ≤ ~300 lines), `CLAUDE.md` (agent contract, ≤ ~600 lines), `Project_Architecture_Document.md` (the blueprint with ADRs), plus this `SKILL.md`. Documentation is a product surface: stale docs are bugs.

---

## §0 The Scaffolding Workflow (any app, this order)

1. **DEFINE** — one-sentence product identity; the 3–7 core entities; the non-negotiable rules (what this app will *never* do). Write `README.md` skeleton first.
2. **SCAFFOLD** — clone this skill's stack (§2): Next.js App Router (standalone output), strict TS, Tailwind 4 CSS-first, Prisma + SQLite, the four config files (§3), and the lint/typecheck/test/build scripts *before* writing features.
3. **DATA** — `prisma/schema.prisma` first (models, indexes, relations), then an idempotent seed (routed through the db-path seam like the app). Money math is integer cents at every aggregation boundary; enums live in one constants module.
4. **AUTH** — stand up the full auth family (§5) before any domain feature: register / login / logout / me / verify / forgot / reset, rate-limited, with the session envelope. Auth is the template's most valuable inheritance — port it, don't rewrite it.
5. **API** — one route per resource following the handler idiom (§6): session gate → Zod parse (bounded reader) → FK/ownership checks → Prisma → envelope. Never throw across the boundary.
6. **UI SHELL** — app shell (sidebar + topbar + mobile nav), layout chrome, the one store (§9), then feature views. Empty/loading/error states are part of every surface.
7. **DASHBOARD + CHARTS** — KPI stat cards first, then sparklines, then full charts from the wrapper family (§10–§11). Decide the zero-data policy explicitly (§11) — a dashboard with no data is a designed surface.
8. **TEST AS YOU GO** — every pure seam gets its Vitest spec when it's written (TDD at the seams); every user-visible surface gets an e2e pin before it ships.
9. **GATE + DOCS** — run the full gate (§15); update all five docs in the same commit; log the session. The gate is the definition of done, not an afterthought.

---

## §1 Product Identity & Design Philosophy

- **One deployable unit.** No microservices, no external auth service, no Redis to start: one Next.js app + a database file + optional LLM SDK. `next build` produces a standalone server. This is a feature — it keeps deploys, tests, and debugging trivial until scale demands more.
- **Degrade, never fail.** Optional integrations (AI, rich export) always carry deterministic fallbacks. The app must never 500 because an optional dependency is down.
- **Pure seams, tested.** Any logic that can break silently (path resolution, validation, routing, money math, rate limiting, date grouping) lives in `src/lib/*.ts` with a Vitest spec. Route handlers and views stay thin.
- **Superset, never regression.** When cloning a reference (a design, a competitor, a spec), match it deliberately and fix its bugs — but record every deviation in the PAD's Known Issues. A deviation nobody wrote down is a bug nobody can defend.
- **Anti-generic mandate.** No glassmorphism-by-default, no purple-gradient-on-white cliché, no `rounded-2xl`-everything, no shadows on shadows. Brand color comes only from tokens (§12). Every page should look *authored*.
- **Count the things.** Env vars, models, routes, tests, checks — know the numbers, keep them true, and when one changes, `rg "<old number>"` the whole doc set in the same commit.

---

## §2 Canonical Stack & Versions

| Layer | Technology | Version floor | Notes |
|---|---|---|---|
| Framework | Next.js (App Router) | 16.4 | `output: "standalone"`, `outputFileTracingRoot` pinned to repo root |
| UI runtime | React | 19.3 | Client components explicit via `"use client"`; no `forwardRef` needed |
| Language | TypeScript | 5.9 | **`strict: true` — do NOT loosen `noImplicitAny`**; `tsc --noEmit` is a gate |
| Styling | Tailwind CSS | 4.3 | CSS-first: tokens in `globals.css` `@theme inline`; **no `tailwind.config.js`** |
| PostCSS | `@tailwindcss/postcss` | ^4 | The only plugin; missing it = pages render unstyled |
| Primitives | shadcn/ui on Radix | per-pkg | dialog, select, popover, dropdown, label, slot, tabs; build bespoke only when primitives can't |
| State | Zustand | 5.0 | **ONE store**; derived selectors MUST use `useShallow` (§9) |
| ORM / DB | Prisma / SQLite (dev) | 6.19 | `db push` in dev; **`migrate` in production**; PostgreSQL swap documented in `.env.example` |
| Validation | Zod | 4.6 | At every API boundary (§7); enums imported from the constants module |
| Charts | recharts | 3.x (the family is now uniform on 3.10.x — neo-crm migrated 2.15→3.10.1 in session-176/ADR-021, which names "the N-3 retirement") | Wrapped, never raw (§11) |
| Icons | lucide-react | 0.525 | Inherit library defaults (stroke 2) unless a measured reason exists |
| Unit tests | Vitest | 5.0 | Node env; `*.test.ts` only; `@` alias |
| E2E | @playwright/test | 1.63+ | Chromium project + setup project; runs against the **production build** (1.64 in digma/neo-crm; 1.63 in pm/zb) |
| A11y | axe-core (Playwright) | 4.x | A11y assertions in the e2e suite, not just manual review |
| Runtime | Bun (or Node ≥ 20) | 1.3 | Scripts run from repo root — this matters (§18) |

**Dependency discipline:** every dependency must have a live import within one commit of being added; run a dead-dependency census periodically (the family repeatedly found and retired zero-import scaffold packages). Prefer library defaults over bespoke micro-styling — bespoke values are drift liabilities.

**Environment contract (keep it at exactly this set; add only with an ADR):**

| Variable | Required | Purpose |
|---|---|---|
| `DATABASE_URL` | yes | `file:../db/custom.db` (SQLite dev) or `postgresql://…` (prod). Relative `file:` URLs resolve against `prisma/schema.prisma` — never against CWD |
| `AUTH_SECRET` | **production: hard requirement** | HMAC key for session tokens, ≥ 16 chars (`openssl rand -hex 32`). Dev may fall back with a warn; **production fails hard** |
| `NEXT_PUBLIC_SITE_URL` | recommended | Canonical origin for metadata/sitemap — **inlined at build time**, so set it before `bun run build` in production (digma's variant is `DIGMA_SITE_URL`) |
| `<APP>_PROXY_HOPS` | prod-behind-proxy | Trusted proxy depth for rate-limit IP keying (unset = 1 last hop; unparsable fails **closed**) — the digma/neo-crm contract; adopt wherever a limiter runs behind proxies |
| `<APP>_DISABLE_IN_APP_OTP` / `_RESET` | prod | Turn OFF demo-mode in-response verification codes / reset links when a real mail transport owns delivery — **mandatory**: the family ships in-response delivery by default, and zb's OTP variant had no knob (a shipped gap, not a pattern to copy) |

`.env` is untracked; `.env.example` is committed, mirrors the contract exactly, and documents the PostgreSQL swap.

---

## §3 Configuration & The Database Path Contract

Config files that carry non-obvious weight:

| File | Locks in |
|---|---|
| `next.config.ts` | `output: "standalone"`; `outputFileTracingRoot` pinned (prevents nested standalone paths under parent workspaces); **do not set `ignoreBuildErrors`** — the build should be the type gate; images `remotePatterns` explicit |
| `tsconfig.json` | strict TS; `@/*` → `src/*`; exclude vendored non-app directories |
| `eslint.config.mjs` | next/core-web-vitals + next/typescript; React 19 hook rules (incl. `set-state-in-effect`) as **errors**; ignore non-app dirs |
| `vitest.config.ts` | include `src/**/*.test.ts` + `tests/**/*.test.ts`; never match Playwright's `*.spec.ts` |
| `playwright.config.ts` | setup project (one login → `storageState`), webServer = standalone build on its own port with its **own** `DATABASE_URL` (e.g. `db/e2e.db`) |
| `postcss.config.mjs` | `@tailwindcss/postcss` only |

**The DATABASE_URL contract (read this twice — it bit all four source codebases):**

A relative `file:` URL resolves differently per reader: the Prisma CLI reading `.env` anchors at `prisma/schema.prisma`; a **shell-inherited** `DATABASE_URL` anchors at the CWD (unpredictable); `dotenv` never overrides an existing process env. And Next's standalone `server.js` runs `process.chdir()` before your code loads.

Therefore:

1. `src/lib/db-path.ts` is the **only** sanctioned source of the runtime URL (anchor chain: standalone-repo-root detector → module anchor validated on disk → CWD with existence guard). `db.ts` never reads `process.env.DATABASE_URL` directly.
2. `db-path.ts` is a **pure seam with fixture tests** — this is the single most-tested module in the template family, for good reason.
3. npm scripts pin the environment: runtime scripts inline `DATABASE_URL=…`; Prisma CLI scripts strip it (`env -u DATABASE_URL prisma …`) so a polluted parent shell can never redirect the database. **Empirically load-bearing (validated 2026-10-23):** under a shell-exported `DATABASE_URL`, the sibling with this discipline ran its full smoke suite 35/35 untouched, while the one without it silently pushed its database outside the repo and fell to 12/30 — and route the seed through `db-path.ts` like the app (a bare `new PrismaClient()` seed bypasses the seam).
4. Symptom to memorize: `Error code 14: Unable to open the database file` = wrong anchor or a shell env override — check `env | rg DATABASE` and the startup log line before touching code.

**Bootstrapping (this exact sequence):**

```bash
bun install
cp .env.example .env        # then set AUTH_SECRET in prod
bun run db:push             # schema → db/custom.db
bun run db:seed             # idempotent demo data
bun run dev                 # :3000
```

---

## §4 Data Layer & Domain Model

- **Schema-first.** `prisma/schema.prisma` is the source of truth: models, `@@index([userId])` on every user-owned table (plus composite indexes for the hot list queries), explicit `onDelete` behaviors (`Cascade` for owned children, `SetNull` for assignees), and `@unique` where the domain implies identity.
- **Enums as single-source constants.** Status vocabularies live in `src/lib/constants.ts` as `as const` arrays + label/color metadata maps (`*_META`). Dropdowns, badges, and Zod schemas all import the same arrays — adding a value touches exactly one file. Never fork an enum copy into a component.
- **Money is integer cents at every aggregation boundary (zero-balance ADR-004).** Amounts may travel and be stored as decimals (zb keeps Prisma `Float` columns for wire parity), but every sum, comparison, and derived total converts to integer cents first (`src/lib/money.ts` owns the format boundary) — IEEE-754 drift (0.1 + 0.2) can never reach a total. For new schemas, integer-cents columns are the stricter option; if you keep decimal columns, the aggregation-boundary rule is non-negotiable.
- **Server-recalculated derivations.** When child rows change a parent's derived value (line items → category total), the **server** recomputes it inside the mutation — clients never write derived aggregates.
- **Seed is idempotent and in-place.** `deleteMany` domain tables → insert canonical demo data. **Never `rm` the db file under a running server** — the process keeps the deleted inode and serves stale data. And after any reseed, live session cookies point at deleted user rows: re-login before probing (symptom: healthy DB, every view empty).
- **Every mutation narrates itself** (if the domain has activity): an API change without its activity-feed write is incomplete by definition.
- **`PrismaClient` is constructed in exactly one place** (`src/lib/db.ts`) — with the URL from `db-path.ts`. Nowhere else. Not in scripts, not in tests. **The seed routes through the same seam** (`process.env.DATABASE_URL = resolveProcessDatabaseUrl()` before `new PrismaClient()` — the zb/neo pattern; a sibling's bare-PrismaClient seed is the counter-example that stranded its database under a polluted shell).
- Production: switch to PostgreSQL (`datasource` stays env-driven) and adopt `prisma migrate` — `db push --accept-data-loss` is a dev-only convenience and a prod data-loss foot-gun.

---

## §5 Authentication & Authorization (the template's crown jewels)

Hand-rolled by design (no NextAuth, no JWT library — fewer moving parts, full control, zero dependency risk):

- **Passwords:** scrypt with per-user salt, `scrypt:salt:hash` format, constant-time compare, in a **pure crypto seam** (`password.ts`, node:crypto only) importable by seeds and routes alike.
- **Sessions:** HMAC-SHA256-signed stateless cookie — `base64url(JSON{uid,iat,exp,v}) + "." + hex_sig`, httpOnly + `sameSite: "lax"` + `secure` in production, 7-day TTL (zero-balance runs 30 days while its own PAD documents 7 — pick one and keep the doc honest; digma/pm/neo-crm run 7). Verification with `timingSafeEqual`; malformed/expired/`v`-shape-invalid tokens all return `null`.
- **The `v` (tokenVersion) revocation dimension:** the version rides the signed payload *and* the user row; `getSessionUser()` rejects any token whose `v` ≠ the live row's. **Password reset increments the row's version and every pre-reset cookie dies** — a stateless format with revocation, the exact gap plain stateless cookies have. A missing `v` reads as 0 (backward-compatible migration).
- **Login timing equalizer:** the wrong-password branch burns the same scrypt work as the right one — no user-enumeration timing oracle.
- **Secret enforcement:** `AUTH_SECRET` missing/short in production → **throw** (fail-hard; forgeable sessions must never ship silently). Dev/test keeps a warned fallback for DX. (Family status at v1.2: digma joined neo-crm here — its session-181 fail-hard cites "the master skill §5 contract" in-code; pm and zb still ship dev-fallback constants.)
- **Forgot/reset funnel:** no-enumeration 200 on forgot; reset tokens are 32-byte, **hashed at rest** (SHA-256 — the raw token lives only in the delivery URL), 60-min TTL, consumed atomically single-use (conditional update, not read-then-write); reset also bumps `tokenVersion`.
- **Verification (email OTP):** per-account verify code + resend with its own limit; in-response delivery of codes/links exists **only for demo mode** and is switched off by `*_DISABLE_IN_APP_*` envs in prod — a real mail transport owns delivery then. Attempt counters must increment **atomically** (`updateMany`) — zero-balance shipped the racy read-then-write form, the family's live counter-example.
- **Rate limiting:** fixed-window per-IP (login 10, signup 10, resend 5, verify 20, forgot 10, reset 10 per 15 min) → `429 RATE_LIMITED` + `Retry-After`. Two in-family shapes are sanctioned: neo-crm's per-route split (those constants, plus upload 20) and digma's single shared credential bucket (10/15 min) with separate `ai` (20/5 min) and `crud` (60/5 min) buckets — pick one and document it. IP keyed on the deploy-declared proxy-hop depth; unparsable hop counts fail closed. In-process by design — **document that multi-instance deploys need a shared store**, or accept the single-node posture explicitly.
- **Gates:** `getSessionUser()` (+ redirect to `/login?from_url=…`) at every page; `requireSession()` as the first statement of every data route (401 envelope). Public by design: only `/api/health` and the auth family (rate-limited instead).
- **Roles:** carry a role on the user; enforce it at the route layer where the domain requires. A role field without route checks is not authorization — it's a label.

---

## §6 API Layer — The Route Handler Idiom

Every handler follows this shape (the family's 60+ handlers converge on it):

```ts
import { db } from "@/lib/db";
import { ok, ERR, isGuarded, parseBody, requireSession } from "@/lib/api";
import { accountCreateSchema } from "@/lib/schemas";

export const dynamic = "force-dynamic";

export async function POST(req: Request) {
  const guard = await requireSession();            // 401 envelope on miss
  if (isGuarded(guard)) return guard.response;
  const parsed = await parseBody(req, accountCreateSchema);  // §7
  if (!parsed.ok) return parsed.response;
  const body = parsed.data;
  if (body.ownerId) {                              // FK checks stay route-side
    const owner = await db.user.findUnique({ where: { id: body.ownerId } });
    if (!owner) return ERR.BAD_REQUEST("Selected owner does not exist");
  }
  const created = await db.account.create({ data: { /* …body */ } });
  return ok(created);
}
```

Rules:

- **The envelope is absolute:** `{ok, data} | {ok:false, error:{code,message}}` — `ok(data, status)` / `fail(code, message, status)`. Never throw across a handler boundary; errors become envelopes.
- **Status discipline:** bad input → 400 with a specific code; unknown id → 404; auth gap → 401; conflict (e.g. already-planned) → 409; rate limit → 429. Every JSON body parse goes through the bounded reader (§7) — a non-`application/json` Content-Type is unparseable-by-policy (the login-CSRF class), the declared length is checked before reading, and chunked streams are counted as they're read.
- **`force-dynamic` on every data route.** No accidental static caching of authenticated payloads.
- **One resource = collection route + `[id]` route.** Filters via query params (`?status=`, `?assignee=`), parsed with the same Zod discipline.
- Route handlers are **thin DB wrappers**: parse → validate → ownership/FK → Prisma → envelope. Anything smarter belongs in `src/lib` with a spec.

---

## §7 Validation Layer (Zod at every boundary)

- One `src/lib/schemas.ts` (or `validation.ts`) consumed by every route via `parseBody()` — **nothing reaches Prisma unvalidated**. Field-level messages in the schema; the route's 400 carries the first issue in a stable order (message equivalence is a migration invariant).
- **Enums import the constants module** — Zod `.refine`/`z.enum` over the same `as const` arrays the dropdowns use.
- **Money schema:** finite, `min(0)`, sane `max`, integer cents at the wire or a documented wire format.
- **Dates:** regex `^\d{4}-\d{2}-\d{2}$` **plus a real-calendar-date refinement** — `Date.parse` accepts rollovers like `"2026-02-30"`, so verify the components round-trip. Native date inputs send `""` when cleared: `z.preprocess` empty-string → `undefined`, don't widen every schema by hand. *(Both rules verified in zero-balance's `validation.ts`.)*
- **PUT semantics are three-state:** absent → `undefined` (no write); `null`/`""` → explicit clear; a value → the trimmed value. Encode it once in the schema helpers, not per-route. *(neo-crm's `clearable*` helpers; note zero-balance's PATCH is deliberately two-state — absent = no-write, `""` elided, `null` rejected — pick one contract per API and document it.)*
- **Migration rule** (proven in-family): when retrofitting Zod onto hand-rolled guards, the schema must reproduce every existing user-facing message byte-for-byte, and the test suite is the proof — zero message drift.

---

## §8 Component Architecture & Client Patterns

**Layer model — imports point DOWN only:**

```
src/app/**          pages (thin, server) + API routes + layouts
src/components/**   layout chrome + feature views + ui/ primitives
src/lib/**          pure seams (no upward imports — db-path imports only fs/path/url)
src/stores/**       the one Zustand store (client)
prisma/**           schema + idempotent seed
```

Patterns the family bled for:

- **Client/server split:** server components render shells and metadata; everything interactive is `"use client"`. The authenticated layout makes the session decision server-side (the guest never receives app HTML); the redirect itself may be a client shim — neo-crm session-147: a server layout cannot know the current path — which still avoids flash because no app HTML ever reaches the guest.
- **Dialog forms — remount-via-key:** `<EntityDialog key={editing?.id ?? "new"} … />`; initialize state FROM PROPS at mount. **Never `useEffect(() => setState(...))` to copy props** (React 19's `set-state-in-effect` is an error rule for this reason — and it's racy in hydration).
- **Adjust-during-render for prop-derived state** (the sanctioned React idiom when remounting is too heavy): track the previous key in state and reset during render when it changes.
- **Drawers/sheets are state machines, not class toggles:** one `open` boolean drives translate, visibility transition, `inert`, `aria-hidden`, body scroll-lock, and focus-trap lifecycle together.
- **Dialogs on conditional mounts need lazy initializers** (`useState(() => initialForm(modal))` + reset-on-modal-identity-change-during-render) — the effect-based reset they replaced was both a lint error and a production race.
- **Anchor + SPA coexistence:** when a real `<a href>` wraps interactive children (card links with action buttons), the click handler needs `if (e.target.closest("button")) { e.preventDefault(); return; }` — the `preventDefault` is mandatory; returning early without it lets the browser follow the href as the default action.
- **Auth navigation uses `router.refresh()`**, never `window.location` assignments — the header must swap without a full reload.
- **Persisted UI state (sidebar collapse)** uses `useSyncExternalStore` over a hydrated external store — never `useState`-in-`useEffect` (React 19 rejects it).
- **`<div onClick>` is banned** — real buttons, `aria-label` when icon-only. Background/decorative images use plain `<img>` with `alt=""` + `aria-hidden` deliberately (and the lint rule is configured off for exactly that case).
- **Layout constants live in one tested module** (`page-layout.ts`) — a single test-pinned source for KPI grid geometry, card paddings, sparkline sizes. Hand-placed page classes drift.

---

## §9 State Management — The ONE Store

- One Zustand store holds all server state + view/modal state. No React Query, no SWR, no context-splitting. One `call()` helper is the **only** sanctioned HTTP client: it unwraps the envelope, converts failures into destructive toasts, and returns `null` — actions treat `null` as "abort silently," never re-throw into render.
- **The selector rule (the single most important perf invariant — it crashed production while looking fine on dev):**

```tsx
// ❌ FORBIDDEN — fresh array per snapshot → infinite re-render (React #185)
const items = useStore((s) => s.items.filter((i) => i.type === "expense"));
// ✅ REQUIRED
import { useShallow } from "zustand/react/shallow";
const items = useStore(useShallow((s) => s.items.filter((i) => i.type === "expense")));
// ✅ Also fine — stable slice reference, no derivation
const items = useStore((s) => s.items);
```

- **Lifecycle:** `boot()` fetches `/api/auth/me` + all slices in parallel once (AppShell mount); mutations refresh the affected slices **and their dependents** (task mutations refresh goal counts + activity feed); `refresh()` re-fetches after writes.
- **Nullable-user pattern:** the shell renders for logged-out visitors (empty states + LOG IN) and the store skips fetches while `user` is null — graceful public surface without a second app.
- **Modal state is a discriminated union per slot** (`item: {kind:"create"} | {kind:"edit", id} | null`) — one `closeModals()` clears all; scoped closers exist only where the reference behavior demands it (keep-the-calculator-open class of decisions).

---

## §10 Dashboards

Composition order that works (proven across the family):

1. **KPI stat cards** — a responsive grid, each card: label (two-tier label system), the value, a delta/trend, a sparkline. Server-derived numbers (a `/api/dashboard` or `/api/stats` aggregation seam), never client-side joins.
2. **Sparklines** before charts — cheap momentum (`Sparkline` with `variant="line" | "area" | "bars"`).
3. **One or two real charts** (§11) answering the page's primary question.
4. **A drill-down list** (3-level expandable: section → category → item) where totals need decomposition.
5. **Quick actions** — the 2–4 things users do most, one click away.
6. **Empty/loading/error states on every block** — a dashboard with zero data is a designed surface, not a blank page (charts render their zero-data form or an explicit empty state; KPI cards render literal zeros, not skeletons forever).
7. **Export** (CSV first, PDF when the audience needs it) wired through the shared `downloadBlob` flow — never `window.location` hacks.

KPI derivation rules: trends compare against a fixed baseline window; "next action"–style widgets read the **source entity list**, not a sibling feed (deriving UI text from the wrong input worked only while old data happened to align — the input must be the source of the fact).

---

## §11 Charting

- **Wrap recharts once; consume wrappers only.** The proven family (neo-crm's `charts.tsx`): `SingleBarChart`, `GroupedBarsChart` (pairs + stock `<Legend/>`), `TrendLineChart` (1–2 strokeWidth-2 lines), `LabelPieChart` (full pie with per-slice label formatter + `Cell` fills), `HorizontalBarChart` (`layout="vertical"`), `RevenueLineChart` (the target-vs-actual **area** pair), `ConversionFunnel` (`FunnelChart` + `LabelList`) — with `Sparkline` living beside the shared page parts (bars/line/area variants). Each wrapper: typed props, explicit fill/height/grid, and a **declared zero-data policy** — the neo-crm doctrine is to render the REAL chart at all-zero data (only Sparkline nulls on empty); an explicit empty state is the alternative. Decide once, in the wrapper, never per page.
- **Stock axes by default.** Don't hide axis/tick lines and hand-roll margins unless a measured reason exists — the scaffold-era instinct to hide axes was a systemic divergence from every reference. Grid, when present, is dashed `"3 3"` explicitly (recharts' default grid is solid).
- **The `tick: undefined` trap (recharts 2.x):** passing `tick` as an explicit `undefined` nullifies `defaultProps.tick` and the grid silently falls back to a 4-line frame. Pass the prop only when you have a value.
- **Palette as named constants** (`CHART_COLORS` — literal hex in `constants.ts`; the CSS `--color-chart-*` tokens are a separate surface in neo-crm); per-series fills are named constants. Donut slice order is a product decision — pin it in one place and pin it with an e2e assertion (fills included).
- Tooltips: stock white box unless the design system truly demands custom `content`; formatters (`dollar`, number, percent) are shared, exported, and unit-tested.
- **The 2.x→3.x migration doctrine (proven in-family — neo-crm session-176/ADR-021):** pin `accessibilityLayer={false}` at every chart-type site (deterministic e2e), add a `tooltipFormatter` adapter, bridge the PieLabel type, and keep the e2e grid sentinel as the standing upgrade guard. The wrapper list and the zero-data policy survived that major **unchanged** — the wrapping discipline is what makes chart upgrades cheap.
- **Charts are e2e-pinned** — fill attributes and geometry asserted against the seeded data, so a chart-library upgrade that changes rendering surfaces as a red test, not a silent drift.

---

## §12 Design System (Tailwind v4, CSS-First)

All tokens in `src/app/globals.css`. **`@theme inline` with literal hex values only.** The five v4 traps, all mitigated in-family:

1. A bare HSL triplet (`0 0% 100%`) in `@theme` **silently resolves to transparent** — use literal hex.
2. v4's default palette is oklch and drifts 1–3 sRGB units per channel from intended hexes — define your brand as literals.
3. Gradient utilities interpolate in oklab and visibly shift brand blends — brand gradients use inline `style={{ background: "linear-gradient(135deg, var(--a), var(--b))" }}`.
4. `space-y-*` rewrote: v3 wrote `margin-top` on `* + *`; v4 writes `margin-block-end` on `:not(:last-child)`. Mirror reference rhythm with explicit `mt-*` on the later child; never stack `mt/mb` on children of `space-y` containers (double-spacing).
5. The shadow scale moved one notch heavier — pin `--shadow-*` to the intended geometry.

More cascade law:

- **Custom classes lose to nothing:** classes in `@layer utilities` emit **after** generated utilities — an arbitrary `shadow-[…]`/`rounded-*`/`h-*` utility on an element that also carries a custom component class **silently loses the cascade**. Override with a dedicated custom class or an inline style. Use v4-native `@utility`, never `@layer utilities`.
- `rounded-full` computes as `calc(infinity * 1px)` (≈33554432px) — assert "radius > 1000" in tests, and pin literal `rounded-[9999px]` when matching a reference.
- A color-only `ring-[…]` utility emits **no box-shadow** in v4; composed `shadow-[…]` utilities emit zero-alpha prefixes from unset `--tw-*` vars — plain-declaration custom classes byte-match reference computed styles.
- Tailwind v4 preflight sets **no `cursor: pointer`** on buttons — add the base-layer rule `button, [role="button"] { cursor: pointer }`.
- `tw-animate-css` imports as CSS (vendoring it is a sanctioned fix if the npm import breaks the bundler).
- **Z-index is a flat documented scale** (§ quick reference) — no `z-[9999]`.
- Typography: system stack or `next/font` only (never a second font-loading path); a two-tier label system (`label` / `label-sm`) beats ad-hoc caption styling.
- **The shadcn `--radius` token overrides `rounded-xl` semantics** (1rem base → 20px) — measured values need explicit `rounded-[Npx]`, not scale names.
- Icons: inherit lucide defaults; a bespoke `strokeWidth` on many sites is a maintenance liability (the family watched a reference flip strokes twice in three deploys — 33 sites to re-edit vs zero for default-inheritors).

---

## §13 Accessibility

- Radix primitives are load-bearing: dialogs expose `role="dialog"` + `aria-modal` + focus trap + focus return + Escape/overlay close; selects expose combobox/option trees. E2E locators depend on these roles — removing them breaks the suite (a feature, not a bug).
- Every input has a `<Label>`; icon-only controls carry `aria-label` ("Actions for {name}", "Delete {name}").
- Visible focus (ring token); 44px touch floor on mobile bands (document exceptions where a reference demands parity).
- Keyboard paths are tested: Escape closes, Enter submits native forms, all controls are real buttons/inputs.
- **Exit animations keep nodes mounted ~200–300ms** — any automation (or a11y probe) asserting "closed" must settle-wait first.
- axe-core runs in the e2e suite; a11y regressions are gate failures, not review comments.

---

## §14 Testing Strategy (three tiers, one law: **the dev server lies about production**)

1. **Unit (Vitest) at the pure seams** — TDD default (red → green → refactor) for `src/lib/*`: db-path resolution, validation schemas, money math, date grouping/relative time, rate-limit windows, router mapping, next-action derivations, greeting boundaries, enum label maps. Route handlers and views are covered by tiers 2–3, not by mocked unit tests — assert observable behavior, not that mocks were called.
2. **E2E (Playwright) against the PRODUCTION build** — the webServer boots the standalone build on its own port with its own `db/e2e.db` (globalSetup pushes + seeds it). The production-only hydration/crash class (the `useShallow` infinite loop shipped invisible on dev) is the reason this is law. One setup project signs the demo user in **once** and shares the cookie via `storageState` — per-test logins self-destruct against the auth rate limiter. Specs that need the logged-out surface opt out with `test.use({ storageState: { cookies: [], origins: [] } })`.
   - Multi-subtree responsive DOM (mobile/desktop variants): `.filter({ visible: true }).first()`.
   - Data-derived numbers: pin **count-independent structure** (child spans, gaps, padding) and give totals a floor + sanity range — counts change when specs legitimately append rows.
   - Shared mutable e2e state is a time bomb — each spec owns its data or reseeds.
3. **API smoke (bash)** — boots the standalone server with a **pinned** `DATABASE_URL` (immune to shell env traps), then curl-checks: health, auth round-trips (valid/invalid/unauthenticated), every read endpoint, one create + invalid-input rejection + a domain round-trip, delete, logout invalidation, page render, 404 guard, rate limit (`429`). Prints PASS/FAIL per step, exits non-zero, cleans up. The script pins its own environment **inside** itself — never per-command.

**Test counts are documentation claims:** the exact check totals live in AGENTS.md and must be updated in the same commit as any test change (count-lockstep), or the docs rot — the proven mechanism is neo-crm's `tests/docs-counts.test.ts`, which puts every live-tense count site under the unit gate: a stale count anywhere fails `bun run test`.

---

## §15 The Quality Gate (there is no CI until you add one — the local gate is the only gate)

```bash
bun run lint            # 0 errors (hook rules are errors); --max-warnings 0 preferred
bun run typecheck       # 0 errors
bun run test            # full unit suite, exact expected count
bun run build           # clean compile + standalone assembly (no ignoreBuildErrors)
./scripts/smoke-test.sh # full smoke suite against the build
bun run test:e2e        # full Playwright suite against the build
```

- **Order matters** (fast gates first); wire the whole thing into ONE `gate` script and run it before every push. `gate:full` adds drift sweeps at 390/768/1024/1440 widths plus a full-page sweep and an interior census when visual parity matters. *(neo-crm adopted this skill's build-as-type-gate posture in session-174 — the contract below is now in active family use, not aspiration.)*
- **Never weaken a guardrail to make a gate pass** — no disabled lint rules, no loosened types, no skipped hooks, no deleted tests. A green gate achieved by weakening the gate is not green.
- **A smoke leg must count what it executed, not only what passed.** project-management's conditional-skip guard silently drops downstream checks when an upstream step fails — a failing leg shrank the gate to 12 passed / 15 failed / 3 skipped (27 executed), and the RESULT line could never reach 30. Failure must be loud and complete.
- **Fresh-clone verification** is a periodic gate of its own: a clean `install → db:push → db:seed → dev` (and `install → typecheck → build`) must work from a pristine clone — lockfile drift and missing env assumptions surface only there. **Both legs bite in-family (verified 2026-10-25):** digma's unit leg ENOENTs without `cp .env.example .env` (its tests read `.env`), and zero-balance's `db:push` P1012-fails without it (its `env -u` discipline requires `.env` for every Prisma CLI leg, and its README quickstart omits the `cp`) — while neo-crm's entire unit leg runs pristine with no `.env` at all. Make the pristine path work, or put the `cp` line before the first command that needs it.
- When a count changes (routes, models, tests, checks), `rg "<old number>"` the entire doc set in the same commit.

---

## §16 Security Checklist (each line traces to a real incident class)

- [ ] All external input validated (Zod at every boundary) before use — including query params and uploads
- [ ] Parameterized queries only (Prisma) — never string-concatenated SQL
- [ ] No `dangerouslySetInnerHTML` anywhere; React escapes render text by default
- [ ] Passwords: scrypt + per-user salt + constant-time compare; pure crypto seam
- [ ] Sessions: HMAC-signed, httpOnly, `sameSite=lax`, `secure` in prod, TTL bounded, **tokenVersion revocation on reset**
- [ ] `AUTH_SECRET` enforced ≥ 16 chars, **fails hard in production**
- [ ] Reset tokens: 32-byte, **hashed at rest**, single-use, 60-min TTL; forgot-password is no-enumeration
- [ ] Login timing equalizer (miss branch burns the same scrypt)
- [ ] Auth routes rate-limited per IP with `Retry-After`; proxy-hop depth declared, fails closed — client-IP extraction never trusts the raw first `x-forwarded-for` hop (zb's limiter does; digma/neo's hops contract is the pattern)
- [ ] Content-Type CSRF gate + bounded body reads on every JSON parse
- [ ] OTP/verification attempt counters increment atomically (`updateMany`), never read-then-write — zb shipped the racy form
- [ ] In-app OTP/reset delivery OFF in production (`*_DISABLE_IN_APP_*`) — real mail transport owns it
- [ ] File uploads: validated names/types, regex-pinned serving routes, no path traversal
- [ ] Secrets never in logs, commits, or error envelopes; `.env` gitignored; `.env.example` mirrors the contract
- [ ] Threat model written in the PAD and re-read when the surface changes
- [ ] Known limitations **documented as known issues** (in-process limiter on multi-instance, stateless trade-offs) — an accepted-and-written risk is engineering; a silent one is a landmine

---

## §17 Performance & Production Deployment

- **Standalone output** is the deploy artifact: `next build` + copy `.next/static` and `public` into `.next/standalone` (keep the build script's copy steps). Start with `bun .next/standalone/server.js` **from the repo root** (or an absolute `DATABASE_URL` — the db-path seam handles both, but know which posture you're in).
- Server pages are thin and dynamic; heavy interactivity is client-isolated. No N+1 Prisma patterns — `_count` includes and composite indexes serve list views.
- Derived client selectors are `useShallow`-wrapped (§9) — that's the production crash you're preventing.
- **Multi-instance production requires:** PostgreSQL (or another server DB), `prisma migrate` (not `db push`), a shared-store rate limiter, and the proxy-hop env set. Until then, document the single-node posture honestly.
- Docker: the standalone output containers cleanly, but the template ships no Dockerfile — add one per target platform; don't cargo-cult.
- Observability: at minimum, structured startup lines (the `[db] DATABASE_URL → …` diagnostic line is load-bearing), request failures logged with codes. Console + `tee` is the floor, not the ceiling.

---

## §18 Debugging Guide (symptom → root cause → fix)

| Symptom | Root cause | Fix |
|---|---|---|
| `Error code 14: Unable to open the database file` | Wrong anchor (server started outside repo root) or shell-inherited absolute `DATABASE_URL` | Start via npm scripts from repo root; check `env | rg DATABASE`; absolute path for exotic service managers |
| App reads the WRONG database (data "missing") | Shell env beats `.env` (dotenv never overrides) | `env -u DATABASE_URL …`; scripts pin the value |
| Standalone server resolves db into `.next/standalone/db/…` | `server.js` chdirs before modules load | Keep `db-path.ts` in the import chain — never inline resolution |
| Login loops to `/login` | `AUTH_SECRET` changed between restarts | Keep the secret stable (prod: fail-hard surfaces it) |
| Sudden 429s | Fixed-window limiter engaged | Wait `Retry-After`; restart clears in-memory buckets |
| "Maximum update depth exceeded" in production only | Derived store selector without `useShallow` | Wrap the selector (§9); pin with an e2e against the build |
| Hydration mismatch / effect races | `useEffect(() => setState)` copying props | Remount-via-key or adjust-during-render |
| E2E flaky after reseed | Session cookies point at deleted user rows | Re-login (storageState) after any reseed |
| E2E strict-mode violations | 2–3 responsive DOM subtrees rendered | `.filter({ visible: true }).first()` |
| A11y probe can't find a DOM-present element | `display:none` subtrees excluded from a11y tree | CSS selectors + visibility filters |
| `rounded-full` asserts fail | v4 `calc(infinity * 1px)` serialization | Assert radius > 1000 |
| Ring/shadow asserts fail on color | v4 oklab serialization | Match `/0\.5\) 0px 0px 0px 4px/`-style patterns |
| Dev badge in screenshots | Captured from `next dev` | Capture docs screenshots from the production build |
| Charts show frame instead of grid (recharts 2.x) | Explicit `tick: undefined` prop | Pass the prop only with a value |
| Pristine `db:push` fails P1012 (`Environment variable not found: DATABASE_URL`) | Prisma CLI leg needs `.env` and the quickstart skipped the `cp` | `cp .env.example .env` first; put the `cp` line before the first db command in the README |

**Diagnostic doctrine:** reproduce before trusting; classify the gate (install/type/lint/test/build/db) before fixing; prefer machine-readable diagnostics (computed styles, structured JSON, `/proc/<pid>/environ`) over terminal echo; fix at the source; never weaken a guardrail to pass.

---

## §19 Documentation System & Agent Conventions

- **Five documents, five jobs:** `README.md` (user-facing: features, quickstart, env table, testing), `AGENTS.md` (operator quick-reference: commands, architecture facts you'd guess wrong, ≤ ~300 lines), `CLAUDE.md` (the agent contract: principles, standards, workflow, anti-patterns, ≤ ~600 lines), `Project_Architecture_Document.md` (the blueprint: ADRs, topology, security, testing, deployment, known issues), `SKILL.md` (this — the distilled engineering memory).
- **Doc-budget rule (learned from the family's own bloat):** when a SKILL exceeds ~1,500 lines, move session-history narrative into dated archive files and keep the living doc to contracts + lessons. A 12,000-line skill is a liability: future agents pay the whole cost on every read and the signal decays.
- **The code-wins rule:** when code and any doc disagree, the code wins — then the doc is fixed in the same commit.
- **Same-commit lockstep:** behavior changes update README/AGENTS/CLAUDE/PAD revision blocks together; count changes trigger a repo-wide `rg` for the old number.
- **Session logs** (dated, per work session: what changed, what was verified, what remains) are the audit trail that makes AI-agent development reviewable — keep them in `docs/`, out of the agent's standing context.
- Conventional Commits; `main` only is acceptable for solo/small teams **with the gate as the bouncer**; never commit `.env`, `*.key`, `db/*.db`, logs.
- Vendored non-app catalogs (agent skills, research scripts) live outside the app tree, ignored by lint/tsconfig/vitest, and are candidates for removal when forking the template.

---

## §20 Known-Issues Register & Pre-Ship Checklist

Maintain a **Known Issues table** in the PAD — Priority / Issue / Impact / Status — and sweep it every few sessions (an "Open" row that's actually fixed is a lie; a shipped default that's actually risky must be a HIGH row). The most honest register in the family self-reported a HIGH on its own forgot-password default; that posture is the standard.

**Pre-ship (condensed):**

```bash
bun run lint && bun run typecheck && bun run test && bun run build \
  && ./scripts/smoke-test.sh && bun run test:e2e
git status   # no .env, *.key, db/*.db, dev.log, server.log staged
```

- [ ] Full gate green (§15), exact expected counts
- [ ] Changed surfaces re-verified in BOTH auth states (logged-out AND logged-in) at 390 / 768 / 1440
- [ ] Empty-state, loading, and error paths exercised for every changed surface
- [ ] Security checklist (§16) re-read for anything the change touched
- [ ] All five docs updated in the same commit; counts lockstep
- [ ] Session log written; known-issues register swept
- [ ] If env/counts changed: fresh-clone bootstrap verified

---

## Appendix A — Distilled Lessons Canon (transferable, battle-proven)

**Measurement & parity**
1. Measure the computed DOM; screenshots (and VLM reads) mislead — colors, shadows, and "missing" elements need computed-style proof (~30% micro-styling misreads disproven by measurement).
2. Presentation attributes are the lowest cascade tier — read COMPUTED styles, never the attribute.
3. Measure SPAs post-hydration; measure every route in both auth states; a redirect that fires in one auth state is invisible to a single-state census.
4. Pin the count-independent structure, not rendered totals; give data-derived widths a floor + range.
5. When observation can't discriminate a formula, read the shipped bundle.
6. Re-crawl/re-measure before every remediation pass — specs age between sessions.

**React & state**
7. The dev server lies about production hydration — the production-build e2e suite is not optional.
8. A zustand selector that allocates is an infinite loop waiting to happen — `useShallow` is the law.
9. Never copy props into state via effect — remount-via-key or adjust-during-render.
10. Anchor-wrapped interactive children need a `preventDefault`-armed button-origin guard.
11. Prefer library defaults over bespoke micro-styling — bespoke values are drift liabilities.

**Environment & build**
12. The standalone server chdirs before your code runs; bundlers rewrite `import.meta.url` — path resolution must be a tested seam, not a CWD assumption.
13. dotenv never overrides the shell — pin env INSIDE scripts, not per-command.
14. Two lockfiles in one repo is a reproducibility bug — one package manager, one lockfile.
15. A reseed invalidates every live session — re-login before diagnosing "empty views + healthy DB".
16. Never `rm` a db file under a running server — the process serves the deleted inode.

**Tailwind v4**
17. The five traps + the cascade law + `rounded-full` infinity + ring-without-shadow + missing `cursor: pointer` (§12). Each one produced a real bug class in the source codebases.

**Testing**
18. Rate limiters count *your* tests — one setup login + storageState, shared per run.
19. Shared mutable e2e state is a time bomb; each spec owns its data.
20. Exit animations keep nodes mounted ~300ms — settle-wait before asserting closed.
21. Assert against the production build; assert structure over totals; keep doc counts lockstep with reality.

**Security & process**
22. Stateless sessions need a revocation dimension (tokenVersion) or a reset can't kill a stolen cookie.
23. In-app delivery of OTP/reset links is demo posture — disable knobs + real transport in prod.
24. Docs drift the moment code lands — same-commit updates, code-wins rule, `rg` the old number when counts change.
25. An honest known-issues register is a feature: self-reported risk is engineering; silent risk is a landmine.
26. When a count changes, every doc copy of that number changes in the same commit — count-claims drift independently across documents.
27. Read-then-write counters race under concurrency — the family's own zb OTP attempt counter is the shipped counter-example; atomic `updateMany` increments are the law (§5).
28. A smoke gate that silently skips checks when upstream fails undercounts its own failure — count executed-vs-passed, and make failure loud and complete (pm's skip guard, P-8).

---

## Appendix B — Quick Reference Card

```bash
bun install && cp .env.example .env && bun run db:push && bun run db:seed && bun run dev
bun run lint && bun run typecheck && bun run test && bun run build \
  && ./scripts/smoke-test.sh && bun run test:e2e      # the gate
bunx prisma generate        # after schema changes
```

- **Envelope:** `{ok, data} | {ok:false, error:{code, message}}` — `ok()/fail()`, never throw across a handler.
- **Session cookie:** `base64url({uid,iat,exp,v}) + "." + HMAC-SHA256` — httpOnly, lax, secure-in-prod, 7-day TTL, `v` = row tokenVersion.
- **File map:** `src/app` (routes) · `src/components/{ui,layout,<feature>}` · `src/lib` (pure seams) · the ONE store (family practice varies: only neo-crm uses `src/stores/`; digma/pm/zb keep it at `src/components/<domain>/store.ts` — pick one location and document it) · `prisma` (schema + seed) · `scripts` (smoke, census, sweeps) · `tests/e2e`.
- **Env set:** `DATABASE_URL`, `AUTH_SECRET`, `NEXT_PUBLIC_SITE_URL` (+ `*_PROXY_HOPS`, `*_DISABLE_IN_APP_*` in prod).
- **The one rule that outranks the rest:** when code and this document disagree, the code wins — then fix this document in the same commit.

---

## Validation & Change Log (v1.1.0 — 2026-10-23)

Validated against the four source repositories at HEADs digma `1ad583b2`, neo-crm `f9bc1bf`, project-management `9ff03bc`, zero-balance `b967d3f`: mechanical census, four documentation deep-dives with file:line verdicts, and executed pipelines per repo — install / prisma generate / typecheck / build green ×4; unit suites 2,501 / 2,717 / 138 / 108 all green (digma's requires the `cp .env.example .env` bootstrap — `tests/lows-s99.test.ts` reads `.env`); smoke suites 73 / 14 / 30 / 35 all green under their documented invocations. Playwright e2e not executed (no browser binaries). This document is byte-identical to the copy vendored at `neo-crm/skills/web-application/SKILL.md`, which session-174 cited while adopting §2/§15's posture — the skill is in active use inside the family it was distilled from.

**Corrections (all Verified):**

1. **§4 money rule restated to match the source design.** "Integer cents end-to-end, floats only at the format boundary" overstated zero-balance's ADR-004: zb stores/exchanges decimal amounts (Prisma `Float` columns) and converts to integer cents **at every aggregation boundary**. The safety property (IEEE-754 drift never reaches a total) is unchanged; the schema contract is not.
2. **§11 wrapper list fixed.** The area chart is `RevenueLineChart` (named, not generic "area chart"); `Sparkline` lives in the shared page-parts module, not `charts.tsx`; and the "empty-state fallback" claim inverted the source doctrine — neo-crm's wrappers deliberately render the REAL chart at all-zero data (only Sparkline nulls on empty). Rewritten as a "declared zero-data policy" rule.
3. **§7 attributions made precise.** The date rules (real-calendar-date refinement, `""` → `undefined` preprocess) are zero-balance's; the three-state PUT helpers are neo-crm's (zb's PATCH is deliberately two-state: `null` rejected, `""` elided). Both were already correct as prescriptions; they are now correct as lineage.
4. **§8 layout-gate wording refined.** "Runs the session guard server-side (redirect, not client flash)" → the gate *decision* is server-side (the guest never receives app HTML); the redirect itself may be a client shim (neo-crm session-147 — a server layout cannot know the current path).
5. **Frontmatter provenance refreshed.** digma_SKILL v1.155 → **v1.158.0**; neo-crm_SKILL v1.168 → **v1.171.0**; project-management_SKILL "(v2.15-era)" → **v1.0.0** (the v2.15 is the *app's* remediation version recorded inside it); zb v1.0.0. Combined commits 1,226 at distillation → 1,244 at re-validation.
6. **§2/§15 strengthened with in-family adoption + empirical proof.** Playwright floor 1.63+ (family range); `NEXT_PUBLIC_SITE_URL` build-time note (+ digma's `DIGMA_SITE_URL` variant); the `*_DISABLE_IN_APP_*` row now records that zb shipped OTP delivery with **no knob and no TTL** (a gap, not a pattern); §3 item 3 records the reproduced natural experiment (disciplined sibling 35/35 vs undefended 12/30 under the same polluted shell) and the seed-through-the-seam rule (a bare-`PrismaClient` seed bypasses it).
7. **§14 count-lockstep upgraded from advice to mechanism** — neo-crm's `tests/docs-counts.test.ts` already test-gates every count claim; §15 notes `gate:full`'s full-page sweep + interior census and that neo-crm adopted the build-as-type-gate in session-174.
8. **Appendix B file map corrected** — only neo-crm keeps the store in `src/stores/`; the others use `src/components/<domain>/store.ts`.

**Validated as accurate and unchanged:** the auth contract (§5 — every neo-crm rate-limit constant, the timing equalizer, hashed reset tokens, tokenVersion, and the boot gate confirmed at line level), the DATABASE_URL contract's mechanism (§3 — all four anchors and traps confirmed; only strengthened), the Tailwind v4 trap catalog (§12 — traps (a)–(e), (g), (h), (l) located in zb's docs; the `@utility` cascade rule in digma+neo's; the `cursor: pointer` rule in zb's base layer), the testing doctrine (§14 — including the `.filter({visible:true})` and settle-wait lessons), the debugging table (§18), and the lessons canon (Appendix A — lesson 14 "two lockfiles" was even cited by neo-crm's session-174 when it fixed exactly that).

---

## Validation & Change Log (v1.2.0 — 2026-10-25)

Re-validated against the four source repositories at HEADs digma `2fa13d7e`, neo-crm `02ac27eb`, project-management `9ff03bcd` (unchanged), zero-balance `1a3553da`: mechanical census, four documentation deep-dives with file:line verdicts, and executed pipelines per repo — typecheck 0 errors ×4; unit suites 2,588 / 2,760 / 138 / 108 all green (digma still requires the `cp .env.example .env` bootstrap — its `tests/lows-s99.test.ts` reads `.env`; neo-crm runs pristine with **no** `.env`); builds ×4; smoke suites 73 / 14 / 30 / 35 all green; and the P-6 polluted-shell reproduction (pm collapses) plus the zb immunity probe re-run in the same session. Playwright e2e not executed (no browser binaries) — static censuses: 262 / 192 / 115 / 319 checks. The v1.1.0 generation remains byte-identical to the copies vendored at `skills/web-application/SKILL.md` in digma/neo-crm/zero-balance; this v1.2.0 supersedes it and is not yet vendored.

**Corrections & additions (all Verified):**

1. **§2/§11 recharts row updated.** neo-crm migrated 2.15.4 → 3.10.1 in session-176 (ADR-021, commit f484701 naming "the N-3 retirement"); the family is now uniform on 3.10.x. The §11 wrapper list, the Sparkline location, and the zero-data policy were re-verified at HEAD and survived the major **unchanged** — the wrapping discipline did its job. The 2.x→3.x migration doctrine (accessibilityLayer={false} pins, tooltipFormatter adapter, PieLabel bridge, e2e grid sentinel) is now a §11 rule.
2. **§11 palette wording corrected.** neo-crm's `CHART_COLORS` is literal hex in `constants.ts`; the CSS `--color-chart-*` token family is a separate surface per the code's own comment — "palette from tokens" overstated the coupling.
3. **§5 rate-limit shapes made precise.** The per-route constants (login 10 / signup 10 / resend 5 / verify 20 / forgot 10 / reset 10 / upload 20 per 15 min) are neo-crm's, re-confirmed at line level; digma ships a single shared credential bucket (10/15 min) plus `ai` (20/5 min) and `crud` (60/5 min). Both shapes are in-family — pick one and document it.
4. **§5 TTL nuance added.** zero-balance runs a 30-day session TTL while its own PAD documents 7-day — "pick one and document" cuts both ways, and zb's doc lost. digma/pm/neo run 7-day.
5. **§5 secret-enforcement status updated.** digma's session-181 (S181-C) adopted the fail-hard production posture — its in-code comment cites "the master skill §5 contract". pm and zb still ship dev-fallback constants.
6. **§5/§16 atomicity + client-IP rules added.** OTP attempt counters must increment atomically — zb shipped read-then-write (racy); client-IP extraction must declare proxy trust and fail closed — zb trusts the first `x-forwarded-for` hop with no hops contract.
7. **§15 smoke-gate arithmetic rule added.** A smoke leg must report executed-vs-passed; pm's conditional-skip guard silently dropped 3 checks under failure (12 passed / 15 failed / 3 skipped, 27 executed — the RESULT line could never reach 30).
8. **§15/§18 fresh-clone DB-leg hazard added.** zb's pristine `db:push` fails P1012 (`Environment variable not found: DATABASE_URL`) because the `env -u` discipline requires `.env` for every Prisma CLI leg and its README quickstart omits the `cp` — the fresh-clone gate must cover the DB leg, not just the unit leg (digma's D-7 is the unit-leg twin; neo-crm's pristine-no-`.env` posture is the standard).
9. **Appendix A lessons 27–28 added** (atomic counters; smoke skip-guards), each traced to a live v1.2 finding.

**Validated as accurate and unchanged at v1.2:** the §0 scaffolding order; the §3 DATABASE_URL contract (all anchors re-confirmed; the seed-through-the-seam rule re-proven load-bearing by the P-6 reproduction and the zb immunity probe in one session); neo-crm's auth contract at line level (every rate-limit constant, the timing equalizer, hashed reset tokens, tokenVersion eviction, the boot gate, and the 15-minute verification TTL — `VERIFICATION_TTL_MS` at verification.ts:33); the §6 handler idiom and status discipline; the §7 validation attributions (zb's calendar-date refinement and two-state PATCH; neo's three-state `clearable*` helpers); the §9 store doctrine (`useShallow`; store location: `src/stores/` in neo-crm vs `src/components/<domain>/…-store` elsewhere — digma `editor-store.ts`, zb `budget/store.ts`, pm `orbital/store.ts`); the §12 Tailwind v4 trap catalog; the §13 a11y floor; the existing §18 rows; and the code-wins rule itself — which the companion evaluation report had to apply to one of its own re-validation claims (its §13.1 #17 records the F-6 revert: pm and zb both carry `noImplicitAny: false` since their initial commits).
