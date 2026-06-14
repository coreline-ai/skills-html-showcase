#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
SKILL = REPO / 'skills/adaptive-html-final'
ASSETS = SKILL / 'assets'
OUT = ROOT / 'pages/06_youtube_analysis_local_rag_knowledge_vault.html'

MODE_MATERIALS = [
    SKILL / 'SKILL.md',
    SKILL / 'recipes/youtube-analysis.prompt.md',
    ASSETS / 'layouts/youtube-analysis.html',
    SKILL / 'references/youtube-analysis-system.md',
    SKILL / 'references/layout-system.md',
    SKILL / 'references/writing-system.md',
    SKILL / 'references/body-icon-system.md',
    SKILL / 'references/visual-html-system.md',
    SKILL / 'references/widget-system.md',
    ASSETS / 'visual-html-templates/04-timeline.html',
    ASSETS / 'visual-html-templates/03-risk-matrix.html',
    ASSETS / 'visual-html-templates/06-quality-gate.html',
    ASSETS / 'visual-html-templates/02-decision-tree.html',
    ASSETS / 'visual-html-templates/13-comparison-cards.html',
    ASSETS / 'visual-html-templates/05-checklist-flow.html',
    ASSETS / 'widget-templates/11-weekly-status.html',
    ASSETS / 'widget-templates/13-annotated-flowchart.html',
    ASSETS / 'widget-templates/14-feature-explainer.html',
    ASSETS / 'widget-templates/16-implementation-plan.html',
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
def h2(num: int, title: str, icon_id: str = 'timeline') -> str:
    return f'<h2>{icon(icon_id)}<span class="num">{num}</span>{title}</h2>'

generated = '''<div class="generated-row"><p class="generated-date">observed_at · 2026-06-07 KST · 입력 Tier C</p><div class="lens-strip" aria-label="적용 렌즈"><span class="lens-strip-label">LENS</span><span class="lens-chip">mode 06</span><span class="lens-chip">youtube_analysis</span><span class="lens-chip">Tier C</span><span class="lens-chip">FACT/INFERENCE/UNKNOWN</span><span class="lens-chip">no iframe</span></div></div>'''

verdict = f'''
{h2(1, 'TL;DW — 조건부 시청', 'decision')}
<p class="h2-sub">입력은 “Local RAG Knowledge Vault”라는 주제 라벨뿐이다. 따라서 이 리포트는 실제 영상 내용을 단정하지 않고, 시청 전 판단·검증 질문·후속 콘텐츠 설계를 정리한다.</p>
<div class="youtube-evidence-grid"><article class="youtube-card youtube-fact"><p class="youtube-label">FACT</p><h3>확보된 입력</h3><p>제공된 정보는 주제 라벨과 분석 요청뿐이다. URL, 자막, 챕터, 댓글 표본, 조회수 같은 영상 표면 데이터는 제공되지 않았다.</p></article><article class="youtube-card youtube-inference"><p class="youtube-label">INFERENCE</p><h3>누가 보면 좋은가</h3><p>로컬 RAG, 개인 지식 금고, 노트/문서 검색 흐름을 설계하려는 독자에게 유효할 가능성이 있다. 단, 실제 영상이 설치 튜토리얼인지 개념 소개인지는 확인 필요다.</p></article><article class="youtube-card youtube-unknown"><p class="youtube-label">UNKNOWN</p><h3>시청 판단 보류 지점</h3><p>영상의 실제 주장, 데모 성공 여부, 사용 도구, 데이터 보안 언급, 댓글 반응은 확인 불가다. 자막 또는 챕터가 확보되면 아래 Evidence Map을 FACT로 승격한다.</p></article></div>
<section class="vt-shell" aria-label="조건부 시청 결정 트리"><div class="vt-frame"><div class="dt-q">지금 이 영상을 봐야 하나?</div><div class="dt-options"><article class="dt-card"><span class="vt-kicker">WATCH</span><h3>로컬 RAG 입문자</h3><p class="vt-text">자막이 확보되고 설치/색인/질의 흐름이 실제로 포함되어 있으면 우선 시청한다.</p></article><article class="dt-card"><span class="vt-kicker">SKIP</span><h3>운영 보안 검토자</h3><p class="vt-text">권한·개인정보·백업 언급이 없으면 단순 데모로 보고 보류한다.</p></article><article class="dt-card"><span class="vt-kicker">CHECK</span><h3>콘텐츠 제작자</h3><p class="vt-text">댓글 질문과 retention 구간을 확인해 후속 시리즈 설계에 쓴다.</p></article></div><div class="dt-arrow">↓</div><div class="dt-q">권장: 자막/챕터/댓글 20개 표본 확보 후 재평가</div></div></section>
'''

question_toc = '''<div class="toc-map">
  <span class="label">시청 판단 목차</span>
  <p>영상 내용을 단정하지 않고, 확보 가능한 증거와 확인 질문으로 읽습니다.</p>
  <div class="toc-pills">
    <a class="toc-pill" href="#source-trust"><b>1</b>믿을 수 있나</a>
    <a class="toc-pill" href="#watching-decision"><b>2</b>누가 보나</a>
    <a class="toc-pill" href="#evidence-map"><b>3</b>근거 좌표</a>
    <a class="toc-pill" href="#chapter-retention"><b>4</b>편집 흐름</a>
    <a class="toc-pill" href="#comments"><b>5</b>댓글 신호</a>
    <a class="toc-pill" href="#opportunity"><b>6</b>콘텐츠 기회</a>
    <a class="toc-pill" href="#source-limits"><b>7</b>확인 한계</a>
  </div>
</div>'''

source_trust = f'''
{h2(2, 'Source & Trust Snapshot', 'source')}
<p class="h2-sub">Tier C에서는 영상 내부 발화를 FACT로 쓰지 않는다. FACT는 “무엇이 제공됐는가”에 한정하고, 콘텐츠 해석은 추론 또는 확인 필요로 표시한다.</p>
<div class="youtube-signal-grid"><article class="youtube-signal youtube-fact"><p class="youtube-label">FACT</p><h3>Input Tier C</h3><p>URL/transcript/comment/metadata가 없고 주제 라벨만 있다. 그래서 타임스탬프, 발화 인용, 댓글 비율을 만들지 않는다.</p></article><article class="youtube-signal youtube-inference"><p class="youtube-label">INFERENCE</p><h3>가정 가능한 주제 범위</h3><p>Local RAG는 로컬 파일 색인, 임베딩, 벡터 검색, 출처 표시, 개인 정보 보호를 포함할 가능성이 높다. 이는 영상 사실이 아니라 주제에서 도출한 분석 프레임이다.</p></article><article class="youtube-signal youtube-unknown"><p class="youtube-label">UNKNOWN</p><h3>승격 조건</h3><p>영상 URL, 자막, 챕터, 댓글 표본 20개 이상, 설명란 링크를 확보하면 주장별 FACT 좌표를 붙일 수 있다.</p></article></div>
<section class="wg-11" aria-labelledby="m06-wg11-title"><header class="wg-11-head"><p class="wg-11-kicker">Source Readiness</p><h2 id="m06-wg11-title" class="wg-11-h">Local RAG 영상 분석 준비도</h2><p class="wg-11-lead">현재는 주제 라벨만 있으므로 시청 판단보다 확인 질문 목록이 더 중요하다.</p></header><div class="wg-11-kpis"><div class="wg-11-kpi wg-11-kpi-risk"><span class="wg-11-kpi-v wg-11-warn">C</span><span class="wg-11-kpi-l">input tier</span></div><div class="wg-11-kpi wg-11-kpi-prog"><span class="wg-11-kpi-v">0</span><span class="wg-11-kpi-l">timestamps</span></div><div class="wg-11-kpi wg-11-kpi-risk"><span class="wg-11-kpi-v">0</span><span class="wg-11-kpi-l">comments</span></div><div class="wg-11-kpi"><span class="wg-11-kpi-v">5</span><span class="wg-11-kpi-l">검증 질문</span></div></div><h3 class="wg-11-h3">확보 수준</h3><div class="wg-11-bars"><div class="wg-11-bar-row"><span class="wg-11-bar-label">주제 파악</span><div class="wg-11-track" role="img" aria-label="주제 파악 60퍼센트"><div class="wg-11-fill wg-11-fill-prog" style="width:60%"></div></div><span class="wg-11-bar-pct">60%</span></div><div class="wg-11-bar-row"><span class="wg-11-bar-label">발화 근거</span><div class="wg-11-track" role="img" aria-label="발화 근거 0퍼센트 리스크"><div class="wg-11-fill wg-11-fill-risk" style="width:8%"></div></div><span class="wg-11-bar-pct">0%</span></div><div class="wg-11-bar-row"><span class="wg-11-bar-label">댓글 신호</span><div class="wg-11-track" role="img" aria-label="댓글 신호 0퍼센트 리스크"><div class="wg-11-fill wg-11-fill-risk" style="width:8%"></div></div><span class="wg-11-bar-pct">0%</span></div></div><div class="wg-11-cols"><div class="wg-11-col wg-11-col-good"><h4 class="wg-11-col-h"><span class="wg-11-dot"></span>확정</h4><ul class="wg-11-col-list"><li>주제 라벨 존재 <span class="wg-11-tk">FACT</span></li></ul></div><div class="wg-11-col wg-11-col-prog"><h4 class="wg-11-col-h"><span class="wg-11-dot"></span>추론</h4><ul class="wg-11-col-list"><li>로컬 RAG 워크플로우 가능성 <span class="wg-11-tk">INFERENCE</span></li></ul></div><div class="wg-11-col wg-11-col-risk"><h4 class="wg-11-col-h"><span class="wg-11-dot"></span>한계</h4><ul class="wg-11-col-list"><li>영상 내용과 댓글 여론은 확인 불가 <span class="wg-11-flag">UNKNOWN</span></li></ul></div></div></section>
'''

watching = f'''
{h2(3, 'Watching Decision — 누가 보고 누가 건너뛰나', 'question')}
<p class="h2-sub">시청 추천은 영상 내용 확인 전이므로 조건부다. 보는 사람은 확인 질문을 들고 보고, 건너뛰는 사람은 먼저 자막이나 챕터를 요청하는 편이 낫다.</p>
<div class="youtube-evidence-grid"><article class="youtube-card"><p class="youtube-label">추천</p><h3>개인 문서 검색을 시작하려는 사람</h3><p>영상이 실제 파일 수집→색인→질의→출처 확인을 보여준다면 유효하다. 특히 노트 앱, PDF, markdown을 한곳에서 검색하려는 사용자에게 적합할 가능성이 있다.</p></article><article class="youtube-card"><p class="youtube-label">조건부</p><h3>팀 지식관리 담당자</h3><p>팀 단위 도입자는 권한, 동기화, 감사 로그가 필요하다. 영상이 개인 로컬 데모만 다루면 팀 운영 판단에는 부족하다.</p></article><article class="youtube-card youtube-unknown"><p class="youtube-label">스킵</p><h3>보안·컴플라이언스 검토자</h3><p>로컬 RAG가 개인정보를 어떻게 저장하고 삭제하는지 언급하지 않으면 바로 채택 판단을 할 수 없다. 해당 항목은 자막 확인 전까지 UNKNOWN이다.</p></article></div>
<section class="wg-14" aria-labelledby="m06-wg14-title"><p class="wg-14-kicker">Viewing Guide</p><h2 id="m06-wg14-title" class="wg-14-h">시청 전 확인할 질문 3개</h2><p class="wg-14-lead">Tier C에서는 질문을 먼저 정하고 영상을 보며 증거를 채워야 한다.</p><div class="wg-14-tldr" role="note" aria-label="핵심 요약"><span class="wg-14-tldr-tag">TL;DR</span><p class="wg-14-tldr-body"><strong>“로컬”이라는 말이 보안 보장을 뜻하지 않는다.</strong> 데이터 위치, 인덱스 삭제, 출처 표시가 실제로 나오는지 확인해야 한다.</p></div><div class="wg-14-acc"><details class="wg-14-sec" open><summary class="wg-14-sum"><span class="wg-14-sum-no">01</span> 무엇을 로컬에 저장하나 <span class="wg-14-chev" aria-hidden="true"></span></summary><div class="wg-14-sec-body"><p>원문 파일, chunk, embedding, vector index, 질의 로그 중 무엇이 디스크에 남는지 확인한다.</p><ul class="wg-14-list"><li>삭제 절차가 있는가</li><li>민감 파일 제외 규칙이 있는가</li></ul></div></details><details class="wg-14-sec"><summary class="wg-14-sum"><span class="wg-14-sum-no">02</span> 답변에 출처가 붙나 <span class="wg-14-chev" aria-hidden="true"></span></summary><div class="wg-14-sec-body"><ol class="wg-14-flow"><li><span class="wg-14-flow-n">1</span>검색 결과 문서명 확인</li><li><span class="wg-14-flow-n">2</span>인용 구간 또는 링크 확인</li><li><span class="wg-14-flow-n">3</span>없는 답을 모른다고 말하는지 확인</li></ol></div></details></div><h3 class="wg-14-h3">검증 메모 형식</h3><div class="wg-14-tabs"><input type="radio" name="m06-wg14-tab" id="wg-14-tab-yml" class="wg-14-tab-in" checked><input type="radio" name="m06-wg14-tab" id="wg-14-tab-cli" class="wg-14-tab-in"><input type="radio" name="m06-wg14-tab" id="wg-14-tab-api" class="wg-14-tab-in"><div class="wg-14-tablist"><label class="wg-14-tab" for="wg-14-tab-yml">watch note</label><label class="wg-14-tab" for="wg-14-tab-cli">evidence</label><label class="wg-14-tab" for="wg-14-tab-api">risk</label></div><pre class="wg-14-code wg-14-code-yml"><code>question: 로컬 인덱스 삭제 절차가 있나?
status: 확인 필요
evidence: 자막/화면 좌표 필요</code></pre><pre class="wg-14-code wg-14-code-cli"><code>claim: "개인 지식 금고 구축 가능"
proof_needed:
  - 파일 수집 방식
  - 출처 표시
  - 재색인/삭제</code></pre><pre class="wg-14-code wg-14-code-api"><code>risk: 보안 과장
mitigation: 개인정보/민감문서 제외 규칙 확인 전 채택 보류</code></pre></div></section>
'''

evidence_map = f'''
{h2(4, 'Video Evidence Map — 주장·근거·판정', 'metric')}
<p class="h2-sub">아래 표는 실제 영상 주장이 아니라, 주제 라벨에서 도출한 “확인해야 할 주장 후보”다. 자막이나 타임스탬프가 들어오면 FACT로 승격한다.</p>
<div class="table-scroll mobile-card-table"><table class="mobile-card-table"><caption>Video Evidence Map — Local RAG Knowledge Vault 검증 후보</caption><thead><tr><th>주장 후보</th><th>현재 근거</th><th>판정</th><th>다음 확인</th></tr></thead><tbody><tr><th>로컬 파일로 개인 지식 금고를 만들 수 있다</th><td data-label="현재 근거">주제 라벨만 있음</td><td data-label="판정">INFERENCE</td><td data-label="다음 확인">실제 파일 수집 화면과 성공 질의 장면 필요</td></tr><tr><th>데이터가 외부로 나가지 않는다</th><td data-label="현재 근거">근거 없음</td><td data-label="판정">UNKNOWN</td><td data-label="다음 확인">모델/API 호출, telemetry, 저장 위치 확인</td></tr><tr><th>답변에 출처가 붙는다</th><td data-label="현재 근거">근거 없음</td><td data-label="판정">UNKNOWN</td><td data-label="다음 확인">출처 링크 또는 인용 구간 화면 확인</td></tr><tr><th>초보자도 설치 가능하다</th><td data-label="현재 근거">근거 없음</td><td data-label="판정">확인 필요</td><td data-label="다음 확인">설치 시간, 실패 경로, OS 요구사항 확인</td></tr><tr><th>후속 콘텐츠 수요가 있다</th><td data-label="현재 근거">주제 자체는 수요 가능성이 있음</td><td data-label="판정">INFERENCE</td><td data-label="다음 확인">댓글 질문, 조회 지속 구간, 반복 요청 확인</td></tr></tbody></table></div>
<section class="vt-shell" aria-label="영상 근거 흐름 타임라인"><div class="vt-frame"><ol class="tl"><li class="tl-item"><b>도입부 확인</b><p class="vt-text">문제가 “검색 불편”인지 “지식 재사용”인지 확인한다. 근거는 자막 첫 30초가 필요하다.</p></li><li class="tl-item"><b>데모 확인</b><p class="vt-text">파일 수집·색인·질의·출처 표시가 한 흐름으로 이어지는지 본다. 화면 녹화 좌표가 필요하다.</p></li><li class="tl-item"><b>한계 확인</b><p class="vt-text">민감문서, 삭제, hallucination, 재색인 한계를 언급하는지 확인한다.</p></li><li class="tl-item"><b>행동 확인</b><p class="vt-text">시청자가 따라 할 체크리스트나 repo 링크가 있는지 확인한다.</p></li></ol></div></section>
'''

chapter = f'''
{h2(5, 'Chapter / Retention Story', 'timeline')}
<p class="h2-sub">실제 챕터가 없기 때문에 아래 구조는 분석 프레임이다. retention 수치가 아니라, 시청자가 이탈할 수 있는 설명 구간을 예측하는 지도다.</p>
<div class="youtube-chapter-grid"><article class="youtube-card youtube-inference"><p class="youtube-label">INFERENCE</p><h3>첫 30초</h3><p>문제 정의가 “내 노트가 쌓이는데 다시 못 찾는다”처럼 구체적이면 유지 가능성이 높다. 도구 이름부터 시작하면 초보자는 이탈할 수 있다.</p></article><article class="youtube-card youtube-inference"><p class="youtube-label">INFERENCE</p><h3>중반 데모</h3><p>파일 추가 후 바로 답변이 바뀌는 장면이 있으면 신뢰도가 올라간다. 반대로 설정 설명만 길면 이탈 위험이 커진다.</p></article><article class="youtube-card youtube-unknown"><p class="youtube-label">UNKNOWN</p><h3>리텐션 데이터</h3><p>실제 retention, CTR, replay 구간은 비공개 analytics이므로 추정하지 않는다. 제작자가 제공해야 FACT가 된다.</p></article></div>
<section class="wg-13-fc" aria-label="영상 구조 확인 플로우차트"><h3 class="wg-13-h">시청 흐름 검증 <span class="wg-13-sub">Tier C용 확인 절차</span></h3><div class="wg-13-flow"><a href="#m06-wg13-s1" class="wg-13-node wg-13-node--start"><span class="wg-13-step">시작</span>자막 확보</a><span class="wg-13-arrow" aria-hidden="true">↓</span><a href="#m06-wg13-s2" class="wg-13-node"><span class="wg-13-step">1</span>주장 표시</a><span class="wg-13-arrow" aria-hidden="true">↓</span><div class="wg-13-branch"><a href="#m06-wg13-s3" class="wg-13-node wg-13-node--decide"><span class="wg-13-step">2</span>증거 좌표 있음?</a><div class="wg-13-paths"><div class="wg-13-path wg-13-path--fail"><span class="wg-13-edge">아니오 → 확인 필요</span><a href="#m06-wg13-fail" class="wg-13-node wg-13-node--fail"><span class="wg-13-step">!</span>UNKNOWN 유지</a></div><div class="wg-13-path wg-13-path--ok"><span class="wg-13-edge">예 → 정상</span><a href="#m06-wg13-s4" class="wg-13-node"><span class="wg-13-step">3</span>판정 갱신</a><span class="wg-13-arrow" aria-hidden="true">↓</span><a href="#m06-wg13-s5" class="wg-13-node wg-13-node--end"><span class="wg-13-step">완료</span>Evidence Map 확정</a></div></div></div></div><div class="wg-13-detail"><h4 class="wg-13-dh">단계 상세 <span class="wg-13-dnote">증거 좌표가 없으면 FACT로 승격하지 않는다</span></h4><details id="m06-wg13-s2" class="wg-13-acc" open><summary><span class="wg-13-tag">1단계</span>주장 표시</summary><div class="wg-13-body"><p>자막에서 “쉽다”, “로컬”, “안전하다”, “검색된다” 같은 핵심 주장 문장을 표시한다.</p></div></details><details id="m06-wg13-s3" class="wg-13-acc"><summary><span class="wg-13-tag">2단계</span>증거 좌표</summary><div class="wg-13-body"><p>각 주장에 타임스탬프, 화면 장면, 설명란 링크, 댓글 표본 중 하나 이상을 연결한다.</p></div></details><details id="m06-wg13-fail" class="wg-13-acc wg-13-acc--fail"><summary><span class="wg-13-tag wg-13-tag--fail">실패</span>UNKNOWN 유지</summary><div class="wg-13-body"><p>좌표가 없으면 “그럴듯한 설명”이어도 FACT가 아니다. 이 리포트는 확인 필요로 남긴다.</p></div></details><details id="m06-wg13-s5" class="wg-13-acc wg-13-acc--ok"><summary><span class="wg-13-tag wg-13-tag--ok">완료</span>Evidence Map 확정</summary><div class="wg-13-body"><p>5개 이상 주장에 좌표가 붙으면 full report로 승격할 수 있다.</p></div></details></div></section>
'''

comments = f'''
{h2(6, 'Comment Signal Wall — 댓글 표본 한계', 'connection')}
<p class="h2-sub">댓글은 아직 제공되지 않았다. 따라서 댓글 여론을 단정하지 않고, 수집되면 어떤 신호로 분류할지 벽면 카드로 준비한다.</p>
<div class="youtube-comment-grid"><article class="youtube-card youtube-unknown"><p class="youtube-label">UNKNOWN</p><h3>반복 질문</h3><p>“어떤 파일 형식을 지원하나요?”, “로컬 LLM도 가능한가요?” 같은 질문이 반복되는지 확인해야 한다. 반복 질문은 후속 영상의 제목 후보가 된다.</p></article><article class="youtube-card youtube-unknown"><p class="youtube-label">UNKNOWN</p><h3>실패 보고</h3><p>설치 오류, 인덱싱 실패, 답변 품질 불만이 있는지 댓글 표본으로 확인한다. 실패 댓글은 튜토리얼 보강 지점이다.</p></article><article class="youtube-card youtube-unknown"><p class="youtube-label">UNKNOWN</p><h3>보안 우려</h3><p>개인 파일, 회사 문서, API 전송, 삭제 방식에 대한 우려가 있는지 본다. 이 신호가 많으면 보안 설명 영상이 우선이다.</p></article></div>
<div class="youtube-evidence-grid"><article class="youtube-evidence"><p class="youtube-label">수집 기준</p><h3>표본 20개 이상</h3><p>상위 댓글만 보면 팬 반응에 치우칠 수 있다. 최신순·인기순을 나눠 최소 20개를 추출해야 한다.</p></article><article class="youtube-evidence"><p class="youtube-label">분류 기준</p><h3>질문 / 실패 / 요청</h3><p>댓글을 감정으로만 보지 말고 다음 콘텐츠로 바꿀 수 있는 요구로 분류한다.</p></article><article class="youtube-evidence"><p class="youtube-label">금지</p><h3>전체 여론 단정 금지</h3><p>댓글 표본은 시청자 전체를 대표하지 않는다. “댓글 반응이 좋다/나쁘다”는 표현은 표본 수와 함께 써야 한다.</p></article></div>
'''

opportunity = f'''
{h2(7, 'Opportunity Matrix — 다음 콘텐츠 기회', 'impact')}
<p class="h2-sub">주제 라벨만 있어도 후속 콘텐츠 가설은 만들 수 있다. 다만 제작 우선순위는 댓글과 retention 확인 후 확정해야 한다.</p>
<section class="vt-shell" aria-label="콘텐츠 기회 비교 카드"><div class="vt-frame"><div class="cmp"><article class="cmp-card pick"><span class="vt-kicker">Series 1</span><h3>로컬 RAG 30분 구축</h3><p class="vt-text">수요 근거는 주제 적합성이다. 난이도는 중간이며 설치 실패 경로를 포함해야 한다.</p></article><article class="cmp-card"><span class="vt-kicker">Series 2</span><h3>개인정보 안전 점검</h3><p class="vt-text">보안 우려 댓글이 많으면 우선순위가 올라간다. 삭제와 제외 규칙이 핵심이다.</p></article><article class="cmp-card"><span class="vt-kicker">Series 3</span><h3>노트 앱별 연결법</h3><p class="vt-text">Obsidian, Notion export, markdown 폴더를 나누면 검색 의도가 선명해진다.</p></article></div></div></section>
<div class="youtube-opportunity-grid"><article class="youtube-opportunity"><span class="youtube-badge">난이도 중</span><h3>설치 튜토리얼</h3><p>파일 10개로 작은 색인부터 시작하는 흐름이 좋다. 설치 실패와 권한 오류를 함께 보여주면 신뢰가 생긴다.</p></article><article class="youtube-opportunity"><span class="youtube-badge">난이도 낮음</span><h3>질문 템플릿 20개</h3><p>“지난 회의에서 결정한 것”, “이 프로젝트의 위험” 같은 질의 예시를 제공하면 재사용성이 높다.</p></article><article class="youtube-opportunity"><span class="youtube-badge">난이도 높음</span><h3>평가 세트 만들기</h3><p>정답이 있는 질문과 출처 검증을 묶어 RAG 품질을 비교한다. 전문가 독자에게 가치가 크다.</p></article></div>
'''

claim_risk = f'''
{h2(8, 'Claim / Evidence / Risk', 'warning')}
<p class="h2-sub">Local RAG 주제에서 가장 위험한 과장은 “로컬이면 자동으로 안전하다”는 암묵적 약속이다. 증거 없이는 보안·정확도·쉬움을 단정하지 않는다.</p>
<section class="vt-shell" aria-label="주장 위험 매트릭스"><div class="vt-frame"><div class="rm-grid"><div class="rm-head">가능성 낮음</div><div class="rm-head">가능성 중간</div><div class="rm-head">가능성 높음</div><div class="rm-cell"><strong>낮은 영향</strong><p class="vt-text">도구명 오기처럼 정정 가능한 오류.</p></div><div class="rm-cell"><strong>중간 영향</strong><p class="vt-text">설치 난이도 축소 표현. 초보자 이탈을 만든다.</p></div><div class="rm-cell"><strong>높은 영향</strong><p class="vt-text"><span class="rm-risk high">보안 안전 단정</span> 근거 없으면 신뢰 리스크가 크다.</p></div><div class="rm-cell"><strong>낮은 영향</strong><p class="vt-text">썸네일 기대치와 실제 난이도 차이.</p></div><div class="rm-cell"><strong>중간 영향</strong><p class="vt-text"><span class="rm-risk med">출처 없는 답변</span> 데모가 좋아 보여도 검증 불가.</p></div><div class="rm-cell"><strong>높은 영향</strong><p class="vt-text"><span class="rm-risk high">개인 파일 처리 불명확</span> 채택 보류 사유.</p></div></div></div></section>
<section class="vt-shell" aria-label="검증 품질 게이트"><div class="vt-frame"><div class="qg-grid"><article class="qg-card block"><span class="vt-kicker">BLOCK</span><h3>데이터 이동 경로 없음</h3><p class="vt-text">외부 API 호출 여부가 없으면 보안 주장은 UNKNOWN이다.</p></article><article class="qg-card warn"><span class="vt-kicker">WARN</span><h3>출처 표시 없음</h3><p class="vt-text">답변 품질은 좋아 보여도 검증 가능성이 떨어진다.</p></article><article class="qg-card"><span class="vt-kicker">PASS</span><h3>작은 파일셋 데모</h3><p class="vt-text">재현 가능한 샘플과 실패 경로가 있으면 입문 콘텐츠로 충분하다.</p></article><div class="qg-final"><strong>Gate:</strong> 보안·정확도 주장은 자막 좌표와 화면 근거 없이는 FACT로 승격하지 않는다.</div></div></div></section>
<div class="table-scroll mobile-card-table"><table class="mobile-card-table"><caption>Claim / Evidence / Risk 완화표</caption><thead><tr><th>주장</th><th>현재 상태</th><th>위험</th><th>완화</th></tr></thead><tbody><tr><th>로컬이라 안전하다</th><td data-label="현재 상태">UNKNOWN</td><td data-label="위험">보안 과장</td><td data-label="완화">데이터 저장 위치와 외부 전송 여부 확인</td></tr><tr><th>쉽게 구축한다</th><td data-label="현재 상태">확인 필요</td><td data-label="위험">초보자 실패</td><td data-label="완화">설치 실패 경로와 OS 조건 확인</td></tr><tr><th>정확히 답한다</th><td data-label="현재 상태">확인 필요</td><td data-label="위험">환각/출처 누락</td><td data-label="완화">정답 세트와 출처 표시 화면 확인</td></tr></tbody></table></div>
'''

blueprint = f'''
{h2(9, 'Video Blueprint — 다시 만든다면', 'flow')}
<p class="h2-sub">다음 영상을 설계한다면 “도구 소개”보다 “내 문서를 다시 찾는 실패를 해결하는 3단계”로 구성하는 편이 명확하다.</p>
<section class="wg-16" aria-labelledby="m06-wg16-title"><header class="wg-16-head"><p class="wg-16-kicker">Video Blueprint</p><h2 id="m06-wg16-title" class="wg-16-h">Local RAG Knowledge Vault 8분 구성안</h2><p class="wg-16-lead">Hook→Proof→Action 구조로 시청자가 끝까지 따라갈 근거를 만든다. 실제 원본 영상과 다른 제안일 수 있으므로 blueprint는 INFERENCE다.</p></header><div class="wg-16-panel"><h3 class="wg-16-h3">마일스톤 타임라인</h3><ol class="wg-16-ms"><li class="wg-16-ms-item wg-16-done"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">0:00~0:30 · 문제 Hook</span><span class="wg-16-badge wg-16-bd-done">Hook</span></div><p class="wg-16-ms-desc">“지난달 회의 결정을 못 찾는 문제”처럼 실제 실패 장면을 보여준다.</p></div></li><li class="wg-16-ms-item wg-16-active"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">0:30~3:00 · 작은 금고 만들기</span><span class="wg-16-badge wg-16-bd-active">Proof</span></div><p class="wg-16-ms-desc">문서 10개로 수집→색인→질의 흐름을 짧게 보여준다.</p></div></li><li class="wg-16-ms-item"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">3:00~6:30 · 검증과 한계</span><span class="wg-16-badge">Trust</span></div><p class="wg-16-ms-desc">출처 표시, 모르는 질문, 삭제, 민감 파일 제외를 보여준다.</p></div></li><li class="wg-16-ms-item"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">6:30~8:00 · 다음 행동</span><span class="wg-16-badge">Action</span></div><p class="wg-16-ms-desc">체크리스트와 sample repo, 질문 템플릿을 제공한다.</p></div></li></ol><h3 class="wg-16-h3">데이터 플로우</h3><div class="wg-16-flow" aria-label="Local RAG 영상 설명 플로우"><div class="wg-16-fnode">Files<span class="wg-16-fnode-s">pdf/md/notes</span></div><div class="wg-16-fnode">Chunking<span class="wg-16-fnode-s">분할·메타</span></div><div class="wg-16-fnode wg-16-fnode-good">Index<span class="wg-16-fnode-s">vector store</span></div><div class="wg-16-fnode wg-16-fnode-hot">Question<span class="wg-16-fnode-s">검색·생성</span></div><div class="wg-16-fnode wg-16-fnode-q">Answer<span class="wg-16-fnode-s">출처·한계</span></div></div><h3 class="wg-16-h3">제작 리스크</h3><div class="wg-16-table-wrap table-scroll"><table class="wg-16-table"><caption>영상 재설계 리스크 — 가능성·영향·완화책</caption><thead><tr><th>리스크</th><th>가능성</th><th>영향</th><th>완화책</th></tr></thead><tbody><tr><th>보안 과장</th><td><span class="wg-16-lv wg-16-lv-mid">중</span></td><td><span class="wg-16-lv wg-16-lv-hi">높음</span></td><td>데이터 이동 경로와 삭제 절차를 화면으로 보여준다.</td></tr><tr><th>설치 실패</th><td><span class="wg-16-lv wg-16-lv-mid">중</span></td><td><span class="wg-16-lv wg-16-lv-mid">중</span></td><td>OS별 사전조건과 실패 경로를 별도 카드로 둔다.</td></tr><tr><th>출처 누락</th><td><span class="wg-16-lv wg-16-lv-lo">낮음</span></td><td><span class="wg-16-lv wg-16-lv-hi">높음</span></td><td>답변마다 문서명/구간을 함께 표시한다.</td></tr></tbody></table></div></div></section>
'''

reuse = f'''
{h2(10, 'Reuse Pack — 플랫폼별 재사용 조각', 'platform')}
<p class="h2-sub">원본 확인 전에도 재사용 설계는 가능하다. 단, 실제 문구와 타임스탬프는 자막 확보 뒤 채워야 한다.</p>
<div class="youtube-reuse-grid"><article class="youtube-card"><p class="youtube-label">Shorts</p><h3>30초 문제 Hook</h3><p>“내 문서가 많은데 다시 못 찾는다” 장면을 짧게 보여준다. 실제 원본에서 가장 강한 문제 제기 구간을 찾아 써야 한다.</p></article><article class="youtube-card"><p class="youtube-label">Blog</p><h3>로컬 RAG 체크리스트</h3><p>파일 수집, 민감 파일 제외, 출처 표시, 삭제 절차를 문서형 체크리스트로 바꾼다.</p></article><article class="youtube-card"><p class="youtube-label">Newsletter</p><h3>질문 템플릿 10개</h3><p>개인 지식 금고에 던질 좋은 질문 예시를 모아 배포한다. 실제 답변 품질은 별도 검증한다.</p></article></div>
<section class="vt-shell" aria-label="재사용 체크 플로우"><div class="vt-frame"><div class="cf"><div class="cf-item"><span class="cf-check">1</span><div><b>원본 구간 선택</b><p class="vt-text">자막/타임스탬프가 있는 구간만 재사용한다.</p></div><span class="cf-state">CHECK</span></div><div class="cf-item"><span class="cf-check">2</span><div><b>근거 수준 표기</b><p class="vt-text">FACT와 INFERENCE를 각 포맷에 명시한다.</p></div><span class="cf-state">PASS</span></div><div class="cf-item"><span class="cf-check">3</span><div><b>과장 제거</b><p class="vt-text">보안·정확도·쉬움은 확인된 장면만 말한다.</p></div><span class="cf-state">GUARD</span></div></div></div></section>
'''

next_actions = f'''
{h2(11, 'Next Actions — UNKNOWN 승격 계획', 'check')}
<p class="h2-sub">다음 단계의 목적은 더 그럴듯한 요약을 쓰는 것이 아니라, UNKNOWN을 FACT로 승격하거나 폐기하는 것이다.</p>
<div class="youtube-blueprint-grid"><article class="youtube-card"><h3>1. URL/자막 확보</h3><p>영상 URL, 자동 자막 또는 수동 transcript, 설명란 링크를 확보한다. 타임스탬프 없는 요약은 full report로 보지 않는다.</p></article><article class="youtube-card"><h3>2. 댓글 표본 수집</h3><p>인기순과 최신순을 나눠 최소 20개 댓글을 모은다. 질문/실패/요청/칭찬으로 분류한다.</p></article><article class="youtube-card"><h3>3. Evidence Map 갱신</h3><p>5개 이상 주장에 좌표를 붙인다. 좌표가 없는 주장은 계속 UNKNOWN으로 둔다.</p></article></div>
<section class="vt-shell" aria-label="UNKNOWN 승격 게이트"><div class="vt-frame"><div class="qg-grid"><article class="qg-card"><span class="vt-kicker">FACT</span><h3>승격 가능</h3><p class="vt-text">자막 문장, 화면 장면, 댓글 원문, 설명란 링크가 있으면 가능하다.</p></article><article class="qg-card warn"><span class="vt-kicker">INFERENCE</span><h3>보류</h3><p class="vt-text">반복 질문이나 제작 기회는 표본 수가 있어야 강해진다.</p></article><article class="qg-card block"><span class="vt-kicker">UNKNOWN</span><h3>유지</h3><p class="vt-text">비공개 retention, CTR, revenue, 전체 댓글 여론은 계속 확인 불가다.</p></article><div class="qg-final"><strong>Source Limits:</strong> Tier C에서는 실제 영상 발화·댓글 여론·analytics를 단정하지 않는다.</div></div></div></section>
'''

source_note = '''<p class="label">Source Limits · 분석 기준 시각</p><p>observed_at: 2026-06-07 KST. 입력 Tier C — 영상 URL, transcript, chapter, metadata, 댓글 표본이 제공되지 않았고 “Local RAG Knowledge Vault” 주제 라벨만 확인했다. 따라서 실제 발화, 타임스탬프, 댓글 여론, 조회수·retention·CTR·revenue는 확인 불가다. 이 HTML은 YouTube iframe/player/embed/자동재생를 의도적으로 사용하지 않는다. 기존 출력 HTML 본문은 렌더 입력으로 사용하지 않았다.</p>'''

layout = (ASSETS / 'layouts/youtube-analysis.html').read_text(encoding='utf-8')
section_ids = {
    'source-trust': 'source-trust',
    'watching-decision': 'watching-decision',
    'video-evidence-map': 'evidence-map',
    'chapter-retention': 'chapter-retention',
    'comment-signals': 'comments',
    'opportunity-matrix': 'opportunity',
    'claim-risk': 'claim-risk',
    'video-blueprint': 'blueprint',
    'reuse-pack': 'reuse',
    'try': 'source-limits',
}
for cls, sid in section_ids.items():
    layout = layout.replace(f'<section class="{cls}"', f'<section id="{sid}" class="{cls}"')
body = layout
repl = {
    'KICKER': 'MODE 06 · YOUTUBE ANALYSIS · CAPTURE REVIEW',
    'TITLE': 'Local RAG Knowledge Vault 영상 분석 리포트',
    'SUBTITLE': '입력 Tier C 기준으로 영상 내용을 단정하지 않고, 근거 지도·댓글 신호·콘텐츠 기회·확인 한계를 분리한 YouTube 분석 문서.',
    'META': '<span>profile auto</span><span>layout youtube-analysis</span><span>input tier C</span><span>observed_at 2026-06-07 KST</span><span>no iframe</span>' + generated,
    'VERDICT': verdict,
    'QUESTION_TOC': question_toc,
    'SOURCE_TRUST': source_trust,
    'WATCHING_DECISION': watching,
    'VIDEO_EVIDENCE_MAP': evidence_map,
    'CHAPTER_RETENTION': chapter,
    'COMMENT_SIGNALS': comments,
    'OPPORTUNITY_MATRIX': opportunity,
    'CLAIM_RISK': claim_risk,
    'VIDEO_BLUEPRINT': blueprint,
    'REUSE_PACK': reuse,
    'NEXT_ACTIONS': next_actions,
    'SOURCE_NOTE': source_note,
}
for k, v in repl.items():
    body = body.replace('{{' + k + '}}', v)

base = (ASSETS / 'base.html').read_text(encoding='utf-8')
html_doc = base
head_slots = {
    'TITLE': 'Local RAG Knowledge Vault 영상 분석 리포트',
    'DESCRIPTION': 'youtube_analysis 모드로 Local RAG Knowledge Vault 주제 영상을 입력 Tier C 기준에서 FACT, INFERENCE, UNKNOWN, Evidence Map, Source Limits로 분석한 한국어 HTML 리포트.',
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
    'mode': '06_youtube_analysis',
    'file': str(OUT.relative_to(ROOT)),
    'link': 'http://localhost:8080/output/2026-06-07/adaptive-html-final-sequential-16-modes-20260607_105404/pages/06_youtube_analysis_local_rag_knowledge_vault.html',
    'policy': 'previous HTML body not reused by render script; common generator not used; youtube_analysis layout/recipe/references/templates consulted for this page only',
    'materials_sha256': MATERIAL_HASH,
    'used_materials': [str(p.relative_to(REPO)) for p in MODE_MATERIALS],
    'input_tier': 'C - topic label only; no URL/transcript/comment/metadata supplied',
    'placeholder_mapping': {
        'VERDICT': 'conditional watch decision + vt decision-tree',
        'QUESTION_TOC': 'question-centered nav with real anchors',
        'SOURCE_TRUST': 'Tier C trust snapshot + wg-11 source readiness',
        'WATCHING_DECISION': 'audience decision + wg-14 viewing guide',
        'VIDEO_EVIDENCE_MAP': '5-row mobile-safe evidence map + vt timeline',
        'CHAPTER_RETENTION': 'retention hypotheses + wg-13 verification flow',
        'COMMENT_SIGNALS': 'comment signal wall with sample limits',
        'OPPORTUNITY_MATRIX': 'vt comparison-cards + opportunity grid',
        'CLAIM_RISK': 'vt risk-matrix + quality-gate + mobile-safe table',
        'VIDEO_BLUEPRINT': 'wg-16 video blueprint plan',
        'REUSE_PACK': 'platform reuse grid + vt checklist-flow',
        'NEXT_ACTIONS': 'UNKNOWN promotion plan + source limits gate',
        'SOURCE_NOTE': 'observed_at, input tier, checked/unknown surfaces, no iframe declaration'
    },
    'visual_contract': {
        'layout': 'youtube-analysis.html',
        'numbered_h2_order': 'body-icon body-icon--sm -> num -> title',
        'generated_row': True,
        'lens_strip': True,
        'no_embed': True,
        'fact_inference_unknown': True,
        'source_limits': True,
        'observed_at': '2026-06-07 KST',
        'vt_required': ['timeline'],
        'vt_used': ['timeline', 'risk-matrix', 'quality-gate', 'decision-tree', 'comparison-cards', 'checklist-flow'],
        'wg_used': ['11-weekly-status', '13-annotated-flowchart', '14-feature-explainer', '16-implementation-plan'],
        'evidence_map_rows': 5,
        'table_mobile_safe': 'table-scroll + mobile-card-table where table is used'
    },
    'review_findings_and_fixes': [
        '기존 화면은 구조적으로 통과 수준이었지만, 목표 조건에 맞춰 기존 HTML 본문을 읽지 않는 youtube_analysis 전용 렌더러로 재생성했다.',
        '입력 Tier C를 더 명확히 드러내고 실제 영상 내용·댓글 여론·비공개 analytics를 단정하지 않도록 재작성했다.',
        '질문 중심 목차에 실제 anchor를 부여하고, Evidence Map 5행과 Source Limits를 명시했다.'
    ],
    'skill_patch_candidates_from_mode_review': [
        'youtube_analysis는 입력 tier가 C일 때 영상 내용 FACT를 금지하고 확인 질문 중심 구조로 강등해야 한다.',
        'QUESTION_TOC는 실제 anchor와 연결되어야 완료로 본다.',
        'wg-16 내부 표도 table-scroll 래퍼를 명시해야 현행 table_no_mobile_safe_wrapper 게이트에 안전하다.',
        'Source Limits에는 observed_at, input tier, 확인 표면, iframe/embed/autoplay 미사용 선언을 모두 포함해야 한다.'
    ],
    'next_mode': '07_manual_analysis'
}
(ROOT / 'sources/06_youtube_analysis-visual-contract-evidence.json').write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(OUT)
