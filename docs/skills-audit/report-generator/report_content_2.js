// Audit report content — Part 2: Skill assessments, comparison, scorecard, ledger, roadmap, appendices.
"use strict";

const blocks = [];

// ============ 4. SKILL-BY-SKILL ASSESSMENT ============
blocks.push({ h1: "4. Skill-by-Skill Assessment" });

blocks.push({ h2: "4.1 analyzing-us-bigtech-stocks — RCA deck with audit gates (rubric 4.45 / 5)" });
blocks.push({ p: "Skill 1 is an eleven-phase pipeline (Phases 0–10) that turns a price question into a 12–16-page HTML investment-committee deck on a fixed 1280×720 canvas, styled by a documented \u201cMidnight IC\u201d design system (deep navy, ivory serif, gold accents, monospaced numerals — explicitly referenced to Goldman Sachs / BlackRock IC-memo aesthetics). Its spine is a JSON fact base governed by a written schema: every number carries an ID, category, unit, as-of period, source tier, source name, URL, retrieval timestamp, confidence label, cross-checks, and the hypothesis IDs it evidences. Phases 3–4 force a hypothesis tree of 5–8 competing explanations with falsifiable predictions and at least one explicitly EXCLUDED verdict; Phase 6 mandates the GAAP-to-adjusted bridge with one-off inventory; Phase 7 separates amplifiers (depth) from triggers (direction) and requires a sourced counter-case page; Phase 8 bans price targets; Phase 10 runs the two executable audits before delivery." });
blocks.push({ p: "**Verified strengths.** The source-tier table is the most institutional element in the repository: T3 aggregators are barred from originating fundamental claims outright — a rule human analysts routinely break. The T+1-close reaction doctrine (\u201cthe after-hours print is thin; the close is what clears real size\u201d) preempts the most common post-earnings analytical error. The transcript protocol requires verbatim capture of one-off explanations with hedging language intact, and its worked illustration (a $5.2B EC fine inside FCF converting a \u201ccash-flow collapse\u201d into an in-line quarter ex-item) is exactly the craft a senior analyst would teach. The fact base is append-only during an engagement, conflicts are recorded rather than silently resolved, rankings must be sourced or dropped, and the data cutoff is stamped on the cover with an explicit refresh duty. The external verification results were strong: GOOG close $282.32 (−12.29%, −$39.57) confirmed exactly by Bloomberg; FCF −$9.1B and TTM FCF $19.7B confirmed in the earnings-call transcript language; adjusted EPS $2.67 and net income path confirmed by Reuters; OCF $42.3B, Cloud $30.7B (+103%), PCE 3.6% from 3.4%, and the \u201c$482B — worst day ever, second-largest wipeout behind Nvidia Jan 2025\u201d framing all confirmed via Yahoo Finance, Bloomberg and WSJ coverage." });
blocks.push({ p: "**Headline gaps.** The numeric audit gate is evadable by digit-substring coincidence (H-4 — verified by execution); the render audit assumes viewport-equals-slide-origin without mandating a body reset (M-1 — verified by probe); the GOOGL cross-class figure conflicts with skill 3's and with accessible public prints (H-1); the placeholder scan matches raw HTML (L-4); and the Playwright prerequisite is undocumented (M-7). fact_base_audit.py itself is genuinely good engineering: exit codes 0/1/2, a JSON report option, an asserting self-test, and a reverse-check that reports slide numbers absent from the fact base as review candidates rather than automatic failures — a smart severity calibration most homegrown QA lacks." });
blocks.push({ p: "**Assessment.** Conditional pass at the stated bar. Methodology, sourcing discipline and quality-assurance design are institutional; the gaps are fixable control weaknesses, and the four P0 items in Section 7 close most of the distance." });

