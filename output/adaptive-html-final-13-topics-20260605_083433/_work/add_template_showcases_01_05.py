#!/usr/bin/env python3
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "pages"


def showcase(name: str, body: str) -> str:
    return f'\n<!-- template-showcase:start {name} -->\n<div class="summary-card template-showcase"><div class="label">TEMPLATE CHECK · {name}</div>\n{body.strip()}\n</div>\n<!-- template-showcase:end {name} -->\n'


def strip_existing(text: str) -> str:
    return re.sub(
        r'\n?<!-- template-showcase:start [^>]+ -->[\s\S]*?<!-- template-showcase:end [^>]+ -->\n?',
        '\n',
        text,
    )


def insert_into_numbered_section(text: str, section_no: int, snippet: str) -> str:
    pattern = rf'(<section[^>]*><h2><span class="no">{section_no}</span>[\s\S]*?)(</section>)'
    updated, count = re.subn(pattern, rf'\1{snippet}\2', text, count=1)
    if count != 1:
        raise RuntimeError(f"section {section_no} replacement failed: {count}")
    return updated


WG10_RAG_SHEET = showcase("wg-10 svg-figure-sheet", """
<section class="wg-10-sheet" aria-label="RAG 구성요소 아이콘 시트">
  <h3 class="wg-10-h">RAG 구성요소 아이콘 시트</h3>
  <div class="wg-10-grid">
    <figure class="wg-10-fig"><div class="wg-10-stage"><svg viewBox="0 0 120 120" role="img" aria-labelledby="rag-wg10-t1" class="wg-10-svg"><title id="rag-wg10-t1">문서 금고</title><rect x="28" y="24" width="64" height="72" rx="8" fill="var(--card)" stroke="var(--ink)" stroke-width="3"/><path d="M42 44h36M42 60h28M42 76h32" stroke="var(--accent)" stroke-width="4" stroke-linecap="round"/></svg></div><figcaption class="wg-10-cap"><strong>문서 금고</strong><span>원문·출처·날짜 보존</span></figcaption></figure>
    <figure class="wg-10-fig"><div class="wg-10-stage"><svg viewBox="0 0 120 120" role="img" aria-labelledby="rag-wg10-t2" class="wg-10-svg"><title id="rag-wg10-t2">청크 조각</title><rect x="18" y="30" width="38" height="28" rx="6" fill="var(--term-bg)" stroke="var(--term-accent)" stroke-width="2"/><rect x="64" y="30" width="38" height="28" rx="6" fill="var(--term-bg)" stroke="var(--term-accent)" stroke-width="2"/><rect x="41" y="68" width="38" height="28" rx="6" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/></svg></div><figcaption class="wg-10-cap"><strong>청크 설계</strong><span>질문에 답할 단위</span></figcaption></figure>
    <figure class="wg-10-fig"><div class="wg-10-stage"><svg viewBox="0 0 120 120" role="img" aria-labelledby="rag-wg10-t3" class="wg-10-svg"><title id="rag-wg10-t3">검색 회수</title><circle cx="52" cy="52" r="24" fill="var(--analogy-bg)" stroke="var(--analogy-accent)" stroke-width="3"/><path d="M70 70l24 24" stroke="var(--ink)" stroke-width="6" stroke-linecap="round"/><circle cx="52" cy="52" r="8" fill="var(--accent)"/></svg></div><figcaption class="wg-10-cap"><strong>검색 회수</strong><span>상위 근거 조각 확인</span></figcaption></figure>
    <figure class="wg-10-fig"><div class="wg-10-stage"><svg viewBox="0 0 120 120" role="img" aria-labelledby="rag-wg10-t4" class="wg-10-svg"><title id="rag-wg10-t4">근거 답변</title><path d="M24 30h72v42H54L38 90V72H24z" fill="var(--good-bg)" stroke="var(--good-label-ink)" stroke-width="3"/><path d="M40 48h42M40 60h28" stroke="var(--good-label-ink)" stroke-width="4" stroke-linecap="round"/></svg></div><figcaption class="wg-10-cap"><strong>근거 답변</strong><span>출처·한계·모름 표시</span></figcaption></figure>
  </div>
</section>
""")


