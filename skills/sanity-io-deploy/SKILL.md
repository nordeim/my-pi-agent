---
name: sanity-io-deploy
description: Connect an existing Next.js app to a standalone Sanity Studio — confirm/scaffold the Studio as a sibling folder (never embedded), fix dangling schema references, deploy the schema and Studio UI to Sanity hosting, mint a read token + webhook secret, wire env vars, add CORS, verify the live deployment with a fresh headless browser + Content Lake query, and rotate any committed secrets. Use when a task references a Sanity onboarding doc, "connect Sanity to my existing Next.js app", a standalone Studio in a sibling folder, or any of `sanity login`, `sanity schema deploy`, `sanity deploy`, `sanity tokens`, `sanity cors`, `sanity hooks`. Companion to `sanity-best-practices`. EXPANDED with lessons from a real production deployment (project v2gzd4bc / stillwater monorepo, 2026-07-13): provider selection, project-access verification, token-mint capture traps, deploy-flag differences, interactive-only webhook CLI, and secret-rotation hygiene.
---

# Sanity Studio: Setup, Configuration, Deployment & Verification (expanded, field-tested)

A playbook for wiring an existing Next.js app to a **standalone** Sanity Studio and getting it
live without the usual false starts. Every command below was run against a real project
(`v2gzd4bc`, dataset `production`, Studio folder `apps/studio` beside a `stillwater` monorepo,
deployed Studio at `stillwater.sanity.studio`, appId `fa2ndc897dahn4e7nugimfs2`). The gotchas
list the exact error strings you will hit and the precise fix for each — including the ones
discovered mid-run that the original playbook did not cover.

---

## 1. Mental model (read this first)

Two completely separate things get deployed, and confusing them is the #1 source of wasted time:

| Artifact | Command | Lives at | Purpose |
|---|---|---|---|
| **Schema** (content model) | `sanity schema deploy` | Content Lake (`<projectId>.api.sanity.io`) | Defines document types the app queries |
| **Studio UI** (authoring app) | `sanity deploy` | `<hostname>.sanity.studio` | The editing interface humans log into |

- `sanity schema deploy` does **NOT** publish the Studio. A Studio URL returning
  `404 "Studio not found"` almost always means the *schema* was deployed but the *UI* was not.
- The app never talks to `*.sanity.studio`. It reads the **Content Lake API**
  (`https://<projectId>.api.sanity.io/...`) via the public CDN. The Studio is only for authors.
- **Standalone Studio rule:** the Studio is its own folder next to the app, **not** embedded
  inside it. Embedding (`next-sanity/studio`) is explicitly not recommended by Sanity — slower
  builds, no auto-updates, no TypeGen watch mode. Keep it sibling.

---

## 2. Pre-flight: folder layout & which Studio is canonical

The working directory is usually a **parent** folder with the Studio and the app as siblings:

```
some-parent/
├── studio/  (or apps/studio, or studio-stillwater)   ← Sanity Studio (standalone)  [THE studio]
└── web/     (or apps/web, or the repo root)           ← Next.js app                  [THE app]
```

Do this **before** anything else:
1. Confirm both folders are visible from your cwd. If you only see the app's source, **stop** —
   you won't be able to see the Studio.
2. Identify the Studio folder: a sibling with its own `package.json` + `sanity.config.ts`.
3. **Confirm the Studio actually has schemas** (see §4 / G1). A Studio scaffolded by the
   onboarding wizard ships an **EMPTY** schema (`schemaTypes = []`) — deploying it "succeeds"
   with 0 types and the app queries return nothing.

### "Two studios" trap (G2)
A monorepo may already contain `apps/studio/` (env-var projectId, possibly unconnected) **and**
a sibling `studio-*` folder (hardcoded projectId). **Treat the folder that actually contains the
real content schemas as canonical** and deploy from there. In the stillwater run, `apps/studio`
held the 8 real schemas; the sibling `studio-stillwater/` was an empty stub — so `apps/studio`
was the deploy source. Don't silently pick one; if ambiguous, ask the user.

---

## 3. Phase 0 — Safety & secret hygiene (do FIRST)

- **Never commit Sanity tokens.** If a Studio's `.env.local` is tracked in git (this happens more
  than you'd think — in the stillwater repo, `apps/web/.env.local` was committed containing a real
  `SANITY_API_TOKEN`, `SANITY_WEBHOOK_SECRET`, `BETTER_AUTH_SECRET`, and an SSH private key was in
  history), treat every value in it as **compromised**.
