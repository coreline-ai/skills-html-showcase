#!/usr/bin/env python3
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "pages"


def replace_main(filename: str, main_html: str) -> None:
    path = PAGES / filename
    text = path.read_text(encoding="utf-8")
    updated, count = re.subn(r'<main id="main"[\s\S]*?</main>', main_html.strip(), text, count=1)
    if count != 1:
        raise RuntimeError(f"main replacement failed for {filename}: {count}")
    path.write_text(updated, encoding="utf-8")


def mark(name: str, body: str) -> str:
    return f'<!-- template-showcase:start {name} --><div class="summary-card template-showcase"><div class="label">TEMPLATE CHECK · {name}</div>{body.strip()}</div><!-- template-showcase:end {name} -->'


CASE_VT12 = mark("vt-12 incident-summary", """
<div class="vt-shell"><div class="vt-frame"><div><div class="inc-head"><div class="inc-card impact"><b>영향</b><p class="vt-text">예약 리마인더 3,260건 지연, 최대 지연 42분, CS 문의 +63건.</p></div><div class="inc-card cause"><b>원인</b><p class="vt-text">리마인더 job과 캠페인 job이 같은 큐를 공유했고 우선순위가 없었다.</p></div><div class="inc-card action"><b>조치</b><p class="vt-text">캠페인을 중지하고 worker를 증설한 뒤 리마인더 전용 큐로 분리했다.</p></div></div><ol class="tl" style="margin-top:12px"><li class="tl-item"><b>17:58 캠페인 시작</b><p class="vt-text">대상 48만명 캠페인 발송 job이 한 번에 들어왔다.</p></li><li class="tl-item"><b>18:05 감지</b><p class="vt-text">상담 채널에서 "예약 알림이 오지 않는다" 문의가 증가했다.</p></li><li class="tl-item"><b>18:12 확인</b><p class="vt-text">queue depth 18,400과 job age p99 상승을 확인했다.</p></li><li class="tl-item"><b>18:25 완화</b><p class="vt-text">캠페인 job을 중지하고 리마인더 worker를 임시 증설했다.</p></li><li class="tl-item"><b>18:47 복구</b><p class="vt-text">대기 중인 리마인더가 모두 처리되고 신규 job age가 정상화됐다.</p></li></ol></div></div></div>
""")


CASE_VT04 = mark("vt-04 timeline", """
<div class="vt-shell"><div class="vt-frame"><ol class="tl"><li class="tl-item"><b>17:55 선행 신호</b><p class="vt-text">캠페인 발송 job이 평소보다 4배 많이 생성됐지만 알림은 없었다.</p></li><li class="tl-item"><b>18:05 사용자 감지</b><p class="vt-text">CS 문의가 먼저 들어오며 내부 감지보다 고객 신호가 앞섰다.</p></li><li class="tl-item"><b>18:18 원인 좁힘</b><p class="vt-text">리마인더와 캠페인이 같은 worker pool을 쓰는 것을 확인했다.</p></li><li class="tl-item"><b>18:47 복구</b><p class="vt-text">큐가 비워지고 예약 알림 지연이 2분 이하로 돌아왔다.</p></li><li class="tl-item"><b>D+1 회고</b><p class="vt-text">SLO가 다른 작업은 큐와 알림도 분리해야 한다는 결론을 남겼다.</p></li></ol></div></div>
""")


CASE_VT14 = mark("vt-14 process-swimlane", """
<div class="vt-shell"><div class="vt-frame"><div class="swim"><div class="lane"><div class="lane-label">CS</div><div class="lane-step">문의 급증</div><div class="lane-step">영향 수집</div><div class="lane-step blank">-</div><div class="lane-step">고객 공지</div></div><div class="lane"><div class="lane-label">On-call</div><div class="lane-step">알림 확인</div><div class="lane-step">큐 진단</div><div class="lane-step">worker 증설</div><div class="lane-step">복구 선언</div></div><div class="lane"><div class="lane-label">Growth</div><div class="lane-step">캠페인 시작</div><div class="lane-step blank">-</div><div class="lane-step">캠페인 pause</div><div class="lane-step">rate limit 합의</div></div><div class="lane"><div class="lane-label">Platform</div><div class="lane-step blank">-</div><div class="lane-step">queue metric 확인</div><div class="lane-step">전용 큐 설계</div><div class="lane-step">게임데이 예약</div></div></div></div></div>
""")


CASE_WG12 = mark("wg-12 incident-timeline", """
<section class="wg-12" aria-labelledby="case-wg12-title">
  <header class="wg-12-head"><p class="wg-12-kicker">POSTMORTEM · SEV-2</p><h2 id="case-wg12-title" class="wg-12-h">INC-RR-20260605 예약 알림 지연</h2><div class="wg-12-meta"><span class="wg-12-chip">발생 2026-06-05 18:05 KST</span><span class="wg-12-chip">지속 42분</span><span class="wg-12-chip">p95 지연 31분</span><span class="wg-12-chip wg-12-chip-sev">SEV-2</span><span class="wg-12-chip">담당 Platform/Ops</span></div></header>
  <h3 class="wg-12-h3">타임라인</h3>
  <ol class="wg-12-tl"><li class="wg-12-tl-item"><span class="wg-12-tl-time">18:05</span><span class="wg-12-tl-dot wg-12-dot-detect"></span><div class="wg-12-tl-body"><strong>감지</strong> - CS 문의와 job age 상승을 확인했다.</div></li><li class="wg-12-tl-item"><span class="wg-12-tl-time">18:12</span><span class="wg-12-tl-dot"></span><div class="wg-12-tl-body"><strong>진단</strong> - queue depth 18,400, 캠페인 job이 리마인더 큐를 점유했다.</div></li><li class="wg-12-tl-item"><span class="wg-12-tl-time">18:18</span><span class="wg-12-tl-dot"></span><div class="wg-12-tl-body"><strong>IC 지정</strong> - On-call이 incident commander를 지정하고 대응 채널을 열었다.</div></li><li class="wg-12-tl-item"><span class="wg-12-tl-time">18:25</span><span class="wg-12-tl-dot wg-12-dot-mit"></span><div class="wg-12-tl-body"><strong>완화</strong> - 캠페인 pause와 worker +6 증설을 적용했다.</div></li><li class="wg-12-tl-item"><span class="wg-12-tl-time">18:47</span><span class="wg-12-tl-dot wg-12-dot-resolve"></span><div class="wg-12-tl-body"><strong>복구</strong> - backlog drain 완료, 신규 리마인더 지연이 2분 이하로 돌아왔다.</div></li></ol>
  <h3 class="wg-12-h3">영향 · 원인 · 조치</h3>
  <div class="tbl table-scroll"><table class="wg-12-table"><caption>예약 알림 지연 사고 영향 원인 조치</caption><thead><tr><th scope="col">구분</th><th scope="col">내용</th></tr></thead><tbody><tr><th scope="row"><span class="wg-12-rk wg-12-rk-impact">영향</span></th><td>리마인더 3,260건 지연, 최대 지연 42분, p95 지연 31분, CS 문의 +63건, 고객 취소 0건.</td></tr><tr><th scope="row"><span class="wg-12-rk wg-12-rk-cause">원인</span></th><td>SLO가 다른 캠페인 job과 예약 리마인더 job이 같은 FIFO 큐와 worker pool을 공유했다.</td></tr><tr><th scope="row"><span class="wg-12-rk wg-12-rk-action">조치</span></th><td>전용 큐, job age 알림, 캠페인 rate limit, pause switch를 후속 액션으로 확정했다.</td></tr></tbody></table></div>
  <h3 class="wg-12-h3">후속 액션</h3>
  <ul class="wg-12-check"><li class="wg-12-ck"><input type="checkbox" id="case-wg12-c1" class="wg-12-ck-in" checked><label for="case-wg12-c1" class="wg-12-ck-lb"><span class="wg-12-ck-box"></span><span class="wg-12-ck-txt">리마인더 전용 큐 생성 <span class="wg-12-owner">@platform</span></span></label></li><li class="wg-12-ck"><input type="checkbox" id="case-wg12-c2" class="wg-12-ck-in" checked><label for="case-wg12-c2" class="wg-12-ck-lb"><span class="wg-12-ck-box"></span><span class="wg-12-ck-txt">job age p95/p99 알림 추가 <span class="wg-12-owner">@sre</span></span></label></li><li class="wg-12-ck"><input type="checkbox" id="case-wg12-c3" class="wg-12-ck-in"><label for="case-wg12-c3" class="wg-12-ck-lb"><span class="wg-12-ck-box"></span><span class="wg-12-ck-txt">캠페인 rate limit 적용 <span class="wg-12-owner">@growth</span></span></label></li><li class="wg-12-ck"><input type="checkbox" id="case-wg12-c4" class="wg-12-ck-in"><label for="case-wg12-c4" class="wg-12-ck-lb"><span class="wg-12-ck-box"></span><span class="wg-12-ck-txt">분기별 큐 포화 게임데이 <span class="wg-12-owner">@team</span></span></label></li></ul>
</section>
""")


