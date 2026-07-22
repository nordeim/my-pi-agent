import type { ExtensionAPI } from '@earendil-works/pi-coding-agent';
import { Type } from 'typebox';
import { executeAuditUi } from './tools/audit-ui.js';
import { executeReflectSession } from './tools/reflect-session.js';

export default async function (pi: ExtensionAPI) {
  pi.on('context', async (event, ctx) => {
    const constraintMessage = {
      role: 'system' as const,
      content: `CRITICAL DIRECTIVE: You MUST retain all brutalist aesthetic rules:
- No rounded corners, no shadows, no gradients.
- JSX nesting depth max 4.
- Banned Tailwind classes: rounded-*, shadow-*, bg-gradient-*.
These constraints must survive compaction.`,
    };
    (event.messages as unknown[]).push(constraintMessage);
  });

  pi.registerTool({
    name: 'audit-ui',
    label: 'Audit UI',
    description: 'Scans a target React/TSX file for DOM bloat (depth > 4) and generic aesthetic slop (banned Tailwind classes).',
    parameters: Type.Object({
      targetPath: Type.String({ description: 'Relative path to the TSX file within the workspace.' }),
    }),
    execute: executeAuditUi,
    renderCall: (args, _theme, _context) =>
      `┌─ AUDIT_UI ──────────────────────────────────────\n│ Scanning: ${args.targetPath ?? 'unknown'}\n└──────────────────────────────────────────────────` as any,
    renderResult: (result, _options, _theme, _context) =>
      `┌─ AUDIT RESULT ──────────────────────────────────\n${result.content[0]?.type === 'text' ? result.content[0].text : 'No output'}\n└──────────────────────────────────────────────────` as any,
  });

  pi.registerTool({
    name: 'reflect-session',
    label: 'Reflect Session',
    description: 'Analyzes the current JSONL session tree to extract past Architectural Decision Records (ADRs) from compaction events.',
    parameters: Type.Object({
      sessionFile: Type.String({ description: 'Absolute path to the session_id.jsonl file.' }),
      leafId: Type.String({ description: 'The ID of the current leaf node to trace back from.' }),
    }),
    execute: executeReflectSession,
    renderCall: (args, _theme, _context) =>
      `┌─ REFLECT_SESSION ───────────────────────────────\n│ Tracing tree from leaf: ${args.leafId.substring(0, 8) ?? 'unknown'}...\n└──────────────────────────────────────────────────` as any,
    renderResult: (result, _options, _theme, _context) =>
      `┌─ SESSION MEMORY ────────────────────────────────\n${result.content[0]?.type === 'text' ? result.content[0].text : 'No output'}\n└──────────────────────────────────────────────────` as any,
  });

  pi.registerCommand('avant-garde', {
    description: 'Lock session into strict brutalist design mode.',
    handler: async (args, ctx) => {
      ctx.ui.notify('STRICT AVANT-GARDE MODE activated', 'info');
    },
  });

  pi.registerMessageRenderer('ava-brutalist', (message, _options, _theme) => {
    const msg = message as unknown as { content?: string };
    if (msg.content) {
      const border = '\x1b[90m┌─ AVA OUTPUT ────────────────────────────────────────\x1b[0m';
      const footer = '\x1b[90m└──────────────────────────────────────────────────────\x1b[0m';
      return `${border}\n${msg.content}\n${footer}` as any;
    }
    return undefined;
  });
}