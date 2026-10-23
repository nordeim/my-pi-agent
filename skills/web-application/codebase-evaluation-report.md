# Comparative Evaluation Report — Four Web-Application Codebases

**Candidates:** `nordeim/digma`, `nordeim/neo-crm`, `nordeim/project-management` (ORBITAL), `nordeim/zero-balance`
**Evaluation purpose:** suitability as a template / foundational codebase to scaffold **any** web application requiring **authentication, dashboard, and charting**
**Evaluation date:** 2026-10-23 (UTC+8)
**Method:** documentation-first audit (AGENTS.md → CLAUDE.md → Project_Architecture_Document.md → `*_SKILL.md` → README), followed by code-level verification and executed build/test verification, per audit discipline (findings separated from fixes, severity taxonomy, evidence-backed confidence labels: **Verified** = executed/observed, **Reasoned** = inferred from code read in full, **Assumed** = stated assumption).

---

## 1. Executive Summary

**Verdict — use `neo-crm` as the foundational template.** It is the most evolved member of the family and the only candidate that fully covers the three required legs (auth, dashboard, charting) at near-production depth: a revocation-capable session-auth core, a KPI/chart dashboard, a 7-type recharts wrapper library, Zod validation at every API boundary, CSV/PDF export, file upload, search, an a11y layer (axe-core in e2e), the family's only open-source **license (MIT)**, and a single-command quality gate (`bun run gate:full`). It also verified green from a clean clone in this environment (install → prisma → typecheck → build → 2,668 unit tests).

**Final ranking (weighted: code quality 30% / feature completeness 40% / architectural robustness 30%):**

| Rank | Codebase | Quality /10 | Features /10 | Architecture /10 | **Weighted** |
|---|---|---|---|---|---|
| **1** | **neo-crm** | 8.0 | 9.0 | 8.5 | **8.55** |
| **2** | **zero-balance** | 8.0 | 7.5 | 8.0 | **7.80** |
| **3** | **digma** | 8.5 | 7.0 | 8.0 | **7.75** |
| **4** | **project-management** | 7.0 | 6.0 | 7.0 | **6.60** |

Rank 2 vs 3 is a near-tie (0.05) and was decided on purpose-fit: zero-balance ships all three required legs (Zod boundary, donut-chart dashboard, build-gated types), while digma — despite the best test suite and strictest TypeScript of the family — **ships no charting library at all** (0 recharts references in `src/`; it is a canvas editor, not a charting app).

**Family-wide caveats (apply to all four, before any production deployment):** no hosted CI/CD (local gate only), no Docker artifacts, SQLite dev-default with per-process in-process rate limiting (single-node posture), in-app OTP/reset-link delivery enabled by default (demo posture; disable knobs exist), no observability layer, and — outside neo-crm — **no license**, which legally blocks template reuse until the owner adds one. See §10 for the full register.

---

## 2. Scope, Method & Evidence Base

### 2.1 What was examined

| Repo | Commits | First→last commit (UTC) | Tracked files | Cloned size | License | Stars/Forks |
|---|---|---|---|---|---|---|
| digma | 391 | 2026-09-27 → 2026-10-23 | 5,806 | 762 MB | **none** | 0 / 0 |
| neo-crm | 446 | 2026-09-29 → 2026-10-23 | 4,114 | 425 MB | **MIT** | 0 / 0 |
| project-management | 121 | 2026-09-17 → 2026-10-22 | 3,083 | 329 MB | **none** | 0 / 0 |
| zero-balance | 268 | 2026-10-02 → 2026-10-23 | 4,374 | 357 MB | **none** | 0 / 0 |

All four are single-author, actively developed (pushed within the last 24 h of evaluation), zero-community projects. Each carries a ~195 MB vendored personal `skills/` library and 5–146 MB of `docs/` session logs/screenshots that are **not app code** — a template-relevant bloat finding (§10).

