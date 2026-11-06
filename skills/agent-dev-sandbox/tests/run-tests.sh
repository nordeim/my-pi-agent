#!/usr/bin/env bash
# ============================================================================
# tests/run-tests.sh — container-free test suite for the bundle's scripts
# ============================================================================
# No podman, systemd, Squid or KVM required. Covers (audit M-11):
#   1. validate_name          (C-1 regression: reserved names)
#   2. validate_resources     (M-4 regression: injection via --memory)
#   3. read_meta              (M-4 regression: hostile meta file never sourced)
#   4. validate_domain        (H-4 regression: '*.' rejected, '.' accepted)
#   5. redact_url             (M-9 regression: userinfo stripped)
#   6. reason_for             (exit-code contract)
#   7. deny-CONNECT probe     (C-1 regression: 403 observed via %{http_connect})
#   8. artifact containment   (M-9 regression: cp -rP never follows symlinks)
#   9. doc-lint               (L-1/L-4: stale markers, edition drift, pins)
# Run after ANY edit to scripts/ or the docs. Exit 0 = all green.
# ============================================================================
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PASS=0; FAIL=0; SKIP=0

ok()   { PASS=$((PASS+1)); echo "  PASS  $1"; }
bad()  { FAIL=$((FAIL+1)); echo "  FAIL  $1${2:+ — $2}"; }
skip() { SKIP=$((SKIP+1)); echo "  SKIP  $1"; }

# Run a function from a bundle script in a clean subshell (the scripts have
# source-guards, so sourcing defines functions without running the CLI).
invoke() { # <script> <ALLOW_RESERVED> <setup-cmd> -- <func> <args...>
    local script="$1" allow="$2" setup="$3"; shift 4
    ( export ALLOW_RESERVED_NAME="${allow}"
      # shellcheck disable=SC1090
      source "${script}" >/dev/null 2>&1
      eval "${setup}" >/dev/null 2>&1
      "$@" ) >/dev/null 2>&1
}

echo "=================================================="
echo "  agent-dev-sandbox — bundle tests (container-free)"
echo "=================================================="

WS="${ROOT}/scripts/40-workspace.sh"
GW="${ROOT}/scripts/30-gateway.sh"
CI="${ROOT}/scripts/45-ci-run.sh"

echo "--- 1. validate_name (C-1) ---"
invoke "${WS}" 0 'NAME=wiser'    -- validate_name && ok   "accepts 'wiser'" \
    || bad "'wiser' rejected"
invoke "${WS}" 0 'NAME=Bad'      -- validate_name && bad  "'Bad' accepted" \
    || ok "rejects 'Bad'"
invoke "${WS}" 0 'NAME=__ci-x'   -- validate_name && bad  "'__ci-x' accepted without the reserved flag" \
    || ok "rejects '__ci-x' without ALLOW_RESERVED_NAME"
invoke "${WS}" 1 'NAME=__verify' -- validate_name && ok   "accepts '__verify' with ALLOW_RESERVED_NAME=1 (50-verify canary)" \
    || bad "canary name still rejected — Phase 4 unreachable"
invoke "${WS}" 1 'NAME=__Bad!'   -- validate_name && bad  "malformed reserved name accepted" \
    || ok "rejects malformed reserved name '__Bad!'"

echo "--- 2. validate_resources (M-4) ---"
invoke "${WS}" 0 '' -- validate_resources 6g 4     && ok "accepts 6g / 4"    || bad "rejected 6g/4"
invoke "${WS}" 0 '' -- validate_resources 512m 1.5 && ok "accepts 512m / 1.5" || bad "rejected 512m/1.5"
invoke "${WS}" 0 '' -- validate_resources '6g; touch /tmp/TEST-INJECTED' 4 && bad "injection payload accepted" \
    || ok "rejects the M-4 injection payload"
invoke "${WS}" 0 '' -- validate_resources 6g '4; id' && bad "cpus payload accepted" || ok "rejects a cpus payload"

