"""Review and format only the files identified by an edit event."""

from pathlib import Path
import re
import subprocess

from hook_input import HookInput

CODE_SUFFIXES = {".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".py", ".sh", ".go", ".rs", ".css", ".html"}
FORMAT_SUFFIXES = {".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".json", ".jsonc"}
VIOLATION = re.compile(
    r"[=*-]{4,}|^(?:const |let |var |def |return |if \(|for \(|import |from |function |class )"
    r"|(?:added|removed|updated|changed|fixed).*(?:20\d{2}|by @)", re.IGNORECASE
)


def comments(data: HookInput) -> None:
    """Report mechanical comment violations in saved source files."""
    violations = []
    for file in data.files():
        if not file.is_file() or file.suffix not in CODE_SUFFIXES:
            continue
        markers = ("#",) if file.suffix in {".py", ".sh"} else ("//", "/*", "*", "<!--")
        for number, line in enumerate(file.read_text(encoding="utf-8").splitlines(), 1):
            line = line.strip()
            if line.startswith("#!") or not line.startswith(markers):
                continue
            body = re.sub(r"^(?://|/\*|\*|#|<!--)\s*", "", line)
            if VIOLATION.search(body):
                violations.append(f"{file}:{number}: {line}")
    if violations:
        raise ValueError("COMMENT RULE VIOLATION: remove dead code/decorations; explain why.\n" + "\n".join(violations))


def format_files(data: HookInput) -> None:
    """Use the nearest installed Biome without downloading packages."""
    errors = []
    for file in data.files():
        if not file.is_file() or file.suffix not in FORMAT_SUFFIXES:
            continue
        for directory in file.parents:
            binary = directory / "node_modules/.bin/biome"
            if not binary.is_file():
                continue
            result = subprocess.run([str(binary), "check", "--write", str(file)],
                                    cwd=directory, capture_output=True, text=True, timeout=60)
            if result.returncode:
                errors.append(result.stdout + result.stderr)
            break
    if errors:
        raise ValueError("Biome failed:\n" + "\n".join(errors))
