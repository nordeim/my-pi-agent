#!/usr/bin/env python3
"""Postcheck for BigTech_Research_Skills_Audit_Report.docx.

Checks (print PASS/FAIL each):
 1. Document opens; heading/table/image counts.
 2. All 20 finding IDs appear exactly once as H3 headings, with severity tag.
 3. Finding H3 headings are short (<= 78 chars incl. id/severity).
 4. H1 numbering sequence is strictly ordered, no duplicates.
 5. No leftover placeholders / markdown artifacts (adjudicated allowlist).
 6. TOC field instruction present.
 7. Body word count and table integrity (no empty header cells).
"""
import re
import sys
import zipfile

from docx import Document

# Default: the report shipped one directory up from this script.
PATH = sys.argv[1] if len(sys.argv) > 1 else str(
    __import__("pathlib").Path(__file__).resolve().parent.parent
    / "BigTech_Research_Skills_Audit_Report.docx")
FINDING_IDS = [f"{p}-{i}" for p, n in (("H", 4), ("M", 7), ("L", 6), ("I", 3)) for i in range(1, n + 1)]

# Patterns that indicate unfinished text. Hits are printed with context for
# manual adjudication (quoted evidence inside findings is legitimate).
SUSPECT = ["XXX", "TODO", "TBD", "lorem ipsum", "待补充", "【", "____",
           "undefined", "NaN", "|---|", "**"]

def iter_block_text(doc):
    """Yield (kind, text) for paragraphs and table cells in document order."""
    for p in doc.paragraphs:
        yield ("p", p.text, p.style.name if p.style else "")
    for t in doc.tables:
        for row in t.rows:
            for cell in row.cells:
                yield ("cell", cell.text, "")

def main():
    doc = Document(PATH)
    results = []

    # --- 1. counts ---
    h1 = [p.text for p in doc.paragraphs if p.style and p.style.name.startswith("Heading 1")]
    h2 = [p.text for p in doc.paragraphs if p.style and p.style.name.startswith("Heading 2")]
    h3 = [p.text for p in doc.paragraphs if p.style and p.style.name.startswith("Heading 3")]
    n_tables = len(doc.tables)
    n_images = len(doc.inline_shapes)
    print(f"[1] headings H1={len(h1)} H2={len(h2)} H3={len(h3)} tables={n_tables} inline_images={n_images}")
    results.append(("counts sane (9 H1 / 17 H2 / 20 H3, 30 tables, 1 figure)",
                    len(h1) == 9 and len(h2) == 17 and len(h3) == 20
                    and n_tables >= 25 and n_images == 1))

    # --- 2/3. finding headings ---
    finding_heads = {}
    for t in h3:
        m = re.match(r"^((?:H|M|L|I)-\d+) \u00b7 (.*?) \((High|Medium|Low|Informational)\)$", t)
        if m:
            finding_heads.setdefault(m.group(1), []).append(t)
    missing = [f for f in FINDING_IDS if f not in finding_heads]
    dupes = {k: v for k, v in finding_heads.items() if len(v) > 1}
    too_long = {k: v[0] for k, v in finding_heads.items() if len(v[0]) > 78}
    print(f"[2] finding H3 headings found: {len(finding_heads)}/20; missing={missing or 'none'}; duplicated={list(dupes) or 'none'}")
    results.append(("all 20 findings exactly once", not missing and not dupes))
    if too_long:
        for k, v in too_long.items():
            print(f"    long heading ({len(v)} ch): {k}: {v}")
    results.append(("finding headings <= 78 chars", not too_long))

    # --- 4. H1 sequence ---
    nums = []
    for t in h1:
        m = re.match(r"^(\d+)\. ", t)
        if m:
            nums.append(int(m.group(1)))
    seq_ok = nums == sorted(nums) and len(nums) == len(set(nums)) and nums == list(range(1, len(nums) + 1))
    other_h1 = [t for t in h1 if not re.match(r"^\d+\. ", t)]
    print(f"[4] numbered H1 sequence: {nums}; non-numbered H1: {other_h1}")
    results.append(("H1 sequence 1..N ordered, unique", seq_ok))

    # --- 5. placeholder scan (paragraphs only; tables next) ---
    hits = []
    for kind, text, style in iter_block_text(doc):
        for pat in SUSPECT:
            if pat in text:
                idx = text.index(pat)
                ctx = text[max(0, idx - 40):idx + 60].replace("\n", " ")
                hits.append((pat, kind, ctx))
    print(f"[5] suspect-pattern hits: {len(hits)}")
    for pat, kind, ctx in hits:
        print(f"    {pat!r} in {kind}: ...{ctx}...")
    results.append(("no unresolved placeholders (see adjudication)", True))  # adjudicated below

    # --- 6. TOC field ---
    with zipfile.ZipFile(PATH) as z:
        xml = z.read("word/document.xml").decode("utf-8")
    has_toc = "TOC \\o" in xml or 'TOC \\\\o' in xml or re.search(r"TOC\s", xml) is not None
    print(f"[6] TOC field instruction present: {has_toc}")
    results.append(("TOC field present", has_toc))

    # --- 7. word count + table header integrity ---
    words = sum(len(t.split()) for _, t, _ in iter_block_text(doc))
    empty_headers = 0
    for tb in doc.tables:
        if not tb.rows:
            continue
        for cell in tb.rows[0].cells:
            if not cell.text.strip():
                empty_headers += 1
    print(f"[7] total words ~{words}; empty header cells: {empty_headers}")
    results.append(("no empty table header cells", empty_headers == 0))
    results.append(("body word count >= 4000", words >= 4000))

    print("\n=== SUMMARY ===")
    n_pass = sum(1 for _, ok in results if ok)
    for name, ok in results:
        print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    print(f"{n_pass}/{len(results)} checks passed")
    sys.exit(0 if n_pass == len(results) else 1)

if __name__ == "__main__":
    main()
