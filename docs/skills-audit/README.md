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

## Round-3 remediation — validated against comparative analysis reports 6/7

A third remediation round was planned and executed after validating the two
later comparative reports (`docs/comparative_analysis_report-6.md`, `-7.md`).
Report 7's Part-D merged finding set (union of its own audit and report 6's
synthesized roadmap, re-ranked) was the acceptance list; report 6's regulatory
correction (Reg AC / FINRA 2241 apply to distributed sell-side research, not
internal buy-side IC memos — conflict disclosure *is* still required under
CFA Institute Standard I(B) / Advisers Act fiduciary duty) was adopted as the
compliance framing.

| Round-3 item (source finding) | Status | Where |
| --- | --- | --- |
| SHA-256 provenance sealing + tamper-evident verification (R6/R7 C-2) | Landed | `scripts/provenance_seal.py` vendored byte-identical ×3; seal line embedded next to the verification-status line; `provenance.json` sidecar; `--verify` re-check |
| Buy-side position & mandate disclosure (R6 synth-2 / R7 C-1+M-4, regime-corrected) | Landed | `meta.mandate_context` (`fund_position`, `position_as_of`) enforced by the MANDATE schema gate when `meta.audience` names an IC; "Fund position:" conditional needles in both lite skills; doctrine in all three SKILL.md compliance sections |
| Consensus sourcing & vintage enforcement (R6 synth-3 / R7 H-1) | Landed | `consensus_provider` / `consensus_vintage` / `contributor_count` schema fields + always-on CONSENSUS gate (T1/T2 tier, `--consensus-max-age-days`, default 10); doctrine in methodology §2.3, skill-3 Phase 1, skill-2 Step 2 |
| Epistemic taxonomy split — `Reasoned (derived)` vs `Reasoned (judged)` (R6 synth-4 / R7 H-2) | Landed | `epistemic_kind` schema field + always-on EPISTEMIC gate (derived requires formula); taxonomy rewritten in sourcing-and-confidence.md, fact-base-schema.md §3, postmortem-framework §2, all three SKILL.md |
| Waterfall sum-to-move identity mechanically enforced (R7 H-2b) | Landed | always-on WATERFALL gate on facts carrying `weights` + `realized_move`; `quant_helpers.waterfall_check` remains the helper-side check |
| Segment-map staleness gate — advisory → fail-safe (R6 synth-5 / R7 H-3) | Landed | machine-readable `reference/segment-maps.json` + `scripts/segment_map_check.py` (fails the build when the filing postdates `verified_through`; unknown ticker → filing-note extraction path); SKILL.md hard rule 9; doctrine: the filing's own ASC 280 segment note is the source of truth, the map is the cached baseline |
| Lite number registry for skill 2 (R6 synth-10 / R7 H-4/H-5) | Landed | `assets/fact_base_lite.template.json` + `scripts/fact_base_lite_audit.py` (forward presence, reverse UNREGISTERED failures, schema/source-field checks, furniture whitelist) — the lite note's numbers are now machine-checked |
| Canonical default beta window (R6 synth-6 / R7 H-2β) | Landed | `DEFAULT_BETA_WINDOW` = 2-year monthly returns vs QQQ; `abnormal_return` applies it when beta is supplied without a window and echoes the source (`canonical default` / `explicit`); override requires documented justification |
| Scoped disclosure needles (R7 M-2) | Landed | `note_audit.py` `required_if` entries accept `near`/`within` — the qualifying label must sit adjacent to the content it qualifies (SCOPED failure otherwise); both lite checks.json rewritten with scoped waterfall/beta/VRP/position needles |
| `--strict-pages` (R7 M-1) | Landed | unverified candidates on named decision-critical pages become failures; furniture elsewhere stays advisory |
| Options implied-move sourcing + VRP caveat (R6 synth-7 / R7 M-3) | Landed | ATM straddle computed from the T-1 closing chain (never a news-quoted percentage); volatility-risk-premium caveat scoped needle; `implied_move` doctrine in formulas.md + methodology Phase 2/pre-event mode |
| FCF ex-SBC mandatory pairing (R6 synth-8 / R7 L-1) | Landed | `quant_helpers.fcf` / `fcf_ex_sbc`; paired reconciliation row doctrine in skill-2 Step 2, skill-3 Phase 4, postmortem-framework §8, formulas.md |
| Canonical peer baskets (R6 synth-9 / R7 M-4) | Landed | `reference/peers.md` (selection criteria + default baskets, TSLA axis note); wired into skill-2 Step 4, skill-3 Phase 5 |
| Accessibility gate (R7 M-5/M-6) | Landed | `scripts/a11y_audit.mjs` vendored ×3 — lang, heading order, image alt, WCAG 2.2 AA contrast (4.5:1 / 3:1 large); the templates' WCAG-AA claim is now enforced, not asserted |
| `quant_helpers` coverage: segment variance (R7 L-4) | Landed | `segment_variance(actual, consensus, prior_q, year_ago_q)` → delta/QoQ/YoY row |
| Family version parity 1.4.0 (R7 L-1) | Landed | all three SKILL.md + both inventory copies |

