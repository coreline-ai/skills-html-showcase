#!/usr/bin/env python3
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "pages"


def replace_main(filename: str, main_html: str) -> None:
    path = PAGES / filename
    text = path.read_text(encoding="utf-8")
    main_html = add_vt_template_labels(main_html)
    updated, count = re.subn(r'<main id="main"[\s\S]*?</main>', main_html.strip(), text, count=1)
    if count != 1:
        raise RuntimeError(f"main replacement failed for {filename}: {count}")
    path.write_text(updated, encoding="utf-8")


def mark(name: str, body: str) -> str:
    return f'<!-- template-showcase:start {name} --><div class="summary-card template-showcase"><div class="label">TEMPLATE CHECK · {name}</div>{body.strip()}</div><!-- template-showcase:end {name} -->'


VT_NAMES = {
    "02": "decision-tree",
    "03": "risk-matrix",
    "06": "quality-gate",
    "07": "card-grid",
    "09": "file-tour",
    "10": "flowchart",
    "13": "comparison-cards",
}


def add_vt_template_labels(main_html: str) -> str:
    lines = []
    pattern = re.compile(r'(?P<prefix><section><h2><span class="no">\d+</span>vt-(?P<num>\d{2})[\s\S]*?</p>)(?P<body><div class="vt-shell">[\s\S]*</div>)(?P<suffix></section>)$')
    for line in main_html.splitlines():
        match = pattern.match(line)
        if match and "template-showcase:start vt-" not in line:
            num = match.group("num")
            name = f"vt-{num} {VT_NAMES.get(num, 'visual-template')}"
            line = f"{match.group('prefix')}{mark(name, match.group('body'))}{match.group('suffix')}"
        lines.append(line)
    return "\n".join(lines)


SEO_WG11 = mark("wg-11 weekly-status", """
<section class="wg-11" aria-labelledby="seo-wg11-title">
  <header class="wg-11-head"><p class="wg-11-kicker">SEO STATUS</p><h2 id="seo-wg11-title" class="wg-11-h">검색 허브 성과 대시보드</h2><p class="wg-11-lead">검색 의도 커버리지, FAQ 완성도, 보안 설명, 전환 CTA를 주간 상태처럼 점검한다.</p></header>
  <div class="wg-11-kpis"><div class="wg-11-kpi"><span class="wg-11-kpi-v">4</span><span class="wg-11-kpi-l">의도 클러스터</span></div><div class="wg-11-kpi"><span class="wg-11-kpi-v">12</span><span class="wg-11-kpi-l">FAQ 후보</span></div><div class="wg-11-kpi"><span class="wg-11-kpi-v wg-11-warn">2</span><span class="wg-11-kpi-l">보안 리스크</span></div><div class="wg-11-kpi"><span class="wg-11-kpi-v">3</span><span class="wg-11-kpi-l">CTA 경로</span></div></div>
  <h3 class="wg-11-h3">콘텐츠 블록 완성도</h3><div class="wg-11-bars"><div class="wg-11-bar-row"><span class="wg-11-bar-label">검색 의도</span><div class="wg-11-track"><div class="wg-11-fill wg-11-fill-good" style="width:92%"></div></div><span class="wg-11-bar-pct">92%</span></div><div class="wg-11-bar-row"><span class="wg-11-bar-label">도구 비교</span><div class="wg-11-track"><div class="wg-11-fill wg-11-fill-prog" style="width:76%"></div></div><span class="wg-11-bar-pct">76%</span></div><div class="wg-11-bar-row"><span class="wg-11-bar-label">동의·보안</span><div class="wg-11-track"><div class="wg-11-fill wg-11-fill-risk" style="width:58%"></div></div><span class="wg-11-bar-pct">58%</span></div></div>
</section>
""")


PLATFORM_WG02 = mark("wg-02 visual-design-directions", """
<section class="wg-02-dir" aria-labelledby="platform-wg02-title">
  <header class="wg-02-head"><p class="wg-02-kicker">PLATFORM DIRECTIONS</p><h2 id="platform-wg02-title" class="wg-02-h">플랫폼별 발행 방향 비교</h2><p class="wg-02-lead">같은 발표라도 플랫폼별 독자 질문과 글의 리듬은 다르다. 카드를 선택하면 방향이 강조된다.</p></header>
  <fieldset class="wg-02-grid"><legend class="wg-02-sr">플랫폼 방향 선택</legend>
    <input type="radio" name="platform-wg02-pick" id="platform-wg02-a" class="wg-02-radio" checked><div class="wg-02-card"><div class="wg-02-preview wg-02-preview--a"><div class="wg-02-pv-bar"><span class="wg-02-pv-dot"></span><span class="wg-02-pv-line"></span></div><div class="wg-02-pv-hero">Tistory</div><div class="wg-02-pv-body"><span></span><span></span><span class="wg-02-pv-short"></span></div><div class="wg-02-pv-cta wg-02-pv-cta--a">검색형 목차</div></div><div class="wg-02-meta"><label for="platform-wg02-a" class="wg-02-pick-label">티스토리 · 검색형</label><p class="wg-02-desc">긴 설명, 목차, 표, FAQ로 검색 유입을 받는다.</p><span class="wg-02-badge">선택됨</span></div></div>
    <input type="radio" name="platform-wg02-pick" id="platform-wg02-b" class="wg-02-radio"><div class="wg-02-card"><div class="wg-02-preview wg-02-preview--b"><div class="wg-02-pv-cards"><span></span><span></span><span></span></div><div class="wg-02-pv-cta wg-02-pv-cta--b">개발자 기록</div></div><div class="wg-02-meta"><label for="platform-wg02-b" class="wg-02-pick-label">벨로그 · 기술 회고</label><p class="wg-02-desc">코드, 실패 설정, 환경 정보를 앞에 둔다.</p><span class="wg-02-badge">선택됨</span></div></div>
    <input type="radio" name="platform-wg02-pick" id="platform-wg02-c" class="wg-02-radio"><div class="wg-02-card"><div class="wg-02-preview wg-02-preview--c"><div class="wg-02-pv-split"><div class="wg-02-pv-aside"></div><div class="wg-02-pv-main"><span></span><span></span></div></div><div class="wg-02-pv-cta wg-02-pv-cta--c">브랜드 CTA</div></div><div class="wg-02-meta"><label for="platform-wg02-c" class="wg-02-pick-label">워드프레스 · 브랜드형</label><p class="wg-02-desc">자료실, 다운로드, 문의 CTA로 연결한다.</p><span class="wg-02-badge">선택됨</span></div></div>
  </fieldset>
</section>
""")


AUDIT_WG03 = mark("wg-03 annotated-pull-request", """
<section class="wg-03" aria-labelledby="audit-wg03-title">
  <header class="wg-03-head"><p class="wg-03-kicker">SKILL PATCH REVIEW</p><h2 id="audit-wg03-title" class="wg-03-title">SKILL.md 패치 주석 리뷰</h2><div class="wg-03-meta"><span class="wg-03-chip">SKILL.md</span><span class="wg-03-chip wg-03-chip-add">+owner</span><span class="wg-03-chip wg-03-chip-del">-generic</span><span class="wg-03-chip">quality-gate</span></div><nav class="wg-03-jump" aria-label="노트 점프"><span class="wg-03-jump-label">노트:</span><a href="#audit-wg03-n1" class="wg-03-jump-link wg-03-sev-critical">L18 critical</a><a href="#audit-wg03-n2" class="wg-03-jump-link wg-03-sev-warn">L24 warn</a></nav></header>
  <div class="wg-03-grid"><div class="wg-03-diff" role="table" aria-label="스킬 패치 diff"><div class="wg-03-row wg-03-ctx" role="row"><span class="wg-03-ln">16</span><code class="wg-03-code">output checklist items:</code></div><div id="audit-wg03-l18" class="wg-03-row wg-03-del wg-03-flag" role="row"><span class="wg-03-ln">18</span><code class="wg-03-code"><span class="wg-03-sign">-</span>  - check deployment readiness</code><a href="#audit-wg03-n1" class="wg-03-dot wg-03-sev-critical" aria-label="L18 critical 노트">!</a></div><div class="wg-03-row wg-03-add" role="row"><span class="wg-03-ln">19</span><code class="wg-03-code"><span class="wg-03-sign">+</span>  - owner, evidence, done criteria required</code></div><div id="audit-wg03-l24" class="wg-03-row wg-03-add wg-03-flag" role="row"><span class="wg-03-ln">24</span><code class="wg-03-code"><span class="wg-03-sign">+</span>  - block/warn/info severity required</code><a href="#audit-wg03-n2" class="wg-03-dot wg-03-sev-warn" aria-label="L24 warn 노트">!</a></div></div><aside class="wg-03-notes" aria-label="감사 노트"><article id="audit-wg03-n1" class="wg-03-note wg-03-sev-critical" tabindex="-1"><header class="wg-03-note-head"><span class="wg-03-badge">critical</span><span class="wg-03-note-loc"><a href="#audit-wg03-l18">L18</a></span></header><p class="wg-03-note-body">일반 문구만 생성하면 배포 차단 판단을 돕지 못한다. 담당자와 증빙을 필수 필드로 고정한다.</p></article><article id="audit-wg03-n2" class="wg-03-note wg-03-sev-warn" tabindex="-1"><header class="wg-03-note-head"><span class="wg-03-badge">warn</span><span class="wg-03-note-loc"><a href="#audit-wg03-l24">L24</a></span></header><p class="wg-03-note-body">심각도 없이는 체크리스트가 우선순위를 만들지 못한다.</p></article></aside></div>
</section>
""")


