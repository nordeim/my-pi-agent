# Comparative Evaluation Report — Four Web-Application Codebases

**Candidates:** `nordeim/digma`, `nordeim/neo-crm`, `nordeim/project-management` (ORBITAL), `nordeim/zero-balance`
**Evaluation purpose:** suitability as a template / foundational codebase to scaffold **any** web application requiring **authentication, dashboard, and charting**
**Evaluation date:** 2026-10-23 (UTC+8) — **re-validated same-day** against repo HEADs digma `1ad583b2`, neo-crm `f9bc1bf`, project-management `9ff03bc`, zero-balance `b967d3f`; corrections logged in §13
**Method:** documentation-first audit (AGENTS.md → CLAUDE.md → Project_Architecture_Document.md → `*_SKILL.md` → README), followed by code-level verification and executed build/test verification, per audit discipline (findings separated from fixes, severity taxonomy, evidence-backed confidence labels: **Verified** = executed/observed, **Reasoned** = inferred from code read in full, **Assumed** = stated assumption).

First git clone their respective GitHub repo to your local workspace before examining and analyzing their code structure, starting with their key documentation: `AGENTS.md`, `CLAUDE.md`, `Project_Architecture_Document.md` , `<repo-name>_SKILL.md` (`digma_SKILL.md` , `neo-crm_SKILL.md` , `project-management_SKILL.md` and  `zero-balance.md` respectively)

1.  `https://github.com/nordeim/digma.git` 
2.  `https://github.com/nordeim/neo-crm.git` 
3.  `https://github.com/nordeim/project-management.git` 
4.  `https://github.com/nordeim/zero-balance.git` 

**Method (added at re-validation):** documentation-first audit (`AGENTS.md` → `CLAUDE.md` → `Project_Architecture_Document.md` → `<repo>_SKILL.md` → README) against repo HEADs digma `1ad583b2`, neo-crm `f9bc1bf`, project-management `9ff03bc`, zero-balance `b967d3f` (2026-10-23), followed by executed verification per repo (install → prisma → typecheck → build → unit suite → smoke suite). This is the condensed sibling of `codebase-evaluation-report-1.md`, which carries the full evidence base, verification ledger, and findings register; both reports were re-validated together and now agree. Confidence labels: **Verified** = executed/observed, **Reasoned** = inferred from code read in full.

---

## 1. Executive Summary

**Verdict — use `neo-crm` as the foundational template.** It is the most evolved member of the family and the only candidate that fully covers the three required legs (auth, dashboard, charting) at near-production depth: a revocation-capable session-auth core, a KPI/chart dashboard, a 7-type recharts wrapper library, Zod validation at every API boundary, CSV/PDF export, file upload, search, an a11y layer (axe-core in e2e), the family's only open-source **license (MIT)**, and a single-command quality gate (`bun run gate:full`). It also verified green from a clean clone in this environment (install → prisma → typecheck → build → **2,717 unit tests**, **smoke 14/14**). Within hours of the original evaluation, the repo's session-174 implemented this report's own §9.2 graft list (build-as-type-gate, full TS strictness, single lockfile), strengthening the verdict.

**Final ranking (weighted: code quality 30% / feature completeness 40% / architectural robustness 30%):**

| Rank | Codebase | Quality /10 | Features /10 | Architecture /10 | **Weighted** |
|---|---|---|---|---|---|
| **1** | **neo-crm** | 8.5 ▲ | 9.0 | 8.5 | **8.70** |
| **2** | **zero-balance** | 8.0 | 8.0 ▲ | 8.0 | **8.00** |
| **3** | **digma** | 8.5 | 7.0 | 8.0 | **7.75** |
| **4** | **project-management** | 7.0 | 6.0 | 6.5 ▼ | **6.45** |

