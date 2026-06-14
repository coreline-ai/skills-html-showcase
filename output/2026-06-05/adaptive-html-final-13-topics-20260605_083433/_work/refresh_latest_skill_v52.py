#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
SKILL = REPO / "skills" / "adaptive-html-final"
ASSETS = SKILL / "assets"

CORE_ASSETS = [
    "theme.css",
    "components.css",
    "visual-components.css",
    "layouts.css",
    "print.css",
]

INLINE_ASSETS = [
    "theme.css",
    "components.css",
    "visual-components.css",
    "widgets.css",
    "visual-html.css",
    "body-icons.css",
    "editorial-patterns.css",
    "shape-visuals.css",
    "workflow-visuals.css",
    "layouts.css",
    "print.css",
    "theme-dark.css",
]

THEMEBAR = """<fieldset class="ahf-themebar" aria-label="테마 선택">
  <input type="radio" name="ahf-theme" id="ahf-light" checked><label for="ahf-light">라이트</label>
  <input type="radio" name="ahf-theme" id="ahf-white"><label for="ahf-white">화이트</label>
  <input type="radio" name="ahf-theme" id="ahf-dark"><label for="ahf-dark">다크</label>
</fieldset>"""


def read_asset(name: str) -> str:
    return (ASSETS / name).read_text(encoding="utf-8")


def core_hash() -> str:
    core_css = "\n".join(read_asset(name) for name in CORE_ASSETS)
    return hashlib.sha256(core_css.encode("utf-8")).hexdigest()


def combined_style() -> str:
    marker = f"/* adaptive-html-final-core-css-sha256: {core_hash()} */"
    return marker + "\n" + "\n\n".join(read_asset(name).strip("\n") for name in INLINE_ASSETS)


def replace_style(html: str) -> str:
    style = "<style>\n" + combined_style() + "\n</style>"
    updated, count = re.subn(r"<style>[\s\S]*?</style>", lambda _m: style, html, count=1)
    if count != 1:
        raise RuntimeError(f"expected exactly one style block, got {count}")
    return updated


def ensure_themebar(html: str) -> str:
    html = re.sub(
        r"\s*<input type=\"checkbox\" id=\"theme-toggle\"[\s\S]*?</label>\s*",
        "\n",
        html,
        count=1,
    )
    html = re.sub(
        r"\s*<fieldset class=\"ahf-themebar\"[\s\S]*?</fieldset>\s*",
        "\n",
        html,
        count=1,
    )
    updated, count = re.subn(r"(<body[^>]*>\s*)", "\\1" + THEMEBAR + "\n", html, count=1)
    if count != 1:
        raise RuntimeError("body tag not found")
    return updated


def update_visible_version_copy(path: Path, html: str) -> str:
    head, sep, tail = html.partition("</style>")
    if not sep:
        raise RuntimeError(f"style close tag not found in {path}")

    replacements = [
        ("adaptive-html-final v5.1.0", "adaptive-html-final v5.2.0"),
        ("v5.1.0 proper-black dark", "v5.2.0 3-theme"),
        ("v5.1.0 refresh", "v5.2.0 refresh"),
        ("v5.1.0의", "v5.2.0의"),
        ("v5.1.0", "v5.2.0"),
        ("v5.1 proper-black 다크 테마", "v5.2.0 3-테마"),
        ("v5.1 proper-black dark", "v5.2.0 3-theme"),
        ("v5.1 재보강", "v5.2.0 최신 스킬 반영"),
        ("proper-black dark CSS", "v5.2.0 3-테마 CSS"),
        ("proper-black dark", "3-theme"),
        ("proper-black 다크", "3-테마"),
        ("proper-black CTA", "3-테마 CTA"),
    ]
    for old, new in replacements:
        tail = tail.replace(old, new)

    if path.name == "index.html":
        tail = tail.replace(
            "최신 adaptive-html-final v5.2.0 기준으로 13개 신규 주제와 1~5번 모드 상세 보강을 확인할 수 있는 HTML 모음이다.",
            "최신 adaptive-html-final v5.2.0 기준으로 13개 신규 주제 전체에 최신 자산, 3-테마 시스템, vt/wg 템플릿 보강을 적용한 HTML 모음이다.",
        )
        tail = tail.replace("1~5 병렬 에이전트", "1~13 최신 스킬")
        tail = tail.replace(
            "1~5번은 병렬 에이전트 분석을 통합해 generated-row/lens-strip, 3-theme, editorial pattern, a11y-checklist, 권장 vt/wg 배치를 다시 보강했다.",
            "1~13번 전체는 병렬 에이전트 점검과 최신 스킬 자산을 통합해 generated-row/lens-strip, 3-theme, editorial pattern, a11y-checklist, 권장 vt/wg 배치를 다시 보강했다.",
        )

    return head + sep + tail


def rebase_sources() -> None:
    sources = ROOT / "sources"
    assets_dir = sources / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    for name in INLINE_ASSETS:
        shutil.copyfile(ASSETS / name, assets_dir / name)
    shutil.copyfile(SKILL / "manifest.json", sources / "adaptive-html-final-manifest.json")
    (sources / "profile.json").write_text(
        json.dumps({"profile": "auto"}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    asset_hashes = {
        name: hashlib.sha256(read_asset(name).encode("utf-8")).hexdigest()
        for name in INLINE_ASSETS
    }
    integrity = {
        "core_css_sha256": core_hash(),
        "asset_order": CORE_ASSETS,
        "conditional_asset_order": [name for name in INLINE_ASSETS if name not in CORE_ASSETS],
        "asset_sha256": asset_hashes,
        "profile": "auto",
        "skill_version": json.loads((SKILL / "manifest.json").read_text(encoding="utf-8"))["version"],
    }
    (sources / "css-integrity.json").write_text(
        json.dumps(integrity, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    html_paths = [ROOT / "index.html", *sorted((ROOT / "pages").glob("*.html"))]
    for path in html_paths:
        html = path.read_text(encoding="utf-8")
        html = replace_style(html)
        html = ensure_themebar(html)
        html = update_visible_version_copy(path, html)
        path.write_text(html, encoding="utf-8")
    rebase_sources()
    print(f"refreshed {len(html_paths)} HTML files with adaptive-html-final v5.2.0 assets")
    print(f"core_css_sha256 {core_hash()}")
    print(f"theme-dark.css sha256 {hashlib.sha256(read_asset('theme-dark.css').encode('utf-8')).hexdigest()}")


if __name__ == "__main__":
    main()
