# Distilling the process into a portable Agent Skill

---

## 1. Distillation plan (executed before authoring)

| Stage | Action | Output |
|---|---|---|
| **S1 Capture** | Mine the four turns for *decisions that changed an outcome*, not for narrative. | 12 incidents (OCR loss, $3\to9$, arg-from-$A$, min-vs-max tangent, non-unique $a$, rejected tangent, false quadrant reason, $O$-collision, dangling "Hence,", imported SE image, invented "$3^2$" correction, over-claimed verification). |
| **S2 Generalise** | Convert each incident → root cause → *transferable rule* → enforcement gate. Rules must survive a change of topic (complex numbers → DE → matrices). | Traceability matrix below. |
| **S3 Encode** | Split by *degrees of freedom*: reasoning = prose workflow; conventions = tables; deterministic acts = scripts. | `SKILL.md` + 4 references + 2 templates + 3 scripts. |
| **S4 Package** | Anthropic Agent Skills layout; progressive disclosure (SKILL.md ≤ 500 lines, details loaded on demand); agent-neutral wording. | Directory tree in §2. |
| **S5 Validate** | Lint frontmatter/structure; run maths checks; run eval suite. | Commands in §7–§9. |
| **S6 Iterate** | Feed failures back into `references/pitfalls-and-lessons.md`. | Versioned via `metadata.version`. |

**Traceability matrix (incident → rule → artefact):**

| Incident observed | Transferable rule | Enforced in |
|---|---|---|
| `\|z−9+4i\|` extracted as `9 4i z −+` | Reconstruct symbols from ≥2 independent signals before solving | `source-fidelity.md`, Gate **G1** |
| Stray `1` + two `*` ⇒ modulus-of-fraction | Use the *solution's first line* as a decoding key | `source-fidelity.md` §3 |
| Model invented "$3$ not $3^2$" | Never fabricate defects in the user's input | `SKILL.md` non-negotiable 6 |
| $3\lvert\cdot\rvert$ squared as $3(\cdot)$ | Scalar multipliers square too | `pitfalls-and-lessons.md` |
| $\arg$ measured from origin | $\arg(z-z_A)$ is a direction **from $A$** | `verification-playbook.md` |
| Adding $\alpha$ gives the maximum | Extremum selection + principal-range check | `verification-playbook.md` |
| Assumed $a$ unique | "All possible values" ⇒ separate fixed vs free parameters | `exam-presentation.md` |
| Second tangent not rejected | Domain restrictions are solution filters | Gate **G4** |
| "$O$ in the second quadrant" (false) | Right answer ≠ right reason; audit justifications | `audit-template.md` |
| $O$ used for centre | Notation reservation table | `exam-presentation.md` |
| Dangling "Hence," | Every required deliverable displayed at point of derivation | Gate **G3** |
| Imported StackExchange figure | Deliverables self-contained; no third-party artefacts | `SKILL.md` non-negotiable 5 |

---

## 2. Package layout

```
solving-a-level-exam-papers/
├── SKILL.md
├── references/
│   ├── source-fidelity.md
│   ├── exam-presentation.md
│   ├── verification-playbook.md
│   └── pitfalls-and-lessons.md
├── assets/
│   ├── solution-template.md
│   └── audit-template.md
└── scripts/
    ├── extract_pdf.py
    ├── check_math.py
    └── lint_skill.py
```

---

## 3. `SKILL.md`

````markdown
---
name: solving-a-level-exam-papers
description: Produces examiner-standard, verified worked solutions to questions from Singapore-Cambridge GCE A-Level examination papers (H1/H2/H3 Mathematics, Further Mathematics, and other quantitative subjects) supplied as PDF. Use when a user shares an exam paper PDF and asks to solve, check, audit or upgrade an answer to a numbered question, wants mark-scheme-quality working, exact answers or a model answer, or pastes OCR-garbled question text. Handles reconstruction of mathematical symbols lost in PDF extraction, mark-aware planning, exam presentation conventions, symbolic verification with an evidence ledger, and severity-classified audits of existing model answers.
metadata:
  version: 1.0.0
  spec: anthropic-agent-skills
  domain: education-assessment
