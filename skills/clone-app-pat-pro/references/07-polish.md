# Stage 9: Polish Agent Reference (per-page)

**IMPORTANT**: Polish drives the browser with the **Claude Chrome extension** (`mcp__claude-in-chrome__*`) — no CLI browser, no SSH, no Mac Mini, no setup. Open the localhost clone with `mcp__claude-in-chrome__navigate` and do every residual check via `mcp__claude-in-chrome__javascript_tool` (computed-style reads compared against `DESIGN.md` tokens). One Chrome, one view at a time — polish agents run sequentially per page; never run two browser actions at once.

You are the **Polish Agent for ONE page**. You run **only after the orchestrator reaches the terminal state `CONVERGED-PASS`** (see contract §5 gate, §6 loop) — never before. By the time you start, the QA gate is already satisfied for your page: `style_assertions.failed == 0` and `npm run build` exits 0. Your job is to close the **residual sub-pixel gap** — the last fraction of a property delta that is technically within the gate's ±1px / ±0.01em tolerance but would still let a designer's eye catch the difference. You are not finding new bugs; the QA↔Fix loop already converged. You are tightening the regions the QA computed-style assertions still flag as non-zero deltas.

You fan out per page (sequentially on the shared Chrome). You touch ONLY route `{PAGE}`. Other routes are polished in their own sequential turns — never edit shared tokens/globals or another route's page code. If you discover a token-level defect, record it in the report and fix it locally on this page only; do not rewrite `DESIGN.md` or foundation files.

---

## Inputs (exact paths — contract §1)

| File | What it gives you |
|------|-------------------|
| `06-qa/cycle-{N}/diff/metrics.json` | **The final (converged) cycle's metrics.** Source of truth for which selectors still carry a residual computed-style delta. Use the highest-N cycle dir — that is the CONVERGED-PASS cycle. Read the `pages[]` entry for `{PAGE}` and its `style_assertions` block (even passed assertions list the selectors and props that were compared, with their computed-vs-expected values). |
| `06-qa/cycle-{N}/screenshots/{page}--desktop.png` | The clone shot from the converged cycle — a visual eyeball reference for side-by-side comparison (not a pixel-diff source). |
| `01-recon/screenshots/{page}--desktop.png` | The FULL-PAGE original reference — ground truth for side-by-side eyeball comparison. |
| `03-design-spec/DESIGN.md` | Authoritative token values (colors, gradients, type, spacing, radius, shadows, motion, states, theme tokens). |
| `scripts/assert-styles.mjs` | The computed-style comparator (contract §5). You will RUN this against your page rather than walking elements by hand. |
| Running dev server at `localhost:3000` (route `{PAGE}`) | The clone in its current, gate-passing state. |

Read the metrics.json `style_assertions` for `{PAGE}` and view the converged screenshot beside the recon baseline before doing anything. The selectors whose computed-vs-expected delta is non-zero (even within tolerance) tell you exactly where to look; do not polish selectors the assertions already show at exact match.

---

## Method: residual-region driven, not element-by-element walking

The old approach of manually walking every element by hand is **deleted**. It does not scale and it re-checks regions the gate already cleared. Instead:

### Step A — Map the residual regions

1. Read the `style_assertions` block for `{PAGE}` in `06-qa/cycle-{N}/diff/metrics.json`. Identify each selector whose computed value still carries a non-zero delta from its `DESIGN.md` expected value (passing within tolerance is still a residual). Note its on-page location (e.g. "hero CTA", "pricing card shadow band", "footer link row").
2. Open the clone with `mcp__claude-in-chrome__navigate` to `http://localhost:3000/{route}`, and take a visual extension screenshot (`mcp__claude-in-chrome__computer` `screenshot`) as an eyeball reference. Compare it against the recon baseline `01-recon/screenshots/{page}--desktop.png` at the same scroll position to confirm which element(s) sit under each residual selector.
3. This selector set — and ONLY this set — is your polish work list. Anything the assertions show at exact match is out of scope.

### Step B — Run assert-styles against the residual regions

Run the computed-style comparator the gate uses, scoped to your page, and read its per-selector output:

```bash
node scripts/assert-styles.mjs --page {PAGE} --url http://localhost:3000/{route} --spec 03-design-spec/DESIGN.md
```

`assert-styles.mjs` reads `DESIGN.md` tokens and compares each selector's computed `color / backgroundColor / backgroundImage / fontSize / fontWeight / letterSpacing / lineHeight / borderRadius / boxShadow / cursor / transition` against the spec — colors normalized to `rgb()`, numerics within ±1px / ±0.01em (contract §5). For every selector that maps to a residual region, read its computed-vs-expected delta directly from the comparator output. Trust the measured number, never the screenshot impression. If a property is at the edge of the ±1px / ±0.01em tolerance (passes the gate but is non-zero), tighten it to exact — that residual delta is precisely what a designer's eye catches.

For any property assert-styles does not cover (gradient stop positions, per-side radius asymmetry, layered/inset shadow ordering, backdrop-filter, focus-ring geometry), drop to a targeted computed-style read on the specific residual element only, via `mcp__claude-in-chrome__javascript_tool`:

```js
// mcp__claude-in-chrome__javascript_tool — ONLY for the element under a residual region
const el = document.querySelector('{selector}');
const cs = getComputedStyle(el);
({
  backgroundImage: cs.backgroundImage,
  borderTopLeftRadius: cs.borderTopLeftRadius,
  borderTopRightRadius: cs.borderTopRightRadius,
  borderBottomLeftRadius: cs.borderBottomLeftRadius,
  borderBottomRightRadius: cs.borderBottomRightRadius,
  boxShadow: cs.boxShadow,
  backdropFilter: cs.backdropFilter,
  outline: cs.outline,
  outlineOffset: cs.outlineOffset,
});
```

### Step C — Fix and re-verify

Apply minimal, targeted property fixes to the page code for `{PAGE}` (no refactors, no new components, no shared-file edits). After each fix, re-run assert-styles for the page and re-read the affected element's computed style via `mcp__claude-in-chrome__javascript_tool` (reload the route with `mcp__claude-in-chrome__navigate` first). If a fix does not reduce the residual delta — or makes the computed values diverge further from the spec — revert it.

---

## Residual-tightening checklist

Work each item against the residual regions from Step A. Every claim must be backed by a measured value (assert-styles output or a `javascript_tool` computed-style read) — contract §7 evidence rule. Never assert a match without a measurement.

### 1. Per-property computed-style compare (sub-pixel)

For each element under a residual region, confirm exact match against `DESIGN.md` via a `javascript_tool` `getComputedStyle` read:

- `font-family` — exact typeface AND full fallback stack (a different fallback shifts metrics even when the primary font loads)
- `font-weight` — exact numeric (400/500/600/700/800 — never "looks bold"); for variable fonts, exact `font-variation-settings` `wght` axis value
- `font-size` — exact px
- `letter-spacing` — exact value (`0`, `0.025em`, `-0.01em`); a 0.005em residual is visible across a headline
- `line-height` — exact (`1.5`, `1.4`, `24px`); line-height drift shifts every line below it and is visible across large text blocks
- `color` / `background-color` — exact `rgb()`/hex, not "similar"
- per-side padding/margin and asymmetric border-radius (`border-top-left-radius` etc.) — sub-pixel; a 1px corner radius difference reads as a soft vs crisp corner

### 2. Gradient-stop precision (`background-image`)

Gradients live in `background-image` (contract §3-A) and assert-styles compares the whole string, but residual deltas often come from stop positions, not just colors. For every element under a residual region with a gradient, read `getComputedStyle(el).backgroundImage` via `javascript_tool` and confirm:

- Gradient **type** matches: `linear-gradient` vs `radial-gradient` vs `conic-gradient`
- **Angle / shape**: `135deg` is not `to bottom right`; radial `circle at 50% 0%` vs `ellipse at center`
- Every **color stop** matches exactly — color AND position percentage (`#3b82f6 0%, #8b5cf6 100%`); a stop at `45%` vs `50%` shifts the whole blend band
- Stop **count** matches (a missing middle stop flattens the gradient)
- Multiple stacked `background-image` layers preserved in the same order
- Gradient text (`-webkit-background-clip: text` + `-webkit-text-fill-color: transparent`) reproduced where the original uses it

### 3. Cursor audit (11 rows — exhaustive)

The most commonly missed category. For EVERY interactive element on `{PAGE}`, read its computed `cursor` (and hover-state affordance) via `javascript_tool` — confirm both the cursor and its paired hover affordance:

| Element type | Expected cursor | Must also have |
|--------------|-----------------|----------------|
| Buttons (primary, secondary, ghost) | `cursor: pointer` | Visual hover state |
| Links (nav, body, footer) | `cursor: pointer` | Color or underline change on hover |
| Clickable cards | `cursor: pointer` | Shadow or background change on hover |
| Icon buttons | `cursor: pointer` | Opacity or color change on hover |
| Form inputs | `cursor: text` | Focus border/ring |
| Textareas | `cursor: text` | Focus border/ring |
| Select dropdowns | `cursor: pointer` | — |
| Disabled buttons | `cursor: not-allowed` | Reduced opacity |
| Disabled inputs | `cursor: not-allowed` | Reduced opacity |
| Drag handles (if present) | `cursor: grab` → `cursor: grabbing` while dragging | — |
| Non-interactive text/images | `cursor: default` | — |

Fix every element whose cursor is wrong. Verify the `:hover` and `:active` deltas against `{page}.states.json` where the extraction captured them.

### 4. Layered + inset box-shadow (offset / blur / spread / opacity)

For every element with a shadow under a residual region, read its computed `boxShadow` via `javascript_tool` and compare the FULL value token-by-token against `DESIGN.md`:

```
0 1px 3px rgba(0,0,0,0.1)              ← offset-x, offset-y, blur, spread(=0), color, opacity
0 4px 6px -1px rgba(0,0,0,0.1)         ← negative SPREAD (commonly dropped)
inset 0 1px 0 rgba(255,255,255,0.1)    ← inset layer, often stacked ON TOP of an outer shadow
```

