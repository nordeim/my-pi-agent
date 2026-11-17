# Layout Catalog — The 10 Page Archetypes

Every deck in this system is a sequence of these archetypes. Each recipe below is
the **content zone** that slots into `assets/page_chassis.html` (cover and closing
replace the whole body). Class strings are canonical — copy them verbatim and swap
only the bracketed `[SLOTS]`.

**Table of contents**

| # | Archetype | Use it for | Recipe |
|---|---|---|---|
| 1 | Cover | Deck opener: title, subtitle, meta card | [§1](#1-cover) |
| 2 | Vision & Metrics | 4 pillars + 4 proof numbers | [§2](#2-vision--metrics) |
| 3 | Chart + Drivers | Doughnut chart + numbered driver list | [§3](#3-chart--drivers) |
| 4 | Persona Triptych | Pains / persona / decision chain | [§4](#4-persona-triptych) |
| 5 | Dark Objectives | 3 big targets on navy (rhythm break) | [§5](#5-dark-objectives) |
| 6 | Pillar Matrix | 6 programs in a 3×2 grid | [§6](#6-pillar-matrix) |
| 7 | Quarterly Roadmap | 4 phase columns + progress bar | [§7](#7-quarterly-roadmap) |
| 8 | Milestone Timeline | 4 month columns with metric + tasks | [§8](#8-milestone-timeline) |
| 9 | Budget + Risk | Doughnut budget split + risk register | [§9](#9-budget--risk) |
| 10 | Closing | Title, 3 highlights, contact bar | [§10](#10-closing) |

**Canonical narrative arc (10-page strategy deck):** 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9 → 10.
Shorter decks: keep 1 and 10, then pick archetypes by content shape (see SKILL.md
selection table). Never place two grid-heavy archetypes (2, 6, 7, 8) back-to-back
without a split layout (3, 4, 9) or the dark page (5) between them.

**Content budgets** (enforced socially — the QA script only checks totals):
content pages carry 60–120 visible words; every list has exactly 4 items (3 only on
the dark objectives page); subtitles are one sentence; driver/risk/task descriptions
are one line each (~12–18 words). Over-stuffing a page breaks the 720px height
budget before the QA script can warn you — trim content, never font sizes.

**Vertical rhythm and the 720px budget.** Every page must FIT the fixed canvas:
85px header + 48px top padding + ~100px title block + content zone + 32px bottom
padding ≤ 720px, which leaves **~455px for the content zone**. The rhythm values in
these recipes (`mt-4`–`mt-8` first-grid margins, compact card paddings, 180px chart
canvases) are pre-budgeted to fit — do not loosen them. Two rules keep you safe:
keep subtitles to ONE line (≤ ~90 characters at 15px in `max-w-3xl`), and when a
description runs long enough to wrap, cut words rather than spacing. The raw sample
deck this system was extracted from overflowed its own canvas by up to 154px on
chart pages — the corrected values here are canonical, and
`scripts/geometry_check.js` verifies the result headlessly.

---

## 1. Cover

**Purpose:** establish brand, tone, and stakes. Full-bleed photo + navy gradient.
**Slots:** eyebrow chip (deck series), title (≤6 words), subtitle (~20 words),
meta card (4 label/value pairs), classification line, brand box, background URL.

```html
<div class="ppt-slide bg-cover bg-center" style="background-image: url('[BACKGROUND_URL]');">
    <!-- Directional overlay: dense on the left where text lives -->
    <div class="absolute inset-0 bg-gradient-to-r from-[#0A2540]/95 via-[#0A2540]/85 to-[#0A2540]/40"></div>

    <div class="relative z-10 h-full flex flex-col justify-between p-12">
        <!-- Top: classification + brand -->
        <div class="flex justify-between items-start">
            <p class="text-white/60 text-[11px] tracking-[0.2em] font-medium">CONFIDENTIAL &amp; PROPRIETARY</p>
            <div class="border border-white/30 rounded px-4 py-2 text-white/80 text-sm tracking-widest">[BRAND]</div>
        </div>

        <!-- Middle: series chip + title ritual + subtitle -->
        <div class="max-w-4xl">
            <span class="inline-block bg-[#FF5722]/20 text-[#FF5722] text-sm font-semibold tracking-[3px] px-4 py-2 rounded">[SERIES_EYEBROW]</span>
            <h1 class="text-white text-[54px] font-black leading-tight mt-6">[TITLE]</h1>
            <div class="w-24 h-1.5 bg-[#FF5722] mt-6"></div>
            <p class="text-white/80 text-lg mt-6 max-w-2xl leading-relaxed">[SUBTITLE]</p>
        </div>

        <!-- Bottom: glass meta card -->
        <div class="grid grid-cols-4 gap-6 max-w-3xl bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20">
            <div>
                <p class="text-white/50 text-xs uppercase tracking-wider">[LABEL_1]</p>
                <p class="text-white text-lg font-bold mt-1">[VALUE_1]</p>
            </div>
            <!-- ×4: Prepared by / Date / Classification / Version -->
        </div>
    </div>
</div>
```

**Pitfalls:** the photo must be dark/calm — busy photos fight the overlay and drop
title contrast below WCAG AA. The title stays left-aligned; never center the cover.

---

## 2. Vision & Metrics

**Purpose:** state the strategic pillars, then prove momentum with numbers.
**Slots:** 4 pillar cards (icon + 8-word title + ~15-word description), 4 metric
cards (value + label). No right slot in the title block.

```html
<!-- Content zone (inside <main> after the title ritual) -->

<!-- Pillar row -->
<div class="grid grid-cols-4 gap-6 mt-10">
    <div class="bg-gradient-to-br from-[#0A2540]/5 to-[#0A2540]/10 rounded-xl p-6 border-2 border-[#0A2540]/10">
        <div class="w-14 h-14 bg-gradient-to-br from-[#FF5722] to-[#FF7043] rounded-xl flex items-center justify-center">
            <i class="material-icons text-white text-[28px]">[ICON]</i>
        </div>
        <h3 class="text-lg font-bold text-[#0A2540] mt-4">[PILLAR_TITLE]</h3>
        <p class="text-[13px] text-[#0A2540]/70 leading-relaxed mt-2">[PILLAR_DESCRIPTION]</p>
    </div>
    <!-- ×4 -->
</div>

<!-- Metric row -->
<div class="grid grid-cols-4 gap-6 mt-6">
    <div class="bg-gradient-to-br from-[#0A2540]/5 to-[#0A2540]/10 rounded-xl p-6 border-2 border-[#0A2540]/10 text-center">
        <p class="text-[44px] font-bold text-[#FF5722]">[VALUE]</p>
        <p class="text-[14px] text-[#0A2540]/70 mt-2">[LABEL]</p>
    </div>
    <!-- ×4 -->
</div>
```

**Pitfalls:** pillar descriptions wrap to 3 lines max at `13px` — write 12–16 words.
Metric values must be short (`220%`, `48`, `99.99%`); long values break the grid.
Icons: one distinct concept per pillar (`rocket_launch`, `hub`, `verified`, `public`).

---

## 3. Chart + Drivers

**Purpose:** quantify a market/budget/allocation story and explain what drives it.
**Slots:** 4 numbered drivers, chart card (icon, title, sub-label, 4 segments,
center figure), 4 legend rows. Chart wiring: see `references/chart-recipes.md`.

```html
<div class="grid grid-cols-12 gap-8 mt-6">
    <!-- Left: drivers -->
    <div class="col-span-5">
        <p class="text-[13px] font-semibold text-[#0A2540]/50 tracking-wider uppercase mb-3">[ZONE_LABEL]</p>
        <div class="space-y-3">
            <div class="bg-white rounded-lg px-4 py-3 border-l-4 border-[#FF5722] shadow-sm">
                <div class="flex items-start gap-3">
                    <span class="text-[#FF5722] font-bold text-lg">01</span>
                    <div>
                        <h4 class="text-[15px] font-bold text-[#0A2540]">[DRIVER_TITLE]</h4>
                        <p class="text-[12px] text-[#0A2540]/60 leading-relaxed mt-1">[DRIVER_DESCRIPTION]</p>
                    </div>
                </div>
            </div>
            <!-- ×4 -->
        </div>
    </div>

    <!-- Right: doughnut chart card -->
    <div class="col-span-7">
        <div class="bg-gradient-to-br from-[#0A2540]/5 to-[#0A2540]/10 rounded-xl px-6 py-5 border-2 border-[#0A2540]/10">
            <div class="flex items-center gap-4">
                <div class="w-12 h-12 bg-gradient-to-br from-[#FF5722] to-[#FF7043] rounded-xl flex items-center justify-center">
                    <i class="material-icons text-white text-2xl">[CHART_ICON]</i>
                </div>
                <div>
                    <h3 class="text-lg font-bold text-[#0A2540]">[CHART_TITLE]</h3>
                    <p class="text-[13px] text-[#0A2540]/60">[CHART_SUBTITLE]</p>
                </div>
            </div>
            <div class="h-[180px] mt-4">
                <canvas id="[CANVAS_ID]"></canvas>
            </div>
            <div class="mt-3 space-y-2">
                <div class="flex items-center justify-between">
                    <div class="flex items-center gap-3">
                        <div class="w-3 h-3 rounded-full bg-[#FF5722]"></div>
                        <span class="text-[13px] text-[#0A2540]/80 font-medium">[SEGMENT_1]</span>
                    </div>
                    <span class="text-[13px] font-bold text-[#0A2540]">[VALUE_1]</span>
                </div>
                <!-- ×4 — dot colors: #FF5722, #FF7043, #0A2540, #0A2540/70 -->
            </div>
        </div>
    </div>
</div>
```

**Pitfalls:** driver descriptions are 12–18 words, one line and a wrap at most.
The chart card is the only place a `w-12 h-12` icon tile appears. Legend values
must match the dataset exactly — they are typed by hand, not generated.

---

## 4. Persona Triptych

**Purpose:** make the buyer human — her pains, her profile, and how she buys.
**Slots:** 4 pain cards (icon + title + description), 1 persona card (avatar, name,
role, quote, 2 stats), 4 decision-chain steps.

```html
<div class="grid grid-cols-12 gap-6 mt-4">
    <!-- Left: pain points -->
    <div class="col-span-4">
        <p class="text-[13px] font-semibold text-[#0A2540]/50 tracking-wider uppercase mb-3">[ZONE_LABEL_EG_TOP_PAIN_POINTS]</p>
        <div class="space-y-2">
            <div class="bg-gradient-to-br from-[#0A2540]/5 to-[#0A2540]/10 rounded-lg px-4 py-3 border-l-4 border-[#FF5722]">
                <div class="flex items-start gap-3">
                    <i class="material-icons text-[#FF5722] text-xl mt-0.5">[ICON]</i>
                    <div>
                        <h4 class="text-[15px] font-bold text-[#0A2540]">[PAIN_TITLE]</h4>
                        <p class="text-[12px] text-[#0A2540]/60 leading-relaxed mt-1">[PAIN_DESCRIPTION]</p>
                    </div>
                </div>
            </div>
            <!-- ×4 -->
        </div>
    </div>

    <!-- Center: persona card (the only navy card on a light page) -->
    <div class="col-span-4">
        <div class="bg-[#0A2540] rounded-2xl p-8 text-center relative overflow-hidden">
            <!-- Decorative corner circles -->
            <div class="absolute -top-10 -right-10 w-40 h-40 bg-[#FF5722]/10 rounded-full"></div>
            <div class="absolute -bottom-10 -left-10 w-32 h-32 bg-[#FF5722]/10 rounded-full"></div>
            <div class="relative">
                <div class="w-20 h-20 bg-gradient-to-br from-[#FF5722] to-[#FF7043] rounded-full mx-auto flex items-center justify-center">
                    <i class="material-icons text-white text-4xl">person</i>
                </div>
                <h3 class="text-white text-2xl font-bold mt-4">[PERSONA_NAME]</h3>
                <p class="text-[#FF5722] text-sm font-medium mt-1">[PERSONA_ROLE]</p>
                <div class="w-12 h-0.5 bg-[#FF5722] mx-auto my-4"></div>
                <p class="text-white/80 text-sm leading-relaxed italic">"[PERSONA_QUOTE]"</p>
                <div class="grid grid-cols-2 gap-4 mt-4">
                    <div class="bg-white/5 rounded-lg p-3">
                        <p class="text-[#FF5722] text-xl font-bold">[STAT_1_VALUE]</p>
                        <p class="text-white/60 text-[11px] mt-1">[STAT_1_LABEL]</p>
                    </div>
                    <div class="bg-white/5 rounded-lg p-3">
                        <p class="text-[#FF5722] text-xl font-bold">[STAT_2_VALUE]</p>
                        <p class="text-white/60 text-[11px] mt-1">[STAT_2_LABEL]</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Right: decision chain -->
    <div class="col-span-4">
        <p class="text-[13px] font-semibold text-[#0A2540]/50 tracking-wider uppercase mb-4">[ZONE_LABEL_EG_DECISION_CHAIN]</p>
        <div class="space-y-5">
            <div class="flex items-start gap-4">
                <div class="w-10 h-10 bg-[#FF5722] rounded-full flex-shrink-0 flex items-center justify-center text-white font-bold">1</div>
                <div>
                    <h4 class="text-[15px] font-bold text-[#0A2540]">[STEP_TITLE]</h4>
                    <p class="text-[12px] text-[#0A2540]/60 leading-relaxed mt-1">[STEP_DESCRIPTION]</p>
                </div>
            </div>
            <!-- ×4, numbered 1–4 -->
        </div>
    </div>
</div>
```

**Pitfalls:** the persona quote is 20–25 words, italic, in quotes. Pain cards here
use the tinted variant (no `bg-white`/`shadow-sm`) so the navy persona card
dominates the middle. Keep persona name/role to real-sounding specifics.

---

## 5. Dark Objectives

**Purpose:** the deck's rhythm break — three audacious targets on full navy.
**Build:** same chassis, but `.ppt-slide` gets `bg-[#0A2540]`; the header bar stays
(it blends into the background — that is intended); title block goes white; a chip
sits in the title-block right slot.

```html
<div class="ppt-slide bg-[#0A2540]">
    <!-- [standard 85px header bar] -->
    <main class="p-12 pb-8">
        <div class="flex items-end justify-between">
            <div>
                <h1 class="text-[40px] font-bold text-white leading-tight">[PAGE_TITLE]</h1>
                <div class="w-20 h-1 bg-[#FF5722] mt-4"></div>
                <p class="text-[15px] text-white/60 mt-3 max-w-3xl">[SUBTITLE]</p>
            </div>
            <span class="bg-[#FF5722]/10 text-[#FF5722] text-sm font-medium px-4 py-2 rounded-full">[HORIZON_CHIP]</span>
        </div>

        <div class="grid grid-cols-3 gap-6 mt-4">
            <div class="bg-white/5 rounded-xl p-6 border border-white/10">
                <div class="w-16 h-16 bg-gradient-to-br from-[#FF5722] to-[#FF7043] rounded-xl flex items-center justify-center">
                    <i class="material-icons text-white text-3xl">[ICON]</i>
                </div>
                <p class="text-[52px] font-bold text-[#FF5722] mt-4">[TARGET_VALUE]</p>
                <h3 class="text-white text-xl font-bold mt-2">[TARGET_TITLE]</h3>
                <p class="text-white/60 text-sm leading-relaxed mt-4">[TARGET_DESCRIPTION]</p>
            </div>
            <!-- ×3 -->
        </div>

        <!-- Bottom highlight (dark variant) -->
        <div class="bg-gradient-to-r from-[#FF5722]/10 to-transparent border-l-4 border-[#FF5722] rounded-r-lg p-5 mt-4 flex items-center gap-4">
            <div class="w-10 h-10 bg-[#FF5722] rounded-lg flex items-center justify-center flex-shrink-0">
                <i class="material-icons text-white text-xl">[ICON]</i>
            </div>
            <div>
                <p class="text-[15px] font-bold text-white/90">[TAKEAWAY_HEADLINE]</p>
                <p class="text-[13px] text-white/60 mt-1">[TAKEAWAY_DETAIL]</p>
            </div>
        </div>
    </main>
</div>
```

**Pitfalls:** exactly 3 cards (the 52px metrics need width). This is the only dark
content page in a standard deck — a second dark page dilutes the rhythm break.
Target descriptions run 18–24 words; trim before shrinking type.

---

## 6. Pillar Matrix

**Purpose:** show the full program portfolio — six coordinated initiatives.
**Slots:** 6 pillar cards (icon + 17px title + description + 2 tag chips), bottom
highlight bar.

```html
<div class="grid grid-cols-3 gap-6 mt-6">
    <div class="bg-gradient-to-br from-[#0A2540]/5 to-[#0A2540]/10 rounded-xl p-4 border-2 border-[#0A2540]/10">
        <div class="flex items-start gap-4">
            <div class="w-14 h-14 bg-gradient-to-br from-[#FF5722] to-[#FF7043] rounded-xl flex items-center justify-center flex-shrink-0">
                <i class="material-icons text-white text-[28px]">[ICON]</i>
            </div>
            <div>
                <h3 class="text-[17px] font-bold text-[#0A2540]">[PILLAR_TITLE]</h3>
                <p class="text-[13px] text-[#0A2540]/70 leading-relaxed mt-2">[PILLAR_DESCRIPTION]</p>
                <div class="flex gap-2 mt-4">
                    <span class="bg-[#FF5722]/10 text-[#FF5722] text-[11px] px-3 py-1 rounded-full font-medium">[TAG_1]</span>
                    <span class="bg-[#FF5722]/10 text-[#FF5722] text-[11px] px-3 py-1 rounded-full font-medium">[TAG_2]</span>
                </div>
            </div>
        </div>
    </div>
    <!-- ×6 (two rows of three) -->
</div>

<div class="bg-gradient-to-r from-[#FF5722]/10 to-transparent border-l-4 border-[#FF5722] rounded-r-lg p-4 mt-5 flex items-center gap-4">
    <div class="w-10 h-10 bg-[#FF5722] rounded-lg flex items-center justify-center flex-shrink-0">
        <i class="material-icons text-white text-xl">[ICON]</i>
    </div>
    <div>
        <p class="text-[15px] font-bold text-[#0A2540]">[TAKEAWAY_HEADLINE]</p>
        <p class="text-[13px] text-[#0A2540]/70 mt-1">[TAKEAWAY_DETAIL]</p>
    </div>
</div>
```

**Pitfalls:** descriptions ≤3 lines at 13px (~20 words) or row 2 overflows 720px —
the compact `p-4` card padding is part of the height budget on this archetype.
Tags are single words. `flex-shrink-0` on the icon tile keeps text columns even.

---

## 7. Quarterly Roadmap

**Purpose:** phased execution plan with honest status per phase.
**Slots (title block right):** status legend — two dot+label pairs. Then 4 quarter
columns + one progress card.

```html
<!-- Title-block right slot -->
<div class="flex items-center gap-6">
    <div class="flex items-center gap-2">
        <div class="w-3 h-3 rounded-full bg-[#FF5722]"></div>
        <span class="text-[13px] text-[#0A2540]/70 font-medium">On Track</span>
    </div>
    <div class="flex items-center gap-2">
        <div class="w-3 h-3 rounded-full bg-[#0A2540]/40"></div>
        <span class="text-[13px] text-[#0A2540]/70 font-medium">At Risk</span>
    </div>
</div>

<!-- Quarter columns -->
<div class="grid grid-cols-4 gap-6 mt-8">
    <div class="bg-gradient-to-br from-[#0A2540]/5 to-[#0A2540]/10 rounded-xl p-6 border-2 border-[#0A2540]/10">
        <div class="flex items-center justify-between">
            <span class="bg-[#0A2540] text-white text-sm font-bold px-4 py-1.5 rounded-full">Q1 [YEAR]</span>
            <span class="bg-[#FF5722]/10 text-[#FF5722] text-[11px] font-bold px-3 py-1 rounded-full">[STATUS]</span>
        </div>
        <h3 class="text-lg font-bold text-[#0A2540] mt-5">[PHASE_NAME]</h3>
        <div class="space-y-3 mt-4">
            <div class="flex items-start gap-3">
                <i class="material-icons text-[#FF5722] text-lg">check_circle</i>
                <span class="text-[13px] text-[#0A2540]/70 leading-relaxed">[MILESTONE]</span>
            </div>
            <!-- pending milestone instead: -->
            <!-- <i class="material-icons text-[#0A2540]/40 text-lg">radio_button_unchecked</i> -->
            <!-- ×3–4 milestones per quarter -->
        </div>
    </div>
    <!-- ×4; AT RISK status uses: bg-[#0A2540]/10 text-[#0A2540] -->
</div>

<!-- Progress card -->
<div class="bg-gradient-to-br from-[#0A2540]/5 to-[#0A2540]/10 rounded-xl p-6 border-2 border-[#0A2540]/10 mt-5">
    <div class="flex items-center justify-between">
        <p class="text-[13px] font-semibold text-[#0A2540]">[PROGRESS_LABEL]</p>
        <p class="text-[#FF5722] text-sm font-bold">[PERCENT]</p>
    </div>
    <div class="w-full h-3 bg-[#0A2540]/10 rounded-full mt-3">
        <div class="w-[78%] h-full bg-gradient-to-r from-[#FF5722] to-[#FF7043] rounded-full"></div>
    </div>
</div>
```

**Pitfalls:** the progress fill `w-[N%]` must match the printed percent exactly.
Completed milestones use `check_circle` in orange; pending use
`radio_button_unchecked` in `text-[#0A2540]/40`. Max 4 milestones per quarter.

---

## 8. Milestone Timeline

**Purpose:** near-term execution calendar — what lands, in which month.
**Slots (title block right):** a metric chip. Then 4 month columns + highlight bar.

```html
<!-- Title-block right slot: metric chip -->
<div class="bg-[#0A2540]/5 border-2 border-[#0A2540]/10 rounded-xl px-6 py-3 text-center">
    <p class="text-[#FF5722] text-2xl font-bold">[VALUE]</p>
    <p class="text-[#0A2540]/60 text-xs mt-1">[LABEL_EG_WEEKS_TO_LAUNCH]</p>
</div>

<!-- Month columns -->
<div class="grid grid-cols-4 gap-6 mt-8">
    <div class="bg-gradient-to-br from-[#0A2540]/5 to-[#0A2540]/10 rounded-xl p-6 border-2 border-[#0A2540]/10">
        <span class="bg-[#0A2540]/10 text-[#0A2540] text-xs font-bold px-3 py-1 rounded-full">[MONTH]</span>
        <p class="text-[#FF5722] text-[36px] font-bold mt-4">[METRIC_VALUE]</p>
        <p class="text-[13px] text-[#0A2540]/70">[METRIC_LABEL]</p>
        <div class="w-full h-px bg-[#0A2540]/10 my-4"></div>
        <div class="space-y-3">
            <div class="flex items-start gap-3">
                <i class="material-icons text-[#FF5722] text-base mt-0.5">arrow_forward</i>
                <span class="text-[12px] text-[#0A2540]/70">[TASK]</span>
            </div>
            <!-- ×3 tasks per month -->
        </div>
    </div>
    <!-- ×4 months -->
</div>

<!-- Bottom highlight bar: the critical-path / dependency statement -->
<div class="bg-gradient-to-r from-[#FF5722]/10 to-transparent border-l-4 border-[#FF5722] rounded-r-lg p-5 mt-8 flex items-center gap-4">
    <div class="w-10 h-10 bg-[#FF5722] rounded-lg flex items-center justify-center flex-shrink-0">
        <i class="material-icons text-white text-xl">schedule</i>
    </div>
    <div>
        <p class="text-[15px] font-bold text-[#0A2540]">[TAKEAWAY_HEADLINE]</p>
        <p class="text-[13px] text-[#0A2540]/70 mt-1">[TAKEAWAY_DETAIL]</p>
    </div>
</div>
```

**Pitfalls:** tasks are 3–6 words each — this is a calendar, not an essay. The
36px metric wants short values (`4`, `12`, `2`). Use the highlight bar for the
critical-path dependency between months.

---

## 9. Budget + Risk

**Purpose:** show where the money goes and what could go wrong — on one page.
**Slots:** budget chart card (4 segments + center total), 4 risk rows with severity
chips. Chart wiring: see `references/chart-recipes.md`.

```html
<div class="grid grid-cols-12 gap-8 mt-6">
    <!-- Left: budget doughnut -->
    <div class="col-span-5">
        <div class="bg-gradient-to-br from-[#0A2540]/5 to-[#0A2540]/10 rounded-xl p-6 border-2 border-[#0A2540]/10">
            <div class="flex items-center gap-4">
                <div class="w-12 h-12 bg-gradient-to-br from-[#FF5722] to-[#FF7043] rounded-xl flex items-center justify-center">
                    <i class="material-icons text-white text-2xl">account_balance_wallet</i>
                </div>
                <div>
                    <h3 class="text-lg font-bold text-[#0A2540]">[CHART_TITLE_EG_BUDGET_ALLOCATION]</h3>
                    <p class="text-[13px] text-[#0A2540]/60">[CHART_SUBTITLE_EG_FY_DISTRIBUTION]</p>
                </div>
            </div>
            <div class="h-[240px] mt-4">
                <canvas id="[CANVAS_ID]"></canvas>
            </div>
            <div class="mt-4 space-y-3">
                <div class="flex items-center justify-between">
                    <div class="flex items-center gap-3">
                        <div class="w-3 h-3 rounded-full bg-[#FF5722]"></div>
                        <span class="text-[13px] text-[#0A2540]/80 font-medium">[SEGMENT]</span>
                    </div>
                    <span class="text-[13px] font-bold text-[#0A2540]">[AMOUNT]</span>
                </div>
                <!-- ×4 — amounts, not percentages, in this legend -->
            </div>
        </div>
    </div>

    <!-- Right: risk register -->
    <div class="col-span-7">
        <p class="text-[13px] font-semibold text-[#0A2540]/50 tracking-wider uppercase mb-3">[ZONE_LABEL_EG_KEY_RISKS_AND_MITIGATION]</p>
        <!-- 2x2 grid — a vertical stack of four two-line risks cannot fit the
             ~455px content budget -->
        <div class="grid grid-cols-2 gap-4">
            <div class="bg-gradient-to-br from-[#0A2540]/5 to-[#0A2540]/10 rounded-xl p-5 border-l-4 border-[#FF5722]">
                <div class="flex items-center justify-between gap-4">
                    <h4 class="text-[16px] font-bold text-[#0A2540]">[RISK_TITLE]</h4>
                    <!-- HIGH: -->
                    <span class="bg-[#FF5722]/10 text-[#FF5722] text-xs font-bold px-3 py-1.5 rounded-full h-fit flex-shrink-0">HIGH</span>
                    <!-- MEDIUM: bg-[#0A2540]/10 text-[#0A2540] -->
                </div>
                <p class="text-[12px] text-[#0A2540]/60 mt-1">[RISK_DESCRIPTION]</p>
                <p class="text-[11px] font-semibold text-[#0A2540]/50 uppercase tracking-wider mt-3">Mitigation</p>
                <p class="text-[12px] text-[#0A2540]/70 mt-1">[MITIGATION]</p>
            </div>
            <!-- ×4 in the 2x2 grid -->
        </div>
    </div>
</div>
```

**Pitfalls:** risk descriptions ~15 words, mitigations ~12 words. The 2×2 grid is
load-bearing — do not switch back to a vertical stack. The chart canvas is
`h-[240px]` here (vs 180px on archetype 3); verify with `scripts/geometry_check.js`
if any description wraps past two lines.

---

## 10. Closing

**Purpose:** end with the mandate and the ask. Full-bleed photo + uniform overlay.
**Slots:** series chip, title (≤5 words), subtitle (~18 words), 3 highlight chips,
contact bar (name/role left; email + site right).

```html
<div class="ppt-slide bg-cover bg-center" style="background-image: url('[BACKGROUND_URL]');">
    <!-- Uniform overlay: everything centered, calmer than the cover -->
    <div class="absolute inset-0 bg-gradient-to-br from-[#0A2540]/95 via-[#0A2540]/90 to-[#0A2540]/80"></div>

    <div class="relative z-10 h-full flex flex-col items-center justify-center p-12">
        <span class="inline-block bg-[#FF5722]/20 text-[#FF5722] text-sm font-semibold tracking-[3px] px-4 py-2 rounded">[SERIES_EYEBROW]</span>
        <h1 class="text-white text-[44px] font-bold text-center leading-tight mt-6">[TITLE]</h1>
        <div class="w-20 h-1.5 bg-[#FF5722] mt-6"></div>
        <p class="text-white/70 text-lg text-center mt-6 max-w-2xl leading-relaxed">[SUBTITLE]</p>

        <!-- Highlight chips -->
        <div class="flex gap-4 mt-10">
            <div class="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl px-6 py-4 flex items-center gap-3">
                <i class="material-icons text-[#FF5722] text-2xl">[ICON]</i>
                <div>
                    <p class="text-white font-bold text-lg">[VALUE]</p>
                    <p class="text-white/60 text-xs">[LABEL]</p>
                </div>
            </div>
            <!-- ×3 -->
        </div>
    </div>

    <!-- Contact bar -->
    <div class="absolute bottom-0 left-0 right-0 bg-[#0A2540]/80 backdrop-blur-md border-t border-white/10 px-12 py-5 flex items-center justify-between">
        <div>
            <p class="text-white/90 font-bold">[OWNER_NAME]</p>
            <p class="text-white/50 text-sm">[OWNER_ROLE]</p>
        </div>
        <div class="flex items-center gap-6">
            <div class="flex items-center gap-2">
                <i class="material-icons text-[#FF5722] text-base">mail</i>
                <span class="text-white/60 text-sm">[EMAIL]</span>
            </div>
            <div class="flex items-center gap-2">
                <i class="material-icons text-[#FF5722] text-base">language</i>
                <span class="text-white/60 text-sm">[WEBSITE]</span>
            </div>
        </div>
    </div>
</div>
```

**Pitfalls:** the three highlight chips echo the deck's three most important
numbers — they are the last thing the audience reads. Keep the photo distinct from
the cover's (different mood: forward-looking vs reflective works well).

---

## Extending the system (when 10 archetypes are not enough)

Prefer recombining existing components over inventing new layouts:

- **Comparison page** — two `col-span-6` gradient cards, each with an icon tile
  header and a list; keep the title ritual and header bar.
- **Section divider** — reuse the Dark Objectives chassis with a single 52px
  statement and no cards; add the chapter chip in the title-block right slot.
- **Big quote page** — closing chassis minus the contact bar, quote at 40px bold
  white, attribution in the series-chip style.

Any new page must: keep the 85px header bar (content pages), the orange underline
ritual, the locked palette, and pass `scripts/qa_check.py`. If a new layout is used
more than once, promote it into this catalog with the same recipe format.
