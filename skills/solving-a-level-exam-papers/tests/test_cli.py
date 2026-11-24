import json, subprocess, sys
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


def blank_pdf(path):
    objs = [b"<</Type/Catalog/Pages 2 0 R>>",
            b"<</Type/Pages/Kids[3 0 R]/Count 1>>",
            b"<</Type/Page/Parent 2 0 R/MediaBox[0 0 200 200]/Resources<<>>/Contents 4 0 R>>",
            b"<</Length 0>>stream\nendstream\n"]
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


def test_no_overwrite_then_force(tmp_path):
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
