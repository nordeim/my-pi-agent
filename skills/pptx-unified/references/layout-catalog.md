# Layout Catalog — 12 Patterns

> 12 battle-tested layout patterns for 1280×720 slides. Each has a structural spec, when-to-use rule, and anti-patterns to avoid.

---

## 1. `cover` — Title slide

**When:** Slide 1. Repo/product name + tagline + stat cards.

**Structure:**
- Top-left eyebrow with accent-dot (e.g., "GITHUB REPO · nordeim/my-pi-agent")
- Center-left massive title (Inter 800, ~110-120px)
- Below title, tagline (Inter 500, ~28px, muted)
- Below tagline, row of 3 `.tag` pills
- Right side: vertical stack of 3 stat cards (`.card .card-accent`), each with big mono number + label
- Bottom `.footer` with repo URL + version

**Layout split:** Left 55% / Right 45%, both vertically centered.

**Anti-patterns:**
- ❌ Title at 120px+ that clips the left column (drop to 110px)
- ❌ More than 3 stat cards on the right (overcrowded)
- ❌ Hero image behind the title (Linear-style covers are photo-free)

---

## 2. `stat_block` — Hero stat

**When:** One massive number dominates the slide. The "hook" slide.

**Structure:**
- Top-left eyebrow with accent-dot
- Center: massive number (JetBrains Mono 700, ~280px, accent color, text-shadow glow)
- Below number: thin 80px accent line (2px tall)
- Below line: subtitle (Inter 600, ~36px, primary)
- Below subtitle: one-line context (Inter 400, ~20px, muted, max-width 880px, centered)
- Bottom-left small mono note (provenance)
- Bottom-right `.tag` pill

**Layout:** Vertically + horizontally centered. Maximum whitespace.

**Anti-patterns:**
- ❌ Multiple stats on the same slide (defeats the "hero" purpose)
- ❌ Number smaller than 200px (loses impact)
- ❌ Photo behind the number (distracts)

---

## 3. `bento_grid` — Component overview

**When:** 3-4 equal-weight components to introduce (e.g., "What's in the box" — skills/extensions/themes/docs).

**Structure:**
- Top eyebrow with accent-dot
- Slide title (Inter 700, ~40px)
- 2×2 grid of `.card` elements (gap 20px, each ~540×220px)
- Each card: Material Icon (accent) + big mono number (48px accent) + label (20px primary) + one-liner (15px muted)
- Bottom `.footer`

**Layout:** Title at top (~80px), 2×2 grid below filling remaining space.

**Anti-patterns:**
- ❌ Unequal card sizes (breaks the "bento" grid feel)
- ❌ More than 4 cards (use `stats_grid` instead)
- ❌ Cards without an icon (feels empty)

---

## 4. `stats_grid` — Dense category map

**When:** 8-10 items to show with counts (e.g., 10 categories with skill counts).

**Structure:**
- Top eyebrow with accent-dot
- Title (Inter 700, ~36px) + subtitle (Inter 400, ~16px, muted)
- 5×2 grid of small category cards (gap 12px, each ~220×130px)
- Each card: mono count (32px accent) + label (15px primary) + one-liner (12px muted)
- Bottom-right `.tag` pill

**Layout:** Title at top (~80px), 5×2 grid below filling remaining space.

**Anti-patterns:**
- ❌ More than 10 cards (split into 2 slides or use a table)
- ❌ Cards with body text instead of a one-liner (grid becomes unreadable)
- ❌ Inconsistent card heights (use grid auto-rows)

---

## 5. `section_divider` — Chapter break

**When:** Chapter transition in a deck ≥10 slides. "01 / 03" chapter marker.

**Structure:**
- Top-left chapter marker (JetBrains Mono 500, ~16px, accent) — "01 / 03"
- Center-left massive title (Inter 800, ~88px, primary)
- Below title, tagline (Inter 400, ~24px, muted)
- Below tagline, row of `.tag` pills
- Right side: vertical accent line (3px wide, 400px tall) with 3 dots spaced along it, each labeled in mono

