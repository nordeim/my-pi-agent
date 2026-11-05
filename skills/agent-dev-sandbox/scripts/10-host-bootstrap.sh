#!/usr/bin/env bash
# ============================================================================
# 10-host-bootstrap.sh — one-time host setup (idempotent, requires sudo)
# ============================================================================
# Installs packages, configures rootless-podman prerequisites (subuid/subgid,
# ping sysctl, lingering), and — with --tier2 — QEMU/KVM plus the host-side
# allowlist proxy for micro-VMs.
#
# Usage (from your normal user account, NOT root):
#     scripts/10-host-bootstrap.sh [--tier2]
# ============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(dirname "${SCRIPT_DIR}")"
TIER2=0
[ "${1:-}" = "--tier2" ] && TIER2=1

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
ok()   { echo -e "  ${GREEN}✓${NC} $1"; }
info() { echo -e "  ${BLUE}→${NC} $1"; }
warn() { echo -e "  ${YELLOW}○${NC} $1"; }

if [ "$(id -u)" -ne 0 ]; then
    exec sudo -E "$0" "${1:-}"
fi

REAL_USER="${SUDO_USER:-}"
if [ -z "${REAL_USER}" ] || [ "${REAL_USER}" = "root" ]; then
    echo -e "${RED}Run this script from your normal user account (it re-execs itself with sudo).${NC}"
    exit 1
fi
REAL_HOME="$(getent passwd "${REAL_USER}" | cut -d: -f6)"
export DEBIAN_FRONTEND=noninteractive

echo "============================================"
echo "  agent-dev-sandbox — Host Bootstrap (user: ${REAL_USER})"
echo "============================================"

# --- 1. Packages --------------------------------------------------------------
info "Installing core packages (podman stack)…"
apt-get update -qq
apt-get install -y -qq podman buildah crun passt slirp4netns uidmap curl ca-certificates

if [ "${TIER2}" -eq 1 ]; then
    info "Installing Tier-2 packages (QEMU/KVM, cloud-image-utils, host squid)…"
    apt-get install -y -qq qemu-system-x86 qemu-utils cloud-image-utils squid
    if ! getent group kvm >/dev/null; then
        warn "no 'kvm' group on this system — check virtualization support"
    elif id -nG "${REAL_USER}" | grep -qw kvm; then
        ok "user ${REAL_USER} already in kvm group"
    else
        usermod -aG kvm "${REAL_USER}"
        warn "added ${REAL_USER} to kvm group — LOG OUT AND BACK IN before Tier 2"
    fi
fi
ok "packages installed"

# --- 2. Rootless podman prerequisites -----------------------------------------
# subuid/subgid ranges: required for --userns=keep-id and rootless networking.
if grep -q "^${REAL_USER}:" /etc/subuid 2>/dev/null; then
    ok "${REAL_USER} already present in /etc/subuid"
else
    usermod --add-subuid 100000-165535 "${REAL_USER}"
    ok "added subuid range for ${REAL_USER} in /etc/subuid"
fi
if grep -q "^${REAL_USER}:" /etc/subgid 2>/dev/null; then
    ok "${REAL_USER} already present in /etc/subgid"
else
    usermod --add-subgid 100000-165535 "${REAL_USER}"
    ok "added subgid range for ${REAL_USER} in /etc/subgid"
fi

# Allow unprivileged ICMP (rootless containers lack CAP_NET_RAW otherwise).
# NOTE: sysctl prints this value TAB-separated ("1\t0"), so compare with all
# whitespace stripped — a plain grep for "0 2000000" would never match.
if [ "$(sysctl -n net.ipv4.ping_group_range 2>/dev/null | tr -d '[:space:]')" != "02000000" ]; then
    printf 'net.ipv4.ping_group_range = 0 2000000\n' > /etc/sysctl.d/99-agent-sandbox.conf
    sysctl --system >/dev/null
    ok "sysctl net.ipv4.ping_group_range widened (rootless ping)"
else
    ok "ping_group_range already wide"
fi

# Linger: keep the user systemd instance (and the gateway quadlet) alive
# across SSH sessions.
if loginctl enable-linger "${REAL_USER}" 2>/dev/null; then
    ok "lingering enabled for ${REAL_USER}"
else
    warn "could not enable lingering (no systemd?) — gateway will need manual restarts"
fi

# --- 3. Directories (as the real user) ----------------------------------------
sudo -u "${REAL_USER}" mkdir -p \
    "${REAL_HOME}/.config/agent-sandbox/workspaces" \
    "${REAL_HOME}/agent-workspaces" \
    "${REAL_HOME}/.local/share/agent-sandbox/microvm" \
    "${REAL_HOME}/.config/containers/systemd" \
    "${REAL_HOME}/.config/systemd/user"
ok "directory skeleton created under ${REAL_HOME}"

# --- 4. Tier-2 host proxy (same allowlist as the container gateway) -----------
if [ "${TIER2}" -eq 1 ] && command -v squid >/dev/null 2>&1; then
    if dpkg -s squid >/dev/null 2>&1 && [ ! -f /etc/squid/squid.conf.agent-sandbox ]; then
        # Preserve any pre-existing config once, then install ours.
        if [ -f /etc/squid/squid.conf ] && ! grep -q "agent sandbox egress allowlist proxy" /etc/squid/squid.conf; then
            cp /etc/squid/squid.conf /etc/squid/squid.conf.pre-agent-sandbox
            warn "existing squid.conf backed up to squid.conf.pre-agent-sandbox"
        fi
        cp "${SKILL_ROOT}/files/squid/squid-host.conf" /etc/squid/squid.conf
        cp "${SKILL_ROOT}/files/squid/allowlist.txt" /etc/squid/allowlist.txt
        chmod 0644 /etc/squid/squid.conf /etc/squid/allowlist.txt
        systemctl enable --now squid
        systemctl restart squid
        ok "host squid installed on 127.0.0.1:3128 (allowlist: /etc/squid/allowlist.txt)"
    else
        if [ -f /etc/squid/squid.conf.agent-sandbox ]; then
            cp "${SKILL_ROOT}/files/squid/allowlist.txt" /etc/squid/allowlist.txt
            systemctl restart squid
            ok "host squid allowlist refreshed"
        else
            warn "squid present but not installed by this script — edit /etc/squid manually per files/squid/squid-host.conf"
        fi
    fi
fi

echo "--------------------------------------------"
echo "  Bootstrap complete."
echo "  Next: scripts/00-preflight.sh --post"
echo "        scripts/20-build-image.sh"
[ "${TIER2}" -eq 1 ] && echo "  (then re-login once for the kvm group, before scripts/60-tier2-microvm.sh)"
echo "============================================"