blocks.push({ h2: "4.2 big-tech-earnings-postmortem — single-file methodology (rubric 2.85 / 5)" });
blocks.push({ p: "Skill 2 is a nine-step post-earnings workflow in one 283-line file: pin the event numerically (session, point and percentage move, market-cap change, historical rank verified in ≥2 sources, pre-event positioning, sector/session context isolating abnormal return); build a scorecard against consensus across top line, profitability, cash generation, guidance and balance sheet; rank root causes on two axes — durability (mechanical/temporary vs structural) and evidentiary basis (disclosed / inferred / assumed); establish peer and industry context; collect sell-side actions within 48 hours with faithful rationale attribution; build a risk/catalyst matrix whose every row carries an observable, dated trigger; synthesize as a falsifiable thesis with confidence tags; assemble a verification ledger of 10–15 load-bearing claims; and render a restrained, data-dense HTML deliverable." });
blocks.push({ p: "**Verified strengths.** The two-axis driver classification is the best single analytical idea across the three skills — durability × evidentiary basis is precisely how a PM triages driver tables, and the skill operationalizes it. The failure-mode catalog reads like desk experience: \u201cflat attribution\u201d (listing causes without ranking), the \u201caccounting-noise hand-wave\u201d (dismissing a GAAP miss without checking whether dilution or a cash fine sits inside it), narrative-first reasoning, peer omission, false precision, \u201csell-side ventriloquism\u201d (attributing a rationale an analyst never stated) and confidence inflation. The metric-emphasis table per company type is factually sound (capex/OCF and cloud backlog for hyperscalers; China exposure and services attach for Apple; backlog and gross margin for Nvidia; deliveries and auto margin ex-credits for Tesla), and the cash-flow-first ranking heuristic for big-tech moves is a defensible prior stated as a prior." });
blocks.push({ p: "**Headline gaps.** No disclaimer language anywhere in the file (H-2) — at the stated bar this alone is disqualifying until fixed. No enforcement: every gate is prose, with no scripts, no templates, no references (M-5). The sourcing rule (\u201ccross-check each figure across at least two independent outlets\u201d) lacks skill 1's tier structure and skill 3's data-gap handling. Confidence labeling is good on paper (four labels, including Unverifiable) but unenforced. Routing overlaps the other two skills (M-6)." });
blocks.push({ p: "**Assessment.** Does not pass at the stated bar in its current form, despite the strongest prose methodology of the three. The gap is not analytical quality; it is compliance posture and the complete absence of enforcement artifacts. Both are cheap to fix, and the P0/P1 items in Section 7 would lift this skill materially." });

blocks.push({ h2: "4.3 bigtech-equity-research — quantified note with strong epistemics (rubric 3.00 / 5)" });
blocks.push({ p: "Skill 3 is a seven-phase process producing a 13-section self-contained HTML research note, with three operating modes (event post-mortem, multi-quarter trend, pre-event setup). Its hard rules are crisply stated: never fabricate; the delta versus consensus moves price, not the absolute; isolate the idiosyncratic move before calling it company-specific; rank root causes and classify each as structural versus cyclical/accounting; tag every figure; label judgment as judgment; no investment advice. Its quant kit covers beat/miss deltas, abnormal return versus QQQ/XLK, options-implied move versus realized, capex-to-OCF ratio, FCF trajectory, an implied-consensus-OCF shortfall identity, average price-target cuts, and a root-cause waterfall with per-factor confidence tags." });
blocks.push({ p: "**Verified strengths.** The anti-fabrication protocol and Data-Gap Ledger are the most sophisticated epistemic devices in the repository: when tools are offline the skill shrinks scope to verified-in-context data, tags every gap Assumed or Unverifiable with explicit bounds, and ledgers the exact source pull needed to close it — rather than backfilling from memory. The rule that no \u201cexecuted verification\u201d claim may be made for price targets or forward guidance correctly distinguishes reported third-party actions from observable outcomes. All seven quant_helpers functions executed correctly against their documented targets in this audit (revenue delta −0.64B / −0.50%; EPS delta −0.90 / −29.80%; alpha −11.1pp; capex/OCF 121.4%; average PT cut −13.7%; waterfall sum 12.6) — the arithmetic is sound even where the governance around it is not (M-4). The miss-versus-deceleration distinction in Phase 3 is a genuinely institutional touch most retail analysis misses." });
blocks.push({ p: "**Headline gaps.** The segment map misstates ASC 280 reportable segments for Nvidia, Amazon and Apple (H-3, verified against the 10-Ks) — in the very file that declares EDGAR segment tables the source of truth. The worked example conflicts with skill 1's on the same event (H-1). The self-test does not assert, and formulas.md's OCF-shortfall example carries a sign error against the code (M-4). The sourcing doc contradicts the methodology on transcript tiers (M-3). There is no GAAP-to-non-GAAP bridge phase (I-2), and the waterfall mandate lacks skill 1's computability guard (M-2)." });
blocks.push({ p: "**Assessment.** Does not pass at the stated bar as shipped. The epistemic framework is the best of the three and the quant kit is sound, but a reference file with ASC 280 errors in a skill whose Phase 3 depends on it is the kind of defect that destroys credibility with an institutional reader on first inspection." });

