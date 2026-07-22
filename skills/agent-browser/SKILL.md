---
name: agent-browser
description: A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands. Is a better choice for AI agent workflows - compact snapshots save tokens, the auth vault handles credentials securely, and React DevTools integration is valuable for frontend debugging.
read_when:
  - Automating web interactions
  - Extracting structured data from pages
  - Filling forms programmatically
  - Testing web UIs
  - Debugging React applications
  - Measuring Core Web Vitals
  - Managing browser auth state
metadata: {"clawdbot":{"emoji":"🌐","requires":{"bins":["node","npm"]}}}
allowed-tools: Bash(agent-browser:*)
---

# Browser Automation with agent-browser

> **Version:** 0.29.1 (Rust-based CLI with Node.js fallback)

## Installation

### npm (recommended)

```bash
npm install -g agent-browser
agent-browser install
agent-browser install --with-deps
```

### Homebrew

```bash
brew install agent-browser
```

### Cargo

```bash
cargo install agent-browser
```

### From Source

```bash
git clone https://github.com/vercel-labs/agent-browser
cd agent-browser
pnpm install
pnpm build
agent-browser install
```

### Maintenance

```bash
agent-browser upgrade       # Upgrade to the latest version
agent-browser doctor        # Diagnose install issues
agent-browser doctor --fix  # Auto-clean stale files
agent-browser profiles      # List available Chrome profiles
```

## Quick start

```bash
agent-browser open <url>        # Navigate to page
agent-browser snapshot -i       # Get interactive elements with refs
agent-browser click @e1         # Click element by ref
agent-browser fill @e2 "text"   # Fill input by ref
agent-browser close             # Close browser
```

## Core workflow

1. Navigate: `agent-browser open <url>`
2. Snapshot: `agent-browser snapshot -i` (returns elements with refs like `@e1`, `@e2`)
3. Interact using refs from the snapshot
4. Re-snapshot after navigation or significant DOM changes

---

## Commands

### Navigation

```bash
agent-browser open <url>      # Navigate to URL
agent-browser back            # Go back
agent-browser forward         # Go forward
agent-browser reload          # Reload page
agent-browser close [--all]   # Close browser (--all closes every session)
```

### SPA / Client-side Navigation

For single-page applications (Next.js, React Router, etc.) where `open` would trigger a full page reload:

```bash
agent-browser pushstate <url>   # SPA client-side navigation
```

`pushstate` auto-detects `window.next.router.push` (triggers RSC fetch on Next.js) and falls back to `history.pushState` + `popstate`/`navigate` events for other frameworks.

### Snapshot (page analysis)

```bash
agent-browser snapshot            # Full accessibility tree
agent-browser snapshot -i         # Interactive elements only (recommended)
agent-browser snapshot -c         # Compact output
agent-browser snapshot -d 3       # Limit depth to 3
agent-browser snapshot -s "#main" # Scope to CSS selector
```

**Snapshot options:**

| Flag | Description |
|---|---|
| `-i, --interactive` | Only interactive elements |
| `-c, --compact` | Remove empty structural elements |
| `-d, --depth <n>` | Limit tree depth |
| `-s, --selector <sel>` | Scope to CSS selector |

### Interactions (use @refs from snapshot)

```bash
agent-browser click @e1           # Click
agent-browser dblclick @e1        # Double-click
agent-browser focus @e1           # Focus element
agent-browser fill @e2 "text"     # Clear and type
agent-browser type @e2 "text"     # Type without clearing
agent-browser press Enter         # Press key
agent-browser press Control+a     # Key combination
agent-browser keyboard type <text>    # Type with real keystrokes (no selector)
agent-browser keyboard inserttext <text>  # Insert text without key events
agent-browser hover @e1           # Hover
agent-browser check @e1           # Check checkbox
agent-browser uncheck @e1         # Uncheck checkbox
agent-browser select @e1 "value"  # Select dropdown
agent-browser scroll <dir> [px]   # Scroll (up/down/left/right)
agent-browser scrollintoview @e1  # Scroll element into view
agent-browser drag @e1 @e2        # Drag and drop
agent-browser upload @e1 file.pdf # Upload files
agent-browser download @e1 <path> # Download file by clicking element
```

### Get information

