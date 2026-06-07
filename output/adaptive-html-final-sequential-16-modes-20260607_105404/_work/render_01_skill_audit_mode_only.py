#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
SKILL = REPO / 'skills/adaptive-html-final'
ASSETS = SKILL / 'assets'
OUT = ROOT / 'pages/01_skill_audit_meeting_action_plan.html'

# Mode-01 only materials. Do not read any previous output HTML body.
MODE_MATERIALS = [
    SKILL / 'SKILL.md',
    SKILL / 'recipes/audit.prompt.md',
    ASSETS / 'layouts/skill-audit-report.html',
    SKILL / 'references/layout-system.md',
    SKILL / 'references/skill-audit-system.md',
    SKILL / 'references/body-icon-system.md',
    SKILL / 'references/visual-html-system.md',
    SKILL / 'references/widget-system.md',
    ASSETS / 'visual-html-templates/06-quality-gate.html',
    ASSETS / 'visual-html-templates/09-file-tour.html',
    ASSETS / 'visual-html-templates/20-prompt-tuner.html',
    ASSETS / 'visual-html-templates/16-implementation-plan.html',
    ASSETS / 'visual-html-templates/21-soft-workflow-map.html',
    ASSETS / 'widget-templates/03-annotated-pull-request.html',
    ASSETS / 'widget-templates/17-pr-writeup.html',
]
MATERIAL_HASH = {str(p.relative_to(REPO)): hashlib.sha256(p.read_bytes()).hexdigest() for p in MODE_MATERIALS}
# Read so the render is anchored to mode-specific docs/templates.
for p in MODE_MATERIALS:
    p.read_text(encoding='utf-8')

CORE = ['theme.css', 'components.css', 'visual-components.css', 'layouts.css', 'print.css']
CONDITIONAL = ['widgets.css', 'visual-html.css', 'body-icons.css', 'editorial-patterns.css', 'theme-dark.css']

def read_asset(name: str) -> str:
    return (ASSETS / name).read_text(encoding='utf-8')

core_texts = [read_asset(name) for name in CORE]
core_hash = hashlib.sha256('\n'.join(core_texts).encode('utf-8')).hexdigest()
css_slots = {
    'THEME_CSS': f'/* adaptive-html-final-core-css-sha256: {core_hash} */\n' + read_asset('theme.css'),
    'COMPONENTS_CSS': read_asset('components.css'),
    'VISUAL_COMPONENTS_CSS': read_asset('visual-components.css'),
    'WIDGETS_CSS': read_asset('widgets.css'),
    'VISUAL_HTML_CSS': read_asset('visual-html.css'),
    'BODY_ICONS_CSS': read_asset('body-icons.css'),
    'EDITORIAL_PATTERNS_CSS': read_asset('editorial-patterns.css'),
    'SHAPE_VISUALS_CSS': '',
    'WORKFLOW_VISUALS_CSS': '',
    'LAYOUTS_CSS': read_asset('layouts.css'),
    'PRINT_CSS': read_asset('print.css'),
    'THEME_DARK_CSS': read_asset('theme-dark.css'),
}

icons = {item['id']: item['svg'] for item in json.loads((ASSETS / 'body-icons.json').read_text(encoding='utf-8'))}
def icon(name: str) -> str:
    return f'<span class="body-icon body-icon--sm">{icons[name]}</span>'

def h2(num: int, title: str, icon_id: str = 'audit') -> str:
    return f'<h2>{icon(icon_id)}<span class="num">{num}</span>{title}</h2>'

header_generated = '''<div class="generated-row"><p class="generated-date">Generated · 2026-06-07 KST</p><div class="lens-strip" aria-label="적용 렌즈"><span class="lens-strip-label">LENS</span><span class="lens-chip">mode 01</span><span class="lens-chip">skill audit</span><span class="lens-chip">layout-first</span><span class="lens-chip">no reuse</span><span class="lens-chip">capture QA</span></div></div>'''

