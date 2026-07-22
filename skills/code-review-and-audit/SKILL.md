---
name: code-review-and-audit
description: "Unified code review and security audit orchestration skill. Coordinates static analysis, security scanning, code quality checks, test coverage, performance profiling, and expert review into a single tiered pipeline. Use when reviewing code, preparing for release, conducting security audits, or running pre-merge gates. Triggers on: review, audit, code review, security scan, quality gate, pre-merge, checklist, lint, vulnerability."
version: 2.0.0
skills:
  - verification-and-review-protocol
  - code-quality-standards
  - code-review-checklist
  - lint-and-validate
  - vulnerability-scanner
  - clean-code
  - testing-patterns
  - performance-profiling
  - systematic-debugging
trigger: code-review-and-audit
runtime: agent
subservices:
  full-review:
    description: Run all 5 phases (standard mode) against a project
    trigger: "code-review-and-audit:full"
    process:
      - Identify project path
      - Run audit_runner.py --mode standard
      - Parse JSON output, aggregate findings by severity
      - Generate markdown report to .audit-report.md
      - Present summary to user with severity breakdown
      - Ask user whether to proceed with fixes
  quick-review:
    description: Fast pre-commit lint check (Phase 1 only)
    trigger: "code-review-and-audit:quick"
    process:
      - Identify project path
      - Run audit_runner.py --mode quick
      - Report only Critical findings
      - Exit code 1 if Critical found
  security-only:
    description: OWASP-focused security scan only (Phase 2 only)
    trigger: "code-review-and-audit:security-only"
    process:
      - Identify project path
      - Run audit_runner.py --mode security-only
      - Present OWASP A01–A10 findings by category
      - Report supply chain, secrets, injection, config findings
  quality-only:
    description: Code quality and test coverage (Phases 1 + 3 + 4)
    trigger: "code-review-and-audit:quality-only"
    process:
      - Identify project path
      - Run audit_runner.py --mode quality-only
      - Present findings across correctness, error handling, naming, type safety, testing
  deep-review:
    description: Comprehensive release audit (all 5 phases + expert review)
    trigger: "code-review-and-audit:deep"
    process:
      - Identify project path and staging URL
      - Run audit_runner.py --mode deep --url <staging_url>
      - Present findings across all severity tiers
      - Dispatch code-reviewer subagent for expert human review (Phase 6)
      - Generate comprehensive markdown report
  report:
    description: Generate audit report from prior run results
    trigger: "code-review-and-audit:report"
    process:
      - Read prior JSON output or regenerate with --json-only
      - Populate audit_report.md template
      - Write report to <project>/.audit-report.md
      - Present structured summary
---

# Code Review & Audit Orchestration Skill

> **Purpose:** Single entry point for all code review and audit tasks. Orchestrates 7 constituent skills and 13 scripts into a unified, tiered pipeline with structured reporting.

---

## Purpose & Scope

This skill is an **orchestration layer** that coordinates multiple specialist skills into one coherent review pipeline. It does NOT replace those skills — it sequences them, aggregates their output, and presents a unified finding report.

**What it is:**
- The "one command" for any code review or audit task
- A tiered system (5 modes) adapting to urgency and depth
- A structured report format by severity with action guidance
- A Python orchestration pipeline with exit codes for CI/CD

**What it is NOT:**
- A replacement for reading the constituent skills (verification-and-review-protocol, vulnerability-scanner, etc.)
- A single-pass scanner — it runs multiple phases in priority order
- A substitute for human expert review in deep mode

---

## Core Principle

**Tiered rigor for tiered urgency.** The depth of review must match the stakes of the decision.

## 🛡️ Native CLI Fallback Protocol (CRITICAL)

The Python orchestration scripts (`audit_runner.py`, `checklist_runner.py`) exist in this skill's `scripts/` directory. However, if an agent runs this skill in an environment where these scripts are NOT available, the agent MUST NOT hallucinate their execution. Fall back to native ecosystem commands:

| Phase | Python Script | Native CLI Fallback |
|-------|---------------|---------------------|
| Phase 1 (Lint/Types) | `lint_runner.py` | `npm run lint && npx tsc --noEmit` (Node.js) or `ruff check && mypy` (Python) |
| Phase 2 (Security) | `security_scan.py` | `npm audit` + `grep -rE '(API_KEY|SECRET|PASSWORD)\s*=' .` |
| Phase 3 (Quality) | `checklist_runner.py` | Agent performs manual review against the 12-category Tactical Matrix (see Phase 3 below) |
| Phase 4 (Tests) | `test_runner.py` | `npx vitest run` / `npm test` / `pytest` |
| Phase 5 (Performance) | `lighthouse_audit.py` | `npx lighthouse <url>` (requires URL) |
| Phase 6 (Expert Review) | Subagent dispatch | Use `verification-and-review-protocol` skill directly |

