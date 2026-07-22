# Skill Critique — `react19-ts6-vite8-tailwindv4-mvp`

> **Date:** 2026-05-09  
> **File:** `/home/pete/.pi/agent/skills/react19-ts6-vite8-tailwindv4-mvp/SKILL.md` (1099 lines, v3.0.0)  
> **Reviewer:** Claw Code (Post-Remediation Review)  
> **Comparison baseline:** Original enhanced skill at `/home/pete/.pi/agent/skills/react19-typescript6-vite8-mvp/SKILL.md` (974 lines, v1.1.0)  

---

## Executive Summary

The unified skill (`react19-ts6-vite8-tailwindv4-mvp`) is a **significantly more mature, polished, and comprehensive** version than the original. It addresses many of the same gaps found in the CHA YUAN remediation (useThrottledScroll, useFocusTrap, CSP, OG, dead code, testing gotchas) but in a **domain-anonymous, production-ready** form. It leverages lessons learned from real-world remediation cycles.

**Overall Grade: A** — Excellent. Well-worth promotion to primary reference.

---

## Strengths 🎉

### 1. Structural Elegance

| Feature | Why It Matters |
|---|---|
| **22 numbered sections** | Logical flow from bootstrap → build → testing → hardening |
| **Foldable details (HTML `<details>`)** | Keeps file navigable without scrolling through boilerplate |
| **Inline reference implementation** | ErrorBoundary class provided verbatim — no need to hunt for it |
| **Pre-Ship Hardening Checklist** (§22) | Ties everything together into actionable go/no-go criteria |
| **Domain-agnostic** | No "tea culture" or "CHA YUAN" references — pure reusable patterns |

### 2. Content Depth

| Section | Depth | Remark |
|---|---|---|
| §2 TypeScript | Includes `tsconfig.node.json` for Vite config | Better than original |
| §3 Tailwind | Full `@theme inline` template with semantic naming | Clearer than original |
| §5 Vite | Notes `tanstackRouter` vs `TanStackRouterVite` deprecation | Critical real-world fix |
| §7 Zustand | Explicit `partialize` for ephemeral UI state | Prevents toast/modal persistence bugs |
| §8 React 19 | `useOptimistic` + `startTransition` guard | Important detail missing from original |
| §10 Testing | Notes `/vitest` subpath import is recommended | Avoids jest-dom registration issues |
| §12 Build | Unified `vite.config.ts` for Vite + Vitest | Simpler than separate configs |
| §18 Accessibility | `useId()` for ARIA tab pairs (no hydration mismatch) | React 19 best practice |
| §19 Security | Warns about `'unsafe-inline'` for production | Responsible security posture |

### 3. Real-World Lessons Integrated

Every section references actual issues:
- "`crypto.randomUUID()` is unavailable in test env" → jsdom-safe ID generation
- "`unsafe-inline'` is only acceptable for dev/font loading" → production CSP strictness
- "Regenerate the route tree after adding it" → catches a common missed step
- "Latest-ref pattern to avoid effect teardown" → scroll throttling optimization

### 4. Hardening Checklist (§22)

This is the crown jewel. It transforms the skill from a "how to" into a "how to ship":
- Performance, Accessibility, Security, Testing, Maintenance — all covered
- Checkbox format → agent can self-audit before claiming completion
- References remediation table in `<details>` → shows real-world provenance

---

## Gaps & Opportunities for Enhancement 🔧

### 1. Dead Code Audit Script (§21 Is Incomplete)

**Current:** Basic CSS token grep.

```bash
grep -r "ivory-500" src/ || echo "Token is unused — safe to remove"
```

**Missing:** The comprehensive auto-audit bash script that scans:
- Path aliases for unused entries
- `@keyframes` for unused animations
- `@theme inline` for unused tokens
- Orphaned files (no imports)
- Sync between `tsconfig.json`, `vite.config.ts`, `vitest.config.ts` aliases

**Recommendation:** Replace the two `grep` examples with the full auto-audit script (≈60 lines) adapted to this skill's alias structure.

### 2. No "One-Shot" Prevention Philosophy

The enhanced original skill includes an explicit **"One-Shot Prevention"** philosophy:

> "Before Enhancement: Agent builds app → works → builds but has scroll jank, no CSP, dead code accumulates → 3+ rounds  
> After Enhancement: Agent reads skill → knows to add `useThrottledScroll` from the start → Result: Fewer rounds, less backtracking, higher quality on first pass"

This **behavioral framing** is missing. The unified skill is a reference, but it doesn't teach the agent *why* each item matters for reducing round trips.

**Recommendation:** Add a brief introduction before §1 explaining that every item in this skill was born from a real remediation round, and that skipping any section likely creates rework.

### 3. Remediation Round Stats Are Hidden in `<details>`

The "Common Real-World Remediations" table in §22's `<details>` block is buried.

| | Original Enhanced | Unified |
|---|---|---|
| Placement | Dedicated §22 frontmatter | Hidden `<details>` in §22 |
| Test evolution | "15 tests (4 files) → 49 tests (10 files) — +240%" | Not prominently displayed |
| Issue count | 15 explicitly listed | 7 in table, potentially more hidden |
| Prevention column for all issues | ✅ Yes | ⚠️ Only for first 7 examples |

**Recommendation:** Expand the remediation table (currently 7 rows) to include all 15 from the original, or extract the `<details>` block into a dedicated section (§23).

### 4. Missing: Path Alias Cleanup Cross-Reference

