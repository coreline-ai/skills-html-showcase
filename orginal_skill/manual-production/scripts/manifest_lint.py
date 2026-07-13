#!/usr/bin/env python3
"""Lint a manifest-based manual plan.

Usage:
  python manifest_lint.py manual.yaml

This is generic and conservative. It prevents accidental promotion from outline to production without evidence, capture state, risk handling, and QA state.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except Exception:
    yaml = None

PRODUCTION_STATUSES = {"ready_for_handoff", "content_qa_passed", "technical_qa_passed", "media_captured_pending_qa"}


def as_list(v: Any) -> list[Any]:
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def main() -> int:
    if yaml is None:
        raise SystemExit("PyYAML is required: python -m pip install pyyaml")
    if len(sys.argv) != 2:
        print(__doc__.strip())
        return 2
    path = Path(sys.argv[1])
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    problems: list[str] = []
    lessons = data.get("lessons") or []
    if not lessons:
        problems.append("manifest has no lessons")
    for idx, lesson in enumerate(lessons):
        lid = lesson.get("id") or f"lessons[{idx}]"
        for key in ["id", "title", "status", "source_evidence"]:
            if not lesson.get(key):
                problems.append(f"{lid}: missing {key}")
        evidence = as_list(lesson.get("source_evidence"))
        if not evidence:
            problems.append(f"{lid}: source_evidence must be non-empty")
        ui_capture_required = lesson.get("ui_capture_required")
        if ui_capture_required is None:
            problems.append(f"{lid}: ui_capture_required must be true/false")
        status = str(lesson.get("status") or "")
        if status in PRODUCTION_STATUSES and ui_capture_required and not lesson.get("ui_capture_ready"):
            problems.append(f"{lid}: production-like status without ui_capture_ready")
        if lesson.get("risky_action"):
            if lesson.get("safe_fixture_required") is None:
                problems.append(f"{lid}: risky_action requires safe_fixture_required")
            if lesson.get("safe_fixture_available") is None:
                problems.append(f"{lid}: risky_action requires safe_fixture_available")
            if not lesson.get("risk_handling"):
                problems.append(f"{lid}: risky_action requires risk_handling")
        qa = lesson.get("qa") or {}
        if not isinstance(qa, dict):
            problems.append(f"{lid}: qa must be an object")
        else:
            if not qa.get("content_status"):
                problems.append(f"{lid}: qa.content_status missing")
            if not qa.get("technical_status"):
                problems.append(f"{lid}: qa.technical_status missing")
    if problems:
        print("FAIL manifest lint")
        for p in problems:
            print(f"- {p}")
        return 1
    print("PASS manifest lint")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
