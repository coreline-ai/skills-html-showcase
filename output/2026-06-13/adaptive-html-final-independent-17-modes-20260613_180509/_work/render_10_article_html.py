#!/usr/bin/env python3
"""Mode 10 / 17 — article_html (sequential). Topic: 관측 가능성은 로그를 모으는 일이 아니다.
Layout: magazine-article.html (.layout-article) · auto · vt: decision-tree(dt-q,dt-options) · wg: wg-14.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _finalize import build_page, write_sources, h2, SKILL, ASSETS  # noqa: E402,F401

for _p in [SKILL/"SKILL.md", SKILL/"references/writing-system.md", ASSETS/"layouts/magazine-article.html",
           ASSETS/"visual-html-templates/02-decision-tree.html", ASSETS/"widget-templates/14-feature-explainer.html"]:
    _p.read_text(encoding="utf-8")

TITLE = "관측 가능성은 로그를 모으는 일이 아니다"
DESC = "로그·메트릭·트레이스를 쌓는 것과 시스템에 질문할 수 있는 능력은 다르다. 관측 가능성을 '미지의 질문에 답하는 능력'으로 다시 정의하는 공개 아티클."

JSON_LD = '<script type="application/ld+json">{"@context":"https://schema.org","@type":"Article","headline":"관측 가능성은 로그를 모으는 일이 아니다","inLanguage":"ko"}</script>'

header = '''
<header class="header article-header">
  <div class="kicker"><span class="kicker-text">ARTICLE · MODE 10 / 17 · 독립 빌드</span></div>
  <h1>관측 가능성은 '로그를 모으는 일'이 아니다</h1>
  <p class="sub lead">대시보드가 늘어날수록 장애는 더 빨리 해결될까? 신호를 쌓는 것과 시스템에 질문할 수 있는 것은 전혀 다른 능력이다.</p>
  <div class="meta"><span>profile auto</span><span>layout magazine-article</span><span>공개 아티클</span><span>읽는 시간 약 8분</span></div>
  <div class="generated-row"><p class="generated-date">Generated · 2026-06-13 KST</p>
  <div class="lens-strip" aria-label="적용 렌즈"><span class="lens-strip-label">LENS</span><span class="lens-chip">정의</span><span class="lens-chip">반례</span><span class="lens-chip">사례</span><span class="lens-chip">실천</span><span class="lens-chip">비용</span></div></div>
</header>'''

pull = '<aside class="pull-quote">"좋은 관측 가능성은 데이터의 양이 아니라, 미리 정의하지 않은 질문에 사후에 답할 수 있는가로 판가름난다."</aside>'

toc = '''
<nav class="toc-map article-toc" aria-label="아티클 목차"><div class="toc-pills">
  <a class="toc-pill" href="#s1"><b>01</b> 대시보드의 역설</a><a class="toc-pill" href="#s2"><b>02</b> 모니터링과의 차이</a>
  <a class="toc-pill" href="#s3"><b>03</b> 무엇을 계측할까</a><a class="toc-pill" href="#s4"><b>04</b> 세 신호의 역할</a>
  <a class="toc-pill" href="#s5"><b>05</b> 카디널리티 함정</a><a class="toc-pill" href="#s6"><b>06</b> 질문 가능하게</a>
  <a class="toc-pill" href="#s7"><b>07</b> 새벽 3시의 사례</a><a class="toc-pill" href="#s8"><b>08</b> 비용과 안티패턴</a>
  <a class="toc-pill" href="#s9"><b>09</b> 핵심 정리</a><a class="toc-pill" href="#snext"><b>→</b> 다음 한 걸음</a>
</div></nav>'''

s1 = f'''
<section id="s1" class="summary-card">
  {h2("01","대시보드의 역설","quote")}
  <p class="h2-sub">대시보드가 30개로 늘었는데 장애 해결은 더 느려졌다. 이 역설이 관측 가능성을 다시 생각하게 만든다.</p>
  <p>많은 팀이 모니터링에 투자하면서 같은 경험을 한다. 그래프는 많아지는데, 정작 장애가 터지면 "어느 대시보드를 봐야 하지?"부터 막힌다. 신호는 넘치지만 답은 없다. 데이터를 쌓는 것과 데이터에 질문하는 것이 다른 일이기 때문이다.</p>
  <p>관측 가능성(observability)은 제어 이론에서 온 말로, "외부 출력만 보고 시스템 내부 상태를 추정할 수 있는 정도"를 뜻한다. 소프트웨어로 옮기면 이렇게 된다 — <strong>운영 중 마주친 처음 보는 문제를, 코드를 새로 배포하지 않고도 기존 신호만으로 진단할 수 있는가.</strong> 이 정의가 핵심이다. 이 기준에서 보면 대시보드 개수는 관측 가능성의 척도가 아니다. 대시보드 30개는 "우리가 미리 예상한 30가지 질문"에 답할 뿐이고, 정작 장애는 늘 예상 밖의 31번째 질문으로 온다. 그 31번째 질문에 사후에 답할 수 있느냐가 관측 가능성의 진짜 시험대다.</p>
</section>'''

s2 = f'''
<section id="s2" class="summary-card">
  {h2("02","모니터링과 무엇이 다른가","idea")}
  <p class="h2-sub">모니터링은 "알고 있는 것"을 감시하고, 관측 가능성은 "모르는 것"을 탐구한다.</p>
  <div class="grid-2">
    <article class="card-block"><h3>모니터링</h3><p>미리 정의한 임계치를 지킨다. "CPU 80% 넘으면 알림." 알려진 실패 모드(known-unknowns)에 강하다. 질문이 미리 정해져 있다.</p></article>
    <article class="card-block"><h3>관측 가능성</h3><p>예상 못 한 조합을 사후에 탐색한다. "왜 이 특정 고객의 특정 엔드포인트만 느릴까?" 미지의 실패(unknown-unknowns)에 답한다.</p></article>
  </div>
  <p>둘은 대립이 아니라 층위다. 모니터링은 "불이 났는지" 알려 주고, 관측 가능성은 "왜, 어디서 났는지" 묻게 해 준다. 모니터링만 있으면 알림은 울리는데 원인 추적에서 막히고, 관측 가능성이 받쳐 줄 때 비로소 알림이 진단으로 이어진다.</p>
</section>'''

s3 = f'''
<section id="s3" class="summary-card">
  {h2("03","무엇을 계측할까 — 결정 흐름","decision")}
  <p class="h2-sub">"전부 다 기록하자"는 비용으로 무너진다. 무엇을 계측할지 결정하는 분기를 따라가 보자.</p>
  <section class="vt-shell" aria-label="계측 대상 결정 트리">
    <div class="vt-frame"><div class="vt-demo">
      <div class="dt-q">
        <article class="dt-card"><div class="vt-kicker">Q1</div><h3>장애 시 이 신호로 답할 질문이 있나?</h3><p class="vt-text">없다면 그 신호는 노이즈일 가능성이 높다.</p></article>
        <div class="dt-arrow"></div>
        <article class="dt-card"><div class="vt-kicker">Q2</div><h3>고차원 맥락이 붙는가?</h3><p class="vt-text">user_id·endpoint·version 같은 차원이 있어야 좁힐 수 있다.</p></article>
        <div class="dt-arrow"></div>
        <article class="dt-card"><div class="vt-kicker">Q3</div><h3>비용을 감당할 카디널리티인가?</h3><p class="vt-text">무한 차원은 저장·질의 비용을 폭발시킨다.</p></article>
      </div>
      <div class="dt-options">
        <article class="dt-card"><b>메트릭</b><p class="vt-text">집계·추세·알림</p></article>
        <article class="dt-card" style="--c:var(--vt-gold)"><b>로그</b><p class="vt-text">개별 사건의 맥락</p></article>
        <article class="dt-card" style="--c:var(--vt-green)"><b>트레이스</b><p class="vt-text">요청의 전 경로</p></article>
      </div>
    </div></div>
  </section>
  <p>결정의 핵심 질문은 하나다. "이 신호로 어떤 질문에 답할 것인가?" 답할 질문이 없는 신호는 비용만 먹는 노이즈다. 계측은 데이터 수집이 아니라 질문 설계에서 시작한다.</p>
</section>'''

s4 = f'''
<section id="s4" class="summary-card">
  {h2("04","세 신호의 역할 분담","metric")}
  <p class="h2-sub">메트릭·로그·트레이스는 경쟁이 아니라 분업이다. 각자 잘하는 질문이 다르다.</p>
  <div class="table-scroll"><table>
    <caption>세 신호의 강점과 답하는 질문</caption>
    <thead><tr><th>신호</th><th>강점</th><th>답하는 질문</th><th>약점</th></tr></thead>
    <tbody>
      <tr><th>메트릭</th><td>저비용 집계·추세</td><td>"전체적으로 나빠졌나?"</td><td>개별 사건 추적 불가</td></tr>
      <tr><th>로그</th><td>개별 사건의 풍부한 맥락</td><td>"이 요청에 무슨 일이?"</td><td>양이 많고 검색 비용↑</td></tr>
      <tr><th>트레이스</th><td>서비스 경계 넘는 경로</td><td>"어느 구간이 느린가?"</td><td>샘플링·계측 부담</td></tr>
    </tbody>
  </table></div>
  <p>흔한 실수는 한 신호로 모든 걸 하려는 것이다. 로그로 추세를 보려다 비용이 폭발하고, 메트릭으로 개별 사건을 추적하려다 좌절한다. 좋은 관측 설계는 "전체는 메트릭으로 알아채고, 트레이스로 구간을 좁히고, 로그로 사건을 확정하는" 흐름을 만든다.</p>
</section>'''

s5 = f'''
<section id="s5" class="summary-card">
  {h2("05","카디널리티라는 함정","experiment")}
  <p class="h2-sub">관측 가능성의 힘은 '차원'에서 나오지만, 같은 차원이 비용을 폭발시키는 양날의 검이다.</p>
  <p>관측 가능성이 강력한 이유는 신호에 고차원 맥락(user_id, endpoint, region, version…)을 붙일 수 있기 때문이다. 이 차원들 덕에 "특정 버전 × 특정 리전의 특정 고객"으로 문제를 좁힐 수 있다. 그런데 바로 그 차원이 카디널리티(고유 조합 수)를 만든다.</p>
  <div class="danger"><span class="label">함정</span><p>user_id를 메트릭 레이블로 붙이면, 사용자 수만큼 시계열이 생긴다. 100만 사용자면 100만 개의 시계열 — 저장·질의 비용이 선형이 아니라 폭발적으로 증가한다. "맥락은 풍부할수록 좋다"는 직관이 비용 앞에서 깨지는 지점이다.</p></div>
  <p>해법은 신호별로 차원을 다르게 두는 것이다. 메트릭에는 저카디널리티 차원(region, status_class)만, 고카디널리티 맥락(user_id, trace_id)은 로그·트레이스에 둔다. 차원을 어디에 둘지가 곧 비용을 어디에 둘지의 결정이다.</p>
</section>'''

s6 = f'''
<section id="s6" class="summary-card">
  {h2("06","한 기능을 '질문 가능하게' 만들기","flow")}
  <p class="h2-sub">추상론을 한 기능에 적용해 보자. 결제 승인 API를 관측 가능하게 만드는 구체적 방법이다.</p>
  <section class="wg-14" aria-labelledby="m10-wg14-title">
    <p class="wg-14-kicker">관측 설계 · 결제 승인 API</p>
    <h2 id="m10-wg14-title" class="wg-14-h">결제 승인을 질문 가능하게</h2>
    <p class="wg-14-lead">"왜 이 결제만 느렸나"에 사후에 답할 수 있도록 신호를 설계합니다.</p>
    <div class="wg-14-tldr" role="note" aria-label="핵심 요약"><span class="wg-14-tldr-tag">TL;DR</span><p class="wg-14-tldr-body"><strong>요청마다 trace_id를 발급</strong>하고, 외부 PG 호출·DB 쓰기를 스팬으로 나누면 "어느 구간이 느린지"가 사후에 보입니다.</p></div>
    <div class="wg-14-acc">
      <details class="wg-14-sec" open><summary class="wg-14-sum"><span class="wg-14-sum-no">01</span> 어떤 질문에 답할까 <span class="wg-14-chev" aria-hidden="true"></span></summary><div class="wg-14-sec-body"><p>"특정 카드사·특정 시간대·특정 금액대 결제가 느린가?"에 답하는 것이 목표입니다.</p><ul class="wg-14-list"><li>PG사·결과코드를 저카디널리티 메트릭 레이블로</li><li>trace_id·user_id는 트레이스/로그 맥락으로</li><li>외부 호출 구간을 별도 스팬으로 분리</li></ul></div></details>
      <details class="wg-14-sec"><summary class="wg-14-sum"><span class="wg-14-sum-no">02</span> 사후 디버깅 흐름 <span class="wg-14-chev" aria-hidden="true"></span></summary><div class="wg-14-sec-body"><ol class="wg-14-flow"><li><span class="wg-14-flow-n">1</span> 메트릭에서 "PG-A 결과코드 지연 상승" 포착</li><li><span class="wg-14-flow-n">2</span> 트레이스로 외부 호출 구간이 병목임을 확인</li><li><span class="wg-14-flow-n">3</span> 로그로 해당 요청의 재시도 패턴 확정</li></ol></div></details>
    </div>
  </section>
</section>'''

s7 = f'''
<section id="s7" class="summary-card">
  {h2("07","새벽 3시의 사례","case")}
  <p class="h2-sub">정의가 추상적이라면, 같은 장애를 두 방식으로 겪어 보면 차이가 분명해진다.</p>
  <div class="grid-2">
    <article class="danger"><span class="label">관측 가능성 없이</span><p>"결제가 느리다"는 알림. 대시보드 30개를 차례로 열며 추측. CPU·메모리·네트워크 모두 정상. 결국 "재시작하니 됐다"로 끝나고 원인은 미궁. 다음 주 재발.</p></article>
    <article class="good"><span class="label">관측 가능성 있게</span><p>알림에서 트레이스로 점프 → PG-A 호출 구간만 6초로 튐 → 로그에서 타임아웃 후 3회 재시도 확인 → PG-A 장애로 특정 → 라우팅 우회로 5분 내 완화. 원인이 기록으로 남음.</p></article>
  </div>
  <p>차이는 "재시작했더니 됐다"와 "PG-A 장애였고 우회했다" 사이에 있다. 전자는 같은 장애를 또 겪고, 후자는 같은 장애를 두 번 겪지 않는다. 관측 가능성의 ROI는 바로 이 "재발 방지"에서 나온다. 그리고 이 차이를 만든 것은 더 많은 대시보드가 아니라, 요청마다 trace_id를 심고 외부 호출을 별도 스팬으로 나눠 둔 단 하나의 설계 결정이었다. 관측 가능성은 사고가 터진 뒤가 아니라, 평온할 때 무엇을 질문 가능하게 심어 둘지 결정하는 데서 갈린다.</p>
</section>'''

s8 = f'''
<section id="s8" class="summary-card">
  {h2("08","비용과 안티패턴","warning")}
  <p class="h2-sub">관측 가능성도 과하면 독이다. 흔한 안티패턴 세 가지를 경계하자.</p>
  <div class="card-grid">
    <article class="mini-card"><h3>전부 기록</h3><p>"혹시 모르니 다 남기자"는 저장 비용을 폭발시키고 정작 검색을 느리게 만든다. 질문 없는 신호는 끈다.</p></article>
    <article class="mini-card"><h3>대시보드 과잉</h3><p>대시보드 수가 곧 성숙도라는 착각. 아무도 안 보는 대시보드는 인지 부하만 늘린다.</p></article>
    <article class="mini-card"><h3>알림 피로</h3><p>임계치 남발로 알림이 노이즈가 되면, 진짜 알림도 무시된다. 알림은 행동 가능한 것만.</p></article>
  </div>
  <p>좋은 관측 가능성은 "더 많이"가 아니라 "더 답할 수 있게"다. 신호의 가치는 양이 아니라 그것이 답하는 질문의 수로 측정해야 한다. 분기마다 "안 보는 대시보드·안 쓰는 신호"를 정리하는 것도 설계의 일부다.</p>
</section>'''

s9 = f'''
<section id="s9" class="box article-takeaway summary-card">
  {h2("09","핵심 정리","check")}
  <p class="h2-sub">긴 글을 세 문장으로 압축한다.</p>
  <ul class="check-list">
    <li><strong>정의</strong> — 관측 가능성은 데이터의 양이 아니라, 미리 정의하지 않은 질문에 사후에 답하는 능력이다.</li>
    <li><strong>분업</strong> — 메트릭으로 알아채고, 트레이스로 좁히고, 로그로 확정한다. 한 신호로 다 하려 하지 않는다.</li>
    <li><strong>비용</strong> — 힘의 원천(차원)이 곧 비용의 원천(카디널리티)이다. 차원을 어디에 둘지가 설계의 핵심이다.</li>
  </ul>
</section>'''

snext = f'''
<section id="snext" class="try">
  {h2(None,"다음 한 걸음","landing")}
  <p>이론보다 한 번의 실천이 낫다. 가장 자주 장애가 나는 엔드포인트 하나를 골라 "질문 가능하게" 만들어 보자.</p>
  <div class="cta-box">
    <p><strong>이번 주에 할 일</strong></p>
    <ol><li>최근 장애 1건을 골라 "그때 어떤 신호가 있었으면 5분 만에 풀렸을까"를 적는다.</li><li>그 질문에 답하는 차원(레이블/스팬)을 한 엔드포인트에 추가한다.</li><li>다음 장애에서 그 신호로 실제로 답이 되는지 검증한다.</li></ol>
    <div class="tag-list"><span class="tag">observability</span><span class="tag">metrics</span><span class="tag">tracing</span><span class="tag">SRE</span></div>
  </div>
</section>'''

source_note = '<aside class="source-note"><p><strong>출처·관점.</strong> 본 글은 관측 가능성에 대한 일반적 업계 정의(제어 이론 유래, 세 신호 모델)와 운영 경험을 바탕으로 한 의견 글이다. 사례의 수치·상황은 설명을 위한 대표 시나리오이며 특정 사건을 지칭하지 않는다.</p></aside>'

body = ('<main id="main" class="page-wide layout-article">' + header + pull + toc + s1+s2+s3+s4+s5+s6+s7+s8+s9+snext + source_note + '</main>')
out = build_page("pages/10_article_html_observability.html", title=TITLE, description=DESC, body=body, json_ld=JSON_LD)
write_sources()
print("WROTE", out)
