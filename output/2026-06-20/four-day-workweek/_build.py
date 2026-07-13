#!/usr/bin/env python3
# 3중 하이브리드: storm-research(출처 기반 조사) → adaptive-html-blog-writer-v2(글쓰기 방법론)
#                → adaptive-html-final 5.10.5 blog_writer 렌더(scaffold-splice).
import json, re, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[3]
SKILL = ROOT / "skills/adaptive-html-final"
EX = SKILL / "examples/05_blog_deepwork_4day_retro.html"
OUT = pathlib.Path(__file__).resolve().parent / "index.html"
ICONS = {d["id"]: d["svg"] for d in json.load(open(SKILL/"assets/body-icons.json", encoding="utf-8"))}
def ic(k): return f'<span class="body-icon body-icon--sm">{ICONS[k]}</span>'
def h2(n,k,t): return f'<h2>{ic(k)}<span class="num">{n}</span>{t}</h2>'
def a(href, txt): return f'<a href="{href}" target="_blank" rel="noopener">{txt}</a>'

HEADER = (
'<header class="header"><div class="kicker"><span class="kicker-text">LONG READ · 분석</span></div>'
'<h1>주 4일 근무제는 환상인가 — 데이터를 직접 파보고 내린 결론</h1>'
'<p class="sub hook">기사 제목은 죄다 “생산성 40% 상승”이다. 너무 좋아서 의심이 들었다. 그래서 6개국 파일럿 데이터와, '
'그 데이터를 깐 경제학자들의 반박과, 100년의 노동시간 역사를 직접 읽어봤다. 결론부터 말하면 — '
'주 4일제는 환상이 아니다. 다만 “어디서, 어떻게”가 빠진 성공담이 문제다.</p>'
'<div class="meta"><span>blog_writer</span><span>personal-blog-essay.html</span><span>page-wide layout-blog</span>'
'<span>adaptive-html-final v5.10.5</span><span>무 JS</span><span>출처 기반 분석</span></div>'
'<div class="generated-row"><p class="generated-date">2026-06-20 · 공개 자료 조사 기반 (모든 수치는 말미 출처에 링크)</p>'
'<div class="lens-strip" aria-label="태그"><span class="lens-strip-label">TAGS</span>'
'<span class="lens-chip">주4일제</span><span class="lens-chip">노동시간</span><span class="lens-chip">생산성</span>'
'<span class="lens-chip">일의 미래</span><span class="lens-chip">근거 점검</span></div></div></header>'
)

TOC_ITEMS=[
 ("다 좋다는데, 왜 아직 주5일일까","section-01"),
 ("제목을 이렇게 골랐다","section-02"),
 ("왜 지금 이 질문인가","section-03"),
 ("데이터는 실제로 무엇을 보여주나","section-04"),
 ("그 숫자를 믿어도 되나","section-05"),
 ("무너진 실험들","section-06"),
 ("핵심은 ‘압축’이 아니라 ‘재설계’","section-07"),
 ("역사가 주는 단서","section-08"),
 ("AI, 그리고 한국 이야기","section-09"),
 ("도입을 고민한다면","section-10"),
 ("마무리 — 4일이 아니라 ‘어떻게’","section-11"),
 ("참고한 자료 · 메타","section-12"),
]
TOC=('<nav class="toc-map" aria-label="문서 목차"><span class="label">문서 목차</span>'
     '<p>글의 흐름(문제→근거→반론→관점→실행)을 chip-nav로 이동합니다.</p><div class="toc-pills">'
     +''.join(f'<a class="toc-pill" href="#{sid}"><b>{i+1}</b>{t}</a>' for i,(t,sid) in enumerate(TOC_ITEMS))+'</div></nav>')

S=[]