WG13_RAG_FLOW = showcase("wg-13 annotated-flowchart", """
<section class="wg-13-fc" aria-label="RAG 검색 우선 플로우차트">
  <h3 class="wg-13-h">RAG 검색 우선 플로우 <span class="wg-13-sub">답변 전 검색 품질 확인</span></h3>
  <div class="wg-13-flow">
    <a href="#rag-wg13-s1" class="wg-13-node wg-13-node--start"><span class="wg-13-step">시작</span>질문 입력</a><span class="wg-13-arrow" aria-hidden="true">&darr;</span>
    <a href="#rag-wg13-s2" class="wg-13-node"><span class="wg-13-step">1</span>상위 청크 3개 검색</a><span class="wg-13-arrow" aria-hidden="true">&darr;</span>
    <a href="#rag-wg13-s3" class="wg-13-node wg-13-node--decide"><span class="wg-13-step">2</span>근거가 맞는가?</a>
    <div class="wg-13-paths"><div class="wg-13-path wg-13-path--fail"><span class="wg-13-edge">아니오 → 실패 경로</span><a href="#rag-wg13-fail" class="wg-13-node wg-13-node--fail"><span class="wg-13-step">!</span>청크·질문 수정</a></div><div class="wg-13-path wg-13-path--ok"><span class="wg-13-edge">예 → 정상 경로</span><a href="#rag-wg13-ok" class="wg-13-node wg-13-node--end"><span class="wg-13-step">완료</span>출처 포함 답변</a></div></div>
  </div>
  <div class="wg-13-detail">
    <details id="rag-wg13-s2" class="wg-13-acc" open><summary><span class="wg-13-tag">검색</span>검색 결과를 먼저 읽기</summary><div class="wg-13-body"><p>답변 생성 전에 실제 검색 조각이 질문과 맞는지 사람이 확인한다.</p></div></details>
    <details id="rag-wg13-fail" class="wg-13-acc wg-13-acc--fail"><summary><span class="wg-13-tag wg-13-tag--fail">실패</span>검색 실패 원인 분리</summary><div class="wg-13-body"><p>문서 없음, 청크 불량, 검색 표현 불일치, 생성 오류를 나눠 기록한다.</p></div></details>
    <details id="rag-wg13-ok" class="wg-13-acc wg-13-acc--ok"><summary><span class="wg-13-tag wg-13-tag--ok">통과</span>출처 포함 답변</summary><div class="wg-13-body"><p>검색된 근거만 사용하고 모르는 부분은 모른다고 표시한다.</p></div></details>
  </div>
</section>
""")


WG15_RAG_CONCEPT = showcase("wg-15 concept-explainer", """
<section class="wg-15" aria-labelledby="rag-wg15-title">
  <p class="wg-15-kicker">개념 교보재 · 로컬 RAG</p>
  <h2 id="rag-wg15-title" class="wg-15-h">검색 품질이 답변 품질을 끌고 간다</h2>
  <p class="wg-15-lead">답변이 틀릴 때는 모델 교체보다 검색된 근거가 질문과 맞는지 먼저 본다.</p>
  <div class="wg-15-steps">
    <input type="radio" name="wg-15-step" id="wg-15-s1" class="wg-15-step-in" checked>
    <input type="radio" name="wg-15-step" id="wg-15-s2" class="wg-15-step-in">
    <input type="radio" name="wg-15-step" id="wg-15-s3" class="wg-15-step-in">
    <div class="wg-15-stepnav"><label class="wg-15-stepbtn" for="wg-15-s1"><span class="wg-15-stepnum">1</span> 원문</label><label class="wg-15-stepbtn" for="wg-15-s2"><span class="wg-15-stepnum">2</span> 검색</label><label class="wg-15-stepbtn" for="wg-15-s3"><span class="wg-15-stepnum">3</span> 답변</label></div>
    <div class="wg-15-stage"><div class="wg-15-ring" aria-hidden="true"><span class="wg-15-node wg-15-na">문</span><span class="wg-15-node wg-15-nb">청</span><span class="wg-15-node wg-15-nc">검</span><span class="wg-15-node wg-15-nd wg-15-new">답</span><span class="wg-15-key wg-15-k1">Q</span><span class="wg-15-key wg-15-k2">근거</span><span class="wg-15-center">RAG</span></div><div class="wg-15-panels"><div class="wg-15-panel wg-15-p1"><h4 class="wg-15-pt">원문을 버리지 않는다</h4><p>요약본만 남기면 누락과 해석이 섞인다. 원문 위치와 날짜를 보존한다.</p></div><div class="wg-15-panel wg-15-p2"><h4 class="wg-15-pt">검색 결과를 사람이 본다</h4><p>상위 조각 3개가 질문과 맞는지 먼저 확인한다.</p></div><div class="wg-15-panel wg-15-p3"><h4 class="wg-15-pt">근거 밖은 추측으로 둔다</h4><p>답변은 출처, 한계, 모르는 부분을 함께 드러낸다.</p></div></div></div>
  </div>
</section>
""")


