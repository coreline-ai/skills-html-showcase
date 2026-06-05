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

THEME_TOGGLE = """<input type="checkbox" id="theme-toggle" aria-label="밝은 테마와 다크 테마 전환">
<label class="theme-switch" for="theme-toggle" title="밝은 테마와 다크 테마 전환" aria-label="밝은 테마와 다크 테마 전환">
  <svg class="ts-sun" width="22" height="22" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
    <circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="2"></circle>
    <path d="M12 2v3M12 19v3M4.22 4.22l2.12 2.12M17.66 17.66l2.12 2.12M2 12h3M19 12h3M4.22 19.78l2.12-2.12M17.66 6.34l2.12-2.12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"></path>
  </svg>
  <svg class="ts-moon" width="22" height="22" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
    <path d="M21 14.2A7.5 7.5 0 0 1 9.8 3a8.5 8.5 0 1 0 11.2 11.2Z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"></path>
  </svg>
</label>"""


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
    return re.sub(r"<style>[\s\S]*?</style>", lambda _m: style, html, count=1)


def add_toggle(html: str) -> str:
    if 'id="theme-toggle"' in re.sub(r"<style>[\s\S]*?</style>", "", html):
        return html
    return html.replace("<body>\n", "<body>\n" + THEME_TOGGLE + "\n", 1)


def rebase_sources() -> None:
    sources = ROOT / "sources"
    assets_dir = sources / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    for name in INLINE_ASSETS:
        shutil.copyfile(ASSETS / name, assets_dir / name)
    shutil.copyfile(SKILL / "manifest.json", sources / "adaptive-html-final-manifest.json")
    (sources / "profile.json").write_text(json.dumps({"profile": "auto"}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    asset_hashes = {name: hashlib.sha256(read_asset(name).encode("utf-8")).hexdigest() for name in INLINE_ASSETS}
    integrity = {
        "core_css_sha256": core_hash(),
        "asset_order": CORE_ASSETS,
        "conditional_asset_order": [name for name in INLINE_ASSETS if name not in CORE_ASSETS],
        "asset_sha256": asset_hashes,
        "profile": "auto",
        "skill_version": json.loads((SKILL / "manifest.json").read_text(encoding="utf-8"))["version"],
    }
    (sources / "css-integrity.json").write_text(json.dumps(integrity, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    html_paths = [ROOT / "index.html", *sorted((ROOT / "pages").glob("*.html"))]
    for path in html_paths:
        html = path.read_text(encoding="utf-8")
        html = add_toggle(replace_style(html))
        path.write_text(html, encoding="utf-8")
    rebase_sources()
    print(f"Added theme toggle to {len(html_paths)} HTML files")
    print(f"theme-dark.css sha256 {hashlib.sha256(read_asset('theme-dark.css').encode('utf-8')).hexdigest()}")


if __name__ == "__main__":
    main()
