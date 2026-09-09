---
description: Adding a third-party dependency. Use before installing any new package or library.
---

# New dependency

Complete all steps before writing an import.

1. Look up the latest stable version in the registry (npm/PyPI), not from memory.
2. Check compatibility with the runtime and framework versions plus peer dependencies. Note the chosen version and reason.
3. Check maintenance: last release date, issue ratio, deprecation banners. Flag anything stale or deprecated and propose the maintained alternative before installing.
4. Fetch current docs for the specific APIs we will use and confirm they match the installed version.
5. Name the 1-2 main alternatives and the reason this one wins. Skip if I already picked it.
6. Note the license (flag GPL/AGPL) and notable install or bundle size.

Report in one block, then install and add a test that exercises the library usage:

```
<dep>@<version> - reason
compat: <runtime/framework>
docs: <APIs confirmed current>
license: <x>, size: <y>
```

Task: $ARGUMENTS