- Plan to **mint a FRESH token** (not reuse the committed one) and **purge** the file(s) from git
  history: `git filter-repo --invert-paths --path apps/web/.env.local --path docs/ssh-key.txt`
  (note: the root `.env.local` alone is NOT enough — cover every tracked secret path).
- The app's Sanity client should have a **null fallback** (returns `null` when env vars are
  missing) so `next build` succeeds without secrets. Keep that; do not rewrite the client.
- Use the **local binary** (`./node_modules/.bin/sanity`), not `pnpm exec sanity` — the latter
  triggers an esbuild install-guard (G4).

---

## 4. Phase 1 — Auth: login AND verify project access

### 4.1 `sanity login` needs `--provider` in unattended/headless mode (G12)
Without it you get:
```
Error: Login failed: Multiple login providers available: google, github, sanity.
Use `--provider <name>` to select one in unattended mode.
```
Fix: `./node_modules/.bin/sanity login --provider google` (or `--provider github`).
**The provider you choose determines WHICH Sanity account you authenticate as** — pick the one
that *owns or is a member of* the target project.

### 4.2 Verify access BEFORE deploying (G11 — discovered mid-run)
After login, the CLI prints `Login successful` — but that only means *an* account authenticated.
It does **NOT** mean that account can touch your target project. Run:
```bash
cd <studio>
export SANITY_STUDIO_PROJECT_ID=<projectId>
export SANITY_STUDIO_DATASET=production
./node_modules/.bin/sanity projects list
./node_modules/.bin/sanity datasets list
```
- `projects list` returns the projects this account can see. **If it is EMPTY**, the account has
  **zero projects** → `schema deploy` / `sanity deploy` will fail with
  `Unauthorized - User is missing the required grant sanity.project.datasets/read`.
  - This happened: logging in via **Google** yielded 0 projects; switching to **GitHub** surfaced
    `v2gzd4bc` ("Stillwater", 2 members). Always confirm the target project is listed.
- `datasets list` should show `production`. If it says `Unauthorized`, the token isn't being read
  or is invalid (see G13).

### 4.3 Are you logged in? (G6)
There is **no `sanity whoami` command**. To confirm a session, check the auth store:
```bash
ls -la ~/.config/sanity/    # Linux: token lives in ~/.config/sanity/config.json (key: authToken)
# macOS: ~/Library/Application Support/sanity ; Windows: %LOCALAPPDATA%/sanity
```
Note (G13): on Linux the session token is written to `~/.config/sanity/config.json` (NOT
`~/.sanity/`). `projects list` returning an *empty* (not Unauthorized) result means the token is
valid but the account has no projects.

### 4.4 Schema present? (G1)
Look in `schemas/` (monorepo style) or `schemaTypes/` (clean template). If
`index.ts`/`schemaTypes/index.ts` exports `[]`, populate it from the real content types first, then
`rewrite the index to export them`. A fresh Studio has an empty schema and will deploy "1/1 schemas"
with 0 types.

### 4.5 Dangling reference check (G3, G20) — do this BEFORE `schema deploy`
`Sanity schema deploy` **validates every reference target**. A `reference` to a type that doesn't
exist in the schema set fails the deploy:
```
[ERROR] [homePage]
  featuredClasses[...].<unnamed_type_@_index_0>
    ✖ Unknown type: class.
[ERROR] [instructorBio]
  classesTeaching[...].<unnamed_type_@_index_0>
    ✖ Unknown type: class.
```
**Cause:** `homePage.featuredClasses` / `instructorBio.classesTeaching` were `array` of
`reference` to a `class` type that does not exist in Sanity (classes live in PostgreSQL, not
Sanity — ADR-005: Sanity = marketing content only). **Fix:** remove those two dangling fields from
the Sanity schemas (edit `homePage.ts` and `instructorBio.ts`). Leave the *app's* GROQ projections
of `featuredClasses` / `classesTeaching` untouched — projecting a now-absent field is a harmless
no-op (`undefined`). General rule: every `to: [{ type: 'X' }]` must have a matching defined type in
the same schema set. Scan first:
```bash
grep -rn "to: \[{ type:" <studio>/schemas/   # every target type must be defined in the set
```

