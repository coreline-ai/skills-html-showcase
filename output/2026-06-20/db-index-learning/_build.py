# -*- coding: utf-8 -*-
"""
하이브리드 빌드 4 — adaptive-html-learning-ultimate-merged(교육 방법론)
  → adaptive-html-final education_html(course-module) 스타일로 출력.
방법: 검증된 예제 04(education)를 스캐폴드로 재사용해 CSS/해시/테마바/scaffold를
유지하고, <main id="main">…</main> 내부 콘텐츠만 정규식 치환(scaffold-splice).
주제: 데이터베이스 인덱스 — 검색은 어떻게 빨라지는가 (자유 주제).
"""
import json, re, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
EX_PATH = os.path.join(ROOT, 'skills/adaptive-html-final/examples/04_education_git_rebase_workshop.html')
ICONS = {x['id']: x['svg'] for x in json.load(
    open(os.path.join(ROOT, 'skills/adaptive-html-final/assets/body-icons.json'), encoding='utf-8'))}

def ic(k):  # body-icon span
    return f'<span class="body-icon body-icon--sm">{ICONS[k]}</span>'
def h2(k, t):
    return f'<h2>{ic(k)}{t}</h2>'

# ───────────────────────── HEADER ─────────────────────────
HEADER = (
'<header class="header">'
'<div class="kicker"><span class="kicker-text">COURSE MODULE</span></div>'
'<h1>데이터베이스 인덱스, 검색은 어떻게 빨라지는가</h1>'
'<p class="sub">100만 행에서 한 줄을 찾는데 어떤 쿼리는 0.1ms, 어떤 쿼리는 1초가 걸린다. '
'그 차이를 만드는 것이 인덱스다. 이 모듈은 인덱스를 “정렬된 사본 + B-Tree 탐색”으로 이해하고, '
'언제 인덱스가 켜지고 꺼지는지, 어떤 비용이 따르는지를 <code>EXPLAIN</code>으로 직접 확인하는 '
'개념→실습 중심 과정이다.</p>'
'<div class="meta"><span>education_html</span><span>course-module.html</span>'
'<span>profile auto</span><span>adaptive-html-final v5.10.5</span><span>무 JS</span></div>'
'<div class="generated-row">'
'<p class="generated-date">생성 기준: 2026-06-20 KST · 최신 스킬 반영</p>'
'<div class="lens-strip" aria-label="적용 렌즈"><span class="lens-strip-label">LENS</span>'
'<span class="lens-chip">개념→실습형</span><span class="lens-chip">EXPLAIN 진단 중심</span>'
'<span class="lens-chip">무 JS</span><span class="lens-chip">평가 루브릭 포함</span></div>'
'</div></header>'
)

# ───────────────────────── TOC ─────────────────────────
TOC_ITEMS = [
    ('section-01', '핵심 요약'),
    ('section-02', '학습 목표'),
    ('section-03', '시작 전 — 알아야 할 4가지'),
    ('section-04', '학습 로드맵: 무엇이 언제 가능해지는가'),
    ('section-05', '1 풀스캔은 왜 느리고, 인덱스는 무엇인가'),
    ('section-06', '2 예제 — 100만 행에서 한 명 찾기'),
    ('section-07', '실습 1 — EXPLAIN으로 직접 확인'),
    ('section-08', '3 복합 인덱스와 ‘왼쪽 접두사’ 규칙'),
    ('section-09', '4 인덱스가 꺼지는 5가지 경우'),
    ('section-10', '실습 2 — 무효화 재현과 교정'),
    ('section-11', '5 퀴즈 · 정답 · 평가 루브릭'),
    ('section-12', '6 판단 흐름 — 이 쿼리가 인덱스를 탈까?'),
    ('section-13', '복습 체크리스트'),
]
TOC = (
'<nav class="toc-map" aria-label="문서 목차"><span class="label">문서 목차</span>'
'<p>개념 → 예제 → 실습 → 점검 순서로 따라가면 한 번에 끝까지 익힐 수 있도록 구성했습니다.</p>'
'<div class="toc-pills">' +
''.join(f'<a class="toc-pill" href="#{sid}"><b>{i+1}</b>{title}</a>'
        for i, (sid, title) in enumerate(TOC_ITEMS)) +
'</div></nav>'
)

S = []

