---
name: web-application-engineering
description: condensed engineering reference for scaffolding, extending, and maintaining production-grade web applications. It synthesizes the hardest lessons from building high-parity, test-heavy Next.js 16 applications. Next.js 16 (App Router, Standalone Output) + React 19 + TypeScript (Strict) + Tailwind CSS v4 (CSS-First) + Shadcn/UI (Radix Primitives) + ONE Zustand store + Zod-validated API + Prisma/SQLite (or Postgres). Validated against the four source repos (digma, neo-crm, project-management, zero-balance); the fuller distillation is web-application_SKILL.md.
version: 1.1.0
last_updated: 2026-10-23
provenance: "Validated 2026-10-23 against repo HEADs digma 1ad583b2, neo-crm f9bc1bf, project-management 9ff03bc, zero-balance b967d3f. See §11 for the correction log."
---

# Generalized Web Application Engineering Skill (The "ORBITAL-ZB" Standard)

> **How to use this document:** This is the definitive engineering reference for scaffolding, extending, and maintaining production-grade web applications. It synthesizes the hardest lessons from building high-parity, test-heavy Next.js 16 applications.

---

## §1 Project Identity & Design Philosophy

**The Stack:** Next.js 16 (App Router, Standalone Output) + React 19 + TypeScript (Strict) + Tailwind CSS v4 (CSS-First) + Shadcn/UI (Radix Primitives) + Zustand + Prisma/SQLite (or Postgres).

**Core Principles:**
1. **The Local Gate is the Only Gate:** No hosted CI is trusted. Nothing is pushed until `lint -> typecheck -> test -> build -> smoke -> e2e` is green.
2. **Server Components by Default:** Pages fetch and gate server-side. Interactivity is isolated in `"use client"` view components.
3. **Pure Domain Seams:** All business logic, data transformation, and validation live in pure functions in `src/lib/`. These seams are heavily unit-tested; UI components merely consume them.
4. **Degrade, Never Fail:** AI integrations and external APIs must have deterministic fallbacks. A failed network call should result in a graceful toast + empty state, never a thrown error that breaks the React render tree.

---

## §2 Tech Stack & Environment

| Layer | Technology | Version | Notes |
|---|---|---|---|
| Framework | Next.js (App Router, Standalone Output) | >=16.x | `output: 'standalone'` + pinned `outputFileTracingRoot`; do NOT set `ignoreBuildErrors` — the build is the type gate. |
| UI Runtime | React | >=19.x | `useSyncExternalStore` for cross-chunk stores. |
| Language | TypeScript (Strict) | >=5.x | Full strictness — never loosen `noImplicitAny`; `tsc --noEmit` is the fast gate, the build is the enforcer. |
| Styling | Tailwind CSS (CSS-first) | >=4.x | NO `tailwind.config.js`. Tokens in `globals.css` `@theme`. |
| Primitives | Shadcn/UI / Radix | Latest | Accessible dialogs, dropdowns, sheets, tabs. |
| Client State | Zustand | >=5.x | **ONE store per application** (all four source repos: crm-store, editor-store, orbital store, budget store). Derived selectors MUST use `useShallow`. |
| ORM / DB | Prisma / SQLite | >=6.x | Use `db-path.ts` anchors for standalone deployments. |
| Validation | Zod | 4.x | At every API boundary — nothing reaches Prisma unvalidated. |
| Unit Tests | Vitest | 5.x | Focus on pure domain seams. |
| E2E Tests | Playwright | 1.63+ | Critical user journeys + visual parity, against the production build. |

**Environment Variables:**
* `DATABASE_URL`: Required. Relative `file:` for dev (resolved against `prisma/schema.prisma` via `db-path.ts`), absolute for production standalone. Pin it INSIDE npm scripts (inline for runtime, `env -u` for the Prisma CLI) so a polluted parent shell can never redirect the database — validated load-bearing: under a shell-exported `DATABASE_URL`, the disciplined sibling ran 35/35 smoke untouched while the undefended one collapsed to 12/30.
* `AUTH_SECRET`: Required for session signing — **fails hard at boot in production** if missing or shorter than 16 chars (generate with `openssl rand -hex 32`).
* `NEXT_PUBLIC_SITE_URL`: Canonical origin for metadata/sitemap/robots — inlined at build time, so set it BEFORE `bun run build` in production. (Family naming: neo-crm/pm/zero-balance use `NEXT_PUBLIC_SITE_URL`; digma uses `DIGMA_SITE_URL`.)

---

## §3 The Design System (Tailwind v4 CSS-First)

All tokens live in ONE plain `@theme` block in `src/app/globals.css`.