**Documentation read (in full or in targeted full-section passes):** `AGENTS.md`, `CLAUDE.md`, `Project_Architecture_Document.md`, `digma_SKILL.md` (720 ln), `neo-crm_SKILL.md` (12,357 ln — core §1–§16 in full, session layers via heading census), `project-management_SKILL.md` (739 ln, §1–§16 in full), `zero-balance_SKILL.md` (1,350 ln, §1–§9 + lesson census), all four READMEs, all four `package.json`, `prisma/schema.prisma`, `next.config.ts`, `tsconfig.json`, `.env.example`, `src/lib/auth.ts` (neo-crm, in full), `src/components/charts/charts.tsx` (neo-crm), `src/lib/validation.ts` (zero-balance), `src/lib/schemas.ts` (neo-crm), `scripts/smoke-test.sh` (zero-balance), route-tree inventories per repo.

### 2.2 What was executed (verification ledger)

| Check | digma | neo-crm | project-management | zero-balance |
|---|---|---|---|---|
| `bun install` (clean clone) | ✅ pass | ✅ pass | ✅ pass | ✅ pass |
| `bunx prisma generate` | ✅ pass | ✅ pass | ✅ pass | ✅ pass |
| `bun run typecheck` | ✅ pass (7 s) | ✅ pass (8 s) | ✅ pass (5 s) | ✅ pass (6 s) |
| `bun run build` (standalone) | ✅ pass (17 s), `server.js` produced | ✅ pass (27 s), `server.js` produced | ✅ pass (18 s), `server.js` produced | ✅ pass (24 s), `server.js` produced |
| `bun run test` (Vitest) | ✅ **2,464 / 2,464** (239 files) | ✅ **2,668 / 2,668** (135 files) | ✅ **138 / 138** (15 files) | ✅ **108 / 108** (9 files) |
| Secrets scan (`git ls-files`, env files) | only `.env.example` tracked | only `.env.example` tracked | only `.env.example` tracked | only `.env.example` tracked |
| Playwright e2e | **not executed** (no browser binaries in this environment) — suites documented: 262 checks / 39 spec files | not executed — 11 spec files | not executed — 115 checks / 10 spec files | not executed — 288 checks / 23 spec files |
| API smoke suite | not executed (73 checks documented) | not executed (script present) | not executed (30 checks documented) | not executed (35 steps documented) |
| Runtime behavior / production deploy / PostgreSQL path | not executed | not executed | not executed | not executed |

All "not executed" rows are reported at **Reasoned** confidence throughout this document; executed rows are **Verified**. Unit-test and build claims above are Verified in this environment on 2026-10-23.

---

## 3. Family DNA (shared context you must know before reusing any of them)

All four repos are siblings from one author and one methodology, which makes their *differences* the real signal:

- **Genesis:** each is a deliberate "superset clone" of a Base44 reference app (design tool / CRM / PM workspace / budget planner), built and continuously parity-remediated through AI-agent sessions (100–450+ commits in 3–5 weeks), with session logs, remediation plans, and pixel-measurement archives committed under `docs/`.
- **Stack (uniform):** Next.js 16 App Router with `output: "standalone"` + pinned `outputFileTracingRoot`, React 19, TypeScript 5.9, Tailwind CSS 4 (CSS-first `@theme`, no JS config), shadcn/ui on Radix, one Zustand 5 store for all server state, Prisma 6 + SQLite (dev default), custom scrypt + HMAC-SHA256 stateless cookie sessions (no NextAuth, no JWT library), z-ai-web-dev-sdk for optional AI features with deterministic fallbacks, Vitest 5 + Playwright 1.6x + a bash API smoke suite, Bun runtime (npm-compatible).
- **Engineering culture (uniform and genuinely strong):** three-tier verification with an isolated self-resetting e2e database; a strict local gate (`lint → typecheck → test → build → smoke → e2e`); "when code and docs disagree, the code wins — fix the doc in the same commit"; why-comments with session-numbered rationale on nearly every non-obvious decision; honest Known-Issues registers.
- **Uniform gaps:** no hosted CI ("the local gate is the only gate" — stated verbatim in all four AGENTS.md), no Docker/compose files, no observability stack, per-process rate limiting, in-app delivery of OTP/reset links by default.

