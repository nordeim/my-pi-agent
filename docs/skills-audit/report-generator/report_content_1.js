// Audit report content — Part 1: Executive Summary, Scope/Standards/Method, Findings.
// Block types: {h1|h2|h3: string}, {p: string with **bold** markers}, {bullets: [..]},
// {table: {caption, headers, rows, widths?, zebra?}}, {finding: {...}}, {chart: {path, caption}}
"use strict";

const blocks = [];

// ============ 1. EXECUTIVE SUMMARY ============
blocks.push({ h1: "1. Executive Summary" });

blocks.push({ p: "This report presents an independent audit of three agent skills in the repository **nordeim/my-pi-agent** (cloned 2026-10-30, HEAD 48cd3f97, commit message \u201cupdate skills\u201d): **analyzing-us-bigtech-stocks**, **big-tech-earnings-postmortem**, and **bigtech-equity-research**. The evaluation question was fixed by the engagement brief: would this work meet the standards expected of major investment banks and institutional fund managers on Wall Street? To answer it, all 17 in-scope files were read in full, all three shipped scripts were executed against positive and negative test cases, and the skills' own embedded \u201cverified\u201d facts were tested against twelve external sources including SEC filings, Bloomberg, Reuters, WSJ and Yahoo Finance. Nineteen verification checks were recorded; every material claim in this report carries a confidence tag (Verified / Reasoned / Assumed)." });

blocks.push({ p: "The verdict: **none of the three skills passes a full bulge-bracket research-controls review as shipped, and one of them is genuinely close.** Skill 1, analyzing-us-bigtech-stocks, is the strongest artifact — its sourcing tiers, forced-hypothesis discipline, GAAP-adjusted bridge and dual executable audit gates are institutional in design, and its worked example survived external verification better than anything else audited: the GOOG close of $282.32 (−12.29%), the −$9.1B quarterly free cash flow, the $2.67 adjusted EPS, the $42.3B operating cash flow, the $30.7B Cloud result and the \u201csecond-largest one-day market-value wipeout ever\u201d ranking were each confirmed against Bloomberg, Reuters, the earnings-call transcript or Yahoo Finance. Its gaps are an evadable numeric-audit matcher (H-4), coordinate assumptions in the render audit (M-1), and one cross-class figure that conflicts with a sibling skill (H-1)." });

blocks.push({ p: "Skill 2, big-tech-earnings-postmortem, contains the best single-file methodology prose of the three — its durability-versus-evidence driver classification and its failure-mode catalog (\u201csell-side ventriloquism\u201d, the \u201caccounting-noise hand-wave\u201d) read like real desk experience — but it is the only skill that promises \u201cinstitutional-grade\u201d research deliverables while containing **no disclaimer language whatsoever** (H-2), and it ships zero enforcement artifacts: every quality gate is prose (M-5). Skill 3, bigtech-equity-research, contributes the most sophisticated epistemics in the repo — a Data-Gap Ledger and an anti-fabrication protocol for offline tooling — but its segment reference file misstates ASC 280 reportable segments for three of seven companies, verified directly against the FY2025/FY2026 10-Ks (H-3); its quant helper's \u201cself-test\u201d prints without asserting (M-4); and its worked example contradicts skill 1's on the same real event (H-1)." });

blocks.push({ p: "The deepest deficiency is portfolio-level. Three skills claim the same trigger space (\u201cwhy did big tech X move after earnings\u201d) with three different deliverable formats, two different confidence taxonomies, and three mutually inconsistent doctrines on whether a price move may be allocated across drivers in percentage terms (M-2, M-3, M-6). The repository thus violates, across skills, the exact conflict-recording discipline the skills themselves enforce within a report. Twenty findings were classified in total; none is Critical in the security or data-loss sense, four are High, seven Medium, six Low and three Informational. A four-item P0 list — segment-map correction, disclaimer, matcher fix, worked-example reconciliation — would close most of the distance between skill 1 and the stated bar." });

blocks.push({ table: {
  caption: "Audit outcome summary",
  headers: ["Severity", "Count", "Findings"],
  widths: [16, 10, 74],
  rows: [
    ["Critical", "0", "None. No security vulnerability, data-loss path or production crash was found."],
    ["High", "4", "H-1 conflicting verified figures across skills · H-2 no disclaimer in skill 2 · H-3 segment-map ASC 280 errors · H-4 numeric-audit false-pass hole"],
    ["Medium", "7", "M-1 render-audit coordinates · M-2 attribution doctrine conflict · M-3 confidence-taxonomy drift · M-4 non-asserting self-test and sign error · M-5 unenforced quality bar in skill 2 · M-6 routing overlap and catalog non-indexing · M-7 environment-coupled Playwright dependency"],
    ["Low", "6", "L-1 packaging drift · L-2 no root LICENSE · L-3 formulas.md fence and circular pair · L-4 placeholder scan on raw HTML · L-5 phase/section mislabel · L-6 unverifiable embedded sell-side specifics"],
    ["Informational", "3", "I-1 no MNPI/Reg FD statement · I-2 skill 3 lacks a GAAP bridge phase · I-3 consensus-vendor attribution variance"],
  ],
}});

