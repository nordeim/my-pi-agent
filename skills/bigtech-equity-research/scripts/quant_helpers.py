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
- abnormal_return returns a dict {excess, convention, beta, beta_window,
  beta_window_source}. The canonical default estimation window is
  DEFAULT_BETA_WINDOW (2-year monthly returns vs QQQ) — supplying a beta
  without a window applies the default so runs stay comparable; a different
  window must be justified in the note (report-6/7 finding H-2). The window
  is echoed in the result so the note can print it next to the figure.

Worked example: Alphabet Q3 2026, GOOG class (close $282.32 on 2026-10-29,
−12.29% from $321.89) — the canonical family example.
"""
import sys
from statistics import mean

TOL = 0.05
PERCENT_MULTIPLIER = 100.0  # scale factor for ratio -> percent conversions

# Canonical default beta estimation window (family doctrine, report-6/7 H-2):
# a beta-adjusted excess return is only comparable across runs when everyone
# estimates beta the same way. Override only when a corporate event
# structurally changed the company's risk profile — and justify it in the note.
DEFAULT_BETA_WINDOW = ("2-year monthly returns vs QQQ, through the last full "
                       "month-end before the event")


def beat_miss_delta(actual, consensus):
    """Return (abs_delta, pct_delta). Raises on zero consensus."""
    if consensus == 0:
        raise ValueError("consensus must be nonzero to compute a beat/miss delta")
    d = actual - consensus
    return d, d / consensus * PERCENT_MULTIPLIER


def abnormal_return(stock_ret, bench_ret, beta=None, beta_window=None):
    """Market-adjusted excess return, in percentage points.

    beta=None      -> stock_return - benchmark_return   (market-adjusted,
                     implicitly assumes beta = 1; NOT a market-model alpha)
    beta=<number>  -> stock_return - beta * benchmark_return  (market-model
                     form)

    beta_window disclosure (report-6/7 H-2): when beta is supplied without a
    window, the CANONICAL DEFAULT (DEFAULT_BETA_WINDOW) is applied and echoed
    with beta_window_source="canonical default" — comparability across runs
    without undisclosed choices. An explicitly passed window must be a
    non-empty string (blank or non-string raises: a beta-adjusted return with
    an unusable window disclosure is not reproducible). The window is echoed
    in the returned dict so the note can print it next to the figure.
    """
    if beta is None:
        return {"excess": stock_ret - bench_ret, "convention": "market-adjusted",
                "beta": None, "beta_window": None, "beta_window_source": None}
    if beta_window is None:
        beta_window = DEFAULT_BETA_WINDOW
        source = "canonical default"
    elif isinstance(beta_window, str) and beta_window.strip():
        source = "explicit"
    else:
        raise ValueError(
            "beta_window must be a non-empty string (e.g. '250 sessions vs QQQ, "
            "through YYYY-MM-DD') or None to apply the canonical default "
            f"({DEFAULT_BETA_WINDOW}) — a beta-adjusted excess return is not "
            "reproducible without a usable window")
    return {"excess": stock_ret - beta * bench_ret,
            "convention": "beta-adjusted", "beta": beta,
            "beta_window": beta_window, "beta_window_source": source}


def capex_ocf_ratio(capex, ocf):
    """Capex / OCF as a percent. Raises on zero OCF."""
    if ocf == 0:
        raise ValueError("OCF must be nonzero to compute the capex/OCF ratio")
    return capex / ocf * PERCENT_MULTIPLIER


def ocf_shortfall(consensus_fcf, consensus_capex, actual_ocf):
    """When capex beats Street but FCF misses, the gap is operating cash flow.

    Positive result = actual OCF below the consensus-implied level."""
    implied_ocf = consensus_fcf + consensus_capex
    return implied_ocf - actual_ocf


def avg_pt_cut(pt_pairs):
    """pt_pairs = [(new_pt, old_pt), ...]. Returns mean % cut."""
    cuts = [(new - old) / old * PERCENT_MULTIPLIER for new, old in pt_pairs]
    return mean(cuts)


def fcf(ocf, capex):
    """Free cash flow = operating cash flow - capex (the family's definition).

    Always computed in code, never in-context — and always paired with its
    ex-SBC companion in the scorecard (see fcf_ex_sbc)."""
    return ocf - capex


def fcf_ex_sbc(ocf, capex, sbc):
    """FCF excluding stock-based compensation = OCF - capex - SBC.

    Report-6/7 finding (report A #6 / synthesized #8): for US mega-cap tech,
    SBC is structurally material, so the scorecard pairs FCF with FCF ex-SBC —
    FCF that ignores SBC overstates the cash generation available for
    buybacks/dividends. SBC comes from the cash-flow statement (T1); state
    which basis beats/misses consensus. Positive/negative sign follows FCF.
    """
    return ocf - capex - sbc


def segment_variance(actual, consensus, prior_q, year_ago_q):
    """One segment row of the ASC 280 variance table (report-7 L-4 helper gap).

    Returns {delta_abs, delta_pct, qoq, yoy} — the beat/miss delta vs
    consensus plus the QoQ and YoY growth the Phase 3 table needs to separate
    a MISS from a DECELERATION. Raises on zero consensus / prior / year-ago
    bases (growth rates are undefined)."""
    if consensus == 0 or prior_q == 0 or year_ago_q == 0:
        raise ValueError("consensus, prior_q and year_ago_q must be nonzero to "
                         "compute a segment variance row")
    delta_abs = actual - consensus
    return {"delta_abs": delta_abs,
            "delta_pct": delta_abs / consensus * PERCENT_MULTIPLIER,
            "qoq": (actual - prior_q) / prior_q * PERCENT_MULTIPLIER,
            "yoy": (actual - year_ago_q) / year_ago_q * PERCENT_MULTIPLIER}


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
    check("excess return (market-adjusted)",
          abnormal_return(-12.29, -1.5)["excess"], -10.79, 0.005)
    # Beta-adjusted variant: explicit window echoed as explicit.
    rab = abnormal_return(-12.29, -1.5, beta=1.2,
                          beta_window="250 sessions vs QQQ, through 2026-10-27")
    check("excess return (beta-adjusted)", rab["excess"], -10.49, 0.005)
    if rab["convention"] != "beta-adjusted" or rab["beta"] != 1.2:
        failures.append("beta-adjusted result must echo the convention and beta")
    if rab["beta_window_source"] != "explicit":
        failures.append("an explicitly passed beta_window must be echoed as 'explicit'")
    # Round-3 (report-6/7 H-2): beta WITHOUT a window applies the canonical
    # default (comparability across runs) and echoes it — no longer raises.
    rad = abnormal_return(-12.29, -1.5, beta=1.2)
    check("excess return (canonical default window)", rad["excess"], -10.49,
          0.005)
    if rad["beta_window"] != DEFAULT_BETA_WINDOW:
        failures.append("beta without a window must apply DEFAULT_BETA_WINDOW")
    if rad["beta_window_source"] != "canonical default":
        failures.append("canonical default must be labeled as such in the result")
    # Regression (M1, report-3/4): an UNUSABLE window still raises.
    try:
        abnormal_return(-12.29, -1.5, beta=1.2, beta_window="   ")
        failures.append("blank beta_window must raise ValueError")
    except ValueError:
        pass
    try:
        abnormal_return(-12.29, -1.5, beta=1.2, beta_window=250)
        failures.append("non-string beta_window must raise ValueError")
    except ValueError:
        pass

    check("capex/OCF ratio", capex_ocf_ratio(51.36, 42.29), 121.4, 0.05)
    check("OCF shortfall", ocf_shortfall(-2.70, 55.09, 42.29), +10.10, 0.005)

    # Round-3 helpers: FCF pairing (report-6/7 synthesized #8) and the
    # segment-variance row (report-7 L-4). The FCF figures are the canonical
    # Alphabet Q3 2026 print; the ex-SBC and variance inputs below are
    # synthetic self-test fixtures, not company figures.
    check("FCF", fcf(42.29, 51.36), -9.07, 0.005)
    check("FCF ex-SBC (synthetic fixture)", fcf_ex_sbc(42.29, 51.36, 6.50),
          -15.57, 0.005)
    if fcf_ex_sbc(42.29, 51.36, 6.50) >= fcf(42.29, 51.36):
        failures.append("positive SBC must make FCF ex-SBC smaller than FCF")
    sv = segment_variance(110.0, 100.0, 100.0, 50.0)
    check("segment delta_abs", sv["delta_abs"], 10.0, 0.005)
    check("segment delta_pct", sv["delta_pct"], 10.0, 0.005)
    check("segment qoq", sv["qoq"], 10.0, 0.005)
    check("segment yoy", sv["yoy"], 120.0, 0.005)
    try:
        segment_variance(110.0, 0.0, 100.0, 50.0)
        failures.append("zero consensus must raise ValueError")
    except ValueError:
        pass

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
          f"{abnormal_return(-12.29, -1.5)['excess']:+.2f}pp")      # −10.79
    print(f"Beta-adjusted ({rab['beta']}, {rab['beta_window']}): "
          f"{rab['excess']:+.2f}pp")                                 # −10.49
    print(f"Beta-adjusted ({rad['beta']}, canonical default): "
          f"{rad['excess']:+.2f}pp [{rad['beta_window']}]")        # −10.49
    print(f"Capex/OCF: {capex_ocf_ratio(51.36, 42.29):.1f}%")      # 121.4%
    print(f"OCF shortfall: {ocf_shortfall(-2.70, 55.09, 42.29):+.2f}B")  # +10.10B
    print(f"FCF: {fcf(42.29, 51.36):+.2f}B (paired with FCF ex-SBC "
          f"in the scorecard)")                                     # −9.07B
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
