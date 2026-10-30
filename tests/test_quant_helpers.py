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
        assert qh.abnormal_return(-12.29, -1.5) == pytest.approx(-10.79, abs=0.005)
        assert qh.abnormal_return(-12.29, -1.5, beta=1.2) == pytest.approx(-10.49, abs=0.005)

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