---

# Solving A-Level Exam Papers (PDF → examiner-standard solution)

## Operating modes

Declare the mode in one line before starting: **SOLVE** (produce an answer),
**AUDIT** (review an existing answer), **SOLVE+AUDIT** (both, then unify).

## Non-negotiables

1. **Fidelity before mathematics.** Never solve OCR-damaged text as written.
   Reconstruct first (Gate G1). State the reconstruction and its confidence.
2. **No unearned "verified".** A claim is `Verified` only if the check was
   actually executed (symbolic/numeric) or is exact algebra shown in full.
   Otherwise label `Reasoned`, `Assumed` or `Unverifiable`.
3. **Exact means exact.** Surds, π, fractions, inverse trig. Decimals are
   sanity checks, never the answer, when "exact" is demanded.
4. **Obey the command word.** "Show that", "Hence", "Deduce", "Write down"
   each impose a different obligation (see `references/exam-presentation.md`).
5. **Self-contained deliverable.** No external links, imported images or
   third-party figures. Diagrams are drawn/described with this question's
   actual labels and coordinates.
6. **Never invent defects** in the user's paste, and never claim to have read
   a typeset page when only extracted text is available.
7. **Disclose deferred debt.** End with what was verified and what was not.

## Workflow and gates

### G0 — Ingest and map
- Run `scripts/extract_pdf.py PAPER.pdf` if a shell is available; otherwise
  read the supplied text. Build a page map: cover instructions, questions,
  **and any bound solutions/mark scheme**.
- Record the cover-page accuracy rules verbatim (they override defaults).
- **Gate:** question located by number AND page; presence/absence of official
  solutions recorded.

### G1 — Reconstruct and confirm
- Apply `references/source-fidelity.md`. Recover `|…|`, conjugates, fractions,
  matrices, inequalities, sub/superscripts.
- Cross-check the reconstruction against ≥2 signals: question text, bound
  solutions, internal consistency, mark allocation.
- **Gate:** every recovered symbol justified; ambiguous readings that change
  the answer are surfaced to the user, not silently chosen.

### G2 — Plan (before computing)
Produce a short table: part → concept → method → marks → expected answer form
→ anticipated pitfall. Choose methods that satisfy "hence"/"deduce" chains.

### G3 — Solve to examination standard
- Work forward; for "show that", never assume the printed result.
- Display every required result at its point of derivation, then state the
  conclusion in words ("…so C is a circle").
- Reserve notation: `O` = origin, `C` = centre, `A`,`B` = fixed points;
  never reuse a symbol for two objects.
- Diagrams: labelled schematic + a table of exact coordinates.
- **Gate:** each part answers exactly what was asked (centre **and** radius,
  all values **and** corresponding values, etc.).

### G4 — Verify (evidence, not assertion)
- Substitute the answer into the **original** conditions, not the derived ones.
- Run topic checks from `references/verification-playbook.md`; prefer
  `scripts/check_math.py` so results are executed, not asserted.
- Check domain/range restrictions, principal values, uniqueness and
  exhaustiveness ("all possible values"), and reject extraneous cases
  explicitly.
- **Gate:** ≥2 independent checks pass, including one substitution into the
  original condition. On failure, fix the root cause and re-verify —
  never weaken or delete a check to make it pass.

### G5 — Audit (only if an existing answer is supplied)
- Use `assets/audit-template.md`. Severity: Critical / Major / Minor /
  Enhancement. Quote evidence; give a minimal fix, not a rewrite.
- Audit your own previous answer with the same rubric.
- **Gate:** findings classified; no unrequested rewrite issued.

### G6 — Deliver
- Use `assets/solution-template.md`. Include the booklet-ready answer summary,
  the verification ledger, and a handoff (verified / deferred).
- If a git repository is available: one atomic Conventional Commit, e.g.
  `docs(solutions): add verified worked solution for 2026 P1 Q6`.