blocks.push({ p: "Scorecard averages on the ten-dimension institutional rubric (Section 5.3, anchored to the evidence in Sections 3 and 6): **skill 1 = 4.45 / 5**, **skill 2 = 2.85 / 5**, **skill 3 = 3.00 / 5**. The rubric scores are the auditor's reasoned judgments, not measurements; the anchors and per-dimension reasoning are stated alongside them." });

// ============ 2. SCOPE, STANDARDS AND METHOD ============
blocks.push({ h1: "2. Scope, Standards and Method" });

blocks.push({ h2: "2.1 Scope and repository context" });
blocks.push({ p: "my-pi-agent is a customization bundle for the Pi agent (themes, extensions and a 340-skill library). The three audited skills sit under skills/ and total 17 files and 2,078 lines (Appendix A). Skill 1 ships a 238-line SKILL.md plus two JSON templates, three reference documents and two executable audit scripts. Skill 2 ships a single 283-line SKILL.md with no supporting artifacts of any kind. Skill 3 ships a deliberately lean 111-line SKILL.md plus four reference files, two templates and one Python helper. The audit was read-only: the cloned repository was not modified, and all experiments ran from scratch copies under the auditor's own scripts directory." });
blocks.push({ p: "Two repository-level facts frame the audit. First, the repository has **no root LICENSE file**; the only license declaration in scope is skill 2's frontmatter (Apache 2.0), which leaves the redistribution terms of skills 1 and 3 ambiguous (L-2). Second, the repository's own discovery layer — skills/skills-catalog.md and skills-inventory.md, which the README designates as the routing entry point — contains **no reference to any of the three skills** (case-insensitive search), so an agent routed through the catalog would never discover them (part of M-6). Both facts were verified directly in the clone." });

blocks.push({ h2: "2.2 The institutional standards applied" });
blocks.push({ p: "The evaluation rubric translates the engagement brief — \u201cthe highest standards expected of major investment banks and fund managers on Wall Street\u201d — into seven concrete regulatory and craft frameworks, plus skill-engineering practice as a secondary axis. The table below lists each standard and where it bites in this audit. This is an analytical benchmark applied by analogy to agent skills, not a claim that the skills are regulated securities research; where a standard is inapplicable in form but applicable in substance (for example, FINRA 2241 as a disclosure-norm template for a non-broker artifact), that is stated." });
blocks.push({ table: {
  caption: "Standards framework and points of application",
  headers: ["Standard", "What it demands", "Where it applies here"],
  widths: [26, 37, 37],
  rows: [
    ["CFA Institute Code & Standards, V(A) and V(B)", "Diligence and reasonable basis for every claim; communication distinguishes fact from opinion; limitations disclosed", "Sourcing tiers, confidence labels, forced two-sidedness, hypothesis-exclusion discipline"],
    ["SEC Reg S-K Item 10(e)", "Non-GAAP measures reconciled to the most comparable GAAP measure; no greater prominence for non-GAAP", "GAAP-vs-adjusted bridges, ex-item arithmetic on the page, consensus-basis statements"],
    ["FINRA Rule 2241 (disclosure norms, by analogy)", "Research disclosures: basis of conclusions, risk framing, no unconditional recommendations, disclaimer language", "Disclaimers, scenario-not-price-target doctrine, risk/catalyst matrices"],
    ["Regulation FD / MNPI discipline", "Public information only; no material non-public information", "Source tiers restricted to filings, press, transcripts; absence of an explicit MNPI statement noted (I-1)"],
    ["OCC SR 11-7 model risk management (by analogy)", "Conceptual soundness, testing, documentation, independent validation for quantitative code", "Script self-tests, formula documentation, quant_helpers governance (M-4)"],
    ["ASC 280 segment reporting", "Use the issuer's actual reportable segments; treat the CODM measure with comparability caveats", "segment-maps.md accuracy for seven companies (H-3)"],
    ["Institutional research hygiene", "Vintage dating of data, consensus-vendor attribution, error-correction policy, audit trail", "Fact-base schema, append-only corrections, cutoff stamps, verification ledgers"],
  ],
}});

blocks.push({ h2: "2.3 Audit method and evidence classes" });
blocks.push({ p: "The audit proceeded in four passes. (1) **Full-file reads**: all 17 files were read end-to-end without truncation, plus the repository README, package.json, skills-catalog.md and skills-inventory.md for context. (2) **Script execution**: fact_base_audit.py was run in self-test, fact-base, checks and scan-only modes, then subjected to a purpose-built negative harness (four cases); quant_helpers.py was executed and every printed output compared with its documented target; overflow_audit.mjs was syntax-checked, usage-checked and executed against a purpose-built overflow probe page. (3) **External verification**: the skills' embedded \u201creal, verified facts\u201d about the Alphabet Q3 2026 event were checked against Bloomberg, Reuters, WSJ, Yahoo Finance and the earnings-call transcript, and the segment maps were checked against the NVDA FY2026 and AMZN FY2025 10-Ks on SEC EDGAR plus Apple's 10-K segment structure. (4) **Cross-skill comparison**: trigger descriptions, confidence taxonomies, attribution doctrines, deliverable formats and worked-example data were diffed across the three skills." });
blocks.push({ p: "Every material claim below is tagged per the audit protocol: **Verified** means the check was executed and the result observed directly in this engagement; **Reasoned** means logical inference from verified evidence; **Assumed** means a stated assumption. Findings and fixes are kept separate — no repository code was rewritten during this audit, in accordance with the review-only scope." });

