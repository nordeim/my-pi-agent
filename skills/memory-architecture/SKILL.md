---
name: memory-architecture
description: OpenClaw memory system architecture, setup guide, and troubleshooting reference. Use when configuring memory on a new machine, diagnosing memory issues after updates, or understanding how workspace files, LCM, and QMD work together.
version: 1.0.0
author: trusty-pal
tags: [memory, architecture, setup, lcm, qmd, troubleshooting]
---

# OpenClaw Memory Architecture

## What It Is

A **three-layer memory system** where each layer handles a different kind of "remembering." None of them replace each other — they're complementary.

```
┌─────────────────────────────────────────────────────────────┐
│  LAYER 1: Workspace Files (Markdown)                        │
│  Human-readable source of truth. What you'd read if you     │
│  opened the workspace in an editor.                         │
├─────────────────────────────────────────────────────────────┤
│  LAYER 2: LCM — Lossless Context Management (Plugin)        │
│  Every conversation message in SQLite. Summaries form a     │
│  DAG. Tools for recalling compacted context.                │
├─────────────────────────────────────────────────────────────┤
│  LAYER 3: QMD — Semantic Search Engine (Sidecar)            │
│  BM25 + vector embeddings + reranking over workspace        │
│  markdown files. Answers "what do I know about X?"          │
└─────────────────────────────────────────────────────────────┘
```

## The Three Layers

### Layer 1: Workspace Markdown Files

**What:** Plain text files that are the source of truth for agent memory.

**Why:** Markdown is portable, human-readable, git-friendly, and survives system updates. If everything else breaks, these files still work.

**Files:**

| File | Purpose | Loaded When |
|------|---------|-------------|
| `MEMORY.md` | Curated long-term memory. Distilled wisdom, patterns, preferences, operational notes. | Main session only (security) |
| `memory/daily/YYYY/MM/DD.md` | Daily notes. Raw session logs, decisions, tasks, observations. | Session start (today + yesterday) |
| `memory/context/active/*.yml` | Active task tracking, current focus, blockers. | As needed |
| `memory/reference/*.md` | Stable reference docs (WHOAMI, PRD, architecture). | As needed |
| `memory/projects/_context.yml` | Project tracking (empty by default). | As needed |

**Security rule:** MEMORY.md is ONLY loaded in main session (direct chat with owner). Never in group chats, Discord, or shared contexts.

**Daily note format (QMD hierarchical):**
```markdown
# 2026-03-15 — Daily Notes

## Morning
- What happened, decisions made

## Afternoon
- Tasks completed, issues encountered

## Notes
- Things to remember
```

**When to write:**
- Decisions and preferences → `MEMORY.md`
- Day-to-day context → `memory/daily/YYYY/MM/DD.md`
- Someone says "remember this" → write it down immediately
- Lessons learned → update `MEMORY.md`

---

### Layer 2: LCM — Lossless Context Management

**What:** A plugin (`@martian-engineering/lossless-claw` v0.3.0) that replaces OpenClaw's default compaction. Instead of throwing away old messages, it persists everything in SQLite and builds a summary DAG.

**Why:** Default compaction is lossy — older messages get summarized and the originals are lost. LCM keeps every raw message and creates a navigable tree of summaries. The agent can drill into any summary to recover original details.

**How it works:**
1. Every message → stored in `~/.openclaw/lcm.db` (SQLite)
2. Messages grouped into chunks → summarized by the LLM
3. Summaries form a DAG (directed acyclic graph) — parent summaries contain child summaries
4. Each turn: LCM assembles context from summaries + recent raw messages (the "fresh tail")
5. Tools let the agent search and expand compacted history

**Database location:** `~/.openclaw/lcm.db`

**Tools provided:**
- `lcm_grep` — Search compacted history by regex or full-text. Returns snippets with IDs.
- `lcm_describe` — Inspect a specific summary by ID. Cheap, no sub-agent.
- `lcm_expand` — Deep recall. Spawns sub-agent, expands DAG, returns answer with citations.
- `lcm_expand_query` — Focused question against expanded summaries. Best for precision questions.

