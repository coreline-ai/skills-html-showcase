#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
SKILL = REPO / 'skills/adaptive-html-final'
ASSETS = SKILL / 'assets'
OUT = ROOT / 'pages/04_education_postgres_query_plan_workshop.html'

MODE_MATERIALS = [
    SKILL / 'SKILL.md',
    SKILL / 'recipes/education.prompt.md',
    ASSETS / 'layouts/course-module.html',
    SKILL / 'references/layout-system.md',
    SKILL / 'references/writing-system.md',
    SKILL / 'references/body-icon-system.md',
    SKILL / 'references/visual-html-system.md',
    SKILL / 'references/widget-system.md',
    ASSETS / 'visual-html-templates/04-timeline.html',
    ASSETS / 'visual-html-templates/05-checklist-flow.html',
    ASSETS / 'visual-html-templates/15-concept-explainer.html',
    ASSETS / 'visual-html-templates/21-soft-workflow-map.html',
    ASSETS / 'widget-templates/13-annotated-flowchart.html',
    ASSETS / 'widget-templates/14-feature-explainer.html',
    ASSETS / 'widget-templates/15-concept-explainer.html',
]

# Deterministic evidence: read the exact mode-specific materials. The previous
# HTML body is intentionally never opened by this renderer.
MATERIAL_HASH = {str(p.relative_to(REPO)): hashlib.sha256(p.read_bytes()).hexdigest() for p in MODE_MATERIALS}
for p in MODE_MATERIALS:
    p.read_text(encoding='utf-8')

CORE = ['theme.css', 'components.css', 'visual-components.css', 'layouts.css', 'print.css']
def read_asset(name: str) -> str:
    return (ASSETS / name).read_text(encoding='utf-8')

core_hash = hashlib.sha256('\n'.join(read_asset(n) for n in CORE).encode('utf-8')).hexdigest()
css_slots = {
    'THEME_CSS': f'/* adaptive-html-final-core-css-sha256: {core_hash} */\n' + read_asset('theme.css'),
    'COMPONENTS_CSS': read_asset('components.css'),
    'VISUAL_COMPONENTS_CSS': read_asset('visual-components.css'),
    'WIDGETS_CSS': read_asset('widgets.css'),
    'VISUAL_HTML_CSS': read_asset('visual-html.css'),
    'BODY_ICONS_CSS': read_asset('body-icons.css'),
    'EDITORIAL_PATTERNS_CSS': read_asset('editorial-patterns.css'),
    'SHAPE_VISUALS_CSS': '',
    'WORKFLOW_VISUALS_CSS': '',
    'LAYOUTS_CSS': read_asset('layouts.css'),
    'PRINT_CSS': read_asset('print.css'),
    'THEME_DARK_CSS': read_asset('theme-dark.css'),
}

icons = {item['id']: item['svg'] for item in json.loads((ASSETS / 'body-icons.json').read_text(encoding='utf-8'))}
def icon(name: str) -> str:
    return f'<span class="body-icon body-icon--sm">{icons[name]}</span>'

def h2(num: int, title: str, icon_id: str = 'learning') -> str:
    return f'<h2>{icon(icon_id)}<span class="num">{num}</span>{title}</h2>'

def code(text: str) -> str:
    return html.escape(text.strip())

generated = '''<div class="generated-row"><p class="generated-date">Generated · 2026-06-07 KST</p><div class="lens-strip" aria-label="적용 렌즈"><span class="lens-strip-label">LENS</span><span class="lens-chip">mode 04</span><span class="lens-chip">education</span><span class="lens-chip">course-module</span><span class="lens-chip">Postgres plan</span><span class="lens-chip">no reuse</span></div></div>'''

