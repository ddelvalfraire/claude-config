---
description: Python module organization and naming conventions. Auto-loads when .py files are touched.
paths:
  - "**/*.py"
---

# Python Module Layout

## Structure
- Package layout: `app/` or `src/<pkg>/` with one module per concern (`models.py`, `services.py`, `routes.py`, `config.py`). No `utils.py` dumping ground — split by domain (`text_utils.py`, `date_utils.py`) or fold into the owning module.
- One class or one cohesive function family per module. Modules > ~300 lines get split by responsibility.
- Tests mirror the package: `app/services.py` → `tests/test_services.py`.

## Conventions
- snake_case modules/functions, PascalCase classes, UPPER_SNAKE constants. Private = `_leading_underscore`.
- Full type hints on all public functions and any function > 5 lines. `from __future__ import annotations` where helpful.
- No wildcard imports. No `import *`. Explicit relative or absolute imports only.
- Pydantic/dataclasses for structured data, not raw dicts, when the shape is stable.
- Errors: raise specific exceptions; never bare `except:`. Catch only what you handle.

## Async
- Async functions only call async functions — no blocking calls (requests, time.sleep, sync file IO) inside `async def`.
