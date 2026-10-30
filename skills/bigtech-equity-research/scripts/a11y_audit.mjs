#!/usr/bin/env node
/**
 * a11y_audit.mjs — accessibility gate for the big-tech research family's HTML deliverables.
 *
 * The note templates claim WCAG-AA ("WCAG-AA contrast. Print-friendly", report-structure
 * §rendering rules; the flagship's report-design tokens claim WCAG 2.2 AA), but the render
 * gate only checks overflow/clipping — a claimed-but-unenforced quality bar (comparative
 * reports 6/7, finding M-5/M-6 "render gate checks layout overflow but not accessibility
 * conformance"). This gate closes the claim/enforcement gap with the checks that matter
 * for a static, self-contained research artifact:
 *
 *   A. Language — <html lang> present and non-empty.
 *   B. Heading order — h1..h6 levels never skip downward (h2 -> h4), and the document
 *      contains at least one h1.
 *   C. Image alt — every <img> carries a non-empty alt (empty alt allowed only on
 *      elements marked decorative via data-decor / aria-hidden="true").
 *   D. Text contrast — every visible text node's computed color vs its effective
 *      background (walking up ancestors until an opaque background) must clear WCAG 2.2
 *      AA: 4.5:1 normal, 3:1 for large text (>= 24px, or >= 18.66px bold).
 *
 * Not attempted here: full axe-core parity (focus order, ARIA semantics, keyboard
 * operability) — those belong to interactive documents; these notes are static print
 * artifacts. This gate enforces exactly what the family's templates claim.
 *
 * Playwright is resolved via standard Node.js module resolution from the current working
 * directory and from this script's directory (no hardcoded machine paths). Install with:
 *   npm install playwright && npx playwright install chromium
 *
 * Usage:
 *   node a11y_audit.mjs --note ./research_note.html
 *   node a11y_audit.mjs --dir ./slides            (every *.html in the directory)
 *   node a11y_audit.mjs --selftest
 *
 * Exit codes: 0 clean, 1 violations found, 2 environment/usage error.
 */
import { createRequire } from 'node:module';
import path from 'node:path';
import fs from 'node:fs';
import os from 'node:os';
import { fileURLToPath } from 'node:url';
import process from 'node:process';

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    const k = argv[i];
    if (k === '--note') args.note = argv[++i];
    else if (k === '--dir') args.dir = argv[++i];
    else if (k === '--selftest') args.selftest = true;
    else if (k === '--help' || k === '-h') args.help = true;
  }
  return args;
}

