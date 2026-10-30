#!/usr/bin/env python3
"""Negative tests for fact_base_audit.py — evidence harness for the skill audit.

Demonstrates that the numeric audit's unanchored substring token matching can
report PASS (and exit CLEAN) for numbers that are genuinely absent, whenever the
fact's digit string is contained inside a different number printed on the slide.

Runs the repo script as a subprocess against scratch decks; prints observed
verdicts and exit codes. Read-only with respect to the repo.
"""
import json
import pathlib
import subprocess
import sys
import tempfile


def locate_audit_script():
    """Find the audited script: explicit argv[1], else search repo upwards."""
    if len(sys.argv) > 1:
        return sys.argv[1]
    here = pathlib.Path(__file__).resolve().parent
    for base in [here, *here.parents]:
        cand = base / "skills" / "analyzing-us-bigtech-stocks" / "scripts" / "fact_base_audit.py"
        if cand.exists():
            return str(cand)
    sys.exit("fact_base_audit.py not found; pass its path as argv[1]")


AUDIT = locate_audit_script()


def run_case(name, slide_html, facts):
    with tempfile.TemporaryDirectory() as td:
        d = pathlib.Path(td)
        (d / "slide_01.html").write_text(slide_html, encoding="utf-8")
        (d / "fb.json").write_text(json.dumps({"facts": facts}), encoding="utf-8")
        p = subprocess.run(
            [sys.executable, AUDIT, "--slides", str(d),
             "--fact-base", str(d / "fb.json")],
            capture_output=True, text=True)
        lines = [l for l in p.stdout.splitlines()
                 if l.startswith(("PASS", "MISSING", "AUDIT RESULT"))]
        print(f"--- {name} ---")
        for l in lines:
            print("   ", l)
        print("    exit code:", p.returncode)
        return p.returncode


# Case 1: FALSE PASS candidate — fact records close 82.3, slide prints only 282.32.
run_case("fact=82.3 vs slide '$282.32' (digit substring)",
         "<html><body><p>Close: $282.32</p></body></html>",
         [{"id": "F-1", "value": 82.3, "unit": "$",
           "slide_pages": ["slide_01.html"]}])

# Case 2: FALSE PASS candidate — fact move 12.29, slide prints only -112.29%.
run_case("fact=12.29 vs slide '-112.29%' (digit substring)",
         "<html><body><p>Move: -112.29%</p></body></html>",
         [{"id": "F-2", "value": 12.29, "unit": "%",
           "slide_pages": ["slide_01.html"]}])

# Case 3: control — number genuinely present, expect PASS.
run_case("CONTROL fact=282.32 vs slide '$282.32'",
         "<html><body><p>Close: $282.32</p></body></html>",
         [{"id": "F-3", "value": 282.32, "unit": "$",
           "slide_pages": ["slide_01.html"]}])

# Case 4: control — number genuinely absent, expect MISSING + exit 1.
run_case("CONTROL fact=63.4 vs slide '$282.32'",
         "<html><body><p>Close: $282.32</p></body></html>",
         [{"id": "F-4", "value": 63.4, "unit": "$B",
           "slide_pages": ["slide_01.html"]}])