blocks.push({ h2: "2.4 Limitations" });
blocks.push({ bullets: [
  "GOOGL's official October 29, 2026 closing price could not be independently confirmed: Bloomberg's GOOGL quote page was robot-blocked, and the accessible Yahoo Finance prints (−12.78% / −12.79%, 283.35–283.37) match neither skill 1's −11.71% nor skill 3's −12.6%. Adjudication of that specific figure is therefore tagged Reasoned, while the existence of the cross-skill conflict is Verified.",
  "Analyst-action specifics embedded in skill 1's worked example (Citizens JMP downgrade, Wedbush price-target move, FactSet consensus figures, a BofA multiple comparison) could not be verified externally within this audit's time box. They are treated as unverified-by-audit, not as false — several surrounding figures in the same worked example did verify (L-6).",
  "overflow_audit.mjs was executed against a synthetic probe deck, not against a complete deck produced by the skill's own 15-page pipeline.",
  "The audit ran on 2026-10-30 against the clone at HEAD 48cd3f97; anything committed later is out of scope.",
]});

// ============ 3. FINDINGS BY SEVERITY ============
blocks.push({ h1: "3. Findings by Severity" });
blocks.push({ p: "Findings are ordered by severity, not by file order. Each finding states location, description, evidence, impact, severity, a concrete recommended fix, and the auditor's confidence. Severity anchors: Critical blocks release (security, data loss, production crash); High is incorrect behavior or a material control gap on a common path; Medium is an edge-case defect, control weakness or consistency problem; Low is style, convention or documentation quality; Informational is advisory. No Critical findings were identified — an honest result, not a padded one: the scripts are well-engineered and the failure modes found are quality-assurance and consistency failures, not safety failures." });

blocks.push({ h2: "3.1 High-severity findings" });

blocks.push({ finding: {
  id: "H-1", title: "Conflicting \u201cverified\u201d figures for the same event across skills — no single source of truth", short: "Cross-skill figure conflicts on the same event",
  severity: "High",
  location: "analyzing-us-bigtech-stocks/references/methodology.md §§3–4 (worked example) vs bigtech-equity-research/reference/formulas.md (worked examples)",
  description: "Both skills use Alphabet's Q3 2026 print (reported 2026-10-28) as their worked example, and both present their figures as verified — yet they publish materially different numbers for the same datapoints: the GOOGL move is −11.71% in skill 1 and −12.6% in skill 3; consensus free cash flow is −$3.5B in skill 1 and −$2.70B in skill 3; revenue is $127.57B against $128.2B consensus in skill 1 and $127.58B against $128.22B in skill 3.",
  evidence: "Direct file comparison (Verified). External checks: Bloomberg's GOOG quote page confirms skill 1's Class C figures exactly — $282.32 close, −$39.57, −12.29%, as of 5:20 PM EDT 2026-10-29 — implying the $321.89 prior close it claims; Yahoo Finance pre-event pages confirm the October 28 closes ($321.89 GOOG / $324.89 GOOGL). For GOOGL on October 29, accessible Yahoo prints show −12.78%/−12.79% (283.35–283.37), matching neither skill. Skill 1's implied GOOGL close is 286.85; skill 3's is 283.95. On Alphabet's ≈$3.95 trillion market value, the 0.89-point gap between the two skills' GOOGL moves is ≈$35 billion of implied value — the two skills disagree by more than the market capitalization of most S&P 500 constituents.",
  impact: "Two skills in one library can issue reports carrying materially different \u201cVerified\u201d figures for the same event; a portfolio manager or research-controls function cross-checking them would flag the desk. The repository violates, across skills, the conflict rule both skills enforce within a report — skill 1: \u201csilent picking is forbidden\u201d; skill 3: \u201cnever present a figure reconstructed from memory.\u201d",
  fix: "Create one canonical, dated, fully sourced worked-example file (or shared fact-base JSON) consumed by all three skills; add a repository-level consistency test that diffs shared datapoints across skills; reconcile the GOOGL figure against an exchange close record and record the correction append-only, exactly as the skills' own doctrine requires.",
  confidence: "Verified (the conflict and its magnitude); Reasoned (which GOOGL figure is correct — GOOG verified exactly, GOOGL adjudication inconclusive).",
}});