function loadPlaywright() {
  const bases = [process.cwd(), path.dirname(fileURLToPath(import.meta.url))];
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
if (args.help || (!args.note && !args.dir && !args.selftest)) {
  console.log('Usage: node a11y_audit.mjs --note <file.html>\n' +
              '       node a11y_audit.mjs --dir <slides-dir>\n' +
              '       node a11y_audit.mjs --selftest');
  process.exit(args.note || args.dir || args.selftest ? 0 : 2);
}

const { chromium } = loadPlaywright();

/** Audit one loaded page; returns a list of violation strings (empty = clean). */
async function auditPage(page) {
  return page.evaluate(() => {
    const problems = [];

    // A. Document language.
    const lang = document.documentElement.getAttribute('lang');
    if (!lang || !lang.trim()) problems.push('A11Y-LANG    <html> has no lang attribute');

    // B. Heading order: levels may not skip downward; an h1 must exist.
    const headings = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')]
      .filter(h => h.textContent.trim().length > 0);
    if (headings.length && !headings.some(h => h.tagName === 'H1')) {
      problems.push('A11Y-HEADING document has headings but no h1');
    }
    let prev = 0;
    for (const h of headings) {
      const level = +h.tagName[1];
      if (prev && level > prev + 1) {
        problems.push(`A11Y-HEADING heading level skips h${prev} -> h${level} ` +
                      `("${h.textContent.trim().slice(0, 40)}")`);
      }
      prev = level;
    }

    // C. Image alt text (decorative images marked data-decor / aria-hidden are exempt).
    document.querySelectorAll('img').forEach(img => {
      if (img.closest('[data-decor], [aria-hidden="true"]')) return;
      const alt = (img.getAttribute('alt') || '').trim();
      if (!alt) problems.push(`A11Y-IMG      <img> without alt text (src="${(img.getAttribute('src') || '').slice(0, 40)}")`);
    });

    // D. Text contrast (WCAG 2.2 AA: 4.5:1 normal, 3:1 large).
    const parseRGB = s => {
      const m = s.match(/rgba?\((\d+)[,\s]+(\d+)[,\s]+(\d+)(?:[,\s/]+([\d.]+))?\)/);
      if (!m) return null;
      return [ +m[1], +m[2], +m[3], m[4] === undefined ? 1 : +m[4] ];
    };
    const blend = (fg, bg) => fg.map((c, i) => i < 3 ? c * fg[3] + bg[i] * (1 - fg[3]) : 1);
    const lum = ([r, g, b]) => {
      const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; };
      return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
    };
    const ratio = (a, b) => {
      const [l1, l2] = [lum(a), lum(b)].sort((x, y) => y - x);
      return (l1 + 0.05) / (l2 + 0.05);
    };
    const effectiveBg = el => {
      let node = el;
      while (node && node !== document.documentElement) {
        const c = parseRGB(getComputedStyle(node).backgroundColor);
        if (c && c[3] >= 0.95) return c;
        node = node.parentElement;
      }
      const root = parseRGB(getComputedStyle(document.documentElement).backgroundColor);
      return root && root[3] > 0 ? root : [255, 255, 255, 1]; // assume white when fully transparent
    };
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    const seen = new Set();
    while (walker.nextNode()) {
      const t = walker.currentNode;
      if (!t.textContent.trim()) continue;
      const el = t.parentElement;
      if (!el || seen.has(el)) continue;
      seen.add(el);
      if (el.closest('[data-decor], [aria-hidden="true"], [data-bleed]')) continue;
      const cs = getComputedStyle(el);
      if (cs.display === 'none' || cs.visibility === 'hidden') continue;
      const fg = parseRGB(cs.color);
      if (!fg) continue;
      const bg = effectiveBg(el);
      const eff = fg[3] < 1 ? blend(fg, bg) : fg;
      const size = parseFloat(cs.fontSize);
      const bold = parseInt(cs.fontWeight, 10) >= 700;
      const large = size >= 24 || (size >= 18.66 && bold);
      const need = large ? 3 : 4.5;
      const r = ratio(eff, bg);
      if (r < need) {
        problems.push(`A11Y-CONTRAST ${r.toFixed(2)}:1 < ${need}:1 ` +
                      `("${t.textContent.trim().slice(0, 30)}" ${cs.color} on bg)`);
      }
    }
    return problems.slice(0, 12);
  });
}

/** Run over files; returns { problems: nBadFiles, lines } so --selftest can assert. */
async function runAudit(files) {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  let bad = 0;
  const lines = [];
  for (const f of files) {
    try {
      await page.goto('file://' + path.resolve(f), { waitUntil: 'networkidle', timeout: 30000 });
      try { await page.evaluate(() => document.fonts.ready); } catch { /* older browsers */ }
      await page.waitForTimeout(300); // let layout settle
      const problems = await auditPage(page);
      if (problems.length) bad++;
      lines.push(`${problems.length ? 'A11Y-FAIL' : 'PASS'}  ${path.basename(f)}` +
                 (problems.length ? `  findings: ${problems.join(' | ')}` : ''));
    } catch (e) {
      lines.push(`ERR       ${path.basename(f)}  ${String(e.message).split('\n')[0]}`);
      bad++;
    }
  }
  await browser.close();
  return { problems: bad, lines };
}

