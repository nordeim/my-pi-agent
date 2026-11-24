# Pitfalls and lessons learnt (from live case work)

## Case study: 2026 ACJC H2 FM P1 Q6 (complex loci)
| # | Incident | Root cause | Rule |
|---|---|---|---|
| 1 | Question pasted without modulus bars/conjugates | PDF glyph loss | Reconstruct before solving (G1) |
| 2 | Printed form was a modulus-of-fraction | Orphan `1` ignored | Use the solution's first line as a decoding key |
| 3 | `3\|z−a\|` squared as `3(…)` | Scalar not squared | `(k\|w\|)² = k²\|w\|²` |
| 4 | arg measured from origin | Misread `arg(z−z_A)` | It is the direction of `AP`, from `A` |
| 5 | Half-angle added, not subtracted | Extremum confusion | Tangent directions are `arg(AC) ± α` |
| 6 | No principal-range check | Branch neglect | Prove both tangents lie in `(π/2, π)` |
| 7 | `a` assumed unique | Only `arg a` constrained | Separate fixed vs free parameters |
| 8 | Second tangent not rejected | Domain filter unused | `0 < arg a < π/2` kills the negative-gradient tangent |
| 9 | "O is in the second quadrant" | Point on an axis | Justify by the components of the vector |
| 10 | `O` used for the centre | Notation collision | Reserve `O` for origin, `C` for centre |
| 11 | Dangling "Hence," | Editing defect | Display every required result |
| 12 | Imported StackExchange figure | Provenance leak | Deliverables self-contained |
| 13 | "The multiplier is 3, not 3²" | Fabricated correction | Never invent defects in the user's input |
| 14 | "PDF verified" badge | Over-claimed evidence | Label reconstruction `Reasoned` |

## Meta-lessons
- **Correct answer ≠ correct reasoning.** Audit the justification, not only
  the boxed result; examiners award method marks.
- **Audit yourself symmetrically.** In the case above, the reviewed model
  answer had the *more faithful* transcription; self-audit caught it.
- **Two independent methods are cheap insurance.** Geometry gave `|w| = √7`;
  algebra gave `w = (3√14 + 7i)/5`; agreement is strong evidence.
- **Findings, not rewrites.** In AUDIT mode, classify and give minimal fixes;
  rewrite only when asked.

## Cross-topic error catalogue
Premature rounding; degrees/radians mismatch; lost `±` on square roots;
`ln` of a negative quantity; missing constant of integration; ignoring
initial conditions; matrix multiplication order; using `det = 0` without
checking independence; forgetting the Jacobian in substitution; unlabelled
sketches; missing units; incomplete case analysis in "all possible values".

## Round 2 — lessons from the independent skill audit
| Incident | Root cause | Rule |
|---|---|---|
| `sympify` executed a payload | convenience parser on untrusted text | whitelist AST interpreter; no eval anywhere |
| `0/0 checks passed`, exit 0 | no minimum-suite validation | fail closed; ≥2 checks, ≥1 original-condition |
| `tol` accepted 1e9 | unbounded gate parameter | clamp tolerance; never weaken a gate |
| Unconditional commit instruction | delivery conflated with authorisation | commit only when authorised; stage named files |
| Textless PDF accepted | `or ""` swallowed the failure | per-page census; exit 3; OCR/visual fallback |
| Outputs overwritten | fixed filenames, unconditional write | hash run-dir; refuse overwrite; atomic write |
| 343 orphan-"1" hits, silent truncation | context-free regex, `[:4000]` | scope heuristics; cap; announce truncation |
| Exemplar missed cover rules/handoff | template did not force them | template + linter enforce both |
| No tests | shipped code unexercised | every finding becomes a regression test |
**Meta-lesson:** a workflow document can be excellent while its helper code is
unsafe. Audit the *executable* surface with the same rigour as the prose.
