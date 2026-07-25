# Clone Pipeline Contract — single source of truth

Every stage agent, the in-conversation orchestrator (the live Claude session), and the verification scripts obey THIS file. It defines the workspace layout, the exact artifact filenames each stage reads and writes, the parallel fan-out keys, the computed-style-assertion gate, the convergence loop, and the agent-prompt standard. If a stage prompt and this contract disagree, the contract wins.

This skill runs **IN-CONVERSATION**: the live Claude orchestrates Task sub-agents, drives the **Claude Chrome extension** (`mcp__claude-in-chrome__*`) to recon/extract/QA, and runs the helper scripts via Bash. Because you're already logged into Chrome, the browser reaches authed sites. There is **one Chrome** — browser stages are **sequential** (one view/tab at a time); **code stages fan out in parallel** via Task sub-agents.

The mission: **own the target — pixel for pixel.** Extract every value that exists in the live page (read off the DOM/CSSOM, not a screenshot guess), rebuild it, and prove the match with **measured computed-style assertions**, not an opinion. Leave no stone unturned.

**Browser tool = the Claude Chrome extension.** Use it for every browser action:

| Need | Chrome-extension tool |
|---|---|
| open a route | `mcp__claude-in-chrome__navigate` |
| read computed styles / CSSOM / run JS (the verification ground truth) | `mcp__claude-in-chrome__javascript_tool` |
| read DOM / find elements | `mcp__claude-in-chrome__read_page` / `find` |
| click / hover / focus (interaction sweep) + visual-reference screenshot | `mcp__claude-in-chrome__computer` |
| set viewport | `mcp__claude-in-chrome__resize_window` |

Asset/font byte downloads and cross-origin sheet refetch use **Bash `curl`** (not browser-specific). The objective ground truth is **computed styles read via `javascript_tool`**, never a screenshot.

---

## 1. Workspace layout (exact paths)

All artifacts live under `clone-workspace/{name}/`. Filenames are fixed — agents must read/write these exact names so downstream stages and the orchestrator find them.

```
clone-workspace/{name}/
├── 00-config.json                 # target_url, viewports, pages[], stack, gate thresholds
├── status.json                    # per-task manifest (resume); see §6
├── progress.md                    # human log
├── 01-recon/
│   ├── sitemap.json               # { "routes": ["/", "/pricing", ...] }
│   ├── screenshots/                # VISUAL-REFERENCE shots only (eyeball, NOT the gate — §11)
│   │   ├── {page}--{viewport}.png        # visual-reference of each view
│   │   ├── hover-states/{page}--{el}.png
│   │   └── interaction-states/{page}--{action-slug}.png  # state revealed by an interaction (§8)
│   ├── interaction-map.json       # EVERY interactive element/panel/menu/filter exercised (§8)
│   └── recon.json                 # themes:["light","dark"], measured breakpoints, frameworks hint
├── 02-extraction/
│   ├── fragments/                 # one set per route (parallel-safe; never write shared files here)
│   │   ├── {page}.computed.json    # deduped computed-style archetypes (§3-A)
│   │   ├── {page}.pseudo.json      # ::before/::after/::placeholder/::marker/::selection/::backdrop
│   │   ├── {page}.states.json      # forced :hover/:focus/:active deltas (CDP)
│   │   ├── {page}.interactions.json # DOM+styles of interaction-REVEALED UI (toolbar, menu, composer, panel) (§8)
│   │   ├── {page}.layout.json      # flex/grid, z-index/stacking, @media + @container breakpoints, rects
│   │   └── {page}.dom.html         # cleaned outerHTML
│   ├── css-variables.json          # all theme scopes (:root, [data-theme], .dark, prefers-color-scheme)
│   ├── all-styles.json             # full CSSOM rule dump incl. cross-origin REFETCHED sheets
│   ├── fonts.json                  # @font-face + document.fonts loaded set + variable-font fvar axes
│   ├── STATES-MANIFEST.md          # punch-list: every view/state × {screenshot ✓, code extracted ✓} (§8)
│   ├── assets.json                 # manifest of DOWNLOADED bytes (hash, ext, intrinsic dims, srcset)
│   └── assets/                     # the actual downloaded files
│       ├── img/  svg/  fonts/
├── 03-design-spec/
│   ├── DESIGN.md           # the authoritative token system (§3-D). Single author.
│   └── assertions.json     # machine-checkable tokens (selector → expected computed prop) — gate input (§5)
├── 04-architecture/
│   ├── file-tree.md
│   └── component-map.md
├── 05-build/                       # build notes/logs (code is written to OUTPUT_DIR)
├── 06-qa/
│   └── cycle-{N}/
│       ├── screenshots/{page}--{viewport}.png      # clone VISUAL-REFERENCE shots (eyeball, not the gate)
│       ├── clone-styles.json                       # clone's computed styles read via javascript_tool (§5)
│       ├── metrics.json                            # the GATE input: style_assertions result (§5)
│       ├── fragments/{page}--{viewport}.bugs.json  # parallel-safe per-task bug fragments
│       └── bugs.json                               # merged + renumbered (deterministic, by orchestrator)
├── 07-fix/cycle-{N}/
│   └── fix-set-{k}.json            # disjoint file partitions for parallel fix agents
└── 09-polish/
    └── final-screenshots/{page}--{viewport}.png
```

