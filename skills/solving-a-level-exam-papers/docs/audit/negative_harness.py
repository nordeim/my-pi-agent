import json
import os
import subprocess
from pathlib import Path

ROOT = Path('/tmp/audit')
BASE = ROOT / 'pin'
S = BASE / 'skills/solving-a-level-exam-papers'
UV = ['uv', 'run', '--python', '3.14.7', '--with', 'pytest==9.2.0',
      '--with', 'sympy==1.14.0', '--with', 'pdfplumber==0.11.11', 'python']
PDF = 'samples/2026_Prelim_P1.pdf'
P = ROOT / 'neg'
P.mkdir(exist_ok=True)
results = []


def record(label, exit_code, text):
    lines = [l.strip() for l in (text or '').splitlines() if l.strip()]
    first = next((l for l in lines if 'ERROR' in l or 'usage:' in l or 'G0 FAILED' in l
                  or 'PASS' in l or 'FAIL' in l or 'Traceback' in l), lines[0] if lines else '')
    trace = 'Traceback' in (text or '')
    results.append((label, exit_code, first[:110], trace))


def run(argv, label, cwd=S, wrapper=None):
    cmd = (wrapper or []) + argv
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=90)
        record(label, p.returncode, p.stdout + p.stderr)
        return p
    except subprocess.TimeoutExpired as e:
        record(label, 'TIMEOUT', (e.stdout or b'') + (e.stderr or b''))
        return None


_seq = [0]


def suite(checks, name=None, extra=None):
    _seq[0] += 1
    name = name or f'suite_{_seq[0]}'
    f = P / f'{name}.json'
    f.write_text(json.dumps({'checks': checks}))
    return UV + ['scripts/check_math.py', str(f)] + (extra or [])


def ck(cid='C1', role='original-condition', kind='zero', expr='1-1', **kw):
    d = {'id': cid, 'role': role, 'kind': kind, 'note': cid, 'expr': expr}
    d.update(kw)
    return d


print('=== extract_pdf negative probes ===')
for spec in ('0', '2-1', 'x', '1,,2', '+4', '-3', '1-99999999999'):
    run(UV + ['scripts/extract_pdf.py', PDF, '--pages', spec, '--out', str(P / 'junk'), '--force'],
        f'pages={spec}')
run(UV + ['scripts/extract_pdf.py', 'no-such-file.pdf', '--out', str(P / 'junk'), '--force'],
    'missing_file')
run(['python3', 'scripts/extract_pdf.py', PDF, '--out', str(P / 'junk'), '--force'],
    'missing_dependency(plain python3)')

corrupt = P / 'corrupt.pdf'
corrupt.write_bytes(b'not a pdf at all\n')
run(UV + ['scripts/extract_pdf.py', str(corrupt), '--out', str(P / 'junk'), '--force'], 'corrupt')
unreadable = P / 'unreadable.pdf'
unreadable.write_bytes((S / PDF).read_bytes())
os.chmod(unreadable, 0)
run(UV + ['scripts/extract_pdf.py', str(unreadable), '--out', str(P / 'junk'), '--force'], 'unreadable')
os.chmod(unreadable, 0o644)

# encrypted PDF (generated with pikepdf, fail soft if unavailable)
enc = P / 'encrypted.pdf'
gen = subprocess.run(['uv', 'run', '--with', 'pikepdf', 'python', '-c',
                      f'import pikepdf; d=pikepdf.Pdf.new(); d.add_blank_page(page_size=(200,200)); '
                      f'd.save(r"{enc}", encryption=pikepdf.Encryption(owner="o", user="u", R=6))'],
                     cwd=P, capture_output=True, text=True, timeout=180)
if enc.exists():
    run(UV + ['scripts/extract_pdf.py', str(enc), '--out', str(P / 'junk'), '--force'], 'encrypted')
else:
    record('encrypted (pikepdf unavailable)', 'NOT-RUN', gen.stderr[:100])

# textless PDF via reportlab blank page
blank = P / 'blank.pdf'
gen = subprocess.run(['uv', 'run', '--with', 'reportlab', 'python', '-c',
                      f'from reportlab.pdfgen import canvas; c=canvas.Canvas(r"{blank}"); c.showPage(); c.save()'],
                     cwd=P, capture_output=True, text=True, timeout=180)
if blank.exists():
    run(UV + ['scripts/extract_pdf.py', str(blank), '--out', str(P / 'textless'), '--force'], 'textless')
    collision = P / 'render_collision'
    collision.mkdir(exist_ok=True)
    (collision / 'page-1.png').write_bytes(b'x')
    run(UV + ['scripts/extract_pdf.py', str(blank), '--render', '--out', str(collision)],
        'render_refusal(existing png)')
    print('   V-25 check: pages.txt present after refusal?', (collision / 'pages.txt').exists(),
          'temp files:', [x.name for x in collision.iterdir()])
    run(UV + ['scripts/extract_pdf.py', str(blank), '--render', '--out', str(P / 'render_ok'), '--force'],
        'render_textless(no collision)')
    print('   render outputs:', sorted(x.name for x in (P / 'render_ok').iterdir()))
else:
    record('textless/render (reportlab unavailable)', 'NOT-RUN', gen.stderr[:100])

overwrite = P / 'overwrite'
overwrite.mkdir(exist_ok=True)
(overwrite / 'pages.txt').write_text('x')
run(UV + ['scripts/extract_pdf.py', PDF, '--out', str(overwrite)], 'overwrite_refusal')

print('=== check_math negative probes ===')
run(suite([]), 'empty_suite')
run(suite([ck()]), 'one_check')
run(suite([ck('D'), ck('D')]), 'duplicate_ids')
run(suite([ck(role='sanity')]), 'zero_original_condition')
run(suite([ck(f'C{i}') for i in range(201)]), '201_checks')
run(suite([ck()], extra=['--min-checks', '1']), 'min_checks_1')
run(suite([ck()], extra=['--timeout', '0']), 'timeout_0')
run(suite([ck()], extra=['--timeout', '-1']), 'timeout_neg1')
run(suite([ck(expr='eval("1")')]), 'unsafe_eval')
run(suite([ck(expr='__import__("os")')]), 'unsafe_import')
run(suite([ck(expr='Matrix([[1]]) - 1')]), 'matrix_vs_scalar')
run(suite([ck(expr='0.5 - 0.5')]), 'float_in_exact')
run(suite([ck(expr='pi - pi')]), 'reserved_symbol_pi')

badjson = P / 'unwritable.json'
badjson.mkdir(exist_ok=True)
run(suite([ck()]) + ['--json', str(badjson)], 'json_write_failure')

for label, expr in [('expand_900', 'expand((x+1)**900) - 1'),
                    ('integrate_1000', 'integrate(1/(1+x**1000),x)'),
                    ('matrix64_pow50', 'Matrix(64,64,[1]*4096)**50')]:
    f = P / f'heavy_{label}.json'
    f.write_text(json.dumps({'symbols': ['x'], 'checks': [ck('H', expr=expr)]}))
    run(UV + ['scripts/check_math.py', str(f)], f'heavy_{label}',
        wrapper=['timeout', '70'])
run(suite([ck(expr='1/0')]), 'div_by_zero_zoo')
run(suite([ck(expr='factorial(10000) - 0')]), 'factorial_10000')

print('\n=== PROBE INVENTORY (label | exit | first line | traceback) ===')
for r in results:
    print(f'{r[0]} | {r[1]} | {r[2]} | traceback={r[3]}')