**Detection:** Before running any script, check if it exists:
```bash
if [ -f "scripts/audit_runner.py" ]; then
  # Use Python orchestration
else
  # Fall back to native CLI commands
fi
```

**Never:** Run a script that doesn't exist and claim it succeeded. This is a verification gate violation per `verification-and-review-protocol`.

| Decision | Stakes | Mode | Time |
|----------|--------|------|------|
| Can I commit this? | Low | `quick` | < 30s |
| Can I merge this? | Medium | `standard` | < 2 min |
| Can I release this? | High | `deep` | < 5 min |
| Is our app secure? | Critical | `security-only` | < 1 min |
| Is our code maintainable? | Medium | `quality-only` | < 2 min |

---

## Orchestration Architecture

```
User Request
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    code-review-and-audit SKILL                       │
│                                                                      │
│  Subservice Dispatch                                                 │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌────────────┐ │
│  │  full-review │ │ quick-review │ │security-only │ │quality-only│ │
│  └──────┬───────┘ └──────┬───────┘ └──────┬───────┘ └─────┬──────┘ │
│         │                │                │               │         │
│         └────────────────┴────────────────┴───────────────┘         │
│                              │                                       │
│                     Mode Selection                                   │
│                              │                                       │
│  ┌───────────────────────────┼───────────────────────────────────┐  │
│  │         audit_runner.py (Master Orchestrator)                  │  │
│  │                                                              │  │
│  │  Phase 1 ──► Phase 2 ──► Phase 3 ──► Phase 4 ──► Phase 5  │  │
│  │     │          │           │           │            │       │  │
│  │  lint-and-  vulnerability- code-review-  testing-  performance-  │  │
│  │  validate     scanner     checklist    patterns   profiling   │  │
│  │     │           │            │            │           │       │  │
│  │  lint_runner  security_   checklist_  test_runner  lighthouse  │  │
│  │     .py       scan.py     runner.py     .py       _audit.py   │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                              │                                       │
│                    JSON Report + Markdown Report                     │
│                              │                                       │
│  ┌───────────────────────────┴───────────────────────────────────┐  │
│  │                  Phase 6: Expert Review (deep mode only)        │  │
│  │                  code-review subagent dispatched                │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    .audit-report.md
                    + stdout summary
                    + exit_code (0=pass, 1=fail)
```

---

## Review Modes

> See `references/review-modes.md` for full comparison table.

| Mode | Phases | Failure Threshold | Duration | Use Case |
|------|--------|-------------------|----------|----------|
| **quick** | 1 | Critical | < 30s | Pre-commit |
| **standard** | 1+2+3 | High | < 2 min | PR / pre-merge |
| **deep** | All 5 | Medium | < 5 min | Release / security audit |
| **security-only** | 2 | Critical | < 1 min | Pen-test prep / compliance |
| **quality-only** | 1+3+4 | High | < 2 min | Tech debt review |

**Default mode:** `standard`

### How Mode Selection Works

```
Intent: "review code" or "audit" or no mode specified
    │
    ▼
Is this a security-focused task?
├─ YES: "security-only" or "deep" → ask: "Focus only on security?"
│   ├─ YES → security-only
│   └─ NO → deep (full review)
│
Is this a quick pre-commit check?
├─ YES → quick
│
Is this a release or compliance review?
├─ YES → deep
│
Default → standard
```

### Running the Audit

```bash
# Standard mode (default)
python scripts/code-review-and-audit/scripts/audit_runner.py <project_path>

# Specific mode
python scripts/code-review-and-audit/scripts/audit_runner.py . --mode quick
python scripts/code-review-and-audit/scripts/audit_runner.py . --mode security-only
python scripts/code-review-and-audit/scripts/audit_runner.py . --mode deep --url https://staging.example.com

# JSON-only (for CI/CD pipelines)
python scripts/code-review-and-audit/scripts/audit_runner.py . --mode standard --json-only

# Don't write markdown report
python scripts/code-review-and-audit/scripts/audit_runner.py . --no-report
```

---

## Orchestration Pipeline

### Phase 1 — Static Analysis (`lint-and-validate`)

**Subskill:** `lint-and-validate`

**Script:** `lint_runner.py`

**What it runs:**
- Node.js: `npm run lint` (or ESLint) + `tsc --noEmit`
- Python: `ruff check` + `mypy`
- Auto-detected from project root

