import { Project, SyntaxKind, type Node } from 'ts-morph';

export interface AuditViolation {
  type: 'DOM_DEPTH' | 'AESTHETIC_SLOP';
  severity: 'CRITICAL' | 'WARNING';
  message: string;
  line: number;
  suggestion: string;
}

export interface AuditReport {
  filePath: string;
  violations: AuditViolation[];
  isCompliant: boolean;
}

const BANNED = new Set([
  'rounded-sm', 'rounded-md', 'rounded-lg', 'rounded-xl', 'rounded-2xl', 'rounded-3xl', 'rounded-full',
  'shadow-sm', 'shadow-md', 'shadow-lg', 'shadow-xl', 'shadow-2xl',
  'bg-gradient-to-r', 'bg-gradient-to-b', 'bg-gradient-to-tr',
  'border-gray-100', 'border-gray-200', 'border-gray-300',
]);

const MAX_DEPTH = 4;

function getJsxDepth(node: Node): number {
  return node.getAncestors().filter(a =>
    a.getKind() === SyntaxKind.JsxElement || a.getKind() === SyntaxKind.JsxSelfClosingElement
  ).length;
}

export function runAstAudit(project: Project, filePath: string): AuditReport {
  const sourceFile = project.addSourceFileAtPath(filePath);
  const violations: AuditViolation[] = [];

  // Check JSX nesting depth
  sourceFile.forEachDescendant((node) => {
    if (node.getKind() === SyntaxKind.JsxElement || node.getKind() === SyntaxKind.JsxSelfClosingElement) {
      const depth = getJsxDepth(node);
      if (depth > MAX_DEPTH) {
        violations.push({
          type: 'DOM_DEPTH',
          severity: 'CRITICAL',
          line: node.getStartLineNumber(),
          message: `JSX nesting depth is ${depth}. Maximum allowed is ${MAX_DEPTH}.`,
          suggestion: 'Extract inner JSX into a dedicated component.',
        });
      }
    }
  });

  // Check banned Tailwind classes
  sourceFile.forEachDescendant((node) => {
    if (node.getKind() === SyntaxKind.JsxAttribute) {
      const attr = node.asKindOrThrow(SyntaxKind.JsxAttribute);
      const attrName = attr.getNameNode().getText();
      if (attrName === 'className') {
        const init = attr.getInitializer();
        if (init && init.getKind() === SyntaxKind.StringLiteral) {
          const value = init.asKindOrThrow(SyntaxKind.StringLiteral).getLiteralValue();
          const classes = value.split(/\s+/);
          for (const cls of classes) {
            if (BANNED.has(cls)) {
              violations.push({
                type: 'AESTHETIC_SLOP',
                severity: 'CRITICAL',
                line: node.getStartLineNumber(),
                message: `Class "${cls}" violates brutalist design rules.`,
                suggestion: 'Use flat, high-contrast primitives like border-2, bg-zinc-950.',
              });
            }
          }
        }
      }
    }
  });

  const unique = Array.from(new Map(violations.map(v => [`${v.line}-${v.type}`, v])).values());

  return { filePath, violations: unique, isCompliant: unique.length === 0 };
}