# ── 01 HOOK ──
S.append(f'''<section id="section-01">{h2(1,"search","다 좋다는데, 왜 아직 주5일일까")}
<div class="lede-note"><div class="label">HOOK</div><p>주 4일 근무제 실험은 거의 다 “성공”했다고 보고된다. 영국에서 61개 기업이 6개월간 해봤더니 56곳이 계속하기로 했고, 6개국 2,896명을 추적한 연구는 번아웃·직무만족·건강이 모두 좋아졌다고 한다. 그런데 이상하지 않은가 — 그렇게 다 좋다면, 왜 100년 가까이 주 5일이 표준으로 버티고 있을까?</p></div>
<p>이 질문이 머리에서 떠나지 않아서 자료를 직접 파보기 시작했다. 가장 먼저 눈에 걸린 건 1930년의 한 사례였다. 시리얼 회사 켈로그(Kellogg’s)는 대공황 한가운데서 하루 8시간 3교대를 <strong>6시간 4교대</strong>로 바꿨다. 일자리를 나눠 더 많은 사람을 고용하려는 시도였고, 실제로 산재와 간접비가 줄었다. 그 6시간제는 무려 50년을 갔다.</p>
<p>그런데 6시간제를 끝낸 건 생산성 저하가 아니었다. <strong>노동자들 스스로가 더 길게 일하기를 원했기 때문</strong>이었다 — 더 벌어 더 사기 위해서. 시간 단축은 “좋으니까 자동으로 정착”하지 않았다. 이 한 장면이, 장밋빛 헤드라인을 곧이곧대로 믿으면 안 되겠다는 출발점이 됐다.</p>
<p>그래서 이 글은 “주 4일제 좋아요/나빠요”의 응원전이 아니다. 실제 실험들이 무엇을 보여주는지, 그 숫자를 얼마나 믿어도 되는지, 어디서 무너졌는지, 그리고 100년의 노동시간 역사가 무슨 단서를 주는지를 차례로 본다. 모든 수치에는 글 맨 끝에 출처 링크를 달아뒀다.</p></section>''')

# ── 02 제목 메타 (personal_note, blog-writer-v2 시그니처) ──
S.append(f'''<section id="section-02">{h2(2,"compare","제목을 이렇게 골랐다")}
<p>(메타) 본문에 들어가기 전에, 블로그는 제목이 절반이라 네 계열로 뽑아봤다. 규칙은 하나 — <strong>본문에서 증명 못 할 과장은 쓰지 않는다.</strong> “충격”, “무조건”, “이것만 보면” 같은 단어는 클릭은 끌어도 글의 신뢰를 깎는다. 주 4일제 기사가 딱 그 함정에 자주 빠진다.</p>
<div class="summary-card"><div class="label">제목 후보 (4계열)</div><p><strong>검색형</strong> — “주 4일 근무제 효과, 데이터로 정리” <br><strong>클릭형</strong> — “‘생산성 40% 상승’이라는 숫자를 의심한 이유” <br><strong>전문가형</strong> — “주 4일제 파일럿의 방법론적 함정과 재설계 변수” <br><strong>질문형</strong> — “다 좋다는데, 왜 아직 주 5일일까”</p></div>
<p>최종 제목은 전문가형의 무게와 질문형의 궁금증을 섞었다. “환상인가”는 도발이 아니라 이 글이 실제로 검증하려는 가설이다. 그리고 “데이터를 직접 파보고”는 약속이다 — 인상이 아니라 출처로 말하겠다는. 제목이 약속한 것을 본문이 지키는가, 그 기준 하나만 통과시켰다.</p></section>''')

# ── 03 why_now ──
S.append(f'''<section id="section-03">{h2(3,"map","왜 지금 이 질문인가")}
<p>주 4일제는 갑자기 튀어나온 유행이 아니다. 그런데 2026년 지금이 유독 이 질문을 피하기 어려운 해다. 세 가지가 겹쳤다.</p>
<p><strong>첫째, 올해는 주 5일제 100주년이다.</strong> 우리가 “당연”하게 여기는 월~금 40시간은 1926년 헨리 포드가 임금을 깎지 않고 토요일 근무를 없애며 표준화한 것이다. 포드의 논리는 자선이 아니라 계산이었다 — “여가가 소비를 늘린다. 주 5일 일하는 사람이 6일 일하는 사람보다 더 많이 산다.” 100년 전에 한 번 ‘근무일 빼기’를 했던 그 자리에서, 한 칸 더 뺄 수 있느냐는 질문이 다시 나온 셈이다.</p>
<p><strong>둘째, AI가 노동시간 방정식을 다시 흔든다.</strong> 생성형 AI가 같은 산출을 더 적은 시간에 낸다면, 그 잉여를 임금으로 돌릴지 시간으로 돌릴지가 곧 현실 선택지가 된다. 뒤에서 보겠지만 이건 경제학자들과 대기업 CEO들이 이미 공개적으로 말하는 주제다.</p>
<p><strong>셋째, 한국에선 제도가 움직이고 있다.</strong> 경기도가 2024년 50여 개 기관에서 격주 4일제·주 35시간 등을 시범 운영했고, 2026년 1월부터 이를 정책으로 확대하기로 했다. 일본 도쿄도는 2025년 4월부터 도청 직원에게 주 4일 선택지를 줬다. “남의 나라 실험”이 아니라 우리 동네 조례가 됐다.</p></section>''')

