#!/usr/bin/env bash
# ============================================================================
# 45-ci-run.sh — ephemeral CI runs (same image, throwaway workspaces)
# ============================================================================
# A CI run is a SINGLE-SHOT hardened container from the same
# agent-dev-sandbox:1 image used by interactive workspaces. Lifecycle:
#     create -> ci-setup (env, caches, browsers, ISOLATION SELF-AUDIT,
#               optional clone) -> run one command -> collect artifacts
#               -> destroy (always, unless --keep-on-failure)
#
# Invariants are identical to 40-workspace.sh (keep-id, cap-drop=ALL,
# no-new-privileges, agent-internal ONLY, env-file secrets, pids/memory/cpu
# caps) plus a walltime timeout. CI mode changes the CONSUMPTION of the image,
# not the trust tier: hostile PR builds still belong in a Tier-2 VM (run this
# same script inside it). Design: BLUEPRINT.md §12.
#
# Names and layout (the '__' prefix is reserved by 40-workspace.sh
# validate_name, so CI containers can never collide with workspaces and
# `reap` can never touch them):
#     containers: agent-__ci-<run-id>
#     ~/agent-workspaces/__ci/cache/           shared package caches (bind -> /cache)
#     ~/agent-workspaces/__ci/runs/<id>/       ephemeral per-run code (+ home)
#     ~/agent-workspaces/__ci/artifacts/<id>/  console.log, isolation-audit.json,
#                                               run-summary.json, copied reports
#
# Usage:
#   scripts/45-ci-run.sh run [options] -- <command...>
#       --repo <url>        shallow-clone inside the run (cwd becomes the repo)
#       --src <dir>         bind-mount an existing host checkout as /workspace
#       --run-id <id>       default: <yyyymmdd-hhmmss>-<pid>
#       --env-file <path>   secrets (0600); default ~/.config/agent-sandbox/ci.env
#                           if that file exists
#       --image <img:tag>   default agent-dev-sandbox:1
#       --memory <6g> --cpus <4>
#       --timeout <sec>     walltime cap, default 3600
#       --artifact-path <p> repeatable; /workspace-relative, copied out after
#                           (defaults: playwright-report test-results coverage
#                            dist build junit.xml)
#       --keep-on-failure   skip teardown when exit != 0 (debug with podman)
#       --skip-audit        skip the per-run isolation self-audit
#       --read-only-rootfs  read-only container fs + writable tmpfs (/tmp,
#                           /var/tmp, /run) and bind-mounted home
#       --no-cache-vol      no shared caches (isolated, cold — for untrusted
#                           sources or trust-domain separation)
#   scripts/45-ci-run.sh list
#   scripts/45-ci-run.sh reap [--ttl-hours N] [--purge-artifacts]
#   scripts/45-ci-run.sh cache        # wipe the shared package caches
#
# Exit codes: 0 ok · 66 isolation audit failed · 124 walltime timeout ·
#             125/126/127 podman-level error · otherwise the command's own.
# ============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(dirname "${SCRIPT_DIR}")"
CI_SETUP_SRC="${SKILL_ROOT}/files/ci-setup.sh"

IMAGE="agent-dev-sandbox"; TAG="1"
NET_INTERNAL="agent-internal"
GW="agent-gateway"
WS_ROOT="${HOME}/agent-workspaces"
CI_ROOT="${WS_ROOT}/__ci"
CFG_DIR="${HOME}/.config/agent-sandbox"

GREEN='\033[0;32m'; RED='\033[0;31m'; YELLOW='\033[1;33m'; NC='\033[0m'
ok()   { echo -e "  ${GREEN}✓${NC} $1"; }
info() { echo "  → $1"; }
die()  { echo -e "  ${RED}✗ $1${NC}" >&2; exit 1; }

usage() { sed -n '/^# Usage:/,/^# =\{70,\}$/p' "${BASH_SOURCE[0]}" | sed '1d;$d'; }

# Set by cmd_run, read by write_summary (avoids ambiguous positional plumbing).
RUN_COMMAND=()
RUN_COPIED=()
RUN_SECONDS=0

json_array() {  # json_array <items...> -> JSON array of strings
    if [ $# -eq 0 ]; then echo '[]'; else printf '%s\n' "$@" | jq -R . | jq -s .; fi
}

ensure_gateway_up() {
    if ! podman ps --format '{{.Names}}' | grep -qx "${GW}"; then
        info "gateway not running; starting it via 30-gateway.sh up"
        "${SCRIPT_DIR}/30-gateway.sh" up >/dev/null
    fi
}

reason_for() {
    case "$1" in
        0)   echo "ok" ;;
        66)  echo "audit-failure" ;;
        124) echo "timeout" ;;
        125|126|127) echo "podman-error" ;;
        *)   echo "command-failed" ;;
    esac
}

