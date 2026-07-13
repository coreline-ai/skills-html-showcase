#!/usr/bin/env python3
"""Build a tiny static manual index from a manual manifest.

Supports:
- legacy-static manifests with lesson.steps_file
- phase-gated pre-capture manifests with lesson.file

For phase-gated/capture-blocked manifests, output is always a provisional preview with
large NOT FINAL banners and no requirement for blocked media assets.

Usage: python build-static-manual.py manual.yaml dist/
"""
from __future__ import annotations

import html
import shutil
import sys
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except Exception:
    yaml = None

BLOCKED_MEDIA = {
    "blocked_until_capture_env_ready",
    "blocked_until_capture_env_ready_and_safe_fixture",
    "blocked_until_safe_fixture",
    "not_required",
}


def md_to_html(text: str) -> str:
    out = []
    in_ul = False
    for line in text.splitlines():
        if line.startswith("# "):
            if in_ul:
                out.append("</ul>"); in_ul = False
            out.append(f"<h1>{html.escape(line[2:])}</h1>")
        elif line.startswith("## "):
            if in_ul:
                out.append("</ul>"); in_ul = False
            out.append(f"<h2>{html.escape(line[3:])}</h2>")
        elif line.startswith("### "):
            if in_ul:
                out.append("</ul>"); in_ul = False
            out.append(f"<h3>{html.escape(line[4:])}</h3>")
        elif line.startswith("- "):
            if not in_ul:
                out.append("<ul>"); in_ul = True
            out.append(f"<li>{html.escape(line[2:])}</li>")
        elif line.strip():
            if in_ul:
                out.append("</ul>"); in_ul = False
            out.append(f"<p>{html.escape(line)}</p>")
        else:
            if in_ul:
                out.append("</ul>"); in_ul = False
            out.append("")
    if in_ul:
        out.append("</ul>")
    return "\n".join(out)


def load_manifest(path: Path) -> dict[str, Any]:
    if yaml is None:
        raise SystemExit("PyYAML is required: python -m pip install pyyaml")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit("Manifest must be a YAML object")
    return data


def is_phase_gated(manual: dict[str, Any], lessons: list[Any]) -> bool:
    return bool(manual.get("language_policy") or any(isinstance(l, dict) and l.get("file") for l in lessons))


def preflight(root: Path, data: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]], bool, list[str]]:
    manual = data.get("manual") or {}
    lessons = data.get("lessons") or []
    if not isinstance(manual, dict) or not isinstance(lessons, list) or not lessons:
        raise SystemExit("Invalid manifest: expected manual object and non-empty lessons list")
    phase = is_phase_gated(manual, lessons)
    problems: list[str] = []
    for lesson in lessons:
        if not isinstance(lesson, dict):
            problems.append("lesson entry must be object")
            continue
        lid = lesson.get("id", "<missing-id>")
        source_field = "file" if phase else "steps_file"
        rel = lesson.get(source_field)
        if not rel:
            problems.append(f"lesson {lid}: {source_field} is required")
            continue
        path = (root / str(rel)).resolve()
        try:
            path.relative_to(root.resolve())
        except ValueError:
            problems.append(f"lesson {lid}: path escapes package root: {rel}")
        if not path.exists():
            problems.append(f"lesson {lid}: missing file {rel}")
    if problems:
        print("FAIL static build preflight")
        for p in problems:
            print(f"- {p}")
        raise SystemExit(1)
    return manual, lessons, phase, problems


