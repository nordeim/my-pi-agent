"""Regression tests for skills/analyzing-us-bigtech-stocks/scripts/overflow_audit.mjs.

Guards audit finding M-1 (overflow was measured against the browser viewport
instead of the slide element's own origin, so unreset body margins caused false
positives) and M-7 (the Playwright prerequisite was implicit and the script
hardcoded a machine-specific absolute path). Source-level guards run without a
browser; the self-test step runs the real headless-Chromium fixture and skips
cleanly (not fails) when Playwright is not resolvable in this environment.

Run from the repository root:  python3 -m pytest tests/ -v
"""
import pathlib
import re
import shutil
import subprocess

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = (REPO_ROOT / "skills" / "analyzing-us-bigtech-stocks" /
          "scripts" / "overflow_audit.mjs")

needs_node = pytest.mark.skipif(shutil.which("node") is None,
                                reason="node not available")


def script_source() -> str:
    return SCRIPT.read_text(encoding="utf-8")


class TestSourceLevelGuards:
    """No browser required — these pin the M-1/M-7 fixes in the source."""

    def test_no_machine_specific_absolute_paths(self):
        # M-1 regression: the script once hardcoded /home/<user>/... paths.
        src = script_source()
        assert not re.search(r"[\"']/home/", src), \
            "machine-specific absolute path reintroduced"

    def test_measures_against_slide_element_origin(self):
        # M-1 core fix: coordinates relative to the .slide box, not the viewport.
        src = script_source()
        assert ".slide" in src
        assert "getBoundingClientRect" in src
        assert re.search(r"slide['\s-]+origin|relative to the\s+`?\.slide", src, re.I), \
            "slide-origin measurement rationale no longer documented"

    def test_documents_playwright_prerequisite(self):
        # M-7: the dependency must be stated where failures point to it.
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


@needs_node
class TestSelftest:
    """Run the real Chromium fixture. Exit 2 is the script's documented
    environment/usage error — treated as an environment-level skip."""

    def test_selftest_passes_or_env_skips(self):
        p = subprocess.run(
            ["node", str(SCRIPT), "--selftest"],
            capture_output=True, text=True, cwd=str(REPO_ROOT))
        if p.returncode == 2:
            pytest.skip(
                "playwright/chromium not resolvable here (exit 2 = documented "
                "env error); CI installs it explicitly")
        assert p.returncode == 0, p.stdout + p.stderr
        assert "SELFTEST: PASS" in p.stdout
        # The fixture must exercise both directions: a clean slide passes and a
        # genuinely overflowing element is flagged.
        assert "OVERFLOW" in p.stdout