AUDIT_WG17 = mark("wg-17 pr-writeup", """
<section class="wg-17" aria-labelledby="audit-wg17-title">
  <header class="wg-17-head"><p class="wg-17-kicker">PATCH WRITEUP</p><h2 id="audit-wg17-title" class="wg-17-title">배포 체크리스트 스킬 개선안</h2><div class="wg-17-meta"><span class="wg-17-chip wg-17-chip-branch">audit/findings → patch-plan</span><span class="wg-17-chip wg-17-chip-add">+risk gate</span><span class="wg-17-chip wg-17-chip-del">-안심용 항목</span></div></header>
  <div class="wg-17-block"><h3 class="wg-17-h3"><span class="wg-17-h3-no">1</span> Before / After</h3><div class="wg-17-ba"><div class="wg-17-ba-col wg-17-ba-before"><p class="wg-17-ba-tag">Before</p><ul class="wg-17-ba-list"><li>항목 수 중심</li><li>담당자 누락</li><li>차단 조건 모호</li></ul></div><div class="wg-17-ba-arrow" aria-hidden="true">→</div><div class="wg-17-ba-col wg-17-ba-after"><p class="wg-17-ba-tag">After</p><ul class="wg-17-ba-list"><li>위험 등급 중심</li><li>owner/evidence 필수</li><li>rollback 기준 포함</li></ul></div></div></div>
  <div class="wg-17-block"><h3 class="wg-17-h3"><span class="wg-17-h3-no">2</span> 파일별 워크스루</h3><details class="wg-17-file" open><summary class="wg-17-summary"><span class="wg-17-file-name">SKILL.md</span><span class="wg-17-file-stat"><span class="wg-17-add">workflow</span></span><span class="wg-17-caret" aria-hidden="true"></span></summary><div class="wg-17-file-body"><p class="wg-17-p">입력 부족 시 질문을 먼저 출력하고, 고위험 배포는 차단 조건 섹션으로 분리한다.</p></div></details><details class="wg-17-file"><summary class="wg-17-summary"><span class="wg-17-file-name">examples/release.md</span><span class="wg-17-file-stat"><span class="wg-17-add">fixture</span></span><span class="wg-17-caret" aria-hidden="true"></span></summary><div class="wg-17-file-body"><p class="wg-17-p">staging, canary, production 예시를 나눠 회귀 테스트에 사용한다.</p></div></details></div>
</section>
""")


REF_WG14 = mark("wg-14 feature-explainer", """
<section class="wg-14" aria-labelledby="ref-wg14-title">
  <p class="wg-14-kicker">REFERENCE FEATURE</p><h2 id="ref-wg14-title" class="wg-14-h">Webhook 서명 검증 기능 설명</h2><p class="wg-14-lead">서명 검증은 raw body, timestamp, event id, secret rotation을 하나의 요청 경계에서 다룬다.</p>
  <div class="wg-14-tldr" role="note" aria-label="핵심 요약"><span class="wg-14-tldr-tag">TL;DR</span><p class="wg-14-tldr-body"><strong>비즈니스 로직보다 먼저 실패</strong>해야 한다. raw body로 HMAC을 만들고 constant-time 비교 후 replay를 차단한다.</p></div>
  <div class="wg-14-acc"><details class="wg-14-sec" open><summary class="wg-14-sum"><span class="wg-14-sum-no">01</span> 검증 순서 <span class="wg-14-chev" aria-hidden="true"></span></summary><div class="wg-14-sec-body"><ol class="wg-14-flow"><li><span class="wg-14-flow-n">1</span>raw body 보존</li><li><span class="wg-14-flow-n">2</span>HMAC 계산</li><li><span class="wg-14-flow-n">3</span>constant-time 비교</li><li><span class="wg-14-flow-n">4</span>replay cache 확인</li></ol></div></details><details class="wg-14-sec"><summary class="wg-14-sum"><span class="wg-14-sum-no">02</span> 실패 처리 <span class="wg-14-chev" aria-hidden="true"></span></summary><div class="wg-14-sec-body"><p>서명 실패는 401, timestamp 만료는 400, 중복 이벤트는 200 already processed로 분리한다.</p></div></details></div>
</section>
""")


REF_WG19 = mark("wg-19 feature-flag-editor", """
<section class="wg-19-editor" aria-label="Webhook 검증 정책 토글">
  <header class="wg-19-head"><h2 class="wg-19-title">Webhook 검증 정책</h2><p class="wg-19-hint">토글은 CSS-only로 상태가 바뀐다. 실제 서버 반영은 JS/API가 필요하다.</p></header>
  <ul class="wg-19-list"><li class="wg-19-row"><div class="wg-19-info"><span class="wg-19-key">require_signature</span><span class="wg-19-desc">서명 없는 요청 차단</span></div><span class="wg-19-env">prod</span><input class="wg-19-cb" type="checkbox" id="ref-wg19-f1" checked><label class="wg-19-toggle" for="ref-wg19-f1"><span class="wg-19-knob"></span><span class="wg-19-state wg-19-state--on">ON</span><span class="wg-19-state wg-19-state--off">OFF</span></label></li><li class="wg-19-row"><div class="wg-19-info"><span class="wg-19-key">replay_cache</span><span class="wg-19-desc">event id 중복 차단</span><span class="wg-19-dep" role="note">⚠ TTL 10분 권장</span></div><span class="wg-19-env">prod</span><input class="wg-19-cb" type="checkbox" id="ref-wg19-f2" checked><label class="wg-19-toggle" for="ref-wg19-f2"><span class="wg-19-knob"></span><span class="wg-19-state wg-19-state--on">ON</span><span class="wg-19-state wg-19-state--off">OFF</span></label></li><li class="wg-19-row"><div class="wg-19-info"><span class="wg-19-key">accept_legacy_secret</span><span class="wg-19-desc">이전 secret 임시 허용</span><span class="wg-19-dep wg-19-dep--warn" role="note">⚠ rotation 종료 후 제거</span></div><span class="wg-19-env wg-19-env--stg">staging</span><input class="wg-19-cb" type="checkbox" id="ref-wg19-f3"><label class="wg-19-toggle" for="ref-wg19-f3"><span class="wg-19-knob"></span><span class="wg-19-state wg-19-state--on">ON</span><span class="wg-19-state wg-19-state--off">OFF</span></label></li></ul>
</section>
""")


REF_WG20 = mark("wg-20 prompt-tuner", """
<section class="wg-20-tuner" aria-label="Webhook 검증 테스트 케이스 튜너">
  <header class="wg-20-head"><h2 class="wg-20-title">서명 검증 테스트 케이스 튜너</h2><p class="wg-20-hint">케이스를 선택하면 입력과 기대 결과가 CSS-only로 바뀐다.</p></header>
  <fieldset class="wg-20-samples"><legend class="wg-20-legend">테스트 케이스</legend><input class="wg-20-radio" type="radio" name="wg-20-sample" id="wg-20-s1" checked><label class="wg-20-chip" for="wg-20-s1">정상 서명</label><input class="wg-20-radio" type="radio" name="wg-20-sample" id="wg-20-s2"><label class="wg-20-chip" for="wg-20-s2">timestamp 만료</label><input class="wg-20-radio" type="radio" name="wg-20-sample" id="wg-20-s3"><label class="wg-20-chip" for="wg-20-s3">중복 event</label></fieldset>
  <div class="wg-20-grid"><div class="wg-20-pane"><div class="wg-20-pane-head">검증 템플릿</div><pre class="wg-20-tpl">raw_body + timestamp + secret으로 HMAC 계산
expected_signature와 constant-time 비교
event_id replay cache 확인</pre></div><div class="wg-20-pane"><div class="wg-20-pane-head">샘플 입력</div><div class="wg-20-input wg-20-input--s1"><span class="wg-20-k">case</span>valid signature</div><div class="wg-20-input wg-20-input--s2"><span class="wg-20-k">case</span>timestamp older than window</div><div class="wg-20-input wg-20-input--s3"><span class="wg-20-k">case</span>event id already processed</div></div><div class="wg-20-pane"><div class="wg-20-pane-head">기대 결과</div><div class="wg-20-out wg-20-out--s1">200 accepted · business handler로 전달</div><div class="wg-20-out wg-20-out--s2">400 stale request · 처리하지 않음</div><div class="wg-20-out wg-20-out--s3">200 already processed · 재처리 생략</div></div></div>
</section>
""")