**Layout:** Left 60% for title block, right 40% for vertical accent rail. Maximum whitespace. Use `.grid-bg` for subtle background.

**Anti-patterns:**
- ❌ Body bullets or images (defeats the "breath" purpose)
- ❌ More than 5 tag pills
- ❌ Dense content (this slide should feel empty)

---

## 6. `split_text_features` — Item list + "why"

**When:** A list of items on the left, with a "why this matters" card on the right.

**Structure:**
- Top eyebrow with accent-dot
- Title (Inter 700, ~36px) + subtitle (Inter 400, ~16px, muted)
- LEFT COLUMN (~48% width): N item rows, each a `.card .card-accent` stacked with 12px gap. Each card: item name (mono 600, 22px, accent) + one-line description (Inter 400, 14px, primary)
- RIGHT COLUMN (~48% width): single `.card` with header (18px primary 600) + bulleted list (each bullet with accent dot, 15px primary)

**Layout:** Title at top, two columns below filling remaining space, 24px gap between columns.

**Anti-patterns:**
- ❌ More than 5 items in the left column (use `comparison_card` instead)
- ❌ Right column without a header (feels disconnected)
- ❌ Inconsistent card heights in the left column

---

## 7. `comparison_card` — 3 variants side-by-side

**When:** Comparing 3 alternatives (e.g., 3 Office skill families).

**Structure:**
- Top eyebrow with accent-dot
- Title (Inter 700, ~36px) + subtitle (Inter 400, ~16px, muted)
- 3-column grid (gap 16px, each card ~380×400px, `.card .card-accent`)
- Each card: header (mono 600, 22px, accent) + subhead (13px muted) + bulleted feature list (14px primary, accent dots)

**Layout:** Title at top, 3-column grid below filling remaining space.

**Anti-patterns:**
- ❌ More than 3 cards (use `three_column_spotlight` or split into 2 slides)
- ❌ Inconsistent bullet counts across the 3 cards (visually unbalanced)
- ❌ Cards without the accent left border (loses the "comparison" feel)

---

## 8. `three_column_spotlight` — 3 categories with tag clouds

**When:** 3 categories to spotlight, each with a tag cloud of item names.

**Structure:**
- Top eyebrow with accent-dot
- Title (Inter 700, ~36px) + subtitle (Inter 400, ~16px, muted)
- 3-column grid (gap 16px, each column ~380×420px, `.card`)
- Each column: top row = big mono count (48px accent) + label (16px primary 600) + subhead (13px muted). Then a tag cloud of item names (each as small `.tag` pill, wrap with 8px gap). Below tags, one-liner (14px muted).

**Layout:** Title at top, 3-column grid below filling remaining space.

**Anti-patterns:**
- ❌ Tag pills that don't wrap (overflow the column)
- ❌ More than 12 tags per column (becomes unreadable)
- ❌ Inconsistent counts across the 3 columns (visually unbalanced)

---

## 9. `timeline` — N-step pipeline

**When:** Showing a workflow with N sequential steps (e.g., 5-step gaokao pipeline).

**Structure:**
- Top eyebrow with accent-dot
- Title (Inter 700, ~36px) + subtitle (Inter 400, ~16px, muted)
- Horizontal timeline: N vertical cards (~210×280px, `.card .card-accent`), arranged in a row with 20px gap
- Connecting 2px accent line runs through the vertical center of the row, BEHIND the cards
- Each card: step number (mono 700, 36px, accent) + step name (mono 500, 14px, primary) + thin divider + role (Inter 400, 13px, primary, 2-3 lines) + output artifact (mono 500, 12px, accent)
- Below timeline, `.tag` pill row

**Layout:** Title at top, horizontal timeline below filling remaining space.

**Anti-patterns:**
- ❌ More than 6 steps (split into 2 slides or use a different layout)
- ❌ Connecting line IN FRONT of the cards (obscures content)
- ❌ Steps without an output artifact (breaks the "pipeline" narrative)

---

## 10. `step_guide` — Setup instructions

**When:** N numbered steps with terminal commands.

