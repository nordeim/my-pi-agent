---
name: playwright-cli
description: Automate browser interactions, test web pages and work with Playwright tests. Is a better choice for traditional browser testing - multi-browser support (Firefox, WebKit), Playwright-native locators, and the run-code command for custom Playwright snippets.
allowed-tools: Bash(playwright-cli:*) Bash(npx:*) Bash(npm:*)
---

> ✅ **Pre-installed:** `playwright-cli` is available system-wide — call directly without any prior installation: `playwright-cli open <url>`

**Status:** ✅ @playwright/cli v0.1.14 | Pre-installed
**Updated:** 2026-06-27

# Browser Automation with playwright-cli

## Quick start

```bash
# open new browser
playwright-cli open
# navigate to a page
playwright-cli goto https://playwright.dev
# interact with the page using refs from the snapshot
playwright-cli click e15
playwright-cli type "page.click"
playwright-cli press Enter
# take a screenshot (rarely used, as snapshot is more common)
playwright-cli screenshot
# close the browser
playwright-cli close
```

---

## Commands

### Core

```bash
playwright-cli open [url]                  # Open browser (optionally navigate)
playwright-cli attach [name]               # Attach to a running Playwright browser
playwright-cli close                       # Close the browser
playwright-cli detach                      # Detach from an attached browser
playwright-cli goto <url>                  # Navigate to a URL
playwright-cli click <target> [button]     # Click element (left/right/middle)
playwright-cli dblclick <target> [button]  # Double-click element
playwright-cli type <text>                 # Type text into focused editable element
playwright-cli fill <target> <text>        # Clear and fill text into element
playwright-cli fill <target> <text> --submit  # Fill + press Enter
playwright-cli hover <target>              # Hover over element
playwright-cli select <target> <val>       # Select dropdown option
playwright-cli check <target>              # Check checkbox/radio
playwright-cli uncheck <target>            # Uncheck checkbox/radio
playwright-cli drag <start> <end>          # Drag and drop between elements
playwright-cli drop <target>               # Drop files or data onto an element
playwright-cli upload <file>               # Upload one or multiple files
playwright-cli snapshot [target]           # Capture page snapshot (YAML with refs)
playwright-cli eval <func> [target]        # Evaluate JS on page or element
playwright-cli dialog-accept [prompt]      # Accept a dialog
playwright-cli dialog-dismiss              # Dismiss a dialog
playwright-cli resize <w> <h>              # Resize browser window
playwright-cli delete-data                 # Delete session data
playwright-cli generate-locator <target>   # Generate Playwright locator for element
playwright-cli highlight [target]          # Highlight element overlay (--hide to remove)
playwright-cli show                        # Show Playwright dashboard
```

### Navigation

```bash
playwright-cli go-back                     # Go back
playwright-cli go-forward                  # Go forward
playwright-cli reload                      # Reload current page
```

### Keyboard

```bash
playwright-cli press <key>                 # Press a key (e.g., Enter, ArrowDown, a)
playwright-cli keydown <key>               # Hold key down
playwright-cli keyup <key>                 # Release key
```

### Mouse

```bash
playwright-cli mousemove <x> <y>           # Move mouse to position
playwright-cli mousedown [button]          # Press mouse button (left/right/middle)
playwright-cli mouseup [button]            # Release mouse button
playwright-cli mousewheel <dx> <dy>        # Scroll mouse wheel
```

### Screenshot & PDF

```bash
playwright-cli screenshot                   # Screenshot viewport (auto-saved)
playwright-cli screenshot <target>          # Screenshot specific element
playwright-cli screenshot --filename=path  # Save to specific path
playwright-cli screenshot --full-page      # Full scrollable page
playwright-cli pdf                         # Save as PDF (auto-saved)
playwright-cli pdf --filename=path.pdf     # Save PDF to specific path
```

### Tabs

```bash
playwright-cli tab-list                     # List all tabs
playwright-cli tab-new [url]               # Create new tab
playwright-cli tab-select <index>          # Select tab by index
playwright-cli tab-close [index]           # Close tab (default: current)
```

### Storage (State, Cookies, Storage)