LANDING_VT01 = mark("vt-01 hero-map", """
<div class="vt-shell"><div class="vt-frame"><div class="vt-demo"><div class="hm-grid"><article class="hm-card"><div class="vt-kicker">Problem</div><h3>결정이 채팅과 회의록에 흩어진다</h3><p class="vt-text">다음 달에 왜 그렇게 정했는지 다시 물어보게 된다.</p></article><article class="hm-card" style="--c:var(--vt-blue)"><div class="vt-kicker">Map</div><h3>회의록·결정·근거 연결</h3><p class="vt-text">프로젝트, 사람, 이슈, 고객 피드백을 같은 맥락으로 묶는다.</p></article><article class="hm-card" style="--c:var(--vt-green)"><div class="vt-kicker">Action</div><h3>다음 회의 전 미완료 작업 확인</h3><p class="vt-text">담당자와 마감일이 흐려지기 전에 다시 띄운다.</p></article></div><div class="hm-result"><b>LocalNote: 작은 팀의 결정 기억장치</b><span>저장소가 아니라 같은 결정을 반복하지 않게 만드는 작업 공간이다.</span></div></div></div></div>
""")


LANDING_VT07 = mark("vt-07 card-grid", """
<div class="vt-shell"><div class="vt-frame"><div class="cg-grid"><article class="cg-card"><em>01</em><b>회의록 수집</b><p>녹취, 요약, 첨부 링크를 프로젝트에 묶는다.</p></article><article class="cg-card"><em>02</em><b>결정 추출</b><p>결정, 보류, 리스크를 분리한다.</p></article><article class="cg-card"><em>03</em><b>근거 연결</b><p>고객 피드백, 이슈, 문서를 근거로 붙인다.</p></article><article class="cg-card"><em>04</em><b>액션 추적</b><p>담당자, 마감일, 다음 확인일을 보존한다.</p></article><article class="cg-card"><em>05</em><b>검색</b><p>사람, 프로젝트, 결정 키워드로 다시 찾는다.</p></article><article class="cg-card"><em>06</em><b>리뷰</b><p>다음 회의 전 바뀐 조건을 확인한다.</p></article></div></div></div>
""")


LANDING_VT19 = mark("vt-19 feature-flag", """
<div class="vt-shell"><div class="vt-frame"><div class="flag-list"><div class="flag"><div><b>decision_extraction</b><p class="vt-text">회의록에서 결정과 보류 항목을 자동 제안한다.</p></div><div class="flag-ctl"><span class="flag-state on">ON</span><span class="switch on" aria-hidden="true"></span></div></div><div class="flag"><div><b>external_ai_sync</b><p class="vt-text">외부 AI 처리 경로는 기업 고객 기본값에서 꺼둔다.</p></div><div class="flag-ctl"><span class="flag-state off">OFF</span><span class="switch off" aria-hidden="true"></span></div></div><div class="flag"><div><b>weekly_digest</b><p class="vt-text">미완료 액션과 오래된 결정을 월요일 아침 요약한다.</p></div><div class="flag-ctl"><span class="flag-state warn">BETA</span><span class="switch warn" aria-hidden="true"></span></div></div></div></div></div>
""")


LANDING_WG02 = mark("wg-02 visual-design-directions", """
<section class="wg-02-dir" aria-labelledby="landing-wg02-title">
  <header class="wg-02-head"><p class="wg-02-kicker">POSITIONING</p><h2 id="landing-wg02-title" class="wg-02-h">LocalNote 포지셔닝 방향</h2><p class="wg-02-lead">검색 도구, 위키, 결정 기억장치 중 랜딩의 첫 문장에 맞는 방향을 고른다.</p></header>
  <fieldset class="wg-02-grid"><legend class="wg-02-sr">포지셔닝 방향 선택</legend><input type="radio" name="landing-wg02-pick" id="landing-wg02-a" class="wg-02-radio" checked><div class="wg-02-card"><div class="wg-02-preview wg-02-preview--a"><div class="wg-02-pv-hero">Decision Memory</div><div class="wg-02-pv-body"><span></span><span></span><span class="wg-02-pv-short"></span></div><div class="wg-02-pv-cta wg-02-pv-cta--a">기본 방향</div></div><div class="wg-02-meta"><label for="landing-wg02-a" class="wg-02-pick-label">결정 기억장치</label><p class="wg-02-desc">결정, 근거, 담당자, 다음 행동을 중심으로 차별화한다.</p><span class="wg-02-badge">선택됨</span></div></div><input type="radio" name="landing-wg02-pick" id="landing-wg02-b" class="wg-02-radio"><div class="wg-02-card"><div class="wg-02-preview wg-02-preview--b"><div class="wg-02-pv-cards"><span></span><span></span><span></span></div><div class="wg-02-pv-cta wg-02-pv-cta--b">Search</div></div><div class="wg-02-meta"><label for="landing-wg02-b" class="wg-02-pick-label">지식 검색</label><p class="wg-02-desc">검색 UX는 익숙하지만 경쟁 제품과 구분이 약하다.</p><span class="wg-02-badge">선택됨</span></div></div><input type="radio" name="landing-wg02-pick" id="landing-wg02-c" class="wg-02-radio"><div class="wg-02-card"><div class="wg-02-preview wg-02-preview--c"><div class="wg-02-pv-split"><div class="wg-02-pv-aside"></div><div class="wg-02-pv-main"><span></span><span></span></div></div><div class="wg-02-pv-cta wg-02-pv-cta--c">Wiki</div></div><div class="wg-02-meta"><label for="landing-wg02-c" class="wg-02-pick-label">팀 위키</label><p class="wg-02-desc">작성 부담이 먼저 떠오르므로 초기 랜딩 메시지에는 덜 적합하다.</p><span class="wg-02-badge">선택됨</span></div></div></fieldset>
</section>
""")


