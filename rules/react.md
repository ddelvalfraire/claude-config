---
description: React/TypeScript layering and module organization rules. Auto-loads when .ts/.tsx files are touched.
paths:
  - "**/*.tsx"
  - "**/*.ts"
---

# React Module Layout

## Directory structure (feature-based, not type-based)
```
src/
  features/<feature>/
    components/     # presentational only: props in, JSX out
    hooks/          # feature hooks: state + side effects, NO JSX
    api/            # network calls, serialization — no React imports
    types.ts        # feature domain types
    index.ts        # public surface of the feature
  components/       # shared/generic UI only (Button, Modal...)
  lib/              # pure utilities, zero React
```

## Separation of concerns — enforce strictly
- **UI components** render. No data fetching, no business logic, no direct store access in presentational components.
- **Hooks** own state and effects. A hook never returns JSX, never imports from components/.
- **API/business logic** lives in `api/` or `lib/` — plain functions, testable without rendering, no `useState`/`useEffect` inside.
- If a component is > ~150 lines or contains fetch/store logic, it must be split: logic → hook, markup → component.

## Conventions
- Components: PascalCase files (`UserProfile.tsx`). Hooks: `useX.ts`. Everything else camelCase.
- One component per file. Colocate a component's own styles/types if small; extract at 2+ consumers.
- Props: explicit interfaces, no `any`. Prefer composition over prop-drilling past 2 levels — use context/store.
- No default exports for components (named exports for refactoring safety); default export allowed at feature `index.ts` only.