**Implication for template selection:** pick the *most evolved sibling for the target shape* (a multi-entity business app with dashboard + charts ⇒ neo-crm), then graft specific superior practices from the others (§9.2).

---

## 4. Candidate Profiles

### 4.1 neo-crm — "the most complete business-app implementation"
- **Shape:** full CRM — marketing route group + app route group; 15 pages, 29 API route files (19 session-gated, 10 public-by-design with rate limits); 9 Prisma models (User…role, Account, Contact, Lead, Activity, Event, Opportunity, SavedReport, Setting); recharts 2.15 chart family; CSV/PDF export (jspdf + html2canvas-pro); file upload + serving; global search; PWA manifest + per-route OG metadata; response-header surface; axe-core in the e2e stack.
- **Auth (deepest of the family):** scrypt hashing; HMAC cookie with a **tokenVersion revocation dimension** (password reset evicts all pre-reset sessions at the DB seam); `timingSafeEqual` verification plus a **login timing equalizer** (miss branch burns the same scrypt work); **fail-hard in production** on missing/short `AUTH_SECRET` (forgeable-session class closed, session-169); reset tokens **hashed at rest** (SHA-256), 60-min TTL, atomic single-use consumption, no-enumeration forgot-password; per-route rate limits (login 10, signup 10, resend 5, verify 20, forgot 10, reset 10 per IP/15 min) keyed on a deploy-declared proxy-hop depth (`NEO_PROXY_HOPS`, fails closed). Verified by full read of `src/lib/auth.ts`.
- **Validation:** Zod 4 at every JSON boundary via `src/lib/schemas.ts` (716 ln) + `parseBody()` composing a **bounded reader** (Content-Type CSRF gate, declared-length fast-path, chunked-stream counter). The file's own header credits zero-balance as pattern donor — the family deliberately cross-pollinates.
- **Tooling:** the only repo with `gate` and `gate:full` scripts (full gate + 5 drift sweeps + interior census as one command), `lint --max-warnings 0`, DB census script.
- **Documentation:** largest corpus — SKILL.md 12,357 lines (v1.168) including ~90 per-session "layer" sections; AGENTS.md 9,421 lines. Extraordinary traceability, but **agent-context bloat** (see findings).
- **Costs:** 9 capitalized `.jsx` route aliases + 2 marketing aliases (intentional, documented parity shims — see §10 before flagging as dead code); two lockfiles committed (`bun.lock` + `package-lock.json`); recharts 2.x (v3 exists); `ignoreBuildErrors: true` (manual typecheck gate); `noImplicitAny: false`.

### 4.2 zero-balance — "the cleanest engineering posture"
- **Shape:** budget planner (net-zero rule) — 7 server-component pages wrapping one client `AppShell`; 5 Prisma models; 13 API route files (21 handlers); recharts 3.10 donut; 3-level drill-down dashboard; the **calculator contract** (every line-item mutation triggers server-side recalculation of the parent item — domain-logic-in-one-place done right); integer-cents money end-to-end (`money.ts` format boundary).
- **Best-in-family specifics:** the **only repo without `ignoreBuildErrors`** (the production build *is* the type gate); npm scripts pin `DATABASE_URL` inline and strip it (`env -u`) for Prisma CLI — environment discipline as code; zod 4 at every boundary (`validation.ts`) with genuinely careful schemas (real-calendar-date refinement, empty-string-vs-optional normalization for native date inputs); `@axe-core/playwright` in the e2e stack; the smallest doc corpus (no session-layer bloat); ADR-001…007 in the PAD.
- **Costs:** smallest unit suite (108 checks — though the strongest e2e-to-surface ratio: 288 e2e checks); no license; no teams/RBAC; single chart type; `noImplicitAny: false`.