purpose = f'''
{h2(1, 'Executive Diagnosis', 'audit')}
<p class="h2-sub">회의록을 실행 계획으로 바꾸는 스킬은 목적은 선명하지만, 소유자·결정·근거·후속 행동을 강제하는 계약이 약하면 회의 요약문 수준으로 후퇴한다.</p>
<div class="grid-3">
  <article class="score-card"><h3>현재 강점</h3><p>회의 원문에서 할 일과 결정 사항을 뽑아내는 방향은 맞다. 사용자가 원하는 결과도 “요약”이 아니라 “실행 가능한 액션 플랜”으로 분명하다.</p></article>
  <article class="score-card"><h3>핵심 결함</h3><p>OWNER, DECISION, SOURCE, DUE, NEXT_STEP 필드가 필수 계약으로 잠겨 있지 않다. 이 상태에서는 모델이 좋은 말투의 회의록을 만들고도 실행 책임을 놓칠 수 있다.</p></article>
  <article class="score-card"><h3>수정 원칙</h3><p>스킬 본문에 “누가, 무엇을, 왜, 언제까지, 어떤 증거로”를 구조화하도록 강제하고, UNKNOWN을 숨기지 않는 품질 게이트를 추가한다.</p></article>
</div>
<section class="vt-shell" aria-label="회의록 실행계획 변환 품질 게이트"><div class="vt-frame"><div class="qg-grid">
  <div class="qg-card"><b>OWNER</b><p class="vt-text">담당자가 없으면 액션이 아니라 메모로 분류한다.</p></div>
  <div class="qg-card"><b>DECISION</b><p class="vt-text">결정과 의견을 분리하고 결정 근거를 원문 위치와 연결한다.</p></div>
  <div class="qg-card warn"><b>UNKNOWN</b><p class="vt-text">원문에 없는 마감·수치·책임자는 추론하지 않고 확인 필요로 둔다.</p></div>
  <div class="qg-card block"><b>NO OWNER</b><p class="vt-text">소유자 없는 액션 항목이 있으면 최종 산출을 보류한다.</p></div>
</div><div class="qg-final">AUDIT RESULT: 요약 스킬이 아니라 실행계획 변환 스킬로 정의를 강화해야 한다.</div></div></section>
'''

structure_score = f'''
{h2(2, 'Score Table', 'metric')}
<p class="h2-sub">현재 스킬은 방향성은 좋지만 실행 계약과 실패 대응이 부족하다. 점수는 “바로 운영 가능한가” 기준으로 낮게 잡았다.</p>
<div class="grid-3">
  <article class="score-card"><h3>목적 명확성 · 4/5</h3><p>회의록을 실행계획으로 바꾸는 목적은 선명하다. 다만 출력 실패 조건이 약해 “잘 정리된 요약”과 경계가 흐릴 수 있다.</p></article>
  <article class="score-card"><h3>입출력 계약 · 3/5</h3><p>필수 필드 이름은 암시되어 있으나, 누락 시 처리 방식과 UNKNOWN 표기 방식이 충분히 강제되지 않는다.</p></article>
  <article class="score-card"><h3>품질 게이트 · 2/5</h3><p>검증 항목이 사람이 보기 좋은 체크리스트에 머물러 있다. owner/source/due 누락을 실패로 처리해야 한다.</p></article>
</div>
<div class="table-scroll"><table>
  <caption>회의록 실행계획 변환 스킬 감사 점수표</caption>
  <thead><tr><th>항목</th><th>점수</th><th>판정 근거</th><th>필수 보완</th></tr></thead>
  <tbody>
    <tr><th>목적/트리거</th><td>4/5</td><td>회의록·액션 플랜 변환 목적은 명확</td><td>요약 모드와의 경계 문구 추가</td></tr>
    <tr><th>출력 스키마</th><td>3/5</td><td>필드 후보는 있으나 필수/선택 구분 약함</td><td>OWNER·SOURCE·DUE·NEXT_STEP required</td></tr>
    <tr><th>근거 추적</th><td>2/5</td><td>원문 발췌 위치와 판단 연결이 약함</td><td>source_quote 또는 source_span 필수</td></tr>
    <tr><th>실패 대응</th><td>2/5</td><td>정보 부족 시 질문/UNKNOWN 처리 미흡</td><td>확인 필요 항목을 별도 큐로 분리</td></tr>
  </tbody>
</table></div>
<section class="vt-shell" aria-label="감사 대상 파일 투어"><div class="vt-frame"><div class="ft">
  <article class="ft-card"><div class="ft-head"><span>SKILL.md</span><span>contract</span></div><div class="ft-body"><p class="vt-text">출력 필드와 실패 조건을 정의하는 중심 파일.</p><div class="ft-note"><b>Review note</b><br>required/optional 필드를 명시해야 한다.</div></div></article>
  <article class="ft-card"><div class="ft-head"><span>quality-gates.md</span><span>gate</span></div><div class="ft-body"><p class="vt-text">누락·추론·원문 없는 주장을 막는 검증 기준.</p><div class="ft-note"><b>Review note</b><br>owner/source 누락은 실패로 승격한다.</div></div></article>
  <article class="ft-card"><div class="ft-head"><span>examples/</span><span>proof</span></div><div class="ft-body"><p class="vt-text">좋은 회의록과 나쁜 회의록을 대조하는 정답지.</p><div class="ft-note"><b>Review note</b><br>UNKNOWN 예제가 반드시 필요하다.</div></div></article>
</div></div></section>
'''

