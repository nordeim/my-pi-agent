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
case "${1:-}" in
    "")        ;;
    --tier2)   TIER2=1 ;;
    *)         echo "unknown option: $1 (only --tier2 is supported)" >&2; exit 2 ;;
esac

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
# jq: required by scripts/45-ci-run.sh on the HOST (audit M-6: it used to be
# an undeclared dependency — a missing jq aborted CI teardown under set -e).
info "Installing core packages (podman stack)…"
apt-get update -qq
apt-get install -y -qq podman buildah crun passt slirp4netns uidmap curl ca-certificates jq

if [ "${TIER2}" -eq 1 ]; then
    info "Installing Tier-2 packages (QEMU/KVM, cloud-image-utils, host squid)…"
    # openssh-client: ssh/scp/ssh-keygen are used by 60-tier2-microvm.sh
    # (audit M-6: absent from minimal server installs).
    apt-get install -y -qq qemu-system-x86 qemu-utils cloud-image-utils squid openssh-client
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
# Audit L-2: the fixed 100000-165535 range could overlap another user's
# allocation on shared hosts — allocate the NEXT FREE range instead.
next_free_range() { # <subuid|subgid file>
    local file="$1" max_end=0
    [ -f "${file}" ] || { echo "100000 165535"; return; }
    local end
    while read -r _ _ end; do
        [ "${end:-0}" -gt "${max_end}" ] && max_end="${end}"
    done < "${file}"
    if [ "${max_end}" -lt 100000 ]; then
        echo "100000 165535"
    else
        echo "$((max_end + 1)) $((max_end + 65536))"
    fi
}
if grep -q "^${REAL_USER}:" /etc/subuid 2>/dev/null; then
    ok "${REAL_USER} already present in /etc/subuid"
else
    read -r SU_START SU_END < <(next_free_range /etc/subuid)
    usermod --add-subuid "${SU_START}-${SU_END}" "${REAL_USER}"
    ok "added subuid range ${SU_START}-${SU_END} for ${REAL_USER} in /etc/subuid"
fi
if grep -q "^${REAL_USER}:" /etc/subgid 2>/dev/null; then
    ok "${REAL_USER} already present in /etc/subgid"
else
    read -r SG_START SG_END < <(next_free_range /etc/subgid)
    usermod --add-subgid "${SG_START}-${SG_END}" "${REAL_USER}"
    ok "added subgid range ${SG_START}-${SG_END} for ${REAL_USER} in /etc/subgid"
fi

# Allow unprivileged ICMP (rootless containers lack CAP_NET_RAW otherwise).
# NOTE: sysctl prints this value TAB-separated, so compare numerically.
# Audit L-2: the old EXACT-string match would have NARROWED a host that was
# already wider (e.g. manually set to 0 2147483647). Widen only, never narrow.
# (Debian 13's systemd ships no ping_group_range default — verified — so the
# common case is the kernel default "1 0".)
PGR="$(sysctl -n net.ipv4.ping_group_range 2>/dev/null | tr -s '[:space:]' ' ')"
PGR_HI="${PGR##* }"
if [ "${PGR_HI:-0}" -lt 2000000 ] 2>/dev/null; then
    printf 'net.ipv4.ping_group_range = 0 2000000\n' > /etc/sysctl.d/99-agent-sandbox.conf
    sysctl --system >/dev/null
    ok "sysctl net.ipv4.ping_group_range widened to 0 2000000 (rootless ping)"
else
    ok "ping_group_range already wide enough (${PGR}) — left untouched"
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
        # Audit L-2: the marker makes the 'refresh' branch below reachable —
        # it was historically checked but never created.
        touch /etc/squid/squid.conf.agent-sandbox
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
