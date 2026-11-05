# Troubleshooting — agent-dev-sandbox

Symptom-driven. Section numbers are referenced from error messages in the
scripts and from `50-verify.sh` output. Work top-to-bottom within a section;
each item states the symptom, the cause, and the fix.

> Escalation rule for AI agents: after two fix attempts that do not produce
> NEW evidence, stop and report the state (commands run, outputs, hypothesis)
> instead of continuing to guess. NEVER make a failing check pass by removing
> the check, weakening limits, or granting privileges — report the failure.

---

## §1 — Preflight blockers (00-preflight.sh)

**"This blueprint targets Debian 13"**
The scripts rely on trixie package names and versions (podman 5.4, passt,
python3.13). On Debian 12 the container path mostly works but
`python3.13*` packages are absent — build the image from a trixie base and
accept an unsupported host at your own risk.

**"host cannot reach https://…"**
The HOST needs open egress at build time (image layers, NodeSource, browser
CDNs). Only containers are restricted. Check the host firewall / DNS, or
proxy the host itself and re-run preflight.

**"Kernel too old for rootless overlay"**
Need ≥ 5.12 for unprivileged overlayfs (Debian 13 ships 6.12, so this only
fires on strange kernels). Without it podman falls back to fuse-overlayfs —
slower but functional; upgrade the kernel instead.

---

## §2 — Bootstrap / rootless podman (10-host-bootstrap.sh, preflight --post)

**`podman info` fails: "cannot find namespaces" / "invalid argument"**
Missing subuid/subgid ranges. Fix:
`sudo usermod --add-subuid 100000-165535 --add-subgid 100000-165535 $USER`
then log out and back in.

**"Error creating new storage: permission denied" under ~/.local/share/containers**
Usually an old rootless store owned by another uid, or a home dir on NFS
(rootless podman does not support NFS homes — rootless.md, containers/podman).
Move storage: `containers-storage.conf` → `graphroot` on a local filesystem.

**Gateway dies when you log out**
Linger not enabled: `sudo loginctl enable-linger $USER`. The quadlet then
survives reboots and logouts.

**kvm group added but /dev/kvm still not writable**
Group membership applies to NEW sessions — log out fully (not just `su`).

---

## §3 — Image build (20-build-image.sh)

**NodeSource key/repo errors**
`deb.nodesource.com` unreachable or the gpg key step failed mid-layer.
Re-run with `--no-cache`. If your host is behind a corporate proxy, set
`http_proxy/https_proxy` in the shell before building (host-side, build-time
only — containers stay restricted).

**Build dies at `playwright install --with-deps` (apt)**
Transient apt mirror failure — re-run; layer caching resumes from the last
good step. Persistent failure: check `apt` egress to `deb.debian.org`.

**Disk full during build (~10-15 GB needed)**
`podman system df` then `podman system prune` for stale layers. The browsers
layer alone is ~750 MB compressed, ~2 GB unpacked.

---

## §4 — Gateway / egress (30-gateway.sh)

**`status` probe fails (no HTTP 200)**
1. `podman ps -a | grep agent-gateway` — Exited? `podman logs agent-gateway`.
2. Squid config syntax: `podman run --rm -v $PWD/files/squid/squid.conf:/etc/squid/squid.conf:ro agent-gateway:1 squid -N -k parse` … or simpler: `podman logs` shows parse errors immediately.
3. Both networks must exist: `podman network ls | grep agent-`.

**403 for a domain you expected to work**
It is not in `files/squid/allowlist.txt` (or the gateway was not restarted).
Add it: `scripts/30-gateway.sh allow <domain>` — that edits the file AND
restarts both proxy tiers.

**Containers cannot resolve `agent-gateway`**
On `--internal` networks, aardvark-dns resolves CONTAINER NAMES only. The
gateway container must be named exactly `agent-gateway` and be attached to
`agent-internal`. If you renamed it, update `GW=` in `40-workspace.sh`.

**DNS works but nothing else leaves the workspace — correct!**
That is the design: no default route, NXDOMAIN externally, proxy-only egress
(`podman-network-create(1)`, `--internal`). If you NEED full egress for a
trusted workspace, run it on a normal network explicitly — and accept that
you have disabled the egress guarantee for that workspace (document it).

**Rootless defined-network egress misbehaving on exotic hosts**
The gateway needs `agent-egress` (a NORMAL rootless bridge network) to reach
the internet. If that network has no NAT on your host (rare; custom
netavark/pasta configs), inspect: `podman network inspect agent-egress`.
Fallback: run the gateway rootful via a system quadlet (see
references/hardening.md §2) — same image, same allowlist.

---

## §5 — Workspaces (40-workspace.sh)

**Files in /workspace owned by wrong user / "Permission denied"**
You ran the container without `--userns=keep-id:uid=1000,gid=1000`. Never
drop that flag: it maps your host uid onto container `dev` (uid 1000) so the
bind mount is writable by the workspace user.

**"pids/memory limits NOT enforced" warning from verify**
Rootless podman needs cgroup v2 delegation. Bootstrap enables linger, which
on Debian delegates `pids`, `cpu`, `memory` to your user session. If your
system overrides that: `systemctl show user@$(id -u) -p DelegateControllers`.
Expect at least `pids memory cpu`.

**git clone fails inside workspace with proxy error**
Host not allowlisted (github.com IS by default). `30-gateway.sh allow <host>`.

**npm/pnpm/bun/git not using the proxy**
They all honor `http_proxy/https_proxy/HTTP_PROXY/HTTPS_PROXY` — set as
container env by `run_workspace`. If a tool still fails: `env | grep -i proxy`
inside the workspace to confirm injection; `no_proxy` must include
`localhost,127.0.0.1` or local dev-server tests will break.

