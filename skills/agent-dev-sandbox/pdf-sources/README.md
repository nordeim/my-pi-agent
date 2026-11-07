# pdf-sources — edition build sources

This directory holds everything needed to regenerate the blueprint's derived
editions, so the three hand-synced files (MD / HTML / PDF) never drift
silently (audit L-4).

## Files

| File | Role |
|---|---|
| `generate_html.py` | Regenerates `../BLUEPRINT.html` from `../BLUEPRINT.md` (self-contained: inline CSS/JS, inline SVG diagram, checklist injection) |
| `html_template.css` / `html_template.js` | The interactive edition's stylesheet and behavior (search, theme, scroll-spy, copy buttons, checklist) — inlined by the generator |
| `cover.html` | PDF cover page source (rendered to PDF at build time) |
| `diagram.html` / `diagram.png` | The §5 system-design figure (HTML source + rendered PNG used by the PDF) |
| `BLUEPRINT-cover-preview.jpg` | Visual preview of the cover for quick review |

## Regenerate the HTML edition

Requires: `python3` + the `markdown` package (`sudo apt install python3-markdown`,
or `pip install markdown`).

```bash
cd pdf-sources/
./generate_html.py        # writes ../BLUEPRINT.html
```

Run `../tests/run-tests.sh` afterwards — its doc-lint section asserts that
every `## ` heading in BLUEPRINT.md exists in BLUEPRINT.html and that no
stale markers remain in either edition.

## Regenerating the PDF edition

`BLUEPRINT.pdf` is produced by a ReportLab-based pipeline (cover rendered
from `cover.html`, body typeset from `BLUEPRINT.md`, merged and normalized
to A4). The body generator IS part of this bundle — it lives at the bundle
root as `generate_blueprint_pdf.py` — but it is kept for **provenance**, not
as a turnkey script: it imports the producing repository's `./skills/pdf`
helper package (`install_font_fallback`, run from that repo's root) and
expects a cover-render + merge step (`html2poster.js`) around it, so it
cannot be re-run from inside this bundle alone. To refresh the PDF after
editing `BLUEPRINT.md`: re-run the PDF pipeline you used to produce it
(body → cover → merge) in the producing environment, then verify with
`pdftotext BLUEPRINT.pdf - | grep '<a heading or fact you changed>'` that
the change landed.

## Rule

`BLUEPRINT.md` is the source of truth. Never hand-edit `BLUEPRINT.html` —
edit the MD, regenerate, and let the tests catch drift.
