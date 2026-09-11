import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class HookTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="hook tests ")
        self.addCleanup(self.temp.cleanup)
        self.cwd = Path(self.temp.name)
        subprocess.run(["git", "init", "-b", "main", str(self.cwd)], check=True,
                       capture_output=True)

    def hook(self, name, args=None, **extra):
        payload = {"cwd": str(self.cwd), "tool_input": args or {}, **extra}
        script = ROOT / "hooks" / name
        self.assertTrue(script.is_file(), f"Missing hook: {name}")
        return subprocess.run(["bash", str(script)], input=json.dumps(payload),
                              text=True, capture_output=True, cwd=self.cwd)

    def test_guard_bare_push_on_main_blocks(self):
        result = self.hook("block-main-commit.sh", {"command": "git push"})
        self.assertEqual(result.returncode, 2)
        self.assertIn("BLOCKED", result.stderr)

    def test_guard_feature_push_to_main_blocks(self):
        subprocess.run(["git", "checkout", "-b", "fix/topic"], cwd=self.cwd,
                       check=True, capture_output=True)
        result = self.hook("block-main-commit.sh", {"command": "git push origin HEAD:main"})
        self.assertEqual(result.returncode, 2)

    def test_guard_git_directory_option_blocks(self):
        result = self.hook("block-main-commit.sh", {"command": f"git -C '{self.cwd}' commit -m test"})
        self.assertEqual(result.returncode, 2)

    def test_guard_feature_commit_allows(self):
        subprocess.run(["git", "checkout", "-b", "fix/topic"], cwd=self.cwd,
                       check=True, capture_output=True)
        self.assertEqual(self.hook("block-main-commit.sh", {"command": "git commit -m test"}).returncode, 0)

    def test_guard_command_workdir_blocks(self):
        repo = self.cwd / "other"
        subprocess.run(["git", "init", "-b", "master", str(repo)], check=True, capture_output=True)
        subprocess.run(["git", "checkout", "-b", "fix/topic"], cwd=self.cwd, check=True, capture_output=True)
        self.assertEqual(self.hook("block-main-commit.sh", {"command": "git commit -m test", "workdir": str(repo)}).returncode, 2)

    def test_comments_camelcase_path_reports_saved_violation(self):
        file = self.cwd / "café file.ts"
        file.write_text("// const old = 1;", encoding="utf-8")
        result = self.hook("comment-review.sh", {"filePath": str(file)})
        self.assertEqual(result.returncode, 2)
        self.assertIn("COMMENT RULE VIOLATION", result.stderr)

    def test_comments_markdown_headings_are_not_code_comments(self):
        file = self.cwd / "README.md"
        file.write_text("# INSTALLATION\n")
        self.assertEqual(self.hook("comment-review.sh", {"file_path": str(file)}).returncode, 0)

    def test_comments_corrected_file_allows(self):
        file = self.cwd / "fixed.ts"
        file.write_text("// Retry because the upstream cache is eventually consistent.\n")
        self.assertEqual(self.hook("comment-review.sh", {"file_path": str(file)}).returncode, 0)

    def test_comments_codex_patch_reviews_added_file(self):
        file = self.cwd / "new.ts"
        file.write_text("// const old = 1;\n")
        patch = "*** Begin Patch\n*** Add File: new.ts\n+// const old = 1;\n*** End Patch"
        self.assertEqual(self.hook("comment-review.sh", {"command": patch}, tool_name="apply_patch").returncode, 2)

    def test_format_new_file_with_spaces_uses_local_binary(self):
        binary = self.cwd / "node_modules/.bin/biome"
        binary.parent.mkdir(parents=True)
        binary.write_text('#!/bin/sh\nprintf "%s\\n" "$@" > biome-args\n')
        binary.chmod(0o755)
        file = self.cwd / "new file.ts"
        file.write_text("let x=1")
        result = self.hook("format-on-edit.sh", {"file_path": str(file)})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.cwd / "biome-args").read_text().splitlines(),
                         ["check", "--write", str(file)])

    def test_format_failure_reports_feedback(self):
        binary = self.cwd / "node_modules/.bin/biome"
        binary.parent.mkdir(parents=True)
        binary.write_text('#!/bin/sh\necho "lint failed" >&2\nexit 1\n')
        binary.chmod(0o755)
        file = self.cwd / "new.ts"
        file.touch()
        result = self.hook("format-on-edit.sh", {"file_path": str(file)})
        self.assertEqual(result.returncode, 2)
        self.assertIn("lint failed", result.stderr)

    def test_stop_failure_blocks_and_active_retry_skips(self):
        (self.cwd / "package.json").write_text('{"scripts":{"test":"exit 1"},"packageManager":"npm@11.0.0"}')
        result = self.hook("test-on-stop.sh")
        self.assertEqual(result.returncode, 2)
        self.assertIn("test", result.stderr.lower())
        self.assertEqual(self.hook("test-on-stop.sh", stop_hook_active=True).returncode, 0)

    def test_stop_non_node_project_skips(self):
        self.assertEqual(self.hook("test-on-stop.sh").returncode, 0)

    def test_malformed_hook_input_reports_error(self):
        result = subprocess.run(["bash", str(ROOT / "hooks/block-main-commit.sh")],
                                input="{bad", text=True, capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("HOOK ERROR", result.stderr)

    def test_settings_comment_review_runs_after_edit(self):
        settings = json.loads((ROOT / "settings.json").read_text())
        pre = json.dumps(settings["hooks"]["PreToolUse"])
        post = json.dumps(settings["hooks"]["PostToolUse"])
        self.assertNotIn("comment-review", pre)
        self.assertIn("after", post)

    def test_guard_quoted_commit_text_is_not_executed(self):
        self.assertEqual(self.hook("block-main-commit.sh", {"command": "printf '%s' 'git commit'"}).returncode, 0)

    def test_guard_cd_and_rtk_wrappers_block(self):
        result = self.hook("block-main-commit.sh", {"command": f"cd '{self.cwd}' && rtk git commit -m test"})
        self.assertEqual(result.returncode, 2)

    def test_comments_renamed_patch_reviews_destination(self):
        (self.cwd / "renamed.ts").write_text("// const obsolete = 1;\n")
        patch = "*** Begin Patch\n*** Update File: old.ts\n*** Move to: renamed.ts\n@@\n*** End Patch"
        self.assertEqual(self.hook("comment-review.sh", {"patchText": patch}).returncode, 2)

    def test_guard_wrong_command_type_reports_error(self):
        result = self.hook("block-main-commit.sh", {"command": ["git", "push"]})
        self.assertEqual(result.returncode, 2)
        self.assertIn("must be a string", result.stderr)

    def test_format_missing_binary_skips(self):
        file = self.cwd / "new.ts"
        file.touch()
        self.assertEqual(self.hook("format-on-edit.sh", {"filePath": str(file)}).returncode, 0)

    def test_stop_success_allows(self):
        (self.cwd / "package.json").write_text('{"scripts":{"test":"exit 0"},"packageManager":"npm@11.0.0"}')
        self.assertEqual(self.hook("test-on-stop.sh").returncode, 0)

    def test_stop_malformed_package_reports_error(self):
        (self.cwd / "package.json").write_text('{bad')
        result = self.hook("test-on-stop.sh")
        self.assertEqual(result.returncode, 2)
        self.assertIn("HOOK ERROR", result.stderr)


if __name__ == "__main__":
    unittest.main()
