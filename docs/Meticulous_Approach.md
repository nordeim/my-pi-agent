# **Meticulous Approach — Six-Phase Workflow**  
Follow `ANALYZE → PLAN → VALIDATE → IMPLEMENT → VERIFY → DELIVER` for all implementation, debugging, refactor, and remediation work. First analyze the full relevant context: files, tests, configs, schema, docs, design tokens, and executable evidence. Then produce the smallest correct, sequential plan, confirming scope for ambiguous or high-risk changes involving auth, sessions, money, state machines, public contracts, destructive data, or security. Validate assumptions against executable truth before coding. Implement in small, typed, test-backed increments, keeping reusable logic in shared seams and updating tests/docs with the change. Verify with the project’s full gate — lint, typecheck, tests, build, smoke/e2e where available — and browser-verify UI changes; never claim success without executed evidence. Deliver atomically, update documentation lockstep, remove scratch artifacts, and hand off with a clear report of what was Verified, Reasoned, Assumed, or Unverifiable.

Use this workflow for implementation, debugging, refactoring, audit remediation, and UI work. Each phase should produce enough evidence to justify moving to the next phase.

---

## 1. ANALYZE

### Purpose

Understand the problem completely before proposing or changing anything.

### Required behavior

- Read all relevant artifacts in full before planning or editing:
  - affected pages, components, routes, hooks, services, and utilities;
  - tests, fixtures, mocks, and e2e specs;
  - schema, migrations, seeds, and database access layers;
  - configs, lockfiles, environment examples, CI scripts, and package scripts;
  - relevant docs, plans, worklogs, screenshots, and design-token sources.
- Never rely on partial excerpts, truncated views, stale summaries, or remembered file contents.
- Identify:
  - explicit requirements;
  - implicit constraints;
  - ambiguous points;
  - non-functional requirements such as scale, latency, accessibility, browser/runtime targets, compliance, and security;
  - affected consumers, public contracts, and downstream dependencies.
- Determine the governing contract for the change:
  - API contract;
  - database contract;
  - validation contract;
  - authentication/session contract;
  - authorization/permission contract;
  - routing contract;
  - UI-parity/design-token contract;
  - state-machine or workflow contract;
  - feature-flag or rollout contract.
- For reported failures:
  - reproduce the failure before theorizing;
  - capture the exact command, input, environment, or user flow that triggers it;
  - distinguish infrastructure failure from source-code failure.
- Prefer executable truth over prose:
  - configs, lockfiles, schema, running app, computed styles, test output, CI logs, and actual CLI behavior outrank documentation or memory.
- For parity or visual work:
  - inspect measured design tokens, constants, screenshots, or reference captures;
  - probe the reference implementation when available;
  - do not guess colors, spacing, typography, breakpoints, or interactive behavior.
- Flag high-risk areas early:
  - authentication;
  - sessions and tokens;
  - payments, balances, or money movement;
  - destructive data operations;
  - state machines;
  - public APIs;
  - database migrations;
  - permissions and role changes;
  - secrets or credential handling.

### Exit criteria

The problem is understood well enough to plan when:

- the affected surface and governing contract are identified;
- the relevant files and tests have been read in full;
- explicit and implicit requirements are captured;
- ambiguities and risks are listed;
- any reported failure has been reproduced or explicitly marked as not yet reproducible.

---

## 2. PLAN

### Purpose

Produce the smallest correct, verifiable path from the current state to the desired state.

### Required behavior

- Write a short, ordered plan before implementation.
- Prefer the smallest implementation path that satisfies the request without sacrificing correctness, security, safety, or maintainability.
- The plan should name, where practical:
  - files likely to be touched;
  - modules or functions to be added or changed;
  - tests to be added or updated;
  - documentation to be updated;
  - scripts to be persisted;
  - migrations or data backfills;
  - rollback or recovery considerations.
- For UI work, include:
  - the view, dialog, route, or component;
  - the states to cover: empty, loading, error, success, disabled, unauthorized;
  - required breakpoints or viewport classes;
  - design tokens or measured values being matched;
  - accessibility expectations;
  - tests or screenshots that pin the behavior.
