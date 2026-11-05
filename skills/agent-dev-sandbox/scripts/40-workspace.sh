#!/usr/bin/env bash
# ============================================================================
# 40-workspace.sh — per-project workspace lifecycle (Tier 1)
# ============================================================================
# One persistent workspace per project/repository. Each workspace is a
# hardened rootless container:
#   * --userns=keep-id:uid=1000,gid=1000  host user == container `dev`
#                                         (bind mounts owned correctly)
#   * --network agent-internal            no route out except the proxy
#   * --cap-drop=ALL + no-new-privileges  no Linux capabilities, ever
#   * pids/memory/cpu limits              runaway builds cannot take the host
#   * secrets via --env-file              never baked into the image
#
# Usage:
#   scripts/40-workspace.sh create  <name> [--repo <url>] [--memory 6g] [--cpus 4]
#   scripts/40-workspace.sh shell   <name>      # interactive login shell
#   scripts/40-workspace.sh exec    <name> <cmd...>
#   scripts/40-workspace.sh start|stop|status   <name>
#   scripts/40-workspace.sh restart <name>      # recreate => re-reads env file
#   scripts/40-workspace.sh list
#   scripts/40-workspace.sh snapshot <name>     # image commit + home backup
#   scripts/40-workspace.sh destroy <name> [--purge-home] [--purge-workspace]
# ============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

IMAGE="agent-dev-sandbox"; TAG="1"
NET_INTERNAL="agent-internal"
GW="agent-gateway"
WS_ROOT="${HOME}/agent-workspaces"
CFG_ROOT="${HOME}/.config/agent-sandbox/workspaces"
NAME=""

GREEN='\033[0;32m'; RED='\033[0;31m'; YELLOW='\033[1;33m'; NC='\033[0m'
ok()   { echo -e "  ${GREEN}✓${NC} $1"; }
die()  { echo -e "  ${RED}✗ $1${NC}" >&2; exit 1; }

validate_name() {
    [[ "${NAME}" =~ ^[a-z][a-z0-9-]{0,38}$ ]] || die "workspace name must be lowercase letters/digits/hyphens, start with a letter, max 39 chars (got: '${NAME}')"
    [[ "${NAME}" != __* ]] || die "names starting with '__' are reserved (50-verify.sh canary '__verify', 45-ci-run.sh ephemeral runs '__ci-*')"
}

ctname()       { echo "agent-${NAME}"; }
env_file()     { echo "${CFG_ROOT}/${NAME}.env"; }
meta_file()    { echo "${CFG_ROOT}/${NAME}.meta"; }

ensure_gateway_up() {
    if ! podman ps --format '{{.Names}}' | grep -qx "${GW}"; then
        echo "  → gateway not running; starting it via 30-gateway.sh up"
        "${SCRIPT_DIR}/30-gateway.sh" up >/dev/null
    fi
}

write_env_template() {
    local f; f="$(env_file)"
    if [ -e "$f" ]; then
        ok "env file exists: $f (mode $(stat -c %a "$f"))"
        return
    fi
    mkdir -p "${CFG_ROOT}"
    cat > "$f" <<EOF
# Secrets for workspace '${NAME}' — injected into the container at start ONLY.
# Lives on the host, outside every container and image. Never commit it.
# Fill in the keys you use, uncomment, then: scripts/40-workspace.sh restart ${NAME}
#ANTHROPIC_API_KEY=
#OPENAI_API_KEY=

# Optional git identity (exported into shells)
#GIT_AUTHOR_NAME=
#GIT_AUTHOR_EMAIL=
EOF
    chmod 600 "$f"
    ok "created env template $f — EDIT IT to add API keys (mode 600)"
}