**Configuration (in `openclaw.json`):**
```json5
{
  plugins: {
    allow: ["lossless-claw", "telegram"],
    slots: {
      contextEngine: "lossless-claw"  // THIS is what activates LCM
    },
    entries: {
      "lossless-claw": {
        enabled: true,
        config: {
          freshTailCount: 32,         // Raw messages kept unsummarized
          contextThreshold: 0.75,     // When to trigger compaction (0-1)
          incrementalMaxDepth: -1     // -1 = unlimited summary depth
        }
      }
    }
  },
  session: {
    reset: {
      mode: "idle",
      idleMinutes: 10080              // 7 days — pair with LCM's long memory
    }
  }
}
```

**Key settings explained:**
- `contextThreshold: 0.75` — LCM compacts when context is 75% full. Lower = more aggressive, higher = more context before compaction.
- `freshTailCount: 32` — Last 32 messages always stay raw. Higher = more context preserved verbatim, but more tokens per turn.
- `incrementalMaxDepth: -1` — Unlimited summary nesting. Set to a number to limit DAG depth.
- `session.reset.idleMinutes: 10080` — Session stays alive for 7 days of inactivity. LCM's strength is long-term memory, so don't reset sessions too aggressively.

**Log verification:**
```
[lcm] Plugin loaded (enabled=true, db=/home/pete/.openclaw/lcm.db, threshold=0.75)
```

---

### Layer 3: QMD — Semantic Search Engine

**What:** A local-first search sidecar that indexes workspace markdown files and provides semantic search via BM25 + vector embeddings + LLM reranking.

**Why:** `memory_search` needs to find relevant context even when wording differs. "router setup" should match notes about "network configuration." QMD provides this with local models — no API calls needed.

**How it works:**
1. QMD watches `MEMORY.md` + `memory/**/*.md` for changes
2. Files are chunked (~400 tokens, 80-token overlap) and embedded
3. Search combines BM25 (keyword) + vector similarity + reranking
4. Results returned as snippets with file paths and line ranges

**QMD binary:** `/usr/bin/qmd` (installed separately, not part of OpenClaw)

**Collections (configured):**

| Collection | Path | Purpose |
|------------|------|---------|
| `daily` | `qmd://daily/` | Daily notes with hierarchical context |
| `system` | `qmd://system/` | Gateway, auth, cron configuration |
| `projects` | `qmd://projects/` | Project tracking |
| `skills` | `qmd://skills/` | OpenClaw skill documentation |
| `reference` | `qmd://reference/` | WHOAMI, PRD, architecture guides |

**Index location:** `~/.cache/qmd/index.sqlite`

**Commands:**
```bash
qmd status                              # Check index status
qmd search "keyword" -c daily           # Fast BM25 keyword search
qmd query "concept" -c daily            # Hybrid (BM25 + vectors + rerank)
qmd vsearch "concept" -c daily          # Semantic vector search only
qmd get "daily/2026/03/15.md"           # Retrieve specific file
qmd ls daily                            # List files in collection
qmd update                              # Refresh file index
qmd embed                               # Regenerate embeddings
```

**Note:** QMD index can go stale. If files were added/changed but QMD wasn't updated, `memory_search` won't find them. Run `qmd update && qmd embed` after significant file changes.

**Models (auto-downloaded on first use):**
- Embedding: `embeddinggemma-300M-GGUF`
- Reranking: `Qwen3-Reranker-0.6B-Q8_0-GGUF`
- Query expansion: `qmd-query-expansion-1.7B-gguf`

---

## How the Layers Work Together

**Typical session flow:**

