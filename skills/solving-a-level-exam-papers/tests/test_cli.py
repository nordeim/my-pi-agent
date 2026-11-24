import json, re, shutil, subprocess, sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
EXAMPLE = json.loads((ROOT / "assets" / "checks.example.json").read_text())


def run(script, *args):
    return subprocess.run([sys.executable, str(SCRIPTS / script), *map(str, args)],
                          capture_output=True, text=True)


def suite(tmp_path, spec):
    p = tmp_path / "checks.json"
    p.write_text(json.dumps(spec), encoding="utf-8")
    return p


def copy_skill(tmp_path):
    dst = tmp_path / ROOT.name
    shutil.copytree(ROOT, dst,
                    ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache",
                                                 "samples", "docs"))
    return dst


def test_example_suite_passes(tmp_path):
    pytest.importorskip("sympy")
    r = run("check_math.py", suite(tmp_path, EXAMPLE))
    assert r.returncode == 0, r.stdout + r.stderr
    assert "7/7 checks passed." in r.stdout
    assert "checks_sha256=" in r.stdout


def test_empty_suite_exit2(tmp_path):
    pytest.importorskip("sympy")
    r = run("check_math.py", suite(tmp_path, {"checks": []}))
    assert r.returncode == 2 and "non-empty" in r.stderr


def test_single_check_exit2(tmp_path):
    pytest.importorskip("sympy")
    r = run("check_math.py", suite(tmp_path, {"checks": EXAMPLE["checks"][:1]}))
    assert r.returncode == 2


def test_missing_original_role_exit2(tmp_path):
    pytest.importorskip("sympy")
    spec = json.loads(json.dumps(EXAMPLE))
    for c in spec["checks"]:
        c["role"] = "sanity"
    assert run("check_math.py", suite(tmp_path, spec)).returncode == 2


def test_duplicate_ids_exit2(tmp_path):
    pytest.importorskip("sympy")
    spec = json.loads(json.dumps(EXAMPLE))
    spec["checks"][1]["id"] = spec["checks"][0]["id"]
    assert run("check_math.py", suite(tmp_path, spec)).returncode == 2


def test_tol_abuse_exit2(tmp_path):
    pytest.importorskip("sympy")
    spec = json.loads(json.dumps(EXAMPLE))
    spec["checks"][0].update(kind="approx", tol=1e9)
    assert run("check_math.py", suite(tmp_path, spec)).returncode == 2


def test_float_in_exact_check_exit2(tmp_path):
    pytest.importorskip("sympy")
    spec = json.loads(json.dumps(EXAMPLE))
    spec["checks"][1]["lhs"] = "5.04 + 12.96"
    assert run("check_math.py", suite(tmp_path, spec)).returncode == 2


def test_false_claim_fails_exit1(tmp_path):
    pytest.importorskip("sympy")
    spec = json.loads(json.dumps(EXAMPLE))
    spec["checks"][1]["rhs"] = "19"
    r = run("check_math.py", suite(tmp_path, spec))
    assert r.returncode == 1 and "FAIL" in r.stdout


def test_injection_exit2_and_no_marker(tmp_path):
    pytest.importorskip("sympy")
    marker = tmp_path / "pwned"
    spec = json.loads(json.dumps(EXAMPLE))
    spec["checks"][0]["expr"] = f"__import__('pathlib').Path(r'{marker}').write_text('x')"
    spec["checks"][0]["kind"] = "zero"
    r = run("check_math.py", suite(tmp_path, spec))
    assert r.returncode == 2 and not marker.exists()


def blank_pdf(path, pages=1):
    kids = " ".join(f"{3 + 2 * i} 0 R" for i in range(pages))
    objs = [b"<</Type/Catalog/Pages 2 0 R>>",
            f"<</Type/Pages/Kids[{kids}]/Count {pages}>>".encode()]
    for i in range(pages):
        objs.append(f"<</Type/Page/Parent 2 0 R/MediaBox[0 0 200 200]/Resources<<>>/Contents {4 + 2 * i} 0 R>>".encode())
        objs.append(b"<</Length 0>>stream\nendstream\n")
    out, offsets = bytearray(b"%PDF-1.4\n"), []
    for i, body in enumerate(objs, 1):
        offsets.append(len(out))
        out += f"{i} 0 obj".encode() + body + b"endobj\n"
    xref = len(out)
    out += f"xref\n0 {len(objs)+1}\n".encode() + b"0000000000 65535 f \n"
    for off in offsets:
        out += f"{off:010d} 00000 n \n".encode()
    out += f"trailer<</Size {len(objs)+1}/Root 1 0 R>>\nstartxref\n{xref}\n%%EOF\n".encode()
    path.write_bytes(bytes(out))


