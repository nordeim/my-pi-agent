---
name: htmx
description: "HTMX 2 (released 2024) hypermedia-driven web frontend workflow skill — HTML over the wire, no SPA framework needed. Covers the core mental model (HTML attributes drive AJAX, WebSocket, SSE, and DOM updates — hx-get, hx-post, hx-put, hx-delete, hx-swap, hx-target, hx-trigger, hx-vals, hx-headers), the swap modes (innerHTML, outerHTML, beforebegin, afterbegin, beforeend, afterend, delete, none — and hx-swap-oob for out-of-band updates), triggers (standard DOM events + custom events + polling via hx-trigger='every 2s' + delay/throttle modifiers + changed/once modifiers + from modifier for delegated events + consume modifier), HTMX 2's WebSocket and SSE support (hx-ws='connect:/chat' + hx-sse='connect:/events'), the extensions ecosystem (hx-ext='json-enc' for JSON requests, hx-ext='multi-swap', hx-ext='client-side-templates', hx-ext='path-params', hx-ext='response-targets', hx-ext='idiomorph' for morphdom-style swaps), the backend-agnostic design (pairs with Go/Ruby/Python/PHP/Java/Elixir — any backend that returns HTML fragments), the progressive enhancement story (HTMX is a progressive enhancement — content works without JS, gets better with it), the security model (HX-Request header for detecting HTMX requests, no built-in CSRF — use backend CSRF), and validation (HTML5 validation + hx-validate='true' for HTMX-aware validation). Use when building any server-rendered web app where React/Vue/Svelte would be overkill — CRUD apps, admin panels, content sites, dashboards — especially when the task involves hx-swap selection, hx-trigger composition, partial template rendering on the backend, or deciding between HTMX and a SPA framework where idiomatic HTMX (hypermedia over the wire) differs fundamentally from React/Vue (JSON API + client-side rendering)."
license: Proprietary. LICENSE.txt has complete terms
---

# HTMX 2 — Hypermedia-Driven Web Frontend

> **Target:** HTMX 2.0+ (released 2024) — a 14 KB JavaScript library (no dependencies) that extends HTML with attributes for AJAX, WebSocket, Server-Sent Events, and DOM updates. HTMX's philosophy: **HTML over the wire** — the server sends HTML fragments (not JSON), and HTMX swaps them into the page. No SPA framework, no client-side rendering, no JSON API layer. Pairs with ANY backend (Go, Ruby, Python, PHP, Java, Elixir).

## When to Use This Skill

Use this skill whenever the user is building, debugging, or extending a server-rendered web app with HTMX. Trigger phrases include "HTMX", "htmx.org", "hx-get", "hx-post", "hx-put", "hx-delete", "hx-swap", "hx-target", "hx-trigger", "hx-vals", "hx-headers", "hx-ws", "hx-sse", "hx-ext", "hx-swap-oob", "HX-Request", "HX-Target", "HX-Trigger", "idiomorph", "htmx extensions", "partial render", "fragment rendering", "HTML over the wire", "hypermedia", "progressive enhancement", and any reference to `<div hx-get="/users">` style attribute-driven interactivity.

Do **not** use this skill for:
- **HTMX 1.x** — the WebSocket/SSE API and some attribute syntax changed in 2.0. Migrate via the official guide.
- **React/Vue/Svelte apps** — different paradigm (client-side rendering with JSON APIs). HTMX is server-side rendering with HTML fragments.
- **Alpine.js / Stimulus** — these are lightweight JS frameworks for client-side interactivity. HTMX is for server-driven interactivity. They can be used together (Alpine for client-only state, HTMX for server-driven updates).
- **Pure static sites** — HTMX needs a server to fetch fragments from. For static sites, see `astro-5` skill.

Cross-reference: HTMX pairs naturally with `go-web`, `rails-8`, `django-6`, `laravel-12`, `phoenix-1-7`, `spring-boot-3`, `nestjs`, `fastapi-sqlalchemy`, `dotnet-9`. The backend renders HTML fragments; HTMX swaps them in.

## Quick Start

