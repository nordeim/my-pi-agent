#!/usr/bin/env python3
"""Audit skills/<name>/SKILL.md against the Agent Skills spec and Claude's platform rules.

Scope (each skill must live in its own sub-folder; loose files are ignored):
  Tier 1  skills/<folder>/SKILL.md                      -> indexed
  Tier 2  SKILL.md nested under a grouping folder       -> indexed as bundled sub-skills,
          (a skills/ child with no SKILL.md of its own)    merged by name
  Other   SKILL.md nested inside a valid Tier-1 skill   -> part of that skill; counted only

Spec rules (errors; https://agentskills.io/specification):
  name 1-64 chars, [a-z0-9-], no leading/trailing/double hyphen, equals folder name;
  description 1-1024 chars; compatibility <= 500 chars; metadata is a string->string
  map; allowed-tools is a string.
Claude-surface rules (errors, reported with a distinct reason code):
  no 'anthropic'/'claude' in name; no XML tags in name/description.
Warnings: body > 500 lines, non-third-person description, unknown top-level keys, and
spec deviations that Claude Code accepts (allowed-tools as a YAML list, metadata values
that are not strings).

Usage: python3 tools/skills_audit.py [--root .] [--json out.json]   (needs PyYAML)
Exit: 0 audit completed | 2 usage/IO error.  Findings never change the exit code;
the report is the product.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml

NAME_RX = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
XML_TAG_RX = re.compile(r"</?[A-Za-z][^>]*>")
FRONTMATTER_RX = re.compile(r"\A\ufeff?---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|\Z)(.*)\Z", re.S)
KNOWN_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
RESERVED_WORDS = ("anthropic", "claude")
FIRST_SECOND_PERSON_RX = re.compile(r"^(?:i|i'm|i can|you|you can|your|my|we)\b", re.I)
MAX_NAME, MAX_DESC, MAX_COMPAT, MAX_BODY_LINES = 64, 1024, 500, 500
NEAR_DUP_JACCARD = 0.80  # 5-word shingles of the SKILL.md body
SHINGLE = 5
MIN_BODY_WORDS = 40  # shorter bodies are too small to compare meaningfully


def words(text: str) -> list[str]:
    return re.findall(r"[a-z0-9']+", text.lower())


def shingles(tokens: list[str]) -> set[tuple[str, ...]]:
    if len(tokens) < SHINGLE:
        return {tuple(tokens)} if tokens else set()
    return {tuple(tokens[i:i + SHINGLE]) for i in range(len(tokens) - SHINGLE + 1)}


def jaccard(a: set, b: set) -> float:
    return len(a & b) / len(a | b) if a and b else 0.0


ARTEFACT_DIRS = {"__pycache__", "node_modules", ".pytest_cache"}


def count_files(folder: Path) -> int:
    """Source files only: build artefacts would make the count depend on local runs."""
    return sum(1 for p in folder.rglob("*")
               if p.is_file() and not ARTEFACT_DIRS & set(p.relative_to(folder).parts))


def declared_scalar(frontmatter_text: str, key: str) -> str | None:
    """Raw top-level scalar, so YAML cannot rewrite versions like 1.10 into 1.1."""
    m = re.search(rf"^{key}:[ \t]*(\S.*?)[ \t]*$", frontmatter_text, re.M)
    if not m or m.group(1) in {">", "|", ">-", "|-"}:
        return None
    return m.group(1).strip("\"'")


def scalar_text(value: object) -> str | None:
    return str(value) if isinstance(value, (str, int, float)) and not isinstance(value, bool) else None


def validate_frontmatter(folder: str, fm: object, body: str) -> tuple[list[dict], list[dict]]:
    """Return (errors, warnings); each item is {'code': ..., 'msg': ...}."""
    errors: list[dict] = []
    warnings: list[dict] = []

    def err(code: str, msg: str) -> None:
        errors.append({"code": code, "msg": msg})

    def warn(code: str, msg: str) -> None:
        warnings.append({"code": code, "msg": msg})

    if not isinstance(fm, dict):
        err("FM_NOT_MAPPING", "frontmatter is not a YAML mapping")
        return errors, warnings
    name, desc = fm.get("name"), fm.get("description")
    if not isinstance(name, str) or not name.strip():
        err("NAME_MISSING", "name is missing or not a string")
    else:
        if len(name) > MAX_NAME:
            err("NAME_LENGTH", f"name is {len(name)} chars (max {MAX_NAME})")
        if not NAME_RX.match(name):
            err("NAME_FORMAT", f"name {name!r} must be lowercase letters/digits/single hyphens, "
                               "not starting or ending with a hyphen")
        if name != folder:
            err("NAME_FOLDER_MISMATCH", f"name {name!r} does not match folder {folder!r}")
        lowered = name.lower()
        for word in RESERVED_WORDS:
            if word in lowered:
                err("NAME_RESERVED_WORD", f"name contains reserved word {word!r} "
                                          "(rejected by Claude skill upload)")
        if XML_TAG_RX.search(name):
            err("NAME_XML_TAG", "name contains an XML tag")
    if not isinstance(desc, str) or not desc.strip():
        err("DESC_MISSING", "description is missing, empty or not a string")
    else:
        if len(desc) > MAX_DESC:
            err("DESC_LENGTH", f"description is {len(desc)} chars (max {MAX_DESC})")
        if XML_TAG_RX.search(desc):
            err("DESC_XML_TAG", "description contains an XML tag")
        if FIRST_SECOND_PERSON_RX.match(desc.strip()):
            warn("DESC_PERSON", "description is not written in the third person")
    compat = fm.get("compatibility")
    if compat is not None and (not isinstance(compat, str) or not 1 <= len(compat) <= MAX_COMPAT):
        err("COMPAT_INVALID", f"compatibility must be a string of 1-{MAX_COMPAT} chars")
    meta = fm.get("metadata")
    if meta is not None:
        if not isinstance(meta, dict):
            err("METADATA_INVALID", "metadata must be a mapping")
        elif not all(isinstance(k, str) and isinstance(v, str) for k, v in meta.items()):
            warn("METADATA_NON_STRING", "metadata values are not all strings (spec: string -> string)")
    tools = fm.get("allowed-tools")
    if isinstance(tools, list) and all(isinstance(t, str) for t in tools):
        warn("ALLOWED_TOOLS_LIST", "allowed-tools is a YAML list (spec: space-separated string)")
    elif tools is not None and not isinstance(tools, str):
        err("ALLOWED_TOOLS_INVALID", "allowed-tools must be a space-separated string")
    lic = fm.get("license")
    if lic is not None and not isinstance(lic, str):
        err("LICENSE_INVALID", "license must be a string")
    unknown = sorted(str(k) for k in fm if k not in KNOWN_KEYS)
    if unknown:
        warn("UNKNOWN_KEYS", f"non-spec top-level keys: {', '.join(unknown)}")
    n = len(body.splitlines())
    if n > MAX_BODY_LINES:
        warn("BODY_LENGTH", f"body is {n} lines (recommended max {MAX_BODY_LINES})")
    return errors, warnings


def audit_folder(folder: Path, skills_dir: Path) -> dict:
    record: dict = {"folder": folder.name, "path": f"skills/{folder.relative_to(skills_dir).as_posix()}",
                    "files": count_files(folder)}
    skill_md = folder / "SKILL.md"
    if not skill_md.is_file():
        near = [p.name for p in folder.iterdir() if p.is_file() and p.name.lower() == "skill.md"]
        record["status"] = "no-skill-md"
        record["errors"] = [{"code": "SKILL_MD_CASE" if near else "SKILL_MD_MISSING",
                             "msg": f"found {near[0]!r}; the file must be named SKILL.md" if near
                             else "no top-level SKILL.md"}]
        record["warnings"] = []
        return record
    raw = skill_md.read_bytes()
    record["sha256"] = hashlib.sha256(raw).hexdigest()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        record.update(status="invalid", errors=[{"code": "ENCODING", "msg": str(exc)}], warnings=[])
        return record
    m = FRONTMATTER_RX.match(text)
    if not m:
        record.update(status="invalid", warnings=[],
                      errors=[{"code": "FM_MISSING", "msg": "no YAML frontmatter delimited by ---"}])
        return record
    try:
        fm = yaml.safe_load(m.group(1))
    except yaml.YAMLError as exc:
        first = str(exc).splitlines()[0] if str(exc) else "YAML error"
        record.update(status="invalid", warnings=[],
                      errors=[{"code": "FM_YAML", "msg": f"frontmatter does not parse: {first}"}])
        return record
    body = m.group(2)
    errors, warnings = validate_frontmatter(folder.name, fm, body)
    meta = fm.get("metadata") if isinstance(fm, dict) and isinstance(fm.get("metadata"), dict) else {}
    fm = fm if isinstance(fm, dict) else {}
    desc = fm.get("description") if isinstance(fm.get("description"), str) else ""
    h1 = re.search(r"^#\s+(.+?)\s*$", body, re.M)
    record.update(
        name=fm.get("name") if isinstance(fm.get("name"), str) else None,
        description=" ".join(desc.split()),
        title=h1.group(1) if h1 else folder.name,
        license=fm.get("license") if isinstance(fm.get("license"), str) else None,
        version=declared_scalar(m.group(1), "version") or scalar_text(meta.get("version")),
        author=declared_scalar(m.group(1), "author") or scalar_text(meta.get("author")),
        body_lines=len(body.splitlines()),
        body_tokens=words(body),
        structure=sorted(d.name for d in folder.iterdir()
                         if d.is_dir() and d.name in {"scripts", "references", "assets", "scenes",
                                                      "routes", "engines", "templates", "examples"}),
        nested_skill_md=sum(1 for p in folder.rglob("SKILL.md") if p != skill_md),
        errors=errors, warnings=warnings,
        status="invalid" if errors else ("valid-with-warnings" if warnings else "valid"),
    )
    return record


def find_duplicates(valid: list[dict]) -> dict:
    """Same-name groups (any tier) and cross-name content duplicates (Tier 1)."""
    def sig_of(r: dict) -> set:
        return shingles(r["body_tokens"])

    by_name: dict[str, list[dict]] = defaultdict(list)
    for r in valid:
        by_name[r["name"]].append(r)
    same_name = []
    for n, g in sorted(by_name.items()):
        if len(g) < 2:
            continue
        hashes = {r["sha256"] for r in g}
        sigs = [sig_of(r) for r in g]
        low = min((jaccard(a, b) for a, b in itertools.combinations(sigs, 2)), default=1.0)
        if len(hashes) == 1:
            verdict = "identical"
        elif low >= NEAR_DUP_JACCARD:
            verdict = "near-identical"
        else:
            verdict = "divergent"
        same_name.append({"name": n, "verdict": verdict, "min_body_jaccard": round(low, 3),
                          "locations": sorted(r["path"] for r in g)})

    tier1 = [r for r in valid if r["tier"] == 1 and len(r["body_tokens"]) >= MIN_BODY_WORDS]
    sig = {r["folder"]: sig_of(r) for r in tier1}
    desc_sig = {r["folder"]: shingles(words(r["description"])) for r in tier1}
    by_hash: dict[str, list[str]] = defaultdict(list)
    for r in tier1:
        by_hash[r["sha256"]].append(r["folder"])
    identical = sorted(sorted(g) for g in by_hash.values() if len(g) > 1)
    seen = {frozenset(p) for g in identical for p in itertools.combinations(g, 2)}
    near = []
    for a, b in itertools.combinations(sorted(sig), 2):
        if frozenset((a, b)) in seen:
            continue
        score = jaccard(sig[a], sig[b])
        if score >= NEAR_DUP_JACCARD:
            near.append({"folders": [a, b], "body_jaccard": round(score, 3),
                         "description_jaccard": round(jaccard(desc_sig[a], desc_sig[b]), 3)})
    return {"same_name": same_name, "identical_content_tier1": identical,
            "near_identical_content_tier1": near}


def run(root: Path) -> dict:
    skills_dir = root / "skills"
    if not skills_dir.is_dir():
        raise FileNotFoundError(f"no skills/ directory under {root}")
    children = sorted(p for p in skills_dir.iterdir() if p.is_dir() and not p.name.startswith("."))
    tier1 = [dict(audit_folder(f, skills_dir), tier=1) for f in children]
    grouping = {r["folder"] for r in tier1 if r["status"] == "no-skill-md"}
    tier2 = []
    for g in sorted(grouping):
        for md in sorted((skills_dir / g).rglob("SKILL.md")):
            rec = audit_folder(md.parent, skills_dir)
            rec["tier"], rec["container"] = 2, g
            tier2.append(rec)
    valid_status = {"valid", "valid-with-warnings"}
    valid = [r for r in tier1 + tier2 if r["status"] in valid_status]
    inside_valid = sum(1 for r in tier1 if r["status"] in valid_status for _ in
                       [p for p in (skills_dir / r["folder"]).rglob("SKILL.md")
                        if p.parent != skills_dir / r["folder"]])
    t1 = [r for r in tier1 if r["status"] != "no-skill-md"]
    return {
        "summary": {
            "top_level_folders_scanned": len(tier1),
            "tier1_with_skill_md": len(t1),
            "tier1_valid": sum(r["status"] in valid_status for r in t1),
            "tier1_valid_with_warnings": sum(r["status"] == "valid-with-warnings" for r in t1),
            "tier1_invalid": sum(r["status"] == "invalid" for r in t1),
            "grouping_folders_without_skill_md": len(grouping),
            "tier2_skill_md_files": len(tier2),
            "tier2_valid": sum(r["status"] in valid_status for r in tier2),
            "tier2_unique_valid_names": len({r["name"] for r in tier2 if r["status"] in valid_status}),
            "tier2_invalid": sum(r["status"] == "invalid" for r in tier2),
            "skill_md_inside_valid_tier1_skills_not_indexed": inside_valid,
        },
        "records": tier1 + tier2,
        "duplicates": find_duplicates(valid),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--json", help="write the full report here (overwrites)")
    args = ap.parse_args()
    try:
        report = run(Path(args.root).resolve())
    except (OSError, FileNotFoundError) as exc:
        print(f"CONFIG ERROR: {exc}", file=sys.stderr)
        return 2
    for r in report["records"]:
        r.pop("body_tokens", None)
    if args.json:
        Path(args.json).write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n",
                                   encoding="utf-8")
    print(json.dumps(report["summary"], indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