COMPARE_WG01 = mark("wg-01 three-code-approaches", """
<section class="wg-01" aria-labelledby="compare-wg01-title">
  <header class="wg-01-head"><p class="wg-01-kicker">ARCHITECTURE OPTIONS</p><h2 id="compare-wg01-title" class="wg-01-title">벡터 검색 세 가지 접근</h2><p class="wg-01-lead">같은 검색 문제를 전용 Vector DB, pgvector, 검색 엔진 하이브리드로 풀 때의 장단점을 카드로 비교한다.</p></header>
  <div class="wg-01-grid" role="list"><article class="wg-01-card" role="listitem"><div class="wg-01-card-head"><span class="wg-01-rank">A</span><div><h3 class="wg-01-card-title">전용 Vector DB</h3><p class="wg-01-card-sub">대규모 ANN · 별도 운영</p></div></div><pre class="wg-01-code" tabindex="0"><code>index = vector_db.create_index(dim=1536)
index.query(vector, top_k=20, filter=tenant)</code></pre><div class="wg-01-cols"><div class="wg-01-pros"><p class="wg-01-coltag wg-01-coltag-good">▲ 장점</p><ul><li>분산 확장</li><li>ANN 최적화</li></ul></div><div class="wg-01-cons"><p class="wg-01-coltag wg-01-coltag-bad">▼ 단점</p><ul><li>새 장애 도메인</li><li>권한 모델 별도</li></ul></div></div></article><article class="wg-01-card wg-01-card-pick" role="listitem"><div class="wg-01-card-head"><span class="wg-01-rank wg-01-rank-pick">B</span><div><h3 class="wg-01-card-title">pgvector <span class="wg-01-pick-badge">MVP 권장</span></h3><p class="wg-01-card-sub">기존 DB · 빠른 도입</p></div></div><pre class="wg-01-code" tabindex="0"><code>SELECT * FROM docs
ORDER BY embedding &lt;-&gt; query
LIMIT 20;</code></pre><div class="wg-01-cols"><div class="wg-01-pros"><p class="wg-01-coltag wg-01-coltag-good">▲ 장점</p><ul><li>권한 공유</li><li>운영 단순</li></ul></div><div class="wg-01-cons"><p class="wg-01-coltag wg-01-coltag-bad">▼ 단점</p><ul><li>대규모 한계</li><li>DB 부하 증가</li></ul></div></div></article><article class="wg-01-card" role="listitem"><div class="wg-01-card-head"><span class="wg-01-rank">C</span><div><h3 class="wg-01-card-title">검색 엔진 하이브리드</h3><p class="wg-01-card-sub">키워드+벡터 · relevance 운영</p></div></div><pre class="wg-01-code" tabindex="0"><code>hybrid = bm25(query) + vector(query)
rerank(hybrid, rules)</code></pre><div class="wg-01-cols"><div class="wg-01-pros"><p class="wg-01-coltag wg-01-coltag-good">▲ 장점</p><ul><li>키워드 보강</li><li>설명 가능성</li></ul></div><div class="wg-01-cons"><p class="wg-01-coltag wg-01-coltag-bad">▼ 단점</p><ul><li>랭킹 운영</li><li>색인 복잡</li></ul></div></div></article></div>
</section>
""")


COMPARE_WG02 = mark("wg-02 visual-design-directions", """
<section class="wg-02-dir" aria-labelledby="compare-wg02-title">
  <header class="wg-02-head"><p class="wg-02-kicker">CHOICE DIRECTIONS</p><h2 id="compare-wg02-title" class="wg-02-h">선택 상황별 추천</h2><p class="wg-02-lead">MVP, 대규모, 하이브리드 검색 중 지금 상황에 맞는 선택지를 강조한다.</p></header>
  <fieldset class="wg-02-grid"><legend class="wg-02-sr">선택 상황</legend><input type="radio" name="compare-wg02-pick" id="compare-wg02-a" class="wg-02-radio" checked><div class="wg-02-card"><div class="wg-02-preview wg-02-preview--a"><div class="wg-02-pv-hero">MVP</div><div class="wg-02-pv-body"><span></span><span></span><span class="wg-02-pv-short"></span></div><div class="wg-02-pv-cta wg-02-pv-cta--a">pgvector</div></div><div class="wg-02-meta"><label for="compare-wg02-a" class="wg-02-pick-label">기존 Postgres 팀</label><p class="wg-02-desc">권한과 운영을 공유하고 빠르게 검증한다.</p><span class="wg-02-badge">선택됨</span></div></div><input type="radio" name="compare-wg02-pick" id="compare-wg02-b" class="wg-02-radio"><div class="wg-02-card"><div class="wg-02-preview wg-02-preview--b"><div class="wg-02-pv-cards"><span></span><span></span><span></span></div><div class="wg-02-pv-cta wg-02-pv-cta--b">Vector DB</div></div><div class="wg-02-meta"><label for="compare-wg02-b" class="wg-02-pick-label">대규모 저지연</label><p class="wg-02-desc">SLO와 데이터 규모가 명확하면 전용 DB를 벤치마크한다.</p><span class="wg-02-badge">선택됨</span></div></div><input type="radio" name="compare-wg02-pick" id="compare-wg02-c" class="wg-02-radio"><div class="wg-02-card"><div class="wg-02-preview wg-02-preview--c"><div class="wg-02-pv-split"><div class="wg-02-pv-aside"></div><div class="wg-02-pv-main"><span></span><span></span></div></div><div class="wg-02-pv-cta wg-02-pv-cta--c">Hybrid</div></div><div class="wg-02-meta"><label for="compare-wg02-c" class="wg-02-pick-label">키워드 중요</label><p class="wg-02-desc">BM25와 벡터를 함께 운영해 설명 가능성을 높인다.</p><span class="wg-02-badge">선택됨</span></div></div></fieldset>
</section>
""")