HTMX is a single JS file — no build step, no dependencies.

### Install via CDN (simplest)

```html
<!doctype html>
<html>
<head>
  <title>HTMX App</title>
  <script src="https://unpkg.com/htmx.org@2.0.3"></script>
  <!-- Or: <script src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.3/dist/htmx.min.js"></script> -->
</head>
<body>
  <h1>HTMX Demo</h1>

  <!-- Click the button → GET /click-count → response HTML swaps into #counter -->
  <button hx-get="/click-count" hx-target="#counter">Click Me</button>
  <div id="counter">0</div>

  <!-- Form submission → POST /submit → response swaps into #result -->
  <form hx-post="/submit" hx-target="#result">
    <input name="email" type="email" required>
    <button type="submit">Subscribe</button>
  </form>
  <div id="result"></div>
</body>
</html>
```

### Install via npm

```bash
npm install htmx.org
```

```javascript
// src/main.js
import 'htmx.org';
```

### Key concepts in 30 seconds

- `hx-get="/url"` — fetch HTML from `/url` on click, swap into target
- `hx-target="#id"` — where to swap the response (`#id`, `.class`, `closest div`, `next div`, `this`)
- `hx-swap="innerHTML"` — how to swap (innerHTML, outerHTML, beforeend, afterbegin, delete, none, etc.)
- `hx-trigger="click"` — what triggers the request (click, change, keyup, submit, load, etc.)
- The server returns **HTML fragments** (not JSON) — HTMX swaps them in

That's it. No client-side state, no JSON serialization, no virtual DOM. The server is the source of truth.

---

## Core Mental Model: HTML Over the Wire + Progressive Enhancement + Backend-Agnostic

HTMX's distinctive paradigm is **the server sends HTML fragments, HTMX swaps them into the DOM.** Three things differentiate HTMX from React/Vue/Svelte:

### 1. HTML over the wire (no JSON API)

```html
<!-- React/Vue approach: -->
<!-- 1. Frontend calls JSON API: GET /api/users/42 -->
<!-- 2. API returns: { "id": 42, "name": "Alice", "email": "alice@example.com" } -->
<!-- 3. Frontend renders: <div id="user"><h1>Alice</h1><p>alice@example.com</p></div> -->

<!-- HTMX approach: -->
<!-- 1. HTMX calls HTML endpoint: GET /users/42/fragment -->
<!-- 2. Server returns: <h1>Alice</h1><p>alice@example.com</p> -->
<!-- 3. HTMX swaps it into #user -->

<div id="user" hx-get="/users/42/fragment" hx-trigger="load">
  Loading...
</div>
```

The server renders a **partial template** (EJS, ERB, Jinja, Blade, etc.) and returns just the HTML fragment. HTMX swaps it into the target element. No JSON, no client-side rendering, no state management.

**Why this is powerful:**
- The server is the single source of truth (no client/server state sync issues)
- The server can use its full templating engine (loops, conditionals, helpers, partials)
- The payload is HTML — smaller than equivalent JSON + JS rendering code for simple cases
- No client-side build step (no Webpack, no Vite, no Babel)
- Works without JavaScript (progressive enhancement — see below)

### 2. Progressive enhancement (works without JS)

```html
<!-- This form works WITHOUT JavaScript -->
<form action="/subscribe" method="POST">
  <input name="email" type="email" required>
  <button type="submit">Subscribe</button>
</form>

<!-- With HTMX, enhance it to submit via AJAX and swap the result -->
<form hx-post="/subscribe" hx-target="#result">
  <input name="email" type="email" required>
  <button type="submit">Subscribe</button>
</form>
<div id="result"></div>
```

Without JavaScript, the form submits normally (full page reload). With JavaScript, HTMX intercepts the submit, sends it via AJAX, and swaps the response into `#result`. The form degrades gracefully.

This is the opposite of React/Vue — those frameworks don't render anything without JavaScript. HTMX apps work in no-JS environments (accessibility tools, screen readers, slow connections).

### 3. Backend-agnostic (use ANY server)

