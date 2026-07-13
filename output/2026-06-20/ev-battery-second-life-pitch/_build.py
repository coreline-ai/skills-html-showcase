#!/usr/bin/env python3
# 3중 하이브리드: storm-research(3관점 출처조사) → bizplan(사업논리·증거태깅 방법론)
#               → adaptive-html-final 5.10.5 landing-brief(투자 피치덱) 렌더(scaffold-splice).
# 주제(storm 자유주제): 중고 EV 배터리 진단·인증 & 2차 사용 라우팅 플랫폼 — 투자 피치덱.
import json, re, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[3]
SKILL = ROOT / "skills/adaptive-html-final"
EX = SKILL / "examples/12_landing_pagercalm_brief.html"
OUT = pathlib.Path(__file__).resolve().parent / "index.html"
ICONS = {d["id"]: d["svg"] for d in json.load(open(SKILL/"assets/body-icons.json", encoding="utf-8"))}
def ic(k): return f'<span class="body-icon body-icon--sm">{ICONS[k]}</span>'
def h2(n,k,t): return f'<h2>{ic(k)}<span class="num">{n}</span>{t}</h2>'
def a(href,txt): return f'<a href="{href}" target="_blank" rel="noopener">{txt}</a>'

HEADER = (
'<header class="header"><div class="kicker"><span class="kicker-text">INVESTOR PITCH · 사업 구상</span></div>'
'<h1>리셀(ReCell) — 중고 EV 배터리에 ‘건강검진서’를 붙이는 진단·인증·재사용 라우팅 플랫폼</h1>'
'<p class="sub">중고 전기차 배터리는 아직 ‘건강검진서 없이 팔리는 중고차’다. 리셀은 EIS·머신러닝 급속 진단으로 '
'배터리 잔존수명(SoH)을 표준 인증서로 만들고, 그 인증을 근거로 재사용(ESS)·재활용·거래를 자동 라우팅한다. '
'— 시장·기술·규제 수치는 모두 공개 출처(말미)로, 회사 고유 항목은 <strong>[가정]·[목표]·[확인 필요]</strong>로 정직하게 표기한다.</p>'
'<div class="meta"><span>landing_brief_html</span><span>landing-brief.html</span><span>profile auto</span>'
'<span>adaptive-html-final v5.10.5</span><span>무 JS</span><span>증거 태깅 적용</span></div>'
'<div class="generated-row"><p class="generated-date">2026-06-20 KST · storm-research 출처조사 → bizplan 사업논리 → adaptive-html-final 렌더</p>'
'<div class="lens-strip" aria-label="태그"><span class="lens-strip-label">TAGS</span>'
'<span class="lens-chip">사용후배터리</span><span class="lens-chip">SoH 진단</span><span class="lens-chip">2차 사용</span>'
'<span class="lens-chip">배터리 여권</span><span class="lens-chip">투자 피치덱</span></div></div></header>'
)

TOC_ITEMS=[
 ("한 문장 정의","section-01"),("우리가 푸는 문제","section-02"),("왜 지금인가","section-03"),
 ("시장 — TAM·SAM·SOM","section-04"),("솔루션","section-05"),("사업 모델","section-06"),
 ("경쟁과 해자","section-07"),("리스크와 대응","section-08"),("팀·실행 계획","section-09"),
 ("재무·투자 요청","section-10"),("다음 단계","section-11"),("출처·증거등급·메타","section-12"),
]
TOC=('<nav class="toc-map" aria-label="문서 목차"><span class="label">문서 목차</span>'
     '<p>피치 흐름(문제→왜지금→시장→솔루션→경쟁→리스크→팀→요청)을 chip-nav로 이동합니다.</p><div class="toc-pills">'
     +''.join(f'<a class="toc-pill" href="#{sid}"><b>{i+1}</b>{t}</a>' for i,(t,sid) in enumerate(TOC_ITEMS))+'</div></nav>')

S=[]