```bash
agent-browser get text @e1        # Get element text
agent-browser get html @e1        # Get innerHTML
agent-browser get value @e1       # Get input value
agent-browser get attr @e1 href   # Get attribute
agent-browser get title           # Get page title
agent-browser get url             # Get current URL
agent-browser get count ".item"   # Count matching elements
agent-browser get box @e1         # Get bounding box (x, y, width, height)
agent-browser get styles @e1      # Get computed styles
agent-browser get cdp-url         # Get CDP WebSocket URL
```

### Check state

```bash
agent-browser is visible @e1      # Check if visible
agent-browser is enabled @e1      # Check if enabled
agent-browser is checked @e1      # Check if checked
```

### Find elements (semantic locators, alternative to refs)

```bash
agent-browser find role button click --name "Submit"
agent-browser find text "Sign In" click
agent-browser find label "Email" fill "user@test.com"
agent-browser find placeholder "Search" fill "query"
agent-browser find alt "Logo" click
agent-browser find title "Tooltip" hover
agent-browser find testid "submit-btn" click
agent-browser find first ".item" click
agent-browser find last ".item" click
agent-browser find nth 2 "a" text
```

### Screenshots & PDF

```bash
agent-browser screenshot              # Screenshot to stdout
agent-browser screenshot path.png     # Save to file
agent-browser screenshot --full       # Full page
agent-browser screenshot --annotate   # Annotated screenshot with numbered labels
agent-browser pdf output.pdf          # Save as PDF
```

### Video recording

```bash
agent-browser record start <path> [url]   # Start recording (WebM)
agent-browser record stop                 # Stop and save video
```

Recording creates a fresh context but preserves cookies/storage from your session. If no URL is provided, it automatically returns to your current page. For smooth demos, explore first, then start recording.

### Wait

```bash
agent-browser wait @e1                     # Wait for element
agent-browser wait 2000                    # Wait milliseconds
agent-browser wait --text "Success"        # Wait for text
agent-browser wait --url "/dashboard"      # Wait for URL pattern
agent-browser wait --load networkidle      # Wait for network idle
agent-browser wait --fn "window.ready"     # Wait for JS condition
```

### Mouse control

```bash
agent-browser mouse move <x> <y>      # Move mouse
agent-browser mouse down [btn]        # Press button (left/right/middle)
agent-browser mouse up [btn]          # Release button
agent-browser mouse wheel <dy> [dx]   # Scroll wheel
```

### Browser settings

```bash
agent-browser set viewport <w> <h>         # Set viewport size
agent-browser set device <name>            # Emulate device (e.g., "iPhone 15 Pro")
agent-browser set geo <lat> <lng>          # Set geolocation
agent-browser set offline [on|off]         # Toggle offline mode
agent-browser set headers '<json>'         # Extra HTTP headers
agent-browser set credentials <user> <pass> # HTTP basic auth
agent-browser set media [dark|light] [reduced-motion]  # Emulate color scheme / motion preference
```

### Cookies & Storage

```bash
# Get / set / clear cookies
agent-browser cookies                              # Get all cookies
agent-browser cookies set <name> <value>           # Set cookie
agent-browser cookies set <name> <value> --url <u> --domain <d> --path <p>
agent-browser cookies set <name> <value> --httpOnly --secure --sameSite strict --expires <unix>
agent-browser cookies set --curl <file> [--domain <host>]  # Import from cURL/JSON/Cookie-header file
agent-browser cookies clear                        # Clear all cookies

# Web storage
agent-browser storage local                        # Get all localStorage
agent-browser storage local key                    # Get specific key
agent-browser storage local set <k> <v>            # Set value
agent-browser storage local clear                  # Clear all
agent-browser storage session                      # Same for sessionStorage
```

### Network

```bash
agent-browser network route <url>                    # Intercept requests
agent-browser network route <url> --abort            # Block requests
agent-browser network route <url> --body '<json>'    # Mock response
agent-browser network route <url> --resource-type <csv>  # Filter by resource type
agent-browser network unroute [url]                  # Remove routes
agent-browser network requests                       # View tracked requests
agent-browser network requests --filter <pattern>    # Filter requests
agent-browser network requests --clear               # Clear tracked requests
agent-browser network har start [path]               # Start HAR recording
agent-browser network har stop [path]                # Stop and save HAR
```

### Tabs

```bash
agent-browser tab                    # List tabs
agent-browser tab new [url]          # New tab
agent-browser tab <n>                # Switch to tab
agent-browser tab close              # Close tab
```

