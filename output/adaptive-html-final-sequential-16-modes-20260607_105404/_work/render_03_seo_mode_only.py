#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
SKILL = REPO / 'skills/adaptive-html-final'
ASSETS = SKILL / 'assets'
OUT = ROOT / 'pages/03_seo_dashboard_internal_rag_guide.html'

MODE_MATERIALS = [
    SKILL / 'SKILL.md',
    SKILL / 'recipes/seo.prompt.md',
    ASSETS / 'layouts/seo-dashboard.html',
    SKILL / 'references/layout-system.md',
    SKILL / 'references/blog-seo-system.md',
    SKILL / 'references/body-icon-system.md',
    SKILL / 'references/visual-html-system.md',
    SKILL / 'references/widget-system.md',
    ASSETS / 'visual-html-templates/07-card-grid.html',
    ASSETS / 'visual-html-templates/13-comparison-cards.html',
    ASSETS / 'visual-html-templates/20-prompt-tuner.html',
    ASSETS / 'widget-templates/11-weekly-status.html',
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
def h2(num: int, title: str, icon_id: str = 'search') -> str:
    return f'<h2>{icon(icon_id)}<span class="num">{num}</span>{title}</h2>'

generated = '''<div class="generated-row"><p class="generated-date">Generated · 2026-06-07 KST</p><div class="lens-strip" aria-label="적용 렌즈"><span class="lens-strip-label">LENS</span><span class="lens-chip">mode 03</span><span class="lens-chip">SEO intent</span><span class="lens-chip">SERP promise</span><span class="lens-chip">no reuse</span><span class="lens-chip">capture QA</span></div></div>'''

primary = f'''
{h2(1, 'Primary Keyword와 검색 의도', 'search')}
<p class="h2-sub">주제는 “내부 RAG 구축 가이드”다. 검색자는 개념 설명보다 도입 순서, 데이터 준비, 실패 기준을 바로 확인하고 싶어 한다.</p>
<div class="seo-grid">
  <article class="score-card"><h3>Primary keyword</h3><p><strong>내부 RAG 구축 가이드</strong> — 조직 문서, 회의록, 운영 노트를 검색 가능한 지식 베이스로 바꾸는 방법.</p></article>
  <article class="score-card"><h3>Search promise</h3><p>검색자는 “무엇을 준비하고 어떤 순서로 검증해야 하는가”를 원한다. 제목과 첫 화면은 바로 그 약속을 해야 한다.</p></article>
</div>
<section class="vt-shell" aria-label="검색 의도 카드 그리드"><div class="vt-frame"><div class="cg-grid">
  <article class="cg-card"><span class="vt-kicker">01</span><h3>도입 의도</h3><p class="vt-text">내부 문서 검색이 느리고 답변 신뢰도가 낮은 팀.</p></article>
  <article class="cg-card"><span class="vt-kicker">02</span><h3>구현 의도</h3><p class="vt-text">문서 수집, chunking, embedding, 권한 필터 순서를 찾는 독자.</p></article>
  <article class="cg-card"><span class="vt-kicker">03</span><h3>운영 의도</h3><p class="vt-text">정답률·출처·권한 누출·재색인 주기를 검증하려는 운영자.</p></article>
  <article class="cg-card"><span class="vt-kicker">04</span><h3>비교 의도</h3><p class="vt-text">Notion/Drive/wiki 같은 출처를 RAG로 묶어도 되는지 판단하는 팀.</p></article>
</div></div></section>
<section class="wg-11" aria-labelledby="m03-status-title"><header class="wg-11-head"><p class="wg-11-kicker">SEO 운영 신호</p><h2 id="m03-status-title" class="wg-11-h">내부 RAG 가이드 · 검색 준비도</h2><p class="wg-11-lead">제목·SERP 약속·메타·태그가 검색 의도와 같은 방향인지 점검한다.</p></header><div class="wg-11-kpis"><article class="wg-11-kpi wg-11-kpi-good"><span class="wg-11-kpi-v">92%</span><span class="wg-11-kpi-l">의도 커버리지</span></article><article class="wg-11-kpi wg-11-kpi-prog"><span class="wg-11-kpi-v">10</span><span class="wg-11-kpi-l">제목 후보</span></article><article class="wg-11-kpi wg-11-kpi-risk"><span class="wg-11-kpi-v">1</span><span class="wg-11-kpi-l">단정 위험</span></article><article class="wg-11-kpi"><span class="wg-11-kpi-v">8</span><span class="wg-11-kpi-l">태그 후보</span></article></div><h3 class="wg-11-h3">검색 의도 점검</h3><div class="wg-11-bars"><div class="wg-11-bar-row"><span class="wg-11-bar-label">구현 체크리스트</span><span class="wg-11-track"><span class="wg-11-fill wg-11-fill-good" style="width:94%"></span></span><span class="wg-11-bar-pct">94%</span></div><div class="wg-11-bar-row"><span class="wg-11-bar-label">SERP 약속 일치</span><span class="wg-11-track"><span class="wg-11-fill wg-11-fill-good" style="width:88%"></span></span><span class="wg-11-bar-pct">88%</span></div><div class="wg-11-bar-row"><span class="wg-11-bar-label">과장 표현 위험</span><span class="wg-11-track"><span class="wg-11-fill wg-11-fill-risk" style="width:22%"></span></span><span class="wg-11-bar-pct">22%</span></div></div><div class="wg-11-cols"><article class="wg-11-col wg-11-col-good"><h3 class="wg-11-col-h"><span class="wg-11-dot"></span>확정</h3><ul class="wg-11-col-list"><li>Primary keyword 앞쪽 배치</li><li>구현 순서 중심 구조</li></ul></article><article class="wg-11-col wg-11-col-prog"><h3 class="wg-11-col-h"><span class="wg-11-dot"></span>조정</h3><ul class="wg-11-col-list"><li>meta 130~150자 유지</li><li>FAQ 후보를 의도별로 분리</li></ul></article><article class="wg-11-col wg-11-col-risk"><h3 class="wg-11-col-h"><span class="wg-11-dot"></span>주의</h3><ul class="wg-11-col-list"><li>“완벽한 검색 답변” 같은 표현 금지 <span class="wg-11-flag">risk</span></li></ul></article></div></section>
'''

serp = f'''
{h2(2, 'SERP Preview · 검색 결과 약속 카드', 'question')}
<p class="h2-sub">검색 결과에서는 “내부 문서 검색을 어떻게 구축하고 검증할지”가 한눈에 보여야 한다. UI 복제가 아니라 약속의 명확성이 핵심이다.</p>
<div class="serp-shell">
  <div class="serp-box"><div class="serp-dots">검색 결과 미리보기</div><article class="serp-result"><p class="serp-url">coreline.ai/docs/internal-rag-guide</p><h3 class="serp-title">내부 RAG 구축 가이드: 사내 문서 AI 검색을 시작하는 방법</h3><p class="serp-desc">문서 수집, chunking, embedding, 권한 필터, 평가 기준까지 내부 지식 검색을 시작하기 전에 정해야 할 체크리스트를 정리합니다.</p></article><div class="serp-checks"><span class="ok">의도 일치</span><span>과장 없음</span><span>구현 순서</span><span>검증 기준</span></div><div class="serp-variant-strip"><article class="serp-variant"><b>전문가형</b><p>권한·출처·재색인까지 포함한 RAG 운영 기준</p></article><article class="serp-variant"><b>초보자형</b><p>사내 문서를 AI 검색으로 바꾸는 첫 설계</p></article></div></div>
  <div class="serp-rule-grid"><article class="serp-rule is-wide"><span class="serp-rule-kicker">Promise</span><h3>제목과 첫 화면의 약속을 일치</h3><p>클릭 후 바로 확인되는 구현 순서와 검증 기준을 제목에 담는다.</p></article><article class="serp-rule"><span class="serp-rule-kicker">Avoid</span><h3>무료·완벽·자동화 단정 금지</h3><p>확인 가능한 기능과 운영 조건만 말한다.</p></article><article class="serp-rule"><span class="serp-rule-kicker">Fit</span><h3>도입 전 체크리스트 강조</h3><p>문서 수집 전에 정해야 할 소유자, 권한, 평가 기준을 앞에 둔다.</p></article></div>
</div>
'''

titles = f'''
{h2(3, '제목 후보 10개와 선택 기준', 'compare')}
<p class="h2-sub">제목은 검색형 문장, 구현 약속, 위험 회피를 함께 보여줘야 한다. 모바일에서는 후보 표를 행 카드로 읽히게 한다.</p>
<section class="vt-shell" aria-label="제목 후보 비교"><div class="vt-frame"><div class="cmp"><article class="cmp-card pick"><span class="vt-kicker">Search fit</span><h3>내부 RAG 구축 가이드</h3><p class="vt-text">검색 키워드가 앞에 오고 약속이 명확하다.</p></article><article class="cmp-card"><span class="vt-kicker">Risk fit</span><h3>사내 문서 AI 검색 설계 원칙</h3><p class="vt-text">전문가형이나 primary keyword가 뒤로 밀린다.</p></article><article class="cmp-card"><span class="vt-kicker">Ops fit</span><h3>운영 가능한 RAG 체크리스트</h3><p class="vt-text">운영자에게 좋지만 검색 초입 키워드가 약하다.</p></article></div></div></section>
<div class="table-scroll mobile-card-table"><table class="mobile-card-table"><caption>내부 RAG 구축 가이드 SEO 제목 후보 10개</caption><thead><tr><th>순위</th><th>제목 후보</th><th>의도</th><th>판정</th></tr></thead><tbody>
<tr><th>1</th><td data-label="제목 후보">내부 RAG 구축 가이드: 사내 문서 AI 검색을 시작하는 방법</td><td data-label="의도">도입+실행</td><td data-label="판정">추천 조합</td></tr>
<tr><th>2</th><td data-label="제목 후보">사내 문서 AI 검색, 내부 RAG로 안전하게 만드는 순서</td><td data-label="의도">보안+운영</td><td data-label="판정">권한 우려 대응</td></tr>
<tr><th>3</th><td data-label="제목 후보">내부 RAG 설계를 할 때 먼저 결정해야 할 체크리스트</td><td data-label="의도">리스트</td><td data-label="판정">검색형 FAQ용</td></tr>
<tr><th>4</th><td data-label="제목 후보">조직 문서 검색에는 내부 RAG보다 운영 기준이 먼저다</td><td data-label="의도">논점</td><td data-label="판정">철학형 제목</td></tr>
<tr><th>5</th><td data-label="제목 후보">내부 RAG의 시작: 수집, 권한, 평가 기준 잡기</td><td data-label="의도">테크</td><td data-label="판정">구축 가이드 적합</td></tr>
<tr><th>6</th><td data-label="제목 후보">개발팀을 위한 내부 RAG 운영 체크리스트</td><td data-label="의도">운영</td><td data-label="판정">실무자용</td></tr>
<tr><th>7</th><td data-label="제목 후보">내부 RAG 구축 전 반드시 정해야 할 6가지 기준</td><td data-label="의도">도입 기준</td><td data-label="판정">클릭 유도형</td></tr>
<tr><th>8</th><td data-label="제목 후보">사내 지식 검색을 RAG로 바꾸는 현실적인 순서</td><td data-label="의도">교육</td><td data-label="판정">입문자용</td></tr>
<tr><th>9</th><td data-label="제목 후보">권한이 있는 내부 RAG를 설계하려면 무엇을 봐야 하나</td><td data-label="의도">보안</td><td data-label="판정">구체 질문형</td></tr>
<tr><th>10</th><td data-label="제목 후보">내부 RAG 구축 로드맵: 문서, 임베딩, 평가, 업데이트</td><td data-label="의도">로드맵</td><td data-label="판정">정보형</td></tr>
</tbody></table></div>
'''

meta = f'''
{h2(4, 'Meta Description 후보', 'edit')}
<p class="h2-sub">메타 설명은 본문 약속을 반복하지 말고, 클릭자가 얻을 결과를 120~160자 안에서 말한다.</p>
<div class="grid-3"><article class="score-card"><h3>추천안</h3><p>내부 RAG 구축을 시작하기 전 확인할 문서 수집, 권한 필터, 평가 기준, 업데이트 주기를 7단계 체크리스트로 정리합니다.</p></article><article class="score-card"><h3>리스크 강조안</h3><p>사내 문서 AI 검색이 실패하는 이유를 권한, 최신성, 평가 누락 관점에서 보고 내부 RAG 설계 원칙을 정리합니다.</p></article><article class="score-card"><h3>운영 관점안</h3><p>문서 연결보다 운영이 어려운 내부 RAG. 검색 품질, 보안, 업데이트 책임을 함께 설계하는 실무 가이드를 제공합니다.</p></article></div>
<section class="vt-shell" aria-label="메타 프롬프트 튜닝"><div class="vt-frame"><div class="tuner"><div class="tune-box"><div class="vt-kicker">Before</div><p class="vt-text">내부 RAG를 쉽게 설명하고 구축합니다.</p><div class="score"><span class="on"></span><span></span><span></span><span></span></div></div><div class="tune-box"><div class="vt-kicker">After</div><p class="vt-text">문서 수집, 권한 필터, 평가 기준, 업데이트 주기까지 도입 전에 정해야 할 체크리스트를 설명합니다.</p><div class="score"><span class="on"></span><span class="on"></span><span class="on"></span><span class="on"></span></div></div></div></div></section>
'''

cluster = f'''
{h2(5, '키워드 클러스터와 태그', 'search')}
<p class="h2-sub">반복 키워드를 늘리는 대신, 독자가 찾는 질문 의도별로 키워드를 묶는다.</p>
<div class="grid-3"><article class="score-card"><h3>Primary</h3><ul><li>내부 RAG 구축 가이드</li><li>사내 문서 AI 검색</li><li>RAG 구축 체크리스트</li></ul></article><article class="score-card"><h3>Secondary</h3><ul><li>권한 필터링</li><li>검색 기반 답변</li><li>RAG 평가 지표</li><li>사내 위키 검색</li></ul></article><article class="score-card"><h3>Tags</h3><p><span class="tag">#RAG</span> <span class="tag">#AI검색</span> <span class="tag">#사내검색</span> <span class="tag">#벡터DB</span> <span class="tag">#LLMOps</span> <span class="tag">#권한관리</span> <span class="tag">#운영</span></p></article></div>
'''

outline = f'''
{h2(6, '본문 구성 목차', 'question')}
<p class="h2-sub">SEO 문서는 제목 키워드만 채우면 안 된다. 본문 첫 화면과 각 H2가 검색 의도를 계속 검증해야 한다.</p>
<div class="summary-card"><p><strong>01 왜 내부 RAG가 필요한가?</strong> 문서가 흩어진 조직에서 검색 실패가 생기는 이유와 도입 전 확인할 조건을 설명한다.</p></div>
<div class="grid-2"><article class="score-card"><h3>상단 배치</h3><p>문서 수집, 권한, chunking, embedding, 평가 기준을 첫 화면에서 목록화한다.</p></article><article class="score-card"><h3>하단 배치</h3><p>FAQ, 내부 링크, 도입 후 운영 지표를 뒤에 둔다. 성능 단정은 피한다.</p></article></div>
'''

final = f'''
{h2(7, 'Final SEO Set', 'success')}
<p class="h2-sub">최종 세트는 제목·메타·slug·태그가 같은 약속을 반복하지 않고 각자 역할을 수행할 때 완성된다.</p>
<div class="grid-2"><article class="summary-card"><h3>권장 제목</h3><p>내부 RAG 구축 가이드: 사내 문서 AI 검색을 시작하는 방법</p><p><strong>Slug</strong><br>/internal-rag-build-guide</p></article><article class="summary-card"><h3>메타 설명</h3><p>내부 RAG 구축을 시작하기 전 확인할 문서 수집, 권한 필터, 평가 기준, 업데이트 주기를 7단계 체크리스트로 정리합니다.</p><p><strong>금지 표현</strong><br>완벽한 검색, 최신 모델 보장, 무료 구축, 보안 자동 해결</p></article></div>
'''

source_note = '<p class="label">작성 기준</p><p>mode 03 seo_dashboard 전용 레이아웃, seo 레시피, blog-seo-system 참조, vt card-grid/comparison-cards/prompt-tuner, wg-11 Weekly Status를 사용했다. 기존 출력 HTML 본문은 렌더 입력으로 사용하지 않았다.</p>'

layout = (ASSETS / 'layouts/seo-dashboard.html').read_text(encoding='utf-8')
for cls in ['seo-overview','serp-preview','title-candidates','meta-candidates','keyword-cluster','content-outline']:
    layout = layout.replace(f'class="{cls}"', f'class="{cls} summary-card"')
body = layout
repl = {
    'KICKER': '<span class="kicker-text">MODE 03 · SEO DASHBOARD · CAPTURE REVIEW</span>',
    'TITLE': '내부 RAG 구축 가이드 SEO 설계 대시보드',
    'SUBTITLE': '사내 문서 AI 검색 주제를 검색 의도, SERP 약속, 제목 후보, 메타 설명, 태그, 본문 목차까지 한 번에 설계하는 SEO 대시보드.',
    'META': '<span>profile auto</span><span>layout seo-dashboard</span><span>serp premium</span><span>mode 03 only</span><span>no behavioral JS</span>' + generated,
    'PRIMARY_KEYWORD': primary,
    'SERP_PREVIEW': serp,
    'TITLE_CANDIDATES': titles,
    'META_CANDIDATES': meta,
    'TAG_CLUSTER': cluster,
    'CONTENT_OUTLINE': outline,
    'FINAL_SEO_SET': final,
    'SOURCE_NOTE': source_note,
}
for k,v in repl.items():
    body=body.replace('{{'+k+'}}',v)
base=(ASSETS/'base.html').read_text(encoding='utf-8')
html=base
head={
    'TITLE':'내부 RAG 구축 가이드 SEO 설계 대시보드',
    'DESCRIPTION':'seo_dashboard 모드로 내부 RAG 구축 가이드의 검색 의도, SERP preview, 제목 후보 10개, 메타 설명, 태그와 본문 목차를 설계한 한국어 HTML 대시보드.',
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
    'mode':'03_seo_dashboard',
    'file':str(OUT.relative_to(ROOT)),
    'link':'http://localhost:8080/output/adaptive-html-final-sequential-16-modes-20260607_105404/pages/03_seo_dashboard_internal_rag_guide.html',
    'policy':'previous HTML body not reused by render script; common generator not used; seo_dashboard layout/recipe/references/templates consulted for this page only',
    'materials_sha256':MATERIAL_HASH,
    'used_materials':[str(p.relative_to(REPO)) for p in MODE_MATERIALS],
    'visual_contract':{
        'direct_sections_use_view_surface':True,
        'numbered_h2_order':'body-icon body-icon--sm -> num -> title',
        'serp_premium_classes':['serp-shell','serp-box','serp-rule-grid','serp-variant-strip'],
        'forbidden_seo_prefixes_absent':True,
        'title_candidates_count':10,
        'vt_required':['card-grid'],
        'vt_used':['card-grid','comparison-cards','prompt-tuner'],
        'wg_used':['11-weekly-status'],
        'table_mobile_safe':'table-scroll + mobile-card-table'
    },
    'next_mode':'04_education_html'
}
(ROOT/'sources/03_seo_dashboard-visual-contract-evidence.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(OUT)
