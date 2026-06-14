#!/usr/bin/env python3
"""Mode 01 / 17 — skill_audit (independent build).
Topic: "회의록을 릴리스 노트로 자동 변환하는 스킬(meeting-to-release-notes) SKILL.md 감사"
Layout: skill-audit-report.html (.layout-audit) · auto · vt: quality-gate(qg-grid) · wg: wg-11, wg-17
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _finalize import build_page, write_sources, h2, SKILL, ASSETS  # noqa: E402,F401

for _p in [SKILL/"SKILL.md", SKILL/"references/skill-audit-system.md", SKILL/"references/layout-system.md",
           ASSETS/"layouts/skill-audit-report.html", ASSETS/"visual-html-templates/06-quality-gate.html",
           ASSETS/"widget-templates/11-weekly-status.html", ASSETS/"widget-templates/17-pr-writeup.html"]:
    _p.read_text(encoding="utf-8")

TITLE = "회의록 → 릴리스 노트 자동 변환 스킬 감사 리포트"
DESC = "skill_audit 모드로 meeting-to-release-notes 스킬의 트리거, 출력 계약, 워크플로우, 실패 처리, 품질 게이트를 진단하고 개선본까지 제시한 한국어 HTML 리포트."

header = '''
<header class="header audit-header">
  <div class="kicker"><span class="kicker-text">SKILL AUDIT · MODE 01 / 17 · 독립 빌드</span></div>
  <h1>회의록 → 릴리스 노트 자동 변환 스킬 감사</h1>
  <p class="sub">"meeting-to-release-notes" 스킬이 회의 요약기에서 멈추지 않고, 책임자·근거·버전 경계까지 강제하는 릴리스 노트 생성기로 동작하는지 라인 단위로 진단한다.</p>
  <div class="meta"><span>profile auto</span><span>layout skill-audit-report</span><span>대상 SKILL.md v0.4 (가상)</span><span>무 동작 JS</span></div>
  <div class="generated-row"><p class="generated-date">Generated · 2026-06-13 KST</p>
  <div class="lens-strip" aria-label="적용 렌즈"><span class="lens-strip-label">LENS</span><span class="lens-chip">출력 계약</span><span class="lens-chip">근거 추적</span><span class="lens-chip">실패 모드</span><span class="lens-chip">버전 경계</span><span class="lens-chip">품질 게이트</span></div></div>
</header>'''

toc = '''
<nav class="toc-map audit-toc" aria-label="감사 목차"><div class="toc-pills">
  <a class="toc-pill" href="#s1"><b>01</b> 총평과 판정</a><a class="toc-pill" href="#s2"><b>02</b> 트리거·활성화 점수</a>
  <a class="toc-pill" href="#s3"><b>03</b> 워크플로우 커버리지</a><a class="toc-pill" href="#s4"><b>04</b> 라인·섹션 진단</a>
  <a class="toc-pill" href="#s5"><b>05</b> 출력 계약의 빈틈</a><a class="toc-pill" href="#s6"><b>06</b> 실패 모드 처리</a>
  <a class="toc-pill" href="#s7"><b>07</b> 개선 로드맵</a><a class="toc-pill" href="#s8"><b>08</b> 패치 작성본</a>
  <a class="toc-pill" href="#s9"><b>09</b> 검증 게이트</a><a class="toc-pill" href="#s10"><b>10</b> 도입 주간 상태</a>
  <a class="toc-pill" href="#snext"><b>→</b> 최종 판정·다음 행동</a>
</div></nav>'''

s1 = f'''
<section id="s1" class="executive-summary summary-card">
  {h2("01","총평과 판정","audit")}
  <p class="h2-sub">방향은 옳다. 그러나 "릴리스 노트"라는 결과물의 정의가 약해, 같은 입력에서 회의 요약과 배포 공지가 뒤섞인 산출이 나온다. 출력 계약을 잠그기 전에는 운영에 올리기 어렵다.</p>
  <div class="grid-3">
    <article class="score-card"><h3>현재 강점</h3><p>회의 원문에서 결정·변경·후속 작업을 분리하려는 의도가 분명하고, 사용자가 원하는 산출이 "요약"이 아니라 "배포 가능한 릴리스 노트"라는 점이 description에 드러난다.</p></article>
    <article class="score-card"><h3>핵심 결함</h3><p>CHANGE / FIX / BREAKING / OWNER / TICKET 필드가 필수 계약으로 잠겨 있지 않다. 모델이 말투 좋은 변경 요약을 만들고도 호환성 깨짐과 책임자를 누락할 수 있다.</p></article>
    <article class="score-card"><h3>판정</h3><p><strong>조건부 보류.</strong> 출력 스키마 고정 · 근거 추적 · UNKNOWN 큐 분리 세 가지를 패치하면 운영 승급 가능. 현 상태로는 사람 검수가 매번 필요하다.</p></article>
  </div>
  <div class="callout"><p><strong>한 줄 결론.</strong> 이 스킬은 "회의록 요약기"와 "릴리스 노트 생성기" 사이에서 정체성이 흔들린다. 릴리스 노트의 최소 단위(변경 1건 = 분류·영향·근거·책임)를 계약으로 박는 순간 가치가 분명해진다.</p></div>
</section>'''

s2 = f'''
<section id="s2" class="summary-grid summary-card">
  {h2("02","트리거·활성화 점수","metric")}
  <p class="h2-sub">"바로 운영에 쓸 수 있는가" 기준으로 채점했다. 의도는 높지만 활성화 경계와 입력 가드가 약해 오작동 여지가 남는다.</p>
  <div class="table-scroll"><table>
    <caption>meeting-to-release-notes 스킬 활성화·계약 점수표</caption>
    <thead><tr><th>항목</th><th>점수</th><th>판정 근거</th><th>필수 보완</th></tr></thead>
    <tbody>
      <tr><th>목적·트리거</th><td>4 / 5</td><td>"회의록을 릴리스 노트로" 트리거는 명확하나 단순 "요약" 요청과 겹친다</td><td>요약 모드와의 분기 문구 추가</td></tr>
      <tr><th>출력 스키마</th><td>2 / 5</td><td>필드 후보는 있으나 required/optional 구분과 검증이 없다</td><td>CHANGE·FIX·BREAKING·OWNER·TICKET required 고정</td></tr>
      <tr><th>근거 추적</th><td>2 / 5</td><td>각 항목이 회의 원문 어디서 왔는지 연결되지 않는다</td><td>source_quote 또는 발언 타임코드 필수</td></tr>
      <tr><th>버전 경계</th><td>1 / 5</td><td>호환성 깨짐(BREAKING)과 마이그레이션 안내 개념이 없다</td><td>BREAKING 항목엔 migration 노트 강제</td></tr>
      <tr><th>실패 대응</th><td>2 / 5</td><td>정보 부족 시 추론으로 메우는 경향</td><td>확인 필요 항목을 UNKNOWN 큐로 분리</td></tr>
    </tbody>
  </table></div>
  <section class="vt-shell" aria-label="릴리스 노트 변환 품질 게이트">
    <div class="vt-frame"><div><div class="qg-grid">
      <div class="qg-card"><b>분류</b><p class="vt-text">모든 항목은 CHANGE / FIX / BREAKING 중 하나로 분류한다.</p></div>
      <div class="qg-card"><b>책임</b><p class="vt-text">OWNER 또는 TICKET이 없으면 항목이 아니라 메모로 강등한다.</p></div>
      <div class="qg-card warn"><b>호환성</b><p class="vt-text">BREAKING은 migration 안내가 없으면 발행을 보류한다.</p></div>
      <div class="qg-card warn"><b>UNKNOWN</b><p class="vt-text">원문에 없는 버전·날짜·수치는 추론하지 않고 확인 필요로 둔다.</p></div>
    </div><div class="qg-final"><span class="qg-final-label">AUDIT GATE</span>요약 스킬이 아니라 릴리스 노트 생성 스킬로 정의를 강화해야 통과한다.</div></div></div>
  </section>
</section>'''

s3 = f'''
<section id="s3" class="summary-card">
  {h2("03","워크플로우 커버리지","flow")}
  <p class="h2-sub">파이프라인은 입력 정규화 → 항목 추출 → 분류·근거 매핑 → 렌더 순서를 따라야 한다. 현재는 추출과 렌더만 명시되어 있고 중간 계약이 비어 있다.</p>
  <section class="vt-shell" aria-label="스킬 파일 투어">
    <div class="vt-frame"><div class="ft">
      <article class="ft-card"><div class="ft-head"><span>SKILL.md</span><span>contract</span></div><div class="ft-body"><p class="vt-text">출력 스키마와 실패 조건을 정의하는 중심 문서.</p><div class="ft-note"><b>Review note</b><br>required 필드와 분기 문구를 상단에 고정해야 한다.</div></div></article>
      <article class="ft-card"><div class="ft-head"><span>recipes/notes.md</span><span>flow</span></div><div class="ft-body"><p class="vt-text">추출 → 분류 → 렌더 절차 레시피.</p><div class="ft-note"><b>Review note</b><br>분류·근거 매핑 단계가 누락돼 추출과 렌더 사이가 빈다.</div></div></article>
      <article class="ft-card"><div class="ft-head"><span>quality-gates.md</span><span>gate</span></div><div class="ft-body"><p class="vt-text">발행 전 검증 기준.</p><div class="ft-note"><b>Review note</b><br>OWNER·BREAKING migration 누락을 실패로 승격해야 한다.</div></div></article>
    </div></div>
  </section>
  <p>요약하면 <strong>중간 계약(분류·근거 매핑) 단계</strong>가 문서에 없다. 이 단계가 비면 모델은 변경 사항을 그럴듯한 문장으로 합치는 쪽으로 흐르고, 항목 단위 추적성이 사라진다. 추출과 렌더만으로는 "보기 좋은 요약"은 되지만 "추적 가능한 릴리스 노트"는 되지 못한다.</p>
</section>'''

s4 = f'''
<section id="s4" class="line-audit summary-card">
  {h2("04","라인·섹션 진단","warning")}
  <p class="h2-sub">문제는 문장 표현이 아니라 계약 누락이다. SKILL.md 본문에 반드시 들어가야 할 세 규칙을 Before/After로 정리했다.</p>
  <div class="ba">
    <div class="ba-col ba-before"><p class="ba-label">Before — 현재 SKILL.md</p><ul><li>"회의록을 읽고 릴리스 노트로 정리한다"</li><li>항목 분류·책임자 개념 없음</li><li>호환성 깨짐을 일반 변경과 동일 취급</li><li>정보가 없으면 자연스럽게 메움</li></ul></div>
    <div class="ba-arrow" aria-hidden="true">→</div>
    <div class="ba-col ba-after"><p class="ba-label">After — 제안 계약</p><ul><li>변경 1건 = 〈분류·영향·근거·책임〉 4필드 필수</li><li>OWNER 또는 TICKET 없으면 항목 제외</li><li>BREAKING은 migration 노트 동반</li><li>빈 값은 UNKNOWN 큐로 분리 출력</li></ul></div>
  </div>
  <p>세 규칙은 표현 다듬기가 아니라 <strong>산출물의 신뢰성</strong>을 결정한다. 릴리스 노트는 배포 후 분쟁의 1차 근거가 되므로, 근거 없는 항목은 노트가 아니라 추측이다.</p>
</section>'''

s5 = f'''
<section id="s5" class="summary-card">
  {h2("05","출력 계약의 빈틈","security")}
  <p class="h2-sub">현재 스키마가 비워 둔 자리마다 운영 사고가 들어온다. 심각도 순으로 정리했다.</p>
  <div class="card-grid">
    <article class="mini-card"><span class="case-label">치명</span><h3>OWNER 누락</h3><p>책임자 없는 변경 항목은 회수·문의 대상이 불명확해진다. 사후 추적 비용이 가장 크다.</p></article>
    <article class="mini-card"><span class="case-label">치명</span><h3>BREAKING 미표기</h3><p>호환성 깨짐이 일반 개선과 같은 줄에 묻히면 소비 측이 무방비로 업그레이드한다.</p></article>
    <article class="mini-card"><span class="case-label">경고</span><h3>근거 단절</h3><p>회의 발언과 항목이 연결되지 않아, 검수자가 원문을 다시 뒤져야 한다.</p></article>
    <article class="mini-card"><span class="case-label">경고</span><h3>추론 혼입</h3><p>원문에 없는 날짜·버전을 모델이 채우면 노트가 사실처럼 읽히는 허위가 된다.</p></article>
  </div>
  <div class="danger"><span class="label">위험</span><p>네 빈틈은 모두 "그럴듯해서 통과되는" 종류다. 정적 검수로는 잘 안 걸리고, 배포 후에야 드러난다. 그래서 출력 단계가 아니라 <strong>계약 단계</strong>에서 막아야 한다.</p></div>
</section>'''

s6 = f'''
<section id="s6" class="summary-card">
  {h2("06","실패 모드 처리","check")}
  <p class="h2-sub">좋은 변환 스킬은 "정보가 없을 때 무엇을 하지 않는가"로 갈린다. 입력 결손 시의 정본 동작을 체크리스트로 고정한다.</p>
  <ul class="check-list">
    <li><strong>책임자 불명</strong> — 항목을 UNKNOWN 큐로 보내고 "담당 확인 필요"로 표시한다. 임의 지정 금지.</li>
    <li><strong>버전 미상</strong> — 릴리스 버전을 추정하지 않고 <code>vUNKNOWN</code>로 두고 발행 보류 사유에 기록한다.</li>
    <li><strong>분류 모호</strong> — CHANGE/FIX/BREAKING 판단이 어려우면 보수적으로 BREAKING 후보로 올려 검수 대상에 둔다.</li>
    <li><strong>근거 없음</strong> — 회의 원문 매핑이 없는 문장은 노트에 싣지 않고 "출처 확인 필요"로 분리한다.</li>
  </ul>
  <div class="good"><span class="label">권장</span><p>핵심 원칙은 단순하다. <strong>모르면 만들지 말고 큐에 쌓는다.</strong> 확인 큐가 비어 있는 노트만 자동 발행 후보가 된다.</p></div>
</section>'''

s7 = f'''
<section id="s7" class="priority-roadmap summary-card">
  {h2("07","개선 로드맵","timeline")}
  <p class="h2-sub">패치는 세 단계면 충분하다. 스키마를 잠그고, 근거를 강제하고, 게이트와 예제로 회귀를 막는다.</p>
  <div class="plan-grid">
    <article class="milestone"><div class="vt-kicker">P1</div><b>출력 스키마 고정</b><p>CHANGE·FIX·BREAKING·OWNER·TICKET·migration 필드를 required로 선언하고 빈 값은 UNKNOWN 큐로 라우팅한다.</p></article>
    <article class="milestone"><div class="vt-kicker">P2</div><b>근거 추적 강제</b><p>모든 항목에 source_quote 또는 발언 타임코드를 붙인다. 근거 없는 항목은 렌더에서 제외한다.</p></article>
    <article class="milestone plan-risk"><div class="vt-kicker">P3</div><b>게이트·예제 정비</b><p>OWNER/BREAKING 누락을 실패로 처리하는 quality gate와, 좋은/나쁜/복구 릴리스 노트 예제 3종을 추가한다.</p></article>
  </div>
  <p>세 단계는 의존 순서가 있다. 스키마 없이 근거를 강제하면 형식 충돌이 나고, 게이트는 두 가지가 자리 잡은 뒤에야 의미가 있다.</p>
</section>'''

s8 = f'''
<section id="s8" class="summary-card">
  {h2("08","패치 작성본","edit")}
  <p class="h2-sub">P1·P2를 하나의 변경으로 묶은 패치 초안이다. SKILL.md 상단 계약과 레시피, 게이트가 함께 바뀐다.</p>
  <section class="wg-17" aria-labelledby="m01-pr-title">
    <header class="wg-17-head"><p class="wg-17-kicker">PATCH · skill-audit</p><h2 id="m01-pr-title" class="wg-17-title">fix: 릴리스 노트 출력 계약과 근거 추적 강제</h2><div class="wg-17-meta"><span class="wg-17-chip wg-17-chip-branch">audit/release-notes-contract → main</span><span class="wg-17-chip">파일 3개</span><span class="wg-17-chip wg-17-chip-add">+schema</span><span class="wg-17-chip wg-17-chip-del">−guessing</span></div></header>
    <div class="wg-17-block"><h3 class="wg-17-h3"><span class="wg-17-h3-no">1</span> 동기 (왜?)</h3><p class="wg-17-p">현재 스킬은 회의 요약과 릴리스 노트를 구분하지 않아 검수자가 매번 원문을 재확인해야 한다. 출력 계약을 잠그고 근거를 강제해 자동 발행 후보를 만들 수 있게 한다.</p></div>
    <div class="wg-17-block"><h3 class="wg-17-h3"><span class="wg-17-h3-no">2</span> Before / After</h3><div class="wg-17-ba">
      <div class="wg-17-ba-col wg-17-ba-before"><p class="wg-17-ba-tag">Before</p><ul class="wg-17-ba-list"><li>변경·요약이 한 문단에 섞임</li><li>책임자·티켓 누락을 자연어로 숨김</li><li>호환성 깨짐 구분 없음</li></ul></div>
      <div class="wg-17-ba-arrow" aria-hidden="true">→</div>
      <div class="wg-17-ba-col wg-17-ba-after"><p class="wg-17-ba-tag">After</p><ul class="wg-17-ba-list"><li>항목별 분류·영향·근거·책임 4필드</li><li>OWNER/TICKET 필수, 빈 값은 UNKNOWN 큐</li><li>BREAKING은 migration 노트 동반</li></ul></div>
    </div></div>
    <div class="wg-17-block"><h3 class="wg-17-h3"><span class="wg-17-h3-no">3</span> 파일별 워크스루</h3>
      <p class="wg-17-hint">각 항목을 펼쳐 변경 의도를 확인하세요.</p>
      <details class="wg-17-file" open><summary class="wg-17-summary"><span class="wg-17-file-name">SKILL.md</span><span class="wg-17-file-stat"><span class="wg-17-add">+contract</span></span><span class="wg-17-caret" aria-hidden="true"></span></summary><div class="wg-17-file-body"><p class="wg-17-p">상단에 출력 스키마와 실패 조건을 명시한다. 모델이 임의로 "좋은 요약"을 선택하지 못하도록 required 필드를 잠근다.</p><ul class="wg-17-file-pts"><li>required: change_type, impact, source, owner</li><li>BREAKING이면 migration 필드 강제</li></ul></div></details>
      <details class="wg-17-file"><summary class="wg-17-summary"><span class="wg-17-file-name">recipes/notes.md</span><span class="wg-17-file-stat"><span class="wg-17-add">+map</span></span><span class="wg-17-caret" aria-hidden="true"></span></summary><div class="wg-17-file-body"><p class="wg-17-p">추출과 렌더 사이에 분류·근거 매핑 단계를 추가한다. 항목별로 회의 발언과 연결한다.</p></div></details>
      <details class="wg-17-file"><summary class="wg-17-summary"><span class="wg-17-file-name">quality-gates.md</span><span class="wg-17-file-stat"><span class="wg-17-add">+gate</span></span><span class="wg-17-caret" aria-hidden="true"></span></summary><div class="wg-17-file-body"><p class="wg-17-p">OWNER 누락·BREAKING migration 누락·근거 없는 항목을 실패로 처리한다.</p></div></details>
    </div>
  </section>
</section>'''

s9 = f'''
<section id="s9" class="summary-card">
  {h2("09","검증 게이트","success")}
  <p class="h2-sub">패치가 회귀하지 않도록 발행 전 자동 게이트를 둔다. 완료 기준·증빙·판정만 담는다.</p>
  <div class="table-scroll"><table>
    <caption>릴리스 노트 발행 전 검증 게이트</caption>
    <thead><tr><th>게이트</th><th>완료 기준</th><th>증빙</th><th>실패 시</th></tr></thead>
    <tbody>
      <tr><th>스키마</th><td>required 필드 모두 채움</td><td>스키마 검증 통과 로그</td><td>발행 차단 + 누락 필드 리포트</td></tr>
      <tr><th>근거</th><td>항목마다 source 존재</td><td>항목↔발언 매핑 표</td><td>근거 없는 항목 큐로 이동</td></tr>
      <tr><th>호환성</th><td>BREAKING에 migration 동반</td><td>migration 노트 링크</td><td>BREAKING 발행 보류</td></tr>
      <tr><th>UNKNOWN</th><td>확인 큐가 비어 있음</td><td>UNKNOWN 큐 카운트 0</td><td>수동 검수 대상으로 강등</td></tr>
    </tbody>
  </table></div>
  <p>게이트는 "사람이 보기 좋은 체크리스트"가 아니라 <strong>실패하면 발행이 멈추는 계약</strong>이어야 한다. 통과 로그가 곧 릴리스 노트의 신뢰 근거가 된다.</p>
</section>'''

s10 = f'''
<section id="s10" class="summary-card">
  {h2("10","도입 주간 상태","database")}
  <p class="h2-sub">패치 적용을 1개 마일스톤으로 운영한 3주차 가상 상태판이다. 스키마·근거는 자리 잡았고 게이트 자동화가 남았다.</p>
  <section class="wg-11" aria-labelledby="m01-ws-title">
    <header class="wg-11-head"><p class="wg-11-kicker">주간 상태 리포트</p><h2 id="m01-ws-title" class="wg-11-h">릴리스 노트 계약 도입 · M1 3주차</h2><p class="wg-11-lead">스키마 적용 <strong>100%</strong> · 근거 매핑 진행 · 게이트 자동화 리스크 1건</p></header>
    <div class="wg-11-kpis">
      <div class="wg-11-kpi wg-11-kpi-good"><span class="wg-11-kpi-v">100%</span><span class="wg-11-kpi-l">스키마 적용</span></div>
      <div class="wg-11-kpi wg-11-kpi-prog"><span class="wg-11-kpi-v">2</span><span class="wg-11-kpi-l">진행 작업</span></div>
      <div class="wg-11-kpi wg-11-kpi-risk"><span class="wg-11-kpi-v wg-11-warn">1</span><span class="wg-11-kpi-l">리스크</span></div>
      <div class="wg-11-kpi"><span class="wg-11-kpi-v">0</span><span class="wg-11-kpi-l">차단됨</span></div>
    </div>
    <h3 class="wg-11-h3">워크스트림 진척도</h3>
    <div class="wg-11-bars">
      <div class="wg-11-bar-row"><span class="wg-11-bar-label">출력 스키마</span><div class="wg-11-track" role="img" aria-label="출력 스키마 진척 100퍼센트"><div class="wg-11-fill wg-11-fill-good" style="width:100%"></div></div><span class="wg-11-bar-pct">100%</span></div>
      <div class="wg-11-bar-row"><span class="wg-11-bar-label">근거 매핑</span><div class="wg-11-track" role="img" aria-label="근거 매핑 진척 70퍼센트"><div class="wg-11-fill wg-11-fill-prog" style="width:70%"></div></div><span class="wg-11-bar-pct">70%</span></div>
      <div class="wg-11-bar-row"><span class="wg-11-bar-label">게이트 자동화</span><div class="wg-11-track" role="img" aria-label="게이트 자동화 진척 35퍼센트, 리스크"><div class="wg-11-fill wg-11-fill-risk" style="width:35%"></div></div><span class="wg-11-bar-pct">35%</span></div>
    </div>
    <div class="wg-11-cols">
      <div class="wg-11-col wg-11-col-good"><h4 class="wg-11-col-h"><span class="wg-11-dot"></span>완료</h4><ul class="wg-11-col-list"><li>required 스키마 고시 <span class="wg-11-tk">RN-04</span></li><li>UNKNOWN 큐 분리 <span class="wg-11-tk">RN-07</span></li></ul></div>
      <div class="wg-11-col wg-11-col-prog"><h4 class="wg-11-col-h"><span class="wg-11-dot"></span>진행 중</h4><ul class="wg-11-col-list"><li>발언↔항목 매핑 뷰 <span class="wg-11-tk">RN-11</span></li><li>예제 3종 작성 <span class="wg-11-tk">RN-12</span></li></ul></div>
      <div class="wg-11-col wg-11-col-risk"><h4 class="wg-11-col-h"><span class="wg-11-dot"></span>리스크</h4><ul class="wg-11-col-list"><li><strong>게이트 자동화</strong> — CI 연결 지연 우려 <span class="wg-11-flag">에스컬레이션</span> <span class="wg-11-tk">RN-15</span></li></ul></div>
    </div>
  </section>
</section>'''

snext = f'''
<section id="snext" class="try">
  {h2(None,"최종 판정 · 다음 행동","landing")}
  <p>이 스킬은 좋은 출발점이지만, 지금 그대로면 "예쁜 회의 요약기"에 머문다. 릴리스 노트의 최소 단위를 계약으로 박는 순간, 검수 부담이 줄고 자동 발행이 가능해진다.</p>
  <div class="cta-box">
    <p><strong>승급 조건</strong> — 아래 세 가지가 끝나면 조건부 보류를 해제하고 운영 승급을 권고한다.</p>
    <ol><li>출력 스키마(분류·영향·근거·책임) required 고정 + UNKNOWN 큐 분리</li><li>항목별 근거(발언/타임코드) 강제, 근거 없는 항목 렌더 제외</li><li>OWNER·BREAKING migration 누락을 실패로 처리하는 게이트 + 예제 3종</li></ol>
    <div class="tag-list"><span class="tag">skill_audit</span><span class="tag">release-notes</span><span class="tag">output-contract</span><span class="tag">조건부 보류</span></div>
  </div>
</section>'''

source_note = '<aside class="source-note"><p><strong>출처·범위.</strong> 본 감사는 "meeting-to-release-notes"라는 가상의 스킬 SKILL.md(v0.4)를 대상으로 한 구조·계약 진단이다. 특정 실제 제품·저장소를 평가한 것이 아니며, 점수와 일정은 운영 승급 판단을 돕기 위한 진단용 추정치다. 실제 도입 시 대상 스킬의 입력 샘플로 재검증이 필요하다.</p></aside>'

body = ('<main id="main" class="page-wide layout-audit">' + header + toc + s1+s2+s3+s4+s5+s6+s7+s8+s9+s10+snext + source_note + '</main>')
out = build_page("pages/01_skill_audit_meeting_to_release_notes.html", title=TITLE, description=DESC, body=body)
write_sources()
print("WROTE", out)
