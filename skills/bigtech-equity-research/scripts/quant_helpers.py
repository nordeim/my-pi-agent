#!/usr/bin/env python3
"""Deterministic quant math for big-tech equity research. Avoids hand-arithmetic errors.

Usage:  python3 quant_helpers.py            # runs a self-test on the worked example
        import quant_helpers as qh          # or import individual functions
"""
from statistics import mean


def beat_miss_delta(actual, consensus):
    """Return (abs_delta, pct_delta)."""
    d = actual - consensus
    return d, (d / consensus * 100.0) if consensus else float("nan")


def abnormal_return(stock_ret, bench_ret):
    """Alpha = stock return minus benchmark return (same window), in pct points."""
    return stock_ret - bench_ret


def capex_ocf_ratio(capex, ocf):
    return capex / ocf * 100.0 if ocf else float("nan")


def ocf_shortfall(consensus_fcf, consensus_capex, actual_ocf):
    """When capex beats Street but FCF misses, the gap is operating cash flow."""
    implied_ocf = consensus_fcf + consensus_capex
    return implied_ocf - actual_ocf


def avg_pt_cut(pt_pairs):
    """pt_pairs = [(new_pt, old_pt), ...]. Returns mean % cut."""
    cuts = [(new - old) / old * 100.0 for new, old in pt_pairs]
    return mean(cuts)


def waterfall_check(weights, realized_move):
    """Validate that factor weights sum to the realized move."""
    total = sum(weights.values())
    return {"sum": round(total, 2), "matches": abs(total - abs(realized_move)) < 0.05}


if __name__ == "__main__":
    # Worked example: Alphabet Q3 2026
    rev_d, rev_p = beat_miss_delta(127.58, 128.22)
    eps_d, eps_p = beat_miss_delta(2.12, 3.02)
    print(f"Revenue delta: {rev_d:+.2f}B ({rev_p:+.2f}%)")      # −0.64B (−0.50%)
    print(f"EPS delta:     {eps_d:+.2f} ({eps_p:+.2f}%)")        # −0.90 (−29.80%)
    print(f"Alpha vs −1.5% beta: {abnormal_return(-12.6, -1.5):+.1f}pp")  # −11.1
    print(f"Capex/OCF: {capex_ocf_ratio(51.36, 42.29):.1f}%")    # 121.4%
    print(f"OCF shortfall: {ocf_shortfall(-2.70, 55.09, 42.29):+.2f}B")  # +10.10B
    pts = [(375, 425), (385, 435), (300, 350), (380, 430), (355, 440)]
    print(f"Avg PT cut: {avg_pt_cut(pts):+.1f}%")                # −13.7%
    wf = {"beta": 1.5, "fcf": 4.0, "eps": 2.8, "search": 2.5, "positioning": 1.8}
    print(f"Waterfall: {waterfall_check(wf, -12.6)}")            # sum 12.6, matches True
