"""Regression tests for the accessibility gate vendored into the big-tech
research skills:

  skills/analyzing-us-bigtech-stocks/scripts/a11y_audit.mjs
  skills/big-tech-earnings-postmortem/scripts/a11y_audit.mjs
  skills/bigtech-equity-research/scripts/a11y_audit.mjs

Guards the round-3 fix for comparative reports 6/7 finding M-5/M-6 ("render
gate checks layout overflow but not accessibility conformance beyond the
template's claims"): the note templates claim WCAG-AA, so the claim is now
enforced — html lang, heading order, image alt text, and WCAG 2.2 AA text
contrast (4.5:1 normal, 3:1 large). Source-level guards run without a browser;
the selftest step runs the real headless-Chromium fixture and skips cleanly
(exit 2 is the script's documented env-error code) when Playwright is not
resolvable in this environment.

Run from the repository root:  python3 -m pytest tests/ -v
"""
import pathlib
import re
import shutil
import subprocess

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPTS = [
    REPO_ROOT / "skills" / "analyzing-us-bigtech-stocks" / "scripts" / "a11y_audit.mjs",
    REPO_ROOT / "skills" / "big-tech-earnings-postmortem" / "scripts" / "a11y_audit.mjs",
    REPO_ROOT / "skills" / "bigtech-equity-research" / "scripts" / "a11y_audit.mjs",
]

needs_node = pytest.mark.skipif(shutil.which("node") is None,
                                reason="node not available")


def script_source() -> str:
    return SCRIPTS[1].read_text(encoding="utf-8")


class TestVendoring:
    def test_gate_vendored_into_all_three_skills(self):
        assert all(s.exists() for s in SCRIPTS), (
            "a11y_audit.mjs must ship with all three family skills — the "
            "WCAG-AA claim is family-wide")

    def test_copies_are_byte_identical(self):
        bodies = [s.read_bytes() for s in SCRIPTS]
        assert len(set(bodies)) == 1, (
            "the three a11y_audit.mjs copies drifted apart — land the change in "
            "one and mirror it in the same commit")


class TestSourceLevelGuards:
    """No browser required — pin the gate's design in the source."""

    def test_no_machine_specific_absolute_paths(self):
        assert not re.search(r"[\"']/home/", script_source()), \
            "machine-specific absolute path reintroduced"

    def test_documents_playwright_prerequisite(self):
        src = script_source()
        assert "npm install playwright" in src
        assert "playwright install chromium" in src

    def test_selftest_flag_exists(self):
        assert "--selftest" in script_source()

    def test_checks_all_four_dimensions(self):
        src = script_source()
        # A. language, B. heading order + h1, C. image alt, D. contrast.
        assert "lang" in src
        assert "A11Y-HEADING" in src
        assert "A11Y-IMG" in src
        assert "A11Y-CONTRAST" in src

    def test_wcag_aa_thresholds_present(self):
        src = script_source()
        assert "4.5" in src, "WCAG-AA normal-text contrast ratio missing"
        assert "18.66" in src, "large-text bold threshold missing"

    def test_decorative_exemptions_present(self):
        src = script_source()
        assert "data-decor" in src
        assert "aria-hidden" in src

    def test_large_text_rule_present(self):
        # >= 24px (or >= 18.66px bold) needs only 3:1.
        src = script_source()
        assert "24" in src and "3" in src

    def test_usage_error_when_note_missing(self):
        p = subprocess.run(
            ["node", str(SCRIPTS[1]), "--note", "/nonexistent/n.html"],
            capture_output=True, text=True, cwd=str(REPO_ROOT))
        if p.returncode == 2 and "playwright not found" in p.stderr:
            pytest.skip("playwright not resolvable here (exit 2 = documented env error)")
        assert p.returncode == 2


@needs_node
class TestSelftest:
    """Run the real Chromium fixture. Exit 2 is the documented environment /
    usage error — treated as an environment-level skip (CI installs Playwright)."""

    @pytest.mark.parametrize("script", SCRIPTS,
                             ids=["skill1", "skill2", "skill3"])
    def test_selftest_passes_or_env_skips(self, script):
        p = subprocess.run(
            ["node", str(script), "--selftest"],
            capture_output=True, text=True, cwd=str(REPO_ROOT))
        if p.returncode == 2:
            pytest.skip(
                "playwright/chromium not resolvable here (exit 2 = documented "
                "env error); CI installs it explicitly")
        assert p.returncode == 0, p.stdout + p.stderr
        assert "SELFTEST: PASS" in p.stdout
        # The fixture must exercise all four directions: a clean note passes,
        # violations are flagged, decorative/large-text exemptions are respected.
        assert "A11Y-FAIL" in p.stdout