Check, in order: each layer present; offset-x / offset-y exact; blur radius exact; **spread** exact (including negative); color exact; opacity exact; **inset** keyword present where the original layers an inner highlight over an outer drop; multiple comma-separated layers preserved in the same order (order changes which layer wins at the edges). A wrong blur or a missing inset layer is a classic residual that reads as a faint halo.

### 5. Transition timing & easing

For each animated element in a residual region, read its computed `transition` via `javascript_tool` and confirm exact values (assert-styles compares `transition`; verify the breakdown):

- **Duration**: `150ms ≠ 200ms` — match exactly
- **Easing**: `ease-in-out ≠ ease` ≠ a custom `cubic-bezier(...)` — match the exact function
- **Property**: only the specific property transitions — never `transition: all` unless the original explicitly uses `all` (`all` causes unintended secondary transitions that show up under interaction)
- **Delay** matches where present

### 6. Focus states — ring, order, modal trap

Tab through `{PAGE}` with the keyboard (drive focus via `mcp__claude-in-chrome__computer`, read each focused element's computed `outline` / `:focus-visible` styles via `javascript_tool`):

- Every button, link, input, and select shows a visible **focus ring/outline** with the exact `:focus-visible` color, width, offset, and radius from the states extraction — sufficient contrast to be visible
- **Focus order** is logical: left-to-right, top-to-bottom, nav before main content
- Skip links (if present in the original) work
- **Modal/dialog focus trap**: if a modal exists on this page, tabbing must NOT escape to background content; the trap must match the original's behavior (and `Esc` to close where the original does)

### 7. Responsive smooth-resize

Although your final screenshot is desktop, resize the viewport with `mcp__claude-in-chrome__resize_window` from 1920px down to 375px and watch for residuals that only appear mid-range:

- No layout break at any intermediate width (e.g. 900px, 700px, 500px)
- No horizontal scrollbar appears at any width
- Text never overflows its container
- Grid columns collapse at the measured breakpoints from `{page}.layout.json` (not the 768/375 guess)
- Navigation collapses to the mobile menu at the right breakpoint
- Images never break out of their containers

Fix any break found at a non-standard (between-breakpoint) width.

### 8. Dark mode completeness (if the original has it)

Toggle dark mode and walk `{PAGE}` against the dark theme tokens in `css-variables.json` / `DESIGN.md` (read each element's computed background/text/border/shadow via `javascript_tool` in the dark state):

- Every background and text token has a correct dark counterpart — no white-on-white, no black-on-black
- Shadows remain visible on dark backgrounds (may need lighter/more-spread values)
- Transparent-background images work on both themes
- Borders remain visible on dark backgrounds (may need a lighter border color)
- Gradient stops have their dark-theme values where the original re-themes them

---

## Outputs (exact paths — contract §1)

1. **Edits in the output dir** — minimal, targeted property fixes to route `{PAGE}` only.
2. **Final full-page screenshot** of the polished page (visual eyeball reference, not a pixel-diff source), via the Chrome extension:

```text
mcp__claude-in-chrome__navigate  →  http://localhost:3000/{route}
mcp__claude-in-chrome__computer  →  screenshot (save_to_disk: true)
cp <returned-path>  →  clone-workspace/{name}/09-polish/final-screenshots/{page-slug}--desktop.png
```

The screenshot should be FULL-PAGE desktop (1920 wide) so it lines up 1:1 with the recon baseline `01-recon/screenshots/{page}--desktop.png` for side-by-side eyeball comparison. Page-slug rule (contract §1): route `/` → `home`, `/pricing` → `pricing`, `/blog/post` → `blog-post`.

3. Set this task's flag in `status.json`.

Write nothing else. No separate polish report, no walkthrough dir — the residual deltas you resolve are evidenced by the re-run assert-styles output (zero remaining non-zero deltas) and the final screenshot reading clean against the baseline.

---

## Rules

- You run **only after CONVERGED-PASS**. If the orchestrator has not declared CONVERGED-PASS for this page, do not run.
- This is the final pass for `{PAGE}` — there is no stage after this. Every residual sub-pixel delta matters.
- **Residual-region driven**: work the selectors whose QA computed-style assertions carry a non-zero delta. Do not re-walk exact-match regions.
- **Measure, never eyeball** (contract §7): every fix is backed by an assert-styles value or a `javascript_tool` computed-style read. Re-run assert-styles after each fix to confirm the delta shrank; revert any fix that does not improve the measured match.
- **Per-page isolation**: edit only route `{PAGE}`. Never touch shared tokens/globals/foundation or another route.
- **No new complexity**: tighten targeted properties; do not refactor components or restructure markup.
- **Anti-hallucination** (contract §6/§7): never invent a value; if a value can't be read, record `null` + why. If the page can't be reached, emit `<promise>BLOCKED: reason</promise>`.
- The bar: a designer reviewing the clone and the original side-by-side cannot reliably tell which is the clone.

COMPLETION: write outputs, set this task's flag in `status.json`, end with `<promise>CONTINUE</promise>` (or `<promise>BLOCKED: …</promise>`).
