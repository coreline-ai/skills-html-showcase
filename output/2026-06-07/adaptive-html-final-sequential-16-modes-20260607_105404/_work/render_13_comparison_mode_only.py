#!/usr/bin/env python3
"""Render mode 13 comparison_html only for sequential QA.

No previous HTML body is read; no shared/common generator is imported.
The script reads only comparison layout/recipe/references and comparison-relevant vt/wg templates.
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
OUT = ROOT / "pages" / "13_comparison_internal_search_architecture_matrix.html"
SOURCES = ROOT / "sources"
SNAP = SOURCES / "assets"

MODE_MATERIALS = [
    "SKILL.md",
    "recipes/comparison.prompt.md",
    "assets/layouts/comparison-matrix.html",
    "references/layout-system.md",
    "references/writing-system.md",
    "references/quality-gates.md",
    "references/body-icon-system.md",
    "references/visual-html-system.md",
    "references/widget-system.md",
    "assets/visual-html-templates/13-comparison-cards.html",
    "assets/visual-html-templates/02-decision-tree.html",
    "assets/visual-html-templates/03-risk-matrix.html",
    "assets/widget-templates/01-three-code-approaches.html",
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


def vt_comparison_cards() -> str:
    return '''<section class="vt-shell" aria-label="internal search option comparison cards">
  <div class="vt-frame">
    <div class="cmp"><article class="cmp-card"><div class="vt-kicker">A</div><h3>Postgres FTS</h3><ul><li>운영 단순성 높음</li><li>검색 경험 확장은 제한</li></ul></article><article class="cmp-card pick"><div class="vt-kicker">B</div><h3>Managed Search</h3><ul><li>랭킹·동의어·분석 확장</li><li>동기화와 비용 관리 필요</li></ul></article><article class="cmp-card"><div class="vt-kicker">C</div><h3>Custom Hybrid</h3><ul><li>도메인 최적화 자유</li><li>팀 유지보수 부담 큼</li></ul></article></div>
  </div>
</section>'''


def vt_decision_tree() -> str:
    return '''<section class="vt-shell" aria-label="search architecture decision tree">
  <div class="vt-frame">
    <div class="vt-demo"><div class="dt-q"><article class="dt-card"><div class="vt-kicker">Q1</div><h3>검색이 핵심 제품 경험인가?</h3><p class="vt-text">검색 품질이 전환·지원 비용에 직접 영향을 주면 별도 검색 계층을 검토합니다.</p></article><div class="dt-arrow"></div><article class="dt-card"><div class="vt-kicker">Q2</div><h3>운영 인력이 충분한가?</h3><p class="vt-text">인덱스 동기화, 장애 대응, 랭킹 실험을 담당할 소유자가 필요합니다.</p></article></div><div class="dt-options"><article class="dt-card"><b>FTS로 시작</b><p class="vt-text">검색이 보조 기능이고 데이터가 한 DB에 있을 때</p></article><article class="dt-card" style="--c:var(--vt-blue)"><b>Managed Search</b><p class="vt-text">검색 경험은 중요하지만 운영 부담은 줄이고 싶을 때</p></article><article class="dt-card" style="--c:var(--vt-gold)"><b>Custom Hybrid</b><p class="vt-text">도메인 랭킹과 권한 필터가 제품 차별점일 때</p></article></div></div>
  </div>
</section>'''


def vt_risk_matrix() -> str:
    return '''<section class="vt-shell" aria-label="search architecture risk matrix">
  <div class="vt-frame">
    <div class="rm-grid"><div class="rm-cell rm-head">가능성</div><div class="rm-cell rm-head">낮음</div><div class="rm-cell rm-head">중간</div><div class="rm-cell rm-head">높음</div><div class="rm-cell rm-head">영향 큼</div><div class="rm-cell rm-risk med">색인 지연</div><div class="rm-cell rm-risk high">권한 누락</div><div class="rm-cell rm-risk high">검색 장애</div><div class="rm-cell rm-head">영향 중간</div><div class="rm-cell rm-risk low">랭킹 튜닝 지연</div><div class="rm-cell rm-risk med">동의어 누락</div><div class="rm-cell rm-risk med">비용 급증</div><div class="rm-cell rm-head">영향 작음</div><div class="rm-cell rm-risk low">관리 UI 부족</div><div class="rm-cell rm-risk low">문서화 지연</div><div class="rm-cell rm-risk low">태그 불일치</div></div>
  </div>
</section>'''


def wg_three_approaches() -> str:
    return '''<div class="wg-01" aria-labelledby="search-approach-title">
  <header class="wg-01-head"><p class="wg-01-kicker">구현 접근 비교</p><h3 id="search-approach-title" class="wg-01-title">내부 검색을 만드는 세 가지 접근</h3><p class="wg-01-lead">같은 “문서 검색” 문제라도 운영 복잡도, 검색 품질, 제품 차별화 정도에 따라 적합한 구현이 달라집니다.</p></header>
  <div class="wg-01-grid" role="list"><article class="wg-01-card" role="listitem" aria-labelledby="search-a1"><div class="wg-01-card-head"><span class="wg-01-rank" aria-hidden="true">A</span><div><h3 id="search-a1" class="wg-01-card-title">DB 내장 검색</h3><p class="wg-01-card-sub">Postgres FTS류 · 낮은 운영 부담</p></div></div><pre class="wg-01-code" tabindex="0"><code>SELECT id, title
FROM docs
WHERE search_vector @@ plainto_tsquery(:query)
ORDER BY ts_rank(search_vector, plainto_tsquery(:query)) DESC;</code></pre><div class="wg-01-cols"><div class="wg-01-pros"><p class="wg-01-coltag wg-01-coltag-good"><span aria-hidden="true">▲</span> 장점</p><ul><li>서비스 수가 늘지 않음</li><li>트랜잭션 데이터와 가까움</li></ul></div><div class="wg-01-cons"><p class="wg-01-coltag wg-01-coltag-bad"><span aria-hidden="true">▼</span> 단점</p><ul><li>고급 랭킹 실험이 제한됨</li><li>대규모 검색 전용 부하 분리가 어려움</li></ul></div></div><div class="wg-01-tags"><span class="wg-01-tag wg-01-tag-time">운영 낮음</span><span class="wg-01-tag wg-01-tag-space">품질 중간</span><span class="wg-01-tag">초기 MVP</span></div></article><article class="wg-01-card wg-01-card-pick" role="listitem" aria-labelledby="search-a2"><div class="wg-01-card-head"><span class="wg-01-rank wg-01-rank-pick" aria-hidden="true">B</span><div><h3 id="search-a2" class="wg-01-card-title">관리형 검색 서비스 <span class="wg-01-pick-badge">권장</span></h3><p class="wg-01-card-sub">Managed Search · 균형형 선택</p></div></div><pre class="wg-01-code" tabindex="0"><code>onDocumentChanged(event):
  payload = buildSearchDocument(event.record)
  search.index("docs").upsert(payload)
  audit.write("search_indexed", payload.id)</code></pre><div class="wg-01-cols"><div class="wg-01-pros"><p class="wg-01-coltag wg-01-coltag-good"><span aria-hidden="true">▲</span> 장점</p><ul><li>랭킹·동의어·필터 기능 확장</li><li>검색 부하를 별도 계층으로 분리</li></ul></div><div class="wg-01-cons"><p class="wg-01-coltag wg-01-coltag-bad"><span aria-hidden="true">▼</span> 단점</p><ul><li>색인 동기화 실패 처리가 필요</li><li>비용과 권한 필터 검증 필요</li></ul></div></div><div class="wg-01-tags"><span class="wg-01-tag wg-01-tag-time">운영 중간</span><span class="wg-01-tag wg-01-tag-space">품질 높음</span><span class="wg-01-tag">성장 단계</span></div></article><article class="wg-01-card" role="listitem" aria-labelledby="search-a3"><div class="wg-01-card-head"><span class="wg-01-rank" aria-hidden="true">C</span><div><h3 id="search-a3" class="wg-01-card-title">커스텀 하이브리드</h3><p class="wg-01-card-sub">도메인 랭킹 · 높은 자유도</p></div></div><pre class="wg-01-code" tabindex="0"><code>score = bm25(text)
score += recency_boost(doc.updated_at)
score += permission_weight(user, doc)
score += business_priority(doc.collection)</code></pre><div class="wg-01-cols"><div class="wg-01-pros"><p class="wg-01-coltag wg-01-coltag-good"><span aria-hidden="true">▲</span> 장점</p><ul><li>제품 도메인에 맞춘 랭킹 가능</li><li>실험·권한·추천 결합 자유로움</li></ul></div><div class="wg-01-cons"><p class="wg-01-coltag wg-01-coltag-bad"><span aria-hidden="true">▼</span> 단점</p><ul><li>검색팀 수준의 운영 역량 필요</li><li>문서화·테스트 부채가 빠르게 커짐</li></ul></div></div><div class="wg-01-tags"><span class="wg-01-tag wg-01-tag-time">운영 높음</span><span class="wg-01-tag wg-01-tag-space">품질 상한 높음</span><span class="wg-01-tag">차별화 단계</span></div></article></div>
</div>'''


def build_mapping() -> dict[str, str]:
    context = f'''{h2(1, "Decision Context", "decision", "작은 팀이 내부 문서·이슈·고객 메모를 검색해야 할 때, 첫 선택은 최고 성능보다 운영 가능한 균형입니다.")}
<p>비교 대상은 세 가지입니다. 첫째, 기존 데이터베이스의 full-text search를 활용하는 방식입니다. 둘째, 관리형 검색 서비스를 붙여 별도 색인 계층을 운영하는 방식입니다. 셋째, 도메인 랭킹과 권한 필터를 직접 설계하는 커스텀 하이브리드 방식입니다.</p>
<p>이 문서는 특정 제품의 가격이나 벤치마크를 단정하지 않습니다. 대신 <span class="hl">운영 복잡도, 검색 품질, 권한 안전성, 확장성, 팀 역량</span>이라는 기준으로 선택지를 비교합니다. 독자는 “지금 당장 무엇을 고를까”뿐 아니라 “언제 다음 단계로 넘어갈까”까지 판단할 수 있어야 합니다.</p>
{vt_comparison_cards()}'''

    matrix = f'''{h2(2, "Matrix", "compare", "선택지는 단일 점수가 아니라 기준별 맞교환으로 봐야 합니다. 낮음/중간/높음은 이 문서의 상대 평가입니다.")}
<div class="table-scroll"><table><caption>Internal search architecture decision matrix</caption><thead><tr><th scope="col">평가 기준</th><th scope="col">DB 내장 검색</th><th scope="col">관리형 검색 서비스</th><th scope="col">커스텀 하이브리드</th></tr></thead><tbody><tr><th scope="row">초기 구축 속도</th><td><strong>높음</strong><br>기존 DB와 가까워 시작이 빠릅니다.</td><td>중간<br>색인 파이프라인과 권한 매핑이 필요합니다.</td><td>낮음<br>랭킹·색인·관측을 모두 설계해야 합니다.</td></tr><tr><th scope="row">검색 품질 상한</th><td>중간<br>간단한 키워드 검색에는 충분하지만 실험 폭은 제한됩니다.</td><td><strong>높음</strong><br>동의어, 필터, 랭킹 조정이 비교적 쉽습니다.</td><td><strong>매우 높음</strong><br>도메인 신호를 직접 결합할 수 있습니다.</td></tr><tr><th scope="row">운영 부담</th><td><strong>낮음</strong><br>서비스 수가 늘지 않습니다.</td><td>중간<br>동기화 실패와 비용 관찰이 필요합니다.</td><td>높음<br>검색팀 수준의 운영·테스트 체계가 필요합니다.</td></tr><tr><th scope="row">권한 안전성</th><td>중간<br>DB 권한 모델과 가깝지만 검색 쿼리 정책을 정리해야 합니다.</td><td>중간~높음<br>문서 단위 권한 필터를 색인에 정확히 반영해야 합니다.</td><td>변동 큼<br>잘 만들면 강력하지만 누락 위험도 큽니다.</td></tr><tr><th scope="row">다음 단계 전환</th><td>쉬움<br>검색 로그를 모아 관리형으로 이전할 수 있습니다.</td><td><strong>쉬움</strong><br>랭킹 실험과 지표를 쌓아 고도화할 수 있습니다.</td><td>어려움<br>내부 구현에 잠금 효과가 생길 수 있습니다.</td></tr></tbody></table></div>
{vt_decision_tree()}'''

    winners = f'''{h2(3, "Winners", "success", "정답은 하나가 아니라 상황별 승자입니다. 현재 팀의 병목이 어디인지에 따라 선택지가 달라집니다.")}
<div class="card-grid"><article class="summary-card"><h3>초기 MVP · DB 내장 검색</h3><p>문서 수가 작고 검색이 보조 기능이면 DB 내장 검색으로 시작합니다. 빠르게 로그를 모으고 실제 검색어와 실패 사례를 확인하는 것이 먼저입니다.</p></article><article class="summary-card"><h3>성장 제품 · 관리형 검색 서비스</h3><p>검색 실패가 고객 문의나 전환 손실로 이어지기 시작하면 관리형 검색 계층이 균형점입니다. 운영 부담은 늘지만 검색 경험 개선 여지가 커집니다.</p></article><article class="summary-card"><h3>검색이 핵심 · 커스텀 하이브리드</h3><p>검색 랭킹 자체가 제품 차별점이고 전담 소유자가 있다면 커스텀 하이브리드가 후보가 됩니다. 단, 테스트와 감사 체계 없이는 시작하지 않는 편이 안전합니다.</p></article></div>
{vt_risk_matrix()}'''

    tradeoffs = f'''{h2(4, "Tradeoffs", "warning", "비교의 목적은 좋아 보이는 선택지를 찾는 것이 아니라, 감당할 부채를 명시하는 것입니다.")}
<p>DB 내장 검색은 시작이 빠른 대신 검색 품질 개선의 상한이 빨리 보일 수 있습니다. 관리형 검색은 균형이 좋지만 색인 동기화, 비용, 권한 필터 검증이라는 새로운 운영 항목이 생깁니다. 커스텀 하이브리드는 가장 강력해 보이지만 검색 품질을 지속적으로 실험할 팀이 없으면 부채가 됩니다.</p>
{wg_three_approaches()}
<div class="grid-2"><article class="danger"><h3>가장 위험한 실수</h3><p>검색 색인에 권한이 없는 문서를 넣고, 검색 결과에서 필터링하면 된다고 생각하는 것입니다. 권한 조건은 색인 설계와 쿼리 설계에서 모두 검증해야 합니다.</p></article><article class="good"><h3>가장 좋은 시작</h3><p>어떤 방식을 고르든 검색 로그, 0건 검색어, 클릭률, 권한 필터 실패 테스트를 먼저 남깁니다. 이 증거가 다음 아키텍처 전환의 근거가 됩니다.</p></article></div>'''

    recommendation = f'''{h2(5, "Recommendation", "metric", "이 문서의 가정에서는 관리형 검색 서비스를 1차 목표로 두되, DB 내장 검색으로 2~4주 관측을 먼저 시작하는 전략을 권장합니다.")}
<div class="card-grid"><article class="summary-card"><h3>1단계 · DB FTS로 로그 확보</h3><p>검색어, 0건 검색, 클릭 결과, 권한 필터 조건을 2~4주 수집합니다. 이 기간에는 고급 랭킹보다 관측 체계를 만드는 것이 목표입니다.</p></article><article class="summary-card"><h3>2단계 · 관리형 검색 PoC</h3><p>실제 상위 검색어와 실패 사례를 이용해 관리형 검색의 랭킹, 필터, 동의어, 색인 지연을 검증합니다. 가격·성능 수치는 사용 중인 제품에서 확인해야 합니다.</p></article><article class="summary-card"><h3>3단계 · 전환 기준 고정</h3><p>0건 검색 감소, 검색 후 클릭률 증가, 권한 필터 테스트 통과, 운영 알림 준비를 전환 기준으로 둡니다. 기준이 없으면 전환하지 않습니다.</p></article><article class="summary-card"><h3>보류 조건</h3><p>전담 소유자가 없거나 문서 권한 모델이 정리되지 않았다면 관리형 검색 도입을 늦춥니다. 먼저 권한 필터와 감사 로그를 정리해야 합니다.</p></article></div>'''

    return {
        "{{KICKER}}": "Comparison Matrix · Internal Search",
        "{{TITLE}}": "Internal Search Architecture Decision Matrix",
        "{{SUBTITLE}}": "DB 내장 검색, 관리형 검색 서비스, 커스텀 하이브리드를 작은 팀의 운영 가능성 기준으로 비교합니다.",
        "{{META}}": '<div class="generated-row"><span>작성일 · 2026-06-07</span><span>mode · comparison_html</span><span>profile · auto</span><span>scope · vendor-neutral</span></div><div class="lens-strip"><span>decision context</span><span>matrix</span><span>winners</span><span>tradeoffs</span></div>',
        "{{DECISION_CONTEXT}}": context,
        "{{MATRIX}}": matrix,
        "{{WINNERS}}": winners,
        "{{TRADEOFFS}}": tradeoffs,
        "{{RECOMMENDATION}}": recommendation,
        "{{SOURCE_NOTE}}": '<strong>Source note.</strong> 이 비교는 특정 검색 제품의 최신 가격, SLA, 성능 수치를 사용하지 않은 벤더 중립 의사결정 매트릭스입니다. 실제 도입 전에는 후보 제품의 현재 가격표, 데이터 위치, 보안 인증, 권한 필터 기능, 장애 정책을 별도로 확인해야 합니다.',
    }


def render() -> None:
    material_hashes = {}
    for rel in MODE_MATERIALS:
        p = SKILL / rel
        if not p.exists():
            raise FileNotFoundError(rel)
        material_hashes[rel] = sha_bytes(p)

    base = read(ASSETS / "base.html")
    layout = read(ASSETS / "layouts" / "comparison-matrix.html")
    for k, v in build_mapping().items():
        layout = layout.replace(k, v)
    remaining = sorted(set(re.findall(r"{{[A-Z0-9_]+}}", layout)))
    if remaining:
        raise RuntimeError(f"unfilled layout placeholders: {remaining}")

    css = {name: read(ASSETS / name) for name in CSS_ORDER}
    core_hash = hashlib.sha256("\n".join(css[name] for name in CORE).encode("utf-8")).hexdigest()
    css["theme.css"] = f"/* adaptive-html-final-core-css-sha256: {core_hash} */\n" + css["theme.css"]

    html = base
    html = html.replace("{{TITLE}}", "Internal Search Architecture Decision Matrix")
    html = html.replace("{{DESCRIPTION}}", "comparison_html 모드로 작성한 내부 검색 아키텍처 비교 매트릭스. Decision Context, Matrix, Winners, Tradeoffs, Recommendation을 포함합니다.")
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
        "mode13_material_sha256": material_hashes,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    })
    integrity_path.write_text(json.dumps(prior, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    render()
    print(OUT)