goals = f'''
{h2(1, '학습 목표', 'learning')}
<p class="h2-sub">이 워크숍은 PostgreSQL 실행 계획을 “빠르다/느리다” 감상으로 보지 않고, 근거 있는 다음 실험으로 바꾸는 읽기 훈련이다.</p>
<div class="grid-2">
  <article class="summary-card"><h3>끝나면 할 수 있는 일</h3><ul><li><code>Seq Scan</code>, <code>Index Scan</code>, <code>Nested Loop</code>, <code>Sort</code>를 보고 병목 후보를 말한다.</li><li><code>cost</code>, <code>rows</code>, <code>actual time</code>, <code>loops</code>를 각각 다른 신호로 구분한다.</li><li>인덱스 추가, 조건식 변경, 통계 갱신 중 무엇을 먼저 실험할지 정한다.</li></ul></article>
  <article class="summary-card"><h3>학습하지 않는 것</h3><p>이 모듈은 튜닝 만능 공식을 제공하지 않는다. 실제 성능은 데이터 분포, 캐시 상태, 동시성, PostgreSQL 버전에 따라 달라지므로 실행 계획을 근거로 작은 실험을 설계하는 능력에 집중한다.</p></article>
</div>
<section class="vt-shell" aria-label="쿼리 플랜 학습 진행 타임라인"><div class="vt-frame"><ol class="tl"><li class="tl-item"><b>읽기</b><p class="vt-text">가장 안쪽 노드부터 실행 단위를 파악한다.</p></li><li class="tl-item"><b>비교</b><p class="vt-text">예상 rows와 actual rows 차이를 찾는다.</p></li><li class="tl-item"><b>가설</b><p class="vt-text">왜 이 Scan/Join/Sort가 선택됐는지 비용 신호로 설명한다.</p></li><li class="tl-item"><b>실험</b><p class="vt-text">한 번에 하나만 바꾸고 같은 조건에서 다시 측정한다.</p></li></ol></div></section>
'''

before = f'''
{h2(2, '시작 전 준비', 'check')}
<p class="h2-sub">실습은 SQL 한 줄보다 환경 통제가 중요하다. 같은 쿼리라도 데이터 수, 통계, 캐시, 인덱스 상태가 바뀌면 플랜이 달라진다.</p>
<div class="grid-3"><article class="summary-card"><h3>사전 지식</h3><p><code>SELECT</code>, <code>WHERE</code>, <code>ORDER BY</code>, <code>LIMIT</code> 의미를 알고 있어야 한다. Join 문법을 몰라도 이번 흐름은 따라올 수 있다.</p></article><article class="summary-card"><h3>환경</h3><p>PostgreSQL 13+ 기준으로 설명한다. 버전별 planner 개선이 있으므로 실제 업무 DB에서는 버전을 먼저 기록한다.</p></article><article class="summary-card"><h3>데이터 조건</h3><p>테이블에 충분한 행이 있어야 차이가 보인다. 샘플 100행에서는 인덱스 효과를 판단하지 않는다.</p></article></div>
<section class="vt-shell" aria-label="실습 전 체크 플로우"><div class="vt-frame"><div class="cf"><div class="cf-item"><span class="cf-check">✓</span><div><b>통계 최신화</b><p class="vt-text"><code>ANALYZE</code> 이후 플랜을 읽어야 rows 추정이 의미 있다.</p></div><span class="cf-state">PASS</span></div><div class="cf-item"><span class="cf-check">✓</span><div><b>쿼리 원문 보존</b><p class="vt-text">튜닝 전 SQL과 실행 계획을 함께 저장한다.</p></div><span class="cf-state">PASS</span></div><div class="cf-item"><span class="cf-check">✓</span><div><b>측정 조건 고정</b><p class="vt-text">같은 DB, 같은 파라미터, 같은 데이터 시점에서 비교한다.</p></div><span class="cf-state">READY</span></div></div></div></section>
'''

