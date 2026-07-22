# n8n Common Node Types

Reference for frequently used node types and their JSON configurations.

---

## Trigger Nodes

### Webhook Trigger

```json
{
  "type": "n8n-nodes-base.webhook",
  "typeVersion": 2,
  "parameters": {
    "httpMethod": "POST",
    "path": "my-webhook-path",
    "responseMode": "responseNode",
    "options": {}
  }
}
```

**Parameters:**

| Parameter | Values | Description |
|-----------|--------|-------------|
| `httpMethod` | GET, POST, PUT, PATCH, DELETE | HTTP method to listen for |
| `path` | string | URL path suffix |
| `responseMode` | "onReceived", "lastNode", "responseNode" | How to respond |
| `authentication` | none, basicAuth, headerAuth, etc. | Auth method |

**Output:** Data arrives under `$json.body`

---

### Schedule Trigger

```json
{
  "type": "n8n-nodes-base.scheduleTrigger",
  "typeVersion": 1.1,
  "parameters": {
    "rule": {
      "interval": [
        { "field": "hours", "hoursInterval": 1 }
      ]
    }
  }
}
```

**Interval Options:**

| Field | Parameter | Example |
|-------|-----------|---------|
| Minutes | `minutesInterval` | `{ "field": "minutes", "minutesInterval": 30 }` |
| Hours | `hoursInterval` | `{ "field": "hours", "hoursInterval": 1 }` |
| Days | `daysInterval` | `{ "field": "days", "daysInterval": 1 }` |
| Weeks | `weeksInterval` | `{ "field": "weeks", "weeksInterval": 1 }` |

**Cron Expression:**

```json
{
  "parameters": {
    "rule": {
      "interval": [],
      "timezone": "Asia/Singapore"
    },
    "cronExpression": "0 9 * * 1-5"
  }
}
```

---

### Manual Trigger

```json
{
  "type": "n8n-nodes-base.manualTrigger",
  "typeVersion": 1,
  "parameters": {}
}
```

Used for testing and manual execution.

---

## Logic Nodes

### IF Node

```json
{
  "type": "n8n-nodes-base.if",
  "typeVersion": 2,
  "parameters": {
    "conditions": {
      "options": {
        "caseSensitive": true,
        "leftValue": "",
        "typeValidation": "strict"
      },
      "conditions": [
        {
          "id": "condition-1",
          "leftValue": "={{ $json.status }}",
          "rightValue": "active",
          "operator": {
            "type": "string",
            "operation": "equals"
          }
        }
      ],
      "combinator": "and"
    },
    "options": {}
  }
}
```

**Operator Types:**

| Type | Operations |
|------|------------|
| `string` | equals, notEquals, contains, notContains, startsWith, endsWith, regex, isEmpty |
| `number` | equals, notEquals, larger, largerEqual, smaller, smallerEqual, between |
| `dateTime` | before, after, between |
| `boolean` | equals |

**Output:** True branch at index 0, False branch at index 1

---

### Switch Node

```json
{
  "type": "n8n-nodes-base.switch",
  "typeVersion": 3,
  "parameters": {
    "rules": [
      {
        "id": "rule-1",
        "output": 0,
        "conditions": {
          "conditions": [
            {
              "leftValue": "={{ $json.priority }}",
              "rightValue": "high",
              "operator": { "type": "string", "operation": "equals" }
            }
          ]
        }
      },
      {
        "id": "rule-2",
        "output": 1,
        "conditions": {
          "conditions": [
            {
              "leftValue": "={{ $json.priority }}",
              "rightValue": "medium",
              "operator": { "type": "string", "operation": "equals" }
            }
          ]
        }
      }
    ],
    "fallbackOutput": 2
  }
}
```

---

### Merge Node

```json
{
  "type": "n8n-nodes-base.merge",
  "typeVersion": 2.1,
  "parameters": {
    "mode": "combine",
    "combineBy": "allItems",
    "options": {}
  }
}
```

**Merge Modes:**

| Mode | Description |
|------|-------------|
| `combine` | Combine all inputs |
| `append` | Append items sequentially |
| `multiplex` | Process each input separately |
| `wait` | Wait for all inputs before merging |

---

## Action Nodes

### HTTP Request Node

