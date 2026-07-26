# Anti-Patterns — 20+ Lessons from Real Builds

> Every lesson here came from a real build failure or near-miss. Read the titles; read any that match your current build context.

---

## Stage 1: CLARIFY

### 1. Skipping clarify "because the request is clear"
**Symptom:** User says "make a deck about X". You skip questions and start building. Result: a 20-slide comprehensive reference deck when the user wanted an 8-slide lightning talk.
**Fix:** Always confirm audience + length + palette, even when the request seems clear. Use the "no-approvals" shortcut (apply recommended defaults) only if the user has explicitly delegated.

### 2. Asking 1 question per turn
**Symptom:** 6 turns spent asking 6 questions. Total wall time: 6+ minutes.
**Fix:** Batch all 6 questions in ONE `AskUserQuestion` call. Max 6 questions per call.

### 3. Vague option descriptions
**Symptom:** Options are "Light / Dark / Other". User can't react to abstractions.
**Fix:** Each option's `description` MUST be concrete — a palette hint (`#0D1117`), a font name (Inter), a sample headline, a named visual reference (Linear changelog).

### 4. Marking multiple options as `recommended`
**Symptom:** Two options both marked `recommended: true`. User doesn't know which is the default.
**Fix:** Exactly ONE option per question gets `recommended: true`.

---

## Stage 2: RESEARCH

### 5. Serial research calls
**Symptom:** 3 `web_search` calls emitted across 3 turns. Wall time: 30+ seconds wasted.
**Fix:** Batch 2-3 queries in ONE turn. They run concurrently.

### 6. Fabricating stats
**Symptom:** "This repo has 10,000 stars" — invented because you didn't verify.
**Fix:** If you can't verify a number, say so explicitly ("estimated", "not verified") or omit it. Fabricated stats destroy credibility.

### 7. Forcing photos on every slide
**Symptom:** Linear-style dark deck with stock photos behind every headline. Looks like AI slop.
**Fix:** Photo-free decks are valid. Linear-style relies on typography + whitespace + accent color, not imagery.

### 8. Ignoring the 6-call image-search limit
**Symptom:** You hit the limit on slide 4 and have 8 more slides that need images.
**Fix:** Plan image needs up front. Cover hero (1) + section dividers (2-3) + key content (2-3) = 6 max. Reuse URLs across slides. Switch to photo-free for remaining slides.

### 9. Keyword-style image queries
**Symptom:** `z-ai image-search --query "office minimalist"` returns poor results.
**Fix:** Use natural-language sentences: `z-ai image-search --query "A photograph of a modern minimalist home office with natural light"`. The ranking model is semantic.

---

## Stage 3: PLAN

### 10. Relative paths in slides_brief.json
**Symptom:** `global_css_path: "global.css"`. Sub-agent resolves it against its own cwd, not the slides/ directory. Slide HTML can't find the stylesheet.
**Fix:** Always use absolute paths: `global_css_path: "/home/z/my-project/download/slides/global.css"`.

### 11. Paraphrasing slide content in the brief
**Symptom:** Brief says "make a slide about the 10 categories". Sub-agent invents the category names. Result: wrong content.
**Fix:** Restate every text element verbatim. "5×2 grid. Row 1: 1. mono '30' / 'Frontend & UI' / 'React 19, Next.js 16...'; 2. mono '11' / ..."

### 12. Meta-reminders per slide
**Symptom:** Every brief ends with "Remember to diversify layouts and verify WCAG AA contrast". 12 slides × 2 reminders = 24 lines of noise.
**Fix:** Put meta-reminders ONCE in the sub-agent dispatch prompt. Keep briefs focused on content.

### 13. Shipping pre-baked typography classes in global.css
**Symptom:** `.h-1`, `.h-display`, `.cn-sub` defined in global.css. Sub-agents fight the cascade — some use the classes, some redefine inline, results are inconsistent.
**Fix:** Define typography TOKENS on `:root` (`--font-heading`, `--fs-h1`, etc.). Let sub-agents apply per-slide inline styles using the tokens.

### 14. Tailwind class collisions
**Symptom:** Custom `.h-1` class in global.css. Tailwind's `.h-1` (height: 4px) overrides it. Heading box collapses to 4px while text renders at full size — heading visibly overlaps the element below.
**Fix:** Never name custom classes `.h-1`, `.h-2`, `.h-3`, `.hidden`, `.block`, `.flex`, `.container`. Use distinctive names (`.eyebrow`, `.tag`, `.card`) or rely on inline styles.

### 15. Writing slides_brief.json without absolute output_paths
**Symptom:** `output_path: "slide_01.html"`. Sub-agent writes to its cwd, not the slides/ directory. Stage 5 export can't find the slides.
**Fix:** Always `output_path: "/home/z/my-project/download/slides/slide_01.html"`.

---

## Stage 4: BUILD