# ── 04 evidence + TIMELINE (primary vt) ──
S.append(f'''<section id="section-04">{h2(4,"timeline","데이터는 실제로 무엇을 보여주나")}
<p>먼저 가장 자주 인용되는 실험들을 시간순으로 늘어놓아 보자. 작은 단일 기업에서 시작해 6개국 공동 연구까지, 표본이 어떻게 커져 왔는지가 한눈에 보인다.</p>
<section class="vt-shell" aria-label="주 4일제 주요 실험 타임라인"><div class="vt-frame"><ol class="tl tl-color-cycle">
<li class="tl-item"><b>2018 · 뉴질랜드 Perpetual Guardian</b><p class="vt-text">직원 240명이 8주간 5일치 임금으로 4일 근무. 생산성 약 20% 향상, 스트레스 45%→38%, 워라밸 만족 54%→78%. 이후 영구 도입을 권고. <em>단, 8주·단일 기업이라 일반화는 금물.</em> [출처: CNBC]</p></li>
<li class="tl-item"><b>2019 · 마이크로소프트 재팬</b><p class="vt-text">약 2,300명 대상 8월 한 달 금요일 휴무. 직원당 매출 생산성이 전년 8월 대비 39.9% 상승, 전력 23% 절감. <em>흔히 인용되는 “40%”의 출처가 이것 — 1개월·여름·회의 단축 등이 섞인 수치다.</em> [출처: CNBC / Japan Times]</p></li>
<li class="tl-item"><b>2015–2019 · 아이슬란드 공공부문</b><p class="vt-text">약 2,500명이 임금 삭감 없이 주 40→35~36시간으로. 웰빙이 개선되고 서비스는 유지. <em>주의: 실제 단축은 대부분 주 1~3시간이라 ‘진짜 4일제’와는 거리가 있다 — “아이슬란드가 4일제로 성공”은 과장이다.</em> [출처: Autonomy/CBC, The Conversation]</p></li>
<li class="tl-item"><b>2022 · 영국 4 Day Week Global</b><p class="vt-text">61개 기업·약 2,900명이 6개월간 임금 100% 유지하며 32시간으로. 번아웃 71%↓, 병가 65%↓, 이직 57%↓, 매출은 평균 +1.4%(사실상 보합). 케임브리지·보스턴칼리지 연구진 분석. [출처: Univ. of Cambridge]</p></li>
<li class="tl-item"><b>2024 · 1년 후, 그리고 독일</b><p class="vt-text">영국 참여사 1년 추적 결과 최소 89%가 정책 유지, 51%가 영구 전환. 독일에선 45개사·약 900명 파일럿에서 직원 90%가 정신건강 개선을 보고. [출처: CNBC / 4 Day Week Global]</p></li>
<li class="tl-item"><b>2025 · 학술지 게재</b><p class="vt-text">미국·캐나다·아일랜드·영국·호주·뉴질랜드 6개국 141개 조직·2,896명의 전후 데이터가 <em>Nature Human Behaviour</em>에 실렸다. 번아웃·직무만족·정신·신체건강이 모두 유의하게 개선(주당 평균 약 5시간 단축). [출처: Nature Human Behaviour]</p></li>
</ol></div></section>
<p>패턴은 분명하다. 표본이 커지고 추적 기간이 길어져도 <strong>웰빙 지표는 일관되게 좋아진다.</strong> 번아웃·이직·병가 감소는 거의 모든 연구에서 같은 방향을 가리킨다. 적어도 “직원이 더 행복하고 덜 그만둔다”는 부분은 우연으로 보기 어렵다.</p></section>''')

