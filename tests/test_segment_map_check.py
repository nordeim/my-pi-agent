"""Regression tests for skills/bigtech-equity-research/scripts/segment_map_check.py.

Guards the round-3 fix for comparative reports 6/7 finding H-3 ("segment-map
staleness risk — advisory, not fail-safe"): a stale ASC 280 map produces a
confidently wrong variance table that still passes the numeric audit, because
nothing downstream catches a misattributed segment. The gate turns the prose
staleness rule into an exit code, and the machine-readable segment-maps.json
mirrors the markdown map.

Run from the repository root:  python3 -m pytest tests/ -v
"""
import importlib.util
import json
import pathlib
import subprocess
import sys

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = (REPO_ROOT / "skills" / "bigtech-equity-research" / "scripts" /
          "segment_map_check.py")
MAP_JSON = (REPO_ROOT / "skills" / "bigtech-equity-research" / "reference" /
            "segment-maps.json")
MAP_MD = (REPO_ROOT / "skills" / "bigtech-equity-research" / "reference" /
          "segment-maps.md")


@pytest.fixture(scope="module")
def smc():
    spec = importlib.util.spec_from_file_location("segment_map_check", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestGateLogic:
    def test_covered_filing_passes(self, smc, tmp_path):
        m = tmp_path / "map.json"
        m.write_text(json.dumps({
            "segment_map_version": "t",
            "last_verified_against_filing": {"forms": "FY2026 10-K",
                                             "verified_through": "2026-10-30"},
            "companies": {"GOOGL": {"reportable_segments": ["A", "B", "C"]}}
        }), encoding="utf-8")
        assert smc.check_map(m, "2026-10-28", company="GOOGL") == 0

    def test_postdating_filing_fails(self, smc, tmp_path):
        m = tmp_path / "map.json"
        m.write_text(json.dumps({
            "segment_map_version": "t",
            "last_verified_against_filing": {"forms": "FY2026 10-K",
                                             "verified_through": "2026-10-30"},
            "companies": {}
        }), encoding="utf-8")
        rc = smc.check_map(m, "2026-11-15")
        assert rc == 1

    def test_unknown_company_fails_with_extraction_path(self, smc, tmp_path):
        m = tmp_path / "map.json"
        m.write_text(json.dumps({
            "segment_map_version": "t",
            "last_verified_against_filing": {"forms": "FY2026 10-K",
                                             "verified_through": "2026-10-30"},
            "companies": {"GOOGL": {"reportable_segments": ["A"]}}
        }), encoding="utf-8")
        rc = smc.check_map(m, "2026-10-28", company="MSFT")
        assert rc == 1  # no cached expectation: extract from the filing directly

    def test_company_lookup_is_case_insensitive(self, smc, tmp_path):
        m = tmp_path / "map.json"
        m.write_text(json.dumps({
            "segment_map_version": "t",
            "last_verified_against_filing": {"forms": "FY2026 10-K",
                                             "verified_through": "2026-10-30"},
            "companies": {"GOOGL": {"reportable_segments": ["A"]}}
        }), encoding="utf-8")
        assert smc.check_map(m, "2026-10-28", company="googl") == 0

    def test_bad_date_is_usage_error(self, smc, tmp_path):
        m = tmp_path / "map.json"
        m.write_text(json.dumps({
            "segment_map_version": "t",
            "last_verified_against_filing": {"forms": "x",
                                             "verified_through": "2026-10-30"},
            "companies": {}
        }), encoding="utf-8")
        assert smc.check_map(m, "not-a-date") == 2


class TestBundledMap:
    """The shipped machine-readable map must mirror the markdown doctrine."""

    def test_map_json_parses_and_is_versioned(self):
        data = json.loads(MAP_JSON.read_text(encoding="utf-8"))
        assert data["segment_map_version"] == "2026-10"
        assert data["last_verified_against_filing"]["verified_through"] == "2026-10-30"

    def test_all_seven_companies_present(self):
        data = json.loads(MAP_JSON.read_text(encoding="utf-8"))
        for ticker in ("GOOGL", "MSFT", "AMZN", "AAPL", "META", "NVDA", "TSLA"):
            assert ticker in data["companies"], f"{ticker} missing from segment-maps.json"
            assert data["companies"][ticker]["reportable_segments"], (
                f"{ticker} must list its ASC 280 reportable segments")

    def test_json_companies_match_markdown_table(self):
        """The machine-readable mirror must not drift from the markdown map."""
        data = json.loads(MAP_JSON.read_text(encoding="utf-8"))
        md = MAP_MD.read_text(encoding="utf-8")
        for ticker, entry in data["companies"].items():
            for seg in entry["reportable_segments"]:
                assert seg in md, (
                    f"segment-maps.json lists {seg!r} for {ticker} but the "
                    "markdown map does not — the two files must change together")

    def test_gate_passes_against_bundled_map_for_covered_filings(self):
        p = subprocess.run(
            [sys.executable, str(SCRIPT), "--map", str(MAP_JSON),
             "--filing-date", "2026-10-28", "--company", "NVDA"],
            capture_output=True, text=True, cwd=str(REPO_ROOT))
        assert p.returncode == 0, p.stdout + p.stderr
        assert "Compute & Networking" in p.stdout

    def test_gate_fails_for_postdating_filing(self):
        p = subprocess.run(
            [sys.executable, str(SCRIPT), "--map", str(MAP_JSON),
             "--filing-date", "2026-11-15"],
            capture_output=True, text=True, cwd=str(REPO_ROOT))
        assert p.returncode == 1
        assert "STALE" in p.stdout


class TestSelftest:
    def test_module_selftest_returns_zero(self, smc):
        assert smc.selftest() == 0

    def test_cli_selftest_exits_zero(self):
        p = subprocess.run(
            [sys.executable, str(SCRIPT), "--selftest"],
            capture_output=True, text=True, cwd=str(REPO_ROOT))
        assert p.returncode == 0, p.stdout + p.stderr
        assert "SELFTEST: PASS" in p.stdout

    def test_missing_filing_date_is_usage_error(self):
        p = subprocess.run(
            [sys.executable, str(SCRIPT)],
            capture_output=True, text=True, cwd=str(REPO_ROOT))
        assert p.returncode == 2
