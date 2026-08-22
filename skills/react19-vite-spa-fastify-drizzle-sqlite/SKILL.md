---
name: react19-vite-spa-fastify-drizzle-sqlite
description: >
  npm-workspaces monorepo reference for reddit-clone (embers): React 19 + Vite 7 SPA with HashRouter and vite-plugin-singlefile (single HTML deploy to GitHub Pages or S3), Tailwind CSS v4 CSS-first, Zustand overlay pattern, Fastify 5 composition-root buildApp, Drizzle ORM 0.36 + SQLite + better-sqlite3 + FTS5, Zod schemas at every boundary, JWT HS256 via jose + argon2id, pino logging, TypeScript 5.9 strict, ESLint 9 flat, Vitest and Playwright.
  Use when building a full-stack TypeScript monorepo, a deploy-anywhere static SPA with deterministic PRNG client data and a real Fastify backend, a community feed or forum with atomic voting and branded IDs, or when you need schema-versioned persistence, pure selectors, or SQLite online backup patterns.
version: 1.1.0
last_updated: 2026-08-19
---

# reddit-clone SKILL — Engineering Reference for Full-Stack TypeScript Monorepos

> **How to use this document:** This is the single-source-of-truth reference
> for the embers (Reddit-clone) codebase. It captures every design decision,
> anti-pattern, debugging procedure, and lesson learned across 15 remediation
> rounds. Any coding agent working on a similar tech stack (React SPA +
> Fastify API + Drizzle/SQLite + Zod + JWT auth) should read this before
> writing code.

---

## Table of Contents

