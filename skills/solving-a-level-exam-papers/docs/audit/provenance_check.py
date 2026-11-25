import hashlib
import json
import re
from pathlib import Path

ROOT = Path('/tmp/audit')
SKILL = 'skills/solving-a-level-exam-papers'


def manifest(base):
    d = ROOT / base / SKILL
    out = {}
    for p in sorted(d.rglob('*')):
        if p.is_file() and '__pycache__' not in p.parts and '.pytest_cache' not in p.parts:
            out[str(p.relative_to(d))] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


pin = manifest('pin')
head = manifest('head')
parent = manifest('parent')

record = json.loads((ROOT / 'head' / SKILL / 'docs/validation_record_current.json').read_text())
json_hashes = record['provenance']['sha256']

rev6 = (ROOT / 'head' / SKILL / 'docs/revalidation_rev6.md').read_text()
appendix = {}
for line in rev6.splitlines():
    m = re.match(r'^([0-9a-f]{64})\s+(\S+)$', line.strip())
    if m:
        appendix[m.group(2)] = m.group(1)

print('== PIN: count ==', len(pin))
print('== PIN vs JSON provenance.sha256 ==')
print('  JSON entries:', len(json_hashes))
matched = [k for k in json_hashes if pin.get(k) == json_hashes[k]]
print(f'  matched: {len(matched)}/{len(json_hashes)}')
print('  mismatched:', [k for k in json_hashes if pin.get(k) != json_hashes[k]])
print('  pin files absent from JSON:', sorted(set(pin) - set(json_hashes)))
print('== PIN vs rev6 Appendix A ==')
print('  appendix entries:', len(appendix))
print(f'  matched: {sum(1 for k in appendix if pin.get(k) == appendix[k])}/{len(appendix)}')
print('  mismatched:', [k for k in appendix if pin.get(k) != appendix[k]])
print('  pin files absent from appendix:', sorted(set(pin) - set(appendix)))

print('== HEAD: count ==', len(head))
added = sorted(set(head) - set(pin))
removed = sorted(set(pin) - set(head))
changed = sorted(k for k in set(head) & set(pin) if head[k] != pin[k])
print('  added:', added)
print('  removed:', removed)
print('  changed:', changed)
print('== PARENT: count ==', len(parent))
print('  parent vs pin added:', sorted(set(pin) - set(parent)))
print('  parent vs pin removed:', sorted(set(parent) - set(pin)))
print('  parent vs pin changed:', sorted(k for k in set(parent) & set(pin) if parent[k] != pin[k]))

print('== D-a byte-level check: N-4 evidence/fix strings ==')
n4 = next(f for f in record['findings'] if f['id'] == 'N-4')
for key in ('evidence', 'fix'):
    raw = re.search(r'"' + key + r'":\s*"(.*)"\s*,?\s*\n', (ROOT / 'head' / SKILL / 'docs/validation_record_current.json').read_text())
    print(f'  {key} decoded repr: {n4[key]!r}')
    print(f'  {key} raw JSON line: {raw.group(1) if raw else "NOT FOUND"}')
print('  fix contains ".replace(\'\\\\\',\'\\\\\\\\\')"?', ".replace('\\\\','\\\\\\\\')" in n4['fix'])
