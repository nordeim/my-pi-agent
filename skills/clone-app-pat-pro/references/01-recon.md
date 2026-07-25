# Stage 1: Recon — detailed instructions

These instructions are injected AFTER the Stage-1 prompt in `stage-prompts.md`. They obey `00-contract.md` (the authoritative contract). Where this file and the contract disagree, the contract wins.

You are recon for **ONE route at ONE viewport**, driven IN-CONVERSATION by the live Claude session. Recon captures the **real, logged-in** site, so it runs through the **Claude Chrome extension** (`mcp__claude-in-chrome__*`) — you're already authed in Chrome. There is ONE Chrome and ONE tab: do recon sequentially (one route×viewport at a time), never two browser actions at once. Your inputs are `PAGE={PAGE}` and `VIEWPORT={VIEWPORT}` (already substituted by the orchestrator), plus the target URL and the workspace name `{NAME}` from `00-config.json`.

Your full-page screenshot is the **pixel-diff baseline** for QA (contract §5) — if it is half-rendered, blank, or the wrong size, the entire downstream gate is poisoned. Capture it correctly or BLOCK. Never fabricate a route, a theme, or a framework from memory (contract §7 anti-hallucination).

---

## Tool: Claude Chrome extension (`mcp__claude-in-chrome__*`)

Run everything through the Chrome extension MCP tools — the real authed site lives in your own Chrome. Single Chrome, one tab at a time, sequential: there is no `--session` isolation to set, because there are no concurrent browser agents racing one tab.

The tools you use (see contract §11 for the save-to-file rule):

```
mcp__claude-in-chrome__navigate        # open a route in the current tab
mcp__claude-in-chrome__resize_window   # set the viewport to exact pixels
mcp__claude-in-chrome__computer        # screenshot (visual reference only), hover, left_click, focus
mcp__claude-in-chrome__javascript_tool # run JS in the page, returns the expression's value as JSON
mcp__claude-in-chrome__read_page       # accessibility/DOM snapshot of interactive elements
mcp__claude-in-chrome__find            # locate an element/ref on the page
```

Capture screenshots with `mcp__claude-in-chrome__computer` action `screenshot` for a visual reference of the route (the file cannot be reliably saved to disk in this environment, so treat the shot as a visual aid, not a workspace artifact). The ground truth for verification is the computed styles you read via `mcp__claude-in-chrome__javascript_tool`. Do NOT use Playwright MCP or SSH.

Viewport pixels (contract §1):

| `{VIEWPORT}` | width | height |
|--------------|-------|--------|
| `desktop`    | 1920  | 1080   |
| `tablet`     | 768   | 1024   |
| `mobile`     | 375   | 667    |

Set the viewport with raw pixels via `mcp__claude-in-chrome__resize_window` (e.g. `768`×`1024`), not device emulation, so dimensions are identical to the QA clone shot for a 1:1 diff.

---

## Page-slug rule (contract §1)

Derive `{page-slug}` from `{PAGE}` deterministically:
- `/` → `home`
- `/pricing` → `pricing`
- `/blog/post` → `blog-post`
- lowercase, every run of non-alphanumeric chars → a single `-`, trim leading/trailing `-`.

Every file you write uses this slug. Get it right or the baseline won't line up with the QA shot.

---

## Step 1 — Open, size, and FULLY hydrate

1. `mcp__claude-in-chrome__resize_window` → set the window to YOUR `{VIEWPORT}`'s exact pixels (e.g. `1920`×`1080`).
2. `mcp__claude-in-chrome__navigate` → the target URL for `{PAGE}`.

Modern targets are JS-heavy SPAs. **Do not screenshot a half-rendered page.** Poll for hydration — do not trust a fixed sleep. Loop until the DOM settles (text is present, the body has real height, and no skeleton/spinner remains), with a hard cap. Re-run this `mcp__claude-in-chrome__javascript_tool` call until it returns true (max ~12s):