WG04_GATEWAY_MAP = showcase("wg-04 module-map", """
<section class="wg-04" aria-labelledby="gate-wg04-title">
  <header class="wg-04-head"><p class="wg-04-kicker">ARCHITECTURE TEMPLATE</p><h2 id="gate-wg04-title" class="wg-04-title">AI 리뷰 게이트웨이 모듈 맵</h2><p class="wg-04-lead"><strong class="wg-04-crit-word">붉은 굵은 경로</strong>는 병합 판정에 직접 영향을 주는 critical path다.</p></header>
  <div class="wg-04-diagram"><svg viewBox="0 0 640 300" class="wg-04-svg" role="img" aria-labelledby="gate-wg04-svg-t"><title id="gate-wg04-svg-t">PR 이벤트에서 품질 게이트까지의 모듈 맵</title><defs><marker id="gate-wg04-arrow" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="var(--ink-mute)"></path></marker><marker id="gate-wg04-arrow-crit" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="var(--accent)"></path></marker></defs><path class="wg-04-edge wg-04-edge-crit" d="M120,70 L250,150" marker-end="url(#gate-wg04-arrow-crit)"></path><path class="wg-04-edge wg-04-edge-crit" d="M330,150 L470,70" marker-end="url(#gate-wg04-arrow-crit)"></path><path class="wg-04-edge" d="M330,170 L480,210" marker-end="url(#gate-wg04-arrow)"></path><g class="wg-04-node wg-04-node-entry"><rect x="60" y="40" width="120" height="40" rx="8"></rect><text x="120" y="65">PR 이벤트</text></g><g class="wg-04-node wg-04-node-core wg-04-node-crit"><rect x="230" y="140" width="130" height="44" rx="8"></rect><text x="295" y="166">정책 라우터</text></g><g class="wg-04-node wg-04-node-core wg-04-node-crit"><rect x="430" y="40" width="130" height="44" rx="8"></rect><text x="495" y="66">게이트 판정</text></g><g class="wg-04-node wg-04-node-leaf"><rect x="430" y="200" width="130" height="44" rx="8"></rect><text x="495" y="226">감사 로그</text></g></svg></div>
  <div class="wg-04-path" role="note"><span class="wg-04-path-label">핵심 경로</span><span class="wg-04-path-chain"><code>PR</code> → <code>정책</code> → <code>판정</code></span><span class="wg-04-path-note">모델은 실행 도구이며 차단 권한은 정책 판정기에 둔다.</span></div>
</section>
""")


WG03_REVIEW_PR = showcase("wg-03 annotated-pull-request", """
<section class="wg-03" aria-labelledby="gate-wg03-title">
  <header class="wg-03-head"><p class="wg-03-kicker">AI REVIEW TEMPLATE</p><h2 id="gate-wg03-title" class="wg-03-title">PR #482 · 권한 검증 누락 탐지</h2><div class="wg-03-meta"><span class="wg-03-chip">src/admin/export.ts</span><span class="wg-03-chip wg-03-chip-add">+18</span><span class="wg-03-chip wg-03-chip-del">-4</span><span class="wg-03-chip">policy authz-007</span></div><nav class="wg-03-jump" aria-label="노트 점프"><span class="wg-03-jump-label">노트:</span><a href="#gate-wg03-n1" class="wg-03-jump-link wg-03-sev-critical">L42 critical</a><a href="#gate-wg03-n2" class="wg-03-jump-link wg-03-sev-warn">L48 warn</a></nav></header>
  <div class="wg-03-grid"><div class="wg-03-diff" role="table" aria-label="권한 검증 diff"><div class="wg-03-row wg-03-ctx" role="row"><span class="wg-03-ln">40</span><code class="wg-03-code">export async function exportUsers(req) {</code></div><div id="gate-wg03-l42" class="wg-03-row wg-03-add wg-03-flag" role="row"><span class="wg-03-ln">42</span><code class="wg-03-code"><span class="wg-03-sign">+</span>  const rows = await userRepo.findAll();</code><a href="#gate-wg03-n1" class="wg-03-dot wg-03-sev-critical" aria-label="L42 critical 노트">!</a></div><div id="gate-wg03-l48" class="wg-03-row wg-03-add wg-03-flag" role="row"><span class="wg-03-ln">48</span><code class="wg-03-code"><span class="wg-03-sign">+</span>  return toCsv(rows);</code><a href="#gate-wg03-n2" class="wg-03-dot wg-03-sev-warn" aria-label="L48 warn 노트">!</a></div></div><aside class="wg-03-notes" aria-label="리뷰 노트"><article id="gate-wg03-n1" class="wg-03-note wg-03-sev-critical" tabindex="-1"><header class="wg-03-note-head"><span class="wg-03-badge">critical</span><span class="wg-03-note-loc"><a href="#gate-wg03-l42">L42</a></span></header><p class="wg-03-note-body">관리자 권한 검증 없이 전체 사용자 데이터를 조회한다. <code>requireRole('admin')</code> 또는 정책 ID 근거가 필요하다.</p></article><article id="gate-wg03-n2" class="wg-03-note wg-03-sev-warn" tabindex="-1"><header class="wg-03-note-head"><span class="wg-03-badge">warn</span><span class="wg-03-note-loc"><a href="#gate-wg03-l48">L48</a></span></header><p class="wg-03-note-body">CSV export에는 감사 이벤트와 다운로드 만료 시간이 함께 남아야 한다.</p></article></aside></div>
</section>
""")


