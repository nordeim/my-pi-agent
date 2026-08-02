---
name: nextjs-typescript-patterns
description: Monorepo web projects using pnpm, Turborepo, TypeScript, Next.js, React, ESLint, Prettier, Drizzle ORM, Postgres, and third-party SDKs (tRPC, Trigger.dev, Stripe, Better Auth, Sanity, React Email, Vitest)
version: 1.6
---

# Consolidated Agent Briefing Document and Programming Handbook

## Agent Programming and Troubleshooting Handbook

Version: 1.6  
Scope: Monorepo web projects using pnpm, Turborepo, TypeScript, Next.js, React, ESLint, Prettier, Drizzle, Postgres, and third-party SDKs.  
Purpose: Prevent repeated mistakes and provide a reusable troubleshooting methodology.  
Reconciliation note: v1.6 adds: (1) §16 v15-v18 supplement — 8 new lessons (dep hygiene contract test, tsconfig.config.json for root configs, ESLint flat config per-package, Zod v4 native API migration, non-null assertion TRPCError guards, ||→?? for empty-string preservation, PII-redacted logging + email escaping, React 19 SubmitEvent); (2) §17 new anti-patterns; (3) §18 new patterns; (4) §19 updated 34-item field card. v1.5 adds: (1) §4.8 four new Mistakes — IntersectionObserver timing in useEffect (V12), next/image fill + CSS Grid anti-pattern (V13), useSearchParams() without Suspense breaks static prerendering (V15), useEffect([]) misses client-side navigation (V14); (2) §5.8 ScrollRevealTrigger pattern — thin Client Component mounting a side-effect hook in a shared layout; (3) §6.8 three React anti-patterns — grid placement on absolutely-positioned Image fill, raw JSON.stringify in dangerouslySetInnerHTML for JSON-LD, hooks defined but never called; (4) §10 six new case-index rows (RENDER-1 through RENDER-5, SECURITY-1); (5) §12 four new lessons ranked 15–18 (hooks called not just defined, IntersectionObserver timing, image fill + grid flow, useSearchParams Suspense). v1.4 adds: (1) §4.2 TS Mistake 17 — runtime assertions (`expect().not.toBeNull()`) do not narrow TypeScript types; (2) §4.4 Prettier Mistake 8 + anti-pattern — `.prettierrignore` as gate-silencer vs. unowned-content marker; (3) §4.9 Testing Mistake 4 — async-deferred-to-null file reads in contract tests (Stillwater's `readFileSync` → `string` pattern); (4) §5.9 corrected both source-contract-test and meta-guard pattern blocks from async to synchronous null-free form; (5) §7 Playbook 17 — `TS18047` after runtime null-check, two-branch fix (preferred: non-null producer); (6) §10 four new case-index rows (TS-9, PRETTIER-6, TEST-1, RUNTIME-6); (7) §12 Lesson 13 sharpened — prior green-checkmarks are also hypotheses, not just prose conclusions. v1.3 added: (1) Playbook 16 Scenario B — auth-guarded route `DYNAMIC_SERVER_USAGE` warnings are expected + the `force-dynamic`/`cacheComponents` trap; (2) §5.9 Testing Patterns — source contract tests for architectural invariants + meta-guard pattern for caller modules; (3) §4.10 Mistake 7 — `.gitignore` `lib/` bleed in Python+JS monorepos; (4) §12 Lesson 14 — distinguishing public-route from auth-route warnings; (5) §4.8 Server/Client Boundary note — the `api()`/`apiPublic()` split is a Server Component concern. v1.2 absorbed the genuine deltas from `update.md` (parser-error line attribution + `cat -A`; `psql -f` fallback for spinner-masked silent Drizzle failures; the named "Surgical Change Discipline" and the Stillwater reference-copy caveat).

---

# 1. How to Use This Handbook

This handbook is divided into:

- **Doctrine**: how an agent should think and behave.
- **Playbooks**: what to do when a specific symptom appears.
- **Domain Handbooks**: detailed rules for specific tooling areas.
- **Pattern Catalog**: good practices to adopt.
- **Anti-Pattern Catalog**: mistakes to avoid.
- **Verification Matrices**: how to prove success.
- **Handoff Standards**: how to leave the repository and report state.

An agent should use it in this order:

1. Before touching code, read the doctrine.
2. When a failure appears, use the universal troubleshooting algorithm.
3. Identify the domain and consult the relevant handbook.
4. Apply the smallest correct fix.
5. Verify the affected gate and adjacent gates.
6. Record outstanding issues and hand off cleanly.

---

# 2. Agent Operating Doctrine

These are the highest-level rules. They override expediency.

## 2.1 Evidence over narrative

Do not trust a brief, document, or prior diagnosis blindly.

Always verify against:

- live commands,
- current files,
- current git state,
- installed packages,
- actual tool output.

A prior summary may be:

- outdated,
- incomplete,
- wrong,
- referring to uncommitted work,
- referring to a different repository state.

### Rule

> Treat every prior diagnosis as a hypothesis until reproduced and validated.

---

## 2.2 Reproduce before prescribing

Never fix based only on a pasted error snippet.

Reproduce:

- the exact failing command,
- in the exact workspace,
- with the exact package manager,
- using the exact script or hook.

### Rule

> If you cannot reproduce the failure, you do not yet understand the failure.

---

## 2.3 Classify the gate

Most failures belong to one of these gates:

1. Install / dependency resolution
2. Type-checking
3. Linting
4. Formatting
5. Testing
6. Build
7. Runtime
8. Database migration / seeding
9. Git hook / pre-commit pipeline

Each gate has different remediation rules.

### Rule

> Do not confuse a formatting failure with a type failure, or an infrastructure failure with source-code debt.

---

## 2.4 Distinguish infrastructure failure from source-code debt

Infrastructure failures mean the tool cannot run correctly.

Examples:

- ESLint cannot load config.
- Prettier cannot parse a file.
- TypeScript cannot resolve modules.
- pnpm cannot resolve a version.
- Drizzle cannot apply migrations.

Source-code debt means the tool runs but reports genuine violations.

Examples:

- unused variables,
- unescaped JSX entities,
- floating promises,
- deprecated event types,
- console usage.

**Third category: construction-time validation failures.** Some frameworks (like tRPC v11) validate code at router construction time, which runs at module load — not during static type analysis. A reserved word in a tRPC procedure name is not an infrastructure failure (the tool runs) nor a source-code debt issue (it's not a lint violation) — it's a **framework contract violation** that only surfaces when the module is actually loaded at build time. This is why `pnpm check-types` passes but `pnpm build` fails.

### Rule

> Fix infrastructure first. Then remediate source-code debt deliberately. For construction-time validation failures (like tRPC reserved words), inspect the build gate output — the error message names the offending identifier.

---

## 2.5 Prefer surgical changes

Avoid broad, speculative changes.

Prefer:

- editing only files implicated by the failure,
- using the project’s existing workflow,
- preserving behavior,
- avoiding unnecessary refactors.

Avoid:

- blanket formatting without approval,
- rewriting configs because one file fails,
- adding abstractions to fix one error,
- relaxing guardrails to make a gate pass.

### Rule

> The smallest correct fix is better than a large convenient fix.

### Surgical Change Discipline

When applying a fix, internalize these rules:

1. **Do not bundle unrelated fixes.** If the error is a Prettier syntax error,
   fix the syntax. Do not run a repo-wide `pnpm format` unless explicitly
   approved.
2. **Verify the blast radius.** Before applying a fix, check how many files it
   touches. If a type fix requires changing 30 router files, look for a
   canonical type definition at the source (e.g. fixing `DrizzleDB` at the
   DB package level) instead of editing every consumer.
3. **Preserve commit hygiene.** Never auto-commit. Leave the working tree in a
   state where the user can logically group changes (e.g. separating
   infrastructure config fixes from source-code lint remediation).
4. **No speculative scaffolding.** If an ESLint config or test setup is
   missing, add only what is strictly required to pass the current gate.

---

## 2.6 Preserve guardrails

Do not weaken:

- lint rules,
- type strictness,
- pre-commit hooks,
- formatting enforcement,
- migration safety checks,

unless there is an explicit policy decision.

### Rule

> A green gate achieved by weakening the gate is not a fix.

---

## 2.7 Use reference implementations carefully

A reference project can show canonical patterns, but it should not be copied blindly.

Use it to answer:

- What is the idiomatic shape?
- What config style is expected?
- What tool ordering is normal?
- What overrides are standard?

Do not copy:

- overrides for directories that do not exist,
- dependencies that are not needed,
- abstractions that do not match the current codebase,
- entire override blocks borrowed from a reference project (e.g. Stillwater) when
  the target project does not yet have the files those overrides apply to.

### Rule

> Adapt reference patterns to the actual project contracts.

---

## 2.8 Verify adjacent gates

Fixing one gate can break another.

After any fix, verify:

- the gate you intended to fix,
- the gate before it,
- the gate after it.

Example:

- ESLint autofix can break Prettier.
- Prettier formatting should not break type-checking.
- Type fixes should not break lint.
- Migration fixes should not break seeding.

### Rule

> A fix is not complete until the surrounding pipeline is verified.

---

## 2.9 Leave the repository better, not mysteriously different

If the working tree contains multiple logical changes, do not mix them silently.

Identify:

- staged changes,
- unstaged changes,
- generated artifacts,
- formatting-only changes,
- infrastructure changes,
- source-code fixes.

### Rule

> One logical change per commit. If commit grouping is unclear, leave it for review.

---

## 2.10 Document outstanding work

Always record:

- what was fixed,
- what was verified,
- what remains broken,
- what was intentionally out of scope,
- what needs runtime validation,
- what needs commit review.

### Rule

> A clean handoff is as important as the fix itself.

---

# 3. Universal Troubleshooting Algorithm

Use this algorithm for almost any failure.

## Step 1 — Read the full error artifact

Do not stop at the first line.

Look for:

- the failing command,
- the package or workspace,
- the gate,
- the exit code,
- whether the failure is fatal or warning,
- whether the error is infrastructural or source-code-level.

### Questions

- What command actually failed?
- Which package failed?
- Is this a parse error, type error, lint error, format error, install error, or runtime error?
- Is the tool itself failing to start?

### Worked example — parser line attribution

Parsers report the error at the *next token they cannot reconcile*, not at the
origin of the defect. Prettier once reported a fatal syntax error on **line 16**
of `trpc.test.ts`; the actual defect was an unclosed parenthesis on **line 15**.

Rule:

> When facing a fatal parse error, inspect the preceding line(s), count
> brackets/parentheses, and only then look at the reported line.

Diagnostics for hidden characters:

```bash
cat -A <file>      # show non-printing bytes ($ line ends, ^I tabs, ^M CR)
```

---

## Step 2 — Inspect repository state

Check:

```bash
git status --short
git log --oneline -10
```

Look for:

- staged files,
- unstaged files,
- untracked artifacts,
- partially applied fixes,
- uncommitted prior work,
- conflicting logical changes.

### Lesson from prior sessions

Several failures were caused or complicated by:

- staged but unformatted files,
- prior fixes not committed,
- working trees mixing multiple logical changes.

---

## Step 3 — Reproduce the exact failure

Run the exact command from the error artifact.

Examples:

```bash
pnpm install
pnpm format:check
pnpm check-types
pnpm lint
pnpm --filter @scope/pkg check-types
bash scripts/pre-commit-check.sh
pnpm db:setup
```

Capture:

- full output,
- exit code,
- whether output was truncated by pipes.

### Exit-code hygiene

Avoid this mistake:

```bash
some-command | tail
echo $?
```

That may report the exit code of `tail`, not `some-command`.

Use:

```bash
set -o pipefail
```

or:

```bash
some-command | tail
echo "${PIPESTATUS[0]}"
```

---

## Step 4 — Classify the failure

Use this table:

| Symptom | Likely Class |
|---|---|
| `ERR_PNPM_NO_MATCHING_VERSION` | Dependency resolution |
| `Cannot find module` | Missing dependency, alias, or scaffolding |
| `TS2307` | Module resolution |
| `TS2554` | Wrong argument count or incompatible overload |
| `TS2339` | Property does not exist, often wrong type |
| `Unexpected top-level property "__esModule"` | ESLint config-format mismatch |
| Prettier `[error]` | Parse failure |
| Prettier `[warn]` | Formatting drift |
| Drizzle silent migrate failure | Migration state or SQL conflict |
| `DATABASE_URL is not set` | Environment loading order |
| Test runner exit 1 with no tests | Empty suite or missing test files |
| Hook fails before type-check | Format gate or parse failure |

---

## Step 5 — Form hypotheses

Create a small hypothesis table.

Example:

| ID | Hypothesis | Evidence Needed |
|---|---|---|
| H1 | Missing dependency | Check `package.json`, `pnpm why`, import graph |
| H2 | Wrong version | Check registry versions |
| H3 | Config format mismatch | Inspect config loader and exports |
| H4 | State drift | Inspect generated artifacts and journals |
| H5 | Misleading error line | Inspect neighboring lines and parser diagnostics |

---

## Step 6 — Use authoritative diagnostics

Prefer machine-readable or low-level evidence:

- `npm view` / registry metadata,
- package `exports`,
- `tsc --traceResolution`,
- ESLint `--format json`,
- Prettier direct file checks,
- Postgres logs,
- Drizzle migration journal,
- TypeScript type definitions,
- `git diff`,
- `git status`.

### Rule

> Do not hand-map truth from noisy terminal output when a machine-readable source exists.

---

## Step 7 — Apply the smallest correct fix

Before editing:

- confirm the root cause,
- confirm the minimal file set,
- confirm the behavior should be preserved,
- confirm no guardrail needs weakening.

---

## Step 8 — Verify the fix and adjacent gates

At minimum:

```bash
pnpm format:check
pnpm check-types
pnpm lint
```

If relevant:

```bash
pnpm test
pnpm build
pnpm db:setup
bash scripts/pre-commit-check.sh
```

---

## Step 9 — Record outstanding issues

Even if the immediate blocker is fixed, record:

- remaining gate failures,
- deferred source-code debt,
- runtime verification not performed,
- commit grouping needed,
- latent defects discovered but not fixed.

---

# 4. Domain Handbooks

---

# 4.1 Dependency and Install Hygiene Handbook

## Core Principle

Dependencies must be:

- real,
- declared,
- used,
- version-compatible,
- workspace-correct,
- lockfile-consistent.

---

## Mistakes and Issues Encountered

### Mistake 1: Declaring a version that does not exist

Example:

```json
"@react-email/components": "^6.6.5"
```

Root cause:

- The package did not have that version.
- The version was conflated with a different package’s version line.

Lesson:

> Always validate package versions against the registry.

Prevention:

```bash
npm view @react-email/components versions --json
npm view react-email versions --json
```

---

### Mistake 2: Keeping unused dependencies

The `@react-email/components` dependency was declared but never imported.

Root cause:

- Dependency was added speculatively or left behind after a design change.

Fix:

- Delete the dependency instead of replacing it with a heavier alternative.

Lesson:

> If a dependency is unused, removal is often the best fix.

Anti-pattern:

- Replacing an unused dependency with a different unused dependency.

Pattern:

- Audit imports before “fixing” a dependency version.

---

### Mistake 3: Conflating similarly named packages

Examples:

- `react-email` vs `@react-email/components`
- Sanity framework version vs Sanity package version

Lesson:

> Package names and version lines are not interchangeable.

Prevention:

- Check the exact package name.
- Check the exact version range.
- Check sibling dependency versions for consistency.

---

### Mistake 4: Relying on undeclared imports in pnpm workspaces

Examples:

- `@vitejs/plugin-react` imported by `vitest.config.ts` but not declared.
- `@upstash/ratelimit` imported by `@maison/api` but not declared.
- `@maison/payments` imported by `@maison/api` but not declared as a workspace dependency.

Root cause:

- pnpm uses strict dependency isolation.
- A package cannot reliably import something just because another workspace package has it installed.

Fix:

```bash
pnpm --filter @scope/pkg add -D some-dep
pnpm --filter @scope/pkg add @scope/other-pkg@workspace:*
```

Lesson:

> Every imported package must be declared in the consuming package’s manifest.

Anti-pattern:

- “It works locally because it is hoisted somewhere.”

Pattern:

- Treat pnpm strict isolation as correct behavior, not an obstacle.

---

### Mistake 5: Caret ranges admitting deprecated versions

Example:

```json
"@testing-library/jest-dom": "^6.9.1"
```

The caret allowed a deprecated `6.10.0`.

Fix:

- Exact-pin to `6.9.1` until a deliberate upgrade is made.

Lesson:

> Caret ranges can silently admit deprecated or broken versions.

Pattern:

- Use exact pins for known-sensitive dependencies.
- Upgrade deliberately.

---

### Mistake 6: Misaligned `packageManager`

Example:

```json
"packageManager": "pnpm@11.9.0"
```

Updated to a real, verified newer version.

Lesson:

> The repository should declare a real, verified package manager version.

Prevention:

```bash
npm view pnpm versions --json
```

---

### Mistake 7: Empty test suites causing nonzero exit

Some packages had test scripts that failed because Vitest found no test files.

Lesson:

> A failing test command is not always a regression; it may be an empty suite.

Options:

- author tests,
- configure `passWithNoTests` if appropriate,
- document the empty-suite condition.

Anti-pattern:

- Assuming test failure always means broken code.

---

### Mistake 8: pnpm 10+ blocks dependency lifecycle scripts by default

Symptom:

- `pnpm install` succeeds but native packages (esbuild, sharp, bcrypt,
  better-sqlite3) fail at build time or produce broken binaries.
- `ERR_PNPM_MISSINGApprovedBuiltinDependency` or silent build failures.

Root cause:

- pnpm ≥ 10 blocks lifecycle scripts of dependencies for security.
- This is a breaking change from pnpm 9.
- Common affected packages: esbuild, sharp, bcrypt, better-sqlite3.

Fix:

In `pnpm-workspace.yaml` (pnpm 10.26+, preferred):

```yaml
allowBuilds:
  esbuild: true
  sharp: true
```

In `pnpm-workspace.yaml` (pnpm 10.0–10.25):

```yaml
onlyBuiltDependencies:
  - esbuild
  - sharp
```

Or run: `pnpm approve-builds`

Lesson:

> pnpm 10+ requires explicit approval for native dependency builds.
> The config syntax changed between pnpm versions — verify against
> your installed pnpm version.

Pattern:

- pnpm 10.0–10.25: `onlyBuiltDependencies` list in `pnpm-workspace.yaml`
- pnpm 10.26+: `allowBuilds` map in `pnpm-workspace.yaml` (preferred)
- pnpm 11+: `onlyBuiltDependencies` removed; `allowBuilds` required

Prevention:

```bash
pnpm --version
# Then use the correct config syntax for your version
```

---

## Dependency Troubleshooting Checklist

When install fails:

1. Read the exact error code.
2. Identify the failing package and version range.
3. Validate the version exists:

   ```bash
   npm view <pkg> versions --json
   ```

4. Check whether the dependency is actually used.
5. Check for package-name conflation.
6. Check sibling dependency versions.
7. Check whether the import is declared in the consuming workspace.
8. Run install with workspace filters if needed.
9. Verify lockfile updates.
10. Re-run type-check and tests after dependency changes.

---

## Dependency Patterns

### Good Pattern: Delete unused dependencies

If no imports exist, remove the dependency.

### Good Pattern: Declare every imported package

Especially in pnpm monorepos.

### Good Pattern: Validate versions before editing manifests

Registry truth beats documentation memory.

### Good Pattern: Pin sensitive dependencies deliberately

Use exact pins when deprecation or breakage is known.

---

## Dependency Anti-Patterns

| Anti-Pattern | Symptom | Prevention |
|---|---|---|
| Inventing versions | `ERR_PNPM_NO_MATCHING_VERSION` | Check registry |
| Conflating package names | Wrong version line | Verify exact package |
| Keeping unused deps | Bloat and confusion | Audit imports |
| Undeclared imports | Module not found in pnpm workspace | Declare in consuming package |
| Caret into deprecated version | Deprecation warnings | Exact-pin deliberately |
| Missing devDep for config import | Test tool fails | Add devDep |
| Assuming hoisting | Works locally, fails elsewhere | Respect pnpm isolation |

---

# 4.2 TypeScript and Type-Check Handbook

## Core Principle

Type errors are often not local syntax mistakes. They are frequently caused by:

- module resolution,
- missing scaffolding,
- incorrect async usage,
- incompatible unions,
- SDK drift,
- strict compiler flags,
- leaky data boundaries.

---

## Mistakes and Issues Encountered

### Mistake 1: Broken path alias due to inherited `baseUrl`

Symptom:

```text
TS2307: Cannot find module '@/components/shop/ProductCard'
```

Even though the file existed.

Root cause:

- `apps/web/tsconfig.json` extended a shared config.
- The shared config’s `baseUrl` resolved relative to the shared package.
- The alias `@/*` resolved to the wrong directory.

Fix:

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

Lesson:

> Shared tsconfig packages can silently break path aliases through inherited `baseUrl`.

Diagnostic:

```bash
tsc --traceResolution
```

Pattern:

- Define local `baseUrl` in the app that owns the paths.

Anti-pattern:

- Assuming an alias is correct because it appears in `paths`.

---

### Mistake 2: Missing scaffolding mistaken for type errors

Symptom:

- Many unresolved imports for `@/lib/trpc/client`, `@/lib/trpc/server`, `@/lib/utils`.

Root cause:

- The `lib/` modules genuinely did not exist.

Fix:

- Scaffold the missing modules using the project’s real contracts.

Lesson:

> Some type errors are actually missing-file errors in disguise.

Pattern:

- Inspect actual consumers to infer required exports before scaffolding.

Anti-pattern:

- Copying reference files without adapting to local contracts.

---

### Mistake 3: Calling an async caller without awaiting it

Symptom:

```text
TS2339: Property 'account' does not exist on type 'Promise<...>'
```

Bad pattern:

```ts
await api().account.listOrders();
```

Correct pattern:

```ts
const caller = await api();
await caller.account.listOrders();
```

Parallel calls:

```ts
const caller = await api();

const [profile, orders, wishlist] = await Promise.all([
  caller.account.getProfile(),
  caller.account.listOrders(),
  caller.account.listWishlist(),
]);
```

Lesson:

> If a factory returns a promise, await it before accessing members.

Anti-pattern:

- Chaining property access onto an unresolved promise.

Pattern:

- Create the caller once, then reuse it.

---

### Mistake 4: Leaking nullable Drizzle join shapes to the UI

Symptom:

- `boolean | null` not assignable to `boolean`.
- `string | null` not assignable to `string`.

Root cause:

- Left joins caused Drizzle to infer nullable fields even when the underlying column was not semantically nullable.

Fix:

Shape data at the router boundary:

```ts
featured: Boolean(row.featured),
isNew: Boolean(row.isNew),
isBestseller: Boolean(row.isBestseller),
email: row.email ?? '',
discountPercent: row.discountPercent ?? 10,
```

Lesson:

> Routers should return UI-friendly contracts, not raw nullable query rows.

Pattern:

- Coerce at boundaries.
- Keep components simple.

Anti-pattern:

- Forcing every component to handle join-artifact nullability.

Caution:

- Boundary coercions may encode business decisions and should be reviewed.

---

### Mistake 5: Dead comparisons after control-flow narrowing

Symptom:

- TypeScript knows a comparison is unreachable.

Example:

```ts
if (step === 'confirmation') {
  return ...;
}

// later
step === 'confirmation'
```

Root cause:

- Earlier control flow narrowed the type.

Fix:

- Remove dead code.

Lesson:

> Type narrowing can reveal genuinely unreachable logic.

Pattern:

- Let the compiler help delete dead branches.

---

### Mistake 6: Violating `exactOptionalPropertyTypes`

Bad:

```ts
onError: env.NODE_ENV === 'development' ? handler : undefined
```

Better:

```ts
...(env.NODE_ENV === 'development'
  ? { onError: handler }
  : {})
```

Lesson:

> Under strict optional property types, omitting a property is different from assigning `undefined`.

Pattern:

- Use conditional spreads.

Anti-pattern:

- Explicitly assigning `undefined` to optional properties.

---

### Mistake 7: Unguarded indexed access

Bad:

```ts
SHIPPING_LABELS[shipping.shippingMethod].split('(')
```

Better:

```ts
SHIPPING_LABELS[shipping.shippingMethod]?.split('(')
```

Lesson:

> With `noUncheckedIndexedAccess`, index access may be undefined.

Pattern:

- Guard all indexed lookups.

---

### Mistake 8: Regex capture groups may be undefined

Bad:

```ts
decodeURIComponent(match[1])
```

Better:

```ts
decodeURIComponent(match[1] ?? '')
```

Lesson:

- Capture groups can be undefined under strict index-access rules.

---

### Mistake 9: Brittle type extraction

Bad:

```ts
db: Parameters<Parameters<typeof router>[0]['query']>[0]['ctx']['db']
```

Better:

```ts
db: DrizzleDB
```

Lesson:

> If a type requires archaeological excavation, expose a canonical type instead.

Pattern:

- Export stable public types from packages.

Anti-pattern:

- Deriving public types from deep internal structures.

---

### Mistake 10: Union of incompatible driver types

Symptom:

```text
TS2554: Expected 0 arguments, but got 1
```

Root cause:

```ts
export const db = isNeonUrl ? drizzleNeon(...) : drizzlePg(...);
export type DrizzleDB = typeof db;
```

TypeScript inferred:

```ts
NeonHttpDatabase<typeof schema> | NodePgDatabase<typeof schema>
```

The union had incompatible method overloads.

Fix:

- Canonicalize the type to the production driver:

```ts
export type DrizzleDB = NeonHttpDatabase<typeof schema>;
```

Lesson:

> Runtime ternaries can create type unions that are unusable at the call site.

Pattern:

- Choose a canonical production type.
- Let the development driver conform to it.

Anti-pattern:

- Letting `typeof db` leak an incompatible union into consumers.

---

### Mistake 11: Direct casts of driver-specific results

Bad:

```ts
result as Array<Record<string, unknown>>
```

Better:

```ts
result as unknown as Array<Record<string, unknown>>
```

Lesson:

- Some driver results do not overlap enough for direct casting.

Caution:

- Use `unknown` casts sparingly and document them.

---

### Mistake 12: Hardcoded SDK API versions

Example:

```ts
apiVersion: '2025-08-27.basil'
```

Installed SDK expected a newer literal.

Fix:

- Remove the hardcoded literal if optional.

Lesson:

> Hardcoded API version literals create drift against installed SDK types.

Pattern:

- Let the SDK infer its supported version when possible.

---

### Mistake 13: Using unavailable SDK namespace types

Example:

- `Stripe.Refund.Status` no longer available as expected.

Fix:

- Define a local union:

```ts
type RefundStatus =
  | 'pending'
  | 'requires_action'
  | 'succeeded'
  | 'failed'
  | 'canceled';
```

Lesson:

> SDK namespace types can change; prefer locally stable types when necessary.

---

### Mistake 14: Outdated authentication API usage

Examples:

- `forgetPassword` no longer existed.
- `sendResetPassword` received `{ user, url, token }`, not `{ email, url }`.

Fix:

- Use `requestPasswordReset`.
- Use `user.email`.

Lesson:

> Installed SDK type definitions are the source of truth, not old documentation or memory.

---

### Mistake 15: tsconfig include hiding broken files

Example:

- `services/workers/trigger.config.ts` contained a broken import.
- It did not fail type-check because it was outside `src/**/*.ts`.

Lesson:

> A green type-check can hide latent errors if include globs are too narrow.

Prevention:

- Periodically audit include paths.
- Move root config files under checked directories or include them explicitly.

---

### Mistake 16: tRPC procedure named with a JavaScript reserved word

Symptom:

```text
Error: Reserved words used in `router({})` call: apply
```

Root cause:

- A tRPC procedure was named `apply` (`packages/api/src/routers/trade.ts`).
- `apply` is `Function.prototype.apply` — a core JavaScript mechanism.
- tRPC v11 validates all procedure names at router construction time against a list of JavaScript built-in reserved words.
- The tRPC adapter route (`/api/trpc/[trpc]`) is statically analyzed by Next.js during `next build`, which triggers the router constructor and surfaces the error.

Fix:

```diff
- apply: protectedProcedure
+ submitApplication: protectedProcedure
```

Lesson:

> tRPC v11 rejects JavaScript reserved words (`apply`, `call`, `bind`, `constructor`, `toString`, `valueOf`, `hasOwnProperty`, `__proto__`, etc.) as procedure names. Use domain-specific verb-noun pairs instead.

Prevention:

- Name procedures with domain-specific verb-noun pairs: `submitApplication`, `listOrders`, `getProfile`.
- Avoid any name that collides with `Object.prototype`, `Function.prototype`, or `Array.prototype` methods.
- The `pnpm build` gate catches this — but only at build time, not at type-check time (the constructor runs at module load, not during static analysis).

Pattern:

```text
good: submitApplication, createOrder, getProfile, listProducts
bad:  apply, call, bind, constructor, toString, valueOf
```

Anti-pattern:

> Naming a tRPC procedure after a common verb without checking for JavaScript built-in collisions.

---

### Mistake 17: Runtime assertions do not narrow TypeScript types

Symptom:

```text
src/lib/__tests__/rendering-strategy.contract.test.ts:111:26 - error TS18047: 'src' is possibly 'null'.
  111         const codeOnly = src
                                ~~~
```
...appearing *immediately after* a line that reads:

```ts
expect(src, `… not found`).not.toBeNull();
```

Root cause:

- The producer was typed `string | null` (`readFile(...).catch(() => null)`).
- `expect(src).not.toBeNull()` is a **Vitest runtime assertion** — it throws at runtime if `src` is null. It is **not** a TypeScript type guard and does **not** narrow `src`'s compile-time type.
- `tsc` keeps `src: string | null`, so the next line (`src.split('\n')`) derefs a maybe-null value → `TS18047` under `strict: true`.

Bad:

```ts
const read = (rel: string) => readFile(join(APP_ROOT, rel), 'utf8').catch(() => null);
// ...
const src = await read(rel);            // string | null
expect(src).not.toBeNull();             // runtime-only — does NOT narrow `src`
const codeOnly = src.split('\n');        // TS18047: 'src' is possibly 'null'
```

Better (preferred — make the producer non-null so the null branch never exists):

```ts
const read = (rel: string): string => readFileSync(join(APP_ROOT, rel), 'utf8');
// ...
const src = read(rel);                   // string — no null branch, no TS18047
const codeOnly = src.split('\n');
```

Acceptable (if you must keep a nullable producer — use a *real* type guard at the deref site):

```ts
if (src === null) throw new Error(`${rel} not found`);  // narrows `src` to string
const codeOnly = src.split('\n');
```

The first fix (non-null producer) is preferred because it also improves the failure mode: a missing file throws a readable ENOENT at `readFileSync` instead of being swallowed to `null` and surfacing later as a confusing regex-assertion failure. See Testing Mistake 4.

Lesson:

> A runtime assertion (`expect(x).not.toBeNull()`, `assert(x)`, `console.assert`) does not narrow `x`'s TypeScript type. To clear `TS18047` you must either make the producer non-null, or use a construct `tsc` recognizes as narrowing (`if (x === null) …`, a user-defined `asserts x` guard, or `x ?? …`).

Prevention:

- Prefer producers that can't return `null` (synchronous `readFileSync`, `.then(x => x!)` with a known-non-null source, etc.) over deferred-to-null `.catch(() => null)`.
- If you write `expect(x).not.toBeNull()` and then use `x`'s members, you are relying on a runtime check the compiler cannot see — restructure so the type reflects the truth.
- Remember `strict: true` (and especially `noUncheckedIndexedAccess`) makes *every* nullable deref a hard error, not a warning.

---

## TypeScript Troubleshooting Checklist

When `check-types` fails:

1. Run per-package checks:

   ```bash
   pnpm --filter @scope/pkg check-types
   ```

2. Determine whether errors are:
   - module resolution,
   - missing files,
   - type mismatch,
   - SDK drift,
   - strictness violations.

3. For module resolution:

   ```bash
   tsc --traceResolution
   ```

4. Check:
   - `baseUrl`,
   - `paths`,
   - `include`,
   - `exclude`,
   - package dependencies,
   - workspace links.

5. For SDK drift:
   - inspect installed type definitions,
   - inspect package exports,
   - compare against registry version.

6. For many similar errors:
   - look for one root cause,
   - fix the source type,
   - avoid editing dozens of consumers unnecessarily.

7. After fixes:
   - rerun per-package checks,
   - rerun workspace check,
   - rerun Prettier on changed files.

8. For `TS18047: 'x' is possibly 'null'` appearing right after a runtime null-check (`expect(x).not.toBeNull()`, `assert(x)`):
   - **the check is not a type guard** — Vitest/Jest assertions narrow at runtime, not compile time,
   - make the producer non-null (e.g. `readFileSync` instead of `readFile().catch(() => null)`),
   - or use a *real* narrowing construct (`if (x === null) throw …` / `asserts x` guard).

9. If `check-types` passes but `build` fails:
   - inspect the build output for module initialization errors,
   - tRPC v11 validates procedure names at router construction time (runtime, not type analysis),
   - check for reserved words (`apply`, `call`, `bind`, `constructor`, etc.) in procedure definitions.

---

## TypeScript Patterns

### Good Pattern: Fix root types, not many consumers

If one exported type causes many errors, fix the export.

### Good Pattern: Shape data at boundaries

Routers and API layers should return clean contracts.

### Good Pattern: Export canonical types

Avoid forcing consumers to derive types from internals.

### Good Pattern: Use conditional spreads for optional properties

Especially under `exactOptionalPropertyTypes`.

### Good Pattern: Await factories before use

If `api()` returns a promise, await it first.

---

## TypeScript Anti-Patterns

| Anti-Pattern | Symptom | Fix |
|---|---|---|
| Inherited `baseUrl` breaks alias | `TS2307` for existing files | Local `baseUrl` |
| Missing scaffolding | Many unresolved imports | Create real modules |
| Promise member access | `TS2339` on `Promise` | Await factory |
| Raw nullable rows in UI | `null` assignability errors | Boundary coercion |
| Dead comparisons | Narrowing errors | Remove dead code |
| Explicit `undefined` optional | `exactOptionalPropertyTypes` | Conditional spread |
| Unguarded index access | Possibly undefined | Optional chaining |
| Brittle `Parameters` type | Unreadable type | Canonical type |
| Incompatible union | Overload errors | Canonical driver type |
| Hardcoded SDK version | Type literal mismatch | Remove or update |
| Outdated SDK methods | Missing property errors | Use installed API |
| Narrow include glob | Hidden broken files | Audit tsconfig include |

---

# 4.3 ESLint Handbook

## Core Principle

ESLint failures fall into two categories:

1. **ESLint cannot run** — infrastructure/config failure.
2. **ESLint runs and reports violations** — source-code debt.

Do not confuse them.

---

## Mistakes and Issues Encountered

### Mistake 1: Using `FlatCompat` with flat config

Symptom:

```text
Unexpected top-level property "__esModule"
```

Root cause:

- Shared ESLint config was modern flat ESM.
- Consumer used legacy `FlatCompat.extends()`.
- ESM interop added `__esModule`.
- Legacy validator rejected it.

Fix:

- Add proper `exports` to shared config package.
- Import shared config directly.
- Export a flat array.

Before:

```js
import { FlatCompat } from '@eslint/eslintrc';

const compat = new FlatCompat();
export default [...compat.extends('@maison/eslint-config')];
```

After:

```js
import sharedConfig from '@maison/eslint-config';

export default [...sharedConfig];
```

Lesson:

> `FlatCompat` is for legacy eslintrc configs, not modern flat configs.

---

### Mistake 2: Missing ESM `exports` in shared config package

Bad:

```json
{
  "main": "index.js"
}
```

Better:

```json
{
  "exports": {
    ".": "./index.js"
  }
}
```

Lesson:

> Modern ESM shared packages should expose explicit exports.

---

### Mistake 3: Copying reference overrides unnecessarily

A reference project may have overrides for:

- tests,
- UI components,
- dashboards.

If the current project does not have those areas, copying overrides is speculative.

Lesson:

> Only add overrides when the codebase actually needs them.

---

### Mistake 4: Running ESLint autofix without Prettier afterward

Symptom:

- ESLint fixes import order or syntax style.
- Prettier then reports formatting drift.

Lesson:

> ESLint autofix does not guarantee Prettier formatting.

Pattern:

```bash
pnpm lint:fix
pnpm format
```

---

### Mistake 5: Treating remaining lint violations as infrastructure failure

After ESLint infrastructure was fixed, remaining violations included:

- `react/no-unescaped-entities`,
- `@typescript-eslint/restrict-template-expressions`,
- `@typescript-eslint/no-floating-promises`,
- `@typescript-eslint/no-unused-vars`,
- `@typescript-eslint/no-deprecated`,
- `@typescript-eslint/require-await`,
- `no-console`.

These were genuine source-code issues.

Lesson:

> Once ESLint runs, lint errors are code remediation, not config scaffolding.

---

## ESLint Source-Code Fix Patterns

### `react/no-unescaped-entities`

Problem:

```tsx
<div>You've got mail</div>
```

Fix:

```tsx
<div>You&apos;ve got mail</div>
```

Rule:

- Escape apostrophes and quotes in JSX text.

---

### `@typescript-eslint/restrict-template-expressions`

Problem:

```ts
`Width: ${progress}%`
```

Fix:

```ts
`Width: ${String(progress)}%`
```

For optional strings:

Problem:

```ts
`Search: ${q}`
```

If `q` can be `undefined`, avoid:

```ts
String(q)
```

because it can produce `"undefined"`.

Better:

```ts
`Search: ${q ?? ''}`
```

Rule:

- Use `String(...)` for numbers.
- Use `?? ''` for optional strings where empty fallback is desired.

---

### `@typescript-eslint/no-floating-promises`

Problem:

```tsx
onChange={(e) => doAsyncThing(e.target.value)}
```

Fix:

```tsx
onChange={async (e) => {
  await doAsyncThing(e.target.value);
}}
```

Or, if intentionally fire-and-forget:

```tsx
onChange={(e) => {
  void doAsyncThing(e.target.value);
}}
```

Rule:

- Do not drop promises silently.

---

### `@typescript-eslint/no-deprecated` for React 19 forms

Problem:

```ts
React.FormEvent<HTMLFormElement>
```

Fix:

```ts
React.SubmitEvent
```

Why:

- React 19 deprecates `FormEvent`.
- `onSubmit` expects a submit event handler.
- `SubmitEvent` still has `.preventDefault()`.

Rule:

- Use the event type matching the DOM handler.

---

### `@typescript-eslint/require-await`

Problem:

```ts
export async function Image() {
  return new ImageResponse(...);
}
```

Fix:

```ts
export function Image() {
  return new ImageResponse(...);
}
```

Rule:

- Remove `async` when there is no `await`.

---

### `no-console`

Problem:

```ts
console.log('webhook received');
```

Fix if diagnostic logging is needed:

```ts
console.warn('webhook received');
```

Or use a proper logger.

Rule:

- Prefer structured logging or allowed console levels.

---

## ESLint Troubleshooting Checklist

When lint fails:

1. Determine whether ESLint can run at all.
2. If config fails:
   - inspect config format,
   - inspect package exports,
   - check flat vs legacy config,
   - remove `FlatCompat` if using flat config.
3. If ESLint runs:
   - get machine-readable output:

     ```bash
     npx eslint . --format json > eslint.json
     ```

   - group by rule,
   - count by rule,
   - separate mechanical from semantic fixes.
4. Batch fixes:
   - mechanical first,
   - semantic second,
   - dead code/narrowing third.
5. After fixes:
   - rerun lint,
   - rerun Prettier,
   - rerun type-check.

---

## ESLint Patterns

### Good Pattern: Separate infrastructure from debt

Fix config first, then source violations.

### Good Pattern: Use ESLint JSON output

Do not manually copy line numbers from noisy terminal output.

### Good Pattern: Batch mechanical fixes first

Mechanical fixes are lower risk.

### Good Pattern: Preserve guardrails

Do not disable rules just to make lint pass.

---

## ESLint Anti-Patterns

| Anti-Pattern | Symptom | Fix |
|---|---|---|
| `FlatCompat` with flat config | `__esModule` error | Direct flat import |
| Missing ESM exports | Config resolution issues | Add `exports` |
| Speculative overrides | Unnecessary config | Add only when needed |
| `lint:fix` without format | Prettier drift | Run Prettier after |
| Disabling rules | Hidden debt | Fix code |
| Hand-mapping lint fixes | Script errors | Use ESLint JSON |
| Declaring done before verify | False success | Rerun lint |

---

# 4.4 Prettier and Formatting Handbook

## Core Principle

Prettier failures are usually not logic failures. They are formatting-state failures.

But they can block commits because many hooks treat Prettier warnings as fatal.

---

## Mistakes and Issues Encountered

### Mistake 1: Confusing Prettier config with Prettier ignore

`.prettierrc` controls formatting options only.

It does not control path exclusion.

Path exclusion requires:

- `.prettierrignore`,
- or an ignore path source,
- or CLI ignore flags.

Lesson:

> Config options and ignore behavior are separate systems.

---

### Mistake 2: `--ignore-path` replaces Prettier's default ignore discovery

By default, Prettier auto-loads both `.gitignore` and `.prettierrignore`.
Passing `--ignore-path` replaces this auto-discovery entirely — only the
specified file(s) are used.

If the command uses:

```bash
prettier --check "**/*" --ignore-path .gitignore
```

then `.prettierrignore` is NOT loaded (overrides defaults).

Fix — pass both explicitly:

```bash
prettier --check "**/*" --ignore-path .gitignore --ignore-path .prettierrignore
```

Multiple `--ignore-path` flags are supported.

Lesson:

> `--ignore-path` replaces, not supplements, Prettier's default ignore
> discovery. Always list all ignore files explicitly when using this flag.

---

### Mistake 3: Gitignoring tracked documentation to exclude it from formatting

Bad idea:

- Add `docs/` to `.gitignore` just to stop Prettier formatting.

Why bad:

- `docs/` contained tracked files.
- Git exclusion is not formatting exclusion.

Fix:

- Use `.prettierrignore`.

Lesson:

> Do not use git tracking mechanisms for formatting-only concerns.

---

### Mistake 4: Using `docs/` instead of `docs` in ignore patterns

In some Prettier ignore contexts:

```text
docs/
```

did not match direct-path globs reliably, while:

```text
docs
```

did.

Lesson:

> Ignore pattern matching must be tested with the real command.

---

### Mistake 5: Introducing a new Prettier config without expecting repo-wide drift

When `.prettierrc` changed defaults:

- quote style changed,
- print width changed,
- many files became dirty.

This was expected, not a regression.

Lesson:

> A new formatting config changes the formatting fixed point.

Pattern:

- Get approval before repo-wide formatting.
- Verify no semantic changes.
- Verify type-check remains green.

---

### Mistake 6: Leaving staged files unformatted

Several pre-commit failures were caused by files that were:

- staged,
- modified,
- but not Prettier-formatted.

Lesson:

> If a file is staged, its staged content must pass the format gate.

Pattern:

- Format touched files before staging or before commit.

---

### Mistake 7: Running ESLint autofix and not reformatting

ESLint autofix can change code style in ways Prettier dislikes.

Lesson:

> Tool ordering matters.

Pattern:

```bash
pnpm lint:fix
pnpm format
pnpm format:check
```

---

### Mistake 8: Using .prettierrignore to silence a real [warn]

Symptom:

- A file emits `[warn] Code style issues found` on `prettier --check`.
- Instead of running `prettier --write`, the file path is added to `.prettierrignore`.
- The `[warn]` disappears from the gate, but the file remains genuinely mis-formatted.

Root cause:

- `.prettierrignore` is being used as a **gate-silencer**, not as a marker for genuinely-unformattable content.
- This violates §2.5 Preserve Guardrails ("Never make a gate green by weakening it").
- The symptom is the same as the Prettier mistake at §4.10 Tooling Mistake 7 (`.gitignore` hiding files from CI) — but on the Prettier side: the gate *passes* now, so the breakage is invisible until the next agent formats the file and sees a diff that has nothing to do with their change.

Bad:

```bash
# Instead of fixing the file:
echo 'apps/web/src/lib/__tests__/my-test.ts' >> .prettierrignore
git add .prettierrignore
```

Better:

```bash
# Fix the file, then remove any bespoke exclusion:
prettier --write apps/web/src/lib/__tests__/my-test.ts
git add apps/web/src/lib/__tests__/my-test.ts
# If .prettierrignore had a line for this file, remove it:
# (the line should only exist for genuinely-unformattable content)
```

Lesson:

> `.prettierrignore` is for content you **cannot or should not format** (vendored docs, generated files, binary-adjacent assets). It is never a substitute for `prettier --write`. If a file is owned by your project and is mis-formatted, the fix is formatting it — not hiding it from the gate.

Prevention:

- After adding any file to `.prettierrignore`, ask: "Is this genuinely unformattable, or am I silencing a `[warn]`?" If the answer is the latter, run `prettier --write` instead.
- Verify `.prettierrignore` entries periodically: remove the entry and re-run `prettier --check` — if the file passes, the entry was masking real drift.
- Reserve `.prettierrignore` for: files outside your control (docs/, skills/, generated content), or content that Prettier cannot parse.

---

## Prettier Troubleshooting Checklist

When Prettier fails:

1. Determine whether the failure is:
   - `[warn]` formatting drift,
   - `[error]` parse failure.
2. If `[error]`:
   - treat it as a syntax problem first,
   - find the true fault site,
   - fix the syntax,
   - then run Prettier.
3. If `[warn]`:
   - identify exact files,
   - run `prettier --write` on those files,
   - avoid blanket formatting unless approved.
4. If ignore behavior is wrong:
   - inspect the exact CLI command,
   - check `--ignore-path`,
   - test with probe files,
   - verify pattern syntax.
5. After formatting:
   - rerun `format:check`,
   - rerun `check-types`,
   - inspect git diff for semantic changes.

---

## Prettier Patterns

### Good Pattern: Separate fatal parse errors from formatting warnings

A parse error blocks Prettier entirely.

### Good Pattern: Format only reported files

Unless repo-wide formatting is explicitly approved.

### Good Pattern: Probe ignore behavior

Create temporary dirty files in:

- root,
- excluded directory,

and verify expected behavior.

### Good Pattern: Run Prettier after ESLint autofix

This restores formatting fixed point.

---

## Prettier Anti-Patterns

| Anti-Pattern | Symptom | Fix |
|---|---|---|
| Assuming `.prettierrignore` loads | Docs still formatted | Add `--ignore-path .prettierrignore` |
| Gitignoring tracked docs | Tracking side effects | Use Prettier ignore |
| Wrong ignore pattern | Exclusion fails | Test `docs` vs `docs/` |
| Blanket formatting | Huge diff | Scope formatting |
| Staged but unformatted | Hook fails | Format before commit |
| ESLint fix without format | Prettier drift | Run format after lint:fix |
| Treating parse error as formatting | Repeated failure | Fix syntax first |
| Silencing `[warn]` via `.prettierrignore` | Real formatting drift hidden | Run `prettier --write`; reserve ignore for unowned content |

---

# 4.5 Git Hooks and Commit Hygiene Handbook

## Core Principle

A pre-commit hook is a pipeline. A failure early in the pipeline can hide later failures.

Typical order:

```text
format:check → check-types → lint
```

Sometimes:

```text
format → types → lint → test → build
```

---

## Mistakes and Issues Encountered

### Mistake 1: Assuming the hook failure is the whole problem

A Prettier failure can hide lint failures.

Lesson:

> Fix the first gate, then simulate the full hook.

Pattern:

```bash
bash scripts/pre-commit-check.sh
```

---

### Mistake 2: Thinking warnings are non-fatal

Some hooks treat Prettier warnings as fatal.

Lesson:

> Understand the hook’s exit-code policy.

---

### Mistake 3: Not re-staging formatted files

If files were staged before formatting, the formatted working-tree copies may differ from the index.

Lesson:

> After formatting, review and re-stage if necessary.

---

### Mistake 4: Mixing multiple logical changes in one working tree

Examples:

- ESLint infrastructure fix,
- ESLint autofixes,
- Prettier formatting,
- type fixes,
- lint fixes.

Lesson:

> Mixed working trees make commit history and review harder.

Pattern:

- Identify logical commit boundaries.
- Leave grouping decisions for review if unclear.

---

## Hook Troubleshooting Checklist

When a pre-commit hook fails:

1. Identify the failing gate.
2. Run the gate command directly.
3. Fix that gate only.
4. Re-run the full hook simulation.
5. Check whether the next gate now fails.
6. Inspect staged vs unstaged state.
7. Do not weaken the hook unless explicitly approved.

---

## Hook Patterns

### Good Pattern: Simulate the hook directly

Run the same script the hook runs.

### Good Pattern: Report gate progression

Example:

- Before: stopped at format.
- After: passes format and types, stops at lint.

### Good Pattern: Preserve strict hooks

Strict hooks prevent debt from entering the repository.

---

## Hook Anti-Patterns

| Anti-Pattern | Symptom | Fix |
|---|---|---|
| Weakening hook | Temporary green | Fix underlying gate |
| Ignoring staged state | Hook fails after format | Re-stage |
| Assuming one gate is all | Next gate fails | Simulate full hook |
| Mixing changes | Unclear commits | Separate logically |
| Bypassing hook | Hidden debt | Avoid unless emergency |

---

# 4.6 Drizzle, Postgres, and Migration Handbook

## Core Principle

Database failures are often state failures, not code failures.

You must inspect:

- migration files,
- migration journal,
- snapshots,
- database state,
- server logs,
- environment loading order.

---

## Mistakes and Issues Encountered

### Mistake 1: Orphaned migration not registered in journal

Symptom:

- `0001_phase3.sql` existed.
- `_journal.json` did not reference it.

Root cause:

- Migration file was committed.
- Journal update was not committed.

Fix:

- Register the orphaned migration in `_journal.json`.

Lesson:

> A migration file is not reachable unless the journal knows about it.

---

### Mistake 2: Missing Drizzle snapshots causing full-schema regeneration

Symptom:

- `drizzle-kit generate` produced a full-schema dump.
- The dump redeclared existing enums and tables.

Root cause:

- Hand-curated migrations existed.
- Drizzle snapshot metadata was missing.
- Generate could not compute an incremental diff.

Lesson:

> If using Drizzle generate, commit snapshots. If hand-curating, do not casually run generate.

---

### Mistake 3: Running `db:generate` inside `db:setup`

Symptom:

- Setup repeatedly generated destructive migrations.

Root cause:

- `db:setup` is provisioning.
- `db:generate` is a developer schema-change workflow.

Fix:

- Remove `db:generate` from setup.
- Make setup run:
  - database startup,
  - migrate,
  - seed.

Lesson:

> Provisioning scripts must be deterministic and idempotent.

Pattern:

```text
db:setup = up + migrate + seed
db:generate = manual schema-change step
```

---

### Mistake 4: Non-idempotent SQL

Bad:

```sql
CREATE TYPE "public"."discount_type" AS ENUM (...);
```

Better when rerunnable:

```sql
DO $$ ... $$;
```

or avoid regenerating existing types.

Lesson:

> Full-schema dumps are dangerous without idempotency guards.

---

### Mistake 5: Silent migration failure hiding the real error

Symptom:

```text
[ELIFECYCLE] Command failed with exit code 1
```

No useful error.

Root cause:

- Drizzle spinner overwrote the error.
- Postgres logs contained the real error:

```text
ERROR: type "discount_type" already exists
```

Lesson:

> When CLI output is silent, inspect server logs.

Pattern:

```bash
docker logs <postgres-container>
```

Strip ANSI noise if needed.

If the spinner is still masking the real error, bypass the tool entirely and
run the migration's raw SQL directly against the database — the SQL engine's
own error surface is unmasked:

```bash
psql "$DATABASE_URL" -f drizzle/<migration>.sql
```

---

### Mistake 6: Importing database client before loading environment

Symptom:

```text
DATABASE_URL is not set
```

Root cause:

- Seed script imported the database client first.
- Environment loader existed but was never imported.
- The database client read env vars at module initialization.

Fix:

```ts
import './env';
```

at the top of the seed entrypoint.

Lesson:

> Environment must load before any client that reads environment variables.

Pattern:

```ts
import './env';
import { db } from '../db';
```

Anti-pattern:

```ts
import { db } from '../db';
import './env';
```

---

### Mistake 7: Verifying only exit code

A migration command can exit zero without proving the desired state.

Verify:

- migration records,
- tables,
- enums,
- expected columns,
- seed row counts.

Example queries:

```sql
select count(*) from drizzle.__drizzle_migrations;
select table_name from information_schema.tables where table_schema = 'public';
select enumlabel from pg_enum;
```

Lesson:

> Database success means correct state, not just a zero exit code.

---

## Migration Troubleshooting Checklist

When migration fails:

1. Check environment variables.
2. Check database connectivity:

   ```bash
   pg_isready -h localhost -p 5432
   ```

3. Inspect migration directory:
   - SQL files,
   - journal,
   - snapshots.
4. Check for orphaned migrations.
5. Check whether generate produced a full dump.
6. Inspect Postgres logs.
7. Run migrate in isolation.
8. Verify database state before and after.
9. Check seed environment loading.
10. Run the full setup command after isolated success.

---

## Migration Patterns

### Good Pattern: Deterministic setup

Setup should not generate schema changes.

### Good Pattern: Journal integrity

Every committed migration must be registered.

### Good Pattern: Idempotent provisioning

Setup should be safe to rerun.

### Good Pattern: Env-first initialization

Load environment before clients.

### Good Pattern: Verify database objects

Do not trust exit codes alone.

---

## Migration Anti-Patterns

| Anti-Pattern | Symptom | Fix |
|---|---|---|
| Orphaned SQL file | Migration not applied | Register in journal |
| Missing snapshots | Full-schema dumps | Commit snapshots or avoid generate |
| Generate in setup | Repeated destructive migrations | Remove from setup |
| Non-idempotent SQL | Type/table already exists | Guard or avoid regeneration |
| Silent failure | No CLI error | Check DB logs |
| Env after client | `DATABASE_URL` missing | Import env first |
| Exit-code-only verification | Wrong state assumed | Query DB state |

---

# 4.7 Third-Party SDK Integration Handbook

## Core Principle

SDK failures are usually caused by:

- missing declaration,
- wrong version,
- wrong subpath,
- outdated API usage,
- type drift,
- incorrect callback payloads.

Always inspect the installed package, not just documentation memory.

---

## Trigger.dev Lessons

### Mistake 1: Assuming a `/v4` subpath exists

Bad import:

```ts
import { TriggerClient } from '@trigger.dev/sdk/v4';
```

Reality:

- No published `/v4` subpath existed.

Fix:

```ts
import { TriggerClient } from '@trigger.dev/sdk';
```

Lesson:

> Inspect package exports before assuming subpaths.

Diagnostic:

```bash
node -e "console.log(require.resolve('@trigger.dev/sdk'))"
```

or inspect `node_modules/@trigger.dev/sdk/package.json`.

---

### Mistake 2: Missing dependency declaration

The package imported Trigger.dev but did not declare it.

Fix:

```bash
pnpm --filter @maison/config add @trigger.dev/sdk@^4.0.0
```

Lesson:

> Dynamic imports still require declared dependencies and valid module specifiers.

---

### Mistake 3: Wrong client configuration

Bad:

```ts
new TriggerClient({
  id: 'maison',
  apiKey: process.env['TRIGGER_SECRET_KEY']!,
});
```

Correct:

```ts
new TriggerClient({
  accessToken: process.env['TRIGGER_SECRET_KEY']!,
});
```

Lesson:

> Use the installed SDK’s type definitions to discover valid fields.

---

### Mistake 4: Wrong method name

Bad:

```ts
client.sendEvent(...)
```

Correct:

```ts
client.tasks.trigger<import('@trigger.dev/sdk').AnyTask>(task, payload);
```

Lesson:

> Method names change across SDK versions; verify against types.

---

## Stripe Lessons

### Mistake 1: Hardcoded API version

Bad:

```ts
apiVersion: '2025-08-27.basil'
```

Fix:

- Remove hardcoded version if optional.

Lesson:

> Let SDK types guide version literals.

---

### Mistake 2: Missing namespace type

Example:

- `Stripe.Refund.Status` unavailable.

Fix:

- Define a local union.

Lesson:

> When SDK namespace types disappear, create stable local types.

---

### Mistake 3: Passing `undefined` explicitly

Bad under strict optional properties:

```ts
{ amount: amountCents }
```

when `amountCents` may be `undefined`.

Better:

```ts
...(amountCents !== undefined ? { amount: amountCents } : {})
```

Lesson:

> Use conditional spreads for optional SDK payloads.

---

## Better Auth Lessons

### Mistake 1: Outdated client method

Bad:

```ts
forgetPassword
```

Correct:

```ts
requestPasswordReset
```

Lesson:

> Auth SDK APIs evolve; verify installed exports.

---

### Mistake 2: Wrong callback payload shape

Bad assumption:

```ts
{ email, url }
```

Actual:

```ts
{ user, url, token }
```

Fix:

```ts
user.email
```

Lesson:

> Callback payloads are part of the SDK contract; inspect types.

---

### Mistake 3: Better Auth React hooks crash during SSR (react-server export condition)

Symptom:

```text
TypeError: Cannot read properties of null (reading 'useRef')
```

Observed at runtime (`next start`) on any page that renders a Client Component calling Better Auth's `useSession()` (or any `authClient.useX()` hook) during the server render pass — e.g. the homepage ProductCard rendering a WishlistButton, or a PDP rendering a ReviewsSection.

Root cause:

- `better-auth/react`'s `useSession()` calls `useStore()` (from nanostores), which calls `useRef()`.
- `react@19.2.x` ships a `"react-server"` export condition (./react.react-server.js), where hooks (useRef, useState, useSyncExternalStore) are null stubs by design (React Server Components forbid hooks).
- When Turbopack bundles `better-auth/react` into an SSR server chunk (`[root-of-the-server]`), it selects the `react-server` export condition for the React import in that chunk.
- `null.useRef()` throws `TypeError: Cannot read properties of null (reading 'useRef')`.
- Client Components DO run on the server (SSR renders their initial HTML); the hooks execute, and the react-server build of React has no dispatcher (null).

Why Stillwater does not hit this:

- Stillwater never invokes `useSession` (or any Better Auth React hook) during SSR. It only uses `authClient.signIn.social()` / `.magicLink()` inside event handlers (dynamic imports). No Better Auth React hook runs during the server render pass — the null-hook path is never reached.

Fix — use a ClientOnly boundary:

```tsx
// CORRECT: defer the component to the client pass via useSyncExternalStore
import { useSyncExternalStore } from 'react';

const emptySubscribe = () => noopUnsubscribe;
const getClientSnapshot = () => true;
const getServerSnapshot = () => false;

export function ClientOnly({ children, fallback = null }) {
  const isHydrated = useSyncExternalStore(
    emptySubscribe,
    getClientSnapshot,
    getServerSnapshot,
  );
  return isHydrated ? children : fallback;
}

// Usage: wraps any component that calls useSession() or other Better Auth hooks:
<ClientOnly fallback={null}>
  <WishlistButton productSlug={product.slug} productName={product.name} />
</ClientOnly>
```

Why this works:

- `useSyncExternalStore` with `getServerSnapshot: () => false` is SSR-safe — it returns false on the server, so children never render during SSR.
- On the client after hydration, `getClientSnapshot` returns true → children mount, `useSession()` fires with the real React dispatcher.
- Hooks are called unconditionally on every render → Rules of Hooks satisfied.
- `useSyncExternalStore` does NOT call useRef/useState from a different package's bundled react — it is a React 18+ built-in primitive.

Why `next/dynamic({ ssr: false })` is NOT the fix for Server Components:

- Next.js 16 forbids `ssr: false` inside Server Components: the build fails with "ssr: false is not allowed with next/dynamic in Server Components."
- The PDP (`/products/[slug]/page.tsx`) is a Server Component (it fetches via `api()` server caller). You cannot use `next/dynamic({ ssr: false })` directly in it.
- `next/dynamic({ ssr: false })` IS valid inside Client Components (e.g. ProductCard). For consistency, use the ClientOnly pattern everywhere.

Lesson:

> Better Auth React hooks (`useSession`, `authClient.useX()`) must not execute during SSR. Wrap the calling component in a `ClientOnly` boundary. `next/dynamic({ ssr: false })` is only valid inside Client Components, not Server Components. See Stillwater SKILL Lesson 89.

---

## Sanity Lessons

### Mistake: Putting `hotspot` on an array instead of the image member

Bad shape:

```ts
{
  type: 'array',
  options: { hotspot: true },
  of: [{ type: 'image' }]
}
```

Better:

```ts
{
  type: 'array',
  of: [
    {
      type: 'image',
      options: { hotspot: true }
    }
  ]
}
```

Lesson:

> Schema options must be placed on the correct member type.

---

## React Email Lessons

### Mistake: Keeping an unused dependency

The dependency was declared but never imported.

Fix:

- Remove it.

Lesson:

> Unused dependencies are liabilities, not assets.

---

## tRPC Lessons

### Mistake 1: Procedure named with a JavaScript reserved word

Symptom:

```text
Error: Reserved words used in `router({})` call: apply
```

The tRPC adapter route (`/api/trpc/[trpc]/route.ts`) imports `appRouter` from the API package. During `next build`, Next.js statically analyzes this route to collect page data. The tRPC router constructor runs at module load time and throws immediately when it encounters a reserved word as a procedure name.

Root cause:

- A procedure was named `apply` in `packages/api/src/routers/trade.ts`.
- `apply` is `Function.prototype.apply` — a core JavaScript mechanism.
- tRPC v11 validates all router/procedure keys at construction time against a list of JavaScript built-in reserved words.
- This error only surfaces at `next build` time, not at `pnpm check-types` time, because the router constructor executes at module load (runtime), not during static type analysis.

Fix:

```diff
// packages/api/src/routers/trade.ts
- apply: protectedProcedure
+ submitApplication: protectedProcedure

// apps/web/src/app/(shop)/trade/page.tsx
- const applyMutation = trpc.trade.apply.useMutation();
+ const applyMutation = trpc.trade.submitApplication.useMutation();
```

Lesson:

> tRPC v11 rejects JavaScript reserved words as procedure names. Use domain-specific verb-noun pairs. The `pnpm build` gate catches this, but `pnpm check-types` does not — the constructor runs at module load, not during static analysis.

Prevention:

- Name procedures with domain-specific verb-noun pairs: `submitApplication`, `listOrders`, `getProfile`.
- Avoid any name that collides with `Object.prototype`, `Function.prototype`, or `Array.prototype` methods.
- Reserved words to avoid: `apply`, `call`, `bind`, `constructor`, `toString`, `valueOf`, `hasOwnProperty`, `isPrototypeOf`, `propertyIsEnumerable`, `toLocaleString`, `__proto__`.

Pattern:

```text
good: submitApplication, createOrder, getProfile, listProducts
bad:  apply, call, bind, constructor, toString, valueOf
```

### Mistake 2: Procedure naming too generic

Example:

```typescript
export const someRouter = router({
  get: publicProcedure.query(...),
  create: protectedProcedure.mutation(...),
  update: protectedProcedure.mutation(...),
  delete: protectedProcedure.mutation(...),
});
```

This works but creates ambiguity when procedures are called:

```typescript
trpc.some.get(...)    // what does "get" mean?
trpc.some.create(...) // what is being created?
```

Better:

```typescript
export const someRouter = router({
  getProfile: publicProcedure.query(...),
  createOrder: protectedProcedure.mutation(...),
  updateAddress: protectedProcedure.mutation(...),
  deleteItem: protectedProcedure.mutation(...),
});
```

Lesson:

> Procedure names should be self-documenting. The tRPC procedure path (`some.getProfile`) is visible in network logs, error messages, and analytics. Generic names make debugging harder.

---

### Mistake 3: Routing public data through session-aware server caller forces routes dynamic

Symptom:

- `pnpm build` emits `DYNAMIC_SERVER_USAGE` warnings for public routes (`/`, `/collections`, `/products`).
- The affected routes render as `ƒ` (Dynamic) instead of `○` (Static) in the build route table.
- During the static-generation probe, the page's `try/catch` swallows the `DYNAMIC_SERVER_USAGE` error and renders an **empty shell** (e.g. an empty product grid on the homepage).
- Prior handoff documents may misdiagnose these as "cosmetic" or "expected" — the build log explicitly names the failing route.

Root cause:

- The server-side tRPC caller (`api()`) unconditionally calls `headers()` from `next/headers` to build the request context.
- In Next.js 16, any route whose render path touches `headers()`, `cookies()`, or `searchParams` is **forced dynamic** (`ƒ`) — the static-generation pass cannot prerender it.
- If a **public, cacheable** page (homepage, collections, product listings) routes through this session-aware caller, it loses all static rendering benefits: no ISR, no PPR, no edge caching, and an empty shell during the static probe.
- This is a **scaffolding gap** — the architectural boundary between public and auth-required data fetching is missing.

Why it matters for DTC e-commerce:

- The homepage is the highest-traffic route. An empty product grid in the prerender is a visible brand defect.
- Static routes are edge-cacheable and return complete HTML on first paint. Dynamic routes require a server round-trip on every request.

Fix — introduce a session-free public caller (`apiPublic`):

```typescript
// apps/web/src/lib/trpc/server.ts
import { appRouter, createContext } from '@maison/api';

const TRPC_ENDPOINT = 'http://localhost:3000/api/trpc';

/** Session-aware caller — uses next/headers → forces route dynamic. */
export async function api() {
  const heads = new Headers(await headers());
  const req = new Request(TRPC_ENDPOINT, { headers: heads });
  const ctx = await createContext({ req });
  return appRouter.createCaller(ctx);
}

/** Session-free caller — no next/headers → route can be static. */
export async function apiPublic() {
  const req = new Request(TRPC_ENDPOINT);
  const ctx = await createContext({ req });
  return appRouter.createCaller(ctx);
}
```

Then switch the public page:

```typescript
// Before (forces dynamic):
import { api } from '@/lib/trpc/server';
const caller = await api();

// After (can be static):
import { apiPublic } from '@/lib/trpc/server';
const caller = await apiPublic();
```

Why this works:

- `apiPublic()` builds context with an empty `Request` — no `headers()` call, no `next/headers` import.
- `createContext` runs `getSessionWithTimeout(req.headers)` against empty headers → returns `null` session.
- `publicProcedure` never reads `ctx.session` — a null session is exactly correct.
- Both callers reuse the **same `appRouter`** — zero duplicated query/shaping logic. Only the transport context differs.
- The route is now `○ Static` in the build table; the `DYNAMIC_SERVER_USAGE` warning is eliminated.

When to use each caller:

| Caller | Use when | Route type |
|---|---|---|
| `api()` | Page needs a session (account, admin, cart, checkout) | `ƒ Dynamic` (by design) |
| `apiPublic()` | Page only calls `publicProcedure`s (browse, search, collections) | `○ Static` (prerendered) |

When to use `apiPublic()`:

- Homepage product/collection grids
- Collection listing pages
- Product listing pages (PLP) — even though `searchParams` may still force dynamic, the caller should not add `headers()` on top
- Search results pages
- Any page that only calls `publicProcedure` and does not need auth context

When `apiPublic()` is NOT sufficient:

- Pages that call `protectedProcedure` or `adminProcedure` — these throw `UNAUTHORIZED` with a null session
- Pages that need the user's session for personalized content (wishlist, loyalty points)
- Pages that read cookies or headers directly

Related `DYNAMIC_SERVER_USAGE` behavior:

- `searchParams` access also forces a route dynamic (correct for filter/search pages that need URL state)
- The `DYNAMIC_SERVER_USAGE` warning is non-fatal — the build completes — but it means the route is server-rendered on every request
- For guarded routes (`/account/*`, `/admin/*`), `DYNAMIC_SERVER_USAGE` is expected and correct — those routes need `headers()` for session verification
- For public routes, `DYNAMIC_SERVER_USAGE` is a **real bug** — it means an empty prerender or a lost static-rendering opportunity

Pattern source: Stillwater ADR V16-1 ("No apiCaller() → no headers() → no streaming → complete HTML returned") and Stillwater's `index-routes-no-apiCaller.test.ts` regression tests.

Lesson:

> The server-side tRPC caller is the single architectural chokepoint for static vs dynamic rendering in Next.js 16. If a public page calls `api()`, it becomes dynamic — not because the page needs a session, but because the caller unconditionally imports `next/headers`. Split the caller into session-aware (`api()`) and session-free (`apiPublic()`) variants. Use `apiPublic()` for all public, cacheable content. This is the single highest-impact fix for Core Web Vitals on DTC storefronts.

---

## Vitest Lessons

### Mistake: Config imports a plugin not declared

`vitest.config.ts` imported `@vitejs/plugin-react`, but the package did not declare it.

Fix:

```bash
pnpm --filter @scope/pkg add -D @vitejs/plugin-react
```

Lesson:

> Tooling config files are real code and need real dependencies.

---

## SDK Integration Checklist

When an SDK import or type fails:

1. Verify the package is declared in the consuming workspace.
2. Verify the version exists.
3. Inspect `package.json` `exports`.
4. Inspect installed type definitions.
5. Search for deprecated or renamed APIs.
6. Check method signatures and callback payloads.
7. Avoid hardcoded version literals unless required.
8. Use conditional spreads for optional payloads.
9. Verify with type-check and package tests.
10. Record latent issues hidden by tsconfig include.
11. For tRPC routers: verify procedure names are not JavaScript reserved words (`apply`, `call`, `bind`, etc.) — this error only surfaces at `pnpm build`, not `pnpm check-types`.
12. For public pages: verify the server caller does not call `next/headers` unless the route genuinely needs a session — `headers()` forces the route dynamic, breaking static generation. Use a session-free caller (`apiPublic()`) for `publicProcedure`-only pages.

---

## SDK Patterns

### Good Pattern: Inspect installed types

`node_modules/<pkg>` is truth.

### Good Pattern: Use real exports

Do not invent subpaths.

### Good Pattern: Bind generics explicitly when needed

Especially for string task identifiers or generic SDK APIs.

### Good Pattern: Local stable types for unstable namespaces

Useful when SDK namespace types change.

---

## SDK Anti-Patterns

| Anti-Pattern | Symptom | Fix |
|---|---|---|
| Invented subpath | Module not found | Inspect exports |
| Missing declaration | pnpm resolution failure | Add dependency |
| Old method names | Missing property | Use installed API |
| Wrong callback shape | Runtime undefined fields | Inspect payload types |
| Hardcoded API version | Type literal mismatch | Remove/update |
| Explicit undefined | Strict optional error | Conditional spread |
| Config-only dependency missing | Tool fails | Add devDep |

---

# 4.8 React and Next.js Handbook

## Core Principle

React and Next.js failures often involve:

- event type changes,
- async handlers,
- JSX text escaping,
- metadata generation,
- route handler conventions,
- server/client boundaries.

---

## React 19 Event Types

### Mistake: Using deprecated `React.FormEvent`

Bad:

```ts
function onSubmit(e: React.FormEvent<HTMLFormElement>) {
  e.preventDefault();
}
```

Better:

```ts
function onSubmit(e: React.SubmitEvent) {
  e.preventDefault();
}
```

Why:

- React 19 deprecates `FormEvent`.
- `onSubmit` expects a submit event handler.
- `SubmitEvent` still has `preventDefault()`.

Lesson:

> Use the event type that matches the DOM handler.

**Version note:** `React.SubmitEvent` requires `@types/react` ≥ 19.2.10
(DefinitelyTyped PR #74383, January 2026). Projects on earlier React 19
versions may not have this type — verify against installed definitions
before applying this pattern.

---

## Async Handlers

### Mistake: Floating promises in JSX handlers

Bad:

```tsx
onClick={() => doAsync()}
```

Better:

```tsx
onClick={async () => {
  await doAsync();
}}
```

Or:

```tsx
onClick={() => {
  void doAsync();
}}
```

Lesson:

> Promises created in handlers must be handled.

---

### Mistake: `async` without `await`

Bad:

```ts
export async function Image() {
  return new ImageResponse(...);
}
```

Better:

```ts
export function Image() {
  return new ImageResponse(...);
}
```

Lesson:

> Do not mark functions async unless they await something.

---

## JSX Text Escaping

### Mistake: Unescaped apostrophes and quotes

Bad:

```tsx
<p>We've got "great" things.</p>
```

Better:

```tsx
<p>We&apos;ve got &quot;great&quot; things.</p>
```

Lesson:

> JSX text has stricter escaping rules than ordinary strings.

---

## Template Literals

### Mistake: Raw numbers in template literals

Bad:

```ts
`${count} items`
```

Better under strict lint:

```ts
`${String(count)} items`
```

Lesson:

> Explicit string conversion avoids edge-case stringification issues.

---

### Mistake: `String(undefined)` in metadata

Bad:

```ts
`Search: ${String(q)}`
```

If `q` is undefined, this becomes:

```text
Search: undefined
```

Better:

```ts
`Search: ${q ?? ''}`
```

Lesson:

> Choose fallbacks deliberately for optional strings.

---

## Console Usage

### Mistake: `console.log` in production handlers

Fix:

- use `console.warn` or `console.error` if allowed,
- or use structured logging.

Lesson:

> Production diagnostics should use appropriate severity levels.

---

## Server/Client Boundary: Better Auth React Hooks

### Mistake: Calling `useSession()` during SSR in a Client Component

Bad:

```tsx
'use client';
import { useSession } from '@maison/auth/client';

export function WishlistButton() {
  const { data: session } = useSession(); // CRASH during SSR
}
```

Better:

```tsx
// WishlistButton remains unchanged, but the PARENT wraps it:
<ClientOnly fallback={null}>
  <WishlistButton productSlug={product.slug} />
</ClientOnly>
```

Why:

- Client Components render on the server (SSR produces initial HTML).
- `useSession()` → `useStore()` → `useRef()` — but Turbopack selects React's `react-server` export for the SSR chunk, where `useRef` is a null stub.
- `null.useRef()` throws `TypeError: Cannot read properties of null (reading 'useRef')`.

Lesson:

> Any Client Component calling Better Auth React hooks (`useSession`, `authClient.useX()`) must be wrapped in a `ClientOnly` boundary at the call site. Do NOT use `next/dynamic({ ssr: false })` in Server Components — it is forbidden by Next.js 16.

### Note: The `api()`/`apiPublic()` contract is a Server Component concern

The rendering-strategy split (`api()` for session-aware pages, `apiPublic()` for session-free public pages) applies to **Server Components** that call the server-side tRPC caller. Client Components (`'use client'`) use the **client-side** tRPC caller (`trpc` from `@/lib/trpc/client`) with React Query — they never call `api()` or `apiPublic()`. When auditing rendering strategy, check whether the page is a Server Component or Client Component before asserting the caller contract. See Playbook 16 Scenario B for the full analysis.

---

## Next.js 16 Static/Dynamic Route Boundary

In Next.js 16, routes are either **static** (`○`) or **dynamic** (`ƒ`). Static routes are prerendered at build time and served from edge/CDN. Dynamic routes are server-rendered on every request. The following APIs force a route dynamic:

| API | Import | Effect |
|---|---|---|
| `headers()` | `next/headers` | Reads request headers → forces dynamic |
| `cookies()` | `next/headers` | Reads request cookies → forces dynamic |
| `searchParams` | Page prop `Promise<...>` | Reads URL query params → forces dynamic |
| `useSearchParams()` | `next/navigation` | Client-side search params → forces dynamic |

When a route is forced dynamic during the static-generation probe, Next.js emits:

```text
[route-name] Failed to fetch data: Error: Dynamic server usage: Route /path couldn't be rendered statically because it used `headers`.
```

### This warning is NOT always cosmetic

A common misdiagnosis is to treat `DYNAMIC_SERVER_USAGE` warnings as "expected" or "cosmetic" for all routes. This is wrong when:

- The affected route is **public and cacheable** (homepage, collections, product listings) — an empty prerender means a visible brand defect (e.g. empty product grid)
- The route loses ISR/PPR/edge-caching benefits — every request hits the server
- The route's data does not actually need request context (session, headers) — the dynamic forcing is caused by the server caller, not the page's own logic

The warning IS expected and correct when:
- The route is auth-guarded (`/account/*`, `/admin/*`) and needs `headers()` for session verification
- The route reads `searchParams` for URL-driven state (filter/search pages)

### Diagnosis

To determine whether a `DYNAMIC_SERVER_USAGE` warning is a bug or expected:

1. Check the route table in `pnpm build` output — is the route `○` or `ƒ`?
2. If `ƒ`, check whether the page imports `api()` (session-aware caller) — if so, the caller's `headers()` call is the cause
3. Check whether the page actually needs a session — if it only calls `publicProcedure`s, it should use `apiPublic()` instead
4. Check whether the page reads `searchParams` — if so, `ƒ` is correct for that route

### Prevention

- Use `apiPublic()` for all public, cacheable pages (see §4.7 Mistake 3)
- Use `api()` only for pages that genuinely need a session
- Do not import the session-aware caller in pages that only browse public content

---

### Mistake: IntersectionObserver callback does not fire for already-visible elements

Symptom:

- A page renders elements with a `.reveal` class (initially `opacity: 0` via CSS).
- An `IntersectionObserver` in a `useEffect` is supposed to add `.visible` (`opacity: 1`) when elements enter the viewport.
- Elements below the fold animate in correctly on scroll.
- The first few elements in the initial viewport stay at `opacity: 0` forever — the page appears blank.

Root cause:

- `IntersectionObserver` does not reliably fire `isIntersecting: true` for elements already in the viewport when the observer is constructed inside a post-hydration `useEffect`.
- This is a timing issue: React hydrates the DOM, `useEffect` runs, the observer is constructed — but the browser has already computed which elements are visible, and the observer's initial callback does not fire for them.

Fix:

```ts
useEffect(() => {
  const observer = new IntersectionObserver(/* ... */);
  document.querySelectorAll('.reveal').forEach((el) => observer.observe(el));

  // Fallback: check elements already in viewport after first paint
  requestAnimationFrame(() => {
    const vh = window.innerHeight;
    document.querySelectorAll('.reveal:not(.visible)').forEach((el) => {
      const rect = el.getBoundingClientRect();
      if (rect.top < vh && rect.bottom > 0) {
        el.classList.add('visible');
        observer.unobserve(el);
      }
    });
  });

  return () => observer.disconnect();
}, [/* deps */]);
```

Lesson:

> Do not strip the `requestAnimationFrame` fallback as "redundant" with the observer — it covers a real first-paint timing gap that the observer cannot detect.

---

### Mistake: `next/image fill` with grid placement on the `<Image>` element

Symptom:

- A CSS Grid layout has 3 images in an asymmetric arrangement.
- Each `<Image>` has `fill` plus `style={{ gridColumn: '1 / 2', gridRow: '1 / 3' }}`.
- All 3 images overlap at full section size (e.g. 1280×577px), filling the entire grid area as a single broken mess.
- No images appear in their intended grid cells.

Root cause:

- `<Image fill>` renders the `<img>` with `position: absolute` (so it stretches to fill its nearest positioned ancestor).
- An absolutely-positioned element is **removed from CSS Grid flow** — `gridColumn` and `gridRow` set on the `<Image>` style have no effect.
- The images position themselves relative to a distant ancestor (typically the section root) instead of their intended grid cell.

Fix:

```tsx
// ❌ Wrong — grid placement on the absolutely-positioned Image
<Image src={...} fill style={{ gridColumn: '1 / 2', gridRow: '1 / 3' }} />

// ✅ Correct — wrapper div IS the grid item, Image fills it
<div style={{ position: 'relative', gridColumn: '1 / 2', gridRow: '1 / 3', overflow: 'hidden' }}>
  <Image src={...} fill style={{ objectFit: 'cover' }} />
</div>
```

The wrapper `<div>` must have:
- `position: 'relative'` (or `'absolute'` inside a positioned ancestor) — so the `fill` Image fills the div, not a distant ancestor.
- `gridColumn` / `gridRow` — grid placement on the div (a normal flow element), not the Image.
- `overflow: 'hidden'` — standard practice for cropped fill images.

Lesson:

> `fill` removes `<Image>` from grid flow. Grid placement must be on a wrapper div, never on the `<Image>` itself.

---

### Mistake: `useSearchParams()` without `<Suspense>` breaks static prerendering

Symptom:

- A page that previously rendered as `○ Static` now renders as `ƒ Dynamic` after adding a Client Component that calls `useSearchParams()`.
- Or, the build fails outright with:

```text
⨯ useSearchParams() should be wrapped in a suspense boundary at page "/cart"
```

Root cause:

- In Next.js 16, `useSearchParams()` in a Client Component causes a **CSR bailout** during static prerendering.
- If the component is not wrapped in a `<Suspense>` boundary, Next.js either:
  - Fails the build (hard error for statically-prerendered pages like `/cart`), or
  - Silently downgrades the route from `○ Static` to `ƒ Dynamic` (no build error, but the page loses static rendering and edge caching).
- A `<Suspense>` boundary in a **layout** only protects the specific component it wraps — other `useSearchParams()` consumers on individual pages still need their own Suspense wrappers.

Fix:

```tsx
// Layout level — protects the ScrollRevealTrigger
<Suspense fallback={null}>
  <ScrollRevealTrigger />
</Suspense>

// Page level — protects SortSelect on /products
<Suspense fallback={null}>
  <SortSelect currentSort={sort} />
</Suspense>
```

`fallback={null}` is correct for components that render nothing visible (side-effect-only triggers) or whose initial state is non-critical.

Lesson:

> Every `useSearchParams()` consumer in a statically-prerendered page needs its own `<Suspense>` boundary. A layout-level Suspense does not protect other consumers on child pages.

---

### Mistake: `useEffect([])` misses client-side navigation

Symptom:

- A page sets up an `IntersectionObserver` or DOM watcher in `useEffect` with an empty dependency array `[]`.
- On initial page load, elements below the fold animate in correctly.
- When the user navigates to a different URL via `<Link>` (client-side navigation), new elements render with the expected class names but never animate — they stay hidden until a full page reload.

Root cause:

- Client-side navigation via `<Link>` changes the URL and renders new page content **without remounting the layout**.
- `useEffect(() => { ... }, [])` only runs once on mount — it never re-runs when the URL changes.
- New `.reveal` elements (or other hook-managed DOM elements) render after the effect has already set up its observer, so they are never observed.

Fix:

```ts
import { usePathname, useSearchParams } from 'next/navigation';

export function useScrollReveal() {
  const pathname = usePathname();
  const searchParams = useSearchParams();

  useEffect(() => {
    const observer = new IntersectionObserver(/* ... */);
    document.querySelectorAll('.reveal').forEach((el) => observer.observe(el));
    return () => observer.disconnect();
  }, [pathname, searchParams]); // ← re-runs on every route/query change
}
```

The cleanup function (returning `() => observer.disconnect()`) is essential: it tears down the old observer before the new one is constructed.

Lesson:

> `useEffect([])` in a shared layout component misses client-side navigations. Add `usePathname()` and `useSearchParams()` as dependencies so the effect re-runs on every route change.

---

## React/Next.js Checklist

When React or Next.js lint/type issues appear:

1. Check event handler types.
2. Check whether async functions actually await.
3. Check JSX text escaping.
4. Check template literal interpolation types.
5. Check metadata optional values.
6. Check console usage.
7. Check server/client component boundaries.
8. Verify route handler conventions.
9. Wrap Better Auth React hooks (`useSession`) in a `ClientOnly` boundary — never let them execute during SSR.
10. For `next/image fill` in CSS Grid layouts: verify grid placement is on a wrapper `<div>`, not the `<Image>` itself.
11. For `useSearchParams()` consumers: verify each is wrapped in `<Suspense>` if the page is statically prerendered.

---

# 4.9 Testing and Vitest Handbook

## Core Principle

Test failures can be caused by:

- broken syntax,
- missing dependencies,
- empty suites,
- malformed mocks,
- incorrect assertions.

Do not assume the cause without inspection.

---

## Mistakes and Issues Encountered

### Mistake 1: Missing test plugin dependency

`vitest.config.ts` imported a plugin not declared.

Fix:

- Add the plugin as a dev dependency.

Lesson:

> Test configuration is code and must satisfy dependency rules.

---

### Mistake 2: Empty test suite causing failure

Vitest may exit nonzero when no test files are found.

Options:

- add tests,
- configure `passWithNoTests`,
- document the condition.

Lesson:

> A failing test script may mean “no tests,” not “broken tests.”

---

### Mistake 3: Malformed mock causing misleading parse error

Symptom:

```text
SyntaxError: ',' expected. (16:11)
```

Real cause:

- Missing closing parenthesis on the previous line.

Lesson:

> Parsers often report the token after the real fault site.

Diagnostic patterns:

- count parentheses,
- compare with sibling lines,
- use TypeScript parser diagnostics,
- inspect raw bytes.

---

### Mistake 4: Async-deferred-to-null file reads in contract tests

Symptom:

- A source-contract test's `read()` helper returns `string | null` via `readFile(...).catch(() => null)`.
- Every assertion site now holds a `string | null`, even after runtime `expect(x).not.toBeNull()` (see TS Mistake 17).
- A missing file is swallowed to `null` and surfaces as a confusing regex-assertion failure instead of a loud "file not found" error.

Root cause:

- `readFile(...).catch(() => null)` erases the ENOENT signal *and* widens the producer type to `string | null`.
- The Stillwater reference (`index-routes-no-apiCaller.test.ts`) avoids this entirely: it uses **synchronous `readFileSync`** into `string`-typed module-scoped `const`s — no `Promise`, no `.catch(() => null)`, no null branch.

Bad:

```ts
const read = (rel: string) =>
  readFile(join(APP_ROOT, rel), 'utf8').catch(() => null);
// ...
for (const rel of PUBLIC_TRPC_PAGES) {
  it(`${rel} imports apiPublic`, async () => {
    const src = await read(rel);          // string | null
    expect(src, `${rel} not found`).not.toBeNull(); // runtime-only — not a type guard
    expect(src).toMatch(/import.*apiPublic/);        // TS18047 on any .method() call
  });
}
```

Better (synchronous, throwing, null-free — mirrors Stillwater):

```ts
const read = (rel: string): string =>
  readFileSync(join(APP_ROOT, rel), 'utf8');
// ...
for (const rel of PUBLIC_TRPC_PAGES) {
  it(`${rel} imports apiPublic`, () => {
    const src = read(rel);                // string — always
    expect(src).toMatch(/import.*apiPublic/);
  });
}
```

This also improves the failure mode: a missing file throws a readable `ENOENT` at `readFileSync` (the Vitest spec name + file path are in the stack trace) instead of being silently swallowed to `null`.

Lesson:

> Contract test file reads should be **synchronous and throwing**. Synchronous reads keep the producer type `string` (no null branch → no `TS18047`), throw loudly on missing files, and avoid async/await boilerplate in tests that need no I/O mocking.

Prevention:

- Use `readFileSync` (not `readFile().catch(() => null)`) for test sources.
- Remove redundant `expect(x).not.toBeNull()` guards after switching to a throwing producer — the throw does that job.
- If you need async reads (e.g. testing a network client), keep the producer's return type `Promise<T>` and narrow with `await` + a real null check before deref.

---

## Testing Checklist

When tests fail:

1. Determine whether the runner starts.
2. Determine whether test files exist.
3. Check for parse errors.
4. Check config dependencies.
5. Check mocks for balanced delimiters.
6. Run the single failing test file.
7. Run the whole package suite.
8. Distinguish regression from empty suite.

---

# 4.10 Tooling, Automation, and Diagnostics Handbook

## Core Principle

Agents often fail not because they lack knowledge, but because they misuse tooling.

Common tooling traps:

- misleading error lines,
- exit-code masking,
- ANSI output,
- quote escaping,
- hand-mapped scripts,
- incomplete verification.

---

## Mistake 1: Trusting the reported error line blindly

Parser errors often point to the next token, not the missing delimiter.

Example: Prettier reported a fatal syntax error on **line 16** of `trpc.test.ts`;
the real defect was an unclosed parenthesis on **line 15**. The parser simply
failed at the first token it could not reconcile after the missing delimiter.

Rule:

> Inspect neighboring lines and delimiter balance.

Diagnostics:

- Count `()`, `{}`, `[]` on preceding lines.
- Inspect raw bytes for hidden characters:

  ```bash
  cat -A <file>      # $ = line end, ^I = tab, ^M = stray CR
  ```

- Use an AST-aware parser diagnostic if available.

---

## Mistake 2: Masking exit codes with pipes

Bad:

```bash
command | tail
echo $?
```

Better:

```bash
command | tail
echo "${PIPESTATUS[0]}"
```

Or:

```bash
set -o pipefail
```

Rule:

> Verify the exit code of the actual failing command.

---

## Mistake 3: Missing errors hidden by spinners or ANSI output

Some CLI tools overwrite error lines.

Rule:

> If output is silent but exit code fails, inspect logs and strip ANSI sequences.

---

## Mistake 4: Using fragile edit operations with embedded quotes

When editing lines containing quotes, structured edit tools may fail due to JSON escaping issues.

Rule:

- For many mechanical replacements, use a script.
- For scripts, use authoritative input.
- Validate expected characters before replacing.

---

## Mistake 5: Hand-mapping mechanical fixes

A manually constructed fix map caused mismatches and file corruption.

Better:

- Generate the fix list from ESLint JSON.
- Validate each expected character.
- Apply replacements in reverse column order.
- Restore from git if corruption occurs.

Rule:

> Use machine-readable sources for mechanical transformations.

---

## Mistake 6: Declaring completion before verification

A batch can be "applied" but not "verified."

Rule:

> Do not report success until the relevant gate passes.

---

## Mistake 7: `.gitignore` `lib/` pattern hides Next.js `apps/*/src/lib/` in Python+JS monorepos

Symptom: A newly created test file in `apps/web/src/lib/__tests__/` does not appear in `git status` as untracked, even though the file exists on disk. `git check-ignore -v` shows the Python `lib/` pattern is matching it.

Root cause: The `.gitignore` has a `lib/` entry (for Python `lib/` directories — `.eggs/`, `dist/`, `sdist/`, etc.) that also matches `apps/web/src/lib/`. This is a common bleed in monorepos that mix Python tooling with JavaScript/TypeScript applications.

Fix: Add negation rules immediately after the `lib/` entry:

```gitignore
lib/
!apps/web/src/lib/
!apps/web/src/lib/**
```

Why this happens: Git's `.gitignore` treats `lib/` as a directory pattern that matches any directory named `lib` at any depth. The negation `!apps/web/src/lib/` un-ignores the specific directory, and `!apps/web/src/lib/**` un-ignores its contents.

Rule:

> In mixed-language monorepos, audit `.gitignore` for patterns that bleed across ecosystems. Python's `lib/`, `dist/`, `build/`, `*.egg-info/` can hide JavaScript source files. Add negations for application source directories.

Diagnostic:

```bash
git check-ignore -v apps/web/src/lib/__tests__/your-file.ts
# If the output shows a Python-era pattern (lib/, dist/, build/), add negation
```

---

## Tooling Patterns

### Good Pattern: Use machine-readable diagnostics

Examples:

```bash
npx eslint . --format json
tsc --traceResolution
npm view <pkg> versions --json
```

### Good Pattern: Validate before mutating

For scripts:

- check file exists,
- check line exists,
- check expected character exists,
- then replace.

### Good Pattern: Recover with git

If a script corrupts files:

```bash
git checkout -- <files>
```

Then rerun a safer script.

### Good Pattern: Probe behavior

Use small probe files to test ignore rules, formatting, or config behavior.

---

# 5. Pattern Catalog

These are reusable good patterns extracted from the entire session history.

## 5.1 Diagnostic Patterns

### Pattern: Reproduce the exact failing command

Use the same command, package manager, and workspace filter.

### Pattern: Classify the gate

Determine whether the failure is install, type, lint, format, test, migration, runtime, or hook.

### Pattern: Use authoritative sources

Registry metadata, package exports, type definitions, ESLint JSON, database logs.

### Pattern: Build a hypothesis table

Prevents tunnel vision.

### Pattern: Verify state before and after

Especially for databases and generated artifacts.

---

## 5.2 Dependency Patterns

### Pattern: Validate versions before editing manifests

```bash
npm view <pkg> versions --json
```

### Pattern: Delete unused dependencies

Unused dependencies should be removed, not version-bumped.

### Pattern: Declare every imported package

Especially in pnpm workspaces.

### Pattern: Exact-pin sensitive packages

Use when caret ranges admit deprecated versions.

---

## 5.3 TypeScript Patterns

### Pattern: Fix root exported types

One canonical type can fix many consumer errors.

### Pattern: Canonicalize driver types

Choose the production driver as the public type surface.

### Pattern: Shape data at boundaries

Routers should return clean UI contracts.

### Pattern: Await factories before member access

```ts
const caller = await api();
```

### Pattern: Use conditional spreads for optional properties

Avoid explicit `undefined`.

### Pattern: Guard indexed access

Use optional chaining and fallbacks.

### Pattern: Name tRPC procedures with domain-specific verb-noun pairs

```ts
// Good — self-documenting, no reserved word collisions
export const tradeRouter = router({
  submitApplication: protectedProcedure.mutation(...),
  myStatus: protectedProcedure.query(...),
  list: adminProcedure.query(...),
  approve: adminWriteProcedure.mutation(...),
});

// Bad — generic, ambiguous, potential reserved word collision
export const tradeRouter = router({
  apply: protectedProcedure.mutation(...),
  get: protectedProcedure.query(...),
  list: adminProcedure.query(...),
});
```

Why:

- Avoids JavaScript reserved words (`apply`, `call`, `bind`, `constructor`, etc.) which tRPC v11 rejects at router construction time.
- Makes the tRPC procedure path self-documenting in network logs and error messages.
- Prevents ambiguity when multiple routers have similar operations.

### Pattern: Session-free public caller for cacheable routes

Public pages that only call `publicProcedure`s should use a session-free server caller (`apiPublic()`) instead of the session-aware `api()`. This preserves static rendering (`○`) and avoids `DYNAMIC_SERVER_USAGE` warnings.

```typescript
// Good — public page uses session-free caller:
import { apiPublic } from '@/lib/trpc/server';
const caller = await apiPublic();
const products = await caller.products.list({ limit: 8 });

// Bad — public page uses session-aware caller:
import { api } from '@/lib/trpc/server';
const caller = await api();  // calls next/headers → forces route dynamic
const products = await caller.products.list({ limit: 8 });
```

When to use each:

- `api()` — page needs a session (account, admin, cart, checkout)
- `apiPublic()` — page only calls `publicProcedure`s (browse, search, collections, homepage)

See §4.7 Mistake 3 for the full pattern and rationale.

---

## 5.4 ESLint Patterns

### Pattern: Separate config failure from code debt

If ESLint cannot run, fix infrastructure first.

### Pattern: Use flat config directly

Avoid legacy compatibility shims for flat configs.

### Pattern: Batch lint fixes

Mechanical first, semantic second.

### Pattern: Use ESLint JSON for mechanical fixes

Avoid hand-mapping from terminal output.

---

## 5.5 Prettier Patterns

### Pattern: Treat parse errors as syntax failures

Do not merely reformat.

### Pattern: Format only reported files

Unless broad formatting is approved.

### Pattern: Run Prettier after ESLint autofix

Restore formatting fixed point.

### Pattern: Probe ignore behavior

Use temporary dirty files.

---

## 5.6 Migration Patterns

### Pattern: Setup should be deterministic

No schema generation during provisioning.

### Pattern: Journal and migrations must be consistent

Every migration file must be registered.

### Pattern: Load environment before clients

Especially in seed scripts.

### Pattern: Inspect database logs for silent failures

CLI output may hide real errors.

---

## 5.7 SDK Patterns

### Pattern: Inspect installed SDK types

Do not rely on memory.

### Pattern: Use real exports and methods

Do not invent subpaths.

### Pattern: Remove hardcoded version literals when optional

Let SDK types guide compatibility.

### Pattern: Define local stable types for unstable SDK namespaces

Useful for status unions and similar types.

---

## 5.8 React Patterns

### Pattern: Use handler-specific event types

`SubmitEvent` for `onSubmit`.

### Pattern: Remove unnecessary async

Only use `async` when awaiting.

### Pattern: Handle promises in handlers

Use `await` or `void`.

### Pattern: Escape JSX text entities

Use `&apos;`, `&quot;`, etc.

### Pattern: Use deliberate fallbacks for optional strings

`q ?? ''` instead of `String(q)`.

### Pattern: ClientOnly boundary for hooks unsafe in SSR

Wrap Client Components that call hooks illegal during SSR (e.g. Better Auth's `useSession`) in a `ClientOnly` boundary that defers rendering to the client pass via `useSyncExternalStore`.

```tsx
<ClientOnly fallback={null}>
  <WishlistButton productSlug={product.slug} />
</ClientOnly>
```

Do NOT use `next/dynamic({ ssr: false })` in Server Components (forbidden by Next.js 16). Use `ClientOnly` everywhere for consistency.

### Pattern: Format every new file before committing

When creating a new file (not just editing an existing one), run Prettier on it before staging. The pre-commit hook checks **all** staged files, including newly created ones. A new file that was never formatted will fail the Prettier gate even if no editing tool touched its formatting.

```bash
pnpm --filter=@scope/pkg exec prettier --write src/components/new-file.tsx
```

This applies even when the file was written by a tool that produces "clean" output — Prettier's formatting rules (print width, trailing commas, semicolons, class sorting) may differ from the writer's defaults.

### Pattern: ScrollRevealTrigger — side-effect-only Client Component in a shared layout

When a hook needs to run as a side effect (e.g. `IntersectionObserver` setup) on every page under a layout, but renders no visible DOM, use a thin Client Component that:

1. Is marked `'use client'`.
2. Calls the hook in its body (no JSX return — renders `null`).
3. Is imported and rendered once in the shared layout.
4. Is wrapped in `<Suspense fallback={null}>` if the hook uses `useSearchParams()` or other APIs that break static prerendering.

```tsx
// ScrollRevealTrigger.tsx
'use client';
import { useScrollReveal } from '@/hooks/useScrollReveal';
export function ScrollRevealTrigger() {
  useScrollReveal();
  return null;
}

// (shop)/layout.tsx
<Suspense fallback={null}>
  <ScrollRevealTrigger />
</Suspense>
```

Why this pattern:
- Separates the hook's lifecycle from the page's render — the hook runs on mount, not per-page.
- Avoids re-running `IntersectionObserver` setup in every `ProductCard` (which would be per-card overhead and miss dynamically-loaded cards).
- The `<Suspense>` boundary satisfies Next.js 16's requirement for `useSearchParams()` in statically-prerendered pages.
- `fallback={null}` is correct because the trigger renders nothing visible.

---

## 5.9 Testing Patterns

### Pattern: Source contract tests for architectural invariants

When an architectural rule (e.g. "public pages must use `apiPublic`, auth pages must use `api`") is enforced by convention rather than by the type system, write a **source contract test** that reads the page source and asserts the import contract.

This is:
- **Deterministic** — no build invocation, no mocks, no network, no React rendering
- **Fast** — runs in <2s under Vitest
- **Hermetic** — fails immediately if an agent migrates a page to the wrong caller
- **Self-documenting** — the test file IS the specification of the architectural invariant

```ts
// apps/web/src/lib/__tests__/rendering-strategy.contract.test.ts
const PUBLIC_TRPC_PAGES = ['(shop)/page.tsx', '(shop)/products/page.tsx', /* ... */];
const read = (rel: string): string => readFileSync(join(APP_ROOT, rel), 'utf8');

for (const rel of PUBLIC_TRPC_PAGES) {
  it(`${rel} imports apiPublic (not api)`, () => {
    const src = read(rel);                          // string — null-free
    expect(src).toMatch(/import\s+\{\s*apiPublic\s*\}/);
    // Strip comment lines before checking — api() in JSDoc is benign
    const codeOnly = src.split('\n')
      .filter((l) => !l.trimStart().startsWith('//') && !l.trimStart().startsWith('*'))
      .join('\n');
    expect(codeOnly).not.toMatch(/\bapi\(\s*\)/);
  });
}
```

Why synchronous `readFileSync` instead of async `readFile().catch(() => null)`:

- Synchronous reads keep the producer type `string` — no null branch, no `TS18047` under `strict: true`.
- A missing file throws `ENOENT` at `readFileSync` (readable failure) instead of being swallowed to `null` (confusing regex-assertion failure).
- No async/await overhead in tests that need no I/O mocking.
- Mirrors the Stillwater reference (`index-routes-no-apiCaller.test.ts`) pattern.

Key design decisions:
- Use `node:fs` `readFile` (not React rendering) — no mock harness needed
- Strip comment lines before asserting `api()` absence — JSDoc mentions are benign
- The test file lives alongside the module it tests (`lib/__tests__/` for `lib/trpc/server.ts`)
- Use `// @vitest-environment node` per-file annotation if the test doesn't need DOM

When to use this pattern:
- The invariant is architectural (import contract), not behavioral (rendering output)
- The invariant can't be enforced by TypeScript (both `api()` and `apiPublic()` have compatible types)
- The invariant is high-stakes (a violation causes runtime `UNAUTHORIZED` or lost static rendering)

Lesson:

> When the type system can't enforce an architectural rule, a source contract test can. Read the source, assert the import, fail the build. This is faster and more reliable than build-output tests that parse the route table.

### Pattern: Meta-guard for caller modules

When a module exports split variants (e.g. `api()` and `apiPublic()`), add a test that asserts the module itself maintains its contract:

```ts
it('lib/trpc/server.ts maintains the api/apiPublic contract', () => {
  const src = readFileSync(join(HERE, '..', 'trpc', 'server.ts'), 'utf8');
  expect(src).toContain('export async function api()');
  expect(src).toContain('export async function apiPublic()');
  // api() must read headers()
  expect(src).toMatch(/import\s+\{\s*headers\s*\}/);
  // apiPublic() must NOT call headers() in its body
  const apiPublicBody = src.slice(
    src.indexOf('export async function apiPublic()'),
    src.indexOf('export async function apiPublic()') + 400,
  );
  expect(apiPublicBody).not.toMatch(/\bheaders\(\)/);
});
```

This catches the case where someone "simplifies" `apiPublic()` by reusing `api()` internally, or removes the `headers()` import from `api()`. The meta-guard is the last line of defense before the split-caller architecture collapses.

---

# 6. Anti-Pattern Catalog

This catalog names recurring mistakes so future agents can recognize them early.

## 6.1 Process Anti-Patterns

| Anti-Pattern | Description | Prevention |
|---|---|---|
| Trusting the brief blindly | Assuming prior diagnosis is current | Reproduce live |
| Scope creep | Fixing unrelated issues | Preserve surgical scope |
| Weakening guardrails | Disabling rules/hooks | Fix root cause |
| Premature success claim | Declaring done before verification | Rerun gates |
| Mixed logical changes | Multiple fixes in one diff | Separate commits |
| Assuming prior work committed | Repo state differs from docs | Check git status/log |
| Ignoring outstanding issues | Not recording deferred work | Handoff list |

---

## 6.2 Dependency Anti-Patterns

| Anti-Pattern | Description | Prevention |
|---|---|---|
| Invented version | Version does not exist | Registry check |
| Package conflation | Wrong package/version family | Verify exact name |
| Unused dependency | Declared but never imported | Delete |
| Undeclared import | pnpm strict isolation failure | Add to manifest |
| Deprecated caret | Range admits deprecated version | Exact pin |
| Missing config devDep | Tool config imports undeclared plugin | Add devDep |
| Empty suite surprise | Test exit nonzero due no tests | Configure or author tests |
| Blocked lifecycle scripts | Native deps fail silently after install | Approve builds in pnpm-workspace.yaml |

---

## 6.3 TypeScript Anti-Patterns

| Anti-Pattern | Description | Prevention |
|---|---|---|
| Inherited alias break | Shared `baseUrl` misresolves paths | Local `baseUrl` |
| Missing scaffolding | Imports point to absent modules | Create real modules |
| Promise member access | Accessing properties on unresolved promise | Await factory |
| Nullable leak | Raw join nullability reaches UI | Boundary coercion |
| Dead comparison | Narrowed type makes branch unreachable | Remove dead code |
| Explicit undefined | Violates strict optional properties | Conditional spread |
| Unguarded index | Index access may be undefined | Optional chaining |
| Brittle type derivation | Deep `Parameters` extraction | Canonical exported type |
| Incompatible union | Driver union breaks overloads | Canonical driver type |
| Hardcoded SDK literal | API version drift | Remove/update |
| Outdated SDK API | Method/payload changed | Inspect installed types |
| Hidden broken file | tsconfig include excludes it | Audit include |
| tRPC reserved word procedure | `apply`/`call`/`bind` etc. as procedure name — rejected at build time | Use domain-specific verb-noun pairs |
| Generic procedure names | `get`/`create`/`update`/`delete` — ambiguous in logs and error paths | Self-documenting names: `getProfile`, `createOrder` |

---

## 6.4 ESLint Anti-Patterns

| Anti-Pattern | Description | Prevention |
|---|---|---|
| FlatCompat with flat config | Legacy shim misloads ESM config | Direct import |
| Missing exports | ESM package resolution ambiguity | Add `exports` |
| Speculative overrides | Unused config blocks | Add only when needed |
| Autofix without format | Prettier drift | Run format after lint:fix |
| Rule disabling | Hides debt | Fix code |
| Hand-mapped fixes | Fragile mechanical edits | Use ESLint JSON |
| Incomplete batch verification | False completion | Rerun lint |

---

## 6.5 Prettier Anti-Patterns

| Anti-Pattern | Description | Prevention |
|---|---|---|
| Config/ignore confusion | Expecting `.prettierrc` to exclude paths | Use ignore file/flags |
| Ignored ignore file | `--ignore-path` overrides default | Add multiple ignore paths |
| Gitignore for formatting | Mixing tracking and formatting concerns | Use `.prettierrignore` |
| Wrong ignore pattern | `docs/` vs `docs` mismatch | Test real command |
| Blanket formatting | Huge diff churn | Scope or get approval |
| Staged unformatted files | Hook fails | Format before commit |
| Parse error as formatting | Syntax fault remains | Fix syntax first |
| New file never formatted | Prettier gate fails on newly created file | Run Prettier on every new file before staging |

---

## 6.6 Migration Anti-Patterns

| Anti-Pattern | Description | Prevention |
|---|---|---|
| Orphan migration | SQL file not in journal | Register migration |
| Missing snapshots | Generate creates full dump | Commit snapshots or avoid generate |
| Generate in setup | Non-deterministic provisioning | Remove from setup |
| Non-idempotent SQL | Type/table conflicts | Use guards or avoid regeneration |
| Silent failure | CLI hides DB error | Check DB logs |
| Env after client | Missing env at init | Import env first |
| Exit-code-only proof | State may be wrong | Query DB objects |

---

## 6.7 SDK Anti-Patterns

| Anti-Pattern | Description | Prevention |
|---|---|---|
| Invented subpath | `/v4` does not exist | Inspect exports |
| Missing dependency | Import without declaration | Add package |
| Old method names | SDK API changed | Inspect types |
| Wrong payload shape | Callback fields changed | Verify SDK contract |
| Hardcoded version | Type literal mismatch | Remove/update |
| Explicit undefined | Strict optional failure | Conditional spread |
| Hidden latent import | File excluded from type-check | Audit tsconfig include |
| Routing public data through session-aware caller | `api()` calls `next/headers` → public route forced dynamic → empty prerender | Use `apiPublic()` for `publicProcedure`-only pages |
| DYNAMIC_SERVER_USAGE misdiagnosed as cosmetic | Prior handoff says "expected, out of scope" when public route is empty | Verify against build log route table; check if route actually needs `headers()` |

---

## 6.8 React Anti-Patterns

| Anti-Pattern | Description | Prevention |
|---|---|---|
| Deprecated event type | `FormEvent` in React 19 | Use `SubmitEvent` |
| Async without await | `require-await` | Remove async |
| Floating promise | Unhandled promise in handler | Await or void |
| Raw number template | Restricted template expression | `String(...)` |
| `String(undefined)` | Bad metadata fallback | `?? ''` |
| Unescaped JSX text | Lint error | Use entities |
| Console.log | Logging hygiene | Use warn/error/logger |
| Better Auth React hooks during SSR | `useSession`/`authClient.useX()` calls `useRef` in SSR chunk → `null.useRef()` | Wrap in `ClientOnly` boundary |
| `next/dynamic({ ssr: false })` in Server Component | Next.js 16 forbids — build fails | Use `ClientOnly` wrapper instead |
| Public route forced dynamic by server caller | `api()` calls `headers()` → public page loses static rendering → empty prerender | Use `apiPublic()` for session-free public data |
| Grid placement on `<Image fill>` | `position: absolute` (from `fill`) removes Image from grid flow; `gridColumn`/`gridRow` silently ignored | Wrap in `<div position:relative>` that carries grid placement |
| Raw `JSON.stringify` in `dangerouslySetInnerHTML` for JSON-LD | XSS vector if data contains `</script>` | Escape with `escapeForScriptContext()` (5-char canonical set: `<>&` + U+2028 + U+2029) |
| Hook defined but never called | Hook file exists, compiles, exports — but no component imports or invokes it; feature silently does nothing | Verify hook is imported AND invoked in a component tree |

---

## 6.9 Tooling Anti-Patterns

| Anti-Pattern | Description | Prevention |
|---|---|---|
| Trusting reported line | Parser points after fault | Check neighbors |
| Pipe exit-code mask | `$?` reports last pipe command | Use `PIPESTATUS`/`pipefail` |
| ANSI-hidden error | Spinner overwrites error | Inspect logs |
| Fragile quote edits | Edit tool JSON escaping fails | Use scripts carefully |
| Hand-mapped replacements | Mismatch/corruption | Use machine-readable source |
| No validation mutation | Script edits wrong char | Validate before replace |
| Incomplete verification | Applied but not proven | Rerun gate |

---

# 7. Symptom-Based Troubleshooting Playbooks

These playbooks are designed for rapid use during incidents.

---

## Playbook 1: `ERR_PNPM_NO_MATCHING_VERSION`

### Symptoms

- Install fails.
- A package version cannot be found.

### Likely Causes

- Version does not exist.
- Package name is wrong.
- Version line conflated with another package.
- Private registry issue.

### Steps

1. Read exact package and version.
2. Check registry:

   ```bash
   npm view <pkg> versions --json
   ```

3. Check whether dependency is used.
4. If unused, delete it.
5. If used, choose a real version.
6. Check sibling dependencies for consistency.
7. Reinstall.
8. Re-run type-check and tests.

### Prevention

- Never add versions from memory.
- Audit unused dependencies.
- Validate package names exactly.

---

## Playbook 2: `Cannot find module`

### Symptoms

- TypeScript or runtime cannot resolve a module.

### Likely Causes

- Missing dependency.
- Missing workspace dependency.
- Broken path alias.
- Missing scaffolding file.
- tsconfig include/exclude issue.

### Steps

1. Check whether the module is a package or local path.
2. If package:
   - check `package.json`,
   - run `pnpm why`,
   - add dependency to consuming workspace.
3. If local path:
   - verify file exists,
   - verify extension resolution,
   - verify alias.
4. For aliases:

   ```bash
   tsc --traceResolution
   ```

5. Check local `baseUrl`.
6. Check whether file is excluded.
7. If scaffolding missing, create module from real consumer contracts.

### Prevention

- Declare every import.
- Define local `baseUrl` where paths are owned.
- Scaffold missing modules deliberately.

---

## Playbook 3: Many `TS2339` property-does-not-exist errors

### Symptoms

- Property access fails on a type.
- Often type is `Promise<...>` or a union.

### Likely Causes

- Accessing members on a promise.
- Incompatible union type.
- Wrong SDK type.
- Stale annotations.

### Steps

1. Inspect the type being accessed.
2. If it is a promise, await it first.
3. If it is a union, identify incompatible members.
4. Look for one root exported type causing many errors.
5. Canonicalize the type if appropriate.
6. Update stale local annotations.
7. Rerun type-check.

### Prevention

- Await factories before use.
- Export canonical types.
- Avoid leaking unions into consumers.

---

## Playbook 4: ESLint config failure with `__esModule`

### Symptoms

```text
Unexpected top-level property "__esModule"
```

### Likely Causes

- Flat config consumed through legacy loader.
- ESM interop marker leaking.
- Missing package exports.

### Steps

1. Inspect shared ESLint package.
2. Confirm it exports flat config.
3. Add proper `exports`.
4. Remove `FlatCompat`.
5. Import shared config directly.
6. Export flat array.
7. Rerun ESLint.

### Prevention

- Use flat config directly.
- Use proper ESM exports.
- Do not mix legacy and modern ESLint systems.

---

## Playbook 5: ESLint runs but many violations remain

### Symptoms

- ESLint executes.
- Reports many source-code problems.

### Likely Causes

- Genuine lint debt.
- Previously masked by config failure.

### Steps

1. Generate JSON output.
2. Group by rule.
3. Separate mechanical from semantic.
4. Fix mechanical rules first:
   - unescaped entities,
   - template expressions,
   - unused vars.
5. Fix semantic rules second:
   - deprecated types,
   - floating promises,
   - require-await.
6. Fix warnings:
   - non-null assertions,
   - console.
7. Rerun lint and Prettier.

### Prevention

- Run lint regularly.
- Do not disable rules to hide debt.

---

## Playbook 6: Prettier `[warn]` failures

### Symptoms

- Prettier reports dirty files.
- Hook fails.

### Likely Causes

- Files not formatted.
- ESLint autofix drift.
- New Prettier config.
- Staged files not formatted.

### Steps

1. Identify exact files.
2. Run:

   ```bash
   npx prettier --write <files>
   ```

3. Rerun:

   ```bash
   pnpm format:check
   ```

4. Check git diff for semantic changes.
5. Rerun type-check.
6. Re-stage if needed.

### Prevention

- Run Prettier after ESLint autofix.
- Format before staging.

---

## Playbook 7: Prettier `[error]` syntax failure

### Symptoms

- Prettier exits with parse error.
- Error line may be misleading.

### Likely Causes

- Missing parenthesis, brace, or bracket.
- Unterminated expression.
- Invalid syntax near reported line.

### Steps

1. Treat as syntax error, not formatting drift.
2. Inspect reported line and previous line.
3. Count delimiters.
4. Compare with sibling lines.
5. Inspect raw bytes for hidden characters:

   ```bash
   cat -A <file>      # $ = line end, ^I = tab, ^M = stray CR
   ```

6. Use TypeScript parser diagnostics if available.
7. Apply minimal syntax fix.
7. Run Prettier `--write`.
8. Run tests if file is test code.

### Prevention

- Do not trust reported line blindly.
- Use delimiter analysis.

---

## Playbook 8: Prettier ignore not working

### Symptoms

- Excluded directory still formatted.
- `.prettierrignore` appears correct.

### Likely Causes

- `--ignore-path` overrides default ignore discovery.
- Pattern syntax mismatch.
- Ignore file not passed to CLI.

### Steps

1. Inspect exact Prettier command.
2. Check whether `--ignore-path` is used.
3. Add:

   ```bash
   --ignore-path .gitignore --ignore-path .prettierrignore
   ```

4. Test pattern:
   - `docs`
   - `docs/`
5. Use probe files.
6. Verify root enforcement still works.

### Prevention

- Treat config and ignore as separate.
- Test ignore behavior with probes.

---

## Playbook 9: Pre-commit hook fails

### Symptoms

- Commit blocked.
- Hook stops at one gate.

### Likely Causes

- Format failure.
- Type failure.
- Lint failure.
- Staged files dirty.

### Steps

1. Identify failing gate.
2. Run gate command directly.
3. Fix that gate surgically.
4. Simulate full hook.
5. Check next gate.
6. Inspect staged vs unstaged.
7. Do not weaken hook.

### Prevention

- Run hook script before committing.
- Keep staged files formatted.

---

## Playbook 10: Drizzle migration fails silently

### Symptoms

- Migration exits nonzero.
- Little or no useful CLI output.

### Likely Causes

- SQL conflict.
- Journal drift.
- Missing snapshots.
- Database already has objects.
- Environment issue.

### Steps

1. Check database connectivity.
2. Inspect migration files and journal.
3. Look for orphaned migrations.
4. Check whether generate produced full dump.
5. Inspect Postgres logs.
6. Run the raw migration SQL directly to bypass the spinner mask:

   ```bash
   psql "$DATABASE_URL" -f drizzle/<migration>.sql
   ```

   This exposes the underlying Postgres error (e.g. `type "discount_type" already exists`) that the Drizzle spinner overwrote.

7. Run migrate in isolation.
8. Verify database state before and after.
9. Fix journal or remove bad generated migration.
10. Remove generate from setup if unsafe.

### Prevention

- Keep journal consistent.
- Commit snapshots if using generate.
- Make setup deterministic.

---

## Playbook 11: Seed script fails with missing env

### Symptoms

```text
DATABASE_URL is not set
```

### Likely Causes

- Env loader not imported.
- Client initialized before env load.
- Wrong env file.

### Steps

1. Inspect seed entrypoint.
2. Ensure env import is first.
3. Verify `.env.local` or `.env` exists.
4. Verify variable names.
5. Rerun seed.

### Prevention

- Load environment before any client initialization.

---

## Playbook 12: SDK subpath import fails

### Symptoms

```text
Cannot find module '@scope/sdk/v4'
```

### Likely Causes

- Subpath does not exist.
- Package version mismatch.
- Missing dependency.

### Steps

1. Inspect installed package exports.
2. Check registry version.
3. Verify dependency declaration.
4. Use real entrypoint.
5. Inspect SDK types for correct API.
6. Update method names and payloads.
7. Rerun type-check and tests.

### Prevention

- Do not invent subpaths.
- Inspect exports and types.

---

## Playbook 13: Test runner fails but no clear test failure

### Symptoms

- Test command exits nonzero.
- No assertion failure visible.

### Likely Causes

- No test files.
- Config dependency missing.
- Parse error in test file.

### Steps

1. Check whether test files exist.
2. Check config imports are declared.
3. Check for syntax errors.
4. Run single test file.
5. If empty suite, configure or author tests.

### Prevention

- Treat test config as real code.
- Document empty-suite policy.

---

## Playbook 14: tRPC build failure — `Reserved words used in router({})` call

### Symptoms

- `pnpm build` fails.
- Error message:
  
  ```text
  Error: Reserved words used in `router({})` call: <word>
  ```
  
  or:
  
  ```text
  Error: Failed to collect page data for /api/trpc/[trpc]
  ```

### Likely Causes

- A tRPC procedure was named with a JavaScript reserved word (`apply`, `call`, `bind`, `constructor`, `toString`, `valueOf`, `hasOwnProperty`, `__proto__`, etc.).
- tRPC v11 validates all procedure names at router construction time.
- The tRPC adapter route (`/api/trpc/[trpc]/route.ts`) imports `appRouter`, which triggers the constructor during `next build` static page collection.

### Why It Only Fails at Build Time

- `pnpm check-types` does not catch this because the router constructor runs at **module load time** (runtime), not during static type analysis.
- `pnpm build` triggers Next.js page data collection, which imports the tRPC adapter route, which imports the root router, which runs the constructor and validates procedure names.
- `pnpm dev` may or may not surface it depending on whether the route is eagerly loaded.

### Steps

1. Read the full error message — it names the offending word.
2. Search the API package for the reserved word:
   
   ```bash
   grep -rn "<word>" packages/api/src/routers/ --include="*.ts"
   ```
   
3. Identify the procedure definition.
4. Rename to a domain-specific verb-noun pair:
   
   ```diff
   - apply: protectedProcedure
   + submitApplication: protectedProcedure
   ```
   
5. Update all callers:
   
   ```bash
   grep -rn "trade\.apply" apps/web/src --include="*.ts" --include="*.tsx"
   ```
   
6. Update the caller:
   
   ```diff
   - trpc.trade.apply.useMutation()
   + trpc.trade.submitApplication.useMutation()
   ```
   
7. Update any related JSDoc comments.
8. Run the verification gates:
   
   ```bash
   pnpm check-types   # Gate 1
   pnpm lint          # Gate 2
   pnpm build         # Gate 5 — the original failure
   ```
   
9. Confirm the build succeeds.

### Prevention

- Name tRPC procedures with domain-specific verb-noun pairs.
- Avoid any name that collides with `Object.prototype`, `Function.prototype`, or `Array.prototype` methods.
- The reserved words list includes: `apply`, `call`, `bind`, `constructor`, `toString`, `valueOf`, `hasOwnProperty`, `isPrototypeOf`, `propertyIsEnumerable`, `toLocaleString`, `__proto__`.
- Add a lint rule or pre-commit check that scans procedure definitions for reserved words.

### Pattern

```text
good: submitApplication, createOrder, getProfile, listProducts, updateAddress, deleteItem
bad:  apply, call, bind, constructor, toString, valueOf, get, create, update, delete
```

### Adjacent Considerations

- The "Dynamic server usage" warnings in the build output are expected for routes using `headers()` — they indicate correctly dynamic routes, not errors.
- The `api/trpc/[trpc]` route must be dynamic (`ƒ`) because it handles authenticated requests.

---

## Playbook 15: Runtime `TypeError: Cannot read properties of null (reading 'useRef')` in SSR

### Symptoms

- `pnpm build` succeeds (37/37 pages).
- `pnpm start` + HTTP request produces:

```text
TypeError: Cannot read properties of null (reading 'useRef')
    at <unknown> (.next/server/chunks/ssr/[root-of-the-server]__<hash>._.js:1:<col>)
```
- The page returns HTTP 500 instead of 200.
- `check-types` and `lint` pass.
- No compile-time error — only a runtime crash during SSR of a Client Component.

### Likely Causes

- A Client Component calls a hook from `better-auth/react` (`useSession`, `authClient.useX()`) during the SSR pass.
- `better-auth/react`'s `useSession()` internally calls `useStore()` (from nanostores), which calls `useRef()`.
- Turbopack bundles `better-auth/react` into the SSR server chunk, where it selects React's `"react-server"` export condition (`./react.react-server.js`).
- The `react-server` build of React has null stubs for all hooks (`useRef`, `useState`, `useSyncExternalStore`) — by design, since React Server Components cannot call hooks.
- `null.useRef()` → `TypeError`.

### Diagnostic Steps

1. Identify the crashing chunk:

```bash
rg -l 'better-auth' .next/server/chunks/ssr/ | head
```

2. Open the chunk referenced in the stack trace and look for `useSession` or `useStore` or `useRef`.

3. Search the web app for which components call `useSession`:

```bash
rg -rn 'useSession|authClient\.use' apps/web/src --glob '!*.test.*'
```

4. Check whether those components render during SSR (are they imported by a Server Component page or layout, or by another Client Component that renders during SSR).

5. Confirm the crash by starting the server and curling the affected page:

```bash
cd apps/web && pnpm start &
curl -s -o /dev/null -w '%{http_code}' http://localhost:3000/
# Expect: 500 (crash)
```

### Fix

Wrap every component that calls a Better Auth React hook in a `ClientOnly` boundary at the call site.

```tsx
// At the call site (Server Component or Client Component):
import { ClientOnly } from '@/components/shop/ClientOnly';
import { WishlistButton } from '@/components/shop/WishlistButton';

<ClientOnly fallback={null}>
  <WishlistButton productSlug={product.slug} productName={product.name} />
</ClientOnly>
```

`ClientOnly` uses `useSyncExternalStore` with `getServerSnapshot: () => false` — an SSR-safe primitive that defers children to the client pass.

Do NOT use `next/dynamic({ ssr: false })` inside a Server Component — Next.js 16 forbids it and the build will fail with:

```text
`ssr: false` is not allowed with `next/dynamic` in Server Components.
```

### Verification

```bash
pnpm check-types   # Gate 1
pnpm lint          # Gate 2
pnpm build         # Gate 5
```

Then start the server and curl:

```bash
cd apps/web && pnpm start &
curl -s -o /dev/null -w '%{http_code}' http://localhost:3000/                # Expect: 200
curl -s -o /dev/null -w '%{http_code}' http://localhost:3000/products/some-slug  # Expect: 200
```

Confirm no `useRef` error in the server log.

### Prevention

- Any Client Component that calls Better Auth React hooks must be wrapped in `ClientOnly` at the call site.
- Do NOT use `next/dynamic({ ssr: false })` in Server Components — use `ClientOnly` everywhere for consistency.
- When adding new auth-gated UI, check whether `useSession` will be called during SSR before importing the component.

---

## Playbook 16: DYNAMIC_SERVER_USAGE warnings during build

This playbook covers `DYNAMIC_SERVER_USAGE` warnings that appear when `next build` runs a static pre-render probe on each route. The probe tries to render every page statically; if the page calls a dynamic API (`headers()`, `cookies()`, `searchParams`), the probe throws `DYNAMIC_SERVER_USAGE`. **Whether this is a bug or expected depends on the route type.** This playbook covers both scenarios.

### Symptoms

- `pnpm build` succeeds but emits warnings:

```text
[route-name] Failed to fetch data: Error: Dynamic server usage: Route /path couldn't be rendered statically because it used `headers`.
```

- The affected route renders as `ƒ` (Dynamic) instead of `○` (Static) in the build route table.
- Prior handoff documents may dismiss these as "cosmetic" or "expected" — verify against the actual build log.
- During the static-generation probe, the page's `try/catch` may swallow the error and render an **empty shell** (e.g. empty product grid on homepage).

### Likely Causes

- The page imports the session-aware server caller (`api()`), which unconditionally calls `next/headers`.
- In Next.js 16, `headers()`, `cookies()`, and `searchParams` access force a route dynamic.
- The page only calls `publicProcedure`s — it does not need a session — but the caller's `headers()` call forces dynamic anyway.

### Why This Is NOT Cosmetic

- **Empty prerender**: The static probe tries to render the page, hits `DYNAMIC_SERVER_USAGE`, the `try/catch` swallows it, and the page renders with empty data. For e-commerce, this means an empty product grid — a visible brand defect.
- **Lost static benefits**: The route loses ISR, PPR, edge caching, and CDN serving. Every request hits the server.
- **Performance regression**: The homepage (highest-traffic route) becomes server-rendered on every request instead of being served from edge.

### Diagnostic Steps

1. Check the route table in `pnpm build` output — is the route `○` or `ƒ`?
2. Search the build log for the route name:

```bash
grep "\[route-name]\" /tmp/build.log
grep "DYNAMIC_SERVER_USAGE" /tmp/build.log | grep "Route /path"
```

3. Check whether the page imports `api()` (session-aware caller):

```bash
grep -n "from '@/lib/trpc/server'" apps/web/src/app/(shop)/path/page.tsx
```

4. Check whether the page only calls `publicProcedure`s — if so, it should use `apiPublic()` instead.
5. Check whether the page reads `searchParams` — if so, `ƒ` is correct for that route (search/filter pages need URL state).

### Fix

Switch the page from `api()` to `apiPublic()`:

```diff
- import { api } from '@/lib/trpc/server';
+ import { apiPublic } from '@/lib/trpc/server';
 
- const caller = await api();
+ const caller = await apiPublic();
```

### Verification

```bash
pnpm check-types          # Gate 1
pnpm lint                 # Gate 2
pnpm build                # Gate 5 — verify route table
```

Check the route table:

```bash
grep "○ /path" /tmp/build.log   # Should show static marker
grep "\[route-name]\" /tmp/build.log   # Should show no warning
grep "DYNAMIC_SERVER_USAGE" /tmp/build.log | grep "Route /path"  # Should be absent
```

### Prevention

- Use `apiPublic()` for all public, cacheable pages (homepage, collections, product listings, search).
- Use `api()` only for pages that genuinely need a session (account, admin, cart, checkout).
- Do not import the session-aware caller in pages that only browse public content.
- Document the caller choice in the page's JSDoc comment.

### Pattern Source

Stillwater ADR V16-1: "No apiCaller() → no headers() → no streaming → complete HTML returned." Stillwater's `index-routes-no-apiCaller.test.ts` regression tests assert that public marketing pages do NOT call `apiCaller()`.

---

### Scenario B: Auth-guarded routes — warnings are expected and correct

The same `DYNAMIC_SERVER_USAGE` warnings on `/account/*` and `/admin/*` routes are **NOT a bug**. They are the correct and intended behavior.

#### Why these routes are dynamic by design

1. The `(account)/layout.tsx` and `(admin)/layout.tsx` call `auth.api.getSession({ headers: await headers() })` — the Layer 2 security boundary (per `PROJECT-ARCHITECTURE.md §6.3`). This is the *real* auth check; `proxy.ts` is only the cookie-existence optimistic gate.
2. Each page under those groups calls `api()` (the headers-bound tRPC caller) to run `protectedProcedure` or `adminProcedure` — which require a session.
3. `next/headers` is a dynamic API. When the static probe hits it, Next.js catches the `DYNAMIC_SERVER_USAGE` throw, opts the route into dynamic rendering, and the build completes.

This is identical to the Stillwater pattern: Stillwater's `(admin)/layout.tsx` → `requireRole()` → `getSession()` → `headers()` — the same architecture.

#### The `force-dynamic` trap

The obvious "fix" to silence these warnings is `export const dynamic = 'force-dynamic'` on each page. **Do NOT do this.**

- `force-dynamic` is **incompatible with `cacheComponents: true`** — a documented Next.js 16 *build error*, not a warning (Stillwater SKILL §6.10 Gotcha 7).
- Maison does not enable `cacheComponents` today, but `next.config.ts` is structured to adopt it in a later phase.
- Adding `force-dynamic` now creates a **time bomb**: the build breaks the day `cacheComponents` is turned on.
- Stillwater's own remediation saga (C3 / V16-1) removed `force-dynamic` from routes for exactly this reason.

The correct approach is to **let the dynamic API force the route dynamic naturally** — which Next.js does automatically. The warnings are informational, not actionable.

#### When to add the guardrail note

Document this in `AGENTS.md` under "Things that look wrong but aren't" so future agents don't re-chase the warnings:

```markdown
- **`DYNAMIC_SERVER_USAGE` warnings for `/account/*` + `/admin/*`** — These routes are `ƒ (Dynamic)` by design: the layouts call `auth.api.getSession({ headers: await headers() })`, which makes `next/headers` hit the static pre-render probe. Next.js catches the probe, marks the route dynamic, and emits a warning. The build completes. Do NOT add `export const dynamic = 'force-dynamic'` to silence them — that is incompatible with `cacheComponents: true`.
```

#### Regression test: source contract tests

The architectural invariant (public routes use `apiPublic`, auth routes use `api`) can be locked with a source contract test that reads page source and asserts the import contract. This is:
- **Deterministic** — no build invocation, no mocks, no network
- **Fast** — runs in <2s under Vitest
- **Hermetic** — fails if an agent migrates a public route to `api()` (forcing it dynamic) or an auth route to `apiPublic()` (nulling the session)

See `apps/web/src/lib/__tests__/rendering-strategy.contract.test.ts` for the implementation. The test covers:
1. Public TRPC pages import `apiPublic` (not `api`)
2. Auth layouts call `auth.api.getSession({ headers })`
3. Auth leaf pages import `api` (not `apiPublic`)
4. Meta-guard: `lib/trpc/server.ts` maintains the `api`/`apiPublic` contract

#### Client Components are exempt from the server-caller contract

Some auth-guarded leaf pages (`account/addresses`, `account/loyalty`, `account/settings`, `admin/products/new`) are pure `'use client'` and use the **client-side** tRPC caller (`trpc` from `@/lib/trpc/client`), not the server-side `api()`. They don't import `api()` at all — and that's correct. They are still forced dynamic by the layout's `headers()` call, but they don't need to be in the source contract test's `AUTH_LEAF_PAGES` array because the server-import contract doesn't apply to them.

Lesson:

> The `api()`/`apiPublic()` split is a **Server Component concern**. Client Components use the client-side `trpc` caller with React Query — they never call `api()` or `apiPublic()`. When auditing rendering strategy, check whether the page is a Server Component or Client Component before asserting the caller contract.

---

## Playbook 17: check-types fails with TS18047 on a value "already null-checked" by a Vitest assertion

### Symptoms

```text
src/lib/__tests__/some.contract.test.ts:111:26 - error TS18047: 'src' is possibly 'null'.
  111         const codeOnly = src
                                ~~~
```

...appearing immediately after:

```ts
expect(src, 'file not found').not.toBeNull();
```

Pre-commit hook fails at the `check-types` gate. The build itself may succeed — the error is in the test file, not the application.

### Likely Causes

1. The test's file reader returns `string | null` via `readFile(...).catch(() => null)`.
2. `expect(x).not.toBeNull()` is a **runtime assertion**, not a TypeScript type guard — it does not narrow `x`'s compile-time type.
3. `tsc` keeps `x: string | null`, so `.split()`, `.match()`, or `.indexOf()` derefs a maybe-null value → `TS18047`.

### Diagnostic Steps

```bash
# 1. Confirm the failing file:
find apps/web/src -name '*.test.ts' | xargs grep 'catch.*null'

# 2. Confirm the type error:
find apps/web/src -name '*.test.ts' | xargs grep 'expect.*not.toBeNull.*\.' | head
# (look for expect(...).not.toBeNull() followed by .method() on the same value)
```

### Fix

Two options, in order of preference:

**Option A (preferred): make the producer non-null.** Switch from async `readFile(...).catch(() => null)` to synchronous `readFileSync` → `string` (mirrors the Stillwater reference pattern in `index-routes-no-apiCaller.test.ts`):

```ts
- const read = (rel: string) =>
-   readFile(join(APP_ROOT, rel), 'utf8').catch(() => null);
+ const read = (rel: string): string =>
+   readFileSync(join(APP_ROOT, rel), 'utf8');
```

This eliminates the null branch at the type level, improves the missing-file failure mode (loud ENOENT instead of confusing regex failure), and removes async/await from tests that don't need it.

**Option B (if you must keep a nullable producer): use a real type guard at the deref site.**

```ts
if (src === null) throw new Error(`${rel} not found`);  // narrows to string
codeOnly = src.split('\n');
```

### Verification

```bash
pnpm --filter=@maison/web exec tsc --noEmit  # no TS18047
pnpm --filter=@maison/web test                # all contract tests pass
pnpm format:check                             # file is Prettier-conformant
```

### Prevention

- **Never use `readFile(...).catch(() => null)` in contract tests.** Synchronous `readFileSync` → `string` is the canonical form.
- **Never rely on `expect(x).not.toBeNull()` to narrow a type.** Use it for the runtime assertion, but also ensure the *type* is non-null via the producer.
- **Before committing a new test file:** run `pnpm check-types` and `prettier --check` on it. Don't rely on the pre-commit hook catching everything — some gates run only on staged content.

---

# 8. Verification Matrices

Verification is not optional. A fix is only real if proven.

---

## 8.1 General Verification Matrix

| Change Type | Minimum Verification |
|---|---|
| Dependency change | install, check-types, tests |
| TypeScript fix | check-types, format, lint |
| ESLint config fix | lint runs, lint:fix, format, check-types |
| ESLint source fix | lint, format, check-types |
| Prettier fix | format:check, check-types |
| Hook fix | direct gate command, full hook simulation |
| Migration fix | migrate, seed, DB state queries, full setup |
| SDK fix | check-types, package tests, consumer regression |
| Test fix | single test, package tests |
| Runtime fix | dev/build/manual flow |
| tRPC router change | check-types, lint, **build** (router constructor runs at build, not type-check) |
| tRPC procedure rename | check-types, lint, build, grep callers for stale references |
| Server caller change (api → apiPublic) | check-types, lint, **build** (verify route table: migrated routes should show `○` not `ƒ`), grep for remaining DYNAMIC_SERVER_USAGE on migrated routes |

---

## 8.2 Monorepo Verification Matrix

| Gate | Command | Expected |
|---|---|---|
| Install | `pnpm install` | exit 0 |
| Format | `pnpm format:check` | exit 0 |
| Type-check | `pnpm check-types` | all tasks pass |
| Lint | `pnpm lint` | exit 0 ideally |
| Tests | `pnpm test` | pass or documented empty-suite policy |
| Build | `pnpm build` | exit 0 |
| Hook | `bash scripts/pre-commit-check.sh` | passes or known next blocker |

---

## 8.3 Database Verification Matrix

| Check | Command/Query | Expected |
|---|---|---|
| Postgres ready | `pg_isready` | accepting connections |
| Migrations applied | `select * from drizzle.__drizzle_migrations` | expected records |
| Tables exist | `information_schema.tables` | expected count |
| Enums exist | `pg_enum` | expected enums |
| Seed rows | table counts | expected seed data |
| Full setup | `pnpm db:setup` | exit 0 |

---

# 9. Handoff and Documentation Standards

Every session should end with a clean handoff.

## 9.1 Required Handoff Information

The report should include:

1. Objective.
2. Current blocker.
3. Root cause.
4. Fix applied.
5. Why the fix was correct.
6. Verification results.
7. Files changed.
8. Outstanding issues.
9. Recommended next steps.
10. Commit grouping advice.

---

## 9.2 Handoff Template

```text
## Objective
What was being fixed.

## Context
Prior state and relevant history.

## Root Cause
The true underlying issue.

## Fix Applied
Concrete changes.

## Why Correct
Evidence and reasoning.

## Verification
Commands run and results.

## Files Changed
List of files and purpose of changes.

## Outstanding Issues
Remaining failures, deferred work, runtime verification needed.

## Recommended Next Steps
Ordered follow-up actions.

## Commit Advice
Suggested logical commit grouping.
```

---

## 9.3 Rules for Handoff

- Do not claim a gate is green unless verified.
- Do not hide latent defects.
- Do not assume commits will be made by someone else without guidance.
- Do not omit runtime verification needs.
- Do not mix “applied” with “verified.”

---

# 10. Condensed Case Index

This index summarizes the major incidents and their distilled lessons.

| ID | Incident | Root Cause | Fix | Key Lesson |
|---|---|---|---|---|
| DEP-1 | Nonexistent `@react-email/components` version | Version conflation | Delete unused dep | Validate versions; delete unused deps |
| DEP-2 | Nonexistent `sanity` version | Wrong version line | Pin real version | Check registry and sibling versions |
| DEP-3 | Sanity hotspot broken | Option on array not image member | Move hotspot to image member | Schema options belong on correct member |
| DEP-4 | Vitest plugin missing | Config import undeclared | Add devDep | Config files need declared deps |
| DEP-5 | jest-dom version drift | Caret admitted unexpected version | Exact pin | Pin sensitive deps deliberately |
| DEP-6 | pnpm version mismatch | Outdated packageManager | Bump to real version | Align package manager |
| DEP-7 | pnpm 10 blocked esbuild lifecycle scripts | pnpm 10 security default | `allowBuilds` config | Approve native builds in pnpm-workspace.yaml |
| DB-1 | Silent migrate failure | Journal drift + full-schema dump | Register migration, delete bad dump | Journal and snapshots matter |
| DB-2 | Setup regenerated bad migration | `db:generate` in setup | Remove generate from setup | Setup must be deterministic |
| DB-3 | Seed env missing | Env loader not imported | Import env first | Env before clients |
| PRETTIER-1 | `trpc.test.ts` syntax error | Missing parenthesis previous line | Add one `)` | Parser line may mislead |
| PRETTIER-2 | Prettier warnings fatal | Formatting drift | Format targeted files | Warnings can block hooks |
| PRETTIER-3 | `.prettierrignore` ignored | `--ignore-path` override | Add second ignore path | Config and ignore are separate |
| PRETTIER-4 | Docs exclusion pattern fail | `docs/` pattern mismatch | Use `docs` | Test ignore patterns |
| PRETTIER-5 | Repo-wide dirty after config | New formatting fixed point | Approved `pnpm format` | New config causes expected churn |
| SDK-1 | Trigger.dev `/v4` missing | Nonexistent subpath | Import main entry | Inspect exports |
| SDK-2 | Trigger.dev missing dep | pnpm strict isolation | Add dependency | Declare every import |
| SDK-3 | Trigger.dev wrong API | Outdated client usage | Use `tasks.trigger` | Inspect installed types |
| SDK-4 | Workers latent `/v4` | File outside tsconfig include | Deferred; audit include | Green check can hide latent errors |
| RUNTIME-1 | `useRef` crash on all SSR pages | Better Auth `useSession` calls `useRef` during SSR; Turbopack selects `react-server` build | Wrap in `ClientOnly` boundary | Auth hooks must not execute during SSR |
| TS-1 | Alias resolution broken | Inherited `baseUrl` | Local `baseUrl` | Trace module resolution |
| TS-2 | Missing lib scaffolding | Files absent | Scaffold from contracts | Adapt reference carefully |
| TS-3 | Async caller misuse | Property access on promise | Await caller | Await factories |
| TS-4 | Nullable join shapes | Drizzle left-join inference | Router boundary coercion | Shape data at boundaries |
| TS-5 | DrizzleDB union | Incompatible driver union | Canonical Neon type | Avoid unusable unions |
| TS-6 | Better Auth drift | API changed | Use new methods/payloads | Verify installed SDK |
| TS-7 | Stripe drift | Hardcoded version/types | Remove literal, local types | Avoid hardcoded SDK literals |
| TS-8 | Missing API deps | Undeclared imports | Add workspace deps | pnpm isolation requires declaration |
| TS-9 | TS18047 after runtime `not.toBeNull` | `readFile().catch(()=>null)` widened producer to `string \| null`; `expect().not.toBeNull()` is not a type guard | Null-free producer (`readFileSync` → `string`) or real type guard at deref site | Runtime assertions do not narrow TypeScript types |
| TS-10 | `z.string().email()` in Zod v4 | Zod v4 deprecated method; 43 sites across 12 files | Migrate to native `z.email()`, `z.uuid()`, `z.url()`, `z.iso.datetime()` | SDK method drift requires systematic migration |
| TS-11 | Residual non-null assertions in payment routers | `!` postfix on possibly-null values in checkout/gift-cards/cart/trade | Replace with explicit `if (!x) throw new TRPCError(...)` guards | Non-null assertions hide runtime null risk; use proper guards |
| ESLINT-1 | `__esModule` config error | FlatCompat with flat config | Direct flat import | Use modern ESLint correctly |
| ESLINT-2 | Lint autofix drift | Prettier not rerun | Format after lint:fix | Tool ordering matters |
| ESLINT-3 | 89 lint violations | Source-code debt | Batched remediation | Separate infra from debt |
| ESLINT-4 | Type-aware rule noise on Drizzle | `@typescript-eslint/no-unnecessary-condition`, `no-deprecated` false positives | Downgrade to `warn` in per-package overrides | Some type-aware rules are incompatible with Drizzle patterns |
| ESLINT-5 | `require-await` on async-no-await | Async functions without await in email/stripe webhooks | Remove `async` or add await | `async` without `await` is dead code |
| REACT-1 | Deprecated FormEvent | React 19 deprecation | Use SubmitEvent | Use handler-specific events |
| REACT-2 | Floating promises | Unhandled promises | Await or void | Handle promises explicitly |
| REACT-3 | OG require-await | Async without await | Remove async | Do not use needless async |
| REACT-4 | Template numbers | Restricted template rule | Use `String(...)` | Explicit conversion |
| REACT-5 | Optional metadata | `String(undefined)` risk | Use `?? ''` | Choose fallbacks deliberately |
| TOOL-1 | Edit tool quote failures | Embedded quotes | Use robust scripts | Use machine-readable inputs |
| TOOL-2 | Script corruption | Hand-mapped fixes | Git restore + ESLint JSON | Validate before mutating |
| TOOL-3 | Exit-code masking | Pipe status | Use `PIPESTATUS`/`pipefail` | Verify real exit codes |
| HOOK-1 | 7-file Prettier failure | Staged unformatted files | Format 7 files | Staged content must pass gates |
| HOOK-2 | Hook advances to lint | Format fixed, lint remains | Report next blocker | Simulate full hook |
| TRPC-1 | Build fails with reserved word | `apply` as tRPC procedure name | Rename to `submitApplication` | tRPC v11 rejects JS reserved words at constructor time; only caught at build, not type-check |
| TRPC-2 | Generic procedure names | `get`/`create`/`update`/`delete` — ambiguous | Self-documenting verb-noun pairs | Procedure paths visible in logs; generic names hinder debugging |
| RUNTIME-2 | Homepage empty prerender | `api()` called `next/headers` → `/` forced dynamic → static probe swallowed error → empty product grid | `apiPublic()` (session-free caller) | `next/headers` is the architectural chokepoint for static vs dynamic in Next.js 16 |
| RUNTIME-3 | DYNAMIC_SERVER_USAGE misdiagnosed as cosmetic | Prior handoff said "/ renders fine" when build log explicitly named `[home]` | Verify claims against actual error log | Prior diagnosis documents can be wrong — reproduce, don't trust the summary |
| RUNTIME-4 | New file not formatted before commit | Prior remediation created ClientOnly.tsx but never ran Prettier | Format every new file before staging | New files are checked by pre-commit hook just like edited files |
| RUNTIME-5 | apiPublic() migration of 5 public pages | Switched api() → apiPublic() on /, /collections, /products, /products/[slug], /search | `/` and `/collections` flipped from `ƒ` to `○`; warnings eliminated | Session-free caller reuses same appRouter — zero duplicated query logic |
| RUNTIME-6 | Prior "all gates green" claim contradicted by error log | Verification table in handoff asserted `check-types 10/10 ✓` and `test 20/20 ✓` for a file that error.txt proved was type-broken at commit time | Reproduce the failing gate directly against the committed code | Treat prior *green checkmarks* as hypotheses too — stale cache or never-run verification produces false positives |
| TS-9 | TS18047 after runtime `not.toBeNull` | `readFile().catch(()=>null)` widened producer to `string | null`; `expect().not.toBeNull()` is not a type guard | Null-free producer (`readFileSync` → `string`) or real type guard at deref site | Runtime assertions do not narrow TypeScript types |
| PRETTIER-6 | `.prettierrignore` masking a real `[warn]` | File genuinely mis-formatted; exclusion added to silence the gate instead of fixing the file | `prettier --write` then remove exclusion from `.prettierrignore` | Ignore files are for unowned content, not gate-silencing |
| TEST-1 | Contract test async null swallow | `readFile().catch(()=>null)` widens type + hides ENOENT into a confusing regex failure | Synchronous `readFileSync` → `string` (throws on missing, null-free) | Contract tests should throw on missing sources |
| RENDER-1 | `/products` blank screen — cards rendered but invisible | `useScrollReveal` hook defined but never called; `.reveal` CSS sets `opacity: 0` | Wire hook via `ScrollRevealTrigger` Client Component in shop layout | Verify hooks are called, not just defined |
| RENDER-2 | Initial product cards stay `opacity: 0` on page load | IntersectionObserver doesn't fire for already-visible elements when constructed in post-hydration `useEffect` | `requestAnimationFrame` fallback with `getBoundingClientRect()` check | IntersectionObserver timing issue with useEffect |
| RENDER-3 | Philosophy section images missing | `next/image fill` (`position: absolute`) with `gridColumn`/`gridRow` on `<Image>` — grid placement silently ignored | Wrap Image in `position: relative` div that IS the grid item | `fill` removes elements from grid flow |
| RENDER-4 | Collection filter pages blank on client-side navigation | `useEffect([])` in `useScrollReveal` never re-runs when URL changes via `<Link>` | Add `usePathname`/`useSearchParams` as `useEffect` dependencies | Client-side nav doesn't re-run empty-deps effects |
| RENDER-5 | Build fails: `useSearchParams() should be wrapped in a suspense boundary` | V14 added `useSearchParams()` to `useScrollReveal`; no Suspense boundary in shop layout | Wrap `<ScrollRevealTrigger />` in `<Suspense fallback={null}>` | `useSearchParams()` needs Suspense in statically-prerendered pages |
| SECURITY-1 | JSON-LD script tag XSS vector | `dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}` — if product data contains `</script>`, attacker-controlled script runs | Apply `escapeForScriptContext()` (5-char canonical set) before `dangerouslySetInnerHTML` | Always escape script context in inline JSON-LD |

---

# 11. Final Agent Checklist Before Declaring Success

Before ending a session, an agent should confirm:

## Diagnosis

- [ ] The original failure was reproduced.
- [ ] The true root cause was identified.
- [ ] The reported error location was validated.
- [ ] The failure class was correctly identified.

## Fix

- [ ] The fix was surgical.
- [ ] No guardrail was weakened.
- [ ] No unnecessary refactor was introduced.
- [ ] No speculative dependency was added.
- [ ] No unused dependency was left behind.
- [ ] No config was changed without reason.

## Verification

- [ ] The failing gate now passes.
- [ ] Adjacent gates were rerun.
- [ ] Exit codes were checked correctly.
- [ ] Machine-readable output was used where useful.
- [ ] Database state was verified if DB work occurred.
- [ ] Tests were run if code behavior changed.
- [ ] Prettier was run after ESLint autofix.

## Repository State

- [ ] Git status was reviewed.
- [ ] Staged and unstaged changes were identified.
- [ ] Generated artifacts were handled deliberately.
- [ ] Corrupted or accidental edits were restored.
- [ ] No commit was made unless approved.

## Handoff

- [ ] Outstanding issues are listed.
- [ ] Runtime verification needs are listed.
- [ ] Commit grouping advice is provided.
- [ ] Latent defects are documented.
- [ ] The next blocker is clearly named.

---

# 12. The Most Important Lessons, Ranked by Impact

If an agent remembers only a few things, they should be these:

## 1. Reproduce before trusting

Prior documentation is not truth. Live reproduction is truth.

## 2. Classify the gate

Do not fix lint when the problem is formatting. Do not fix code when the problem is infrastructure.

## 3. Use authoritative diagnostics

Registry metadata, package exports, TypeScript resolution traces, ESLint JSON, and database logs beat guesswork.

## 4. Fix root causes, not symptoms

One canonical type fix can replace dozens of consumer edits. One journal fix can replace destructive resets. One env import can fix seeding.

## 5. Preserve guardrails

Never make a gate green by weakening it.

## 6. Respect tool ordering

ESLint autofix can create Prettier drift. Formatting must come after lint fixes.

## 7. Treat staged content as final

If it is staged, it must pass the hook.

## 8. Verify state, not just exit codes

Especially for databases.

## 9. Keep changes surgical

Large diffs hide intent and create review risk.

## 10. Hand off cleanly

A fix is not complete until the next agent or human knows exactly what remains.

## 11. Build gate catches what type-check misses

Some errors (like tRPC reserved word procedure names) only surface at `pnpm build` time because the router constructor runs at module load, not during static type analysis. If `check-types` passes but `build` fails, inspect the actual runtime imports — the error is in module initialization, not in type definitions.

## 12. Runtime crashes can pass all static gates

`check-types` passes. `lint` passes. `build` succeeds. The page still returns HTTP 500 at runtime. The `react-server` export condition in React 19 causes Better Auth React hooks (`useSession`) to call null-stub hooks (`useRef`) during SSR — a runtime-only failure that no static gate catches. Always verify with `pnpm start` + `curl` against the live server, not just the build output.

## 13. Verify prior diagnoses against the actual error log

A prior remediation document (`last_remediation.md`, a handoff from a previous session) may contain confidently stated but incorrect conclusions. In the original session, the prior document claimed: "`DYNAMIC_SERVER_USAGE` warnings are non-fatal… build still completes 37/37. Expected and correct; out of scope per Surgical Changes." The build log explicitly showed `[home] Failed to fetch data: Route / couldn't be rendered statically because it used headers` — the homepage was forced dynamic and rendered an empty product grid during the static probe. The prior document was wrong about `/` being fine. This was later fixed (public routes migrated to `apiPublic()`). A later remediation compound this: its verification table claimed `check-types 10/10 ✓` and `test 20/20 ✓` for a test file that the next `check-types` run proved was type-broken (`TS18047`) at commit time — the verification was either run against stale cache or never actually executed. Lesson: always verify a prior diagnosis against the actual error log, not the summary. Treat every prior conclusion — *and every prior green checkmark* — as a hypothesis until reproduced. (See RUNTIME-3, RUNTIME-6.)

## 14. Distinguish public-route from auth-route DYNAMIC_SERVER_USAGE warnings

Not all `DYNAMIC_SERVER_USAGE` warnings are equal. The same warning message means different things depending on the route:

- **Public routes** (`/`, `/collections`, `/products`, `/search`) — the warning is a **real bug**. The page doesn't need a session, but `api()` calls `headers()` anyway. The route is forced dynamic, loses static rendering, and the static probe may render an empty shell (e.g. empty product grid). Fix: migrate to `apiPublic()`.
- **Auth-guarded routes** (`/account/*`, `/admin/*`) — the warning is **expected and correct**. The layout calls `auth.api.getSession({ headers: await headers() })` (the Layer 2 security boundary), which correctly forces the route dynamic. Fix: none. Do NOT add `export const dynamic = 'force-dynamic'` to silence them — that is incompatible with `cacheComponents: true`.

The diagnostic is simple: check the route table. If the route is `ƒ` and it's an auth-guarded route, that's by design. If it's `ƒ` and it's a public route, that's a bug.

Lesson:

> When you see `DYNAMIC_SERVER_USAGE`, ask: "Does this route actually need a session?" If yes, the warning is correct. If no, it's a real bug. Never blanket-fix all warnings without distinguishing the two cases.

## 15. Verify hooks are called, not just defined

A hook file exists, exports cleanly, and compiles without error — but no component imports or calls it. The feature silently does nothing. After defining a hook, verify it is imported AND invoked in a component tree (not just referenced in a CSS comment or type definition). This was the root cause of the `/products` blank-screen defect: `useScrollReveal` was defined but had zero consumers. The `.reveal` CSS set `opacity: 0`, the `.reveal.visible` CSS set `opacity: 1`, but the bridge between them (the hook that adds the `visible` class) was never executed.

## 16. IntersectionObserver may not fire for already-visible elements

When an `IntersectionObserver` is constructed inside a post-hydration `useEffect`, it may not fire the `isIntersecting` callback for elements already in the viewport on page load. The browser has already computed which elements are visible, and the observer's initial check does not trigger for them. Add a `requestAnimationFrame` fallback that checks `getBoundingClientRect()` and manually adds the visible class to elements whose bounding box overlaps the viewport. Do not remove this fallback as "redundant" — it covers a real first-paint timing gap that the observer cannot detect.

## 17. `next/image fill` renders `position: absolute` — grid placement must be on a wrapper div

`<Image fill>` renders the `<img>` with `position: absolute` so it stretches to fill its nearest positioned ancestor. An absolutely-positioned element is removed from CSS Grid flow — so `gridColumn` / `gridRow` set on the `<Image>` style have no effect. The image positions itself relative to a distant ancestor instead of its intended grid cell, producing broken or invisible images. Fix: wrap each `<Image fill>` in a `<div style={{ position: 'relative', gridColumn, gridRow, overflow: 'hidden' }}>` that IS the grid item.

## 18. `useSearchParams()` in a Client Component requires `<Suspense>` for static pages

In Next.js, a Client Component calling `useSearchParams()` during static prerendering causes either a hard build error (`useSearchParams() should be wrapped in a suspense boundary`) or a silent downgrade from `○ Static` to `ƒ Dynamic`. Wrap the consumer in `<Suspense fallback={null}>`. This applies to **every** `useSearchParams()` consumer — not just one instance. A layout-level Suspense boundary only protects the component it wraps; other consumers on individual pages need their own Suspense wrappers.

---

# 13. One-Page Agent Field Card

Use this during live troubleshooting.

```text
1. Reproduce the exact failure.
2. Identify the gate: install / type / lint / format / test / db / hook.
3. Separate infrastructure failure from source-code debt.
4. Use authoritative diagnostics.
5. Build a hypothesis table.
6. Apply the smallest correct fix.
7. Do not weaken guardrails.
8. Run the fixed gate.
9. Run adjacent gates.
10. If DB: verify objects, not just exit code.
11. If ESLint autofix: run Prettier after.
12. If Prettier ignore: test exact command.
13. If SDK: inspect exports and installed types.
14. If parser error: inspect previous line.
15. If script edit: validate before mutating.
16. If tRPC build fails: check procedure names for JS reserved words.
17. Check git status and staged state.
18. Record outstanding issues.
19. Do not claim success before verification.
20. If `useRef`/`useState` crash in SSR: Better Auth React hooks must not run during SSR — wrap in `ClientOnly` boundary, never use `next/dynamic ssr:false` in Server Components.
21. If public page shows empty prerender: check whether server caller calls `next/headers` — use `apiPublic()` for session-free public data.
22. If build warns `DYNAMIC_SERVER_USAGE` on a public route: this is a real bug (empty prerender + lost static benefits), not cosmetic.
23. Before trusting a prior remediation document: verify its claims against the actual error log.
24. If build warns `DYNAMIC_SERVER_USAGE` on an auth-guarded route (`/account/*`, `/admin/*`): this is expected and correct — the layout calls `headers()` for session verification. Do NOT add `force-dynamic` to silence it (incompatible with `cacheComponents: true`).
25. The `api()`/`apiPublic()` split is a Server Component concern. Client Components use `trpc` from `@/lib/trpc/client` — they never call `api()` or `apiPublic()`.
26. Source contract tests (read source, assert import) lock architectural invariants faster and more reliably than build-output tests.
```

---

# 14. Conclusion

The accumulated sessions reveal a consistent pattern:

- Many failures looked local but were systemic.
- Many reported errors were misleading.
- Many fixes required validating assumptions against live evidence.
- Many recurring problems were caused by tool ordering, missing declarations, state drift, or outdated SDK usage.
- The best fixes were surgical, evidence-based, and verified across adjacent gates.

This handbook should be used as a living guide:

- before making changes,
- during diagnosis,
- when choosing a fix strategy,
- and before declaring success.

The ultimate goal is not merely to fix the current project, but to make future agents **less likely to repeat the same class of mistakes** and **more likely to troubleshoot with discipline, precision, and clean handoffs**.


---

# 15. v12-v14 Remediation Arc Lessons (v1.6 Supplement)

**Date:** 2026-08-01
**Source:** Maison e-commerce monorepo remediation (commits `5eee3370` through `ee397b2e`)

This supplement documents 10 lessons from the v12-v14 remediation arc that are not covered in the main handbook (§1-§14). Each lesson follows the same structure: **Symptom → Root Cause → Fix → Contract Test**.

## 15.1 ENV-1: createEnv() proxy throws on client at module load

**Symptom:** Live site shows "This page couldn't load" — server returns HTTP 200 with correct HTML, but React fails to hydrate.

**Root cause:** `@t3-oss/env-core`'s `createEnv()` uses a proxy that throws when server-side env vars (like `BETTER_AUTH_URL`) are accessed on the client (`isServer=false`). If a module-load-time statement accesses `env.BETTER_AUTH_URL`, the entire client bundle crashes.

**Fix:** Guard all server-side env access with `typeof window === 'undefined'` (or `typeof globalThis.window === 'undefined'`).

```ts
// BAD — throws on client
export const env = loadEnv();
warnOnAuthUrlMismatch(env.BETTER_AUTH_URL, env.NEXT_PUBLIC_APP_URL);

// GOOD — server-only
export const env = loadEnv();
if (typeof globalThis !== 'undefined' && typeof (globalThis as { window?: unknown }).window === 'undefined') {
  warnOnAuthUrlMismatch(env.BETTER_AUTH_URL, env.NEXT_PUBLIC_APP_URL);
}
```

**Contract test:** `env-server-only.contract.test.ts` — asserts the guard exists and `env.BETTER_AUTH_URL` is not accessed unguarded.

## 15.2 DB-4: server-only guard on db client breaks tsx CLI scripts

**Symptom:** `pnpm db:seed` fails with `"This module cannot be imported from a Client Component module"`.

**Root cause:** `import 'server-only'` was added to `packages/db/src/index.ts`. The seed script (`tsx src/seed/index.ts`) imports `db` from `../index`. The `tsx` runtime doesn't set the `react-server` export condition, so the `server-only` package resolves to its `index.js` (which throws) instead of `empty.js` (which is a no-op).

**Fix:** The `server-only` guard belongs at the **API/server boundary consumer** (like `api/context.ts`, `api/trpc.ts`, `auth/config.ts`), NOT the low-level db utility layer. The db client is consumed by both server code AND CLI scripts.

**Contract test:** `db-seed-runnable.contract.test.ts` — asserts `packages/db/src/index.ts` does NOT contain `import 'server-only'`.

## 15.3 DB-5: Compound cursor must be USED in WHERE, not just accepted

**Symptom:** Product listing pagination returns the same first N items on every "next page" request.

**Root cause:** The `cursor` input was accepted by the query schema but never used in the WHERE clause. The `conditions` array only had `isActive` and `collection` filters — the cursor was computed and returned as `nextCursor`, but when the client passed it back, it was silently ignored.

**Fix:** Implement compound cursor pagination:
1. Change cursor schema from `z.string().uuid()` to `z.string()` (opaque encoded cursor)
2. Decode cursor as `${sortValue}|${id}`
3. Add cursor-based WHERE clause for each sort option (using `OR` for tie-breaking)
4. Encode `nextCursor` from the last row's sort value + id

**Contract test:** `cursor-pagination.contract.test.ts` — asserts the cursor is decoded and used in a WHERE condition.

## 15.4 SDK-5: Stripe webhook returning 500 on handler errors → infinite retries

**Symptom:** Transient errors (DB connection blip) cause Stripe to retry webhooks for up to 3 days.

**Root cause:** The webhook route returned HTTP 500 on any handler error after signature verification. Stripe interprets non-200 responses as "retry later" and retries for 3 days.

**Fix:** Return HTTP 200 for ALL handler errors after signature verification passes. The idempotency layer (`payment_events.stripe_event_id` UNIQUE + `pg_advisory_xact_lock`) ensures duplicate events are safe to re-process.

```ts
// BAD — Stripe retries forever
return NextResponse.json({ error: message }, { status: 500 });

// GOOD — Stripe stops retrying
console.error('[stripe-webhook] Handler error:', message);
return NextResponse.json({ received: true, error: message });
```

**Contract test:** `webhook-error-handling.contract.test.ts` — asserts the route does not return status 500 in the handler-error catch block.

## 15.5 DB-6: Non-atomic multi-row writes (must use db.transaction())

**Symptom:** A mid-flow failure (e.g., line-items insert fails) leaves an orphaned pending order in the database.

**Root cause:** `checkout.createPaymentIntent` inserted the order and then inserted line items as two separate queries without wrapping in `db.transaction()`.

**Fix:** Wrap multi-row writes in `db.transaction()`.

```ts
const order = await ctx.db.transaction(async (tx) => {
  const [newOrder] = await tx.insert(orders).values({...}).returning({...});
  if (!newOrder) throw new TRPCError({ code: 'INTERNAL_SERVER_ERROR' });
  await tx.insert(lineItems).values(cartItemsList.map(item => ({ orderId: newOrder.id, ... })));
  return newOrder;
});
```

## 15.6 SDK-6: Missing Stripe idempotencyKey in stripe.paymentIntents.create()

**Symptom:** A retry creates duplicate Payment Intents for the same order.

**Root cause:** The code generated an idempotency key and stored it on the order, but never passed it to the Stripe SDK call.

**Fix:** Pass `{ idempotencyKey }` as the second argument to `stripe.paymentIntents.create()`.

```ts
const paymentIntent = await stripe.paymentIntents.create(
  { amount, currency: 'usd', metadata: {...} },
  { idempotencyKey },
);
```

**Contract test:** `stripe-idempotency.contract.test.ts` — asserts the 2nd argument shape.

## 15.7 TRPC-3: rateLimitMiddleware loses session type narrowing

**Symptom:** Adding `.use(rateLimitMiddleware)` after `protectedProcedure` causes TS18047: `'ctx.session' is possibly 'null'`.

**Root cause:** The standalone `rateLimitMiddleware` (created via `t.middleware()`) doesn't preserve the session type narrowing that `protectedProcedure` establishes via `next({ ctx: { ...ctx, session: ctx.session } })`.

**Fix:** Define a `protectedRateLimitedProcedure` builder that composes the rate-limit step inside the narrowed context via inline `.use()`:

```ts
export const protectedRateLimitedProcedure = protectedProcedure.use(
  async ({ ctx, next }) => {
    // rate limiting logic here — ctx.session is narrowed to Session (not null)
    return next({ ctx });
  },
);
```

**Contract test:** `rate-limited-procedures.contract.test.ts` — asserts the 3 payment mutations use `protectedRateLimitedProcedure`.

## 15.8 AUTH-1: Missing BETTER_AUTH_URL host-mismatch warning

**Symptom:** Session cookies set for the wrong domain → P0 auth outage (users can't log in).

**Root cause:** No runtime check comparing `BETTER_AUTH_URL` and `NEXT_PUBLIC_APP_URL` hosts.

**Fix:** Add a `warnOnAuthUrlMismatch()` helper in `packages/config/src/env.ts`, guarded by `typeof window === 'undefined'` (see ENV-1 above).

**Contract test:** `auth-url-warning.contract.test.ts` — asserts the check exists.

## 15.9 TEST-2: vitest server-only stub alias required

**Symptom:** Tests that transitively import a `server-only`-guarded module fail with `"This module cannot be imported from a Client Component module"`.

**Root cause:** The `server-only` package throws in non-`react-server` contexts. Vitest runs in Node, not React Server Components.

**Fix:** Add a `server-only` stub alias to every `vitest.config.ts`:

```ts
resolve: {
  alias: {
    'server-only': resolve(__dirname, '../../scripts/server-only-stub.js'),
  },
},
```

The stub file (`scripts/server-only-stub.js`) is a 1-line no-op: `// Stub for vitest — server-only is a no-op in test environments`.

## 15.10 Lesson Summary: server-only guard placement principle

The `server-only` guard is a **build-time** tool to prevent accidental client-side bundling. Its placement follows a simple principle:

| Layer | Guard? | Why |
|---|---|---|
| **API/server boundary consumer** (`api/context.ts`, `api/trpc.ts`, `auth/config.ts`) | ✅ YES | These modules are only imported by server code; the guard prevents accidental client imports |
| **Low-level utility** (`db/index.ts`) | ❌ NO | These modules are consumed by both server code AND CLI scripts (`tsx`); the guard breaks CLI scripts |
| **Client Component** (`'use client'` files) | ❌ NO | These are explicitly client-side |

**The guard belongs at the consumer, not the utility.**

---

# 16. v15-v18 Remediation Arc Lessons (v1.6 Supplement)

**Date:** 2026-08-02  
**Source:** Maison e-commerce monorepo remediation (commits `e1eccdc` through `64728de6`)

This supplement documents 8 lessons from the v15-v18 remediation arc.

## 16.1 DEP-7: Systematic unused-dependency audit with contract tests

**Symptom:** 38 unused dependencies across 6 packages bloated install tree (166 packages removed on cleanup).

**Root cause:** Dependencies accumulated over time without import audits. Some were transitive type deps (e.g., `zod` in `@maison/auth` for Better Auth inferred types) — these must be kept with documentation.

**Fix:** 
1. Write a contract test (`deps-hygiene.contract.test.ts`) that parses each package's `package.json` + scans its `src/` for imports, then asserts declared deps match used imports.
2. Remove unused deps via script.
3. Re-add transitive type deps with explicit comments (e.g., `// Transitive Better Auth type dependency`).

**Contract test:** `deps-hygiene.contract.test.ts` — 37 tests, asserts no unused deps in any `@maison/*` package.

**Lesson:**
> Unused dependencies are silent debt. A contract test that compares `package.json` deps against actual imports catches drift automatically. Transitive type deps (like `zod` for Better Auth) must be documented, not deleted.

## 16.2 DEP-8: tsconfig.config.json for root-config type-checking

**Symptom:** Root config files (`next.config.ts`, `tailwind.config.ts`, `drizzle.config.ts`, `proxy.ts`, etc.) were outside `tsconfig.json` `include` globs — type errors in them were invisible.

**Root cause:** Each package's `tsconfig.json` only included `src/**/*.ts`. Root configs were never type-checked.

**Fix:**
1. Add `tsconfig.config.json` to each package with `"include": ["*.config.ts", "*.config.tsx"]`.
2. Update `check-types` script to run both: `"tsc -p tsconfig.config.json --noEmit && tsc --noEmit"`.

**Contract test:** `tsconfig-include.contract.test.ts` — 9 tests, asserts tsconfig.config.json include globs cover every root config file. Type-check cleanliness is enforced by the per-package `check-types` script, not this test.

**Lesson:**
> A green `check-types` can hide latent errors if include globs are too narrow. Always add a `tsconfig.config.json` + dual-check script for root config files.

## 16.3 DEP-9: ESLint flat config for all packages with per-package overrides

**Symptom:** Only 1 of 12 packages had `eslint.config.mjs`; the rest relied on a shared config that couldn't be extended correctly.

**Root cause:** ESLint flat config requires each package to have its own config file that imports the shared config directly (no `FlatCompat`). The shared config (`@maison/eslint-config`) must export a flat array with proper `exports`.

**Fix:**
1. Create `eslint.config.mjs` in each of 11 consumer packages (7 `@maison/*` + `tooling/tailwind` + `services/workers` + `apps/web` + `apps/studio`).
2. Import shared config directly: `import sharedConfig from '@maison/eslint-config'; export default [...sharedConfig];`
3. Add per-package override blocks downgrading noisy type-aware rules to `warn` (Drizzle `or()`/`and()` false positives, `@typescript-eslint/no-unnecessary-condition` on nullish coalescing, etc.).

**Lesson:**
> Flat config cannot be shared via `extends` — each package needs its own config file. Per-package overrides for framework-specific noise (Drizzle, tRPC) are essential; don't disable rules globally.

## 16.4 TS-12: Zod v4 native API migration — systematic pattern

**Symptom:** Pre-migration inventory showed 40 deprecated `z.string().uuid()` / `.url()` / `.email()` / `.datetime()` calls across 12 files; Zod v4 mandates native top-level forms. Post-migration state: zero deprecated calls, 40 v4-native API sites across 12 files.

**Root cause:** Zod v4 deprecated the chained-string methods in favor of native string-format validators: `z.uuid()`, `z.url()`, `z.email()`, `z.iso.datetime()`.

**Fix:** Mechanical migration via script:
- `z.string().uuid()` → `z.uuid()`
- `z.string().url()` → `z.url()`
- `z.string().email()` → `z.email()`
- `z.string().datetime()` → `z.iso.datetime()`
- `z.string().uuid().optional()` → `z.uuid().optional()` (preserve chains)

**Contract tests:**
- `zod-email.contract.test.ts` — asserts 4 email-validating files use `z.email()`, not `z.string().email()`.
- `zod-v4-native-api.contract.test.ts` — 167 tests, walks all prod files and asserts zero deprecated forms across all 4 patterns.

**Lesson:**
> SDK method drift requires systematic migration with contract tests. Don't manually fix — script it, then lock with a test that scans the entire source tree.

## 16.5 TS-13: Non-null assertion cleanup with TRPCError guards

**Symptom:** 18 residual `!` postfix assertions in 7 router files (`loyalty`, `admin`, `account`, `reviews`, `discounts`, `trade`, `cart`) — `TS18047` under strict mode.

**Root cause:** `!` postfix is not a type guard — it asserts non-null to the compiler but crashes at runtime if wrong. The v12 cleanup fixed checkout/gift-cards/cart; v16 extended to 6 more routers.

**Fix:** Replace every `value!` with explicit guard:
```ts
// BAD
const x = value!;
// GOOD
if (!value) throw new TRPCError({ code: 'INTERNAL_SERVER_ERROR', message: '...' });
const x = value;
```

**Contract test:** `non-null-assertion-cleanup.contract.test.ts` — 6 tests, audits 6 router files with regex that catches postfix `!` (excluding prefix `!` logical-NOT and Drizzle `or()`/`and()` intentional `)!`).

**Lesson:**
> Non-null assertions are a runtime hazard. Replace with explicit `TRPCError` guards that fail loudly with context. Lock with a contract test that scans for the regex pattern.

## 16.6 REACT-7: `||` → `??` for empty-string preservation in form fields

**Symptom:** 3 sites in `trade.ts` used `input.field || null` where `field` was an optional string (`z.string().optional()` for instagram/projectTypes, `z.url().optional().or(z.literal(''))` for website) — empty string `''` is a valid input, but `||` coerces it to `null`.

**Root cause:** JavaScript's `||` treats `''` as falsy. The nullish coalescing operator `??` only falls through on `null`/`undefined`, preserving `''`.

**Fix:** Replace `|| null` with `?? null` for optional string fields where empty string is semantically valid.

**Lesson:**
> When a schema accepts `z.literal('')` (empty string as valid), `||` is a bug. Use `??` for nullish coalescing. This is a real logic error, not just style.

## 16.7 SECURITY-3: Email template apostrophe escaping + PII-redacted logging

**Symptom:** 5 unescaped apostrophes in `OrderConfirmation.tsx` / `WelcomeMember.tsx` were remediated (now use `&apos;`). Separately, 3 production runtime sites logged PII (email, message body, Stripe payload) — remediated to `console.warn` with `(PII redacted)` markers.

**Fix:**
1. Replace `'` → `&apos;` in all JSX text nodes (mechanical).
2. Adopt `(PII redacted)` logging pattern:
   ```ts
   // Contact form
   console.warn('[contact] Submission received (PII redacted)');
   // Newsletter
   console.warn('[newsletter] New subscriber from ${input.source} (PII redacted)');
   // Stripe webhook
   console.warn('[stripe] Order ${order.orderNumber} confirmed + email sent (PII redacted)');
   ```

**Lesson:**
> Skill §13.10 mandates PII redaction. Never log user-supplied data. Email templates must escape `'` → `&apos;` in JSX text — not `'` (both work but `&apos;` is the HTML5 named entity).

## 16.8 REACT-8: React 19 `SubmitEvent` migration — handler-specific types

**Symptom:** 11 form handlers used deprecated `React.FormEvent<HTMLFormElement>` (or `React.SyntheticEvent<HTMLFormElement>`).

**Fix:** Migrate to `React.SubmitEvent` — matches the `onSubmit` handler type exactly and retains `.preventDefault()`.

**Contract test:** `react-submit-event.contract.test.ts` — 1 test, asserts zero `React.SyntheticEvent<HTMLFormElement>` in `apps/web/src` production code. (Note: test only asserts absence; a positive-presence assertion for `React.SubmitEvent` is a future enhancement.)

**Lesson:**
> React 19 deprecates `FormEvent`. Use handler-specific event types: `SubmitEvent` for `onSubmit`, `ChangeEvent` for `onChange`, etc. This is both a lint fix and a semantic correctness fix.

---

# 17. Additional Anti-Patterns (v15-v18)

## 17.1 Dependency Anti-Patterns

| Anti-Pattern | Description | Prevention |
|---|---|---|
| Unused transitive type dep deleted | `zod` removed from `@maison/auth` broke Better Auth inferred types | Document transitive type deps with comments; contract test validates |
| Root config outside type-check | `next.config.ts`, `drizzle.config.ts` never type-checked | Add `tsconfig.config.json` + dual-check script |
| Single ESLint config for all packages | Flat config can't be `extends`'ed; each package needs own file | Create per-package `eslint.config.mjs` importing shared config |
| No per-package override block | Type-aware rules fire false positives on Drizzle/tRPC patterns | Add override block downgrading noisy rules to `warn` |

## 17.2 TypeScript Anti-Patterns

| Anti-Pattern | Description | Prevention |
|---|---|---|
| Deprecated Zod chained methods | `z.string().uuid()` / `.email()` / `.url()` / `.datetime()` in v4 | Migrate to native `z.uuid()` / `z.email()` / `z.url()` / `z.iso.datetime()` |
| Non-null assertion on nullable value | `value!` crashes at runtime if wrong | Replace with `if (!value) throw TRPCError(...)` |
| `||` on empty-string-valid field | `field || null` coerces `''` → `null` | Use `??` for nullish coalescing |
| Missing transitive type dep | Better Auth infers types from `zod` but `zod` not declared | Declare transitive type deps with comments |

## 17.3 React Anti-Patterns

| Anti-Pattern | Description | Prevention |
|---|---|---|
| Unescaped apostrophe in JSX | `We've` in JSX text | Replace `'` → `&apos;` |
| PII in structured logs | `console.log(user.email, message)` | Use `(PII redacted)` pattern; log only IDs/types/source |
| Deprecated `FormEvent` | React 19 warns on `React.FormEvent<HTMLFormElement>` | Use `React.SubmitEvent` |

## 17.4 Security Anti-Patterns

| Anti-Pattern | Description | Prevention |
|---|---|---|
| Raw `JSON.stringify` in `dangerouslySetInnerHTML` | XSS if data contains `</script>` | Apply `escapeForScriptContext()` (5-char canonical: `<>&` + U+2028 + U+2029) |
| PII in console logs | Email, message body, Stripe payload leaked | Skill §13.10: `(PII redacted)` pattern mandatory |

---

# 18. Additional Patterns (v15-v18)

## 18.1 Dependency Patterns

### Pattern: Contract test for dependency hygiene
```ts
// deps-hygiene.contract.test.ts
for (const pkg of MAISON_PACKAGES) {
  it(`${pkg} declares only used deps`, () => {
    const pkgJson = JSON.parse(readFileSync(join(pkg, 'package.json'), 'utf8'));
    const imports = scanImports(join(pkg, 'src'));
    const declared = new Set([...Object.keys(pkgJson.dependencies || {}), ...Object.keys(pkgJson.devDependencies || {})]);
    const unused = [...declared].filter(d => !imports.has(d) && !isTransitiveTypeDep(d));
    expect(unused, `Unused deps: ${unused.join(', ')}`).toEqual([]);
  });
}
```

### Pattern: Dual check-types script for root configs
```json
"check-types": "tsc -p tsconfig.config.json --noEmit && tsc --noEmit"
```

### Pattern: Per-package ESLint flat config with overrides
```js
// eslint.config.mjs
import sharedConfig from '@maison/eslint-config';
export default [
  ...sharedConfig,
  {
    rules: {
      '@typescript-eslint/no-unnecessary-condition': 'warn',
      '@typescript-eslint/no-deprecated': 'warn',
      // ... Drizzle-specific noise
    },
  },
];
```

## 18.2 TypeScript Patterns

### Pattern: Zod v4 native string formats
```ts
// Good (Zod v4)
z.uuid(), z.url(), z.email(), z.iso.datetime()
// Bad (deprecated)
z.string().uuid(), z.string().email(), z.string().url(), z.string().datetime()
```

### Pattern: Explicit TRPCError guards over non-null assertions
```ts
// Good
if (!customer) throw new TRPCError({ code: 'NOT_FOUND', message: 'Customer not found' });
const email = customer.email;
// Bad
const email = customer!.email;
```

### Pattern: Nullish coalescing for empty-string preservation
```ts
// Good — preserves '' as valid input
const website = input.website ?? null;
// Bad — coerces '' to null
const website = input.website || null;
```

## 18.3 Security Patterns

### Pattern: PII-redacted logging (Skill §13.10)
```ts
// Contact form
console.warn('[contact] Submission received (PII redacted)');
// Newsletter
console.warn('[newsletter] New subscriber from ${input.source} (PII redacted)');
// Stripe webhook
console.warn('[stripe] Order ${order.orderNumber} confirmed + email sent (PII redacted)');
```

### Pattern: JSON-LD XSS prevention
```ts
import { escapeForScriptContext } from '@/lib/utils';
<script type="application/ld+json" dangerouslySetInnerHTML={{ __html: escapeForScriptContext(JSON.stringify(jsonLd)) }} />
```

## 18.4 React Patterns

### Pattern: React 19 handler-specific event types
```ts
// Good
const handleSubmit = async (e: React.SubmitEvent) => {
  e.preventDefault();
  // ...
};
// Deprecated
const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => { ... };
```

---

# 19. Updated Field Card (v16)

```text
1. Reproduce the exact failure.
2. Identify the gate: install / type / lint / format / test / db / hook.
3. Separate infrastructure failure from source-code debt.
4. Use authoritative diagnostics.
5. Build a hypothesis table.
6. Apply the smallest correct fix.
7. Do not weaken guardrails.
8. Run the fixed gate.
9. Run adjacent gates.
10. If DB: verify objects, not just exit code.
11. If ESLint autofix: run Prettier after.
12. If Prettier ignore: test exact command.
13. If SDK: inspect exports and installed types.
14. If parser error: inspect previous line.
15. If script edit: validate before mutating.
16. If tRPC build fails: check procedure names for JS reserved words.
17. Check git status and staged state.
18. Record outstanding issues.
19. Do not claim success before verification.
20. If `useRef`/`useState` crash in SSR: Better Auth React hooks must not run during SSR — wrap in `ClientOnly` boundary, never use `next/dynamic ssr:false` in Server Components.
21. If public page shows empty prerender: check whether server caller calls `next/headers` — use `apiPublic()` for session-free public data.
22. If build warns `DYNAMIC_SERVER_USAGE` on a public route: this is a real bug (empty prerender + lost static benefits), not cosmetic.
23. Before trusting a prior remediation document: verify its claims against the actual error log.
24. If build warns `DYNAMIC_SERVER_USAGE` on an auth-guarded route (`/account/*`, `/admin/*`): this is expected and correct — the layout calls `headers()` for session verification. Do NOT add `force-dynamic` to silence it (incompatible with `cacheComponents: true`).
25. The `api()`/`apiPublic()` split is a Server Component concern. Client Components use `trpc` from `@/lib/trpc/client` — they never call `api()` or `apiPublic()`.
26. Source contract tests (read source, assert import) lock architectural invariants faster and more reliably than build-output tests.
27. If `check-types` shows TS18047 after `expect().not.toBeNull()`: runtime assertions don't narrow types — use `readFileSync` or real type guard.
28. If Zod v4 deprecation warnings: migrate `z.string().uuid()` → `z.uuid()`, `.email()` → `z.email()`, `.url()` → `z.url()`, `.datetime()` → `z.iso.datetime()`.
29. If non-null assertions (`!`) on nullable values: replace with explicit `TRPCError` guards.
30. If `||` on optional string field: use `??` to preserve empty string.
31. If `console.log` in production: use `console.warn` + `(PII redacted)` pattern.
32. If email template has `'` in JSX: escape to `&apos;`.
33. If `React.FormEvent` in form handler: migrate to `React.SubmitEvent`.
34. If `JSON.stringify` in `dangerouslySetInnerHTML`: apply `escapeForScriptContext()`.
```

---

# 20. Conclusion

The v15-v18 remediation arc adds 8 new lessons spanning dependency hygiene, TypeScript strictness, React 19 migration, security hardening, and systematic contract-test locking. The pattern is consistent: **every systemic issue is caught by a contract test that prevents regression**. The handbook now contains 20+ lessons ranked by impact, 10+ anti-pattern catalogs, 18+ case-index entries, and a 34-item field card — making future agents significantly less likely to repeat these classes of mistakes.
