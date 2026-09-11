"""Catch direct protected-branch writes in ordinary shell commands."""

from pathlib import Path
import shlex
import subprocess

from hook_input import HookInput

PROTECTED = {"main", "master", "refs/heads/main", "refs/heads/master"}


def git_output(prefix: list[str], cwd: Path, *args: str) -> str:
    """Query local Git state without executing the proposed command."""
    result = subprocess.run(prefix + list(args), cwd=cwd, capture_output=True,
                            text=True, timeout=10)
    return result.stdout.strip() if result.returncode == 0 else ""


def git_invocation(tokens: list[str], cwd: Path) -> tuple[list[str], list[str], Path]:
    """Retain Git global options when determining the target repository."""
    prefix = ["git"]
    index = 1
    while index < len(tokens) and tokens[index].startswith("-"):
        option = tokens[index]
        prefix.append(option)
        index += 1
        if option in ("-C", "-c", "--git-dir", "--work-tree", "--namespace"):
            if index == len(tokens):
                raise ValueError(f"missing argument for git {option}")
            prefix.append(tokens[index])
            index += 1
    return prefix, tokens[index:], cwd


def check_git(tokens: list[str], cwd: Path) -> None:
    """Reject commits and push destinations that target a protected branch."""
    prefix, args, cwd = git_invocation(tokens, cwd)
    if not args or args[0] not in ("commit", "push"):
        return
    branch = git_output(prefix, cwd, "symbolic-ref", "--quiet", "--short", "HEAD")
    if args[0] == "commit":
        if branch in PROTECTED:
            raise ValueError("BLOCKED: never commit on main/master; create a feature branch first.")
        return
    targets = [arg.lstrip("+").rsplit(":", 1)[-1] for arg in args[1:]]
    configured = git_output(prefix, cwd, "config", "--get-regexp", r"^remote\..*\.push$")
    configured_targets = [line.split()[-1].rsplit(":", 1)[-1] for line in configured.splitlines()]
    upstream = git_output(prefix, cwd, "config", "--get", f"branch.{branch}.merge")
    push_default = git_output(prefix, cwd, "config", "--get", "push.default")
    implicit_upstream = upstream in PROTECTED and push_default == "upstream"
    if (branch in PROTECTED or PROTECTED.intersection(targets + configured_targets)
            or any(arg in ("--all", "--mirror", ":") or "*" in arg for arg in args[1:])
            or implicit_upstream):
        raise ValueError("BLOCKED: never push directly to main/master; push a feature branch and open a PR.")


def guard(data: HookInput) -> None:
    """Inspect shell segments, including cd, Git -C, and the RTK wrapper."""
    command = data.args.get("command") or data.args.get("cmd", "")
    lexer = shlex.shlex(command, posix=True, punctuation_chars=";&|()\n")
    lexer.whitespace = " \t\r"
    lexer.whitespace_split = True
    tokens = list(lexer)
    cwd = data.cwd
    segment = []
    for token in tokens + [";"]:
        if token and all(char in ";&|()\n" for char in token):
            if segment and segment[0] == "cd" and len(segment) > 1:
                cwd = (cwd / segment[-1]).resolve()
            else:
                while segment and ("=" in segment[0] or segment[0] in ("env", "command", "rtk", "proxy")):
                    segment.pop(0)
                if segment and Path(segment[0]).name == "git":
                    check_git(segment, cwd)
            segment = []
        else:
            segment.append(token)