### JavaScript

```bash
agent-browser eval "<js>"            # Run JavaScript in page context
```

### Clipboard

```bash
agent-browser clipboard read         # Read clipboard text
agent-browser clipboard write <text> # Write text to clipboard
agent-browser clipboard copy         # Copy current selection
agent-browser clipboard paste        # Paste from clipboard
```

### State management

```bash
agent-browser state save <path>      # Save session state (cookies + storage)
agent-browser state load <path>      # Load saved state
```

State files can be encrypted with `AGENT_BROWSER_ENCRYPTION_KEY` (64-char hex AES-256-GCM key).

---

## Auth Vault

Securely store and replay credentials. Never pass passwords as CLI arguments — use the vault.

```bash
# Save credentials (prompts for password if not provided)
agent-browser auth save <name> --url <login-url> --username <user>
agent-browser auth save <name> --url <login-url> --username <user> --password <pass>
agent-browser auth save <name> --url <login-url> --username <user> --password-stdin

# Login using saved credentials (auto-detects form fields)
agent-browser auth login <name>

# Login with custom selectors
agent-browser auth login <name> --username-selector "#email" --password-selector "#pass"

# Login with credential provider plugin
agent-browser auth login <name> --credential-provider <plugin> [--item <ref>] [--url <url>]

# Manage profiles
agent-browser auth list              # List saved auth profiles
agent-browser auth show <name>       # Show profile metadata (no password)
agent-browser auth delete <name>     # Delete auth profile
```

---

## React DevTools Integration

Requires opening with `--enable react-devtools`:

```bash
agent-browser open <url> --enable react-devtools
```

```bash
agent-browser react tree                        # Full React component tree (depth, id, parent, name)
agent-browser react inspect <id>                # Inspect one fiber (props, hooks, state, source)
agent-browser react renders start               # Start recording re-renders
agent-browser react renders stop [--json]        # Stop and print render profile
agent-browser react suspense [--only-dynamic] [--json]  # Walk Suspense boundaries + classifier
```

---

## Performance (Core Web Vitals)

```bash
agent-browser vitals [url] [--json]   # Core Web Vitals (LCP, CLS, TTFB, FCP, INP)
                                      # + React hydration summary
```

Returns metrics with letter grades. `--json` returns full data for programmatic use.

---

## Streaming (WebSocket)

Stream browser events to external consumers in real-time:

```bash
agent-browser stream enable [--port <n>]   # Start runtime WebSocket streaming
agent-browser stream disable              # Stop streaming
agent-browser stream status               # Show streaming status and active port
```

---

## MCP Server Mode

Expose agent-browser as an MCP (Model Context Protocol) tool server via stdio:

```bash
agent-browser mcp
```

---

## Dashboard (Observability)

Start the web-based observability dashboard:

```bash
agent-browser dashboard [start]          # Start dashboard (default port: 4848)
agent-browser dashboard start --port <n> # Start on specific port
agent-browser dashboard stop             # Stop dashboard
```

---

## Plugins

```bash
agent-browser plugin add <ref>           # Add plugin from npm or GitHub
agent-browser plugin [list]              # List configured plugins
agent-browser plugin show <name>         # Show one plugin config
agent-browser plugin run <name> <type>   # Run a command.run or custom plugin request
```

---

## Diff (Page Comparison)

```bash
agent-browser diff snapshot              # Compare current vs last snapshot
agent-browser diff screenshot --baseline <path>  # Compare current vs baseline image
agent-browser diff url <u1> <u2>         # Compare two pages
```

---

## Sessions (parallel browsers)

```bash
agent-browser --session <name> open site-a.com    # Isolated session
agent-browser --session <name> open site-b.com    # Another isolated session
agent-browser session list                         # List active sessions
agent-browser session                              # Show current session name
```

### Session persistence (auto-save/restore state)

```bash
agent-browser --session-name myapp open example.com   # Auto-save/restore cookies + localStorage by name
```

State auto-saves on close and restores on next open with the same name. Controlled by `AGENT_BROWSER_STATE_EXPIRE_DAYS` (default: 30).

---

## Confirmation (Action Policy)

Require explicit approval for sensitive actions:

```bash
agent-browser confirm <id>               # Approve a pending action
agent-browser deny <id>                  # Deny a pending action
```

