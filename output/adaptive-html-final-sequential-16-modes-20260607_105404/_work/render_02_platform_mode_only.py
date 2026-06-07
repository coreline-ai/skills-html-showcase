#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
SKILL = REPO / 'skills/adaptive-html-final'
ASSETS = SKILL / 'assets'
OUT = ROOT / 'pages/02_platform_blog_ai_code_review_gateway.html'

MODE_MATERIALS = [
    SKILL / 'SKILL.md',
    SKILL / 'recipes/platform.prompt.md',
    ASSETS / 'layouts/platform-adaptation.html',
    SKILL / 'references/layout-system.md',
    SKILL / 'references/platform-system.md',
    SKILL / 'references/body-icon-system.md',
    SKILL / 'references/visual-html-system.md',
    SKILL / 'references/widget-system.md',
    ASSETS / 'visual-html-templates/07-card-grid.html',
    ASSETS / 'visual-html-templates/13-comparison-cards.html',
    ASSETS / 'visual-html-templates/17-pr-writeup.html',
    ASSETS / 'widget-templates/02-visual-design-directions.html',
]
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
def h2(num: int, title: str, icon_id: str = 'platform') -> str:
    return f'<h2>{icon(icon_id)}<span class="num">{num}</span>{title}</h2>'

generated = '''<div class="generated-row"><p class="generated-date">Generated · 2026-06-07 KST</p><div class="lens-strip" aria-label="적용 렌즈"><span class="lens-strip-label">LENS</span><span class="lens-chip">mode 02</span><span class="lens-chip">platform split</span><span class="lens-chip">same facts</span><span class="lens-chip">no reuse</span><span class="lens-chip">capture QA</span></div></div>'''

original_summary = f'''
{h2(1, '원문 보존: AI 코드리뷰 게이트웨이의 고정 사실', 'source')}
<p class="h2-sub">플랫폼별 문체를 바꾸더라도 사실은 바꾸지 않는다. 이 글의 원재료는 “AI 코드리뷰를 팀 운영 게이트로 쓰는 방법”이다.</p>
<div class="grid-3">
  <article class="score-card"><h3>고정 문제</h3><p>AI 리뷰가 개인 생산성 도구에 머물면 팀의 승인·보류·재검토 기준이 흩어진다. 운영기는 이 기준을 문서화해야 한다.</p></article>
  <article class="score-card"><h3>고정 해결</h3><p>Pull Request 앞단에 리뷰 게이트를 두고, 심각도·근거·소유자·다음 행동을 하나의 체크로 묶는다.</p></article>
  <article class="score-card"><h3>고정 금지</h3><p>플랫폼별 변환 과정에서 성능 수치, 도입 성공률, 최신 기능을 새로 꾸며 넣지 않는다.</p></article>
</div>
<section class="vt-shell" aria-label="원문 핵심 카드 그리드"><div class="vt-frame"><div class="cg-grid">
  <article class="cg-card"><span class="vt-kicker">01</span><h3>문제</h3><p class="vt-text">리뷰 기준이 사람마다 달라 merge 판단이 늦어진다.</p></article>
  <article class="cg-card"><span class="vt-kicker">02</span><h3>장치</h3><p class="vt-text">AI 리뷰를 권고가 아니라 “검토 게이트”로 위치시킨다.</p></article>
  <article class="cg-card"><span class="vt-kicker">03</span><h3>증거</h3><p class="vt-text">diff, 테스트 실패, 보안 경고, 소유자 응답을 함께 남긴다.</p></article>
  <article class="cg-card"><span class="vt-kicker">04</span><h3>결과</h3><p class="vt-text">merge 가능/보류/수정 요청이 같은 언어로 정리된다.</p></article>
</div></div></section>
'''

