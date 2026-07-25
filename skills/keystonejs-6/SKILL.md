---
name: keystonejs-6
description: "KeystoneJS 6 (TypeScript, Node.js 20+) schema-as-code headless CMS + admin panel generator + GraphQL API workflow skill. Covers the schema-as-code paradigm (define lists with fields in keystone.ts → Keystone auto-generates the admin UI, GraphQL schema, and Prisma schema — no manual CRUD, no manual admin, no manual GraphQL resolvers), the list system (list(fields: { name: text(), email: text({ isUnique: true }), posts: relationship({ ref: 'Post.author', many: true }) }) — each list becomes a GraphQL type with auto-generated CRUD queries/mutations), the field types (text, select, integer, float, timestamp, calendarDay, checkbox, password, image, file, document, relationship, virtual, computed, json, slug, color, etc. — each with its own admin UI widget + GraphQL input/output types), access control (list-level access control via access: { operation: { read: true, create: () => false, update: ({ session }) => session?.isAdmin, delete: false }, filter: { read: ({ session }) => session ? { author: { id: { equals: session.itemId } } } : false } }), the session management (createAuthStrategy for email/password auth, or custom session strategy with JWT/cookies), hooks (resolveInput, validateInput, beforeChange, afterChange, beforeDelete, afterDelete — server-side logic triggered on CRUD operations), the Keystone + Prisma integration (Keystone generates the Prisma schema, runs migrations, and uses Prisma Client under the hood — but you never write Prisma code directly), the Admin UI (auto-generated React app at /admin — searchable, filterable, sortable lists with inline editing, relationship pickers, file upload), and deployment (Keystone is a standard Node.js app — deploy to Vercel, Railway, Render, Fly.io, or any Node host). Use when building any content-heavy app — blog, CMS, e-commerce catalog, documentation site, admin panel, internal tool — especially when the task involves schema design, access control rules, hooks for business logic, or auto-generated admin UI where idiomatic Keystone (schema-as-code → auto-generated everything) differs fundamentally from building CRUD manually with Express/Fastify/NestJS + a separate admin library."
license: Proprietary. LICENSE.txt has complete terms
---

# KeystoneJS 6 — Schema-as-Code Headless CMS + Admin + GraphQL API

> **Target:** KeystoneJS 6 (the 2022+ rewrite — completely different from KeystoneJS 4/5) on Node.js 20+ with TypeScript 5+. Keystone's distinctive paradigm: **define your schema as code → get a fully functional admin UI + GraphQL API + Prisma database layer for free.** No manual CRUD, no manual admin panel, no manual GraphQL resolvers. The schema IS the application.

## When to Use This Skill

Use this skill whenever the user is building, debugging, or extending a KeystoneJS 6 application. Trigger phrases include "Keystone", "KeystoneJS", "Keystone 6", "keystone.ts", "keystone-server.ts", "createList", "lists:", "fields:", "relationship(", "text(", "image(", "document(", "select(", "access:", "hooks:", "resolveInput", "beforeChange", "afterChange", "createAuthStrategy", "session:", "Admin UI", "/admin", "graphql", "prisma", "@keystone-6/core", "@keystone-6/fields-document", "@keystone-6/auth", "@keystone-6/session-store", and any reference to a `keystone.ts` config file or the `list(config)` function.

Do **not** use this skill for:
- **KeystoneJS 4 / 5** — completely different API (the 6 rewrite was a from-scratch rewrite). The `keystone.createList()` API from v4 is gone.
- **Strapi / Directus / Sanity** — these are also headless CMSes but with different APIs (Strapi is plugin-based, Directus is database-first, Sanity is content lake + GROQ). Different paradigms.
- **WordPress** — PHP-based, plugin/theme architecture, completely different ecosystem.
- **Contentful / Contentstack** — hosted SaaS CMSes, no server-side code.
- **Manual CRUD apps** (Express + admin library) — Keystone replaces the entire CRUD + admin + API stack. If you're building CRUD manually, see `fastify` or `nestjs` skills.

