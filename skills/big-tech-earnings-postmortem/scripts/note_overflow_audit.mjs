#!/usr/bin/env node
/**
 * note_overflow_audit.mjs — render audit for single-file HTML research notes.
 *
 * The lite members of the big-tech research family deliver one scrolling,
 * self-contained HTML note (not a fixed 1280x720 slide deck). This is the
 * render gate for that shape, adapted from the flagship's overflow_audit.mjs:
 *
 *   A. Document overflow — documentElement.scrollWidth must not exceed the
 *      viewport width (+ tolerance): the note must never scroll sideways.
 *   B. Element spill — no visible element may extend past the viewport's
 *      content width (right edge or negative left). In a scrolling document
 *      an element beyond the width either forces horizontal scrolling or is
 *      clipped invisible by an overflow-hidden ancestor — both are defects.
 *   C. Clipped content — no overflow:hidden box may clip its own content
 *      (scrollHeight/scrollWidth beyond its client box). overflow:auto and
 *      overflow:scroll are legitimate (user-scrollable) and are not flagged.
 *
 * Decorative bleed elements are skipped only when marked with the family's
 * explicit conventions (no className guessing):
 *   data-bleed="intentional"   (this family's spec)
 *   data-decor                 (common deck convention)
 *   aria-hidden="true"         (standard non-content marker)
 *
 * Playwright is resolved via standard Node.js module resolution from the
 * current working directory and from this script's directory (no hardcoded
 * machine paths). Install it next to the note, in an ancestor directory, or
 * globally:  npm install playwright && npx playwright install chromium
 *
 * Usage:
 *   node note_overflow_audit.mjs --note ./research_note.html
 *   node note_overflow_audit.mjs --note ./note.html --width 1280 --tolerance 2 --shots /tmp
 *   node note_overflow_audit.mjs --selftest
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
  const args = { width: 1280, height: 900, tolerance: 2 };
  for (let i = 0; i < argv.length; i++) {
    const k = argv[i];
    if (k === '--note') args.note = argv[++i];
    else if (k === '--width') args.width = +argv[++i];
    else if (k === '--height') args.height = +argv[++i];
    else if (k === '--tolerance') args.tolerance = +argv[++i];
    else if (k === '--shots') args.shots = argv[++i];
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
  console.error('ERROR  playwright not found. Install it next to this script or the note:');
  console.error('       npm install playwright && npx playwright install chromium');
  process.exit(2);
}

const args = parseArgs(process.argv.slice(2));
if (args.help || (!args.note && !args.selftest)) {
  console.log('Usage: node note_overflow_audit.mjs --note <file.html> [--width 1280]\n' +
              '       [--height 900] [--tolerance 2] [--shots DIR]\n' +
              '       node note_overflow_audit.mjs --selftest');
  process.exit(args.note || args.selftest ? 0 : 2);
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
 * Audit one loaded page: returns { err?, docW, docSW, overs: [...] } where
 * overs mixes document-level and element-level and clipping findings.
 */
async function auditPage(page, W, TOL) {
  return page.evaluate(({ W, TOL }) => {
    const de = document.documentElement;
    const overs = [];
    // A. Document horizontal overflow: the note must not scroll sideways.
    if (de.scrollWidth > W + TOL) {
      overs.push(`document  scrollWidth=${de.scrollWidth} exceeds viewport ` +
                 `width ${W} (by ${de.scrollWidth - W}px)`);
    }
    const isBleed = el =>
      el.closest('[data-bleed="intentional"], [data-decor], [aria-hidden="true"]');
    // B. Element spill past the viewport content width.
    document.querySelectorAll('body *').forEach(el => {
      const cs = getComputedStyle(el);
      if (cs.display === 'none' || cs.visibility === 'hidden') return;
      if (isBleed(el)) return;
      const b = el.getBoundingClientRect();
      if (b.height <= 0 || b.width <= 0) return;
      if (b.right > W + TOL || b.left < -TOL) {
        const cls = String(el.className).split(/\s+/)[0] || '';
        overs.push(`${el.tagName.toLowerCase()}${cls ? '.' + cls : ''}` +
                   ` spills past viewport width (left=${Math.round(b.left)}, ` +
                   `right=${Math.round(b.right)} vs ${W})`);
      }
    });
    // C. overflow:hidden boxes clipping their own content (auto/scroll are
    // user-scrollable and legitimate; hidden clipping is invisible content).
    document.querySelectorAll('body *').forEach(el => {
      const cs = getComputedStyle(el);
      if (cs.display === 'none' || cs.visibility === 'hidden') return;
      if (isBleed(el)) return;
      const hiddenY = cs.overflowY === 'hidden' || cs.overflow === 'hidden';
      const hiddenX = cs.overflowX === 'hidden' || cs.overflow === 'hidden';
      const clipY = hiddenY && el.scrollHeight > el.clientHeight + TOL;
      const clipX = hiddenX && el.scrollWidth > el.clientWidth + TOL;
      if (clipY || clipX) {
        const cls = String(el.className).split(/\s+/)[0] || '';
        overs.push(`${el.tagName.toLowerCase()}${cls ? '.' + cls : ''}` +
                   ` clips its content (scroll=${el.scrollWidth}x${el.scrollHeight}` +
                   ` vs client=${el.clientWidth}x${el.clientHeight})`);
      }
    });
    return { docW: de.clientWidth, docSW: de.scrollWidth, overs: overs.slice(0, 8) };
  }, { W, TOL });
}

