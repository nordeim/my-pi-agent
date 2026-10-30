#!/usr/bin/env python3
"""provenance_seal.py — tamper-evident provenance sealing for delivered research artifacts.

The big-tech research family's audit gates (fact_base_audit.py, fact_base_lite_audit.py,
note_audit.py, the render/a11y gates) are point-in-time checks: they pass, the deliverable
ships, and nothing connects the shipped file to the audited inputs afterwards. A
"verification-status line" in the HTML is self-reported and freely editable. This script
closes that gap (comparative reports 6/7, finding C-2 "immutable provenance chain void")
with the control that is in scope for a skill bundle: SHA-256 sealing.

What it does NOT do (deliberately out of scope, per the round-2/3 rejections): WORM
archival, retention scheduling, or cryptographic signing with a firm key — those are
operational infrastructure, not skill doctrine. Sealing is the lightweight, portable
core that makes every other gate defensible.

Modes:
  seal (default)
      python3 provenance_seal.py --inputs fact_base.json note.html [--out provenance.json]
      Hashes every input (SHA-256, size-stamped), computes a composite digest over the
      sorted "name:sha256" lines, writes the sidecar manifest, and prints a seal line
      to embed in the deliverable's footer/cover, e.g.:

        Provenance seal: sha256:9f2a1c4e7b8d — sealed 2026-10-30T12:00:00Z — 2 file(s)

      Embed that line verbatim next to the verification-status line, and ship
      provenance.json alongside the deliverable.

  verify
      python3 provenance_seal.py --verify provenance.json --inputs fact_base.json note.html
      Recomputes every hash and the composite; exits 1 naming the first file that
      changed (or is missing) since sealing. Run it before relying on a delivered
      artifact — a mismatch means the file was edited after the gates passed.

Exit codes: 0 success, 1 verification mismatch (or selftest failure), 2 usage error.

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
TOOL_ID = "provenance_seal.py v1 (big-tech research family)"
READ_CHUNK = 1 << 20  # 1 MiB — constant memory for large decks


def _sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            chunk = fh.read(READ_CHUNK)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def _composite(entries: list) -> str:
    """Digest over the sorted 'name:sha256' lines — order-independent, so the manifest
    is stable across re-seals of the same file set on different machines."""
    lines = sorted(f"{e['path']}:{e['sha256']}" for e in entries)
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()


def seal(inputs: list, out: pathlib.Path) -> dict:
    entries = []
    for p in inputs:
        p = pathlib.Path(p)
        if not p.is_file():
            print(f"ERROR  input not found: {p}", file=sys.stderr)
            sys.exit(2)
        entries.append({"path": p.name, "sha256": _sha256_file(p), "bytes": p.stat().st_size})
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "sealed_at_utc": _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tool": TOOL_ID,
        "inputs": entries,
        "composite_sha256": _composite(entries),
    }
    out.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def verify(manifest_path: pathlib.Path, inputs: list) -> list:
    """Returns a list of mismatch descriptions; empty list means intact."""
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        return [f"manifest unreadable ({e})"]
    problems = []
    recorded = {e["path"]: e["sha256"] for e in manifest.get("inputs", [])}
    present = {pathlib.Path(p).name: _sha256_file(pathlib.Path(p))
               for p in inputs if pathlib.Path(p).is_file()}
    for name, sha in recorded.items():
        if name not in present:
            problems.append(f"missing since seal: {name}")
        elif present[name] != sha:
            problems.append(f"modified since seal: {name}")
    for name in present:
        if name not in recorded:
            problems.append(f"not in manifest: {name}")
    if _composite(manifest.get("inputs", [])) != manifest.get("composite_sha256"):
        problems.append("composite digest does not match the recorded entries")
    return problems


def seal_line(manifest: dict) -> str:
    c = manifest["composite_sha256"][:12]
    return (f"Provenance seal: sha256:{c} — sealed {manifest['sealed_at_utc']} "
            f"— {len(manifest['inputs'])} file(s)")


def selftest() -> int:
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        d = pathlib.Path(td)
        (d / "fact_base.json").write_text('{"facts": []}', encoding="utf-8")
        (d / "note.html").write_text("<html><body>note v1</body></html>", encoding="utf-8")
        manifest_path = d / "provenance.json"
        m = seal([d / "fact_base.json", d / "note.html"], manifest_path)
        ok = manifest_path.is_file() and len(m["inputs"]) == 2 and len(m["composite_sha256"]) == 64
        ok = ok and "sha256:" in seal_line(m) and verify(manifest_path,
                                                         [d / "fact_base.json", d / "note.html"]) == []
        # Tamper: edit the note after sealing -> verify must name it.
        (d / "note.html").write_text("<html><body>note v2 (edited)</body></html>", encoding="utf-8")
        problems = verify(manifest_path, [d / "fact_base.json", d / "note.html"])
        ok = ok and any("modified since seal: note.html" in p for p in problems)
        # Deletion: removing an input must be caught too.
        (d / "fact_base.json").unlink()
        problems = verify(manifest_path, [d / "note.html"])
        ok = ok and any("missing since seal: fact_base.json" in p for p in problems)
        print("=" * 60)
        print("SELFTEST:", "PASS" if ok else "FAIL")
        return 0 if ok else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--inputs", nargs="+", metavar="FILE",
                    help="files to seal/verify: the fact base and the rendered "
                         "deliverable(s)")
    ap.add_argument("--out", default="provenance.json",
                    help="seal mode: where to write the manifest (default ./provenance.json)")
    ap.add_argument("--verify", metavar="MANIFEST",
                    help="verify mode: recompute hashes against this manifest "
                         "(requires --inputs)")
    ap.add_argument("--selftest", action="store_true", help="run built-in self-test and exit")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.inputs:
        print("ERROR  --inputs is required (or --selftest)", file=sys.stderr)
        return 2
    if args.verify:
        problems = verify(pathlib.Path(args.verify), args.inputs)
        if problems:
            print("PROVENANCE: MISMATCH — the artifact does not match its seal:")
            for p in problems:
                print("  -", p)
            return 1
        print("PROVENANCE: intact — every input matches the sealed manifest")
        return 0
    manifest = seal(args.inputs, pathlib.Path(args.out))
    print(f"sealed {len(manifest['inputs'])} file(s) -> {args.out}")
    print("Embed this line next to the verification-status line in the deliverable:")
    print("  " + seal_line(manifest))
    print("Re-check anytime with:")
    print(f"  python3 {pathlib.Path(__file__).name} --verify {args.out} "
          + " ".join(f"'{pathlib.Path(p).name}'" for p in args.inputs))
    return 0


if __name__ == "__main__":
    sys.exit(main())
