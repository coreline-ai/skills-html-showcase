#!/usr/bin/env python3
# 하이브리드 빌더(확장판): adaptive-html-blog-writer-v2 방법론 → adaptive-html-final 5.10.5 blog_writer.
import json, re, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[3]
SKILL = ROOT / "skills/adaptive-html-final"
EX = SKILL / "examples/05_blog_deepwork_4day_retro.html"
OUT = pathlib.Path(__file__).resolve().parent / "index.html"
ICONS = {d["id"]: d["svg"] for d in json.load(open(SKILL/"assets/body-icons.json", encoding="utf-8"))}
def ic(k): return f'<span class="body-icon body-icon--sm">{ICONS[k]}</span>'
def h2(n,k,t): return f'<h2>{ic(k)}<span class="num">{n}</span>{t}</h2>'

HEADER = (
'<header class="header"><div class="kicker"><span class="kicker-text">PERSONAL BLOG · 경험담</span></div>'
'<h1>AI에게 코딩을 맡기고 6개월, 다시 손으로 짜기 시작한 이유</h1>'
'<p class="sub hook">반년 동안 거의 모든 코드를 에이전트에게 맡겼다. 분명히 빨라졌는데, 어느 날 내가 머지한 코드를 내가 설명하지 못했다. 속도를 잃지 않으면서 그 감각을 되찾으려고 바꾼 습관들을 적는다 — AI를 끄자는 이야기가 아니다.</p>'
'<div class="meta"><span>blog_writer</span><span>personal-blog-essay.html</span><span>page-wide layout-blog</span><span>adaptive-html-final v5.10.5</span><span>무 JS</span><span>6개월 회고</span></div>'
'<div class="generated-row"><p class="generated-date">2026-06-20 · 개인 경험 기록 (수치는 내 작업 로그 기준)</p>'
'<div class="lens-strip" aria-label="태그"><span class="lens-strip-label">TAGS</span><span class="lens-chip">AI 페어프로그래밍</span><span class="lens-chip">개발 습관</span><span class="lens-chip">코드 리뷰</span><span class="lens-chip">러닝커브</span><span class="lens-chip">회고</span></div></div></header>'
)

TOC_ITEMS=[("처음엔 마법 같았다","section-01"),("제목을 이렇게 골랐다","section-02"),("6개월의 타임라인","section-03"),("결제 버그의 밤","section-04"),("속도와 이해는 다른 축이다","section-05"),("내 워크플로, 무엇을 바꿨나","section-06"),("지금 지키는 세 가지 습관","section-07"),("동료들도 비슷했다","section-08"),("그럼 AI를 쓰지 말라는 거냐","section-09"),("마무리 — 다음 PR에서","section-10"),("메타·태그","section-11")]
TOC=('<nav class="toc-map" aria-label="문서 목차"><span class="label">문서 목차</span><p>경험담의 흐름(문제→관점→사례→실행)을 chip-nav로 이동합니다.</p><div class="toc-pills">'
     +''.join(f'<a class="toc-pill" href="#{sid}"><b>{i+1}</b>{t}</a>' for i,(t,sid) in enumerate(TOC_ITEMS))+'</div></nav>')

S=[]

S.append(f'''<section id="section-01">{h2(1,"edit","처음엔 마법 같았다")}
<div class="lede-note"><div class="label">HOOK</div><p>작년 말, 나는 에디터에서 직접 타이핑하는 시간을 거의 0으로 만들었다. 기능을 한 문단으로 설명하면 에이전트가 파일 여러 개를 동시에 고치고, 테스트를 돌리고, 빨간 줄이 사라질 때까지 스스로 반복했다. 첫 2주는 솔직히 황홀했다 — 금요일 오후에 끝낼 일을 수요일 점심에 끝냈으니까.</p></div>
<p>그 시절의 나를 한 장면으로 요약하면 이렇다. 모니터 앞에 앉아 "결제 실패 시 3회까지 지수 백오프로 재시도하고, 그래도 실패하면 데드레터 큐로 보내줘"라고 적는다. 90초 뒤, 네 개 파일에 걸친 diff가 올라온다. 테스트도 같이 짜여 있다. 전부 초록불. 나는 diff를 위에서 아래로 스크롤하며 "음, 그럴듯하네" 하고 승인 버튼을 누른다. 키보드로 코드를 친 기억은 없다. 그저 <em>읽고, 끄덕이고, 머지</em>했다.</p>
<p>속도는 거짓말을 하지 않았다. 그 분기 내 PR 수는 평소의 1.6배였고, 팀에서 "요즘 일 많이 한다"는 말을 들었다. 나는 그게 실력이 늘어난 거라고 생각했다. 적어도 3월의 그 밤 전까지는.</p>
<p>이 글은 그 밤 이후 6개월 동안 내가 무엇을 잃을 뻔했고, 속도를 포기하지 않으면서 그걸 어떻게 되찾았는지에 대한 기록이다. 거창한 방법론이 아니라, 한 사람의 작업 로그에 가깝다. 그리고 미리 말해두면 — <strong>결론은 "AI를 끄자"가 아니다.</strong></p></section>''')

