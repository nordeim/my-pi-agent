---
name: scaffold-ui
description: Generates an anti-generic React component with brutalist styling and strict DOM hygiene.
---

When invoked, produce a React component following these strict rules:

1. **Imports**: Group external (react, lucide-react) vs internal imports.
2. **Structure**: Export the default function. Use early returns for conditional states (loading, error, empty).
3. **Styling Constraints**: 
   - Use stark, high-contrast Tailwind classes (`bg-zinc-950 text-zinc-50 border-2 border-white`).
   - ABSOLUTELY NO `rounded-*`, `shadow-*`, or `bg-gradient-*`.
4. **Hygiene**: Ensure JSX nesting never exceeds 4 levels. Extract sub-components if necessary.
5. **MANDATORY AUDIT**: Before writing the file to disk, you MUST invoke the `audit-ui` tool on the generated code. If it returns violations, you must refactor and re-audit until it passes.