# The Maison Monorepo Agent Handbook: Troubleshooting, Patterns, and Anti-Patterns

This document is a comprehensive distillation of the troubleshooting experiences, architectural mistakes, and programming patterns encountered during the remediation of the `@maison` monorepo. It is designed as a definitive playbook for AI agents and developers to avoid repeating these errors, recognize hidden anti-patterns, and apply correct troubleshooting methodologies in complex Next.js / Turborepo / pnpm / Drizzle / tRPC environments.

---

## Part 1: The Agent’s Troubleshooting Methodology

Before touching code, an agent must adopt the following diagnostic principles. The majority of bugs in this project were not caused by complex logic, but by **false assumptions about tooling boundaries, dependency resolution, and error message literalism.**

### 1. Never Trust the Error Message's Line Number Blindly
*   **The Mistake:** Prettier reported a fatal syntax error on line 16 of `trpc.test.ts`. The agent initially tried to fix line 16.
*   **The Reality:** The actual defect was an unclosed parenthesis on line 15. Parsers often report the error at the *next token they cannot reconcile*, not the origin of the defect.
*   **The Playbook:** When facing a fatal syntax/parse error, do not just look at the reported line. Count brackets/parentheses on preceding lines. Use AST tools or `cat -A` to check for hidden characters. 

### 2. Validate Documentation Against the Installed Registry
*   **The Mistake:** The code imported `@trigger.dev/sdk/v4` because the installed package was `v4.5.7`. The agent assumed the subpath existed.
*   **The Reality:** The npm package's `exports` map did not contain a `/v4` subpath. The main entry `.` was the v3 API surface.
*   **The Playbook:** Never guess module subpaths based on SemVer. Always inspect the actual `node_modules/<package>/package.json` `exports` field or the `index.d.ts` file to verify the exact API surface and import paths.

### 3. Beware of Silent Failures and Tooling Spinners
*   **The Mistake:** `drizzle-kit migrate` failed with `[ELIFECYCLE] Command failed with exit code 1`, but printed no SQL error.
*   **The Reality:** Drizzle Kit's animated spinner overwrote the standard error output from Postgres (`ERROR: type "discount_type" already exists`).
*   **The Playbook:** If a CLI tool fails silently, bypass the tool's output formatting. Check the underlying service logs (e.g., `docker logs postgres`), or strip ANSI escape codes, or run the underlying command directly (e.g., `psql -f migration.sql`).

### 4. Isolate the Blast Radius (pnpm Workspace Isolation)
*   **The Mistake:** `@maison/api` failed to resolve `@maison/payments` and `@upstash/ratelimit`, even though they were installed in the monorepo.
*   **The Reality:** pnpm uses strict, isolated `node_modules` by default. A package cannot import a dependency just because it exists in the workspace root or another package.
*   **The Playbook:** If a module resolves in development but fails in type-checking/CI, verify it is explicitly declared in the *consuming package's* `package.json`. Use `workspace:*` for internal packages.

---

## Part 2: Database & Drizzle ORM Patterns

### Anti-Pattern: The Drizzle Driver Union Trap
*   **The Issue:** The database was initialized conditionally: `export const db = isNeon ? drizzleNeon() : drizzlePg();`. The type was exported as `export type DrizzleDB = typeof db;`.
*   **The Failure:** TypeScript widened `DrizzleDB` to `NeonHttpDatabase | NodePgDatabase`. Because the two drivers have incompatible method overloads, calling `.returning({ id: table.id })` threw `TS2554: Expected 0 arguments, but got 1`.
*   **The Fix:** Canonicalize the type to the production driver. 
    ```typescript
    // Anti-pattern
    export type DrizzleDB = typeof db; 
    
    // Correct Pattern
    import type { NeonHttpDatabase } from 'drizzle-orm/neon-http';
    export type DrizzleDB = NeonHttpDatabase<typeof schema>;
    ```
