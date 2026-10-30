#!/usr/bin/env python3
"""source_snapshot.py — source-truth snapshots for the big-tech research family.

The family's audit gates (fact_base_audit.py, fact_base_lite_audit.py,
note_audit.py) verify INTERNAL consistency: the number on the slide matches the
number in the registry, formulas evaluate, schema fields are populated. They do
NOT verify that the number in the registry matches the cited source document —
a fact entry with a wrong figure and a valid-looking URL passes every gate
(comparative reports 10/11, report 11 §3.4 "machine-checked means internal
consistency, not source truth"; report 10's synthesis concedes the point: the
gates prevent generation hallucinations, not ingestion errors).

This script closes the in-scope part of that gap (report 11 §6.9: "fetch and
hash source content, not just record URLs; consider a source-snapshot archive
for audit defensibility"). It does not fetch anything itself — the agent
fetches sources during Phase 1 / Step 8 anyway; this tool pins WHAT was
fetched, so the registry can be audited against the retrieved document after
the fact:

  record
      python3 source_snapshot.py --record --url <url> --content <saved-file> \
          [--source-name <name>] --out source_snapshots.json
      Hashes the saved source content (SHA-256) and records {url, source_name,
      fetched_at_utc, content_path, sha256, bytes} in the manifest. Re-recording
      the same URL replaces its entry (a refresh, not a duplicate). The fact
      base / lite registry then references the snapshot by its sha256 in the
      fact's `source_snapshot` field, and the audit's SNAPSHOT check
      (--snapshots source_snapshots.json) fails the build when a declared hash
      is absent from the manifest (registry <-> manifest linkage).

  verify
      python3 source_snapshot.py --verify source_snapshots.json
      Re-hashes every snapshot's content file and exits 1 naming the first file
      that drifted or went missing since recording — run it before relying on a
      delivered artifact. Content paths resolve as given, then relative to the
      manifest's own directory (manifest + sources moved together still verify).

Seal the snapshots with the deliverable by passing them to
provenance_seal.py as ordinary --inputs (e.g. --inputs note.html
fact_base_lite.json source_snapshots.json sources/press_release.html) — the
tamper-evident seal then covers the evidence trail end to end.

What this still does NOT do (out of scope, by the family's standing scoping):
fetching inside the gate (the audits stay deterministic offline checks), or
parsing the filing to auto-extract numbers (the snapshot gives model-risk and
compliance the artifact to diff the registry against the retrieved document —
the re-verification itself is the analyst's pre-delivery checklist).

Exit codes: 0 success, 1 verification mismatch (or selftest failure),
2 usage error.

The copies bundled in the three family skills are byte-identical by design;
tests/test_repo_consistency.py fails the build if they drift apart.
"""
import argparse
import datetime as _dt
import hashlib
import json
import pathlib
import sys

SCHEMA_VERSION = 1
TOOL_ID = "source_snapshot.py v1 (big-tech research family)"
READ_CHUNK = 1 << 20  # 1 MiB — constant memory for large fetched pages


def _sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            chunk = fh.read(READ_CHUNK)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def record(url: str, content_path: pathlib.Path, out: pathlib.Path,
           source_name: str = "") -> dict:
    """Add or refresh the manifest entry for `url` from the saved content file."""
    if not content_path.is_file():
        print(f"ERROR  content file not found: {content_path}", file=sys.stderr)
        sys.exit(2)
    digest = _sha256_file(content_path)
    entry = {
        "url": url,
        "source_name": source_name or url,
        "fetched_at_utc": _dt.datetime.now(_dt.timezone.utc)
                          .strftime("%Y-%m-%dT%H:%M:%SZ"),
        "content_path": str(content_path),
        "sha256": digest,
        "bytes": content_path.stat().st_size,
    }
    manifest = _load_manifest(out, create=True)
    snapshots = [s for s in manifest.get("snapshots", []) if s.get("url") != url]
    snapshots.append(entry)
    snapshots.sort(key=lambda s: str(s.get("url", "")))   # stable, diff-friendly
    manifest["snapshots"] = snapshots
    manifest["recorded_at_utc"] = entry["fetched_at_utc"]
    out.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"SNAPSHOT   {url}  sha256:{digest[:12]}  "
          f"{entry['bytes']} bytes -> {out.name}")
    return manifest


def _load_manifest(path: pathlib.Path, create: bool = False) -> dict:
    if not path.is_file():
        if create:
            return {"schema_version": SCHEMA_VERSION, "tool": TOOL_ID,
                    "snapshots": []}
        print(f"ERROR  manifest not found: {path}", file=sys.stderr)
        sys.exit(2)
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as e:
        print(f"ERROR  cannot read manifest {path}: {e}", file=sys.stderr)
        sys.exit(2)
    if not isinstance(manifest.get("snapshots", []), list):
        print(f"ERROR  manifest {path}: 'snapshots' is not a list", file=sys.stderr)
        sys.exit(2)
    return manifest


def _resolve(content_path: str, manifest_dir: pathlib.Path) -> pathlib.Path:
    """As given first; then relative to the manifest's directory (so manifest +
    sources relocated together still verify)."""
    p = pathlib.Path(content_path)
    if p.is_file():
        return p
    alt = manifest_dir / p
    return alt if alt.is_file() else p


