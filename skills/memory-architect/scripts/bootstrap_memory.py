#!/usr/bin/env python3
"""
Memory Architecture Bootstrap Script

Bootstraps the 3-layer OpenClaw memory system on a new machine:
- Layer 1: Creates workspace files (MEMORY.md, daily structure, supporting files)
- Layer 2: Configures lossless-claw plugin in openclaw.json
- Layer 3: Sets up QMD collections and index

Usage:
    python3 bootstrap_memory.py [--dry-run] [--skip-qmd]

Options:
    --dry-run    Show what would be done without making changes
    --skip-qmd   Skip QMD setup (use if not installed)
"""

import argparse
import json
import os
import shutil
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

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def create_directory_structure(dry_run=False):
    """Create workspace directory structure"""
    dirs = [
        WORKSPACE,
        WORKSPACE / "memory",
        DAILY_DIR,
        WORKSPACE / "skills",
        WORKSPACE / "scripts",
    ]

    created = []
    for d in dirs:
        if not d.exists():
            if dry_run:
                created.append(f"[DRY-RUN] Would create: {d}")
            else:
                d.mkdir(parents=True, exist_ok=True)
                created.append(f"Created: {d}")
    return created

def create_memory_md(dry_run=False):
    """Create MEMORY.md template"""
    if MEMORY_FILE.exists():
        return [f"Skipped: {MEMORY_FILE} already exists"]

    template = '''# MEMORY.md — Long-Term Memory

> **Purpose:** Distilled wisdom, patterns, preferences, and operational notes.
> **Security:** Only load in main session (direct chats). Never in shared contexts.
> **Last Updated:** {date}

---

## Quick Reference

- **Daily files:** `memory/daily/YYYY/MM/DD.md`
- **LCM database:** `~/.openclaw/lcm.db`
- **QMD index:** `~/.cache/qmd/index.sqlite`

---

## Key Decisions

*Document significant decisions and their rationale here.*

---

## Active Projects

*Track ongoing work and context.*

---

## Known Issues & Constraints

*Document limitations and gotchas.*

---

*This file is your curated memory. Update it regularly.*
'''

    if dry_run:
        return [f"[DRY-RUN] Would create: {MEMORY_FILE}"]
    else:
        with open(MEMORY_FILE, "w") as f:
            f.write(template.format(date=get_timestamp()))
        return [f"Created: {MEMORY_FILE}"]

def create_supporting_files(dry_run=False):
    """Create AGENTS.md, SOUL.md, USER.md, HEARTBEAT.md, TODO.md"""

    files = {
        "AGENTS.md": '''# AGENTS.md — Agent Instructions

This folder is home. Treat it that way.

## First Run
If `BOOTSTRAP.md` exists, read it, then delete it.

## Every Session
1. Read `SOUL.md` — who you are
2. Read `USER.md` — who you're helping
3. Read today's daily file: `memory/daily/YYYY/MM/DD.md`

## Memory
- Daily notes: `memory/daily/YYYY/MM/DD.md`
- Long-term: `MEMORY.md` — curated, distilled learnings

## Safety
- Private things stay private.
- When in doubt, ask.
''',
        "SOUL.md": '''# SOUL.md — Who You Are

You're an AI assistant. Be helpful, honest, and harmless.

## Core Principles
- Just answer. Get to the point.
- Have opinions. Not "it depends" hedging.
- Be resourceful before asking.

## Tone
Keep information tight. Let personality take up the space.

---
*Update this file as you learn who you are.*
''',
        "USER.md": '''# USER.md — About Your Human

*Learn about the person you're helping. Update this as you go.*

- **Name:** *(to be determined)*
- **Location:** *(to be determined)*
- **Interests:** *(build this over time)*

---
*The more you know, the better you can help.*
''',
        "HEARTBEAT.md": '''# HEARTBEAT.md

## Daily TODO Review
Check `TODO.md` once per day.

## Memory Maintenance
Review recent daily files. Distill significant learnings into `MEMORY.md`.
''',
        "TODO.md": '''# TODO.md — Action Items

> **Status legend:** KIV = Keep In View | IN-PROGRESS | DONE | BLOCKED

---

## Active Items
*(None yet)*

---

## Completed

---

*Created: {date}*
'''.format(date=get_timestamp()),
    }

    results = []
    for fname, content in files.items():
        fpath = WORKSPACE / fname
        if fpath.exists():
            results.append(f"Skipped: {fname} already exists")
        else:
            if dry_run:
                results.append(f"[DRY-RUN] Would create: {fname}")
            else:
                with open(fpath, "w") as f:
                    f.write(content)
                results.append(f"Created: {fname}")

    return results

def create_today_daily(dry_run=False):
    """Create today's daily file"""
    today = datetime.now()
    today_path = DAILY_DIR / str(today.year) / f"{today.month:02d}" / f"{today.day:02d}.md"

    if today_path.exists():
        return [f"Skipped: Today's file already exists: {today_path}"]

    content = f'''# {today.strftime('%Y-%m-%d')} — Daily Notes

## Session Start

*Memory architecture bootstrapped on this machine.*

---

*Add session notes as you work.*
'''

    if dry_run:
        return [f"[DRY-RUN] Would create: {today_path}"]
    else:
        today_path.parent.mkdir(parents=True, exist_ok=True)
        with open(today_path, "w") as f:
            f.write(content)
        return [f"Created: {today_path}"]