# ── 01 hero-analogy (한 문장) ──
S.append(f'''<section class="hero-analogy" id="section-01"><h2>{ic("idea")}한 문장 정의</h2>
<h3>중고 EV 배터리는 ‘건강검진서 없이 팔리는 중고차’다. 리셀은 배터리에 신뢰할 수 있는 건강검진서를 붙인다.</h3>
<p>중고차에는 성능점검기록부가 있어 거래·보험·금융이 돌아간다. 그런데 한 대당 수백만 원짜리 EV 배터리는 잔존수명(SoH)을 객관적으로 증명할 표준 검진서가 없어, 재사용해도 될 배터리가 헐값에 폐기되거나 위험한 배터리가 그대로 재유통된다.</p>
<p>리셀이 파는 약속은 “배터리를 더 싸게”가 아니라 <span class="hl">‘이 배터리를 믿고 다시 써도 된다’는 인증과, 그 인증을 근거로 한 자동 재사용·거래 라우팅</span>이다. 진단(EIS+ML) → 표준 SoH 인증서 → 재사용/재활용/거래로 보내는 한 흐름을 하나의 플랫폼으로 잇는다.</p>
<div class="vt-shell"><div class="vt-frame"><div class="vt-demo"><div class="hm-grid">
<article class="hm-card"><div class="vt-kicker">문제</div><h3>SoH가 안 보여 거래가 막힌다</h3><p class="vt-text">잔존수명을 증명할 표준 검진서가 없어 중고 EV·사용후 배터리의 잔존가치가 무너지고, 재사용·재활용 라우팅도 추측에 의존한다.</p></article>
<article class="hm-card" style="--c:var(--vt-blue)"><div class="vt-kicker">기회</div><h3>규제가 진단을 ‘필수재’로 만든다</h3><p class="vt-text">EU 배터리 여권(2027)·한국 사용후배터리법(2026 통과)이 SoH·이력 데이터를 법적 필수재로 만든다. 진단이 옵션에서 의무로.</p></article>
<article class="hm-card" style="--c:var(--vt-green)"><div class="vt-kicker">솔루션</div><h3>진단 → 인증 → 라우팅</h3><p class="vt-text">EIS+머신러닝 급속 진단으로 표준 SoH 인증서를 발급하고, 그 등급에 따라 재사용(ESS)·재활용·거래로 자동 라우팅한다.</p></article>
</div><div class="hm-result"><b>한 장 요약: 새 배터리를 만드는 회사가 아니라, 이미 만들어진 배터리의 ‘신뢰’를 만드는 회사</b><span>진단 한 건이 인증서가 되고, 인증서가 거래·재사용·금융의 기준이 된다 — 데이터가 쌓일수록 등급의 정확도와 해자가 커진다.</span></div></div></div></div></section>''')

# ── 02 문제 ──
S.append(f'''<section id="section-02">{h2(2,"warning","우리가 푸는 문제")}
<p class="h2-sub">통증은 ‘배터리가 부족해서’가 아니라 ‘배터리를 믿을 수 없어서’ 생긴다.</p>
<p>전기차 1세대(2010년대 중반) 배터리가 은퇴하기 시작하면서, 한국의 사용후 배터리 배출량은 <strong>2023년 약 2,355개 → 2029년 약 78,981개 → 2030년 약 10.7만 개</strong>로 급증할 전망이다 [추정] (환경부·에너지경제연구원 추정 인용). 그런데 이 배터리들을 다시 쓰려는 순간 세 가지 벽에 부딪힌다.</p>
<div class="card-grid">
<article class="mini-card"><h3>① SoH 표준의 부재</h3><p>잔존수명(SoH)은 전압처럼 직접 측정되지 않고 추정되며, OEM마다 알고리즘이 달라 “같은 90%”가 브랜드 간 같은 뜻이 아니다 [사실]. 거래·보증·인증의 신뢰 기반이 없다.</p></article>
<article class="mini-card"><h3>② OEM 데이터 락인</h3><p>핵심 셀 데이터(셀 전압·SoH·팩 온도)는 OEM 전용 도구 뒤에 잠겨 있어, 검증 없이 매입한 배터리는 성능 실패·보증 분쟁을 낳는다 [사실].</p></article>
<article class="mini-card"><h3>③ 라우팅의 부재</h3><p>“이 배터리는 재사용인가, 재활용인가”를 가를 객관 기준이 없어, 재사용 가능한 배터리가 폐기되거나 위험한 배터리가 재유통된다 [추론].</p></article>
</div>
<p>그 결과는 명확하다 — 수백만 원짜리 자산이 ‘검진서가 없다’는 이유 하나로 잔존가치를 잃는다. 문제의 본질은 공급이 아니라 <strong>신뢰의 부재</strong>다.</p></section>''')

