#!/usr/bin/env python3
"""Verify a provisional static manual preview package.

Usage:
  python verify-preview-package.py preview-static V1-00 V1-18

Checks:
- index.html exists
- lesson HTML files exist from first id through last id
- every HTML includes the provisional/capture-blocked banner
- no img/video/audio/source tags are embedded
- no obvious final/completion language appears
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

BANNER = "PROVISIONAL / CAPTURE-BLOCKED / NOT FINAL"
MEDIA_TAG_RE = re.compile(r"<(?:img|video|audio|source)\b", re.I)
FINAL_RE = re.compile(r"final manual|manual complete|completion claim|완성(?:되었습니다|됨)|최종 매뉴얼", re.I)
ID_RE = re.compile(r"^(.*?)(\d+)$")


def expand_ids(start: str, end: str) -> list[str]:
    sm = ID_RE.match(start)
    em = ID_RE.match(end)
    if not sm or not em or sm.group(1) != em.group(1):
        raise SystemExit("Lesson ids must share a prefix and end in numbers, e.g. V1-00 V1-18")
    prefix = sm.group(1)
    width = max(len(sm.group(2)), len(em.group(2)))
    a, b = int(sm.group(2)), int(em.group(2))
    if a > b:
        raise SystemExit("Start id must be <= end id")
    return [f"{prefix}{i:0{width}d}" for i in range(a, b + 1)]


def main() -> int:
    if len(sys.argv) != 4:
        print(__doc__.strip())
        return 2
    root = Path(sys.argv[1])
    ids = expand_ids(sys.argv[2], sys.argv[3])
    problems: list[str] = []
    files = [root / "index.html"] + [root / "lessons" / f"{lesson_id}.html" for lesson_id in ids]
    for path in files:
        if not path.exists():
            problems.append(f"missing: {path}")
            continue
        if path.stat().st_size == 0:
            problems.append(f"empty: {path}")
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if BANNER not in text:
            problems.append(f"missing banner: {path}")
        if MEDIA_TAG_RE.search(text):
            problems.append(f"embedded media tag: {path}")
        if FINAL_RE.search(text):
            problems.append(f"final/completion language: {path}")
    if problems:
        print("FAIL preview package verification")
        for p in problems:
            print(f"- {p}")
        return 1
    print("PASS preview package verification")
    print(f"html_count {len(files)}")
    print(f"lesson_count {len(ids)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
