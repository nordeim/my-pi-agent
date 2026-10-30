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
from statistics import mean, pstdev

TOL = 0.05
PERCENT_MULTIPLIER = 100.0  # scale factor for ratio -> percent conversions

# Canonical default beta estimation window (family doctrine, report-6/7 H-2):
# a beta-adjusted excess return is only comparable across runs when everyone
# estimates beta the same way. Override only when a corporate event
# structurally changed the company's risk profile — and justify it in the note.
DEFAULT_BETA_WINDOW = ("2-year monthly returns vs QQQ, through the last full "
                       "month-end before the event")

# Round-4 regime diagnostics (reports 8/9 M-7): a canonical 2-year monthly beta
# is only trustworthy while the stock/benchmark correlation holds and realized
# vol is in its historical regime. Below this R^2 floor the beta is noise-fit;
# the agent must justify the window or switch to a shorter (e.g. 6-month daily)
# window and disclose it.
R_SQUARED_FLOOR = 0.30
VOL_REGIME_Z_THRESHOLD = 2.0


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


def beta_diagnostics(stock_rets, bench_rets):
    """OLS beta + R^2 + correlation-breakdown flag from paired return series.

    Round 4 (reports 8/9 M-7, "static beta regime assumption"): the canonical
    2-year monthly beta window smooths regime breaks (2022 rate shock, 2023 AI
    re-rating), and "structurally changed" detection was delegated entirely to
    judgment. This helper turns that judgment into a quantitative trigger:
    when `correlation_breakdown` is True (R^2 < R_SQUARED_FLOOR), the beta is
    fitting noise — the note must either explicitly justify the 2-year window
    or re-estimate over a shorter (e.g. 6-month daily) window and disclose it.

    stock_rets / bench_rets: equal-length sequences of periodic returns in
    percent (e.g. monthly % returns vs QQQ over the canonical window). Returns
    {beta, r_squared, correlation, r_squared_floor, correlation_breakdown}.
    Raises on length mismatch or zero benchmark variance.
    """
    xs, ys = list(stock_rets), list(bench_rets)
    if len(xs) != len(ys):
        raise ValueError("stock_rets and bench_rets must have equal length")
    if len(xs) < 3:
        raise ValueError("beta diagnostics need >= 3 paired returns")
    mx, my = mean(xs), mean(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    if syy == 0:
        raise ValueError("benchmark return series has zero variance — beta is "
                         "undefined")
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    beta = sxy / syy          # cov(stock, bench) / var(bench) — the slope of
                              # stock-on-bench OLS, NOT the reverse regression
    corr = (sxy / (sxx * syy) ** 0.5) if sxx > 0 else 0.0
    r2 = corr * corr
    return {"beta": round(beta, 4), "r_squared": round(r2, 4),
            "correlation": round(corr, 4), "r_squared_floor": R_SQUARED_FLOOR,
            "correlation_breakdown": r2 < R_SQUARED_FLOOR}


def volatility_regime_flag(monthly_rets, recent_n=3, history_n=24):
    """Trailing realized-vol z-score vs the 2-year mean (reports 8/9 M-7).

    Compares the annualized realized volatility of the trailing `recent_n`
    months against the mean and population standard deviation of rolling
    realized vol over `history_n` months. |z| > VOL_REGIME_Z_THRESHOLD means
    the stock has exited its volatility regime — applying the canonical
    2-year beta then misattributes market moves to company specifics. The
    note must justify the window or use a shorter one.

    monthly_rets: >= history_n monthly % returns (most recent last).
    Returns {recent_vol, baseline_vol, z_score, z_threshold,
    regime_shift}. Raises when the series is too short or baseline vol is 0.
    """
    rets = list(monthly_rets)
    if len(rets) < history_n:
        raise ValueError(f"volatility_regime_flag needs >= {history_n} monthly "
                         f"returns (got {len(rets)})")
    def _vol(series):
        return (sum(r * r for r in series) / len(series)) ** 0.5
    recent_vol = _vol(rets[-recent_n:])
    rolling = [_vol(rets[i:i + recent_n])
               for i in range(len(rets) - recent_n + 1)]
    baseline = rolling[-history_n:]
    b_mean, b_sd = mean(baseline), pstdev(baseline)
    if b_sd == 0:
        raise ValueError("baseline rolling-vol series has zero dispersion — "
                         "z-score is undefined")
    z = (recent_vol - b_mean) / b_sd
    return {"recent_vol": round(recent_vol, 4),
            "baseline_vol": round(b_mean, 4),
            "z_score": round(z, 4), "z_threshold": VOL_REGIME_Z_THRESHOLD,
            "regime_shift": abs(z) > VOL_REGIME_Z_THRESHOLD}


def market_cap_delta(class_specs):
    """Market-cap delta for (possibly) multi-class share structures (H-4).

    Reports 8/9 H-4: "shares outstanding x delta price" is ambiguous for
    GOOG/GOOGL and META A/B — using one class's shares with another's price
    misstates the cap change. Canonical method: compute each class separately
    and sum: delta_class = shares x (price_after - price_before).

    class_specs: list of dicts {"label", "shares", "price_before",
    "price_after"} — one entry per share class (single-class names pass one).
    Returns {delta, per_class: [{label, delta}], method}. Raises on
    non-positive shares or missing keys.
    """
    if not class_specs:
        raise ValueError("market_cap_delta needs >= 1 share-class spec")
    per_class, total = [], 0.0
    for spec in class_specs:
        label = str(spec.get("label", "?"))
        try:
            shares = float(spec["shares"])
            before = float(spec["price_before"])
            after = float(spec["price_after"])
        except (KeyError, TypeError, ValueError):
            raise ValueError(f"class {label!r}: shares/price_before/price_after "
                             "must be present and numeric")
        if shares <= 0:
            raise ValueError(f"class {label!r}: shares must be positive")
        d = shares * (after - before)
        per_class.append({"label": label, "delta": round(d, 2)})
        total += d
    return {"delta": round(total, 2), "per_class": per_class,
            "method": "sum of per-class shares x price delta (multi-class "
                      "disclosed, single-class trivially equal)"}


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

    # Round-4 (reports 8/9 M-7): beta regime diagnostics. Fixtures are
    # synthetic: a tight linear series (high R^2, no breakdown) and a
    # noise series (R^2 below the floor, breakdown flagged).
    tight_bench = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
    tight_stock = [2.0 + 1.2 * (b - 1.0) for b in tight_bench]  # beta 1.2, R^2=1
    dg = beta_diagnostics(tight_stock, tight_bench)
    check("beta diagnostics beta", dg["beta"], 1.2, 0.001)
    check("beta diagnostics r_squared", dg["r_squared"], 1.0, 0.001)
    if dg["correlation_breakdown"]:
        failures.append("a perfectly linear pair must not flag a breakdown")
    noise_stock = [2.0, -3.0, 1.0, 2.0, -3.0, 1.0]   # ~orthogonal to the bench
    dn = beta_diagnostics(noise_stock, tight_bench)
    if not dn["correlation_breakdown"]:
        failures.append("an uncorrelated pair (R^2 < 0.30) must flag a "
                        "correlation breakdown")
    if dn["r_squared"] >= R_SQUARED_FLOOR:
        failures.append("noise-pair R^2 must sit below the floor")
    for bad in ([[1.0, 2.0], [1.0, 2.0, 3.0]], [1.0], [1.0, 2.0]):
        try:
            beta_diagnostics(bad, bad)
            failures.append("length-mismatched / short series must raise")
        except ValueError:
            pass

    # Round-4 (reports 8/9 M-7): volatility regime. Calm history + a violent
    # trailing quarter must flag |z| > 2; the same history ending calm must
    # not. 24 synthetic monthly % returns, st. the last 3 triple the vol.
    calm = [2.0, -2.0, 1.9, -1.9, 2.1, -2.1, 2.0, -2.0, 1.8, -1.8, 2.2, -2.2,
            2.0, -2.0, 1.9, -1.9, 2.0, -2.0, 2.1, -2.1, 2.0]
    calm = calm[:21]  # 21 calm months
    spiking = calm + [6.0, -6.0, 7.0]  # trailing 3 months triple the vol
    vz = volatility_regime_flag(spiking)
    if not vz["regime_shift"]:
        failures.append(f"a tripling of trailing vol must flag a regime shift "
                        f"(z={vz['z_score']})")
    vz2 = volatility_regime_flag(calm + [2.0, -2.0, 2.0])
    if vz2["regime_shift"]:
        failures.append("in-regime trailing vol must not flag a shift")
    try:
        volatility_regime_flag(calm[:5])
        failures.append("a too-short series must raise ValueError")
    except ValueError:
        pass

    # Round-4 (reports 8/9 H-4): multi-class market-cap delta. Synthetic
    # GOOG/GOOGL-style fixture (not company figures).
    mc = market_cap_delta([
        {"label": "GOOGL A", "shares": 5.8, "price_before": 324.89,
         "price_after": 283.10},
        {"label": "GOOG C", "shares": 5.4, "price_before": 321.89,
         "price_after": 282.32},
    ])
    check("multi-class cap delta total", mc["delta"], -456.06, 0.2)
    if len(mc["per_class"]) != 2:
        failures.append("multi-class cap delta must return one row per class")
    single = market_cap_delta([
        {"label": "SINGLE", "shares": 12.1, "price_before": 321.89,
         "price_after": 282.32}])
    check("single-class cap delta", single["delta"], -478.80, 0.05)
    try:
        market_cap_delta([{"label": "X", "shares": 0, "price_before": 1,
                           "price_after": 2}])
        failures.append("non-positive shares must raise ValueError")
    except ValueError:
        pass

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
    print(f"Beta diagnostics (tight fixture): {dg}")   # beta 1.2, R^2 1.0
    print(f"Beta diagnostics (noise fixture): R^2={dn['r_squared']}, "
          f"breakdown={dn['correlation_breakdown']}")
    print(f"Vol regime (spike fixture): z={vz['z_score']}, "
          f"shift={vz['regime_shift']}")
    print(f"Market-cap delta (two-class fixture): {mc['delta']} "
          f"({mc['method']})")
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
