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

## Ledger
| # | Claim | Evidence | Status |
Statuses: Verified / Reasoned / Assumed / Unverifiable. Third-party results stay
**Reported-Verified (external)** until re-executed.