blocks.push({ finding: {
  id: "H-2", title: "Skill 2 produces \u201cinstitutional-grade\u201d research deliverables with no disclaimer anywhere", short: "No disclaimer anywhere in skill 2",
  severity: "High",
  location: "big-tech-earnings-postmortem/SKILL.md — the entire 283-line file",
  description: "The skill's stated ambition is a research artifact \u201ca portfolio manager could defend in an investment committee.\u201d The file contains zero occurrences of \u201cinvestment advice\u201d, \u201cdisclaimer\u201d or \u201csolicitation\u201d. The quality-gates checklist omits any disclaimer requirement, and the deliverable spec (Step 9) bans placeholder values and fabricated citations but not missing disclosures.",
  evidence: "Case-insensitive grep across all three skills (Verified): skills 1 and 3 carry disclaimers in multiple places — skill 1's Definition of Done (\u201cDisclaimer present: informational only, not investment advice\u201d), its methodology §14 (\u201cInformational only — not investment advice, not a solicitation. No price targets published.\u201d) and its slide templates; skill 3's description, hard rule 7 and a dedicated Disclaimer section in sourcing-and-confidence.md. Skill 2 returns no matches in any form.",
  impact: "Measured against the FINRA 2241-style disclosure norms this audit applies by analogy, distributing an institutional-grade research artifact with no disclaimer or basis language is a compliance non-starter. It is also internally inconsistent: two sibling skills in the same repository treat the disclaimer as non-negotiable, and a publicly distributed skill teaches the omission by example.",
  fix: "Add the disclaimer to the quality gates and to Step 9's design constraints, aligned with skills 1 and 3; while editing, add the public-sources-only statement (I-1). Estimated effort: minutes.",
  confidence: "Verified.",
}});

blocks.push({ finding: {
  id: "H-3", title: "Segment map misstates ASC 280 reportable segments for three of seven companies", short: "Segment map wrong for 3 of 7 companies",
  severity: "High",
  location: "bigtech-equity-research/reference/segment-maps.md — the \u201cReportable segments\u201d column",
  description: "The file opens with \u201cUse the EDGAR 10-Q segment table as the source of truth,\u201d then lists, as reportable segments: for Nvidia — Data Center, Gaming, Professional Visualization, Automotive, OEM (these are market platforms, i.e. revenue disaggregation inside Nvidia's two reportable segments); for Amazon — North America, International, AWS and Advertising (Advertising is a net-sales disclosure line, not a reportable segment); for Apple — iPhone, Mac, iPad, Wearables/Home/Accessories, Services (product-line disaggregation; Apple's reportable segments are geographic). The Google, Microsoft, Meta and Tesla mappings are correct.",
  evidence: "SEC EDGAR, retrieved during this audit (Verified). NVIDIA FY2026 10-K (nvda-20260125.htm): \u201cThe Compute & Networking segment includes our Data Center … and Automotive platforms … The Graphics segment includes GeForce GPUs for gaming and PCs, and Quadro/NVIDIA RTX GPUs …\u201d — exactly two reportable segments, with Data Center and Automotive inside Compute & Networking. Amazon FY2025 10-K (amzn-20251231.htm): segment tables for North America, International and AWS only, with advertising discussed as a net-sales driver, not a segment. Apple's 10-K reports five geographic segments (Americas, Europe, Greater China, Japan, Rest of Asia Pacific; FY2025 net sales $178.4B / $111.0B / $64.4B respectively), with the product categories appearing as revenue disaggregation.",
  impact: "A Phase 3 \u201csegment variance table\u201d built from this map would attribute consensus variance to segments that do not exist as such in the filings — the exact class of error an institutional reader catches immediately, and the exact hallucination the skill's own sourcing rules exist to prevent. It also contradicts the file's own source-of-truth claim.",
  fix: "Restructure the map into two columns — \u201cReportable segments (ASC 280)\u201d versus \u201cKey disclosed revenue disaggregation / market platforms\u201d — per company, each with an as-of vintage (\u201cper FY2026 10-K\u201d) and a stated refresh cadence; add the comparability caveat that segment operating income is the CODM-reviewed measure and is not comparable across issuers.",
  confidence: "Verified (SEC filings retrieved and quoted).",
}});

blocks.push({ finding: {
  id: "H-4", title: "The numeric audit gate can silently pass absent numbers (unanchored substring matching)", short: "Numeric audit gate can silently pass",
  severity: "High",
  location: "analyzing-us-bigtech-stocks/scripts/fact_base_audit.py — token_in(), lines 59–66",
  description: "Fact tokens are matched against slide text with unanchored substring tests, so a fact's digit string \u201cpasses\u201d whenever it appears inside any other number printed on the page. The docstring's sign/symbol tolerance is a deliberate and reasonable design goal, but the implementation lacks digit-boundary anchoring.",
  evidence: "Executed harness, built and run for this audit (Verified): a fact recording a close of 82.3 against a slide printing only \u201c$282.32\u201d returns \u201cPASS — '82.3' present\u201d and exit code 0 (CLEAN); a fact of 12.29 against a slide printing only \u201c−112.29%\u201d likewise returns PASS and exit 0. Control cases behave correctly: a genuinely present number passes; a genuinely absent number (63.4) fails with exit 1. The script's own --selftest passes; these evasion cases are not in it.",
  impact: "Skill 1's golden rule 5 — \u201ca report that has not passed the numeric and render audits is not finished\u201d — is weaker than claimed. Number drift from the fact base can ship undetected whenever digits overlap, a realistic occurrence with prices and percentages that share digits (82.3 inside 282.32 is a live example, not a contrivance). In Wall Street QA terms, this is a control with a known evasion path.",
  fix: "Match tokens on digit boundaries — for example a regex of the form (?<![\\d.])TOKEN(?![\\d.]) applied to the symbol-stripped text, or tokenize the slide's numbers and compare parsed values under a formatting-normalization table; add the two evasion cases above to --selftest so the gate proves its own anchoring.",
  confidence: "Verified (executed and observed).",
}});

