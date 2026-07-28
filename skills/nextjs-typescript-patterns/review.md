# Validation Plan & Cross-Check Report: `nextjs-typescript_SKILL.md`

## 0. Capability Disclosure (Important)

I do **not** have a live web-search tool in this environment, so I cannot execute "extensive web searches" literally. What I can do — and have done below — is:

1. **Full internal validation**: line-by-line trace of every SKILL claim against the two Project Brief files (complete, authoritative — I have all three documents).
2. **External fact-check from training knowledge (cutoff 2026)**: covers ESLint 9, React 19, TypeScript 5.x, Prettier 3, pnpm 10/11, Drizzle, Stripe, Trigger.dev, Better Auth, Sanity, Vitest landscapes current through mid-2026.
3. **A live-verification checklist** with exact commands/URLs so any remaining ❓ items can be confirmed in minutes against registry/npm/docs truth.

Each finding carries a confidence badge: ✅ corroborated / ⚠️ nuance or amplification / ❌ likely inaccurate / ❓ verify live.

---

## Part A — Validation Plan (Methodology)

### A.1 Four validation dimensions

| Dimension | Question | Method | Authority |
|---|---|---|---|
| **D1. Internal fidelity** | Does the SKILL accurately distill what the sessions actually did? | Trace each Case Index entry + handbook "Mistake" entry to its source narrative in the briefs | `Project_Brief.md` (status_8–12), `Project_Brief_previous.md` (deps, db, prettier, trigger.dev, workspace check-types) |
| **D2. External accuracy** | Are the technical claims true in the real world? | Check against tool docs, registry metadata, installed type definitions | Official docs, `npm view`, `node_modules` types |
| **D3. Currency (July 2026)** | Are recommended patterns still idiomatic? | Check major-version defaults: ESLint 9 flat config, React 19 types, TS 5.x flags, Prettier 3, pnpm 10+ | Release notes / changelogs |
| **D4. Completeness** | Did the SKILL drop lessons the briefs contain, or canonize hypotheses as facts? | Diff brief "Outstanding Issues" + hedged language ("likely", "appears") against SKILL doctrine | Side-by-side reading |

### A.2 Verdict taxonomy

- ✅ **Corroborated** — brief evidence + external knowledge agree.
- ⚠️ **Amplified/Imprecise** — directionally right, but the SKILL states more than the evidence supports, or the mechanism description is loose.
- ❌ **Likely inaccurate** — conflicts with external knowledge; needs correction.
- ❓ **Verify live** — knowledge-cutoff sensitive (version literals, SDK renames).
- ➖ **Omitted** — brief lesson absent from SKILL.

### A.3 Priority order

1. Claims that, if wrong, would cause an agent to **introduce new type errors** (highest — this is where REACT-1 lands).
2. Claims about **tool defaults/behavior** (Prettier ignore, tsconfig inheritance, ESLint config systems).
3. **Version literals and SDK API names** (drift-prone).
4. **Completeness gaps** (lowest risk).

---

## Part B — Internal Validation (Executed): SKILL ↔ Briefs

### B.1 Case Index audit (39 entries)

