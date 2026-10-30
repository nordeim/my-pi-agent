#!/usr/bin/env python3
"""note_audit.py — lite delivery audit for single-file HTML research notes.

The lite members of the big-tech research family (big-tech-earnings-postmortem,
bigtech-equity-research) state the same hard rules as the flagship
(analyzing-us-bigtech-stocks) but historically shipped no executable gate of
their own — compliance depended on operator discipline. This script is that
gate: a trimmed port of the flagship's fact_base_audit.py checks that require
no fact base.

What it enforces on the delivered note:

  1. Placeholder scan (always): visible text must contain no `lorem`, `todo`,
     `tbd`, `xxx`, `nan`, `undefined`, `placeholder`, `insert data/numbers`,
     `foo bar`, or fullwidth-bracket `【` tokens. Script/style blocks are not
     reader-visible and are skipped (same scoping rule as the flagship).
  2. Disclosure needles (--checks FILE): strings that MUST appear in the
     visible text — the compliance disclaimer, the verification-status line,
     the "Reasoned allocation — not a measured decomposition" label when a
     quantified waterfall is present, and any other mandatory disclosure the
     skill's assets/checks.json lists.
  3. Conditional disclosures: `required_if` entries — {"if_any": [triggers],
     "then": needle} — a needle that becomes mandatory only when one of its
     trigger substrings appears (e.g. the waterfall label only when the note
     quantifies an allocation).
  4. Scoped needles (round 3, reports 6/7 M-2): a `required_if` entry may add
     "near": [tokens] and "within": N (default 400) — the disclosure must
     then appear within N normalized characters of one of the near tokens,
     not just anywhere in the document. A label buried in the footer while
     the body presents the waterfall as a measured decomposition is an inert
     disclosure; scoping makes the needle contextual. Entries without "near"
     keep the document-wide behavior. Choose near tokens that do NOT appear
     inside the disclosure string itself, or the scoping is vacuous.

Usage:
  python3 note_audit.py --note <file.html> --checks <checks.json>
  python3 note_audit.py --note <file.html>                # placeholder scan only
  python3 note_audit.py --note <file.html> --checks <checks.json> --json
  python3 note_audit.py --selftest

--json (round 5, reports 10/11 — CI/CD integration): stdout carries a
machine-readable summary {"tool", "ok", "failure_count", "failures"}; the
human-readable diagnostics go to stderr so pipelines can consume stdout
directly. Exit codes unchanged.

Exit codes: 0 clean, 1 failures found, 2 usage/environment error.

Needle matching is normalization-tolerant (em/en-dash, minus sign, NBSP,
apostrophes, case-insensitive, whitespace-squashed), so a disclosure printed
with typographic dashes still satisfies the literal needle.

The copies bundled in big-tech-earnings-postmortem/scripts/ and
bigtech-equity-research/scripts/ are byte-identical by design;
tests/test_note_audit.py fails the build if they drift apart.
"""
import argparse, json, re, sys, tempfile, pathlib

TOOL_ID = "note_audit.py (big-tech research family, round 5)"

PLACEHOLDER_PATTERNS = [
    r"lorem", r"\btodo\b", r"placeholder", r"\btbd\b", r"\bxxx\b", r"\bnan\b",
    r"\bundefined\b", r"insert (data|here|numbers)", r"foo bar", r"【",
]


def norm(s: str) -> str:
    """Normalize dashes (hyphen/en/em/minus), NBSP, apostrophes, whitespace; lowercase."""
    s = (s.replace("\u2013", "-").replace("\u2014", "-")
          .replace("\u2212", "-").replace("\u00a0", " ").replace("\u2019", "'"))
    return re.sub(r"\s+", " ", s).strip().lower()


def visible_text(html: str) -> str:
    """Strip <script>/<style> and tags — audit only what readers see."""
    html = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    return re.sub(r"<[^>]+>", " ", html)


def scan_placeholders(fname: str, raw_html: str) -> list:
    fails = []
    low = norm(visible_text(raw_html))
    for pat in PLACEHOLDER_PATTERNS:
        if re.search(pat, low):
            fails.append(f"PLACEHOLDER  {fname}  matches /{pat}/")
    return fails