lesson = f'''
{h2(3, '개념 강의: 플랜을 읽는 4단계', 'timeline')}
<p class="h2-sub">PostgreSQL 플랜은 위에서 아래로 읽는 문서가 아니라, 아래 노드가 만들어낸 행이 위 노드로 전달되는 실행 흐름이다.</p>
<section class="vt-shell" aria-label="쿼리 플랜 핵심 개념"><div class="vt-frame"><div class="concept-ring"><div class="vt-section-title"><span class="vt-num">?</span><h3 style="margin:0">Cost, Rows, Actual의 관계</h3></div><p class="vt-text"><code>cost</code>는 planner의 예상 비용, <code>rows</code>는 예상 행 수, <code>actual</code>은 실제 실행 결과다. 튜닝은 세 값의 차이를 보고 다음 확인 지점을 찾는 과정이다.</p><div class="concept-steps"><div class="concept-step"><b>1</b>노드</div><div class="concept-step"><b>2</b>예상</div><div class="concept-step"><b>3</b>실제</div><div class="concept-step"><b>4</b>가설</div></div></div></div></section>
<section class="wg-15" aria-labelledby="m04-wg15-title"><p class="wg-15-kicker">개념 교보재 · EXPLAIN</p><h2 id="m04-wg15-title" class="wg-15-h">EXPLAIN과 EXPLAIN ANALYZE를 구분하기</h2><p class="wg-15-lead"><code>EXPLAIN</code>은 예상 계획만 보여주고, <code>EXPLAIN ANALYZE</code>는 실제 실행한 뒤 시간과 행 수를 붙인다. 운영 DB에서는 실제 실행이 부담이 될 수 있으므로 읽기 쿼리인지, 락/부하 위험이 없는지 먼저 확인한다.</p><h3 class="wg-15-h3">방식 비교</h3><div class="table-scroll"><table class="wg-15-table"><caption class="wg-15-cap">플랜 확인 방식 비교</caption><thead><tr><th scope="col">기준</th><th scope="col">EXPLAIN</th><th scope="col">EXPLAIN ANALYZE</th></tr></thead><tbody><tr><th scope="row">실제 실행</th><td>하지 않음</td><td><span class="wg-15-good">실행함</span></td></tr><tr><th scope="row">볼 수 있는 값</th><td>cost, rows 예상</td><td>actual time, actual rows, loops</td></tr><tr><th scope="row">주의점</th><td>실제 병목을 단정할 수 없음</td><td><span class="wg-15-bad">쓰기 쿼리·부하 위험 확인 필요</span></td></tr></tbody></table></div><h3 class="wg-15-h3">읽는 순서</h3><div class="wg-15-steps"><input type="radio" name="m04-wg15-step" id="m04-wg15-s1" class="wg-15-step-in" checked><input type="radio" name="m04-wg15-step" id="m04-wg15-s2" class="wg-15-step-in"><input type="radio" name="m04-wg15-step" id="m04-wg15-s3" class="wg-15-step-in"><div class="wg-15-stepnav"><label class="wg-15-stepbtn" for="m04-wg15-s1"><span class="wg-15-stepnum">1</span> 아래 노드</label><label class="wg-15-stepbtn" for="m04-wg15-s2"><span class="wg-15-stepnum">2</span> 행 차이</label><label class="wg-15-stepbtn" for="m04-wg15-s3"><span class="wg-15-stepnum">3</span> 다음 실험</label></div><div class="wg-15-stage"><div class="wg-15-ring" aria-hidden="true"><span class="wg-15-node wg-15-na">S</span><span class="wg-15-node wg-15-nb">J</span><span class="wg-15-node wg-15-nc">T</span><span class="wg-15-node wg-15-nd wg-15-new">?</span><span class="wg-15-key wg-15-k1">rows</span><span class="wg-15-key wg-15-k2">cost</span><span class="wg-15-center">plan</span></div><div class="wg-15-panels"><div class="wg-15-panel wg-15-p1"><h4 class="wg-15-pt">가장 안쪽 Scan부터 본다</h4><p>어떤 테이블에서 몇 행을 읽는지가 시작점이다. 큰 테이블을 전부 읽는다면 조건식과 인덱스 후보를 먼저 확인한다.</p><p class="wg-15-note-line">핵심: 위 노드는 아래 노드의 결과를 소비한다.</p></div><div class="wg-15-panel wg-15-p2"><h4 class="wg-15-pt">예상 rows와 실제 rows를 비교한다</h4><p>예상 10행인데 실제 10만 행이면 통계나 조건 선택도 추정이 틀렸을 가능성이 높다.</p><p class="wg-15-note-line">핵심: rows 오차는 잘못된 join/scan 선택으로 이어진다.</p></div><div class="wg-15-panel wg-15-p3"><h4 class="wg-15-pt">한 번에 하나의 가설만 실험한다</h4><p>인덱스 추가, 통계 갱신, 쿼리 재작성, 메모리 설정을 동시에 바꾸면 무엇이 효과였는지 알 수 없다.</p><p class="wg-15-note-line">핵심: 작은 실험이 재현 가능한 튜닝을 만든다.</p></div></div></div></div></section>
<div class="grid-2"><article class="summary-card"><h3>Cost를 오해하지 않기</h3><p>cost는 밀리초가 아니다. 디스크/CPU/행 수 추정 등을 planner가 비교하기 위해 만든 상대 비용이다. 절대값보다 같은 DB·같은 조건에서 후보 플랜 간 비교가 의미 있다.</p></article><article class="summary-card"><h3>Rows를 먼저 보는 이유</h3><p>planner가 행 수를 크게 잘못 예상하면 인덱스, join 방식, sort 위치가 줄줄이 달라진다. 튜닝의 첫 질문은 “실제 행 수와 얼마나 다른가?”다.</p></article></div>
'''

