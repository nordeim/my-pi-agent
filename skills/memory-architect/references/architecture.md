# Memory Architecture Reference

## Overview

OpenClaw's memory system uses a 3-layer architecture for persistent context:

```
┌─────────────────────────────────────────────────────────────┐
│                     Layer 1: Workspace                       │
│  MEMORY.md + daily files + supporting files                  │
│  (Manual file-based, human-readable)                         │
├─────────────────────────────────────────────────────────────┤
│                     Layer 2: LCM                              │
│  Lossless Context Management (SQLite)                        │
│  (Automatic compaction, summary DAG, retrieval tools)        │
├─────────────────────────────────────────────────────────────┤
│                     Layer 3: QMD                              │
│  Quick Markdown Search (semantic index)                      │
│  (BM25 + vector search + LLM reranking)                      │
└─────────────────────────────────────────────────────────────┘
```

## Layer 1: Workspace Files

### MEMORY.md
- **Location:** `~/.openclaw/workspace/MEMORY.md`
- **Purpose:** Curated long-term memory (distilled wisdom, decisions, patterns)
- **Format:** Markdown, human-editable
- **When to update:** Significant learnings, decisions, completed work

### Daily Files
- **Location:** `~/.openclaw/workspace/memory/daily/YYYY/MM/DD.md`
- **Purpose:** Raw session logs, task progress, decisions made
- **Format:** Markdown, auto-created but human-editable
- **Lifecycle:** Distilled into MEMORY.md periodically

### Supporting Files
| File | Purpose |
|------|---------|
| `AGENTS.md` | Agent behavior rules |
| `SOUL.md` | Persona and tone |
| `USER.md` | Human profile |
| `HEARTBEAT.md` | Periodic check instructions |
| `TODO.md` | Action items |

## Layer 2: LCM (Lossless Context Management)

### What It Is
Plugin that provides lossless conversation compaction via summary DAG (Directed Acyclic Graph).

### Key Concepts
- **Summary DAG:** Messages → Summaries → Higher-level summaries
- **Fresh Tail:** Recent messages kept uncompressed (configurable)
- **Incremental Compaction:** Summaries updated, not recreated

### Configuration
```json
{
  "plugins": {
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
  }
}
```

### Recommended Settings
| Parameter | Recommended | Purpose |
|-----------|-------------|---------|
| `freshTailCount` | 32 | Messages kept uncompressed |
| `contextThreshold` | 0.75 | Trigger compaction at 75% context |
| `incrementalMaxDepth` | -1 | Unlimited summary depth |

### Session Idle Reset
Pair LCM with extended session idle reset:
```json
{
  "session": {
    "reset": {
      "mode": "idle",
      "idleMinutes": 10080
    }
  }
}
```
(10,080 minutes = 7 days)

### Database
- **Location:** `~/.openclaw/lcm.db`
- **Tables:**
  - `conversations` — Conversation metadata
  - `messages` — Raw messages
  - `summaries` — Compacted summaries (DAG nodes)
  - `files` — Stored file references

## Layer 3: QMD (Quick Markdown Search)

### What It Is
Local semantic search engine for markdown files with hybrid retrieval.

### How It Works
1. **BM25** — Fast keyword matching
2. **Vector Embeddings** — Semantic similarity
3. **LLM Reranking** — Context-aware scoring

### Installation
```bash
npm install -g @tobilu/qmd
```

### Collections
Standard collections for OpenClaw workspace:
```bash
qmd collection add daily ~/.openclaw/workspace/memory/daily --pattern "**/*.md"
qmd collection add skills ~/.openclaw/workspace/skills --pattern "**/*.md"
qmd collection add system ~/.openclaw --pattern "*.md"
```

### Index Location
`~/.cache/qmd/index.sqlite`

### MCP Server
QMD can run as an MCP server for agent integration:
```bash
qmd mcp --http --port 8181
```

Health check: `curl http://127.0.0.1:8181/health`

## Verification Commands

### Check Workspace
```bash
wc -l ~/.openclaw/workspace/MEMORY.md
ls ~/.openclaw/workspace/memory/daily/*/*/
```

### Check LCM
```bash
sqlite3 ~/.openclaw/lcm.db "SELECT COUNT(*) FROM messages; SELECT COUNT(*) FROM summaries;"
```

### Check QMD
```bash
qmd status
qmd collection list
```

## Common Issues

### LCM Database Empty
- Plugin not enabled → Check `openclaw.json`
- Plugin error → Check gateway logs

### Daily Files Not Created
- Directory missing → Run bootstrap script
- Permissions → Check workspace ownership

### QMD Index Stale
- Run `qmd update` to reindex
- Check collection paths exist

## Recovery Priorities

When recovering from corruption:

1. **Config first** — Without config, plugin won't load
2. **Workspace second** — MEMORY.md is irreplaceable (backup!)
3. **LCM third** — Database can be rebuilt (but history lost)
4. **QMD last** — Index is always rebuildable from source files
