#!/usr/bin/env python3
"""Render mode 08 expert_html only for the sequential 16-mode QA run.

Contract:
- Does not read any previous HTML body as source input.
- Does not import a shared/common page generator.
- Reads the expert layout, expert recipe, expert-relevant references, and the expert vt/wg templates only.
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
OUT = ROOT / "pages" / "08_expert_multi_agent_html_quality_gate_architecture.html"
SOURCES = ROOT / "sources"
SNAP = SOURCES / "assets"

MODE_MATERIALS = [
    "SKILL.md",
    "recipes/expert.prompt.md",
    "assets/layouts/expert-report.html",
    "references/layout-system.md",
    "references/writing-system.md",
    "references/quality-gates.md",
    "references/eval-rubric.md",
    "references/body-icon-system.md",
    "references/visual-html-system.md",
    "references/widget-system.md",
    "assets/visual-html-templates/03-risk-matrix.html",
    "assets/visual-html-templates/08-raci.html",
    "assets/visual-html-templates/06-quality-gate.html",
    "assets/visual-html-templates/16-implementation-plan.html",
    "assets/visual-html-templates/21-soft-workflow-map.html",
    "assets/widget-templates/03-annotated-pull-request.html",
    "assets/widget-templates/04-module-map.html",
    "assets/widget-templates/11-weekly-status.html",
    "assets/widget-templates/12-incident-timeline.html",
    "assets/widget-templates/16-implementation-plan.html",
    "assets/widget-templates/17-pr-writeup.html",
]
CSS_ORDER = [
    "theme.css", "components.css", "visual-components.css", "widgets.css", "visual-html.css",
    "body-icons.css", "editorial-patterns.css", "shape-visuals.css", "workflow-visuals.css",
    "layouts.css", "print.css", "theme-dark.css",
]
CORE = ["theme.css", "components.css", "visual-components.css", "layouts.css", "print.css"]

EXPERT_LOCAL_CSS = """
/* mode08 expert local contract: all direct report sections render as view surfaces; semantic grid wrappers stay normal flow. */
.layout-expert>section:not(.try){background:var(--card);border:1px solid var(--line);border-radius:var(--radius-md);padding:22px 24px;box-sizing:border-box}
.layout-expert>section.decision-section{display:block}
.layout-expert>section .expert-inner-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;margin:18px 0}
.layout-expert>section.decision-section .expert-inner-grid{grid-template-columns:repeat(2,minmax(0,1fr))}
.layout-expert>section .expert-inner-grid.three{grid-template-columns:repeat(3,minmax(0,1fr))}
.layout-expert>section .expert-note{background:var(--bg);border:1px solid var(--line);border-radius:var(--radius-sm);padding:12px 14px;margin:12px 0;color:var(--ink-soft)}
.layout-expert>section .vt-shell{margin:18px 0 0}
.layout-expert .validation-evidence-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;margin:18px 0 0}
.layout-expert .validation-evidence-card{background:var(--bg);border:1px solid var(--line);border-radius:var(--radius-sm);padding:14px 16px;min-width:0}
.layout-expert .validation-evidence-card h3{margin:0 0 8px;font-size:15px}
.layout-expert .validation-evidence-card p{margin:0;color:var(--ink-soft);font-size:13.8px;line-height:1.65}
.layout-expert .validation-evidence-card strong{color:var(--ink)}
.layout-expert .validation-status{display:inline-flex;align-items:center;gap:6px;border-radius:999px;border:1px solid var(--line);background:var(--card);color:var(--accent);font-weight:900;font-size:11px;letter-spacing:.05em;padding:3px 8px;margin-bottom:8px;text-transform:uppercase}
@media(max-width:760px){.layout-expert>section:not(.try){padding:18px 16px}.layout-expert>section .expert-inner-grid,.layout-expert>section.decision-section .expert-inner-grid,.layout-expert>section .expert-inner-grid.three{grid-template-columns:1fr}}
@media(max-width:760px){.layout-expert .validation-evidence-grid{grid-template-columns:1fr}}
"""


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def sha_bytes(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_icons() -> dict[str, str]:
    return {i["id"]: i["svg"] for i in json.loads(read(ASSETS / "body-icons.json"))}

ICONS = load_icons()


def icon(name: str) -> str:
    return f'<span class="body-icon body-icon--sm">{ICONS[name]}</span>'


def h2(n: int, title: str, icon_name: str, sub: str) -> str:
    return f'<h2>{icon(icon_name)}<span class="num">{n}</span>{title}</h2>\n<p class="h2-sub">{sub}</p>'


def li(items: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{x}</li>" for x in items) + "</ul>"


def vt_risk_matrix() -> str:
    return '''<section class="vt-shell" aria-label="품질 게이트 리스크 매트릭스">
  <div class="vt-frame"><div class="rm-grid">
    <div class="rm-cell rm-head">가능성</div><div class="rm-cell rm-head">낮음</div><div class="rm-cell rm-head">중간</div><div class="rm-cell rm-head">높음</div>
    <div class="rm-cell rm-head">영향 큼</div><div class="rm-cell rm-risk med">테마 토큰 drift</div><div class="rm-cell rm-risk high">section surface 누락</div><div class="rm-cell rm-risk high">공통 생성기 복사</div>
    <div class="rm-cell rm-head">영향 중간</div><div class="rm-cell rm-risk low">근거 문장 부족</div><div class="rm-cell rm-risk med">vt/wg 오선택</div><div class="rm-cell rm-risk med">모바일 표 overflow</div>
    <div class="rm-cell rm-head">영향 작음</div><div class="rm-cell rm-risk low">칩 문구 불일치</div><div class="rm-cell rm-risk low">caption 누락</div><div class="rm-cell rm-risk low">source note 약함</div>
  </div></div>
</section>'''


def vt_raci() -> str:
    return '''<section class="vt-shell" aria-label="멀티 에이전트 RACI">
  <div class="vt-frame"><div class="raci">
    <div class="h">작업</div><div class="h">R</div><div class="h">A</div><div class="h">C</div><div class="h">I</div>
    <div class="task">모드별 생성</div><div class="r">Mode owner</div><div class="a">Editor lead</div><div>Layout QA</div><div>Requester</div>
    <div class="task">정적 게이트</div><div class="r">QA agent</div><div class="a">Skill owner</div><div>CSS owner</div><div>Mode owner</div>
    <div class="task">시각 검수</div><div class="r">Design QA</div><div class="a">Editor lead</div><div>Browser QA</div><div>Requester</div>
    <div class="task">회귀 승인</div><div class="r">Integrator</div><div class="a">Skill owner</div><div>All mode owners</div><div>Team</div>
  </div></div>
</section>'''


def vt_quality_gate() -> str:
    return '''<section class="vt-shell" aria-label="릴리즈 품질 게이트">
  <div class="vt-frame"><div><div class="qg-grid">
    <div class="qg-card"><b>구조</b><p class="vt-text">layout slot가 모두 채워지고 번호 h2는 body-icon→num→제목 순서를 지킨다.</p></div>
    <div class="qg-card"><b>레이아웃</b><p class="vt-text">직접 section은 view surface, grid는 내부 wrapper에만 적용한다.</p></div>
    <div class="qg-card warn"><b>품질</b><p class="vt-text">요약 카드 반복과 예제 말투는 validate OK여도 재작성한다.</p></div>
    <div class="qg-card"><b>렌더</b><p class="vt-text">1280px/390px 캡처에서 overflow, 테마바, 다크 대비를 확인한다.</p></div>
  </div><div class="qg-final">완료 판정: current_mode_issue_count=0과 full_output_residual=0을 각각 증빙한다.</div></div></div>
</section>'''


def vt_plan() -> str:
    return '''<section class="vt-shell" aria-label="90일 도입 계획">
  <div class="vt-frame"><div class="plan-grid">
    <article class="milestone"><div class="vt-kicker">0-30</div><b>계약 잠금</b><p class="vt-text">body-icon, surface, layout-first, quality gate를 생성 전 체크리스트로 승격.</p></article>
    <article class="milestone"><div class="vt-kicker">31-60</div><b>독립 실행</b><p class="vt-text">1모드 1컨텍스트와 전용 recipe/layout/reference 로딩을 운영 절차화.</p></article>
    <article class="milestone plan-risk"><div class="vt-kicker">61-90</div><b>평가 분리</b><p class="vt-text">생성과 평가를 분리하고 390/1280 캡처 증거를 evidence JSON에 기록.</p></article>
    <article class="milestone"><div class="vt-kicker">운영</div><b>통합 보류</b><p class="vt-text">미수정 미래 페이지가 남아 있으면 전체 완료 보고를 금지.</p></article>
  </div></div>
</section>'''


def vt_workflow() -> str:
    return '''<section class="vt-shell" aria-label="멀티 에이전트 품질 파이프라인">
  <div class="vt-frame"><div class="wf-board">
    <div class="wf-top"><span class="wf-newbadge">AI PIPELINE</span><div class="wf-aistack" aria-hidden="true"><span class="wf-aibadge">QA</span><span class="wf-bag">▣</span></div></div>
    <div class="wf-map"><div class="wf-col">
      <article class="wf-card"><div class="wf-icon">01</div><strong>Mode Owner</strong><p>전용 layout/recipe/ref만 읽고 한 모드씩 생성한다.</p></article>
      <article class="wf-card"><div class="wf-icon">02</div><strong>Layout QA</strong><p>surface, wrapper/grid 분리, body-icon 순서를 확인한다.</p></article>
      <article class="wf-card"><div class="wf-icon">03</div><strong>Editor QA</strong><p>얇은 섹션과 공통 카드 반복을 차단한다.</p></article>
    </div><div class="wf-center"><div class="wf-codewin" aria-hidden="true"><span></span><span></span><span></span></div><div class="wf-dash" aria-hidden="true"><div class="wf-dashbar"></div><div class="wf-dashblock"></div></div><div class="wf-metrics"><div class="wf-metric"><b>1</b><span>mode/turn</span></div><div class="wf-metric"><b>0</b><span>icon miss</span></div><div class="wf-metric"><b>2</b><span>screens</span></div></div></div><div class="wf-col">
      <article class="wf-card"><div class="wf-icon">04</div><strong>Static Gate</strong><p>validate_output와 quality_contract_check를 함께 실행한다.</p></article>
      <article class="wf-card"><div class="wf-icon">05</div><strong>Browser Gate</strong><p>1280px/390px 렌더와 document overflow를 확인한다.</p></article>
      <article class="wf-card"><div class="wf-icon">06</div><strong>Integrator</strong><p>full output residual issue를 숨기지 않는다.</p></article>
    </div></div><div class="wf-bottom" aria-hidden="true"><span class="wf-rail-short"></span><span class="wf-rail-long"></span><span class="wf-arrow"><i>→</i></span></div>
  </div></div>
</section>'''


def wg_status() -> str:
    return '''<section class="wg-11" aria-labelledby="wg11-expert-title">
  <header class="wg-11-head"><p class="wg-11-kicker">운영 상태</p><h3 id="wg11-expert-title" class="wg-11-h">Quality gate rollout · 08 expert 기준</h3><p class="wg-11-lead">전역 계약은 정의되어 있지만 산출물 검수는 모드별 증거로 닫아야 합니다.</p></header>
  <div class="wg-11-kpis"><div class="wg-11-kpi wg-11-kpi-good"><span class="wg-11-kpi-v">0</span><span class="wg-11-kpi-l">08번 icon miss</span></div><div class="wg-11-kpi wg-11-kpi-prog"><span class="wg-11-kpi-v">2</span><span class="wg-11-kpi-l">렌더 폭</span></div><div class="wg-11-kpi wg-11-kpi-risk"><span class="wg-11-kpi-v wg-11-warn">8</span><span class="wg-11-kpi-l">잔여 모드</span></div><div class="wg-11-kpi"><span class="wg-11-kpi-v">1</span><span class="wg-11-kpi-l">mode/turn</span></div></div>
</section>'''


def wg_module() -> str:
    return '''<section class="wg-04" aria-labelledby="wg04-expert-title">
  <header class="wg-04-head"><p class="wg-04-kicker">시스템 구조</p><h3 id="wg04-expert-title" class="wg-04-title">HTML quality gate architecture</h3><p class="wg-04-lead">핵심 경로는 모드 전용 생성에서 정적 검증, 브라우저 증거, 통합 승인으로 이어집니다.</p></header>
  <div class="wg-04-path" role="note"><span class="wg-04-path-label">핵심 경로</span><span class="wg-04-path-chain"><code>mode</code> → <code>layout</code> → <code>static</code> → <code>browser</code> → <code>evidence</code></span><span class="wg-04-path-note">이전 HTML 본문과 공통 생성기는 이 경로 밖으로 격리합니다.</span></div>
</section>'''


def wg_incident() -> str:
    return '''<section class="wg-12" aria-labelledby="wg12-expert-title">
  <header class="wg-12-head"><p class="wg-12-kicker">회귀 사건 타임라인</p><h3 id="wg12-expert-title" class="wg-12-title">공통 생성기 회귀가 감지되는 순서</h3><p class="wg-12-meta">증상은 HTML 구조보다 시각 품질에서 먼저 보입니다.</p></header>
  <ol class="wg-12-tl"><li class="wg-12-tl-item"><span class="wg-12-tl-time">T+0</span><span class="wg-12-tl-dot wg-12-dot-detect"></span><div class="wg-12-tl-body"><h3>layout class만 맞음</h3><p>실제 slot 흐름 대신 카드 반복이 들어갑니다.</p></div></li><li class="wg-12-tl-item"><span class="wg-12-tl-time">T+1</span><span class="wg-12-tl-dot wg-12-dot-mit"></span><div class="wg-12-tl-body"><h3>h2 아이콘 누락</h3><p>번호는 보이지만 최신 스킬의 body-icon 계약이 빠집니다.</p></div></li><li class="wg-12-tl-item"><span class="wg-12-tl-time">T+2</span><span class="wg-12-tl-dot wg-12-dot-resolve"></span><div class="wg-12-tl-body"><h3>브라우저 캡처에서 확정</h3><p>390px overflow, 테마바 누락, 얇은 섹션이 시각적으로 드러납니다.</p></div></li></ol>
</section>'''


def wg_pr_review() -> str:
    return '''<section class="wg-03" aria-labelledby="wg03-expert-title">
  <header class="wg-03-head"><p class="wg-03-kicker">패치 리뷰</p><h3 id="wg03-expert-title" class="wg-03-title">스킬 패치가 필요한 코드 리뷰 포인트</h3><p class="wg-03-meta"><span class="wg-03-badge">review</span><span>전역 계약은 생성 절차와 검증기에 함께 들어가야 합니다.</span></p></header>
  <div class="wg-03-grid"><pre class="wg-03-diff"><code><span class="wg-03-row wg-03-add"><span class="wg-03-ln">+</span>layout_slot_map required</span>
<span class="wg-03-row wg-03-add"><span class="wg-03-ln">+</span>numbered_h2_body_icon required</span>
<span class="wg-03-row wg-03-add"><span class="wg-03-ln">+</span>browser_capture_1280_390 required</span></code></pre><div class="wg-03-notes"><article class="wg-03-note"><div class="wg-03-note-head"><span class="wg-03-sev-critical">BLOCK</span><span class="wg-03-note-loc">generation contract</span></div><p class="wg-03-note-body">공통 생성기 또는 이전 HTML 본문 재사용은 즉시 실패로 둡니다.</p></article><article class="wg-03-note"><div class="wg-03-note-head"><span class="wg-03-sev-warn">WARN</span><span class="wg-03-note-loc">quality gate</span></div><p class="wg-03-note-body">validate OK만으로 완료 보고하지 않도록 quality_contract와 캡처 증거를 묶습니다.</p></article></div></div>
</section>'''


def wg_plan() -> str:
    return '''<section class="wg-16" aria-labelledby="wg16-expert-title">
  <header class="wg-16-head"><p class="wg-16-kicker">실행 계획</p><h3 id="wg16-expert-title" class="wg-16-title">게이트 운영을 90일 안에 제도화</h3><p class="wg-16-lead">문서 패치가 아니라 생성 워크플로의 운영모델로 고정합니다.</p></header>
  <div class="wg-16-panel"><h3 class="wg-16-h3">마일스톤</h3><ol class="wg-16-ms"><li class="wg-16-ms-item wg-16-done"><span class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></span><div class="wg-16-ms-card"><div class="wg-16-ms-top"><strong class="wg-16-ms-name">0-30일 · 계약 게이트</strong><span class="wg-16-badge wg-16-bd-done">lock</span></div><p class="wg-16-ms-desc">numbered h2 icon, section surface, mode depth를 완료 조건에 둡니다.</p></div></li><li class="wg-16-ms-item wg-16-active"><span class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></span><div class="wg-16-ms-card"><div class="wg-16-ms-top"><strong class="wg-16-ms-name">31-60일 · 독립 실행</strong><span class="wg-16-badge wg-16-bd-active">active</span></div><p class="wg-16-ms-desc">1모드 1컨텍스트, 전용 자료만 읽는 재작성 루프를 도입합니다.</p></div></li><li class="wg-16-ms-item"><span class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></span><div class="wg-16-ms-card"><div class="wg-16-ms-top"><strong class="wg-16-ms-name">61-90일 · 평가 분리</strong><span class="wg-16-badge">next</span></div><p class="wg-16-ms-desc">생성자와 평가자를 분리하고 evidence JSON을 릴리즈 산출물로 남깁니다.</p></div></li></ol></div>
</section>'''


def wg_pr_writeup() -> str:
    return '''<section class="wg-17" aria-labelledby="wg17-expert-title">
  <header class="wg-17-head"><p class="wg-17-kicker">릴리즈 노트 초안</p><h3 id="wg17-expert-title" class="wg-17-title">품질 게이트 패치 요약</h3><p class="wg-17-p">다음 패치는 산출물 품질 저하를 만든 실행 구멍을 닫는 데 집중합니다.</p></header>
  <div class="wg-17-summary"><span class="wg-17-chip wg-17-chip-add">ADD</span><span>per-mode evidence requirement</span><span class="wg-17-chip wg-17-chip-branch">CHANGE</span><span>layout-first preflight</span></div>
  <div class="wg-17-ba"><div class="wg-17-ba-col wg-17-ba-before"><span class="wg-17-ba-tag">Before</span><ul class="wg-17-ba-list"><li>공통 구조 반복</li><li>검증 OK 과신</li><li>캡처 증거 누락</li></ul></div><div class="wg-17-ba-arrow">→</div><div class="wg-17-ba-col wg-17-ba-after"><span class="wg-17-ba-tag">After</span><ul class="wg-17-ba-list"><li>모드별 생성</li><li>정성 게이트 병행</li><li>1280/390 증거 기록</li></ul></div></div>
</section>'''


def build_mapping() -> dict[str, str]:
    executive = f'''{h2(1, "Executive Summary · 결론과 우선순위", "decision", "문제는 스킬 정의 부재가 아니라 최신 계약을 산출물 생성 루프가 끝까지 강제하지 못한 데 있습니다.")}
<div class="summary-grid">
  <article class="decision-card"><h3>결론</h3><p>멀티 에이전트 HTML 품질 게이트는 스킬 문서 패치만으로 끝나지 않습니다. 생성 전 계약, 단일 모드 생성, 정적 게이트, 브라우저 증거, 통합 보류가 하나의 운영 체계로 묶여야 회귀가 멈춥니다.</p></article>
  <article class="decision-card"><h3>우선순위</h3><p>1순위는 번호 h2의 body-icon, 주요 section의 view surface, 모드별 vt/wg 적용을 page 단위로 닫는 것입니다. 2순위는 운영모델·RACI·리스크·로드맵·검증 증빙까지 포함하는 전문가 문서 깊이입니다.</p></article>
  <article class="decision-card"><h3>즉시 조치</h3><p>한 번에 여러 모드를 만들지 말고, 한 모드가 검증과 캡처까지 끝나야 다음 모드로 넘어갑니다. 보고에서는 current mode OK와 full output residual을 분리해야 합니다.</p></article>
</div>
{wg_status()}'''

    decisions = f'''<div class="expert-section-stack">{h2(2, "Decision Cards · 도입 판단 4가지", "metric", "각 판단은 근거와 실행 포인트를 함께 가져야 운영 의사결정에 쓸 수 있습니다.")}
<div class="expert-inner-grid">
  <article class="decision-card"><h3>01 · 1모드 1턴 고정</h3><p><strong>판단:</strong> 대량 생성은 품질보다 속도를 최적화해 공통 구조 복사를 재발시킵니다. <strong>실행:</strong> tracker의 last_completed와 next_mode를 근거로 한 모드만 완료 처리합니다.</p></article>
  <article class="decision-card"><h3>02 · 생성과 검증 분리</h3><p><strong>판단:</strong> 생성자가 자기 결과를 바로 통과 처리하면 전문성 결함을 과소평가합니다. <strong>실행:</strong> static, quality, browser gate 결과를 각각 evidence에 남깁니다.</p></article>
  <article class="decision-card"><h3>03 · layout-first 강제</h3><p><strong>판단:</strong> layout 클래스만 붙인 자유형 main은 최신 스킬 결과물이 아닙니다. <strong>실행:</strong> slot를 먼저 매핑하고 추가 블록은 해당 섹션 내부에만 넣습니다.</p></article>
  <article class="decision-card"><h3>04 · 중간 성공과 전체 성공 분리</h3><p><strong>판단:</strong> 한 페이지가 통과해도 잔여 페이지가 남으면 목표는 미완성입니다. <strong>실행:</strong> isolated OK, full OK, residual issue count를 함께 기록합니다.</p></article>
</div>{vt_raci()}</div>'''

    operating = f'''{h2(3, "Architecture Map · 게이트 운영모델", "map", "전문가 리포트의 핵심은 누가 무엇을 만들고 어떻게 증명하는가를 구조화하는 것입니다.")}
<p>권장 구조는 Mode Owner, Layout QA, Editorial QA, Browser QA, Integrator의 5역할입니다. 생성자는 모드 전용 자료만 읽고, QA는 생성 의도보다 렌더링 결과와 규칙 위반을 우선합니다.</p>
{wg_module()}
<div class="table-scroll"><table class="mobile-card-table"><caption>Operating Model · 책임, 산출물, 주기, 판단 기준</caption><thead><tr><th>역할</th><th>책임</th><th>산출물</th><th>주기</th><th>판단 기준</th></tr></thead><tbody>
<tr><td data-label="역할">Mode Owner</td><td data-label="책임">전용 recipe/layout/reference만 읽고 한 모드 생성</td><td data-label="산출물">HTML page, source snapshot</td><td data-label="주기">모드별 1회</td><td data-label="판단 기준">layout slot 완전 충족</td></tr>
<tr><td data-label="역할">Layout QA</td><td data-label="책임">section surface, grid wrapper, h2 icon 순서 검사</td><td data-label="산출물">structural metrics</td><td data-label="주기">생성 직후</td><td data-label="판단 기준">numbered icon 100%, overflow 0</td></tr>
<tr><td data-label="역할">Editorial QA</td><td data-label="책임">얇은 카드 반복, 근거 부재, 예제 문구 제거</td><td data-label="산출물">quality contract result</td><td data-label="주기">정적 게이트 후</td><td data-label="판단 기준">전문 문서 깊이 하한 충족</td></tr>
<tr><td data-label="역할">Browser QA</td><td data-label="책임">1280/390 렌더, 테마바, 모바일 문서폭 확인</td><td data-label="산출물">screenshots, browser metrics</td><td data-label="주기">페이지별</td><td data-label="판단 기준">document overflow false</td></tr>
<tr><td data-label="역할">Integrator</td><td data-label="책임">전체 산출물 residual issue와 tracker 관리</td><td data-label="산출물">evidence JSON, next_mode</td><td data-label="주기">모드 완료 보고 전</td><td data-label="판단 기준">현재 모드 issue 0, 잔여 이슈 명시</td></tr>
</tbody></table></div>
{vt_workflow()}'''

    risk = f'''{h2(4, "Risk Matrix · 실패 모드와 통제책", "warning", "리스크는 영향도·가능성·통제책·검증 방법까지 있어야 실제 게이트가 됩니다.")}
<div class="table-scroll"><table class="mobile-card-table"><caption>멀티 에이전트 HTML 품질 리스크</caption><thead><tr><th>리스크</th><th>영향도</th><th>가능성</th><th>통제책</th><th>검증 방법</th></tr></thead><tbody>
<tr><td data-label="리스크">공통 생성기 복사</td><td data-label="영향도">높음</td><td data-label="가능성">높음</td><td data-label="통제책">1모드 1턴, 전용 layout/recipe/ref만 읽기</td><td data-label="검증 방법">vt/wg 다양성, repeated heading, quality_contract_check</td></tr>
<tr><td data-label="리스크">번호 h2 아이콘 누락</td><td data-label="영향도">높음</td><td data-label="가능성">중간</td><td data-label="통제책">numbered_h2_body_icon_gate 전역 강제</td><td data-label="검증 방법">numberedH2 == numberedIcon</td></tr>
<tr><td data-label="리스크">섹션 surface 누락</td><td data-label="영향도">높음</td><td data-label="가능성">중간</td><td data-label="통제책">section surface CSS와 browser metric 병행</td><td data-label="검증 방법">direct section view surface 확인</td></tr>
<tr><td data-label="리스크">전문성 얇음</td><td data-label="영향도">중간</td><td data-label="가능성">높음</td><td data-label="통제책">운영모델, RACI, 리스크, 로드맵, 검증 증빙 필수</td><td data-label="검증 방법">mode depth와 수동 전문가 체크리스트</td></tr>
<tr><td data-label="리스크">모바일 표 overflow</td><td data-label="영향도">중간</td><td data-label="가능성">중간</td><td data-label="통제책">table-scroll 또는 mobile-card-table 사용</td><td data-label="검증 방법">390px scrollWidth == clientWidth</td></tr>
</tbody></table></div>
{vt_risk_matrix()}
{wg_incident()}'''

    roadmap = f'''{h2(5, "Priority Roadmap · 0~90일 실행 흐름", "flow", "로드맵은 날짜가 아니라 산출물과 완료 증거를 기준으로 닫습니다.")}
<div class="roadmap-grid">
  <article class="decision-card"><h3>0~30일 · 계약 잠금</h3><p>스킬 본체, AGENTS, validate_output, quality_contract_check가 같은 완료 정의를 보도록 맞춥니다. 완료 증거는 governance 57/57과 샘플 페이지 isolated OK입니다.</p></article>
  <article class="decision-card"><h3>31~60일 · 모드별 재작성</h3><p>16개 모드를 한 번에 만들지 않고 tracker 기반으로 순차 진행합니다. 각 모드는 evidence JSON, 1280/390 캡처, mode-specific issue count 0으로 닫습니다.</p></article>
  <article class="decision-card"><h3>61~90일 · 통합 릴리즈</h3><p>마지막 모드까지 끝난 뒤 full output validate OK와 전체 브라우저 스모크를 수행합니다. 최종 산출물은 index 재동기화, manifest/hash 일치, 최종 링크와 검증표입니다.</p></article>
</div>
{vt_plan()}
{wg_plan()}'''

    validation = f'''{h2(6, "Validation Checklist · 완료 기준과 증빙", "check", "완료는 말이 아니라 명령 결과, 렌더 지표, evidence 파일로 증명해야 합니다.")}
<div class="expert-inner-grid">
  <article class="mini-card"><h3>정적 검증</h3><p><code>validate_output.py</code>는 코어 CSS 해시, no-JS, table caption, body-icon, section surface를 확인합니다. 실패 시 브라우저 캡처보다 먼저 수정합니다.</p></article>
  <article class="mini-card"><h3>품질 검증</h3><p><code>quality_contract_check.py</code>는 임시 생성 문구, 반복 기준명, mini-card 과사용 같은 붕어빵 냄새를 차단합니다.</p></article>
  <article class="mini-card"><h3>브라우저 검증</h3><p>1280px와 390px에서 themebar, generated-row, direct section surface, document overflow를 수집합니다.</p></article>
  <article class="mini-card"><h3>통합 검증</h3><p>현재 모드가 OK여도 잔여 페이지가 실패하면 full output은 미완성입니다. 완료 보고에는 full_ok와 current_mode_issue_count를 함께 적습니다.</p></article>
</div>
{vt_quality_gate()}
<div class="validation-evidence-grid" aria-label="완료 증빙 매트릭스">
  <article class="validation-evidence-card"><span class="validation-status">static</span><h3>명령 증빙</h3><p><strong>필수:</strong> <code>validate_output.py</code>와 <code>quality_contract_check.py</code> 결과를 그대로 남깁니다. 통과 문구만 적지 말고 대상 폴더와 실행 시각을 함께 기록합니다.</p></article>
  <article class="validation-evidence-card"><span class="validation-status">visual</span><h3>렌더 증빙</h3><p><strong>필수:</strong> 1280px·390px 캡처, section class, display, grid columns, document overflow 값을 evidence JSON에 남깁니다.</p></article>
  <article class="validation-evidence-card"><span class="validation-status">editorial</span><h3>품질 증빙</h3><p><strong>필수:</strong> 얇은 카드 반복, 예제 말투, 이전 HTML 복사 흔적이 없는지 별도 검수합니다. 스킬 문서와 결과물의 계약이 같은지 확인합니다.</p></article>
  <article class="validation-evidence-card"><span class="validation-status">release</span><h3>완료 판정</h3><p><strong>필수:</strong> 현재 모드 issue 0과 전체 산출물 residual 0을 분리합니다. 둘 중 하나라도 남으면 완료가 아니라 다음 수정 항목입니다.</p></article>
</div>'''

    final = f'''{h2(7, "Final Recommendation · 다음 모드 진행 조건", "success", "08번은 전문가 리포트 계약을 충족했으므로 다음은 09 article_html을 같은 방식으로 진행합니다.")}
<p>이 아키텍처의 핵심은 검증기를 더 많이 만드는 것이 아니라, 생성 행위를 검증 가능한 운영 절차로 바꾸는 것입니다. 다음 모드도 전용 자료를 새로 읽고, 이전 HTML 본문 없이, 한 페이지 검증 후 중단해야 합니다.</p>
<div class="card-grid"><article class="summary-card"><h3>Do</h3><p>1모드 1턴, layout-first, body-icon/surface 100%, evidence JSON 기록.</p></article><article class="summary-card"><h3>Do not</h3><p>공통 생성기, 이전 HTML 복사, 예제 문구, full output 실패 은폐.</p></article><article class="summary-card"><h3>Next</h3><p>09 article_html을 article recipe/layout/reference 기반으로 재작성.</p></article></div>'''

    return {
        "{{KICKER}}": "Expert HTML Report · Quality Gate Architecture",
        "{{TITLE}}": "멀티 에이전트 HTML 품질 게이트 아키텍처",
        "{{SUBTITLE}}": "스킬 정의와 산출물 생성 사이의 회귀를 끊기 위한 운영모델, RACI, 리스크 통제, 90일 로드맵, 검증 증빙 체계입니다.",
        "{{META}}": '<div class="generated-row"><span>generated · 2026-06-07</span><span>mode · expert_html</span><span>profile · auto</span><span>status · single-mode revision</span></div><div class="lens-strip"><span>Architecture</span><span>RACI</span><span>Risk</span><span>Validation</span></div>',
        "{{EXECUTIVE_SUMMARY}}": executive,
        "{{DECISION_CARDS}}": decisions,
        "{{ARCHITECTURE}}": operating,
        "{{RISK_MATRIX}}": risk,
        "{{PRIORITY_ROADMAP}}": roadmap,
        "{{VALIDATION_CHECKLIST}}": validation,
        "{{FINAL_RECOMMENDATION}}": final,
        "{{SOURCE_NOTE}}": '<strong>Source note.</strong> 2026-06-07 현재 스킬 자산 기준으로 작성한 expert_html 운영모델 제안입니다. 사용한 단일 출처는 expert.prompt.md, expert-report.html, layout/writing/visual-html/widget/body-icon/quality-gates references입니다. 실제 조직 역할명, CI 환경, 브라우저 캡처 인프라는 입력 원문에 없으므로 일반 운영모델로 제안했고 환경별 수치는 확인 필요입니다.',
    }


def render() -> None:
    material_hashes = {}
    for rel in MODE_MATERIALS:
        p = SKILL / rel
        if not p.exists():
            raise FileNotFoundError(rel)
        material_hashes[rel] = sha_bytes(p)

    base = read(ASSETS / "base.html")
    layout = read(ASSETS / "layouts" / "expert-report.html")
    for k, v in build_mapping().items():
        layout = layout.replace(k, v)
    if re.search(r"{{[A-Z0-9_]+}}", layout):
        raise RuntimeError(f"unfilled layout slots: {sorted(set(re.findall(r'{{[A-Z0-9_]+}}', layout)))}")

    css = {name: read(ASSETS / name) for name in CSS_ORDER}
    core_hash = hashlib.sha256("\n".join(css[name] for name in CORE).encode("utf-8")).hexdigest()
    css["theme.css"] = f"/* adaptive-html-final-core-css-sha256: {core_hash} */\n" + css["theme.css"]

    html = base
    html = html.replace("{{TITLE}}", "멀티 에이전트 HTML 품질 게이트 아키텍처")
    html = html.replace("{{DESCRIPTION}}", "expert_html 모드로 작성한 멀티 에이전트 HTML 품질 게이트 운영모델, RACI, 리스크, 로드맵 리포트")
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
        "{{LAYOUTS_CSS}}": css["layouts.css"] + "\n" + EXPERT_LOCAL_CSS,
        "{{PRINT_CSS}}": css["print.css"],
        "{{THEME_DARK_CSS}}": css["theme-dark.css"],
    }
    for slot, value in slot_map.items():
        html = html.replace(slot, value)
    if "{{" in html:
        raise RuntimeError("unfilled base slots")

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
        "mode08_material_sha256": material_hashes,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    })
    integrity_path.write_text(json.dumps(prior, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    render()
    print(OUT)