example_sql = code('''SELECT id, status, total_price, created_at
FROM orders
WHERE customer_id = 42
ORDER BY created_at DESC
LIMIT 20;''')
plan_text = code('''Limit  (cost=0.43..37.91 rows=20 width=48) (actual time=0.041..0.208 rows=20 loops=1)
  ->  Index Scan Backward using idx_orders_customer_created on orders
      (cost=0.43..12420.55 rows=6624 width=48) (actual time=0.039..0.202 rows=20 loops=1)
      Index Cond: (customer_id = 42)
Planning Time: 0.410 ms
Execution Time: 0.246 ms''')
example = f'''
{h2(4, '예제: 최근 주문 20개를 찾는 쿼리', 'database')}
<p class="h2-sub">예제의 핵심은 인덱스가 “조건 필터”와 “정렬 순서”를 동시에 도와줄 때 LIMIT 쿼리가 어떻게 짧게 끝나는지 보는 것이다.</p>
<pre><code>{example_sql}</code></pre>
<div class="grid-2"><article class="summary-card"><h3>느린 플랜에서 자주 보이는 신호</h3><p><code>Seq Scan</code> 후 많은 행을 버리고, 다시 <code>Sort</code>로 정렬한 뒤 <code>LIMIT</code>을 적용한다. 작은 결과를 얻기 위해 큰 작업을 먼저 한 셈이다.</p></article><article class="summary-card"><h3>좋은 플랜의 방향</h3><p><code>(customer_id, created_at)</code> 계열 인덱스로 필요한 고객의 최신 주문부터 읽으면 LIMIT 20에서 빠르게 멈출 수 있다.</p></article></div>
<section class="wg-14" aria-labelledby="m04-wg14-title"><p class="wg-14-kicker">Feature Explainer · Query Plan</p><h2 id="m04-wg14-title" class="wg-14-h">EXPLAIN ANALYZE 읽는 순서</h2><p class="wg-14-lead">플랜을 통째로 외우지 말고, 결과를 줄이는 노드와 행 수 오차를 먼저 찾는다.</p><div class="wg-14-tldr" role="note" aria-label="핵심 요약"><span class="wg-14-tldr-tag">TL;DR</span><p class="wg-14-tldr-body"><strong>좋은 LIMIT 플랜은 빨리 멈춘다.</strong> 인덱스가 조건과 정렬을 동시에 만족하면 전체 정렬 없이 필요한 20행만 읽는다.</p></div><div class="wg-14-acc"><details class="wg-14-sec" open><summary class="wg-14-sum"><span class="wg-14-sum-no">01</span> 노드 이름을 먼저 읽기 <span class="wg-14-chev" aria-hidden="true"></span></summary><div class="wg-14-sec-body"><p><code>Index Scan Backward</code>는 인덱스 역순으로 읽는다는 뜻이다. <code>ORDER BY created_at DESC</code>와 방향이 맞으면 별도 Sort가 필요 없다.</p><ul class="wg-14-list"><li>Index Cond가 조건식을 얼마나 흡수했는지 확인</li><li>Filter가 남아 있으면 인덱스 밖에서 버린 행이 있는지 확인</li></ul></div></details><details class="wg-14-sec"><summary class="wg-14-sum"><span class="wg-14-sum-no">02</span> actual rows와 loops 확인 <span class="wg-14-chev" aria-hidden="true"></span></summary><div class="wg-14-sec-body"><ol class="wg-14-flow"><li><span class="wg-14-flow-n">1</span> 각 노드가 실제 몇 행을 내보냈는지 본다.</li><li><span class="wg-14-flow-n">2</span> loops가 1보다 크면 반복 실행 비용을 곱해서 생각한다.</li><li><span class="wg-14-flow-n">3</span> 예상 rows와 실제 rows 차이가 크면 통계·조건식을 의심한다.</li></ol></div></details></div><h3 class="wg-14-h3">실행 예시</h3><div class="wg-14-tabs"><input type="radio" name="m04-wg14-tab" id="m04-wg14-tab-plan" class="wg-14-tab-in" checked><input type="radio" name="m04-wg14-tab" id="m04-wg14-tab-index" class="wg-14-tab-in"><input type="radio" name="m04-wg14-tab" id="m04-wg14-tab-check" class="wg-14-tab-in"><div class="wg-14-tablist"><label class="wg-14-tab" for="m04-wg14-tab-plan">plan</label><label class="wg-14-tab" for="m04-wg14-tab-index">index</label><label class="wg-14-tab" for="m04-wg14-tab-check">check</label></div><pre class="wg-14-code wg-14-code-yml"><code>{plan_text}</code></pre><pre class="wg-14-code wg-14-code-cli"><code>CREATE INDEX CONCURRENTLY idx_orders_customer_created
ON orders (customer_id, created_at DESC);</code></pre><pre class="wg-14-code wg-14-code-api"><code>-- 비교는 같은 조건에서
EXPLAIN (ANALYZE, BUFFERS)
SELECT ...;</code></pre></div><h3 class="wg-14-h3">자주 묻는 질문</h3><div class="wg-14-faq"><details class="wg-14-q"><summary class="wg-14-q-sum">Index Scan이면 항상 빠른가요</summary><p class="wg-14-q-a">아니다. 결과 행이 너무 많거나 랜덤 I/O가 많으면 Seq Scan이 더 나을 수 있다.</p></details><details class="wg-14-q"><summary class="wg-14-q-sum">Sort가 있으면 무조건 나쁜가요</summary><p class="wg-14-q-a">아니다. 작은 결과를 정렬하는 Sort는 괜찮다. 큰 테이블을 대부분 읽고 정렬하면 위험 신호다.</p></details></div></section>
'''

