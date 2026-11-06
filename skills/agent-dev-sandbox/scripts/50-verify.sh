#!/usr/bin/env bash
# ============================================================================
# 50-verify.sh — end-to-end verification suite (evidence, not vibes)
# ============================================================================
# Creates a disposable canary workspace through the REAL toolpath
# (40-workspace.sh create __verify) and runs positive AND negative checks.
# Negative checks (must-fail) prove the isolation guarantees:
#   * direct egress (no proxy env)   -> no route to the internet
#   * external DNS                   -> NXDOMAIN (aardvark answers names only)
#   * non-allowlisted domain via proxy -> HTTP 403 from Squid
#
# Exit code 0 only if every HARD check passes. SOFT checks warn but do not
# fail the suite (documented limitations, not broken guarantees).
#
# Usage: scripts/50-verify.sh [--keep]     (keep = leave canary for inspection)
# ============================================================================
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CANARY="__verify"
CT="agent-${CANARY}"
KEEP=0
[ "${1:-}" = "--keep" ] && KEEP=1

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
PASS=0; FAIL=0; WARN=0

# -i is REQUIRED: checks that pipe scripts via stdin (the Playwright heredoc)
# would silently run nothing without it.
ws() { podman exec -i "${CT}" "$@" 2>&1; }

pass() { PASS=$((PASS+1)); echo -e "  ${GREEN}PASS${NC}  $1"; [ -n "${2:-}" ] && echo "        evidence: ${2}"; }
fail() { FAIL=$((FAIL+1)); echo -e "  ${RED}FAIL${NC}  $1"; [ -n "${2:-}" ] && echo "        evidence: ${2}"; }
soft_warn() { WARN=$((WARN+1)); echo -e "  ${YELLOW}WARN${NC}  $1"; [ -n "${2:-}" ] && echo "        ${2}"; }

section() { echo; echo "--- $1 ---"; }

echo "============================================"
echo "  agent-dev-sandbox — Verification Suite"
echo "============================================"

# --- Canary workspace through the real toolpath ------------------------------
if podman container exists "${CT}" 2>/dev/null; then
    echo "  canary ${CT} already exists — reusing (stale? run: 40-workspace.sh destroy ${CANARY} --purge-home --purge-workspace)"
else
    echo "  creating canary workspace via 40-workspace.sh …"
    ALLOW_RESERVED_NAME=1 "${SCRIPT_DIR}/40-workspace.sh" create "${CANARY}" --memory 2g --cpus 2 >/dev/null \
        || { echo -e "${RED}canary creation FAILED — the workspace toolpath itself is broken${NC}"; exit 1; }
fi

# --- 1. Isolation guarantees (negative checks are the point) ------------------
section "Isolation guarantees"

# Mechanism 1 — no route. Direct egress (proxy vars stripped) to an IP
# LITERAL must fail at the network layer. An IP target removes DNS from the
# equation (audit H-1: the old name-based check could pass purely on a DNS
# failure without ever exercising the no-route guarantee). curl exit 7 =
# network unreachable, 28 = timeout — both prove the packet had nowhere to go.
CODE_DIRECT=0
ws env -u http_proxy -u https_proxy -u HTTP_PROXY -u HTTPS_PROXY \
    curl -sS --connect-timeout 5 --max-time 8 -o /dev/null http://1.1.1.1/ >/dev/null 2>&1 || CODE_DIRECT=$?
case "${CODE_DIRECT}" in
    7|28) pass "direct egress blocked (no route from agent-internal)" "curl exit ${CODE_DIRECT} to IP literal 1.1.1.1" ;;
    0)    fail "direct egress must be BLOCKED" "curl to 1.1.1.1 SUCCEEDED (exit 0)" ;;
    *)    fail "direct egress must be BLOCKED" "curl exit ${CODE_DIRECT} to 1.1.1.1 (expected 7 or 28 — investigate)" ;;
esac

# Mechanism 2 — no external DNS: aardvark-dns on internal networks resolves
# container names only; everything else is NXDOMAIN.
if ws getent hosts registry.npmjs.org >/dev/null 2>&1; then
    fail "external DNS must be blocked" "getent resolved an external name"
else
    pass "external DNS blocked (NXDOMAIN outside the network)" "getent hosts registry.npmjs.org -> no result"
fi

# Mechanism 3 — the proxy ACL. For CONNECT (HTTPS) the proxy's verdict is in
# %{http_connect}; %{http_code} stays 000 when the tunnel is denied (audit
# C-1: asserting on %{http_code} alone could never observe the 403).
CODES="$(ws curl -sS --max-time 15 -o /dev/null -w '%{http_connect} %{http_code}' https://en.wikipedia.org)"
DENY="$(echo "${CODES}" | awk '{print $1}')"
if [ "${DENY}" = "403" ]; then
    pass "non-allowlisted domain denied by proxy" "Squid CONNECT verdict: 403 (${CODES})"
