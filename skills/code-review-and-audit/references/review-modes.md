# Review Modes Reference

> Defines the scope, phase coverage, failure threshold, and intended use for each audit mode.

---

## Mode Comparison Table

| Mode | Phases | Failure Threshold | Typical Duration | Intended Use |
|------|--------|-------------------|-----------------|------------- |
| **quick** | 1 | Critical | < 30s | Pre-commit, fast CI feedback |
| **standard** | 1 + 2 + 3 | High | < 2 min | PR review, pre-merge gate |
| **deep** | All 5 | Medium | < 5 min | Release audit, security review |
| **security-only** | 2 | Critical | < 1 min | Focused pen-test prep, compliance |
| **quality-only** | 1 + 3 + 4 | High | < 2 min | Code quality focus, tech debt review |

---

## Phase Coverage by Mode

| Phase | quick | standard | deep | security-only | quality-only |
|-------|-------|----------|------|---------------|-------------|
| 1. Static Analysis | ✅ | ✅ | ✅ | ❌ | ✅ |
| 2. Security Scan | ❌ | ✅ | ✅ | ✅ | ❌ |
| 3. Code Quality | ❌ | ✅ | ✅ | ❌ | ✅ |
| 4. Test Coverage | ❌ | ❌ | ✅ | ❌ | ✅ |
| 5. Performance | ❌ | ❌ | ✅ (--url) | ❌ | ❌ |
| 6. Expert Review | ❌ | ❌ | ✅ | ❌ | ❌ |

---

## Quick Mode

**Trigger:** Pre-commit hook, fast CI pipeline, iterative development feedback.

**Scope:** Phase 1 only (lint + type checking).

**Failure threshold:** Critical — exit code 1 only if lint fails or TypeScript errors.

**Example:**
```bash
python audit_runner.py . --mode quick
```

**What it catches:**
- Syntax errors
- TypeScript compilation errors
- ESLint violations (if configured)
- Missing imports, unused variables

---

## Standard Mode

**Trigger:** PR review, pre-merge gate, code review before feature completion.

**Scope:** Phases 1 + 2 + 3.

**Failure threshold:** High — exit code 1 if any High or Critical findings.

**Example:**
```bash
python audit_runner.py . --mode standard
```

**What it catches:**
- Everything in quick mode
- OWASP Top 10 vulnerabilities (A01–A10)
- Hardcoded secrets, injection risks
- Code quality issues (naming, DRY, error handling)
- Missing test coverage indicators

---

## Deep Mode

**Trigger:** Release audits, security compliance, architecture reviews, post-incident analysis.

**Scope:** All 5 phases + Phase 6 (expert review).

**Failure threshold:** Medium — exit code 1 if any Medium or higher severity findings.

**Example:**
```bash
python audit_runner.py . --mode deep --url https://staging.example.com
```

**What it catches:**
- Everything in standard mode
- Test coverage gaps
- Performance regressions (Core Web Vitals)
- Bundle size issues
- Lighthouse accessibility / SEO scores

---

## Security-Only Mode

**Trigger:** Pre-penetration test, compliance audit (SOC2, ISO 27001), incident response.

**Scope:** Phase 2 only (full security scan).

**Failure threshold:** Critical — exit code 1 only for Critical severity.

**Example:**
```bash
python audit_runner.py . --mode security-only
```

**What it catches:**
- Supply chain vulnerabilities (OWASP A03)
- Hardcoded credentials and secrets (OWASP A04)
- Injection vulnerabilities (OWASP A05)
- Security misconfiguration (OWASP A02)
- Fail-open error handling (OWASP A10)

---

## Quality-Only Mode

**Trigger:** Tech debt review, code maintainability audit, team retrospectives.

**Scope:** Phases 1 + 3 + 4.

**Failure threshold:** High — exit code 1 if any High or Critical findings.

**Example:**
```bash
python audit_runner.py . --mode quality-only
```

**What it catches:**
- Everything in quick mode
- Naming convention violations
- Deep nesting and anti-patterns
- Missing test files
- Missing documentation (README, .gitignore)

---

## Choosing the Right Mode

```
What are you doing?
│
├─ Pre-commit / fast feedback
│   └─ → quick
│
├─ Pull request / pre-merge gate
│   └─ → standard
│
├─ Security audit / compliance check
│   ├─ Full scope
│   │   └─ → deep
│   └─ Focused only
│       └─ → security-only
│
└─ Tech debt / code quality review
    └─ → quality-only
```
