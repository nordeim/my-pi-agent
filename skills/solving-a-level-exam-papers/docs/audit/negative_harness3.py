import json
import subprocess
from pathlib import Path

P = Path('/tmp/audit/neg')
S = Path('/tmp/audit/pin/skills/solving-a-level-exam-papers')
UV = ['uv', 'run', '--python', '3.14.7', '--with', 'sympy==1.14.0', 'python']


def ck(cid, role='original-condition', kind='zero', expr='1-1'):
    return {'id': cid, 'role': role, 'kind': kind, 'note': cid, 'expr': expr}


def go(name, checks, extra=(), symbols=()):
    spec = {'checks': checks}
    if symbols:
        spec['symbols'] = list(symbols)
    f = P / f'v3_{name}.json'
    f.write_text(json.dumps(spec))
    p = subprocess.run(UV + ['scripts/check_math.py', str(f), *extra], cwd=S,
                       capture_output=True, text=True, timeout=120)
    text = (p.stdout + p.stderr).strip().splitlines()
    interesting = [l for l in text if 'CONFIG ERROR' in l or 'checks passed' in l or 'ERROR' in l and '|' not in l]
    print(f'{name}: exit={p.returncode} | {interesting[:2]}')
    return p


go('no_original', [ck('C1', role='sanity'), ck('C2', role='domain')])
go('float_survives', [ck('C0'), ck('C1', expr='0.5 - 0.25')])
go('float_degenerate', [ck('C0'), ck('C1', expr='0.5 - 0.5')])
go('factorial10000', [ck('C0'), ck('C1', expr='factorial(10000) - 0')])
go('factorial10001', [ck('C0'), ck('C1', expr='factorial(10001) - 0')])
d = P / 'dirjson3'
d.mkdir(exist_ok=True)
go('json_to_directory', [ck('C0'), ck('C1')], extra=['--json', str(d)])
