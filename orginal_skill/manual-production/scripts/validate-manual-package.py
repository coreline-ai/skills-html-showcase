#!/usr/bin/env python3
"""Validate a manifest-based manual package.

Usage:
  python validate-manual-package.py path/to/manual.yaml [package_root]

Supports two schema modes:
- legacy-static: final/static package manifests with steps_file/review_card.
- phase-gated-pre-capture: provisional manuals that use lesson.file, source_evidence,
  risk fields, media.status, and QA placeholders.

Checks are intentionally generic:
- required manifest keys
- referenced lesson/media/review files exist
- forbidden terms in lesson/review/html text files
- risky-action safe-fixture fields
- blocked media is not required to exist before capture
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

TEXT_EXTS = {".md", ".html", ".htm", ".txt"}
MEDIA_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".mp4", ".mov", ".webm"}
BLOCKED_MEDIA = {
    "blocked_until_capture_env_ready",
    "blocked_until_capture_env_ready_and_safe_fixture",
    "blocked_until_safe_fixture",
    "not_required",
}


def load_yaml(path: Path) -> dict[str, Any]:
    if yaml is None:
        raise SystemExit("PyYAML is required: python -m pip install pyyaml")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit(f"Manifest is not a YAML object: {path}")
    return data


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def check_path(root: Path, rel: str, problems: list[str], min_bytes: int = 1) -> Path:
    path = (root / rel).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError:
        problems.append(f"Path escapes package root: {rel}")
        return path
    if not path.exists():
        problems.append(f"Missing file: {rel}")
    elif path.is_file() and path.stat().st_size < min_bytes:
        problems.append(f"Empty/tiny file: {rel}")
    return path


def scan_forbidden(path: Path, terms: list[str], problems: list[str]) -> None:
    if not path.exists() or path.suffix.lower() not in TEXT_EXTS:
        return
    text = path.read_text(encoding="utf-8", errors="ignore")
    for term in terms:
        if re.search(rf"\b{re.escape(term)}\b", text, flags=re.IGNORECASE):
            problems.append(f"Forbidden term '{term}' in {path}")


def detect_mode(manual: dict[str, Any], lessons: list[Any]) -> str:
    if manual.get("language_policy") or any(isinstance(l, dict) and l.get("file") for l in lessons):
        return "phase-gated-pre-capture"
    return "legacy-static"


def validate_manual_common(manual: dict[str, Any], problems: list[str]) -> None:
    for key in ["id", "title"]:
        if not manual.get(key):
            problems.append(f"manual.{key} is required")


def validate_phase_gated(root: Path, manual: dict[str, Any], lessons: list[Any], problems: list[str], text_paths: list[Path]) -> None:
    validate_manual_common(manual, problems)
    if not (manual.get("language") or manual.get("language_policy")):
        problems.append("manual.language or manual.language_policy is required")
    if not (manual.get("audience") or manual.get("primary_audience")):
        problems.append("manual.audience or manual.primary_audience is required")
    if not (manual.get("version_basis") or manual.get("target_version") or manual.get("version_source")):
        problems.append("manual.version_basis or manual.target_version/version_source is required")

    for i, lesson in enumerate(lessons):
        if not isinstance(lesson, dict):
            problems.append(f"lessons[{i}] must be an object")
            continue
        lesson_id = lesson.get("id") or f"index-{i}"
        for key in ["id", "title", "status", "source_evidence", "ui_capture_required", "risky_action", "domain_expert_required", "media", "qa"]:
            if key not in lesson or lesson.get(key) in (None, ""):
                problems.append(f"lesson {lesson_id}: {key} is required")
        if lesson.get("file"):
            text_paths.append(check_path(root, str(lesson["file"]), problems))
        else:
            problems.append(f"lesson {lesson_id}: file is required in phase-gated mode")
        media = lesson.get("media") or {}
        if not isinstance(media, dict):
            problems.append(f"lesson {lesson_id}: media must be an object")
            media = {}
        if not media.get("status"):
            problems.append(f"lesson {lesson_id}: media.status is required")
        qa = lesson.get("qa") or {}
        if not isinstance(qa, dict):
            problems.append(f"lesson {lesson_id}: qa must be an object")
            qa = {}
        for key in ["content_status", "technical_status"]:
            if not qa.get(key):
                problems.append(f"lesson {lesson_id}: qa.{key} is required")
        if lesson.get("risky_action") is True:
            for key in ["safe_fixture_required", "safe_fixture_available", "risk_handling"]:
                if key not in lesson:
                    problems.append(f"lesson {lesson_id}: risky_action requires {key}")
        # Only require media files when media is not blocked/not_required.
        status = str(media.get("status") or "")
        if status not in BLOCKED_MEDIA:
            for rel in as_list(media.get("screenshots")) + as_list(media.get("videos")):
                path = check_path(root, str(rel), problems, min_bytes=128)
                if path.suffix.lower() not in MEDIA_EXTS:
                    problems.append(f"Unexpected media extension: {rel}")


def validate_legacy(root: Path, manual: dict[str, Any], lessons: list[Any], problems: list[str], text_paths: list[Path]) -> None:
    validate_manual_common(manual, problems)
    for key in ["language", "audience", "version_basis"]:
        if not manual.get(key):
            problems.append(f"manual.{key} is required")
    for i, lesson in enumerate(lessons):
        if not isinstance(lesson, dict):
            problems.append(f"lessons[{i}] must be an object")
            continue
        lesson_id = lesson.get("id") or f"index-{i}"
        for key in ["id", "title", "audience", "goal"]:
            if not lesson.get(key):
                problems.append(f"lesson {lesson_id}: {key} is required")
        for field in ["steps_file", "review_card"]:
            if lesson.get(field):
                path = check_path(root, str(lesson[field]), problems)
                text_paths.append(path)
            else:
                problems.append(f"lesson {lesson_id}: {field} is required")
        media = lesson.get("media") or {}
        if isinstance(media, dict):
            for rel in as_list(media.get("screenshots")) + as_list(media.get("videos")):
                path = check_path(root, str(rel), problems, min_bytes=128)
                if path.suffix.lower() not in MEDIA_EXTS:
                    problems.append(f"Unexpected media extension: {rel}")
        else:
            problems.append(f"lesson {lesson_id}: media must be an object")


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__.strip())
        return 2
    manifest_path = Path(sys.argv[1]).resolve()
    root = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else manifest_path.parent.resolve()
    manifest = load_yaml(manifest_path)
    problems: list[str] = []

    manual = manifest.get("manual") or {}
    lessons = manifest.get("lessons") or []
    if not isinstance(manual, dict):
        problems.append("manual must be an object")
        manual = {}
    if not isinstance(lessons, list) or not lessons:
        problems.append("lessons must be a non-empty list")
        lessons = []

    mode = detect_mode(manual, lessons)
    forbidden_terms = [str(x) for x in as_list(manual.get("forbidden_terms"))]
    text_paths: list[Path] = []

    if mode == "phase-gated-pre-capture":
        validate_phase_gated(root, manual, lessons, problems, text_paths)
    else:
        validate_legacy(root, manual, lessons, problems, text_paths)

    for path in text_paths:
        scan_forbidden(path, forbidden_terms, problems)

    if problems:
        print(f"FAIL manual package validation ({mode})")
        for p in problems:
            print(f"- {p}")
        return 1
    print(f"PASS manual package validation ({mode})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
