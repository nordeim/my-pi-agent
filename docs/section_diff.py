#!/usr/bin/env python3
"""Two-way section analysis: for the non-identical matched skills, find
headings/sections present in the SANDBOX SKILL.md that are absent from the
REPO SKILL.md (candidate enhancement content), and vice versa."""
import re
import sys
from pathlib import Path

REPO = Path("/home/z/my-project/my-pi-agent/skills")
SANDBOX = Path("/home/z/my-project/skills")

SKILLS = ["agent-browser", "charts", "pdf", "fullstack-dev", "pptx", "skill-creator",
          "image-edit", "image-generation", "image-search", "video-understand"]

HEAD_RX = re.compile(r"^(#{1,3}) (.+)$", re.M)


def headings(text: str) -> list[str]:
    return [m.group(2).strip() for m in HEAD_RX.finditer(text)]


def norm(h: str) -> str:
    return re.sub(r"\s+", " ", h.strip().lower())


def sections(text: str) -> dict[str, str]:
    """heading -> body text until next heading of same-or-higher level."""
    out = {}
    matches = list(HEAD_RX.finditer(text))
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        out[norm(m.group(2))] = text[start:end]
    return out


for name in SKILLS:
    rp, bp = REPO / name / "SKILL.md", SANDBOX / name / "SKILL.md"
    if not (rp.is_file() and bp.is_file()):
        print(f"== {name}: missing one side, skip")
        continue
    rt = rp.read_text(encoding="utf-8")
    bt = bp.read_text(encoding="utf-8")
    rh, bh = headings(rt), headings(bt)
    rn, bn = {norm(h) for h in rh}, {norm(h) for h in bh}
    sandbox_unique = [h for h in bh if norm(h) not in rn]
    repo_unique = [h for h in rh if norm(h) not in bn]
    print(f"== {name}")
    if sandbox_unique:
        print(f"   sandbox-only sections ({len(sandbox_unique)}):")
        for h in sandbox_unique:
            print(f"     + {h}")
    else:
        print("   sandbox-only sections: none (all sandbox headings exist in repo)")
    if repo_unique and len(repo_unique) <= 15:
        print(f"   repo-only sections ({len(repo_unique)}): " + "; ".join(repo_unique[:15]))
    elif repo_unique:
        print(f"   repo-only sections: {len(repo_unique)} (repo much richer)")
    print()
