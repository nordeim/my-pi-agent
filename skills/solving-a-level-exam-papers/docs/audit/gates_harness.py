import json
import subprocess
import sys
from pathlib import Path

ROOT = Path('/tmp/audit')
UV = ['uv', 'run', '--python', '3.14.7', '--with', 'pytest==9.2.0',
      '--with', 'sympy==1.14.0', '--with', 'pdfplumber==0.11.11', 'python']
SUITES = {
    'eigen': {"checks": [
        {"id": "E1", "role": "original-condition", "kind": "equal", "note": "A v = 2 v",
         "lhs": "Matrix([[2,0],[0,3]])*Matrix([[1],[0]])", "rhs": "2*Matrix([[1],[0]])"},
        {"id": "E2", "role": "independent-method", "kind": "zero", "note": "det = 6",
         "expr": "det(Matrix([[2,0],[0,3]])) - 6"}]},
    'inverse': {"checks": [
        {"id": "I1", "role": "original-condition", "kind": "zero", "note": "A A^-1 = I",
         "expr": "Matrix([[1,2],[3,4]])*inv(Matrix([[1,2],[3,4]])) - eye(2)"},
        {"id": "I2", "role": "independent-method", "kind": "zero", "note": "det = -2",
         "expr": "det(Matrix([[1,2],[3,4]])) + 2"}]},
    'tangency': {"symbols": ["u"], "checks": [
        {"id": "T1", "role": "original-condition", "kind": "zero", "note": "discriminant = 0",
         "expr": "discriminant(25*u**2 - 30*sqrt(14)*u + 126, u)"},
        {"id": "T2", "role": "domain", "kind": "interval", "note": "sqrt14 in (3,4)",
         "expr": "sqrt(14)", "lo": "3", "hi": "4"}]},
    'antiderivative': {"symbols": ["x"], "checks": [
        {"id": "A1", "role": "original-condition", "kind": "zero", "note": "F' = f",
         "expr": "diff(sin(x)+3, x) - cos(x)"},
        {"id": "A2", "role": "original-condition", "kind": "zero", "note": "F(0) = 3",
         "expr": "sin(0)+3 - 3"}]},
}


def run(cmd, cwd, label):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=180)
    print(f'--- {label} exit={p.returncode} ---')
    out = (p.stdout + p.stderr).strip().splitlines()
    for line in out[-6:]:
        print('   ', line)
    return p


for base in ('pin', 'head'):
    s = ROOT / base / 'skills/solving-a-level-exam-papers'
    print(f'================ {base} ================')
    r3json = ROOT / f'{base}_r3.json'
    run(UV + ['scripts/check_math.py', 'assets/checks.example.json', '--json', str(r3json)], s, 'R3 example')
    if r3json.exists():
        prov = json.loads(r3json.read_text())['provenance']
        print('   R3 provenance:', prov)

    subset = ROOT / f'{base}_subset'
    run(UV + ['scripts/extract_pdf.py', 'samples/2026_Prelim_P1.pdf',
              '--pages', '4,16-18', '--out', str(subset), '--force'], s, 'R4 subset')
    mf = subset / 'manifest.json'
    if mf.exists():
        m = json.loads(mf.read_text())
        print('   R4 subset:', {'pages_ingested': m['pages_ingested'],
                                'no_text_pages': m['no_text_pages'], 'gate_G0': m['gate_G0'],
                                'sha256': m['sha256']})
    full = ROOT / f'{base}_full'
    run(UV + ['scripts/extract_pdf.py', 'samples/2026_Prelim_P1.pdf',
              '--out', str(full), '--force'], s, 'R4 full')
    mf = full / 'manifest.json'
    if mf.exists():
        m = json.loads(mf.read_text())
        print('   R4 full:', {'pages_ingested': m['pages_ingested'],
                              'no_text_pages': m['no_text_pages'], 'gate_G0': m['gate_G0']})

    for name, spec in SUITES.items():
        f = ROOT / f'{base}_r6_{name}.json'
        f.write_text(json.dumps(spec))
        p = run(UV + ['scripts/check_math.py', str(f)], s, f'R6 {name}')
        print('   R6', name, 'summary:', next((l for l in p.stdout.splitlines() if 'checks passed' in l), 'n/a'))
