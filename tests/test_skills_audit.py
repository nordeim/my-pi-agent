"""Tests for tools/skills_audit.py (spec + Claude-rule validation, tiers, duplicates)."""
import sys
from pathlib import Path

import pytest

yaml = pytest.importorskip("yaml")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import skills_audit  # noqa: E402

BODY = " ".join(f"word{i}" for i in range(80))


def write_skill(root: Path, rel: str, frontmatter: str, body: str = BODY) -> None:
    folder = root / "skills" / rel
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "SKILL.md").write_text(f"---\n{frontmatter}\n---\n\n# Title\n\n{body}\n", encoding="utf-8")


def record(report: dict, folder: str, tier: int = 1) -> dict:
    return next(r for r in report["records"] if r["folder"] == folder and r["tier"] == tier)


def codes(rec: dict) -> set[str]:
    return {e["code"] for e in rec["errors"]}


def test_valid_skill_is_valid(tmp_path):
    write_skill(tmp_path, "good-skill", "name: good-skill\ndescription: Does a thing. Use when asked.")
    rec = record(skills_audit.run(tmp_path), "good-skill")
    assert rec["status"] == "valid" and rec["errors"] == []


@pytest.mark.parametrize("name,expected", [
    ("Bad_Name", "NAME_FORMAT"), ("-lead", "NAME_FORMAT"), ("dou--ble", "NAME_FORMAT"),
    ("other-name", "NAME_FOLDER_MISMATCH"), ("x" * 65, "NAME_LENGTH"),
])
def test_name_rules(tmp_path, name, expected):
    write_skill(tmp_path, "folder-x", f"name: {name}\ndescription: ok")
    assert expected in codes(record(skills_audit.run(tmp_path), "folder-x"))


def test_claude_reserved_words_are_rejected(tmp_path):
    write_skill(tmp_path, "claude-helper", "name: claude-helper\ndescription: ok")
    rec = record(skills_audit.run(tmp_path), "claude-helper")
    assert rec["status"] == "invalid" and "NAME_RESERVED_WORD" in codes(rec)


@pytest.mark.parametrize("fm,expected", [
    ("name: d\ndescription: uses <script setup> tags", "DESC_XML_TAG"),
    ("name: d\ndescription: ''", "DESC_MISSING"),
    ("name: d", "DESC_MISSING"),
    ("name: d\ndescription: " + "a" * 1025, "DESC_LENGTH"),
    ("name: d\ndescription: ok\ncompatibility: " + "c" * 501, "COMPAT_INVALID"),
    ("name: d\ndescription: ok\nmetadata: [1, 2]", "METADATA_INVALID"),
])
def test_frontmatter_rules(tmp_path, fm, expected):
    write_skill(tmp_path, "d", fm)
    assert expected in codes(record(skills_audit.run(tmp_path), "d"))


def test_unparseable_yaml_and_missing_frontmatter(tmp_path):
    write_skill(tmp_path, "badyaml", "name: [unclosed\ndescription: x")
    (tmp_path / "skills" / "nofm").mkdir()
    (tmp_path / "skills" / "nofm" / "SKILL.md").write_text("# no frontmatter\n", encoding="utf-8")
    report = skills_audit.run(tmp_path)
    assert "FM_YAML" in codes(record(report, "badyaml"))
    assert "FM_MISSING" in codes(record(report, "nofm"))


def test_spec_deviations_accepted_by_claude_code_are_warnings(tmp_path):
    write_skill(tmp_path, "w", "name: w\ndescription: ok\nallowed-tools:\n  - Read\n  - Bash\n"
                               "metadata:\n  version: 1.0\nauthor: someone")
    rec = record(skills_audit.run(tmp_path), "w")
    assert rec["status"] == "valid-with-warnings"
    assert {"ALLOWED_TOOLS_LIST", "METADATA_NON_STRING", "UNKNOWN_KEYS"} <= {w["code"] for w in rec["warnings"]}


def test_folder_without_skill_md_is_grouping_and_wrongly_cased_file_is_reported(tmp_path):
    (tmp_path / "skills" / "group").mkdir(parents=True)
    (tmp_path / "skills" / "lower").mkdir()
    (tmp_path / "skills" / "lower" / "skill.md").write_text("x", encoding="utf-8")
    (tmp_path / "skills" / "loose.md").write_text("not a skill", encoding="utf-8")
    report = skills_audit.run(tmp_path)
    assert record(report, "group")["status"] == "no-skill-md"
    assert "SKILL_MD_CASE" in codes(record(report, "lower"))
    assert report["summary"]["tier1_valid"] == 0  # the loose file is never counted


def test_bundled_same_name_identical_copies_are_merged_and_flagged(tmp_path):
    fm = "name: shared\ndescription: shared sub-skill"
    for bundle in ("bundle-a", "bundle-b"):
        write_skill(tmp_path, f"{bundle}/skills/shared", fm)
    report = skills_audit.run(tmp_path)
    assert report["summary"]["tier2_valid"] == 2 and report["summary"]["tier2_unique_valid_names"] == 1
    (group,) = report["duplicates"]["same_name"]
    assert group["name"] == "shared" and group["verdict"] == "identical" and len(group["locations"]) == 2


def test_same_name_different_content_is_a_collision_not_a_duplicate(tmp_path):
    other = " ".join(f"other{i}" for i in range(80))
    write_skill(tmp_path, "dup", "name: dup\ndescription: top-level")
    write_skill(tmp_path, "bundle/skills/dup", "name: dup\ndescription: nested", body=other)
    (group,) = skills_audit.run(tmp_path)["duplicates"]["same_name"]
    assert group["verdict"] == "divergent"


def test_near_identical_top_level_skills_across_names(tmp_path):
    write_skill(tmp_path, "alpha", "name: alpha\ndescription: first")
    write_skill(tmp_path, "beta", "name: beta\ndescription: second")
    near = skills_audit.run(tmp_path)["duplicates"]["near_identical_content_tier1"]
    assert near and near[0]["folders"] == ["alpha", "beta"]


def test_skill_md_inside_a_valid_skill_is_not_indexed_separately(tmp_path):
    write_skill(tmp_path, "parent", "name: parent\ndescription: ok")
    write_skill(tmp_path, "parent/templates/inner", "name: inner\ndescription: part of parent")
    summary = skills_audit.run(tmp_path)["summary"]
    assert summary["tier1_valid"] == 1 and summary["tier2_valid"] == 0
    assert summary["skill_md_inside_valid_tier1_skills_not_indexed"] == 1


def test_missing_skills_dir_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        skills_audit.run(tmp_path)