Configure categories requiring confirmation:

```bash
agent-browser --confirm-actions "navigate,download,upload" open example.com
agent-browser --confirm-interactive open example.com  # Interactive prompts (auto-denies if non-TTY)
```

Load policy from file:

```bash
agent-browser --action-policy policy.json open example.com
```

---

## Batch execution

Execute multiple commands sequentially in a single call:

```bash
agent-browser batch ["cmd1" "cmd2" "cmd3"]        # Execute sequentially (continue on error)
agent-browser batch --bail ["cmd1" "cmd2"]        # Stop on first error
echo 'open example.com\nsnapshot -i' | agent-browser batch   # Via stdin
```

---

## Init scripts

Register JavaScript that runs before first navigation:

```bash
agent-browser --init-script ./setup.js open example.com
agent-browser removeinitscript <id>    # Remove a registered script
```

Multiple scripts via `AGENT_BROWSER_INIT_SCRIPTS` env (comma-separated).

---

## JSON output (for parsing)

Add `--json` for machine-readable output:

```bash
agent-browser snapshot -i --json
agent-browser get text @e1 --json
agent-browser vitals --json
```

---

## Debugging

```bash
agent-browser open example.com --headed              # Show browser window
agent-browser console                                # View console messages
agent-browser console --clear                        # Clear console
agent-browser errors                                 # View page errors
agent-browser errors --clear                         # Clear errors
agent-browser highlight @e1                          # Highlight element
agent-browser inspect                                # Open Chrome DevTools for active page
agent-browser trace start                            # Start Chrome DevTools trace
agent-browser trace stop [path]                      # Stop and save trace
agent-browser profiler start                         # Start CPU profiling
agent-browser profiler stop [path]                   # Stop and save profile
agent-browser record start <path> [url]              # Record video (WebM)
agent-browser record stop                            # Save recording
agent-browser --cdp 9222 snapshot                    # Connect via CDP port
agent-browser --auto-connect snapshot                # Auto-discover running Chrome
```

---

## Chat (AI-driven)

Send natural language instructions to an AI model that controls the browser:

```bash
agent-browser chat "open google.com and search for cats"   # Single-shot
agent-browser chat                                        # Interactive REPL (TTY)
agent-browser chat --model <name> "summarize this page"   # Specific model
agent-browser -q chat "click the login button"            # Quiet mode (text only)
```

Requires `AI_GATEWAY_API_KEY` or equivalent model provider credentials.

---

## Examples

### Form submission

```bash
agent-browser open https://example.com/form
agent-browser snapshot -i
# Output shows: textbox "Email" [ref=e1], textbox "Password" [ref=e2], button "Submit" [ref=e3]

agent-browser fill @e1 "user@example.com"
agent-browser fill @e2 "password123"
agent-browser click @e3
agent-browser wait --load networkidle
agent-browser snapshot -i  # Check result
```

### Authentication with saved state

```bash
# Login once
agent-browser open https://app.example.com/login
agent-browser snapshot -i
agent-browser fill @e1 "username"
agent-browser fill @e2 "password"
agent-browser click @e3
agent-browser wait --url "/dashboard"
agent-browser state save auth.json

# Later sessions: load saved state
agent-browser state load auth.json
agent-browser open https://app.example.com/dashboard
```

### Authentication with vault (recommended)

```bash
# Save credentials once
agent-browser auth save myapp --url https://app.example.com/login --username user

# Use in any session
agent-browser auth login myapp
agent-browser wait --url "/dashboard"
```

### Next.js SPA navigation

```bash
agent-browser open http://localhost:3000/
agent-browser snapshot -i
# Click a link that triggers client-side nav
agent-browser click @e5
# OR use pushstate for known URLs
agent-browser pushstate http://localhost:3000/dashboard
agent-browser wait --load networkidle
agent-browser snapshot -i
```

### React debugging

```bash
agent-browser open http://localhost:3000/ --enable react-devtools
agent-browser react tree                    # See component tree
agent-browser react inspect 42              # Inspect fiber #42 (props, hooks, state)
agent-browser react renders start           # Record re-renders
# ... interact with page ...
agent-browser react renders stop            # See what re-rendered
agent-browser react suspense --only-dynamic # Find Suspense boundaries
```

### Performance audit