## Command words (quick reference)

| Command | Obligation |
|---|---|
| Show that / Prove | Forward derivation ending at the given result; no calculator-only support |
| Hence | Must visibly use the earlier result |
| Deduce | Must derive from the stated prior result, not restart |
| Write down / State | Answer alone; no working required |
| Find the exact value | No decimals; surds/π/log/inverse-trig form |
| Explain | Reasoned sentences with the mathematical cause |
| Sketch | Labelled key features: intercepts, asymptotes, turning points, endpoints |
| Determine the nature | Test + explicit conclusion per case |
| Find all possible values | Exhaustive case analysis; state free parameters |

Full conventions, accuracy rules and mark-depth heuristics:
`references/exam-presentation.md`.

## Evidence labels (mandatory in the ledger)

| Label | Meaning |
|---|---|
| Verified | Executed check, or exact algebra displayed in full |
| Reasoned | Sound inference from available evidence, not executed |
| Assumed | Plausible default, flagged as unconfirmed |
| Unverifiable | Cannot be checked with the available artefacts |

## Top pitfalls (full catalogue: `references/pitfalls-and-lessons.md`)

1. Squaring `k|z−a|` as `k(…)` instead of `k²(…)`.
2. Measuring `arg(z−z_A)` from the origin instead of from `A`.
3. Adding the tangent half-angle (gives the maximum, not the minimum).
4. Ignoring the principal-argument range and branch wrap.
5. Assuming a parameter is unique when only its argument is constrained.
6. Failing to reject solutions excluded by a stated domain restriction.
7. Right answer with a false justification.
8. Notation collisions (`O` for both origin and centre).
9. Missing final displayed result / dangling "Hence,".
10. External images or links inside an exam deliverable.
11. Decimals where exactness is required; premature rounding.
12. Claiming "PDF verified" or "mark scheme says" without the artefact.

## Reference index (load on demand)

| File | Load when |
|---|---|
| `references/source-fidelity.md` | Always at G1 |
| `references/exam-presentation.md` | At G2–G3 |
| `references/verification-playbook.md` | At G4 |
| `references/pitfalls-and-lessons.md` | At G2 (topic pitfalls) and G5 |
| `assets/solution-template.md` | At G6 (SOLVE) |
| `assets/audit-template.md` | At G5 (AUDIT) |

## Scripts

```bash
uv run --with pdfplumber python scripts/extract_pdf.py PAPER.pdf --out out/
uv run --with sympy   python scripts/check_math.py checks.json
python scripts/lint_skill.py .
```

Scripts are optional accelerators. If no shell is available, perform the same
checks by hand and label them accordingly — never simulate execution output.
````

---

## 4. `references/source-fidelity.md`

````markdown
# Source fidelity: recovering mathematics from PDF extraction

## 1. Why extraction fails
PDF text layers store glyphs and positions, not semantics. Extraction flattens
layout, drops non-alphanumeric glyphs, and reorders fractions/matrices.

| Lost construct | Typical extracted residue | Recovery signal |
|---|---|---|
| Modulus bars `\|z−a\|` | `9 4i z −+` | Solution squares the expression |
| Conjugate `a*` / `\bar a` | stray `*`, `\*` | "perpendicular bisector of a* and −a*" |
| Fraction = 1 | orphan `1` beside two `*` | Solution's first step clears the denominator |
| Matrix brackets | numbers in reading order | "3×3 matrix", eigenvalues, column vectors |
| `≤ ≥ ≠` | ` ` or `` | Interval statements in words |
| Sub/superscripts | `x2`, `e i` | Dimensional/degree consistency |
| Integral limits | limits inline | "from 0 to π/2" |
| Greek/π | blank or `p` | Context (angles, periods) |

## 2. Ground-truth hierarchy
1. Official worked solutions / mark scheme bound in the same PDF.
2. The printed question, reconstructed.
3. Independent re-derivation.
4. Third-party or model answers (audit these; never trust them).