**What it catches:**
- Syntax errors
- TypeScript type mismatches
- ESLint/Prettier violations
- Import resolution errors

**SKILL.md reference:** `lint-and-validate` skill

---

### Phase 2 — Security Scan (`vulnerability-scanner`)

**Subskill:** `vulnerability-scanner`

**Script:** `security_scan.py`

**What it runs:**
- `npm audit` (if Node.js project)
- Lock file presence check (supply chain)
- Secret pattern scan (API keys, tokens, credentials)
- Dangerous code pattern scan (eval, innerHTML, SQL concat)
- Security configuration scan (debug mode, CORS, SSL verify)

**OWASP Coverage:**
- A01: Broken Access Control (IDOR patterns, auth checks)
- A02: Security Misconfiguration (defaults, headers)
- A03: Software Supply Chain (lock files, npm audit)
- A04: Cryptographic Failures (hardcoded secrets)
- A05: Injection (SQL, XSS, RCE patterns)
- A06: Insecure Design (architecture flaws)
- A07: Authentication Failures (session handling)
- A08: Integrity Failures (unsigned updates)
- A09: Logging & Alerting (missing error handling)
- A10: Exceptional Conditions (fail-open error handlers)

**SKILL.md reference:** `vulnerability-scanner` skill

---

### Phase 3 — Code Quality (`code-quality-standards` + `code-review-checklist` + `clean-code`)

**Subskills:** `code-quality-standards`, `code-review-checklist`, `clean-code`

**Script:** `checklist_runner.py`

**Relationship:** `code-quality-standards` is the comprehensive Six-Axis quality constitution (Correctness, Readability, Architecture, Security, Performance, Aesthetic/UX Rigor). `code-review-checklist` is a lightweight quick-reference for the 12 tactical categories below. This Phase uses both: the checklist for automated scanning, the standards for holistic review.

**What it evaluates (12 tactical categories):**

| # | Category | What It Checks |
|---|----------|---------------|
| 1 | **Correctness** | Unsafe array access, null returns, parseInt without radix |
| 2 | **Security** | eval, XSS, injection, hardcoded credentials |
| 3 | **Performance** | for...in on arrays, N+1 patterns, large static imports |
| 4 | **Code Quality** | Long functions (>500 chars), large classes, unclear comments |
| 5 | **Testing** | Missing test files, skipped tests |
| 6 | **Documentation** | Missing README, missing .gitignore |
| 7 | **Error Handling** | Bare except+pass, empty catch blocks, log-only catch |
| 8 | **Naming** | Single-letter variables, PascalCase const variables |
| 9 | **Type Safety** | `: any` type, @ts-ignore, @ts-nocheck, non-null assertion abuse |
| 10 | **React/UI** | Object setState, missing useEffect deps, missing loading states |
| 11 | **LLM/AI Patterns** | Untyped AI generate calls, missing schema validation |
| 12 | **Anti-Patterns** | Magic numbers, deep nesting, God functions |

**SKILL.md references:** `code-quality-standards` (constitution), `code-review-checklist` (quick-reference), `clean-code` (simplification patterns)

---

### Phase 4 — Test Coverage (`testing-patterns`)

**Subskill:** `testing-patterns`

**Script:** `test_runner.py` (if found in agent skills)

**What it checks:**
- Test runner execution (Jest, Vitest, pytest)
- Pass/fail count and rate
- Failed test names and error messages

**Note:** Skipped if `test_runner.py` is not found in any skills directory. This is informational only — test failures do not fail the audit in `standard` mode unless explicitly configured.

**SKILL.md reference:** `testing-patterns` skill

---

### Phase 5 — Performance (`performance-profiling`)

**Subskill:** `performance-profiling`

**Script:** `lighthouse_audit.py` (requires `--url` flag)

**What it checks (Core Web Vitals):**
- LCP (Largest Contentful Paint) < 2.5s
- INP (Interaction to Next Paint) < 200ms
- CLS (Cumulative Layout Shift) < 0.1
- Lighthouse scores: Performance, Accessibility, Best Practices, SEO

**Activation:** Requires `--url <staging_url>` flag. Only runs in `deep` mode.

**SKILL.md reference:** `performance-profiling` skill

---

### Phase 6 — Expert Review (deep mode only)

**Subskill:** `verification-and-review-protocol`

**Trigger:** Automatic in `deep` mode after automated phases complete.

**Standards Reference:** Expert review applies the Six-Axis criteria from `code-quality-standards` (including Axis 6: Aesthetic & UX Rigor for frontend deliverables).