The Path Alias Cleanup Checklist (§20) is excellent but **scattered across three files**:
1. Delete file
2. Remove from `tsconfig.json` paths
3. Remove from `vite.config.ts` `resolve.alias`
4. Remove from `vitest.config.ts` `resolve.alias`

**However:** It doesn't mention that `vitest.config.ts` may **not exist** (unified approach has test config in `vite.config.ts`). This could confuse agents:

```
# In unified config (§5), there is NO separate vitest.config.ts
# So step 4 above is only for separate-config projects
```

**Recommendation:** Clarify that for unified configs, only `tsconfig.json` and `vite.config.ts` need updating.

### 5. Build Verification Order Is Not Front-and-Center

In the CHA YUAN codebase (and its AGENTS.md), the build verification order is **absolute gospel**:

```bash
npx tsc --noEmit → npm run build → npx vitest run
```

The unified skill mentions this in §12 but doesn't emphasize it as a **non-negotiable gate**. In practice, skipping this order (e.g., running tests before type check) causes cascading confusion.

**Recommendation:** Add a ⚠️ WARNING callout in §1 or §12: "Always run `tsc --noEmit` FIRST. Type errors fail tests silently or produce misleading test output."

### 6. Missing: Console Error Test Best Practice Evolved

The enhanced skill has this specific detail that the unified skill lacks:

```ts
// Enhanced skill:
let consoleSpy: ReturnType<typeof vi.spyOn>
beforeAll(() => { consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {}) })
afterAll(() => { consoleSpy.mockRestore() })
```

The unified skill's §10 shows `<details>` with `TanStack Router Link Mocking` but **does not show the `consoleSpy` guarding pattern**. This was a critical finding from the CHA YUAN remediation (ErrorBoundary tests emitting stderr).

**Recommendation:** Add a "Guarding Console Output in Tests" subsection to §10 or §17.

### 7. No Mention of `@shared/*` Path Alias Care

The unified skill defines `@shared/*` → `./src/components/shared/*` alias. This is **contentious**:
- `@shared` is semantically confusing (reads like a shared library, not shared components)
- Many projects skip it in favor of `@/components/shared/*`
- The alias is a **convention**, not a standard

**Recommendation:** Add a note: "`@shared/*` is optional. If unused, remove from `tsconfig.json` / `vite.config.ts` to avoid confusion."

---

## What the Unified Does BETTER than the Original 👏

| Area | Unified | Original |
|---|---|---|
| `tanstackRouter` vs deprecated name | ✅ Correct, with callout | ❌ Old name |
| `tsconfig.node.json` | ✅ Included | ❌ Missing |
| `partialize` for ephemeral state | ✅ Example: `partialize: () => ({})` | ❌ Missing detail |
| `startTransition` for `useOptimistic` | ✅ Warned about warning | ❌ Not mentioned |
| `useId()` for ARIA | ✅ React 19 best practice | ❌ Missing |
| CSP `'unsafe-inline'` warning | ✅ Production guidance | ❌ Basic CSP only |
| `/vitest` subpath import | ✅ Official recommended path | ❌ Missing |
| Unified `vite.config.ts` | ✅ Vite + Vitest merged | ❌ Separate config |
| Pre-Ship Hardening Checklist | ✅ 5 categories, 20+ items | ❌ Missing |
| Hardening `<details>` remediation table | ✅ Real-world issues | ❌ Missing |
| Inline `ErrorBoundary` reference | ✅ Full class component | ❄️ Mentioned only |
| `z-index` CSS variable tokens | ✅ `--z-base` through `--z-toast` | ❌ Missing |
| `$` catch-all route | ✅ For 404 handling | ❌ Mentioned but not explicit |
| Semantic color naming | ✅ `--color-surface`, `--color-primary` | ❄️ Generic `warm-white` etc. |

---

## Suggested Enhancements (Priority Order)

### High Priority
1. **Dead code auto-audit script** (§21): Replace grep examples with full bash script
2. **Build order gate** (§1 or §12): Add ⚠️ "Always run `tsc --noEmit` first"
3. **Console spy approach** (§10 or §17): Add `beforeAll`/`afterAll` guarding pattern

### Medium Priority
4. **Unified vs separate config clarification** (§20): Note `vitest.config.ts` may not exist
5. **`@shared/*` alias disclaimer** (§2 or §5): Note it's optional
6. **Extract `<details>` remediation into dedicated section** (§23): Promote from hidden to visible

### Low Priority
7. **"One-Shot Prevention" framing** (Introduction): Add behavioral rationale for the checklist
8. **Test evolution stats** (§22): Add before/after metrics ("15 → 49 tests") for credibility

---

## Overall Assessment

| Dimension | Grade | Notes |
|---|---|---|
| **Completeness** | A+ | 22 sections, edge cases covered, real-world tested |
| **Accuracy** | A | Correct deprecations, correct patterns, responsive to framework changes |
| **Usability** | A | Folding sections, inline code, checklist format |
| **One-Shot Prevention** | B+ | Content is there but lacks the behavioral framing |
| **Dead Code Detection** | B | Has audit guidance but not the full script |
| **Maintenance** | A | Version bumpable, clearly structured |

**Final Verdict:** The skill should be **promoted as the primary reference**. The original enhanced skill (v1.1.0) can be **deprecated** or the two can be merged, with the unified version absorbing the behavioral insights and the full auto-audit script.

---

*Critique generated from meticulous comparison of both skill versions against the actual CHA YUAN remediation deliverables.*
