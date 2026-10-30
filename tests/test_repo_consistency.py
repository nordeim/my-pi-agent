"""Repository-level consistency tests for the three big-tech research skills.

Guards the cross-skill regressions recorded in docs/skills-audit/:

  H-1  conflicting restatements of the canonical worked example
       (Alphabet Q3 2026, GOOG class) across the skill family
  H-2  disclaimer presence in every family skill
  M-2  attribution-doctrine parity (ordinal ranks by default; quantified
       allocations only as labeled Reasoned signed allocations)
  M-3  confidence-taxonomy parity (Verified / Reasoned / Assumed / Unverifiable)
  M-6  catalog registration of all three skills
  L-1  frontmatter sanity (name matches folder; description within the
       1024-character skill-spec limit; semver version)

Plus the round-2 remediation guards (validated against
docs/comparative_analysis_report-3/4/5.md):

  R3-C1/R4-2/R5-H1  lite audit gates vendored into skills 2 and 3
  R4-5              verification-status line + valuation boundary everywhere
  R3-synth-1        compute-don't-recall rule in every skill
  R4-4              segment-map versioning / staleness control
  R5-M1             root LICENSE + standardized license frontmatter
  (ci)              CI regression suite actually triggers on push/PR to main

Doctrine changes are legitimate; silent divergence is not. If one of these
tests fails after an intentional change, land the change in the canonical
source first (skill 1's references for family doctrine), mirror it into the
other family skills in the same commit, then update the expectation here.

Run from the repository root:  python3 -m pytest tests/ -v
"""
import pathlib
import re

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILL1 = REPO_ROOT / "skills" / "analyzing-us-bigtech-stocks"
SKILL2 = REPO_ROOT / "skills" / "big-tech-earnings-postmortem"
SKILL3 = REPO_ROOT / "skills" / "bigtech-equity-research"
SKILL_DIRS = [SKILL1, SKILL2, SKILL3]
SKILL_SLUGS = [d.name for d in SKILL_DIRS]