1. **Session starts** → OpenClaw reads `SOUL.md`, `USER.md`, `memory/daily/YYYY/MM/DD.md` (today + yesterday), and `MEMORY.md` (main session only)
2. **Agent responds** → LCM stores every message in SQLite, builds summaries as context grows
3. **Agent needs past info** → Uses `lcm_grep`/`lcm_expand` for conversation history, `memory_search` for workspace knowledge
4. **Context nears limit** → LCM compacts older messages into summaries, keeps fresh tail raw
5. **Session ends** → Agent writes important notes to daily files and/or MEMORY.md

**Which tool to use when:**

| Need | Tool | Layer |
|------|------|-------|
| "What did we discuss about X?" | `lcm_grep` or `lcm_expand_query` | LCM |
| "What do I know about X?" | `memory_search` | QMD |
| "Show me the exact conversation" | `lcm_expand` with summary IDs | LCM |
| "Read my notes from March 10" | `memory_get` | Workspace files |
| "What's in MEMORY.md about Y?" | `memory_search` then `memory_get` | QMD + Files |
| Search compacted conversation details | `lcm_grep` → `lcm_expand` | LCM |
| Find a config value or decision | `memory_search` → `memory_get` | QMD + Files |

---

## Setup: New Machine Installation

### Prerequisites
- OpenClaw installed and configured
- Node.js 22+
- An LLM provider configured (for LCM summarization)

### Step 1: Install LCM Plugin

```bash
openclaw plugins install @martian-engineering/lossless-claw
```

This installs the plugin and enables it. Verify with:
```bash
openclaw plugins list | grep lossless
```

### Step 2: Configure Context Engine Slot

Edit `~/.openclaw/openclaw.json` (or use `gateway config.patch`):

```json5
{
  plugins: {
    slots: {
      contextEngine: "lossless-claw"
    },
    allow: ["lossless-claw", "telegram"],  // Add your channel plugins
    entries: {
      "lossless-claw": {
        enabled: true,
        config: {
          freshTailCount: 32,
          contextThreshold: 0.75,
          incrementalMaxDepth: -1
        }
      }
    }
  }
}
```

### Step 3: Tune Session Reset

```json5
{
  session: {
    reset: {
      mode: "idle",
      idleMinutes: 10080  // 7 days
    }
  }
}
```

### Step 4: Set Up Workspace Memory Files

Create the directory structure:
```bash
mkdir -p ~/.openclaw/workspace/memory/daily/$(date +%Y)/$(date +%m)
mkdir -p ~/.openclaw/workspace/memory/context/active
mkdir -p ~/.openclaw/workspace/memory/reference
mkdir -p ~/.openclaw/workspace/memory/projects
```

Create `_context.yml` files for QMD collections:
```bash
# memory/daily/_context.yml
cat > ~/.openclaw/workspace/memory/daily/_context.yml << 'EOF'
context: |
  Daily raw notes capture session transcripts, quick captures, and timestamps.
  Synthesized weekly into MEMORY.md for long-term retention.
  Format: Conversations, decisions, tasks, observations.
EOF

# memory/daily/YYYY/_context.yml (year context)
cat > ~/.openclaw/workspace/memory/daily/$(date +%Y)/_context.yml << EOF
context: |
  Year $(date +%Y): Active year. Notes here are most current and relevant.
  Prioritize over older years unless querying historical context.
EOF
```

Create MEMORY.md:
```bash
cat > ~/.openclaw/workspace/MEMORY.md << 'EOF'
# MEMORY.md — Curated Long-Term Memory

> **Purpose:** Distilled wisdom, patterns, preferences, and operational notes.
> **Security:** ONLY loaded in main session (direct chats). Never in shared contexts.

---

## [Your sections here]

---
*Created: $(date +%Y-%m-%d)*
EOF
```

### Step 5: Install and Configure QMD

```bash
# Install QMD (if not already installed)
bun install -g https://github.com/tobi/qmd
# or download a release binary

# Verify
qmd --version
```

QMD will auto-configure its collections on first run. Verify:
```bash
qmd status
```

