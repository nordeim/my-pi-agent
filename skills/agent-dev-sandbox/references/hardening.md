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
Adenylist profile (Docker's default + `clone3`, `perf_event_open` etc.
already blocked) adds little; a custom ALLOWLIST profile adds a lot of
maintenance. Only pursue with a compliance requirement.

**Systemd user slice limits.** Per-container `--memory/--cpus` caps one
container. Cap the whole rootless realm (gateway + all workspaces + image
store) with a user drop-in:
`systemctl --user edit` on the slice, e.g. `MemoryMax=12G`, `TasksMax=8192`
in `~/.config/systemd/user/user@1000.service.d/limits.conf`. Cost: the
whole fleet shares the cap; one runaway multi-workspace job can starve others.

**Image provenance.** Pin the base image by digest
(`docker.io/library/debian@sha256:…` instead of `:trixie-slim`) and verify
with `skopeo inspect docker://…`. Cost: you must bump digests deliberately
(no automatic base updates). Recommended once the environment stabilizes.

**Egress netns audit.** Periodically assert that no workspace container is
attached to a non-internal network:
```bash
for c in $(podman ps -q); do
  podman inspect -f '{{.Name}}: {{.NetworkSettings.Networks}}' "$c"
done
# anything showing a network other than agent-internal / agent-gateway is a finding
```

## 2. Gateway

**Rootful gateway variant.** If rootless defined-network NAT misbehaves on
your host (rare), run the SAME gateway image as a SYSTEM quadlet
(`/etc/containers/systemd/agent-gateway.container`) attached to rootful
`agent-egress`/`agent-internal` networks. Rootless workspaces can reach it
via published port + `host.containers.internal`. Cost: the proxy runs as
root-owned service (still a container, still cap-dropped); benefit: NAT
behavior is the well-trodden rootful path.

**Allowlist governance.** Treat `files/squid/allowlist.txt` like production
config: review diffs, avoid `*.` wildcards beyond the shipped ones, and
revoke domains when a task ends. Every line is a standing grant to untrusted
code.

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
- home volumes via `40-workspace.sh snapshot`

## 4. Micro-VM tier (Tier 2)

**Revoke cloud-init sudo after provisioning.** The golden image grants dev
passwordless sudo for setup. After `base` completes, optionally:
`scripts/60-tier2-microvm.sh ssh` → edit `/etc/sudoers.d/90-cloud-init-users`
to remove NOPASSWD. Cost: you lose ad-hoc root inside the VM (re-add
temporarily when needed).

**Fresh golden per engagement.** Overlays share the golden backing file —
a compromise of the golden disk image poisons every overlay. Rebuild golden
(`60-tier2-microvm.sh base`) when moving between trust boundaries.

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
  and are injected at container start. Never in images, never in
  `podman commit` snapshots (snapshot commits the CONTAINER fs, which
  contains env only in PID 1's /proc, not on disk — but still: rotate keys
  after any snapshot of a workspace that had secrets if unsure).
- Rotate API keys when a workspace is destroyed (`--purge-home`).
- Different keys per provider per workspace where the provider allows it;
  budget-capped keys for untrusted-workload VMs.

## 6. What the baseline deliberately does NOT defend against

Honest scope statement:
1. Supply-chain compromise of an ALLOWLISTED domain (registry.npmjs.org
   serving a malicious package you install) — mitigated by nothing here
   beyond least-egress; add lockfile review / `npm audit` in your workflow.
2. Kernel exploits from inside a Tier-1 container (shared kernel). Tier 2
   exists precisely for this residual risk.
3. A malicious HOST admin — out of scope entirely.
4. Data you explicitly exfiltrate yourself through allowed channels
   (git push to an allowed host).
5. Side channels / timing attacks across containers on the same host.