LANDING_WG05 = mark("wg-05 living-design-system", """
<section class="wg-05-dls" aria-labelledby="landing-wg05-title">
  <header class="wg-05-head"><p class="wg-05-kicker">PRODUCT SYSTEM</p><h2 id="landing-wg05-title" class="wg-05-h">LocalNote 메시지 토큰</h2><p class="wg-05-lead">랜딩에서 반복되는 제품 언어를 문제, 가치, 증거, CTA 토큰으로 고정한다.</p></header>
  <details class="wg-05-group" open><summary class="wg-05-summary"><span class="wg-05-sum-label">핵심 메시지</span><span class="wg-05-sum-count">4 토큰</span></summary><ul class="wg-05-grid" role="list"><li class="wg-05-swatch"><span class="wg-05-chip" style="background:var(--accent)" aria-hidden="true"></span><span class="wg-05-name">problem</span><code class="wg-05-val">결정이 사라짐</code><span class="wg-05-role">첫 화면 문제</span></li><li class="wg-05-swatch"><span class="wg-05-chip" style="background:var(--good-bg);border:1px solid var(--good-border)" aria-hidden="true"></span><span class="wg-05-name">promise</span><code class="wg-05-val">다시 찾는 결정</code><span class="wg-05-role">가치 제안</span></li><li class="wg-05-swatch"><span class="wg-05-chip" style="background:var(--term-bg);border:1px solid var(--term-border)" aria-hidden="true"></span><span class="wg-05-name">proof</span><code class="wg-05-val">회의 전 3분 리뷰</code><span class="wg-05-role">증거 문장</span></li><li class="wg-05-swatch"><span class="wg-05-chip wg-05-chip--dark" style="background:var(--ink)" aria-hidden="true"></span><span class="wg-05-name">cta</span><code class="wg-05-val">첫 프로젝트 만들기</code><span class="wg-05-role">주 행동</span></li></ul></details>
  <details class="wg-05-group" open><summary class="wg-05-summary"><span class="wg-05-sum-label">보안 언어</span><span class="wg-05-sum-count">3 토큰</span></summary><ul class="wg-05-type-list" role="list"><li class="wg-05-type-row"><span class="wg-05-type-sample" style="font-size:var(--fs-md)">팀 데이터는 워크스페이스 안에 보존</span><span class="wg-05-name">privacy</span><code class="wg-05-val">default</code></li><li class="wg-05-type-row"><span class="wg-05-type-sample" style="font-size:var(--fs-md)">민감 회의는 AI 제안 제외 가능</span><span class="wg-05-name">control</span><code class="wg-05-val">admin</code></li><li class="wg-05-type-row"><span class="wg-05-type-sample" style="font-size:var(--fs-md)">삭제 요청과 보관 기간을 문서화</span><span class="wg-05-name">retention</span><code class="wg-05-val">policy</code></li></ul></details>
</section>
""")


LANDING_WG08 = mark("wg-08 clickable-flow", """
<section class="wg-08-proto" aria-label="LocalNote 온보딩 화면 프로토타입">
  <div class="wg-08-bar"><span class="wg-08-title">첫 프로젝트 온보딩</span><ol class="wg-08-steps" aria-label="진행 단계"><li><a href="#wg-08-cart">1 업로드</a></li><li><a href="#wg-08-pay">2 결정 확인</a></li><li><a href="#wg-08-done">3 공유</a></li></ol></div>
  <div class="wg-08-device"><div class="wg-08-viewport"><article id="wg-08-cart" class="wg-08-screen wg-08-screen--default" tabindex="-1" aria-label="화면 A: 회의록 업로드"><header class="wg-08-shead"><span class="wg-08-badge">화면 A</span><h3>회의록 업로드</h3></header><ul class="wg-08-list"><li><span>제품 주간 회의</span><span class="wg-08-price">36분</span></li><li><span>고객 인터뷰 요약</span><span class="wg-08-price">12개 질문</span></li></ul><div class="wg-08-total"><span>추출 후보</span><strong>9개</strong></div><a class="wg-08-cta" href="#wg-08-pay">결정 확인 &rarr;</a></article><article id="wg-08-pay" class="wg-08-screen" tabindex="-1" aria-label="화면 B: 결정 확인"><header class="wg-08-shead"><span class="wg-08-badge">화면 B</span><h3>결정 확인</h3></header><fieldset class="wg-08-pick"><legend class="wg-08-legend">분류 선택</legend><label><span class="wg-08-dot" aria-hidden="true"></span>결정: 6월 베타 유지</label><label><span class="wg-08-dot" aria-hidden="true"></span>보류: 가격 정책</label><label><span class="wg-08-dot" aria-hidden="true"></span>액션: 고객 5팀 인터뷰</label></fieldset><div class="wg-08-nav"><a class="wg-08-back" href="#wg-08-cart">&larr; 뒤로</a><a class="wg-08-cta" href="#wg-08-done">팀에 공유 &rarr;</a></div></article><article id="wg-08-done" class="wg-08-screen" tabindex="-1" aria-label="화면 C: 공유 완료"><header class="wg-08-shead"><span class="wg-08-badge wg-08-badge--ok">화면 C</span><h3>공유 완료</h3></header><div class="wg-08-ok"><span class="wg-08-check" aria-hidden="true">&#10003;</span><p>프로젝트 결정 로그가 생성되었습니다.<br><span class="wg-08-order">Project LocalNote / Week 23</span></p></div><a class="wg-08-back" href="#wg-08-cart">처음으로 돌아가기</a></article></div></div>
  <p class="wg-08-hint">상단 단계 또는 화면 내 링크로 전환됩니다. JS 없이 :target으로만 동작합니다.</p>
</section>
""")


LANDING_WG09 = mark("wg-09 arrow-key-slide-deck", """
<section class="wg-09-deck" aria-label="LocalNote 공유용 4장 피치 덱">
  <header class="wg-09-bar"><span class="wg-09-name">LocalNote in 5 minutes</span><nav class="wg-09-dots" aria-label="슬라이드 바로가기"><a href="#wg-09-s1">1</a><a href="#wg-09-s2">2</a><a href="#wg-09-s3">3</a><a href="#wg-09-s4">4</a></nav></header>
  <div class="wg-09-track" tabindex="0" aria-label="좌우 스크롤로 슬라이드 이동"><article id="wg-09-s1" class="wg-09-slide wg-09-slide--title" aria-label="슬라이드 1"><span class="wg-09-no">01 / 04</span><h2 class="wg-09-title">LocalNote</h2><p class="wg-09-lead">팀의 결정 기억장치</p><div class="wg-09-cta-row"><a class="wg-09-next" href="#wg-09-s2">다음 &rarr;</a></div></article><article id="wg-09-s2" class="wg-09-slide" aria-label="슬라이드 2"><span class="wg-09-no">02 / 04</span><h2 class="wg-09-title">문제</h2><ul class="wg-09-points"><li>같은 질문이 반복된다.</li><li>결정 근거가 흩어진다.</li><li>후속 작업 담당자가 흐려진다.</li></ul><div class="wg-09-cta-row"><a class="wg-09-prev" href="#wg-09-s1">&larr; 이전</a><a class="wg-09-next" href="#wg-09-s3">다음 &rarr;</a></div></article><article id="wg-09-s3" class="wg-09-slide" aria-label="슬라이드 3"><span class="wg-09-no">03 / 04</span><h2 class="wg-09-title">해결</h2><div class="wg-09-stats"><div class="wg-09-stat"><strong>12</strong><span>결정</span></div><div class="wg-09-stat"><strong>7</strong><span>액션</span></div><div class="wg-09-stat"><strong>3분</strong><span>회의 전 리뷰</span></div></div><div class="wg-09-cta-row"><a class="wg-09-prev" href="#wg-09-s2">&larr; 이전</a><a class="wg-09-next" href="#wg-09-s4">다음 &rarr;</a></div></article><article id="wg-09-s4" class="wg-09-slide wg-09-slide--end" aria-label="슬라이드 4"><span class="wg-09-no">04 / 04</span><h2 class="wg-09-title">다음 행동</h2><p class="wg-09-lead">첫 프로젝트 만들기, 회의록 3개 업로드, 결정 타임라인 확인.</p><div class="wg-09-cta-row"><a class="wg-09-prev" href="#wg-09-s3">&larr; 이전</a><a class="wg-09-next" href="#wg-09-s1">처음으로</a></div></article></div>
  <p class="wg-09-hint">점 링크 또는 슬라이드 내 이전/다음 링크로 이동한다. 화살표키 이동은 JS 필요.</p>
</section>
""")


