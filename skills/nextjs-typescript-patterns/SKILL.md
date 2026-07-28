---
name: nextjs-typescript-patterns
description: Monorepo web projects using pnpm, Turborepo, TypeScript, Next.js, React, ESLint, Prettier, Drizzle ORM, Postgres, and third-party SDKs (tRPC, Trigger.dev, Stripe, Better Auth, Sanity, React Email, Vitest). v1.2 — canonical troubleshooting handbook with 40+ case-indexed anti-patterns across install, type-check, lint, format, test, build, migration, and pre-commit-hook gates. Covers pnpm 10+ native-build approval (allowBuilds, onlyBuiltDependencies), strict workspace isolation, tsconfig path aliases and inherited baseUrl, Drizzle migration journal drift and silent spinner-masked failures, exactOptionalPropertyTypes, noUncheckedIndexedAccess, React 19 SubmitEvent migration, ESLint flat-config FlatCompat, Prettier ignore-path semantics, SDK drift (subpath exports, hardcoded API versions, callback payload shapes), and the Surgical Change Discipline. Use when debugging failing gates, reproducing mysterious install/type/lint/format/hook failures, remediating monorepo tooling debt across Next.js + TypeScript + Drizzle + tRPC + Better Auth, or hardening a fresh monorepo against repeated mistakes — symptoms like ERR_PNPM_NO_MATCHING_VERSION, TS2307/TS2339, __esModule config errors, passWithNoTests, or silent DATABASE_URL/Drizzle migration failures.
version: 1.2
---

# Consolidated Agent Briefing Document and Programming Handbook

## Agent Programming and Troubleshooting Handbook

Version: 1.2  
Scope: Monorepo web projects using pnpm, Turborepo, TypeScript, Next.js, React, ESLint, Prettier, Drizzle, Postgres, and third-party SDKs.  
Purpose: Prevent repeated mistakes and provide a reusable troubleshooting methodology.  
Reconciliation note: v1.2 absorbs the genuine deltas from `update.md` (parser-error line attribution + `cat -A`; `psql -f` fallback for spinner-masked silent Drizzle failures; the named "Surgical Change Discipline" and the Stillwater reference-copy caveat). The remainder of `update.md` was already present here in expanded form.

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

### Rule

> Fix infrastructure first. Then remediate source-code debt deliberately.

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
React.SubmitEvent<HTMLFormElement>
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
function onSubmit(e: React.SubmitEvent<HTMLFormElement>) {
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

A batch can be “applied” but not “verified.”

Rule:

> Do not report success until the relevant gate passes.

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
| TS-1 | Alias resolution broken | Inherited `baseUrl` | Local `baseUrl` | Trace module resolution |
| TS-2 | Missing lib scaffolding | Files absent | Scaffold from contracts | Adapt reference carefully |
| TS-3 | Async caller misuse | Property access on promise | Await caller | Await factories |
| TS-4 | Nullable join shapes | Drizzle left-join inference | Router boundary coercion | Shape data at boundaries |
| TS-5 | DrizzleDB union | Incompatible driver union | Canonical Neon type | Avoid unusable unions |
| TS-6 | Better Auth drift | API changed | Use new methods/payloads | Verify installed SDK |
| TS-7 | Stripe drift | Hardcoded version/types | Remove literal, local types | Avoid hardcoded SDK literals |
| TS-8 | Missing API deps | Undeclared imports | Add workspace deps | pnpm isolation requires declaration |
| ESLINT-1 | `__esModule` config error | FlatCompat with flat config | Direct flat import | Use modern ESLint correctly |
| ESLINT-2 | Lint autofix drift | Prettier not rerun | Format after lint:fix | Tool ordering matters |
| ESLINT-3 | 89 lint violations | Source-code debt | Batched remediation | Separate infra from debt |
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
16. Check git status and staged state.
17. Record outstanding issues.
18. Do not claim success before verification.
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