platform_strategy = f'''
{h2(2, '변환 전략: 같은 사실, 다른 그릇', 'edit')}
<p class="h2-sub">플랫폼별 발행은 내용을 새로 쓰는 일이 아니라, 독자가 들어오는 입구와 읽는 순서를 바꾸는 일이다.</p>
<div class="platform-split">
  <article class="platform-anchor"><span class="platform-kicker">ANCHOR</span><h3>한 문장 약속</h3><p>“AI 코드리뷰를 개인 도구가 아니라 팀 merge gate로 운영하는 방법.” 모든 플랫폼의 제목과 구조는 이 약속을 벗어나지 않는다.</p></article>
  <div>
    <div class="platform-route-grid">
      <article class="platform-route-card is-search"><div><span class="platform-kicker">Search</span><h3>검색형 접근</h3><p>문제 키워드와 결과 약속을 제목 앞에 둔다.</p></div></article>
      <article class="platform-route-card is-dev"><div><span class="platform-kicker">Dev</span><h3>구현형 접근</h3><p>PR 게이트, diff, 테스트, 정책 파일을 먼저 보여준다.</p></div></article>
      <article class="platform-route-card is-story"><div><span class="platform-kicker">Story</span><h3>경험형 접근</h3><p>리뷰 지연, 재검토, merge 대기 시간을 사례로 시작한다.</p></div></article>
      <article class="platform-route-card is-essay"><div><span class="platform-kicker">Asset</span><h3>자산형 접근</h3><p>체크리스트와 템플릿을 저장 가능한 형태로 제공한다.</p></div></article>
    </div>
    <article class="platform-analogy"><h3>비유</h3><p>같은 재료를 도시락·코스요리·간편식으로 포장하는 차이다. 사실은 그대로 두고 먹는 순서만 바꾼다.</p></article>
  </div>
</div>
<section class="wg-02-dir" aria-labelledby="m02-wg02-title">
  <header class="wg-02-head"><p class="wg-02-kicker">Platform Directions</p><h2 id="m02-wg02-title" class="wg-02-h">같은 글의 3가지 발행 렌더 비교</h2><p class="wg-02-lead">검색형, 개발자형, 경험형 중 첫 화면에서 어떤 약속을 보여줄지 선택한다. 라디오 선택은 CSS-only다.</p></header>
  <fieldset class="wg-02-grid"><legend class="wg-02-sr">발행 렌더 선택</legend>
    <input class="wg-02-radio" type="radio" name="m02-dir" id="m02-dir-a" checked><article class="wg-02-card"><div class="wg-02-preview wg-02-preview--a"><div class="wg-02-pv-bar"><span class="wg-02-pv-dot"></span><span class="wg-02-pv-line"></span></div><div class="wg-02-pv-hero">검색형</div><div class="wg-02-pv-body"><span></span><span class="wg-02-pv-short"></span></div><span class="wg-02-pv-cta wg-02-pv-cta--a">읽기</span></div><div class="wg-02-meta"><label class="wg-02-pick-label" for="m02-dir-a">Tistory · Naver</label><p class="wg-02-desc">문제 키워드와 결과 약속을 첫 문장에 둔다.</p><span class="wg-02-badge">PICK</span></div></article>
    <input class="wg-02-radio" type="radio" name="m02-dir" id="m02-dir-b"><article class="wg-02-card"><div class="wg-02-preview wg-02-preview--b"><div class="wg-02-pv-cards"><span></span><span></span><span></span></div><span class="wg-02-pv-cta wg-02-pv-cta--b">코드 보기</span></div><div class="wg-02-meta"><label class="wg-02-pick-label" for="m02-dir-b">Velog · GitHub Pages</label><p class="wg-02-desc">정책 파일, PR diff, 체크리스트를 먼저 둔다.</p><span class="wg-02-badge">DEV</span></div></article>
    <input class="wg-02-radio" type="radio" name="m02-dir" id="m02-dir-c"><article class="wg-02-card"><div class="wg-02-preview wg-02-preview--c"><div class="wg-02-pv-split"><span class="wg-02-pv-aside"></span><div class="wg-02-pv-main"><span></span><span></span><span></span></div></div><span class="wg-02-pv-cta wg-02-pv-cta--c">사례 읽기</span></div><div class="wg-02-meta"><label class="wg-02-pick-label" for="m02-dir-c">Naver · 브런치형</label><p class="wg-02-desc">리뷰 지연 사례와 팀 운영 맥락을 먼저 보여준다.</p><span class="wg-02-badge">STORY</span></div></article>
  </fieldset>
  <p class="wg-02-foot">권장 기본값은 검색형이다. 단, 개발자 커뮤니티에는 코드와 실패 케이스를 더 앞에 배치한다.</p>
</section>
'''