LANDING_WG16 = mark("wg-16 implementation-plan", """
<section class="wg-16" aria-labelledby="landing-wg16-title">
  <header class="wg-16-head"><p class="wg-16-kicker">LAUNCH PLAN</p><h2 id="landing-wg16-title" class="wg-16-h">LocalNote 30일 출시 계획</h2><p class="wg-16-lead">랜딩 브리프가 실제 제품 출시로 이어지도록 메시지, 온보딩, 보안, 전환 실험을 순서화한다.</p></header>
  <h3 class="wg-16-h3">마일스톤</h3><ol class="wg-16-ms"><li class="wg-16-ms-item wg-16-done"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">M1 · 메시지 고정</span><span class="wg-16-badge wg-16-bd-done">완료</span></div><p class="wg-16-ms-desc">문제, 가치, CTA, 보안 문장을 한 장으로 고정한다.</p></div></li><li class="wg-16-ms-item wg-16-active"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">M2 · 온보딩 플로우</span><span class="wg-16-badge wg-16-bd-active">진행 중</span></div><p class="wg-16-ms-desc">회의록 업로드에서 결정 로그 생성까지 3단계로 줄인다.</p></div></li><li class="wg-16-ms-item"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">M3 · 보안 FAQ</span><span class="wg-16-badge">예정</span></div><p class="wg-16-ms-desc">민감 회의 제외, 보관 기간, 삭제 요청을 FAQ로 제공한다.</p></div></li><li class="wg-16-ms-item"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">M4 · 전환 실험</span><span class="wg-16-badge">예정</span></div><p class="wg-16-ms-desc">첫 프로젝트 생성과 데모 예약 CTA를 비교한다.</p></div></li></ol>
  <h3 class="wg-16-h3">리스크 평가</h3><div class="tbl table-scroll"><table class="wg-16-table"><caption>LocalNote 출시 리스크</caption><thead><tr><th scope="col">리스크</th><th scope="col">가능성</th><th scope="col">영향</th><th scope="col">완화책</th></tr></thead><tbody><tr><th scope="row">AI 제안 신뢰 부족</th><td><span class="wg-16-lv wg-16-lv-mid">중</span></td><td><span class="wg-16-lv wg-16-lv-hi">높음</span></td><td>모든 결정 제안에 원문 근거와 수동 확인 단계를 둔다.</td></tr><tr><th scope="row">보안 우려</th><td><span class="wg-16-lv wg-16-lv-mid">중</span></td><td><span class="wg-16-lv wg-16-lv-hi">높음</span></td><td>민감 회의 제외와 데이터 보관 정책을 첫 화면 하단에 둔다.</td></tr><tr><th scope="row">빈 워크스페이스 이탈</th><td><span class="wg-16-lv wg-16-lv-lo">낮음</span></td><td><span class="wg-16-lv wg-16-lv-mid">중</span></td><td>샘플 프로젝트와 3분 온보딩을 제공한다.</td></tr></tbody></table></div>
</section>
""")


CHECK_VT05 = mark("vt-05 checklist-flow", """
<div class="vt-shell"><div class="vt-frame"><div class="cf"><div class="cf-item"><span class="cf-check">✓</span><div><b>데이터 권한 확인</b><p class="vt-text">학습/추론 입력에 개인정보, 고객 비밀, 삭제 요청 데이터가 섞이지 않았는지 확인한다.</p></div><span class="cf-state">PASS</span></div><div class="cf-item"><span class="cf-check">✓</span><div><b>평가 세트 고정</b><p class="vt-text">대표 질문, 실패 질문, 악성 입력을 출시 전 기준선으로 묶는다.</p></div><span class="cf-state">PASS</span></div><div class="cf-item"><span class="cf-check">✓</span><div><b>운영 알림 연결</b><p class="vt-text">오류율, 신고율, fallback 비율, 지연을 대시보드로 본다.</p></div><span class="cf-state">WARN</span></div><div class="cf-item"><span class="cf-check">✓</span><div><b>중단 경로 확보</b><p class="vt-text">feature flag, fallback UX, 공지 문구가 준비되지 않으면 출시하지 않는다.</p></div><span class="cf-state">BLOCK</span></div></div></div></div>
""")


CHECK_VT06 = mark("vt-06 quality-gate", """
<div class="vt-shell"><div class="vt-frame"><div><div class="qg-grid"><div class="qg-card"><b>데이터</b><p class="vt-text">권한과 보관 정책이 문서화되어야 한다.</p></div><div class="qg-card warn"><b>품질</b><p class="vt-text">대표 평가만 있고 실패 fixture가 부족하면 경고다.</p></div><div class="qg-card block"><b>보안</b><p class="vt-text">권한 없는 문서 노출 가능성이 있으면 출시 차단이다.</p></div><div class="qg-card warn"><b>운영</b><p class="vt-text">fallback과 온콜이 없으면 점진 출시만 허용한다.</p></div></div><div class="qg-final">PRE-FLIGHT: P0 실패 모드가 하나라도 남으면 출시하지 않는다.</div></div></div></div>
""")


CHECK_VT14 = mark("vt-14 process-swimlane", """
<div class="vt-shell"><div class="vt-frame"><div class="swim"><div class="lane"><div class="lane-label">PM</div><div class="lane-step">위험 정의</div><div class="lane-step">출시 범위</div><div class="lane-step">공지 승인</div><div class="lane-step">회고 예약</div></div><div class="lane"><div class="lane-label">ML</div><div class="lane-step">평가 세트</div><div class="lane-step">실패 분석</div><div class="lane-step">모델 카드</div><div class="lane-step blank">-</div></div><div class="lane"><div class="lane-label">Security</div><div class="lane-step">데이터 권한</div><div class="lane-step">프롬프트 공격</div><div class="lane-step">로그 마스킹</div><div class="lane-step">감사 기록</div></div><div class="lane"><div class="lane-label">Ops</div><div class="lane-step">flag 준비</div><div class="lane-step">알림 연결</div><div class="lane-step">rollback drill</div><div class="lane-step">7일 모니터</div></div></div></div></div>
""")


CHECK_VT16 = mark("vt-16 implementation-plan", """
<div class="vt-shell"><div class="vt-frame"><div class="plan-grid"><article class="milestone"><div class="vt-kicker">M1</div><b>사전 평가</b><p class="vt-text">대표/실패/악성 입력 세트를 실행한다.</p></article><article class="milestone"><div class="vt-kicker">M2</div><b>제한 출시</b><p class="vt-text">내부 5%, 베타 20%, 전체 100%로 넓힌다.</p></article><article class="milestone plan-risk"><div class="vt-kicker">M3</div><b>중단 조건</b><p class="vt-text">신고율, 오류율, fallback 비율 임계값을 둔다.</p></article><article class="milestone"><div class="vt-kicker">M4</div><b>회고</b><p class="vt-text">출시 7일 후 실패 로그를 제품 결정으로 환원한다.</p></article></div></div></div>
""")


CHECK_VT18 = mark("vt-18 triage-board", """
<div class="vt-shell"><div class="vt-frame"><div class="board"><div class="board-col"><h3>출시 차단</h3><div class="ticket active">권한 없는 문서 노출</div><div class="ticket active">rollback flag 미준비</div></div><div class="board-col"><h3>출시 전 완화</h3><div class="ticket">유해 응답 FAQ 보강</div><div class="ticket">fallback 문구 승인</div></div><div class="board-col"><h3>모니터링</h3><div class="ticket">신고율 0.5% 초과</div><div class="ticket">p95 지연 2초 초과</div></div></div></div></div>
""")