// ============ 5. CROSS-SKILL COMPARISON AND SCORECARD ============
blocks.push({ h1: "5. Cross-Skill Comparison and Scorecard" });

blocks.push({ h2: "5.1 Portfolio comparison matrix" });
blocks.push({ p: "The three skills are best understood as one product family with three divergent implementations of the same brief. The matrix below compares them across the dimensions an institutional reviewer would tabulate first." });
blocks.push({ table: {
  caption: "Portfolio comparison of the three skills",
  headers: ["Dimension", "Skill 1 · analyzing-us-bigtech-stocks", "Skill 2 · big-tech-earnings-postmortem", "Skill 3 · bigtech-equity-research"],
  widths: [22, 26, 26, 26],
  rows: [
    ["Primary deliverable", "12–16-page HTML deck + keyboard viewer (\u201cMidnight IC\u201d system, 1280×720)", "7-section restrained HTML deliverable", "13-section self-contained HTML research note"],
    ["Artifacts shipped", "8 files: SKILL.md, 2 JSON templates, 3 references, 2 scripts", "1 file: SKILL.md (283 lines)", "8 files: SKILL.md, 4 references, 2 templates, 1 script"],
    ["Enforcement gates", "2 executable audits + Definition-of-Done checklist", "Definition-of-Done checklist only — no scripts", "Definition-of-Done checklist + non-asserting quant helper"],
    ["Confidence taxonomy", "3 labels; Verified = ≥1 primary source, decision-critical double-sourced", "4 labels (adds Unverifiable); Verified = executed and observed", "4 labels; Verified = ≥2 independent primary sources, consistent to precision"],
    ["Attribution doctrine", "Ordinal ranks; percentages only if computable from sourced data", "Ordinal ranks only; percentages are \u201cfalse precision\u201d", "Quantified waterfall summing to the realized move, weights tagged Reasoned"],
    ["Segment reference data", "None embedded — process guidance only", "None embedded", "Embedded map; 3 of 7 companies misstate ASC 280 segments"],
    ["Worked example", "Alphabet Q3 2026; externally verified in most respects (Bloomberg-exact GOOG close)", "None", "Alphabet Q3 2026; conflicts with skill 1 (GOOGL move, consensus FCF)"],
    ["Disclaimer present", "Yes — SKILL.md, methodology, templates", "No — zero occurrences", "Yes — description, hard rules, sourcing doc"],
    ["License declared", "No", "Apache 2.0 (frontmatter)", "No"],
    ["Rubric average (0–5)", "4.45", "2.85", "3.00"],
  ],
}});

blocks.push({ h2: "5.2 Doctrinal conflicts" });
blocks.push({ p: "Beyond packaging, the three skills disagree on doctrine — the rules an executing agent would follow differently depending on which skill fires. These conflicts are the strongest argument for the shared-standard remediation in Section 7." });
blocks.push({ table: {
  caption: "Doctrinal positions in direct conflict",
  headers: ["Question", "Skill 1", "Skill 2", "Skill 3"],
  widths: [28, 24, 24, 24],
  rows: [
    ["May the move be allocated in percentages?", "Only if computable from sourced data; otherwise state qualitative", "Never — use ordinal ranks", "Yes — waterfall must sum to the realized move"],
    ["What earns the Verified label?", "Observed in ≥1 named primary source; decision-critical cross-checked in ≥2", "Executed/checked and observed directly", "≥2 independent primary/near-primary sources, consistent to precision"],
    ["Where do Motley Fool transcripts sit?", "Tier 1 (primary), alongside EDGAR and company IR", "Not specified", "Preference tier 2 in methodology; tier 6 aggregator in sourcing doc (internal conflict)"],
    ["Market-cap delta method", "Shares outstanding × Δprice (10-Q cover), percentage method labeled approximation", "Not specified", "Pre-print market cap × |move| as the stated formulas"],
    ["What happens when tools are offline?", "Data cutoff restated; refresh duty before delivery", "Not specified", "Anti-fabrication protocol + Data-Gap Ledger with exact pulls"],
    ["Deliverable format", "Fixed-canvas deck + viewer", "HTML slide sequence", "Single-file semantic HTML note (WCAG-AA, print-friendly)"],
  ],
}});