# ── 05 skepticism (contradiction-map) ──
S.append(f'''<section id="section-05">{h2(5,"audit","그 숫자를 믿어도 되나")}
<p>여기서 멈추면 절반짜리 글이다. 위 숫자들을 깐 사람들의 말을 들어야 한다. 그리고 그 비판은 꽤 날카롭다.</p>
<div class="summary-card"><div class="label">{ic("warning")}이 데이터를 의심해야 하는 이유</div><p>
<strong>① 자원한 기업만 참여한다.</strong> 무작위 대조 실험(RCT)이 아니라, “될 것 같다”고 판단한 회사들이 자발적으로 들어온다. 텍사스대 경제학자 대니얼 해머메시는 영국 파일럿 결과에 “거의 비중을 두지 않겠다”며, 설문은 “사람들이 실험에 참여할 의향이 있음을 보여줄 뿐”이라고 했다.<br>
<strong>② 대부분 자기보고(설문)다.</strong> 2025년 <em>Nature</em> 연구조차 RCT가 아니고 대조군이 작으며, 모든 지표가 직원 설문이다. 추가 휴일을 지키려는 동기가 응답을 부풀렸을 수 있다.<br>
<strong>③ ‘생산성’ 수치가 모호하다.</strong> 경제학자 딘 베이커는 “하룻밤 새 생산성을 25% 올리는 정책이라니, 불가능할 만큼 좋은 얘기”라고 꼬집었다. 많은 ‘생산성 향상’은 객관 산출이 아니라 매출·인식 대리지표다.</p></div>
<p>특히 정직하게 짚어야 할 대목이 하나 있다. 영국 파일럿의 매출 효과는 인용처마다 <strong>+1.4%(시범기간 중)에서 +35%(전년 동기 대비 등 다른 기준)까지</strong> 갈린다. 같은 실험인데 산정 방식이 달라 생긴 차이다. 이 글에서 굳이 보수적인 +1.4%를 쓰는 이유가 여기 있다 — 유리한 숫자만 골라 쓰면, 내가 비판하는 그 헤드라인과 똑같아진다.</p>
<p>요컨대 “직원이 행복해진다”는 강하지만, <strong>“생산성이 오른다”는 아직 약하다.</strong> 둘을 같은 신뢰도로 다루면 안 된다.</p></section>''')

# ── 06 reversals (example/사례 + table) ──
S.append(f'''<section id="section-06">{h2(6,"warning","무너진 실험들")}
<p>성공담만 모으면 생존편향이다. 조용히 5일제로 돌아간 곳들을 봐야 그림이 완성된다.</p>
<div class="tbl table-scroll"><table><caption>주 4일제를 철회·축소한 사례 — 무엇이 문제였나</caption><thead><tr><th>사례</th><th>결과</th><th>무너진 지점</th></tr></thead><tbody>
<tr><td>마자르 텔레콤<br>(도이체텔레콤 헝가리)</td><td>2022~2024.2, 약 1년 반 만에 폐지</td><td>300명·설문 100회·인터뷰 50회까지 했지만 “업무 성격·생활 여건상 다수가 효율적으로 일하지 못했다”. 전 직원 균일 적용이 불가능했던 게 핵심.</td></tr>
<tr><td>Yarno<br>(호주 에듀테크)</td><td>약 2년 운영 후 철회</td><td>경영진·클라이언트 미팅 탓에 일부만 금요일을 쉬었고, 그 불일치가 사기 저하와 원망을 낳았다. “생각대로 작동하지 않았다.”</td></tr>
<tr><td>시간당 산출 업종<br>(의료·제조·소매·돌봄)</td><td>구조적으로 도입 난항</td><td>치료의 연속성, 물리적 생산 시간, 상시 영업 커버리지가 필요해 “시간을 압축할 여지”가 적다. 시급 노동자에게 특히 불리.</td></tr>
</tbody></table></div>
<p>철회 사례들의 공통점은 “직원이 게을러서”가 아니다. <strong>일부는 4일, 일부는 5일로 갈리는 ‘부분 도입’의 형평성 문제</strong>와, 애초에 시간을 압축할 수 없는 업무 성격이었다. 즉 실패의 원인은 제도 자체보다 <em>적용 방식과 업종 적합성</em>에 있었다. 이 관찰이 다음 장의 핵심으로 이어진다.</p></section>''')

