# Skill Enhancement Summary — `react19-typescript6-vite8-mvp`

> **Original:** 632 lines, 15 sections  
> **Enhanced:** 974 lines, 22 sections (+342 lines, +7 sections)

---

## New Sections Added

### 16. Custom Hooks (Advanced)
| Hook | Purpose | Key Insight |
|---|---|---|
| `useThrottledScroll` | Throttle scroll events via `requestAnimationFrame` + `setTimeout` | Prevents 60fps re-renders; critical for performance |
| `useFocusTrap` | Trap Tab within modals/mobile menus | Manual implementation (no `react-focus-lock` dep); tracks trigger for focus restoration |

### 17. Testing Gotchas (Advanced)
| Gotcha | Solution |
|---|---|
| `requestAnimationFrame` not in jsdom | `vi.stubGlobal('requestAnimationFrame', cb => setTimeout(cb, 16))` |
| Fake timers with rAF | `vi.useFakeTimers({ shouldAdvanceTime: true })` |
| Throttled scroll tests | Advance by `rAF_delay + throttle_delay` (e.g., 120ms) |
| `consoleSpy` at module scope | Move to `beforeAll`/`afterAll` — prevents cross-test leaks |
| ErrorBoundary `stderr` | Expected — `componentDidCatch` logs to `stderr`; assertions still pass |

### 18. Accessibility (WCAG)
| Pattern | Code |
|---|---|
| Skip-to-content link | `sr-only focus:not-sr-only` with `<main id="main-content">` |
| Roving tabindex | `tabIndex={active ? 0 : -1}` on tab buttons |
| ARIA tabs | `role="tablist"`, `role="tab"`, `role="tabpanel"` with keyboard nav |

### 19. Security Essentials
| Layer | Meta Tag |
|---|---|
| CSP | `<meta http-equiv="Content-Security-Policy" content="..."/>` |
| Open Graph | `<meta property="og:title" content="..."/>` |
| Twitter Card | `<meta name="twitter:card" content="summary_large_image"/>` |
| External links | `rel="noopener noreferrer"` |

### 20. Dead Code Prevention
| Type | Detection | Fix |
|---|---|---|
| CSS tokens | `grep "token" src/` — if no matches, remove | Delete from `globals.css` |
| @keyframes | `grep "name" src/` — if no matches, remove | Delete from `globals.css` |
| Type aliases | `grep "@types" src/` — if no matches, remove | Delete from `tsconfig.json`, `vite.config.ts`, `vitest.config.ts` |
| Orphaned files | `find` + `grep` — no imports | Delete file + cleanup aliases |

### 21. Removable Dead Code Checklist (Auto-Audit)
Complete bash script provided for automated dead code detection:
- Scans path aliases for unused entries
- Scans `@theme inline` for unused CSS tokens
- Scans `@keyframes` for unused animations
- Scans `src/` for orphaned files (no imports)

### 22. Remediation Round Reference (Real-World)
15 real-world issues from the CHA YUAN project with fixes and prevention strategies:

| # | Issue | Fix |
|---|---|---|
| 1 | Empty `types/index.ts` | Delete + remove path alias |
| 2 | Unused CSS token (`ivory-500`) | Remove from `globals.css` |
| 3 | Unused `@keyframes` | Remove from `globals.css` |
| 4 | Duplicated hook (`useScrollReveal`) | Delete (component has its own) |
| 5 | Toast timeout stacking | Module-level `timeoutId` + `clearTimeout` |
| 6 | No CSP | Add meta tag |
| 7 | No OG/Twitter meta | Add meta tags |
| 8 | `consoleSpy` at module scope | Move to `beforeAll`/`afterAll` |
| 9 | Unthrottled scroll | `useThrottledScroll` hook |
| 10 | No focus trap | `useFocusTrap` hook |
| 11 | No skip link | Add `SkipLink` component |
| 12 | No 404 route | Add `not-found.tsx` |
| 13 | Decorative SVGs not hidden | Add `aria-hidden` |
| 14 | `rAF` fails in tests | `vi.stubGlobal('requestAnimationFrame', ...)` |
| 15 | Throttled scroll tests timeout | `vi.useFakeTimers({ shouldAdvanceTime: true })` |

**Test evolution:** 15 tests (4 files) → 49 tests (10 files) — **+240%**

---

## Key Insight: "One-Shot" Prevention

The #1 goal of this enhancement is **reducing unnecessary rounds** by embedding:
1. **Hooks that solve common problems** (scroll throttling, focus trap — no new dependencies)
2. **Testing patterns that actually work** (rAF mocking, fake timer config, console spy placement)
3. **Dead code detection** (auto-audit script prevents bloat)
4. **Security + accessibility checklists** (CSP, OG, skip links, ARIA tabs)
5. **Real-world remediation table** (15 issues with prevention — no more repeating)

### Before Enhancement
- Agent builds app → works → builds but has scroll jank, no CSP, dead code accumulates
- Each new agent wastes time discovering same issues

### After Enhancement
- Agent reads skill → knows to add `useThrottledScroll` from the start
- Agent adds `SkipLink` because the skill says WCAG requires it
- Agent runs dead code audit script before declaring "done"
- Agent adds CSP + OG meta in `index.html` from day one
- Agent places `consoleSpy` in `beforeAll` not module scope → no test flakiness
- **Result:** Fewer rounds, less backtracking, higher quality on first pass