blocks.push({ h2: "5.3 Institutional-readiness scorecard" });
blocks.push({ p: "The scorecard below expresses the audit's conclusions on ten dimensions, scored 0–5 against fixed anchors: 0 = absent; 1 = mentioned only; 2 = partial or inconsistent; 3 = present with material gaps; 4 = present and enforced with minor gaps; 5 = institutional grade. The scores are the auditor's reasoned judgments anchored to the findings in Section 3 and the verification ledger in Section 6 — they are assessments, not measurements, and the anchors are stated so the reader can recalibrate." });
blocks.push({ chart: { path: "assets/rubric_heatmap.png", caption: "Institutional-readiness scorecard, ten dimensions × three skills (auditor assessment, 0–5)" } });
blocks.push({ table: {
  caption: "Scorecard with per-dimension basis",
  headers: ["Dimension", "Skill 1", "Skill 2", "Skill 3", "Basis (finding refs)"],
  widths: [30, 11, 11, 11, 37],
  rows: [
    ["Sourcing & verification discipline", "5.0", "3.5", "3.5", "Tier system vs two-outlet rule vs hierarchy with internal contradiction (M-3)"],
    ["Fact / judgment separation & confidence labels", "4.0", "4.0", "4.0", "All three label rigorously; taxonomies differ (M-3)"],
    ["GAAP vs non-GAAP reconciliation", "5.0", "5.0", "2.5", "Skill 2's cash/non-cash × recurring/one-time split strongest; skill 3 has no bridge phase (I-2)"],
    ["Reference-data accuracy (segments, examples)", "4.0", "3.0", "2.0", "Skill 1 verified externally with one disputed figure (H-1); skill 3's segment map in error (H-3); skill 2 embeds none"],
    ["Attribution methodology rigor", "5.0", "4.0", "3.5", "Skill 1's conditional rule is the defensible canon; skill 3 mandates without the guard (M-2)"],
    ["Model governance (SR 11-7 analogy)", "4.0", "1.0", "2.5", "Asserting self-test vs none vs non-asserting test and sign error (M-4, M-5)"],
    ["Audit gates & QA automation", "4.0", "1.0", "1.5", "Two real gates (one evadable, H-4) vs prose-only vs checklist (M-5)"],
    ["Compliance posture (disclaimer, MNPI, licensing)", "4.5", "1.5", "4.0", "Disclaimer present in 1 and 3, absent in 2 (H-2); MNPI statement absent in all (I-1); licensing (L-2)"],
    ["Reproducibility & engineering hygiene", "4.0", "2.0", "3.0", "Deterministic helpers and JSON audits vs environment-coupled Playwright (M-7), packaging drift (L-1)"],
    ["Deliverable craftsmanship", "5.0", "3.5", "3.5", "Documented design system with overflow budget; two deliverable specs unspecified to that depth"],
    ["Average", "4.45", "2.85", "3.00", "—"],
  ],
}});

