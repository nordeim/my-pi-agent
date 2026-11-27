#!/usr/bin/env python3
"""Compare repo skills/ with sandbox workspace skills/ to plan enhancement merges.

For each skill name present in BOTH:
- record file counts, SKILL.md sizes, description hashes
- classify: identical SKILL.md / sandbox-only files / repo-only files / both
Output: JSON report + console summary.
"""
import hashlib
import json
import sys
from pathlib import Path

REPO = Path("/home/z/my-project/my-pi-agent/skills")
SANDBOX = Path("/home/z/my-project/skills")
OUT = Path("/home/z/my-project/scripts/overlap_report.json")


def skill_dirs(base: Path) -> dict[str, Path]:
    """name -> dir for top-level folders containing SKILL.md."""
    out = {}
    if not base.is_dir():
        return out
    for d in sorted(base.iterdir()):
        if d.is_dir() and (d / "SKILL.md").is_file():
            out[d.name] = d
    return out


def rel_files(d: Path) -> set[str]:
    return {p.relative_to(d).as_posix() for p in d.rglob("*")
            if p.is_file() and "__pycache__" not in p.parts
            and not any(part.startswith(".") for part in p.parts)}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    repo, box = skill_dirs(REPO), skill_dirs(SANDBOX)
    common = sorted(set(repo) & set(box))
    report = {"repo_total": len(repo), "sandbox_total": len(box),
              "common": len(common),
              "repo_only": sorted(set(repo) - set(box)),
              "sandbox_only": sorted(set(box) - set(repo)),
              "matches": []}
    for name in common:
        r, b = repo[name], box[name]
        rf, bf = rel_files(r), rel_files(b)
        rmd, bmd = r / "SKILL.md", b / "SKILL.md"
        match = {
            "name": name,
            "repo_files": len(rf), "sandbox_files": len(bf),
            "skill_md_identical": sha(rmd) == sha(bmd),
            "identical_files": sorted(rf & bf),
            "sandbox_only_files": sorted(bf - rf),
            "repo_only_files": sorted(rf - bf),
        }
        # which identical-named files actually differ in content?
        diff_content = []
        for f in sorted(rf & bf):
            if f == "SKILL.md":
                continue
            try:
                if sha(r / f) != sha(b / f):
                    diff_content.append(f)
            except OSError:
                diff_content.append(f)
        match["differing_files"] = diff_content
        report["matches"].append(match)

    OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"repo skills: {report['repo_total']}; sandbox skills: {report['sandbox_total']}; "
          f"common: {report['common']}")
    print(f"repo-only: {len(report['repo_only'])}; sandbox-only: {len(report['sandbox_only'])}")
    ident = [m for m in report["matches"] if m["skill_md_identical"]]
    richer = [m for m in report["matches"]
              if m["sandbox_only_files"] and not m["skill_md_identical"]]
    print(f"\nSKILL.md identical: {len(ident)}")
    print(f"Sandbox has extra files AND different SKILL.md (prime enhance candidates): {len(richer)}")
    for m in richer:
        extra = m["sandbox_only_files"]
        print(f"  {m['name']}: +{len(extra)} sandbox files, "
              f"{len(m['differing_files'])} differing files "
              f"(repo {m['repo_files']} / box {m['sandbox_files']})")
    diff_only = [m for m in report["matches"]
                 if not m["skill_md_identical"] and not m["sandbox_only_files"]]
    print(f"\nDifferent SKILL.md, no sandbox-only files: {len(diff_only)}")
    for m in diff_only:
        print(f"  {m['name']} (repo {m['repo_files']} / box {m['sandbox_files']} files, "
              f"{len(m['differing_files'])} differing)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