### 16. The main agent writes slide HTML
**Symptom:** Main agent calls `Write` to commit slide HTML. 12 slides take 12 turns. Total wall time: 5+ minutes.
**Fix:** Main agent NEVER writes slide HTML. Every slide is committed by a sub-agent. Fan out 3 sub-agents in ONE turn — 12 slides render in ~1 minute.

### 17. 4+ sub-agent calls
**Symptom:** 16-slide deck → 4 groups of 4 slides → 4 Agent calls. Wall time: longer than 3 groups of 5-6.
**Fix:** HARD CAP: 3 Agent calls per deck. If you have 4 sections, merge 2 adjacent sections into one group of 6-7 slides.

### 18. Serial dispatch (1 Agent call per turn)
**Symptom:** 3 Agent calls emitted across 3 turns. Loses parallelism — 3× slower than parallel.
**Fix:** Emit ALL 3 Agent calls in ONE assistant turn. They run concurrently.

### 19. Vague dispatch prompts
**Symptom:** "Render the cover slide" without absolute paths or index range. Sub-agent fails.
**Fix:** Every dispatch prompt MUST explicitly carry: (a) index range, (b) absolute path to slides_brief.json, (c) absolute path to global.css, (d) the slide list with titles and output_paths.

### 20. Re-rendering for minor fidelity compromises
**Symptom:** Sub-agent set the title at 110px instead of 120px to fit the canvas. You force a re-render. New sub-agent makes a different compromise. Infinite loop.
**Fix:** Accept minor fidelity compromises (±10% font size, slight spacing differences). Document in worklog. Only re-render for: missing content, wrong palette, fabricated image URLs, or forbidden patterns (SVG flowchart, base64 image, Reveal.js).

---

## Stage 5: EXPORT

### 21. Hard-coding the script path
**Symptom:** `node /home/z/my-project/skills/ppt/batch_html2pptx.js` fails with `Cannot find module`. The skill doc has a typo (`ppt` not `pptx`).
**Fix:** Always `find` the script dynamically: `SCRIPT=$(find /home/z/my-project/skills -name "batch_html2pptx.js" -type f | head -1)`. Or use the bundled `export_pptx.sh` wrapper.

### 22. Trusting "Done." without checking for `🚨`
**Symptom:** Converter prints `Done.` You deliver the .pptx. User opens it — slide 7 is missing content because of a `🚨 CRITICAL OVERFLOW` you didn't see.
**Fix:** Always scan the full converter output for `🚨 CRITICAL`. Fix any critical issues before delivering.

### 23. Forgetting `NODE_PATH`
**Symptom:** `node batch_html2pptx.js` fails with `Cannot find module 'pptxgenjs'`.
**Fix:** Always set `NODE_PATH=/usr/local/lib/node_modules` so `pptxgenjs` / `playwright` / `sharp` resolve.

### 24. Renaming files without updating slides_brief.json
**Symptom:** You rename `slide_1.html` to `slide_01.html` for proper sort order. `slides_brief.json` still says `slide_1.html`. Brief and on-disk files diverge.
**Fix:** If you rename files, update `output_path` in `slides_brief.json` to match. The brief is the single source of truth.

### 25. Deleting source HTML after export
**Symptom:** User asks for a typo fix. You have to re-render the entire deck from scratch because the source HTML is gone.
**Fix:** ALWAYS preserve source HTML + global.css + slides_brief.json at `<work_dir>/slides/`. The .pptx is a build artifact; the source is the contract.

### 26. Screenshot-to-PDF as a substitute
**Symptom:** You screenshot each slide to PNG and assemble into a PDF. Text is blurry, file is 3-5× larger, not selectable.
**Fix:** Always use `batch_html2pptx.js` — it produces vector text (selectable, sharp at any zoom, small file).

---

## Cross-stage anti-patterns

### 27. Skipping stages
**Symptom:** "I'll just write the slides directly, skip the clarify and plan stages." Result: inconsistent design, wrong audience tone, missing content.
**Fix:** Never skip stages. Each stage produces an artifact the next stage depends on.

### 28. Diverging brief and on-disk slides
**Symptom:** You edit a slide HTML directly without updating the brief. Next time someone reads the brief, it doesn't match reality.
**Fix:** `slides_brief.json` is the single source of truth. For layout-level changes, update the brief FIRST, then edit the HTML. For typo fixes, the brief doesn't need updating.

### 29. No worklog updates
**Symptom:** Sub-agents finish but don't update the worklog. Next agent has no idea what happened.
**Fix:** Every sub-agent MUST update the worklog once, when finished — one sentence summary per slide.

### 30. Not testing the .pptx after export
**Symptom:** You deliver the .pptx without opening it. User opens it — slide 4 is blank because of a rendering issue.
**Fix:** After export, run `ls -lh <output.pptx>` (file exists, size > 0) and `file <output.pptx>` (reports "Zip archive data"). For extra confidence, run `python3 -c "from pptx import Presentation; print(len(Presentation('<output.pptx>').slides))"` to verify slide count.
