---
name: solving-a-level-exam-papers
description: Produces examiner-standard, verified worked solutions to questions from Singapore-Cambridge GCE A-Level examination papers (H1/H2/H3 Mathematics, Further Mathematics, and other quantitative subjects) supplied as PDF. Use when a user shares an exam paper PDF and asks to solve, check, audit or upgrade an answer to a numbered question, wants mark-scheme-quality working, exact answers or a model answer, or pastes OCR-garbled question text. Handles reconstruction of mathematical symbols lost in PDF extraction, mark-aware planning, exam presentation conventions, symbolic verification with an evidence ledger, and severity-classified audits of existing model answers.
metadata:
  version: 1.0.0
  spec: anthropic-agent-skills
  domain: education-assessment
---

# Solving A-Level Exam Papers (PDF → examiner-standard solution)

## Package layout

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
