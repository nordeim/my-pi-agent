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
import json
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


# --------------------------------------------------------------------------
# Round 3 — provenance sealing, lite number registry, segment-map gate,
# scoped needles, buy-side disclosure, canonical beta window, peer baskets
# (validated against docs/comparative_analysis_report-6/7.md)
# --------------------------------------------------------------------------

class TestDoctrineGuardsRound3:
    """Cross-family doctrine added in round 3 (reports 6/7)."""

    @pytest.mark.parametrize("slug", SKILL_SLUGS)
    def test_provenance_seal_vendored_and_wired(self, slug):
        d = REPO_ROOT / "skills" / slug
        assert (d / "scripts" / "provenance_seal.py").exists(), (
            f"{slug}: provenance sealing gate not bundled (report-6/7 C-2)")
        t = read(d / "SKILL.md")
        assert re.search(r"provenance[_ ]seal", t, re.I), (
            f"{slug}: SKILL.md does not wire the provenance seal step")

    @pytest.mark.parametrize("slug", SKILL_SLUGS)
    def test_position_disclosure_doctrine(self, slug):
        t = read(REPO_ROOT / "skills" / slug / "SKILL.md")
        assert re.search(r"fund[_ ]position", t, re.I), (
            f"{slug}: buy-side fund-position disclosure doctrine missing "
            "(report-6/7 C-1, buy-side regime)")

    def test_skill2_bundles_lite_number_registry(self):
        d = SKILL2
        assert (d / "scripts" / "fact_base_lite_audit.py").exists(), (
            "skill 2: number-registry gate not bundled (report-6/7 H-4/H-5)")
        assert (d / "assets" / "fact_base_lite.template.json").exists(), (
            "skill 2: lite fact-base template not bundled")
        t = read(d / "SKILL.md")
        assert "fact_base_lite_audit.py" in t and "fact_base_lite" in t, (
            "skill 2: the number-registry gate is not wired into the workflow")

    def test_skill2_bundles_a11y_gate(self):
        assert (SKILL2 / "scripts" / "a11y_audit.mjs").exists(), (
            "skill 2: accessibility gate not bundled (report-6/7 M-5/M-6)")
        assert "a11y_audit.mjs" in read(SKILL2 / "SKILL.md")

    def test_skill3_segment_map_gate_wired(self):
        d = SKILL3
        assert (d / "scripts" / "segment_map_check.py").exists(), (
            "skill 3: segment-map staleness gate not bundled (report-6/7 H-3)")
        assert (d / "reference" / "segment-maps.json").exists(), (
            "skill 3: machine-readable segment map missing")
        t = read(d / "SKILL.md")
        assert "segment_map_check.py" in t, (
            "skill 3: SKILL.md hard rule 9 must run the mechanical staleness gate")

    def test_skill3_peers_reference_bundled(self):
        p = SKILL3 / "reference" / "peers.md"
        assert p.exists(), (
            "skill 3: canonical peer-basket reference missing (report-6/7 M-4)")
        t = read(p)
        assert "market-cap proximity" in t.lower() or "order of magnitude" in t.lower(), (
            "peers.md must state the selection criteria, not just baskets")
        for ticker in ("GOOGL", "MSFT", "AMZN", "META", "AAPL", "NVDA", "TSLA"):
            assert ticker in t, f"peers.md: no basket guidance for {ticker}"

    def test_canonical_beta_window_documented(self):
        t = read(SKILL3 / "reference" / "formulas.md")
        assert "2-year monthly returns vs QQQ" in t, (
            "formulas.md: the canonical default beta window (report-6/7 H-2) "
            "is not stated")
        m = read(SKILL3 / "reference" / "methodology.md")
        assert "DEFAULT_BETA_WINDOW" in m, (
            "methodology.md: the canonical-default code contract is undocumented")

    def test_reasoned_split_documented_family_wide(self, corpora):
        for slug, text in corpora.items():
            assert "Reasoned (derived)" in text and "Reasoned (judged)" in text, (
                f"{slug}: the derived/judged split of the Reasoned label "
                "(report-6/7 H-2) is not stated")

    def test_consensus_vintage_doctrine_family_wide(self, corpora):
        for slug, text in corpora.items():
            assert "consensus_vintage" in text or "vintage" in text.lower(), (
                f"{slug}: consensus provider/vintage doctrine (report-6/7 H-1) "
                "is not stated")

    def test_fcf_ex_sbc_doctrine(self, corpora):
        for slug, text in corpora.items():
            assert re.search(r"fcf ex[- ]sbc", text, re.I), (
                f"{slug}: the mandatory FCF ex-SBC pairing (report-6/7 "
                "synthesized #8) is not stated")

    def test_vrp_caveat_doctrine(self, corpora):
        for slug, text in corpora.items():
            assert re.search(r"volatility[ -]risk[ -]premium", text, re.I), (
                f"{slug}: the implied-move volatility-risk-premium caveat "
                "(report-6/7 M-3) is not stated")

    def test_schema_documents_round3_fields(self):
        t = read(SKILL1 / "references" / "fact-base-schema.md")
        for needle in ("consensus_provider", "consensus_vintage", "epistemic_kind",
                       "mandate_context", "weights", "realized_move"):
            assert needle in t, (
                f"fact-base-schema.md: round-3 field {needle!r} undocumented")

    def test_methodology_documents_strict_pages(self):
        t = read(SKILL1 / "references" / "methodology.md")
        assert "--strict-pages" in t, (
            "methodology.md: the --strict-pages mode (report-7 M-1) is undocumented")

    def test_family_versions_parity(self):
        """Report-7 L-1: the family version reflects doctrinal equivalence —
        all three skills carry the same semver after a family-wide round."""
        versions = [frontmatter(REPO_ROOT / "skills" / slug / "SKILL.md")["version"]
                    for slug in SKILL_SLUGS]
        assert len(set(versions)) == 1, (
            f"family versions diverged: {dict(zip(SKILL_SLUGS, versions))} — "
            "round 3 landed family-wide; the version must say so")