async function selftest() {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'a11y-selftest-'));
  // Clean: lang, one h1 then h2, alt text, black-on-white.
  fs.writeFileSync(path.join(tmp, 'clean.html'),
    '<html lang="en"><head><style>body{background:#fff;color:#111}' +
    'h1{color:#111}h2{color:#111}</style></head><body>' +
    '<h1>Clean note</h1><h2>Section</h2><p>Body text at 4.5:1+.</p>' +
    '<img alt="GOOG price ladder chart" src="data:image/gif;base64,R0lGODlhAQABAAAAACw=">' +
    '</body></html>');
  // Violations: no lang, h1 -> h3 skip, missing alt, low-contrast gray text.
  fs.writeFileSync(path.join(tmp, 'bad.html'),
    '<html><head><style>body{background:#fff;color:#111}' +
    'h1{color:#111}h3{color:#111}.faint{color:#aaa}</style></head><body>' +
    '<h1>Bad note</h1><h3>Skipped level</h3>' +
    '<p class="faint">low contrast body text</p>' +
    '<img src="data:image/gif;base64,R0lGODlhAQABAAAAACw=">' +
    '</body></html>');
  // Decorative image without alt must be exempt; large text at ~3.5:1 passes
  // (large-text rule: >= 24px needs only 3:1). bad.html's #aaa at body size
  // is ~2.3:1 and fails the 4.5:1 normal-text bar.
  fs.writeFileSync(path.join(tmp, 'decor.html'),
    '<html lang="en"><head><style>body{background:#111;color:#eee}' +
    'h1{color:#eee;font-size:36px}.mid{color:#6a6a6a;font-size:28px}</style></head><body>' +
    '<h1>Dark note</h1><p class="mid">large text at roughly 3.5:1</p>' +
    '<img src="data:image/gif;base64,R0lGODlhAQABAAAAACw=" data-decor>' +
    '</body></html>');
  const { problems, lines } = await runAudit(
    [path.join(tmp, 'clean.html'), path.join(tmp, 'bad.html'), path.join(tmp, 'decor.html')]);
  const cleanPass = lines.some(l => l.startsWith('PASS  clean.html'));
  const badFlagged = lines.some(l => l.startsWith('A11Y-FAIL  bad.html') &&
                                     l.includes('A11Y-LANG') && l.includes('A11Y-HEADING') &&
                                     l.includes('A11Y-IMG') && l.includes('A11Y-CONTRAST'));
  const decorPass = lines.some(l => l.startsWith('PASS  decor.html'));
  const ok = problems === 1 && cleanPass && badFlagged && decorPass;
  for (const l of lines) console.log(l);
  console.log('='.repeat(60));
  console.log('SELFTEST:', ok ? 'PASS' : 'FAIL',
    `(clean ${cleanPass ? 'passed' : 'FAILED'}; violations ${badFlagged ? 'flagged' : 'MISSED'};` +
    ` decorative/large-text exemptions ${decorPass ? 'respected' : 'WRONGLY FLAGGED'})`);
  fs.rmSync(tmp, { recursive: true, force: true });
  process.exit(ok ? 0 : 1);
}

if (args.selftest) {
  await selftest();
}

let files = [];
if (args.note) {
  if (!fs.existsSync(args.note)) {
    console.error(`ERROR  note file not found: ${args.note}`);
    process.exit(2);
  }
  files = [args.note];
} else if (args.dir) {
  if (!fs.existsSync(args.dir)) {
    console.error(`ERROR  directory not found: ${args.dir}`);
    process.exit(2);
  }
  files = fs.readdirSync(args.dir).filter(f => f.endsWith('.html'))
    .map(f => path.join(args.dir, f));
  if (!files.length) {
    console.error(`ERROR  no .html files in ${args.dir}`);
    process.exit(2);
  }
}

const { problems, lines } = await runAudit(files);
for (const l of lines) console.log(l);
console.log('='.repeat(60));
console.log('A11Y AUDIT:', problems === 0 ? 'CLEAN' : `${problems} file(s) with violations`);
process.exit(problems === 0 ? 0 : 1);
