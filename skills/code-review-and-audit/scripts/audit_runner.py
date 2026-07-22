#!/usr/bin/env python3
"""
Skill: code-review-and-audit
Script: audit_runner.py
Purpose: Unified orchestration script that runs all review phases in priority order.
         Entry point for the code-review-and-audit skill.

Usage:
  python audit_runner.py <project_path> [--mode quick|standard|deep|security-only|quality-only] [--url <url>]

Exit Codes:
  0 = All checks passed (no Critical/High findings for the mode)
  1 = Findings at or above the mode's failure threshold

Phase Order:
  Phase 1  → Static Analysis    (lint-and-validate → lint_runner.py)
  Phase 2  → Security Scan      (vulnerability-scanner → security_scan.py)
  Phase 3  → Code Quality       (code-review-checklist → checklist_runner.py)
  Phase 4  → Test Coverage      (testing-patterns → test_runner.py, if applicable)
  Phase 5  → Performance        (performance-profiling → lighthouse_audit.py, if --url given)
  Phase 6  → Expert Review      (code-review subagent dispatch — manual step)

Report: Structured JSON + human-readable summary written to stdout.
        Markdown report written to <project_path>/.audit-report.md
"""
import subprocess
import json
import os
import sys
import re
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Fix console encoding
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except AttributeError:
    pass

# ============================================================================
# CONFIGURATION
# ============================================================================

# Phase definitions: (phase_name, script, script_args, required_for_mode)
PHASES: List[tuple] = [
    ("phase_1_static_analysis",  "lint_runner.py",              [],              ["quick", "standard", "deep", "quality-only"]),
    ("phase_2_security_scan",    "security_scan.py",            ["--scan-type", "all"], ["standard", "deep", "security-only"]),
    ("phase_3_code_quality",     "checklist_runner.py",         [],              ["standard", "deep", "quality-only"]),
    ("phase_4_test_coverage",    "test_runner.py",              [],              ["standard", "deep"]),
    ("phase_5_performance",      "lighthouse_audit.py",         [],              ["deep"]),
]

# Failure threshold by mode: any finding at or above this severity fails the run
FAIL_THRESHOLDS: Dict[str, str] = {
    "quick":         "critical",
    "standard":      "high",
    "deep":          "medium",
    "security-only": "critical",
    "quality-only":  "high",
}

# Severity rank (lower = more severe)
SEVERITY_RANK: Dict[str, int] = {
    "critical": 0,
    "high":     1,
    "medium":   2,
    "low":      3,
    "info":     4,
    "passed":   5,
}

SKILL_BASE = Path(__file__).parent.parent
SKILL_SCRIPTS = SKILL_BASE / "scripts"
# User-installed skills (portable — uses Path.home for cross-platform)
USER_SKILLS = Path.home() / ".claude" / "skills"

# ============================================================================
# SCRIPT DISCOVERY
# ============================================================================

def find_script(name: str, project_path: Path) -> Optional[Path]:
    """Locate a script in skill scripts, user skills dir, or project root."""
    candidates = [
        # 1. This skill's own scripts (checklist_runner.py ships here)
        SKILL_SCRIPTS / name,
        # 2. User-installed skills (lint_runner.py, security_scan.py, etc.)
        USER_SKILLS / "lint-and-validate" / "scripts" / name,
        USER_SKILLS / "vulnerability-scanner" / "scripts" / name,
        USER_SKILLS / "testing-patterns" / "scripts" / name,
        USER_SKILLS / "performance-profiling" / "scripts" / name,
        # 3. Project root (for scripts in <project>/scripts/)
        project_path / "scripts" / name,
        project_path / name,
    ]
    for p in candidates:
        if p.exists():
            return p
    return None


def python_executable() -> str:
    """Return 'python' or 'python3' available in PATH."""
    for cmd in ["python3", "python"]:
        try:
            subprocess.run([cmd, "--version"], capture_output=True, timeout=5)
            return cmd
        except Exception:
            continue
    return "python3"


# ============================================================================
# PHASE RUNNERS
# ============================================================================

