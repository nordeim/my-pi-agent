#!/usr/bin/env python3
"""fact_base_audit.py — numeric + placeholder audit for stock-RCA slide decks.

Verifies that every number in the report's fact base actually appears on the
slides, reverse-checks numbers found on slides against the fact base, scans
for placeholder tokens, evaluates derived-fact formulas, and checks that
`Assumed` facts are listed on the method/assumptions page. Modes:

  1. Fact-base mode : --slides DIR --fact-base FILE
     Every fact's numeric tokens must appear on >=1 of its slide_pages (or
     anywhere in the deck if slide_pages is unset). Matching is
     sign/symbol tolerant ("-$9.1B" matches fact -9.1; "$482B erased"
     matches fact -482) but ANCHORED: a token matches only a complete
     number on the slide, never a digit substring of a longer number
     ("82.3" does NOT match "$282.32").
     Numbers found on slides but absent from the fact base are reported as
     "unverified candidates" — a to-review list, not automatic failures
     (promote them to failures with the opt-in --fail-on-unverified, or
     per decision-critical page with --strict-pages).
     Facts carrying a `formula` of the form "LHS = RHS" (numbers and
     + - * / ( ) only) are arithmetically checked: both sides are evaluated
     and must agree (percent-aware: "…= -12.29%" compares against LHS*100).
     Facts with confidence "Assumed" must be listed on the method/
     assumptions page, designated via --method-page FILE or the fact base's
     meta.method_page field.
     Round-3 schema gates (always on — deterministic, no heuristic false
     positives; reports 6/7 findings H-1/H-2/C-1):
       CONSENSUS   consensus-side facts (is_consensus, or a metric naming
                   consensus/estimates) must carry consensus_provider,
                   consensus_vintage (YYYY-MM-DD), consensus_statistic in
                   {mean, median, undisclosed} (round 4, reports 8/9 M-1 —
                   mean-vs-median is a recorded disclosure) and a T1/T2
                   source_tier, with the vintage inside
                   --consensus-max-age-days (default 5 calendar days ≈ 3
                   trading days, 0 disables) of meta.event_timestamp — the
                   consensus is the denominator of every beat/miss delta
       EPISTEMIC   every `Reasoned` fact must declare epistemic_kind:
                   "derived" (deterministic — a formula is then required)
                   or "judged" (analytical allocation, explicitly non-causal)
       WATERFALL   facts carrying a signed driver `weights` dict must sum
                   to their realized_move within tolerance — the sum-to-move
                   identity is enforced in code, not just claimed in prose
       MANDATE     when meta.audience names an IC / investment committee,
                   meta.mandate_context (fund_position + position_as_of)
                   must be present — buy-side conflict-of-interest disclosure
       TEMPORAL    (round 4, reports 8/9 M-6, report-9-corrected design) when
                   meta.t1_filing_timestamp is set (the verified T1
                   filing/publication time), every fact must declare data_type
                   in {pre_event_input, post_event_fact}, and every
                   post_event_fact must carry retrieved_at >= the T1 timestamp
                   — a post-event claim retrieved pre-filing is contamination:
                   flag it Unverifiable and strip it from the fact base. A
                   data-integrity control, not a Reg FD control: pre-event
                   inputs (consensus, positioning, prior guidance, options
                   OI) legitimately predate the event and are exempt. Silent
                   when meta.t1_filing_timestamp is absent.
     Opt-in strict compliance modes (institutional builds):
       --strict-verified     every fact tagged `Verified` must carry >=2
                             entries in cross_checked_with (the family's
                             double-sourcing rule; report-3/4 finding M2)
       --decision-critical A,B  fact IDs that must carry >=2 cross-checks
                             regardless of --strict-verified (same effect as
                             meta.decision_critical in the fact base)
       --fail-on-unverified  reverse-check "unverified candidates" become
                             failures (exit 1) instead of a NOTE review list
                             — opt-in only: the reverse-check is heuristic,
                             and page furniture (years, section numbers)
                             legitimately appears without fact-base entries
       --strict-pages A.html,B.html  decision-critical pages (executive
                             summary, root-cause decomposition) where
                             unverified candidates are failures even without
                             --fail-on-unverified — strict where it matters,
                             advisory for page furniture elsewhere
  2. Checks mode    : --slides DIR --checks FILE
     FILE = {"slide_01.html": ["-12.29%", "$482B", ...]} — per-slide needles.
  3. Scan-only      : --slides DIR — placeholder scan only.

Self-test: python3 fact_base_audit.py --selftest
Exit codes: 0 clean, 1 failures found, 2 usage/environment error.
"""
import argparse, ast, json, re, sys, tempfile, pathlib
from datetime import date, datetime

PLACEHOLDER_PATTERNS = [
    r"lorem", r"\btodo\b", r"placeholder", r"\btbd\b", r"\bxxx\b", r"\bnan\b",
    r"\bundefined\b", r"insert (data|here|numbers)", r"foo bar", r"【",
]
NUM_RE = re.compile(r"-?\d[\d,]*(?:\.\d+)?")


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
    """Complete number tokens in normalized slide text, with $ % + stripped.

    Anchoring: matching happens token-to-token, so a fact's "82.3" can never
    satisfy itself against a slide's "$282.32" — the slide's number is the
    single token 282.32, not a bag of digit substrings."""
    hay2 = re.sub(r"[$%,+]", "", hay_norm)
    return {t.replace(",", "").rstrip(".")
            for t in NUM_RE.findall(hay2)
            if t.replace(",", "").rstrip(".") not in ("", "-", ".")}


