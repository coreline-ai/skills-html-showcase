#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import html
import json
import re
import shutil
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "adaptive-html-final"
ASSETS = SKILL / "assets"
DEMO = ROOT / "output" / "2026-06-15" / "demo17"
SOURCES = DEMO / "sources"

CORE_ORDER = ["theme.css", "components.css", "visual-components.css", "layouts.css", "print.css"]
INLINE_ORDER = [
    "theme.css",
    "components.css",
    "visual-components.css",
    "widgets.css",
    "visual-html.css",
    "body-icons.css",
    "editorial-patterns.css",
    "layouts.css",
    "print.css",
    "theme-dark.css",
]

MODE_LABELS = {
    "skill_audit": "스킬 감사",
    "platform_blog": "플랫폼 블로그",
    "seo_dashboard": "SEO 대시보드",
    "education_html": "교육 모듈",
    "github_analysis": "GitHub 분석",
    "github_feature_usage": "GitHub 기능 가이드",
    "youtube_analysis": "YouTube 분석",
    "manual_analysis": "매뉴얼 분석",
    "expert_html": "전문가 리포트",
    "article_html": "아티클",
    "blog_writer": "블로그 글",
    "beginner_html": "초보자 학습",
    "reference_html": "레퍼런스",
    "comparison_html": "비교 매트릭스",
    "case_study_html": "케이스 스터디",
    "landing_brief_html": "랜딩 브리프",
    "checklist_playbook": "체크리스트",
}


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def strip_tags(fragment: str) -> str:
    fragment = re.sub(r"<style\b[^>]*>[\s\S]*?</style>", " ", fragment, flags=re.I)
    fragment = re.sub(r"<script\b[^>]*>[\s\S]*?</script>", " ", fragment, flags=re.I)
    fragment = re.sub(r"<[^>]+>", " ", fragment)
    return re.sub(r"\s+", " ", html.unescape(fragment)).strip()