| ID | Brief source | Verdict | Note |
|---|---|---|---|
| DEP-1 | Prev §1: `@react-email/components@^6.6.5` never existed; zero imports; deleted | ✅ | SKILL's "delete unused dep" matches the rejected swap-to-`react-email` decision |
| DEP-2 | Prev §2: `sanity@^6.30.0` never existed → `^6.6.0` | ✅ | |
| DEP-3 | Prev §3: hotspot moved from array to image member | ✅ | |
| DEP-4 | Prev §4: `@vitejs/plugin-react` undeclared in email pkg | ✅ | |
| DEP-5 | Prev §5: jest-dom caret admitted deprecated 6.10.0; exact-pinned | ✅ internal / ❓ external | See C.3 — the "deprecated 6.10.0" claim needs a registry check |
| DEP-6 | Prev §5: `pnpm@11.9.0` → verified real version | ✅ | SKILL wisely omits the specific number |
| DB-1 | Prev db §4–6: orphaned `0001_phase3.sql`, journal drift, full-schema dump, silent failure recovered from Postgres logs | ✅ | |
| DB-2 | Prev db Decision 5: `db:generate` removed from `db-setup.sh` | ✅ | |
| DB-3 | Prev db Decision 6: `import './env';` added first | ✅ | |
| PRETTIER-1 | Prev trpc.test: missing `)` on line 15, error reported 16:11 | ✅ | |
| PRETTIER-2 | status_10 (16 files), status_12 (7 files) | ✅ | |
| PRETTIER-3 | Prev prettier §2–6: `--ignore-path .gitignore` bypassed ignore file; second `--ignore-path` added | ⚠️ | Mechanism imprecise — see C.2 |
| PRETTIER-4 | Prev prettier §4: `docs` matched where `docs/` didn't | ✅ | |
| PRETTIER-5 | Prev prettier §8–9: ~195 files dirty after new config; approved repo format | ✅ | |
| SDK-1 | Prev trigger §3: no `/v4` subpath in any published version | ✅ | Brief includes export-map evidence (`.`, `./v3`, `./ai`, …) |
| SDK-2 | Prev trigger §5: dependency undeclared in `@maison/config` | ✅ | |
| SDK-3 | Prev trigger §5: `accessToken`, `tasks.trigger`, `AnyTask` generic | ✅ | SKILL reproduces the exact corrected call |
| SDK-4 | Prev trigger §4: `services/workers/trigger.config.ts` outside `src/**/*.ts` include | ✅ | |
| TS-1 | status_8 §2: inherited `baseUrl` resolved under `tooling/typescript` | ✅ | Proven in-brief via `tsc --traceResolution` |
| TS-2 | status_8 §3: `lib/trpc/{server,client}`, `lib/utils` scaffolded from consumer contracts | ✅ | |
| TS-3 | status_8 §4: `await api().x.y()` → `const caller = await api()` | ✅ | |
| TS-4 | status_8 §7: `Boolean(row.featured)`, `email ?? ''`, `discountPercent ?? 10` | ✅ | SKILL correctly preserves the "business-decision review" caveat |
| TS-5 | Prev workspace §4: `NeonHttpDatabase \| NodePgDatabase` union broke `.returning()` overloads | ✅ | Empirically proven with probes in the brief |
| TS-6 | Prev workspace §5: `forgetPassword` → `requestPasswordReset`; `{user,url,token}` | ✅ internal / ❓ external | See C.4 |
| TS-7 | Prev workspace §7: `basil` vs `dahlia`; local `RefundStatus`; conditional spread | ✅ internal / ❓ external | Version literals drift-prone — see C.5 |
| TS-8 | Prev workspace §6: `@upstash/ratelimit`, `@maison/payments@workspace:*` | ✅ | |
| ESLINT-1 | status_9 §3–5: FlatCompat + flat ESM → `__esModule`; two-file fix | ✅ | |
| ESLINT-2 | status_10 §2: autofix left 16 files Prettier-dirty | ✅ | |
| ESLINT-3 | status_11: 89 problems → batched plan | ✅ | Note: live count was 47 by status_12 — SKILL's 89 is correct *for its case moment* |
| REACT-1 | status_11: "**likely** React 19 FormEvent/event deprecations" (planned, **never executed or verified**) | ❌/⚠️ | **Most important finding — see B.2** |
| REACT-2 | status_11 Batch B plan (not executed) | ⚠️ | Pattern is standard-correct, but brief shows it was planned, not proven |
| REACT-3 | status_11 plan + Stillwater reference | ✅ | Pattern unconditionally correct (`async` without `await`) |
| REACT-4 | status_11 Batch A executed | ✅ | |
| REACT-5 | status_11 Batch A executed (`q ?? ''`) | ✅ | |
| TOOL-1 | status_11: edit-tool quote failures | ✅ | |
| TOOL-2 | status_11: corruption → `git checkout` → ESLint-JSON-driven script | ✅ | |
| TOOL-3 | Doctrine-level; standard bash hygiene | ✅ | Not tied to one incident |
| HOOK-1 | status_12: 7 staged unformatted files | ✅ | |
| HOOK-2 | status_12: hook advances format→types→lint (47 remaining) | ✅ | |

