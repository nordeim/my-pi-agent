---
name: memory-architect
description: "Bootstrap, audit, and recover the OpenClaw 3-layer memory architecture (workspace files, LCM database, QMD semantic index). Use when: (1) Setting up memory on a new OpenClaw instance, (2) Auditing existing memory health, (3) Recovering from corruption or system crash, (4) Migrating or restructuring memory layout, (5) User asks about memory architecture setup or health. Triggers on phrases like 'bootstrap memory', 'audit memory', 'memory architecture', 'memory setup', 'LCM configuration', 'QMD setup', 'memory recovery', 'check memory health'."
---

# Memory Architect

Bootstrap, audit, and recover OpenClaw's 3-layer memory architecture.

## Architecture Overview

```
Layer 1: WORKSPACE FILES (Human-editable)
├── MEMORY.md — Long-term curated memory
├── memory/daily/YYYY/MM/DD.md — Session notes
└── Supporting: AGENTS.md, SOUL.md, USER.md, HEARTBEAT.md, TODO.md

Layer 2: LCM (Lossless Context Management)
├── SQLite database: ~/.openclaw/lcm.db
├── Full message history + summary DAG
└── Configured via lossless-claw plugin

Layer 3: QMD (Quick Markdown Search)
├── Semantic index: ~/.cache/qmd/index.sqlite
├── Collections: daily, skills, reference, etc.
└── MCP server: http://127.0.0.1:8181
```

## Operations

### Bootstrap New Instance

Set up memory architecture on a fresh OpenClaw installation:

```bash
cd ~/.openclaw/workspace/skills/memory-architect
python3 scripts/bootstrap_memory.py [--dry-run] [--skip-qmd]
```

**What it does:**
1. Creates directory structure (`memory/daily/YYYY/MM/`, `skills/`, `scripts/`)
2. Generates core files (MEMORY.md, AGENTS.md, SOUL.md, USER.md, HEARTBEAT.md, TODO.md)
3. Configures lossless-claw plugin in `openclaw.json`
4. Sets session idle timeout to 7 days (pairs with LCM)
5. Initializes QMD collections (unless `--skip-qmd`)

**After bootstrap:**
```bash
openclaw gateway restart
python3 scripts/audit_memory.py
```

### Audit Existing Setup

Check health of all three layers:

```bash
python3 scripts/audit_memory.py [--fix] [--json]
```

**Output includes:**
- Layer 1: File existence, sizes, modification dates
- Layer 2: Database integrity, message/summary counts, freshness
- Layer 3: QMD installation, index size, MCP server status
- Overall health score (0-100%)

**Options:**
- `--fix` — Create missing daily file if needed
- `--json` — Machine-readable output for automation

### Recover from Corruption

Repair after system crash or corruption:

```bash
python3 scripts/recover_memory.py [--backup-dir PATH] [--force]
```

**What it does:**
1. Diagnoses issues across all three layers
2. Backs up corrupted files before modifying
3. Checks LCM database integrity, attempts repair
4. Rebuilds QMD index from workspace files
5. Recreates missing files from templates

**After recovery:**
```bash
openclaw gateway restart
python3 scripts/audit_memory.py
```

## Configuration Reference

### LCM (lossless-claw) Plugin

Required in `~/.openclaw/openclaw.json`:

```json
{
  "plugins": {
    "allow": ["lossless-claw"],
    "slots": { "contextEngine": "lossless-claw" },
    "entries": {
      "lossless-claw": {
        "enabled": true,
        "config": {
          "freshTailCount": 32,
          "contextThreshold": 0.75,
          "incrementalMaxDepth": -1
        }
      }
    }
  },
  "session": {
    "reset": { "mode": "idle", "idleMinutes": 10080 }
  }
}
```

**Key parameters:**

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `freshTailCount` | 32 | Recent messages kept uncompressed |
| `contextThreshold` | 0.75 | Compression trigger (75% context) |
| `incrementalMaxDepth` | -1 | Unlimited summary DAG depth |
| `idleMinutes` | 10080 | Session timeout (7 days) |

### QMD Collections

Standard collections (auto-created by bootstrap):

| Collection | Pattern | Purpose |
|------------|---------|---------|
| `daily` | `memory/daily/**/*.md` | Session notes |
| `skills` | `skills/**/*.md` | Skill documentation |
| `system` | `~/.openclaw/*.md` | Config files |

**Manual commands:**
```bash
qmd status              # Check index health
qmd collection list     # Show collections
qmd update              # Rebuild index
```

## Troubleshooting

### LCM Database Not Created
**Cause:** Gateway not restarted after config change.
**Fix:** `openclaw gateway restart`

### QMD Index Empty
**Cause:** Collections not indexed.
**Fix:** `qmd update`

### Memory Files Missing
**Cause:** Bootstrap not run.
**Fix:** `python3 scripts/bootstrap_memory.py`

### Session Context Lost
**Cause:** Session idle timeout too short.
**Fix:** Ensure `idleMinutes` is 10080 in config.

## Resources

- `scripts/bootstrap_memory.py` — Fresh installation setup
- `scripts/audit_memory.py` — Health check for all layers
- `scripts/recover_memory.py` — Corruption recovery
- `references/architecture.md` — Detailed architecture docs
- `references/checklist.md` — Bootstrap/audit/recovery checklists
- `assets/` — Example templates (see Notes section)

## Quick Reference

```bash
# Bootstrap new setup
python3 scripts/bootstrap_memory.py

# Audit health
python3 scripts/audit_memory.py --fix

# Recover from crash
python3 scripts/recover_memory.py

# Verify all layers
openclaw gateway restart && python3 scripts/audit_memory.py
```

---

## Notes

### Template Files

The `assets/` directory contains example template files (`memory_md_template.md`, `daily_template.md`). These are **reference examples only** — the scripts use inline templates rather than reading from these files.

This design choice avoids file path dependencies during bootstrap/recovery scenarios where the filesystem may be partially corrupted.

If you want to customize the templates used by scripts, you must edit the inline template strings in:

- `bootstrap_memory.py` (lines 62-101 for MEMORY.md template)
- `recover_memory.py` (lines 140-164 for MEMORY.md template)
- `bootstrap_memory.py` (lines 178-195 for daily file template)
- `recover_memory.py` (lines 180-196 for daily file template)

### Verifying LCM is Active

After bootstrap or recovery, verify LCM is actually working:

```bash
# Check database exists and has recent activity
ls -lh ~/.openclaw/lcm.db

# Check plugin is configured
grep -A5 "lossless-claw" ~/.openclaw/openclaw.json

# Verify session idle is 7 days
grep -A3 '"session"' ~/.openclaw/openclaw.json
```