def read(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")


def norm(text: str) -> str:
    """Normalize for numeric matching: dashes to hyphen, drop $ and commas."""
    return (text.replace("\u2212", "-").replace("\u2013", "-")
                .replace("\u2014", "-").replace(",", "").replace("$", ""))


def squash(text: str) -> str:
    """Collapse all whitespace (incl. hard line wraps) to single spaces."""
    return re.sub(r"\s+", " ", text)


def skill_markdown(skill_dir: pathlib.Path):
    """Every markdown file in a skill folder."""
    return sorted(p for p in skill_dir.rglob("*.md"))


@pytest.fixture(scope="module")
def corpora():
    """{skill_slug: concatenated normalized markdown of the whole skill}."""
    out = {}
    for d in SKILL_DIRS:
        out[d.name] = norm("\n".join(read(p) for p in skill_markdown(d)))
    return out


# --------------------------------------------------------------------------
# H-1 — one event, one set of verified headline numbers across the family
# --------------------------------------------------------------------------

class TestSharedDatapoints:
    CANON = {
        "close": "282.32",          # GOOG T+1 close, 2026-10-29
        "move_pct": "12.29",        # session move, percent
        "prior_close": "321.89",    # 2026-10-28 close
        "cap_erased": "482",        # ~$B of market value erased (press figure)
    }
    # Figures the audit found stated as conflicting "verified" numbers for the
    # same event. They must never reappear in the family skills.
    FORBIDDEN = ["-12.6%", "-11.71%", "283.35", "283.37"]

    def test_canonical_figures_in_skill1_methodology(self):
        t = norm(read(SKILL1 / "references" / "methodology.md"))
        for v in self.CANON.values():
            assert v in t, f"canonical figure {v} missing from skill 1 methodology"

    def test_canonical_figures_in_skill3_formulas(self):
        t = norm(read(SKILL3 / "reference" / "formulas.md"))
        for v in self.CANON.values():
            assert v in t, f"canonical figure {v} missing from skill 3 formulas.md"

    def test_move_pct_recomputes_from_closes(self):
        """The headline move must be the arithmetic identity of the two closes
        it is stated with (catches silent edits of any one figure)."""
        m1 = norm(read(SKILL1 / "references" / "methodology.md"))
        m = re.search(
            r"GOOG\s+(-\d+\.\d+)%\s+to\s+(\d+\.\d+)\s+\(Oct 29 2026\)\s+from\s+(\d+\.\d+)",
            m1)
        assert m, "skill 1 methodology headline-move sentence not found"
        pct, close, prior = (float(m.group(1)), float(m.group(2)), float(m.group(3)))
        assert (close - prior) / prior * 100 == pytest.approx(pct, abs=0.01)

        m3 = norm(read(SKILL3 / "reference" / "formulas.md"))
        m = re.search(
            r"close\s+(\d+\.\d+)\s+on\s+2026-10-29\s*(-\d+\.\d+)%\s+from\s+the\s+(\d+\.\d+)\s+prior\s+close",
            m3)
        assert m, "skill 3 formulas.md canonical-print sentence not found"
        assert float(m.group(1)) == close
        assert float(m.group(2)) == pytest.approx(pct, abs=0.01)
        assert float(m.group(3)) == prior

    def test_rev_and_eps_examples_are_consistent(self):
        """formulas.md's beat/miss examples must be internally consistent
        arithmetic (guarding the reconciled worked example)."""
        t = norm(read(SKILL3 / "reference" / "formulas.md"))
        m = re.search(r"revenue\): (\d+\.\d+) - (\d+\.\d+) = (-\d+\.\d+)B", t)
        assert m
        assert float(m.group(1)) - float(m.group(2)) == pytest.approx(
            float(m.group(3)), abs=0.005)
        m = re.search(r"EPS\): (\d+\.\d+) - (\d+\.\d+) = (-\d+\.\d+);", t)
        assert m
        assert float(m.group(1)) - float(m.group(2)) == pytest.approx(
            float(m.group(3)), abs=0.005)

    def test_no_legacy_conflicting_figures_anywhere(self, corpora):
        for slug, text in corpora.items():
            for bad in self.FORBIDDEN:
                assert bad not in text, (
                    f"{slug}: legacy conflicting figure {bad!r} for the "
                    "canonical Alphabet Q3 2026 event has reappeared "
                    "(audit finding H-1)")


# --------------------------------------------------------------------------
# H-2 — disclaimer presence
# --------------------------------------------------------------------------

class TestDisclaimer:
    def test_every_skill_carries_disclaimer(self):
        for d in SKILL_DIRS:
            t = squash(read(d / "SKILL.md")).lower()
            assert "not investment advice" in t, (
                f"{d.name}: disclaimer language missing (audit finding H-2)")

    def test_every_skill_declares_mnpi_hygiene(self, corpora):
        for slug, text in corpora.items():
            assert ("mnpi" in text.lower()
                    or "regulation fd" in text.lower()), (
                f"{slug}: Reg FD / MNPI information-barrier statement missing")


# --------------------------------------------------------------------------
# M-3 — one confidence taxonomy across the family
# --------------------------------------------------------------------------

class TestConfidenceTaxonomy:
    LABELS = ("Verified", "Reasoned", "Assumed", "Unverifiable")

    def test_every_skill_declares_all_four_labels(self, corpora):
        for slug, text in corpora.items():
            for label in self.LABELS:
                assert label in text, (
                    f"{slug}: confidence label {label!r} missing from the "
                    "family taxonomy (audit finding M-3)")

    def test_no_legacy_confidence_tiers(self, corpora):
        for slug, text in corpora.items():
            assert not re.search(r"\b(high|medium|low)[ -]confidence\b",
                                 text, re.I), (
                f"{slug}: legacy High/Medium/Low confidence tier language "
                "present — the family taxonomy is "
                "Verified/Reasoned/Assumed/Unverifiable (audit finding M-3)")


# --------------------------------------------------------------------------
# M-2 — one attribution doctrine across the family
# --------------------------------------------------------------------------

class TestAttributionDoctrine:
    def test_skill1_states_computability_rule(self):
        t = read(SKILL1 / "SKILL.md")
        assert re.search(
            r"percentage attribution only if it is computable", t), (
            "skill 1: canonical attribution policy (percentage attribution "
            "only if computable from sourced data) not stated in SKILL.md")

    def test_skill2_states_ordinal_ranks_rule(self):
        t = read(SKILL2 / "SKILL.md")
        assert "ordinal ranks, not fake decompositions" in t, (
            "skill 2: ordinal-ranks doctrine not stated in SKILL.md")

    def test_skill3_states_signed_allocation_rule(self):
        t = read(SKILL3 / "SKILL.md")
        assert "signed allocation" in t, (
            "skill 3: Reasoned signed-allocation doctrine not stated in "
            "SKILL.md")
        m = read(SKILL3 / "reference" / "methodology.md")
        assert "ordinal ranking is the primary output" in m, (
            "skill 3: ordinal-ranking-is-primary doctrine not stated in "
            "reference/methodology.md")

    def test_ordinal_doctrine_in_every_skill(self, corpora):
        for slug, text in corpora.items():
            assert "ordinal" in text.lower(), (
                f"{slug}: ordinal-ranking doctrine absent from the whole "
                "skill (audit finding M-2)")


# --------------------------------------------------------------------------
# M-6 — catalog registration
# --------------------------------------------------------------------------

class TestCatalogRegistration:
    DOCS = [
        REPO_ROOT / "skills" / "skills-catalog.md",
        REPO_ROOT / "skills-inventory.md",
        REPO_ROOT / "docs" / "skills-inventory.md",
        REPO_ROOT / "README.md",
    ]

    def test_all_three_skills_registered_everywhere(self):
        for doc in self.DOCS:
            assert doc.exists(), f"catalog document missing: {doc}"
            t = read(doc)
            for slug in SKILL_SLUGS:
                assert slug in t, (
                    f"{doc.relative_to(REPO_ROOT)}: skill {slug!r} not "
                    "registered (audit finding M-6)")


# --------------------------------------------------------------------------
# P2 — post-mortem framework fold-in wiring
# --------------------------------------------------------------------------

class TestPostmortemFrameworkFoldIn:
    """Skill 1 owns the canonical copy of skill 2's framework; skill 2 defers
    to it. Guards the fold-in (audit roadmap P1 item 4, deferred P2 half)
    from regressing into a fourth divergent restatement."""

    FRAMEWORK = SKILL1 / "references" / "postmortem-framework.md"

    def test_framework_reference_exists(self):
        assert self.FRAMEWORK.exists(), (
            "skills/analyzing-us-bigtech-stocks/references/postmortem-framework.md "
            "is missing — the canonical post-mortem framework must live in "
            "skill 1's references")

    def test_skill1_skill_md_points_to_framework(self):
        t = read(SKILL1 / "SKILL.md")
        assert "postmortem-framework.md" in t, (
            "skill 1 SKILL.md no longer references the post-mortem framework "
            "(Bundled resources / Adaptations wiring)")

    def test_skill2_defers_to_canonical_copy(self):
        t = read(SKILL2 / "SKILL.md")
        assert "postmortem-framework.md" in t, (
            "skill 2 SKILL.md no longer points at the canonical framework "
            "copy in skill 1")
        assert re.search(r"canonical", t, re.I), (
            "skill 2 SKILL.md no longer states the canonical-copy rule")

    def test_framework_declares_family_confidence_labels(self):
        t = read(self.FRAMEWORK)
        for label in ("Verified", "Reasoned", "Assumed", "Unverifiable"):
            assert label in t, (
                f"postmortem-framework.md: confidence label {label!r} missing")

    def test_framework_declares_two_axes(self):
        t = read(self.FRAMEWORK)
        assert "durability" in t.lower()
        assert "evidentiary" in t.lower(), (
            "postmortem-framework.md: the two-axis classification "
            "(durability x evidentiary basis) is not stated")

    def test_framework_cross_references_sibling_skill(self):
        t = read(self.FRAMEWORK)
        assert "big-tech-earnings-postmortem" in t, (
            "postmortem-framework.md: provenance cross-reference to the "
            "standalone lightweight skill is missing")

    def test_framework_keeps_audit_gates_mandatory(self):
        t = read(self.FRAMEWORK)
        # Round-2 doctrine: the lightweight mode enforces the bundled lite gates
        # (note_audit.py + note_overflow_audit.mjs) standalone, and upgrades to
        # the full Phase 10 gates (audit_all.sh) when the flagship is available.
        assert "note_audit.py" in t
        assert "note_overflow_audit.mjs" in t
        assert "audit_all.sh" in t, (
            "postmortem-framework.md: the lightweight mode must still require "
            "delivery gates — lite bundled, full via the Phase 10 wrapper")


# --------------------------------------------------------------------------
# L-1 — frontmatter sanity
# --------------------------------------------------------------------------

class TestFrontmatterSanity:
    @pytest.mark.parametrize("slug", SKILL_SLUGS)
    def test_name_matches_folder(self, slug):
        fm = frontmatter(REPO_ROOT / "skills" / slug / "SKILL.md")
        assert fm.get("name") == slug, (
            f"frontmatter name {fm.get('name')!r} != folder {slug!r}")

    @pytest.mark.parametrize("slug", SKILL_SLUGS)
    def test_description_within_spec_limit(self, slug):
        fm = frontmatter(REPO_ROOT / "skills" / slug / "SKILL.md")
        desc = fm.get("description", "")
        assert 0 < len(desc) <= 1024, (
            f"{slug}: description is {len(desc)} chars; the skill-spec limit "
            "is 1024")

    @pytest.mark.parametrize("slug", SKILL_SLUGS)
    def test_version_is_semver(self, slug):
        fm = frontmatter(REPO_ROOT / "skills" / slug / "SKILL.md")
        assert re.fullmatch(r"\d+\.\d+\.\d+", str(fm.get("version", ""))), (
            f"{slug}: version {fm.get('version')!r} is not semver")


# --------------------------------------------------------------------------
# Round 2 — lite audit gates, licensing, CI wiring, doctrine guards
# (validated against docs/comparative_analysis_report-3/4/5.md)
# --------------------------------------------------------------------------

class TestLiteAuditGates:
    """R3-C1 / R4 #2 / R5 H-1: skills 2 and 3 must ship their own executable
    delivery gates and mandate them — compliance may not depend on the
    flagship being installed."""

    @pytest.mark.parametrize("skill_dir", [SKILL2, SKILL3], ids=["skill2", "skill3"])
    def test_note_audit_vendored(self, skill_dir):
        assert (skill_dir / "scripts" / "note_audit.py").exists(), (
            f"{skill_dir.name}: lite numeric/disclosure gate not bundled")
        assert (skill_dir / "assets" / "checks.json").exists(), (
            f"{skill_dir.name}: disclosure-needle spec not bundled")

    @pytest.mark.parametrize("skill_dir", [SKILL2, SKILL3], ids=["skill2", "skill3"])
    def test_render_gate_vendored(self, skill_dir):
        assert (skill_dir / "scripts" / "note_overflow_audit.mjs").exists(), (
            f"{skill_dir.name}: single-file render gate not bundled (R3-H2)")

    def test_skill2_claims_bundled_gates(self):
        t = read(SKILL2 / "SKILL.md")
        assert "mandatory and bundled" in t, (
            "skill 2 must present the lite gates as mandatory and bundled, not "
            "as an 'if the sibling is installed' dependency")


class TestLicenseStandardization:
    """R5 M-1: one license posture for the family — root LICENSE present and
    every family skill declares it in frontmatter."""

    def test_root_license_exists(self):
        assert (REPO_ROOT / "LICENSE").exists(), (
            "no root LICENSE despite a skill declaring Apache-2.0 (report-5 M-1)")
        assert "Apache License" in read(REPO_ROOT / "LICENSE")
        assert "Version 2.0" in read(REPO_ROOT / "LICENSE")

    @pytest.mark.parametrize("slug", SKILL_SLUGS)
    def test_every_skill_declares_license(self, slug):
        fm = frontmatter(REPO_ROOT / "skills" / slug / "SKILL.md")
        assert fm.get("license") == "Apache-2.0", (
            f"{slug}: license frontmatter key missing or non-Apache-2.0 — the "
            "family is standardized on Apache-2.0")


class TestCIWiring:
    """The regression suite must actually trigger on push/PR to main — a
    malformed or narrowed branch filter would silently disable the whole
    suite while the workflow file still parses."""

    def test_ci_triggers_on_main(self):
        ci = REPO_ROOT / ".github" / "workflows" / "ci.yml"
        assert ci.exists(), "CI workflow missing"
        t = read(ci)
        assert t.count("branches: [main]") == 2, (
            "ci.yml must gate both push and pull_request on branches: [main] "
            "— a malformed trigger silently disables the whole suite")

    def test_ci_runs_the_regression_suite(self):
        t = read(REPO_ROOT / ".github" / "workflows" / "ci.yml")
        assert "pytest tests/" in t, "CI must run the tests/ regression suite"


class TestDoctrineGuardsRound2:
    """Cross-family doctrine added in round 2: verification-status line,
    valuation boundary, compute-don't-recall, segment-map versioning."""

    @pytest.mark.parametrize("slug", SKILL_SLUGS)
    def test_verification_status_required(self, slug):
        t = read(REPO_ROOT / "skills" / slug / "SKILL.md")
        assert re.search(r"verification[\s-]+status", t, re.I), (
            f"{slug}: the deliverable's verification-status line is not required "
            "(report-4 finding #5)")

    @pytest.mark.parametrize("slug", SKILL_SLUGS)
    def test_valuation_boundary_stated(self, slug):
        t = read(REPO_ROOT / "skills" / slug / "SKILL.md")
        assert "valuation boundary" in t.lower(), (
            f"{slug}: valuation boundary (pre-valuation causal-attribution "
            "product) not stated (report-4 finding #1)")

    @pytest.mark.parametrize("slug", SKILL_SLUGS)
    def test_compute_dont_recall_rule(self, slug):
        t = read(REPO_ROOT / "skills" / slug / "SKILL.md")
        assert "in-context" in t.lower() and "arithmetic" in t.lower(), (
            f"{slug}: the no-in-context-arithmetic rule is missing (report-3 "
            "synthesized gap: the hallucinated-math vector)")

    def test_segment_map_is_versioned(self):
        t = read(SKILL3 / "reference" / "segment-maps.md")
        assert "segment_map_version" in t, (
            "segment-maps.md: segment_map_version field missing (report-4 #4)")
        assert "last_verified_against_filing" in t, (
            "segment-maps.md: last_verified_against_filing field missing")
        assert "Staleness rule" in t, (
            "segment-maps.md: the hard staleness rule is missing")

    def test_report_structure_is_14_sections(self):
        t = read(SKILL3 / "templates" / "report-structure.md")
        assert "14-Section" in t, (
            "report-structure.md: dedicated Risk Factors & Falsification "
            "section added — the title must say 14 sections")
        assert "Risk Factors & Falsification Conditions" in t, (
            "report-structure.md: the dedicated falsifiers section (report-4 "
            "medium) is missing")

    def test_strict_modes_documented(self):
        for doc in [SKILL1 / "SKILL.md", SKILL1 / "references" / "fact-base-schema.md",
                    SKILL1 / "references" / "methodology.md"]:
            t = read(doc)
            assert "--strict-verified" in t, (
                f"{doc.name}: strict compliance modes not documented")
            assert "--fail-on-unverified" in t

    def test_audit_all_wrapper_wired(self):
        assert (SKILL1 / "scripts" / "audit_all.sh").exists(), (
            "audit_all.sh wrapper missing (report-5 L-2)")
        t = read(SKILL1 / "SKILL.md")
        assert "audit_all.sh" in t, "SKILL.md does not reference the one-command wrapper"

    def test_beta_window_contract_documented(self):
        t = read(SKILL3 / "reference" / "formulas.md")
        assert "beta_window" in t, (
            "formulas.md: the abnormal_return beta-window code contract is "
            "undocumented (report-3 M1)")


class TestCatalogParity:
    """The two inventory copies stay identical, and their three family entries
    mirror the live SKILL.md frontmatter (versions and descriptions drift
    otherwise — L-1 class hygiene)."""

    INV = [REPO_ROOT / "skills-inventory.md", REPO_ROOT / "docs" / "skills-inventory.md"]

    def test_inventory_copies_identical(self):
        a = read(self.INV[0])
        b = read(self.INV[1])
        assert a == b, "skills-inventory.md and docs/skills-inventory.md diverged"

    @pytest.mark.parametrize("slug", SKILL_SLUGS)
    def test_inventory_mirrors_skill_versions(self, slug):
        fm = frontmatter(REPO_ROOT / "skills" / slug / "SKILL.md")
        for inv in self.INV:
            t = read(inv)
            m = re.search(rf"^### `{re.escape(slug)}`\n\n(.*?)(?=^### )", t, re.S | re.M)
            assert m, f"{inv.name}: entry for {slug} missing"
            vm = re.search(r"^- \*\*Version\*\*: (.+)$", m.group(1), re.M)
            assert vm and vm.group(1).strip() == fm["version"], (
                f"{inv.name}: {slug} entry version {vm.group(1) if vm else None!r} "
                f"!= SKILL.md version {fm['version']!r}")


def frontmatter(path: pathlib.Path) -> dict:
    """Minimal YAML frontmatter parser for flat key: value blocks."""
    text = read(path)
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    assert m, f"{path.name}: no frontmatter block"
    out = {}
    for line in m.group(1).splitlines():
        km = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if not km:
            continue
        key, val = km.group(1), km.group(2).strip()
        if val in ('>', '|', '|-', '>-'):
            # Folded scalar: consume indented continuation lines.
            val = ""
            continue
        if val.startswith('"') and val.endswith('"'):
            val = val[1:-1]
        out[key] = val
    # Folded descriptions: capture the indented block after 'description: >'.
    dm = re.search(r"^description:\s*[>|]\n((?:[ \t]+.*\n?)+)", m.group(1), re.M)
    if dm:
        out["description"] = re.sub(r"\s+", " ", dm.group(1)).strip()
    dm = re.search(r'^description:\s*"(.*)"\s*$', m.group(1), re.S)
    if dm:
        out["description"] = dm.group(1)
    return out