Cross-reference: `nestjs` and `fastify` cover building APIs manually. Keystone is for when you want the schema to drive the API + admin. `astro-5` is the canonical frontend to pair with Keystone (Astro fetches from Keystone's GraphQL API).

## Quick Start

```bash
# Create a new Keystone project
npm init keystone-app@latest my-app
# OR: npx create-keystone-app@latest my-app

cd my-app
npm install

# Dev server — starts Keystone + Admin UI + GraphQL playground
npm run dev                  # http://localhost:3000 (Admin UI at /admin, GraphQL at /api/graphql)

# The starter includes:
# - keystone.ts (the schema config)
# - schema.graphql (auto-generated — don't edit)
# - schema.prisma (auto-generated — don't edit)
```

### Key commands

```bash
npm run dev                  # Dev server with hot reload
npm run build                # Production build
npm run start                # Run the production build

# Prisma migrations (Keystone generates the schema, Prisma runs migrations)
npx keystone prisma migrate dev --name <migration-name>
npx keystone prisma migrate deploy
npx keystone prisma migrate status
npx keystone prisma migrate reset     # DESTRUCTIVE — drop + recreate

# Generate the Keystone artifacts (after schema changes)
npx keystone build            # Regenerates schema.graphql + schema.prisma + builds Admin UI
```

### Project structure

```
my-app/
├── keystone.ts               # ← THE config (schema, database, auth, session)
├── schema.graphql            # Auto-generated GraphQL schema (don't edit)
├── schema.prisma             # Auto-generated Prisma schema (don't edit)
├── src/
│   ├── schema/               # Schema definitions (split for large projects)
│   │   ├── user.ts           # User list definition
│   │   ├── post.ts           # Post list definition
│   │   └── index.ts          # Combines all lists
│   ├── access.ts             # Access control helpers
│   ├── hooks/                # Hook functions
│   │   ├── user.ts
│   │   └── post.ts
│   ├── lib/
│   │   ├── auth.ts           # Auth strategy config
│   │   ├── session.ts        # Session config
│   │   └── s3.ts             # S3 storage config for images
│   └── server.ts             # Custom server (rarely needed)
├── migrations/               # Prisma migrations (auto-generated, but commit them)
├── public/                   # Static assets served at /
├── package.json
├── tsconfig.json
└── Dockerfile
```

---

## Core Mental Model: Schema-as-Code → Auto-Generated Admin + GraphQL + Prisma

Keystone's distinctive paradigm is **you define the schema; Keystone generates everything else.** Three things differentiate Keystone from building CRUD manually:

### 1. The schema IS the application

```typescript
// keystone.ts
import { config, list } from '@keystone-6/core';
import { text, password, relationship, select, timestamp, image, document } from '@keystone-6/core/fields';
import { allowAll } from '@keystone-6/core/access';

export default config({
  db: {
    provider: 'postgresql',
    url: process.env.DATABASE_URL!,
  },
  lists: {
    User: list({
      fields: {
        name: text({ validation: { isRequired: true } }),
        email: text({ validation: { isRequired: true }, isIndexed: 'unique' }),
        password: password(),
        role: select({
          options: [
            { label: 'Admin', value: 'admin' },
            { label: 'Editor', value: 'editor' },
            { label: 'Viewer', value: 'viewer' },
          ],
          defaultValue: 'viewer',
        }),
        posts: relationship({ ref: 'Post.author', many: true }),
      },
      access: allowAll,   // Or a custom access function
    }),

    Post: list({
      fields: {
        title: text({ validation: { isRequired: true } }),
        slug: text({ isIndexed: 'unique' }),
        content: document({
          relationships: { mention: { list: 'User', label: 'Mentioned Users', many: true } },
        }),
        status: select({
          options: [
            { label: 'Draft', value: 'draft' },
            { label: 'Published', value: 'published' },
            { label: 'Archived', value: 'archived' },
          ],
          defaultValue: 'draft',
        }),
        author: relationship({ ref: 'User.posts', many: false }),
        publishedAt: timestamp(),
        heroImage: image({ storage: 's3' }),
      },
      access: {
        operation: {
          read: allowAll.read,
          create: ({ session }) => !!session,
          update: ({ session, item }) => session?.itemId === item.authorId || session?.data.role === 'admin',
          delete: ({ session }) => session?.data.role === 'admin',
        },
      },
    }),
  },
  storage: {
    s3: {
      kind: 's3',
      bucketName: process.env.S3_BUCKET!,
      region: process.env.S3_REGION!,
      accessKeyId: process.env.S3_ACCESS_KEY!,
      secretAccessKey: process.env.S3_SECRET_KEY!,
    },
  },
});
```

**What Keystone generates from this config:**

1. **Prisma schema** (`schema.prisma`):
   ```prisma
   model User {
     id       String   @id @default(cuid())
     name     String
     email    String   @unique
     password String
     role     String   @default("viewer")
     posts    Post[]
   }

   model Post {
     id          String    @id @default(cuid())
     title       String
     slug        String    @unique
     content     Json
     status      String    @default("draft")
     authorId    String?
     author      User?     @relation(fields: [authorId], references: [id])
     publishedAt DateTime?
     heroImage   String?
   }
   ```

2. **GraphQL schema** (`schema.graphql`) — full CRUD for both lists:
   ```graphql
   type User {
     id: ID!
     name: String
     email: String
     password: PasswordState
     role: String
     posts: [Post]
   }

   type Query {
     users(where: UserWhereInput): [User]
     user(where: UserWhereUniqueInput!): User
     posts(where: PostWhereInput): [Post]
     post(where: PostWhereUniqueInput!): Post
   }

   type Mutation {
     createUser(data: UserCreateInput): User
     updateUser(where: UserWhereUniqueInput!, data: UserUpdateInput): User
     deleteUser(where: UserWhereUniqueInput!): User
     # ... same for Post
   }
   ```

3. **Admin UI** at `/admin` — a React app with:
   - Searchable, sortable, filterable list views for User and Post
   - Create/edit forms with the right widget for each field (text input for `text`, dropdown for `select`, date picker for `timestamp`, image uploader for `image`, rich text editor for `document`)
   - Relationship pickers (select a User for `Post.author`)
   - Inline editing, bulk operations, pagination

**You wrote zero CRUD code, zero admin code, zero GraphQL resolver code.** The schema config IS the application.

### 2. Field types are full-stack (admin widget + GraphQL type + DB column)

Each field type (`text`, `select`, `relationship`, `image`, `document`, etc.) bundles:
- **Admin UI widget** — the React component for editing this field
- **GraphQL input/output types** — the GraphQL schema for this field
- **Database column** — the Prisma/SQL representation
- **Validation** — server-side validation rules

```typescript
import { text, select, relationship, image, document, timestamp, integer, checkbox, password, json, virtual, computed } from '@keystone-6/core/fields';

const Post = list({
  fields: {
    // text — string field with admin text input
    title: text({ validation: { isRequired: true, length: { min: 3, max: 200 } } }),

    // select — dropdown in admin, enum in GraphQL
    status: select({
      options: [
        { label: 'Draft', value: 'draft' },
        { label: 'Published', value: 'published' },
      ],
      defaultValue: 'draft',
      validation: { isRequired: true },
    }),

    // relationship — foreign key with relationship picker in admin
    author: relationship({ ref: 'User.posts', many: false }),
    tags: relationship({ ref: 'Tag.posts', many: true }),

    // image — file upload with S3 storage + image preview in admin
    heroImage: image({ storage: 's3' }),

    // document — rich text editor (Keystone's DocumentField — like Notion)
    content: document({
      relationships: { mention: { list: 'User', label: 'Mention', many: true } },
    }),

    // timestamp — date/time picker in admin
    publishedAt: timestamp({ defaultValue: { kind: 'now' } }),

    // integer — number input in admin
    viewCount: integer({ defaultValue: 0 }),

    // checkbox — toggle in admin
    featured: checkbox({ defaultValue: false }),

    // password — password input with hashing (never returned in GraphQL)
    password: password(),

    // json — JSON editor in admin
    metadata: json(),

    // virtual — computed field (not stored in DB, computed on read)
    excerpt: virtual({
      field: graphql.field({
        type: graphql.String,
        resolve: (item) => (item.content ? item.content.substring(0, 200) + '...' : null),
      }),
    }),

    // computed — computed AND stored (updated via hooks)
    wordCount: computed({
      type: graphql.Int,
      resolve: (item) => (item.content ? item.content.split(/\s+/).length : 0),
    }),
  },
});
```

### 3. Access control is a function (not a static rule)

```typescript
// src/access.ts
import { SessionContext } from '@keystone-6/core/types';

type Session = { itemId: string; data: { role: string } } | undefined;

export function isSignedIn({ session }: { session: Session }) {
  return !!session;
}

export function isAdmin({ session }: { session: Session }) {
  return session?.data.role === 'admin';
}

export function isOwner({ session, item }: { session: Session; item: any }) {
  return session?.itemId === item.authorId;
}

export const postAccess = {
  operation: {
    // Who can perform each operation at all?
    read: true,                                    // Anyone can read
    create: isSignedIn,                            // Must be signed in
    update: isSignedIn,                            // Must be signed in (further filtered below)
    delete: isAdmin,                               // Only admins
  },
  filter: {
    // For read/update, filter the items they can see/modify
    read: ({ session }: { session: Session }) => {
      if (!session) return { status: { equals: 'published' } };   // Anonymous: only published
      if (session.data.role === 'admin') return true;             // Admin: all posts
      return { author: { id: { equals: session.itemId } } };      // Others: own posts
    },
    update: ({ session }: { session: Session }) => {
      if (session?.data.role === 'admin') return true;
      return { author: { id: { equals: session.itemId } } };      // Only own posts
    },
  },
  item: {
    // For create/update/delete, check the specific item
    update: ({ session, item }: { session: Session; item: any }) => {
      if (session?.data.role === 'admin') return true;
      return session?.itemId === item.authorId;
    },
    delete: ({ session, item }: { session: Session; item: any }) => {
      return session?.data.role === 'admin';
    },
  },
};
```

Access control in Keystone has three levels:
- **`operation`** — can the user perform this operation at all? (boolean)
- **`filter`** — for read/update, which items can they see/modify? (a Prisma `where` filter)
- **`item`** — for create/update/delete, check the specific item being modified (boolean)

This is more expressive than role-based access control (RBAC) — you can express "users can edit their own posts" naturally.

---

## Field Types (the catalog)

### Basic fields

| Field | Use | Admin widget |
|---|---|---|
| `text` | Short string | Text input |
| `textarea` | Long string | Textarea |
| `password` | Hashed password | Password input (never returned in GraphQL) |
| `checkbox` | Boolean | Toggle |
| `integer` | Whole number | Number input |
| `float` | Decimal number | Number input |
| `select` | Enum | Dropdown |
| `timestamp` | Date + time | Date picker |
| `calendarDay` | Date only | Date picker |
| `json` | Arbitrary JSON | JSON editor |

### Relationship fields

| Field | Use |
|---|---|
| `relationship({ ref: 'OtherList.field', many: false })` | Foreign key (one-to-many) |
| `relationship({ ref: 'OtherList.field', many: true })` | Many-to-many (junction table auto-created) |

### Rich content fields

| Field | Use |
|---|---|
| `document` | Rich text editor (Keystone's DocumentField — like Notion/Editor.js; supports relationships, code blocks, images) |
| `image` | Image upload (with storage config — S3, local) |
| `file` | File upload (any type) |

### Computed fields

| Field | Use |
|---|---|
| `virtual` | Computed on read (not stored in DB) |
| `computed` | Computed and stored (updated via hooks) |

### Field configuration options

```typescript
text({
  label: 'Post Title',                          // Custom label in admin
  ui: {
    description: 'The title shown at the top of the post',  // Help text
    displayMode: 'textarea',                    // Override the widget
    createView: { fieldMode: 'edit' },          // Editable on create
    itemView: { fieldMode: 'read' },            // Read-only on edit
    listView: { fieldMode: 'read' },            // Shown in list view
  },
  validation: {
    isRequired: true,
    length: { min: 3, max: 200 },
  },
  isIndexed: 'unique',                          // DB index (unique)
  isFilterable: true,                           // Can filter in admin + GraphQL
  isOrderable: true,                            // Can sort in admin + GraphQL
  defaultValue: 'Untitled',                     // Default value on create
  hooks: {
    resolveInput: ({ resolvedData }) => {       // Transform on write
      return { ...resolvedData, slug: slugify(resolvedData.title) };
    },
  },
})
```

---

## Hooks (server-side logic on CRUD operations)

```typescript
const Post = list({
  fields: { /* ... */ },
  hooks: {
    // Resolve input — transform data before it's saved
    resolveInput: async ({ resolvedData, operation, item, context }) => {
      if (operation === 'create') {
        resolvedData.createdAt = new Date().toISOString();
        resolvedData.slug = slugify(resolvedData.title);
      }
      if (operation === 'update') {
        resolvedData.updatedAt = new Date().toISOString();
      }
      return resolvedData;
    },

    // Validate input — reject invalid data
    validateInput: async ({ resolvedData, addValidationError }) => {
      if (resolvedData.title && resolvedData.title.length < 3) {
        addValidationError('Title must be at least 3 characters');
      }
      if (resolvedData.status === 'published' && !resolvedData.publishedAt) {
        addValidationError('Published posts must have a publishedAt date');
      }
    },

    // Before change — run side effects before save
    beforeChange: async ({ resolvedData, item, operation, context }) => {
      if (operation === 'create') {
        console.log(`Creating post: ${resolvedData.title}`);
      }
    },

    // After change — run side effects after save
    afterChange: async ({ resolvedData, item, operation, context }) => {
      if (operation === 'create' && resolvedData.status === 'published') {
        await sendNotificationEmail(resolvedData.authorId, resolvedData.title);
        await invalidateCache(`/posts/${resolvedData.slug}`);
      }
    },

    // Before delete
    beforeDelete: async ({ item, context }) => {
      // Prevent deleting posts with comments
      const comments = await context.sudo().db.Comment.count({
        where: { post: { id: { equals: item.id } } },
      });
      if (comments > 0) {
        throw new Error('Cannot delete a post with comments');
      }
    },

    // After delete
    afterDelete: async ({ item, context }) => {
      await deleteImageFromS3(item.heroImage);
    },
  },
});
```

Hooks are how you add business logic without writing CRUD. Common uses:
- **`resolveInput`** — auto-generate slugs, set timestamps, compute fields
- **`validateInput`** — cross-field validation
- **`afterChange`** — send emails, invalidate caches, trigger webhooks
- **`beforeDelete`** — prevent cascading deletes, archive instead

---

## Auth + Sessions

### Email/password auth (built-in via `@keystone-6/auth`)

```typescript
// keystone.ts
import { createAuth } from '@keystone-6/auth';

const { withAuth } = createAuth({
  listKey: 'User',
  identityField: 'email',
  secretField: 'password',
  sessionData: 'id name role',           // What to store in the session
  initFirstItem: {                        // Bootstrap the first admin user
    fields: ['name', 'email', 'password'],
    itemData: { role: 'admin' },
  },
});

export default withAuth(config({
  db: { /* ... */ },
  lists: { User: list({ /* ... */ }) },
  session: {
    // @keystone-6/session-store-redis for Redis-backed sessions
    maxAge: 60 * 60 * 24 * 30,            // 30 days
    secret: process.env.SESSION_SECRET!,
  },
}));
```

The `createAuth` function adds:
- `signIn(email, password)` mutation
- `signOut()` mutation
- `authenticateUser({ email, password })` query
- A sign-in page in the Admin UI

### Custom session strategy (JWT, OAuth, etc.)

```typescript
import { config } from '@keystone-6/core';
import { statelessSessions } from '@keystone-6/core/session';

export default config({
  session: statelessSessions({
    maxAge: 60 * 60 * 24 * 30,
    secret: process.env.SESSION_SECRET!,
    // Custom session data
    sessionData: 'id name email role',
  }),
  lists: { /* ... */ },
});
```

For OAuth (Google, GitHub, etc.), use `passport` in a custom server, then create Keystone sessions from the OAuth callback.

---

## Storage (S3, local, cloud)

```typescript
export default config({
  storage: {
    s3: {
      kind: 's3',
      bucketName: process.env.S3_BUCKET!,
      region: process.env.S3_REGION!,
      accessKeyId: process.env.S3_ACCESS_KEY!,
      secretAccessKey: process.env.S3_SECRET_KEY!,
      // signed: { expiry: 3600 },  // For private files (presigned URLs)
    },
    local_images: {
      kind: 'local',
      type: 'image',
      generateUrl: (path) => `https://cdn.example.com${path}`,
      serverRoute: { path: '/images' },
      storagePath: 'public/images',
    },
  },
  lists: {
    Post: list({
      fields: {
        heroImage: image({ storage: 's3' }),
        thumbnail: image({ storage: 'local_images' }),
      },
    }),
  },
});
```

---

## The GraphQL API

Keystone auto-generates a full GraphQL CRUD API. Query it from any frontend (Astro, Next.js, React Native, etc.):

```graphql
# Query — list posts with filters, sorting, pagination
query {
  posts(
    where: { status: { equals: "published" } }
    orderBy: { publishedAt: desc }
    take: 10
    skip: 0
  ) {
    id
    title
    slug
    excerpt
    author {
      name
      avatar
    }
    publishedAt
  }
}

