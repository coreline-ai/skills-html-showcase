#!/usr/bin/env python3
"""Re-inline a single-style-block demo output from current skill assets + rebase sources."""
import hashlib, json, re, shutil, sys
from pathlib import Path

SKILL = Path("<repo-root>/skills/adaptive-html-final")
ASSETS = SKILL / "assets"
CORE = ['theme.css', 'components.css', 'visual-components.css', 'layouts.css', 'print.css']
INLINE = ['theme.css', 'components.css', 'visual-components.css', 'widgets.css', 'visual-html.css',
          'body-icons.css', 'editorial-patterns.css', 'shape-visuals.css', 'workflow-visuals.css',
          'layouts.css', 'print.css', 'theme-dark.css']


def ra(n): return (ASSETS / n).read_text(encoding='utf-8')
def core_hash(): return hashlib.sha256("\n".join(ra(n) for n in CORE).encode('utf-8')).hexdigest()
def combined():
    return f"/* adaptive-html-final-core-css-sha256: {core_hash()} */\n" + "\n\n".join(ra(n).strip("\n") for n in INLINE)


def replace_style(html):
    style = "<style>\n" + combined() + "\n</style>"
    out, c = re.subn(r"<style>[\s\S]*?</style>", lambda _m: style, html, count=1)
    if c != 1:
        raise RuntimeError(f"expected exactly one style block, got {c}")
    return out


def rebase(root):
    sdir = root / "sources"; adir = sdir / "assets"; adir.mkdir(parents=True, exist_ok=True)
    for n in INLINE:
        shutil.copyfile(ASSETS / n, adir / n)
    shutil.copyfile(SKILL / "manifest.json", sdir / "adaptive-html-final-manifest.json")
    (sdir / "profile.json").write_text(json.dumps({"profile": "auto"}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    hashes = {n: hashlib.sha256(ra(n).encode('utf-8')).hexdigest() for n in INLINE}
    integ = {"core_css_sha256": core_hash(), "asset_order": CORE,
             "conditional_asset_order": [n for n in INLINE if n not in CORE],
             "asset_sha256": hashes, "profile": "auto",
             "skill_version": json.loads((SKILL / "manifest.json").read_text())["version"]}
    (sdir / "css-integrity.json").write_text(json.dumps(integ, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


root = Path(sys.argv[1])
html_paths = [root / "index.html"] if (root / "index.html").exists() else sorted(root.glob("*.html"))
reinlined = 0
for p in html_paths:
    html = p.read_text(encoding='utf-8')
    if html.count('<style') == 1:  # single-bundle demo → re-inline; multi-block showcases keep their blocks
        p.write_text(replace_style(html), encoding='utf-8')
        reinlined += 1
rebase(root)
print(f"{root.name}: re-inlined {reinlined}/{len(html_paths)} file(s), sources rebased")
