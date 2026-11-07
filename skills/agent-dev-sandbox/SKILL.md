---
name: agent-dev-sandbox
description: Build and operate a secure, egress-restricted development environment for AI coding agents on a Debian 13 host — hardened rootless Podman workspaces behind an allowlist Squid gateway, an optional KVM micro-VM tier for untrusted code, with Python 3.13, Node.js 24, Bun, pnpm, uv, Playwright, Chromium, agent-browser, Claude Code, Codex, and OpenCode preinstalled. Use when asked to set up, build, verify, or troubleshoot an isolated agent sandbox / hardened dev environment on Debian 13.
read_when:
  - Setting up an isolated AI-agent development environment
  - Building hardened container workspaces on a Debian 13 host
  - Restricting sandbox egress to a domain allowlist
  - Creating KVM micro-VMs for untrusted code
  - Troubleshooting an existing agent-dev-sandbox deployment
metadata: {"clawdbot":{"emoji":"🛡️","requires":{"bins":["bash","sudo","podman","jq","shellcheck"]}}}
allowed-tools: Bash(scripts/00-preflight.sh:*), Bash(scripts/10-host-bootstrap.sh:*), Bash(scripts/20-build-image.sh:*), Bash(scripts/30-gateway.sh:*), Bash(scripts/40-workspace.sh:*), Bash(scripts/45-ci-run.sh:*), Bash(scripts/50-verify.sh:*), Bash(scripts/60-tier2-microvm.sh:*), Bash(sudo scripts/10-host-bootstrap.sh:*), Bash(sudo -E scripts/10-host-bootstrap.sh:*), Bash(tests/run-tests.sh:*), Bash(shellcheck:*), Bash(bash -n:*), Bash(podman ps:*), Bash(podman logs:*), Bash(podman inspect:*), Bash(podman image ls:*), Bash(podman network inspect:*), Bash(podman system df:*), Bash(bash scripts/*:*), Bash(./scripts/*:*)
---

# Agent Dev Sandbox — build & operate

## Purpose

Deliver a tiered, self-contained development environment in which AI coding
agents (Claude Code, OpenAI Codex, OpenCode) can clone, build, test, and
browser-verify codebases you would otherwise run yourself — without
exposing the host or the internet:

- **Tier 1 (daily driver)**: one hardened rootless Podman container per
  project. No capabilities, no-new-privileges, resource-capped, on an
  internal network with **no route to the internet and no external DNS** —
  egress exists ONLY through an allowlisted Squid proxy. Honest scope
  (audit M-2): the bind mount shares your uid, so Tier 1 is for code you
  would run yourself — unknown/untrusted repos belong in Tier 2.
- **Tier 2 (hostile workloads)**: a KVM micro-VM per engagement, egress
  enforced on BOTH sides (host-side QEMU `restrict=on` with a proxy-only
  guestfwd, plus nftables inside the VM), running THE SAME container image
  (container-in-VM).

Design rationale, comparison matrix, and every version pin are documented in
`BLUEPRINT.md` (same directory). Read it before deviating from this file.

## When NOT to use this skill

- Host is not Debian 13 (package names/versions assume trixie).
- You need a shared multi-tenant CI fleet with a registry (this is a
  single-user, per-project-workstation design).
- The task is a one-off `docker run` of a known-good image — use plain
  podman/docker directly.

## Prerequisites

- Debian 13 host, sudo access, ≥16 GB RAM recommended (8 GB floor), ≥40 GB
  free disk in `$HOME`.
- Host has internet egress at BUILD time (containers are restricted; the
  build host is not).
- Tier 2 additionally requires `/dev/kvm` (nested virt is NOT required —
  bare KVM on the host).

## File manifest (this bundle)

| Path | Role |
|---|---|
| `BLUEPRINT.md` | Full design document: threat model, architecture decisions, specs, runbooks |
| `BLUEPRINT.pdf` | Print edition of the blueprint (cover, TOC, 14 sections, system-design figure, 5 tables — the MD/HTML editions render the fifth, the CI exit-code contract, as prose) |
| `BLUEPRINT.html` | Interactive single-file edition: search, dark/light theme, Day-0 checklist with saved progress, copy buttons — fully offline |
| `pdf-sources/` | Editable build sources + the HTML generator (regenerate the HTML from the MD; see pdf-sources/README.md) |
| `generate_blueprint_pdf.py` | ReportLab body generator behind `BLUEPRINT.pdf` — kept for provenance; depends on the producing repo's `./skills/pdf` helper package and a cover-render/merge step, so it is not runnable from inside this bundle alone (see pdf-sources/README.md) |
| `references/audit-remediation.md` | 2026-11-06 external audit: validation of all 22 findings + the remediation applied — plus the 2026-11-07 second-pass validation (4 residual defects fixed) and the third-pass review remediation (R-1–R-8) |
| `remediation_log_1.md` … `remediation_log_3.md` | Session logs of the remediation rounds (second pass S-1–S-4; third-pass review R-1–R-8; its remediation) — provenance; `references/audit-remediation.md` remains the canonical record |
| `files/Containerfile` | Tier-1 image: Debian 13 + Python 3.13 + Node 24 + Bun + browsers + agent CLIs (version-pinned ARGs) |
| `files/ci-setup.sh` | In-container CI preamble (bind-mounted per run, NOT baked): CI env, caches, browsers, isolation self-audit |
| `files/profile-agent-env.sh` | `/etc/profile.d` setup inside the image (login shells) |
| `files/seed-playwright-browsers.sh` | Links image-baked browsers into each workspace home (idempotent) |
| `files/ws-shell` | Shell entry wrapper used by `40-workspace.sh shell` |
| `files/squid/Containerfile` | Gateway image (Squid on Debian slim) |
| `files/squid/squid.conf` | Container-gateway Squid config (allowlist, no cache, no leaks) |
| `files/squid/squid-host.conf` | Host Squid variant for Tier 2 (loopback bind) |
| `files/squid/allowlist.txt` | **THE egress policy** — single editable allowlist file |
| `scripts/00-preflight.sh` | Read-only host readiness checks |
| `scripts/10-host-bootstrap.sh` | One-time host setup (sudo, idempotent; `--tier2` adds QEMU+KVM) |
| `scripts/20-build-image.sh` | Build `agent-dev-sandbox:1` |
| `scripts/30-gateway.sh` | Gateway lifecycle: `up/status/logs/restart/allow/down` |
| `scripts/40-workspace.sh` | Workspace lifecycle: `create/shell/exec/start/stop/restart/list/snapshot/destroy` |
| `scripts/45-ci-run.sh` | Ephemeral CI runs: `run/list/reap/cache` (same image, throwaway) |
| `scripts/50-verify.sh` | End-to-end verification suite (positive AND negative checks) |
| `scripts/60-tier2-microvm.sh` | Micro-VM tier: `base/create/ssh/verify/start/stop/list/destroy` |
| `tests/run-tests.sh` | Container-free test suite: pure-function units, audit regressions (C-1/H-4/M-9/L-2/R-6), doc-lint — run after ANY script edit |
| `.shellcheckrc` | Lint config documenting the bundle's accepted shell idioms (run with `tests/run-tests.sh`) |
| `references/troubleshooting.md` | Symptom→cause→fix, keyed §1-§9 |
| `references/hardening.md` | Beyond-baseline options with costs; explicit non-goals |
| `build-agent-dev-sandbox-html-tar.sh` | Reproduces the distributed tar archive from the GitHub repo: clone → patch-if-needed → lint/test gates → `tar` (test-suite integrity guard included) |

## Build procedure (execute in order)

Run every phase from the bundle root. After each phase, confirm the stated
expected outcome before continuing. On failure: `references/troubleshooting.md`
(section numbers appear in error messages), fix the CAUSE, re-run the phase.

### Phase 0 — Preflight
```bash
scripts/00-preflight.sh
```
Expected: `0 blocker(s)`. If blockers: fix host issues (distro, disk, egress).
Tier-2 INFO lines are informational only at this stage.

### Phase 1 — Host bootstrap
```bash
scripts/10-host-bootstrap.sh          # core: podman stack
scripts/10-host-bootstrap.sh --tier2  # optional: QEMU/KVM + host squid
```
Expected: all `✓`. If kvm group was just added: user must re-login before
Phase 5. Then `scripts/00-preflight.sh --post` → `0 blocker(s)`.

### Phase 2 — Image build
```bash
scripts/20-build-image.sh
```
Expected: image `agent-dev-sandbox:1` (first build 5-15 min, ~2 GB download).
Re-run on failure; layer cache resumes.

### Phase 3 — Gateway
```bash
scripts/30-gateway.sh up
```
Expected: gateway container running on `agent-egress` + `agent-internal`,
live probe prints `status=200`. Reboot-persistent (systemd user unit) when
linger is enabled.

### Phase 4 — Verification (GATE — do not skip)
```bash
scripts/50-verify.sh
```
Expected: `0 failed`. The suite creates a canary workspace through the real
toolpath and proves BOTH function (tools, browsers, git clone of the
representative repo `nordeim/budget-wiser`) AND isolation (direct egress
blocked, external DNS blocked, non-allowlisted domain → 403, caps dropped,
non-root, pids limit). SOFT warnings are documented limitations, not
failures. **A suite that never ran, or whose failures were suppressed, means
the environment is NOT done.**

### Phase 5 (optional) — Tier 2 golden micro-VM
```bash
scripts/60-tier2-microvm.sh base      # one-time, 15-30 min
scripts/60-tier2-microvm.sh create probe
scripts/60-tier2-microvm.sh verify probe   # Tier-2 isolation gate
```
Expected: `golden-agent.qcow2` frozen with the agent image loaded inside;
`verify` reports every Tier-2 check OK (direct egress blocked, DNS blocked,
proxy 403/200, no port-53 rule) before any untrusted workload runs there.

## Daily operations

```bash
scripts/40-workspace.sh create wiser --repo https://github.com/nordeim/budget-wiser.git
# → edit ~/.config/agent-sandbox/workspaces/wiser.env (API keys; mode 600)
scripts/40-workspace.sh restart wiser        # keys injected
scripts/40-workspace.sh shell wiser          # login shell as dev in /workspace
scripts/40-workspace.sh stop wiser           # data preserved
scripts/40-workspace.sh snapshot wiser       # image commit + home backup
scripts/40-workspace.sh destroy wiser        # code dir kept unless --purge-workspace
```
Inside a workspace: `claude`, `codex`, `opencode`, `agent-browser`,
`bun run dev`, `pnpm test`, `uv sync` — everything routes through the
allowlist; `localhost` is exempt (`no_proxy`).

Add an egress domain (both tiers, one command):
```bash
scripts/30-gateway.sh allow <domain>
```

Representative workload acceptance (budget-wiser, run inside its workspace):
```bash
bun install && bun run db:push && bun run db:seed && bun run gate
# Playwright e2e runs against localhost:3000 — no external egress needed.
```

## Ephemeral CI runs (optional)

One-shot jobs — PR checks, scheduled tests, agent batch runs — use the same
image and the same allowlist through `scripts/45-ci-run.sh`:

```bash
scripts/45-ci-run.sh run --repo https://github.com/nordeim/budget-wiser.git \
    -- bash -lc 'bun install && bun run db:push && bun run db:seed && bun run gate'
scripts/45-ci-run.sh list          # past runs (from run-summary.json)
scripts/45-ci-run.sh reap          # remove orphaned containers + stale run dirs
scripts/45-ci-run.sh cache         # wipe shared package caches
```

Every run: hardened exactly like a workspace plus a walltime timeout
(`--timeout`, default 3600 s); a per-run isolation self-audit (direct egress,
external DNS, proxy 403/200) writes `artifacts/<id>/isolation-audit.json`
and FAILS the run (exit 66) if the guarantees do not hold — never bypass it
with `--skip-audit`; artifacts (`console.log`, `run-summary.json`, report
dirs) land in `~/agent-workspaces/__ci/artifacts/<id>/`. CI mode changes
consumption, not trust: hostile PR builds still belong in a Tier-2 VM (the
same script runs inside it). Full options and exit codes: script header;
design: `BLUEPRINT.md` §12; failures: `references/troubleshooting.md` §9.

## Security invariants (NEVER violate — audit these on any deviation)

1. **No secrets in images.** Keys only via `--env-file` at `podman run`
   (file 0600, host-side). Never `ENV` a key in a Containerfile, never
   commit env files. `podman commit` copies container env into the image
   config — `snapshot` blanks env-file keys from the committed image, but
   rotate keys after snapshotting a workspace that had live secrets and
   never push a `ws-snap-*` image anywhere.
2. **Never mount `docker.sock`/`podman.sock`** into any workspace, and never
   run a workspace `--privileged`.
3. **Workspaces attach ONLY to `agent-internal`.** No other `--network`.
4. **Never drop** `--cap-drop=ALL`, `--security-opt no-new-privileges`,
   `--userns=keep-id:uid=1000,gid=1000`, or the pids/memory/cpu limits.
5. **No sudo inside workspaces** — missing system package ⇒ rebuild the
   image (Phase 2), don't escalate.
6. **Egress changes go through the allowlist file** (`30-gateway.sh allow`),
   never through network re-attachment.
7. **Tier-2 workspaces never bind-mount host paths**; artifacts leave via
   `scp` only, by explicit action.
8. **Never weaken a failing check** to complete a phase — report it
   (troubleshooting escalation rule). This includes the CI self-audit:
   `--skip-audit` exists for speed on TRUSTED, already-verified pipelines,
   never to make a failing run pass.

> CI runs (`45-ci-run.sh`) are workspaces under these same rules — their
> `agent-__ci-*` containers use the reserved `__` prefix, so they can never
> collide with interactive workspaces.

## Verification gates & Definition of Done

The environment is DONE when ALL of the following hold:
1. `00-preflight.sh --post` → 0 blockers.
2. `agent-dev-sandbox:1` and `agent-gateway:1` images exist; gateway running.
3. `50-verify.sh` → **0 failed** (warnings allowed, each explained).
4. The representative workload onboarding succeeded in the verify evidence
   (budget-wiser clone via proxy) — or an equivalent clone if GitHub is
   deliberately disallowlisted.
5. A report of what was verified, with the check output as evidence, and any
   deviations from this SKILL documented with reasons.

Report format for completion: phase list, per-phase result, verify summary
line (`N passed / 0 failed / M warnings`), deviations, next-step suggestions.

## Maintenance

- **After ANY edit to scripts/**: `tests/run-tests.sh` (container-free) and
  `shellcheck -x scripts/*.sh files/*.sh files/ws-shell` must stay clean; then
  re-run `50-verify.sh` on the host.
- **Refresh a tool**: bump its `ARG` in `files/Containerfile` →
  `20-build-image.sh` → `30-gateway.sh restart` → `50-verify.sh` →
  recreate workspaces (`40-workspace.sh restart <name>` picks up the new
  image; home volumes keep credentials).
- **Allowlist governance**: `files/squid/allowlist.txt` is production
  policy — review diffs, revoke domains when tasks end. Leading dot =
  subdomains; bare domain = exact match; `*.` is invalid and rejected.
- **Disk**: `podman system df`; prune stale layers and old snapshots
  (including `~/agent-workspaces/snapshots/` and old
  `golden-agent.qcow2.old-*` files).
- **Backups**: `40-workspace.sh snapshot` before risky operations
  (snapshots land 0600 in the 0700 snapshots dir — they contain auth
  tokens; encrypt at rest); workspace code belongs in git remotes, not
  just volumes.

## Troubleshooting

`references/troubleshooting.md` (§1-§9, symptom → cause → fix). Escalation
rule: after two unsuccessful fix attempts with no new evidence, stop and
report state instead of guessing; never silence a check to proceed.