---

## 5. Phase 2 — Deploy the schema (validates references!)

```bash
cd <studio>
export SANITY_STUDIO_PROJECT_ID=<projectId>
export SANITY_STUDIO_DATASET=production
./node_modules/.bin/sanity schema deploy
./node_modules/.bin/sanity schema list
```
- `schema deploy` prints `Deployed 1/1 schemas` — that is **1 schema *set*** (which contains all N
  document types), not 1 type (G19). The real proof is **0 reference errors**.
- `schema list` confirms the schema set exists in the project.
- If you hit `Unknown type: …` (G3), fix the schema and re-deploy.

---

## 6. Phase 3 — Frontend env wiring (G7)

The app reads these from its **own** `.env.local` (Next.js loads `.env.local` from the directory it
runs in — usually `apps/web/.env.local`, **not** the monorepo root). Set them in BOTH the app's env
and the root env for safety:

```dotenv
# ─── Sanity CMS ────────────────────────────────────────────────────
NEXT_PUBLIC_SANITY_PROJECT_ID=<projectId>
NEXT_PUBLIC_SANITY_DATASET=production
SANITY_API_TOKEN=<viewer token>          # server-only
SANITY_WEBHOOK_SECRET=<webhook secret>   # server-only
```
- `NEXT_PUBLIC_*` are public (safe in `.env.example` as a hint).
- `SANITY_API_TOKEN` / `SANITY_WEBHOOK_SECRET` are **secrets** — keep them only in `.env.local`,
  never in `.env.example` (committed). The client's null-fallback means the app builds without them.
- `SANITY_STUDIO_PROJECT_ID` / `SANITY_STUDIO_DATASET` are **deploy-time only** (read by
  `sanity.cli.ts` / `sanity.config.ts`); they are NOT needed in the web app's runtime env.

---

## 7. Phase 4 — Mint read token (viewer) + webhook secret (G14, G15)

### 7.1 Mint a viewer token — capture the key correctly
```bash
cd <studio>
export SANITY_STUDIO_PROJECT_ID=<projectId>
export SANITY_STUDIO_DATASET=production
./node_modules/.bin/sanity tokens add "stillwater-web-read" --role viewer --yes > /tmp/tok.txt 2>&1
grep -oE "sk[A-Za-z0-9]+" /tmp/tok.txt | head -1 > /tmp/sanity_key.txt
```
- **Do NOT use `--json`** to capture (G14): redirecting `--json` produced an *empty* file in the
  real run — the key lands in the human-readable stdout line `Token: sk…`. Capture both streams
  and `grep` for `sk…`.
- The key is shown **ONCE** ("this is your only chance to do so!"). Save it immediately.
- **Label conflict (G15):** re-running with the same label fails with
  `Conflict - Token with same label already exists`. Either mint with a **unique label**, or delete
  the old one. Note: `sanity tokens remove <id>` is **NOT** a valid subcommand in v6.3.0 — use
  `sanity tokens delete <id>` or remove it in the Sanity Cloud UI (API → Tokens).
- Put the key into `SANITY_API_TOKEN` (apps/web/.env.local + Vercel). Use **viewer** (read-only) —
  never an editor/admin token.