```bash
# Full state (auth persistence)
playwright-cli state-save [filename]       # Save cookies + storage to file
playwright-cli state-load <filename>       # Load saved state from file

# Cookies
playwright-cli cookie-list                          # List all cookies
playwright-cli cookie-list --domain=example.com     # Filter by domain
playwright-cli cookie-get <name>                    # Get specific cookie
playwright-cli cookie-set <name> <value>            # Set cookie
playwright-cli cookie-set <name> <value> --domain=example.com --path=/ --expires=<unix> --httpOnly --secure --sameSite=strict
playwright-cli cookie-delete <name>                 # Delete specific cookie
playwright-cli cookie-clear                         # Clear all cookies

# LocalStorage
playwright-cli localstorage-list                    # List all
playwright-cli localstorage-get <key>               # Get item
playwright-cli localstorage-set <key> <value>       # Set item
playwright-cli localstorage-delete <key>            # Delete item
playwright-cli localstorage-clear                  # Clear all

# SessionStorage
playwright-cli sessionstorage-list                  # List all
playwright-cli sessionstorage-get <key>             # Get item
playwright-cli sessionstorage-set <key> <value>     # Set item
playwright-cli sessionstorage-delete <key>          # Delete item
playwright-cli sessionstorage-clear                # Clear all
```

### Network

```bash
# Request inspection (numbered list; use number with subcommands below)
playwright-cli requests                    # List network requests (excludes static)
playwright-cli requests --static           # Include static assets (fonts, images, etc.)
playwright-cli request <index>             # Full details of single request (headers, body, response)
playwright-cli request-headers <index>     # Request headers only
playwright-cli request-body <index>        # Request body only
playwright-cli response-headers <index>    # Response headers only
playwright-cli response-body <index>       # Response body (text inline, binary saved to file)

# Request mocking
playwright-cli route <pattern>             # Intercept requests matching URL pattern
playwright-cli route <pattern> --status=404
playwright-cli route <pattern> --body='{"mock": true}'
playwright-cli route <pattern> --content-type=application/json
playwright-cli route <pattern> --header="Authorization: Bearer token"
playwright-cli route <pattern> --remove-header="Set-Cookie"
playwright-cli route-list                  # List active routes
playwright-cli unroute [pattern]           # Remove routes (or all)

# Network state
playwright-cli network-state-set <state>   # Set online or offline
```

### DevTools & Debugging

```bash
playwright-cli console [min-level]         # List console messages (info/warning/error)
playwright-cli console --clear             # Clear console logs
playwright-cli run-code [code]             # Run Playwright code snippet
playwright-cli run-code --filename=path.js # Run code from file
playwright-cli tracing-start               # Start trace recording
playwright-cli tracing-stop                # Stop trace recording
playwright-cli video-start [filename]      # Start video recording (WebM)
playwright-cli video-start recording.webm --size=800x600
playwright-cli video-stop                  # Stop and save video
playwright-cli video-chapter <title>       # Add chapter marker
playwright-cli video-chapter "Login" --description="Auth flow" --duration=2000
playwright-cli video-show-actions          # Annotate CLI actions on video
playwright-cli video-show-actions --duration=500 --position=top-right --cursor=pointer
playwright-cli video-hide-actions          # Stop annotating actions
playwright-cli show                        # Open Playwright dashboard
```

### Test Debugging

```bash
playwright-cli pause-at <file>:<line>      # Run test up to location and pause
playwright-cli resume                      # Resume paused test execution
playwright-cli step-over                   # Step over next call
```

### Browser Sessions

```bash
playwright-cli list                        # List active browser sessions
playwright-cli close-all                   # Close all browser sessions
playwright-cli kill-all                    # Force-kill all browser processes (zombie cleanup)
```

### Install

```bash
playwright-cli install                     # Initialize workspace
playwright-cli install-browser [browser]   # Install browser (chrome/firefox/webkit)
playwright-cli install-browser --with-deps # Also install system dependencies (Linux)
playwright-cli install-browser --list      # List browsers from all Playwright installations
playwright-cli install-browser --force     # Force reinstall
playwright-cli install-browser --only-shell  # Install headless shell only (Chromium)
```

---

## Global Options

| Flag | Description |
|---|---|
| `-s, --session <name>` | Use named browser session |
| `--json` | Output response as JSON |
| --raw` | Output only result value (no status/code/page sections) |
| `--version` | Print version |

---

## Sessions (Parallel Browsers)

### Named sessions

```bash
playwright-cli -s=mysession open example.com
playwright-cli -s=mysession click e6
playwright-cli -s=mysession snapshot
playwright-cli -s=mysession close
playwright-cli list
```

### Persistent profiles

```bash
# In-memory (default)
playwright-cli open example.com

# Persistent profile (auto-created)
playwright-cli open example.com --persistent