def token_in(tok: str, hay_norm: str) -> bool:
    """Sign/symbol-tolerant ANCHORED token presence check.

    Primary: exact (sign included) match against a complete slide number.
    Fallback: magnitude-only match (a slide may print 'erased $482B' for a
    fact recorded as -482) and numeric equality ('9.1' == '9.10')."""
    toks = hay_tokens(hay_norm)
    if tok in toks or tok.lstrip("-") in toks:
        return True
    try:
        tv = float(tok)
    except ValueError:
        return False
    return any(float(t) == tv for t in toks)


def scan_placeholders(slides: dict) -> list:
    fails = []
    for fname, raw in slides.items():
        low = norm(visible_text(raw))
        for pat in PLACEHOLDER_PATTERNS:
            if re.search(pat, low):
                fails.append(f"PLACEHOLDER  {fname}  matches /{pat}/")
    return fails


# ---------- derived-fact formula checking ----------

_ALLOWED_NODES = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Add, ast.Sub,
                  ast.Mult, ast.Div, ast.USub, ast.UAdd, ast.Constant)


def _eval_arith(expr: str):
    """Evaluate a numbers/+-*/() expression safely; None if not pure arithmetic."""
    expr = expr.strip().rstrip("%").strip()
    if not re.fullmatch(r"[-+*/().\d\s]+", expr):
        return None
    try:
        tree = ast.parse(expr, mode="eval")
        for node in ast.walk(tree):
            if not isinstance(node, _ALLOWED_NODES):
                return None
            if isinstance(node, ast.Constant) and not isinstance(node.value, (int, float)):
                return None
        return eval(compile(tree, "<formula>", "eval"),
                    {"__builtins__": {}}, {})
    except (SyntaxError, ValueError, ZeroDivisionError, TypeError):
        return None


def check_formulas(fb: dict) -> list:
    """Arithmetic gate for derived facts: evaluate 'LHS = RHS' formulas.

    Percent-aware: when the RHS carries a '%' the LHS is compared * 100.
    Formulas containing words/names are skipped (checked only when both
    sides are pure arithmetic)."""
    fails = []
    for fact in fb.get("facts", []):
        fid = fact.get("id", "?")
        formula = fact.get("formula")
        if not formula or "=" not in str(formula):
            continue
        lhs_src, rhs_src = str(formula).split("=", 1)
        has_pct = "%" in rhs_src
        lhs, rhs = _eval_arith(lhs_src), _eval_arith(rhs_src)
        if lhs is None or rhs is None:
            continue
        if has_pct:
            lhs = lhs * 100.0
        tol = max(0.051, abs(rhs) * 0.005)
        if abs(lhs - rhs) > tol:
            fails.append(f"FORMULA      {fid}  '{formula}' does not compute: "
                         f"LHS {lhs:.4f} vs RHS {rhs:.4f}")
        else:
            print(f"PASS   {fid}  formula checks out ({lhs:.4f} ≈ {rhs:.4f})")
    return fails


def check_assumed_on_method_page(fb: dict, slides: dict, method_page: str) -> list:
    """Every Assumed fact must be listed on the method/assumptions page.

    Numeric Assumed facts: their tokens must appear on the method page.
    Text-only Assumed facts: at least one significant word of the metric
    must appear there. Fails closed when Assumed facts exist but no method
    page is designated."""
    fails = []
    assumed = [f for f in fb.get("facts", []) if f.get("confidence") == "Assumed"]
    if not assumed:
        return fails
    if not method_page or method_page not in slides:
        fails.append("ASSUMED-PAGE no method/assumptions page designated but "
                     f"{len(assumed)} Assumed fact(s) exist — pass --method-page "
                     "or set meta.method_page")
        return fails
    page_text = norm(visible_text(slides[method_page]))
    page_toks = hay_tokens(page_text)
    for fact in assumed:
        fid = fact.get("id", "?")
        toks = numeric_tokens(fact.get("value"))
        if toks:
            ok = any(t in page_toks or t.lstrip("-") in page_toks or
                     any(float(t) == float(p) for p in page_toks if _isfloat(p))
                     for t in toks)
        else:
            words = [w for w in re.findall(r"[a-z]{5,}", norm(str(fact.get("metric", ""))))]
            ok = any(w in page_text for w in words)
        if ok:
            print(f"PASS   {fid}  Assumed fact listed on {method_page}")
        else:
            fails.append(f"ASSUMED      {fid}  Assumed but not listed on the "
                         f"method page {method_page}")
    return fails