Rejected again (with reasoning): sell-side Reg AC / FINRA 2241 certification
module and supervisory-approval stamps (regime misapplication — the family's
standing internal-buy-side scoping; conflict disclosure implemented instead,
per report 6's own correction of report 7's C-1); WORM archival / retention
scheduling / firm-key signing (operational infrastructure beyond skill scope —
SHA-256 sealing is the in-scope core); a DCF/SOTP valuation skill (the
valuation-boundary doctrine stands).

The regression suite grew from 6 to 10 files (247 tests): the round-3 gates
carry dedicated test modules (`test_provenance_seal.py`,
`test_segment_map_check.py`, `test_fact_base_lite_audit.py`,
`test_a11y_audit.py`), and `test_repo_consistency.py` gained
`TestDoctrineGuardsRound3` (vendoring parity ×3, wiring, doctrine presence,
family version parity). The vendored `provenance_seal.py` and `a11y_audit.mjs`
copies are byte-identical across the three skills, guarded by tests.

## Round-4 remediation — validated against comparative analysis reports 8/9

A fourth remediation round was planned and executed after validating the two
later comparative reports (`docs/comparative_analysis_report-8.md`, `-9.md`).
Report 9's reconciled master audit (its unified finding set: 2 Critical /
6 High / 8 Medium / 4 Low) was the acceptance list, with report 9's own
corrections applied to report 8's findings: the MNPI temporal gate was
re-scoped as a **data-integrity control** (not Reg FD — Reg FD binds issuers,
10b-5 attaches to trading) with a `data_type` discriminator (report 8's
original fix would have wrongly stripped legitimate pre-event inputs), the
peer-basket fix was re-scoped to per-constituent corporate-action checks (an
index-membership API is the wrong control for bespoke analyst baskets), and
the EV-sizing finding was elevated from Informational to High (H-6).

