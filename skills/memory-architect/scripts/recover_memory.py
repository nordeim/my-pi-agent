#!/usr/bin/env python3
"""
Memory Architecture Recovery Script

Recovers the 3-layer OpenClaw memory system after corruption:
- Diagnoses what's broken
- Attempts to recover what can be recovered
- Rebuilds what's missing

Usage:
    python3 recover_memory.py [--backup-dir PATH] [--force]

Options:
    --backup-dir PATH   Directory to backup corrupted files (default: ~/memory-backup-TIMESTAMP)
    --force             Proceed with recovery without confirmation
"""

import argparse
import json
import os
import shutil
import sqlite3
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Configuration
WORKSPACE = Path.home() / ".openclaw" / "workspace"
OPENCLAW_CONFIG = Path.home() / ".openclaw" / "openclaw.json"
MEMORY_FILE = WORKSPACE / "MEMORY.md"
DAILY_DIR = WORKSPACE / "memory" / "daily"
LCM_DB = Path.home() / ".openclaw" / "lcm.db"
QMD_INDEX = Path.home() / ".cache" / "qmd" / "index.sqlite"

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def diagnose():
    """Diagnose what's broken"""
    issues = []

    # Check workspace
    if not WORKSPACE.exists():
        issues.append({"layer": "workspace", "severity": "critical", "issue": "Workspace directory missing"})
    elif not MEMORY_FILE.exists():
        issues.append({"layer": "workspace", "severity": "critical", "issue": "MEMORY.md missing"})
    elif MEMORY_FILE.stat().st_size == 0:
        issues.append({"layer": "workspace", "severity": "critical", "issue": "MEMORY.md is empty"})

    if not DAILY_DIR.exists():
        issues.append({"layer": "workspace", "severity": "high", "issue": "Daily directory missing"})

    # Check LCM
    if not LCM_DB.exists():
        issues.append({"layer": "lcm", "severity": "critical", "issue": "LCM database missing"})
    else:
        try:
            conn = sqlite3.connect(str(LCM_DB))
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM messages")
            count = cursor.fetchone()[0]
            conn.close()
            if count == 0:
                issues.append({"layer": "lcm", "severity": "high", "issue": "LCM database empty"})
        except sqlite3.Error as e:
            issues.append({"layer": "lcm", "severity": "critical", "issue": f"LCM database corrupt: {e}"})

    # Check QMD
    if QMD_INDEX.exists():
        try:
            conn = sqlite3.connect(str(QMD_INDEX))
            conn.close()
        except sqlite3.Error as e:
            issues.append({"layer": "qmd", "severity": "medium", "issue": f"QMD index corrupt: {e}"})

    # Check config
    if OPENCLAW_CONFIG.exists():
        try:
            with open(OPENCLAW_CONFIG, "r") as f:
                config = json.load(f)
            if config.get("plugins", {}).get("slots", {}).get("contextEngine") != "lossless-claw":
                issues.append({"layer": "config", "severity": "medium", "issue": "lossless-claw not configured as context engine"})
        except json.JSONDecodeError as e:
            issues.append({"layer": "config", "severity": "critical", "issue": f"openclaw.json corrupt: {e}"})

    return issues

def backup_corrupted(backup_dir, force=False):
    """Backup corrupted files before recovery"""

    if not backup_dir.exists():
        backup_dir.mkdir(parents=True)

    backed_up = []

    # Backup LCM if corrupt
    if LCM_DB.exists():
        try:
            conn = sqlite3.connect(str(LCM_DB))
            conn.close()
        except:
            target = backup_dir / "lcm.db.corrupt"
            shutil.copy2(LCM_DB, target)
            backed_up.append(f"Backed up corrupt LCM: {target}")

    # Backup config if corrupt
    if OPENCLAW_CONFIG.exists():
        try:
            with open(OPENCLAW_CONFIG, "r") as f:
                json.load(f)
        except:
            target = backup_dir / "openclaw.json.corrupt"
            shutil.copy2(OPENCLAW_CONFIG, target)
            backed_up.append(f"Backed up corrupt config: {target}")

    # Backup MEMORY.md if empty/corrupt
    if MEMORY_FILE.exists() and MEMORY_FILE.stat().st_size == 0:
        target = backup_dir / "MEMORY.md.empty"
        shutil.copy2(MEMORY_FILE, target)
        backed_up.append(f"Backed up empty MEMORY.md: {target}")

    return backed_up