# The single auditable container invocation used by create + restart.
run_workspace() {
    local memory="$1" cpus="$2"
    podman run -d \
        --name "$(ctname)" \
        --hostname "${NAME}" \
        --userns=keep-id:uid=1000,gid=1000 \
        --network "${NET_INTERNAL}" \
        --cap-drop=ALL \
        --security-opt no-new-privileges \
        --pids-limit 1024 \
        --memory "${memory}" \
        --cpus "${cpus}" \
        -v "${WS_ROOT}/${NAME}:/workspace:Z" \
        -v "agent-home-${NAME}:/home/dev:Z" \
        -e "http_proxy=http://${GW}:3128" \
        -e "https_proxy=http://${GW}:3128" \
        -e "HTTP_PROXY=http://${GW}:3128" \
        -e "HTTPS_PROXY=http://${GW}:3128" \
        -e "no_proxy=localhost,127.0.0.1,::1" \
        -e "NO_PROXY=localhost,127.0.0.1,::1" \
        -e "PLAYWRIGHT_BROWSERS_PATH=/home/dev/.cache/ms-playwright" \
        --env-file "$(env_file)" \
        "${IMAGE}:${TAG}" >/dev/null
}

clone_repo() {
    local repo="$1"
    local dest; dest="/workspace/$(basename "${repo%.git}")"
    echo "  → cloning ${repo} through the allowlist proxy…"
    if podman exec --workdir /workspace "$(ctname)" git clone "${repo}" "${dest}"; then
        ok "cloned to ${WS_ROOT}/${NAME}/$(basename "${repo%.git}")"
    else
        echo -e "  ${YELLOW}○${NC} clone failed — is the git host in files/squid/allowlist.txt? Add it: 30-gateway.sh allow <domain>"
    fi
}

cmd_create() {
    local repo="" memory="6g" cpus="4"
    while [ $# -gt 0 ]; do
        case "$1" in
            --repo)   shift; repo="${1:?--repo needs a URL}" ;;
            --memory) shift; memory="${1:?--memory needs a value}" ;;
            --cpus)   shift; cpus="${1:?--cpus needs a value}" ;;
            *) die "unknown option: $1" ;;
        esac
        shift
    done
    validate_name
    podman image exists "${IMAGE}:${TAG}" 2>/dev/null || die "image ${IMAGE}:${TAG} not found — run scripts/20-build-image.sh"
    podman container exists "$(ctname)" 2>/dev/null && die "workspace '${NAME}' already exists"
    ensure_gateway_up

    mkdir -p "${WS_ROOT}/${NAME}"
    write_env_template
    printf 'MEMORY=%s\nCPUS=%s\n' "${memory}" "${cpus}" > "$(meta_file)"

    run_workspace "${memory}" "${cpus}"
    ok "workspace '${NAME}' started (container $(ctname), ${memory} RAM, ${cpus} CPUs)"

    podman exec "$(ctname)" seed-playwright-browsers
    ok "shared browsers linked into workspace home"

    [ -n "${repo}" ] && clone_repo "${repo}"
    echo
    echo "  Enter it:   scripts/40-workspace.sh shell ${NAME}"
    echo "  Add keys:   $(env_file)  → then: scripts/40-workspace.sh restart ${NAME}"
}

cmd_shell() {
    podman container exists "$(ctname)" >/dev/null 2>&1 || die "workspace '${NAME}' does not exist"
    podman start "$(ctname)" >/dev/null 2>&1 || true
    exec podman exec -it "$(ctname)" ws-shell
}

cmd_exec() {
    local name="$1"; shift
    NAME="${name}"; validate_name
    podman start "$(ctname)" >/dev/null 2>&1 || true
    exec podman exec -it "$(ctname)" "$@"
}

cmd_start()  { podman start "$(ctname)" >/dev/null && ok "'${NAME}' started"; }
cmd_stop()   { podman stop  "$(ctname)" >/dev/null && ok "'${NAME}' stopped (data preserved)"; }
cmd_status() { podman ps -a --filter "name=^$(ctname)$" --format "table {{.Names}}\t{{.Status}}\t{{.Networks}}"; }

