#!/usr/bin/env python3
"""Page-marked PDF extraction plus a maths-symbol-loss report.

Usage:
    uv run --with pdfplumber python scripts/extract_pdf.py PAPER.pdf --out out/

Writes out/pages.txt and out/fidelity_report.txt. Deterministic; no network.
"""
from __future__ import annotations
import argparse, pathlib, re, sys

SUSPECT = [
    ("possible lost modulus bars",
     re.compile(r"(?<![\w|])[-+]?\s*\d+\s*i\b"), lambda s: "|" not in s),
    ("conjugate markers present", re.compile(r"\\\*|(?<=\w)\*"), None),
    ("orphan '1' (fraction = 1?)", re.compile(r"(?<![\w.])1(?![\w.])"), None),
    ("possible lost inequality", re.compile(r"\b0\s+\w+\s+π|\bfor\s+0\b"), None),
    ("matrix/vector residue", re.compile(r"(?:\d+\s+){4,}\d+"), None),
]

def extract(pdf: pathlib.Path) -> list[str]:
    try:
        import pdfplumber
    except ImportError:
        sys.exit("pdfplumber missing: uv run --with pdfplumber python ...")
    pages = []
    with pdfplumber.open(str(pdf)) as doc:
        for i, page in enumerate(doc.pages, start=1):
            pages.append(f"\n===== PDF PAGE {i} =====\n" + (page.extract_text() or ""))
    return pages

def report(pages: list[str]) -> str:
    lines = ["MATHS FIDELITY REPORT", "=" * 60,
             "Flags are heuristics: confirm each against the bound solutions.", ""]
    for i, text in enumerate(pages, start=1):
        hits = []
        for ln, line in enumerate(text.splitlines(), start=1):
            for name, rx, guard in SUSPECT:
                if rx.search(line) and (guard is None or guard(line)):
                    hits.append(f"  p{i} L{ln}: {name} :: {line.strip()[:90]}")
        if re.search(r"\bSolutions?\b|AO[123]", text):
            hits.append(f"  p{i}: SOLUTIONS/MARK TAGS DETECTED (ground truth available)")
        if hits:
            lines += [f"Page {i}:"] + hits + [""]
    return "\n".join(lines)

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf"); ap.add_argument("--out", default="out")
    a = ap.parse_args()
    out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
    pages = extract(pathlib.Path(a.pdf))
    (out / "pages.txt").write_text("".join(pages), encoding="utf-8")
    rep = report(pages)
    (out / "fidelity_report.txt").write_text(rep, encoding="utf-8")
    print(rep[:4000])
    print(f"\nWrote {out/'pages.txt'} and {out/'fidelity_report.txt'}")

if __name__ == "__main__":
    main()