def _isfloat(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False


def check_cross_checks(fb: dict, strict_verified: bool, extra_ids: str) -> list:
    """Cross-check enforcement (opt-in strict compliance modes).

    A fact needs >=2 entries in cross_checked_with when either
      (a) --strict-verified is on and the fact is tagged `Verified`, or
      (b) the fact's id is decision-critical (meta.decision_critical in the
          fact base, or the --decision-critical CLI list).
    Default mode stays silent: the schema marks cross_checked_with
    "decision-critical" — enforcing it for every fact would flag routine
    Verified observations that were never required to be double-sourced."""
    fails = []
    meta = fb.get("meta", {}) or {}
    dc = {str(x) for x in meta.get("decision_critical", [])}
    dc |= {x.strip() for x in (extra_ids or "").split(",") if x.strip()}
    for fact in fb.get("facts", []):
        fid = fact.get("id", "?")
        n = len(fact.get("cross_checked_with") or [])
        if n >= 2:
            continue
        if strict_verified and fact.get("confidence") == "Verified":
            fails.append(f"CROSSCHECK   {fid}  `Verified` with {n} cross-check(s) "
                         "— strict mode requires >=2 independent sources")
        elif fid in dc:
            fails.append(f"CROSSCHECK   {fid}  decision-critical with {n} "
                         "cross-check(s) — requires >=2 independent sources")
    return fails


# ---------- round-3 schema gates (reports 6/7: H-1, H-2, C-1) ----------

def _parse_iso_date(s: str):
    """Best-effort YYYY-MM-DD prefix parse; None when unparseable."""
    try:
        return date.fromisoformat(str(s).strip()[:10])
    except (ValueError, TypeError):
        return None


def _parse_moment(raw):
    """Best-effort ISO parse -> (datetime-or-date, has_time); None when
    unparseable. Timezone offsets are kept so aware-vs-aware comparison is
    exact across offsets; date-only strings compare at date granularity."""
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


def _is_consensus_fact(fact: dict) -> bool:
    if fact.get("is_consensus") is True:
        return True
    metric = str(fact.get("metric", "")).lower()
    return any(k in metric for k in ("consensus", "estimate", "whisper"))


def check_consensus_facts(fb: dict, max_age_days: int = 5) -> list:
    """Consensus-side facts carry provider, vintage, recorded statistic and
    a T1/T2 tier, fresh relative to the event (report-6/7 H-1 + round-4
    reports 8/9 M-1: the consensus is the denominator of every beat/miss
    delta — a stale, aggregator-only, or mean-vs-median-undisclosed print
    corrupts them all)."""
    fails = []
    meta = fb.get("meta", {}) or {}
    event_date = _parse_iso_date(meta.get("event_timestamp", ""))
    for fact in fb.get("facts", []):
        fid = fact.get("id", "?")
        if not _is_consensus_fact(fact):
            continue
        missing = [f for f in ("consensus_provider", "consensus_vintage",
                               "consensus_statistic")
                   if not str(fact.get(f, "")).strip()]
        tier = str(fact.get("source_tier", "")).strip()
        if tier not in ("T1", "T2"):
            missing.append(f"source_tier in T1/T2 (got {tier or 'missing'}; an "
                           "aggregator consensus print is never sufficient)")
        if missing:
            fails.append(f"CONSENSUS    {fid}  consensus-side fact missing: "
                         + ", ".join(missing))
            continue
        stat = str(fact.get("consensus_statistic", "")).strip().lower()
        if stat not in ("mean", "median", "undisclosed"):
            fails.append(f"CONSENSUS    {fid}  consensus_statistic {stat!r} is "
                         "not one of mean / median / undisclosed — record "
                         "which statistic the provider prints (undisclosed "
                         "only when the outlet genuinely does not say)")
            continue
        if max_age_days and event_date:
            v = _parse_iso_date(fact.get("consensus_vintage", ""))
            if v is None:
                fails.append(f"CONSENSUS    {fid}  consensus_vintage is not "
                             "YYYY-MM-DD")
                continue
            age = (event_date - v).days
            if age < 0 or age > max_age_days:
                fails.append(f"CONSENSUS    {fid}  consensus_vintage {v} is {age} "
                             f"days before the event — outside the {max_age_days}-day "
                             "window (stale consensus corrupts every delta; re-verify "
                             "against a fresh named-provider print)")
            else:
                print(f"PASS   {fid}  consensus vintage {v} ({age}d before the event, "
                      f"{fact.get('consensus_provider')}, "
                      f"{fact.get('consensus_statistic')})")
    return fails


def check_temporal_order(fb: dict) -> list:
    """TEMPORAL gate (round 4, reports 8/9 M-6, report-9-corrected design).

    Active only when meta.t1_filing_timestamp is set (the verified T1
    filing/publication time). Enforces, per fact: a data_type classification
    in {pre_event_input, post_event_fact}; and for post_event_fact entries,
    retrieved_at >= the T1 timestamp. A post-event claim retrieved before
    the filing is pre-filing contamination — flag it Unverifiable and strip
    it from the fact base. Pre-event inputs (consensus, positioning, prior
    guidance, options OI) legitimately predate the event and are exempt by
    design: the report-9 correction — stripping every pre-filing retrieval
    would purge legitimate pre-event inputs, so the gate discriminates on
    data_type. Date-only retrieved_at on the filing date itself is a NOTE
    (precision insufficient), not a failure. A data-integrity control, not
    a Reg FD control (Reg FD binds issuers; 10b-5 attaches to trading)."""
    meta = fb.get("meta", {}) or {}
    t1_raw = str(meta.get("t1_filing_timestamp", "")).strip()
    if not t1_raw:
        return []          # gate opted out: no verified T1 timestamp on record
    t1, t1_has_time = _parse_moment(t1_raw)
    if t1 is None:
        return ["TEMPORAL    meta.t1_filing_timestamp is not ISO-parseable — "
                "pin the verified T1 filing time as YYYY-MM-DD[THH:MM:SS] "
                "or remove it to disable the gate"]
    fails = []
    for fact in fb.get("facts", []):
        fid = fact.get("id", "?")
        dtype = str(fact.get("data_type", "")).strip().lower()
        if dtype not in ("pre_event_input", "post_event_fact"):
            fails.append(f"TEMPORAL    {fid}  missing/invalid data_type "
                         f"{dtype or '(absent)'} — classify every fact "
                         "pre_event_input or post_event_fact when the T1 "
                         "filing time is on record")
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
            else:
                ordered = (ret.date() if hasattr(ret, "date") else ret) >= \
                          (t1.date() if hasattr(t1, "date") else t1)
        except TypeError:    # mixed aware/naive — date-level fallback
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
                         "the fact Unverifiable and strip it from the fact base")
    return fails


