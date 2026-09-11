"""Normalize the shared Claude, Codex, and OpenCode hook payloads."""

from dataclasses import dataclass
from pathlib import Path
import re


@dataclass
class HookInput:
    """Carry validated tool arguments and their effective working directory."""

    cwd: Path
    args: dict
    stop_hook_active: bool = False

    @classmethod
    def parse(cls, payload: dict) -> "HookInput":
        """Reject malformed payloads instead of silently bypassing hooks."""
        if not isinstance(payload, dict):
            raise ValueError("hook input must be an object")
        args = payload.get("tool_input", {})
        if not isinstance(args, dict):
            raise ValueError("tool_input must be an object")
        for key in ("command", "cmd", "file_path", "filePath", "patchText", "workdir", "cwd"):
            if key in args and not isinstance(args[key], str):
                raise ValueError(f"{key} must be a string")
        cwd = args.get("workdir") or args.get("cwd") or payload.get("cwd") or str(Path.cwd())
        if not isinstance(cwd, str):
            raise ValueError("cwd must be a string")
        base = Path(payload.get("cwd") or Path.cwd())
        return cls((base / cwd).resolve(), args, payload.get("stop_hook_active") is True)

    def files(self) -> list[Path]:
        """Find saved paths without relying on Git tracking or whitespace splitting."""
        path = self.args.get("file_path") or self.args.get("filePath")
        if path:
            return [(self.cwd / path).resolve()]
        patch = self.args.get("patchText") or self.args.get("command", "")
        paths = []
        for line in patch.splitlines():
            match = re.match(r"^\*\*\* (?:Add File|Update File|Move to): (.+)$", line)
            if match:
                paths.append((self.cwd / match[1]).resolve())
        return list(dict.fromkeys(paths))