S.append(f'''<section id="section-02">{h2(2,"compare","제목을 이렇게 골랐다")}
<p>(메타) 블로그는 제목이 절반이라, 본문에 들어가기 전에 제목부터 네 계열로 뽑아봤다. 다만 규칙을 하나 걸었다 — <strong>본문에서 증명 못 할 과장은 쓰지 않는다.</strong> "충격", "무조건", "이것만 알면" 같은 단어는 클릭은 끌어도 글의 신뢰를 깎는다.</p>
<div class="summary-card"><div class="label">제목 후보 (4계열)</div><p><strong>검색형</strong> — "AI 코딩 6개월 후기: 다시 손으로 짜는 이유" <br><strong>클릭형</strong> — "내가 머지한 코드를 내가 설명하지 못했다" <br><strong>전문가형</strong> — "AI 페어프로그래밍의 숨은 비용: 이해의 외주화" <br><strong>초보자형</strong> — "AI로 코딩을 시작한 사람이 꼭 한 번은 들어야 할 이야기"</p></div>
<p>최종으로는 클릭형의 궁금증과 전문가형의 무게를 섞은 지금 제목을 골랐다. "다시 손으로 짜기 시작한 이유"는 독자에게 질문 하나를 던진다 — 더 빠른 도구를 두고 왜 느린 길로 돌아갔을까? 이 글 전체가 그 한 질문에 대한 대답이다. 제목이 약속한 것을 본문이 지킬 수 있는가, 그 기준 하나만 통과시켰다.</p></section>''')

S.append(f'''<section id="section-03">{h2(3,"timeline","6개월의 타임라인")}
<p>되돌아보면 변화는 한 번에 오지 않았다. 환희에서 불안으로, 불안에서 실험으로 — 한 달 단위로 감각이 어떻게 바뀌었는지 적어둔 메모를 거의 그대로 옮긴다.</p>
<section class="vt-shell" aria-label="AI 코딩 6개월 변화 타임라인"><div class="vt-frame"><ol class="tl tl-color-cycle">
<li class="tl-item"><b>1개월 · 황홀기</b><p class="vt-text">속도에 취했다. PR 수는 평소의 1.6배, 야근은 줄었다. "이제 타이핑은 끝났다"고 농담했다. 코드 리뷰는 diff를 훑고 테스트 초록불만 확인하는 의식이 됐다. 이때의 나는 도구가 곧 실력이라고 믿었다.</p></li>
<li class="tl-item"><b>2개월 · 미세한 불편</b><p class="vt-text">스탠드업에서 동료의 질문에 막히기 시작했다. "여기 왜 락을 이렇게 잡았어요?" → "음… 에이전트가 그렇게 짰는데, 한 번 볼게요." 그 "한 번 볼게요"가 쌓였다. 처음엔 대수롭지 않게 넘겼다.</p></li>
<li class="tl-item"><b>3개월 · 결제 버그의 밤</b><p class="vt-text">내가 2주 전에 머지한 코드에서 간헐적 버그가 터졌다. 그런데 그 코드가 낯설었다. 디버깅에 평소의 세 배가 걸렸다. 내 이름이 커밋에 박혀 있는데 남의 코드를 읽는 기분 — 이날이 전환점이었다.</p></li>
<li class="tl-item"><b>4개월 · 의심과 실험</b><p class="vt-text">"내가 정말 이걸 할 줄 아는가?"라는 질문이 떠나지 않았다. 하루 한 번은 AI를 끄고 작은 기능을 직접 짜보기로 했다. 느렸다. 부끄러울 만큼. 그런데 막히는 지점에서 "왜"가 다시 보이기 시작했다.</p></li>
<li class="tl-item"><b>5개월 · 경계선 찾기</b><p class="vt-text">전부 손으로도, 전부 위임도 답이 아니었다. 설계와 핵심 로직은 손으로 먼저, 반복·보일러플레이트·테스트 골격은 에이전트로. 무엇을 어느 쪽에 둘지의 경계선을 매주 조금씩 옮겨봤다.</p></li>
<li class="tl-item"><b>6개월 · 새 균형</b><p class="vt-text">속도는 황홀기의 약 80% 수준으로 안착했다. 대신 디버깅에 쓰는 시간은 황홀기보다 오히려 줄었다 — 내가 코드를 이해하고 있으니까. 잃은 20%의 속도로 잃을 뻔한 이해를 되샀다고 지금은 생각한다.</p></li>
</ol></div></section>
<p>숫자는 전부 내 작업 로그 기준이라 일반화할 수는 없다. 다만 곡선의 모양 — <em>빠른 환희 → 조용한 침식 → 의식적 회복</em> — 은 나중에 이야기 나눈 동료들에게서도 반복해서 들렸다.</p></section>''')