### 7.2 Generate a webhook secret
```bash
openssl rand -base64 32 > /tmp/sanity_webhook_secret.txt   # → SANITY_WEBHOOK_SECRET
```
(The handler HMAC-verifies the `sanity-webhook-signature` header over the raw body; the secret
format — base64 or hex — doesn't matter as long as both sides use the same string.)

---

## 8. Phase 5 — CORS origins (G18)

```bash
./node_modules/.bin/sanity cors add http://localhost:3000 --credentials
./node_modules/.bin/sanity cors add https://<your-domain> --credentials
./node_modules/.bin/sanity cors list
```
- The Studio itself is auto-added as `http://localhost:3333`.
- `Conflict - Duplicate origin already exists for this project` is **benign** (G18) — the origin was
  already registered. Verify with `cors list`. Expected after a normal run:
  `http://localhost:3333`, `http://localhost:3000`, `https://<your-domain>` (and possibly
  `https://<your-studio-host>`).

---

## 9. Phase 6 — Deploy the Studio UI (corrected flags, G16)

Schema deployed ≠ Studio live. Deploy the UI:
```bash
cd <studio>
export SANITY_STUDIO_PROJECT_ID=<projectId>
export SANITY_STUDIO_DATASET=production
./node_modules/.bin/sanity deploy --url=stillwater --yes --schema-required
```
- **No `--title` flag** in v6.3.0 (G16) — `sanity deploy --title "X"` errors with
  `Nonexistent flag: --title`. The title is unnecessary; `--url` + `--yes` suffices.
- `--schema-required` makes the deploy fail fast if the schema isn't deployed (good safety).
- `--url=stillwater` → `https://stillwater.sanity.studio`. If the hostname is taken, pick another
  (e.g. `stillwater-studio`).
- On success it prints `Add appId: 'fa2ndc897dahn4e7nugimfs2' to the deployment section in
  sanity.cli.ts`. **Pin it** so future deploys don't re-prompt:
  ```ts
  export default defineCliConfig({
    api: { projectId: process.env.SANITY_STUDIO_PROJECT_ID ?? 'placeholder-project-id', dataset: 'production' },
    deployment: { appId: 'fa2ndc897dahn4e7nugimfs2' },
  })
  ```

---

## 10. Phase 7 — ISR webhook (Cloud UI; CLI is interactive-only, G17)

The app already has the handler (e.g. `apps/web/src/app/api/sanity/webhook/route.ts`) that
HMAC-verifies `SANITY_WEBHOOK_SECRET`. **`sanity hooks create` is interactive-only** (G17) — it has
no flags for URL/secret/triggers (only `-p project-id`). You cannot script it non-interactively.
Create it in the **Sanity Cloud UI**:
- Sanity Manage → your project → **API** → **Webhooks** → **Create webhook**
  - Name: `stillwater-isr-revalidation`
  - URL: `https://<domain>/api/sanity/webhook` (dev: `http://localhost:3000/api/sanity/webhook`)
  - HTTP method: `POST`
  - HTTP Headers: `{ "Content-Type": "application/json" }`
  - Secret: the value in `SANITY_WEBHOOK_SECRET`
  - Trigger on: **Create, Update, Delete**
- The handler maps content types → routes (e.g. `blogPost` → `/blog`, `homePage` → `/`) and calls
  `revalidatePath()`. Publish a blog post → the live page updates within seconds.

> If the webhook handler's own comment points at the Studio domain (e.g.
> `https://stillwater.studio/api/sanity/webhook`), that is a **misleading comment** — the webhook
> target is the *web app* domain (`https://stillwater.jesspete.shop/...`), not the Studio. Fix the
> comment; the route path is correct.

---

## 11. Phase 8 — Create initial content

Author in the Studio UI (`https://<hostname>.sanity.studio/`): Site Settings, Home, About, ≥1 Blog
Post, Instructor Bios, FAQs/Testimonials/Announcements. **Do not** expect fields you removed in §4.5
(Featured Classes / Classes Teaching). Set `published = true` on each so marketing pages render.

---

## 12. Phase 9 — Verify (fresh browser + Content Lake) (G8, G9, G23)

### 12.1 Content Lake API query (no auth needed for the public dataset)
```
curl -s "https://<projectId>.api.sanity.io/v2021-06-07/data/query/production?query=*%5B_type%20%3D%3D%20%22siteSettings%22%5D%5B0%5D"
```
Expected: `{"query":"*[_type == \"siteSettings\"][0]","result":null,"syncTags":["s1:..."],"ms":3}`
→ dataset is live and the schema is valid (just no content yet).

### 12.2 Fresh headless-browser check (the definitive "Studio is live" proof)
Use the native `agent_browser` tool (NOT a bash `agent-browser` invocation). Recipe:
`open` → `eval --stdin`. **Always use `sessionMode: "fresh"`** — a reused session serves a stale
404.
```js
// agent_browser args: ["open", "https://<hostname>.sanity.studio/"]  (sessionMode: "fresh", timeoutMs: 90000)
// then:  agent_browser args: ["eval", "--stdin"]  (sessionMode: "auto")
// stdin code (must be an EXPRESSION, no top-level return — G9):
JSON.stringify({ url: location.href, title: document.title,
  body: (document.body ? document.body.innerText : '').replace(/\s+/g,' ').slice(0,200) })
```
- **Before deploy:** `https://<hostname>.sanity.studio/` returns a body of
  `{"statusCode":404,"error":"Not Found","message":"Studio not found"}`.
