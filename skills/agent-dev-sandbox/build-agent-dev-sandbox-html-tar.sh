#!/usr/bin/env bash
set -euo pipefail

REPO="https://github.com/nordeim/my-pi-agent.git"
WORK="$(mktemp -d)"
ARCHIVE="agent-dev-sandbox-html.tar.gz"
BUNDLE="my-pi-agent/skills/agent-dev-sandbox"

echo "==> Cloning ${REPO}"
git clone --depth 1 "${REPO}" "${WORK}/my-pi-agent"
cd "${WORK}"

echo "==> Checking test-suite integrity (R-1)"
LINES=$(wc -l < "${BUNDLE}/tests/run-tests.sh")
if [ "${LINES}" -lt 100 ]; then
  echo "ERROR: tests/run-tests.sh has only ${LINES} lines — likely truncated. Restore the full suite before packaging." >&2
  exit 1
fi

echo "==> Applying documentation and metadata patches"
python3 - <<'PY'
from pathlib import Path

b = Path("my-pi-agent/skills/agent-dev-sandbox")

# R-2: SKILL.md allowed-tools
skill = (b/"SKILL.md").read_text()
old_tools_prefix = "allowed-tools: "
lines = skill.splitlines()
for i, line in enumerate(lines):
    if line.startswith("allowed-tools:"):
        lines[i] = ("allowed-tools: Bash(scripts/00-preflight.sh:*), "
                    "Bash(scripts/10-host-bootstrap.sh:*), "
                    "Bash(scripts/20-build-image.sh:*), "
                    "Bash(scripts/30-gateway.sh:*), "
                    "Bash(scripts/40-workspace.sh:*), "
                    "Bash(scripts/45-ci-run.sh:*), "
                    "Bash(scripts/50-verify.sh:*), "
                    "Bash(scripts/60-tier2-microvm.sh:*), "
                    "Bash(sudo scripts/10-host-bootstrap.sh:*), "
                    "Bash(sudo -E scripts/10-host-bootstrap.sh:*), "
                    "Bash(tests/run-tests.sh:*), Bash(shellcheck:*), "
                    "Bash(bash -n:*), Bash(podman ps:*), Bash(podman logs:*), "
                    "Bash(podman inspect:*), Bash(podman image ls:*), "
                    "Bash(podman network inspect:*), Bash(podman system df:*), "
                    "Bash(bash scripts/*:*), Bash(./scripts/*:*)")
        break
(b/"SKILL.md").write_text("\n".join(lines) + "\n")

# R-3: metadata requires bins
skill = (b/"SKILL.md").read_text()
skill = skill.replace('"bins":["bash","sudo"]',
                      '"bins":["bash","sudo","podman","jq","shellcheck","git"]')
(b/"SKILL.md").write_text(skill)

# R-4: BLUEPRINT header second-pass note
bp = (b/"BLUEPRINT.md").read_text()
needle = "audit remediations were applied and re-verified on **2026-11-06**"
if needle in bp and "2026-11-07" not in bp.split("## 1.")[0]:
    bp = bp.replace(
        "audit remediations were applied and re-verified on **2026-11-06**",
        "audit remediations were applied and re-verified on **2026-11-06**; "
        "a second-pass validation on **2026-11-07** closed four residual defects (S-1–S-4)"
    )
(b/"BLUEPRINT.md").write_text(bp)

# R-8: audit provenance
ar = (b/"references/audit-remediation.md").read_text()
prov = """## Audit provenance
- External audit report URL: https://01a1aedb-2643-732a-a055-34847c36e9cb.arena.site/
  (user-generated, JS-rendered; capture as PDF/screenshot for retention).
- Canonical findings and dispositions: this file (22 findings + 4 second-pass defects).
- Validation method: full-file read, executable reproductions, primary-source checks.

"""
if "## Audit provenance" not in ar:
    ar = prov + ar
(b/"references/audit-remediation.md").write_text(ar)

# R-7: port note in allowlist
al = (b/"files/squid/allowlist.txt").read_text()
note = ("# NOTE: the gateway proxies only ports 80 and 443. Services on other ports\n"
        "# (e.g. 8443) require a squid.conf change, not an allowlist line.\n")
if "proxies only ports 80 and 443" not in al:
    al = al.replace("# --- OS package mirrors", note + "# --- OS package mirrors", 1)
(b/"files/squid/allowlist.txt").write_text(al)
PY

echo "==> Running syntax checks and test suite"
cd "${BUNDLE}"
bash -n scripts/*.sh files/*.sh tests/run-tests.sh
if command -v shellcheck >/dev/null 2>&1; then
  shellcheck -x scripts/*.sh files/*.sh
else
  echo "WARN: shellcheck not installed — skipping shellcheck gate"
fi
bash tests/run-tests.sh

echo "==> Building archive"
cd "${WORK}"
tar -czf "${OLDPWD}/${ARCHIVE}" -C skills agent-dev-sandbox

echo "==> Archive: ${OLDPWD}/${ARCHIVE}"
ls -lh "${OLDPWD}/${ARCHIVE}"
sha256sum "${OLDPWD}/${ARCHIVE}"
