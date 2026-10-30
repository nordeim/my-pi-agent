"""Regression tests for skills/analyzing-us-bigtech-stocks/scripts/fact_base_audit.py.

Guards audit finding H-4 (unanchored substring matching let absent numbers pass
the numeric gate) plus the script's self-test wiring and the L-4 fix (placeholder
scan sees visible text only, never <script>/<style> blocks).

Run from the repository root:  python3 -m pytest tests/ -v
"""
import importlib.util
import pathlib
import subprocess
import sys

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "skills" / "analyzing-us-bigtech-stocks" / "scripts" / "fact_base_audit.py"
EVIDENCE = REPO_ROOT / "docs" / "skills-audit" / "evidence" / "test_fact_base_audit_falsepass.py"


@pytest.fixture(scope="module")
def fba():
    """Load fact_base_audit.py as a module (it lives outside any package)."""
    spec = importlib.util.spec_from_file_location("fact_base_audit", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestTokenInAnchoring:
    """The H-4 false-pass hole, pinned at the unit level.

    Pre-fix, token_in() used unanchored substring matching, so a fact of 82.3
    satisfied itself against a slide printing $282.32 (exit 0). These tests fail
    if the anchoring is ever loosened again.
    """

    def test_substring_inside_larger_number_is_not_a_match(self, fba):
        # Audit case 1: fact 82.3 vs slide "$282.32"
        assert fba.token_in("82.3", fba.norm("$282.32")) is False

    def test_token_inside_negative_percent_is_not_a_match(self, fba):
        # Audit case 2: fact 12.29 vs slide "-112.29%" (unicode minus and hyphen)
        assert fba.token_in("12.29", fba.norm("\u2212112.29%")) is False
        assert fba.token_in("12.29", fba.norm("-112.29%")) is False

    def test_exact_token_matches(self, fba):
        assert fba.token_in("282.32", fba.norm("$282.32")) is True
        assert fba.token_in("-12.29", fba.norm("\u221212.29%")) is True

    def test_magnitude_fallback_matches_sign_flip(self, fba):
        # Slide prints "erased $482B" for a fact recorded as -482.
        assert fba.token_in("-482", fba.norm("$482B erased")) is True
        assert fba.token_in("-9.1", fba.norm("-$9.1B")) is True

    def test_numeric_equality_matches_trailing_zero(self, fba):
        assert fba.token_in("9.10", fba.norm("$9.1B")) is True

    def test_absent_number_stays_absent(self, fba):
        assert fba.token_in("63.4", fba.norm("$282.32")) is False


class TestNumericTokens:
    def test_plain_number(self, fba):
        assert fba.numeric_tokens(282.32) == ["282.32"]

    def test_symbol_broken_sign_degrades_to_magnitude(self, fba):
        # "-" separated from the digits by "$" is not captured; token_in()'s
        # magnitude fallback covers the sign either way.
        assert fba.numeric_tokens("-$9.1B") == ["9.1"]

    def test_non_numeric_yields_no_tokens(self, fba):
        assert fba.numeric_tokens("n/a") == []
        assert fba.numeric_tokens(None) == []
        assert fba.numeric_tokens(True) == []


class TestPlaceholderScanScope:
    """The L-4 fix: scan visible text only, not <script>/<style> blocks."""

    def test_visible_todo_is_flagged(self, fba):
        fails = fba.scan_placeholders(
            {"slide_01.html": "<html><body><p>TODO fill in</p></body></html>"})
        assert any("todo" in f for f in fails)

    def test_css_class_placeholder_is_not_flagged(self, fba):
        fails = fba.scan_placeholders({
            "slide_01.html":
            "<html><head><style>.placeholder{color:red}</style></head>"
            "<body><p>Close: $282.32</p></body></html>"})
        assert fails == []

    def test_js_undefined_token_is_not_flagged(self, fba):
        fails = fba.scan_placeholders({
            "slide_01.html":
            "<html><head><script>var undefined = 1;</script></head>"
            "<body><p>Move: -12.29%</p></body></html>"})
        assert fails == []


class TestStrictComplianceModes:
    """Report-3 M2 / report-4 #3: opt-in strict modes for institutional builds.

    --strict-verified     every `Verified` fact needs >=2 cross_checked_with
    --decision-critical   named fact IDs need >=2 cross-checks (CLI form of
                           meta.decision_critical)
    --fail-on-unverified  reverse-check candidates become failures

    The modes are opt-in by design (report-4's reconciliation of report-3's
    strict-by-default proposal): the default run must NOT enforce them.
    """

    @pytest.fixture(scope="class")
    def fb(self):
        return {
            "meta": {"method_page": "slide_01.html", "decision_critical": ["F-9"]},
            "facts": [
                {"id": "F-1", "value": 1.0, "confidence": "Verified",
                 "cross_checked_with": ["F-2"], "slide_pages": ["slide_01.html"]},
                {"id": "F-2", "value": 2.0, "confidence": "Verified",
                 "cross_checked_with": ["F-1", "F-3"],
                 "slide_pages": ["slide_01.html"]},
                {"id": "F-9", "value": 9.0, "confidence": "Verified",
                 "cross_checked_with": [], "slide_pages": ["slide_01.html"]},
            ],
        }

    @pytest.fixture(scope="class")
    def slides(self, tmp_path_factory):
        d = tmp_path_factory.mktemp("strict")
        (d / "slide_01.html").write_text(
            "<html><body><p>1.0 2.0 9.0 — and an unsourced $103% figure.</p></body></html>",
            encoding="utf-8")
        return d

    def _run(self, fba, slides, fb, *extra):
        import json as _json
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            fbp = pathlib.Path(td) / "fb.json"
            fbp.write_text(_json.dumps(fb), encoding="utf-8")
            rp = pathlib.Path(td) / "r.json"
            code = fba.main(["--slides", str(slides), "--fact-base", str(fbp),
                             "--report", str(rp), *extra])
            report = _json.loads(rp.read_text())
        return code, report

    def test_default_run_enforces_nothing_strict(self, fba, slides, fb):
        code, report = self._run(fba, slides, fb)
        # F-1 (Verified, 1 cross-check) and F-9 (decision-critical via meta!) ...
        # meta.decision_critical IS enforced by default:
        assert any("F-9" in f and "CROSSCHECK" in f for f in report["failures"])
        # ... but plain Verified facts are not:
        assert not any("F-1" in f and "CROSSCHECK" in f for f in report["failures"])
        # ... and unverified candidates stay advisory, not failures:
        assert not any("UNVERIFIED" in f for f in report["failures"])
        assert code == 1  # F-9 cross-check failure

    def test_strict_verified_enforces_double_sourcing(self, fba, slides, fb):
        code, report = self._run(fba, slides, fb, "--strict-verified")
        assert any("F-1" in f and "CROSSCHECK" in f for f in report["failures"]), (
            "--strict-verified must fail a Verified fact with <2 cross-checks")
        assert not any("F-2" in f and "CROSSCHECK" in f for f in report["failures"]), (
            "a fact with 2 cross-checks must pass strict mode")

    def test_fail_on_unverified_promotes_candidates(self, fba, slides, fb):
        code, report = self._run(fba, slides, fb, "--fail-on-unverified")
        assert any("UNVERIFIED" in f and "103" in f for f in report["failures"]), (
            "--fail-on-unverified must promote the unsourced $103% figure to a failure")

    def test_decision_critical_cli_list(self, fba, slides, fb):
        import copy
        fb2 = copy.deepcopy(fb)
        del fb2["meta"]["decision_critical"]
        code, report = self._run(fba, slides, fb2, "--decision-critical", "F-1")
        assert any("F-1" in f and "CROSSCHECK" in f for f in report["failures"]), (
            "--decision-critical F-1 must enforce the >=2 rule without meta/strict")

    def test_cross_check_unit_function(self, fba):
        fb = {"meta": {}, "facts": [
            {"id": "A", "confidence": "Verified", "cross_checked_with": ["x"]},
            {"id": "B", "confidence": "Verified", "cross_checked_with": ["x", "y"]},
            {"id": "C", "confidence": "Reasoned", "cross_checked_with": []},
        ]}
        fails = fba.check_cross_checks(fb, strict_verified=True, extra_ids="")
        assert [f.split()[1] for f in fails] == ["A"]
        fails = fba.check_cross_checks(fb, strict_verified=False, extra_ids="C")
        assert [f.split()[1] for f in fails] == ["C"]
        assert fba.check_cross_checks(fb, strict_verified=False, extra_ids="") == []


class TestSelftest:
    def test_module_selftest_returns_zero(self, fba):
        assert fba.selftest() == 0

    def test_cli_selftest_exits_zero(self):
        p = subprocess.run(
            [sys.executable, str(SCRIPT), "--selftest"],
            capture_output=True, text=True, cwd=str(REPO_ROOT))
        assert p.returncode == 0, p.stdout + p.stderr
        assert "SELFTEST: PASS" in p.stdout


class TestEvidenceHarness:
    """docs/skills-audit/evidence/ — the H-4 reproduction script.

    Post-fix it asserts the hole is closed: both evasion cases must exit 1
    (MISSING) and the controls must behave. It must exit 0 as a whole.
    """

    def test_evidence_harness_passes_against_fixed_script(self):
        if not EVIDENCE.exists():
            pytest.skip("evidence harness not present in this checkout")
        p = subprocess.run(
            [sys.executable, str(EVIDENCE)],
            capture_output=True, text=True, cwd=str(REPO_ROOT))
        assert p.returncode == 0, p.stdout + p.stderr
        assert "H-4" in p.stdout
