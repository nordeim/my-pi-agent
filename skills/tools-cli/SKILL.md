---
name: tools-cli
description: Standalone CLI wrapper exposing Claude Code's core file operations (read, glob, grep, edit, write) as command-line utilities. Use for scripting and automation without requiring a full Claude session.
---

# Tools CLI - Standalone file operation wrapper

**Purpose:** CLI wrapper for Claude Code's file operations (read, write, edit, glob, grep) without a full session.

**Key facts:**
- Binary: `/home/project/cc-src/dist/tools-cli.js` (20.1 MB, ~500ms startup)
- Runs in `bypass` mode (no permission prompts)
- `glob`/`grep` require: `export USE_BUILTIN_RIPGREP=false`
- **If installed:** Use `tools-cli` directly (check with `which tools-cli`)

**Usage:** `tools-cli <command> [options]` or `bun /home/project/cc-src/dist/tools-cli.js <command> [options]`

---

## When to Use tools-cli vs Built-in Pi Agent Tools

**Priority: Built-in pi agent tools by default.** Use tools-cli when it offers clear convenience:

| Scenario | Pi Agent Tools | tools-cli | Winner |
|----------|---------------|-----------|--------|
| Single file read/write/edit | `read`, `write`, `edit` | Same | **Pi** (cache works) |
| Find files by pattern | `bash` + `find`/`ls` | `glob` | **tools-cli** (cleaner syntax) |
| Search file contents | `bash` + `grep`/`rg` | `grep` | **tools-cli** (structured output) |
| Batch operations in scripts | Multiple tool calls | Single bash command | **tools-cli** (loops work) |
| JSON structured output | Parse manually | `--json` flag | **tools-cli** (built-in) |
| CI/CD pipelines | Not applicable | Native bash | **tools-cli** (designed for it) |

**Use tools-cli when:**
- Writing bash scripts that need file discovery (`glob`) or content search (`grep`)
- Building CI/CD pipelines with file operations
- Needing structured JSON output for parsing
- Chaining multiple file operations in a single bash command

**Use pi agent tools when:**
- Performing single file edits (cache protection works)
- Working within agent session (no shell overhead)
- Editing files that might have concurrent modifications

---

## Commands

### read — Read file contents
```bash
tools-cli read --file <path> [--limit N] [--offset N] [--json] [--silent]
```
Returns JSON with `file.content`, `numLines`, `startLine`, `totalLines`.

### write — Create or overwrite files
```bash
tools-cli write --file <path> --content "<text>"
```
⚠️ **Cache check applies to existing files.** If file was read/modified in session, write fails with "File has been unexpectedly modified."

### edit — String replacement (cache-protected)
```bash
tools-cli edit --file <path> --old "<exact>" --new "<replacement>"
```
**Fails in CLI** — each invocation is separate process with empty cache.

**CLI workaround:** Read → modify in shell → write back:
```bash
content=$(tools-cli read --file config.json | jq -r '.file.content')
new_content="${content/old/new}"
tools-cli write --file config.json --content "$new_content"
```

### glob — Find files by pattern
```bash
tools-cli glob --pattern "<glob>" [--path <dir>] [--head N] [--silent]
```
Requires `USE_BUILTIN_RIPGREP=false`. Supports `**`, `*`, `?`, `[]`.

### grep — Search file contents
```bash
tools-cli grep --pattern "<regex>" [--path <dir>] [--mode content|files] [--head N] [-i] [--context N]
```
Requires `USE_BUILTIN_RIPGREP=false`.

---

## Global Options

| Option | Description |
|--------|-------------|
| `--cwd <path>` | Set working directory |
| `--json` | Output as JSON |
| `--silent` | Suppress non-error output |
| `--verbose` | Debug info |
| `--help` | Help message |
| `--version` | Version |

---

## Cache Protection (FileStateCache)

**Purpose:** Prevents editing files modified by external processes since last read.

**How it works:**
1. `read` stores file content + timestamp in cache
2. `edit`/`write` validate: file read? stale? modified since read?
3. If validation fails → error, requires re-read

**CLI limitation:** Each invocation creates fresh empty cache → `read` → `edit` across invocations fails.

**Error messages:**
- "File has not been read yet"
- "File has been unexpectedly modified. Read it again before attempting to write it."

**In agent sessions (OpenClaw/Claude Code):** Cache persists across tool calls → `read` → `edit` works.

---

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| "File has been unexpectedly modified" | Cache validation failed | Re-read file before edit/write |
| "ripgrep not found" | `USE_BUILTIN_RIPGREP` not set | `export USE_BUILTIN_RIPGREP=false` |
| Slow startup | 20MB binary init | Acceptable for scripts; use alias for interactive |

---

## Quick Reference

```bash
# Setup (for glob/grep)
export USE_BUILTIN_RIPGREP=false

# Read
tools-cli read --file README.md --limit 10
tools-cli read --file README.md --offset 5 --limit 3 --json

# Write (new file)
tools-cli write --file /tmp/test.txt --content "Hello World"

# Edit workaround (CLI)
content=$(tools-cli read --file config.json | jq -r '.file.content')
tools-cli write --file config.json --content "${content/old/new}"

# Glob
tools-cli glob --pattern "*.ts" --path src/ --head 10

# Grep
tools-cli grep --pattern "TODO" --path src/ --mode content --head 5
```
