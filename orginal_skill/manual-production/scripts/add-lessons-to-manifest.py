#!/usr/bin/env python3
"""Insert lesson records into a manual manifest while preserving lesson-id order.

Usage:
  python add-lessons-to-manifest.py manifest.yml V1-02:path/to/lesson.md "V1-03:Another Title:path/to/file.md"

The argument format is intentionally simple:
- V1-02:path/to/file.md -> title is inferred from filename
- V1-03:Title:path/to/file.md -> explicit title

Records are conservative capture-blocked defaults and should be edited with source evidence.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except Exception:
    yaml = None

ID_RE = re.compile(r"^([A-Za-z]+)(\d+)-(\d+)$")


def sort_key(item: dict[str, Any]) -> tuple[str, int, int, str]:
    mid = ID_RE.match(str(item.get("id", "")))
    if mid:
        return (mid.group(1), int(mid.group(2)), int(mid.group(3)), str(item.get("id")))
    return ("ZZZ", 999, 999, str(item.get("id")))


def infer_title(path: str) -> str:
    return Path(path).stem.replace('-', ' ').title()


def parse_arg(arg: str) -> tuple[str, str, str]:
    parts = arg.split(':')
    if len(parts) == 2:
        lid, path = parts
        return lid, infer_title(path), path
    if len(parts) >= 3:
        lid, title = parts[0], parts[1]
        path = ':'.join(parts[2:])
        return lid, title, path
    raise ValueError(f"Bad lesson arg: {arg}")


def main() -> int:
    if yaml is None:
        raise SystemExit("PyYAML is required: python -m pip install pyyaml")
    if len(sys.argv) < 3:
        print(__doc__.strip())
        return 2
    manifest = Path(sys.argv[1])
    data = yaml.safe_load(manifest.read_text(encoding='utf-8'))
    lessons = data.setdefault('lessons', [])
    by_id = {l.get('id'): l for l in lessons}
    for raw in sys.argv[2:]:
        lid, title, file_path = parse_arg(raw)
        if lid in by_id:
            print(f"skip existing {lid}")
            continue
        rec = {
            'id': lid,
            'title': title,
            'file': file_path,
            'status': 'provisional_conceptual_draft',
            'source_evidence': [{'evidence_tier': 'unverified', 'source': 'TBD', 'status': 'unverified'}],
            'ui_capture_required': True,
            'risky_action': False,
            'domain_expert_required': False,
            'media': {'required': True, 'status': 'blocked_until_capture_env_ready'},
            'qa': {'content_status': 'pending', 'technical_status': 'not_started'},
        }
        lessons.append(rec)
        print(f"add {lid}")
    lessons.sort(key=sort_key)
    manifest.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding='utf-8')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