- For API/schema work, include:
  - backward compatibility implications;
  - migration order;
  - validation changes;
  - consumer impact;
  - rollback path if relevant.
- For debugging, include:
  - the reproduction case;
  - the suspected root cause;
  - the regression test that will be added;
  - how the original failure will be re-verified.
- For refactoring, include:
  - characterization tests or the plan to add them;
  - behavioral invariants that must remain unchanged;
  - incremental steps.
- State the verification strategy:
  - which commands will be run;
  - which tests prove the change;
  - which manual or browser checks are required;
  - what evidence will be captured.
- Confirm scope before implementation when:
  - the request is materially ambiguous;
  - the change affects auth, sessions, money, permissions, destructive data operations, public contracts, or state machines;
  - the change requires a breaking change or irreversible migration;
  - the project or user requires explicit approval.
- If no material ambiguity remains, proceed with clearly stated assumptions instead of asking unnecessary questions.

### Exit criteria

The plan is ready when:

- it satisfies the acceptance criteria;
- it identifies the required tests and evidence;
- it names high-risk effects;
- it can be executed in small, individually verifiable steps;
- any required scope confirmation has been obtained or the assumptions are explicitly recorded.

---

## 3. VALIDATE

### Purpose

Confirm that the plan is compatible with reality before writing code.

### Required behavior

- Validate assumptions against executable truth:
  - package manager and dependency versions;
  - lockfile state;
  - config files;
  - environment variables;
  - database schema;
  - running application behavior;
  - computed styles or rendered markup for UI work;
  - existing utilities and shared seams.
- Check whether existing utilities already solve part of the problem.
- Avoid duplicating logic that belongs in a shared domain or utility seam.
- Confirm that required tools, binaries, scripts, and test runners are available.
- Confirm the project’s verification gate:
  - lint;
  - format check, if separate;
  - type checking;
  - unit tests;
  - integration tests;
  - build;
  - smoke tests;
  - e2e tests;
  - visual or screenshot comparison, if applicable.
- If no test infrastructure exists, state that explicitly and propose the minimal runnable setup.
- For UI parity work, validate the measured tokens, screenshots, or reference behavior before implementation.
- For database work, validate that migrations, seeds, enums, constraints, and indexes are represented in executable schema sources rather than only prose.
- For external integrations, validate:
  - authentication mechanism;
  - expected payload shape;
  - error behavior;
  - timeout and retry expectations;
  - whether sandbox/mock mode is available.

### Exit criteria

Implementation may begin when:

- the plan matches the acceptance criteria;
- critical assumptions are validated or explicitly flagged;
- the required tools and tests are available or their absence is documented;
- the verification path is known;
- no unresolved high-risk ambiguity remains.

---

## 4. IMPLEMENT

### Purpose

Make the smallest safe, testable change that satisfies the validated plan.

### Required behavior

- Implement incrementally.
- Prefer small, pure, typed, testable units.
- Place reusable domain rules in the project’s shared seams instead of inlining them into UI, routes, or scripts.
- UI should consume shared logic, not own business rules.
- Keep changes surgical:
  - preserve unrelated content;
  - avoid speculative scaffolding;
  - avoid unrequested configuration;
  - avoid premature abstraction;
  - avoid repo-wide reformatting unless explicitly required.
- Use one logical change per commit where version control is part of the workflow.
- Update tests in the same change as the behavior they cover.
- Update documentation in the same change when behavior, setup steps, contracts, counts, screenshots, or workflows change.
- Persist reusable scripts instead of relying on long inline commands when the operation is repeatable or project-specific.
- Keep the codebase green as you go:
  - lint;
  - type checking;
  formatting;
  - relevant tests.
- Never weaken a guardrail to make a gate pass:
  - do not disable lint rules to avoid fixing issues;
  - do not loosen type strictness to hide errors;
  - do not skip tests or hooks;
  - do not suppress warnings unless that is the documented correct behavior.
- Handle failure explicitly:
  - invalid input;
  - missing fields;
  - empty collections;
  - network failure;
  - unauthorized access;
  - concurrent mutation;
  - partial success;
  - timeout;
  - retry idempotency where applicable.
