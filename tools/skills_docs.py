#!/usr/bin/env python3
"""Regenerate skills/skills-catalog.md, skills-inventory.md and docs/skills-inventory.md.

Source of truth: tools/skills_audit.py (live scan of skills/), tools/skills_categories.json
(category per skill; skills missing from it appear under "Uncategorised"), and
tools/skills_curated_duplicates.md (hand-written overlap notes, embedded verbatim).

Usage: python3 tools/skills_docs.py [--root .] [--date YYYY-MM-DD]     (needs PyYAML)
Exit: 0 written | 2 usage/IO error.
"""
from __future__ import annotations

import argparse
import datetime
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import skills_audit  # noqa: E402

VALID = {"valid", "valid-with-warnings"}
FIX_HINTS = {
    "NAME_RESERVED_WORD": "rename the folder and `name` (drop the reserved word) before uploading to Claude",
    "DESC_XML_TAG": "remove angle-bracket tags from `description` (use plain words or backticks)",
    "COMPAT_INVALID": "shorten `compatibility` to <= 500 characters",
    "NAME_FOLDER_MISMATCH": "make `name` equal the folder name",
}


def cell(text: str) -> str:
    return " ".join(text.split()).replace("|", "\\|")


def load_categories(root: Path) -> tuple[dict[int, str], dict[int, str], dict[str, int]]:
    data = json.loads((root / "tools" / "skills_categories.json").read_text(encoding="utf-8"))
    return ({int(k): v for k, v in data["categories"].items()},
            {int(k): v for k, v in data["blurbs"].items()}, data["skills"])


def anchor(title: str) -> str:
    keep = "".join(c if c.isalnum() or c in " -" else "" for c in title.lower())
    return keep.replace(" ", "-")


def loose_files(skills_dir: Path) -> list[str]:
    return sorted(p.name for p in skills_dir.iterdir() if p.is_file())


def duplicate_block(report: dict, heading: str, curated: str) -> list[str]:
    dup = report["duplicates"]
    same = dup["same_name"]
    by = Counter(x["verdict"] for x in same)
    out = [f"{heading} Duplicating skills", "",
           "> **Detected automatically** by `tools/skills_audit.py`; two skills are *duplicates* when "
           "they share a `name` and an essentially identical `SKILL.md` body (5-word-shingle "
           f"Jaccard >= {skills_audit.NEAR_DUP_JACCARD}). No folder was deleted; entries are merged "
           "in this document only.", ""]
    out += [f"**Same name, different folders: {len(same)} names** "
            f"({by['identical']} byte-identical, {by['near-identical']} near-identical, "
            f"{by['divergent']} divergent).", "",
            "| Skill name | Verdict | Copies | Locations |", "|---|---|---|---|"]
    for x in same:
        flag = {"identical": "DUPLICATE (identical)", "near-identical": "DUPLICATE (near-identical)",
                "divergent": "NAME COLLISION - content differs; do not merge"}[x["verdict"]]
        locs = "<br>".join(f"`{p}`" for p in x["locations"])
        out.append(f"| `{x['name']}` | {flag} | {len(x['locations'])} | {locs} |")
    out += ["", "**Different names, essentially the same content (top-level skills):**", "",
            "| Skills | Body similarity | Note |", "|---|---|---|"]
    notes = {("pdf", "pdf-old-20260806"): "archived dated snapshot of `pdf`; prefer `pdf`",
             ("skill-creator", "skill-creator-zai"): "same scope and content; keep one",
             ("greploop", "greploop-apps"): "per its description, `greploop-apps` is identical except it tags "
                                           "`@greptile-apps` (bypasses the file-count limit on huge PRs)"}
    for x in dup["near_identical_content_tier1"]:
        a, b = x["folders"]
        out.append(f"| `{a}` ↔ `{b}` | {x['body_jaccard']:.1%} | {notes.get((a, b), 'review and consolidate')} |")
    if not dup["near_identical_content_tier1"]:
        out.append("| _none_ | | |")
    out += ["", f"{curated.strip()}", ""]
    return out


