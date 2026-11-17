# Chart Recipes — Chart.js Doughnut System

The reference deck uses exactly ONE chart type: the **doughnut**, drawn with
Chart.js from CDN. This constraint is a feature — a single calm chart per page,
with the number that matters written in the middle, beats a dashboard of squinty
charts. Do not introduce bar/line/radar charts unless the user explicitly asks;
if they do, keep the palette, spacing, and legend rules below.

## Wiring (in order — order matters)

1. Chart.js CDN in `<head>`, after the Material Icons link:
   ```html
   <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
   ```
2. A sized wrapper around the canvas (Chart.js needs a constrained parent):
   ```html
   <div class="h-[180px] mt-4"><canvas id="marketChart"></canvas></div>
   ```
   Heights: `h-[180px]` on Chart+Drivers pages · `h-[240px]` on Budget+Risk pages.
   Both are part of the 720px height budget (see layout-catalog's "Vertical rhythm"
   section) — a taller canvas silently pushes the legend off the canvas.
3. The init script as the LAST child of `<body>`, after the slide markup:
   ```html
   <script>
       const centerTextPlugin = { /* see below */ };
       new Chart(document.getElementById('marketChart'), { /* see below */ });
   </script>
   ```
   If the script runs before the canvas exists, the chart silently never renders —
   this ordering is why the QA script checks for `new Chart(`.

## Center-text plugin (canonical)

```js
const centerTextPlugin = {
    id: 'centerText',
    afterDraw(chart) {
        const { ctx } = chart;
        const meta = chart.getDatasetMeta(0);
        const x = meta.data[0].x;
        const y = meta.data[0].y;
        ctx.save();
        ctx.textAlign = 'center';
        ctx.font = 'bold 28px Roboto';
        ctx.fillStyle = '#0A2540';
        ctx.fillText('[BIG_NUMBER]', x, y - 5);
        ctx.font = '500 13px Roboto';
        ctx.fillStyle = '#0A254099';
        ctx.fillText('[CENTER_LABEL]', x, y + 18);
        ctx.restore();
    }
};
```

The big number is the page's takeaway (`$5.8B` TAM, `$40M` total budget); the label
is its unit (`Global TAM`, `Total Budget`). On the rare case of a doughnut on a dark
card, switch fills to `#FFFFFF` / `#FFFFFF99`.

## Chart configuration (canonical)

```js
new Chart(document.getElementById('[CANVAS_ID]'), {
    type: 'doughnut',
    data: {
        labels: ['[Segment 1]', '[Segment 2]', '[Segment 3]', '[Segment 4]'],
        datasets: [{
            data: [38, 27, 22, 13],
            backgroundColor: ['#FF5722', '#FF7043', '#0A2540', '#0A2540B3'],
            borderWidth: 4,
            borderColor: '#FEFEFE',
            hoverOffset: 8
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '65%',
        plugins: {
            legend: { display: false }
        }
    },
    plugins: [centerTextPlugin]
});
```

Non-negotiables, and why:

- **`cutout: '65%'`** (use `'68%'` only when the center number is short like `$40M`)
  — leaves room for two centered text lines without the ring collapsing.
- **`legend: { display: false }`** — the built-in legend cannot match the design's
  typography; the custom legend rows below the chart are the real legend.
- **`maintainAspectRatio: false`** — otherwise Chart.js letterboxes the chart inside
  the fixed-height wrapper.
- **`borderColor: '#FEFEFE'`** — segment separators only read as separators when
  they match the card's tint base.
- **Exactly 4 segments** (3 minimum, 5 absolute max) — more segments turn the ring
  into mud and the legend into a wall.

## Palette discipline

```
hero segment    → #FF5722   (orange — the largest or most important share)
second          → #FF7043   (light orange)
third           → #0A2540   (navy)
fourth          → #0A2540B3 (navy @ 70% — in HTML legend rows: bg-[#0A2540]/70)
```

Order segments largest-first (hero first). The custom legend below the chart must
repeat this exact order and these exact colors.

## Custom legend (canonical row)

```html
<div class="mt-3 space-y-2">
    <div class="flex items-center justify-between">
        <div class="flex items-center gap-3">
            <div class="w-3 h-3 rounded-full bg-[#FF5722]"></div>
            <span class="text-[13px] text-[#0A2540]/80 font-medium">[Segment label]</span>
        </div>
        <span class="text-[13px] font-bold text-[#0A2540]">[Value]</span>
    </div>
    <!-- ×4 -->
</div>
```

Legend values: **percentages** on market-share charts (`38%`), **amounts** on
budget charts (`$16M`). Whatever the dataset uses, the legend repeats — do not
mix units on one page, and never let legend values disagree with `data:`.

## Checklist before shipping a chart page

- [ ] Chart.js `<script>` present in `<head>`; init script is the last `<body>` child
- [ ] Canvas wrapped in the sized `div` (`h-[180px]` / `h-[240px]`)
- [ ] 4 segments, palette order `#FF5722 → #FF7043 → #0A2540 → #0A2540B3`
- [ ] Center number/label match the page's message, not just the data
- [ ] Custom legend order/colors mirror the dataset; units consistent
- [ ] `scripts/qa_check.py` reports `chart wiring (Chart.js CDN + init script)` PASS
