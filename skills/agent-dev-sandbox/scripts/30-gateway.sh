#!/usr/bin/env bash
# ============================================================================
# 30-gateway.sh — manage the egress allowlist gateway (Tier 1)
# ============================================================================
# The gateway is a rootless Squid container with TWO interfaces:
#   * agent-egress   (normal network, NAT to the internet)
#   * agent-internal (internal network: no default route, no external DNS)
# Workspace containers attach ONLY to agent-internal — they can talk to the
# gateway and to each other, nothing else. Egress enforcement is structural:
# there is no route out except through the allowlisted proxy.
#
# Usage:
#   scripts/30-gateway.sh up            # build + start (idempotent)
#   scripts/30-gateway.sh status        # state + live allowlist probe
#   scripts/30-gateway.sh logs
#   scripts/30-gateway.sh restart       # after editing the allowlist
#   scripts/30-gateway.sh allow <dom>   # add a domain + restart (both tiers)
#   scripts/30-gateway.sh down
# ============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(dirname "${SCRIPT_DIR}")"
ALLOWLIST="${SKILL_ROOT}/files/squid/allowlist.txt"

GW_IMAGE="agent-gateway:1"
GW_NAME="agent-gateway"
NET_EGRESS="agent-egress"
NET_INTERNAL="agent-internal"
QUADLET_DIR="${HOME}/.config/containers/systemd"
QUADLET_FILE="${QUADLET_DIR}/${GW_NAME}.container"

GREEN='\033[0;32m'; RED='\033[0;31m'; YELLOW='\033[1;33m'; NC='\033[0m'
ok() { echo -e "  ${GREEN}✓${NC} $1"; }
info() { echo "  → $1"; }
die() { echo -e "  ${RED}✗ $1${NC}" >&2; exit 1; }

ensure_networks() {
    if ! podman network exists "${NET_EGRESS}" 2>/dev/null; then
        podman network create "${NET_EGRESS}" >/dev/null
        ok "created network ${NET_EGRESS} (has internet egress)"
    fi
    if ! podman network exists "${NET_INTERNAL}" 2>/dev/null; then
        # --internal: no default route in attached containers, IP forwarding
        # disabled on the bridge, aardvark-dns answers container names only
        # (external names -> NXDOMAIN). Verified against podman-network-create(1).
        podman network create --internal "${NET_INTERNAL}" >/dev/null
        ok "created network ${NET_INTERNAL} (internal: no route, no external DNS)"
    fi
}

ensure_image() {
    if ! podman image exists "${GW_IMAGE}" 2>/dev/null; then
        info "building ${GW_IMAGE} (one-time, ~1 min)…"
        podman build -t "${GW_IMAGE}" "${SKILL_ROOT}/files/squid" >/dev/null \
            || die "gateway image build failed — see references/troubleshooting.md §4"
        ok "built ${GW_IMAGE}"
    fi
}

# Parse-check the LIVE config (squid.conf + allowlist) in a throwaway
# container before it reaches the real gateway (audit H-4: a bad allowlist
# edit used to restart straight into a crash-looping Squid).
validate_squid_conf() {
    local out rc=0
    out="$(podman run --rm --network none \
            -v "${SKILL_ROOT}/files/squid/squid.conf:/etc/squid/squid.conf:ro,Z" \
            -v "${ALLOWLIST}:/etc/squid/allowlist.txt:ro,Z" \
            "${GW_IMAGE}" squid -N -k parse 2>&1)" || rc=$?
    if [ "${rc}" -ne 0 ]; then
        die "squid -k parse REJECTED the configuration — gateway NOT restarted:
${out}"
    fi
}