*   **Lesson:** Runtime conditionals that swap underlying ORM drivers will create union types that break method overloads. Always type your DB instance to your primary production driver.

### Anti-Pattern: Auto-Generating Migrations Without Snapshots
*   **The Issue:** Running `drizzle-kit generate` in a setup script created a full-schema dump (`0001_abnormal_puck.sql`) instead of an incremental diff, because Drizzle snapshot metadata was missing. This caused `CREATE TYPE` to fail on subsequent runs.
*   **The Fix:** Never run `generate` in automated provisioning scripts (`db:setup`). Setup scripts should only run `migrate` and `seed`. `generate` is a developer workflow step that requires committed snapshots to compute incremental diffs.

### Anti-Pattern: Orphaned Migration Journals
*   **The Issue:** A migration file (`0001_phase3.sql`) was committed, but its entry was missing from `_journal.json`. Drizzle ignored it, leading to state drift.
*   **The Fix:** Always verify `_journal.json` integrity when manually curating or merging SQL migrations. 

### Pattern: Environment Loading Order in Seed Scripts
*   **The Issue:** `DATABASE_URL is not set` during seeding, even though `.env.local` existed.
*   **The Root Cause:** The DB client (`import { db } from './db'`) was imported at the top of the seed script. The client reads `process.env` at *module initialization time*. The `dotenv` loader was in a separate file that was imported *after* the DB client.
*   **The Fix:** Environment variables must be loaded before any module that depends on them is initialized.
    ```typescript
    // packages/db/src/seed/index.ts
    import './env'; // MUST be the very first import
    import { db } from '../index'; 
    ```

---

## Part 3: TypeScript & Third-Party API Drift

### Anti-Pattern: Fragile Type Extraction
*   **The Issue:** Extracting the DB type from the tRPC context using `Parameters<Parameters<typeof router>[0]['query']>[0]['ctx']['db']`.
*   **The Fix:** Use canonical types. Import `DrizzleDB` directly from the DB package. Fragile type hacks break the moment the router signature changes.

### Pattern: Handling `exactOptionalPropertyTypes` with External SDKs
*   **The Issue:** Stripe's `refund.create` rejected `amount: undefined` when a variable was optional, due to TypeScript's `exactOptionalPropertyTypes` flag.
*   **The Fix:** Use conditional object spreading to completely omit the property rather than passing `undefined`.
    ```typescript
    // Anti-pattern
    stripe.refunds.create({ amount: amountCents }); // Fails if amountCents is undefined
    
    // Correct Pattern
    stripe.refunds.create({
      ...(amountCents !== undefined ? { amount: amountCents } : {})
    });
    ```

### Pattern: Coercing Nullable Joins for Strict Inserts
*   **The Issue:** A `leftJoin` in Drizzle returns `number | null` for foreign columns, but the target table's insert schema requires `number`.
*   **The Fix:** Coerce at the router boundary before insertion.
    ```typescript
    priceCents: Number(item.priceCents ?? 0)
    ```
    *(Note: Agents must flag this to the user, as treating null prices as 0 is a business logic decision, not just a type fix).*

### Pattern: Double-Casting Raw SQL Results
*   **The Issue:** Drizzle's `.execute()` returns a driver-specific result wrapper, not a raw array. Direct casting `result as Array<...>` fails.
*   **The Fix:** Cast through `unknown` to satisfy the compiler while preserving runtime behavior.
    ```typescript
    const rows = result as unknown as Array<Record<string, unknown>>;
    ```

---

## Part 4: Tooling Boundaries (Prettier, ESLint, Vitest)

