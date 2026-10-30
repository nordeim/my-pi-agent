#!/usr/bin/env node
/**
 * overflow_audit.mjs — render audit for stock-RCA slide decks.
 *
 * Opens every slide_NN.html in a headless Chromium at the deck canvas size
 * (default 1280x720) and flags any visible element extending past the canvas
 * by more than --tolerance px (default 2). Decorative bleed elements are
 * skipped when marked with any of the recognized conventions:
 *   data-bleed="intentional"   (this skill's spec)
 *   data-decor                 (common deck convention)
 *   aria-hidden="true"         (standard non-content marker)
 *
 * Usage:
 *   node overflow_audit.mjs --dir ./slides
 *   node overflow_audit.mjs --dir ./slides --shots /tmp/shots --width 1280 --height 720
 *
 * Exit codes: 0 clean, 1 overflow/errors found, 2 environment error.
 */
import { createRequire } from 'node:module';
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';
import process from 'node:process';

function parseArgs(argv) {
  const args = { width: 1280, height: 720, tolerance: 2, pattern: /^slide_\d+\.html$/ };
  for (let i = 0; i < argv.length; i++) {
    const k = argv[i];
    if (k === '--dir') args.dir = argv[++i];
    else if (k === '--width') args.width = +argv[++i];
    else if (k === '--height') args.height = +argv[++i];
    else if (k === '--tolerance') args.tolerance = +argv[++i];
    else if (k === '--shots') args.shots = argv[++i];
    else if (k === '--selector') args.selector = argv[++i];
    else if (k === '--pattern') args.pattern = new RegExp(argv[++i]);
    else if (k === '--help' || k === '-h') args.help = true;
  }
  return args;
}

function loadPlaywright() {
  const bases = [
    process.cwd(),
    path.dirname(fileURLToPath(import.meta.url)),
    '/home/z/my-project',
    '/home/z/my-project/scripts',
  ];
  for (const base of bases) {
    try {
      return createRequire(path.join(base, 'noop.js'))('playwright');
    } catch { /* try next base */ }
  }
  console.error('ERROR  playwright not found. Install it next to this script or the deck:');
  console.error('       npm install playwright && npx playwright install chromium');
  process.exit(2);
}

const args = parseArgs(process.argv.slice(2));
if (args.help || !args.dir) {
  console.log('Usage: node overflow_audit.mjs --dir ./slides [--width 1280 --height 720]\n' +
              '       [--tolerance 2] [--selector .slide] [--shots DIR] [--pattern "^slide_\\d+\\.html$"]');
  process.exit(args.dir ? 0 : 2);
}
if (!fs.existsSync(args.dir)) {
  console.error(`ERROR  slides dir not found: ${args.dir}`);
  process.exit(2);
}

const { chromium } = loadPlaywright();
const files = fs.readdirSync(args.dir).filter(f => args.pattern.test(f)).sort();
if (!files.length) {
  console.error(`ERROR  no files matching ${args.pattern} in ${args.dir}`);
  process.exit(2);
}
if (args.shots) fs.mkdirSync(args.shots, { recursive: true });

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: args.width, height: args.height } });
let problems = 0;

for (const f of files) {
  try {
    await page.goto('file://' + path.resolve(args.dir, f), { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(400); // let webfonts settle
    const r = await page.evaluate(({ W, H, TOL, selector }) => {
      const slide = document.querySelector(selector || '.slide');
      if (!slide) return { err: `no "${selector || '.slide'}" element` };
      const overs = [];
      slide.querySelectorAll('*').forEach(el => {
        const cs = getComputedStyle(el);
        if (cs.display === 'none' || cs.visibility === 'hidden') return;
        if (el.closest('[data-bleed="intentional"], [data-decor], [aria-hidden="true"]') ||
            /bleed/.test(String(el.className))) return;
        const b = el.getBoundingClientRect();
        if (b.height > 0 && b.width > 0 &&
            (b.bottom > H + TOL || b.right > W + TOL || b.top < -TOL || b.left < -TOL)) {
          const cls = String(el.className).split(/\s+/)[0] || '';
          overs.push(`${el.tagName.toLowerCase()}${cls ? '.' + cls : ''}` +
                     ` bottom=${Math.round(b.bottom)} right=${Math.round(b.right)}`);
        }
      });
      // Note: .slide is overflow:hidden, so scrollWidth/Height mostly mirrors
      // intentional decorative bleeds — the per-element scan above is the real gate.
      return { sw: slide.scrollWidth, sh: slide.scrollHeight, overs: overs.slice(0, 5) };
    }, { W: args.width, H: args.height, TOL: args.tolerance, selector: args.selector });

    if (r.err) {
      console.log(`ERR       ${f}  ${r.err}`);
      problems++;
      continue;
    }
    const flag = r.overs.length ? 'OVERFLOW' : 'PASS';
    if (flag === 'OVERFLOW') problems++;
    console.log(`${flag}  ${f}  scroll=${r.sw}x${r.sh}` +
                (r.overs.length ? `  clipped: ${r.overs.join(' | ')}` : ''));
    if (args.shots) await page.screenshot({ path: path.join(args.shots, f.replace(/\.html$/, '.png')) });
  } catch (e) {
    console.log(`ERR       ${f}  ${String(e.message).split('\n')[0]}`);
    problems++;
  }
}

await browser.close();
console.log('='.repeat(60));
console.log('LAYOUT AUDIT:', problems === 0 ? 'CLEAN' : `${problems} slide(s) need fixes`);
process.exit(problems === 0 ? 0 : 1);
