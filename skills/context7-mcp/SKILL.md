---
name: context7-mcp
description: |
  Programmatic document lookup via Context7 API and MCP server. Use when: (1) Need structured documentation for any library/package/framework, (2) Want code examples without browser automation, (3) Building with specific tools and need accurate API references, (4) Avoiding hallucinated or outdated docs.
  
  Priority: API (fastest) → MCP Server → Browser (fallback)
  
  Triggers: "lookup docs for", "get Context7 docs", "find documentation", "API reference for", "code examples for [library]"
---

# Context7 MCP/API Document Lookup

Programmatic access to Context7's curated documentation index for 74,000+ libraries. Retrieves accurate, up-to-date docs without browser automation.

## Access Priority

```
1. Direct REST API (preferred) — fastest, no server dependency
2. MCP Server (fallback) — structured tool interface
3. Browser Mode (last resort) — use context7-docs skill
```

---

## Method 1: Direct REST API (Preferred)

**Prerequisites:** API key set in `CONTEXT7_API_KEY` environment variable or available in `~/.bashrc`

### API Endpoints

| Endpoint | Purpose | Required Params |
|----------|---------|-----------------|
| `GET /api/v2/libs/search` | Find library ID | `libraryName`, `query` |
| `GET /api/v2/context` | Get documentation | `libraryId`, `query` |

**Base URL:** `https://context7.com`

### Step 1: Search for Library

```bash
# Set API key (if not in environment)
export CONTEXT7_API_KEY="ctx7sk-XXXXXXXX"

# Search for library
curl -s "https://context7.com/api/v2/libs/search?libraryName=react&query=hooks+state+management" \
  -H "Authorization: Bearer $CONTEXT7_API_KEY"
```

**Response Fields:**

| Field | Meaning | Use For |
|-------|---------|---------|
| `id` | Library identifier (e.g., `/facebook/react`) | Next API call |
| `versions` | Available versions (e.g., `["v19_2_0", "v18_3_1"]`) | Version-specific docs |
| `totalSnippets` | Code examples count | More = richer content |
| `benchmarkScore` | Quality score (0-100) | Higher = better structured |
| `trustScore` | Source reliability | Higher = more authoritative |
| `state` | Library status | `"finalized"` = ready to use |

### Step 2: Get Documentation

```bash
# Get docs for specific version
curl -s "https://context7.com/api/v2/context?libraryId=/facebook/react/v19_2_0&query=use+hook+context" \
  -H "Authorization: Bearer $CONTEXT7_API_KEY"

# Get docs without version (uses latest)
curl -s "https://context7.com/api/v2/context?libraryId=/vercel/next.js&query=app+router+server+components" \
  -H "Authorization: Bearer $CONTEXT7_API_KEY"
```

### Response Format

Returns markdown-formatted documentation with:

- `### Title` — Section headers
- `Source: [URL]` — Original source link
- Code blocks with syntax highlighting
- Separated by `--------------------------------` dividers

### Query Best Practices

**Good queries** (specific, natural language):

```
"How to set up authentication with JWT in Express"
"useEffect cleanup function examples"
"Server Components data fetching patterns"
```

**Bad queries** (too vague):

```
"auth"
"hooks"
"components"
```

### Version Pinning

For reproducible results, pin to specific version:

```bash
# Pin to Next.js 16.1.6
libraryId=/vercel/next.js/v16.1.6

# Pin to React 19.2.0
libraryId=/facebook/react/v19_2_0
```

### Error Handling

| Status Code | Meaning | Action |
|-------------|---------|--------|
| 200 | Success | Process response |
| 202 | Library not finalized | Wait and retry |
| 301 | Library redirected | Use new `libraryId` from response |
| 401 | Invalid API key | Check key format (`ctx7sk-` prefix) |
| 404 | Library not found | Verify `libraryId` from search |
| 429 | Rate limit exceeded | Wait for `Retry-After` header |

---

## Method 2: MCP Server (Fallback)

