#!/usr/bin/env python3
"""Deterministic quant math for big-tech equity research. Avoids hand-arithmetic errors.

Usage:  python3 quant_helpers.py            # runs an asserting self-test on the
                                           # worked example (exits 1 on any failure)
        import quant_helpers as qh          # or import individual functions

Conventions:
- Percentages are plain numbers (−12.29 means −12.29%).
- Waterfall weights are SIGNED: positive = tailwind, negative = headwind. A
  decomposition whose signed sum disagrees with the realized move's sign is
  wrong, not a formatting difference.
- ocf_shortfall > 0 means actual OCF ran below consensus-implied OCF.

Worked example: Alphabet Q3 2026, GOOG class (close $282.32 on 2026-10-29,
−12.29% from $321.89) — the canonical family example.
"""
import sys
from statistics import mean

TOL = 0.05


def beat_miss_delta(actual, consensus):
    """Return (abs_delta, pct_delta). Raises on zero consensus."""
    if consensus == 0:
        raise ValueError("consensus must be nonzero to compute a beat/miss delta")
    d = actual - consensus
    return d, d / consensus * 100.0


def abnormal_return(stock_ret, bench_ret, beta=None):
    """Market-adjusted excess return, in percentage points.

    beta=None      -> stock_return - benchmark_return   (market-adjusted,
                     implicitly assumes beta = 1; NOT a market-model alpha)
    beta=<number>  -> stock_return - beta * benchmark_return  (market-model
                     form; disclose the estimation window used for beta)
    """
    if beta is None:
        return stock_ret - bench_ret
    return stock_ret - beta * bench_ret


def capex_ocf_ratio(capex, ocf):
    """Capex / OCF as a percent. Raises on zero OCF."""
    if ocf == 0:
        raise ValueError("OCF must be nonzero to compute the capex/OCF ratio")
    return capex / ocf * 100.0


def ocf_shortfall(consensus_fcf, consensus_capex, actual_ocf):
    """When capex beats Street but FCF misses, the gap is operating cash flow.

    Positive result = actual OCF below the consensus-implied level."""
    implied_ocf = consensus_fcf + consensus_capex
    return implied_ocf - actual_ocf


def avg_pt_cut(pt_pairs):
    """pt_pairs = [(new_pt, old_pt), ...]. Returns mean % cut."""
    cuts = [(new - old) / old * 100.0 for new, old in pt_pairs]
    return mean(cuts)


def waterfall_check(weights, realized_move, tol=TOL):
    """Consistency check for a SIGNED driver decomposition.

    weights: {factor: signed_pct_points}; positive = tailwind, negative =
    headwind. `matches` is True only when the signed sum reproduces the
    realized move within tol — this checks arithmetic consistency of a
    Reasoned allocation; it is NOT evidence of causation.
    """
    total = sum(weights.values())
    return {"sum": round(total, 2),
            "matches": abs(total - realized_move) < tol}


# ---------------------------------------------------------------------------
# Asserting self-test: exits 0 only if every worked-example figure reproduces.
# ---------------------------------------------------------------------------
def _selftest():
    failures = []

    def check(name, got, want, tol=0.005):
        if abs(got - want) > tol:
            failures.append(f"{name}: got {got:+.4f}, expected {want:+.4f}")

    rev_d, rev_p = beat_miss_delta(127.58, 128.22)
    check("revenue delta abs", rev_d, -0.64, 0.005)
    check("revenue delta pct", rev_p, -0.50, 0.005)

    eps_d, eps_p = beat_miss_delta(2.12, 3.02)
    check("EPS delta abs", eps_d, -0.90, 0.005)
    check("EPS delta pct", eps_p, -29.80, 0.01)

    # Market-adjusted excess return, GOOG class, beta=1 convention.
    check("excess return (market-adjusted)", abnormal_return(-12.29, -1.5), -10.79, 0.005)
    # Beta-adjusted variant.
    check("excess return (beta-adjusted)", abnormal_return(-12.29, -1.5, beta=1.2), -10.49, 0.005)

    check("capex/OCF ratio", capex_ocf_ratio(51.36, 42.29), 121.4, 0.05)
    check("OCF shortfall", ocf_shortfall(-2.70, 55.09, 42.29), +10.10, 0.005)

    pts = [(375, 425), (385, 435), (300, 350), (380, 430), (355, 440)]
    check("avg PT cut", avg_pt_cut(pts), -13.7, 0.05)

    # Signed waterfall on the canonical GOOG print (sums to -12.3 vs -12.29).
    wf = {"benchmark": -1.5, "fcf_capex": -3.9, "eps_quality": -2.7,
          "search": -2.4, "positioning": -1.8}
    r = waterfall_check(wf, -12.29)
    if r["sum"] != -12.3:
        failures.append(f"waterfall sum: got {r['sum']}, expected -12.3")
    if not r["matches"]:
        failures.append("signed waterfall summing to the realized move must match")

    # Regression (the old abs() bug): a sign-flipped decomposition must NOT match.
    flipped = {k: -v for k, v in wf.items()}
    if waterfall_check(flipped, -12.29)["matches"]:
        failures.append("sign-flipped decomposition must not match a negative move")
    # Regression: unsigned magnitudes summing to +12.3 must NOT match -12.29.
    unsigned = {k: abs(v) for k, v in wf.items()}
    if waterfall_check(unsigned, -12.29)["matches"]:
        failures.append("unsigned magnitude sum must not match a signed move")

    print(f"Revenue delta: {rev_d:+.2f}B ({rev_p:+.2f}%)")        # −0.64B (−0.50%)
    print(f"EPS delta:     {eps_d:+.2f} ({eps_p:+.2f}%)")          # −0.90 (−29.80%)
    print(f"Excess return vs −1.5% benchmark: "
          f"{abnormal_return(-12.29, -1.5):+.2f}pp")               # −10.79
    print(f"Capex/OCF: {capex_ocf_ratio(51.36, 42.29):.1f}%")      # 121.4%
    print(f"OCF shortfall: {ocf_shortfall(-2.70, 55.09, 42.29):+.2f}B")  # +10.10B
    print(f"Avg PT cut: {avg_pt_cut(pts):+.1f}%")                  # −13.7%
    print(f"Waterfall: {waterfall_check(wf, -12.29)}")             # sum -12.3, matches True
    print("=" * 60)
    if failures:
        print(f"SELFTEST: FAIL ({len(failures)} failure(s))")
        for f in failures:
            print("  -", f)
        return 1
    print("SELFTEST: PASS (all worked-example figures reproduced)")
    return 0


if __name__ == "__main__":
    sys.exit(_selftest())
