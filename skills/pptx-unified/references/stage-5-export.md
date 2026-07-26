# Stage 5: EXPORT

> Convert `slides/` → single `.pptx` via `batch_html2pptx.js`. The final step — but full of traps if you skip path resolution or warning triage.

---

## The path-resolution trap (LESSON #1 from real build)

The canonical `pptx` skill's SKILL.md says the export script is at:
```
/home/z/my-project/skills/ppt/batch_html2pptx.js    ← WRONG (skill doc typo, "ppt" not "pptx")
```

The actual location is:
```
/home/z/my-project/skills/pptx/batch_html2pptx.js   ← CORRECT
```

**Always resolve the script path dynamically** rather than hard-coding:

```bash
SCRIPT=$(find /home/z/my-project/skills -name "batch_html2pptx.js" -type f 2>/dev/null | head -1)
echo "Resolved: $SCRIPT"
```

Or use the bundled wrapper (preferred — it handles path resolution + NODE_PATH + warnings):

```bash
bash /home/z/my-project/my-pi-agent/skills/pptx-unified/scripts/export_pptx.sh \
  /home/z/my-project/download/slides \
  /home/z/my-project/download/<deck-name>.pptx
```

---

## The export command

```bash
cd /home/z/my-project && \
NODE_PATH=/usr/local/lib/node_modules node \
  /home/z/my-project/skills/pptx/batch_html2pptx.js \
  /home/z/my-project/download/slides \
  /home/z/my-project/download/<deck-name>.pptx
```

### Arguments

| Arg | Purpose | Required |
|-----|---------|----------|
| Arg 1 | Slides directory (containing `slide_NN.html` files) | Yes |
| Arg 2 | Output `.pptx` path; defaults to `<work_dir>/<basename(work_dir)>.pptx` | No |

### Environment

- `NODE_PATH=/usr/local/lib/node_modules` is REQUIRED so `pptxgenjs` / `playwright` / `sharp` resolve. Without it, you get `Cannot find module 'pptxgenjs'` errors.
- The script uses Playwright to render each HTML slide to an image, then assembles them into a .pptx via pptxgenjs.
- Concurrency is 8 by default (8 slides rendered in parallel).

---

## Pre-export checklist

Before running the export, verify:

1. **Filenames sort alphabetically into list order.**
   - `slide_01.html`, `slide_02.html`, ..., `slide_12.html` ✅
   - `slide_1.html`, `slide_10.html`, `slide_2.html` ❌ (zero-pad required)
   - If filenames are out of order, rename to `slide_{NN:02d}.html` matching list index AND update each entry's `output_path` in `slides_brief.json`.

2. **All slides exist on disk.**
   ```bash
   ls <work_dir>/slides/slide_*.html | wc -l    # Should match slides_brief.json length
   ```

3. **`global.css` is in the same directory as the slides.**
   Sub-agents link it via `<link rel="stylesheet" href="global.css">` (relative path).

4. **No `🚨 CRITICAL` issues in any slide HTML.**
   Quick scan: open each slide in a browser mentally. If a slide has obvious overflow (content extending past 1280×720), fix it before export.

---

## Warning triage

The converter prints per-slide warnings. Triage by severity:

### `🚨 CRITICAL OVERFLOW` — HARD BLOCKER

**Meaning:** A slide's content extends significantly past the 1280×720 canvas.

**Action:** Fix the source HTML and re-run the export (the .pptx is overwritten in place).

**Common causes:**
- Text container too small for the content
- Image at native resolution exceeding canvas
- Flexbox/grid layout miscalculated

**Fix:** Open the slide HTML, identify the overflowing element, either (a) shrink font size (last resort), (b) trim content (preferred), or (c) widen the container.

### `⚠ BOUNDS` — SOFT WARNING

**Meaning:** A shape is slightly outside the 1280×720 canvas (usually within 20px).

**Action:** Review — likely a decorative element (accent line, dot) slightly clipped. Usually acceptable.

### `⚠ FONT` — SOFT WARNING

**Meaning:** A font may not have loaded before screenshot.

**Action:** Check that `global.css` has the `@import` line for Google Fonts. If the font is custom, ensure it's available in the environment.

### `⚠ OVERLAP` — SOFT WARNING

**Meaning:** Two elements may be touching or overlapping.

**Action:** Review the slide. If the overlap is intentional (e.g., an accent dot overlapping a card border), ignore. If unintentional, adjust spacing.

### `⚠ LAYOUT` — SOFT WARNING

**Meaning:** The layout heuristic flagged something unusual (e.g., a single-column layout where multi-column was expected).

**Action:** Review — may be a false positive or may indicate a structural issue.

### `Browser console: cdn.tailwindcss.com should not be used in production` — IGNORE

**Meaning:** Tailwind CDN prints this warning to the browser console.

**Action:** Ignore. Tailwind CDN is fine for slide rendering (it's not production web — it's a one-time screenshot).

---

## Post-export verification

```bash
# 1. File exists and is non-empty
ls -lh <output.pptx>

# 2. File is a valid OOXML (Zip archive)
file <output.pptx>
# Should report: "Zip archive data, made by v2.0..."

# 3. Slide count in .pptx matches brief
python3 -c "
from pptx import Presentation
prs = Presentation('<output.pptx>')
print(f'{len(prs.slides)} slides in .pptx')
"

# 4. Source HTML + global.css + slides_brief.json preserved
ls <work_dir>/slides/
```

---

## Anti-patterns

### Anti-pattern: hard-coding the script path
`/home/z/my-project/skills/ppt/batch_html2pptx.js` is WRONG (skill doc typo). Always `find` the script dynamically or use the bundled `export_pptx.sh` wrapper.

### Anti-pattern: trusting "Done." without checking for `🚨`
The converter prints `Done.` even when slides had `🚨 CRITICAL` warnings. Always scan the full output for `🚨` and fix any critical issues before delivering.

### Anti-pattern: forgetting `NODE_PATH`
Without `NODE_PATH=/usr/local/lib/node_modules`, the script fails with `Cannot find module 'pptxgenjs'`. Always set it.

### Anti-pattern: renaming files without updating slides_brief.json
If you rename `slide_1.html` to `slide_01.html`, you MUST update the `output_path` in `slides_brief.json` to match. Otherwise the brief and on-disk files diverge.

### Anti-pattern: deleting source HTML after export
ALWAYS preserve the source HTML + `global.css` + `slides_brief.json` at `<work_dir>/slides/`. Future edits (typo fixes, layout changes, slide additions) require these source files. The .pptx is a build artifact; the source is the contract.

### Anti-pattern: screenshot-to-PDF as a substitute
The .pptx MUST be generated via `batch_html2pptx.js` (vector text, selectable, small file). Never screenshot slides to PNG and assemble into a PDF — that produces a raster deck with blurry text and 3-5× larger file size.

---

## Output of Stage 5

A single `.pptx` file at the specified output path, plus the preserved source files at `<work_dir>/slides/`.

Deliver to the user:
- The `.pptx` file path
- The source slides/ directory path (for future edits)
- A brief summary (slide count, file size, design name)