// ============ 6. VERIFICATION LEDGER ============
blocks.push({ h1: "6. Verification Ledger" });
blocks.push({ p: "Per the audit protocol, the ledger records what was checked, how, and the observed result. Commands were executed on 2026-10-30 against the clone at HEAD 48cd3f97; external sources were consulted the same day. Exit codes are reported where meaningful." });
blocks.push({ table: {
  caption: "Verification ledger (19 checks)",
  headers: ["#", "Check", "Method", "Result", "Confidence"],
  widths: [5, 27, 30, 26, 12],
  zebra: true,
  rows: [
    ["1", "Repository cloned at stated HEAD", "git clone --depth 1; git log -1", "48cd3f97 · 2026-10-30 13:15 +0800 · \u201cupdate skills\u201d", "Verified"],
    ["2", "File inventory of the three skills", "find + wc -l", "17 files · 2,078 lines; skill 2 = single file", "Verified"],
    ["3", "fact_base_audit.py self-test", "python3 …/fact_base_audit.py --selftest", "PASS (exit 0); detects missing token, BADREF page, placeholder", "Verified"],
    ["4", "Numeric-audit evasion (substring false-pass)", "Custom 4-case harness against the script", "82.3 vs \u201c$282.32\u201d → PASS exit 0; 12.29 vs \u201c−112.29%\u201d → PASS exit 0; controls correct", "Verified"],
    ["5", "Checks-mode and scan-only mode", "Probe slide + checks.json", "Missing needle flagged exit 1; placeholder scan flags TODO/placeholder", "Verified"],
    ["6", "Placeholder scan scope (raw HTML)", "Probe slide with clean visible text + CSS class / JS token", "False positives on /placeholder/ and /\\bundefined\\b/ from code blocks", "Verified"],
    ["7", "quant_helpers.py correctness", "python3 quant_helpers.py; hand-checked identities", "All 7 outputs match documented targets; OCF shortfall prints +10.10B vs formulas.md −10.10B", "Verified"],
    ["8", "overflow_audit.mjs behavior", "node --check; usage run; probe slide with true overflow + data-bleed element", "True overflow flagged (exit 1); body-margin false positive on h1/p (right=1288); Playwright resolved via hardcoded path", "Verified"],
    ["9", "GOOG October 29 close", "Bloomberg quote page (GOOG:US)", "$282.32 · −$39.57 · −12.29% as of 5:20 PM EDT 10/29/26 — matches skill 1 exactly", "Verified"],
    ["10", "Prior closes (October 28)", "Yahoo Finance pre-event article ticker strip", "GOOG $321.89 (+1.60%) · GOOGL $324.89 (+1.34%)", "Verified"],
    ["11", "Alphabet Q3 2026 fundamentals", "Yahoo Finance, WSJ, Reuters, earnings-call transcript", "Revenue $127.6B (consensus $127.9B Yahoo) · GAAP EPS $2.12 · adj. EPS $2.67 · OCF $42.3B · FCF −$9.1B · TTM FCF $19.7B · Cloud $30.7B (+103%)", "Verified"],
    ["12", "Event superlatives", "Yahoo, Bloomberg, WSJ headlines", "Worst day ever since 2004 IPO; ≈$482B erased (Yahoo), ~$500B (WSJ); second-largest one-day wipeout for a US-listed stock (Bloomberg)", "Verified"],
    ["13", "Nvidia reportable segments", "SEC EDGAR FY2026 10-K (nvda-20260125.htm)", "Two segments: Compute & Networking, Graphics — segment-maps.md in error", "Verified"],
    ["14", "Amazon reportable segments", "SEC EDGAR FY2025 10-K (amzn-20251231.htm)", "Three segments: North America, International, AWS; advertising is a net-sales line — segment-maps.md in error", "Verified"],
    ["15", "Apple reportable segments", "10-K structure via multiple secondary confirmations", "Five geographic segments; product lines are revenue disaggregation — segment-maps.md in error", "Verified"],
    ["16", "GOOGL October 29 close adjudication", "Yahoo article/ticker prints; Bloomberg GOOGL page (blocked)", "Prints −12.78% / −12.79% (283.35–283.37); matches neither skill (−11.71% / −12.6%); official close unconfirmed", "Reasoned"],
    ["17", "Disclaimer presence", "Case-insensitive grep across the three skills", "Skills 1 and 3: multiple hits; skill 2: zero", "Verified"],
    ["18", "Licensing and catalog indexing", "Filesystem check; case-insensitive grep of skills-catalog.md and skills-inventory.md", "No root LICENSE; no catalog/inventory entry for any of the three skills", "Verified"],
    ["19", "Impact arithmetic", "Python computation", "12.15B × $39.57 = $480.8B ≈ press $482B; GOOGL move gap 0.89pp ≈ $35.1B on ≈$3.95T; avg PT cut −13.7%; rev delta −0.50%", "Verified"],
  ],
}});

// ============ 7. REMEDIATION ROADMAP ============
blocks.push({ h1: "7. Remediation Roadmap" });
blocks.push({ p: "The roadmap is sequenced by the standard applied throughout: fix what blocks the stated bar first, then governance, then hygiene. Effort estimates assume the repository maintainer executes with the audit's evidence in hand; every P0 item is independently verifiable after the fix using the same checks recorded in Section 6." });

