# n8n Workflow Patterns

Proven patterns for building n8n workflows programmatically.

---

## Pattern 1: Webhook Processing

**Use Case:** Receive POST data, process, respond, and notify.

```json
{
  "name": "Webhook Processor",
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
        "mode": "runOnceForAllItems",
        "jsCode": "const formData = $input.first().json.body;\nreturn [{\n  json: {\n    name: formData.name,\n    email: formData.email,\n    message: formData.message,\n    timestamp: new Date().toISOString()\n  }\n}];"
      },
      "name": "Process Form",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [450, 300]
    },
    {
      "parameters": {
        "resource": "message",
        "operation": "post",
        "channel": "#notifications",
        "text": "New contact: {{ $json.name }} ({{ $json.email }})"
      },
      "name": "Notify Slack",
      "type": "n8n-nodes-base.slack",
      "typeVersion": 2,
      "position": [650, 300]
    },
    {
      "parameters": {
        "respondWith": "json",
        "responseBody": "{ \"success\": true }"
      },
      "name": "Respond",
      "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1,
      "position": [850, 300]
    }
  ],
  "connections": {
    "Webhook": { "main": [[{ "node": "Process Form", "type": "main", "index": 0 }]] },
    "Process Form": { "main": [[{ "node": "Notify Slack", "type": "main", "index": 0 }]] },
    "Notify Slack": { "main": [[{ "node": "Respond", "type": "main", "index": 0 }]] }
  }
}
```

---

## Pattern 2: API Integration with Error Handling

**Use Case:** Fetch data from API, handle errors gracefully.

```json
{
  "name": "API Integration",
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
        "url": "https://api.example.com/users",
        "options": { "timeout": 10000 }
      },
      "name": "Get Users",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.1,
      "position": [450, 300],
      "continueOnFail": true
    },
    {
      "parameters": {
        "conditions": {
          "conditions": [{
            "leftValue": "={{ $json.error }}",
            "operator": { "type": "string", "operation": "isEmpty" }
          }]
        }
      },
      "name": "Check Success",
      "type": "n8n-nodes-base.if",
      "typeVersion": 2,
      "position": [650, 300]
    },
    {
      "parameters": {
        "mode": "runOnceForAllItems",
        "jsCode": "const data = $input.all();\nreturn data.filter(item => item.json.status === 'active').map(item => ({\n  json: {\n    id: item.json.id,\n    name: item.json.name,\n    email: item.json.email\n  }\n}));"
      },
      "name": "Filter Active",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [850, 200]
    },
    {
      "parameters": {
        "resource": "message",
        "operation": "post",
        "channel": "#alerts",
        "text": "⚠️ API Error: {{ $json.error.message }}"
      },
      "name": "Alert Error",
      "type": "n8n-nodes-base.slack",
      "typeVersion": 2,
      "position": [850, 400]
    }
  ],
  "connections": {
    "Schedule": { "main": [[{ "node": "Get Users", "type": "main", "index": 0 }]] },
    "Get Users": { "main": [[{ "node": "Check Success", "type": "main", "index": 0 }]] },
    "Check Success": {
      "main": [
        [{ "node": "Filter Active", "type": "main", "index": 0 }],
        [{ "node": "Alert Error", "type": "main", "index": 0 }]
      ]
    }
  }
}
```

---

## Pattern 3: Conditional Routing

**Use Case:** Route data based on priority level.

