# Hardening — beyond the baseline

The baseline (SKILL.md phases) is a coherent, verified security floor. Every
item below STRENGTHENS a specific dimension, with its cost stated. Apply the
ones that match your threat model; do not cargo-cult all of them.

## 1. Container tier (Tier 1)

**Read-only rootfs.** Run workspaces with `--read-only --tmpfs /tmp:rw,size=2g`
plus the existing volumes. Cost: anything that writes outside `/workspace`,
`/home/dev`, `/tmp` breaks (some one-off installers). Benefit: fileless
malware drops and filesystem persistence inside the container become
impossible. Try it per-workspace before making it default.

**Custom seccomp profile.** The default podman profile is already strict.
A deny-list profile (Docker's default + `clone3`, `perf_event_open` etc.
already blocked) adds little; a custom ALLOWLIST profile adds a lot of
maintenance. Only pursue with a compliance requirement.

**Systemd user slice limits.** Per-container `--memory/--cpus` caps one
container. Cap the whole rootless realm (gateway + all workspaces + image
store) with a user drop-in:
`systemctl --user edit` on the slice, e.g. `MemoryMax=12G`, `TasksMax=8192`
in `~/.config/systemd/user/user@1000.service.d/limits.conf`. Cost: the
whole fleet shares the cap; one runaway multi-workspace job can starve others.

**Image provenance.** The base image is digest-pinned by default in the
Containerfile (`BASE_DIGEST` ARG; verified live 2026-11-06). Refresh
deliberately when you want new security updates: fetch the current digest
(see the Containerfile header comment), bump the ARG, rebuild, re-verify.
Verify what you pulled with `skopeo inspect docker://…`. Remaining
build-time trust (stated honestly, audit M-10): the uv/bun installer
scripts and transitive npm dependencies arrive over TLS without checksum
verification; browser revisions are resolved at build time.

**Egress netns audit.** Periodically assert that no workspace container is
attached to a non-internal network:
```bash
for c in $(podman ps -q); do
  podman inspect -f '{{.Name}}: {{.NetworkSettings.Networks}}' "$c"
done
# anything showing a network other than agent-internal / agent-egress is a finding
```

