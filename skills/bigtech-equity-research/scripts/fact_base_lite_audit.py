#!/usr/bin/env python3
"""fact_base_lite_audit.py — machine-checked number registry for the single-file note.

Comparative reports 6/7 (finding H-4/H-5, "lite-variant verification gap" /
"credibility spillover"): big-tech-earnings-postmortem executed the family doctrine but
shipped only placeholder + disclosure + render gates — nothing machine-checked that the
numbers on the delivered note trace to sources, while the note LOOKED indistinguishable
from a flagship deliverable (confidence tags, verification-status line). This gate is
the preferred fix: a minimal fact-base registry for the lightweight variant, so even the
fastest-ship member has a machine-checked number trail.

What it enforces on the delivered note + its registry (fact_base_lite.json):

  1. Placeholder scan (always, visible text only — same tokens as the family).
  2. Schema check: every registry fact carries id, metric, value, source_name,
     source_url, retrieved_at, and a confidence label from the family taxonomy
     (Verified / Reasoned / Assumed / Unverifiable).
  3. Forward check: every fact's numeric tokens must appear in the note (anchored,
     sign/symbol-tolerant matching — a digit substring of a longer printed number never
     satisfies a fact; same matcher discipline as the flagship's fact_base_audit.py).
  4. Reverse check: every money/percentage figure printed in the note must be covered
     by a registry entry — uncovered figures are UNREGISTERED failures (this is the
     number-registry gate; it fails closed by design). Benign repeated tokens
     (years, section numbers) can be whitelisted via meta.furniture in the registry or
     --furniture "2026,Q3" on the command line; keep the whitelist short and justified.
  5. CONSENSUS check (round 4, reports 8/9 M-1): consensus-side registry facts
     (is_consensus flag, or a metric naming consensus/estimate/whisper) must carry
     consensus_provider, consensus_vintage, and consensus_statistic in
     {mean, median, undisclosed} — mean-vs-median is now a recorded disclosure,
     not a courtesy. "undisclosed" is a valid entry for outlets that do not say
     which statistic they print; the point is that the recorder had to look.
  6. TEMPORAL check (round 4, reports 8/9 M-6, report-9-corrected design): when
     meta.t1_filing_timestamp is set (the verified T1 filing/publication time),
     every registry fact must declare data_type in {pre_event_input,
     post_event_fact}, and every post_event_fact must carry retrieved_at >= the
     T1 timestamp. A post-event claim retrieved before the filing is pre-filing
     contamination — flag it Unverifiable and strip it from the registry. This is
     a DATA-INTEGRITY control (never launder unconfirmed pre-filing chatter into
     a confirmed fact), not a Reg FD control: pre_event_input entries (consensus,
     positioning, prior guidance, options OI) legitimately predate the event and
     are exempt. Date-only retrieved_at on the filing date itself is a NOTE
     (timestamp precision insufficient), not a failure — unless --strict-temporal
     (round 5, reports 10/11) is passed, which fails it: intraday-sensitive
     engagements need time-precise retrieval stamps. The gate is silent when
     meta.t1_filing_timestamp is absent.
  7. MANDATE check (round 5, reports 10/11 §3.5): an IC-named meta.audience
     requires meta.mandate_context (fund_position + position_as_of) — and a
     DECLARED mandate_context must be complete regardless of audience. A
     position disclosure does not become optional because the deliverable
     happens to face a non-IC audience (CFA Institute Standard I(B):
     unconditional once a position exists).
  8. SNAPSHOT check (round 5, reports 10/11 — internal consistency vs source
     truth): the registry audit verifies the note matches the registry; it does
     NOT verify the registry matches the cited source. Facts may carry
     `source_snapshot` (the SHA-256 of the fetched source content, recorded by
     scripts/source_snapshot.py --record). With --snapshots <manifest> every
     declared hash must exist in the manifest (registry <-> manifest linkage);
     with --strict-snapshots every `Verified` fact must declare one. Without a
     manifest the run prints the standing limitation NOTE — internal
     consistency, not source truth.

Usage:
  python3 fact_base_lite_audit.py --note <note.html> --fact-base <fact_base_lite.json>
  python3 fact_base_lite_audit.py --note <note.html> --fact-base <fb.json> \
      --furniture "2026,2027"
  python3 fact_base_lite_audit.py --note <note.html> --fact-base <fb.json> \
      --snapshots source_snapshots.json [--strict-snapshots] [--strict-temporal]
  python3 fact_base_lite_audit.py --note <note.html> --fact-base <fb.json> --json
  python3 fact_base_lite_audit.py --selftest

--json (round 5, reports 10/11 — CI/CD integration): stdout carries a
machine-readable summary {"tool", "ok", "failure_count", "failures", "flags"};
the human-readable PASS/NOTE diagnostics go to stderr so pipelines can consume
stdout directly. Exit codes unchanged.

Exit codes: 0 clean, 1 failures found, 2 usage/environment error.
"""
import argparse
import json
import re
import sys
import tempfile
import pathlib
from datetime import date, datetime

TOOL_ID = "fact_base_lite_audit.py (big-tech research family, round 5)"

