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
     (timestamp precision insufficient), not a failure. The gate is silent when
     meta.t1_filing_timestamp is absent.

Usage:
  python3 fact_base_lite_audit.py --note <note.html> --fact-base <fact_base_lite.json>
  python3 fact_base_lite_audit.py --note <note.html> --fact-base <fb.json> \
      --furniture "2026,2027"
  python3 fact_base_lite_audit.py --selftest

Exit codes: 0 clean, 1 failures found, 2 usage/environment error.
"""
import argparse
import json
import re
import sys
import tempfile
import pathlib
from datetime import date, datetime

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


def check_temporal_order(fb: dict) -> list:
    """TEMPORAL gate (round 4, reports 8/9 M-6, report-9-corrected design).

    Active only when meta.t1_filing_timestamp is set (the verified T1
    filing/publication time). Enforces, per fact: a data_type classification
    in {pre_event_input, post_event_fact}; and for post_event_fact entries,
    retrieved_at >= the T1 timestamp. Pre-filing retrieval of a post-event
    claim is contamination: flag it Unverifiable and strip it from the
    registry. Pre-event inputs (consensus, positioning, prior guidance,
    options OI) legitimately predate the event and are exempt by design.
    Date-only retrieved_at landing on the filing date is a precision NOTE,
    not a failure. A data-integrity control, not a Reg FD control."""
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
        ok = (code_ok == 0 and code_extra == 1 and code_furn == 0
              and code_bad == 1 and code_cons == 1
              and any("L-10" in f and "CONSENSUS" in f
                      for f in rep_cons["failures"])
              and code_temp_ok == 0 and code_temp_bad == 1
              and any("L-13" in f and "TEMPORAL" in f
                      for f in rep_temp["failures"])
              and any("L-14" in f and "data_type" in f
                      for f in rep_temp["failures"]))
        print("=" * 60)
        print("SELFTEST:", "PASS" if ok else "FAIL",
              f"(clean {code_ok}, unregistered {code_extra}, "
              f"furniture {code_furn}, schema {code_bad}, consensus {code_cons}, "
              f"temporal-clean {code_temp_ok}, temporal-dirty {code_temp_bad})")
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
    ap.add_argument("--selftest", action="store_true",
                    help="run built-in self-test and exit")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.note or not args.fact_base:
        print("ERROR  --note and --fact-base are required (or --selftest)",
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
    failures += scan_placeholders(note.name, raw)
    failures += check_registry_schema(fb)
    failures += check_consensus_facts(fb)
    failures += check_temporal_order(fb)
    failures += check_forward(note.name, raw, fb)
    failures += check_reverse(note.name, raw, fb, furniture)

    if args.report:
        pathlib.Path(args.report).write_text(
            json.dumps({"failures": failures}, indent=2), encoding="utf-8")

    print("=" * 60)
    print("AUDIT RESULT:", "CLEAN" if not failures else f"{len(failures)} failure(s)")
    for f in failures:
        print(" ", f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
