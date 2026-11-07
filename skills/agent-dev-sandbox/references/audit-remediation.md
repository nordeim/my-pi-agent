# Audit remediation — 2026-11-06

Response to the external read-only audit of this bundle (22 findings:
1 critical, 6 high, 11 medium, 4 low). This document records, for every
finding, whether it was **validated** against this bundle, the evidence, and
the remediation applied. Sections marked **deferred to live host** cannot be
concluded in a container-less environment and remain owned by
`scripts/50-verify.sh` (Tier 1) and `60-tier2-microvm.sh verify` (Tier 2).

Validation methods used here: every cited file read in full; shell-verifiable
claims reproduced in isolation (regex, mock 403-CONNECT proxy + curl
semantics, meta-file injection, `cp -r` symlink following, pipeline env
scoping); external claims verified against primary sources (podman v5.4
source and docs, Squid docs, QEMU docs, Node.js docs, the bun installer
source, the budget-wiser repository, live Docker Hub and NodeSource
endpoints).

## Verdicts and dispositions

| ID | Sev | Verdict | Evidence summary | Disposition |
|---|---|---|---|---|
| C-1 | CRIT | **Valid (all 3 defects)** | `__verify` reproduced as rejected by the shipped regex; mock deny-CONNECT proxy shows `%{http_code}`=000 with 403 only in `%{http_connect}` (curl exit 56); ci-setup expression yields `000000`, never `403` | Fixed: reserved-name channel for internal callers; CONNECT-denial asserted on `%{http_connect}`; curl status captured separately. Regression tests added |
| H-1 | HIGH | **Valid** | `ws()` merges stderr; `v()` discards status; `[ -n "$OUT" ]` passes on error text (reproduced); direct-egress test is DNS-confounded (resolves by name) | Fixed: per-tool version-regex + exit-status checks; route test now uses an IP literal and asserts curl exit 7/28 |
| H-2 | HIGH | **Valid** | Pipeline env scoping reproduced (`BUN_INSTALL` never reaches bash); installer source: `install_dir=${!BUN_INSTALL:-$HOME/.bun}`, version accepted as `$1` | Fixed: `BUN_INSTALL=/usr/local/bun bash -s "bun-v${BUN_VERSION}"`, new `BUN_VERSION` ARG, in-layer `bun --version` assertion |
| H-3 | HIGH | **Valid** | podman v5.4 `container_commit.go` copies `Spec.Process.Env` into the image config (source read) | Fixed: `snapshot` blanks every env-file key via `podman commit --change 'ENV KEY='`; docs corrected; rotation still advised |
| H-4 | HIGH | **Valid** | Squid docs + FAQ: leading `.` = subdomains, bare = exact, `*.` is a literal; documented subdomain-ordering hazard; `allow` regex accepted `*.` and rejected `.` | Fixed: allowlist uses `.githubusercontent.com`; comments corrected; `allow` accepts `.domain`, rejects `*.`; `squid -k parse` gate before every restart |
| H-5 | HIGH | **Valid** | No `restrict=on` on `-nic user`; guest dev has NOPASSWD sudo; 10.0.2.3:53 allowed; QEMU docs: `restrict=on` isolates the guest but leaves explicit forwarding rules working | Fixed: `restrict=on` + `guestfwd` proxy channel + `hostfwd` ssh; port-53 rules removed; nftables kept as second layer; new `verify` subcommand; docs updated |
| H-6 | HIGH | **Valid** | podman-systemd.unit(5): generated units cannot be `systemctl enable`d; the generator applies `[Install]`; `is-system-running` exits non-zero for degraded/starting | Fixed: `daemon-reload` + `start` (no enable); systemd detection via `show-environment`; `status` reports the active mode |
| M-1 | MED | **Valid** | grep-confirmed absence of cap-drop/NNP/limits on both gateway run paths | Fixed: `DropCapability=ALL` + `AddCapability=SETUID SETGID`, `NoNewPrivileges=true`, pids/memory limits; diagram/spec wording now matches. **Live-host confirmation of Squid's privilege drop still required** (troubleshooting §4 updated) |
| M-2 | MED | **Valid** | `keep-id:uid=1000` maps container `dev` onto the host user; workload-user escape = full host user; SKILL Purpose vs §2 mismatch | Fixed: D1/§8/SKILL Purpose reworded; host-side persistence vectors listed as residual risks |
| M-3 | MED | **Valid** (was Assumed) | budget-wiser package.json fetched: `gate` = lint+typecheck+test+**build+smoke+e2e**; Prisma 6.19.3 with `allowScripts` (postinstall enabled); `binaries.prisma.sh` confirmed as Prisma's engine host (vendor docs) | Fixed: `binaries.prisma.sh` allowlisted; §7 describes `gate` accurately and documents the Prisma engine download; acceptance run remains the live confirmation |
| M-4 | MED | **Valid** | Injection via sourced meta reproduced (`6g; touch /tmp/…` executes); name validation gaps and unguarded `git clone` confirmed by read | Fixed: memory/cpus regex validation; meta parsed with `read` (never sourced); `validate_name` for every subcommand; `git clone --`; env template written under `umask 077` |
| M-5 | MED | **Valid** | Backup helper had no network/caps/keep-id flags; userns reasoning confirmed; default umask | Fixed: helper runs `--network none --cap-drop=ALL --userns=keep-id` + `no-new-privileges`; backups written under `umask 077` into a 0700 `snapshots/` dir |
| M-6 | MED | **Valid** | `jq` used by 45-ci-run but not installed/checked; `openssh-client` not in tier2 set; teardown bypass under `set -e` | Fixed: bootstrap installs jq + openssh-client; preflight `--post` checks jq + netavark backend; runner checks jq upfront; summary failure no longer skips teardown |
| M-7 | MED | **Valid** | `stdio:stderr` is not the stdio-module's path form; probe reproduced counting 403 as success; squid.conf baked into the image | Fixed: `stdio:/dev/stderr` (+ `cache_log`, `pid_filename /dev/null`); probe requires status=200; squid.conf bind-mounted like the allowlist |
| M-8 | MED | **Valid** | `mv` over a backing file in use; poweroff wait unconfirmed; `package_update` ≠ upgrade; sysctl line unquoted and unpersisted | Fixed: golden rebuild refuses while overlays exist and requires confirmed shutdown; `package_upgrade: true`; sysctl quoted + persisted via `/etc/sysctl.d` |
| M-9 | MED | **Valid** | URL/command echoed into console.log and run-summary.json; `cp -r` follows workload-planted symlinks (reproduced; `cp -rP` verified safe) | Fixed: userinfo redaction before logging/storing (runner + ci-setup display); artifact copy uses `cp -rP` + realpath containment |
| M-10 | MED | **Valid** | Mutable base tag, unpinned installer paths, no npm lockfile, over-broad `allowed-tools` | Fixed: base digest-pinned (live-verified 2026-11-06); NodeSource key fingerprint verified in-build; Bun pinned; D8 rewritten to state build-time trust honestly; `allowed-tools` narrowed to script invocations |
| M-11 | MED | **Valid** | No test harness | Fixed: `tests/run-tests.sh` (unit + regression + doc-lint, no podman needed); scripts made sourceable via main-guards |
| L-1 | LOW | **Valid, one sub-item corrected** | Node 16+ vs 24; Bun version wording; size wording; §9 restart claim; hardening garble + wrong network name + broken rootful fallback; phantom `--force` — all confirmed. **Sub-item corrected:** "manifest says five tables" was a misattribution — the manifest row describes the PDF, which legitimately renders five tables (MD/HTML express the fifth, the CI exit-code contract, as prose); the row now says so explicitly | Fixed in all locations (see group 5) |
| L-2 | LOW | **Valid, one premise corrected** | Fixed-range overlap, exact-match sysctl compare, silent unknown flags, dead marker — all confirmed. **Premise corrected:** Debian 13's systemd ships no wider `ping_group_range` default (verified: no sysctl.d entry; kernel default `1 0`), so no host is silently narrowed today — the numeric compare is still the right fix | Fixed: next-free subuid range allocation; numeric sysctl compare (widen only); unknown flags rejected; marker now created |
| L-3 | LOW | **Valid** | `NODE_USE_ENV_PROXY` confirmed (Node v24.0.0+): built-in fetch ignores proxy env without it; `--no-sandbox` behavior under cap-drop undocumented; agent-CLI sandbox caveats | Fixed: `NODE_USE_ENV_PROXY=1` in the image and profile; documented in troubleshooting §6 + §10 caveats |
| L-4 | LOW | **Valid** | Three hand-synced editions; PDF already drifted ("Node.js 16" absent) | Fixed: `tests/run-tests.sh` doc-lint greps MD+HTML for stale markers; HTML generator + templates shipped in `pdf-sources/` with a regeneration README; PDF pipeline documented |

