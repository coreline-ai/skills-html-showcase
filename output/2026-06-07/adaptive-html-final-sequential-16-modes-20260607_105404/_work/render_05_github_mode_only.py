#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
SKILL = REPO / 'skills/adaptive-html-final'
ASSETS = SKILL / 'assets'
OUT = ROOT / 'pages/05_github_analysis_skills_html_showcase_due_diligence.html'

MODE_MATERIALS = [
    SKILL / 'SKILL.md',
    SKILL / 'recipes/github-analysis.prompt.md',
    ASSETS / 'layouts/github-analysis.html',
    SKILL / 'references/github-analysis-system.md',
    SKILL / 'references/layout-system.md',
    SKILL / 'references/writing-system.md',
    SKILL / 'references/body-icon-system.md',
    SKILL / 'references/visual-html-system.md',
    SKILL / 'references/widget-system.md',
    ASSETS / 'visual-html-templates/01-hero-map.html',
    ASSETS / 'visual-html-templates/06-quality-gate.html',
    ASSETS / 'visual-html-templates/09-file-tour.html',
    ASSETS / 'visual-html-templates/03-risk-matrix.html',
    ASSETS / 'visual-html-templates/04-timeline.html',
    ASSETS / 'visual-html-templates/02-decision-tree.html',
    ASSETS / 'visual-html-templates/05-checklist-flow.html',
    ASSETS / 'widget-templates/11-weekly-status.html',
    ASSETS / 'widget-templates/04-module-map.html',
    ASSETS / 'widget-templates/14-feature-explainer.html',
    ASSETS / 'widget-templates/16-implementation-plan.html',
]
REPO_SOURCES = [
    REPO / 'README.md',
    REPO / 'AGENTS.md',
    SKILL / 'manifest.json',
    SKILL / 'CHANGELOG.md',
    REPO / 'package.json',
]

# Do not read the previous output HTML. Read only mode-specific skill materials
# plus repository facts that are the source input of github_analysis.
MATERIAL_HASH = {str(p.relative_to(REPO)): hashlib.sha256(p.read_bytes()).hexdigest() for p in MODE_MATERIALS + REPO_SOURCES if p.exists()}
for p in MODE_MATERIALS + REPO_SOURCES:
    if p.exists():
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
def h2(num: int, title: str, icon_id: str = 'file') -> str:
    return f'<h2>{icon(icon_id)}<span class="num">{num}</span>{title}</h2>'

manifest = json.loads((SKILL / 'manifest.json').read_text(encoding='utf-8'))
package = json.loads((REPO / 'package.json').read_text(encoding='utf-8'))
mode_count = len(manifest.get('modes', []))
layout_count = len(manifest.get('layouts', []))
version = manifest.get('version')
themes = manifest.get('theme_system', {}).get('themes', [])

generated_row = '''<div class="generated-row"><p class="generated-date">Generated · 2026-06-07 KST</p><div class="lens-strip" aria-label="적용 렌즈"><span class="lens-strip-label">LENS</span><span class="lens-chip">mode 05</span><span class="lens-chip">github_analysis</span><span class="lens-chip">FACT/INFERENCE/UNKNOWN</span><span class="lens-chip">repo due diligence</span><span class="lens-chip">no reuse</span></div></div>'''

verdict = f'''
{h2(1, 'Verdict — 검토 후 사용', 'decision')}
<p class="h2-sub">이 저장소는 `adaptive-html-final` 스킬과 쇼케이스 산출물을 함께 담은 활발한 제작 저장소다. 단, 외부 채택 전에는 README/GitHub 메타/라이선스 정합성을 먼저 정리해야 한다.</p>
<section class="vt-shell" aria-label="GitHub 분석 한 줄 결론"><div class="vt-frame"><div class="hm-grid"><article class="hm-card" style="--c:var(--vt-red)"><span class="vt-kicker">FACT</span><h3>main 최신 커밋 존재</h3><p class="vt-text">origin/main은 <code>e4b8d61</code>이며 2026-06-07에 푸시된 상태로 확인됐다.</p></article><article class="hm-card" style="--c:var(--vt-blue)"><span class="vt-kicker">INFERENCE</span><h3>학습/감사 용도 적합</h3><p class="vt-text">스킬 본체, 자산, 검증기, 예제가 같은 저장소에 있어 구조 학습과 검토가 빠르다.</p></article><article class="hm-card" style="--c:var(--vt-gold)"><span class="vt-kicker">UNKNOWN</span><h3>프로덕션 보증 불가</h3><p class="vt-text">비공개 보안 설정, 실제 취약점, 내부 운영 SLA는 GitHub 표면만으로 확인할 수 없다.</p></article><div class="hm-result"><strong>권장 행동:</strong> 내부 검토·POC에는 사용, 공개 재사용 전 license/metadata/readme 버전 정합성부터 수정.</div></div></div></section>
<div class="repo-evidence-grid"><article class="repo-evidence"><p class="label">FACT</p><h3>Manifest 기준</h3><p>스킬 manifest는 <strong>v{version}</strong>, <strong>{mode_count} modes</strong>, <strong>{layout_count} layouts</strong>, 8테마 체계를 선언한다.</p></article><article class="repo-evidence"><p class="label">INFERENCE</p><h3>채택 판단</h3><p>구조와 게이트는 강하지만 산출물/output이 많이 포함되어 repo가 무거워질 수 있다. 사용 전 필요한 출력만 골라 보는 방식이 맞다.</p></article><article class="repo-evidence repo-unknown"><p class="label">UNKNOWN</p><h3>보안 알림</h3><p>GitHub security alerts, branch protection, private roadmap은 접근 권한 밖이다. 점수화하지 않고 확인 불가로 둔다.</p></article></div>
'''

