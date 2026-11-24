## 0. Fail-closed ingestion (G0)
`extract_pdf.py` exits **3** when any page yields < 20 non-space characters.
That is a G0 FAILURE: render the pages (`--render`) and read them, or OCR.
Never reconstruct a question from an empty corpus. Keep `manifest.json`
(sha256 + per-page char census) as the provenance record.
Flags are **candidates**, never confirmed defects; confirm each against the
bound solutions before quoting a "correction" to the user.
