#!/usr/bin/env bash
# ============================================================================
# ci-setup — in-container preamble for every ephemeral CI run.
# ============================================================================
# Bind-mounted READ-ONLY into the run container by scripts/45-ci-run.sh:
#   files/ci-setup.sh -> /usr/local/bin/ci-setup
# It is deliberately NOT baked into the image — the image stays byte-identical
# for interactive and CI consumption (BLUEPRINT.md §4 D6, §12).
#
# Order of operations (each step fails the run before untrusted code runs):
#   1. export CI environment + point package-manager caches at /cache
#   2. seed image-baked browsers into this run's ephemeral home
#   3. ISOLATION SELF-AUDIT (direct egress / external DNS / proxy 403 + 200
#      / resource-cap evidence) -> writes /artifacts/isolation-audit.json,
#      exits 66 on any failure
#   4. optional shallow clone of $CI_REPO_URL (cwd becomes the repo)
#   5. exec the user command (the runner invokes:
#        bash -lc 'source /usr/local/bin/ci-setup; exec "$@"' ci <cmd...>)
#
# Cache facts (verified):
#   * bun honors BUN_INSTALL_CACHE_DIR          (present in bun 1.3 binary)
#   * pnpm reads storeDir from the global config file
#     ~/.config/pnpm/config.yaml                (documented at pnpm.io/settings)
#   * pnpm defaults frozenLockfile=true in CI   (documented default when CI=true)
# ============================================================================
set -euo pipefail

: "${CI_RUN_ID:=unknown}"
export CI_RUN_ID
export CI=true
export AGENT_SANDBOX_PROFILE=ci
export DEBIAN_FRONTEND=noninteractive
export npm_config_fund=false          # npm: no funding noise in CI logs
export CI_ARTIFACTS_DIR=/artifacts
export PLAYWRIGHT_BROWSERS_PATH=/home/dev/.cache/ms-playwright
# Node >= 24 built-in fetch ignores proxy env vars unless this is set
# (verified: NODE_USE_ENV_PROXY shipped in Node 24.0.0) — audit L-3.
export NODE_USE_ENV_PROXY=1

# URL display helper: strip userinfo before anything reaches a log or an
# artifact (audit M-9: https://token@host/... used to be echoed verbatim into
# console.log). The full URL is still used for the clone itself.
redact_url() {
    printf '%s' "$1" | sed -E 's#(://)[^/@:?]+:[^/@]+@#\1[REDACTED]@#g; s#(://)[^/@:?]+@#\1[REDACTED]@#g'
}

# --- 1. Shared package caches (bind-mounted host dir, not a named volume) ----
# /cache is the shared cache tree under ~/agent-workspaces/__ci/cache on the
# host. It is shared writable state across runs: same host, same user, same
# trust domain — pnpm's own documentation makes exactly this point about its
# store. For untrusted sources run 45-ci-run.sh with --no-cache-vol.
if [ -d /cache ] && [ -w /cache ]; then
    export npm_config_cache=/cache/npm
    export PIP_CACHE_DIR=/cache/pip
    export UV_CACHE_DIR=/cache/uv
    export BUN_INSTALL_CACHE_DIR=/cache/bun
    mkdir -p /cache/npm /cache/pip /cache/uv /cache/bun /cache/pnpm-store
    # pnpm: point the content-addressable store at the shared tree via the
    # documented global config file (version-stable; the npm_config_store_dir
    # env spelling changed across pnpm major versions, the config file did not).
    mkdir -p "${HOME}/.config/pnpm"
    printf 'storeDir: /cache/pnpm-store\n' > "${HOME}/.config/pnpm/config.yaml"
else
    echo "[ci] shared cache not mounted/writable — falling back to ephemeral caches (slower, isolated)"
fi

# --- 2. Browsers: link image-baked builds into this run's ephemeral home -----
seed-playwright-browsers