# ── 01 summary-card — 핵심 요약 ──
S.append(
'<section class="summary-card" id="section-01">' +
h2('idea', '핵심 요약') +
f'<div class="label">{ic("learning")}Learning Goal</div>'
'<p><strong>인덱스는 책 맨 뒤의 “찾아보기”와 같다.</strong> 본문을 처음부터 넘기는 대신, '
'정렬된 색인에서 페이지 번호를 보고 한 번에 펼친다. 데이터베이스는 이 색인을 '
'<strong>B-Tree</strong>로 유지해, 전체를 훑는 <em>O(N)</em> 풀스캔을 '
'<em>O(log N)</em> 탐색으로 바꾼다. 이 모듈을 마치면 (1) 인덱스가 왜 빠른지 구조로 설명하고, '
'(2) 어떤 컬럼에 인덱스를 걸지 선택도로 판단하며, (3) <code>EXPLAIN</code>으로 인덱스 사용 여부를 '
'진단하고, (4) 인덱스가 무력화되는 패턴을 피할 수 있다.</p></section>'
)

# ── 02 learning-goals — 학습 목표 ──
S.append(
'<section class="learning-goals" id="section-02">' +
h2('learning', '학습 목표') +
f'<div class="label">{ic("success")}이 모듈을 마치면 할 수 있는 일</div>'
'<ul>'
'<li><strong>설명한다</strong> — 풀스캔과 인덱스 스캔의 차이를, B-Tree의 높이와 “읽는 페이지 수”로 설명한다.</li>'
'<li><strong>판단한다</strong> — 선택도(고유한 값이 얼마나 많은가)를 기준으로 어떤 컬럼에 인덱스를 걸지 정한다.</li>'
'<li><strong>진단한다</strong> — <code>EXPLAIN ANALYZE</code> 출력에서 <code>Seq Scan</code>과 '
'<code>Index Scan</code>을 구분하고 실제 실행 시간을 읽는다.</li>'
'<li><strong>피한다</strong> — 함수 적용·앞 와일드카드·형 변환·낮은 선택도 등 인덱스를 꺼뜨리는 패턴을 알아채고 교정한다.</li>'
'</ul></section>'
)

# ── 03 before_start — 시작 전 4가지 ──
S.append(
'<section id="section-03">' +
h2('note', '시작 전 — 알아야 할 4가지') +
'<p class="lede-note">아래 네 가지만 손에 쥐고 있으면 인덱스의 동작이 “마법”이 아니라 '
'당연한 결과로 보이기 시작한다.</p>'
'<ul>'
'<li><strong>행과 페이지</strong> — 테이블은 행(row)의 모음이고, 디스크에는 보통 8~16KB짜리 '
'<strong>페이지(page)</strong> 단위로 묶여 저장된다. DB가 한 번에 읽고 쓰는 최소 단위가 페이지다.</li>'
'<li><strong>풀스캔(Full / Seq Scan)</strong> — 조건에 맞는 행을 찾으려 테이블의 페이지를 '
'<em>처음부터 끝까지</em> 전부 읽는 것. 행이 많을수록 선형으로 느려진다.</li>'
'<li><strong>병목은 CPU가 아니라 ‘읽는 양’</strong> — 비교 연산 자체는 싸다. 느린 건 디스크/페이지를 '
'얼마나 많이 읽느냐다. 그래서 속도 최적화 = <strong>읽는 페이지 수를 줄이는 것</strong>이다.</li>'
'<li><strong>정렬과 이진탐색</strong> — 데이터가 정렬돼 있으면 가운데를 보고 절반씩 후보를 줄여 찾을 수 있다. '
'100만 개라도 약 20번이면 닿는다(log₂1,000,000 ≈ 20). 인덱스는 바로 이 “정렬”을 미리 만들어 둔 것이다.</li>'
'</ul></section>'
)

# ── 04 timeline (PRIMARY VT: tl-item, vt-shell) — 학습 로드맵 ──
S.append(
'<section id="section-04">' +
h2('timeline', '학습 로드맵: 무엇이 언제 가능해지는가') +
'<p class="h2-sub">시간이 아니라 “할 수 있게 되는 일”을 기준으로 진도를 잡는다.</p>'
'<div class="vt-shell"><div class="vt-shell-head"><div>'
'<div class="vt-id">VT-01 TIMELINE</div>'
'<h2>풀스캔 체감 → B-Tree 이해 → 복합 인덱스 → 진단·튜닝</h2>'
'<p>각 단계의 끝에 “직접 확인한 것”과 손에 남는 산출물을 못 박아, 개념이 실습으로 닫히게 한다.</p>'
'</div><span class="vt-fit">learning sequence</span></div>'
'<div class="vt-frame"><ol class="tl">'
'<li class="tl-item"><b>1단계 · 풀스캔을 체감한다</b><p class="vt-text">'
'100만 행 테이블을 만들고 인덱스 없이 한 행을 조회한다. <code>EXPLAIN ANALYZE</code>에서 '
'<strong>Seq Scan</strong>과 수십~수백 ms의 실행 시간을 눈으로 본다. “느림”을 숫자로 확인한 노트가 남는다.</p></li>'
'<li class="tl-item"><b>2단계 · 인덱스의 구조를 이해한다</b><p class="vt-text">'
'인덱스를 <strong>정렬된 사본 + B-Tree</strong>로 그릴 수 있게 된다. 같은 쿼리가 '
'<strong>Index Scan</strong>으로 바뀌고 실행 시간이 1000배 가까이 줄어드는 것을 비교한 표가 남는다.</p></li>'
'<li class="tl-item"><b>3단계 · 복합 인덱스를 설계한다</b><p class="vt-text">'
'두 컬럼을 묶은 인덱스에서 <strong>왼쪽 접두사 규칙</strong>과 컬럼 순서(등호→범위)를 적용한다. '
'어떤 쿼리가 인덱스를 타고 어떤 쿼리가 못 타는지 구분한 목록이 남는다.</p></li>'
'<li class="tl-item"><b>4단계 · 진단하고 판단한다</b><p class="vt-text">'
'인덱스가 꺼지는 패턴을 재현·교정하고, 흐름도로 “이 쿼리가 인덱스를 탈까”를 스스로 판단한다. '
'평가 루브릭과 복습 체크리스트로 학습을 닫는다.</p></li>'
'</ol></div></div></section>'
)