```bash
agent-browser open https://example.com
agent-browser vitals --json
# Returns: TTFB, FCP, LCP, CLS, INP + React hydration data
```

### Parallel sessions

```bash
agent-browser --session test1 open site-a.com
agent-browser --session test2 open site-b.com
agent-browser --session test1 snapshot -i
agent-browser --session test2 snapshot -i
agent-browser session list
```

### Connect to running Chrome

```bash
# Auto-discover and connect
agent-browser --auto-connect snapshot

# Connect via specific CDP port
agent-browser --cdp 9222 snapshot

# Save auth state from running Chrome
agent-browser --auto-connect state save ./auth.json
```

---

## Full Options Reference

### Session & Browser

| Flag | Description |
|---|---|
| `--session <name>` | Isolated session (or `AGENT_BROWSER_SESSION`) |
| `--session-name <name>` | Auto-save/restore state persistence name (or `AGENT_BROWSER_SESSION_NAME`) |
| `--profile <name\|path>` | Chrome profile to reuse login state, or custom profile directory (or `AGENT_BROWSER_PROFILE`) |
| `--state <path>` | Load saved auth state from JSON file (or `AGENT_BROWSER_STATE`) |
| `--auto-connect` | Connect to running Chrome to reuse auth state |
| `--headed` | Show browser window, not headless (or `AGENT_BROWSER_HEADED`) |
| `--executable-path <path>` | Custom browser executable (or `AGENT_BROWSER_EXECUTABLE_PATH`) |
| `--engine <name>` | Browser engine: `chrome` (default), `lightpanda` (or `AGENT_BROWSER_ENGINE`) |
| `--cdp <port>` | Connect via CDP port |

### Network & Security

| Flag | Description |
|---|---|
| `--proxy <server>` | Proxy server URL. Supports auth: `http://user:pass@host:port` (or `AGENT_BROWSER_PROXY`, `HTTP_PROXY`, `HTTPS_PROXY`, `ALL_PROXY`) |
| `--proxy-bypass <hosts>` | Bypass proxy for hosts (or `AGENT_BROWSER_PROXY_BYPASS`, `NO_PROXY`) |
| `--ignore-https-errors` | Ignore HTTPS certificate errors |
| `--headers <json>` | HTTP headers scoped to URL's origin |
| `--allow-file-access` | Allow `file://` URLs to access local files (Chromium only) |

### Appearance & Media

| Flag | Description |
|---|---|
| `--color-scheme <scheme>` | `dark`, `light`, `no-preference` (or `AGENT_BROWSER_COLOR_SCHEME`) |
| `--hide-scrollbars <bool>` | Hide native scrollbars in headless screenshots (default: `true`) |

### Output Control

| Flag | Description |
|---|---|
| `--json` | JSON output (or `AGENT_BROWSER_JSON`) |
| `--annotate` | Annotated screenshot with numbered labels (or `AGENT_BROWSER_ANNOTATE`) |
| `--content-boundaries` | Wrap page output in boundary markers (or `AGENT_BROWSER_CONTENT_BOUNDARIES`) |
| `--max-output <chars>` | Truncate page output to N chars (or `AGENT_BROWSER_MAX_OUTPUT`) |
| `--debug` | Debug output (or `AGENT_BROWSER_DEBUG`) |

### Screenshot Options

| Flag | Description |
|---|---|
| `--screenshot-dir <path>` | Default screenshot directory (or `AGENT_BROWSER_SCREENSHOT_DIR`) |
| `--screenshot-quality <n>` | JPEG quality 0-100 (or `AGENT_BROWSER_SCREENSHOT_QUALITY`) |
| `--screenshot-format <fmt>` | `png`, `jpeg` (or `AGENT_BROWSER_SCREENSHOT_FORMAT`) |

### Extensions & Scripts

| Flag | Description |
|---|---|
| `--extension <path>` | Load browser extension (repeatable) |
| `--init-script <path>` | Register page init script before first navigation (repeatable) |
| `--enable <feature>` | Built-in init scripts: `react-devtools` (repeatable or comma-separated) |
| `--args <args>` | Browser launch args, comma/newline separated (or `AGENT_BROWSER_ARGS`) |

### Safety & Policy