- **After deploy (fresh session):** redirects to
  `https://www.sanity.io/login?type=token&origin=…/studio/<appId>` and the page **title is
  "Log in to Sanity"**. **That redirect is the proof the Studio is live** (the headless browser
  just isn't authenticated). Confirm the `appId` in the redirect URL matches the one pinned in
  `sanity.cli.ts`.
- **`open` can exceed the 35s default watchdog** on slow auth redirects → pass `timeoutMs: 90000`.
- **`eval` code is an expression**, not a statement. Use `(() => {...})()` or a bare expression;
  never a bare `return`.
- **`args` must be an array of strings.** Multi-part calls (`["eval","--stdin"]`) go in `args`;
  the script body goes in the `stdin` param — not nested arrays.

---

## 13. Critical gotchas (exact errors → exact fixes)

| # | Symptom | Fix |
|---|---|---|
| G1 | Fresh Studio has empty schema (`schemaTypes = []`); app queries return nothing | Populate schemas from real content types; rewrite `index.ts`; redeploy |
| G2 | "Two studios" trap (monorepo `apps/studio` + sibling `studio-*`) | Deploy from the folder that holds the real schemas; ask if ambiguous |
| G3 | `Unknown type: class.` at schema deploy | Remove dangling `reference` fields (`featuredClasses`, `classesTeaching`) from Sanity schemas; classes live in Postgres |
| G4 | `pnpm exec sanity` triggers esbuild install-guard | Call `./node_modules/.bin/sanity` directly |
| G5 | Invalid `pnpm-workspace.yaml` placeholder | Set `allowBuilds.esbuild: true` (real boolean) |
| G6 | `sanity whoami` is not a command | Check `~/.config/sanity/` (Linux) / `~/Library/...` (macOS) for a session |
| G7 | Env var location — set in root `.env.local` but app reads `your-project-id` | Next.js reads `.env.local` from `apps/web/`; set it there (+ root mirror) |
| G8 | Reused browser session shows stale 404 after deploy | Re-check with `sessionMode: "fresh"`; fresh session redirects to Sanity login = proof live |
| G9 | `agent-browser` eval "Illegal return statement" | eval code is wrapped in a function; use a pure expression or IIFE |
| G10 | Secrets in `.env.example` | Keep `.env.example` placeholders; real secrets only in `.env.local` |
| **G11** | `Login successful` but `schema deploy` → `Unauthorized / missing grant sanity.project.datasets/read` | After login run `sanity projects list`; if empty, the account lacks project access — re-login with the account that owns the target project |
| **G12** | `Login failed: Multiple login providers available` | `sanity login --provider google|github`; provider selects which Sanity account authenticates |
| **G13** | Token stored at `~/.config/sanity/config.json` (Linux), not `~/.sanity/`; empty `projects list` = valid token, no projects | Know the real auth-store path; empty (vs Unauthorized) distinguishes "no projects" from "no token" |
| **G14** | `sanity tokens add --json` → empty captured file; key lost | Run without `--json`, capture both streams, `grep -oE "sk[A-Za-z0-9]+"`; key shown once |
| **G15** | `Conflict - Token with same label already exists` | Use a unique label, or `sanity tokens delete <id>` / Cloud UI (NOT `tokens remove`) |
| **G16** | `Nonexistent flag: --title` on `sanity deploy` | Drop `--title`; use `sanity deploy --url=<host> --yes --schema-required` |
| **G17** | `sanity hooks create` has no URL/secret/trigger flags | Create the ISR webhook in the Sanity Cloud UI (API → Webhooks) |
| **G18** | `Conflict - Duplicate origin already exists` on `cors add` | Benign — origin already registered; verify with `cors list` |
| **G19** | `Deployed 1/1 schemas` looks like only 1 type | It's 1 schema *set* containing all N types; 0 reference errors is the real proof |
| **G20** | Dangling `reference` to a non-Sanity type (e.g. `class`) | Remove the field from the Sanity schema; keep GROQ projections (harmless no-op) |
| **G21** | App can't read Sanity vars from root env | Put `NEXT_PUBLIC_SANITY_*` + secrets in `apps/web/.env.local` |
| **G22** | Studio `.env.local` (and SSH key) committed to git | Mint fresh token (rotate), purge via `git filter-repo --invert-paths --path <every-secret-file>`; client null-fallback keeps build working |
| **G23** | Can't tell if Studio is actually live | Fresh `agent-browser` session → redirect to `sanity.io/login?…/studio/<appId>` = live; Content Lake query → `result:null`+`syncTags` |
| **G24** | Webhook handler comment points at Studio domain | The webhook targets the *web app* domain; fix the comment (route path is correct) |

---

## 14. Command cheat-sheet (verified working)

```bash
cd <studio>

# Auth + verify access (G11/G12)
./node_modules/.bin/sanity login --provider github
export SANITY_STUDIO_PROJECT_ID=<projectId>
export SANITY_STUDIO_DATASET=production
./node_modules/.bin/sanity projects list      # MUST list target project
./node_modules/.bin/sanity datasets list      # MUST list 'production'

# Schema (validates references — catches G3)
./node_modules/.bin/sanity schema deploy
./node_modules/.bin/sanity schema list

# Token + secret (G14/G15)
./node_modules/.bin/sanity tokens add "stillwater-web-read" --role viewer --yes > /tmp/tok.txt 2>&1
grep -oE "sk[A-Za-z0-9]+" /tmp/tok.txt | head -1 > /tmp/sanity_key.txt
openssl rand -base64 32 > /tmp/sanity_webhook_secret.txt

# CORS (G18)
./node_modules/.bin/sanity cors add http://localhost:3000 --credentials
./node_modules/.bin/sanity cors add https://<domain> --credentials
./node_modules/.bin/sanity cors list

# Studio UI (G16)
./node_modules/.bin/sanity deploy --url=stillwater --yes --schema-required
# → pin appId in sanity.cli.ts: deployment: { appId: '...' }

# Webhook → Sanity Cloud UI (API → Webhooks): URL, POST, secret, triggers C/U/D (G17)

# Verify (G23)
curl -s "https://<projectId>.api.sanity.io/v2021-06-07/data/query/production?query=*%5B_type%20%3D%3D%20%22siteSettings%22%5D%5B0%5D"
# agent_browser open https://<hostname>.sanity.studio/  (sessionMode: fresh) → redirects to sanity.io/login
```

---

## 15. Verification checklist (done when all green)

- [ ] `sanity projects list` shows the target project; `sanity datasets list` shows the dataset.
- [ ] Schema populated (not empty template); `sanity schema deploy` succeeds with 0 reference errors; `grep` shows no dangling `to: [{ type: … }]` targets.
- [ ] `NEXT_PUBLIC_SANITY_*` set in `apps/web/.env.local` (+ root mirror).
- [ ] `SANITY_API_TOKEN` = a **viewer** token (fresh, not reused from a committed file); `SANITY_WEBHOOK_SECRET` = generated value (both in `.env.local` only).
- [ ] CORS includes `localhost:3000` + production domain.
- [ ] `sanity deploy` succeeded; `appId` pinned in `sanity.cli.ts`.
- [ ] Fresh `agent-browser` session on `https://<hostname>.sanity.studio/` redirects to the Sanity login (proves live; 404 before deploy was expected); redirect `appId` matches the pinned one.
- [ ] Content Lake API query returns `result: null` + `syncTags` (dataset live, no content yet).
- [ ] ISR webhook created in Sanity Cloud UI pointing at `/api/sanity/webhook` with the secret.
- [ ] (Security) Any committed Studio `.env.local` / SSH key purged from git history; fresh token rotated.

---

## 16. Decision points to surface to the user (don't pick silently)

1. **Which Studio is canonical** when a monorepo already has `apps/studio/` and a sibling exists (G2).
2. **Which Sanity account / provider** owns the target project — verify with `sanity projects list`
   before deploying (G11/G12).
3. **Schema source** — copy existing types, author new ones, or different content model?
4. **Live mutations** — `schema deploy` / `cors` / `deploy` / `tokens add` hit the real Sanity
   project (needs auth + network). Offer to stage commands if the user prefers to run them.
5. **Secrets** — mint a fresh token (rotate any committed one) or leave placeholders? (Client
   null-fallback means placeholders are safe for a first pass; committed secrets must be rotated.)
6. **ISR webhook** — create in Cloud UI (CLI is interactive-only, G17) or stage the exact fields.
