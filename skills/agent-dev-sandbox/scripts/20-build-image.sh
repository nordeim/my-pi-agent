#!/usr/bin/env bash
# ============================================================================
# 20-build-image.sh — build the Tier-1 workspace image (rootless podman)
# ============================================================================
# Usage: scripts/20-build-image.sh [--no-cache] [--tag <tag>]
#
# First build downloads ~1.5-2 GB (Node, Chromium, browsers) and takes
# 5-15 minutes depending on network. Later builds are layer-cached and fast.
# ============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(dirname "${SCRIPT_DIR}")"

TAG="1"
NO_CACHE=""
while [ $# -gt 0 ]; do
    case "$1" in
        --no-cache) NO_CACHE="--no-cache" ;;
        --tag) shift; TAG="${1:?--tag needs a value}" ;;
        *) echo "unknown option: $1" >&2; exit 2 ;;
    esac
    shift
done

IMAGE="agent-dev-sandbox"

echo "============================================"
echo "  Building ${IMAGE}:${TAG}"
echo "============================================"

# Guard: rootless podman must work (bootstrap not run / subuid missing).
if ! podman info >/dev/null 2>&1; then
    echo "ERROR: 'podman info' failed as $(id -un)." >&2
    echo "       Run scripts/10-host-bootstrap.sh first (see references/troubleshooting.md §2)." >&2
    exit 1
fi

# NO_CACHE is intentionally word-split when empty:
# shellcheck disable=SC2086
podman build ${NO_CACHE} -t "${IMAGE}:${TAG}" -f "${SKILL_ROOT}/files/Containerfile" "${SKILL_ROOT}/files" \
    || { echo "ERROR: image build failed — see the podman output above (references/troubleshooting.md §3)" >&2; exit 1; }

echo
echo "  Image built:"
podman image ls "${IMAGE}:${TAG}" --format "table {{.Repository}}:{{.Tag}}\t{{.Size}}\t{{.CreatedSince}}"
echo
echo "  Next: scripts/30-gateway.sh up"
echo "============================================"
