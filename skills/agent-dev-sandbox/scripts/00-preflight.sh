#!/usr/bin/env bash
# ============================================================================
# 00-preflight.sh — read-only host readiness checks
# ============================================================================
# Checks everything the blueprint needs on the Debian 13 host BEFORE and
# AFTER bootstrap. Fixes nothing; reports BLOCKERS (must fix) and WARNINGS
# (may proceed). Exit code: 0 = no blockers, 1 = blockers found.
#
# Usage: scripts/00-preflight.sh [--post]   (--post = stricter post-install
#                                          checks: podman, linger, subuid)
# ============================================================================
set -uo pipefail

case "${1:-}" in
    "")       MODE="" ;;
    --post)   MODE="--post" ;;
    *)        echo "unknown option: $1 (only --post is supported)" >&2; exit 2 ;;
esac

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
ok()   { echo -e "  ${GREEN}PASS${NC}  $1"; }
fail() { echo -e "  ${RED}FAIL${NC}  $1"; }
warn() { echo -e "  ${YELLOW}WARN${NC}  $1"; }
info() { echo -e "  ${BLUE}INFO${NC}  $1"; }

BLOCKERS=0
WARNINGS=0
fail_b() { fail "$1"; BLOCKERS=$((BLOCKERS+1)); }
warn_w() { warn "$1"; WARNINGS=$((WARNINGS+1)); }

echo "============================================"
echo "  agent-dev-sandbox — Host Preflight"
echo "============================================"

# --- OS / kernel -------------------------------------------------------------
if [ -r /etc/os-release ]; then
    # shellcheck disable=SC1091
    . /etc/os-release
    if [ "${ID:-}" = "debian" ] && [ "${VERSION_ID:-}" = "13" ]; then
        ok "Debian 13 (${PRETTY_NAME:-trixie})"
    else
        fail_b "This blueprint targets Debian 13; found ${PRETTY_NAME:-unknown} — the scripts rely on trixie package names and versions. Do not proceed on other distributions."
    fi
else
    fail_b "/etc/os-release unreadable — cannot identify distribution"
fi

KVER="$(uname -r | cut -d. -f1-2)"
KMAJ="${KVER%%.*}"; KMIN="${KVER#*.}"
if [ "${KMAJ}" -gt 5 ] || { [ "${KMAJ}" -eq 5 ] && [ "${KMIN}" -ge 12 ]; }; then
    ok "Kernel ${KVER} (>= 5.12 needed for unprivileged overlayfs)"
else
    fail_b "Kernel ${KVER} too old for rootless overlay (need >= 5.12)"
fi

case "$(uname -m)" in
    x86_64) ok "Architecture x86_64 (all tiers supported)";;
    aarch64) warn_w "Architecture aarch64: Tier 1 fully supported; Tier 2 script selects the arm64 cloud image — verify it exists on cloud.debian.org before use";;
    *) fail_b "Unsupported architecture $(uname -m)";;
esac

# --- Resources ---------------------------------------------------------------
RAM_MB="$(awk '/MemTotal/ {print int($2/1024)}' /proc/meminfo)"
if   [ "${RAM_MB}" -ge 16000 ]; then ok "RAM ${RAM_MB} MB (comfortable for containers + 1 micro-VM)"
elif [ "${RAM_MB}" -ge 8000 ];  then warn_w "RAM ${RAM_MB} MB — Tier 1 fine; micro-VM tier will be tight"
else fail_b "RAM ${RAM_MB} MB — below the 8 GB floor for any tier"; fi

DISK_AVAIL_GB="$(df -BG "${HOME}" | awk 'NR==2 {gsub("G","",$4); print $4}')"
if [ "${DISK_AVAIL_GB}" -ge 40 ]; then
    ok "Free disk in \$HOME: ${DISK_AVAIL_GB} GB (need ~15 GB base + ~4 GB/VM)"
else
    warn_w "Free disk in \$HOME: ${DISK_AVAIL_GB} GB — image + browsers alone need ~10-15 GB"
fi

# --- KVM (Tier 2 only) -------------------------------------------------------
if [ -e /dev/kvm ] && [ -w /dev/kvm ]; then
    ok "/dev/kvm present and writable — Tier 2 (micro-VM) available"
elif [ -e /dev/kvm ]; then
    warn_w "/dev/kvm exists but not writable — run bootstrap --tier2, then re-login (kvm group)"
else
    info "/dev/kvm not found — Tier 2 unavailable; Tier 1 (containers) unaffected (CPU without virt extensions or module not loaded)"
fi

# --- Host egress (needed at BUILD time; only containers are restricted) ------
for url in https://deb.debian.org https://registry.npmjs.org https://deb.nodesource.com https://github.com https://cloud.debian.org; do
    if curl -sI --max-time 8 -o /dev/null "${url}"; then
        ok "host egress: ${url}"
    else
        fail_b "host cannot reach ${url} — image build will fail"
    fi
done

# --- Rootless podman state (post-bootstrap mode) ------------------------------
if [ "${MODE}" = "--post" ]; then
    if command -v podman >/dev/null 2>&1; then
        if podman info >/dev/null 2>&1; then
            ok "podman info works as $(id -un)"
        else
            fail_b "podman installed but 'podman info' fails — check subuid/subgid and storage (see references/troubleshooting.md §2)"
        fi
    else
        fail_b "podman not installed — run scripts/10-host-bootstrap.sh"
    fi

    if grep -q "^$(id -un):" /etc/subuid 2>/dev/null && grep -q "^$(id -un):" /etc/subgid 2>/dev/null; then
        ok "subuid/subgid ranges present for $(id -un)"
    else
        fail_b "missing subuid/subgid ranges — run scripts/10-host-bootstrap.sh"
    fi

    if command -v loginctl >/dev/null 2>&1 && loginctl show-user "$(id -un)" 2>/dev/null | grep -q "^Linger=yes"; then
        ok "user lingering enabled (gateway survives logout)"
    else
        warn_w "user lingering not enabled — gateway quadlet will stop when you log out"
    fi

    # jq is required on the HOST by 45-ci-run.sh (installed by bootstrap;
    # audit M-6: it used to be an undeclared dependency).
    if command -v jq >/dev/null 2>&1; then
        ok "jq present (required by 45-ci-run.sh)"
    else
        warn_w "jq missing — CI runs (45-ci-run.sh) will refuse to start: sudo apt install jq"
    fi

    # The --internal network semantics (no default route, aardvark answering
    # container names only) are guaranteed by netavark (audit M-6).
    if command -v podman >/dev/null 2>&1; then
        NETBACKEND="$(podman info --format '{{.Host.NetworkBackend}}' 2>/dev/null || true)"
        case "${NETBACKEND}" in
            netavark) ok "podman network backend: netavark (--internal semantics as documented)" ;;
            "")       : ;;  # podman info failed; already reported above
            *)        warn_w "podman network backend is '${NETBACKEND}', not netavark — --internal DNS/routing semantics are unverified on this setup" ;;
        esac
    fi
else
    command -v podman >/dev/null 2>&1 && info "podman $(podman --version | awk '{print $3}') already installed" \
                                    || info "podman not installed yet — that is expected before bootstrap"
fi

echo "--------------------------------------------"
echo -e "  ${GREEN}${BLOCKERS} blocker(s)${NC}, ${YELLOW}${WARNINGS} warning(s)${NC}"
if [ "${BLOCKERS}" -gt 0 ]; then
    echo "  Fix blockers, then re-run. See references/troubleshooting.md §1."
    exit 1
fi
echo "  Ready for the next phase (see SKILL.md)."
exit 0
