import { SessionGraph } from '../utils/session-graph.js';
import type { ExtensionContext, AgentToolResult } from '@earendil-works/pi-coding-agent';

export async function executeReflectSession(
  toolCallId: string,
  params: { sessionFile: string; leafId: string },
  signal: AbortSignal | undefined,
  onUpdate: ((partialResult: AgentToolResult<unknown>) => void) | undefined,
  ctx: ExtensionContext,
): Promise<AgentToolResult<unknown>> {
  const { sessionFile, leafId } = params;

  onUpdate?.({
    content: [{ type: "text", text: `Loading session graph from ${sessionFile}...` }],
    details: {},
  });

  const graph = new SessionGraph();
  await graph.loadFromFile(sessionFile);

  onUpdate?.({
    content: [{ type: "text", text: `Extracting architectural decisions for leaf ${leafId.substring(0, 8)}...` }],
    details: {},
  });

  const decisions = graph.extractDecisions(leafId);

  if (decisions.length === 0) {
    return {
      content: [{ type: "text", text: "No historical architectural decisions found in this branch." }],
      details: { decisions: [] },
    };
  }

  const adrLog = decisions.map(d =>
    `### ${d.timestamp}\nSummary: ${d.summary}\nConstraints: ${d.constraints.join(', ')}\nDecisions: ${d.decisions.join(', ')}`,
  ).join('\n\n');

  return {
    content: [{ type: "text", text: `# ARCHITECTURAL DECISION RECORDS\n\n${adrLog}` }],
    details: { decisions },
  };
}