**Score: 35 ✅, 3 ⚠️, 1 ❌/⚠️, plus 3 ❓ external flags.**

### B.2 The one serious fidelity problem: REACT-1

The SKILL states as **doctrine** (§4.3, §4.8, §6.8, Case Index):

> "React 19 deprecates `FormEvent`. Use `React.SubmitEvent<HTMLFormElement>`."

The brief evidence is much weaker:

- status_11 classified 11 `@typescript-eslint/no-deprecated` errors as "**likely** React 19 FormEvent/event deprecations" — an unverified hypothesis.
- The fix was **planned for Batch B but never executed** and **never verified** (status_11 ends mid-Batch-A; status_12 shows 47 problems still outstanding, deprecations included).

So the SKILL canonized an unexecuted, hedged hypothesis into a handbook rule. This matters because (per Part C) the claim is probably factually wrong, and an agent following it would generate *new* type errors. **This violates the SKILL's own Doctrine 2.10 / checklist item "Do not mix 'applied' with 'verified'."**

### B.3 Completeness gaps (brief lessons missing from SKILL)

| ➖ Omission | Source | Suggested placement |
|---|---|---|
| Turbo/`error.txt` can **underreport** the failing package set (bare `ELIFECYCLE` hid db/auth/payments errors; live per-package rerun revealed 5 failing packages) | Prev workspace §1 | §3 Step 3 or §4.10 tooling |
| Next.js `manifest.ts` requires **snake_case** (`short_name`, `start_url`, `theme_color`) | status_8 §5 | §4.8 React/Next handbook |
| Sentry SDK option drift (`silent` invalid in current `BrowserOptions/NodeOptions/EdgeOptions`) | status_8 §5 | §4.7 SDK handbook |
| Documented counts drift from live counts (89 → 47 between sessions) — concrete exemplar for Doctrine 2.1 | status_11 vs status_12 | §2.1 |
| Prettier exit-code semantics: `1` = diffs, `2` = parse error — useful triage signal | Prev trpc.test | §4.4 |
| Modern tsconfig alternative: `paths` **without** `baseUrl` (TS ≥ 4.1; relative to declaring tsconfig in 5.x) | General currency | §4.2 Mistake 1 |
| pnpm 10+ **build-script gating** (`onlyBuiltDependencies`) — affects esbuild/sharp/bcrypt installs | Currency (not in briefs) | §4.1 |
| Naming divergence: SKILL `name: nextjs-typescript-patterns` vs briefs' referenced skill `nextjs16-react19-tailwind4-better-auth-monorepo` | File headers | Metadata alignment |

---

## Part C — External Fact-Check (2026 knowledge; live checks where needed)

### C.1 High-confidence confirmations ✅

