# Comparative Evaluation Report — Four Web-Application Codebases

**Candidates:** `nordeim/digma`, `nordeim/neo-crm`, `nordeim/project-management` (ORBITAL), `nordeim/zero-balance`
**Evaluation purpose:** suitability as a template / foundational codebase to scaffold **any** web application requiring **authentication, dashboard, and charting**
**Evaluation date:** 2026-10-23 (UTC+8) — re-validated same-day against repo HEADs digma `1ad583b2`, neo-crm `f9bc1bf`, project-management `9ff03bc`, zero-balance `b967d3f` — **and re-validated again 2026-10-25 (this edition, v1.2)** against repo HEADs digma `2fa13d7e`, neo-crm `02ac27eb`, project-management `9ff03bcd` (unchanged), zero-balance `1a3553da`; corrections logged in §13
**Method:** documentation-first audit (AGENTS.md → CLAUDE.md → Project_Architecture_Document.md → `*_SKILL.md` → README), followed by code-level verification and executed build/test verification, per audit discipline (findings separated from fixes, severity taxonomy, evidence-backed confidence labels: **Verified** = executed/observed, **Reasoned** = inferred from code read in full, **Assumed** = stated assumption).

First git clone their respective GitHub repo to your local workspace before examining and analyzing their code structure, starting with their key documentation: `AGENTS.md`, `CLAUDE.md`, `Project_Architecture_Document.md` , `<repo-name>_SKILL.md` (`digma_SKILL.md` , `neo-crm_SKILL.md` , `project-management_SKILL.md` and  `zero-balance.md` respectively)

1.  `https://github.com/nordeim/digma.git` 
2.  `https://github.com/nordeim/neo-crm.git` 
3.  `https://github.com/nordeim/project-management.git` 
4.  `https://github.com/nordeim/zero-balance.git` 

**Method (added at re-validation):** documentation-first audit (`AGENTS.md` → `CLAUDE.md` → `Project_Architecture_Document.md` → `<repo>_SKILL.md` → README) against repo HEADs digma `1ad583b2`, neo-crm `f9bc1bf`, project-management `9ff03bc`, zero-balance `b967d3f` (2026-10-23), followed by executed verification per repo (install → prisma → typecheck → build → unit suite → smoke suite). This is the condensed sibling of `codebase-evaluation-report-1.md`, which carries the full evidence base, verification ledger, and findings register; both reports were re-validated together and now agree. Confidence labels: **Verified** = executed/observed, **Reasoned** = inferred from code read in full.

---

## 1. Executive Summary

**Verdict — use `neo-crm` as the foundational template.** It is the most evolved member of the family and the only candidate that fully covers the three required legs (auth, dashboard, charting) at near-production depth: a revocation-capable session-auth core, a KPI/chart dashboard, a 7-type recharts wrapper library, Zod validation at every API boundary, CSV/PDF export, file upload, search, an a11y layer (axe-core in e2e), the family's only open-source **license (MIT)**, and a single-command quality gate (`bun run gate:full`). It also verified green from a clean clone in this environment (install → prisma → typecheck → build → **2,760 unit tests**, **smoke 14/14** — re-executed 2026-10-25). Within hours of the original evaluation, the repo's session-174 implemented this report's own §9.2 graft list (build-as-type-gate, full TS strictness, single lockfile) — and on 2026-10-24 session-176 retired the N-3 recharts debt (2.15 → 3.10.1, ADR-021, the commit naming "the N-3 retirement") — both strengthening the verdict.

**Final ranking (weighted: code quality 30% / feature completeness 40% / architectural robustness 30%):**

| Rank | Codebase | Quality /10 | Features /10 | Architecture /10 | **Weighted** |
|---|---|---|---|---|---|
| **1** | **neo-crm** | 8.5 ▲ | 9.0 | 8.5 | **8.70** |
| **2** | **zero-balance** | 8.0 | 8.0 ▲ | 8.0 | **8.00** |
| **3** | **digma** | 8.5 | 7.0 | 8.0 | **7.75** |
| **4** | **project-management** | 7.0 | 6.0 | 6.5 ▼ | **6.45** |

