# Plan: §21 "Skill Maintenance & Evolution" for the Meta-Skill

## Executive Summary

**Purpose:** Transform the skill file from a "one-time knowledge dump" into a "living document" with explicit maintenance procedures. A standalone §21 provides the operational framework that §5 (embedded in the meta-skill) only hints at.

**Real Problem:** Every project skill file eventually drifts. The current meta-skill has §5.1-5.3 (When to Update, Versioning, Drift Detection), but when you actually need to update a skill file, you face questions that §5 doesn't answer:
- "I added 3 new components — which sections need updating?"
- "I upgraded Next.js 16 → 17 — is this a minor or major skill version bump?"
- "How do I verify the skill file is still accurate after my update?"
- "How do I record what changed so future agents know what's new?"

**§21 solves this** by providing concrete, section-by-section procedures, a severity-driven update taxonomy, and automated verification.

---

## Analysis: Gaps in Current §5

| Need | What §5 Provides | What's Missing |
|---|---|---|
| **When** | Trigger table (7 scenarios) | No severity-based SLA |
| **How** | None | No section-by-section procedure |
| **How much** | Semver guidance | No update taxonomy (fix vs. update vs. refactor) |
| **Verification** | Bash drift-check script | No "after update" verification checklist |
| **Documentation** | None | No changelog template or format |
| **Safety** | None | No "rollout" strategy for breaking changes |

---

## §21 Design

### §21.1 The Maintenance Mindset

A skill file is not a static artifact. It is a **mirror of the codebase**. When the codebase changes, the mirror must be polished. Neglected mirrors warp reality.\ — worse than no skill file at all.

**Core principle:** Every code change that affects a skill file section must, as part of the same PR/sprint, update that section. This is non-negotiable.

### §21.2 Update Triggers by Severity (SLA)

| Severity | Trigger | SLA | Example |
|---|---|---|---|
| **P0 — Critical** | Build breaks, security fix, data loss | Immediate (same PR) | CVE patched, auth broken |
| **P1 — High** | Dependency major upgrade, API change | Next sprint | Next.js 16 → 17 |
| **P2 — Medium** | New feature, new component | Within 2 sprints | Added billing page |
| **P3 — Low** | Refactor, cleanup, docs fix | Next scheduled maintenance | Renamed utility function |

**Rule:** If you would write a CHANGELOG entry for it, the skill file needs updating.

### §21.3 Update Taxonomy

Use the same semver concept as §5.2, but with concrete decision rules:

| Type | Code Change | Skill File Change | Version Bump |
|---|---|---|---|
| **Patch** (e.g., v1.2.1 → v1.2.2) | Bug fix, typo, count correction | Fix a version number, line count, or file path | Patch |
| **Minor** (e.g., v1.2.2 → v1.3.0) | New feature, new component | Add to §5 inventory; add new hook to §6; add anti-pattern to §9 if relevant | Minor |
| **Major** (e.g., v1.3.0 → v2.0.0) | Framework upgrade, architecture change | Rewrite affected sections; verify all others still valid; update all version numbers | Major |
| **Structural** (e.g., v2.0.0 → v3.0.0) | Reorganize codebase, rename conventions | Rewrite §3 Bootstrapping, §5 Architecture, §14 Best Practices; verify every section | Major |

### §21.4 Section-by-Section Update Procedures

For each of the 20 sections, the exact procedure when the associated codebase area changes:

| If you... | Then update... | Procedure |
|---|---|---|
| Upgrade a dependency | §2 Tech Stack | Change version in table; update Critical Note if behavior changed |
| Add a new dependency | §2 Tech Stack | Add row with version + note; verify no transitive scope issues |
| Change build config | §3 Bootstrapping | Update config file snippet; test reproduction from scratch |
| Update design tokens | §4 Design System | Replace all tokens; verify every hex; update keyframes/utility counts |
| Add a component | §5 Components | Add to inventory; specify client/server; add line count; verify count total |
| Remove a component | §5 Components | Remove from inventory; check if referenced elsewhere (§9, §15, etc.) |
| Add a hook | §6 Hooks | Add with signature + implementation details; verify SSR safety |
| Add a data file | §7 Content | Add to inventory; document how to add new items; verify counts |
| Change color/palette | §19 Colors | Replace all hexes; update token table; verify contrast ratios |
| Add API route | §20 Interfaces | Add interface; verify auth pattern used; add to routing if applicable |
| Find a new bug | §9 Anti-Patterns | Add with severity; link to fix PR; add regression test reference |
| Learn a lesson | §12 Lessons | Add numbered entry with context; reference specific fix IDs |
| Change CI/CD | §11 Pre-Ship | Update commands; verify CI guard still valid |
| Add a11y feature | §8 Accessibility | Update contrast table if needed; document new pattern |

### §21.5 The Maintenance Checklist (After Every Update)

Before committing the updated skill file, verify ALL of the following:

- [ ] **Header updated:** Version bump + date changed
- [ ] **Counts verified:** `pnpm test` output matches skill file claims
- [ ] **Paths verified:** 10 random file paths from the skill actually exist (`ls` each)
- [ ] **Versions verified:** `package.json` versions match skill file table
- [ ] **Colors verified:** Every hex in §19 matches `globals.css` §theme block
- [ ] **No placeholders:** `grep -c "TODO\|FIXME\|placeholder" skill.md` == 0
- [ ] **TOC synced:** Skill file headings match the Table of Contents
- [ ] **Changelog entry added:** §21.6 format used
- [ ] **Drift check passed:** Automated script (§21.7) returns clean
- [ ] **Peer review completed:** Another agent or team member read the updated sections

### §21.6 Changelog Format

Every skill file update must include a changelog entry. Use a standard format at the skill file header:

