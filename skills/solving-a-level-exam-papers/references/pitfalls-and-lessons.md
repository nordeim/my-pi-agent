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