| Claim | Assessment |
|---|---|
| ESLint 9 flat config is default; `FlatCompat` is for legacy eslintrc only; flat-config-through-FlatCompat yields `__esModule`/invalid-property validation errors | ✅ Accurate; classic ESLint 9 migration symptom |
| Shared ESM packages should use `"exports"` maps, not bare `"main"` | ✅ Current Node ESM best practice |
| TS inherits `baseUrl` relative to the **declaring** config file → monorepo alias breakage; fix with local `baseUrl`/`paths` | ✅ Documented TypeScript behavior; known turborepo pitfall |
| `exactOptionalPropertyTypes` forbids explicit `undefined`; conditional spreads are the idiom | ✅ |
| `noUncheckedIndexedAccess` makes index/capture-group access possibly-undefined | ✅ |
| pnpm strict isolation: undeclared imports fail; workspace deps need `workspace:*` | ✅ Still pnpm's default model in v10/11 |
| Drizzle Kit: `_journal.json` + `meta/*_snapshot.json` drive generate/migrate; missing snapshots → full-schema dumps; `CREATE TYPE` non-idempotent collisions | ✅ Matches drizzle-kit 0.2x–0.4x behavior |
| `NeonHttpDatabase` vs `NodePgDatabase` union → incompatible `.returning()` overloads; canonicalize one driver type | ✅ Known drizzle-orm typing pattern |
| Prettier: `--check` exits 1 on diffs, 2 on parse errors; multiple `--ignore-path` flags supported; ESLint `--fix` ≠ Prettier-formatted | ✅ |
| `@typescript-eslint/restrict-template-expressions` flags raw numbers under recommended configs; `String(...)` / `?? ''` fixes | ✅ |
| Sanity `hotspot: true` belongs on the image member, not the array | ✅ Per Sanity schema docs |
| Vitest `passWithNoTests`; empty suite → nonzero exit | ✅ |
| Trigger.dev: main entry is the current API; `client.tasks.trigger(...)` with `accessToken` auth; no `/v4` subpath | ✅ Consistent with v3/v4 SDK shape |
| Next.js `manifest.ts` snake_case fields; `ImageResponse` OG handlers may be synchronous | ✅ |
| `set -o pipefail` / `${PIPESTATUS[0]}`; parser errors point past the true fault site | ✅ Standard |

### C.2 ⚠️ Prettier ignore-file naming (imprecise mechanism)

SKILL/briefs say passing `--ignore-path .gitignore` "disables automatic loading of `.prettierrignore`." More precisely: Prettier's auto-loaded default ignore file is **`.prettierignore`** — it never auto-loaded `.prettierrignore` (non-standard name) at all. The operational lesson and fix (explicit second `--ignore-path`) are correct and the probe evidence is solid, but the SKILL should either rename the file to `.prettierignore` or state that `.prettierrignore` is a project-chosen name requiring explicit `--ignore-path`.

### C.3 ❓ jest-dom "deprecated 6.10.0"

The brief (and SKILL DEP-5) claims caret `^6.9.1` admitted a **deprecated** `6.10.0`. The pattern-advice (exact-pin sensitive deps) is sound regardless, but the specific deprecation claim should be confirmed:

```bash
npm view @testing-library/jest-dom@6.10.0 deprecated time --json
```

### C.4 ❓ Better Auth `forgetPassword` → `requestPasswordReset`

The session verified against **installed** `better-auth@1.6.25` types (correct methodology), but better-auth's public docs historically showed `forgetPassword`. This may be a genuine late-2025/2026 rename, or a surface-shape nuance (e.g., plugin-gated). Verify:

```bash
grep -rn "forgetPassword\|requestPasswordReset" node_modules/better-auth/dist/client.d.ts
```

The SKILL's *lesson* ("installed SDK types are truth") is correct either way; the specific rename should be marked version-scoped (`≥1.6.x`) once confirmed.

### C.5 ❓ Stripe `basil` / `dahlia` literals

Codename-dated API versions and `stripe@22.x` are plausible for 2026, and the **pattern** (omit optional `apiVersion`; define local unions when namespace types vanish) is unconditionally sound. Exact literals drift every Stripe release — verify per-install:

```bash
grep -rn "ApiVersion\|'20.*\.\(basil\|dahlia\)'" node_modules/stripe/types/shared.d.ts
```

### C.6 ❌/❓ REACT-1: `React.FormEvent` deprecation / `React.SubmitEvent`

**This is the highest-risk item.** To my 2026 knowledge, `@types/react@19` does **not** deprecate `React.FormEvent`, and `React.SubmitEvent<T>` is **not** a standard React synthetic-event type (`onSubmit` remains `FormEventHandler<T> = EventHandler<FormEvent<T>>`; the only `SubmitEvent` is the native DOM type in `lib.dom.d.ts`). The 11 `no-deprecated` errors were more plausibly about genuinely deprecated React-19-era surfaces (legacy lifecycle methods `componentWillMount`/`componentWillReceiveProps`, `ReactDOM.render`/`findDOMNode`, legacy `Ref`/`LegacyRef`, `propTypes`/`defaultProps` on function components).

Verify in 30 seconds:

