#!/usr/bin/env python3
"""qa_check.py — machine lint for executive-strategy-deck slides.

Verifies each generated slide against the locked design system:
canvas, CDN scaffold, palette hexes, chart wiring, forbidden patterns.

Usage:
    python qa_check.py <slide.html | directory> [more paths...] [--json]

Exit code 1 if any FAIL-level finding, else 0. WARN findings do not fail
the run but must be reviewed by the agent before delivery.
"""
import json
import re
import sys
from pathlib import Path

# --- Design-system constants (mirror references/design-tokens.md) -------------
ALLOWED_HEX_BASES = {"0A2540", "FF5722", "FF7043", "FEFEFE", "F4F4F4", "FFFFFF"}
ALLOWED_3DIGIT = {"FFF"}
ALLOWED_LOCAL_URL_PREFIXES = ("fonts/MiSans",)

PLACEHOLDER_PATTERNS = [
    r"\blorem\b", r"\bipsum\b", r"\btodo\b", r"\bfixme\b", r"\bxxx\b",
    r"insert (your |the )?(data|text|here)", r"placeholder (text|content|image)",
]
HEX_RE = re.compile(r"#([0-9A-Fa-f]{8}|[0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})")
URL_RE = re.compile(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)")
CLASS_ATTR_RE = re.compile(r'class="([^"]*)"')


def check_file(path: Path):
    """Return a dict with findings list + severity counts for one slide."""
    f = []
    src = path.read_text(encoding="utf-8", errors="replace")
    low = src.lower()

    def fail(msg):
        f.append(("FAIL", msg))

    def warn(msg):
        f.append(("WARN", msg))

    def ok(msg):
        f.append(("OK", msg))

    # --- Structure ---------------------------------------------------------
    if not src.lstrip().startswith("<!DOCTYPE html>"):
        fail("missing <!DOCTYPE html> as first line")
    if not src.rstrip().endswith("</html>"):
        fail("file does not end with </html> (truncated?)")
    else:
        ok("document structure (DOCTYPE + </html>)")

    if src.count('class="ppt-slide') + src.count("class='ppt-slide") == 0:
        # allow extra classes on the same attribute
        if not re.search(r'class="[^"]*ppt-slide', src):
            fail("missing .ppt-slide root element")
    elif src.count("ppt-slide") > 2:
        warn("multiple .ppt-slide elements in one file (one slide per file)")
    else:
        ok(".ppt-slide root element")

    # --- Canvas ------------------------------------------------------------
    if not re.search(r"width:\s*1280px", src):
        fail("canvas width 1280px not declared in CSS")
    if not re.search(r"height:\s*720px", src):
        fail("canvas height 720px not declared in CSS")
    if re.search(r"width:\s*1280px", src) and re.search(r"height:\s*720px", src):
        ok("canvas 1280x720")
    if not re.search(r"overflow:\s*hidden", src):
        warn(".ppt-slide missing overflow:hidden")

    # --- CDN scaffold ------------------------------------------------------
    if "cdn.tailwindcss.com" not in src:
        fail("Tailwind CDN <script> missing")
    if "family=Roboto" not in src:
        fail("Roboto Google Fonts link missing")
    if "family=Material+Icons" not in src:
        fail("Material Icons link missing")
    if "cdn.tailwindcss.com" in src and "family=Roboto" in src and "family=Material+Icons" in src:
        ok("CDN scaffold (Tailwind + Roboto + Material Icons)")
    if not re.search(r"font-family:\s*'Roboto'", src):
        fail("body font-family stack must lead with 'Roboto'")
    if "<html lang=" not in src:
        warn("<html> missing lang attribute")
    if "charset" not in low:
        warn("<meta charset> missing")

    # --- Palette lock ------------------------------------------------------
    bad_hexes = sorted({
        m.group(0) for m in HEX_RE.finditer(src)
        if not _hex_allowed(m.group(1))
    })
    if bad_hexes:
        fail(f"colors outside the locked palette: {', '.join(bad_hexes)} "
             f"(allowed: {', '.join(sorted(ALLOWED_HEX_BASES))} + 8-digit alpha variants)")
    else:
        ok("palette lock (navy/orange system only)")

    # --- Asset references --------------------------------------------------
    if "data:image" in low:
        fail("base64/data-URI image found — use https:// URLs only")
    bad_urls = []
    for m in URL_RE.finditer(src):
        u = m.group(1).strip()
        if u.startswith("data:"):
            fail("base64/data URI image found — use https:// URLs only")
            continue
        if u.startswith("https://"):
            continue
        if any(u.startswith(p) for p in ALLOWED_LOCAL_URL_PREFIXES):
            continue
        bad_urls.append(u)
    if bad_urls:
        fail(f"non-https url() reference(s): {bad_urls} "
             f"(only https:// or the bundled MiSans font path are allowed)")
    else:
        ok("asset references (https only, no local files)")

    if "<img" in low:
        warn("<img> tag found — the system uses CSS background-image, not <img>")

    # --- Brand frame + title ritual ----------------------------------------
    has_header_bar = "h-[85px]" in src
    has_full_bleed = "bg-cover" in src
    if not has_header_bar and not has_full_bleed:
        warn("no brand frame: content pages need the 85px header bar; "
             "cover/closing need a bg-cover photo + overlay")
    else:
        ok("brand frame (header bar or full-bleed cover)")

    ritual = any(
        ("h-1" in attr.split() or "h-1.5" in attr.split())
        and "bg-[#FF5722]" in attr.split()
        for attr in CLASS_ATTR_RE.findall(src)
    )
    if not ritual:
        warn("orange underline ritual (h-1/h-1.5 + bg-[#FF5722]) not found")

    # --- Charts -------------------------------------------------------------
    if "<canvas" in low:
        if "chart.js" not in low:
            fail("<canvas> present but Chart.js CDN script missing")
        elif "new Chart(" not in src:
            fail("<canvas> present but no `new Chart(` initialization")
        else:
            ok("chart wiring (Chart.js CDN + init script)")

    # --- Placeholder hygiene -------------------------------------------------
    for pat in PLACEHOLDER_PATTERNS:
        m = re.search(pat, low)
        if m:
            fail(f"placeholder text found: '{m.group(0)}'")

    # --- Title + density ----------------------------------------------------
    tm = re.search(r"<title>\s*([^<]*?)\s*</title>", src, re.I)
    if not tm or not tm.group(1) or tm.group(1).lower() in {"untitled", "slide", "presentation"}:
        warn("missing or generic <title>")
    words = _visible_word_count(src)
    if words < 30:
        warn(f"visible word count {words} is very low (content pages target 60-120)")
    elif words > 200:
        warn(f"visible word count {words} exceeds 200 — slide is likely overcrowded")
    else:
        ok(f"content density ({words} words)")

    counts = {"FAIL": 0, "WARN": 0, "OK": 0}
    for sev, _ in f:
        counts[sev] += 1
    return {"file": str(path), "words": words, "findings": f, "counts": counts}


