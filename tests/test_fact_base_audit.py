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
