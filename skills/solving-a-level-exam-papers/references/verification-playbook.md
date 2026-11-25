# Verification playbook

Verify against the **original** conditions, not derived ones.

## Suite contract (enforced by check_math.py)
- `checks`: non-empty list, **≥2** entries, unique `id`, mandatory `note`.
- **≥1 check with `role:"original-condition"`**; other roles:
  `independent-method`, `domain`, `sanity`.
- Kinds: `zero` (expr = 0), `equal` (lhs = rhs), `approx` (|lhs−rhs| < tol),
  `interval` (lo < expr < hi, or `inclusive: true`).
- `zero`/`equal` reject floats: write `Rational(7,5)`, not `1.4`.
- `0 < tol <= 1e-6`. Use `**`, never `^`.
- Per-check timeout (default 20 s, POSIX). Errors fail closed.
- Output ledger carries `checks_sha256` and SymPy version; undated unless `--stamp`.

## Universal checks (apply to every answer)
1. **Substitution** of the answer into every *original* condition (exact).
2. **Domain/range**: every stated restriction is satisfied.
3. **Principal values**: `arg ∈ (−π, π]`, `arcsin ∈ [−π/2, π/2]`, `√ ≥ 0`.
4. **Uniqueness/exhaustiveness**: discriminant, monotonicity, case count.
5. **Independent method**: geometric vs algebraic agreement.
6. **Limiting/sanity**: sign, magnitude, symmetry, units, boundary behaviour.
7. **Numerical**: high-precision evaluation as a *cross-check only*.

## Topic checks
| Topic | Checks that catch real errors |
|---|---|
| Complex loci | substitute into the original modulus equation; tangency ⇔ discriminant 0 |
| Arguments | quadrant of the difference vector; both tangents inside the principal range |
| ODEs | substitute solution into the ODE **and** the initial condition |
| Numerical methods | recompute each iteration; compare with the exact value |
| Matrices | `A v = λ v`; `A = P D P⁻¹`; independence before spanning claims |
| Vectors | dot/cross; point-on-plane; direction ⟂ normal |
| Integration | differentiate back; check limits and Jacobian |
| Series | ratio test; partial sums against first terms |
| Stationary points | gradient zero; second-derivative test; classify each |
| Probability/stats | probabilities sum to 1; expectation within the support; variance ≥ 0 |

## Expression patterns (`checks.json` syntax; whitelist in `scripts/safe_expr.py`)
| Claim | Kind | Expression |
|---|---|---|
| Exact identity | `equal` | `lhs`, `rhs` (floats rejected; `Rational(7,5)`) |
| Tangency / repeated root | `zero` | `discriminant(25*u**2 - 30*sqrt(14)*u + 126, u)` |
| Antiderivative | `zero` | `diff(F, x) - f` |
| Eigenpair `A v = λ v` | `equal` | `Matrix([[2,0],[0,3]])*Matrix([[1],[0]])` vs `2*Matrix([[1],[0]])` |
| Inverse | `zero` | `Matrix([[1,2],[3,4]])*inv(Matrix([[1,2],[3,4]])) - eye(2)` |
| Admissible angle | `interval` | `asin(3*sqrt(2)/5)` within `0`..`pi/2` |
| Sanity value | `approx` | `lhs`, `rhs`, `tol` ≤ 1e-6 |

Matrix results are compared entrywise after `simplify`. Each side must be a
scalar or a matrix of equal shape; lists, or a matrix against a scalar, are
rejected as a suite error (exit 2). Variables must be listed in `symbols`.
Outside the suite, a REPL may use `sp.simplify(lhs - rhs) == 0` and
`sp.N(expr, 30)`; never pass untrusted text to `sympify`.

## Ledger
| # | Claim | Evidence | Status |
Statuses: Verified / Reasoned / Assumed / Unverifiable. Third-party results stay
**Reported-Verified (external)** until re-executed.
