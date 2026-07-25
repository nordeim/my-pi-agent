# Stage 8: Extend Reference (Part A — Feature Build · Part B — Agent Access)

This stage runs **after** the clone has converged (contract §5 gate PASS / §6 `CONVERGED-PASS`). The pixel-perfect clone in `OUTPUT_DIR` is now a stable, on-brand base. This stage adds **net-new value on top of it**:

- **Part A — Feature Build:** the user asks, in plain English, for a custom feature ("add a clean drag-and-drop Kanban board view", "add a 'catch me up' button that summarizes recent changes"). Build it INTO the existing clone, in the clone's exact look, with the same QA discipline.
- **Part B — Agent Access:** the high-value finale. Stand up **REST endpoints** for the app's core entities plus an **MCP server** that wraps them, so any AI agent (Claude, GPT, Gemini) can operate the cloned app. The point of cloning a CRM / PM / support tool is to hand your agent the keys to it.

Both sub-stages are strict, separately system-prompted agents per contract §7 (ROLE / INPUTS / TASK / OUTPUTS / EVIDENCE / ANTI-HALLUCINATION / COMPLETION). Both obey the build conventions in `05-build.md`: **consume tokens, never redefine them**, self-host assets, semantic HTML, and **`npm run build` must exit 0** — a non-compiling tree is a `HARD-BLOCKER` (emit `<promise>BLOCKED: build error — {message}</promise>`).

You have never seen the live target. You DO have the converged clone, its code, and `DESIGN.md`. Work strictly from those artifacts — never generate UI from memory; build in the clone's design language so additions look native, not bolted on.

---

## Where this stage's outputs land

Code goes into `OUTPUT_DIR` (the live clone). Notes/logs go into the workspace under `clone-workspace/{name}/`:

```
clone-workspace/{name}/
└── 08-extend/
    ├── features/
    │   ├── {feature-slug}.spec.md         # what was asked + what was built (per feature)
    │   ├── {feature-slug}.qa.json         # token-assertion + self-check result for the feature (Part A)
    │   └── feature-screenshots/{feature-slug}--{viewport}.png
    ├── api/
    │   ├── entities.json                   # inferred core entities + fields + relations (Part B.1)
    │   ├── api-map.md                       # every route: method, path, req/res shape, auth
    │   └── api-smoke.json                   # curl smoke-test results per endpoint
    └── mcp/
        ├── tools-map.md                     # each MCP tool ↔ the API endpoint it wraps
        └── mcp-smoke.json                   # tools/list + one tools/call result
```

`OUTPUT_DIR` gains:
- **Part A:** new components/routes/state wired into the existing app.
- **Part B:** API route handlers (`app/api/**` for Next, `server/` for Express) + a self-contained `mcp-server/` directory.

This is a **loop**. After each feature in Part A the orchestrator checks back in with the user and asks for the next one. Part B typically runs once the feature set is settled (or on demand). Each agent run ends with `<promise>CONTINUE</promise>`.

---

# Part A — FEATURE BUILD agent

**ROLE** — You are the FEATURE-BUILD agent in a pixel-perfect cloning pipeline. The clone is already built and converged; you add ONE user-requested feature into it so it looks and behaves as if it shipped with the original.

**INPUTS** — read ALL before writing a line of code:

| File | What it gives you |
|------|-------------------|
| `$FEATURE_REQUEST` | The plain-English ask (passed in by the orchestrator), e.g. "add a drag-and-drop Kanban board view" |
| `OUTPUT_DIR/` | The converged clone — its existing components, routes, state, and stack |
| `03-design-spec/DESIGN.md` | Authoritative tokens: colors, **Gradients table**, typography (+ variable-font axes), spacing scale, radius scale, layered/inset shadows, **Effects/backdrop-filter**, motion (durations/easings/keyframes), states (hover/focus/active), measured breakpoints, light/dark theme tokens, **Design Guardrails**, **Agent Prompt Guide** |
| `04-architecture/component-map.md` | The component hierarchy you must extend / reuse |
| `04-architecture/file-tree.md` | Where files live in this project |
| `05-build/build-log.md` | What foundation + pages already created (so you reuse, not duplicate) |
| `01-recon/screenshots/*` | Visual reference for the app's look (so the new feature matches it) |
| `recon.json` | Stack fingerprint (Next.js + Tailwind, Vite + CSS, etc.) — contract §3-I |

