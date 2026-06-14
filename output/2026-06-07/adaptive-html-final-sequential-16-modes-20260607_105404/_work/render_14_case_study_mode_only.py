#!/usr/bin/env python3
"""Render mode 14 case_study_html only for sequential QA.

No previous HTML body is read; no shared/common generator is imported.
The script reads only case-study layout/recipe/references and case-study relevant vt/wg templates.
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
OUT = ROOT / "pages" / "14_case_study_search_index_lag_postmortem.html"
SOURCES = ROOT / "sources"
SNAP = SOURCES / "assets"

MODE_MATERIALS = [
    "SKILL.md",
    "recipes/case-study.prompt.md",
    "assets/layouts/case-study.html",
    "references/layout-system.md",
    "references/writing-system.md",
    "references/quality-gates.md",
    "references/body-icon-system.md",
    "references/visual-html-system.md",
    "references/widget-system.md",
    "assets/visual-html-templates/12-incident-summary.html",
    "assets/visual-html-templates/04-timeline.html",
    "assets/visual-html-templates/14-process-swimlane.html",
    "assets/widget-templates/12-incident-timeline.html",
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


def vt_incident_summary() -> str:
    return '''<section class="vt-shell" aria-label="search index lag incident summary">
  <div class="vt-frame">
    <div><div class="inc-head"><div class="inc-card impact"><b>영향</b><p class="vt-text">최근 문서 18~42분 검색 누락</p></div><div class="inc-card cause"><b>원인</b><p class="vt-text">전체 평균 freshness만 관측</p></div><div class="inc-card action"><b>조치</b><p class="vt-text">tenant별 lag 알림과 재색인 큐 분리</p></div></div><ol class="tl" style="margin-top:12px"><li class="tl-item"><b>09:12 감지</b><p class="vt-text">고객지원팀이 신규 문서 검색 누락 제보</p></li><li class="tl-item"><b>09:31 완화</b><p class="vt-text">지연 tenant 우선 재색인 시작</p></li><li class="tl-item"><b>10:08 복구</b><p class="vt-text">p95 freshness 6분 이하로 회복</p></li></ol></div>
  </div>
</section>'''


def vt_timeline() -> str:
    return '''<section class="vt-shell" aria-label="postmortem timeline overview">
  <div class="vt-frame">
    <ol class="tl"><li class="tl-item"><b>08:40 배포</b><p class="vt-text">문서 권한 필터 개선 배포 후 색인 큐 처리량 하락</p></li><li class="tl-item"><b>09:12 제보</b><p class="vt-text">신규 문서가 목록에는 보이지만 검색에는 없음</p></li><li class="tl-item"><b>09:25 진단</b><p class="vt-text">전체 평균은 정상이나 특정 tenant lag가 급증</p></li><li class="tl-item"><b>10:08 안정</b><p class="vt-text">우선순위 큐와 재처리로 지연 구간 해소</p></li></ol>
  </div>
</section>'''


def vt_swimlane() -> str:
    return '''<section class="vt-shell" aria-label="incident response swimlane">
  <div class="vt-frame">
    <div class="swim"><div class="lane"><div class="lane-label">Support</div><div class="lane-step">제보 접수</div><div class="lane-step">영향 계정 묶음</div><div class="lane-step blank">—</div><div class="lane-step">고객 공지</div></div><div class="lane"><div class="lane-label">Search</div><div class="lane-step blank">—</div><div class="lane-step">lag 분석</div><div class="lane-step">재색인</div><div class="lane-step">알림 추가</div></div><div class="lane"><div class="lane-label">Platform</div><div class="lane-step">배포 확인</div><div class="lane-step">큐 처리량 점검</div><div class="lane-step">worker 증설</div><div class="lane-step blank">—</div></div><div class="lane"><div class="lane-label">PM</div><div class="lane-step blank">—</div><div class="lane-step">영향 범위 승인</div><div class="lane-step blank">—</div><div class="lane-step">재발 기준 확정</div></div></div>
  </div>
</section>'''


def wg_incident_timeline() -> str:
    return '''<div class="wg-12" aria-labelledby="search-incident-title">
  <header class="wg-12-head"><p class="wg-12-kicker">포스트모템 · SEV-3</p><h3 id="search-incident-title" class="wg-12-h">검색 인덱스 freshness 지연</h3><div class="wg-12-meta"><span class="wg-12-chip">발생 2026-06-07 09:12 KST</span><span class="wg-12-chip">지속 56분</span><span class="wg-12-chip wg-12-chip-sev">SEV-3</span><span class="wg-12-chip">담당 Search Platform</span></div></header>
  <h3 class="wg-12-h3">타임라인</h3><ol class="wg-12-tl"><li class="wg-12-tl-item"><span class="wg-12-tl-time">08:40</span><span class="wg-12-tl-dot"></span><div class="wg-12-tl-body"><strong>배포</strong> — 권한 필터 개선 배포, 색인 payload가 커지고 큐 처리량 하락</div></li><li class="wg-12-tl-item"><span class="wg-12-tl-time">09:12</span><span class="wg-12-tl-dot wg-12-dot-detect"></span><div class="wg-12-tl-body"><strong>감지</strong> — 고객지원팀이 “방금 만든 문서가 검색되지 않는다”는 제보를 incident 채널에 공유</div></li><li class="wg-12-tl-item"><span class="wg-12-tl-time">09:25</span><span class="wg-12-tl-dot"></span><div class="wg-12-tl-body"><strong>진단</strong> — 전체 평균 lag는 정상이나 상위 3개 tenant의 p95 freshness가 40분 이상임을 확인</div></li><li class="wg-12-tl-item"><span class="wg-12-tl-time">09:31</span><span class="wg-12-tl-dot wg-12-dot-mit"></span><div class="wg-12-tl-body"><strong>완화</strong> — 영향 tenant를 우선순위 큐로 이동하고 worker를 임시 증설</div></li><li class="wg-12-tl-item"><span class="wg-12-tl-time">10:08</span><span class="wg-12-tl-dot wg-12-dot-resolve"></span><div class="wg-12-tl-body"><strong>복구</strong> — 영향 tenant p95 freshness가 6분 이하로 회복, 후속 모니터링 전환</div></li></ol>
  <h3 class="wg-12-h3">영향 · 원인 · 조치</h3><div class="table-scroll"><table class="wg-12-table"><caption>Incident summary table</caption><tbody><tr><th scope="row"><span class="wg-12-rk wg-12-rk-impact">영향</span></th><td>신규·수정 문서가 검색 결과에 늦게 반영되어 고객지원 문의가 증가했습니다. 정확한 매출 영향은 확인 필요로 남겼습니다.</td></tr><tr><th scope="row"><span class="wg-12-rk wg-12-rk-cause">원인</span></th><td>전체 평균 freshness만 알림으로 보았고 tenant별 p95/p99 lag를 보지 않아 특정 고객군 지연을 늦게 발견했습니다.</td></tr><tr><th scope="row"><span class="wg-12-rk wg-12-rk-action">조치</span></th><td>tenant별 lag 알림, 재색인 우선순위 큐, 권한 필터 payload 크기 회귀 테스트를 추가했습니다.</td></tr></tbody></table></div>
  <h3 class="wg-12-h3">후속 액션 체크리스트</h3><ul class="wg-12-check"><li class="wg-12-ck"><input type="checkbox" id="wg-12-search-c1" class="wg-12-ck-in" checked><label for="wg-12-search-c1" class="wg-12-ck-lb"><span class="wg-12-ck-box"></span><span class="wg-12-ck-txt">tenant별 p95/p99 freshness 대시보드 추가 <span class="wg-12-owner">@search</span></span></label></li><li class="wg-12-ck"><input type="checkbox" id="wg-12-search-c2" class="wg-12-ck-in" checked><label for="wg-12-search-c2" class="wg-12-ck-lb"><span class="wg-12-ck-box"></span><span class="wg-12-ck-txt">재색인 우선순위 큐 분리 <span class="wg-12-owner">@platform</span></span></label></li><li class="wg-12-ck"><input type="checkbox" id="wg-12-search-c3" class="wg-12-ck-in"><label for="wg-12-search-c3" class="wg-12-ck-lb"><span class="wg-12-ck-box"></span><span class="wg-12-ck-txt">권한 필터 payload 회귀 테스트 <span class="wg-12-owner">@qa</span></span></label></li></ul>
</div>'''


def build_mapping() -> dict[str, str]:
    situation = f'''{h2(1, "Situation", "case", "신규 문서가 실제로 저장되었지만 검색 결과에는 늦게 나타난 사건입니다. 평균 지표가 정상처럼 보여 감지가 늦었습니다.")}
<p>팀은 내부 지식베이스 검색을 운영하고 있었습니다. 문서를 저장하면 이벤트가 색인 큐로 들어가고, 검색 인덱스가 갱신된 뒤 사용자에게 노출되는 구조였습니다. 사고 당일에는 권한 필터 개선 배포가 있었고, 이 변경으로 색인 payload가 커졌습니다.</p>
<p>문제는 전체 평균 freshness가 정상 범위처럼 보였다는 점입니다. 일부 대형 tenant의 큐가 밀렸지만, 작은 tenant의 빠른 처리가 평균을 끌어내렸습니다. 그래서 검색팀은 고객지원팀의 제보 전까지 “방금 만든 문서가 검색되지 않는다”는 경험을 지표로 보지 못했습니다.</p>
<div class="grid-2"><article class="mini-card"><h3>목표</h3><p>문서 저장 후 검색 반영까지 p95 10분 이하를 유지합니다.</p></article><article class="mini-card"><h3>제약</h3><p>색인 파이프라인은 운영 중단 없이 완화해야 했고, 권한 필터 정확도는 낮출 수 없었습니다.</p></article></div>
{vt_incident_summary()}'''

    timeline = f'''{h2(2, "Timeline", "timeline", "사건은 배포 직후 시작되었지만, 실제 감지는 고객지원 제보 이후에야 이루어졌습니다.")}
{wg_incident_timeline()}
{vt_timeline()}'''

    decisions = f'''{h2(3, "Decisions", "decision", "대응 중 가장 중요한 결정은 전체 재색인이 아니라 영향 tenant 우선 복구였습니다.")}
<div class="card-grid"><article class="summary-card"><h3>전체 재색인을 하지 않음</h3><p>전체 재색인은 단순해 보였지만 큐를 더 밀리게 만들 수 있었습니다. 먼저 영향 tenant만 분리해 우선순위 큐로 보냈습니다.</p></article><article class="summary-card"><h3>권한 필터 롤백 대신 payload 최적화</h3><p>권한 정확도 개선 자체는 필요한 변경이었습니다. 즉시 롤백보다 payload 크기와 큐 처리량을 줄이는 쪽을 선택했습니다.</p></article><article class="summary-card"><h3>평균 지표 폐기</h3><p>전체 평균 freshness는 운영 판단에 충분하지 않았습니다. tenant별 p95/p99와 큐 나이를 핵심 알림으로 승격했습니다.</p></article><article class="summary-card"><h3>고객 공지 범위 제한</h3><p>모든 고객에게 광범위 공지를 보내기보다 영향 tenant와 신규 문서 작성자에게 상태를 설명했습니다.</p></article></div>
{vt_swimlane()}'''

    results = f'''{h2(4, "Results", "metric", "복구는 빠르게 되었지만, 이 사건의 성과는 숫자보다 관측 기준을 바꾼 데 있습니다.")}
<div class="table-scroll"><table><caption>Postmortem result facts</caption><thead><tr><th scope="col">항목</th><th scope="col">사건 중 관찰</th><th scope="col">후속 기준</th></tr></thead><tbody><tr><th scope="row">p95 freshness</th><td>영향 tenant에서 40분 이상으로 증가</td><td>tenant별 p95 10분 초과 시 알림</td></tr><tr><th scope="row">감지 경로</th><td>고객지원팀 제보가 최초 신호</td><td>큐 나이·색인 지연 알림이 먼저 울려야 함</td></tr><tr><th scope="row">완화 방식</th><td>우선순위 큐와 worker 증설로 복구</td><td>대형 tenant 재색인 전용 경로 유지</td></tr><tr><th scope="row">사업 영향</th><td>고객 문의 증가 확인, 매출 영향은 확인 필요</td><td>영향 산정 필드를 incident template에 추가</td></tr></tbody></table></div>
<div class="card-grid"><article class="good"><h3>개선된 것</h3><p>전체 평균 대신 세그먼트별 freshness를 보게 되었습니다. 다음 지연은 고객 제보 전에 감지될 가능성이 높아졌습니다.</p></article><article class="danger"><h3>아직 남은 것</h3><p>권한 필터 변경이 색인 payload와 큐 처리량에 주는 영향을 배포 전 자동으로 예측하는 테스트는 아직 완료 전입니다.</p></article></div>'''

    lessons = f'''{h2(5, "Lessons", "learning", "회고는 감상이 아니라 다음 배포에서 다른 행동을 만들 때 완성됩니다.")}
<div class="card-grid"><article class="summary-card"><h3>평균은 사고를 숨길 수 있다</h3><p>고객군이 나뉘는 시스템에서는 평균보다 p95/p99와 segment별 지표가 먼저입니다. 특히 대형 tenant가 소수일수록 평균은 위험합니다.</p></article><article class="summary-card"><h3>freshness는 제품 경험 지표다</h3><p>검색 지연은 단순 백엔드 큐 문제가 아닙니다. 사용자는 문서가 사라진 것처럼 느끼므로 제품 품질 지표로 다뤄야 합니다.</p></article><article class="summary-card"><h3>재색인은 마지막 수단이다</h3><p>전체 재색인은 쉽게 보이지만 큐를 더 밀리게 만들 수 있습니다. 영향 범위별 우선순위 복구 경로가 필요합니다.</p></article><article class="summary-card"><h3>후속 액션은 owner와 함께 닫는다</h3><p>“알림 추가”처럼 넓게 쓰지 않고 어떤 지표, 어떤 임계치, 누가 검증하는지를 함께 적어야 합니다.</p></article></div>'''

    return {
        "{{KICKER}}": "Case Study · Search Index Lag",
        "{{TITLE}}": "검색 인덱스 지연 회고: 평균 freshness가 숨긴 문제",
        "{{SUBTITLE}}": "전체 평균 지표만 믿다가 특정 tenant의 검색 반영 지연을 늦게 발견한 사건을 상황, 타임라인, 결정, 결과, 교훈으로 정리합니다.",
        "{{META}}": '<div class="generated-row"><span>작성일 · 2026-06-07</span><span>mode · case_study_html</span><span>profile · auto</span><span>incident · SEV-3</span></div><div class="lens-strip"><span>situation</span><span>timeline</span><span>decisions</span><span>results</span><span>lessons</span></div>',
        "{{SITUATION}}": situation,
        "{{TIMELINE}}": timeline,
        "{{DECISIONS}}": decisions,
        "{{RESULTS}}": results,
        "{{LESSONS}}": lessons,
        "{{SOURCE_NOTE}}": '<strong>Source note.</strong> 이 케이스 스터디는 검색 인덱스 freshness 지연이라는 운영 상황을 설명하기 위한 내부형 회고 문서입니다. 고객 수, 금액 영향, 특정 제품 성능 수치는 단정하지 않았고, 확인되지 않은 영향은 “확인 필요”로 표시했습니다.',
    }


def render() -> None:
    material_hashes = {}
    for rel in MODE_MATERIALS:
        p = SKILL / rel
        if not p.exists():
            raise FileNotFoundError(rel)
        material_hashes[rel] = sha_bytes(p)

    base = read(ASSETS / "base.html")
    layout = read(ASSETS / "layouts" / "case-study.html")
    for k, v in build_mapping().items():
        layout = layout.replace(k, v)
    remaining = sorted(set(re.findall(r"{{[A-Z0-9_]+}}", layout)))
    if remaining:
        raise RuntimeError(f"unfilled layout placeholders: {remaining}")

    css = {name: read(ASSETS / name) for name in CSS_ORDER}
    core_hash = hashlib.sha256("\n".join(css[name] for name in CORE).encode("utf-8")).hexdigest()
    css["theme.css"] = f"/* adaptive-html-final-core-css-sha256: {core_hash} */\n" + css["theme.css"]

    html = base
    html = html.replace("{{TITLE}}", "검색 인덱스 지연 회고: 평균 freshness가 숨긴 문제")
    html = html.replace("{{DESCRIPTION}}", "case_study_html 모드로 작성한 검색 인덱스 freshness 지연 회고. 상황, 타임라인, 의사결정, 결과, 교훈을 포함합니다.")
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
        "mode14_material_sha256": material_hashes,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    })
    integrity_path.write_text(json.dumps(prior, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    render()
    print(OUT)