| Round-4 item (source finding) | Status | Where |
| --- | --- | --- |
| Machine-checked number registry for skill 3 (R8/R9 H-2 — "the most surprising inconsistency in the family") | Landed | `fact_base_lite_audit.py` + `fact_base_lite.template.json` vendored byte-identical into `bigtech-equity-research`; wired into SKILL.md hard rule 10, workflow step 8, delivery gates, Definition of Done |
| Event-window rule — T+0 vs T+1 (R8/R9 H-3) | Landed | after-close → T+1 close; pre-market/intraday → T+0 close; stated in the event charter (`meta.reaction_definition`); doctrine in all three SKILL.md + methodology §1/§2 + skill-3 hard rule 12 |
| Multi-class market-cap delta (R8/R9 H-4) | Landed | `quant_helpers.market_cap_delta` (per-class sum, method echoed); doctrine family-wide + formulas.md §Market cap + methodology §2.2 |
| Expected Fundamental Value matrix (R8/R9 H-6, elevated from Informational) | Landed | optional-for-IC scenario probability weighting on *fundamental* outcomes, EV-adjusted range computed in code, `Reasoned (judged)`, strictly never a price target; doctrine in all three SKILL.md + methodology §9 / Phase 7 / postmortem-framework §7 / report-structure §12 |
| Consensus vintage tightened + mean/median recorded (R8/R9 M-1) | Landed | `--consensus-max-age-days` default 10 → 5 calendar days ≈ 3 trading days; `consensus_statistic` (mean/median/undisclosed) now a required field in the flagship CONSENSUS gate, the lite CONSENSUS check, both lite templates, and the fact-base schema |
| Reg G / Item 10(e) non-GAAP reconciliation (R8/R9 M-2) | Landed | checklist doctrine: every non-GAAP metric reconciled to its most directly comparable GAAP measure (bridge shown or issuer's table cited) + beat/miss basis stated; family-wide + methodology §7 / Phase 4 |
| Public-source-only limitation (R8/R9 M-3) | Landed | stated limitation on every deliverable; **required needle** in both lite `checks.json` ("Public-source-only"); doctrine in all three SKILL.md |
| Data licensing / redistribution (R8/R9 M-4) | Landed | doctrine: vendor figures cited with attribution for internal analytical use; no at-scale reproduction of vendor tables; no external redistribution (rights belong to licensed feeds); family-wide compliance sections |
| Postmortem standalone arithmetic (R8/R9 M-5) | Landed | `quant_helpers.py` vendored byte-identical ×3 (canonical copy in skill 3); SKILL.md references now point at the bundled copy; byte-identity guarded by tests |
| Temporal embargo — pre-filing contamination gate (R8/R9 M-6, report-9-corrected design) | Landed | `meta.t1_filing_timestamp` pins the verified T1 filing time; every fact declares `data_type` `pre_event_input`/`post_event_fact`; post-event facts must be retrieved at/after the filing time — TEMPORAL gate in `fact_base_audit.py` + lite TEMPORAL check in `fact_base_lite_audit.py` (selftests + unit tests both); pre-event inputs exempt by design; date-only retrieval on the filing date is a precision NOTE |
| Beta regime diagnostics (R8/R9 M-7) | Landed | `quant_helpers.beta_diagnostics` (OLS beta + R² + `correlation_breakdown` at `R_SQUARED_FLOOR` 0.30) and `volatility_regime_flag` (trailing-vol z-score vs 2-year mean at threshold 2.0); R² < 0.30 or \|z\| > 2 → justify the canonical window or re-estimate shorter; doctrine family-wide + formulas.md + methodology Phase 2 |
| Peer-basket constituent hygiene (R8/R9 M-8, report-9-corrected fix) | Landed | `peers.md` §Constituent hygiene: per-named-constituent corporate-action check (T2 news sweep — not an index API) + cache-age gate (>90 days or undated → re-verify); doctrine family-wide; DoD checklists pin it |
| Microstructure lens (R8/R9 L-4) | Landed | flagship hypothesis-tree lens (i) Market Microstructure & Flow (dealer gamma, CTA unwinds, index rebalances) + conditional pre-event options-OI/skew amplifier input (when sourced; Data-Gap ledger otherwise); methodology §3/§4; template lens enum |
| C-1 scope hardening, buy-side option (a) (R9 C-1) | Landed | "not a research report" legend + internal-use-only distribution control (no client/external distribution without compliance sign-off) — legend is a **required needle** in both lite checks.json; IC pre-read firewall stated family-wide |
| Variant-view annex (R9 H-1, in-scope subset) | Landed | optional own-estimates annex with an explicit assumption table + consensus bridge (own − consensus per line), all inputs `Assumed`/`Reasoned (judged)`; forecast gap named in open items when not commissioned |
| Methodology validation protocol (R9 H-5, documented) | Landed (protocol) | `references/methodology.md` §15: validation set → blind re-run (cutoff discipline) → hit-rate scoring → published accuracy note → re-validation cadence; "face validity only" disclaimer until the harness exists |
| Dependency minimums (R9 L-3, partial) | Landed | `compatibility:` frontmatter now declares Python ≥ 3.9 / Node ≥ 18 / Playwright ≥ 1.40 minimums in all three skills |
| Family version parity 1.5.0 | Landed | all three SKILL.md + both inventory copies |

Rejected (with reasoning, per the standing round-2/3 positions and report 9's
own regime corrections): the full sell-side compliance module / Reg AC /
FINRA 2241 / supervisory sign-off (regime misapplication — these attach to
distributed sell-side research; scope hardening option (a) implemented
instead); the full valuation/recommendation/position-sizing module (the
family's standing causal-attribution scoping; the H-6 EV fundamental matrix +
variant-view annex + firewall language are the in-scope subsets); WORM/17a-4
archival and firm-key signing (operational infrastructure beyond skill scope);
index-membership APIs for peer baskets (report 9's own correction — bespoke
baskets need per-constituent checks); SKILL.md router-only restructuring (L-1 —
surgical patches preferred this round; noted for a future round).

The regression suite grew from 247 to **337 tests** across the same 10 files:
the round-4 gates carry new unit tests (TEMPORAL gate in
`test_fact_base_audit.py`, lite CONSENSUS/TEMPORAL + vendoring parity in
`test_fact_base_lite_audit.py`, beta diagnostics + multi-class cap delta +
×3 byte-identity in `test_quant_helpers.py`, legend needles in
`test_note_audit.py`), and `test_repo_consistency.py` gained
`TestDoctrineGuardsRound4` (~40 doctrine guards: registry vendoring,
event-window rule, multi-class cap, EV matrix, consensus statistic, Reg G,
legends, licensing, temporal embargo, beta diagnostics, peer hygiene,
microstructure lens, validation protocol).

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
