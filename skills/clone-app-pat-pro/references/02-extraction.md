# Stage 2: Extraction — detailed reference (per route, sequential, in-conversation)

> **ROLE.** You are the EXTRACTION stage of a pixel-perfect cloning pipeline, running **in-conversation** (SKILL.md → "How this runs"). You read every style value off the **real, logged-in** target page — *leave no stone unturned*. The old "50 elements / 17 properties" cap is **DELETED**. You bound size with **signature-dedup + delta-from-default + per-section batching**, not by capping coverage.

This file is the Stage 2 reference (see `stage-prompts.md` → `## Stage 2: Extraction`). It implements **contract §3 (A–I)** exactly and writes **only** the artifact paths in **contract §1**. When this file and `00-contract.md` disagree, the contract wins.

**Browser tool — Claude Chrome extension (`mcp__claude-in-chrome__*`).** Extraction reads values off the REAL, authed site, so it uses the Claude Chrome extension you're already logged into. Every JS capture below runs through `mcp__claude-in-chrome__javascript_tool`; navigation through `mcp__claude-in-chrome__navigate`; DOM reads through `read_page` / `find` / a `javascript_tool` `outerHTML` read. Asset/font byte downloads and cross-origin stylesheet refetches stay as Bash `curl` (not browser-tool-specific). There is **one Chrome**: run extraction **sequentially, one route / one tab at a time** — never two browser actions at once.

---

## 0. Inputs, tool, and conventions

**Inputs you read:**
- `clone-workspace/{name}/00-config.json` — `target_url`, `pages[]`, `viewports`, `stack`, `gate`.
- `clone-workspace/{name}/01-recon/sitemap.json` — `{ "routes": [...] }`. You extract **one `{PAGE}` at a time** (sequential — one Chrome, one tab).
- `clone-workspace/{name}/01-recon/recon.json` — may already carry `themes` and the framework fingerprint (§3-I). Read it; do not re-derive what's already measured.

**Tool: the Claude Chrome extension (`mcp__claude-in-chrome__*`).** Extraction reads off the REAL, logged-in site, so you drive the Chrome you're already authed in — JS via `mcp__claude-in-chrome__javascript_tool`, navigation via `mcp__claude-in-chrome__navigate`, DOM reads via `read_page` / `find` / a `javascript_tool` `outerHTML` read. **No `--session` isolation, no SSH/Mac Mini/Playwright.** There is **one Chrome**: run routes **sequentially, one tab at a time**. Set per-route path vars in the shell for the `curl` downloads/refetches:

```bash
URL="$(jq -r .target_url clone-workspace/{name}/00-config.json)"
SLUG="{page-slug}"                     # route '/' → home ; '/blog/post' → blog-post  (contract §1)
FRAG="clone-workspace/{name}/02-extraction/fragments"
EXT="clone-workspace/{name}/02-extraction"
mkdir -p "$FRAG" "$EXT/assets/img" "$EXT/assets/svg" "$EXT/assets/fonts" /tmp/extract-{PAGE}
```