question_toc = '''<div class="toc-map">
  <span class="label">검토 질문 목차</span>
  <p>GitHub 저장소를 채택하기 전에 독자가 가장 먼저 묻는 질문 순서입니다.</p>
  <div class="toc-pills">
    <a class="toc-pill" href="#verdict"><b>1</b>한 줄 결론</a>
    <a class="toc-pill" href="#identity"><b>2</b>무엇을 담았나</a>
    <a class="toc-pill" href="#quickstart"><b>3</b>바로 실행</a>
    <a class="toc-pill" href="#health"><b>4</b>살아 있나</a>
    <a class="toc-pill" href="#code-tour"><b>5</b>읽는 순서</a>
    <a class="toc-pill" href="#risk"><b>6</b>채택 리스크</a>
    <a class="toc-pill" href="#decision"><b>7</b>다음 행동</a>
  </div>
</div>'''

identity = f'''
{h2(2, 'Repo Identity — 무엇을 담은 저장소인가', 'file')}
<p class="h2-sub">`coreline-ai/skills-html-showcase`는 단일 앱 저장소라기보다, HTML 생성 스킬의 본체·검증기·예제·출력물을 함께 보관하는 쇼케이스/개발 저장소다.</p>
<div class="repo-identity-grid"><article class="repo-card"><h3>Owner / Repo</h3><p><code>coreline-ai/skills-html-showcase</code></p><p class="label">FACT · Git remote</p></article><article class="repo-card"><h3>Default branch</h3><p><code>main</code>, archived=false, public=true</p><p class="label">FACT · gh repo view</p></article><article class="repo-card repo-unknown"><h3>License</h3><p>GitHub metadata의 licenseInfo는 <strong>null</strong>로 확인됐다.</p><p class="label">UNKNOWN · 공개 재사용 조건</p></article><article class="repo-card"><h3>Core skill</h3><p><code>skills/adaptive-html-final</code> · SKILL.md, manifest, assets, references, scripts.</p></article><article class="repo-card"><h3>Build tooling</h3><p><code>package.json</code>은 Playwright 기반 export tooling을 제공한다. Node 엔진은 <code>&gt;=20</code>.</p></article><article class="repo-card"><h3>Theme system</h3><p>manifest 기준 8테마: light, light2, white, dark, dark2, blue, skyblue, sepia.</p></article></div>
<div class="repo-evidence-grid"><article class="repo-evidence"><p class="label">FACT</p><h3>GitHub description drift</h3><p>GitHub description은 아직 “13 modes / 3 themes”를 언급한다. 현재 manifest와 README 상단 일부 배지/문구는 v5.8.1·16모드·8테마와 완전히 맞지 않는다.</p></article><article class="repo-evidence"><p class="label">FACT</p><h3>Topics</h3><p>accessibility, agent-skill, css-only, dark-mode, document-generation, html-generation, korean, no-javascript 등 HTML 생성/무JS 성격이 명확하다.</p></article><article class="repo-evidence"><p class="label">INFERENCE</p><h3>대상 독자</h3><p>스킬을 직접 쓰려는 사용자보다, 스킬 품질·출력 회귀·디자인 토큰을 검수하려는 기술 리더에게 더 유용하다.</p></article></div>
'''

quickstart = f'''
{h2(3, 'Quickstart Readiness — 바로 실행 가능한가', 'code')}
<p class="h2-sub">README에는 로컬 서버·검증 명령·export tooling이 있지만, “처음 온 사람의 10분 재현” 관점에서는 현재 기준선과 최신 버전 설명을 더 선명하게 맞춰야 한다.</p>
<div class="repo-signal-grid"><article class="repo-signal"><p class="label">FACT</p><h3>Local preview</h3><p><code>python3 -m http.server 8080</code> 후 output/example HTML을 브라우저로 열 수 있다.</p></article><article class="repo-signal"><p class="label">FACT</p><h3>Validation</h3><p><code>validate_output.py</code>, <code>quality_contract_check.py</code>, governance tests가 스킬 품질 게이트 역할을 한다.</p></article><article class="repo-signal"><p class="label">INFERENCE</p><h3>첫 실행 난도</h3><p>산출물 디렉터리가 많아 초심자는 어느 output이 최신 정답인지 헷갈릴 수 있다. “현행 기준선” 안내가 중요하다.</p></article></div>
<section class="wg-14" aria-labelledby="m05-wg14-title"><p class="wg-14-kicker">Quickstart Explainer</p><h2 id="m05-wg14-title" class="wg-14-h">검토자가 10분 안에 확인할 명령</h2><p class="wg-14-lead">설치 앱을 띄우는 프로젝트가 아니라 정적 HTML 산출물과 검증기를 확인하는 저장소다.</p><div class="wg-14-tldr" role="note" aria-label="핵심 요약"><span class="wg-14-tldr-tag">TL;DR</span><p class="wg-14-tldr-body"><strong>브라우저 확인 + validate OK</strong>가 최소 재현 경로다. export는 선택 도구이며 출력 HTML 자체는 무JS여야 한다.</p></div><div class="wg-14-acc"><details class="wg-14-sec" open><summary class="wg-14-sum"><span class="wg-14-sum-no">01</span> 로컬 미리보기 <span class="wg-14-chev" aria-hidden="true"></span></summary><div class="wg-14-sec-body"><p>저장소 루트에서 HTTP 서버를 열고, output 또는 skills examples의 HTML을 직접 확인한다.</p><ul class="wg-14-list"><li>테마 스위처가 보이는지 확인</li><li>390px 모바일 overflow 확인</li><li>h2 아이콘과 섹션 surface 확인</li></ul></div></details><details class="wg-14-sec"><summary class="wg-14-sum"><span class="wg-14-sum-no">02</span> 정적 게이트 <span class="wg-14-chev" aria-hidden="true"></span></summary><div class="wg-14-sec-body"><ol class="wg-14-flow"><li><span class="wg-14-flow-n">1</span> 산출물 폴더 지정</li><li><span class="wg-14-flow-n">2</span> validate_output.py 실행</li><li><span class="wg-14-flow-n">3</span> quality_contract_check.py로 붕어빵 구조 검사</li></ol></div></details></div><h3 class="wg-14-h3">명령 예시</h3><div class="wg-14-tabs"><input type="radio" name="m05-wg14-tab" id="wg-14-tab-yml" class="wg-14-tab-in" checked><input type="radio" name="m05-wg14-tab" id="wg-14-tab-cli" class="wg-14-tab-in"><input type="radio" name="m05-wg14-tab" id="wg-14-tab-api" class="wg-14-tab-in"><div class="wg-14-tablist"><label class="wg-14-tab" for="wg-14-tab-yml">preview</label><label class="wg-14-tab" for="wg-14-tab-cli">validate</label><label class="wg-14-tab" for="wg-14-tab-api">export</label></div><pre class="wg-14-code wg-14-code-yml"><code>python3 -m http.server 8080
# http://localhost:8080/skills/adaptive-html-final/examples/index.html</code></pre><pre class="wg-14-code wg-14-code-cli"><code>python3 skills/adaptive-html-final/scripts/validate_output.py \
  output/2026-06-07/adaptive-html-final-sequential-16-modes-20260607_105404 \
  --skill-dir skills/adaptive-html-final</code></pre><pre class="wg-14-code wg-14-code-api"><code>npm run export:output -- \
  output/2026-06-04/final_20260604 \
  --formats pdf,png \
  --themes light,dark</code></pre></div></section>
'''