**Page slug rule:** route `/` → `home`; `/pricing` → `pricing`; `/blog/post` → `blog-post` (lowercase, non-alphanumerics → `-`, trim). **Viewport keys:** `desktop` (1920×1080), `tablet` (768×1024), `mobile` (375×667). Every per-page/per-viewport artifact uses `{page}--{viewport}` so the recon reference and the QA clone capture line up 1:1 for the side-by-side eyeball.

---

## 2. Stages and parallelism

**One Chrome — browser stages run sequentially.** Recon, Extraction, and the QA computed-style read all drive the single Claude Chrome extension, so they process one view/tab at a time. **Code stages fan out in parallel** via Task sub-agents (build each page, fix each disjoint file-set concurrently). The "Parallel?" column below means *code* parallelism via Task agents; anything that touches the browser is sequential.

| # | Stage | Parallel? | Fan-out key | Reads | Writes |
|---|-------|-----------|-------------|-------|--------|
| 1 | Recon | sequential (one Chrome) | page × viewport | URL | `01-recon/` reference shots, `sitemap.json`, `recon.json` |
| 2 | Extraction | sequential (one Chrome) | per page | `sitemap.json` | `02-extraction/fragments/*`, then orchestrator merges shared files |
| 3 | Design Spec | no (fan-in) | — | all `02-extraction/*` | `DESIGN.md`, `assertions.json` |
| 4 | Architecture | no | — | `DESIGN.md`, `recon.json` | `file-tree.md`, `component-map.md` |
| 5a | Build-foundation | no | — | spec, architecture | tokens/globals, layout, nav, shared components in OUTPUT_DIR |
| 5b | Build-page | **yes** (‖ Task agents) | per page | foundation, spec | one route's page code |
| 6 | QA | sequential read, ‖ analysis | page × viewport | clone (dev server) + `clone-styles.json` + `DESIGN.md`/`assertions.json` | `06-qa/cycle-N/...` `clone-styles.json`, `metrics.json`, fragments, reference shots |
| 7 | Fix | **yes** (‖ Task agents) | disjoint file-set | merged `bugs.json` + `metrics.json` | edits in OUTPUT_DIR |
| 8 | (loop) | — | — | `metrics.json` | converges QA↔Fix (§5) |
| 9 | Polish | sequential (one Chrome) | per page | final `metrics.json` residual failures | OUTPUT_DIR + `09-polish/*` |