HTMX doesn't care what backend you use. The only contract: the server returns HTML fragments when HTMX requests come in.

```go
// Go (net/http or chi or Echo or Gin)
func userFragment(w http.ResponseWriter, r *http.Request) {
    user := getUser(r.PathValue("id"))
    tmpl := `<h1>{{.Name}}</h1><p>{{.Email}}</p>`
    t := template.Must(template.New("user").Parse(tmpl))
    t.Execute(w, user)
}
```

```python
# Python (Flask)
@app.route("/users/<id>/fragment")
def user_fragment(id):
    user = get_user(id)
    return render_template("user_fragment.html", user=user)
```

```ruby
# Ruby (Rails)
def fragment
  @user = User.find(params[:id])
  render partial: "users/user", locals: { user: @user }
end
```

```php
// PHP (Laravel)
public function fragment($id)
{
    $user = User::findOrFail($id);
    return view('users._user_fragment', ['user' => $user]);
}
```

```elixir
# Elixir (Phoenix)
def fragment(conn, %{"id" => id}) do
  user = Blog.get_user!(id)
  render(conn, "user_fragment.html", user: user)
end
```

The backend renders a partial template and returns it as HTML. HTMX swaps it in. That's the entire integration.

---

## The HTMX Attributes (memorize these)

### Request attributes

| Attribute | Method | Use |
|---|---|---|
| `hx-get="/url"` | GET | Fetch and swap |
| `hx-post="/url"` | POST | Submit data, swap response |
| `hx-put="/url"` | PUT | Update, swap response |
| `hx-patch="/url"` | PATCH | Partial update, swap response |
| `hx-delete="/url"` | DELETE | Delete, swap response |

### Target + Swap

| Attribute | Values | Use |
|---|---|---|
| `hx-target` | `#id`, `.class`, `closest div`, `next div`, `previous div`, `this` (default) | Where to put the response |
| `hx-swap` | `innerHTML` (default), `outerHTML`, `beforebegin`, `afterbegin`, `beforeend`, `afterend`, `delete`, `none` | How to insert the response |
| `hx-select` | CSS selector | Use only part of the response (e.g., `hx-select="#main"` to extract just `#main` from a full page) |
| `hx-swap-oob` | `true`, `#id`, `.class` | Out-of-band swap — update elements outside the target (see below) |

### Trigger

| Attribute | Example | Use |
|---|---|---|
| `hx-trigger` | `click` (default for buttons), `submit` (default for forms), `change` (default for inputs), `load`, `revealed`, `keyup`, `keydown`, `input`, `change` | What fires the request |
| `hx-trigger` | `click delay:500ms` | Debounce (wait 500ms after click) |
| `hx-trigger` | `keyup throttle:500ms` | Throttle (max once per 500ms) |
| `hx-trigger` | `change` | On input change (default for `<input>`, `<select>`, `<textarea>`) |
| `hx-trigger` | `every 2s` | Poll every 2 seconds |
| `hx-trigger` | `load delay:1s` | 1 second after page load |
| `hx-trigger` | `revealed` | When scrolled into view (lazy load) |
| `hx-trigger` | `click once` | Only trigger once |
| `hx-trigger` | `click changed` | Only if value changed |
| `hx-trigger` | `click from:#other` | Trigger when `#other` is clicked (event delegation) |
| `hx-trigger` | `click consume` | Prevent event bubbling |
| `hx-trigger` | `keyup[keyCode==13]` | Only on Enter key (filter modifier) |
| `hx-trigger` | `customEvent` | Listen for custom events (`htmx:trigger`) |

### Values + Headers

| Attribute | Example | Use |
|---|---|---|
| `hx-vals` | `{"key":"value"}` or `js:{key: getValue()}` | Add form values to the request |
| `hx-headers` | `{"X-Header":"value"}` | Add custom headers |
| `hx-params` | `*`, `none`, `name1,name2`, `not name1` | Which form fields to include |
| `hx-include` | `#form1, #form2` | Include other forms' values |
| `hx-disable` | (no value) | Disable HTMX on this element |
| `hx-disinherit` | `hx-target hx-swap` | Don't inherit these attributes to children |
| `hx-encoding` | `multipart/form-data` | For file uploads |
| `hx-preserve` | `true` | Don't swap this element (preserve video state, etc.) |
| `hx-validate` | `true` | Trigger HTML5 validation before request |