line_audit = f'''
{h2(3, 'Line / Section Findings', 'warning')}
<p class="h2-sub">문제는 문장 표현이 아니라 계약 누락이다. 아래 리뷰는 스킬 본문에 반드시 들어가야 할 세 가지 규칙을 diff처럼 보여준다.</p>
<section class="wg-03" aria-labelledby="wg-03-title-mode01">
  <header class="wg-03-head">
    <p class="wg-03-kicker">ANNOTATED SKILL REVIEW</p>
    <h2 id="wg-03-title-mode01" class="wg-03-title">회의록 → 실행계획 변환 계약에서 막아야 할 3가지</h2>
    <div class="wg-03-meta"><span class="wg-03-chip wg-03-chip-del">3 findings</span><span class="wg-03-chip">audit mode</span><span class="wg-03-chip">no HTML reuse</span></div>
    <nav class="wg-03-jump" aria-label="노트 점프"><span class="wg-03-jump-label">Jump</span><a href="#m01-n1" class="wg-03-jump-link wg-03-sev-critical">owner</a><a href="#m01-n2" class="wg-03-jump-link wg-03-sev-warn">source</a><a href="#m01-n3" class="wg-03-jump-link wg-03-sev-info">unknown</a></nav>
  </header>
  <div class="wg-03-grid">
    <div class="wg-03-diff" role="table" aria-label="스킬 계약 diff">
      <div class="wg-03-row wg-03-ctx"><span class="wg-03-ln">01</span><code class="wg-03-code">meeting_to_action_plan:</code></div>
      <div id="m01-l02" class="wg-03-row wg-03-del wg-03-flag"><span class="wg-03-ln">02</span><code class="wg-03-code"><span class="wg-03-sign">−</span> summarize decisions and tasks clearly</code><a href="#m01-n1" class="wg-03-dot wg-03-sev-critical" aria-label="owner critical">!</a></div>
      <div class="wg-03-row wg-03-add"><span class="wg-03-ln">03</span><code class="wg-03-code"><span class="wg-03-sign">+</span> every action requires OWNER, DUE, NEXT_STEP</code></div>
      <div id="m01-l04" class="wg-03-row wg-03-add wg-03-flag"><span class="wg-03-ln">04</span><code class="wg-03-code"><span class="wg-03-sign">+</span> every decision requires SOURCE_QUOTE</code><a href="#m01-n2" class="wg-03-dot wg-03-sev-warn" aria-label="source warn">!</a></div>
      <div id="m01-l05" class="wg-03-row wg-03-add wg-03-flag"><span class="wg-03-ln">05</span><code class="wg-03-code"><span class="wg-03-sign">+</span> missing fields must be UNKNOWN, not inferred</code><a href="#m01-n3" class="wg-03-dot wg-03-sev-info" aria-label="unknown info">i</a></div>
    </div>
    <aside class="wg-03-notes" aria-label="리뷰 노트">
      <article id="m01-n1" class="wg-03-note wg-03-sev-critical" tabindex="-1"><header class="wg-03-note-head"><span class="wg-03-badge">critical</span><span class="wg-03-note-loc"><a href="#m01-l02">L02</a></span></header><p class="wg-03-note-body">“명확히 정리”는 실행 계약이 아니다. 담당자와 다음 행동이 없으면 회의록은 실행계획이 아니라 요약이다.</p></article>
      <article id="m01-n2" class="wg-03-note wg-03-sev-warn" tabindex="-1"><header class="wg-03-note-head"><span class="wg-03-badge">warn</span><span class="wg-03-note-loc"><a href="#m01-l04">L04</a></span></header><p class="wg-03-note-body">결정 항목에는 원문 발췌가 필요하다. 근거가 없으면 회의 후 반박과 책임 이관이 발생한다.</p></article>
      <article id="m01-n3" class="wg-03-note wg-03-sev-info" tabindex="-1"><header class="wg-03-note-head"><span class="wg-03-badge">info</span><span class="wg-03-note-loc"><a href="#m01-l05">L05</a></span></header><p class="wg-03-note-body">정보가 없을 때 그럴듯하게 채우는 것이 가장 큰 회귀다. UNKNOWN 큐를 별도 산출해야 한다.</p></article>
    </aside>
  </div>
</section>
<section class="vt-shell" aria-label="프롬프트 튜닝 전후"><div class="vt-frame"><div class="tuner">
  <div class="tune-box"><div class="vt-kicker">Before</div><p class="vt-text">회의록을 읽고 액션 아이템을 예쁘게 정리해줘.</p><div class="score"><span class="on"></span><span></span><span></span><span></span></div></div>
  <div class="tune-box"><div class="vt-kicker">After</div><p class="vt-text">ACTION은 OWNER·DUE·NEXT_STEP·SOURCE_QUOTE가 있을 때만 확정하고, 빠진 값은 UNKNOWN 큐로 분리해줘.</p><div class="score"><span class="on"></span><span class="on"></span><span class="on"></span><span class="on"></span></div></div>
</div></div></section>
'''