blocks.push({ h2: "7.1 P0 — ship blockers at the stated bar (≈1 day combined)" });
blocks.push({ table: {
  caption: "P0 remediation items",
  headers: ["#", "Action", "Closes", "Effort", "Verification after fix"],
  widths: [5, 42, 12, 11, 30],
  rows: [
    ["1", "Restructure segment-maps.md into \u201creportable segments\u201d vs \u201crevenue disaggregation\u201d with per-company vintages and refresh cadence", "H-3", "30 min", "Diff against NVDA FY2026 / AMZN FY2025 / AAPL 10-K segment tables"],
    ["2", "Add disclaimer + public-sources statement to skill 2's quality gates and Step 9 design constraints", "H-2, I-1", "15 min", "Grep for disclaimer language returns hits in all three skills"],
    ["3", "Boundary-anchor token_in() in fact_base_audit.py; add the two evasion cases to --selftest", "H-4", "1 h", "The Section 6 harness returns MISSING + exit 1 for both substring cases"],
    ["4", "Reconcile worked examples into one canonical, dated, sourced file; correct or source the GOOGL figure and the consensus figures", "H-1", "2 h", "Cross-skill diff of shared datapoints returns zero conflicts; GOOGL figure matches an exchange close record"],
  ],
}});

blocks.push({ h2: "7.2 P1 — governance and control quality (≈1 week)" });
blocks.push({ bullets: [
  "Extract a shared sourcing / confidence / attribution standard (one taxonomy, one source hierarchy with transcript tiering resolved, one attribution policy) consumed by all three skills; add a repository-level consistency test that diffs shared doctrine and shared datapoints at commit time (M-2, M-3, H-1 recurrence).",
  "Fix the render audit: overflow relative to the .slide rectangle or a mandated html,body reset in the token sheet; offline-tolerant page-load strategy; document the Playwright prerequisite and remove machine-specific absolute paths (M-1, M-7).",
  "Convert quant_helpers.py to an asserting self-test; correct the formulas.md OCF-sign example or define the convention in both places; add pytest with zero-division and empty-input cases (M-4).",
  "Port the fact-base and audit-gate pattern into skill 2 (or delegate to skill 1's scripts), reuse skill 3's evidence-ledger template, and demarcate the three skills' descriptions with cross-references; register all three in skills-catalog.md (M-5, M-6).",
]});

blocks.push({ h2: "7.3 P2 — hygiene (as convenient)" });
blocks.push({ bullets: [
  "Standardize folder conventions and frontmatter across the three skills (L-1); add a root LICENSE and per-skill license fields (L-2).",
  "Repair the formulas.md code fence and replace the circular market-cap pair with shares × Δprice as primary (L-3); scope the placeholder scan to visible text (L-4); relabel the evidence-ledger phase reference (L-5).",
  "Move the worked example's analyst-action specifics into a dated, source-linked appendix, or mark them illustrative (L-6); add a GAAP-bridge phase to skill 3 (I-2); require consensus-vendor attribution in every worked example (I-3).",
]});

blocks.push({ p: "Sequencing note: items 1–4 of P0 are independent of each other and can land as four atomic commits; the P1 shared-standard work should follow the P0 reconciliation so the canonical example file becomes the first consumer of the shared standard rather than a fourth divergent copy." });

// ============ 8. APPENDIX A ============
blocks.push({ h1: "8. Appendix A — File Inventory" });
blocks.push({ p: "The seventeen in-scope files with line counts and roles, as read in full during this audit (HEAD 48cd3f97)." });
blocks.push({ table: {
  caption: "Audited file inventory",
  headers: ["File", "Lines", "Role"],
  widths: [52, 10, 38],
  zebra: true,
  rows: [
    ["analyzing-us-bigtech-stocks/SKILL.md", "238", "Entry point: triggers, confidence system, 11-phase pipeline, bundled-resources map"],
    ["…/assets/fact_base.template.json", "75", "Fact-base skeleton with worked example patterns"],
    ["…/assets/slides_brief.template.json", "32", "15-page deck-plan skeleton with per-slide task briefs"],
    ["…/references/fact-base-schema.md", "153", "Field definitions, confidence rules, conflicts, worked examples"],
    ["…/references/methodology.md", "355", "Full phase-by-phase playbook, source tiers, pitfall catalog, compliance notes"],
    ["…/references/report-design.md", "135", "Midnight IC tokens, component library, 15-page archetype map, overflow budget"],
    ["…/scripts/fact_base_audit.py", "228", "Numeric + placeholder audit (modes: fact-base, checks, scan, selftest)"],
    ["…/scripts/overflow_audit.mjs", "126", "Playwright render/overflow audit for 1280×720 decks"],
    ["big-tech-earnings-postmortem/SKILL.md", "283", "Single-file 9-step post-earnings RCA methodology"],
    ["bigtech-equity-research/SKILL.md", "111", "Entry point: hard rules, modes, workflow, anti-fabrication protocol"],
    ["…/reference/formulas.md", "73", "Quant formulas with worked examples"],
    ["…/reference/methodology.md", "109", "Seven-phase research process"],
    ["…/reference/segment-maps.md", "20", "Reportable segments per company (subject of H-3)"],
    ["…/reference/sourcing-and-confidence.md", "35", "Source hierarchy, confidence taxonomy, anti-hallucination rules, disclaimer"],
    ["…/scripts/quant_helpers.py", "55", "Deterministic delta/alpha/waterfall math (subject of M-4)"],
    ["…/templates/evidence-ledger.md", "21", "Evidence + Data-Gap ledger format"],
    ["…/templates/report-structure.md", "29", "13-section deliverable spec"],
  ],
}});

