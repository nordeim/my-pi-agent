## Duplicates & Obsolete Skills

Every spec-compliant skill is indexed above, including several that overlap heavily or have been superseded. They are flagged here so you pick deliberately rather than by accident.

### Obsolete — superseded, kept only as archive

| Skill | Note |
|-------|------|
| `pdf-old-20260806` | Legacy snapshot of the `pdf` toolkit (the same four production lines), archived under a dated name. Use `pdf`. |

### Direct near-duplicates — overlapping scope

| Cluster | Overlap |
|---------|---------|
| `web-app-foundation` ↔ `web-application` ↔ `web-application-engineering` | Three distillations of the same four source codebases (digma, neo-crm, project-management, zero-balance). `web-application` v1.2.0 is the newer, fuller line; `web-application-engineering` is its self-described condensed companion ("the fuller distillation is web-application_SKILL.md"); `web-app-foundation` is the earlier foundation variant (v1.1.0). |
| `skill-creator` ↔ `skill-creator-zai` | Near-identical scope — create/improve skills, run evals, benchmark with variance analysis, optimize descriptions. |
| `memory-architect` ↔ `memory-architecture` | Both cover the OpenClaw 3-layer memory system — bootstrap/audit/recover vs setup guide/troubleshooting. |
| `tdd` ↔ `tdd-workflow` ↔ `test-driven-development` | Three overlapping test-first skills with overlapping trigger conditions. |
| `spec` ↔ `spec-driven-development` | Both turn vague intent into a spec before coding (adjacent stages: `to-spec`, `implement-spec`). |
| `ship` ↔ `land-and-deploy` ↔ `shipping-and-launch` | Three overlapping ship/deploy workflow skills. |
| `webapp-testing-journey` ↔ `frontend-ui-testing-journey` | Both walk the same browser-testing toolset (OpenClaw browser, agent-browser CLI, chrome-devtools-mcp, @playwright/mcp). |
| `thermo-nuclear-review` ↔ `thermo-nuclear-code-quality-review` | Same "thermonuclear review" trigger phrase; security/correctness vs maintainability focus. |
| `docx-generation` ↔ `docx` | `docx-generation` is a one-line scoped subset of the canonical `docx` skill. |

### Overlapping families — deliberate variants, check descriptions before choosing

- **Document formats** — `docx` / `kimi-docx` / `minimax-docx` / `pandoc-docx-template`; `pdf` / `kimi-pdf` / `minimax-pdf` / `make-pdf`; `xlsx` / `kimi-xlsx` / `minimax-xlsx`; `pptx` / `pptx-generator` / `pptx-unified` (combines the canonical `pptx` pipeline with `cyber-ppt` and `pptx-generator` strengths) / `codex-ppt` / `cyber-ppt`.
- **Next.js 16 stack references** — `web-application`, `web-app-foundation`, `fullstack-dev`, `web-frameworks`, `nextjs16-tailwind4`, and the eight `nextjs16-react19-*` variants share the same core stack (Next.js 16 + React 19 + TypeScript strict + Tailwind v4 + Prisma/Drizzle); each variant adds app-specific lessons.
- **Code review** — `code-review` / `code-review-and-audit` / `code-review-checklist` / `code-quality-standards` form a differentiated family; the checklist explicitly defers to the others.
- **Grilling** — `grilling` (primitive) / `grill-me` (stateless) / `grill-with-docs` (stateful, captures ADRs) — one family, three modes.
- **De-slopping** — `deslop` (code slop) vs `unslop` / `humanizer` (prose) — split by target, with the prose pair overlapping.

**Repo hygiene note** — `skills/brutalist-portfolio-nextjs/rutalist-portfolio-nextjs/` is a stray, typo-named nested copy containing only a `SKILL.md`; it is tracked in git and is safe to delete.