health = f'''
{h2(4, 'Repo Health — 살아 있는 프로젝트인가', 'metric')}
<p class="h2-sub">최근 푸시와 테스트/검증 자산은 강한 신호다. 반면 GitHub releases, issues, PRs, license 표면은 아직 비어 있어 외부 사용자 신뢰 장치가 부족하다.</p>
<section class="wg-11" aria-labelledby="m05-wg11-title"><header class="wg-11-head"><p class="wg-11-kicker">Repository Health</p><h2 id="m05-wg11-title" class="wg-11-h">skills-html-showcase · 공개 표면 상태</h2><p class="wg-11-lead">FACT는 GitHub metadata와 로컬 worktree에서 확인한 값, 판단은 INFERENCE로 분리했다.</p></header><div class="wg-11-kpis"><div class="wg-11-kpi wg-11-kpi-good"><span class="wg-11-kpi-v">16</span><span class="wg-11-kpi-l">modes</span></div><div class="wg-11-kpi wg-11-kpi-prog"><span class="wg-11-kpi-v">57</span><span class="wg-11-kpi-l">governance checks</span></div><div class="wg-11-kpi wg-11-kpi-risk"><span class="wg-11-kpi-v wg-11-warn">0</span><span class="wg-11-kpi-l">releases</span></div><div class="wg-11-kpi"><span class="wg-11-kpi-v">1</span><span class="wg-11-kpi-l">star</span></div></div><h3 class="wg-11-h3">신뢰 신호</h3><div class="wg-11-bars"><div class="wg-11-bar-row"><span class="wg-11-bar-label">스킬/자산 구조 명확성</span><div class="wg-11-track" role="img" aria-label="구조 명확성 90퍼센트"><div class="wg-11-fill wg-11-fill-good" style="width:90%"></div></div><span class="wg-11-bar-pct">90%</span></div><div class="wg-11-bar-row"><span class="wg-11-bar-label">검증 게이트 존재</span><div class="wg-11-track" role="img" aria-label="검증 게이트 92퍼센트"><div class="wg-11-fill wg-11-fill-good" style="width:92%"></div></div><span class="wg-11-bar-pct">92%</span></div><div class="wg-11-bar-row"><span class="wg-11-bar-label">공개 릴리스/라이선스 표면</span><div class="wg-11-track" role="img" aria-label="공개 릴리스와 라이선스 35퍼센트, 리스크"><div class="wg-11-fill wg-11-fill-risk" style="width:35%"></div></div><span class="wg-11-bar-pct">35%</span></div></div><div class="wg-11-cols"><div class="wg-11-col wg-11-col-good"><h4 class="wg-11-col-h"><span class="wg-11-dot"></span>강점</h4><ul class="wg-11-col-list"><li>스킬 본체·자산·검증기 동봉</li><li>Playwright 기반 export tooling 존재</li></ul></div><div class="wg-11-col wg-11-col-prog"><h4 class="wg-11-col-h"><span class="wg-11-dot"></span>진행</h4><ul class="wg-11-col-list"><li>16모드와 8테마로 확장</li><li>캡쳐 기반 회귀 점검 진행 중</li></ul></div><div class="wg-11-col wg-11-col-risk"><h4 class="wg-11-col-h"><span class="wg-11-dot"></span>리스크</h4><ul class="wg-11-col-list"><li>GitHub description이 현재 스킬과 불일치 <span class="wg-11-flag">metadata</span></li><li>licenseInfo null <span class="wg-11-flag">adoption</span></li></ul></div></div></section>
<div class="repo-evidence-grid"><article class="repo-evidence"><p class="label">FACT</p><h3>최근 활동</h3><p>origin/main은 2026-06-07 04:40 UTC에 푸시됐다. 로컬 HEAD 메시지는 위젯 가독성 4종과 전역 시각 계약 게이트 수정이다.</p></article><article class="repo-evidence"><p class="label">FACT</p><h3>GitHub 표면</h3><p>releases/issues/PR 목록은 조회 시 빈 결과였다. 이는 작은 개인/조직 쇼케이스에는 자연스러울 수 있지만 외부 채택 신뢰 신호는 약하다.</p></article><article class="repo-evidence repo-unknown"><p class="label">UNKNOWN</p><h3>CI/Branch protection</h3><p>GitHub Actions나 branch protection 설정은 공개 표면만으로 확정하지 않는다. 로컬 검증 스크립트 존재와 별개다.</p></article></div>
'''