**Critical Tailwind v4 Traps to Avoid:**
1. **NO `var()` chains for colors in `@theme`:** The current v4 build drops them. Use literal hex values.
2. **NO `var()` for fonts:** `next/font` scopes font variables to `<body>`, causing `var(--font-sans)` at `:root` to compute to invalid and silently fall back to the UA serif default. Use literal font-family strings.
3. **NO `tailwind.config.js`:** Reintroducing the legacy config file is the #1 cause of the "flat/minimal look" bug in v4. *(Caveat from the source repos: project-management is the one sibling that still carries a legacy `tailwind.config.ts` for shadcn HSL tokens + tailwindcss-animate — kept deliberately per its CLAUDE.md; new scaffolds should not copy it.)*
4. **Stroke Widths:** If using Lucide icons, be aware that CSS `stroke-width` styles override SVG presentation attributes. Measure the reference DOM to ensure consistency.
5. **Custom utilities:** define them with v4-native `@utility`, never inside `@layer utilities` (custom classes in `@layer utilities` emit after generated utilities and silently lose the cascade to arbitrary utilities on the same element).

---

## §4 Architecture & State Management

### 4.1 Session-Gated Pages
Every gated `page.tsx`/layout calls a server-side `getSessionUser()` and the guest never receives the app's HTML. The redirect itself may be a client shim (`router.replace('/login?from_url=…')`) — a server layout cannot know the current path. Client components **never** gate themselves; they assume the user is authenticated or handle empty states gracefully.

### 4.2 The API Envelope
All API routes return a standardized envelope:
```typescript
type ApiResponse<T> = { ok: true; data: T } | { ok: false; error: { code: string; message: string } };
```
Client-side fetch wrappers unwrap this envelope. Failures are converted to toasts + `null` returns, preventing unhandled promise rejections from crashing the UI.