else
    fail "non-allowlisted domain must get 403" "CONNECT verdict: ${CODES} (expected 403)"
fi

# Allowlisted domain through the proxy must work end-to-end: tunnel AND
# response both 200.
CODES="$(ws curl -sS --max-time 20 -o /dev/null -w '%{http_connect} %{http_code}' https://registry.npmjs.org)"
CONN="$(echo "${CODES}" | awk '{print $1}')"; HTTP="$(echo "${CODES}" | awk '{print $2}')"
if [ "${CONN}" = "200" ] && [ "${HTTP}" = "200" ]; then
    pass "allowlisted domain reachable via proxy" "registry.npmjs.org -> CONNECT ${CONN}, HTTP ${HTTP}"
else
    fail "allowlisted domain must work through the proxy" "CONNECT ${CONN}, HTTP ${HTTP} (gateway up? 30-gateway.sh status)"
fi

# Mechanism 4 — IP forwarding disabled on the internal bridge — lives in the
# netavark configuration and is not separately observable from inside a
# workspace; its failure mode collapses into mechanism 1 (a route would
# exist). Not asserted independently, by design.

# --- 2. Container hardening ----------------------------------------------------
section "Container hardening"

OUT="$(ws sh -c 'id -u')"
[ "${OUT}" = "1000" ] && pass "runs as non-root user (uid 1000)" "id -u -> ${OUT}" \
                     || fail "must run as uid 1000" "id -u -> ${OUT}"

OUT="$(ws sh -c 'grep NoNewPrivs /proc/self/status | awk "{print \$2}"')"
[ "${OUT}" = "1" ] && pass "no-new-privileges active" "NoNewPrivs: ${OUT}" \
                  || fail "no-new-privileges must be set" "NoNewPrivs: ${OUT}"

OUT="$(ws sh -c 'grep CapEff /proc/self/status | awk "{print \$2}"')"
[ "${OUT}" = "0000000000000000" ] && pass "all Linux capabilities dropped" "CapEff: ${OUT}" \
                                 || fail "capabilities must be empty" "CapEff: ${OUT}"

OUT="$(ws sh -c 'cat /sys/fs/cgroup/pids.max 2>/dev/null || echo max')"
if [[ "${OUT}" =~ ^[0-9]+$ ]] && [ "${OUT}" -le 1024 ]; then
    pass "pids limit enforced" "pids.max = ${OUT}"
elif [ "${OUT}" = "max" ]; then
    soft_warn "pids/memory limits NOT enforced (cgroup delegation missing)" "pids.max = max — see references/troubleshooting.md §5"
else
    pass "pids limit present" "pids.max = ${OUT}"
fi

# --- 3. Toolchain ---------------------------------------------------------------
section "Toolchain (versions from the image)"

# Tool checks assert BOTH the exit status AND a version pattern on the first
# output line (audit H-1: the old `[ -n "$OUT" ]` passed on any error text —
# a missing tool's error message counted as a PASS).
tool_check() { # <tool> <ERE matched against the first --version line>
    local tool="$1" pat="$2" out rc=0 first
    out="$(ws "${tool}" --version 2>&1)" || rc=$?
    first="$(echo "${out}" | sed -n 1p)"
    if [ "${rc}" -eq 0 ] && echo "${first}" | grep -Eq "${pat}"; then
        pass "${tool}" "${first}"
    else
        fail "${tool} not working (exit ${rc})" "${first:-<no output>}"
    fi
}

tool_check python3.13 'Python 3\.13'

OUT_RC=0; OUT="$(ws node --version 2>&1)" || OUT_RC=$?
NODE_MAJ="$(echo "${OUT}" | sed -E 's/^v([0-9]+)\..*/\1/')"
if [ "${OUT_RC}" -eq 0 ] && [ "${NODE_MAJ}" -ge 20 ] 2>/dev/null; then
    pass "Node.js (>=20, expect 24)" "${OUT}"
else
    fail "Node.js >=20 missing" "exit ${OUT_RC}: ${OUT}"
fi

tool_check bun       '[0-9]+\.[0-9]+\.[0-9]+'
tool_check pnpm      '[0-9]+\.[0-9]+'
tool_check uv        'uv [0-9]'
tool_check git       'git version [0-9]'
tool_check chromium  '[0-9]+\.[0-9]+'
tool_check jq        'jq-'
tool_check rg        'ripgrep'