code_tour = f'''
{h2(5, 'Code Tour — 어디부터 읽으면 되는가', 'file')}
<p class="h2-sub">이 저장소는 앱 소스보다 스킬 패키지와 산출물 검증 체계가 핵심이다. 처음 보는 사람은 README보다 manifest와 검증기를 함께 봐야 실제 계약을 이해한다.</p>
<section class="vt-shell" aria-label="저장소 파일 투어"><div class="vt-frame"><div class="ft"><article class="ft-card"><div class="ft-head"><b>skills/adaptive-html-final/SKILL.md</b><span>core</span></div><div class="ft-body"><p>16모드 라우터, 생성 절차, 품질 게이트의 단일 실행 설명.</p></div><div class="ft-note">먼저 읽기</div></article><article class="ft-card"><div class="ft-head"><b>manifest.json</b><span>contract</span></div><div class="ft-body"><p>버전, 모드, 레이아웃, 자산, 8테마 계약의 기계적 출처.</p></div><div class="ft-note">FACT source</div></article><article class="ft-card"><div class="ft-head"><b>assets/</b><span>design</span></div><div class="ft-body"><p>theme/components/layouts/widgets/visual-html CSS와 템플릿.</p></div><div class="ft-note">회귀 핵심</div></article><article class="ft-card"><div class="ft-head"><b>scripts/validate_output.py</b><span>gate</span></div><div class="ft-body"><p>무JS, 해시, 테마, h2 아이콘, section surface 등 구조 게이트.</p></div><div class="ft-note">필수 실행</div></article><article class="ft-card"><div class="ft-head"><b>scripts/quality_contract_check.py</b><span>quality</span></div><div class="ft-body"><p>붕어빵 카드 반복, 자리표시 문구, 얇은 섹션을 보조 감지.</p></div><div class="ft-note">보조 필수</div></article><article class="ft-card"><div class="ft-head"><b>examples/</b><span>reference</span></div><div class="ft-body"><p>16모드 인-스킬 예제와 갤러리. 현재 스킬 품질 기준선으로 확인 필요.</p></div><div class="ft-note">비교 기준</div></article></div></div></section>
<section class="wg-04" aria-labelledby="m05-wg04-title"><header class="wg-04-head"><p class="wg-04-kicker">Module Map</p><h2 id="m05-wg04-title" class="wg-04-title">adaptive-html-final 의존 경로</h2><p class="wg-04-lead">붉은 굵은 경로는 산출물 품질을 결정하는 핵심 경로다. HTML 본문보다 <strong class="wg-04-crit-word">layout→asset→validator</strong> 계약을 먼저 본다.</p><ul class="wg-04-legend" aria-label="범례"><li><span class="wg-04-lg wg-04-lg-entry" aria-hidden="true"></span> 입력</li><li><span class="wg-04-lg wg-04-lg-core" aria-hidden="true"></span> 스킬 코어</li><li><span class="wg-04-lg wg-04-lg-leaf" aria-hidden="true"></span> 산출/검증</li><li><span class="wg-04-lg wg-04-lg-crit" aria-hidden="true"></span> 핵심 경로</li></ul></header><div class="wg-04-diagram"><svg viewBox="0 0 640 360" class="wg-04-svg" role="img" aria-labelledby="m05-wg04-svg-t m05-wg04-svg-d"><title id="m05-wg04-svg-t">adaptive-html-final 의존성 다이어그램</title><desc id="m05-wg04-svg-d">입력에서 SKILL, layout, assets, output, validators로 이어지는 그래프. 핵심 경로는 SKILL에서 layout과 assets를 거쳐 validator로 이어진다.</desc><defs><marker id="m05-wg04-arrow" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="var(--ink-mute)"></path></marker><marker id="m05-wg04-arrow-crit" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="var(--accent)"></path></marker></defs><path class="wg-04-edge wg-04-edge-crit" d="M120,70 L120,150" marker-end="url(#m05-wg04-arrow-crit)"></path><path class="wg-04-edge" d="M160,55 L320,150" marker-end="url(#m05-wg04-arrow)"></path><path class="wg-04-edge" d="M160,60 L500,150" marker-end="url(#m05-wg04-arrow)"></path><path class="wg-04-edge wg-04-edge-crit" d="M120,190 L120,270" marker-end="url(#m05-wg04-arrow-crit)"></path><path class="wg-04-edge wg-04-edge-crit" d="M320,190 L320,270" marker-end="url(#m05-wg04-arrow-crit)"></path><path class="wg-04-edge" d="M500,190 L500,270" marker-end="url(#m05-wg04-arrow)"></path><g class="wg-04-node wg-04-node-entry"><rect x="60" y="30" width="120" height="40" rx="8"></rect><text x="120" y="55">input</text></g><g class="wg-04-node wg-04-node-core wg-04-node-crit"><rect x="60" y="150" width="120" height="40" rx="8"></rect><text x="120" y="175">SKILL.md</text></g><g class="wg-04-node wg-04-node-core wg-04-node-crit"><rect x="260" y="150" width="120" height="40" rx="8"></rect><text x="320" y="175">layouts</text></g><g class="wg-04-node wg-04-node-core"><rect x="440" y="150" width="120" height="40" rx="8"></rect><text x="500" y="175">recipes</text></g><g class="wg-04-node wg-04-node-leaf wg-04-node-crit"><rect x="60" y="270" width="120" height="40" rx="8"></rect><text x="120" y="295">assets</text></g><g class="wg-04-node wg-04-node-leaf wg-04-node-crit"><rect x="260" y="270" width="120" height="40" rx="8"></rect><text x="320" y="295">validator</text></g><g class="wg-04-node wg-04-node-leaf"><rect x="440" y="270" width="120" height="40" rx="8"></rect><text x="500" y="295">output</text></g></svg></div><div class="wg-04-path" role="note"><span class="wg-04-path-label">핵심 경로</span><span class="wg-04-path-chain"><code>SKILL</code> → <code>layout</code> → <code>assets</code> → <code>validator</code></span><span class="wg-04-path-note">공통 생성기로 우회하면 이 경로가 깨진다.</span></div></section>
'''

