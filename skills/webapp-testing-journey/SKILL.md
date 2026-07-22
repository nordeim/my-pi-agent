---
name: webapp-testing-journey
description: |
  Systematic web application testing methodology using OpenClaw browser tools, agent-browser CLI, and chrome-devtools-mcp. Use when testing web application user journeys, validating bug fixes, performing QA verification, or debugging frontend issues. 
  
  Covers URL journey testing, accessibility tree analysis, DOM inspection, network request debugging, performance tracing, visual regression, and comprehensive issue verification.
  
  Triggers on phrases like "test this application", "verify the fix", "check if it works", "test the user journey", "debug this issue".
---

# Webapp Testing Journey

Systematic methodology for testing web applications. Built from real-world QA testing of AI Academy (2026-03-24).

| Tools | Versions |
|-------|----------|
| agent-browser | v0.26.0 |
| chrome-devtools-mcp | v0.23.0 |
| @playwright/mcp | v0.0.70 |
| @playwright/cli | v0.1.9 |

**Last Validated:** April 26, 2026

## Core Philosophy

**Test assumptions, not claims.** Teams may claim fixes are deployed, but verification requires actual execution. Use browser automation to validate behavior, inspect DOM state, capture network activity, and record evidence.

## Tool Selection Matrix

| Testing Phase | Primary Tool | Reason |
|---------------|--------------|--------|
| Quick navigation | OpenClaw `browser` | Native integration, no exec |
| Annotated screenshots | `agent-browser screenshot --annotate` | Visual labels on elements |
| Video evidence | `agent-browser record` | WebM capture of interactions |
| Visual regression | `agent-browser diff` | Compare snapshots/screenshots |
| Network inspection | `chrome-devtools-mcp` | Full request/response details |
| Performance analysis | `chrome-devtools-mcp` | LCP, CLS, INP tracing |
| Lighthouse audits | `chrome-devtools-mcp` | A11y/SEO/Best Practices scores |
| Console debugging | Either (browser console or agent-browser) | Both work |
| Form filling | `agent-browser fill` or `chrome-devtools fill` | UID-based or ref-based |
| Mobile emulation | `agent-browser set device` or `chrome-devtools emulate` | Both support device profiles |
| Authenticated testing | `agent-browser auth` | Credential vault |
| **Profiler traces** | `agent-browser profiler` | Chrome DevTools CPU profiling |
| **Network HAR** | `agent-browser network har` | HTTP archive capture |
| **Console/errors** | `agent-browser console/errors` | JS error tracking |
| **Visual highlights** | `agent-browser highlight` | Element debugging |
| **AI testing** | `agent-browser chat` | Natural language test commands |
| AI agent integration | `@playwright/mcp` | MCP-native, custom code execution |

---

## Testing Workflow

```
1. PLAN: Define test cases with expected vs actual
2. EXECUTE: Navigate, interact, capture state
3. INSPECT: DOM, accessibility tree, console, network
4. VERIFY: Compare against expected behavior
5. EVIDENCE: Screenshots, video, diffs
6. REPORT: Document findings with proof
```

---

## Quick Reference: All Four Tools

### @playwright/mcp (Microsoft Official MCP Server)
```bash
# Navigation
mcporter call playwright.browser_navigate --args '{"url": "https://example.com"}'

# Interaction
mcporter call playwright.browser_click --args '{"ref": "e1", "element": "Submit button"}'

# Custom code execution
mcporter call playwright.browser_run_code --args '{"code": "async (page) => { return await page.title(); }"}'

# Screenshots, console, network
mcporter call playwright.browser_take_screenshot
mcporter call playwright.browser_console_messages
mcporter call playwright.browser_network_requests
```
**21 tools** — including `browser_run_code` for custom Playwright execution.

### OpenClaw Browser Tool (built-in)

```bash
# Navigation
browser open <url>
browser snapshot --refs aria
browser close

# Interaction
browser act kind=click ref=e312
browser act kind=type ref=e41 text="test@example.com"
browser act kind=press key="Control+k"
browser act kind=evaluate fn="() => document.title"

# Inspection
browser console
browser screenshot
```

### agent-browser CLI

