# n8n Expression Syntax

Complete reference for n8n expressions and data access patterns.

---

## Expression Basics

n8n uses **double curly braces** for dynamic expressions:

```
{{ expression }}
```

### Valid Expressions

| Expression | Result |
|------------|--------|
| `{{ $json.email }}` | Email field from current item |
| `{{ $json.body.name }}` | Name from webhook body |
| `{{ $node["HTTP Request"].json.data }}` | Data from specific node |

### Invalid Expressions

| Expression | Problem |
|------------|---------|
| `$json.email` | Missing `{{ }}` braces - treated as literal text |
| `{ $json.email }` | Single braces - invalid syntax |
| `{{ $json.email` | Unclosed braces - syntax error |

---

## Core Variables

### Current Item Data

| Variable | Description |
|----------|-------------|
| `$json` | JSON data of current item |
| `$json.fieldName` | Specific field from current item |
| `$json['field with spaces']` | Field with special characters |
| `$binary` | Binary data of current item |

### Previous Node Data

| Variable | Description |
|----------|-------------|
| `$("NodeName").first()` | First item from named node |
| `$("NodeName").item` | Linked item from named node |
| `$("NodeName").all()` | All items from named node |
| `$("NodeName").last()` | Last item from named node |

### Date/Time

| Variable | Description |
|----------|-------------|
| `$now` | Current date and time (DateTime object) |
| `$today` | Today's date at midnight |
| `$now.toFormat("yyyy-MM-dd")` | Formatted date string |

### Environment & Workflow

| Variable | Description |
|----------|-------------|
| `$env.VARIABLE_NAME` | Environment variable |
| `$workflow.id` | Current workflow ID |
| `$workflow.name` | Current workflow name |
| `$execution.id` | Current execution ID |

---

## Webhook Data Structure

**CRITICAL**: Webhook data is nested under `.body` property!

```json
{
  "headers": { "content-type": "application/json" },
  "params": {},
  "query": {},
  "body": {
    "name": "John Doe",
    "email": "john@example.com",
    "message": "Hello!"
  }
}
```

### Correct Access

```
{{ $json.body.name }}     ✅ From webhook trigger
{{ $json.body.email }}    ✅ Nested under .body
```

### Incorrect Access

```
{{ $json.name }}          ❌ Returns undefined
{{ $json.email }}         ❌ Wrong - not at root level
```

---

## Conditionals

### $if Helper

```
{{ $if(condition, "trueValue", "falseValue") }}
```

**Examples:**

```
{{ $if($json.status === "active", "Yes", "No") }}
{{ $if($json.price > 100, "Premium", "Standard") }}
```

### Ternary Operator

```
{{ condition ? "trueValue" : "falseValue" }}
```

**Examples:**

```
{{ $json.age >= 18 ? "Adult" : "Minor" }}
{{ $json.items.length > 0 ? $json.items[0].name : "Empty" }}
```

### $ifEmpty Helper

Returns second value if first is empty:

```
{{ $ifEmpty($json.optionalField, "default value") }}
```

---

## String Methods

| Method | Example |
|--------|---------|
| `toUpperCase()` | `{{ $json.name.toUpperCase() }}` |
| `toLowerCase()` | `{{ $json.email.toLowerCase() }}` |
| `includes("text")` | `{{ $json.message.includes("urgent") }}` |
| `trim()` | `{{ $json.text.trim() }}` |
| `split(",")` | `{{ $json.tags.split(",") }}` |
| `replace("old", "new")` | `{{ $json.text.replace("foo", "bar") }}` |
| `extractEmail()` | `{{ $json.content.extractEmail() }}` |

---

## Array Methods