def check_mandate_context(fb: dict) -> list:
    """IC-facing fact bases must disclose position/mandate context.

    Reports 6/7 C-1, corrected to the buy-side regime: Reg AC / FINRA 2241
    apply to distributed sell-side research, which these skills explicitly are
    not — but an internal IC deliverable still requires conflict-of-interest
    visibility (CFA Institute Standard I(B), Advisers Act fiduciary duty).
    Deterministic presence check: no heuristic false positives."""
    meta = fb.get("meta", {}) or {}
    audience = meta.get("audience", "")
    if isinstance(audience, list):
        audience = " ".join(str(a) for a in audience)
    if not re.search(r"\b(ic|investment[\s-]committee)\b", str(audience).lower()):
        return []
    mc = meta.get("mandate_context") or {}
    if not isinstance(mc, dict) or not str(mc.get("fund_position", "")).strip() \
            or not str(mc.get("position_as_of", "")).strip():
        return ["MANDATE      meta.audience names an IC audience but "
                "meta.mandate_context is absent or incomplete — an IC-facing "
                "deliverable must disclose fund_position (long/short/none/"
                "undetermined) and position_as_of; conflict visibility is what "
                "lets the committee discount the analysis for an existing "
                "position"]
    print(f"PASS   mandate_context present (fund_position: "
          f"{mc.get('fund_position')}, as of {mc.get('position_as_of')})")
    return []


def check_epistemic_kinds(fb: dict) -> list:
    """`Reasoned` facts declare epistemic_kind: derived vs judged.

    Report-6/7 H-2: the single `Reasoned` label conflated deterministic
    derivation (reproducible: formula + parents) with analyst judgment
    (allocation, non-causal). The split is now schema-enforced so an IC reader
    can tell reproducible math from opinion at the record level. Accepts the
    parenthesized forms ("Reasoned (derived)" / "Reasoned (judged)") too."""
    fails = []
    for fact in fb.get("facts", []):
        fid = fact.get("id", "?")
        conf = str(fact.get("confidence", "")).strip()
        if conf == "Reasoned":
            kind = str(fact.get("epistemic_kind", "")).strip().lower()
        elif conf.lower().startswith("reasoned ("):
            kind = conf.lower().replace("reasoned", "", 1).strip(" ()")
        else:
            continue
        if kind not in ("derived", "judged"):
            fails.append(f"EPISTEMIC    {fid}  `Reasoned` fact without epistemic_kind: "
                         "classify it 'derived' (deterministic — formula + "
                         "derived_from required, audit-checked) or 'judged' "
                         "(analytical allocation, signed, explicitly non-causal)")
            continue
        if kind == "derived" and not str(fact.get("formula", "")).strip():
            fails.append(f"EPISTEMIC    {fid}  epistemic_kind 'derived' but no formula "
                         "— a deterministic derivation must be reproducible")
    return fails


def check_waterfall_sums(fb: dict) -> list:
    """Facts carrying a signed driver `weights` dict must sum to their
    realized_move within tolerance (report-6/7 H-2: the sum-to-move identity
    was claimed in prose; nothing checked it). Arithmetic consistency, not
    causation — same contract as quant_helpers.waterfall_check."""
    fails = []
    for fact in fb.get("facts", []):
        fid = fact.get("id", "?")
        weights, realized = fact.get("weights"), fact.get("realized_move")
        if not isinstance(weights, dict) or realized is None:
            continue
        try:
            total = sum(float(v) for v in weights.values())
            r = float(realized)
        except (TypeError, ValueError):
            fails.append(f"WATERFALL    {fid}  weights/realized_move are not numeric")
            continue
        tol = max(0.05, abs(r) * 0.005)
        if abs(total - r) > tol:
            fails.append(f"WATERFALL    {fid}  signed weights sum to {total:.2f} vs "
                         f"realized_move {r:.2f} (tolerance ±{tol:.2f}) — a `Judged` "
                         "allocation must reproduce the move it allocates")
        else:
            print(f"PASS   {fid}  waterfall weights sum to {total:.2f} ≈ realized "
                  f"{r:.2f} (consistency check, not causation)")
    return fails