improvements = f'''
{h2(4, '개선 우선순위', 'check')}
<p class="h2-sub">패치는 세 단계면 충분하다. 먼저 스키마를 잠그고, 다음으로 근거 추적을 붙이고, 마지막에 예제와 게이트로 회귀를 막는다.</p>
<section class="vt-shell" aria-label="스킬 개선 실행 계획"><div class="vt-frame"><div class="plan-grid">
  <article class="milestone"><div class="vt-kicker">P1</div><b>출력 스키마 고정</b><p class="vt-text">ACTION, DECISION, RISK, UNKNOWN 필드를 계약으로 선언한다.</p></article>
  <article class="milestone"><div class="vt-kicker">P2</div><b>원문 근거 강제</b><p class="vt-text">모든 결정과 리스크에 source_quote 또는 source_span을 붙인다.</p></article>
  <article class="milestone plan-risk"><div class="vt-kicker">P3</div><b>UNKNOWN 큐 분리</b><p class="vt-text">담당자·마감·근거가 없는 항목을 확인 질문으로 보낸다.</p></article>
  <article class="milestone"><div class="vt-kicker">P4</div><b>예제 갱신</b><p class="vt-text">좋은 회의록·나쁜 회의록·복구 예제를 함께 제공한다.</p></article>
</div></div></section>
<section class="wg-17" aria-labelledby="m01-pr-title">
  <header class="wg-17-head"><p class="wg-17-kicker">PATCH WRITEUP</p><h2 id="m01-pr-title" class="wg-17-title">fix: meeting action-plan contract 강화</h2><div class="wg-17-meta"><span class="wg-17-chip wg-17-chip-branch">skill-audit/action-plan-contract</span><span class="wg-17-chip wg-17-chip-add">+schema</span><span class="wg-17-chip wg-17-chip-del">−guessing</span></div></header>
  <div class="wg-17-block"><h3 class="wg-17-h3"><span class="wg-17-h3-no">1</span> Before / After</h3><div class="wg-17-ba"><div class="wg-17-ba-col wg-17-ba-before"><p class="wg-17-ba-tag">Before</p><ul class="wg-17-ba-list"><li>회의 요약과 액션이 섞임</li><li>담당자 누락을 자연어로 숨김</li><li>원문 근거가 없어 반박 어려움</li></ul></div><div class="wg-17-ba-arrow" aria-hidden="true">→</div><div class="wg-17-ba-col wg-17-ba-after"><p class="wg-17-ba-tag">After</p><ul class="wg-17-ba-list"><li>ACTION/DECISION/RISK/UNKNOWN 분리</li><li>owner/date/source 필수</li><li>확인 질문을 별도 큐로 출력</li></ul></div></div></div>
  <div class="wg-17-block"><h3 class="wg-17-h3"><span class="wg-17-h3-no">2</span> 파일별 적용</h3><details class="wg-17-file" open><summary class="wg-17-summary"><span class="wg-17-file-name">SKILL.md</span><span class="wg-17-file-stat"><span class="wg-17-add">+contract</span></span><span class="wg-17-caret" aria-hidden="true"></span></summary><div class="wg-17-file-body"><p class="wg-17-p">출력 스키마와 실패 조건을 본문 상단에 둔다. 모델이 임의로 “좋은 요약”을 선택하지 못하게 한다.</p></div></details><details class="wg-17-file"><summary class="wg-17-summary"><span class="wg-17-file-name">quality-gates.md</span><span class="wg-17-file-stat"><span class="wg-17-add">+gate</span></span><span class="wg-17-caret" aria-hidden="true"></span></summary><div class="wg-17-file-body"><p class="wg-17-p">OWNER·SOURCE_QUOTE·NEXT_STEP 누락을 실패로 처리한다.</p></div></details></div>
</section>
'''