# ── 05 concept 1 — 풀스캔 vs 인덱스 ──
S.append(
'<section id="section-05">' +
h2('database', '<span class="no" aria-hidden="true">1</span>풀스캔은 왜 느리고, 인덱스는 무엇인가') +
'<p class="h2-sub">인덱스 = 특정 컬럼만 정렬해 둔 별도의 자료구조(보통 B-Tree)와, 원본 행으로 가는 포인터.</p>'
'<p>이름 100만 개가 <em>아무 순서로</em> 적힌 종이 뭉치에서 “김영희”를 찾는다고 하자. 정렬이 안 돼 있으니 '
'운이 나쁘면 끝장까지 다 넘겨야 한다(풀스캔). 반대로 가나다순으로 정렬돼 있으면 가운데를 펼쳐 '
'앞/뒤를 가르며 절반씩 줄인다(이진탐색). <strong>인덱스는 이 “정렬된 별도 목록”을 미리 만들어 '
'유지하는 것</strong>이다.</p>'
'<p class="core-insight">핵심: 풀스캔의 비용은 <strong>행 수에 비례</strong>(O(N))하지만, B-Tree 탐색은 '
'<strong>트리 높이에 비례</strong>(O(log N))한다. 100만 행이라도 B-Tree 높이는 보통 3~4단계뿐이라, '
'시작 위치를 찾는 데 페이지 몇 개만 읽으면 된다.</p>'
'<div class="box"><p><strong>B-Tree를 그림으로</strong> — 맨 위 <em>루트</em> 노드가 넓은 범위를, '
'그 아래 <em>브랜치</em>가 더 좁은 범위를 가리키고, 맨 아래 <em>리프</em>에 실제 정렬된 키와 '
'행 위치가 있다. 리프끼리는 정렬 순서대로 옆으로 연결돼 있어, 한 번 시작점을 찾으면 '
'범위 검색(<code>BETWEEN</code>, <code>ORDER BY</code>)도 리프 체인을 따라 이어서 읽을 수 있다.</p></div>'
'</section>'
)

# ── 06 example — 100만 행에서 한 명 찾기 ──
S.append(
'<section id="section-06">' +
h2('case', '<span class="no" aria-hidden="true">2</span>예제 — 100만 행에서 한 명 찾기') +
'<p class="h2-sub">같은 쿼리를 인덱스 전/후로 실행해, 읽는 양과 시간이 어떻게 달라지는지 본다.</p>'
'<pre class="code"><code>-- users 테이블에 100만 행이 있다고 하자.\n'
'SELECT * FROM users WHERE email = \'kim@example.com\';\n\n'
'-- (1) 인덱스 없음 → 순차 스캔(Seq Scan)\n'
'--     일치하는 1행을 찾으려 최대 1,000,000행을 한 줄씩 검사한다.\n\n'
'-- (2) 인덱스 생성\n'
'CREATE INDEX idx_users_email ON users(email);\n\n'
'-- (3) 같은 쿼리 → 인덱스 스캔(Index Scan)\n'
'--     B-Tree 높이가 3~4단계라, 약 20번 비교로 시작 위치에 도달한다.</code></pre>'
'<div class="tbl table-scroll"><table><caption>인덱스 전/후 — 같은 쿼리, 다른 비용</caption>'
'<thead><tr><th>방식</th><th>읽는 행(논리)</th><th>대략 비교 횟수</th><th>EXPLAIN 노드</th></tr></thead>'
'<tbody>'
'<tr><td>인덱스 없음</td><td>최대 1,000,000</td><td>~1,000,000</td><td><code>Seq Scan</code></td></tr>'
'<tr><td>인덱스 있음</td><td>수십 페이지</td><td>~20 (log₂N)</td><td><code>Index Scan</code></td></tr>'
'</tbody></table></div>'
'<div class="box"><p><strong>수치는 환경마다 다르지만 차원이 다르다.</strong> 100만 행 기준 풀스캔이 '
'수십~수백 ms라면 인덱스 조회는 흔히 1ms 미만이다. 핵심은 “몇 ms냐”가 아니라 '
'<strong>읽는 양이 선형(N)에서 로그(log N)로 줄어든다</strong>는 점이다 — 데이터가 커질수록 격차는 벌어진다.</p></div>'
'</section>'
)

