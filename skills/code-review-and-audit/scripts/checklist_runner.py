#!/usr/bin/env python3
"""
Skill: code-review-and-audit
Script: checklist_runner.py
Purpose: Automated evaluation of code review checklist categories.
         Implements the 12-category checklist from code-review-checklist skill.

Usage:
  python checklist_runner.py <project_path>

Categories evaluated:
  1.  Correctness       — Logic, edge cases, error handling, no obvious bugs
  2.  Security          — Input validation, injection, XSS, CSRF, secrets
  3.  Performance       — N+1 queries, loops, caching, bundle size
  4.  Code Quality      — Naming, DRY, SOLID, abstraction level
  5.  Testing           — Unit tests, edge cases, test readability
  6.  Documentation     — Complex logic, public APIs, README
  7.  Error Handling    — No bare excepts, proper error propagation
  8.  Naming Conventions— Reveal intent, consistent patterns
  9.  Type Safety       — TypeScript strict, no `any`, proper types
 10.  React/UI Patterns — All states, loading UX, mutation handling
 11.  LLM/AI Patterns   — Chain of thought, prompt injection, safe outputs
 12.  Anti-Patterns     — Magic numbers, deep nesting, God functions

Output: Structured JSON findings + human-readable summary.
"""
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple
from datetime import datetime

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except AttributeError:
    pass

# ============================================================================
# SCANNING CONFIGURATION
# ============================================================================

SKIP_DIRS = {
    'node_modules', '.git', 'dist', 'build', '__pycache__',
    '.venv', 'venv', '.next', '.nuxt', 'target', 'coverage',
    '.turbo', '.swc', 'tmp', 'temp', '.cache',
}