def run_fact_base_mode(slides: dict, fb: dict, method_page: str,
                       strict_verified: bool = False,
                       decision_critical: str = "",
                       consensus_max_age: int = 10) -> tuple:
    """Per-fact presence checks. Returns (failures, skipped_ids, covered_tokens)."""
    fails, skipped, covered = [], [], set()
    deck_text = norm(" ".join(visible_text(v) for v in slides.values()))
    for fact in fb.get("facts", []):
        fid = fact.get("id", "?")
        toks = numeric_tokens(fact.get("value"))
        if not toks:
            print(f"SKIP   {fid}  no numeric tokens (verify manually)")
            skipped.append(fid)
            continue
        covered.update(toks)
        listed = fact.get("slide_pages") or []
        pages = [p for p in listed if p in slides]
        for tok in toks:
            if pages:
                hit = any(token_in(tok, norm(visible_text(slides[p]))) for p in pages)
                target = f"its listed pages {listed}"
            else:
                hit = token_in(tok, deck_text)
                target = "the deck"
            if hit:
                print(f"PASS   {fid}  '{tok}' present")
            else:
                fails.append(f"MISSING     {fid}  token '{tok}' not found on {target}")
        if listed and len(pages) < len(listed):
            fails.append(f"BADREF      {fid}  slide_pages contains unknown page "
                         f"{[p for p in listed if p not in slides]}")
    fails += check_formulas(fb)
    fails += check_assumed_on_method_page(fb, slides, method_page)
    fails += check_cross_checks(fb, strict_verified, decision_critical)
    fails += check_consensus_facts(fb, consensus_max_age)
    fails += check_temporal_order(fb)
    fails += check_mandate_context(fb)
    fails += check_epistemic_kinds(fb)
    fails += check_waterfall_sums(fb)
    return fails, skipped, covered


def unverified_candidates(slides: dict, covered: set) -> list:
    """Numbers visible on slides but not covered by any fact — to review.
    Sign-tolerant: a fact recorded as -482 covers a slide's '$48B erased'."""
    return sorted({c for lst in _candidates_by_page(slides, covered).values()
                   for c in lst})


def _candidates_by_page(slides: dict, covered: set) -> dict:
    """Per-slide unverified candidates — the --strict-pages gate needs to know
    WHICH decision-critical page an uncovered number sits on."""
    out = {}
    for fname, raw in slides.items():
        cands = []
        for m in re.finditer(r"\$\d[\d,\.]*\s?[BM]?|\d+\.\d+%?|\d{2,}%", visible_text(raw)):
            disp = m.group(0).strip()
            tok = disp.replace(",", "").replace("$", "").replace("%", "").rstrip("BMK.")
            tok = tok.lstrip("-").rstrip(".")
            if tok and tok not in covered and ("-" + tok) not in covered \
               and float(tok) != 0:
                cands.append(disp)
        if cands:
            out[fname] = cands
    return out


def run_checks_mode(slides: dict, checks: dict) -> list:
    fails = []
    for fname, needles in checks.items():
        if fname not in slides:
            fails.append(f"NOFILE       {fname}")
            continue
        body = norm(slides[fname])
        missing = [n for n in needles if norm(str(n)) not in body]
        if missing:
            fails.append(f"MISSING     {fname}  needles: {missing}")
        else:
            print(f"PASS   {fname}  ({len(needles)} checks)")
    return fails


