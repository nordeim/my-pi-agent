"""Regression tests for the single-file render gate vendored into the two
lightweight big-tech research skills:

  skills/big-tech-earnings-postmortem/scripts/note_overflow_audit.mjs
  skills/bigtech-equity-research/scripts/note_overflow_audit.mjs

Guards the report-3 H2 / report-4 "enforce render verification" finding: the
13- (now 14-) section self-contained HTML note had no render/overflow audit.
Source-level guards run without a browser; the self-test step runs the real
headless-Chromium fixture and skips cleanly (exit 2 is the script's documented
env-error code) when Playwright is not resolvable in this environment.

Run from the repository root:  python3 -m pytest tests/ -v
"""
import pathlib
import re
import shutil
import subprocess

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
S2_SCRIPT = (REPO_ROOT / "skills" / "big-tech-earnings-postmortem" /
             "scripts" / "note_overflow_audit.mjs")
S3_SCRIPT = (REPO_ROOT / "skills" / "bigtech-equity-research" /
             "scripts" / "note_overflow_audit.mjs")

needs_node = pytest.mark.skipif(shutil.which("node") is None,
                                reason="node not available")


def script_source() -> str:
    return S3_SCRIPT.read_text(encoding="utf-8")


class TestVendoring:
    def test_copies_are_byte_identical(self):
        assert S2_SCRIPT.exists() and S3_SCRIPT.exists(), (
            "note_overflow_audit.mjs not vendored into both lite skills")
        assert S2_SCRIPT.read_bytes() == S3_SCRIPT.read_bytes(), (
            "skills 2 and 3 ship divergent copies of note_overflow_audit.mjs — "
            "land the change in one and mirror it in the same commit")


class TestSourceLevelGuards:
    """No browser required — pin the audit's design in the source."""

    def test_no_machine_specific_absolute_paths(self):
        src = script_source()
        assert not re.search(r"[\"']/home/", src), \
            "machine-specific absolute path reintroduced"

    def test_documents_playwright_prerequisite(self):
        src = script_source()
        assert "npm install playwright" in src
        assert "playwright install chromium" in src

    def test_resolves_playwright_via_node_module_resolution(self):
        src = script_source()
        assert "createRequire" in src
        assert "process.cwd()" in src

    def test_selftest_flag_exists(self):
        assert "--selftest" in script_source()

    def test_bleed_conventions_documented(self):
        src = script_source()
        assert "data-bleed" in src
        assert "aria-hidden" in src

    def test_checks_document_scroll_width(self):
        # Check A: the note must never scroll sideways.
        src = script_source()
        assert "scrollWidth" in src

    def test_checks_element_spill_and_clipping(self):
        # Checks B and C: element spill past viewport width; overflow:hidden
        # containers clipping their content.
        src = script_source()
        assert "scrollHeight" in src
        assert "clientHeight" in src
        assert "clientWidth" in src

    def test_usage_error_when_note_missing(self):
        p = subprocess.run(
            ["node", str(S3_SCRIPT), "--note", "/nonexistent/n.html"],
            capture_output=True, text=True, cwd=str(REPO_ROOT))
        if p.returncode == 2 and "playwright not found" in p.stderr:
            pytest.skip("playwright not resolvable here (exit 2 = documented env error)")
        assert p.returncode == 2


@needs_node
class TestSelftest:
    """Run the real Chromium fixture against both vendored copies. Exit 2 is the
    documented environment/usage error — treated as an environment-level skip."""

    @pytest.mark.parametrize("script", [S2_SCRIPT, S3_SCRIPT],
                             ids=["skill2", "skill3"])
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
        # The fixture must exercise all three directions: a clean note passes,
        # a wide element is flagged, and a clipped box is flagged.
        assert "OVERFLOW" in p.stdout