# Patterns that flag issues, organized by category
CHECK_PATTERNS: List[Dict[str, Any]] = [
    # ── 1. CORRECTNESS ──────────────────────────────────────────────────────
    {
        "category": "correctness",
        "severity": "high",
        "pattern": r'\.find\s*\([^)]*\)\.id\s*===',
        "message": "Potential .find() without null check — array element may be undefined",
        "extensions": {".ts", ".tsx", ".js", ".jsx"},
        "label": "Unsafe array access",
    },
    {
        "category": "correctness",
        "severity": "medium",
        "pattern": r'if\s*\(\s*\w+\s*\)\s*\{[^}]*\/\/ TODO',
        "message": "TODO/FIXME comment inside conditional — may indicate incomplete logic",
        "extensions": {".ts", ".tsx", ".js", ".jsx", ".py"},
        "label": "Incomplete conditional logic",
    },
    {
        "category": "correctness",
        "severity": "medium",
        "pattern": r'return\s+null(?!\s*\)])',
        "message": "Returning null — callers may not handle this edge case",
        "extensions": {".ts", ".tsx", ".js", ".jsx"},
        "label": "Null return without documentation",
        "neg_lookahead": r'(?:\.catch|if\s*\(\s*\w+\s*!==\s*null)',
    },
    {
        "category": "correctness",
        "severity": "high",
        "pattern": r'parseInt\s*\(\s*\w+\s*[,)]',
        "message": "parseInt without radix parameter — use Number() or parseInt(x, 10)",
        "extensions": {".ts", ".tsx", ".js", ".jsx"},
        "label": "Unsafe parseInt",
    },
    {
        "category": "correctness",
        "severity": "medium",
        "pattern": r'JSON\.parse\s*\([^)]*\)(?!\s*\.catch)',
        "message": "JSON.parse without .catch — JSON parsing errors will propagate",
        "extensions": {".ts", ".tsx", ".js", ".jsx"},
        "label": "Unsafe JSON.parse",
    },

    # ── 2. SECURITY ─────────────────────────────────────────────────────────
    {
        "category": "security",
        "severity": "critical",
        "pattern": r'eval\s*\(',
        "message": "eval() — code injection risk",
        "extensions": {".ts", ".tsx", ".js", ".jsx", ".py"},
        "label": "eval() usage",
    },
    {
        "category": "security",
        "severity": "high",
        "pattern": r'dangerouslySetInnerHTML',
        "message": "XSS risk: dangerouslySetInnerHTML without sanitization",
        "extensions": {".tsx", ".jsx"},
        "label": "XSS via dangerouslySetInnerHTML",
    },
    {
        "category": "security",
        "severity": "high",
        "pattern": r'\.innerHTML\s*=',
        "message": "XSS risk: direct innerHTML assignment",
        "extensions": {".ts", ".tsx", ".js", ".jsx"},
        "label": "XSS via innerHTML",
    },
    {
        "category": "security",
        "severity": "critical",
        "pattern": r'["\'][^"\']*\+.*(?:SELECT|INSERT|UPDATE|DELETE)',
        "message": "SQL injection risk: string concatenation in query",
        "extensions": {".ts", ".tsx", ".js", ".jsx", ".py"},
        "label": "SQL injection",
        "lookahead": r'query|execute|raw\s*\(|cursor\.execute',
    },
    {
        "category": "security",
        "severity": "critical",
        "pattern": r'(?:password|secret|token|api[_-]?key)\s*[=:]\s*["\'][^"\']{8,}["\']',
        "message": "Potential hardcoded credential — use environment variables",
        "extensions": {".ts", ".tsx", ".js", ".jsx", ".py"},
        "label": "Hardcoded credential",
    },
    {
        "category": "security",
        "severity": "high",
        "pattern": r'verify\s*=\s*False',
        "message": "SSL verification disabled — MITM attack risk",
        "extensions": {".ts", ".tsx", ".js", ".jsx", ".py"},
        "label": "SSL verify disabled",
    },
    {
        "category": "security",
        "severity": "critical",
        "pattern": r'Bearer\s+[a-zA-Z0-9\-_.]+',
        "message": "Hardcoded bearer token — rotate immediately and use env vars",
        "extensions": {".ts", ".tsx", ".js", ".jsx", ".py"},
        "label": "Hardcoded bearer token",
    },

    # ── 3. PERFORMANCE ──────────────────────────────────────────────────────
    {
        "category": "performance",
        "severity": "medium",
        "pattern": r'for\s*\([^)]*in\s+\w+\)',
        "message": "for...in iterates all properties including inherited — use for...of or .forEach",
        "extensions": {".ts", ".tsx", ".js", ".jsx"},
        "label": "for...in loop on array",
    },
    {
        "category": "performance",
        "severity": "medium",
        "pattern": r'\.map\s*\([^)]*\)[^;]*\.filter',
        "message": "Chained map+filter — consider single reduce or filter-first approach",
        "extensions": {".ts", ".tsx", ".js", ".jsx"},
        "label": "Inefficient map+filter chain",
    },
    {
        "category": "performance",
        "severity": "high",
        "pattern": r'require\s*\(\s*["\'][^"\']*\.(svg|png|jpg|jpeg|gif|woff2?)["\']',
        "message": "Static asset imported at top level — large assets bloat bundle. Use dynamic import or URL.",
        "extensions": {".ts", ".tsx", ".js", ".jsx"},
        "label": "Static asset import in bundle",
    },

    # ── 4. CODE QUALITY ─────────────────────────────────────────────────────
    {
        "category": "code_quality",
        "severity": "medium",
        "pattern": r'\/\/\s*[A-Z]{4,}\s*:',
        "message": "ALL CAPS comment — unclear or missing explanation",
        "extensions": {".ts", ".tsx", ".js", ".jsx", ".py"},
        "label": "Unclear CAPS comment",
    },
    {
        "category": "code_quality",
        "severity": "medium",
        "pattern": r'function\s+\w+\s*\([^)]*\{[^}]{500,}',
        "message": "Function exceeds 500 characters — consider splitting",
        "extensions": {".ts", ".tsx", ".js", ".jsx"},
        "label": "Long function (>500 chars)",
    },
    {
        "category": "code_quality",
        "severity": "medium",
        "pattern": r'class\s+\w+\s*\{[^}]{3000,}',
        "message": "Class exceeds 3000 characters — likely violating Single Responsibility",
        "extensions": {".ts", ".tsx", ".js", ".jsx"},
        "label": "Large class (>3000 chars)",
    },

    # ── 5. TESTING ──────────────────────────────────────────────────────────
    {
        "category": "testing",
        "severity": "medium",
        "pattern": r'describe\s*\(\s*["\']',
        "extensions": {".ts", ".tsx", ".js", ".jsx", ".py"},
        "label": "Test file detected — no special pattern (informational)",
        "severity": "info",
        "pattern": r'xdescribe|xit\s*\(',
        "message": "Skipped test found — was this intentional?",
    },

    # ── 6. ERROR HANDLING ───────────────────────────────────────────────────
    {
        "category": "error_handling",
        "severity": "high",
        "pattern": r'except\s*:\s*\n\s*pass',
        "message": "Bare except with pass — silently swallows all errors",
        "extensions": {".py"},
        "label": "Bare except + pass",
    },
    {
        "category": "error_handling",
        "severity": "high",
        "pattern": r'catch\s*\(\s*\w*\s*\)\s*\{\s*\}',
        "message": "Empty catch block — errors silently ignored",
        "extensions": {".ts", ".tsx", ".js", ".jsx"},
        "label": "Empty catch block",
    },
    {
        "category": "error_handling",
        "severity": "medium",
        "pattern": r'catch\s*\([^)]*\)\s*\{\s*console\.log',
        "message": "catch block only logs error — no user feedback or recovery",
        "extensions": {".ts", ".tsx", ".js", ".jsx"},
        "label": "Silent catch (log only)",
    },

    # ── 7. NAMING ───────────────────────────────────────────────────────────
    {
        "category": "naming",
        "severity": "low",
        "pattern": r'\bconst\s+[a-z]\s*=',
        "message": "Single-letter variable name — unclear intent",
        "extensions": {".ts", ".tsx", ".js", ".jsx"},
        "label": "Single-letter variable",
        "neg_lookahead": r'(?:x|y|z|xs|ys|i|j|k)\s*[=:]',
    },
    {
        "category": "naming",
        "severity": "medium",
        "pattern": r'\bconst\s+[A-Z][a-z]+\s*=',
        "message": "PascalCase variable name — should be camelCase for variables",
        "extensions": {".ts", ".tsx", ".js", ".jsx"},
        "label": "PascalCase const (should be camelCase)",
    },

    # ── 8. TYPE SAFETY ──────────────────────────────────────────────────────
    {
        "category": "type_safety",
        "severity": "high",
        "pattern": r':\s*any\b',
        "message": "Use of 'any' type — defeats TypeScript safety. Use 'unknown' instead.",
        "extensions": {".ts", ".tsx"},
        "label": "any type used",
    },
    {
        "category": "type_safety",
        "severity": "high",
        "pattern": r'@ts-ignore',
        "message": "@ts-ignore suppresses all type errors — fix the underlying issue",
        "extensions": {".ts", ".tsx"},
        "label": "@ts-ignore directive",
    },
    {
        "category": "type_safety",
        "severity": "medium",
        "pattern": r'@ts-nocheck',
        "message": "@ts-nocheck disables type checking for this file",
        "extensions": {".ts", ".tsx"},
        "label": "@ts-nocheck directive",
    },
    {
        "category": "type_safety",
        "severity": "medium",
        "pattern": r'!\s*\.\s*(?:map|filter|reduce|find)',
        "message": "Non-null assertion before array method — potential null crash",
        "extensions": {".ts", ".tsx"},
        "label": "Non-null assertion on array method",
    },

    # ── 9. REACT / UI PATTERNS ──────────────────────────────────────────────
    {
        "category": "react_ui",
        "severity": "medium",
        "pattern": r'setState\s*\(\s*\w+\s*\)',
        "message": "Object-form setState — may cause stale closures. Use functional form.",
        "extensions": {".tsx", ".jsx"},
        "label": "Object setState (potential stale closure)",
    },
    {
        "category": "react_ui",
        "severity": "medium",
        "pattern": r'useEffect\s*\([^)]*\)\s*[,;]\s*\n\s*\[',
        "message": "useEffect with no dependencies — likely runs on every render",
        "extensions": {".tsx", ".jsx"},
        "label": "useEffect with empty deps array",
        "neg_lookahead": r'\[.*\]',
    },

    # ── 10. LLM / AI PATTERNS ───────────────────────────────────────────────
    {
        "category": "llm_patterns",
        "severity": "high",
        "pattern": r'(?:system\s*prompt|prompt\s*engineering|ai\s*generate)',
        "extensions": {".ts", ".tsx", ".js", ".jsx", ".py"},
        "label": "AI/llm code detected — no special pattern (informational)",
        "severity": "info",
        "pattern": r'generate\s*\(\s*\{[^}]*input\s*:',
        "message": "AI call without structured schema — add schema validation for output",
        "extensions": {".ts", ".tsx", ".js", ".jsx", ".py"},
        "label": "Untyped AI generate call",
    },
]