blocks.push({ h2: "3.2 Medium-severity findings" });

blocks.push({ finding: {
  id: "M-1", title: "Render audit measures against the viewport, not the slide origin; no mandated body reset", short: "Render audit measures viewport, not slide origin",
  severity: "Medium",
  location: "overflow_audit.mjs evaluate() (lines 85–105); report-design.md §1 (design tokens omit a html,body margin reset)",
  description: "The overflow check compares each element's bounding rectangle to the viewport dimensions (W×H), not to the .slide element's own box. Any deck whose page omits a body margin reset — the design tokens never mandate one — offsets the entire 1280×720 canvas by the default 8px, and every full-width element then reports a right edge at 1288px and fails the 2px-tolerance check.",
  evidence: "Probe execution (Verified): a purpose-built slide with a genuinely overflowing element and a properly sized .slide produced \u201cOVERFLOW … clipped: h1 bottom=66 right=1288 | p bottom=106 right=1288 | div.too-low bottom=755\u201d — the h1 and p flags are pure body-margin artifacts; only div.too-low was a true overflow. A secondary observation: the page load uses waitUntil networkidle against a design system that @imports Google Fonts, which can stall toward the 30-second timeout in offline environments.",
  impact: "Systematic false positives train users to dismiss OVERFLOW flags — the skill's own protocol then normalizes \u201cdocumented false positives\u201d — or, if a generator happens to reset margins, genuine 8px-scale defects are measured against a shifted origin. Either way the gate's authority erodes.",
  fix: "Compute overflow relative to the .slide element's bounding rect (offset-aware), or mandate html,body{margin:0;padding:0} in the token sheet and audit for it; make page loading fall back from networkidle to domcontentloaded with a bounded wait when fonts do not resolve.",
  confidence: "Verified (probe executed).",
}});

blocks.push({ finding: {
  id: "M-2", title: "Three mutually inconsistent doctrines on attribution quantification", short: "Three inconsistent attribution doctrines",
  severity: "Medium",
  location: "Skill 1 methodology §9; skill 2 SKILL.md \u201cCommon failure modes\u201d and Step 3; skill 3 SKILL.md Definition of Done and methodology Phase 7",
  description: "On the core methodological question — may the analyst allocate a realized price move across drivers in percentage terms — skill 1 says conditionally (\u201cordinal ranks only. Publish a percentage attribution only if it is computable from sourced data; otherwise write attribution is qualitative\u201d), skill 2 says never (\u201cFalse precision: inventing a percentage of the move attributable to each driver. Use ordinal ranks, not fake decompositions\u201d), and skill 3 says always, as a Definition-of-Done item (\u201cWaterfall quantified, sums to the realized move\u201d), softened only by its hard rule that weights are Reasoned.",
  evidence: "Direct quotation from the three files (Verified). Skill 3's own worked waterfall allocates −12.6 points across beta, FCF/capex, EPS quality, Search and positioning; skill 2's failure-mode list would classify exactly that artifact as a \u201cfake decomposition\u201d if the weights are not regression-derived.",
  impact: "Skill routing silently decides the answer to a methodological controversy: the same question yields a ranked table from one skill and a quantified waterfall from another, and the outputs are not comparable. A research desk operates one attribution policy, not three.",
  fix: "Adopt skill 1's conditional rule as the repository canon — quantify the market-wide beta component (computable from sourced index returns), label idiosyncratic splits explicitly as Reasoned analytical allocations, and never present weights as regression output — then make skills 2 and 3 reference the shared policy instead of restating divergent ones.",
  confidence: "Verified (textual).",
}});

blocks.push({ finding: {
  id: "M-3", title: "Confidence-taxonomy drift across skills, and an internal contradiction inside skill 3", short: "Confidence taxonomy drift across skills",
  severity: "Medium",
  location: "Skill 1 SKILL.md \u201cThe confidence system\u201d; skill 2 Step 7; skill 3 sourcing-and-confidence.md and methodology.md Phase 1",
  description: "The three skills ship different confidence taxonomies with different evidentiary bars for the same labels. Skill 1 uses three labels (Verified / Reasoned / Assumed) with Verified = observed in ≥1 named primary source and decision-critical items cross-checked in ≥2. Skill 2 uses four (adding Unverifiable) with Verified = \u201cexecuted/checked and observed directly.\u201d Skill 3 uses four with Verified = \u201c≥2 independent primary/near-primary sources, consistent to the reported precision.\u201d Separately, skill 3 contradicts itself on transcript providers: methodology.md Phase 1 lists Motley Fool / Seeking Alpha transcripts as source preference 2 (cross-checked against audio), while sourcing-and-confidence.md ranks Motley Fool in tier 6 aggregators (\u201cverify the underlying number elsewhere\u201d); skill 1 ranks the same transcripts T1.",
  evidence: "Direct quotation from the four files (Verified).",
  impact: "The same badge asserts different evidentiary bars depending on which skill fired, so outputs are not comparable and a quality function cannot apply one standard; the \u201cVerified\u201d guarantee degrades from a specification to an inclination. The intra-skill-3 contradiction additionally leaves transcript tiering undefined at exactly the point where earnings-postmortem evidence is densest.",
  fix: "Extract one shared sourcing-and-confidence reference (single taxonomy, single source hierarchy with transcript-provider tiering resolved) and have all three SKILL.md files consume it; keep the stronger of duplicate definitions and delete the weaker rather than reconciling by paraphrase.",
  confidence: "Verified (textual).",
}});