## Changes by file

**Group 1 — restore a passable, honest gate** (C-1, H-1, H-2, M-11)

- `scripts/40-workspace.sh` — reserved-name channel (`ALLOW_RESERVED_NAME=1`,
  set only by 50-verify.sh for the canary); `--memory/--cpus` regex
  validation; meta parsed with `read`, never sourced; `validate_name` on
  every subcommand; `git clone --`; env template under `umask 077`;
  main-guard so the script can be sourced by tests.
- `scripts/50-verify.sh` — canary lifecycle uses the reserved-name channel;
  proxy-denial checks assert `%{http_connect}` = 403 (allow-check requires
  connect 200 **and** code 200); tool checks match a version regex on exit 0;
  direct-egress check targets `http://1.1.1.1/` and requires curl exit 7/28;
  DNS checked separately by name (mechanism 2), proxy ACL (mechanism 3) by
  403; mechanism 4 (bridge forwarding) noted as not directly testable from
  inside a workspace.
- `files/ci-setup.sh` — audit probes read `%{http_connect}` for the
  known-denied domain and `%{http_code}` for the allowed one, no `|| echo`
  fallback; direct-egress probe uses an IP literal and classifies curl exit
  codes (only 7/28 count as blocked); repo URL echoed in redacted form.
- `files/Containerfile` — `ARG BUN_VERSION=1.3.14`; installer invocation
  fixed (`BUN_INSTALL=… bash -s "bun-v${BUN_VERSION}"`); `bun --version`
  asserted in the same layer; `ENV NODE_USE_ENV_PROXY=1`.
