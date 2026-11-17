// geometry_check.js — optional height-budget audit for executive-strategy-deck slides.
// Loads each slide in headless Chromium at 1280x720 and reports whether the
// .ppt-slide content fits the canvas (scrollHeight <= 720 + tolerance).
// Usage: NODE_PATH=/usr/local/lib/node_modules node geometry_check.js <file.html|dir> [...]
const fs = require('fs');
const path = require('path');

async function main() {
  let chromium;
  try { chromium = require('playwright').chromium; }
  catch (e) {
    console.error('playwright not available — geometry check skipped (optional gate)');
    process.exit(3);
  }
  const targets = [];
  for (const a of process.argv.slice(2)) {
    const p = path.resolve(a);
    if (fs.statSync(p).isDirectory()) targets.push(...fs.readdirSync(p).filter(f => f.endsWith('.html')).map(f => path.join(p, f)).sort());
    else if (p.endsWith('.html')) targets.push(p);
  }
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  let bad = 0;
  for (const t of targets) {
    await page.goto('file://' + t, { waitUntil: 'networkidle', timeout: 30000 }).catch(() => {});
    await page.waitForTimeout(400); // fonts/charts settle
    const m = await page.evaluate(() => {
      const s = document.querySelector('.ppt-slide');
      if (!s) return null;
      return { scrollH: s.scrollHeight, scrollW: s.scrollWidth };
    });
    const name = path.basename(t);
    if (!m) { console.log(`${name}: NO .ppt-slide ELEMENT`); bad++; continue; }
    const overflowY = m.scrollH - 720, overflowX = m.scrollW - 1280;
    const status = (overflowY > 2 || overflowX > 2) ? `OVERFLOW y+${overflowY}px x+${overflowX}px` : 'FITS';
    if (overflowY > 2 || overflowX > 2) bad++;
    console.log(`${name}: ${m.scrollW}x${m.scrollH}  ${status}`);
  }
  await browser.close();
  console.log(bad === 0 ? 'ALL SLIDES FIT THE 1280x720 CANVAS' : `${bad} slide(s) overflow`);
  process.exit(bad === 0 ? 0 : 1);
}
main();