WG11_GATEWAY_KPI = showcase("wg-11 weekly-status", """
<section class="wg-11" aria-labelledby="gate-wg11-title">
  <header class="wg-11-head"><p class="wg-11-kicker">운영 대시보드 템플릿</p><h2 id="gate-wg11-title" class="wg-11-h">AI 리뷰 게이트웨이 주간 상태</h2><p class="wg-11-lead">정책 커버리지, 오탐, override, 감사 로그 완전성을 한 화면에 둔다.</p></header>
  <div class="wg-11-kpis"><div class="wg-11-kpi"><span class="wg-11-kpi-v">92%</span><span class="wg-11-kpi-l">정책 커버리지</span></div><div class="wg-11-kpi"><span class="wg-11-kpi-v wg-11-warn">7%</span><span class="wg-11-kpi-l">오탐 재분류</span></div><div class="wg-11-kpi"><span class="wg-11-kpi-v">3</span><span class="wg-11-kpi-l">override</span></div><div class="wg-11-kpi"><span class="wg-11-kpi-v">99%</span><span class="wg-11-kpi-l">감사 로그 완전성</span></div></div>
  <h3 class="wg-11-h3">규칙군별 신뢰도</h3><div class="wg-11-bars"><div class="wg-11-bar-row"><span class="wg-11-bar-label">권한/인증</span><div class="wg-11-track"><div class="wg-11-fill wg-11-fill-good" style="width:94%"></div></div><span class="wg-11-bar-pct">94%</span></div><div class="wg-11-bar-row"><span class="wg-11-bar-label">테스트 공백</span><div class="wg-11-track"><div class="wg-11-fill wg-11-fill-prog" style="width:68%"></div></div><span class="wg-11-bar-pct">68%</span></div><div class="wg-11-bar-row"><span class="wg-11-bar-label">민감정보</span><div class="wg-11-track"><div class="wg-11-fill wg-11-fill-risk" style="width:41%"></div></div><span class="wg-11-bar-pct">41%</span></div></div>
</section>
""")


WG16_GATEWAY_PLAN = showcase("wg-16 implementation-plan", """
<section class="wg-16" aria-labelledby="gate-wg16-title">
  <header class="wg-16-head"><p class="wg-16-kicker">ROLLOUT TEMPLATE</p><h2 id="gate-wg16-title" class="wg-16-h">게이트웨이 단계적 롤아웃</h2><p class="wg-16-lead">관찰 → 비차단 코멘트 → 소프트 차단 → 조직 표준화 순서로 차단 권한을 늦게 부여한다.</p></header>
  <ol class="wg-16-ms"><li class="wg-16-ms-item wg-16-done"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">M1 · 관찰 모드</span><span class="wg-16-badge wg-16-bd-done">완료</span></div><p class="wg-16-ms-desc">PR 100개 기준선을 만들고 댓글 없이 내부 finding만 수집한다.</p></div></li><li class="wg-16-ms-item wg-16-active"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">M2 · 비차단 코멘트</span><span class="wg-16-badge wg-16-bd-active">진행 중</span></div><p class="wg-16-ms-desc">리뷰어 유용성 피드백과 오탐 라벨을 받는다.</p></div></li><li class="wg-16-ms-item"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">M3 · 소프트 차단</span><span class="wg-16-badge">예정</span></div><p class="wg-16-ms-desc">고신뢰 보안 규칙부터 승인 기반 override를 요구한다.</p></div></li></ol>
  <h3 class="wg-16-h3">데이터 플로우</h3><div class="wg-16-flow"><div class="wg-16-fnode">PR<span class="wg-16-fnode-s">diff</span></div><span class="wg-16-farrow" aria-hidden="true">→</span><div class="wg-16-fnode wg-16-fnode-q">정책<span class="wg-16-fnode-s">rule_id</span></div><span class="wg-16-farrow" aria-hidden="true">→</span><div class="wg-16-fnode wg-16-fnode-hot">판정<span class="wg-16-fnode-s">gate</span></div><span class="wg-16-farrow" aria-hidden="true">→</span><div class="wg-16-fnode">감사<span class="wg-16-fnode-s">log</span></div></div>
</section>
""")


