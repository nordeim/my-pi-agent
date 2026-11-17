// probe_depth.js — one-off diagnostic: report the deepest-reaching elements in a slide.
const path = require('path');
(async () => {
  const { chromium } = require('playwright');
  const file = path.resolve(process.argv[2]);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  await page.goto('file://' + file, { waitUntil: 'networkidle', timeout: 30000 }).catch(() => {});
  await page.waitForTimeout(400);
  const rows = await page.evaluate(() => {
    const out = [];
    for (const el of document.querySelectorAll('.ppt-slide *')) {
      const r = el.getBoundingClientRect();
      if (r.height === 0) continue;
      out.push({ bottom: Math.round(r.bottom), h: Math.round(r.height), tag: el.tagName.toLowerCase(),
                 cls: (el.getAttribute('class') || '').slice(0, 70), text: (el.textContent || '').trim().slice(0, 40) });
    }
    out.sort((a, b) => b.bottom - a.bottom);
    return out.slice(0, 8);
  });
  console.log(path.basename(file));
  for (const r of rows) console.log(`  bottom=${r.bottom}  <${r.tag} .${r.cls}>  ${r.text.replace(/\s+/g, ' ')}`);
  await browser.close();
})();