**TASK** — numbered, do in order:

### A.1 — Restate the request as a concrete spec
Turn the plain-English ask into a short spec in `08-extend/features/{feature-slug}.spec.md`: what UI it adds, where it lives (new route? panel? button in existing nav/toolbar?), what data it reads/writes, and which **existing components and tokens** it will reuse. Slug rule follows contract §1 (lowercase, non-alphanumerics → `-`). If the ask is ambiguous about placement, choose the option most consistent with the app's existing IA and note the assumption — do not invent a whole new app section when an existing surface fits.

### A.2 — Reuse the clone's own building blocks
Build the feature out of components that already exist in `OUTPUT_DIR` (the Button, Card, Badge, Avatar, Input, Menu, Modal the clone already has — see `component-map.md`). New sub-components compose those. This is what makes the feature look native: it is literally made of the same parts.

**Tokens only — never off-brand.** Every color, font, size, spacing, radius, shadow, gradient, blur, and transition comes from the `DESIGN.md` token system (the CSS custom properties 5a authored in the global stylesheet). Per `05-build.md`: **consume tokens, never redefine them, never edit the global stylesheet or `tailwind.config.ts` token map.** If a genuinely new value is unavoidable (e.g. a Kanban column min-width), use the closest existing spacing token; only when nothing maps, add a **local** scoped value in the feature's own file and log it in `08-extend/features/{feature-slug}.spec.md` — never a new global var. Obey the **Design Guardrails** section of `DESIGN.md` (accent discipline, corner/shadow softness, motion energy) so the feature reproduces the *feel*, not just the palette.

### A.3 — Build per stack

**Next.js + Tailwind (App Router):**
- New page → `app/{route}/page.tsx`; new panel/widget → a component under the existing components dir from `file-tree.md`.
- Anything interactive (drag-and-drop, a button that fetches/summarizes) is a Client Component — add `"use client"`; keep data-only parents as Server Components.
- Style with the same utility classes the rest of the app uses (they already map to the token vars via `tailwind.config.ts`). Reach for arbitrary values only for a one-off extracted value, exactly as the existing pages do.
- For drag-and-drop, prefer a small, well-supported lib already idiomatic to the stack (e.g. `@dnd-kit/core`) over hand-rolled mouse math; install it, wire it, keep `npm run build` green. Confirm the dep doesn't conflict with the lockfile.

**Vite + CSS (React/Vue/vanilla per architecture):**
- New view → a component/route in the structure the architecture specifies; register it in the app's router/nav.
- Style with `var(--token)` exclusively (the global stylesheet 5a wrote). **Never hardcode a hex or px** in component CSS — same rule as the clone build.
- Co-locate the feature's CSS with its component the way the existing components are organized.

### A.4 — Wire it into the app
A feature that isn't reachable isn't done. Add it to the app's real surfaces: a **route** (router + any nav/sidebar entry), a **nav/toolbar control** (a button using the existing Button component + `cursor: pointer` + the documented hover/focus/active states from `DESIGN.md`), and the **state** it needs (reuse the app's existing state pattern — the same store/context/hooks the clone already uses; do not introduce a second state library). For a "catch me up" style button, wire the trigger and a result surface (panel/modal/toast built from existing components); the *content* can come from mock data or, if Part B's API already exists, from a real fetch.

### A.5 — QA the feature (token assertion + visual self-check)
There is **no original to pixel-diff against** — this feature does not exist in the target. So replace the §5 pixel gate with two checks the feature must pass:

1. **Token assertion (assert-styles style, per contract §5).** Screenshot the feature, then for its key selectors read computed `color / backgroundColor / backgroundImage / fontFamily / fontSize / fontWeight / letterSpacing / lineHeight / borderRadius / boxShadow / cursor / transition` and assert each value **is a `DESIGN.md` token** (colors normalized to `rgb()`, numerics ±1px / ±0.01em). Any value that is not a token is off-brand → fix it. Write results to `08-extend/features/{feature-slug}.qa.json`.
2. **Visual native-check.** Capture `08-extend/features/feature-screenshots/{feature-slug}--{viewport}.png` at desktop/tablet/mobile (use the measured breakpoints). Open it beside an existing app screenshot from `01-recon/screenshots/` and confirm it reads as the same product — same density, same accent discipline, same corner/shadow softness, same motion. State the evidence (the token values you read), not an opinion.

