# QUICKSTART — Distill Your First SKILL.md

> **Time estimate:** 6-10 hours for a mid-size project (500-2,000 source files)  
> **Output:** A verified `PROJECT西北地区准时的 SKILL.md` ready for future AI coding agents  
> **Scope:** This meta-skill is optimized for **web application** codebases (React, Vue, Svelte, Angular, etc.). For non-web projects (CLI tools, backend APIs, data pipelines), adapt the web-specific sections (§4, §6, §8, §17, §19) to your domain. See `SKILL.md` §Scope Note for full adaptation guidance.

---

## Prerequisites

- [ ] codebase exists and builds successfully ( `pnpm build` or equivalent passes )
- [ ] test suite passes ( `pnpm test` or equivalent ) — or you know why it does not
- [ ] you have read access to all configuration files
- [ ] you know the deployment target ( Vercel, AWS, Docker, etc. )

---

## Phase 1: ANALYZE ( 45 min )

Run these commands to gather intelligence:

exus```bash
# 1. Project identity
cat package.json | jq '.name, .version'
head -20 README.md
cat go.mod | head -5  # Or pyproject.toml, Cargo.toml, etc.

# 2. Tech stack inventory
npm list --depth=0 2>/dev/null || pnpm list --depth=0 2>/dev/null

# 3. Directory structure
find src -type f | head -100

# 4. Test count
pnpm test 2>&1 | grep -E "(Test Files|Tests)" | head -5

# 5. Component breakdown
grep -r "'use client'" src --include="*.tsx" | wc -l  # client components
grep -rL "'use client'" src --include="*.tsx" | wc -l  # server (approximate)

# 6. Env var count
grep -c "^env\." src/lib/env/index.ts 2>/dev/null || echo "no env module found"
```

**Deliverable:** A one-paragraph project summary + version table

## Phase 2: PLAN ( 30 min )

Map the 20 sections to actual files:

```bash
# Map sections to source files
echo "Paste into the 20-section plan:"
for section in {1..20}; do
  echo "§$section → "
done
```

**Deliverable:** Numbered checklist with file paths for each section

## Phase 3: VALIDATE ( 15 min )

Confirm your plan before writing:

```bash
# Verify all planned source files exist
# (check phase 2 paths with ls -la)
```

**Deliverable:** Go/no-go decision with explicit gap list

## Phase 4: IMPLEMENT ( 90-180 min )

Write the SKILL.md section by section:

*   **Time per section:** Expect **15-20 min per code-specific section** (§2, §4, §5, §6, §19, §20), **10 min per knowledge-specific section** (§9, §10, §12, §13, §14).
*   **For each section:** Read source → Write → Verify → Commit.

## Phase 5: VERIFY ( 30 min )

```bash
# Version accuracy
npm list next react react-dom | grep "@" || pip freeze | grep your-package

# Test counts match
pnpm test 2>&1 | grep -E "Test Files|Tests"  # or pytest, cargo test, etc.

# Red flags
grep -n "TODO\|FIXME\|placeholder\|example.com" PROJECT_SKILL.md || echo "Clean!"

# File paths exist (spot-check 10)
awk '/src\// {print}' PROJECT_SKILL.md | head -10

# Code snippet compiles
echo "If a snippet is wrong, the test suite will catch it."
```

## Phase 6: DELIVER ( 15 min )

1. Rename to `PROJECT_NAME_SKILL.md`
2. Add version stamp: `v1.0.0`
3. One-paragraph summary
4. Move to project root or `docs/`

## Troubleshooting

| Problem | Solution |
|---|---|
| "I don't know what goes in §7" | Skip it, mark as ` [WIP] `, come back later |
| "Test counts don't match" | Re-run; document flaky tests |
| "Found a file not in plan" | Add to §5 inventory |
| "§12 is empty" | Skip — only document actual lessons |
| "Document is too long" | Good. If brevity needed, focus on §1-§5. |

---

*For complete specifications, see `SKILL.md`.*
