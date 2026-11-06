# Agent Dev Sandbox — deliverables

The complete bundle lives in `agent-dev-sandbox/`. Two archives carry the
identical tree — pick whichever your tooling prefers:

| Archive | Size | Extract |
|---|---|---|
| `agent-dev-sandbox-html.tar.gz` | ~630 KB | `tar xzf agent-dev-sandbox-html.tar.gz` |
| `agent-dev-sandbox.zip` | ~640 KB | `unzip agent-dev-sandbox.zip` |

## What is inside

- `BLUEPRINT.md` — the editable source edition (threat model, ADRs, specs,
  runbooks, 14 sections).
- `BLUEPRINT.pdf` — print edition (cover, TOC, figure, 5 tables).
- `BLUEPRINT.html` — interactive single-file edition: sidebar TOC with
  scroll-spy, full-text search, dark/light theme, Day-0 checklist with
  saved progress, copy buttons. Zero external resources — fully offline.
- `SKILL.md` — phased build procedure (Phase 0–5), security invariants,
  verification gates, full file manifest.
- `files/` — Tier-1 Containerfile (digest-pinned base, fingerprint-checked
  NodeSource key, pinned tools), Squid gateway configs, `allowlist.txt`
  (the egress policy), workspace and CI helper scripts.
- `scripts/` — `00-preflight` … `60-tier2-microvm` (incl. the CI runner and
  the Tier-2 `verify` gate).
- `tests/run-tests.sh` — container-free test suite (units, audit-regression
  tests, doc-lint). Runs green on this bundle.
- `references/` — troubleshooting (§1–§9), hardening, and
  `audit-remediation.md` (the 2026-11-06 external audit: all 22 findings
  validated against this bundle, with the fixes applied and re-verified).
- `pdf-sources/` — editable build sources + the HTML generator and README
  (regenerate the HTML from the MD; the PDF pipeline is documented there).

## State of this bundle

- 2026-11-05: initial blueprint, skill package, PDF/HTML editions, CI profile.
- 2026-11-06 (a): three interaction bugs fixed in the HTML edition
  (copy-payload pollution, clipboard fallback, dead buttons after search).
- 2026-11-06 (b): external read-only audit (22 findings) — every finding
  validated against the bundle (local reproductions, primary-source checks),
  all remediations applied: passable verification gate (C-1/H-1/H-2),
  correct Squid allowlist semantics (H-4), secret-safe snapshots (H-3),
  host-side Tier-2 egress enforcement (H-5), quadlet-correct gateway
  lifecycle (H-6), hardened gateway (M-1), input validation and containment
  (M-4/M-9), dependency and doc alignment (M-2/M-3/M-6/M-10, L-1–L-4),
  plus a test suite. See `references/audit-remediation.md`.

## Verification performed

- `bash -n` clean and **shellcheck 0.10 zero warnings** over all scripts
  (`.shellcheckrc` documents the accepted idioms).
- `tests/run-tests.sh` → **38 passed / 0 failed** (validate_name reserved
  names, resource validation, hostile-meta parsing, allow-domain rules, URL
  redaction, exit-code contract, mock deny-CONNECT 403 semantics, `cp -rP`
  containment, doc-lint incl. MD↔HTML heading parity and pin agreement).
- HTML: structure, anchor integrity, self-containment, JS syntax, content
  parity with the MD, interaction tests in a headless browser, VLM visual QA
  (light/dark/mobile PASS).
- PDF: regenerated from the remediated content; text spot-checks (new claims
  present, stale claims absent) and VLM visual QA of cover, figure and
  tables (PASS).
- Archives: gzip integrity, extraction diff against source, executable-bit
  preservation, zip/tar/disk byte-identity.
- Not verifiable here (no podman/KVM): the live Phase-4 gate
  (`50-verify.sh` → `0 failed`), Squid's privilege drop under the hardened
  capability set, and the QEMU `restrict=on` behavior — these remain the
  evidence gates on the target host, per `references/audit-remediation.md`.