1. [Project Identity & Design Philosophy](#1-project-identity--design-philosophy)
2. [Tech Stack & Environment](#2-tech-stack--environment)
3. [Bootstrapping & Configuration](#3-bootstrapping--configuration)
4. [The Design System (Code-First)](#4-the-design-system-code-first)
5. [Component Architecture & Patterns](#5-component-architecture--patterns)
6. [Custom Hooks & Context Deep Dive](#6-custom-hooks--context-deep-dive)
7. [Content Management & Data Layer](#7-content-management--data-layer)
8. [Accessibility (WCAG 2.2 AA) Implementation](#8-accessibility-wcag-22-aa-implementation)
9. [Anti-Patterns & Common Bugs](#9-anti-patterns--common-bugs)
10. [Debugging Guide](#10-debugging-guide)
11. [Pre-Ship Checklist](#11-pre-ship-checklist)
12. [Lessons Learnt & How to Avoid Them](#12-lessons-learnt--how-to-avoid-them)
13. [Pitfalls to Avoid](#13-pitfalls-to-avoid)
14. [Best Practices](#14-best-practices)
15. [Coding Patterns](#15-coding-patterns)
16. [Coding Anti-Patterns](#16-coding-anti-patterns)
17. [Monorepo & Build Configuration](#17-monorepo--build-configuration)
18. [Database Schema & Migrations](#18-database-schema--migrations)
19. [Security Architecture](#19-security-architecture)
20. [TypeScript Interface Reference](#20-typescript-interface-reference)
21. [Appendix: Round History & Audit Trail](#21-appendix-round-history--audit-trail)

---

## 1. Project Identity & Design Philosophy

**One-sentence description:** embers is a Reddit-style community feed that began as a client-only React SPA with deterministic PRNG-generated data and grew into a full-stack npm-workspaces monorepo with a Fastify REST API backend, Drizzle ORM + SQLite database, and JWT authentication.

**Design thesis:** "Deploy anywhere, scale when ready." The client SPA uses `HashRouter` + `vite-plugin-singlefile` to produce a single ~537 KB HTML file that works on GitHub Pages, S3, `python -m http.server`, or any static host — zero infrastructure required. The backend is additive, not replacement: the client works fully without it, and the API is wired in incrementally (auth first, feeds/search deferred).

**Non-negotiable rules:**
- The "deploy anywhere" static-hosting story is sacred — do NOT switch to `BrowserRouter` or remove `vite-plugin-singlefile` without explicit user confirmation (deferred as B17).
- Generated data is immutable — user mutations live in separate Zustand overlay slices, never in the `POSTS`/`USERS`/`COMMUNITIES` arrays.
- All API input/output is Zod-validated — no exceptions, no `any`, no hand-written types at the boundary.
- TDD for all logic changes — failing test first, then implementation, then verify green.
- Documentation stays in sync with code — AGENTS.md, CLAUDE.md, README.md, docs/Project-Architecture-Document.md are updated every round. (Round 15 F4 deleted the root `Project-Architecture-Document.md` duplicate — `docs/` is canonical per the README Documentation Map, enforced by `npm run test:plan-alignment`.)

**The anti-generic mandate:** This is not a tutorial project. Every architectural decision traces to a specific ADR (001–110). Do not add "popular" patterns (tRPC, pnpm, Turborepo, RS256, UUID PKs) — the project uses REST+Zod, npm-workspaces, HS256, and branded string IDs by explicit decision.

---

## 2. Tech Stack & Environment

| Layer | Technology | Version | Critical Note |
|---|---|---|---|
| UI Runtime | React | 19.2.6 | StrictMode + concurrent features |
| Build Tool | Vite | 7.3.2 | Native ESM, Rolldown bundler |
| Language | TypeScript | 5.9.3 | `strict: true`, `noUnusedLocals: true` |
| CSS | Tailwind CSS | 4.1.17 | CSS-first `@theme`, no config file |
| Routing | react-router-dom | 7.18.2 | `HashRouter` (NOT `BrowserRouter`) |
| State | zustand | 5.0.14 | `persist` middleware, schema-versioned |
| Animation | framer-motion | 13.x | `MotionConfig reducedMotion="user"` |
| Icons | lucide-react | 1.31.0 | Stroke-based, consistent |
| Single-file | vite-plugin-singlefile | 2.3.0 | Inlines all JS/CSS into one HTML |
| Backend | Fastify | 5.11.3 | Composition-root `buildApp()` pattern |
| ORM | drizzle-orm | 0.36.4 | Type-safe SQL, SQLite dialect |
| Database | better-sqlite3 | 13.0.3 | Synchronous, WAL mode, online backup |
| Auth JWT | jose | 5.10.0 | HS256 (symmetric), 15m access + 7d refresh |
| Password | argon2 | 0.41.1 | Argon2id (RFC 9106) |
| Validation | zod | 3.25.76 | All API boundaries, `*ResponseSchema` naming |
| Logging | pino | 9.14.0 | Structured JSON, redacted secrets |
| Test Runner | vitest | 2.1.9 | Per-workspace configs, `globals: true` |
| E2E | Playwright | 1.62.1 | 5 config variants (local/live/repro/local-prod) |
| Linter | ESLint | 9.39.5 | Flat config, `no-explicit-any: error` |
| CI | GitHub Actions | — | gitleaks → test → build → e2e |

**Verification:** Run `node -e "const p=require('./package.json'); console.log(p.devDependencies)"` and cross-check every version in this table against the actual `package.json`.

---

## 3. Bootstrapping & Configuration

### 3.1 Monorepo Structure

```
reddit-clone/
├── apps/
│   ├── web/          ← @embers/web — React 19 SPA (client)
│   └── server/       ← @embers/server — Fastify REST API (backend)
├── packages/
│   ├── shared/       ← @embers/shared — Zod schemas + branded IDs
│   └── db/           ← @embers/db — Drizzle ORM + SQLite + FTS5 + seed
├── docs/             ← All documentation (REMEDIATION_PLAN_*, session_*, audit_*)
├── e2e/              ← Playwright E2E specs
├── scripts/          ← CI verification scripts (verify-*.mjs, verify-*.sh)
├── Dockerfile        ← Multi-stage Node 20 bookworm-slim
├── docker-compose.yml
├── eslint.config.mjs ← ESLint 9 flat config
├── package.json      ← Root: workspaces, scripts, devDependencies
└── tsconfig.base.json ← Shared: strict, noUnusedLocals, noUnusedParameters
```

### 3.2 Key Configuration Files

| File | Purpose | Critical Setting |
|---|---|---|
| `tsconfig.base.json` | Shared TS config | `strict: true`, `noUnusedLocals: true`, `noUnusedParameters: true` |
| `apps/web/tsconfig.json` | Web client | `paths: { "@/*": ["src/*"] }` (alias exists but is unused) |
| `apps/web/vite.config.ts` | Vite build | `plugins: [react(), tailwindcss(), viteSingleFile()]` |
| `apps/server/src/config.ts` | Env loader | `loadEnv()` — zod-validated, refuses to start in prod without required vars |
| `packages/db/drizzle.config.ts` | Drizzle Kit | `dialect: "sqlite"`, `schema: "./src/schema/index.ts"` |
| `eslint.config.mjs` | Linter | `no-explicit-any: error`, `consistent-type-imports: error` |
| `playwright.config.ts` | E2E | `testIgnore: /live\.spec\.ts|repro_r10_postpage\.spec\.ts/` |

### 3.3 npm Scripts (Root)

```bash
npm run dev          # Start all workspaces in dev mode
npm run build        # Topological: shared → db → server → web
npm test             # Run vitest in all workspaces (pretest builds shared+db first)
npm run typecheck    # tsc --noEmit in all workspaces (pretypecheck builds shared+db)
npm run lint         # ESLint 9 flat config across the whole repo
npm run db:setup     # Migrate + seed the SQLite DB
npm run db:backup    # Back up the DB to ./backups/dev-<timestamp>.db (Round 13)
npm run test:e2e     # Playwright: 18 local tests (9 smoke + 9 auth)
npm run test:build   # Asserts dist/index.html has no Vite dev modules
npm run test:plan-alignment  # Asserts REMEDIATION_PLAN.md has no forbidden tokens
npm run test:no-secrets      # Asserts no .env / env.bak tracked
npm run test:gitignore       # Asserts no tracked file is gitignored
npm run test:ci-config       # Asserts gitleaks job in CI
```

### 3.4 Environment Variables

| Var | Required in Prod | Default | Notes |
|---|---|---|---|
| `NODE_ENV` | No | `development` | `production` triggers required-var enforcement |
| `PORT` | No | `4000` | Docker uses 4000; `server:start-prod` uses 5000 |
| `DATABASE_URL` | Yes (prod) | `./dev.db` | Resolved to repo-root by `loadEnv()`; `.env.example` overrides to `packages/db/dev.db` |
| `JWT_ACCESS_SECRET` | Yes (prod) | — | Min 32 chars; HS256 signing key |
| `JWT_REFRESH_SECRET` | Yes (prod) | — | Min 32 chars; refresh token signing key |
| `JWT_ACCESS_TTL` | No | `15m` | Access token expiry |
| `JWT_REFRESH_TTL` | No | `7d` | Refresh token expiry |
| `CORS_ORIGIN` | Yes (prod) | `*` | Comma-separated origins; `*` rejected in prod |
| `COOKIE_DOMAIN` | No | — | For cross-subdomain auth |
| `RATE_LIMIT_MAX` | No | `100` | Global rate limit per IP |
| `AUTH_RATE_LIMIT_MAX` | No | `5` | Per-IP auth endpoint limit (brute-force protection) |

---

## 4. The Design System (Code-First)

### 4.1 Tailwind v4 CSS-First Configuration

The project uses **Tailwind CSS v4** with the CSS-first `@theme` approach — no `tailwind.config.js` or `postcss.config.js` files exist. The `@theme` block in `apps/web/src/index.css` defines only the `--font-sans` token; the UI otherwise uses Tailwind's default `orange-*` / `zinc-*` palette (e.g. the global focus outline references `var(--color-orange-500)`).

```css
/* apps/web/src/index.css */
@import "tailwindcss";

@custom-variant dark (&:where(.dark, .dark *));

@theme {
  --font-sans: "Inter", ui-sans-serif, system-ui, -apple-system, sans-serif;
}

.line-clamp-1 { /* plain class — functional identical under @tailwindcss/vite; @utility is not used in this codebase */
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 1;
}
```

### 4.2 Theme Bootstrap

To prevent a flash of light theme before React hydrates, an inline `<script>` in `index.html` reads `localStorage` and applies the `dark` class before paint:

```html
<!-- apps/web/index.html -->
<script>
  (function() {
    try {
      var state = JSON.parse(localStorage.getItem('reddit-clone-state') || '{}');
      if (state.state?.theme === 'dark') {
        document.documentElement.classList.add('dark');
      }
    } catch (e) {}
  })();
</script>
```

### 4.3 Category Color Gradients

Avatars use `gradientFor(seed)` → 10 deterministic pairs via FNV-1a hash → mulberry32 PRNG (`apps/web/src/utils/random.ts:59` / `packages/db/src/seed/random.ts:59`) — client and server share the same hash so avatar gradients are identical. Communities do **not** use `gradientFor`; their `colorFrom`/`colorTo` are hard-coded in `SEEDS` (`apps/web/src/data/communities.ts:8-15`). (The `ImageCategory` type defines an 8th value, `nature`, but it appears only in the post-image `TITLE_BANK`/`CATEGORY_IMAGES` fallbacks and is never assigned to a community.)

---

## 5. Component Architecture & Patterns

### 5.1 The Composition-Root Pattern (`buildApp`)

The Fastify server uses a **composition-root** pattern: `buildApp()` is a pure function that takes optional dependencies and returns an unstarted `FastifyInstance`. This allows tests to `inject()` without binding a port.

```typescript
// apps/server/src/app.ts
export async function buildApp(opts: BuildAppOptions = {}): Promise<FastifyInstance> {
  const env = loadEnv(opts.env);
  const app = Fastify({ logger: { level: env.LOG_LEVEL, redact: { ... } } });

  // Plugin order MATTERS:
  // 1. helmet   — outermost, hardens all responses
  // 2. cors     — must precede routes so preflight works
  // 3. cookie   — auth refresh cookie parsing
  // 4. rateLimit — guards all routes
  // 5. requestId — assigns req.id before error handler uses it
  // 6. auth      — registers app.authenticate decorator
  // 7. routes    — health + (when db provided) all API routes
  // 8. static    — optional SPA (when STATIC_DIR set, wildcard:false, after routes; does not shadow /api/* or /health)
  // 9. errorHandler — last, wraps everything

  // Note: §5 lists 8 in earlier versions — Round 16 added `static` (apps/server/src/app.ts:195) via @fastify/static for same-origin SPA serving; CSP allows 'unsafe-inline' only when STATIC_DIR is set (ADR-003 tradeoff).

  if (opts.db && opts.rawDb) {
    // Lazy-import repositories + routes only when a DB is provided
    const { createUserRepository } = await import("./repositories/userRepository.js");
    // ... wire all deps ...
  }

  return app;
}
```

**Why this matters:** Tests can call `buildApp({ skipHelmet: true, skipRateLimit: true })` with an in-memory DB and `inject()` requests without network I/O.

### 5.2 The Overlay Pattern (Zustand)

Generated data (users, posts, communities, comments, notifications) is **immutable at runtime**. User mutations live in separate Zustand store slices and are merged at render time.

```typescript
// apps/web/src/store/store.ts
interface AppState {
  schemaVersion: number;
  theme: "light" | "dark";
  votes: Record<string, VoteValue>;           // overlay: post:<id> or comment:<id> → vote value
  joinedCommunityIds: string[];               // overlay: which communities the user joined
  savedPostIds: string[];                     // overlay: which posts the user saved
  localPosts: Post[];                         // overlay: posts created by the user
  localComments: Record<string, Comment[]>;    // overlay: comments created by the user
  notificationReadOverrides: Record<string, boolean>; // overlay: read state
  toasts: ToastMessage[];                      // ephemeral — NOT persisted
}
```

**Why this matters:** Adding a new user-mutable feature means adding a new overlay slice — never touching `USERS`, `POSTS`, or `COMMUNITIES`.

### 5.3 The Pure Selector Pattern

All derived state calculations are extracted into pure functions in `apps/web/src/store/selectors.ts` that take plain state slices as input — they do NOT call `useAppStore` themselves.

```typescript
// apps/web/src/store/selectors.ts
export function getVisibleScore(baseScore: number, vote: -1 | 0 | 1): number {
  return baseScore + vote;
}

export function getUnreadNotificationCount(
  notifications: readonly AppNotification[],
  readOverrides: Record<string, boolean>,
): number {
  let n = 0;
  for (const notif of notifications) {
    const read = readOverrides[notif.id] ?? notif.read;
    if (!read) n += 1;
  }
  return n;
}
```

**Why this matters:** Pure selectors are unit-testable without mocking zustand — just pass in arrays and records.

### 5.4 Client/Server Component Decision Tree

This project uses React 19 (not Next.js), so all components are client-side. However, the architecture separates:
- **Deterministic data layer** (`apps/web/src/data/*`) — generates all content at import time via PRNG
- **API client layer** (`apps/web/src/lib/api.ts`) — fetch-based, framework-agnostic, dependency-injected
- **Auth context layer** (`apps/web/src/auth/AuthProvider.tsx`) — React context + `useAuth()` hook

### 5.5 The `ErrorBoundary` Pattern

`ErrorBoundary` wraps `<Outlet />` in `AppShell` so route-level errors don't crash the entire app:

```tsx
// apps/web/src/components/layout/AppShell.tsx
<ErrorBoundary>
  <Outlet />
</ErrorBoundary>
```

---

## 6. Custom Hooks & Context Deep Dive

### 6.1 `useAuth()` — Auth Context Hook

```typescript
// apps/web/src/auth/AuthProvider.tsx
export interface AuthContextValue {
  user: AuthUser | null;
  status: AuthStatus;  // "anonymous" | "authenticated" | "loading"
  error: string | null;
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, password: string, displayName?: string) => Promise<AuthUser>;
  logout: () => Promise<void>;
}
```

**Critical implementation detail:** The access token is held in a `useRef` (not `useState`) to avoid re-renders on every token change. Only `user`/`status`/`error` trigger re-renders.

```typescript
const tokenRef = useRef<string | null>(null);
const getToken = useCallback(() => tokenRef.current, []);
const onTokenRefresh = useCallback((token: string) => { tokenRef.current = token; }, []);
```

### 6.2 `useAppStore()` — Zustand Store Hook

The store uses `persist` middleware with:
- **`partialize`** — whitelists only the 8 persisted fields (excludes `toasts`)
- **`mergePersistedState`** — safe-parse + validate + per-field drop (never throws)
- **`version` + `migrate`** — schema-versioned for future migrations

### 6.3 `useFocusTrap()` — Modal Accessibility Hook

Used by `Modal.tsx` to trap keyboard focus within the dialog while it's open, and restores focus to the trigger element on close. `Dropdown.tsx` does NOT use this hook — it implements its own Escape-to-close and ArrowUp/ArrowDown menu navigation via `useOnClickOutside` plus a keydown handler.

---

## 7. Content Management & Data Layer

### 7.1 Deterministic PRNG Data Layer (Client)

All client-side content is generated at import time in `apps/web/src/data/*`:
- `users.ts` — `generateUsers(48)` → 48 users with deterministic names, bios, karma, gradient colors
- `communities.ts` — `generateCommunities()` → 18 communities across 7 categories
- `posts.ts` — `generatePosts(320)` → 320 posts with titles, bodies, comment trees
- `notifications.ts` — 18 notifications
- `comments.ts` — per-post comment trees (total ~2881 in client PRNG vs ~3037 in DB seed — 5% demo parity gap due to RNG call order at `apps/web/src/data/comments.ts:40` vs `packages/db/src/seed/comments.ts:64`; DB is source of truth post-B16)

**Seed strings (reshuffling hazard):** `users-seed-v1`, `posts-seed-v2`, `notifications-seed-v1`, `community-${name}`, `comments-${postId}`. Changing any seed or the order of `rng()` calls reshuffles all downstream data.

### 7.2 Backend Database Layer (Server)

The backend mirrors the client's data using:
- `packages/db/src/schema/index.ts` — 7 Drizzle tables + 3 performance indexes
- `packages/db/src/fts5.ts` — FTS5 virtual table + sync triggers + `searchPosts()`
- `packages/db/src/seed/` — Ports the client PRNG into DB inserts via `runSeed()`
- `packages/db/scripts/seed.ts` — CLI: `npm run db:seed`

### 7.3 Accessor Contracts

| Function | On Found | On Not Found |
|---|---|---|
| `getPost(id)` | `Post` | `undefined` |
| `getCommunityByName(name)` | `Community` | `undefined` |
| `getCommunity(id)` | `Community` | **throws** (use `getCommunityByName` for safe lookups) |
| `getUser(id)` | `User` | Returns `CURRENT_USER` silently |

---

## 8. Accessibility (WCAG 2.2 AA) Implementation

- **Skip-to-content link:** `<a href="#main" className="skip-link">Skip to content</a>` in `AppShell`
- **Focus trap:** `useFocusTrap()` hook in `Modal.tsx` (the dialog). `Dropdown.tsx` implements its own Escape/arrow-key focus handling rather than using this hook.
- **Reduced motion:** `<MotionConfig reducedMotion="user">` wraps the entire app — respects browser's `prefers-reduced-motion`
- **Semantic HTML:** `<main id="main">`, `<nav>`, `<button>` (not `<div onClick>`)
- **Color contrast:** All category gradients meet WCAG AA 4.5:1 against white/black text
- **Touch targets:** All buttons are ≥44×44px on mobile

---

## 9. Anti-Patterns & Common Bugs

### AP-1: Using `BrowserRouter` instead of `HashRouter` (Critical)
- **Symptom:** Deep links break on static hosts (GitHub Pages, S3 without SPA fallback)
- **Root cause:** `BrowserRouter` requires server-side SPA fallback routing
- **Fix:** Use `HashRouter` — the `#/path` URLs work on any static host
- **Lesson:** The "deploy anywhere" story is sacred. Do NOT switch without explicit user confirmation (deferred as B17).

### AP-2: Using `React.lazy` or dynamic `import()` (Critical)
- **Symptom:** `vite-plugin-singlefile` fails to inline the dynamic chunk
- **Root cause:** Single-file build inlines all JS/CSS into one HTML; dynamic imports create separate chunks that can't be inlined
- **Fix:** No code-splitting. All components are eagerly imported.

### AP-3: Mutating generated data (High)
- **Symptom:** Reseeding orphans persisted votes/saves keyed to old IDs
- **Root cause:** Directly modifying `POSTS`, `USERS`, or `COMMUNITIES` arrays
- **Fix:** Use Zustand overlay slices (`votes`, `localPosts`, `localComments`) merged at render time

### AP-4: Reading `process.env` directly (High)
- **Symptom:** Tests fail because env vars aren't set; production starts with missing secrets
- **Root cause:** `process.env.SOME_VAR` bypasses validation and defaults
- **Fix:** Use `loadEnv()` (zod-validated) from `apps/server/src/config.ts`. **Bounded exception:** CLI entrypoints `packages/db/scripts/{backup,migrate,seed}.ts` read `process.env.DATABASE_URL` directly to avoid importing the full server config — acceptable at the process boundary.

### AP-5: Using `any` instead of `unknown` (Medium)
- **Symptom:** Type errors propagate silently; runtime crashes in production
- **Root cause:** `any` disables type checking
- **Fix:** Use `unknown` + type narrowing. ESLint `no-explicit-any: error` enforces this.

### AP-6: Claiming security controls that don't exist (Critical)
- **Symptom:** Documentation says "Double-submit cookie pattern for CSRF" but no such code exists
- **Root cause:** Aspirational documentation that was never implemented
- **Fix:** Document the ACTUAL posture: "Bearer tokens (not cookies) for state-changing API calls — inherently CSRF-resistant. Refresh cookie is `SameSite=Strict`."
- **Lesson:** Never document a security control that doesn't exist. Audit reports will find it. (Round 11, F1)

### AP-7: Mixing `*OutputSchema` and `*ResponseSchema` naming (Medium)
- **Symptom:** `loginOutputSchema` and `registerResponseSchema` coexist — inconsistent
- **Root cause:** Added a new schema with a different naming convention than existing ones
- **Fix:** Standardize on `*ResponseSchema` for all response-body schemas. `*InputSchema` for request bodies. `paginateOutputSchema()` retains its name (factory function, not a response schema). (Round 12, F5)

### AP-8: Committing `.env` files to git (Critical)
- **Symptom:** JWT secrets leak in git history
- **Root cause:** `.env` was tracked before `.gitignore` was added
- **Fix:** `git rm --cached .env` + add to `.gitignore` + **rotate all leaked secrets** + add `test:no-secrets` CI gate. (Round 9, R9.1 incident) **Bounded exception:** `skills/` is intentionally tracked (13,896 files) despite `.gitignore:skills/` — verifier `scripts/verify-gitignore-enforced.sh:12-20` excludes `^skills/` so the gate still passes; do not `git rm -r --cached skills/`.

### AP-9: Leaving stale `allowScripts` entries (Low)
- **Symptom:** `package.json` `allowScripts` lists `better-sqlite3@11.10.0` but the actual dep is `13.0.3`
- **Root cause:** Version upgrade without cleaning up the old entry
- **Fix:** Remove stale entries. (Round 12, F3)

### AP-10: Weakening guardrails to make gates pass (Critical)
- **Symptom:** ESLint rules disabled, type strictness loosened, tests skipped — all to make CI green
- **Root cause:** "Just make it pass" mentality
- **Fix:** Fix the underlying issue. A green gate achieved by weakening the gate is not a fix. State the debt explicitly. (Distilled Hard Lesson #5)

### AP-11: Renaming without checking blast radius (Medium)
- **Symptom:** Renaming a shared schema breaks downstream importers
- **Root cause:** Not grepping for all callers before renaming
- **Fix:** `grep -rn "oldName"` across the entire repo before any rename. (Round 12, F5 — verified zero downstream breakage)

### AP-12: Type assertions that don't actually fail (Medium)
- **Symptom:** `type _Check = AssertExact<T, U>` compiles even when types have drifted
- **Root cause:** TypeScript silently evaluates to `false` without erroring
- **Fix:** Add a constraint: `type AssertTrue<T extends true> = T; type _Check = AssertTrue<AssertExact<T, U>>;` — this FAILS the typecheck when types drift. (Round 13, F2)

### AP-13: Forgetting `--> statement-breakpoint` in Drizzle migrations (Medium)
- **Symptom:** `Database.prepare: supplied SQL string contains more than one statement`
- **Root cause:** Drizzle migrator requires `--> statement-breakpoint` between statements
- **Fix:** Add `--> statement-breakpoint` between each CREATE INDEX / CREATE TABLE in migration SQL files. (Round 11, F2)

### AP-14: Using `localStorage` for access tokens (Critical)
- **Symptom:** XSS attack steals access tokens from `localStorage`
- **Root cause:** Storing tokens in `localStorage` makes them accessible to any JS on the page
- **Fix:** Access token in `useRef` (JS memory, never `localStorage`). Refresh token in `HttpOnly`, `Secure`, `SameSite=Strict` cookie.

---

## 10. Debugging Guide

### DG-1: `git push` fails with "Permission denied (publickey)"
- **Cause:** SSH key not found, wrong format, or not registered on GitHub
- **Fix:** Use the `how-to-git-push-using-ssh-wrapper` skill; ensure paramiko is installed in the correct Python; chmod 600 the key file; use `StrictHostKeyChecking=accept-new`

### DG-2: `better-sqlite3` migration fails with "more than one statement"
- **Cause:** Missing `--> statement-breakpoint` in migration SQL
- **Fix:** Add `--> statement-breakpoint` between each statement. See `packages/db/src/migrations/0001_add_performance_indexes.sql` for the correct pattern.

### DG-3: Vitest discovers wrong test count
- **Cause:** Running `npx vitest run` from the repo root instead of via `npm test`
- **Fix:** Always use `npm test` (which triggers `pretest` to build shared+db first, then runs per-workspace vitest configs)

### DG-4: `test:plan-alignment` fails
- **Cause:** `docs/REMEDIATION_PLAN.md` contains forbidden tokens (tRPC, pnpm, Turborepo, RS256, UUID)
- **Fix:** Read `scripts/verify-plan-alignment.mjs` to see the forbidden list; update the plan to reflect the actual stack

### DG-5: ESLint reports `no-unused-vars` on type assertions
- **Cause:** `noUnusedLocals: true` flags unused type aliases
- **Fix:** Use `export type` instead of `type` — exported types are not flagged as unused. Type-only exports are erased at compile time (zero runtime cost).

### DG-6: `401 Unauthorized` loop on token refresh
- **Cause:** Refresh endpoint itself triggers a refresh, causing infinite recursion
- **Fix:** Pass `skipRefresh: true` to the internal `request()` call for the refresh endpoint. See `apps/web/src/lib/api.ts` line 280-284.

### DG-7: React `act()` warnings in tests
- **Cause:** Async state updates not wrapped in `act()`
- **Fix:** Use `await userEvent.setup()` (Testing Library) instead of `fireEvent` — it auto-wraps in `act()`. (Round 8 silenced 6 such warnings in LoginPage + RegisterPage tests)

### DG-8: `noUnusedLocals` blocks compile-time type drift detection
- **Cause:** `type _DriftCheck = AssertExact<T, U>` is flagged as unused
- **Fix:** Use `export type _DriftCheck = AssertTrue<AssertExact<T, U>>;` — the `export` avoids `noUnusedLocals`, and the `AssertTrue<T extends true>` constraint makes the typecheck actually FAIL on drift. (Round 13, F2)

---

## 11. Pre-Ship Checklist

### 11.1 Quality Gates (run in order)

```bash
npm run lint                    # 0 errors, 0 warnings
npm run typecheck               # all 4 workspaces clean (pretypecheck builds shared+db first)
npm test --workspaces --if-present  # 485 vitest tests pass
npm run test:plan-alignment     # REMEDIATION_PLAN.md has no forbidden tokens
npm run test:build              # dist/index.html is a valid production build (no Vite dev modules)
npm run test:no-secrets         # no .env / env.bak tracked
npm run test:gitignore          # no tracked file matches .gitignore
npm run test:ci-config          # gitleaks job present in CI
npm run test:e2e                # 18 local Playwright tests pass (9 smoke + 9 auth)
```

### 11.2 Security Checklist

- [ ] No secrets in `.env` / `.env.local` tracked by git (`test:no-secrets`)
- [ ] No hardcoded secrets in source code (`grep -rn "JWT_" apps/ packages/` should return only `config.ts` references)
- [ ] `loadEnv()` refuses to start in production without required vars
- [ ] All API input validated by Zod schemas (`registerInputSchema`, `loginInputSchema`, `createPostInputSchema`, etc.)
- [ ] All state-changing API routes use `preHandler: [app.authenticate]`
- [ ] Author-only routes return 403 (not 401) when caller is not the author
- [ ] Refresh cookie: `HttpOnly`, `Secure`, `SameSite=Strict`, `Path=/api/auth`
- [ ] Access token in `useRef` (never `localStorage`)
- [ ] `linkUrl` input rejects `javascript:` and `data:` schemes (XSS/SSRF prevention)
- [ ] Pino logger redacts `authorization`, `cookie`, `password`, `accessToken`, `refreshToken`

### 11.3 Documentation Checklist

- [ ] AGENTS.md test counts match actual test output
- [ ] CLAUDE.md commands match `package.json` scripts
- [ ] README.md file tree matches actual directory structure
- [ ] docs/Project-Architecture-Document.md "Last Updated" line reflects the latest round (root duplicate deleted in Round 15 F4)
- [ ] `docs/REMEDIATION_PLAN.md` checkboxes reflect actual completion status

---

## 12. Lessons Learnt & How to Avoid Them

### Lesson 1: Audit-driven development catches real bugs
- **What happened:** Round 11 audited `REMEDIATION_PLAN.md` against the codebase and found 9 findings (1 High, 2 Medium, 3 Low, 3 Informational). All were real — none were fabricated.
- **Why it mattered:** The fabricated CSRF "double-submit cookie" claim could have misled any reviewer relying on the plan. The missing indexes would have caused O(n) full scans at production scale. The missing `registerResponseSchema` broke the "single source of truth" property.
- **How to avoid:** Run a Mode-C audit (review existing code without fixing) before every major release. Validate every documentation claim against the actual source file at the exact line number.

### Lesson 2: TDD prevents regression
- **What happened:** Every code change in Rounds 11–13 followed RED → GREEN → REFACTOR. The failing test was written BEFORE the implementation. Zero regressions across 485 tests.
- **Why it mattered:** When the migration `0001_add_performance_indexes.sql` was first written without `--> statement-breakpoint`, the test caught it immediately (RED). When the schema rename in Round 12 was applied, the test suite confirmed zero downstream breakage in minutes.
- **How to avoid:** Never write implementation without a failing test first. Even for "trivial" changes like a rename — the test verifies the blast radius.

### Lesson 3: Pure functions are testable functions
- **What happened:** The Zustand selectors in `apps/web/src/store/selectors.ts` were extracted from ad-hoc `useAppStore` call sites into pure functions that take plain state slices as input. This made them unit-testable without mocking zustand.
- **Why it mattered:** 271 web tests (including selector tests) run in ~3 seconds with zero mocking infrastructure.
- **How to avoid:** If a function can be pure (no framework imports, no side effects), make it pure. Extract it into its own file with a co-located test.

### Lesson 4: Type-only imports are erased at compile time
- **What happened:** Round 13 added `@embers/shared` as a devDependency of `@embers/web` and used `import type { AuthUser as SharedAuthUser }` for compile-time drift detection. The production bundle was unaffected (525.3 KB before and after).
- **Why it mattered:** This allowed adding a type-safety bridge between the web client and the shared schemas WITHOUT coupling the runtime or bloating the bundle.
- **How to avoid:** Use `import type` for any import that's only needed at compile time (types, interfaces, type assertions). TypeScript erases them — zero runtime cost.

### Lesson 5: The `AssertTrue<T extends true>` constraint is essential
- **What happened:** Round 13's first attempt at type drift detection used `type _Check = AssertExact<T, U>` — but TypeScript silently evaluated to `false` without erroring when types drifted. The second attempt used `type AssertTrue<T extends true> = T; type _Check = AssertTrue<AssertExact<T, U>>` — this FAILS the typecheck when types drift.
- **Why it mattered:** Without the `extends true` constraint, the "drift detection" was a no-op — it never actually detected drift.
- **How to avoid:** When writing compile-time type assertions, always use a constraint pattern (`T extends true`) to force a typecheck failure on mismatch.

### Lesson 6: Repo hygiene is non-negotiable
- **What happened:** Round 12 untracked 13,926 `skills/` files that were committed despite the `.gitignore` rule. The `.gitignore` entry existed but was never enforced via `git rm --cached`.
- **Why it mattered:** 13,926 tracked files bloated the repo, slowed clones, and made `git status` noisy. (Note: the user later restored the skills/ folder — their decision, not a doc error.)
- **How to avoid:** After adding a directory to `.gitignore`, always run `git rm -r --cached <dir>` to untrack existing files. Adding to `.gitignore` alone does NOT untrack already-tracked files.

### Lesson 7: Never weaken a guardrail to make a gate pass
- **What happened:** Distilled from 40+ production monorepo remediation sessions — the most common failure is disabling ESLint rules, loosening type strictness, or skipping tests to make CI green.
- **Why it mattered:** A green gate achieved by weakening the gate is not a fix — it's hiding the problem.
- **How to avoid:** Fix the underlying issue. If you must suppress, state the debt explicitly with a justification comment. Never silently weaken.

### Lesson 8: The SSH wrapper is environment-dependent
- **What happened:** The `how-to-git-push-using-ssh-wrapper` skill requires paramiko installed in the correct Python (venv vs system). The `python3` on `PATH` may be a venv, while `pip` installs to system Python. Always verify with `python3 -c "import paramiko"`.
- **Why it mattered:** Push failures waste time and are confusing — "Permission denied (publickey)" or "Invalid key" errors are almost always paramiko-installation issues, not key issues.
- **How to avoid:** Follow the skill's verification steps: `python3 --version`, `python3 -c "import paramiko"`, `ls -la ~/.ssh/id_github` (mode 600), `chmod +x wrapper.py`.

### Lesson 9: Drizzle migrations need `--> statement-breakpoint`
- **What happened:** The first migration `0001_add_performance_indexes.sql` failed with "supplied SQL string contains more than one statement" because the 3 CREATE INDEX statements were separated by semicolons + blank lines but no Drizzle breakpoint markers.
- **Why it mattered:** The Drizzle migrator splits on `--> statement-breakpoint`, not on semicolons. Without the markers, the entire file is treated as one statement.
- **How to avoid:** Always use `--> statement-breakpoint` between statements in Drizzle migration SQL files. See the existing `0000_greedy_major_mapleleaf.sql` for the correct pattern.

### Lesson 10: Documentation is a living artifact
- **What happened:** Across 15 rounds, the docs (AGENTS.md, CLAUDE.md, README.md, docs/Project-Architecture-Document.md) were updated every single time code changed — test counts, file trees, commands, architecture notes.
- **Why it mattered:** The `docs/ALIGNMENT_REVIEW.md` audit found only 6 minor doc-precision issues out of 24 verification areas. The docs are exceptionally well-aligned because they're treated as code.
- **How to avoid:** After every code change, update the docs in the same commit. Test counts, file paths, commands, and architecture descriptions must match the code. Run `npm run test:plan-alignment` as a CI gate.

### Lesson 11: Open-redirect guards on `state.from`
- **What happened:** Round 15 F1 wired up `LoginPage` to redirect back to `location.state?.from` after login (deferred since Round 7). The `<RequireAuth>` preserves the original destination, but if a hostile link lands the user on `/login` with crafted `state.from = "https://evil.example.com"`, react-router would issue a full-page navigation. The fix: `validateFromPath()` rejects anything that doesn't start with `/`, plus rejects `//` (protocol-relative) and `/\` (some browsers normalize backslashes).
- **Why it mattered:** Without the guard, an attacker could redirect users to phishing sites after they log in to a legitimate embers instance.
- **How to avoid:** Always validate redirect destinations against an allowlist pattern (e.g., `^/[^/\\]`). Never `navigate(userSuppliedString)` directly. Test the guard explicitly.

### Lesson 12: Normalize network errors before they reach the UI
- **What happened:** Round 15 F2 caught a UX gap surfaced by the live E2E audit: when the backend is unreachable, `fetch` throws `TypeError("Failed to fetch")`. This raw browser error propagated up through `request → api.* → auth.* → LoginPage` and the user saw "Failed to fetch" in the `role=alert` div — meaningless to a non-engineer. The fix: wrap `fetchFn` in try/catch, throw `ApiError(0, "NETWORK_ERROR", "Could not reach the embers server. Please try again later.", undefined, cause)`. Preserve the original error via `Error.cause` (ES2022) for diagnostics.
- **Why it mattered:** The error message is the only feedback the user gets when the backend is down. A friendly message tells them what happened and what to do next.
- **How to avoid:** Any client-side `fetch` call should be wrapped in a normalizer that produces a domain-specific error type. Never let raw `TypeError` from `fetch` reach the UI layer.

### Lesson 13: Strict gates vs informational audits
- **What happened:** Round 8 added `e2e/live.spec.ts` and `e2e/live_extended.spec.ts` to document the LIVE-CRIT-2/3/4 deployment gaps. The tests intentionally did NOT fail — they `console.log`'d the gaps so CI stayed green. As of Round 15 (2026-08-19) the gaps were STILL present, and there was still no gate that failed. Round 15 F3 added `scripts/verify-prod-readiness.mjs` as a separate strict gate (exits 1 on failure) that operators opt into via `npm run test:prod-readiness`.
- **Why it mattered:** Informational audits document gaps; strict gates enforce them. Mixing the two creates ambiguity — operators don't know whether a green CI means "all good" or "all known gaps are documented but still present".
- **How to avoid:** Keep informational audits (console.log) and strict gates (exit 1) as separate scripts with separate npm commands. Operators opt into strict gates when they're ready to block releases on the gaps.

---

## 13. Pitfalls to Avoid

### P-1: Don't use `BrowserRouter`
- **Don't:** `<BrowserRouter>` — requires server-side SPA fallback routing
- **Do:** `<HashRouter>` — `#/path` URLs work on any static host

### P-2: Don't use `React.lazy` or dynamic `import()`
- **Don't:** `const Component = React.lazy(() => import("./Component"))`
- **Do:** `import Component from "./Component"` — eager imports only (viteSingleFile inlines everything)

### P-3: Don't mutate generated data
- **Don't:** `POSTS[0].upvotes += 1` — breaks determinism
- **Do:** `useAppStore.getState().setVote("post:p1", 1)` — overlay slice merged at render time

### P-4: Don't read `process.env` directly
- **Don't:** `const port = process.env.PORT || 4000`
- **Do:** `const env = loadEnv(); const port = env.PORT;` — zod-validated, production-safe

### P-5: Don't use `any`
- **Don't:** `function parse(data: any) { return JSON.parse(data) }`
- **Do:** `function parse(data: unknown) { return JSON.parse(data as string) }` — or better, use Zod

### P-6: Don't use default exports
- **Don't:** `export default function App() { ... }`
- **Do:** `export function App() { ... }` — named exports only (enforced by convention)

### P-7: Don't hand-edit `package.json` or lockfiles
- **Don't:** Manually adding `"axios": "^1.0.0"` to `package.json`
- **Do:** `npm install axios` — let the package manager update the lockfile

### P-8: Don't use `Path=/api/auth/refresh` for the refresh cookie
- **Don't:** `path: "/api/auth/refresh"` — logout can't read the cookie
- **Do:** `path: "/api/auth"` — covers both `/api/auth/refresh` and `/api/auth/logout`

### P-9: Don't claim security controls that don't exist
- **Don't:** "Double-submit cookie pattern for CSRF" (when no such code exists)
- **Do:** "Bearer tokens (not cookies) for state-changing API calls — inherently CSRF-resistant. Refresh cookie is `SameSite=Strict`."

### P-10: Don't mix `*OutputSchema` and `*ResponseSchema` naming
- **Don't:** `loginOutputSchema` + `registerResponseSchema` — inconsistent
- **Do:** `loginResponseSchema` + `registerResponseSchema` — standardize on `*ResponseSchema`

### P-11: Don't use `localStorage` for access tokens
- **Don't:** `localStorage.setItem("accessToken", token)` — XSS can steal it
- **Do:** `tokenRef.current = token` — JS memory via `useRef`, never `localStorage`

### P-12: Don't use `rs256` or UUID primary keys
- **Don't:** `SignJWT.setProtectedHeader({ alg: "RS256" })` or `id: uuid()`
- **Do:** `alg: "HS256"` (symmetric, simpler) and branded string IDs (`u-<uuid>`, `p-<uuid>`)

### P-13: Don't skip the `pretest` / `pretypecheck` hooks
- **Don't:** `npx vitest run` from the repo root (won't find workspace configs)
- **Do:** `npm test` or `npm run typecheck` (triggers `pretest`/`pretypecheck` which builds shared+db first)

### P-14: Don't write migrations without `--> statement-breakpoint`
- **Don't:** `CREATE INDEX a; CREATE INDEX b;` (Drizzle treats as one statement)
- **Do:** `CREATE INDEX a; --> statement-breakpoint CREATE INDEX b;`

---

## 14. Best Practices

### BP-1: Composition Root Pattern
Use a `buildApp()` function that takes optional dependencies and returns an unstarted server instance. Tests inject mock deps and call `inject()` without binding a port.

### BP-2: Zod at Every API Boundary
Every request body, query string, and response body is validated by a Zod schema in `@embers/shared`. The Fastify route handler uses `schema.safeParse(req.body)` and throws on failure.

### BP-3: Schema-Versioned Persistence
The Zustand store uses `persist` middleware with `SCHEMA_VERSION`, `validatePersistedState` (per-field drop, not all-or-nothing), and `mergePersistedState` (never throws). This survives corrupt localStorage, missing fields, and schema migrations.

### BP-4: Pure Selectors
Extract derived-state calculations into pure functions in `selectors.ts` that take plain slices as input. They're unit-testable without mocking zustand.

### BP-5: Plugin Order Matters
Fastify plugin registration order is load-bearing: `helmet → cors → cookie → rateLimit → requestId → auth → routes → errorHandler`. Reordering breaks header injection, cookie parsing, rate limiting, and error correlation.

### BP-6: Token in `useRef`, Not `useState`
The access token is stored in a `useRef` to avoid re-renders on every token change. Only `user`/`status`/`error` trigger re-renders. The `getToken` accessor is stable across renders.

### BP-7: 401 Refresh-and-Retry with Recursive Guard
The API client's `request()` function checks for 401, calls `refresh()` with `skipRefresh: true` (to prevent infinite recursion), and retries the original request once with the new token.

### BP-8: Compile-Time Type Drift Detection
Use `AssertExact<T, U>` + `AssertTrue<T extends true>` with type-only imports to enforce that the web client's hand-written interfaces stay structurally identical to the shared Zod schemas. Zero runtime cost (type-only imports are erased).

### BP-9: SQLite Online Backup
Use `better-sqlite3`'s `.backup()` method for safe online backups. It uses SQLite's backup API — page-level copy with coordinated read locks, never blocking writers for more than a single page copy.

### BP-10: TDD RED → GREEN → REFACTOR
Write the failing test first. Implement the minimum code to pass. Refactor. Verify the full suite still passes. This prevents regressions and documents the intent.

### BP-11: Audit-Driven Remediation
Run a Mode-C audit (review without fixing) against the codebase periodically. Validate every documentation claim at the exact line number. Classify findings by severity. Fix root causes, not symptoms.

### BP-12: CI Gates as Guardrails
8 CI gates: lint, typecheck, test, `test:plan-alignment`, `test:build`, `test:no-secrets`, `test:gitignore`, `test:ci-config`. Each catches a specific class of regression. Never weaken a gate to make it pass.

### BP-13: ESLint 9 Flat Config
Use ESLint 9's flat config (`eslint.config.mjs`) with `no-explicit-any: error`, `consistent-type-imports: error`, `exhaustive-deps: error`. No Prettier — ESLint's `--fix` is the project's formatter.

### BP-14: Branded IDs
Use nominal-typed branded IDs (`UserId`, `PostId`, `CommentId`, `CommunityId`, `NotificationId`) to prevent accidental cross-assignment at compile time. The `asUserId()` / `asPostId()` constructors are the only sanctioned way to lift a raw string.

---

## 15. Coding Patterns

### CP-1: Composition Root (Fastify)

```typescript
// apps/server/src/app.ts
export async function buildApp(opts: BuildAppOptions = {}): Promise<FastifyInstance> {
  const env = loadEnv(opts.env);
  const app = Fastify({ logger: { level: env.LOG_LEVEL, redact: { paths: [...], censor: "[REDACTED]" } } });

  // Plugin order: helmet → cors → cookie → rateLimit → requestId → auth → routes → errorHandler
  if (!opts.skipHelmet) await app.register(helmet, { contentSecurityPolicy: { directives: { ... } } });
  await app.register(cors, { origin: env.CORS_ORIGIN === "*" ? true : env.CORS_ORIGIN.split(","), credentials: true });
  await app.register(cookie, { secret: env.JWT_REFRESH_SECRET ?? "dev-cookie-secret" });
  if (!opts.skipRateLimit && env.NODE_ENV !== "test") await app.register(rateLimit, { max: env.RATE_LIMIT_MAX, timeWindow: env.RATE_LIMIT_WINDOW });
  await app.register(requestIdPlugin);
  await app.register(authPlugin);
  await app.register(healthRoutes);

  if (opts.db && opts.rawDb) {
    // Lazy-import + wire repositories + routes
    const userRepo = createUserRepository(opts.db);
    // ...
    await app.register(buildAuthRoutes({ userRepo, sessionRepo, env: authEnv }));
    await app.register(buildPostRoutes({ postRepo, communityRepo }));
    // ...
  }

  await app.register(errorHandlerPlugin);
  app.decorate("env", env);
  return app;
}
```

### CP-2: 401 Refresh-and-Retry (API Client)

```typescript
// apps/web/src/lib/api.ts
async function request<T>(method: string, path: string, body?: unknown, opts: { skipRefresh?: boolean } = {}): Promise<T> {
  const res = await fetchFn(url, { method, headers, body: JSON.stringify(body) });
  if (!res.ok) {
    if (res.status === 401 && tryRefreshOn401 && !opts.skipRefresh && token !== null) {
      try {
        const refreshResult = await request<LoginResponse>("POST", "/api/auth/refresh", undefined, { skipRefresh: true });
        if (onTokenRefresh) onTokenRefresh(refreshResult.accessToken);
        // Retry original request with new token...
      } catch {
        // Refresh failed — propagate the ORIGINAL 401
      }
    }
    throw new ApiError(res.status, code, message, requestId);
  }
  return res.status === 204 ? undefined as T : await res.json() as T;
}
```

### CP-3: Type Drift Detection

```typescript
// apps/web/src/lib/api.ts
import type { AuthUser as SharedAuthUser } from "@embers/shared";

type AssertExact<T, U> =
  (<G>() => G extends T ? 1 : 2) extends
  (<G>() => G extends U ? 1 : 2) ? true : false;

type AssertTrue<T extends true> = T;
export type _DriftCheckAuthUser = AssertTrue<AssertExact<AuthUser, SharedAuthUser>>;
// If types drift, typecheck FAILS: "Type 'false' does not satisfy the constraint 'true'"
```

### CP-4: Schema-Versioned Persistence

```typescript
// apps/web/src/store/storage.ts
export const SCHEMA_VERSION = 1;
export const PERSISTED_FIELDS = ["schemaVersion", "theme", "votes", "joinedCommunityIds", "savedPostIds", "localPosts", "localComments", "notificationReadOverrides"] as const;

export function validatePersistedState(input: unknown): PersistedState {
  if (!isObject(input)) return { ...DEFAULT_PERSISTED_STATE };
  const candidate = isObject(input.state) ? input.state : input;
  const result: PersistedState = { ...DEFAULT_PERSISTED_STATE };
  if (candidate.theme === "light" || candidate.theme === "dark") result.theme = candidate.theme;
  if (isObject(candidate.votes)) result.votes = sanitizeVoteRecord(candidate.votes);
  // ... per-field validation, drop invalid entries individually
  result.schemaVersion = SCHEMA_VERSION;
  return result;
}
```

### CP-5: Atomic Vote Service

```typescript
// apps/server/src/services/voteService.ts
export function createVoteService(db: DrizzleDB, deps: { voteRepo, postRepo, commentRepo }) {
  return {
    castVote(input: CastVoteInput): CastVoteResult {
      return db.transaction(() => {
        const existing = deps.voteRepo.find(input.userId, input.targetId, input.targetType);
        // Case 1: no prior vote → insert + increment
        // Case 2: same value → toggle off (delete + decrement)
        // Case 3: opposite value → flip (update + decrement old + increment new)
        // All counter updates use atomic SQL: UPDATE posts SET upvotes = upvotes + 1
      });
    }
  };
}
```

### CP-6: SQLite Online Backup

```typescript
// packages/db/src/client.ts
export async function backupDb(sourcePath: string, destinationPath: string): Promise<BackupResult> {
  const { raw } = openDb({ path: sourcePath, skipMigrate: true, skipFts5: true });
  try {
    const meta = await raw.backup(destinationPath);
    return { totalPages: meta.totalPages, remainingPages: meta.remainingPages, destination: destinationPath };
  } finally {
    raw.close();
  }
}
```

### CP-7: FTS5 External-Content Pattern

```sql
-- packages/db/src/fts5.ts
CREATE VIRTUAL TABLE IF NOT EXISTS posts_fts USING fts5(
  title, body, content='posts', content_rowid='rowid'
);
CREATE TRIGGER posts_ai AFTER INSERT ON posts BEGIN ... END;
CREATE TRIGGER posts_ad AFTER DELETE ON posts BEGIN ... END;
CREATE TRIGGER posts_au AFTER UPDATE ON posts BEGIN ... END;
```

### CP-8: Refresh Token Rotation

```typescript
// apps/server/src/routes/auth.ts
app.post("/api/auth/refresh", async (req, reply) => {
  const payload = await verifyRefreshToken(token, env.JWT_REFRESH_SECRET!);
  // Atomic rotation: revoke old jti, issue new jti
  const newJtiValue = newJti();
  const rotated = sessionRepo.rotate(payload.jti, newJtiValue, payload.id, newExpiresAt);
  if (!rotated) return reply.code(401).send({ error: { code: "UNAUTHORIZED", message: "Refresh token has been revoked" } });
  const accessToken = await signAccessToken({ id: user.id, username: user.username }, env.JWT_ACCESS_SECRET!, env.JWT_ACCESS_TTL);
  const newRefreshToken = await signRefreshToken({ id: user.id, jti: newJtiValue }, env.JWT_REFRESH_SECRET!, env.JWT_REFRESH_TTL);
  setRefreshCookie(reply, newRefreshToken, env);
  return reply.send({ accessToken, user: toAuthUser(user) });
});
```

---

## 16. Coding Anti-Patterns

### CAP-1: `any` vs `unknown`
```typescript
// DON'T
function parse(data: any) { return data.foo; }
// DO
function parse(data: unknown) { return (data as { foo: string }).foo; }
```

### CAP-2: Default exports
```typescript
// DON'T
export default function App() { ... }
// DO
export function App() { ... }
```

### CAP-3: `process.env` directly
```typescript
// DON'T
const port = process.env.PORT || 4000;
// DO
const env = loadEnv(); const port = env.PORT;
```

### CAP-4: Mutating generated data
```typescript
// DON'T
POSTS[0].upvotes += 1;
// DO
useAppStore.getState().setVote("post:p1", 1);
```

### CAP-5: `localStorage` for tokens
```typescript
// DON'T
localStorage.setItem("accessToken", token);
// DO
tokenRef.current = token; // useRef, JS memory only
```

### CAP-6: Missing `--> statement-breakpoint`
```sql
-- DON'T
CREATE INDEX a ON posts (community_id);
CREATE INDEX b ON comments (post_id);
-- DO
CREATE INDEX a ON posts (community_id);
--> statement-breakpoint
CREATE INDEX b ON comments (post_id);
```

### CAP-7: Silent type assertions
```typescript
// DON'T (silently evaluates to false, no error)
type _Check = AssertExact<T, U>;
// DO (fails typecheck when types drift)
type AssertTrue<T extends true> = T;
type _Check = AssertTrue<AssertExact<T, U>>;
```

---

## 17. Monorepo & Build Configuration

### 17.1 npm Workspaces

```json
// Root package.json
{
  "workspaces": ["apps/*", "packages/*"],
  "scripts": {
    "build": "npm run build --workspace @embers/shared && npm run build --workspace @embers/db && npm run build --workspace @embers/server && npm run build --workspace @embers/web",
    "pretest": "npm run build --workspace @embers/shared && npm run build --workspace @embers/db",
    "pretypecheck": "npm run build --workspace @embers/shared && npm run build --workspace @embers/db"
  }
}
```

### 17.2 Build Order (Topological)

`@embers/shared` → `@embers/db` → `@embers/server` → `@embers/web`

The `pretest` and `pretypecheck` hooks build `shared` + `db` first because:
- Server tests import from `@embers/shared` and `@embers/db`
- Web typecheck imports from `@embers/shared` (devDependency, type-only)

### 17.3 Docker (Multi-Stage)

```dockerfile
# Stage 1: builder
FROM node:20-bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends python3 make g++ && rm -rf /var/lib/apt/lists/*
COPY package.json package-lock.json* ./
COPY apps/server/package.json apps/server/
# ... copy all workspace package.jsons
RUN npm ci --no-audit --no-fund
COPY . .
RUN npm run build
RUN npm prune --omit=dev

# Stage 2: runner
FROM node:20-bookworm-slim AS runner
COPY --from=builder /app/node_modules /app/node_modules
COPY --from=builder /app/apps/server/dist /app/apps/server/dist
COPY --from=builder /app/apps/web/dist /app/apps/web/dist
ENV STATIC_DIR=/app/apps/web/dist
CMD ["node", "apps/server/dist/index.js"]
# Note: web dist copy + STATIC_DIR added in Round 15 for unified origin (Fastify serves / + /api/* + /health from one process).
```

---

## 18. Database Schema & Migrations

### 18.1 Tables (7 + FTS5 virtual table)

| Table | Key Columns | Indexes |
|---|---|---|
| `users` | `id` (PK), `username` (UNIQUE), `password_hash`, `display_name`, `bio`, `karma`, `created_at`, `color_from`, `color_to` | UNIQUE(username) implicit |
| `communities` | `id` (PK), `slug` (UNIQUE), `name`, `title`, `description`, `owner_id` (FK), `member_count`, `online_count`, `category`, `color_from`, `color_to`, `icon`, `rules` (JSON) | UNIQUE(slug) implicit |
| `posts` | `id` (PK), `community_id` (FK), `author_id` (FK), `title`, `type`, `body`, `link_url`, `link_domain`, `image_category`, `flair`, `upvotes`, `downvotes`, `comment_count`, `created_at` | `idx_posts_community_created` (community_id, created_at DESC) |
| `comments` | `id` (PK), `post_id` (FK), `author_id` (FK), `parent_id` (self-ref), `body`, `upvotes`, `downvotes`, `depth`, `created_at` | `idx_comments_post_id` (post_id) |
| `votes` | `user_id` (FK), `target_id`, `target_type`, `value` | Composite PK (user_id, target_id, target_type) |
| `notifications` | `id` (PK), `user_id` (FK), `type`, `message`, `detail`, `post_id`, `actor_id` (FK), `read`, `created_at` | `idx_notifications_user_read` (user_id, read) |
| `sessions` | `jti` (PK), `user_id` (FK), `expires_at`, `created_at`, `revoked_at` | PK(jti) implicit |
| `posts_fts` | Virtual table (FTS5), external-content pattern | — |

### 18.2 SQLite Hardening

```typescript
// packages/db/src/client.ts
raw.pragma("foreign_keys=ON");
if (!opts.skipWal && !isMemory) {
  raw.pragma("journal_mode=WAL");
  raw.pragma("busy_timeout=5000");
  raw.pragma("synchronous=NORMAL");
}
```

### 18.3 Migration Pattern

```sql
-- packages/db/src/migrations/0001_add_performance_indexes.sql
CREATE INDEX IF NOT EXISTS `idx_posts_community_created` ON `posts` (`community_id`, `created_at` DESC);
--> statement-breakpoint
CREATE INDEX IF NOT EXISTS `idx_comments_post_id` ON `comments` (`post_id`);
--> statement-breakpoint
CREATE INDEX IF NOT EXISTS `idx_notifications_user_read` ON `notifications` (`user_id`, `read`);
```

**Migration journal:** `packages/db/src/migrations/meta/_journal.json` tracks applied migrations. Each entry has `idx`, `version`, `when`, `tag`, `breakpoints`.

---

## 19. Security Architecture

### 19.1 Authentication Flow

1. **Register:** `POST /api/auth/register` → 201 `{ user }` (no session, no tokens)
2. **Login:** `POST /api/auth/login` → 200 `{ accessToken, user }` + Set-Cookie `embers_refresh` (HttpOnly, Secure, SameSite=Strict, Path=/api/auth, 7d)
3. **Refresh:** `POST /api/auth/refresh` → 200 `{ accessToken, user }` + rotated refresh cookie. Old jti revoked, new jti issued.
4. **Logout:** `POST /api/auth/logout` → 204. Revokes the jti, clears the cookie. Idempotent.

### 19.2 JWT Configuration

| Property | Access Token | Refresh Token |
|---|---|---|
| Algorithm | HS256 (jose) | HS256 (jose) |
| TTL | 15m | 7d |
| Stored in | JS memory (`useRef`) | `HttpOnly` cookie |
| Contains | `{ id, username }` | `{ id, jti }` |
| Revocation | N/A (short-lived) | `sessions.revokedAt` |

### 19.3 Password Hashing

```typescript
// apps/server/src/auth/password.ts
export async function hashPassword(plain: string): Promise<string> {
  return argon2.hash(plain, { type: argon2.argon2id });
}
```

Argon2id defaults: `timeCost: 3`, `memoryCost: 4096 KiB (4 MB)`, `parallelism: 1`.

### 19.4 CSRF Posture

State-changing API calls use `Authorization: Bearer` tokens (not cookies), which are not sent cross-origin and are therefore inherently CSRF-resistant. The refresh cookie is `SameSite=Strict` and scoped to `Path=/api/auth`. No double-submit cookie pattern is implemented or needed given the Bearer-token architecture.

### 19.5 Rate Limiting

- Global: 100 requests per minute per IP
- Auth endpoints (`/api/auth/register`, `/api/auth/login`): 5 requests per minute per IP (brute-force protection)
- 429 response body: `{ error: { code: "RATE_LIMITED", message: "Rate limit exceeded. Retry after 1 minute." } }`

### 19.6 Pino Logger Redaction

```typescript
// apps/server/src/app.ts
logger: {
  redact: {
    paths: [
      "req.headers.authorization",
      "req.headers.cookie",
      "req.body.password",
      "res.body.accessToken",
      "res.body.refreshToken",
    ],
    censor: "[REDACTED]",
  },
}
```

---

## 20. TypeScript Interface Reference

### 20.1 Shared Schemas (`@embers/shared`)

```typescript
// packages/shared/src/ids.ts
export type UserId = string & Brand<"UserId">;
export type CommunityId = string & Brand<"CommunityId">;
export type PostId = string & Brand<"PostId">;
export type CommentId = string & Brand<"CommentId">;
export type NotificationId = string & Brand<"NotificationId">;

// packages/shared/src/api/index.ts
export interface AuthUser {
  id: string; username: string; displayName: string; bio: string;
  karma: number; createdAt: string; colorFrom: string; colorTo: string;
}

export interface LoginResponse { accessToken: string; user: AuthUser; }
export interface RegisterResponse { user: AuthUser; }
export interface RefreshTokenResponse { accessToken: string; user: AuthUser; }
export interface CastVoteResponse { targetId: string; targetType: "post" | "comment"; value: -1 | 0 | 1; score: number; }
export interface ErrorResponse { error: { code: string; message: string; details?: unknown; requestId?: string; }; }
```

### 20.2 Web Client Types (`apps/web/src/lib/api.ts`)

The web client has hand-written interfaces that mirror the shared schemas. Compile-time `AssertExact` assertions enforce they stay in sync (Round 13, F2).

```typescript
export interface AuthUser { id: string; username: string; displayName: string; bio: string; karma: number; createdAt: string; colorFrom: string; colorTo: string; }
export interface LoginResponse { accessToken: string; user: AuthUser; }
export interface RegisterResponse { user: AuthUser; }
export class ApiError extends Error { readonly status: number; readonly code: string; readonly requestId?: string; }
```

### 20.3 Server Config (`apps/server/src/config.ts`)

```typescript
export interface Env {
  NODE_ENV: "development" | "production" | "test";
  PORT: number; HOST: string; LOG_LEVEL?: string;
  DATABASE_URL: string;
  JWT_ACCESS_SECRET?: string; JWT_REFRESH_SECRET?: string;
  JWT_ACCESS_TTL: string; JWT_REFRESH_TTL: string;
  COOKIE_DOMAIN?: string; CORS_ORIGIN: string;
  RATE_LIMIT_MAX: number; RATE_LIMIT_WINDOW: string;
  AUTH_RATE_LIMIT_MAX: number; AUTH_RATE_LIMIT_WINDOW: string;
}
```

---

## 21. Appendix: Round History & Audit Trail

| Round | Date | Summary | Tests | Key Changes |
|---|---|---|---|---|
| 1–3 | 2026-08-09/10 | Monorepo transition, server scaffolding, DB schema, FTS5, auth, CRUD routes | ~300 | B0–B16 done |
| 4 | 2026-08-10 | ESLint 9 flat config added | ~350 | Phase 1.4 |
| 5 | 2026-08-10 | Doc-alignment + `lib/api.ts` foundational client | ~350 | B17–B22 TDD breakdown |
| 6–7 | 2026-08-10 | B18 Auth Provider (AuthProvider, LoginPage, RegisterPage, RequireAuth, 401 refresh) | 453 | B18 done (R6=428 → R7=453 after +25 web tests) |
| 8 | 2026-08-10 | Live-deployment audit + hardening (test:build, test:fresh-clone, live E2E) | 453 | 3 critical deployment gaps (no test-count change) |
| 9 | 2026-08-10 | Secret rotation (.env committed to git history) | 453 | R9.1 incident + 6 CI gates (zero tests added) |
| 10 | 2026-08-10 | Comprehensive audit-driven remediation (4 bugs, 7 drift points) | 462 | BUG-R10-2 through R10-5 |
| 11 | 2026-08-12 | Audit-driven doc + schema reconciliation (9 findings) | 466 | F1–F9 (CSRF, indexes, registerResponseSchema, cookie path, ID strategy, Postgres FTS5, route count, checkboxes, Prettier) |
| 12 | 2026-08-13 | Hygiene + schema-naming reconciliation (6 findings) | 466 | F1–F6 (DATABASE_URL doc, stale allowScripts, untrack skills/, schema rename, stray file deletion) |
| 13 | 2026-08-13 | Self-scoped infrastructure + type-safety (3 deliverables) | 467 | F1 (backupDb), F2 (type drift detection), F3 (14 checkboxes ticked) |
| 14 | 2026-08-18 | Knowledge distillation — distilled 13 rounds into reddit-clone_SKILL.md | 467 | No code changes; 21-section SKILL.md created |
| 15 | 2026-08-19 | Live-audit-driven codebase + doc remediation (6 findings) | 473 vitest + 14 `node --test` | F1 (LoginPage `state.from`), F2 (NETWORK_ERROR), F3 (prod-readiness gate), F4 (PAD reconciliation), F5 (worklog backfill), F6 (Sentry annotation) |
| 16 | 2026-08-19 | Live-E2E + production-origin remediations (9 items) | 485 vitest + 14 `node --test` | R15.1 same-origin + R15.2 STATIC_DIR + R15.3 CSP unsafe-inline + R15.4 LoginPage state.from + R15.5 register link + R15.6 favicon + R15.7 unified start/Docker + R15.8 _headers + R15.9 doc alignment |

### Audit Reports

| File | Scope | Verdict |
|---|---|---|
| `docs/audit_report_1.md` | REMEDIATION_PLAN.md vs codebase | Highly aligned |
| `docs/audit_report_2.md` | 5-Phase ToDo list vs B0–B24 backlog | 11 checkboxes needed ticking |
| `docs/audit_report_3.md` | REMEDIATION_PLAN.md vs codebase | Strictly aligned, 0 contradictions |
| `docs/audit_report_4.md` | REMEDIATION_PLAN.md vs codebase | Exceptional alignment |
| `docs/ALIGNMENT_REVIEW.md` | AGENTS/CLAUDE/README vs codebase | 24 PASS + 6 minor (all resolved) |
| `docs/session_11.md` | Mode-C audit of REMEDIATION_PLAN.md | 9 findings (all remediated in R11) |
| `docs/session_12.md` | Mode-C alignment audit + R11 re-validation | 6 findings (all remediated in R12) |
| `docs/session_13.md` | Round 12 + 13 worklog | Accurate, faithful to codebase |
| `docs/session_14.md` | Review of session_13.md | 5 discrepancies (all post-doc, none are doc errors) |

### Skills Referenced (from `skills/skills-catalog.md`)

- `planning-and-task-breakdown` — structured ToDo lists for every round
- `tdd-workflow` — RED-GREEN-REFACTOR for all code changes
- `testing-patterns` — unit test design for backup function, selectors, auth
- `code-review-checklist` — 12-category scan during validation
- `how-to-git-push-using-ssh-wrapper` — SSH push when OpenSSH is not installed
- `code-simplification` — removing stale entries + untracking bloat
- `distill-codebase-skill` — reference template for this SKILL.md
- `to-distill-project-into-skill` — meta-skill guiding the distillation process

---

*This SKILL.md is a living document. Update it after every round of remediation. Verify every claim against the actual source file at the exact line number. Run `npm run test:plan-alignment` as a CI gate to prevent forbidden tokens from re-entering the documentation.*