**Sequential spine (never parallelize the writer):** Recon → Extraction → **Design Spec (single author)** → Architecture → **Build-foundation (sole author of tokens/globals)** → Build-pages → [QA → Fix]×converge → Polish. Code work that can fan out fans out via Task sub-agents; every browser-touching step stays sequential under the one Chrome.

**Merge steps are deterministic code (jq/python in the orchestrator), NEVER an agent:** `sitemap.json` (union routes), extraction shared files (concat fragments), `bugs.json` (concat + renumber `BUG-NNN`).

---

## 3. Extraction completeness — leave no stone unturned

Capture from the LIVE page via `mcp__claude-in-chrome__javascript_tool` (run the extraction JS in the page; for large scripts, write the JS to a file and pass its contents to `javascript_tool`). The cap of "50 elements / 17 properties" is **deleted**. Authoritative order when sources conflict: **CSSOM authored rules > forced-state computed > deduped computed archetypes > screenshot estimate.**

**A. Computed styles — ALL meaningful nodes, deduped by signature.** Walk `document.querySelectorAll('*')` minus `script/style/meta/link/head` and zero-area nodes. For each, read the full property set below; build a signature hash; emit ONE representative per unique signature with a `count` + sample selector + `getBoundingClientRect()` (pixel ground truth). Drop any property equal to its CSS initial value (delta-from-default). Property set (minimum):
- **Color/bg:** color, backgroundColor, **backgroundImage** (gradients live here — mandatory), backgroundSize, backgroundPosition, backgroundRepeat, backgroundClip, backgroundBlendMode, opacity, mixBlendMode, accentColor, caretColor, `-webkit-background-clip`/`-webkit-text-fill-color` (gradient text)
- **Typography:** fontFamily, fontSize, fontWeight, fontStyle, fontStretch, lineHeight, letterSpacing, wordSpacing, textTransform, textDecoration{Line,Color,Style,Thickness}, textShadow, textAlign, whiteSpace, textOverflow, **fontVariationSettings**, fontOpticalSizing, fontFeatureSettings, textUnderlineOffset
- **Box model (per-side, not shorthand):** paddingTop/Right/Bottom/Left, marginT/R/B/L, border{T/R/B/L}{Width,Style,Color}, borderT/B-L/R-Radius (asymmetric), boxSizing, width/height, min/max-W/H, aspectRatio, inset/top/right/bottom/left, outline{Width,Style,Color,Offset}
- **Effects:** boxShadow, textShadow, filter, **backdropFilter** (glassmorphism), clipPath, maskImage/`-webkit-mask-image`, isolation
- **Layout:** display, flexDirection, flexWrap, justifyContent, alignItems, alignContent, alignSelf, flexGrow/Shrink/Basis, order, gridTemplateColumns/Rows/Areas, gridAutoFlow/Columns/Rows, justifyItems, placeItems, gridColumn/Row, rowGap, columnGap, overflowX/Y, overscrollBehavior, scrollSnapType, scrollBehavior, containerType, containerName
- **Layering/motion:** zIndex, position, transform, transformOrigin, perspective, willChange, transitionProperty/Duration/TimingFunction/Delay, animationName/Duration/TimingFunction/IterationCount/Direction/FillMode
- **Cursor:** cursor (every interactive element)

**B. Pseudo-elements** → `{page}.pseudo.json`: `getComputedStyle(el,'::before')` and `::after` (emit where `content!=='none'`), plus `::placeholder ::marker ::selection ::first-letter ::first-line ::backdrop`. Capture content, background/backgroundImage, geometry, transform, mask, clipPath, color, font.

**C. Interaction states** → `{page}.states.json`: drive `:hover :focus :focus-visible :active` via the extension's `computer` (hover/focus the element) then re-read computed styles via `javascript_tool`; emit **deltas only**. Primary fallback (most reliable here): parse the authored `:hover/:focus/:active` rules straight from the CSSOM (`javascript_tool` walking `cssRules`).