# ── 03 왜 지금 ──
S.append(f'''<section id="section-03">{h2(3,"timeline","왜 지금인가")}
<p class="h2-sub">세 곡선이 2025~2027년에 교차한다 — 더 빠르지도, 늦지도 않은 창(window).</p>
<p><strong>① 은퇴 파동의 시작.</strong> 시장조사기관들은 2025년을 EV 배터리 1차 대량 은퇴의 출발점으로 본다 [추정]. 글로벌 2차 사용 배터리 시장은 2025년 약 25~30GWh → 2030년 약 <strong>330~350GWh</strong>, 연평균 약 <strong>65%</strong> 성장이 전망된다 [추정] ({a("https://www.prnewswire.com/news-releases/second-life-ev-battery-market-worth-330-350-gwh-by-2030--marketsandmarkets-302525085.html","MarketsandMarkets")}).</p>
<p><strong>② 규제가 진단을 의무로 만든다.</strong> EU 배터리 규정은 2027년 2월 18일부터 EV 배터리에 <strong>디지털 배터리 여권</strong>을 의무화하고, 셀 단위 SoH·사이클 이력·온도 기록을 표준 포맷으로 요구한다 [사실] ({a("https://www.automotive-iq.com/electrics-electronics/articles/eu-battery-passport-explained-requirements-timeline-and-compliance-steps-to-2027","Automotive IQ")}). 한국도 <strong>사용후 배터리 산업 육성법이 2026년 4월 국회 본회의를 통과</strong>해 성능·안전 평가 의무화와 이력관리·거래 시스템 근거가 마련됐고, 탈거 전 성능평가는 2027년 시행이 예정돼 있다 [사실] ({a("https://biz.heraldcorp.com/article/10724433","헤럴드경제")}).</p>
<p><strong>③ 수요처(ESS)의 폭증.</strong> 2차 사용 배터리의 주 수요처인 ESS 시장은 2030년 글로벌 설치 약 <strong>750GWh</strong>로 2024년 대비 2.5~3배 전망이다 [추정] ({a("https://www.todayenergy.kr/news/articleView.html?idxno=294732","SNE리서치 인용")}).</p>
<p>요컨대 규제가 ‘진단 데이터’를 법적 필수재로 만드는 바로 그 시점에 은퇴 물량과 수요처가 동시에 커진다. <strong>진단·인증을 표준으로 선점할 단 한 번의 창</strong>이다.</p></section>''')

# ── 04 시장 TAM/SAM/SOM ──
S.append(f'''<section id="section-04">{h2(4,"metric","시장 — TAM·SAM·SOM")}
<p class="h2-sub">민간 조사기관 간 편차가 커, 단일 출처를 명시하고 산식을 공개한다(보수 기준).</p>
<div class="tbl table-scroll"><table><caption>시장 규모 — 모든 수치에 증거등급·산식·출처 표기 (보수적 단일 출처 기준)</caption>
<thead><tr><th scope="col">구분</th><th scope="col">정의</th><th scope="col">규모(연·약)</th><th scope="col">산식·근거 [태그]</th></tr></thead><tbody>
<tr><td><strong>TAM</strong></td><td>글로벌 배터리 진단 + 2차 사용 시장</td><td>약 10조원+<br>(2034~2035)</td><td>진단 $6.6B(2034, {a("https://www.globenewswire.com/news-release/2025/09/29/3157465/28124/en/EV-Battery-Health-Diagnostics-System-Market-Growth.html","GMI")}) + 2차사용 $4.2B(2035, {a("https://www.idtechex.com/en/research-report/second-life-ev-batteries-2025/1056","IDTechEx")}) 합산 [추정·추론]</td></tr>
<tr><td><strong>SAM</strong></td><td>국내 사용후 배터리 진단·인증(서비스 가능 시장)</td><td>약 500억원+<br>(2030, 국내)</td><td>2030년 국내 EoL 약 10.75만 개(환경부 추정 [추정]) × 진단·인증 객단가 50만원 [가정] ≈ 538억원/년. 거래·라우팅·SaaS 수수료는 별도 상방</td></tr>
<tr><td><strong>SOM</strong></td><td>초기 3년 확보 목표(국내 SAM 내)</td><td>SAM의 5~10%<br>(2028 목표)</td><td>인증 파트너십 기반 초기 점유 [목표] — 실증 2곳·OEM/딜러 제휴 확보 가정</td></tr>
</tbody></table></div>
<p>핵심 모수는 검증된 공식 추정이다 — 국내 사용후 배터리 발생량은 2023년 2,355개에서 2030년 약 10.7만 개로 약 45배 증가한다 [추정]. 글로벌 폐배터리 재활용 시장만 2030년 약 <strong>60조원(글로벌)</strong> 규모로 전망되나 [추정] ({a("https://www.industrynews.co.kr/news/articleView.html?idxno=48830","SNE리서치")}), 이는 한국 단독 수치가 아니므로 본 덱은 국내 기준 SAM으로 보수 산정했다.</p></section>''')