- For UI:
  - use existing component-library primitives where available;
  - implement loading, empty, error, and success states;
  - support required breakpoints;
  - preserve keyboard operability and visible focus;
  - use theme variables instead of hardcoded colors where theming exists;
  - use controlled form handling where applicable.
- For data and security:
  - validate external input;
  - use parameterized queries;
  - avoid secret logging;
  - apply least privilege;
  - preserve transactional boundaries;
  - avoid unsafe deserialization;
  - prevent path traversal and injection vectors.

### Exit criteria

Implementation is ready for verification when:

- the change matches the plan or deviations are explicitly recorded;
- the code is typed, lint-clean, and formatted according to project conventions;
- relevant tests are added or updated;
- no debug output, placeholders, secrets, or scratch artifacts remain;
- the diff is focused and does not include unrelated changes.

---

## 5. VERIFY

### Purpose

Prove that the change works using executed evidence, not assumption.

### Required behavior

Run the project’s full verification gate in the correct order.

A generalized gate chain is:

```text
dependency sanity
→ lint
→ format check or formatter
→ typecheck
→ unit/integration tests
→ build
→ smoke tests
→ e2e tests
→ visual/accessibility/manual browser checks
```

If the project provides a chained gate script, use it. If not, use the project’s equivalent commands.

### Verification rules

- Never state that something “works,” “passes,” or “is fixed” unless it was executed and observed.
- If verification cannot be run in the current environment, say so and provide the exact commands the user should run.
- A green build alone is not sufficient evidence that an interactive page works.
- New behavior requires a new test.
- A bug fix requires a regression test that fails before the fix and passes after it.
- Do not delete, skip, or weaken tests to make the gate pass.
- If a gate fails, fix the underlying issue or report the failure explicitly.

### Domain-specific verification

For UI changes:

- drive the real application in a browser or browser automation tool;
- verify desktop and mobile viewports when responsiveness matters;
- verify known regression areas, such as drawers, modals, navigation, forms, and focus management;
- verify empty, loading, error, success, and disabled states;
- compare against design tokens, reference screenshots, or visual captures where parity is required;
- check accessibility basics:
  - labels;
  - focus visibility;
  - contrast;
  - keyboard access;
  - semantic structure;
  - disabled-state behavior.

For API or backend changes:

- verify success responses;
- verify validation failures;
- verify authentication and authorization failures;
- verify malformed payloads;
- verify idempotency or retry behavior where relevant;
- verify transactional effects and database state, not only exit codes.

For database or migration work:

- verify migration status;
- verify table/column/index/constraint changes;
- verify seed or backfill counts;
- verify rollback assumptions if rollback is in scope;
- query actual database state instead of relying only on command exit codes.

For external integrations:

- verify against mocks, fixtures, or recorded responses where live calls are unsafe;
- verify live behavior only when the environment supports it and side effects are acceptable;
- check timeout, retry, and error-handling behavior.

For performance-sensitive changes:

- check for N+1 query patterns;
- check unbounded loops or collections;
- verify pagination or limits where external data may grow;
- avoid declaring performance improvements without measured evidence.

For security-sensitive changes:

- verify input validation;
- verify authorization boundaries;
- verify secret handling;
- verify output encoding/sanitization;
- verify that logs do not contain secrets, tokens, credentials, or full sensitive payloads.

### Evidence requirements

Capture, where applicable:

- command output;
- test counts;
- failing-before/passing-after regression evidence;
- screenshots;
- browser console/network evidence;
- migration records;
- smoke-test results;
- e2e results;
- manual verification notes.

Any numeric claim in documentation, such as test counts, endpoint counts, feature counts, or screenshot references, must match the current executed tree. Do not carry old counts forward from memory.

### Exit criteria

Verification is complete when:

- the full gate passes, or failures are explicitly reported;
- the original failure is confirmed fixed when debugging;
- new behavior is covered by tests;
- UI changes are browser-verified where relevant;
- evidence exists for all non-trivial claims;
- unverified items are labeled clearly.

---

## 6. DELIVER

### Purpose

Hand off the change honestly, completely, and maintainably.

