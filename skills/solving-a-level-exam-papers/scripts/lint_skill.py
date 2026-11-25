#!/usr/bin/env python3
"""Validate skill structure, frontmatter, referenced paths, and script safety patterns."""
from __future__ import annotations
import ast, re, sys
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
# Executable constructs only: mentions inside strings or comments are inert, so no
# script (including this one) needs an exemption.
BANNED_NAMES = {"eval", "exec", "__import__", "sympify", "parse_expr"}
BANNED_ATTRS = {"sympify", "parse_expr"}
PACKAGE_DIRS = "references|assets|scripts|tests|samples|docs"
PATH_RX = re.compile(rf"(?<![\w/.-])((?:{PACKAGE_DIRS})/[\w./{{}},-]*)")
BRACE_RX = re.compile(r"\{([^{}]*)\}")


def expand_braces(path: str) -> list[str]:
    m = BRACE_RX.search(path)
    if not m:
        return [path]
    return [alt for opt in m.group(1).split(",")
            for alt in expand_braces(path[:m.start()] + opt + path[m.end():])]


TREE_RX = re.compile(r"^[├└]── (\S+)$", re.M)


def referenced_paths(body: str) -> list[str]:
    """Package-relative paths named in prose, code spans and the file tree."""
    found = []
    for raw in PATH_RX.findall(body) + TREE_RX.findall(body):
        found += [p.rstrip(".,/") for p in expand_braces(raw)]
    return sorted(set(found))


def tree_paths(body: str) -> set[str]:
    return {p.rstrip(".,/") for raw in TREE_RX.findall(body)
            for p in expand_braces(raw)}


def unsafe_constructs(source: str) -> list[str]:
    hits = []
    for node in ast.walk(ast.parse(source)):
        line = getattr(node, "lineno", 0)
        if isinstance(node, ast.Name) and node.id in BANNED_NAMES:
            hits.append(f"{node.id} (line {line})")
        elif isinstance(node, ast.alias) and node.name in BANNED_NAMES:
            hits.append(f"import {node.name}")
        elif isinstance(node, ast.Attribute):
            owner = node.value.id if isinstance(node.value, ast.Name) else ""
            if node.attr in BANNED_ATTRS or (owner == "os" and node.attr == "system"):
                hits.append(f"{owner + '.' if owner else ''}{node.attr} (line {line})")
        elif (isinstance(node, ast.keyword) and node.arg == "shell"
              and isinstance(node.value, ast.Constant) and node.value.value is True):
            hits.append("shell=True")
    return hits


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
        target = link.split("#", 1)[0]
        if target and not link.startswith(("http://", "https://")) and not (root / target).exists():
            errs.append(f"broken local link: {link}")
    for rel in referenced_paths(body):
        if not (root / rel).exists():
            errs.append(f"broken referenced path: {rel}")
    listed = tree_paths(body)
    for dirname in PACKAGE_DIRS.split("|"):
        base = root / dirname
        if not base.is_dir():
            continue
        for path in base.rglob("*"):
            if not path.is_file():
                continue
            rel = path.relative_to(root)
            if any(part.startswith((".", "__")) for part in rel.parts):
                continue
            rel_str = rel.as_posix()
            if rel_str not in listed:
                errs.append(f"unlisted package file: {rel_str}")
    for rel in REQUIRED:
        if not (root / rel).exists():
            errs.append(f"missing required file: {rel}")
    for script in sorted((root / "scripts").glob("*.py")):
        try:
            hits = unsafe_constructs(script.read_text(encoding="utf-8"))
        except SyntaxError as exc:
            errs.append(f"scripts/{script.name} does not parse: {exc.msg} (line {exc.lineno})")
            continue
        errs += [f"unsafe pattern {hit} in scripts/{script.name}" for hit in hits]
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
    print("PASS: structure, frontmatter, referenced paths, template and script-safety checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