def page_title(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    match = re.search(r"<h1\b[^>]*>([\s\S]*?)</h1>", text, re.I)
    if match:
        return strip_tags(match.group(1))
    title = re.search(r"<title\b[^>]*>([\s\S]*?)</title>", text, re.I)
    return strip_tags(title.group(1)) if title else path.parent.name


def mode_from_dir(dirname: str) -> str:
    match = re.match(r"\d+_(.+?)_[^/]+$", dirname)
    return match.group(1) if match else dirname


def icon(icon_id: str) -> str:
    out = subprocess.check_output(
        ["python3", str(SKILL / "scripts" / "body_icon_markup.py"), icon_id, "--class", "body-icon--sm"],
        cwd=ROOT,
        text=True,
    ).strip()
    return out


def h2(num: int, title: str, icon_id: str, key: bool = False) -> str:
    cls = "num is-key" if key else "num"
    return f'{icon(icon_id)}<span class="{cls}">{num}</span>{esc(title)}'


def collect_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for idx in sorted(DEMO.glob("[0-9][0-9]_*")):
        page = idx / "index.html"
        if not page.exists():
            continue
        no = idx.name.split("_", 1)[0]
        mode = mode_from_dir(idx.name)
        rows.append(
            {
                "no": no,
                "dir": idx.name,
                "href": f"{idx.name}/index.html",
                "mode": mode,
                "label": MODE_LABELS.get(mode, mode),
                "title": page_title(page),
            }
        )
    if len(rows) != 17:
        raise SystemExit(f"expected 17 demo pages, found {len(rows)}")
    return rows


def css_bundle() -> tuple[dict[str, str], str, dict]:
    asset_text = {name: (ASSETS / name).read_text(encoding="utf-8") for name in INLINE_ORDER}
    core = "\n".join(asset_text[name] for name in CORE_ORDER)
    core_hash = hashlib.sha256(core.encode("utf-8")).hexdigest()
    slots = {
        "THEME_CSS": f"/* adaptive-html-final-core-css-sha256: {core_hash} */\n" + asset_text["theme.css"],
        "COMPONENTS_CSS": asset_text["components.css"],
        "VISUAL_COMPONENTS_CSS": asset_text["visual-components.css"],
        "WIDGETS_CSS": asset_text["widgets.css"],
        "VISUAL_HTML_CSS": asset_text["visual-html.css"],
        "BODY_ICONS_CSS": asset_text["body-icons.css"],
        "EDITORIAL_PATTERNS_CSS": asset_text["editorial-patterns.css"],
        "SHAPE_VISUALS_CSS": "",
        "WORKFLOW_VISUALS_CSS": "",
        "LAYOUTS_CSS": asset_text["layouts.css"],
        "PRINT_CSS": asset_text["print.css"],
        "THEME_DARK_CSS": asset_text["theme-dark.css"],
    }
    integrity = {
        "core_css_sha256": core_hash,
        "asset_order": CORE_ORDER,
        "profile": "auto",
        "asset_sha256": {name: hashlib.sha256(asset_text[name].encode("utf-8")).hexdigest() for name in INLINE_ORDER},
    }
    return slots, core_hash, integrity


def build_body(rows: list[dict[str, str]]) -> str:
    version = json.loads((SKILL / "manifest.json").read_text(encoding="utf-8"))["version"]
    commit = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, text=True).strip()
    generated = datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%d %H:%M KST")
    cards = "\n".join(
        f'''<article class="mini-card rail-red">
  <h3><a href="{esc(r['href'])}">{esc(r['no'])}. {esc(r['label'])}</a></h3>
  <p>{esc(r['title'])}</p>
  <p><span class="tag">{esc(r['mode'])}</span></p>
</article>'''
        for r in rows[:6]
    )
    table_rows = "\n".join(
        f'''<tr>
  <td>{esc(r['no'])}</td>
  <td><span class="tag">{esc(r['mode'])}</span></td>
  <td>{esc(r['label'])}</td>
  <td><a href="{esc(r['href'])}">{esc(r['title'])}</a></td>
</tr>'''
        for r in rows
    )
    toc = "".join(
        f'<a class="toc-pill" href="#section-{i:02d}"><b>{i}</b>{label}</a>'
        for i, label in enumerate(["한 화면 요약", "대표 6개", "17개 전체 링크", "탐색 방식", "바로 열기"], 1)
    )

    hero_map = '''<section class="vt-shell">
  <div class="vt-frame">
    <div class="vt-demo"><div class="hm-grid"><article class="hm-card"><div class="vt-kicker">Index</div><h3>상위 목차 복구</h3><p class="vt-text">누락되어 있던 demo17 루트 index를 생성해 17개 결과물의 진입점을 하나로 모았습니다.</p></article><article class="hm-card" style="--c:var(--vt-blue)"><div class="vt-kicker">Scope</div><h3>17개 모드 전체 연결</h3><p class="vt-text">각 하위 폴더의 index.html을 상대 링크로 연결해 체크아웃 위치가 바뀌어도 탐색됩니다.</p></article><article class="hm-card" style="--c:var(--vt-green)"><div class="vt-kicker">Action</div><h3>열람과 검증 분리</h3><p class="vt-text">이 페이지는 네비게이션 셸이며, 각 데모의 본문·증빙은 하위 결과물에서 확인합니다.</p></article></div><div class="hm-result"><b>결론: demo17의 단일 진입점</b><span>사용자는 이제 상위 index에서 모든 모드 결과물을 순서대로 열 수 있습니다.</span></div></div>
  </div>
</section>'''

    wg02 = '''<section class="wg-02-dir" aria-labelledby="wg-02-title">
  <header class="wg-02-head">
    <p class="wg-02-kicker">NAVIGATION DIRECTIONS</p>
    <h2 id="wg-02-title" class="wg-02-h">데모 탐색 방식 선택</h2>
    <p class="wg-02-lead">17개 산출물을 어떤 기준으로 볼지 세 가지 방향으로 나눴습니다. 선택 강조는 CSS 라디오만 사용합니다.</p>
  </header>
  <fieldset class="wg-02-grid">
    <legend class="wg-02-sr">탐색 방식 선택</legend>
    <input type="radio" name="wg-02-pick" id="wg-02-a" class="wg-02-radio" checked>
    <div class="wg-02-card" data-dir="A"><div class="wg-02-preview wg-02-preview--a"><div class="wg-02-pv-bar"><span class="wg-02-pv-dot"></span><span class="wg-02-pv-line"></span></div><div class="wg-02-pv-hero">순서대로</div><div class="wg-02-pv-body"><span></span><span></span><span class="wg-02-pv-short"></span></div><div class="wg-02-pv-cta wg-02-pv-cta--a">01→17</div></div><div class="wg-02-meta"><label for="wg-02-a" class="wg-02-pick-label">모드 라우터 순서</label><p class="wg-02-desc">AGENTS.md 결정표의 01~17 우선순서대로 검수합니다.</p><ul class="wg-02-palette" aria-label="순서 탐색"><li style="background:var(--bg)"><span>bg</span></li><li style="background:var(--ink)"><span>ink</span></li><li style="background:var(--accent)"><span>go</span></li></ul><span class="wg-02-badge">선택됨</span></div></div>
    <input type="radio" name="wg-02-pick" id="wg-02-b" class="wg-02-radio">
    <div class="wg-02-card" data-dir="B"><div class="wg-02-preview wg-02-preview--b"><div class="wg-02-pv-bar wg-02-pv-bar--b"><span class="wg-02-pv-dot"></span><span class="wg-02-pv-line"></span></div><div class="wg-02-pv-cards"><span></span><span></span><span></span></div><div class="wg-02-pv-cta wg-02-pv-cta--b">리포트형</div></div><div class="wg-02-meta"><label for="wg-02-b" class="wg-02-pick-label">검토·판정 중심</label><p class="wg-02-desc">감사, GitHub 분석, 전문가 리포트, 체크리스트처럼 판정이 중요한 결과물부터 봅니다.</p><ul class="wg-02-palette" aria-label="검토 탐색"><li style="background:var(--dark)"><span>dark</span></li><li style="background:var(--good-accent)"><span>ok</span></li><li style="background:var(--accent)"><span>risk</span></li></ul><span class="wg-02-badge">선택됨</span></div></div>
    <input type="radio" name="wg-02-pick" id="wg-02-c" class="wg-02-radio">
    <div class="wg-02-card" data-dir="C"><div class="wg-02-preview wg-02-preview--c"><div class="wg-02-pv-bar wg-02-pv-bar--c"><span class="wg-02-pv-dot"></span><span class="wg-02-pv-line"></span></div><div class="wg-02-pv-split"><div class="wg-02-pv-aside"></div><div class="wg-02-pv-main"><span></span><span></span></div></div><div class="wg-02-pv-cta wg-02-pv-cta--c">학습형</div></div><div class="wg-02-meta"><label for="wg-02-c" class="wg-02-pick-label">학습·발행 중심</label><p class="wg-02-desc">교육, 초보자, 레퍼런스, 블로그, 플랫폼 변환처럼 읽기 경험을 먼저 확인합니다.</p><ul class="wg-02-palette" aria-label="학습 탐색"><li style="background:var(--analogy-bg)"><span>soft</span></li><li style="background:var(--analogy-accent)"><span>learn</span></li><li style="background:var(--accent)"><span>cta</span></li></ul><span class="wg-02-badge">선택됨</span></div></div>
  </fieldset>
  <p class="wg-02-foot">이 위젯은 landing_brief_html의 권장 wg-02를 사용한 무 JS 탐색 보강입니다.</p>
</section>'''

    body = f'''<main id="main" class="page-wide layout-landing">
  <header class="header landing-header"><div class="kicker"><span class="kicker-text">DEMO17 INDEX · ADAPTIVE HTML FINAL</span></div><h1>17개 데모 결과물 상위 목차</h1><p class="sub">오늘 pull된 origin/main 기준 데모 세트에 루트 index가 없어서, adaptive-html-final의 landing_brief_html 모드로 17개 하위 결과물을 한 곳에 연결했습니다. 모든 링크는 상대 경로라 로컬 파일과 GitHub Pages 양쪽에서 같은 구조로 이동합니다.</p><div class="meta"><span>landing_brief_html</span><span>landing-brief.html</span><span>profile auto</span><span>adaptive-html-final v{esc(version)}</span><span>commit {esc(commit)}</span><span>17 links</span></div><div class="generated-row"><p class="generated-date">Generated · {esc(generated)}</p><div class="lens-strip" aria-label="적용 렌즈"><span class="lens-strip-label">LENS</span><span class="lens-chip">상위 목차</span><span class="lens-chip">17모드</span><span class="lens-chip">무 JS</span><span class="lens-chip">상대 링크</span></div></div></header>
  <nav class="toc-map" aria-label="문서 목차"><span class="label">문서 목차</span><p>상위 목차의 목적, 대표 결과물, 전체 링크, 탐색 방식, 바로 열기를 순서대로 확인합니다.</p><div class="toc-pills">{toc}</div></nav>
  <section class="hero-analogy" id="section-01"><h2>{h2(1, '한 화면 요약', 'landing', True)}</h2><p class="h2-sub">누락된 상위 index를 복구하고, 17개 결과물의 진입 링크를 안정적으로 고정합니다.</p>{hero_map}<p>이 페이지는 새 데모 본문을 다시 생성하는 것이 아니라, 이미 커밋된 17개 데모 산출물의 <strong>상위 네비게이션 셸</strong>입니다. 각 링크는 하위 폴더의 <code>index.html</code>로 직접 연결되며, 파일 시스템 위치가 달라져도 루트 폴더 내부 상대 경로를 유지합니다.</p><div class="box"><p><strong>구성 원칙</strong></p><ul><li>17개 링크를 모두 노출해 브라우저 탭으로 바로 열 수 있게 했습니다.</li><li>상위 페이지는 <code>landing_brief_html</code> 모드의 hero, value props, how it works, FAQ, CTA 구조를 따릅니다.</li><li>외부 동작 JS 없이 테마 스위처, vt hero-map, wg-02 탐색 위젯만 사용합니다.</li></ul></div></section>
  <section class="value-grid" id="section-02"><h2>{h2(2, '대표 6개 빠른 진입', 'map')}</h2><p class="h2-sub">전체 목록에 들어가기 전, 검수 흐름에서 자주 확인하는 대표 결과물부터 빠르게 엽니다.</p><div class="card-grid rail-cycle">{cards}</div><p>대표 카드는 전체 17개 중 앞쪽 여섯 모드를 빠르게 여는 진입점입니다. 전체 검수나 공유 링크 정리는 아래 표를 기준으로 진행하면 누락 없이 순서가 맞습니다.</p></section>
  <section class="how-it-works" id="section-03"><h2>{h2(3, '17개 전체 링크', 'reference')}</h2><p class="h2-sub">각 행은 모드 번호, 모드 ID, 사람이 읽는 레이블, 실제 하위 index 링크로 구성됩니다.</p><div class="table-scroll"><table class="table"><caption>demo17 하위 결과물 17개 링크</caption><thead><tr><th>No</th><th>Mode</th><th>Label</th><th>Open</th></tr></thead><tbody>{table_rows}</tbody></table></div><p>표의 링크를 클릭하면 같은 브라우저 탭에서 해당 데모로 이동합니다. 새 탭이 필요하면 브라우저의 기본 새 탭 열기 동작을 사용하면 됩니다.</p></section>
  <section class="faq" id="section-04"><h2>{h2(4, '탐색 방식', 'check')}</h2><p class="h2-sub">상위 index는 단순 링크 목록에 그치지 않고, 어떤 기준으로 볼지 선택할 수 있게 구성했습니다.</p>{wg02}<dl><dt>왜 상위 index가 필요했나?</dt><dd>하위 17개 폴더에는 각각 index가 있었지만, <code>demo17/index.html</code>이 없어 전체 세트를 한 번에 공유하거나 열기 어려웠습니다.</dd><dt>링크가 절대 경로인가?</dt><dd>아닙니다. 모두 하위 폴더 기준 상대 링크라 로컬 checkout 위치와 무관하게 동작합니다.</dd><dt>개별 데모 내용도 바뀌었나?</dt><dd>아닙니다. 이번 작업은 상위 목차 생성과 루트 sources 스냅샷 추가에 한정했습니다.</dd></dl></section>
  <section class="try" id="section-05"><h2>{h2(5, '바로 열기', 'success', True)}</h2><p>가장 최근에 요청했던 전문가 리포트 데모와 전체 첫 번째 데모를 바로 열 수 있습니다. 전체 검수는 위 표의 01부터 17까지 순서대로 진행하세요.</p><div class="summary-card"><p><strong>추천 시작점</strong></p><p><a href="09_expert_html_read-replica-feasibility/index.html">09 전문가 리포트 · Read Replica Feasibility</a></p><p><a href="01_skill_audit_meeting-summary-bot-audit/index.html">01 스킬 감사 · Meeting Summary Bot Audit</a></p></div><div class="tag-list"><span class="tag">NO behavioral script</span><span class="tag">17 demo links</span><span class="tag">relative href</span><span class="tag">v{esc(version)}</span></div></section>
  <aside class="source-note"><div class="label">Source snapshot</div><p>목차 생성 시점의 manifest, CSS integrity, profile 정보는 <code>sources/</code>에 기록했습니다. 하위 17개 데모의 원본 산출물은 각 폴더의 <code>sources/</code>를 유지합니다.</p></aside>
</main>'''
    return body


