import * as path from 'path';
import { Project } from 'ts-morph';
import { runAstAudit } from '../utils/ast-auditor.js';
import type { ExtensionContext, AgentToolResult } from '@earendil-works/pi-coding-agent';

export async function executeAuditUi(
  toolCallId: string,
  params: { targetPath: string },
  signal: AbortSignal | undefined,
  onUpdate: ((partialResult: AgentToolResult<unknown>) => void) | undefined,
  ctx: ExtensionContext,
): Promise<AgentToolResult<unknown>> {
  const { targetPath } = params;

  if (signal?.aborted) {
    throw new Error('Aborted: Audit-UI tool was cancelled before completion.');
  }

  const workspaceRoot = ctx.cwd || process.cwd();
  const resolvedPath = path.resolve(workspaceRoot, targetPath);
  if (!resolvedPath.startsWith(path.resolve(workspaceRoot) + path.sep) && resolvedPath !== path.resolve(workspaceRoot)) {
    throw new Error(`SECURITY VIOLATION: Path traversal detected. ${targetPath} is outside workspace.`);
  }

  onUpdate?.({
    content: [{ type: "text", text: `Parsing AST for ${resolvedPath}...` }],
    details: {},
  });

  const project = new Project({ useInMemoryFileSystem: true });
  const report = runAstAudit(project, resolvedPath);

  if (report.isCompliant) {
    return {
      content: [{ type: "text", text: "COMPLIANT: DOM depth is optimal. No generic aesthetic slop detected." }],
      details: { violations: [] },
    };
  }

  const errorReport = report.violations.map(v =>
    `[${v.severity}] Line ${v.line}: ${v.message}\n  Suggestion: ${v.suggestion}`,
  ).join('\n\n');

  return {
    content: [{ type: "text", text: `VIOLATIONS DETECTED:\n\n${errorReport}\n\nYou must refactor this component immediately.` }],
    details: { violations: report.violations },
  };
}