practice = f'''
{h2(5, '실습: 한 번에 하나만 바꿔 보기', 'experiment')}
<p class="h2-sub">실습의 목적은 “인덱스를 넣었더니 빨라졌다”가 아니라, 왜 빨라졌는지 플랜 신호로 설명하는 것이다.</p>
<div class="grid-3"><article class="summary-card"><h3>실습 A · 기준선 저장</h3><p>현재 쿼리와 <code>EXPLAIN (ANALYZE, BUFFERS)</code> 결과를 저장한다. 실행 시간만 적지 말고 Scan 방식, rows 오차, Sort 유무도 함께 적는다.</p></article><article class="summary-card"><h3>실습 B · 인덱스 후보</h3><p><code>customer_id</code> 단일 인덱스와 <code>(customer_id, created_at DESC)</code> 복합 인덱스의 차이를 예측한 뒤 하나씩 비교한다.</p></article><article class="summary-card"><h3>실습 C · 통계 확인</h3><p>데이터가 크게 바뀐 뒤라면 <code>ANALYZE orders;</code> 전후 rows 추정이 달라지는지 확인한다.</p></article></div>
<section class="vt-shell" aria-label="실습 절차 주석 흐름"><div class="vt-frame"><div class="cf"><div class="cf-item"><span class="cf-check">1</span><div><b>기준 플랜 캡처</b><p class="vt-text">SQL, plan, 실행 조건을 그대로 저장한다.</p></div><span class="cf-state">START</span></div><div class="cf-item"><span class="cf-check">2</span><div><b>가설 하나 선택</b><p class="vt-text">인덱스·통계·쿼리 재작성 중 하나만 바꾼다.</p></div><span class="cf-state">DO</span></div><div class="cf-item"><span class="cf-check">3</span><div><b>같은 쿼리 재측정</b><p class="vt-text">rows, buffers, sort, execution time을 다시 기록한다.</p></div><span class="cf-state">CHECK</span></div></div></div></section>
<div class="summary-card"><h3>제출물</h3><p>실습 결과는 “변경 전 플랜 → 바꾼 것 → 변경 후 플랜 → 좋아진 신호/나빠진 신호 → 다음 실험” 5줄로 정리한다. 단일 숫자 비교가 아니라 플랜 근거를 포함해야 한다.</p></div>
'''

