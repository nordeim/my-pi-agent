#!/usr/bin/env node
/**
 * overflow_audit.mjs — render audit for stock-RCA slide decks.
 *
 * Opens every slide_NN.html in a headless Chromium at the deck canvas size
 * (default 1280x720) and flags any visible element extending past the slide
 * canvas by more than --tolerance px (default 2). Measurement is relative to
 * the `.slide` element's own box (not the browser viewport), so default body
 * margins cannot cause false positives and elements beyond the slide's right
 * or bottom edge are caught even when they remain inside the viewport.
 * Decorative bleed elements are skipped only when marked with one of the
 * explicit conventions (no className guessing):
 *   data-bleed="intentional"   (this skill's spec)
 *   data-decor                 (common deck convention)
 *   aria-hidden="true"         (standard non-content marker)
 *
 * Playwright is resolved via standard Node.js module resolution from the
 * current working directory and from this script's directory (no hardcoded
 * machine paths). Install it next to the deck, in an ancestor directory, or
 * globally:  npm install playwright && npx playwright install chromium
 *
 * Usage:
 *   node overflow_audit.mjs --dir ./slides
 *   node overflow_audit.mjs --dir ./slides --shots /tmp/shots --width 1280 --height 720
 *   node overflow_audit.mjs --selftest
 *
 * Exit codes: 0 clean, 1 overflow/errors found, 2 environment/usage error.
 */
import { createRequire } from 'node:module';
import path from 'node:path';
import fs from 'node:fs';
import os from 'node:os';
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
    else if (k === '--selftest') args.selftest = true;
    else if (k === '--help' || k === '-h') args.help = true;
  }
  return args;
}