WG12_GATEWAY_FAILURE = showcase("wg-12 incident-timeline", """
<section class="wg-12" aria-labelledby="gate-wg12-title">
  <header class="wg-12-head"><p class="wg-12-kicker">FAILURE MODE TEMPLATE</p><h2 id="gate-wg12-title" class="wg-12-h">게이트 장애 대응 타임라인</h2><div class="wg-12-meta"><span class="wg-12-chip">모델 장애</span><span class="wg-12-chip wg-12-chip-sev">SEV-3</span><span class="wg-12-chip">fallback 수동 리뷰</span></div></header>
  <ol class="wg-12-tl"><li class="wg-12-tl-item"><span class="wg-12-tl-time">09:10</span><span class="wg-12-tl-dot wg-12-dot-detect"></span><div class="wg-12-tl-body"><strong>감지</strong> — 분석 실행기 timeout 증가</div></li><li class="wg-12-tl-item"><span class="wg-12-tl-time">09:14</span><span class="wg-12-tl-dot wg-12-dot-mit"></span><div class="wg-12-tl-body"><strong>완화</strong> — 고위험 레포만 수동 리뷰 강화</div></li><li class="wg-12-tl-item"><span class="wg-12-tl-time">09:31</span><span class="wg-12-tl-dot wg-12-dot-resolve"></span><div class="wg-12-tl-body"><strong>복구</strong> — 재실행 결과와 누락 PR 감사 완료</div></li></ol>
  <h3 class="wg-12-h3">후속 액션</h3><ul class="wg-12-check"><li class="wg-12-ck"><input type="checkbox" id="gate-wg12-c1" class="wg-12-ck-in" checked><label for="gate-wg12-c1" class="wg-12-ck-lb"><span class="wg-12-ck-box"></span><span class="wg-12-ck-txt">fallback 정책 문서화 <span class="wg-12-owner">@platform</span></span></label></li><li class="wg-12-ck"><input type="checkbox" id="gate-wg12-c2" class="wg-12-ck-in"><label for="gate-wg12-c2" class="wg-12-ck-lb"><span class="wg-12-ck-box"></span><span class="wg-12-ck-txt">모델 변경 골든 PR 재평가 <span class="wg-12-owner">@appsec</span></span></label></li></ul>
</section>
""")


WG02_DOC_DIRECTIONS = showcase("wg-02 visual-design-directions", """
<section class="wg-02-dir" aria-labelledby="article-wg02-title">
  <header class="wg-02-head"><p class="wg-02-kicker">DOCUMENT DIRECTIONS</p><h2 id="article-wg02-title" class="wg-02-h">운영 문서 형식 선택</h2><p class="wg-02-lead">반복 판단을 줄이는 문서는 목적에 맞는 형태를 골라야 한다.</p></header>
  <fieldset class="wg-02-grid"><legend class="wg-02-sr">운영 문서 방향 선택</legend><input type="radio" name="wg-02-pick" id="wg-02-a" class="wg-02-radio" checked><div class="wg-02-card"><div class="wg-02-preview wg-02-preview--a"><div class="wg-02-pv-bar"><span class="wg-02-pv-dot"></span><span class="wg-02-pv-line"></span></div><div class="wg-02-pv-hero">Decision</div><div class="wg-02-pv-body"><span></span><span></span><span class="wg-02-pv-short"></span></div><div class="wg-02-pv-cta wg-02-pv-cta--a">기준 확인</div></div><div class="wg-02-meta"><label for="wg-02-a" class="wg-02-pick-label">결정 기준 문서</label><p class="wg-02-desc">승인·보류·중단 기준을 짧게 고정한다.</p><span class="wg-02-badge">선택됨</span></div></div><input type="radio" name="wg-02-pick" id="wg-02-b" class="wg-02-radio"><div class="wg-02-card"><div class="wg-02-preview wg-02-preview--b"><div class="wg-02-pv-cards"><span></span><span></span><span></span></div><div class="wg-02-pv-cta wg-02-pv-cta--b">상태판</div></div><div class="wg-02-meta"><label for="wg-02-b" class="wg-02-pick-label">운영 상태판</label><p class="wg-02-desc">반복 상황과 담당자를 카드로 보여준다.</p><span class="wg-02-badge">선택됨</span></div></div><input type="radio" name="wg-02-pick" id="wg-02-c" class="wg-02-radio"><div class="wg-02-card"><div class="wg-02-preview wg-02-preview--c"><div class="wg-02-pv-split"><div class="wg-02-pv-aside"></div><div class="wg-02-pv-main"><span></span><span></span></div></div><div class="wg-02-pv-cta wg-02-pv-cta--c">온보딩</div></div><div class="wg-02-meta"><label for="wg-02-c" class="wg-02-pick-label">온보딩 문서</label><p class="wg-02-desc">새 팀원의 첫 판단을 안내한다.</p><span class="wg-02-badge">선택됨</span></div></div></fieldset>
</section>
""")