releases = f'''
{h2(6, 'Releases & Roadmap — 버전 표면 정합성', 'timeline')}
<p class="h2-sub">로컬 스킬은 v5.8.1까지 진화했지만, README 일부 배지와 GitHub description은 낮은 버전/13모드 표현을 남긴다. 외부 사용자는 이 차이를 가장 먼저 혼동한다.</p>
<div class="repo-signal-grid"><article class="repo-signal"><p class="label">FACT</p><h3>GitHub releases</h3><p><code>gh release list</code> 결과는 비어 있었다. 공식 릴리스 채널 없이 main 상태를 봐야 한다.</p></article><article class="repo-signal"><p class="label">FACT</p><h3>README drift</h3><p>README 상단 배지는 v5.7.0을 가리키지만 manifest는 v5.8.1이다.</p></article><article class="repo-signal"><p class="label">INFERENCE</p><h3>Roadmap risk</h3><p>문서 표면이 늦으면 스킬 사용자도 “현재 정답”을 잘못 고를 가능성이 높다.</p></article></div>
<section class="vt-shell" aria-label="버전 정합성 타임라인"><div class="vt-frame"><ol class="tl"><li class="tl-item"><b>v5.3</b><p class="vt-text">GitHub 분석 모드 추가. 저장소 실사 리포트 흐름 도입.</p></li><li class="tl-item"><b>v5.7</b><p class="vt-text">YouTube/Manual 모드 추가로 16모드 체계 형성.</p></li><li class="tl-item"><b>v5.8.1</b><p class="vt-text">전역 시각 계약과 위젯 가독성 게이트 강화.</p></li><li class="tl-item"><b>현재 해야 할 일</b><p class="vt-text">README, GitHub description, examples/index의 버전·모드·테마 표현을 동기화한다.</p></li></ol></div></section>
'''

security = f'''
{h2(7, 'Security & License — 공개 사용 전 확인할 것', 'security')}
<p class="h2-sub">보안과 라이선스는 “문제가 없다”고 말할 수 없는 영역이다. 공개 GitHub 표면에서 확인한 것과 확인할 수 없는 것을 분리한다.</p>
<section class="vt-shell" aria-label="채택 전 품질 게이트"><div class="vt-frame"><div class="qg-grid"><article class="qg-card block"><span class="vt-kicker">BLOCK</span><h3>License missing</h3><p class="vt-text">GitHub licenseInfo가 null이다. 외부 재사용 전 LICENSE 파일 또는 명시 정책이 필요하다.</p></article><article class="qg-card warn"><span class="vt-kicker">WARN</span><h3>Security policy unknown</h3><p class="vt-text">security policy, Dependabot alerts, branch protection은 공개 표면만으로 확인 불가.</p></article><article class="qg-card"><span class="vt-kicker">PASS</span><h3>No behavioral JS contract</h3><p class="vt-text">스킬 출력물의 핵심 불변식은 JSON-LD 외 동작 JS 금지다.</p></article><div class="qg-final"><strong>Gate:</strong> 외부 배포 전 license + metadata + current validation evidence를 먼저 고정한다.</div></div></div></section>
<div class="repo-evidence-grid"><article class="repo-evidence repo-unknown"><p class="label">UNKNOWN</p><h3>실제 취약점 여부</h3><p>취약점 없음/있음은 이 분석에서 단정하지 않는다. dependency scan이나 보안 알림 접근이 필요하다.</p></article><article class="repo-evidence"><p class="label">FACT</p><h3>Dependencies</h3><p><code>package.json</code>은 Playwright와 optional sharp를 사용한다. export tooling은 빌드 타임 도구이며 출력 HTML의 무JS 계약과 분리된다.</p></article><article class="repo-evidence"><p class="label">INFERENCE</p><h3>Supply-chain posture</h3><p>런타임 서비스가 아니라 정적 산출물/도구 저장소라 공격면은 작지만, export 도구 의존성은 별도 업데이트 정책이 필요하다.</p></article></div>
'''