# ============================================================================
# run
# ============================================================================
cmd_run() {
    local repo="" src="" run_id="" env_file="" memory="6g" cpus="4" timeout_s=3600
    local image="${IMAGE}:${TAG}"
    local keep=0 skip_audit=0 read_only=0 use_cache=1
    local -a extra_arts=() run_command=()
    while [ $# -gt 0 ]; do
        case "$1" in
            --repo)             shift; repo="${1:?--repo needs a URL}" ;;
            --src)              shift; src="${1:?--src needs a directory}" ;;
            --run-id)           shift; run_id="${1:?--run-id needs a value}" ;;
            --env-file)         shift; env_file="${1:?--env-file needs a path}" ;;
            --image)            shift; image="${1:?--image needs img:tag}" ;;
            --memory)           shift; memory="${1:?--memory needs a value}" ;;
            --cpus)             shift; cpus="${1:?--cpus needs a value}" ;;
            --timeout)          shift; timeout_s="${1:?--timeout needs seconds}" ;;
            --artifact-path)    shift; extra_arts+=("${1:?--artifact-path needs a path}") ;;
            --keep-on-failure)  keep=1 ;;
            --skip-audit)       skip_audit=1 ;;
            --read-only-rootfs) read_only=1 ;;
            --no-cache-vol)     use_cache=0 ;;
            --)                 shift; run_command=("$@"); break ;;
            *) die "unknown option: $1 (see usage)" ;;
        esac
        shift
    done
    [ ${#run_command[@]} -ge 1 ] || die "no command given — usage: $0 run [options] -- <command...>"
    [ -z "${repo}" ] || [ -z "${src}" ] || die "--repo and --src are mutually exclusive"

    # --- resolve run identity ---------------------------------------------------
    if [ -z "${run_id}" ]; then
        run_id="$(date +%Y%m%d-%H%M%S)-$$"
    fi
    [[ "${run_id}" =~ ^[a-z0-9][a-z0-9-]{0,38}$ ]] \
        || die "run-id must be lowercase alnum/hyphens, start alnum, max 39 chars (got: '${run_id}')"
    local ct="agent-__ci-${run_id}"
    podman container exists "${ct}" 2>/dev/null && die "container ${ct} already exists — pick another --run-id"

    # --- resolve inputs ------------------------------------------------------------
    podman image exists "${image}" 2>/dev/null || die "image ${image} not found — run scripts/20-build-image.sh"
    ensure_gateway_up
    [ -f "${CI_SETUP_SRC}" ] || die "missing ${CI_SETUP_SRC} (incomplete bundle?)"

    local src_dir=""
    if [ -n "${src}" ]; then
        [ -d "${src}" ] || die "--src directory not found: ${src}"
        src_dir="$(cd "${src}" && pwd)"
    fi

    # Default env file: standard CI location, used only if it exists.
    local env_note="none (no secrets injected)"
    if [ -z "${env_file}" ] && [ -f "${CFG_DIR}/ci.env" ]; then
        env_file="${CFG_DIR}/ci.env"
    fi
    if [ -n "${env_file}" ]; then
        [ -f "${env_file}" ] || die "env file not found: ${env_file}"
        local mode; mode="$(stat -c %a "${env_file}")"
        [ "${mode}" = "600" ] || echo -e "  ${YELLOW}○${NC} env file mode is ${mode}, not 600 — tighten it: chmod 600 ${env_file}"
        env_note="${env_file}"
    fi

    # --- layout -----------------------------------------------------------------------
    local run_dir="${CI_ROOT}/runs/${run_id}"
    local art_dir="${CI_ROOT}/artifacts/${run_id}"
    mkdir -p "${CI_ROOT}/runs" "${CI_ROOT}/artifacts"
    [ -n "${src_dir}" ] || mkdir -p "${run_dir}"
    mkdir -p "${art_dir}"
    if [ "${use_cache}" -eq 1 ]; then
        mkdir -p "${CI_ROOT}/cache"/{npm,pip,uv,bun,pnpm-store}
    fi

    # Source root for post-run artifact copying (none for --src: the checkout
    # itself persists on the host, copying out would be redundant).
    local copy_root=""
    if [ -n "${repo}" ]; then
        copy_root="${run_dir}/$(basename "${repo%.git}")"
    elif [ -z "${src_dir}" ]; then
        copy_root="${run_dir}"
    fi

    # --- container invocation ------------------------------------------------------------
    # Commas inside option values (userns mapping, tmpfs sizes) are literal, so
    # they are held in named variables — array literals with commas read as
    # element separators to both humans and shellcheck.
    local userns_opt="keep-id:uid=1000,gid=1000"
    local tmpfs_tmp="/tmp:rw,size=2g,mode=1777"
    local tmpfs_vartmp="/var/tmp:rw,size=1g,mode=1777"
    local tmpfs_run="/run:rw,size=64m"
    local -a run_args=(
        --name "${ct}"
        --hostname "ci-${run_id}"
        --userns "${userns_opt}"
        --network "${NET_INTERNAL}"
        --cap-drop=ALL
        --security-opt no-new-privileges
        --pids-limit 1024
        --memory "${memory}"
        --cpus "${cpus}"
        --stop-timeout 30
        -v "${art_dir}:/artifacts:Z"
        -v "${CI_SETUP_SRC}:/usr/local/bin/ci-setup:ro,Z"
        -e "http_proxy=http://${GW}:3128"
        -e "https_proxy=http://${GW}:3128"
        -e "HTTP_PROXY=http://${GW}:3128"
        -e "HTTPS_PROXY=http://${GW}:3128"
        -e "no_proxy=localhost,127.0.0.1,::1"
        -e "NO_PROXY=localhost,127.0.0.1,::1"
        -e "PLAYWRIGHT_BROWSERS_PATH=/home/dev/.cache/ms-playwright"
        -e "CI_RUN_ID=${run_id}"
        -e "CI_SKIP_AUDIT=${skip_audit}"
    )
    if [ -n "${src_dir}" ]; then
        run_args+=(-v "${src_dir}:/workspace:Z")
    else
        run_args+=(-v "${run_dir}:/workspace:Z")
    fi
    if [ -n "${repo}" ]; then
        run_args+=(-e "CI_REPO_URL=${repo}")
    fi
    if [ "${use_cache}" -eq 1 ]; then
        run_args+=(-v "${CI_ROOT}/cache:/cache:Z")
    fi
    if [ "${read_only}" -eq 1 ]; then
        # Writable island mounts: tmpfs for system scratch, bind for home
        # (same-uid bind mounts are this design's proven primitive, D5).
        mkdir -p "${run_dir}/home"
        run_args+=(--read-only
                   --tmpfs "${tmpfs_tmp}"
                   --tmpfs "${tmpfs_vartmp}"
                   --tmpfs "${tmpfs_run}"
                   -v "${run_dir}/home:/home/dev:Z")
    fi
    if [ -n "${env_file}" ]; then
        run_args+=(--env-file "${env_file}")
    fi

    echo "============================================"
    echo "  CI run ${run_id}"
    echo "    image:    ${image}"
    echo "    source:   ${repo:-${src_dir:-empty workspace}}"
    echo "    command:  ${run_command[*]}"
    echo "    env file: ${env_note}"
    echo "    cache:    $([ "${use_cache}" -eq 1 ] && echo shared || echo 'isolated (--no-cache-vol)')"
    echo "    audit:    $([ "${skip_audit}" -eq 0 ] && echo enabled || echo 'SKIPPED (--skip-audit)')"
    echo "============================================"

    local started_at rc
    started_at="$(date -Is)"
    RUN_COMMAND=("${run_command[@]}")
    RUN_COPIED=()
    SECONDS=0

    # Ctrl-C / kill: remove the container, then exit with the signal convention.
    # (Single-quoted body: ${ct} expands at signal time, inside cmd_run scope.)
    trap 'podman rm -f "${ct}" >/dev/null 2>&1 || true; exit 130' INT
    trap 'podman rm -f "${ct}" >/dev/null 2>&1 || true; exit 143' TERM

    # Attached run: output streams live AND is captured to console.log.
    # PIPESTATUS[0] is the container's exit code even under pipefail.
    set +e
    timeout -k 30s "${timeout_s}s" podman run "${run_args[@]}" \
        "${image}" \
        bash -lc 'source /usr/local/bin/ci-setup; exec "$@"' ci "${run_command[@]}" \
        2>&1 | tee "${art_dir}/console.log"
    rc=${PIPESTATUS[0]}
    set -e
    trap - INT TERM

    # --- collect well-known artifacts -------------------------------------------------
    local -a copied=()
    if [ -n "${copy_root}" ]; then
        local -a default_arts=(playwright-report test-results coverage dist build junit.xml)
        shopt -s nullglob
        local p f
        for p in "${default_arts[@]}" "${extra_arts[@]}"; do
            # copy_root is quoted (paths with spaces stay whole); ${p} is left
            # unquoted on purpose so --artifact-path may use shell globs.
            for f in "${copy_root}"/${p}; do
                if [ -e "$f" ]; then
                    cp -r "$f" "${art_dir}/" && copied+=("$(basename "$f")")
                fi
            done
        done
        shopt -u nullglob
    fi
    if [ ${#copied[@]} -gt 0 ]; then ok "artifacts copied: ${copied[*]}"; fi
    RUN_COPIED=("${copied[@]}")
    RUN_SECONDS=${SECONDS}

    write_summary "${rc}" "${run_id}" "${image}" "${repo}" "${src_dir}" \
        "${started_at}" "${art_dir}" "${use_cache}" "${read_only}" "${skip_audit}"
    finish_run "${rc}" "${ct}" "${run_dir}" "${src_dir}" "${keep}" "${art_dir}"
}

# write_summary <rc> <run_id> <image> <repo> <src> <started_at> <art_dir>
#               <use_cache> <read_only> <skip_audit>
# Reads RUN_COMMAND / RUN_COPIED / RUN_SECONDS set by cmd_run.
write_summary() {
    local rc="$1" run_id="$2" image="$3" repo="$4" src="$5"
    local started_at="$6" art_dir="$7" use_cache="$8" read_only="$9" skip_audit="${10}"

    local audit="skipped"
    if [ "${skip_audit}" -eq 0 ]; then
        if [ "${rc}" -eq 66 ]; then
            audit="fail"
        elif [ -f "${art_dir}/isolation-audit.json" ]; then
            if jq -e '.pass == true' "${art_dir}/isolation-audit.json" >/dev/null 2>&1; then
                audit="pass"
            else
                audit="fail"
            fi
        else
            audit="not-run"
        fi
    fi

    local source_type="empty" source_value=""
    if [ -n "${repo}" ]; then source_type="repo"; source_value="${repo}"
    elif [ -n "${src}" ]; then source_type="src"; source_value="${src}"; fi

    jq -n \
        --arg run_id "${run_id}" \
        --arg image "${image}" \
        --arg source_type "${source_type}" \
        --arg source_value "${source_value}" \
        --argjson command "$(json_array "${RUN_COMMAND[@]}")" \
        --arg started_at "${started_at}" \
        --arg finished_at "$(date -Is)" \
        --argjson duration_s "${RUN_SECONDS}" \
        --argjson exit_code "${rc}" \
        --arg exit_reason "$(reason_for "${rc}")" \
        --arg isolation_audit "${audit}" \
        --arg cache "$([ "${use_cache}" -eq 1 ] && echo shared || echo isolated)" \
        --argjson read_only_rootfs "${read_only}" \
        --arg artifacts_dir "${art_dir}" \
        --argjson copied "$(json_array "${RUN_COPIED[@]}")" \
        '{schema: "agent-sandbox.ci-run/1",
          run_id: $run_id, image: $image,
          source: {type: $source_type, value: $source_value},
          command: $command,
          started_at: $started_at, finished_at: $finished_at, duration_s: $duration_s,
          exit_code: $exit_code, exit_reason: $exit_reason,
          isolation_audit: $isolation_audit, cache: $cache,
          read_only_rootfs: $read_only_rootfs,
          artifacts_dir: $artifacts_dir, copied_artifacts: $copied}' \
        > "${art_dir}/run-summary.json"
}

# finish_run <rc> <ct> <run_dir> <src_dir> <keep> <art_dir>
finish_run() {
    local rc="$1" ct="$2" run_dir="$3" src_dir="$4" keep="$5" art_dir="$6"
    echo
    echo "============================================"
    echo "  run finished: exit=${rc} ($(reason_for "${rc}")) after ${RUN_SECONDS}s"
    echo "  artifacts:    ${art_dir}"
    echo "============================================"
    if [ "${rc}" -ne 0 ] && [ "${keep}" -eq 1 ]; then
        echo -e "  ${YELLOW}○${NC} kept for debugging (--keep-on-failure):"
        echo "        podman logs ${ct}"
        echo "        podman start ${ct} && podman exec -it ${ct} bash"
        echo "        rm when done: podman rm -f ${ct}; rm -rf ${run_dir}"
        return
    fi
    podman rm -f "${ct}" >/dev/null 2>&1 || true
    [ -n "${src_dir}" ] || rm -rf "${run_dir:?}"
    if [ "${rc}" -eq 0 ]; then
        ok "ephemeral workspace destroyed (code dir removed, artifacts kept)"
    else
        ok "ephemeral workspace destroyed (use --keep-on-failure to debug failures)"
    fi
}

# ============================================================================
# list / reap / cache
# ============================================================================
cmd_list() {
    local f n=0
    printf "  %-22s %-19s %-5s %-15s %s\n" "RUN" "STARTED" "EXIT" "REASON" "COMMAND"
    for f in "${CI_ROOT}/artifacts"/*/run-summary.json; do
        [ -e "$f" ] || continue
        n=$((n+1))
        jq -r '[.run_id, (.started_at | split("T")[0] + " " + split("T")[1][:8]),
                (.exit_code|tostring), .exit_reason, (.command|join(" "))] | @tsv' "$f" \
            | awk -F'\t' '{printf "  %-22s %-19s %-5s %-15s %s\n", $1, $2, $3, $4, $5}'
    done
    [ "$n" -eq 0 ] && info "no runs recorded yet (artifacts live under ${CI_ROOT}/artifacts/)"
    return 0
}

cmd_reap() {
    local ttl=24 purge_arts=0
    while [ $# -gt 0 ]; do
        case "$1" in
            --ttl-hours)       shift; ttl="${1:?--ttl-hours needs a value}" ;;
            --purge-artifacts) purge_arts=1 ;;
            *) die "unknown option: $1" ;;
        esac
        shift
    done
    # Stopped CI containers — never running ones, never workspaces: the
    # agent-__ci- prefix is unreachable for 40-workspace.sh names.
    local c state removed=0
    while IFS= read -r c; do
        [ -n "$c" ] || continue
        state="$(podman inspect -f '{{.State.Status}}' "$c" 2>/dev/null || echo gone)"
        if [ "${state}" != "running" ]; then
            podman rm -f "$c" >/dev/null 2>&1 || true
            removed=$((removed+1))
        fi
    done < <(podman ps -a --format '{{.Names}}' 2>/dev/null | grep '^agent-__ci-' || true)
    [ "${removed}" -gt 0 ] && ok "removed ${removed} stopped CI container(s)"

    # Stale run dirs (code + read-only-mode homes). Artifacts are NEVER touched
    # unless --purge-artifacts: they are the product of the runs.
    local stale
    if [ -d "${CI_ROOT}/runs" ]; then
        stale="$(find "${CI_ROOT}/runs" -mindepth 1 -maxdepth 1 -type d -mmin "+$((ttl * 60))" | wc -l)"
        if [ "${stale}" -gt 0 ]; then
            find "${CI_ROOT}/runs" -mindepth 1 -maxdepth 1 -type d -mmin "+$((ttl * 60))" -exec rm -rf {} +
            ok "removed ${stale} run dir(s) older than ${ttl}h"
        fi
    fi
    if [ "${purge_arts}" -eq 1 ] && [ -d "${CI_ROOT}/artifacts" ]; then
        stale="$(find "${CI_ROOT}/artifacts" -mindepth 1 -maxdepth 1 -type d -mmin "+$((ttl * 60))" | wc -l)"
        if [ "${stale}" -gt 0 ]; then
            find "${CI_ROOT}/artifacts" -mindepth 1 -maxdepth 1 -type d -mmin "+$((ttl * 60))" -exec rm -rf {} +
            ok "removed ${stale} artifact dir(s) older than ${ttl}h"
        fi
    fi
}

cmd_cache() {
    [ -d "${CI_ROOT}/cache" ] || { info "no shared cache yet (created on first run)"; exit 0; }
    du -sh "${CI_ROOT}/cache" 2>/dev/null || true
    rm -rf "${CI_ROOT:?}/cache"
    mkdir -p "${CI_ROOT}/cache"/{npm,pip,uv,bun,pnpm-store}
    ok "shared package caches wiped (next run starts cold)"
}

# ============================================================================
main() {
    [ $# -ge 1 ] || { usage; exit 2; }
    local cmd="$1"; shift
    case "${cmd}" in
        run)   cmd_run "$@" ;;
        list)  cmd_list ;;
        reap)  cmd_reap "$@" ;;
        cache) cmd_cache ;;
        *)     usage; exit 2 ;;
    esac
}
main "$@"
