---
name: e2e-testing-lessons
description: Condensed experience from 15-phase E2E testing initiative covering authentication, API contracts, tool selection, and hybrid testing methodology. Use when planning E2E tests, selecting testing tools, or debugging test failures.
---

# E2E Testing Lessons Learned

**Source:** LedgerSG E2E Testing Experience Report (2026-03-14)
**Summary:** Condensed experience from 15-phase E2E testing initiative covering authentication, API contracts, tool selection, and hybrid testing methodology.

---

## The Golden Rule: Hybrid API + UI

Pure UI testing fails with modern JWT auth (HttpOnly cookies, token expiry). The winning approach:

```
Authentication  → API (get JWT tokens)
Data Creation   → API (fast, reliable, no flake)
Assertions      → API + UI
Visual Proof    → UI screenshots
```

**Never depend on UI for authentication flow in automated tests.** HttpOnly cookies are invisible to browser automation tools and tokens stored in JS memory are lost on navigation.

---

## Tool Selection Guide

| Scenario | Tool | Why |
|----------|------|-----|
| Quick smoke test | `agent-browser` | Fast, no setup, CLI |
| Debug auth issue | `agent-browser` | Interactive, visual, snapshot |
| Regression suite | Playwright | Reliable, maintainable, parallel |
| Visual regression | Playwright | Screenshot comparison built-in |
| API testing | `aiohttp` / `requests` | Fast, no browser overhead |
| CI/CD integration | Playwright | Industry standard |
| Complex hybrid workflow | Custom Python script | Flexible, optimal control |

### agent-browser — When to Use

- ✅ Quick manual verification after deploy
- ✅ Debugging auth flows interactively (`--headed`)
- ✅ Ad-hoc screenshot capture
- ✅ Smoke testing
- ❌ Complex multi-step E2E suites
- ❌ Automated regression testing
- ❌ CI/CD pipelines

### Playwright — When to Use

- ✅ Comprehensive E2E test suites
- ✅ Visual regression testing
- ✅ Cross-browser testing
- ✅ Parallel execution
- ❌ Quick one-off checks (overkill)

---

## Session Persistence Problem

### The Problem

Modern apps use a 3-tier auth architecture that breaks automation:

```
Tier 1: Access Token  → JS memory, 15min TTL, lost on navigation
Tier 2: Refresh Token → HttpOnly cookie, invisible to automation
Tier 3: Backend       → Returns 401, frontend redirects to login
```

### The Solution

**Option A: API-Only Auth (Recommended)**
```python
tokens = await api_login()  # Get tokens via API
headers = {"Authorization": f"Bearer {tokens['access']}"}
# All data operations via API with headers
```

**Option B: Playwright Storage State**
```python
await context.storage_state(path="auth.json")  # Save after login
context = await browser.new_context(storage_state="auth.json")  # Reuse
```

**Option C: Test-Specific Auth Endpoint**
- Backend provides `/api/v1/auth/test-login/` that returns tokens without HttpOnly cookie

---

## API Contract Mismatches — Silent Killers

### What Happened
Backend returned an array, frontend expected `{results: [], count: N}`. Entire feature broken silently — `undefined.map()` crash.

### Prevention

1. **Always validate response schemas** in both frontend and backend tests
2. **Use OpenAPI/Swagger** as single source of truth
3. **Test all list endpoints** return consistent paginated format:
   ```json
   {"results": [...], "count": N}
   ```
4. **Contract tests** run on every PR to catch drift early

---

## Debugging Playbook

When something breaks, follow this order:

1. **Screenshot everything** — `page.screenshot(path=f"error-{timestamp}.png")`
2. **Log current URL** — `print(f"URL: {page.url}")` (catches redirect loops)
3. **Check console errors** — `page.on("console", lambda msg: print(msg.text))`
4. **Check network** — `page.on("response", lambda res: print(res.status, res.url))`
5. **Inspect DOM** — `html = await page.content()`

---

## Test Data Best Practices

- **Tests create their own data** — never depend on existing state
- **Use flexible matching** — don't assume specific account codes/IDs exist
- **Always cleanup** — wrap test logic in try/finally with API cleanup
- **Log data IDs** — print created resource IDs for debugging

---

## agent-browser Quick Reference

```bash
agent-browser open <url>                           # Navigate
agent-browser --session-name <name> open <url>     # Persistent session
agent-browser snapshot -i                          # Interactive elements with refs
agent-browser click @e2 / fill @e3 "text"          # Interact by ref
agent-browser find label "Email" fill "test@x.com" # Semantic locator
agent-browser screenshot --annotate /tmp/out.png   # Debug with labels
agent-browser eval "document.title"                # Run JS
agent-browser get title / url / text @ref          # Query page
agent-browser --headed open <url>                  # Debug mode
agent-browser close                                # Done
```

**Key gotcha:** `--session-name` does NOT persist HttpOnly cookies across page navigations. Use API auth instead.

---

## Anti-Patterns to Avoid

| ❌ Don't | ✅ Do Instead |
|---------|--------------|
| Pure UI auth flow | API login, store tokens |
| Assume test data exists | Create data in test setup |
| Test only via screenshots | Assert via API + UI |
| Ignore console errors | Log and check on every page |
| Use agent-browser for CI/CD | Use Playwright |
| Trust documentation counts | Validate against actual code |
| Leave test data behind | Always cleanup in teardown |

---

## Recommended Test Structure

```python
class TestWorkflow:
    async def setup(self):
        """API authentication"""
        self.tokens = await api_login()
        self.org_id = extract_org_id(self.tokens)

    async def test_something(self):
        # Arrange: Get state via API
        accounts = await api_get_accounts()
        
        # Act: Create/update via API
        result = await api_create_entry(data)
        
        # Assert: Verify via API
        assert result["id"] is not None
        
        # Visual: Screenshot via UI
        await page.goto(f"{BASE_URL}/ledger")
        await page.screenshot(path="ledger.png")

    async def teardown(self):
        """Always cleanup"""
        await api_cleanup_created_resources()
```

---

## Key Metrics Reference (LedgerSG)

For context on scale:
- 15 test phases, ~3 hours execution
- 25+ screenshots captured
- 1 critical API contract bug found and fixed (9 views affected)
- 116 additional tests discovered by fixing pytest collection
- Revenue verification: S$22,450 YTD confirmed via API