**D. CSS variables / themes** → `css-variables.json`: every rule whose selector matches `:root, html, [data-theme], .dark, .light`, plus `@media (prefers-color-scheme)` groups; resolve the var union under each theme by toggling and re-reading `getPropertyValue`. Shape: `{ "themes": { "light": {...}, "dark": {...} } }`.

**E. CSSOM full dump** → `all-styles.json`: iterate every sheet's `cssRules` (style + `@media`/`@container`/`@font-face`/`@keyframes`/`@supports`). **When `cssRules` throws (cross-origin), refetch the sheet over HTTP with Bash `curl sheet.href` and parse the text** — do not stub with `/* cross-origin */`.

**F. Fonts** → `fonts.json` + `assets/fonts/`: `@font-face` rules + `Array.from(document.fonts)` filtered to `status==='loaded'`; resolve each `src url()` to absolute and **download the woff2/woff/ttf bytes with Bash `curl`**; record variable-font `fvar` axes (e.g. `wght 100..900`).

**G. Assets** → `assets.json` + `assets/{img,svg}/`: resolve every `img.currentSrc` (+`srcset`/`sizes`), CSS `url()` backgrounds, `<link rel=icon>`, OG images; **download the bytes with Bash `curl -sL`**. Inline SVG: emit FULL `outerHTML` (no 500-char truncation, no 20-element cap); for `<use href="#...">` fetch the sprite. Record intrinsic `naturalWidth/Height`. The build NEVER uses picsum/pravatar placeholders unless a download genuinely failed (log it).

**H. Layout/breakpoints** → `{page}.layout.json`: real `@media`/`@container` `conditionText` (actual breakpoints, not the 768/375 guess), stacking-context map (every positioned/transformed/opacity<1/filtered node + zIndex), and the per-archetype `getBoundingClientRect`.

**I. Framework fingerprint** → in `recon.json`: `__NEXT_DATA__`/`self.__next_f`, `__remixContext`, `__NUXT__`, `data-reactroot`/React hook, `ng-version`, `data-v-*`, `data-astro-*`; Tailwind via `--tw-*` props / utility-class density; asset hosts (`_next/static`, Vite `/assets/index-*`); `<meta name=generator>`.

---

## 4. Design system (Stage 3, single author)

Read all `02-extraction/*`. Produce `DESIGN.md` — a **portable, drop-in design file** in the widely-used `design.md` best-practice structure (à la `github.com/VoltAgent/awesome-design-md`), written so it can be referenced to build new pages, customize the app, or be dropped into a different project, not just consumed internally by this pipeline. Also emit `03-design-spec/assertions.json` — the machine-checkable form of these tokens (selector → expected computed property) that the gate compares against (§5). DESIGN.md is still the **single author** of tokens (Stage 5 wires them) and still the **gate's reference** (§5 asserts against `assertions.json` derived from it). It is a **token system inferred by usage frequency + confidence** (most-used value for a role = the token), not a flat per-element dump.

Structure: it **opens** with a **Visual Theme** paragraph (the overall feel/atmosphere — mood, density, contrast, accent discipline, corner/shadow softness, motion energy), then the rigorous token sections — Colors (incl. a **Gradients** table: type, angle/shape, stops), Typography (incl. variable-font axes), Spacing scale, Border-radius scale, Shadows (layered/inset), **Effects/backdrop-filter**, Motion (durations/easings/keyframes), States (hover/focus/active), Layout/breakpoints (measured), Assets (downloaded paths), Theme tokens (light/dark) — and **closes** with **Design Guardrails** (do's-and-don'ts that reproduce the *feel*) and an **Agent Prompt Guide** (how a coding agent uses this file alone to build in the design language). Boost confidence for values seen on multiple pages. The file must be self-contained: a reader with only DESIGN.md (in another repo or a fresh session) can reproduce the look; artifact citations stay in each row's `Evidence` column to prove values are measured, not invented.

---

## 5. The computed-style-assertion GATE (objective, machine-computed)

