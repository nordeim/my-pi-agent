# Severity Matrix Reference

> Defines how findings are classified, prioritized, and actioned based on severity and category.

---

## Severity Levels

| Level | Icon | CVSS Range | Response Time | Action |
|-------|------|------------|--------------|--------|
| **Critical** | 🔴 | 9.0 – 10.0 | Immediate | Stop. Fix before anything else. |
| **High** | 🟠 | 7.0 – 8.9 | Same day | Fix before merge/release. |
| **Medium** | 🟡 | 4.0 – 6.9 | This week | Schedule in sprint. |
| **Low** | 🟢 | 0.1 – 3.9 | This month | Nice to fix. Document if not. |
| **Info** | ⚪ | 0.0 | Backlog | Note only. No immediate action. |

---

## Finding Classification Rules

### Security Findings

| Finding Type | Default Severity | Override Condition | Rationale |
|-------------|-----------------|-------------------|-----------|
| Remote Code Execution (RCE) | **Critical** | — | Full system compromise |
| SQL / NoSQL Injection | **Critical** | If user-controlled input in query | Data breach risk |
| Hardcoded Credentials | **Critical** | Any secret in source | Immediate rotation required |
| SSRF | **High** | If internal network access | Lateral movement risk |
| XSS (stored) | **High** | Any stored XSS | Account takeover vector |
| XSS (reflected) | **Medium** | Requires user interaction | Phishing vector |
| Missing Auth Check | **High** | On sensitive endpoint | Unauthorized access |
| Insecure Deserialization | **High** | If user-controlled data | RCE vector |
| Missing Rate Limiting | **Medium** | On auth endpoints | Brute force enabler |
| Missing Security Headers | **Low** | — | Defense in depth only |
| Debug Mode Enabled | **Medium** | In production config | Information disclosure |

### Code Quality Findings

| Finding Type | Default Severity | Rationale |
|-------------|-----------------|-----------|
| Bare `eval()` | **Critical** | Code injection risk |
| `dangerouslySetInnerHTML` | **High** | XSS vector in React |
| Empty `catch {}` | **High** | Silent error swallowing |
| `: any` type | **High** | Type safety bypass |
| `@ts-ignore` | **Medium** | Suppressed type errors |
| Magic numbers | **Low** | Maintainability issue |
| Single-letter variable | **Low** | Readability issue |
| Long function (>500 chars) | **Medium** | SRP violation likely |

### Performance Findings

| Finding Type | Default Severity | Rationale |
|-------------|-----------------|-----------|
| N+1 query pattern | **High** | Database DoS risk |
| Uncached expensive computation | **Medium** | Unnecessary CPU |
| Static asset in initial bundle | **Medium** | LCP impact |
| No code splitting | **Medium** | TTI degradation |
| Lighthouse < 50 | **High** | Poor UX |
| Lighthouse 50-89 | **Medium** | Needs improvement |

---

## Priority Decision Tree

```
Finding discovered
│
├─ Is it actively exploited in the wild? (EPSS > 0.5)
│   ├─ YES → Elevate to CRITICAL regardless of CVSS
│   └─ NO → Continue
│
├─ Can it lead to data breach or RCE? (OWASP A01/A05/A08)
│   ├─ YES → CRITICAL or HIGH
│   └─ NO → Continue
│
├─ Does it require specific conditions? (auth, network, user interaction)
│   ├─ YES → MEDIUM
│   └─ NO → Check CVSS score
│
└─ CVSS Score
    ├─ 9.0+ → CRITICAL
    ├─ 7.0–8.9 → HIGH
    ├─ 4.0–6.9 → MEDIUM
    └─ < 4.0 → LOW / INFO
```

---

## Phase → Severity Impact

Findings accumulate across phases. A finding's severity determines which phases flag it:

| Mode | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Phase 5 |
|------|---------|---------|---------|---------|---------|
| **quick** | Fails on Critical | — | — | — | — |
| **standard** | Fails on High+ | Fails on High+ | Fails on High+ | — | — |
| **deep** | Fails on Medium+ | Fails on Medium+ | Fails on Medium+ | Fails on Medium+ | Fails on Medium+ |
| **security-only** | — | Fails on Critical | — | — | — |
| **quality-only** | Fails on High+ | — | Fails on High+ | Fails on High+ | — |

---

## Aggregation Rules

1. **Highest severity wins** — if the same issue is flagged by multiple phases, report the highest severity.

2. **Duplicate suppression** — the same finding in the same file should not appear twice. The first occurrence is reported; subsequent matches increment a count rather than duplicate.

3. **Contextual overrides** — severity can be elevated based on context:
   - **Internet-facing** → +1 severity tier
   - **Authentication-required** → -1 severity tier
   - **Internal tooling only** → -1 severity tier
   - **Production environment** → +1 severity tier

4. **False positive handling** — findings flagged as false positive by an expert reviewer are marked `suppressed: true` and excluded from counts.

---

## Response SLAs

| Severity | Acknowledge | First Fix Attempt | Verification |
|----------|------------|-------------------|-------------|
| **Critical** | 15 min | 2 hours | Same day |
| **High** | 4 hours | 24 hours | Next day |
| **Medium** | 24 hours | 1 week | This sprint |
| **Low** | 1 week | 1 month | Next sprint |
| **Info** | Backlog | Backlog | Backlog |