**Prerequisites:** Context7 MCP server running on `localhost:8080`

### Start MCP Server

```bash
# Start in background
nohup /home/pete/bin/bun run /Home1/node-v24/lib/node_modules/@upstash/context7-mcp/dist/index.js --transport http --port 8080 &

# Verify server is running
curl -s http://127.0.0.1:8080/mcp -H "Accept: application/json, text/event-stream"
```

### Check Server Health

```bash
# Should return MCP error (not connection refused)
curl -s http://127.0.0.1:8080/

# Expected: {"error":"not_found","message":"Endpoint not found. Use /mcp for MCP protocol communication."}
```

**If connection refused:** Server not running — start it with command above

### Available Tools

| Tool | Purpose | Required Args |
|------|---------|---------------|
| `resolve-library-id` | Find library ID | `libraryName`, `query` |
| `query-docs` | Get documentation | `libraryId`, `query` |

### Step 1: Resolve Library ID

```bash
curl -s -X POST http://127.0.0.1:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc":"2.0",
    "id":1,
    "method":"tools/call",
    "params":{
      "name":"resolve-library-id",
      "arguments":{
        "libraryName":"react",
        "query":"React 19 new features"
      }
    }
  }'
```

### Step 2: Query Documentation

```bash
curl -s -X POST http://127.0.0.1:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc":"2.0",
    "id":2,
    "method":"tools/call",
    "params":{
      "name":"query-docs",
      "arguments":{
        "libraryId":"/facebook/react/v19_2_0",
        "query":"use hook for reading context"
      }
    }
  }'
```

### MCP Response Format

Returns JSON-RPC 2.0 response:

```json
{
  "result": {
    "content": [
      {
        "type": "text",
        "text": "### Title\n\nSource: https://github.com/...\n\n```javascript\n// code example\n```"
      }
    ]
  },
  "jsonrpc": "2.0",
  "id": 2
}
```

---

## Method 3: Browser Mode (Last Resort)

If both API and MCP methods fail, use the `context7-docs` skill for browser-based lookup:

```
See: /home/pete/.openclaw/workspace/skills/context7-docs/SKILL.md
```

**When to use:**

- API key unavailable
- MCP server won't start
- Need interactive browsing/selection
- Want to explore available libraries visually

---

## Complete Workflow Example

### Python Script for API Access

```python
import os
import requests
import time

class Context7API:
    def __init__(self):
        self.api_key = os.environ.get('CONTEXT7_API_KEY')
        self.base_url = "https://context7.com/api/v2"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
    
    def search_library(self, library_name: str, query: str) -> dict:
        """Search for library and return best match."""
        response = requests.get(
            f"{self.base_url}/libs/search",
            headers=self.headers,
            params={"libraryName": library_name, "query": query}
        )
        results = response.json().get("results", [])
        return results[0] if results else None
    
    def get_docs(self, library_id: str, query: str, version: str = None) -> str:
        """Get documentation for library."""
        if version:
            library_id = f"{library_id}/{version}"
        
        response = requests.get(
            f"{self.base_url}/context",
            headers=self.headers,
            params={"libraryId": library_id, "query": query}
        )
        return response.text
    
    def fetch_with_retry(self, url: str, max_retries: int = 3) -> requests.Response:
        """Fetch with exponential backoff for rate limits."""
        for attempt in range(max_retries):
            response = requests.get(url, headers=self.headers)
            if response.status_code == 429:
                time.sleep(2 ** attempt)
                continue
            return response
        raise Exception("Max retries exceeded")

# Usage
ctx7 = Context7API()

# Search for Next.js
lib = ctx7.search_library("next.js", "app router SSR")
print(f"Found: {lib['id']} (v{lib.get('versions', ['latest'])[0]})")

