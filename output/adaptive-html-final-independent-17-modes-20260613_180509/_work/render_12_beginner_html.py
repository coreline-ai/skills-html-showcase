#!/usr/bin/env python3
"""Mode 12 / 17 — beginner_html (sequential). Topic: HTTPS와 TLS 핸드셰이크 입문.
Layout: beginner-learning.html (.layout-beginner) · auto · vt: concept-explainer(concept-ring) · wg: wg-13.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _finalize import build_page, write_sources, h2, SKILL, ASSETS  # noqa: E402,F401

for _p in [SKILL/"SKILL.md", SKILL/"references/layout-system.md", ASSETS/"layouts/beginner-learning.html",
           ASSETS/"visual-html-templates/15-concept-explainer.html", ASSETS/"widget-templates/13-annotated-flowchart.html"]:
    _p.read_text(encoding="utf-8")

TITLE = "HTTPS와 TLS 핸드셰이크, 처음부터 천천히"
DESC = "자물쇠 아이콘 뒤에서 무슨 일이 벌어지는지 비유와 단계로 풀어내는 초보자용 입문. 대칭/비대칭 키, 인증서, 핸드셰이크 흐름과 흔한 오해까지 천천히 짚는다."

header = '''
<header class="header">
  <div class="kicker"><span class="kicker-text">BEGINNER · MODE 12 / 17 · 독립 빌드</span></div>
  <h1>HTTPS와 TLS 핸드셰이크, 천천히</h1>
  <p class="sub">주소창의 자물쇠 아이콘은 무엇을 보장할까? 그 뒤에서 브라우저와 서버가 주고받는 "악수(handshake)"를 비유로 차근차근 풀어 본다.</p>
  <div class="meta"><span>profile auto</span><span>layout beginner-learning</span><span>선수 지식 없음</span><span>비유 중심</span></div>
  <div class="generated-row"><p class="generated-date">Generated · 2026-06-13 KST</p>
  <div class="lens-strip" aria-label="적용 렌즈"><span class="lens-strip-label">LENS</span><span class="lens-chip">비유</span><span class="lens-chip">용어</span><span class="lens-chip">단계</span><span class="lens-chip">오해 교정</span><span class="lens-chip">실습</span></div></div>
</header>'''

toc = '''
<nav class="toc-map beginner-toc" aria-label="학습 순서"><div class="toc-pills">
  <a class="toc-pill" href="#s1"><b>01</b> HTTPS란</a><a class="toc-pill" href="#s2"><b>02</b> 왜 필요한가</a>
  <a class="toc-pill" href="#s3"><b>03</b> 핵심 용어</a><a class="toc-pill" href="#s4"><b>04</b> 핸드셰이크 한눈에</a>
  <a class="toc-pill" href="#s5"><b>05</b> 두 종류의 열쇠</a><a class="toc-pill" href="#s6"><b>06</b> 인증서와 신뢰</a>
  <a class="toc-pill" href="#s7"><b>07</b> 단계별 흐름</a><a class="toc-pill" href="#s8"><b>08</b> 흔한 오해</a>
  <a class="toc-pill" href="#s9"><b>09</b> 직접 확인하기</a><a class="toc-pill" href="#snext"><b>→</b> 복습 체크리스트</a>
</div></nav>'''

s1 = f'''
<section id="s1" class="beginner-zero summary-card">
  {h2("01","HTTPS란 무엇인가","learning")}
  <p class="h2-sub">HTTP에 S 하나가 붙었을 뿐인데, 그 S가 통신을 통째로 봉인한다. S는 Secure, 즉 "안전한"이다.</p>
  <p>웹페이지를 불러올 때 브라우저와 서버는 HTTP라는 규칙으로 대화한다. 문제는 기본 HTTP가 <strong>엽서</strong>와 같다는 점이다. 오가는 내용을 중간의 누구나 읽을 수 있다. 로그인 비밀번호도, 카드 번호도 평문으로 흐른다.</p>
  <p>HTTPS는 이 대화를 봉인한다. 내용을 암호화해서, 중간에서 가로채도 의미를 알 수 없게 만든다. 동시에 "내가 접속한 서버가 진짜 그 서버가 맞는지"도 확인해 준다. 즉 HTTPS는 <strong>비밀 유지(암호화)</strong>와 <strong>신원 확인(인증)</strong>을 함께 제공한다. 자물쇠 아이콘은 이 두 가지가 작동 중이라는 표시다.</p>
</section>'''

s2 = f'''
<section id="s2" class="beginner-analogy summary-card">
  {h2("02","왜 필요한가 — 엽서와 봉인 편지","idea")}
  <p class="h2-sub">암호화가 없는 통신이 왜 위험한지, 우편에 비유하면 한 번에 와닿는다.</p>
  <div class="analogy"><span class="label">비유</span><p>HTTP는 <strong>엽서</strong>다. 우체부도, 중간 분류소 직원도 내용을 다 볼 수 있다. HTTPS는 <strong>봉인된 편지</strong>다. 받는 사람만 열 수 있는 자물쇠로 잠겨 있어, 배달 과정의 누구도 내용을 읽지 못한다. 게다가 봉인에는 발신자의 "인장"이 찍혀 있어, 가짜가 보낸 편지인지도 구별된다.</p></div>
  <p>공공 와이파이를 떠올리면 더 분명하다. 카페 와이파이로 엽서(HTTP)를 보내면 같은 네트워크의 누군가가 들여다볼 수 있다. 하지만 봉인 편지(HTTPS)라면, 가로채도 잠긴 봉투만 보일 뿐이다. 오늘날 거의 모든 사이트가 HTTPS를 쓰는 이유가 여기 있다.</p>
</section>'''

s3 = f'''
<section id="s3" class="beginner-terms summary-card">
  {h2("03","핵심 용어 먼저 정리","reference")}
  <p class="h2-sub">앞으로 나올 단어 네 개만 알면 나머지는 술술 읽힌다.</p>
  <div class="card-grid">
    <article class="term"><span class="label">용어</span><p class="word">암호화(Encryption)</p><p class="meaning">읽을 수 있는 내용을 열쇠 없이는 못 읽는 형태로 바꾸는 것.</p></article>
    <article class="term"><span class="label">용어</span><p class="word">키(Key)</p><p class="meaning">암호를 걸고 푸는 데 쓰는 비밀 값. 자물쇠의 열쇠에 해당.</p></article>
    <article class="term"><span class="label">용어</span><p class="word">인증서(Certificate)</p><p class="meaning">"이 서버는 진짜 OO다"를 증명하는, 신뢰 기관이 발급한 신분증.</p></article>
    <article class="term"><span class="label">용어</span><p class="word">핸드셰이크(Handshake)</p><p class="meaning">본 대화 전에 키와 신원을 합의하는 "사전 인사" 절차.</p></article>
  </div>
  <p>이 네 단어의 관계는 이렇다. 핸드셰이크 동안 인증서로 서버 신원을 확인하고, 안전하게 키를 합의한 뒤, 그 키로 본 대화를 암호화한다. 다음 섹션부터 이 흐름을 하나씩 펼친다.</p>
</section>'''

s4 = f'''
<section id="s4" class="beginner-zero summary-card">
  {h2("04","핸드셰이크 한눈에","connection")}
  <p class="h2-sub">세부에 들어가기 전, 전체 그림을 먼저 본다. 큰 그림이 있으면 단계가 헷갈리지 않는다.</p>
  <section class="vt-shell" aria-label="핸드셰이크 개념">
    <div class="vt-frame"><div class="concept-ring">
      <div class="vt-section-title"><span class="vt-num">?</span><h3 style="margin:0">핸드셰이크는 왜 필요한가</h3></div>
      <p class="vt-text">서로 처음 만난 브라우저와 서버는 "어떤 암호 방식을 쓸지, 상대가 진짜인지, 어떤 비밀 열쇠를 공유할지"를 본 대화 전에 합의해야 합니다. 이 사전 합의가 핸드셰이크입니다.</p>
      <div class="concept-steps">
        <div class="concept-step"><b>1</b>인사·방식 합의</div>
        <div class="concept-step"><b>2</b>신원 확인</div>
        <div class="concept-step"><b>3</b>비밀 키 공유</div>
        <div class="concept-step"><b>4</b>암호 통신 시작</div>
      </div>
    </div></div>
  </section>
  <p>핵심은 "본 대화 전에 한 번만" 일어난다는 점이다. 한 번 키를 합의하고 나면, 이후 실제 데이터는 그 키로 빠르게 암호화해 주고받는다. 인사는 신중하게, 대화는 빠르게 — 이게 HTTPS의 기본 리듬이다.</p>
</section>'''

s5 = f'''
<section id="s5" class="beginner-zero summary-card">
  {h2("05","두 종류의 열쇠","code")}
  <p class="h2-sub">HTTPS의 묘미는 성격이 다른 두 암호를 영리하게 조합한다는 데 있다.</p>
  <div class="grid-2">
    <article class="card-block"><h3>비대칭 키 (공개/개인)</h3><p>자물쇠는 누구나 잠글 수 있게 공개(공개키)하고, 여는 열쇠는 서버만 가진다(개인키). 안전하지만 느리다. 그래서 "비밀 값을 처음 전달"하는 데만 쓴다.</p></article>
    <article class="card-block"><h3>대칭 키 (공유 비밀)</h3><p>잠그고 여는 데 같은 열쇠를 쓴다. 빠르지만, 그 열쇠를 안전하게 나눠 갖는 게 어렵다. 그래서 본 대화의 암호화에 쓴다.</p></article>
  </div>
  <p>조합의 아이디어는 단순하다. <strong>느리지만 안전한 비대칭 키로 "대칭 키 자체"를 안전하게 전달</strong>하고, 그 다음부터는 <strong>빠른 대칭 키로 실제 데이터를 암호화</strong>한다. 안전함과 빠름을 둘 다 가져가는 영리한 거래다. 핸드셰이크가 하는 일의 절반은 바로 이 "대칭 키를 안전하게 합의"하는 것이다.</p>
</section>'''

s6 = f'''
<section id="s6" class="beginner-terms summary-card">
  {h2("06","인증서와 신뢰의 사슬","security")}
  <p class="h2-sub">암호화만으로는 부족하다. "지금 암호로 대화 중인 상대가 진짜인가?"를 보장하는 게 인증서다.</p>
  <p>중간에 누군가 끼어들어 "내가 그 서버야"라고 속이면(중간자 공격), 암호화돼 있어도 그 가짜와 안전하게 대화하는 셈이 된다. 그래서 서버는 신뢰할 수 있는 기관(인증 기관, CA)이 발급한 인증서를 제시한다.</p>
  <div class="analogy"><span class="label">비유</span><p>인증서는 <strong>여권</strong>과 같다. 내가 직접 "나는 OO야"라고 말하면 못 믿지만, 국가(CA)가 발급한 여권을 보이면 믿을 수 있다. 브라우저는 이미 신뢰하는 기관 목록을 갖고 있어, 그 기관이 서명한 인증서면 신원을 인정한다. 기관이 또 상위 기관의 보증을 받는 구조라 "신뢰의 사슬"이라 부른다.</p></div>
  <p>그래서 브라우저가 "이 사이트는 안전하지 않음"이라고 경고하면, 대개 암호화가 깨진 게 아니라 <strong>신원 증명(인증서)에 문제</strong>가 있다는 뜻이다. 만료됐거나, 신뢰받지 못한 기관이 발급했거나, 주소와 인증서의 이름이 다른 경우다.</p>
</section>'''

s7 = f'''
<section id="s7" class="beginner-zero summary-card">
  {h2("07","단계별 흐름 따라가기","flow")}
  <p class="h2-sub">이제 큰 그림을 단계로 펼친다. 박스를 펼쳐 각 단계에서 무슨 일이 일어나는지 확인하자.</p>
  <section class="wg-13-fc" aria-label="TLS 핸드셰이크 흐름">
    <h3 class="wg-13-h">TLS 핸드셰이크 <span class="wg-13-sub">본 대화 시작 전 1회</span></h3>
    <div class="wg-13-flow">
      <a href="#tls-s1" class="wg-13-node wg-13-node--start"><span class="wg-13-step">시작</span>Client Hello</a>
      <span class="wg-13-arrow" aria-hidden="true">&darr;</span>
      <a href="#tls-s2" class="wg-13-node"><span class="wg-13-step">1</span>Server Hello + 인증서</a>
      <span class="wg-13-arrow" aria-hidden="true">&darr;</span>
      <div class="wg-13-branch">
        <a href="#tls-s3" class="wg-13-node wg-13-node--decide"><span class="wg-13-step">2</span>인증서 신뢰되나?</a>
        <div class="wg-13-paths">
          <div class="wg-13-path wg-13-path--fail"><span class="wg-13-edge">아니오 &rarr; 경고</span><a href="#tls-fail" class="wg-13-node wg-13-node--fail"><span class="wg-13-step">!</span>연결 차단·경고</a></div>
          <div class="wg-13-path wg-13-path--ok"><span class="wg-13-edge">예 &rarr; 진행</span><a href="#tls-ok" class="wg-13-node wg-13-node--end"><span class="wg-13-step">완료</span>대칭 키 공유·암호 통신</a></div>
        </div>
      </div>
    </div>
    <div class="wg-13-detail">
      <h4 class="wg-13-dh">단계 상세 <span class="wg-13-dnote">박스를 펼쳐 확인</span></h4>
      <details id="tls-s1" class="wg-13-acc" open><summary><span class="wg-13-tag">시작</span>Client Hello</summary><div class="wg-13-body"><p>브라우저가 "이런 암호 방식들을 쓸 수 있어"라며 후보 목록과 임의 값을 보냅니다.</p></div></details>
      <details id="tls-s2" class="wg-13-acc"><summary><span class="wg-13-tag">1단계</span>Server Hello + 인증서</summary><div class="wg-13-body"><p>서버가 방식 하나를 고르고, 자신의 인증서(여권)를 함께 보냅니다.</p></div></details>
      <details id="tls-fail" class="wg-13-acc wg-13-acc--fail"><summary><span class="wg-13-tag wg-13-tag--fail">실패</span>신뢰 불가</summary><div class="wg-13-body"><p>인증서가 만료·불일치·미신뢰 기관이면 브라우저가 연결을 막고 경고합니다.</p></div></details>
      <details id="tls-ok" class="wg-13-acc wg-13-acc--ok"><summary><span class="wg-13-tag wg-13-tag--ok">완료</span>키 공유·통신</summary><div class="wg-13-body"><p>신뢰되면 대칭 키를 안전하게 합의하고, 이후 실제 데이터를 그 키로 빠르게 암호화합니다.</p></div></details>
    </div>
  </section>
</section>'''

s8 = f'''
<section id="s8" class="beginner-traps summary-card">
  {h2("08","흔한 오해 바로잡기","warning")}
  <p class="h2-sub">초보자가 자주 빠지는 오해 세 가지를 짚는다. 표현이 아니라 개념을 고치는 게 목적이다.</p>
  <ul class="check-list">
    <li><strong>"자물쇠가 있으면 안전한 사이트다"</strong> — 아니다. 자물쇠는 "통신이 암호화됐다"는 뜻이지 "사이트가 선의다"는 보장이 아니다. 피싱 사이트도 HTTPS를 쓸 수 있다.</li>
    <li><strong>"HTTPS면 서버에 저장된 데이터도 안전하다"</strong> — 아니다. HTTPS는 <em>오가는 길</em>을 지킬 뿐, 도착한 서버가 데이터를 어떻게 보관하는지는 별개다.</li>
    <li><strong>"암호화와 인증은 같은 것"</strong> — 다르다. 암호화는 "못 읽게", 인증은 "상대가 진짜인지". HTTPS는 둘을 함께 제공한다.</li>
  </ul>
  <div class="danger"><span class="label">주의</span><p>특히 첫 번째 오해가 위험하다. 자물쇠만 보고 안심하면, 주소가 미묘하게 다른 가짜 사이트(예: 한 글자 다른 도메인)에 비밀번호를 넣을 수 있다. 자물쇠는 "암호화 여부"일 뿐, 주소를 직접 확인하는 습관이 필요하다.</p></div>
</section>'''

s9 = f'''
<section id="s9" class="beginner-practice summary-card">
  {h2("09","직접 확인해 보기","experiment")}
  <p class="h2-sub">읽기만 하면 잊는다. 지금 브라우저로 5분이면 끝나는 두 가지를 직접 해 보자.</p>
  <ol class="practice-list">
    <li><strong>인증서 들여다보기</strong> — 아무 HTTPS 사이트에서 주소창 자물쇠를 클릭해 "인증서" 정보를 연다. 발급 기관(CA), 유효 기간, 대상 도메인을 확인한다. 방금 배운 "여권"의 실물이다.</li>
    <li><strong>경고 만나 보기</strong> — 인증서가 만료됐거나 자체 서명된 테스트 사이트(검색하면 학습용 사이트가 있다)에 접속해, 브라우저가 어떤 경고를 띄우는지 읽어 본다. 경고 문구가 "암호화"가 아니라 "신원"을 말하고 있음을 확인한다.</li>
  </ol>
  <div class="good"><span class="label">팁</span><p>인증서 정보에서 "유효 기간"을 눈여겨보자. 대부분의 인증서는 몇 달~1년 단위로 갱신된다. 사이트 운영자가 갱신을 놓치면, 어느 날 갑자기 "안전하지 않음" 경고가 뜨는 이유가 바로 이것이다.</p></div>
</section>'''

snext = f'''
<section id="snext" class="try">
  {h2(None,"복습 체크리스트","check")}
  <p>아래 질문에 스스로 답할 수 있으면, 자물쇠 아이콘 뒤의 일을 이해한 것이다.</p>
  <div class="cta-box">
    <p><strong>스스로 점검</strong></p>
    <ol><li>HTTPS가 보장하는 두 가지(암호화·인증)를 말할 수 있다.</li><li>비대칭 키와 대칭 키를 왜 함께 쓰는지 설명할 수 있다.</li><li>"안전하지 않음" 경고가 보통 무엇(신원) 때문인지 안다.</li></ol>
    <div class="tag-list"><span class="tag">https</span><span class="tag">tls</span><span class="tag">handshake</span><span class="tag">초보자</span></div>
  </div>
</section>'''

source_note = '<aside class="source-note"><p><strong>범위.</strong> 본 입문은 HTTPS/TLS의 개념을 비유 중심으로 단순화했다. 실제 TLS 1.3은 핸드셰이크를 더 줄이고 순서가 다른 부분이 있으며, 키 합의 방식(예: ECDHE)도 더 정교하다. 더 깊이 들어갈 때는 TLS 1.3 표준 문서를 참고한다.</p></aside>'

body = ('<main id="main" class="page-wide layout-beginner">' + header + toc + s1+s2+s3+s4+s5+s6+s7+s8+s9+snext + source_note + '</main>')
out = build_page("pages/12_beginner_html_https_tls_handshake.html", title=TITLE, description=DESC, body=body)
write_sources()
print("WROTE", out)