### Anti-Pattern: Using `.prettierrc` for Path Exclusion
*   **The Mistake:** Attempting to add an `ignore` array inside `.prettierrc` to exclude the `docs/` folder.
*   **The Reality:** Prettier 3 removed path exclusion from the config file. Config files are strictly for formatting options.
*   **The Fix:** Use a dedicated `.prettierignore` file and explicitly pass it to the CLI.
    ```json
    // package.json scripts
    "format": "prettier --write \"**/*.{ts,tsx,md,json,css}\" --ignore-path .gitignore --ignore-path .prettierignore"
    ```

### Anti-Pattern: Trailing Slashes in Ignore Files
*   **The Mistake:** Writing `docs/` in `.prettierignore`.
*   **The Reality:** Prettier's gitignore-style matcher does not reliably match direct-path globs with trailing slashes.
*   **The Fix:** Omit the trailing slash. Use `docs` instead of `docs/`.

### Pattern: Vitest Empty Suite Failures
*   **The Issue:** `pnpm test` fails with exit code 1 in packages like `@maison/auth` or `@maison/payments`.
*   **The Reality:** Vitest exits with an error if it finds zero test files. This is not a code failure; it's a configuration gap.
*   **The Fix:** Either author a minimal placeholder test, or add `--passWithNoTests` to the Vitest script in `package.json`.

---

## Part 5: Dependency & Schema Hygiene

### Anti-Pattern: Version Conflation
*   **The Mistake:** Declaring `@react-email/components@^6.6.5` and `sanity@^6.30.0`.
*   **The Reality:** The agent conflated the framework versions (`react-email@6.x`, `sanity@3.x`) with the component library versions. Those specific versions never existed on npm.
*   **The Playbook:** Before fixing a "missing version" error, verify if the dependency is actually used. In the case of `@react-email/components`, it was declared but never imported. The correct fix was deletion, not version pinning.

### Anti-Pattern: Sanity Schema Misplacement
*   **The Mistake:** Placing `options: { hotspot: true }` on an `array` type instead of the `image` member inside the `of: []` block.
*   **The Fix:** Sanity schema options must be applied to the specific field type that supports them.
    ```typescript
    // Anti-pattern
    defineField({ name: 'images', type: 'array', of: [{ type: 'image' }], options: { hotspot: true } })
    
    // Correct Pattern
    defineField({ name: 'images', type: 'array', of: [{ type: 'image', options: { hotspot: true } }] })
    ```

---

## Part 6: The "Surgical Change" Discipline

Throughout the remediation, the most successful interventions adhered to a strict "Surgical Change" discipline. Agents must internalize these rules:

1.  **Do Not Bundle Unrelated Fixes:** If the error is a Prettier syntax error, fix the syntax. Do not run a repo-wide `pnpm format` unless explicitly approved.
2.  **Verify the Blast Radius:** Before applying a fix, check how many files it touches. If a type fix requires changing 30 router files, look for a canonical type definition at the source (e.g., fixing `DrizzleDB` at the DB package level).
3.  **Preserve Commit Hygiene:** Never auto-commit. Leave the working tree in a state where the user can logically group changes (e.g., separating infrastructure config fixes from source-code lint remediation).
4.  **No Speculative Scaffolding:** If an ESLint config or test setup is missing, only add what is strictly required to pass the current gate. Do not copy entire override blocks from reference projects (like Stillwater) if the target project doesn't yet have the files those overrides apply to.

---

## Summary Checklist for Future Agents

When handed a new monorepo with failing gates, execute in this order:
1.  **Read the actual error, not the summary.** (Check Docker logs, strip ANSI, count brackets).
2.  **Verify the dependency graph.** (Check `package.json` exports, verify pnpm workspace links).
3.  **Check tooling boundaries.** (Are we using Prettier 3 configs correctly? Is Vitest configured for empty suites?).
4.  **Isolate the type union.** (Are conditional DB drivers creating incompatible TS unions?).
5.  **Validate API drift against `node_modules`.** (Don't trust the docs; inspect the installed `.d.ts` files).
6.  **Apply surgical fixes.** (Fix the root cause, not the symptom; avoid repo-wide churn).