def selftest() -> int:
    with tempfile.TemporaryDirectory() as td:
        d = pathlib.Path(td)
        (d / "slide_01.html").write_text(
            "<html><body><p>GOOG closed $282.32, −12.29%, ≈$482B erased; +103% ignored; "
            "FCF −$9.1B, ex-fine ≈ −$3.9B; rev $127.58B vs $128.22B cons; EPS 2.12 vs 3.02.</p>"
            "<div class='ghost' data-bleed='intentional' style='position:absolute;left:1200px'>X</div>"
            "</body></html>", encoding="utf-8")
        (d / "slide_02.html").write_text("<html><body><p>TODO fix this</p></body></html>",
                                         encoding="utf-8")
        # Substring trap: '82.3' is a digit-substring of '$282.32' — must FAIL.
        # Sign trap: '12.29' is a digit-substring of '-112.29%' — must FAIL.
        (d / "slide_03.html").write_text("<html><body><p>Move: -112.29%</p></body></html>",
                                         encoding="utf-8")
        (d / "slide_14.html").write_text(
            "<html><body><h2>Assumptions</h2><p>Event-day beta assumed at 1.5; "
            "no index closes pulled.</p></body></html>", encoding="utf-8")
        fb = {"meta": {"method_page": "slide_14.html",
                       "event_timestamp": "2026-10-28T16:05:00-04:00",
                       "audience": "institutional PM/IC",
                       "mandate_context": {"fund_position": "undetermined",
                                            "position_as_of": "2026-10-30"}},
              "facts": [
            {"id": "F-1", "value": 282.32, "slide_pages": ["slide_01.html"]},
            {"id": "F-2", "value": "-12.29%", "slide_pages": ["slide_01.html"]},
            {"id": "F-3", "value": -482, "unit": "$B", "slide_pages": ["slide_01.html"]},
            {"id": "F-4", "value": "no digits here", "slide_pages": ["slide_01.html"]},
            {"id": "F-5", "value": 63.4, "slide_pages": ["slide_01.html"]},   # must FAIL
            {"id": "F-6", "value": 999.9, "slide_pages": ["slide_99.html"]},  # must BADREF+FAIL
            # H-4 regression: substring of a longer slide number must NOT pass.
            {"id": "F-7", "value": 82.3, "slide_pages": ["slide_01.html"]},   # must FAIL
            {"id": "F-8", "value": 12.29, "slide_pages": ["slide_03.html"]},  # must FAIL
            # Derived-fact formula checks (round-3: epistemic_kind declared).
            {"id": "F-9", "value": -3.9, "confidence": "Reasoned",
             "epistemic_kind": "derived",
             "formula": "-9.1 + 5.2 = -3.9", "slide_pages": ["slide_01.html"]},
            {"id": "F-10", "value": -3.8, "confidence": "Reasoned",
             "epistemic_kind": "derived",
             "formula": "-9.1 + 5.2 = -3.8", "slide_pages": ["slide_01.html"]},  # must FORMULA-FAIL
            {"id": "F-11", "value": -12.29, "confidence": "Reasoned",
             "epistemic_kind": "derived",
             "formula": "(282.32 - 321.89) / 321.89 = -12.29%",
             "slide_pages": ["slide_01.html"]},
            # Assumed fact must be listed on meta.method_page (slide_14);
            # its value legitimately appears on the assumptions page itself.
            {"id": "F-12", "value": 1.5, "confidence": "Assumed",
             "metric": "Event-day beta (index closes unavailable)",
             "slide_pages": ["slide_14.html"]},
            # Strict-mode fixtures: F-1 is Verified with only 1 cross-check
            # (must fail --strict-verified); F-2 has 2 (must pass); F-13 is
            # named decision-critical with 0 (must fail even without
            # --strict-verified when listed via meta.decision_critical).
            {"id": "F-13", "value": 42.29, "confidence": "Verified",
             "cross_checked_with": [], "slide_pages": ["slide_01.html"]},
            # Round-3 fixtures — epistemic split, waterfall, consensus, mandate.
            {"id": "F-14", "value": "signed allocation, 5 factors",
             "confidence": "Reasoned", "epistemic_kind": "judged",
             "weights": {"benchmark": -1.5, "fcf_capex": -3.9, "eps_quality": -2.7,
                         "search": -2.4, "positioning": -1.8},
             "realized_move": -12.29},                          # must WATERFALL-PASS
            {"id": "F-15", "value": "signed allocation, inconsistent",
             "confidence": "Reasoned", "epistemic_kind": "judged",
             "weights": {"benchmark": -1.5, "fcf_capex": -2.0},
             "realized_move": -12.29},                          # must WATERFALL-FAIL
            {"id": "F-16", "category": "fundamentals",
             "metric": "Revenue consensus, Q3 2026", "value": 128.22,
             "confidence": "Verified", "source_tier": "T2",
             "consensus_provider": "LSEG (via Reuters)", "consensus_vintage": "2026-10-26",
             "consensus_statistic": "mean",
             "slide_pages": ["slide_01.html"]},                # must CONSENSUS-PASS
            {"id": "F-17", "category": "fundamentals",
             "metric": "EPS consensus, Q3 2026", "value": 3.02,
             "confidence": "Verified", "source_tier": "T3",
             "slide_pages": ["slide_01.html"]},                # must CONSENSUS-FAIL
        ]}
        fb["facts"][0]["cross_checked_with"] = ["F-002"]
        fb["facts"][1]["cross_checked_with"] = ["F-001", "F-003"]
        fb["meta"]["decision_critical"] = ["F-13"]
        (d / "fb.json").write_text(json.dumps(fb), encoding="utf-8")
        code = main(["--slides", str(d), "--fact-base", str(d / "fb.json"),
                     "--report", str(d / "r.json")])
        report = json.loads((d / "r.json").read_text())
        ok = (code == 1
              and any("F-5" in f and "MISSING" in f for f in report["failures"])
              and any("F-6" in f and "BADREF" in f for f in report["failures"])
              and any("PLACEHOLDER" in f and "slide_02" in f for f in report["failures"])
              # anchored-matching regressions (were false PASSes before the fix)
              and any("F-7" in f and "MISSING" in f for f in report["failures"])
              and any("F-8" in f and "MISSING" in f for f in report["failures"])
              # formula gate
              and any("F-10" in f and "FORMULA" in f for f in report["failures"])
              and not any("F-9" in f and "FORMULA" in f for f in report["failures"])
              and not any("F-11" in f and "FORMULA" in f for f in report["failures"])
              # Assumed-on-method-page gate
              and not any("F-12" in f for f in report["failures"])
              and any("F-4" in s for s in report["passes_skipped"])       # text-only skipped
              and any("103%" in c for c in report["unverified_candidates"])
              # round-3 gates: waterfall, consensus, epistemic, mandate
              and any("F-15" in f and "WATERFALL" in f for f in report["failures"])
              and not any("F-14" in f and "WATERFALL" in f for f in report["failures"])
              and any("F-17" in f and "CONSENSUS" in f for f in report["failures"])
              and not any("F-16" in f and "CONSENSUS" in f for f in report["failures"])
              and not any("EPISTEMIC" in f for f in report["failures"])
              and not any("MANDATE" in f for f in report["failures"]))
        # Default run must NOT enforce cross-checks (opt-in discipline) but
        # MUST enforce meta.decision_critical, and unverified candidates stay
        # advisory notes, not failures.
        ok = ok and not any("F-1 " in f and "CROSSCHECK" in f
                            for f in report["failures"])
        ok = ok and any("F-13" in f and "CROSSCHECK" in f
                        for f in report["failures"])
        ok = ok and not any("UNVERIFIED" in f for f in report["failures"])
        # Strict run: F-1 (Verified, 1 cross-check) now fails and the
        # unverified candidate "103%" is promoted to a failure.
        code_s = main(["--slides", str(d), "--fact-base", str(d / "fb.json"),
                       "--strict-verified", "--fail-on-unverified",
                       "--report", str(d / "r_strict.json")])
        r_strict = json.loads((d / "r_strict.json").read_text())
        ok = ok and code_s == 1
        ok = ok and any("F-1" in f and "CROSSCHECK" in f
                        for f in r_strict["failures"])
        ok = ok and not any("F-2" in f and "CROSSCHECK" in f
                            for f in r_strict["failures"])
        ok = ok and any("UNVERIFIED" in f and "103%" in f
                        for f in r_strict["failures"])
        # CLI --decision-critical works without meta.decision_critical and
        # without --strict-verified: F-5 (Verified, no cross-checks) fails.
        fb2 = json.loads(json.dumps(fb))
        del fb2["meta"]["decision_critical"]
        (d / "fb2.json").write_text(json.dumps(fb2), encoding="utf-8")
        code_c = main(["--slides", str(d), "--fact-base", str(d / "fb2.json"),
                       "--decision-critical", "F-5"])
        # Round-4: --strict-pages promotes the slide_01 candidate ("103%") to a
        # failure WITHOUT --fail-on-unverified, while slide furniture elsewhere
        # (none here) stays advisory; an unknown strict page is a BADREF.
        code_sp = main(["--slides", str(d), "--fact-base", str(d / "fb.json"),
                        "--strict-pages", "slide_01.html,slide_77.html",
                        "--report", str(d / "r_sp.json")])
        r_sp = json.loads((d / "r_sp.json").read_text())
        ok = ok and code_sp == 1
        ok = ok and any("UNVERIFIED" in f and "103%" in f and "slide_01" in f
                        for f in r_sp["failures"])
        ok = ok and any("BADREF" in f and "slide_77" in f
                        for f in r_sp["failures"])
        # Round-3: an IC audience without mandate_context fails the MANDATE gate.
        fb3 = json.loads(json.dumps(fb))
        del fb3["meta"]["mandate_context"]
        (d / "fb3.json").write_text(json.dumps(fb3), encoding="utf-8")
        code_m = main(["--slides", str(d), "--fact-base", str(d / "fb3.json"),
                       "--report", str(d / "r_m.json")])
        r_m = json.loads((d / "r_m.json").read_text())
        ok = ok and code_m == 1 and any("MANDATE" in f for f in r_m["failures"])
        # Round-3: a non-IC audience with no mandate_context stays silent, and
        # `Reasoned` without epistemic_kind fails EPISTEMIC (fb4 strips kinds).
        fb4 = json.loads(json.dumps(fb))
        fb4["meta"]["audience"] = "internal research desk"
        for fact in fb4["facts"]:
            fact.pop("epistemic_kind", None)
        (d / "fb4.json").write_text(json.dumps(fb4), encoding="utf-8")
        code_e = main(["--slides", str(d), "--fact-base", str(d / "fb4.json"),
                       "--report", str(d / "r_e.json")])
        r_e = json.loads((d / "r_e.json").read_text())
        ok = ok and code_e == 1
        ok = ok and any("EPISTEMIC" in f and "F-9" in f for f in r_e["failures"])
        ok = ok and not any("MANDATE" in f for f in r_e["failures"])
        # Round-4 (reports 8/9 M-6): TEMPORAL gate. fb5 pins the verified T1
        # filing time; F-1 is a post-event fact retrieved after the filing
        # (PASS), F-18 is a pre-event consensus input retrieved before it
        # (exempt by design), F-19 is a post-event fact retrieved BEFORE the
        # filing (contamination — must fail), F-20 lacks a data_type (must
        # fail). Consensus facts need the round-4 statistic field, so F-16's
        # vintage/statistic are kept and F-18 carries the full set.
        fb5 = json.loads(json.dumps(fb))
        fb5["meta"]["t1_filing_timestamp"] = "2026-10-28T16:05:00-04:00"
        fb5["facts"][0]["data_type"] = "post_event_fact"
        fb5["facts"][0]["retrieved_at"] = "2026-10-29T20:00:00+08:00"
        fb5["facts"][1]["data_type"] = "post_event_fact"
        fb5["facts"][1]["retrieved_at"] = "2026-10-29T20:00:00+08:00"
        fb5["facts"].extend([
            {"id": "F-18", "value": 128.22, "metric": "Revenue consensus, Q3 2026",
             "confidence": "Verified", "source_tier": "T2",
             "consensus_provider": "LSEG (via Reuters)",
             "consensus_vintage": "2026-10-26", "consensus_statistic": "mean",
             "data_type": "pre_event_input",
             "retrieved_at": "2026-10-28T09:00:00+08:00",
             "slide_pages": ["slide_01.html"]},              # exempt: pre-event
            {"id": "F-19", "value": 42.29, "confidence": "Verified",
             "data_type": "post_event_fact",
             "retrieved_at": "2026-10-28T10:00:00-04:00",
             "slide_pages": ["slide_01.html"]},                # TEMPORAL-FAIL
            {"id": "F-20", "value": 40.6, "confidence": "Verified",
             "retrieved_at": "2026-10-29T20:00:00+08:00",
             "slide_pages": ["slide_01.html"]},                # data_type-FAIL
        ])
        (d / "fb5.json").write_text(json.dumps(fb5), encoding="utf-8")
        code_t = main(["--slides", str(d), "--fact-base", str(d / "fb5.json"),
                       "--report", str(d / "r_t.json")])
        r_t = json.loads((d / "r_t.json").read_text())
        ok = ok and code_t == 1
        ok = ok and any("F-19" in f and "TEMPORAL" in f for f in r_t["failures"])
        ok = ok and any("F-20" in f and "data_type" in f for f in r_t["failures"])
        ok = ok and not any("F-1 " in f and "TEMPORAL" in f
                            for f in r_t["failures"])
        ok = ok and not any("F-18" in f and "TEMPORAL" in f
                            for f in r_t["failures"])
        print("=" * 60)
        print("SELFTEST:", "PASS" if ok else "FAIL",
              f"(default exit {code}, strict exit {code_s}, cli-dc exit {code_c}, "
              f"strict-pages exit {code_sp}, mandate exit {code_m}, "
              f"epistemic exit {code_e}, temporal exit {code_t})")
        return 0 if ok else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--slides", default="./slides", help="directory of slide_NN.html files")
    ap.add_argument("--fact-base", help="fact_base.json (mode 1)")
    ap.add_argument("--checks", help="checks.json {slide: [needles]} (mode 2)")
    ap.add_argument("--method-page",
                    help="slide carrying the assumptions/method list (default: "
                         "fact-base meta.method_page; required when Assumed "
                         "facts exist)")
    ap.add_argument("--strict-verified", action="store_true",
                    help="opt-in: every fact tagged `Verified` must carry >=2 "
                         "entries in cross_checked_with")
    ap.add_argument("--decision-critical", default="",
                    help="comma-separated fact IDs that require >=2 "
                         "cross_checked_with entries (same effect as "
                         "meta.decision_critical in the fact base)")
    ap.add_argument("--fail-on-unverified", action="store_true",
                    help="opt-in: promote reverse-check 'unverified candidates' "
                         "to failures (exit 1). Default keeps them as a NOTE "
                         "review list because the reverse-check is heuristic")
    ap.add_argument("--strict-pages", default="",
                    help="comma-separated slide files where unverified candidates "
                         "are failures even without --fail-on-unverified — the "
                         "decision-critical pages (executive summary, root-cause "
                         "decomposition); page furniture elsewhere stays advisory")
    ap.add_argument("--consensus-max-age-days", type=int, default=5,
                    metavar="N",
                    help="CONSENSUS gate: maximum calendar days between a fact's "
                         "consensus_vintage and meta.event_timestamp (default 5 "
                         "calendar days ≈ 3 trading days — round 4, reports 8/9 "
                         "M-1 tightened it from 10; 0 disables the freshness "
                         "check — provider/statistic/tier still required)")
    ap.add_argument("--report", help="optional path for a JSON audit report")
    ap.add_argument("--selftest", action="store_true", help="run built-in self-test and exit")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()

    sdir = pathlib.Path(args.slides)
    if not sdir.is_dir():
        print(f"ERROR  slides dir not found: {sdir}", file=sys.stderr)
        return 2
    slides = {f.name: f.read_text(encoding="utf-8") for f in sorted(sdir.glob("slide_*.html"))}
    if not slides:
        print(f"ERROR  no slide_*.html files in {sdir}", file=sys.stderr)
        return 2

    failures, skipped, covered = [], [], set()
    if args.fact_base:
        fb = json.loads(pathlib.Path(args.fact_base).read_text(encoding="utf-8"))
        method_page = args.method_page or (fb.get("meta", {}) or {}).get("method_page")
        failures, skipped, covered = run_fact_base_mode(
            slides, fb, method_page,
            strict_verified=args.strict_verified,
            decision_critical=args.decision_critical,
            consensus_max_age=args.consensus_max_age_days)
    if args.checks:
        checks = json.loads(pathlib.Path(args.checks).read_text(encoding="utf-8"))
        failures += run_checks_mode(slides, checks)
        for needles in checks.values():
            covered.update(str(n) for n in needles)
    if not args.fact_base and not args.checks:
        print(f"Scanned {len(slides)} slide(s) — placeholder scan only "
              "(no fact base / checks given).")

    failures += scan_placeholders(slides)

    cands_by_page = _candidates_by_page(slides, covered) if args.fact_base else {}
    strict_pages = {p.strip() for p in (args.strict_pages or "").split(",")
                    if p.strip()}
    # Decision-critical pages fail closed; --fail-on-unverified promotes the rest.
    for fname in sorted(strict_pages):
        if fname not in slides:
            failures.append(f"BADREF      --strict-pages names unknown page {fname}")
        for c in cands_by_page.get(fname, []):
            failures.append(f"UNVERIFIED   {fname}  slide number '{c}' has no "
                            "fact-base entry (--strict-pages: decision-critical "
                            "page — add it to the fact base or confirm benign)")
    if args.fail_on_unverified:
        for fname, lst in cands_by_page.items():
            if fname in strict_pages:
                continue  # already failures above — no double count
            for c in lst:
                failures.append(f"UNVERIFIED   slide number '{c}' has no "
                                "fact-base entry (add it or confirm benign)")
    cands = sorted({c for lst in cands_by_page.values() for c in lst})
    advisory = [c for c in cands
                if not args.fail_on_unverified
                and not any(c in cands_by_page.get(p, []) for p in strict_pages)]
    if advisory:
        print("-" * 60)
        print(f"NOTE   {len(advisory)} unverified candidate(s) on slides — add to "
              "the fact base or confirm benign (years, page furniture); promoted "
              "to failures on --strict-pages pages or with --fail-on-unverified:")
        for c in advisory:
            print(f"       ? {c}")

    if args.report:
        pathlib.Path(args.report).write_text(json.dumps(
            {"failures": failures, "passes_skipped": skipped,
             "unverified_candidates": cands}, indent=2), encoding="utf-8")

    print("=" * 60)
    print("AUDIT RESULT:", "CLEAN" if not failures else f"{len(failures)} failure(s)")
    for f in failures:
        print(" ", f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