If your result disagrees with (1), **investigate before publishing** — either
you erred, or the key erred; say which, with evidence.

## 3. Five-signal reconstruction protocol
1. **Token inventory** — list every surviving number, letter, operator, `*`, `1`.
2. **Operator placement** — decide where `=`, `|`, `−` must sit for the string
   to be well-formed.
3. **Solution decode** — read the first line of the official solution; it
   usually re-states the condition in expanded form.
4. **Consistency test** — does the reconstruction reproduce the key's result?
5. **Mark-weight test** — is the reconstructed task worth the marks printed?

### Worked example (2026 ACJC H2 FM P1 Q6)
- Extracted: `9 4i 3 1 4i z z −+ = − −`
  → `|z − 9 + 4i| = 3|z − 1 − 4i|`.
  Confirmation: solution line `(x−9)²+(y+4)² = 9[(x−1)²+(y−4)²]`.
- Extracted: `* * 1 w a w a − = +`
  → `|(w − a*)/(w + a*)| = 1` (two conjugates **and** an orphan `1`).
  Confirmation: solution's first step is `|w − a*| = |w + a*|`, i.e. the
  denominator was cleared. Equivalent for `a ≠ 0`; prefer the fraction form
  when quoting the paper.
- Consistency: both reproduce centre `5i`, radius `3√2`. ✔

## 4. Reporting rules
- Publish a short table: *extracted → reconstructed → evidence → confidence*.
- Label the typography `Reasoned` when only text extraction is available;
  reserve `Verified` for mathematical content confirmed against the key.
- List genuine losses only. **Do not invent corrections** the user never made.

## 5. Gate G1 checklist
- [ ] Every operator/bar/asterisk accounted for
- [ ] ≥2 independent signals agree
- [ ] Reconstruction reproduces the key's results (if a key exists)
- [ ] Ambiguities that change the answer escalated to the user
- [ ] Confidence labels attached
````

---

## 5. `references/exam-presentation.md`

````markdown
# Examination presentation conventions (Singapore-Cambridge GCE A-Level)

## 1. Read the cover page first
Typical standing instructions (confirm per paper):
- Non-exact numerical answers: **3 significant figures**; angles in degrees:
  **1 decimal place**, unless the question specifies otherwise.
- Approved graphing calculator expected; **unsupported GC answers allowed
  unless the question says otherwise**.
- Where unsupported answers are disallowed, present **mathematical notation,
  not calculator commands**.
- Marks in brackets at the end of each part.

## 2. Command words → obligations
See the table in `SKILL.md`. Additional traps:
- **"By letting z = x + iy …"** prescribes the method: a purely geometric or
  GC-only solution forfeits credit.
- **"Hence"** forbids an independent restart.
- **"Show that"** forbids working backwards from the printed result.
- **"Find the exact minimum"** forbids a decimal answer.

## 3. Mark-aware depth
| Marks | Expected substance |
|---|---|
| 1 | Single result or one-line justification |
| 2 | Method step + result |
| 3 | 2–3 linked steps + explicit conclusion |
| 4–5 | Multi-stage chain: model → condition → solve → interpret |
| 8+ | Extended derivation with substitution/limits and exact evaluation |

Allocate effort proportionally; do not over-write 1-mark parts.

## 4. Notation discipline
- Reserve `O` = origin, `C` = centre, `A`,`B`,`P`,`T` = named points.
- Distinguish position vector `\overrightarrow{OT}` from displacement
  `\overrightarrow{CT}`; label them correctly.
- Do not reuse `a`,`b` as generic reals if they are named data elsewhere.
- Define every symbol before use; keep `θ`, `ρ`, `r` roles consistent.

## 5. Diagrams
- Draw the **actual** configuration: label points with exact coordinates.
- Provide a coordinate table so the reader can reproduce the sketch.
- Mark the geometric fact being used (right angle at tangency, half-angle,
  asymptote, region shaded).
- Caption "schematic, not to scale" when appropriate.
- **Never** import external images or paste links.