def configure_lossless_claw(dry_run=False):
    """Configure lossless-claw plugin in openclaw.json"""

    if not OPENCLAW_CONFIG.exists():
        return [f"ERROR: OpenClaw config not found at {OPENCLAW_CONFIG}"]

    results = []

    try:
        with open(OPENCLAW_CONFIG, "r") as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        return [f"ERROR: Invalid JSON in config: {e}"]

    # Check if plugins section exists
    if "plugins" not in config:
        config["plugins"] = {}

    # Configure lossless-claw
    modified = False

    # Add to allow list
    if "allow" not in config["plugins"]:
        config["plugins"]["allow"] = []
    if "lossless-claw" not in config["plugins"]["allow"]:
        config["plugins"]["allow"].append("lossless-claw")
        modified = True
        results.append("Added lossless-claw to plugins.allow")

    # Set contextEngine slot
    if config["plugins"].get("slots", {}).get("contextEngine") != "lossless-claw":
        if "slots" not in config["plugins"]:
            config["plugins"]["slots"] = {}
        config["plugins"]["slots"]["contextEngine"] = "lossless-claw"
        modified = True
        results.append("Set contextEngine slot to lossless-claw")

    # Add plugin entry with recommended config
    if "entries" not in config["plugins"]:
        config["plugins"]["entries"] = {}

    if "lossless-claw" not in config["plugins"]["entries"]:
        config["plugins"]["entries"]["lossless-claw"] = {
            "enabled": True,
            "config": {
                "freshTailCount": 32,
                "contextThreshold": 0.75,
                "incrementalMaxDepth": -1
            }
        }
        modified = True
        results.append("Added lossless-claw entry with recommended config")

    # Set session idle to 7 days
    if "session" not in config:
        config["session"] = {}
    if config["session"].get("reset", {}).get("idleMinutes") != 10080:
        if "reset" not in config["session"]:
            config["session"]["reset"] = {}
        config["session"]["reset"]["idleMinutes"] = 10080
        modified = True
        results.append("Set session idle reset to 10080 minutes (7 days)")

    if modified:
        if dry_run:
            results.insert(0, "[DRY-RUN] Would update openclaw.json:")
        else:
            with open(OPENCLAW_CONFIG, "w") as f:
                json.dump(config, f, indent=2)
            results.insert(0, "Updated openclaw.json:")
    else:
        results.append("Config already correct, no changes needed")

    return results

def setup_qmd_collections(dry_run=False):
    """Set up QMD collections"""

    # Check if qmd is available
    result = subprocess.run(["which", "qmd"], capture_output=True, text=True)
    if result.returncode != 0:
        return ["Skipped: QMD not installed"]

    results = []

    # Define collections
    collections = [
        ("daily", str(WORKSPACE / "memory" / "daily"), "**/*.md"),
        ("skills", str(WORKSPACE / "skills"), "**/*.md"),
        ("system", str(Path.home() / ".openclaw"), "*.md"),
    ]

    for name, path, pattern in collections:
        if not Path(path).exists():
            results.append(f"Skipped collection '{name}': path doesn't exist ({path})")
            continue

        # Check if collection exists
        check = subprocess.run(
            ["qmd", "collection", "list"],
            capture_output=True, text=True
        )

        if name in check.stdout:
            results.append(f"Collection '{name}' already exists")
            continue

        if dry_run:
            results.append(f"[DRY-RUN] Would add collection: {name}")
        else:
            add = subprocess.run(
                ["qmd", "collection", "add", name, path, "--pattern", pattern],
                capture_output=True, text=True
            )
            if add.returncode == 0:
                results.append(f"Added collection: {name}")
            else:
                results.append(f"Failed to add collection '{name}': {add.stderr}")

    # Update index
    if not dry_run:
        results.append("Updating QMD index...")
        subprocess.run(["qmd", "update"], capture_output=True)

    return results

def main():
    parser = argparse.ArgumentParser(description="Bootstrap OpenClaw memory architecture")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without executing")
    parser.add_argument("--skip-qmd", action="store_true", help="Skip QMD setup")
    args = parser.parse_args()

    print(f"\n{'='*60}")
    print(f"Memory Architecture Bootstrap — {get_timestamp()}")
    if args.dry_run:
        print("*** DRY RUN — No changes will be made ***")
    print(f"{'='*60}\n")

    all_results = []

    # Layer 1: Workspace files
    print("Layer 1: Workspace Files")
    print("-" * 40)

    results = create_directory_structure(dry_run=args.dry_run)
    for r in results:
        print(f"  {r}")
    all_results.extend(results)

    results = create_memory_md(dry_run=args.dry_run)
    for r in results:
        print(f"  {r}")

    results = create_supporting_files(dry_run=args.dry_run)
    for r in results:
        print(f"  {r}")

    results = create_today_daily(dry_run=args.dry_run)
    for r in results:
        print(f"  {r}")

    # Layer 2: LCM
    print("\nLayer 2: LCM Configuration")
    print("-" * 40)

    results = configure_lossless_claw(dry_run=args.dry_run)
    for r in results:
        print(f"  {r}")

    # Layer 3: QMD
    if not args.skip_qmd:
        print("\nLayer 3: QMD Setup")
        print("-" * 40)

        results = setup_qmd_collections(dry_run=args.dry_run)
        for r in results:
            print(f"  {r}")

    print(f"\n{'='*60}")
    print("Bootstrap complete.")
    if args.dry_run:
        print("Run without --dry-run to apply changes.")
    print(f"{'='*60}\n")

    return 0

if __name__ == "__main__":
    sys.exit(main())