CHECK_WG11 = mark("wg-11 weekly-status", """
<section class="wg-11" aria-labelledby="check-wg11-title">
  <header class="wg-11-head"><p class="wg-11-kicker">RELEASE READINESS</p><h2 id="check-wg11-title" class="wg-11-h">AI 기능 출시 준비 상태</h2><p class="wg-11-lead">데이터, 품질, 보안, 운영 게이트를 주간 상태판처럼 점검한다.</p></header>
  <div class="wg-11-kpis"><div class="wg-11-kpi"><span class="wg-11-kpi-v">8/10</span><span class="wg-11-kpi-l">데이터 게이트</span></div><div class="wg-11-kpi"><span class="wg-11-kpi-v">124</span><span class="wg-11-kpi-l">평가 fixture</span></div><div class="wg-11-kpi"><span class="wg-11-kpi-v wg-11-warn">3</span><span class="wg-11-kpi-l">차단 위험</span></div><div class="wg-11-kpi"><span class="wg-11-kpi-v">7일</span><span class="wg-11-kpi-l">모니터링</span></div></div>
  <h3 class="wg-11-h3">게이트 진행률</h3><div class="wg-11-bars"><div class="wg-11-bar-row"><span class="wg-11-bar-label">데이터 권한</span><div class="wg-11-track"><div class="wg-11-fill wg-11-fill-good" style="width:90%"></div></div><span class="wg-11-bar-pct">90%</span></div><div class="wg-11-bar-row"><span class="wg-11-bar-label">품질 평가</span><div class="wg-11-track"><div class="wg-11-fill wg-11-fill-prog" style="width:74%"></div></div><span class="wg-11-bar-pct">74%</span></div><div class="wg-11-bar-row"><span class="wg-11-bar-label">운영 대응</span><div class="wg-11-track"><div class="wg-11-fill wg-11-fill-risk" style="width:56%"></div></div><span class="wg-11-bar-pct">56%</span></div></div>
</section>
""")


CHECK_WG13 = mark("wg-13 annotated-flowchart", """
<section class="wg-13-fc" aria-label="AI 출시 게이트 플로우차트">
  <h3 class="wg-13-h">AI 출시 게이트 <span class="wg-13-sub">평가 통과 후 점진 출시</span></h3>
  <div class="wg-13-flow"><a href="#wg-13-s1" class="wg-13-node wg-13-node--start"><span class="wg-13-step">시작</span>릴리즈 후보</a><span class="wg-13-arrow" aria-hidden="true">&darr;</span><a href="#wg-13-s2" class="wg-13-node"><span class="wg-13-step">1</span>데이터 권한 확인</a><span class="wg-13-arrow" aria-hidden="true">&darr;</span><div class="wg-13-branch"><a href="#wg-13-s3" class="wg-13-node wg-13-node--decide"><span class="wg-13-step">2</span>P0 실패 모드 없음?</a><div class="wg-13-paths"><div class="wg-13-path wg-13-path--fail"><span class="wg-13-edge">아니오 &rarr; 실패 경로</span><a href="#wg-13-fail" class="wg-13-node wg-13-node--fail"><span class="wg-13-step">!</span>출시 중단</a></div><div class="wg-13-path wg-13-path--ok"><span class="wg-13-edge">예 &rarr; 정상 경로</span><a href="#wg-13-s4" class="wg-13-node"><span class="wg-13-step">3</span>카나리 출시</a><span class="wg-13-arrow" aria-hidden="true">&darr;</span><a href="#wg-13-s5" class="wg-13-node wg-13-node--end"><span class="wg-13-step">완료</span>7일 모니터링</a></div></div></div></div>
  <div class="wg-13-detail"><h4 class="wg-13-dh">단계 상세 <span class="wg-13-dnote">박스를 클릭하면 해당 단계로 이동</span></h4><details id="wg-13-s2" class="wg-13-acc" open><summary><span class="wg-13-tag">1단계</span>데이터 권한 확인</summary><div class="wg-13-body"><p>입력 데이터의 출처, 삭제 요청, 워크스페이스 권한을 확인한다.</p></div></details><details id="wg-13-s3" class="wg-13-acc"><summary><span class="wg-13-tag">2단계</span>P0 실패 모드</summary><div class="wg-13-body"><p>권한 없는 문서 노출, 개인정보 포함 응답, 차별적 추천은 출시 차단이다.</p></div></details><details id="wg-13-fail" class="wg-13-acc wg-13-acc--fail"><summary><span class="wg-13-tag wg-13-tag--fail">실패</span>출시 중단</summary><div class="wg-13-body"><p>owner와 완화 일정이 붙기 전까지 베타 범위를 넓히지 않는다.</p></div></details><details id="wg-13-s4" class="wg-13-acc"><summary><span class="wg-13-tag">3단계</span>카나리 출시</summary><div class="wg-13-body"><p>5% 트래픽으로 시작하고 신고율과 fallback 비율을 2시간 단위로 본다.</p></div></details><details id="wg-13-s5" class="wg-13-acc wg-13-acc--ok"><summary><span class="wg-13-tag wg-13-tag--ok">완료</span>7일 모니터링</summary><div class="wg-13-body"><p>7일 뒤 실패 로그를 제품 요구사항과 모델 평가 세트로 환원한다.</p></div></details></div>
</section>
""")


CHECK_WG16 = mark("wg-16 implementation-plan", """
<section class="wg-16" aria-labelledby="check-wg16-title">
  <header class="wg-16-head"><p class="wg-16-kicker">ROLLBACK PLAN</p><h2 id="check-wg16-title" class="wg-16-h">AI 기능 점진 출시 계획</h2><p class="wg-16-lead">평가 통과 후에도 바로 100% 출시하지 않고 플래그와 모니터링으로 범위를 넓힌다.</p></header>
  <h3 class="wg-16-h3">마일스톤</h3><ol class="wg-16-ms"><li class="wg-16-ms-item wg-16-done"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">M1 · 내부 dogfood</span><span class="wg-16-badge wg-16-bd-done">완료</span></div><p class="wg-16-ms-desc">내부 워크스페이스에서 50개 실패 질문을 실행한다.</p></div></li><li class="wg-16-ms-item wg-16-active"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">M2 · 베타 5%</span><span class="wg-16-badge wg-16-bd-active">진행 중</span></div><p class="wg-16-ms-desc">신고율과 fallback 비율을 기준으로 확대 여부를 판단한다.</p></div></li><li class="wg-16-ms-item"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">M3 · 50% 확대</span><span class="wg-16-badge">예정</span></div><p class="wg-16-ms-desc">권한 필터 통합 테스트가 재통과해야 한다.</p></div></li><li class="wg-16-ms-item"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">M4 · 전체 출시</span><span class="wg-16-badge">예정</span></div><p class="wg-16-ms-desc">온콜과 고객 공지 템플릿이 준비된 뒤 진행한다.</p></div></li></ol>
  <h3 class="wg-16-h3">리스크 평가</h3><div class="tbl table-scroll"><table class="wg-16-table"><caption>AI 출시 계획 리스크</caption><thead><tr><th scope="col">리스크</th><th scope="col">가능성</th><th scope="col">영향</th><th scope="col">완화책</th></tr></thead><tbody><tr><th scope="row">권한 필터 누락</th><td><span class="wg-16-lv wg-16-lv-lo">낮음</span></td><td><span class="wg-16-lv wg-16-lv-hi">높음</span></td><td>통합 테스트와 샘플 워크스페이스 교차 검증.</td></tr><tr><th scope="row">잘못된 자동 요약</th><td><span class="wg-16-lv wg-16-lv-mid">중</span></td><td><span class="wg-16-lv wg-16-lv-mid">중</span></td><td>원문 근거 링크와 사용자 수정 UI 제공.</td></tr><tr><th scope="row">운영 알림 과다</th><td><span class="wg-16-lv wg-16-lv-mid">중</span></td><td><span class="wg-16-lv wg-16-lv-lo">낮음</span></td><td>임계값을 신고율과 fallback 비율 중심으로 조정.</td></tr></tbody></table></div>
</section>
""")


