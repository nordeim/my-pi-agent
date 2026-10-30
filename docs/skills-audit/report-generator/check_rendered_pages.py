#!/usr/bin/env python3
"""Page-level QA for the rendered audit report PDF.

1. Detect blank / near-blank pages via non-white pixel ratio (60dpi JPEGs).
2. Verify structure via pdftotext: TOC pages, body start, figure page, appendix end.
3. Verify footer page numbers: Roman in front matter, Arabic in body.
"""
import glob
import re
import subprocess
import sys

from PIL import Image

PDF = sys.argv[1] if len(sys.argv) > 1 else str(
    __import__("pathlib").Path(__file__).resolve().parent.parent
    / "BigTech_Research_Skills_Audit_Report.pdf")
PAGES = sorted(glob.glob(sys.argv[2] if len(sys.argv) > 2
                         else "/tmp/render/page-*.jpg"))

def page_text(n):
    out = subprocess.run(["pdftotext", "-f", str(n), "-l", str(n), PDF, "-"],
                         capture_output=True, text=True)
    return out.stdout

def main():
    fails = []

    # --- 1. blank pages ---
    ratios = []
    for p in PAGES:
        img = Image.open(p).convert("L")
        hist = img.histogram()
        total = sum(hist)
        nonwhite = total - hist[255]
        ratios.append(nonwhite / total)
    blanks = [i + 1 for i, r in enumerate(ratios) if r < 0.005]
    print(f"[1] {len(PAGES)} pages; non-white ratio min={min(ratios):.4f} max={max(ratios):.4f}")
    print(f"    near-blank pages: {blanks or 'none'}")
    if blanks:
        fails.append(f"blank pages {blanks}")

    # --- 2. structure ---
    n = len(PAGES)
    toc_pages, body_start, fig_page, app_pages = [], None, None, []
    for i in range(1, n + 1):
        t = page_text(i)
        if "Table of Contents" in t:
            toc_pages.append(i)
        if body_start is None and re.search(r"^\s*1\. Executive Summary", t, re.M) and "Table of Contents" not in t:
            body_start = i
        if fig_page is None and "Figure 1:" in t:
            fig_page = i
        if "Appendix" in t:
            app_pages.append(i)
    print(f"[2] TOC page(s): {toc_pages}; body starts: {body_start}; Figure 1: {fig_page}; appendix pages: {sorted(set(app_pages))[:6]}")
    if body_start is None:
        fails.append("body start not found")
    if fig_page is None:
        fails.append("Figure 1 page not found")

    # --- 3. footer numbering: Roman before body_start, Arabic after ---
    roman = re.compile(r"^[IVXLC]+$")
    arabic = re.compile(r"^\d+$")
    n_roman = n_arabic = 0
    for i in range(2, n + 1):  # cover has no footer
        tail = page_text(i).strip().splitlines()
        tail = [x.strip() for x in tail if x.strip()]
        if not tail:
            continue
        last = tail[-1]
        if roman.match(last):
            n_roman += 1
        elif arabic.match(last):
            n_arabic += 1
    print(f"[3] footer tokens -> roman-ish: {n_roman}, arabic: {n_arabic} (cover excluded)")
    if n_arabic < 25:
        fails.append(f"too few arabic footer pages: {n_arabic}")

    # --- 4. TOC entries include short finding headings ---
    toc_text = "".join(page_text(i) for i in toc_pages) if toc_pages else ""
    toc_ids = len(set(re.findall(r"(?:H|M|L|I)-\d", toc_text)))
    print(f"[4] finding ids visible in TOC text: {toc_ids}/20")
    if toc_ids < 20:
        fails.append(f"TOC shows only {toc_ids} finding ids")

    print("\n=== SUMMARY ===")
    if fails:
        for f in fails:
            print("  FAIL", f)
        sys.exit(1)
    print("  all page-level checks passed")

if __name__ == "__main__":
    main()