def test_textless_pdf_exit3(tmp_path):
    pytest.importorskip("pdfplumber")
    pdf = tmp_path / "blank.pdf"
    blank_pdf(pdf)
    r = run("extract_pdf.py", pdf, "--out", tmp_path / "o")
    assert r.returncode == 3 and "NO_TEXT" in r.stdout and "G0 FAILED" in r.stderr


def test_force_overwrites(tmp_path):
    pytest.importorskip("pdfplumber")
    pdf = tmp_path / "blank.pdf"
    blank_pdf(pdf)
    out = tmp_path / "o"
    run("extract_pdf.py", pdf, "--out", out)
    sentinel = out / "pages.txt"
    sentinel.write_text("SENTINEL", encoding="utf-8")
    r = run("extract_pdf.py", pdf, "--out", out)
    assert r.returncode == 2 and sentinel.read_text() == "SENTINEL"
    r = run("extract_pdf.py", pdf, "--out", out, "--force")
    assert r.returncode == 3 and sentinel.read_text() != "SENTINEL"


def test_lint_passes_package():
    r = run("lint_skill.py", ROOT)
    assert r.returncode == 0, r.stdout + r.stderr


def test_provenance_present(tmp_path):
    pytest.importorskip("sympy")
    r = run("check_math.py", suite(tmp_path, EXAMPLE))
    assert r.returncode == 0, r.stdout + r.stderr
    assert "checks_sha256=" in r.stdout and "sympy=" in r.stdout


def test_interval_complex_errors(tmp_path):
    pytest.importorskip("sympy")
    spec = {"symbols": ["x"], "checks": [
        {"id": "O", "role": "original-condition", "kind": "equal",
         "note": "1 = 1", "lhs": "1", "rhs": "1"},
        {"id": "C", "role": "domain", "kind": "interval",
         "note": "complex value", "expr": "I", "lo": "0", "hi": "1"},
    ]}
    r = run("check_math.py", suite(tmp_path, spec))
    assert r.returncode == 1, r.stdout + r.stderr
    assert "| C |" in r.stdout and "ERROR" in r.stdout


def test_timeout_fails_closed(tmp_path):
    pytest.importorskip("sympy")
    spec = {"symbols": ["x"], "checks": [
        {"id": "O", "role": "original-condition", "kind": "equal",
         "note": "1 = 1", "lhs": "1", "rhs": "1"},
        {"id": "T", "role": "sanity", "kind": "zero",
         "note": "slow expression", "expr": "expand((x+1)**900)"},
    ]}
    out = tmp_path / "results.json"
    r = run("check_math.py", suite(tmp_path, spec), "--timeout", "0.01", "--json", out)
    assert r.returncode == 1, r.stdout + r.stderr
    results = json.loads(out.read_text(encoding="utf-8"))["results"]
    slow = next(x for x in results if x["id"] == "T")
    assert slow["status"] == "ERROR" and "time limit" in slow["detail"]


def test_report_truncation_notice(tmp_path):
    pytest.importorskip("pdfplumber")
    pdf = tmp_path / "many.pdf"
    blank_pdf(pdf, pages=45)
    r = run("extract_pdf.py", pdf, "--out", tmp_path / "o")
    assert r.returncode == 3, r.stdout + r.stderr
    assert "[OUTPUT TRUNCATED" in r.stdout and "manifest.json" in r.stdout


def test_lint_requires_authorisation_gate(tmp_path):
    dst = copy_skill(tmp_path)
    md = dst / "SKILL.md"
    text = re.sub(r"(?i)explicit authori[sz]ation", "approval",
                  md.read_text(encoding="utf-8"))
    md.write_text(text, encoding="utf-8")
    r = run("lint_skill.py", dst)
    assert r.returncode == 1, r.stdout + r.stderr
    assert "must gate git delivery" in r.stdout


def test_lint_still_flags_other_scripts(tmp_path):
    dst = copy_skill(tmp_path)
    script = dst / "scripts" / "extract_pdf.py"
    script.write_text(script.read_text(encoding="utf-8") + "\n# eval(\n",
                      encoding="utf-8")
    r = run("lint_skill.py", dst)
    assert r.returncode == 1, r.stdout + r.stderr
    assert "unsafe pattern" in r.stdout and "extract_pdf.py" in r.stdout