```bash
grep -n "deprecated" node_modules/@types/react/index.d.ts | grep -i "formevent"
grep -n "interface SubmitEvent" node_modules/@types/react/index.d.ts
npx eslint apps/web --format json | jq '.[].messages[] | select(.ruleId=="@typescript-eslint/no-deprecated") | .message'
```

**Recommended correction** unless verification surprises us: rewrite §4.8/§6.8/REACT-1 to *"Run `no-deprecated` with JSON output and fix whatever the installed types actually flag; do not assume FormEvent."* If `React.SubmitEvent` truly doesn't exist, the current SKILL advice would break `check-types`.

### C.7 Currency gap: pnpm 10+ build scripts

pnpm ≥ 10 no longer runs dependency lifecycle scripts by default (requires `pnpm.onlyBuiltDependencies` / approval). This is a common 2026 install "failure" (esbuild/sharp/better-sqlite3/bcrypt) that the Dependency Handbook doesn't mention. Recommend adding as DEP Mistake 8.

---

## Part D — Consolidated Findings & Recommended Corrections

| # | Severity | Item | Action |
|---|---|---|---|
| 1 | **High** | REACT-1 asserts `FormEvent` deprecated / `React.SubmitEvent` exists — unverified hypothesis canonized as fact; probably false | Verify via C.6 commands; rewrite to evidence-driven guidance; demote to "planned, unverified" in Case Index |
| 2 | Medium | REACT-2/Batch-B fixes were planned but never executed/verified in the briefs | Tag Case Index entries as "planned pattern" or verify live before keeping as doctrine |
| 3 | Medium | Prettier ignore mechanism description conflates `.prettierrignore` with Prettier's default `.prettierignore` | Correct §4.4 Mistake 2–4 wording |
| 4 | Medium | pnpm 10+ build-script gating absent | Add to §4.1 + Anti-Pattern Catalog |
| 5 | Low | Underreported Turbo failures (rerun per-package) not in playbooks | Add to §3 Step 3 / Playbook 3 |
| 6 | Low | manifest snake_case, Sentry `silent`, Prettier exit codes, `paths`-without-`baseUrl` | Add as small handbook entries |
| 7 | Low | Version-scoped claims (jest-dom 6.10.0, better-auth rename, Stripe literals) stated timelessly | Prefix with "verify against installed version" + commands |
| 8 | Trivial | SKILL `name` vs briefs' referenced skill name diverge | Align metadata |

**Overall verdict:** The SKILL is a **high-fidelity, technically sound consolidation** — ~90% of entries are fully corroborated by the briefs and consistent with 2026 tooling reality, and its doctrine (reproduce-first, gate classification, infra-vs-debt, surgical fixes, adjacent-gate verification) is excellent. The single must-fix is **REACT-1**, which violates the document's own "applied ≠ verified" rule and is likely factually wrong. Everything else is polish, currency, or version-scoping.

---

## Part E — Live Verification Checklist (to replace the web searches I cannot run)

```bash
# REACT-1 (priority)
grep -c "@deprecated" node_modules/@types/react/index.d.ts
grep -n "SubmitEvent" node_modules/@types/react/index.d.ts
npm view @types/react@19 version

# Version/SDK claims
npm view @testing-library/jest-dom@6.10.0 deprecated --json
npm view @react-email/components versions --json | tail -5
npm view pnpm@11.17.0 version
node -p "JSON.stringify(require('@trigger.dev/sdk/package.json').exports, null, 2)"
grep -rn "requestPasswordReset\|forgetPassword" node_modules/better-auth/dist/*.d.ts | head
grep -rn "dahlia\|basil" node_modules/stripe/types/shared.d.ts | head

# ESLint/Prettier behavior
npx eslint --print-config apps/web/eslint.config.mjs | head -20
npx prettier --help | grep -A2 "ignore-path"

# Doctrine ground-truth for the repo itself
pnpm --filter @maison/web lint --format json > /tmp/eslint.json
jq '[.[].messages[].ruleId] | group_by(.) | map({(.[0]): length}) | add' /tmp/eslint.json
```