**CI variant.** `45-ci-run.sh --read-only-rootfs` composes the read-only
rootfs automatically (tmpfs `/tmp`, `/var/tmp`, `/run` plus a writable
bind-mounted home), and `--no-cache-vol` removes the shared cache tree for
runs whose source you do not trust — package caches are shared writable
state across runs (pnpm's documentation says the same about its store), so
isolate them per trust domain. For genuinely hostile PR builds, the answer
is not more container flags — it is Tier 2 (run the same `45-ci-run.sh`
inside a micro-VM).

## 2. Gateway

**If rootless defined-network NAT misbehaves.** The old versions of this
document suggested a rootful system-quadlet gateway reachable via a
published port — that variant CANNOT work in this topology: workspaces on
the `--internal` network have no route to the host loopback (that is the
enforcement, not a bug), and moving workspaces to a routed network would
violate invariant 3. Debug the actual layer instead: `podman network
inspect agent-egress`, check `podman info --format '{{.Host.NetworkBackend}}'`
(expect netavark), and consult troubleshooting §4. There is deliberately
no supported rootful fallback for Tier 1; Tier 2's host squid is a different
path (VMs reach it through QEMU's guestfwd, not through a container
network).

**Allowlist governance.** Treat `files/squid/allowlist.txt` like production
config: review diffs and revoke domains when a task ends. Matching is
Squid `dstdomain`: a LEADING DOT (`.example.com`) matches all subdomains,
a bare domain is an exact match, and `*.` is not a wildcard —
`30-gateway.sh allow` rejects it. Do not list a subdomain before its
leading-dot entry (Squid treats that as a fatal parse error; every change
is `squid -k parse`-validated before the gateway restarts). Every line is
a standing grant to untrusted code.

**Squid TLS interception (DO NOT by default).** `ssl_bump` would let you
audit payloads, but requires a CA trusted by every tool in every workspace —
and silently breaks pinned-TLS CLIs (Claude Code, Codex). Domain-level
allowlisting + access logs are the right level for this threat model.

## 3. Host

**Unattended security upgrades:** `sudo apt install unattended-upgrades &&
sudo dpkg-reconfigure -plow unattended-upgrades`. Kernel updates need reboots
— schedule them.

**auditd** on the host for exec logging:
`sudo apt install auditd && sudo auditctl -a always,exit -F arch=b64 -S execve -k agent-host-exec`.
Cost: log volume; keep rules targeted.

**SSH:** the host is a server — keys only (`PasswordAuthentication no`),
no root login, fail2ban if exposed. The VM tier also exposes only
loopback-forwarded SSH ports (127.0.0.1), so nothing is reachable off-box
unless you forward it.

**Backups of the state that matters:**
- `~/agent-workspaces/` (code — but use git remotes as primary)
- `~/.config/agent-sandbox/` (env templates — SECRETS: encrypt at rest,
  e.g. age/gpg, or never back this dir up and rely on your vault)
- `~/agent-workspaces/snapshots/` via `40-workspace.sh snapshot` — created
  0600 inside a 0700 directory (agent CLI auth tokens live in those
  tarballs; the same encryption advice applies)
- home volumes via `40-workspace.sh snapshot`

## 4. Micro-VM tier (Tier 2)

**Revoke cloud-init sudo after provisioning.** The golden image grants dev
passwordless sudo for setup. After `base` completes, optionally:
`scripts/60-tier2-microvm.sh ssh` → edit `/etc/sudoers.d/90-cloud-init-users`
to remove NOPASSWD. Cost: you lose ad-hoc root inside the VM (re-add
temporarily when needed).

**Fresh golden per engagement.** Overlays share the golden backing file —
a compromise of the golden disk image poisons every overlay. Rebuild golden
(`60-tier2-microvm.sh base`) when moving between trust boundaries: the
command now refuses to run while overlay VMs still reference the golden
(and keeps the previous golden beside the new one until you delete it),
runs `package_upgrade` during provisioning, and confirms shutdown before
freezing. Verify each new VM with `60-tier2-microvm.sh verify <name>`.

**vCPU/RAM per VM** are set in the script (`VM_MEM_MB`, `VM_CPUS`); on a
16-32 GB host, one 6 GB VM + container workspaces is the comfortable budget.
Two VMs max on 32 GB.

**Firecracker / Cloud Hypervisor.** For fleet-scale microVMs (dozens,
sub-second boot), QEMU+KVM gives way to Firecracker or Cloud Hypervisor
(static binaries, minimal device model). Not packaged in Debian — upstream
installs only. The cloud-init seed + overlay pattern here ports directly;
only the `boot_vm()` function changes.

## 5. Secrets lifecycle

- Keys live ONLY in `~/.config/agent-sandbox/workspaces/<name>.env` (0600)
  and are injected at container start. Never in images. CAVEAT (audit H-3,
  verified against podman 5.4 source): `podman commit` copies the
  container's full environment — including `--env-file` values — into the
  committed image config, where `podman image inspect` (and any
  save/push) can read it. The remediated `snapshot` blanks every env-file
  key from the committed image (`--change 'ENV KEY='`), but the honest rule
  stands: rotate keys after any snapshot of a workspace that had live
  secrets, and NEVER push a `ws-snap-*` image anywhere.
- Rotate API keys when a workspace is destroyed (`--purge-home`).
- Different keys per provider per workspace where the provider allows it;
  budget-capped keys for untrusted-workload VMs.

## 6. What the baseline deliberately does NOT defend against

Honest scope statement:
1. Supply-chain compromise of an ALLOWLISTED domain (registry.npmjs.org
   serving a malicious package you install) — mitigated by nothing here
   beyond least-egress; add lockfile review / `npm audit` in your workflow.
2. Supply-chain compromise of BUILD-TIME endpoints (the uv/bun installer
   scripts, npm transitives, NodeSource beyond its pinned key fingerprint,
   the digest-pinned base aside) — TLS-trusted, not checksum-verified; see
   D8 for the full honest statement.
3. Kernel exploits from inside a Tier-1 container (shared kernel). Tier 2
   exists precisely for this residual risk.
4. A malicious HOST admin — out of scope entirely.
5. Data you explicitly exfiltrate yourself through allowed channels
   (git push to an allowed host).
6. Side channels / timing attacks across containers on the same host.