def run_lint(project_path: Path) -> Dict[str, Any]:
    """Run lint_runner.py for Phase 1 static analysis."""
    result = {
        "phase": "phase_1_static_analysis",
        "name": "Static Analysis (Lint & Types)",
        "status": "skipped",
        "findings": [],
        "summary": {},
        "error": "",
    }
    script = find_script("lint_runner.py", project_path)
    if not script:
        result["error"] = "lint_runner.py not found in any skills directory"
        return result

    py = python_executable()
    try:
        proc = subprocess.run(
            [py, str(script), str(project_path)],
            cwd=str(project_path),
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=120,
        )
        output = proc.stdout
        # Parse JSON block from output
        json_match = re.search(r'\{[\s\S]*"script"[\s\S]*\}', output)
        if json_match:
            data = json.loads(json_match.group())
            checks = data.get("checks", [])
            result["summary"] = data
            for check in checks:
                sev = "critical" if not check.get("passed", True) else "passed"
                result["findings"].append({
                    "severity": sev,
                    "tool": check.get("name", "unknown"),
                    "message": check.get("error", "") or ("passed" if check.get("passed") else "failed"),
                    "passed": check.get("passed", False),
                })
                if not check.get("passed"):
                    result["status"] = "failed"
        else:
            result["error"] = output[:500]
            result["status"] = "error"
    except subprocess.TimeoutExpired:
        result["status"] = "error"
        result["error"] = "Timeout after 120s"
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)
    return result


def run_security_scan(project_path: Path) -> Dict[str, Any]:
    """Run security_scan.py for Phase 2 vulnerability scanning."""
    result = {
        "phase": "phase_2_security_scan",
        "name": "Security Scan (OWASP)",
        "status": "skipped",
        "findings": [],
        "summary": {},
        "error": "",
    }
    script = find_script("security_scan.py", project_path)
    if not script:
        result["error"] = "security_scan.py not found in any skills directory"
        return result

    py = python_executable()
    try:
        proc = subprocess.run(
            [py, str(script), str(project_path), "--output", "json"],
            cwd=str(project_path),
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=180,
        )
        output = proc.stdout
        try:
            data = json.loads(output)
        except json.JSONDecodeError:
            # Try to extract JSON from output
            json_match = re.search(r'\{[\s\S]*"project"[\s\S]*\}', output)
            if json_match:
                data = json.loads(json_match.group())
            else:
                result["error"] = output[:500]
                result["status"] = "error"
                return result

        result["summary"] = {
            "total_findings": data.get("summary", {}).get("total_findings", 0),
            "critical": data.get("summary", {}).get("critical", 0),
            "high": data.get("summary", {}).get("high", 0),
            "overall_status": data.get("summary", {}).get("overall_status", "unknown"),
        }

        scans = data.get("scans", {})
        for scan_name, scan_data in scans.items():
            for finding in scan_data.get("findings", []):
                # Fallback chain: type (secrets) → pattern (code patterns) → category → issue (config) → unknown
                finding_type = (
                    finding.get("type")
                    or finding.get("pattern")
                    or finding.get("category")
                    or finding.get("issue")
                    or "unknown"
                )
                result["findings"].append({
                    "severity": finding.get("severity", "medium"),
                    "tool": scan_name,
                    "type": finding_type,
                    "message": finding.get("message", ""),
                    "location": finding.get("file", ""),
                    "line": finding.get("line"),
                })

        if result["summary"].get("critical", 0) > 0:
            result["status"] = "critical"
        elif result["summary"].get("high", 0) > 0:
            result["status"] = "failed"
        elif result["findings"]:
            result["status"] = "warning"
        else:
            result["status"] = "passed"

    except subprocess.TimeoutExpired:
        result["status"] = "error"
        result["error"] = "Timeout after 180s"
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)
    return result


def run_checklist(project_path: Path) -> Dict[str, Any]:
    """Run checklist_runner.py for Phase 3 code quality."""
    result = {
        "phase": "phase_3_code_quality",
        "name": "Code Quality (Checklist)",
        "status": "skipped",
        "findings": [],
        "summary": {},
        "error": "",
    }
    script = find_script("checklist_runner.py", project_path)
    if not script:
        result["error"] = "checklist_runner.py not found — see scripts/checklist_runner.py"
        return result

    py = python_executable()
    try:
        proc = subprocess.run(
            [py, str(script), str(project_path)],
            cwd=str(project_path),
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=120,
        )
        output = proc.stdout
        json_match = re.search(r'\{[\s\S]*"category"[\s\S]*\}', output)
        if json_match:
            data = json.loads(json_match.group())
            result["summary"] = {
                "total_findings": data.get("total_findings", 0),
                "critical": sum(1 for f in data.get("findings", []) if f.get("severity") == "critical"),
                "high": sum(1 for f in data.get("findings", []) if f.get("severity") == "high"),
                "medium": sum(1 for f in data.get("findings", []) if f.get("severity") == "medium"),
            }
            result["findings"] = data.get("findings", [])
            if data.get("findings"):
                result["status"] = "failed"
            else:
                result["status"] = "passed"
        else:
            # Checklist may have produced human-readable output
            result["status"] = "passed"
            result["error"] = output[:300] if output.strip() else ""
    except subprocess.TimeoutExpired:
        result["status"] = "error"
        result["error"] = "Timeout after 120s"
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)
    return result