### 4.3 digma — "the deepest testing culture, wrong shape for this purpose"
- **Shape:** Figma-like canvas editor — DOM-element canvas, layers/properties panels, AI assistant (degrade-not-fail), teams, PNG export; 5 Prisma models; **zero charting** (0 recharts references; dashboards are stat/project cards).
- **Best-in-family specifics:** **fully strict TypeScript** (`strict: true` with no `noImplicitAny` loosening — the only one); the largest test investment (2,464 unit checks across 239 files — including 232 files under `tests/` — plus 262 e2e checks across 39 spec files and a 73-check smoke suite); the most honest Known-Issues register of the family (a HIGH self-reported finding on its own forgot-password default; plaintext-token-at-rest disclosure; the no-revocation-list trade-off); ADR-001…013+004a; 3,114-line PAD; env knobs for prod-hardening (`DIGMA_DISABLE_IN_APP_OTP/RESET/AI_LLM`, `DIGMA_PROXY_HOPS`).
- **Costs:** **no charting** (decisive against rank 2 for this evaluation's purpose); two lockfiles; stray sibling SKILL files committed (`project-management_SKILL.md`, `scandihaven_SKILL.md`); 390 MB `.git` / 146 MB `docs/`; HIGH-severity default (in-app reset URL in response body) documented but shipped as default.

### 4.4 project-management (ORBITAL) — "lean, disciplined, exotic"
- **Shape:** PM workspace where an AI agent drafts task plans; 8 Prisma models with an ActivityLog narrating every mutation; a degrade-never-fail AI planning pipeline with a sanitizer seam.
- **Architecture (the differentiator — and the problem):** a **SPA-in-one-page** pattern — every view path (`/goals`, `/my-tasks`, `/activity`…) is a `rewrites()` onto a single workspace page with client-side view switching via a tested `router.ts` seam. Elegant for its parity goal, but as a *general template* it inverts Next.js conventions (no per-view routes, no layout-level code splitting per view) and transfers poorly to "any given web application."
- **Costs:** hand-rolled validation by ADR ("do not introduce Zod halfway" — internally consistent but the weakest input-hardening of the family); oldest dependency generation (Next 16.1, Prisma 6.11, React 19.0); smallest doc corpus; `ignoreBuildErrors: true`; no license; no charting (CSS progress rings only).

---

## 5. Dimension A — Code Quality (30%)

| Sub-criterion | digma | neo-crm | project-management | zero-balance |
|---|---|---|---|---|
| TypeScript strictness | **strict, no loosening** | strict + `noImplicitAny: false` | strict + `noImplicitAny: false` | strict + `noImplicitAny: false` |
| Build-time type gate | `ignoreBuildErrors` (manual typecheck) | `ignoreBuildErrors` (manual typecheck) | `ignoreBuildErrors` (manual typecheck) | **build is the gate** |
| Unit test depth (executed) | **2,464** | **2,668** | 138 | 108 |
| Lint discipline | `eslint .` | `eslint . --max-warnings 0` | `eslint .` | `eslint .` |
| Validation layer | hand-rolled (`validation.ts` + per-route clamps) | **Zod 4 everywhere** (`schemas.ts` + `parseBody`) | hand-rolled (ADR) | **Zod 4 everywhere** (`validation.ts`) |
| Why-comments / traceability | exemplary | exemplary | exemplary | exemplary |
| Repo hygiene | two lockfiles; stray sibling SKILL files | two lockfiles; 9.4k-line AGENTS.md | clean | clean |
| Known-issues honesty | **best** (self-reported HIGH) | good (session layers) | good | good |

**Reading:** all four are far above the norm for AI-generated codebases — none contains TODO-slop, dead commented code, or placeholder values in app code; comments consistently explain *why* with session-numbered provenance; error handling follows the envelope discipline (never throw across a handler boundary). The quality axis differentiates on strictness policy (digma best on TS, zb best on build-gating, neo-crm best on validation + lint ceiling) and hygiene (zb cleanest; digma the most cluttered). This dimension is the closest of the three; the ranking differences come from the other two dimensions.

---

## 6. Dimension B — Feature Completeness for Production Deployment (40%)

Purpose-weighted: authentication depth, dashboard quality, charting, plus the surrounding production surface.

| Capability | digma | neo-crm | project-management | zero-balance |
|---|---|---|---|---|
| Email+password auth (register/login/logout/me) | ✅ | ✅ | ✅ | ✅ |
| Email verification (OTP + resend) | ✅ | ✅ | — | — |
| Password reset funnel | ✅ (in-app URL default ⚠) | ✅ (hashed tokens, single-use, no-enumeration) | — (forgot state only) | partial (reset UI) |
| Session revocation (post-reset eviction) | ✅ tokenVersion (origin) | ✅ tokenVersion | — | — |
| Rate limiting (auth routes) | ✅ + proxy-hops env | ✅ per-route limits + proxy-hops | ✅ (10/15 min) | ✅ |
| Production secret enforcement | dev-fallback warn | **fail-hard in prod** | dev-fallback | dev-fallback warn |
| RBAC / roles | role field | role field + owner FKs across entities | team members (human/agent) | — |
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
| Email transport | in-app delivery + disable knob | in-app delivery + disable knob | — | — |
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
| Data-access discipline | `db.ts` singleton + **db-path seam (fixture-tested)** | db-path seam (20 checks) + `prisma-env.ts` wrapper | db-path seam (pinned) | db-path seam (15 checks) + env-discipline scripts |
| API contract | ok/fail envelope everywhere | envelope + Zod + bounded reader everywhere | envelope + manual validation | envelope + Zod |
| Route architecture | per-page routes (+ proxy.ts legacy-case redirects) | route groups (marketing)/(app) + server-guarded layout | **SPA rewrites onto one page** (exotic) | per-page routes, server components |
| Cross-pollination proven | pattern *origin* (tokenVersion, bounded reader) | **proven importer** (zb's Zod, digma's auth ports) | pattern donor (db-path origin) | pattern donor (Zod seam) |
| Scalability posture | single-node documented | single-node documented | single-node documented | single-node documented |
| Agent-readiness (docs as interface) | excellent but bloated | excellent but bloated (12k-line SKILL) | lean and excellent | lean and excellent |

**Reading:** the family's architectural core (layered imports-down, one store, envelope API, schema-anchored DB URL resolution with the standalone-server chdir trap solved and pinned by tests) is sound and unusually well-defended against its own known failure modes. neo-crm edges ahead on enforcement (inventoried layers, gate scripts, drift sweeps) and on the route-group + server-guarded-layout pattern, which is the most conventional and therefore most transferable to "any given web application." project-management's SPA-rewrite pattern is coherent but is the least transferable foundation. digma's editor-store engineering (gesture coalescing, net-zero guards, autosave deadline drain) is the most sophisticated client architecture in the family but is specific to canvas editors.

---

## 8. Scoring & Final Ranking

Weights reflect the evaluation purpose: feature completeness for the stated triad (auth + dashboard + charting) and production deployment carries the most weight (40%), because a template's job is to remove work; code quality 30%; architectural robustness 30%.

| Dimension (weight) | digma | neo-crm | project-management | zero-balance |
|---|---|---|---|---|
| Code quality (30%) | 8.5 | 8.0 | 7.0 | 8.0 |
| Feature completeness (40%) | 7.0 | 9.0 | 6.0 | 7.5 |
| Architectural robustness (30%) | 8.0 | 8.5 | 7.0 | 8.0 |
| **Weighted total** | **7.75** | **8.55** | **6.60** | **7.80** |
| **Rank** | **3** | **1** | **4** | **2** |

**Sensitivity notes (stated plainly):**
- neo-crm is #1 under any plausible weighting — it leads or ties every dimension that matters for this purpose.
- zero-balance vs digma is a genuine 0.05 tie. If your future apps will never chart, or you weight test-suite size and full TS strictness above built-in charting, swap them (digma → #2). For *this* evaluation's hard requirement (charting), zero-balance wins.
- project-management ranks last not because it is sloppy — it is disciplined — but because its SPA-in-one-page architecture, hand-rolled validation, and absent verification/reset funnel make it the weakest *foundation for arbitrary web apps*.

---

## 9. Recommendations

### 9.1 Primary recommendation
**Scaffold from `neo-crm`.** Concretely: delete the vendored `skills/` and `docs/` session archives (≈245 MB), strip the CRM domain entities (keep User + the auth family + the layout chrome + charts + dashboard skeleton + export/upload/search utilities as your starter), then rebrand. Keep its `gate` script as your definition of done. This yields, on day one: production-grade session auth with revocation, a Zod-validated API envelope layer, a chart component library, a dashboard shell, CSV/PDF export, a11y-tested primitives, and the family's best documentation contract — verified green from a clean clone.

### 9.2 Graft from the siblings (the family cross-pollinates by design — continue the tradition)
- From **zero-balance**: drop `ignoreBuildErrors` and make the build the type gate; adopt its inline-`DATABASE_URL` / `env -u` npm-script discipline; adopt its lean documentation size as your doc budget.
- From **digma**: adopt its test-density target and its honest Known-Issues register format; enable full TS strictness (drop `noImplicitAny: false`).
- From **project-management**: adopt the "every mutation writes an ActivityLog row" invariant if your domain benefits from audit narration.

### 9.3 Hardening checklist before any production deployment (all four need this)
1. **License** — add one (neo-crm already MIT; the others have none — legally, no one else may reuse them as-is). *(High, legal)*
2. **Hosted CI** — port the local gate (`lint → typecheck → test → build → smoke → e2e`) into a CI workflow; nothing currently enforces it on push. *(High)*
3. **Database** — switch SQLite → PostgreSQL (`.env.example` documents the swap but it is untested in all four) and adopt `prisma migrate` over `db push --accept-data-loss`. *(High)*
4. **Rate limiting** — replace the in-process limiter with a shared store (Redis) for multi-instance deploys; keep the proxy-hops env contract. *(High)*
5. **Email transport** — wire a real mail service behind the existing `*_DISABLE_IN_APP_OTP/RESET` knobs; in-app delivery of OTP/reset links is a demo posture. *(High)*
6. **Secrets at rest** — hash OTP codes and reset tokens (neo-crm already hashes reset tokens; digma self-reports plaintext at rest). *(Medium)*
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
| F-4 | **In-app OTP / reset-link delivery by default** | auth routes return codes/URLs in response bodies unless `*_DISABLE_IN_APP_*` set | Account-takeover class if deployed as-is publicly | **High** (default posture) | Verified (documented; digma self-reports its own as HIGH) |
| F-5 | `ignoreBuildErrors: true` | `next.config.ts` (digma, neo-crm, pm) | Type errors do not fail builds; relies on manual `typecheck` | Medium | Verified |
| F-6 | `noImplicitAny: false` | `tsconfig.json` (neo-crm, pm, zb) | Weakened strict mode | Medium | Verified |
| F-7 | **Repo bloat**: ~195 MB vendored `skills/` + 5–146 MB `docs/` session archives + screenshots in every repo | `du`, `git ls-files` counts | Clone/agent-context cost; not app code; template noise | Medium | Verified |
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
| D-5 | Two lockfiles (`bun.lock` + `package-lock.json`) | root listing | Non-reproducible installs across package managers | Low | Verified |
| D-6 | 390 MB `.git`, 146 MB `docs/` (450+ session logs, screenshot archives) | `du` | Clone weight; history noise | Low | Verified |

### 10.3 neo-crm

| # | Finding | Evidence | Impact | Severity | Confidence |
|---|---|---|---|---|---|
| N-1 | AGENTS.md 9,421 lines; SKILL.md 12,357 lines, largely per-session narrative | `wc -l` | Agent-context bloat; signal-to-noise decay for future agents (the family's own leaner repos prove the same discipline fits in ~1,300 lines) | Medium | Verified |
| N-2 | 11 capitalized `.jsx` route alias files alongside lowercase `.tsx` pages | `git ls-files` + file header comments | **Initially suspected dead code — disproven on read:** intentional, documented parity aliases (reference app links to `/Dashboard`); `.jsx` extension deliberately avoids TS1149 casing collision. Cosmetic exoticism only | Informational | Verified (file contents read) |
| N-3 | recharts 2.15 (v3 is current; sibling zb runs 3.10) | `package.json` | Older chart major; migration debt | Low | Verified |
| N-4 | Two lockfiles committed | root listing | Same as D-5 | Low | Verified |
| N-5 | Zod adoption is recent (session-163/166) — CRUD seams verified consistent, but the migration is young | `schemas.ts` header | Watch item, not a defect | Informational | Verified (header documents lineage) |

### 10.4 project-management

| # | Finding | Evidence | Impact | Severity | Confidence |
|---|---|---|---|---|---|
| P-1 | SPA-rewrite architecture (all views rewritten onto one page) | `next.config.ts` rewrites + `router.ts` + CLAUDE.md contract | Poor fit as a general template; inverts App Router conventions | **High (purpose-fit)** | Verified |
| P-2 | No email verification / password-reset funnel | route inventory (auth: register/login/logout/me only) | Missing production auth legs | Medium | Verified |
| P-3 | Hand-rolled validation by ADR ("do not introduce Zod halfway") | CLAUDE.md; SKILL §8 | Weakest input-hardening of the family | Medium | Verified |
| P-4 | Oldest dependency generation (Next 16.1, Prisma 6.11, React 19.0) | `package.json` | Upgrade debt | Low | Verified |
| P-5 | Smallest unit suite (138 checks) | executed run | Thinnest regression net | Low | Verified |

### 10.5 zero-balance

| # | Finding | Evidence | Impact | Severity | Confidence |
|---|---|---|---|---|---|
| Z-1 | No license | root listing / GitHub API | Same as F-1 | **High (legal)** | Verified |
| Z-2 | Smallest unit suite (108 checks / 9 files) | executed run | Pure-seam coverage thin relative to siblings | Low | Verified |
| Z-3 | Single chart type (donut) | 1 recharts-consuming file | Charting present but shallow vs neo-crm | Low (purpose-fit) | Verified |
| Z-4 | No teams / multi-entity ownership | 5-model schema, userId-only relations | Fine for its domain; limits as generic template | Informational | Verified |

### 10.6 Positive findings worth recording (no inflation — these are real)

- All four repos **build, typecheck, and pass their entire unit suites from a clean clone** in this environment — executed and observed (§2.2). This is rare even among human-maintained templates.
- No secrets committed anywhere (`.env.example` only, `.env` gitignored) — Verified across all four.
- The `db-path` seam (solving the standalone-server `process.chdir` + Prisma relative-URL ambiguity) is designed, implemented, and **pinned by fixture tests in all four repos** — a genuinely production-grade solution to a real Next.js standalone deployment trap.
- Comment quality is exemplary family-wide: nearly every non-obvious decision carries a *why* comment with session-numbered provenance, and every doc states "when code and this document disagree, the code wins — update the doc in the same commit."

---

## 11. Verification Ledger (what was checked, how, result)

| # | Check | How | Result |
|---|---|---|---|
| 1 | Clean-clone build pipeline (×4) | `verify-build.sh`: `bun install` → `bunx prisma generate` → `bun run typecheck` → `bun run build` (script persisted at `/home/z/my-project/scripts/verify-build.sh`; logs at `scripts/build-verify-<repo>.log`) | **All green, ×4**; standalone `server.js` produced ×4 |
| 2 | Unit suites (×4) | `bun run test` (Vitest) | digma 2,464/2,464 · neo-crm 2,668/2,668 · pm 138/138 · zb 108/108 — **all pass** |
| 3 | Secrets hygiene | `git ls-files` env-file census | Only `.env.example` tracked, ×4 |
| 4 | License presence | root file listing + GitHub API | MIT (neo-crm) only |
| 5 | Charting capability | `rg -l recharts src/` per repo | neo-crm 7 files · zb 1 · digma 0 · pm 0 |
| 6 | Auth implementation quality | full read of neo-crm `src/lib/auth.ts`; family comparison via SKILL §8 + route inventories | Verified claims in §4.1 |
| 7 | Validation boundaries | full/partial reads of `schemas.ts` (neo-crm), `validation.ts` (zb); ADR/docs for digma/pm | Verified claims in §5 |
| 8 | Suspicion check: neo-crm capitalized `.jsx` routes | read file contents | **Disproved dead-code hypothesis** — documented intentional aliases |
| 9 | Doc corpora sizes | `wc -l` across all key docs | As reported in §4 |
| 10 | Repo activity & metadata | `git log` census + GitHub API | As reported in §2.1 |
| 11 | E2E / smoke suites | **not executed** (no browser binaries provisioned) | Counts reported as documented claims (Reasoned) |

---

## 12. Appendix A — Comparative Quick Facts

| | digma | neo-crm | project-management | zero-balance |
|---|---|---|---|---|
| Domain | design workspace (canvas editor) | CRM | PM workspace + AI planner | budget planner |
| Next.js / React / Prisma | 16.4 / 19.3 / 6.19 | 16.4 / 19.3 / 6.19 | 16.1 / 19.0 / 6.11 | 16.1 / 19.0 / 6.11 |
| Prisma models | 5 | 9 | 8 | 5 |
| API route files | ~13 | 29 | ~14 | 13 |
| Runtime deps | 17 | 20 | 18 | 22 |
| Zod | — | ✅ 4.6 | — (ADR against) | ✅ 4.6 |
| Charts | — | recharts 2.15 (7 wrappers) | — (CSS rings) | recharts 3.10 (donut) |
| Export | PNG | CSV + PDF | — | — |
| Unit checks (executed) | 2,464 | 2,668 | 138 | 108 |
| E2E checks (documented) | 262 | n/a (11 spec files) | 115 | 288 |
| Smoke checks (documented) | 73 | present | 30 | 35 |
| `ignoreBuildErrors` | yes | yes | yes | **no** |
| `noImplicitAny:false` | **no** | yes | yes | yes |
| License | none | **MIT** | none | none |
| SKILL.md size | 720 ln | 12,357 ln | 739 ln | 1,350 ln |

## Appendix B — Documentation set examined per repo

`AGENTS.md` · `CLAUDE.md` · `Project_Architecture_Document.md` · `README.md` · `digma_SKILL.md` / `neo-crm_SKILL.md` / `project-management_SKILL.md` / `zero-balance_SKILL.md` (per the evaluation brief) · `package.json` · `prisma/schema.prisma` · `next.config.ts` · `tsconfig.json` · `.env.example` · key `src/lib/*` seams · chart/dashboard components · `scripts/smoke-test.sh` · root-level hygiene census. digma additionally carries stray `project-management_SKILL.md` + `scandihaven_SKILL.md` (noted D-4); zero-balance carries a stray `project-management_SKILL.md`.
