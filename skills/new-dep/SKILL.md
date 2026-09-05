---
name: new-dep
description: Adding a third-party dependency. Use whenever installing any new package/library into a project.
---

# New Dependency Checklist

Run ALL steps before writing any import. Skip nothing.

## 1. Version & compatibility
- Look up the latest stable version (npm/pypi registry, not memory).
- Check compatibility with the project: runtime version (node/python), framework version (React/FastAPI/...), and peer dependencies. Report the exact version you chose and why.
- Check maintenance signals: last release date, open issue ratio, deprecated banners. Flag anything stale (>1yr unmaintained) or deprecated BEFORE installing — propose the maintained alternative.

## 2. Documentation (via context7 if available)
- Fetch current docs for the specific APIs we'll use — never write integration code from training-data memory of the API.
- Confirm the API surface actually matches the version being installed (breaking changes between major versions are the #1 failure mode).

## 3. Alternatives
- Name the 1–2 main alternatives and why this one wins (one line each). If I've already picked it, skip this step.

## 4. Footprint
- Note license (flag GPL/AGPL in a product), bundle size / install size if notable, and whether it pulls heavy transitive deps.

## Report format (one short block)
```
<dep>@<version> — reason
compat: <runtime/framework OK or issue>
docs: <APIs confirmed current via context7/web>
license: MIT (fine) | size: ~40kB min+gz
```

Then and only then: install, write the integration, and add a test exercising the library usage.