// ============ 9. APPENDIX B ============
blocks.push({ h1: "9. Appendix B — External Sources Consulted" });
blocks.push({ p: "External sources consulted during verification, with what each was used to establish. All retrievals occurred 2026-10-30; quotes are as retrieved. Paywalled or robot-blocked pages are marked and their accessible content described." });
blocks.push({ table: {
  caption: "External sources and what they verified",
  headers: ["Source", "Used to establish", "Reference"],
  widths: [30, 42, 28],
  zebra: true,
  rows: [
    ["Bloomberg — GOOG:US quote page", "GOOG official close $282.32, −$39.57, −12.29% (as of 5:20 PM EDT 2026-10-29); \u201cworst drop on record; second biggest-ever market-value wipeout\u201d", "bloomberg.com/quote/GOOG:US (GOOGL page robot-blocked)"],
    ["Yahoo Finance — event coverage", "$482B market-value loss headline; GOOG/GOOGL ticker prints 281.14/283.37 (−12.66%/−12.78%); intraday article 281.09/283.35; revenue $127.6B vs $127.9B S&P-analyst consensus; GAAP EPS $2.12; ad revenue short of estimates with Cloud beat at $30.7B; PCE 3.6% from 3.4%; Fed hold", "finance.yahoo.com — Alphabet Q3 2026 coverage set"],
    ["Yahoo Finance — pre-event article ticker", "October 28 closes: GOOG $321.89 (+1.60%), GOOGL $324.89 (+1.34%)", "finance.yahoo.com — pre-earnings preview page"],
    ["Reuters", "Net income to common fell 25% to $26.17B; adjusted EPS $2.67 missed Wall Street", "reuters.com — \u201cAlphabet stock sinks as search woes cause revenue miss\u201d"],
    ["WSJ", "Worst day on record; roughly $500B erased; $127.6B sales narrowly missing expectations; Cloud $30.7B beat", "wsj.com — Alphabet selloff coverage"],
    ["Earnings-call transcript (via Yahoo Finance)", "\u201cWe had negative free cash flow of $9.1 billion in the third quarter, driven by our investments in CapEx\u201d; FCF $19.7B TTM; OCF $42.3B", "Alphabet Q3 FY2026 earnings call transcript"],
    ["SEC EDGAR — NVIDIA FY2026 10-K", "Two reportable segments (Compute & Networking; Graphics) with Data Center and Automotive inside C&N — segment-maps.md error confirmed", "sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm"],
    ["SEC EDGAR — Amazon FY2025 10-K", "Three reportable segments (North America, International, AWS); advertising as net-sales driver, not a segment", "sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm"],
    ["Apple 10-K structure (secondary confirmations)", "Five geographic reportable segments; FY2025 net sales Americas $178.4B, Europe $111.0B, Greater China $64.4B", "stock-analysis-on.net; secfilingdata.com; academic case analyses"],
    ["Amazon IR — Q4 2025 results release", "Segment tables for North America / International / AWS only", "ir.aboutamazon.com — fourth-quarter results"],
    ["Business Insider / mlq.ai / Barron's headlines", "Corroborating event framing, analyst-reaction timing, sector tape", "businessinsider.com; mlq.ai; barrons.com"],
    ["Stooq daily CSV (attempted)", "Independent close adjudication — blocked by JavaScript verification wall; noted as a limitation", "stooq.com (inaccessible to fetcher)"],
  ],
}});

module.exports = { blocks };