blocks.push({ finding: {
  id: "M-4", title: "quant_helpers self-test does not assert; formulas.md carries a sign error; no unit tests", short: "Self-test prints without asserting; sign error",
  severity: "Medium",
  location: "bigtech-equity-research/scripts/quant_helpers.py __main__ block; reference/formulas.md \u201cOCF shortfall\u201d worked example",
  description: "The __main__ block prints computed values next to hand-written comments but contains no assertions, so a silent formula regression would still print a healthy-looking \u201cself-test.\u201d The OCF-shortfall worked example in formulas.md states \u201c(−2.70 + 55.09) − 42.29 = −10.10B\u201d, while the same arithmetic executed in the script returns +10.10B — the document and the code disagree on the sign convention of the skill's signature derived metric. avg_pt_cut has no zero-division guard, and the module ships with no unit tests of any kind.",
  evidence: "Executed (Verified): python3 quant_helpers.py reproduces every documented target — revenue delta −0.64B (−0.50%), EPS delta −0.90 (−29.80%), alpha −11.1pp, capex/OCF 121.4%, average PT cut −13.7%, waterfall sum 12.6 — and prints \u201cOCF shortfall: +10.10B\u201d against formulas.md's −10.10B. The arithmetic identity is unambiguous: (−2.70 + 55.09) − 42.29 = +10.10.",
  impact: "Under the SR 11-7 analogy this is untested model code inside a research pipeline: regressions ship silently, and a junior analyst following formulas.md states a negative shortfall (or the sign silently flips between documentation and tool). The other skill's audit script demonstrates the correct pattern — an asserting self-test — so the repo already contains the fix as a template.",
  fix: "Convert the __main__ block to an asserting self-test in the fact_base_audit.py style; correct the formulas.md example or define the sign convention in both places in one sentence; add pytest coverage including consensus=0, old_pt=0, empty inputs and rounding boundaries.",
  confidence: "Verified (executed).",
}});

blocks.push({ finding: {
  id: "M-5", title: "Skill 2's quality bar is unenforced prose — no gates, templates or references ship", short: "Skill 2 quality bar is unenforced prose",
  severity: "Medium",
  location: "big-tech-earnings-postmortem/ — a single SKILL.md, no scripts/, templates/ or references/",
  description: "Skill 2's quality gates — \u201cFCF is computed, not copied\u201d, \u201ca verification ledger exists with 10+ load-bearing claims\u201d, \u201cno fabricated numbers\u201d — have no executable counterpart, unlike skill 1's two audit scripts, and not even a static template: skill 3 ships an evidence-ledger template that skill 2 reimplements in prose.",
  evidence: "File-tree verification (Verified): one file, 283 lines, zero supporting artifacts.",
  impact: "The same user request routed to skill 2 yields a deliverable with materially weaker guarantees than routing to skill 1, for identical inputs. The gap between claimed rigor and enforceable rigor is exactly what a research-controls function measures.",
  fix: "Either port the fact-base and audit-gate pattern into skill 2 (or have its Phase-equivalent explicitly invoke skill 1's scripts), or demote skill 2 in its own description to a lightweight fast path with the limitations stated; reuse skill 3's evidence-ledger template rather than restating it.",
  confidence: "Verified (file tree).",
}});

blocks.push({ finding: {
  id: "M-6", title: "Routing overlap: three skills claim the same trigger space, and the catalog indexes none of them", short: "Routing overlap; catalog indexes none",
  severity: "Medium",
  location: "The three SKILL.md descriptions; skills/skills-catalog.md and skills-inventory.md (repository discovery layer)",
  description: "All three descriptions trigger on variants of \u201cwhy did big-tech X move after earnings\u201d: skill 1 (\u201cUse when asked why a stock moved, to run a root-cause analysis (RCA) on a price event\u201d), skill 2 (\u201cUse when the user asks why a big-tech stock moved sharply after earnings\u201d), skill 3 (\u201cUse when asked to explain a stock-price event (post-earnings move, guidance shock, regulatory action)\u201d). None of the three references the others. Meanwhile the repository's catalog — which the README designates as the routing entry point — contains no entry for any of the three skills (case-insensitive search over both catalog files).",
  evidence: "Frontmatter text and catalog greps (Verified).",
  impact: "Skill selection for the highest-value research request in the library is nondeterministic, and the catalog routing layer would never surface the skills at all. Three deliverable formats (15-page deck, 7-section HTML, 13-section note) for one question family multiplies maintenance surface — which is precisely where the drift in M-2, M-3 and H-1 already shows.",
  fix: "Demarcate the three in their descriptions (deck-with-audit-gates vs lightweight post-mortem vs quantified-note), cross-reference each other explicitly, and register all three in skills-catalog.md with a note that the catalog must be regenerated when skills land.",
  confidence: "Verified.",
}});