CHECK_WG18 = mark("wg-18 ticket-triage-board", """
<section class="wg-18-board" aria-label="AI 출시 위험 보드">
  <header class="wg-18-head"><h2 class="wg-18-title">출시 위험 분류 보드</h2><p class="wg-18-hint">드래그앤드롭은 JS가 필요하다. 여기서는 정적 보드로 차단, 완화, 모니터링 상태를 보여준다.</p></header>
  <div class="wg-18-cols" role="list"><div class="wg-18-col" role="listitem"><div class="wg-18-col-head"><span class="wg-18-dot wg-18-dot--todo" aria-hidden="true"></span><h3 class="wg-18-col-name">출시 차단</h3><span class="wg-18-count" aria-label="2건">2</span></div><article class="wg-18-card" tabindex="0"><div class="wg-18-card-top"><span class="wg-18-id">AI-001</span><span class="wg-18-pri wg-18-pri--high">● 높음</span></div><p class="wg-18-card-title">권한 없는 문서가 요약에 포함될 수 있음</p><div class="wg-18-meta"><span class="wg-18-tag">security</span><span class="wg-18-assignee">security</span></div></article><article class="wg-18-card" tabindex="0"><div class="wg-18-card-top"><span class="wg-18-id">AI-004</span><span class="wg-18-pri wg-18-pri--high">● 높음</span></div><p class="wg-18-card-title">fallback UX와 중단 공지 문구 미승인</p><div class="wg-18-meta"><span class="wg-18-tag">ops</span><span class="wg-18-assignee">pm</span></div></article></div><div class="wg-18-col" role="listitem"><div class="wg-18-col-head"><span class="wg-18-dot wg-18-dot--prog" aria-hidden="true"></span><h3 class="wg-18-col-name">완화 중</h3><span class="wg-18-count" aria-label="2건">2</span></div><article class="wg-18-card wg-18-card--active" tabindex="0"><div class="wg-18-card-top"><span class="wg-18-id">AI-006</span><span class="wg-18-pri wg-18-pri--mid">● 보통</span></div><p class="wg-18-card-title">악성 프롬프트 평가 세트 20개 추가</p><div class="wg-18-meta"><span class="wg-18-tag">eval</span><span class="wg-18-assignee">ml</span></div></article><article class="wg-18-card wg-18-card--active" tabindex="0"><div class="wg-18-card-top"><span class="wg-18-id">AI-008</span><span class="wg-18-pri wg-18-pri--mid">● 보통</span></div><p class="wg-18-card-title">신고율 대시보드 알림 임계값 조정</p><div class="wg-18-meta"><span class="wg-18-tag">monitor</span><span class="wg-18-assignee">sre</span></div></article></div><div class="wg-18-col" role="listitem"><div class="wg-18-col-head"><span class="wg-18-dot wg-18-dot--done" aria-hidden="true"></span><h3 class="wg-18-col-name">완료</h3><span class="wg-18-count" aria-label="2건">2</span></div><article class="wg-18-card wg-18-card--done" tabindex="0"><div class="wg-18-card-top"><span class="wg-18-id">AI-002</span><span class="wg-18-pri">✓ 완료</span></div><p class="wg-18-card-title">데이터 보관 기간 문서화</p><div class="wg-18-meta"><span class="wg-18-tag">policy</span><span class="wg-18-assignee">legal</span></div></article><article class="wg-18-card wg-18-card--done" tabindex="0"><div class="wg-18-card-top"><span class="wg-18-id">AI-003</span><span class="wg-18-pri">✓ 완료</span></div><p class="wg-18-card-title">feature flag 생성과 rollback drill</p><div class="wg-18-meta"><span class="wg-18-tag">release</span><span class="wg-18-assignee">ops</span></div></article></div></div>
</section>
""")


CHECK_WG19 = mark("wg-19 feature-flag-editor", """
<section class="wg-19-editor" aria-label="AI 기능 출시 플래그">
  <header class="wg-19-head"><h2 class="wg-19-title">AI 출시 플래그</h2><p class="wg-19-hint">토글은 CSS-only로 상태가 바뀐다. 실제 서버 반영은 별도 API가 필요하다.</p></header>
  <ul class="wg-19-list"><li class="wg-19-row"><div class="wg-19-info"><span class="wg-19-key">ai_summary_beta</span><span class="wg-19-desc">베타 사용자에게 AI 요약 노출</span></div><span class="wg-19-env">prod</span><input class="wg-19-cb" type="checkbox" id="wg-19-f1" checked><label class="wg-19-toggle" for="wg-19-f1"><span class="wg-19-knob"></span><span class="wg-19-state wg-19-state--on">ON</span><span class="wg-19-state wg-19-state--off">OFF</span></label></li><li class="wg-19-row"><div class="wg-19-info"><span class="wg-19-key">ai_summary_100pct</span><span class="wg-19-desc">전체 사용자 확대</span><span class="wg-19-dep" role="note">⚠ 7일 모니터링 통과 필요</span></div><span class="wg-19-env">prod</span><input class="wg-19-cb" type="checkbox" id="wg-19-f2"><label class="wg-19-toggle" for="wg-19-f2"><span class="wg-19-knob"></span><span class="wg-19-state wg-19-state--on">ON</span><span class="wg-19-state wg-19-state--off">OFF</span></label></li><li class="wg-19-row"><div class="wg-19-info"><span class="wg-19-key">fallback_classic_summary</span><span class="wg-19-desc">AI 장애 시 기존 요약 UI 사용</span></div><span class="wg-19-env">prod</span><input class="wg-19-cb" type="checkbox" id="wg-19-f3" checked><label class="wg-19-toggle" for="wg-19-f3"><span class="wg-19-knob"></span><span class="wg-19-state wg-19-state--on">ON</span><span class="wg-19-state wg-19-state--off">OFF</span></label></li><li class="wg-19-row"><div class="wg-19-info"><span class="wg-19-key">log_raw_prompt</span><span class="wg-19-desc">원문 프롬프트 로그 저장</span><span class="wg-19-dep wg-19-dep--warn" role="note">⚠ 개인정보 위험으로 OFF 유지</span></div><span class="wg-19-env">prod</span><input class="wg-19-cb" type="checkbox" id="wg-19-f4"><label class="wg-19-toggle" for="wg-19-f4"><span class="wg-19-knob"></span><span class="wg-19-state wg-19-state--on">ON</span><span class="wg-19-state wg-19-state--off">OFF</span></label></li></ul>
</section>
""")