# ── 07 practice-card — 실습 1 ──
S.append(
'<section class="practice-card" id="section-07">' +
h2('experiment', '실습 1 — EXPLAIN으로 직접 확인') +
f'<div class="label">{ic("search")}측정 먼저, 최적화는 그다음</div>'
'<h3>풀스캔과 인덱스 스캔을 같은 쿼리로 비교하기</h3>'
'<p>추측하지 말고 <code>EXPLAIN ANALYZE</code>로 실제 계획과 시간을 확인한다. (예시는 PostgreSQL 기준)</p>'
'<pre class="code"><code>-- 1) 100만 행 테스트 테이블\n'
'CREATE TABLE users (id int, email text, name text);\n'
'INSERT INTO users\n'
'  SELECT g, \'user\' || g || \'@example.com\', \'name\' || g\n'
'  FROM generate_series(1, 1000000) AS g;\n\n'
'-- 2) 인덱스 없이 조회 → Seq Scan 확인\n'
'EXPLAIN ANALYZE SELECT * FROM users WHERE email = \'user777777@example.com\';\n\n'
'-- 3) 인덱스 생성 후 다시 조회 → Index Scan + 실행 시간 비교\n'
'CREATE INDEX idx_users_email ON users(email);\n'
'EXPLAIN ANALYZE SELECT * FROM users WHERE email = \'user777777@example.com\';</code></pre>'
'<ol>'
'<li>2)의 출력에서 <code>Seq Scan on users</code>와 <code>Rows Removed by Filter</code> 값을 적는다.</li>'
'<li>3)의 출력에서 <code>Index Scan using idx_users_email</code>로 바뀌었는지 확인한다.</li>'
'<li>두 경우의 <code>Execution Time</code>을 나란히 적고, 몇 배 차이인지 계산한다.</li>'
'</ol></section>'
)

# ── 08 concept 2 — 복합 인덱스 ──
S.append(
'<section id="section-08">' +
h2('connection', '<span class="no" aria-hidden="true">3</span>복합 인덱스와 ‘왼쪽 접두사’ 규칙') +
'<p class="h2-sub">두 컬럼을 묶은 인덱스는 “먼저 A로 정렬, 같으면 B로 정렬”한 전화번호부와 같다.</p>'
'<pre class="code"><code>CREATE INDEX idx_orders_user_time ON orders(user_id, created_at);\n\n'
'-- 인덱스를 타는 쿼리 (선두 컬럼 user_id를 쓴다)\n'
'WHERE user_id = 42\n'
'WHERE user_id = 42 AND created_at &gt;= \'2026-06-01\'\n\n'
'-- 인덱스를 못 타는 쿼리 (선두 컬럼 user_id가 조건에 없음)\n'
'WHERE created_at &gt;= \'2026-06-01\'</code></pre>'
'<p class="core-insight">왼쪽 접두사 규칙: 복합 인덱스 <code>(A, B)</code>는 <code>A</code> 또는 '
'<code>(A, B)</code> 조건에는 쓰이지만, <code>B</code> 단독 조건에는 쓰이지 않는다. '
'성으로 먼저 정렬한 전화번호부에서 이름만으로는 빨리 못 찾는 것과 같다.</p>'
'<div class="box"><p><strong>컬럼 순서 정하기</strong> — 등호(<code>=</code>)로 거르는 컬럼을 앞에, '
'범위(<code>&gt;</code>, <code>&lt;</code>, <code>BETWEEN</code>)로 거르는 컬럼을 뒤에 둔다. '
'범위 조건이 먼저 오면 그 뒤 컬럼의 정렬이 흩어져 인덱스를 끝까지 활용하지 못한다. '
'또 조회에 필요한 컬럼을 인덱스에 모두 포함하면(<em>커버링 인덱스</em>) 원본 테이블을 다시 읽지 않아 더 빠르다.</p></div>'
'</section>'
)

