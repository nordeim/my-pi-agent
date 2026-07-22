---
name: chrome-devtools-mcp
description: Google-official MCP server providing full Chrome DevTools Protocol access (29 tools). Use for Lighthouse audits, performance traces, network inspection, console log access, JavaScript evaluation, mobile emulation, and memory snapshots.
---

# chrome-devtools-mcp

**Skill:** `/home/pete/.openclaw/workspace/skills/chrome-devtools-mcp/SKILL.md`
**Status:** ✅ v0.23.0 | Chrome 147.0.7727.24
**Updated:** 2026-04-26
**What it is:** Google-official MCP server providing full Chrome DevTools Protocol access (29 tools). Installed via npm, configured in mcporter.

### Version Info

| Component | Version | Notes |
|-----------|---------|-------|
| chrome-devtools-mcp | 0.23.0 | CLI wrapper |
| Chrome (headless) | 147.0.7727.24 | Updated Mar 26 2026 |
| Transport | mcporter stdio | — |

### Key Capabilities (29 Tools)
- **Navigation** (5): navigate_page, new_page, list_pages, select_page, close_page
- **Interaction** (8): click, hover, drag, fill, fill_form, type_text, press_key, upload_file
- **Inspection & Debugging** (5): evaluate_script, list_console_messages, get_console_message, list_network_requests, get_network_request
- **Performance** (3): performance_start_trace, performance_stop_trace, performance_analyze_insight
- **Audit** (1): lighthouse_audit
- **Memory** (1): take_memory_snapshot
- **Visual** (3): take_screenshot, take_snapshot, wait_for
- **Emulation** (2): emulate, resize_page
- **Dialog** (1): handle_dialog

### When to Use
Use **chrome-devtools-mcp** for:
- Lighthouse audits (Accessibility, Best Practices, SEO scores with reports)
- Performance traces (LCP, CLS, INP with actionable insights)
- Network inspection (list/get requests with full headers, body, timing)
- Console log access (filter by type: error/warning/info)
- JavaScript evaluation (run arbitrary JS in page context)
- Mobile emulation (device profiles: iPhone, Pixel, network throttling: 3G, CPU throttling)
- Memory snapshots (heap dump capture for leak debugging)

Use **built-in browser tool** for:
- Quick nav, screenshots, simple snapshots
- Profile switching (openclaw/user/chrome-relay)
- Routine automation where DevTools-grade inspection isn't needed

### Quick Reference
```bash
# Via mcporter (recommended)
mcporter call chrome-devtools.navigate_page url=https://example.com
mcporter call chrome-devtools.take_snapshot          # A11y tree with UIDs
mcporter call chrome-devtools.lighthouse_audit       # Full Lighthouse run
mcporter call chrome-devtools.performance_start_trace
mcporter call chrome-devtools.performance_stop_trace
mcporter call chrome-devtools.evaluate_script --args '{"function": "() => document.title"}'
mcporter call chrome-devtools.list_network_requests
mcporter call chrome-devtools.emulate viewport="375x812x2,mobile,touch"

# CLI wrapper
/usr/bin/chrome-devtools <tool_name> [args...]
```

### Configuration
**Config:** `~/.mcporter/mcporter.json` — stdio transport, headless mode
**Flags:** `--headless`, `--no-usage-statistics`, `--no-performance-crux`
**Connect to existing Chrome:** `--browserUrl=http://127.0.0.1:9222`

### Practical Example: Performance Analysis
```bash
# 1. Navigate
mcporter call chrome-devtools.navigate_page url=https://www.example.com

# 2. Start performance trace
mcporter call chrome-devtools.performance_start_trace reload=true

# 3. Stop trace and get analysis
mcporter call chrome-devtools.performance_stop_trace
# → Returns LCP, CLS, INP, TTFB, and insights like:
#    LCPBreakdown, CLSCulprits, NetworkDependencyTree, ThirdParties, Cache

# 4. Deep-dive into specific insight
mcporter call chrome-devtools.performance_analyze_insight \
  --args '{"insightSetId": "NAVIGATION_0", "insightName": "LCPBreakdown"}'
```

### Gotchas
- Element UIDs from `take_snapshot` are ephemeral — they change on every snapshot/DOM mutation. Always re-snapshot after navigation or interaction.
- The `function` parameter in `evaluate_script` must be a string containing a valid JS function.
- Performance traces are per-navigation; each start/stop pair captures one page load.
- Lighthouse audits take 5-15 seconds; use `--no-performance-crux` to skip CrUX field data for faster audits.
- All pages share one Chrome instance; emulation settings (viewport, network throttling) apply globally until reset.
- Memory snapshots generate large heap dump files; use `filePath` to control output location.

### Verification (2026-04-23)
- Daemon confirmed running via mcporter with 29 tools available
- Basic navigation and snapshot functionality verified
- Lighthouse audit, performance tracing, and network inspection tools accessible
- Mobile emulation and console log access functional

*Skill updated: 2026-04-26 | chrome-devtools-mcp v0.23.0 with Chrome 147.0.7727.24 headless*