```bash
# Navigation
agent-browser open <url>
agent-browser snapshot -i
agent-browser close

# Interaction
agent-browser click @e2
agent-browser fill @e3 "text"
agent-browser press Enter
agent-browser eval "document.title"

# NEW v0.25.3: Annotated Screenshots
agent-browser screenshot --annotate /tmp/proof.png

# NEW v0.25.3: Video Recording
agent-browser record start /tmp/test.webm
agent-browser record stop

# NEW v0.25.3: Visual Diff
agent-browser diff snapshot              # Current vs last
agent-browser diff screenshot --baseline # Current vs baseline
agent-browser diff url <url1> <url2>     # Side-by-side pages

# NEW v0.25.3: Auth Testing
agent-browser auth save myapp --url https://app.com --username test@example.com
agent-browser auth login myapp

# NEW v0.25.3: Debug & Profiling
agent-browser profiler start
agent-browser profiler stop /tmp/profile.json
agent-browser trace start
agent-browser trace stop /tmp/trace.json
agent-browser console --clear
agent-browser errors --clear
agent-browser highlight @e3

# NEW v0.25.3: Network HAR Capture
agent-browser network har start
agent-browser network har stop /tmp/requests.har

# NEW v0.25.3: AI Natural Language
agent-browser chat "open example.com and click the login button"

# NEW: Batch Testing
echo '[["open", "http://localhost:5173"], ["snapshot", "-i"], ["screenshot", "--annotate", "/tmp/test.png"]]' | agent-browser batch

# Network & Storage
agent-browser network har start /tmp/requests.har
agent-browser network requests --filter "api"
agent-browser network har stop
agent-browser cookies get

# Mobile Emulation
agent-browser set device "iPhone 12"
agent-browser set viewport 375 812
agent-browser set offline on

# Debug
agent-browser console --clear
agent-browser errors
agent-browser trace start /tmp/trace.json
```

### chrome-devtools-mcp

```bash
# Navigation
mcporter call chrome-devtools.navigate_page url=https://example.com
mcporter call chrome-devtools.take_snapshot
mcporter call chrome-devtools.take_screenshot filePath=/tmp/page.png

# Interaction (UID-based)
mcporter call chrome-devtools.click uid=1_12
mcporter call chrome-devtools.fill uid=1_45 value="test@example.com"
mcporter call chrome-devtools.fill_form elements='[{"uid": "1_45", "value": "email"}, {"uid": "1_46", "value": "password"}]'

# Performance
mcporter call chrome-devtools.performance_start_trace reload=true
mcporter call chrome-devtools.performance_stop_trace
mcporter call chrome-devtools.performance_analyze_insight --args '{"insightSetId": "NAVIGATION_0", "insightName": "LCPBreakdown"}'

# Audit
mcporter call chrome-devtools.lighthouse_audit

# Network
mcporter call chrome-devtools.list_network_requests resourceTypes='["xhr", "fetch"]'
mcporter call chrome-devtools.get_network_request reqid=29

# Console
mcporter call chrome-devtools.list_console_messages types='["error"]'
mcporter call chrome-devtools.get_console_message msgid=<id>

# Mobile Emulation
mcporter call chrome-devtools.emulate viewport="375x812x3,mobile,touch" networkConditions="Slow3G"
```

---

## Methodology: URL Journey Testing

### Phase 1: Define Test Cases

Before testing, document:

- **Expected behavior**: What should happen
- **Previous state**: What was broken (if regression test)
- **Verification criteria**: How to confirm fix

Example test case matrix:

```
| Issue | Expected | Verification | Tool |
|-------|----------|--------------|------|
| Hero button click | Navigate to Sign In | URL changes, form visible | browser snapshot |
| Registration submit | 201 Created | Console shows success | agent-browser network har |
| Command Palette | Search results render | List height > 0px | browser act evaluate |
| Page performance | LCP < 2.5s | Lighthouse pass | chrome-devtools lighthouse_audit |
```

### Phase 2: Execute Navigation

```bash
# Option A: OpenClaw browser (from agent session)
browser open http://localhost:5173/
browser snapshot --refs aria

# Option B: agent-browser CLI (from shell)
agent-browser open http://localhost:5173/
agent-browser snapshot -i

# Option C: chrome-devtools-mcp (DevTools-grade)
mcporter call chrome-devtools.navigate_page url=http://localhost:5173/
mcporter call chrome-devtools.take_snapshot
```

### Phase 3: Interact and Observe

```bash
# Click target element (OpenClaw browser)
browser act kind=click ref=e312
browser snapshot --refs aria

# Click target element (agent-browser)
agent-browser click @e12
agent-browser snapshot -i

# Click target element (chrome-devtools)
mcporter call chrome-devtools.click uid=1_12
mcporter call chrome-devtools.take_snapshot

# Verify navigation
agent-browser eval "window.location.href"
```

### Phase 4: Deep Inspection

When surface-level testing fails, inspect internals:

#### DOM Inspection (all tools)

```bash
# OpenClaw browser
browser act kind=evaluate fn='() => {
  const listbox = document.querySelector("[role=\"listbox\"]");
  return {
    height: listbox?.style?.getPropertyValue("--cmdk-list-height"),
    hidden: listbox?.getAttribute("hidden"),
    childCount: listbox?.childElementCount
  };
}'

# agent-browser
agent-browser eval 'JSON.stringify({
  title: document.title,
  listboxHeight: document.querySelector("[role=\"listbox\"]")?.style?.getPropertyValue("--cmdk-list-height")
})'

# chrome-devtools
mcporter call chrome-devtools.evaluate_script --args '{"function": "() => JSON.stringify({title: document.title, url: location.href})"}'
```

#### Accessibility Tree Analysis

```bash
# OpenClaw browser (ARIA refs)
browser snapshot --refs aria

# agent-browser (interactive elements)
agent-browser snapshot -i

# chrome-devtools (full a11y tree with UIDs)
mcporter call chrome-devtools.take_snapshot
```

**Look for:**
- `[hidden]` attributes on visible elements
- Missing `[cursor=pointer]` on buttons
- Empty listbox/group containers
- Incorrect `aria-*` attributes

#### Console Debugging

```bash
# OpenClaw browser
browser console

# agent-browser
agent-browser console
agent-browser console --clear
agent-browser errors

# chrome-devtools (filtered)
mcporter call chrome-devtools.list_console_messages --args '{"types": ["error", "warning"]}'
```

#### Network Request Verification

```bash
# Option A: Direct API testing (curl)
curl -s -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"testuser","password":"Test123!@","acceptTerms":"on"}'

# Option B: agent-browser HAR capture
agent-browser network har start /tmp/requests.har
# ... perform actions ...
agent-browser network har stop
agent-browser network requests --filter "api"

# Option C: chrome-devtools network inspection
mcporter call chrome-devtools.list_network_requests --args '{"resourceTypes": ["xhr", "fetch"]}'
mcporter call chrome-devtools.get_network_request reqid=29
```

#### Performance Analysis (chrome-devtools only)

```bash
# Lighthouse audit
mcporter call chrome-devtools.lighthouse_audit

# Performance trace
mcporter call chrome-devtools.performance_start_trace reload=true
# ... page loads ...
mcporter call chrome-devtools.performance_stop_trace

# Analyze specific insight
mcporter call chrome-devtools.performance_analyze_insight \
  --args '{"insightSetId": "NAVIGATION_0", "insightName": "LCPBreakdown"}'
```

### Phase 5: Evidence Collection

```bash
# Annotated screenshot (element labels)
agent-browser screenshot --annotate /tmp/evidence.png

# Video recording (interaction proof)
agent-browser record start /tmp/test-journey.webm
# ... perform test actions ...
agent-browser record stop

# Visual regression baseline
agent-browser screenshot /tmp/baseline.png
# After changes:
agent-browser diff screenshot --baseline

# Snapshot diff (structural changes)
agent-browser snapshot -i
# ... make changes ...
agent-browser diff snapshot

# Full page screenshot
agent-browser screenshot --full /tmp/full-page.png

# Mobile screenshot
agent-browser set device "iPhone 12"
agent-browser screenshot /tmp/mobile-view.png
```

---

## Common Testing Patterns

### Button Functionality Test

```bash
# 1. Identify button in snapshot
# button "Enroll Now" [ref=e312] [cursor=pointer]

# 2. Click and observe (OpenClaw)
browser act kind=click ref=e312
browser snapshot --refs aria

# 3. Click and observe (agent-browser)
agent-browser click @e12
agent-browser snapshot -i

# 4. Verify navigation
agent-browser eval "window.location.href"
```

### Form Submission Test

```bash
# 1. Navigate to form
agent-browser open http://localhost:5173/register

# 2. Start network capture
agent-browser network har start /tmp/register.har

# 3. Fill fields
agent-browser fill @e1 "test@example.com"
agent-browser fill @e2 "testuser"
agent-browser fill @e3 "TestPassword123!@"
agent-browser click @e4  # checkbox

# 4. Submit and check console
agent-browser click @e5  # submit button
agent-browser console

# 5. Stop network capture
agent-browser network har stop
agent-browser network requests --filter "auth"

# Look for: [API Response] POST /auth/register/ - 201
```

### Search/Filter Test

