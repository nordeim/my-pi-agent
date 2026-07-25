# clone-app-pat-pro

A Claude Code skill that clones any web app **pixel for pixel** from a URL.

Most "clone this site with AI" attempts look at a screenshot and guess. They come out as slop — generic, obviously AI, and they fall apart the second you put them next to the real thing. This does the opposite: it reads the **real, live code** of the site, measures every value, rebuilds it, and then **proves the match with measured computed-style assertions** — fixing itself in a loop until the copy matches the original's design, value for value.

It runs in a Claude session: the live Claude orchestrates Task sub-agents and drives the Claude Chrome extension. Code stages run in parallel; browser work goes one view at a time.

---

## How it works — step by step

You give it one thing: a URL (e.g. `linear.app`). Then:

**1. Recon — look at the real thing, and click everything.**
It opens the live site (the Chrome extension, so it's logged in) and walks every view — and **exhaustively clicks through it**: every left sidebar item, tab, filter, layout, menu, side panel, and editor, at desktop/tablet/mobile. For each view it takes a screenshot as a visual reference and reads the real computed styles. This matters because the UI that's easiest to miss (a toolbar that only appears when you focus the editor, a comment box, an opened menu) doesn't exist until you interact. Sampling = a skin-deep clone, so it clicks everything.

**2. Extraction — measure everything (leave no stone unturned).**
This is the part that separates a real clone from slop. Instead of eyeballing a screenshot, agents read the site's actual rendered code and pull out *every exact value*:
- every color, and every **gradient** (the thing almost every AI clone misses)
- fonts — including the real font files, downloaded, and exact weights
- spacing, down to the pixel, on every side
- shadows, blurs, rounded corners, borders
- hover, focus, and click states
- the real images and icons — **downloaded**, not faked with placeholders

**3. Design system — turn raw values into a rulebook.**
One agent reads all those measurements and writes a single `DESIGN.md` — the source-of-truth tokens (the brand's real colors, type scale, spacing scale, gradients, shadows). The most-used value for each role becomes the official token.

**4. Architecture — plan the build.**
An agent maps the real page structure into a clean component tree and a build order.

**5. Build — recreate it in code.**
First a "foundation" agent builds the shared pieces (the design tokens, layout, nav, shared components) using the real downloaded fonts and assets. Then page agents build each page in parallel, using only those tokens.

**6. QA — grade the copy by the numbers.**
It reads the clone's actual computed styles (via the Chrome extension) and a script compares them, value by value, against the design-system tokens — colors, spacing, type, radii, shadows. Every mismatch is a measured failure with the exact expected-vs-actual value. No "looks good" — it's measured.

**7. Fix — close the gap, then re-check.**
The failures get handed to fix agents (split up so they never touch the same file). After each fix it re-reads the computed styles; if a change didn't actually clear the failure, it reverts.

**8. Loop until it matches.**
Steps 6–7 repeat automatically. It keeps going until the clone passes the gate — **zero style-assertion failures and the build compiles** — or until it's genuinely stuck or hits a wall (like a login page it can't get past). It only comes back to you when it's actually done.

**9. Polish — sub-pixel cleanup.**
A final pass tightens the last tiny differences: exact gradient stops, shadow blur, cursor on every button, focus rings.

The result is a working, running app that matches the original pixel for pixel — built without touching a screenshot-and-guess shortcut.

---

## What makes it pixel-perfect (the two ideas)

1. **It reads the real code, not a screenshot.** Screenshots throw away the exact values; the live DOM/CSS has them. This skill harvests them directly.
2. **It grades itself with measured computed-style assertions and loops.** "Pixel-perfect" isn't an opinion here — every token (color, spacing, type, radius, shadow) is checked against the clone's real computed values, and it has to clear every failure before it's allowed to finish.

---

## What's in this repo

| Path | What it is |
|------|------------|
| `SKILL.md` | The in-conversation playbook — the live Claude reads this and orchestrates Task sub-agents + the Chrome extension. |
| `scripts/assert-styles.mjs` | The gate — compares the clone's computed styles (read via the Chrome extension) to the design tokens. |
| `scripts/partition_bugs.py` | Splits fixes across agents so they don't collide. |
| `references/01-recon.md` … `07-polish.md` | The detailed instructions each stage agent follows. |
| `references/00-contract.md` | The **internal spec** every agent obeys — exact file locations, the pass/fail gate numbers, and the rules each agent must follow. You don't need to read it to *use* the skill; read it if you want to understand or change the internals. |

---

## Install
Copy this repo's contents into your project's skill directory:
```bash
mkdir -p .claude/skills/clone-app-pat-pro
cp -r clone-app-pat-pro/{SKILL.md,references,scripts} .claude/skills/clone-app-pat-pro/
```

## Dependencies
- **Claude Chrome extension** (`mcp__claude-in-chrome__*`) — the browser tool for everything (you're authed in Chrome, so it reaches logged-in sites). Computed styles read via `javascript_tool` are the verification ground truth; screenshots are a visual reference only.
- Node (for `scripts/assert-styles.mjs`) and `python3` (for `scripts/partition_bugs.py`)

## Run
**In a Claude session**, just ask:
```
clone linear.app — pixel for pixel
```
Claude runs the in-conversation workflow: orchestrates Task sub-agents, drives the Chrome extension (recon every view, extract computed styles, build, then gate the clone with computed-style assertions), and checks in with you after each stage. See SKILL.md.

Artifacts land in `clone-workspace/<name>/` (screenshots, extracted values, the design system, diff overlays, metrics) and the built clone in your `--output` dir.