### Step 6: Restart OpenClaw

```bash
openclaw gateway restart
```

### Step 7: Validate

Run these checks:
```bash
# 1. LCM plugin loaded
openclaw status | grep -i lcm
# Expected: [lcm] Plugin loaded (enabled=true, db=..., threshold=0.75)

# 2. Context engine slot active
openclaw status | grep -i "context engine"
# Or check config:
cat ~/.openclaw/openclaw.json | grep contextEngine

# 3. LCM database exists
ls -la ~/.openclaw/lcm.db
# Expected: file exists, non-zero size

# 4. QMD index healthy
qmd status
# Expected: collections listed, files indexed, vectors embedded

# 5. Memory files accessible
ls -la ~/.openclaw/workspace/MEMORY.md
ls -la ~/.openclaw/workspace/memory/daily/

# 6. Session reset configured
openclaw status | grep -i "idle"
# Or check config:
cat ~/.openclaw/openclaw.json | grep idleMinutes
```

Send a test message and verify:
- LCM stores it: `lcm_grep` with a keyword from your message
- QMD can find it (after update): `memory_search` with a related query

---

## Troubleshooting

### LCM not active (compacting normally instead of losslessly)

**Symptom:** Messages are being lost after compaction. No `lcm_grep` results.

**Check:**
```bash
openclaw plugins list | grep lossless
openclaw status | grep "context engine"
cat ~/.openclaw/openclaw.json | grep contextEngine
```

**Fix:** Ensure `plugins.slots.contextEngine` is set to `"lossless-claw"`:
```json5
{ plugins: { slots: { contextEngine: "lossless-claw" } } }
```
Then restart: `openclaw gateway restart`

### QMD search returns stale or no results

**Symptom:** `memory_search` doesn't find recent notes.

**Check:**
```bash
qmd status
# Look at "Updated: X ago" — if > 1 day, index is stale
```

**Fix:**
```bash
qmd update && qmd embed
```

### Built-in memory search shows 0 files

**Symptom:** `openclaw status` shows "Memory: 0 files · 0 chunks · dirty"

**Diagnosis:** This is normal if using QMD as the search backend. The built-in SQLite index (`~/.openclaw/memory/main.sqlite`) may be empty while QMD handles indexing. Check if `memory_search` actually works despite the 0-file count.

**If memory_search truly doesn't work:** Ensure either:
- QMD is installed and configured (`qmd status` works)
- Or a remote embedding provider is configured (`agents.defaults.memorySearch.provider`)

### Daily note missing for today

**Symptom:** No `memory/daily/YYYY/MM/DD.md` for current date.

**Fix:** Create it:
```bash
mkdir -p ~/.openclaw/workspace/memory/daily/$(date +%Y)/$(date +%m)
cat > ~/.openclaw/workspace/memory/daily/$(date +%Y)/$(date +%m)/$(date +%d).md << EOF
# $(date +%Y-%m-%d) — Daily Notes

## $(date +%H:%M)
- Session started
EOF
```

**Prevention:** Add to AGENTS.md session protocol: "Create today's daily note if it doesn't exist."

### LCM database too large

**Symptom:** `~/.openclaw/lcm.db` is growing unexpectedly.

**Check:**
```bash
sqlite3 ~/.openclaw/lcm.db "SELECT COUNT(*) FROM messages;"
sqlite3 ~/.openclaw/lcm.db "SELECT COUNT(*) FROM summaries;"
ls -lh ~/.openclaw/lcm.db
```

**Diagnosis:** LCM keeps every message by design (lossless). Over months of use, this grows. 146 messages ≈ 1MB. Thousands of messages will be proportionally larger.

**Mitigation:** If needed, old conversations can be archived by exporting and removing from the database. But this defeats LCM's purpose — only do this if storage is truly constrained.

### Old flat memory files still exist

