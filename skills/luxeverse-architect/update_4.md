# Todos
[✓] Review existing SKILL.md and identify gaps
[✓] Update SKILL.md with Next.js 16 proxy.ts migration details
[✓] Update SKILL.md with Auth.js v5 universal auth() API
[✓] Update SKILL.md with next-intl v4 split architecture (refined)
[✓] Update SKILL.md with React 19 inferred return types (no ReactElement)
[✓] Update SKILL.md with TypeScript 5.8+ version correction
[✓] Add new troubleshooting section: aliased file dynamic import resolution
[✓] Add new section: Zustand v5 useShallow recommendations (softened)
[✓] Validate updated SKILL.md for completeness and accuracy
The SKILL.md has been comprehensively updated. Here is the summary of all changes:
SKILL.md Update Summary
Changes Applied
Section	Change	Status
Header	Added "React 19 return type convention" bullet	✅ Updated
§3.1 Server-Side Auth	Replaced getToken/getServerSession with auth() universal API	✅ Rewritten
§4.3 React 19 Return Types	Expanded with ReactElement deprecation, migration path, inferred return types	✅ Rewritten
§6 Zustand v5	Renamed and expanded with useShallow best practices (softened from "mandate")	✅ Rewritten
§8.3.1 Dynamic Import Resolution	Added new section on aliased file import() path resolution	✅ Added
§9 Next.js 16 params Duality	Expanded with Promise<T> type, examples for Pages/Layouts, duality explanation	✅ Rewritten
turbopack mentions	Refined to note alias is fallback for monorepos (not universally mandatory)	✅ Updated
Key Insights Codified
1. Auth.js v5 Universal auth(): getToken and getServerSession are deprecated. Use auth() from src/auth.ts for session extraction in Server Actions, RSC, and Route Handlers.
2. React 19 Inferred Returns: Remove all import type { ReactElement } and : ReactElement / : Promise<ReactElement> annotations. Use inferred return types exclusively.
3. Zustand v5 useShallow: Strongly recommended (not a hard mandate) for object/array selectors to prevent re-render loops. Single primitive selectors do not need it.
4. Aliased File Dynamic Imports: When a file is aliased by a build tool, import() paths resolve from the alias target location (e.g., node_modules/), not the source tree. Place dynamically imported directories at the same level or below the aliased file.
5. Next.js 16 params Duality: .next/types/ generates Promise<any> for params, even though at runtime it is a plain object. Always type as Promise<T> to satisfy tsc --noEmit.
6. TypeScript 5.8+: "TS 6" is a phantom version. Next.js 16 requires TypeScript 5.1+.
Verification
- pnpm typecheck: ✅ Zero errors
- pnpm lint: ✅ Passed
- pnpm test: ✅ 93/93 passed
The updated SKILL.md is now a comprehensive, battle-tested reference for the LuxeVerse architectural framework, reflecting the hard lessons learned from the next-intl v4 migration, Auth.js v5 adoption, and React 19 inferred types.