platform_cards = '''
<article class="platform-output-card is-search"><span class="platform-kicker">Tistory</span><h3>검색 유입형: 도입 기준을 먼저 답한다</h3><p class="platform-prompt-box">제목 후보: “AI 코드리뷰 게이트웨이 운영 기준 5가지”</p><ul><li>첫 H2는 “왜 리뷰 게이트가 필요한가?”로 시작한다.</li><li>중간에는 체크리스트와 FAQ를 둔다.</li><li>태그는 AI코드리뷰, PR리뷰, 개발팀운영 중심.</li></ul><div class="platform-tags"><span>검색형</span><span>FAQ</span><span>체크리스트</span></div></article>
<article class="platform-output-card is-dev"><span class="platform-kicker">Velog</span><h3>개발자 구현형: 정책 코드와 diff를 먼저 공개한다</h3><p class="platform-prompt-box">제목 후보: “PR merge 전에 AI review gate 붙이기”</p><ul><li>정책 YAML, diff, 실패 케이스 순서로 쓴다.</li><li>코드블럭과 체크리스트를 적극 사용한다.</li><li>태그는 code-review, github-actions, llm-review 중심.</li></ul><div class="platform-tags"><span>코드</span><span>정책</span><span>재현</span></div></article>
<article class="platform-output-card is-story"><span class="platform-kicker">Naver Blog</span><h3>경험 서사형: 팀의 갈등을 낮추는 소재로 쓴다</h3><p class="platform-prompt-box">제목 후보: “AI 코드리뷰를 팀에 도입하면서 가장 먼저 정한 약속”</p><ul><li>리뷰 지연 경험과 적용 전후 장면을 짧게 제시한다.</li><li>이미지는 회의 장면, PR 화면, 체크리스트 위치를 제안한다.</li><li>문단은 짧게 나누고 반복 검색어를 자연스럽게 둔다.</li></ul><div class="platform-tags"><span>경험담</span><span>팀운영</span></div></article>
<article class="platform-output-card is-essay"><span class="platform-kicker">WordPress / GitHub Pages</span><h3>자산 보존형: schema와 내부 링크를 설계한다</h3><p class="platform-prompt-box">slug: /ai-code-review-gateway-operating-model</p><ul><li>canonical, meta description, JSON-LD 자리를 둔다.</li><li>운영 템플릿, 체크리스트, 감사 리포트로 내부 링크를 연결한다.</li><li>문서 마지막에 다운로드 가능한 정책 예시를 둔다.</li></ul><div class="platform-tags"><span>schema</span><span>canonical</span><span>evergreen</span></div></article>
<article class="platform-guard" style="grid-column:1/-1"><span class="platform-kicker">Guardrail</span><h3>플랫폼만 바꾸고 사실은 바꾸지 않는다</h3><p>확인되지 않은 성능 수치, 최신 모델명, 특정 도구의 보안 우월성은 플랫폼별 변환 과정에서도 새로 추가하지 않는다.</p></article>
'''
comparison = f'''
{h2(3, '플랫폼별 변환 비교와 선택 기준', 'compare')}
<p class="h2-sub">독자의 진입 의도에 따라 제목·첫 화면·근거 배치가 달라진다. 4열 비교는 모바일 안전을 위해 카드형 표로 전환한다.</p>
<section class="vt-shell" aria-label="플랫폼 비교 카드"><div class="vt-frame"><div class="cmp">
  <article class="cmp-card pick"><span class="vt-kicker">Tistory</span><h3>검색 해결</h3><p class="vt-text">문제 키워드와 답을 앞에 두고 FAQ로 마무리한다.</p></article>
  <article class="cmp-card"><span class="vt-kicker">Velog</span><h3>구현 기록</h3><p class="vt-text">코드, 정책, 실패 케이스, 체크리스트 순서로 쓴다.</p></article>
  <article class="cmp-card"><span class="vt-kicker">Naver</span><h3>경험 서사</h3><p class="vt-text">도입 배경과 팀의 대화 장면을 짧은 문단으로 나눈다.</p></article>
</div></div></section>
<div class="mobile-card-table table-scroll"><table class="mobile-card-table">
  <caption>AI 코드리뷰 게이트웨이 발행 플랫폼별 변환 선택 기준</caption>
  <thead><tr><th>플랫폼</th><th>첫 화면 약속</th><th>필수 증거</th><th>최적 CTA</th></tr></thead>
  <tbody>
    <tr><th>Tistory</th><td data-label="첫 화면 약속">도입 전 판단 기준</td><td data-label="필수 증거">목차, 체크리스트, FAQ</td><td data-label="최적 CTA">우리 팀 기준표 복사</td></tr>
    <tr><th>Velog</th><td data-label="첫 화면 약속">구현 가능한 운영 룰</td><td data-label="필수 증거">정책 파일, PR diff, 실패 예시</td><td data-label="최적 CTA">코드 템플릿 저장</td></tr>
    <tr><th>Naver</th><td data-label="첫 화면 약속">팀 갈등을 줄인 약속</td><td data-label="필수 증거">before/after, 짧은 사례</td><td data-label="최적 CTA">도입 전 질문 목록</td></tr>
    <tr><th>WordPress</th><td data-label="첫 화면 약속">장기 참조 가능한 운영 모델</td><td data-label="필수 증거">schema, meta, 내부 링크</td><td data-label="최적 CTA">정책 문서 다운로드</td></tr>
  </tbody>
</table></div>
<section class="vt-shell" aria-label="변환 PR 요약"><div class="vt-frame"><div class="pr-box"><div class="pr-diff"><p class="pr-del">- 플랫폼마다 새 사실과 과장된 수치를 추가</p><p class="pr-add">+ 같은 사실을 유지하고 제목·입구·근거 순서만 변경</p><p class="pr-add">+ 확인되지 않은 성능 주장은 guardrail로 차단</p></div><div class="pr-walk"><article class="pr-file"><b>tistory.md</b><span>검색형 H2와 FAQ 추가</span></article><article class="pr-file"><b>velog.md</b><span>정책 YAML과 diff 먼저 배치</span></article><article class="pr-file"><b>wordpress.html</b><span>meta/schema 설계 자리 추가</span></article></div></div></div></section>
'''

