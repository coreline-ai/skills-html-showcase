#!/usr/bin/env python3
"""Build an evidence map Markdown table from a phase-gated manual manifest.

Usage:
  python build-evidence-map.py manifest.yml [output.md]

The script preserves explicit evidence_tier objects when present and otherwise uses
path-based heuristics. Live UI remains the final source of truth for user-facing steps.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except Exception:
    yaml = None


def classify_source(src: str) -> str:
    s = src.lower()
    if src == "TBD" or "ui_capture_required" in s:
        return "unverified"
    if "owner-decision" in s or "owner-decisions" in s:
        return "owner_decision"
    if "verification-log" in s or "worklog" in s:
        return "project_worklog"
    if "workspace_sidebar" in s or "workspace" in s:
        return "workspace_config"
    if "/doctype/" in s or "/report/" in s or s.endswith(".py") or s.endswith(".json"):
        return "doctype_or_source_config"
    if s.startswith("http://") or s.startswith("https://"):
        return "official_docs"
    return "unverified_or_repo_path"


def normalize_evidence(items: Any) -> tuple[list[str], list[str]]:
    sources: list[str] = []
    tiers: list[str] = []
    if items is None:
        return ["TBD"], ["unverified"]
    if not isinstance(items, list):
        items = [items]
    for item in items:
        if isinstance(item, dict):
            src = str(item.get("source") or item.get("path") or item.get("url") or "TBD")
            tier = str(item.get("evidence_tier") or classify_source(src))
        else:
            src = str(item)
            tier = classify_source(src)
        sources.append(src)
        tiers.append(tier)
    return sources or ["TBD"], sorted(set(tiers or ["unverified"]))


def live_ui_need(lesson: dict[str, Any]) -> str:
    needs = []
    if lesson.get("ui_capture_required"):
        needs.append("actual target-version menu path, labels, list/form/report layout")
    if lesson.get("risky_action"):
        needs.append("safe demo fixture before any state change")
    if lesson.get("domain_expert_required"):
        needs.append("domain-risk wording remains conceptual or gets expert review")
    if not needs:
        needs.append("content QA within full package context")
    return "; ".join(needs)


def esc_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", "<br>")


def main() -> int:
    if yaml is None:
        raise SystemExit("PyYAML is required: python -m pip install pyyaml")
    if len(sys.argv) not in (2, 3):
        print(__doc__.strip())
        return 2
    manifest_path = Path(sys.argv[1])
    data = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    lessons = data.get("lessons") or []
    lines = [
        "# Evidence Map",
        "",
        "Status: generated pre-capture evidence map. Live UI remains the final source of truth.",
        "",
        "| Lesson | Source evidence | Evidence tier | Live UI must verify |",
        "|---|---|---|---|",
    ]
    for lesson in lessons:
        if not isinstance(lesson, dict):
            continue
        sources, tiers = normalize_evidence(lesson.get("source_evidence"))
        lines.append(
            f"| {esc_cell(str(lesson.get('id', '')))} | "
            f"{esc_cell('<br>'.join(sources))} | "
            f"{esc_cell(', '.join(tiers))} | "
            f"{esc_cell(live_ui_need(lesson))} |"
        )
    output = "\n".join(lines) + "\n"
    if len(sys.argv) == 3:
        Path(sys.argv[2]).write_text(output, encoding="utf-8")
        print(f"Wrote {sys.argv[2]}")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