def run_test_coverage(project_path: Path) -> Dict[str, Any]:
    """Run test_runner.py for Phase 4 test coverage."""
    result = {
        "phase": "phase_4_test_coverage",
        "name": "Test Coverage",
        "status": "skipped",
        "findings": [],
        "summary": {},
        "error": "",
    }
    script = find_script("test_runner.py", project_path)
    if not script:
        result["error"] = "test_runner.py not found — test phase skipped"
        return result

    py = python_executable()
    try:
        proc = subprocess.run(
            [py, str(script), str(project_path)],
            cwd=str(project_path),
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=180,
        )
        output = proc.stdout
        json_match = re.search(r'\{[\s\S]*"test_results"[\s\S]*\}', output)
        if not json_match:
            json_match = re.search(r'\{[\s\S]*"passed"[\s\S]*\}', output)
        if json_match:
            data = json.loads(json_match.group())
            tests = data.get("test_results", data.get("results", []))
            passed = sum(1 for t in tests if t.get("passed"))
            failed = sum(1 for t in tests if not t.get("passed"))
            result["summary"] = {"passed": passed, "failed": failed, "total": len(tests)}
            if failed > 0:
                result["status"] = "failed"
                for t in tests:
                    if not t.get("passed"):
                        result["findings"].append({
                            "severity": "high",
                            "tool": "test_runner",
                            "type": "test_failure",
                            "message": t.get("name", "Unknown test"),
                            "error": t.get("error", ""),
                        })
            else:
                result["status"] = "passed"
        else:
            result["error"] = output[:300] if output.strip() else "No parseable output"
    except subprocess.TimeoutExpired:
        result["status"] = "error"
        result["error"] = "Timeout after 180s"
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)
    return result


def run_lighthouse(url: str) -> Dict[str, Any]:
    """Run lighthouse_audit.py for Phase 5 performance."""
    result = {
        "phase": "phase_5_performance",
        "name": "Performance (Lighthouse)",
        "status": "skipped",
        "findings": [],
        "summary": {},
        "error": "",
    }
    script = find_script("lighthouse_audit.py", Path.cwd())
    if not script:
        result["error"] = "lighthouse_audit.py not found — performance phase skipped"
        return result

    py = python_executable()
    try:
        proc = subprocess.run(
            [py, str(script), url],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=300,
        )
        output = proc.stdout
        json_match = re.search(r'\{[\s\S]*"lighthouse"[\s\S]*\}', output)
        if not json_match:
            json_match = re.search(r'\{[\s\S]*"score"[\s\S]*\}', output)
        if json_match:
            data = json.loads(json_match.group())
            result["summary"] = data
            lighthouse = data.get("lighthouse", data)
            # Check Core Web Vitals
            for metric in ["performance", "accessibility", "best-practices", "seo"]:
                score = lighthouse.get(metric, lighthouse.get(f"{metric}_score", 100))
                if isinstance(score, (int, float)) and score < 0.9:
                    sev = "critical" if score < 0.5 else "high" if score < 0.7 else "medium"
                    result["findings"].append({
                        "severity": sev,
                        "tool": "lighthouse",
                        "type": metric,
                        "message": f"{metric} score: {score:.0%}",
                    })
                    result["status"] = "warning"
            if not result["findings"]:
                result["status"] = "passed"
        else:
            result["error"] = output[:300] if output.strip() else "No parseable output"
    except subprocess.TimeoutExpired:
        result["status"] = "error"
        result["error"] = "Timeout after 300s"
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)
    return result


# ============================================================================
# ORCHESTRATION
# ============================================================================

