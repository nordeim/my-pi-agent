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
