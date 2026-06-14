#!/usr/bin/env python3
"""Render mode 09 article_html only for sequential QA.

No previous HTML body is read; no shared/common page generator is imported.
The script reads the article layout/recipe/references and article-relevant vt/wg templates only.
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
OUT = ROOT / "pages" / "09_article_judgment_log_over_prompt.html"
SOURCES = ROOT / "sources"
SNAP = SOURCES / "assets"

MODE_MATERIALS = [
    "SKILL.md",
    "recipes/article.prompt.md",
    "assets/layouts/magazine-article.html",
    "references/layout-system.md",
    "references/writing-system.md",
    "references/quality-gates.md",
    "references/body-icon-system.md",
    "references/visual-html-system.md",
    "references/widget-system.md",
    "assets/visual-html-templates/02-decision-tree.html",
    "assets/visual-html-templates/13-comparison-cards.html",
    "assets/visual-html-templates/15-concept-explainer.html",
    "assets/widget-templates/13-annotated-flowchart.html",
    "assets/widget-templates/14-feature-explainer.html",
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


def ul(items: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{item}</li>" for item in items) + "</ul>"


def vt_concept() -> str:
    return '''<section class="vt-shell" aria-label="판단 로그 개념 설명">
  <div class="vt-frame"><div class="concept-steps">
    <article class="concept-card"><div class="concept-no">1</div><h3>관찰</h3><p class="vt-text">무엇을 봤는지 기록한다. “사용자가 화났다”가 아니라 “승인 버튼 위치를 세 번 찾았다”처럼 적는다.</p></article>
    <article class="concept-card"><div class="concept-no">2</div><h3>판단</h3><p class="vt-text">그 관찰에서 무엇을 선택했는지 남긴다. 선택지는 버린 이유까지 함께 적어야 다음 사람이 검토할 수 있다.</p></article>
    <article class="concept-card"><div class="concept-no">3</div><h3>검증</h3><p class="vt-text">좋아 보이는가가 아니라 어떤 캡처·수치·테스트로 확인했는지 닫는다.</p></article>
  </div></div>
</section>'''


def vt_comparison() -> str:
    return '''<section class="vt-shell" aria-label="프롬프트 중심과 판단 로그 중심 비교">
  <div class="vt-frame"><div class="cmp"><article class="cmp-card"><div class="vt-kicker">Prompt first</div><h3>요청을 더 자세히 쓴다</h3><p class="vt-text">초기 방향을 맞추는 데는 좋지만, 결과가 틀렸을 때 왜 틀렸는지 축적되지 않는다.</p></article><article class="cmp-card win"><div class="vt-kicker">Judgment first</div><h3>선택 기준을 남긴다</h3><p class="vt-text">다음 생성자는 문장을 복사하지 않고 판단 근거를 재사용한다. 회귀 원인이 보인다.</p></article><article class="cmp-card"><div class="vt-kicker">Hybrid</div><h3>프롬프트 + 로그</h3><p class="vt-text">프롬프트는 입력 계약, 판단 로그는 산출물 품질의 변경 이력으로 둔다.</p></article></div></div>
</section>'''


def vt_decision() -> str:
    return '''<section class="vt-shell" aria-label="판단 로그 도입 결정 트리">
  <div class="vt-frame"><div class="vt-demo"><div class="dt-q">
    <article class="dt-card"><div class="vt-kicker">Q1</div><h3>결과를 반복 생성하나?</h3><p class="vt-text">한 번 쓰고 버릴 문서라면 프롬프트만으로 충분할 수 있다.</p></article>
    <div class="dt-arrow"></div>
    <article class="dt-card"><div class="vt-kicker">Q2</div><h3>실패가 되풀이되나?</h3><p class="vt-text">레이아웃·톤·근거 누락이 반복된다면 판단 로그가 필요하다.</p></article>
  </div><div class="dt-options"><article class="dt-card"><b>로그 생략</b><p class="vt-text">일회성 초안, 낮은 위험.</p></article><article class="dt-card" style="--c:var(--vt-gold)"><b>간단 로그</b><p class="vt-text">검수 기준 3개와 캡처 1장.</p></article><article class="dt-card" style="--c:var(--vt-green)"><b>정식 로그</b><p class="vt-text">결정·근거·대안·검증을 모두 기록.</p></article></div></div></div>
</section>'''


def wg_feature() -> str:
    return '''<div class="wg-14" aria-labelledby="article-feature-title">
  <p class="wg-14-kicker">본문 보조 · 기능 설명</p>
  <h3 id="article-feature-title" class="wg-14-h">판단 로그는 프롬프트의 반대가 아니라 품질 메모리다</h3>
  <p class="wg-14-lead">프롬프트는 “무엇을 해 달라”는 주문이고, 판단 로그는 “왜 이렇게 고쳤는가”라는 변경 기록입니다.</p>
  <div class="wg-14-tldr" role="note"><span class="wg-14-tldr-tag">핵심</span><p class="wg-14-tldr-body"><strong>다음 사람이 같은 실수를 피하게 만드는 기록</strong>이면 판단 로그이고, 단지 더 길어진 요청문이면 프롬프트 보강입니다.</p></div>
  <div class="wg-14-acc"><details class="wg-14-sec" open><summary class="wg-14-sum"><span class="wg-14-sum-no">01</span> 무엇을 적나 <span class="wg-14-chev" aria-hidden="true"></span></summary><div class="wg-14-sec-body"><p>관찰, 선택, 버린 대안, 검증 증거를 짧게 적습니다. “좋아 보인다”보다 “390px 캡처에서 overflow가 사라졌다”가 더 좋은 문장입니다.</p></div></details><details class="wg-14-sec"><summary class="wg-14-sum"><span class="wg-14-sum-no">02</span> 언제 생략하나 <span class="wg-14-chev" aria-hidden="true"></span></summary><div class="wg-14-sec-body"><p>한 번 쓰고 버릴 초안, 이해관계자가 없는 개인 메모, 실패 비용이 낮은 탐색 작업에서는 간단 체크만으로 충분합니다.</p></div></details></div>
</div>'''


def wg_flow() -> str:
    return '''<div class="wg-13-fc" aria-label="판단 로그 작성 흐름">
  <h3 class="wg-13-h">판단 로그 4단 흐름 <span class="wg-13-sub">관찰에서 다음 행동까지</span></h3>
  <div class="wg-13-flow"><a href="#article-problem" class="wg-13-node wg-13-node--start"><span class="wg-13-step">시작</span>문제 관찰</a><span class="wg-13-arrow" aria-hidden="true">↓</span><a href="#article-context" class="wg-13-node"><span class="wg-13-step">1</span>맥락 분리</a><span class="wg-13-arrow" aria-hidden="true">↓</span><a href="#article-argument" class="wg-13-node wg-13-node--decide"><span class="wg-13-step">2</span>판단 가능?</a><div class="wg-13-paths"><div class="wg-13-path wg-13-path--fail"><span class="wg-13-edge">아니오 → 확인 필요</span><a href="#article-source" class="wg-13-node wg-13-node--fail"><span class="wg-13-step">!</span>근거 보강</a></div><div class="wg-13-path wg-13-path--ok"><span class="wg-13-edge">예 → 기록</span><a href="#article-takeaway" class="wg-13-node wg-13-node--end"><span class="wg-13-step">끝</span>다음 행동</a></div></div></div>
</div>'''


def build_mapping() -> dict[str, str]:
    problem = f'''<div id="article-problem">{h2(1, "프롬프트를 더 길게 쓰면 해결된다는 착각", "question", "문제가 반복될수록 필요한 것은 더 긴 요청문이 아니라 실패가 남는 기록입니다.")}
<p>AI와 함께 문서를 만들다 보면 가장 쉬운 처방은 프롬프트를 늘리는 것입니다. “섹션을 뷰로 감싸라”, “아이콘을 빼지 마라”, “전문가처럼 써라” 같은 문장을 더하고 또 더합니다. 그런데 같은 문제가 다시 나타난다면 요청문이 짧아서가 아니라 <span class="hl">어떤 판단을 왜 했는지 남지 않았기 때문</span>일 가능성이 큽니다.</p>
<p>프롬프트는 방향을 정하지만 결과의 이력은 남기지 않습니다. 어느 섹션이 어색했는지, 어떤 캡처에서 문제가 보였는지, 왜 특정 템플릿을 골랐는지 기록하지 않으면 다음 생성자는 이전 실패를 학습하지 못합니다. 그래서 반복 작업에서는 프롬프트보다 판단 로그가 먼저입니다.</p>
{vt_concept()}</div>'''

    context = f'''<div id="article-context">{h2(2, "왜 지금 판단 로그인가", "timeline", "생성 품질 문제는 한 번의 문장 수정이 아니라 여러 번의 선택 누락에서 생깁니다.")}
<p>최근의 HTML 생성 작업은 단순한 글쓰기보다 운영 작업에 가깝습니다. 테마 토큰, 모바일 폭, 섹션 표면, 접근성, 템플릿 선택, 검증 명령이 함께 움직입니다. 이때 “잘 만들어 줘”라는 프롬프트는 너무 넓고, “이 CSS를 써”라는 지시는 너무 좁습니다.</p>
<p>판단 로그는 그 사이를 잇습니다. 요청자가 무엇을 중요하게 봤는지, 검수자가 무엇을 회귀로 판단했는지, 생성자가 어떤 대안을 버렸는지를 짧게 남깁니다. 그러면 다음 작업자는 과거 HTML을 복사하지 않고도 과거 판단을 재사용할 수 있습니다.</p>
{vt_comparison()}
{wg_feature()}</div>'''

    argument = f'''<div id="article-argument">{h2(3, "핵심 주장: 프롬프트는 입력 계약, 판단 로그는 품질 계약", "decision", "둘은 경쟁 관계가 아니라 서로 다른 층의 계약입니다.")}
<p>좋은 프롬프트는 시작점을 좁힙니다. 그러나 좋은 판단 로그는 작업이 끝난 뒤에도 남아 다음 결과물의 기준이 됩니다. 특히 여러 모드를 순차 생성하거나 여러 에이전트가 역할을 나눌 때, 판단 로그는 “이번 결과에서 무엇을 지켜야 하는가”를 전달하는 작은 운영 문서가 됩니다.</p>
<p>판단 로그에는 네 가지가 있으면 충분합니다. 첫째, 관찰한 문제입니다. 둘째, 선택한 수정 방향입니다. 셋째, 버린 대안입니다. 넷째, 검증 증거입니다. 이 네 칸이 있으면 프롬프트가 짧아도 결과물의 방향은 흔들리지 않습니다.</p>
{vt_decision()}</div>'''

    case = f'''<div id="article-case">{h2(4, "사례: HTML 스킬 검수에서 보인 회귀", "case", "구조 검증과 시각 품질 사이의 간극은 판단 로그가 없을 때 커집니다.")}
<p>한 HTML 쇼케이스 검수에서 구조 검증은 통과했지만 사용자가 보기에 결과물이 낮은 품질로 느껴지는 상황이 있었습니다. 섹션이 카드처럼 보이지 않거나, 제목 번호 앞 아이콘이 빠지거나, 여러 모드가 같은 틀로 찍힌 것처럼 보이는 문제가 반복되었습니다. 단순히 “최신 스킬을 사용하라”고 적는 것만으로는 부족했습니다.</p>
<p>판단 로그가 있었다면 문제는 더 빨리 좁혀졌을 것입니다. “최신 스킬”이라는 말은 추상적이지만 “모든 직접 섹션 h2는 body-icon을 먼저 둔다”, “layout 파일의 슬롯을 먼저 채운다”, “390px 캡처에서 overflow가 없어야 한다”는 판단은 실행 가능합니다. 프롬프트는 요청이고, 판단 로그는 회귀를 막는 체크포인트입니다.</p>
<div class="source-preserve"><div class="case-label">관찰 → 판단 → 검증</div><p><strong>관찰:</strong> 일부 산출물은 구조상 HTML이지만 모드별 템플릿 특성이 약했다.<br><strong>판단:</strong> 공통 생성기와 이전 본문 재사용을 금지하고 1모드 1검증으로 나눈다.<br><strong>검증:</strong> validate, quality contract, 1280/390 캡처를 각각 증거로 남긴다.</p></div></div>'''

    conclusion = f'''<div id="article-conclusion">{h2(5, "결론: 좋은 요청보다 좋은 회고 단위가 오래 간다", "success", "반복 작업의 품질은 프롬프트 길이가 아니라 판단이 남는 단위에서 결정됩니다.")}
<p>프롬프트를 잘 쓰는 일은 여전히 중요합니다. 하지만 작업이 반복되고, 결과물이 검수되고, 여러 사람이 같은 기준을 공유해야 한다면 프롬프트만으로는 부족합니다. 결과가 왜 좋은지, 왜 나쁜지, 무엇을 보고 고쳤는지가 남아야 합니다.</p>
<p>판단 로그는 거창한 문서가 아닙니다. 세 줄이어도 괜찮습니다. 다만 그 세 줄은 다음 작업자가 바로 행동할 수 있어야 합니다. “더 고급스럽게”보다 “다크 테마에서 카드 배경과 텍스트 대비가 4.5:1 이상이어야 한다”가 낫습니다. 그렇게 남은 판단이 다음 프롬프트를 짧고 정확하게 만듭니다.</p>
{wg_flow()}</div>'''

    takeaway = f'''{h2(6, "Takeaway · 판단 로그를 남기는 5문장", "check", "다음 생성이 같은 실패를 반복하지 않게 하는 최소 기록입니다.")}
<div id="article-takeaway" class="card-grid"><article class="summary-card"><h3>1 · 무엇을 봤나</h3><p>캡처, 검증 결과, 사용자 피드백 중 하나로 관찰을 적습니다.</p></article><article class="summary-card"><h3>2 · 무엇을 선택했나</h3><p>수정 방향을 한 문장으로 씁니다. “카드화”처럼 모호한 말은 피합니다.</p></article><article class="summary-card"><h3>3 · 무엇을 버렸나</h3><p>선택하지 않은 대안을 남기면 다음 사람이 같은 길을 반복하지 않습니다.</p></article><article class="summary-card"><h3>4 · 어떻게 확인했나</h3><p>명령 결과나 브라우저 캡처처럼 다시 확인 가능한 증거를 적습니다.</p></article><article class="summary-card"><h3>5 · 다음 조건은 무엇인가</h3><p>완료가 아니라 다음 작업의 시작 기준을 남깁니다.</p></article></div>'''

    related = f'''{h2(7, "Related Topics · 함께 읽을 주제", "connection", "판단 로그는 문서 작성뿐 아니라 코드 리뷰와 디자인 QA에도 같은 방식으로 적용됩니다.")}
<div class="related-grid"><article class="decision-card"><h3>레이아웃 QA</h3><p>화면 캡처를 근거로 섹션 간격, 카드 표면, 모바일 overflow를 판단하는 법.</p></article><article class="decision-card"><h3>프롬프트 운영</h3><p>작업 요청문과 결과 검수 기준을 분리해 반복 생성 품질을 높이는 법.</p></article><article class="decision-card"><h3>스킬 품질 게이트</h3><p>validate OK 이후에도 전문성·모드 적합성·템플릿 다양성을 확인하는 법.</p></article></div>'''

    return {
        "{{KICKER}}": "Article HTML · Editorial Essay",
        "{{TITLE}}": "프롬프트를 더 길게 쓰기 전에, 판단 로그를 남겨라",
        "{{LEAD}}": "AI 협업에서 같은 실수가 반복될 때 우리는 보통 프롬프트를 더 길게 씁니다. 하지만 반복 품질을 결정하는 것은 요청문의 길이가 아니라 판단이 남는 방식입니다. 이 글은 프롬프트 중심 작업을 판단 로그 중심 작업으로 바꾸면 왜 레이아웃·텍스트·검증 회귀가 줄어드는지 설명합니다.",
        "{{META}}": '<div class="generated-row"><span>작성일 · 2026-06-07</span><span>mode · article_html</span><span>profile · auto</span><span>topic · judgment log</span></div><div class="lens-strip"><span>Prompt</span><span>Judgment</span><span>QA</span><span>Regression</span></div>',
        "{{PULL_QUOTE}}": '<p>좋은 프롬프트는 시작점을 좁히지만, 좋은 판단 로그는 다음 결과물의 기준을 남긴다.</p>',
        "{{PROBLEM}}": problem,
        "{{CONTEXT}}": context,
        "{{CORE_ARGUMENT}}": argument,
        "{{CASE_STUDY}}": case,
        "{{CONCLUSION}}": conclusion,
        "{{TAKEAWAY}}": takeaway,
        "{{RELATED_TOPICS}}": related,
        "{{SOURCE_NOTE}}": '<strong id="article-source">Source note.</strong> 이 글은 2026-06-07 현재 로컬 HTML 스킬 순차 검수 과정에서 관찰한 레이아웃·텍스트 회귀 패턴을 바탕으로 쓴 공개용 아티클입니다. 외부 최신 통계나 특정 제품 성능 수치는 사용하지 않았으며, 사례는 개념 설명을 위한 내부 검수 맥락으로 한정합니다.',
    }


def render() -> None:
    material_hashes = {}
    for rel in MODE_MATERIALS:
        p = SKILL / rel
        if not p.exists():
            raise FileNotFoundError(rel)
        material_hashes[rel] = sha_bytes(p)

    base = read(ASSETS / "base.html")
    layout = read(ASSETS / "layouts" / "magazine-article.html")
    for k, v in build_mapping().items():
        layout = layout.replace(k, v)
    if re.search(r"{{[A-Z0-9_]+}}", layout):
        raise RuntimeError(f"unfilled layout placeholders: {sorted(set(re.findall(r'{{[A-Z0-9_]+}}', layout)))}")

    css = {name: read(ASSETS / name) for name in CSS_ORDER}
    core_hash = hashlib.sha256("\n".join(css[name] for name in CORE).encode("utf-8")).hexdigest()
    css["theme.css"] = f"/* adaptive-html-final-core-css-sha256: {core_hash} */\n" + css["theme.css"]

    html = base
    html = html.replace("{{TITLE}}", "프롬프트를 더 길게 쓰기 전에, 판단 로그를 남겨라")
    html = html.replace("{{DESCRIPTION}}", "article_html 모드로 작성한 프롬프트와 판단 로그의 차이, AI 협업 품질 회귀를 줄이는 방법에 대한 공개용 아티클")
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
        "mode09_material_sha256": material_hashes,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    })
    integrity_path.write_text(json.dumps(prior, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    render()
    print(OUT)