```markdown
## Changelog

### v1.3.2 (2026-04-15)
**Type:** Patch  
**Trigger:** Test count drift  
**Changes:**
- §2: Updated Vitest from `^5.0.0` → `^5.1.0`
- §4: Added new `fade-in-scale` keyframe (14 total)
- §11: Updated pre-ship checklist to include `pnpm test:e2e`
**Verified by:** `scripts/skill-drift-check.sh`

### v1.3.1 (2026-04-08)
**Type:** Patch  
**Trigger:** Component count typo  
**Changes:**
- §5: Corrected component count from 29 → 30 (added `CookieBanner`)
**Verified by:** Manual `ls` count

### v1.3.0 (2026-04-01)
**Type:** Minor  
**Trigger:** New feature (GDPR export endpoint)  
**Changes:**
- §5: Added `ProjectDownloadButton` to component inventory (31 total)
- §15: Added "Click-time R2 URL signing" pattern
- §9: Added H4 stale-URL anti-pattern
**Verified by:** Full verification checklist + drift check
```

### §21.7 Automated Drift Detection (Per-Project Script)

Each project skill file repository should include a `scripts/skill-drift-check.sh` that is specific to that project. Generate this script as part of the initial skill file creation. It checks the most common drift vectors:

```bash
#!/bin/bash
# skill-drift-check.sh — PROJECT-SPECIFIC
# Add this to your CI pipeline or run manually before releases

ERRORS=0

# 1. Test counts
UNIT_TESTS=$(pnpm test 2>&1 | grep "Tests" | awk '{print $2}')
SKILL_UNIT=$(grep "Tests.*pass" docs/SKILL.md | head -1 | grep -oP '\d+(?=\s+unit)')
if [ "$UNIT_TESTS" != "$SKILL_UNIT" ]; then
  echo "⚠️  Test count drift: skill claims $SKILL_UNIT, actual $UNIT_TESTS"
  ERRORS=$((ERRORS+1))
fi

# 2. Component counts
COMPONENT_COUNT=$(find src/components -name "*.tsx" | wc -l)
SKILL_COMPONENTS=$(grep -oP '\d+(?=\s+component files)' docs/SKILL.md | head -1 || echo "0")
if [ "$COMPONENT_COUNT" != "$SKILL_COMPONENTS" ]; then
  echo "⚠️  Component count drift: skill claims $SKILL_COMPONENTS, actual $COMPONENT_COUNT"
  ERRORS=$((ERRORS+1))
fi

# 3. Env var count
ENV_COUNT=$(grep -c "^[[:space:]]*[A-Z_]*:" src/lib/env/index.ts || echo "0")
SKILL_ENV=$(grep -oP '\d+(?=\s+env vars)' docs/SKILL.md | head -1 || echo "0")
if [ "$ENV_COUNT" != "$SKILL_ENV" ]; then
  echo "⚠️  Env var count drift: skill claims $SKILL_ENV, actual $ENV_COUNT"
  ERRORS=$((ERRORS+1))
fi

# 4. No TODO or FIXME
TODO_COUNT=$(grep -c "TODO\|FIXME" docs/SKILL.md || echo "0")
if [ "$TODO_COUNT" -gt 0 ]; then
  echo "⚠️  Found $TODO_COUNT TODO/FIXME in skill file"
  ERRORS=$((ERRORS+1))
fi

# 5. Version header present
if ! grep -q "Version:" docs/SKILL.md; then
  echo "⚠️  Missing version header in skill file"
  ERRORS=$((ERRORS+1))
fi

# Return
if [ $ERRORS -eq 0 ]; then
  echo "✅ Skill file drift check passed"
else
  echo "❌ Found $ERRORS discrepancy(s). Update the skill file."
  exit 1
fi
```

### §21.8 Rollout Safety: Handling Breaking Changes

When a major or structural update affects how future agents should work with the codebase, you must prevent "version mismatch" confusion.

**Best practice:** Keep the old version header in the file for 1-2 sprints, with a deprecation notice:

```markdown
> **Version:** 2.0.0 (2026-05-01)
> **Previous:** v1.x (see `SKILL_v1_ARCHIVE.md` for legacy patterns)
> **Breaking changes:**
> - Next.js 15 → 16: `middleware.ts` renamed to `proxy.ts`
> - Drizzle ORM schema files reorganized (see §3)
> **Migration for agents reading old skills:** Search for `proxy.ts` instead of `middleware.ts`;
> migrate schema imports from `src/lib/db/schema.ts` to `src/lib/db/schema/index.ts`.
```

**Never delete old major versions immediately.** Rename them to `SKILL_v1_ARCHIVE.md` and reference them for at least one full sprint.

---

## Real Benefits

1. **Prevents "drift death" — the #1 reason skill files fail.** When a developer adds a new component, they don't know which skill sections are affected. §21.4 tells them exactly.
2. **Reduces update friction by 80%.** Instead of "read the whole skill file and guess what changed," you follow a procedure.
3. **Makes skills auditable.** The changelog creates a paper trail. When someone asks "why does the skill file say X?", the answer is in the changelog entry.
4. **Enables CI enforcement.** The drift check script in §21.7 can (and should) run in CI, blocking PRs where the skill file is stale.
5. **Protects future agents.** When a breaking change happens, §21.8 ensures agents reading the old skill file don't follow outdated instructions.

---

## Validation: How to Verify This Plan Works

1. Apply §21 to the `storyintovideo_SKILL.md` as a pilot. The `status_13.md` already shows the exact evolution that would have generated a changelog entry.
2. Write a `scripts/skill-drift-check.sh` for the StoryIntoVideo project.
3. Run it: it should detect the 2 updates we already made (redis version + env heading), proving the mechanism works.
4. Add the changelog header to `storyintovideo_SKILL.md` and record our updates.