# ── 09 warning — 인덱스가 꺼지는 5가지 ──
S.append(
'<section id="section-09">' +
h2('warning', '<span class="no" aria-hidden="true">4</span>인덱스가 꺼지는 5가지 경우') +
'<p class="h2-sub">인덱스를 “만들어 두기만” 하면 끝이 아니다 — 쿼리가 정렬 순서를 깨면 옵티마이저는 풀스캔으로 돌아간다.</p>'
'<div class="tbl table-scroll"><table><caption>인덱스를 무력화하는 안티패턴과 교정</caption>'
'<thead><tr><th>안티패턴</th><th>왜 꺼지나</th><th>교정</th></tr></thead><tbody>'
'<tr><td>컬럼에 함수·연산<br><code>WHERE YEAR(created_at)=2026</code></td>'
'<td>가공된 값은 인덱스의 정렬과 다르다</td>'
'<td><code>created_at &gt;= \'2026-01-01\' AND created_at &lt; \'2027-01-01\'</code></td></tr>'
'<tr><td>앞부분 와일드카드<br><code>LIKE \'%kim\'</code></td>'
'<td>시작 글자를 모르면 정렬을 활용 못 한다</td>'
'<td>접미사 검색이 필요하면 역순 인덱스/전문검색 사용, 가능하면 <code>LIKE \'kim%\'</code></td></tr>'
'<tr><td>암묵적 형 변환<br>문자 컬럼에 숫자 비교</td>'
'<td>DB가 컬럼 전체를 캐스팅 → 함수 적용과 같음</td>'
'<td>비교 값의 타입을 컬럼 타입과 맞춘다</td></tr>'
'<tr><td>낮은 선택도<br>(예: 성별·상태 플래그)</td>'
'<td>결과가 전체의 큰 비율이면 인덱스가 더 느리다</td>'
'<td>선택도 높은 컬럼과 묶거나, 부분 인덱스를 고려</td></tr>'
'<tr><td>과도한 인덱스</td>'
'<td>쓰기(INSERT/UPDATE)마다 인덱스도 갱신 → 쓰기 지연·디스크 증가</td>'
'<td>실제 쿼리가 쓰는 인덱스만 유지하고 주기적으로 정리</td></tr>'
'</tbody></table></div>'
'<div class="box"><p><strong>한 줄 요약</strong> — 인덱스는 <em>읽기</em>를 빠르게 하는 대신 '
'<em>쓰기</em>와 <em>저장공간</em>에 비용을 청구한다. “모든 컬럼에 인덱스”가 아니라 '
'“자주·선택적으로 거르는 컬럼에만”이 원칙이다.</p></div>'
'</section>'
)

# ── 10 practice-card — 실습 2 ──
S.append(
'<section class="practice-card" id="section-10">' +
h2('experiment', '실습 2 — 무효화 재현과 교정') +
f'<div class="label">{ic("audit")}꺼지는 걸 직접 보고, 켜지게 고친다</div>'
'<h3>“왜 인덱스를 안 타지?”를 스스로 진단하기</h3>'
'<pre class="code"><code>-- A) 함수 적용으로 인덱스가 꺼지는 것 재현\n'
'CREATE INDEX idx_users_created ON users(created_at);\n'
'EXPLAIN ANALYZE SELECT * FROM users WHERE date(created_at) = \'2026-06-20\';  -- Seq Scan?\n\n'
'-- B) 범위 조건으로 바꿔 Index Scan 되는지 확인\n'
'EXPLAIN ANALYZE SELECT * FROM users\n'
'  WHERE created_at &gt;= \'2026-06-20\' AND created_at &lt; \'2026-06-21\';\n\n'
'-- C) 복합 인덱스의 왼쪽 접두사 확인\n'
'CREATE INDEX idx_ab ON orders(user_id, created_at);\n'
'EXPLAIN ANALYZE SELECT * FROM orders WHERE created_at &gt;= \'2026-06-01\';  -- 선두 컬럼 없음 → 못 탐</code></pre>'
'<ol>'
'<li>A에서 <code>Seq Scan</code>이 나오는 것을 확인하고, 왜 꺼졌는지 한 줄로 적는다.</li>'
'<li>B로 바꾼 뒤 <code>Index Scan</code>으로 바뀌고 시간이 줄었는지 비교한다.</li>'
'<li>C에서 복합 인덱스가 <code>created_at</code> 단독 조건에는 쓰이지 않음을 확인한다.</li>'
'</ol></section>'
)

