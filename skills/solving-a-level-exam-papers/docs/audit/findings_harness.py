import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path('/tmp/audit')
S = ROOT / 'head/skills/solving-a-level-exam-papers'
P = ROOT / 'findings'
P.mkdir(exist_ok=True)
UV = ['uv', 'run', '--python', '3.14.7', '--with', 'sympy==1.14.0', 'python']
UVALL = ['uv', 'run', '--python', '3.14.7', '--with', 'sympy==1.14.0',
         '--with', 'pdfplumber==0.11.11', 'python']


def run(cmd, cwd=S, timeout=120):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)


def ck(cid, expr='1-1', note='C'):
    return {'id': cid, 'role': 'original-condition', 'kind': 'zero', 'note': note, 'expr': expr}


def checks(name, rows):
    f = P / f'{name}.json'
    f.write_text(json.dumps({'checks': rows}))
    return f

print('=== N-4 ledger escaping ===')
f = checks('n4', [ck('C0', note=r'a\|b'), ck('C1')])
p = run(UV + ['scripts/check_math.py', str(f)])
print('  exit', p.returncode)
print('  ledger row:', repr(next(l for l in p.stdout.splitlines() if '| C0 |' in l)))

print('=== N-7 nested brace expansion ===')
sys.path.insert(0, str(S / 'scripts'))
from lint_skill import expand_braces
print('  expand_braces:', expand_braces('references/{a,{b,c}}.md'))

print('=== N-8 partial output / temp leak ===')
out = P / 'n8'
if out.exists():
    shutil.rmtree(out)
(out / 'manifest.json').mkdir(parents=True)
p = run(UVALL + ['scripts/extract_pdf.py', 'samples/2026_Prelim_P1.pdf',
                 '--out', str(out), '--force'])
print('  exit', p.returncode, 'pages.txt exists:', (out / 'pages.txt').exists())
print('  dir contents:', sorted(x.name for x in out.iterdir()))

print('=== N-9 duplicate page specs ===')
out = P / 'n9'
if out.exists():
    shutil.rmtree(out)
p = run(UVALL + ['scripts/extract_pdf.py', 'samples/2026_Prelim_P1.pdf',
                 '--pages', '1,1', '--out', str(out), '--force'])
m = json.loads((out / 'manifest.json').read_text())
print('  exit', p.returncode, 'pages_ingested', m['pages_ingested'],
      'page numbers', [x['page'] for x in m['pages']])

print('=== N-11 hidden-path completeness blind spot ===')
rg = P / 'n11'
if rg.exists():
    shutil.rmtree(rg)
shutil.copytree(S, rg)
(rg / 'scripts/__init__.py').write_text('')
(rg / 'scripts/.secret.py').write_text('x=1\n')
p = run(['python3', 'scripts/lint_skill.py', '.'], cwd=rg)
print('  lint exit with scripts/__init__.py + scripts/.secret.py:', p.returncode,
      '|', p.stdout.strip().splitlines()[-1])

print('=== N-6 getattr documentation absence ===')
for f in list((S / 'references').glob('*.md')) + [S / 'SKILL.md']:
    if 'getattr' in f.read_text():
        print('  FOUND getattr in', f.relative_to(S))
print('  remediation_plan.md mentions getattr:',
      'getattr' in (S / 'docs/remediation_plan.md').read_text())

print('=== security reject battery ===')
payloads = {
    'nested_pow': '2**(3**4)', 'xor': '2^3', 'attribute': 'pi.real',
    'subscript': '[1][0]', 'lambda': '(lambda x:x)(1)',
    'comprehension': '[x for x in [1]]', 'dunder': '__import__("os")',
    'unknown_name': 'foobar', 'string': '"abc"', 'complex': '1+2j', 'boolean': 'True',
    'pow_1001': '2**1001', 'seq_4097': '[1]*4097',
}
for name, expr in payloads.items():
    f = checks(f'sec_{name}', [ck('C0'), ck('C1', expr=expr)])
    p = run(UV + ['scripts/check_math.py', str(f)])
    msg = next((l for l in (p.stdout + p.stderr).splitlines() if 'CONFIG ERROR' in l), '')
    print(f'  {name}: exit={p.returncode} {msg[:90]}')
for name, expr in {'pow_1000': '2**1000', 'seq_4096': '[1]*4096'}.items():
    f = checks(f'sec_{name}', [ck('C0'), ck('C1', expr=expr)])
    p = run(UV + ['scripts/check_math.py', str(f)])
    print(f'  {name}: exit={p.returncode} (allowed by whitelist; check result may FAIL)')
