"""Regression tests for the lite delivery gate vendored into the two lightweight
big-tech research skills:

  skills/big-tech-earnings-postmortem/scripts/note_audit.py
  skills/bigtech-equity-research/scripts/note_audit.py

Guards the report-3/4/5 convergent finding (skills 2 and 3 stated strict rules
but shipped no executable gate — R3-C1, R4 enforcement gap, R5 H-1): the
placeholder scan, the disclosure-needle checks (including the conditional
"Reasoned allocation" label — R5 M-3 — and the beta estimation-window needle —
R3 M1's doc-side counterpart), the verification-status requirement (R4 #5),
and the byte-identical vendoring of both copies.

Run from the repository root:  python3 -m pytest tests/ -v
"""
import importlib.util
import json
import pathlib
import subprocess
import sys

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
S2_SCRIPT = REPO_ROOT / "skills" / "big-tech-earnings-postmortem" / "scripts" / "note_audit.py"
S3_SCRIPT = REPO_ROOT / "skills" / "bigtech-equity-research" / "scripts" / "note_audit.py"
S2_CHECKS = REPO_ROOT / "skills" / "big-tech-earnings-postmortem" / "assets" / "checks.json"
S3_CHECKS = REPO_ROOT / "skills" / "bigtech-equity-research" / "assets" / "checks.json"