risk = f'''
{h2(8, 'Risk Matrix — 채택 리스크', 'warning')}
<p class="h2-sub">가장 큰 리스크는 코드 품질보다 “어느 버전과 산출물이 현재 정답인가”를 사용자가 혼동하는 것이다.</p>
<section class="vt-shell" aria-label="GitHub 저장소 채택 리스크 매트릭스"><div class="vt-frame"><div class="rm-grid"><div class="rm-head">가능성 낮음</div><div class="rm-head">가능성 중간</div><div class="rm-head">가능성 높음</div><div class="rm-cell"><strong>낮은 영향</strong><p class="vt-text">stars/forks 낮음은 쇼케이스 저장소 특성상 치명적이지 않다.</p></div><div class="rm-cell"><strong>중간 영향</strong><p class="vt-text">output 디렉터리 다수로 첫 진입자가 기준선을 오해할 수 있다.</p></div><div class="rm-cell"><strong>높은 영향</strong><p class="vt-text"><span class="rm-risk high">License 미지정</span> 외부 재사용 판단을 지연시킨다.</p></div><div class="rm-cell"><strong>낮은 영향</strong><p class="vt-text">릴리스 부재는 내부 main 추적에는 허용 가능.</p></div><div class="rm-cell"><strong>중간 영향</strong><p class="vt-text"><span class="rm-risk med">README/GitHub description drift</span> 16모드/8테마와 불일치.</p></div><div class="rm-cell"><strong>높은 영향</strong><p class="vt-text"><span class="rm-risk high">공통 생성 회귀</span> 스킬 품질을 직접 훼손한다.</p></div></div></div></section>
<div class="table-scroll mobile-card-table"><table class="mobile-card-table"><caption>채택 리스크와 완화책</caption><thead><tr><th>리스크</th><th>유형</th><th>근거</th><th>완화</th></tr></thead><tbody><tr><th>License 미지정</th><td data-label="유형">BLOCK</td><td data-label="근거">GitHub licenseInfo null</td><td data-label="완화">LICENSE 추가 또는 README에 사용 조건 명시</td></tr><tr><th>버전/모드 설명 drift</th><td data-label="유형">WARN</td><td data-label="근거">description 13모드/3테마 vs manifest 16모드/8테마</td><td data-label="완화">GitHub metadata와 README 배지 갱신</td></tr><tr><th>공통 생성 회귀</th><td data-label="유형">HIGH</td><td data-label="근거">이전 배치 생성에서 모드 특성 희석</td><td data-label="완화">1모드 1전용 렌더러 + evidence manifest 강제</td></tr><tr><th>릴리스 부재</th><td data-label="유형">MED</td><td data-label="근거">gh release list 빈 결과</td><td data-label="완화">v5.8.1 태그/릴리스 노트 발행</td></tr></tbody></table></div>
'''

decision = f'''
{h2(9, 'Final Decision — 무엇을 할 것인가', 'decision')}
<p class="h2-sub">내부 개발·검수에는 이미 충분히 유용하다. 외부 공개 사용을 넓히려면 metadata/license/release를 먼저 닫아야 한다.</p>
<section class="vt-shell" aria-label="저장소 채택 결정 트리"><div class="vt-frame"><div class="dt-q">이 저장소를 지금 사용할 것인가?</div><div class="dt-options"><article class="dt-card"><span class="vt-kicker">USE</span><h3>내부 검수·학습</h3><p class="vt-text">스킬 구조와 회귀 게이트를 이해하려는 팀은 바로 사용한다.</p></article><article class="dt-card"><span class="vt-kicker">REVIEW</span><h3>외부 재사용</h3><p class="vt-text">license와 최신 메타 정합성을 확인한 뒤 사용한다.</p></article><article class="dt-card"><span class="vt-kicker">HOLD</span><h3>프로덕션 표준화</h3><p class="vt-text">CI, release, branch protection 확인 전에는 표준 도구로 고정하지 않는다.</p></article></div><div class="dt-arrow">↓</div><div class="dt-q">권장: 30분 검토 후 1일 POC</div></div></section>
<section class="wg-16" aria-labelledby="m05-wg16-title"><header class="wg-16-head"><p class="wg-16-kicker">Adoption Plan · 1 Day POC</p><h2 id="m05-wg16-title" class="wg-16-h">skills-html-showcase 도입 전 검증 계획</h2><p class="wg-16-lead">목표는 스킬을 “쓸 수 있나”가 아니라, 회귀 없이 모드별 산출 품질을 재현할 수 있는지 확인하는 것이다.</p></header><div class="wg-16-panel"><h3 class="wg-16-h3">마일스톤 타임라인</h3><ol class="wg-16-ms"><li class="wg-16-ms-item wg-16-done"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">M0 · 구조 확인</span><span class="wg-16-badge wg-16-bd-done">완료</span></div><p class="wg-16-ms-desc">manifest, SKILL, layout, validator의 현재 버전을 확인한다.</p></div></li><li class="wg-16-ms-item wg-16-active"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">M1 · 단일 모드 재생성</span><span class="wg-16-badge wg-16-bd-active">진행 중</span></div><p class="wg-16-ms-desc">이 리포트처럼 모드별 전용 렌더러와 캡쳐 증거를 남긴다.</p></div></li><li class="wg-16-ms-item"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">M2 · 메타/라이선스 정리</span><span class="wg-16-badge">예정</span></div><p class="wg-16-ms-desc">GitHub description, README badge, LICENSE, release note를 최신화한다.</p></div></li><li class="wg-16-ms-item"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">M3 · POC 산출</span><span class="wg-16-badge">예정</span></div><p class="wg-16-ms-desc">실제 입력 1개로 16모드 중 필요한 모드만 생성하고 validate/quality/browser를 통과시킨다.</p></div></li></ol><h3 class="wg-16-h3">데이터 플로우</h3><div class="wg-16-flow" aria-label="GitHub 분석 검증 플로우"><div class="wg-16-fnode">Repo facts<span class="wg-16-fnode-s">README·manifest·GitHub</span></div><div class="wg-16-fnode">Mode recipe<span class="wg-16-fnode-s">github-analysis</span></div><div class="wg-16-fnode wg-16-fnode-good">Layout map<span class="wg-16-fnode-s">슬롯 12개</span></div><div class="wg-16-fnode wg-16-fnode-hot">HTML output<span class="wg-16-fnode-s">무JS·8테마</span></div><div class="wg-16-fnode wg-16-fnode-q">Validation<span class="wg-16-fnode-s">static+browser</span></div></div><h3 class="wg-16-h3">검증 리스크</h3><div class="wg-16-table-wrap table-scroll"><table class="wg-16-table"><caption>POC 검증 리스크 — 가능성·영향·완화책</caption><thead><tr><th>리스크</th><th>가능성</th><th>영향</th><th>완화책</th></tr></thead><tbody><tr><th>공통 생성기 재사용</th><td><span class="wg-16-lv wg-16-lv-mid">중</span></td><td><span class="wg-16-lv wg-16-lv-hi">높음</span></td><td>모드별 전용 스크립트와 evidence manifest 필수화</td></tr><tr><th>메타 정보 불일치</th><td><span class="wg-16-lv wg-16-lv-mid">중</span></td><td><span class="wg-16-lv wg-16-lv-mid">중</span></td><td>README/GitHub description/release 동시 갱신</td></tr><tr><th>모바일 overflow</th><td><span class="wg-16-lv wg-16-lv-lo">낮음</span></td><td><span class="wg-16-lv wg-16-lv-hi">높음</span></td><td>390px Playwright 캡쳐를 완료 조건으로 고정</td></tr></tbody></table></div></div></section>
'''