def bundled_section(report: dict, heading: str) -> list[str]:
    tier2 = [r for r in report["records"] if r["tier"] == 2 and r["status"] in VALID]
    groups: dict[str, list[dict]] = defaultdict(list)
    for r in tier2:
        groups[r["name"]].append(r)
    dup_names = {x["name"]: x["verdict"] for x in report["duplicates"]["same_name"]}
    out = [f"{heading} Bundled sub-skills (merged by name)", "",
           f"{len(tier2)} valid `SKILL.md` files sit inside grouping folders (agent bundles with no "
           f"`SKILL.md` of their own). Merged by `name` they are **{len(groups)} unique skills**; "
           "each row lists every bundle that carries a copy.", "",
           "| Sub-skill | Copies | Found in bundles | Merge verdict | Description |", "|---|---|---|---|---|"]
    for name in sorted(groups):
        g = groups[name]
        verdict = dup_names.get(name, "unique")
        verdict = {"identical": "DUPLICATE - merged", "near-identical": "DUPLICATE - merged",
                   "divergent": "COLLISION - kept separate", "unique": "unique"}[verdict]
        bundles = ", ".join(f"`{r['container']}`" for r in sorted(g, key=lambda r: r["container"]))
        out.append(f"| `{name}` | {len(g)} | {bundles} | {verdict} | {cell(g[0]['description'])} |")
    out.append("")
    return out


def exclusions_section(report: dict, skills_dir: Path, heading: str) -> list[str]:
    s = report["summary"]
    t1_bad = [r for r in report["records"] if r["tier"] == 1 and r["status"] == "invalid"]
    t2_bad = [r for r in report["records"] if r["tier"] == 2 and r["status"] == "invalid"]
    grouping = sorted(r["folder"] for r in report["records"] if r["status"] == "no-skill-md")
    warn = Counter(w["code"] for r in report["records"] if r["tier"] == 1 and r["status"] in VALID
                   for w in r["warnings"])
    out = [f"{heading} Validation & exclusions", "",
           "A folder is indexed only if `skills/<folder>/SKILL.md` exists and passes both rule sets "
           "audited by `tools/skills_audit.py`:", "",
           "- **Agent Skills specification** (<https://agentskills.io/specification>): `name` 1-64 chars, "
           "lowercase letters/digits/single hyphens, not starting or ending with a hyphen, equal to the "
           "folder name; `description` 1-1024 chars; `compatibility` <= 500 chars; well-formed YAML frontmatter.",
           "- **Claude platform rules**: no `anthropic`/`claude` in `name`; no XML tags in `name` or "
           "`description`.", "",
           "Spec deviations that Claude Code accepts are *warnings*, not exclusions "
           "(YAML-list `allowed-tools`, non-string `metadata` values, non-spec top-level keys such as "
           "`author`/`version`, bodies over 500 lines). Warning counts across indexed skills: "
           + (", ".join(f"`{k}` x{v}" for k, v in sorted(warn.items())) or "none") + ".", "",
           f"Result: **{s['tier1_valid']} valid top-level skills** of {s['tier1_with_skill_md']} folders with a "
           f"`SKILL.md`; {s['tier1_invalid']} excluded; {s['grouping_folders_without_skill_md']} grouping "
           f"folders; {s['skill_md_inside_valid_tier1_skills_not_indexed']} nested `SKILL.md` files inside "
           "valid skills are parts of those skills and are not indexed separately.", "",
           f"### Excluded: top-level folders with an invalid `SKILL.md` ({len(t1_bad)})", "",
           "| Folder | Rule broken | Detail | Suggested fix |", "|---|---|---|---|"]
    for r in t1_bad:
        for e in r["errors"]:
            out.append(f"| `{r['folder']}` | `{e['code']}` | {cell(e['msg'])} | {FIX_HINTS.get(e['code'], 'fix frontmatter')} |")
    out += ["", "These were **not modified**; fixing them is a separate, reviewable change.", ""]
    if t2_bad:
        out += [f"### Excluded: invalid bundled sub-skills ({len(t2_bad)})", "",
                "| Path | Rule broken | Detail |", "|---|---|---|"]
        for r in t2_bad:
            for e in r["errors"]:
                out.append(f"| `{r['path']}` | `{e['code']}` | {cell(e['msg'])} |")
        out.append("")
    out += [f"### Grouping folders without a top-level `SKILL.md` ({len(grouping)})", "",
            ", ".join(f"`{g}`" for g in grouping) + ".", "",
            "### Loose files in `skills/` (not skills: no sub-folder)", "",
            ", ".join(f"`{f}`" for f in loose_files(skills_dir)) + ".", ""]
    return out


