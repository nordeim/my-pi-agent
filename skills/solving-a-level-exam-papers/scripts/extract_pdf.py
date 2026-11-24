#!/usr/bin/env python3
"""Fail-closed, non-destructive PDF ingestion with scoped fidelity candidates.

Exit: 0 OK | 2 configuration/IO error | 3 one or more pages have NO TEXT.
"""
from __future__ import annotations
import argparse, hashlib, json, os, re, sys, tempfile
from pathlib import Path

NO_TEXT_MIN_CHARS = 20
MAX_FLAGS_PER_PAGE = 12
STDOUT_LINE_CAP = 40

MATHS_CONTEXT = re.compile(r"(?:\d\s*i\b|\bi\s*\d|[=<>]|\barg\b|\b[zwxy]\b|\*)")
RULES = [
    ("modulus-candidate", re.compile(r"\d\s*i\b"), lambda s: "|" not in s),
    ("conjugate-marker", re.compile(r"\\\*|(?<=\w)\*"), None),
    ("fraction-modulus-candidate", re.compile(r"(?<![\w.])1(?![\w.])"),
     lambda s: "*" in s and "/" not in s),
    ("inequality-candidate", re.compile(r"\barg\b"), lambda s: not re.search(r"[<>≤≥]", s)),
    ("matrix-candidate", re.compile(r"(?:-?\d+\s+){5,}-?\d+"),
     lambda s: not re.search(r"[\[\]()]", s)),
]


def atomic_write(path: Path, text: str, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"refusing to overwrite {path} (use --force)")
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=path.parent, delete=False,
                                     encoding="utf-8") as fh:
        fh.write(text)
        tmp = fh.name
    os.replace(tmp, path)


def page_flags(text: str) -> list[dict]:
    out, seen = [], set()
    for ln, line in enumerate(text.splitlines(), 1):
        if not MATHS_CONTEXT.search(line):
            continue
        for name, rx, guard in RULES:
            if rx.search(line) and (guard is None or guard(line)):
                key = (name, line.strip())
                if key in seen:
                    continue
                seen.add(key)
                out.append({"line": ln, "kind": name, "tier": "candidate",
                            "text": line.strip()[:120]})
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--out")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--pages", help="e.g. 4,16-18 (1-based)")
    ap.add_argument("--render", action="store_true", help="write PNGs for NO_TEXT pages")
    a = ap.parse_args()

    src = Path(a.pdf)
    if not src.is_file():
        print(f"CONFIG ERROR: no such file: {src}", file=sys.stderr)
        return 2
    try:
        import pdfplumber
    except ImportError:
        print("CONFIG ERROR: uv run --with pdfplumber python scripts/extract_pdf.py ...",
              file=sys.stderr)
        return 2

    digest = hashlib.sha256(src.read_bytes()).hexdigest()
    out = Path(a.out) if a.out else Path("out") / f"{src.stem}-{digest[:8]}"
    wanted = None
    if a.pages:
        wanted = set()
        for chunk in a.pages.split(","):
            lo, _, hi = chunk.partition("-")
            wanted.update(range(int(lo), int(hi or lo) + 1))

    pages, corpus = [], []
    with pdfplumber.open(str(src)) as doc:
        for i, page in enumerate(doc.pages, 1):
            if wanted and i not in wanted:
                continue
            text = page.extract_text() or ""
            n = len(re.sub(r"\s", "", text))
            status = "OK" if n >= NO_TEXT_MIN_CHARS else "NO_TEXT"
            flags = page_flags(text)
            pages.append({"page": i, "chars": n, "status": status,
                          "solutions_detected": bool(re.search(r"\bSolutions?\b|AO[123]", text)),
                          "flags": flags[:MAX_FLAGS_PER_PAGE],
                          "flags_suppressed": max(0, len(flags) - MAX_FLAGS_PER_PAGE)})
            corpus.append(f"\n===== PDF PAGE {i} [{status}] =====\n{text}")
            if a.render and status == "NO_TEXT":
                try:
                    out.mkdir(parents=True, exist_ok=True)
                    page.to_image(resolution=200).save(out / f"page-{i}.png")
                except Exception as exc:  # noqa: BLE001
                    print(f"render unavailable for page {i}: {exc}", file=sys.stderr)

    no_text = [p["page"] for p in pages if p["status"] == "NO_TEXT"]
    manifest = {"pdf": str(src), "sha256": digest, "pdfplumber": pdfplumber.__version__,
                "pages_ingested": len(pages), "no_text_pages": no_text,
                "gate_G0": "FAIL" if no_text or not pages else "PASS", "pages": pages}
    try:
        atomic_write(out / "pages.txt", "".join(corpus), a.force)
        atomic_write(out / "manifest.json", json.dumps(manifest, indent=2), a.force)
    except FileExistsError as exc:
        print(f"CONFIG ERROR: {exc}", file=sys.stderr)
        return 2

    lines = [f"{src.name}  sha256={digest[:16]}…  pages={len(pages)}"]
    for p in pages:
        head = f"page {p['page']}: {p['status']} ({p['chars']} chars)"
        if p["solutions_detected"]:
            head += "  [SOLUTIONS/MARK TAGS]"
        lines.append(head)
        lines += [f"    L{f['line']} {f['kind']}: {f['text']}" for f in p["flags"]]
        if p["flags_suppressed"]:
            lines.append(f"    (+{p['flags_suppressed']} further candidates in manifest.json)")
    shown = lines[:STDOUT_LINE_CAP]
    print("\n".join(shown))
    if len(lines) > STDOUT_LINE_CAP:
        print(f"\n[OUTPUT TRUNCATED: {len(lines) - STDOUT_LINE_CAP} further lines — "
              f"full detail in {out/'manifest.json'}]")
    print(f"\nWrote {out/'pages.txt'} and {out/'manifest.json'}")
    if no_text or not pages:
        print(f"\nG0 FAILED: pages with no text layer: {no_text or 'ALL'}. "
              "Re-run with --render and read the images, or OCR, before solving. "
              "Do not proceed on an empty corpus.", file=sys.stderr)
        return 3
    print("Candidates are heuristics, not confirmed defects: confirm each against "
          "the bound solutions (G1).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
