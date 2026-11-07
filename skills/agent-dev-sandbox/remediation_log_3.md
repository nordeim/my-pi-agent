# Remediation log 3 — third-pass remediation session (2026-11-07)

Six-phase workflow applied to `remediation_log_2.md` (the third-pass review,
R-1–R-8): every finding validated against executable truth before any edit,
then remediated. Canonical dispositions live in
`references/audit-remediation.md` ("Third-pass review"); this file is the
session-level provenance.

## 1. ANALYZE

- Repo refreshed to `origin/main` (6bff327a). Divergence vs the local tree:
  upstream had absorbed the second-pass fixes (content-identical), added
  `remediation_log_1.md`/`remediation_log_2.md`,
  `build-agent-dev-sandbox-html-tar.sh`, an updated `SKILL.md`
  `allowed-tools` line (= the R-2 fix, applied by the repo owner), and
  deleted the superseded `docs/` copies.
- Read in full: `remediation_log_2.md` (both parts), `remediation_log_1.md`,
  `SKILL.md`, `README.md`, `BLUEPRINT.md` (all 539 lines), `references/
  audit-remediation.md`, `tests/run-tests.sh`, `files/ci-setup.sh`,
  `files/squid/allowlist.txt`, `files/squid/squid.conf`,
  `build-agent-dev-sandbox-html-tar.sh`, plus the relevant sections of
  `45-ci-run.sh`, `40-workspace.sh`, `50-verify.sh`, `00-preflight.sh`,
  `generate_blueprint_pdf.py`, `pdf-sources/*`.
- Baseline gates on the unmodified tree: `bash -n` clean (13 files),
  ShellCheck 0.11.0 zero warnings, `tests/run-tests.sh` 45/45 — which
  already disproved R-1's "truncated suite" premise.
- Arena site re-checked (per remediation_log_2's caveat): still serves only
  the JS-rendered shell ("Audit Report — agent-dev-sandbox" + boilerplate);
  no new findings. `references/audit-remediation.md` stays canonical.

## 2. VALIDATE — findings vs executable truth

| ID | Verdict |
|---|---|
| R-1 | False alarm — suite complete (243 lines) and green (45/45 executed); "23 lines" was the reviewing session's raw-view truncation |
| R-2 | Valid finding, already fixed upstream — byte-for-byte the recommended line |
| R-3 | Partially valid — podman/jq/shellcheck are genuine host requirements (scripts + preflight + maintenance contract); **git is not** (exhaustive grep: every host-side git invocation runs inside a container; the image bakes git) |
| R-4 | Valid — header stopped at the 2026-11-06 pass; requires MD + HTML + PDF edition lockstep |
| R-5 | Valid — pre-build size/count claims |
| R-6 | Gap valid; **suggested hardening hazardous** — a hard `audit_fail=1` on a `max` reading contradicts `50-verify.sh`, which treats `pids.max=max` as a SOFT warning (rootless cgroup delegation variance, troubleshooting §5); it would fail every CI run on non-delegated hosts — stricter than the Tier-1 gate it mirrors |
| R-7 | Valid — `squid.conf` allows only 80/443; allowlist silent about it |
| R-8 | Valid — no provenance recorded |

Pipeline validation before relying on it: HTML regeneration on the
unchanged MD produced a byte-identical file except the rendered-date chip;
the PDF body generator reproduced a text-identical 16-page PDF (cover page
reused from the existing edition, body regenerated, qpdf merge).

New defects found in the repo's `build-agent-dev-sandbox-html-tar.sh`
while validating it: **B-1** fatal tar `-C skills` path (no such dir from
the tmpdir root — the archive step could never succeed); **B-2** archive
written inside the bundle being archived; **B-3** the R-4 patch needle
spanned a line wrap (silent no-op); **B-4** lint gates missed the
extensionless `files/ws-shell`; **B-5** built the superseded archive name;
**B-6** patch payloads diverged from the validated fixes (R-3 listed git).

## 3-4. PLAN → IMPLEMENT

Tests first, then fixes (failing-before captured):

1. `tests/run-tests.sh` group 11 (cgroup-cap evidence): structural
   assertion + set -e survival lock — **failing-before: 46 passed / 1
   failed**; then `files/ci-setup.sh` R-6 (pids_max/memory_max evidence
   fields in `isolation-audit.json`, no fail-on-max, header comment,
   echo line) — **after: 47/47**.
2. `files/squid/allowlist.txt` — port note (R-7).
3. `SKILL.md` — R-3 bins `["bash","sudo","podman","jq","shellcheck"]`;
   manifest rows for the remediation logs and the build script; tests row
   gains R-6; the maintenance shellcheck gate now includes `files/ws-shell`.
4. `BLUEPRINT.md` — R-4 header (second + third pass) and R-6 §12 wording;
   `BLUEPRINT.html` regenerated; `generate_blueprint_pdf.py` lines synced
   (285 header, 442 §12); PDF body regenerated; cover reused; merged —
   all three editions in sync.
5. `references/audit-remediation.md` — audit provenance (R-8) + the
   third-pass disposition tables (R-1–R-8, B-1–B-6).
6. `build-agent-dev-sandbox-html-tar.sh` — B-1…B-6 fixed (tar path, output
   dir, wrap-tolerant guarded patches, ws-shell in gates, v2 archive name,
   payload alignment, presence-guarded R-2 rewrite); verified end-to-end
   against the live GitHub repo (patches applied, 45/45 gates green,
   archive built and listed).
7. `README.md` — refreshed for `agent-dev-sandbox-html-v2.tar.gz`
   (measured size, sha256, test count 47, state entry, verification list).

## 5. VERIFY

On the final tree: `bash -n` clean (14 shell files), ShellCheck 0.11.0
zero warnings, `tests/run-tests.sh` **47 passed / 0 failed**, doc-lint
green (heading parity, stale markers, pins), HTML regenerated from the MD,
PDF text spot-checks (new claims present, stale markers absent), jq program
shape-checked, archive battery (gzip integrity, extraction diff ≡ source
tree, executable bits, md5 agreement, no nested archives), and the fixed
build script executed end-to-end. Unverifiable here (no podman/KVM): the
live Phase-4 gate, Tier-2 verify, Squid privilege drop — unchanged
ownership, per `references/audit-remediation.md`.

## 6. DELIVER

Commit on `main`; archive `agent-dev-sandbox-html-v2.tar.gz` built from the
committed tree (`tar -czf … -C skills agent-dev-sandbox`). Supersedes the
2026-11-07 `agent-dev-sandbox-html.tar.gz` distribution (and the unrelated
2026-11-05 archive that briefly used the same `-v2` name — disambiguated by
the sha256 in `README.md`).