```js
  (() => {
    const b = document.body;
    if (!b) return false;
    const txt = (b.innerText || '').trim().length;
    const tall = document.documentElement.scrollHeight > window.innerHeight * 0.9;
    const skeleton = document.querySelector(
      '[class*=skeleton i],[class*=shimmer i],[class*=placeholder i],[aria-busy=true],.spinner,[class*=loading i]'
    );
    // React/Next/Vue mounted markers, if present
    const reactRoot = document.querySelector('#__next,#root,[data-reactroot]');
    const mounted = !reactRoot || reactRoot.childElementCount > 0;
    return txt > 30 && tall && !skeleton && mounted;
  })()
```

After hydration looks true, give web fonts and lazy media a final beat so the baseline is deterministic. Run via `mcp__claude-in-chrome__javascript_tool`:

```js
document.fonts.ready.then(()=>true)
```

```js
  (async () => {
    const imgs = Array.from(document.images);
    await Promise.all(imgs.map(i => i.complete ? 0 : i.decode().catch(()=>0)));
    // nudge lazy content into view, then return to top
    window.scrollTo(0, document.body.scrollHeight);
    await new Promise(r => setTimeout(r, 400));
    window.scrollTo(0, 0);
    await new Promise(r => setTimeout(r, 200));
    return true;
  })()
```

---

## Step 2 — AUTH CHECK (do this BEFORE any capture)

Recon runs against the **logged-in** site, so you should normally already be authed in this Chrome. But if the route still bounced to a login/paywall or rendered nothing, there is nothing to clone. Detect it, then **stop** — do not burn the pipeline diffing a login screen (contract §6 auth-wall, §7 anti-hallucination). Run via `mcp__claude-in-chrome__javascript_tool`:

```js
  (() => {
    const url = location.href.toLowerCase();
    const redirected = /\\/login|\\/signin|\\/sign-in|\\/auth|\\/account\\/login|\\/sso|\\/paywall/.test(url);
    const txt = (document.body?.innerText || '').toLowerCase();
    const hasPw = !!document.querySelector('input[type=password]');
    const wallWords = /(log ?in|sign ?in|subscribe to continue|create an account|members only|please authenticate|403 forbidden|401 unauthorized|access denied)/.test(txt);
    const blank = (document.body?.innerText || '').trim().length < 20;
    return { url: location.href, redirected, hasPw, wallWords, blank,
             blocked: redirected || (hasPw && wallWords) || blank };
  })()
```

If `blocked` is true: emit exactly `<promise>BLOCKED: auth wall at {PAGE}</promise>` and STOP. Do NOT generate UI from memory, do NOT screenshot, do NOT write any other artifact. (Leave the tab as-is — there's a single shared Chrome; don't close it out from under the next step.)

---

## Step 3 — FULL-PAGE baseline capture (visual reference)

Capture the full page as a **visual reference** for this route×viewport (contract §1, §11). The file cannot be reliably saved to disk in this environment, so treat the shot as a visual aid — the verification ground truth for QA is the computed styles you read via `mcp__claude-in-chrome__javascript_tool`, not the PNG.

```bash
mkdir -p "clone-workspace/{NAME}/01-recon/fragments"
```

Take the shot with `mcp__claude-in-chrome__computer` — action `screenshot`, full page (not just the viewport):

It MUST capture the FULL page (not just the viewport), one capture per route×viewport, so the visual reference is complete. The measured `getComputedStyle` values (Steps 5–7) and the per-archetype computed styles the extraction stage reads are what QA diffs 1:1 — the visual capture only helps you spot obvious breakage.

---

## Step 4 — Hover-state screenshots of primary interactive elements

Enumerate the primary interactive elements (buttons, nav links, cards), assign stable refs, then hover and shoot each. Cap at the ~8 highest-signal elements so you don't fan out forever.

Get the elements via `mcp__claude-in-chrome__javascript_tool` (returns refs + a slug for the filename — each element is also tagged with a `data-recon-ref` attribute so you can target it afterward):