# ── 05 솔루션 ──
S.append(f'''<section id="section-05">{h2(5,"flow","솔루션")}
<p class="h2-sub">새 배터리를 만들지 않는다. 이미 만들어진 배터리의 ‘신뢰’를 만든다.</p>
<div class="card-grid">
<article class="mini-card"><h3>EIS+ML 급속 진단</h3><p>전기화학 임피던스 분광(EIS)에 머신러닝을 결합해 수 분 내 비파괴로 SoH를 추정한다. 연구에서 단일 EIS 측정만으로 잔존수명 예측이 보고됐다 [사실] ({a("https://pmc.ncbi.nlm.nih.gov/articles/PMC7136228/","Nature Comm.")}). <strong>목표 정확도</strong>: 90%+ [목표].</p></article>
<article class="mini-card"><h3>표준 SoH 인증서</h3><p>진단 결과를 등급화한 <strong>기계판독 가능 인증서</strong>로 발급한다. EU 배터리 여권·한국 이력관리 시스템과 연동되도록 설계한다 [목표].</p></article>
<article class="mini-card"><h3>재사용·재활용 라우팅</h3><p>인증 등급에 따라 재사용(ESS)·재제조·재활용·거래로 자동 분기한다. 화학조성(LFP↔NCA)별로 경제성이 갈리므로 등급+화학을 함께 본다 [추론].</p></article>
<article class="mini-card"><h3>거래·데이터 레이어</h3><p>인증서 기반 B2B 거래·금융을 붙이고, 누적 진단 데이터로 잔존가치 예측 모델을 고도화한다. <strong>데이터가 쌓일수록 정확도·해자 강화</strong> [목표].</p></article>
</div>
<p>핵심은 단일 제품이 아니라 <strong>진단→인증→라우팅의 연결</strong>이다. 진단만 파는 회사, 거래만 하는 회사는 있어도, ‘인증을 축으로 셋을 잇는’ 자리는 비어 있다.</p>
<p>배터리 한 팩이 리셀을 거치는 경로는 이렇다 — 수거부터 거래·데이터 적립까지 한 흐름으로 이어진다.</p>
<div class="wg-08-proto"><ol class="wg-08-static">
<li class="wg-08-static-step"><span class="wg-08-static-no">1</span><div><h3>수거·접수</h3><p>은퇴 배터리가 OEM·딜러·정비망에서 접수된다. 새 배터리를 만들지 않고, 이미 만들어진 것을 받는다.</p></div></li>
<li class="wg-08-static-step"><span class="wg-08-static-no">2</span><div><h3>EIS+ML 급속 진단</h3><p>전기화학 임피던스에 머신러닝을 결합해 수 분 내 비파괴로 SoH를 추정한다 [목표: 정확도 90%+].</p></div></li>
<li class="wg-08-static-step"><span class="wg-08-static-no">3</span><div><h3>표준 SoH 인증서 발급</h3><p>진단 결과를 등급화해 기계판독 가능 인증서로 만든다. EU 배터리 여권·한국 이력제와 연동되도록 설계한다.</p></div></li>
<li class="wg-08-static-step wg-08-static-step--hot"><span class="wg-08-static-no">!</span><div><h3>안전 분기</h3><p>위험 등급은 재사용에서 즉시 제외하고 안전 처리·재활용으로 보낸다. 신뢰가 위험으로 바뀌지 않게 두는 규칙이다.</p></div></li>
<li class="wg-08-static-step"><span class="wg-08-static-no">4</span><div><h3>재사용·재활용 라우팅</h3><p>등급+화학조성(LFP↔NCA)에 따라 재사용(ESS)·재제조·재활용·거래로 자동 분기한다.</p></div></li>
<li class="wg-08-static-step wg-08-static-step--ok"><span class="wg-08-static-no">✓</span><div><h3>거래·데이터 적립</h3><p>인증 기반 거래가 성사되고, 진단 데이터가 쌓여 잔존가치 예측 모델을 고도화한다.</p></div></li>
</ol><p class="wg-08-hint">단계는 정적 흐름으로 읽는다(무 JS). 진단 정확도·소요시간은 [목표]이며 실증으로 검증할 값이다.</p></div></section>''')