PAGE_06 = f"""
<main id="main" class="page-wide layout-seo">
<header class="header"><div class="kicker">SEO DASHBOARD</div><h1>AI 회의록 자동화 검색 허브</h1><p class="sub">검색 의도, SERP 문안, 키워드 클러스터, 보안 FAQ, 전환 CTA를 한 화면에서 점검하는 SEO 대시보드다.</p><div class="meta"><span>seo_dashboard</span><span>seo-dashboard.html</span><span>profile auto</span><span>2026-06-05 08:34</span><span>템플릿 쇼케이스 확장</span></div></header>
<section class="summary-card"><div class="label">Overview</div><p><strong>이 키워드는 제품 탐색과 도입 리스크가 섞인 혼합 의도다.</strong> 기능 소개만으로는 부족하고 보안, 동의, 보관 기간, 액션 아이템 누락 방지를 함께 설명해야 한다.</p></section>
<section class="serp-box"><h2>검색 결과 미리보기</h2><p class="serp-url">example.com/ai-meeting-notes-automation-seo</p><p class="serp-title">AI 회의록 자동화: 녹음부터 액션 아이템까지 안전하게 설계하는 방법</p><p>회의 녹음, 요약, 할 일 추출, 보안 검토, 도입 체크리스트까지 AI 회의록 자동화의 전체 흐름을 실무 기준으로 정리합니다.</p></section>
<section class="vt-shell"><div class="vt-frame"><div class="cg-grid"><article class="cg-card"><em>01</em><b>녹음·전사</b><p>회의 내용을 텍스트로 변환한다.</p></article><article class="cg-card"><em>02</em><b>요약</b><p>결정과 보류 항목을 분리한다.</p></article><article class="cg-card"><em>03</em><b>액션 아이템</b><p>담당자와 마감일을 추출한다.</p></article><article class="cg-card"><em>04</em><b>보안</b><p>보관 기간과 민감정보를 통제한다.</p></article><article class="cg-card"><em>05</em><b>검색</b><p>프로젝트별로 다시 찾는다.</p></article><article class="cg-card"><em>06</em><b>자동화</b><p>캘린더와 태스크 도구로 연결한다.</p></article></div></div></section>
<section><h2><span class="no">1</span>검색 의도 클러스터</h2><p class="h2-sub">AI 회의록 자동화는 정보 탐색, 도구 비교, 도입 실무, 운영 개선 의도가 섞인다.</p><div class="grid-2"><article class="mini-card"><h3>정보 탐색</h3><p>AI 회의록 자동화가 무엇인지, 회의 전사와 어떤 차이가 있는지 설명한다.</p></article><article class="mini-card"><h3>도구 비교</h3><p>전사 정확도, 화자 분리, 할 일 추출, 연동 기능을 비교한다.</p></article><article class="mini-card"><h3>도입 실무</h3><p>참석자 동의, 보관 기간, 민감정보 마스킹을 다룬다.</p></article><article class="mini-card"><h3>운영 개선</h3><p>회의 후 액션 아이템 누락과 담당자 미지정을 줄인다.</p></article></div></section>
<section><h2><span class="no">2</span>vt-07 카드 그리드: 콘텐츠 허브 지도</h2><p class="h2-sub">1순위 vt 템플릿인 card-grid를 검색 허브 전체 구조로 사용한다.</p><div class="vt-shell"><div class="vt-frame"><div class="cg-grid"><article class="cg-card"><em>HUB</em><b>개념</b><p>회의록 자동화의 입력·처리·출력을 한 번에 설명한다.</p></article><article class="cg-card"><em>HOW</em><b>워크플로우</b><p>녹음, 전사, 요약, 할 일 추출, 배포 순서.</p></article><article class="cg-card"><em>RISK</em><b>보안</b><p>동의, 보관, 민감정보, 접근 권한.</p></article><article class="cg-card"><em>BUY</em><b>도구 선택</b><p>요구사항 표와 비교 체크리스트.</p></article></div></div></div></section>
<section><h2><span class="no">3</span>검색 결과 문안 세트</h2><p class="h2-sub">제목은 키워드와 문제를 함께 담고, 메타 설명은 기능보다 결과를 먼저 말한다.</p><div class="tbl table-scroll"><table><caption>AI 회의록 자동화 SERP 문안 후보</caption><thead><tr><th>유형</th><th>제목 후보</th><th>메타 설명</th><th>전환</th></tr></thead><tbody><tr><td>가이드</td><td>AI 회의록 자동화 도입 가이드</td><td>녹음부터 액션 아이템까지 안전하게 설계하는 법</td><td>도입 체크리스트</td></tr><tr><td>비교</td><td>AI 회의록 도구 비교 기준</td><td>전사, 요약, 보안, 연동 기준을 실무 관점으로 비교</td><td>요구사항 템플릿</td></tr><tr><td>보안</td><td>AI 회의록 보안 체크리스트</td><td>동의, 보관 기간, 민감정보 마스킹, 접근 권한 점검</td><td>정책 샘플</td></tr></tbody></table></div></section>
<section><h2><span class="no">4</span>키워드 클러스터 보드</h2><p class="h2-sub">키워드를 기능, 도입, 보안, 운영으로 분리해야 같은 글 안에서 의도가 충돌하지 않는다.</p><ul><li>기능형: AI 회의록, 자동 요약, 화자 분리, 액션 아이템 추출</li><li>도입형: 회의록 자동화 도입, 회의 요약 툴 비교, 업무 자동화 회의록</li><li>보안형: 회의 녹음 동의, 회의록 보관 기간, 민감정보 마스킹</li><li>운영형: 회의 후 할 일 관리, 결정사항 추적, 프로젝트 회의 검색</li></ul></section>
<section><h2><span class="no">5</span>wg-11 주간 상태: SEO 운영 대시보드</h2><p class="h2-sub">권장 wg-11을 SEO 콘텐츠 품질 상태판으로 사용한다.</p>{SEO_WG11}</section>
<section><h2><span class="no">6</span>FAQ와 People Also Ask 설계</h2><p class="h2-sub">FAQ에는 기능 질문뿐 아니라 동의와 보관 기간을 반드시 넣는다.</p><div class="grid-2"><article class="mini-card"><h3>AI 회의록은 녹음 동의가 필요한가?</h3><p>조직 정책과 지역 법규에 따라 다르므로, 참석자 고지와 동의 절차를 먼저 설명한다.</p></article><article class="mini-card"><h3>회의록은 어디에 저장되는가?</h3><p>보관 위치, 접근 권한, 삭제 주기, 외부 모델 전송 여부를 분리해 쓴다.</p></article><article class="mini-card"><h3>액션 아이템은 어떻게 검증하는가?</h3><p>담당자, 기한, 원문 근거, 회의 후 확인 루프를 제시한다.</p></article><article class="mini-card"><h3>기존 캘린더와 연결되는가?</h3><p>캘린더, 태스크 도구, 지식관리 도구 연결 기준을 설명한다.</p></article></div></section>
<section><h2><span class="no">7</span>보안·동의 콘텐츠 블록</h2><p class="h2-sub">회의록 자동화 글에서 보안 설명은 부록이 아니라 구매 판단의 핵심 블록이다.</p><ol><li>참석자에게 녹음과 AI 요약 사용을 고지한다.</li><li>민감정보가 포함된 회의는 자동 요약 제외 또는 마스킹 정책을 둔다.</li><li>회의록 보관 기간과 삭제 요청 경로를 문서화한다.</li><li>외부 모델 또는 외부 저장소로 전송되는 범위를 명확히 한다.</li></ol></section>
<section><h2><span class="no">8</span>전환 CTA와 리드 마그넷</h2><p class="h2-sub">검색 허브의 전환은 바로 구매보다 요구사항 정리로 시작하는 편이 자연스럽다.</p><div class="grid-2"><article class="mini-card"><h3>도입 체크리스트</h3><p>동의, 보안, 연동, 운영자 책임을 점검하는 PDF.</p></article><article class="mini-card"><h3>회의록 정책 샘플</h3><p>보관 기간, 삭제 요청, 민감정보 처리 기준.</p></article><article class="mini-card"><h3>도구 비교표</h3><p>전사 정확도, 화자 분리, 태스크 연동, 비용.</p></article><article class="mini-card"><h3>파일럿 계획서</h3><p>2주간 회의 10개로 품질을 검증하는 플랜.</p></article></div></section>
<section><h2><span class="no">9</span>콘텐츠 품질 게이트</h2><p class="h2-sub">SEO 대시보드는 순위보다 먼저 누락된 사용자 질문을 찾는다.</p><div class="tbl table-scroll"><table><caption>SEO 품질 게이트</caption><thead><tr><th>게이트</th><th>통과 기준</th><th>실패 시 조치</th></tr></thead><tbody><tr><td>의도 커버리지</td><td>4개 의도 모두 H2 이상 배치</td><td>섹션 추가</td></tr><tr><td>보안 설명</td><td>동의/보관/삭제/전송 범위 포함</td><td>FAQ 보강</td></tr><tr><td>전환 경로</td><td>체크리스트 또는 비교표 CTA</td><td>리드 마그넷 추가</td></tr></tbody></table></div></section>
<section><h2><span class="no">10</span>업데이트 루프</h2><p class="h2-sub">검색 허브는 한 번 쓰는 글이 아니라 회의 운영 변화에 맞춰 갱신되는 대시보드다.</p><ul><li>검색어 유입 질문을 월 1회 FAQ 후보로 옮긴다.</li><li>도구 비교표는 기능 릴리즈나 가격 정책 변경 시 갱신한다.</li><li>보안 정책 변경은 SERP 설명과 FAQ에 즉시 반영한다.</li><li>회의 후 액션 아이템 누락 사례를 운영 섹션에 추가한다.</li></ul></section>
<section class="try"><div class="label">NEXT ACTION</div><h2>바로 실행할 일</h2><ol><li>제목 후보 3개를 만든다.</li><li>검색 의도 4개를 H2로 배치한다.</li><li>FAQ 12개 중 보안 질문 4개를 포함한다.</li><li>wg-11 상태판으로 콘텐츠 누락을 점검한다.</li></ol></section>
<aside class="source-note"><div class="label">Source Note</div><p>SEO 대시보드 예시이며 실제 검색량과 순위는 확인하지 않았다.</p></aside></main>
"""