def recover_workspace():
    """Recover workspace layer"""
    results = []

    # Create directory structure
    if not WORKSPACE.exists():
        WORKSPACE.mkdir(parents=True)
        results.append("Created workspace directory")

    if not DAILY_DIR.exists():
        DAILY_DIR.mkdir(parents=True)
        results.append("Created daily directory")

    # Create MEMORY.md if missing
    if not MEMORY_FILE.exists() or MEMORY_FILE.stat().st_size == 0:
        template = '''# MEMORY.md — Long-Term Memory

> **Recovered:** {date}
> **Note:** This file was recreated after corruption. Previous content may be lost.

---

## Quick Reference

- **Daily files:** `memory/daily/YYYY/MM/DD.md`
- **LCM database:** `~/.openclaw/lcm.db`

---

## Recovery Notes

*Document any context you remember about previous sessions.*

---

*This file is your curated memory. Rebuild it as you work.*
'''
        with open(MEMORY_FILE, "w") as f:
            f.write(template.format(date=get_timestamp()))
        results.append("Created MEMORY.md (recovery template)")

    # Create supporting files if missing
    supporting = {
        "AGENTS.md": "# AGENTS.md — Agent Instructions\n\nSee memory-architect skill for setup.\n",
        "HEARTBEAT.md": "# HEARTBEAT.md\n\n## Daily TODO Review\nCheck `TODO.md` once per day.\n",
        "TODO.md": f"# TODO.md — Action Items\n\n*Recovered: {get_timestamp()}*\n\n---\n\n## Active Items\n\n*(None yet)*\n",
    }

    for fname, content in supporting.items():
        fpath = WORKSPACE / fname
        if not fpath.exists():
            with open(fpath, "w") as f:
                f.write(content)
            results.append(f"Created {fname}")

    return results

def recover_lcm():
    """Recover LCM layer"""
    results = []

    # If DB missing, it will be created by plugin on next startup
    if not LCM_DB.exists():
        results.append("LCM database missing — will be created by lossless-claw plugin on restart")
        return results

    # Try to repair
    try:
        conn = sqlite3.connect(str(LCM_DB))
        cursor = conn.cursor()

        # Check integrity
        cursor.execute("PRAGMA integrity_check")
        integrity = cursor.fetchone()[0]

        if integrity != "ok":
            results.append(f"Integrity check: {integrity}")
            # Try to recover
            cursor.execute("PRAGMA wal_checkpoint(TRUNCATE)")
            results.append("Attempted WAL checkpoint")
        else:
            results.append("Database integrity OK")

        conn.close()
    except sqlite3.Error as e:
        results.append(f"Database error: {e}")
        results.append("Recommend: Delete lcm.db and let plugin recreate it")

    return results

def recover_qmd():
    """Recover QMD layer"""
    results = []

    # Check if qmd is installed
    check = subprocess.run(["which", "qmd"], capture_output=True, text=True)
    if check.returncode != 0:
        results.append("QMD not installed — skipping")
        return results

    # Rebuild index if corrupt
    if QMD_INDEX.exists():
        try:
            conn = sqlite3.connect(str(QMD_INDEX))
            conn.close()
            results.append("QMD index OK")
        except:
            results.append("QMD index corrupt — rebuilding...")
            subprocess.run(["qmd", "update"], capture_output=True)
            results.append("QMD index rebuilt")
    else:
        results.append("QMD index missing — will be created on next 'qmd update'")

    return results