PLACEHOLDER_PATTERNS = [
    r"lorem", r"\btodo\b", r"placeholder", r"\btbd\b", r"\bxxx\b", r"\bnan\b",
    r"\bundefined\b", r"insert (data|here|numbers)", r"foo bar", r"【",
]
NUM_RE = re.compile(r"-?\d[\d,]*(?:\.\d+)?")
EXTRACT_RE = re.compile(r"\$\d[\d,\.]*\s?[BM]?|\d+\.\d+%?|\d{2,}%")
CONFIDENCE_LABELS = {"Verified", "Reasoned", "Assumed", "Unverifiable",
                     "Reasoned (derived)", "Reasoned (judged)"}
DATA_TYPES = {"pre_event_input", "post_event_fact"}
CONSENSUS_STATISTICS = {"mean", "median", "undisclosed"}


def norm(s: str) -> str:
    """Normalize dashes (hyphen/en/em/minus), NBSP, apostrophes, whitespace; lowercase."""
    s = (s.replace("\u2013", "-").replace("\u2014", "-")
          .replace("\u2212", "-").replace("\u00a0", " ").replace("\u2019", "'"))
    return re.sub(r"\s+", " ", s).strip().lower()


def visible_text(html: str) -> str:
    """Strip <script>/<style> and tags — audit only what readers see."""
    html = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    return re.sub(r"<[^>]+>", " ", html)


def numeric_tokens(value) -> list:
    """Extract number tokens from a fact value for presence matching."""
    if isinstance(value, bool) or value is None:
        return []
    s = str(value)
    if not NUM_RE.search(s):
        return []
    out = []
    for tok in NUM_RE.findall(s):
        tok = tok.replace(",", "").rstrip(".")
        if tok not in ("", "-", "."):
            out.append(tok)
    return out


def hay_tokens(hay_norm: str) -> set:
    """Complete number tokens in normalized note text, with $ % + stripped (anchored)."""
    hay2 = re.sub(r"[$%,+]", "", hay_norm)
    return {t.replace(",", "").rstrip(".")
            for t in NUM_RE.findall(hay2)
            if t.replace(",", "").rstrip(".") not in ("", "-", ".")}


def token_in(tok: str, hay_norm: str) -> bool:
    """Sign/symbol-tolerant ANCHORED token presence (flagship matcher discipline)."""
    toks = hay_tokens(hay_norm)
    if tok in toks or tok.lstrip("-") in toks:
        return True
    try:
        tv = float(tok)
    except ValueError:
        return False
    return any(float(t) == tv for t in toks)


def scan_placeholders(fname: str, raw_html: str) -> list:
    fails = []
    low = norm(visible_text(raw_html))
    for pat in PLACEHOLDER_PATTERNS:
        if re.search(pat, low):
            fails.append(f"PLACEHOLDER  {fname}  matches /{pat}/")
    return fails


def check_registry_schema(fb: dict) -> list:
    """Every registry fact is complete enough to be a number trail."""
    fails = []
    facts = fb.get("facts", [])
    if not isinstance(facts, list) or not facts:
        return ["SCHEMA       registry has no facts — register every money/percentage "
                "figure the note prints before assembling the HTML"]
    for fact in facts:
        fid = str(fact.get("id", "?"))
        for field in ("metric", "value", "source_name", "source_url", "retrieved_at"):
            if not str(fact.get(field, "")).strip():
                fails.append(f"SCHEMA       {fid}  missing required field '{field}'")
        conf = str(fact.get("confidence", "")).strip()
        if conf not in CONFIDENCE_LABELS:
            fails.append(f"SCHEMA       {fid}  confidence {conf!r} is not one of "
                         f"{sorted(CONFIDENCE_LABELS)}")
    return fails


def _is_consensus_fact(fact: dict) -> bool:
    """Same routing rule as the flagship's CONSENSUS gate."""
    if fact.get("is_consensus") is True:
        return True
    metric = str(fact.get("metric", "")).lower()
    return any(k in metric for k in ("consensus", "estimate", "whisper"))


def check_consensus_facts(fb: dict) -> list:
    """Lite CONSENSUS gate (round 4, reports 8/9 M-1): provider + vintage +
    recorded mean-vs-median statistic on every consensus-side registry fact."""
    fails = []
    for fact in fb.get("facts", []):
        if not _is_consensus_fact(fact):
            continue
        fid = str(fact.get("id", "?"))
        missing = [f for f in ("consensus_provider", "consensus_vintage",
                               "consensus_statistic")
                   if not str(fact.get(f, "")).strip()]
        if missing:
            fails.append(f"CONSENSUS    {fid}  consensus-side fact missing: "
                         + ", ".join(missing)
                         + " (mean vs median is a recorded disclosure, not a "
                           "courtesy — use 'undisclosed' only when the outlet "
                           "genuinely does not say)")
            continue
        stat = str(fact.get("consensus_statistic", "")).strip().lower()
        if stat not in CONSENSUS_STATISTICS:
            fails.append(f"CONSENSUS    {fid}  consensus_statistic {stat!r} is not "
                         f"one of {sorted(CONSENSUS_STATISTICS)}")
        else:
            if stat == "undisclosed":
                # Round 5, reports 10/11 §5.7: 'undisclosed' is honest but weaker
                # than a licensed point-in-time feed — surface the residual gap.
                print(f"NOTE   {fid}  consensus_statistic is 'undisclosed' — the "
                      "outlet does not say which statistic it prints; log the "
                      "licensed-feed pull needed to close the gap in the "
                      "Data-Gap Ledger")
            print(f"PASS   {fid}  consensus carries provider + vintage "
                  f"({fact.get('consensus_provider')}, "
                  f"{fact.get('consensus_statistic')})")
    return fails


