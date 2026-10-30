"""Regression tests for skills/big-tech-earnings-postmortem/scripts/fact_base_lite_audit.py.

Guards the round-3 fix for comparative reports 6/7 findings H-4/H-5 (the
"lite-variant verification gap" / credibility spillover): the postmortem skill's
gates checked placeholders, disclosures, and rendering, but nothing
machine-checked that the delivered note's numbers trace to sources — while the
note carried confidence tags and a verification-status line that made it look
indistinguishable from a flagship deliverable. The number-registry gate closes
that: every money/percentage figure printed in the note must be registered in
fact_base_lite.json with a source trail, and every registered number must
actually appear.

Run from the repository root:  python3 -m pytest tests/ -v
"""
import importlib.util
import json
import pathlib
import subprocess
import sys

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = (REPO_ROOT / "skills" / "big-tech-earnings-postmortem" / "scripts" /
          "fact_base_lite_audit.py")
TEMPLATE = (REPO_ROOT / "skills" / "big-tech-earnings-postmortem" / "assets" /
            "fact_base_lite.template.json")


@pytest.fixture(scope="module")
def fla():
    spec = importlib.util.spec_from_file_location("fact_base_lite_audit", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture()
def clean(tmp_path):
    note = tmp_path / "note.html"
    note.write_text(
        "<html><body><h1>GOOG —12.29%</h1>"
        "<p>Close $282.32; revenue $127.58B vs $128.22B consensus.</p>"
        "</body></html>", encoding="utf-8")
    fb = tmp_path / "fact_base_lite.json"
    fb.write_text(json.dumps({"meta": {"furniture": []}, "facts": [
        {"id": "L-1", "metric": "close", "value": 282.32,
         "source_name": "Yahoo Finance", "source_url": "https://x",
         "retrieved_at": "2026-10-30", "confidence": "Verified"},
        {"id": "L-2", "metric": "session move", "value": "-12.29%",
         "source_name": "computed", "source_url": "n/a (derived)",
         "retrieved_at": "2026-10-30", "confidence": "Reasoned (derived)"},
        {"id": "L-3", "metric": "revenue actual", "value": 127.58,
         "source_name": "press release", "source_url": "https://x",
         "retrieved_at": "2026-10-30", "confidence": "Verified"},
        {"id": "L-4", "metric": "revenue consensus", "value": 128.22,
         "source_name": "LSEG via Reuters", "source_url": "https://x",
         "retrieved_at": "2026-10-30", "confidence": "Verified"},
    ]}), encoding="utf-8")
    return note, fb


class TestRegistryGate:
    def test_clean_registry_passes(self, fla, clean):
        note, fb = clean
        rc, lines = fla.main(["--note", str(note), "--fact-base", str(fb)]), None
        assert rc == 0

    def test_unregistered_figure_fails(self, fla, clean):
        note, fb = clean
        note.write_text(note.read_text(encoding="utf-8").replace(
            "</p>", "; erased $482B.</p>"), encoding="utf-8")
        rc = fla.main(["--note", str(note), "--fact-base", str(fb)])
        assert rc == 1

    def test_unregistered_detection_message(self, fla, clean):
        note, fb = clean
        note.write_text("<html><body><p>erased $482B</p></body></html>",
                        encoding="utf-8")
        fails = fla.check_reverse(note.name, note.read_text(encoding="utf-8"),
                                  json.loads(fb.read_text(encoding="utf-8")), set())
        assert any("UNREGISTERED" in f and "482" in f for f in fails), (
            "a note figure with no registry entry must fail the number-registry gate")

    def test_registered_number_absent_from_note_fails(self, fla, clean):
        note, fb = clean
        note.write_text("<html><body><p>Close $282.32 only.</p></body></html>",
                        encoding="utf-8")
        rc = fla.main(["--note", str(note), "--fact-base", str(fb)])
        assert rc == 1

    def test_missing_source_fields_fail_schema(self, fla, tmp_path):
        note = tmp_path / "n.html"
        note.write_text("<html><body><p>$282.32</p></body></html>", encoding="utf-8")
        fb = tmp_path / "fb.json"
        fb.write_text(json.dumps({"meta": {}, "facts": [
            {"id": "L-9", "metric": "close", "value": 282.32}]}), encoding="utf-8")
        rc = fla.main(["--note", str(note), "--fact-base", str(fb)])
        assert rc == 1

    def test_bad_confidence_label_fails(self, fla, tmp_path):
        note = tmp_path / "n.html"
        note.write_text("<html><body><p>$282.32</p></body></html>", encoding="utf-8")
        fb = tmp_path / "fb.json"
        fb.write_text(json.dumps({"meta": {}, "facts": [
            {"id": "L-9", "metric": "close", "value": 282.32,
             "source_name": "x", "source_url": "https://x",
             "retrieved_at": "2026-10-30", "confidence": "Pretty sure"}]}),
            encoding="utf-8")
        fails = fla.check_registry_schema(json.loads(fb.read_text(encoding="utf-8")))
        assert any("SCHEMA" in f and "confidence" in f for f in fails)

    def test_furniture_whitelist_covers_rounded_forms(self, fla, tmp_path):
        note = tmp_path / "n.html"
        note.write_text(
            "<html><body><p>Close $282.32 (−12% headline form).</p></body></html>",
            encoding="utf-8")
        fb = tmp_path / "fb.json"
        fb.write_text(json.dumps({"meta": {"furniture": ["12"]}, "facts": [
            {"id": "L-1", "metric": "close", "value": 282.32,
             "source_name": "Yahoo", "source_url": "https://x",
             "retrieved_at": "2026-10-30", "confidence": "Verified"}]}),
            encoding="utf-8")
        rc = fla.main(["--note", str(note), "--fact-base", str(fb)])
        assert rc == 0

    def test_placeholder_scan_reuses_family_tokens(self, fla):
        fails = fla.scan_placeholders(
            "n.html", "<html><body><p>TODO fill in</p></body></html>")
        assert any("todo" in f for f in fails)

    def test_anchored_matching_not_substring(self, fla):
        # A registry entry of 82.3 must NOT cover a printed $282.32.
        assert fla.token_in("82.3", fla.norm("$282.32")) is False
        assert fla.token_in("282.32", fla.norm("$282.32")) is True


class TestTemplate:
    def test_template_parses_and_documents_fields(self):
        data = json.loads(TEMPLATE.read_text(encoding="utf-8"))
        assert data.get("meta", {}).get("furniture") == []
        assert len(data.get("facts", [])) >= 3
        for fact in data["facts"]:
            for field in ("id", "metric", "value", "source_name", "source_url",
                          "retrieved_at", "confidence"):
                assert field in fact, (
                    f"template fact {fact.get('id')} missing {field}")
        # The consensus example demonstrates the round-3 provider/vintage fields.
        cons = [f for f in data["facts"] if f.get("consensus_provider")]
        assert cons and cons[0].get("consensus_vintage")


class TestCLI:
    def test_selftest_exits_zero(self):
        p = subprocess.run(
            [sys.executable, str(SCRIPT), "--selftest"],
            capture_output=True, text=True, cwd=str(REPO_ROOT))
        assert p.returncode == 0, p.stdout + p.stderr
        assert "SELFTEST: PASS" in p.stdout

    def test_missing_args_is_usage_error(self):
        p = subprocess.run(
            [sys.executable, str(SCRIPT)],
            capture_output=True, text=True, cwd=str(REPO_ROOT))
        assert p.returncode == 2

    def test_end_to_end_clean_and_dirty(self, clean):
        note, fb = clean
        p = subprocess.run(
            [sys.executable, str(SCRIPT), "--note", str(note),
             "--fact-base", str(fb)],
            capture_output=True, text=True, cwd=str(REPO_ROOT))
        assert p.returncode == 0, p.stdout + p.stderr
        assert "AUDIT RESULT: CLEAN" in p.stdout
        note.write_text(
            "<html><body><p>Close $282.32 and an unsourced $482B.</p></body></html>",
            encoding="utf-8")
        p = subprocess.run(
            [sys.executable, str(SCRIPT), "--note", str(note),
             "--fact-base", str(fb)],
            capture_output=True, text=True, cwd=str(REPO_ROOT))
        assert p.returncode == 1
        assert "UNREGISTERED" in p.stdout


class TestSelftest:
    def test_module_selftest_returns_zero(self, fla):
        assert fla.selftest() == 0
