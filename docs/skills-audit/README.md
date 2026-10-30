# Skills Audit — Big-Tech Equity Research Skills (2026-10-30)

Independent **Mode C audit** (review without modifying the audited code) of the three
big-tech research skills in this repository, evaluated against the standards expected
of major investment banks and institutional fund managers:

| Skill | Directory | Rubric score (0–5) |
| --- | --- | --- |
| Skill 1 — RCA deck with audit gates | `skills/analyzing-us-bigtech-stocks/` | **4.45** |
| Skill 2 — single-file post-mortem methodology | `skills/big-tech-earnings-postmortem/` | **2.85** |
| Skill 3 — quantified research note | `skills/bigtech-equity-research/` | **3.00** |

**Verdict:** none of the three passes a full bulge-bracket research-controls review as
shipped; skill 1 is genuinely close. The standards applied combine CFA Institute Code &
Standards (diligence, fact-vs-opinion), SEC Reg S-K Item 10(e) non-GAAP discipline,
FINRA Rule 2241 research-report norms, Reg FD/MNPI hygiene, SR 11-7-style model
governance, and ASC 280 segment comparability.

## Findings summary — 20 total (0 Critical / 4 High / 7 Medium / 6 Low / 3 Informational)

High-severity findings:

- **H-1** Conflicting "verified" figures for the same real event (Alphabet Q3 2026
  sell-off) across skills — no single source of truth.
- **H-2** `big-tech-earnings-postmortem` promises "institutional-grade" deliverables
  but contains no disclaimer language anywhere.
- **H-3** `bigtech-equity-research/reference/segment-maps.md` misstates ASC 280
  reportable segments for three of seven companies (Nvidia, Amazon, Apple), verified
  against the FY2025/FY2026 10-Ks.
- **H-4** `fact_base_audit.py` uses unanchored substring matching, so the numeric
  audit gate silently passes absent numbers (reproducible via `evidence/`).

Full details, evidence, impact and recommended fixes: the report itself.

## Contents

- `BigTech_Research_Skills_Audit_Report.docx` — the audit report (36 pp. rendered;
  cover, TOC, 9 sections, 30 tables, 1 figure, 20 finding records).
- `BigTech_Research_Skills_Audit_Report.pdf` — rendered copy.
- `report-generator/` — toolchain that builds the report from content modules
  (`report_content_1.js`, `report_content_2.js`). Audited repo state: HEAD `48cd3f97`.
- `evidence/` — executable evidence for finding H-4: negative tests demonstrating the
  false-PASS hole in `fact_base_audit.py`.

The audited skills themselves are untouched (audit discipline: findings are reported,
not silently fixed).

## Regenerating the report

Requires Node.js ≥ 18 with the `docx` npm package (v9.x) resolvable from
`report-generator/`, and Python 3 with `matplotlib`/`numpy` for the figure:

```bash
cd docs/skills-audit/report-generator
npm install                # optional if docx@9 is already resolvable
python3 make_rubric_heatmap.py                     # rebuild assets/rubric_heatmap.png
node generate_audit_report.js                      # writes ../BigTech_Research_Skills_Audit_Report.docx
python3 postprocess_footers.py ../BigTech_Research_Skills_Audit_Report.docx
python3 verify_audit_docx.py                       # 8 postcheck assertions
```

`report-generator/package.json` declares `"type": "commonjs"` because the repo root
manifest sets `"type": "module"`.

Reproduce finding H-4 from the repo root:

```bash
python3 docs/skills-audit/evidence/test_fact_base_audit_falsepass.py
```

## Audit evidence basis

All 17 in-scope files were read in full; all three shipped scripts
(`fact_base_audit.py`, `overflow_audit.mjs`, `quant_helpers.py`) were executed against
positive and negative cases; the skills' embedded "verified" facts were tested against
external sources (SEC filings, Bloomberg, Reuters, WSJ, Yahoo Finance). Every material
claim in the report carries a confidence tag (Verified / Reasoned / Assumed), and
Section 6 is a verification ledger of the checks performed.

*Informational audit prepared by an automated coding-specialist agent — not
investment advice.*