def _hex_allowed(hexstr: str) -> bool:
    h = hexstr.upper()
    if len(h) == 3:
        return h in ALLOWED_3DIGIT
    if len(h) == 6:
        return h in ALLOWED_HEX_BASES
    if len(h) == 8:
        return h[:6] in ALLOWED_HEX_BASES
    return False


def _visible_word_count(src: str) -> int:
    text = re.sub(r"<script\b.*?</script>", " ", src, flags=re.S | re.I)
    text = re.sub(r"<style\b.*?</style>", " ", text, flags=re.S | re.I)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    # Material icon ligature names are not content words
    text = re.sub(r"<i\s[^>]*material-icons[^>]*>\s*[^<]*?\s*</i>", " ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    tokens = re.findall(r"[A-Za-z0-9\u4e00-\u9fff][\w\u2019'\-\.,%$]*", text)
    return len(tokens)


def collect_targets(args):
    targets = []
    for a in args:
        p = Path(a)
        if p.is_dir():
            targets.extend(sorted(p.glob("*.html")))
        elif p.suffix.lower() == ".html":
            targets.append(p)
        else:
            print(f"skipping non-html path: {a}", file=sys.stderr)
    return targets


def main(argv):
    as_json = "--json" in argv
    paths = [a for a in argv[1:] if a != "--json"]
    if not paths:
        print(__doc__)
        return 2
    targets = collect_targets(paths)
    if not targets:
        print("no .html files found", file=sys.stderr)
        return 2

    results, seen_titles = [], {}
    for t in targets:
        r = check_file(t)
        tm = re.search(r"<title>\s*([^<]*?)\s*</title>", t.read_text(encoding="utf-8", errors="replace"), re.I)
        if tm and tm.group(1):
            title = tm.group(1).strip()
            if title in seen_titles:
                r["findings"].append(("WARN", f"duplicate <title> with {seen_titles[title]}"))
                r["counts"]["WARN"] += 1
            else:
                seen_titles[title] = str(t)
        results.append(r)

    if as_json:
        print(json.dumps(results, indent=2))
    else:
        for r in results:
            print(f"\n[{Path(r['file']).name}]  ({r['words']} words)")
            for sev, msg in r["findings"]:
                icon = {"OK": "  PASS", "WARN": "  WARN", "FAIL": "!!FAIL"}[sev]
                print(f"{icon}  {msg}")
        total = {"FAIL": 0, "WARN": 0}
        for r in results:
            total["FAIL"] += r["counts"]["FAIL"]
            total["WARN"] += r["counts"]["WARN"]
        print(f"\nSUMMARY: {len(results)} file(s) — {total['FAIL']} FAIL, {total['WARN']} WARN")
        if total["FAIL"] == 0 and total["WARN"] == 0:
            print("All checks passed.")
    return 1 if any(r["counts"]["FAIL"] for r in results) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
