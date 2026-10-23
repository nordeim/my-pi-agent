---
name: web-application-engineering
description: definitive engineering reference for scaffolding, extending, and maintaining production-grade web applications. It synthesizes the hardest lessons from building high-parity, test-heavy Next.js 16 applications. Next.js 16 (App Router, Standalone Output) + React 19 + TypeScript (Strict) + Tailwind CSS v4 (CSS-First) + Shadcn/UI (Radix Primitives) + Zustand + Prisma/SQLite (or Postgres).
version: 1.0.0
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
| Framework | Next.js (App Router, Turbopack) | >=16.x | Standalone output enabled. |
| UI Runtime | React | >=19.x | `useSyncExternalStore` for cross-chunk stores. |
| Language | TypeScript (Strict) | >=5.x | `bun run typecheck` is the manual gate. |
| Styling | Tailwind CSS (CSS-first) | >=4.x | NO `tailwind.config.js`. Tokens in `globals.css` `@theme`. |
| Primitives | Shadcn/UI / Radix | Latest | Accessible dialogs, dropdowns, sheets, tabs. |
| Client State | Zustand | >=5.x | One store per complex domain (e.g., Dashboard, Editor). |
| ORM / DB | Prisma / SQLite | >=6.x | Use `db-path.ts` anchors for standalone deployments. |
| Unit Tests | Vitest | Latest | Focus on pure domain seams. |
| E2E Tests | Playwright | Latest | Focus on critical user journeys and visual parity. |

**Environment Variables:**
* `DATABASE_URL`: Required. Use relative paths for dev, absolute for production standalone.
* `AUTH_SECRET`: Required for session signing.
* `APP_SITE_URL`: Required for SEO and absolute redirects.

---

## §3 The Design System (Tailwind v4 CSS-First)

All tokens live in ONE plain `@theme` block in `src/app/globals.css`.

**Critical Tailwind v4 Traps to Avoid:**
1. **NO `var()` chains for colors in `@theme`:** The current v4 build drops them. Use literal hex values.
2. **NO `var()` for fonts:** `next/font` scopes font variables to `<body>`, causing `var(--font-sans)` at `:root` to compute to invalid and silently fall back to the UA serif default. Use literal font-family strings.
3. **NO `tailwind.config.js`:** Reintroducing the legacy config file is the #1 cause of the "flat/minimal look" bug in v4.
4. **Stroke Widths:** If using Lucide icons, be aware that CSS `stroke-width` styles override SVG presentation attributes. Measure the reference DOM to ensure consistency.

---

## §4 Architecture & State Management

### 4.1 Session-Gated Pages
Every `page.tsx` calls a server-side `getSessionUser()` function. If unauthenticated, it redirects to `/login?from_url=...`. Client components **never** gate themselves; they assume the user is authenticated or handle empty states gracefully.

### 4.2 The API Envelope
All API routes return a standardized envelope:
```typescript
type ApiResponse<T> = { ok: true; data: T } | { ok: false; error: { code: string; message: string } };
```
Client-side fetch wrappers unwrap this envelope. Failures are converted to toasts + `null` returns, preventing unhandled promise rejections from crashing the UI.

### 4.3 State Management (Zustand)
Use Zustand for complex client-side state (e.g., multi-step wizards, interactive dashboards, canvas editors).
* **The Replace Contract:** For complex lists or arrays, prefer optimistic full-list replacements over partial PATCH updates. It simplifies undo/redo logic and prevents race conditions.
* **Store Isolation:** Never use module-level singletons for client state if code-splitting is involved (Turbopack will duplicate the store). Use `globalThis` or `useSyncExternalStore` patterns.

---

## §5 Dashboard & Charting Patterns

### 5.1 Time-Aware Chrome
Dashboards should feel alive. Implement time-aware greetings ("Good Morning/Afternoon") and dynamic imagery (e.g., rotating hero images based on time of day). Boundary logic for these changes must be unit-tested.

### 5.2 Charting & Data Visualization
* **Pure Calculation Seams:** Never calculate chart data inside the React component. Extract data aggregation (sums, averages, drill-downs) into pure functions in `src/lib/`.
* **Visual Parity Testing:** Charts are prone to silent regressions. Write Playwright tests that verify the exact dimensions, colors, and text labels of rendered SVG/Canvas elements.
* **Drill-Down Architecture:** Use state to track the "drill-down" level. Ensure that URL parameters reflect the current drill-down state so that deep-linking works correctly.

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
Hand-roll validation in `src/lib/validation.ts` or use a lightweight schema library. Enforce length caps, enum membership, and hex checks before data ever reaches the database.

---

## §7 Testing Strategy (The Local Gate)

### 7.1 The Test Pyramid
1. **Unit Tests (Vitest):** Pure domain seams. Test the math, the formatting, the sanitization. Aim for 100% coverage of `src/lib/`.
2. **Smoke Tests (Shell/Bash):** Fast HTTP-level checks against the standalone build. Verify that routes return 200/401, auth gates work, and basic CRUD operations succeed.
3. **E2E Tests (Playwright):** Critical user journeys. Login, create a resource, view the dashboard, log out. Use `storageState` to share auth across tests.

### 7.2 Visual Parity & "The Parity Pin"
When cloning or matching a specific design, write a test that asserts the exact Tailwind classes or computed styles of the element.
* *Example:* `expect(element).toHaveClass('bg-purple-50 text-purple-700')`
* This prevents "silent drift" where a component looks similar but uses different underlying tokens.

---

## §8 Anti-Patterns & Common Bugs

1. **React 19 `setState` in Effects:** Never call `setState` synchronously inside a `useEffect` body. It triggers a lint error. Use render-time state adjustment or async boundaries.
2. **`window.location` for Auth Redirects:** Breaks server-component header swaps. Always use Next.js `router.push()` + `router.refresh()`.
3. **Standalone SQLite Path Resolution:** In production standalone builds, relative `file:` URLs resolve against the `.next/standalone` folder, not the repo root. Always use a `db-path.ts` helper that dynamically resolves the correct absolute path based on `process.cwd()` or environment variables.
4. **Next.js Case-Sensitive Redirects:** Next.js 16 matches redirect sources case-insensitively. If you need to enforce casing (e.g., `/editor` -> `/Editor`), do it in a proxy or middleware, not in `next.config.js` redirects.
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
