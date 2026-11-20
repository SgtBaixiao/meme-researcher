#!/usr/bin/env python3
"""Check local file targets in the current Markdown entry points."""
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
CURRENT = ["README.md", "SKILL.md", "references/README.md",
           "references/runtime.md", "references/evidence-contract.md"]

def check_file(file, root):
    problems = []
    for target in re.findall(r"\[[^\]]*\]\(([^\s)]+)\)", file.read_text(encoding="utf8")):
        parsed = urlsplit(target)
        if parsed.scheme or not parsed.path:
            continue
        destination = (file.parent / unquote(parsed.path)).resolve()
        if not destination.is_relative_to(root.resolve()) or not destination.exists():
            problems.append(f"{file.name}: missing or outside-root target {target}")
    return problems

def main():
    problems = [problem for name in CURRENT for problem in check_file(ROOT / name, ROOT)]
    print(json.dumps({"ok": not problems, "problems": problems, "scope": "current Markdown local file targets; remote URLs and anchors are not probed"}, indent=2))
    return 1 if problems else 0

if __name__ == "__main__":
    raise SystemExit(main())
