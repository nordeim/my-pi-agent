"""Regression tests for skills/bigtech-equity-research/scripts/quant_helpers.py.

Guards audit finding M-4: the helper's self-test printed values without
asserting (silent regressions shipped), avg_pt_cut had no empty-input contract,
and the OCF-shortfall sign convention disagreed between code (+10.10B) and
formulas.md (-10.10B). These tests pin the asserting self-test, the
zero-division and empty-input contracts, the sign conventions, and the
doc/code agreement on the worked example.

Run from the repository root:  python3 -m pytest tests/ -v
"""
import importlib.util
import pathlib
import re
import subprocess
import sys

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "skills" / "bigtech-equity-research" / "scripts" / "quant_helpers.py"
FORMULAS_MD = REPO_ROOT / "skills" / "bigtech-equity-research" / "reference" / "formulas.md"


@pytest.fixture(scope="module")
def qh():
    spec = importlib.util.spec_from_file_location("quant_helpers", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def norm_doc(text: str) -> str:
    """Normalize formulas.md for matching: dashes, currency, bold markers."""
    return (text.replace("\u2212", "-").replace("\u2013", "-")
                .replace("$", "").replace("**", ""))


class TestSelftest:
    def test_module_selftest_returns_zero(self, qh):
        assert qh._selftest() == 0

    def test_cli_selftest_exits_zero(self):
        p = subprocess.run(
            [sys.executable, str(SCRIPT)],
            capture_output=True, text=True, cwd=str(REPO_ROOT))
        assert p.returncode == 0, p.stdout + p.stderr
        assert "SELFTEST: PASS" in p.stdout


class TestZeroDivisionAndEmptyInputs:
    def test_beat_miss_delta_rejects_zero_consensus(self, qh):
        with pytest.raises(ValueError):
            qh.beat_miss_delta(1.0, 0)

    def test_capex_ocf_ratio_rejects_zero_ocf(self, qh):
        with pytest.raises(ValueError):
            qh.capex_ocf_ratio(1.0, 0)

    def test_avg_pt_cut_rejects_empty_input(self, qh):
        with pytest.raises(Exception):
            qh.avg_pt_cut([])


class TestBetaWindowContract:
    """Report-3 M1 (confirmed by report-4) + round-3 refinement (reports 6/7 H-2):
    the canonical default window is applied when beta is supplied without one
    (comparability across runs), echoed with its source; an unusable explicit
    window still raises — the disclosure is the point, now with a default."""

    def test_beta_without_window_uses_canonical_default(self, qh):
        r = qh.abnormal_return(-12.29, -1.5, beta=1.2)
        assert r["excess"] == pytest.approx(-10.49, abs=0.005)
        assert r["beta_window"] == qh.DEFAULT_BETA_WINDOW
        assert r["beta_window_source"] == "canonical default"
        assert "2-year monthly returns vs QQQ" in r["beta_window"]

    def test_canonical_default_window_constant(self, qh):
        assert "2-year monthly" in qh.DEFAULT_BETA_WINDOW
        assert "QQQ" in qh.DEFAULT_BETA_WINDOW

    def test_blank_window_raises(self, qh):
        with pytest.raises(ValueError):
            qh.abnormal_return(-12.29, -1.5, beta=1.2, beta_window="   ")

    def test_non_string_window_raises(self, qh):
        with pytest.raises(ValueError):
            qh.abnormal_return(-12.29, -1.5, beta=1.2, beta_window=250)

    def test_explicit_window_is_echoed_as_explicit(self, qh):
        r = qh.abnormal_return(-12.29, -1.5, beta=1.2,
                               beta_window="250 sessions vs QQQ, through 2026-10-27")
        assert r["beta_window_source"] == "explicit"
        assert "250 sessions" in r["beta_window"]

    def test_market_adjusted_needs_no_window(self, qh):
        # The beta=1 convention has nothing to disclose — must keep working.
        r = qh.abnormal_return(-12.29, -1.5)
        assert r["excess"] == pytest.approx(-10.79, abs=0.005)
        assert r["beta_window_source"] is None

    def test_percent_multiplier_constant_used(self, qh):
        # Report-3 L2: no magic 100.0 — conversions go through the named constant.
        assert qh.PERCENT_MULTIPLIER == 100.0
        src = SCRIPT.read_text(encoding="utf-8")
        assert src.count("PERCENT_MULTIPLIER") >= 4, (
            "percent conversions must use the PERCENT_MULTIPLIER constant, not "
            "repeated magic 100.0 literals")


class TestSignConventions:
    def test_ocf_shortfall_sign_convention(self, qh):
        # Positive = actual OCF below the consensus-implied level (the M-4 fix:
        # +10.10B, not -10.10B).
        assert qh.ocf_shortfall(-2.70, 55.09, 42.29) == pytest.approx(10.10, abs=0.005)

    def test_beat_miss_delta_signs(self, qh):
        d, p = qh.beat_miss_delta(127.58, 128.22)
        assert d == pytest.approx(-0.64, abs=0.005)
        assert p == pytest.approx(-0.50, abs=0.005)

    def test_abnormal_return_both_conventions(self, qh):
        # v1.4 contract: abnormal_return returns a dict echoing the convention,
        # the estimation window, and whether the window was canonical or explicit.
        r = qh.abnormal_return(-12.29, -1.5)
        assert r["excess"] == pytest.approx(-10.79, abs=0.005)
        assert r["convention"] == "market-adjusted"
        assert r["beta"] is None
        r = qh.abnormal_return(-12.29, -1.5, beta=1.2,
                               beta_window="250 sessions vs QQQ, through 2026-10-27")
        assert r["excess"] == pytest.approx(-10.49, abs=0.005)
        assert r["convention"] == "beta-adjusted"
        assert r["beta"] == 1.2
        assert "250 sessions" in r["beta_window"]
        assert r["beta_window_source"] == "explicit"

    def test_waterfall_sign_flip_regression(self, qh):
        """A sign-flipped decomposition must NOT match a negative realized move
        (the pre-fix abs() bug)."""
        wf = {"benchmark": -1.5, "fcf_capex": -3.9, "eps_quality": -2.7,
              "search": -2.4, "positioning": -1.8}
        flipped = {k: -v for k, v in wf.items()}
        assert qh.waterfall_check(flipped, -12.29)["matches"] is False

    def test_waterfall_consistent_allocation_matches(self, qh):
        wf = {"benchmark": -1.5, "fcf_capex": -3.9, "eps_quality": -2.7,
              "search": -2.4, "positioning": -1.8}
        r = qh.waterfall_check(wf, -12.29)
        assert r["sum"] == pytest.approx(-12.3, abs=0.05)
        assert r["matches"] is True


class TestRound3Helpers:
    """Round-3 additions (reports 6/7): FCF ex-SBC pairing and the
    segment-variance row."""

    def test_fcf_canonical_print(self, qh):
        # Alphabet Q3 2026: OCF 42.29, capex 51.36 -> the canonical −9.07.
        assert qh.fcf(42.29, 51.36) == pytest.approx(-9.07, abs=0.005)

    def test_fcf_ex_sbc_subtracts_sbc(self, qh):
        # Synthetic fixtures (not company figures).
        assert qh.fcf_ex_sbc(42.29, 51.36, 6.50) == pytest.approx(-15.57, abs=0.005)
        assert qh.fcf_ex_sbc(42.29, 51.36, 0) == qh.fcf(42.29, 51.36)

    def test_segment_variance_row(self, qh):
        sv = qh.segment_variance(110.0, 100.0, 100.0, 50.0)
        assert sv["delta_abs"] == pytest.approx(10.0)
        assert sv["delta_pct"] == pytest.approx(10.0)
        assert sv["qoq"] == pytest.approx(10.0)
        assert sv["yoy"] == pytest.approx(120.0)

    def test_segment_variance_rejects_zero_base(self, qh):
        with pytest.raises(ValueError):
            qh.segment_variance(110.0, 0.0, 100.0, 50.0)
        with pytest.raises(ValueError):
            qh.segment_variance(110.0, 100.0, 0.0, 50.0)
        with pytest.raises(ValueError):
            qh.segment_variance(110.0, 100.0, 100.0, 0.0)


class TestRound4Helpers:
    """Round-4 additions (reports 8/9): beta regime diagnostics (M-7) and the
    multi-class market-cap delta (H-4). Fixtures are synthetic."""

    # --- beta_diagnostics -------------------------------------------------

    def test_beta_diagnostics_regresses_stock_on_bench(self, qh):
        # stock = 0.8 + 1.2 x bench -> slope 1.2, R^2 = 1 (the slope must be
        # cov/var(bench), NOT the reverse regression cov/var(stock)).
        bench = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
        stock = [2.0 + 1.2 * (b - 1.0) for b in bench]
        dg = qh.beta_diagnostics(stock, bench)
        assert dg["beta"] == pytest.approx(1.2, abs=0.001)
        assert dg["r_squared"] == pytest.approx(1.0, abs=0.001)
        assert dg["correlation_breakdown"] is False

    def test_beta_diagnostics_flags_correlation_breakdown(self, qh):
        bench = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
        noise = [2.0, -3.0, 1.0, 2.0, -3.0, 1.0]     # ~orthogonal to the bench
        dn = qh.beta_diagnostics(noise, bench)
        assert dn["r_squared"] < qh.R_SQUARED_FLOOR
        assert dn["correlation_breakdown"] is True, (
            "R^2 below the floor must flag the regime diagnostic (M-7)")

    def test_beta_diagnostics_floor_constant(self, qh):
        assert qh.R_SQUARED_FLOOR == 0.30
        assert qh.VOL_REGIME_Z_THRESHOLD == 2.0

    def test_beta_diagnostics_rejects_malformed_series(self, qh):
        with pytest.raises(ValueError):
            qh.beta_diagnostics([1.0, 2.0], [1.0, 2.0, 3.0])
        with pytest.raises(ValueError):
            qh.beta_diagnostics([1.0], [1.0])
        with pytest.raises(ValueError):
            qh.beta_diagnostics([1.0, 1.0, 1.0], [2.0, 2.0, 2.0])  # zero bench var

    # --- volatility_regime_flag -------------------------------------------

    def test_vol_regime_flags_spike(self, qh):
        calm = [2.0, -2.0, 1.9, -1.9, 2.1, -2.1, 2.0, -2.0, 1.8, -1.8,
                2.2, -2.2, 2.0, -2.0, 1.9, -1.9, 2.0, -2.0, 2.1, -2.1, 2.0]
        spiking = calm + [6.0, -6.0, 7.0]           # trailing quarter triples vol
        vz = qh.volatility_regime_flag(spiking)
        assert vz["regime_shift"] is True
        assert abs(vz["z_score"]) > qh.VOL_REGIME_Z_THRESHOLD

    def test_vol_regime_calm_history_stays_in_regime(self, qh):
        calm = [2.0, -2.0, 1.9, -1.9, 2.1, -2.1, 2.0, -2.0, 1.8, -1.8,
                2.2, -2.2, 2.0, -2.0, 1.9, -1.9, 2.0, -2.0, 2.1, -2.1, 2.0]
        vz = qh.volatility_regime_flag(calm + [2.0, -2.0, 2.0])
        assert vz["regime_shift"] is False

    def test_vol_regime_rejects_short_series(self, qh):
        with pytest.raises(ValueError):
            qh.volatility_regime_flag([1.0, 2.0, 3.0])

    # --- market_cap_delta ---------------------------------------------------

    def test_multi_class_cap_delta_sums_per_class(self, qh):
        mc = qh.market_cap_delta([
            {"label": "A", "shares": 5.8, "price_before": 324.89,
             "price_after": 283.10},
            {"label": "C", "shares": 5.4, "price_before": 321.89,
             "price_after": 282.32},
        ])
        # 5.8 x -41.79 = -242.38; 5.4 x -39.57 = -213.68; total -456.06.
        assert mc["delta"] == pytest.approx(-456.06, abs=0.01)
        assert [c["delta"] for c in mc["per_class"]] == [
            pytest.approx(-242.38, abs=0.01), pytest.approx(-213.68, abs=0.01)]
        assert "per-class" in mc["method"] or "sum" in mc["method"]

    def test_single_class_cap_delta_matches_shares_times_delta(self, qh):
        single = qh.market_cap_delta([
            {"label": "SINGLE", "shares": 12.1, "price_before": 321.89,
             "price_after": 282.32}])
        assert single["delta"] == pytest.approx(12.1 * (282.32 - 321.89),
                                                abs=0.01)

    def test_market_cap_delta_rejects_bad_specs(self, qh):
        with pytest.raises(ValueError):
            qh.market_cap_delta([])
        with pytest.raises(ValueError):
            qh.market_cap_delta([{"label": "X", "shares": 0,
                                  "price_before": 1, "price_after": 2}])
        with pytest.raises(ValueError):
            qh.market_cap_delta([{"label": "X", "price_before": 1,
                                  "price_after": 2}])   # shares missing


class TestVendoringParity:
    """Round 4 (reports 8/9 M-5): quant_helpers.py is vendored byte-identical
    into all three family skills — the postmortem is standalone again."""

    SCRIPTS = [
        REPO_ROOT / "skills" / "analyzing-us-bigtech-stocks" / "scripts" /
        "quant_helpers.py",
        REPO_ROOT / "skills" / "big-tech-earnings-postmortem" / "scripts" /
        "quant_helpers.py",
        REPO_ROOT / "skills" / "bigtech-equity-research" / "scripts" /
        "quant_helpers.py",
    ]

    def test_quant_helpers_vendored_byte_identical_x3(self):
        bodies = [p.read_bytes() for p in self.SCRIPTS]
        assert all(bodies), "a quant_helpers.py copy is missing"
        assert len(set(bodies)) == 1, (
            "quant_helpers.py drifted across the family — vendoring is "
            "byte-identical by design (reports 8/9 M-5)")

    def test_vendored_copies_selftest_exit_zero(self):
        import subprocess
        for p in self.SCRIPTS:
            proc = subprocess.run([sys.executable, str(p)],
                                  capture_output=True, text=True,
                                  cwd=str(REPO_ROOT))
            assert proc.returncode == 0, (
                f"{p.name} in {p.parent.parent.name}: selftest failed — "
                f"{proc.stdout}{proc.stderr}")


class TestFormulasDocAgreement:
    """M-4's documentation half: formulas.md must state the numbers the code
    computes — inputs extracted from the doc, outputs recomputed by the module
    and required to appear in the doc."""

    @pytest.fixture(scope="class")
    def doc(self):
        return norm_doc(FORMULAS_MD.read_text(encoding="utf-8"))

    def test_header_pins_canonical_print(self, doc):
        assert "close 282.32 on 2026-10-29" in doc
        assert "-12.29% from the 321.89 prior close" in doc

    def test_revenue_delta_doc_agrees_with_code(self, qh, doc):
        m = re.search(r"revenue\): (\d+\.\d+) - (\d+\.\d+) = (-\d+\.\d+)B", doc)
        assert m, "formulas.md revenue example not found"
        actual, consensus = float(m.group(1)), float(m.group(2))
        d, p = qh.beat_miss_delta(actual, consensus)
        assert d == pytest.approx(float(m.group(3)), abs=0.005)
        assert f"{d:.2f}B" in doc
        assert f"{p:.2f}%" in doc

    def test_eps_delta_doc_agrees_with_code(self, qh, doc):
        m = re.search(r"EPS\): (\d+\.\d+) - (\d+\.\d+) = (-\d+\.\d+);", doc)
        assert m, "formulas.md EPS example not found"
        d, p = qh.beat_miss_delta(float(m.group(1)), float(m.group(2)))
        assert d == pytest.approx(float(m.group(3)), abs=0.005)
        assert f"{d:.2f}" in doc
        assert f"{p:.1f}%" in doc

    def test_ocf_shortfall_doc_agrees_with_code(self, qh, doc):
        # The exact M-4 discrepancy: doc must show the full chain with the
        # code's sign convention (+10.10B), including the 52.39 intermediate.
        got = qh.ocf_shortfall(-2.70, 55.09, 42.29)
        assert got == pytest.approx(10.10, abs=0.005)
        assert "52.39 - 42.29" in doc
        assert "+10.10B" in doc

    def test_capex_ocf_doc_agrees_with_code(self, qh, doc):
        m = re.search(r"(\d+\.\d+) / (\d+\.\d+) = (\d+\.\d+)%", doc)
        assert m, "formulas.md capex/OCF example not found"
        got = qh.capex_ocf_ratio(float(m.group(1)), float(m.group(2)))
        assert got == pytest.approx(float(m.group(3)), abs=0.05)