# ── 11 quiz-box — 퀴즈·정답·루브릭 (quiz + answer_key) ──
S.append(
'<section class="quiz-box" id="section-11">' +
h2('question', '<span class="no is-key" aria-hidden="true">5</span>퀴즈 · 정답 · 평가 루브릭') +
'<p class="h2-sub">명령 암기가 아니라 “왜 그렇게 되는가”의 판단 근거를 확인한다.</p>'
'<ol>'
'<li>인덱스가 풀스캔보다 빠른 이유를 B-Tree의 높이로 설명하면?</li>'
'<li><code>EXPLAIN</code>에서 <code>Seq Scan</code>과 <code>Index Scan</code>을 어떻게 구분하나?</li>'
'<li>복합 인덱스 <code>(user_id, created_at)</code>가 <code>WHERE created_at = ?</code>만으로는 '
'쓰이지 않는 이유는?</li>'
'<li><code>WHERE YEAR(created_at) = 2026</code>이 인덱스를 못 타는 이유와 교정 방법은?</li>'
'<li>성별처럼 값 종류가 적은 컬럼에 인덱스를 걸어도 풀스캔이 선택될 수 있는 이유는?</li>'
'<li>인덱스를 많이 만들수록 무조건 좋지 않은 이유는?</li>'
'</ol>'
'<p><strong>정답 요약:</strong> ① B-Tree 높이는 행이 100만이어도 3~4단계뿐이라 시작 위치를 찾는 비교가 '
'log N(≈20)에 그친다 — 풀스캔의 N에 비해 차원이 다르다. ② 계획에 <code>Seq Scan</code>이 보이면 전부 읽는 것, '
'<code>Index Scan</code>(또는 <code>Index Only Scan</code>)이 보이면 인덱스로 일부만 읽는 것이다. '
'③ 인덱스는 선두 컬럼부터 정렬하므로 <code>user_id</code>가 조건에 없으면 정렬을 활용할 수 없다(왼쪽 접두사 규칙). '
'④ 컬럼을 함수로 가공하면 정렬 순서가 깨진다 → 조건을 값 쪽 범위로 바꾼다'
'(<code>created_at &gt;= \'2026-01-01\' AND &lt; \'2027-01-01\'</code>). '
'⑤ 선택도가 낮으면(결과가 전체의 큰 비율) 인덱스로 일부만 읽고 원본을 랜덤 접근하는 비용이 '
'풀스캔보다 커서 옵티마이저가 풀스캔을 택한다. ⑥ 인덱스는 읽기를 빠르게 하지만 쓰기마다 갱신되고 '
'저장공간을 쓰므로, 안 쓰는 인덱스는 순수 비용이다.</p>'
'<details><summary>④·⑤가 헷갈린다면 — 한 번 더 풀어보기</summary>'
'<p>④는 “쿼리가 인덱스의 정렬을 깨뜨려서” 못 타는 경우(쿼리를 고치면 해결)이고, '
'⑤는 “쿼리는 멀쩡한데 인덱스를 쓰는 게 오히려 손해여서” 옵티마이저가 스스로 풀스캔을 고른 경우다. '
'전자는 내 잘못, 후자는 합리적 선택 — 진단 방향이 다르다.</p></details>'
'<div class="tbl table-scroll"><table><caption>평가 루브릭 (28/35 이상 통과)</caption>'
'<thead><tr><th>축</th><th>기준</th><th>우수 답안의 모습</th></tr></thead><tbody>'
'<tr><td>동작 모델</td><td>인덱스를 정렬된 사본 + B-Tree로 설명한다.</td><td>O(N) vs O(log N)을 높이로 그려 보인다.</td></tr>'
'<tr><td>진단 능력</td><td>EXPLAIN에서 스캔 종류와 시간을 읽는다.</td><td>Rows Removed·Execution Time까지 근거로 든다.</td></tr>'
'<tr><td>설계 판단</td><td>선택도·컬럼 순서로 인덱스를 정한다.</td><td>등호→범위 순서와 커버링까지 고려한다.</td></tr>'
'<tr><td>비용 인식</td><td>쓰기·저장 비용을 함께 말한다.</td><td>“안 쓰는 인덱스 = 비용”을 사례로 든다.</td></tr>'
'</tbody></table></div></section>'
)