PAGE_07 = f"""
<main id="main" class="page-wide layout-platform">
<header class="header"><div class="kicker">PLATFORM BLOG</div><h1>컨퍼런스 발표를 플랫폼별 글로 변환하기</h1><p class="sub">한 번의 발표 자료를 티스토리, 벨로그, 네이버, 워드프레스 글로 나눠 발행하는 플랫폼별 변환 설계다.</p><div class="meta"><span>platform_blog</span><span>platform-adaptation.html</span><span>profile auto</span><span>2026-06-05 08:34</span><span>템플릿 쇼케이스 확장</span></div></header>
<section class="summary-card"><div class="label">Overview</div><p><strong>같은 발표도 플랫폼마다 독자가 기다리는 증거가 다르다.</strong> 복붙이 아니라 플랫폼별 질문, 문단 길이, CTA, 기술 밀도를 다시 설계해야 한다.</p></section>
<section class="vt-shell"><div class="vt-frame"><div class="cg-grid"><article class="cg-card"><em>01</em><b>티스토리</b><p>긴 설명과 목차 중심.</p></article><article class="cg-card"><em>02</em><b>벨로그</b><p>개발자 실험 기록 중심.</p></article><article class="cg-card"><em>03</em><b>네이버</b><p>쉬운 표현과 짧은 문단.</p></article><article class="cg-card"><em>04</em><b>워드프레스</b><p>브랜드 자료실과 CTA.</p></article><article class="cg-card"><em>05</em><b>뉴스레터</b><p>핵심 문장과 다음 행동.</p></article><article class="cg-card"><em>06</em><b>링크드인</b><p>조직 운영 관점의 배운 점.</p></article></div></div></section>
<section><h2><span class="no">1</span>원본 발표 분해</h2><p class="h2-sub">발표 자료는 슬라이드 순서대로 글이 되지 않는다. 주장, 증거, 사례, CTA로 먼저 분해한다.</p><div class="grid-2"><article class="mini-card"><h3>핵심 주장</h3><p>발표의 결론 3개를 뽑는다.</p></article><article class="mini-card"><h3>증거</h3><p>데모, 수치, 실패 사례, 인용 가능한 문장을 분리한다.</p></article><article class="mini-card"><h3>독자 질문</h3><p>플랫폼별 독자가 가장 먼저 물을 질문을 다시 쓴다.</p></article><article class="mini-card"><h3>CTA</h3><p>댓글, 다운로드, 문의, 후속 글 중 하나로 연결한다.</p></article></div></section>
<section><h2><span class="no">2</span>vt-07 카드 그리드: 플랫폼 변환 지도</h2><p class="h2-sub">1순위 vt 템플릿인 card-grid로 플랫폼별 산출물을 한눈에 보이게 한다.</p><div class="vt-shell"><div class="vt-frame"><div class="cg-grid"><article class="cg-card"><em>TS</em><b>티스토리</b><p>목차, 표, FAQ, 검색 키워드.</p></article><article class="cg-card"><em>VL</em><b>벨로그</b><p>코드, 실패 설정, 재현 환경.</p></article><article class="cg-card"><em>NV</em><b>네이버</b><p>쉬운 말, 짧은 문단, 생활형 예시.</p></article><article class="cg-card"><em>WP</em><b>워드프레스</b><p>브랜드 메시지, 자료실, CTA.</p></article></div></div></div></section>
<section><h2><span class="no">3</span>wg-02 디자인 방향: 플랫폼별 발행 톤</h2><p class="h2-sub">권장 wg-02를 플랫폼별 발행 방향 비교 위젯으로 사용한다.</p>{PLATFORM_WG02}</section>
<section><h2><span class="no">4</span>티스토리 변환</h2><p class="h2-sub">티스토리는 검색 유입을 고려해 목차, 표, FAQ, 긴 설명을 앞세운다.</p><ul><li>제목에는 발표 핵심 키워드와 문제를 함께 넣는다.</li><li>서두는 “왜 이 주제가 중요한가”를 설명한다.</li><li>중간에는 비교표와 단계별 체크리스트를 둔다.</li><li>마지막에는 후속 글 또는 자료 다운로드 CTA를 둔다.</li></ul></section>
<section><h2><span class="no">5</span>벨로그 변환</h2><p class="h2-sub">벨로그는 기술적 실패와 재현 가능한 환경을 숨기지 않을 때 신뢰도가 높아진다.</p><ul><li>발표의 추상 주장을 코드와 로그로 바꾼다.</li><li>실패한 설정, 삽질, 재현 조건을 남긴다.</li><li>코드 블록에는 환경 버전과 전제 조건을 붙인다.</li><li>결론보다 “다음에 다르게 할 것”을 강조한다.</li></ul></section>
<section><h2><span class="no">6</span>네이버 변환</h2><p class="h2-sub">네이버용 글은 전문용어보다 생활형 문제와 짧은 문단이 중요하다.</p><p>발표의 기술 용어를 바로 쓰기보다 “회의 후 할 일을 놓치지 않는 방법”, “팀 문서가 빨라지는 이유”처럼 일상적 질문으로 바꾼다. 한 문단은 짧게 유지하고, 사진이나 요약 박스로 흐름을 끊어준다.</p></section>
<section><h2><span class="no">7</span>워드프레스 변환</h2><p class="h2-sub">워드프레스는 브랜드 자료실과 전환 CTA를 품고 있어야 한다.</p><p>발표 자료를 단순 후기보다 고객이 다시 읽을 수 있는 리소스로 정리한다. 다운로드 가능한 발표 요약, 도입 체크리스트, 문의 CTA, 관련 제품 문서 링크를 연결하면 랜딩과 블로그 사이의 역할을 할 수 있다.</p></section>
<section><h2><span class="no">8</span>플랫폼별 운영표</h2><p class="h2-sub">제목, 문단 길이, 증거, CTA를 플랫폼별로 분리한다.</p><div class="tbl table-scroll"><table><caption>플랫폼별 발행 운영표</caption><thead><tr><th>플랫폼</th><th>제목 기준</th><th>본문 증거</th><th>CTA</th></tr></thead><tbody><tr><td>티스토리</td><td>검색 키워드 포함</td><td>표, FAQ, 단계</td><td>체크리스트</td></tr><tr><td>벨로그</td><td>기술 문제 명확화</td><td>코드, 로그, 실패 사례</td><td>GitHub/후속 실험</td></tr><tr><td>네이버</td><td>쉬운 표현</td><td>생활형 예시</td><td>댓글/공유</td></tr><tr><td>워드프레스</td><td>브랜드 메시지</td><td>고객 가치, 자료실</td><td>문의/다운로드</td></tr></tbody></table></div></section>
<section><h2><span class="no">9</span>재사용 가능한 원본 조각</h2><p class="h2-sub">플랫폼마다 글은 달라져도 원본 조각은 공통 자산으로 관리한다.</p><ol><li>핵심 주장 3개</li><li>데모 캡처 4장</li><li>실패 사례 2개</li><li>표 1개와 체크리스트 1개</li><li>발표자 소개와 관련 링크</li></ol></section>
<section><h2><span class="no">10</span>발행 후 검증</h2><p class="h2-sub">복붙 여부가 아니라 플랫폼별 독자 반응 차이를 본다.</p><div class="grid-2"><article class="mini-card"><h3>티스토리</h3><p>검색 유입 키워드와 체류 시간을 본다.</p></article><article class="mini-card"><h3>벨로그</h3><p>댓글의 기술 질문과 코드 재현 요청을 본다.</p></article><article class="mini-card"><h3>네이버</h3><p>공감, 저장, 쉬운 질문을 본다.</p></article><article class="mini-card"><h3>워드프레스</h3><p>다운로드, 문의, 관련 글 이동을 본다.</p></article></div></section>
<section class="try"><div class="label">NEXT ACTION</div><h2>바로 실행할 일</h2><ol><li>발표의 핵심 주장 3개를 뽑는다.</li><li>플랫폼별 독자 질문을 새로 쓴다.</li><li>wg-02 방향 카드로 발행 톤을 고른다.</li><li>공통 표와 체크리스트를 플랫폼별로 변환한다.</li></ol></section>
<aside class="source-note"><div class="label">Source Note</div><p>플랫폼별 일반 발행 전략 예시이며 정책 변경은 별도 확인이 필요하다.</p></aside></main>
"""