**Structure:**
- Top eyebrow with accent-dot
- Title (Inter 700, ~36px) + subtitle (Inter 400, ~16px, muted)
- N horizontal step cards (gap 16px, each ~380×340px, `.card`)
- Each card: top row = mono step number (40px accent) + label (14px primary 600, letter-spacing 0.08em). Below, a dark code block (background `var(--bg-surface)`, border, border-radius 8px, padding 16px) with mono 400, 14px, primary. Below code block, one-liner (13px muted).
- Bottom strip: full-width `.card-accent` with 3 columns of pro-tips

**Layout:** Title at top, N step cards in a row below, pro-tip strip at bottom.

**Anti-patterns:**
- ❌ Code blocks without dark surface background (loses the "terminal" feel)
- ❌ More than 4 steps (split into 2 slides)
- ❌ Pro-tip strip with more than 3 tips (overcrowded)

---

## 11. `closing` — Final CTA

**When:** Last slide. Big URL + tagline + 3 takeaways.

**Structure:**
- Top eyebrow with accent-dot ("THE ASK")
- Center: massive URL (JetBrains Mono 700, ~60-64px, accent)
- Below URL, tagline (Inter 600, ~36px, primary)
- Below tagline, thin 120px accent line (2px tall, centered)
- Below line, 3 takeaway columns (gap 24px, each ~360×140px, `.card .card-accent`): big mono number (40px accent) + label (15px primary) + sub (13px muted)
- Bottom-right `.tag` pill row
- Bottom-left small mono note
- Background: `.grid-bg` utility (bookending the cover)

**Layout:** URL + tagline vertically centered, takeaways below, pills bottom-right.

**Anti-patterns:**
- ❌ URL at 64px+ that clips (drop to 60px for 30-char strings)
- ❌ More than 3 takeaways (overcrowded)
- ❌ No accent line between tagline and takeaways (loses visual hierarchy)

---

## 12. `quote` — Pull quote (bonus)

**When:** A single impactful quote needs its own slide.

**Structure:**
- Top eyebrow with accent-dot
- Center: large opening quotation mark (Inter 800, ~120px, accent-soft)
- Below mark, quote text (Inter 500, ~32px, primary, max-width 900px, line-height 1.4)
- Below quote, attribution (Inter 400, ~18px, muted, with em-dash prefix)
- Bottom `.footer`

**Layout:** Vertically centered, maximum whitespace.

**Anti-patterns:**
- ❌ Quote text smaller than 28px (loses impact)
- ❌ More than 2 lines of quote (use a different layout)
- ❌ Attribution without an em-dash (feels disconnected)

---

## Layout selection rules

1. **Diversify across consecutive slides.** Never repeat the same layout back-to-back.
2. **A 12-slide deck should use 8+ distinct layouts.**
3. **Cover is always `cover`.** Closing is always `closing`.**
4. **Section dividers use `section_divider`.** Don't use it for content slides.
5. **For 3+ items:** 3 items → `comparison_card`. 4 items → `bento_grid` (2×2). 5-6 items → `split_text_features` or `timeline`. 8-10 items → `stats_grid`.

## Layout + narrative mapping

For a standard 12-slide marketing deck:

| Slide | Layout | Narrative |
|-------|--------|-----------|
| 1 | `cover` | Title + tagline + 3 stats |
| 2 | `stat_block` | Hero stat (the hook) |
| 3 | `bento_grid` | "What's in the box" — 4 components |
| 4 | `stats_grid` | Category map — 10 items with counts |
| 5 | `section_divider` | Chapter 01/03 |
| 6 | `split_text_features` | Family 1 — items + "why" |
| 7 | `comparison_card` | Family 2 — 3 variants compared |
| 8 | `comparison_card` | Family 3 — 3 variants compared |
| 9 | `three_column_spotlight` | Beyond the main focus — 3 categories |
| 10 | `timeline` | Skill composition — 5-step pipeline |
| 11 | `step_guide` | Setup in 3 steps with code |
| 12 | `closing` | CTA + 3 takeaways |