def write_sources(integrity: dict) -> None:
    (SOURCES / "assets").mkdir(parents=True, exist_ok=True)
    for name in INLINE_ORDER:
        shutil.copyfile(ASSETS / name, SOURCES / "assets" / name)
    (SOURCES / "css-integrity.json").write_text(json.dumps(integrity, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    shutil.copyfile(SKILL / "manifest.json", SOURCES / "adaptive-html-final-manifest.json")
    (SOURCES / "profile.json").write_text('{"profile":"auto"}\n', encoding="utf-8")
    (SOURCES / "fresh-generation-rule.json").write_text(
        json.dumps(
            {
                "fresh_run": False,
                "reused_previous_pages": False,
                "mode_scope": "demo17 navigation index only",
                "linked_pages": 17,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def render() -> Path:
    rows = collect_rows()
    slots, _core_hash, integrity = css_bundle()
    body = build_body(rows)
    base = (ASSETS / "base.html").read_text(encoding="utf-8")
    html_text = base
    replacements = {
        "TITLE": "17개 데모 결과물 상위 목차",
        "DESCRIPTION": "adaptive-html-final demo17 하위 17개 결과물을 모두 연결한 상위 index 페이지입니다.",
        "JSON_LD_BLOCK": "",
        "BODY": body,
        "FOOTER": "",
        **slots,
    }
    for key, value in replacements.items():
        html_text = html_text.replace("{{" + key + "}}", value)
    leftovers = re.findall(r"\{\{[A-Z_]+\}\}", html_text)
    if leftovers:
        raise SystemExit(f"unfilled placeholders: {sorted(set(leftovers))}")
    DEMO.mkdir(parents=True, exist_ok=True)
    (DEMO / "index.html").write_text(html_text, encoding="utf-8")
    write_sources(integrity)
    return DEMO / "index.html"


if __name__ == "__main__":
    print(render().relative_to(ROOT))