def _all_positions(hay: str, needle: str) -> list:
    """Every occurrence index of needle in hay (needle is already normalized)."""
    out, start = [], 0
    while needle:
        i = hay.find(needle, start)
        if i == -1:
            return out
        out.append(i)
        start = i + 1
    return out


def run_needle_checks(fname: str, raw_html: str, checks: dict) -> list:
    """Required and conditional disclosure needles, on normalized visible text.

    Conditional entries may be scoped with "near"/"within": the disclosure
    must sit within `within` normalized characters of a near token, so a
    qualifying label actually qualifies the content it applies to."""
    fails = []
    body = norm(visible_text(raw_html))
    for needle in checks.get("required", []):
        if norm(str(needle)) not in body:
            fails.append(f"MISSING      {fname}  required disclosure absent: "
                         f"'{needle}'")
    for spec in checks.get("required_if", []):
        triggers, then = spec.get("if_any", []), spec.get("then", "")
        if not triggers or not then:
            fails.append(f"CHECKS-BAD   {fname}  required_if entry needs "
                         "'if_any' (non-empty list) and 'then' (string)")
            continue
        if not any(norm(str(t)) in body for t in triggers):
            continue
        n_then = norm(str(then))
        if n_then not in body:
            fails.append(f"MISSING      {fname}  conditional disclosure absent: "
                         f"'{then}' (triggered by {triggers!r})")
            continue
        near, within = spec.get("near"), spec.get("within", 400)
        if not near:
            continue
        near_pos = sorted({i for t in near for i in _all_positions(body, norm(str(t)))
                           if norm(str(t))})
        then_pos = _all_positions(body, n_then)
        if near_pos and not any(min(abs(p - q) for q in near_pos) <= int(within)
                                for p in then_pos):
            fails.append(f"SCOPED       {fname}  disclosure '{then}' present but "
                         f"> {within} chars from its trigger context {near!r} — "
                         "a footer disclosure does not qualify the content it "
                         "applies to (move it next to the trigger)")
    return fails