**Process:**

1. Get git SHAs: `BASE_SHA=$(git rev-parse HEAD~1)` and `HEAD_SHA=$(git rev-parse HEAD)`
2. Dispatch `code-reviewer` subagent via `Task` tool with:
   - `WHAT_WAS_IMPLEMENTED`: Summary of changes
   - `PLAN_OR_REQUIREMENTS`: What the code should do
   - `BASE_SHA`, `HEAD_SHA`: Diff range
   - `DESCRIPTION`: Context for the review
3. Act on feedback:
   - **Critical:** Fix immediately before proceeding
   - **Important:** Fix before merge
   - **Minor:** Note for later, document in PR comments
4. Mark findings as `addressed` or `acknowledged_and_deferred`

**SKILL.md reference:** `verification-and-review-protocol` skill (section: Requesting Review Protocol)

---

## Report Format

### Severity Sections

Each audit report contains exactly these sections, in order:

```
## 🔴 Critical Findings (N items)
## 🟠 High Findings (N items)
## 🟡 Medium Findings (N items)
## 🟢 Low Findings (N items)
## ⚪ Info (N items)
## ✅ Passed Checks
```

### Finding Structure

Every finding includes:

| Field | Description |
|-------|-------------|
| **severity** | Critical / High / Medium / Low / Info |
| **category** | security, correctness, performance, etc. |
| **type** | Specific finding type (e.g., "SQL injection") |
| **message** | Plain-language description of the issue |
| **file** | Relative path from project root |
| **line** | Line number (if applicable) |
| **snippet** | First 100 chars of the offending line |
| **phase** | Which phase detected this |
| **remediation** | One-sentence fix guidance |

### JSON Output Structure

```json
{
  "skill": "code-review-and-audit",
  "audit_runner_version": "1.0.0",
  "project": "/path/to/project",
  "mode": "standard",
  "timestamp": "2026-04-13T10:00:00Z",
  "phases": [
    {
      "phase": "phase_1_static_analysis",
      "name": "Static Analysis (Lint & Types)",
      "status": "passed|failed|critical|error|skipped",
      "findings": [...],
      "summary": {...}
    }
  ],
  "total_findings": 5,
  "by_severity": {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 2,
    "info": 0
  },
  "failed_phases": [],
  "overall_status": "PASSED|FAILED (HIGH)",
  "exit_code": 0
}
```

**Exit codes:**
- `0` = All checks passed for the mode's threshold
- `1` = Findings at or above the failure threshold

---

## Finding Classification Rules

> See `references/severity-matrix.md` for full matrix.

### Quick Decision Rules

```
Finding type?
│
├─ RCE, hardcoded credential, unauthenticated data exposure
│   └─ → CRITICAL
│
├─ SQL injection, XSS, eval(), empty catch block
│   ├─ If requires no special conditions
│   │   └─ → HIGH
│   └─ If requires user interaction or auth
│       └─ → MEDIUM
│
├─ Long function, magic numbers, single-letter vars
│   └─ → LOW
│
└─ Test file present, proper naming, clean structure
    └─ → Passed (no finding)
```

### Override Conditions

- **Internet-facing endpoint** → +1 tier (Medium → High)
- **Authentication-required** → -1 tier (High → Medium)
- **Internal tooling only** → -1 tier
- **Production environment** → +1 tier
- **EPSS > 0.5** (actively exploited) → CRITICAL regardless

---

## Script Output Handling

**MANDATORY protocol — every time a script runs:**

```
1. RUN the script
2. READ the full output
3. SUMMARIZE in this format:

## Script Results: [script_name.py]

### ❌ Errors Found (X items)
- [File:Line] Error description

### ⚠️ Warnings (Y items)
- [File:Line] Warning description

### ✅ Passed (Z items)
- Check 1 passed
- Check 2 passed

**Should I fix the X errors?**

4. WAIT for user confirmation before fixing
5. FIX the issues
6. RE-RUN the script to confirm
```

> 🔴 **VIOLATION:** Running script and ignoring output = FAILED task.
> 🔴 **VIOLATION:** Auto-fixing without asking = NOT ALLOWED.
> 🔴 **Rule:** Always READ → SUMMARIZE → ASK → then fix.

**Reference:** `clean-code` skill (Script Output Handling section)

---

## Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| Run in `quick` mode before release | Use `deep` mode for release audits |
| Skip Phase 2 if it takes time | Security findings are often the most critical |
| Ignore Info/Low severity | They indicate systemic patterns worth noting |
| Auto-fix without asking | Follow the Script Output Handling protocol |
| Skip Phase 6 in deep mode | Expert human review catches what tools miss |
| Merge with Critical findings | Stop, fix, re-audit, then merge |
| Use `any` to "fix" TypeScript errors | Address the root cause |