| Flag | Description |
|---|---|
| `--allowed-domains <list>` | Restrict navigation domains (or `AGENT_BROWSER_ALLOWED_DOMAINS`) |
| `--action-policy <path>` | Action policy JSON file (or `AGENT_BROWSER_ACTION_POLICY`) |
| `--confirm-actions <list>` | Categories requiring confirmation (or `AGENT_BROWSER_CONFIRM_ACTIONS`) |
| `--confirm-interactive` | Interactive confirmation prompts; auto-denies if non-TTY (or `AGENT_BROWSER_CONFIRM_INTERACTIVE`) |
| `--no-auto-dialog` | Disable automatic dismissal of alert/beforeunload dialogs (or `AGENT_BROWSER_NO_AUTO_DIALOG`) |

### Miscellaneous

| Flag | Description |
|---|---|
| `--user-agent <ua>` | Custom User-Agent (or `AGENT_BROWSER_USER_AGENT`) |
| `--download-path <path>` | Default download directory (or `AGENT_BROWSER_DOWNLOAD_PATH`) |
| `--model <name>` | AI model for chat (or `AI_GATEWAY_MODEL`) |
| `-v, --verbose` | Show tool commands and raw output |
| `-q, --quiet` | Show only AI text responses (hide tool calls) |
| `--config <path>` | Custom config file (or `AGENT_BROWSER_CONFIG`) |
| `--version, -V` | Show version |

### Provider Options

| Flag | Description |
|---|---|
| `-p, --provider <name>` | Browser provider: `ios`, `browserbase`, `kernel`, `browseruse`, `browserless`, `agentcore`, or plugin name |
| `--device <name>` | iOS device name (e.g., `"iPhone 15 Pro"`) |

---

## Environment Variables

