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

## Remediation status

The audit itself was Mode C (report, don't modify). Remediation landed on
`main` afterwards, in dependency order — every item verifiable with the checks
recorded in the report's Section 6:

| Roadmap item | Status | Where |
| --- | --- | --- |
| P0 — segment-map restructure (H-3) | Landed | `c0326fde` |
| P0 — skill 2 disclaimer + source tiers (H-2, I-1) | Landed | `5c3b251e` |
| P0 — boundary-anchored matcher + selftest (H-4) | Landed | `ff4b9809` |
| P0 — worked-example reconciliation (H-1) | Landed | `c0326fde`, `f3ee290f` |
| P1/P2 — taxonomy, attribution, WCAG, compliance framing (M-2, M-3) | Landed | `f3ee290f`, `5c3b251e`, `c0326fde` |
| P1 — catalog registration (M-6) | Landed | `3f11c28b` |
| **P1 — regression tests wired into CI** (deferred) | **Landed** | `tests/` + `.github/workflows/ci.yml` (`c9e25004`) |
| **P2 — skill 2's framework folded into skill 1 as a methodology reference** (deferred) | **Landed** | `skills/analyzing-us-bigtech-stocks/references/postmortem-framework.md` (`92f9c7bc`) |

The regression suite runs on every push and pull request to `main`: unit
regressions for the H-4 matcher, the M-4 quant helpers (including doc/code
agreement), and the M-1/M-7 render audit, plus the repository-level consistency
test (H-1/H-2/M-2/M-3/M-6/L-1 recurrence and the fold-in wiring).

## Round-2 remediation — validated against comparative analysis reports 3/4/5

A second remediation round was planned and executed after validating the three
later comparative reports (`docs/comparative_analysis_report-3.md`, `-4.md`,
`-5.md`). Findings were accepted or rejected explicitly (report 4's
claim-by-claim validation was used as the tiebreaker). During the round, the
CI workflow's `branches: [main]` triggers were base64-verified against HEAD
and the remote (a terminal-rendering artifact had initially made them look
corrupted) — the wiring is sound, and a regression test now pins it.

| Round-2 item (source finding) | Status | Where |
| --- | --- | --- |
| Lite audit gates vendored into skills 2 & 3 (R3-C1, R4 #2, R5 H-1) | Landed | `skills/{big-tech-earnings-postmortem,bigtech-equity-research}/scripts/note_audit.py` + `assets/checks.json` |
| Single-file render/overflow gate for the HTML notes (R3-H2, R4) | Landed | `scripts/note_overflow_audit.mjs` in both lite skills (byte-identical vendoring, consistency-tested) |
| Opt-in strict compliance modes for the numeric audit (R3-M2, R4 #3) | Landed | `fact_base_audit.py`: `--strict-verified`, `--fail-on-unverified`, `--decision-critical` / `meta.decision_critical` |
| One-command gate wrapper (R5 L-2) | Landed | `skills/analyzing-us-bigtech-stocks/scripts/audit_all.sh` (`STRICT=1` adds both strict flags) |
| Beta estimation-window disclosure enforced in code (R3-M1, R4 confirmed) | Landed | `quant_helpers.py::abnormal_return` (raises without `beta_window`; returns `{excess, convention, beta, beta_window}`) |
| `PERCENT_MULTIPLIER` constant replaces magic `100.0` (R3-L2) | Landed | `quant_helpers.py` |
| Segment-map versioning + staleness rule (R3 Phase-1, R4 #4) | Landed | `reference/segment-maps.md` (`segment_map_version`, `last_verified_against_filing`), methodology Phase 3, SKILL.md hard rule |
| Valuation-boundary statement in every deliverable (R3 Phase-1, R4 #1) | Landed | all three SKILL.md files, methodology §9, report-structure §11, evidence-ledger method note |
| Verification-status line on every cover (R4 #5) | Landed | report-design §4, slides_brief template, both lite SKILL.md files, note_audit needle |
| Descriptions aligned with actual verification backing (R4 #5) | Landed | all three SKILL.md frontmatter (skill 2 no longer overstates; no "no executable audit tooling") |
| Compute-don't-recall rule (R3 synthesized: in-context arithmetic vector) | Landed | golden rule 6 / hard rule 8 in all three SKILL.md files, pitfall 16 |
| Dedicated Risk Factors & Falsification section (R4 medium) | Landed | `templates/report-structure.md` — 13 → 14 sections |
| T1/T2/T3 tier boundaries explicit in the schema (R4 medium) | Landed | `references/fact-base-schema.md` §2.1 |
| Root LICENSE + license frontmatter standardization (R5 M-1) | Landed | `LICENSE` (Apache-2.0) + `license:`/`compatibility:` keys in all three SKILL.md |
| Waterfall-label enforcement (R5 M-3) | Landed | conditional needle in both `assets/checks.json` |
| CI trigger wiring pinned (`branches: [main]` on push/PR) | Verified — no fix needed | `.github/workflows/ci.yml` + `tests/test_repo_consistency.py::TestCIWiring` |

Rejected (with reasoning, per report 4's reconciliation): FINRA
forward-looking-statement disclaimer automation (regime misapplication — the
skills explicitly disclaim sell-side status); strict-by-default for the
unverified-candidate reverse check (heuristic — opt-in flags instead);
WORM-archiving/MCP-vendor integration (operational infrastructure beyond skill
scope); a valuation model (the boundary statement per report 4 instead of a
new DCF skill).

## Contents

- `BigTech_Research_Skills_Audit_Report.docx` — the audit report (36 pp. rendered;
  cover, TOC, 9 sections, 30 tables, 1 figure, 20 finding records).
- `BigTech_Research_Skills_Audit_Report.pdf` — rendered copy.
- `report-generator/` — toolchain that builds the report from content modules
  (`report_content_1.js`, `report_content_2.js`). Audited repo state: HEAD `48cd3f97`.
- `evidence/` — executable evidence for finding H-4: the negative tests that
  demonstrated the false-PASS hole in `fact_base_audit.py`. Post-fix the same
  harness asserts the hole stays closed (evasion cases must exit 1) and is
  wired into the regression suite.

The report documents the audited state at HEAD `48cd3f97`; the skills have
since been remediated on `main` as recorded above (audit discipline: findings
were reported first, fixes landed as separately verifiable commits).

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

Reproduce / regression-guard finding H-4 from the repo root (exits 0 only if
the substring-evasion cases stay closed):

```bash
python3 docs/skills-audit/evidence/test_fact_base_audit_falsepass.py
python3 -m pytest tests/ -v          # the full regression + consistency suite
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
