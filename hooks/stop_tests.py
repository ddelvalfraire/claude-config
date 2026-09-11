"""Run configured Node tests at stop without recursive continuation."""

import json
import subprocess

from hook_input import HookInput


def stop_tests(data: HookInput) -> None:
    """Surface test failures once; skip projects without a Node test script."""
    if data.stop_hook_active:
        return
    for directory in (data.cwd, *data.cwd.parents):
        package = directory / "package.json"
        if not package.is_file():
            continue
        config = json.loads(package.read_text(encoding="utf-8"))
        if not config.get("scripts", {}).get("test"):
            return
        manager = config.get("packageManager", "").split("@", 1)[0]
        if not manager:
            manager = "pnpm" if (directory / "pnpm-lock.yaml").exists() else "npm"
        if manager not in {"pnpm", "npm", "yarn", "bun"}:
            raise ValueError(f"Unsupported test package manager: {manager}")
        result = subprocess.run([manager, "run", "test"], cwd=directory,
                                capture_output=True, text=True, timeout=120)
        if result.returncode:
            raise ValueError(f"{manager} run test failed ({result.returncode}):\n" +
                             (result.stdout + result.stderr)[-12000:])
        return