# ── 06 사업 모델 ──
S.append(f'''<section id="section-06">{h2(6,"platform","사업 모델")}
<p class="h2-sub">진단 한 건이 인증서가 되고, 인증서가 거래·재사용의 기준이 된다 — 단계마다 과금점이 생긴다.</p>
<div class="card-grid">
<article class="mini-card"><h3>① 진단 건당 수수료</h3><p>배터리 1팩당 진단·인증 발급 수수료 [가정]. 물량(은퇴 배터리)과 함께 선형 성장.</p></article>
<article class="mini-card"><h3>② 인증 SaaS 구독</h3><p>OEM·딜러·재사용 사업자 대상 인증 발급·관리·이력 연동 구독 [가정]. 규제 대응 수요와 직결.</p></article>
<article class="mini-card"><h3>③ 거래 라우팅 수수료</h3><p>인증 등급 기반 B2B 거래·재사용 중개 수수료 [가정]. 거래액 증가에 따른 마진.</p></article>
<article class="mini-card"><h3>④ 데이터·금융</h3><p>누적 잔존가치 데이터 기반 보증·금융·리스 연계 [목표]. 장기 수익·해자.</p></article>
</div>
<p>초기에는 ①·②(규제 대응 수요가 확실한 진단·인증)로 현금흐름을 만들고, 데이터가 쌓이면 ③·④로 단위경제를 끌어올리는 순서다. 모든 가격·전환율은 현재 <strong>[가정]</strong>이며 실증·파일럿으로 검증할 항목이다 [확인 필요].</p></section>''')

# ── 07 경쟁과 해자 ──
S.append(f'''<section id="section-07">{h2(7,"compare","경쟁과 해자")}
<p class="h2-sub">진단·2차사용·재활용은 각각 강자가 있다. 비어 있는 건 ‘셋을 잇는 인증 축’이다.</p>
<div class="tbl table-scroll"><table><caption>경쟁 지형 — 투자·실적은 보도 기준 [사실]</caption>
<thead><tr><th scope="col">구분</th><th scope="col">대표 플레이어</th><th scope="col">강점 / 한계</th></tr></thead><tbody>
<tr><td>글로벌 진단 SaaS</td><td>TWAICE(누적 ~$75M), ACCURE(~$34.5M)</td><td>분석·안전 SaaS 선두 / 운영데이터 기반, 독립 물리진단·인증·라우팅과는 결이 다름 [사실]</td></tr>
<tr><td>2차 사용 BESS</td><td>B2U, Connected Energy</td><td>저비용 비개조 ESS 모델 / ‘정밀 진단 없이’ 투입해, 진단 가치제안의 대체 경로 [사실]</td></tr>
<tr><td>재활용</td><td>Redwood($6B+ 밸류), Li-Cycle(2025 파산)</td><td>막대한 자본 흡수 / 재활용은 자본집약·물량/금속가 민감 — Li-Cycle 파산이 방증 [사실]</td></tr>
<tr><td>한국 진단·OEM</td><td>민테크(국내 진단), 현대글로비스(회수 수직계열)</td><td>국내 진단 선점·OEM 회수망 / OEM 수직계열은 독립 플랫폼의 물량 접근을 제약할 수 있음 [사실]</td></tr>
</tbody></table></div>
<p><strong>우리의 해자.</strong> ① <strong>진단+인증+라우팅 통합</strong>(점이 아닌 흐름), ② <strong>규제 연동</strong>(EU 여권·한국 이력제와 인증 표준 정렬), ③ <strong>독립성</strong>(특정 OEM에 묶이지 않은 중립 인증), ④ <strong>데이터 누적</strong>(진단이 쌓일수록 등급 정확도↑). 단일 제품은 모방되지만, ‘중립 인증 표준+데이터’ 자리는 선점이 곧 해자다.</p></section>''')

