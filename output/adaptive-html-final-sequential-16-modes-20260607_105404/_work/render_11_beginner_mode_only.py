#!/usr/bin/env python3
"""Render mode 11 beginner_html only for sequential QA.

No previous HTML body is read; no shared/common generator is imported.
The script reads only beginner layout/recipe/references and beginner-relevant vt/wg templates.
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
SKILL = REPO / "skills" / "adaptive-html-final"
ASSETS = SKILL / "assets"
OUT = ROOT / "pages" / "11_beginner_browser_cache_everyday_library.html"
SOURCES = ROOT / "sources"
SNAP = SOURCES / "assets"

MODE_MATERIALS = [
    "SKILL.md",
    "recipes/beginner.prompt.md",
    "assets/layouts/beginner-learning.html",
    "references/layout-system.md",
    "references/writing-system.md",
    "references/quality-gates.md",
    "references/body-icon-system.md",
    "references/visual-html-system.md",
    "references/widget-system.md",
    "assets/visual-html-templates/15-concept-explainer.html",
    "assets/visual-html-templates/01-hero-map.html",
    "assets/visual-html-templates/05-checklist-flow.html",
    "assets/widget-templates/10-svg-figure-sheet.html",
    "assets/widget-templates/13-annotated-flowchart.html",
    "assets/widget-templates/15-concept-explainer.html",
]
CSS_ORDER = [
    "theme.css", "components.css", "visual-components.css", "widgets.css", "visual-html.css",
    "body-icons.css", "editorial-patterns.css", "shape-visuals.css", "workflow-visuals.css",
    "layouts.css", "print.css", "theme-dark.css",
]
CORE = ["theme.css", "components.css", "visual-components.css", "layouts.css", "print.css"]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def sha_bytes(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


ICONS = {i["id"]: i["svg"] for i in json.loads(read(ASSETS / "body-icons.json"))}


def icon(name: str) -> str:
    return f'<span class="body-icon body-icon--sm">{ICONS[name]}</span>'


def h2(n: int, title: str, icon_name: str, sub: str) -> str:
    return f'<h2>{icon(icon_name)}<span class="num">{n}</span>{title}</h2>\n<p class="h2-sub">{sub}</p>'


def vt_concept() -> str:
    return '''<section class="vt-shell" aria-label="캐시 개념 4단 설명">
  <div class="vt-frame">
    <div class="concept-ring">
      <div class="vt-section-title"><span class="vt-num">?</span><h3 style="margin:0">캐시는 왜 필요할까</h3></div>
      <p class="vt-text">브라우저는 매번 서버에 모든 자료를 다시 달라고 하지 않고, 자주 쓰는 자료를 가까운 곳에 잠깐 보관합니다. 그래서 같은 사이트를 다시 열 때 더 빠르게 보일 수 있습니다.</p>
      <div class="concept-steps"><div class="concept-step"><b>1</b>요청</div><div class="concept-step"><b>2</b>저장</div><div class="concept-step"><b>3</b>재사용</div><div class="concept-step"><b>4</b>갱신</div></div>
    </div>
  </div>
</section>'''


def vt_hero_map() -> str:
    return '''<section class="vt-shell" aria-label="도서관 비유 지도">
  <div class="vt-frame">
    <div class="vt-demo">
      <div class="hm-grid"><article class="hm-card"><div class="vt-kicker">Library</div><h3>자주 찾는 책</h3><p class="vt-text">이미 한 번 빌린 책을 사서가 카운터 가까이에 두면 다음 방문자가 더 빨리 찾습니다.</p></article><article class="hm-card" style="--c:var(--vt-blue)"><div class="vt-kicker">Browser</div><h3>자주 쓰는 파일</h3><p class="vt-text">로고, 글꼴, 스타일 파일처럼 변하지 않는 자료는 브라우저가 잠깐 보관합니다.</p></article><article class="hm-card" style="--c:var(--vt-green)"><div class="vt-kicker">Refresh</div><h3>새 판 확인</h3><p class="vt-text">책이 개정되면 사서는 새 책인지 확인하고, 브라우저도 새 파일인지 확인합니다.</p></article></div>
      <div class="hm-result"><b>결론: 캐시는 게으름이 아니라 가까운 임시 책장</b><span>빠르게 보여주되, 오래된 자료를 계속 쓰지 않도록 갱신 규칙이 함께 필요합니다.</span></div>
    </div>
  </div>
</section>'''


def vt_checklist() -> str:
    return '''<section class="vt-shell" aria-label="새로고침 판단 체크 흐름">
  <div class="vt-frame">
    <div class="cf"><div class="cf-step"><span class="cf-check">1</span><div><b>화면이 이전과 똑같나?</b><p class="vt-text">내용을 고쳤는데도 예전 화면이면 먼저 일반 새로고침을 해봅니다.</p></div></div><div class="cf-step"><span class="cf-check">2</span><div><b>다른 사람 화면도 같은가?</b><p class="vt-text">내 브라우저만 오래된 자료를 보고 있는지 비교합니다.</p></div></div><div class="cf-step"><span class="cf-check">3</span><div><b>그래도 이상하면 강력 새로고침</b><p class="vt-text">캐시를 건너뛰고 서버에서 다시 가져오는 방식으로 확인합니다.</p></div></div></div>
  </div>
</section>'''


def wg_concept_mini() -> str:
    return '''<div class="wg-15" aria-labelledby="cache-concept-widget-title">
  <p class="wg-15-kicker">개념 교보재 · 브라우저 캐시</p>
  <h3 id="cache-concept-widget-title" class="wg-15-h3">단순 저장과 캐시 저장의 차이</h3>
  <div class="wg-15-steps">
    <input type="radio" name="cache-beginner-step" id="cache-beginner-s1" class="wg-15-step-in" checked>
    <input type="radio" name="cache-beginner-step" id="cache-beginner-s2" class="wg-15-step-in">
    <input type="radio" name="cache-beginner-step" id="cache-beginner-s3" class="wg-15-step-in">
    <div class="wg-15-stepnav"><label class="wg-15-stepbtn" for="cache-beginner-s1"><span class="wg-15-stepnum">1</span> 처음 방문</label><label class="wg-15-stepbtn" for="cache-beginner-s2"><span class="wg-15-stepnum">2</span> 잠깐 보관</label><label class="wg-15-stepbtn" for="cache-beginner-s3"><span class="wg-15-stepnum">3</span> 다시 확인</label></div>
    <div class="wg-15-stage"><div class="wg-15-ring" aria-hidden="true"><span class="wg-15-node wg-15-na">서버</span><span class="wg-15-node wg-15-nb">브라우저</span><span class="wg-15-node wg-15-nc">화면</span><span class="wg-15-node wg-15-nd wg-15-new">새판</span><span class="wg-15-key wg-15-k1">CSS</span><span class="wg-15-key wg-15-k2">이미지</span><span class="wg-15-center">cache</span></div><div class="wg-15-panels"><div class="wg-15-panel wg-15-p1"><h4 class="wg-15-pt">1. 처음에는 서버에서 받는다</h4><p>브라우저는 필요한 자료를 서버에 요청하고 화면을 만듭니다. 이때 일부 자료는 다시 쓸 수 있도록 표시됩니다.</p></div><div class="wg-15-panel wg-15-p2"><h4 class="wg-15-pt">2. 자주 쓰는 자료를 가까이 둔다</h4><p>같은 사이트를 다시 열면 보관한 자료를 먼저 확인합니다. 그래서 두 번째 방문은 더 빠르게 느껴질 수 있습니다.</p></div><div class="wg-15-panel wg-15-p3"><h4 class="wg-15-pt">3. 필요하면 새 자료로 바꾼다</h4><p>자료가 오래되었거나 사이트가 새 판을 알려주면 브라우저는 다시 서버에서 받아옵니다.</p></div></div></div>
  </div>
</div>'''


def wg_flow_mini() -> str:
    return '''<div class="wg-13" aria-labelledby="cache-flow-widget-title">
  <p class="wg-13-kicker">흐름 메모</p>
  <h3 id="cache-flow-widget-title" class="wg-13-title">캐시 문제를 만났을 때 말로 설명하는 순서</h3>
  <div class="wg-13-flow"><div class="wg-13-node"><b>1</b><span>무엇이 안 바뀌었는지 말한다</span></div><div class="wg-13-arrow">→</div><div class="wg-13-node"><b>2</b><span>내 브라우저만 그런지 본다</span></div><div class="wg-13-arrow">→</div><div class="wg-13-node"><b>3</b><span>새로고침 단계를 높인다</span></div></div>
</div>'''


def build_mapping() -> dict[str, str]:
    toc = '''<a href="#first-concept"><span>1</span>캐시 한 문장</a><a href="#terms"><span>2</span>처음 용어</a><a href="#analogy"><span>3</span>도서관 비유</a><a href="#traps"><span>4</span>헷갈리는 함정</a><a href="#practice"><span>5</span>직접 해보기</a><a href="#final-checklist"><span>6</span>마지막 점검</a>'''
    hero = '''<h2><span class="body-icon body-icon--sm">''' + ICONS["learning"] + '''</span>동네 도서관으로 먼저 생각하기</h2>
<p>브라우저 캐시는 어려운 기술처럼 들리지만, 사실은 <strong>자주 찾는 책을 카운터 가까이에 빼두는 도서관</strong>과 비슷합니다. 매번 창고 끝까지 가서 책을 찾지 않아도 되니 빠릅니다. 다만 책이 개정되었는데도 오래된 책을 계속 건네면 문제가 됩니다.</p>
<div class="card-grid"><article class="mini-card"><h3>처음 방문</h3><p>사서가 창고에서 책을 찾아 카운터로 가져옵니다. 브라우저는 서버에서 파일을 받아 화면을 만듭니다.</p></article><article class="mini-card"><h3>두 번째 방문</h3><p>사서가 가까운 책장에서 바로 꺼냅니다. 브라우저는 보관한 파일을 먼저 써서 빠르게 보여줍니다.</p></article><article class="mini-card"><h3>책이 바뀐 날</h3><p>사서는 새 판인지 확인해야 합니다. 브라우저도 새 파일인지 확인하고 필요하면 다시 가져옵니다.</p></article></div>'''

    first = f'''<div id="first-concept">{h2(1, "캐시는 ‘잠깐 보관함’이다", "idea", "브라우저 캐시는 인터넷을 복사해 두는 창고가 아니라, 다시 쓸 가능성이 높은 자료를 가까이에 두는 임시 책장입니다.")}
<p>웹사이트를 열면 브라우저는 글, 이미지, 스타일, 글꼴 같은 여러 자료를 받아옵니다. 이 자료를 매번 처음부터 다시 받으면 시간이 오래 걸립니다. 그래서 브라우저는 일부 자료를 내 기기 안에 잠깐 저장합니다. 이 저장 공간을 아주 쉽게 말하면 <span class="hl">잠깐 보관함</span>이라고 부를 수 있습니다.</p>
<p>중요한 점은 캐시가 “영원히 저장”을 뜻하지 않는다는 것입니다. 사이트는 자료마다 “얼마나 오래 써도 되는지”를 알려줄 수 있고, 브라우저는 그 힌트를 보고 다시 쓸지, 서버에 새 자료를 물어볼지 결정합니다. 초보자는 여기서 딱 한 문장만 기억하면 됩니다. 캐시는 빠르게 보여주려고 가까이 둔 임시 자료입니다.</p>
{vt_concept()}</div>'''

    terms = f'''<div id="terms">{h2(2, "처음 만나는 용어 5개", "question", "용어를 외우기보다, 각각이 도서관 비유에서 어떤 역할인지 붙여두면 이해가 쉬워집니다.")}
<div class="card-grid"><article class="term"><h3>브라우저</h3><p>웹사이트를 보여주는 앱입니다. 도서관 비유에서는 책을 찾아주는 사서입니다.</p></article><article class="term"><h3>서버</h3><p>웹사이트 자료가 있는 원래 장소입니다. 비유에서는 책이 보관된 큰 창고입니다.</p></article><article class="term"><h3>캐시</h3><p>다시 쓸 자료를 가까이에 둔 임시 보관함입니다. 비유에서는 카운터 옆 작은 책장입니다.</p></article><article class="term"><h3>새로고침</h3><p>현재 화면을 다시 확인하는 행동입니다. 사서에게 “혹시 새 판이 있나요?”라고 묻는 것과 비슷합니다.</p></article><article class="term"><h3>강력 새로고침</h3><p>가까운 책장을 덜 믿고 창고까지 다시 확인하는 행동입니다. 개발 중 화면이 안 바뀔 때 자주 씁니다.</p></article></div>
<p>이 다섯 단어를 알면 대부분의 캐시 대화를 따라갈 수 있습니다. “캐시를 지워보세요”라는 말도 겁낼 필요가 없습니다. 인터넷 전체를 지운다는 뜻이 아니라, 브라우저가 가까이에 둔 임시 자료 일부를 비우자는 말에 가깝습니다.</p></div>'''

    analogy = f'''<div id="analogy">{h2(3, "도서관 비유로 다시 보기", "learning", "캐시가 좋은 이유와 조심해야 할 이유는 같은 그림 안에 있습니다. 가까워서 빠르지만, 오래되면 틀릴 수 있습니다.")}
<p>동네 도서관에서 인기 있는 책은 사람들이 자주 찾습니다. 사서가 매번 먼 서고까지 걸어가면 줄이 길어집니다. 그래서 자주 찾는 책을 카운터 가까이에 두면 모두가 편해집니다. 이것이 캐시의 장점입니다. 브라우저도 자주 쓰는 이미지나 스타일 파일을 가까이 두면 페이지가 빠르게 열립니다.</p>
<p>하지만 문제도 있습니다. 책이 개정되었는데 가까운 책장에는 예전 판이 남아 있을 수 있습니다. 이때 독자는 최신 내용을 못 봅니다. 웹에서도 비슷합니다. 사이트 운영자가 버튼 색이나 문구를 바꿨는데 내 브라우저가 예전 파일을 계속 쓰면 “왜 나만 안 바뀌지?”라는 일이 생깁니다.</p>
{vt_hero_map()}
{wg_concept_mini()}</div>'''

    traps = f'''<div id="traps">{h2(4, "헷갈리는 함정 세 가지", "warning", "캐시는 편리하지만, 문제가 생겼을 때 원인을 너무 크게 오해하기 쉽습니다.")}
<div class="card-grid"><article class="danger"><h3>함정 1 · 새로고침했는데도 그대로</h3><p>일반 새로고침은 일부 보관 자료를 계속 쓸 수 있습니다. 화면이 계속 예전 같다면 강력 새로고침이나 캐시 비우기를 시도할 수 있습니다.</p></article><article class="danger"><h3>함정 2 · 캐시 삭제가 모든 데이터를 지운다고 생각</h3><p>캐시 삭제는 보통 임시 파일을 비우는 일입니다. 북마크나 계정 자체를 삭제한다는 뜻은 아닙니다. 다만 사이트 설정에 따라 다시 로그인해야 할 수 있습니다.</p></article><article class="danger"><h3>함정 3 · 항상 캐시가 범인이라고 단정</h3><p>화면이 안 바뀌는 이유가 서버 배포 문제, 네트워크 문제, 권한 문제일 수도 있습니다. 캐시는 먼저 확인할 후보이지 항상 정답은 아닙니다.</p></article></div>
{vt_checklist()}</div>'''

    practice = f'''<div id="practice">{h2(5, "직접 해보기: 화면이 안 바뀔 때 말로 설명하기", "check", "초보자에게 가장 좋은 연습은 단축키를 외우는 것보다 문제를 순서대로 말하는 것입니다.")}
<p>다음에 웹사이트가 이상하게 예전 화면처럼 보이면 바로 “캐시 문제야”라고 말하지 말고, 아래 순서대로 설명해 보세요. 이 순서가 있으면 개발자에게 질문할 때도 훨씬 정확해집니다.</p>
<div class="card-grid"><article class="mini-card"><h3>1. 무엇이 그대로인가</h3><p>버튼 색, 이미지, 글자, 로그인 상태처럼 안 바뀐 대상을 구체적으로 말합니다.</p></article><article class="mini-card"><h3>2. 어디에서 보이나</h3><p>내 브라우저, 휴대폰, 다른 사람의 화면 중 어디에서 같은지 확인합니다.</p></article><article class="mini-card"><h3>3. 어떤 새로고침을 했나</h3><p>일반 새로고침만 했는지, 강력 새로고침이나 캐시 비우기까지 했는지 적습니다.</p></article><article class="mini-card"><h3>4. 그래도 같다면</h3><p>캐시 외 원인을 의심합니다. 배포가 안 되었거나 서버가 다른 파일을 줄 수도 있습니다.</p></article></div>
{wg_flow_mini()}</div>'''

    final = f'''<div id="final-checklist">{h2(6, "마지막 점검", "success", "브라우저 캐시를 설명할 때 이 여섯 문장만 말할 수 있으면 충분합니다.")}
<div class="card-grid"><article class="summary-card"><h3>한 문장 정의</h3><p>캐시는 다시 쓸 자료를 가까이에 잠깐 두는 임시 보관함입니다.</p></article><article class="summary-card"><h3>좋은 점</h3><p>같은 자료를 매번 서버에서 받지 않아 페이지가 더 빠르게 열릴 수 있습니다.</p></article><article class="summary-card"><h3>주의점</h3><p>오래된 자료가 남아 있으면 화면이 바뀌지 않은 것처럼 보일 수 있습니다.</p></article><article class="summary-card"><h3>첫 대응</h3><p>일반 새로고침을 하고, 그래도 같으면 강력 새로고침이나 캐시 비우기를 생각합니다.</p></article><article class="summary-card"><h3>오해 금지</h3><p>캐시 삭제는 보통 임시 자료를 비우는 일이지 인터넷 전체를 지우는 일이 아닙니다.</p></article><article class="summary-card"><h3>질문법</h3><p>무엇이, 어디에서, 어떤 새로고침 뒤에도 그대로인지 적으면 도움을 빨리 받을 수 있습니다.</p></article></div>'''

    source = '<strong>Source note.</strong> 이 페이지는 브라우저 캐시 개념을 초보자에게 설명하기 위한 로컬 학습 문서입니다. 최신 브라우저별 단축키나 벤더별 세부 정책은 다루지 않고, 캐시의 기본 개념·오해·질문 방법만 안전하게 설명합니다.'
    return {
        "{{KICKER}}": "Beginner HTML · Everyday Tech",
        "{{TITLE}}": "브라우저 캐시를 동네 도서관처럼 이해하기",
        "{{SUBTITLE}}": "웹사이트가 왜 두 번째 방문부터 빨라지는지, 왜 가끔 새로고침이나 캐시 비우기가 필요한지 초보자용 비유로 정리합니다.",
        "{{META}}": '<div class="generated-row"><span>작성일 · 2026-06-07</span><span>mode · beginner_html</span><span>profile · auto</span><span>topic · browser cache</span></div><div class="lens-strip"><span>초보자</span><span>도서관 비유</span><span>용어 풀이</span><span>함정 점검</span></div>',
        "{{TOC}}": toc,
        "{{HERO_ANALOGY}}": hero,
        "{{FIRST_CONCEPT}}": first,
        "{{TERMS}}": terms,
        "{{ANALOGY}}": analogy,
        "{{TRAPS}}": traps,
        "{{PRACTICE}}": practice,
        "{{FINAL_CHECKLIST}}": final,
        "{{SOURCE_NOTE}}": source,
    }


def render() -> None:
    material_hashes = {}
    for rel in MODE_MATERIALS:
        p = SKILL / rel
        if not p.exists():
            raise FileNotFoundError(rel)
        material_hashes[rel] = sha_bytes(p)

    base = read(ASSETS / "base.html")
    layout = read(ASSETS / "layouts" / "beginner-learning.html")
    for k, v in build_mapping().items():
        layout = layout.replace(k, v)
    remaining = sorted(set(re.findall(r"{{[A-Z0-9_]+}}", layout)))
    if remaining:
        raise RuntimeError(f"unfilled layout placeholders: {remaining}")

    css = {name: read(ASSETS / name) for name in CSS_ORDER}
    core_hash = hashlib.sha256("\n".join(css[name] for name in CORE).encode("utf-8")).hexdigest()
    css["theme.css"] = f"/* adaptive-html-final-core-css-sha256: {core_hash} */\n" + css["theme.css"]

    html = base
    html = html.replace("{{TITLE}}", "브라우저 캐시를 동네 도서관처럼 이해하기")
    html = html.replace("{{DESCRIPTION}}", "beginner_html 모드로 작성한 브라우저 캐시 초보자용 학습 자료. 도서관 비유, 용어 풀이, 함정, 직접 점검 흐름을 포함합니다.")
    html = html.replace("{{JSON_LD_BLOCK}}", "")
    html = html.replace("{{BODY}}", layout)
    html = html.replace("{{FOOTER}}", "")
    slot_map = {
        "{{THEME_CSS}}": css["theme.css"],
        "{{COMPONENTS_CSS}}": css["components.css"],
        "{{VISUAL_COMPONENTS_CSS}}": css["visual-components.css"],
        "{{WIDGETS_CSS}}": css["widgets.css"],
        "{{VISUAL_HTML_CSS}}": css["visual-html.css"],
        "{{BODY_ICONS_CSS}}": css["body-icons.css"],
        "{{EDITORIAL_PATTERNS_CSS}}": css["editorial-patterns.css"],
        "{{SHAPE_VISUALS_CSS}}": css["shape-visuals.css"],
        "{{WORKFLOW_VISUALS_CSS}}": css["workflow-visuals.css"],
        "{{LAYOUTS_CSS}}": css["layouts.css"],
        "{{PRINT_CSS}}": css["print.css"],
        "{{THEME_DARK_CSS}}": css["theme-dark.css"],
    }
    for slot, value in slot_map.items():
        html = html.replace(slot, value)
    if "{{" in html:
        raise RuntimeError("unfilled base placeholders")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8")

    SNAP.mkdir(parents=True, exist_ok=True)
    asset_sha = {}
    for name in CSS_ORDER:
        raw = read(ASSETS / name)
        (SNAP / name).write_text(raw, encoding="utf-8")
        asset_sha[name] = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    (SOURCES / "profile.json").write_text(json.dumps({"profile": "auto"}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (SOURCES / "adaptive-html-final-manifest.json").write_text(json.dumps(json.loads(read(SKILL / "manifest.json")), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    integrity_path = SOURCES / "css-integrity.json"
    prior = {}
    if integrity_path.exists():
        try:
            prior = json.loads(integrity_path.read_text(encoding="utf-8"))
        except Exception:
            prior = {}
    prior.update({
        "core_css_sha256": core_hash,
        "asset_order": CORE,
        "asset_sha256": asset_sha,
        "profile": "auto",
        "mode11_material_sha256": material_hashes,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    })
    integrity_path.write_text(json.dumps(prior, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    render()
    print(OUT)
