---
name: context7-docs
description: |
  Search and retrieve up-to-date curated documentation from Context7 for any software, library, or package.
  Use when: (1) Need latest documentation for a specific library or tool, (2) Looking for code examples and patterns,
  (3) Need accurate API reference information, (4) Building workflows with specific tools like n8n, (5) Want to avoid hallucinated or outdated documentation.
  Triggers on phrases like "search Context7 for", "get documentation for", "find latest docs", "n8n workflow", "package documentation".
---

# Context7 Documentation Search

Retrieve accurate, up-to-date documentation from Context7's curated library index for LLMs and AI code editors.

## What is Context7?

Context7 is a documentation search engine that indexes 74,000+ libraries, providing:
- **Curated documentation** optimized for LLM consumption
- **Code snippets** extracted from official sources (GitHub repos, docs sites, npm packages)
- **Freshness indicators** showing last update time
- **Benchmark scores** indicating documentation quality
- **Trust scores** based on source reliability

---

## Search Workflow

### Step 1: Navigate to Context7

**URL:** `https://context7.com/`

### Step 2: Search for Documentation

1. Use the search box labeled "Search a library"
2. Type your package/library name (e.g., "n8n", "react", "nextjs")
3. Press Enter to search

### Step 3: Evaluate Results

Context7 shows results in a table with these columns:

| Column | Meaning | How to Use |
|--------|---------|------------|
| **SOURCE** | Library name and GitHub path | Identifies the exact package |
| **BENCHMARK** | Quality score (0-100) | Higher = better structured docs |
| **SNIPPETS** | Number of code examples | More = richer code samples |
| **UPDATE** | Last refresh time | Prefer "hours/days" over "months" |
| **TRUST** | Reliability indicators | Multiple icons = verified |

### Step 4: Select Best Match

**Selection Criteria (in order):**

1. **Official sources preferred:** `/n8n-io/n8n-docs` > community forks
2. **Higher benchmark score:** 77.2 > 53.8
3. **Recent updates:** "11 hours ago" > "3 weeks ago"
4. **More snippets:** 23K > 1.1K

**Example:**
```
✓ docs.n8n.io/llms-full.txt (77.2, 23K snippets, 11 hours)
✗ /n8n-io/n8n (53.8, 1.6K snippets, 3 weeks)
```

### Step 5: Extract Documentation

Click the link to view:
- **Context:** Generated summary
- **Code:** Raw documentation with snippets
- **Info:** Metadata
- **Skills:** Pre-built skill files (if available)

---

## Special Documentation Types

### LLMs-Full.txt (AI-Optimized)

**Best for:** Comprehensive knowledge, workflow building

**URL Pattern:** `/{path}/llms-full.txt`

**Contains:**
- Complete API references
- Configuration patterns
- Code examples with context
- Step-by-step guides

### llms.txt (Concise)

**Best for:** Quick reference, single questions

**URL Pattern:** `/{path}/llms.txt`

### GitHub Repository Sources

**Best for:** Source code, implementation details

**URL Pattern:** `/{owner}/{repo}`

---

## Advanced Techniques

### Filter by Topic

After opening documentation, use "Show doc for..." textbox:
- `webhook data` → webhook-related snippets
- `json format` → JSON structure examples

### Extract Raw Content

For programmatic access:
1. Click "Raw" link
2. URL format: `/{path}/llms.txt?tokens=10000`
3. Adjust tokens: 10000, 20000, 50000

### Copy Permalink

Use "Copy permalink" for shareable links.

---

## n8n Workflow JSON Structure

From Context7 n8n documentation:

```json
{
  "name": "Workflow Name",
  "nodes": [
    {
      "parameters": { "path": "webhook-path" },
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 2,
      "position": [250, 300],
      "id": "node-id"
    }
  ],
  "connections": {
    "Webhook": {
      "main": [[{ "node": "Next Node", "type": "main", "index": 0 }]]
    }
  }
}
```

### Key n8n Concepts from Context7

| Concept | Pattern |
|---------|---------|
| **Webhook data** | Nested under `.body` property |
| **Expressions** | Must use `{{ }}` double braces |
| **Node types** | `n8n-nodes-base.{type}` in JSON |
| **Connections** | Array of `{node, type, index}` objects |

---

## Common Libraries Available

| Category | Examples |
|----------|----------|
| **Frameworks** | Next.js, React, Vue, Svelte |
| **AI/LLM** | LangChain, OpenAI, Anthropic SDKs |
| **Automation** | n8n, Pipedream |
| **Database** | Prisma, Supabase, MongoDB |
| **Styling** | Tailwind, shadcn/ui |
| **Tools** | OpenClaw, Claude Code, Cursor |

---

## Related Skills

| Skill | When to Use |
|-------|-------------|
| `web_fetch` | Direct URL fetching |
| `web_search` | General web search |
| `browser` | Interactive browsing |