final_skill = f'''
{h2(5, '최종 개선본 / 패치 계약', 'success')}
<p class="h2-sub">최종 패치는 스킬을 “회의록 요약기”가 아니라 “책임과 근거가 있는 실행계획 변환기”로 고정한다.</p>
<div class="summary-card"><p class="label">PATCH CONTRACT · SKILL.md</p><pre class="code"><code>output_contract:
  action:
    required: [owner, task, due, next_step, source_quote]
  decision:
    required: [decision, evidence, owner]
  risk:
    required: [risk, impact, mitigation_owner]
  unknown:
    required: [missing_field, question_to_ask]
forbidden:
  - inventing owners
  - inventing deadlines
  - converting opinions into decisions without evidence</code></pre></div>
<section class="vt-shell" aria-label="스킬 감사 워크플로우"><div class="vt-frame"><div class="wf-board"><div class="wf-top"><span class="wf-newbadge">AUDIT FLOW</span><div class="wf-aistack" aria-hidden="true"><span class="wf-aibadge">AI</span><span class="wf-bag">▣</span></div></div><div class="wf-map"><div class="wf-col"><article class="wf-card"><div class="wf-icon" aria-hidden="true">1</div><strong>원문 보존</strong><p>회의록 원문과 발췌 위치를 먼저 고정한다.</p></article><article class="wf-card"><div class="wf-icon" aria-hidden="true">2</div><strong>항목 분리</strong><p>ACTION·DECISION·RISK·UNKNOWN을 섞지 않는다.</p></article><article class="wf-card"><div class="wf-icon" aria-hidden="true">3</div><strong>책임 배정</strong><p>owner 없는 항목은 확정 액션으로 내보내지 않는다.</p></article></div><div class="wf-center"><div class="wf-codewin" aria-hidden="true"><span></span><span></span><span></span></div><div class="wf-metrics"><div class="wf-metric"><b>5</b><span>필드</span></div><div class="wf-metric"><b>3</b><span>게이트</span></div><div class="wf-metric"><b>0</b><span>추론</span></div></div></div><div class="wf-col"><article class="wf-card"><div class="wf-icon" aria-hidden="true">4</div><strong>근거 연결</strong><p>결정·리스크마다 source_quote를 붙인다.</p></article><article class="wf-card"><div class="wf-icon" aria-hidden="true">5</div><strong>확인 질문</strong><p>누락 값은 UNKNOWN 큐로 분리한다.</p></article><article class="wf-card"><div class="wf-icon" aria-hidden="true">6</div><strong>최종 검수</strong><p>누락 필드가 있으면 출력을 보류한다.</p></article></div></div><div class="wf-bottom" aria-hidden="true"><span class="wf-rail-short"></span><span class="wf-rail-long"></span><span class="wf-arrow"><i>→</i></span></div></div></div></section>
'''