# Query — single post by ID or slug
query {
  post(where: { slug: "hello-world" }) {
    id
    title
    content
    author {
      name
    }
  }
}

# Mutation — create a post (requires auth)
mutation {
  createPost(data: {
    title: "New Post"
    slug: "new-post"
    content: "Hello world"
    status: "draft"
    author: { connect: { id: "abc123" } }
  }) {
    id
    title
  }
}

# Mutation — update a post
mutation {
  updatePost(
    where: { id: "abc123" }
    data: { status: "published", publishedAt: "2025-01-15T00:00:00.000Z" }
  ) {
    id
    status
  }
}

# Mutation — delete a post
mutation {
  deletePost(where: { id: "abc123" }) {
    id
  }
}
```

The GraphQL playground is available at `/api/graphql` in dev mode — auto-generated from your schema.

### Querying from a frontend (Astro example)

```typescript
// src/lib/keystone.ts
const KEYSTONE_URL = process.env.KEYSTONE_URL || 'http://localhost:3000/api/graphql';

export async function query(gql: string, variables?: Record<string, any>) {
  const res = await fetch(KEYSTONE_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query: gql, variables }),
  });
  const { data, errors } = await res.json();
  if (errors) throw new Error(errors[0].message);
  return data;
}

// Fetch published posts for the blog index
export async function getPublishedPosts() {
  const data = await query(`
    query {
      posts(where: { status: { equals: "published" } }, orderBy: { publishedAt: desc }) {
        id title slug excerpt publishedAt
        author { name }
      }
    }
  `);
  return data.posts;
}
```

---

## Testing

Keystone apps are tested via the GraphQL API or by calling the Keystone context directly:

```typescript
// test/post.test.ts
import { getContext } from '@keystone-6/core/context';
import { config } from '../keystone';
import baseConfig from '../keystone';

