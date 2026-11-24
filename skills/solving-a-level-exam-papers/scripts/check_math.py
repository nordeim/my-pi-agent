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