write_quadlet() {
    mkdir -p "${QUADLET_DIR}"
    cat > "${QUADLET_FILE}" <<EOF
# Managed by scripts/30-gateway.sh — edit the allowlist, not this unit.
[Unit]
Description=Agent sandbox egress allowlist gateway

[Container]
Image=${GW_IMAGE}
ContainerName=${GW_NAME}
Network=${NET_EGRESS}
Network=${NET_INTERNAL}
Volume=${ALLOWLIST}:/etc/squid/allowlist.txt:ro,Z
Volume=${SKILL_ROOT}/files/squid/squid.conf:/etc/squid/squid.conf:ro,Z
# Hardened like the workspaces (audit M-1): the only component on BOTH
# networks and parsing untrusted requests runs with no capabilities beyond
# what Squid needs to drop privileges to its cache user. If Squid on your
# kernel cannot start with these caps, see references/troubleshooting.md §4.
DropCapability=ALL
AddCapability=SETUID SETGID
NoNewPrivileges=true
PodmanArgs=--pids-limit=256 --memory=512m

[Service]
Restart=always

[Install]
WantedBy=default.target
EOF
}

start_gateway() {
    ensure_networks
    ensure_image
    validate_squid_conf
    # Prefer the systemd user unit whenever a user session manager is
    # REACHABLE. Probing with show-environment (not is-system-running):
    # the latter exits non-zero for "degraded"/"starting", which pushed
    # healthy hosts into the non-persistent fallback (audit H-6).
    if systemctl --user show-environment >/dev/null 2>&1; then
        podman rm -f "${GW_NAME}" >/dev/null 2>&1 || true   # transition from a previous plain-podman run
        write_quadlet
        systemctl --user daemon-reload
        # NOTE: quadlet-generated units CANNOT be `systemctl enable`d
        # (podman-systemd.unit(5)); the generator applies [Install]
        # itself on daemon-reload — so: start only (audit H-6).
        systemctl --user start "${GW_NAME}.service"
        ok "gateway started via systemd user unit (boot-persistent: [Install] WantedBy=default.target + linger)"
    else
        # Fallback: no working user systemd — plain rootless podman.
        # --restart=always covers crashes; boot persistence requires the
        # quadlet path (or manual start) — status prints which mode is active.
        podman rm -f "${GW_NAME}" >/dev/null 2>&1 || true
        podman run -d --name "${GW_NAME}" \
            --network "${NET_EGRESS}" --network "${NET_INTERNAL}" \
            --restart=always \
            --cap-drop=ALL --cap-add=SETUID --cap-add=SETGID \
            --security-opt no-new-privileges \
            --pids-limit=256 --memory=512m \
            -v "${ALLOWLIST}:/etc/squid/allowlist.txt:ro,Z" \
            -v "${SKILL_ROOT}/files/squid/squid.conf:/etc/squid/squid.conf:ro,Z" \
            "${GW_IMAGE}" >/dev/null
        ok "gateway started via plain podman (no systemd user session: NOT boot-persistent)"
    fi
    sleep 1
    status
}

cmd_up() { start_gateway; }

cmd_down() {
    # Generated units cannot be disabled either (audit H-6): stop the
    # service, drop the quadlet, remove the container.
    if [ -f "${QUADLET_FILE}" ]; then
        systemctl --user stop "${GW_NAME}.service" 2>/dev/null || true
        rm -f "${QUADLET_FILE}"
        systemctl --user daemon-reload 2>/dev/null || true
    fi
    podman rm -f "${GW_NAME}" >/dev/null 2>&1 || true
    ok "gateway stopped (networks left in place for running workspaces)"
}

cmd_restart() {
    validate_squid_conf
    if [ -f "${QUADLET_FILE}" ]; then
        systemctl --user restart "${GW_NAME}.service"
    else
        podman restart "${GW_NAME}" >/dev/null
    fi
    ok "gateway restarted — new allowlist active"
    # Sync the Tier-2 host proxy if it is installed (best effort).
    if [ -f /etc/squid/allowlist.txt ] && command -v squid >/dev/null 2>&1; then
        if sudo -n cp "${ALLOWLIST}" /etc/squid/allowlist.txt 2>/dev/null \
           && sudo -n systemctl restart squid 2>/dev/null; then
            ok "Tier-2 host squid allowlist synced + restarted"
        else
            echo -e "  ${YELLOW}○${NC} Tier-2 host squid present but not synced (needs sudo). Run:"
            echo "        sudo cp ${ALLOWLIST} /etc/squid/allowlist.txt && sudo systemctl restart squid"
        fi
    fi
}