| Method | Example | Description |
|--------|---------|-------------|
| `length` | `{{ $json.items.length }}` | Array size |
| `first()` | `{{ $json.items.first() }}` | First element |
| `last()` | `{{ $json.items.last() }}` | Last element |
| `join(", ")` | `{{ $json.tags.join(", ") }}` | Join to string |
| `map(x => x.id)` | `{{ $json.items.map(x => x.id) }}` | Transform items |
| `filter(x => x > 10)` | `{{ $json.scores.filter(x => x > 10) }}` | Filter items |
| `find(x => x.id === 1)` | `{{ $json.items.find(x => x.id === 1) }}` | Find first match |
| `reduce((a,b) => a + b)` | `{{ $json.prices.reduce((a,b) => a + b) }}` | Reduce to single value |
| `sum()` | `{{ $json.prices.sum() }}` | Sum all numbers |
| `average()` | `{{ $json.scores.average() }}` | Average of numbers |
| `unique()` | `{{ $json.tags.unique() }}` | Remove duplicates |
| `sort()` | `{{ $json.names.sort() }}` | Sort strings |
| `slice(0, 5)` | `{{ $json.items.slice(0, 5) }}` | First 5 items |

---

## Object Methods

| Method | Example | Description |
|--------|---------|-------------|
| `keys()` | `{{ $json.keys() }}` | Get all keys |
| `values()` | `{{ $json.values() }}` | Get all values |
| `has("key")` | `{{ $json.has("email") }}` | Check if key exists |

---

## DateTime Methods (Luxon)

| Method | Example |
|--------|---------|
| `toFormat("yyyy-MM-dd")` | `{{ $now.toFormat("yyyy-MM-dd") }}` |
| `toISO()` | `{{ $now.toISO() }}` |
| `plus({ days: 1 })` | `{{ $now.plus({ days: 1 }) }}` |
| `minus({ hours: 2 })` | `{{ $now.minus({ hours: 2 }) }}` |
| `setZone("UTC")` | `{{ $now.setZone("UTC") }}` |
| `weekday` | `{{ $now.weekday }}` |
| `month` | `{{ $now.month }}` |
| `year` | `{{ $now.year }}` |

---

## Complex Expressions

### IIFE for Multi-Line Code

For complex logic, use Immediately Invoked Function Expression:

```
{{ 
  (() => {
    const items = $json.items;
    const total = items.reduce((sum, item) => sum + item.price, 0);
    const avg = total / items.length;
    return avg.toFixed(2);
  })() 
}}
```

### Nested Property Access

```
{{ $json.level1.level2.level3 }}
{{ $json['level1']['level2']['level3'] }}
{{ $json?.optional?.field ?? 'default' }}
```

### Combining Data from Multiple Nodes

```
{{ $json.name }} - {{ $("HTTP Request").first().json.title }}
```

---

## Common Patterns

### Format Date for API

```
{{ $now.toFormat("yyyy-MM-dd'T'HH:mm:ss") }}
```

### Build URL with Parameters

```
https://api.example.com/users/{{ $json.id }}?format=json
```

### Conditional Message

```
{{ $if($json.status === "success", "✅ Done", "❌ Failed") }}
```

### Extract Domain from Email

```
{{ $json.email.split("@")[1] }}
```

### Join Array as Comma List

```
{{ $json.tags.join(", ") }}
```

### Calculate Total

```
{{ $json.items.map(x => x.price).sum() }}
```

---

## Error Handling

### Check for Undefined

```
{{ $json.optionalField ?? 'default value' }}
{{ $json.field || 'fallback' }}
```

### Safe Property Access

```
{{ $json?.nested?.field }}
{{ $json && $json.field ? $json.field : 'none' }}
```

### Validate Required Fields

```
{{ $if($json.email && $json.name, "Valid", "Missing fields") }}
```

---

## Expression Gotchas

1. **Webhook data under `.body`** - Most common mistake
2. **Node names are case-sensitive** - `"HTTP Request"` ≠ `"http request"`
3. **Expressions must be single-line** - Use IIFE for multi-line logic
4. **Quotes in JSON** - Use `{{ $json["field name"] }}` for fields with spaces
5. **No external imports** - Can't use `require()` or `import` in expressions