const context = getContext(baseConfig, process.env.DATABASE_URL);

beforeEach(async () => {
  await context.sudo().db.Post.deleteMany({});
});

test('createPost creates a post', async () => {
  const post = await context.sudo().db.Post.createOne({
    data: { title: 'Test Post', slug: 'test-post', status: 'draft' },
  });

  expect(post.title).toBe('Test Post');
  expect(post.slug).toBe('test-post');
});

test('afterChange hook sends email', async () => {
  const sendEmail = jest.fn();
  // Mock the email service

  await context.sudo().db.Post.createOne({
    data: { title: 'Published Post', slug: 'published', status: 'published' },
  });

  expect(sendEmail).toHaveBeenCalled();
});

test('access control blocks anonymous create', async () => {
  // Anonymous context (no session)
  await expect(
    context.db.Post.createOne({ data: { title: 'Test', slug: 'test' } })
  ).rejects.toThrow();
});
```

`context.sudo()` bypasses access control (for setup/teardown). `context.db` respects access control (for testing the rules).

Cross-reference: `testing-patterns` for general test pyramid / mocking strategies.

---

## Deployment

Keystone is a standard Node.js app — deploy anywhere Node runs.

```bash
npm run build        # Build the Admin UI + server
npm run start        # Start the production server (port 3000 by default)
```

### Vercel (serverless)

Keystone 6 supports Vercel serverless deployment:

```typescript
// keystone.ts — use the serverless config
import { config } from '@keystone-6/core';

