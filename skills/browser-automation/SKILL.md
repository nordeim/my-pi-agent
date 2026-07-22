---
name: browser-automation
description: Fast browser automation CLI for AI agents using Chrome/Chromium via CDP. Use when automating web interactions, taking snapshots, filling forms, navigating pages, or testing web applications without Playwright/Puppeteer dependency.
---

# browser-automation

**Skill:** `/home/pete/.openclaw/workspace/skills/browser-automation/SKILL.md`
**Status:** ✅ v0.26.0 | Chrome 147.0.7727.24 | Pre-installed
**Updated:** 2026-04-23

> ✅ **Pre-installed:** `agent-browser` is available system-wide — call directly without any prior installation: `agent-browser open <url>`

**What it is:** Fast browser automation CLI for AI agents. Chrome/Chromium via CDP, no Playwright or Puppeteer dependency. Accessibility-tree snapshots with compact `@eN` refs let agents interact with pages in ~200-400 tokens instead of parsing raw HTML.

### Key Capabilities
- **Core loop**: `open → snapshot -i → click @ref → re-snapshot` workflow
- **Built-in skills system** (NEW in v0.26.0): core, dogfood, electron, slack, vercel-sandbox, agentcore
- **Semantic locators**: role, text, label, placeholder, alt, title, testid, first, last, nth
- **Snapshot options**: `-i` (interactive), `-u` (href urls), `-c` (compact), `-d` (depth), `-s` (selector), `--json` (machine-readable)
- **Interacting**: click, fill, type, select, upload, scroll, drag-and-drop, hover, focus, check/uncheck
- **Keyboard**: `keyboard type` (real keystrokes), `keyboard inserttext` (no key events), `press` (Enter, Tab, Control+a, etc.)
- **Get Info**: text, html, value, attr, title, url, count, box, styles, cdp-url
- **Check State**: is <what> (visible, enabled, checked)
- **Find Elements**: find <locator> <value> <action> [text]
- **Mouse**: mouse <action> [args] (move, down, up, wheel)
- **Browser Settings**: set <setting> [value] (viewport, device, geo, offline, headers, credentials, media)
- **Network**: network <action> (route, unroute, requests, har)
- **Storage**: cookies, storage (local/session)
- **Tabs**: tab [new|list|close|<n>]
- **Console & Errors**: console, errors
- **Wait Strategies**: wait @ref, wait --text "...", wait --url "**/pattern", wait --load networkidle/domcontentloaded, wait --fn "JS condition"
- **Common workflows**: log in, persist session (state save/load), auth vault
- **Parallel sessions**: multiple browser sessions via --session flag

### New Capabilities in v0.26.0
- **Built-in skills system**: Specialized skills for specific domains:
  - `core`: Core usage guide (always load first)
  - `dogfood`: Systematic exploratory testing with issue taxonomy and structured reporting
  - `electron`: Automate Electron desktop apps (VS Code, Slack, Discord, Figma, etc.)
  - `slack`: Interact with Slack workspaces using browser automation
  - `vercel-sandbox`: Run agent-browser + Chrome inside Vercel Sandbox microVMs
  - `agentcore`: Run agent-browser on AWS Bedrock AgentCore cloud browsers
- **Chrome DevTools profiler and trace capture** (via skills)
- **Network HAR recording**: `agent-browser network har start|stop [path]`
- **Console and error tracking**: `agent-browser console`, `agent-browser errors`
- **Video recording (WebM)**: Available via skills
- **Visual diff**: snapshot, screenshot, URL comparison (via skills)
- **Semantic locators**: role, text, label, placeholder, alt, title, testid, first, last, nth
- **Batch execution**: Execute multiple commands efficiently
- **Auth vault**: Secure credential management with `agent-browser auth save|login|list|remove`
- **Confirm-actions workflow**: For destructive operations requiring explicit confirmation
- **Dashboard**: Visual interface for monitoring and control
- **AI chat mode**: Natural language control via `agent-browser chat`

### Quick Reference
```bash
# Core workflow
agent-browser open https://example.com          # 1. Navigate
agent-browser snapshot -i                       # 2. See interactive elements
agent-browser click @e3                         # 3. Act on ref
agent-browser snapshot -i                       # 4. Re-snapshot after change

# With built-in skills
agent-browser skills list                       # See available skills
agent-browser skills get core --full            # Load core skill documentation
agent-browser skills get dogfood                # Load exploratory testing skill

# Authentication vault
agent-browser auth save my-app --url https://app.example.com/login \
  --username user@example.com --password-stdin
agent-browser auth login my-app                 # Auto-fill and login

# Network monitoring
agent-browser network har start /tmp/network.har # Start HAR recording
# ... perform actions ...
agent-browser network har stop                  # Stop and save HAR

# Device emulation
agent-browser set device "iPhone 12"            # Emulate iPhone 12
agent-browser set viewport 1920 1080            # Set custom viewport

# Tab management
agent-browser tab new                           # Open new tab
agent-browser tab list                          # List all tabs
agent-browser tab close                         # Close current tab
agent-browser tab 2                             # Switch to tab index 2

# Console and errors
agent-browser console                           # View console logs
agent-browser errors                            # View JavaScript errors

# Wait strategies (critical for reliability)
agent-browser wait @e1                          # Wait for element to appear
agent-browser wait --text "Success"             # Wait for text on page
agent-browser wait --url "**/dashboard"         # Wait for URL pattern
agent-browser wait --load networkidle           # Wait for network idle (SPA navigation)

# Semantic locators (no prior snapshot needed)
agent-browser find role button click --name "Submit"
agent-browser find text "Sign In" click
agent-browser find label "Email" fill "user@test.com"
agent-browser find placeholder "Search" type "query"
agent-browser find testid "submit-btn" click

# Mouse actions
agent-browser mouse move 100 200                # Move to coordinates
agent-browser mouse down                        # Mouse down
agent-browser mouse up                          # Mouse up
agent-browser mouse wheel -100                  # Scroll vertically

# Specialized skills
agent-browser dogfood init {OUTPUT_DIR}         # Initialize exploratory testing
agent-browser dogfood auth {SESSION}            # Handle authentication
agent-browser dogfood orient {SESSION}          # Take initial snapshot
agent-browser dogfood explore {SESSION}         # Systematic exploration
agent-browser dogfood document {SESSION}        # Document issues found
```

### Configuration
- No configuration file needed - works out of the box
- Uses Chrome/Chromium via Chrome DevTools Protocol (CDP)
- Browser binary automatically managed
- Skills are version-matched to the CLI

### When to Use
- Navigate to URLs and interact with web pages
- Fill forms, click buttons, extract data
- Take screenshots or generate PDFs
- Test web applications and find bugs
- Automate repetitive browser tasks
- Exploratory testing with structured reporting (dogfood skill)
- Electron app automation (electron skill)
- Slack workspace interaction (slack skill)
- Cloud browser provisioning (agentcore, vercel-sandbox skills)

### Gotchas
- Refs (`@eN`) become stale the moment the page changes - always re-snapshot after clicks that navigate, form submits, dynamic re-renders, or dialog opens
- Avoid bare `wait 2000` - use intelligent waits based on element appearance, text, URL, or network idle
- For sensitive credentials, use the auth vault instead of typing passwords in shell commands
- The direct `agent-browser` binary uses the fast Rust client; avoid `npx agent-browser` which is significantly slower
- When refs don't work, fall back to semantic locators (role/text/label) or raw CSS selectors