cmd_list() {
    printf "  %-24s %-12s %s\n" "WORKSPACE" "STATE" "HOME VOLUME"
    local f n state
    for f in "${CFG_ROOT}"/*.env; do
        [ -e "$f" ] || break
        n="$(basename "$f" .env)"
        state="$(podman inspect -f '{{.State.Status}}' "agent-${n}" 2>/dev/null || echo '-')"
        printf "  %-24s %-12s %s\n" "${n}" "${state}" "agent-home-${n}"
    done
}

cmd_snapshot() {
    local ts; ts="$(date +%Y%m%d-%H%M%S)"
    podman commit "$(ctname)" "ws-snap-${NAME}:${ts}" >/dev/null
    ok "container state committed as ws-snap-${NAME}:${ts}"
    podman run --rm -v "agent-home-${NAME}:/from:ro" -v "${WS_ROOT}:/to" \
        "${IMAGE}:${TAG}" tar czf "/to/${NAME}-home-${ts}.tar.gz" -C /from . >/dev/null
    ok "home volume backed up to ${WS_ROOT}/${NAME}-home-${ts}.tar.gz"
}

cmd_restart() {
    [ -f "$(meta_file)" ] || die "no meta file for '${NAME}' — recreate it with: create ${NAME}"
    # shellcheck disable=SC1090
    source "$(meta_file)"
    podman rm -f "$(ctname)" >/dev/null 2>&1 || die "workspace '${NAME}' has no container"
    run_workspace "${MEMORY:-6g}" "${CPUS:-4}"
    podman exec "$(ctname)" seed-playwright-browsers
    ok "'${NAME}' recreated — env file re-read, new keys now active"
}

cmd_destroy() {
    local purge_home=0 purge_ws=0
    while [ $# -gt 0 ]; do
        case "$1" in
            --purge-home)      purge_home=1 ;;
            --purge-workspace) purge_ws=1 ;;
            *) die "unknown option: $1" ;;
        esac
        shift
    done
    podman rm -f "$(ctname)" >/dev/null 2>&1 || die "workspace '${NAME}' has no container"
    ok "container $(ctname) removed"
    if [ "${purge_home}" -eq 1 ]; then
        podman volume rm "agent-home-${NAME}" >/dev/null && ok "home volume agent-home-${NAME} removed"
    else
        echo -e "  ${YELLOW}○${NC} home volume 'agent-home-${NAME}' KEPT (use --purge-home to delete auth/caches too)"
    fi
    if [ "${purge_ws}" -eq 1 ]; then
        rm -rf "${WS_ROOT:?}/${NAME:?}" && ok "workspace directory removed"
    else
        ok "workspace directory kept at ${WS_ROOT}/${NAME} (your code!) — use --purge-workspace to delete"
    fi
    rm -f "$(env_file)" "$(meta_file)" && ok "env + meta files removed"
}

main() {
    [ $# -ge 1 ] || { sed -n '2,21p' "${BASH_SOURCE[0]}"; exit 2; }
    local cmd="$1"; shift
    case "${cmd}" in
        create)   NAME="${1:?usage: create <name> [options]}"; shift; cmd_create "$@" ;;
        shell)    NAME="${1:?usage: shell <name>}"; cmd_shell ;;
        exec)     [ $# -ge 2 ] || die "usage: exec <name> <cmd...>"; cmd_exec "$@" ;;
        start)    NAME="${1:?usage: start <name>}"; cmd_start ;;
        stop)     NAME="${1:?usage: stop <name>}"; cmd_stop ;;
        status)   NAME="${1:?usage: status <name>}"; cmd_status ;;
        restart)  NAME="${1:?usage: restart <name>}"; cmd_restart ;;
        list)     cmd_list ;;
        snapshot) NAME="${1:?usage: snapshot <name>}"; cmd_snapshot ;;
        destroy)  NAME="${1:?usage: destroy <name> [--purge-home] [--purge-workspace]}"; shift; cmd_destroy "$@" ;;
        *) sed -n '2,21p' "${BASH_SOURCE[0]}"; exit 2 ;;
    esac
}
main "$@"
