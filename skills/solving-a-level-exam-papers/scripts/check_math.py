#!/usr/bin/env python3
"""Execute declared mathematical checks; emit a provenance-bearing ledger.

Exit: 0 all pass | 1 a check FAILED/ERRORED | 2 suite invalid, unsafe, unreadable
or results unwritable.
Undated by default (reproducible); --stamp adds a UTC timestamp.
"""
from __future__ import annotations
import argparse, hashlib, json, os, signal, sys, tempfile
from pathlib import Path

import sympy as sp
sys.path.insert(0, str(Path(__file__).resolve().parent))
from safe_expr import UnsafeExpression, is_inexact, parse  # noqa: E402

KINDS = {"zero", "equal", "approx", "interval"}
ROLES = {"original-condition", "independent-method", "domain", "sanity"}
EXACT_KINDS = {"zero", "equal"}
MIN_CHECKS_FLOOR, MAX_CHECKS, MAX_TOL = 2, 200, 1e-6
REQUIRED = {"zero": ("expr",), "equal": ("lhs", "rhs"),
            "approx": ("lhs", "rhs"), "interval": ("expr", "lo", "hi")}


class ConfigError(ValueError):
    pass


def validate(spec, min_checks):
    if min_checks < MIN_CHECKS_FLOOR:
        raise ConfigError(f"--min-checks cannot be below {MIN_CHECKS_FLOOR} (gate G4)")
    if not isinstance(spec, dict):
        raise ConfigError("top level must be a JSON object")
    checks = spec.get("checks")
    if not isinstance(checks, list) or not checks:
        raise ConfigError("'checks' must be a non-empty list; an empty suite is not a pass")
    if len(checks) < min_checks:
        raise ConfigError(f"{len(checks)} check(s) supplied; G4 requires >= {min_checks}")
    if len(checks) > MAX_CHECKS:
        raise ConfigError(f"more than {MAX_CHECKS} checks")
    seen, roles = set(), []
    for i, c in enumerate(checks):
        where = f"checks[{i}]"
        if not isinstance(c, dict):
            raise ConfigError(f"{where} must be an object")
        cid, kind, note = c.get("id"), c.get("kind"), c.get("note")
        if not isinstance(cid, str) or not cid.strip():
            raise ConfigError(f"{where}.id must be a non-empty string")
        if cid in seen:
            raise ConfigError(f"duplicate check id: {cid}")
        seen.add(cid)
        if kind not in KINDS:
            raise ConfigError(f"{where}.kind must be one of {sorted(KINDS)}")
        if not isinstance(note, str) or not note.strip():
            raise ConfigError(f"{where}.note must state the claim being checked")
        role = c.get("role")
        if role is not None:
            if role not in ROLES:
                raise ConfigError(f"{where}.role must be one of {sorted(ROLES)}")
            roles.append(role)
        for field in REQUIRED[kind]:
            if not isinstance(c.get(field), str):
                raise ConfigError(f"{where}.{field} must be a string expression")
        if "tol" in c:
            try:
                tol = float(c["tol"])
            except (TypeError, ValueError):
                raise ConfigError(f"{where}.tol must be numeric") from None
            if not (0 < tol <= MAX_TOL):
                raise ConfigError(f"{where}.tol must satisfy 0 < tol <= {MAX_TOL}")
        if "inclusive" in c and not isinstance(c["inclusive"], bool):
            raise ConfigError(f"{where}.inclusive must be a boolean")
    if "original-condition" not in roles:
        raise ConfigError("G4 requires >= 1 check with role 'original-condition'")
    return checks


def _difference(cid, lhs, rhs):
    lhs_matrix, rhs_matrix = isinstance(lhs, sp.MatrixBase), isinstance(rhs, sp.MatrixBase)
    if lhs_matrix != rhs_matrix:
        raise ConfigError(f"{cid}: cannot compare a matrix with a scalar")
    if not lhs_matrix and not (isinstance(lhs, sp.Expr) and isinstance(rhs, sp.Expr)):
        raise ConfigError(f"{cid}: both sides must evaluate to scalars or matrices")
    if lhs_matrix and lhs.shape != rhs.shape:
        raise ConfigError(f"{cid}: matrix shapes differ: {lhs.shape} vs {rhs.shape}")
    return lhs - rhs


def _is_zero(cid, target):
    if isinstance(target, sp.MatrixBase):
        simplified = target.applyfunc(sp.simplify)
        return bool(simplified.is_zero_matrix), simplified
    if not isinstance(target, sp.Expr):
        raise ConfigError(f"{cid}: expression must evaluate to a scalar or matrix")
    simplified = sp.simplify(target)
    return simplified == 0, simplified


