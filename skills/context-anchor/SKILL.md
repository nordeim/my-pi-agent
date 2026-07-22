---
name: context-anchor
version: 1.1.0
description: Recover from context compaction by scanning memory files and surfacing where you left off. Use when waking up fresh, after compaction, or when you feel lost about what you were doing. Now supports both flat (YYYY-MM-DD.md) and QMD hierarchical (daily/YYYY/MM/DD.md) memory structures.
---

# Context Anchor Skill

Helps agents recover context after compaction by scanning memory files and generating a "here's where you are" briefing.

## Why This Exists

Context compaction loses memory. Files survive. But after waking up fresh, you need to:
1. Know what you were working on
2. See decisions that were made
3. Find open loops that need closing
4. Get oriented fast

This skill automates that recovery.

---

## Quick Start

```bash
# Full briefing (default)
./scripts/anchor.sh

# Just show current task
./scripts/anchor.sh --task

# Just show active context files
./scripts/anchor.sh --active

# Just show recent decisions
./scripts/anchor.sh --decisions

# Show open loops / questions
./scripts/anchor.sh --loops

# Scan specific number of days back
./scripts/anchor.sh --days 3
```

---

## What It Scans

| Source | What It Extracts |
|--------|------------------|
| `memory/current-task.md` | Current task status, blockers, next steps |
| `memory/YYYY-MM-DD.md` | Recent daily logs (flat structure, legacy) |
| `memory/daily/YYYY/MM/DD.md` | Recent daily logs (QMD hierarchical structure) |
| `context/active/*.md` | In-progress task files |
| Daily logs | Decisions (lines with "Decision:", "Decided:", "✅") |
| Daily logs | Open loops (lines with "?", "TODO:", "Blocker:", "Need to") |

### Memory Structure Support

The script automatically detects and supports **both** memory file structures:

1. **QMD Hierarchical** (preferred): `memory/daily/2026/02/23.md`
2. **Flat** (legacy): `memory/2026-02-23.md`

When scanning, the script checks the QMD path first. If found, it uses that. Otherwise, it falls back to the flat file. This allows both systems to coexist during migration.

---

## Output Format

The script outputs a structured briefing:

```
═══════════════════════════════════════════════════════════
                    CONTEXT ANCHOR
              Where You Left Off
═══════════════════════════════════════════════════════════

📋 CURRENT TASK
───────────────────────────────────────────────────────────
[Contents of memory/current-task.md or "No current task set"]

📂 ACTIVE CONTEXT FILES
───────────────────────────────────────────────────────────
• context/active/project-name.md (updated 2h ago)
  └─ First line preview...

🎯 RECENT DECISIONS (last 2 days)
───────────────────────────────────────────────────────────
[2026-01-30] Decision: Use Cloudflare Pages for hosting
[2026-01-30] ✅ Completed email capture setup

❓ OPEN LOOPS
───────────────────────────────────────────────────────────
[2026-01-30] Need to enable SFTP on NAS
[2026-01-30] TODO: Create Product Hunt account

═══════════════════════════════════════════════════════════
```

---

## Integration with AGENTS.md

Add to your "Every Session" routine:

```markdown
## Every Session

Before doing anything else:
1. Run `./skills/context-anchor/scripts/anchor.sh` for orientation
2. Read `SOUL.md` — this is who you are
3. Read `USER.md` — this is who you're helping
...
```

Or use it manually when you feel lost about context.

---

## Customization

### Change workspace root

```bash
WORKSPACE=/path/to/workspace ./scripts/anchor.sh
```

### Change days to scan

```bash
./scripts/anchor.sh --days 5  # Scan 5 days back
```

---

## No Dependencies

Pure bash. Uses only:
- `find`, `grep`, `head`, `tail`, `date`, `stat`
- Works on macOS and Linux
- No external tools required

---

## When to Use

- **Session start**: Quick orientation on what's happening
- **After compaction**: Recover lost context
- **Feeling lost**: "Wait, what was I doing?"
- **Handoff**: Show another agent where things stand
- **Daily review**: See what decisions were made
