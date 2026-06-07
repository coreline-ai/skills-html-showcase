#!/usr/bin/env python3
"""Render mode 10 blog_writer only for sequential QA.

No previous HTML body is read; no shared/common generator is imported.
The script reads the blog layout/recipe/references and blog-relevant vt/wg templates only.
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
OUT = ROOT / "pages" / "10_blog_four_days_with_ai_review_notes.html"
SOURCES = ROOT / "sources"
SNAP = SOURCES / "assets"

MODE_MATERIALS = [
    "SKILL.md",
    "recipes/blog.prompt.md",
    "assets/layouts/personal-blog-essay.html",
    "references/layout-system.md",
    "references/writing-system.md",
    "references/quality-gates.md",
    "references/body-icon-system.md",
    "references/visual-html-system.md",
    "references/widget-system.md",
    "assets/visual-html-templates/04-timeline.html",
    "assets/visual-html-templates/11-weekly-status.html",
    "assets/visual-html-templates/13-comparison-cards.html",
    "assets/widget-templates/17-pr-writeup.html",
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


def vt_timeline() -> str:
    return '''<section class="vt-shell" aria-label="4일간의 변화 타임라인">
  <div class="vt-frame"><div class="tl">
    <div class="tl-item"><span class="tl-dot"></span><div><b>Day 1 · 프롬프트만 고침</b><p class="vt-text">요청문은 길어졌지만 다음 결과가 왜 달라져야 하는지 남지 않았다.</p></div></div>
    <div class="tl-item"><span class="tl-dot"></span><div><b>Day 2 · 캡처를 붙임</b><p class="vt-text">문제 설명이 시각 증거와 연결되자 수정 방향이 좁아졌다.</p></div></div>
    <div class="tl-item"><span class="tl-dot"></span><div><b>Day 3 · 판단을 기록</b><p class="vt-text">“왜 이 레이아웃을 유지하는가”가 남자 같은 실수가 줄었다.</p></div></div>
    <div class="tl-item"><span class="tl-dot"></span><div><b>Day 4 · 다음 조건을 씀</b><p class="vt-text">완료 보고 대신 다음 모드의 시작 조건이 생겼다.</p></div></div>
  </div></div>
</section>'''


def vt_weekly_status() -> str:
    return '''<section class="vt-shell" aria-label="리뷰 노트 상태판">
  <div class="vt-frame"><div class="wk"><div class="wk-head"><b>AI review notes · 4-day pulse</b><span>writing system</span></div><div class="wk-cols"><article><strong>3</strong><span>반복 회귀</span></article><article><strong>2</strong><span>증거 캡처</span></article><article><strong>1</strong><span>남긴 판단</span></article></div><div class="wk-row"><span>프롬프트 보강</span><div class="wk-bar"><i style="width:70%"></i></div><b>70%</b></div><div class="wk-row"><span>판단 로그 전환</span><div class="wk-bar"><i style="width:92%"></i></div><b>92%</b></div></div></div>
</section>'''


def vt_comparison() -> str:
    return '''<section class="vt-shell" aria-label="프롬프트와 리뷰 노트 비교">
  <div class="vt-frame"><div class="cmp"><article class="cmp-card"><div class="vt-kicker">Prompt</div><h3>시작을 빠르게 만든다</h3><p class="vt-text">요청을 명확히 하고 범위를 좁히는 데 좋다. 하지만 실패 이유는 자동으로 남지 않는다.</p></article><article class="cmp-card win"><div class="vt-kicker">Review Note</div><h3>다음 수정을 쉽게 만든다</h3><p class="vt-text">캡처, 판단, 버린 대안을 남겨 다음 생성자가 같은 실수를 피하게 한다.</p></article><article class="cmp-card"><div class="vt-kicker">Pair</div><h3>둘을 함께 쓴다</h3><p class="vt-text">프롬프트는 입력 계약, 리뷰 노트는 결과물의 품질 계약으로 나눠 쓴다.</p></article></div></div>
</section>'''


def wg_pr_writeup() -> str:
    return '''<div class="wg-17" aria-labelledby="blog-pr-title">
  <header class="wg-17-head"><p class="wg-17-kicker">작은 PR 메모</p><h3 id="blog-pr-title" class="wg-17-title">refactor: AI 리뷰 노트를 프롬프트 앞에 두기</h3><p class="wg-17-p">바꾼 것은 문장의 길이가 아니라 작업 순서였습니다. 먼저 관찰과 판단을 적고, 그다음 프롬프트를 짧게 정리했습니다.</p></header>
  <div class="wg-17-summary"><span class="wg-17-chip wg-17-chip-del">before</span><span>요청문 계속 추가</span><span class="wg-17-chip wg-17-chip-add">after</span><span>관찰·판단·검증 먼저 기록</span></div>
  <div class="wg-17-ba"><div class="wg-17-ba-col wg-17-ba-before"><span class="wg-17-ba-tag">Before</span><ul class="wg-17-ba-list"><li>“더 고급지게” 같은 넓은 지시</li><li>어디가 문제였는지 기억에 의존</li><li>다음 작업에서 같은 회귀 반복</li></ul></div><div class="wg-17-ba-arrow">→</div><div class="wg-17-ba-col wg-17-ba-after"><span class="wg-17-ba-tag">After</span><ul class="wg-17-ba-list"><li>캡처 위치와 판단 기준 기록</li><li>버린 대안까지 짧게 남김</li><li>다음 프롬프트가 짧아짐</li></ul></div></div>
</div>'''


def build_mapping() -> dict[str, str]:
    personal_note = '''<p><strong>추천 제목:</strong> AI 리뷰 노트를 프롬프트 앞에 두었더니 달라진 것</p>
<p><strong>제목 후보:</strong> ① 프롬프트보다 먼저 써야 할 것 ② AI 협업에서 회귀를 줄인 작은 습관 ③ 리뷰 노트를 남기자 프롬프트가 짧아졌다</p>
<p><strong>메타 설명:</strong> 4일 동안 AI 산출물을 검수하며 프롬프트보다 판단 로그와 리뷰 노트가 더 오래 가는 이유를 기록한 개인 블로그 글.</p>
<nav class="toc-map" aria-label="글 목차">
  <span class="label">글의 흐름</span>
  <p>문제를 본 순간부터 작은 기록 습관으로 이어지는 개인 블로그 구조입니다.</p>
  <div class="toc-pills">
    <a class="toc-pill" href="#why-now"><b>1</b>왜 지금</a>
    <a class="toc-pill" href="#my-view"><b>2</b>내 관점</a>
    <a class="toc-pill" href="#example"><b>3</b>작은 사례</a>
    <a class="toc-pill" href="#how-to-start"><b>4</b>시작법</a>
    <a class="toc-pill" href="#closing"><b>5</b>마무리</a>
  </div>
</nav>'''

    why_now = f'''<div id="why-now">{h2(1, "왜 지금 AI 리뷰 노트를 말하게 됐나", "question", "프롬프트를 계속 고치는데도 같은 회귀가 반복될 때, 남겨야 할 것은 더 긴 요청문이 아니었습니다.")}
<p>처음에는 프롬프트가 문제라고 생각했습니다. “섹션을 카드처럼 감싸라”, “모바일에서 넘치지 않게 하라”, “전문 문서처럼 써라” 같은 문장을 계속 붙였습니다. 그런데 이상하게도 다음 결과물은 또 비슷한 곳에서 무너졌습니다.</p>
<p>그때 알게 된 것은 간단했습니다. 나는 요청을 남겼지만 <span class="hl">판단을 남기지 않았습니다</span>. 어떤 화면에서 문제를 봤는지, 왜 그 레이아웃을 틀렸다고 판단했는지, 다음에는 무엇을 먼저 확인해야 하는지 기록하지 않았습니다. 그러니 다음 프롬프트는 길어졌지만 다음 작업은 똑똑해지지 않았습니다.</p>
{vt_timeline()}</div>'''

    my_view = f'''<div id="my-view">{h2(2, "내 관점: 프롬프트는 주문서, 리뷰 노트는 작업 기억", "idea", "좋은 프롬프트는 시작을 돕고, 좋은 리뷰 노트는 다음 실패를 줄입니다.")}
<p>프롬프트는 주문서에 가깝습니다. 이번에 무엇을 만들지, 어떤 톤을 원하는지, 어떤 제약을 지켜야 하는지 알려줍니다. 하지만 주문서는 주방에서 무슨 일이 있었는지 알려주지 않습니다. 어떤 재료가 과했는지, 어떤 조합이 실패했는지, 손님이 무엇을 남겼는지는 리뷰 노트에 가깝습니다.</p>
<p>AI와 협업할 때도 비슷했습니다. 프롬프트만 고치면 매번 새 주문을 하는 셈입니다. 리뷰 노트를 남기면 작업장이 조금씩 정리됩니다. “이 스타일이 좋다”가 아니라 “이 섹션은 390px 캡처에서 줄바꿈이 안정적이었다”처럼 쓰면, 다음 요청은 짧아져도 더 정확해집니다.</p>
{vt_comparison()}</div>'''

    example = f'''<div id="example">{h2(3, "작은 사례: 4일 동안 달라진 것", "timeline", "거창한 시스템이 아니라 세 줄의 메모가 다음 결과를 바꿨습니다.")}
<p>첫날에는 결과가 마음에 들지 않으면 곧바로 프롬프트를 늘렸습니다. “더 자연스럽게”, “더 고급스럽게”, “모드별 특성을 살려서” 같은 말을 붙였습니다. 말은 맞았지만 넓었습니다. 다음 결과가 조금 나아져도 왜 나아졌는지 설명하기 어려웠습니다.</p>
<p>둘째 날부터는 캡처와 함께 짧은 리뷰 노트를 남겼습니다. “오른쪽 카드가 390px에서 너무 좁다”, “제목 앞 아이콘이 빠지면 최신 스킬처럼 보이지 않는다”, “결론이 예제 설명처럼 끝난다”처럼 보이는 문제를 문장으로 바꿨습니다. 셋째 날에는 그 문장을 프롬프트보다 먼저 읽었습니다. 그때부터 수정이 조금 덜 흔들렸습니다.</p>
{vt_weekly_status()}
{wg_pr_writeup()}</div>'''

    how_to_start = f'''<div id="how-to-start">{h2(4, "어떻게 시작하면 좋을까", "edit", "리뷰 노트는 길게 쓰는 문서가 아니라 다음 프롬프트를 짧게 만드는 메모입니다.")}
<p>나는 리뷰 노트를 네 칸으로 쓰기 시작했습니다. 첫 칸은 관찰입니다. 두 번째는 판단입니다. 세 번째는 버린 대안입니다. 네 번째는 검증입니다. 이 네 칸이 있으면 다음 요청을 길게 쓰지 않아도 됩니다.</p>
<div class="card-grid"><article class="mini-card"><h3>관찰</h3><p>무엇을 봤는지 씁니다. “어색함”보다 “헤더 폭이 본문보다 좁다”가 좋습니다.</p></article><article class="mini-card"><h3>판단</h3><p>왜 고쳐야 하는지 씁니다. 최신 스킬의 기본 계약인지, 취향 문제인지 구분합니다.</p></article><article class="mini-card"><h3>버린 대안</h3><p>하지 않기로 한 방법을 씁니다. 그래야 다음 작업자가 같은 길을 다시 가지 않습니다.</p></article><article class="mini-card"><h3>검증</h3><p>명령 결과나 캡처처럼 다시 확인 가능한 증거를 남깁니다.</p></article></div>
<p>처음부터 완벽하게 쓰려고 하면 오래가지 않습니다. 한 줄이면 충분합니다. 중요한 것은 매번 같은 위치에 남기는 것입니다. 그래야 리뷰 노트가 감상이 아니라 작은 품질 시스템이 됩니다.</p></div>'''

    closing = f'''<div id="closing">{h2(5, "마지막 생각: 프롬프트가 짧아질 때 협업이 좋아진다", "success", "리뷰 노트가 쌓이면 요청은 짧아지고, 결과물은 더 일관됩니다.")}
<p>좋은 프롬프트를 쓰는 일은 계속 중요합니다. 하지만 반복되는 작업에서는 좋은 프롬프트보다 좋은 피드백 단위가 더 오래 갑니다. 내가 무엇을 봤고, 왜 고쳤고, 어떻게 확인했는지가 남으면 다음 생성은 과거 결과물을 복사하지 않아도 과거 판단을 이어받을 수 있습니다.</p>
<p>4일 동안 가장 크게 달라진 것은 산출물 자체보다 내 말투였습니다. “다시 잘 만들어줘”라고 말하기보다 “이 캡처에서 이 기준이 깨졌으니 이 방향으로 고쳐줘”라고 말하게 됐습니다. 그 순간 프롬프트는 길어지지 않았고, 오히려 짧아졌습니다.</p>
<p>AI 협업에서 오래 가는 것은 멋진 한 문장이 아니라 다음 사람이 같은 실수를 하지 않게 만드는 작은 기록입니다.</p></div>'''

    soft_cta = f'''{h2(6, "오늘 바로 남길 리뷰 노트", "check", "다음 작업 전에 아래 네 줄만 남겨도 충분합니다.")}
<div class="card-grid"><article class="summary-card"><h3>관찰</h3><p>어떤 화면, 문장, 검증 결과에서 문제를 봤나요?</p></article><article class="summary-card"><h3>판단</h3><p>그 문제를 왜 회귀나 품질 저하로 봤나요?</p></article><article class="summary-card"><h3>대안</h3><p>어떤 방식은 하지 않기로 했나요?</p></article><article class="summary-card"><h3>검증</h3><p>다음에는 무엇을 보면 고쳐졌다고 말할 수 있나요?</p></article></div>
<p><strong>태그:</strong> AI협업 · 프롬프트 · 리뷰노트 · 품질관리 · HTML스킬</p>'''

    return {
        "{{KICKER}}": "Blog Writer · Personal Essay",
        "{{TITLE}}": "AI 리뷰 노트를 프롬프트 앞에 두었더니 달라진 것",
        "{{HOOK}}": "프롬프트를 계속 늘리는데도 결과가 반복해서 무너질 때가 있습니다. 4일 동안 HTML 산출물을 검수하면서, 나는 더 긴 요청문보다 더 짧고 정확한 리뷰 노트가 필요하다는 것을 배웠습니다.",
        "{{META}}": '<div class="generated-row"><span>작성일 · 2026-06-07</span><span>mode · blog_writer</span><span>profile · auto</span><span>tone · personal essay</span></div><div class="lens-strip"><span>AI 협업</span><span>리뷰 노트</span><span>프롬프트</span><span>회귀 방지</span></div>',
        "{{PERSONAL_NOTE}}": personal_note,
        "{{WHY_NOW}}": why_now,
        "{{MY_VIEW}}": my_view,
        "{{EXAMPLE}}": example,
        "{{HOW_TO_START}}": how_to_start,
        "{{CLOSING_THOUGHT}}": closing,
        "{{SOFT_CTA}}": soft_cta,
        "{{SOURCE_NOTE}}": '<strong>Source note.</strong> 이 블로그 글은 2026-06-07 로컬 HTML 스킬 순차 검수 과정에서 관찰한 개인 작업 메모를 바탕으로 쓴 에세이입니다. 외부 통계나 최신 제품 사실은 사용하지 않았고, 수치 표현은 작업 회고의 설명을 위한 내부 관찰값으로 한정합니다.',
    }


def render() -> None:
    material_hashes = {}
    for rel in MODE_MATERIALS:
        p = SKILL / rel
        if not p.exists():
            raise FileNotFoundError(rel)
        material_hashes[rel] = sha_bytes(p)

    base = read(ASSETS / "base.html")
    layout = read(ASSETS / "layouts" / "personal-blog-essay.html")
    for k, v in build_mapping().items():
        layout = layout.replace(k, v)
    if re.search(r"{{[A-Z0-9_]+}}", layout):
        raise RuntimeError(f"unfilled layout placeholders: {sorted(set(re.findall(r'{{[A-Z0-9_]+}}', layout)))}")

    css = {name: read(ASSETS / name) for name in CSS_ORDER}
    core_hash = hashlib.sha256("\n".join(css[name] for name in CORE).encode("utf-8")).hexdigest()
    css["theme.css"] = f"/* adaptive-html-final-core-css-sha256: {core_hash} */\n" + css["theme.css"]

    html = base
    html = html.replace("{{TITLE}}", "AI 리뷰 노트를 프롬프트 앞에 두었더니 달라진 것")
    html = html.replace("{{DESCRIPTION}}", "blog_writer 모드로 작성한 AI 협업, 프롬프트, 리뷰 노트, 반복 품질 회귀에 대한 개인 블로그 에세이")
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
        "mode10_material_sha256": material_hashes,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    })
    integrity_path.write_text(json.dumps(prior, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    render()
    print(OUT)