### 4.3 State Management (Zustand)
Use Zustand for complex client-side state (multi-step wizards, interactive dashboards, canvas editors) — **ONE store per application**.
* **The Replace Contract:** For complex lists or arrays, prefer optimistic full-list replacements over partial PATCH updates. It simplifies undo/redo logic and prevents race conditions. (digma ADR-005.)
* **Store Isolation:** module-level singletons CAN be duplicated across code-split chunks under Turbopack — observed in digma (ADR-007: two client chunks each got their own copy of a toast-store module, so toasts fired from a page never reached the layout's Toaster). The fix pattern: keep the state AND the listener set on `globalThis` and subscribe via `useSyncExternalStore`. Apply it to any singleton that must be shared across chunk boundaries.

---

## §5 Dashboard & Charting Patterns

### 5.1 Time-Aware Chrome
Dashboards should feel alive. Implement time-aware greetings ("Good Morning/Afternoon") and dynamic imagery (e.g., rotating hero images based on time of day). Boundary logic for these changes must be unit-tested.

### 5.2 Charting & Data Visualization
* **Pure Calculation Seams:** Never calculate chart data inside the React component. Extract data aggregation (sums, averages, drill-downs) into pure functions in `src/lib/`.
* **Visual Parity Testing:** Charts are prone to silent regressions. Write Playwright tests that verify the exact dimensions, colors, and text labels of rendered SVG/Canvas elements.
* **Drill-Down Architecture:** Use state to track the "drill-down" level (the source apps keep it in store/component state, NOT the URL). Reflect drill-down state in URL parameters only if deep-linking is an explicit requirement — decide the ownership deliberately.

### 5.3 Responsive Layouts
* **Desktop:** Sticky sidebars with collapsible icon rails.
* **Tablet (768px-1024px):** Floating pill navigation or condensed headers.
* **Mobile (<768px):** Full-bleed chrome, bottom-attached tab bars (with active-state chips), and bottom-sheet dialogs instead of standard modals.

---

## §6 Auth & Security Implementation

### 6.1 Hand-Rolled or Minimalist Auth
Avoid heavy auth libraries if possible. A minimalist approach using `scrypt` for password hashing and HMAC-signed HTTP-only cookies for sessions provides maximum control and minimal bundle size.

### 6.2 Rate Limiting
Implement fixed-window, in-process rate limiting on all public auth routes (login, register, forgot-password).
* Return `429 Too Many Requests` with a `Retry-After` header.
* Ensure E2E tests use a shared `storageState` to avoid tripping the rate limiter during test runs.

### 6.3 Validation
**Zod at every API boundary** — one `src/lib/schemas.ts`/`validation.ts` consumed by every route via a `parseBody()`-style helper, so nothing reaches Prisma unvalidated. Enforce length caps, enum membership (enums imported from one constants module), real-calendar-date refinements (`Date.parse` accepts `2026-02-30`), and empty-string normalization for native date inputs. Hand-rolled validation is a documented, deliberate alternative (digma/pm) — but the family's most evolved members (zero-balance, neo-crm) both chose Zod; if you hand-roll, do it as an ADR, not an accident.

---

## §7 Testing Strategy (The Local Gate)

### 7.1 The Test Pyramid
1. **Unit Tests (Vitest):** Pure domain seams. Test the math, the formatting, the sanitization. Aim for 100% coverage of `src/lib/`.
2. **Smoke Tests (Shell/Bash):** Fast HTTP-level checks against the standalone build. Verify that routes return 200/401, auth gates work, and basic CRUD operations succeed.
3. **E2E Tests (Playwright):** Critical user journeys. Login, create a resource, view the dashboard, log out. Use `storageState` to share auth across tests.

### 7.2 Visual Parity & "The Parity Pin"
When cloning or matching a specific design, write a test that asserts the element's **computed styles and geometry** — the family's parity specs pin `toHaveCSS` / `boundingBox` values, not class lists.
* *Example:* `await expect(chip).toHaveCSS("border-radius", "14px")` and `Math.abs(chipBox.width - tabBox.width) < 2`
* This prevents "silent drift" where a component looks similar but uses different underlying tokens.

---

## §8 Anti-Patterns & Common Bugs

1. **React 19 `setState` in Effects:** Never call `setState` synchronously inside a `useEffect` body. It triggers a lint error. Use render-time state adjustment or async boundaries.
2. **`window.location` for Auth Redirects:** Breaks server-component header swaps. Always use Next.js `router.push()` + `router.refresh()`.
3. **Standalone SQLite Path Resolution:** In production standalone builds, relative `file:` URLs resolve against the `.next/standalone` folder, not the repo root. Always use a `db-path.ts` helper that dynamically resolves the correct absolute path based on `process.cwd()` or environment variables.
4. **Next.js Case-Sensitive Redirects:** In Next.js 16, `next.config` `redirects()` matches sources **case-insensitively** and the per-rule `caseSensitive` flag is NOT honored — attempting a `/editor` → `/Editor` redirect there self-loops (observed live: ERR_TOO_MANY_REDIRECTS). Enforce casing in a proxy/middleware (digma's `src/proxy.ts` + ADR-008 pattern) instead.
5. **Dead Controls Below Breakpoints:** If a UI element only appears on desktop (`hidden md:flex`), its toggle/button must also be hidden on mobile. Rendering a button that does nothing on mobile is a critical accessibility failure.

---

## §9 Deployment

### 9.1 The Standalone Build
Always configure `output: 'standalone'` in `next.config.js`. This traces dependencies and produces a minimal `server.js` file that can be run with `node` without requiring `node_modules`.

### 9.2 Pre-Ship Checklist
```bash
bun run lint          # clean
bun run typecheck     # clean
bun run test          # unit tests green
bun run build         # standalone build succeeds
./scripts/smoke-test.sh # smoke tests green
bun run test:e2e      # e2e tests green
```

---

## §10 Lessons Learnt

1. **Measure the Live DOM:** Never guess Tailwind classes. Use browser devtools to extract the exact computed styles and classes from the reference design.
2. **TDD the Seams:** Write the unit test for a calculation before writing the calculation. Write the E2E test for a route before wiring the UI.
3. **Docs Drift:** If code and documentation disagree, the code wins. Update the documentation in the same commit that changes the behavior.
4. **Session Harvesting:** In E2E testing, log in once in the global setup, save the `storageState`, and reuse it. Logging in per-test will inevitably trigger rate limiters and flaky tests.

---

## §11 Validation & Change Log (v1.1.0 — 2026-10-23)

Validated against the four source repositories (HEADs digma `1ad583b2`, neo-crm `f9bc1bf`, project-management `9ff03bc`, zero-balance `b967d3f`), including executed pipelines (install → prisma → typecheck → build → unit → smoke per repo: 2,501/2,717/138/108 unit and 73/14/30/35 smoke, all green under documented invocations). This document and its fuller sibling `web-application_SKILL.md` are byte-identical to copies vendored inside `neo-crm/skills/`.

**Corrections (all Verified):**
1. `APP_SITE_URL` → **`NEXT_PUBLIC_SITE_URL`** — the original env var matched no source repo (neo-crm/pm/zb use NEXT_PUBLIC_SITE_URL; digma uses DIGMA_SITE_URL).
2. "One store per complex domain" → **ONE store per application** — all four source repos run exactly one Zustand store.
3. §6.3 "Hand-roll validation… or a lightweight schema library" → **Zod at every API boundary** — the family's most evolved members (zero-balance, neo-crm) both standardized on Zod 4; hand-rolling survives only as digma/pm's documented deliberate choice.
4. §7.2 parity-pin example `toHaveClass('bg-purple-50…')` → **computed-style/geometry assertions** (`toHaveCSS`, `boundingBox`) — what the family's parity specs actually pin.
5. §4.3 Turbopack store-duplication re-attributed precisely: it is digma ADR-007's toast-store lesson (globalThis + `useSyncExternalStore`), not a property of the domain stores.
6. §5.2 drill-down URL claim reframed — the source apps keep drill-down state out of the URL; URL reflection is only for explicit deep-linking requirements.
7. §8.4 sharpened with the observed failure mode (case-insensitive source matching; `caseSensitive` flag not honored; ERR_TOO_MANY_REDIRECTS self-loop) — digma ADR-008/proxy.ts, validated.
8. Added: build-as-type-gate (never `ignoreBuildErrors`), full TS strictness, `useShallow` selector law, the `@utility`-vs-`@layer utilities` cascade rule, pm's `tailwind.config.ts` caveat, inline-`DATABASE_URL`/`env -u` script discipline (empirically load-bearing), and the server-gate + client-shim-redirect nuance.
