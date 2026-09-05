---
description: Python module organization and naming conventions. Auto-loads when .py files are touched.
paths:
  - "**/*.py"
---

# Python layout

- Use app/ or src/<pkg>/ with one module per concern: models.py, services.py, routes.py, config.py.
- Split by domain instead of a utils.py dumping ground: text_utils.py, date_utils.py, or fold into the owning module.
- Keep one cohesive class or function family per module. Split modules over ~300 lines by responsibility.
- Mirror tests to the package: app/services.py maps to tests/test_services.py.

## Conventions
- Use snake_case for modules and functions, PascalCase for classes, UPPER_SNAKE for constants, _leading_underscore for private.
- Add full type hints to public functions and any function over 5 lines.
- Use explicit imports; each import names what it uses.
- Model stable data shapes with Pydantic or dataclasses rather than raw dicts.
- Raise specific exceptions and catch only what you handle.
- Use async for I/O-bound code and keep blocking calls (requests, time.sleep, sync file IO) out of async def.

## Tests
Use the testing rules in rules/testing.md for all test code.