def _parse_moment(raw):
    """Best-effort ISO parse -> (value, has_time). value is an aware/naive
    datetime or a date; None when unparseable. Timezone offsets are kept
    (aware-vs-aware comparison is exact across offsets); date-only strings
    parse to a date and compare at date granularity."""
    s = str(raw or "").strip()
    if not s:
        return None, False
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    try:
        v = datetime.fromisoformat(s)      # date-only -> midnight datetime
        return v, len(s) > 10
    except ValueError:
        pass
    try:
        return date.fromisoformat(s[:10]), False
    except ValueError:
        return None, False


def check_temporal_order(fb: dict, strict: bool = False) -> list:
    """TEMPORAL gate (round 4, reports 8/9 M-6, report-9-corrected design).

    Active only when meta.t1_filing_timestamp is set (the verified T1
    filing/publication time). Enforces, per fact: a data_type classification
    in {pre_event_input, post_event_fact}; and for post_event_fact entries,
    retrieved_at >= the T1 timestamp. Pre-filing retrieval of a post-event
    claim is contamination: flag it Unverifiable and strip it from the
    registry. Pre-event inputs (consensus, positioning, prior guidance,
    options OI) legitimately predate the event and are exempt by design.
    Date-only retrieved_at landing on the filing date is a precision NOTE,
    not a failure — with strict=True (round 5, reports 10/11 --strict-temporal)
    it fails instead: intraday-sensitive engagements require time-precise
    retrieval stamps (a same-day date-only stamp cannot distinguish a
    pre-filing pull from a post-filing one). A data-integrity control, not
    a Reg FD control."""
    meta = fb.get("meta", {}) or {}
    t1_raw = str(meta.get("t1_filing_timestamp", "")).strip()
    if not t1_raw:
        return []          # gate opted out: no verified T1 timestamp on record
    t1, t1_has_time = _parse_moment(t1_raw)
    if t1 is None:
        return ["TEMPORAL    meta.t1_filing_timestamp is not ISO-parseable — "
                "pin the verified T1 filing time as YYYY-MM-DD[THH:MM:SS] or "
                "remove it to disable the gate"]
    fails = []
    for fact in fb.get("facts", []):
        fid = str(fact.get("id", "?"))
        dtype = str(fact.get("data_type", "")).strip().lower()
        if dtype not in DATA_TYPES:
            fails.append(f"TEMPORAL    {fid}  missing/invalid data_type "
                         f"{dtype or '(absent)'} — classify every registry fact "
                         "pre_event_input or post_event_fact when the T1 filing "
                         "time is on record")
            continue
        if dtype != "post_event_fact":
            continue       # pre-event inputs legitimately predate the event
        ret, ret_has_time = _parse_moment(fact.get("retrieved_at", ""))
        if ret is None:
            fails.append(f"TEMPORAL    {fid}  retrieved_at is not ISO-parseable — "
                         "a post_event_fact needs a usable retrieval timestamp")
            continue
        exact = t1_has_time and ret_has_time
        try:
            if exact:
                ordered = ret >= t1
            else:            # date-level comparison at best available precision
                ordered = (ret.date() if hasattr(ret, "date") else ret) >= \
                          (t1.date() if hasattr(t1, "date") else t1)
        except TypeError:    # mixed aware/naive datetimes — fall back to dates
            ordered = (ret.date() if hasattr(ret, "date") else ret) >= \
                      (t1.date() if hasattr(t1, "date") else t1)
        if ordered:
            if not exact and (ret.date() if hasattr(ret, "date") else ret) == \
                    (t1.date() if hasattr(t1, "date") else t1):
                if strict:
                    fails.append(f"TEMPORAL    {fid}  retrieved_at is date-only on "
                                 "the filing date — --strict-temporal: an "
                                 "intraday-sensitive engagement needs a "
                                 "time-precise retrieval stamp (YYYY-MM-"
                                 "DDTHH:MM:SS) to prove the pull came at/after "
                                 "the verified filing time")
                else:
                    print(f"NOTE   {fid}  retrieved_at is date-only on the filing "
                          "date — timestamp precision would make the temporal "
                          "check exact")
            else:
                print(f"PASS   {fid}  post_event_fact retrieved at/after the T1 "
                      "filing time")
        else:
            fails.append(f"TEMPORAL    {fid}  post_event_fact retrieved_at "
                         f"{fact.get('retrieved_at')} precedes the verified T1 "
                         f"filing time {t1_raw} — pre-filing contamination: tag "
                         "the fact Unverifiable and strip it from the registry")
    return fails