- `tests/run-tests.sh` (new) — see below.

**Group 2 — fix policy semantics** (H-4, M-7, H-6, M-1)

- `files/squid/allowlist.txt` — `.githubusercontent.com` (leading dot);
  `binaries.prisma.sh`; header comment states the real matching rules.
- `files/squid/squid.conf` — `access_log stdio:/dev/stderr`, plus
  `cache_log stdio:/dev/stderr` and `pid_filename /dev/null`.
- `scripts/30-gateway.sh` — `allow` accepts `.domain` and rejects `*.` with
  an explanatory error; every config change is validated with
  `squid -k parse` (throwaway container, both files mounted) before any
  restart; `start` = write quadlet + `daemon-reload` + `start` (no
  `systemctl enable`); systemd presence probed with `show-environment`;
  `squid.conf` bind-mounted read-only (quadlet + fallback); gateway runs
  with `DropCapability=ALL` (+`SETUID SETGID`), `NoNewPrivileges=true`,
  pids/memory limits; `status` requires probe status=200 and reports the
  active mode; `down` stops cleanly without `disable` on generated units.

**Group 3 — close secret leaks** (H-3, M-5, M-9, M-4)

- `scripts/40-workspace.sh` `snapshot` — env-file keys blanked from the
  committed image (`--change 'ENV KEY='`), backup helper hardened
  (`--network none`, cap-drop, keep-id, no-new-privileges), backups land in
  `~/agent-workspaces/snapshots/` (0700) under `umask 077`.
- `scripts/45-ci-run.sh` — `redact_url()` (userinfo stripped) applied to the
  console banner, ci-setup display and `run-summary.json`; artifact copy
  uses `cp -rP` and skips paths whose `realpath` escapes the run dir;
  jq presence checked upfront; summary write failures no longer skip
  teardown.
- `files/ci-setup.sh` — same redaction for its cloning banner.

**Group 4 — harden Tier 2 and the gateway** (H-5, M-8)

- `scripts/60-tier2-microvm.sh` — `boot_vm` uses
  `restrict=on,hostfwd=…-:22,guestfwd=tcp:10.0.2.2:3128-tcp:127.0.0.1:3128`
  (host-side enforcement: the only guest-initiated egress is the allowlist
  proxy on the host); cloud-init nftables drops the 10.0.2.3:53 rules
  (DNS is no longer needed or allowed; everything resolves at the proxy);
  `package_upgrade: true`; the ping sysctl is quoted and persisted via
  `/etc/sysctl.d/`; `base` refuses to replace the golden while overlays
  exist and requires a confirmed shutdown first; new `verify <name>`
  subcommand runs the Tier-2 negative checks (direct egress, DNS, proxy
  403/200, nftables ruleset) inside a VM.
- `references/troubleshooting.md` §8, `BLUEPRINT.md` §2/§5 — enforcement
  described as dual (host-side restrict + guest nftables), DNS channel
  closed.

**Group 5 — align the documents** (M-2, M-3, M-6, M-10, L-1…L-4)