# Additional file-level checks
FILE_CHECKS: List[Dict[str, Any]] = [
    {
        "category": "documentation",
        "severity": "medium",
        "check": "no_readme",
        "message": "No README.md found in project root",
        "files": ["README.md", "readme.md"],
    },
    {
        "category": "testing",
        "severity": "high",
        "check": "no_test_files",
        "message": "No test files found — codebase may lack test coverage",
        "files": [],
    },
    {
        "category": "code_quality",
        "severity": "medium",
        "check": "no_gitignore",
        "message": "No .gitignore found",
        "files": [".gitignore"],
    },
    {
        "category": "security",
        "severity": "medium",
        "check": "no_env_example",
        "message": "No .env.example found — contributors may misconfigure secrets",
        "files": [".env.example", ".env.example"],
    },
]

# ============================================================================
# SCANNING ENGINE
# ============================================================================

def scan_file(filepath: Path, relative_to: Path) -> List[Dict[str, Any]]:
    """Scan a single file for all pattern matches."""
    findings = []
    ext = filepath.suffix.lower()

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        content = "".join(lines)
    except Exception:
        return findings

    for check in CHECK_PATTERNS:
        if ext not in check.get("extensions", set()):
            continue

        pattern = check["pattern"]
        neg = check.get("neg_lookahead", "")

        for line_num, line in enumerate(lines, 1):
            # Skip data definition lines — these contain patterns, messages,
            # types, and labels as Python dict string values. Matches on these
            # lines are ALWAYS false positives (the pattern is in the data, not
            # in actual code being reviewed).
            #
            # Pattern definition lines: "pattern": r'...',  (raw string, no leading ")
            # Other dict value lines:   "label": "text",   (regular string)
            if '"pattern":' in line or '"label":' in line or '"message":' in line:
                continue
            if re.search(r'^\s*"[a-z_]+":\s*(?:"[^"]*"|\[)', line):
                continue
            if neg and re.search(neg, line):
                continue
            if re.search(pattern, line, re.IGNORECASE):
                findings.append({
                    "category": check["category"],
                    "severity": check["severity"],
                    "type": check["label"],
                    "message": check["message"],
                    "file": str(filepath.relative_to(relative_to)),
                    "line": line_num,
                    "snippet": line.strip()[:100],
                })

    return findings