### Required behavior

- Commit logical, atomic changes.
- Use the project’s commit convention if one exists, such as Conventional Commits.
- Commit messages should explain why the change exists, not only what changed.
- Do not bundle unrelated changes.
- Update all touched documentation in the same delivery:
  - README;
  - worklog;
  - plan files;
  - API docs;
  - changelog;
  - runbooks;
  - screenshot references;
  - architecture notes;
  - test documentation.
- Remove stale documentation that conflicts with the new behavior.
- Ensure documentation claims are lockstep with the code:
  - no remembered counts;
  - no stale setup steps;
  - no outdated architecture claims;
  - no orphaned screenshots or references.
- Remove all scratch artifacts:
  - temporary files;
  - debug logging;
  - commented-out code;
  - placeholder values;
  - fake keys;
  - unused experiments.
- Push or open the change using the project’s approved mechanism:
  - normal Git remote;
  - SSH wrapper;
  - pull request workflow;
  - internal review system;
  - CI pipeline.
- If CI is required, confirm the relevant pipeline state or provide the exact command/URL to inspect it.

### Handoff report

Every non-trivial delivery should state:

- what changed;
- why it changed;
- what was tested;
- what was verified by execution;
- what was reasoned but not executed;
- what was assumed;
- what remains unverifiable;
- what deferred debt or follow-up work remains;
- any breaking changes or migration steps;
- exact commands to run, if the user needs to verify locally.

Use confidence labels:

- **Verified**: executed and observed directly.
- **Reasoned**: inferred from code or design, but not executed.
- **Assumed**: based on an explicit assumption.
- **Unverifiable**: cannot be verified in the current environment.

### Exit criteria

Delivery is complete when:

- the change is committed or presented in the correct output location;
- documentation is updated;
- no scratch material remains;
- evidence is attached or summarized;
- remaining risk is disclosed honestly;
- the next maintainer can continue without reconstructing context.

# Cross-cutting safeguards

These apply across all six phases:

- **Executable truth over prose**: configs, lockfiles, schemas, running apps, tests, and CLI output outrank memory or documentation.
- **Full-file awareness**: never modify a file based on a partial view.
- **Smallest safe diff**: avoid unrelated refactors, speculative abstraction, and broad reformatting.
- **No weakened guardrails**: never disable lint, loosen types, skip tests, or suppress errors merely to pass a gate.
- **Evidence-based claims**: distinguish executed evidence from reasoning and assumption.
- **Security by default**: validate untrusted input, protect secrets, use parameterized queries, apply least privilege, and sanitize output for context.
- **Documentation lockstep**: docs touched by the change are updated in the same change; counts and claims must match the current tree.
- **Honest handoff**: state what was verified, what was not, what remains broken, and what was intentionally deferred.

---

# Generalized gate definition

Use the project’s actual gate. If the project has a chained script, prefer it.

Typical generalized gate:

```text
lint
→ typecheck
→ unit/integration tests
→ build
→ smoke tests
→ e2e tests
```

Additional requirements:

- If lint autofix is used, run the formatter afterward when the project separates lint and formatting.
- If e2e tests boot a server, ensure they run against the intended build and not a stale local process.
- If CI mode is available and appropriate, use it to force a clean environment.
- If visual parity matters, include screenshot or token comparison.
- If accessibility matters, include keyboard and semantic checks.
- If database migrations matter, verify actual migration state, not only exit codes.

---

# Project-specific adaptation map

The unified workflow should be instantiated using the project’s own conventions:

| General concept | Example project-specific form |
|---|---|
| Plans live in a known location | `docs/plans/` |
| Shared pure/domain seams | `src/lib/` |
| Full verification gate | `bun run gate`, `npm test`, `pnpm verify`, etc. |
| Test counts in docs | Must match current executed suite |
| Visual evidence | `docs/screenshots/` or equivalent captures |
| Worklog | `worklog.md` or issue/PR notes |
| Push mechanism | normal Git, SSH wrapper, PR pipeline, or internal tool |
| Reference app probing | project extraction/probe scripts |
| UI parity evidence | measured design tokens, constants, screenshots, reference captures |