function loadPlaywright() {
  // Standard Node.js module resolution: cwd and the script's own directory
  // (both walk up the ancestor tree looking for node_modules).
  const bases = [
    process.cwd(),
    path.dirname(fileURLToPath(import.meta.url)),
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
if (args.help || (!args.dir && !args.selftest)) {
  console.log('Usage: node overflow_audit.mjs --dir ./slides [--width 1280 --height 720]\n' +
              '       [--tolerance 2] [--selector .slide] [--shots DIR] [--pattern "^slide_\\d+\\.html$"]\n' +
              '       node overflow_audit.mjs --selftest');
  process.exit(args.dir || args.selftest ? 0 : 2);
}

const { chromium } = loadPlaywright();

/** Launch with the documented env-error contract: a browser binary that cannot
 *  launch (installed module, missing chromium download) is exit 2 — an
 *  environment error — not an unhandled crash (exit 1). Round 5: the
 *  exit-code contract in the header is load-bearing; tests env-skip on 2. */
async function launchBrowser() {
  try {
    return await chromium.launch();
  } catch (e) {
    console.error('ERROR  cannot launch Chromium — ' + String(e.message).split('\n')[0]);
    console.error('       Install the browser binary: npx playwright install chromium');
    console.error('       (documented environment error — exiting 2 per the exit-code contract)');
    process.exit(2);
  }
}

/**
 * Audit one loaded page: slide-origin-relative overflow scan.
 * Returns { err?, sw, sh, overs: [...] }.
 */
async function auditPage(page, W, H, TOL, selector) {
  return page.evaluate(({ W, H, TOL, selector }) => {
    const slide = document.querySelector(selector || '.slide');
    if (!slide) return { err: `no "${selector || '.slide'}" element` };
    const sb = slide.getBoundingClientRect();
    const overs = [];
    slide.querySelectorAll('*').forEach(el => {
      const cs = getComputedStyle(el);
      if (cs.display === 'none' || cs.visibility === 'hidden') return;
      if (el.closest('[data-bleed="intentional"], [data-decor], [aria-hidden="true"]')) return;
      const b = el.getBoundingClientRect();
      if (b.height <= 0 || b.width <= 0) return;
      // Coordinates relative to the slide's own box, so body margins and
      // page furniture cannot fake either a pass or a failure.
      const rel = {
        left: b.left - sb.left, right: b.right - sb.left,
        top: b.top - sb.top, bottom: b.bottom - sb.top,
      };
      if (rel.bottom > H + TOL || rel.right > W + TOL || rel.top < -TOL || rel.left < -TOL) {
        const cls = String(el.className).split(/\s+/)[0] || '';
        overs.push(`${el.tagName.toLowerCase()}${cls ? '.' + cls : ''}` +
                   ` bottom=${Math.round(rel.bottom)} right=${Math.round(rel.right)}`);
      }
    });
    return { sw: slide.scrollWidth, sh: slide.scrollHeight, overs: overs.slice(0, 5) };
  }, { W, H, TOL, selector });
}

/**
 * Run the audit over files; returns { problems, lines } so --selftest can
 * assert on outcomes without parsing console output.
 */
async function runAudit(files, dir, opts) {
  const browser = await launchBrowser();
  const page = await browser.newPage({ viewport: { width: opts.width, height: opts.height } });
  let problemSlides = 0;
  const lines = [];
  for (const f of files) {
    try {
      await page.goto('file://' + path.resolve(dir, f), { waitUntil: 'networkidle', timeout: 30000 });
      try { await page.evaluate(() => document.fonts.ready); } catch { /* older browsers */ }
      await page.waitForTimeout(400); // let webfonts/layout settle
      const r = await auditPage(page, opts.width, opts.height, opts.tolerance, opts.selector);
      if (r.err) {
        lines.push(`ERR       ${f}  ${r.err}`);
        problemSlides++;
        continue;
      }
      const flag = r.overs.length ? 'OVERFLOW' : 'PASS';
      if (flag === 'OVERFLOW') problemSlides++;
      lines.push(`${flag}  ${f}  scroll=${r.sw}x${r.sh}` +
                 (r.overs.length ? `  clipped: ${r.overs.join(' | ')}` : ''));
      if (opts.shots) await page.screenshot({ path: path.join(opts.shots, f.replace(/\.html$/, '.png')) });
    } catch (e) {
      lines.push(`ERR       ${f}  ${String(e.message).split('\n')[0]}`);
      problemSlides++;
    }
  }
  await browser.close();
  return { problems: problemSlides, lines };
}

async function selftest() {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'overflow-selftest-'));
  // Slide 1: clean — one in-bounds element. Body has a default margin on
  // purpose: measurement is slide-relative, so it must still PASS.
  fs.writeFileSync(path.join(tmp, 'slide_01.html'),
    '<html><head><style>.slide{position:relative;width:1280px;height:720px;' +
    'overflow:hidden;background:#0A1628;color:#F2EDE4}' +
    'h1{font-size:40px;margin:40px}</style></head><body>' +
    '<div class="slide"><h1>Clean headline</h1></body></html>');
  // Slide 2: one genuinely overflowing element (must flag) + one marked
  // data-bleed="intentional" overflowing element (must be skipped).
  fs.writeFileSync(path.join(tmp, 'slide_02.html'),
    '<html><head><style>.slide{position:relative;width:1280px;height:720px;overflow:hidden}' +
    '.wide{position:absolute;left:0;top:0;width:1400px;height:40px}' +
    '.ghost{position:absolute;left:1200px;top:600px;width:200px;height:200px}' +
    '</style></head><body><div class="slide">' +
    '<div class="wide">spills past the right edge</div>' +
    '<div class="ghost" data-bleed="intentional">decorative</div>' +
    '</div></body></html>');
  const { problems, lines } = await runAudit(
    ['slide_01.html', 'slide_02.html'], tmp,
    { width: 1280, height: 720, tolerance: 2, selector: undefined, shots: undefined });
  const slide1Pass = lines.some(l => l.startsWith('PASS  slide_01.html'));
  const slide2Flagged = lines.some(l => l.startsWith('OVERFLOW  slide_02.html') && l.includes('div.wide'));
  const bleedSkipped = !lines.some(l => l.includes('div.ghost'));
  const ok = problems === 1 && slide1Pass && slide2Flagged && bleedSkipped;
  for (const l of lines) console.log(l);
  console.log('='.repeat(60));
  console.log('SELFTEST:', ok ? 'PASS' : 'FAIL',
    `(clean slide ${slide1Pass ? 'passed' : 'FAILED'}; overflow ${slide2Flagged ? 'flagged' : 'MISSED'};` +
    ` bleed-marked element ${bleedSkipped ? 'skipped' : 'WRONGLY FLAGGED'})`);
  fs.rmSync(tmp, { recursive: true, force: true });
  process.exit(ok ? 0 : 1);
}

if (args.selftest) {
  await selftest();
}

if (!fs.existsSync(args.dir)) {
  console.error(`ERROR  slides dir not found: ${args.dir}`);
  process.exit(2);
}
const files = fs.readdirSync(args.dir).filter(f => args.pattern.test(f)).sort();
if (!files.length) {
  console.error(`ERROR  no files matching ${args.pattern} in ${args.dir}`);
  process.exit(2);
}
if (args.shots) fs.mkdirSync(args.shots, { recursive: true });

const { problems, lines } = await runAudit(files, args.dir, args);
for (const l of lines) console.log(l);
console.log('='.repeat(60));
console.log('LAYOUT AUDIT:', problems === 0 ? 'CLEAN' : `${problems} slide(s) need fixes`);
process.exit(problems === 0 ? 0 : 1);
