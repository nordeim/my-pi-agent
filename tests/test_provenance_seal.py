"""Regression tests for the provenance sealing gate vendored into all three
big-tech research skills:

  skills/analyzing-us-bigtech-stocks/scripts/provenance_seal.py
  skills/big-tech-earnings-postmortem/scripts/provenance_seal.py
  skills/bigtech-equity-research/scripts/provenance_seal.py

Guards the round-3 fix for comparative reports 6/7 finding C-2 ("immutable
provenance & audit chain void"): the audit gates were point-in-time checks and
the delivered HTML's verification-status line was self-reported and freely
editable. The seal computes SHA-256 hashes of the fact base and the rendered
deliverable, writes a provenance.json sidecar, prints a seal line to embed,
and re-verifies the artifact later with --verify. WORM archival and firm-key
signing remain out of scope by the standing round-2 rejection.

Run from the repository root:  python3 -m pytest tests/ -v
"""
import importlib.util
import json
import pathlib
import subprocess
import sys

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPTS = [
    REPO_ROOT / "skills" / "analyzing-us-bigtech-stocks" / "scripts" / "provenance_seal.py",
    REPO_ROOT / "skills" / "big-tech-earnings-postmortem" / "scripts" / "provenance_seal.py",
    REPO_ROOT / "skills" / "bigtech-equity-research" / "scripts" / "provenance_seal.py",
]


@pytest.fixture(scope="module")
def ps():
    spec = importlib.util.spec_from_file_location("provenance_seal", SCRIPTS[0])
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestVendoring:
    def test_sealed_into_all_three_skills(self):
        assert all(s.exists() for s in SCRIPTS), (
            "provenance_seal.py must ship with all three family skills")

    def test_copies_are_byte_identical(self):
        bodies = [s.read_bytes() for s in SCRIPTS]
        assert len(set(bodies)) == 1, (
            "the three provenance_seal.py copies drifted apart — land the change "
            "in one and mirror it in the same commit")


class TestSealAndVerify:
    def test_seal_writes_manifest_and_seal_line(self, ps, tmp_path):
        fb = tmp_path / "fact_base.json"
        note = tmp_path / "note.html"
        fb.write_text('{"facts": []}', encoding="utf-8")
        note.write_text("<html><body>note</body></html>", encoding="utf-8")
        out = tmp_path / "provenance.json"
        m = ps.seal([fb, note], out)
        assert out.is_file()
        loaded = json.loads(out.read_text(encoding="utf-8"))
        assert loaded["composite_sha256"] == m["composite_sha256"]
        assert len(loaded["inputs"]) == 2
        assert all(len(e["sha256"]) == 64 for e in loaded["inputs"])
        line = ps.seal_line(m)
        assert "sha256:" in line and "2 file(s)" in line

    def test_verify_intact_passes(self, ps, tmp_path):
        fb = tmp_path / "fact_base.json"
        note = tmp_path / "note.html"
        fb.write_text('{"facts": []}', encoding="utf-8")
        note.write_text("<html><body>note</body></html>", encoding="utf-8")
        out = tmp_path / "provenance.json"
        ps.seal([fb, note], out)
        assert ps.verify(out, [fb, note]) == []

    def test_verify_detects_tampering(self, ps, tmp_path):
        fb = tmp_path / "fact_base.json"
        note = tmp_path / "note.html"
        fb.write_text('{"facts": []}', encoding="utf-8")
        note.write_text("<html><body>note v1</body></html>", encoding="utf-8")
        out = tmp_path / "provenance.json"
        ps.seal([fb, note], out)
        note.write_text("<html><body>note v2 — edited after the gates</body></html>",
                        encoding="utf-8")
        problems = ps.verify(out, [fb, note])
        assert any("modified since seal: note.html" in p for p in problems), (
            "editing the deliverable after sealing must be caught — the seal is "
            "the tamper-evident link between the audited inputs and the shipped file")

    def test_verify_detects_missing_file(self, ps, tmp_path):
        fb = tmp_path / "fact_base.json"
        fb.write_text('{"facts": []}', encoding="utf-8")
        out = tmp_path / "provenance.json"
        ps.seal([fb], out)
        fb.unlink()
        assert any("missing since seal" in p for p in ps.verify(out, []))

    def test_composite_is_order_independent(self, ps, tmp_path):
        a, b = tmp_path / "a.json", tmp_path / "b.json"
        a.write_text("{}", encoding="utf-8")
        b.write_text("{}", encoding="utf-8")
        m1 = ps.seal([a, b], tmp_path / "p1.json")
        m2 = ps.seal([b, a], tmp_path / "p2.json")
        assert m1["composite_sha256"] == m2["composite_sha256"]


class TestCLI:
    def test_selftest_exits_zero(self):
        p = subprocess.run(
            [sys.executable, str(SCRIPTS[0]), "--selftest"],
            capture_output=True, text=True, cwd=str(REPO_ROOT))
        assert p.returncode == 0, p.stdout + p.stderr
        assert "SELFTEST: PASS" in p.stdout

    def test_cli_seal_then_verify_roundtrip(self, tmp_path):
        note = tmp_path / "note.html"
        note.write_text("<html><body>delivered</body></html>", encoding="utf-8")
        out = tmp_path / "provenance.json"
        r1 = subprocess.run(
            [sys.executable, str(SCRIPTS[1]), "--inputs", str(note),
             "--out", str(out)],
            capture_output=True, text=True, cwd=str(REPO_ROOT))
        assert r1.returncode == 0, r1.stdout + r1.stderr
        assert "Provenance seal: sha256:" in r1.stdout
        r2 = subprocess.run(
            [sys.executable, str(SCRIPTS[1]), "--verify", str(out),
             "--inputs", str(note)],
            capture_output=True, text=True, cwd=str(REPO_ROOT))
        assert r2.returncode == 0, r2.stdout + r2.stderr
        assert "intact" in r2.stdout

    def test_missing_inputs_is_usage_error(self):
        p = subprocess.run(
            [sys.executable, str(SCRIPTS[0])],
            capture_output=True, text=True, cwd=str(REPO_ROOT))
        assert p.returncode == 2


class TestSelftest:
    def test_module_selftest_returns_zero(self, ps):
        assert ps.selftest() == 0