quiz = f'''
{h2(6, '퀴즈', 'question')}
<p class="h2-sub">아래 문제는 정답 맞히기보다 판단 근거를 말하는 연습이다. 모르는 항목은 확인해야 할 추가 정보로 표시한다.</p>
<div class="grid-2"><article class="summary-card"><h3>Q1</h3><p><code>Seq Scan</code>이 보이면 무조건 인덱스를 만들어야 하는가?</p><ol><li>항상 그렇다</li><li>항상 아니다</li><li>테이블 크기, 선택도, 필요한 행 수에 따라 다르다</li></ol></article><article class="summary-card"><h3>Q2</h3><p>예상 rows 10, 실제 rows 100000이면 가장 먼저 의심할 것은?</p><ol><li>통계 또는 조건 선택도 추정</li><li>SQL 키워드 대소문자</li><li>LIMIT 값 자체</li></ol></article><article class="summary-card"><h3>Q3</h3><p><code>EXPLAIN ANALYZE</code>를 운영 DB에서 실행하기 전 확인할 것은?</p><ol><li>실제 실행해도 되는 쿼리인지</li><li>결과 컬럼 이름이 예쁜지</li><li>테이블 이름 길이</li></ol></article><article class="summary-card"><h3>Q4</h3><p><code>ORDER BY created_at DESC LIMIT 20</code>이 느리다면 유력한 인덱스 후보는?</p><ol><li><code>(customer_id, created_at DESC)</code></li><li><code>(total_price)</code></li><li><code>(status)</code>만 단독</li></ol></article></div>
'''

