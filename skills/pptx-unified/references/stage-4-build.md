# Stage 4: BUILD

> Fan out 3 `ppt-expert` sub-agents to render all slides in parallel. The main agent NEVER writes slide HTML — that's the sub-agents' job.

---

## The 3-call cap

**HARD CAP: at most 3 `Agent` calls per deck.**

If the deck has more sections than 3 groups, MERGE adjacent sections rather than spawning a 4th group. More groups = more sub-agent spin-up overhead AND weaker visual consistency across the deck.

### Why 3?
- Each sub-agent spin-up costs ~10-15 seconds of latency.
- 3 groups × 4 slides = 12 slides rendered in the time it would take to serially render 4.
- More than 3 groups dilutes the "lock in a consistent layout language across a section" benefit — sub-agents diverge in styling decisions when there are more of them.

---

## Grouping strategy

### For a 12-slide deck (3 groups of 4)

| Group | Slides | Narrative section |
|-------|--------|-------------------|
| Agent 1 | slides[0:4] | Opening (Cover + Hook + Bento + Category Map) |
| Agent 2 | slides[4:8] | Middle (Section Divider + 3 family deep-dives) |
| Agent 3 | slides[8:12] | Closing (Beyond + Timeline + Setup + CTA) |

### For an 8-slide deck (2 groups of 4, or 3 groups of 3-3-2)

| Group | Slides |
|-------|--------|
| Agent 1 | slides[0:4] (Cover + Hook + 2 highlights) |
| Agent 2 | slides[4:8] (2 deep-dives + Setup + CTA) |

Or for tighter visual consistency:
| Agent 1 | slides[0:3] (Cover + Hook + Bento) |
| Agent 2 | slides[3:6] (3 deep-dives) |
| Agent 3 | slides[6:8] (Setup + CTA) |

### For a 16-slide deck (3 groups of 5-6)

| Group | Slides |
|-------|--------|
| Agent 1 | slides[0:6] (Cover + Hook + Map + Section Divider + 2 deep-dives) |
| Agent 2 | slides[6:11] (3 deep-dives + Beyond + Timeline) |
| Agent 3 | slides[11:16] (Setup + Comparison + 2 reference + CTA) |

### Grouping rules
1. Groups must be CONTIGUOUS RANGES (e.g., 0..4, 4..8, 8..12), not interleaved.
2. Groups should follow narrative sections, not arbitrary index ranges.
3. Keep groups small (5-7 slides max). Larger groups = more context per sub-agent = slower rendering.
4. Single-slide groups are fine when a section (or the cover) stands alone.

---

## Dispatch in a SINGLE turn

Emit ALL 3 `Agent` calls in ONE assistant turn. They run concurrently — this is 3-5× faster than sequential iteration.

If you emit them serially across 3 turns, you lose the parallelism benefit entirely.

---

## The dispatch prompt (use this exact shape)

Substitute the bracketed values per group:

