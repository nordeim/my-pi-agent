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

PLACEHOLDER_PATTERNS = [
    r"lorem", r"\btodo\b", r"placeholder", r"\btbd\b", r"\bxxx\b", r"\bnan\b",
    r"\bundefined\b", r"insert (data|here|numbers)", r"foo bar", r"【",
]
NUM_RE = re.compile(r"-?\d[\d,]*(?:\.\d+)?")
EXTRACT_RE = re.compile(r"\$\d[\d,\.]*\s?[BM]?|\d+\.\d+%?|\d{2,}%")
CONFIDENCE_LABELS = {"Verified", "Reasoned", "Assumed", "Unverifiable",
                     "Reasoned (derived)", "Reasoned (judged)"}


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
             "retrieved_at": "2026-10-30", "confidence": "Verified"},
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
        ok = (code_ok == 0 and code_extra == 1 and code_furn == 0 and code_bad == 1)
        print("=" * 60)
        print("SELFTEST:", "PASS" if ok else "FAIL",
              f"(clean {code_ok}, unregistered {code_extra}, "
              f"furniture {code_furn}, schema {code_bad})")
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