# ── 07 my_view: 재설계 vs 압축 (wg-17 before→after) ──
S.append(f'''<section id="section-07">{h2(7,"flow","핵심은 ‘압축’이 아니라 ‘재설계’")}
<p>성공한 실험과 무너진 실험을 나란히 놓으니 변수가 보였다. 결정적인 건 “4일이냐”가 아니라 <strong>“같은 일을 4일에 욱여넣었나, 아니면 일을 다시 설계했나”</strong>였다.</p>
<section class="wg-17" aria-labelledby="wg-17-title"><header class="wg-17-head"><p class="wg-17-kicker">두 가지 4일제</p><h2 id="wg-17-title" class="wg-17-title">압축형 4일제 → 재설계형 4일제</h2><div class="wg-17-meta"><span class="wg-17-chip wg-17-chip-branch">압축 → 재설계</span><span class="wg-17-chip">같은 ‘4일’, 다른 결과</span><span class="wg-17-chip wg-17-chip-del">−저가치 회의</span><span class="wg-17-chip wg-17-chip-add">+집중 시간</span></div></header>
<div class="wg-17-block"><h3 class="wg-17-h3"><span class="wg-17-h3-no">1</span> 압축형 — 5일치를 4일에 욱여넣기</h3><p class="wg-17-p">업무량은 그대로 두고 날짜만 줄인다. 결과는 ‘노동 강도 강화(work intensification)’다. 학계는 이 강도 강화가 웰빙과 동기, 나아가 성과까지 갉아먹는다고 본다. 마자르 텔레콤·Yarno가 부딪힌 벽이 여기였다.</p></div>
<div class="wg-17-block"><h3 class="wg-17-h3"><span class="wg-17-h3-no">2</span> 재설계형 — 저가치 일을 덜어내기</h3><p class="wg-17-p">100-80-100 모델(임금 100%·시간 80%·성과 100%)의 진짜 조건은 “덜 중요한 일을 잘라내는 것”이다. 독일 파일럿에서 회의 효율이 52%, 집중력이 32% 올랐다는 건 시간을 압축해서가 아니라 <strong>쓸데없는 회의를 없애서</strong> 나온 숫자다.</p></div>
<div class="wg-17-block"><h3 class="wg-17-h3"><span class="wg-17-h3-no">3</span> 갈림길 — 같은 ‘4일’, 다른 운명</h3><p class="wg-17-p">그래서 “주 4일제가 효과 있나?”는 질문이 애초에 틀렸다. 효과를 가르는 건 날짜 수가 아니라 운영 설계다. 회의·승인·보고 같은 저가치 활동을 도려낼 여지가 있는 조직에선 통하고, 그렇지 못한 조직에선 압축형으로 변질돼 무너진다.</p></div></section>
<p>이 렌즈로 보면 “성공률 89%”와 “1년 반 만에 폐지”가 모순이 아니다. 전자는 재설계에 성공한 표본, 후자는 압축형으로 흘러간 표본이다. 도구가 아니라 <strong>운영의 문제</strong>였던 셈이다.</p></section>''')