echo "--- 3. read_meta (M-4) ---"
T="$(mktemp -d)"
printf 'MEMORY=8g\nCPUS=2\n' > "${T}/ok.meta"
( export ALLOW_RESERVED_NAME=0
  # shellcheck disable=SC1090
  source "${WS}" >/dev/null 2>&1
  read_meta "${T}/ok.meta" && echo "${MEMORY}|${CPUS}" ) > "${T}/out" 2>/dev/null
grep -qx '8g|2' "${T}/out" && ok "round-trips valid values" || bad "round-trip" "$(cat "${T}/out" 2>/dev/null)"
printf 'MEMORY=6g; rm -rf /tmp/TEST-META-INJECTED\nCPUS=4\n' > "${T}/evil.meta"
if ( export ALLOW_RESERVED_NAME=0
     # shellcheck disable=SC1090
     source "${WS}" >/dev/null 2>&1
     read_meta "${T}/evil.meta" ) >/dev/null 2>&1; then
    [ -e /tmp/TEST-META-INJECTED ] && bad "hostile meta EXECUTED code" || ok "hostile meta parsed without execution (read, never sourced)"
else
    ok "hostile meta rejected outright by validation"
fi
printf 'EVIL=1\n' > "${T}/unknown.meta"
( export ALLOW_RESERVED_NAME=0
  # shellcheck disable=SC1090
  source "${WS}" >/dev/null 2>&1
  read_meta "${T}/unknown.meta" ) >/dev/null 2>&1 && bad "unknown meta key accepted" || ok "dies on unknown meta key"

echo "--- 4. validate_domain (H-4) ---"
for d in example.com .example.com api.github.co.uk; do
    invoke "${GW}" 0 '' -- validate_domain "${d}" && ok "accepts '${d}'" || bad "should accept '${d}'"
done
for d in '*.example.com' 'https://example.com' 'example.com/path' 'a b.com' 'example' '*.x'; do
    invoke "${GW}" 0 '' -- validate_domain "${d}" && bad "should reject '${d}'" || ok "rejects '${d}'"
done

echo "--- 5. redact_url (M-9) ---"
ru() { ( # shellcheck disable=SC1090
         source "${CI}" >/dev/null 2>&1; redact_url "$1" ); }
[ "$(ru 'https://user:pass@github.com/a/b.git')" = "https://[REDACTED]@github.com/a/b.git" ] \
    && ok "strips user:pass@" || bad "user:pass@ not stripped" "$(ru 'https://user:pass@github.com/a/b.git')"
[ "$(ru 'https://token@github.com/x.git')" = "https://[REDACTED]@github.com/x.git" ] \
    && ok "strips user@" || bad "user@ not stripped"
[ "$(ru 'https://github.com/x.git')" = "https://github.com/x.git" ] \
    && ok "leaves clean URLs untouched" || bad "clean URL modified"

echo "--- 6. reason_for (exit-code contract) ---"
rf() { ( # shellcheck disable=SC1090
         source "${CI}" >/dev/null 2>&1; reason_for "$1" ); }
[ "$(rf 0)" = "ok" ] && [ "$(rf 66)" = "audit-failure" ] && [ "$(rf 124)" = "timeout" ] \
    && [ "$(rf 127)" = "podman-error" ] && [ "$(rf 42)" = "command-failed" ] \
    && ok "mapping intact" || bad "exit-code mapping drifted"

echo "--- 7. deny-CONNECT probe semantics (C-1) ---"
if command -v python3 >/dev/null 2>&1; then
    python3 - <<'PY' &
import socket, threading
srv = socket.socket(); srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind(("127.0.0.1", 31297)); srv.listen(8)
def h(c):
    try:
        c.recv(65536); c.sendall(b"HTTP/1.1 403 Forbidden\r\nContent-Length: 0\r\n\r\n")
    finally:
        c.close()
while True:
    c, _ = srv.accept(); threading.Thread(target=h, args=(c,), daemon=True).start()
PY
    MPID=$!
    sleep 1
    # The FIXED ci-setup expression (no `|| echo` fallback, %{http_connect}):
    a_deny="$(curl -sS --max-time 5 -o /dev/null -w '%{http_connect}' \
                  --proxy http://127.0.0.1:31297 https://example.net 2>/dev/null)"
    a_deny="${a_deny:-000}"
    [ "${a_deny}" = "403" ] \
        && ok "deny probe observes 403 via %{http_connect} (old code saw 000000)" \
        || bad "deny probe got '${a_deny}'"
    kill "${MPID}" 2>/dev/null
