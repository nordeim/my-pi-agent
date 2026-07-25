#!/usr/bin/env python3
"""partition_bugs.py — split merged bugs.json into disjoint per-file fix sets so parallel
Fix agents never edit the same file. See references/00-contract.md §2 (Fix fan-out).

Usage: partition_bugs.py <bugs.json> <out_dir> <max_parallel>

Groups bugs by their target file (bug['file'] or parsed from bug['fix_hint']), then bin-packs
file-groups into <= max_parallel sets. Each fix-set-{k}.json owns a disjoint set of files.
"""
import json, os, re, sys
from collections import defaultdict

def target_file(bug):
    if bug.get("file"):
        return bug["file"]
    hint = bug.get("fix_hint", "") + " " + bug.get("element", "")
    m = re.search(r"[\w./-]+\.(?:tsx|ts|jsx|js|css|scss)", hint)
    return m.group(0) if m else "_unassigned"

def main():
    bugs_path, out_dir, max_parallel = sys.argv[1], sys.argv[2], int(sys.argv[3])
    try:
        bugs = json.load(open(bugs_path))
    except Exception:
        return
    if not bugs:
        return
    os.makedirs(out_dir, exist_ok=True)
    by_file = defaultdict(list)
    for b in bugs:
        by_file[target_file(b)].append(b)
    # bin-pack file-groups (largest first) into N sets balanced by bug count
    groups = sorted(by_file.items(), key=lambda kv: -len(kv[1]))
    n = max(1, min(max_parallel, len(groups)))
    sets = [[] for _ in range(n)]
    loads = [0] * n
    for _file, items in groups:
        i = loads.index(min(loads))
        sets[i].extend(items)
        loads[i] += len(items)
    k = 0
    for s in sets:
        if not s:
            continue
        json.dump(s, open(os.path.join(out_dir, f"fix-set-{k}.json"), "w"), indent=2)
        k += 1
    print(f"partitioned {len(bugs)} bugs across {k} fix set(s)")

if __name__ == "__main__":
    main()