# --------------------------------------------------------------------------
# Round 4 — validated against comparative analysis reports 8/9:
# number registry for skill 3, event-window rule, multi-class cap delta,
# EV fundamental matrix, consensus statistic, Reg G, legends, temporal
# embargo, beta regime diagnostics, peer hygiene, microstructure lens
# --------------------------------------------------------------------------

class TestDoctrineGuardsRound4:
    """Cross-family doctrine added in round 4 (reports 8/9)."""

    # --- H-2: skill 3 finally ships a machine-checked number registry --------

    def test_skill3_bundles_lite_number_registry(self):
        assert (SKILL3 / "scripts" / "fact_base_lite_audit.py").exists(), (
            "skill 3: number-registry gate not vendored (reports 8/9 H-2 — the "
            "most quantitative member shipped untraceable numbers)")
        assert (SKILL3 / "assets" / "fact_base_lite.template.json").exists(), (
            "skill 3: lite fact-base template not vendored (reports 8/9 H-2)")
        t = read(SKILL3 / "SKILL.md")
        assert "fact_base_lite_audit.py" in t and "fact_base_lite" in t, (
            "skill 3: the number-registry gate is not wired into the workflow")

    def test_skill3_gate_byte_identical_to_skill2(self):
        s2 = (SKILL2 / "scripts" / "fact_base_lite_audit.py").read_bytes()
        s3 = (SKILL3 / "scripts" / "fact_base_lite_audit.py").read_bytes()
        assert s2 == s3, ("the two fact_base_lite_audit.py copies drifted — "
                          "vendoring is byte-identical by design")

    # --- H-3: event-window rule -----------------------------------------------

    @pytest.mark.parametrize("slug", SKILL_SLUGS)
    def test_event_window_rule_family_wide(self, slug):
        t = read(REPO_ROOT / "skills" / slug / "SKILL.md")
        assert re.search(r"pre-market|intraday", t, re.I), (
            f"{slug}: the event-window rule (intraday -> T+0 close, "
            "reports 8/9 H-3) is not stated")
        assert "T+0" in t and "T+1" in t

    def test_event_window_rule_in_flagship_methodology(self):
        t = read(SKILL1 / "references" / "methodology.md")
        assert "event-window rule" in t.lower(), (
            "methodology.md: the Phase 0 event-window rule is undocumented")

    # --- H-4: multi-class market-cap delta --------------------------------------

    @pytest.mark.parametrize("slug", SKILL_SLUGS)
    def test_multiclass_cap_delta_doctrine_family_wide(self, slug):
        t = read(REPO_ROOT / "skills" / slug / "SKILL.md")
        assert re.search(r"market[- ]cap delta", t, re.I), (
            f"{slug}: the multi-class market-cap delta doctrine "
            "(reports 8/9 H-4) is not stated")
        assert "market_cap_delta" in t or "per class" in t.lower()

    def test_multiclass_helper_and_formula_documented(self):
        assert "market_cap_delta" in read(SKILL3 / "scripts" / "quant_helpers.py")
        f = read(SKILL3 / "reference" / "formulas.md")
        assert "per share class and sum" in f, (
            "formulas.md: the per-class sum method is not stated")

    # --- H-6: Expected Fundamental Value matrix ---------------------------------

    @pytest.mark.parametrize("slug", SKILL_SLUGS)
    def test_ev_fundamental_matrix_family_wide(self, slug):
        t = read(REPO_ROOT / "skills" / slug / "SKILL.md")
        assert "Expected Fundamental Value" in t, (
            f"{slug}: the EV fundamental matrix option (reports 8/9 H-6) "
            "is not stated")
        assert "never a price target" in t.lower() or "not a price target" in t.lower()

    # --- M-1: consensus statistic ----------------------------------------------

    @pytest.mark.parametrize("slug", SKILL_SLUGS)
    def test_consensus_statistic_family_wide(self, slug):
        t = squash(read(REPO_ROOT / "skills" / slug / "SKILL.md"))
        assert "consensus_statistic" in t, (
            f"{slug}: the recorded mean/median statistic (reports 8/9 M-1) "
            "is not stated")
        assert "1–3 trading days" in t or "1-3 trading days" in t, (
            f"{slug}: the tightened consensus vintage window is not stated")

    def test_schema_documents_round4_fields(self):
        t = read(SKILL1 / "references" / "fact-base-schema.md")
        for needle in ("consensus_statistic", "data_type", "t1_filing_timestamp"):
            assert needle in t, (
                f"fact-base-schema.md: round-4 field {needle!r} undocumented")

    def test_flagship_gate_default_window_tightened(self):
        t = read(SKILL1 / "scripts" / "fact_base_audit.py")
        assert 'default=5' in t, (
            "fact_base_audit.py: --consensus-max-age-days default must be 5 "
            "calendar days (≈ 3 trading days, reports 8/9 M-1)")
        assert "consensus_statistic" in t

    # --- M-2: Reg G / Item 10(e) ------------------------------------------------

    @pytest.mark.parametrize("slug", SKILL_SLUGS)
    def test_reg_g_doctrine_family_wide(self, slug):
        t = read(REPO_ROOT / "skills" / slug / "SKILL.md")
        assert re.search(r"reg g / item 10\(e\)", t, re.I), (
            f"{slug}: the non-GAAP reconciliation discipline (reports 8/9 M-2) "
            "is not stated")

    # --- M-3 / C-1: legends ------------------------------------------------------

    @pytest.mark.parametrize("slug", SKILL_SLUGS)
    def test_not_a_research_report_legend_family_wide(self, slug):
        t = read(REPO_ROOT / "skills" / slug / "SKILL.md")
        assert "not a research report" in t.lower(), (
            f"{slug}: the internal-use legend (reports 8/9 C-1 scope hardening) "
            "is not stated")
        assert "internal use only" in t.lower()

    @pytest.mark.parametrize("slug", SKILL_SLUGS)
    def test_public_source_only_family_wide(self, slug):
        t = read(REPO_ROOT / "skills" / slug / "SKILL.md")
        assert "Public-source-only" in t or "public-source-only" in t.lower(), (
            f"{slug}: the public-source-only limitation (reports 8/9 M-3) "
            "is not stated")

    def test_lite_checks_json_carry_round4_legends(self):
        for slug in ("big-tech-earnings-postmortem", "bigtech-equity-research"):
            data = json.loads(read(REPO_ROOT / "skills" / slug / "assets" /
                                   "checks.json"))
            req = " ".join(str(x).lower() for x in data.get("required", []))
            assert "not a research report" in req, (
                f"{slug}: 'not a research report' legend is not an enforced needle")
            assert "public-source-only" in req, (
                f"{slug}: 'Public-source-only' limitation is not an enforced needle")

    # --- M-4: data licensing -----------------------------------------------------

    @pytest.mark.parametrize("slug", SKILL_SLUGS)
    def test_data_licensing_family_wide(self, slug):
        t = read(REPO_ROOT / "skills" / slug / "SKILL.md")
        assert re.search(r"data licensing", t, re.I), (
            f"{slug}: the data-licensing/redistribution doctrine "
            "(reports 8/9 M-4) is not stated")

    # --- M-5: the postmortem bundles its own arithmetic helper -------------------

    def test_quant_helpers_vendored_byte_identical_x3(self):
        bodies = [(d / "scripts" / "quant_helpers.py").read_bytes()
                  for d in (SKILL1, SKILL2, SKILL3)]
        assert all(bodies), "a quant_helpers.py copy is missing"
        assert len(set(bodies)) == 1, (
            "quant_helpers.py drifted across the family (reports 8/9 M-5: the "
            "postmortem must be standalone — byte-identical vendoring)")

    def test_postmortem_no_longer_depends_on_sibling_helper(self):
        t = read(SKILL2 / "SKILL.md")
        assert "sibling skill's" not in t or "bundled" in t.lower(), (
            "skill 2 still routes arithmetic to a sibling helper without "
            "bundling its own (reports 8/9 M-5)")

    # --- M-6: temporal embargo ----------------------------------------------------

    @pytest.mark.parametrize("slug", SKILL_SLUGS)
    def test_temporal_embargo_family_wide(self, slug):
        t = read(REPO_ROOT / "skills" / slug / "SKILL.md")
        assert "t1_filing_timestamp" in t, (
            f"{slug}: the temporal embargo pin (reports 8/9 M-6) is not stated")
        assert "data_type" in t
        assert "pre_event_input" in t and "post_event_fact" in t

    def test_flagship_temporal_gate_implemented(self):
        t = read(SKILL1 / "scripts" / "fact_base_audit.py")
        assert "TEMPORAL" in t and "check_temporal_order" in t, (
            "fact_base_audit.py: the TEMPORAL gate is not implemented")

    def test_lite_temporal_gate_implemented(self):
        t = read(SKILL2 / "scripts" / "fact_base_lite_audit.py")
        assert "TEMPORAL" in t and "check_temporal_order" in t, (
            "fact_base_lite_audit.py: the lite TEMPORAL check is not implemented")

    # --- M-7: beta regime diagnostics ----------------------------------------------

    def test_beta_regime_diagnostics_implemented_and_documented(self):
        qh = read(SKILL3 / "scripts" / "quant_helpers.py")
        assert "beta_diagnostics" in qh and "volatility_regime_flag" in qh, (
            "quant_helpers.py: the beta regime diagnostics (reports 8/9 M-7) "
            "are not implemented")
        f = read(SKILL3 / "reference" / "formulas.md")
        assert "beta_diagnostics" in f and "R_SQUARED_FLOOR" in f, (
            "formulas.md: the regime diagnostics contract is undocumented")
        m = read(SKILL3 / "reference" / "methodology.md")
        assert "beta_diagnostics" in m, (
            "methodology.md: the regime diagnostics are not wired into Phase 2")

    @pytest.mark.parametrize("slug", SKILL_SLUGS)
    def test_beta_regime_doctrine_family_wide(self, slug):
        t = read(REPO_ROOT / "skills" / slug / "SKILL.md")
        assert "beta_diagnostics" in t or "R²" in t or "R2" in t, (
            f"{slug}: the beta regime diagnostic doctrine (reports 8/9 M-7) "
            "is not stated")

    # --- M-8: peer-basket hygiene ---------------------------------------------------

    def test_peer_hygiene_in_peers_reference(self):
        t = read(SKILL3 / "reference" / "peers.md")
        assert "Constituent hygiene" in t, (
            "peers.md: the constituent-hygiene protocol (reports 8/9 M-8) "
            "is missing")
        assert "corporate-action" in t.lower() and "index-membership" in t.lower()

    @pytest.mark.parametrize("slug", SKILL_SLUGS)
    def test_peer_hygiene_family_wide(self, slug):
        t = read(REPO_ROOT / "skills" / slug / "SKILL.md")
        assert "corporate-action" in t.lower(), (
            f"{slug}: the peer corporate-action check (reports 8/9 M-8) "
            "is not stated")

    # --- L-4: microstructure lens -----------------------------------------------------

    def test_microstructure_lens_in_flagship(self):
        t = read(SKILL1 / "SKILL.md")
        assert re.search(r"\(i\) market microstructure", t, re.I) or \
            "market microstructure" in t.lower(), (
            "flagship: the microstructure lens (reports 8/9 L-4) is missing "
            "from the hypothesis tree")
        m = read(SKILL1 / "references" / "methodology.md")
        assert "Market microstructure & flow" in m, (
            "methodology.md: lens (i) is undocumented")

    # --- H-5: validation protocol -------------------------------------------------------

    def test_validation_protocol_documented(self):
        t = read(SKILL1 / "references" / "methodology.md")
        assert "Methodology validation protocol" in t, (
            "methodology.md: the validation protocol (reports 8/9 H-5, "
            "documented-pending) is missing")