else
    skip "python3 not available"
fi

echo "--- 8. artifact containment (M-9) ---"
T2="$(mktemp -d)"
mkdir -p "${T2}/run/dist" "${T2}/secret" "${T2}/art"
echo topsecret > "${T2}/secret/creds.txt"
ln -s "${T2}/secret" "${T2}/run/dist/exfil"
cp -rP "${T2}/run/dist" "${T2}/art/" 2>/dev/null
rm -rf "${T2}/secret"
if [ -e "${T2}/art/dist/exfil/creds.txt" ]; then
    bad "cp -rP followed the planted symlink"
else
    ok "cp -rP copies the symlink itself — no content exfil"
fi
rm -rf "${T2}" "${T}"

echo "--- 9. doc-lint (L-1 / L-4) ---"
dl() { # <file> <pattern> <should-exist:0|1> <label>
    if grep -q -- "$2" "$1" 2>/dev/null; then
        [ "$3" -eq 1 ] && ok "$4 present" || bad "$4 found in $1 (stale)"
    else
        [ "$3" -eq 1 ] && bad "$4 missing from $1" || ok "$4 absent from $1"
    fi
}
for f in "${ROOT}/BLUEPRINT.md" "${ROOT}/BLUEPRINT.html"; do
    [ -f "${f}" ] || { skip "$(basename "${f}") not built yet"; continue; }
    dl "${f}" 'Node\.js 16'      0 "stale 'Node.js 16'"
    dl "${f}" '\*\.githubusercontent' 0 "stale '*.' wildcard entry"
    dl "${f}" 'stdio:stderr'     0 "broken log sink spelling"
done
if [ -f "${ROOT}/BLUEPRINT.html" ]; then
    # Normalize HTML entities so '&' in headings compares equal to the MD.
    HTML_NORM="$(sed 's/&amp;/\&/g; s/&lt;/</g; s/&gt;/>/g' "${ROOT}/BLUEPRINT.html")"
    miss=0
    while IFS= read -r h; do
        grep -qF -- "${h}" <<<"${HTML_NORM}" || { miss=$((miss+1)); echo "        missing in HTML: ${h}"; }
    done < <(sed -n 's/^## //p' "${ROOT}/BLUEPRINT.md")
    [ "${miss}" -eq 0 ] && ok "all MD section headings present in the HTML edition" \
                        || bad "${miss} MD heading(s) missing from the HTML edition"
fi
# Pin agreement: BUN_VERSION in the Containerfile must equal the version in BLUEPRINT.md.
if [ -f "${ROOT}/files/Containerfile" ]; then
    CV="$(sed -n 's/^ARG BUN_VERSION=//p' "${ROOT}/files/Containerfile")"
    BM="$(sed -n 's/^| bun | \([0-9][0-9.]*\).*/\1/p' "${ROOT}/BLUEPRINT.md" | head -1)"
    if [ -n "${CV}" ] && [ -n "${BM}" ] && [ "${CV}" = "${BM}" ]; then
        ok "Bun pin agrees between Containerfile (${CV}) and BLUEPRINT.md"
    else
        bad "Bun pin drift" "Containerfile='${CV}' BLUEPRINT='${BM}'"
    fi
fi
# The allowlist must not contain the dead wildcard and must carry the fixed entries.
AL="${ROOT}/files/squid/allowlist.txt"
dl "${AL}" '^\*\.|/\*\.githubusercontent' 0 "'*.' wildcard entry"
grep -qx 'binaries.prisma.sh' "${AL}" && ok "binaries.prisma.sh allowlisted" || bad "binaries.prisma.sh missing from allowlist"
grep -qx '.githubusercontent.com' "${AL}" && ok "leading-dot githubusercontent entry present" || bad "leading-dot githubusercontent entry missing"

echo "=================================================="
echo "  ${PASS} passed, ${FAIL} failed, ${SKIP} skipped"
echo "=================================================="
[ "${FAIL}" -eq 0 ]