# ── 08 리스크와 대응 ──
S.append(f'''<section id="section-08">{h2(8,"audit","리스크와 대응")}
<p class="h2-sub">좋은 피치는 반론을 숨기지 않는다 — 가장 날카로운 반론 네 가지와 대응.</p>
<div class="tbl table-scroll"><table><caption>핵심 리스크와 대응 (반론을 견디는 논리)</caption>
<thead><tr><th scope="col">리스크</th><th scope="col">근거</th><th scope="col">대응</th></tr></thead><tbody>
<tr><td>SoH 표준 부재</td><td>차량 수준 SoH 정의·측정 절차에 산업 합의 없음 [사실]</td><td>규제(EU 여권·한국 이력제)가 표준을 강제하는 흐름에 인증 포맷을 선제 정렬 → 표준 부재가 오히려 기회</td></tr>
<tr><td>OEM 데이터 락인</td><td>핵심 셀 데이터가 OEM 전용 도구에 잠김 [사실]</td><td>OEM 데이터에 의존하지 않는 <strong>물리 진단(EIS)</strong> 기반 → 데이터 미개방 상황에서도 독립 측정 가능</td></tr>
<tr><td>물량 지연 + 신규 셀가 하락</td><td>대량 은퇴는 2030년대 중반, 신품 셀가 $30~50/kWh까지 하락 [사실/추정]</td><td>초기 수익을 ‘물량’이 아니라 규제 대응 <strong>진단·인증(①②)</strong>에 둠 → 물량 도래 전에 인증 표준·데이터 선점</td></tr>
<tr><td>재활용이 더 경제적인 구간</td><td>NCA 등은 재활용이 유리, 2차사용 TAM은 화학별로 쪼개짐 [사실]</td><td>‘재사용 강요’가 아니라 <strong>재사용/재활용 라우팅</strong>이 본업 — 어느 쪽이 경제적이든 인증·분기 수수료 발생</td></tr>
</tbody></table></div>
<p>주의: 재활용 경로 역시 피드스톡 부족·금속가 하락으로 흔들리며(Li-Cycle 파산, 성일하이텍 2024 적자전환 [사실]), “재활용이 항상 우월”하다는 반론도 절대적이지 않다. 우리는 어느 한쪽에 베팅하지 않고 <strong>‘판단의 기준(인증)’</strong>을 판다.</p></section>''')

# ── 09 팀·실행 ──
S.append(f'''<section id="section-09">{h2(9,"user","팀·실행 계획")}
<p class="h2-sub">현재는 사업 구상 단계 — 보유/결손 역량을 정직하게 구분한다.</p>
<p>이 덱은 특정 회사의 실적을 주장하지 않는다. 팀·트랙션·계약은 <strong>[확인 필요]</strong>로 두고, 실행 마일스톤은 <strong>[목표]</strong>로 표기한다(bizplan 무날조 원칙).</p>
<div class="card-grid">
<article class="mini-card"><h3>필요 핵심 역량</h3><p>배터리 전기화학·EIS 진단, ML 모델링, 인증·규제(EU 여권/한국 이력제) 대응, ESS·재사용 사업개발 [확인 필요].</p></article>
<article class="mini-card"><h3>외부 파트너</h3><p>실증 시설(요양·물류 ESS), OEM·딜러 회수망, 시험·인증기관, 재활용사 [가정].</p></article>
<article class="mini-card"><h3>마일스톤 M1 (0~12개월)</h3><p>EIS+ML 진단 PoC, 인증서 포맷 v1, 실증 1곳·배터리 50팩 진단 [목표].</p></article>
<article class="mini-card"><h3>마일스톤 M2 (12~24개월)</h3><p>인증 SaaS 베타, 거래 라우팅 파일럿, 규제 표준 연동 검증, 실증 2곳 확대 [목표].</p></article>
</div></section>''')

