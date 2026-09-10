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
- Import cross-feature and cross-layer modules by alias; reserve relative paths (`./`, `../`) for imports within the same feature directory.
- If a repo lacks path aliases, add them to tsconfig.json (`baseUrl` + `paths`) and matching bundler/vitest resolution before importing across directories.
- Reach another feature's public surface through its `index.ts` (`@features/x`); import internals only from within that feature.

## Barrel exports
- Treat a barrel (`index.ts`) as a public API boundary: create one where outside code consumes the folder (each feature's `index.ts`, shared `components/` and `lib/` entry points, published package entries), and rely on path aliases for short imports elsewhere.
- Re-export explicitly: `export { Button } from './Button'` — this keeps tree-shaking effective and the public surface visible, where `export *` forces the bundler to treat the whole sibling surface as reachable.
- Keep barrels pure: limit them to re-exports, and put constants, logic, and side effects in their own modules. Mark type-only re-exports with `export type`.
- Inside the folder, import siblings directly (`./Button`); route imports through the barrel only from outside the folder, which keeps import cycles out.
- Split oversized modules rather than letting a barrel accumulate dozens of exports.

## Conventions
- Name component files in PascalCase (UserProfile.tsx), hooks useX.ts, everything else camelCase.
- One component per file. Colocate small private types; extract shared types at the second consumer.
- Type all props explicitly. Use context or a store instead of prop-drilling past two levels.
- Use named exports for components; allow a default export only at each feature index.ts.

## Ternaries
- Never write nested or multi-line ternary expressions. A ternary is allowed only when it fits on one line and its branches are simple: a single function call or a plain variable/constant.
- Anything else (chained conditions, ternaries as sub-expressions, ternaries spanning lines) becomes if/else statements or an early-return helper function.

```ts
// Bad - nested multi-line ternary
const slugError =
  slugIssue !== 'none'
    ? i18n._(orgSlugMessage(slugIssue, slug))
    : takenSlug === slug
      ? i18n._(orgSlugMessage('taken', slug))
      : null;

// Good - if/else
let slugError: string | null = null;
if (slugIssue !== 'none') {
  slugError = i18n._(orgSlugMessage(slugIssue, slug));
} else if (takenSlug === slug) {
  slugError = i18n._(orgSlugMessage('taken', slug));
}
```