# ── 08 history ──
S.append(f'''<section id="section-08">{h2(8,"quote","역사가 주는 단서")}
<p>한 발 물러서면, 노동시간 단축은 200년째 진행 중인 장기 추세다. 1870년 초기 산업국 노동자는 연 3,000시간 이상 일했지만, 오늘날 선진국은 대략 그 절반이다. 독일은 같은 기간 약 60% 줄었다. 큰 그림에서 ‘근무일 빼기’는 예외가 아니라 흐름이다.</p>
<p>그 흐름 속에 유명한 빗나간 예언이 하나 있다. 케인스는 1930년 「우리 손주 세대의 경제적 가능성」에서 기술 진보 덕에 후대는 <strong>주 15시간</strong>만 일하게 되리라 봤다. “하루 3시간이면 우리 안의 ‘늙은 아담’을 만족시키기 충분하다”고 썼다. 생산성만 보면 그가 옳았다 — 우리는 그가 예상한 만큼 부유해졌다. 그런데 노동시간은 15시간 근처에도 못 갔다.</p>
<p>왜 빗나갔나. 경제사학자 니컬러스 크래프츠는 케인스가 <strong>불평등 확대</strong>(중위소득이 예상보다 더디게 상승)와 <strong>끝없이 새로 생기는 소비 욕구</strong>(신상품·광고)를 과소평가했다고 본다. 더 부유해진 만큼 시간을 산 게 아니라, 더 많은 것을 사느라 시간을 계속 팔았다는 것이다. 앞서 본 켈로그 6시간제의 종말 — 노동자들이 더 벌려고 시간을 되늘린 그 장면 — 과 정확히 같은 이야기다.</p>
<p>역사의 단서는 이렇다. 생산성이 오른다고 노동시간이 자동으로 줄지는 않는다. <strong>줄어든 시간을 ‘소비를 늘릴 기회’로 볼지 ‘삶을 늘릴 기회’로 볼지는 정책과 문화의 선택</strong>이다. 주 4일제 논쟁은 결국 그 선택에 관한 것이다.</p></section>''')

# ── 09 AI + Korea (future + home) ──
S.append(f'''<section id="section-09">{h2(9,"impact","AI, 그리고 한국 이야기")}
<p>그 선택을 지금 가장 세게 떠미는 변수가 AI다. 경제학자 줄리엣 쇼어는 AI가 생산성을 끌어올릴 때 <strong>“일자리당 노동시간을 줄이는 것”이 더 많은 사람의 고용을 유지하는 강력한 방법</strong>이라고 주장한다 [주장 주체: Schor]. JP모건 CEO 제이미 다이먼은 2025년 한 포럼에서 “20~40년 뒤 선진국은 주 3.5일 일하게 될 것”이라 내다봤다 [주장 주체: Dimon] — 다만 그는 같은 입에서 “AI가 일자리를 없앤다. 모래에 머리를 묻지 말라”고 경고했다. 노벨상 수상자 크리스토퍼 피사리데스도 비슷한 전망을 내놓았다 [주장 주체: Pissarides].</p>
<p>물론 이건 모두 <strong>예측</strong>이다 [추론]. AI가 만든 잉여가 시간으로 갈지, 더 많은 산출 요구로 갈지는 정해져 있지 않다 — 켈로그와 케인스가 보여줬듯, 잉여는 늘 ‘더 많이’ 쪽으로도 흐른다.</p>
<p>한국은 이 논쟁에서 가장 절박한 자리에 있다. OECD에 따르면 한국 노동자는 2024년 연 <strong>1,865시간</strong> 일해 세계 평균(1,736시간)을 웃돈다. 주 52시간제를 둘러싼 논쟁이 아직 안 끝났고, 한쪽에선 노동시간 상한을 더 늘리자는 주장도 나온다. 그 와중에 경기도는 2026년부터 단축근무 시범을 정책으로 확대한다. 장시간 노동의 대명사였던 나라가 ‘근무일 빼기’를 진지하게 실험하기 시작한 것 자체가, 이 질문이 더는 남의 일이 아님을 보여준다.</p></section>''')

# ── 10 how_to_start ──
S.append(f'''<section id="section-10">{h2(10,"check","도입을 고민한다면")}
<p>여기까지 왔다면 결론은 “좋다/나쁘다”가 아니라 “어떻게”라는 데 동의했을 것이다. 조직에서 진지하게 고민한다면, 무너진 실험들이 남긴 교훈을 체크리스트로 정리하면 이렇다.</p>
<ul>
<li><strong>압축하지 말고 재설계하라.</strong> 가장 먼저 할 일은 “하루를 빼는 것”이 아니라 “저가치 회의·승인·보고를 도려내는 것”이다. 잘라낼 게 없다면 그 조직은 아직 준비가 안 된 것이다.</li>
<li><strong>자기보고 말고 진짜 산출을 재라.</strong> 직원 만족 설문만으로 판단하지 말고, 객관적 산출·납기·품질 지표를 함께 본다. 가능하면 비교할 대조 팀을 둔다 — 호손 효과를 의심하라.</li>
<li><strong>업종 적합성을 먼저 본다.</strong> 시간당 산출이 곧 서비스인 일(의료·제조·접객)은 인력 충원 없이는 ‘부분 도입’이 형평성 문제로 번진다. 마자르 텔레콤의 교훈이다.</li>
<li><strong>‘부분 도입’의 원망을 설계로 막아라.</strong> 누구는 쉬고 누구는 못 쉬는 구조를 방치하면 사기가 먼저 무너진다. 팀 단위·교대 설계로 형평을 맞춘다.</li>
<li><strong>유리한 숫자만 인용하지 마라.</strong> 내부 보고든 외부 홍보든, +1.4%와 +35%가 있으면 보수적인 쪽을 기준으로 삼아야 신뢰가 쌓인다.</li>
</ul></section>''')

