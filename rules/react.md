---
description: React/TypeScript layering and module organization rules. Auto-loads when .ts/.tsx files are touched.
paths:
  - "**/*.tsx"
  - "**/*.ts"
---

# React layout

Use feature-based structure:

```
src/
  features/<feature>/
    components/     # presentational: props in, JSX out
    hooks/          # state and side effects, no JSX
    api/            # network calls and serialization, no React imports
    types.ts        # domain types
    index.ts        # public surface of the feature
  components/       # shared generic UI (Button, Modal, ...)
  lib/              # pure utilities, zero React
```

## Separation
- Put data fetching, business logic, and store access in hooks or api/, and keep components rendering-only.
- Keep hooks free of JSX and free of imports from components/.
- Write business logic as plain testable functions in api/ or lib/.
- Split any component over ~150 lines or containing fetch/store logic: logic into a hook, markup into a component.

## Imports
- Prefer aliased paths over relative ones: use `@/lib/...`, `@/components/...`, `@features/<name>` style imports instead of `../../` chains.
- Cross-feature and cross-layer imports must use an alias. Relative paths (`./`, `../`) are allowed only within the same feature directory.
- If a repo lacks path aliases, add them to tsconfig.json (`baseUrl` + `paths`) and matching bundler/vitest resolution before importing across directories.
- Never import a feature's internals (`@features/x/components/...`) from another feature; go through its public `index.ts`.

## Barrel exports
- A barrel (`index.ts`) is a public API boundary, not a default. Create one only where outside code consumes the folder: each feature's `index.ts`, shared `components/` and `lib/` entry points, and published package entries.
- Do NOT create app-wide barrels (e.g. a single `src/index.ts` re-exporting everything) or barrels whose only purpose is tidier imports — path aliases give short imports without the module-graph cost.
- Re-export explicitly: `export { Button } from './Button'`, never `export *`. Wildcard barrels defeat tree-shaking and hide the public surface.
- Keep barrels pure: re-exports only, no constants, no logic, no side effects. Mark type-only re-exports with `export type`.
- Inside the folder, import siblings directly (`./Button`), never through the folder's own barrel — that's how import cycles start.
- Keep barrels small; a barrel with dozens of exports is a smell — split the module instead.

## Conventions
- Name component files in PascalCase (UserProfile.tsx), hooks useX.ts, everything else camelCase.
- One component per file. Colocate small private types; extract shared types at the second consumer.
- Type all props explicitly. Use context or a store instead of prop-drilling past two levels.
- Use named exports for components; allow a default export only at each feature index.ts.