---

## Common Patterns

### Inline edit (click to edit)

```html
<span hx-get="/users/42/edit" hx-target="this" hx-swap="outerHTML">
  Alice
</span>

<!-- Server returns: -->
<!-- <form hx-put="/users/42" hx-target="this" hx-swap="outerHTML"> -->
<!--   <input name="name" value="Alice"> -->
<!--   <button type="submit">Save</button> -->
<!--   <button hx-get="/users/42" hx-target="this" hx-swap="outerHTML">Cancel</button> -->
<!-- </form> -->
```

Click the name → fetch an edit form → swap it in → submit updates → swap back to display.

### Live search (debounced input)

```html
<input
  type="search"
  name="q"
  placeholder="Search..."
  hx-get="/search"
  hx-trigger="keyup changed delay:300ms"
  hx-target="#results"
  hx-select="#results"
>
<div id="results">
  <!-- Search results swap in here -->
</div>
```

- `keyup` — fires on every key press
- `changed` — only if the value changed
- `delay:300ms` — wait 300ms after the last keypress (debounce)
- `hx-select="#results"` — extract just `#results` from the response (in case the server returns a full page)

### Infinite scroll

```html
<div id="posts" hx-get="/posts?page=1" hx-trigger="revealed" hx-swap="beforeend">
  <!-- Posts load here, and when this div is revealed, fetch more -->
</div>

<!-- Server returns the next page of posts PLUS a sentinel: -->
<!-- <div class="post">...</div> -->
<!-- <div class="post">...</div> -->
<!-- <div hx-get="/posts?page=2" hx-trigger="revealed" hx-swap="beforeend"></div> -->
```

The sentinel div has `hx-trigger="revealed"` — when it scrolls into view, it fetches the next page and appends it (`hx-swap="beforeend"`). The response includes a new sentinel for the next page. This creates infinite scroll with no JavaScript.

### Delete with confirmation

```html
<button
  hx-delete="/posts/42"
  hx-target="closest .post"
  hx-swap="outerHTML"
  hx-confirm="Are you sure you want to delete this post?"
>
  Delete
</button>

<!-- Server returns: empty response with 200 status -->
<!-- The .post element is removed from the DOM -->
```

### Out-of-band swaps (update multiple elements)

```html
<button hx-post="/like/42" hx-target="this">
  Like (<span id="like-count-42">5</span>)
</button>

<!-- Server response: -->
<!-- <button hx-swap-oob="true" id="like-button-42">Liked!</button> -->
<!-- <span hx-swap-oob="true" id="like-count-42">6</span> -->
<!-- <div hx-swap-oob="true" id="notification">Post liked!</div> -->
```

The button is the target (swapped normally). The other elements (`#like-count-42`, `#notification`) have `hx-swap-oob="true"` — they're updated even though they're outside the target. This lets one request update multiple parts of the page.

### Polling (live updates)

```html
<div hx-get="/notifications" hx-trigger="every 10s" hx-swap="innerHTML">
  <!-- Notifications swap in every 10 seconds -->
</div>
```

For real-time without polling, use WebSocket or SSE (below).

### Loading indicators

```html
<button hx-get="/slow-endpoint" hx-indicator="#spinner">
  Fetch Data
</button>
<span id="spinner" class="htmx-indicator">
  Loading...
</span>

<style>
.htmx-indicator { display: none; }
.htmx-request .htmx-indicator { display: inline; }
/* HTMX adds .htmx-request to the element while a request is in flight */
</style>
```

---

## WebSocket + SSE (HTMX 2)

### WebSocket

```html
<!-- Connect to a WebSocket -->
<div hx-ext="ws" ws-connect="/chat">
  <!-- Messages from the server swap in here -->
  <div id="messages"></div>

  <!-- Send a message -->
  <form ws-send>
    <input name="message" type="text">
    <button type="submit">Send</button>
  </form>
</div>

<script src="https://unpkg.com/htmx.org/dist/ext/ws.js"></script>
```

