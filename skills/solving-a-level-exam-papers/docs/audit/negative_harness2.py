import json
import shlex
import subprocess
from pathlib import Path

ROOT = Path('/tmp/audit')
P = ROOT / 'neg'
S = ROOT / 'pin/skills/solving-a-level-exam-papers'
UV = ['uv', 'run', '--python', '3.14.7', '--with', 'pytest==9.2.0',
      '--with', 'sympy==1.14.0', '--with', 'pdfplumber==0.11.11', 'python']
rows = []


def ck(cid, role='original-condition', kind='zero', expr='1-1'):
    return {'id': cid, 'role': role, 'kind': kind, 'note': cid, 'expr': expr}


def record(label, p):
    text = (p.stdout or '') + (p.stderr or '')
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    first = next((l for l in lines if 'ERROR' in l or 'CONFIG ERROR' in l or 'checks passed' in l
                  or 'Traceback' in l), lines[0] if lines else '')
    rows.append((label, p.returncode, first[:120], 'Traceback' in text))


def run(cmd, label, timeout=90, cwd=S):
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        record(label, p, )
    except subprocess.TimeoutExpired:
        rows.append((label, 'TIMEOUT', 'outer timeout', False))


def suite(name, probe, symbols=()):
    spec = {'checks': [ck('C0'), probe]}
    if symbols:
        spec['symbols'] = list(symbols)
    f = P / f'v2_{name}.json'
    f.write_text(json.dumps(spec))
    return UV + ['scripts/check_math.py', str(f)]


print('=== missing-dependency probe (no site-packages) ===')
run(['python3', '-S', 'scripts/extract_pdf.py', 'samples/2026_Prelim_P1.pdf',
     '--out', str(P / 'junk'), '--force'], 'missing_dependency(-S)')

print('=== corrected check_math probes (all 2-check suites) ===')
run(suite('zero_roles', ck('C1', role='sanity')), 'zero_original_condition(2 checks)')
run(suite('eval', ck('C1', expr='eval("1")')), 'unsafe_eval')
run(suite('import', ck('C1', expr='__import__("os")')), 'unsafe_import')
run(suite('matrix', ck('C1', expr='Matrix([[1]]) - 1')), 'matrix_vs_scalar')
run(suite('float', ck('C1', expr='0.5 - 0.5')), 'float_in_exact')
run(suite('symbol', ck('C1', expr='pi - pi'), symbols=('pi',)), 'reserved_symbol_pi')
bad = P / 'unwritable2'
bad.mkdir(exist_ok=True)
run(suite('jsonfail', ck('C1')) + ['--json', str(bad)], 'json_write_failure')

for name, expr in [('expand900', 'expand((x+1)**900) - 1'),
                   ('integrate1000', 'integrate(1/(1+x**1000),x)'),
                   ('matrix64', 'Matrix(64,64,[1]*4096)**50')]:
    spec = {'symbols': ['x'], 'checks': [ck('C0'), ck('C1', expr=expr)]}
    f = P / f'v2_heavy_{name}.json'
    f.write_text(json.dumps(spec))
    cmd = ' '.join(shlex.quote(x) for x in UV + ['scripts/check_math.py', str(f)])
    run(['bash', '-c', f'ulimit -v 4000000; timeout 70 {cmd}'], f'heavy_{name}', timeout=100)

run(suite('zoo', ck('C1', expr='1/0')), 'div_by_zero_zoo')
run(suite('fact', ck('C1', expr='factorial(10000) - factorial(10000)')), 'factorial_10000')
run(suite('caps', ck('C1', expr='eye(65)')), 'eye_65_rejected')
run(suite('caps2', ck('C1', expr='eye(64)')), 'eye_64_allowed')
run(suite('bigpow', ck('C1', expr='2**1001')), 'pow_1001_rejected')

print('\n=== CORRECTED PROBE INVENTORY ===')
for r in rows:
    print(f'{r[0]} | {r[1]} | {r[2]} | traceback={r[3]}')