- `BLUEPRINT.md` — Node 24 (not 16+); Bun pinned row; consistent size
  wording; §6 secrets plumbing corrected (snapshot strips env-file keys);
  §7 `gate` described accurately + Prisma engine note; D1/§8 reworded
  (container-root escape lands on a subordinate uid; workload-user escape
  lands on the host user — Tier 1 is for code you would run yourself);
  §9 reboot behavior corrected (no restart policy; workspaces stay stopped
  after host reboot); D8 states what is pinned and what is trusted at build
  time; diagram updated (cap-dropped gateway detail, restrict=on, no DNS
  rule); header notes the remediation date.
- `SKILL.md` — Purpose aligned with §2 (untrusted code → Tier 2);
  manifest updated (new files; the PDF row's table count clarified — five
  rendered tables, the fifth is prose in MD/HTML); Phase 5 includes
  `verify`; invariant 1 describes snapshot env-stripping; `allowed-tools`
  narrowed to script invocations (+ read-only podman queries); tests
  referenced.
- `references/hardening.md` — "Adenylist" garble fixed; `agent-gateway` →
  `agent-egress` where a network was meant; rootful-gateway variant
  replaced with an honest statement (workspaces on an internal network
  cannot reach host loopback by design); wildcard guidance corrected
  (leading-dot form); §5 secrets lifecycle corrected (podman commit env
  semantics, verified against podman 5.4 source); §1 base digest now
  pinned by default; §4 golden lifecycle matches the new safeguards.
- `references/troubleshooting.md` — gateway hardening entry (SETUID/SETGID
  rollback note), probe semantics, `verify` for Tier 2, jq/exit-127 note,
  NODE_USE_ENV_PROXY and Chromium `--no-sandbox` notes, removed the broken
  rootful fallback pointer.
- `scripts/10-host-bootstrap.sh` — installs `jq` (core) and
  `openssh-client` (tier2); unknown flags rejected; next-free subuid/subgid
  allocation (no cross-user overlap); numeric `ping_group_range` compare
  (widen only, never narrow); squid marker file actually created.
- `scripts/00-preflight.sh` — `--post` checks `jq` (warning: required for
  CI) and the podman network backend (netavark expected); phantom
  `--force` text removed; unknown flags rejected.
- `files/profile-agent-env.sh` — exports `NODE_USE_ENV_PROXY=1`.
- `pdf-sources/` — ships the HTML generator + templates (paths relative to
  the bundle) and a README documenting both edition pipelines; the PDF
  generator depends on a ReportLab toolchain and is documented instead of
  shipped.

## New tests (M-11, L-4)

`tests/run-tests.sh` runs without podman, systemd, Squid or KVM:

1. validate_name: accepts `wiser`; rejects `Bad`, `__ci-x`; accepts
   `__verify` only with `ALLOW_RESERVED_NAME=1`.
2. Resource validation: accepts `6g`/`512m`/`4`/`1.5`; rejects the
   injection payload and garbage.
3. Meta round-trip: valid values survive the `read`-based parser; a
   hand-crafted hostile meta file yields no code execution.
4. Allow-domain regex: accepts `example.com` and `.example.com`; rejects
   `*.example.com`, URLs, paths, spaces.
5. redact_url: strips `user:pass@` and `user@` from URLs.
6. reason_for: exit-code mapping contract.
7. C-1 regression: mock deny-CONNECT proxy; the fixed expression must
   observe 403 via `%{http_connect}` — and, second pass, the same guarded
   expression must SURVIVE `set -euo pipefail` against an unreachable
   proxy (no abort before the audit json is written).
8. M-9 regression: `cp -rP` must not follow a planted symlink.
9. Doc-lint: MD and HTML contain no stale markers (`Node.js 16`,
   `*.githubusercontent.com`, `stdio:stderr`), and pinned versions agree
   between BLUEPRINT.md and the Containerfile.
10. L-2 second pass: `next_free_range` parses colon-separated
    `/etc/subuid` lines (`login:first:count`) — an existing range must
    yield the NEXT free range, never an overlapping one; garbage lines are
    skipped; missing/empty files fall back to the default allocation.

## Deferred to a live host (unchanged ownership)

- Squid privilege drop under `DropCapability=ALL + SETUID SETGID` — if the
  gateway fails to start, troubleshooting §4 documents the rollback.
- The budget-wiser acceptance run with `binaries.prisma.sh` allowlisted.
- `50-verify.sh` → `0 failed` and `60-tier2-microvm.sh verify` as the
  Tier-1/Tier-2 evidence gates (this environment has no podman/KVM).
