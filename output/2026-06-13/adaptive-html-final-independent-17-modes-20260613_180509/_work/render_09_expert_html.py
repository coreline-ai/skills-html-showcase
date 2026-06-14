#!/usr/bin/env python3
"""Mode 09 / 17 — expert_html (sequential). Topic: 멀티리전 결제 시스템 아키텍처 진단.
Layout: expert-report.html (.layout-expert) · auto · vt: risk-matrix(rm-grid) · wg: wg-16(로드맵).
주의: 직접 section에 decision-grid 금지, validation-checklist 안에 wg-03/17 금지.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _finalize import build_page, write_sources, h2, SKILL, ASSETS  # noqa: E402,F401

for _p in [SKILL/"SKILL.md", SKILL/"references/layout-system.md", ASSETS/"layouts/expert-report.html",
           ASSETS/"visual-html-templates/03-risk-matrix.html", ASSETS/"widget-templates/16-implementation-plan.html"]:
    _p.read_text(encoding="utf-8")

TITLE = "멀티리전 결제 시스템 아키텍처 진단 리포트"
DESC = "단일 리전 결제 시스템을 멀티리전으로 확장하기 전, 가용성·정합성·데이터 주권·운영 리스크를 진단하고 RACI·리스크 매트릭스·90일 로드맵·검증 기준을 제시한 expert_html 리포트."

header = '''
<header class="header report-header">
  <div class="kicker"><span class="kicker-text">EXPERT REPORT · MODE 09 / 17 · 독립 빌드</span></div>
  <h1>멀티리전 결제 시스템 아키텍처 진단</h1>
  <p class="sub">단일 리전에서 안정적으로 동작하는 결제 시스템을 멀티리전으로 확장하기 전, 무엇이 깨질 수 있고 무엇을 먼저 결정해야 하는지를 의사결정 가능한 형태로 정리한다.</p>
  <div class="meta"><span>profile auto</span><span>layout expert-report</span><span>대상 결제플랫폼 리드·아키텍트</span><span>진단 기준 2026-06-13</span></div>
  <div class="generated-row"><p class="generated-date">Generated · 2026-06-13 KST</p>
  <div class="lens-strip" aria-label="적용 렌즈"><span class="lens-strip-label">LENS</span><span class="lens-chip">가용성</span><span class="lens-chip">정합성</span><span class="lens-chip">데이터 주권</span><span class="lens-chip">운영</span><span class="lens-chip">비용</span></div></div>
</header>'''

toc = '''
<nav class="toc-map expert-toc" aria-label="리포트 목차"><div class="toc-pills">
  <a class="toc-pill" href="#s1"><b>01</b> 핵심 결론</a><a class="toc-pill" href="#s2"><b>02</b> 의사결정 카드</a>
  <a class="toc-pill" href="#s3"><b>03</b> 아키텍처 현황</a><a class="toc-pill" href="#s4"><b>04</b> 운영 모델·RACI</a>
  <a class="toc-pill" href="#s5"><b>05</b> 리스크 매트릭스</a><a class="toc-pill" href="#s6"><b>06</b> SLO·관측 지표</a>
  <a class="toc-pill" href="#s7"><b>07</b> 90일 도입 로드맵</a><a class="toc-pill" href="#s8"><b>08</b> 트레이드오프</a>
  <a class="toc-pill" href="#s9"><b>09</b> 검증 기준</a><a class="toc-pill" href="#s10"><b>10</b> 리전·비용 고려</a>
  <a class="toc-pill" href="#snext"><b>→</b> 최종 권고</a>
</div></nav>'''

s1 = f'''
<section id="s1" class="executive-summary summary-card">
  {h2("01","핵심 결론","audit")}
  <p class="h2-sub">결론: <strong>액티브-패시브로 시작</strong>하라. 멀티리전의 진짜 비용은 인프라가 아니라 "데이터 정합성과 운영 복잡도"이며, 결제 도메인에서는 이 둘이 직접 사고로 이어진다.</p>
  <div class="grid-3">
    <article class="score-card"><h3>지금 상태</h3><p>단일 리전 액티브 구성. 가용성은 충분하나, 리전 장애 시 전체 결제가 중단되는 단일 실패 지점이 존재한다.</p></article>
    <article class="score-card"><h3>핵심 위험</h3><p>멀티리전 액티브-액티브로 직행하면 결제 정합성(이중 승인·중복 정산) 위험이 급증한다. CAP 트레이드오프를 결제 도메인에 맞게 결정해야 한다.</p></article>
    <article class="score-card"><h3>권고 방향</h3><p>1단계 액티브-패시브(읽기 복제 + 빠른 승격)로 가용성을 확보하고, 정합성 설계가 검증된 뒤에만 액티브-액티브를 검토한다.</p></article>
  </div>
  <p>핵심 표(아래 RACI·리스크·로드맵)는 모두 이 결론을 뒷받침한다. "리전을 늘리는 일"이 아니라 "정합성을 어디까지 양보할지 결정하는 일"이 이 프로젝트의 본질이다. 경영진에게 보고할 한 줄은 이렇게 잡는다 — "가용성은 1단계로 빠르게 올리되, 정합성을 파는 거래는 검증 게이트를 통과하기 전까지 하지 않는다."</p>
</section>'''

s2 = f'''
<section id="s2" class="decision-section summary-card">
  {h2("02","의사결정 카드","decision")}
  <p class="h2-sub">먼저 답해야 할 세 가지 결정. 이 답이 정해지지 않으면 아키텍처 선택이 표류한다.</p>
  <div class="grid-3">
    <article class="card-block"><h3>D1 · 토폴로지</h3><p>액티브-패시브 vs 액티브-액티브. <strong>권고: 패시브 우선.</strong> 결제는 정합성이 가용성보다 비싼 도메인이다.</p></article>
    <article class="card-block"><h3>D2 · 데이터 정합성</h3><p>동기 복제(지연↑, 정합성↑) vs 비동기(지연↓, 정합성 위험). <strong>권고: 승인 경로는 동기, 분석은 비동기.</strong></p></article>
    <article class="card-block"><h3>D3 · 장애 전환</h3><p>수동 승격 vs 자동 페일오버. <strong>권고: 초기엔 사람이 버튼을 누르는 반자동.</strong> 자동 분할뇌(split-brain)가 더 위험하다.</p></article>
  </div>
  <p>세 결정은 서로 묶여 있다. 액티브-패시브 + 승인 동기복제 + 반자동 승격이 한 묶음으로 가장 보수적이고 안전한 출발선이다. 더 공격적인 선택은 정합성 검증 이후로 미룬다.</p>
</section>'''

s3 = f'''
<section id="s3" class="architecture-map summary-card">
  {h2("03","아키텍처 현황과 목표","flow")}
  <p class="h2-sub">현재에서 목표로 가는 경로를 단계로 본다. 한 번에 점프하지 않는 것이 핵심이다.</p>
  <section class="vt-shell" aria-label="아키텍처 전환 단계">
    <div class="vt-frame"><ol class="tl">
      <li class="tl-item"><b>현재</b><p class="vt-text">단일 리전 액티브. 동기 DB, 단일 장애 지점.</p></li>
      <li class="tl-item"><b>1단계</b><p class="vt-text">보조 리전에 읽기 복제 + 비상 승격 절차 + 정기 페일오버 훈련.</p></li>
      <li class="tl-item"><b>2단계</b><p class="vt-text">승인 경로 동기 복제 강화, 멱등 키 기반 중복 차단 도입.</p></li>
      <li class="tl-item"><b>3단계</b><p class="vt-text">정합성 검증 완료 후에만 부분 액티브-액티브(리전 분할 라우팅) 검토.</p></li>
    </ol></div>
  </section>
  <p>이 경로의 미덕은 "각 단계가 독립적으로 가치를 준다"는 점이다. 1단계만으로도 리전 장애 시 복구 가능성이 생기고, 이후 단계는 정합성 자신감이 쌓인 만큼만 진행한다. 반대로 가장 위험한 안티패턴은 "이왕 하는 김에" 한 분기에 액티브-액티브까지 점프하는 것이다. 결제 정합성 설계가 검증되지 않은 상태에서 두 리전이 동시에 쓰기를 받으면, 평소엔 멀쩡하다가 네트워크 분단 순간 이중 승인이 터진다. 그래서 단계 사이에는 반드시 "정합성 게이트를 통과했는가"라는 질문을 둔다.</p>
</section>'''

s4 = f'''
<section id="s4" class="summary-card">
  {h2("04","운영 모델 · RACI","user")}
  <p class="h2-sub">멀티리전은 기술보다 운영이 어렵다. 누가 무엇에 책임지는지를 먼저 못 박는다(핵심 표, 6행).</p>
  <div class="table-scroll"><table>
    <caption>멀티리전 운영 RACI</caption>
    <thead><tr><th>활동</th><th>결제플랫폼</th><th>SRE</th><th>DBA</th><th>보안/법무</th></tr></thead>
    <tbody>
      <tr><th>토폴로지 결정</th><td>A</td><td>C</td><td>C</td><td>I</td></tr>
      <tr><th>복제 구성</th><td>C</td><td>R</td><td>A</td><td>I</td></tr>
      <tr><th>페일오버 실행</th><td>A</td><td>R</td><td>C</td><td>I</td></tr>
      <tr><th>정합성 검증</th><td>R</td><td>C</td><td>A</td><td>I</td></tr>
      <tr><th>데이터 주권 준수</th><td>C</td><td>I</td><td>C</td><td>A</td></tr>
      <tr><th>장애 사후분석</th><td>A</td><td>R</td><td>R</td><td>C</td></tr>
    </tbody>
  </table></div>
  <p>가장 흔한 실패는 "페일오버는 SRE 일이겠지"라는 공백이다. 결제 도메인 판단(중복 정산 허용 여부 등)은 결제플랫폼이 Accountable이어야 하며, 데이터 주권은 보안/법무가 막판이 아니라 설계 단계에 들어와야 한다.</p>
</section>'''

s5 = f'''
<section id="s5" class="risk-matrix summary-card">
  {h2("05","리스크 매트릭스","warning")}
  <p class="h2-sub">가능성×영향으로 정렬한다. 우상단(높음·큼)이 설계의 1순위 방어 대상이다.</p>
  <section class="vt-shell" aria-label="멀티리전 리스크 매트릭스">
    <div class="vt-frame"><div class="rm-grid">
      <div class="rm-cell rm-head">가능성</div><div class="rm-cell rm-head">낮음</div><div class="rm-cell rm-head">중간</div><div class="rm-cell rm-head">높음</div>
      <div class="rm-cell rm-head">영향 큼</div><div class="rm-cell rm-risk med">데이터 주권 위반</div><div class="rm-cell rm-risk high">이중 승인·중복 정산</div><div class="rm-cell rm-risk high">스플릿브레인</div>
      <div class="rm-cell rm-head">영향 중간</div><div class="rm-cell rm-risk low">복제 지연 노출</div><div class="rm-cell rm-risk med">페일오버 지연</div><div class="rm-cell rm-risk med">운영 복잡도 폭증</div>
      <div class="rm-cell rm-head">영향 작음</div><div class="rm-cell rm-risk low">대시보드 혼선</div><div class="rm-cell rm-risk low">비용 추정 오차</div><div class="rm-cell rm-risk low">문서 노후</div>
    </div></div>
  </section>
  <p>최우선 방어 4건: ① 이중 승인/중복 정산(멱등 키), ② 스플릿브레인(반자동 승격 + 펜싱), ③ 데이터 주권(리전 고정 저장), ④ 운영 복잡도(런북·훈련). 나머지는 모니터링으로 관리한다.</p>
</section>'''

s6 = f'''
<section id="s6" class="summary-card">
  {h2("06","SLO · 관측 지표","metric")}
  <p class="h2-sub">멀티리전 전환의 성패는 숫자로 판정한다. 전환 전후 같은 지표를 본다.</p>
  <div class="table-scroll"><table>
    <caption>핵심 SLO와 관측 지표</caption>
    <thead><tr><th>지표</th><th>현재</th><th>목표</th><th>경보 임계</th></tr></thead>
    <tbody>
      <tr><th>승인 성공률</th><td>99.95%</td><td>≥99.97%</td><td>5분 99.9% 미만</td></tr>
      <tr><th>승인 p99 지연</th><td>320ms</td><td>≤450ms(동기복제 감안)</td><td>p99 800ms 초과</td></tr>
      <tr><th>복제 지연</th><td>해당없음</td><td>≤1s(승인 경로)</td><td>5s 초과</td></tr>
      <tr><th>RTO(복구목표)</th><td>해당없음</td><td>≤10분</td><td>훈련 미달 시</td></tr>
      <tr><th>중복 정산 건</th><td>0</td><td>0(불변)</td><td>1건도 즉시</td></tr>
    </tbody>
  </table></div>
  <p>주목할 점은 "지연 목표를 의도적으로 완화"했다는 것이다. 동기 복제는 지연을 늘린다 — 그 대가로 정합성을 산다. 중복 정산은 단 1건도 허용하지 않는 불변 지표로 둔다.</p>
</section>'''

s7 = f'''
<section id="s7" class="priority-roadmap summary-card">
  {h2("07","90일 도입 로드맵","timeline")}
  <p class="h2-sub">마일스톤·데이터 플로우·리스크를 한 팩으로 본다. 단계마다 검증 게이트를 둔다.</p>
  <section class="wg-16" aria-labelledby="m09-wg16-title">
    <header class="wg-16-head"><p class="wg-16-kicker">도입 계획 · MR-09</p><h2 id="m09-wg16-title" class="wg-16-h">멀티리전 결제 확장</h2><p class="wg-16-lead">액티브-패시브로 시작해 <strong>정합성 검증을 게이트</strong>로 두고 90일 안에 1차 가용성을 확보합니다.</p></header>
    <div class="wg-16-panel">
      <h3 class="wg-16-h3">마일스톤 타임라인</h3>
      <ol class="wg-16-ms">
        <li class="wg-16-ms-item wg-16-done"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">M0 · 결정 합의</span><span class="wg-16-badge wg-16-bd-done">완료</span></div><p class="wg-16-ms-desc">토폴로지·정합성·페일오버 3대 결정 합의. ~D0.</p></div></li>
        <li class="wg-16-ms-item wg-16-active"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">M1 · 읽기 복제·승격 절차 (0~30일)</span><span class="wg-16-badge wg-16-bd-active">진행 중</span></div><p class="wg-16-ms-desc">보조 리전 복제 + 비상 승격 런북 + 첫 페일오버 훈련.</p></div></li>
        <li class="wg-16-ms-item"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">M2 · 정합성 강화 (31~60일)</span><span class="wg-16-badge">예정</span></div><p class="wg-16-ms-desc">승인 경로 동기복제 + 멱등 키 중복 차단 + 부하 검증.</p></div></li>
        <li class="wg-16-ms-item"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">M3 · 게임데이·정착 (61~90일)</span><span class="wg-16-badge">예정</span></div><p class="wg-16-ms-desc">월간 리전 장애 훈련, RTO 측정, 운영 인계.</p></div></li>
      </ol>
      <h3 class="wg-16-h3">데이터 플로우</h3>
      <div class="wg-16-flow" aria-label="결제 데이터 플로우">
        <div class="wg-16-fnode">클라이언트<span class="wg-16-fnode-s">승인 요청</span></div>
        <div class="wg-16-fnode wg-16-fnode-good">주 리전<span class="wg-16-fnode-s">동기 처리</span></div>
        <div class="wg-16-fnode wg-16-fnode-hot">동기 복제<span class="wg-16-fnode-s">승인 원장</span></div>
        <div class="wg-16-fnode">보조 리전<span class="wg-16-fnode-s">대기·승격</span></div>
        <div class="wg-16-fnode wg-16-fnode-q">정합성 게이트<span class="wg-16-fnode-s">멱등·검증</span></div>
      </div>
    </div>
  </section>
</section>'''

s8 = f'''
<section id="s8" class="summary-card">
  {h2("08","트레이드오프","compare")}
  <p class="h2-sub">"공짜 점심은 없다." 각 선택이 무엇을 사고 무엇을 파는지 명시한다.</p>
  <div class="grid-2">
    <article class="card-block"><h3>액티브-패시브</h3><p><strong>산다:</strong> 단순함·정합성·낮은 사고 위험. <strong>판다:</strong> 보조 리전 자원이 평시 유휴, 페일오버 동안 짧은 중단.</p></article>
    <article class="card-block"><h3>액티브-액티브</h3><p><strong>산다:</strong> 자원 활용·지연 최적화. <strong>판다:</strong> 정합성 설계 난이도 폭증, 중복 정산 위험.</p></article>
    <article class="card-block"><h3>동기 복제</h3><p><strong>산다:</strong> 데이터 손실 제로. <strong>판다:</strong> 쓰기 지연 증가, 리전 간 네트워크에 민감.</p></article>
    <article class="card-block"><h3>자동 페일오버</h3><p><strong>산다:</strong> 빠른 복구. <strong>판다:</strong> 오판 시 스플릿브레인 — 결제에선 치명적.</p></article>
  </div>
  <p>결제 도메인의 트레이드오프 원칙은 분명하다. <strong>가용성을 위해 정합성을 파는 거래는 하지 않는다.</strong> 그래서 자원 효율(액티브-액티브)보다 안전(액티브-패시브)을 먼저 산다. 이 원칙을 한 문장으로 팀에 공유해 두면, 이후 모든 세부 선택에서 길게 토론하지 않고 같은 기준으로 빠르게 정렬할 수 있다.</p>
</section>'''

s9 = f'''
<section id="s9" class="validation-checklist summary-card">
  {h2("09","검증 기준","check")}
  <p class="h2-sub">완료를 선언하려면 아래 4가지 증빙이 있어야 한다. 코드 리뷰나 릴리스 노트가 아니라 운영 증빙이다.</p>
  <ul class="check-list">
    <li><strong>페일오버 훈련 통과</strong> — 주 리전 강제 중단 후 RTO ≤10분으로 승격 성공(증빙: 훈련 로그·타임스탬프).</li>
    <li><strong>중복 차단 검증</strong> — 동일 멱등 키 중복 요청 부하 테스트에서 중복 정산 0건(증빙: 테스트 리포트).</li>
    <li><strong>복제 지연 SLO</strong> — 승인 경로 복제 지연 p99 ≤1s 유지(증빙: 대시보드 7일 추이).</li>
    <li><strong>데이터 주권</strong> — 리전별 저장 위치가 정책과 일치(증빙: 저장소 구성 감사).</li>
  </ul>
  <p>네 증빙이 모두 녹색이 되기 전에는 액티브-액티브로 진행하지 않는다. 검증은 "한 번 통과"가 아니라 "지속 유지"여야 하므로, 게임데이를 월간 정례로 둔다.</p>
</section>'''

s10 = f'''
<section id="s10" class="summary-card">
  {h2("10","리전·비용 고려","database")}
  <p class="h2-sub">기술 결정이 끝나면 리전 선택과 비용이 남는다. 데이터 주권이 비용보다 먼저다.</p>
  <div class="card-grid">
    <article class="mini-card"><h3>리전 선택</h3><p>주 사용자 지역 + 데이터 주권 요건을 만족하는 보조 리전. 법적 제약이 후보를 먼저 좁힌다.</p></article>
    <article class="mini-card"><h3>비용 구조</h3><p>유휴 보조 리전 자원 + 리전 간 네트워크 + 복제 트래픽. 액티브-패시브는 자원 효율은 낮지만 위험 비용이 낮다.</p></article>
    <article class="mini-card"><h3>비용 vs 위험</h3><p>"유휴 자원이 아깝다"는 이유로 액티브-액티브를 택하면, 정합성 사고 1건의 비용이 절감액을 초과할 수 있다.</p></article>
  </div>
  <p>비용 최적화는 가용성·정합성이 검증된 뒤의 문제다. 초기에는 "조금 비싸지만 안전한" 구성을 택하고, 운영 자신감이 쌓이면 자원 효율을 단계적으로 높인다. 또한 비용 추정에는 자주 빠지는 항목이 있다 — 리전 간 데이터 전송료와 복제 트래픽은 평시에는 작아 보여도 트래픽이 커지면 무시할 수 없게 누적된다. 도입 전 이 두 항목을 별도 라인으로 추정에 넣고, 분기마다 실측과 대조해 추정 오차를 줄여 나가는 것을 권한다.</p>
</section>'''

snext = f'''
<section id="snext" class="try">
  {h2(None,"최종 권고","landing")}
  <p>멀티리전은 "리전을 늘리는 프로젝트"가 아니라 "정합성을 어디까지 지킬지 결정하는 프로젝트"다. 보수적으로 시작해 증빙을 쌓아 가는 것이 결제 도메인의 정답이다.</p>
  <div class="cta-box">
    <p><strong>즉시 착수 3건</strong></p>
    <ol><li>D1~D3 결정을 문서로 확정하고 RACI 합의.</li><li>보조 리전 읽기 복제 + 비상 승격 런북 작성, 첫 페일오버 훈련 일정 확정.</li><li>중복 정산 0 검증을 위한 멱등 키 설계 착수.</li></ol>
    <div class="tag-list"><span class="tag">expert_html</span><span class="tag">multi-region</span><span class="tag">payments</span><span class="tag">active-passive</span></div>
  </div>
</section>'''

source_note = '<aside class="source-note"><p><strong>출처·범위.</strong> 본 진단은 일반적 멀티리전 결제 아키텍처 원칙(CAP 트레이드오프, 멱등성, 페일오버)을 바탕으로 한 의사결정 리포트다. SLO 수치·일정은 판단을 돕기 위한 기준선이며, 실제 도입 시 자사 트래픽·규제·클라우드 SLA로 재산정해야 한다.</p></aside>'

body = ('<main id="main" class="page-wide layout-expert">' + header + toc + s1+s2+s3+s4+s5+s6+s7+s8+s9+s10+snext + source_note + '</main>')
out = build_page("pages/09_expert_html_multiregion_payments.html", title=TITLE, description=DESC, body=body)
write_sources()
print("WROTE", out)
