#!/usr/bin/env python3
"""Mode 07 / 17 — youtube_analysis (sequential). Topic: "프로덕션 LLM 비용 70% 절감" 토크 분석 (URL-only tier).
Layout: youtube-analysis.html (.layout-youtube) · auto · vt: timeline(tl-item) · wg: wg-13. iframe/embed 금지.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _finalize import build_page, write_sources, h2, SKILL, ASSETS  # noqa: E402,F401

for _p in [SKILL/"SKILL.md", SKILL/"references/youtube-analysis-system.md", ASSETS/"layouts/youtube-analysis.html",
           ASSETS/"visual-html-templates/04-timeline.html", ASSETS/"widget-templates/13-annotated-flowchart.html"]:
    _p.read_text(encoding="utf-8")

TITLE = "LLM 비용 70% 절감 토크 영상 분석 — 근거 우선"
DESC = "'프로덕션 LLM 비용을 70% 줄인 방법' 컨퍼런스 토크를 입력 tier(URL/메타데이터)에 맞춰 FACT/INFERENCE/UNKNOWN으로 분리 분석한 youtube_analysis 리포트. 트랜스크립트 미확보 한계를 명시한다."

header = '''
<header class="header youtube-header">
  <div class="kicker"><span class="kicker-text">YOUTUBE ANALYSIS · MODE 07 / 17 · 독립 빌드</span></div>
  <h1>LLM 비용 70% 절감 토크, 근거 우선 분석</h1>
  <p class="sub">"프로덕션 LLM 비용을 70% 줄인 방법"이라는 컨퍼런스 토크 영상을 분석한다. 단, 입력은 URL·메타데이터 수준이라 영상 내용을 사실처럼 생성하지 않고 확인 가능/불가를 엄격히 나눈다.</p>
  <div class="meta"><span>profile auto</span><span>layout youtube-analysis</span><span>입력 tier: URL·메타데이터</span><span>분석 기준 시각 2026-06-13 KST</span></div>
  <div class="generated-row"><p class="generated-date">Generated · 2026-06-13 KST</p>
  <div class="lens-strip" aria-label="적용 렌즈"><span class="lens-strip-label">LENS</span><span class="lens-chip">FACT</span><span class="lens-chip">INFERENCE</span><span class="lens-chip">UNKNOWN</span><span class="lens-chip">콘텐츠 갭</span><span class="lens-chip">재가공</span></div></div>
</header>'''

toc = '''
<nav class="toc-map youtube-question-toc" aria-label="YouTube 분석 목차"><div class="toc-pills">
  <a class="toc-pill" href="#s1"><b>01</b> 시청 판정</a><a class="toc-pill" href="#s2"><b>02</b> 출처·신뢰 스냅샷</a>
  <a class="toc-pill" href="#s3"><b>03</b> TL;DW·시청 결정</a><a class="toc-pill" href="#s4"><b>04</b> 영상 근거 지도</a>
  <a class="toc-pill" href="#s5"><b>05</b> 챕터·리텐션 가설</a><a class="toc-pill" href="#s6"><b>06</b> 댓글 신호</a>
  <a class="toc-pill" href="#s7"><b>07</b> 콘텐츠 갭→제작 흐름</a><a class="toc-pill" href="#s8"><b>08</b> 주장·근거·리스크</a>
  <a class="toc-pill" href="#s9"><b>09</b> 후속 영상 설계</a><a class="toc-pill" href="#s10"><b>10</b> 출처 한계</a>
  <a class="toc-pill" href="#snext"><b>→</b> 다음 행동</a>
</div></nav>'''

s1 = f'''
<section id="s1" class="youtube-verdict summary-card">
  {h2("01","시청 판정","audit")}
  <p class="h2-sub">결론부터: 제목의 "70%"는 강한 주장이므로 <strong>맥락 확인 전까지 인용 보류</strong>. 비용 절감 주제에 관심 있다면 볼 가치는 있으나, 수치를 그대로 가져다 쓰면 위험하다.</p>
  <div class="grid-3">
    <article class="score-card"><h3>FACT · 확인</h3><p>제목·채널·길이 등 메타데이터만 입력으로 주어졌다. 영상 본문(발화)은 확인하지 못했다.</p></article>
    <article class="score-card"><h3>INFERENCE · 추론</h3><p>"70% 절감"은 특정 워크로드·기준선에 한정된 수치일 가능성이 높다. 일반화된 보장으로 보기 어렵다.</p></article>
    <article class="score-card"><h3>UNKNOWN · 확인 필요</h3><p>절감의 기준선, 측정 방법, 품질 영향, 적용 조건은 트랜스크립트 없이는 알 수 없다.</p></article>
  </div>
  <p>핵심 태도는 "흥미롭지만 인용 금지"다. 제목의 수치는 클릭을 유도하기 위한 압축일 수 있으므로, 본 분석은 영상 내용을 사실처럼 단정하지 않고 무엇을 확인해야 하는지를 체크리스트로 정리하는 데 집중한다. 즉 이 리포트의 결과물은 "정답"이 아니라 "검증 계획"이다.</p>
</section>'''

s2 = f'''
<section id="s2" class="source-trust summary-card">
  {h2("02","출처·신뢰 스냅샷","source")}
  <p class="h2-sub">무엇을 입력으로 받았고 무엇을 못 받았는지 먼저 못 박는다. 신뢰도는 입력 tier가 좌우한다.</p>
  <div class="table-scroll"><table>
    <caption>입력 tier와 신뢰 범위</caption>
    <thead><tr><th>항목</th><th>상태</th><th>분석 가능 범위</th></tr></thead>
    <tbody>
      <tr><th>URL/제목/채널</th><td>확인됨(FACT)</td><td>주제·포지셔닝 추정</td></tr>
      <tr><th>설명·챕터</th><td>부분/미상</td><td>있으면 구조 추정, 없으면 UNKNOWN</td></tr>
      <tr><th>트랜스크립트</th><td>미확보</td><td>발화 인용 불가</td></tr>
      <tr><th>댓글</th><td>미확보</td><td>반응 신호 분석 불가</td></tr>
    </tbody>
  </table></div>
  <p>분석 기준 시각(observed_at)은 <strong>2026-06-13 KST</strong>다. 영상은 시간이 지나면 수정·삭제될 수 있으므로, 이후 인용 시 같은 시점인지 확인한다. 비공개 analytics(노출수·시청 지속률 절대값)는 추정하지 않는다.</p>
</section>'''

s3 = f'''
<section id="s3" class="watching-decision summary-card">
  {h2("03","TL;DW · 볼지 말지","decision")}
  <p class="h2-sub">한 줄 요약과, 누가 보면 좋고 누가 건너뛰어도 되는지를 정리한다(메타데이터 기반 추정).</p>
  <div class="grid-2">
    <article class="good"><span class="label">보면 좋음</span><p>LLM 운영 비용에 책임이 있는 엔지니어·리드. 캐싱·배치·모델 라우팅 같은 절감 기법의 <strong>아이디어 목록</strong>을 얻는 용도로 적합하다.</p></article>
    <article class="danger"><span class="label">건너뛰어도 됨</span><p>구체적 벤치마크·재현 코드를 기대하는 사람. 토크 형식 특성상 깊은 수치 근거는 제한적일 가능성이 크다(INFERENCE).</p></article>
  </div>
  <p>TL;DW(추정): "비용은 모델·캐싱·요청 설계의 함수이며, 몇 가지 레버를 조합하면 크게 줄일 수 있다"는 메시지일 것이다. 다만 70%라는 결과 수치는 발표자의 특정 환경에 묶인 사례로 받아들이는 편이 안전하다.</p>
</section>'''

s4 = f'''
<section id="s4" class="video-evidence-map summary-card">
  {h2("04","영상 근거 지도 (Video Evidence Map)","search")}
  <p class="h2-sub">주장과 그 근거 가능성을 표로 정리한다. 트랜스크립트가 없으므로 '근거'는 확인 대상이지 확정이 아니다.</p>
  <div class="table-scroll"><table>
    <caption>주장 · 근거 가능성 · 판정 · 다음 확인</caption>
    <thead><tr><th>주장(추정)</th><th>근거 유형</th><th>판정</th><th>다음 확인</th></tr></thead>
    <tbody>
      <tr><th>비용 70% 절감</th><td>사례 수치</td><td>UNKNOWN</td><td>기준선·워크로드·기간 확인</td></tr>
      <tr><th>캐싱이 큰 레버</th><td>일반 통념</td><td>INFERENCE</td><td>적중률·무효화 비용 확인</td></tr>
      <tr><th>작은 모델 라우팅</th><td>아키텍처 패턴</td><td>INFERENCE</td><td>품질 저하 측정 여부</td></tr>
      <tr><th>배치/비동기화</th><td>운영 기법</td><td>INFERENCE</td><td>지연 허용 범위 확인</td></tr>
      <tr><th>토큰 다이어트</th><td>프롬프트 최적화</td><td>INFERENCE</td><td>정확도 영향 확인</td></tr>
    </tbody>
  </table></div>
  <p>다섯 항목 중 확정(FACT)은 없다. 이 표의 가치는 "영상을 볼 때 무엇을 메모해야 하는지"의 체크리스트라는 데 있다. 각 주장에 대해 발표자가 제시하는 기준선과 측정 방법을 받아 적으면, 70%가 우리 상황에 의미 있는지 판단할 수 있다.</p>
</section>'''

s5 = f'''
<section id="s5" class="chapter-retention summary-card">
  {h2("05","챕터·리텐션 가설","timeline")}
  <p class="h2-sub">설명/챕터가 없으면 구조는 추정이다. 토크의 전형적 전개를 가설로 두고, 시청 시 검증한다.</p>
  <section class="vt-shell" aria-label="추정 챕터 타임라인">
    <div class="vt-frame"><ol class="tl">
      <li class="tl-item"><b>도입</b><p class="vt-text">비용 문제 제기 — "왜 LLM 비용이 폭증하는가"(추정).</p></li>
      <li class="tl-item"><b>진단</b><p class="vt-text">비용 분해 — 토큰·호출 빈도·모델 단가(추정).</p></li>
      <li class="tl-item"><b>레버</b><p class="vt-text">캐싱·라우팅·배치·프롬프트 최적화 소개(추정).</p></li>
      <li class="tl-item"><b>결과</b><p class="vt-text">사례 수치(70%)와 한계·교훈(추정).</p></li>
    </ol></div>
  </section>
  <p>이 타임라인은 사실이 아니라 가설이다. 실제 챕터가 제공되면 교체해야 한다. 리텐션(시청 지속률)의 절대값은 비공개 데이터이므로 추정하지 않으며, "도입·결과 구간에 사람이 몰릴 것"이라는 일반 패턴만 참고로 둔다.</p>
</section>'''

s6 = f'''
<section id="s6" class="comment-signals summary-card">
  {h2("06","댓글 신호","quote")}
  <p class="h2-sub">댓글이 입력으로 주어지지 않았으므로 분석할 수 없다. 대신 "확인되면 무엇을 볼지"를 정의한다.</p>
  <ul class="check-list">
    <li><strong>반박 신호</strong> — "우리 환경에선 안 됐다" 류의 반례가 있는가? 절감 주장의 일반성 검증에 핵심.</li>
    <li><strong>보강 신호</strong> — 시청자가 구체 수치·코드·기준선을 댓글로 보완했는가?</li>
    <li><strong>질문 빈도</strong> — "품질은 안 떨어지나?"가 반복되면, 영상이 품질 영향을 충분히 다루지 않았다는 신호.</li>
  </ul>
  <div class="danger"><span class="label">한계</span><p>현재 입력으로는 위 신호를 측정할 수 없다(UNKNOWN). 댓글 텍스트가 확보되면 별도 분석으로 보강해야 하며, 그 전까지 "반응이 좋았다/나빴다"를 단정하지 않는다.</p></div>
</section>'''

s7 = f'''
<section id="s7" class="opportunity-matrix summary-card">
  {h2("07","콘텐츠 갭 → 제작 흐름","impact")}
  <p class="h2-sub">이 영상이 비웠을 가능성이 큰 부분을, 우리 콘텐츠/문서의 기회로 전환하는 흐름이다.</p>
  <section class="wg-13-fc" aria-label="콘텐츠 갭 제작 흐름">
    <h3 class="wg-13-h">갭 → 검증 → 제작 <span class="wg-13-sub">영상 시청 후 실행 경로</span></h3>
    <div class="wg-13-flow">
      <a href="#yt-s1" class="wg-13-node wg-13-node--start"><span class="wg-13-step">시작</span>갭 식별</a>
      <span class="wg-13-arrow" aria-hidden="true">&darr;</span>
      <div class="wg-13-branch">
        <a href="#yt-s2" class="wg-13-node wg-13-node--decide"><span class="wg-13-step">?</span>우리가 재현 가능한가?</a>
        <div class="wg-13-paths">
          <div class="wg-13-path wg-13-path--fail"><span class="wg-13-edge">아니오 &rarr; 보류</span><a href="#yt-fail" class="wg-13-node wg-13-node--fail"><span class="wg-13-step">!</span>가정으로 표기</a></div>
          <div class="wg-13-path wg-13-path--ok"><span class="wg-13-edge">예 &rarr; 제작</span><a href="#yt-ok" class="wg-13-node wg-13-node--end"><span class="wg-13-step">완료</span>검증 글/영상</a></div>
        </div>
      </div>
    </div>
    <div class="wg-13-detail">
      <h4 class="wg-13-dh">단계 상세 <span class="wg-13-dnote">박스를 펼쳐 확인</span></h4>
      <details id="yt-s2" class="wg-13-acc" open><summary><span class="wg-13-tag">판단</span>재현 가능성</summary><div class="wg-13-body"><p>우리 트래픽으로 같은 레버(캐싱·라우팅)를 적용해 기준선 대비 절감을 측정할 수 있는지 본다.</p></div></details>
      <details id="yt-fail" class="wg-13-acc wg-13-acc--fail"><summary><span class="wg-13-tag wg-13-tag--fail">보류</span>가정 표기</summary><div class="wg-13-body"><p>재현 불가하면 "발표자 환경 한정"으로 명시하고 인용하지 않는다.</p></div></details>
      <details id="yt-ok" class="wg-13-acc wg-13-acc--ok"><summary><span class="wg-13-tag wg-13-tag--ok">제작</span>검증 콘텐츠</summary><div class="wg-13-body"><p>우리 수치로 재현한 "LLM 비용 절감 실측" 글이 영상보다 신뢰도 높은 자산이 된다.</p></div></details>
    </div>
  </section>
</section>'''

s8 = f'''
<section id="s8" class="claim-risk summary-card">
  {h2("08","주장 · 근거 · 리스크","warning")}
  <p class="h2-sub">영상 메시지를 그대로 인용했을 때의 위험을 정리한다. 가장 큰 리스크는 수치의 무비판적 재사용이다.</p>
  <div class="card-grid">
    <article class="mini-card"><span class="case-label">높음</span><h3>수치 일반화</h3><p>"70%"를 우리 발표·문서에 그대로 쓰면, 조건이 다른 환경에서 책임 소재가 생긴다.</p></article>
    <article class="mini-card"><span class="case-label">중간</span><h3>품질 누락</h3><p>비용만 강조하고 품질 저하를 다루지 않았다면, 절감 기법 도입 시 정확도 회귀를 놓친다.</p></article>
    <article class="mini-card"><span class="case-label">중간</span><h3>맥락 손실</h3><p>토크의 전제(워크로드 형태)를 빼고 기법만 옮기면 효과가 재현되지 않는다.</p></article>
  </div>
  <p>완화책은 단순하다. 인용할 때 항상 "발표자 환경 기준"이라는 단서를 붙이고, 우리 환경에서 재현한 수치로 대체될 때까지 70%를 사실로 쓰지 않는다.</p>
</section>'''

s9 = f'''
<section id="s9" class="video-blueprint summary-card">
  {h2("09","후속 영상·콘텐츠 설계","edit")}
  <p class="h2-sub">이 분석을 우리 자산으로 바꾸는 설계다. 영상의 약점(재현성)을 우리 강점으로 만든다.</p>
  <ol class="practice-list">
    <li><strong>제목</strong> — "LLM 비용, 우리 환경에서 실제로 얼마나 줄였나(측정 포함)" — 재현성으로 차별화.</li>
    <li><strong>구성</strong> — 기준선 공개 → 레버별 적용 → 비용·품질 동시 측정 → 한계.</li>
    <li><strong>증거</strong> — 토큰·호출·단가 분해 표와 before/after 수치를 공개해 신뢰를 확보.</li>
  </ol>
  <div class="good"><span class="label">차별점</span><p>원본 토크가 "사례 수치"에 그쳤다면, 우리 콘텐츠는 "재현 가능한 측정"을 제공한다. 이 한 가지 차이가 인용되는 자산과 흘러가는 영상의 차이를 만든다.</p></div>
</section>'''

s10 = f'''
<section id="s10" class="summary-card">
  {h2("10","출처 한계 (Source Limits)","security")}
  <p class="h2-sub">이 리포트가 무엇을 못 했는지 분명히 한다. 아래는 모두 추가 입력 없이는 확인 불가(UNKNOWN)다.</p>
  <ul class="check-list">
    <li><strong>발화 내용</strong> — 트랜스크립트 미확보로 발표자의 실제 주장·수치·전제를 인용할 수 없다.</li>
    <li><strong>반응</strong> — 댓글·좋아요·시청 지속률 미확보로 시청자 반응을 단정할 수 없다.</li>
    <li><strong>수치 근거</strong> — 70% 절감의 기준선·측정 방법·품질 영향은 영상 본문 확인이 필요하다.</li>
    <li><strong>시점</strong> — 분석 기준 시각 2026-06-13 이후 영상이 바뀌면 본 분석은 무효일 수 있다.</li>
  </ul>
  <p>요약하면 이 문서는 "영상을 보기 전 준비물"이자 "보면서 채울 빈칸"이다. 빈칸이 채워지기 전까지 어떤 수치도 사실로 인용하지 않는다.</p>
</section>'''

snext = f'''
<section id="snext" class="try">
  {h2(None,"다음 행동","landing")}
  <p>이 영상은 아이디어 소스로 쓰고, 수치는 우리 손으로 재현해 자산화하는 것이 가장 안전하고 가치 있는 경로다.</p>
  <div class="cta-box">
    <p><strong>실행 플랜</strong></p>
    <ol><li>영상 시청하며 §4 근거 지도의 각 칸을 발표자 발화로 채운다.</li><li>우리 트래픽으로 캐싱·라우팅 1개씩 적용해 비용·품질을 동시 측정.</li><li>before/after 수치로 "재현 가능한 비용 절감" 글 발행.</li></ol>
    <div class="tag-list"><span class="tag">youtube_analysis</span><span class="tag">llm-cost</span><span class="tag">근거 우선</span><span class="tag">재현성</span></div>
  </div>
</section>'''

source_note = '<aside class="source-note"><p><strong>출처 한계.</strong> 본 분석의 입력은 영상 URL·제목·채널 등 메타데이터 수준이며 트랜스크립트·댓글·analytics는 확보되지 않았다. 따라서 영상 내부 주장·수치(특히 "70% 절감")는 확인 불가(UNKNOWN)로 처리했고, 챕터·전개는 추정 가설이다. 인용 전 반드시 영상 본문과 출처를 직접 확인한다. 분석 기준 시각: 2026-06-13 KST.</p></aside>'

body = ('<main id="main" class="page-wide layout-youtube">' + header + toc + s1+s2+s3+s4+s5+s6+s7+s8+s9+s10+snext + source_note + '</main>')
out = build_page("pages/07_youtube_analysis_llm_cost_talk.html", title=TITLE, description=DESC, body=body)
write_sources()
print("WROTE", out)