The server sends HTML fragments over the WebSocket — they swap into `#messages`. The form's `ws-send` attribute sends form data as a WebSocket message (serialized as JSON or form-encoded).

### Server-Sent Events (SSE)

```html
<div hx-ext="sse" sse-connect="/events">
  <!-- Listen for 'new-post' events -->
  <div sse-swap="new-post" hx-target="this" hx-swap="beforeend">
    <!-- New post HTML swaps in here -->
  </div>

  <!-- Listen for 'notification' events -->
  <div sse-swap="notification">
    <!-- Notification HTML swaps in here -->
  </div>
</div>

<script src="https://unpkg.com/htmx.org/dist/ext/sse.js"></script>
```

The server sends SSE events with named types (`new-post`, `notification`). HTMX listens for those events and swaps the event data into the matching elements. This is the modern replacement for polling — server pushes updates, client renders them.

---

## Extensions

HTMX has an extension system for adding functionality. Load the extension script, then enable via `hx-ext`.

### Common extensions

```html
<!-- JSON encoding (send JSON instead of form-encoded) -->
<script src="https://unpkg.com/htmx.org/dist/ext/json-enc.js"></script>
<div hx-ext="json-enc" hx-post="/api" hx-vals='{"key":"value"}'>
  <!-- Sends: POST /api with Content-Type: application/json and body {"key":"value"} -->
</div>

<!-- Multi-swap (swap multiple elements via CSS selectors) -->
<script src="https://unpkg.com/htmx.org/dist/ext/multi-swap.js"></script>
<div hx-ext="multi-swap" hx-get="/page" hx-swap="multi:#header:outerHTML, #main:innerHTML">
  <!-- Server returns full page, multi-swap extracts #header and #main and swaps them -->
</div>

<!-- Client-side templates (Mustache, Handlebars, etc.) -->
<script src="https://unpkg.com/htmx.org/dist/ext/client-side-templates.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/mustache.js/4.2.0/mustache.min.js"></script>
<div hx-ext="client-side-templates" hx-get="/api/data" hx-template="my-template">
  <!-- Fetches JSON, renders via Mustache template, swaps in -->
</div>

<!-- Path params -->
<script src="https://unpkg.com/htmx.org/dist/ext/path-params.js"></script>
<div hx-ext="path-params" hx-get="/users/{id}" hx-vals='{"id": 42}'>
  <!-- Replaces {id} in the URL with 42 → GET /users/42 -->
</div>

<!-- Response targets (different targets for different status codes) -->
<script src="https://unpkg.com/htmx.org/dist/ext/response-targets.js"></script>
<form hx-ext="response-targets"
      hx-post="/submit"
      hx-target="#success"
      hx-target-4xx="#errors"
      hx-target-5xx="#server-errors">
  <!-- 2xx → #success, 4xx → #errors, 5xx → #server-errors -->
</form>

<!-- Idiomorph (morphdom-style DOM diffing — preserves state in inputs, scroll, etc.) -->
<script src="https://unpkg.com/htmx.org/dist/ext/idiomorph.js"></script>
<div hx-ext="idiomorph" hx-get="/refresh" hx-swap="morph:outerHTML">
  <!-- Morphs the DOM (diffs and patches) instead of replacing it — preserves focus, scroll, etc. -->
</div>
```