PAGE_08 = f"""
<main id="main" class="page-wide layout-audit layout-skill-audit">
<header class="header"><div class="kicker">SKILL AUDIT</div><h1>배포 체크리스트 생성 스킬 감사 리포트</h1><p class="sub">배포 전 체크리스트 생성 스킬을 목적, 트리거, 실패 대응, 품질 게이트, 패치 계획 관점에서 감사한다.</p><div class="meta"><span>skill_audit</span><span>skill-audit-report.html</span><span>profile auto</span><span>2026-06-05 08:34</span><span>템플릿 쇼케이스 확장</span></div></header>
<section class="summary-card"><div class="label">Overview</div><p><strong>체크리스트 생성 스킬의 품질은 항목 수가 아니라 위험 분류 능력이다.</strong> 환경별 차단 조건, 롤백 기준, 담당자 지정이 빠지면 안심용 문서로 변한다.</p></section>
<section class="vt-shell"><div class="vt-frame"><div><div class="qg-grid"><div class="qg-card"><b>목적</b><p class="vt-text">릴리즈 위험을 줄이는 배포 전 확인표를 만든다.</p></div><div class="qg-card"><b>트리거</b><p class="vt-text">배포, 릴리즈, 롤백 요청을 감지한다.</p></div><div class="qg-card warn"><b>실패 대응</b><p class="vt-text">정보 부족 시 확인 필요 항목을 분리한다.</p></div><div class="qg-card block"><b>완료 기준</b><p class="vt-text">차단/경고/정보 등급과 담당자가 있어야 한다.</p></div></div><div class="qg-final">PRE-FLIGHT: 체크리스트는 항목 수가 아니라 차단 조건의 명확성으로 평가한다.</div></div></div></section>
<section><h2><span class="no">1</span>감사 요약</h2><p class="h2-sub">점수는 4.1/5다. 목적과 트리거는 명확하지만 실패 대응과 증빙 요구가 약하다.</p><div class="grid-2"><article class="mini-card"><h3>가장 큰 리스크</h3><p>환경별 차단 조건 없이 일반 문구만 생성될 수 있다.</p></article><article class="mini-card"><h3>우선 패치</h3><p>owner, evidence, done criteria를 필수화한다.</p></article><article class="mini-card"><h3>검증 부족</h3><p>staging/canary/production fixture가 필요하다.</p></article><article class="mini-card"><h3>완료 조건</h3><p>차단, 경고, 정보 등급이 명확해야 한다.</p></article></div></section>
<section><h2><span class="no">2</span>vt-06 품질 게이트</h2><p class="h2-sub">1순위 vt 템플릿인 quality-gate로 감사 결론을 시각화한다.</p><div class="vt-shell"><div class="vt-frame"><div class="qg-grid"><div class="qg-card"><b>PASS</b><p class="vt-text">목적과 트리거가 배포 문맥과 연결된다.</p></div><div class="qg-card warn"><b>WARN</b><p class="vt-text">입력 부족 시 질문이 충분하지 않다.</p></div><div class="qg-card block"><b>BLOCK</b><p class="vt-text">담당자와 증빙 없는 체크 항목은 배포 판단에 쓸 수 없다.</p></div><div class="qg-card warn"><b>NEXT</b><p class="vt-text">예시와 회귀 테스트 fixture를 추가한다.</p></div></div><div class="qg-final">권장 판정: 문서 패치 후 재검증</div></div></div></section>
<section><h2><span class="no">3</span>vt-09 파일 투어</h2><p class="h2-sub">후순위 vt=file-tour를 사용해 개선해야 할 스킬 파일 구조를 보여준다.</p><div class="vt-shell"><div class="vt-frame"><div class="ft"><article class="ft-card"><div class="ft-head"><span>SKILL.md</span><span>core</span></div><div class="ft-body"><p class="vt-text">workflow와 output schema를 고정한다.</p><div class="ft-note">owner/evidence/done criteria 필수화</div></div></article><article class="ft-card"><div class="ft-head"><span>examples/release.md</span><span>fixture</span></div><div class="ft-body"><p class="vt-text">staging/canary/production 예시를 둔다.</p><div class="ft-note">고위험 배포 샘플 포함</div></div></article><article class="ft-card"><div class="ft-head"><span>tests/checklist.md</span><span>gate</span></div><div class="ft-body"><p class="vt-text">필수 필드 누락을 실패 처리한다.</p><div class="ft-note">차단 조건 회귀 방지</div></div></article></div></div></div></section>
<section><h2><span class="no">4</span>wg-03 주석 PR: 패치 리뷰</h2><p class="h2-sub">권장 wg-03으로 스킬 패치의 문제 라인을 실제 리뷰처럼 보여준다.</p>{AUDIT_WG03}</section>
<section><h2><span class="no">5</span>wg-17 PR Writeup: 개선 계획</h2><p class="h2-sub">권장 wg-17로 감사 finding을 패치 계획서로 변환한다.</p>{AUDIT_WG17}</section>
<section><h2><span class="no">6</span>감사 매트릭스</h2><p class="h2-sub">스킬의 섹션별 현재 상태, 위험, 개선안을 고정한다.</p><div class="tbl table-scroll"><table><caption>배포 체크리스트 스킬 감사표</caption><thead><tr><th>섹션</th><th>현재 상태</th><th>위험</th><th>개선안</th></tr></thead><tbody><tr><td>Purpose</td><td>릴리즈 전 확인표 생성</td><td>위험 저감 목적 약함</td><td>차단 조건 중심</td></tr><tr><td>Trigger</td><td>배포 키워드</td><td>롤백 요청 누락</td><td>트리거 확장</td></tr><tr><td>Workflow</td><td>항목 생성 후 출력</td><td>입력 부족 대응 없음</td><td>확인 필요 섹션</td></tr><tr><td>Quality Gate</td><td>체크리스트 포함</td><td>담당자/증빙 누락</td><td>owner/evidence 필수</td></tr></tbody></table></div></section>
<section><h2><span class="no">7</span>입력 부족 대응</h2><p class="h2-sub">스킬은 모르는 값을 채우지 말고 확인 필요 항목으로 분리해야 한다.</p><ol><li>배포 대상 서비스와 환경을 묻는다.</li><li>변경 범위와 되돌릴 수 있는 방법을 묻는다.</li><li>데이터 마이그레이션 여부를 묻는다.</li><li>고객 영향과 커뮤니케이션 필요 여부를 묻는다.</li><li>배포 승인자와 온콜 담당자를 묻는다.</li></ol></section>
<section><h2><span class="no">8</span>출력 스키마</h2><p class="h2-sub">체크리스트 항목은 사람이 바로 실행하고 검증할 수 있는 필드를 가져야 한다.</p><div class="tbl table-scroll"><table><caption>권장 출력 필드</caption><thead><tr><th>필드</th><th>의미</th><th>예시</th></tr></thead><tbody><tr><td>severity</td><td>block/warn/info</td><td>block</td></tr><tr><td>owner</td><td>실행 책임자</td><td>release manager</td></tr><tr><td>evidence</td><td>통과 증빙</td><td>CI 링크, 스크린샷</td></tr><tr><td>done criteria</td><td>완료 기준</td><td>rollback test passed</td></tr></tbody></table></div></section>
<section><h2><span class="no">9</span>회귀 테스트 fixture</h2><p class="h2-sub">좋은 스킬은 예쁜 출력보다 나쁜 입력에서 안전한 출력을 낸다.</p><ul><li>배포 환경 누락 입력</li><li>DB migration 포함 배포</li><li>고객 영향이 있는 배포</li><li>롤백 불가 배포</li><li>보안 설정 변경 배포</li></ul></section>
<section><h2><span class="no">10</span>최종 판정</h2><p class="h2-sub">문서 패치만으로 충분하지만, 완료 기준은 예시와 테스트 fixture까지 포함해야 한다.</p><p>권장 조치는 SKILL.md의 workflow와 output schema를 좁히고, examples와 tests에 고위험 배포 fixture를 추가하는 것이다. 이후 생성물에서 owner, evidence, done criteria가 빠지면 실패하도록 검증해야 한다.</p></section>
<section class="try"><div class="label">NEXT ACTION</div><h2>바로 실행할 일</h2><ol><li>Purpose를 위험 기반 배포 판단으로 좁힌다.</li><li>입력 부족 질문 5개를 추가한다.</li><li>출력 형식을 owner/evidence/done으로 고정한다.</li><li>테스트 fixture를 만든다.</li></ol></section>
<aside class="source-note"><div class="label">Source Note</div><p>가상의 배포 체크리스트 생성 스킬을 감사하는 예시 리포트다.</p></aside></main>
"""