# ── 11 closing + soft-cta ──
S.append(f'''<section class="try soft-cta" id="section-11">{h2(11,"success","마무리 — 4일이 아니라 ‘어떻게’")}
<p>긴 글이었지만 결론은 한 문장으로 줄어든다. <strong>주 4일제는 환상이 아니다. 하지만 ‘주 5일을 4일에 욱여넣기’는 환상이다.</strong> 데이터가 일관되게 보여주는 건 “직원이 더 건강하고 덜 그만둔다”는 것이고, 약한 건 “생산성이 저절로 오른다”는 약속이다. 그 둘을 구분하는 순간, 논쟁은 응원전에서 설계 문제로 바뀐다.</p>
<p>그래서 당신에게 권하는 실천은 거창하지 않다. 딱 두 가지다.</p>
<ol>
<li><strong>당신의 캘린더에서 회의 하나를 지워보라.</strong> 이번 주, 가장 가치 낮은 정기 회의 하나를 없애고 그 시간에 무슨 일이 생기는지 보라. 4일제의 핵심 동작은 바로 이 ‘재설계’다 — 작게 먼저 해볼 수 있다.</li>
<li><strong>숫자를 만나면 출처를 물어라.</strong> “생산성 40%↑” 같은 헤드라인을 보면, 무슨 표본·기간·측정인지 한 번만 되물어보라. 그 습관 하나가 환상과 데이터를 가른다.</li>
</ol>
<p>100년 전 포드가 토요일을 뺐을 때도, 사람들은 “일이 안 돌아갈 것”이라 했다. 한 칸을 더 뺄 수 있을지는, 날짜가 아니라 <strong>우리가 일을 다시 설계할 의지가 있느냐</strong>에 달렸다.</p></section>''')