The `idiomorph` extension (developed by the HTMX team) is particularly powerful — it does DOM morphing (like `morphdom` or React's reconciliation) instead of wholesale replacement. This preserves input focus, scroll position, and component state across swaps.

---

## Backend Integration Patterns

### Detecting HTMX requests

HTMX sends specific headers you can check on the backend:

```
HX-Request: true                    # Always sent for HTMX requests
HX-Target: #main                    # The id of the target element
HX-Trigger: submit-btn              # The id of the triggering element
HX-Trigger-Name: submit             # The name of the triggering element
HX-Prompt: <user input>             # If hx-prompt was used
HX-Current-URL: https://...         # The current page URL
```

```python
# Python (Flask) — render full page or fragment based on HTMX header
@app.route("/users/42")
def user_page():
    user = get_user(42)
    if request.headers.get("HX-Request"):
        # HTMX request — return just the fragment
        return render_template("users/_user_fragment.html", user=user)
    else:
        # Normal request — return full page
        return render_template("users/show.html", user=user)
```

```ruby
# Ruby (Rails) — same pattern
def show
  @user = User.find(params[:id])
  if request.headers["HX-Request"]
    render partial: "users/user", locals: { user: @user }
  else
    render :show
  end
end
```

This is the canonical pattern: one route handles both full-page loads (no JS, direct navigation, SEO crawlers) and HTMX fragment requests (AJAX-driven updates).

### Triggering client-side events from the server

The server can send `HX-Trigger` headers to trigger client-side events:

```python
# Python (Flask)
@app.route("/posts", methods=["POST"])
def create_post():
    post = create_post_from_form(request.form)
    response = make_response(render_template("posts/_post.html", post=post))
    response.headers["HX-Trigger"] = json.dumps({
        "postCreated": post.id,    # Trigger a 'postCreated' event with the post ID
        "showToast": "Post created successfully!"
    })
    return response
```

```html
<!-- Client listens for the events -->
<body hx-on:postCreated="alert('Post ' + event.detail + ' created!')">
  <div hx-on:showToast="alert(event.detail)">
    <!-- Toast appears here -->
  </div>
</body>
```

This is the HTMX way to do "after a successful submit, show a toast" — the server tells the client what happened via the `HX-Trigger` header, and the client listens via `hx-on:` attributes.

### Redirects

HTMX follows redirects automatically, but for full-page redirects (e.g., after login), use the `HX-Redirect` header:

```python
@app.route("/login", methods=["POST"])
def login():
    if authenticate(request.form):
        response = make_response("")
        response.headers["HX-Redirect"] = "/dashboard"   # Full page redirect
        return response
    else:
        return render_template("login/_errors.html", error="Invalid credentials")
```

---

## Validation

### HTML5 validation (built-in)

```html
<form hx-post="/submit" hx-validate="true">
  <input name="email" type="email" required>          <!-- HTML5 validation -->
  <input name="age" type="number" min="18" max="120" required>
  <button type="submit">Submit</button>
</form>
```

With `hx-validate="true"`, HTMX respects HTML5 validation — the request only fires if all fields pass validation. No JavaScript needed.

### Server-side validation (return error fragments)

```python
# Python (Flask)
@app.route("/submit", methods=["POST"])
def submit():
    errors = validate_form(request.form)
    if errors:
        return render_template("form/_errors.html", errors=errors), 422   # 422 Unprocessable Entity
    else:
        return render_template("form/_success.html")
```

```html
<form hx-post="/submit" hx-target="#result" hx-target-4xx="#errors">
  <!-- ... -->
</form>
<div id="errors"></div>
<div id="result"></div>
```

With the `response-targets` extension, 4xx responses swap into `#errors`, 2xx responses swap into `#result`.

---

## Security

### CSRF protection

HTMX sends AJAX requests with standard form encoding — same as a normal form submit. This means **your existing CSRF protection works** (Rails, Django, Laravel all have built-in CSRF that protects HTMX requests automatically).

```html
<!-- Rails example: csrf_meta_tag inserts the CSRF token -->
<%= csrf_meta_tags %>

<!-- HTMX automatically includes the CSRF token from the meta tag (via the meta extension) -->
<script src="https://unpkg.com/htmx.org/dist/ext/ajax-header.js"></script>
<div hx-ext="ajax-header">
  <!-- All HTMX requests include X-CSRF-Token header from the meta tag -->
</div>
```

### The `HX-Request` header is NOT a security boundary

Don't rely on `HX-Request: true` for authz — anyone can send that header. Use real authentication (session cookies, JWT tokens).

### XSS protection

HTMX swaps HTML into the DOM via `innerHTML` by default. If the server-rendered HTML contains user input, it must be escaped (every templating engine does this by default — Jinja, ERB, Blade, EEx all auto-escape). Don't disable auto-escaping for fragment rendering.

---

## Testing

### End-to-end tests (Playwright)

HTMX apps are testable with standard browser testing tools:

```typescript
import { test, expect } from '@playwright/test';

test('inline edit updates name', async ({ page }) => {
  await page.goto('/users/42');

  await page.click('text=Alice');
  await page.fill('input[name="name"]', 'Alice Smith');
  await page.click('text=Save');

  await expect(page.locator('text=Alice Smith')).toBeVisible();
});
```

### Server-side tests (render the fragment)

```python
# Python (pytest + Flask)
def test_user_fragment(client):
    response = client.get('/users/42/fragment', headers={'HX-Request': 'true'})
    assert response.status_code == 200
    assert b'Alice' in response.data
```

Cross-reference: `testing-patterns` for general test pyramid / mocking strategies.

---

## When to Choose HTMX vs React/Vue/Svelte

| Use HTMX when | Use React/Vue/Svelte when |
|---|---|
| Server-rendered app (CRUD, admin panel, dashboard) | Rich client-side interactivity (drag-and-drop, complex forms, real-time editing) |
| You have a backend team but no frontend team | You have a dedicated frontend team |
| SEO matters (content renders without JS) | SEO doesn't matter (logged-in app) |
| You want progressive enhancement | You're OK with JS-required |
| The app is mostly read-heavy with simple writes | The app has complex client-side state |
| You want to avoid the SPA complexity tax | You need offline support or PWA features |
| You're using Go/Ruby/Python/PHP/Elixir on the backend | You're using Next.js/Nuxt/SvelteKit (full-stack JS) |

**The HTMX sweet spot:** 80% of business apps are CRUD with some interactivity. HTMX handles this with 1/10th the complexity of a SPA. Save the SPA for the 20% that genuinely needs client-side state (drag-and-drop editors, real-time collaboration, complex visualization).

---

## Top 10 Anti-Patterns (the most valuable section)

1. **Treating HTMX like a SPA framework.** HTMX is server-driven. Don't try to manage client-side state, do client-side routing, or build "components" with complex lifecycle. If you need that, use React/Vue. HTMX is for server-rendered apps with progressive enhancement.

2. **Not using `hx-swap-oob` for multi-element updates.** When a single request should update multiple parts of the page (e.g., like count + notification + button label), use `hx-swap-oob="true"` on the additional elements in the response. Don't fire multiple requests — one request, multiple updates via OOB swaps.

3. **Returning JSON from the server.** HTMX expects HTML fragments. If you return JSON, HTMX will swap the raw JSON string into the DOM. Either render the HTML on the server (preferred), or use the `client-side-templates` extension to render JSON client-side (but then you're reinventing React).

4. **Not handling the `HX-Request` header for full-page fallbacks.** If a user navigates directly to `/users/42` (no JS, or shares a URL), they should get the full page, not just the fragment. Check `HX-Request` on the server and render appropriately. Without this, deep links break.

5. **Using `hx-trigger="every 1s"` for everything.** Polling is wasteful. Use SSE (`sse-connect`) or WebSocket (`ws-connect`) for true real-time. Reserve polling for cases where SSE isn't available (e.g., the backend doesn't support it).

6. **Not using `delay` or `throttle` on input-triggered requests.** `hx-trigger="keyup"` without `delay:300ms` fires a request on every keypress — DDoS your own server. Always debounce (`delay`) for search inputs, throttle for scroll/resize.

7. **Forgetting `hx-target`.** Without `hx-target`, the response swaps into the element itself (often the button or input). Usually you want it to swap into a separate results container. Always specify `hx-target="#results"` explicitly.

8. **Not using `hx-select` when the server returns a full page.** If the server returns a full HTML page (with `<html>`, `<head>`, `<body>`), HTMX swaps the entire page into the target — usually broken. Use `hx-select="#main"` to extract just the relevant fragment from the response.

9. **Disabling auto-escaping in templates.** HTMX swaps HTML via `innerHTML`. If your server-rendered HTML contains unescaped user input, it's an XSS vulnerability. Every templating engine auto-escapes by default — don't disable it with `| safe` (Jinja), `{!! !!}` (Blade), or `raw` (ERB) unless you have a specific reason and have sanitized the input.

10. **Reaching for client-side JS when HTMX can do it.** HTMX handles most interactivity: inline edit, infinite scroll, live search, modals, tabs, accordions, form validation, file uploads, real-time updates. Before writing custom JavaScript, check if HTMX has an attribute for it. The less JS you write, the simpler the app.

---

## Cross-references

- `framework-templates` — CLAUDE.md generation template for HTMX (project onboarding)
- `go-web` — Go web backend (renders HTML fragments for HTMX)
- `rails-8` — Ruby on Rails (Hotwire/Turbo is similar to HTMX — but HTMX is framework-agnostic)
- `django-6` — Python Django (renders HTML fragments for HTMX)
- `laravel-12` — PHP Laravel (renders Blade partials for HTMX)
- `phoenix-1-7` — Elixir Phoenix (LiveView is similar to HTMX but framework-specific)
- `spring-boot-3` — Java Spring Boot (Thymeleaf fragments for HTMX)
- `nestjs` — TypeScript NestJS (renders template fragments for HTMX)
- `fastapi-sqlalchemy` — Python FastAPI (Jinja2 templates for HTMX)
- `dotnet-9` — .NET ASP.NET Core (Razor Pages partials for HTMX)
- `frontend-ui-engineering` — Production-quality UI build patterns
- `api-and-interface-design` — Type contract design (HTMX endpoints are HTML, not JSON — different contract)
- `security-and-hardening` — OWASP-aware hardening (CSRF works with HTMX; XSS requires escaped templates)
- `clean-code` — General coding standards
- `testing-patterns` — Test pyramid, mocking strategies
- `code-review-checklist` — 12-category code review checklist

---

## Dependencies

Required:
- **HTMX** 2.0+ — install via CDN (`<script src="https://unpkg.com/htmx.org@2.0.3">`) or npm (`npm install htmx.org`)
- **A backend** that renders HTML fragments — any of:
  - Go: `net/http`, chi, Echo, Gin (render HTML templates)
  - Ruby: Rails (render partials), Sinatra
  - Python: Flask, Django (render templates), FastAPI (Jinja2Templates)
  - PHP: Laravel (Blade partials), Symfony
  - Java: Spring Boot (Thymeleaf fragments)
  - Elixir: Phoenix (render templates)
  - C#: ASP.NET Core (Razor Pages partials)
  - Node.js: Express, Hono, NestJS (render template engines)

### Official extensions (load via CDN)

- `ext/ws.js` — WebSocket support
- `ext/sse.js` — Server-Sent Events support
- `ext/json-enc.js` — JSON request encoding
- `ext/multi-swap.js` — Multiple element swaps
- `ext/client-side-templates.js` — Mustache/Handlebars client-side rendering
- `ext/path-params.js` — URL path parameter substitution
- `ext/response-targets.js` — Different targets for different status codes
- `ext/idiomorph.js` — DOM morphing (preserves state)
- `ext/ajax-header.js` — Auto-include headers from meta tags (CSRF)
- `ext/preload.js` — Preload links on hover
- `ext/class-tools.js` — Add/remove classes on events
- `ext/loading-states.js` — Loading state management
- `ext/remove-me.js` — Auto-remove element after delay

### Common additions

- **Alpine.js** (`<script src="https://unpkg.com/alpinejs">`) — for client-only interactivity that doesn't need the server (toggles, dropdowns, tabs). Pairs well with HTMX — Alpine for client state, HTMX for server-driven updates.
- **Tailwind CSS** — styling (via CDN or build step)
- **DaisyUI** — Tailwind component library (works perfectly with HTMX)
- **PicoCSS** — classless CSS framework (minimal, works with semantic HTML)
- **htmx.org/hyperscript** — `_` attribute for small client-side scripts (HTMX team project, optional)