WG04_DOC_MAP = showcase("wg-04 module-map", """
<section class="wg-04" aria-labelledby="article-wg04-title">
  <header class="wg-04-head"><p class="wg-04-kicker">DOC SYSTEM MAP</p><h2 id="article-wg04-title" class="wg-04-title">작은 팀 운영 문서 맵</h2><p class="wg-04-lead">배포·장애·고객 응대 문서가 제품 결정 기록으로 연결된다.</p></header>
  <div class="wg-04-diagram"><svg viewBox="0 0 640 260" class="wg-04-svg" role="img" aria-labelledby="article-wg04-t"><title id="article-wg04-t">운영 문서 의존 맵</title><defs><marker id="article-wg04-arrow" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="var(--ink-mute)"></path></marker></defs><path class="wg-04-edge" d="M170,70 L310,130" marker-end="url(#article-wg04-arrow)"></path><path class="wg-04-edge" d="M170,190 L310,150" marker-end="url(#article-wg04-arrow)"></path><path class="wg-04-edge" d="M430,140 L520,140" marker-end="url(#article-wg04-arrow)"></path><g class="wg-04-node wg-04-node-entry"><rect x="60" y="50" width="120" height="40" rx="8"></rect><text x="120" y="75">배포 기준</text></g><g class="wg-04-node wg-04-node-core"><rect x="60" y="170" width="120" height="40" rx="8"></rect><text x="120" y="195">장애 대응</text></g><g class="wg-04-node wg-04-node-core wg-04-node-crit"><rect x="300" y="120" width="130" height="44" rx="8"></rect><text x="365" y="146">제품 결정</text></g><g class="wg-04-node wg-04-node-leaf"><rect x="500" y="120" width="120" height="44" rx="8"></rect><text x="560" y="146">온보딩</text></g></svg></div>
</section>
""")


WG06_PLAN_VARIANTS = showcase("wg-06 component-variants", """
<section class="wg-06-cs" aria-labelledby="edu-wg06-title">
  <header class="wg-06-head"><p class="wg-06-kicker">PLAN NODE CONTACT SHEET</p><h2 id="edu-wg06-title" class="wg-06-h">실행 계획 노드 변형 시트</h2><p class="wg-06-lead">Scan·Join·Sort 판단 상태를 한 장에서 비교한다.</p></header>
  <fieldset class="wg-06-density"><legend class="wg-06-density-leg">배경 토글</legend><input type="radio" name="wg-06-bg" id="wg-06-bg-light" class="wg-06-bg-input" checked><label for="wg-06-bg-light" class="wg-06-bg-label">라이트</label><input type="radio" name="wg-06-bg" id="wg-06-bg-dark" class="wg-06-bg-input"><label for="wg-06-bg-dark" class="wg-06-bg-label">다크</label></fieldset>
  <div class="tbl table-scroll wg-06-sheet"><table class="wg-06-table"><caption class="wg-06-cap">행 = 노드 유형 · 열 = 판단 상태</caption><thead><tr><th scope="col" class="wg-06-rowhead">Node \\ State</th><th scope="col">정상</th><th scope="col">주의</th><th scope="col">검증 필요</th></tr></thead><tbody><tr><th scope="row" class="wg-06-rowhead">Seq Scan</th><td><button type="button" class="wg-06-btn wg-06-btn--secondary wg-06-md">작은 테이블</button></td><td><button type="button" class="wg-06-btn wg-06-btn--danger wg-06-md wg-06-is-hover">대량 읽기</button></td><td><button type="button" class="wg-06-btn wg-06-btn--ghost wg-06-md wg-06-is-focus">선택도 확인</button></td></tr><tr><th scope="row" class="wg-06-rowhead">Nested Loop</th><td><button type="button" class="wg-06-btn wg-06-btn--secondary wg-06-md">row 적음</button></td><td><button type="button" class="wg-06-btn wg-06-btn--danger wg-06-md wg-06-is-hover">반복 큼</button></td><td><button type="button" class="wg-06-btn wg-06-btn--ghost wg-06-md wg-06-is-focus">loops 확인</button></td></tr><tr><th scope="row" class="wg-06-rowhead">Sort</th><td><button type="button" class="wg-06-btn wg-06-btn--secondary wg-06-md">이미 축소</button></td><td><button type="button" class="wg-06-btn wg-06-btn--danger wg-06-md wg-06-is-hover">대량 정렬</button></td><td><button type="button" class="wg-06-btn wg-06-btn--ghost wg-06-md wg-06-is-focus">인덱스 정렬</button></td></tr></tbody></table></div>
</section>
""")


