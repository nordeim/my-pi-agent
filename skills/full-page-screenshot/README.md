# full-page-screenshot — Skill Bundle

This archive packages the **full-page-screenshot** skill (a quality-gated methodology for
capturing pixel-perfect, full-page PNG screenshots of any website) together with the
**system-repertoire skills that were invoked or referenced** while producing and
validating it in a live session. Everything needed for a coding agent to understand,
install, replicate, and further improve the methodology is included.

## Contents

| Path | Role | Provenance |
|------|------|------------|
| `full-page-screenshot/SKILL.md` | **The new skill.** Trigger description, quality gates G1–G6, 9-phase capture methodology, edge cases, pitfalls. | Authored in-session from a validated reference run |
| `full-page-screenshot/scripts/fullpage_capture.sh` | Executable one-shot capture script (URL, OUT, [W], [H]) implementing Phases 0–8 with built-in Pillow verification. | Authored in-session, smoke-tested live |
| `agent-browser/SKILL.md` | System skill **invoked** as the browser-automation tool reference (agent-browser CLI v0.39.0 commands used by every phase). | System repertoire |
| `skill-creator/` | System skill **invoked** for skill-authoring standards (frontmatter anatomy, progressive disclosure, eval/testing loop, packaging). | System repertoire (full bundle incl. `agents/`, `scripts/`, `eval-viewer/`, `references/`) |
| `task-review/SKILL.md` | System skill **invoked** for the post-task distillation protocol (when/how to persist a completed task as a reusable skill). | System repertoire |
| `reference-run/worklog.md` | Shared work-log copy documenting the original capture task and the skill-distillation task — the provenance record of this bundle. | Session artifact |

## How the pieces fit together

1. **`agent-browser`** provides the raw CLI capabilities (`open`, `set viewport`,
   `wait --load networkidle`, `eval`, `scroll`, `screenshot --full`, `errors`, `close`).
2. **`full-page-screenshot`** layers a quality-gated methodology on top of those
   primitives: viewport-before-navigation, load gating, page-metrics probing,
   lazy-content scroll pass, return-to-top settle, capture, and numeric + visual
   post-capture verification (gates G1–G6).
3. **`skill-creator`** and **`task-review`** governed how that methodology was distilled
   into SKILL.md form and how it can be evaluated/iterated going forward.

## Reference run (provenance of the methodology)

- Target: `https://preview-chat-91a7145b-e328-46b1-8fae-58f89dd46a79.space-z.ai/` (NEO CRM landing page)
- Result: PNG 1920×4986 RGB (~498 KB), all gates passed, visually verified end-to-end
- Reproduction: the bundled `fullpage_capture.sh` was smoke-tested against the same URL
  and reproduced the identical result (1920×4986, G5 PASS, G6 visual check passed)

## Quick start

```bash
# Requirements: agent-browser (npm i -g agent-browser && agent-browser install),
#               python3 + Pillow (pip install pillow)

# Standard desktop capture
bash full-page-screenshot/scripts/fullpage_capture.sh "https://example.com/" ./example-fullpage.png

# Custom viewport (e.g. mobile)
bash full-page-screenshot/scripts/fullpage_capture.sh "https://example.com/" ./mobile.png 390 844
```

For capture flows that need interaction first (cookie consent, login, tabs), perform the
interaction with agent-browser commands per `agent-browser/SKILL.md`, then follow the
remaining phases in `full-page-screenshot/SKILL.md` manually.

