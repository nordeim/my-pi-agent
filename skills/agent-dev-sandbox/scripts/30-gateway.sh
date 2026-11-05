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

[Service]
Restart=always

[Install]
WantedBy=default.target
EOF
}

start_gateway() {
    ensure_networks
    ensure_image
    # Prefer the systemd user unit whenever a user session manager exists;
    # fall back to plain podman otherwise.
    if systemctl --user is-system-running >/dev/null 2>&1; then
        podman rm -f "${GW_NAME}" >/dev/null 2>&1 || true   # transition from a previous plain-podman run
        write_quadlet
        systemctl --user daemon-reload
        systemctl --user enable --now "${GW_NAME}.service"
        ok "gateway started via systemd user unit (survives reboots)"
    else
        # Fallback: no working user systemd — plain rootless podman.
        podman rm -f "${GW_NAME}" >/dev/null 2>&1 || true
        podman run -d --name "${GW_NAME}" \
            --network "${NET_EGRESS}" --network "${NET_INTERNAL}" \
            --restart=always \
            -v "${ALLOWLIST}:/etc/squid/allowlist.txt:ro,Z" \
            "${GW_IMAGE}" >/dev/null
        ok "gateway started via podman (no systemd user session detected)"
    fi
    sleep 1
    status
}

cmd_up() { start_gateway; }

cmd_down() {
    if [ -f "${QUADLET_FILE}" ]; then
        systemctl --user disable --now "${GW_NAME}.service" 2>/dev/null || true
        systemctl --user daemon-reload 2>/dev/null || true
    fi
    podman rm -f "${GW_NAME}" >/dev/null 2>&1 || true
    ok "gateway stopped (networks left in place for running workspaces)"
}

cmd_restart() {
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
    echo "  networks:"
    podman network ls --format "    {{.Name}}  {{.Driver}}" | grep -E "agent-(egress|internal)" || echo "    (missing — run: $0 up)"
    echo "  live allowlist probe (expect HTTP 200 through the proxy):"
    if podman run --rm --network "${NET_INTERNAL}" \
            agent-dev-sandbox:1 \
            curl -sS --max-time 15 --proxy "http://${GW_NAME}:3128" \
                 -o /dev/null -w '    status=%{http_code}\n' \
                 https://registry.npmjs.org 2>/dev/null; then
        ok "proxy path works end-to-end"
    else
        echo -e "  ${RED}✗ probe failed — see $0 logs and references/troubleshooting.md §4${NC}"
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

cmd_allow() {
    local domain="${1:?usage: $0 allow <domain>}"
    # Basic sanity: looks like a domain name (no scheme, no path, no spaces).
    if ! [[ "${domain}" =~ ^(\*\.)?[A-Za-z0-9]([A-Za-z0-9-]*[A-Za-z0-9])?(\.[A-Za-z]([A-Za-z0-9-]*[A-Za-z0-9])?)+$ ]]; then
        die "'${domain}' does not look like a bare domain (no https://, no path)"
    fi
    if grep -qxF "${domain}" "${ALLOWLIST}"; then
        ok "'${domain}' already allowlisted"
        return
    fi
    printf '%s\n' "${domain}" >> "${ALLOWLIST}"
    ok "added '${domain}' to ${ALLOWLIST}"
    cmd_restart
}

case "${1:-}" in
    up)      cmd_up ;;
    down)    cmd_down ;;
    status)  cmd_status ;;
    restart) cmd_restart ;;
    logs)    cmd_logs ;;
    allow)   shift; cmd_allow "${1:-}" ;;
    *)       sed -n '2,15p' "${BASH_SOURCE[0]}"; exit 2 ;;
esac
