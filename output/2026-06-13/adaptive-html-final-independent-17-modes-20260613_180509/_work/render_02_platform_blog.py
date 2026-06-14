#!/usr/bin/env python3
"""Mode 02 / 17 — platform_blog (independent build, sequential).
Topic: "온콜(On-call) 알림 정책을 개편해 새벽 호출을 줄인 경험"을 플랫폼별 블로그로 변환.
Layout: platform-adaptation.html (.layout-platform) · auto · vt: card-grid(cg-grid) · wg: wg-02
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _finalize import build_page, write_sources, h2, SKILL, ASSETS  # noqa: E402,F401

for _p in [SKILL/"SKILL.md", SKILL/"references/platform-system.md", ASSETS/"layouts/platform-adaptation.html",
           ASSETS/"visual-html-templates/07-card-grid.html", ASSETS/"widget-templates/02-visual-design-directions.html"]:
    _p.read_text(encoding="utf-8")

TITLE = "온콜 알림 정책 개편기 — 플랫폼별 발행 전략"
DESC = "새벽 호출을 줄인 온콜 알림 정책 개편 경험 하나를 티스토리·벨로그·브런치·링크드인 네 플랫폼의 독자와 포맷에 맞게 변환하는 platform_blog 모드 대시보드."

header = '''
<header class="header platform-header">
  <div class="kicker"><span class="kicker-text">PLATFORM BLOG · MODE 02 / 17 · 독립 빌드</span></div>
  <h1>온콜 알림 정책 개편기, 네 플랫폼으로</h1>
  <p class="sub">"새벽 3시 호출을 절반으로 줄인 알림 정책 개편" 경험 하나를 티스토리·벨로그·브런치·링크드인의 독자·포맷·말투에 맞게 변환한다. 사실은 그대로, 전달은 플랫폼별로.</p>
  <div class="meta"><span>profile auto</span><span>layout platform-adaptation</span><span>원문 1편 → 4채널</span><span>무 동작 JS</span></div>
  <div class="generated-row"><p class="generated-date">Generated · 2026-06-13 KST</p>
  <div class="lens-strip" aria-label="적용 렌즈"><span class="lens-strip-label">LENS</span><span class="lens-chip">독자 정렬</span><span class="lens-chip">포맷 변환</span><span class="lens-chip">말투</span><span class="lens-chip">SEO/해시태그</span><span class="lens-chip">사실 보존</span></div></div>
</header>'''

toc = '''
<nav class="toc-map platform-toc" aria-label="변환 목차"><div class="toc-pills">
  <a class="toc-pill" href="#s1"><b>01</b> 원문 한 장 요약</a><a class="toc-pill" href="#s2"><b>02</b> 변환 원칙</a>
  <a class="toc-pill" href="#s3"><b>03</b> 플랫폼 지형</a><a class="toc-pill" href="#s4"><b>04</b> 변환 전략</a>
  <a class="toc-pill" href="#s5"><b>05</b> 플랫폼별 결과</a><a class="toc-pill" href="#s6"><b>06</b> 플랫폼 비교표</a>
  <a class="toc-pill" href="#s7"><b>07</b> 제목·도입부 변주</a><a class="toc-pill" href="#s8"><b>08</b> 비주얼·포맷 방향</a>
  <a class="toc-pill" href="#s9"><b>09</b> 해시태그·길이 가이드</a><a class="toc-pill" href="#s10"><b>10</b> 발행 체크리스트</a>
  <a class="toc-pill" href="#snext"><b>→</b> 발행 순서·다음 행동</a>
</div></nav>'''

s1 = f'''
<section id="s1" class="original-summary summary-card">
  {h2("01","원문 한 장 요약","source")}
  <p class="h2-sub">원문은 사내 기술 블로그에 올린 회고다. 무엇을 바꿨고 무엇이 나아졌는지가 핵심이며, 플랫폼 변환에서도 이 사실은 변하지 않는다.</p>
  <div class="grid-3">
    <article class="score-card"><h3>문제</h3><p>온콜 담당자가 주당 평균 11회 새벽 호출을 받았고, 그 중 60%가 자동 복구 가능한 일시적 경보였다. 피로 누적으로 이직 신호가 보였다.</p></article>
    <article class="score-card"><h3>개편</h3><p>경보를 심각도 3단계로 재분류하고, 자동 복구 가능한 경보는 5분 억제(suppression) 후 미해소 시에만 호출하도록 정책을 바꿨다.</p></article>
    <article class="score-card"><h3>결과</h3><p>4주 뒤 새벽 호출이 주당 11회에서 5회로 줄었고, 거짓 경보 비율이 60%에서 22%로 감소했다. 정량 수치는 사내 대시보드 기준이다.</p></article>
  </div>
  <p>이 글의 가치는 "정책을 어떻게 설계하고, 무엇을 측정했고, 어디서 반발이 있었는가"에 있다. 플랫폼마다 강조점은 달라져도 이 뼈대는 공유한다.</p>
</section>'''

s2 = f'''
<section id="s2" class="summary-card">
  {h2("02","변환 원칙 — 무엇을 지키고 무엇을 바꾸나","idea")}
  <p class="h2-sub">변환은 표절이 아니라 재편집이다. 사실·수치·시간순은 고정하고, 길이·말투·도입부·강조점만 채널에 맞춘다.</p>
  <div class="good"><span class="label">지킨다</span><p>핵심 수치(11→5회, 60→22%), 정책의 3단계 분류, 측정 지표, 반발과 합의 과정. 이 사실들은 어느 플랫폼에서도 동일하게 유지한다.</p></div>
  <div class="danger"><span class="label">바꾼다</span><p>제목 후킹, 도입부 길이, 코드/대시보드 노출 정도, 결론의 호출(CTA). 플랫폼 독자가 기대하는 리듬에 맞춰 재배치한다. 없는 사실을 만들어 채우지 않는다.</p></div>
  <p>이 원칙을 어기는 가장 흔한 방식은 "강조점을 바꾸려다 사실까지 비트는 것"이다. 예를 들어 링크드인 버전에서 임팩트를 키우려고 55% 감소를 70%로 반올림하면, 같은 사건을 다룬 티스토리 글과 충돌해 신뢰가 무너진다. 변환의 자유는 형식에만 허용되고 숫자·인과·시간순에는 허용되지 않는다. 그래서 변환 작업표의 맨 위 칸은 항상 "고정 사실 목록"이고, 나머지 칸이 그 아래에서만 움직인다.</p>
</section>'''

s3 = f'''
<section id="s3" class="summary-card">
  {h2("03","플랫폼 지형 — 어디에 무엇을 둘까","compare")}
  <p class="h2-sub">네 플랫폼은 독자와 검색 경로가 다르다. 같은 글을 그대로 올리면 어디서도 최적이 아니다.</p>
  <section class="vt-shell" aria-label="플랫폼별 배치 지형">
    <div class="vt-frame"><div class="cg-grid">
      <article class="cg-card"><em>01</em><b>티스토리</b><p>검색 유입 · 정리글</p></article>
      <article class="cg-card"><em>02</em><b>벨로그</b><p>개발자 · 회고체</p></article>
      <article class="cg-card"><em>03</em><b>브런치</b><p>에세이 · 서사</p></article>
      <article class="cg-card"><em>04</em><b>링크드인</b><p>의사결정자 · 요약</p></article>
      <article class="cg-card"><em>05</em><b>공통</b><p>사실·수치 고정</p></article>
      <article class="cg-card"><em>06</em><b>차별</b><p>도입부·길이·CTA</p></article>
    </div></div>
  </section>
  <p>티스토리는 검색 의도를 만족시키는 구조적 정리글, 벨로그는 동료 개발자와 나누는 솔직한 회고, 브런치는 사람과 번아웃을 다루는 서사, 링크드인은 결정권자를 위한 결과 요약이 맞는다. 같은 사실이라도 독자가 기대하는 형태가 다르므로, 채널을 고르는 순간 강조점도 함께 정해진다.</p>
</section>'''

s4 = f'''
<section id="s4" class="platform-strategy summary-card">
  {h2("04","변환 전략 — 원문 한 덩어리를 채널로 분기","flow")}
  <p class="h2-sub">원문의 앵커(고정 사실)를 가운데 두고, 각 채널로 가는 변환 경로를 분리한다.</p>
  <div class="platform-split">
    <div class="platform-anchor"><h3>고정 앵커</h3><ul><li>11→5회 / 60→22%</li><li>심각도 3단계 분류</li><li>5분 억제 후 호출</li><li>4주 측정 창</li></ul></div>
    <div class="platform-route-grid">
      <div class="platform-anchor"><h3>티스토리 경로</h3><p>검색 키워드("온콜 알림 정책")를 제목·소제목에 배치하고 절차를 단계화한다.</p></div>
      <div class="platform-anchor"><h3>벨로그 경로</h3><p>코드/설정 스니펫과 시행착오를 노출하고 동료 톤으로 쓴다.</p></div>
      <div class="platform-anchor"><h3>브런치 경로</h3><p>새벽 호출을 받던 사람의 장면으로 열고 감정선을 따라간다.</p></div>
      <div class="platform-anchor"><h3>링크드인 경로</h3><p>결과 수치를 먼저 던지고 의사결정 포인트로 압축한다.</p></div>
    </div>
  </div>
  <p>앵커를 가운데 고정해 두면 네 경로가 갈라져도 사실이 어긋나지 않는다. 변환 작업은 늘 "앵커 확인 → 채널 경로 선택 → 도입부·길이 조정" 순서로 진행한다.</p>
</section>'''

s5 = f'''
<section id="s5" class="summary-card">
  {h2("05","플랫폼별 결과 카드","platform")}
  <p class="h2-sub">같은 사실에서 출발한 네 버전의 첫 문단·구성을 나란히 둔다.</p>
  <div class="platform-output-grid">
    <article class="platform-output-card"><h3>티스토리</h3><p><strong>제목:</strong> 온콜 새벽 호출을 절반으로 — 알림 정책 3단계 재설계 기록</p><p>도입부는 "왜 새벽 호출이 많았나"를 검색 의도에 맞춰 진단하고, 본문은 분류 기준→억제 규칙→측정 순으로 단계화한다. 코드보다 표와 절차 중심.</p></article>
    <article class="platform-output-card"><h3>벨로그</h3><p><strong>제목:</strong> 알림을 줄였더니 사람이 남았다 — 온콜 정책 회고</p><p>설정 변경 diff와 "처음엔 억제 시간을 10분으로 잡았다가 SLA를 넘겨 5분으로 줄인" 시행착오를 솔직하게 노출한다. 동료 개발자 대상 반말톤.</p></article>
    <article class="platform-output-card"><h3>브런치</h3><p><strong>제목:</strong> 새벽 3시의 진동, 그리고 우리가 바꾼 것</p><p>호출 진동에 깨던 담당자의 장면으로 연다. 정책은 배경으로 두고, 피로와 회복, 팀의 합의 과정을 서사로 풀어낸다.</p></article>
    <article class="platform-output-card"><h3>링크드인</h3><p><strong>제목:</strong> On-call 새벽 호출 55% 감소: 우리가 바꾼 3가지</p><p>첫 줄에 결과 수치. 이어 3개 의사결정(분류·억제·측정)만 불릿으로. 채용·운영 관점의 시사점으로 닫는다.</p></article>
  </div>
  <p>네 카드는 같은 타임라인을 공유하지만 진입 문장이 다르다. 티스토리·벨로그는 "어떻게 했는가"를 절차와 코드로 풀고, 브런치·링크드인은 "그래서 무엇이 달라졌는가"를 사람과 결과로 먼저 말한다. 변환 시 가장 흔한 실수는 네 버전이 결국 같은 도입부로 수렴하는 것이다. 첫 문단만큼은 채널마다 의도적으로 다르게 써야 복붙이 아닌 재편집이 된다.</p>
</section>'''

s6 = f'''
<section id="s6" class="platform-comparison-table summary-card">
  {h2("06","플랫폼 비교표","metric")}
  <p class="h2-sub">길이·말투·도입부·핵심 CTA를 한눈에 비교해 발행 전 의사결정을 빠르게 한다.</p>
  <div class="table-scroll"><table>
    <caption>플랫폼별 변환 사양 비교</caption>
    <thead><tr><th>플랫폼</th><th>독자</th><th>분량</th><th>도입부</th><th>핵심 CTA</th></tr></thead>
    <tbody>
      <tr><th>티스토리</th><td>검색 유입</td><td>2,500~3,500자</td><td>문제 진단형</td><td>관련 글 더 읽기</td></tr>
      <tr><th>벨로그</th><td>동료 개발자</td><td>1,800~2,600자</td><td>코드/시행착오</td><td>설정 저장소 링크</td></tr>
      <tr><th>브런치</th><td>일반 독자</td><td>1,500~2,200자</td><td>장면 묘사</td><td>구독</td></tr>
      <tr><th>링크드인</th><td>의사결정자</td><td>600~900자</td><td>결과 수치</td><td>의견 댓글 유도</td></tr>
    </tbody>
  </table></div>
  <p>분량이 가장 큰 변수다. 링크드인은 600자대에서 결론부터, 티스토리는 검색 만족을 위해 절차를 풀어 쓴다. 같은 사실을 다른 밀도로 담는 셈이다.</p>
</section>'''

s7 = f'''
<section id="s7" class="summary-card">
  {h2("07","제목·도입부 변주","edit")}
  <p class="h2-sub">하나의 사실에서 네 개의 진입점이 나온다. Before(원문)와 After(채널 변주)를 대조한다.</p>
  <div class="ba">
    <div class="ba-col ba-before"><p class="ba-label">Before — 원문 제목/도입</p><ul><li>"온콜 알림 정책 개편 회고"</li><li>도입: 배경 설명부터 시작</li><li>수치는 본문 중반</li></ul></div>
    <div class="ba-arrow" aria-hidden="true">→</div>
    <div class="ba-col ba-after"><p class="ba-label">After — 채널 변주</p><ul><li>티스토리: 키워드 선행 제목</li><li>브런치: 장면 도입</li><li>링크드인: 수치 선행 첫 줄</li></ul></div>
  </div>
  <p>도입부 한 문단이 체류시간을 좌우한다. 검색·피드·구독 등 진입 맥락이 다르므로, 첫 3초에 보여줄 것을 채널마다 다르게 고른다. 같은 글을 네 번 복붙하지 않으려면 바로 이 첫 문단을 채널 수만큼 새로 쓰는 수고를 들여야 한다.</p>
</section>'''

s8 = f'''
<section id="s8" class="summary-card">
  {h2("08","비주얼·포맷 방향","experiment")}
  <p class="h2-sub">채널별로 어울리는 비주얼 방향이 다르다. 세 방향을 카드로 비교하고 글마다 하나를 고른다.</p>
  <section class="wg-02-dir" aria-labelledby="m02-wg02-title">
    <header class="wg-02-head"><p class="wg-02-kicker">FORMAT DIRECTIONS</p><h2 id="m02-wg02-title" class="wg-02-h">플랫폼별 비주얼 방향</h2><p class="wg-02-lead">에디토리얼·대시보드·소프트 세 방향을 비교해 채널에 맞춰 선택한다.</p></header>
    <fieldset class="wg-02-grid"><legend class="wg-02-sr">방향 선택</legend>
      <input type="radio" name="m02-fmt" id="m02-a" class="wg-02-radio" checked>
      <div class="wg-02-card"><div class="wg-02-preview wg-02-preview--a"><div class="wg-02-pv-bar"><span class="wg-02-pv-dot"></span><span class="wg-02-pv-line"></span></div><div class="wg-02-pv-hero">Editorial</div><div class="wg-02-pv-body"><span></span><span></span><span class="wg-02-pv-short"></span></div><div class="wg-02-pv-cta wg-02-pv-cta--a">읽기</div></div>
        <div class="wg-02-meta"><label for="m02-a" class="wg-02-pick-label">브런치 · 에디토리얼</label><p class="wg-02-desc">넉넉한 여백과 장면 사진 1장. 서사 호흡에 맞는 긴 글.</p><ul class="wg-02-palette" aria-label="에디토리얼 팔레트"><li style="background:var(--bg)"><span>bg</span></li><li style="background:var(--ink)"><span>ink</span></li><li style="background:var(--accent)"><span>accent</span></li></ul><span class="wg-02-badge">선택됨</span></div></div>
      <input type="radio" name="m02-fmt" id="m02-b" class="wg-02-radio">
      <div class="wg-02-card"><div class="wg-02-preview wg-02-preview--b"><div class="wg-02-pv-bar wg-02-pv-bar--b"><span class="wg-02-pv-dot"></span><span class="wg-02-pv-line"></span></div><div class="wg-02-pv-cards"><span></span><span></span><span></span></div><div class="wg-02-pv-cta wg-02-pv-cta--b">지표</div></div>
        <div class="wg-02-meta"><label for="m02-b" class="wg-02-pick-label">티스토리 · 지표 대시보드</label><p class="wg-02-desc">표·차트·단계 카드. 검색 독자가 훑어 읽기 좋은 구조.</p><ul class="wg-02-palette" aria-label="대시보드 팔레트"><li style="background:var(--dark)"><span>dark</span></li><li style="background:var(--good-accent)"><span>good</span></li><li style="background:var(--accent)"><span>accent</span></li></ul><span class="wg-02-badge">선택됨</span></div></div>
      <input type="radio" name="m02-fmt" id="m02-c" class="wg-02-radio">
      <div class="wg-02-card"><div class="wg-02-preview wg-02-preview--c"><div class="wg-02-pv-bar wg-02-pv-bar--c"><span class="wg-02-pv-dot"></span><span class="wg-02-pv-line"></span></div><div class="wg-02-pv-split"><div class="wg-02-pv-aside"></div><div class="wg-02-pv-main"><span></span><span></span></div></div><div class="wg-02-pv-cta wg-02-pv-cta--c">요약</div></div>
        <div class="wg-02-meta"><label for="m02-c" class="wg-02-pick-label">링크드인 · 소프트 요약</label><p class="wg-02-desc">불릿 3개 + 결과 수치 강조. 모바일 피드에서 한 화면.</p><ul class="wg-02-palette" aria-label="소프트 팔레트"><li style="background:var(--analogy-bg)"><span>soft</span></li><li style="background:var(--analogy-accent)"><span>blue</span></li><li style="background:var(--accent)"><span>accent</span></li></ul><span class="wg-02-badge">선택됨</span></div></div>
    </fieldset>
    <p class="wg-02-foot">라디오 선택으로 카드가 강조됩니다(무 JS 근사). 실시간 토큰 편집은 별도 도구가 필요합니다.</p>
  </section>
</section>'''

s9 = f'''
<section id="s9" class="summary-card">
  {h2("09","해시태그·길이·SEO 가이드","note")}
  <p class="h2-sub">발행 직전 채널별 메타데이터를 정리한다. 키워드는 사실과 일치하는 것만 쓴다.</p>
  <div class="card-grid">
    <article class="mini-card"><h3>티스토리</h3><p>키워드 "온콜 알림 정책", "경보 억제". 소제목에 키워드 1회씩. 내부 링크 2개.</p></article>
    <article class="mini-card"><h3>벨로그</h3><p>태그: on-call, sre, alerting. 코드 블록 언어 지정. 시리즈 묶음 권장.</p></article>
    <article class="mini-card"><h3>브런치</h3><p>키워드 대신 감성 태그. 대표 이미지 1장. 구독 유도 마무리.</p></article>
    <article class="mini-card"><h3>링크드인</h3><p>해시태그 3개(#oncall #SRE #번아웃). 첫 2줄에 결과. 질문으로 마무리.</p></article>
  </div>
  <p>해시태그와 키워드는 "더 많이"가 아니라 "사실과 일치하게" 붙이는 것이 원칙이다. 글에서 다루지 않은 도구나 결과를 태그로 끌어오면 유입은 늘지 몰라도 체류·신뢰가 떨어진다. 특히 정량 수치를 제목에 쓸 때는 본문이 같은 수치를 근거와 함께 다시 설명하는지 반드시 확인한다. 검색·피드 알고리즘은 결국 "제목의 약속을 본문이 지키는가"를 체류시간으로 측정하기 때문이다.</p>
</section>'''

s10 = f'''
<section id="s10" class="summary-card">
  {h2("10","발행 체크리스트","check")}
  <p class="h2-sub">네 버전 모두 발행 전 이 점검을 통과해야 한다. 사실 일관성이 1순위다.</p>
  <ul class="check-list">
    <li><strong>수치 일관성</strong> — 네 버전의 11→5회, 60→22% 수치가 모두 동일한지 대조.</li>
    <li><strong>출처 표기</strong> — 정량 수치는 "사내 대시보드 기준"임을 각 글에 한 번씩 명시.</li>
    <li><strong>민감정보</strong> — 담당자 실명·내부 시스템명·미공개 장애 내용 제거.</li>
    <li><strong>채널 포맷</strong> — 분량·도입부·CTA가 비교표 사양과 일치하는지 확인.</li>
    <li><strong>중복 패널티</strong> — 동일 본문 복붙 금지. canonical/요약 차별로 SEO 중복 회피.</li>
  </ul>
  <p>체크리스트의 핵심은 "발행 전 5분"이다. 네 글을 동시에 손보면 한 곳에서 수치를 고치고 다른 곳을 빠뜨리기 쉽다. 그래서 수치·출처·민감정보는 발행 직전 한 번에 교차 점검하고, 채널 포맷은 비교표를 옆에 띄워 둔 채 맞춘다. 이 절차를 거치지 않은 변환은 "재편집"이 아니라 "분산된 복사본"이 되고, 독자는 금세 알아챈다.</p>
</section>'''

snext = f'''
<section id="snext" class="try publish-checklist">
  {h2(None,"발행 순서 · 다음 행동","landing")}
  <p>네 버전이 준비됐다면 발행 순서도 전략이다. 검색 자산을 먼저 쌓고, 도달을 넓히고, 서사로 마무리한다.</p>
  <div class="cta-box">
    <p><strong>권장 발행 순서</strong></p>
    <ol><li>티스토리 먼저 — 검색 인덱싱 리드타임이 길다(자산화 우선).</li><li>벨로그 다음 날 — 개발자 커뮤니티 반응으로 본문 보강.</li><li>링크드인 — 결과 요약으로 도달 확장, 원문 링크 연결.</li><li>브런치 마지막 — 서사 버전으로 브랜드 톤 마무리.</li></ol>
    <div class="tag-list"><span class="tag">platform_blog</span><span class="tag">on-call</span><span class="tag">멀티채널</span><span class="tag">사실 보존</span></div>
  </div>
</section>'''

source_note = '<aside class="source-note"><p><strong>출처·범위.</strong> 원문은 가상의 사내 회고이며 수치(11→5회, 60→22%)는 예시용 시나리오 값이다. 실제 발행 시에는 각 채널 정책(중복 콘텐츠·이미지 권리·해시태그 규정)과 사내 정보 공개 가이드를 다시 확인한다.</p></aside>'

body = ('<main id="main" class="page-wide layout-platform">' + header + toc + s1+s2+s3+s4+s5+s6+s7+s8+s9+s10+snext + source_note + '</main>')
out = build_page("pages/02_platform_blog_oncall_alert_policy.html", title=TITLE, description=DESC, body=body)
write_sources()
print("WROTE", out)