## 6. Rounding and exactness
- Keep intermediates exact, or ≥6 s.f.; round only at the final line.
- Give exact forms whenever the question says "exact", or when the key does.
- Show the simplification `√18 = 3√2`; do not leave unsimplified surds.

## 7. Answering the whole question
- "State the centre **and** radius" → both.
- "Find all possible values of a **and** the corresponding w" → the family
  **and** the value(s), with the free parameter quantified (`for all r > 0`).
- "Determine the nature of **each**" → a conclusion per case.

## 8. Frequent mark losses
Missing concluding statement; no units; degrees/radians mismatch; unlabelled
sketch; skipped justification for rejecting a root; premature rounding;
calculator syntax in a "no unsupported answers" question.

## 9. Other subjects (same workflow, different conventions)
- **Physics:** units and significant figures at every final answer; state
  assumptions; free-body/circuit diagrams labelled.
- **Chemistry:** state symbols, balanced equations, conditions, units.
- **Economics/GP:** definition → diagram → analysis → evaluation; label axes.
````

---

## 6. `references/verification-playbook.md`

````markdown
# Verification playbook

## Principle
Verify against the **original** conditions, not the equations you derived —
an algebra slip propagates into derived forms but not into the original.

## Universal checks
1. **Substitution** of the answer into every original condition (exact).
2. **Domain/range**: does the answer satisfy every stated restriction?
3. **Principal values**: `arg ∈ (−π, π]`, `arcsin ∈ [−π/2, π/2]`, `√ ≥ 0`.
4. **Uniqueness/exhaustiveness**: discriminant, monotonicity, case count.
5. **Independent method**: geometric vs algebraic agreement.
6. **Limiting/sanity**: sign, magnitude, symmetry, units, boundary behaviour.
7. **Numerical**: high-precision evaluation as a *cross-check only*.

## Topic playbook
| Topic | Checks that catch real errors |
|---|---|
| Complex loci | Substitute point into circle/line; tangency ⇔ discriminant 0; distance from centre = radius |
| Arguments | Quadrant of the *difference vector*; extremum at tangency; both tangents inside the principal range |
| Differential equations | Substitute solution into the ODE **and** the initial condition |
| Numerical ODE/roots | Recompute each iteration; compare with the exact value; sign of the gradient across the step |
| Matrices/eigen | `A v = λ v` for each pair; `A = P D P⁻¹`; `det(A−λI)=0`; check span/independence claims |
| Vectors/planes | Dot/cross products; point-on-plane; direction ⟂ normal |
| Integration | Differentiate the antiderivative back; check limits and substitution Jacobian |
| Series | Ratio test; partial-sum formula against first terms |
| Stationary points | Gradient zero; second-derivative test sign; classify each |
| Probability/stats | Probabilities sum to 1; expectation within support; variance ≥ 0 |

## Executable checks
Write `checks.json` and run `scripts/check_math.py`:

```json
{
  "symbols": ["u"],
  "checks": [
    {"id":"V2","kind":"equal","note":"w lies on C",
     "lhs":"(3*sqrt(14)/5)**2 + (Rational(7,5)-5)**2","rhs":"18"},
    {"id":"V6","kind":"zero","note":"tangency: repeated root",
     "expr":"discriminant(25*u**2-30*sqrt(14)*u+126, u)"},
    {"id":"V9","kind":"interval","note":"theta admissible",
     "expr":"asin(3*sqrt(2)/5)","lo":"0","hi":"pi/2"}
  ]
}
```

Useful SymPy patterns:
```python
sp.simplify(lhs - rhs) == 0            # exact identity
sp.discriminant(poly, x) == 0          # tangency / repeated root
sp.simplify(sp.diff(F, x) - f) == 0    # antiderivative check
sp.simplify(ode.lhs - ode.rhs) == 0    # ODE solution check
sp.N(expr, 30)                         # 30-digit sanity value
```

## Ledger format (mandatory)
| # | Claim | Evidence | Status |
|---|---|---|---|
| 1 | … | exact algebra or executed output | Verified / Reasoned / Assumed / Unverifiable |