answers = f'''
{h2(7, '정답 해설', 'success')}
<p class="h2-sub">정답은 하나의 공식이 아니라, 실행 계획에서 어떤 신호를 확인해야 하는지와 함께 이해해야 한다.</p>
<div class="table-scroll mobile-card-table"><table class="mobile-card-table"><caption>쿼리 플랜 워크숍 퀴즈 정답과 해설</caption><thead><tr><th>문항</th><th>정답</th><th>해설</th></tr></thead><tbody><tr><th>Q1</th><td data-label="정답">3</td><td data-label="해설">작은 테이블이나 대부분의 행을 읽는 쿼리에서는 Seq Scan이 합리적일 수 있다. 선택도와 반환 행 수가 핵심이다.</td></tr><tr><th>Q2</th><td data-label="정답">1</td><td data-label="해설">rows 오차가 크면 planner가 잘못된 비용 비교를 했을 수 있다. 통계 최신화와 조건식 분포를 확인한다.</td></tr><tr><th>Q3</th><td data-label="정답">1</td><td data-label="해설">ANALYZE는 실제 실행한다. 쓰기 쿼리, 긴 쿼리, 락 가능성이 있는 쿼리는 안전 장치가 필요하다.</td></tr><tr><th>Q4</th><td data-label="정답">1</td><td data-label="해설">조건과 정렬을 함께 만족하는 복합 인덱스가 LIMIT 조기 종료를 도울 가능성이 높다. 실제 효과는 플랜으로 확인한다.</td></tr></tbody></table></div>
'''

review = f'''
{h2(8, '복습 체크리스트', 'check')}
<p class="h2-sub">다음 체크가 가능하면 이 워크숍의 최소 목표를 달성한 것이다. 모르면 다시 예제 플랜을 보고 답을 채운다.</p>
<div class="grid-2"><article class="summary-card"><h3>개념 점검</h3><ul><li>Cost가 시간 단위가 아니라 상대 비용임을 설명할 수 있다.</li><li>Rows 예상과 actual rows 차이가 왜 중요한지 말할 수 있다.</li><li>Seq Scan이 항상 나쁜 것은 아님을 사례로 설명할 수 있다.</li></ul></article><article class="summary-card"><h3>실무 점검</h3><ul><li>EXPLAIN ANALYZE 실행 전에 안전성을 확인한다.</li><li>튜닝 전후 플랜을 같은 조건으로 비교한다.</li><li>인덱스·통계·쿼리 변경을 한 번에 하나씩 실험한다.</li></ul></article></div>
'''

source_note = '<p class="label">작성 기준</p><p>mode 04 education_html 전용 course-module 레이아웃, education 레시피, layout/writing/body-icon/visual-html/widget 참조, vt timeline/checklist-flow/concept-explainer, wg-14 Feature Explainer, wg-15 Concept Explainer를 사용했다. 기존 출력 HTML 본문은 렌더 입력으로 사용하지 않았다.</p>'

layout = (ASSETS / 'layouts/course-module.html').read_text(encoding='utf-8')
body = layout
repl = {
    'KICKER': '<span class="kicker-text">MODE 04 · EDUCATION HTML · CAPTURE REVIEW</span>',
    'TITLE': 'PostgreSQL 쿼리 플랜 읽기 워크숍',
    'SUBTITLE': 'EXPLAIN 결과를 읽고, rows 오차와 Scan/Sort/Index 신호를 근거로 다음 실험을 설계하는 교육 모듈.',
    'META': '<span>profile auto</span><span>layout course-module</span><span>vt timeline</span><span>wg-14/wg-15</span><span>no behavioral JS</span>' + generated,
    'LEARNING_GOALS': goals,
    'BEFORE_START': before,
    'CONCEPT_LESSON': lesson,
    'EXAMPLE': example,
    'PRACTICE': practice,
    'QUIZ': quiz,
    'ANSWER_KEY': answers,
    'REVIEW_CHECKLIST': review,
    'SOURCE_NOTE': source_note,
}
for k, v in repl.items():
    body = body.replace('{{' + k + '}}', v)