# ── 12 판단 흐름 intro + wg-13 중첩 (예제처럼 wg-13을 섹션 안에 넣어 직접-자식 h2 게이트 면제) ──
S.append(
'<section id="section-12">' +
h2('decision', '<span class="no" aria-hidden="true">6</span>판단 흐름 — 이 쿼리가 인덱스를 탈까?') +
'<p class="h2-sub">쿼리가 느릴 때 위에서부터 짚어 내려가면 “왜 인덱스를 안 타는지”가 대개 한 군데에서 잡힌다.</p>'
'<p class="lede-note">아래 흐름도의 노드를 누르면 단계별 판단 근거가 그 자리에서 펼쳐진다.</p>'
# ── wg-13 (WG MARKER): 인덱스 사용 판단 흐름 — 위 섹션 안에 중첩 ──
'<section class="wg-13" aria-labelledby="wg-13-title">'
'<div class="wg-13-fc">'
'<h3 id="wg-13-title" class="wg-13-h">이 쿼리가 인덱스를 탈까? '
'<span class="wg-13-sub">노드를 누르면 판단 근거가 펼쳐집니다</span></h3>'
'<div class="wg-13-flow">'
'<a href="#wg-13-s1" class="wg-13-node wg-13-node--start">'
'<span class="wg-13-step">시작</span>WHERE·JOIN·ORDER BY에 인덱스 컬럼이 쓰였다</a>'
'<span class="wg-13-arrow" aria-hidden="true">&darr;</span>'
'<a href="#wg-13-s2" class="wg-13-node">'
'<span class="wg-13-step">확인</span>그 컬럼을 함수·연산으로 가공했나?</a>'
'<span class="wg-13-arrow" aria-hidden="true">&darr;</span>'
'<a href="#wg-13-s3" class="wg-13-node wg-13-node--decide">'
'<span class="wg-13-step">판단</span>가공이 없고, 걸러낼 결과가 전체의 소수인가?</a>'
'<div class="wg-13-branch"><div class="wg-13-paths">'
'<div class="wg-13-path wg-13-path--fail">'
'<span class="wg-13-edge" aria-hidden="true">아니오 · 풀스캔</span>'
'<a href="#wg-13-s4" class="wg-13-node wg-13-node--fail">'
'<span class="wg-13-step">Seq Scan</span>옵티마이저가 전부 읽기를 택한다</a></div>'
'<div class="wg-13-path wg-13-path--ok">'
'<span class="wg-13-edge" aria-hidden="true">예 · 인덱스</span>'
'<a href="#wg-13-s5" class="wg-13-node wg-13-node--end">'
'<span class="wg-13-step">Index Scan</span>B-Tree로 소수 페이지만 읽는다</a></div>'
'</div></div>'
'</div>'
'<div class="wg-13-detail">'
'<h4 class="wg-13-dh">단계별 판단 근거 <span class="wg-13-dnote">위 노드와 같은 색으로 묶여 있습니다</span></h4>'
'<details id="wg-13-s1" class="wg-13-acc">'
'<summary><span class="wg-13-tag">시작</span>WHERE·JOIN·ORDER BY에 인덱스 컬럼이 쓰였다</summary>'
'<div class="wg-13-body"><p>인덱스는 쿼리가 그 컬럼을 <strong>조건·정렬·조인</strong>에 쓸 때만 후보가 된다. '
'<code>SELECT</code> 목록에만 등장하는 컬럼은 인덱스 선택과 무관하다. 그러니 먼저 '
'<code>WHERE</code>·<code>JOIN ... ON</code>·<code>ORDER BY</code>를 보고, 자주 거르는 컬럼에 인덱스가 있는지 확인한다.</p></div></details>'
'<details id="wg-13-s2" class="wg-13-acc">'
'<summary><span class="wg-13-tag">확인</span>그 컬럼을 함수·연산으로 가공했나?</summary>'
'<div class="wg-13-body"><p>컬럼을 가공하면 인덱스의 정렬 순서가 깨져 못 쓴다. '
'<code>YEAR(created_at)=2026</code>, 앞 와일드카드 <code>LIKE \'%kim\'</code>, 암묵적 형 변환이 대표적이다. '
'가공을 조건이 아니라 <strong>값 쪽으로</strong> 옮기면 인덱스가 다시 살아난다.</p>'
'<code class="wg-13-code">-- 꺼짐:  WHERE YEAR(created_at) = 2026\n'
'-- 켜짐:  WHERE created_at &gt;= \'2026-01-01\' AND created_at &lt; \'2027-01-01\'</code></div></details>'
'<details id="wg-13-s3" class="wg-13-acc">'
'<summary><span class="wg-13-tag">판단</span>가공이 없고, 결과가 전체의 소수인가?</summary>'
'<div class="wg-13-body"><p>가공이 없어도 옵티마이저는 “인덱스로 일부만 읽고 원본을 랜덤 접근”하는 비용과 '
'“그냥 순차로 다 읽는” 비용을 비교한다. 조건이 전체의 큰 비율(예: 30% 이상)을 통과시키면 '
'인덱스가 오히려 느려 풀스캔을 택한다. 이 “얼마나 잘 거르는가”가 <strong>선택도(selectivity)</strong>다.</p></div></details>'
'<details id="wg-13-s4" class="wg-13-acc wg-13-acc--fail">'
'<summary><span class="wg-13-tag wg-13-tag--fail">Seq Scan</span>아니오 · 풀스캔이 선택됐다면</summary>'
'<div class="wg-13-body"><p>계획에 <code>Seq Scan</code>이 보이면 ① 조건의 가공을 풀거나 ② 선택도 높은 컬럼으로 '
'복합 인덱스를 만들거나 ③ 정말로 대부분 행이 필요한 쿼리인지 다시 본다. 추측 말고 '
'<code>EXPLAIN ANALYZE</code>로 실제 읽은 행과 시간을 확인한다.</p>'
'<code class="wg-13-code">EXPLAIN ANALYZE SELECT ...;   -- Seq Scan / Rows Removed by Filter 확인</code></div></details>'
'<details id="wg-13-s5" class="wg-13-acc wg-13-acc--ok">'
'<summary><span class="wg-13-tag wg-13-tag--ok">Index Scan</span>예 · 인덱스를 탄다면</summary>'
'<div class="wg-13-body"><p><code>Index Scan</code>이면 B-Tree 루트→리프 몇 단계로 시작 위치를 찾고, 필요한 범위만 '
'리프 체인을 따라 읽는다. 100만 행이라도 읽는 페이지는 수십 개 수준이다. 다만 결과 행이 많으면 '
'원본 테이블 랜덤 접근이 비용이 되며, 조회 컬럼을 인덱스에 모두 담은 '
'<strong>커버링 인덱스</strong>(<code>Index Only Scan</code>)로 이를 피할 수 있다.</p></div></details>'
'</div></div></section>'  # wg-13 닫음
'</section>'              # section-12 닫음 (wg-13을 감쌌으므로)
)