# ── 10 재무·투자 요청 ──
S.append(f'''<section id="section-10">{h2(10,"decision","재무·투자 요청")}
<p class="h2-sub">모든 수치는 [목표]·[가정] — 실증으로 검증할 계획 값이다(미확정을 사실로 표기하지 않는다).</p>
<div class="tbl table-scroll"><table><caption>자금 사용 계획 (예시·[목표] 기준 · 총액/배분은 실사 시 확정)</caption>
<thead><tr><th scope="col">용도</th><th scope="col">내용</th><th scope="col">비중(예시)</th></tr></thead><tbody>
<tr><td>R&D·진단엔진</td><td>EIS 측정 HW + ML 모델·인증 포맷 개발</td><td>45% [목표]</td></tr>
<tr><td>실증·파트너십</td><td>실증 사이트 2곳, OEM/딜러·인증기관 제휴</td><td>25% [목표]</td></tr>
<tr><td>인증 SaaS·플랫폼</td><td>인증 발급·이력연동·거래 라우팅 구축</td><td>20% [목표]</td></tr>
<tr><td>운영·규제 대응</td><td>표준 대응, 안전·법무, 핵심 인력</td><td>10% [목표]</td></tr>
</tbody></table></div>
<p><strong>요청.</strong> 시드/프리A 라운드로 24개월 런웨이를 확보해 M1·M2(진단 PoC → 인증 SaaS 베타 → 실증 2곳)를 완주하는 것이 목표다 [목표]. 구체 금액·밸류·지분은 실사 자료와 함께 별도 제시하며, 현 단계에서 단정하지 않는다 [확인 필요].</p></section>''')

# ── 11 try (다음 단계 / the ask) ──
S.append(f'''<section class="try" id="section-11"><div class="label">NEXT ACTION</div>
{h2(11,"success","다음 단계 — 함께 검증할 일")}
<p>이 사업의 진짜 검증은 슬라이드가 아니라 실증에서 난다. 투자자·파트너와 가장 빠르게 확인할 수 있는 네 단계를 제안한다.</p>
<ol>
<li><strong>진단 PoC 공동 설계.</strong> 보유 배터리 샘플로 EIS+ML 진단 정확도(목표 90%+)를 4~6주 내 1차 검증한다.</li>
<li><strong>인증서 v1 표준 정렬.</strong> EU 배터리 여권·한국 이력관리 데이터셋과 인증 포맷을 맞춰 본다.</li>
<li><strong>실증 1곳 확보.</strong> 요양·물류 ESS 등 재사용 수요처 한 곳에서 ‘진단→인증→재사용’ 한 흐름을 돌려본다.</li>
<li><strong>규제 타임라인 점검.</strong> 2027 의무화 전, 인증 표준 선점의 시장 진입 시나리오를 함께 검토한다.</li>
</ol>
<div class="box"><p><strong>한 줄 요청:</strong> ‘배터리를 더 싸게’가 아니라 ‘배터리를 믿게’ 만드는 인프라에, 규제가 진단을 의무화하는 이 창에서 함께 베팅해 주십시오.</p></div></section>''')

