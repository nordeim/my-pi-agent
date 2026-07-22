---
name: pi-agent-customize-system-prompt
description: guide for customizing the Pi Agent system prompt to add custom tools and workflow instructions
version: 1.0.0
---

# Customizing the Pi Coding Agent System Prompt

Pi ([pi.dev](https://pi.dev/)) uses a lightweight, modular system prompt that can be tailored per session, per project, or globally. This guide explains how to inspect the default prompt, append instructions, replace it entirely, and integrate custom tools and workflows.

## 1. Default System Prompt Architecture

The default system prompt is defined in the Pi source code at  
[`packages/agent/src/harness/system-prompt.ts`](https://github.com/earendil-works/pi/blob/main/packages/agent/src/harness/system-prompt.ts).  
Its template dynamically injects the active tool list, MCP server details, and any skill guidelines:

```text
You are an expert coding assistant operating inside pi, a coding agent harness.
You help users by reading files, executing commands, editing code, and writing new files.
Available tools: \${toolsList}. In addition to the tools above, you may have access to
other custom tools depending on the project.

Guidelines:
- Be concise in your responses
- Show file paths clearly when working with files
\${dynamically_injected_tool_or_skill_guidelines}
```

At runtime, Pi also appends contextual information: repository root, current date, active Model Context Protocol (MCP) server configurations, and discovered skills.

## 2. Customization Methods

Pi offers three configuration files that control how the system prompt is built. They can be placed globally (affects all sessions) or locally (per‑project).

| File | Scope | Behaviour | When to Use |
|------|-------|-----------|-------------|
| `SYSTEM.md` | `.pi/` (local) or `~/.pi/agent/` (global) | **Replaces** the entire default prompt preamble. Dynamic tool/skill injection is lost unless you replicate it manually. | When you need a completely different agent identity (e.g., a data analyst or SRE assistant). |
| `APPEND_SYSTEM.md` | `.pi/` or `~/.pi/agent/` | **Appends** instructions to the end of the default prompt. All default tool parsing remains intact. | The recommended method for adding style rules, workflow steps, or custom pseudo‑tools. |
| `AGENTS.md` / `CLAUDE.md` | Repository root | Injected as a project‑specific rule block. Does not alter the core system message. | To enforce coding conventions, testing mandates, or architectural constraints without touching the prompt structure. |

> ⚠️ **Important:** If you completely replace the prompt with `SYSTEM.md`, you must manually handle tools and context injection; otherwise the agent will lose its ability to access the file system, terminal, and other built‑ins.

## 3. Adding Custom Instructions for Specific Workflows

To force the agent to follow a step‑by‑step workflow (e.g., plan → approve → code → test), create an `APPEND_SYSTEM.md` file.

### Step‑by‑Step Example: Strict SRE Workflow

1. Create `.pi/APPEND_SYSTEM.md` in your repository root.
2. Insert the following content:

```markdown
## Workflow: Incident Response

**Identity:** You are an automated Site Reliability Engineer companion. Be precise; do not use conversational filler.

**Execution Protocol:**
1. **Discovery** – Before any edit, run `ls`, `read`, or `bash` to inspect the affected files and architecture.
2. **Plan** – Write a brief markdown plan describing the intended changes. Wait for explicit user approval before proceeding.
3. **Execute** – Apply edits using the `edit` tool.
4. **Verify** – Immediately run the project’s test suite (e.g., `npm test`, `pytest`). If any command fails, stop and ask for guidance.

**Formatting:**
- Always present diffs using unified headers (`--- a/` and `+++ b/`).
- Wrap log snippets or JSON in triple backticks with the appropriate language identifier.
```

3. Apply the changes without restarting the session:
   ```
   /reload
   ```

Now every interaction in this repository will adhere to that workflow.

## 4. Extending the System Prompt with Custom Tools

Pi supports two main approaches for adding custom tools:

### A. Using TypeScript Extensions (native Pi tool schema)

Extensions written with the `@earendil-works/pi-coding-agent` SDK register a proper tool with type‑safe parameters. The tool will appear automatically in the `\${toolsList}` placeholder.

**Example: `fetch_production_logs` extension**

1. Create a file `custom-tools.ts` (or any name) in your extension directory.
2. Write the extension:

```typescript
import { ExtensionAPI } from "@earendil-works/pi-coding-agent";
import { Type } from "typebox";

export default function (pi: ExtensionAPI) {
  pi.registerTool({
    name: "fetch_production_logs",
    label: "Production Log Fetcher",
    description: "Queries the production logging endpoint for recent error traces.",
    parameters: Type.Object({
      serviceName: Type.String({ description: "Microservice name, e.g., 'auth-service'" }),
      limit: Type.Optional(Type.Number({ description: "Number of log entries" })),
    }),
    execute: async (input) => {
      // Your custom implementation
      return { output: `[ERROR] Token verification failed for ${input.serviceName} at step 2.` };
    },
  });
}
```

3. Load the extension by placing it in the Pi extensions folder or referencing it in your configuration. The tool and any associated prompt guidelines will be injected automatically.

### B. Declaring Pseudo‑Tools via `APPEND_SYSTEM.md`

For quick, no‑code additions, define “pseudo‑tools” as text instructions that the agent will interpret. Because they are not validated by a schema, they are less robust but require zero setup.

Add this to `.pi/APPEND_SYSTEM.md`:

```markdown
## Available Custom Workflows

When the user asks to analyze logs or fetch internal metrics, use the following procedures:

### Tool: fetch_internal_metrics
- **Description:** Queries local telemetry.
- **Usage:** Run `curl -s http://localhost:8080/metrics` via the `bash` tool.
- **Output:** Parse the JSON and present it as a markdown table.
```

After reloading (`/reload`), the agent will treat these as available actions.

## 5. Integrating External Tools via MCP

If you use Model Context Protocol servers, Pi automatically includes their capabilities in the system prompt. To ensure the agent uses them correctly, add explicit guidelines in `APPEND_SYSTEM.md`:

```markdown
## MCP Server Usage
- When the user mentions “database”, query the `postgres-mcp-server`.
- Always verify available MCP tools with `mcp_list_tools` before executing any command.
```

## 6. Inspecting the Final System Prompt

You can always see exactly what is being sent to the language model:

1. In an active Pi session, run:
   ```
   /export my_debug.html
   ```
2. Open `my_debug.html` in a browser. The page contains the full, flattened system message, including all injected tools, guidelines, and customisations.

This export is invaluable for debugging unexpected behavior.

## 7. Quick Reference

| Goal | Recommended File | Command |
|------|------------------|---------|
| Add style/conciseness rules | `APPEND_SYSTEM.md` | `/reload` |
| Completely change agent persona | `SYSTEM.md` | `/reload` |
| Enforce project‑specific coding rules | `AGENTS.md` in repo root | restart session |
| Add a custom, validated tool | TypeScript extension | Reload extensions (automatic) |
| Add a quick pseudo‑tool | `APPEND_SYSTEM.md` (plain text) | `/reload` |
| Debug the final prompt | – | `/export` |

---

The default system prompt template for the Pi coding agent is maintained at `https://github.com/earendil-works/pi/blob/main/packages/agent/src/harness/system-prompt.ts`

For more details, refer to the [official Pi documentation](https://pi.dev/docs/latest/usage) and the [source repository](https://github.com/earendil-works/pi).