def recover_config():
    """Recover OpenClaw configuration"""
    results = []

    if not OPENCLAW_CONFIG.exists():
        results.append("Config missing — OpenClaw will create default on restart")
        return results

    try:
        with open(OPENCLAW_CONFIG, "r") as f:
            config = json.load(f)

        # Ensure lossless-claw is configured
        modified = False

        if "plugins" not in config:
            config["plugins"] = {}

        if config["plugins"].get("slots", {}).get("contextEngine") != "lossless-claw":
            if "slots" not in config["plugins"]:
                config["plugins"]["slots"] = {}
            config["plugins"]["slots"]["contextEngine"] = "lossless-claw"
            modified = True
            results.append("Set contextEngine to lossless-claw")

        if "lossless-claw" not in config["plugins"].get("entries", {}):
            if "entries" not in config["plugins"]:
                config["plugins"]["entries"] = {}
            config["plugins"]["entries"]["lossless-claw"] = {
                "enabled": True,
                "config": {
                    "freshTailCount": 32,
                    "contextThreshold": 0.75,
                    "incrementalMaxDepth": -1
                }
            }
            modified = True
            results.append("Added lossless-claw configuration")

        if modified:
            with open(OPENCLAW_CONFIG, "w") as f:
                json.dump(config, f, indent=2)
            results.append("Config updated")

    except json.JSONDecodeError as e:
        results.append(f"Config corrupt: {e}")
        results.append("Recommend: Run 'openclaw configure' to regenerate")

    return results

def main():
    parser = argparse.ArgumentParser(description="Recover OpenClaw memory architecture")
    parser.add_argument("--backup-dir", type=str, help="Backup directory for corrupted files")
    parser.add_argument("--force", action="store_true", help="Proceed without confirmation")
    args = parser.parse_args()

    print(f"\n{'='*60}")
    print(f"Memory Architecture Recovery — {get_timestamp()}")
    print(f"{'='*60}\n")

    # Diagnose
    print("Step 1: Diagnosis")
    print("-" * 40)
    issues = diagnose()

    if not issues:
        print("  No critical issues found.")
        print("  Run 'audit_memory.py' for a full health check.")
        return 0

    critical = [i for i in issues if i["severity"] == "critical"]
    high = [i for i in issues if i["severity"] == "high"]

    print(f"  Found {len(critical)} critical, {len(high)} high severity issues:")
    for i in issues:
        print(f"    [{i['severity'].upper()}] {i['layer']}: {i['issue']}")

    # Confirm
    if not args.force:
        print(f"\n  Proceed with recovery? [y/N] ", end="", flush=True)
        response = input().lower()
        if response != "y":
            print("  Aborted.")
            return 1

    # Backup
    print(f"\nStep 2: Backup")
    print("-" * 40)
    backup_dir = Path(args.backup_dir) if args.backup_dir else Path.home() / f"memory-backup-{get_timestamp().replace(' ', '-').replace(':', '')}"
    backed_up = backup_corrupted(backup_dir)
    if backed_up:
        print(f"  Backup directory: {backup_dir}")
        for b in backed_up:
            print(f"  {b}")
    else:
        print("  No corrupted files to backup")

    # Recover each layer
    print(f"\nStep 3: Recovery")
    print("-" * 40)

    print("\n  Layer 1: Workspace")
    results = recover_workspace()
    for r in results:
        print(f"    ✓ {r}")

    print("\n  Layer 2: LCM")
    results = recover_lcm()
    for r in results:
        print(f"    ✓ {r}")

    print("\n  Layer 3: QMD")
    results = recover_qmd()
    for r in results:
        print(f"    ✓ {r}")

    print("\n  Configuration")
    results = recover_config()
    for r in results:
        print(f"    ✓ {r}")

    print(f"\n{'='*60}")
    print("Recovery complete.")
    print("\nNext steps:")
    print("  1. Restart OpenClaw: 'openclaw gateway restart'")
    print("  2. Run audit: 'python3 audit_memory.py'")
    print("  3. Review and update MEMORY.md with any remembered context")
    print(f"{'='*60}\n")

    return 0

if __name__ == "__main__":
    sys.exit(main())