# Custom profile directory
playwright-cli open example.com --profile=/path/to/profile
playwright-cli -s=mysession open example.com --profile=/path/to/profile
playwright-cli -s=mysession delete-data   # Delete user data for persistent session
```

### Browser selection

```bash
playwright-cli open --browser=chrome
playwright-cli open --browser=firefox
playwright-cli open --browser=webkit
playwright-cli open --browser=msedge
```

### Headed mode

```bash
playwright-cli open example.com --headed
```

### Config file

```bash
playwright-cli open --config=my-config.json
```

### Attach to running browser

```bash
# Attach by name
playwright-cli attach mybrowser

# Connect via CDP endpoint
playwright-cli attach --cdp=ws://localhost:9222/devtools/browser/...

# Connect via Playwright endpoint
playwright-cli attach --endpoint=ws://localhost:9222/...

# Connect via browser extension
playwright-cli attach --extension
playwright-cli attach --extension=chrome
```

### Detach (keep browser running)

```bash
playwright-cli detach    # Detach without closing
```

---

## Raw Output Mode

The `--raw` flag strips page status, generated code, and snapshot sections — returns only the result value. Use it for piping into other tools.

```bash
playwright-cli --raw eval "JSON.stringify(performance.timing)" | jq '.loadEventEnd - .navigationStart'
playwright-cli --raw eval "JSON.stringify([...document.querySelectorAll('a')].map(a => a.href))" > links.json
playwright-cli --raw snapshot > before.yml
playwright-cli click e5
playwright-cli --raw snapshot > after.yml
diff before.yml after.yml
TOKEN=$(playwright-cli --raw cookie-get session_id)
playwright-cli --raw localstorage-get theme
```

### JSON Output Mode

The `--json` flag returns structured JSON:

```bash
playwright-cli --json eval "document.title"
# {"result": "\"StoryIntoVideo - Turn Stories Into Videos with AI\""}
```

---

## Snapshots

After each command, playwright-cli outputs a snapshot of the current browser state. Use `snapshot` on demand.

```bash
# Default: save to file with timestamp-based name
playwright-cli snapshot

# Save to specific file
playwright-cli snapshot --filename=after-click.yaml

# Snapshot a specific element (partial snapshot)
playwright-cli snapshot "#main"
playwright-cli snapshot e34

# Limit depth for efficiency
playwright-cli snapshot --depth=4

# Include bounding boxes
playwright-cli snapshot --boxes
```

### Snapshot options

| Flag | Description |
|---|---|
| `--filename <path>` | Save snapshot to file instead of inline |
| `--depth <n>` | Limit snapshot depth |
| `--boxes` | Include bounding boxes `[box=x,y,width,height]` |

---

## Targeting Elements

### By ref (recommended)

```bash
playwright-cli snapshot
playwright-cli click e15
playwright-cli fill e22 "text"
```

### By CSS selector

```bash
playwright-cli click "#main > button.submit"
playwright-cli fill "#email" "user@example.com"
```

### By Playwright locator

```bash
playwright-cli click "getByRole('button', { name: 'Submit' })"
playwright-cli fill "getByTestId('submit-button')" "text"
```

### Generate locator from ref

```bash
playwright-cli generate-locator e45
# Output: getByRole('heading', { name: 'Your Projects' })
```

### Highlight element

```bash
playwright-cli highlight e49              # Show highlight overlay
playwright-cli highlight e49 --style "outline: 2px dashed red"
playwright-cli highlight e49 --hide       # Remove highlight for element
playwright-cli highlight --hide           # Remove all highlights
```

---

## Drop (Drag & Drop Target)

Drop files or data onto an element:

```bash
# Drop files
playwright-cli drop e10 --path=/tmp/file1.pdf --path=/tmp/file2.pdf

# Drop data
playwright-cli drop e10 --data "text/plain=hello" --data "text/uri-list=https://example.com"
```

---

## Eval (JavaScript Evaluation)

```bash
# Page-level eval
playwright-cli eval "document.title"
playwright-cli eval "document.querySelectorAll('img').length"

# Element-level eval (receives element as argument)
playwright-cli eval "el => el.textContent" e5
playwright-cli eval "el => el.id" e5
playwright-cli eval "el => el.getAttribute('data-testid')" e5
playwright-cli eval "el => el.getBoundingClientRect().width" e5
```

---

## Run Code (Custom Playwright Snippets)

Execute arbitrary Playwright code:

```bash
# Inline code (function receives page as argument)
playwright-cli run-code "async page => await page.context().grantPermissions(['geolocation'])"
playwright-cli run-code "async page => { await page.setViewportSize({ width: 1920, height: 1080 }); }"