S.append(f'''<section id="section-04">{h2(4,"warning","결제 버그의 밤")}
<p>그 밤을 좀 더 자세히 적어야겠다. 이 글에서 가장 중요한 장면이기 때문이다.</p>
<p>금요일 밤 11시, 결제 실패율이 평소의 다섯 배라는 알림이 왔다. 로그를 열어보니 재시도 로직이 어떤 조건에서 무한 루프에 가깝게 돌고 있었다. 문제의 파일을 열었다 — 2주 전 내가 "머지"한, 그 90초 만에 만들어진 재시도 코드였다.</p>
<p>그런데 코드를 읽는데 손이 멈췄다. 백오프 계산식에 내가 모르는 변수가 있었고, 예외 분기 하나가 왜 거기 있는지 짐작이 안 갔다. 나는 그 코드를 <strong>처음 보는 사람처럼</strong> 읽고 있었다. 결국 원인을 찾는 데 두 시간이 걸렸다. 직접 짠 코드였다면 20분이면 됐을 버그였다.</p>
<p>그날의 진짜 충격은 버그 자체가 아니었다. "내가 승인한 코드인데 내가 모른다"는 사실이었다. 테스트는 초록불이었다. 하지만 테스트는 <em>내가 상상한 경우</em>만 검증한다. 내가 상상하지 못한 경계 조건 — 정확히 그 지점에서 버그가 났고, 그건 코드를 직접 짜며 "이 부분이 좀 위험한데" 하고 손끝으로 느꼈어야 할 종류의 위험이었다. 위임은 그 감각의 입력을 통째로 건너뛰게 했다.</p></section>''')

S.append(f'''<section id="section-05">{h2(5,"idea","속도와 이해는 다른 축이다")}
<p>이 경험을 한 문장으로 줄이면 이렇다. <strong>생산성이 올라가는 것과 내 실력이 올라가는 것은 같은 축이 아니다.</strong> 둘은 평소엔 같이 가지만, AI에 깊이 의존하면 갈라진다 — 산출물은 늘고 이해는 준다.</p>
<p>나중에 찾아보니 비슷한 신호가 연구에도 있었다. AI 보조가 단기 과제 완료는 빠르게 하지만, 개념 이해·디버깅 평가에서는 오히려 점수가 낮아진다는 통제 실험이 있었고(효과크기가 작지 않았다), 여러 연구를 묶은 메타분석에서는 "학습" 효과가 통계적으로 0과 잘 구분되지 않았다. 즉 측정된 건 실력이 아니라 <em>도구가 옆에 있을 때의 성과</em>였던 셈이다. 도구를 치우면 남는 게 별로 없는. 내 결제 버그의 밤이 데이터로도 설명되는 느낌이었다.</p>
<p>오해는 말자. 이건 "AI가 사람을 멍청하게 만든다"는 이야기가 아니다. <strong>근육에 가깝다.</strong> 무거운 걸 기계가 늘 대신 들어주면 몸은 편하다. 문제는 들지 않은 근육이 자란다고 <em>착각</em>하게 된다는 것이다. 매일 지게차로 짐을 옮기면서 "나 요즘 힘 좋아졌어"라고 말하는 격이다. 힘이 좋아진 건 지게차다.</p>
<p>그래서 질문이 "AI냐 아니냐"에서 "무엇을 위임하고 무엇을 직접 드느냐"로 바뀌었다. 이해가 길게 자산이 되는 영역에서는 일부러 손으로 든다. 반복이 그냥 비용인 영역에서는 기꺼이 지게차를 쓴다. 도구 탓이 아니라 배분의 문제였다.</p></section>''')

