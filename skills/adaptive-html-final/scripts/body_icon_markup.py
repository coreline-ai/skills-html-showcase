#!/usr/bin/env python3
"""Print canonical adaptive-html-final body-icon markup from assets/body-icons.json.

Usage:
  python3 skills/adaptive-html-final/scripts/body_icon_markup.py idea
  python3 skills/adaptive-html-final/scripts/body_icon_markup.py warning --class body-icon--sm
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_icons(skill_dir: Path) -> dict[str, str]:
    icons_path = skill_dir / "assets" / "body-icons.json"
    icons = json.loads(icons_path.read_text(encoding="utf-8"))
    return {item["id"]: item["svg"] for item in icons}


def main() -> int:
    ap = argparse.ArgumentParser(description="Emit canonical .body-icon markup from body-icons.json")
    ap.add_argument("icon_id", help="body-icons.json id, e.g. idea/source/check/warning")
    ap.add_argument("--skill-dir", type=Path, default=Path(__file__).resolve().parent.parent)
    ap.add_argument("--class", dest="extra_class", default="", help="optional extra class such as body-icon--sm or body-icon--plain")
    ns = ap.parse_args()

    icons = load_icons(ns.skill_dir)
    if ns.icon_id not in icons:
        valid = ", ".join(sorted(icons))
        raise SystemExit(f"unknown body icon id: {ns.icon_id}\nvalid ids: {valid}")
    classes = "body-icon" + ((" " + ns.extra_class.strip()) if ns.extra_class.strip() else "")
    print(f'<span class="{classes}" aria-hidden="true">{icons[ns.icon_id]}</span>')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
