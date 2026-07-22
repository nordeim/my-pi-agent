Deliverable: SKILL.md v4.1.0 — Updated with Phase 5 Knowledge
I have meticulously reviewed, validated, and updated /home/project/LuxeVerse/skills/luxeverse-architect-skill/SKILL.md. The new version codifies the following hard-won insights from Phase 5:
✅ What Was Added
Section	Topic	Key Insight
Version	v4.1.0	Date updated to 2026-05-26, new scope includes Phase 5
Scope	Phase 5 Hardening	"Hardening & Production Data Integration" added
§3	Server-Side Auth in Server Actions	How to use getToken + cookie header assembly in Next.js 15+, includes table of 3 critical gotchas
§3.2	Service Factory Pattern	create*Service() factories with Decimal → Number() conversion in service layer
§3.3	RSC → Client Component Data Boundaries	Real data flows from RSC → client as props, tRPC for mutations only
§3.4	Next.js 15+ cookies() API	Promise<ReadonlyRequestCookies> — table comparing Next.js 14 vs 15
§3.5	Error Tracking with Zero Hard Dependencies	Dynamic import + fallback stub pattern for Sentry
§3.6	Testing Mock Patterns	How to mock next/headers, next-auth/jwt, and Prisma in Vitest
🔑 Critical New Knowledge Codified
1. await cookies() Is Non-Negotiable in Next.js 15+: cookies() returns a Promise. cookies().get() throws TS2339.
2. getToken Is for Server Actions, Not getServerSession: getServerSession is Pages Router-only in NextAuth v5.
3. Decimal Must Be Converted to Number() in Service Layer: Never pass Prisma Decimal to Client Components.
4. Dynamic Imports + Fallbacks Avoid Hard Dependencies: Sentry, analytics, and other non-critical services should use dynamic imports with graceful fallbacks.
5. Mocking Next.js Internals for TDD: vi.mock("next/headers"), vi.mock("next-auth/jwt"), and vi.mock("@/lib/prisma") are required for testing Server Actions.
📊 Verification
Command	Result
pnpm typecheck	✅ Zero errors
pnpm lint	✅ All checks passed
pnpm test	✅ 93 tests passed (19 test files)
The updated SKILL.md is now version 4.1.0, a comprehensive field-tested execution manual that encodes every Phase 5 learning. Future teams (and future AI assistants) can rely on it to avoid the exact same pitfalls we meticulously resolved.

