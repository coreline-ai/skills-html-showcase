#!/usr/bin/env python3
"""Mode 03 / 17 — seo_dashboard (independent build, sequential).
Topic: 기술 포스트 "사내 문서 검색을 OpenSearch로 구축하기"의 검색 최적화 대시보드.
Primary keyword: "사내 문서 검색 구축". Layout: seo-dashboard.html (.layout-seo) · auto
1순위 vt: card-grid(cg-grid) · 권장 wg: wg-11(weekly-status)
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _finalize import build_page, write_sources, h2, SKILL, ASSETS  # noqa: E402,F401

for _p in [SKILL/"SKILL.md", SKILL/"references/blog-seo-system.md", ASSETS/"layouts/seo-dashboard.html",
           ASSETS/"visual-html-templates/07-card-grid.html", ASSETS/"widget-templates/11-weekly-status.html"]:
    _p.read_text(encoding="utf-8")

TITLE = "사내 문서 검색 구축 — SEO 대시보드"
DESC = "기술 포스트 '사내 문서 검색을 OpenSearch로 구축하기'의 검색 의도, SERP 미리보기, 제목·메타 후보, 키워드 클러스터, 발행 후 추적 지표를 정리한 seo_dashboard."

header = '''
<header class="header seo-header">
  <div class="kicker"><span class="kicker-text">SEO DASHBOARD · MODE 03 / 17 · 독립 빌드</span></div>
  <h1>사내 문서 검색 구축, 검색에 닿게</h1>
  <p class="sub">"사내 문서 검색을 OpenSearch로 구축하기" 포스트를, 검색 유입까지 고려해 제목·메타·키워드·구조로 설계하는 대시보드. 핵심 키워드는 <strong>사내 문서 검색 구축</strong>.</p>
  <div class="meta"><span>profile auto</span><span>layout seo-dashboard</span><span>1차 키워드 사내 문서 검색 구축</span><span>무 동작 JS</span></div>
  <div class="generated-row"><p class="generated-date">Generated · 2026-06-13 KST</p>
  <div class="lens-strip" aria-label="적용 렌즈"><span class="lens-strip-label">LENS</span><span class="lens-chip">검색 의도</span><span class="lens-chip">SERP</span><span class="lens-chip">제목·메타</span><span class="lens-chip">키워드 클러스터</span><span class="lens-chip">추적</span></div></div>
</header>'''

toc = '''
<nav class="toc-map seo-toc" aria-label="SEO 목차"><div class="toc-pills">
  <a class="toc-pill" href="#s1"><b>01</b> 핵심 키워드</a><a class="toc-pill" href="#s2"><b>02</b> 검색 의도 분해</a>
  <a class="toc-pill" href="#s3"><b>03</b> SERP 미리보기</a><a class="toc-pill" href="#s4"><b>04</b> 제목 후보</a>
  <a class="toc-pill" href="#s5"><b>05</b> 메타 후보</a><a class="toc-pill" href="#s6"><b>06</b> 키워드 클러스터</a>
  <a class="toc-pill" href="#s7"><b>07</b> 본문 H2 골격</a><a class="toc-pill" href="#s8"><b>08</b> 내부 링크·구조화</a>
  <a class="toc-pill" href="#s9"><b>09</b> 발행 후 추적</a><a class="toc-pill" href="#s10"><b>10</b> 흔한 SEO 실수</a>
  <a class="toc-pill" href="#snext"><b>→</b> 발행 체크리스트</a>
</div></nav>'''

s1 = f'''
<section id="s1" class="summary-card">
  {h2("01","핵심 키워드와 포지셔닝","search")}
  <p class="h2-sub">1차 키워드는 "사내 문서 검색 구축". 검색하는 사람은 대개 "흩어진 사내 지식을 검색 가능하게 만들고 싶은 실무자"다.</p>
  <div class="grid-3">
    <article class="score-card"><h3>1차 키워드</h3><p>사내 문서 검색 구축 — 명확한 구축 의도. 경쟁은 중간, 전환(도입 검토)으로 이어지는 가치 높은 질의.</p></article>
    <article class="score-card"><h3>독자</h3><p>위키·드라이브에 흩어진 문서를 "검색되게" 만들려는 플랫폼/백엔드 엔지니어. 도구 선택과 구축 절차를 동시에 원한다.</p></article>
    <article class="score-card"><h3>약속</h3><p>제목이 "OpenSearch로 구축"을 약속했으면, 본문은 색인 설계·동의어·권한 필터까지 실제 구축 절차를 줘야 한다.</p></article>
  </div>
  <p>SEO의 출발은 키워드가 아니라 "검색자가 이루려는 일"이다. 이 포스트는 단순 소개가 아니라 "따라 하면 구축되는" 실무 가이드를 약속하므로, 제목·메타·본문이 그 약속을 일관되게 지켜야 검색·체류 모두 좋아진다.</p>
</section>'''

s2 = f'''
<section id="s2" class="summary-card">
  {h2("02","검색 의도 분해","idea")}
  <p class="h2-sub">같은 키워드라도 의도가 갈린다. 어느 의도를 1차 타깃으로 둘지 정한다.</p>
  <div class="card-grid">
    <article class="mini-card"><h3>정보형</h3><p>"사내 문서 검색이 뭐가 어렵나" — 개념·문제 이해. 도입부에서 충족.</p></article>
    <article class="mini-card"><h3>비교형</h3><p>"OpenSearch vs Elasticsearch vs SaaS" — 선택 기준. 본문 중반 표로 충족.</p></article>
    <article class="mini-card"><h3>구축형(1차)</h3><p>"OpenSearch로 어떻게 색인·검색을 붙이나" — 절차·코드. 본문 핵심.</p></article>
    <article class="mini-card"><h3>운영형</h3><p>"권한·동의어·관련도 튜닝" — 도입 후 과제. 후반에서 충족.</p></article>
  </div>
  <p>이 포스트는 <strong>구축형</strong>을 1차로, 비교형·운영형을 보조로 둔다. 의도를 섞어 모두를 노리면 어느 검색자도 만족시키지 못한다. 1차 의도를 정하면 제목·도입·H2 순서가 자동으로 정렬된다.</p>
</section>'''

s3 = f'''
<section id="s3" class="serp-preview summary-card">
  {h2("03","SERP 미리보기","experiment")}
  <p class="h2-sub">검색 결과에 어떻게 보일지 먼저 그려 본다. 제목·URL·설명이 한 화면에서 클릭을 결정한다.</p>
  <div class="serp-shell">
    <div class="serp-box">
      <div class="serp-url">example.dev › blog › opensearch-internal-search</div>
      <div class="serp-title">사내 문서 검색을 OpenSearch로 구축하기 — 색인부터 권한까지</div>
      <div class="serp-desc">흩어진 위키·드라이브 문서를 OpenSearch로 검색 가능하게 만드는 전 과정. 색인 설계, 한국어 형태소 분석, 동의어, 권한 필터, 관련도 튜닝까지 실제 설정과 함께 정리했습니다.</div>
    </div>
  </div>
  <div class="serp-rule-grid">
    <div class="serp-rule"><span class="serp-rule-kicker">제목</span>키워드를 앞에, 30자 내외. "OpenSearch"와 "구축"을 모두 포함.</div>
    <div class="serp-rule"><span class="serp-rule-kicker">URL</span>짧고 키워드 포함한 슬러그. 한글·날짜·물음표 지양.</div>
    <div class="serp-rule"><span class="serp-rule-kicker">설명</span>120~155자. 무엇을 다루는지 + 절차 키워드를 자연스럽게.</div>
  </div>
  <p>SERP 미리보기를 먼저 만드는 이유는, 본문을 다 쓴 뒤 제목·설명을 끼워 맞추면 늘 어색해지기 때문이다. "검색 결과 한 줄"이 곧 독자가 보는 첫 약속이므로, 이 약속을 먼저 정하고 본문이 그것을 지키게 한다.</p>
</section>'''

s4 = f'''
<section id="s4" class="summary-card">
  {h2("04","제목 후보","edit")}
  <p class="h2-sub">제목은 키워드·길이·후킹의 균형이다. 후보를 두고 의도 적합도로 고른다.</p>
  <div class="table-scroll"><table>
    <caption>제목 후보 비교</caption>
    <thead><tr><th>후보</th><th>키워드 위치</th><th>길이</th><th>판단</th></tr></thead>
    <tbody>
      <tr><th>사내 문서 검색을 OpenSearch로 구축하기 — 색인부터 권한까지</th><td>앞</td><td>적정</td><td><strong>채택</strong> · 키워드+범위 명확</td></tr>
      <tr><th>OpenSearch로 만드는 사내 검색 시스템 완벽 가이드</th><td>중</td><td>적정</td><td>"완벽"은 과장 신호, 보류</td></tr>
      <tr><th>우리 회사 문서, 드디어 검색된다</th><td>없음</td><td>짧음</td><td>후킹은 좋으나 키워드 부재</td></tr>
      <tr><th>Elasticsearch 대신 OpenSearch를 고른 이유와 구축기</th><td>중</td><td>김</td><td>비교형 의도엔 적합, 1차 의도엔 분산</td></tr>
    </tbody>
  </table></div>
  <p>채택 기준은 "1차 의도(구축형)와 키워드를 앞에서 만족시키되 과장이 없는가"다. "완벽 가이드" 같은 표현은 클릭은 올려도 기대-내용 격차로 체류를 떨어뜨리므로 피한다.</p>
</section>'''

s5 = f'''
<section id="s5" class="summary-card">
  {h2("05","메타 디스크립션 후보","note")}
  <p class="h2-sub">메타는 순위 요인은 약하지만 클릭률(CTR)을 좌우한다. 120~155자에 절차 키워드를 자연스럽게 담는다.</p>
  <ul class="check-list">
    <li><strong>후보 A (채택)</strong> — "흩어진 위키·드라이브 문서를 OpenSearch로 검색 가능하게. 색인 설계, 한국어 형태소 분석, 동의어, 권한 필터, 관련도 튜닝까지 실제 설정과 함께."</li>
    <li><strong>후보 B</strong> — "사내 검색을 직접 구축하는 법. OpenSearch 설치부터 운영까지 단계별로." (키워드는 있으나 구체 절차 신호가 약함)</li>
    <li><strong>후보 C</strong> — "검색이 안 되는 사내 문서, 이제 그만." (감성적이지만 무엇을 주는지 불명확)</li>
  </ul>
  <p>채택한 후보 A는 "무엇을(문서 검색) + 무엇으로(OpenSearch) + 어디까지(색인·동의어·권한·튜닝)"를 한 문장에 담아, 검색자가 "내가 찾던 깊이의 글"임을 즉시 판단하게 한다. 메타는 본문 첫 문단과 일치시켜 기대-내용 격차를 없앤다.</p>
</section>'''

s6 = f'''
<section id="s6" class="summary-card">
  {h2("06","키워드 클러스터","compare")}
  <p class="h2-sub">1차 키워드 하나로는 부족하다. 함께 다뤄야 검색 폭이 넓어지는 보조 키워드를 묶는다.</p>
  <section class="vt-shell" aria-label="키워드 클러스터">
    <div class="vt-frame"><div class="cg-grid">
      <article class="cg-card"><em>01</em><b>색인 설계</b><p>매핑·분석기</p></article>
      <article class="cg-card"><em>02</em><b>한국어 분석</b><p>nori 형태소</p></article>
      <article class="cg-card"><em>03</em><b>동의어</b><p>synonym 필터</p></article>
      <article class="cg-card"><em>04</em><b>권한 필터</b><p>문서 단위 ACL</p></article>
      <article class="cg-card"><em>05</em><b>관련도 튜닝</b><p>BM25·부스팅</p></article>
      <article class="cg-card"><em>06</em><b>운영</b><p>색인 재구축</p></article>
    </div></div>
  </section>
  <p>이 여섯 보조 키워드는 각각 하위 H2가 되어 long-tail 검색을 흡수한다. "OpenSearch 한국어 검색", "문서 권한 필터" 같은 구체 질의가 모두 이 한 글로 들어오게 만드는 것이 클러스터 전략의 목적이다. 주의할 점은 클러스터를 욕심내 한 글에 모든 키워드를 담으면 글이 산만해진다는 것이다. 1차 키워드를 본문의 척추로 삼고, 보조 키워드는 그 척추에 매달린 갈비뼈처럼 각자 한 섹션씩만 책임지게 해야 글의 초점이 흐려지지 않는다.</p>
</section>'''

s7 = f'''
<section id="s7" class="summary-card">
  {h2("07","본문 H2 골격 매핑","reference")}
  <p class="h2-sub">키워드 클러스터를 본문 구조로 옮긴다. 검색 의도 순서대로 H2를 배치한다.</p>
  <div class="table-scroll"><table>
    <caption>H2 골격과 대응 키워드·의도</caption>
    <thead><tr><th>H2</th><th>대응 키워드</th><th>충족 의도</th></tr></thead>
    <tbody>
      <tr><th>왜 사내 검색이 어려운가</th><td>사내 문서 검색</td><td>정보형 도입</td></tr>
      <tr><th>색인 설계와 한국어 분석</th><td>색인 설계·nori</td><td>구축형 핵심</td></tr>
      <tr><th>동의어와 권한 필터</th><td>동의어·권한</td><td>구축형 심화</td></tr>
      <tr><th>관련도 튜닝</th><td>BM25·부스팅</td><td>운영형</td></tr>
      <tr><th>도구 비교(부록)</th><td>OpenSearch vs ES</td><td>비교형 보조</td></tr>
    </tbody>
  </table></div>
  <p>H2 순서는 "정보 → 구축 → 운영 → 비교"로, 1차 의도(구축)를 가운데 핵심에 두고 앞뒤로 진입·심화를 배치한다. 비교형은 본문을 분산시키지 않도록 부록으로 내려 long-tail만 흡수하게 한다.</p>
</section>'''

s8 = f'''
<section id="s8" class="summary-card">
  {h2("08","내부 링크·구조화 데이터","connection")}
  <p class="h2-sub">한 글이 외딴섬이면 검색 자산이 안 된다. 내부 링크와 구조화 데이터로 맥락을 연결한다.</p>
  <div class="grid-2">
    <article class="card-block"><h3>내부 링크</h3><ul><li>관련 글 "OpenSearch 운영 비용 최적화"로 연결</li><li>상위 허브 "사내 플랫폼 가이드"에서 이 글로 링크</li><li>앵커 텍스트에 키워드 자연 포함</li></ul></article>
    <article class="card-block"><h3>구조화 데이터</h3><ul><li>Article 스키마(제목·작성자·날짜)</li><li>HowTo 스키마(구축 단계가 절차형이므로 적합)</li><li>FAQ 스키마(권한·한국어 분석 자주 묻는 질문)</li></ul></article>
  </div>
  <p>구조화 데이터는 순위를 직접 올리진 않지만, 검색 결과에 단계·FAQ 리치 스니펫으로 노출될 가능성을 높인다. 다만 본문에 실제로 있는 내용만 마크업해야 하며, 없는 단계를 스키마로 지어내면 정책 위반이다.</p>
</section>'''

s9 = f'''
<section id="s9" class="summary-card">
  {h2("09","발행 후 추적 지표","metric")}
  <p class="h2-sub">발행은 끝이 아니라 시작이다. 4주 추적으로 제목·메타를 개선한다.</p>
  <section class="wg-11" aria-labelledby="m03-ws-title">
    <header class="wg-11-head"><p class="wg-11-kicker">발행 후 4주 추적 (목표치)</p><h2 id="m03-ws-title" class="wg-11-h">사내 검색 구축 글 SEO 성과판</h2><p class="wg-11-lead">노출·CTR·평균 순위·체류를 한 화면으로. 실제 값은 서치 콘솔에서 확인.</p></header>
    <div class="wg-11-kpis">
      <div class="wg-11-kpi wg-11-kpi-prog"><span class="wg-11-kpi-v">≤10</span><span class="wg-11-kpi-l">평균 순위</span></div>
      <div class="wg-11-kpi wg-11-kpi-good"><span class="wg-11-kpi-v">3%+</span><span class="wg-11-kpi-l">CTR</span></div>
      <div class="wg-11-kpi"><span class="wg-11-kpi-v">2분+</span><span class="wg-11-kpi-l">체류</span></div>
      <div class="wg-11-kpi wg-11-kpi-risk"><span class="wg-11-kpi-v wg-11-warn">감시</span><span class="wg-11-kpi-l">이탈률</span></div>
    </div>
    <h3 class="wg-11-h3">개선 워크스트림</h3>
    <div class="wg-11-bars">
      <div class="wg-11-bar-row"><span class="wg-11-bar-label">색인(검색 노출)</span><div class="wg-11-track" role="img" aria-label="색인 노출 진척 90퍼센트"><div class="wg-11-fill wg-11-fill-good" style="width:90%"></div></div><span class="wg-11-bar-pct">진행</span></div>
      <div class="wg-11-bar-row"><span class="wg-11-bar-label">제목 CTR 실험</span><div class="wg-11-track" role="img" aria-label="제목 실험 진척 50퍼센트"><div class="wg-11-fill wg-11-fill-prog" style="width:50%"></div></div><span class="wg-11-bar-pct">진행</span></div>
      <div class="wg-11-bar-row"><span class="wg-11-bar-label">long-tail 보강</span><div class="wg-11-track" role="img" aria-label="long-tail 보강 진척 30퍼센트, 리스크"><div class="wg-11-fill wg-11-fill-risk" style="width:30%"></div></div><span class="wg-11-bar-pct">대기</span></div>
    </div>
    <div class="wg-11-cols">
      <div class="wg-11-col wg-11-col-good"><h4 class="wg-11-col-h"><span class="wg-11-dot"></span>점검 완료</h4><ul class="wg-11-col-list"><li>색인 등록 확인</li><li>구조화 데이터 검증</li></ul></div>
      <div class="wg-11-col wg-11-col-prog"><h4 class="wg-11-col-h"><span class="wg-11-dot"></span>진행 중</h4><ul class="wg-11-col-list"><li>제목 A/B 관찰</li><li>이탈 구간 분석</li></ul></div>
      <div class="wg-11-col wg-11-col-risk"><h4 class="wg-11-col-h"><span class="wg-11-dot"></span>주의</h4><ul class="wg-11-col-list"><li>노출 대비 CTR 저조 시 메타 재작성 <span class="wg-11-flag">개선 필요</span></li></ul></div>
    </div>
  </section>
</section>'''

s10 = f'''
<section id="s10" class="summary-card">
  {h2("10","흔한 SEO 실수","warning")}
  <p class="h2-sub">기술 글이 검색에서 손해 보는 전형적 패턴들. 발행 전 한 번 더 확인한다.</p>
  <div class="card-grid">
    <article class="mini-card"><span class="case-label">치명</span><h3>제목-내용 격차</h3><p>"완벽 가이드"라 해놓고 개념만 다루면, 클릭은 늘어도 즉시 이탈해 순위가 떨어진다.</p></article>
    <article class="mini-card"><span class="case-label">경고</span><h3>키워드 스터핑</h3><p>"사내 문서 검색"을 부자연스럽게 반복하면 가독성과 신뢰가 함께 떨어진다.</p></article>
    <article class="mini-card"><span class="case-label">경고</span><h3>코드만 나열</h3><p>설정 블록만 쌓고 설명이 없으면 체류는 짧고 공유는 안 된다.</p></article>
    <article class="mini-card"><span class="case-label">경고</span><h3>이미지 alt 누락</h3><p>다이어그램 alt가 없으면 이미지 검색·접근성 점수를 모두 잃는다.</p></article>
  </div>
  <p>네 실수의 공통 원인은 "검색 엔진을 속이려는" 접근이다. 현대 SEO는 결국 "검색자의 일을 실제로 끝내 주는 글"을 보상한다. 기술 글에서는 코드 + 설명 + 검증 가능한 절차가 그 보상의 핵심이다.</p>
</section>'''

snext = f'''
<section id="snext" class="try">
  {h2(None,"발행 체크리스트 · 다음 행동","landing")}
  <p>제목·메타·구조가 정해졌다면, 발행 전 마지막 점검으로 검색 자산의 완성도를 끌어올린다.</p>
  <div class="cta-box">
    <p><strong>발행 전 점검</strong></p>
    <ol><li>제목·메타·본문 첫 문단이 같은 약속을 하는가.</li><li>H2 골격이 검색 의도 순서(정보→구축→운영→비교)를 따르는가.</li><li>구조화 데이터가 본문에 실제 있는 내용만 마크업하는가.</li><li>서치 콘솔 색인 요청 + 4주 추적 일정 설정.</li></ol>
    <div class="tag-list"><span class="tag">seo_dashboard</span><span class="tag">opensearch</span><span class="tag">사내 검색</span><span class="tag">검색 의도</span></div>
  </div>
</section>'''

source_note = '<aside class="source-note"><p><strong>출처·범위.</strong> 본 대시보드의 순위·CTR·체류 목표치는 일반적 기술 블로그 기준의 추정치이며, 실제 성과는 도메인 권위·경쟁·서치 콘솔 데이터로 재확인해야 한다. 키워드 난이도·검색량은 키워드 도구로 별도 검증한다.</p></aside>'

body = ('<main id="main" class="page-wide layout-seo">' + header + toc + s1+s2+s3+s4+s5+s6+s7+s8+s9+s10+snext + source_note + '</main>')
out = build_page("pages/03_seo_dashboard_internal_doc_search.html", title=TITLE, description=DESC, body=body)
write_sources()
print("WROTE", out)