```js
  (() => {
    const slug = s => (s||'el').toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-\$/g,'').slice(0,32) || 'el';
    const sel = 'a[href], button, [role=button], nav a, [class*=card i], [class*=btn i]';
    const seen = new Set(), out = [];
    document.querySelectorAll(sel).forEach(el => {
      const r = el.getBoundingClientRect();
      if (r.width < 8 || r.height < 8) return;               // skip invisible
      const label = (el.getAttribute('aria-label') || el.innerText || el.getAttribute('title') || el.tagName).trim();
      const key = label + ':' + Math.round(r.x) + ':' + Math.round(r.y);
      if (seen.has(key)) return; seen.add(key);
      el.setAttribute('data-recon-ref', 'e' + out.length);    // stable handle: target via [data-recon-ref=e0]
      out.push({ ref: 'e' + out.length, slug: slug(label), tag: el.tagName });
    });
    return out.slice(0, 8);
  })()
```

For each returned `{ref, slug}`, hover it then shoot it. Use `mcp__claude-in-chrome__find` to locate the element by its `[data-recon-ref=e0]` selector (or `mcp__claude-in-chrome__read_page` to get the matching ref), then:

1. `mcp__claude-in-chrome__computer` action `hover` over that element (or use `mcp__claude-in-chrome__javascript_tool` to scroll it into view first if it's off-screen).
2. `mcp__claude-in-chrome__computer` action `screenshot`, full page — a visual reference of the hover state.

Capture the hover shot only for elements whose appearance actually changes on hover (the extraction stage measures the exact deltas via `getComputedStyle`; the capture is a visual reference only, not a workspace artifact).

---

## Interaction sweep — click everything (per route)

The full-page screenshot (Step 3) and the ~8 hover shots (Step 4) only capture **first paint plus a hover tint.** That is not the app. A web app is not a stack of static pages: a rich-text editor toolbar that appears only when you focus the description field, the comment composer, an opened priority menu, a side panel that slides in when you click a row, a board/list/kanban view switcher, a filter popover — **these controls do not exist in the DOM until you interact.** A clone built from first-paint screenshots silently ships skin-deep. So after the static captures, recon does **not sample — it EXHAUSTIVELY exercises every interactive element on this route** (contract §8).

The rule is literal: **click EVERY button and open EVERY side panel, menu, filter, and view.** Do not stop at the first screen, do not cap the count (Step 4's ~8-element cap is for *hover tints only* — it does NOT apply here). The controls that matter most only appear after an interaction, so missing them ships a hollow clone.

### A. Enumerate every interactive element

Use `mcp__claude-in-chrome__javascript_tool` to list every interactive element on the route — buttons, links, menu/dropdown triggers, tabs, view switchers (board/list/kanban), filter controls, every row/card that opens a side panel or detail, every input and `contenteditable`. Assign a stable ref and a filename slug to each, just like Step 4 — but here you keep ALL of them, not a slice. (`mcp__claude-in-chrome__read_page` is the quickest way to list the current interactive refs + labels; the JS below also tags each with a `data-recon-ix` attribute so you can act on them afterward.)

`mcp__claude-in-chrome__read_page` → list current interactive refs + labels. Then enumerate + tag with `mcp__claude-in-chrome__javascript_tool`:

```js
  (() => {
    const slug = s => (s||'el').toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-\$/g,'').slice(0,40) || 'el';
    // every interactive element kind — NOT a curated subset
    const sel = [
      'button', 'a[href]', '[role=button]', '[role=menuitem]', '[role=tab]',
      '[role=switch]', '[role=checkbox]', '[role=radio]', '[role=combobox]',
      '[aria-haspopup]', '[aria-expanded]', '[data-state]',
      'summary', 'select', 'input', 'textarea', '[contenteditable]', '[contenteditable=true]',
      '[tabindex]:not([tabindex=\"-1\"])',
      '[class*=tab i]', '[class*=toggle i]', '[class*=switch i]',
      '[class*=filter i]', '[class*=view i]', '[class*=menu i]', '[class*=dropdown i]',
      '[class*=row i], [class*=card i], [class*=item i], [class*=list-item i]'  // rows/cards that open panels
    ].join(',');
    const kindOf = el => {
      const t = el.tagName.toLowerCase();
      if (t === 'input' || t === 'textarea' || el.isContentEditable) return 'focus';
      if (el.matches('[aria-haspopup],[class*=menu i],[class*=dropdown i],[class*=filter i]')) return 'click';
      if (el.matches('[role=tab],[class*=tab i],[class*=view i],[class*=toggle i],[class*=switch i]')) return 'click';
      return 'click';
    };
    const seen = new Set(), out = [];
    document.querySelectorAll(sel).forEach(el => {
      const r = el.getBoundingClientRect();
      if (r.width < 6 || r.height < 6) return;                 // skip invisible / zero-area
      const label = (el.getAttribute('aria-label') || el.getAttribute('placeholder') ||
                     (el.innerText||'').trim().slice(0,60) || el.getAttribute('title') ||
                     el.getAttribute('name') || el.tagName).trim();
      const key = el.tagName + ':' + label + ':' + Math.round(r.x) + ':' + Math.round(r.y);
      if (seen.has(key)) return; seen.add(key);
      el.setAttribute('data-recon-ix', 'i' + out.length);      // stable handle: target via [data-recon-ix=i0]
      out.push({
        ref: 'i' + out.length,
        action_slug: slug(label),
        trigger: el.getAttribute('data-recon-ix') ? '[data-recon-ix=i'+out.length+']' : el.tagName.toLowerCase(),
        kind: kindOf(el),
        tag: el.tagName.toLowerCase(),
        label
      });
    });
    return out;                                                // NO .slice() — keep them all
  })()
```

### B. Exercise each one, capture the revealed state, then reset

For **each** enumerated element (every entry — do not skip any), perform the appropriate action, **wait for the revealed UI to render**, capture it as a visual reference, then **close/escape the state before the next** so captures stay clean and one open panel doesn't bleed into the next shot. Target each element by the `[data-recon-ix=i0]` selector you recorded — use `mcp__claude-in-chrome__find` (or `read_page`) to resolve it to the coordinates/ref the `computer` tool needs. The ground truth for each revealed state is the DOM + computed styles you confirm via `mcp__claude-in-chrome__javascript_tool` / `read_page` (step below); the screenshot is a visual aid only.

```text
# kind=click  → open menus, dropdowns, filters, view switchers, side panels, tabs
1. mcp__claude-in-chrome__computer  action left_click  on [data-recon-ix=i0]
2. mcp__claude-in-chrome__javascript_tool:  new Promise(r=>setTimeout(()=>r(true),350))   // let the revealed UI render
3. mcp__claude-in-chrome__computer  action screenshot  full page   // visual reference of the revealed state
4. mcp__claude-in-chrome__javascript_tool:  document.activeElement && document.activeElement.blur(); document.body.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true})); true   // close menu/panel before next

# kind=focus  → reveal rich-text toolbars, comment composers (these appear ONLY on focus)
1. mcp__claude-in-chrome__computer  action left_click  on [data-recon-ix=i3]   // click to focus the input/contenteditable
2. mcp__claude-in-chrome__javascript_tool:  new Promise(r=>setTimeout(()=>r(true),350))
3. mcp__claude-in-chrome__computer  action screenshot  full page   // visual reference of the revealed state
4. mcp__claude-in-chrome__javascript_tool:  document.activeElement && document.activeElement.blur(); true

# hover is appropriate for elements whose UI is reveal-on-hover (submenus, tooltips)
1. mcp__claude-in-chrome__computer  action hover  on [data-recon-ix=i7]
2. mcp__claude-in-chrome__computer  action screenshot  full page   // visual reference of the revealed state
```

If a click navigates away from the route instead of revealing in-place UI, note it (it's a link, not a panel trigger) and re-`navigate` (`mcp__claude-in-chrome__navigate`) to the route before continuing the sweep — never let navigation silently truncate the sweep. (Re-tag with the section-A enumeration JS after navigating, since the `data-recon-ix` attributes are gone on the fresh DOM.)

After each capture, confirm the revealed UI was actually present — a quick `mcp__claude-in-chrome__javascript_tool` check that a popover/menu/toolbar node now exists (or a `mcp__claude-in-chrome__read_page` snapshot showing it) — so `captured` is truthful, not assumed.

### C. Record every interaction in `interaction-map.json` (exact contract §8 schema)

Write one entry per enumerated element to `01-recon/interaction-states/.../interaction-map.json` using the **exact** schema from contract §8 — `route`, `interactions[]` of `{action_slug, trigger, kind, reveals[], screenshot, captured}`, and `unreached[]`:

```json
{ "route": "/issue/PER-9",
  "interactions": [
    {"action_slug":"focus-description","trigger":"[contenteditable]","kind":"focus",
     "reveals":["rich-text toolbar (Aa,B,I,link,quote,code)"],
     "screenshot":"01-recon/screenshots/interaction-states/issue-per-9--focus-description.png","captured":true},
    {"action_slug":"open-priority-menu","trigger":"[data-priority]","kind":"click",
     "reveals":["priority dropdown: Urgent/High/Medium/Low/None"],
     "screenshot":"01-recon/screenshots/interaction-states/issue-per-9--open-priority-menu.png","captured":true},
    {"action_slug":"view-board","trigger":"[class*=view i]","kind":"click",
     "reveals":["kanban board columns"],
     "screenshot":"01-recon/screenshots/interaction-states/issue-per-9--view-board.png","captured":true},
    {"action_slug":"comment-composer","trigger":".comment-box","kind":"focus",
     "reveals":["composer + send button"],
     "screenshot":"01-recon/screenshots/interaction-states/issue-per-9--comment-composer.png","captured":true}
  ],
  "unreached": [
    {"action_slug":"export-csv","trigger":"button[aria-label=Export]","kind":"click",
     "reason":"behind an unauthenticated paywall modal — could not reach revealed state"}
  ] }
```

- `reveals[]` describes what newly appeared (the toolbar buttons, the menu items, the panel sections) — recorded from what you actually SAW in the `mcp__claude-in-chrome__javascript_tool` / `read_page` result after the action, never from memory.
- `screenshot` is the interaction-states path for the visual-reference capture (a visual aid only — the file may not persist to disk in this environment).
- `captured` is `true` ONLY if you confirmed via `mcp__claude-in-chrome__javascript_tool` / `read_page` that the revealed UI actually rendered; otherwise `false`.
- **Anything you cannot reach goes in `unreached[]` with a concrete `reason`** (navigated away, element detached, behind auth, no visible change after the action). **Never fabricate an interaction or a reveal** (contract §7 anti-hallucination) — an honest `unreached` entry is correct; an invented `captured:true` poisons the coverage critic in Stage 6.

This is a real DOM mutation, not a CSS pseudo-state: forcing `:hover` (Step 4 / contract §3-C) is NOT enough — you must perform the interaction (click/focus/hover via `mcp__claude-in-chrome__computer`) and capture what newly appears. Stage 2 re-triggers each of these to extract the revealed DOM + computed styles into `{page}.interactions.json`, Stage 5 rebuilds and wires the behavior, and the Stage 6 coverage critic gates on every entry here being captured, rebuilt, and behaving in the clone.

```bash
mkdir -p "clone-workspace/{NAME}/01-recon/screenshots/interaction-states"
# write the assembled object to:
clone-workspace/{NAME}/01-recon/interaction-map.json
```

---

## Step 5 — Theme detection (confirm light/dark by toggling `prefers-color-scheme`)

Report which themes the site actually responds to. Measure whether the page responds to `prefers-color-scheme` and detect explicit theme classes/attributes/toggles. Run the probe with `mcp__claude-in-chrome__javascript_tool` — it reads the current `prefers-color-scheme` match and the page's theme hooks:

```js
  (() => {
    const bg = () => getComputedStyle(document.body).backgroundColor;
    const fg = () => getComputedStyle(document.body).color;
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    // Authored dark support: any rule scope or media for dark?
    const hasDarkClass = !!document.querySelector('.dark, [data-theme=dark], [data-theme=\"dark\"], html.dark, [data-color-mode=dark]');
    const hasLightClass = !!document.querySelector('.light, [data-theme=light], [data-color-mode=light]');
    // A visible theme toggle?
    const toggle = !!document.querySelector(
      '[aria-label*=theme i],[aria-label*=dark i],[title*=theme i],[class*=theme-toggle i],button[class*=dark i]'
    );
    return {
      currentBg: bg(), currentFg: fg(),
      systemPrefersDark: prefersDark,
      hasDarkClass, hasLightClass, hasToggle: toggle
    };
  })()
```

To CONFIRM the site actually reacts to dark mode, if the page exposes a visible theme toggle, click it (`mcp__claude-in-chrome__computer` action `left_click`) and re-read the background, then toggle back:

```js
getComputedStyle(document.body).backgroundColor
```

(If there's no toggle, rely on the `.dark`/`[data-theme]` scope or `@media (prefers-color-scheme)` evidence from the probe above — don't fabricate a dark theme you can't trigger.)

Decide the `themes` array by EVIDENCE:
- background changes when the theme toggle/scope is applied, OR a `.dark`/`[data-theme]` scope exists, OR a toggle is present → include both `"light"` and `"dark"`.
- otherwise → `["light"]` only (or `["dark"]` if the site is dark-only).

Never list a theme you couldn't confirm. Restore the page to its default theme before continuing.

---

## Step 6 — Framework fingerprint (contract §3-I)

Detect the stack from real signals in the page, not a guess. Run via `mcp__claude-in-chrome__javascript_tool`:

```js
  (() => {
    const has = s => !!document.querySelector(s);
    const w = window;
    const html = document.documentElement;
    const scripts = Array.from(document.scripts).map(s => s.src).filter(Boolean);
    const hasNextStatic = scripts.some(s => /\\/_next\\/static\\//.test(s));
    const hasViteAssets = scripts.some(s => /\\/assets\\/index-[\\w-]+\\.js/.test(s));
    // Tailwind: presence of --tw-* custom props anywhere
    let tw = false;
    try { tw = getComputedStyle(html).getPropertyValue('--tw-ring-color') !== '' ||
               !!document.querySelector('[class*=\" \"]') &&
               /\\b(flex|grid|px-\\d|py-\\d|text-(xs|sm|base|lg|xl)|bg-)\\b/.test(html.innerHTML.slice(0, 50000)); } catch(e){}
    return {
      next: !!(w.__NEXT_DATA__) || !!(w.__next_f) || hasNextStatic,
      remix: !!(w.__remixContext),
      nuxt: !!(w.__NUXT__),
      react: has('[data-reactroot]') || !!(w.React) || has('#__next') || has('#root[data-reactroot]'),
      angular: has('[ng-version]'),
      angularVersion: (document.querySelector('[ng-version]')||{}).getAttribute?.('ng-version') || null,
      vue: has('[data-v-app]') || !!(w.__VUE__) || /data-v-[0-9a-f]{8}/.test(html.outerHTML.slice(0,50000)),
      svelte: /svelte-[0-9a-z]+/.test(html.outerHTML.slice(0,50000)),
      astro: has('[data-astro-cid]') || /data-astro-/.test(html.outerHTML.slice(0,50000)),
      tailwind: tw,
      generator: (document.querySelector('meta[name=generator]')||{}).getAttribute?.('content') || null,
      assetHosts: Array.from(new Set(scripts.map(s => { try { return new URL(s).pathname.split('/').slice(0,3).join('/'); } catch(e){ return null; } }).filter(Boolean))).slice(0,8)
    };
  })()
```

Keep the raw object as the `framework` value in `recon.json`. Don't normalize it into a single guessed name — Stage 4 (Architecture) reads these signals.

---

## Step 7 — Measure real breakpoints

Don't assume 768/375. Pull the actual `@media (width...)` breakpoints authored in the page's own stylesheets. Run via `mcp__claude-in-chrome__javascript_tool`:

```js
  (() => {
    const bps = new Set();
    for (const sheet of document.styleSheets) {
      let rules; try { rules = sheet.cssRules; } catch (e) { continue; } // cross-origin: extraction stage refetches
      if (!rules) continue;
      for (const r of rules) {
        if (r.type === CSSRule.MEDIA_RULE) {
          const m = r.conditionText.match(/(min|max)-width:\\s*([\\d.]+)(px|rem|em)/g);
          if (m) m.forEach(x => bps.add(x.trim()));
        }
      }
    }
    return Array.from(bps).sort();
  })()
```

Use these conditions as the `breakpoints` array. If everything is cross-origin and unreadable here, record the breakpoints you CAN read and leave the rest for extraction (§3-E refetches cross-origin sheets) — never invent values.

---

## Step 8 — Same-origin link discovery → routes fragment

Discover internal routes so the orchestrator can build the sitemap. Write a JSON ARRAY of route paths (not objects) to the fragment path — the orchestrator unions all fragments into `sitemap.json` (contract §1, §2; merge is deterministic code, never an agent). Run via `mcp__claude-in-chrome__javascript_tool`:

```js
  (() => {
    const origin = location.origin;
    const norm = p => {
      try {
        const u = new URL(p, location.href);
        if (u.origin !== origin) return null;            // same-origin only
        let path = u.pathname.replace(/\\/+\$/,'') || '/'; // strip trailing slash, keep root
        if (/\\.(png|jpe?g|svg|gif|webp|ico|css|js|json|pdf|zip|mp4|woff2?)\$/i.test(path)) return null;
        return path;
      } catch (e) { return null; }
    };
    const set = new Set();
    document.querySelectorAll('a[href]').forEach(a => {
      const p = norm(a.getAttribute('href'));
      if (p) set.add(p);
    });
    return Array.from(set).sort();
  })()
```

Write the returned array verbatim:

```bash
# write the javascript_tool result (a JSON array like ["/","/pricing","/about"]) to:
clone-workspace/{NAME}/01-recon/fragments/{page-slug}.routes.json
```

If the result is `[]` (e.g. a fully client-routed app with no `<a href>`), write `[]` — do not fabricate routes.

---

## Step 9 — Merge-safe write of `recon.json` (read-modify-write)

Multiple recon agents share `01-recon/recon.json`. You MUST read-modify-write so a parallel agent's data is not clobbered (contract §1, §2). Build your contribution, then merge into any existing file. Keep `themes`/`breakpoints` as a UNION across agents; `framework` is keyed by page-slug so each agent contributes its own fingerprint without overwriting another's.

Target shape:

```json
{
  "themes": ["light", "dark"],
  "breakpoints": ["min-width: 768px", "min-width: 1024px"],
  "framework": { "home": { "next": true, "tailwind": true, "...": "..." } }
}
```

Do the merge with a tiny script (jq or node), not by hand-editing — concurrent writers make hand-edits unsafe. Example with `node` (atomic-ish read-modify-write):

```bash
RECON="clone-workspace/{NAME}/01-recon/recon.json"
node -e '
  const fs = require("fs");
  const path = process.argv[1];
  const slug = process.argv[2];
  const mine = JSON.parse(process.argv[3]);   // {themes:[...],breakpoints:[...],framework:{...}}
  let cur = {themes:[],breakpoints:[],framework:{}};
  try { cur = JSON.parse(fs.readFileSync(path,"utf8")); } catch(e){}
  const uniq = a => Array.from(new Set(a));
  cur.themes = uniq([...(cur.themes||[]), ...mine.themes]);
  cur.breakpoints = uniq([...(cur.breakpoints||[]), ...mine.breakpoints]);
  cur.framework = cur.framework || {};
  cur.framework[slug] = mine.framework;       // per-page key — never overwrite another page
  fs.writeFileSync(path, JSON.stringify(cur, null, 2));
' "$RECON" "{page-slug}" '{"themes":["light"],"breakpoints":["min-width: 768px"],"framework":{ ... your fingerprint ... }}'
```

(If two agents race the read-modify-write, that is acceptable for this advisory file — the orchestrator treats `recon.json` as a hint, and any single missing per-page framework key is non-fatal. Still, prefer this node merge over a blind overwrite.)

---

## Step 10 — Complete

Leave the shared Chrome tab open (the next sequential recon route reuses it — there's a single browser, so don't tear it down). Then set this task's flag in `status.json` per contract §7 (the orchestrator defines the flag name for your page×viewport task — write only your own task's flag, read-modify-write).

---

## OUTPUTS you wrote (exact paths — nothing else, contract §1)

- `clone-workspace/{NAME}/01-recon/screenshots/{page-slug}--{VIEWPORT}.png`  (full-page baseline)
- `clone-workspace/{NAME}/01-recon/screenshots/hover-states/{page-slug}--{slug}.png`  (per hovered element)
- `clone-workspace/{NAME}/01-recon/screenshots/interaction-states/{page-slug}--{action-slug}.png`  (per interaction-revealed state, §8)
- `clone-workspace/{NAME}/01-recon/interaction-map.json`  (every interactive element exercised, exact §8 schema)
- `clone-workspace/{NAME}/01-recon/fragments/{page-slug}.routes.json`  (JSON array of same-origin paths)
- `clone-workspace/{NAME}/01-recon/recon.json`  (merge-safe `{themes,breakpoints,framework}`)

Do NOT write `sitemap.json` (orchestrator merges it) or `recon-report.md` — they are not in the contract. (Note: `interaction-map.json` IS in the contract per §1/§8 and is required; the Stage-2 `{page}.interactions.json` is NOT yours to write — that's the extraction stage, §3 / §8.)

---

## Evidence & anti-hallucination (contract §7)

- The ground-truth verification source is the measured `getComputedStyle` / CSSOM values you read via `mcp__claude-in-chrome__javascript_tool` — captured full-page at exact `{VIEWPORT}` pixels, fully hydrated. The full-page screenshot is a visual reference only (it may not persist to disk in this environment), so a measured value always beats a screenshot impression.
- Every `themes` / `breakpoints` / `framework` value comes from a measured `mcp__claude-in-chrome__javascript_tool` result above — never from memory or assumption.
- Every `interaction-map.json` entry is grounded in an action you actually performed and a revealed UI you actually observed (confirmed via `mcp__claude-in-chrome__javascript_tool` / `read_page`). `captured:true` requires that you confirmed the revealed UI rendered via `mcp__claude-in-chrome__javascript_tool` / `read_page`; otherwise the element goes in `unreached[]` with a concrete reason. Never fabricate an interaction, a reveal, or a `captured:true`.
- A value you genuinely cannot read = omit it / `null` + the reason in `progress.md`. Never invent a route, a breakpoint, or a theme.
- If the page can't be reached or is gated, you already emitted `<promise>BLOCKED: auth wall at {PAGE}</promise>` in Step 2 and stopped.

## COMPLETION

After writing all outputs and your `status.json` flag, end with exactly:

`<promise>CONTINUE</promise>`

---

## CAPTURE EVERY VIEW — non-negotiable

**Capture each view with the Claude Chrome extension as a visual reference** (`mcp__claude-in-chrome__computer` action `screenshot`) — the file may not persist to disk in this environment, so treat the shot as a visual aid and rely on the measured `getComputedStyle` / `read_page` reads for the ground truth. (See contract §11.)

**Capture EVERY view — exhaustive, not a sample.** Do not stop after the first screen. You must reach and capture:
- **every left-hand sidebar item** — click each, navigate into the view it opens, capture it;
- **every tab / top filter** (Active, Backlog, All, …);
- **every filter and layout control** — open the filter menu and apply each; toggle board ↔ list ↔ every layout; sort/group;
- **every menu, dropdown, and context menu** (capture the open state);
- **every side panel, detail, and modal** (open an issue, open settings panels, slide-overs);
- **every interaction-revealed state** (focus the editor → its toolbar; the comment composer; hover states);
- at **every viewport** (desktop, tablet, mobile).

Log each in `interaction-map.json`, grounded in the `mcp__claude-in-chrome__javascript_tool` / `read_page` confirmation that the view actually rendered. If you finish recon having exercised only one or a handful of views, it is wrong — go back and exercise every sidebar item, tab, filter, and panel until each is confirmed.