S.append(f'''<section id="section-06">{h2(6,"flow","내 워크플로, 무엇을 바꿨나")}
<p>그래서 워크플로를 다시 짰다. 무엇을 빼고 무엇을 더했는지, before→after로 정리하면 이렇다.</p>
<section class="wg-17" aria-labelledby="wg-17-title"><header class="wg-17-head"><p class="wg-17-kicker">워크플로 변경 요약</p><h2 id="wg-17-title" class="wg-17-title">위임 우선 워크플로 → 검증자 우선 워크플로</h2><div class="wg-17-meta"><span class="wg-17-chip wg-17-chip-branch">위임-우선 → 검증자-우선</span><span class="wg-17-chip">6개월 관찰</span><span class="wg-17-chip wg-17-chip-add">+3 습관</span><span class="wg-17-chip wg-17-chip-del">−2 습관</span></div></header>
<div class="wg-17-block"><h3 class="wg-17-h3"><span class="wg-17-h3-no">1</span> 뺀 것 — "diff 훑고 머지"</h3><p class="wg-17-p">테스트만 초록불이면 승인하던 습관을 버렸다. 테스트는 내가 모르는 것을 모르고, 미묘한 보안·경계 버그는 초록불 뒤에 숨는다. 결제 버그가 정확히 그랬다. 지금은 diff를 "검토"가 아니라 "내가 쓴 것처럼 읽기"로 대한다.</p></div>
<div class="wg-17-block"><h3 class="wg-17-h3"><span class="wg-17-h3-no">2</span> 뺀 것 — "전부 위임이 기본값"</h3><p class="wg-17-p">예전엔 모든 작업의 첫 동작이 "에이전트에게 시키기"였다. 지금은 작업을 받으면 먼저 5초간 묻는다 — "이건 내가 이해해야 하는 코드인가, 그냥 빨리 치워야 하는 코드인가?" 그 분류가 모든 걸 바꿨다.</p></div>
<div class="wg-17-block"><h3 class="wg-17-h3"><span class="wg-17-h3-no">3</span> 더한 것 — "먼저 손으로, 그다음 위임"</h3><p class="wg-17-p">새 로직은 거칠게라도 내가 먼저 스케치한다. 그 뒤 에이전트에게 다듬고 채우게 한다. 순서만 바꿨을 뿐인데 AI 산출물을 읽는 눈이 달라졌다 — 비교 대상(내 초안)이 있으니, 에이전트가 다르게 짠 부분이 곧 "내가 놓친 것 또는 에이전트가 틀린 것"으로 또렷이 보인다.</p></div>
<div class="wg-17-block"><h3 class="wg-17-h3"><span class="wg-17-h3-no">4</span> 더한 것 — "설명 못 하면 머지 안 함"</h3><p class="wg-17-p">스스로에게 건 규칙. PR을 올리기 전에 "이게 왜 동작하는가"를 한 문단으로 적을 수 없으면 머지하지 않는다. 적는 과정에서 버그를 두 번 잡았고, 한 번은 더 단순한 설계를 발견했다.</p></div></section>
<p>이걸 매번 직감으로 정하긴 어려워서, 작업이 들어오면 빠르게 분류하는 기준표를 만들어 책상 옆에 붙여뒀다.</p>
<div class="tbl table-scroll"><table><caption>무엇을 위임하고 무엇을 직접 드는가 — 내 기본값(상황 따라 조정)</caption><thead><tr><th>작업 유형</th><th>기본 선택</th><th>이유</th></tr></thead><tbody>
<tr><td>핵심 비즈니스 로직</td><td>직접 짠 뒤 다듬기만 위임</td><td>오래 유지보수하고, 이해 자체가 자산이 되는 코드</td></tr>
<tr><td>보안·인증·결제</td><td>직접 (검증자 모드)</td><td>경계·예외 버그가 가장 비싸다 — 결제 버그의 밤이 그랬다</td></tr>
<tr><td>보일러플레이트·CRUD</td><td>위임</td><td>반복은 그냥 비용. 읽되 깊이 파지 않는다</td></tr>
<tr><td>테스트 골격</td><td>위임 후 케이스 보강</td><td>틀은 빠르게, 내가 상상한 경계 케이스는 직접 추가</td></tr>
<tr><td>낯선 기술 학습</td><td>위임 금지 · "교사"로 사용</td><td>코드를 받지 말고 "왜?"를 되물어 직접 변형해본다</td></tr>
<tr><td>일회성 스크립트</td><td>전적 위임</td><td>곧 버릴 코드에 이해를 투자하지 않는다</td></tr>
</tbody></table></div>
<p>기준표의 핵심은 정답이 아니라 <strong>"5초 멈춤"</strong>이다. 작업을 받자마자 위임 버튼을 누르는 대신, 이게 어느 칸인지 한 번 묻는 그 5초가 6개월 전의 나와 지금의 나를 가른다.</p></section>''')