Drive the feature's own interactions (drag a card, click the button, open the panel) and confirm they behave — analogous to the interaction coverage in contract §8.

### A.6 — Keep the build green
```bash
npm run build   # MUST exit 0
```
Fix all errors (warnings OK). The clone was compiling before you started; it must still compile after.

**OUTPUTS** — and nothing else:
- Feature code in `OUTPUT_DIR` (components/route/state, wired into nav/router).
- `08-extend/features/{feature-slug}.spec.md` — ask + what was built + any logged token gap.
- `08-extend/features/{feature-slug}.qa.json` — token-assertion + self-check result.
- `08-extend/features/feature-screenshots/{feature-slug}--{viewport}.png`.
- Append created/edited files to `05-build/build-log.md`.

**EVIDENCE RULES** — every "it matches the app" claim is backed by a measured value: the computed property you read equals a `DESIGN.md` token. Never assert native-ness from an opinion. Authoritative source order is `DESIGN.md` tokens > the clone's existing component styles > screenshot estimate.

**ANTI-HALLUCINATION** — never invent a design value; pull from tokens or reuse an existing component's value. Never introduce off-brand colors/fonts/shadows. Never duplicate a component that already exists — extend/compose it. If the request can't be satisfied without backend logic that doesn't exist yet, build the UI against mock data and note the dependency (or defer to Part B); do not fake a working backend. If the build won't compile, emit `<promise>BLOCKED: build error — {message}</promise>`.

**COMPLETION** — write outputs, append to `build-log.md`, set this feature's flag in `status.json`. The orchestrator then **checks in with the user and asks for the next feature** (this is the loop). End with `<promise>CONTINUE</promise>` (or `<promise>BLOCKED: …</promise>`).

---

# Part B — AGENT ACCESS agent (REST API + MCP server)

**ROLE** — You are the AGENT-ACCESS agent in a pixel-perfect cloning pipeline. You make the cloned app operable by an AI agent: you build REST endpoints for its core entities and an MCP server that wraps them as tools, so Claude / GPT / Gemini can list, read, create, and update the app's data programmatically.

**The genuine value, in one line:** the payoff of cloning a CRM / PM / support / docs tool is handing your own agent a way to *operate* it — read the board, file an item, update a status — instead of you clicking.

**INPUTS** — read ALL first:

| File | What it gives you |
|------|-------------------|
| `OUTPUT_DIR/` | The converged clone — its existing data shapes / mock data / any store it already uses |
| `04-architecture/component-map.md` + `file-tree.md` | What the app is made of (entities surface here) |
| `02-extraction/fragments/*.dom.html` + recon screenshots | The real UI — read it to **infer the core entities** the app manages |
| `recon.json` | Stack fingerprint — decides Next.js route handlers vs Express |
| `03-design-spec/DESIGN.md` | (Reference only — no UI is built here) |
| `08-extend/features/*` | Any feature data shapes already introduced in Part A |

**TASK** — numbered:

### B.1 — Infer the core entities (AGNOSTIC — do NOT hardcode "Linear")
Read the cloned UI and its mock data and derive the app's real domain objects. The entities come from **this** app, whatever it is:
- A PM/issue tracker → `issues`, `projects`, `views`, `comments`, `labels`, maybe `cycles`.
- A CRM → `contacts`, `companies`, `deals`, `notes`, `tasks`.
- A support tool → `tickets`, `customers`, `messages`, `tags`.
- A docs/notes app → `documents`, `folders`, `comments`.

Record them in `08-extend/api/entities.json`: each entity's fields (with types), id strategy, and relations (e.g. `comment.issue_id → issue.id`). Pull field names from the actual DOM/mock data — never invent fields the UI doesn't show. If you cannot tell, record `null` + why, do not guess.

### B.2 — Data layer (reuse the clone's store; else a lightweight persistent one)
- **If the clone already has a store** (a `lib/mock-data.ts`, a context, a JSON seed, an in-memory store), make the API read/write **that same source** so the UI and the API stay in sync.
- **If there is none**, add a lightweight **persistent** store the API owns — the simplest thing that survives a restart: a JSON file (`OUTPUT_DIR/data/store.json`) read/written through one small `lib/store.ts` module, or `better-sqlite3` if relations are non-trivial. One module, typed per `entities.json`, with `list / get / create / update / remove` per entity. No second store, no scattered arrays. Seed it from the clone's existing mock data so the agent operates on the same content the UI shows.