```json
{
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4.1,
  "parameters": {
    "method": "POST",
    "url": "https://api.example.com/endpoint",
    "authentication": "predefinedCredentialType",
    "nodeCredentialType": "httpHeaderAuth",
    "sendBody": true,
    "contentType": "json",
    "specifyBody": "json",
    "jsonBody": "={{ JSON.stringify($json) }}",
    "options": {
      "timeout": 10000,
      "response": {
        "response": {
          "neverError": false,
          "responseFormat": "json"
        }
      }
    }
  }
}
```

**Parameters:**

| Parameter | Values | Description |
|-----------|--------|-------------|
| `method` | GET, POST, PUT, PATCH, DELETE | HTTP method |
| `url` | string or expression | Target URL |
| `sendBody` | boolean | Include request body |
| `contentType` | json, form-urlencoded, form-multipart | Body format |
| `sendHeaders` | boolean | Include custom headers |
| `sendQuery` | boolean | Include query parameters |

---

### Code Node (JavaScript)

```json
{
  "type": "n8n-nodes-base.code",
  "typeVersion": 2,
  "parameters": {
    "mode": "runOnceForAllItems",
    "jsCode": "const items = $input.all();\nconst processed = items.map(item => ({\n  json: {\n    ...item.json,\n    processed: true,\n    timestamp: new Date().toISOString()\n  }\n}));\nreturn processed;"
  }
}
```

**Mode Options:**

| Mode | Use Case |
|------|----------|
| `runOnceForAllItems` | Process all items at once (recommended) |
| `runOnceForEachItem` | Process each item separately |

**Critical Return Format:**

```javascript
// ✅ Correct
return [{ json: { result: "data" } }];

// ❌ Wrong - missing .json wrapper
return [{ result: "data" }];

// ❌ Wrong - not an array
return { result: "data" };
```

---

### Set Node (Edit Fields)

```json
{
  "type": "n8n-nodes-base.set",
  "typeVersion": 3.3,
  "parameters": {
    "assignments": {
      "assignments": [
        {
          "id": "assignment-1",
          "name": "newField",
          "value": "={{ $json.originalField }}",
          "type": "string"
        },
        {
          "id": "assignment-2",
          "name": "computedField",
          "value": "={{ $json.price * 1.1 }}",
          "type": "number"
        }
      ]
    },
    "options": {}
  }
}
```

**Type Options:** `string`, `number`, `boolean`, `array`, `object`

---

### Slack Node

```json
{
  "type": "n8n-nodes-base.slack",
  "typeVersion": 2,
  "parameters": {
    "resource": "message",
    "operation": "post",
    "channel": "#notifications",
    "text": "={{ $json.message }}",
    "otherFields": {}
  }
}
```

**Operations:**

| Resource | Operations |
|----------|------------|
| `message` | post, schedule, update, delete |
| `file` | upload, search |
| `user` | get, getProfile |

---

### Gmail Node

```json
{
  "type": "n8n-nodes-base.gmail",
  "typeVersion": 2.1,
  "parameters": {
    "resource": "message",
    "operation": "send",
    "sendTo": "={{ $json.email }}",
    "subject": "Notification",
    "message": "={{ $json.body }}"
  }
}
```

---

## Credential References

Nodes requiring authentication use credential references:

```json
{
  "name": "Slack",
  "type": "n8n-nodes-base.slack",
  "parameters": { ... },
  "credentials": {
    "slackApi": {
      "id": "credential-uuid",
      "name": "Slack Account"
    }
  }
}
```

**Common Credential Types:**

| Node | Credential Type |
|------|-----------------|
| HTTP Request | `httpHeaderAuth`, `httpBasicAuth`, `httpDigestAuth`, `oAuth2Api` |
| Slack | `slackApi` |
| Gmail | `gmailOAuth2` |
| Google Sheets | `googleSheetsOAuth2Api` |

---

## Error Handling

### Per-Node Error Configuration

```json
{
  "name": "HTTP Request",
  "type": "n8n-nodes-base.httpRequest",
  "parameters": { ... },
  "continueOnFail": true,
  "onError": "continueRegularOutput"
}
```

**Options:**

| Setting | Values |
|---------|--------|
| `continueOnFail` | true, false |
| `onError` | "stopWorkflow", "continueRegularOutput", "continueErrorOutput" |

---

## Best Practices

1. **Always use expressions for dynamic values**: `={{ $json.field }}`
2. **Webhook data is under `.body`**: Access via `{{ $json.body.field }}`
3. **Code node must return array**: `return [{ json: {...} }]`
4. **Node names must match exactly in connections**: Case-sensitive
5. **Use typeVersion matching your n8n version**: Check node documentation