PAGE_11 = f"""
<main id="main" class="page-wide layout-case">
<header class="header"><div class="kicker">CASE STUDY</div><h1>예약 알림 지연 사고 케이스 스터디</h1><p class="sub">예약 알림이 42분 지연된 가상 사고를 영향, 원인, 조치, 재발 방지 관점에서 기록한다.</p><div class="meta"><span>case_study_html</span><span>case-study.html</span><span>profile auto</span><span>2026-06-05 08:34</span><span>템플릿 쇼케이스 확장</span></div></header>
<section class="summary-card"><div class="label">Overview</div><p><strong>SLO가 다른 작업을 같은 큐에 두면 우선순위를 잃는다.</strong> 고객 취소는 없었지만 상담 채널 대기 시간이 증가했고 알림 신뢰도가 흔들렸다.</p></section>
<section><h2><span class="no">1</span>사고 한 줄 요약</h2><p class="h2-sub">회고는 책임 추궁이 아니라 다음 포화 상황에서 더 빨리 감지하고 덜 섞이게 하는 기록이다.</p><div class="grid-2"><article class="mini-card"><h3>영향</h3><p>예약 리마인더 3,260건이 지연되고 최대 지연은 42분이었다.</p></article><article class="mini-card"><h3>탐지</h3><p>시스템 알림보다 CS 문의 증가가 먼저 도착했다.</p></article><article class="mini-card"><h3>원인</h3><p>캠페인 job과 리마인더 job이 같은 큐를 공유했다.</p></article><article class="mini-card"><h3>예방</h3><p>job age 지표, 전용 큐, 캠페인 pause switch를 추가한다.</p></article></div></section>
<section><h2><span class="no">2</span>vt-12 사고 요약</h2><p class="h2-sub">1순위 vt=incident-summary로 영향, 원인, 조치를 첫 화면에서 확인하게 한다.</p>{CASE_VT12}</section>
<section><h2><span class="no">3</span>vt-04 상세 타임라인</h2><p class="h2-sub">후순위 vt=timeline으로 감지, 진단, 완화, 복구, 회고 순서를 고정한다.</p>{CASE_VT04}</section>
<section><h2><span class="no">4</span>wg-12 포스트모템 타임라인</h2><p class="h2-sub">권장 wg-12를 실제 사고 회고 위젯으로 변환했다.</p>{CASE_WG12}</section>
<section><h2><span class="no">5</span>vt-14 대응 swimlane</h2><p class="h2-sub">후순위 vt=process-swimlane으로 CS, 온콜, 그로스, 플랫폼의 책임 흐름을 나눈다.</p>{CASE_VT14}</section>
<section><h2><span class="no">6</span>영향 분석</h2><p class="h2-sub">사용자 영향과 내부 운영 영향을 분리해야 재발 방지 우선순위가 선명해진다.</p><div class="tbl table-scroll"><table><caption>예약 알림 지연 영향 분석</caption><thead><tr><th>영향 영역</th><th>관측값</th><th>사업 영향</th><th>후속 조치</th></tr></thead><tbody><tr><td>고객</td><td>알림 최대 42분 지연</td><td>예약 준비 시간 감소</td><td>지연 공지 템플릿</td></tr><tr><td>CS</td><td>문의 128건 증가</td><td>응답 대기 증가</td><td>상태 페이지 연결</td></tr><tr><td>시스템</td><td>job age p99 41분</td><td>SLO 위반</td><td>전용 큐와 알림</td></tr><tr><td>그로스</td><td>캠페인 중단</td><td>발송 목표 지연</td><td>rate limit 협의</td></tr></tbody></table></div></section>
<section><h2><span class="no">7</span>근본 원인</h2><p class="h2-sub">직접 원인은 큐 적체지만 근본 원인은 SLO별 격리와 감지 기준이 없었던 것이다.</p><ol><li>캠페인 job 생성량 증가가 리마인더 큐를 점유했다.</li><li>worker pool이 공유되어 리마인더 우선 처리가 불가능했다.</li><li>큐 depth만 보고 job age p95/p99를 보지 않았다.</li><li>캠페인 pause switch가 운영자에게 노출되어 있지 않았다.</li></ol></section>
<section><h2><span class="no">8</span>수정 계획</h2><p class="h2-sub">단기 완화와 구조 개선을 분리해 재발 방지 액션을 추적한다.</p><div class="tbl table-scroll"><table><caption>재발 방지 액션 계획</caption><thead><tr><th>액션</th><th>소유자</th><th>기한</th><th>완료 기준</th></tr></thead><tbody><tr><td>리마인더 전용 큐</td><td>platform</td><td>D+7</td><td>캠페인 부하와 독립 처리</td></tr><tr><td>job age 알림</td><td>sre</td><td>D+3</td><td>p95 5분 초과 알림</td></tr><tr><td>캠페인 pause switch</td><td>growth</td><td>D+10</td><td>온콜이 즉시 중지 가능</td></tr><tr><td>큐 포화 게임데이</td><td>team</td><td>D+30</td><td>복구 절차 20분 이내</td></tr></tbody></table></div></section>
<section><h2><span class="no">9</span>재발 감지 지표</h2><p class="h2-sub">큐 depth보다 사용자 지연을 설명하는 지표를 앞에 둔다.</p><ul><li>reminder job age p50/p95/p99</li><li>worker 처리량과 실패율</li><li>캠페인 job 생성량과 rate limit hit</li><li>CS 문의 키워드: 알림, 예약, 지연</li><li>예약 시작 30분 전 알림 도착률</li></ul></section>
<section><h2><span class="no">10</span>회고 결론</h2><p class="h2-sub">사고의 핵심 교훈은 작업을 빨리 처리하는 것이 아니라 중요한 작업이 섞이지 않게 하는 것이다.</p><p>이번 케이스의 권장 조치는 큐 분리, job age 기반 알림, 캠페인 rate limit, pause switch, 분기별 게임데이다. 완료 기준은 지연이 다시 생기지 않는다는 약속이 아니라 지연을 더 빨리 보고 더 좁게 멈출 수 있는 구조다.</p></section>
<section class="try"><div class="label">NEXT ACTION</div><h2>바로 실행할 일</h2><ol><li>전용 큐와 worker pool을 만든다.</li><li>job age p95/p99 알림을 배포한다.</li><li>캠페인 pause switch를 온콜 런북에 넣는다.</li><li>30일 안에 큐 포화 게임데이를 진행한다.</li></ol></section>
<aside class="source-note"><div class="label">Source Note</div><p>가상의 예약 알림 지연 사고를 기반으로 한 케이스 스터디 예시다.</p></aside></main>
"""


PAGE_12 = f"""
<main id="main" class="page-wide layout-landing">
<header class="header"><div class="kicker">LANDING BRIEF</div><h1>LocalNote 팀 지식관리 랜딩 브리프</h1><p class="sub">회의록, 의사결정, 운영 문서를 한곳에서 찾고 연결하는 작은 팀용 지식관리 제품 브리프다.</p><div class="meta"><span>landing_brief_html</span><span>landing-brief.html</span><span>profile auto</span><span>2026-06-05 08:34</span><span>템플릿 쇼케이스 확장</span></div></header>
<section class="summary-card"><div class="label">Overview</div><p><strong>회의가 끝난 뒤에도 결정이 살아 있어야 한다.</strong> LocalNote는 회의록을 단순 저장하지 않고 결정, 근거, 담당자, 후속 작업을 연결한다.</p></section>
<section><h2><span class="no">1</span>제품 약속</h2><p class="h2-sub">랜딩은 기능 나열보다 팀이 반복 설명을 줄이는 장면을 먼저 보여줘야 한다.</p><div class="grid-2"><article class="mini-card"><h3>사용자</h3><p>10~50명 규모의 제품팀, 운영팀, 고객 성공팀.</p></article><article class="mini-card"><h3>문제</h3><p>결정과 근거가 회의록, 채팅, 이슈에 흩어진다.</p></article><article class="mini-card"><h3>전환</h3><p>첫 프로젝트 생성과 회의록 3개 업로드로 좁힌다.</p></article><article class="mini-card"><h3>증거</h3><p>다음 회의 전 미완료 작업과 오래된 결정을 보여준다.</p></article></div></section>
<section><h2><span class="no">2</span>vt-01 히어로 맵</h2><p class="h2-sub">1순위 vt=hero-map으로 문제, 지도, 행동을 한 화면에 연결한다.</p>{LANDING_VT01}</section>
<section><h2><span class="no">3</span>vt-07 기능 카드 그리드</h2><p class="h2-sub">후순위 vt=card-grid로 제품이 만드는 지식 흐름을 보여준다.</p>{LANDING_VT07}</section>
<section><h2><span class="no">4</span>wg-02 포지셔닝 방향</h2><p class="h2-sub">권장 wg-02로 검색 도구가 아니라 결정 재사용 제품이라는 방향을 고른다.</p>{LANDING_WG02}</section>
<section><h2><span class="no">5</span>wg-08 온보딩 플로우</h2><p class="h2-sub">권장 wg-08로 첫 프로젝트 생성 흐름을 클릭 가능한 CSS-only 프로토타입으로 보여준다.</p>{LANDING_WG08}</section>
<section><h2><span class="no">6</span>wg-05 메시지 시스템</h2><p class="h2-sub">권장 wg-05를 디자인 토큰 대신 제품 메시지 토큰으로 사용한다.</p>{LANDING_WG05}</section>
<section><h2><span class="no">7</span>vt-19 기능 플래그</h2><p class="h2-sub">후순위 vt=feature-flag로 기본 활성 기능과 보안상 꺼둘 기능을 구분한다.</p>{LANDING_VT19}</section>
<section><h2><span class="no">8</span>wg-16 출시 계획</h2><p class="h2-sub">권장 wg-16으로 랜딩 브리프가 실제 출시 계획으로 이어지게 한다.</p>{LANDING_WG16}</section>
<section><h2><span class="no">9</span>wg-09 공유용 피치 덱</h2><p class="h2-sub">권장 wg-09로 팀에 설명하는 4장짜리 짧은 피치 덱을 제공한다.</p>{LANDING_WG09}</section>
<section><h2><span class="no">10</span>FAQ와 CTA</h2><p class="h2-sub">랜딩 FAQ는 "채팅 검색과 뭐가 다른가"를 정면으로 답하고 첫 프로젝트 생성으로 닫는다.</p><div class="tbl table-scroll"><table><caption>LocalNote FAQ와 CTA</caption><thead><tr><th>질문</th><th>답변</th><th>CTA</th></tr></thead><tbody><tr><td>Slack 검색과 무엇이 다른가?</td><td>대화 검색이 아니라 결정, 근거, 액션을 구조화한다.</td><td>샘플 결정 보기</td></tr><tr><td>회의록 원문은 보존되는가?</td><td>원문과 요약을 분리하고 결정 변경 이력을 남긴다.</td><td>보존 정책 보기</td></tr><tr><td>권한은 어떻게 막는가?</td><td>프로젝트 단위 기본 비공개, 공유 전 검토를 제공한다.</td><td>보안 FAQ 보기</td></tr><tr><td>처음 무엇을 넣어야 하나?</td><td>최근 회의록 3개와 반복 질문 5개로 시작한다.</td><td>첫 프로젝트 만들기</td></tr></tbody></table></div><p>5분 안에 첫 결정 타임라인이 보여야 랜딩의 약속이 성립한다.</p></section>
<section class="try"><div class="label">NEXT ACTION</div><h2>바로 실행할 일</h2><ol><li>첫 프로젝트를 만든다.</li><li>회의록 3개를 업로드한다.</li><li>결정 문장과 담당자를 확인한다.</li><li>다음 회의 전 미완료 액션을 리뷰한다.</li></ol></section>
<aside class="source-note"><div class="label">Source Note</div><p>가상의 팀 지식관리 제품 랜딩 브리프 예시다.</p></aside></main>
"""