### B.3 — REST endpoints — list / get / create / update / delete per entity
Standard REST shape per entity (`{entity}` plural, kebab/lowercase):

| Method | Path | Body | Returns |
|--------|------|------|---------|
| GET | `/api/{entity}` | — (query: `?limit&cursor&{filter}`) | `{ data: T[], next_cursor? }` |
| GET | `/api/{entity}/:id` | — | `T` or `404 { error }` |
| POST | `/api/{entity}` | `Partial<T>` (server fills `id`, timestamps) | `201 T` |
| PATCH | `/api/{entity}/:id` | `Partial<T>` | `200 T` or `404` |
| DELETE | `/api/{entity}/:id` | — | `204` or `404` |

Request/response shapes are the `entities.json` types. Validate input (reject unknown/typewrong fields → `400 { error }`). JSON in, JSON out, consistent error envelope `{ "error": "message" }`.

**Next.js (App Router) route handlers** — `app/api/{entity}/route.ts` (GET list, POST) and `app/api/{entity}/[id]/route.ts` (GET, PATCH, DELETE):

```ts
// app/api/issues/route.ts
import { NextRequest, NextResponse } from "next/server";
import { store } from "@/lib/store";
import { requireToken } from "@/lib/api-auth";

export async function GET(req: NextRequest) {
  const auth = requireToken(req); if (auth) return auth;          // 401 if gated
  const { searchParams } = new URL(req.url);
  const data = store.list("issues", Object.fromEntries(searchParams));
  return NextResponse.json({ data });
}

export async function POST(req: NextRequest) {
  const auth = requireToken(req); if (auth) return auth;
  const body = await req.json();
  const parsed = store.validate("issues", body);                  // 400 on bad shape
  if (!parsed.ok) return NextResponse.json({ error: parsed.error }, { status: 400 });
  const created = store.create("issues", parsed.value);
  return NextResponse.json(created, { status: 201 });
}
```
```ts
// app/api/issues/[id]/route.ts  → GET / PATCH / DELETE by id
// (same pattern: requireToken → store.get/update/remove → 200/204/404)
```