Verification is measured, never eyeballed — and the measurement is **computed styles, not a pixel diff.** Each QA cycle:

1. The QA agent opens the running clone in the Claude Chrome extension and, via `mcp__claude-in-chrome__javascript_tool`, reads each asserted selector's computed styles (`getComputedStyle`) → writes `06-qa/cycle-N/clone-styles.json`.
2. The orchestrator runs, via Bash:
   ```
   node scripts/assert-styles.mjs \
     --assertions 03-design-spec/assertions.json \
     --clone-styles 06-qa/cycle-N/clone-styles.json \
     --out 06-qa/cycle-N/metrics.json
   ```
   `assert-styles.mjs` compares the clone's read computed values to the DESIGN.md tokens in `assertions.json` — per selector, the asserted `color/bg/backgroundImage/fontSize/fontWeight/letterSpacing/lineHeight/borderRadius/boxShadow/cursor/transition` (colors normalized to `rgb()`, numerics ±1px / ±0.01em).

`metrics.json`:

```json
{ "cycle": N,
  "style_assertions": {"total":142,"passed":138,"failed":4,
    "failures":[{"selector":".hero-title","prop":"fontWeight","expected":"800","actual":"700"}]},
  "build_ok": true }
```

**PASS gate (ALL must hold):** `style_assertions.failed == 0` AND `npm run build` exits 0. On pass, also do a **visual eyeball** — a Chrome-extension screenshot of the clone next to the real site (§11) — as a human sanity check, NOT a measured gate input.

**No pixel diff in the gate.** There is no `pixelmatch` / `mismatch_pct` / `diff.mjs` / `.diff.png`. A pixel diff is only possible for **PUBLIC sites** where real PNG files of both clone and original can be written to disk; for **authed sites** (the common case here) the Chrome extension can't reliably write screenshot files, so pixel diff does not apply. Computed-style assertions are the gate either way.

---

## 6. Convergence loop + escalation (autonomous)

Replace the fixed 4 cycles with loop-until-converged. The pipeline does NOT return to the human between cycles — only on a terminal state.

```
start_dev_server (poll localhost until ready, else HARD-BLOCKER)
cycle=0; prev_failed=∞; stall=0; MAX_CYCLES=10
while cycle < MAX_CYCLES:
  cycle++
  QA (read clone computed styles → clone-styles.json) → assert-styles.mjs → metrics.json
  if style_assertions.failed == 0 AND npm run build exits 0:  → terminal CONVERGED-PASS; break
  failed = metrics.style_assertions.failed
  if (prev_failed - failed) < 1:     stall++   else stall = 0   # no improvement in failure count
  prev_failed = failed
  if cycle ≥ 2 and stall ≥ 2:        → terminal STUCK; break
  Fix (partition bugs by file, fan out disjoint sets via Task agents; re-read affected selectors after each fix; revert if failures grow)
  npm run build  (regression gate)
→ if cycle == MAX_CYCLES:            → terminal CEILING
```