publish = f'''
{h2(4, '발행 전 체크리스트', 'check')}
<p class="h2-sub">플랫폼별 문법을 바꾼 뒤에도 사실, 링크, 근거, 검색 의도가 같은지 마지막으로 확인한다.</p>
<div class="grid-2"><article class="summary-card"><h3>사실 고정</h3><ul><li>본문 근거와 수치가 원문에서 벗어나지 않았는가.</li><li>새로운 최신성·성능 주장을 추가하지 않았는가.</li><li>각 플랫폼의 제목이 같은 약속을 유지하는가.</li></ul></article><article class="summary-card"><h3>발행 품질</h3><ul><li>모바일 390px에서 표와 카드가 넘치지 않는가.</li><li>제목, slug, meta, 태그가 충돌하지 않는가.</li><li>독자가 다음에 할 행동이 한 문장으로 보이는가.</li></ul></article></div>
<div class="summary-card"><p class="label">PUBLISH / PLATFORM-ADAPTATION</p><pre class="code"><code>facts.lock = 원문 문제·해결·금지 주장 고정
platform.routes = search | dev | story | asset
publishing.gate = mobile_safe + no_new_claims + clear_cta</code></pre></div>
'''

source_note = '<p class="label">작성 기준</p><p>mode 02 platform_blog 전용 레이아웃, platform-adaptation 레시피, platform-system 참조, vt card-grid/comparison-cards/pr-writeup, wg-02 Visual Design Directions를 사용했다. 기존 출력 HTML 본문은 렌더 입력으로 사용하지 않았다.</p>'