WG20_EXPLAIN_PROMPT = showcase("wg-20 prompt-tuner", """
<section class="wg-20-tuner" aria-label="EXPLAIN 분석 프롬프트 튜너">
  <header class="wg-20-head"><h2 class="wg-20-title">EXPLAIN 분석 프롬프트 튜너</h2><p class="wg-20-hint">샘플을 선택하면 입력과 기대 분석 결과가 CSS-only로 전환된다.</p></header>
  <fieldset class="wg-20-samples"><legend class="wg-20-legend">샘플 플랜</legend><input class="wg-20-radio" type="radio" name="wg-20-sample" id="wg-20-s1" checked><label class="wg-20-chip" for="wg-20-s1">Seq Scan</label><input class="wg-20-radio" type="radio" name="wg-20-sample" id="wg-20-s2"><label class="wg-20-chip" for="wg-20-s2">Nested Loop</label><input class="wg-20-radio" type="radio" name="wg-20-sample" id="wg-20-s3"><label class="wg-20-chip" for="wg-20-s3">Sort + Limit</label></fieldset>
  <div class="wg-20-grid"><div class="wg-20-pane"><div class="wg-20-pane-head">템플릿</div><pre class="wg-20-tpl">플랜에서 병목 가설을 2개 세우고, evidence line과 다음 실험을 제안하라.
입력: <span class="wg-20-var">[[plan]]</span></pre></div><div class="wg-20-pane"><div class="wg-20-pane-head">샘플 입력</div><div class="wg-20-input wg-20-input--s1"><span class="wg-20-k">plan</span>Seq Scan on orders rows=900000</div><div class="wg-20-input wg-20-input--s2"><span class="wg-20-k">plan</span>Nested Loop actual rows=1 loops=2547647</div><div class="wg-20-input wg-20-input--s3"><span class="wg-20-k">plan</span>Sort before Limit 10</div></div><div class="wg-20-pane"><div class="wg-20-pane-head">렌더 결과</div><div class="wg-20-out wg-20-out--s1">선택도가 낮거나 인덱스가 도움 되지 않는 상황일 수 있다. 조건 컬럼 분포와 실제 필요한 row를 확인한다.</div><div class="wg-20-out wg-20-out--s2">반복 횟수가 핵심 병목이다. 바깥쪽 row estimate와 안쪽 접근 경로를 먼저 검증한다.</div><div class="wg-20-out wg-20-out--s3">LIMIT 전에 많은 row를 정렬할 수 있다. 정렬 가능한 인덱스와 필터 축소를 검토한다.</div></div></div>
</section>
""")