```json
{
  "name": "Priority Router",
  "nodes": [
    {
      "parameters": { "httpMethod": "POST", "path": "ticket" },
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 2,
      "position": [250, 300]
    },
    {
      "parameters": {
        "rules": [
          {
            "output": 0,
            "conditions": {
              "conditions": [{
                "leftValue": "={{ $json.body.priority }}",
                "rightValue": "critical",
                "operator": { "type": "string", "operation": "equals" }
              }]
            }
          },
          {
            "output": 1,
            "conditions": {
              "conditions": [{
                "leftValue": "={{ $json.body.priority }}",
                "rightValue": "high",
                "operator": { "type": "string", "operation": "equals" }
              }]
            }
          }
        ],
        "fallbackOutput": 2
      },
      "name": "Priority Switch",
      "type": "n8n-nodes-base.switch",
      "typeVersion": 3,
      "position": [450, 300]
    },
    {
      "parameters": {
        "resource": "message",
        "channel": "#critical-alerts",
        "text": "🚨 CRITICAL: {{ $json.body.title }}"
      },
      "name": "Critical Alert",
      "type": "n8n-nodes-base.slack",
      "typeVersion": 2,
      "position": [650, 150]
    },
    {
      "parameters": {
        "resource": "message",
        "channel": "#high-priority",
        "text": "⚠️ HIGH: {{ $json.body.title }}"
      },
      "name": "High Alert",
      "type": "n8n-nodes-base.slack",
      "typeVersion": 2,
      "position": [650, 300]
    },
    {
      "parameters": {
        "assignments": {
          "assignments": [{
            "name": "status",
            "value": "queued"
          }]
        }
      },
      "name": "Queue",
      "type": "n8n-nodes-base.set",
      "typeVersion": 3.3,
      "position": [650, 450]
    }
  ],
  "connections": {
    "Webhook": { "main": [[{ "node": "Priority Switch", "type": "main", "index": 0 }]] },
    "Priority Switch": {
      "main": [
        [{ "node": "Critical Alert", "type": "main", "index": 0 }],
        [{ "node": "High Alert", "type": "main", "index": 0 }],
        [{ "node": "Queue", "type": "main", "index": 0 }]
      ]
    }
  }
}
```

---

## Pattern 4: Data Aggregation

**Use Case:** Aggregate data from multiple sources.

```json
{
  "name": "Data Aggregator",
  "nodes": [
    {
      "parameters": { "rule": { "interval": [{ "field": "hours", "hoursInterval": 1 }] } },
      "name": "Schedule",
      "type": "n8n-nodes-base.scheduleTrigger",
      "typeVersion": 1.1,
      "position": [250, 200]
    },
    {
      "parameters": {
        "method": "GET",
        "url": "https://api.example.com/sales"
      },
      "name": "Get Sales",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.1,
      "position": [450, 150]
    },
    {
      "parameters": {
        "method": "GET",
        "url": "https://api.example.com/inventory"
      },
      "name": "Get Inventory",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.1,
      "position": [450, 300]
    },
    {
      "parameters": {
        "mode": "combine",
        "combineBy": "allItems"
      },
      "name": "Merge Data",
      "type": "n8n-nodes-base.merge",
      "typeVersion": 2.1,
      "position": [650, 200]
    },
    {
      "parameters": {
        "mode": "runOnceForAllItems",
        "jsCode": "const items = $input.all();\nconst sales = items.filter(i => i.json.source === 'sales');\nconst inventory = items.filter(i => i.json.source === 'inventory');\n\nconst totalRevenue = sales.reduce((sum, item) => sum + item.json.amount, 0);\nconst totalStock = inventory.reduce((sum, item) => sum + item.json.quantity, 0);\n\nreturn [{\n  json: {\n    totalRevenue,\n    totalStock,\n    averageOrderValue: totalRevenue / sales.length,\n    timestamp: new Date().toISOString()\n  }\n}];"
      },
      "name": "Calculate",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [850, 200]
    },
    {
      "parameters": {
        "resource": "message",
        "channel": "#reports",
        "text": "📊 Report\\nRevenue: ${{ $json.totalRevenue }}\\nStock: {{ $json.totalStock }} units\\nAvg Order: ${{ $json.averageOrderValue }}"
      },
      "name": "Report",
      "type": "n8n-nodes-base.slack",
      "typeVersion": 2,
      "position": [1050, 200]
    }
  ],
  "connections": {
    "Schedule": { "main": [[{ "node": "Get Sales", "type": "main", "index": 0 }, { "node": "Get Inventory", "type": "main", "index": 0 }]] },
    "Get Sales": { "main": [[{ "node": "Merge Data", "type": "main", "index": 0 }]] },
    "Get Inventory": { "main": [[{ "node": "Merge Data", "type": "main", "index": 1 }]] },
    "Merge Data": { "main": [[{ "node": "Calculate", "type": "main", "index": 0 }]] },
    "Calculate": { "main": [[{ "node": "Report", "type": "main", "index": 0 }]] }
  }
}
```

