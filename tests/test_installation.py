import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class InstallationTests(unittest.TestCase):
    def test_project_and_global_templates_execute_copied_hooks(self):
        with tempfile.TemporaryDirectory(prefix="config install ") as temp:
            home = Path(temp)
            project = home / "project with spaces"
            subprocess.run(["git", "init", "-b", "main", str(project)],
                           check=True, capture_output=True)
            cases = [("settings.json", project / ".claude"),
                     ("settings.global.json", home / ".claude"),
                     ("codex/hooks.json", project / ".codex"),
                     ("codex/hooks.global.json", home / ".codex")]
            for template, destination in cases:
                with self.subTest(template=template):
                    shutil.copytree(ROOT / "hooks", destination / "hooks")
                    settings = json.loads((ROOT / template).read_text())
                    command = settings["hooks"]["PreToolUse"][0]["hooks"][0]["command"]
                    payload = {"cwd": str(project), "tool_input": {"command": "git push"}}
                    env = {**os.environ, "HOME": str(home), "CLAUDE_PROJECT_DIR": str(project)}
                    result = subprocess.run(["bash", "-c", command], cwd=project,
                                            env=env, input=json.dumps(payload),
                                            text=True, capture_output=True)
                    self.assertEqual(result.returncode, 2, result.stderr)
                    self.assertIn("BLOCKED", result.stderr)


if __name__ == "__main__":
    unittest.main()
