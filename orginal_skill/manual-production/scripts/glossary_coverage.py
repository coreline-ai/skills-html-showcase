#!/usr/bin/env python3
"""Check whether visible English UI labels used in lessons appear in glossary.

Usage:
  python glossary_coverage.py glossary.md tracks/**/*.md

Heuristic: extracts parenthesized English-ish labels like 품목(Item), 판매 주문(Sales Order), then checks the label text appears in the glossary file.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

LABEL_RE = re.compile(r"\(([A-Z][A-Za-z0-9 /&_-]{1,60})\)")
IGNORE = {"TBD", "TODO", "API", "URL", "HTML", "PDF", "QA", "UI"}


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__.strip())
        return 2
    glossary = Path(sys.argv[1]).read_text(encoding='utf-8').lower()
    missing: dict[str, list[str]] = {}
    for raw in sys.argv[2:]:
        path = Path(raw)
        if not path.exists() or path.is_dir():
            continue
        text = path.read_text(encoding='utf-8')
        for label in sorted(set(LABEL_RE.findall(text))):
            if label in IGNORE:
                continue
            # Skip obvious prose fragments, keep common UI labels.
            if len(label.split()) > 5:
                continue
            if label.lower() not in glossary:
                missing.setdefault(label, []).append(str(path))
    if missing:
        print("FAIL glossary coverage")
        for label, paths in sorted(missing.items()):
            print(f"- {label}: {', '.join(paths[:5])}")
        return 1
    print("PASS glossary coverage")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