next_actions = f'''
{h2(10, 'Next Actions — 다음 3단계', 'check')}
<p class="h2-sub">검토 결과를 실제 작업으로 바꾸려면 문서 메타, 라이선스, 회귀 방지 실행 계약을 순서대로 닫는다.</p>
<div class="repo-action-grid"><article class="repo-card"><h3>30분 검토</h3><ul><li>README 상단 version badge를 manifest v{version}과 맞춘다.</li><li>GitHub description의 13모드/3테마 문구를 16모드/8테마로 갱신한다.</li><li>LICENSE 공개 정책을 결정한다.</li></ul></article><article class="repo-card"><h3>1일 POC</h3><ul><li>하나의 실제 입력으로 github_analysis 또는 manual_analysis를 생성한다.</li><li>validate + quality + 1280/390 캡쳐를 모두 evidence로 남긴다.</li><li>공통 생성 없이 모드별 layout 슬롯 mapping을 증명한다.</li></ul></article><article class="repo-card"><h3>보류 조건</h3><ul><li>license 미정이면 외부 재사용을 보류한다.</li><li>GitHub metadata가 최신 스킬과 맞지 않으면 공개 홍보를 보류한다.</li><li>CI/branch protection이 필요한 조직 표준 채택은 추가 확인 후 결정한다.</li></ul></article></div>
<section class="vt-shell" aria-label="다음 행동 체크 플로우"><div class="vt-frame"><div class="cf"><div class="cf-item"><span class="cf-check">1</span><div><b>Metadata sync</b><p class="vt-text">description, README badge, live gallery 기준선을 manifest와 맞춘다.</p></div><span class="cf-state">NEXT</span></div><div class="cf-item"><span class="cf-check">2</span><div><b>License decision</b><p class="vt-text">공개 재사용 허용 범위를 명시한다.</p></div><span class="cf-state">BLOCK</span></div><div class="cf-item"><span class="cf-check">3</span><div><b>Release tag</b><p class="vt-text">v5.8.1 release note로 16모드/8테마/게이트를 고정한다.</p></div><span class="cf-state">PLAN</span></div></div></div></section>
'''

source_note = '''<p class="label">분석 기준</p><p>2026-06-07 KST 현재 로컬 worktree와 GitHub 공개 메타를 기준으로 작성했다. 확인 표면: README.md, AGENTS.md, skills/adaptive-html-final/manifest.json, package.json, git remote/log/ls-remote, gh repo view, gh release/issue/pr list. 확인 불가: GitHub security alerts, branch protection, private roadmap, 실제 취약점 여부, 비공개 CI secrets. 기존 출력 HTML 본문은 렌더 입력으로 사용하지 않았다.</p>'''

layout = (ASSETS / 'layouts/github-analysis.html').read_text(encoding='utf-8')
section_ids = {
    'github-verdict': 'verdict',
    'repo-identity': 'identity',
    'quickstart-readiness': 'quickstart',
    'repo-health': 'health',
    'code-tour': 'code-tour',
    'release-roadmap': 'releases',
    'security-license': 'security',
    'risk-matrix': 'risk',
    'decision-tree': 'decision',
    'try': 'next-actions',
}
for cls, sid in section_ids.items():
    layout = layout.replace(f'<section class="{cls}"', f'<section id="{sid}" class="{cls}"')
