#!/usr/bin/env python3
"""Mode 16 / 17 — landing_brief_html (sequential). Topic: 팀 지식베이스 SaaS 'Cortex' 랜딩 브리프.
Layout: landing-brief.html (.layout-landing) · auto · vt: hero-map(hm-grid) · wg: wg-16.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _finalize import build_page, write_sources, h2, SKILL, ASSETS  # noqa: E402,F401

for _p in [SKILL/"SKILL.md", SKILL/"references/layout-system.md", ASSETS/"layouts/landing-brief.html",
           ASSETS/"visual-html-templates/01-hero-map.html", ASSETS/"widget-templates/16-implementation-plan.html"]:
    _p.read_text(encoding="utf-8")

TITLE = "Cortex — 팀 지식베이스 랜딩 브리프"
DESC = "흩어진 팀 지식을 검색 가능한 단일 소스로 모으는 지식베이스 SaaS 'Cortex'의 가치 제안·작동 방식·도입 계획·FAQ를 정리한 landing_brief."

header = '''
<header class="header landing-header">
  <div class="kicker"><span class="kicker-text">LANDING BRIEF · MODE 16 / 17 · 독립 빌드</span></div>
  <h1>Cortex — 팀의 답이 검색되는 곳</h1>
  <p class="sub">위키·슬랙·드라이브에 흩어진 팀 지식을, 묻는 순간 답이 나오는 단일 소스로 모으는 지식베이스 SaaS. 이 브리프는 무엇을·어떻게·왜 도입하는지 한 장으로 설명한다.</p>
  <div class="meta"><span>profile auto</span><span>layout landing-brief</span><span>대상 50~300인 팀</span><span>무 동작 JS</span></div>
  <div class="generated-row"><p class="generated-date">Generated · 2026-06-13 KST</p>
  <div class="lens-strip" aria-label="적용 렌즈"><span class="lens-strip-label">LENS</span><span class="lens-chip">문제</span><span class="lens-chip">가치</span><span class="lens-chip">작동 방식</span><span class="lens-chip">도입</span><span class="lens-chip">FAQ</span></div></div>
</header>'''

toc = '''
<nav class="toc-map landing-toc" aria-label="랜딩 목차"><div class="toc-pills">
  <a class="toc-pill" href="#s1"><b>01</b> 한 줄 소개</a><a class="toc-pill" href="#s2"><b>02</b> 제품 한눈에</a>
  <a class="toc-pill" href="#s3"><b>03</b> 가치 제안</a><a class="toc-pill" href="#s4"><b>04</b> 작동 방식</a>
  <a class="toc-pill" href="#s5"><b>05</b> 핵심 기능</a><a class="toc-pill" href="#s6"><b>06</b> 도입 90일</a>
  <a class="toc-pill" href="#s7"><b>07</b> 적합·부적합</a><a class="toc-pill" href="#s8"><b>08</b> 플랜 개요</a>
  <a class="toc-pill" href="#s9"><b>09</b> 자주 묻는 질문</a><a class="toc-pill" href="#snext"><b>→</b> 시작하기</a>
</div></nav>'''

s1 = f'''
<section id="s1" class="hero-analogy summary-card">
  {h2("01","한 줄 소개","landing")}
  <p class="h2-sub">Cortex는 "팀의 답을 검색 가능하게" 만든다. 사람을 붙잡고 묻는 대신, 질문하면 출처와 함께 답이 나온다.</p>
  <div class="grid-3">
    <article class="score-card"><h3>문제</h3><p>지식이 위키·슬랙·드라이브·사람 머릿속에 흩어져 있어, 같은 질문이 매주 반복되고 신규 입사자는 "누구한테 물어야 하지"부터 막힌다.</p></article>
    <article class="score-card"><h3>해결</h3><p>흩어진 소스를 한곳에 연결하고, 자연어로 물으면 근거 문서와 함께 답을 돌려준다. 답마다 출처 링크가 붙어 신뢰할 수 있다.</p></article>
    <article class="score-card"><h3>대상</h3><p>50~300인 규모로, 문서는 쌓였지만 "찾기"가 안 되는 팀. 정보가 많을수록 가치가 커진다.</p></article>
  </div>
  <p>핵심 약속은 단순하다. <strong>"묻는 순간 출처 있는 답."</strong> 새 지식을 만들라는 게 아니라, 이미 있는 지식을 찾을 수 있게 만든다. 검색이 안 되는 지식은 없는 지식과 같기 때문이다.</p>
</section>'''

s2 = f'''
<section id="s2" class="summary-card">
  {h2("02","제품 한눈에","map")}
  <p class="h2-sub">연결 → 색인 → 응답의 세 단계로 동작한다. 한 화면으로 본다.</p>
  <section class="vt-shell" aria-label="제품 개요 지도">
    <div class="vt-frame"><div class="vt-demo"><div class="hm-grid">
      <article class="hm-card"><div class="vt-kicker">Connect</div><h3>소스 연결</h3><p class="vt-text">위키·슬랙·드라이브·이슈 트래커를 읽기 권한으로 연결.</p></article>
      <article class="hm-card" style="--c:var(--vt-blue)"><div class="vt-kicker">Index</div><h3>검색 색인</h3><p class="vt-text">문서를 색인하고 권한을 보존해, 볼 수 있는 것만 검색되게 한다.</p></article>
      <article class="hm-card" style="--c:var(--vt-green)"><div class="vt-kicker">Answer</div><h3>출처 있는 답</h3><p class="vt-text">질문에 근거 문서 링크와 함께 요약 답을 제시.</p></article>
    </div><div class="hm-result"><b>요약: 연결 → 색인 → 출처 있는 답</b><span>새 문서를 강요하지 않고, 기존 지식을 찾을 수 있게 만든다.</span></div></div></div>
  </section>
  <p>중요한 설계 원칙은 "권한 보존"이다. 검색은 사용자가 원래 볼 수 있는 문서만 대상으로 한다. 지식베이스가 권한 우회 통로가 되지 않도록, 소스의 접근 권한을 그대로 따른다.</p>
</section>'''

s3 = f'''
<section id="s3" class="value-grid summary-card">
  {h2("03","가치 제안","idea")}
  <p class="h2-sub">세 가지 측정 가능한 가치로 요약한다. 추상적 "생산성"이 아니라 줄어드는 시간으로 말한다.</p>
  <div class="card-grid">
    <article class="card-block"><h3>반복 질문 감소</h3><p>"이거 어디 있어요?" 류의 반복 질문을 셀프서비스로 흡수해, 시니어의 답변 시간을 회수한다.</p></article>
    <article class="card-block"><h3>온보딩 가속</h3><p>신규 입사자가 "누구에게 묻지" 대신 "검색"으로 시작해, 첫 주 자립 시간을 앞당긴다.</p></article>
    <article class="card-block"><h3>지식 유실 방지</h3><p>핵심 인력이 떠나도 답이 문서·대화에 남아 검색된다. 버스 팩터 위험을 낮춘다.</p></article>
  </div>
  <p>가치의 공통 축은 "시간"이다. 흩어진 지식을 찾느라 쓰는 시간 — 묻고, 기다리고, 다시 묻는 — 을 회수하는 것이 Cortex의 ROI다. 도입 후엔 "반복 질문 수"와 "온보딩 자립 시간"으로 효과를 측정하길 권한다.</p>
</section>'''

s4 = f'''
<section id="s4" class="how-it-works summary-card">
  {h2("04","작동 방식","flow")}
  <p class="h2-sub">"마법"이 아니라 단계다. 사용자가 질문을 던지면 내부에서 일어나는 일을 순서로 본다.</p>
  <section class="vt-shell" aria-label="작동 흐름">
    <div class="vt-frame"><ol class="tl">
      <li class="tl-item"><b>질문 입력</b><p class="vt-text">자연어로 "환불 정책 어떻게 돼요?"처럼 묻는다.</p></li>
      <li class="tl-item"><b>권한 필터 검색</b><p class="vt-text">사용자가 볼 수 있는 문서만 대상으로 관련 구절을 찾는다.</p></li>
      <li class="tl-item"><b>근거 기반 요약</b><p class="vt-text">찾은 구절을 근거로 답을 구성하고, 각 문장에 출처를 붙인다.</p></li>
      <li class="tl-item"><b>출처 제시</b><p class="vt-text">답과 함께 원문 링크를 보여 사용자가 검증할 수 있게 한다.</p></li>
    </ol></div>
  </section>
  <p>핵심은 "출처 없는 답은 내지 않는다"는 원칙이다. 근거 문서를 찾지 못하면 "확실한 답을 찾지 못했다"고 말하고 관련 문서만 제시한다. 그럴듯한 추측보다 "모른다"가 신뢰를 지킨다.</p>
</section>'''

s5 = f'''
<section id="s5" class="summary-card">
  {h2("05","핵심 기능","compare")}
  <p class="h2-sub">도입 검토 시 자주 묻는 기능을 묶음으로 정리한다.</p>
  <div class="card-grid">
    <article class="mini-card"><h3>다중 소스 연결</h3><p>위키·슬랙·드라이브·이슈 트래커 커넥터. 읽기 권한 기반, 주기적 동기화.</p></article>
    <article class="mini-card"><h3>출처 있는 답변</h3><p>모든 답에 근거 링크. 근거 없으면 추측 대신 관련 문서 제시.</p></article>
    <article class="mini-card"><h3>권한 보존</h3><p>소스 권한을 그대로 따라, 볼 수 없는 문서는 검색·인용되지 않는다.</p></article>
    <article class="mini-card"><h3>지식 공백 리포트</h3><p>"답을 못 찾은 질문"을 모아, 문서화가 필요한 주제를 알려준다.</p></article>
  </div>
  <p>차별점은 마지막 "지식 공백 리포트"다. 단순 검색이 아니라, 무엇이 문서화되지 않았는지를 데이터로 보여줘 지식베이스가 스스로 보강 방향을 가리키게 한다. 검색 도구가 아니라 지식 관리 루프를 만든다.</p>
</section>'''

s6 = f'''
<section id="s6" class="summary-card">
  {h2("06","도입 90일","timeline")}
  <p class="h2-sub">"깔면 끝"이 아니다. 90일에 걸쳐 단계적으로 가치를 키우는 도입 계획을 제시한다.</p>
  <section class="wg-16" aria-labelledby="m16-wg16-title">
    <header class="wg-16-head"><p class="wg-16-kicker">도입 계획 · ONB-16</p><h2 id="m16-wg16-title" class="wg-16-h">Cortex 90일 온보딩</h2><p class="wg-16-lead">한 팀 파일럿으로 시작해 <strong>출처 신뢰</strong>를 확인한 뒤 전사로 확장합니다.</p></header>
    <div class="wg-16-panel">
      <h3 class="wg-16-h3">마일스톤</h3>
      <ol class="wg-16-ms">
        <li class="wg-16-ms-item wg-16-done"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">M0 · 소스 연결</span><span class="wg-16-badge wg-16-bd-done">완료</span></div><p class="wg-16-ms-desc">핵심 위키·드라이브 읽기 권한 연결, 색인 시작.</p></div></li>
        <li class="wg-16-ms-item wg-16-active"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">M1 · 한 팀 파일럿 (0~30일)</span><span class="wg-16-badge wg-16-bd-active">진행 중</span></div><p class="wg-16-ms-desc">한 팀에서 답변 정확도·출처 신뢰 검증, 지식 공백 수집.</p></div></li>
        <li class="wg-16-ms-item"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">M2 · 부서 확장 (31~60일)</span><span class="wg-16-badge">예정</span></div><p class="wg-16-ms-desc">권한 경계 검증 후 2~3개 부서로 확장, 공백 문서화.</p></div></li>
        <li class="wg-16-ms-item"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">M3 · 전사 정착 (61~90일)</span><span class="wg-16-badge">예정</span></div><p class="wg-16-ms-desc">전사 롤아웃, 반복 질문 감소·온보딩 시간 측정.</p></div></li>
      </ol>
      <h3 class="wg-16-h3">데이터 플로우</h3>
      <div class="wg-16-flow" aria-label="지식 데이터 플로우">
        <div class="wg-16-fnode">소스<span class="wg-16-fnode-s">위키·슬랙·드라이브</span></div>
        <div class="wg-16-fnode wg-16-fnode-good">커넥터<span class="wg-16-fnode-s">권한 보존 수집</span></div>
        <div class="wg-16-fnode wg-16-fnode-hot">색인<span class="wg-16-fnode-s">검색·임베딩</span></div>
        <div class="wg-16-fnode">질의<span class="wg-16-fnode-s">권한 필터</span></div>
        <div class="wg-16-fnode wg-16-fnode-q">답변<span class="wg-16-fnode-s">출처 동반</span></div>
      </div>
    </div>
  </section>
</section>'''

s7 = f'''
<section id="s7" class="summary-card">
  {h2("07","적합·부적합","decision")}
  <p class="h2-sub">모든 팀에 맞는 제품은 없다. 솔직하게 적합·부적합을 가른다.</p>
  <div class="grid-2">
    <article class="good"><span class="label">적합</span><p>문서가 이미 어느 정도 쌓였고 흩어져 있는 50~300인 팀. "정보는 있는데 못 찾는" 문제가 핵심인 조직.</p></article>
    <article class="danger"><span class="label">부적합</span><p>문서 자체가 거의 없는 초기 팀(검색할 대상이 없음), 또는 규제상 외부 SaaS에 지식을 둘 수 없는 조직(셀프호스트 요건).</p></article>
  </div>
  <p>부적합 사례를 분명히 하는 이유는, 잘못된 도입이 양쪽 모두에 손해이기 때문이다. 문서가 없는 팀은 먼저 기록 문화를 만들어야 하고, 규제 요건이 강한 조직은 셀프호스트 옵션을 먼저 확인해야 한다. 맞는 팀에 들어갈 때 가장 큰 가치가 난다.</p>
</section>'''

s8 = f'''
<section id="s8" class="summary-card">
  {h2("08","플랜 개요","metric")}
  <p class="h2-sub">정확한 가격은 영업 견적이 필요하므로, 여기서는 플랜 구조와 무엇이 가격을 결정하는지만 밝힌다.</p>
  <div class="table-scroll"><table>
    <caption>플랜 구조 개요</caption>
    <thead><tr><th>플랜</th><th>대상</th><th>핵심 차이</th><th>가격 결정 요인</th></tr></thead>
    <tbody>
      <tr><th>Team</th><td>단일 팀 파일럿</td><td>핵심 커넥터·기본 검색</td><td>사용자 수</td></tr>
      <tr><th>Business</th><td>부서~전사</td><td>권한 정밀 제어·공백 리포트</td><td>사용자 수 + 소스 수</td></tr>
      <tr><th>Enterprise</th><td>규제·대규모</td><td>SSO·감사 로그·셀프호스트 옵션</td><td>요건 협의</td></tr>
    </tbody>
  </table></div>
  <p>가격은 주로 "사용자 수 + 연결 소스 수"로 결정된다. 정확한 수치는 확인이 필요하므로(확인 필요) 견적으로 안내하며, 본 브리프는 구조만 제시한다. 도입 ROI는 가격보다 "회수되는 반복 질문 시간"으로 따지는 편이 합리적이다.</p>
</section>'''

s9 = f'''
<section id="s9" class="faq summary-card">
  {h2("09","자주 묻는 질문","question")}
  <p class="h2-sub">도입 검토에서 가장 많이 나오는 질문에 솔직히 답한다.</p>
  <div class="faq-list">
    <details class="faq-item" open><summary>권한이 없는 문서가 검색에 노출되나요?</summary><p>아니요. 소스의 읽기 권한을 그대로 따릅니다. 볼 수 없는 문서는 검색·인용·답변 어디에도 나타나지 않습니다.</p></details>
    <details class="faq-item"><summary>답이 틀리면 어떻게 되나요?</summary><p>모든 답에 출처 링크가 붙어 사용자가 즉시 검증할 수 있습니다. 근거를 못 찾으면 추측 대신 "확실한 답을 찾지 못했다"고 답합니다.</p></details>
    <details class="faq-item"><summary>우리 데이터로 모델을 학습시키나요?</summary><p>도입 정책에 따라 다르며, 기본적으로 고객 데이터를 모델 학습에 쓰지 않는 옵션을 제공합니다(계약·플랜으로 확인 필요).</p></details>
    <details class="faq-item"><summary>기존 위키를 버려야 하나요?</summary><p>아니요. Cortex는 기존 소스를 대체하지 않고 그 위에서 검색·답변을 제공합니다. 문서는 원래 있던 곳에 그대로 둡니다.</p></details>
  </div>
</section>'''

snext = f'''
<section id="snext" class="try">
  {h2(None,"시작하기","success")}
  <p>가장 빠른 검증은 "한 팀, 핵심 소스 하나"로 2주 파일럿을 돌려 답변 정확도와 출처 신뢰를 직접 보는 것이다.</p>
  <div class="cta-box">
    <p><strong>2주 파일럿 시작</strong></p>
    <ol><li>가장 질문이 많은 한 팀 선정 + 핵심 위키 1개 연결</li><li>실제 반복 질문 20개로 답변·출처 정확도 평가</li><li>지식 공백 리포트로 문서화 우선순위 도출 → 확장 결정</li></ol>
    <div class="tag-list"><span class="tag">landing_brief</span><span class="tag">knowledge-base</span><span class="tag">saas</span><span class="tag">출처 있는 답</span></div>
  </div>
</section>'''

source_note = '<aside class="source-note"><p><strong>출처·범위.</strong> 본 브리프는 가상의 지식베이스 SaaS "Cortex"의 도입 안내 예시다. 가격·데이터 정책 등 계약 사항은 확인이 필요(확인 필요)하며, 효과(반복 질문 감소·온보딩 시간)는 도입 후 자사 지표로 측정해야 한다.</p></aside>'

body = ('<main id="main" class="page-wide layout-landing">' + header + toc + s1+s2+s3+s4+s5+s6+s7+s8+s9+snext + source_note + '</main>')
out = build_page("pages/16_landing_brief_html_cortex.html", title=TITLE, description=DESC, body=body)
write_sources()
print("WROTE", out)
