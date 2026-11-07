# Agent Dev Sandbox — deliverables

The complete bundle lives in `agent-dev-sandbox/`. This archive carries the
identical tree:

| Archive | Size | Extract |
|---|---|---|
| `agent-dev-sandbox-html.tar.gz` | ~656 KB | `tar xzf agent-dev-sandbox-html.tar.gz` |

This archive supersedes every earlier distribution (`agent-dev-sandbox-html.tar.gz`
v1, `agent-dev-sandbox-html-v2.tar.gz`, `agent-dev-sandbox.zip`): it carries
the full 2026-11-06 audit remediation, the 2026-11-06(c) lint fix, and the
2026-11-07 second-pass validation fixes.

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
  validated against this bundle, with the fixes applied and re-verified —
  plus the 2026-11-07 second-pass validation).
- `pdf-sources/` — editable build sources + the HTML generator and README
  (regenerate the HTML from the MD; the PDF pipeline is documented there).
- `generate_blueprint_pdf.py` — the ReportLab body generator behind the PDF
  edition, kept for provenance (not runnable inside the bundle alone; see
  `pdf-sources/README.md`).

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
  files/*.sh` must stay clean) now passes.
- 2026-11-07: **second-pass validation of the remediation** — all 22
  finding-fixes re-verified against executable truth (tests, shellcheck,
  byte-identical HTML regeneration from the MD, PDF text spot-checks);
  four residual defects found, fixed and regression-tested: the
  `next_free_range` colon-parsing bug that silently restored the L-2
  subuid overlap on shared hosts, `set -euo pipefail` aborts in the CI
  and Tier-2 probes exactly when the gateway is down (audit evidence lost
  instead of recorded), the gateway status-probe `000000` append, and
  vacuous-pass guards (dead exec channel in `50-verify.sh`, unreadable
  nftables ruleset in the Tier-2 check). Documentation reconciled:
  `generate_blueprint_pdf.py` added to the SKILL manifest, pdf-sources
  README corrected, doc-lint description aligned with the actual tests.
  Suite grew 38 → 45 (all green). See `references/audit-remediation.md`,
  "Second-pass validation". Packaged as `agent-dev-sandbox-html.tar.gz`.

## Verification performed

- `bash -n` clean and **shellcheck zero warnings** over all scripts —
  remediation-era run on 0.10, re-verified on 0.11.0 after (c) and again
  after the 2026-11-07 second pass (`.shellcheckrc` documents the accepted
  idioms).
- `tests/run-tests.sh` → **45 passed / 0 failed** (validate_name reserved
  names, resource validation, hostile-meta parsing, allow-domain rules, URL
  redaction, exit-code contract, mock deny-CONNECT 403 semantics plus
  set -e probe survival, `cp -rP` containment, doc-lint incl. MD↔HTML
  heading parity and pin agreement, and the colon-parsing `next_free_range`
  regressions) — re-run green after the second pass.
- HTML: structure, anchor integrity, self-containment, JS syntax, content
  parity with the MD, interaction tests in a headless browser, VLM visual QA
  (light/dark/mobile PASS) — from the (b)/(c) rounds; the 2026-11-07 pass
  re-verified MD→HTML parity by regenerating the edition from the MD and
  diffing **byte-identical** (BLUEPRINT.md is unchanged by the second pass).
- PDF: regenerated from the remediated content; text spot-checks (new claims
  present, stale claims absent) and VLM visual QA of cover, figure and
  tables (PASS) — from the (b) round; the 2026-11-07 pass re-ran the text
  spot-checks green (PDF stays in sync: its MD source is unchanged).
- Archive: gzip integrity, extraction diff against the source tree,
  executable-bit preservation (34/34), no nested archives, per-file md5
  tar↔disk agreement — verified for this archive after the second pass.
- Not verifiable here (no podman/KVM): the live Phase-4 gate
  (`50-verify.sh` → `0 failed`), Squid's privilege drop under the hardened
  capability set, and the QEMU `restrict=on` behavior — these remain the
  evidence gates on the target host, per `references/audit-remediation.md`.
