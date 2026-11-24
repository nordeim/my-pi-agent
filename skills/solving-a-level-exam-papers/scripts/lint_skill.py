#!/usr/bin/env python3
"""Validate an Agent Skill directory: frontmatter, size, and local links.

Usage: python scripts/lint_skill.py path/to/skill-dir
"""
from __future__ import annotations
import pathlib, re, sys

NAME_RX = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

def main() -> None:
    root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    md = root / "SKILL.md"
    errs: list[str] = []
    if not md.is_file():
        sys.exit("FAIL: SKILL.md not found")
    text = md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        sys.exit("FAIL: missing YAML frontmatter")
    fm = text.split("---", 2)[1]
    body = text.split("---", 2)[2]
    name = re.search(r"^name:\s*(.+)$", fm, re.M)
    desc = re.search(r"^description:\s*(.+)$", fm, re.M)
    if not name or not NAME_RX.match(name.group(1).strip()):
        errs.append("name missing or not lowercase-hyphen")
    elif len(name.group(1).strip()) > 64:
        errs.append("name exceeds 64 characters")
    elif name.group(1).strip() != root.resolve().name:
        errs.append("name does not match directory name")
    if not desc:
        errs.append("description missing")
    elif len(desc.group(1).strip()) > 1024:
        errs.append("description exceeds 1024 characters")
    n = len(body.splitlines())
    if n > 500:
        errs.append(f"body is {n} lines (>500): move detail into references/")
    for link in re.findall(r"\]\(([^)]+)\)", body):
        if link.startswith(("http://", "https://")):
            continue
        if not (root / link).exists():
            errs.append(f"broken local link: {link}")
    print(f"SKILL.md body: {n} lines")
    if errs:
        print("FAIL:"); [print("  -", e) for e in errs]; sys.exit(1)
    print("PASS: structure and frontmatter valid")

if __name__ == "__main__":
    main()