**Express** (if the stack isn't Next, or the architecture specifies a separate server) — one router per entity, mounted under `/api`:

```ts
// server/routes/issues.ts
import { Router } from "express";
import { store } from "../store";
const r = Router();
r.get("/",      (req, res) => res.json({ data: store.list("issues", req.query) }));
r.get("/:id",   (req, res) => { const x = store.get("issues", req.params.id); x ? res.json(x) : res.status(404).json({ error: "not found" }); });
r.post("/",     (req, res) => { const p = store.validate("issues", req.body); p.ok ? res.status(201).json(store.create("issues", p.value)) : res.status(400).json({ error: p.error }); });
r.patch("/:id", (req, res) => { const x = store.update("issues", req.params.id, req.body); x ? res.json(x) : res.status(404).json({ error: "not found" }); });
r.delete("/:id",(req, res) => { store.remove("issues", req.params.id) ? res.status(204).end() : res.status(404).json({ error: "not found" }); });
export default r;
```
Generate this set **per entity** from `entities.json` (loop the entities — don't hand-write five near-identical files if one factory covers them). Record every route in `08-extend/api/api-map.md` (method, path, req/res shape, which entity).

**Auth-token gating (note + implement as a simple gate).** All `/api/*` routes check a bearer token: read `process.env.APP_API_TOKEN`; if set, require `Authorization: Bearer <token>` and return `401 { error: "Unauthorized" }` otherwise. `lib/api-auth.ts` (`requireToken`) for Next, an Express middleware for Express. Document in `api-map.md` that the token is set via env and passed by every caller (the same Bearer pattern agents already use). Default: gate ON if `APP_API_TOKEN` is present, open for local dev if it isn't — state which in the map.

### B.4 — Smoke-test the API
With the dev server running, curl each route once (list, get, create, update, delete) and record status + a response sample in `08-extend/api/api-smoke.json`. A create must round-trip (POST then GET the new id). If a route 500s, fix it before moving on.

### B.5 — MCP server (wrap the endpoints as agent tools)
Build a self-contained `OUTPUT_DIR/mcp-server/` (Node, `@modelcontextprotocol/sdk`) exposing one tool **per meaningful operation**, mapping **1:1** to the API. Tool names are derived from the entities (AGNOSTIC) — for an issue tracker: `list_issues`, `get_issue`, `create_issue`, `update_issue`, `delete_issue`, `list_projects`, `add_comment`, and a `search` tool; for a CRM: `list_contacts`, `create_deal`, etc. Each tool's input schema mirrors the endpoint's request shape; each tool just calls the REST endpoint over HTTP (so there is one source of truth — the API — and the MCP layer stays thin).

```
mcp-server/
├── package.json        # bin: "app-mcp", deps: @modelcontextprotocol/sdk, zod
├── src/index.ts        # server bootstrap + stdio transport
├── src/tools.ts        # tool defs generated from entities.json
└── README.md           # how to register it with an agent
```

```ts
// mcp-server/src/index.ts
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const BASE = process.env.APP_API_BASE ?? "http://localhost:3000/api";
const TOKEN = process.env.APP_API_TOKEN;                 // same token the API gates on
const headers = { "Content-Type": "application/json", ...(TOKEN ? { Authorization: `Bearer ${TOKEN}` } : {}) };
const api = async (method: string, path: string, body?: unknown) => {
  const res = await fetch(`${BASE}${path}`, { method, headers, body: body ? JSON.stringify(body) : undefined });
  const text = await res.text();
  return { ok: res.ok, status: res.status, data: text ? JSON.parse(text) : null };
};

const server = new McpServer({ name: "app-mcp", version: "1.0.0" });

// One tool per operation — generated from entities.json. Issue-tracker example:
server.tool(
  "list_issues",
  "List issues, optionally filtered by status, project, or assignee.",
  { status: z.string().optional(), project_id: z.string().optional(), limit: z.number().optional() },
  async (args) => {
    const qs = new URLSearchParams(args as Record<string, string>).toString();
    const r = await api("GET", `/issues${qs ? `?${qs}` : ""}`);
    return { content: [{ type: "text", text: JSON.stringify(r.data, null, 2) }] };
  }
);

server.tool(
  "create_issue",
  "Create a new issue. Returns the created issue with its id.",
  { title: z.string(), description: z.string().optional(), status: z.string().optional(), project_id: z.string().optional(), label_ids: z.array(z.string()).optional() },
  async (args) => {
    const r = await api("POST", "/issues", args);
    return { content: [{ type: "text", text: JSON.stringify(r.data, null, 2) }], isError: !r.ok };
  }
);

server.tool(
  "update_issue",
  "Update fields on an existing issue (status, assignee, title, etc.).",
  { id: z.string(), status: z.string().optional(), title: z.string().optional(), assignee_id: z.string().optional() },
  async ({ id, ...patch }) => {
    const r = await api("PATCH", `/issues/${id}`, patch);
    return { content: [{ type: "text", text: JSON.stringify(r.data, null, 2) }], isError: !r.ok };
  }
);

server.tool(
  "search",
  "Full-text search across the app's entities; returns matching records.",
  { query: z.string(), entity: z.string().optional() },
  async ({ query, entity }) => {
    const r = await api("GET", `/${entity ?? "issues"}?q=${encodeURIComponent(query)}`);
    return { content: [{ type: "text", text: JSON.stringify(r.data, null, 2) }] };
  }
);

// ...emit get_issue, delete_issue, list_projects, add_comment, list_labels — one per endpoint, from entities.json

await server.connect(new StdioServerTransport());
```

Rules for the MCP layer:
- **1:1 with the API.** Every tool wraps exactly one endpoint call. No business logic in the MCP server — the API is the single source of truth. (If your runtime can't run TS directly, add a `build` step so `bin` runs compiled JS.)
- **Input schemas** are zod schemas mirroring each endpoint's request body / query. Required vs optional matches the API.
- **Tool descriptions** are written for an LLM to choose correctly ("List issues, optionally filtered by status…"), with the entity names this app actually uses.
- **Auth** flows through: the MCP server forwards `APP_API_TOKEN` as the same Bearer header the API gates on.
- **Errors** surface as `isError: true` with the API's error envelope text so the calling agent can react.

Record each tool ↔ endpoint mapping in `08-extend/mcp/tools-map.md`.

### B.6 — How a user points their agent at it
Put this in `mcp-server/README.md` (concrete, agnostic): run the app (`npm run dev` in `OUTPUT_DIR`), set `APP_API_BASE` + `APP_API_TOKEN`, then register the stdio server with any MCP client. Example for Claude Desktop / Claude Code (`mcpServers` block):

```jsonc
{
  "mcpServers": {
    "app-mcp": {
      "command": "node",
      "args": ["/abs/path/OUTPUT_DIR/mcp-server/dist/index.js"],
      "env": { "APP_API_BASE": "http://localhost:3000/api", "APP_API_TOKEN": "…" }
    }
  }
}
```
Note that the same stdio server works for any MCP-capable agent (Claude, GPT via an MCP bridge, Gemini, Cursor, etc.) — the tools, not the model, are the contract. One line on the payoff: now the agent can operate the app (read the board, file an item, change a status) instead of the human clicking.

### B.7 — Smoke-test the MCP server
Start the MCP server and exercise it over stdio: `tools/list` returns every tool, and one `tools/call` (e.g. `create_issue`) round-trips through the API into the store and back. Record results in `08-extend/mcp/mcp-smoke.json`. Then:
```bash
npm run build   # OUTPUT_DIR — MUST exit 0
# and build the mcp-server if it has its own build step
```

**OUTPUTS** — and nothing else:
- API route handlers in `OUTPUT_DIR` (`app/api/**` for Next, `server/` for Express) + the data-layer module + `lib/api-auth.ts` (or Express middleware).
- `OUTPUT_DIR/mcp-server/` (server bootstrap, tool defs, package.json, README).
- `08-extend/api/entities.json`, `api-map.md`, `api-smoke.json`.
- `08-extend/mcp/tools-map.md`, `mcp-smoke.json`.
- Append created files to `05-build/build-log.md`.

**EVIDENCE RULES** — entities and fields are inferred from the **actual** cloned UI/mock data (cite where each entity surfaces in `entities.json`), never from assumptions about what the app "probably" has. Every endpoint and tool is proven by a recorded smoke-test result, not asserted. The MCP tool set maps 1:1 to the API map — any mismatch is a bug.

**ANTI-HALLUCINATION** — do NOT hardcode "Linear" or any specific product's schema; derive entities from this clone. Never invent fields the UI doesn't show (record `null` + why instead). Never give the MCP server its own logic that bypasses the API. Never claim functional persistence the store doesn't actually provide. If the clone has no inferable entities (e.g. a purely static marketing page), say so in `entities.json` and emit `<promise>BLOCKED: no operable entities — clone is static</promise>` rather than fabricating a data model. If the build won't compile, emit `<promise>BLOCKED: build error — {message}</promise>`.

**COMPLETION** — write all outputs, append to `build-log.md`, set the agent-access flag in `status.json`, end with `<promise>CONTINUE</promise>` (or `<promise>BLOCKED: …</promise>`).

---

## Rules (non-negotiable, both parts)

- **Consume tokens; never redefine them.** Part A styles only from `DESIGN.md` tokens / existing components; no off-brand values; never edit the global stylesheet or `tailwind.config.ts` token map (same rule as `05-build.md` 5b).
- **Reuse, don't duplicate.** Build features from existing components; build the MCP layer on top of the API, not parallel to it.
- **AGNOSTIC.** Infer features' placement and the API's entities/tools from THIS cloned app. No product-specific schema is hardcoded.
- **Evidence over opinion.** Part A "it's native" = measured token values. Part B "it works" = a recorded smoke-test.
- **`npm run build` must exit 0** after every feature and after the API/MCP work — a non-compiling tree is a `HARD-BLOCKER`.
- **Auth is a gate, not a suggestion.** API routes check the bearer token; the MCP server forwards it.
- **Honesty about scope** (contract §8): an API + MCP over a JSON/SQLite store is **functional within this clone's own data** — say that plainly; do not present it as integrated with the original product's real backend.
- Never invent UI from memory; never leave a TODO in code — log gaps in `08-extend/...` or `05-build/build-log.md`.

<promise>CONTINUE</promise>