# ── 13 review_checklist — 복습 체크리스트 ──
S.append(
'<section id="section-13">' +
h2('check', '복습 체크리스트') +
'<p class="lede-note">아래를 막힘없이 “예”라고 답할 수 있으면 이 모듈의 목표를 채운 것이다.</p>'
'<ul>'
'<li><strong>설명</strong> — 인덱스가 왜 O(log N)인지 B-Tree의 높이로 설명할 수 있다.</li>'
'<li><strong>진단</strong> — <code>EXPLAIN</code>에서 <code>Seq Scan</code>과 <code>Index Scan</code>을 구분하고 실행 시간을 읽을 수 있다.</li>'
'<li><strong>설계</strong> — 복합 인덱스의 컬럼 순서를 “등호 먼저, 범위 나중”으로 정할 수 있다.</li>'
'<li><strong>규칙</strong> — 왼쪽 접두사 규칙을 전화번호부 비유로 예를 들어 설명할 수 있다.</li>'
'<li><strong>회피</strong> — 인덱스가 꺼지는 5가지 패턴을 떠올리고 각각 교정안을 말할 수 있다.</li>'
'<li><strong>비용</strong> — 인덱스를 무한정 늘리면 안 되는 이유를 쓰기·저장 비용으로 설명할 수 있다.</li>'
'</ul></section>'
)

# ── try CTA — 바로 실행할 일 ──
S.append(
'<section class="try"><div class="label">NEXT ACTION</div>' +
h2('success', '바로 실행할 일') +
'<ol>'
'<li>실제 프로젝트의 느린 쿼리 하나를 골라 <code>EXPLAIN ANALYZE</code>로 계획과 시간을 기록한다.</li>'
'<li><code>Seq Scan</code>이라면, 자주 거르는 컬럼을 찾아 인덱스를 만들고 전/후를 비교한다.</li>'
'<li><code>WHERE</code>에 함수가 씌워진 조건이 있으면 값 쪽 범위 조건으로 바꿔 본다.</li>'
'<li>두 컬럼으로 거르는 쿼리에 복합 인덱스를 만들고, 컬럼 순서를 바꿔 가며 계획을 비교한다.</li>'
'<li>현재 테이블의 인덱스 목록을 뽑아, 실제로 쓰이지 않는 인덱스가 있는지 점검하고 정리 후보를 메모한다.</li>'
'</ol></section>'
)

MAIN_INNER = HEADER + TOC + ''.join(S)

ex = open(EX_PATH, encoding='utf-8').read()
new = re.sub(r'(<main\s+id="main"[^>]*>)[\s\S]*(</main>)',
             lambda m: m.group(1) + MAIN_INNER + m.group(2), ex, count=1)

# 본문에서 보이는 글자 수(대략) 계산 — 산출물 점검용
visible = re.sub(r'<[^>]+>', '', MAIN_INNER)
visible = re.sub(r'\s+', ' ', visible).strip()

out_path = os.path.join(HERE, 'index.html')
open(out_path, 'w', encoding='utf-8').write(new)
print('WROTE', out_path)
print('len(html)', len(new), 'sections', len(S), 'visible_chars', len(visible))
print('main spliced?', '<main id="main" class="page-wide layout-education">' in new)
print('has tl-item:', new.count('tl-item'), ' wg-13 nodes:', new.count('wg-13-node'))
