# Validation Report rev7 — independent re-audit (dual-pin)

> **Status: superseded by revision 8.** This report records the rev7 audit of
> commit `4016d922` (delivered `a0e0aaa0`). See
> `docs/validation_record_current.json` (revision 8) and the remediation notes
> in that record for the corrections applied after this audit. This file
> replaces a previously committed raw chat transcript that had been saved here
> by mistake; the audit evidence below is the same content, restructured.

## Scope

- **Rubric A** — re-confirm the rev6 Verified verdict at pin `32084a2f`.
- **Rubric B** — extend Verified to HEAD `4016d922` (the rev6 delivery commit).
- Method: pinned exports (head / pin / parent), pinned tool versions, gates
  R1–R7, red→green guards, provenance hashing, three-way adjudication of
  rev5 ↔ rev6 ↔ JSON record.

## Verdicts

| Rubric | Result | Basis |
|---|---|---|
| A — re-confirm at `32084a2f` | **PASS** | 27/27 pin hashes match JSON record and rev6 appendix; lint exit 0; 101/101 ×3 |
| B — extend to `4016d922` | **PASS** | 30/30 HEAD manifest; drift = 4 commit-explained entries; gates identical |

No new High/Medium skill defect was found by the rev7 audit itself.

## Gates (executed at both pins unless noted)

| Gate | Pin (`32084a2f`) | HEAD (`4016d922`) |
|---|---|---|
| Provenance | 27/27 vs JSON + rev6 App. A; 27/27 tree↔disk | 30/30; drift = 4 commit-explained entries |
| R1 lint | exit 0, 149 lines | exit 0, 149 lines (parent fails: missing PDF) |
| R2 suite | 101 collected, 101 passed ×3, 0 skips | identical ×3 |
| R3 example | 7/7, checks_sha256 `18c1a7f6…`, full match | identical |
| R4 ingest | 4/24 pages subset, G0 PASS, pdf sha `c5873a17…` | identical |
| R5 negatives | exit battery (2/2/…/3), no traceback; heavy probes ERROR/exit 1 | scripts byte-identical; key probes re-run |
| R6 playbook | 4× 2/2 (eigen / inverse / tangency / antiderivative) | identical |
| R7 root | — | 390 passed, 9 skipped (rev5's "≠390/9" refuted) |
| Red→green | 4 guards red on parent scripts → 5 green at HEAD; parent 2 failed / 95 passed | — |

PDF blob `e69a127e…` identical at `3d9c8bfe` / `32084a2f` / HEAD; absent at
`0f17edb4` / `7c5cc0b8` (bulk cleanup; A-3 / N-5 closed). Commit scope of
`4016d922`: SKILL.md tree line + 3 docs only.

## Candidate findings adjudicated during rev7

| ID | Disposition | Evidence |
|---|---|---|
| D-a JSON escape-loss | Refuted (fix string) / new Low (evidence string) | Raw bytes carry correct backslashes; rendering layers, not the file, dropped them |
| D-b promotionSupersededBy missing | Confirmed | Absent from rev6 record; historical `validation_report.json` still says `promotableToVerified: true` |
| D-c rev5 banner | Confirmed | Opens with conversational preamble; no disposition/supersession banner |
| D-d R5 schema | Confirmed | JSON values are exit codes (10 keys) vs rev6's 11 probe rows; schema undocumented |
| D-e coverage/currency | Confirmed | 3 new docs had no hash baseline; record pinned to `32084a2f` |
| D-f mirrors stale | Confirmed | `skills-inventory.md` / `docs/skills-inventory.md` said Files: 26 (actual 30) |

## Additional findings (non-blocking, from the rev7 audit)

- **Low — N-9 disposition corrected:** `--pages 1,1` yields `[(1,1),(1,1)]`
  from `parse_pages`, but the ingest loop is page-keyed, so `pages_ingested = 1`;
  "page extracted twice" was refuted.
- N-4, N-6, N-7, N-8, N-10, N-11, N-1 all reproduced unchanged; security
  caps/reject battery held (eye 64/65, factorial 10 000/10 001, seq 4096/4097,
  `2**1000`/1001, attributes/subscripts/lambdas/comprehensions/dunders/
  strings/complex/booleans all rejected).
- Residual risks (unchanged): Windows SIGALRM gap; heavy-SymPy bounded only by
  per-check timeout; heuristic lint; non-atomic PNG writes; partial text on
  exit 2; paper ↔ model-answer mathematics stays Reported.

## Handoff — Verified / Deferred

**Verified:** both rubric verdicts, all gates at both pins, red→green guards,
security contracts, adjudication table.

**Deferred (carried into rev8 remediation):** record repairs (D-a evidence
string, D-b…D-e), inventory regeneration (D-f), optional N-1/N-4/N-6…N-11
fixes.

## Erratum (recorded at rev8 remediation)

The original rev7 delivery claimed "post-edit lint 31/31, suite 101/101" but
the accompanying commit `a0e0aaa0` added 7 files (6 `docs/audit/*.py` harnesses
plus this report) without adding them to the SKILL.md tree, so lint actually
**failed** at the delivered tree (7 unlisted-file errors; 2 dependent test
failures). Commit `a0e0aaa0` also committed 5 `__pycache__` `.pyc` artifacts.
Both were corrected in the rev8 remediation; see
`docs/validation_record_current.json` revision 8.
