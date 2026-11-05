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
    "${SCRIPT_DIR}/40-workspace.sh" create "${CANARY}" --memory 2g --cpus 2 >/dev/null \
        || { echo -e "${RED}canary creation FAILED — the workspace toolpath itself is broken${NC}"; exit 1; }
fi

# --- 1. Isolation guarantees (negative checks are the point) ------------------
section "Isolation guarantees"

# Direct egress (proxy vars stripped) must FAIL: agent-internal has no route.
if OUT="$(ws env -u http_proxy -u https_proxy -u HTTP_PROXY -u HTTPS_PROXY curl -sS --max-time 8 -o /dev/null https://registry.npmjs.org)"; then
    fail "direct egress must be BLOCKED" "curl succeeded without proxy: ${OUT}"
else
    pass "direct egress blocked (no route from agent-internal)" "${OUT}"
fi

# External DNS must FAIL: aardvark-dns on internal networks resolves container
# names only; everything else is NXDOMAIN.
if ws getent hosts registry.npmjs.org >/dev/null; then
    fail "external DNS must be blocked" "getent resolved an external name"
else
    pass "external DNS blocked (NXDOMAIN outside the network)"
fi

# Non-allowlisted domain through the proxy must return Squid's 403.
CODE="$(ws curl -sS --max-time 15 -o /dev/null -w '%{http_code}' https://en.wikipedia.org)"
if [ "${CODE}" = "403" ]; then
    pass "non-allowlisted domain denied by proxy" "HTTP ${CODE} (Squid ACL deny)"
else
    fail "non-allowlisted domain must get 403" "got HTTP ${CODE}"
fi

# Allowlisted domain through the proxy must work.
CODE="$(ws curl -sS --max-time 20 -o /dev/null -w '%{http_code}' https://registry.npmjs.org)"
if [ "${CODE}" = "200" ]; then
    pass "allowlisted domain reachable via proxy" "registry.npmjs.org -> HTTP ${CODE}"
else
    fail "allowlisted domain must work through proxy" "got HTTP ${CODE} (gateway up? 30-gateway.sh status)"
fi

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

v() { ws "$1" "${2:---version}" | sed -n 1p; }

OUT="$(v python3.13)"
[[ "${OUT}" == *"3.13"* ]] && pass "Python 3.13" "${OUT}" || fail "Python 3.13 missing" "${OUT}"

OUT="$(v node)"
NODE_MAJ="$(echo "${OUT}" | sed -E 's/^v([0-9]+)\..*/\1/')"
[ "${NODE_MAJ}" -ge 20 ] 2>/dev/null && pass "Node.js (>=20, expect 24)" "${OUT}" || fail "Node.js >=20 missing" "${OUT}"

for tool in bun pnpm uv git chromium jq rg; do
    OUT="$(v "${tool}")"
    [ -n "${OUT}" ] && pass "${tool}" "${OUT}" || fail "${tool} not working" "empty version output"
done

OUT="$(ws playwright --version)"
[[ "${OUT}" == *1.* ]] && pass "Playwright (Node)" "${OUT}" || fail "Playwright (Node) missing" "${OUT}"

OUT="$(ws /opt/py-tools/bin/python -c 'import playwright; print(playwright.__file__)')"
[ -n "${OUT}" ] && pass "Playwright (Python)" "${OUT}" || fail "Playwright (Python) missing" "${OUT}"

for tool in agent-browser claude codex opencode; do
    OUT="$(v "${tool}")"
    [ -n "${OUT}" ] && pass "${tool}" "${OUT}" || fail "${tool} not working" "empty version output"
done

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
    "${SCRIPT_DIR}/40-workspace.sh" destroy "${CANARY}" --purge-home --purge-workspace >/dev/null
    echo "  Canary cleaned up."
fi
[ "${WARN}" -gt 0 ] && echo "  Review the warnings above — they are documented limitations, not breakage."
exit 0