OUT_RC=0; OUT="$(ws playwright --version 2>&1)" || OUT_RC=$?
if [ "${OUT_RC}" -eq 0 ] && [[ "${OUT}" == *1.* ]]; then
    pass "Playwright (Node)" "${OUT}"
else
    fail "Playwright (Node) missing" "exit ${OUT_RC}: ${OUT}"
fi

OUT_RC=0; OUT="$(ws /opt/py-tools/bin/python -c 'import playwright; print(playwright.__file__)' 2>&1)" || OUT_RC=$?
if [ "${OUT_RC}" -eq 0 ] && [ -n "${OUT}" ]; then
    pass "Playwright (Python)" "${OUT}"
else
    fail "Playwright (Python) missing" "exit ${OUT_RC}: ${OUT}"
fi

tool_check agent-browser '[0-9]+\.[0-9]+'
tool_check claude        '[0-9]+(\.[0-9]+)+'
tool_check codex         '[0-9]+(\.[0-9]+)+'
tool_check opencode      '[0-9]+(\.[0-9]+)+'

# --- 4. Browser paths -------------------------------------------------------------
section "Browsers"

if ws /opt/py-tools/bin/python - <<'PY' >/dev/null 2>&1
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_page()
    page.goto("data:text/html,<title>pw-ok</title><h1>hello</h1>")
    assert page.title() == "pw-ok"
    b.close()
print("ok")
PY
then
    pass "Playwright Chromium launches + renders (image-baked build)"
else
    fail "Playwright Chromium smoke test" "launch or render failed — run with output visible to diagnose"
fi

OUT="$(ws bash -lc '
    set -e
    cd /tmp
    printf "<html><head><title>local-ok</title></head><body>hi</body></html>" > v.html
    python3.13 -m http.server 8123 >/dev/null 2>&1 &
    SRV=$!
    sleep 1
    agent-browser open http://localhost:8123/v.html >/dev/null
    T="$(agent-browser get title)"
    agent-browser close >/dev/null
    kill $SRV 2>/dev/null || true
    echo "$T"
')"
if [ "${OUT}" = "local-ok" ]; then
    pass "agent-browser drives a local dev server (the agent UI-testing path)" "title -> local-ok"
else
    fail "agent-browser local-server test" "got title '${OUT}'"
fi

# SOFT: browsing an EXTERNAL page through the proxy depends on Chromium honoring
# http_proxy env vars — treat as informational, not a guarantee.
OUT="$(ws bash -lc 'agent-browser open https://example.com >/dev/null 2>&1 && agent-browser get title 2>/dev/null; agent-browser close >/dev/null 2>&1' | sed -n 1p)"
if [ "${OUT}" = "Example Domain" ]; then
    pass "agent-browser reaches allowlisted external page via proxy env" "title -> ${OUT}"
else
    soft_warn "agent-browser external browsing not proxied by env alone" \
        "for projects needing external pages, pass proxy to Playwright: { proxy: { server: 'http://agent-gateway:3128' } } (local-first flows are unaffected)"
fi

# --- 5. Representative workload onboarding -----------------------------------------
section "Representative workload (nordeim/budget-wiser)"

if ws bash -c 'rm -rf /tmp/bw-check && git clone --depth 1 https://github.com/nordeim/budget-wiser.git /tmp/bw-check >/dev/null 2>&1 && test -f /tmp/bw-check/package.json && grep -q next /tmp/bw-check/package.json'; then
    pass "git clone budget-wiser via allowlist proxy" "repo + package.json verified"
else
    fail "budget-wiser clone" "github.com must be allowlisted and reachable via proxy"
fi

# --- Summary ------------------------------------------------------------------------
echo
echo "============================================"
echo -e "  ${GREEN}${PASS} passed${NC}  ${RED}${FAIL} failed${NC}  ${YELLOW}${WARN} warnings${NC}"
echo "============================================"

if [ "${FAIL}" -gt 0 ]; then
    echo "  Evidence above is the failure ledger. Do NOT proceed to 'done'."
    echo "  Debug: scripts/40-workspace.sh shell ${CANARY}   (canary kept)"
    echo "  Docs:  references/troubleshooting.md (§ numbers appear in messages)"
    exit 1
fi

if [ "${KEEP}" -eq 1 ]; then
    echo "  Canary kept for inspection: scripts/40-workspace.sh shell ${CANARY}"
else
    ALLOW_RESERVED_NAME=1 "${SCRIPT_DIR}/40-workspace.sh" destroy "${CANARY}" --purge-home --purge-workspace >/dev/null
    echo "  Canary cleaned up."
fi
[ "${WARN}" -gt 0 ] && echo "  Review the warnings above — they are documented limitations, not breakage."
exit 0