export default config({
  db: { provider: 'postgresql', url: process.env.DATABASE_URL! },
  lists: { /* ... */ },
  server: {
    maxFileSize: 10 * 1024 * 1024,  // 10 MB
    healthCheck: true,
  },
});
```

```bash
vercel --prod
```

### Docker

```dockerfile
FROM node:20-slim AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-slim
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY --from=builder /app/.keystone ./.keystone
COPY --from=builder /app/dist ./dist
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

### Database

Keystone uses Prisma under the hood. The database can be:
- **PostgreSQL** (recommended for production)
- **MySQL**
- **SQLite** (dev/test only — doesn't support all features)

Run migrations after schema changes:

```bash
npx keystone prisma migrate dev --name "add_user_role"
npx keystone prisma migrate deploy  # In CI/CD
```

---

## Top 10 Anti-Patterns (the most valuable section)

1. **Editing `schema.graphql` or `schema.prisma` directly.** These are auto-generated from `keystone.ts`. Manual edits are overwritten on the next build. Always edit the Keystone config (`keystone.ts` / `src/schema/*.ts`), not the generated files.

2. **Not using access control.** `access: allowAll` is the default — anyone can read, create, update, and delete anything. This is fine for dev, dangerous in production. Always define access control rules, even for "internal" apps. The `operation`, `filter`, and `item` levels give you fine-grained control.

3. **Storing sensitive data in `text` fields.** Passwords, API keys, tokens should use the `password` field type (which hashes and never returns the value in GraphQL). Storing secrets in `text` fields exposes them in the admin UI and GraphQL API.

4. **Using `context.sudo()` in production code.** `context.sudo()` bypasses access control — useful in tests and hooks (where you need to query/update related data), but dangerous in handlers. Always use `context.db` (which respects access control) for user-facing operations.

5. **Not using hooks for computed fields.** If a field's value depends on other fields (e.g., `wordCount` from `content`), use a `resolveInput` hook to compute it on write, or a `virtual`/`computed` field to compute it on read. Don't compute it client-side and pass it in — that's inconsistent and racy.

6. **Not running migrations after schema changes.** Adding a field to `keystone.ts` updates the Prisma schema, but doesn't update the database. Run `npx keystone prisma migrate dev` to generate and apply the migration. In production, run `npx keystone prisma migrate deploy`.

7. **Treating Keystone like a generic CRUD framework.** Keystone's value is the auto-generated admin UI + GraphQL API. If you're building custom admin pages or custom GraphQL resolvers for basic CRUD, you're fighting the framework. Use the Admin UI; extend it with custom pages only when necessary.

8. **Not using the `document` field for rich text.** Keystone's `document` field is a full rich text editor (like Notion) with relationship support, code blocks, images. Using `text` or `json` for rich content means you build the editor yourself — reinventing what `document` provides for free.

9. **Not splitting the schema into multiple files for large projects.** A single `keystone.ts` with 20 lists becomes unmaintainable. Split lists into `src/schema/user.ts`, `src/schema/post.ts`, etc., and combine them in `keystone.ts`. Each list definition can also export its hooks, access control, and types.

10. **Using SQLite in production.** SQLite works for dev and tests but has limitations in production (no concurrent writes, no connection pooling, file-based). Always use PostgreSQL for production Keystone deployments. The switch is just changing `provider: 'sqlite'` to `provider: 'postgresql'` and updating `DATABASE_URL` — Keystone handles the rest.

---

## Cross-references

- `framework-templates` — CLAUDE.md generation template for KeystoneJS (project onboarding)
- `nestjs` — Enterprise TypeScript backend (contrast: NestJS builds APIs manually; Keystone generates them from schema)
- `fastify` — High-performance Node API (use as a custom Keystone server if you need non-GraphQL endpoints)
- `astro-5` — Astro is the canonical frontend for Keystone (fetch from Keystone's GraphQL API at build time via the Content Layer API)
- `django-6` — Django admin is the Python equivalent of Keystone's admin UI (different language, similar "auto-generated admin" concept)
- `api-and-interface-design` — Type contract design (Keystone's schema IS the type contract)
- `api-patterns` — REST API patterns (Keystone generates GraphQL, not REST — but the patterns are relevant)
- `security-and-hardening` — OWASP-aware hardening (Keystone's access control system covers most OWASP concerns for CRUD apps)
- `clean-code` — General coding standards applicable to TypeScript
- `testing-patterns` — Test pyramid, mocking strategies
- `code-review-checklist` — 12-category code review checklist

---

## Dependencies

Required:
- **Node.js** 20+ (or Bun 1.1+)
- **KeystoneJS** 6.0+ (`@keystone-6/core`)
- **Prisma** (bundled with Keystone — Keystone generates the schema, Prisma runs migrations)
- **TypeScript** 5+ (default, can opt out but not recommended)
- **A database**:
  - **PostgreSQL** (recommended for production)
  - **MySQL**
  - **SQLite** (dev/test only)

### Official packages

- `@keystone-6/core` — the core framework
- `@keystone-6/auth` — email/password auth (signIn/signOut mutations, sign-in UI)
- `@keystone-6/session-store-redis` — Redis-backed sessions
- `@keystone-6/fields-document` — the `document` rich text field (DocumentField)
- `@keystone-6/document-renderer` — render `document` field content to HTML/React
- `@keystone-6/core/fields` — built-in field types (text, select, relationship, image, etc.)

### Common additions

- `graphql` — the GraphQL runtime (Keystone uses it under the hood)
- `@apollo/server` — if you want to add Apollo Server alongside Keystone (for custom resolvers)
- `passport` + `passport-google-oauth20` etc. — OAuth authentication
- `aws-sdk` (or `@aws-sdk/client-s3`) — S3 storage for images/files
- `slugify` — for auto-generating slugs in `resolveInput` hooks
- `argon2` or `bcrypt` — password hashing (Keystone's `password` field uses bcrypt by default)
- `stripe` — Stripe integration (for e-commerce Keystone apps)
- `algoliasearch` — Algolia search integration (Keystone's built-in search is basic)
- `react` + `react-dom` — for custom Admin UI pages (Keystone's Admin UI is React-based)
- `@keystone-6/core/context` — for accessing the Keystone context outside the server (e.g., in scripts, tests)
