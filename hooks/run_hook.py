"""Expose the same hook behavior to each supported agent host."""

import json
import subprocess
import sys

from file_checks import comments, format_files
from git_guard import guard
from hook_input import HookInput
from stop_tests import stop_tests


def main() -> int:
    """Convert validation and process errors into agent-visible hook feedback."""
    try:
        data = HookInput.parse(json.load(sys.stdin))
        action = sys.argv[1]
        if action == "after":
            errors = []
            for check in (format_files, comments):
                try:
                    check(data)
                except (ValueError, OSError, subprocess.TimeoutExpired) as error:
                    errors.append(str(error))
            if errors:
                raise ValueError("\n".join(errors))
        else:
            {"guard": guard, "comments": comments, "format": format_files, "stop": stop_tests}[action](data)
        return 0
    except (ValueError, OSError, subprocess.TimeoutExpired) as error:
        print(f"HOOK ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