# Get documentation
docs = ctx7.get_docs(lib['id'], "server components data fetching", "v16.1.6")
print(docs)
```

### Bash One-Liner (Quick Lookup)

```bash
# Quick React hooks reference
export CONTEXT7_API_KEY="ctx7sk-XXXX" && \
LIB_ID=$(curl -s "https://context7.com/api/v2/libs/search?libraryName=react&query=hooks" -H "Authorization: Bearer $CONTEXT7_API_KEY" | jq -r '.results[0].id') && \
curl -s "https://context7.com/api/v2/context?libraryId=$LIB_ID&query=useEffect+cleanup" -H "Authorization: Bearer $CONTEXT7_API_KEY"
```

---

## Library Selection Strategy

When multiple matches exist, prioritize:

1. **Official sources** — `/facebook/react` > `/someuser/react-fork`
2. **Version availability** — Libraries with version tags > no versions
3. **Benchmark score** — Higher = better docs structure (85 > 62)
4. **Snippet count** — More snippets = richer code examples (2796 > 500)
5. **Recent updates** — Fresher docs preferred

### Example Selection

```
Results for "react":
  /facebook/react          — 3,580 snippets, v19_2_0 available, benchmark: 62.25
  /reactjs/react.dev       — 2,781 snippets, no versions, benchmark: 85.24
  /websites/react_dev      — 2,796 snippets, no versions, benchmark: 89.70

Decision:
- For specific version: /facebook/react/v19_2_0
- For best docs structure: /websites/react_dev
- For source code: /facebook/react
```

---

## Common Libraries Quick Reference

| Library | Library ID | Notable Versions |
|---------|------------|------------------|
| React | `/facebook/react` | v19_2_0, v18_3_1, v17.0.2 |
| Next.js | `/vercel/next.js` | v16.1.6, v15.1.8, v14.3.0-canary.87 |
| Vue | `/vuejs/vue` | v3.5.13, v2.7.16 |
| Tailwind CSS | `/tailwindlabs/tailwindcss` | v4.1.4, v3.4.17 |
| Supabase | `/supabase/supabase` | (docs only) |
| Prisma | `/prisma/prisma` | v6.5.0, v5.22.0 |
| n8n | `/n8n-io/n8n-docs` | (docs) |
| LangChain | `/langchain-ai/langchain` | (Python/JS split) |

---

## Rate Limits

| Tier | Rate Limit | Notes |
|------|------------|-------|
| No API key | Low | Not recommended |
| With API key | Higher | Based on plan |
| Enterprise | Custom | Contact Context7 |

Check usage at: `https://context7.com/dashboard`

---

## Troubleshooting

### API Key Issues

```bash
# Check if key is set
echo $CONTEXT7_API_KEY

# Expected format: ctx7sk-XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX

# Test key validity
curl -s "https://context7.com/api/v2/libs/search?libraryName=react&query=test" \
  -H "Authorization: Bearer $CONTEXT7_API_KEY" | head -100
```

### MCP Server Issues

```bash
# Check if server is running
curl -s http://127.0.0.1:8080/ 2>&1

# If "Connection refused" — server not running
# Start server:
nohup /home/pete/bin/bun run /Home1/node-v24/lib/node_modules/@upstash/context7-mcp/dist/index.js --transport http --port 8080 &

# If server hangs — kill and restart
pkill -f context7-mcp
nohup /home/pete/bin/bun run /Home1/node-v24/lib/node_modules/@upstash/context7-mcp/dist/index.js --transport http --port 8080 &
```

### Empty Results

- Query too vague — use more specific terms
- Library not indexed — try alternate name (e.g., "nextjs" vs "next.js")
- Version not available — check `versions` array in search response

---

## Related Skills

| Skill | When to Use |
|-------|-------------|
| `context7-docs` | Browser-based lookup (last resort) |
| `web_fetch` | Direct URL fetching |
| `web_search` | General web search |
| `mcporter` | MCP server management |

---

## API Key Storage

**Current location:** `~/.bashrc`

```bash
export CONTEXT7_API_KEY="ctx7sk-87812280-66e8-4899-9520-0cd33273afe0"
```

**Security:** Never commit API keys to git. Keep in local config files only.