/**
 * Run the audit over files; returns { problems, lines } so --selftest can
 * assert on outcomes without parsing console output.
 */
async function runAudit(files, opts) {
  const browser = await launchBrowser();
  const page = await browser.newPage({ viewport: { width: opts.width, height: opts.height } });
  let problemNotes = 0;
  const lines = [];
  for (const f of files) {
    try {
      await page.goto('file://' + path.resolve(f), { waitUntil: 'networkidle', timeout: 30000 });
      try { await page.evaluate(() => document.fonts.ready); } catch { /* older browsers */ }
      await page.waitForTimeout(400); // let webfonts/layout settle
      const r = await auditPage(page, opts.width, opts.tolerance);
      const flag = r.overs.length ? 'OVERFLOW' : 'PASS';
      if (flag === 'OVERFLOW') problemNotes++;
      lines.push(`${flag}  ${path.basename(f)}  doc=${r.docSW}x${page.viewportSize().height}` +
                 (r.overs.length ? `  findings: ${r.overs.join(' | ')}` : ''));
      if (opts.shots) await page.screenshot({ path: path.join(opts.shots, path.basename(f).replace(/\.html$/, '.png')), fullPage: true });
    } catch (e) {
      lines.push(`ERR       ${path.basename(f)}  ${String(e.message).split('\n')[0]}`);
      problemNotes++;
    }
  }
  await browser.close();
  return { problems: problemNotes, lines };
}

async function selftest() {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'note-overflow-selftest-'));
  // Note 1: clean — flowing content, default body margins on purpose (the
  // audit measures against the viewport width, not absolute coordinates).
  fs.writeFileSync(path.join(tmp, 'note_01.html'),
    '<html><head><style>body{font-family:serif;margin:24px}' +
    '.stat{display:inline-block;width:300px;padding:12px}</style></head><body>' +
    '<h1>Clean note headline</h1><p>Some body text.</p>' +
    '<span class="stat">move −12.29%</span><span class="stat">cap −$482B</span>' +
    '</body></html>');
  // Note 2: a genuinely wide element (must flag: doc scrollWidth + spill) +
  // one data-bleed element beyond the right edge (must be skipped).
  fs.writeFileSync(path.join(tmp, 'note_02.html'),
    '<html><head><style>.wide{width:1400px;height:40px}' +
    '.ghost{position:absolute;left:1250px;top:0;width:200px;height:50px}' +
    '</style></head><body>' +
    '<div class="wide">spills past the right edge</div>' +
    '<div class="ghost" data-bleed="intentional">decorative</div>' +
    '</body></html>');
  // Note 3: fixed-height overflow:hidden box clipping taller text (must flag).
  fs.writeFileSync(path.join(tmp, 'note_03.html'),
    '<html><head><style>.callout{height:40px;overflow:hidden;width:400px}' +
    'p{margin:0;line-height:20px}</style></head><body>' +
    '<div class="callout"><p>line 1</p><p>line 2</p><p>line 3</p><p>line 4</p></div>' +
    '</body></html>');
  const { problems, lines } = await runAudit(
    [path.join(tmp, 'note_01.html'), path.join(tmp, 'note_02.html'),
     path.join(tmp, 'note_03.html')],
    { width: 1280, height: 900, tolerance: 2, shots: undefined });
  const n1Pass = lines.some(l => l.startsWith('PASS  note_01.html'));
  const n2Flagged = lines.some(l => l.startsWith('OVERFLOW  note_02.html') && l.includes('div.wide'));
  const bleedSkipped = !lines.some(l => l.includes('div.ghost'));
  const n3Flagged = lines.some(l => l.startsWith('OVERFLOW  note_03.html') && l.includes('div.callout') && l.includes('clips its content'));
  const ok = problems === 2 && n1Pass && n2Flagged && bleedSkipped && n3Flagged;
  for (const l of lines) console.log(l);
  console.log('='.repeat(60));
  console.log('SELFTEST:', ok ? 'PASS' : 'FAIL',
    `(clean note ${n1Pass ? 'passed' : 'FAILED'}; wide element ${n2Flagged ? 'flagged' : 'MISSED'};` +
    ` bleed-marked element ${bleedSkipped ? 'skipped' : 'WRONGLY FLAGGED'};` +
    ` clipped box ${n3Flagged ? 'flagged' : 'MISSED'})`);
  fs.rmSync(tmp, { recursive: true, force: true });
  process.exit(ok ? 0 : 1);
}

if (args.selftest) {
  await selftest();
}

if (!fs.existsSync(args.note)) {
  console.error(`ERROR  note file not found: ${args.note}`);
  process.exit(2);
}
if (args.shots) fs.mkdirSync(args.shots, { recursive: true });

const { problems, lines } = await runAudit([args.note], args);
for (const l of lines) console.log(l);
console.log('='.repeat(60));
console.log('LAYOUT AUDIT:', problems === 0 ? 'CLEAN' : 'note needs fixes');
process.exit(problems === 0 ? 0 : 1);