layout = (ASSETS / 'layouts/platform-adaptation.html').read_text(encoding='utf-8')
layout = layout.replace('class="original-summary"', 'class="original-summary summary-card"')
layout = layout.replace('class="platform-strategy"', 'class="platform-strategy summary-card"')
layout = layout.replace('class="platform-comparison-table"', 'class="platform-comparison-table summary-card"')
body = layout
repl = {
    'KICKER': '<span class="kicker-text">MODE 02 · PLATFORM BLOG · CAPTURE REVIEW</span>',
    'TITLE': 'AI 코드리뷰 게이트웨이 운영기 플랫폼별 발행 전략',
    'SUBTITLE': '같은 원문을 티스토리·벨로그·네이버·WordPress/GitHub Pages에 맞춰 변환하되, 사실과 근거는 고정하는 플랫폼 발행 설계.',
    'META': '<span>profile auto</span><span>layout platform-adaptation</span><span>same facts</span><span>mode 02 only</span><span>no behavioral JS</span>' + generated,
    'ORIGINAL_SUMMARY': original_summary,
    'PLATFORM_STRATEGY': platform_strategy,
    'PLATFORM_CARDS': platform_cards,
    'COMPARISON_TABLE': comparison,
    'PUBLISH_CHECKLIST': publish,
    'SOURCE_NOTE': source_note,
}
for k,v in repl.items():
    body=body.replace('{{'+k+'}}',v)
base=(ASSETS/'base.html').read_text(encoding='utf-8')
html=base
head={
    'TITLE':'AI 코드리뷰 게이트웨이 운영기 플랫폼별 발행 전략',
    'DESCRIPTION':'platform_blog 모드로 AI 코드리뷰 게이트웨이 운영기를 티스토리, 벨로그, 네이버, WordPress/GitHub Pages에 맞게 변환한 한국어 HTML 발행 전략.',
    'JSON_LD_BLOCK':'',
    'BODY':body,
    'FOOTER':'',
}
for k,v in {**css_slots,**head}.items():
    html=html.replace('{{'+k+'}}',v)
if '{{' in html:
    raise SystemExit('unresolved placeholder')
OUT.write_text(html,encoding='utf-8')

evidence={
    'mode':'02_platform_blog',
    'file':str(OUT.relative_to(ROOT)),
    'link':'http://localhost:8080/output/adaptive-html-final-sequential-16-modes-20260607_105404/pages/02_platform_blog_ai_code_review_gateway.html',
    'policy':'previous HTML body not reused by render script; common generator not used; platform_blog layout/recipe/references/templates consulted for this page only',
    'materials_sha256':MATERIAL_HASH,
    'used_materials':[str(p.relative_to(REPO)) for p in MODE_MATERIALS],
    'visual_contract':{
        'direct_sections_use_view_surface':True,
        'numbered_h2_order':'body-icon body-icon--sm -> num -> title',
        'platform_grid_is_div_not_section':True,
        'premium_platform_classes_used':['platform-split','platform-anchor','platform-route-grid','platform-grid','platform-output-card','platform-guard'],
        'vt_required':['card-grid'],
        'vt_used':['card-grid','comparison-cards','pr-writeup'],
        'wg_used':['02-visual-design-directions'],
        'table_mobile_safe':'mobile-card-table'
    },
    'next_mode':'03_seo_dashboard'
}
(ROOT/'sources/02_platform_blog-visual-contract-evidence.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(OUT)