```bash
# 1. Open search interface
agent-browser press Control+k

# 2. Type search query
agent-browser fill @e1 "ai"

# 3. Check results rendered
agent-browser eval 'JSON.stringify({
  hasItems: document.querySelector("[role=\"listbox\"]")?.querySelectorAll("[cmdk-item]")?.length,
  height: document.querySelector("[role=\"listbox\"]")?.style?.getPropertyValue("--cmdk-list-height")
})'
```

### Mobile Navigation Test

```bash
# 1. Emulate mobile device
agent-browser set device "iPhone 12"

# 2. Navigate to page
agent-browser open http://localhost:5173/

# 3. Take screenshot
agent-browser screenshot --annotate /tmp/mobile-nav.png

# 4. Check nav visibility
agent-browser eval 'JSON.stringify({
  navVisible: !!document.querySelector("nav")?.offsetParent,
  hamburgerVisible: !!document.querySelector("[aria-label=\"Menu\"]")?.offsetParent,
  viewportWidth: window.innerWidth
})'

# 5. Test hamburger interaction
agent-browser click @e5  # hamburger button
agent-browser snapshot -i
agent-browser screenshot --annotate /tmp/mobile-nav-open.png
```

### Performance Regression Test

```bash
# 1. Navigate to page
mcporter call chrome-devtools.navigate_page url=http://localhost:5173/

# 2. Run Lighthouse
mcporter call chrome-devtools.lighthouse_audit

# 3. Start performance trace
mcporter call chrome-devtools.performance_start_trace reload=true

# 4. Stop and analyze
mcporter call chrome-devtools.performance_stop_trace

# 5. Check specific metrics
# LCP < 2500ms, CLS < 0.1, FID < 100ms
```

### Visual Regression Test

```bash
# 1. Capture baseline
agent-browser open http://localhost:5173/
agent-browser screenshot --annotate /tmp/baseline/homepage.png

# 2. After changes, capture comparison
agent-browser open http://localhost:5173/
agent-browser diff screenshot --baseline /tmp/baseline/homepage.png

# 3. Or compare snapshots
agent-browser snapshot -i
agent-browser diff snapshot

# 4. Or compare two URLs
agent-browser diff url http://localhost:5173/ http://localhost:5174/
```

---

## Troubleshooting Guide

### Issue: Element Not Found

**Symptoms:** `TimeoutError: locator.click: Timeout 8000ms exceeded`

**Causes:**
- Element not in viewport
- Element hidden by CSS
- Element not yet rendered (timing)

**Solutions:**

```bash
# Use evaluate to click directly
agent-browser eval '(() => {
  const btn = document.querySelector("button");
  if (btn?.textContent?.includes("Enroll Now")) {
    btn.click();
    return "clicked";
  }
  return "not found";
})()'

# Wait for element
agent-browser eval 'new Promise(resolve => {
  const check = () => {
    const el = document.querySelector("button");
    if (el) resolve("found");
    else setTimeout(check, 100);
  };
  check();
})'

# Use semantic locator
agent-browser find text "Enroll Now" click

# Check if element exists
agent-browser is visible @e5
```

### Issue: React State Not Updating

**Symptoms:** Input has value but component state is null

**Diagnosis:**

```bash
# Check if React state matches DOM
agent-browser eval 'JSON.stringify({
  domValue: document.querySelector("input")?.value,
  hasOnInput: !!document.querySelector("input")?.oninput,
  hasOnChange: !!document.querySelector("input")?.onchange
})'
```

**Solutions:**
- Check for conflicting handlers (cmdk library issue)
- Verify `shouldFilter` prop configuration
- Look for duplicate handler bindings

### Issue: API 400 Bad Request

**Symptoms:** Form submission fails with validation error

**Diagnosis:**

```bash
# Test API directly with curl
curl -s -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"test","password":"Test123!@","acceptTerms":"on"}'

# Check response for missing fields
# {"errors": {"first_name": ["This field is required."]}}

# Or use chrome-devtools for full request/response
mcporter call chrome-devtools.list_network_requests --args '{"resourceTypes": ["xhr"]}'
mcporter call chrome-devtools.get_network_request reqid=29
```

**Solutions:**
- Compare frontend fields with API requirements
- Check for hidden required fields
- Verify field name mapping (frontend vs backend)

### Issue: Hidden Elements in Accessibility Tree

**Symptoms:** Element shows `[hidden]` but should be visible

**Diagnosis:**

