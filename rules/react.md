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

## Conventions
- Name component files in PascalCase (UserProfile.tsx), hooks useX.ts, everything else camelCase.
- One component per file. Colocate small private types; extract shared types at the second consumer.
- Type all props explicitly. Use context or a store instead of prop-drilling past two levels.
- Use named exports for components; allow a default export only at each feature index.ts.
