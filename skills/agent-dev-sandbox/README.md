# Agent Dev Sandbox — deliverables

The complete bundle lives in `agent-dev-sandbox/`. Two archives carry the
identical tree — pick whichever your tooling prefers:

| Archive | Size | Extract |
|---|---|---|
| `agent-dev-sandbox-html-v2.tar.gz` | ~634 KB | `tar xzf agent-dev-sandbox-html-v2.tar.gz` |
| `agent-dev-sandbox.zip` | ~648 KB | `unzip agent-dev-sandbox.zip` |

`agent-dev-sandbox-html-v2.tar.gz` supersedes the earlier
`agent-dev-sandbox-html.tar.gz` (it carries the full audit remediation plus
the lint fix below; the old archive has been removed to avoid ambiguity).

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
- 2026-11-06 (c): post-remediation lint hygiene — `files/profile-agent-env.sh`
  gained a `# shellcheck shell=sh` directive; as a sourced profile.d snippet
  it previously tripped SC1008/SC1113/SC2096 and escaped linting entirely.
  The bundle's own documented gate (SKILL.md: `shellcheck -x scripts/*.sh
  files/*.sh` must stay clean) now passes. Re-verified: tests 38/38, HTML
  parity, archive integrity. Packaged as `agent-dev-sandbox-html-v2.tar.gz`.

## Verification performed

- `bash -n` clean and **shellcheck zero warnings** over all scripts —
  remediation-era run on 0.10, re-verified on 0.11.0 after (c)
  (`.shellcheckrc` documents the accepted idioms).
- `tests/run-tests.sh` → **38 passed / 0 failed** (validate_name reserved
  names, resource validation, hostile-meta parsing, allow-domain rules, URL
  redaction, exit-code contract, mock deny-CONNECT 403 semantics, `cp -rP`
  containment, doc-lint incl. MD↔HTML heading parity and pin agreement) —
  re-run green after (c).
- HTML: structure, anchor integrity, self-containment, JS syntax, content
  parity with the MD, interaction tests in a headless browser, VLM visual QA
  (light/dark/mobile PASS).
- PDF: regenerated from the remediated content; text spot-checks (new claims
  present, stale claims absent) and VLM visual QA of cover, figure and
  tables (PASS).
- Archives (v2 tar + refreshed zip): gzip integrity, extraction diff against
  source, executable-bit preservation (34/34), no nested archives, per-file
  md5 tar↔zip↔disk agreement; the v2 tar differs from the remediation tar by
  exactly the one directive line in `files/profile-agent-env.sh`.
- Not verifiable here (no podman/KVM): the live Phase-4 gate
  (`50-verify.sh` → `0 failed`), Squid's privilege drop under the hardened
  capability set, and the QEMU `restrict=on` behavior — these remain the
  evidence gates on the target host, per `references/audit-remediation.md`.