# From file
playwright-cli run-code --filename=script.js
```

---

## Examples

### Form submission

```bash
playwright-cli open https://example.com/form
playwright-cli snapshot

playwright-cli fill e1 "user@example.com"
playwright-cli fill e2 "password123"
playwright-cli click e3
playwright-cli snapshot
playwright-cli close
```

### Authentication with saved state

```bash
# Login once
playwright-cli open https://app.example.com/login
playwright-cli snapshot
playwright-cli fill e1 "username"
playwright-cli fill e2 "password"
playwright-cli click e3
playwright-cli snapshot
playwright-cli state-save auth.json

# Later sessions: load saved state
playwright-cli state-load auth.json
playwright-cli open https://app.example.com/dashboard
```

### Multi-tab workflow

```bash
playwright-cli open https://example.com
playwright-cli tab-new https://example.com/other
playwright-cli tab-list
playwright-cli tab-select 0
playwright-cli snapshot
playwright-cli close
```

### Network request inspection

```bash
playwright-cli open https://app.example.com
playwright-cli requests                # List API calls (excludes static)
playwright-cli requests --static       # Include all requests
playwright-cli request 5               # Full details of request #5
playwright-cli response-body 5         # Get response body
playwright-cli request-headers 5       # Get request headers
```

### Request mocking

```bash
playwright-cli open https://app.example.com
playwright-cli route "**/api/users" --status=404
playwright-cli route "https://api.example.com/**" --body='{"mock": true}' --content-type=application/json
playwright-cli route-list
playwright-cli click e10               # Trigger mocked request
playwright-cli requests                # Verify mock was hit
playwright-cli unroute                 # Clean up
```

### Offline mode testing

```bash
playwright-cli open https://app.example.com
playwright-cli network-state-set offline
playwright-cli reload                  # Test offline behavior
playwright-cli network-state-set online
```

### Video recording with action annotations

```bash
playwright-cli open https://app.example.com
playwright-cli video-start demo.webm
playwright-cli video-show-actions      # Annotate subsequent actions
playwright-cli click e10
playwright-cli fill e12 "test"
playwright-cli video-chapter "Login" --description="Auth flow" --duration=2000
playwright-cli video-hide-actions
playwright-cli video-stop
```

### Debugging with traces

```bash
playwright-cli open https://example.com
playwright-cli tracing-start
playwright-cli click e4
playwright-cli fill e7 "test"
playwright-cli tracing-stop
playwright-cli close
```

### Connect to running browser via CDP

```bash
# Auto-discover via CDP
playwright-cli attach --cdp=ws://localhost:9222/devtools/browser/...

# Or via Playwright endpoint
playwright-cli attach --endpoint=ws://localhost:9222/...

# Use it
playwright-cli snapshot
playwright-cli click e10

# Detach (browser keeps running)
playwright-cli detach
```

### Parallel sessions

```bash
playwright-cli -s=chrome open site-a.com --browser=chrome
playwright-cli -s=firefox open site-b.com --browser=firefox
playwright-cli -s=chrome snapshot
playwright-cli -s=firefox snapshot
playwright-cli list
playwright-cli close-all
```

---

## Installation

### CLI Tool
If global `playwright-cli` command is not available, try a local version via `npx playwright-cli`:

```bash
npx --no-install playwright-cli --version
```

When local version is available, use `npx playwright-cli` in all commands. Otherwise, install `playwright-cli` as a global command:

```bash
# Install CLI (v0.1.14)
npm install -g @playwright/cli@latest
```

### MCP Server
`@playwright/mcp` provides a Playwright MCP server with 21 tools including `browser_run_code` for custom Playwright snippets. Configure in `~/.mcporter/mcporter.json`:
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp"]
    }
  }
}
```

### Choose Your Tool
- **playwright-cli** — CLI for terminal/scripts, session management
- **@playwright/mcp** — MCP server for AI agent integration via mcporter

---

## Specific tasks

* **Running and Debugging Playwright tests** [references/playwright-tests.md](references/playwright-tests.md)
* **Request mocking** [references/request-mocking.md](references/request-mocking.md)
* **Running Playwright code** [references/running-code.md](references/running-code.md)
* **Browser session management** [references/session-management.md](references/session-management.md)
* **Storage state (cookies, localStorage)** [references/storage-state.md](references/storage-state.md)
* **Test generation** [references/test-generation.md](references/test-generation.md)
* **Tracing** [references/tracing.md](references/tracing.md)
* **Video recording** [references/video-recording.md](references/video-recording.md)
* **Inspecting element attributes** [references/element-attributes.md](references/element-attributes.md)
