---
name: full-page-screenshot
description: Capture pixel-perfect, full-page PNG screenshots of any website, landing page, or web app using the agent-browser CLI, with load verification, lazy-content scroll triggering, and post-capture integrity checks. Use this skill whenever the user asks to screenshot, screen-capture, or snapshot a webpage, save a page/site/landing page as a PNG or image file, document how a rendered page looks, or visually verify a built page — even if they only say "grab the page", "capture the landing page", or "save this site as an image" and never literally say "full page" or "screenshot".
read_when:
  - User asks for a screenshot / screen capture of any URL
  - User wants a webpage or landing page saved as a PNG/image
  - User needs visual documentation or a visual record of a rendered page
  - User wants to verify how a just-built page renders in a real browser
allowed-tools: Bash(agent-browser:*)
---

# Full-Page Website Screenshot — Quality-Gated Capture Methodology

## Purpose and definition of done

The deliverable is **one PNG file containing the entire scrollable page**, rendered at a
real desktop viewport, with every section fully painted (no blank areas, no missing
lazy-loaded content, no mid-animation states, no truncated bottom edge).

A capture is DONE only when **all** of the following gates pass:

| Gate | Check | Why it matters |
|------|-------|----------------|
| G1 | Network reached idle after initial load | Avoids capturing a half-loaded page |
| G2 | Page title confirmed, no page errors | Confirms the right page rendered |
| G3 | Full scroll pass executed before capture | Triggers lazy images and scroll-reveal animations |
| G4 | Returned to top (scrollY = 0) before capture | Resets sticky headers / parallax to their natural state |
| G5 | PNG verified: format, width == viewport width, height == `scrollHeight` | Proves nothing is truncated and no blank padding was added |
| G6 | Visual sanity check of the PNG | Catches blank sections that numeric checks cannot |

Do not report success to the user until G1–G6 all pass. If a gate fails, fix and re-run —
the whole flow is cheap (typically < 60 seconds).

## Tooling

- **agent-browser** CLI (headless Chromium automation). Install: `npm install -g agent-browser && agent-browser install`
- **Python + Pillow** for post-capture integrity verification (`pip install pillow`)
- Everything runs headless; never use `--headed` in server environments

## The methodology, phase by phase

### Phase 0 — Pre-flight

```bash
which agent-browser && agent-browser --version   # confirm tooling exists
mkdir -p /home/z/my-project/download             # output directory (adapt to env convention)
```

If the CLI is missing, install it before anything else. Decide the output filename now:
descriptive and stable, e.g. `<site-or-project>-landing-fullpage.png`.

### Phase 1 — Set the viewport BEFORE navigation

```bash
agent-browser set viewport 1920 1080
```

Order matters. The viewport must be set **before** `open` so the page renders its
desktop responsive layout from first paint. Setting it after navigation can reflow the
page mid-load and produce a layout the site never intended at that size.
1920×1080 is the default desktop choice; use 390×844 for a mobile capture
(then pair with `set device "iPhone 14"` if device-level emulation is wanted).

### Phase 2 — Navigate and gate on load (G1, G2)

```bash
agent-browser open "https://example.com/" --timeout 60000
agent-browser wait --load networkidle --timeout 30000
agent-browser get title
agent-browser get url
agent-browser errors
```

- `networkidle` waits until network requests stop — a far better "loaded" signal than a
  fixed sleep.
- Confirm the returned title/url match expectations; this catches redirects and wrong URLs.
- `agent-browser errors` prints JavaScript page errors. Empty output is expected; visible
  errors are a warning to investigate, not necessarily a capture blocker.

### Phase 3 — Probe page metrics (feeds gate G5 and the scroll loop)

```bash
agent-browser eval "JSON.stringify({pageHeight: document.documentElement.scrollHeight, viewportH: window.innerHeight, images: document.images.length, lazyImages: Array.from(document.images).filter(i => i.loading === 'lazy').length})"
```

Record `pageHeight` — it is the expected height of the final PNG and the input for the
scroll pass. Note that `images` can legitimately be **0**: modern landing pages often
draw everything with CSS shapes, inline SVG, or canvas. Zero `<img>` tags does NOT mean
a visual-free page, and it does not remove the need for the scroll pass.

### Phase 4 — Scroll pass to trigger lazy content (G3)

Scroll through the whole page in viewport-sized chunks, pausing briefly at each step:

```bash
agent-browser scroll down 1200; sleep 0.5   # repeat ceil(pageHeight / 1200) times
agent-browser wait --load networkidle --timeout 15000   # scrolling may fire new requests
```

Why this is mandatory: many sites lazy-load below-the-fold content or run
scroll-triggered reveal animations. A capture taken from a cold page can show empty
cards or missing sections even though `--full` resizes the viewport — some reveal
effects only fire when a scroll event actually visits the region.

