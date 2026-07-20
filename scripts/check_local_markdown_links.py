import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
SCAN_ROOTS = [ROOT / "README.md", ROOT / "docs" / "tutorial", ROOT / "docs" / "security"]

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def markdown_files():
    for root in SCAN_ROOTS:
        if root.is_file():
            yield root
        elif root.is_dir():
            yield from root.rglob("*.md")


failures = []
for markdown_path in markdown_files():
    content = markdown_path.read_text(encoding="utf-8")
    for match in MARKDOWN_LINK.finditer(content):
        raw_target = match.group(1).strip().strip("<>")
        target = raw_target.split("#", 1)[0]
        if not target or re.match(r"^[a-z][a-z0-9+.-]*:", target, re.IGNORECASE):
            continue
        resolved = (markdown_path.parent / unquote(target)).resolve()
        if not resolved.exists():
            line = content.count("\n", 0, match.start()) + 1
            failures.append(f"{markdown_path.relative_to(ROOT)}:{line} -> {raw_target}")

if failures:
    raise SystemExit("Broken local Markdown links:\n" + "\n".join(failures))

print("OK: README、tutorial 與 security 文件的本機連結都存在")