```
You are a slide-rendering sub-agent. Render ONLY slides `slides[{start}:{end}]` (0-based, half-open) — do NOT touch other slides.

First Read these absolute paths:
  • Brief manifest:    {absolute path to slides/slides_brief.json}
  • Global stylesheet: {absolute path to slides/global.css}
Both live in the SAME directory ({absolute path to slides/}); write each slide HTML there as a sibling.

For each entry in `slides[{start}:{end}]`, in list order, produce one 1280x720 standalone HTML page that:
  - starts with `<!DOCTYPE html>`, ends with `</html>`, and links `global.css` via `<link rel="stylesheet" href="global.css">` in `<head>`
  - loads Tailwind via `<script src="https://cdn.tailwindcss.com"></script>` and Material Icons via `<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">`
  - uses ONLY the palette/typography in `design`, and renders EVERY fact/headline/bullet/stat/quote in `task_brief` verbatim
  - obeys every constraint in the SLIDE QUALITY BAR (exact 1280×720 canvas, overflow-hidden, WCAG AA contrast, diversified layouts, no fabricated image URLs, no graphical timelines/SVG flowcharts/code-drawn maps/base64 images/Reveal.js)
  - speaker notes: since `speaker_notes` is `{none|short|full}`, generate notes as the LAST `<body>` child `<aside data-notes class="hidden">…</aside>` (visually hidden via Tailwind's `hidden` class). Match the deck language. {If short: "3-5 bullet hints"} {If full: "~80-150 word script"} {If none: "omit entirely"}

Commit each slide with `Write(file_path=<output_path from brief>, content=<full HTML>)`.

The {N} slides you are responsible for:
  - slides[{i}]: "{title}" → {output_path}
  - slides[{i+1}]: "{title}" → {output_path}
  ...

Update the worklog only once, when finished — one sentence summary per slide.
```

### Critical fields in the dispatch prompt

1. **Index range** (`slides[{start}:{end}]`, 0-based, half-open) — explicitly state which slides the sub-agent owns.
2. **Absolute path to `slides_brief.json`** — the sub-agent reads the brief from here.
3. **Absolute path to `global.css`** — the sub-agent reads the stylesheet from here.
4. **The slide list** — restate the indices, titles, and output_paths so the sub-agent can verify it's rendering the right slides.
5. **Speaker notes instruction** — explicitly state `none` / `short` / `full` and the expected format.

If any of these is missing or relative, the sub-agent will fail to render.

---

## Sub-agent type

Pass `subagent_type: ppt-expert`. This is the specialized PPT rendering agent.

If the harness reports `ppt-expert` as unavailable, fall back to `subagent_type: general-purpose` and PREPEND the rendering rules from this skill's SKILL.md into the dispatch prompt. The general-purpose agent needs the rules inlined because it doesn't have the pptx-unified skill loaded.

---

## Handling sub-agent fidelity compromises

Sub-agents will sometimes make small fidelity compromises to fit content into the 1280×720 canvas. Examples from the reference build:

- Cover title set at 110px instead of 120px (fits 55% left column without clipping)
- Closing URL at 60px instead of 64px (30-char JetBrains Mono string fits 1136px inner canvas)

**These are acceptable.** The sub-agent is making a reasonable engineering trade-off. Document it in the worklog but do NOT force a re-render unless the compromise breaks the design intent.

### When to force a re-render
- The sub-agent omitted required content (missing bullets, missing stats)
- The sub-agent used a different palette than committed
- The sub-agent fabricated an image URL
- The sub-agent used a forbidden pattern (SVG flowchart, base64 image, Reveal.js)

### When to accept the compromise
- Font size ±10% from brief target
- Spacing slightly different from brief
- Layout structure preserved but element sizing adjusted

---

## Post-build verification

After all sub-agents return, verify:

```bash
ls -la <work_dir>/slides/slide_*.html | wc -l    # Should match slides_brief.json length
```

If any slides are missing, re-dispatch a sub-agent for just those slides (single-slide group is fine).

---

## Anti-patterns

### Anti-pattern: the main agent writes slide HTML
The main agent NEVER calls `Write` to commit slide HTML. This serializes work and removes the parallelism benefit. Every slide — cover, body, closing — is committed by a sub-agent.

### Anti-pattern: 4+ sub-agent calls
The 3-call cap is real. If you have 4 narrative sections, merge 2 adjacent sections into one group of 6-7 slides rather than spawning a 4th agent.

### Anti-pattern: serial dispatch (1 Agent call per turn)
Emitting 3 Agent calls across 3 turns loses the parallelism benefit. Emit all 3 in ONE turn.

### Anti-pattern: vague dispatch prompts
"Render the cover slide" without the absolute paths, index range, and slide list will fail. The sub-agent has no context beyond what you put in the prompt.

### Anti-pattern: re-rendering for minor fidelity compromises
If the sub-agent set the title at 110px instead of 120px to fit the canvas, accept it. Re-rendering wastes 30+ seconds and the new sub-agent may make a different compromise.

---

## Output of Stage 4

N HTML files on disk at `<work_dir>/slides/slide_NN.html`, one per entry in `slides_brief.json.slides[]`.

Proceed to Stage 5: EXPORT.