def _scalar(cid, value):
    if not isinstance(value, sp.Expr):
        raise ConfigError(f"{cid}: expression must evaluate to a scalar, "
                          f"got {type(value).__name__}")
    return value


class _Timeout(Exception):
    pass


def _alarm(signum, frame):
    raise _Timeout("per-check time limit exceeded")


def run_check(c, symbols, timeout):
    if hasattr(signal, "SIGALRM"):
        signal.signal(signal.SIGALRM, _alarm)
        signal.setitimer(signal.ITIMER_REAL, timeout)
    try:
        kind = c["kind"]
        get = lambda k: parse(c[k], symbols)
        if kind in EXACT_KINDS:
            exprs = [get(k) for k in REQUIRED[kind]]
            if any(is_inexact(e) for e in exprs):
                raise ConfigError(f"{c['id']}: floats are forbidden in exact checks; use Rational(7,5)")
            target = exprs[0] if kind == "zero" else _difference(c["id"], *exprs)
            ok, simplified = _is_zero(c["id"], target)
            detail = f"simplified: {simplified}"
        elif kind == "approx":
            lhs, rhs = _scalar(c["id"], get("lhs")), _scalar(c["id"], get("rhs"))
            d = sp.N(sp.Abs(lhs - rhs), 30)
            tol = float(c.get("tol", 1e-10))
            ok = bool(d.is_real) and float(d) < tol
            detail = f"|difference| = {d}, tol = {tol}"
        else:
            v = sp.N(_scalar(c["id"], get("expr")), 30)
            if not v.is_real:
                raise ValueError("interval check requires a real value")
            lo = float(sp.N(_scalar(c["id"], get("lo")), 30))
            hi = float(sp.N(_scalar(c["id"], get("hi")), 30))
            x = float(v)
            ok = (lo <= x <= hi) if c.get("inclusive") else (lo < x < hi)
            detail = f"value = {x}, bounds = ({lo}, {hi})"
        return {"id": c["id"], "note": c["note"], "kind": kind,
                "role": c.get("role", "-"), "status": "PASS" if ok else "FAIL",
                "detail": detail}
    except ConfigError:
        raise
    except UnsafeExpression as exc:
        raise ConfigError(f"{c['id']}: unsafe expression: {exc}") from None
    except Exception as exc:  # noqa: BLE001 - fail closed
        return {"id": c["id"], "note": c.get("note", ""), "kind": c["kind"],
                "role": c.get("role", "-"), "status": "ERROR", "detail": str(exc)}
    finally:
        if hasattr(signal, "SIGALRM"):
            signal.setitimer(signal.ITIMER_REAL, 0)


def _md_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("checks")
    ap.add_argument("--min-checks", type=int, default=MIN_CHECKS_FLOOR)
    ap.add_argument("--timeout", type=float, default=20.0)
    ap.add_argument("--json")
    ap.add_argument("--stamp", action="store_true")
    a = ap.parse_args()
    if not 0 < a.timeout <= 120:
        print("CONFIG ERROR: --timeout must be in (0, 120]", file=sys.stderr)
        return 2
    try:
        raw = Path(a.checks).read_bytes()
        spec = json.loads(raw)
        checks = validate(spec, a.min_checks)
        rows = [run_check(c, spec.get("symbols", []), a.timeout) for c in checks]
    except (ConfigError, OSError, json.JSONDecodeError) as exc:
        print(f"CONFIG ERROR: {exc}", file=sys.stderr)
        return 2
    failed = sum(r["status"] != "PASS" for r in rows)
    ledger = ["| # | Claim | Kind | Role | Result |", "|---|---|---|---|---|"]
    ledger += [f"| {_md_cell(r['id'])} | {_md_cell(r['note'])} | {_md_cell(r['kind'])} | "
               f"{_md_cell(r['role'])} | {_md_cell(r['status'])} |" for r in rows]
    provenance = {"checks_sha256": hashlib.sha256(raw).hexdigest(),
                  "sympy": sp.__version__, "python": sys.version.split()[0],
                  "passed": len(rows) - failed, "total": len(rows)}
    if a.stamp:
        import datetime
        provenance["generated_utc"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    print("\n".join(ledger))
    print(f"\n{len(rows) - failed}/{len(rows)} checks passed.")
    print(f"provenance: checks_sha256={provenance['checks_sha256'][:16]}… sympy={sp.__version__}")
    if a.json:
        payload = {"provenance": provenance, "results": rows}
        p = Path(a.json)
        try:
            with tempfile.NamedTemporaryFile("w", dir=p.parent, delete=False,
                                             encoding="utf-8") as fh:
                json.dump(payload, fh, indent=2)
                tmp = fh.name
            os.replace(tmp, p)
        except OSError as exc:
            print(f"CONFIG ERROR: cannot write {p}: {exc}", file=sys.stderr)
            return 2
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
