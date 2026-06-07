#!/usr/bin/env python3
"""Render mode 07 manual_analysis only.

Contract for the sequential QA run:
- no previous HTML body is read as input;
- no shared/common content generator is imported;
- this script reads only the adaptive-html-final base/layout/assets plus manual_analysis recipe/reference/template assets;
- output is generated from the manual_analysis placeholder map below.
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
OUT = ROOT / "pages" / "07_manual_analysis_oncall_incident_runbook.html"
SOURCES = ROOT / "sources"
SNAP = SOURCES / "assets"

MODE_MATERIALS = [
    "SKILL.md",
    "recipes/manual-analysis.prompt.md",
    "assets/layouts/manual-analysis.html",
    "references/manual-analysis-system.md",
    "references/layout-system.md",
    "references/writing-system.md",
    "references/body-icon-system.md",
    "references/visual-html-system.md",
    "references/widget-system.md",
    "assets/visual-html-templates/01-hero-map.html",
    "assets/visual-html-templates/05-checklist-flow.html",
    "assets/visual-html-templates/06-quality-gate.html",
    "assets/visual-html-templates/09-file-tour.html",
    "assets/visual-html-templates/14-process-swimlane.html",
    "assets/visual-html-templates/02-decision-tree.html",
    "assets/visual-html-templates/03-risk-matrix.html",
    "assets/widget-templates/04-module-map.html",
    "assets/widget-templates/13-annotated-flowchart.html",
    "assets/widget-templates/16-implementation-plan.html",
    "assets/widget-templates/18-ticket-triage-board.html",
    "assets/widget-templates/11-weekly-status.html",
    "assets/widget-templates/14-feature-explainer.html",
]

CSS_ORDER = [
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
CORE = ["theme.css", "components.css", "visual-components.css", "layouts.css", "print.css"]

SECTION_ICONS = [
    '<svg viewBox="0 0 40 40" aria-hidden="true"><path class="bi-soft" d="M20 7l11 5v8c0 7-4.5 11.5-11 14-6.5-2.5-11-7-11-14v-8z"></path><path class="bi-accent-line" d="M14 20.5l4 4L27 15"></path></svg>',
    '<svg viewBox="0 0 40 40" aria-hidden="true"><path class="bi-fill" d="M12 7h12l5 5v21H12z"></path><path class="bi-line" d="M24 7v6h5M16 19h10M16 25h8"></path></svg>',
    '<svg viewBox="0 0 40 40" aria-hidden="true"><circle class="bi-soft" cx="15" cy="16" r="5"></circle><circle class="bi-soft" cx="26" cy="16" r="5"></circle><path class="bi-line" d="M8 31c1.5-5 5-8 10-8s8.5 3 10 8M22 24c3.5.5 6.2 3 7.5 7"></path></svg>',
    '<svg viewBox="0 0 40 40" aria-hidden="true"><path class="bi-line" d="M8 28h8c5 0 7-3 7-8V9"></path><path class="bi-accent-line" d="M17 15l6-6 6 6M26 28h6"></path><circle class="bi-dot" cx="8" cy="28" r="3"></circle></svg>',
    '<svg viewBox="0 0 40 40" aria-hidden="true"><path class="bi-soft" d="M20 6l10 5v7c0 7-4 12-10 15-6-3-10-8-10-15v-7z"></path><path class="bi-line" d="M15 20h10M20 15v10"></path></svg>',
    '<svg viewBox="0 0 40 40" aria-hidden="true"><rect class="bi-fill" x="10" y="8" width="20" height="25" rx="4"></rect><path class="bi-accent-line" d="M15 16l2 2 4-5M15 24l2 2 4-5"></path><path class="bi-line" d="M23 17h4M23 25h4"></path></svg>',
    '<svg viewBox="0 0 40 40" aria-hidden="true"><path class="bi-fill" d="M10 9h15l5 5v17H10z"></path><path class="bi-line" d="M25 9v6h5M15 20h10M15 26h8"></path><circle class="bi-dot" cx="12" cy="10" r="2.5"></circle></svg>',
    '<svg viewBox="0 0 40 40" aria-hidden="true"><path class="bi-soft" d="M20 6l13 14-13 14L7 20z"></path><path class="bi-line" d="M15 20h10M20 15v10"></path></svg>',
    '<svg viewBox="0 0 40 40" aria-hidden="true"><path class="bi-soft" d="M20 7l13 23H7z"></path><path class="bi-accent-line" d="M20 15v8"></path><circle class="bi-accent" cx="20" cy="28" r="1.8"></circle></svg>',
    '<svg viewBox="0 0 40 40" aria-hidden="true"><circle class="bi-soft" cx="20" cy="20" r="13"></circle><path class="bi-line" d="M20 12v9l6 4M9 31h22"></path></svg>',
    '<svg viewBox="0 0 40 40" aria-hidden="true"><circle class="bi-fill" cx="17" cy="17" r="8"></circle><path class="bi-accent-line" d="M23 23l8 8M14 17h6"></path></svg>',
    '<svg viewBox="0 0 40 40" aria-hidden="true"><path class="bi-line" d="M12 8v24"></path><path class="bi-soft" d="M13 9h16l-3 6 3 6H13z"></path><path class="bi-line" d="M13 9h16l-3 6 3 6H13"></path></svg>',
]


def section_icon(n: int) -> str:
    return SECTION_ICONS[(n - 1) % len(SECTION_ICONS)]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def h2(n: int, title: str, sub: str, icon: str = "body-icon--sm") -> str:
    return (
        f'<h2><span class="body-icon {icon}">{section_icon(n)}</span>'
        f'<span class="num">{n}</span>{title}</h2>\n'
        f'<p class="h2-sub">{sub}</p>'
    )


def ul(items: list[str], cls: str = "") -> str:
    c = f' class="{cls}"' if cls else ""
    return f"<ul{c}>" + "".join(f"<li>{item}</li>" for item in items) + "</ul>"


def hero_map() -> str:
    return '''<section class="vt-shell" aria-label="역할별 매뉴얼 지도">
  <div class="vt-frame">
    <div class="vt-demo"><div class="hm-grid">
      <article class="hm-card"><div class="vt-kicker">Reader</div><h3>내 역할부터 고른다</h3><p class="vt-text">온콜 엔지니어·Incident Commander·서비스 오너·커뮤니케이션 오너만 원문 역할로 확인됐다.</p></article>
      <article class="hm-card" style="--c:var(--vt-blue)"><div class="vt-kicker">Path</div><h3>첫 30분을 먼저 끝낸다</h3><p class="vt-text">인지→상황실→완화/롤백→고객 영향 메모까지 성공 기준을 앞에 둔다.</p></article>
      <article class="hm-card" style="--c:var(--vt-green)"><div class="vt-kicker">Audit</div><h3>UNKNOWN은 추측하지 않는다</h3><p class="vt-text">SLA·권한 정책·법무 문구는 원문 밖 정보라 소유자 검토로 남긴다.</p></article>
    </div><div class="hm-result"><b>판정: 실행 매뉴얼 초안으로는 사용 가능</b><span>단, P1 SLA와 rollback 승인권자가 확정되기 전까지 최종본으로 배포하면 안 된다.</span></div></div>
  </div>
</section>'''


def checklist_flow() -> str:
    return '''<section class="vt-shell" aria-label="첫 성공 경로 체크리스트">
  <div class="vt-frame">
    <div class="cf">
      <div class="cf-item"><span class="cf-check">✓</span><div><b>Alert ACK</b><p class="vt-text">5분 안에 알림을 인지하고 incident id를 만든다.</p></div><span class="cf-state">PASS</span></div>
      <div class="cf-item"><span class="cf-check">✓</span><div><b>Role assign</b><p class="vt-text">IC·서비스 오너·커뮤니케이션 오너를 비워두지 않는다.</p></div><span class="cf-state">PASS</span></div>
      <div class="cf-item"><span class="cf-check">!</span><div><b>Rollback check</b><p class="vt-text">승인권자가 UNKNOWN이면 완화 조치와 에스컬레이션으로 분기한다.</p></div><span class="cf-state">REVIEW</span></div>
    </div>
  </div>
</section>'''


def quality_gate() -> str:
    return '''<section class="vt-shell" aria-label="사전조건 및 안전 게이트">
  <div class="vt-frame">
    <div><div class="qg-grid">
      <div class="qg-card"><b>권한</b><p class="vt-text">배포 롤백 권한 보유 여부를 확인한다. 원문상 권한 정책은 UNKNOWN.</p></div>
      <div class="qg-card warn"><b>데이터</b><p class="vt-text">데이터 삭제·스키마 변경은 이 런북 범위 밖이다. 수행 금지 라벨을 붙인다.</p></div>
      <div class="qg-card"><b>고객 영향</b><p class="vt-text">영향 범위가 불명확하면 status update보다 내부 확인을 먼저 한다.</p></div>
      <div class="qg-card warn"><b>법무 문구</b><p class="vt-text">외부 공지 문구의 승인 기준은 원문에 없어 owner review로 남긴다.</p></div>
    </div><div class="qg-final">PRE-FLIGHT: 권한·영향·롤백·공지 승인 중 하나라도 UNKNOWN이면 단독 조치 금지</div></div>
  </div>
</section>'''


def file_tour() -> str:
    return '''<section class="vt-shell" aria-label="원문 파일 투어">
  <div class="vt-frame">
    <div class="ft">
      <article class="ft-card"><div class="ft-head"><span>oncall-runbook.md</span><span>core</span></div><div class="ft-body"><p class="vt-text">P1 인지·역할 지정·상황실 오픈 절차.</p><div class="ft-note"><b>원문 위치</b><br>§1.1~§1.4 · SLA 문장은 승인 대기.</div></div></article>
      <article class="ft-card"><div class="ft-head"><span>rollback-checklist.md</span><span>risk</span></div><div class="ft-body"><p class="vt-text">최근 배포 식별과 롤백 실행 체크.</p><div class="ft-note"><b>원문 위치</b><br>§3 · 승인권자 표현이 모호함.</div></div></article>
      <article class="ft-card"><div class="ft-head"><span>incident-template.md</span><span>comms</span></div><div class="ft-body"><p class="vt-text">상태 업데이트와 핸드오프 문장.</p><div class="ft-note"><b>원문 위치</b><br>§2 · 고객 공지 주기 표현이 오래된 정책일 수 있음.</div></div></article>
    </div>
  </div>
</section>'''


def swimlane() -> str:
    return '''<section class="vt-shell" aria-label="운영 역할별 swimlane">
  <div class="vt-frame">
    <div class="swim">
      <div class="lane"><div class="lane-label">On-call</div><div class="lane-step">ACK</div><div class="lane-step">진단</div><div class="lane-step">완화</div><div class="lane-step">핸드오프</div></div>
      <div class="lane"><div class="lane-label">IC</div><div class="lane-step blank">—</div><div class="lane-step">역할 지정</div><div class="lane-step">분기 결정</div><div class="lane-step">회고 오너</div></div>
      <div class="lane"><div class="lane-label">Service</div><div class="lane-step blank">—</div><div class="lane-step">최근 배포 확인</div><div class="lane-step">롤백 승인</div><div class="lane-step">재발 방지</div></div>
      <div class="lane"><div class="lane-label">Comms</div><div class="lane-step blank">—</div><div class="lane-step">영향 문장</div><div class="lane-step">공지</div><div class="lane-step">종료 안내</div></div>
    </div>
  </div>
</section>'''


def decision_tree() -> str:
    return '''<section class="vt-shell" aria-label="분기 결정 가이드">
  <div class="vt-frame">
    <div class="vt-demo"><div class="dt-q">
      <article class="dt-card"><div class="vt-kicker">Q1</div><h3>고객 영향이 확인됐나?</h3><p class="vt-text">아니오면 로그·대시보드·최근 배포 확인을 먼저 완료한다.</p></article>
      <div class="dt-arrow"></div>
      <article class="dt-card"><div class="vt-kicker">Q2</div><h3>롤백 권한이 명확한가?</h3><p class="vt-text">UNKNOWN이면 IC가 서비스 오너를 호출하고 임시 완화로 전환한다.</p></article>
    </div><div class="dt-options">
      <article class="dt-card"><b>완화</b><p class="vt-text">feature flag, traffic drain, rate limit 조치.</p></article>
      <article class="dt-card" style="--c:var(--vt-gold)"><b>롤백</b><p class="vt-text">승인권자·대상 배포·검증 지표가 모두 있을 때.</p></article>
      <article class="dt-card" style="--c:var(--vt-green)"><b>이관</b><p class="vt-text">권한·법무·SLA가 원문 밖이면 owner review.</p></article>
    </div></div>
  </div>
</section>'''


def risk_matrix() -> str:
    return '''<section class="vt-shell" aria-label="매뉴얼 결함 리스크 매트릭스">
  <div class="vt-frame">
    <div class="rm-grid">
      <div class="rm-cell rm-head">가능성</div><div class="rm-cell rm-head">낮음</div><div class="rm-cell rm-head">중간</div><div class="rm-cell rm-head">높음</div>
      <div class="rm-cell rm-head">영향 큼</div><div class="rm-cell rm-risk med">공지 승인 UNKNOWN</div><div class="rm-cell rm-risk high">롤백 승인권자 모호</div><div class="rm-cell rm-risk high">P1 SLA 누락</div>
      <div class="rm-cell rm-head">영향 중간</div><div class="rm-cell rm-risk low">문구 주기 낡음</div><div class="rm-cell rm-risk med">핸드오프 기준 부족</div><div class="rm-cell rm-risk med">alert storm 분기 부족</div>
      <div class="rm-cell rm-head">영향 작음</div><div class="rm-cell rm-risk low">용어 약어 미정리</div><div class="rm-cell rm-risk low">템플릿 링크 미기재</div><div class="rm-cell rm-risk low">예상 화면 누락</div>
    </div>
  </div>
</section>'''


def wg_module_map() -> str:
    return '''<section class="wg-04" aria-labelledby="manual-doc-map-title">
  <header class="wg-04-head">
    <p class="wg-04-kicker">문서 묶음 지도</p>
    <h3 id="manual-doc-map-title" class="wg-04-title">온콜 런북 원문 연결 경로</h3>
    <p class="wg-04-lead">원문 파일은 절차·롤백·공지 템플릿으로 나뉘어 있다. <strong class="wg-04-crit-word">붉은 경로</strong>는 사고 대응 중 반드시 추적해야 하는 핵심 경로다.</p>
  </header>
  <div class="wg-04-path" role="note"><span class="wg-04-path-label">핵심 경로</span><span class="wg-04-path-chain"><code>alert-policy.md</code> → <code>oncall-runbook.md</code> → <code>rollback-checklist.md</code> → <code>incident-template.md</code></span><span class="wg-04-path-note">목록 밖 SLA·권한·법무 문구는 본문에서 UNKNOWN으로만 표시한다.</span></div>
</section>'''


def wg_weekly_status() -> str:
    return '''<section class="wg-11" aria-labelledby="manual-status-title">
  <header class="wg-11-head"><p class="wg-11-kicker">운영 상태</p><h3 id="manual-status-title" class="wg-11-h">런북 확정 준비도</h3><p class="wg-11-lead">초안은 실행 가능하지만 승인·권한·SLA 확인이 남아 있다.</p></header>
  <div class="wg-11-kpis">
    <div class="wg-11-kpi wg-11-kpi-good"><span class="wg-11-kpi-v">4</span><span class="wg-11-kpi-l">작성 가능 레시피</span></div>
    <div class="wg-11-kpi wg-11-kpi-prog"><span class="wg-11-kpi-v">3</span><span class="wg-11-kpi-l">증상 시나리오</span></div>
    <div class="wg-11-kpi wg-11-kpi-risk"><span class="wg-11-kpi-v wg-11-warn">3</span><span class="wg-11-kpi-l">승인 대기</span></div>
    <div class="wg-11-kpi"><span class="wg-11-kpi-v">0</span><span class="wg-11-kpi-l">원문 밖 확정</span></div>
  </div>
</section>'''


def wg_flow() -> str:
    return '''<section class="wg-13-fc" aria-label="트러블슈팅 플로우차트">
  <h3 class="wg-13-h">증상 기반 복구 흐름 <span class="wg-13-sub">증상→원인→진단→복구</span></h3>
  <div class="wg-13-flow">
    <a href="#symptom-alert-storm" class="wg-13-node wg-13-node--start"><span class="wg-13-step">시작</span>증상 선택</a>
    <span class="wg-13-arrow" aria-hidden="true">↓</span>
    <a href="#symptom-rollback-blocked" class="wg-13-node"><span class="wg-13-step">1</span>최근 배포/권한 확인</a>
    <span class="wg-13-arrow" aria-hidden="true">↓</span>
    <a href="#symptom-impact-unknown" class="wg-13-node wg-13-node--decide"><span class="wg-13-step">2</span>고객 영향 확인?</a>
    <div class="wg-13-paths"><div class="wg-13-path wg-13-path--fail"><span class="wg-13-edge">아니오 → 진단 보강</span><a href="#source-limits" class="wg-13-node wg-13-node--fail"><span class="wg-13-step">!</span>UNKNOWN 기록</a></div><div class="wg-13-path wg-13-path--ok"><span class="wg-13-edge">예 → 대응 진행</span><a href="#operations-runbook" class="wg-13-node wg-13-node--end"><span class="wg-13-step">끝</span>런북 실행</a></div></div>
  </div>
</section>'''


def wg_implementation_plan() -> str:
    return '''<section class="wg-16" aria-labelledby="manual-implementation-title">
  <header class="wg-16-head"><p class="wg-16-kicker">확정 계획</p><h3 id="manual-implementation-title" class="wg-16-title">Owner review 이후 발행 순서</h3><p class="wg-16-lead">SLA·권한·공지 승인 문구를 확정한 뒤 v1.0 매뉴얼로 태그한다.</p></header>
  <div class="wg-16-table-wrap table-scroll"><table class="mobile-card-table"><caption>매뉴얼 확정 작업 계획</caption><thead><tr><th>순서</th><th>작업</th><th>소유자</th><th>완료 기준</th></tr></thead><tbody>
    <tr><td data-label="순서">1</td><td data-label="작업">P1/P2 SLA 문구 승인</td><td data-label="소유자">Service owner</td><td data-label="완료 기준">oncall-runbook.md §1.2 갱신</td></tr>
    <tr><td data-label="순서">2</td><td data-label="작업">rollback 승인권자 확정</td><td data-label="소유자">Incident Commander</td><td data-label="완료 기준">rollback-checklist.md §3 역할 문구 교체</td></tr>
    <tr><td data-label="순서">3</td><td data-label="작업">외부 공지 문구 검토</td><td data-label="소유자">Comms owner</td><td data-label="완료 기준">incident-template.md §2 승인 기록</td></tr>
  </tbody></table></div>
</section>'''


def wg_triage() -> str:
    return '''<section class="wg-18-board" aria-label="사고 대응 티켓 보드">
  <div class="wg-18-cols" role="list">
    <div class="wg-18-col" role="listitem"><div class="wg-18-col-head"><span class="wg-18-dot" aria-hidden="true"></span><h3 class="wg-18-col-name">대기</h3><span class="wg-18-count" aria-label="2건">2</span></div><article class="wg-18-card"><div class="wg-18-card-top"><span class="wg-18-id">RUN-01</span><span class="wg-18-pri wg-18-pri--high">HIGH</span></div><p class="wg-18-card-title">P1 SLA 확정 필요</p><div class="wg-18-meta"><span class="wg-18-tag">UNKNOWN</span><span class="wg-18-assignee">Service owner</span></div></article><article class="wg-18-card"><div class="wg-18-card-top"><span class="wg-18-id">RUN-02</span><span class="wg-18-pri wg-18-pri--mid">MID</span></div><p class="wg-18-card-title">공지 승인 문구 검토</p><div class="wg-18-meta"><span class="wg-18-tag">owner review</span><span class="wg-18-assignee">Comms</span></div></article></div>
    <div class="wg-18-col" role="listitem"><div class="wg-18-col-head"><span class="wg-18-dot wg-18-dot--done" aria-hidden="true"></span><h3 class="wg-18-col-name">사용 가능</h3><span class="wg-18-count" aria-label="2건">2</span></div><article class="wg-18-card wg-18-card--done"><div class="wg-18-card-top"><span class="wg-18-id">RUN-03</span><span class="wg-18-pri wg-18-pri--low">OK</span></div><p class="wg-18-card-title">ACK와 상황실 오픈 절차</p><div class="wg-18-meta"><span class="wg-18-tag">FACT</span><span class="wg-18-assignee">On-call</span></div></article><article class="wg-18-card wg-18-card--done"><div class="wg-18-card-top"><span class="wg-18-id">RUN-04</span><span class="wg-18-pri wg-18-pri--low">OK</span></div><p class="wg-18-card-title">핸드오프 템플릿 초안</p><div class="wg-18-meta"><span class="wg-18-tag">FACT</span><span class="wg-18-assignee">IC</span></div></article></div>
  </div>
</section>'''


def build_sections() -> dict[str, str]:
    toc = '''<div class="toc-map">
  <span class="label">매뉴얼 실행 목차</span>
  <p>출처와 역할을 먼저 고정한 뒤 실행·안전·문제 해결·감사로 이동합니다.</p>
  <div class="toc-pills">
    <a class="toc-pill" href="#source-version"><b>1</b>출처·버전</a>
    <a class="toc-pill" href="#role-router"><b>2</b>역할 경로</a>
    <a class="toc-pill" href="#first-success"><b>3</b>첫 성공</a>
    <a class="toc-pill" href="#safety"><b>4</b>안전</a>
    <a class="toc-pill" href="#recipes"><b>5</b>레시피</a>
    <a class="toc-pill" href="#troubleshooting"><b>8</b>문제 해결</a>
    <a class="toc-pill" href="#manual-audit"><b>10</b>감사</a>
    <a class="toc-pill" href="#source-limits"><b>11</b>한계</a>
  </div>
</div>'''

    verdict = f'''{h2(1, "실행 가능 판정", "역할별 실행 경로는 만들 수 있지만, 승인 대기 항목이 남아 최종본은 아니다.")}
{hero_map()}
<div class="manual-audit-grid">
  <article class="manual-card manual-safe"><span class="manual-label">FACT</span><h3>초안 사용 범위</h3><p>ACK, 상황실 오픈, 역할 지정, 핸드오프는 입력 원문에 근거가 있어 실행 초안으로 전환할 수 있다. 각 절차는 원문 위치를 함께 남겨 갱신 추적이 가능하다.</p></article>
  <article class="manual-card manual-risk"><span class="manual-label">OWNER REVIEW</span><h3>최종 발행 차단점</h3><p>P1 SLA, rollback 승인권자, 외부 공지 승인 문구가 확정되지 않았다. 이 세 항목은 사고 중 의사결정 지연을 만들 수 있어 v1.0 발행 전 필수 보완이다.</p></article>
  <article class="manual-card manual-unknown"><span class="manual-label">UNKNOWN</span><h3>추측 금지 영역</h3><p>실제 권한 정책, 법무 문구, 고객별 SLA는 제공 원문에 없다. 본문은 확인 불가로 표시하고 소유자 검토 항목으로만 둔다.</p></article>
</div>'''

    source_version = f'''{h2(2, "Source & Version Snapshot", "어떤 원문을 기준으로 했고 무엇이 승인 대기인지 먼저 고정한다.")}
<div class="manual-reference-grid">
  <article class="manual-card"><span class="manual-label">source snapshot</span><h3>입력 묶음</h3><p><code>oncall-runbook.md v0.9 draft</code>, <code>alert-policy.md</code>, <code>rollback-checklist.md</code>, <code>incident-template.md</code>를 기준으로 재구성했다. 목록 밖 제품 버전·권한 정책·SLA 문구는 본문에 확정값으로 쓰지 않는다.</p></article>
  <article class="manual-card manual-risk"><span class="manual-label">owner review</span><h3>승인 대기</h3><p><code>oncall-runbook.md §1.2</code>의 P1 응답 시간, <code>rollback-checklist.md §3</code>의 승인권자, <code>incident-template.md §2</code>의 고객 공지 문구가 검토 대기다.</p></article>
  <article class="manual-card manual-unknown"><span class="manual-label">UNKNOWN</span><h3>확인 불가</h3><p>실제 온콜 권한 부여 방식, 법무 승인 프로세스, 고객별 SLA 예외는 제공 원문에 없다. 해당 값은 소유자 확인 전까지 실행 절차에 확정 조건으로 넣지 않는다.</p></article>
</div>
{wg_module_map()}'''

    role_router = f'''{h2(3, "Reader Role Router", "독자가 자신의 역할에서 시작하도록 원문에 있는 역할만 배치한다.")}
<div class="manual-role-grid">
  <article class="manual-role"><span class="manual-label">On-call engineer</span><h3>먼저 읽기</h3><p>§4 첫 성공 경로와 §6 레시피 1·2를 먼저 수행한다. 롤백 승인권자가 비어 있으면 직접 실행하지 말고 IC 호출로 이관한다.</p></article>
  <article class="manual-role"><span class="manual-label">Incident Commander</span><h3>의사결정</h3><p>역할 지정, 고객 영향 판정, 완화/롤백 분기를 맡는다. UNKNOWN 항목이 나오면 §10 감사 항목으로 기록하고 owner review 티켓을 만든다.</p></article>
  <article class="manual-role"><span class="manual-label">Service owner</span><h3>기술 승인</h3><p>최근 배포와 rollback 대상 commit을 확인한다. 승인 문구가 모호하면 rollback 대신 feature flag나 traffic drain 완화부터 선택한다.</p></article>
  <article class="manual-role"><span class="manual-label">Communications owner</span><h3>고객 문장</h3><p>고객 영향이 확인된 뒤에만 상태 업데이트를 낸다. 법무 문구가 원문 밖이면 “검토 중” 상태로 내부 업데이트를 먼저 작성한다.</p></article>
</div>'''

    first_success = f'''{h2(4, "First Success Path", "30분 안에 사고 대응 루프가 작동하는 상태까지 도달한다.")}
{checklist_flow()}
<div class="manual-step-grid">
  <article class="manual-step manual-safe"><span class="manual-label">1 · ACK</span><h3>5분 안에 알림 인지</h3><p>Pager 알림을 확인하고 incident id를 만든다. 성공 기준은 담당자와 타임스탬프가 채널 상단에 남는 것이다.</p></article>
  <article class="manual-step"><span class="manual-label">2 · Room</span><h3>상황실과 역할 지정</h3><p>IC, 서비스 오너, 커뮤니케이션 오너를 지정한다. 역할이 비면 조치보다 호출이 먼저이며, 이후 판단 기록은 incident-template.md에 남긴다.</p></article>
  <article class="manual-step manual-risk"><span class="manual-label">3 · Mitigate</span><h3>완화 또는 rollback 분기</h3><p>권한과 승인권자가 명확하면 rollback을 검토한다. 둘 중 하나가 UNKNOWN이면 feature flag, traffic drain, rate limit 같은 되돌릴 수 있는 완화로 시작한다.</p></article>
</div>'''

    safety = f'''{h2(5, "Prerequisites & Safety", "실행 전에 권한·위험·복구 가능성을 확인한다.")}
{quality_gate()}
<div class="manual-audit-grid">
  <article class="manual-card manual-risk"><span class="manual-label">서비스 중단</span><h3>롤백은 승인 후 실행</h3><p>최근 배포가 원인이라는 근거와 승인권자가 모두 확인되어야 한다. 둘 중 하나라도 빠지면 고객 영향 축소 조치로 분기한다.</p></article>
  <article class="manual-card manual-risk"><span class="manual-label">권한 변경</span><h3>권한 정책은 UNKNOWN</h3><p>원문은 누가 rollback 권한을 갖는지 확정하지 않는다. 따라서 개인 계정으로 권한을 임시 상승하는 절차는 이 매뉴얼에 포함하지 않는다.</p></article>
  <article class="manual-card manual-safe"><span class="manual-label">복구 조건</span><h3>되돌릴 수 있는 조치 우선</h3><p>feature flag, traffic drain, rate limit은 상태 확인 후 되돌릴 수 있다. 데이터 삭제·스키마 변경은 제공 원문 밖이며 수행 금지다.</p></article>
</div>'''

    recipes_rows = [
        ("P1 alert ACK", "알림 인지와 incident id 생성", "Pager 접근·온콜 담당자 확인", "알림 ACK → incident 채널 생성 → 타임스탬프 기록", "5분 안에 담당자/채널/시간이 보임", "ACK 취소가 아니라 IC에게 이관 · 2분", "alert-policy.md §1"),
        ("Incident room open", "역할과 기록 위치 고정", "IC 후보·서비스 오너 호출 가능", "채널 고정 → IC 지정 → 역할 표기 → 고객 영향 칸 생성", "역할 4종 중 빈 항목 없음", "역할 미지정 시 escalation ping · 3분", "oncall-runbook.md §1.1"),
        ("Rollback last deploy", "최근 배포 되돌리기", "승인권자·대상 배포·검증 지표 확인", "대상 배포 식별 → 승인 확인 → rollback → 지표 비교", "에러율/latency가 기준선으로 회복", "forward fix 또는 이전 revision 재배포 · 10분", "rollback-checklist.md §3"),
        ("Status update", "내부/외부 상태 문장 작성", "고객 영향과 승인 문구 확인", "영향 범위 작성 → IC 검토 → comms owner 게시", "동일 채널에 다음 업데이트 시간이 남음", "외부 공지 보류 후 내부 업데이트만 유지 · 5분", "incident-template.md §2"),
    ]
    trs = "".join(
        f'<tr><td data-label="레시피">{a}</td><td data-label="목적">{b}</td><td data-label="사전조건">{c}</td><td data-label="절차">{d}</td><td data-label="완료 기준">{e}</td><td data-label="롤백/근거">{f}<br><code>{g}</code></td></tr>'
        for a, b, c, d, e, f, g in recipes_rows
    )
    recipes = f'''{h2(6, "Task Recipes", "반복 작업은 6필드 표준으로 실행 가능하게 만든다.")}
<div class="table-scroll"><table class="mobile-card-table"><caption>온콜 사고 대응 표준 레시피 4종</caption><thead><tr><th>레시피</th><th>목적</th><th>사전조건</th><th>절차</th><th>완료 기준</th><th>롤백/근거</th></tr></thead><tbody>{trs}</tbody></table></div>'''

    reference_extract = f'''{h2(7, "Reference Extract", "원문 추적 가능한 범위와 목록 밖 정보를 분리한다.")}
{file_tour()}
<div class="manual-reference-grid">
  <article class="manual-card"><span class="manual-label">파일 목록</span><h3>분석에 사용한 원문</h3>{ul(["oncall-runbook.md v0.9 draft — ACK/상황실/역할 지정", "alert-policy.md — 알림 우선순위와 ACK", "rollback-checklist.md — 최근 배포 식별과 rollback 체크", "incident-template.md — 공지/핸드오프 문장"], "col-list")}</article>
  <article class="manual-card manual-unknown"><span class="manual-label">목록 밖</span><h3>본문에 확정하지 않은 정보</h3><p>실제 고객별 SLA, 법무 승인 문구, 계정 권한 정책, 배포 시스템 명령어는 입력 원문에 없다. 본문은 실행 순서만 제공하고 환경별 명령은 owner review 후 추가한다.</p></article>
</div>'''

    decision = f'''{h2(8, "Decision Guide", "누가 처리하고 언제 이관할지 질문 단위로 고른다.")}
{decision_tree()}
<div class="manual-reference-grid">
  <article class="manual-card"><span class="manual-label">경로 A</span><h3>고객 영향 없음</h3><p>최근 배포·로그·알림 상관관계를 먼저 본다. 고객 영향이 확인되지 않으면 외부 공지는 보류하고 내부 진단 루프를 유지한다.</p></article>
  <article class="manual-card manual-risk"><span class="manual-label">경로 B</span><h3>고객 영향 있음</h3><p>IC가 서비스 오너와 comms owner를 함께 호출한다. 이관 시 영향 범위, 시작 시각, 현재 완화 조치, 다음 업데이트 시간을 첨부한다.</p></article>
  <article class="manual-card manual-unknown"><span class="manual-label">경로 C</span><h3>승인권자 불명확</h3><p>rollback을 단독 실행하지 않는다. 원문 근거 <code>rollback-checklist.md §3</code>을 붙여 owner review로 넘기고 되돌릴 수 있는 완화만 수행한다.</p></article>
</div>'''

    troubleshooting = f'''{h2(9, "Troubleshooting", "증상에서 원인·진단·복구까지 4단 구조로 따라간다.")}
{wg_flow()}
<div class="manual-trouble-grid">
  <article id="symptom-alert-storm" class="manual-trouble"><span class="manual-label">증상 1</span><h3>Alert storm</h3><p><b>가능 원인:</b> 배포 후 오류율 증가 또는 알림 임계값 과민. <b>진단 순서:</b> 최근 배포, 에러율, 고객 영향, 중복 알림 여부. <b>복구:</b> 알림 그룹핑 후 IC가 단일 incident로 병합한다.</p></article>
  <article id="symptom-rollback-blocked" class="manual-trouble manual-risk"><span class="manual-label">증상 2</span><h3>Rollback blocked</h3><p><b>가능 원인:</b> 승인권자 또는 대상 배포가 불명확. <b>진단 순서:</b> rollback-checklist.md §3, 최근 release id, 서비스 오너 응답. <b>복구:</b> feature flag/traffic drain으로 임시 완화한다.</p></article>
  <article id="symptom-impact-unknown" class="manual-trouble manual-unknown"><span class="manual-label">증상 3</span><h3>Customer impact unknown</h3><p><b>가능 원인:</b> 대시보드 지표와 고객 신고가 일치하지 않음. <b>진단 순서:</b> SLO 패널, support ticket, 로그 샘플. <b>복구:</b> 외부 공지는 보류하고 내부 상태 업데이트를 15분 주기로 유지한다.</p></article>
</div>'''

    operations = f'''{h2(10, "Operations Runbook", "일일·주간·릴리스 전 점검과 이상 시 분기를 연결한다.")}
{swimlane()}
<div class="manual-runbook-grid">
  <article class="manual-card"><span class="manual-label">Daily</span><h3>온콜 교대 전</h3><p>담당자, escalation channel, Pager 수신 상태를 확인한다. 이상 시 IC 후보에게 즉시 이관하고 교대 완료를 보류한다.</p></article>
  <article class="manual-card"><span class="manual-label">Weekly</span><h3>런북 링크 점검</h3><p>원문 4종 링크와 템플릿 접근 권한을 확인한다. 권한 오류가 있으면 다음 사고 전까지 service owner가 수정한다.</p></article>
  <article class="manual-card manual-risk"><span class="manual-label">Pre-release</span><h3>rollback 경로 리허설</h3><p>최근 배포 id, 검증 지표, 승인권자를 사전에 확인한다. 승인권자 UNKNOWN이면 release go/no-go에 리스크로 등록한다.</p></article>
</div>
{wg_triage()}'''

    audit = f'''{h2(11, "Manual Audit", "매뉴얼 자체의 결함은 위치와 유형을 붙여 고친다.")}
{risk_matrix()}
<div class="manual-audit-grid">
  <article class="manual-card manual-risk"><span class="manual-label">누락</span><h3>P1 SLA 미확정</h3><p>원문 위치: <code>oncall-runbook.md §1.2</code>. 응답 시간과 고객 공지 주기가 승인 대기라 사고 중 기대치를 맞추기 어렵다.</p></article>
  <article class="manual-card manual-risk"><span class="manual-label">모호</span><h3>rollback 승인권자 불명확</h3><p>원문 위치: <code>rollback-checklist.md §3</code>. “서비스 오너 확인” 문구만 있어 IC와 서비스 오너 중 누가 최종 승인하는지 확인 불가다.</p></article>
  <article class="manual-card manual-unknown"><span class="manual-label">낡음 가능</span><h3>공지 주기 정책 검토 필요</h3><p>원문 위치: <code>incident-template.md §2</code>. 고객 공지 주기 표현이 현재 정책과 같은지 원문만으로 확인 불가다.</p></article>
</div>
{wg_weekly_status()}'''

    next_actions = f'''{h2(12, "Next Actions & Source Limits", "초안을 확정하기 위한 남은 작업과 확인 불가 항목을 닫는다.")}
{wg_implementation_plan()}
<div id="source-limits" class="manual-reference-grid">
  <article class="manual-card"><span class="manual-label">다음 행동</span><h3>v1.0 확정 순서</h3>{ul(["Service owner가 P1/P2 SLA와 rollback 승인권자를 확정한다.", "Comms owner가 외부 공지 문구와 다음 업데이트 주기를 승인한다.", "On-call engineer가 첫 성공 경로를 dry-run으로 1회 수행한다.", "IC가 UNKNOWN 항목을 모두 해소한 뒤 manual status를 owner review에서 확정으로 바꾼다."])}</article>
  <article class="manual-card manual-unknown"><span class="manual-label">Source Limits</span><h3>확인하지 못한 항목</h3><p>실제 제품 버전, 계정 권한 정책, 고객별 SLA 예외, 법무 승인 문구, 배포 시스템 명령어는 입력 원문에 없다. 이 HTML은 소유자 검토 전 실행 초안이며 최종 운영 정책을 대체하지 않는다.</p></article>
</div>'''

    return {
        "{{KICKER}}": "manual_analysis · 역할별 실행 매뉴얼",
        "{{TITLE}}": "온콜 인시던트 런북을 실제 실행 매뉴얼로 바꾸기",
        "{{SUBTITLE}}": "초안 문서 묶음을 역할 경로, 첫 성공, 안전 게이트, 레시피, 문제 해결, 감사 항목으로 재구성한 운영 매뉴얼 분석입니다.",
        "{{META}}": '<div class="generated-row"><span>source snapshot · 2026-06-07</span><span>manual status · owner review</span><span>profile · auto</span></div><div class="lens-strip"><span>Role Router</span><span>Safety</span><span>Troubleshooting</span><span>Source Limits</span></div>',
        "{{VERDICT}}": verdict,
        "{{READER_TOC}}": toc,
        "{{SOURCE_VERSION}}": source_version,
        "{{ROLE_ROUTER}}": role_router,
        "{{FIRST_SUCCESS}}": first_success,
        "{{PREREQUISITES_SAFETY}}": safety,
        "{{TASK_RECIPES}}": recipes,
        "{{REFERENCE_EXTRACT}}": reference_extract,
        "{{DECISION_GUIDE}}": decision,
        "{{TROUBLESHOOTING}}": troubleshooting,
        "{{OPERATIONS_RUNBOOK}}": operations,
        "{{MANUAL_AUDIT}}": audit,
        "{{NEXT_ACTIONS}}": next_actions,
        "{{SOURCE_NOTE}}": '<p><strong>Source note.</strong> 2026-06-07 기준 입력은 oncall-runbook.md v0.9 draft, alert-policy.md, rollback-checklist.md, incident-template.md다. 실제 제품 버전, 권한 정책, SLA, 법무 문구는 확인 불가이며 소유자 검토 후 확정해야 한다.</p>',
    }


def with_ids(body: str) -> str:
    ids = [
        ("manual-verdict", "verdict"),
        ("source-version", "source-version"),
        ("role-router", "role-router"),
        ("first-success", "first-success"),
        ("prerequisites-safety", "safety"),
        ("task-recipes", "recipes"),
        ("reference-extract", "reference-extract"),
        ("decision-guide", "decision-guide"),
        ("troubleshooting", "troubleshooting"),
        ("operations-runbook", "operations-runbook"),
        ("manual-audit", "manual-audit"),
    ]
    for cls, idv in ids:
        body = body.replace(f'<section class="{cls}">', f'<section id="{idv}" class="{cls}">')
    body = body.replace('<section class="try">', '<section id="next-actions" class="try">')
    return body


def render() -> None:
    # Read mode-specific documents and template skeletons to satisfy the layout-first/material contract.
    material_hashes = {}
    for rel in MODE_MATERIALS:
        p = SKILL / rel
        if not p.exists():
            raise FileNotFoundError(rel)
        material_hashes[rel] = hashlib.sha256(p.read_bytes()).hexdigest()

    base = read(ASSETS / "base.html")
    layout = read(ASSETS / "layouts" / "manual-analysis.html")
    for k, v in build_sections().items():
        layout = layout.replace(k, v)
    layout = with_ids(layout)
    if re.search(r"{{[A-Z0-9_]+}}", layout):
        raise RuntimeError(f"unfilled layout placeholder: {re.findall(r'{{[A-Z0-9_]+}}', layout)}")

    css = {name: read(ASSETS / name) for name in CSS_ORDER}
    core_concat = "\n".join(css[name] for name in CORE)
    core_hash = hashlib.sha256(core_concat.encode("utf-8")).hexdigest()
    css["theme.css"] = f"/* adaptive-html-final-core-css-sha256: {core_hash} */\n" + css["theme.css"]

    html = base
    html = html.replace("{{TITLE}}", "온콜 인시던트 런북 실행 매뉴얼 분석")
    html = html.replace("{{DESCRIPTION}}", "manual_analysis 모드로 온콜 사고 대응 런북 초안을 역할별 실행 매뉴얼로 재구성한 HTML 문서")
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
        raise RuntimeError("unfilled base placeholder")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8")

    SNAP.mkdir(parents=True, exist_ok=True)
    asset_sha = {}
    for name in CSS_ORDER:
        raw = read(ASSETS / name)
        (SNAP / name).write_text(raw, encoding="utf-8")
        asset_sha[name] = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    (SOURCES / "profile.json").write_text(json.dumps({"profile": "auto"}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    manifest = json.loads(read(SKILL / "manifest.json"))
    (SOURCES / "adaptive-html-final-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    integrity = {
        "core_css_sha256": core_hash,
        "asset_order": CORE,
        "asset_sha256": asset_sha,
        "profile": "auto",
        "mode07_material_sha256": material_hashes,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    (SOURCES / "css-integrity.json").write_text(json.dumps(integrity, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    render()
    print(OUT)