PAGE_13 = f"""
<main id="main" class="page-wide layout-checklist">
<header class="header"><div class="kicker">CHECKLIST PLAYBOOK</div><h1>AI 기능 출시 전 안전성 플레이북</h1><p class="sub">AI 기능을 출시하기 전에 데이터, 품질, 보안, 운영, 사용자 커뮤니케이션을 점검하는 실무 플레이북이다.</p><div class="meta"><span>checklist_playbook</span><span>checklist-playbook.html</span><span>profile auto</span><span>2026-06-05 08:34</span><span>템플릿 쇼케이스 확장</span></div></header>
<section class="summary-card"><div class="label">Overview</div><p><strong>AI 기능 출시는 빠른 감지와 안전한 되돌림이 핵심이다.</strong> 요약, 추천, 분류, 자동 작성처럼 사용자 판단에 영향을 주는 기능은 출시 전 별도 안전성 게이트가 필요하다.</p></section>
<section><h2><span class="no">1</span>출시 전 원칙</h2><p class="h2-sub">P0 실패 모드가 남아 있으면 출시하지 않고, P1 위험은 owner와 완화 일정이 있을 때만 허용한다.</p><div class="grid-2"><article class="mini-card"><h3>데이터</h3><p>개인정보, 삭제 요청, 출처 권한을 확인한다.</p></article><article class="mini-card"><h3>품질</h3><p>대표 질문 세트와 금지 응답을 평가한다.</p></article><article class="mini-card"><h3>보안</h3><p>권한 없는 문서 노출과 프롬프트 공격을 막는다.</p></article><article class="mini-card"><h3>운영</h3><p>feature flag, fallback, 온콜을 준비한다.</p></article></div></section>
<section><h2><span class="no">2</span>vt-05 체크리스트 플로우</h2><p class="h2-sub">1순위 vt=checklist-flow로 출시 전 확인 항목과 상태를 고정한다.</p>{CHECK_VT05}</section>
<section><h2><span class="no">3</span>vt-06 품질 게이트</h2><p class="h2-sub">후순위 vt=quality-gate로 차단, 경고, 통과 기준을 분리한다.</p>{CHECK_VT06}</section>
<section><h2><span class="no">4</span>wg-13 주석 플로우차트</h2><p class="h2-sub">권장 wg-13으로 출시 게이트의 정상 경로와 실패 경로를 클릭 가능한 구조로 보여준다.</p>{CHECK_WG13}</section>
<section><h2><span class="no">5</span>wg-11 준비 상태판</h2><p class="h2-sub">권장 wg-11로 데이터, 품질, 보안, 운영 게이트 진행률을 보여준다.</p>{CHECK_WG11}</section>
<section><h2><span class="no">6</span>vt-14 책임 swimlane</h2><p class="h2-sub">후순위 vt=process-swimlane으로 PM, ML, 보안, 운영의 책임을 나눈다.</p>{CHECK_VT14}</section>
<section><h2><span class="no">7</span>wg-16 점진 출시 계획</h2><p class="h2-sub">권장 wg-16으로 베타, 확대, 전체 출시의 조건을 고정한다.</p>{CHECK_WG16}</section>
<section><h2><span class="no">8</span>wg-18 위험 분류 보드</h2><p class="h2-sub">권장 wg-18로 차단, 완화, 모니터링 위험을 정적 보드로 보여준다.</p>{CHECK_WG18}</section>
<section><h2><span class="no">9</span>wg-19 출시 플래그</h2><p class="h2-sub">권장 wg-19로 베타, 전체 확대, fallback, 위험 로그 플래그를 점검한다.</p>{CHECK_WG19}</section>
<section><h2><span class="no">10</span>최종 검증표</h2><p class="h2-sub">플레이북은 체크리스트가 아니라 출시 여부를 결정하는 게이트여야 한다.</p><div class="tbl table-scroll"><table><caption>AI 기능 출시 최종 검증표</caption><thead><tr><th>게이트</th><th>통과 기준</th><th>실패 시 결정</th></tr></thead><tbody><tr><td>데이터 권한</td><td>출처, 권한, 삭제 요청 데이터 확인</td><td>출시 차단</td></tr><tr><td>품질 평가</td><td>대표/실패/악성 fixture 통과</td><td>베타 범위 축소</td></tr><tr><td>보안</td><td>권한 없는 문서 노출 0건</td><td>출시 차단</td></tr><tr><td>운영</td><td>fallback, flag, 온콜, 공지 준비</td><td>점진 출시만 허용</td></tr></tbody></table></div></section>
<section class="try"><div class="label">NEXT ACTION</div><h2>바로 실행할 일</h2><ol><li>데이터 권한을 확인한다.</li><li>평가 세트를 실행한다.</li><li>feature flag를 준비한다.</li><li>출시 7일 모니터링 담당자를 정한다.</li></ol></section>
<aside class="source-note"><div class="label">Source Note</div><p>AI 기능 출시 안전성 점검을 위한 가상 플레이북 예시다.</p></aside></main>
"""


def main() -> None:
    pages = {
        "11-reservation-reminder-delay-case-study.html": PAGE_11,
        "12-localnote-team-knowledge-landing.html": PAGE_12,
        "13-ai-feature-release-safety-playbook.html": PAGE_13,
    }
    for filename, html in pages.items():
        replace_main(filename, html)
        print(f"updated {filename}")


if __name__ == "__main__":
    main()
