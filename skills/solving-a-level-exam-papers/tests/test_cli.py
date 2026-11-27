import json, re, shutil, subprocess, sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
EXAMPLE = json.loads((ROOT / "assets" / "checks.example.json").read_text())
sys.path.insert(0, str(SCRIPTS))
import extract_pdf  # noqa: E402


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
                    ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
    return dst


def test_example_suite_passes(tmp_path):
    pytest.importorskip("sympy")
    r = run("check_math.py", suite(tmp_path, EXAMPLE))
    assert r.returncode == 0, r.stdout + r.stderr
    assert "7/7 checks passed." in r.stdout
    assert "checks_sha256=" in r.stdout


def test_ledger_escapes_pipes_and_newlines(tmp_path):
    # Regression V-23: a pipe or newline in a note broke the Markdown ledger.
    pytest.importorskip("sympy")
    spec = two_check_suite({"kind": "zero", "expr": "0", "note": "a | b\nc"})
    r = run("check_math.py", suite(tmp_path, spec))
    assert r.returncode == 0, r.stdout + r.stderr
    assert "| a \\| b c |" in r.stdout


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


def test_render_refuses_existing_png_without_force(tmp_path):
    # Regression V-25: --render wrote page images before the overwrite check.
    pytest.importorskip("pdfplumber")
    pdf = tmp_path / "blank.pdf"
    blank_pdf(pdf)
    out = tmp_path / "o"
    out.mkdir()
    sentinel = out / "page-1.png"
    sentinel.write_bytes(b"SENTINEL")
    r = run("extract_pdf.py", pdf, "--out", out, "--render")
    assert r.returncode == 2, r.stdout + r.stderr
    assert "refusing to overwrite" in r.stderr
    assert sentinel.read_bytes() == b"SENTINEL"
    assert not (out / "pages.txt").exists()


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
    script.write_text(script.read_text(encoding="utf-8") + "\nresult = eval('1')\n",
                      encoding="utf-8")
    r = run("lint_skill.py", dst)
    assert r.returncode == 1, r.stdout + r.stderr
    assert "unsafe pattern" in r.stdout and "extract_pdf.py" in r.stdout


@pytest.mark.parametrize("snippet", [
    "run = eval\n",                                  # alias, invisible to a call-text scan
    "result = eval ('1')\n",                         # whitespace defeats a literal 'eval(' match
    "from sympy import sympify\n",
    "import subprocess\nsubprocess.run('ls', shell=True)\n",
    "import os\nos.system('true')\n",
])
def test_lint_flags_executable_unsafe_constructs(tmp_path, snippet):
    dst = copy_skill(tmp_path)
    script = dst / "scripts" / "extract_pdf.py"
    script.write_text(script.read_text(encoding="utf-8") + "\n" + snippet, encoding="utf-8")
    r = run("lint_skill.py", dst)
    assert r.returncode == 1 and "unsafe pattern" in r.stdout, r.stdout + r.stderr


def test_lint_ignores_inert_mentions_and_copies_of_itself(tmp_path):
    # Regression V-19: the text scan flagged every copy of lint_skill.py (its own
    # ban list), so linting a sibling skill that ships the same script failed.
    dst = copy_skill(tmp_path)
    script = dst / "scripts" / "extract_pdf.py"
    script.write_text(script.read_text(encoding="utf-8") +
                      '\n# never call eval( or sympify( here\nNOTE = "exec( is banned"\n',
                      encoding="utf-8")
    r = run("lint_skill.py", dst)
    assert r.returncode == 0, r.stdout + r.stderr


def test_lint_flags_unparseable_script(tmp_path):
    dst = copy_skill(tmp_path)
    (dst / "scripts" / "broken.py").write_text("def (:\n", encoding="utf-8")
    r = run("lint_skill.py", dst)
    assert r.returncode == 1 and "does not parse" in r.stdout


def two_check_suite(extra):
    return {"checks": [
        {"id": "O", "role": "original-condition", "kind": "equal",
         "note": "1 = 1", "lhs": "1", "rhs": "1"},
        {"id": "X", "role": "sanity", "note": "check under test", **extra},
    ]}


def test_missing_checks_file_exit2(tmp_path):
    # Regression V-15: read_bytes() sat outside the try block and raised a traceback.
    pytest.importorskip("sympy")
    r = run("check_math.py", tmp_path / "absent.json")
    assert r.returncode == 2 and "CONFIG ERROR" in r.stderr
    assert "Traceback" not in r.stderr


@pytest.mark.parametrize("extra", [
    {"kind": "zero", "expr": "[1, 2]"},
    {"kind": "approx", "lhs": "[1, 2]", "rhs": "1"},
    {"kind": "interval", "expr": "eye(2)", "lo": "0", "hi": "1"},
    {"kind": "equal", "lhs": "eye(2)", "rhs": "1"},
])
def test_non_scalar_or_mismatched_result_exit2(tmp_path, extra):
    # Regression V-11: config-class type errors must be exit 2, not a maths ERROR.
    pytest.importorskip("sympy")
    r = run("check_math.py", suite(tmp_path, two_check_suite(extra)))
    assert r.returncode == 2, r.stdout + r.stderr
    assert "CONFIG ERROR" in r.stderr


def test_true_matrix_identity_passes(tmp_path):
    # Regression V-16: Matrix - Matrix was compared with `== 0` and reported a false FAIL.
    pytest.importorskip("sympy")
    spec = two_check_suite({"kind": "equal",
                            "lhs": "Matrix([[1,2],[3,4]])*Matrix([[1],[0]])",
                            "rhs": "Matrix([[1],[3]])"})
    r = run("check_math.py", suite(tmp_path, spec))
    assert r.returncode == 0, r.stdout + r.stderr