S.append(f'''<section id="section-07">{h2(7,"check","지금 지키는 세 가지 습관")}
<p>거창한 방법론은 아니다. 6개월 시행착오 끝에 남은, 작고 매일 지킬 수 있는 규칙 세 개다. 거창하지 않아서 지켜진다.</p>
<ul>
<li><strong>하루 한 번은 AI를 끈다.</strong> 짧은 함수 하나, 작은 버그 하나라도 처음부터 손으로 짠다. 느리지만 "왜"의 근육을 유지하는 최소한의 운동이다. 헬스장 가듯, 매일 조금.</li>
<li><strong>AI 코드도 "내 코드"의 기준으로 읽는다.</strong> 생성된 코드라고 리뷰 기준을 낮추지 않는다. 모르는 API·패턴이 나오면 그 자리에서 찾아 이해하고 넘어간다. "나중에 보자"의 나중은 결제 버그의 밤으로 온다.</li>
<li><strong>"설명 가능성"을 머지 게이트로 둔다.</strong> 동작하는 코드가 아니라 <em>설명되는 코드</em>를 머지한다. 셋 중 효과가 가장 컸고, 부수 효과로 PR 설명의 질도 같이 올라갔다.</li>
</ul>
<p>이 세 가지를 지키면서도 속도는 황홀기의 80% 수준은 유지된다. 완벽한 균형은 아니지만, 적어도 내가 무엇을 만들고 있는지 아는 상태로 빠르다.</p></section>''')

S.append(f'''<section id="section-08">{h2(8,"user","동료들도 비슷했다")}
<p>처음엔 나만 뒤처진 줄 알았다. "다들 잘 쓰는데 나만 적응을 못 하나" 싶었다. 그래서 조심스럽게 팀과 다른 회사 친구들에게 물어봤는데, 의외로 같은 곡선을 그린 사람이 많았다.</p>
<p>한 시니어는 "주니어 리뷰가 갑자기 어려워졌다"고 했다. 예전엔 코드를 보면 그 사람이 어디까지 이해했는지 보였는데, 이제는 잘 짠 코드인데도 본인이 설명을 못 하는 경우가 늘었다는 것이다. 또 다른 친구는 "산출물은 늘었는데 팀의 집단 지식은 얇아지는 느낌"이라고 표현했다. 코드는 쌓이는데, 그 코드를 진짜로 아는 사람은 줄어드는 상태.</p>
<p>물론 반대 경우도 있었다. AI를 "더 빨리 배우는 도구"로 쓰는 사람들이다. 모르는 코드가 나오면 에이전트에게 "이거 왜 이렇게 동작해?"라고 되묻고, 설명을 듣고, 직접 변형해본다. 같은 도구인데 결과가 갈렸다. 차이는 도구가 아니라 <strong>"위임"으로 쓰느냐 "교사"로 쓰느냐</strong>였다.</p></section>''')