def check_mandate_context(fb: dict) -> list:
    """Lite MANDATE check (round 5, reports 10/11 §3.5).

    The checks.json needle enforces the disclosure TEXT on IC-facing notes;
    this registry-side check enforces the DATA. Two triggers:
      - meta.audience names an IC -> meta.mandate_context with fund_position +
        position_as_of is required (round-3 doctrine, flagship parity);
      - meta.mandate_context is declared at all -> it must be complete,
        whatever the audience. A position disclosure is unconditional once a
        position exists (CFA Institute Standard I(B) / Advisers Act fiduciary
        duty) — it does not get to be optional because the deliverable happens
        to face a non-IC audience. A partially-declared block is the worst
        state: it hints at a position while omitting the as-of date that makes
        it interpretable."""
    meta = fb.get("meta", {}) or {}
    audience = meta.get("audience", "")
    if isinstance(audience, list):
        audience = " ".join(str(a) for a in audience)
    ic_facing = bool(re.search(r"\b(ic|investment[\s-]committee)\b",
                               str(audience).lower()))
    mc = meta.get("mandate_context")
    mc = mc if isinstance(mc, dict) else {}
    declared = any(str(v).strip() for v in mc.values())
    if not ic_facing and not declared:
        return []          # no IC audience, nothing declared — nothing to enforce
    if not str(mc.get("fund_position", "")).strip() \
            or not str(mc.get("position_as_of", "")).strip():
        if ic_facing:
            return ["MANDATE      meta.audience names an IC audience but "
                    "meta.mandate_context is absent or incomplete — an "
                    "IC-facing deliverable must disclose fund_position (long/"
                    "short/none/undetermined) and position_as_of"]
        return ["MANDATE      meta.mandate_context is present but incomplete — "
                "fund_position AND position_as_of are required once any "
                "mandate context is declared (round 5, reports 10/11: the "
                "position disclosure is unconditional whatever the audience); "
                "complete the block or remove it"]
    print(f"PASS   mandate_context present (fund_position: "
          f"{mc.get('fund_position')}, as of {mc.get('position_as_of')})")
    return []


def check_source_snapshots(fb: dict, manifest: dict = None,
                           strict: bool = False) -> list:
    """SNAPSHOT check (round 5, reports 10/11 — internal consistency vs source truth).

    This audit verifies the note matches the registry; it does NOT verify the
    registry matches the cited source document — a fact entry with a wrong
    figure and a valid-looking URL passes every other gate (report 11 §3.4,
    conceded by report 10's synthesis). Facts close that gap by carrying
    `source_snapshot`: the SHA-256 of the fetched source content, recorded by
    scripts/source_snapshot.py --record into a manifest passed via
    --snapshots. This check enforces the registry <-> manifest linkage:
      - a declared hash missing from the manifest fails (registry drift);
      - --strict-snapshots: every `Verified` fact must declare a snapshot
        (opt-in like the family's other strict modes — routine T3 price pulls
        may not warrant archiving; decision-critical T1 pulls do);
      - without a manifest, a declared snapshot fails (unverifiable claim),
        and a run with no snapshots at all prints the standing limitation
        NOTE so the gap is visible in every log, never silent.
    Content-file integrity (does the saved file still hash to the recorded
    digest?) is source_snapshot.py --verify's job; this gate stays a
    deterministic offline check."""
    fails = []
    facts = fb.get("facts", [])
    hashes_in_manifest = set()
    if manifest is not None:
        for s in manifest.get("snapshots", []):
            h = str(s.get("sha256", "")).strip().lower()
            if h:
                hashes_in_manifest.add(h)
    declared_any = False
    for fact in facts:
        fid = str(fact.get("id", "?"))
        h = str(fact.get("source_snapshot", "")).strip().lower()
        if not h:
            if strict and str(fact.get("confidence", "")).strip() \
                    .lower().startswith("verified"):
                fails.append(f"SNAPSHOT    {fid}  Verified fact carries no "
                             "source_snapshot — --strict-snapshots: every "
                             "Verified figure needs the SHA-256 of its fetched "
                             "source (scripts/source_snapshot.py --record)")
            continue
        declared_any = True
        if not re.fullmatch(r"[0-9a-f]{64}", h):
            fails.append(f"SNAPSHOT    {fid}  source_snapshot {h[:16]!r} is not a "
                         "64-hex SHA-256 — record it with "
                         "scripts/source_snapshot.py --record")
            continue
        if manifest is None:
            fails.append(f"SNAPSHOT    {fid}  declares source_snapshot "
                         f"sha256:{h[:12]} but no --snapshots manifest was "
                         "passed — re-run with --snapshots "
                         "source_snapshots.json to verify the linkage")
            continue
        if h not in hashes_in_manifest:
            fails.append(f"SNAPSHOT    {fid}  declares source_snapshot "
                         f"sha256:{h[:12]} which the manifest does not contain "
                         "— the registry and the snapshot archive drifted "
                         "apart; re-record the source or fix the reference")
        else:
            print(f"PASS   {fid}  source_snapshot sha256:{h[:12]} linked")
    if manifest is not None:
        referenced = {str(f.get("source_snapshot", "")).strip().lower()
                      for f in facts}
        for s in manifest.get("snapshots", []):
            h = str(s.get("sha256", "")).strip().lower()
            if h and h not in referenced:
                print(f"NOTE   orphan snapshot sha256:{h[:12]} "
                      f"({s.get('url', '?')}) referenced by no registry fact — "
                      "prune it or register the fact it supports")
    elif not declared_any and not strict:
        print("NOTE   no source snapshots on record — this audit certifies "
              "internal consistency, not source truth (reports 10/11 §3.4); "
              "snapshot decision-critical T1 sources with "
              "scripts/source_snapshot.py --record to close the gap")
    return fails


def check_forward(fname: str, raw_html: str, fb: dict) -> list:
    """Every registry number must actually appear in the note."""
    fails = []
    body = norm(visible_text(raw_html))
    for fact in fb.get("facts", []):
        fid = str(fact.get("id", "?"))
        toks = numeric_tokens(fact.get("value"))
        for tok in toks:
            if token_in(tok, body):
                print(f"PASS   {fid}  '{tok}' present in the note")
            else:
                fails.append(f"MISSING     {fid}  token '{tok}' registered but not "
                             "printed in the note (prune the registry or fix the note)")
    return fails