| Variable | Description |
|---|---|
| `AGENT_BROWSER_CONFIG` | Path to config file |
| `AGENT_BROWSER_SESSION` | Session name (default: "default") |
| `AGENT_BROWSER_SESSION_NAME` | Auto-save/restore state persistence name |
| `AGENT_BROWSER_ENCRYPTION_KEY` | 64-char hex key for AES-256-GCM state encryption |
| `AGENT_BROWSER_STATE_EXPIRE_DAYS` | Auto-delete states older than N days (default: 30) |
| `AGENT_BROWSER_EXECUTABLE_PATH` | Custom browser executable path |
| `AGENT_BROWSER_EXTENSIONS` | Comma-separated browser extension paths |
| `AGENT_BROWSER_INIT_SCRIPTS` | Comma-separated page init script paths |
| `AGENT_BROWSER_ENABLE` | Comma-separated built-in init script features |
| `AGENT_BROWSER_HEADED` | Show browser window (not headless) |
| `AGENT_BROWSER_JSON` | JSON output |
| `AGENT_BROWSER_ANNOTATE` | Annotated screenshot with numbered labels |
| `AGENT_BROWSER_DEBUG` | Debug output |
| `AGENT_BROWSER_IGNORE_HTTPS_ERRORS` | Ignore HTTPS certificate errors |
| `AGENT_BROWSER_PROVIDER` | Browser provider |
| `AGENT_BROWSER_AUTO_CONNECT` | Auto-discover and connect to running Chrome |
| `AGENT_BROWSER_ALLOW_FILE_ACCESS` | Allow file:// URLs to access local files |
| `AGENT_BROWSER_HIDE_SCROLLBARS` | Hide scrollbars in headless screenshots (default: true) |
| `AGENT_BROWSER_COLOR_SCHEME` | Color scheme preference |
| `AGENT_BROWSER_DOWNLOAD_PATH` | Default download directory |
| `AGENT_BROWSER_DEFAULT_TIMEOUT` | Default action timeout in ms (default: 25000) |
| `AGENT_BROWSER_STREAM_PORT` | Override WebSocket streaming port (default: OS-assigned) |
| `AGENT_BROWSER_IDLE_TIMEOUT_MS` | Auto-shutdown daemon after N ms of inactivity (disabled by default) |
| `AGENT_BROWSER_IOS_DEVICE` | Default iOS device name |
| `AGENT_BROWSER_IOS_UDID` | Default iOS device UDID |
| `AGENT_BROWSER_CONTENT_BOUNDARIES` | Wrap page output in boundary markers |
| `AGENT_BROWSER_MAX_OUTPUT` | Max characters for page output |
| `AGENT_BROWSER_ALLOWED_DOMAINS` | Comma-separated allowed domain patterns |
| `AGENT_BROWSER_ACTION_POLICY` | Path to action policy JSON file |
| `AGENT_BROWSER_CONFIRM_ACTIONS` | Action categories requiring confirmation |
| `AGENT_BROWSER_CONFIRM_INTERACTIVE` | Enable interactive confirmation prompts |
| `AGENT_BROWSER_NO_AUTO_DIALOG` | Disable automatic dismissal of dialogs |
| `AGENT_BROWSER_ENGINE` | Browser engine: chrome (default), lightpanda |
| `AGENT_BROWSER_PLUGINS` | JSON plugin registry override |
| `AGENT_BROWSER_SCREENSHOT_DIR` | Default screenshot output directory |
| `AGENT_BROWSER_SCREENSHOT_QUALITY` | JPEG quality 0-100 |
| `AGENT_BROWSER_SCREENSHOT_FORMAT` | Screenshot format: png, jpeg |
| `AGENT_BROWSER_PROXY` | Proxy server URL |
| `AGENT_BROWSER_PROXY_BYPASS` | Bypass proxy for hosts |
| `HTTP_PROXY` / `HTTPS_PROXY` | Standard proxy env vars (fallback) |
| `ALL_PROXY` | SOCKS proxy (fallback) |
| `NO_PROXY` | Bypass proxy for hosts (fallback) |
| `AI_GATEWAY_URL` | Vercel AI Gateway base URL (default: https://ai-gateway.vercel.sh) |
| `AI_GATEWAY_API_KEY` | API key for AI Gateway (enables chat + dashboard AI) |
| `AI_GATEWAY_MODEL` | Default AI model (default: anthropic/claude-sonnet-4.6) |

---

## Configuration File

agent-browser looks for `agent-browser.json` in these locations (lowest to highest priority):

1. `~/.agent-browser/config.json` — User-level defaults
2. `./agent-browser.json` — Project-level overrides
3. Environment variables — Override config file values
4. CLI flags — Override everything

Use `--config <path>` to load a specific config file. Boolean flags accept `true`/`false` to override config:

```bash
--headed false     # Disables "headed": true from config
--hide-scrollbars false  # Keeps scrollbars visible
```

**Example `agent-browser.json`:**

```json
{
  "headed": true,
  "hideScrollbars": false,
  "proxy": "http://localhost:8080"
}
```

**Plugin config example:**

```json
{
  "plugins": [
    { "name": "vault", "command": "agent-browser-plugin-vault", "capabilities": ["credential.read"] },
    { "name": "stealth", "command": "agent-browser-plugin-stealth", "capabilities": ["launch.mutate"] }
  ]
}
```

Extensions from user and project configs are merged (not replaced).

---

## iOS Simulator (requires Xcode + Appium)

```bash
agent-browser -p ios open example.com                    # Default iPhone
agent-browser -p ios --device "iPhone 15 Pro" open url   # Specific device
agent-browser -p ios device list                         # List simulators
agent-browser -p ios swipe up                            # Swipe gesture
agent-browser -p ios tap @e1                             # Touch element
```

---

## Troubleshooting

| Issue | Solution |
|---|---|
| Command not found on Linux ARM64 | Use full path in the bin folder |
| Element not found | Use `snapshot` to find the correct ref |
| Page not loaded | Add `wait --load network idle` after navigation |
| Need to see the browser | Use `--headed` to show the window |
| Auth state lost between runs | Use `--session-name` or `state save/load` |
| Stale install | Run `agent-browser doctor --fix` |
| Need latest version | Run `agent-browser upgrade` |
| Cross-origin blocked in dev | Add origin to `allowedDevOrigins` in `next.config.ts` |
| HTTPS certificate errors | Use `--ignore-https-errors` |

## Notes

- Refs are stable per page load but change on navigation.
- Always snapshot after navigation to get new refs.
- Use `fill` instead of `type` for input fields to ensure existing text is cleared.
- `keyboard type` bypasses the selector system entirely — useful for non-input elements.
- `pushstate` is preferred over `open` for SPA routes to avoid full page reloads.
- State files auto-expire after `AGENT_BROWSER_STATE_EXPIRE_DAYS` (default: 30).
- Boolean flags accept optional `true`/`false` to override config file values.

## Reporting Issues

- **CLI issues:** https://github.com/vercel-labs/agent-browser