WG17_BLOG_WRITEUP = showcase("wg-17 pr-writeup", """
<section class="wg-17" aria-labelledby="blog-wg17-title">
  <header class="wg-17-head"><p class="wg-17-kicker">CHANGE WRITEUP TEMPLATE</p><h2 id="blog-wg17-title" class="wg-17-title">refactor: 두 번째 뇌를 작게 만들기</h2><div class="wg-17-meta"><span class="wg-17-chip wg-17-chip-branch">big-system → small-system</span><span class="wg-17-chip wg-17-chip-add">+회수율</span><span class="wg-17-chip wg-17-chip-del">-관리비</span></div></header>
  <div class="wg-17-block"><h3 class="wg-17-h3"><span class="wg-17-h3-no">1</span> Before / After</h3><div class="wg-17-ba"><div class="wg-17-ba-col wg-17-ba-before"><p class="wg-17-ba-tag">Before</p><ul class="wg-17-ba-list"><li>태그와 폴더가 많음</li><li>링크만 저장</li><li>회고가 불규칙</li></ul></div><div class="wg-17-ba-arrow" aria-hidden="true">→</div><div class="wg-17-ba-col wg-17-ba-after"><p class="wg-17-ba-tag">After</p><ul class="wg-17-ba-list"><li>질문형 제목</li><li>저장 이유 한 문장</li><li>금요일 30분 회고</li></ul></div></div></div>
  <div class="wg-17-block"><h3 class="wg-17-h3"><span class="wg-17-h3-no">2</span> 파일별 워크스루처럼 읽는 습관</h3><details class="wg-17-file" open><summary class="wg-17-summary"><span class="wg-17-file-name">notes/inbox.md</span><span class="wg-17-file-stat"><span class="wg-17-add">정리</span></span><span class="wg-17-caret" aria-hidden="true"></span></summary><div class="wg-17-file-body"><p class="wg-17-p">임시함은 바로 쓸 것, 보류할 것, 지울 것 세 종류만 남긴다.</p></div></details><details class="wg-17-file"><summary class="wg-17-summary"><span class="wg-17-file-name">weekly/review.md</span><span class="wg-17-file-stat"><span class="wg-17-add">회수</span></span><span class="wg-17-caret" aria-hidden="true"></span></summary><div class="wg-17-file-body"><p class="wg-17-p">다시 쓸 노트 3개와 다음 행동 1개만 남긴다.</p></div></details></div>
</section>
""")


VT_BLOG_WEEKLY = showcase("vt-11 weekly-status", """
<section class="vt-shell"><div class="vt-frame"><div class="wk-bars"><div class="wk-row"><strong>삭제</strong><div class="wk-bar"><div class="wk-fill" style="width:88%"></div></div><span>88%</span></div><div class="wk-row"><strong>질문형 제목</strong><div class="wk-bar"><div class="wk-fill" style="width:74%"></div></div><span>74%</span></div><div class="wk-row"><strong>회고 루틴</strong><div class="wk-bar"><div class="wk-fill" style="width:100%"></div></div><span>100%</span></div></div><div class="wk-cols"><div class="wk-col"><b>완료</b><p class="vt-text">열지 않는 노트와 중복 태그를 줄였다.</p></div><div class="wk-col"><b>진행</b><p class="vt-text">링크 저장 이유를 한 문장으로 붙인다.</p></div><div class="wk-col"><b>리스크</b><p class="vt-text">바쁜 주에는 회고 시간이 쉽게 밀린다.</p></div></div></div></section>
""")


VT_BLOG_COMPARE = showcase("vt-13 comparison-cards", """
<section class="vt-shell"><div class="vt-frame"><div class="cmp"><article class="cmp-card"><h3>Before</h3><ul><li>저장량 중심</li><li>태그 과다</li><li>임시함 부채</li></ul></article><article class="cmp-card pick"><h3>After</h3><ul><li>회수율 중심</li><li>질문형 제목</li><li>주간 복구 루틴</li></ul></article><article class="cmp-card"><h3>Next</h3><ul><li>월말 삭제</li><li>회수 안 된 노트 점검</li><li>규칙 하나 더 제거</li></ul></article></div></div></section>
""")


INSERTS = {
    "01-local-rag-personal-knowledge-vault.html": [(3, WG10_RAG_SHEET), (5, WG13_RAG_FLOW), (9, WG15_RAG_CONCEPT)],
    "02-ai-code-review-gateway-operating-model.html": [(2, WG04_GATEWAY_MAP), (7, WG03_REVIEW_PR), (8, WG11_GATEWAY_KPI), (9, WG16_GATEWAY_PLAN), (10, WG12_GATEWAY_FAILURE)],
    "03-small-team-operating-docs-product-speed.html": [(6, WG02_DOC_DIRECTIONS), (8, WG04_DOC_MAP), (10, WG17_BLOG_WRITEUP)],
    "04-postgres-query-plan-3week-course.html": [(5, WG06_PLAN_VARIANTS), (9, WG13_RAG_FLOW), (10, WG20_EXPLAIN_PROMPT)],
    "05-small-second-brain-30days-retro.html": [(5, VT_BLOG_WEEKLY), (9, VT_BLOG_COMPARE), (10, WG17_BLOG_WRITEUP)],
}


def main() -> None:
    for filename, inserts in INSERTS.items():
        path = PAGES / filename
        text = strip_existing(path.read_text(encoding="utf-8"))
        for section_no, snippet in inserts:
            text = insert_into_numbered_section(text, section_no, snippet)
        path.write_text(text, encoding="utf-8")
        labels = ", ".join(f"{no}" for no, _ in inserts)
        print(f"updated {filename}: sections {labels}")


if __name__ == "__main__":
    main()