---

## Integration with Other Skills

### Skill Dependency Graph

```
code-review-and-audit (this skill)
    │
    ├──► lint-and-validate
    │        └──► lint_runner.py
    │        └──► type_coverage.py
    │
    ├──► vulnerability-scanner
    │        └──► security_scan.py
    │        └──► dependency_analyzer.py
    │
    ├──► code-quality-standards (the Constitution)
    │        └──► Six-Axis Review criteria
    │        └──► Anti-Generic Litmus Test (Axis 6)
    │
    ├──► code-review-checklist (quick-reference for Phase 3)
    │        └──► checklist_runner.py (this skill)
    │        └──► references/severity-matrix.md (this skill)
    │
    ├──► clean-code
    │        └──► Self-checks before any code change
    │
    ├──► testing-patterns
    │        └──► test_runner.py
    │        └──► playwright_runner.py
    │
    ├──► performance-profiling
    │        └──► lighthouse_audit.py
    │        └──► bundle_analyzer.py
    │
    ├──► systematic-debugging (when bugs found)
    │        └──► 4-phase RCA methodology
    │
    └──► verification-and-review-protocol (Phase 6, deep mode only)
             └──► code-reviewer subagent dispatch
             └──► Iron Law: No completion claims without verification
```

### Skill Loading Order

When activated, read skills in this order:

1. **This SKILL.md** — understand mode selection and pipeline
2. **`verification-and-review-protocol` SKILL.md** — Phase 6 protocol for subagent dispatch
3. **`code-quality-standards` SKILL.md** — Six-Axis review criteria (including Axis 6 for frontend)
4. **`vulnerability-scanner` SKILL.md** — Phase 2 OWASP details
5. **`code-review-checklist` SKILL.md** — Phase 3 tactical checklist reference
6. **`clean-code` SKILL.md** — Script Output Handling protocol
7. **`lint-and-validate` SKILL.md** — Phase 1 ecosystem details
8. **`testing-patterns` SKILL.md** — Phase 4 test pyramid
9. **`performance-profiling` SKILL.md** — Phase 5 Core Web Vitals

### Integration with GEMINI.md

Per `GEMINI.md` Final Checklist Protocol, this skill's scripts map to:

| Phase | Script | GEMINI.md Mapping |
|-------|--------|------------------|
| Phase 1 | `lint_runner.py` | `lint_runner.py` |
| Phase 2 | `security_scan.py` | `security_scan.py` |
| Phase 3 | `checklist_runner.py` | (not in GEMINI, new) |
| Phase 4 | `test_runner.py` | `test_runner.py` |
| Phase 5 | `lighthouse_audit.py` | `lighthouse_audit.py` |
| Phase 6 | Subagent dispatch | (human review step) |

**GEMINI.md integration note:** `checklist_runner.py` is a new script that supplements (not replaces) the existing `ux_audit.py`, `accessibility_checker.py`, and `seo_checker.py` scripts from the frontend-design skill.

---

## Success Criteria

Before completing any audit task, verify:

- [ ] Mode was correctly selected based on task intent
- [ ] All applicable phases were run (phases skipped had informational reasons)
- [ ] All findings were categorized by severity and category
- [ ] Report written to `.audit-report.md` in project root
- [ ] Findings above the mode's failure threshold were clearly flagged
- [ ] User was asked about fixing Critical/High findings before proceeding
- [ ] Phase 6 (expert review) was triggered in deep mode
- [ ] Exit code correctly reflects pass/fail state for the mode
- [ ] No findings were silently dropped or ignored
- [ ] JSON output is valid and parseable

---

## References

| File | Purpose |
|------|---------|
| `scripts/audit_runner.py` | Master orchestration script (Phase 1–5 runner) |
| `scripts/checklist_runner.py` | Automated 12-category code quality checker |
| `scripts/templates/audit_report.md` | Markdown report template |
| `references/review-modes.md` | Full mode comparison + decision tree |
| `references/severity-matrix.md` | Finding classification + SLAs |
| `code-quality-standards/SKILL.md` | Six-Axis quality constitution |
| `verification-and-review-protocol/SKILL.md` | Phase 6 subagent dispatch + Iron Law |
| `code-review-checklist/SKILL.md` | Phase 3 tactical checklist reference |
| `vulnerability-scanner/SKILL.md` | Phase 2 OWASP detail reference |