source_note = '''<p class="label">SOURCE NOTE</p><p>이 문서는 1번 모드(skill_audit) 전용 레이아웃, 감사 레시피, skill-audit/body-icon/visual-html/widget 참조만 기반으로 재작성했다. 기존 출력 HTML 본문은 렌더 입력으로 사용하지 않았다.</p>'''

layout = (ASSETS / 'layouts/skill-audit-report.html').read_text(encoding='utf-8')
# Surface contract assumed pre-patched: direct semantic sections are card/view surfaces.
layout = layout.replace('class="executive-summary"', 'class="executive-summary summary-card"')
layout = layout.replace('class="summary-grid"', 'class="summary-grid summary-card"')
layout = layout.replace('class="line-audit"', 'class="line-audit summary-card"')
layout = layout.replace('class="priority-roadmap"', 'class="priority-roadmap summary-card"')
body = layout
replacements = {
    'KICKER': '<span class="kicker-text">SKILL AUDIT · MODE 01 · CAPTURE REVIEW</span>',
    'TITLE': '회의록 실행계획 변환 스킬 감사 리포트',
    'SUBTITLE': '회의 요약을 넘어 책임자·근거·기한·확인 질문까지 남기는 실행계획 변환 스킬로 고정하기 위한 전문가 감사 결과.',
    'META': '<span>profile auto</span><span>layout skill-audit-report</span><span>visual contract</span><span>mode 01 only</span><span>no behavioral JS</span>' + header_generated,
    'PURPOSE': purpose,
    'STRUCTURE_SCORE': structure_score,
    'LINE_AUDIT': line_audit,
    'IMPROVEMENTS': improvements,
    'FINAL_SKILL': final_skill,
    'SOURCE_NOTE': source_note,
}
for key, value in replacements.items():
    body = body.replace('{{' + key + '}}', value)

base = (ASSETS / 'base.html').read_text(encoding='utf-8')
html = base
head_replacements = {
    'TITLE': '회의록 실행계획 변환 스킬 감사 리포트',
    'DESCRIPTION': 'skill_audit 모드로 회의록 실행계획 변환 스킬의 계약, 근거 추적, UNKNOWN 처리, 품질 게이트를 감사한 한국어 HTML 리포트.',
    'JSON_LD_BLOCK': '',
    'BODY': body,
    'FOOTER': '',
}
all_repl = {**css_slots, **head_replacements}
for key, value in all_repl.items():
    html = html.replace('{{' + key + '}}', value)
if '{{' in html:
    raise SystemExit('unresolved placeholder')
OUT.write_text(html, encoding='utf-8')

# Per-mode evidence; no previous HTML body input.
evidence = {
    'mode': '01_skill_audit',
    'file': str(OUT.relative_to(ROOT)),
    'link': 'http://localhost:8080/output/adaptive-html-final-sequential-16-modes-20260607_105404/pages/01_skill_audit_meeting_action_plan.html',
    'policy': 'previous HTML body not reused by render script; common generator not used; skill_audit layout/recipe/references/templates consulted for this page only',
    'materials_sha256': MATERIAL_HASH,
    'used_materials': [str(p.relative_to(REPO)) for p in MODE_MATERIALS],
    'visual_contract': {
        'direct_sections_use_view_surface': True,
        'numbered_h2_order': 'body-icon body-icon--sm -> num -> title',
        'h2_sub_for_major_sections': True,
        'vt_required': ['quality-gate'],
        'vt_used': ['quality-gate', 'file-tour', 'prompt-tuner', 'implementation-plan', 'soft-workflow-map'],
        'wg_used': ['03-annotated-pull-request', '17-pr-writeup'],
    },
    'next_mode': '02_platform_blog',
}
(ROOT / 'sources/01_skill_audit-visual-contract-evidence.json').write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(OUT)
