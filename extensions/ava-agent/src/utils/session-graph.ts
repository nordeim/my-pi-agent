import * as fs from 'fs';
import * as readline from 'readline';

export interface SessionNode {
  id: string;
  parentId: string | null;
  type: string;
  role: string;
  content: string;
  timestamp: string;
  isCompaction: boolean;
}

export interface ArchitecturalDecisionRecord {
  timestamp: string;
  summary: string;
  constraints: string[];
  decisions: string[];
}

interface RawSessionEntry {
  id: string;
  parentId: string | null;
  type: string;
  timestamp: string;
  message?: {
    role: string;
    content: string;
  };
  summary?: string;
}

function isRawSessionEntry(obj: unknown): obj is RawSessionEntry {
  if (typeof obj !== 'object' || obj === null) return false;
  const record = obj as Record<string, unknown>;
  return typeof record.id === 'string' &&
    typeof record.type === 'string' &&
    typeof record.timestamp === 'string';
}

export class SessionGraph {
  private nodes = new Map<string, SessionNode>();

  async loadFromFile(filePath: string): Promise<void> {
    const fileStream = fs.createReadStream(filePath, { encoding: 'utf-8' });
    const rl = readline.createInterface({ input: fileStream, crlfDelay: Infinity });

    for await (const line of rl) {
      if (!line.trim()) continue;
      try {
        const raw = JSON.parse(line) as unknown;
        if (!isRawSessionEntry(raw)) continue;

        const isCompaction = raw.type === 'compaction';
        let content = '';
        let role = '';

        if (raw.message) {
          role = raw.message.role;
          content = raw.message.content;
        } else if (isCompaction && raw.summary) {
          content = raw.summary;
          role = 'compaction';
        }

        this.nodes.set(raw.id, {
          id: raw.id,
          parentId: raw.parentId,
          type: raw.type,
          role,
          content,
          timestamp: raw.timestamp,
          isCompaction,
        });
      } catch {
        // Skip malformed lines
      }
    }
  }

  resolvePath(leafId: string): SessionNode[] {
    const path: SessionNode[] = [];
    let currentId: string | null = leafId;

    const visited = new Set<string>();

    while (currentId) {
      if (visited.has(currentId)) break;
      const node = this.nodes.get(currentId);
      if (!node) break;
      visited.add(currentId);
      path.unshift(node);
      currentId = node.parentId;
    }

    return path;
  }

  extractDecisions(leafId: string): ArchitecturalDecisionRecord[] {
    const path = this.resolvePath(leafId);
    const decisions: ArchitecturalDecisionRecord[] = [];

    for (const node of path) {
      if (node.isCompaction) {
        decisions.push({
          timestamp: node.timestamp,
          summary: node.content.substring(0, 150).replace(/\n/g, ' ') + '...',
          constraints: this.extractMarkdownList(node.content, 'Constraints'),
          decisions: this.extractMarkdownList(node.content, 'Key Decisions'),
        });
      }
    }

    return decisions;
  }

  private extractMarkdownList(text: string, header: string): string[] {
    const regex = new RegExp(`# ${header}\\n((?:- .+\\n?)+)`, 'i');
    const match = text.match(regex);
    if (!match || !match[1]) return [];
    return match[1].split('\n').filter(Boolean).map(line => line.replace(/^-\s*/, ''));
  }
}