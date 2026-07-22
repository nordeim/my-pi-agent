---
name: n8n-workflow-automation
description: |
  Build and automate n8n workflows using JSON specification.
  Use when: (1) Creating n8n workflows programmatically, (2) Converting workflows to/from JSON,
  (3) Understanding n8n node types and connections, (4) Writing n8n expressions,
  (5) Debugging workflow JSON structure, (6) Building workflow templates.
  Triggers on phrases like "n8n workflow", "n8n JSON", "n8n expression", "webhook workflow", "n8n automation".
---

# n8n Workflow Automation

Programmatically build n8n workflows using JSON specification.

## Quick Reference

### Workflow Structure

```json
{
  "name": "Workflow Name",
  "nodes": [...],
  "connections": {...}
}
```

### Node Structure

```json
{
  "name": "Node Name",
  "type": "n8n-nodes-base.webhook",
  "typeVersion": 2,
  "parameters": {...},
  "position": [x, y]
}
```

### Connection Structure

```json
"connections": {
  "Source": { "main": [[{ "node": "Target", "type": "main", "index": 0 }]] }
}
```

---

## Common Node Types

| Category | Nodes |
|----------|-------|
| **Triggers** | `webhook`, `scheduleTrigger`, `manualTrigger` |
| **Logic** | `if`, `switch`, `merge`, `splitInBatches` |
| **Actions** | `httpRequest`, `code`, `set` |
| **Integrations** | `slack`, `gmail`, `googleSheets` |

---

## Expression Syntax

| Expression | Purpose |
|------------|---------|
| `{{ $json.field }}` | Access current item data |
| `{{ $("Node").first() }}` | Get data from named node |
| `{{ $now }}` | Current timestamp |
| `{{ $json.body.name }}` | Webhook body data |

---

## Key Gotcha

**Webhook data is under `.body`** - Access via `{{ $json.body.field }}` not `{{ $json.field }}`

---

## Usage Flow

1. **Define workflow structure** using JSON schema
2. **Configure nodes** with appropriate types and parameters
3. **Set up connections** between nodes
4. **Use expressions** for dynamic data
5. **Test** by importing JSON into n8n

---

## References

For complete documentation:
- `references/01-workflow-json-structure.md` - Full JSON specification
- `references/02-expression-syntax.md` - Expression reference
- `references/03-common-nodes.md` - Node type catalog
- `references/04-workflow-patterns.md` - Proven patterns
- `references/n8n-llms-full.txt` - Official n8n documentation (94,504 lines)

---

## Examples

### Simple Webhook Handler

```json
{
  "name": "Contact Form Handler",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "contact-form",
        "responseMode": "responseNode"
      },
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 2,
      "position": [250, 300]
    },
    {
      "parameters": {
        "resource": "message",
        "operation": "post",
        "channel": "#notifications",
        "text": "={{ 'Contact: ' + $json.body.name + ' (' + $json.body.email + ')' }}"
      },
      "name": "Slack",
      "type": "n8n-nodes-base.slack",
      "typeVersion": 2,
      "position": [450, 300]
    }
  ],
  "connections": {
    "Webhook": { "main": [[{ "node": "Slack", "type": "main", "index": 0 }]] }
  }
}
```

### Scheduled API Call

```json
{
  "name": "Hourly API Check",
  "nodes": [
    {
      "parameters": {
        "rule": { "interval": [{ "field": "hours", "hoursInterval": 1 }] }
      },
      "name": "Schedule",
      "type": "n8n-nodes-base.scheduleTrigger",
      "typeVersion": 1.1,
      "position": [250, 300]
    },
    {
      "parameters": {
        "method": "GET",
        "url": "https://api.example.com/status"
      },
      "name": "Get Status",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.1,
      "position": [450, 300]
    }
  ],
  "connections": {
    "Schedule": { "main": [[{ "node": "Get Status", "type": "main", "index": 0 }]] }
  }
}
```

---

## Best Practices

1. **Node names must be unique** in a workflow
2. **Connection names are case-sensitive** - must match exactly
3. **Webhook data is nested** under `$json.body`
4. **Code node must return** `[{ json: {...} }]` format
5. **Always wrap expressions** with `{{ }}`
6. **Use $now for timestamps** - not new Date() in expressions
7. **Test connections** by importing JSON into n8n UI

---

## Import/Export

### Export
1. Select all nodes: Ctrl+A
2. Copy: Ctrl+C
3. Paste into file

### Import
1. Copy JSON to clipboard
2. In n8n: Ctrl+V
3. Or: Workflow menu → Import from JSON

---

## External Documentation

- **n8n Official Docs:** https://docs.n8n.io/
- **Context7 Curated:** https://context7.com/n8n
- **Fresh LLMs.txt:** https://docs.n8n.io/llms-full.txt