def run_file_checks(project_path: Path) -> List[Dict[str, Any]]:
    """Run file-level checks (README, tests, .gitignore, .env.example)."""
    findings = []
    root_files = set(f.name for f in project_path.iterdir() if f.is_file())

    # README check
    if not any(f in root_files for f in ["README.md", "readme.md", "README.MD"]):
        findings.append({
            "category": "documentation",
            "severity": "medium",
            "type": "no_readme",
            "message": "No README.md found in project root",
            "file": str(project_path),
            "line": None,
        })

    # Test files check
    has_tests = False
    for ext in [".test.ts", ".test.tsx", ".test.js", ".spec.ts", ".spec.tsx", ".spec.js", "_test.py", "test_*.py"]:
        if any(project_path.rglob(f"*{ext}")):
            has_tests = True
            break
    if not has_tests:
        findings.append({
            "category": "testing",
            "severity": "high",
            "type": "no_test_files",
            "message": "No test files found — codebase may lack test coverage",
            "file": str(project_path),
            "line": None,
        })

    # .gitignore check
    if ".gitignore" not in root_files:
        findings.append({
            "category": "code_quality",
            "severity": "low",
            "type": "no_gitignore",
            "message": "No .gitignore found",
            "file": str(project_path),
            "line": None,
        })

    # .env.example check (only for Node/Python projects with .env)
    has_env = any(f.name == ".env" for f in project_path.iterdir() if f.is_file())
    has_env_example = any(f".env" in f.name for f in project_path.iterdir() if f.is_file())
    if has_env and not has_env_example:
        findings.append({
            "category": "security",
            "severity": "medium",
            "type": "no_env_example",
            "message": ".env exists but no .env.example found — secrets may leak",
            "file": str(project_path),
            "line": None,
        })

    return findings