*(Score adjustments from re-validation are explained in §8 and §13: neo-crm's quality costs were retired same-day by session-174; zero-balance's email-verification funnel was confirmed to exist; project-management's architecture loses a half-point to the reproduced P-6 env-discipline failure. Ranking order is unchanged under every adjustment.)*

Rank 2 vs 3 was a 0.05 near-tie at evaluation; re-validation widened it to 0.25 (zero-balance's email-verification funnel was confirmed to exist, digma's posture is unchanged). The purpose-fit argument still carries the decision: zero-balance ships all three required legs (Zod boundary, donut-chart dashboard, build-gated types), while digma — despite the best test suite of the family — **ships no charting library at all** (0 recharts references in `src/`; it is a canvas editor, not a charting app). If your future apps will never chart, the two remain close enough to swap.

**Family-wide caveats (apply to all four, before any production deployment):** no hosted CI/CD (local gate only), no Docker artifacts, SQLite dev-default with per-process in-process rate limiting (single-node posture), in-app OTP/reset-link delivery enabled by default (demo posture; disable knobs exist in digma and neo-crm — zero-balance's OTP delivery has **no** knob and **no** code TTL), no observability layer, and — outside neo-crm — **no license**, which legally blocks template reuse until the owner adds one. See §10 for the full register.

---

## 2. Scope, Method & Evidence Base

### 2.1 What was examined

| Repo | Commits | First→last commit (UTC) | Tracked files | Cloned size | License | Stars/Forks |
|---|---|---|---|---|---|---|
| digma | 391 → **399** | 2026-09-27 → 2026-10-23 | 5,806 → **5,883** | 762 → **777 MB** | **none** | 0 / 0 |
| neo-crm | 446 → **455** | 2026-09-29 → 2026-10-23 | 4,114 → **4,478** | 425 → **434 MB** | **MIT** | 0 / 0 |
| project-management | 121 *(unchanged)* | 2026-09-17 → 2026-10-22 | 3,083 *(unchanged)* | 329 MB | **none** | 0 / 0 |
| zero-balance | 268 → **269** *(docs-only commit)* | 2026-10-02 → 2026-10-23 | 4,374 → **4,375** | 357 MB | **none** | 0 / 0 |

*Original-evaluation census → re-validation census. The drift is one-sided: digma gained sessions 178–180 (test pins + docs only, zero `src/` changes), neo-crm gained sessions 172–174 (property-test families, then the §9.2 config hardening); pm and zb are code-identical to the evaluation point — every discrepancy against them below is a report error, not drift.*

All four are single-author, actively developed (pushed within the last 24 h of evaluation), zero-community projects. Each carries a ~195 MB vendored personal `skills/` library (194–201 MB measured), 4.9–148 MB of `docs/` session logs/screenshots (digma: 469 session logs + 155 remediation-plan files), and a root `worklog.md` (204–6,820 lines) that are **not app code** — a template-relevant bloat finding (§10).

**Documentation read (in full or in targeted full-section passes):** `AGENTS.md`, `CLAUDE.md`, `Project_Architecture_Document.md`, `digma_SKILL.md` (723 ln, v1.158.0 — twenty numbered sections + a 166-lesson canon; the per-session layers live in `docs/remediation-plan-session*.md`, 155 files, not in the SKILL), `neo-crm_SKILL.md` (12,378 ln, v1.171.0 — 16 core sections + ~136 session layers), `project-management_SKILL.md` (739 ln, v1.0.0 — twenty numbered sections + appendices, distilled at app remediation v2.15), `zero-balance_SKILL.md` (1,350 ln, v1.0.0 — twenty numbered sections incl. a 38-lesson §12), all four READMEs, all four `package.json`, `prisma/schema.prisma`, `next.config.ts`, `tsconfig.json`, `.env.example`, `src/lib/auth.ts` (neo-crm, in full), `src/components/charts/charts.tsx` (neo-crm), `src/lib/validation.ts` (zero-balance), `src/lib/schemas.ts` (neo-crm), `scripts/smoke-test.sh` (zero-balance), route-tree inventories per repo.

### 2.2 What was executed (verification ledger)

| Check | digma | neo-crm | project-management | zero-balance |
|---|---|---|---|---|
| install (clean clone) | ✅ `bun install` | ✅ `bun install` | ✅ `bun install` | ✅ `npm ci` (its lockfile is package-lock.json) |
| `prisma generate` | ✅ pass | ✅ pass | ✅ pass | ✅ pass |
| typecheck | ✅ pass | ✅ pass | ✅ pass | ✅ pass |
| build (standalone) | ✅ pass, `server.js` produced | ✅ pass **without `ignoreBuildErrors`** — the build *is* the type gate (session-174) | ✅ pass, `server.js` produced | ✅ pass, `server.js` produced |
| unit tests (Vitest) | ✅ **2,501 / 2,501** (242 files) — ⚠ requires the `cp .env.example .env` bootstrap: `tests/lows-s99.test.ts` reads `.env` and ENOENT-fails on a pristine clone (2,475 pass + 1 file fail) | ✅ **2,717 / 2,717** (138 files — includes session-174's type-gate pins and the test-gated doc-count pins, all green) | ✅ **138 / 138** (15 files) | ✅ **108 / 108** (9 files) |
| Secrets scan (`git ls-files`, env files) | only `.env.example` tracked | only `.env.example` tracked | only `.env.example` tracked | only `.env.example` tracked |
| API smoke suite — **now executed** | ✅ **73/73 pass** (via its documented `unset DATABASE_URL && ./scripts/smoke-test.sh` invocation) | ✅ **14/14 pass** (own pinned `smoke.db` + throwaway secret + boot-gate probe on :3210) | ✅ **30/30 pass** on a clean shell — ⚠ **12/30 under a shell-exported `DATABASE_URL`** (P-6) | ✅ **35/35 pass** (pinned `DATABASE_URL` + :3210; structurally immune to shell pollution) |
| Playwright e2e | **not executed** (no browser binaries in this environment) — documented: 262 checks / 39 spec files | not executed — documented: 192 checks / 11 spec files | not executed — documented: 115 checks / 10 spec files | not executed — documented: **309** checks / 23 spec files (the "288" in parts of zb's own doc set is stale) |
| Runtime behavior / production deploy / PostgreSQL path | not executed | not executed | not executed | not executed |

All "not executed" rows are reported at **Reasoned** confidence throughout this document; executed rows are **Verified**. Unit-test, build, and smoke claims above were re-executed and Verified in this environment on 2026-10-23 (bun 1.3.14 / node 24 on a 2-core runner; the original run's timings are not comparable and were dropped).

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
- **Shape:** full CRM — marketing route group + app route group; 15 pages, 29 API route files (20 session-gated via `requireSession` — including `/api/auth/me` and the destructive demo-wipe `/api/reset`; 7 public-by-design: signup, verify, resend, forgot-password, logout, `/api/health`, and the regex-pinned `/api/uploads/[name]` serving route; login and reset-password read session state within public flows); 9 Prisma models (User…role, Account, Contact, Lead, Activity, Event, Opportunity, SavedReport, Setting); recharts 2.15 chart family; CSV/PDF export (jspdf + html2canvas-pro); file upload + serving; global search; PWA manifest + per-route OG metadata; response-header surface; axe-core in the e2e stack.
- **Auth (deepest of the family):** scrypt hashing; HMAC cookie with a **tokenVersion revocation dimension** (password reset evicts all pre-reset sessions at the DB seam); `timingSafeEqual` verification plus a **login timing equalizer** (miss branch burns the same scrypt work); **fail-hard in production** on missing/short `AUTH_SECRET` (forgeable-session class closed, session-169); reset tokens **hashed at rest** (SHA-256), 60-min TTL, atomic single-use consumption, no-enumeration forgot-password; per-route rate limits (login 10, signup 10, resend 5, verify 20, forgot 10, reset 10, upload 20 per IP/15 min) keyed on a deploy-declared proxy-hop depth (`NEO_PROXY_HOPS`, fails closed). Verified by full read of `src/lib/auth.ts` — every number confirmed at line level, plus the session-170 boot-gate (the server refuses to boot on a missing/short `AUTH_SECRET` in production, enforced via `src/instrumentation.ts` → `src/lib/boot-env.ts`).
- **Validation:** Zod 4 at every JSON boundary via `src/lib/schemas.ts` (716 ln) + `parseBody()` composing a **bounded reader** (Content-Type CSRF gate, declared-length fast-path, chunked-stream counter). The file's own header credits zero-balance as pattern donor — the family deliberately cross-pollinates.
- **Tooling:** the only repo with `gate` and `gate:full` scripts (full gate + 5 drift sweeps + interior census as one command), `lint --max-warnings 0`, DB census script.
- **Documentation:** largest corpus — SKILL.md 12,378 lines (v1.171.0; 16 core sections + ~136 session layers); AGENTS.md 9,683 lines (~90 per-session sections; every count claim is *test-gated* by `tests/docs-counts.test.ts` — a stale count anywhere fails `bun run test`). Current documented counts: 2,717 unit / 192 e2e / 14 smoke. Extraordinary traceability, but **agent-context bloat** (see findings).
- **Costs:** 9 capitalized `.jsx` route aliases + 2 marketing aliases (intentional, documented parity shims — see §10 before flagging as dead code); recharts 2.x (v3 exists). The three costs flagged at evaluation time — two lockfiles, `ignoreBuildErrors: true`, `noImplicitAny: false` — were **all retired within hours of this report by session-174** (single `bun.lock`; the build is now the type gate; full TS strictness), which is literally this report's §9.2 graft list (the commit message cites this report and the vendored `skills/web-application/SKILL.md` by name).

### 4.2 zero-balance — "the cleanest engineering posture"
- **Shape:** budget planner (net-zero rule) — 7 server-component pages wrapping one client `AppShell`; 5 Prisma models; 15 API route files (23 handlers), including a full **email-verification funnel** (`/auth/verify-email` + `/auth/resend` — codes delivered in-response in demo mode, no disable knob, no code TTL); recharts 3.10 donut (its only chart type); the 3-level drill-down dashboard (section → category → subcategory → item); the **calculator contract** (every line-item mutation triggers server-side recalculation of the parent item — domain-logic-in-one-place done right); **integer-cent money arithmetic at every aggregation boundary** (ADR-004: amounts are stored and exchanged as decimals — Prisma `Float` columns — but every sum converts to integer cents first via `money.ts`, so IEEE-754 drift can never reach a total).
- **Best-in-family specifics:** the **first repo without `ignoreBuildErrors`** (the production build *is* the type gate; neo-crm joined it in session-174); npm scripts pin `DATABASE_URL` inline and strip it (`env -u`) for Prisma CLI — environment discipline as code (empirically load-bearing: under this validation environment's shell-exported `DATABASE_URL`, zb's full pipeline ran 35/35 untouched while the undefended sibling collapsed — see P-6); the seed routes through the db-path seam (`resolveProcessDatabaseUrl`) like the app; zod 4 at every boundary (`validation.ts`) with genuinely careful schemas (real-calendar-date refinement, empty-string-vs-optional normalization for native date inputs; note its PATCH semantics are two-state — absent = no-write, `""` elided, `null` rejected — the three-state PUT helpers live in neo-crm's `schemas.ts`); `@axe-core/playwright` in the e2e stack behind a two-gate design (structural + palette-provenance); a lean doc corpus (second-smallest — pm's is smaller); ADR-001…007 in the PAD.
- **Costs:** smallest unit suite (108 checks — though the strongest e2e-to-surface ratio: **309** e2e checks; the 288 figure in parts of zb's own doc set is stale); no license; no teams/RBAC; single chart type; **no password-reset funnel at all** (the login card's forgot state renders a message-only "reset unavailable" notice — no API route, no token, no page); the OTP code is stored plaintext at rest and returned in-response with **no disable knob and no TTL** (Z-6); a stray `project-management_SKILL.md` committed at the repo root, byte-identical to pm's own (Z-5); `z-ai-web-dev-sdk` declared as a runtime dependency despite scripts-only (parity-probe) usage; npm-documented but bun-executed runtime scripts (mixed posture — informational).

### 4.3 digma — "the deepest testing culture, wrong shape for this purpose"
- **Shape:** Figma-like canvas editor — DOM-element canvas, layers/properties panels, AI assistant (degrade-not-fail), teams, PNG export; 5 Prisma models; **zero charting** (0 recharts references; dashboards are stat/project cards).
- **Best-in-family specifics:** **fully strict TypeScript** (alongside pm and zb — digma is the only one of the four that ever needed a strictness *repair*: session-79 removed a leftover `noImplicitAny` contradiction on 2026-10-05); the largest test investment (2,501 unit checks across 242 files — including 235 files under `tests/`; ⚠ the suite presumes the `cp .env.example .env` bootstrap, see D-7, and post-evaluation session-180 added the README prerequisite line — plus 262 e2e checks across 39 spec files and a 73-check smoke suite, the smoke re-executed 73/73 at validation); the most honest Known-Issues register of the family (a HIGH self-reported finding on its own forgot-password default; plaintext-token-at-rest disclosure; the no-revocation-list trade-off); ADR-001…014 plus 002a/004a (16 ADRs); 3,120-line PAD; env knobs for prod-hardening (`DIGMA_DISABLE_IN_APP_OTP/RESET/AI_LLM`, `DIGMA_PROXY_HOPS`, plus `DIGMA_SITE_URL` and the `DIGMA_REPO_ROOT` db-path escape hatch).
- **Costs:** **no charting** (decisive against rank 2 for this evaluation's purpose); two lockfiles — but documented as intentional (AGENTS.md: `bun.lock` canonical, `package-lock.json` the operator-committed npm mirror, S171-A); stray sibling SKILL files committed (`project-management_SKILL.md`, `scandihaven_SKILL.md`); 401 MB `.git` / 148 MB `docs/` (469 session logs + 155 remediation plans); HIGH-severity default (in-app reset URL in response body) documented but shipped as default; `AUTH_SECRET` is warn-only in production (the dev fallback secret is used — unlike neo-crm's fail-hard).

### 4.4 project-management (ORBITAL) — "lean, disciplined, exotic"
- **Shape:** PM workspace where an AI agent drafts task plans; 8 Prisma models with an ActivityLog narrating every mutation; a degrade-never-fail AI planning pipeline with a sanitizer seam.
- **Architecture (the differentiator — and the problem):** a **SPA-in-one-page** pattern — every view path (`/goals`, `/my-tasks`, `/activity`…) is a `rewrites()` onto a single workspace page with client-side view switching via a tested `router.ts` seam. Elegant for its parity goal, but as a *general template* it inverts Next.js conventions (no per-view routes, no layout-level code splitting per view) and transfers poorly to "any given web application."
- **Costs:** hand-rolled validation by CLAUDE.md TypeScript-standards rule + v1.2 dependency prune ("do not introduce Zod halfway" — CLAUDE.md:57; Zod was explicitly removed in the v1.2 prune — internally consistent but the weakest input-hardening of the family); oldest dependency generation (Next 16.1, React 19.0; Prisma declared `^6.11.1` but lockfile-resolved to 6.19.3); smallest doc corpus; `ignoreBuildErrors: true`; the only sibling with a legacy `tailwind.config.ts` (shadcn HSL tokens + tailwindcss-animate, kept deliberately per CLAUDE.md:62); no license; no charting (goals use a hand-rolled SVG progress ring; the date-card ring is a plain div). **New at re-validation (P-6): no database-environment discipline** — `db:push`/`db:seed` carry no `env -u` guard or inline pin, and the seed bypasses the db-path seam (direct `PrismaClient`), so a shell-exported `DATABASE_URL` silently redirects the database outside the repo (reproduced: smoke 12/30 → 30/30 after `unset`).

---

## 5. Dimension A — Code Quality (30%)

| Sub-criterion | digma | neo-crm | project-management | zero-balance |
|---|---|---|---|---|
| TypeScript strictness | **strict, no loosening** | strict + `noImplicitAny: false` *(at evaluation; retired same-day by session-174)* | **strict, no loosening** (never had the flag — F-6 corrected) | **strict, no loosening** (never had the flag — F-6 corrected) |
| Build-time type gate | `ignoreBuildErrors` (manual typecheck) | **build is the gate** (session-174) | `ignoreBuildErrors` (manual typecheck) | **build is the gate** |
| Unit test depth (executed) | **2,501** | **2,717** | 138 | 108 |
| Lint discipline | `eslint .` | `eslint . --max-warnings 0` | `eslint .` | `eslint .` |
| Validation layer | hand-rolled (`validation.ts` + per-route clamps) | **Zod 4 everywhere** (`schemas.ts` + `parseBody`) | hand-rolled (CLAUDE.md rule + v1.2 prune) | **Zod 4 everywhere** (`validation.ts`) |
| Why-comments / traceability | exemplary | exemplary | exemplary | exemplary |
| Repo hygiene | two lockfiles (documented intentional, S171-A); stray sibling SKILL files | single `bun.lock` (session-174 retired package-lock.json); 9.7k-line AGENTS.md | cleanest doc corpus, but the only sibling with a legacy `tailwind.config.ts` | stray `project-management_SKILL.md` at root |
| Known-issues honesty | **best** (self-reported HIGH) | good (session layers) | good | good |

**Reading:** all four are far above the norm for AI-generated codebases — none contains TODO-slop, dead commented code, or placeholder values in app code; comments consistently explain *why* with session-numbered provenance; error handling follows the envelope discipline (never throw across a handler boundary). The quality axis differentiates on strictness policy (at evaluation only neo-crm carried a loosened `noImplicitAny` — a mis-scoped claim in the original F-6 row, corrected in §10.1 — and it closed the gap itself in session-174; zb led build-gating with neo-crm joining it in session-174; neo-crm leads on validation + lint ceiling) and hygiene (zb's corpus is second-cleanest with one stray file; digma the most cluttered). This dimension is the closest of the three; the ranking differences come from the other two dimensions.

---

## 6. Dimension B — Feature Completeness for Production Deployment (40%)

Purpose-weighted: authentication depth, dashboard quality, charting, plus the surrounding production surface.

| Capability | digma | neo-crm | project-management | zero-balance |
|---|---|---|---|---|
| Email+password auth (register/login/logout/me) | ✅ | ✅ | ✅ | ✅ |
| Email verification (OTP + resend) | ✅ | ✅ | — | ✅ (in-response delivery, no disable knob, no TTL) |
| Password reset funnel | ✅ (in-app URL default ⚠) | ✅ (hashed tokens, single-use, no-enumeration) | — (none) | — (message-only "reset unavailable" notice; no API route, no token, no page) |
| Session revocation (post-reset eviction) | ✅ tokenVersion (origin) | ✅ tokenVersion | — | — |
| Rate limiting (auth routes) | ✅ + proxy-hops env | ✅ per-route limits + proxy-hops | ✅ (10/15 min) | ✅ |
| Production secret enforcement | dev-fallback warn | **fail-hard in prod** | dev-fallback | dev-fallback warn |
| RBAC / roles | — (no User.role; TeamMember.role is a job title) | role field + owner FKs across entities | team members (human/agent) | — |
| Dashboard | project stat cards | **KPI grid + sparklines + pipeline charts + export** | 2×2 stat/goal/activity grid | hero + drill-down + stat cards + donut |
| **Charting** | **none** | **7 wrapper components, 6 consuming surfaces** | none (CSS rings) | donut (recharts 3) |
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

*Score movements at re-validation (all Verified, reasoning in §13): neo-crm quality 8.0→8.5 (the three flagged costs — two lockfiles, `ignoreBuildErrors`, `noImplicitAny: false` — were all retired by session-174 within hours of the original evaluation, exactly the §9.2 graft list); zero-balance features 7.5→8.0 (the email-verification funnel exists and was wrongly denied in the original §6 table); project-management architecture 7.0→6.5 (P-6: the reproduced database-environment fragility). digma unchanged.*

**Sensitivity notes (stated plainly):**
- neo-crm is #1 under any plausible weighting — it leads or ties every dimension that matters for this purpose, and the same-day session-174 hardening widened the lead.
- zero-balance vs digma widened from a 0.05 tie to 0.25: re-validation confirmed zb's email-verification funnel (feature credit) and empirically proved its env-discipline scripts are load-bearing, while digma's posture is unchanged. If your future apps will never chart, or you weight test-suite size above built-in charting, they remain close enough to swap.
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
6. **Secrets at rest** — hash OTP codes and reset tokens (neo-crm already hashes reset tokens; digma self-reports plaintext at rest — and zero-balance's OTP is also plaintext at rest, with in-response delivery and no disable knob, Z-6). *(Medium)*
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
| F-4 | **In-app OTP / reset-link delivery by default** | digma/neo-crm return codes/URLs in response bodies unless `*_DISABLE_IN_APP_*` set; zero-balance returns the OTP code in-response with **no disable knob and no code TTL** (register/resend routes, code-verified) | Account-takeover class if deployed as-is publicly | **High** (default posture) | Verified (documented + code-read; digma self-reports its own as HIGH) |
| F-5 | `ignoreBuildErrors: true` | `next.config.ts` — digma and pm only (neo-crm retired it in session-174, post-evaluation; zb never had it) | Type errors do not fail builds; relies on manual `typecheck` | Medium | Verified |
| F-6 | ~~`noImplicitAny: false`~~ **— corrected at re-validation** | Only neo-crm ever set it (retired by session-174, post-evaluation). pm and zb never did — both tsconfigs are `strict: true` with the flag unset since their initial commits. The original claim here repeated pm's own *stale* PAD/CLAUDE.md row over the code — the family's code-wins rule, violated. All four repos are now fully strict | No longer applicable | **Retired (correction)** | Verified (`git log -- tsconfig.json` ×4) |
| F-7 | **Repo bloat**: 194–201 MB vendored `skills/` + 4.9–148 MB `docs/` session archives (digma: 469 session logs + 155 remediation plans) + screenshots + a root `worklog.md` (204–6,820 lines) in every repo | `du`, `git ls-files` counts | Clone/agent-context cost; not app code; template noise | Medium | Verified |
| F-8 | `db push --accept-data-loss` as primary schema workflow | `package.json` scripts | Data-loss foot-gun; migrations underused | Medium | Verified |
| F-9 | No observability layer | console logs, `tee dev.log/server.log` | Production diagnosability gap | Medium | Verified |
| F-10 | No email transport integration | docs; disable-knob envs exist | Production auth flows incomplete | Medium | Verified |
| F-11 | Zero community (0 stars/forks, single author, 3–5 weeks old) | GitHub API | Maintenance-risk factor for foundation adoption | Informational | Verified |

### 10.2 digma

| # | Finding | Evidence | Impact | Severity | Confidence |
|---|---|---|---|---|---|
| D-1 | Forgot-password returns live reset URL in response body by default | PAD §10 Known Issues (self-reported HIGH); route code documented | Unauthenticated capture of reset link | **High** (as-shipped default) | Verified (documented, self-reported) |
| D-2 | **No charting capability** | 0 recharts references in `src/`; no chart dependency | Disqualifying for this evaluation's purpose | **High (purpose-fit)** | Verified |
| D-3 | Reset tokens and OTP codes stored recoverable (plaintext) in User row | PAD §10 (B82-L6, self-reported) | DB-compromise → account takeover within TTL window | Medium | Verified (documented) |
| D-4 | Stray sibling SKILL files committed (`project-management_SKILL.md`, `scandihaven_SKILL.md`) | root `git ls-files` | Template confusion; hygiene | Low | Verified |
| D-5 | Two lockfiles (`bun.lock` + `package-lock.json`) | root listing; documented as intentional (AGENTS.md: bun.lock canonical, package-lock.json the operator-committed npm mirror, S171-A — direct deps verified coherent, transitive layer registered unverified) | Non-reproducible installs across package managers (mitigated by documentation) | Low | Verified |
| D-6 | 401 MB `.git`, 148 MB `docs/` (469 session logs + 155 remediation plans, screenshot archives) | `du` | Clone weight; history noise | Low | Verified |
| D-7 | **Unit gate presumes a bootstrapped `.env`** — new at re-validation | `tests/lows-s99.test.ts` does `readFileSync(ROOT/.env)`: ENOENT on a pristine clone (2,475 pass + 1 file fail); 2,501/2,501 green after `cp .env.example .env`. Session-180 (post-evaluation) added a README `.env`-prerequisite line | Fresh-clone `bun run test` fails before the documented bootstrap step | Low | Verified (executed both ways) |

### 10.3 neo-crm

| # | Finding | Evidence | Impact | Severity | Confidence |
|---|---|---|---|---|---|
| N-1 | AGENTS.md 9,683 lines; SKILL.md 12,378 lines (v1.171.0), largely per-session narrative | `wc -l` | Agent-context bloat; signal-to-noise decay for future agents (the family's own leaner repos prove the same discipline fits in ~1,300 lines) | Medium | Verified |
| N-2 | 11 capitalized `.jsx` route alias files alongside lowercase `.tsx` pages | `git ls-files` + file header comments | **Initially suspected dead code — disproven on read:** intentional, documented parity aliases (reference app links to `/Dashboard`); `.jsx` extension deliberately avoids TS1149 casing collision. Cosmetic exoticism only | Informational | Verified (file contents read) |
| N-3 | recharts 2.15 (v3 is current; sibling zb runs 3.10) | `package.json` | Older chart major; migration debt | Low | Verified |
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
| P-6 | **No database-environment discipline** — new at re-validation: `db:push`/`db:seed` carry no `env -u` guard or inline pin, and `prisma/seed.ts` bypasses the db-path seam (direct `PrismaClient`; zb's and neo-crm's seeds route through the shared resolver) | Reproduced both ways: under a shell-exported `DATABASE_URL`, pm's push/seed silently wrote outside the repo while its smoke server (pinned relative URL) read an empty in-repo db → login 500s (P2021) → **smoke 12/30**; clean shell → **30/30**. zb under the same polluted shell: 35/35 (immune by design); digma's smoke refuses loudly; neo's smoke pins its own throwaway db | A polluted parent shell (CI runner, workspace env) silently breaks the gate — the exact trap the family's own DATABASE_URL contract documents | **Medium** | Verified (executed, both ways) |

### 10.5 zero-balance

| # | Finding | Evidence | Impact | Severity | Confidence |
|---|---|---|---|---|---|
| Z-1 | No license | root listing / GitHub API | Same as F-1 | **High (legal)** | Verified |
| Z-2 | Smallest unit suite (108 checks / 9 files) | executed run | Pure-seam coverage thin relative to siblings | Low | Verified |
| Z-3 | Single chart type (donut) | 1 recharts-consuming file | Charting present but shallow vs neo-crm | Low (purpose-fit) | Verified |
| Z-4 | No teams / multi-entity ownership | 5-model schema, userId-only relations | Fine for its domain; limits as generic template | Informational | Verified |
| Z-5 | Stray `project-management_SKILL.md` committed at repo root (byte-identical to pm's own file; unreferenced by the app) — noted in Appendix B at evaluation but missing from this register, an internal-consistency omission of the original report | root listing; `diff` | Template confusion; hygiene | Low | Verified |
| Z-6 | OTP stored plaintext at rest (`verificationCode` raw in the User row) and delivered in-response (`devCode` in register/resend bodies) with **no disable knob and no code TTL** — `MAX_CODE_ATTEMPTS=5` is the only guard | `prisma/schema.prisma:30`; `src/lib/verification.ts`; register/resend routes | Same DB-compromise → account-takeover class as digma's self-reported B82-L6, plus no production kill-switch | Medium | Verified (code-read) |
| Z-7 | `z-ai-web-dev-sdk` declared as a runtime dependency but used only by `scripts/parity-probes/*.mjs` (VLM parity sweeps); documented manager is npm while `start`/`db:seed`/Playwright webServer/smoke boot via bun | `package.json`; scripts census | Dependency-classification drift; mixed-runtime posture | Informational | Verified |

### 10.6 Positive findings worth recording (no inflation — these are real)

- All four repos **build, typecheck, and pass their entire unit suites from a clean clone** in this environment — executed and observed (§2.2; digma after its documented `.env` bootstrap, D-7). This is rare even among human-maintained templates.
- **All four smoke suites now executed green under their documented invocations** (73/14/30/35) — the original report had these as documented-only.
- No secrets committed anywhere (`.env.example` only, `.env` gitignored) — Verified across all four.
- The `db-path` seam (solving the standalone-server `process.chdir` + Prisma relative-URL ambiguity) is designed, implemented, and **pinned by fixture tests in all four repos** — a genuinely production-grade solution to a real Next.js standalone deployment trap.
- **The DATABASE_URL environment-discipline hierarchy is real and load-bearing** — new at re-validation: under this validation environment's own shell-exported `DATABASE_URL` (an unplanned natural experiment), zero-balance's `env -u` + inline-pin scripts ran its full smoke 35/35 untouched, digma's smoke refused loudly per its documented contract, neo-crm's smoke pinned its own throwaway database — and project-management, the one repo without the discipline, collapsed to 12/30 until the shell was cleaned (P-6). The family's documented contract is not documentation theater; it is the difference between green and red. (Verified, executed)
- Comment quality is exemplary family-wide: nearly every non-obvious decision carries a *why* comment with session-numbered provenance, and every doc states "when code and this document disagree, the code wins — update the doc in the same commit."

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
| 9 | Suspicion checks: neo-crm capitalized `.jsx` routes; pm/zb `noImplicitAny`; zb money model; zb email-verification funnel | file reads, `git log -- tsconfig.json` ×4, schema reads, route inventory | `.jsx` aliases = intentional (kept); pm/zb **never** had `noImplicitAny: false` (F-6 corrected); zb money = decimal storage + cents-at-aggregation (§4.2 corrected); zb verification funnel **exists** (§6 corrected) |
| 10 | Doc corpora sizes + versions | `wc -l` + version headers across all key docs | As reported in §2.1/§4 |
| 11 | Repo activity & metadata | `git log` census + GitHub API | As reported in §2.1 |
| 12 | E2E suites | **not executed** (no browser binaries) | Documented counts (Reasoned): digma 262 / 39 files · neo 192 / 11 · pm 115 / 10 · zb 309 / 23 |
| 13 | Provenance of the validated documents | `diff` vs `neo-crm/skills/web-application{,-engineering}/` | All four validation targets are byte-identical to copies vendored inside neo-crm — session-174 cites them as its rotation trigger |

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
| Charts | — | recharts 2.15 (7 wrappers) | — (hand-rolled SVG ring) | recharts 3.10 (donut) |
| Export | PNG | CSV (dashboard) + PDF (reports) | — | — |
| Unit checks (executed) | 2,501 | 2,717 | 138 | 108 |
| E2E checks (documented) | 262 | 192 | 115 | 309 |
| Smoke checks (executed) | 73 | 14 | 30 | 35 |
| `ignoreBuildErrors` | yes | **no** (retired s174) | yes | **no** |
| `noImplicitAny: false` | never | only repo that ever had it (retired s174) | never | never |
| License | none | **MIT** | none | none |
| SKILL.md size | 723 ln (v1.158.0) | 12,378 ln (v1.171.0) | 739 ln (v1.0.0) | 1,350 ln (v1.0.0) |

## Appendix B — Documentation set examined per repo

`AGENTS.md` · `CLAUDE.md` · `Project_Architecture_Document.md` · `README.md` · `digma_SKILL.md` / `neo-crm_SKILL.md` / `project-management_SKILL.md` / `zero-balance_SKILL.md` (per the evaluation brief) · `package.json` · `prisma/schema.prisma` · `next.config.ts` · `tsconfig.json` · `.env.example` · key `src/lib/*` seams · chart/dashboard components · `scripts/smoke-test.sh` · root-level hygiene census. digma additionally carries stray `project-management_SKILL.md` + `scandihaven_SKILL.md` (noted D-4); zero-balance carries a stray `project-management_SKILL.md` (now also registered as Z-5). The file the evaluation brief calls `zero-balance.md` is actually `zero-balance_SKILL.md` in the repo.

---

## 13. Validation & Corrections Log (v1.1 — 2026-10-23 re-validation)

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
