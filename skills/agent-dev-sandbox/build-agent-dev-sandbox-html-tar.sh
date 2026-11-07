#!/usr/bin/env bash
set -euo pipefail

REPO="https://github.com/nordeim/my-pi-agent.git"
WORK="$(mktemp -d)"
OUTDIR="$(pwd)"
ARCHIVE="agent-dev-sandbox-html-v2.tar.gz"
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

echo "==> Applying documentation and metadata patches (idempotent: no-ops on an already-fixed tree)"
python3 - <<'PY'
import re
from pathlib import Path

b = Path("my-pi-agent/skills/agent-dev-sandbox")

# R-2: SKILL.md allowed-tools — presence-guarded so a later, different
# allowed-tools line is never clobbered on an already-fixed tree.
skill = (b/"SKILL.md").read_text()
if "Bash(tests/run-tests.sh:*)" not in skill:
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

# R-3: metadata requires bins — validated list. git is deliberately absent:
# no host-side script invokes git (it runs inside containers; the image
# bakes it).
skill = (b/"SKILL.md").read_text()
if '"bins":["bash","sudo"]' in skill:
    skill = skill.replace('"bins":["bash","sudo"]',
                          '"bins":["bash","sudo","podman","jq","shellcheck"]')
    (b/"SKILL.md").write_text(skill)

# R-4: BLUEPRINT header pass history. Wrap-tolerant anchor (B-3: the
# original needle spanned a line break in BLUEPRINT.md and never matched);
# guarded against double application.
bp = (b/"BLUEPRINT.md").read_text()
if "2026-11-07" not in bp.split("## 1.")[0]:
    bp = re.sub(
        r"their validation, and the fixes\)\. Version",
        "their validation, and the fixes), a second-pass validation on **2026-11-07** "
        "closed four residual defects (S-1\u2013S-4), and a third-pass review the same "
        "day validated and remediated its eight follow-up findings (R-1\u2013R-8). Version",
        bp, count=1)
    (b/"BLUEPRINT.md").write_text(bp)

# R-8: audit provenance (aligned with the in-repo section).
ar = (b/"references/audit-remediation.md").read_text()
if "## Audit provenance" not in ar:
    prov = (
        "## Audit provenance\n\n"
        "- External audit report URL: https://01a1aedb-2643-732a-a055-34847c36e9cb.arena.site/\n"
        "  (user-generated, JavaScript-rendered; the findings were captured from the\n"
        "  page bundle and are recorded here \u2014 this file is the canonical\n"
        "  findings-and-dispositions record for every pass).\n"
        "- Session logs kept alongside this bundle: `remediation_log_1.md` (second\n"
        "  pass, S-1\u2013S-4), `remediation_log_2.md` (third-pass review, R-1\u2013R-8),\n"
        "  `remediation_log_3.md` (third-pass remediation session).\n"
        "- Validation method, every pass: full-file reads, executable reproductions,\n"
        "  primary-source checks.\n\n")
    ar = ar.replace("## Verdicts and dispositions",
                    prov + "## Verdicts and dispositions", 1)
    (b/"references/audit-remediation.md").write_text(ar)

# R-7: port note in the allowlist header (same text as the in-repo note).
al = (b/"files/squid/allowlist.txt").read_text()
note = ("# NOTE: the gateway proxies only ports 80 and 443. Services on other ports\n"
        "# (e.g. 8443) require a squid.conf change, not an allowlist line.\n")
if "proxies only ports 80 and 443" not in al:
    al = al.replace("# fatal configuration error at parse time.\n",
                    "# fatal configuration error at parse time.\n" + note, 1)
    (b/"files/squid/allowlist.txt").write_text(al)
PY

echo "==> Running syntax checks and test suite"
cd "${BUNDLE}"
bash -n scripts/*.sh files/*.sh files/ws-shell tests/run-tests.sh
if command -v shellcheck >/dev/null 2>&1; then
  shellcheck -x scripts/*.sh files/*.sh files/ws-shell
else
  echo "WARN: shellcheck not installed — skipping shellcheck gate"
fi
bash tests/run-tests.sh

echo "==> Building archive"
cd "${WORK}"
tar -czf "${OUTDIR}/${ARCHIVE}" -C my-pi-agent/skills agent-dev-sandbox

echo "==> Archive: ${OUTDIR}/${ARCHIVE}"
ls -lh "${OUTDIR}/${ARCHIVE}"
sha256sum "${OUTDIR}/${ARCHIVE}"