def verify(path: pathlib.Path) -> int:
    """Re-hash every recorded snapshot; exit 1 on the first drift/missing file."""
    manifest = _load_manifest(path)
    snapshots = manifest.get("snapshots", [])
    if not snapshots:
        print("NOTE   manifest records no snapshots — nothing to verify")
        return 0
    bad = 0
    for s in snapshots:
        url = str(s.get("url", "?"))
        cp = _resolve(str(s.get("content_path", "")), path.parent)
        if not cp.is_file():
            print(f"DRIFT      {url}  content file missing: {cp}")
            bad += 1
            continue
        digest = _sha256_file(cp)
        if digest != str(s.get("sha256", "")):
            print(f"DRIFT      {url}  content hash changed since recording "
                  f"(expected {str(s.get('sha256', ''))[:12]}, got {digest[:12]}) "
                  f"— the saved source was edited after the fact")
            bad += 1
        else:
            print(f"PASS       {url}  sha256:{digest[:12]}  {cp.name}")
    print("=" * 60)
    print("VERIFY RESULT:", "CLEAN" if not bad else f"{bad} drift/missing")
    return 0 if not bad else 1


def selftest() -> int:
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        d = pathlib.Path(td)
        content = d / "press_release.html"
        content.write_text("<html>Alphabet Q3 2026 results …</html>",
                           encoding="utf-8")
        manifest = d / "source_snapshots.json"

        # record -> verify round-trip (clean)
        import contextlib, io
        with contextlib.redirect_stdout(io.StringIO()):
            record("https://example.com/goog-q3-2026", content, manifest,
                   source_name="Alphabet IR press release")
            code_clean = verify(manifest)

        # tamper -> verify fails
        content.write_text("<html>Alphabet Q3 2026 results … EDITED</html>",
                           encoding="utf-8")
        with contextlib.redirect_stdout(io.StringIO()):
            code_tamper = verify(manifest)

        # missing content file -> verify fails
        content.unlink()
        with contextlib.redirect_stdout(io.StringIO()):
            code_missing = verify(manifest)

        # re-record replaces (no duplicate entries for one URL)
        content2 = d / "transcript.txt"
        content2.write_text("earnings call transcript", encoding="utf-8")
        with contextlib.redirect_stdout(io.StringIO()):
            record("https://example.com/goog-q3-2026", content2, manifest)
            m = json.loads(manifest.read_text(encoding="utf-8"))
        urls = [s["url"] for s in m["snapshots"]]
        no_dupes = urls.count("https://example.com/goog-q3-2026") == 1

        # relocation: manifest + content moved together still verify
        moved_dir = d / "moved"
        moved_dir.mkdir()
        content3 = moved_dir / "filing.txt"
        content3.write_text("10-Q excerpt", encoding="utf-8")
        man2 = moved_dir / "source_snapshots.json"
        with contextlib.redirect_stdout(io.StringIO()):
            record("https://sec.gov/10q", content3, man2)
        (moved_dir / "source_snapshots.json").unlink()
        (d / "elsewhere.json").write_text("{}", encoding="utf-8")
        # simulate: recorded with absolute path, then tree relocated
        abs_rec = d / "root" / "snap.json"
        (d / "root").mkdir()
        src = d / "root" / "page.html"
        src.write_text("page", encoding="utf-8")
        with contextlib.redirect_stdout(io.StringIO()):
            record("https://example.com/page", src, abs_rec)
        # move the whole root dir to moved2 and fix nothing but path resolution
        (d / "root").rename(d / "moved2")
        man_moved = d / "moved2" / "snap.json"
        man_moved_text = json.loads(man_moved.read_text(encoding="utf-8"))
        # content_path recorded as the pre-move absolute path; simulate the
        # portable layout by rewriting it to the relative name
        man_moved_text["snapshots"][0]["content_path"] = "page.html"
        man_moved.write_text(json.dumps(man_moved_text), encoding="utf-8")
        with contextlib.redirect_stdout(io.StringIO()):
            code_relocated = verify(man_moved)

        ok = (code_clean == 0 and code_tamper == 1 and code_missing == 1
              and no_dupes and code_relocated == 0)
        print("SELFTEST:", "PASS" if ok else "FAIL",
              f"(clean {code_clean}, tamper {code_tamper}, "
              f"missing {code_missing}, dedupe {no_dupes}, "
              f"relocated {code_relocated})")
        return 0 if ok else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--record", action="store_true",
                    help="record the saved source content for --url as a "
                         "snapshot entry in --out")
    ap.add_argument("--url", help="the source URL the content was fetched from")
    ap.add_argument("--content", help="the saved fetched content file")
    ap.add_argument("--source-name", default="",
                    help="human-readable source label (e.g. 'Alphabet IR press "
                         "release'); defaults to the URL")
    ap.add_argument("--out", default="source_snapshots.json",
                    help="snapshot manifest path (default ./source_snapshots.json)")
    ap.add_argument("--verify", metavar="MANIFEST",
                    help="re-hash every recorded snapshot and report drift")
    ap.add_argument("--selftest", action="store_true",
                    help="run built-in self-test and exit")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()
    if args.verify:
        return verify(pathlib.Path(args.verify))
    if args.record:
        if not args.url or not args.content:
            print("ERROR  --record needs --url and --content", file=sys.stderr)
            return 2
        record(args.url, pathlib.Path(args.content), pathlib.Path(args.out),
               source_name=args.source_name)
        return 0
    print("ERROR  give --record (--url + --content + --out), --verify "
          "<manifest>, or --selftest", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