```bash
# Check hidden attribute source
agent-browser eval 'JSON.stringify({
  hiddenAttr: document.querySelector("[role=\"listbox\"]")?.getAttribute("hidden"),
  computedDisplay: getComputedStyle(document.querySelector("[role=\"listbox\"]"))?.display,
  computedVisibility: getComputedStyle(document.querySelector("[role=\"listbox\"]"))?.visibility
})'
```

### Issue: Page Performance Slow

**Symptoms:** Page loads slowly, LCP > 4s

**Diagnosis:**

```bash
# Run Lighthouse audit
mcporter call chrome-devtools.lighthouse_audit

# Performance trace
mcporter call chrome-devtools.performance_start_trace reload=true
mcporter call chrome-devtools.performance_stop_trace

# Analyze LCP breakdown
mcporter call chrome-devtools.performance_analyze_insight \
  --args '{"insightSetId": "NAVIGATION_0", "insightName": "LCPBreakdown"}'

# Check network timing
mcporter call chrome-devtools.list_network_requests
mcporter call chrome-devtools.get_network_request reqid=<slowest>
```

---

## Lessons Learned

### 1. Team Claims Need Verification

**Case:** Team reported "Homepage Enroll Now button fixed" but earlier testing showed noop handlers.

**Lesson:** Always execute actual clicks and verify navigation. Don't trust status reports without evidence.

### 2. Root Cause May Differ from Symptom

**Case:** Registration failed with generic error, suspected checkbox validation, actual cause was missing `first_name`/`last_name` fields.

**Lesson:** Use `curl` or `chrome-devtools` to test API directly. Console logs show actual API errors, not frontend interpretation.

### 3. Accessibility Tree Reveals State

**Case:** Command Palette showed `hidden=""` and `height: 0px` when broken, `hidden: null` and `height: 124px` when working.

**Lesson:** Accessibility tree snapshots provide definitive evidence of component state.

### 4. Console Logs Are Gold

**Case:** Console showed `[API Response] POST /auth/register/ - 201` confirming registration success.

**Lesson:** Always check console during form submissions. Network requests logged with status codes.

### 5. Direct API Testing Isolates Frontend from Backend

**Case:** `curl` requests proved checkbox fix worked before UI testing.

**Lesson:** Test backend independently to isolate frontend issues from backend issues.

### 6. Annotated Screenshots Communicate Better

**Case:** `agent-browser screenshot --annotate` shows element refs on image, making bug reports clearer.

**Lesson:** Use annotated screenshots for visual evidence. Labels help developers locate elements quickly.

### 7. Video Recording Captures Interactions

**Case:** WebM recording of test session shows exact sequence of actions and results.

**Lesson:** Record video for complex interactions. Helps reproduce issues and demonstrate fixes.

### 8. Performance Tracing Finds Hidden Bottlenecks

**Case:** Lighthouse showed 89 a11y score, but performance trace revealed LCP 258ms with specific resource blocking.

**Lesson:** Use chrome-devtools performance tracing for detailed timing analysis beyond Lighthouse scores.

---

## Blockers Encountered (Historical)

### Solved: Checkbox Validation

**Problem:** Checkbox sends `"on"` string, backend expected boolean.

**Solution:** Team updated Zod schema to accept `z.union([z.boolean(), z.string()])`.

**Verification:** Both `"on"` and `true` now accepted via curl.

### Solved: Missing Required Fields

**Problem:** Registration form missing `first_name`/`last_name`, API returned 400.

**Solution:** Backend made fields optional or auto-populated.

**Verification:** Registration now succeeds with just email/username/password.

### Solved: Command Palette Not Rendering

**Problem:** `query` state null, list height 0px, no items rendered.

**Solution:** Team added `shouldFilter={false}` to disable cmdk's built-in filtering.

**Verification:** List height 124px, items visible in accessibility tree.

---

## Recommended Next Steps

1. **Automate repetitive tests** — Use `agent-browser batch` for regression testing
2. **Document API schemas** — Maintain OpenAPI specs for frontend/backend contract
3. **Add visual regression** — Use `agent-browser diff` for UI change detection
4. **Record test sessions** — Use `agent-browser record` for historical evidence
5. **Create test data fixtures** — Consistent test accounts and data
6. **Monitor performance** — Regular Lighthouse audits with chrome-devtools

---

## Resources

### Related Skills

- **browser-automation/SKILL.md** — Full browser automation guide (agent-browser + OpenClaw browser)
- **chrome-devtools-mcp/SKILL.md** — DevTools-grade debugging with MCP
- **mobile-navigation.md** — Mobile navigation debugging taxonomy (Classes A-H)

### Reference Files

- **mobile-navigation.md** — Root-cause taxonomy for mobile nav failures