def catalog(report: dict, root: Path, date: str, curated: str) -> str:
    titles, blurbs, cat_of = load_categories(root)
    t1 = [r for r in report["records"] if r["tier"] == 1 and r["status"] in VALID]
    s = report["summary"]
    by_cat: dict[int, list[dict]] = defaultdict(list)
    for r in t1:
        by_cat[cat_of.get(r["folder"], 0)].append(r)
    out = ["# Skills Catalog", "",
           f"> **{len(t1)} valid skills** in {len(titles)} categories, plus "
           f"{len({r['name'] for r in report['records'] if r['tier'] == 2 and r['status'] in VALID})} "
           "unique bundled sub-skills. Regenerated on "
           f"{date} by `tools/skills_docs.py`; only folders under `skills/` whose own `SKILL.md` passes "
           "the Agent Skills spec and Claude's platform rules are listed "
           "(see [Validation & exclusions](#validation--exclusions)).", "", "---", ""]
    for n in sorted(titles):
        out += [f"## {n}. {titles[n]}", "", f"> {blurbs.get(n, '')}", "", "| Skill | Description |", "|-------|-------------|"]
        out += [f"| **{r['folder']}** | {cell(r['description'])} |"
                for r in sorted(by_cat[n], key=lambda r: r["folder"])]
        out += [""]
    if by_cat.get(0):
        out += ["## Uncategorised", "", "> Valid skills not yet assigned in `tools/skills_categories.json`.", "",
                "| Skill | Description |", "|-------|-------------|"]
        out += [f"| **{r['folder']}** | {cell(r['description'])} |" for r in sorted(by_cat[0], key=lambda r: r["folder"])]
        out.append("")
    out += ["---", ""] + duplicate_block(report, "##", curated) + ["---", ""]
    out += bundled_section(report, "##") + ["---", ""]
    out += exclusions_section(report, root / "skills", "##") + ["---", "",
            "## How to Use This Catalog", "",
            "1. Identify the category that matches your task.",
            "2. Scan the skill names in that category - the description tells you when to use each one.",
            "3. Open `skills/<skill-name>/SKILL.md` for the full workflow.",
            "4. Most skills also ship `scripts/`, `references/`, `scenes/`, `routes/`, or `engines/` "
            "subdirectories - the SKILL.md will tell you which to load.",
            "5. For per-skill file counts, structure and licences see [`skills-inventory.md`](../skills-inventory.md).",
            "6. Regenerate: `python3 tools/skills_audit.py --json /tmp/audit.json && python3 tools/skills_docs.py`."]
    return "\n".join(out) + "\n"


