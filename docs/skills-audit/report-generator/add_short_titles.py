#!/usr/bin/env python3
"""Insert a concise `short` title into each finding object in report_content_1.js
so the H3 heading (and thus the TOC entry) stays on one line. The full title is
preserved and rendered in the finding table caption by generate_audit_report.js.
Idempotent: skips findings that already have a short field.
"""
import re
import sys

PATH = sys.argv[1] if len(sys.argv) > 1 else str(
    __import__("pathlib").Path(__file__).resolve().parent
    / "report_content_1.js")

SHORTS = {
    "H-1": "Cross-skill figure conflicts on the same event",
    "H-2": "No disclaimer anywhere in skill 2",
    "H-3": "Segment map wrong for 3 of 7 companies",
    "H-4": "Numeric audit gate can silently pass",
    "M-1": "Render audit measures viewport, not slide origin",
    "M-2": "Three inconsistent attribution doctrines",
    "M-3": "Confidence taxonomy drift across skills",
    "M-4": "Self-test prints without asserting; sign error",
    "M-5": "Skill 2 quality bar is unenforced prose",
    "M-6": "Routing overlap; catalog indexes none",
    "M-7": "Implicit, environment-coupled Playwright dependency",
    "L-1": "Packaging and frontmatter drift",
    "L-2": "No root LICENSE",
    "L-3": "Markdown defect; circular market-cap pair",
    "L-4": "Placeholder scan reads script and style blocks",
    "L-5": "Evidence ledger cites a nonexistent phase",
    "L-6": "Embedded sell-side specifics unverifiable",
    "I-1": "No MNPI / Reg FD statement",
    "I-2": "No explicit GAAP-to-non-GAAP phase",
    "I-3": "Consensus-vendor attribution varies",
}

def main():
    with open(PATH, "r", encoding="utf-8") as f:
        src = f.read()

    inserted, skipped = [], []
    for fid, short in SHORTS.items():
        # Already has a short field directly after this finding's title?
        pat = re.compile(r'(id: "' + re.escape(fid) + r'", title: "[^"]*")(, short: )')
        if pat.search(src):
            skipped.append(fid)
            continue
        pat = re.compile(r'(id: "' + re.escape(fid) + r'", title: "[^"]*")')
        src, n = pat.subn(r'\1, short: "' + short + '"', src, count=1)
        if n != 1:
            print(f"ERROR: finding {fid} not matched (n={n})")
            sys.exit(1)
        inserted.append(fid)

    with open(PATH, "w", encoding="utf-8") as f:
        f.write(src)

    print(f"inserted short for {len(inserted)} findings: {', '.join(inserted)}")
    if skipped:
        print(f"already present (skipped): {', '.join(skipped)}")

if __name__ == "__main__":
    main()