**Claude Code / Codex / OpenCode logged out after recreate**
Auth lives in the home VOLUME (`agent-home-<name>`), which persists across
restart/restart/destroy-without-purge. `destroy --purge-home` deletes
credentials on purpose. Re-login: `claude login` / `codex login` / opencode
auth inside the workspace.

**Different Playwright version in a project re-downloads a browser**
Expected: each Playwright pin maps to a browser revision. Baked revisions are
symlinked into the home volume by `seed-playwright-browsers`; anything else
downloads through the proxy into the home volume (one-time per project).

---

## §6 — In-container tool issues

**agent-browser external pages fail; local pages fine**
Chromium does not reliably honor proxy env vars in every configuration. For
projects that must browse external pages, configure Playwright explicitly:
`agent-browser open` is fine for local; for Playwright projects use
`launch({ proxy: { server: 'http://agent-gateway:3128' } })`. Local-first
flows (dev server + e2e) are unaffected — they use `no_proxy` localhost.

**`python3.13 -m venv` fails: ensurepip not available**
Impossible in the image (python3.13-venv is installed). If you see it inside
a Tier-2 VM: the golden image missed the package — re-run `base`. On the
HOST: `sudo apt install python3.13-venv`.

---

## §7 — verify.sh failures

Every FAIL line prints its evidence. Mapping:
- proxy 403-but-expected-200 → §4 (allowlist/gateway)
- expected-403-but-got-200 → allowlist too broad (did you add the domain?)
- direct-egress SUCCEEDED → CRITICAL: container is not on `agent-internal`,
  or someone re-created it with another network. Rebuild via 40-workspace.sh.
- CapEff nonzero → container created without `--cap-drop=ALL`.
- browser smoke failed → run `50-verify.sh --keep`, then
  `40-workspace.sh shell __verify` and launch manually to see the error.

---

## §8 — Tier 2 micro-VMs (60-tier2-microvm.sh)

**`base` hangs at "waiting for SSH"**
Read `~/.local/share/agent-sandbox/microvm/logs/golden.console.log`. Common
causes: no KVM (boot is glacial under tcg — require_kvm should have caught
it), or cloud-init waiting on network. The seed ISO is NoCloud; make sure
`cloud-localds` produced it without errors.

**cloud-init "status: error"**
`vm_ssh` in and run `sudo cloud-init status --long` and
`sudo cat /var/log/cloud-init-output.log`. Most common: apt could not reach
mirrors — the VM apt config points at `http://10.0.2.2:3128`, so the HOST
squid must be installed (`bootstrap --tier2`) and running.

**Image transfer fails / disk full**
The image tarball is 1-3 GB compressed. It passes through `/tmp` in the VM
and `${VM_DIR}` on the host; both need space. `df -h` both sides.

**VM has no internet but proxy domains work — correct!**
`/etc/nftables.conf` inside the VM permits only 10.0.2.2:3128 (proxy) and
10.0.2.3:53 (DNS). That is the enforcement, not a bug.

**Cannot reach a NEW domain from inside a VM**
Same allowlist as Tier 1: `30-gateway.sh allow <domain>` syncs the host squid
(Tier 2) and the container gateway (Tier 1) in one step.

---

## §9 — Ephemeral CI runs (45-ci-run.sh)

**Run exits 66 — "[ci-audit] FAILED"**
The per-run isolation self-audit proved a guarantee does NOT hold; the command
was never executed. Read `~/agent-workspaces/__ci/artifacts/<id>/isolation-audit.json`:
- `direct_egress: open` → the container is not on `agent-internal` (recreate
  via 45-ci-run.sh; never re-run with another network).
- `external_dns: resolves` → same root cause as above, §4.
- `proxy_allow_status != 200` → gateway down or `example.com` pruned from the
  allowlist (it is a verification target — restore it, do not pick another).
- `proxy_deny_status != 403` → `example.net` somehow became allowlisted; that
  domain is the audit's known-denied probe — remove it again.
- uid/caps/nnp wrong → the image or flags drifted from the Containerfile /
  runner defaults; do not proceed until restored.
NEVER use `--skip-audit` to force a run green — that is the escalation-rule
violation this bundle forbids (report the failure instead).

**Run exits 124**
Walltime timeout: `timeout` TERM'd the container after `--timeout` seconds
(default 3600). Raise the value only if the job legitimately needs longer;
otherwise debug the hang with `--keep-on-failure` (container + code dir kept).

**Artifacts directory has no report files**
The command wrote reports somewhere the copier does not look. Defaults copied
from the code dir: `playwright-report test-results coverage dist build
junit.xml`. Add your own: `--artifact-path <relative-path-or-glob>` (globs
allowed; avoid spaces in paths). Output written to `/artifacts` (=
`$CI_ARTIFACTS_DIR`) lands there directly.

**"shared cache not mounted/writable" notice inside a run**
The run was started with `--no-cache-vol` (isolated caches — slower but no
state shared across runs), or the cache bind mount failed. Intentional for
untrusted sources: pnpm's own documentation describes package stores as
shared writable state for a single trust domain.

**`reap` deleted a container I was debugging**
`reap` only removes `agent-__ci-*` containers that are NOT running and run
dirs older than the TTL (default 24 h — tune `--ttl-hours`). Interactive
workspaces are structurally unreachable (their names cannot start with
`__`). Start the container you are debugging, or re-run with a longer TTL.

**`list` shows a run with `isolation_audit: not-run`**
The container died before ci-setup reached the audit (e.g. exit 125/126/127:
podman-level failure — image missing, name clash, OCI runtime error). Fix the
podman-level cause first; the command itself never started.