def badge(value: Any) -> str:
    return html.escape(str(value)).replace("_", " ")


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__.strip())
        return 2
    manifest_path = Path(sys.argv[1]).resolve()
    root = manifest_path.parent
    out_dir = Path(sys.argv[2]).resolve()
    data = load_manifest(manifest_path)
    manual, lessons, phase, _ = preflight(root, data)

    if out_dir.exists():
        shutil.rmtree(out_dir)
    lessons_out = out_dir / "lessons"
    lessons_out.mkdir(parents=True, exist_ok=True)

    lang = str(manual.get("language") or manual.get("language_policy") or "ko")
    title = str(manual.get("title") or "Manual")
    provisional = phase or any(str(l.get("status", "")).startswith(("provisional", "draft")) for l in lessons)
    banner = ""
    if provisional:
        banner = '<div class="banner">PROVISIONAL / CAPTURE-BLOCKED / NOT FINAL — live UI and media are not verified.</div>'

    links = []
    for lesson in lessons:
        lesson_id = str(lesson["id"])
        lesson_title = str(lesson.get("title") or lesson_id)
        rel = lesson.get("file") if phase else lesson.get("steps_file")
        steps_path = root / str(rel)
        body = md_to_html(steps_path.read_text(encoding="utf-8"))
        media = lesson.get("media", {}) or {}
        media_status = media.get("status", "unknown") if isinstance(media, dict) else "invalid"
        meta = f"""
<section class="meta">
<span>Status: {badge(lesson.get('status', 'unknown'))}</span>
<span>UI capture: {badge(lesson.get('ui_capture_required', 'unknown'))}</span>
<span>Risky action: {badge(lesson.get('risky_action', 'unknown'))}</span>
<span>Domain review: {badge(lesson.get('domain_expert_required', 'unknown'))}</span>
<span>Media: {badge(media_status)}</span>
</section>
"""
        media_html = []
        if isinstance(media, dict) and str(media_status) not in BLOCKED_MEDIA:
            for img in media.get("screenshots", []) or []:
                media_html.append(f'<figure><img src="../{html.escape(str(img))}" alt="{html.escape(lesson_title)} screenshot"></figure>')
            for video in media.get("videos", []) or []:
                media_html.append(f'<video controls src="../{html.escape(str(video))}"></video>')
        elif phase:
            media_html.append(f'<p class="blocked">Media not embedded: {badge(media_status)}</p>')
        page = f"""<!doctype html>
<html lang="{html.escape(lang)}">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{html.escape(lesson_title)}</title><style>body{{font-family:system-ui,sans-serif;max-width:960px;margin:40px auto;padding:0 20px;line-height:1.65}}.banner{{background:#7c2d12;color:white;padding:14px 18px;border-radius:10px;font-weight:700;margin:0 0 20px}}.meta span{{display:inline-block;background:#eef2ff;border:1px solid #c7d2fe;border-radius:999px;padding:4px 10px;margin:3px;font-size:13px}}.blocked{{background:#fff7ed;border:1px solid #fdba74;padding:10px;border-radius:8px}}img,video{{max-width:100%;border:1px solid #ddd;border-radius:12px;background:#111}}</style></head>
<body>{banner}<a href="../index.html">← Index</a><h1>{html.escape(lesson_title)}</h1>{meta}{body}{''.join(media_html)}</body></html>"""
        rel_page = f"lessons/{lesson_id}.html"
        (out_dir / rel_page).write_text(page, encoding="utf-8")
        links.append(f'<li><a href="{html.escape(rel_page)}">{html.escape(lesson_id)} — {html.escape(lesson_title)}</a> <small>{badge(lesson.get("status", ""))}</small></li>')

    for dirname in ["assets", "review"]:
        src = root / dirname
        dst = out_dir / dirname
        if src.exists():
            shutil.copytree(src, dst)

    audience = manual.get("audience") or manual.get("primary_audience") or ""
    index = f"""<!doctype html>
<html lang="{html.escape(lang)}">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{html.escape(title)}</title><style>body{{font-family:system-ui,sans-serif;max-width:960px;margin:40px auto;padding:0 20px;line-height:1.65}}.banner{{background:#7c2d12;color:white;padding:14px 18px;border-radius:10px;font-weight:700;margin:0 0 20px}}</style></head>
<body>{banner}<h1>{html.escape(title)}</h1><p>Audience: {html.escape(str(audience))}</p><p>Source: {html.escape(str(manual.get('target_version') or manual.get('version_basis') or 'TBD'))}</p><ol>{''.join(links)}</ol></body></html>"""
    (out_dir / "index.html").write_text(index, encoding="utf-8")
    print(f"Built {out_dir / 'index.html'}")
    if provisional:
        print("Mode: provisional/capture-blocked preview")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