def test_matrix_zero_and_false_matrix_claim(tmp_path):
    pytest.importorskip("sympy")
    ok = run("check_math.py", suite(tmp_path, two_check_suite(
        {"kind": "zero", "expr": "Matrix([[1,2],[3,4]])*inv(Matrix([[1,2],[3,4]])) - eye(2)"})))
    assert ok.returncode == 0, ok.stdout + ok.stderr
    bad = run("check_math.py", suite(tmp_path, two_check_suite(
        {"kind": "equal", "lhs": "Matrix([[1,2],[3,4]])", "rhs": "Matrix([[1,2],[3,5]])"})))
    assert bad.returncode == 1 and "FAIL" in bad.stdout


@pytest.mark.parametrize("pages", ["abc", "3-1", "0", "1,,2", "-2", "1-2-3"])
def test_pages_garbage_exit2(tmp_path, pages):
    # Regression V-8: int() ValueError escaped as a traceback with exit 1.
    pytest.importorskip("pdfplumber")
    pdf = tmp_path / "blank.pdf"
    blank_pdf(pdf)
    r = run("extract_pdf.py", pdf, "--out", tmp_path / "o", "--pages", pages)
    assert r.returncode == 2, r.stdout + r.stderr
    assert "Traceback" not in r.stderr and "--pages" in r.stderr


def test_pages_out_of_range_exit2(tmp_path):
    # --pages 999 used to report "G0 FAILED ... ALL" (exit 3), masking a usage error.
    pytest.importorskip("pdfplumber")
    pdf = tmp_path / "blank.pdf"
    blank_pdf(pdf, pages=2)
    r = run("extract_pdf.py", pdf, "--out", tmp_path / "o", "--pages", "1,5")
    assert r.returncode == 2 and "out of range" in r.stderr


def test_lint_flags_broken_referenced_path(tmp_path):
    # Regression V-5: the old link check only parsed ](...) links, which SKILL.md never uses.
    dst = copy_skill(tmp_path)
    md = dst / "SKILL.md"
    md.write_text(md.read_text(encoding="utf-8") + "\nSee `references/nope.md`.\n",
                  encoding="utf-8")
    r = run("lint_skill.py", dst)
    assert r.returncode == 1, r.stdout + r.stderr
    assert "references/nope.md" in r.stdout


def test_lint_flags_unlisted_tree_entry(tmp_path):
    dst = copy_skill(tmp_path)
    md = dst / "SKILL.md"
    text = md.read_text(encoding="utf-8").replace("├── assets/", "├── ghost/{a,b}.md\n├── assets/", 1)
    md.write_text(text, encoding="utf-8")
    r = run("lint_skill.py", dst)
    assert r.returncode == 1 and "ghost/a.md" in r.stdout


def test_lint_flags_unlisted_package_file(tmp_path):
    # Regression V-24: a real file omitted from the tree passed the old check.
    dst = copy_skill(tmp_path)
    (dst / "docs" / "unlisted_orphan.md").write_text("x", encoding="utf-8")
    r = run("lint_skill.py", dst)
    assert r.returncode == 1, r.stdout + r.stderr
    assert "unlisted package file: docs/unlisted_orphan.md" in r.stdout


def test_lint_flags_hidden_and_dunder_package_files(tmp_path):
    # Regression N-11: excluding every dot/dunder path component let
    # scripts/__init__.py and scripts/.secret.py slip past the completeness
    # check; only known artifact directories are skipped now.
    dst = copy_skill(tmp_path)
    (dst / "scripts" / "__init__.py").write_text("", encoding="utf-8")
    (dst / "scripts" / ".secret.py").write_text("x = 1\n", encoding="utf-8")
    r = run("lint_skill.py", dst)
    assert r.returncode == 1, r.stdout + r.stderr
    assert "unlisted package file: scripts/__init__.py" in r.stdout
    assert "unlisted package file: scripts/.secret.py" in r.stdout


def test_command_words_distinguish_hence_and_deduce():
    # Regression V-14: "Hence / Deduce" had been merged into a single obligation.
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    assert "| Hence |" in skill and "| Deduce |" in skill
    assert "**\"Deduce\"**" in (ROOT / "references" / "exam-presentation.md").read_text(encoding="utf-8")


def test_skill_tree_lists_every_top_level_directory():
    # Regression V-12: the file tree omitted samples/ and docs/.
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    for d in sorted(p.name for p in ROOT.iterdir() if p.is_dir() and not p.name.startswith((".", "__"))):
        assert f"├── {d}/" in skill or f"└── {d}/" in skill, f"tree omits {d}/"


def test_unreadable_pdf_exit2(tmp_path, monkeypatch, capsys):
    # Regression V-22: read_bytes() raised PermissionError as a traceback (exit 1).
    pytest.importorskip("pdfplumber")
    pdf = tmp_path / "locked.pdf"
    pdf.write_bytes(b"%PDF-1.4\n")

    def boom(self):
        raise PermissionError(13, "Permission denied", str(self))

    monkeypatch.setattr(Path, "read_bytes", boom)
    monkeypatch.setattr(sys, "argv", ["extract_pdf.py", str(pdf)])
    assert extract_pdf.main() == 2
    err = capsys.readouterr().err
    assert "CONFIG ERROR" in err and "Traceback" not in err


def test_corrupt_pdf_exit2(tmp_path):
    # Regression V-18: a non-PDF input escaped as a PdfminerException traceback (exit 1).
    pytest.importorskip("pdfplumber")
    bad = tmp_path / "bad.pdf"
    bad.write_text("this is not a pdf", encoding="utf-8")
    r = run("extract_pdf.py", bad, "--out", tmp_path / "o")
    assert r.returncode == 2, r.stdout + r.stderr
    assert "CONFIG ERROR" in r.stderr and "Traceback" not in r.stderr