PAGE_09 = f"""
<main id="main" class="page-wide layout-reference">
<header class="header"><div class="kicker">REFERENCE MANUAL</div><h1>Webhook 서명 검증 레퍼런스</h1><p class="sub">Webhook 요청이 실제 발신자에게서 왔고 중간에 변조되지 않았는지 확인하는 보안 레퍼런스다.</p><div class="meta"><span>reference_html</span><span>reference-manual.html</span><span>profile auto</span><span>2026-06-05 08:34</span><span>템플릿 쇼케이스 확장</span></div></header>
<section class="summary-card"><div class="label">Overview</div><p><strong>서명 검증은 비즈니스 로직보다 먼저 실패해야 한다.</strong> 공유 비밀키로 raw body를 HMAC 계산하고 헤더 서명과 constant-time 비교한다.</p></section>
<section class="vt-shell"><div class="vt-frame"><div class="ft"><article class="ft-card"><div class="ft-head"><span>webhook.ts</span><span>entry</span></div><div class="ft-body"><p class="vt-text">HTTP 요청에서 raw body와 headers를 추출한다.</p><div class="ft-note"><b>메모</b><br>body parser가 원문을 바꾸지 않게 한다.</div></div></article><article class="ft-card"><div class="ft-head"><span>signature.ts</span><span>crypto</span></div><div class="ft-body"><p class="vt-text">HMAC-SHA256 expected signature를 만든다.</p><div class="ft-note"><b>메모</b><br>알고리즘과 인코딩을 고정한다.</div></div></article><article class="ft-card"><div class="ft-head"><span>replay-cache.ts</span><span>replay</span></div><div class="ft-body"><p class="vt-text">event id와 timestamp로 재전송을 차단한다.</p><div class="ft-note"><b>메모</b><br>TTL 캐시로 중복 이벤트를 걸러낸다.</div></div></article><article class="ft-card"><div class="ft-head"><span>handler.ts</span><span>business</span></div><div class="ft-body"><p class="vt-text">검증된 이벤트만 도메인 처리로 넘긴다.</p><div class="ft-note"><b>메모</b><br>검증 실패와 처리 실패 로그를 분리한다.</div></div></article></div></div></section>
<section><h2><span class="no">1</span>레퍼런스 개요</h2><p class="h2-sub">검증 로직, replay 차단, 비즈니스 핸들러를 파일 단위로 분리한다.</p><div class="grid-2"><article class="mini-card"><h3>Raw body</h3><p>요청 원문을 그대로 보존한다.</p></article><article class="mini-card"><h3>HMAC</h3><p>정해진 포맷과 secret으로 계산한다.</p></article><article class="mini-card"><h3>Timestamp</h3><p>허용 시간 범위를 둔다.</p></article><article class="mini-card"><h3>Replay cache</h3><p>중복 event id를 짧은 TTL로 막는다.</p></article></div></section>
<section><h2><span class="no">2</span>vt-09 파일 투어</h2><p class="h2-sub">1순위 vt=file-tour로 구현 파일의 책임을 보여준다.</p><div class="vt-shell"><div class="vt-frame"><div class="ft"><article class="ft-card"><div class="ft-head"><span>webhook.ts</span><span>entry</span></div><div class="ft-body"><p class="vt-text">헤더와 raw body를 보존한다.</p><div class="ft-note">검증 전 JSON parse 금지</div></div></article><article class="ft-card"><div class="ft-head"><span>signature.ts</span><span>crypto</span></div><div class="ft-body"><p class="vt-text">HMAC과 constant-time 비교.</p><div class="ft-note">secret 로그 금지</div></div></article><article class="ft-card"><div class="ft-head"><span>replay-cache.ts</span><span>cache</span></div><div class="ft-body"><p class="vt-text">event id와 timestamp를 검사한다.</p><div class="ft-note">TTL 정책 문서화</div></div></article></div></div></div></section>
<section><h2><span class="no">3</span>vt-10 검증 플로우</h2><p class="h2-sub">후순위 vt=flowchart로 요청 처리 순서를 고정한다.</p><div class="vt-shell"><div class="vt-frame"><div class="fc"><div class="fc-node hot">raw body</div><div class="fc-arrow">→</div><div class="fc-node">HMAC</div><div class="fc-arrow">→</div><div class="fc-node hot">compare</div></div><p class="vt-text">비교 통과 후 timestamp와 replay cache를 확인하고, 마지막에 비즈니스 핸들러로 넘긴다.</p></div></div></section>
<section><h2><span class="no">4</span>wg-14 기능 설명</h2><p class="h2-sub">권장 wg-14로 레퍼런스의 핵심 기능을 접이식 설명과 탭 구조로 보여준다.</p>{REF_WG14}</section>
<section><h2><span class="no">5</span>wg-19 정책 토글</h2><p class="h2-sub">권장 wg-19로 서명 검증 정책의 on/off 상태를 시각화한다.</p>{REF_WG19}</section>
<section><h2><span class="no">6</span>wg-20 테스트 케이스 튜너</h2><p class="h2-sub">권장 wg-20으로 서명 검증 케이스별 입력과 기대 결과를 비교한다.</p>{REF_WG20}</section>
<section><h2><span class="no">7</span>오류 처리 매트릭스</h2><p class="h2-sub">오류 상황별 응답과 로그를 분리한다.</p><div class="tbl table-scroll"><table><caption>Webhook 서명 검증 오류 처리</caption><thead><tr><th>상황</th><th>응답</th><th>로그</th><th>재시도</th></tr></thead><tbody><tr><td>서명 누락</td><td>401 invalid signature</td><td>security.warn</td><td>설정 확인</td></tr><tr><td>timestamp 만료</td><td>400 stale request</td><td>security.info</td><td>재전송 차단</td></tr><tr><td>중복 event id</td><td>200 already processed</td><td>event.info</td><td>처리 생략</td></tr><tr><td>처리 실패</td><td>500 processing failed</td><td>app.error</td><td>정책에 따라 재시도</td></tr></tbody></table></div></section>
<section><h2><span class="no">8</span>보안 운영 원칙</h2><p class="h2-sub">secret이나 raw payload를 로그에 남기지 않고 검증 실패와 처리 실패를 다른 레벨로 기록한다.</p><ul><li>raw body 보존 테스트를 만든다.</li><li>constant-time 비교를 사용한다.</li><li>timestamp 허용 범위를 문서화한다.</li><li>중복 이벤트 정책을 정한다.</li><li>secret rotation 기간과 종료일을 기록한다.</li></ul></section>
<section><h2><span class="no">9</span>API 제공자별 차이</h2><p class="h2-sub">실제 제공자마다 헤더 이름, 서명 포맷, timestamp 정책이 다르다.</p><div class="tbl table-scroll"><table><caption>제공자별 확인 항목</caption><thead><tr><th>항목</th><th>확인할 것</th><th>실패 위험</th></tr></thead><tbody><tr><td>헤더 이름</td><td>signature, timestamp, event id</td><td>검증 누락</td></tr><tr><td>서명 입력</td><td>raw body만인지 timestamp 포함인지</td><td>서명 불일치</td></tr><tr><td>인코딩</td><td>hex/base64</td><td>상시 실패</td></tr><tr><td>재전송</td><td>event id 정책</td><td>중복 처리</td></tr></tbody></table></div></section>
<section><h2><span class="no">10</span>검증 체크리스트</h2><p class="h2-sub">레퍼런스 문서는 바로 구현 가능한 체크리스트로 끝나야 한다.</p><ol><li>raw body가 검증 전 변형되지 않는가?</li><li>HMAC 알고리즘과 인코딩이 문서와 일치하는가?</li><li>signature 비교가 constant-time인가?</li><li>timestamp 허용 범위가 있는가?</li><li>event id replay cache가 있는가?</li><li>secret과 payload가 로그에 남지 않는가?</li></ol></section>
<section class="try"><div class="label">NEXT ACTION</div><h2>바로 실행할 일</h2><ol><li>raw body 파이프라인을 확인한다.</li><li>HMAC 유닛 테스트를 만든다.</li><li>replay cache TTL을 정한다.</li><li>실패 로그에서 secret을 제거한다.</li></ol></section>
<aside class="source-note"><div class="label">Source Note</div><p>보안 레퍼런스 예시이며 실제 제공자 서명 포맷은 각 API 문서를 확인해야 한다.</p></aside></main>
"""