**Symptom:** Files like `memory/2026-03-03.md` exist alongside `memory/daily/2026/03/03.md`.

**Fix:** Verify content is in the hierarchical location, then remove old flat files:
```bash
# Check content exists in new location
cat memory/daily/2026/03/03.md
# Remove old flat file
rm memory/2026-03-03.md
```

### Session resets too aggressively

**Symptom:** Conversation context lost after short idle periods.

**Check:**
```bash
cat ~/.openclaw/openclaw.json | grep idleMinutes
```

**Fix:** Set to 10080 (7 days) to pair with LCM's long-term memory:
```json5
{ session: { reset: { mode: "idle", idleMinutes: 10080 } } }
```

### Gateway restart clears cron jobs

**Symptom:** Cron jobs disappear after gateway restart.

**Diagnosis:** OpenClaw cron jobs are stored in the running gateway's memory. They persist across restarts in the config, but if the config was modified externally (not through OpenClaw), jobs may be lost.

**Fix:** Use system cron for critical jobs (like daily ping) instead of OpenClaw cron. System cron is independent of OpenClaw's lifecycle.

---

## Architecture Decisions Log

### Why LCM instead of default compaction?

Default compaction summarizes older messages and discards originals. For a long-running personal assistant, this means:
- Past decisions and context are permanently lost
- No way to recover specific details from weeks ago
- Summaries can miss nuance

LCM solves this by keeping everything and providing tools to navigate the history.

### Why QMD instead of built-in memory search?

The built-in memory search works, but QMD provides:
- Local models (no API dependency for embeddings)
- BM25 + vector + reranking (better recall)
- Hierarchical collections (structured context)
- Offline operation

### Why 7-day session idle?

LCM's strength is long-term memory across many sessions. Short session resets would waste this by starting fresh. 7 days gives enough time for natural conversation gaps while keeping sessions reasonably bounded.

### Why threshold 0.75?

Default 0.75 means LCM compacts when context is 75% full. This balances:
- Enough raw context for the model to work with (not too aggressive)
- Early enough compaction to avoid context overflow (not too late)

Adjust based on your model's context window and typical conversation length.

---

## Health Check Command

Run this to validate the entire memory system:

```bash
#!/bin/bash
echo "=== Memory Architecture Health Check ==="

echo -e "\n[1/6] LCM Plugin"
openclaw plugins list 2>/dev/null | grep -i "lossless" || echo "  ❌ LCM not found"

echo -e "\n[2/6] Context Engine Slot"
grep -q "contextEngine" ~/.openclaw/openclaw.json 2>/dev/null && echo "  ✅ Configured" || echo "  ❌ Not configured"

echo -e "\n[3/6] LCM Database"
[ -f ~/.openclaw/lcm.db ] && echo "  ✅ Exists ($(du -h ~/.openclaw/lcm.db | cut -f1))" || echo "  ❌ Missing"

echo -e "\n[4/6] QMD Index"
qmd status 2>/dev/null | grep -E "Total:|Vectors:" || echo "  ❌ QMD not available"

echo -e "\n[5/6] Memory Files"
[ -f ~/.openclaw/workspace/MEMORY.md ] && echo "  ✅ MEMORY.md exists" || echo "  ❌ MEMORY.md missing"
TODAY=$(date +%Y/%m/%d)
[ -f ~/.openclaw/workspace/memory/daily/$TODAY.md ] && echo "  ✅ Today's daily note exists" || echo "  ⚠️  Today's daily note missing"

echo -e "\n[6/6] Session Reset"
grep "idleMinutes" ~/.openclaw/openclaw.json 2>/dev/null || echo "  ⚠️  idleMinutes not set"

echo -e "\n=== Done ==="
```

---

## Related Skills

- `context-anchor` — Recover from context compaction by scanning memory files
- `session-logs` — Search and analyze session logs using jq
- `trustskill` — Security scanner for OpenClaw skills

---

*Last updated: 2026-03-15*
