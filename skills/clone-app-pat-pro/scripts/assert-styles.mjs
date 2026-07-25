#!/usr/bin/env node
// assert-styles.mjs — computed-style assertion gate (NO browser; pure comparison).
//
// The QA agent opens the localhost clone with the Claude Chrome extension and reads
// the clone's computed styles via `javascript_tool` (getComputedStyle on each asserted
// selector), then writes them as JSON. THIS script just compares that JSON to the
// design tokens/assertions and writes the verdict. No browser here at all — pure comparison.
//
// Usage:
//   node assert-styles.mjs --assertions <03-design-spec/assertions.json> \
//        --clone-styles <clone-styles.json> --out <metrics.json>
//
//   assertions.json   : [{ "selector": "...", "prop": "...", "expected": "..." }]
//   clone-styles.json : { "<selector>": { "<prop>": "<actual computed value>" } }
//                       (produced by the agent via javascript_tool getComputedStyle)
//
// PASS = failed === 0.

import fs from "node:fs";

const args = Object.fromEntries(
  process.argv.slice(2).reduce((a, v, i, arr) => (v.startsWith("--") ? [...a, [v.slice(2), arr[i + 1]]] : a), [])
);
const assertionsPath = args.assertions;
const clonePath = args["clone-styles"];
const outPath = args.out;
if (!assertionsPath || !clonePath) {
  console.error("usage: assert-styles.mjs --assertions <a.json> --clone-styles <c.json> [--out <metrics.json>]");
  process.exit(2);
}

let assertions = [], clone = {};
try { assertions = JSON.parse(fs.readFileSync(assertionsPath)); } catch (e) { console.error("can't read assertions:", e.message); process.exit(2); }
try { clone = JSON.parse(fs.readFileSync(clonePath)); } catch (e) { console.error("can't read clone-styles:", e.message); process.exit(2); }

const norm = (s) => String(s ?? "").replace(/\s+/g, " ").trim().toLowerCase();
const numeric = (s) => { const m = String(s).match(/-?\d*\.?\d+/); return m ? parseFloat(m[0]) : NaN; };

const failures = [];
let passed = 0;
for (const a of assertions) {
  const actual = (clone[a.selector] || {})[a.prop];
  const exp = a.expected;
  let ok;
  const en = numeric(exp), an = numeric(actual);
  if (!isNaN(en) && !isNaN(an) && /px|em|rem|%|^\s*-?\d/.test(String(exp))) {
    ok = Math.abs(en - an) <= (String(exp).includes("em") ? 0.01 : 1);
  } else {
    ok = norm(exp) === norm(actual);
  }
  if (ok) passed++; else failures.push({ selector: a.selector, prop: a.prop, expected: exp, actual: actual ?? null });
}

const block = { total: assertions.length, passed, failed: failures.length, failures };

if (outPath) {
  let metrics = {};
  if (fs.existsSync(outPath)) { try { metrics = JSON.parse(fs.readFileSync(outPath)); } catch {} }
  metrics.style_assertions = block;
  fs.writeFileSync(outPath, JSON.stringify(metrics, null, 2));
}
console.log(`style assertions: ${passed}/${assertions.length} passed, ${failures.length} failed`);
process.exit(failures.length === 0 ? 0 : 1);
