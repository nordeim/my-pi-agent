#!/usr/bin/env python3
"""Validate skill structure, frontmatter, links, and script safety patterns."""
from __future__ import annotations
import re, sys
from pathlib import Path

NAME_RX = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
REQUIRED = [
    "references/source-fidelity.md", "references/exam-presentation.md",
    "references/verification-playbook.md", "references/pitfalls-and-lessons.md",
    "references/tool-safety.md", "assets/solution-template.md",
    "assets/audit-template.md", "assets/checks.example.json",
    "scripts/safe_expr.py", "scripts/check_math.py",
    "scripts/extract_pdf.py", "scripts/lint_skill.py",
]
BANNED = ["sympify(", "parse_expr(", "eval(", "exec(", "__import__(",
          "os.system(", "shell=True"]
ALLOWED_BANNED = {"safe_expr.py"}  # interpreter module: contains none of these
SELF = Path(__file__).resolve()


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    md = root / "SKILL.md"
    errs: list[str] = []
    if not md.is_file():
        print("FAIL: SKILL.md not found")
        return 1
    text = md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        print("FAIL: missing YAML frontmatter")
        return 1
    _, fm, body = text.split("---", 2)
    name = re.search(r"^name:\s*(.+)$", fm, re.M)
    desc = re.search(r"^description:\s*(.+)$", fm, re.M)
    if not name or not NAME_RX.match(name.group(1).strip()):
        errs.append("name missing or not lowercase-hyphen")
    else:
        if len(name.group(1).strip()) > 64:
            errs.append("name exceeds 64 characters")
        if name.group(1).strip() != root.name:
            errs.append("name does not match directory name")
    if not desc:
        errs.append("description missing")
    elif len(desc.group(1).strip()) > 1024:
        errs.append("description exceeds 1024 characters")
    n = len(body.splitlines())
    if n > 500:
        errs.append(f"body is {n} lines (>500): move detail into references/")
    for link in re.findall(r"\]\(([^)]+)\)", body):
        if not link.startswith(("http://", "https://")) and not (root / link).exists():
            errs.append(f"broken local link: {link}")
    for rel in REQUIRED:
        if not (root / rel).exists():
            errs.append(f"missing required file: {rel}")
    for script in (root / "scripts").glob("*.py"):
        if script.name in ALLOWED_BANNED or script.resolve() == SELF:
            continue
        src = script.read_text(encoding="utf-8")
        for token in BANNED:
            if token in src:
                errs.append(f"unsafe pattern {token!r} in scripts/{script.name}")
    tmpl = root / "assets" / "solution-template.md"
    if tmpl.exists():
        t = tmpl.read_text(encoding="utf-8").lower()
        for token in ("cover", "verification ledger", "handoff"):
            if token not in t:
                errs.append(f"solution-template.md missing mandatory section: {token}")
    skill = text.lower()
    if "explicit authorisation" not in skill and "explicit authorization" not in skill:
        errs.append("SKILL.md must gate git delivery on explicit authorisation")
    if not list((root / "tests").glob("test_*.py")):
        errs.append("no regression tests found in tests/")
    print(f"SKILL.md body: {n} lines")
    if errs:
        print("FAIL:")
        for e in errs:
            print("  -", e)
        return 1
    print("PASS: structure, frontmatter, links, template and script-safety checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