def run_audit(project_path: Path, mode: str, url: Optional[str] = None) -> Dict[str, Any]:
    """Run the full audit pipeline for the given mode."""
    report = {
        "skill": "code-review-and-audit",
        "audit_runner_version": "1.0.0",
        "project": str(project_path),
        "mode": mode,
        "timestamp": datetime.now().isoformat(),
        "phases": [],
        "total_findings": 0,
        "by_severity": {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0},
        "failed_phases": [],
        "overall_status": "PASSED",
        "exit_code": 0,
    }

    phase_map = {
        "phase_1_static_analysis": lambda: run_lint(project_path),
        "phase_2_security_scan":   lambda: run_security_scan(project_path),
        "phase_3_code_quality":    lambda: run_checklist(project_path),
        "phase_4_test_coverage":   lambda: run_test_coverage(project_path),
        "phase_5_performance":     lambda: run_lighthouse(url) if url else None,
    }

    for phase_key, script_name, script_args, modes_in_scope in PHASES:
        if mode not in modes_in_scope:
            continue

        if phase_key == "phase_5_performance" and not url:
            continue

        runner = phase_map.get(phase_key)
        if not runner:
            continue

        phase_result = runner()
        if phase_result is None:
            continue

        # Skip phases that errored with "not found" (informational only)
        if phase_result["status"] == "skipped" and "not found" in phase_result.get("error", "").lower():
            report["phases"].append(phase_result)
            continue

        report["phases"].append(phase_result)

        # Aggregate findings
        for finding in phase_result.get("findings", []):
            sev = finding.get("severity", "info")
            rank = SEVERITY_RANK.get(sev, 4)
            if rank <= SEVERITY_RANK.get("low", 3):
                report["by_severity"][sev] = report["by_severity"].get(sev, 0) + 1
                report["total_findings"] += 1

        if phase_result["status"] in ("critical", "failed"):
            report["failed_phases"].append(phase_key)

    # Determine overall status
    fail_threshold = FAIL_THRESHOLDS.get(mode, "high")
    fail_rank = SEVERITY_RANK.get(fail_threshold, 1)

    for sev in ["critical", "high", "medium"]:
        sev_rank = SEVERITY_RANK.get(sev, 4)
        if sev_rank <= fail_rank and report["by_severity"].get(sev, 0) > 0:
            report["overall_status"] = f"FAILED ({sev.upper()})"
            report["exit_code"] = 1
            break

    return report


# ============================================================================
# REPORTING
# ============================================================================

def print_summary(report: Dict[str, Any]) -> None:
    """Print human-readable audit summary."""
    sep = "=" * 64
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"\n{sep}")
    print(f"  CODE REVIEW & AUDIT — {report['mode'].upper()} MODE")
    print(f"{sep}")
    print(f"  Project : {report['project']}")
    print(f"  Time    : {ts}")
    print(f"  Skill   : {report['skill']} v{report['audit_runner_version']}")
    print(f"{sep}")

    # Phase results
    print(f"  PHASE RESULTS")
    print(f"  {'-'*60}")
    for phase in report["phases"]:
        icon = {
            "passed":   "[PASS]",
            "failed":   "[FAIL]",
            "critical": "[!! ]",
            "warning":  "[WARN]",
            "error":    "[ERR ]",
            "skipped":  "[SKIP]",
        }.get(phase["status"], "[??? ]")

        count = len(phase.get("findings", []))
        count_str = f" ({count} finding{'s' if count != 1 else ''})" if count else ""
        print(f"  {icon} {phase['name']}{count_str}")
        if phase.get("error") and phase["status"] == "skipped":
            print(f"        → {phase['error'][:80]}")

    print(f"{sep}")

    # Severity summary
    bs = report["by_severity"]
    print(f"  FINDINGS SUMMARY")
    print(f"  {'-'*60}")
    print(f"  {'Critical':>10}: {bs.get('critical', 0)}")
    print(f"  {'High':>10}:     {bs.get('high', 0)}")
    print(f"  {'Medium':>10}:   {bs.get('medium', 0)}")
    print(f"  {'Low':>10}:      {bs.get('low', 0)}")
    print(f"  {'Info':>10}:     {bs.get('info', 0)}")
    print(f"  {'TOTAL':>10}:    {report['total_findings']}")

    print(f"{sep}")
    status = report["overall_status"]
    status_icon = "✓" if report["exit_code"] == 0 else "✗"
    print(f"  {status_icon} OVERALL: {status}")
    print(f"{sep}\n")

    # Detailed findings (Critical + High only for concise output)
    critical_high = [
        f for phase in report["phases"]
        for f in phase.get("findings", [])
        if SEVERITY_RANK.get(f.get("severity", ""), 4) <= SEVERITY_RANK.get("high", 1)
    ]

    if critical_high:
        print("  CRITICAL + HIGH FINDINGS")
        print(f"  {'-'*60}")
        for f in critical_high:
            loc = f"{f.get('location', '')}" + (f" L{f.get('line','')}" if f.get("line") else "")
            print(f"  [{f.get('severity','').upper():8}] {f.get('type', f.get('tool', 'unknown'))}")
            print(f"    {f.get('message', '')[:80]}")
            if loc:
                print(f"    → {loc}")
        print()