If no execution environment exists, say so explicitly and show the algebra.
Never fabricate calculator or script output.
````

---

## 7. `references/pitfalls-and-lessons.md`

````markdown
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
````

---

## 8. `assets/solution-template.md`

````markdown
# <Paper code> — Question <n> — Worked solution (<N> marks)

## 0. Source and fidelity note
| Item | Status |
|---|---|
| Mathematical content vs bound solutions | Verified / Reasoned |
| Typeset form of condition(s) | Reasoned (reconstructed from extraction) |

## 1. Question (reconstructed)
<parts, with marks>

## 2. Plan
| Part | Concept | Method | Marks | Pitfall |

## 3. Worked solution
### (a) [n]
<forward working; display each required result; state the conclusion>
### (b) [n]
<figure: labelled schematic + exact coordinate table>
### (c) [n]
<steps; explicit rejection of inadmissible cases>

## 4. Answer summary (booklet-ready)
| Part | Answer |

## 5. Verification ledger
| # | Claim | Evidence | Status |

## 6. Examiner notes
Indicative credit; common errors (label mark-splits as indicative).

## 7. Handoff
Verified: … | Deferred: …
````

---

## 9. `assets/audit-template.md`

````markdown
# Audit: <artefact>

## 1. Method
Ground truth: bound solutions > printed question > independent derivation.
Passes: fidelity → algebra → logic → completeness → presentation → provenance
→ differential comparison → classification.

## 2. Severity rubric
Critical (wrong result/invalid method) · Major (material defect) ·
Minor (local wording/notation) · Enhancement (optional).

## 3. Findings
| ID | Severity | Location | Evidence (quote) | Impact | Minimal fix |

## 4. Self-audit
<same rubric applied to your own prior answer>

## 5. Comparison matrix
| Dimension | Artefact | Own answer | Edge |

## 6. Verification ledger
| # | Check | Evidence | Status |

## 7. Recommendation
Accept / fix-before-use / reject. No rewrite unless requested.
````

---

## 10. `scripts/extract_pdf.py`

````python
#!/usr/bin/env python3
"""Page-marked PDF extraction plus a maths-symbol-loss report.

Usage:
    uv run --with pdfplumber python scripts/extract_pdf.py PAPER.pdf --out out/

Writes out/pages.txt and out/fidelity_report.txt. Deterministic; no network.
"""
from __future__ import annotations
import argparse, pathlib, re, sys

SUSPECT = [
    ("possible lost modulus bars",
     re.compile(r"(?<![\w|])[-+]?\s*\d+\s*i\b"), lambda s: "|" not in s),
    ("conjugate markers present", re.compile(r"\\\*|(?<=\w)\*"), None),
    ("orphan '1' (fraction = 1?)", re.compile(r"(?<![\w.])1(?![\w.])"), None),
    ("possible lost inequality", re.compile(r"\b0\s+\w+\s+π|\bfor\s+0\b"), None),
    ("matrix/vector residue", re.compile(r"(?:\d+\s+){4,}\d+"), None),
]

def extract(pdf: pathlib.Path) -> list[str]:
    try:
        import pdfplumber
    except ImportError:
        sys.exit("pdfplumber missing: uv run --with pdfplumber python ...")
    pages = []
    with pdfplumber.open(str(pdf)) as doc:
        for i, page in enumerate(doc.pages, start=1):
            pages.append(f"\n===== PDF PAGE {i} =====\n" + (page.extract_text() or ""))
    return pages