**The JS-capture pattern (mandatory).** Every capture below is large JS — an IIFE that ends with `return JSON.stringify(...)`. **Run it through `mcp__claude-in-chrome__javascript_tool`** (the snippet bodies below are unchanged; they're the same JS, just executed via the extension instead of an `eval` CLI). Take the string the tool returns and write it to the fragment file (Write tool, or `cat`/redirect via Bash). After every write, sanity-check it parsed: `jq -e . "$FRAG/$SLUG.computed.json" >/dev/null || echo "PARSE FAIL $SLUG.computed.json"`.

**Open + fully hydrate before reading anything:**

1. `mcp__claude-in-chrome__navigate` → `$URL{PAGE}`.
2. Wait ~2.5s for hydration.
3. Force lazy content to mount via `mcp__claude-in-chrome__javascript_tool` — same snippet, scroll to bottom in steps then back to top:

```js
(async()=>{const h=document.body.scrollHeight;for(let y=0;y<h;y+=600){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,120));}window.scrollTo(0,0);await new Promise(r=>setTimeout(r,400));return document.readyState;})()
```

If the route is blank, redirects to `/login`, or shows an auth wall → **do not fabricate**. Write what you safely got, set the task flag, and emit `<promise>BLOCKED: auth-wall on {PAGE}</promise>` (contract §6). (Note: because you're driving the real, already-logged-in Chrome, a genuine auth wall here is rare — but if the session is logged out, do not fabricate.)

**Screenshots** (the optional interaction-state captures below) follow contract §11: take with the Chrome extension's screenshot tool (`mcp__claude-in-chrome__computer` action `screenshot`) as a visual reference only — the file may not persist to disk in this environment, so it is a visual aid, never the source of a value. The ground truth is the DOM + computed styles you read via `mcp__claude-in-chrome__javascript_tool`.

**Evidence order when sources conflict (contract §3 / §7):** `CSSOM authored rules > CDP forced-state computed > deduped computed archetypes > screenshot estimate`. **Anti-hallucination:** a value you cannot read is recorded as `null` with a `reason` — never invented, never carried over from memory.

**Output map (contract §1) — what is per-route vs shared:**

| Artifact | Scope | Write mode |
|---|---|---|
| `fragments/{slug}.computed.json` | per-route | overwrite (you own this file) |
| `fragments/{slug}.pseudo.json` | per-route | overwrite |
| `fragments/{slug}.states.json` | per-route | overwrite |
| `fragments/{slug}.layout.json` | per-route | overwrite |
| `fragments/{slug}.dom.html` | per-route | overwrite |
| `css-variables.json` | **shared** | **read-modify-write (merge)** |
| `all-styles.json` | **shared** | read-modify-write (merge) |
| `fonts.json` | **shared** | read-modify-write (merge) |
| `assets.json` | **shared** | read-modify-write (merge) |
| `assets/{img,svg,fonts}/*` | shared dir | content-hashed filenames (no clobber) |

> **Shared files.** Routes run sequentially (one Chrome), so the shared JSONs (`css-variables.json`, `all-styles.json`, `fonts.json`, `assets.json`) are read-modify-write **merged** across routes — each route folds its partial into the existing file rather than blind-overwriting (see §9). Per-route fragments are collision-free by `{slug}` and are simply overwritten.

---

## §3-A — Computed styles for ALL meaningful nodes (signature-deduped)

**Goal.** Walk every meaningful node, read the full property set, **dedupe by a signature hash of the full computed map**, and emit ONE representative per unique signature with `count`, a sample CSS selector, and `getBoundingClientRect()` (pixel ground truth). **Drop every property equal to its CSS initial value** (delta-from-default) so the JSON carries only what the author actually changed.

**Why this stays bounded.** A real page has thousands of nodes but only dozens-to-low-hundreds of *distinct* styling signatures (every card, every nav link, every body paragraph collapses to one archetype). Signature-dedup + delta-from-default typically shrinks 4,000 nodes to ~80–250 archetypes — full coverage, bounded output. If a single section is still huge, batch by section (see "Per-section batching" below) and append.

**Meaningful node filter.** `document.querySelectorAll('*')` minus `script, style, meta, link, head, title, noscript`, minus zero-area nodes (`rect.width===0 || rect.height===0`) **unless** the node is `position:fixed/absolute` and merely offscreen (keep those — they're real). Keep `display:none`? No — skip `display:none` for the computed pass (it has no box), but the CSSOM dump (§3-E) still preserves its authored rules.

**The full property list (contract §3-A, minimum).** Read all of these via one `getComputedStyle` per node:

- **Color/bg:** `color, backgroundColor, backgroundImage` *(gradients live here — MANDATORY)*, `backgroundSize, backgroundPosition, backgroundRepeat, backgroundClip, backgroundOrigin, backgroundAttachment, backgroundBlendMode, opacity, mixBlendMode, accentColor, caretColor, webkitBackgroundClip, webkitTextFillColor` *(gradient text)*
- **Typography:** `fontFamily, fontSize, fontWeight, fontStyle, fontStretch, lineHeight, letterSpacing, wordSpacing, textTransform, textDecorationLine, textDecorationColor, textDecorationStyle, textDecorationThickness, textUnderlineOffset, textShadow, textAlign, whiteSpace, textOverflow, fontVariationSettings, fontOpticalSizing, fontFeatureSettings, fontKerning`
- **Box model (PER-SIDE — never the shorthand):** `paddingTop, paddingRight, paddingBottom, paddingLeft, marginTop, marginRight, marginBottom, marginLeft, borderTopWidth, borderRightWidth, borderBottomWidth, borderLeftWidth, borderTopStyle, borderRightStyle, borderBottomStyle, borderLeftStyle, borderTopColor, borderRightColor, borderBottomColor, borderLeftColor, borderTopLeftRadius, borderTopRightRadius, borderBottomRightRadius, borderBottomLeftRadius` *(asymmetric radii)*, `boxSizing, width, height, minWidth, minHeight, maxWidth, maxHeight, aspectRatio, top, right, bottom, left, outlineWidth, outlineStyle, outlineColor, outlineOffset`
- **Effects:** `boxShadow, filter, backdropFilter` *(glassmorphism — MANDATORY)*, `webkitBackdropFilter, clipPath, maskImage, webkitMaskImage, isolation`
- **Layout:** `display, flexDirection, flexWrap, justifyContent, alignItems, alignContent, alignSelf, flexGrow, flexShrink, flexBasis, order, gridTemplateColumns, gridTemplateRows, gridTemplateAreas, gridAutoFlow, gridAutoColumns, gridAutoRows, justifyItems, placeItems, gridColumn, gridRow, rowGap, columnGap, overflowX, overflowY, overscrollBehavior, scrollSnapType, scrollBehavior, containerType, containerName`
- **Layering/motion:** `zIndex, position, transform, transformOrigin, perspective, willChange, transitionProperty, transitionDuration, transitionTimingFunction, transitionDelay, animationName, animationDuration, animationTimingFunction, animationIterationCount, animationDirection, animationFillMode`
- **Cursor:** `cursor` (on every interactive element)

**Delta-from-default.** Compare each read value against the CSS initial value. Compute the initial map ONCE per document by reading `getComputedStyle` off a throwaway element appended to a `<div style="all:initial">` host, then drop any property whose value equals that baseline. (`all:initial` resets the host so its children's *unset* properties report initials; we still read property-by-property because inherited props differ — so we keep a per-property initial table built from the host.)

**Signature + representative.** Signature = a stable hash of the *kept* (post-delta) property map. Use a cheap FNV-1a over the sorted `key:value;` string. For each signature keep: the hash, the full kept-property map, `count`, the **first** node's CSS selector (built nth-of-type path), its `tagName`, a 60-char text sample, and that node's `getBoundingClientRect()` rounded to 0.1px.

Copy-pasteable walker (write to `walker.js`):

```js
(() => {
  const SKIP = new Set(['SCRIPT','STYLE','META','LINK','HEAD','TITLE','NOSCRIPT','BASE','TEMPLATE']);
  const PROPS = ["color","backgroundColor","backgroundImage","backgroundSize","backgroundPosition","backgroundRepeat","backgroundClip","backgroundOrigin","backgroundAttachment","backgroundBlendMode","opacity","mixBlendMode","accentColor","caretColor","webkitBackgroundClip","webkitTextFillColor","fontFamily","fontSize","fontWeight","fontStyle","fontStretch","lineHeight","letterSpacing","wordSpacing","textTransform","textDecorationLine","textDecorationColor","textDecorationStyle","textDecorationThickness","textUnderlineOffset","textShadow","textAlign","whiteSpace","textOverflow","fontVariationSettings","fontOpticalSizing","fontFeatureSettings","fontKerning","paddingTop","paddingRight","paddingBottom","paddingLeft","marginTop","marginRight","marginBottom","marginLeft","borderTopWidth","borderRightWidth","borderBottomWidth","borderLeftWidth","borderTopStyle","borderRightStyle","borderBottomStyle","borderLeftStyle","borderTopColor","borderRightColor","borderBottomColor","borderLeftColor","borderTopLeftRadius","borderTopRightRadius","borderBottomRightRadius","borderBottomLeftRadius","boxSizing","width","height","minWidth","minHeight","maxWidth","maxHeight","aspectRatio","top","right","bottom","left","outlineWidth","outlineStyle","outlineColor","outlineOffset","boxShadow","filter","backdropFilter","webkitBackdropFilter","clipPath","maskImage","webkitMaskImage","isolation","display","flexDirection","flexWrap","justifyContent","alignItems","alignContent","alignSelf","flexGrow","flexShrink","flexBasis","order","gridTemplateColumns","gridTemplateRows","gridTemplateAreas","gridAutoFlow","gridAutoColumns","gridAutoRows","justifyItems","placeItems","gridColumn","gridRow","rowGap","columnGap","overflowX","overflowY","overscrollBehavior","scrollSnapType","scrollBehavior","containerType","containerName","zIndex","position","transform","transformOrigin","perspective","willChange","transitionProperty","transitionDuration","transitionTimingFunction","transitionDelay","animationName","animationDuration","animationTimingFunction","animationIterationCount","animationDirection","animationFillMode","cursor"];

  // per-property CSS initial table (delta-from-default baseline)
  const host = document.createElement('div'); host.style.all = 'initial';
  const probe = document.createElement('div'); host.appendChild(probe); document.documentElement.appendChild(host);
  const init = {}; { const cs = getComputedStyle(probe); for (const p of PROPS) init[p] = cs[p]; }
  document.documentElement.removeChild(host);

  const fnv = s => { let h = 0x811c9dc5; for (let i=0;i<s.length;i++){ h ^= s.charCodeAt(i); h = Math.imul(h,0x01000193); } return (h>>>0).toString(16); };
  const sel = el => { const parts=[]; let n=el; while(n && n.nodeType===1 && parts.length<5){ let s=n.tagName.toLowerCase(); if(n.id){ parts.unshift(s+'#'+CSS.escape(n.id)); break; } const cls=(n.className&&n.className.baseVal!==undefined?n.className.baseVal:n.className||'').toString().trim().split(/\s+/).filter(Boolean).slice(0,2).map(c=>'.'+CSS.escape(c)).join(''); let i=1,sib=n; while((sib=sib.previousElementSibling)) if(sib.tagName===n.tagName) i++; parts.unshift(s+cls+`:nth-of-type(${i})`); n=n.parentElement; } return parts.join(' > '); };

  const sigs = new Map();
  for (const el of document.querySelectorAll('*')) {
    if (SKIP.has(el.tagName)) continue;
    const cs = getComputedStyle(el);
    if (cs.display === 'none') continue;
    const r = el.getBoundingClientRect();
    const fixedish = cs.position==='fixed'||cs.position==='absolute'||cs.position==='sticky';
    if ((r.width===0 || r.height===0) && !fixedish) continue;
    const kept = {};
    for (const p of PROPS) { const v = cs[p]; if (v !== init[p] && v !== '' && v != null) kept[p] = v; }
    if (Object.keys(kept).length === 0) continue;
    const key = Object.keys(kept).sort().map(k=>k+':'+kept[k]+';').join('');
    const h = fnv(key);
    let rec = sigs.get(h);
    if (!rec) { rec = { signature:h, count:0, tag:el.tagName.toLowerCase(), sampleSelector:sel(el), text:(el.textContent||'').trim().slice(0,60), rect:{x:+r.x.toFixed(1),y:+r.y.toFixed(1),w:+r.width.toFixed(1),h:+r.height.toFixed(1)}, styles:kept }; sigs.set(h, rec); }
    rec.count++;
  }
  const archetypes = [...sigs.values()].sort((a,b)=>b.count-a.count);
  return JSON.stringify({ page:"{PAGE}", viewport:"desktop", nodeCountKept: archetypes.reduce((s,a)=>s+a.count,0), archetypeCount: archetypes.length, archetypes }, null, 0);
})()
```

Run the walker via `mcp__claude-in-chrome__javascript_tool`, then write the returned string to `$FRAG/$SLUG.computed.json` and sanity-check it:

```bash
jq -e '.archetypeCount' "$FRAG/$SLUG.computed.json" >/dev/null || echo "PARSE FAIL computed"
```

**Per-section batching (only if a single `javascript_tool` run blows up / OOMs / hits an output limit).** Re-run the same walker via `javascript_tool` but scope `querySelectorAll` to `header,nav,main,section,footer,[role=region]` one at a time (pass a section index as a `{SECTION}` placeholder), tag each archetype with `section`, and `jq -s 'reduce .[] as $f (...)` merge the section files into `$SLUG.computed.json`. Dedup by signature again at merge time (sum counts). Default to the single-pass walker; batch only on failure.

---

## §3-B — Pseudo-elements → `fragments/{slug}.pseudo.json`

For every meaningful node read `getComputedStyle(el, P)` for `P ∈ ['::before','::after','::placeholder','::marker','::selection','::first-letter','::first-line','::backdrop']`. **Emit only where the pseudo is real** — for `::before/::after` that means `content !== 'none'`; for the others, emit where any captured prop deviates from initial. Capture `content, backgroundColor, backgroundImage, backgroundSize, backgroundPosition, width, height, top, right, bottom, left, position, display, transform, transformOrigin, maskImage, clipPath, color, fontFamily, fontSize, fontWeight, borderRadius, boxShadow, opacity, filter`. Dedupe by signature exactly like §3-A.

```js
(() => {
  const SKIP = new Set(['SCRIPT','STYLE','META','LINK','HEAD','TITLE','NOSCRIPT']);
  const PSEUDOS = ['::before','::after','::placeholder','::marker','::selection','::first-letter','::first-line','::backdrop'];
  const PROPS = ["content","backgroundColor","backgroundImage","backgroundSize","backgroundPosition","width","height","top","right","bottom","left","position","display","transform","transformOrigin","maskImage","webkitMaskImage","clipPath","color","fontFamily","fontSize","fontWeight","borderTopLeftRadius","boxShadow","opacity","filter"];
  const fnv = s => { let h=0x811c9dc5; for(let i=0;i<s.length;i++){h^=s.charCodeAt(i);h=Math.imul(h,0x01000193);} return (h>>>0).toString(16); };
  const sel = el => { let n=el,p=[]; while(n&&n.nodeType===1&&p.length<4){ if(n.id){p.unshift(n.tagName.toLowerCase()+'#'+n.id);break;} let i=1,s=n; while((s=s.previousElementSibling)) if(s.tagName===n.tagName)i++; p.unshift(n.tagName.toLowerCase()+`:nth-of-type(${i})`); n=n.parentElement; } return p.join(' > '); };
  const out = new Map();
  for (const el of document.querySelectorAll('*')) {
    if (SKIP.has(el.tagName)) continue;
    for (const P of PSEUDOS) {
      let cs; try { cs = getComputedStyle(el, P); } catch(e){ continue; }
      const content = cs.content;
      const isCA = P==='::before'||P==='::after';
      if (isCA && (content==='none'||content==='normal'||content==='')) continue;
      const m = {}; for (const p of PROPS) { const v=cs[p]; if(v&&v!=='none'&&v!=='normal'&&v!=='auto'&&v!=='0px'&&v!=='rgba(0, 0, 0, 0)') m[p]=v; }
      if (!isCA && Object.keys(m).length===0) continue;
      const key = P+'|'+Object.keys(m).sort().map(k=>k+':'+m[k]).join(';');
      const h = fnv(key); let rec = out.get(h);
      if (!rec){ rec={signature:h,pseudo:P,count:0,sampleSelector:sel(el),styles:m}; out.set(h,rec); }
      rec.count++;
    }
  }
  return JSON.stringify({ page:"{PAGE}", pseudoArchetypes:[...out.values()].sort((a,b)=>b.count-a.count) }, null, 0);
})()
```

Run via `mcp__claude-in-chrome__javascript_tool`; write the returned string to `$FRAG/$SLUG.pseudo.json`.

---

## §3-C — Forced interaction states → `fragments/{slug}.states.json`

Force `:hover :focus :focus-visible :active` and re-read computed; **emit deltas only** (the property names + values that *changed* from the resting computed map). This is where buttons reveal their hover background, links their underline, inputs their focus ring.

**Primary — parse authored state rules from the CSSOM (via `javascript_tool`).** Because the Chrome extension exposes JS evaluation but not a raw CDP `CSS.forcePseudoState` passthrough, the **authored-rule path is the primary method** here — and it's the *highest* item in the evidence order (CSSOM authored rules), so this is not a downgrade. Walk every style rule whose `selectorText` matches `/:hover|:focus|:focus-visible|:active/`, keep the rule's declarations, and resolve which resting archetype each base selector maps to. Record `evidence_method:"cssom-authored"` so the design-spec agent knows the provenance.

**Optional — forced-state computed via `:focus` you can actually drive.** For `:focus`/`:focus-visible` you can force the real thing with `mcp__claude-in-chrome__javascript_tool`: call `el.focus()` on each interactive element, re-read `getComputedStyle`, diff against the resting map, then `el.blur()`. (`:hover`/`:active` aren't reliably forceable without CDP — rely on the authored-rule path for those.) Where you do capture a forced read, record `evidence_method:"forced-computed"` and `{selector, state, deltas:{prop:{from,to}}}`.

```js
// PRIMARY: authored state rules from CSSOM (run via javascript_tool)
(() => {
  const STATES = [':hover',':focus-visible',':focus',':active'];
  const rules = [];
  const walk = (list) => { for (const r of list) {
    if (r.cssRules && (r.media||r.conditionText!==undefined)) { walk(r.cssRules); continue; }
    if (!r.selectorText) continue;
    const st = STATES.find(s => r.selectorText.includes(s));
    if (!st) continue;
    const decls = {}; for (const p of r.style) decls[p] = r.style.getPropertyValue(p);
    rules.push({ state: st, selector: r.selectorText, declarations: decls });
  }};
  for (const sh of document.styleSheets) { try { walk(sh.cssRules); } catch(e){ /* cross-origin: covered by §3-E refetch */ } }
  return JSON.stringify({ page:"{PAGE}", evidence_method:"cssom-authored", stateRules: rules }, null, 0);
})()
```

Run via `mcp__claude-in-chrome__javascript_tool`; write the returned string to `$FRAG/$SLUG.states.json`.

If neither path yields anything (no interactive elements found), write `{"page":"{PAGE}","evidence_method":null,"stateRules":[],"reason":"no interactive elements / no state rules in CSSOM"}` — **null + reason, never invented.**

---

## Interaction-state extraction (from the recon interaction map) → `fragments/{slug}.interactions.json`

§3-C above captures CSS pseudo-states — the styling a node *already has* that only switches on under `:hover/:focus/:active`. **This section is a different thing entirely.** A rich-text toolbar that appears when you focus the editor, an opened priority menu, a comment composer, a side panel that slides in when you click a row, a board/list view toggle — **these are real DOM MUTATIONS, not pseudo-states.** Forcing `:hover`/`:focus` via CDP (§3-C) is **NOT enough**: the toolbar/menu/composer/panel are *new DOM that did not exist at first paint* and only come into being after you actually perform the interaction. You cannot read them off the resting page. You must trigger the interaction and capture what newly appears — its structure, its full computed styles, and where/how it was triggered. A clone built without this ships skin-deep (contract §8).

**Input.** Read `01-recon/interaction-map.json` and take the entry for **your assigned route** (`route` matches `$URL{PAGE}` / your `{PAGE}`). It lists every interactive element recon exercised, each as `{action_slug, trigger, kind, reveals, screenshot, captured}`.

**Task — for each entry in that route's `interactions[]`:** PERFORM the interaction on the live page (focus the editor, open the menu, open the side panel, focus the comment composer, click the row, toggle the view), wait for the revealed UI to mount, then snapshot the **REVEALED DOM + computed styles** of the newly-appeared nodes. Close/escape each state before the next so captures stay clean and the next trigger isn't occluded.

**Schema per interaction entry** (array `interactions[]` in `fragments/{slug}.interactions.json`):

```jsonc
{
  "action_slug": "open-priority-menu",          // from interaction-map.json, 1:1
  "trigger": { "selector": "[data-priority]", "kind": "click" },  // what you acted on + how (click|focus|hover|toggle)
  "revealed_dom": "<div class=\"menu\" role=\"menu\">…</div>",     // cleaned outerHTML of the NEW UI only (scripts/handlers stripped, classes/data-*/ARIA/inline-style KEPT)
  "computed": [                                  // deduped style archetypes of the revealed nodes (same dedup as §3-A)
    { "signature":"…", "count":5, "tag":"div", "sampleSelector":"…",
      "rect":{"x":0,"y":0,"w":0,"h":0}, "styles":{ /* full §3-A property set, delta-from-default */ } }
  ],
  "notes": "menu portals to document.body; position:absolute; z-index 50; appears below trigger"
}
```

- **`revealed_dom`** — cleaned `outerHTML` of the **newly-appeared** UI ONLY (the menu / toolbar / composer / panel), not the whole page. Strip script bodies + inline `on*` handlers; KEEP classes, `data-*`, ARIA, and inline `style=` (same cleaning rule as `{slug}.dom.html`).
- **`computed`** — deduped style archetypes of the revealed nodes, using the **exact same full computed-style property set and signature-dedup + delta-from-default** machinery as static nodes (§3-A). Walk only the revealed subtree, not the whole document.
- **`trigger` / `notes`** — the trigger selector + kind, plus position/portal/stacking facts (where it mounts, z-index, anchor) so the build can wire and place it.

**Identifying "what newly appeared."** Diff the DOM before/after the interaction: snapshot the set of element references (or a count + a marker) pre-trigger, perform the trigger, then treat nodes present after but absent before as the revealed subtree. A robust approach: record `document.querySelectorAll('*').length` and the existing top-level overlay containers before; after the trigger, take the newly-added nodes (commonly portaled to `body`, or a panel toggled from `hidden`/`display:none` to visible) as the revealed UI.

**Concrete sequence** (per route; reuse the already-open hydrated page in the **Claude Chrome extension** — read the interaction list with Bash `jq`, drive each interaction with `javascript_tool`, write the result with the Write tool / Bash):

```bash
MAP="clone-workspace/{name}/01-recon/interaction-map.json"
# (page already open + hydrated from §0, in the Chrome extension tab)

# pull this route's interaction list (shell-side bookkeeping)
jq -c --arg r "$URL{PAGE}" '.[]? // . | select(.route==$r) | .interactions[]?' "$MAP" \
  > /tmp/extract-{PAGE}/interactions.list.jsonl
: > "$FRAG/$SLUG.interactions.tmp.jsonl"
```

For **each** interaction entry (iterate the list above), run these steps in the open tab — one at a time, sequentially:

1. **Mark the pre-interaction DOM** so you can isolate what newly appears — `mcp__claude-in-chrome__javascript_tool`:
   ```js
   (()=>{window.__before=new Set(document.querySelectorAll('*'));return document.querySelectorAll('*').length;})()
   ```
2. **PERFORM the interaction** (a real DOM mutation, not a forced pseudo-state) on the trigger selector. Drive it with `mcp__claude-in-chrome__javascript_tool` by `kind`: `click` → `document.querySelector(TRIG).click()`; `focus` → `.focus()`; `hover` → dispatch a `pointerover`/`mouseover` `MouseEvent` on the element; `toggle`/menu/panel-open → `.click()`. Then wait ~600ms for the toolbar/menu/composer/panel to mount.
3. **Snapshot the REVEALED nodes only** (present after, absent before) + their computed styles, using the SAME full property set + signature-dedup + delta-from-default as §3-A — run this via `mcp__claude-in-chrome__javascript_tool` and capture its returned string into `$REVEAL`:

```js
  (() => {
    const before = window.__before || new Set();
    const fresh = [...document.querySelectorAll('*')].filter(n => !before.has(n) && getComputedStyle(n).display!=='none');
    // collapse to the top-most newly-added roots (drop nodes whose parent is also fresh)
    const roots = fresh.filter(n => !fresh.includes(n.parentElement));
    const clean = el => { const c = el.cloneNode(true);
      c.querySelectorAll('script').forEach(s=>s.textContent='');
      c.querySelectorAll('*').forEach(e=>{[...e.attributes].forEach(a=>{ if(/^on/i.test(a.name)) e.removeAttribute(a.name); });});
      return c.outerHTML; };
    const PROPS = /* the IDENTICAL §3-A property list */ window.__PROPS;
    const init  = window.__INIT;   // §3-A per-property CSS-initial table (reuse if cached, else rebuild)
    const fnv = s => { let h=0x811c9dc5; for(let i=0;i<s.length;i++){h^=s.charCodeAt(i);h=Math.imul(h,0x01000193);} return (h>>>0).toString(16); };
    const sigs = new Map();
    for (const root of roots) for (const el of [root, ...root.querySelectorAll('*')]) {
      const cs = getComputedStyle(el); if (cs.display==='none') continue;
      const r = el.getBoundingClientRect();
      const kept = {}; for (const p of PROPS){ const v=cs[p]; if(v!==init[p]&&v!==''&&v!=null) kept[p]=v; }
      if (!Object.keys(kept).length) continue;
      const key = Object.keys(kept).sort().map(k=>k+':'+kept[k]+';').join(''); const h=fnv(key);
      let rec = sigs.get(h);
      if(!rec){ rec={signature:h,count:0,tag:el.tagName.toLowerCase(),sampleSelector:(el.id?'#'+el.id:el.tagName.toLowerCase()),rect:{x:+r.x.toFixed(1),y:+r.y.toFixed(1),w:+r.width.toFixed(1),h:+r.height.toFixed(1)},styles:kept}; sigs.set(h,rec); }
      rec.count++;
    }
    return JSON.stringify({ revealed_dom: roots.map(clean).join('\n'), computed:[...sigs.values()].sort((a,b)=>b.count-a.count) });
  })()
```

4. **(Optional) Screenshot the revealed state** for the human/QA trail (contract §11): take it with the Chrome extension's screenshot tool (`mcp__claude-in-chrome__computer` action `screenshot`) as a visual reference — the file may not persist to disk in this environment, so it's the lowest-rank corroboration, never the source of a value.
5. **ESCAPE / close the state** before the next interaction so captures stay clean — via `javascript_tool`: `document.activeElement.blur(); document.body.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true}))` (or click an empty area of `body`).
6. **Append** this interaction's object to the route's JSONL, combining the map entry with the `$REVEAL` string the `javascript_tool` returned in step 3:
   ```bash
   printf '%s\n%s\n' "$entry" "$REVEAL" | jq -s '{action_slug:.[0].action_slug, trigger:{selector:.[0].trigger, kind:.[0].kind}, revealed_dom:.[1].revealed_dom, computed:.[1].computed, notes:null}' \
     >> "$FRAG/$SLUG.interactions.tmp.jsonl"
   ```

After all interactions, fold the per-interaction objects into the route fragment (Bash):

```bash
jq -s '{page:"{PAGE}", interactions:.}' "$FRAG/$SLUG.interactions.tmp.jsonl" > "$FRAG/$SLUG.interactions.json"
jq -e '.interactions' "$FRAG/$SLUG.interactions.json" >/dev/null || echo "PARSE FAIL interactions"
```

> The before/after node-set diff (step 1 → step 3) is how you isolate the revealed UI through `javascript_tool`. If you prefer to confirm what mounted, `mcp__claude-in-chrome__read_page` / `find` after the trigger to locate the new toolbar/menu/composer/panel, then read its `outerHTML` and `getComputedStyle` over that subtree via `javascript_tool` for `revealed_dom` + `computed` — either path yields the same schema. The sequence above is the contract — adapt the mechanics, not the steps.

**Evidence order is unchanged** (CSSOM authored rules > CDP forced-state computed > deduped computed archetypes > screenshot estimate): `revealed_dom` + its `getComputedStyle` reads are direct measurement of the mounted UI; the optional screenshot is the lowest-rank corroboration, never the source of a value.

**Anti-hallucination.** If an interaction in the map cannot be performed (trigger not found, nothing new mounts, state gated behind auth), record that entry with `revealed_dom: null`, `computed: []`, and `notes: "<reason>"` — **never invent a toolbar/menu/panel from memory.** If the whole route is unreachable / auth-walled, emit `<promise>BLOCKED: reason</promise>` (contract §6). Anything recon listed in `unreached` for this route is carried through as a `null` entry with its reason — surfaced, not silently dropped.

---

## §3-D — CSS variables across ALL theme scopes → `css-variables.json` (shared, merge)

Harvest every custom property under every theme scope and resolve the **effective value per theme** by toggling the theme and re-reading `getPropertyValue` (not just reading authored rule text — computed resolves `var()` chains and `prefers-color-scheme`). Scopes: `:root, html, [data-theme], .dark, .light` and `@media (prefers-color-scheme: dark|light)`.

```js
(() => {
  // 1) collect every declared custom-property name from authored rules
  const names = new Set();
  const scan = (list) => { for (const r of list) {
    if (r.cssRules) { scan(r.cssRules); }
    if (r.style) for (const p of r.style) if (p.startsWith('--')) names.add(p);
  }};
  for (const sh of document.styleSheets) { try { scan(sh.cssRules); } catch(e){} }
  // also pull whatever is live on :root right now
  const rootCS = getComputedStyle(document.documentElement);

  const readAll = () => { const cs = getComputedStyle(document.documentElement); const o={}; for (const n of names) { const v = cs.getPropertyValue(n).trim(); if (v) o[n]=v; } return o; };

  // 2) snapshot current theme
  const htmlEl = document.documentElement;
  const prevTheme = htmlEl.getAttribute('data-theme');
  const prevClasses = htmlEl.className;

  // light
  htmlEl.setAttribute('data-theme','light'); htmlEl.classList.remove('dark'); htmlEl.classList.add('light');
  const light = readAll();
  // dark
  htmlEl.setAttribute('data-theme','dark'); htmlEl.classList.remove('light'); htmlEl.classList.add('dark');
  const dark = readAll();

  // restore
  if (prevTheme===null) htmlEl.removeAttribute('data-theme'); else htmlEl.setAttribute('data-theme',prevTheme);
  htmlEl.className = prevClasses;

  return JSON.stringify({ page:"{PAGE}", themes: { light, dark }, declaredNames:[...names] }, null, 0);
})()
```

Run via `mcp__claude-in-chrome__javascript_tool`; write the returned string to `/tmp/extract-{PAGE}/vars.json`, then MERGE into shared `css-variables.json` (read-modify-write; see §9).

> If the site has no theme attribute hooks, `light` and `dark` will be identical — that's fine, it means single-theme. If `getPropertyValue` returns empty for all names (Tailwind utility site with no custom props), write `{"themes":{"light":{},"dark":{}},"note":"utility-class site; tokens live in computed archetypes"}` and rely on §3-A.

---

## §3-E — Full CSSOM dump → `all-styles.json` (shared, merge) — REFETCH cross-origin

Iterate every sheet's `cssRules` (style + `@media` + `@container` + `@font-face` + `@keyframes` + `@supports`). **When `cssRules` throws (cross-origin), do NOT stub `/* cross-origin */`** — capture the sheet's `href` so we can `curl` and parse the real text on the shell side.

```js
(() => {
  const rules = []; const crossOrigin = [];
  const dump = (list) => { for (const r of list) rules.push(r.cssText); };
  for (const sh of document.styleSheets) {
    try { dump(sh.cssRules); }
    catch(e) { if (sh.href) crossOrigin.push(sh.href); }
  }
  return JSON.stringify({ page:"{PAGE}", inlineRules: rules, crossOriginHrefs: crossOrigin }, null, 0);
})()
```

Run the CSSOM dump via `mcp__claude-in-chrome__javascript_tool`; write the returned string to `/tmp/extract-{PAGE}/cssom.json`. Then REFETCH every cross-origin sheet as real text with Bash `curl` (this part is not browser-tool-specific — keep it):

```bash
# REFETCH every cross-origin sheet as real text (do NOT stub)
mkdir -p /tmp/extract-{PAGE}/sheets
for href in $(jq -r '.crossOriginHrefs[]' /tmp/extract-{PAGE}/cssom.json); do
  fn="/tmp/extract-{PAGE}/sheets/$(echo "$href" | shasum | cut -c1-12).css"
  curl -sL --max-time 20 "$href" -o "$fn" && echo "refetched $href -> $fn"
done
# fold inline rules + refetched sheet text into one rules array, then MERGE into shared all-styles.json (§9)
jq -n --slurpfile c /tmp/extract-{PAGE}/cssom.json \
  --rawfile combined <(cat /tmp/extract-{PAGE}/sheets/*.css 2>/dev/null) \
  '{page:$c[0].page, inlineRules:$c[0].inlineRules, refetchedCss:$combined}' \
  > /tmp/extract-{PAGE}/all-styles.partial.json
```

If a `curl` fails (403/timeout), record `{"href":..., "status":"refetch-failed", "reason":"..."}` in the merged file — null + reason, never a stub that pretends success.

---

## §3-F — Fonts → `fonts.json` (shared, merge) + download bytes to `assets/fonts/`

Capture `@font-face` rules **and** the actually-loaded set (`Array.from(document.fonts)` filtered to `status==='loaded'`). Resolve each `src url()` to an absolute URL, **download the woff2/woff/ttf bytes**, and record variable-font `fvar` axes (e.g. `wght 100 900`).

```js
(() => {
  const faces = [];
  const scan = (list) => { for (const r of list) { if (r.cssRules) scan(r.cssRules); if (r.type===CSSRule.FONT_FACE_RULE || r.constructor.name==='CSSFontFaceRule') {
    faces.push({ family: r.style.getPropertyValue('font-family'), src: r.style.getPropertyValue('src'), weight: r.style.getPropertyValue('font-weight'), style: r.style.getPropertyValue('font-style'), stretch: r.style.getPropertyValue('font-stretch'), display: r.style.getPropertyValue('font-display'), unicodeRange: r.style.getPropertyValue('unicode-range') });
  }}};
  for (const sh of document.styleSheets) { try { scan(sh.cssRules); } catch(e){} }
  const loaded = Array.from(document.fonts).filter(f=>f.status==='loaded').map(f=>({ family:f.family, weight:f.weight, style:f.style, stretch:f.stretch, unicodeRange:f.unicodeRange, variationSettings:f.variationSettings, ascentOverride:f.ascentOverride }));
  // resolve every url() in src to absolute
  const urls = []; for (const f of faces) { const re=/url\(\s*['"]?([^'")]+)['"]?\s*\)/g; let m; while((m=re.exec(f.src))) urls.push(new URL(m[1], location.href).href); }
  // external font CSS (Google/Typekit) for the shell to refetch & parse for nested url()
  const links = Array.from(document.querySelectorAll('link[rel=stylesheet][href*="font"],link[href*="fonts.googleapis"],link[href*="use.typekit"],link[href*="fonts.cdnfonts"]')).map(l=>l.href);
  return JSON.stringify({ page:"{PAGE}", faces, loaded, fontFileUrls:[...new Set(urls)], externalFontCss: links }, null, 0);
})()
```

Run the fonts capture via `mcp__claude-in-chrome__javascript_tool`; write the returned string to `/tmp/extract-{PAGE}/fonts.json`. Then download the resolved font bytes with Bash `curl` (keep — not browser-tool-specific):

```bash
# download every resolved font file as real bytes
for u in $(jq -r '.fontFileUrls[]' /tmp/extract-{PAGE}/fonts.json); do
  ext="${u##*.}"; ext="${ext%%\?*}"; [ "$ext" = "$u" ] && ext="woff2"
  fn="$EXT/assets/fonts/$(echo "$u" | shasum | cut -c1-12).$ext"
  curl -sL --max-time 20 "$u" -o "$fn" && echo "font $u -> $fn"
done
# external font CSS (Google) often hides the real woff2 behind @font-face in the CSS file:
for css in $(jq -r '.externalFontCss[]' /tmp/extract-{PAGE}/fonts.json); do
  curl -sL --max-time 20 -A "Mozilla/5.0" "$css" | grep -oE "https://[^)]+\.(woff2|woff|ttf)" | while read -r fu; do
    fn="$EXT/assets/fonts/$(echo "$fu" | shasum | cut -c1-12).woff2"; curl -sL "$fu" -o "$fn"; done
done
```

**Variable-font fvar axes.** For any font where `loaded[].variationSettings` is non-trivial or the family name hints variable, record the axes (`wght`, `wdth`, `opsz`, `slnt`, custom). If undetectable from `document.fonts`, note the family + `fvar:null, reason:"axes not exposed by document.fonts; inspect downloaded file"` — never invent a range. Then MERGE into shared `fonts.json` (§9).

---

## §3-G — Assets → `assets.json` (shared, merge) + download bytes to `assets/{img,svg}/`

Resolve **every** raster source (`img.currentSrc` + parsed `srcset`/`sizes`), CSS `url()` backgrounds (from the computed archetypes — the gradients stay inline, the `url()`s get downloaded), favicons (`<link rel~=icon>`), and OG/Twitter images (`meta[property^=og:image]`, `meta[name^=twitter:image]`). **Download the bytes with `curl -sL`.** For inline SVG, emit the **FULL `outerHTML`** — NO 500-char truncation, NO 20-element cap (those caps are deleted). For `<svg><use href="#id">` sprites, fetch the sprite file.

```js
(() => {
  const abs = u => { try { return new URL(u, location.href).href; } catch(e){ return null; } };
  const images = Array.from(document.querySelectorAll('img')).map(el => ({
    currentSrc: el.currentSrc || el.src, src: el.getAttribute('src'),
    srcset: el.getAttribute('srcset'), sizes: el.getAttribute('sizes'),
    alt: el.alt, loading: el.loading, naturalWidth: el.naturalWidth, naturalHeight: el.naturalHeight,
    urls: [...new Set([el.currentSrc, ...(el.getAttribute('srcset')||'').split(',').map(s=>s.trim().split(/\s+/)[0])].filter(Boolean).map(abs))]
  }));
  // CSS url() backgrounds from live computed styles
  const bgUrls = new Set();
  for (const el of document.querySelectorAll('*')) { const bi = getComputedStyle(el).backgroundImage; if (bi && bi.includes('url(')) { const re=/url\(\s*['"]?([^'")]+)['"]?\s*\)/g; let m; while((m=re.exec(bi))) { const a=abs(m[1]); if(a) bgUrls.add(a); } } }
  const favicons = Array.from(document.querySelectorAll('link[rel~=icon],link[rel="apple-touch-icon"],link[rel="mask-icon"]')).map(l=>abs(l.href)).filter(Boolean);
  const og = Array.from(document.querySelectorAll('meta[property^="og:image"],meta[name^="twitter:image"]')).map(m=>abs(m.content)).filter(Boolean);
  // inline SVGs — FULL outerHTML, no truncation, no cap
  const inlineSvgs = Array.from(document.querySelectorAll('svg')).map((el,i)=>({ index:i, id:el.id||null, classes:(el.getAttribute('class')||''), viewBox:el.getAttribute('viewBox'), width:el.getAttribute('width'), height:el.getAttribute('height'), outerHTML: el.outerHTML }));
  // <use href> sprite refs to fetch
  const spriteRefs = [...new Set(Array.from(document.querySelectorAll('use')).map(u=>u.getAttribute('href')||u.getAttribute('xlink:href')).filter(h=>h&&!h.startsWith('#')).map(abs))];
  return JSON.stringify({ page:"{PAGE}", images, bgUrls:[...bgUrls], favicons, og, inlineSvgs, spriteRefs }, null, 0);
})()
```

Run the assets capture via `mcp__claude-in-chrome__javascript_tool`; write the returned string to `/tmp/extract-{PAGE}/assets.json`. Then download the bytes with Bash `curl` (keep — not browser-tool-specific):

```bash
dl() { # url -> dir ; content-hashed filename, records failures
  local u="$1" dir="$2"; [ -z "$u" ] && return
  local ext="${u##*.}"; ext="${ext%%\?*}"; case "$ext" in svg|png|jpg|jpeg|webp|avif|gif|ico) ;; *) ext="bin";; esac
  local fn="$dir/$(echo "$u" | shasum | cut -c1-12).$ext"
  if curl -sL --max-time 25 -A "Mozilla/5.0" "$u" -o "$fn" && [ -s "$fn" ]; then echo "ok $u -> $fn"; else echo "FAIL $u" >> /tmp/extract-{PAGE}/asset-failures.txt; rm -f "$fn"; fi
}
for u in $(jq -r '.images[].urls[]?' /tmp/extract-{PAGE}/assets.json | sort -u); do dl "$u" "$EXT/assets/img"; done
for u in $(jq -r '.bgUrls[]?, .favicons[]?, .og[]?' /tmp/extract-{PAGE}/assets.json | sort -u); do
  case "$u" in *.svg*) dl "$u" "$EXT/assets/svg";; *) dl "$u" "$EXT/assets/img";; esac; done
for u in $(jq -r '.spriteRefs[]?' /tmp/extract-{PAGE}/assets.json | sort -u); do dl "$u" "$EXT/assets/svg"; done
```

**No placeholders rule (contract §3-G).** The build must NEVER fall back to picsum/pravatar **unless** a genuine download failed — and that failure must be logged in `asset-failures.txt` and surfaced in `assets.json`. MERGE into shared `assets.json` (§9), recording for each downloaded file its source URL, local path, content hash, ext, and intrinsic `naturalWidth/Height` where known.

---

## §3-H — Layout / breakpoints / stacking → `fragments/{slug}.layout.json`

Capture the **real** breakpoints (`@media`/`@container` `conditionText` — not the 768/375 guess), the stacking-context map (every positioned/transformed/opacity<1/filtered node + its `zIndex`), and per-archetype rects (already in §3-A; reference them).

```js
(() => {
  const media = []; const container = [];
  const scan = (list) => { for (const r of list) {
    if (r.type===CSSRule.MEDIA_RULE || r.constructor.name==='CSSMediaRule') media.push(r.conditionText || r.media.mediaText);
    if (r.constructor.name==='CSSContainerRule') container.push({ name:r.containerName, condition:r.containerQuery||r.conditionText });
    if (r.cssRules) scan(r.cssRules);
  }};
  for (const sh of document.styleSheets) { try { scan(sh.cssRules); } catch(e){} }
  // stacking contexts: positioned / transformed / filtered / opacity<1 / will-change / isolation
  const stack = [];
  for (const el of document.querySelectorAll('*')) {
    const cs = getComputedStyle(el);
    const creates = (cs.position!=='static' && cs.zIndex!=='auto') || cs.transform!=='none' || cs.filter!=='none' || cs.backdropFilter!=='none' || parseFloat(cs.opacity)<1 || cs.willChange!=='auto' || cs.isolation==='isolate' || cs.mixBlendMode!=='normal';
    if (!creates) continue;
    const r = el.getBoundingClientRect();
    stack.push({ selector: el.tagName.toLowerCase()+(el.id?'#'+el.id:'')+(el.className&&el.className.toString?('.'+el.className.toString().trim().split(/\s+/).slice(0,2).join('.')):''), position:cs.position, zIndex:cs.zIndex, transform:cs.transform!=='none', opacity:cs.opacity, isolation:cs.isolation, rect:{x:+r.x.toFixed(1),y:+r.y.toFixed(1),w:+r.width.toFixed(1),h:+r.height.toFixed(1)} });
  }
  return JSON.stringify({ page:"{PAGE}", viewport:"desktop", mediaConditions:[...new Set(media)], containerConditions:container, stackingContexts: stack.sort((a,b)=>(parseInt(b.zIndex)||0)-(parseInt(a.zIndex)||0)) }, null, 0);
})()
```

Run via `mcp__claude-in-chrome__javascript_tool`; write the returned string to `$FRAG/$SLUG.layout.json`.

The `mediaConditions` array is the **measured** breakpoint set — the design-spec agent uses these, not the viewport guesses.

---

## §3-I — Framework fingerprint (record in `recon.json`; do not duplicate if present)

Recon usually writes this already. **Read `01-recon/recon.json` first** — if `frameworks` is populated, skip. Only if absent, detect and patch it (read-modify-write, §9): `__NEXT_DATA__`/`self.__next_f` (Next.js), `__remixContext` (Remix), `__NUXT__` (Nuxt), `[data-reactroot]`/React fiber keys (React), `ng-version` (Angular), `[data-v-*]` (Vue), `[data-astro-*]` (Astro); Tailwind via `--tw-*` custom props or utility-class density; asset hosts (`_next/static`, `/assets/index-*` Vite); `<meta name=generator>`.

```js
(() => ({ next: !!(window.__NEXT_DATA__||self.__next_f), remix: !!window.__remixContext, nuxt: !!window.__NUXT__, react: !!document.querySelector('[data-reactroot]')||!!Object.keys(document.body||{}).find(k=>k.startsWith('__react')), angular: !!document.querySelector('[ng-version]'), vue: !!document.querySelector('*[data-v-app],*[__vue__]'), astro: !!document.querySelector('[data-astro-cid],[data-astro-source-file]'), tailwind: getComputedStyle(document.documentElement).getPropertyValue('--tw-ring-color')!=='' || /\b(flex|grid|px-\d|text-\w+-\d)\b/.test(document.body.className), generator: (document.querySelector('meta[name=generator]')||{}).content||null, assetHosts: [...new Set(Array.from(document.querySelectorAll('script[src],link[href]')).map(e=>{try{return new URL(e.src||e.href).pathname.split('/').slice(0,3).join('/')}catch(_){return null}}).filter(Boolean))].slice(0,12) }))()
```

Run via `mcp__claude-in-chrome__javascript_tool`. Wrap the result and patch into `recon.json` only if it lacks `frameworks`.

---

## Also: cleaned DOM → `fragments/{slug}.dom.html`

Read the full markup with `mcp__claude-in-chrome__javascript_tool` (`document.documentElement.outerHTML`) — or `mcp__claude-in-chrome__read_page` — and write the returned string to `/tmp/extract-{PAGE}/raw.html`. Then strip script bodies + inline event handlers with Bash (not browser-tool-specific), keeping structure/classes/`data-*`/inline `style`:

```bash
# strip script bodies + inline event handlers but KEEP structure, classes, data-*, inline style attrs
node -e 'const fs=require("fs");let h=fs.readFileSync("/tmp/extract-{PAGE}/raw.html","utf8");h=h.replace(/<script[\s\S]*?<\/script>/gi,"<script></script>").replace(/ on[a-z]+="[^"]*"/gi,"");fs.writeFileSync(process.argv[1],h);' "$FRAG/$SLUG.dom.html"
```

Keep classes, `data-*`, ARIA, and inline `style=` attributes — they're evidence. Only script bodies and inline event handlers are stripped.

---

## §9 — Shared-file merge (read-modify-write)

`css-variables.json`, `all-styles.json`, `fonts.json`, `assets.json` accumulate values from **every** route. Extraction runs sequentially (one Chrome, one route at a time), so there's no concurrent writer — but you still **never blind-overwrite**: each route reads the existing shared file, folds in its partial, and writes back, so earlier routes' values are preserved. (The `mkdir` directory-lock below is harmless under sequential runs and keeps the merge robust if a run is ever parallelized; the `merge_shared` helper and `jq` merge exprs are unchanged.)

```bash
merge_shared() { # $1=target shared file ; $2=this route's partial ; $3=jq merge expr
  local target="$EXT/$1" partial="$2" expr="$3" lock="$EXT/.lock-$1"
  for i in $(seq 1 100); do mkdir "$lock" 2>/dev/null && break; sleep 0.2; done
  [ -f "$target" ] || echo '{}' > "$target"
  jq -s "$expr" "$target" "$partial" > "$target.tmp" && mv "$target.tmp" "$target"
  rmdir "$lock"
}

# css-variables.json — union theme maps across routes (later non-empty wins per key)
merge_shared css-variables.json /tmp/extract-{PAGE}/vars.json \
  '{themes:{light:((.[0].themes.light//{})+(.[1].themes.light//{})), dark:((.[0].themes.dark//{})+(.[1].themes.dark//{}))}, declaredNames:((.[0].declaredNames//[])+(.[1].declaredNames//[])|unique)}'

# all-styles.json — collect per-page rule sets keyed by page (dedupe identical sheets at design-spec time)
merge_shared all-styles.json /tmp/extract-{PAGE}/all-styles.partial.json \
  '{pages:((.[0].pages//[])+[{page:.[1].page, inlineRuleCount:(.[1].inlineRules|length)}]), inlineRules:((.[0].inlineRules//[])+(.[1].inlineRules//[])|unique), refetchedCss:((.[0].refetchedCss//"")+"\n"+(.[1].refetchedCss//""))}'

# fonts.json — union faces + loaded + file urls
merge_shared fonts.json /tmp/extract-{PAGE}/fonts.json \
  '{faces:((.[0].faces//[])+(.[1].faces//[])|unique), loaded:((.[0].loaded//[])+(.[1].loaded//[])|unique), fontFileUrls:((.[0].fontFileUrls//[])+(.[1].fontFileUrls//[])|unique), externalFontCss:((.[0].externalFontCss//[])+(.[1].externalFontCss//[])|unique)}'

# assets.json — union manifests
merge_shared assets.json /tmp/extract-{PAGE}/assets.json \
  '{images:((.[0].images//[])+(.[1].images//[])), bgUrls:((.[0].bgUrls//[])+(.[1].bgUrls//[])|unique), favicons:((.[0].favicons//[])+(.[1].favicons//[])|unique), og:((.[0].og//[])+(.[1].og//[])|unique), inlineSvgs:((.[0].inlineSvgs//[])+(.[1].inlineSvgs//[])), spriteRefs:((.[0].spriteRefs//[])+(.[1].spriteRefs//[])|unique)}'
```

(Downloaded byte files in `assets/{img,svg,fonts}/` use content-hashed names, so concurrent writes of the same asset are idempotent — no lock needed for the binaries.)

---

## Completion checklist (contract §1 + §7)

Per-route fragments (you own — overwrite):
- [ ] `fragments/{slug}.computed.json` — signature-deduped archetypes, delta-from-default, full §3-A property set, rects (§3-A)
- [ ] `fragments/{slug}.pseudo.json` — `::before/::after/::placeholder/::marker/::selection/::backdrop` where real (§3-B)
- [ ] `fragments/{slug}.states.json` — `:hover/:focus/:active` rules from authored CSSOM (primary) and any forced-`:focus` computed deltas, with `evidence_method` (§3-C)
- [ ] `fragments/{slug}.interactions.json` — DOM + computed styles of interaction-REVEALED UI (toolbar/menu/composer/panel), one entry per `interaction-map.json` action (Interaction-state extraction)
- [ ] `fragments/{slug}.layout.json` — measured `@media`/`@container` conditions + stacking-context map + rects (§3-H)
- [ ] `fragments/{slug}.dom.html` — cleaned outerHTML

Shared (read-modify-write merge, §9):
- [ ] `css-variables.json` — `{themes:{light,dark}}` (§3-D)
- [ ] `all-styles.json` — full CSSOM incl. **refetched** cross-origin sheets, never stubbed (§3-E)
- [ ] `fonts.json` + `assets/fonts/*` bytes + fvar axes (§3-F)
- [ ] `assets.json` + `assets/{img,svg}/*` bytes, full inline-SVG `outerHTML`, no placeholders (§3-G)
- [ ] `recon.json` framework fingerprint present (§3-I)

**Evidence & honesty:** every value traces to a `getComputedStyle` / CSSOM read / downloaded byte. Authoritative order **CSSOM rules > CDP forced-state computed > computed archetypes > screenshot**. Any value you cannot read → `null` + `reason`; never invent, never carry from memory. If the route is unreachable / auth-walled, emit `<promise>BLOCKED: reason</promise>`.

Set this task's flag in `status.json`, then end with `<promise>CONTINUE</promise>`.

---

## States manifest + large-data extraction

Maintain `02-extraction/STATES-MANIFEST.md`: one row per view/state from `01-recon/interaction-map.json`, with columns `screenshot` and `code extracted`. Check `code extracted` only once you've actually pulled that state's computed styles / DOM. This is your punch-list — work down it; don't stop until every row's code column is checked. The coverage critic gates on it.

**Large JSON / SVG extraction — beat the truncation.** `javascript_tool` results are truncated (~1.2k chars), so a big computed-style dump or full SVG markup won't come back inline. Workaround: have the page build the JSON/markup and trigger a download (a `Blob` + a synthetic `<a download>` click) — the full file lands in `~/Downloads`, then `mv` it into the workspace (e.g. `02-extraction/fragments/...`). No truncation, fully accurate. **Heads-up:** Chrome blocks *repeated* automatic downloads from a site until the user allows them — allow downloads for the target once, up front, or every download after the first silently fails.