### Phase 5 — Return to top and settle (G4)

```bash
agent-browser eval "window.scrollTo(0,0); 'top'"
sleep 1.5
```

Full-page capture expands the viewport from the top of the document. Sticky headers,
floating chat widgets, and scroll-linked styles should be photographed in their natural
top-of-page state, and entrance animations need a moment to finish.

### Phase 6 — Capture

```bash
agent-browser screenshot --full /path/to/output.png
```

`--full` is the whole point: without it you only get the 1080px-tall viewport, not the
page. Do not add `--json`; you want the file artifact.

### Phase 7 — Post-capture verification (G5, G6)

Numeric verification with Pillow:

```python
from PIL import Image
img = Image.open(path); fmt = img.format
w, h = Image.open(path).size
# expect: fmt == "PNG", w == viewport width (1920), h == pageHeight from Phase 3
```

- `width == viewport width` and `height == scrollHeight` together prove the capture is
  complete and un-truncated. A mismatch means the page changed under you (rerun the
  probe) or the capture silently failed (retry).
- Then do the visual check: **Read the PNG as an image** (or open it) and scan top to
  bottom for blank bands, missing images, overlapping text, or a cut-off footer.
  Numeric checks cannot catch these; the visual pass can.

### Phase 8 — Cleanup and handoff

```bash
agent-browser close
```

Close the browser session to free resources. In multi-agent environments, append a
section to the shared worklog (`/home/z/my-project/worklog.md`) recording the target
URL, output path, and verified dimensions.

## One-shot bundled script

`scripts/fullpage_capture.sh` in this skill folder implements Phases 0–8 with all gates,
a scroll loop computed from the probed page height, and built-in Pillow verification.
Use it when no deviation is needed:

```bash
bash fullpage_capture.sh "https://example.com/" /home/z/my-project/download/example-fullpage.png
# optional args: [width] [height]  →  fullpage_capture.sh URL OUT 1920 1080
```

When the task needs custom interaction first (accept cookies, log in, click a tab), do
those steps interactively with agent-browser commands (snapshot / click / fill), then
run the remaining phases manually — or simply run the script afterward for the
standardized capture and verification half of the flow.

## Edge cases and adaptations

- **Cookie banners / modals overlaying content**: after Phase 2, take
  `agent-browser snapshot -i`, find the accept/close button ref, `agent-browser click @ref`,
  then continue. Capture only after the overlay is gone, or it will be baked into the PNG.
- **Auth-gated pages**: log in first (snapshot → fill → click → `wait --url`), or reuse
  saved state (`agent-browser state load auth.json`) before Phase 1.
- **Infinite scroll feeds** (height keeps growing while scrolling): loop the scroll pass
  until `scrollHeight` stops growing across two consecutive probes, then verify the PNG
  height against the final probe value, not the initial one.
- **Very tall pages** (height ≳ 16384 px): some Chromium builds cap single-screenshot
  height. Fallback: capture viewport-by-viewport while scrolling, then stitch the tiles
  with Pillow. Gate G5 detects this problem automatically.
- **SPAs with slow client render**: if the body is nearly empty at networkidle, wait on a
  DOM condition instead: `agent-browser wait --fn "window.__ready === true"` or wait for a
  known selector's text before probing and capturing.
- **Animations that never settle**: after the 1.5 s settle, if the visual check shows a
  mid-animation state, pause animations via eval
  (`document.querySelectorAll('*').forEach(e => e.style.animationPlayState = 'paused')`)
  or inject a style `{ animation: none !important; transition: none !important; }`,
  then recapture.
- **Dark mode / theme variants**: `agent-browser set media dark` (or `light`) before
  Phase 1; do a separate capture per theme.

## Pitfalls learned from the reference run

These were observed or actively defended against while capturing a React-style SaaS
landing page (NEO CRM, 1920×4986 px). They are the reasons the gates exist:

1. **Viewport set after navigation** risks a reflow mid-load; always set viewport first.
2. **networkidle alone is not enough.** The reference page reported 0 `<img>` tags — all
   visuals were CSS/SVG — yet it still needed the scroll pass for scroll-triggered
   reveals. "No images to load" is never an excuse to skip Phase 4.
3. **A second networkidle after scrolling** matters: scrolling can fire new requests
   (fonts, route-prefetched chunks) that would otherwise land mid-capture.
4. **Height must be verified against the probe**, not assumed: the reference capture came
   out exactly 1920×4986, matching the probed `scrollHeight` — that equality IS the
   proof of completeness.
5. **Skipping the return-to-top** leaves widgets/sticky elements in a scrolled state in
   the final PNG.
6. **Never trust "✓ Screenshot saved" alone** — the file must pass format/dimension/
   visual verification before being reported as a deliverable.