def report(pages: list[str]) -> str:
    lines = ["MATHS FIDELITY REPORT", "=" * 60,
             "Flags are heuristics: confirm each against the bound solutions.", ""]
    for i, text in enumerate(pages, start=1):
        hits = []
        for ln, line in enumerate(text.splitlines(), start=1):
            for name, rx, guard in SUSPECT:
                if rx.search(line) and (guard is None or guard(line)):
                    hits.append(f"  p{i} L{ln}: {name} :: {line.strip()[:90]}")
        if re.search(r"\bSolutions?\b|AO[123]", text):
            hits.append(f"  p{i}: SOLUTIONS/MARK TAGS DETECTED (ground truth available)")
        if hits:
            lines += [f"Page {i}:"] + hits + [""]
    return "\n".join(lines)

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf"); ap.add_argument("--out", default="out")
    a = ap.parse_args()
    out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
    pages = extract(pathlib.Path(a.pdf))
    (out / "pages.txt").write_text("".join(pages), encoding="utf-8")
    rep = report(pages)
    (out / "fidelity_report.txt").write_text(rep, encoding="utf-8")
    print(rep[:4000])
    print(f"\nWrote {out/'pages.txt'} and {out/'fidelity_report.txt'}")

if __name__ == "__main__":
    main()
````

---

## 11. `scripts/check_math.py`

````python
#!/usr/bin/env python3
"""Execute declared mathematical checks; emit a Markdown verification ledger.

Usage: uv run --with sympy python scripts/check_math.py checks.json
Exit code 1 if any check FAILs (never silently pass).

Check kinds:
  zero      : expr simplifies to 0
  equal     : lhs - rhs simplifies to 0
  interval  : lo < expr < hi        (numeric, strict)
  approx    : |lhs - rhs| < tol     (default tol 1e-10)
"""
from __future__ import annotations
import json, sys

def main() -> None:
    try:
        import sympy as sp
    except ImportError:
        sys.exit("sympy missing: uv run --with sympy python ...")
    if len(sys.argv) != 2:
        sys.exit("usage: check_math.py checks.json")
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    locals_ = {s: sp.Symbol(s) for s in spec.get("symbols", [])}
    S = lambda t: sp.sympify(t, locals=locals_)
    rows, failed = [], 0
    for c in spec["checks"]:
        kind, note, cid = c["kind"], c.get("note", ""), c["id"]
        try:
            if kind == "zero":
                ok = sp.simplify(S(c["expr"])) == 0
            elif kind == "equal":
                ok = sp.simplify(S(c["lhs"]) - S(c["rhs"])) == 0
            elif kind == "interval":
                v = float(sp.N(S(c["expr"]), 30))
                ok = float(sp.N(S(c["lo"]))) < v < float(sp.N(S(c["hi"])))
            elif kind == "approx":
                d = abs(complex(sp.N(S(c["lhs"]) - S(c["rhs"]), 30)))
                ok = d < float(c.get("tol", 1e-10))
            else:
                raise ValueError(f"unknown kind {kind!r}")
            status = "PASS" if ok else "FAIL"
        except Exception as exc:                      # noqa: BLE001
            ok, status = False, f"ERROR: {exc}"
        failed += 0 if ok else 1
        rows.append(f"| {cid} | {note} | {kind} | {status} |")
    print("| # | Claim | Check | Result |")
    print("|---|---|---|---|")
    print("\n".join(rows))
    print(f"\n{len(rows)-failed}/{len(rows)} checks passed.")
    sys.exit(1 if failed else 0)

if __name__ == "__main__":
    main()
````

---

## 12. `scripts/lint_skill.py`

````python
#!/usr/bin/env python3
"""Validate an Agent Skill directory: frontmatter, size, and local links.

Usage: python scripts/lint_skill.py path/to/skill-dir
"""
from __future__ import annotations
import pathlib, re, sys

NAME_RX = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