def selftest() -> int:
    with tempfile.TemporaryDirectory() as td:
        d = pathlib.Path(td)
        clean = ("<html><body><h1>GOOG —12.29%</h1>"
                 "<p>Verification status: lite audit gates passed — "
                 "disclosure needles + render audit.</p>"
                 "<p>Informational only — not investment advice.</p>"
                 "</body></html>")
        (d / "note_clean.html").write_text(clean, encoding="utf-8")
        # Visible TODO must fail; a TODO inside a <script> must not.
        (d / "note_placeholder.html").write_text(
            "<html><head><script>var todo = 1;</script></head><body>"
            "<p>TODO fill this in</p></body></html>", encoding="utf-8")
        # Waterfall present but the Reasoned-allocation label absent → the
        # conditional disclosure must fire.
        (d / "note_waterfall.html").write_text(
            "<html><body><h2>Driver decomposition</h2>"
            "<p>Waterfall: benchmark −1.5, FCF −3.9 …</p>"
            "<p>Verification status: lite audit gates passed — "
            "disclosure needles + render audit.</p>"
            "<p>Informational only — not investment advice.</p>"
            "</body></html>", encoding="utf-8")
        # Scoped needle: the label is present but parked in the footer far
        # from the waterfall it must qualify → SCOPED failure (round 3).
        # NOTE: the near token must not appear inside the disclosure string
        # itself, or the scoping is vacuous — use content tokens ("waterfall").
        filler = "<p>" + ("Section narrative content. " * 60) + "</p>"
        (d / "note_scoped.html").write_text(
            "<html><body><h2>Driver decomposition</h2>"
            "<p>Waterfall: benchmark −1.5, FCF −3.9 …</p>" + filler +
            "<p>Reasoned allocation — not a measured decomposition.</p>"
            "<p>Verification status: lite audit gates passed — "
            "disclosure needles + render audit.</p>"
            "<p>Informational only — not investment advice.</p>"
            "</body></html>", encoding="utf-8")
        checks = {
            "required": ["Informational only — not investment advice",
                         "Verification status:"],
            "required_if": [
                {"if_any": ["waterfall", "decomposition", "allocation"],
                 "then": "Reasoned allocation — not a measured decomposition",
                 "near": ["waterfall"], "within": 400},
            ],
        }
        (d / "checks.json").write_text(json.dumps(checks), encoding="utf-8")

        r_clean = main(["--note", str(d / "note_clean.html"),
                        "--checks", str(d / "checks.json")])
        r_place = main(["--note", str(d / "note_placeholder.html"),
                        "--checks", str(d / "checks.json")])
        r_wf = main(["--note", str(d / "note_waterfall.html"),
                     "--checks", str(d / "checks.json")])
        r_sc = main(["--note", str(d / "note_scoped.html"),
                     "--checks", str(d / "checks.json")])
        # Script-block TODO alone must not fail; placeholder scan only, no
        # checks file (missing 'Verification status:' would fail under checks).
        (d / "note_js.html").write_text(
            "<html><head><script>var todo = 1;</script></head><body>"
            "<p>Close $282.32</p></body></html>", encoding="utf-8")
        r_js = main(["--note", str(d / "note_js.html")])
        # Round 5 — --json: stdout is a machine-readable summary.
        import contextlib, io
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            r_json = main(["--note", str(d / "note_placeholder.html"),
                           "--json"])
        try:
            payload = json.loads(buf.getvalue())
            json_ok = (payload.get("ok") is False
                       and payload.get("failure_count", 0) >= 1
                       and payload.get("tool", "").startswith("note_audit"))
        except json.JSONDecodeError:
            json_ok = False
        ok = (r_clean == 0 and r_place == 1 and r_wf == 1 and r_js == 0
              and r_sc == 1 and r_json == 1 and json_ok)
        print("=" * 60)
        print("SELFTEST:", "PASS" if ok else "FAIL",
              f"(clean {r_clean}, placeholder {r_place}, "
              f"waterfall-label {r_wf}, js-scope {r_js}, scoped {r_sc}, "
              f"json {r_json})")
        return 0 if ok else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--note", help="the delivered single-file HTML note")
    ap.add_argument("--checks",
                    help="checks.json with 'required' needles and optional "
                         "'required_if' conditional disclosures "
                         "(see assets/checks.json)")
    ap.add_argument("--report", help="optional path for a JSON audit report")
    ap.add_argument("--json", action="store_true",
                    help="machine-readable summary on stdout (diagnostics go "
                         "to stderr) for CI/CD integration (round 5)")
    ap.add_argument("--selftest", action="store_true",
                    help="run built-in self-test and exit")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.note:
        print("ERROR  --note is required (or --selftest)", file=sys.stderr)
        return 2
    note = pathlib.Path(args.note)
    if not note.is_file():
        print(f"ERROR  note file not found: {note}", file=sys.stderr)
        return 2

    failures = []
    try:
        raw = note.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        print(f"ERROR  cannot read {note}: {e}", file=sys.stderr)
        return 2
    real_stdout = sys.stdout
    if args.json:
        sys.stdout = sys.stderr      # diagnostics to stderr; stdout stays JSON
    try:
        failures += scan_placeholders(note.name, raw)

        checks = {}
        if args.checks:
            cpath = pathlib.Path(args.checks)
            if not cpath.is_file():
                sys.stdout = real_stdout
                print(f"ERROR  checks file not found: {cpath}", file=sys.stderr)
                return 2
            try:
                checks = json.loads(cpath.read_text(encoding="utf-8"))
            except json.JSONDecodeError as e:
                sys.stdout = real_stdout
                print(f"ERROR  checks file is not valid JSON: {e}", file=sys.stderr)
                return 2
            if not isinstance(checks, dict):
                sys.stdout = real_stdout
                print("ERROR  checks file must be a JSON object", file=sys.stderr)
                return 2
            failures += run_needle_checks(note.name, raw, checks)
        else:
            print(f"Scanned {note.name} — placeholder scan only (no checks file "
                  "given; the skill's assets/checks.json is the default gate).")
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
        }, indent=2))
        return 0 if not failures else 1

    print("=" * 60)
    print("AUDIT RESULT:", "CLEAN" if not failures else f"{len(failures)} failure(s)")
    for f in failures:
        print(" ", f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