*(Score adjustments from re-validation are explained in §8 and §13: neo-crm's quality costs were retired same-day by session-174; zero-balance's email-verification funnel was confirmed to exist; project-management's architecture loses a half-point to the reproduced P-6 env-discipline failure. The 2026-10-25 v1.2 pass re-executed everything green and reverted one erroneous re-validation correction (F-6) — ranking order is unchanged under every adjustment.)*

Rank 2 vs 3 was a 0.05 near-tie at evaluation; re-validation widened it to 0.25 (zero-balance's email-verification funnel was confirmed to exist, digma's posture is unchanged). The purpose-fit argument still carries the decision: zero-balance ships all three required legs (Zod boundary, donut-chart dashboard, build-gated types), while digma — despite the best test suite of the family — **ships no charting library at all** (0 recharts references in `src/`; it is a canvas editor, not a charting app). If your future apps will never chart, the two remain close enough to swap.

**Family-wide caveats (apply to all four, before any production deployment):** no hosted CI/CD (local gate only), no Docker artifacts, SQLite dev-default with per-process in-process rate limiting (single-node posture), in-app OTP/reset-link delivery enabled by default (demo posture; disable knobs exist in digma and neo-crm — zero-balance's OTP delivery has **no** knob and **no** code TTL), no observability layer, and — outside neo-crm — **no license**, which legally blocks template reuse until the owner adds one. See §10 for the full register.

---

## 2. Scope, Method & Evidence Base

### 2.1 What was examined

| Repo | Commits | First→last commit (UTC) | Tracked files | Cloned size | License | Stars/Forks |
|---|---|---|---|---|---|---|
| digma | 391 → 399 → **417** | 2026-09-27 → 2026-10-24 | 5,806 → 5,883 → **6,365** | 762 → 777 → **813 MB** | **none** | 0 / 0 |
| neo-crm | 446 → 455 → **476** | 2026-09-29 → 2026-10-24 | 4,114 → 4,478 → **4,575** | 425 → 434 → **438 MB** | **MIT** | 0 / 0 |
| project-management | 121 *(unchanged through 2026-10-25)* | 2026-09-17 → 2026-10-23 | 3,083 *(unchanged)* | 329 MB | **none** | 0 / 0 |
| zero-balance | 268 → 269 → **294** *(25 docs/tests-only commits since 10-23)* | 2026-10-02 → 2026-10-24 | 4,374 → 4,375 → **4,931** | 357 → **367 MB** | **none** | 0 / 0 |

*Original-evaluation → 10-23 re-validation → 10-25 current census (this edition). The 10-23 drift was one-sided (digma sessions 178–180 test/docs-only; neo 172–174; pm and zb code-identical). The 10-25 drift is code-bearing: digma gained sessions 181–186 — including a real auth-hardening cycle (reset tokens SHA-256-hashed at rest, S181-B; production `AUTH_SECRET` fail-hard, S181-C) plus test/docs layers; neo-crm gained sessions 175–183 (recharts 3.x migration s176/ADR-021, layout fixes, +43 unit checks); zero-balance gained 25 docs/tests-only commits (e2e 309 → 319, lockfile audit bumps) with zero `src/` changes; pm is unchanged since the evaluation — every discrepancy against pm is a report error, and one was found (F-6, reverted at v1.2).*

All four are single-author, actively developed (three of four pushed within 24 h of the 2026-10-25 re-validation; pm last pushed 2026-10-23), zero-community projects. Each carries a 194–201 MB vendored personal `skills/` library, 4.9–152 MB of `docs/` session logs/screenshots (digma: 502 session logs + 161 remediation-plan files; zb also carries 282 + 116), and a root `worklog.md` (204–7,392 lines) that are **not app code** — a template-relevant bloat finding (§10).

**Documentation read (in full or in targeted full-section passes):** `AGENTS.md`, `CLAUDE.md`, `Project_Architecture_Document.md`, `digma_SKILL.md` (723 ln at pin → 729 ln, v1.164.0 — twenty numbered sections + a 166-lesson canon; the per-session layers live in `docs/remediation-plan-session*.md`, 161 files, not in the SKILL), `neo-crm_SKILL.md` (12,378 ln at pin → 12,443 ln, v1.180.0 — 16 core sections + ~127 session layers), `project-management_SKILL.md` (739 ln, v1.0.0 — twenty numbered sections + appendices, distilled at app remediation v2.15), `zero-balance_SKILL.md` (1,350 ln at pin → 1,360 ln, v1.0.0 — twenty numbered sections incl. a **42**-lesson §12 — the "38" in the previous edition of this report was an undercount, corrected at v1.2), all four READMEs, all four `package.json`, `prisma/schema.prisma`, `next.config.ts`, `tsconfig.json`, `.env.example`, `src/lib/auth.ts` (neo-crm, in full), `src/components/charts/charts.tsx` (neo-crm), `src/lib/validation.ts` (zero-balance), `src/lib/schemas.ts` (neo-crm), `scripts/smoke-test.sh` (zero-balance), route-tree inventories per repo.

### 2.2 What was executed (verification ledger)

| Check | digma | neo-crm | project-management | zero-balance |
|---|---|---|---|---|
| install (clean clone) | ✅ `bun install` | ✅ `bun install` | ✅ `bun install` | ✅ `npm ci` (its lockfile is package-lock.json) |
| `prisma generate` | ✅ pass | ✅ pass | ✅ pass | ✅ pass |
| typecheck | ✅ pass | ✅ pass | ✅ pass | ✅ pass |
| build (standalone) | ✅ pass, `server.js` produced | ✅ pass **without `ignoreBuildErrors`** — the build *is* the type gate (session-174) | ✅ pass, `server.js` produced | ✅ pass, `server.js` produced |
| unit tests (Vitest) | ✅ **2,588 / 2,588** (248 files; re-executed 10-25) — ⚠ requires the `cp .env.example .env` bootstrap: `tests/lows-s99.test.ts` reads `.env` and ENOENT-fails on a pristine clone (2,562 pass + 1 file fail, re-reproduced 10-25) | ✅ **2,760 / 2,760** (138 files; **pristine — no `.env` needed for the unit leg**; includes session-174's type-gate pins and the test-gated doc-count pins, all green) | ✅ **138 / 138** (15 files; pristine) | ✅ **108 / 108** (9 files; pristine) |
| Secrets scan (`git ls-files`, env files) | only `.env.example` tracked | only `.env.example` tracked | only `.env.example` tracked | only `.env.example` tracked |
| API smoke suite — **executed at both validations** | ✅ **73/73 pass** (documented invocation; the script *refuses loudly* — exit 1 — on an exported `DATABASE_URL`) | ✅ **14/14 pass** (own pinned `smoke.db` + throwaway secret + boot-gate probe on :3210) | ✅ **30/30 pass** on a clean shell — ⚠ **12 passed / 15 failed / 3 silently skipped (27 executed)** under a shell-exported `DATABASE_URL` (P-6, re-reproduced 10-25; the silent-skip guard is itself a new finding, P-8) | ✅ **35/35 pass** (pinned `DATABASE_URL` + :3210; re-proven immune 10-25 — 35/35 again under a hostile export, the probe file never created) |
| Playwright e2e | **not executed** (no browser binaries) — static `--list` census 10-25: 262 checks / 39 spec files | not executed — static census: 192 checks / 11 spec files | not executed — static census: 115 checks / 10 spec files | not executed — static census: **319** checks / 23 spec files (309 at the 10-23 pin — drift, not error; the stale "288" persists in parts of zb's own doc set) |
| Runtime behavior / production deploy / PostgreSQL path | not executed | not executed | not executed | not executed |

All "not executed" rows are reported at **Reasoned** confidence throughout this document; executed rows are **Verified**. Unit-test, build, and smoke claims were re-executed and Verified on 2026-10-23 **and again on 2026-10-25 at post-report HEADs** (bun 1.3.14 / node 24.21 on a 2-core / 4 GB runner: typecheck 0 errors ×4, standalone `server.js` ×4, unit 2,588 / 2,760 / 138 / 108, smoke 73 / 14 / 30 / 35 — all green at both passes; the original run's timings are not comparable and were dropped).

---

## 3. Family DNA (shared context you must know before reusing any of them)

All four repos are siblings from one author and one methodology, which makes their *differences* the real signal:

- **Genesis:** each is a deliberate "superset clone" of a Base44 reference app (design tool / CRM / PM workspace / budget planner), built and continuously parity-remediated through AI-agent sessions (100–450+ commits in 3–5 weeks), with session logs, remediation plans, and pixel-measurement archives committed under `docs/`.
- **Stack (uniform):** Next.js 16 App Router with `output: "standalone"` + pinned `outputFileTracingRoot`, React 19, TypeScript 5.9, Tailwind CSS 4 (CSS-first `@theme`, no JS config), shadcn/ui on Radix, one Zustand 5 store for all server state, Prisma 6 + SQLite (dev default), custom scrypt + HMAC-SHA256 stateless cookie sessions (no NextAuth, no JWT library), z-ai-web-dev-sdk for optional AI features with deterministic fallbacks, Vitest 5 + Playwright 1.6x + a bash API smoke suite, Bun runtime (npm-compatible).
- **Engineering culture (uniform and genuinely strong):** three-tier verification with an isolated self-resetting e2e database; a strict local gate (`lint → typecheck → test → build → smoke → e2e`; zero-balance's documented clean-check chain is the five-stage form — its smoke suite runs as a separate command); "when code and docs disagree, the code wins — fix the doc in the same commit"; why-comments with session-numbered rationale on nearly every non-obvious decision; honest Known-Issues registers.
- **Uniform gaps:** no hosted CI ("the local gate is the only gate" — stated verbatim in all four AGENTS.md), no Docker/compose files, no observability stack, per-process rate limiting, in-app delivery of OTP/reset links by default.

**Implication for template selection:** pick the *most evolved sibling for the target shape* (a multi-entity business app with dashboard + charts ⇒ neo-crm), then graft specific superior practices from the others (§9.2).

---

## 4. Candidate Profiles

### 4.1 neo-crm — "the most complete business-app implementation"
- **Shape:** full CRM — marketing route group + app route group; 15 pages, 29 API route files (41 handlers; **19 session-gated via `requireSession`** — including the destructive demo-wipe `/api/reset`; `/api/auth/me` is ungated *by design* — a logged-out caller receives `data:null`, which smoke check 10 asserts — so the split is 19 gated + 7 public-by-design: signup, verify, resend, forgot-password, logout, `/api/health`, and the regex-pinned `/api/uploads/[name]` serving route; + 3 un-gated public flows: me, login — which mints from user rows — and reset-password — which consumes token rows; corrected at v1.2, see §13); 9 Prisma models (User…role, Account, Contact, Lead, Activity, Event, Opportunity, SavedReport, Setting); recharts 3.10.1 chart family (migrated from 2.15 on 2026-10-24, session-176/ADR-021, the commit naming "the N-3 retirement"); CSV/PDF export (jspdf + html2canvas-pro); file upload + serving; global search; PWA manifest + per-route OG metadata; response-header surface; axe-core in the e2e stack.
- **Auth (deepest of the family):** scrypt hashing; HMAC cookie with a **tokenVersion revocation dimension** (password reset evicts all pre-reset sessions at the DB seam); `timingSafeEqual` verification plus a **login timing equalizer** (miss branch burns the same scrypt work); **fail-hard in production** on missing/short `AUTH_SECRET` (forgeable-session class closed, session-169); reset tokens **hashed at rest** (SHA-256), 60-min TTL, atomic single-use consumption, no-enumeration forgot-password; per-route rate limits (login 10, signup 10, resend 5, verify 20, forgot 10, reset 10, upload 20 per IP/15 min) keyed on a deploy-declared proxy-hop depth (`NEO_PROXY_HOPS`, fails closed). Verified by full read of `src/lib/auth.ts` — every number confirmed at line level, plus the session-170 boot-gate (the server refuses to boot on a missing/short `AUTH_SECRET` in production, enforced via `src/instrumentation.ts` → `src/lib/boot-env.ts`).
- **Validation:** Zod 4 at every JSON boundary via `src/lib/schemas.ts` (716 ln) + `parseBody()` composing a **bounded reader** (Content-Type CSRF gate, declared-length fast-path, chunked-stream counter). The file's own header credits zero-balance as pattern donor — the family deliberately cross-pollinates.
- **Tooling:** the only repo with `gate` and `gate:full` scripts (full gate + 5 drift sweeps + interior census as one command), `lint --max-warnings 0`, DB census script.
- **Documentation:** largest corpus — SKILL.md 12,443 lines (v1.180.0; 16 core sections + ~127 session layers); AGENTS.md 10,625 lines (per-session sections; every count claim is *test-gated* by `tests/docs-counts.test.ts` — a stale count anywhere fails `bun run test`). Current documented counts: 2,760 unit / 192 e2e / 14 smoke (README badge: 2,952 combined). Extraordinary traceability, but **agent-context bloat** (see findings).
- **Costs:** 9 capitalized `.jsx` route aliases + 2 marketing aliases (intentional, documented parity shims — see §10 before flagging as dead code). ~~recharts 2.x~~ — retired by session-176 (see N-3). The three costs flagged at evaluation time — two lockfiles, `ignoreBuildErrors: true`, `noImplicitAny: false` — were **all retired within hours of this report by session-174** (single `bun.lock`; the build is now the type gate; full TS strictness), which is literally this report's §9.2 graft list (the commit message cites this report and the vendored `skills/web-application/SKILL.md` by name).

### 4.2 zero-balance — "the cleanest engineering posture"
- **Shape:** budget planner (net-zero rule) — 7 thin *client*-component pages (`"use client"` compositions — the earlier "server-component" wording was loose; zb's own PAD says so) wrapping one client `AppShell`; 5 Prisma models; 15 API route files (23 handlers), including a full **email-verification funnel** (`/auth/verify-email` + `/auth/resend` — the 6-digit code is returned in-response (`devCode`) *unconditionally* (no SMTP path exists at all), no disable knob, no code TTL, and the attempt counter is non-atomic read-then-write — Z-6/Z-9); recharts 3.10 donut (its only chart type); the 3-level drill-down dashboard (section → category → subcategory → item); the **calculator contract** (every line-item mutation triggers server-side recalculation of the parent item — domain-logic-in-one-place done right); **integer-cent money arithmetic at every aggregation boundary** (ADR-004: amounts are stored and exchanged as decimals — Prisma `Float` columns — but every sum converts to integer cents first via `money.ts`, so IEEE-754 drift can never reach a total).
- **Best-in-family specifics:** the **first repo without `ignoreBuildErrors`** (the production build *is* the type gate; neo-crm joined it in session-174); npm scripts pin `DATABASE_URL` inline and strip it (`env -u`) for Prisma CLI — environment discipline as code (empirically load-bearing: under this validation environment's shell-exported `DATABASE_URL`, zb's full pipeline ran 35/35 untouched while the undefended sibling collapsed — see P-6); the seed routes through the db-path seam (`resolveProcessDatabaseUrl`) like the app; zod 4 at every boundary (`validation.ts`) with genuinely careful schemas (real-calendar-date refinement, empty-string-vs-optional normalization for native date inputs; note its PATCH semantics are two-state — absent = no-write, `""` elided, `null` rejected — the three-state PUT helpers live in neo-crm's `schemas.ts`); `@axe-core/playwright` in the e2e stack behind a two-gate design (structural + palette-provenance); a lean doc corpus (second-smallest — pm's is smaller); ADR-001…007 in the PAD.
- **Costs:** smallest unit suite (108 checks — though the strongest e2e-to-surface ratio: **319** e2e checks after the 2026-10-24 parity iterations — the 10-23 figure of 309 is itself now superseded; stale "288" mentions persist at SKILL :177/:1255, and a further stale "30-step smoke" family lives in CLAUDE.md:66/PAD while everything else says 35 — Z-12); no license; no teams/RBAC; single chart type; **no password-reset funnel at all** (the login card's forgot state renders a message-only "reset unavailable" notice — no API route, no token, no page); the OTP code is stored plaintext at rest and returned in-response with **no disable knob and no TTL** (Z-6); a stray `project-management_SKILL.md` committed at the repo root, byte-identical to pm's own (Z-5); `z-ai-web-dev-sdk` declared as a runtime dependency despite scripts-only (parity-probe) usage; npm-documented but bun-executed runtime scripts (mixed posture — informational); **new at v1.2:** a pristine clone's `db:push` fails P1012 (the README Quick Start omits the `cp .env.example .env` step before it — Z-8, same fresh-clone class as digma's D-7 but on the DB leg); the session TTL is 30 days in code while its PAD claims 7-day (Z-10); the rate-limiter's `clientIp` trusts the first `x-forwarded-for` hop with no proxy-hops contract, contradicting its own doc-comment (Z-11).

### 4.3 digma — "the deepest testing culture, wrong shape for this purpose"
- **Shape:** Figma-like canvas editor — DOM-element canvas, layers/properties panels, AI assistant (degrade-not-fail), teams, PNG export; 5 Prisma models; **zero charting** (0 recharts references; dashboards are stat/project cards).
- **Best-in-family specifics:** **fully strict TypeScript** (alongside pm and zb — digma is the only one of the four that ever needed a strictness *repair*: session-79 removed a leftover `noImplicitAny` contradiction on 2026-10-05); the largest test investment (2,588 unit checks across 248 files — 241 under `tests/`; ⚠ the suite presumes the `cp .env.example .env` bootstrap, see D-7, and session-180 added the README prerequisite line — plus 262 e2e checks across 39 spec files and a 73-check smoke suite, both re-executed green at the 10-25 pass); the most honest Known-Issues register of the family (a HIGH self-reported finding on its own forgot-password default; the no-revocation-list trade-off) — though that register's plaintext-token row is now itself stale (D-8); ADR-001…014 plus 002a/004a (16 ADRs); 3,132-line PAD; env knobs for prod-hardening (`DIGMA_DISABLE_IN_APP_OTP/RESET/AI_LLM`, `DIGMA_PROXY_HOPS`, plus `DIGMA_SITE_URL` and the `DIGMA_REPO_ROOT` db-path escape hatch).
- **Costs:** **no charting** (decisive against rank 2 for this evaluation's purpose); two lockfiles — but documented as intentional (AGENTS.md: `bun.lock` canonical, `package-lock.json` the operator-committed npm mirror, S171-A); stray sibling SKILL files committed (`project-management_SKILL.md`, `scandihaven_SKILL.md`); 401 MB→**424 MB `.git`**, 148 MB→**152 MB `docs/`** (502 session logs + 161 remediation plans); HIGH-severity default (in-app reset URL in response body) documented but shipped as default — **still open at HEAD**; ~~`AUTH_SECRET` is warn-only in production~~ — **resolved by session-181 (S181-C, 2026-10-23, post-report): production now fails hard on a missing/short secret, and its in-code comment cites "the master skill §5 contract"** — the family asymmetry with neo-crm no longer exists.

### 4.4 project-management (ORBITAL) — "lean, disciplined, exotic"
- **Shape:** PM workspace where an AI agent drafts task plans; 8 Prisma models with an ActivityLog narrating every mutating handler (all 12 write it — though goal/task *field* edits short of status/assignee transitions narrate nothing); a degrade-never-fail AI planning pipeline with a sanitizer seam (fallback computed on demand via `?? templatePlan(...)`, no SDK-call timeout, and — unlike digma — no disable knob).
- **Architecture (the differentiator — and the problem):** a **SPA-in-one-page** pattern — every view path (`/goals`, `/my-tasks`, `/activity`…) is a `rewrites()` onto a single workspace page with client-side view switching via a tested `router.ts` seam. Elegant for its parity goal, but as a *general template* it inverts Next.js conventions (no per-view routes, no layout-level code splitting per view) and transfers poorly to "any given web application."
- **Costs:** hand-rolled validation by CLAUDE.md TypeScript-standards rule + v1.2 dependency prune ("do not introduce Zod halfway" — CLAUDE.md:57; Zod was explicitly removed in the v1.2 prune — internally consistent but the weakest input-hardening of the family); oldest dependency generation (declared Next `^16.1.1` — resolved 16.3.5 — React 19.0; Prisma declared `^6.11.1` but lockfile-resolved to 6.19.3); smallest doc corpus; `ignoreBuildErrors: true`; the only sibling with a legacy `tailwind.config.ts` (shadcn HSL tokens + tailwindcss-animate, kept deliberately per CLAUDE.md:62); no license; no charting (goals use a hand-rolled SVG progress ring; the date-card ring is a plain div). **New at re-validation (P-6): no database-environment discipline** — `db:push`/`db:seed` carry no `env -u` guard or inline pin, and the seed bypasses the db-path seam (direct `PrismaClient`), so a shell-exported `DATABASE_URL` silently redirects the database outside the repo (reproduced twice — 10-23 and 10-25: smoke 12 passed / 15 failed / 3 silently skipped → 30/30 after `unset`; the silent-skip guard is new finding P-8).

---

## 5. Dimension A — Code Quality (30%)

| Sub-criterion | digma | neo-crm | project-management | zero-balance |
|---|---|---|---|---|
| TypeScript strictness | **strict, no loosening** (session-79 removed the scaffold-era contradiction) | **strict, no loosening** since session-174 (the flag it carried at evaluation was retired same-day) | **`strict: true` + `noImplicitAny: false`** — present since the initial commit; the 10-23 re-validation's F-6 "correction" was wrong and is **reverted at v1.2** | **`strict: true` + `noImplicitAny: false`** — present since the root commit; same revert (F-6) |
| Build-time type gate | `ignoreBuildErrors` (manual typecheck) | **build is the gate** (session-174) | `ignoreBuildErrors` (manual typecheck) | **build is the gate** |
| Unit test depth (executed 10-25) | **2,588** | **2,760** | 138 | 108 |
| Lint discipline | `eslint .` | `eslint . --max-warnings 0` | `eslint .` | `eslint .` |
| Validation layer | hand-rolled (`validation.ts` + per-route clamps) | **Zod 4 everywhere** (`schemas.ts` + `parseBody`) | hand-rolled (CLAUDE.md rule + v1.2 prune) | **Zod 4 everywhere** (`validation.ts`) |
| Why-comments / traceability | exemplary | exemplary | exemplary | exemplary |
| Repo hygiene | two lockfiles (documented intentional, S171-A); stray sibling SKILL files | single `bun.lock` (session-174 retired package-lock.json); 9.7k-line AGENTS.md | cleanest doc corpus, but the only sibling with a legacy `tailwind.config.ts` | stray `project-management_SKILL.md` at root |
| Known-issues honesty | **best** (self-reported HIGH) | good (session layers) | good | good |

**Reading:** all four are far above the norm for AI-generated codebases — none contains TODO-slop, dead commented code, or placeholder values in app code; comments consistently explain *why* with session-numbered provenance; error handling follows the envelope discipline (never throw across a handler boundary). The quality axis differentiates on strictness policy (the true map, restored at v1.2: digma fully strict since its session-79 repair; neo-crm fully strict since session-174; **pm and zb both carry `noImplicitAny: false` to this day** — the 10-23 re-validation briefly claimed otherwise, see F-6; zb led build-gating with neo-crm joining it in session-174; neo-crm leads on validation + lint ceiling) and hygiene (zb's corpus is second-cleanest with one stray file; digma the most cluttered). This dimension is the closest of the three; the ranking differences come from the other two dimensions.

---

## 6. Dimension B — Feature Completeness for Production Deployment (40%)

Purpose-weighted: authentication depth, dashboard quality, charting, plus the surrounding production surface.

| Capability | digma | neo-crm | project-management | zero-balance |
|---|---|---|---|---|
| Email+password auth (register/login/logout/me) | ✅ | ✅ | ✅ | ✅ |
| Email verification (OTP + resend) | ✅ (in-response by default; `DIGMA_DISABLE_IN_APP_OTP` knob; no code TTL) | ✅ (code hashed, 15-min TTL, knob) | — | ✅ (unconditional in-response delivery, no disable knob, no TTL, non-atomic attempt counter — Z-6/Z-9) |
| Password reset funnel | ✅ (in-app URL default ⚠) | ✅ (hashed tokens, single-use, no-enumeration) | — (none) | — (message-only "reset unavailable" notice; no API route, no token, no page) |
| Session revocation (post-reset eviction) | ✅ tokenVersion (origin) | ✅ tokenVersion | — | — |
| Rate limiting (auth routes) | ✅ + proxy-hops env | ✅ per-route limits + proxy-hops | ✅ (10/15 min) | ✅ |
| Production secret enforcement | **fail-hard in prod** (S181-C, post-report; was dev-fallback warn at evaluation) | **fail-hard in prod** | dev-fallback (silent constant, no warn) | dev-fallback warn |
| RBAC / roles | — (no User.role; TeamMember.role is a job title) | role field + owner FKs across entities (role informational — no route-level RBAC; PAD known-issues "Open") | — (TeamMember.kind human/agent is a classification, not RBAC; PAD §6.3: single-workspace, no RBAC) | — |
| Dashboard | project stat cards | **KPI grid + sparklines + pipeline charts + export** | 2×2 stat/goal/activity grid | hero + drill-down + stat cards + donut |
| **Charting** | **none** | **7 wrapper components, 4 consuming pages** (+ `Sparkline` direct in shared page-parts; the earlier "6 consuming surfaces" overcounted — v1.2) | none (CSS rings) | donut (recharts 3.10) |
| CSV / PDF export | PNG export | **CSV + PDF (jspdf)** | — | — |
| File upload | — | ✅ (upload + regex-pinned serving) | — | — |
| Global search | — | ✅ | — | — |
| PWA / installability | — | ✅ (manifest + icons) | — | ✅ (manifest.webmanifest) |
| SEO surface (robots/sitemap/OG) | ✅ | ✅ (per-route OG family) | ✅ sitemap | basic |
| Accessibility tooling | manual QA matrix | **axe-core in e2e** | manual QA matrix | **@axe-core/playwright** |
| Teams / multi-user data | ✅ teams | ✅ owners across 9 models | ✅ team + activity feed | single-user domain |
| AI features (optional, degrading) | ✅ assistant | — | ✅ planner + clarify | — |
| Email transport | in-app delivery + disable knob | in-app delivery + disable knob | — | in-app OTP delivery, **no disable knob** |
| Hosted CI / CD | **none** | **none** | **none** | **none** |
| Docker / deploy artifacts | standalone build + docs/DEPLOYMENT.md | standalone + docs | standalone + docs | standalone + docs |
| Observability | console + tee logs | console + tee logs | console + tee logs | console + tee logs |
| License | **none** | **MIT** | **none** | **none** |

**Reading:** neo-crm is the only candidate whose feature set approaches what "production deployment" of a generic business web app needs — and its gaps (CI, email transport, observability) are family-wide. digma's auth stack is actually the family's *origin* for the best patterns neo-crm now carries (tokenVersion, bounded reader), but it has no charting and no export/upload/search. zero-balance covers the three required legs at the smallest scale. project-management lacks two of the three legs (no charting, no verification/reset funnel).

---

## 7. Dimension C — Architectural Robustness (30%)

| Criterion | digma | neo-crm | project-management | zero-balance |
|---|---|---|---|---|
| Layer model | 4 layers, imports-down | **5 layers, enforced + inventoried** | 4 layers, clean | 5 layers, clean |
| State architecture | ONE Zustand store + undo/redo gesture stack + autosave drain (impressive, domain-specific) | ONE store + `call()` envelope helper | ONE store + refresh pattern | ONE store + `boot()/refresh()` |
| Data-access discipline | `db.ts` singleton + **db-path seam (fixture-tested, 19 checks)** | db-path seam (20 checks) + `prisma-env.ts` wrapper | db-path seam (15 checks) — but **no env-pinning on db:push/db:seed** (P-6) | db-path seam (15 checks) + env-discipline scripts (empirically load-bearing — see P-6) |
| API contract | ok/fail envelope everywhere | envelope + Zod + bounded reader everywhere | envelope + manual validation | envelope + Zod |
| Route architecture | per-page routes (+ proxy.ts legacy-case redirects) | route groups (marketing)/(app) + server-gated layout (server-side gate decision; the redirect itself is a client shim — session-147, because a server layout cannot know the current path) | **SPA rewrites onto one page** (exotic) | per-page routes, server components |
| Cross-pollination proven | pattern *origin* (tokenVersion, bounded reader) | **proven importer** (zb's Zod, digma's auth ports) | db-path seam first implementer by commit chronology (2026-09-22; pm's docs claim no donor status — the framing is this report's) | pattern donor (Zod seam; seed-through-seam; env-pinning discipline) |
| Scalability posture | single-node documented | single-node documented | single-node documented | single-node documented |
| Agent-readiness (docs as interface) | excellent but bloated | excellent but bloated (12k-line SKILL) | lean and excellent | lean and excellent |

**Reading:** the family's architectural core (layered imports-down, one store, envelope API, schema-anchored DB URL resolution with the standalone-server chdir trap solved and pinned by tests) is sound and unusually well-defended against its own known failure modes. neo-crm edges ahead on enforcement (inventoried layers, gate scripts, drift sweeps) and on the route-group + server-guarded-layout pattern, which is the most conventional and therefore most transferable to "any given web application." project-management's SPA-rewrite pattern is coherent but is the least transferable foundation. digma's editor-store engineering (gesture coalescing, net-zero guards, autosave deadline drain) is the most sophisticated client architecture in the family but is specific to canvas editors.

---

## 8. Scoring & Final Ranking

Weights reflect the evaluation purpose: feature completeness for the stated triad (auth + dashboard + charting) and production deployment carries the most weight (40%), because a template's job is to remove work; code quality 30%; architectural robustness 30%.

| Dimension (weight) | digma | neo-crm | project-management | zero-balance |
|---|---|---|---|---|
| Code quality (30%) | 8.5 | 8.5 ▲ | 7.0 | 8.0 |
| Feature completeness (40%) | 7.0 | 9.0 | 6.0 | 8.0 ▲ |
| Architectural robustness (30%) | 8.0 | 8.5 | 6.5 ▼ | 8.0 |
| **Weighted total** | **7.75** | **8.70** | **6.45** | **8.00** |
| **Rank** | **3** | **1** | **4** | **2** |

*Score movements at re-validation (all Verified, reasoning in §13): neo-crm quality 8.0→8.5 (the three flagged costs — two lockfiles, `ignoreBuildErrors`, `noImplicitAny: false` — were all retired by session-174 within hours of the original evaluation, exactly the §9.2 graft list); zero-balance features 7.5→8.0 (the email-verification funnel exists and was wrongly denied in the original §6 table); project-management architecture 7.0→6.5 (P-6: the reproduced database-environment fragility). digma unchanged.* At v1.2 (2026-10-25) no scores move: everything re-executed green ×4, and the F-6 revert restores strictness facts the original evaluation had already priced in — while post-report drift (digma's session-181 auth hardening; neo-crm's session-176 recharts 3.x migration) strengthens ranks 1 and 3 without changing the order.*

**Sensitivity notes (stated plainly):**
- neo-crm is #1 under any plausible weighting — it leads or ties every dimension that matters for this purpose, and the same-day session-174 hardening widened the lead.
- zero-balance vs digma widened from a 0.05 tie to 0.25: re-validation confirmed zb's email-verification funnel (feature credit) and empirically proved its env-discipline scripts are load-bearing (re-proven 10-25). digma's auth *posture* hardened materially in sessions 181–186 (hashed reset tokens, fail-hard secret), but the purpose-fit gap (zero charting) is unchanged, so the ranking stands. If your future apps will never chart, or you weight test-suite size above built-in charting, they remain close enough to swap.
- project-management ranks last not because it is sloppy — it is disciplined — but because its SPA-in-one-page architecture, hand-rolled validation, and absent verification/reset funnel make it the weakest *foundation for arbitrary web apps*; re-validation added the reproduced P-6 env fragility.

---

## 9. Recommendations

### 9.1 Primary recommendation
**Scaffold from `neo-crm`.** Concretely: delete the vendored `skills/` and `docs/` session archives (≈245 MB), strip the CRM domain entities (keep User + the auth family + the layout chrome + charts + dashboard skeleton + export/upload/search utilities as your starter), then rebrand. Keep its `gate` script as your definition of done. This yields, on day one: production-grade session auth with revocation, a Zod-validated API envelope layer, a chart component library, a dashboard shell, CSV/PDF export, a11y-tested primitives, and the family's best documentation contract — verified green from a clean clone.

### 9.2 Graft from the siblings (the family cross-pollinates by design — continue the tradition)
- From **zero-balance**: drop `ignoreBuildErrors` and make the build the type gate; adopt its inline-`DATABASE_URL` / `env -u` npm-script discipline; adopt its lean documentation size as your doc budget. *(All three were adopted by neo-crm in session-174 within hours of this report — the commit cites §9.2 directly; the env-pinning discipline is now also empirically proven load-bearing, see P-6.)*
- From **digma**: adopt its test-density target and its honest Known-Issues register format; enable full TS strictness. *(The strictness graft was likewise adopted by neo-crm in session-174.)*
- From **project-management**: adopt the "every mutation writes an ActivityLog row" invariant if your domain benefits from audit narration.

### 9.3 Hardening checklist before any production deployment (all four need this)
1. **License** — add one (neo-crm already MIT; the others have none — legally, no one else may reuse them as-is). *(High, legal)*
2. **Hosted CI** — port the local gate (`lint → typecheck → test → build → smoke → e2e`) into a CI workflow; nothing currently enforces it on push. *(High)*
3. **Database** — switch SQLite → PostgreSQL (`.env.example` documents the swap but it is untested in all four) and adopt `prisma migrate` over `db push --accept-data-loss`. *(High)*
4. **Rate limiting** — replace the in-process limiter with a shared store (Redis) for multi-instance deploys; keep the proxy-hops env contract. *(High)*
5. **Email transport** — wire a real mail service behind the existing `*_DISABLE_IN_APP_OTP/RESET` knobs; in-app delivery of OTP/reset links is a demo posture. *(High)*
6. **Secrets at rest** — hash OTP codes and reset tokens (neo-crm hashes both — code scrypt-hashed with 15-min TTL, tokens SHA-256; digma hashed its reset tokens in S181-B but its OTP codes remain plaintext; zero-balance's OTP is plaintext at rest with in-response delivery, no disable knob, and a non-atomic attempt counter — Z-6/Z-9). *(Medium)*
7. **Observability** — structured logging + error tracking (all four tee console output to `server.log` at best). *(Medium)*
8. **RBAC enforcement** — role fields exist but route-level authorization is session-gate only; enforce role checks where the domain requires. *(Medium)*
9. **Docker artifacts** — standalone output is ready for it, but no Dockerfile/compose exists in any repo. *(Medium)*

---

## 10. Findings Register (severity-ordered; Location / Evidence / Impact / Severity / Confidence)

### 10.1 Family-wide (all four repos)

| # | Finding | Evidence | Impact | Severity | Confidence |
|---|---|---|---|---|---|
| F-1 | **No license** (digma, project-management, zero-balance) | `git ls-files` root; GitHub API `license: null` | Template reuse legally blocked (all-rights-reserved by default) | **High (legal)** | Verified |
| F-2 | **No hosted CI/CD** | no app-level `.github/workflows` (only inside vendored `skills/`); AGENTS.md: "There is no hosted CI — the local gate is the only gate" | Quality gates unenforced on push; single-machine bus factor | **High** | Verified |
| F-3 | **Single-node runtime posture** | `rate-limit.ts` per-process fixed-window (documented); SQLite default | N-instance deploys break limiting and require DB migration | **High** | Verified (code) / Reasoned (deploy behavior) |
| F-4 | **In-app OTP / reset-link delivery by default** | digma/neo-crm return codes/URLs in response bodies unless `*_DISABLE_IN_APP_*` set (digma's reset tokens are now hashed at rest, S181-B — but the reset URL still rides the response body by default); zero-balance returns the OTP code in-response **unconditionally** (no SMTP path exists at all) with **no disable knob and no code TTL** (register/resend routes, code-verified) | Account-takeover class if deployed as-is publicly | **High** (default posture) | Verified (documented + code-read; digma self-reports its own as HIGH) |
| F-5 | `ignoreBuildErrors: true` | `next.config.ts` — digma and pm only (neo-crm retired it in session-174, post-evaluation; zb's app-as-built never had it — though its root scaffold commit briefly carried one, replaced same-day) | Type errors do not fail builds; relies on manual `typecheck` | Medium | Verified |
| F-6 | `noImplicitAny: false` — **restored at v1.2 (the re-validation's "correction" was itself wrong)** | `tsconfig.json:13` sets it in **pm** (present at initial commit `3d583ea`, 2026-09-17) and in **zb** (present at root commit `9a1c7ae`, 2026-10-02) — both at current HEAD; both repos' own docs (CLAUDE.md:55, PAD §1.2/§9.3/§10) correctly acknowledge it; zb's config demonstrably compiles implicit-any. The 10-23 re-validation struck this finding on a "git log ×4" proof that does not exist — the very code-wins violation it accused the original of. Only digma (s79) and neo-crm (s174) are fully strict | pm/zb ship loosened `noImplicitAny`; the "all four fully strict" claim is withdrawn; scoring unaffected (the original evaluation priced the flag in) | **Medium** | Verified (`git show <initial>:tsconfig.json` + file read at HEAD, both repos; executable tsc behavior for zb) |
| F-7 | **Repo bloat**: 194–201 MB vendored `skills/` + 4.9–152 MB `docs/` session archives (digma: 502 session logs + 161 remediation plans; zb: 282 + 116) + screenshots + a root `worklog.md` (204–7,392 lines) in every repo | `du`, `git ls-files` counts | Clone/agent-context cost; not app code; template noise | Medium | Verified |
| F-8 | `db push --accept-data-loss` as primary schema workflow | `package.json` scripts | Data-loss foot-gun; migrations underused | Medium | Verified |
| F-9 | No observability layer | console logs, `tee dev.log/server.log` | Production diagnosability gap | Medium | Verified |
| F-10 | No email transport integration | docs; disable-knob envs exist | Production auth flows incomplete | Medium | Verified |
| F-11 | Zero community (0 stars/forks, single author, 3–5 weeks old) | GitHub API | Maintenance-risk factor for foundation adoption | Informational | Verified |

### 10.2 digma

| # | Finding | Evidence | Impact | Severity | Confidence |
|---|---|---|---|---|---|
| D-1 | Forgot-password returns live reset URL in response body by default | PAD §10 Known Issues (self-reported HIGH); route code documented | Unauthenticated capture of reset link | **High** (as-shipped default) | Verified (documented, self-reported) |
| D-2 | **No charting capability** | 0 recharts references in `src/`; no chart dependency | Disqualifying for this evaluation's purpose | **High (purpose-fit)** | Verified |
| D-3 | ~~Reset tokens and OTP codes stored recoverable (plaintext) in User row~~ — **half-resolved by session-181 (S181-B, post-report): reset tokens are now stored SHA-256-hashed at rest** (raw token only in the delivery URL; schema comment + code current). **OTP codes remain plaintext with no TTL** (ADR-0014: the reference's 10-min expiry deliberately not ported) | PAD §10 (B82-L6) + `src/lib/password.ts` hashResetToken + forgot/reset routes | Only the OTP half remains live — and the PAD register row itself is now stale (D-8) | ~~Medium~~ → **Low** (reset half resolved; OTP half remains) | Verified (code + schema comment; register read) |
| D-4 | Stray sibling SKILL files committed — `project-management_SKILL.md` is a **stale variant** of pm's own (578 ln, 2026-09-22, pre-v1.0 numbers vs pm's current 739 ln) and `scandihaven_SKILL.md` (1,512 ln) is a **different app's** skill entirely (a DTC e-commerce monorepo on Drizzle/Postgres/Better-Auth) | root `git ls-files` + `diff` vs pm's own | Template confusion; hygiene; cross-project leakage | Low | Verified |
| D-5 | Two lockfiles (`bun.lock` + `package-lock.json`) | root listing; documented as intentional (AGENTS.md: bun.lock canonical, package-lock.json the operator-committed npm mirror, S171-A — direct deps verified coherent, transitive layer registered unverified) | Non-reproducible installs across package managers (mitigated by documentation) | Low | Verified |
| D-6 | 424 MB `.git`, 152 MB `docs/` (502 session logs + 161 remediation plans, screenshot archives) | `du` | Clone weight; history noise | Low | Verified |
| D-7 | **Unit gate presumes a bootstrapped `.env`** — new at re-validation | `tests/lows-s99.test.ts` does `readFileSync(ROOT/.env)`: ENOENT on a pristine clone (2,475 pass + 1 file fail at 10-23; re-reproduced 10-25: 2,562 pass + 1 file fail); 2,501/2,501 then 2,588/2,588 green after `cp .env.example .env`. Session-180 (post-evaluation) added a README `.env`-prerequisite line | Fresh-clone `bun run test` fails before the documented bootstrap step | Low | Verified (executed both ways, twice) |
| D-8 | **digma's own Known-Issues register row B82-L6 is now materially false for reset tokens** — new at v1.2 | PAD §10 (:3014) still reads "Reset tokens and OTP codes are stored recoverable (plaintext)" while the same PAD's §6.3/§11, the schema comment, and the code (S181-B) carry SHA-256-at-rest; six audit cycles missed the row | A security reviewer reading the register overstates the at-rest exposure (conservative direction); the repo's own S127-C status-sweep doctrine was not applied | **Medium** (register truth) | Verified (row + code + schema read) |

### 10.3 neo-crm

| # | Finding | Evidence | Impact | Severity | Confidence |
|---|---|---|---|---|---|
| N-1 | AGENTS.md 10,625 lines; SKILL.md 12,443 lines (v1.180.0), largely per-session narrative | `wc -l` | Agent-context bloat; signal-to-noise decay for future agents (the family's own leaner repos prove the same discipline fits in ~1,300 lines) | Medium | Verified |
| N-2 | 11 capitalized `.jsx` route alias files alongside lowercase `.tsx` pages | `git ls-files` + file header comments | **Initially suspected dead code — disproven on read:** intentional, documented parity aliases (reference app links to `/Dashboard`); `.jsx` extension deliberately avoids TS1149 casing collision. Cosmetic exoticism only | Informational | Verified (file contents read) |
| N-3 | ~~recharts 2.15~~ — **resolved post-report by session-176** (2026-10-24): 2.15.4 → 3.10.1 (ADR-021); `accessibilityLayer={false}` pinned at all 9 chart-type sites, `tooltipFormatter` adapter, PieLabel bridge; the e2e grid sentinel kept as the standing upgrade guard; wrapper list and zero-data policy survived unchanged | `package.json`; commit f484701 ("the N-3 retirement"); ADR-021 | Migration debt retired inside the family — a live demonstration of the §9.2 graft loop | **Resolved** | Verified |
| N-4 | ~~Two lockfiles committed~~ **— resolved post-evaluation** | session-174 (F-174c) retired `package-lock.json`; single `bun.lock` now, enforced by a type-gate pin | Same as D-5 | **Resolved** | Verified |
| N-5 | Zod adoption is recent (session-163/166) — CRUD seams verified consistent, but the migration is young | `schemas.ts` header | Watch item, not a defect | Informational | Verified (header documents lineage) |

### 10.4 project-management

| # | Finding | Evidence | Impact | Severity | Confidence |
|---|---|---|---|---|---|
| P-1 | SPA-rewrite architecture (all views rewritten onto one page) | `next.config.ts` rewrites + `router.ts` + CLAUDE.md contract | Poor fit as a general template; inverts App Router conventions | **High (purpose-fit)** | Verified |
| P-2 | No email verification / password-reset funnel | route inventory (auth: register/login/logout/me only) | Missing production auth legs | Medium | Verified |
| P-3 | Hand-rolled validation by CLAUDE.md TypeScript-standards rule + v1.2 dependency prune ("do not introduce Zod halfway" — CLAUDE.md:57; not an ADR) | CLAUDE.md; SKILL §8; PAD v1.2 changelog | Weakest input-hardening of the family | Medium | Verified |
| P-4 | Oldest dependency generation (Next 16.1, React 19.0; Prisma declared `^6.11.1` but lockfile-resolved to 6.19.3) | `package.json`, `bun.lock` | Upgrade debt | Low | Verified |
| P-5 | Second-smallest unit suite (138 checks; zero-balance's 108 is smaller — the original "smallest" superlative here was wrong) | executed run | Thinnest pure-seam regression net (its e2e layer is comparatively strong) | Low | Verified |
| P-6 | **No database-environment discipline** — new at re-validation: `db:push`/`db:seed` carry no `env -u` guard or inline pin, and `prisma/seed.ts` bypasses the db-path seam (direct `PrismaClient`; zb's and neo-crm's seeds route through the shared resolver) | Reproduced both ways, twice (10-23 and 10-25): under a shell-exported `DATABASE_URL`, pm's push/seed silently wrote outside the repo while its smoke server (pinned relative URL) read an empty in-repo db → login 500s (P2021) → **smoke 12 passed / 15 failed / 3 silently skipped (27 executed)**; clean shell → **30/30**. zb under the same polluted shell: 35/35 (immune by design; re-proven 10-25 — probe file never created); digma's smoke refuses loudly (exit 1); neo's smoke pins its own throwaway db | A polluted parent shell (CI runner, workspace env) silently breaks the gate — the exact trap the family's own DATABASE_URL contract documents | **Medium** | Verified (executed, both ways, twice) |
| P-7 | **Second bare-`PrismaClient` site** — new at v1.2: `scripts/wizard-cleanup.mjs:6` constructs a client directly (same P-6 class as `seed.ts`; only mitigated under `capture-all.sh`'s pinned tree) | file read | Same silent-redirection trap in a cleanup utility | Low-Medium | Verified (code-read) |
| P-8 | **Smoke's `TASK_ID` guard silently skips 3 checks when upstream legs fail** — the RESULT line cannot reach 30 under failure (12 + 15 = 27 executed in the P-6 reproduction) | `scripts/smoke-test.sh` conditional `ok` sites | A failing leg shrinks the gate's own arithmetic — it undercounts its own failure | Low (gate integrity) | Verified (executed) |
| P-9 | **AI seams have no SDK-call timeout and no disable knob** — fallback computed on demand (`?? templatePlan(...)`), not first; `clarify` + `generate-tasks` can stall until socket death; no `DISABLE_AI_LLM` equivalent exists (digma has one) | `generate-tasks/route.ts:13-46`, `clarify/route.ts`; src env census (only AUTH_SECRET / DATABASE_URL / NEXT_PUBLIC_SITE_URL) | Degrade-never-fail covers failure, not stall; e2e cannot force the deterministic path | Low | Verified (code-read) |
| P-10 | **Stale doc-claim sites the repo's own sweeps missed**: `next.config.ts:14-16` comment enumerates six view paths (seven rewrites exist); PAD §1.2 lockfile-resolution parentheticals (next 16.1.3 vs actual 16.3.5; prisma 6.19.2 vs 6.19.3; zustand 5.0.10 vs 5.0.15); PAD §3.2/§11 line counts and §4.1's Person seed count (10 vs 12) | file reads | Doc-truth drift inside the family's own count-grep discipline — the v2.15 lesson-23 sweep repaired the named docs but missed the comment | Low | Verified |

### 10.5 zero-balance

| # | Finding | Evidence | Impact | Severity | Confidence |
|---|---|---|---|---|---|
| Z-1 | No license | root listing / GitHub API | Same as F-1 | **High (legal)** | Verified |
| Z-2 | Smallest unit suite (108 checks / 9 files) | executed run | Pure-seam coverage thin relative to siblings | Low | Verified |
| Z-3 | Single chart type (donut) | 1 recharts-consuming file | Charting present but shallow vs neo-crm | Low (purpose-fit) | Verified |
| Z-4 | No teams / multi-entity ownership | 5-model schema, userId-only relations | Fine for its domain; limits as generic template | Informational | Verified |
| Z-5 | Stray `project-management_SKILL.md` committed at repo root (byte-identical to pm's own file; unreferenced by the app) — noted in Appendix B at evaluation but missing from this register, an internal-consistency omission of the original report | root listing; `diff` | Template confusion; hygiene | Low | Verified |
| Z-6 | OTP stored plaintext at rest (`verificationCode` raw in the User row, `schema.prisma:30`) and delivered in-response (`devCode` in register/resend bodies) **unconditionally — no SMTP path exists at all** — with **no disable knob and no code TTL**; `MAX_CODE_ATTEMPTS=5` is the only guard, and its counter is **non-atomic read-then-write** (Z-9) | `prisma/schema.prisma:30`; `src/lib/verification.ts`; register/resend/verify-email routes | Same DB-compromise → account-takeover class as digma's B82-L6, plus no production kill-switch | Medium | Verified (code-read; re-verified at the 10-25 HEAD) |
| Z-7 | `z-ai-web-dev-sdk` declared as a runtime dependency but used only by `scripts/parity-probes/*.mjs` (VLM parity sweeps); documented manager is npm while `start`/`db:seed`/Playwright webServer/smoke boot via bun (all four sites verified) | `package.json`; scripts census | Dependency-classification drift; mixed-runtime posture | Informational | Verified |
| Z-8 | **Pristine-clone `db:push` fails P1012** — new at v1.2: the `env -u DATABASE_URL` discipline makes every Prisma CLI leg hard-require `.env`, and the README Quick Start never says `cp .env.example .env` before `db:push` | executed 10-25: `Error code: P1012 … Environment variable not found: DATABASE_URL`; green after the `cp` | Fresh-clone bootstrap fails on the DB leg (same class as digma's D-7, different leg); one-line README fix | Low-Medium | Verified (executed both ways) |
| Z-9 | **OTP attempt counter is read-then-write** — `findUnique` → `user.codeAttempts + 1` → `update`; concurrent wrong codes race the counter | `src/app/api/auth/verify-email/route.ts:38-42` | Loses increments under concurrency; weakens the 5-attempt ladder — violates the family's own atomicity doctrine | Low | Verified (code-read) |
| Z-10 | **Session TTL is 30 days in code, 7 days in its own PAD** — `SESSION_TTL_MS = 30 * 24 * 60 * 60 * 1000` (auth.ts:15) vs PAD ADR-005/§6.3 "7-day expiry"; the only family member off the 7-day norm | code + PAD read | Doc-vs-code drift the family's code-wins rule requires fixing | Low | Verified |
| Z-11 | **Rate-limiter `clientIp` trusts the first `x-forwarded-for` hop** (then `x-real-ip`) with no proxy-hops contract — while its own doc-comment claims "the socket address, unaffected by spoofable headers" | `src/lib/rate-limit.ts` vs its comment; digma/neo ship fail-closed `*_PROXY_HOPS` | Limiter key spoofable when directly exposed; comment contradicts code | Low | Verified |
| Z-12 | **Stale "30-step smoke" count family** — CLAUDE.md:66 says 30 while its own :76 and everything else say 35; PAD ADR-007/§7.1/§7.4/§9.2/§11 also carry "30-step" (and §7.1's whole unit/e2e table is stale: 7 files / 34 e2e vs actual 9 / 319) | doc reads | A stale-count family this report's 10-23 pass missed (it caught the 288s but not the 30-steps) | Low (doc-truth) | Verified |

### 10.6 Positive findings worth recording (no inflation — these are real)

- All four repos **build, typecheck, and pass their entire unit suites from a clean clone** in this environment — executed and observed (§2.2; digma after its documented `.env` bootstrap, D-7). This is rare even among human-maintained templates.
- **All four smoke suites now executed green under their documented invocations** (73/14/30/35) — the original report had these as documented-only.
- No secrets committed anywhere (`.env.example` only, `.env` gitignored) — Verified across all four.
- The `db-path` seam (solving the standalone-server `process.chdir` + Prisma relative-URL ambiguity) is designed, implemented, and **pinned by fixture tests in all four repos** — a genuinely production-grade solution to a real Next.js standalone deployment trap.
- **The DATABASE_URL environment-discipline hierarchy is real and load-bearing** — new at re-validation: under this validation environment's own shell-exported `DATABASE_URL` (an unplanned natural experiment), zero-balance's `env -u` + inline-pin scripts ran its full smoke 35/35 untouched, digma's smoke refused loudly per its documented contract, neo-crm's smoke pinned its own throwaway database — and project-management, the one repo without the discipline, collapsed to 12 passed / 15 failed / 3 silently skipped (27 executed — v1.1's shorthand "12/30" was loose; corrected in §13.1 #23) until the shell was cleaned (P-6). The family's documented contract is not documentation theater; it is the difference between green and red. (Verified, executed)
- Comment quality is exemplary family-wide: nearly every non-obvious decision carries a *why* comment with session-numbered provenance, and every doc states "when code and this document disagree, the code wins — update the doc in the same commit."
- **Re-executed green ×4 on 2026-10-25 at post-report HEADs** — new at v1.2: typecheck 0 errors, builds, and unit suites (2,588 / 2,760 / 138 / 108) all pass without touching a single tracked file; neo-crm's entire unit leg runs pristine with **no `.env` at all** (the only repo of the four that can say that).
- **The vendored family skills are measurably steering the codebases** — new at v1.2: digma's S181-C fail-hard comment cites "the master skill §5 contract" verbatim; neo-crm's session-174 commit cites `skills/web-application/SKILL.md` and this report's §9.2; neo's session-176 retires N-3 by name. The evaluation changed the codebase it evaluated — repeatedly, and traceably.
- **The env-discipline hierarchy re-proven in a single session (10-25)**: the same hostile shell produced zb 35/35 (probe file never created), digma loud-refusal (exit 1), neo 14/14 on its own throwaway db — and pm 12 passed / 15 failed / 3 skipped. Same inputs, same separation, twice.

---

## 11. Verification Ledger (what was checked, how, result)

| # | Check | How | Result |
|---|---|---|---|
| 1 | Clean-clone build pipeline (×4) | `scripts/verify-pipeline.sh`: install → prisma generate → typecheck → build (logs at `scripts/verify-<repo>.log`; bun for digma/neo/pm, npm ci for zb) | **All green, ×4**; standalone `server.js` produced ×4 |
| 2 | Unit suites (×4) | `vitest run` per repo | digma 2,501/2,501 (242 files; `.env` bootstrap required — D-7) · neo 2,717/2,717 (138 files, incl. type-gate + doc-count pins) · pm 138/138 (15 files) · zb 108/108 (9 files) — **all pass** |
| 3 | Smoke suites (×4) — **newly executed** | each repo's `scripts/smoke-test.sh` under its documented invocation | digma **73/73** · neo **14/14** · pm **30/30** clean-shell / **12/30** under exported `DATABASE_URL` (P-6) · zb **35/35** |
| 4 | Secrets hygiene | `git ls-files` env-file census | Only `.env.example` tracked, ×4 |
| 5 | License presence | root file listing + GitHub API | MIT (neo-crm) only |
| 6 | Charting capability | `git grep recharts -- src` per repo | neo-crm 7 files · zb 1 · digma 0 · pm 0 |
| 7 | Auth implementation quality | full read of neo-crm `src/lib/auth.ts` + family comparison via SKILL/CLAUDE + route inventories | §4.1 claims confirmed at line level (incl. exact rate-limit constants and the boot gate) |
| 8 | Validation boundaries | full/partial reads of `schemas.ts` (neo), `validation.ts` (zb); CLAUDE.md rules for digma/pm | §5 claims verified |
| 9 | Suspicion checks: neo-crm capitalized `.jsx` routes; pm/zb `noImplicitAny`; zb money model; zb email-verification funnel | file reads, `git log -- tsconfig.json` ×4, schema reads, route inventory | `.jsx` aliases = intentional (kept); pm/zb **never** had `noImplicitAny: false` (F-6 corrected) — **[v1.2: this verdict was itself wrong — see ledger row 16 and §13.1 #17; both repos have carried the flag since their initial commits]**; zb money = decimal storage + cents-at-aggregation (§4.2 corrected); zb verification funnel **exists** (§6 corrected) |
| 10 | Doc corpora sizes + versions | `wc -l` + version headers across all key docs | As reported in §2.1/§4 |
| 11 | Repo activity & metadata | `git log` census + GitHub API | As reported in §2.1 |
| 12 | E2E suites | **not executed** (no browser binaries) | Documented counts (Reasoned): digma 262 / 39 files · neo 192 / 11 · pm 115 / 10 · zb 309 / 23 |
| 13 | Provenance of the validated documents | `diff` vs `neo-crm/skills/web-application{,-engineering}/` | All four validation targets are byte-identical to copies vendored inside neo-crm — session-174 cites them as its rotation trigger |
| 14 | **v1.2 pass (10-25): pipelines ×4 re-executed** | install / prisma generate / typecheck / unit / build / smoke per repo, `env -u DATABASE_URL` discipline, foreground runs | All green ×4 — unit 2,588 / 2,760 / 138 / 108; smoke 73 / 14 / 30 / 35; `server.js` ×4; typecheck 0 errors ×4 |
| 15 | P-6 re-reproduction + zb immunity probe | pm: polluted `db:push`/`db:seed` → db written outside the repo → smoke 12 pass / 15 fail / 3 skipped (P2021 in the server log); clean rerun 30/30. zb: smoke 35/35 under the hostile export, probe file never created | P-6 confirmed exactly; zb structurally immune (both Verified, executed) |
| 16 | F-6 strictness archaeology | `git show <initial-commit>:tsconfig.json` (pm 3d583ea, zb 9a1c7ae) + current file read ×4 + executable tsc probe for zb | pm and zb both carry `noImplicitAny: false` since birth — the 10-23 "correction" reverted |
| 17 | Provenance byte-checks (v1.2) | `cmp` uploads vs all vendored copies | `web-application_SKILL.md` + evaluation report byte-identical in digma/neo/zb `skills/web-application/`; `web-app-foundation_SKILL.md` byte-identical in **all four** `skills/web-app-foundation/`; neo also stages v1.5/v2 generations there; the 175-ln `web-application-engineering` skill + 92-ln condensed report are distinct companion condensations, not byte-copies |
| 18 | Post-pin drift disambiguation | `git show <pin>:<doc>` ×4 + `git diff <pin>..HEAD --stat` per repo | All four doc-version claims were correct at their pinned HEADs; every changed number since is drift (digma s181–186, neo s175–183, zb docs-only) — and every pm mismatch is report error (one found: F-6) |
| 19 | E2E static censuses | `playwright test --list` per repo (no browser binaries) | digma 262 checks / 39 spec files · neo 192 / 11 · pm 115 / 10 · zb 319 / 23 (+1 setup file each) — Reasoned (listed, not executed) |

---

## 12. Appendix A — Comparative Quick Facts

| | digma | neo-crm | project-management | zero-balance |
|---|---|---|---|---|
| Domain | design workspace (canvas editor) | CRM | PM workspace + AI planner | budget planner |
| Next.js / React / Prisma (declared) | 16.4 / 19.3 / 6.19 | 16.4 / 19.3 / 6.19 | 16.1 / 19.0 / ^6.11.1 | 16.1 / 19.0 / 6.11.1 (exact pin) |
| Prisma (lockfile-resolved) | 6.19.3 | 6.19.3 | 6.19.3 | 6.11.1 |
| Prisma models | 5 | 9 | 8 | 5 |
| API route files | 18 | 29 | 16 | 15 |
| Runtime deps | 17 | 20 | 20 | 25 |
| Zod | — | ✅ 4.6 | — (CLAUDE.md rule against) | ✅ 4.6 |
| Charts | — | recharts 3.10.1 (7 wrappers; s176 migration) | — (hand-rolled SVG ring) | recharts 3.10 (donut) |
| Export | PNG | CSV (dashboard) + PDF (reports) | — | — |
| Unit checks (executed 10-25) | 2,588 | 2,760 | 138 | 108 |
| E2E checks (static census) | 262 | 192 | 115 | 319 |
| Smoke checks (executed 10-25) | 73 | 14 | 30 | 35 |
| `ignoreBuildErrors` | yes | **no** (retired s174) | yes | **no** (as-built) |
| `noImplicitAny: false` | never (scaffold contradiction removed s79) | had it; retired s174 | **false — set since the initial commit** | **false — set since the root commit** |
| License | none | **MIT** | none | none |
| SKILL.md size | 729 ln (v1.164.0) | 12,443 ln (v1.180.0) | 739 ln (v1.0.0) | 1,360 ln (v1.0.0) |

## Appendix B — Documentation set examined per repo

`AGENTS.md` · `CLAUDE.md` · `Project_Architecture_Document.md` · `README.md` · `digma_SKILL.md` / `neo-crm_SKILL.md` / `project-management_SKILL.md` / `zero-balance_SKILL.md` (per the evaluation brief) · `package.json` · `prisma/schema.prisma` · `next.config.ts` · `tsconfig.json` · `.env.example` · key `src/lib/*` seams · chart/dashboard components · `scripts/smoke-test.sh` · root-level hygiene census. digma additionally carries stray `project-management_SKILL.md` + `scandihaven_SKILL.md` (noted D-4); zero-balance carries a stray `project-management_SKILL.md` (now also registered as Z-5). The file the evaluation brief calls `zero-balance.md` is actually `zero-balance_SKILL.md` in the repo.

---

## 13. Validation & Corrections Log (v1.1 — 2026-10-23; v1.2 — 2026-10-25)

**Method.** The four repos were re-cloned (HEADs pinned in the header), re-censused mechanically (`scripts/census-*.txt`), re-audited documentation-first by four parallel deep-dive passes (~90 claim verdicts with file:line evidence), and re-executed end-to-end (`scripts/verify-pipeline.sh` → install / prisma generate / typecheck / build / unit tests per repo, plus every repo's smoke suite under its documented invocation — logs at `scripts/verify-<repo>.log`). Environment: bun 1.3.14, node 24, 2-core / 4 GB runner. Playwright e2e remains not executed (no browser binaries). This environment pre-exports a `DATABASE_URL` pointing outside the repos — an unplanned natural experiment that materially strengthened the findings (P-6, §10.6).

**Provenance.** All four documents under validation (this report, its shorter sibling `codebase-evaluation-report-2.md`, and both `web-application*_SKILL.md` files) are **byte-identical to copies vendored inside neo-crm** (`skills/web-application/` and `skills/web-application-engineering/`). neo-crm's session-174 commit (2026-10-23 09:28 UTC) names them as its rotation trigger and implements this report's §9.2 — the evaluation measurably changed the codebase it evaluated, within hours.

**Corrections applied to this report** (numbered; severity = impact the error had on the report's conclusions):

1. **§6/§4.2 zb email verification — cell was wrong, code unchanged since evaluation.** zb has a full OTP verification funnel (`/auth/verify-email` + `/auth/resend`, since 2026-10-09). The original "—" cell denied a shipped feature. (High — affected feature scoring; zb features 7.5→8.0.)
2. **§6/§4.2 zb password reset — "partial (reset UI)" overstated.** zb has *no* reset funnel at all: the login card's forgot state is a message-only "reset unavailable" notice; no API route, token, or page. (Medium.)
3. **§4.2 zb money model — "integer-cents end-to-end" misdescribed the design.** Actual: decimal amounts on the wire and in storage (Prisma `Float` columns) with integer-cent conversion at every aggregation boundary (ADR-004). Equally safe for totals; different contract for schema authors. (Medium.)
4. **F-6 — `noImplicitAny: false` was only ever true of neo-crm.** pm and zb never set it (git history of tsconfig.json). Root cause of the original error: pm's own PAD/CLAUDE.md carry a stale row claiming it — the report trusted documentation over code, violating the family's code-wins rule. neo-crm retired the flag post-evaluation (session-174). (Medium — mis-scoped a Medium finding across two repos.)
5. **Route counts — digma ~13→18, pm ~14→16, zb 13→15 (21→23 handlers).** Verified at the evaluation-point commits; these were report errors, not drift. (Medium — factual.)
6. **§4.1 neo gated/public split — 19/10 → 20 `requireSession`-gated + 2 session-reading (login, reset-password) + 7 public.** (Low.)
7. **§6 digma RBAC — "role field" wrong.** digma's User has no role field; TeamMember.role is a job title, not a role class. (Low.)
8. **Superlative double-claims.** "Smallest doc corpus" was claimed for both zb (§4.2) and pm (§4.4) — pm's is smaller; "smallest unit suite" was claimed for both pm (P-5) and zb (Z-2) — zb's is smaller. Both now single-attributed. (Low — internal consistency.)
9. **zb e2e count — 288 → 309.** The 288 came from stale sections of zb's own documentation; the SKILL frontmatter and a live count both say 309. (Low.)
10. **digma ADR census — "ADR-001…013+004a" → 16 ADRs (001–014 + 002a + 004a).** (Low.)
11. **P-3 — "hand-rolled validation by ADR" mislabeled.** The rule is a CLAUDE.md TypeScript-standards line plus the v1.2 dependency prune, not an ADR. (Low.)
12. **pm/zb/neo SKILL structure descriptions** — §1–§16/§1–§9 undercounts; all three are twenty-section documents (+ digma's 166-lesson canon; neo's 16 core + ~136 session layers). (Low.)
13. **Numbers refreshed to re-validation HEADs** — commits 399/455/121/269; tracked files 5,883/4,478/3,083/4,375; AGENTS/SKILL/PAD line counts; unit counts 2,501/2,717/138/108 (digma +37 and neo +49 from post-evaluation sessions 178–180 / 172–174; pm and zb unchanged); cloned sizes. Drift and error are disambiguated per repo (§2.1 note).
14. **N-4 (two lockfiles) and the neo-crm `ignoreBuildErrors` / `noImplicitAny` costs — resolved/retired by session-174**, post-evaluation, per the repo's own commit which cites this report's §9.2. (Improvement — noted, not an error.)
15. **New findings added:** D-7 (digma's `.env`-bootstrap test requirement — verified executed both ways), P-6 (pm's missing database-environment discipline — reproduced 12/30 → 30/30), Z-5 (stray sibling SKILL file, promoted from an Appendix-B-only mention), Z-6 (zb plaintext OTP, no knob, no TTL), Z-7 (zb z-ai-sdk as runtime dep for scripts-only use; mixed npm/bun posture).
16. **§2.2 ledger rewritten** — smoke suites now executed (73/14/30/35), digma `.env` caveat recorded, provenance check added; the original ledger's referenced artifacts (`scripts/build-verify-*.log`) belong to the prior workspace and were superseded by this run's `scripts/verify-*.log`.

**What survived validation unchanged (and was strengthened):** the verdict (neo-crm first) and ranking order under every correction; all neo-crm auth-depth claims (confirmed at line level, including every rate-limit constant, the timing equalizer, hashed reset tokens, and the boot gate); the architecture characterizations (pm's SPA contract is quoted verbatim in its CLAUDE.md; neo's route-group + server-gated layout confirmed); license and zero-community facts; the positive findings (§10.6); and the family-wide caveats — now including empirical proof that the documented DATABASE_URL discipline is load-bearing.

**Confidence.** All corrections above are **Verified** (executed, observed, or read at file:line with git-history disambiguation) except where a cell cites the repos' own documentation (Reasoned), as labeled in the tables.

---

## 13.1 v1.2 Re-Validation (2026-10-25) — Corrections & Refresh

**Method (v1.2).** The four repos were re-cloned at the new HEADs pinned in the header (digma `2fa13d7e` · neo-crm `02ac27eb` · project-management `9ff03bcd` — unchanged · zero-balance `1a3553da`), re-censused mechanically, re-audited documentation-first by four parallel deep-dive passes (~70 claim verdicts with file:line evidence), and re-executed end-to-end per repo (install → prisma generate → typecheck → unit → build → smoke) under an `env -u DATABASE_URL` discipline — plus the P-6 polluted-shell reproduction (pm) and the immunity probe (zb) re-run in the same session. Environment: bun 1.3.14, node 24.21, 2-core / 4 GB runner. Playwright e2e remains not executed (no browser binaries); counts come from `playwright test --list` static censuses.

**Corrections applied at v1.2** (numbered; continuing the v1.1 series):

17. **F-6 reverted — the v1.1 correction #4 was itself wrong.** pm and zb both ship `noImplicitAny: false` (pm `tsconfig.json:13` present at initial commit `3d583ea`, 2026-09-17; zb `tsconfig.json:13` at root commit `9a1c7ae`, 2026-10-02 — both confirmed by `git show` at those commits and both present at current HEAD; zb's config demonstrably compiles implicit-any). The repos' own docs (pm CLAUDE.md:55, PAD §1.2/§9.3/§10) were right all along; the v1.1 "`git log ×4`" proof does not exist. §5/§12 rows restored; the "all four fully strict" claim is withdrawn; scoring is unaffected because the original evaluation had already priced the flag in. The irony is recorded plainly: the code-wins rule indicts this report's own re-validation, not the repos.
18. **§4.1 route-gate split corrected: 19 gated, not 20.** `/api/auth/me` is ungated *by design* (a logged-out caller receives `data:null`; smoke check 10 asserts exactly that); login and reset-password are un-gated flows that do not read session state (login mints from user rows; reset consumes token rows). Identical at the pin → report error, not drift.
19. **Chart consumers corrected: 4 consuming pages**, not "6 consuming surfaces" (+ `Sparkline` consumed directly from the shared page-parts module). Identical at the pin → report error.
20. **zb §12 lesson count corrected: 42, not 38.** Identical at the pin → report error.
21. **zb page wording corrected**: the 7 pages are thin `"use client"` compositions, not server components (zb's own PAD says so).
22. **zb OTP delivery wording tightened**: not "in demo mode" — delivery is unconditional; no SMTP path exists in the codebase at all.
23. **pm smoke arithmetic corrected**: under the polluted shell the tally is 12 passed / 15 failed / **3 silently skipped** (27 executed) — the smoke's `TASK_ID` guard drops checks when upstream legs fail; the guard itself is registered as P-8.
24. **pm RBAC cell corrected**: TeamMember.kind human/agent is a classification, not RBAC (PAD §6.3 "single-workspace model with no RBAC") — the cell now reads "—", like digma's. neo's row gained the same honesty note (role field exists but no route-level RBAC — PAD known-issues "Open").
25. **Drift-driven status updates (not errors):** digma D-3 half-resolved (S181-B: reset tokens SHA-256-hashed at rest) + production `AUTH_SECRET` fail-hard (S181-C — its comment cites the vendored master skill's §5; the family asymmetry is closed) + **D-8 added** (digma's own register row B82-L6 is now stale); neo N-3 resolved (s176/ADR-021: recharts 3.10.1, commit f484701 naming "the N-3 retirement"); zb e2e 309 → 319 and lockfile audit bumps (next 16.4.0 → 16.4.3, zod 4.6.5 → 4.6.7 — package.json untouched).
26. **New findings registered:** D-8; P-7 (second bare `PrismaClient` in `scripts/wizard-cleanup.mjs`); P-8 (smoke silent-skip guard); P-9 (AI SDK no timeout, no disable knob); P-10 (stale doc-claim sites: six-view comment, PAD resolution parentheticals, seed counts); Z-8 (pristine `db:push` P1012 — README quickstart omits the `cp`); Z-9 (non-atomic OTP attempt counter); Z-10 (30-day session TTL vs PAD's 7-day claim); Z-11 (`clientIp` trusts the first XFF hop, comment contradicts code); Z-12 (stale "30-step smoke" family).
27. **Census + provenance refreshed to the 10-25 HEADs**: §2.1 triplets; unit 2,588 / 2,760 / 138 / 108 (executed); e2e static census 262 / 192 / 115 / 319; smoke 73 / 14 / 30 / 35 (re-executed); doc line counts and SKILL versions; docs corpus 502/161 (digma) etc.; worklog range 204–7,392. Provenance tightened: the application skill and this report are byte-identical to the copies vendored in digma/neo/zb `skills/web-application/`; the foundation skill is byte-identical to `skills/web-app-foundation/SKILL.md` in **all four** repos (where neo also stages v1.5/v2 generations of it); the 175-line `web-application-engineering` skill and the 92-line `Codebase_Evaluation_Report.md` are *distinct condensed companions*, not byte-copies — the v1.1 "all four documents byte-identical across both dirs" sentence overstated the set.

**What survived the v1.2 pass:** the verdict and ranking (re-executed green ×4; both post-report drift windows strengthened #1 and #3 without reordering); every neo-crm auth constant (re-confirmed at line level at HEAD, including the upload-20 limit, the 15-minute verification TTL, and the boot gate); the P-6 hierarchy (re-proven in one session, both directions); the positive findings (§10.6, now with re-execution rows); and the family-wide caveats.

**Confidence (v1.2).** All corrections above are **Verified** (executed, observed, or read at file:line with git-history disambiguation) except the e2e static censuses (Reasoned — listed, not executed).