blocks.push({ finding: {
  id: "M-7", title: "Playwright dependency is implicit and environment-coupled", short: "Implicit, environment-coupled Playwright dependency",
  severity: "Medium",
  location: "overflow_audit.mjs loadPlaywright() — fallback resolution bases include the hardcoded absolute paths /home/z/my-project and /home/z/my-project/scripts; repository package.json (no playwright); SKILL.md Phase 10 (prerequisite unstated)",
  description: "The render audit resolves Playwright from the working directory, the script's own directory, or two machine-specific absolute paths. Playwright is absent from the repository's dependencies, and the skill text never states the install prerequisite — the script merely prints an install hint after failing.",
  evidence: "Code inspection plus execution (Verified): the script ran in this audit environment only because the auditor's sandbox happens to match one of the two hardcoded paths; the repository itself has no node_modules and no playwright dependency entry.",
  impact: "The Definition-of-Done line \u201cboth audit scripts exit clean\u201d is unverifiable in a fresh clone, and shipped skill code contains author-machine absolute paths — a portability smell that will surface as an environment error (exit 2) for most users on first use.",
  fix: "State the prerequisite in SKILL.md Phase 10 and the Bundled-resources table (npm install playwright && npx playwright install chromium); resolve from the working directory and a documented relative location only; remove the absolute paths.",
  confidence: "Verified (code read; behavior observed).",
}});

blocks.push({ h2: "3.3 Low-severity findings" });

blocks.push({ finding: {
  id: "L-1", title: "Packaging and frontmatter drift across the three skills", short: "Packaging and frontmatter drift", severity: "Low",
  location: "Folder structure and YAML frontmatter of the three skills",
  description: "Skill 1 uses references/ + assets/ + scripts/; skill 3 uses reference/ + templates/ + scripts/; skill 2 ships no subdirectories. Frontmatter keys are inconsistent: skill 1 carries name and description only; skill 2 adds license and a non-standard compatibility key; skill 3 adds version — none matches the repository spec's full optional set (license / author / version), and only skill 2 declares any license.",
  evidence: "Directory listing and frontmatter parsing (Verified): description lengths 602 / 607 / 539 characters — all within the 1024-character limit, and all three names match their folders, so spec compliance in the narrow sense holds.",
  impact: "Discoverability and tooling assumptions suffer; the license asymmetry feeds L-2.",
  fix: "Standardize on one folder convention and one full frontmatter set across the three skills.",
  confidence: "Verified.",
}});

blocks.push({ finding: {
  id: "L-2", title: "No root LICENSE in a 340-skill public repository", short: "No root LICENSE", severity: "Low",
  location: "Repository root (no LICENSE file); skill 2 frontmatter (Apache 2.0)",
  description: "The repository ships skills publicly with no top-level license; the only declaration in scope is skill 2's Apache 2.0, which does not cover skills 1 and 3 whose content includes substantial original methodology and code.",
  evidence: "Filesystem check (Verified).",
  impact: "Redistribution terms for the audited skills are ambiguous — a licensing reviewer would flag it before any institutional reuse of the methodology.",
  fix: "Add a root LICENSE and per-skill license fields; state whether the Apache 2.0 declaration on skill 2 was intended repo-wide.",
  confidence: "Verified.",
}});

blocks.push({ finding: {
  id: "L-3", title: "formulas.md markdown defect and a circular market-cap pair", short: "Markdown defect; circular market-cap pair", severity: "Low",
  location: "bigtech-equity-research/reference/formulas.md, \u201cMarket cap\u201d section (lines 66–73)",
  description: "A stray closing code fence causes the trailing sentence (\u201cRun the math with scripts/quant_helpers.py to avoid arithmetic errors.\u201d) to render inside a code block. The section's two formulas are also mutual inverses (market-cap-erased = pre-print cap × |move|; pre-print cap ≈ erased / |move|) — a bounding identity rather than a computation recipe — whereas skill 1's methodology prefers shares-outstanding × Δprice (sourced from the 10-Q cover) and explicitly labels the percentage method an approximation.",
  evidence: "File content (Verified).",
  impact: "Rendering noise in a reference file, and an inverted priority on market-cap arithmetic relative to the sibling skill's stronger doctrine.",
  fix: "Repair the fence; replace the circular pair with the shares × Δprice formula and keep the percentage method as the labeled cross-check.",
  confidence: "Verified.",
}});

blocks.push({ finding: {
  id: "L-4", title: "Placeholder scan runs on raw HTML including script and style blocks", short: "Placeholder scan reads script and style blocks", severity: "Low",
  location: "fact_base_audit.py scan_placeholders() — normalizes the raw file, not visible text",
  description: "The fact-presence checks strip <script>/<style> and tags before matching, but the placeholder scan matches against the full raw HTML, so a CSS class named placeholder-bar or the JavaScript token undefined inside a script triggers failures on content readers never see.",
  evidence: "Executed (Verified): a probe slide whose visible text was clean produced \u201cPLACEHOLDER … matches /placeholder/\u201d and \u201cmatches /\\bundefined\\b/\u201d from its style and script blocks. A related dead-code observation: in checks mode, covered.update() adds needle strings in a format the candidate suppressor never consults.",
  impact: "False positives on code-bearing decks; the scan errs safe but noisy.",
  fix: "Run the placeholder patterns against visible_text() output only; remove or repair the dead covered.update() in checks mode.",
  confidence: "Verified (executed).",
}});

