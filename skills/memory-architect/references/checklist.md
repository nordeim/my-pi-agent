# Memory Architecture Checklist

## Bootstrap Checklist (New Machine)

### Prerequisites
- [ ] OpenClaw installed
- [ ] Node.js 18+ available
- [ ] Python 3.10+ available

### Layer 1: Workspace
- [ ] Create workspace directory: `mkdir -p ~/.openclaw/workspace`
- [ ] Create daily directory: `mkdir -p ~/.openclaw/workspace/memory/daily`
- [ ] Create MEMORY.md from template
- [ ] Create AGENTS.md
- [ ] Create SOUL.md
- [ ] Create USER.md
- [ ] Create HEARTBEAT.md
- [ ] Create TODO.md
- [ ] Create today's daily file

### Layer 2: LCM
- [ ] Add lossless-claw to `plugins.allow`
- [ ] Set `plugins.slots.contextEngine` to "lossless-claw"
- [ ] Add `plugins.entries.lossless-claw` with config
- [ ] Set `session.reset.idleMinutes` to 10080
- [ ] Restart OpenClaw gateway
- [ ] Verify `lcm.db` created

### Layer 3: QMD
- [ ] Install QMD: `npm install -g @tobilu/qmd`
- [ ] Create daily collection
- [ ] Create skills collection
- [ ] Run `qmd update` to build index
- [ ] (Optional) Start MCP server: `qmd mcp --http --port 8181`

### Verification
- [ ] Run audit script: `python3 audit_memory.py`
- [ ] Health score ≥ 90%

---

## Audit Checklist (Health Check)

### Workspace Layer
- [ ] MEMORY.md exists and has content
- [ ] MEMORY.md updated within reasonable time (check modified date)
- [ ] Daily directory exists
- [ ] Today's daily file exists
- [ ] Supporting files present (AGENTS.md, SOUL.md, USER.md)

### LCM Layer
- [ ] Database file exists at `~/.openclaw/lcm.db`
- [ ] Database readable (not corrupt)
- [ ] Messages table has entries
- [ ] Summaries table has entries
- [ ] Recent messages (within last 24h)
- [ ] Plugin configured in openclaw.json

### QMD Layer
- [ ] QMD installed (`which qmd`)
- [ ] Index file exists
- [ ] Collections configured
- [ ] Files indexed
- [ ] MCP server running (if used)

### Configuration
- [ ] `plugins.slots.contextEngine` = "lossless-claw"
- [ ] `plugins.entries.lossless-claw.enabled` = true
- [ ] `session.reset.idleMinutes` ≥ 10080

---

## Recovery Checklist (After Corruption)

### Step 1: Diagnosis
- [ ] Run diagnosis to identify affected layers
- [ ] Check for error messages in gateway logs
- [ ] Identify root cause (disk error, crash, etc.)

### Step 2: Backup
- [ ] Create backup directory
- [ ] Backup corrupted files before modifying
- [ ] Note what was backed up

### Step 3: Recovery (by Layer)

#### Workspace Recovery
- [ ] Restore from backup if available
- [ ] Or recreate from template
- [ ] Create missing supporting files

#### LCM Recovery
- [ ] Check database integrity (`PRAGMA integrity_check`)
- [ ] Attempt repair if corrupt
- [ ] If unrecoverable: delete and let plugin recreate

#### QMD Recovery
- [ ] Delete corrupt index
- [ ] Rebuild with `qmd update`

#### Config Recovery
- [ ] Validate JSON syntax
- [ ] Fix plugin configuration
- [ ] Restart gateway

### Step 4: Verification
- [ ] Run audit script
- [ ] Health score ≥ 80%
- [ ] Test LCM retrieval
- [ ] Test QMD search

### Step 5: Documentation
- [ ] Update MEMORY.md with recovery notes
- [ ] Log in daily file
- [ ] Note any lost context

---

## Maintenance Checklist (Periodic)

### Daily
- [ ] Check TODO.md status
- [ ] Review heartbeat (if enabled)

### Weekly
- [ ] Run audit script
- [ ] Review recent daily files
- [ ] Distill learnings to MEMORY.md

### Monthly
- [ ] Check LCM database size
- [ ] Reindex QMD: `qmd update`
- [ ] Clean up old daily files (archive, don't delete)
- [ ] Review MEMORY.md for stale content

### As Needed
- [ ] Update plugin configuration for new features
- [ ] Add new QMD collections for projects
- [ ] Backup MEMORY.md and LCM database