@pytest.fixture(scope="module")
def na():
    """Load the skill-2 copy of note_audit.py as a module (it lives outside any package)."""
    spec = importlib.util.spec_from_file_location("note_audit", S2_SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestVendoring:
    """The two bundled copies are byte-identical by design; drift is a regression
    (the same discipline that guards the postmortem-framework fold-in)."""

    def test_copies_are_byte_identical(self):
        assert S2_SCRIPT.exists() and S3_SCRIPT.exists(), "note_audit.py not vendored"
        assert S2_SCRIPT.read_bytes() == S3_SCRIPT.read_bytes(), (
            "skills 2 and 3 ship divergent copies of note_audit.py — land the change "
            "in one and mirror it in the same commit")

    def test_checks_files_exist_and_parse(self):
        for p in (S2_CHECKS, S3_CHECKS):
            assert p.exists(), f"checks.json missing: {p}"
            data = json.loads(p.read_text(encoding="utf-8"))
            assert isinstance(data.get("required", []), list)


class TestChecksSpecContent:
    """Each skill's needle list enforces the family's non-negotiable disclosures."""

    @pytest.mark.parametrize("checks", [S2_CHECKS, S3_CHECKS], ids=["skill2", "skill3"])
    def test_disclaimer_and_verification_status_required(self, checks):
        data = json.loads(checks.read_text(encoding="utf-8"))
        req = " ".join(str(x).lower() for x in data["required"])
        assert "not investment advice" in req, (
            "compliance disclaimer needle missing from checks.json")
        assert "verification status" in req, (
            "verification-status needle missing (report-4 finding #5)")

    @pytest.mark.parametrize("checks", [S2_CHECKS, S3_CHECKS], ids=["skill2", "skill3"])
    def test_waterfall_label_is_conditional_needle(self, checks):
        data = json.loads(checks.read_text(encoding="utf-8"))
        specs = data.get("required_if", [])
        wf = [s for s in specs if "waterfall" in [str(t).lower() for t in s.get("if_any", [])]]
        assert wf and "not a measured decomposition" in str(wf[0].get("then", "")).lower(), (
            "conditional Reasoned-allocation label needle missing (report-5 M-3)")

    @pytest.mark.parametrize("checks", [S2_CHECKS, S3_CHECKS], ids=["skill2", "skill3"])
    def test_beta_window_is_conditional_needle(self, checks):
        data = json.loads(checks.read_text(encoding="utf-8"))
        specs = data.get("required_if", [])
        beta = [s for s in specs if "beta" in [str(t).lower() for t in s.get("if_any", [])]]
        assert beta and "estimation window" in str(beta[0].get("then", "")).lower(), (
            "conditional beta estimation-window needle missing (report-3 M1)")


class TestPlaceholderScan:
    def test_visible_todo_is_flagged(self, na):
        fails = na.scan_placeholders(
            "n.html", "<html><body><p>TODO fill in</p></body></html>")
        assert any("todo" in f for f in fails)

    def test_script_block_todo_is_not_flagged(self, na):
        fails = na.scan_placeholders(
            "n.html", "<html><head><script>var todo = 1;</script></head>"
                      "<body><p>Close $282.32</p></body></html>")
        assert fails == []


class TestNeedleChecks:
    """Unit-level behavior of run_needle_checks on synthetic notes."""

    def test_missing_required_disclosure_fails(self, na):
        checks = {"required": ["not investment advice"]}
        fails = na.run_needle_checks(
            "n.html", "<html><body><p>GOOG -12.29%</p></body></html>", checks)
        assert any("MISSING" in f and "not investment advice" in f for f in fails)

    def test_dash_normalization_satisfies_needle(self, na):
        # The needle is written with an em dash; the note prints an en dash —
        # normalization must make them equivalent.
        checks = {"required": ["Reasoned allocation — not a measured decomposition"]}
        html = "<html><body><p>Reasoned allocation – not a measured decomposition</p></body></html>"
        assert na.run_needle_checks("n.html", html, checks) == []

    def test_conditional_disclosure_fires_on_trigger(self, na):
        checks = {"required": [],
                  "required_if": [{"if_any": ["waterfall"], "then": "not a measured decomposition"}]}
        html = "<html><body><p>Waterfall of the move</p></body></html>"
        fails = na.run_needle_checks("n.html", html, checks)
        assert any("conditional disclosure absent" in f for f in fails)

    def test_conditional_disclosure_silent_without_trigger(self, na):
        checks = {"required": [],
                  "required_if": [{"if_any": ["waterfall"], "then": "not a measured decomposition"}]}
        html = "<html><body><p>Ranked driver table only</p></body></html>"
        assert na.run_needle_checks("n.html", html, checks) == []

    def test_malformed_required_if_is_reported(self, na):
        checks = {"required": [], "required_if": [{"if_any": [], "then": ""}]}
        fails = na.run_needle_checks("n.html", "<p>x</p>", checks)
        assert any("CHECKS-BAD" in f for f in fails)


class TestEndToEnd:
    """CLI-level: a clean note passes the skill's own checks.json; a note with a
    placeholder or a missing disclosure exits 1."""

    @pytest.fixture(scope="class")
    def clean_note(self, tmp_path_factory):
        p = tmp_path_factory.mktemp("note") / "research_note.html"
        p.write_text(
            "<html><body><h1>GOOG −12.29%</h1>"
            "<p>Verification status: lite audit gates passed — disclosure needles "
            "+ render audit.</p>"
            "<p>Informational only — not investment advice, not a solicitation. "
            "No price targets published.</p>"
            "<h2>Data-Gap Ledger</h2><p>none open</p>"
            "</body></html>", encoding="utf-8")
        return p

    def test_clean_note_passes_skill3_checks(self, clean_note):
        p = subprocess.run(
            [sys.executable, str(S3_SCRIPT), "--note", str(clean_note),
             "--checks", str(S3_CHECKS)],
            capture_output=True, text=True, cwd=str(REPO_ROOT))
        assert p.returncode == 0, p.stdout + p.stderr
        assert "AUDIT RESULT: CLEAN" in p.stdout

    def test_clean_note_passes_skill2_checks(self, clean_note):
        p = subprocess.run(
            [sys.executable, str(S2_SCRIPT), "--note", str(clean_note),
             "--checks", str(S2_CHECKS)],
            capture_output=True, text=True, cwd=str(REPO_ROOT))
        assert p.returncode == 0, p.stdout + p.stderr

    def test_waterfall_without_label_fails(self, tmp_path):
        p = tmp_path / "n.html"
        p.write_text(
            "<html><body><h2>Driver decomposition</h2>"
            "<p>Signed waterfall: benchmark −1.5, FCF −3.9.</p>"
            "<p>Verification status: lite audit gates passed — disclosure needles "
            "+ render audit.</p>"
            "<p>Informational only — not investment advice.</p>"
            "</body></html>", encoding="utf-8")
        for script, checks in ((S3_SCRIPT, S3_CHECKS), (S2_SCRIPT, S2_CHECKS)):
            r = subprocess.run(
                [sys.executable, str(script), "--note", str(p), "--checks", str(checks)],
                capture_output=True, text=True, cwd=str(REPO_ROOT))
            assert r.returncode == 1, (
                f"{script.parent.parent.name}: quantified waterfall without the "
                "Reasoned-allocation label must fail the gate")
            assert "not a measured decomposition" in r.stdout

    def test_beta_without_window_fails(self, tmp_path):
        p = tmp_path / "n.html"
        p.write_text(
            "<html><body><p>Idiosyncratic move via beta-adjusted excess return "
            "(beta 1.2): −10.49pp.</p>"
            "<p>Verification status: lite audit gates passed — disclosure needles "
            "+ render audit.</p>"
            "<p>Informational only — not investment advice.</p>"
            "</body></html>", encoding="utf-8")
        r = subprocess.run(
            [sys.executable, str(S3_SCRIPT), "--note", str(p), "--checks", str(S3_CHECKS)],
            capture_output=True, text=True, cwd=str(REPO_ROOT))
        assert r.returncode == 1
        assert "estimation window" in r.stdout

    def test_missing_note_file_is_usage_error(self):
        p = subprocess.run(
            [sys.executable, str(S3_SCRIPT), "--note", "/nonexistent/n.html"],
            capture_output=True, text=True, cwd=str(REPO_ROOT))
        assert p.returncode == 2


class TestSelftest:
    def test_module_selftest_returns_zero(self, na):
        assert na.selftest() == 0

    @pytest.mark.parametrize("script", [S2_SCRIPT, S3_SCRIPT],
                             ids=["skill2", "skill3"])
    def test_cli_selftest_exits_zero(self, script):
        p = subprocess.run(
            [sys.executable, str(script), "--selftest"],
            capture_output=True, text=True, cwd=str(REPO_ROOT))
        assert p.returncode == 0, p.stdout + p.stderr
        assert "SELFTEST: PASS" in p.stdout


class TestSkillWiring:
    """Both lite skills' SKILL.md must mandate the bundled gates (the R5-H-1
    fix is 'mandatory last step', not 'if installed')."""

    @pytest.mark.parametrize("skill", [
        "skills/big-tech-earnings-postmortem/SKILL.md",
        "skills/bigtech-equity-research/SKILL.md",
    ], ids=["skill2", "skill3"])
    def test_skill_md_mandates_note_audit(self, skill):
        t = (REPO_ROOT / skill).read_text(encoding="utf-8")
        assert "note_audit.py" in t, f"{skill}: bundled lite audit not wired"
        assert "note_overflow_audit.mjs" in t, f"{skill}: render gate not wired"

    def test_skill2_no_longer_claims_no_tooling(self):
        t = (REPO_ROOT / "skills" / "big-tech-earnings-postmortem" / "SKILL.md").read_text(
            encoding="utf-8")
        assert "ships no executable tooling" not in t, (
            "skill 2 still claims it ships no executable tooling — the lite gates "
            "are bundled now (report-5 H-1 fix)")