**Terminal states (the "before it comes back to me" contract):** `CONVERGED-PASS` (gate met) · `STUCK` (no-progress/oscillation in the failure count) · `HARD-BLOCKER` (auth wall / login redirect / build won't compile — emit `<promise>BLOCKED: reason</promise>`) · `CEILING` (MAX_CYCLES). Each writes `final-report.md` (pass) or `escalation.md` (failing assertions + `failed_history` + the offending selectors/props).

**Auth-wall detection:** if recon reaches a blank/login page or a clone route 302s to `/login`, flag HARD-BLOCKER — don't burn cycles on a login screen.

---

## 7. Agent-prompt standard (every stage = strict, separately system-prompted)

Each stage runs as a Task sub-agent with NO memory of other agents. Every stage prompt MUST contain, in this order:
1. **ROLE** — one line: "You are the {stage} agent in a pixel-perfect cloning pipeline."
2. **INPUTS** — exact artifact paths it reads (from §1).
3. **TASK** — numbered steps; any browser work uses the **Claude Chrome extension** (`mcp__claude-in-chrome__*`: `navigate`, `javascript_tool`, `read_page`/`find`, `computer`, `resize_window`).
4. **OUTPUTS** — exact artifact paths it writes (from §1). Nothing else.
5. **EVIDENCE RULES** — every visual claim needs a measured `evidence_method` (a `getComputedStyle` value read via `javascript_tool`). Never assert a match without measurement. Authoritative-source order from §3.
6. **ANTI-HALLUCINATION** — never invent values; if a value can't be read, record `null` + why. Never generate UI from memory; if the page can't be reached, emit `<promise>BLOCKED: reason</promise>`.
7. **COMPLETION** — write outputs, set this task's flag in `status.json`, end with `<promise>CONTINUE</promise>` (or `<promise>BLOCKED: …</promise>`).

**There is one Chrome and no per-task browser sessions.** Browser-touching stages (recon, extraction, QA read) run **sequentially** through the single Claude Chrome extension — there are no `--session` keys and no parallel browser. Parallelism comes from **code stages**: build-pages and fixes fan out via Task sub-agents keyed `{name}-{role}-{page}[-c{cycle}]` (each edits its own disjoint files), while the browser work stays sequential. Browser tooling: the Claude Chrome extension only — never Playwright MCP / SSH.

---

## 8. Exhaustive interaction coverage — click EVERYTHING

A web app is not a stack of static pages. The controls that matter most — a rich-text toolbar that appears when you focus the editor, the comment composer, an opened menu, a side panel, a filter, a Kanban/board view toggle — **only exist after an interaction.** A clone built from first-paint screenshots silently ships skin-deep. So recon does not sample; it **exercises every interactive element on every route.**

**Recon interaction sweep (Stage 1, per route).** Enumerate every interactive element — buttons, links, menu/dropdown triggers, tabs, view switchers, filter controls, every row that opens a panel, every input and `contenteditable` — and exercise each one: **click it, open it, focus it, hover it.** After each action, capture the resulting state as `01-recon/screenshots/interaction-states/{page}--{action-slug}.png` and record it in `interaction-map.json`:

```json
{ "route": "/issue/PER-9",
  "interactions": [
    {"action_slug":"focus-description","trigger":".description","kind":"focus",
     "reveals":["rich-text toolbar (Aa,B,I,link,quote,code)"],"screenshot":"...","captured":true},
    {"action_slug":"open-priority-menu","trigger":"[data-priority]","kind":"click",
     "reveals":["priority dropdown: Urgent/High/Medium/Low/None"],"screenshot":"...","captured":true},
    {"action_slug":"comment-composer","trigger":".comment-box","kind":"focus","reveals":["composer + send"],"captured":true}
  ],
  "unreached": [] }
```

The rule is literal: **click every single button and open every single side panel, menu, filter, and view** — don't stop at the first screen. Close/escape each state before the next so captures stay clean.

**Interaction-state extraction (Stage 2).** For each entry in `interaction-map.json`, trigger the interaction, then snapshot the **revealed DOM + computed styles** (the toolbar, the open menu, the composer, the side panel) into `{page}.interactions.json`. Note: this is a real DOM mutation, not a CSS pseudo-state — forcing `:hover` (§3-C) is not enough; you must perform the interaction and capture what newly appears.

**Build (Stage 5)** reproduces these interaction-revealed components and wires their client-side behavior (focus → show toolbar, click → open menu, composer renders).

**Coverage critic (runs after build, gates with QA).** Assert that **every** interactive element in every route's `interaction-map.json` was (a) captured, (b) rebuilt, and (c) appears + behaves in the clone when the same interaction is performed. Anything in `unreached`, or present in the original but missing in the clone, is logged loudly and **fails the gate** — a clone that's only skin-deep does not pass. The QA interaction check (§5) drives the same interactions on the clone and diffs the revealed states against the originals.

**Scope levels (state explicitly in `00-config.json` → `scope`).** (a) **visual** — looks like it; (b) **interactive** — the interaction-revealed UI appears and behaves client-side (default for this skill); (c) **functional** — it actually works end-to-end (data persists, comments post). Level (c) is real app logic + a backend — that's building the app, not cloning it. The skill must not present a level-(a/b) clone as a working product.

**States Manifest (the punch-list).** Maintain `02-extraction/STATES-MANIFEST.md` — a table with one row per view/state discovered in `01-recon/interaction-map.json` and two checkboxes per row: **screenshot captured** and **code/values extracted**. Recon fills the screenshot column; extraction fills the code column, working the list top to bottom. The coverage critic fails the gate on any unchecked box — a state you screenshotted but never extracted (or vice-versa) shows as an empty box, so a gap is impossible to hide.

## 9. Check-in gate — MANDATORY, after every stage (hard stop)

This skill runs in a live conversation, so the per-stage check-in is **always on and is a hard stop** — not an optional flag. After each stage the agent **stops, reports what it produced (summary + exact artifact paths / captured views), and WAITS** for the user before doing anything else. See SKILL.md "⛔ STOP-AND-CHECK-IN GATE."

At each pause the user can **approve & continue**, **revise** (add instructions and re-run that stage — e.g. tell recon "also click the filters and every side panel," and it runs another round that *augments* its prior pass, then checks in again), or **stop**.

**Running the next stage — or calling any tool — before the user replies is a failure.** The check-in is the whole human-in-the-loop point: review recon before extraction, review the design system before the build, review the build before QA. One stage → stop → wait, every time.

## 10. Post-clone extension (guided) — customize + agent access

Once the clone is done, guided mode keeps going (it needs your input, so it only runs with `--guided`): the agent checks in and asks **"anything else you want to build?"** Each feature you describe is built into the clone, matched to `DESIGN.md` so it looks native, then loops for the next. After features, it offers to build **agent access** — REST **API endpoints** for the app's core entities plus an **MCP server** wrapping them, so any AI agent (Claude/GPT/Gemini) can operate the app (create an issue, query what's on your plate). Both sub-stages are detailed, agnostic, and pre-programmed in `references/08-extend.md` (Part A feature build, Part B API + MCP). This is the genuine payoff of cloning a PM/CRM-style tool: your agent can use it.

