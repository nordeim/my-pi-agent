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
     (promote them to failures with the opt-in --fail-on-unverified).
     Facts carrying a `formula` of the form "LHS = RHS" (numbers and
     + - * / ( ) only) are arithmetically checked: both sides are evaluated
     and must agree (percent-aware: "…= -12.29%" compares against LHS*100).
     Facts with confidence "Assumed" must be listed on the method/
     assumptions page, designated via --method-page FILE or the fact base's
     meta.method_page field.
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
  2. Checks mode    : --slides DIR --checks FILE
     FILE = {"slide_01.html": ["-12.29%", "$482B", ...]} — per-slide needles.
  3. Scan-only      : --slides DIR — placeholder scan only.

Self-test: python3 fact_base_audit.py --selftest
Exit codes: 0 clean, 1 failures found, 2 usage/environment error.
"""
import argparse, ast, json, re, sys, tempfile, pathlib

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


def run_fact_base_mode(slides: dict, fb: dict, method_page: str,
                       strict_verified: bool = False,
                       decision_critical: str = "") -> tuple:
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
    return fails, skipped, covered


def unverified_candidates(slides: dict, covered: set) -> list:
    """Numbers visible on slides but not covered by any fact — to review.
    Sign-tolerant: a fact recorded as -482 covers a slide's '$48B erased'."""
    cands = set()
    for raw in slides.values():
        for m in re.finditer(r"\$\d[\d,\.]*\s?[BM]?|\d+\.\d+%?|\d{2,}%", visible_text(raw)):
            disp = m.group(0).strip()
            tok = disp.replace(",", "").replace("$", "").replace("%", "").rstrip("BMK.")
            tok = tok.lstrip("-").rstrip(".")
            if tok and tok not in covered and ("-" + tok) not in covered \
               and float(tok) != 0:
                cands.add(disp)
    return sorted(cands)


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
            "FCF −$9.1B, ex-fine ≈ −$3.9B.</p>"
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
        fb = {"meta": {"method_page": "slide_14.html"}, "facts": [
            {"id": "F-1", "value": 282.32, "slide_pages": ["slide_01.html"]},
            {"id": "F-2", "value": "-12.29%", "slide_pages": ["slide_01.html"]},
            {"id": "F-3", "value": -482, "unit": "$B", "slide_pages": ["slide_01.html"]},
            {"id": "F-4", "value": "no digits here", "slide_pages": ["slide_01.html"]},
            {"id": "F-5", "value": 63.4, "slide_pages": ["slide_01.html"]},   # must FAIL
            {"id": "F-6", "value": 999.9, "slide_pages": ["slide_99.html"]},  # must BADREF+FAIL
            # H-4 regression: substring of a longer slide number must NOT pass.
            {"id": "F-7", "value": 82.3, "slide_pages": ["slide_01.html"]},   # must FAIL
            {"id": "F-8", "value": 12.29, "slide_pages": ["slide_03.html"]},  # must FAIL
            # Derived-fact formula checks.
            {"id": "F-9", "value": -3.9, "confidence": "Reasoned",
             "formula": "-9.1 + 5.2 = -3.9", "slide_pages": ["slide_01.html"]},
            {"id": "F-10", "value": -3.8, "confidence": "Reasoned",
             "formula": "-9.1 + 5.2 = -3.8", "slide_pages": ["slide_01.html"]},  # must FORMULA-FAIL
            {"id": "F-11", "value": -12.29, "confidence": "Reasoned",
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
              and any("103%" in c for c in report["unverified_candidates"]))
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
        print("=" * 60)
        print("SELFTEST:", "PASS" if ok else "FAIL",
              f"(default exit {code}, strict exit {code_s}, cli-dc exit {code_c})")
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
            decision_critical=args.decision_critical)
    if args.checks:
        checks = json.loads(pathlib.Path(args.checks).read_text(encoding="utf-8"))
        failures += run_checks_mode(slides, checks)
        for needles in checks.values():
            covered.update(str(n) for n in needles)
    if not args.fact_base and not args.checks:
        print(f"Scanned {len(slides)} slide(s) — placeholder scan only "
              "(no fact base / checks given).")

    failures += scan_placeholders(slides)

    cands = unverified_candidates(slides, covered) if args.fact_base else []
    if cands:
        print("-" * 60)
        if args.fail_on_unverified:
            print(f"NOTE   {len(cands)} unverified candidate(s) promoted to "
                  "failures by --fail-on-unverified:")
            for c in cands:
                failures.append(f"UNVERIFIED   slide number '{c}' has no "
                                 "fact-base entry (add it or confirm benign)")
                print(f"       ! {c}")
        else:
            print(f"NOTE   {len(cands)} unverified candidate(s) on slides — add to the fact "
                  "base or confirm benign (years, page furniture); promoted to "
                  "failures only with --fail-on-unverified:")
            for c in cands:
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
