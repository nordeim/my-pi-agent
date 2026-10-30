"""Regression tests for skills/analyzing-us-bigtech-stocks/scripts/fact_base_audit.py.

Guards audit finding H-4 (unanchored substring matching let absent numbers pass
the numeric gate) plus the script's self-test wiring and the L-4 fix (placeholder
scan sees visible text only, never <script>/<style> blocks).

Run from the repository root:  python3 -m pytest tests/ -v
"""
import importlib.util
import json
import pathlib
import subprocess
import sys

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "skills" / "analyzing-us-bigtech-stocks" / "scripts" / "fact_base_audit.py"
EVIDENCE = REPO_ROOT / "docs" / "skills-audit" / "evidence" / "test_fact_base_audit_falsepass.py"


@pytest.fixture(scope="module")
def fba():
    """Load fact_base_audit.py as a module (it lives outside any package)."""
    spec = importlib.util.spec_from_file_location("fact_base_audit", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestTokenInAnchoring:
    """The H-4 false-pass hole, pinned at the unit level.

    Pre-fix, token_in() used unanchored substring matching, so a fact of 82.3
    satisfied itself against a slide printing $282.32 (exit 0). These tests fail
    if the anchoring is ever loosened again.
    """

    def test_substring_inside_larger_number_is_not_a_match(self, fba):
        # Audit case 1: fact 82.3 vs slide "$282.32"
        assert fba.token_in("82.3", fba.norm("$282.32")) is False

    def test_token_inside_negative_percent_is_not_a_match(self, fba):
        # Audit case 2: fact 12.29 vs slide "-112.29%" (unicode minus and hyphen)
        assert fba.token_in("12.29", fba.norm("\u2212112.29%")) is False
        assert fba.token_in("12.29", fba.norm("-112.29%")) is False

    def test_exact_token_matches(self, fba):
        assert fba.token_in("282.32", fba.norm("$282.32")) is True
        assert fba.token_in("-12.29", fba.norm("\u221212.29%")) is True

    def test_magnitude_fallback_matches_sign_flip(self, fba):
        # Slide prints "erased $482B" for a fact recorded as -482.
        assert fba.token_in("-482", fba.norm("$482B erased")) is True
        assert fba.token_in("-9.1", fba.norm("-$9.1B")) is True

    def test_numeric_equality_matches_trailing_zero(self, fba):
        assert fba.token_in("9.10", fba.norm("$9.1B")) is True

    def test_absent_number_stays_absent(self, fba):
        assert fba.token_in("63.4", fba.norm("$282.32")) is False


class TestNumericTokens:
    def test_plain_number(self, fba):
        assert fba.numeric_tokens(282.32) == ["282.32"]

    def test_symbol_broken_sign_degrades_to_magnitude(self, fba):
        # "-" separated from the digits by "$" is not captured; token_in()'s
        # magnitude fallback covers the sign either way.
        assert fba.numeric_tokens("-$9.1B") == ["9.1"]

    def test_non_numeric_yields_no_tokens(self, fba):
        assert fba.numeric_tokens("n/a") == []
        assert fba.numeric_tokens(None) == []
        assert fba.numeric_tokens(True) == []


class TestPlaceholderScanScope:
    """The L-4 fix: scan visible text only, not <script>/<style> blocks."""

    def test_visible_todo_is_flagged(self, fba):
        fails = fba.scan_placeholders(
            {"slide_01.html": "<html><body><p>TODO fill in</p></body></html>"})
        assert any("todo" in f for f in fails)

    def test_css_class_placeholder_is_not_flagged(self, fba):
        fails = fba.scan_placeholders({
            "slide_01.html":
            "<html><head><style>.placeholder{color:red}</style></head>"
            "<body><p>Close: $282.32</p></body></html>"})
        assert fails == []

    def test_js_undefined_token_is_not_flagged(self, fba):
        fails = fba.scan_placeholders({
            "slide_01.html":
            "<html><head><script>var undefined = 1;</script></head>"
            "<body><p>Move: -12.29%</p></body></html>"})
        assert fails == []


class TestStrictComplianceModes:
    """Report-3 M2 / report-4 #3: opt-in strict modes for institutional builds.

    --strict-verified     every `Verified` fact needs >=2 cross_checked_with
    --decision-critical   named fact IDs need >=2 cross-checks (CLI form of
                           meta.decision_critical)
    --fail-on-unverified  reverse-check candidates become failures

    The modes are opt-in by design (report-4's reconciliation of report-3's
    strict-by-default proposal): the default run must NOT enforce them.
    """

    @pytest.fixture(scope="class")
    def fb(self):
        return {
            "meta": {"method_page": "slide_01.html", "decision_critical": ["F-9"]},
            "facts": [
                {"id": "F-1", "value": 1.0, "confidence": "Verified",
                 "cross_checked_with": ["F-2"], "slide_pages": ["slide_01.html"]},
                {"id": "F-2", "value": 2.0, "confidence": "Verified",
                 "cross_checked_with": ["F-1", "F-3"],
                 "slide_pages": ["slide_01.html"]},
                {"id": "F-9", "value": 9.0, "confidence": "Verified",
                 "cross_checked_with": [], "slide_pages": ["slide_01.html"]},
            ],
        }

    @pytest.fixture(scope="class")
    def slides(self, tmp_path_factory):
        d = tmp_path_factory.mktemp("strict")
        (d / "slide_01.html").write_text(
            "<html><body><p>1.0 2.0 9.0 — and an unsourced $103% figure.</p></body></html>",
            encoding="utf-8")
        return d

    def _run(self, fba, slides, fb, *extra):
        import json as _json
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            fbp = pathlib.Path(td) / "fb.json"
            fbp.write_text(_json.dumps(fb), encoding="utf-8")
            rp = pathlib.Path(td) / "r.json"
            code = fba.main(["--slides", str(slides), "--fact-base", str(fbp),
                             "--report", str(rp), *extra])
            report = _json.loads(rp.read_text())
        return code, report

    def test_default_run_enforces_nothing_strict(self, fba, slides, fb):
        code, report = self._run(fba, slides, fb)
        # F-1 (Verified, 1 cross-check) and F-9 (decision-critical via meta!) ...
        # meta.decision_critical IS enforced by default:
        assert any("F-9" in f and "CROSSCHECK" in f for f in report["failures"])
        # ... but plain Verified facts are not:
        assert not any("F-1" in f and "CROSSCHECK" in f for f in report["failures"])
        # ... and unverified candidates stay advisory, not failures:
        assert not any("UNVERIFIED" in f for f in report["failures"])
        assert code == 1  # F-9 cross-check failure

    def test_strict_verified_enforces_double_sourcing(self, fba, slides, fb):
        code, report = self._run(fba, slides, fb, "--strict-verified")
        assert any("F-1" in f and "CROSSCHECK" in f for f in report["failures"]), (
            "--strict-verified must fail a Verified fact with <2 cross-checks")
        assert not any("F-2" in f and "CROSSCHECK" in f for f in report["failures"]), (
            "a fact with 2 cross-checks must pass strict mode")

    def test_fail_on_unverified_promotes_candidates(self, fba, slides, fb):
        code, report = self._run(fba, slides, fb, "--fail-on-unverified")
        assert any("UNVERIFIED" in f and "103" in f for f in report["failures"]), (
            "--fail-on-unverified must promote the unsourced $103% figure to a failure")

    def test_decision_critical_cli_list(self, fba, slides, fb):
        import copy
        fb2 = copy.deepcopy(fb)
        del fb2["meta"]["decision_critical"]
        code, report = self._run(fba, slides, fb2, "--decision-critical", "F-1")
        assert any("F-1" in f and "CROSSCHECK" in f for f in report["failures"]), (
            "--decision-critical F-1 must enforce the >=2 rule without meta/strict")

    def test_cross_check_unit_function(self, fba):
        fb = {"meta": {}, "facts": [
            {"id": "A", "confidence": "Verified", "cross_checked_with": ["x"]},
            {"id": "B", "confidence": "Verified", "cross_checked_with": ["x", "y"]},
            {"id": "C", "confidence": "Reasoned", "cross_checked_with": []},
        ]}
        fails = fba.check_cross_checks(fb, strict_verified=True, extra_ids="")
        assert [f.split()[1] for f in fails] == ["A"]
        fails = fba.check_cross_checks(fb, strict_verified=False, extra_ids="C")
        assert [f.split()[1] for f in fails] == ["C"]
        assert fba.check_cross_checks(fb, strict_verified=False, extra_ids="") == []


class TestRound3SchemaGates:
    """Round 3 (reports 6/7): consensus sourcing, epistemic kinds, waterfall
    sums, and mandate context — always-on, deterministic schema checks."""

    def _fb(self, **over):
        fb = {"meta": {"event_timestamp": "2026-10-28T16:05:00-04:00"},
              "facts": []}
        fb.update(over)
        return fb

    def test_consensus_fact_requires_provider_vintage_tier(self, fba):
        fb = self._fb(facts=[
            {"id": "C-1", "metric": "Revenue consensus, Q3 2026", "value": 128.22}])
        fails = fba.check_consensus_facts(fb)
        assert any("C-1" in f and "CONSENSUS" in f for f in fails), (
            "a consensus fact without provider/vintage/tier must fail (H-1)")

    def test_t3_consensus_source_fails(self, fba):
        fb = self._fb(facts=[
            {"id": "C-2", "metric": "EPS consensus", "value": 3.02,
             "source_tier": "T3", "consensus_provider": "an aggregator",
             "consensus_vintage": "2026-10-26"}])
        fails = fba.check_consensus_facts(fb)
        assert any("C-2" in f and "T1/T2" in f for f in fails), (
            "an aggregator consensus print is never sufficient (H-1)")

    def test_fresh_consensus_fact_passes(self, fba):
        fb = self._fb(facts=[
            {"id": "C-3", "metric": "Revenue consensus", "value": 128.22,
             "source_tier": "T2", "consensus_provider": "LSEG (via Reuters)",
             "consensus_vintage": "2026-10-26",
             "consensus_statistic": "mean"}])
        assert fba.check_consensus_facts(fb) == []

    def test_stale_consensus_vintage_fails(self, fba):
        fb = self._fb(facts=[
            {"id": "C-4", "metric": "Revenue consensus", "value": 128.22,
             "source_tier": "T2", "consensus_provider": "LSEG",
             "consensus_vintage": "2026-09-01",             # 57 days before the event
             "consensus_statistic": "mean"}])
        fails = fba.check_consensus_facts(fb)
        assert any("C-4" in f and "CONSENSUS" in f for f in fails)

    def test_consensus_age_window_configurable(self, fba):
        fb = self._fb(facts=[
            {"id": "C-5", "metric": "Revenue consensus", "value": 128.22,
             "source_tier": "T2", "consensus_provider": "LSEG",
             "consensus_vintage": "2026-09-01",
             "consensus_statistic": "mean"}])
        assert fba.check_consensus_facts(fb, max_age_days=0) == [], (
            "max_age_days=0 must disable the freshness check while keeping "
            "the provider/statistic/tier requirements")

    def test_vintage_at_the_round4_default_boundary_passes(self, fba):
        """Round 4 (reports 8/9 M-1): the default window tightened 10 -> 5
        calendar days ≈ 3 trading days. 5 days old passes, 6 days old fails."""
        fb = self._fb(facts=[
            {"id": "C-7", "metric": "Revenue consensus", "value": 128.22,
             "source_tier": "T2", "consensus_provider": "LSEG",
             "consensus_vintage": "2026-10-23",               # 5 days before the event
             "consensus_statistic": "mean"}])
        assert fba.check_consensus_facts(fb) == []
        fb["facts"][0]["consensus_vintage"] = "2026-10-22"   # 6 days — now stale
        fails = fba.check_consensus_facts(fb)
        assert any("C-7" in f and "outside the 5-day" in f for f in fails)

    def test_consensus_statistic_required(self, fba):
        """Round 4 (reports 8/9 M-1): mean-vs-median is a recorded disclosure —
        a consensus fact without consensus_statistic fails the gate."""
        fb = self._fb(facts=[
            {"id": "C-8", "metric": "EPS consensus", "value": 3.02,
             "source_tier": "T2", "consensus_provider": "LSEG",
             "consensus_vintage": "2026-10-26"}])
        fails = fba.check_consensus_facts(fb)
        assert any("C-8" in f and "consensus_statistic" in f for f in fails), (
            "the recorded mean/median/undisclosed statistic is mandatory")

    def test_consensus_statistic_must_be_valid(self, fba):
        fb = self._fb(facts=[
            {"id": "C-9", "metric": "EPS consensus", "value": 3.02,
             "source_tier": "T2", "consensus_provider": "LSEG",
             "consensus_vintage": "2026-10-26",
             "consensus_statistic": "average-ish"}])
        fails = fba.check_consensus_facts(fb)
        assert any("C-9" in f and "mean / median / undisclosed" in f for f in fails)

    def test_undisclosed_statistic_is_valid(self, fba):
        fb = self._fb(facts=[
            {"id": "C-10", "metric": "EPS consensus", "value": 3.02,
             "source_tier": "T2", "consensus_provider": "LSEG",
             "consensus_vintage": "2026-10-26",
             "consensus_statistic": "undisclosed"}])
        assert fba.check_consensus_facts(fb) == []

    def test_is_consensus_flag_detected(self, fba):
        fb = self._fb(facts=[
            {"id": "C-6", "metric": "Street revenue estimate set", "value": 128.22,
             "is_consensus": True}])
        fails = fba.check_consensus_facts(fb)
        assert any("C-6" in f and "CONSENSUS" in f for f in fails), (
            "the is_consensus marker must route a fact into the consensus gate")

    def test_reasoned_fact_requires_epistemic_kind(self, fba):
        fb = self._fb(facts=[
            {"id": "E-1", "value": -3.9, "confidence": "Reasoned",
             "formula": "-9.1 + 5.2 = -3.9"}])
        fails = fba.check_epistemic_kinds(fb)
        assert any("E-1" in f and "EPISTEMIC" in f for f in fails), (
            "a Reasoned fact without epistemic_kind conflates reproducible math "
            "with opinion (H-2)")

    def test_derived_kind_requires_formula(self, fba):
        fb = self._fb(facts=[
            {"id": "E-2", "value": -3.9, "confidence": "Reasoned",
             "epistemic_kind": "derived"}])
        fails = fba.check_epistemic_kinds(fb)
        assert any("E-2" in f and "formula" in f for f in fails)

    def test_parenthesized_forms_accepted(self, fba):
        fb = self._fb(facts=[
            {"id": "E-3", "value": -3.9, "confidence": "Reasoned (derived)",
             "formula": "-9.1 + 5.2 = -3.9"},
            {"id": "E-4", "value": "allocation", "confidence": "Reasoned (judged)"}])
        assert fba.check_epistemic_kinds(fb) == []

    def test_waterfall_weights_must_sum_to_move(self, fba):
        fb = self._fb(facts=[
            {"id": "W-1", "value": "allocation",
             "weights": {"benchmark": -1.5, "fcf_capex": -3.9, "eps_quality": -2.7,
                         "search": -2.4, "positioning": -1.8},
             "realized_move": -12.29}])
        assert fba.check_waterfall_sums(fb) == []

    def test_waterfall_mismatch_fails(self, fba):
        fb = self._fb(facts=[
            {"id": "W-2", "value": "allocation",
             "weights": {"benchmark": -1.5, "fcf_capex": -2.0},
             "realized_move": -12.29}])
        fails = fba.check_waterfall_sums(fb)
        assert any("W-2" in f and "WATERFALL" in f for f in fails), (
            "the sum-to-move identity must be enforced in code, not just prose (H-2)")

    def test_waterfall_sign_flip_fails(self, fba):
        fb = self._fb(facts=[
            {"id": "W-3", "value": "allocation",
             "weights": {"benchmark": 1.5, "fcf_capex": 3.9},
             "realized_move": -12.29}])
        assert any("W-3" in f for f in fba.check_waterfall_sums(fb))

    def test_ic_audience_requires_mandate_context(self, fba):
        fb = self._fb(meta={"event_timestamp": "2026-10-28T16:05:00-04:00",
                            "audience": "institutional PM/IC"}, facts=[])
        fails = fba.check_mandate_context(fb)
        assert any("MANDATE" in f for f in fails), (
            "an IC-facing fact base must disclose fund_position + position_as_of "
            "(C-1, buy-side conflict disclosure)")

    def test_mandate_context_passes_when_present(self, fba):
        fb = self._fb(meta={"event_timestamp": "2026-10-28T16:05:00-04:00",
                            "audience": "investment committee",
                            "mandate_context": {"fund_position": "none",
                                                "position_as_of": "2026-10-30"}},
                      facts=[])
        assert fba.check_mandate_context(fb) == []

    def test_non_ic_audience_stays_silent(self, fba):
        fb = self._fb(meta={"event_timestamp": "2026-10-28T16:05:00-04:00",
                            "audience": "internal research desk"}, facts=[])
        assert fba.check_mandate_context(fb) == []


class TestTemporalGate:
    """Round 4 (reports 8/9 M-6, report-9-corrected design): the pre-filing
    embargo with the data_type discriminator. Post-event facts retrieved
    before the verified T1 filing time fail; pre-event inputs are exempt;
    the gate is silent without meta.t1_filing_timestamp."""

    def _fb(self, **over):
        fb = {"meta": {"t1_filing_timestamp": "2026-10-28T16:05:00-04:00"},
              "facts": []}
        fb.update(over)
        return fb

    def test_pre_filing_post_event_fact_fails(self, fba):
        fb = self._fb(facts=[
            {"id": "T-1", "value": 42.29, "confidence": "Verified",
             "data_type": "post_event_fact",
             "retrieved_at": "2026-10-28T10:00:00-04:00"}])
        fails = fba.check_temporal_order(fb)
        assert any("T-1" in f and "TEMPORAL" in f
                   and "pre-filing contamination" in f for f in fails), (
            "a post-event claim retrieved before the filing is contamination")

    def test_post_filing_post_event_fact_passes(self, fba):
        fb = self._fb(facts=[
            {"id": "T-2", "value": 282.32, "confidence": "Verified",
             "data_type": "post_event_fact",
             "retrieved_at": "2026-10-29T20:00:00+08:00"}])
        assert fba.check_temporal_order(fb) == []

    def test_pre_event_input_retrieved_pre_filing_is_exempt(self, fba):
        """The report-9 correction: stripping ALL pre-filing retrievals would
        purge legitimate pre-event inputs (consensus, positioning, guidance)."""
        fb = self._fb(facts=[
            {"id": "T-3", "value": 128.22, "confidence": "Verified",
             "data_type": "pre_event_input",
             "retrieved_at": "2026-10-28T09:00:00+08:00"}])
        assert fba.check_temporal_order(fb) == []

    def test_unclassified_fact_fails_when_t1_pinned(self, fba):
        fb = self._fb(facts=[
            {"id": "T-4", "value": 40.6, "confidence": "Verified",
             "retrieved_at": "2026-10-29T20:00:00+08:00"}])
        fails = fba.check_temporal_order(fb)
        assert any("T-4" in f and "data_type" in f for f in fails), (
            "every fact must be classified when the T1 filing time is on record")

    def test_gate_silent_without_t1_timestamp(self, fba):
        fb = {"meta": {}, "facts": [
            {"id": "T-5", "value": 42.29, "confidence": "Verified",
             "retrieved_at": "2026-10-20T10:00:00-04:00"}]}
        assert fba.check_temporal_order(fb) == []

    def test_unparseable_t1_timestamp_fails(self, fba):
        fb = self._fb()
        fb["meta"]["t1_filing_timestamp"] = "not-a-date"
        fails = fba.check_temporal_order(fb)
        assert any("t1_filing_timestamp" in f and "not ISO-parseable" in f
                   for f in fails)

    def test_cross_timezone_comparison_is_exact(self, fba):
        """An aware retrieved_at in +08:00 compared against an aware T1 in
        -04:00 must compare on instant, not clock face (regression guard
        for the s[:19] offset-stripping bug)."""
        fb = self._fb(facts=[
            # 2026-10-29T04:05+08:00 == the filing instant; 08:00 is after it.
            {"id": "T-6", "value": 1.0, "confidence": "Verified",
             "data_type": "post_event_fact",
             "retrieved_at": "2026-10-29T08:00:00+08:00"}])
        assert fba.check_temporal_order(fb) == []

    def test_date_only_retrieval_on_filing_date_is_advisory(self, fba):
        fb = self._fb(facts=[
            {"id": "T-7", "value": 2.0, "confidence": "Verified",
             "data_type": "post_event_fact",
             "retrieved_at": "2026-10-28"}])
        assert fba.check_temporal_order(fb) == [], (
            "date-only retrieval landing on the filing date is a precision NOTE, "
            "not a failure — it may legitimately be post-filing")


class TestStrictPagesMode:
    """Round 3 (report-7 M-1): --strict-pages promotes unverified candidates on
    the decision-critical pages to failures, leaving furniture advisory."""

    @pytest.fixture(scope="class")
    def slides(self, tmp_path_factory):
        d = tmp_path_factory.mktemp("strictpages")
        (d / "slide_01.html").write_text(
            "<html><body><p>Exec summary: move −12.29% and an unsourced "
            "103% surprise figure.</p></body></html>", encoding="utf-8")
        (d / "slide_02.html").write_text(
            "<html><body><p>Timeline with furniture year 2026 and an unsourced "
            "98% figure.</p></body></html>", encoding="utf-8")
        return d

    @pytest.fixture(scope="class")
    def fb(self, tmp_path_factory):
        p = tmp_path_factory.mktemp("strictpagesfb") / "fb.json"
        p.write_text(json.dumps({
            "meta": {}, "facts": [
                {"id": "F-1", "value": -12.29, "slide_pages": ["slide_01.html"]},
            ]}), encoding="utf-8")
        return p

    def _run(self, fba, slides, fb, *extra):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            rp = pathlib.Path(td) / "r.json"
            code = fba.main(["--slides", str(slides), "--fact-base", str(fb),
                             "--report", str(rp), *extra])
            report = json.loads(rp.read_text())
        return code, report

    def test_strict_pages_promotes_only_named_pages(self, fba, slides, fb):
        code, report = self._run(fba, slides, fb, "--strict-pages", "slide_01.html")
        assert code == 1
        assert any("UNVERIFIED" in f and "103%" in f and "slide_01" in f
                   for f in report["failures"]), (
            "the unsourced figure on the decision-critical page must fail")
        assert not any("UNVERIFIED" in f and "98%" in f for f in report["failures"]), (
            "furniture-page candidates stay advisory without --fail-on-unverified")

    def test_unknown_strict_page_is_badref(self, fba, slides, fb):
        code, report = self._run(fba, slides, fb, "--strict-pages", "slide_99.html")
        assert any("BADREF" in f and "slide_99" in f for f in report["failures"])

    def test_default_stays_advisory(self, fba, slides, fb):
        code, report = self._run(fba, slides, fb)
        assert not any("UNVERIFIED" in f for f in report["failures"])


class TestSelftest:
    def test_module_selftest_returns_zero(self, fba):
        assert fba.selftest() == 0

    def test_cli_selftest_exits_zero(self):
        p = subprocess.run(
            [sys.executable, str(SCRIPT), "--selftest"],
            capture_output=True, text=True, cwd=str(REPO_ROOT))
        assert p.returncode == 0, p.stdout + p.stderr
        assert "SELFTEST: PASS" in p.stdout


class TestEvidenceHarness:
    """docs/skills-audit/evidence/ — the H-4 reproduction script.

    Post-fix it asserts the hole is closed: both evasion cases must exit 1
    (MISSING) and the controls must behave. It must exit 0 as a whole.
    """

    def test_evidence_harness_passes_against_fixed_script(self):
        if not EVIDENCE.exists():
            pytest.skip("evidence harness not present in this checkout")
        p = subprocess.run(
            [sys.executable, str(EVIDENCE)],
            capture_output=True, text=True, cwd=str(REPO_ROOT))
        assert p.returncode == 0, p.stdout + p.stderr
        assert "H-4" in p.stdout


class TestRound5Gates:
    """Round 5 (reports 10/11): --strict-temporal, the unconditional MANDATE
    rule, the SNAPSHOT linkage gate, and --json machine-readable output."""

    def test_strict_temporal_fails_date_only_on_filing_date(self, fba):
        fb = {"meta": {"t1_filing_timestamp": "2026-10-28T16:05:00-04:00"},
              "facts": [
            {"id": "R5-1", "value": 2.0, "confidence": "Verified",
             "data_type": "post_event_fact",
             "retrieved_at": "2026-10-28"}]}
        fails = fba.check_temporal_order(fb, strict=True)
        assert any("R5-1" in f and "TEMPORAL" in f
                   and "--strict-temporal" in f for f in fails), (
            "intraday-sensitive engagements need time-precise retrieval stamps: "
            "a same-day date-only stamp cannot distinguish pre-filing from "
            "post-filing (reports 10/11 §5.3)")

    def test_strict_temporal_keeps_time_precise_stamp_clean(self, fba):
        fb = {"meta": {"t1_filing_timestamp": "2026-10-28T16:05:00-04:00"},
              "facts": [
            {"id": "R5-2", "value": 2.0, "confidence": "Verified",
             "data_type": "post_event_fact",
             "retrieved_at": "2026-10-28T20:00:00-04:00"}]}
        assert fba.check_temporal_order(fb, strict=True) == []

    def test_declared_but_incomplete_mandate_fails_for_non_ic(self, fba):
        """Reports 10/11 §3.5: the position disclosure is unconditional once
        a position exists — audience independence was the round-4 gap."""
        fb = {"meta": {"audience": "internal research desk",
                       "mandate_context": {"fund_position": "long"}},
              "facts": []}
        fails = fba.check_mandate_context(fb)
        assert any("MANDATE" in f and "incomplete" in f for f in fails), (
            "a declared mandate_context must carry fund_position AND "
            "position_as_of whatever the audience")

    def test_complete_mandate_passes_for_non_ic(self, fba):
        fb = {"meta": {"audience": "internal research desk",
                       "mandate_context": {"fund_position": "long",
                                           "position_as_of": "2026-10-30"}},
              "facts": []}
        assert fba.check_mandate_context(fb) == []

    def test_ic_audience_still_requires_mandate(self, fba):
        fb = {"meta": {"audience": "institutional PM/IC"}, "facts": []}
        fails = fba.check_mandate_context(fb)
        assert any("MANDATE" in f and "IC audience" in f for f in fails)

    # --- SNAPSHOT linkage gate (reports 10/11 §3.4) ---

    def _snap_hash(self):
        import hashlib
        return hashlib.sha256(b"<html>Alphabet Q3 2026 8-K</html>").hexdigest()

    def _fb_with_snapshot(self):
        return {"meta": {}, "facts": [
            {"id": "S-1", "value": 282.32, "confidence": "Verified",
             "source_snapshot": self._snap_hash()}]}

    def _manifest(self, sha=None):
        return {"schema_version": 1, "tool": "source_snapshot.py",
                "snapshots": [{"url": "https://x/8k",
                               "sha256": sha or self._snap_hash()}]}

    def test_declared_snapshot_without_manifest_fails(self, fba):
        fails = fba.check_source_snapshots(self._fb_with_snapshot(), None)
        assert any("S-1" in f and "SNAPSHOT" in f
                   and "no --snapshots manifest" in f for f in fails)

    def test_linked_snapshot_passes(self, fba):
        fails = fba.check_source_snapshots(self._fb_with_snapshot(),
                                           self._manifest())
        assert fails == []

    def test_mismatched_manifest_fails(self, fba):
        fails = fba.check_source_snapshots(self._fb_with_snapshot(),
                                           self._manifest(sha="0" * 64))
        assert any("S-1" in f and "SNAPSHOT" in f
                   and "does not contain" in f for f in fails), (
            "registry <-> archive drift must fail the build")

    def test_strict_snapshots_requires_verified_facts_to_declare(self, fba):
        fb = {"meta": {}, "facts": [
            {"id": "S-2", "value": 1.0, "confidence": "Verified"},
            {"id": "S-3", "value": "-12.29%", "confidence": "Reasoned (derived)"}]}
        fails = fba.check_source_snapshots(fb, self._manifest(), strict=True)
        assert any("S-2" in f and "SNAPSHOT" in f for f in fails)
        assert not any("S-3" in f and "SNAPSHOT" in f for f in fails), (
            "strict mode binds Verified facts; derived facts are exempt")

    def test_malformed_snapshot_hash_fails(self, fba):
        fb = {"meta": {}, "facts": [
            {"id": "S-4", "value": 1.0, "confidence": "Verified",
             "source_snapshot": "not-a-hash"}]}
        fails = fba.check_source_snapshots(fb, self._manifest())
        assert any("S-4" in f and "64-hex" in f for f in fails)

    # --- --json CI mode (reports 10/11 §5.3) ---

    def test_json_mode_stdout_is_machine_readable(self, fba, tmp_path):
        import contextlib, io
        d = tmp_path
        (d / "slide_01.html").write_text(
            "<html><body><p>Close $282.32 — move −12.29%.</p></body></html>",
            encoding="utf-8")
        fb = {"meta": {}, "facts": [
            {"id": "J-1", "value": 282.32, "confidence": "Verified",
             "slide_pages": ["slide_01.html"]},
            {"id": "J-2", "value": 63.4, "confidence": "Verified",
             "slide_pages": ["slide_01.html"]}]}   # missing on the slide
        fbp = d / "fb.json"
        fbp.write_text(json.dumps(fb), encoding="utf-8")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = fba.main(["--slides", str(d), "--fact-base", str(fbp),
                             "--json"])
        payload = json.loads(buf.getvalue())
        assert code == 1
        assert payload["ok"] is False
        assert payload["failure_count"] >= 1
        assert any("J-2" in f and "MISSING" in f for f in payload["failures"])
        assert payload["tool"].startswith("fact_base_audit")

    def test_strict_snapshots_without_manifest_is_usage_error(self, tmp_path):
        d = tmp_path
        (d / "slide_01.html").write_text(
            "<html><body><p>Close $282.32.</p></body></html>", encoding="utf-8")
        fb = {"meta": {}, "facts": [
            {"id": "U-1", "value": 282.32, "confidence": "Verified",
             "slide_pages": ["slide_01.html"]}]}
        fbp = d / "fb.json"
        fbp.write_text(json.dumps(fb), encoding="utf-8")
        p = subprocess.run(
            [sys.executable, str(SCRIPT), "--slides", str(d),
             "--fact-base", str(fbp), "--strict-snapshots"],
            capture_output=True, text=True, cwd=str(REPO_ROOT))
        assert p.returncode == 2, (
            "--strict-snapshots without --snapshots is a usage error, "
            "not a silent no-op")
