---
name: authjs-vs-better-auth
description: Compares Auth.js v5 and Better Auth for Next.js 16 projects. Side-by-side code for instance setup, route handlers, client auth, and server sessions. Database schema mapping for migration. Proxy.ts route protection pattern. Use when choosing an auth library, migrating from Auth.js to Better Auth, implementing proxy.ts checks, or debugging Next.js 16 auth issues.
version: 1.0.0
---

## Release Status

Auth.js v5 remains in beta — it has never left the beta channel since the rewrite began, and npm's `latest` tag still points to the legacy v4.x stable line. Better Auth has a stable v1.x release line with a 1.7.0-beta channel in testing.

| Aspect             | Auth.js v5                                                                        | Better Auth                                        |
| ------------------ | --------------------------------------------------------------------------------- | -------------------------------------------------- |
| Release channel    | `5.0.0-beta.26+` (npm `latest` = `v4.24.14`)                                      | `1.6.23` stable; `1.7.0-beta` in testing           |
| Next.js 16 support | Peer-dependency conflicts on fresh installs                                       | Fully compatible; `middleware` renamed to `proxy`  |
| Architecture       | Framework wrapper (NextAuth-specific)                                             | Framework-agnostic core with Next.js adapter       |
| Maintenance        | Original NextAuth team; Better Auth team now also patches Auth.js security issues | Actively developed, TypeScript-first, plugin-based |

## Next.js 16 Compatibility Notes

A GitHub issue confirms Next.js 16's middleware-to-proxy change initially broke Better Auth compatibility, but this was resolved and the library is now documented as "fully compatible with Next.js 16," with `middleware.ts` renamed to `proxy.ts` and the exported function renamed from `middleware` to `proxy`. Auth.js users have filed open compatibility questions about whether Next.js 16 is officially supported and whether the v5 peer-dependency range needs updating, suggesting some friction remains for greenfield Next.js 16 + Auth.js v5 setups. [github](https://github.com/nextauthjs/next-auth/issues/13302)

## Core Programming Differences

The two libraries diverge in initialization, session handling, and client APIs — migration requires more than find-and-replace.

**Instance setup:**

```ts
// Auth.js v5
import NextAuth from 'next-auth';
import GitHub from 'next-auth/providers/github';
export const { handlers, signIn, signOut, auth } = NextAuth({
  providers: [GitHub],
});

// Better Auth
import { betterAuth } from 'better-auth';
export const auth = betterAuth({
  socialProviders: {
    github: {
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    },
  },
});
```

**Route handler:** rename `/app/api/auth/[...nextauth]` to `/app/api/auth/[...all]` and swap the handler export.

```ts
// Auth.js v5
import { handlers } from '@/lib/auth';
export const { GET, POST } = handlers;

// Better Auth
import { auth } from '@/lib/auth';
import { toNextJsHandler } from 'better-auth/next-js';
export const { POST, GET } = toNextJsHandler(auth);
```

**Client-side sign-in/sign-out/session:** Auth.js exposes discrete `signIn`, `signOut`, and `useSession` from `next-auth/react`. Better Auth centralizes everything on a single `authClient` object.

```ts
// Auth.js v5
import { signIn, signOut, useSession } from 'next-auth/react';
signIn('github');
signOut();
const { data, status, update } = useSession();

// Better Auth
import { authClient } from '@/lib/auth-client';
await authClient.signIn.social({ provider: 'github' });
await authClient.signOut();
const { data, error, refetch, isPending } = authClient.useSession();
```

**Server-side session:** Better Auth requires explicitly passing request headers; Auth.js's `auth()` call is header-implicit.

```ts
// Auth.js v5
const session = await auth();

// Better Auth
import { headers } from 'next/headers';
const session = await auth.api.getSession({ headers: await headers() });
```

## Database Schema Mapping

Better Auth uses different field names and stricter typing than Auth.js's Prisma/Drizzle adapters.

- **User:** `name` and `emailVerified` are required (optional in Auth.js); `emailVerified` is a boolean, not a timestamp.
- **Session:** `token`/`expiresAt` replace `sessionToken`/`expires`; adds `ipAddress`/`userAgent`.
- **Account:** camelCase enforced (`refreshToken` vs `refresh_token`); adds `accountId` and `providerId` (replacing `provider`); drops `token_type`/`session_state`.
- **VerificationToken → Verification:** renamed table, single `id` primary key instead of composite, `value` field instead of `token`.
- All Better Auth tables add `createdAt`/`updatedAt` timestamps automatically.

## Route Protection (Next.js 16 proxy.ts)

Keep `proxy.ts` lightweight — check only for a session cookie's existence. Push full session validation into Server Components or Server Actions where the Node.js runtime is available.

```ts
// proxy.ts — cookie-only optimistic check
import { getSessionCookie } from 'better-auth/cookies';
export async function proxy(request) {
  const sessionCookie = getSessionCookie(request);
  if (!sessionCookie) return redirectToSignIn();
}

// Full validation belongs in the page/route itself
import { auth } from '@/lib/auth';
import { headers } from 'next/headers';
import { redirect } from 'next/navigation';
const session = await auth.api.getSession({ headers: await headers() });
if (!session) redirect('/sign-in');
```

Both Auth.js and Better Auth docs discourage using proxy/middleware as a full session-validation layer — per-page `getSession()` checks are required for real security guarantees.

## Decision Guide

- **Greenfield project:** Favor Better Auth — verified Next.js 16 compatibility, stable release, type-safe plugin architecture (RBAC, 2FA, organizations).
- **Existing Auth.js codebase:** Weigh migration cost against Auth.js v5's indefinite beta status. The Better Auth team has committed to patching Auth.js security issues. Budget separate time for a database schema migration if you use persistent sessions rather than JWT-only.
- **Either library:** Rename `middleware.ts`/`middleware()` to `proxy.ts`/`proxy()` — this is a Next.js 16 platform change, not an auth-library one.

## References

- https://www.npmjs.com/package/next-auth
- https://www.reddit.com/r/nextjs/comments/1k5vhfd/authjs_bumped_to_500beta26/
- https://www.pkgpulse.com/guides/better-auth-vs-nextauth-v5-vs-clerk-2026
- https://www.npmjs.com/package/better-auth
- https://better-auth.com/docs/integrations/next
- https://better-auth.com/docs/guides/next-auth-migration-guide
- https://authjs.dev/getting-started/migrate-to-better-auth
- https://auth0.com/blog/whats-new-nextjs-16/
- https://github.com/nextauthjs/next-auth/issues/13302