# --- 3. Isolation self-audit (evidence per run, before any workload code) ----
# Mirrors the four mechanisms of 50-verify.sh: no route (direct egress must
# fail), NXDOMAIN (external DNS must fail), proxy 403 for non-allowlisted,
# proxy 200 for allowlisted. Targets: example.com is an allowlisted
# verification domain; example.net is deliberately NOT allowlisted.
if [ "${CI_SKIP_AUDIT:-0}" != "1" ]; then
    audit_json="${CI_ARTIFACTS_DIR}/isolation-audit.json"
    audit_fail=0

    a_uid="$(id -u)"
    [ "${a_uid}" = "1000" ] || audit_fail=1

    a_caps="$(awk '/^CapEff/ {print $2}' /proc/self/status)"
    [ "${a_caps}" = "0000000000000000" ] || audit_fail=1

    a_nnp="$(awk '/^NoNewPrivs/ {print $2}' /proc/self/status)"
    [ "${a_nnp}" = "1" ] || audit_fail=1

    # Resource caps are recorded as per-run EVIDENCE (third pass, R-6):
    # 45-ci-run.sh caps every run (--pids-limit 1024, --memory …), but cgroup
    # delegation for rootless podman varies by host — 50-verify.sh treats a
    # missing delegation as a SOFT condition (references/troubleshooting.md
    # §5), so the audit RECORDS the readings instead of failing on them: a
    # `max` value is reported in the json for the operator to judge, while
    # the fail-closed checks above keep proving the isolation guarantees.
    a_pids="$(cat /sys/fs/cgroup/pids.max 2>/dev/null || echo max)"
    a_mem="$(cat /sys/fs/cgroup/memory.max 2>/dev/null || echo max)"

    # Direct egress (proxy vars stripped) must FAIL at the network layer —
    # tested with an IP literal so DNS cannot mask the result, and classified
    # by curl's exit code: only 7 (unreachable) / 28 (timeout) count as
    # "blocked"; anything else is an inconclusive result and FAILS the audit
    # (audit C-1/H-1: the old name-based check counted any error as blocked).
    D_RC=0
    env -u http_proxy -u https_proxy -u HTTP_PROXY -u HTTPS_PROXY \
        curl -sS --connect-timeout 4 --max-time 5 -o /dev/null http://1.1.1.1/ 2>/dev/null || D_RC=$?
    case "${D_RC}" in
        7|28) a_direct="blocked" ;;
        0)    a_direct="open"; audit_fail=1 ;;
        *)    a_direct="error(exit ${D_RC})"; audit_fail=1 ;;
    esac

    # External DNS must FAIL — aardvark answers container names only.
    if getent hosts example.com >/dev/null 2>&1; then
        a_dns="resolves"; audit_fail=1
    else
        a_dns="blocked"
    fi

    # Non-allowlisted domain through the proxy must be denied at CONNECT.
    # The verdict is %{http_connect} (audit C-1: %{http_code} reads 000 on a
    # denied CONNECT; the old `|| echo 000` fallback made the value "000000"
    # and the check unpassable). If curl cannot even reach the proxy, the
    # value stays 000 and the audit correctly fails.
    # `|| :` (second pass, C-1): this script runs under `set -euo pipefail` —
    # an UNGUARDED assignment of a failing command substitution would abort
    # ci-setup with curl's exit code (e.g. 7) BEFORE the audit json is
    # written, turning an audit failure (66, with evidence) into an
    # unlabeled "command-failed" run with no evidence. The guard keeps
    # control flow alive; the fallback below records the failure.
    a_deny="$(curl -sS --max-time 10 -o /dev/null -w '%{http_connect}' https://example.net 2>/dev/null)" || :
    a_deny="${a_deny:-000}"
    [ "${a_deny}" = "403" ] || audit_fail=1

    # Allowlisted domain through the proxy must work (also proves gateway up).
    a_allow="$(curl -sS --max-time 10 -o /dev/null -w '%{http_code}' https://example.com 2>/dev/null)" || :
    a_allow="${a_allow:-000}"
    [ "${a_allow}" = "200" ] || audit_fail=1

    jq -n \
        --arg run_id "${CI_RUN_ID}" \
        --arg uid "${a_uid}" \
        --arg caps_eff "${a_caps}" \
        --arg no_new_privs "${a_nnp}" \
        --arg direct_egress "${a_direct}" \
        --arg external_dns "${a_dns}" \
        --arg proxy_deny_status "${a_deny}" \
        --arg proxy_allow_status "${a_allow}" \
        --arg pids_max "${a_pids}" \
        --arg memory_max "${a_mem}" \
        --argjson pass "$(( 1 - audit_fail ))" \
        '{schema: "agent-sandbox.isolation-audit/1",
          run_id: $run_id,
          uid: $uid, caps_eff: $caps_eff, no_new_privs: $no_new_privs,
          direct_egress: $direct_egress, external_dns: $external_dns,
          proxy_deny_status: $proxy_deny_status, proxy_allow_status: $proxy_allow_status,
          pids_max: $pids_max, memory_max: $memory_max,
          pass: ($pass == 1)}' > "${audit_json}"

    echo "[ci-audit] uid=${a_uid} caps=${a_caps} no-new-privs=${a_nnp} direct-egress=${a_direct} external-dns=${a_dns} proxy(allow=${a_allow} deny=${a_deny}) pids-max=${a_pids} memory-max=${a_mem}"
    if [ "${audit_fail}" -ne 0 ]; then
        echo "[ci-audit] FAILED — sandbox guarantees did NOT hold; command not run. See ${audit_json}" >&2
        exit 66
    fi
    echo "[ci-audit] pass — guarantees proven for run ${CI_RUN_ID}"
fi

# --- 4. Optional repo checkout (through the allowlist proxy) ------------------
if [ -n "${CI_REPO_URL:-}" ]; then
    repo_dir="/workspace/$(basename "${CI_REPO_URL%.git}")"
    echo "[ci] shallow-cloning $(redact_url "${CI_REPO_URL}") via allowlist proxy…"
    git clone --depth 1 -- "${CI_REPO_URL}" "${repo_dir}"
    cd "${repo_dir}"
fi

# --- 5. exec the user command (performed by the calling bash -lc) -------------
