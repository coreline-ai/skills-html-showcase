#!/usr/bin/env python3
"""Mode 11 / 17 — blog_writer (sequential). Topic: 사이드 프로젝트를 6개월 만에 접고 배운 것.
Layout: personal-blog-essay.html (.layout-blog) · auto · vt: timeline(tl-item) · wg: wg-17.
article>section CSS 카운터가 번호를 부여하므로 h2에 .num 미사용(body-icon 유지).
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _finalize import build_page, write_sources, h2, SKILL, ASSETS  # noqa: E402,F401

for _p in [SKILL/"SKILL.md", SKILL/"references/writing-system.md", ASSETS/"layouts/personal-blog-essay.html",
           ASSETS/"visual-html-templates/04-timeline.html", ASSETS/"widget-templates/17-pr-writeup.html"]:
    _p.read_text(encoding="utf-8")

TITLE = "사이드 프로젝트를 6개월 만에 접고 배운 것"
DESC = "야심차게 시작한 사이드 프로젝트를 6개월 만에 종료하며 배운 것 — 시작의 이유, 멈춤의 신호, 매몰비용, 그리고 다음에 다르게 할 것들에 대한 개인 회고."

header = '''
<header class="header blog-header">
  <div class="kicker"><span class="kicker-text">BLOG · MODE 11 / 17 · 독립 빌드</span></div>
  <h1>사이드 프로젝트를 6개월 만에 접었다</h1>
  <p class="sub hook">실패담은 아니다. 다만 "끝내는 결정"이 "시작하는 결정"만큼 중요하다는 걸, 6개월을 쓰고서야 배웠다.</p>
  <div class="meta"><span>profile auto</span><span>layout personal-blog-essay</span><span>개인 회고</span><span>읽는 시간 약 7분</span></div>
  <div class="generated-row"><p class="generated-date">Generated · 2026-06-13 KST</p>
  <div class="lens-strip" aria-label="적용 렌즈"><span class="lens-strip-label">LENS</span><span class="lens-chip">동기</span><span class="lens-chip">신호</span><span class="lens-chip">매몰비용</span><span class="lens-chip">교훈</span><span class="lens-chip">솔직함</span></div></div>
</header>'''

personal = '<aside class="box personal-note"><p><strong>미리 밝혀 둘 것.</strong> 이 글은 "사이드 프로젝트 하지 마세요"가 아니다. 오히려 더 잘, 더 가볍게, 그리고 멈출 줄도 알면서 하자는 이야기다.</p></aside>'

toc = '''
<nav class="toc-map blog-toc" aria-label="글 목차"><div class="toc-pills">
  <a class="toc-pill" href="#s1"><b>01</b> 왜 지금 이 글을</a><a class="toc-pill" href="#s2"><b>02</b> 왜 시작했나</a>
  <a class="toc-pill" href="#s3"><b>03</b> 6개월의 타임라인</a><a class="toc-pill" href="#s4"><b>04</b> 멈춰야 한다는 신호</a>
  <a class="toc-pill" href="#s5"><b>05</b> 내가 오판한 것</a><a class="toc-pill" href="#s6"><b>06</b> 매몰비용의 무게</a>
  <a class="toc-pill" href="#s7"><b>07</b> 종료를 PR처럼</a><a class="toc-pill" href="#s8"><b>08</b> 다음엔 다르게</a>
  <a class="toc-pill" href="#s9"><b>09</b> 남은 생각</a><a class="toc-pill" href="#snext"><b>→</b> 비슷한 당신에게</a>
</div></nav>'''

s1 = f'''<section id="s1">
  {h2(None,"왜 지금 이 글을 쓰나","quote")}
  <p>프로젝트를 접은 지 한 달이 지났다. 처음엔 부끄러워서 아무 말도 안 했는데, 정리하다 보니 "끝내는 법을 몰랐던 게 진짜 문제였구나" 싶었다. 시작에 대한 글은 넘치는데, 잘 끝내는 법에 대한 글은 드물다. 그래서 기록을 남긴다.</p>
  <p>6개월 동안 주말과 새벽을 갈아 넣었다. 결과물은 살아남지 못했지만, 그 시간이 통째로 손해는 아니었다. 다만 같은 교훈을 더 싸게 배울 수 있었다는 게 아쉬울 뿐이다. 이 글은 그 "더 싼 학습"을 누군가에게 미리 넘겨주려는 시도다.</p>
</section>'''

s2 = f'''<section id="s2">
  {h2(None,"왜 시작했나","idea")}
  <p>출발은 흔한 가려움이었다. 내가 매일 쓰는 도구에 작은 불편이 있었고, "이 정도는 주말에 만들겠는데?"라고 생각했다. 문제 정의는 명확했고, 첫 두 주는 짜릿했다. 동작하는 프로토타입이 나왔고, 친구 몇 명이 "오 이거 좋다"고 했다.</p>
  <p>지금 돌아보면 그 "좋다"가 함정이었다. 칭찬과 사용은 다른 일이다. 나는 "쓰겠다"는 말과 "써 봤다"는 행동을 구분하지 않았고, 사회적 호응을 시장 신호로 착각했다. 시작의 동기는 진심이었지만, 검증의 기준은 처음부터 허술했다. 돌이켜 보면 첫 두 주의 짜릿함은 "사용자가 생겼다"가 아니라 "내가 만들고 싶은 걸 만들고 있다"는 만족감이었다. 둘은 닮았지만 전혀 다른 감정이고, 그 차이를 일찍 구분했다면 방향이 달라졌을 것이다.</p>
</section>'''

s3 = f'''<section id="s3">
  {h2(None,"6개월의 타임라인","timeline")}
  <p>한 달 단위로 무슨 일이 있었는지 압축하면 이렇다. 흥미롭게도 위험 신호는 3개월 차에 이미 다 나와 있었다.</p>
  <section class="vt-shell" aria-label="6개월 타임라인">
    <div class="vt-frame"><ol class="tl">
      <li class="tl-item"><b>1~2개월</b><p class="vt-text">프로토타입 완성, 지인 피드백에 고무됨. 기능 추가에 몰두.</p></li>
      <li class="tl-item"><b>3개월</b><p class="vt-text">베타 공개. 가입은 늘었지만 재방문이 없음. 첫 위험 신호.</p></li>
      <li class="tl-item"><b>4~5개월</b><p class="vt-text">"기능이 부족해서겠지" 하며 더 만듦. 재방문은 그대로.</p></li>
      <li class="tl-item"><b>6개월</b><p class="vt-text">번아웃과 함께 직시. 핵심 가치가 약했음을 인정하고 종료 결정.</p></li>
    </ol></div>
  </section>
  <p>가장 뼈아픈 건 4~5개월이다. 3개월 차 신호(재방문 없음)를 보고도, 나는 "기능을 더 만들면 해결된다"는 익숙한 답으로 도망쳤다. 만드는 일은 즐겁고, 직시하는 일은 불편하기 때문이다.</p>
</section>'''

s4 = f'''<section id="s4">
  {h2(None,"멈춰야 한다는 신호","warning")}
  <p>지나고 보니 신호는 분명했다. 문제는 신호가 없던 게 아니라, 내가 보고 싶은 것만 봤다는 데 있었다.</p>
  <div class="grid-2">
    <article class="danger"><span class="label">무시한 신호</span><p>가입 후 일주일 내 재방문율이 한 자릿수. "온보딩이 문제겠지"로 미뤘지만, 사실은 다시 올 이유 자체가 약했다.</p></article>
    <article class="danger"><span class="label">합리화</span><p>"아직 입소문이 안 나서", "기능이 부족해서". 모두 내가 더 만들 핑계였지, 가설을 검증하는 질문이 아니었다.</p></article>
  </div>
  <p>멈춤의 신호는 대개 "더 노력하라"가 아니라 "가설이 틀렸다"고 말한다. 그런데 노력은 내가 통제할 수 있고 가설 수정은 자존심이 상하니, 사람은 자연히 노력 쪽으로 도망친다. 그게 6개월을 끌게 만든 진짜 원인이었다. 신호를 읽는 데 필요한 건 더 많은 데이터가 아니라 "내가 듣기 싫은 답을 받아들일 준비"였다. 재방문율이라는 한 줄 숫자는 처음부터 명확하게 말하고 있었는데, 나는 그 숫자 대신 가입자 수라는 듣기 좋은 숫자만 쳐다봤다.</p>
</section>'''

s5 = f'''<section id="s5">
  {h2(None,"내가 오판한 것","decision")}
  <p>오판은 기술이 아니라 판단에 있었다. 세 가지를 꼽을 수 있다.</p>
  <div class="card-grid">
    <article class="mini-card"><h3>칭찬 = 수요</h3><p>지인의 "좋다"를 수요로 읽었다. 돈을 내거나 매일 쓰는 행동만이 진짜 신호였다.</p></article>
    <article class="mini-card"><h3>기능 = 가치</h3><p>가치가 약한 걸 기능 수로 메우려 했다. 핵심 가치가 약하면 기능은 무게만 늘린다.</p></article>
    <article class="mini-card"><h3>바쁨 = 진전</h3><p>커밋 수와 진전을 혼동했다. 코드는 늘었지만 사용자의 문제는 그대로였다.</p></article>
  </div>
  <p>세 오판의 공통점은 "측정하기 쉬운 것"을 "중요한 것"으로 바꿔치기한 것이다. 칭찬·기능·커밋은 세기 쉽고, 재방문·지불·문제 해결은 세기 불편하다. 불편한 지표를 외면한 대가가 6개월이었다.</p>
</section>'''

s6 = f'''<section id="s6">
  {h2(None,"매몰비용의 무게","impact")}
  <p>"여기까지 했는데" — 이 한 문장이 가장 비쌌다. 이미 쓴 시간은 돌아오지 않는데, 그 시간이 오히려 멈추지 못하게 붙잡았다.</p>
  <p>경제학에서 매몰비용은 의사결정에서 무시해야 할 비용이라고 배운다. 머리로는 안다. 그런데 그 6개월이 내 주말과 자존심으로 이뤄져 있으면, 무시가 안 된다. "이만큼 했으니 조금만 더"가 반복되면서, 손절선이 계속 뒤로 밀렸다.</p>
  <div class="good"><span class="label">배운 것</span><p>그래서 다음엔 시작할 때 <strong>멈출 조건을 미리 적어 둘 것</strong>이다. "3개월 차 재방문율이 X% 미만이면 접는다" 같은 선을 감정이 개입하기 전에 정해 두면, 매몰비용이 판단을 흐리는 걸 막을 수 있다.</p></div>
</section>'''

s7 = f'''<section id="s7">
  {h2(None,"종료를 PR처럼 정리하기","edit")}
  <p>접기로 한 뒤, 코드 PR을 정리하듯 프로젝트의 종료도 문서로 남겼다. 감정이 아니라 사실로 닫고 싶었다.</p>
  <section class="wg-17" aria-labelledby="m11-pr-title">
    <header class="wg-17-head"><p class="wg-17-kicker">RETRO · close-out</p><h2 id="m11-pr-title" class="wg-17-title">chore: 사이드 프로젝트 종료 및 회고</h2><div class="wg-17-meta"><span class="wg-17-chip wg-17-chip-branch">side-project → archive</span><span class="wg-17-chip">기간 6개월</span><span class="wg-17-chip wg-17-chip-del">−번아웃</span></div></header>
    <div class="wg-17-block"><h3 class="wg-17-h3"><span class="wg-17-h3-no">1</span> 무엇을 시도했나</h3><p class="wg-17-p">매일 쓰는 도구의 작은 불편을 해결하는 웹 서비스. 프로토타입·베타까지 도달했으나 재방문이 확보되지 않았다.</p></div>
    <div class="wg-17-block"><h3 class="wg-17-h3"><span class="wg-17-h3-no">2</span> 무엇을 배웠나</h3><div class="wg-17-ba">
      <div class="wg-17-ba-col wg-17-ba-before"><p class="wg-17-ba-tag">처음 믿음</p><ul class="wg-17-ba-list"><li>좋다는 말 = 수요</li><li>기능이 많으면 쓴다</li><li>열심히 = 전진</li></ul></div>
      <div class="wg-17-ba-arrow" aria-hidden="true">→</div>
      <div class="wg-17-ba-col wg-17-ba-after"><p class="wg-17-ba-tag">지금 믿음</p><ul class="wg-17-ba-list"><li>지불·재방문만 신호</li><li>핵심 가치 먼저</li><li>멈출 조건을 먼저 정함</li></ul></div>
    </div></div>
    <div class="wg-17-block"><h3 class="wg-17-h3"><span class="wg-17-h3-no">3</span> 무엇을 남겼나</h3><p class="wg-17-p">코드는 공개 아카이브로, 배운 점은 이 글로 남긴다. 다음 프로젝트의 "멈춤 조건 템플릿"도 함께 정리했다.</p></div>
  </section>
</section>'''

s8 = f'''<section id="s8">
  {h2(None,"다음엔 다르게","check")}
  <p>다음 프로젝트가 있다면, 이 세 가지는 반드시 다르게 할 것이다.</p>
  <ul class="check-list">
    <li><strong>가설 먼저, 코드 나중</strong> — "누가 왜 이걸 매일 쓸까"를 코드 한 줄 전에 5명에게 물어본다.</li>
    <li><strong>멈춤 조건 명문화</strong> — 시작과 동시에 "이 지표가 이 선 아래면 접는다"를 적어 둔다.</li>
    <li><strong>가볍게 검증</strong> — 완성품이 아니라 가장 작은 검증 가능한 형태로, 한 달 안에 신호를 본다.</li>
  </ul>
  <p>요약하면 "더 빨리 틀리기"다. 6개월에 걸쳐 비싸게 틀리는 대신, 한 달 안에 싸게 틀리고 방향을 바꾸는 것. 사이드 프로젝트의 진짜 자산은 결과물이 아니라 이 학습 속도다. 세 가지 모두 "코드를 덜 쓰고 사람을 더 만나는" 방향을 가리킨다. 엔지니어에게 가장 어려운 일은 사실 코드를 안 쓰는 것이다 — 만드는 일은 통제 가능하고 즐겁지만, 사람에게 묻고 거절당하는 일은 불확실하고 불편하기 때문이다. 그 불편함을 앞당겨 겪는 것이 결국 가장 싼 학습이다.</p>
</section>'''

s9 = f'''<section id="s9">
  {h2(None,"남은 생각","quote")}
  <p>접고 나니 의외로 후회는 없다. 6개월의 시간은 결과물 대신 "판단 근육"을 남겼다. 다음엔 더 빨리 신호를 읽고, 더 일찍 방향을 틀고, 필요하면 더 담담하게 멈출 수 있을 것이다.</p>
  <p>그리고 무엇보다, 끝내는 일을 부끄러워하지 않게 됐다. 잘 끝낸 프로젝트는 실패가 아니라 학습이다. 시작만큼 멈춤도 실력이라는 것 — 그게 6개월이 내게 준 가장 비싼, 그러나 값진 교훈이다. 누군가는 "그래도 6개월이 아깝지 않냐"고 묻는다. 아깝다. 하지만 그 아까움 때문에 7개월, 8개월을 더 쓰는 것이야말로 진짜 손해다. 멈춤은 과거를 부정하는 게 아니라, 남은 시간을 더 나은 곳에 쓰겠다는 선택이다.</p>
</section>'''

snext = f'''
<section id="snext" class="try soft-cta">
  {h2(None,"비슷한 고민 중인 당신에게","landing")}
  <p>지금 사이드 프로젝트를 붙잡고 있고, "조금만 더"를 반복하고 있다면, 잠깐 멈춰서 한 가지만 적어 보길 권한다.</p>
  <div class="cta-box">
    <p><strong>오늘 적어 볼 한 줄</strong> — "이 프로젝트는 OO 지표가 OO 아래로 OO 기간 지속되면 접는다."</p>
    <p>이 한 줄을 감정이 개입하기 전에 적어 두면, 나처럼 6개월을 쓰지 않아도 된다. 멈춤의 기준을 미리 가진 사람만이 끝까지 가볼지, 일찍 접을지를 자유롭게 선택할 수 있다.</p>
    <div class="tag-list"><span class="tag">side-project</span><span class="tag">회고</span><span class="tag">매몰비용</span><span class="tag">멈춤의 기술</span></div>
  </div>
</section>'''

source_note = '<aside class="source-note"><p><strong>밝혀 둘 것.</strong> 개인 경험에 기반한 회고이며, 일반적 조언으로 일반화하기 어려운 부분이 있다. 수치(재방문율 등)는 구체값 대신 추세로만 적었다. 같은 상황이라도 결론은 사람·시장마다 다를 수 있다.</p></aside>'

body = ('<main id="main" class="page-wide layout-blog">' + header + personal + toc + '<article>' + s1+s2+s3+s4+s5+s6+s7+s8+s9 + '</article>' + snext + source_note + '</main>')
out = build_page("pages/11_blog_writer_side_project_retro.html", title=TITLE, description=DESC, body=body)
write_sources()
print("WROTE", out)
