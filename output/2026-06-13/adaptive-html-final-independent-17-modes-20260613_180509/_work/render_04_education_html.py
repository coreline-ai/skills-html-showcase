#!/usr/bin/env python3
"""Mode 04 / 17 — education_html (sequential). Topic: Rust 소유권과 빌림 입문 4주 온보딩.
Layout: course-module.html (.layout-education) · auto · vt: timeline(tl-item) · wg: wg-13
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _finalize import build_page, write_sources, h2, SKILL, ASSETS  # noqa: E402,F401

for _p in [SKILL/"SKILL.md", SKILL/"references/writing-system.md", ASSETS/"layouts/course-module.html",
           ASSETS/"visual-html-templates/04-timeline.html", ASSETS/"widget-templates/13-annotated-flowchart.html"]:
    _p.read_text(encoding="utf-8")

TITLE = "Rust 소유권과 빌림 입문 — 4주 온보딩 모듈"
DESC = "Rust의 소유권·이동·빌림·수명을 비유와 코드, 실습과 퀴즈로 익히는 education_html 모드의 4주 사내 온보딩 교육 모듈."

header = '''
<header class="header course-header">
  <div class="kicker"><span class="kicker-text">EDUCATION · MODE 04 / 17 · 독립 빌드</span></div>
  <h1>Rust 소유권과 빌림, 4주로 익히기</h1>
  <p class="sub">가비지 컬렉터 없이 메모리 안전을 보장하는 Rust의 핵심 — 소유권·이동·빌림·수명을 비유에서 코드, 실습, 퀴즈까지 단계로 익히는 사내 온보딩 모듈이다.</p>
  <div class="meta"><span>profile auto</span><span>layout course-module</span><span>대상 신입~주니어</span><span>선수 기초 프로그래밍</span></div>
  <div class="generated-row"><p class="generated-date">Generated · 2026-06-13 KST</p>
  <div class="lens-strip" aria-label="적용 렌즈"><span class="lens-strip-label">LENS</span><span class="lens-chip">학습 목표</span><span class="lens-chip">비유</span><span class="lens-chip">실습</span><span class="lens-chip">퀴즈</span><span class="lens-chip">오개념 교정</span></div></div>
</header>'''

toc = '''
<nav class="toc-map course-toc" aria-label="학습 목차"><div class="toc-pills">
  <a class="toc-pill" href="#s1"><b>01</b> 학습 목표</a><a class="toc-pill" href="#s2"><b>02</b> 4주 학습 여정</a>
  <a class="toc-pill" href="#s3"><b>03</b> 시작 전 준비</a><a class="toc-pill" href="#s4"><b>04</b> 소유권이란</a>
  <a class="toc-pill" href="#s5"><b>05</b> 이동 vs 복사</a><a class="toc-pill" href="#s6"><b>06</b> 빌림 규칙</a>
  <a class="toc-pill" href="#s7"><b>07</b> 빌림 검사 흐름</a><a class="toc-pill" href="#s8"><b>08</b> 실습 과제</a>
  <a class="toc-pill" href="#s9"><b>09</b> 퀴즈</a><a class="toc-pill" href="#s10"><b>10</b> 정답·오개념 교정</a>
  <a class="toc-pill" href="#snext"><b>→</b> 복습 체크리스트</a>
</div></nav>'''

s1 = f'''
<section id="s1" class="learning-goals summary-card">
  {h2("01","학습 목표","learning")}
  <p class="h2-sub">이 모듈을 마치면 컴파일러가 왜 특정 코드를 거부하는지 스스로 설명할 수 있어야 한다. 목표는 암기가 아니라 "왜"의 이해다.</p>
  <div class="grid-3">
    <article class="score-card"><h3>이해</h3><p>소유권·이동·빌림·수명이 각각 무엇을 보장하고 무엇을 막는지 한 문장으로 설명할 수 있다.</p></article>
    <article class="score-card"><h3>적용</h3><p>borrow checker가 낸 오류 메시지를 읽고, 가변/불변 빌림 규칙 위반을 직접 고칠 수 있다.</p></article>
    <article class="score-card"><h3>판단</h3><p>값을 이동시킬지, 빌려줄지, 복제(clone)할지를 상황에 맞게 선택하고 그 트레이드오프를 말할 수 있다.</p></article>
  </div>
  <p>핵심은 단 하나의 원칙에서 출발한다. <strong>"하나의 값에는 하나의 소유자만 있고, 소유자가 사라지면 값도 정리된다."</strong> 이 모듈의 모든 규칙은 이 문장의 따름정리다. 처음에는 규칙이 많아 보이지만, 결국 이 한 문장을 다양한 상황에 적용하는 연습일 뿐이다.</p>
</section>'''

s2 = f'''
<section id="s2" class="summary-card">
  {h2("02","4주 학습 여정","timeline")}
  <p class="h2-sub">개념을 한 번에 쏟지 않고, 매주 하나의 질문에 답하며 쌓아 올린다.</p>
  <section class="vt-shell" aria-label="4주 커리큘럼 타임라인">
    <div class="vt-frame"><ol class="tl">
      <li class="tl-item"><b>1주 · 소유권</b><p class="vt-text">"이 값은 누구 것인가?" 스코프와 정리(drop) 시점을 손으로 추적한다.</p></li>
      <li class="tl-item"><b>2주 · 이동</b><p class="vt-text">"대입하면 복사일까 이동일까?" move 의미론과 clone 비용을 비교한다.</p></li>
      <li class="tl-item"><b>3주 · 빌림</b><p class="vt-text">"소유권을 넘기지 않고 쓰려면?" 불변/가변 참조 규칙을 익힌다.</p></li>
      <li class="tl-item"><b>4주 · 수명</b><p class="vt-text">"참조가 가리키는 값이 먼저 사라지면?" 수명 표기로 댕글링을 막는다.</p></li>
    </ol></div>
  </section>
  <p>각 주는 이전 주의 답을 전제로 한다. 소유권을 모르면 이동이 안 보이고, 이동을 모르면 빌림이 왜 필요한지 와닿지 않는다. 순서를 건너뛰지 않는 것이 가장 빠른 길이다.</p>
</section>'''

s3 = f'''
<section id="s3" class="before-start summary-card">
  {h2("03","시작 전 준비","check")}
  <p class="h2-sub">설치와 사고방식 두 가지를 준비한다. 환경보다 중요한 건 "컴파일러를 적이 아니라 코치로 보는" 태도다.</p>
  <ul class="check-list">
    <li><strong>도구</strong> — <code>rustup</code>으로 stable 툴체인 설치, <code>cargo new</code>로 연습 프로젝트 생성.</li>
    <li><strong>사고 전환</strong> — 컴파일 오류는 실패가 아니라 "런타임에 터질 버그를 미리 알려주는 리뷰"라고 본다.</li>
    <li><strong>비교 기준</strong> — C/C++의 수동 해제, 자바/파이썬의 GC를 떠올려 두면 Rust의 선택이 또렷해진다.</li>
  </ul>
  <div class="good"><span class="label">마음가짐</span><p>처음에는 borrow checker와 싸우는 느낌이 든다. 그러나 이 싸움은 곧 "메모리 버그를 컴파일 단계로 끌어올린" 거래임을 알게 된다. 며칠이면 직관이 생긴다.</p></div>
</section>'''

s4 = f'''
<section id="s4" class="lesson-step summary-card">
  {h2("04","소유권이란 무엇인가","idea")}
  <p class="h2-sub">소유권은 "이 값을 정리할 책임이 누구에게 있는가"를 컴파일 시점에 못 박는 규칙이다.</p>
  <div class="analogy"><span class="label">비유</span><p>도서관 책 한 권을 떠올리자. 책은 한 번에 한 사람에게만 대출된다(소유자 1명). 대출자가 반납하면(스코프 종료) 책은 서가로 돌아간다(메모리 정리). 사본 없이 원본을 다른 사람에게 넘기면(이동), 원래 대출자는 더 이상 그 책을 읽을 수 없다.</p></div>
  <p>Rust는 이 규칙을 런타임 검사나 GC가 아니라 <strong>컴파일 타임</strong>에 강제한다. 그래서 실행 중 추가 비용이 없고(영-비용 추상화), 동시에 use-after-free 같은 메모리 버그가 원천적으로 차단된다. 값이 스코프를 벗어나는 순간 <code>drop</code>이 자동 호출되어 자원이 정리된다.</p>
</section>'''

s5 = ('<section id="s5" class="example-block summary-card">' + h2("05","이동 vs 복사 — 코드로 보기","code") + '''
  <p class="h2-sub">힙에 데이터를 둔 타입은 대입할 때 '이동'한다. 같은 코드라도 어떤 타입이냐에 따라 동작이 갈린다.</p>
  <pre><code>let a = String::from("hello");
let b = a;            // a의 소유권이 b로 '이동'
// println!("{}", a); // 컴파일 오류: a는 더 이상 유효하지 않음
println!("{}", b);    // OK

let x = 5;            // i32는 Copy 타입
let y = x;            // '복사' — x도 그대로 유효
println!("{} {}", x, y); // OK</code></pre>
  <p><code>String</code>은 힙 버퍼를 가리키므로, 둘이 같은 버퍼를 소유하면 이중 해제 위험이 생긴다. Rust는 이를 막으려고 대입 시 소유권을 <strong>이동</strong>시키고 원본을 무효화한다. 반대로 <code>i32</code>처럼 스택에만 사는 작은 값은 <code>Copy</code>라서 그냥 복사된다. 원본을 계속 쓰고 싶다면 <code>a.clone()</code>으로 깊은 복사를 명시하되, 그 비용(힙 할당)을 인지하고 선택한다.</p>
</section>''')

s6 = f'''
<section id="s6" class="lesson-step summary-card">
  {h2("06","빌림 규칙 — 넘기지 않고 쓰기","reference")}
  <p class="h2-sub">매번 소유권을 넘기면 불편하다. 그래서 참조(&)로 '빌려' 쓴다. 단, 빌림에는 두 가지 철칙이 있다.</p>
  <div class="card-grid">
    <article class="mini-card"><h3>규칙 1 · 공유 vs 독점</h3><p>불변 참조(<code>&T</code>)는 여러 개 동시에 가능하지만, 가변 참조(<code>&mut T</code>)는 그 순간 오직 하나만 존재할 수 있다.</p></article>
    <article class="mini-card"><h3>규칙 2 · 동시 불가</h3><p>가변 참조가 살아 있는 동안에는 불변 참조도 만들 수 없다. 읽는 사람과 쓰는 사람이 겹치지 않게 한다.</p></article>
    <article class="mini-card"><h3>왜?</h3><p>이 두 규칙이 데이터 경쟁(data race)을 컴파일 단계에서 차단한다. 동시성 버그의 큰 축이 사라진다.</p></article>
  </div>
  <div class="danger"><span class="label">흔한 오류</span><p>"cannot borrow as mutable more than once" 메시지는 가변 참조를 두 번 만들었다는 뜻이다. 한 참조의 사용 범위를 좁히거나, 스코프 블록으로 분리하면 해결된다.</p></div>
</section>'''

s7 = f'''
<section id="s7" class="summary-card">
  {h2("07","빌림 검사 흐름 따라가기","flow")}
  <p class="h2-sub">컴파일러가 참조를 어떤 순서로 검사하는지 흐름으로 보면, 오류 메시지가 더 이상 무섭지 않다.</p>
  <section class="wg-13-fc" aria-label="빌림 검사 흐름">
    <h3 class="wg-13-h">borrow checker 판단 흐름 <span class="wg-13-sub">참조 생성 시점마다 실행</span></h3>
    <div class="wg-13-flow">
      <a href="#bc-s1" class="wg-13-node wg-13-node--start"><span class="wg-13-step">시작</span>참조 생성</a>
      <span class="wg-13-arrow" aria-hidden="true">&darr;</span>
      <div class="wg-13-branch">
        <a href="#bc-s2" class="wg-13-node wg-13-node--decide"><span class="wg-13-step">?</span>가변 참조인가?</a>
        <div class="wg-13-paths">
          <div class="wg-13-path wg-13-path--fail"><span class="wg-13-edge">예 &rarr; 독점 필요</span><a href="#bc-fail" class="wg-13-node wg-13-node--fail"><span class="wg-13-step">!</span>다른 참조 있으면 거부</a></div>
          <div class="wg-13-path wg-13-path--ok"><span class="wg-13-edge">아니오 &rarr; 공유 가능</span><a href="#bc-ok" class="wg-13-node wg-13-node--end"><span class="wg-13-step">완료</span>불변 다중 허용</a></div>
        </div>
      </div>
    </div>
    <div class="wg-13-detail">
      <h4 class="wg-13-dh">단계 상세 <span class="wg-13-dnote">박스를 펼쳐 규칙을 확인</span></h4>
      <details id="bc-s2" class="wg-13-acc" open><summary><span class="wg-13-tag">판단</span>가변/불변 구분</summary><div class="wg-13-body"><p>같은 값에 대해 가변 참조 1개 또는 불변 참조 N개 중 하나만 동시에 살아 있을 수 있습니다.</p></div></details>
      <details id="bc-fail" class="wg-13-acc wg-13-acc--fail"><summary><span class="wg-13-tag wg-13-tag--fail">거부</span>충돌</summary><div class="wg-13-body"><p>가변 참조 중 다른 참조가 살아 있으면 컴파일 거부. 참조 수명을 좁혀 해결합니다.</p></div></details>
      <details id="bc-ok" class="wg-13-acc wg-13-acc--ok"><summary><span class="wg-13-tag wg-13-tag--ok">허용</span>공유 읽기</summary><div class="wg-13-body"><p>불변 참조는 여러 개가 동시에 읽기만 하므로 안전합니다.</p></div></details>
    </div>
  </section>
</section>'''

s8 = f'''
<section id="s8" class="practice-card summary-card">
  {h2("08","실습 과제","experiment")}
  <p class="h2-sub">읽기만으로는 직관이 생기지 않는다. 아래 두 과제를 직접 컴파일하며 오류 메시지를 마주하자.</p>
  <ol class="practice-list">
    <li><strong>과제 A</strong> — <code>String</code> 벡터를 받아 가장 긴 문자열의 길이를 반환하는 함수를 작성하되, 인자를 <strong>이동시키지 말고 빌려서</strong>(&amp;) 처리하라.</li>
    <li><strong>과제 B</strong> — 카운터 구조체에 <code>increment(&amp;mut self)</code>를 만들고, 같은 스코프에서 불변 참조와 가변 참조를 동시에 시도해 오류를 직접 확인한 뒤 스코프 분리로 고쳐라.</li>
  </ol>
  <div class="good"><span class="label">힌트</span><p>과제 A에서 반환 타입은 소유권을 가질 필요가 없는 <code>usize</code>다. 입력은 <code>&amp;[String]</code>이면 충분하다. "필요한 최소 권한만 빌린다"가 좋은 시그니처의 기준이다.</p></div>
</section>'''

s9 = f'''
<section id="s9" class="quiz-box summary-card">
  {h2("09","퀴즈","question")}
  <p class="h2-sub">정답을 보기 전에 스스로 답을 적어 보자. 틀린 곳이 곧 다음에 복습할 곳이다.</p>
  <ol class="quiz-list">
    <li><strong>Q1.</strong> <code>let b = a;</code> 이후 <code>a</code>를 다시 쓰면 항상 오류일까? 어떤 조건에서 괜찮은가?</li>
    <li><strong>Q2.</strong> 같은 값에 대해 불변 참조 3개와 가변 참조 1개를 동시에 만들 수 있는가? 이유는?</li>
    <li><strong>Q3.</strong> <code>clone()</code>은 언제 쓰는 게 정당하고, 언제 설계 냄새인가?</li>
  </ol>
</section>'''

s10 = f'''
<section id="s10" class="answer-box summary-card">
  {h2("10","정답 · 오개념 교정","success")}
  <p class="h2-sub">정답과 함께 자주 빠지는 오해를 바로잡는다. 표현이 아니라 모델을 고치는 것이 목적이다.</p>
  <div class="table-scroll"><table>
    <caption>퀴즈 정답과 흔한 오개념</caption>
    <thead><tr><th>문항</th><th>정답 요지</th><th>흔한 오개념</th></tr></thead>
    <tbody>
      <tr><th>Q1</th><td><code>a</code>가 <code>Copy</code> 타입(예: i32)이면 복사라서 OK. <code>String</code>이면 이동이라 오류.</td><td>"대입은 늘 복사"라는 C식 직관</td></tr>
      <tr><th>Q2</th><td>불가능. 가변 참조가 있으면 불변 참조와 공존할 수 없다.</td><td>"읽기 1개쯤은 괜찮겠지"</td></tr>
      <tr><th>Q3</th><td>소유권이 정말 필요할 때만 clone. 빌림으로 충분하면 설계 냄새.</td><td>"오류 나면 일단 clone"</td></tr>
    </tbody>
  </table></div>
  <p>가장 큰 오개념은 "borrow checker를 통과시키려고 clone을 남발하는 것"이다. clone은 도구일 뿐, 빈번한 clone은 대개 소유권 설계를 다시 보라는 신호다. 오류 메시지를 회피하지 말고 모델을 점검하자.</p>
</section>'''

snext = f'''
<section id="snext" class="try">
  {h2(None,"복습 체크리스트 · 다음 단계","landing")}
  <p>아래 항목에 모두 "네"라고 답할 수 있으면 다음 주제(스마트 포인터·동시성)로 넘어갈 준비가 된 것이다.</p>
  <div class="cta-box">
    <p><strong>스스로 점검</strong></p>
    <ol><li>이동과 복사의 차이를 타입을 들어 설명할 수 있다.</li><li>불변/가변 빌림 규칙 두 가지를 외우지 않고 이유로 말할 수 있다.</li><li>borrow checker 오류 한 개를 읽고 스스로 고칠 수 있다.</li></ol>
    <div class="tag-list"><span class="tag">education</span><span class="tag">rust</span><span class="tag">ownership</span><span class="tag">borrow-checker</span></div>
  </div>
</section>'''

source_note = '<aside class="source-note"><p><strong>출처·범위.</strong> 본 모듈은 Rust 공식 문서(The Rust Programming Language)의 소유권 모델을 사내 온보딩용으로 재구성한 교육 자료다. 코드 예시는 stable 툴체인 기준의 대표 패턴이며, 특정 버전별 세부 동작은 실제 컴파일러 메시지로 확인한다.</p></aside>'

body = ('<main id="main" class="page-wide layout-education">' + header + toc + s1+s2+s3+s4+s5+s6+s7+s8+s9+s10+snext + source_note + '</main>')
out = build_page("pages/04_education_html_rust_ownership.html", title=TITLE, description=DESC, body=body)
write_sources()
print("WROTE", out)