## 11. Screenshots are a VISUAL REFERENCE only — the gate does NOT depend on them

The objective ground truth of this pipeline is **computed styles read via `mcp__claude-in-chrome__javascript_tool`** (§5). Screenshots from the Claude Chrome extension are a **visual reference** — something you and the user eyeball (clone vs the real site) — **not** a measured gate input. The extension can't reliably write screenshot files to disk in this environment, so the gate is built on computed styles, never on saved PNGs.

- **Capture** with the extension's `mcp__claude-in-chrome__computer` (`screenshot`) for the side-by-side eyeball. If a PNG happens to land in the workspace (`01-recon/screenshots/{page}--{viewport}.png`, etc.), great — but a missing file is **not** a failure, because nothing in the gate reads it.
- **Pixel diff is out of scope** as a gate (§5). It is only meaningful for **public** sites where both the clone and the original can be written to disk as real PNGs; for authed sites it does not apply. Convergence is driven by `style_assertions.failed`, not by any diff image.

**"Every view" is exhaustive, not a sample (recon, §8).** Reach ALL of: every left-hand sidebar item (navigate into each), every tab / top filter (Active/Backlog/All/etc.), every filter and layout toggle (board↔list↔every view), every menu/dropdown/context-menu (open state), every side panel / detail / modal, every interaction-revealed state (editor toolbar, comment composer, hover), at every viewport. For each, **read its computed styles via `javascript_tool`** (the data that matters) and take a visual-reference screenshot. One view captured = broken recon; keep going until each of these is read into the extraction artifacts and logged as an entry in `interaction-map.json`.
