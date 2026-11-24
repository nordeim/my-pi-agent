# Source fidelity: recovering mathematics from PDF extraction

## 0. Fail-closed ingestion (G0)
`extract_pdf.py` exits **3** when any page yields < 20 non-space characters.
That is a G0 FAILURE: render the pages (`--render`) and read them, or OCR.
Never reconstruct a question from an empty corpus. Keep `manifest.json`
(sha256 + per-page char census) as the provenance record.
Flags are **candidates**, never confirmed defects; confirm each against the
bound solutions before quoting a "correction" to the user.

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
