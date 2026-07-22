# n8n Workflow JSON Structure

Complete reference for n8n workflow JSON specification.

---

## Top-Level Structure

```json
{
  "name": "Workflow Name",
  "nodes": [...],
  "connections": {...},
  "pinData": {},
  "settings": {...},
  "staticData": {...},
  "tags": [...],
  "triggerCount": 0,
  "updatedAt": "2026-03-19T00:00:00.000Z",
  "versionId": "uuid-string"
}
```

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Workflow display name |
| `nodes` | array | Array of node configurations |
| `connections` | object | Node connection mapping |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `pinData` | object | Pinned data for testing |
| `settings` | object | Workflow-level settings |
| `staticData` | object | Persistent data between executions |
| `tags` | array | Workflow tags |
| `triggerCount` | number | Number of trigger nodes |
| `updatedAt` | string | Last modification timestamp |
| `versionId` | string | Unique workflow version identifier |

---

## Node Structure

Each node in the `nodes` array has this structure:

```json
{
  "parameters": {
    // Node-specific configuration
  },
  "id": "6bf64d5c-4b00-43cf-8439-3cbf5e5f203b",
  "name": "Node Display Name",
  "type": "n8n-nodes-base.webhook",
  "typeVersion": 2,
  "position": [250, 300],
  "webhookId": "optional-webhook-uuid"
}
```

### Required Node Fields

| Field | Type | Description |
|-------|------|-------------|
| `parameters` | object | Node-specific settings |
| `name` | string | Unique display name in workflow |
| `type` | string | Node type identifier |
| `typeVersion` | number | Node type version |
| `position` | array | Canvas position [x, y] |

### Optional Node Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique node identifier (UUID) |
| `webhookId` | string | For webhook nodes |
| `credentials` | object | Credential references |
| `disabled` | boolean | Node is disabled |
| `notes` | string | Node notes |
| `notesInFlow` | boolean | Show notes on canvas |
| `retryOnFail` | object | Retry configuration |
| `onError` | string | Error handling mode |
| `continueOnFail` | boolean | Continue workflow on error |

---

## Common Node Types

### Trigger Nodes

| Type | Description |
|------|-------------|
| `n8n-nodes-base.webhook` | Webhook trigger |
| `n8n-nodes-base.scheduleTrigger` | Scheduled execution |
| `n8n-nodes-base.manualTrigger` | Manual execution button |
| `n8n-nodes-base.emailTrigger` | Email received trigger |
| `n8n-nodes-base.executeworkflowtrigger` | Sub-workflow trigger |

### Logic Nodes

| Type | Description |
|------|-------------|
| `n8n-nodes-base.if` | Conditional branching |
| `n8n-nodes-base.switch` | Multi-way branching |
| `n8n-nodes-base.merge` | Merge multiple inputs |
| `n8n-nodes-base.splitInBatches` | Batch processing |
| `n8n-nodes-base.loopOverItems` | Loop iteration |

### Action Nodes

| Type | Description |
|------|-------------|
| `n8n-nodes-base.httpRequest` | HTTP requests |
| `n8n-nodes-base.code` | JavaScript/Python code |
| `n8n-nodes-base.set` | Set/edit fields |
| `n8n-nodes-base.slack` | Slack integration |
| `n8n-nodes-base.gmail` | Gmail integration |

---

## Connections Structure

Connections define how nodes link together:

```json
"connections": {
  "Source Node Name": {
    "main": [
      [
        {
          "node": "Target Node Name",
          "type": "main",
          "index": 0
        }
      ]
    ]
  }
}
```

### Connection Fields

| Field | Type | Description |
|-------|------|-------------|
| `node` | string | Target node name (must match exactly) |
| `type` | string | Connection type (usually "main") |
| `index` | number | Output index (usually 0) |

### Multi-Output Example (IF Node)

```json
"connections": {
  "If Node": {
    "main": [
      [
        { "node": "True Branch Target", "type": "main", "index": 0 }
      ],
      [
        { "node": "False Branch Target", "type": "main", "index": 0 }
      ]
    ]
  }
}
```

---

## Complete Example: Webhook → Code → Slack

```json
{
  "name": "Contact Form Handler",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "contact-form",
        "responseMode": "responseNode",
        "options": {}
      },
      "id": "webhook-001",
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
      "id": "code-001",
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
        "text": "={{ $json.name }} ({{ $json.email }}): {{ $json.message }}"
      },
      "id": "slack-001",
      "name": "Slack",
      "type": "n8n-nodes-base.slack",
      "typeVersion": 2,
      "position": [650, 300]
    },
    {
      "parameters": {
        "respondWith": "json",
        "responseBody": "{ \"success\": true, \"message\": \"Form received\" }"
      },
      "id": "respond-001",
      "name": "Respond",
      "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1,
      "position": [850, 300]
    }
  ],
  "connections": {
    "Webhook": {
      "main": [[{ "node": "Process Form", "type": "main", "index": 0 }]]
    },
    "Process Form": {
      "main": [[{ "node": "Slack", "type": "main", "index": 0 }]]
    },
    "Slack": {
      "main": [[{ "node": "Respond", "type": "main", "index": 0 }]]
    }
  }
}
```

---

## Workflow Settings

```json
"settings": {
  "executionOrder": "v1",
  "saveDataErrorExecution": "all",
  "saveDataSuccessExecution": "all",
  "saveExecutionProgress": true,
  "saveManualExecutions": true,
  "executionTimeout": 3600,
  "timezone": "Asia/Singapore",
  "errorWorkflow": "workflow-id-for-error-handling"
}
```

---

## Import/Export

### Export Workflow
1. Select all nodes on canvas
2. Press `Ctrl+C` to copy workflow JSON
3. Paste into file or share directly

### Import Workflow
1. Press `Ctrl+V` with workflow JSON in clipboard
2. Or use: Workflow menu → Import from URL/File/JSON

### Share Workflow
- Remove credential references before sharing
- Anonymize any sensitive data in parameters
- Remove `id` fields for clean imports
