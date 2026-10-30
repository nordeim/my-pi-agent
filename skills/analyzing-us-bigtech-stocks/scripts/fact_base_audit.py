#!/usr/bin/env python3
"""fact_base_audit.py — numeric + placeholder audit for stock-RCA slide decks.

Verifies that every number in the report's fact base actually appears on the
slides, reverse-checks numbers found on slides against the fact base, and scans
for placeholder tokens. Modes:

  1. Fact-base mode : --slides DIR --fact-base FILE
     Every fact's numeric tokens must appear on >=1 of its slide_pages (or
     anywhere in the deck if slide_pages is unset). Matching is sign/symbol
     tolerant ("-$9.1B" matches fact -9.1; "$482B erased" matches fact -482)
     so formatting differences do not mask genuinely missing numbers.
     Numbers found on slides but absent from the fact base are reported as
     "unverified candidates" — a to-review list, not automatic failures.
  2. Checks mode    : --slides DIR --checks FILE
     FILE = {"slide_01.html": ["-12.29%", "$482B", ...]} — per-slide needles.
  3. Scan-only      : --slides DIR — placeholder scan only.

Self-test: python3 fact_base_audit.py --selftest
Exit codes: 0 clean, 1 failures found, 2 usage/environment error.
"""
import argparse, json, re, sys, tempfile, pathlib

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


def token_in(tok: str, hay_norm: str) -> bool:
    """Sign/symbol-tolerant token presence check.

    Primary: exact (sign included) match against hay with '$', '%', '+', ','
    stripped. Fallback: magnitude-only match (a slide may print 'erased $482B'
    for a fact recorded as -482)."""
    hay2 = re.sub(r"[$%,+]", "", hay_norm)
    return tok in hay2 or tok.lstrip("-") in hay2


def scan_placeholders(slides: dict) -> list:
    fails = []
    for fname, raw in slides.items():
        low = norm(raw)
        for pat in PLACEHOLDER_PATTERNS:
            if re.search(pat, low):
                fails.append(f"PLACEHOLDER  {fname}  matches /{pat}/")
    return fails


def run_fact_base_mode(slides: dict, fb: dict) -> tuple:
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
            "<html><body><p>GOOG closed $282.32, −12.29%, ≈$482B erased; +103% ignored.</p>"
            "<div class='ghost' data-bleed='intentional' style='position:absolute;left:1200px'>X</div>"
            "</body></html>", encoding="utf-8")
        (d / "slide_02.html").write_text("<html><body><p>TODO fix this</p></body></html>",
                                         encoding="utf-8")
        fb = {"facts": [
            {"id": "F-1", "value": 282.32, "slide_pages": ["slide_01.html"]},
            {"id": "F-2", "value": "-12.29%", "slide_pages": ["slide_01.html"]},
            {"id": "F-3", "value": -482, "unit": "$B", "slide_pages": ["slide_01.html"]},
            {"id": "F-4", "value": "no digits here", "slide_pages": ["slide_01.html"]},
            {"id": "F-5", "value": 63.4, "slide_pages": ["slide_01.html"]},   # must FAIL
            {"id": "F-6", "value": 999.9, "slide_pages": ["slide_99.html"]},  # must BADREF+FAIL
        ]}
        (d / "fb.json").write_text(json.dumps(fb), encoding="utf-8")
        code = main(["--slides", str(d), "--fact-base", str(d / "fb.json"),
                     "--report", str(d / "r.json")])
        report = json.loads((d / "r.json").read_text())
        ok = (code == 1
              and any("F-5" in f for f in report["failures"])             # missing token caught
              and any("F-6" in f and "BADREF" in f for f in report["failures"])
              and any("PLACEHOLDER" in f and "slide_02" in f for f in report["failures"])
              and any("F-4" in s for s in report["passes_skipped"])       # text-only skipped
              and any("103%" in c for c in report["unverified_candidates"]))
        print("=" * 60)
        print("SELFTEST:", "PASS" if ok else "FAIL", "(exit was", str(code) + ")")
        return 0 if ok else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--slides", default="./slides", help="directory of slide_NN.html files")
    ap.add_argument("--fact-base", help="fact_base.json (mode 1)")
    ap.add_argument("--checks", help="checks.json {slide: [needles]} (mode 2)")
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
        failures, skipped, covered = run_fact_base_mode(slides, fb)
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
        print(f"NOTE   {len(cands)} unverified candidate(s) on slides — add to the fact "
              "base or confirm benign (years, page furniture):")
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