# ── 12 sources + meta (storm 출처 규칙 이행) ──
S.append(f'''<section id="section-12">{h2(12,"reference","참고한 자료 · 메타")}
<aside class="source-note"><div class="label">{ic("source")}출처 (모든 수치는 아래 공개 자료에서 확인)</div>
<p><strong>실험·데이터</strong> · {a("https://www.sociology.cam.ac.uk/news/new-results-worlds-largest-trial-four-day-working-week","케임브리지대 — 영국 2022 파일럿 결과")} · {a("https://www.cnbc.com/2024/02/22/four-day-working-week-most-firms-in-worlds-biggest-trial-stick-to-it.html","CNBC — 1년 후 89% 유지")} · {a("https://www.nature.com/articles/s41562-025-02259-6","Nature Human Behaviour(2025) — 6개국 연구")} · {a("https://www.cnbc.com/2018/07/19/new-zealand-experiment-finds-4-day-work-week-a-success.html","CNBC — Perpetual Guardian(뉴질랜드)")} · {a("https://www.cnbc.com/2019/11/04/microsoft-japan-4-day-work-week-experiment-sees-productivity-jump-40percent.html","CNBC — 마이크로소프트 재팬")} · {a("https://www.4dayweek.com/germany-2024-pilot-results","4 Day Week Global — 독일 2024 파일럿")}</p>
<p><strong>회의론·반례</strong> · {a("https://wol.iza.org/opinions/four-day-workweek","IZA World of Labor — 해머메시")} · {a("https://www.techtarget.com/searchhrsoftware/news/252525395/Four-day-workweek-productivity-claims-gather-criticism","TechTarget — 생산성 주장 비판(해머메시·딘 베이커)")} · {a("https://www.scientificamerican.com/article/biggest-trial-of-four-day-workweek-finds-workers-are-happier-and-feel-just/","Scientific American — 자기보고 한계")} · {a("https://theconversation.com/the-success-of-icelands-four-day-week-trial-has-been-greatly-overstated-164083","The Conversation — 아이슬란드 과장 지적")} · {a("https://www.telekom.hu/about_us/press_room/press_releases/2024/february_13","마자르 텔레콤 — 폐지 보도자료")} · {a("https://www.yarno.com.au/blog/4-day-work-week-failure","Yarno — 철회 회고")} · {a("https://www.apa.org/monitor/2025/01/rise-of-4-day-workweek","APA Monitor — 노동 강도 강화")}</p>
<p><strong>역사·미래</strong> · {a("https://www.history.com/this-day-in-history/may-1/ford-factory-workers-get-40-hour-week","HISTORY — 포드 주 40시간(1926)")} · {a("https://www.informationweek.com/it-leadership/six-hour-shifts-satisfied-kellogg-s-appetite-for-productivity","InformationWeek — 켈로그 6시간제")} · {a("https://www.marxists.org/reference/subject/economics/keynes/1930/our-grandchildren.htm","케인스(1930) 원문 — 주 15시간 예측")} · {a("https://ourworldindata.org/working-more-than-ever","Our World in Data — 노동시간 장기 추세")} · {a("https://www.weforum.org/stories/2025/10/four-day-week-work-jobs-and-skills/","WEF — AI와 노동시간(Schor)")} · {a("https://fortune.com/2026/04/06/jpmorgan-ceo-jamie-dimon-ai-cut-workweek-3-5-days-gen-z-developing-eq-important/","Fortune — 다이먼 ‘주 3.5일’ 전망")} · {a("https://www.seoulz.com/korea-4-5-day-workweek-2026/","Seoulz — 한국·경기도 2026")}</p>
<p><strong>메타 설명</strong>: 주 4일 근무제를 둘러싼 실증 데이터·회의론·노동시간 역사를 출처 기반으로 검증한 분석 글. “주 4일제는 환상이 아니지만, 압축형은 환상”이라는 관점에서 성공·실패 사례를 가르는 변수(압축 vs 재설계)를 짚는다.</p>
<p><strong>태그</strong>: #주4일제 #노동시간 #생산성 #일의미래 #100_80_100 #근거점검 #케인스 #AI와노동</p>
<p><strong>제작 노트</strong>: 주제 탐색과 출처 수집은 storm-research 방식(3개 관점 병렬 조사 — 학술·회의론·역사/미래, 모든 주장에 출처, 추정은 [추론] 표기)으로 했고, 글쓰기는 adaptive-html-blog-writer-v2 방법론(제목 4계열·Hook→문제→근거→반론→관점→실행→CTA·과장어 금지)을 따랐다. HTML 렌더는 adaptive-html-final 5.10.5 blog_writer 모드(무 JS·8테마·타임라인·wg-17 before/after)다. 일부 미래 전망과 매체 간 수치 불일치(예: 영국 매출 +1.4% vs +35%)는 본문에 그대로 노출해 보수적 수치를 기준으로 삼았다.</p></aside></section>''')

MAIN_INNER = HEADER + TOC + ''.join(S)
ex = EX.read_text(encoding="utf-8")
new = re.sub(r'(<main\s+id="main"[^>]*>)[\s\S]*(</main>)', lambda m: m.group(1)+MAIN_INNER+m.group(2), ex, count=1)
OUT.write_text(new, encoding="utf-8")
vis=re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',re.sub(r'<style[\s\S]*?</style>','',MAIN_INNER))).strip()
print("빌드 완료:", OUT.name, "| 크기:", len(new), "| 섹션:", len(S), "| 본문:", len(vis), "자")
print("tl-item:", new.count("tl-item"), "| wg-17 head:", new.count('wg-17-title'), "| try soft-cta:", new.count('try soft-cta'), "| 출처 링크:", new.count('target="_blank"'))
