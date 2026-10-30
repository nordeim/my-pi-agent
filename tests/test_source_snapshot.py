"""Regression tests for the source-snapshot gate vendored into all three
big-tech research skills:

  skills/analyzing-us-bigtech-stocks/scripts/source_snapshot.py
  skills/big-tech-earnings-postmortem/scripts/source_snapshot.py
  skills/bigtech-equity-research/scripts/source_snapshot.py

Guards the round-5 fix for comparative reports 10/11 §3.4/§6.9 ("machine-checked
means internal consistency, not source truth" / "fetch and hash source content,
not just record URLs"): the audit gates verify the deliverable matches the
registry, but nothing verified the registry against the fetched sources — a
fact entry with a wrong figure and a valid-looking URL passed every gate (the
ingestion-error gap). source_snapshot.py pins WHAT was fetched: --record hashes
the saved source content into a manifest the fact base references via the
`source_snapshot` field, --verify re-hashes it (tamper evidence), and the audit
gates' SNAPSHOT check enforces the registry <-> manifest linkage.

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
    REPO_ROOT / "skills" / "analyzing-us-bigtech-stocks" / "scripts" / "source_snapshot.py",
    REPO_ROOT / "skills" / "big-tech-earnings-postmortem" / "scripts" / "source_snapshot.py",
    REPO_ROOT / "skills" / "bigtech-equity-research" / "scripts" / "source_snapshot.py",
]


@pytest.fixture(scope="module")
def ss():
    spec = importlib.util.spec_from_file_location("source_snapshot", SCRIPTS[0])
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestVendoring:
    def test_vendored_into_all_three_skills(self):
        assert all(s.exists() for s in SCRIPTS), (
            "source_snapshot.py must ship with all three family skills "
            "(round 5, reports 10/11 §3.4)")

    def test_copies_are_byte_identical(self):
        bodies = [s.read_bytes() for s in SCRIPTS]
        assert len(set(bodies)) == 1, (
            "the three source_snapshot.py copies drifted apart — land the "
            "change in one copy and re-vendor byte-identically")


class TestRecord:
    def test_record_writes_manifest_entry(self, ss, tmp_path):
        content = tmp_path / "press.html"
        content.write_text("<html>Alphabet Q3 2026 — revenue $127.58B</html>",
                           encoding="utf-8")
        out = tmp_path / "source_snapshots.json"
        manifest = ss.record("https://example.com/press", content, out,
                             source_name="Alphabet IR press release")
        assert manifest["snapshots"][0]["sha256"] == \
            ss._sha256_file(content)
        assert manifest["snapshots"][0]["bytes"] == content.stat().st_size
        assert manifest["snapshots"][0]["url"] == "https://example.com/press"
        assert manifest["snapshots"][0]["source_name"] == "Alphabet IR press release"
        assert out.is_file(), "the manifest must be written to --out"

    def test_re_record_replaces_not_duplicates(self, ss, tmp_path):
        a = tmp_path / "a.html"
        a.write_text("first fetch", encoding="utf-8")
        b = tmp_path / "b.html"
        b.write_text("second fetch (refresh)", encoding="utf-8")
        out = tmp_path / "source_snapshots.json"
        ss.record("https://example.com/x", a, out)
        ss.record("https://example.com/x", b, out)
        manifest = json.loads(out.read_text(encoding="utf-8"))
        urls = [s["url"] for s in manifest["snapshots"]]
        assert urls.count("https://example.com/x") == 1, (
            "re-recording a URL is a refresh, not a duplicate")
        assert manifest["snapshots"][0]["sha256"] == ss._sha256_file(b)

    def test_missing_content_file_is_usage_error(self, ss, tmp_path, capsys):
        out = tmp_path / "source_snapshots.json"
        with pytest.raises(SystemExit) as ei:
            ss.record("https://example.com/x", tmp_path / "nope.html", out)
        assert ei.value.code == 2


class TestVerify:
    def _recorded(self, ss, tmp_path):
        content = tmp_path / "filing.txt"
        content.write_text("10-Q excerpt: segment revenue", encoding="utf-8")
        out = tmp_path / "source_snapshots.json"
        ss.record("https://sec.gov/10q", content, out)
        return content, out

    def test_verify_clean(self, ss, tmp_path):
        content, out = self._recorded(ss, tmp_path)
        assert ss.verify(out) == 0

    def test_verify_detects_tampering(self, ss, tmp_path):
        content, out = self._recorded(ss, tmp_path)
        content.write_text("10-Q excerpt: segment revenue EDITED", encoding="utf-8")
        assert ss.verify(out) == 1, (
            "a snapshot whose saved content changed after recording must fail "
            "--verify (tamper evidence)")

    def test_verify_detects_missing_file(self, ss, tmp_path):
        content, out = self._recorded(ss, tmp_path)
        content.unlink()
        assert ss.verify(out) == 1

    def test_verify_resolves_relative_to_manifest(self, ss, tmp_path):
        """Manifest + content moved together still verify (portable layout)."""
        root = tmp_path / "engagement"
        root.mkdir()
        content = root / "press.html"
        content.write_text("press release body", encoding="utf-8")
        out = root / "source_snapshots.json"
        ss.record("https://example.com/press", content, out)
        # relocate the whole engagement dir and rewrite the path to relative
        moved = tmp_path / "moved"
        root.rename(moved)
        manifest = json.loads((moved / "source_snapshots.json").read_text())
        manifest["snapshots"][0]["content_path"] = "press.html"
        (moved / "source_snapshots.json").write_text(json.dumps(manifest))
        assert ss.verify(moved / "source_snapshots.json") == 0


class TestIntegrationWithProvenanceSeal:
    """Report 11 §6.9: seal the snapshots with the deliverable — the evidence
    trail is covered end to end by the existing provenance seal."""

    def test_snapshots_are_sealable_inputs(self, tmp_path):
        content = tmp_path / "press.html"
        content.write_text("press release body", encoding="utf-8")
        snap = tmp_path / "source_snapshots.json"
        rc = subprocess.run(
            [sys.executable, str(SCRIPTS[0]), "--record",
             "--url", "https://example.com/press",
             "--content", str(content), "--out", str(snap)],
            capture_output=True, text=True, cwd=str(REPO_ROOT))
        assert rc.returncode == 0, rc.stdout + rc.stderr
        seal = REPO_ROOT / "skills" / "analyzing-us-bigtech-stocks" / "scripts" \
            / "provenance_seal.py"
        prov = tmp_path / "provenance.json"
        note = tmp_path / "note.html"
        note.write_text("<html>note</html>", encoding="utf-8")
        rc = subprocess.run(
            [sys.executable, str(seal), "--inputs", str(note), str(snap),
             str(content), "--out", str(prov)],
            capture_output=True, text=True, cwd=str(REPO_ROOT))
        assert rc.returncode == 0, rc.stdout + rc.stderr
        manifest = json.loads(prov.read_text(encoding="utf-8"))
        names = {e["path"] for e in manifest["inputs"]}
        assert {"note.html", "source_snapshots.json", "press.html"} <= names


class TestSelftest:
    @pytest.mark.parametrize("script", SCRIPTS, ids=lambda s: s.parent.parent.name)
    def test_selftest_exits_zero(self, script):
        p = subprocess.run([sys.executable, str(script), "--selftest"],
                           capture_output=True, text=True, cwd=str(REPO_ROOT))
        assert p.returncode == 0, p.stdout + p.stderr
        assert "SELFTEST: PASS" in p.stdout