S.append(f'''<section id="section-09">{h2(9,"question","그럼 AI를 쓰지 말라는 거냐")}
<p>가장 많이 받은 반론이라 선제적으로 답해둔다. <strong>전혀 아니다.</strong> 나는 지금도 매일 에이전트를 쓰고, 보일러플레이트·리팩터링·테스트 골격·일회성 스크립트에서는 위임이 압도적으로 빠르다. 이 글도 자료 정리에 도구의 도움을 받았다.</p>
<p>요지는 "끄자"가 아니라 <strong>"무엇을 위임할지 내가 정하자"</strong>다. 이해가 자산이 되는 영역(핵심 로직·보안·아키텍처·내가 오래 유지보수할 코드)은 직접 들고, 반복이 그냥 비용인 영역은 기꺼이 넘긴다. 위임의 기본값을 "전부"에서 "선택"으로 바꾼 것뿐이다.</p>
<p>특히 막 시작하는 주니어라면 더 그렇다고 생각한다. 아직 한 번도 길러본 적 없는 근육을 기계가 처음부터 대신 들어주면, 그 근육은 영영 생기지 않는다. 도구의 속도와 자신의 기본기는 분리해서 키우는 게 — 역설적이지만 — 길게 보면 둘 다 빨라지는 길이다. 기본기가 있어야 도구를 의심할 줄 알고, 의심할 줄 알아야 도구를 안전하게 빨리 쓸 수 있다.</p></section>''')

S.append(f'''<section class="try" id="section-10">{h2(10,"decision","마무리 — 다음 PR에서")}
<p>긴 이야기였지만 실천은 단순하다. 당신의 다음 PR에서 딱 두 가지만 해보길 권한다. 6개월짜리 깨달음을 5분으로 압축하면 이거다.</p>
<ol>
<li><strong>머지 전 한 문단.</strong> "이 변경이 왜 동작하는가"를 PR 설명에 한 문단으로 적어보라. 술술 적히면 좋고, 못 적겠으면 그게 바로 신호다 — 당신은 아직 그 코드를 모른다.</li>
<li><strong>오늘 하루, 함수 하나는 손으로.</strong> AI를 끄고 작은 것 하나를 직접 짜보라. 느린 만큼, 그 느림 속에서 보이는 것이 있다.</li>
</ol>
<p>속도는 도구가 준다. 이해는 아무도 대신 길러주지 않는다. 그 둘을 같은 것으로 착각하지 않는 것 — 6개월의 결론은 그게 전부다. 다시 손으로 짜기 시작한 건, 느리게 가려는 게 아니라 <strong>내가 만든 것을 계속 알고 있기 위해서</strong>였다.</p></section>''')

S.append(f'''<section id="section-11">{h2(11,"reference","메타·태그")}
<aside class="source-note"><div class="label">{ic("reference")}Blog Meta · adaptive-html-blog-writer-v2 × adaptive-html-final</div>
<p><strong>메타 설명</strong>: AI 코딩 에이전트에 6개월 의존한 뒤 다시 손코딩을 병행하게 된 개인 회고. "속도와 이해는 다른 축"이라는 관점에서, 워크플로를 '위임 우선'에서 '검증자 우선'으로 바꾼 과정과 지금 지키는 세 가지 습관을 정리한다.</p>
<p><strong>태그</strong>: #AI페어프로그래밍 #개발습관 #코드리뷰 #러닝커브 #회고 #검증자모드 #손코딩</p>
<p><strong>제작 노트</strong>: 글쓰기 방법론(제목 4계열·Hook→문제→관점→사례→실행→CTA 흐름·본문 밀도·과장어 금지·톤)은 adaptive-html-blog-writer-v2 규칙을 따랐고, editorial HTML 렌더는 adaptive-html-final 5.10.5 blog_writer 모드(무 JS·8테마·타임라인·wg-17 before/after)로 했다. 본문 수치는 글쓴이 개인 작업 로그 기준의 회고이며 일반화된 통계가 아니다. §5에서 언급한 학습 관련 연구 경향은 공개된 통제 실험·메타분석의 결을 요약한 것으로, 정확한 수치는 원 논문에서 확인하길 권한다.</p></aside></section>''')

MAIN_INNER = HEADER + TOC + ''.join(S)
ex = EX.read_text(encoding="utf-8")
new = re.sub(r'(<main\s+id="main"[^>]*>)[\s\S]*(</main>)', lambda m: m.group(1)+MAIN_INNER+m.group(2), ex, count=1)
OUT.write_text(new, encoding="utf-8")
vis=re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',re.sub(r'<style[\s\S]*?</style>','',MAIN_INNER))).strip()
print("빌드 완료:", OUT, "| 크기:", len(new), "| 섹션:", len(S), "| 본문:", len(vis), "자")
