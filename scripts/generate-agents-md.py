#!/usr/bin/env python3
"""Generate AGENTS.md for Codex and OpenCode from CLAUDE.md and rules/*.md.

Strips YAML frontmatter (Codex/OpenCode don't parse it), flattens the rules
into one document, and annotates each rule block with its intended path scope
so the glob information in Claude frontmatter isn't lost.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def strip_frontmatter(text: str) -> str:
    """Strip only a complete frontmatter block bounded by delimiter lines."""
    match = re.match(r"\A---\r?\n.*?\r?\n---(?:\r?\n|$)", text, re.DOTALL)
    if match:
        return text[match.end():].lstrip("\r\n")
    return text


def scope_from_frontmatter(text: str) -> str | None:
    """Extract the path scopes used by this repository's rule templates."""
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return None
    paths = re.findall(r'-\s+"([^"]+)"', m.group(1))
    return ", ".join(paths) if paths else None


def main() -> None:
    """Regenerate the standalone instruction bundle from its source files."""
    parts = []

    claude_md = ROOT / "CLAUDE.md"
    parts.append(strip_frontmatter(claude_md.read_text()).strip())

    for rule in sorted((ROOT / "rules").glob("*.md")):
        raw = rule.read_text()
        scope = scope_from_frontmatter(raw)
        body = strip_frontmatter(raw).strip()
        block = f"## Rule: {rule.stem}\n"
        if scope:
            block += f"_Applies to: {scope}_\n"
        parts.append(block + "\n" + body)

    # Keep workflows available even when only AGENTS.md is installed.
    for skill in sorted((ROOT / "skills").glob("*/SKILL.md")):
        parts.append(strip_frontmatter(skill.read_text()).strip())

    out = "\n\n".join(parts) + "\n"
    (ROOT / "AGENTS.md").write_text(out)
    print(f"wrote AGENTS.md ({len(out)} chars)")


if __name__ == "__main__":
    sys.exit(main())