blocks.push({ finding: {
  id: "L-5", title: "Evidence-ledger cites a phase that does not exist", short: "Evidence ledger cites a nonexistent phase", severity: "Low",
  location: "bigtech-equity-research/templates/evidence-ledger.md, Table 2 (\u201cForward P/E vs band | 11\u201d)",
  description: "The Data-Gap ledger's Phase column cites \u201c11\u201d for the forward-P/E gap, but skill 3's methodology defines seven phases; 11 is a deliverable section number in report-structure.md, not a phase.",
  evidence: "File comparison across the three skill-3 files (Verified).",
  impact: "Minor cross-reference confusion for the executing agent at exactly the moment it is deciding what to re-pull.",
  fix: "Relabel the column or the value (\u201cDeliverable section 11\u201d).",
  confidence: "Verified.",
}});

blocks.push({ finding: {
  id: "L-6", title: "Embedded sell-side specifics could not be verified externally", short: "Embedded sell-side specifics unverifiable", severity: "Low",
  location: "analyzing-us-bigtech-stocks/references/methodology.md — Citizens JMP downgrade, Wedbush PT $445→$387, FactSet consensus $426.20→$404.63 across 61 analysts, BofA Search-at-~10x comparison",
  description: "The worked example asserts specific named analyst actions and a consensus price-target path as facts from the October 2026 engagement. This audit could not verify them externally within its time box; the surrounding fundamentals in the same worked example (close, FCF, EPS, OCF, Cloud, macro prints) did verify, so these are unverified-by-audit rather than presumed false.",
  evidence: "External searches returned the event coverage but not these specific action details (Reasoned / Assumed).",
  impact: "If any specific is wrong, the skill teaches fabrication by example; if all are right, they rot silently as the example ages.",
  fix: "Move worked-example specifics into a dated, source-linked appendix (URL + retrieval date each), or mark them illustrative; the fact-base schema the skill itself defines already models the right pattern.",
  confidence: "Assumed (could not be verified or falsified).",
}});

blocks.push({ h2: "3.4 Informational observations" });

blocks.push({ finding: {
  id: "I-1", title: "No MNPI / Regulation FD statement in any of the three skills", short: "No MNPI / Reg FD statement", severity: "Informational",
  location: "All three SKILL.md files",
  description: "All three skills effectively restrict sourcing to public materials through their tier hierarchies, but none states the compliance principle that only public information is used and material non-public information is out of scope.",
  evidence: "Full-text reads (Verified — absence).",
  impact: "A research-controls review under the Wall Street framing of the engagement brief would require the statement, even for an agent tool.",
  fix: "One sentence in each SKILL.md (\u201cpublic sources only; if you are in possession of material non-public information, stop\u201d), ideally in the shared standard file proposed under M-3.",
  confidence: "Verified (absence).",
}});

blocks.push({ finding: {
  id: "I-2", title: "Skill 3 lacks an explicit GAAP-to-non-GAAP reconciliation phase", short: "No explicit GAAP-to-non-GAAP phase", severity: "Informational",
  location: "bigtech-equity-research/reference/methodology.md (Phases 1–7) and templates/report-structure.md",
  description: "One-time items appear in skill 3 only inside the Phase 7 waterfall; there is no bridge step. Skills 1 and 2 mandate bridges — skill 2's cash/non-cash × recurring/one-time × dilution classification is the strongest treatment of the three, and skill 1 requires the ex-item arithmetic on the slide.",
  evidence: "Methodology comparison (Verified).",
  impact: "An Item 10(e)-style reviewer would ask where the reconciliation lives for skill 3 outputs.",
  fix: "Add a bridge requirement to Phase 4 or a dedicated section in the report template.",
  confidence: "Verified.",
}});

blocks.push({ finding: {
  id: "I-3", title: "Consensus-vendor attribution varies", short: "Consensus-vendor attribution varies", severity: "Informational",
  location: "Skill 1 methodology §2.3 (requires naming the outlet); skill 3 formulas.md worked examples (bare \u201cconsensus\u201d)",
  description: "The audit's own external checks illustrate the stakes: Yahoo's S&P-analyst consensus for Alphabet Q3 2026 revenue was $127.9B (\u201cin line\u201d) while the skills cite $128.2B/$128.22B (miss) — plausibly different vendors, materially different surprise framing. Skill 1 already requires outlet attribution; skill 3's examples do not model it.",
  evidence: "Yahoo Finance versus the two skills' figures (Verified).",
  impact: "Unattributed consensus is unreproducible consensus — the first thing a research-controls reviewer asks.",
  fix: "Require vendor + as-of date on every consensus figure; make skill 3's worked examples carry the attribution skill 1 already mandates.",
  confidence: "Verified.",
}});

module.exports = { blocks };
