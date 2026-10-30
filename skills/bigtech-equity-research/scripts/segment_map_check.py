#!/usr/bin/env python3
"""segment_map_check.py — mechanical staleness gate for the ASC 280 segment map.

Comparative reports 6/7 (finding H-3 / synthesized #5): the segment map's
`last_verified_against_filing` staleness control was advisory — the SKILL.md told the
agent to check the vintage, but nothing failed the build when a stale map met a newer
filing. A stale map produces a confidently wrong variance table that PASSES the numeric
audit (the numbers match the fact base) while misattributing the cause — the most
insidious failure mode in the family. This gate turns the prose rule into an exit code.

Doctrine it enforces (reference/segment-maps.md is the human-readable statement):
  - The filing's own segment note (ASC 280, usually Note 10-15 of the 10-Q/10-K) is the
    source of truth; the map is a cached baseline expectation.
  - If the filing you are using postdates the map's `verified_through`, STOP: re-verify
    the segment structure against that filing's segment note, update segment-maps.md AND
    segment-maps.json (bump segment_map_version), then re-run this gate.
  - A company absent from the map is not an error in the analysis — it means the map has
    no cached expectation: extract the segment structure from the filing directly and
    add it to the map (report-6's dynamic-extraction doctrine, made explicit).

Usage:
  python3 segment_map_check.py --map reference/segment-maps.json \
      --filing-date 2026-10-28 [--company GOOGL] [--form 10-Q]
  python3 segment_map_check.py --selftest

--filing-date : publication date (YYYY-MM-DD) of the 10-Q/10-K/8-K you are actually using.
--company     : optional ticker; when given, the map must have an entry for it.
Exit codes: 0 gate passed, 1 stale/unknown — fix the map (or the filing) before building
the variance table, 2 usage/environment error.
"""
import argparse
import datetime as _dt
import json
import pathlib
import sys


def _load_map(map_path: pathlib.Path) -> dict:
    try:
        data = json.loads(map_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"ERROR  cannot read segment map {map_path}: {e}", file=sys.stderr)
        sys.exit(2)
    if "companies" not in data or "last_verified_against_filing" not in data:
        print(f"ERROR  segment map {map_path} lacks 'companies' or "
              "'last_verified_against_filing'", file=sys.stderr)
        sys.exit(2)
    return data


def _parse_date(s: str):
    try:
        return _dt.date.fromisoformat(str(s).strip())
    except ValueError:
        return None


def check_map(map_path: pathlib.Path, filing_date: str, company: str = "",
              form: str = "") -> int:
    data = _load_map(map_path)
    verified = _parse_date(
        (data.get("last_verified_against_filing") or {}).get("verified_through", ""))
    fdate = _parse_date(filing_date)
    if fdate is None:
        print(f"ERROR  --filing-date must be YYYY-MM-DD, got {filing_date!r}",
              file=sys.stderr)
        return 2
    version = data.get("segment_map_version", "?")
    forms = (data.get("last_verified_against_filing") or {}).get("forms", "?")

    problems = []
    if verified is None:
        problems.append("map has no parseable verified_through date "
                        f"({(data.get('last_verified_against_filing') or {}).get('verified_through')!r})")
    elif fdate > verified:
        problems.append(
            f"STALE: the filing you are using ({filing_date}{f' {form}' if form else ''}) "
            f"postdates the segment map's verified_through ({verified}). Re-verify the "
            "segment structure against THIS filing's own segment note, update "
            "segment-maps.md and segment-maps.json (bump segment_map_version), then "
            "re-run this gate — a variance table on a stale map ties out to nothing.")

    if company:
        entry = data["companies"].get(company.upper())
        if entry is None:
            problems.append(
                f"UNKNOWN: no map entry for {company.upper()} — the map has no cached "
                "expectation for this name. Extract the reportable segments directly "
                "from the filing's segment note (source of truth), add the entry to "
                "segment-maps.json + segment-maps.md, and re-run.")
        else:
            print(f"map entry {company.upper()}: {', '.join(entry['reportable_segments'])}")

    if problems:
        for p in problems:
            print(f"SEGMENT-MAP {p}")
        print(f"map: segment_map_version={version} verified against {forms} "
              f"through {verified}")
        return 1

    print(f"SEGMENT-MAP: OK — filing {filing_date} is covered by map version "
          f"{version} (verified against {forms} through {verified})")
    return 0


def selftest() -> int:
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        d = pathlib.Path(td)
        m = d / "segment-maps.json"
        m.write_text(json.dumps({
            "segment_map_version": "test-1",
            "last_verified_against_filing": {"forms": "FY2026 10-K",
                                             "verified_through": "2026-10-30"},
            "companies": {"GOOGL": {"reportable_segments": ["Google Services",
                                                             "Google Cloud", "Other Bets"]}}
        }), encoding="utf-8")
        ok = check_map(m, "2026-10-28", company="GOOGL") == 0          # covered
        ok = ok and check_map(m, "2026-09-30") == 0                    # older filing, fine
        ok = ok and check_map(m, "2026-11-12") == 1                    # future filing -> STALE
        ok = ok and check_map(m, "2026-10-28", company="MSFT") == 1    # unknown ticker
        ok = ok and check_map(m, "2026-10-28", company="googl") == 0   # case-insensitive
        ok = ok and check_map(m, "not-a-date") == 2                    # usage error
        print("=" * 60)
        print("SELFTEST:", "PASS" if ok else "FAIL")
        return 0 if ok else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    here = pathlib.Path(__file__).resolve().parent
    ap.add_argument("--map", default=str(here.parent / "reference" / "segment-maps.json"),
                    help="segment-maps.json (default: the skill's bundled copy)")
    ap.add_argument("--filing-date", default=None,
                    help="publication date (YYYY-MM-DD) of the filing being used "
                         "(required unless --selftest)")
    ap.add_argument("--company", default="",
                    help="optional ticker covered by the variance table")
    ap.add_argument("--form", default="",
                    help="optional form type echo (10-Q / 10-K / 8-K) for messages")
    ap.add_argument("--selftest", action="store_true", help="run built-in self-test and exit")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.filing_date:
        print("ERROR  --filing-date is required (or --selftest)", file=sys.stderr)
        return 2
    return check_map(pathlib.Path(args.map), args.filing_date,
                     company=args.company, form=args.form)


if __name__ == "__main__":
    sys.exit(main())
