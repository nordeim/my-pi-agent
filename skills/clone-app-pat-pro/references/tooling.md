# Tooling & Conventions

This skill runs **in-conversation**: the live Claude session orchestrates the pipeline directly — spawning Task sub-agents, driving the browser, and running the deterministic helper scripts. **`00-contract.md` is the single source of truth.** Where this file and the contract disagree about paths, artifact names, fan-out keys, the gate, or the loop — the contract wins. Read it first.

---

## 1. Browser capture — Claude Chrome extension

All browser work — the real logged-in site, the localhost clone, and the QA diff loop — runs through the **Claude Chrome extension** (`mcp__claude-in-chrome__*`). You're already authed in Chrome, so the real target loads behind its login, and the localhost clone loads with no auth at all. The ground truth for verification is the **computed styles you read via `mcp__claude-in-chrome__javascript_tool`** (a `getComputedStyle` value on the real page vs. the same read on the clone); a screenshot is a visual reference only, not a value source.

**One Chrome, one tab at a time.** Never run two browser actions at once. Browser stages (recon, extraction, QA capture, polish) are **sequential**. Code stages (build-page, fix) fan out in parallel via Task sub-agents.

| What you're capturing | Tool | Why |
|---|---|---|
| The **real, logged-in site** (e.g. linear.app) | **Claude Chrome extension** (`mcp__claude-in-chrome__*`) | You're already authed in Chrome, so the real page loads behind its login. Read its computed styles via `mcp__claude-in-chrome__javascript_tool` for the verification ground truth; a `screenshot` is a visual reference only. |
| The **localhost clone** (no auth) + the **QA diff loop** | **Claude Chrome extension** (`mcp__claude-in-chrome__*`) | The clone has no auth, so it loads directly. Compare the clone's `getComputedStyle` reads (via `mcp__claude-in-chrome__javascript_tool`) against the real page's, route by route. |

### Browser-tool mapping

**Real authed site (Chrome extension):** open route → `mcp__claude-in-chrome__navigate`; screenshot for visual reference → `mcp__claude-in-chrome__computer` (`screenshot`); read computed styles / CSSOM / run JS (the verification ground truth) → `mcp__claude-in-chrome__javascript_tool`; read DOM / find → `read_page` / `find`; click/hover/focus for the interaction sweep → `mcp__claude-in-chrome__computer`; viewport → `resize_window`.

**Localhost clone (Chrome extension):** open route → `mcp__claude-in-chrome__navigate http://localhost:3000{route}`; set viewport → `mcp__claude-in-chrome__resize_window <w> <h>`; capture for visual reference → `mcp__claude-in-chrome__computer` (`screenshot`); read the clone's computed styles → `mcp__claude-in-chrome__javascript_tool`. Diff the clone's `getComputedStyle` reads against the real page's per route.

Page/viewport keys are fixed by the contract: `desktop` (1920×1080), `tablet` (768×1024), `mobile` (375×667). Artifacts use `{page}--{viewport}` so the recon baseline and QA clone reads line up 1:1.

---

## 2. Screenshots are a visual reference; computed styles are the ground truth (contract §11)

A screenshot from the Chrome extension is a **visual reference only** — capture it to eyeball layout and catch obvious breakage, but treat it as an aid, not a workspace artifact (the file cannot be reliably saved to disk in this environment). Do not build verification on a PNG landing under `clone-workspace/{name}/.../screenshots/`.

- **Real authed site + localhost clone** (Chrome extension): take the shot with `mcp__claude-in-chrome__computer` (`screenshot`) for a quick visual check of the route at each viewport.
- **The verdict is the computed style, not the image.** The thing that actually gates a match is `getComputedStyle` read via `mcp__claude-in-chrome__javascript_tool` — read the value on the real page, read the same value on the clone, and compare them. A measured value beats a visual impression every time.

---

## 3. Evidence & anti-hallucination

These rules apply to ALL QA, Fix, and Polish work, and complement the contract's EVIDENCE RULES and ANTI-HALLUCINATION sections (§7).

1. **Every visual claim needs a measured `evidence_method`** — a `getComputedStyle` value or a diff %. The pixel-diff gate (`metrics.json`) and `getComputedStyle` are the only verdicts that count. "Looks good" is not a grade.
2. **Authoritative-source order** when sources conflict (§3): **CSSOM authored rules > CDP forced-state computed > deduped computed archetypes > screenshot estimate.** A measured value always beats a screenshot impression — visual impression cannot distinguish `#f0f0f0` from `#f5f5f5`.
3. **Never invent a value.** If a value can't be read, record `null` + the reason.
4. **Never fabricate a match.** Fix the clone to match the original exactly, or record the bug honestly — the gate is objective, so gaming it is impossible. If the page can't be reached (auth wall / 302 to login), do NOT generate UI from memory — emit `<promise>BLOCKED: reason</promise>` (HARD-BLOCKER, contract §6).
5. **Never skip a page × viewport.** The gate evaluates every `{page}--{viewport}`; an unmeasured cell is a failure, not a pass.

### Bug fragment shape (parallel-safe)

QA agents write per-task fragments to `06-qa/cycle-N/fragments/{page}--{viewport}.bugs.json`; the orchestrator concatenates + renumbers into `bugs.json`. Every entry carries measured evidence:

```json
{
  "id": "BUG-001",
  "severity": "C",
  "category": "color",
  "element": "TopNav background",
  "page": "home",
  "viewport": "desktop",
  "expected": "rgb(255,255,255) (DESIGN.md token --surface)",
  "actual": "rgb(245,245,245) (getComputedStyle)",
  "evidence_method": "getComputedStyle",
  "diff_region": "cycle-1/diff/home--desktop.diff.png",
  "fix_hint": "Change bg-gray-50 → bg-white in TopNav.tsx"
}
```

`evidence_method` is required. Valid values: `getComputedStyle` (computed CSS via JS) · `CSSOM` (authored rule) · `forced-state` (CDP `:hover/:focus/:active` delta) · `pixelmatch diff` (mismatch region from `metrics.json` / a diff PNG) · `assert-styles.mjs` (a recorded style-assertion failure).
