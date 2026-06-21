#!/usr/bin/env python3
"""generation_smoke_check.py — output이 adaptive-html-final 스킬 자산으로 생성됐는지 최소 smoke.

신규 모드 후보/산출물이 `base.html`·layout 템플릿·테마 스위처·코어 CSS·source snapshot을
실제로 거쳐 생성됐는지(=임의 custom HTML이 아닌지)를 빠르게 확인한다. 공식 official 판정은
`validate_output.py` + `pretest_contract_check.py`가 담당하고, 본 스크립트는 그 앞단의
"스킬-자산 생성 지문" 유무만 본다(L126 재발 방지 smoke).

검사 지문(HTML):
  - skip-link `href="#main"`            (base.html 접근성 골격)
  - `<main id="main">` + `layout-*` 클래스 (layout 템플릿 사용)
  - 테마 라디오 `name="ahf-theme"` ≥ 8   (base.html 8테마 스위처)
  - 코어 CSS 해시 marker `core-css-sha256: <8hex>` (코어 CSS 인라인)
부가 신호(디렉터리): sources/ 스냅샷(manifest·profile·css-integrity).

사용: python3 scripts/generation_smoke_check.py <dir|index.html> [--recursive] [--json]
종료코드: 모든 대상이 skill-generated면 0, 핵심 지문(main+layout, core-hash) 누락이 하나라도 있으면 1.
"""
import sys
import json
import re
from pathlib import Path

SKIP_LINK_RE = re.compile(r'href=["\']#main["\']')
MAIN_RE = re.compile(r'<main\b[^>]*\bid=["\']main["\']', re.IGNORECASE)
LAYOUT_RE = re.compile(r'class=["\'][^"\']*\blayout-[a-z-]+', re.IGNORECASE)
THEME_RADIO_RE = re.compile(r'name=["\']ahf-theme["\']')
CORE_HASH_RE = re.compile(r'core-css-sha256:\s*[0-9a-f]{8}', re.IGNORECASE)


def _index_of(d: Path) -> Path | None:
    idx = d / "index.html"
    if idx.is_file():
        return idx
    htmls = sorted(p for p in d.glob("*.html"))
    return htmls[0] if htmls else None


def smoke(target: Path) -> dict:
    html_path = target if target.is_file() else _index_of(target)
    if html_path is None:
        return {"target": str(target), "verdict": "fail", "missing": ["no html"], "fingerprints": {}}
    html = html_path.read_text(encoding="utf-8", errors="ignore")
    fp = {
        "skip_link": bool(SKIP_LINK_RE.search(html)),
        "main_layout": bool(MAIN_RE.search(html)) and bool(LAYOUT_RE.search(html)),
        "theme_radios_8": len(THEME_RADIO_RE.findall(html)) >= 8,
        "core_hash_marker": bool(CORE_HASH_RE.search(html)),
    }
    d = html_path.parent
    sources_ok = all((d / "sources" / f).is_file() for f in
                     ("adaptive-html-final-manifest.json", "css-integrity.json", "profile.json"))
    missing = [k for k, ok in fp.items() if not ok]
    # 핵심 지문: main+layout, core_hash 누락이면 custom/비-스킬 HTML 의심 → fail
    core_missing = [k for k in ("main_layout", "core_hash_marker") if not fp[k]]
    if core_missing:
        verdict = "fail"
    elif missing:
        verdict = "warn"
    else:
        verdict = "pass"
    return {"target": str(target), "verdict": verdict, "fingerprints": fp,
            "sources_snapshot": sources_ok, "missing": missing}


def _leaf_dirs(root: Path) -> list:
    out = []
    for idx in sorted(root.rglob("index.html")):
        if idx.parent.name in ("sources", "assets", "_bodies", "_qa", "_screenshots"):
            continue
        out.append(idx.parent)
    return out


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    recursive = "--recursive" in argv
    as_json = "--json" in argv
    if not args:
        print("usage: generation_smoke_check.py <dir|index.html> [--recursive] [--json]", file=sys.stderr)
        return 2
    root = Path(args[0]).resolve()
    targets = _leaf_dirs(root) if (recursive and root.is_dir()) else [root]
    results = [smoke(t) for t in targets]

    if as_json:
        print(json.dumps({"results": results}, ensure_ascii=False, indent=2))
    else:
        sym = {"pass": "✅", "warn": "🟡", "fail": "❌"}
        for r in results:
            name = Path(r["target"]).name or r["target"]
            extra = "" if not r["missing"] else f"  (누락: {', '.join(r['missing'])})"
            snap = "" if r.get("sources_snapshot") else "  [sources 스냅샷 없음]"
            print(f"{sym[r['verdict']]} {r['verdict'].upper():5} {name}{extra}{snap}")
        npass = sum(1 for r in results if r["verdict"] == "pass")
        nwarn = sum(1 for r in results if r["verdict"] == "warn")
        nfail = sum(1 for r in results if r["verdict"] == "fail")
        print(f"\n요약: pass {npass} · warn {nwarn} · fail {nfail}  (총 {len(results)})")
    return 1 if any(r["verdict"] == "fail" for r in results) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