def main() -> None:
    root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    md = root / "SKILL.md"
    errs: list[str] = []
    if not md.is_file():
        sys.exit("FAIL: SKILL.md not found")
    text = md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        sys.exit("FAIL: missing YAML frontmatter")
    fm = text.split("---", 2)[1]
    body = text.split("---", 2)[2]
    name = re.search(r"^name:\s*(.+)$", fm, re.M)
    desc = re.search(r"^description:\s*(.+)$", fm, re.M)
    if not name or not NAME_RX.match(name.group(1).strip()):
        errs.append("name missing or not lowercase-hyphen")
    elif len(name.group(1).strip()) > 64:
        errs.append("name exceeds 64 characters")
    elif name.group(1).strip() != root.resolve().name:
        errs.append("name does not match directory name")
    if not desc:
        errs.append("description missing")
    elif len(desc.group(1).strip()) > 1024:
        errs.append("description exceeds 1024 characters")
    n = len(body.splitlines())
    if n > 500:
        errs.append(f"body is {n} lines (>500): move detail into references/")
    for link in re.findall(r"\]\(([^)]+)\)", body):
        if link.startswith(("http://", "https://")):
            continue
        if not (root / link).exists():
            errs.append(f"broken local link: {link}")
    print(f"SKILL.md body: {n} lines")
    if errs:
        print("FAIL:"); [print("  -", e) for e in errs]; sys.exit(1)
    print("PASS: structure and frontmatter valid")

if __name__ == "__main__":
    main()
````

---

## 13. Spec-conformance checklist

| Requirement | Status in this package |
|---|---|
| Directory containing `SKILL.md` | ✔ |
| YAML frontmatter with required `name`, `description` | ✔ |
| `name` lowercase/hyphens, ≤64 chars, matches directory | ✔ (27 chars) |
| `description` third person, what + when, ≤1024 chars | ✔ (~700 chars) |
| Body < 500 lines, progressive disclosure | ✔ (~200 lines; detail in `references/`) |
| Optional `metadata`; `license`/`allowed-tools` omitted deliberately | ✔ — omitting `allowed-tools` keeps the skill portable across Claude/Codex/Gemini |
| Supporting files referenced by relative, forward-slash paths | ✔ |
| No auxiliary README/CHANGELOG inside the skill | ✔ |
| Scripts deterministic, dependency-light, no network | ✔ |

**Portability:** Claude — drop into `~/.claude/skills/` or `.claude/skills/`. Codex — reference the folder from `AGENTS.md`. Gemini — reference it from `GEMINI.md`/system instructions. The prose is agent-neutral; only the optional `allowed-tools` field is Claude-specific and is intentionally absent.

---

## 14. Validation commands (converts claims into evidence)

```bash
python scripts/lint_skill.py solving-a-level-exam-papers
uv run --with pdfplumber python scripts/extract_pdf.py "2026_ Prelim_P1.pdf" --out out/
uv run --with sympy python scripts/check_math.py checks.json   # Q6 regression suite
```

**Eval suite (keep outside the skill folder):** Q6 complex loci · Q4 DE + Euler/improved Euler · Q5 eigen/diagonalisation · Q9 substitution volume · Q10 separable PDE.
**Pass criteria per case:** correct final answers; exact forms where required; reconstruction disclosed; ≥2 executed checks; no external links; ledger + handoff present.

---

## 15. Verification ledger for this deliverable

| # | Claim | Evidence | Status |
|---|---|---|---|
| 1 | Q6 mathematics used in examples | Exact algebra shown in earlier turns (substitution, discriminant 0) | **Verified** |
| 2 | Frontmatter fields/limits per Agent Skills spec | Stated from knowledge of the spec; not checked against live docs here | **Reasoned** |
| 3 | `lint_skill.py` would report PASS on this package | Desk-checked only; **not executed** in this environment | **Unverifiable here** |
| 4 | `extract_pdf.py`, `check_math.py` correctness | Desk-checked; **not executed** | **Unverifiable here** |
| 5 | Body line count ≈200 (<500) | Estimated by construction; measure with the linter | **Assumed** |
| 6 | Generalisation to other subjects/topics | Design intent, untested across the eval suite | **Assumed** |

### Handoff

**Delivered:** distillation plan + traceability matrix + complete skill package (1 `SKILL.md`, 4 references, 2 templates, 3 scripts) + conformance checklist + validation commands + eval design.
**Deferred (disclosed):** no script was executed here — run §14 to promote rows 3–5 to `Verified`; confirm the frontmatter limits against the current Agent Skills documentation; run the five-case eval suite before declaring the skill reliable across topics.