base = (ASSETS / 'base.html').read_text(encoding='utf-8')
html_doc = base
head_slots = {
    'TITLE': 'PostgreSQL 쿼리 플랜 읽기 워크숍',
    'DESCRIPTION': 'education_html 모드로 PostgreSQL EXPLAIN, EXPLAIN ANALYZE, cost, rows, actual, Index Scan과 Sort를 실습·퀴즈·정답 해설로 배우는 한국어 HTML 교육 모듈.',
    'JSON_LD_BLOCK': '',
    'BODY': body,
    'FOOTER': '',
}
for k, v in {**css_slots, **head_slots}.items():
    html_doc = html_doc.replace('{{' + k + '}}', v)
if '{{' in html_doc:
    raise SystemExit('unresolved placeholder remains')
OUT.write_text(html_doc, encoding='utf-8')

evidence = {
    'mode': '04_education_html',
    'file': str(OUT.relative_to(ROOT)),
    'link': 'http://localhost:8080/output/2026-06-07/adaptive-html-final-sequential-16-modes-20260607_105404/pages/04_education_postgres_query_plan_workshop.html',
    'policy': 'previous HTML body not reused by render script; common generator not used; education_html layout/recipe/references/templates consulted for this page only',
    'materials_sha256': MATERIAL_HASH,
    'used_materials': [str(p.relative_to(REPO)) for p in MODE_MATERIALS],
    'placeholder_mapping': {
        'LEARNING_GOALS': 'learning goals + vt timeline',
        'BEFORE_START': 'prerequisites + vt checklist-flow',
        'CONCEPT_LESSON': 'concept lecture + vt concept-explainer + wg-15 concept explainer',
        'EXAMPLE': 'query example + wg-14 feature explainer',
        'PRACTICE': 'hands-on tasks + vt checklist-flow',
        'QUIZ': 'four quiz cards',
        'ANSWER_KEY': 'visible answer table with mobile-safe wrapper',
        'REVIEW_CHECKLIST': 'final review checklist in try section',
        'SOURCE_NOTE': 'source/mode limits and no-reuse note'
    },
    'visual_contract': {
        'layout': 'course-module.html',
        'direct_sections_expected': 8,
        'numbered_h2_order': 'body-icon body-icon--sm -> num -> title',
        'vt_required': ['timeline'],
        'vt_used': ['timeline', 'checklist-flow', 'concept-explainer'],
        'wg_used': ['14-feature-explainer', '15-concept-explainer'],
        'table_mobile_safe': 'table-scroll + mobile-card-table where table is used',
        'education_signature_blocks': ['learning goals', 'before start', 'concept lesson', 'example', 'practice', 'quiz', 'answer key', 'review checklist']
    },
    'review_findings_and_fixes': [
        '기존 화면은 큰 overflow나 h2 아이콘 누락은 없었지만, 목표 조건상 기존 HTML 본문을 신뢰하지 않고 education 전용 자료만 읽는 전용 렌더러로 재생성했다.',
        '교육 모드 특성이 흐려지지 않도록 학습목표→준비→개념→예제→실습→퀴즈→정답→복습 순서를 layout placeholder에 1:1 매핑했다.',
        '테이블은 모두 table-scroll 또는 mobile-card-table로 감싸 390px overflow 회귀를 막았다.'
    ],
    'skill_patch_candidates_from_mode_review': [
        'education_html은 course-module placeholder 8개가 모두 채워져야 완료로 본다.',
        '교육 모드에는 quiz와 answer key가 동시에 있어야 하며, 정답 표는 모바일 safe wrapper를 강제한다.',
        'EXPLAIN/실습형 교육처럼 코드와 표가 함께 있는 섹션은 390px 캡쳐를 완료 조건으로 둔다.'
    ],
    'next_mode': '05_github_analysis'
}
(ROOT / 'sources/04_education_html-visual-contract-evidence.json').write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(OUT)