def inventory(report: dict, root: Path, date: str, curated: str, link_prefix: str) -> str:
    titles, _, cat_of = load_categories(root)
    t1 = [r for r in report["records"] if r["tier"] == 1 and r["status"] in VALID]
    s = report["summary"]
    by_cat: dict[int, list[dict]] = defaultdict(list)
    for r in t1:
        by_cat[cat_of.get(r["folder"], 0)].append(r)
    out = ["# Skills Inventory — my-pi-agent", "",
           f"> Generated {date} by `tools/skills_docs.py` from a live scan (`tools/skills_audit.py`). "
           "**Consistent with `skills/skills-catalog.md`.**",
           f"> **{len(t1)} valid skills** (each in its own folder with a spec- and Claude-compliant "
           f"`SKILL.md`), {s['tier2_unique_valid_names']} unique bundled sub-skills merged from "
           f"{s['tier2_valid']} copies, {s['tier1_invalid']} excluded folders.", "", "---", "",
           "## How to read this inventory", "",
           "- **Path / SKILL.md** — location of the skill folder and its manifest",
           "- **Title** — first H1 in `SKILL.md` (falls back to the folder name)",
           "- **Files** — total files in the skill folder (recursive)",
           "- **Structure** — standard sub-directories present (`flat` when none)",
           "- **Flags** — validator warnings that do not exclude the skill (see Validation & exclusions)",
           "- **Duplicate** — a top-level skill whose body is essentially identical to another", "",
           "## Category Index", ""]
    for n in sorted(titles):
        out.append(f"{n}. **{titles[n]}** — {len(by_cat[n])} skills — [jump](#{n}-{anchor(titles[n])})")
    if by_cat.get(0):
        out.append(f"{len(titles) + 1}. **Uncategorised** — {len(by_cat[0])} skills")
    out += ["", "---", ""]
    dup_pairs: dict[str, str] = {}
    for x in report["duplicates"]["near_identical_content_tier1"]:
        a, b = x["folders"]
        dup_pairs[a], dup_pairs[b] = b, a
    for n in sorted(titles) + ([0] if by_cat.get(0) else []):
        title = titles.get(n, "Uncategorised")
        out += [f"## {n}. {title}" if n else f"## {title}", "", f"> **{len(by_cat[n])} skills** in this category.", ""]
        for r in sorted(by_cat[n], key=lambda r: r["folder"]):
            md = f"{link_prefix}{r['path']}/SKILL.md"
            out += [f"### `{r['folder']}`", "", f"- **Path**: `{r['path']}`",
                    f"- **SKILL.md**: [`{r['path']}/SKILL.md`]({md})", f"- **Title**: {cell(r['title'])}",
                    f"- **Files**: {r['files']}", f"- **Structure**: {', '.join(r['structure']) or 'flat'}"]
            if r.get("license"):
                out.append(f"- **License**: {cell(r['license'])}")
            if r.get("author"):
                out.append(f"- **Author**: {cell(r['author'])}")
            if r.get("version"):
                out.append(f"- **Version**: {cell(r['version'])}")
            if r["warnings"]:
                out.append("- **Flags**: " + ", ".join(f"`{w['code']}`" for w in r["warnings"]))
            if r["folder"] in dup_pairs:
                out.append(f"- **Duplicate**: essentially identical to `{dup_pairs[r['folder']]}`")
            out += ["", f"> {cell(r['description'])}", ""]
    out += ["---", ""] + duplicate_block(report, "##", curated) + ["---", ""]
    out += bundled_section(report, "##") + ["---", ""]
    out += exclusions_section(report, root / "skills", "##")
    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    args = ap.parse_args()
    root = Path(args.root).resolve()
    try:
        report = skills_audit.run(root)
        curated = (root / "tools" / "skills_curated_duplicates.md").read_text(encoding="utf-8")
        heading_fix = curated.replace("## Duplicates & Obsolete Skills", "### Curated overlap notes", 1)
        heading_fix = heading_fix.replace("\n### Obsolete", "\n#### Obsolete").replace(
            "\n### Direct near-duplicates", "\n#### Direct near-duplicates").replace(
            "\n### Overlapping families", "\n#### Overlapping families")
        # Byte-identical copies (tests/test_repo_consistency.py); "/"-rooted links resolve from both.
        inv = inventory(report, root, args.date, heading_fix, "/")
        outputs = {
            root / "skills" / "skills-catalog.md": catalog(report, root, args.date, heading_fix),
            root / "skills-inventory.md": inv,
            root / "docs" / "skills-inventory.md": inv,
        }
        for path, text in outputs.items():
            path.write_text(text, encoding="utf-8")
    except (OSError, KeyError, json.JSONDecodeError) as exc:
        print(f"CONFIG ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(report["summary"], indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