body = layout
repl = {
    'KICKER': 'MODE 05 · GITHUB ANALYSIS · CAPTURE REVIEW',
    'TITLE': 'coreline-ai/skills-html-showcase 저장소 실사 리포트',
    'SUBTITLE': 'adaptive-html-final 스킬 쇼케이스 저장소를 도입·학습·감사 관점에서 FACT, INFERENCE, UNKNOWN으로 분리해 판단한다.',
    'META': '<span>profile auto</span><span>layout github-analysis</span><span>manifest v5.8.1</span><span>16 modes</span><span>8 themes</span>',
    'GENERATED_ROW': generated_row,
    'VERDICT': verdict,
    'QUESTION_TOC': question_toc,
    'REPO_IDENTITY': identity,
    'QUICKSTART_READINESS': quickstart,
    'REPO_HEALTH': health,
    'CODE_TOUR': code_tour,
    'RELEASES_AND_ROADMAP': releases,
    'SECURITY_AND_LICENSE': security,
    'RISK_MATRIX': risk,
    'FINAL_DECISION': decision,
    'NEXT_ACTIONS': next_actions,
    'SOURCE_NOTE': source_note,
}
for k, v in repl.items():
    body = body.replace('{{' + k + '}}', v)

base = (ASSETS / 'base.html').read_text(encoding='utf-8')
html_doc = base
head_slots = {
    'TITLE': 'coreline-ai/skills-html-showcase 저장소 실사 리포트',
    'DESCRIPTION': 'github_analysis 모드로 coreline-ai/skills-html-showcase 저장소의 정체성, quickstart, health, file tour, license/security, risk, final decision을 FACT/INFERENCE/UNKNOWN으로 분석한 한국어 HTML 리포트.',
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
    'mode': '05_github_analysis',
    'file': str(OUT.relative_to(ROOT)),
    'link': 'http://localhost:8080/output/2026-06-07/adaptive-html-final-sequential-16-modes-20260607_105404/pages/05_github_analysis_skills_html_showcase_due_diligence.html',
    'policy': 'previous HTML body not reused by render script; common generator not used; github_analysis layout/recipe/references/templates consulted for this page only',
    'materials_sha256': MATERIAL_HASH,
    'used_materials': [str(p.relative_to(REPO)) for p in MODE_MATERIALS],
    'repo_sources_checked': [str(p.relative_to(REPO)) for p in REPO_SOURCES if p.exists()] + ['git remote/log/ls-remote', 'gh repo view metadata', 'gh release/issue/pr list'],
    'repo_facts': {
        'name_with_owner': 'coreline-ai/skills-html-showcase',
        'default_branch': 'main',
        'origin_main': 'e4b8d61c3e7bf8212b5cb694cd397e86c6f77656',
        'manifest_version': version,
        'mode_count': mode_count,
        'layout_count': layout_count,
        'theme_count': len(themes),
        'license_info': None,
        'github_releases_observed': 0,
        'github_issues_observed': 0,
        'github_prs_observed': 0,
        'package_export_script': package.get('scripts', {}).get('export:output'),
    },
    'placeholder_mapping': {
        'VERDICT': 'one-line recommendation + vt hero-map + FACT/INFERENCE/UNKNOWN cards',
        'QUESTION_TOC': 'question-centered nav with real anchors',
        'REPO_IDENTITY': 'repo identity grid + metadata drift evidence',
        'QUICKSTART_READINESS': 'quickstart signals + wg-14 command explainer',
        'REPO_HEALTH': 'wg-11 health board + observed GitHub surface',
        'CODE_TOUR': 'vt file-tour + wg-04 module map',
        'RELEASES_AND_ROADMAP': 'version drift + vt timeline',
        'SECURITY_AND_LICENSE': 'vt quality-gate + UNKNOWN separation',
        'RISK_MATRIX': 'vt risk-matrix + mobile-safe table',
        'FINAL_DECISION': 'vt decision-tree + wg-16 adoption plan',
        'NEXT_ACTIONS': '3-step action cards + vt checklist-flow',
        'SOURCE_NOTE': 'checked surfaces and limits'
    },
    'visual_contract': {
        'layout': 'github-analysis.html',
        'numbered_h2_order': 'body-icon body-icon--sm -> num -> title',
        'generated_row': True,
        'lens_strip': True,
        'fact_inference_unknown': True,
        'question_toc_links': 7,
        'vt_required': ['hero-map'],
        'vt_used': ['hero-map', 'quality-gate', 'file-tour', 'risk-matrix', 'timeline', 'decision-tree', 'checklist-flow'],
        'wg_used': ['11-weekly-status', '04-module-map', '14-feature-explainer', '16-implementation-plan'],
        'table_mobile_safe': 'table-scroll + mobile-card-table where table is used',
    },
    'review_findings_and_fixes': [
        '기존 화면은 구조적으로 큰 문제는 없었지만, 목표 조건에 맞춰 기존 HTML 본문을 읽지 않는 github_analysis 전용 렌더러로 재생성했다.',
        'GitHub description의 13모드/3테마 문구와 manifest v5.8.1·16모드·8테마 사이의 정합성 drift를 핵심 리스크로 명시했다.',
        '질문 중심 목차에 실제 section anchor를 부여해 목차가 장식이 아니라 탐색 구조로 동작하게 했다.'
    ],
    'skill_patch_candidates_from_mode_review': [
        'github_analysis는 GitHub metadata drift를 별도 FACT 리스크로 다뤄야 한다.',
        'github_analysis layout의 QUESTION_TOC는 실제 anchor와 연결되어야 완료로 본다.',
        'licenseInfo null, releases/issues/pr 빈 표면은 UNKNOWN/리스크로 분리하되 품질 단정에 쓰지 않는다.',
        'recipe의 3테마 표현은 현행 base.html 8테마 계약과 맞게 업데이트해야 한다.'
    ],
    'next_mode': '06_youtube_analysis'
}
(ROOT / 'sources/05_github_analysis-visual-contract-evidence.json').write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(OUT)
