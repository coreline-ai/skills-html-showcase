#!/usr/bin/env python3
"""Mode 15 / 17 — case_study_html (sequential). Topic: 결제 정산 배치 8시간 지연 장애 사후 분석.
Layout: case-study.html (.layout-case) · auto · vt: incident-summary(inc-head,inc-card) · wg: wg-12.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _finalize import build_page, write_sources, h2, SKILL, ASSETS  # noqa: E402,F401

for _p in [SKILL/"SKILL.md", SKILL/"references/layout-system.md", ASSETS/"layouts/case-study.html",
           ASSETS/"visual-html-templates/12-incident-summary.html", ASSETS/"widget-templates/12-incident-timeline.html"]:
    _p.read_text(encoding="utf-8")

TITLE = "결제 정산 배치 8시간 지연 장애 사후 분석"
DESC = "야간 정산 배치가 8시간 지연되어 정산 지급이 밀린 장애의 사후 분석. 상황·타임라인·대응 결정·결과·근본 원인·재발 방지를 기록한 case_study."

header = '''
<header class="header case-header">
  <div class="kicker"><span class="kicker-text">CASE STUDY · MODE 15 / 17 · 독립 빌드</span></div>
  <h1>정산 배치 8시간 지연 — 무엇이, 왜, 어떻게</h1>
  <p class="sub">야간 정산 배치가 평소 40분에서 8시간으로 늘어 아침 정산 지급이 밀린 장애를, 비난이 아니라 학습을 위해 기록한다. 같은 일을 두 번 겪지 않기 위한 사후 분석이다.</p>
  <div class="meta"><span>profile auto</span><span>layout case-study</span><span>SEV-2 · 정산 도메인</span><span>비난 없는 회고</span></div>
  <div class="generated-row"><p class="generated-date">Generated · 2026-06-13 KST</p>
  <div class="lens-strip" aria-label="적용 렌즈"><span class="lens-strip-label">LENS</span><span class="lens-chip">상황</span><span class="lens-chip">타임라인</span><span class="lens-chip">결정</span><span class="lens-chip">근본 원인</span><span class="lens-chip">재발 방지</span></div></div>
</header>'''

toc = '''
<nav class="toc-map case-toc" aria-label="케이스 목차"><div class="toc-pills">
  <a class="toc-pill" href="#s1"><b>01</b> 상황 요약</a><a class="toc-pill" href="#s2"><b>02</b> 영향·원인·조치</a>
  <a class="toc-pill" href="#s3"><b>03</b> 분 단위 타임라인</a><a class="toc-pill" href="#s4"><b>04</b> 대응 중 결정</a>
  <a class="toc-pill" href="#s5"><b>05</b> 결과·지표</a><a class="toc-pill" href="#s6"><b>06</b> 근본 원인(5 Whys)</a>
  <a class="toc-pill" href="#s7"><b>07</b> 영향 범위 분석</a><a class="toc-pill" href="#s8"><b>08</b> 재발 방지 액션</a>
  <a class="toc-pill" href="#s9"><b>09</b> 무엇을 배웠나</a><a class="toc-pill" href="#snext"><b>→</b> 다음 행동</a>
</div></nav>'''

s1 = f'''
<section id="s1" class="summary-card">
  {h2("01","상황 요약","case")}
  <p class="h2-sub">한 문장으로: 야간 정산 배치가 입력 데이터 급증과 비효율 쿼리가 겹쳐 8시간 지연됐고, 아침 정산 지급이 4시간 밀렸다.</p>
  <div class="grid-3">
    <article class="score-card"><h3>무슨 일</h3><p>매일 02:00에 도는 정산 배치가 평소 40분 → 8시간으로 늘었다. 가맹점 정산 지급 마감(09:00)을 넘겨 일부 지급이 지연됐다.</p></article>
    <article class="score-card"><h3>왜 중요</h3><p>정산 지연은 가맹점 신뢰·자금 흐름에 직접 영향을 준다. CS 문의가 급증했고, 수동 지급 보정이 필요했다.</p></article>
    <article class="score-card"><h3>현재 상태</h3><p>당일 수동 보정으로 지급 완료, 배치는 임시 분할 실행으로 복구. 근본 수정은 재발 방지 액션으로 진행 중.</p></article>
  </div>
  <p>이 회고의 목적은 "누가 잘못했나"가 아니라 "어떤 조건이 겹쳐 이 일이 가능했나"를 드러내는 것이다. 사람은 주어진 시스템 안에서 합리적으로 행동했고, 문제는 그 시스템의 사각지대에 있었다.</p>
</section>'''

s2 = f'''
<section id="s2" class="summary-card">
  {h2("02","영향·원인·조치 한눈에","warning")}
  <p class="h2-sub">세부 타임라인 전에, 장애의 뼈대를 세 칸으로 먼저 본다.</p>
  <section class="vt-shell" aria-label="장애 요약">
    <div class="vt-frame"><div>
      <div class="inc-head">
        <div class="inc-card impact"><b>영향</b><p class="vt-text">정산 지급 4시간 지연, 가맹점 CS 문의 약 120건, 수동 보정 발생</p></div>
        <div class="inc-card cause"><b>원인</b><p class="vt-text">거래량 급증 + 정산 쿼리 풀스캔 + 단일 배치 직렬 실행</p></div>
        <div class="inc-card action"><b>조치</b><p class="vt-text">배치 가맹점 그룹 분할 병렬 실행 + 수동 지급 보정</p></div>
      </div>
      <ol class="tl" style="margin-top:12px">
        <li class="tl-item"><b>02:00 시작</b><p class="vt-text">정산 배치 평소처럼 시작</p></li>
        <li class="tl-item"><b>04:30 이상 감지</b><p class="vt-text">평소 완료 시각 초과, 알림 발화</p></li>
        <li class="tl-item"><b>09:50 복구</b><p class="vt-text">분할 실행 + 수동 보정으로 지급 완료</p></li>
      </ol>
    </div></div>
  </section>
  <p>핵심은 단일 원인이 아니라 "세 조건의 동시 발생"이다. 거래량 급증만으로도, 풀스캔만으로도 평소엔 버텼지만, 셋이 겹치자 배치가 마감 시각을 넘겼다. 사후 분석은 이 "겹침"을 푸는 데 집중한다.</p>
</section>'''

s3 = f'''
<section id="s3" class="summary-card">
  {h2("03","분 단위 타임라인","timeline")}
  <p class="h2-sub">감지부터 복구까지의 흐름을 분 단위로 기록한다. 대응 지연 구간이 다음 개선 지점이다.</p>
  <section class="wg-12" aria-labelledby="m15-wg12-title">
    <header class="wg-12-head">
      <p class="wg-12-kicker">포스트모템 · SEV-2</p>
      <h2 id="m15-wg12-title" class="wg-12-h">INC-3007 정산 배치 지연 장애</h2>
      <div class="wg-12-meta"><span class="wg-12-chip">발생 2026-06-10 02:00 KST</span><span class="wg-12-chip">지연 약 8시간</span><span class="wg-12-chip wg-12-chip-sev">SEV-2</span><span class="wg-12-chip">담당 정산플랫폼팀</span></div>
    </header>
    <h3 class="wg-12-h3">타임라인</h3>
    <ol class="wg-12-tl">
      <li class="wg-12-tl-item"><span class="wg-12-tl-time">02:00</span><span class="wg-12-tl-dot wg-12-dot-detect"></span><div class="wg-12-tl-body"><strong>시작</strong> — 정산 배치 평소처럼 시작</div></li>
      <li class="wg-12-tl-item"><span class="wg-12-tl-time">04:30</span><span class="wg-12-tl-dot"></span><div class="wg-12-tl-body"><strong>감지</strong> — 완료 예상 시각(02:40) 크게 초과, 지연 알림 발화</div></li>
      <li class="wg-12-tl-item"><span class="wg-12-tl-time">05:10</span><span class="wg-12-tl-dot"></span><div class="wg-12-tl-body"><strong>원인 추정</strong> — DB CPU 포화·정산 쿼리 풀스캔 확인, 전일 거래량 급증 파악</div></li>
      <li class="wg-12-tl-item"><span class="wg-12-tl-time">07:20</span><span class="wg-12-tl-dot wg-12-dot-mit"></span><div class="wg-12-tl-body"><strong>완화</strong> — 가맹점 그룹별 배치 분할 병렬 실행으로 전환</div></li>
      <li class="wg-12-tl-item"><span class="wg-12-tl-time">09:50</span><span class="wg-12-tl-dot wg-12-dot-resolve"></span><div class="wg-12-tl-body"><strong>복구</strong> — 분할 실행 완료 + 지연 지급분 수동 보정 완료</div></li>
    </ol>
    <h3 class="wg-12-h3">영향 · 원인 · 조치</h3>
    <div class="table-scroll"><table class="wg-12-table">
      <caption>INC-3007 영향·원인·조치 요약</caption>
      <thead><tr><th scope="col">구분</th><th scope="col">내용</th></tr></thead>
      <tbody>
        <tr><th scope="row"><span class="wg-12-rk wg-12-rk-impact">영향</span></th><td>정산 지급 4시간 지연, CS 문의 약 120건, 가맹점 신뢰 영향</td></tr>
        <tr><th scope="row"><span class="wg-12-rk wg-12-rk-cause">원인</span></th><td>거래량 급증 + 인덱스 미스로 인한 풀스캔 + 단일 직렬 배치</td></tr>
        <tr><th scope="row"><span class="wg-12-rk wg-12-rk-action">조치</span></th><td>배치 분할 병렬화(임시), 정산 쿼리 인덱스 추가(영구), 마감 알림 임계 신설</td></tr>
      </tbody>
    </table></div>
    <h3 class="wg-12-h3">후속 액션</h3>
    <ul class="wg-12-check">
      <li class="wg-12-ck"><input type="checkbox" id="m15-c1" class="wg-12-ck-in" checked><label for="m15-c1" class="wg-12-ck-lb"><span class="wg-12-ck-box"></span><span class="wg-12-ck-txt">정산 쿼리 인덱스 추가 <span class="wg-12-owner">@dba</span></span></label></li>
      <li class="wg-12-ck"><input type="checkbox" id="m15-c2" class="wg-12-ck-in"><label for="m15-c2" class="wg-12-ck-lb"><span class="wg-12-ck-box"></span><span class="wg-12-ck-txt">배치 가맹점 그룹 분할 병렬화 정식화 <span class="wg-12-owner">@batch</span></span></label></li>
      <li class="wg-12-ck"><input type="checkbox" id="m15-c3" class="wg-12-ck-in"><label for="m15-c3" class="wg-12-ck-lb"><span class="wg-12-ck-box"></span><span class="wg-12-ck-txt">마감 90분 전 진척 예측 알림 도입 <span class="wg-12-owner">@sre</span></span></label></li>
    </ul>
    <p class="wg-12-ck-foot" aria-live="off">체크 상태는 표시용입니다 — 저장·집계 등 완전 인터랙션은 JS 필요.</p>
  </section>
</section>'''

s4 = f'''
<section id="s4" class="decisions summary-card">
  {h2("04","대응 중 결정","decision")}
  <p class="h2-sub">장애 중 내린 판단과 그 근거를 기록한다. 옳았던 결정과 아쉬웠던 결정을 함께 남긴다.</p>
  <div class="grid-2">
    <article class="good"><span class="label">옳았던 결정</span><p>"원인 완전 규명보다 마감 전 복구 우선" — 분할 병렬 실행으로 일단 지급을 끝내고, 인덱스 수정은 사후로 미룬 판단. 복구와 분석을 분리한 것이 마감 피해를 줄였다.</p></article>
    <article class="danger"><span class="label">아쉬웠던 결정</span><p>감지(04:30)에서 완화 착수(07:20)까지 약 3시간. "조금 더 기다리면 끝나겠지"라는 기대로 완화 결정이 늦었다. 마감 역산 알림이 없어 시간 압박을 체감하지 못했다.</p></article>
  </div>
  <p>가장 큰 교훈은 결정의 내용이 아니라 타이밍이다. 옳은 완화책(분할 실행)을 알고 있었지만, "끝나길 기다리는" 관성 때문에 늦게 꺼냈다. 마감까지 남은 시간을 강제로 보여주는 장치가 있었다면 더 빨리 움직였을 것이다.</p>
</section>'''

s5 = f'''
<section id="s5" class="results summary-card">
  {h2("05","결과·지표","metric")}
  <p class="h2-sub">장애의 정량 결과와 복구 지표를 기록한다. 숫자가 다음 개선의 기준선이 된다.</p>
  <div class="table-scroll"><table>
    <caption>장애 결과 지표</caption>
    <thead><tr><th>지표</th><th>평소</th><th>장애 시</th><th>비고</th></tr></thead>
    <tbody>
      <tr><th>배치 소요</th><td>약 40분</td><td>약 8시간</td><td>12배 증가</td></tr>
      <tr><th>지급 지연</th><td>0</td><td>4시간</td><td>마감 09:00 초과</td></tr>
      <tr><th>감지→완화</th><td>—</td><td>약 3시간</td><td>핵심 개선 구간</td></tr>
      <tr><th>CS 문의</th><td>평소 수준</td><td>약 120건</td><td>가맹점 정산 관련</td></tr>
    </tbody>
  </table></div>
  <p>가장 주목할 숫자는 "감지→완화 3시간"이다. 배치가 느려진 것 자체는 외부 요인(거래량)이 컸지만, 그 3시간은 우리가 줄일 수 있는 구간이다. 다음 개선의 목표 지표를 여기에 둔다.</p>
</section>'''

s6 = f'''
<section id="s6" class="summary-card">
  {h2("06","근본 원인 (5 Whys)","search")}
  <p class="h2-sub">"왜"를 다섯 번 물어 표면 증상에서 시스템 결함으로 내려간다.</p>
  <ol class="practice-list">
    <li><strong>왜 지연됐나?</strong> 배치가 8시간 걸렸다.</li>
    <li><strong>왜 8시간?</strong> 정산 쿼리가 풀스캔으로 돌았다.</li>
    <li><strong>왜 풀스캔?</strong> 거래량이 임계를 넘자 옵티마이저가 인덱스 대신 풀스캔을 택했고, 정산 기준 컬럼에 적합한 복합 인덱스가 없었다.</li>
    <li><strong>왜 인덱스가 없었나?</strong> 평소 거래량에선 풀스캔도 40분이라 문제가 드러나지 않아, 인덱스 필요성이 인지되지 않았다.</li>
    <li><strong>왜 마감 전에 못 막았나?</strong> 배치 "지연"은 감지했지만 "마감까지 남은 시간" 기준 경보가 없어 긴급도를 체감하지 못했다.</li>
  </ol>
  <div class="good"><span class="label">진짜 원인</span><p>표면 원인은 풀스캔이지만, 근본 원인은 두 가지 <strong>사각지대</strong>다 — ① 거래량 임계를 넘으면 쿼리 계획이 바뀐다는 점이 모니터링되지 않았고, ② 경보가 "지연 시간"이 아니라 "마감 역산"으로 설계되지 않았다.</p></div>
</section>'''

s7 = f'''
<section id="s7" class="summary-card">
  {h2("07","영향 범위 분석","impact")}
  <p class="h2-sub">장애가 어디까지 번졌는지, 무엇은 다행히 막혔는지 분리해 본다.</p>
  <div class="card-grid">
    <article class="mini-card"><h3>직접 영향</h3><p>정산 지급 4시간 지연, 일부 가맹점의 자금 일정 차질, CS 문의 급증.</p></article>
    <article class="mini-card"><h3>간접 영향</h3><p>운영팀 새벽 대응 피로, 수동 보정 과정에서의 추가 실수 위험.</p></article>
    <article class="mini-card"><h3>막힌 것</h3><p>결제 승인(실시간 경로)은 영향 없음 — 정산 배치와 분리돼 있어 본 장애가 결제로 번지지 않았다.</p></article>
    <article class="mini-card"><h3>데이터 정합성</h3><p>지연됐을 뿐 금액 오류·중복 지급은 없음. 수동 보정도 검증 후 진행해 정합성 유지.</p></article>
  </div>
  <p>다행인 점은 "결제와 정산이 분리"돼 있어 실시간 결제로 번지지 않은 것이다. 이 격리가 없었다면 SEV-1로 커졌을 것이다. 즉 기존의 좋은 설계 결정(경로 분리) 하나가 피해를 한 도메인에 가뒀다.</p>
</section>'''

s8 = f'''
<section id="s8" class="summary-card">
  {h2("08","재발 방지 액션","check")}
  <p class="h2-sub">"다시는 안 그러겠다"가 아니라, 같은 조건에서 자동으로 막히도록 시스템을 바꾼다.</p>
  <ul class="check-list">
    <li><strong>인덱스(영구)</strong> — 정산 기준 컬럼 복합 인덱스 추가 + 쿼리 계획 회귀 테스트. 거래량이 늘어도 풀스캔으로 떨어지지 않게 한다.</li>
    <li><strong>분할 병렬화(영구)</strong> — 가맹점 그룹 분할 병렬 실행을 임시 조치가 아니라 정식 배치 구조로 승격.</li>
    <li><strong>마감 역산 경보</strong> — "지연 시간"이 아니라 "마감까지 남은 시간 대비 진척"으로 경보를 재설계. 마감 90분 전 미완료 예측 시 발화.</li>
    <li><strong>쿼리 계획 모니터링</strong> — 정산 쿼리가 인덱스 대신 풀스캔으로 전환되면 알림.</li>
  </ul>
  <p>네 액션의 우선순위는 "마감 역산 경보"가 가장 높다. 인덱스·병렬화는 이번 원인을 막지만, 경보 재설계는 <strong>다음에 모르는 원인으로 느려져도</strong> 우리가 더 빨리 움직이게 해 준다. 즉 특정 원인이 아니라 "대응 속도" 자체를 고치는 액션이다.</p>
</section>'''

s9 = f'''
<section id="s9" class="summary-card">
  {h2("09","무엇을 배웠나","idea")}
  <p class="h2-sub">이 장애가 남긴 일반화 가능한 교훈 세 가지.</p>
  <div class="card-grid">
    <article class="mini-card"><h3>임계는 비선형</h3><p>"평소 40분"은 위험을 숨긴다. 거래량 같은 입력이 임계를 넘으면 쿼리 계획이 비선형으로 나빠질 수 있다. 평균이 아니라 임계 부근을 본다.</p></article>
    <article class="mini-card"><h3>경보는 마감 기준</h3><p>"느림"이 아니라 "마감을 지킬 수 있나"로 경보를 설계해야 긴급도가 전달된다.</p></article>
    <article class="mini-card"><h3>복구와 분석 분리</h3><p>장애 중에는 원인 규명보다 복구가 먼저다. 분석은 사후에, 충분히.</p></article>
  </div>
  <p>가장 값진 교훈은 "비난 없는 회고"가 작동했다는 것이다. 누구를 탓하는 대신 시스템의 사각지대를 찾았기에, 사람들이 솔직하게 타이밍 실수(완화 지연)까지 기록할 수 있었다. 그 솔직함이 가장 중요한 개선(마감 역산 경보)을 끌어냈다.</p>
</section>'''

snext = f'''
<section id="snext" class="try">
  {h2(None,"다음 행동","landing")}
  <p>사후 분석의 가치는 액션이 실제로 닫힐 때 나온다. 기한과 담당을 명확히 해 추적한다.</p>
  <div class="cta-box">
    <p><strong>2주 내 완료 목표</strong></p>
    <ol><li>정산 쿼리 인덱스 추가 + 쿼리 계획 회귀 테스트(@dba).</li><li>마감 역산 진척 예측 경보 도입(@sre) — 최우선.</li><li>배치 분할 병렬화 정식 구조로 승격(@batch).</li><li>2주 뒤 액션 완료 여부 회고 재점검.</li></ol>
    <div class="tag-list"><span class="tag">case_study</span><span class="tag">postmortem</span><span class="tag">정산</span><span class="tag">blameless</span></div>
  </div>
</section>'''

source_note = '<aside class="source-note"><p><strong>출처·범위.</strong> 본 사후 분석은 정산 배치 지연 장애 시나리오를 사후 분석 형식으로 재구성한 사례다. 시각·수치(8시간·120건 등)는 사례 설명을 위한 값이며 특정 실제 사건을 지칭하지 않는다. 실제 포스트모템은 로그·메트릭 원본과 함께 작성한다.</p></aside>'

body = ('<main id="main" class="page-wide layout-case">' + header + toc + s1+s2+s3+s4+s5+s6+s7+s8+s9+snext + source_note + '</main>')
out = build_page("pages/15_case_study_html_settlement_batch_delay.html", title=TITLE, description=DESC, body=body)
write_sources()
print("WROTE", out)