- QEMU `restrict=on` + `guestfwd` behavior against QEMU 10 (docs-verified
  here; the `verify` subcommand asserts it on the real host).

## Second-pass validation — 2026-11-07

An independent re-validation of the remediated bundle (same method as the
audit: every file read in full; claims checked against executable truth).
**All 22 original finding-fixes were re-verified as present and correct**
(bash -n clean on 13 scripts; ShellCheck 0.11.0 zero warnings; test suite
green; BLUEPRINT.html regenerated from BLUEPRINT.md byte-identical; PDF
text spot-checks: remediated claims present, stale markers absent).
Four residual defects — three of them introduced by or surviving the first
remediation pass — were found, fixed, and covered by new regression tests:

| # | Severity | Location | Defect (all reproduced before the fix) | Fix + test |
|---|---|---|---|---|
| S-1 | HIGH | `10-host-bootstrap.sh` `next_free_range` | `/etc/subuid` is colon-separated (`login:first:count`, man subuid) but the L-2 fix read whitespace fields — `end` was always empty, so the function ALWAYS returned 100000-165535 and the cross-user overlap L-2 claimed to fix could still occur on shared hosts. Reproduced: `alice:100000:65536` input → `max_end=0` | Parse with `IFS=:`, numeric field guards, `end = first + count - 1`; output contract documented against `usermod --add-subuids FIRST-LAST`. Tests: 6 cases incl. failing-before/passing-after overlap regression |
| S-2 | HIGH | `files/ci-setup.sh` (a_deny/a_allow), `scripts/60-tier2-microvm.sh` (verify probes 1/3/4) | Under `set -euo pipefail`, an UNGUARDED `var="$(curl …)"` ABORTS the script when curl fails (reproduced: `bash -euo pipefail -c 'x=$(false); …'` dies). With the gateway down — exactly the scenario the audit exists to catch — ci-setup died with curl's exit code BEFORE writing isolation-audit.json (mislabeling an audit failure 66 as "command-failed", no evidence), and Tier-2 `verify` died silently instead of printing its diagnostics | `|| :` guards on the probe assignments (value semantics unchanged: empty capture → `000` → check fails honestly). Test: the guarded expression must survive `set -e` against an unreachable proxy and fall back to 000 |
| S-3 | MEDIUM | `scripts/30-gateway.sh` `status` probe | Leftover `… || echo 000` append — the C-1(3) pattern fixed in ci-setup but missed here: a failed probe displayed `status=000000` (fail-closed, but wrong evidence) | Captured directly with the `|| :` guard + `${probe:-000}` normalization, consistent with the ci-setup fix |
| S-4 | LOW | `scripts/50-verify.sh`, `scripts/60-tier2-microvm.sh` verify check 5 | (a) If the `podman exec` channel itself was dead, the DNS negative check could pass vacuously (any error looks "blocked"). (b) `sudo nft list ruleset | grep -q 'dport 53'` passed vacuously when sudo/ssh failed (e.g. after hardening §4 revokes guest sudo) | (a) Dead-channel guard: `ws true` must succeed before any check runs — the suite exits with a diagnostic instead of tallying meaningless passes. (b) The ruleset read must succeed; an empty capture fails the check as "unverifiable" |

Documentation reconciliations in the same pass:

- `SKILL.md` manifest now lists `generate_blueprint_pdf.py` (it was shipped
  but undocumented — an L-4-class gap), with its portability limits stated.
- `pdf-sources/README.md` no longer claims the PDF pipeline is "not
  shipped"; it points at the actual generator and explains the producing
  environment it depends on.
- The doc-lint description above now matches the actual test patterns
  (`stdio:stderr`, not "cap-dropped-without-qualification" — the gateway
  legitimately IS cap-dropped since M-1, so that marker is not stale).
- `BLUEPRINT.md`/`.html`/`.pdf` are UNCHANGED by this pass: the validated
  fixes are in scripts, tests and reference docs, so all three editions
  remain in sync (verified: HTML regeneration byte-identical; PDF text
  spot-checks).
- `README.md` (deliverables) updated: new archive name
  `agent-dev-sandbox-html.tar.gz`, second-pass state entry, refreshed
  verification numbers (tests now 45, was 38).

Second-pass verification run on this bundle: `bash -n` clean (13 scripts),
ShellCheck 0.11.0 zero warnings, `tests/run-tests.sh` **45 passed / 0
failed**, HTML byte-identical regeneration, doc-lint green, PDF spot-checks
green. Still deferred to a live host: the same four items listed above.