# --------------------------------------------------------------------------
# Round 5 — validated against comparative analysis reports 10/11:
# source snapshots (internal consistency vs source truth), unconditional
# position disclosure, methodology-status disclosure, --strict-temporal,
# --json CI output, the .mjs env-error exit-code contract
# --------------------------------------------------------------------------

class TestDoctrineGuardsRound5:
    """Cross-family doctrine added in round 5 (reports 10/11)."""

    # --- §3.4/§6.9: source snapshots -----------------------------------------

    def test_source_snapshot_vendored_x3_byte_identical(self):
        scripts = [REPO_ROOT / "skills" / slug / "scripts" / "source_snapshot.py"
                   for slug in SKILL_SLUGS]
        assert all(s.exists() for s in scripts), (
            "source_snapshot.py must ship with all three family skills "
            "(round 5, reports 10/11 §3.4)")
        bodies = {s.read_bytes() for s in scripts}
        assert len(bodies) == 1, (
            "the three source_snapshot.py copies drifted — vendoring is "
            "byte-identical by design")

    @pytest.mark.parametrize("slug", SKILL_SLUGS)
    def test_snapshot_doctrine_family_wide(self, slug):
        t = read(REPO_ROOT / "skills" / slug / "SKILL.md")
        assert "source_snapshot" in t, (
            f"{slug}: the source-snapshot discipline (round 5, reports 10/11 "
            "§3.4 — internal consistency vs source truth) is not stated")
        assert "internal consistency" in t.lower(), (
            f"{slug}: the internal-consistency-vs-source-truth caveat is not "
            "stated (reports 10/11 §3.4)")

    def test_snapshot_gate_in_both_audits(self):
        for script in (SKILL1 / "scripts" / "fact_base_audit.py",
                       SKILL2 / "scripts" / "fact_base_lite_audit.py",
                       SKILL3 / "scripts" / "fact_base_lite_audit.py"):
            assert "check_source_snapshots" in read(script), (
                f"{script.name}: the SNAPSHOT gate is missing")
        assert (SKILL2 / "scripts" / "fact_base_lite_audit.py").read_bytes() == \
            (SKILL3 / "scripts" / "fact_base_lite_audit.py").read_bytes(), (
                "the two lite audit copies drifted")

    def test_schema_documents_source_snapshot_field(self):
        t = read(SKILL1 / "references" / "fact-base-schema.md")
        assert "`source_snapshot`" in t, (
            "fact-base-schema.md: the source_snapshot field (round 5) is "
            "undocumented")

    def test_snapshot_doctrine_in_methodology(self):
        t = read(SKILL1 / "references" / "methodology.md")
        assert "Source snapshots" in t, (
            "methodology.md: the Phase 1 snapshot doctrine (round 5) is missing")
        assert "--strict-temporal" in t, (
            "methodology.md: the --strict-temporal flag (round 5) is undocumented")

    def test_lite_templates_demonstrate_snapshot_field(self):
        for tpl in (SKILL2 / "assets" / "fact_base_lite.template.json",
                    SKILL3 / "assets" / "fact_base_lite.template.json"):
            data = json.loads(tpl.read_text(encoding="utf-8"))
            assert any("source_snapshot" in str(f) for f in data["facts"]), (
                f"{tpl.parent.parent.name}: lite template does not demonstrate "
                "the source_snapshot field")
            assert "mandate_context" in data.get("meta", {}), (
                f"{tpl.parent.parent.name}: lite template does not demonstrate "
                "meta.mandate_context")

    # --- §3.5: unconditional position disclosure ---------------------------------

    @pytest.mark.parametrize("slug", SKILL_SLUGS)
    def test_unconditional_position_disclosure_family_wide(self, slug):
        t = read(REPO_ROOT / "skills" / slug / "SKILL.md")
        assert re.search(r"unconditional", t, re.I), (
            f"{slug}: the unconditional position disclosure doctrine "
            "(round 5, reports 10/11 §3.5) is not stated")

    def test_mandate_gate_hardened_in_both_audits(self):
        for script in (SKILL1 / "scripts" / "fact_base_audit.py",
                       SKILL2 / "scripts" / "fact_base_lite_audit.py"):
            body = read(script)
            assert "incomplete" in body and "MANDATE" in body, (
                f"{script.name}: the declared-but-incomplete mandate failure "
                "(round 5, reports 10/11 §3.5) is missing")

    # --- §3.6: methodology-status disclosure ---------------------------------------

    @pytest.mark.parametrize("slug", ("big-tech-earnings-postmortem",
                                      "bigtech-equity-research"))
    def test_methodology_status_needle_in_lite_checks(self, slug):
        checks = json.loads(
            (REPO_ROOT / "skills" / slug / "assets" / "checks.json")
            .read_text(encoding="utf-8"))
        assert "Methodology status:" in checks.get("required", []), (
            f"{slug}: the methodology-status required needle (round 5, "
            "reports 10/11 §3.6) is missing from checks.json")

    @pytest.mark.parametrize("slug", SKILL_SLUGS)
    def test_methodology_status_doctrine_family_wide(self, slug):
        t = read(REPO_ROOT / "skills" / slug / "SKILL.md")
        assert re.search(r"methodology[- ]status", t, re.I), (
            f"{slug}: the methodology-status line doctrine (round 5, reports "
            "10/11 §3.6) is not stated")
        assert re.search(r"face validity", t, re.I), (
            f"{slug}: the face-validity-only caveat is not stated")

    def test_methodology_status_in_report_structure_template(self):
        t = read(SKILL3 / "templates" / "report-structure.md")
        assert re.search(r"methodology[- ]status", t, re.I), (
            "report-structure.md: the methodology-status line (round 5) is "
            "undocumented for the note template")

    def test_methodology_status_in_evidence_ledger_template(self):
        t = read(SKILL3 / "templates" / "evidence-ledger.md")
        assert re.search(r"methodology status", t, re.I), (
            "evidence-ledger.md: the method-note methodology status (round 5) "
            "is undocumented")

    # --- §5.3: --strict-temporal + --json ------------------------------------------

    def test_strict_temporal_flag_in_both_audits(self):
        for script in (SKILL1 / "scripts" / "fact_base_audit.py",
                       SKILL2 / "scripts" / "fact_base_lite_audit.py"):
            body = read(script)
            assert "--strict-temporal" in body, (
                f"{script.name}: the --strict-temporal flag (round 5, "
                "reports 10/11 §5.3) is missing")

    def test_json_mode_in_all_python_gates(self):
        gates = [
            SKILL1 / "scripts" / "fact_base_audit.py",
            SKILL2 / "scripts" / "fact_base_lite_audit.py",
            SKILL2 / "scripts" / "note_audit.py",
            SKILL3 / "scripts" / "segment_map_check.py",
        ]
        for g in gates:
            assert '"--json"' in read(g) or "--json" in read(g), (
                f"{g.name}: the --json CI mode (round 5, reports 10/11 §5.3) "
                "is missing")

    # --- report 11 §5.7: undisclosed consensus NOTE -----------------------------------

    def test_undisclosed_consensus_note_in_both_audits(self):
        for script in (SKILL1 / "scripts" / "fact_base_audit.py",
                       SKILL2 / "scripts" / "fact_base_lite_audit.py"):
            body = read(script)
            assert "undisclosed" in body and "Data-Gap Ledger" in body, (
                f"{script.name}: the undisclosed-statistic NOTE pointing at "
                "the Data-Gap Ledger (round 5, reports 10/11 §5.7) is missing")

    # --- .mjs env-error exit-code contract (own finding, reproduced) ------------------

    def test_mjs_gates_exit_2_on_missing_browser_binary(self):
        """The gates' documented exit-code contract says 2 = environment
        error; a Chromium launch failure used to crash with exit 1, so the
        tests' env-skip never fired. Each .mjs gate guards the launch."""
        mjs = [
            SKILL1 / "scripts" / "a11y_audit.mjs",
            SKILL2 / "scripts" / "a11y_audit.mjs",
            SKILL3 / "scripts" / "a11y_audit.mjs",
            SKILL1 / "scripts" / "overflow_audit.mjs",
            SKILL2 / "scripts" / "note_overflow_audit.mjs",
            SKILL3 / "scripts" / "note_overflow_audit.mjs",
        ]
        for m in mjs:
            assert m.exists(), f"{m} missing"
            body = read(m)
            assert "launchBrowser" in body, (
                f"{m.name}: the guarded browser launch (exit 2 env error, "
                "round 5) is missing")
        bodies_a11y = {(REPO_ROOT / "skills" / s / "scripts" /
                        "a11y_audit.mjs").read_bytes()
                       for s in SKILL_SLUGS}
        assert len(bodies_a11y) == 1, "a11y_audit.mjs copies drifted"
        bodies_nof = {(REPO_ROOT / "skills" / s / "scripts" /
                       "note_overflow_audit.mjs").read_bytes()
                      for s in ("big-tech-earnings-postmortem",
                                "bigtech-equity-research")}
        assert len(bodies_nof) == 1, "note_overflow_audit.mjs copies drifted"

    # --- family version parity ---------------------------------------------------------

    def test_family_version_is_1_6_0(self):
        """Round 5 landed family-wide — the semver says so in all three
        skills (reports 10/11 remediation round)."""
        for slug in SKILL_SLUGS:
            v = frontmatter(REPO_ROOT / "skills" / slug / "SKILL.md")["version"]
            assert v == "1.6.0", (
                f"{slug}: version {v} != 1.6.0 — round 5 landed family-wide")


# --------------------------------------------------------------------------
# Catalog parity (kept last: the inventory copies mirror live frontmatter)
# --------------------------------------------------------------------------

class TestCatalogInventoryParity:
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