def check_reverse(fname: str, raw_html: str, fb: dict, furniture: set) -> list:
    """Every money/percentage figure in the note must be registered (fails closed).

    Sign-tolerant: a registry entry of -12.29 covers a printed '−12.29%'; whitelisted
    furniture tokens are exempt with a NOTE so the exemption is visible in the log."""
    fails = []
    covered = set()
    for fact in fb.get("facts", []):
        covered.update(numeric_tokens(fact.get("value")))
    body = visible_text(raw_html)
    for m in EXTRACT_RE.finditer(body):
        disp = m.group(0).strip()
        tok = disp.replace(",", "").replace("$", "").replace("%", "")
        tok = tok.rstrip("BMK.").rstrip(".")
        if not tok:
            continue
        if tok in furniture or ("-" + tok) in furniture:
            print(f"NOTE   '{disp}' whitelisted as benign furniture "
                  "(years / section numbers)")
            continue
        if tok in covered or ("-" + tok) in covered:
            continue
        try:
            if float(tok) == 0:
                continue
        except ValueError:
            continue
        fails.append(f"UNREGISTERED note figure '{disp}' has no registry entry — "
                     "add it to fact_base_lite.json with a source (or whitelist it "
                     "as furniture with a justification)")
    return fails


def selftest() -> int:
    with tempfile.TemporaryDirectory() as td:
        d = pathlib.Path(td)
        (d / "note_ok.html").write_text(
            "<html><body><h1>GOOG —12.29%</h1>"
            "<p>Close $282.32; revenue $127.58B vs $128.22B consensus.</p>"
            "</body></html>", encoding="utf-8")
        fb = {"meta": {"furniture": []}, "facts": [
            {"id": "L-1", "metric": "close", "value": 282.32, "source_name": "Yahoo",
             "source_url": "https://x", "retrieved_at": "2026-10-30",
             "confidence": "Verified"},
            {"id": "L-2", "metric": "move", "value": "-12.29%", "source_name": "computed",
             "source_url": "n/a", "retrieved_at": "2026-10-30",
             "confidence": "Reasoned (derived)"},
            {"id": "L-3", "metric": "revenue actual", "value": 127.58,
             "source_name": "press release", "source_url": "https://x",
             "retrieved_at": "2026-10-30", "confidence": "Verified"},
            {"id": "L-4", "metric": "revenue consensus", "value": 128.22,
             "source_name": "LSEG via Reuters", "source_url": "https://x",
             "retrieved_at": "2026-10-30", "confidence": "Verified",
             "consensus_provider": "LSEG", "consensus_vintage": "2026-10-28",
             "consensus_statistic": "mean"},
        ]}
        (d / "fb_ok.json").write_text(json.dumps(fb), encoding="utf-8")
        code_ok = main(["--note", str(d / "note_ok.html"),
                        "--fact-base", str(d / "fb_ok.json")])
        # Unregistered figure on the note -> UNREGISTERED failure (only failure).
        (d / "note_extra.html").write_text(
            "<html><body><p>GOOG —12.29% to $282.32; revenue $127.58B vs $128.22B "
            "consensus; erased $482B.</p></body></html>", encoding="utf-8")
        code_extra = main(["--note", str(d / "note_extra.html"),
                           "--fact-base", str(d / "fb_ok.json")])
        # Furniture whitelist: the note prints a rounded "−12%" executive-summary
        # form of a registered "−12.29%" — whitelisting "12" acknowledges the
        # rounding instead of registering a duplicate fact.
        (d / "note_furn.html").write_text(
            "<html><body><p>Close $282.32 (−12% headline form).</p></body></html>",
            encoding="utf-8")
        fb_furn = {"meta": {"furniture": []}, "facts": [fb["facts"][0]]}
        (d / "fb_furn.json").write_text(json.dumps(fb_furn), encoding="utf-8")
        code_furn = main(["--note", str(d / "note_furn.html"),
                          "--fact-base", str(d / "fb_furn.json"),
                          "--furniture", "12"])
        # Missing source fields -> SCHEMA failure.
        fb_bad = {"meta": {}, "facts": [
            {"id": "L-9", "metric": "close", "value": 282.32}]}
        (d / "fb_bad.json").write_text(json.dumps(fb_bad), encoding="utf-8")
        code_bad = main(["--note", str(d / "note_ok.html"),
                         "--fact-base", str(d / "fb_bad.json")])
        # Round 4 — CONSENSUS: a consensus-side fact without the recorded
        # provider/vintage/statistic fails (mean vs median is a disclosure).
        fb_cons = {"meta": {}, "facts": [
            {"id": "L-10", "metric": "EPS consensus", "value": 3.02,
             "source_name": "Reuters", "source_url": "https://x",
             "retrieved_at": "2026-10-30", "confidence": "Verified"}]}
        (d / "fb_cons.json").write_text(json.dumps(fb_cons), encoding="utf-8")
        r_cons = d / "r_cons.json"
        code_cons = main(["--note", str(d / "note_ok.html"),
                          "--fact-base", str(d / "fb_cons.json"),
                          "--report", str(r_cons)])
        rep_cons = json.loads(r_cons.read_text()) if r_cons.exists() else {
            "failures": []}
        # Round 4 — TEMPORAL (clean): t1 filing time on record; every fact
        # classified; the post-event fact retrieved after the filing; the
        # pre-event consensus legitimately predates it.
        fb_temp_ok = {"meta": {"t1_filing_timestamp": "2026-10-28T16:05:00-04:00"},
                      "facts": [
            {"id": "L-11", "metric": "close", "value": 282.32,
             "source_name": "Yahoo", "source_url": "https://x",
             "retrieved_at": "2026-10-29T20:00:00+08:00", "confidence": "Verified",
             "data_type": "post_event_fact"},
            {"id": "L-12", "metric": "revenue consensus", "value": 128.22,
             "source_name": "LSEG via Reuters", "source_url": "https://x",
             "retrieved_at": "2026-10-28T09:00:00+08:00", "confidence": "Verified",
             "data_type": "pre_event_input",
             "consensus_provider": "LSEG", "consensus_vintage": "2026-10-28",
             "consensus_statistic": "mean"},
            {"id": "L-15", "metric": "revenue actual", "value": 127.58,
             "source_name": "press release", "source_url": "https://x",
             "retrieved_at": "2026-10-29T20:00:00+08:00", "confidence": "Verified",
             "data_type": "post_event_fact"},
            {"id": "L-16", "metric": "move", "value": "-12.29%",
             "source_name": "computed", "source_url": "n/a",
             "retrieved_at": "2026-10-29T20:00:00+08:00",
             "confidence": "Reasoned (derived)", "data_type": "post_event_fact"}]}
        (d / "fb_temp_ok.json").write_text(json.dumps(fb_temp_ok),
                                             encoding="utf-8")
        code_temp_ok = main(["--note", str(d / "note_ok.html"),
                             "--fact-base", str(d / "fb_temp_ok.json")])
        # Round 4 — TEMPORAL (dirty): a post_event_fact retrieved before the
        # verified filing time (pre-filing contamination), an unclassified
        # fact, and a bad statistic — all must fail.
        fb_temp_bad = {"meta": {"t1_filing_timestamp": "2026-10-28T16:05:00-04:00"},
                       "facts": [
            {"id": "L-13", "metric": "close", "value": 282.32,
             "source_name": "Yahoo", "source_url": "https://x",
             "retrieved_at": "2026-10-28T10:00:00-04:00", "confidence": "Verified",
             "data_type": "post_event_fact"},
            {"id": "L-14", "metric": "move", "value": "-12.29%",
             "source_name": "computed", "source_url": "n/a",
             "retrieved_at": "2026-10-29", "confidence": "Reasoned (derived)"}]}
        (d / "fb_temp_bad.json").write_text(json.dumps(fb_temp_bad),
                                              encoding="utf-8")
        r_temp = d / "r_temp.json"
        code_temp_bad = main(["--note", str(d / "note_ok.html"),
                              "--fact-base", str(d / "fb_temp_bad.json"),
                              "--report", str(r_temp)])
        rep_temp = json.loads(r_temp.read_text()) if r_temp.exists() else {
            "failures": []}
        # Round 5 — STRICT-TEMPORAL: date-only retrieved_at on the filing date
        # is a NOTE by default (clean exit) but FAILS under --strict-temporal
        # (intraday-sensitive engagement). All four note figures stay covered
        # so the exit codes isolate the temporal behavior.
        fb_temp_date = {"meta": {"t1_filing_timestamp": "2026-10-28T16:05:00-04:00"},
                        "facts": [
            {"id": "L-17", "metric": "close", "value": 282.32,
             "source_name": "Yahoo", "source_url": "https://x",
             "retrieved_at": "2026-10-28", "confidence": "Verified",
             "data_type": "post_event_fact"},
            {"id": "L-12", "metric": "revenue consensus", "value": 128.22,
             "source_name": "LSEG via Reuters", "source_url": "https://x",
             "retrieved_at": "2026-10-28T09:00:00+08:00", "confidence": "Verified",
             "data_type": "pre_event_input",
             "consensus_provider": "LSEG", "consensus_vintage": "2026-10-28",
             "consensus_statistic": "mean"},
            {"id": "L-15", "metric": "revenue actual", "value": 127.58,
             "source_name": "press release", "source_url": "https://x",
             "retrieved_at": "2026-10-28", "confidence": "Verified",
             "data_type": "post_event_fact"},
            {"id": "L-16", "metric": "move", "value": "-12.29%",
             "source_name": "computed", "source_url": "n/a",
             "retrieved_at": "2026-10-28", "confidence": "Reasoned (derived)",
             "data_type": "post_event_fact"}]}
        (d / "fb_temp_date.json").write_text(json.dumps(fb_temp_date),
                                               encoding="utf-8")
        code_temp_note = main(["--note", str(d / "note_ok.html"),
                               "--fact-base", str(d / "fb_temp_date.json")])
        r_st = d / "r_st.json"
        code_temp_strict = main(["--note", str(d / "note_ok.html"),
                                 "--fact-base", str(d / "fb_temp_date.json"),
                                 "--strict-temporal", "--report", str(r_st)])
        rep_st = json.loads(r_st.read_text()) if r_st.exists() else {
            "failures": []}
        # Round 5 — MANDATE (lite): a declared-but-incomplete mandate_context
        # fails even with NO IC audience (position disclosure is unconditional
        # once declared); a complete one passes. All four facts stay registered
        # so the exit codes isolate the mandate behavior.
        fb_mand_bad = {"meta": {"mandate_context": {"fund_position": "long"}},
                       "facts": fb["facts"]}
        (d / "fb_mand_bad.json").write_text(json.dumps(fb_mand_bad),
                                             encoding="utf-8")
        code_mand_bad = main(["--note", str(d / "note_ok.html"),
                              "--fact-base", str(d / "fb_mand_bad.json")])
        fb_mand_ok = {"meta": {"mandate_context": {"fund_position": "long",
                                                   "position_as_of": "2026-10-30"}},
                      "facts": fb["facts"]}
        (d / "fb_mand_ok.json").write_text(json.dumps(fb_mand_ok),
                                            encoding="utf-8")
        code_mand_ok = main(["--note", str(d / "note_ok.html"),
                             "--fact-base", str(d / "fb_mand_ok.json")])
        # Round 5 — SNAPSHOT: a fact declaring source_snapshot without a
        # manifest fails; with a matching manifest it links clean; strict mode
        # requires every Verified fact to declare one. The dedicated note
        # prints exactly the two registered figures.
        (d / "note_snap.html").write_text(
            "<html><body><h1>GOOG —12.29%</h1>"
            "<p>Revenue $127.58B.</p></body></html>", encoding="utf-8")
        import hashlib
        content = "<html>Alphabet Q3 2026 press release — revenue $127.58B</html>"
        snap_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
        (d / "press.html").write_text(content, encoding="utf-8")
        manifest = {"schema_version": 1, "tool": "source_snapshot.py",
                    "snapshots": [{"url": "https://x/press", "source_name": "IR",
                                   "fetched_at_utc": "2026-10-29T00:00:00Z",
                                   "content_path": str(d / "press.html"),
                                   "sha256": snap_hash, "bytes": len(content)}]}
        (d / "source_snapshots.json").write_text(json.dumps(manifest),
                                                   encoding="utf-8")
        fb_snap = {"meta": {}, "facts": [
            {"id": "L-18", "metric": "revenue actual", "value": 127.58,
             "source_name": "press release", "source_url": "https://x/press",
             "retrieved_at": "2026-10-30", "confidence": "Verified",
             "source_snapshot": snap_hash},
            {"id": "L-19", "metric": "move", "value": "-12.29%",
             "source_name": "computed", "source_url": "n/a",
             "retrieved_at": "2026-10-30", "confidence": "Reasoned (derived)"}]}
        (d / "fb_snap.json").write_text(json.dumps(fb_snap), encoding="utf-8")
        code_snap_nomani = main(["--note", str(d / "note_snap.html"),
                                 "--fact-base", str(d / "fb_snap.json")])
        code_snap_ok = main(["--note", str(d / "note_snap.html"),
                             "--fact-base", str(d / "fb_snap.json"),
                             "--snapshots", str(d / "source_snapshots.json")])
        code_snap_strict_noargs = main(
            ["--note", str(d / "note_snap.html"),
             "--fact-base", str(d / "fb_snap.json"), "--strict-snapshots"])
        code_snap_strict = main(
            ["--note", str(d / "note_snap.html"),
             "--fact-base", str(d / "fb_snap.json"),
             "--snapshots", str(d / "source_snapshots.json"),
             "--strict-snapshots"])
        # and a mismatched manifest entry -> linkage failure
        manifest_bad = json.loads(json.dumps(manifest))
        manifest_bad["snapshots"][0]["sha256"] = "0" * 64
        (d / "source_snapshots_bad.json").write_text(json.dumps(manifest_bad),
                                                       encoding="utf-8")
        r_snap = d / "r_snap.json"
        code_snap_bad = main(["--note", str(d / "note_snap.html"),
                              "--fact-base", str(d / "fb_snap.json"),
                              "--snapshots", str(d / "source_snapshots_bad.json"),
                              "--report", str(r_snap)])
        rep_snap = json.loads(r_snap.read_text()) if r_snap.exists() else {
            "failures": []}
        # Round 5 — --json: stdout is a machine-readable summary.
        import contextlib, io
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code_json = main(["--note", str(d / "note_extra.html"),
                              "--fact-base", str(d / "fb_ok.json"), "--json"])
        try:
            payload = json.loads(buf.getvalue())
            json_ok = (payload.get("ok") is False
                       and payload.get("failure_count", 0) >= 1
                       and payload.get("tool", "").startswith(
                           "fact_base_lite_audit"))
        except json.JSONDecodeError:
            json_ok = False
        buf2 = io.StringIO()
        with contextlib.redirect_stdout(buf2):
            code_json_clean = main(["--note", str(d / "note_ok.html"),
                                    "--fact-base", str(d / "fb_ok.json"),
                                    "--json"])
        try:
            payload2 = json.loads(buf2.getvalue())
            json_clean = payload2.get("ok") is True
        except json.JSONDecodeError:
            json_clean = False
        ok = (code_ok == 0 and code_extra == 1 and code_furn == 0
              and code_bad == 1 and code_cons == 1
              and any("L-10" in f and "CONSENSUS" in f
                      for f in rep_cons["failures"])
              and code_temp_ok == 0 and code_temp_bad == 1
              and any("L-13" in f and "TEMPORAL" in f
                      for f in rep_temp["failures"])
              and any("L-14" in f and "data_type" in f
                      for f in rep_temp["failures"])
              and code_temp_note == 0 and code_temp_strict == 1
              and any("L-17" in f and "TEMPORAL" in f
                      for f in rep_st["failures"])
              and code_mand_bad == 1 and code_mand_ok == 0
              and code_snap_nomani == 1 and code_snap_ok == 0
              and code_snap_strict_noargs == 2 and code_snap_strict == 0
              and code_snap_bad == 1
              and any("L-18" in f and "SNAPSHOT" in f
                      for f in rep_snap["failures"])
              and code_json == 1 and json_ok
              and code_json_clean == 0 and json_clean)
        print("=" * 60)
        print("SELFTEST:", "PASS" if ok else "FAIL",
              f"(clean {code_ok}, unregistered {code_extra}, "
              f"furniture {code_furn}, schema {code_bad}, consensus {code_cons}, "
              f"temporal-clean {code_temp_ok}, temporal-dirty {code_temp_bad}, "
              f"strict-temporal {code_temp_note}->{code_temp_strict}, "
              f"mandate {code_mand_bad}/{code_mand_ok}, "
              f"snapshots {code_snap_nomani}/{code_snap_ok}/"
              f"{code_snap_strict_noargs}/{code_snap_strict}/{code_snap_bad}, "
              f"json {code_json}/{code_json_clean})")
        return 0 if ok else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--note", help="the delivered single-file HTML note")
    ap.add_argument("--fact-base", help="fact_base_lite.json number registry")
    ap.add_argument("--furniture", default="",
                    help="comma-separated benign tokens to whitelist in the reverse "
                         "check (years, section numbers); prefer meta.furniture in "
                         "the registry so the exemption is versioned with it")
    ap.add_argument("--report", help="optional path for a JSON audit report")
    ap.add_argument("--snapshots", metavar="MANIFEST",
                    help="source_snapshots.json recorded by "
                         "scripts/source_snapshot.py --record; enables the "
                         "SNAPSHOT linkage check (round 5, reports 10/11)")
    ap.add_argument("--strict-snapshots", action="store_true",
                    help="opt-in: every `Verified` fact must carry a "
                         "source_snapshot hash present in the --snapshots "
                         "manifest (requires --snapshots)")
    ap.add_argument("--strict-temporal", action="store_true",
                    help="opt-in (round 5, reports 10/11): a date-only "
                         "retrieved_at on the filing date FAILS instead of "
                         "NOTE — for intraday-sensitive engagements")
    ap.add_argument("--json", action="store_true",
                    help="machine-readable summary on stdout (diagnostics go "
                         "to stderr) for CI/CD integration (round 5)")
    ap.add_argument("--selftest", action="store_true",
                    help="run built-in self-test and exit")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.note or not args.fact_base:
        print("ERROR  --note and --fact-base are required (or --selftest)",
              file=sys.stderr)
        return 2
    if args.strict_snapshots and not args.snapshots:
        print("ERROR  --strict-snapshots requires --snapshots <manifest>",
              file=sys.stderr)
        return 2
    note = pathlib.Path(args.note)
    fbp = pathlib.Path(args.fact_base)
    if not note.is_file():
        print(f"ERROR  note file not found: {note}", file=sys.stderr)
        return 2
    if not fbp.is_file():
        print(f"ERROR  fact-base file not found: {fbp}", file=sys.stderr)
        return 2
    manifest = None
    if args.snapshots:
        sp = pathlib.Path(args.snapshots)
        if not sp.is_file():
            print(f"ERROR  snapshots manifest not found: {sp}", file=sys.stderr)
            return 2
        try:
            manifest = json.loads(sp.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as e:
            print(f"ERROR  cannot read snapshots manifest: {e}", file=sys.stderr)
            return 2
    try:
        raw = note.read_text(encoding="utf-8")
        fb = json.loads(fbp.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as e:
        print(f"ERROR  cannot read inputs: {e}", file=sys.stderr)
        return 2

    meta = fb.get("meta", {}) or {}
    raw_furn = meta.get("furniture", [])
    if isinstance(raw_furn, str):
        raw_furn = [raw_furn]
    furniture = {str(t).strip() for t in raw_furn if str(t).strip()}
    furniture |= {t.strip() for t in args.furniture.split(",") if t.strip()}

    failures = []
    real_stdout = sys.stdout
    if args.json:
        sys.stdout = sys.stderr      # diagnostics to stderr; stdout stays JSON
    try:
        failures += scan_placeholders(note.name, raw)
        failures += check_registry_schema(fb)
        failures += check_consensus_facts(fb)
        failures += check_temporal_order(fb, strict=args.strict_temporal)
        failures += check_mandate_context(fb)
        failures += check_source_snapshots(fb, manifest,
                                           strict=args.strict_snapshots)
        failures += check_forward(note.name, raw, fb)
        failures += check_reverse(note.name, raw, fb, furniture)
    finally:
        if args.json:
            sys.stdout = real_stdout

    if args.report:
        pathlib.Path(args.report).write_text(
            json.dumps({"failures": failures}, indent=2), encoding="utf-8")

    if args.json:
        print(json.dumps({
            "tool": TOOL_ID,
            "ok": not failures,
            "failure_count": len(failures),
            "failures": failures,
            "flags": {"strict_temporal": bool(args.strict_temporal),
                      "strict_snapshots": bool(args.strict_snapshots),
                      "snapshots": bool(args.snapshots)},
        }, indent=2))
        return 0 if not failures else 1

    print("=" * 60)
    print("AUDIT RESULT:", "CLEAN" if not failures else f"{len(failures)} failure(s)")
    for f in failures:
        print(" ", f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
