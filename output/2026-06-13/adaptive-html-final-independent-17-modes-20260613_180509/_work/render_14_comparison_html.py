#!/usr/bin/env python3
"""Mode 14 / 17 — comparison_html (sequential). Topic: React 상태관리 비교 (Redux Toolkit vs Zustand vs Jotai).
Layout: comparison-matrix.html (.layout-compare) · auto · vt: comparison-cards(cmp-card) · wg: wg-02.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _finalize import build_page, write_sources, h2, SKILL, ASSETS  # noqa: E402,F401

for _p in [SKILL/"SKILL.md", SKILL/"references/layout-system.md", ASSETS/"layouts/comparison-matrix.html",
           ASSETS/"visual-html-templates/13-comparison-cards.html", ASSETS/"widget-templates/02-visual-design-directions.html"]:
    _p.read_text(encoding="utf-8")

TITLE = "React 상태관리 비교 — Redux Toolkit · Zustand · Jotai"
DESC = "React 상태관리 라이브러리 세 가지(Redux Toolkit, Zustand, Jotai)를 결정 맥락·핵심 매트릭스·상황별 승자·트레이드오프 기준으로 비교하고 팀 상황별 권고를 제시하는 comparison_html."

header = '''
<header class="header compare-header">
  <div class="kicker"><span class="kicker-text">COMPARISON · MODE 14 / 17 · 독립 빌드</span></div>
  <h1>React 상태관리, 무엇을 고를까</h1>
  <p class="sub">Redux Toolkit·Zustand·Jotai를 "유행"이 아니라 "우리 팀의 규모와 문제"에 맞춰 비교한다. 정답은 하나가 아니라 상황별로 갈린다.</p>
  <div class="meta"><span>profile auto</span><span>layout comparison-matrix</span><span>대상 React 개발팀</span><span>무 동작 JS</span></div>
  <div class="generated-row"><p class="generated-date">Generated · 2026-06-13 KST</p>
  <div class="lens-strip" aria-label="적용 렌즈"><span class="lens-strip-label">LENS</span><span class="lens-chip">결정 맥락</span><span class="lens-chip">매트릭스</span><span class="lens-chip">승자</span><span class="lens-chip">트레이드오프</span><span class="lens-chip">권고</span></div></div>
</header>'''

toc = '''
<nav class="toc-map compare-toc" aria-label="비교 목차"><div class="toc-pills">
  <a class="toc-pill" href="#s1"><b>01</b> 무엇을 결정하나</a><a class="toc-pill" href="#s2"><b>02</b> 후보 한눈에</a>
  <a class="toc-pill" href="#s3"><b>03</b> 핵심 비교 매트릭스</a><a class="toc-pill" href="#s4"><b>04</b> 보조 기준표</a>
  <a class="toc-pill" href="#s5"><b>05</b> 상황별 승자</a><a class="toc-pill" href="#s6"><b>06</b> 트레이드오프</a>
  <a class="toc-pill" href="#s7"><b>07</b> 도입 방향</a><a class="toc-pill" href="#s8"><b>08</b> 마이그레이션 비용</a>
  <a class="toc-pill" href="#s9"><b>09</b> 흔한 함정</a><a class="toc-pill" href="#snext"><b>→</b> 최종 권고</a>
</div></nav>'''

s1 = f'''
<section id="s1" class="decision-context summary-card">
  {h2("01","무엇을 결정하나","question")}
  <p class="h2-sub">상태관리 선택은 "어느 게 더 좋은가"가 아니라 "우리 상태의 성격이 무엇인가"의 문제다. 먼저 결정의 맥락을 좁힌다.</p>
  <div class="grid-3">
    <article class="score-card"><h3>상태의 성격</h3><p>서버 캐시(목록·상세)인가, 클라이언트 전역 상태(테마·인증)인가? 서버 상태가 대부분이면 사실 React Query류가 먼저고, 이 비교는 클라이언트 전역 상태에 한정한다.</p></article>
    <article class="score-card"><h3>팀 규모·숙련도</h3><p>대규모·엄격한 규약이 필요한가, 소규모·빠른 생산성이 우선인가? 보일러플레이트 허용도가 선택을 가른다.</p></article>
    <article class="score-card"><h3>디버깅·도구</h3><p>타임트래블·미들웨어·DevTools 의존도가 높은가? 도구 생태계 요구가 크면 후보가 좁혀진다.</p></article>
  </div>
  <p>이 세 축을 먼저 정하지 않으면 어떤 비교표도 무의미하다. "유행하니까 Zustand", "큰 회사니까 Redux" 같은 선택이 6개월 뒤 부채가 되는 이유는, 도구가 아니라 우리 상태의 성격을 안 본 데 있다.</p>
</section>'''

s2 = f'''
<section id="s2" class="summary-card">
  {h2("02","후보 한눈에","compare")}
  <p class="h2-sub">세 후보의 철학을 한 문장으로 요약한다. 각자 "무엇을 단순하게 만들려 했는가"가 다르다.</p>
  <section class="vt-shell" aria-label="상태관리 후보 비교 카드">
    <div class="cmp">
      <article class="cmp-card"><div class="vt-kicker">Redux Toolkit</div><h3>규약 있는 단일 스토어</h3><ul><li>예측 가능한 단방향 흐름</li><li>강력한 DevTools·미들웨어</li><li>보일러플레이트는 RTK로 완화</li></ul></article>
      <article class="cmp-card pick"><div class="vt-kicker">Zustand</div><h3>가벼운 훅 스토어</h3><ul><li>최소 API, 보일러플레이트 거의 없음</li><li>스토어를 자유롭게 분할</li><li>러닝 커브 낮음</li></ul></article>
      <article class="cmp-card"><div class="vt-kicker">Jotai</div><h3>원자(atom) 단위 상태</h3><ul><li>상태를 작은 atom으로 조립</li><li>세밀한 리렌더 제어</li><li>파생 상태가 자연스러움</li></ul></article>
    </div>
  </section>
  <p>핵심 차이는 "단위"다. Redux는 하나의 큰 스토어와 규약을, Zustand는 자유로운 훅 스토어를, Jotai는 잘게 쪼갠 atom을 기본 단위로 삼는다. 이 단위 선택이 코드 구조·리렌더·테스트 방식 전체를 결정한다.</p>
</section>'''

s3 = f'''
<section id="s3" class="matrix summary-card">
  {h2("03","핵심 비교 매트릭스","metric")}
  <p class="h2-sub">가장 자주 묻는 6개 축을 한 표로 모았다. 단일 "승자"는 없고 축마다 강점이 갈린다.</p>
  <div class="table-scroll"><table>
    <caption>상태관리 라이브러리 핵심 비교</caption>
    <thead><tr><th>축</th><th>Redux Toolkit</th><th>Zustand</th><th>Jotai</th></tr></thead>
    <tbody>
      <tr><th>러닝 커브</th><td>중간(개념 다수)</td><td>낮음</td><td>낮음~중간</td></tr>
      <tr><th>보일러플레이트</th><td>중간(RTK로 완화)</td><td>매우 적음</td><td>적음</td></tr>
      <tr><th>리렌더 제어</th><td>selector로 제어</td><td>selector로 제어</td><td>atom 단위 자동</td></tr>
      <tr><th>DevTools</th><td>최상(타임트래블)</td><td>지원(미들웨어)</td><td>지원</td></tr>
      <tr><th>대규모 규약</th><td>강함</td><td>팀 규약 필요</td><td>팀 규약 필요</td></tr>
      <tr><th>번들 크기</th><td>상대적 큼</td><td>매우 작음</td><td>작음</td></tr>
    </tbody>
  </table></div>
  <p>표를 한 줄로 읽으면: Redux는 "규모와 규약", Zustand는 "단순함과 속도", Jotai는 "세밀한 리렌더"가 강점이다. 약점도 그 강점의 그림자다 — Redux는 무겁고, Zustand·Jotai는 규약을 팀이 직접 세워야 한다.</p>
</section>'''

s4 = f'''
<section id="s4" class="summary-card">
  {h2("04","보조 기준표","reference")}
  <p class="h2-sub">핵심 축 외에 도입 시 따져야 할 보조 기준을 표로 압축한다(카드 반복 대신 비교 표).</p>
  <div class="table-scroll"><table class="table criteria-table">
    <caption>도입 보조 기준 — 판단 포인트·유리한 후보·주의점</caption>
    <thead><tr><th>기준</th><th>판단 포인트</th><th>유리한 후보</th><th>주의할 점</th></tr></thead>
    <tbody>
      <tr><th>비동기·서버 상태</th><td>서버 데이터가 대부분인가</td><td>(별도) React Query 병행</td><td>전역 스토어에 서버 캐시를 욱여넣지 말 것</td></tr>
      <tr><th>SSR/Next.js</th><td>서버 렌더 하이드레이션</td><td>Jotai·Zustand(경량)</td><td>스토어 초기화 범위·요청별 격리 확인</td></tr>
      <tr><th>테스트 용이성</th><td>순수 함수 분리</td><td>Redux(리듀서 순수)</td><td>Zustand/Jotai는 스토어 격리 패턴 필요</td></tr>
      <tr><th>팀 온보딩</th><td>신규 인원 적응 속도</td><td>Zustand</td><td>Redux는 개념 학습 비용 선투자</td></tr>
      <tr><th>대규모 협업</th><td>규약·경계 강제</td><td>Redux Toolkit</td><td>경량 도구는 폴더·규약을 직접 합의해야</td></tr>
    </tbody>
  </table></div>
  <p>보조 기준에서 반복되는 메시지는 "서버 상태는 분리하라"이다. 세 라이브러리 모두 클라이언트 전역 상태 도구이며, 서버 데이터 캐싱은 React Query 같은 전용 도구와 병행하는 것이 거의 항상 옳다.</p>
</section>'''

s5 = f'''
<section id="s5" class="winners summary-card">
  {h2("05","상황별 승자","success")}
  <p class="h2-sub">"무조건 1등"은 없다. 우리 상황을 골라 그 줄을 따라가면 된다.</p>
  <div class="grid-3">
    <article class="good"><span class="label">Redux Toolkit</span><p>여러 팀이 한 코드베이스를 만지고, 엄격한 규약·타임트래블 디버깅·미들웨어가 필요한 대규모 앱.</p></article>
    <article class="good"><span class="label">Zustand</span><p>소규모~중간 팀, 빠른 생산성과 낮은 러닝 커브가 우선이고 전역 상태가 비교적 단순한 경우.</p></article>
    <article class="good"><span class="label">Jotai</span><p>상태가 잘게 쪼개지고 파생 상태가 많으며, 리렌더 범위를 세밀하게 제어하고 싶은 경우.</p></article>
  </div>
  <p>경험칙 하나: 의심스러우면 Zustand로 시작하라. 가장 적은 비용으로 도입해 보고, 규약·도구 요구가 커지면 Redux로, 리렌더 세밀함이 필요하면 Jotai로 옮기는 편이, 처음부터 무거운 도구로 시작해 후회하는 것보다 싸다.</p>
</section>'''

s6 = f'''
<section id="s6" class="tradeoffs summary-card">
  {h2("06","트레이드오프","decision")}
  <p class="h2-sub">각 선택이 무엇을 사고 무엇을 파는지 명시한다. 강점과 약점은 동전의 양면이다.</p>
  <div class="grid-3">
    <article class="card-block"><h3>Redux Toolkit</h3><p><strong>산다:</strong> 예측 가능성·도구·대규모 규약. <strong>판다:</strong> 초기 학습 비용·코드량·번들.</p></article>
    <article class="card-block"><h3>Zustand</h3><p><strong>산다:</strong> 단순함·속도·작은 번들. <strong>판다:</strong> 규약을 팀이 직접 세워야 함(자유의 비용).</p></article>
    <article class="card-block"><h3>Jotai</h3><p><strong>산다:</strong> 세밀한 리렌더·조립식 상태. <strong>판다:</strong> atom이 많아지면 추적·구조화 부담.</p></article>
  </div>
  <p>트레이드오프의 핵심 축은 "강제된 규약 vs 자유"다. Redux는 규약을 도구가 강제해 큰 팀의 일관성을 사고, 경량 도구는 자유를 주는 대신 그 일관성을 팀이 직접 책임져야 한다. 팀의 규율 수준이 선택을 좌우한다.</p>
</section>'''

s7 = f'''
<section id="s7" class="summary-card">
  {h2("07","도입 방향 — 어떤 스타일이 맞나","flow")}
  <p class="h2-sub">세 도입 스타일을 카드로 비교하고, 우리 팀 문화에 맞는 방향을 고른다.</p>
  <section class="wg-02-dir" aria-labelledby="m14-wg02-title">
    <header class="wg-02-head"><p class="wg-02-kicker">ADOPTION DIRECTIONS</p><h2 id="m14-wg02-title" class="wg-02-h">상태관리 도입 스타일</h2><p class="wg-02-lead">규약 중심·경량 중심·원자 중심 세 방향을 비교해 팀에 맞춰 선택한다.</p></header>
    <fieldset class="wg-02-grid"><legend class="wg-02-sr">방향 선택</legend>
      <input type="radio" name="m14-dir" id="m14-a" class="wg-02-radio" checked>
      <div class="wg-02-card"><div class="wg-02-preview wg-02-preview--b"><div class="wg-02-pv-bar wg-02-pv-bar--b"><span class="wg-02-pv-dot"></span><span class="wg-02-pv-line"></span></div><div class="wg-02-pv-cards"><span></span><span></span><span></span></div><div class="wg-02-pv-cta wg-02-pv-cta--b">규약</div></div>
        <div class="wg-02-meta"><label for="m14-a" class="wg-02-pick-label">Redux · 규약 중심</label><p class="wg-02-desc">단일 스토어 + 슬라이스 규약. 대규모 협업에서 일관성.</p><ul class="wg-02-palette" aria-label="규약 팔레트"><li style="background:var(--ink)"><span>strict</span></li><li style="background:var(--accent)"><span>tool</span></li><li style="background:var(--bg)"><span>bg</span></li></ul><span class="wg-02-badge">선택됨</span></div></div>
      <input type="radio" name="m14-dir" id="m14-b" class="wg-02-radio">
      <div class="wg-02-card"><div class="wg-02-preview wg-02-preview--a"><div class="wg-02-pv-bar"><span class="wg-02-pv-dot"></span><span class="wg-02-pv-line"></span></div><div class="wg-02-pv-hero">Zustand</div><div class="wg-02-pv-body"><span></span><span></span><span class="wg-02-pv-short"></span></div><div class="wg-02-pv-cta wg-02-pv-cta--a">경량</div></div>
        <div class="wg-02-meta"><label for="m14-b" class="wg-02-pick-label">Zustand · 경량 중심</label><p class="wg-02-desc">훅 스토어 최소 API. 빠른 생산성과 낮은 진입 장벽.</p><ul class="wg-02-palette" aria-label="경량 팔레트"><li style="background:var(--good-accent)"><span>fast</span></li><li style="background:var(--accent)"><span>min</span></li><li style="background:var(--bg)"><span>bg</span></li></ul><span class="wg-02-badge">선택됨</span></div></div>
      <input type="radio" name="m14-dir" id="m14-c" class="wg-02-radio">
      <div class="wg-02-card"><div class="wg-02-preview wg-02-preview--c"><div class="wg-02-pv-bar wg-02-pv-bar--c"><span class="wg-02-pv-dot"></span><span class="wg-02-pv-line"></span></div><div class="wg-02-pv-split"><div class="wg-02-pv-aside"></div><div class="wg-02-pv-main"><span></span><span></span></div></div><div class="wg-02-pv-cta wg-02-pv-cta--c">원자</div></div>
        <div class="wg-02-meta"><label for="m14-c" class="wg-02-pick-label">Jotai · 원자 중심</label><p class="wg-02-desc">atom 조립과 파생 상태. 세밀한 리렌더 제어.</p><ul class="wg-02-palette" aria-label="원자 팔레트"><li style="background:var(--analogy-bg)"><span>atom</span></li><li style="background:var(--analogy-accent)"><span>derive</span></li><li style="background:var(--accent)"><span>fine</span></li></ul><span class="wg-02-badge">선택됨</span></div></div>
    </fieldset>
    <p class="wg-02-foot">라디오 선택으로 방향 카드가 강조됩니다(무 JS 근사). 실제 도입은 PoC로 검증하세요.</p>
  </section>
</section>'''

s8 = f'''
<section id="s8" class="summary-card">
  {h2("08","마이그레이션 비용","timeline")}
  <p class="h2-sub">"바꾸면 끝"이 아니다. 이미 한 도구를 쓰고 있다면 전환 비용을 먼저 따진다.</p>
  <ul class="check-list">
    <li><strong>Redux → Zustand</strong> — 보일러플레이트가 줄지만, 미들웨어·타임트래블에 의존하던 디버깅 흐름을 다시 설계해야 한다.</li>
    <li><strong>무 도구 → 무엇이든</strong> — Context 남용으로 리렌더가 문제라면, 전역 상태를 도구로 옮기되 "정말 전역인 상태"만 추린다.</li>
    <li><strong>점진 전환</strong> — 한 번에 전부 바꾸지 말고, 새 기능부터 새 도구를 쓰고 기존은 그대로 두는 점진 전환이 안전하다.</li>
  </ul>
  <p>가장 비싼 마이그레이션은 "도구만 바꾸고 상태 설계는 그대로" 옮기는 것이다. 전환은 도구 교체가 아니라 "무엇이 진짜 전역 상태인가"를 재검토할 기회로 삼아야 비용이 회수된다. 또한 전환 결정에는 코드 비용뿐 아니라 팀의 학습 비용도 함께 계산해야 한다 — 모두가 익숙한 도구를 떠나는 비용이 새 도구의 이점보다 큰 경우가 의외로 많다.</p>
</section>'''

s9 = f'''
<section id="s9" class="summary-card">
  {h2("09","흔한 함정","warning")}
  <p class="h2-sub">도구 선택과 무관하게 반복되는 실수들. 어떤 라이브러리를 골라도 이건 피해야 한다.</p>
  <div class="card-grid">
    <article class="mini-card"><span class="case-label">치명</span><h3>서버 상태 혼입</h3><p>API 응답 캐시를 전역 스토어에 넣으면, 무효화·재검증을 직접 구현하다 무너진다. 서버 상태는 전용 도구로.</p></article>
    <article class="mini-card"><span class="case-label">경고</span><h3>전부 전역화</h3><p>로컬에서 충분한 상태까지 전역으로 올리면 결합도가 폭증한다. "정말 여러 곳에서 쓰는가"를 먼저 묻는다.</p></article>
    <article class="mini-card"><span class="case-label">경고</span><h3>유행 추종</h3><p>"요즘 다 Zustand 쓴다"는 선택 근거가 아니다. 우리 상태의 성격과 팀 규율이 근거다.</p></article>
  </div>
  <p>세 함정의 공통 교훈은 "도구가 설계를 대신해 주지 않는다"이다. 어떤 라이브러리도 잘못된 상태 경계를 고쳐 주지 않는다. 좋은 선택의 절반은 도구 비교가 아니라 "무엇을 전역으로 둘지"의 설계에 있다.</p>
</section>'''

snext = f'''
<section id="snext" class="try">
  {h2(None,"최종 권고","landing")}
  <p>정답은 팀 상황에 있다. 아래 한 줄 질문으로 빠르게 좁힌 뒤, 작은 PoC로 확정하라.</p>
  <div class="cta-box">
    <p><strong>30초 결정 가이드</strong></p>
    <ol><li>여러 팀·엄격한 규약·타임트래블이 필요하다 → <strong>Redux Toolkit</strong></li><li>작고 빠르게, 러닝 커브 최소 → <strong>Zustand</strong></li><li>상태가 잘게 쪼개지고 파생이 많다 → <strong>Jotai</strong></li><li>그리고 서버 데이터는 셋 중 무엇과도 React Query를 병행</li></ol>
    <div class="tag-list"><span class="tag">comparison_html</span><span class="tag">react</span><span class="tag">state-management</span><span class="tag">의사결정</span></div>
  </div>
</section>'''

source_note = '<aside class="source-note"><p><strong>출처·범위.</strong> 본 비교는 세 라이브러리의 공개 문서와 일반적 사용 경험을 바탕으로 한 의사결정 가이드다. 번들 크기·성능 수치는 버전·번들러·사용 패턴에 따라 달라지므로, 도입 전 자사 환경에서 측정·PoC로 확인한다.</p></aside>'

body = ('<main id="main" class="page-wide layout-compare">' + header + toc + s1+s2+s3+s4+s5+s6+s7+s8+s9+snext + source_note + '</main>')
out = build_page("pages/14_comparison_html_react_state.html", title=TITLE, description=DESC, body=body)
write_sources()
print("WROTE", out)