cmd_status() {
    echo "  gateway container:"
    podman ps -a --filter "name=^${GW_NAME}$" --format "    {{.Names}}  {{.Status}}  {{.Networks}}" || true
    if [ -f "${QUADLET_FILE}" ]; then
        echo "  mode: systemd user unit (boot-persistent) — ${QUADLET_FILE}"
    else
        echo "  mode: plain podman (NOT boot-persistent; run '$0 up' to adopt systemd)"
    fi
    echo "  networks:"
    podman network ls --format "    {{.Name}}  {{.Driver}}" | grep -E "agent-(egress|internal)" || echo "    (missing — run: $0 up)"
    echo "  live allowlist probe (expect status=200 through the proxy):"
    # Capture curl's output DIRECTLY, with a `|| :` guard. The old
    # `... || echo 000` had two defects (audit C-1's third defect, cleaned up
    # in the second pass): (a) when the command exited non-zero AFTER -w had
    # already printed "000", the fallback APPENDED a second code ("000000");
    # (b) conversely, without any fallback an unguarded assignment would
    # abort this script under `set -e` with no diagnostic. The guard keeps
    # control flow alive; an empty capture is normalized to 000 below.
    local probe=""
    probe="$(podman run --rm --network "${NET_INTERNAL}" \
            agent-dev-sandbox:1 \
            curl -sS --max-time 15 --proxy "http://${GW_NAME}:3128" \
                 -o /dev/null -w '%{http_code}' \
                 https://registry.npmjs.org 2>/dev/null)" || :
    probe="${probe:-000}"
    # Audit M-7: curl exits 0 on ANY HTTP status — 403/500 used to print
    # "proxy path works end-to-end". Only 200 passes now.
    if [ "${probe}" = "200" ]; then
        ok "proxy path works end-to-end (status=200)"
        return 0
    else
        echo -e "  ${RED}✗ probe failed (status=${probe}) — see $0 logs and references/troubleshooting.md §4${NC}"
        return 1
    fi
}

cmd_logs() {
    if [ -f "${QUADLET_FILE}" ]; then
        journalctl --user -u "${GW_NAME}.service" -f
    else
        podman logs -f "${GW_NAME}"
    fi
}

validate_domain() { # <domain> — dies unless it is a bare domain or a
    # leading-dot subdomain entry. Audit H-4: Squid dstdomain has exactly ONE
    # wildcard form — a LEADING DOT. "*.x.com" is a literal that matches
    # nothing, so it is rejected with an explanation instead of silently
    # added as a dead line.
    local domain="${1:?usage: validate_domain <domain>}"
    if [[ "${domain}" =~ ^\*\. ]]; then
        die "'${domain}': Squid dstdomain does not support '*.' — use a LEADING DOT ('.${domain#*.}') to match all subdomains, or a bare domain for an exact match"
    fi
    if ! [[ "${domain}" =~ ^(\.)?[A-Za-z0-9]([A-Za-z0-9-]*[A-Za-z0-9])?(\.[A-Za-z0-9]([A-Za-z0-9-]*[A-Za-z0-9])?)+$ ]]; then
        die "'${domain}' does not look like a bare domain (github.com) or a leading-dot subdomain entry (.githubusercontent.com) — no https://, no path"
    fi
}

cmd_allow() {
    local domain="${1:?usage: $0 allow <domain>}"
    validate_domain "${domain}"
    if grep -qxF "${domain}" "${ALLOWLIST}"; then
        ok "'${domain}' already allowlisted"
        return
    fi
    printf '%s\n' "${domain}" >> "${ALLOWLIST}"
    ok "added '${domain}' to ${ALLOWLIST}"
    cmd_restart
}

# Source-guard: tests/run-tests.sh sources this file to unit-test the pure
# functions; the CLI must only run when executed directly.
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    case "${1:-}" in
        up)      cmd_up ;;
        down)    cmd_down ;;
        status)  cmd_status ;;
        restart) cmd_restart ;;
        logs)    cmd_logs ;;
        allow)   shift; cmd_allow "${1:-}" ;;
        *)       sed -n '2,15p' "${BASH_SOURCE[0]}"; exit 2 ;;
    esac
fi
