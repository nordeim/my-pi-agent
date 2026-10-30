#!/usr/bin/env python3
"""Regression guard for fact_base_audit.py — evidence harness for the skill audit.

Originally demonstrated audit finding H-4: the numeric audit's unanchored
substring token matching reported PASS (exit CLEAN) for numbers that were
genuinely absent, whenever the fact's digit string was contained inside a
different number printed on the slide (82.3 vs "$282.32"; 12.29 vs
"-112.29%").

Since the H-4 fix (boundary-anchored token matching), this harness ASSERTS the
hole stays closed: both evasion cases must now exit 1 with MISSING, and the two
controls must behave (present -> exit 0, absent -> exit 1). Exits 0 only when
every expectation holds, so it is wired into the repository regression suite
(tests/test_fact_base_audit.py) and CI.

Runs the repo script as a subprocess against scratch decks. Read-only with
respect to the repo.
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
        return p.returncode, p.stdout


# (label, slide, facts, expected_exit, expected_stdout_fragment)
CASES = [
    ("fact=82.3 vs slide '$282.32' (digit substring) — must be MISSING",
     "<html><body><p>Close: $282.32</p></body></html>",
     [{"id": "F-1", "value": 82.3, "unit": "$",
       "slide_pages": ["slide_01.html"]}],
     1, "MISSING"),
    ("fact=12.29 vs slide '-112.29%' (digit substring) — must be MISSING",
     "<html><body><p>Move: -112.29%</p></body></html>",
     [{"id": "F-2", "value": 12.29, "unit": "%",
       "slide_pages": ["slide_01.html"]}],
     1, "MISSING"),
    ("CONTROL fact=282.32 vs slide '$282.32' — must PASS",
     "<html><body><p>Close: $282.32</p></body></html>",
     [{"id": "F-3", "value": 282.32, "unit": "$",
       "slide_pages": ["slide_01.html"]}],
     0, "PASS"),
    ("CONTROL fact=63.4 vs slide '$282.32' — must be MISSING",
     "<html><body><p>Close: $282.32</p></body></html>",
     [{"id": "F-4", "value": 63.4, "unit": "$B",
       "slide_pages": ["slide_01.html"]}],
     1, "MISSING"),
]


def main():
    failures = []
    for name, slide, facts, want_exit, want_frag in CASES:
        got_exit, stdout = run_case(name, slide, facts)
        ok = got_exit == want_exit and want_frag in stdout
        if not ok:
            failures.append(
                f"{name}: expected exit {want_exit} with {want_frag!r}, "
                f"got exit {got_exit}")
        print("    expectation:", "OK" if ok else "VIOLATED")
    print("=" * 60)
    if failures:
        print(f"H-4 regression guard: FAIL ({len(failures)} violation(s))")
        for f in failures:
            print("  -", f)
        return 1
    print("H-4 regression guard: PASS "
          "(substring evasion cases exit 1; controls behave)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