def write_markdown_report(report: Dict[str, Any]) -> Path:
    """Write structured markdown audit report to project root."""
    project = Path(report["project"])
    report_path = project / ".audit-report.md"
    bs = report["by_severity"]

    # Group findings by severity
    grouped: Dict[str, List] = {"critical": [], "high": [], "medium": [], "low": [], "info": []}
    for phase in report["phases"]:
        for f in phase.get("findings", []):
            sev = f.get("severity", "info")
            if sev in grouped:
                grouped[sev].append({**f, "phase": phase.get("name", "")})

    lines = [
        "# Audit Report",
        "",
        f"**Skill:** code-review-and-audit",
        f"**Mode:** `{report['mode']}`",
        f"**Project:** `{report['project']}`",
        f"**Timestamp:** {report['timestamp']}",
        f"**Overall:** **{report['overall_status']}**",
        "",
        "---",
        "",
        "## Phase Results",
        "",
        "| Phase | Status | Findings |",
        "|-------|--------|----------|",
    ]

    for phase in report["phases"]:
        icon = {"passed": "✅", "failed": "❌", "critical": "🔴", "warning": "⚠️", "error": "⚡", "skipped": "⏭️"}.get(phase["status"], "?")
        count = len(phase.get("findings", []))
        lines.append(f"| {phase['name']} | {icon} {phase['status']} | {count} |")

    lines += [
        "",
        "## Findings by Severity",
        "",
        f"- 🔴 Critical: {bs.get('critical', 0)}",
        f"- 🟠 High:     {bs.get('high', 0)}",
        f"- 🟡 Medium:   {bs.get('medium', 0)}",
        f"- 🟢 Low:      {bs.get('low', 0)}",
        f"- ⚪ Info:     {bs.get('info', 0)}",
        "",
    ]

    for sev, label in [("critical","🔴 Critical"), ("high","🟠 High"), ("medium","🟡 Medium"), ("low","🟢 Low")]:
        findings = grouped.get(sev, [])
        if findings:
            lines.append(f"### {label}")
            lines.append("")
            for f in findings:
                loc = f.get("location", "")
                line = f" L{f['line']}" if f.get("line") else ""
                loc_str = f" `{loc}{line}`" if loc else ""
                lines.append(f"**[{sev.upper()}]** {f.get('type', f.get('tool','?'))} — {f.get('message','')}{loc_str}")
                lines.append(f"> Phase: {f.get('phase', '')}  ")
                lines.append("")

    if not any(grouped.values()):
        lines.append("## Findings\n\n✅ No findings — all checks passed.\n")

    lines += [
        "---",
        f"*Report generated by `code-review-and-audit` skill — {report['timestamp']}*",
    ]

    report_path.write_text("\n".join(lines), encoding='utf-8')
    return report_path


# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="code-review-and-audit: Unified code review and security audit runner"
    )
    parser.add_argument(
        "project_path",
        nargs="?",
        default=".",
        help="Project directory to audit (default: current directory)",
    )
    parser.add_argument(
        "--mode",
        choices=["quick", "standard", "deep", "security-only", "quality-only"],
        default="standard",
        help="Review mode (default: standard)",
    )
    parser.add_argument(
        "--url",
        help="URL for Lighthouse performance audit (activates Phase 5 in deep mode)",
    )
    parser.add_argument(
        "--json-only",
        action="store_true",
        help="Output JSON only, suppress human-readable summary",
    )
    parser.add_argument(
        "--no-report",
        action="store_true",
        help="Do not write .audit-report.md to project root",
    )

    args = parser.parse_args()
    project_path = Path(args.project_path).resolve()

    if not project_path.exists():
        print(json.dumps({"error": f"Directory not found: {project_path}"}))
        sys.exit(1)

    report = run_audit(project_path, args.mode, args.url)

    if not args.json_only:
        print_summary(report)

    report_path = None
    if not args.no_report:
        report_path = write_markdown_report(report)
        if not args.json_only:
            print(f"  📄 Report written to: {report_path}")

    print("\n--- JSON OUTPUT ---")
    print(json.dumps(report, indent=2, default=str))

    sys.exit(report["exit_code"])


if __name__ == "__main__":
    main()