---

## Pattern 5: Loop with Batch Processing

**Use Case:** Process large datasets in batches.

```json
{
  "name": "Batch Processor",
  "nodes": [
    {
      "parameters": { "rule": { "interval": [{ "field": "hours", "hoursInterval": 1 }] } },
      "name": "Schedule",
      "type": "n8n-nodes-base.scheduleTrigger",
      "typeVersion": 1.1,
      "position": [250, 300]
    },
    {
      "parameters": {
        "method": "GET",
        "url": "https://api.example.com/users?limit=1000"
      },
      "name": "Get All Users",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.1,
      "position": [450, 300]
    },
    {
      "parameters": {
        "batchSize": 50
      },
      "name": "Split in Batches",
      "type": "n8n-nodes-base.splitInBatches",
      "typeVersion": 3,
      "position": [650, 300]
    },
    {
      "parameters": {
        "mode": "runOnceForAllItems",
        "jsCode": "const batch = $input.all();\nconst processed = batch.map(item => ({\n  json: {\n    ...item.json,\n    processedAt: new Date().toISOString()\n  }\n}));\nreturn processed;"
      },
      "name": "Process Batch",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [850, 300]
    },
    {
      "parameters": {
        "method": "POST",
        "url": "https://api.example.com/batch-update",
        "sendBody": true,
        "contentType": "json",
        "jsonBody": "={{ JSON.stringify($input.all().map(i => i.json)) }}"
      },
      "name": "Save Batch",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.1,
      "position": [1050, 300]
    }
  ],
  "connections": {
    "Schedule": { "main": [[{ "node": "Get All Users", "type": "main", "index": 0 }]] },
    "Get All Users": { "main": [[{ "node": "Split in Batches", "type": "main", "index": 0 }]] },
    "Split in Batches": { "main": [[{ "node": "Process Batch", "type": "main", "index": 0 }]] },
    "Process Batch": { "main": [[{ "node": "Save Batch", "type": "main", "index": 0 }]] },
    "Save Batch": { "main": [[{ "node": "Split in Batches", "type": "main", "index": 0 }]] }
  }
}
```

---

## Connection Patterns Quick Reference

### Linear Chain
```
A → B → C → D
```
```json
"connections": {
  "A": { "main": [[{ "node": "B", "type": "main", "index": 0 }]] },
  "B": { "main": [[{ "node": "C", "type": "main", "index": 0 }]] },
  "C": { "main": [[{ "node": "D", "type": "main", "index": 0 }]] }
}
```

### Parallel Execution
```
    ┌→ B ─┐
A → ├     ├→ D
    └→ C ─┘
```
```json
"connections": {
  "A": { "main": [[{ "node": "B", "type": "main", "index": 0 }, { "node": "C", "type": "main", "index": 0 }]] },
  "B": { "main": [[{ "node": "D", "type": "main", "index": 0 }]] },
  "C": { "main": [[{ "node": "D", "type": "main", "index": 1 }]] }
}
```

### Conditional Branch (IF)
```
    ┌→ B (true) ──→ D
A → ├
    └→ C (false) ─→ D
```
```json
"connections": {
  "A": { "main": [[{ "node": "B", "type": "main", "index": 0 }], [{ "node": "C", "type": "main", "index": 0 }]] }
}
```

### Merge Two Branches
```
A → B ─┐
       ├→ D
C → ───┘
```
```json
"connections": {
  "A": { "main": [[{ "node": "B", "type": "main", "index": 0 }]] },
  "C": { "main": [[{ "node": "D", "type": "main", "index": 0 }]] },
  "B": { "main": [[{ "node": "D", "type": "main", "index": 0 }]] }
}
```

---

## Workflow Template Checklist

When creating a new workflow JSON:

- [ ] Unique workflow `name`
- [ ] All nodes have unique `name` values
- [ ] All nodes have correct `type` and `typeVersion`
- [ ] All nodes have `position` arrays
- [ ] `connections` reference exact node names (case-sensitive)
- [ ] Webhook nodes include `webhookId` if needed
- [ ] Expressions use `{{ }}` syntax
- [ ] Code nodes return `[{ json: {...} }]` arrays
- [ ] Credentials referenced by name, not embedded values