# ── 12 출처·증거등급·메타 ──
S.append(f'''<section id="section-12">{h2(12,"reference","출처·증거등급·메타")}
<aside class="source-note"><div class="label">{ic("note")}증거등급 범례 (bizplan 무날조 원칙)</div>
<p><strong>[사실]</strong> 외부 출처/1차 자료로 검증 · <strong>[추정]</strong> 근거+산식으로 도출(민간 조사기관 전망 포함) · <strong>[가정]</strong> 미검증 전제 · <strong>[목표]</strong> 달성하려는 미래값 · <strong>[확인 필요]</strong> 추가 자료 필요. 시장·기술·규제 수치는 공개 출처, 회사 고유(팀·트랙션·가격·재무)는 [가정]·[목표]·[확인 필요]로 표기했다.</p>
<div class="label">{ic("source")}출처 (모든 수치는 아래 공개 자료에서 확인)</div>
<p><strong>시장</strong> · {a("https://www.iea.org/reports/global-ev-outlook-2025/executive-summary","IEA Global EV Outlook 2025")} · {a("https://www.prnewswire.com/news-releases/second-life-ev-battery-market-worth-330-350-gwh-by-2030--marketsandmarkets-302525085.html","MarketsandMarkets 2차사용 330–350GWh")} · {a("https://www.idtechex.com/en/research-report/second-life-ev-batteries-2025/1056","IDTechEx 2차사용 $4.2B(2035)")} · {a("https://www.mckinsey.com/industries/automotive-and-assembly/our-insights/second-life-ev-batteries-the-newest-value-pool-in-energy-storage","McKinsey 2차사용")} · {a("https://www.globenewswire.com/news-release/2025/09/29/3157465/28124/en/EV-Battery-Health-Diagnostics-System-Market-Growth.html","GMI 진단시장 $6.6B(2034)")} · {a("https://www.industrynews.co.kr/news/articleView.html?idxno=48830","SNE리서치 재활용시장")} · {a("https://www.newspim.com/news/view/20260520000434","환경부 국내 발생량")}</p>
<p><strong>기술</strong> · {a("https://pmc.ncbi.nlm.nih.gov/articles/PMC7136228/","Nature Comm. — EIS 단일측정 RUL 예측")} · {a("https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2024.1493869/full","Frontiers — EIS 반자동 진단")} · {a("https://www.nature.com/articles/s44406-025-00010-8","npj — SoH 표준 부재")} · {a("https://evreporter.com/the-missing-link-in-ev-battery-management-independent-diagnostics/","EVreporter — OEM 데이터 락인")}</p>
<p><strong>규제</strong> · {a("https://www.automotive-iq.com/electrics-electronics/articles/eu-battery-passport-explained-requirements-timeline-and-compliance-steps-to-2027","Automotive IQ — EU 배터리 여권 2027")} · {a("https://www.tuv.com/landingpage/en/eu-new-battery-regulation-eu-2023-1542/","TÜV — EU 배터리 규정 2023/1542")} · {a("https://biz.heraldcorp.com/article/10724433","헤럴드경제 — 한국 사용후배터리법 2026.4 통과")} · {a("https://www.kimchang.com/ko/insights/detail.kc?sch_section=4&idx=30348","김·장 — 사용후 배터리 육성방안")}</p>
<p><strong>경쟁</strong> · {a("https://mercomcapital.com/battery-analytics-platform-twaice-series-b-financing/","TWAICE 조달")} · {a("https://www.esgtoday.com/accure-raises-16-million-to-scale-ai-based-platform-to-make-batteries-safer-and-more-reliable/","ACCURE 조달")} · {a("https://www.bloomberg.com/news/articles/2025-10-23/redwood-materials-tops-6-billion-valuation-in-new-funding-round","Redwood $6B")} · {a("https://resource-recycling.com/e-scrap/2025/06/26/li-cycle-files-for-bi-national-bankruptcy-seeks-buyer/","Li-Cycle 파산")} · {a("https://www.newsis.com/view/NISX20240711_0002807338","현대글로비스 회수망")}</p>
<p><strong>메타 설명</strong>: 중고 EV 배터리 진단·인증·재사용 라우팅 플랫폼(리셀)의 투자 피치덱(사업 구상). 시장·기술·규제는 storm-research 3관점(시장/경쟁·회의론/기술·규제) 출처조사로, 사업 논리·증거 태깅·TAM·SAM·SOM 산식·무날조 원칙은 bizplan 방법론으로, HTML 렌더는 adaptive-html-final 5.10.5 landing-brief 모드(무 JS·8테마·hero-map)로 했다.</p>
<p><strong>태그</strong>: #사용후배터리 #SoH진단 #2차사용 #ESS #배터리여권 #순환경제 #투자피치덱 #증거태깅</p>
<p><strong>무날조 고지</strong>: 회사명 ‘리셀’과 팀·트랙션·가격·재무는 실재가 아닌 <strong>사업 구상</strong>이며 [가정]·[목표]·[확인 필요]로 표기했다. 시장·기술·규제 수치만 공개 출처에 근거하며, 민간 조사기관 전망은 기관 간 편차가 커 보수적 단일 출처를 기준으로 삼았다.</p></aside></section>''')

MAIN_INNER = HEADER + TOC + ''.join(S)
ex = EX.read_text(encoding="utf-8")
new = re.sub(r'(<main\s+id="main"[^>]*>)[\s\S]*(</main>)', lambda m: m.group(1)+MAIN_INNER+m.group(2), ex, count=1)
OUT.write_text(new, encoding="utf-8")
vis=re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',re.sub(r'<style[\s\S]*?</style>','',MAIN_INNER))).strip()
print("빌드 완료:", OUT.name, "| 크기:", len(new), "| 섹션:", len(S), "| 본문:", len(vis), "자")
print("hm-grid:", new.count("hm-grid"), "| hero-analogy:", new.count("hero-analogy"), "| tbl:", new.count('class="tbl'), "| card-grid:", new.count("card-grid"), "| try:", new.count('class="try"'), "| 출처링크:", new.count('target="_blank"'))
for tag in ['[사실]','[추정]','[가정]','[목표]','[확인 필요]']:
    print(f"  증거태그 {tag}: {new.count(tag)}")