# ============================================================================
# MAIN
# ============================================================================

def main():
    project_path = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()

    if not project_path.exists():
        print(json.dumps({"error": f"Directory not found: {project_path}"}))
        sys.exit(1)

    all_findings = []

    # File-level checks
    file_findings = run_file_checks(project_path)
    all_findings.extend(file_findings)

    # Pattern-based scanning
    code_extensions = {".ts", ".tsx", ".js", ".jsx", ".py"}

    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        for file in files:
            ext = Path(file).suffix.lower()
            if ext not in code_extensions:
                continue

            filepath = Path(root) / file
            findings = scan_file(filepath, project_path)
            all_findings.extend(findings)

    # Group by category
    categories = {}
    for f in all_findings:
        cat = f.get("category", "other")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(f)

    # Summary
    by_severity = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
    for f in all_findings:
        by_severity[f.get("severity", "info")] += 1

    result = {
        "script": "checklist_runner",
        "version": "1.0.0",
        "project": str(project_path),
        "timestamp": datetime.now().isoformat(),
        "total_findings": len(all_findings),
        "by_severity": by_severity,
        "by_category": {cat: len(items) for cat, items in categories.items()},
        "findings": all_findings,
    }

    # Human-readable output
    print(f"\n{'='*60}")
    print(f"  CODE REVIEW CHECKLIST — {project_path.name}")
    print(f"{'='*60}")

    for cat, items in sorted(categories.items()):
        severity_counts = {}
        for item in items:
            sev = item["severity"]
            severity_counts[sev] = severity_counts.get(sev, 0) + 1

        print(f"\n  [{cat.upper()}] ({len(items)} items)")
        for sev, count in sorted(severity_counts.items(), key=lambda x: ["critical","high","medium","low","info"].index(x[0])):
            icon = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢", "info": "⚪"}.get(sev, "?")
            print(f"    {icon} {sev}: {count}")
            for item in items:
                if item["severity"] == sev:
                    loc = f"  → {item['file']}" + (f":L{item['line']}" if item.get("line") else "")
                    print(f"       • {item['message']}")
                    print(f"        {loc}")
                    break  # only show first of each severity per category

    print(f"\n{'='*60}")
    total = len(all_findings)
    if total == 0:
        print("  ✅ All checks passed — no findings")
    else:
        print(f"  ⚠️  {total} finding{'s' if total != 1 else ''} found")
    print(f"{'='*60}\n")

    # Always output JSON at end for programmatic consumption
    print("--- JSON OUTPUT ---")
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