PAGE_10 = f"""
<main id="main" class="page-wide layout-compare layout-comparison">
<header class="header"><div class="kicker">COMPARISON MATRIX</div><h1>벡터 검색 선택 기준: 전용 Vector DB vs pgvector vs 검색 엔진</h1><p class="sub">문서 검색과 추천 시스템을 만들 때 어떤 저장소를 고를지 기능, 운영, 비용, 전환 가능성으로 비교한다.</p><div class="meta"><span>comparison_html</span><span>comparison-matrix.html</span><span>profile auto</span><span>2026-06-05 08:34</span><span>템플릿 쇼케이스 확장</span></div></header>
<section class="summary-card"><div class="label">Overview</div><p><strong>벡터 검색 선택은 벤치마크보다 운영 맥락이 먼저다.</strong> 데이터 규모, 필터 조건, 권한, 기존 스택, 장애 대응 방식을 함께 봐야 한다.</p></section>
<section class="vt-shell"><div class="vt-frame"><div class="cmp"><article class="cmp-card"><div class="vt-kicker">선택지</div><h3>전용 Vector DB</h3><ul><li>대규모 ANN과 분산 확장에 강하다</li><li>운영 스택이 하나 더 늘어난다</li><li>권한 모델을 별도로 맞춘다</li></ul></article><article class="cmp-card pick"><div class="vt-kicker">선택지</div><h3>PostgreSQL pgvector</h3><ul><li>기존 DB와 권한을 공유한다</li><li>MVP와 내부 검색에 빠르다</li><li>대규모 저지연은 튜닝 한계가 있다</li></ul></article><article class="cmp-card"><div class="vt-kicker">선택지</div><h3>검색 엔진 하이브리드</h3><ul><li>키워드+벡터 검색에 강하다</li><li>색인과 relevance 운영이 필요하다</li><li>랭킹 설명이 편하다</li></ul></article></div></div></section>
<section><h2><span class="no">1</span>선택 문제 정의</h2><p class="h2-sub">세 후보를 초기 도입, 권한, 확장, 운영 난이도로 비교한다.</p><div class="grid-2"><article class="mini-card"><h3>MVP</h3><p>PostgreSQL 사용 중이면 pgvector로 시작한다.</p></article><article class="mini-card"><h3>성장 단계</h3><p>검색 로그가 쌓이면 하이브리드를 검토한다.</p></article><article class="mini-card"><h3>대규모</h3><p>SLO가 명확하면 전용 DB를 벤치마크한다.</p></article><article class="mini-card"><h3>이전 가능성</h3><p>색인 스키마와 평가 세트를 독립적으로 둔다.</p></article></div></section>
<section><h2><span class="no">2</span>vt-13 비교 카드</h2><p class="h2-sub">1순위 vt=comparison-cards로 세 후보의 선택 맥락을 명확히 보여준다.</p><div class="vt-shell"><div class="vt-frame"><div class="cmp"><article class="cmp-card"><h3>Vector DB</h3><ul><li>대규모 저지연</li><li>분산 색인</li><li>새 운영 도메인</li></ul></article><article class="cmp-card pick"><h3>pgvector</h3><ul><li>MVP 빠름</li><li>권한 공유</li><li>DB 부하 관리 필요</li></ul></article><article class="cmp-card"><h3>Hybrid Search</h3><ul><li>키워드 보강</li><li>랭킹 설명</li><li>색인 운영 필요</li></ul></article></div></div></div></section>
<section><h2><span class="no">3</span>wg-01 세 가지 접근</h2><p class="h2-sub">권장 wg-01을 기술 선택 카드로 변환했다.</p>{COMPARE_WG01}</section>
<section><h2><span class="no">4</span>wg-02 선택 방향</h2><p class="h2-sub">권장 wg-02로 상황별 추천을 선택 카드로 보여준다.</p>{COMPARE_WG02}</section>
<section><h2><span class="no">5</span>vt-02 의사결정 트리</h2><p class="h2-sub">후순위 vt=decision-tree로 선택 질문을 순서화한다.</p><div class="vt-shell"><div class="vt-frame"><div class="vt-demo"><div class="dt-q"><article class="dt-card"><div class="vt-kicker">Q1</div><h3>기존 Postgres 권한을 써야 하는가?</h3><p class="vt-text">그렇다면 pgvector가 첫 후보가 된다.</p></article><div class="dt-arrow"></div><article class="dt-card"><div class="vt-kicker">Q2</div><h3>키워드 검색 품질도 중요한가?</h3><p class="vt-text">그렇다면 하이브리드 검색을 검토한다.</p></article></div><div class="dt-options"><article class="dt-card" style="--c:var(--vt-green)"><b>pgvector</b><p class="vt-text">MVP와 내부 검색.</p></article><article class="dt-card" style="--c:var(--vt-gold)"><b>Hybrid</b><p class="vt-text">키워드와 벡터 결합.</p></article><article class="dt-card" style="--c:var(--vt-red)"><b>Vector DB</b><p class="vt-text">대규모 SLO.</p></article></div></div></div></div></section>
<section><h2><span class="no">6</span>vt-03 리스크 매트릭스</h2><p class="h2-sub">후순위 vt=risk-matrix로 운영 리스크를 시각화한다.</p><div class="vt-shell"><div class="vt-frame"><div class="rm-grid"><div class="rm-cell rm-head">가능성</div><div class="rm-cell rm-head">낮음</div><div class="rm-cell rm-head">중간</div><div class="rm-cell rm-head">높음</div><div class="rm-cell rm-head">영향 큼</div><div class="rm-cell rm-risk med">권한 모델 불일치</div><div class="rm-cell rm-risk high">색인 재생성 지연</div><div class="rm-cell rm-risk high">SLO 미달</div><div class="rm-cell rm-head">영향 중간</div><div class="rm-cell rm-risk low">툴 학습 비용</div><div class="rm-cell rm-risk med">랭킹 튜닝 실패</div><div class="rm-cell rm-risk med">DB 부하 증가</div><div class="rm-cell rm-head">영향 작음</div><div class="rm-cell rm-risk low">메트릭 누락</div><div class="rm-cell rm-risk low">문서 부족</div><div class="rm-cell rm-risk low">운영자 교대</div></div></div></div></section>
<section><h2><span class="no">7</span>상세 선택 매트릭스</h2><p class="h2-sub">선택 기준별로 강점과 부담을 나눈다.</p><div class="tbl table-scroll"><table><caption>벡터 검색 선택 매트릭스</caption><thead><tr><th>기준</th><th>전용 Vector DB</th><th>PostgreSQL pgvector</th><th>검색 엔진 하이브리드</th></tr></thead><tbody><tr><td>초기 도입</td><td>별도 인프라</td><td>기존 DB면 빠름</td><td>검색 스택 있으면 빠름</td></tr><tr><td>권한/필터</td><td>제품별 확인</td><td>기존 권한 활용</td><td>색인 필터 필요</td></tr><tr><td>대규모 확장</td><td>강점</td><td>중간</td><td>강점</td></tr><tr><td>운영 난이도</td><td>새 장애 도메인</td><td>DB 운영과 통합</td><td>랭킹 운영 필요</td></tr></tbody></table></div></section>
<section><h2><span class="no">8</span>평가 데이터셋 설계</h2><p class="h2-sub">처음부터 최종 스택을 고르기보다 평가 질문과 실패 로그를 먼저 만든다.</p><ul><li>문서 수와 예상 벡터 수를 계산한다.</li><li>권한 필터가 검색 조건인지 확인한다.</li><li>키워드 실패와 벡터 실패를 따로 기록한다.</li><li>색인 재생성 시간을 측정한다.</li><li>질문 100개와 기대 문서 세트를 만든다.</li></ul></section>
<section><h2><span class="no">9</span>이전 가능성 확보</h2><p class="h2-sub">검색 저장소는 바뀔 수 있으므로 색인 스키마와 평가 세트를 독립적으로 둔다.</p><ol><li>문서 ID와 chunk ID를 저장소와 분리한다.</li><li>embedding model 버전을 메타데이터로 남긴다.</li><li>검색 로그를 공통 포맷으로 저장한다.</li><li>권한 필터와 랭킹 규칙을 별도 레이어로 둔다.</li></ol></section>
<section><h2><span class="no">10</span>권장 결론</h2><p class="h2-sub">MVP는 pgvector, 키워드가 중요하면 하이브리드, 대규모 SLO가 명확하면 전용 DB를 검증한다.</p><p>가장 보수적인 선택은 현재 운영 중인 스택에서 평가 세트를 만들고, 검색 실패 로그가 쌓인 뒤 이전하는 것이다. 선택은 제품명이 아니라 실패 모드와 운영자 역량을 기준으로 해야 한다.</p></section>
<section class="try"><div class="label">NEXT ACTION</div><h2>바로 실행할 일</h2><ol><li>현재 규모를 수치화한다.</li><li>MVP 스택을 하나 고른다.</li><li>검색 실패 로그를 남긴다.</li><li>3개월 뒤 재평가한다.</li></ol></section>
<aside class="source-note"><div class="label">Source Note</div><p>기술 선택 기준 예시이며 특정 제품의 최신 성능이나 가격은 확인하지 않았다.</p></aside></main>
"""


def main() -> None:
    pages = {
        "06-ai-meeting-notes-automation-seo.html": PAGE_06,
        "07-conference-talk-platform-adaptation.html": PAGE_07,
        "08-release-checklist-skill-audit.html": PAGE_08,
        "09-webhook-signature-verification-reference.html": PAGE_09,
        "10-vector-db-pgvector-search-engine-comparison.html": PAGE_10,
    }
    for filename, html in pages.items():
        replace_main(filename, html)
        print(f"updated {filename}")


if __name__ == "__main__":
    main()
