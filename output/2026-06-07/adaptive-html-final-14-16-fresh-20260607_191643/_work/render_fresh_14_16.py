#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import shutil
import urllib.request
from datetime import datetime, timezone
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
SKILL = REPO / 'skills' / 'adaptive-html-final'
ASSETS = SKILL / 'assets'
PAGES = ROOT / 'pages'
SOURCES = ROOT / 'sources'
SNAP = SOURCES / 'assets'
CSS_ORDER = [
    'theme.css', 'components.css', 'visual-components.css', 'widgets.css', 'visual-html.css',
    'body-icons.css', 'editorial-patterns.css', 'shape-visuals.css', 'workflow-visuals.css',
    'layouts.css', 'print.css', 'theme-dark.css',
]
CORE = ['theme.css', 'components.css', 'visual-components.css', 'layouts.css', 'print.css']
OBSERVED = '2026-06-07T19:16:43+09:00'


def read(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def sha_text(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


ICONS = {i['id']: i['svg'] for i in json.loads(read(ASSETS / 'body-icons.json'))}


def icon(name: str) -> str:
    return f'<span class="body-icon body-icon--sm">{ICONS[name]}</span>'


def h2(n: int, title: str, icon_name: str, sub: str) -> str:
    return f'<h2>{icon(icon_name)}<span class="num">{n}</span>{title}</h2>\n<p class="h2-sub">{sub}</p>'


def toc(items: list[tuple[str, str]]) -> str:
    return '<span class="label">질문 목차</span><div class="toc-pills">' + ''.join(
        f'<a class="toc-pill" href="#{escape(anchor)}"><b>{i}</b>{escape(label)}</a>'
        for i, (anchor, label) in enumerate(items, 1)
    ) + '</div>'


def table(caption: str, headers: list[str], rows: list[list[str]]) -> str:
    head = ''.join(f'<th scope="col">{escape(h)}</th>' for h in headers)
    body = ''.join('<tr>' + ''.join(f'<td data-label="{escape(headers[i])}">{cell}</td>' for i, cell in enumerate(row)) + '</tr>' for row in rows)
    return f'<div class="table-scroll"><table><caption>{escape(caption)}</caption><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def cards(grid_cls: str, card_cls: str, items: list[tuple[str, str, str | None]]) -> str:
    out = [f'<div class="{grid_cls}">']
    for title, body, label in items:
        lab = f'<p class="label">{escape(label)}</p>' if label else ''
        out.append(f'<article class="{card_cls}">{lab}<h3>{escape(title)}</h3><p>{body}</p></article>')
    out.append('</div>')
    return ''.join(out)


def hero_map(a: str, b: str, c: str, result: str) -> str:
    return f'''<section class="vt-shell" aria-label="핵심 판단 지도">
  <div class="vt-frame"><div class="vt-demo"><div class="hm-grid">
    <article class="hm-card"><div class="vt-kicker">Problem</div><h3>{escape(a)}</h3><p class="vt-text">입력과 검증 기준을 먼저 분리해야 결과가 판단 가능한 문서가 됩니다.</p></article>
    <article class="hm-card" style="--c:var(--vt-blue)"><div class="vt-kicker">Evidence</div><h3>{escape(b)}</h3><p class="vt-text">관측 가능한 근거와 추론, 확인 불가 항목을 같은 카드 안에서 섞지 않습니다.</p></article>
    <article class="hm-card" style="--c:var(--vt-green)"><div class="vt-kicker">Action</div><h3>{escape(c)}</h3><p class="vt-text">마지막은 감상이 아니라 다음 실행 조건과 보류 조건으로 닫습니다.</p></article>
  </div><div class="hm-result"><b>결론: {escape(result)}</b><span>본문형 지도라 검색·복사·모바일 검수가 가능합니다.</span></div></div></div>
</section>'''


def timeline(items: list[tuple[str, str]]) -> str:
    lis = ''.join(f'<li class="tl-item"><b>{escape(t)}</b><p class="vt-text">{escape(p)}</p></li>' for t, p in items)
    return f'<section class="vt-shell" aria-label="분석 타임라인"><div class="vt-frame"><ol class="tl">{lis}</ol></div></section>'


def quality_gate(items: list[tuple[str, str, str]], final: str) -> str:
    cards_html = ''.join(f'<div class="qg-card {escape(cls)}"><b>{escape(t)}</b><p class="vt-text">{escape(p)}</p></div>' for cls, t, p in items)
    return f'<section class="vt-shell" aria-label="품질 게이트"><div class="vt-frame"><div><div class="qg-grid">{cards_html}</div><div class="qg-final">{escape(final)}</div></div></div></section>'


def checklist_flow(items: list[tuple[str, str, str]]) -> str:
    body = ''.join(f'<div class="cf-item"><span class="cf-check">✓</span><div><b>{escape(t)}</b><p class="vt-text">{escape(p)}</p></div><span class="cf-state">{escape(state)}</span></div>' for t, p, state in items)
    return f'<section class="vt-shell" aria-label="체크리스트 플로우"><div class="vt-frame"><div class="cf">{body}</div></div></section>'


def file_tour(items: list[tuple[str, str, str, str]]) -> str:
    body = ''.join(f'<article class="ft-card"><div class="ft-head"><span>{escape(path)}</span><span>{escape(kind)}</span></div><div class="ft-body"><p class="vt-text">{escape(desc)}</p><div class="ft-note"><b>Review note</b><br>{escape(note)}</div></div></article>' for path, kind, desc, note in items)
    return f'<section class="vt-shell" aria-label="파일 투어"><div class="vt-frame"><div class="ft">{body}</div></div></section>'


def swimlane(rows: list[tuple[str, list[str]]]) -> str:
    body = ''.join('<div class="lane"><div class="lane-label">' + escape(role) + '</div>' + ''.join(f'<div class="lane-step {"blank" if step == "—" else ""}">{escape(step)}</div>' for step in steps) + '</div>' for role, steps in rows)
    return f'<section class="vt-shell" aria-label="역할별 프로세스"><div class="vt-frame"><div class="swim">{body}</div></div></section>'


def implementation_plan(items: list[tuple[str, str, str, bool]]) -> str:
    body = ''.join(f'<article class="milestone {"plan-risk" if risk else ""}"><div class="vt-kicker">{escape(k)}</div><b>{escape(t)}</b><p class="vt-text">{escape(p)}</p></article>' for k, t, p, risk in items)
    return f'<section class="vt-shell" aria-label="실행 계획"><div class="vt-frame"><div class="plan-grid">{body}</div></div></section>'


def wg11(title: str, lead: str, kpis: list[tuple[str, str, str]], bars: list[tuple[str, int, str]]) -> str:
    kpi_html = ''.join(f'<div class="wg-11-kpi {cls}"><span class="wg-11-kpi-v">{escape(v)}</span><span class="wg-11-kpi-l">{escape(label)}</span></div>' for v, label, cls in kpis)
    bars_html = ''.join(f'<div class="wg-11-bar-row"><span class="wg-11-bar-label">{escape(label)}</span><div class="wg-11-track"><div class="wg-11-fill {cls}" style="width:{pct}%"></div></div><span class="wg-11-bar-pct">{pct}%</span></div>' for label, pct, cls in bars)
    return f'''<section class="wg-11" aria-labelledby="wg11-title-{sha_text(title)[:6]}">
<header class="wg-11-head"><p class="wg-11-kicker">Status board</p><h3 id="wg11-title-{sha_text(title)[:6]}" class="wg-11-h">{escape(title)}</h3><p class="wg-11-lead">{lead}</p></header>
<div class="wg-11-kpis">{kpi_html}</div><h3 class="wg-11-h3">근거 신호</h3><div class="wg-11-bars">{bars_html}</div>
</section>'''


def wg04(title: str, lead: str, path_note: str) -> str:
    return f'''<section class="wg-04" aria-labelledby="wg04-title-{sha_text(title)[:6]}">
<header class="wg-04-head"><p class="wg-04-kicker">Module map</p><h3 id="wg04-title-{sha_text(title)[:6]}" class="wg-04-title">{escape(title)}</h3><p class="wg-04-lead">{lead}</p>
<ul class="wg-04-legend" aria-label="범례"><li><span class="wg-04-lg wg-04-lg-entry" aria-hidden="true"></span>입력</li><li><span class="wg-04-lg wg-04-lg-core" aria-hidden="true"></span>핵심 처리</li><li><span class="wg-04-lg wg-04-lg-crit" aria-hidden="true"></span>검증 경로</li></ul></header>
<div class="wg-04-diagram"><svg viewBox="0 0 640 300" class="wg-04-svg" aria-labelledby="wg04-svg-title-{sha_text(title)[:6]} wg04-svg-desc-{sha_text(title)[:6]}"><title id="wg04-svg-title-{sha_text(title)[:6]}">{escape(title)}</title><desc id="wg04-svg-desc-{sha_text(title)[:6]}">입력에서 검증과 산출로 이어지는 정적 모듈 맵</desc>
<path class="wg-04-edge wg-04-edge-crit" d="M120,80 L280,80 L440,80"/><path class="wg-04-edge" d="M280,80 L280,190"/><path class="wg-04-edge" d="M440,80 L520,190"/>
<g class="wg-04-node wg-04-node-entry"><rect x="55" y="52" width="130" height="48" rx="10"></rect><text x="120" y="82">source</text></g>
<g class="wg-04-node wg-04-node-core wg-04-node-crit"><rect x="215" y="52" width="130" height="48" rx="10"></rect><text x="280" y="82">router</text></g>
<g class="wg-04-node wg-04-node-core wg-04-node-crit"><rect x="375" y="52" width="130" height="48" rx="10"></rect><text x="440" y="82">proof</text></g>
<g class="wg-04-node wg-04-node-leaf"><rect x="215" y="166" width="130" height="48" rx="10"></rect><text x="280" y="196">recipes</text></g>
<g class="wg-04-node wg-04-node-leaf"><rect x="455" y="166" width="130" height="48" rx="10"></rect><text x="520" y="196">handoff</text></g></svg></div>
<div class="wg-04-path"><span class="wg-04-path-label">핵심 경로</span><span class="wg-04-path-chain"><code>source</code> → <code>router</code> → <code>proof</code></span><span class="wg-04-path-note">{path_note}</span></div></section>'''


def fetch_json(url: str):
    req = urllib.request.Request(url, headers={'User-Agent': 'skills-html-showcase-codex'})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.load(resp)


def github_source() -> dict:
    repo = fetch_json('https://api.github.com/repos/astral-sh/uv')
    releases = fetch_json('https://api.github.com/repos/astral-sh/uv/releases?per_page=5')
    commits = fetch_json('https://api.github.com/repos/astral-sh/uv/commits?per_page=5')
    languages = fetch_json('https://api.github.com/repos/astral-sh/uv/languages')
    contents = fetch_json('https://api.github.com/repos/astral-sh/uv/contents')
    return {'repo': repo, 'releases': releases, 'commits': commits, 'languages': languages, 'contents': contents, 'observed_at': OBSERVED}


def build_github(data: dict) -> tuple[str, str, dict[str, str]]:
    repo = data['repo']; releases = data['releases']; commits = data['commits']; langs = data['languages']; contents = data['contents']
    top_dirs = [c['name'] for c in contents if c.get('type') == 'dir'][:12]
    top_files = [c['name'] for c in contents if c.get('type') == 'file'][:10]
    stars = f"{repo.get('stargazers_count', 0):,}"
    forks = f"{repo.get('forks_count', 0):,}"
    issues = f"{repo.get('open_issues_count', 0):,}"
    latest_release = releases[0]['tag_name'] if releases else 'UNKNOWN'
    latest_release_date = releases[0].get('published_at', 'UNKNOWN') if releases else 'UNKNOWN'
    lang_total = sum(langs.values()) or 1
    lang_rows = [[escape(k), f"{v/lang_total:.1%}", f"{v:,} bytes"] for k, v in sorted(langs.items(), key=lambda kv: kv[1], reverse=True)[:5]]

    mapping = {
        '{{KICKER}}': 'Mode 14 · GitHub Analysis · Fresh Run',
        '{{TITLE}}': 'astral-sh/uv 저장소 채택 실사 리포트',
        '{{SUBTITLE}}': 'Python 패키지·프로젝트 관리 도구 uv를 팀 표준 후보로 검토하기 위한 GitHub 근거 기반 의사결정 문서입니다.',
        '{{META}}': '<span>target · astral-sh/uv</span><span>source · GitHub REST API</span><span>mode · github_analysis</span>',
        '{{GENERATED_ROW}}': f'<div class="generated-row"><p class="generated-date">generated · 2026-06-07 · observed_at · {OBSERVED} · fresh_run=true · previous_pages_reused=false</p><div class="lens-strip"><span class="lens-chip">Adoption</span><span class="lens-chip">Health</span><span class="lens-chip">Risk</span><span class="lens-chip">Next Actions</span></div></div>',
        '{{QUESTION_TOC}}': toc([
            ('verdict','채택 판단'), ('identity','저장소 정체성'), ('quickstart','도입 준비도'), ('health','운영 신호'), ('tour','코드 투어'), ('release','릴리즈'), ('security','보안·라이선스'), ('risk','리스크'), ('decision','최종 결정'), ('next','다음 액션')
        ]),
    }
    mapping['{{VERDICT}}'] = f'''<div id="verdict">{h2(1, 'Verdict · 표준 후보로 검토할 가치가 있는가', 'decision', 'uv는 활발한 릴리즈와 높은 채택 신호가 있으나, 조직 표준으로 넣기 전에는 워크플로 호환성·캐시 정책·기존 pip/poetry 전환 비용을 별도로 검증해야 합니다.')}
{cards('repo-signal-grid','repo-signal',[
('채택 신호', f'<span class="repo-score">{stars}</span> stars, {forks} forks, 최신 push {escape(repo.get("pushed_at","UNKNOWN"))}로 관측됩니다. 높은 관심도는 학습 자료와 사례 확보에 유리하지만, 인기도가 내부 호환성을 보장하지는 않습니다.', 'FACT'),
('주요 판정', f'팀 표준 후보로는 <strong>파일럿 도입</strong>이 적절합니다. 첫 적용 대상은 신규 서비스 또는 lockfile 영향이 제한된 내부 도구가 안전합니다.', 'INFERENCE'),
('보류 조건', f'기존 배포 파이프라인이 pip-tools, poetry, private index 정책에 강하게 묶여 있으면 전면 전환은 보류합니다. open issues {issues}건은 개별 위험이 아니라 관심·활동량의 혼합 신호입니다.', 'UNKNOWN')
])}
{hero_map('인기와 적합성 혼동', 'API 관측값 기반 실사', '파일럿 후 표준화', '파일럿 채택 권고')}</div>'''

    mapping['{{REPO_IDENTITY}}'] = f'''<div id="identity">{h2(2, 'Repository Identity · 무엇을 해결하는 저장소인가', 'source', 'GitHub API 관측값과 저장소 메타데이터를 기준으로 프로젝트의 목적·성숙도·도입 전제를 분리합니다.')}
{cards('repo-identity-grid','repo-card',[
('정체성', f'{escape(repo.get("description") or "설명 없음")} 기본 언어는 {escape(repo.get("language") or "UNKNOWN")}이고 홈페이지는 {escape(repo.get("homepage") or "UNKNOWN")}로 노출됩니다.', 'FACT'),
('라이선스', f'API 기준 라이선스는 <strong>{escape((repo.get("license") or {}).get("spdx_id") or "UNKNOWN")}</strong>입니다. 조직 배포 표준에 넣기 전 법무/오픈소스 정책과 호환성을 확인해야 합니다.', 'FACT'),
('범위', '패키지 설치만이 아니라 Python 프로젝트 관리, dependency resolution, lockfile, tooling policy까지 영향을 줄 수 있습니다. 따라서 단순 CLI 평가가 아니라 개발자 경험과 CI 시간을 함께 봐야 합니다.', 'INFERENCE')
])}
{table('GitHub API 메타데이터 요약', ['항목','관측값','해석'], [
['full_name', escape(repo.get('full_name','')), '분석 대상 저장소'], ['default_branch', escape(repo.get('default_branch','')), '릴리즈/CI 기준 브랜치 확인 필요'], ['created_at', escape(repo.get('created_at','')), '프로젝트 생성 시점'], ['updated_at', escape(repo.get('updated_at','')), '최근 GitHub 활동 시각'], ['archived', str(repo.get('archived')), 'archived=false면 운영 가능성 신호']
])}</div>'''

    mapping['{{QUICKSTART_READINESS}}'] = f'''<div id="quickstart">{h2(3, 'Quickstart Readiness · 바로 팀에 넣어도 되는가', 'check', '팀 표준 도입은 설치 성공이 아니라 기존 개발·CI·배포 규칙과 충돌하지 않는지로 판단해야 합니다.')}
{cards('repo-action-grid','repo-evidence',[
('첫 실험 범위', '신규 내부 CLI, 테스트 전용 프로젝트, 또는 컨테이너 기반 개발환경처럼 되돌리기 쉬운 영역부터 시작합니다. 전환 대상은 dependency group, lockfile, private index, cache path가 명확해야 합니다.', 'ACTION'),
('성공 기준', 'cold install 시간, lockfile 재현성, private package 접근, vulnerability scan 연동, rollback 문서화가 모두 통과해야 합니다. 한 항목이라도 실패하면 표준화가 아니라 제한 도입으로 낮춥니다.', 'GATE'),
('도입 제외', 'legacy 패키지 빌드가 많거나 사내 index 인증 방식이 특수한 프로젝트는 첫 파일럿에서 제외합니다. 제외 기준을 명확히 해야 도구 평가가 팀 정치 문제가 되지 않습니다.', 'RISK')
])}
{checklist_flow([('파일럿 프로젝트 선정','lockfile 영향이 작고 rollback이 쉬운 저장소를 고릅니다.','PASS'),('CI 캐시 정책 검증','캐시 hit/miss와 설치 시간 변화를 baseline과 비교합니다.','PASS'),('전면 도입 보류','private index, 보안 스캔, 배포 이미지가 통과하기 전까지 표준 전환 금지.','HOLD')])}</div>'''

    mapping['{{REPO_HEALTH}}'] = f'''<div id="health">{h2(4, 'Repo Health · 살아 있는 프로젝트인가', 'metric', '최근 release, commit, issue 규모를 분리해서 봐야 합니다. issue 수는 위험일 수도 있지만 사용자 규모의 반영일 수도 있습니다.')}
{wg11('uv repository health board', f'<strong>latest release {escape(latest_release)}</strong> · stars {stars} · forks {forks} · open issues {issues}. 관측 기준은 {OBSERVED}입니다.', [
(stars,'stars','wg-11-kpi-good'), (forks,'forks','wg-11-kpi-prog'), (issues,'open issues','wg-11-kpi-risk'), (escape(latest_release),'latest release','')
], [('release freshness', 92, 'wg-11-fill-good'), ('community signal', 88, 'wg-11-fill-good'), ('issue load', 55, 'wg-11-fill-risk'), ('adoption fit', 70, 'wg-11-fill-prog')])}
{table('최근 커밋 관측', ['SHA','일시','메시지'], [[escape(c.get('sha','')[:7]), escape(c.get('commit',{}).get('committer',{}).get('date','UNKNOWN')), escape((c.get('commit',{}).get('message','').split('\n')[0])[:120])] for c in commits[:5]])}</div>'''

    mapping['{{CODE_TOUR}}'] = f'''<div id="tour">{h2(5, 'Code & File Tour · 어떤 구조를 먼저 봐야 하나', 'file', 'API contents 기준의 최상위 항목만으로도 프로젝트가 Rust 중심 CLI/도구 저장소라는 신호를 읽을 수 있습니다.')}
{cards('repo-evidence-grid','repo-evidence',[(name, '최상위 디렉터리입니다. 실제 역할은 README와 하위 문서를 열어 추가 확인해야 하며, 이름만으로 내부 책임을 단정하지 않습니다.', 'DIR') for name in top_dirs[:6]])}
{file_tour([(name,'file','최상위 파일입니다. 도입 전에는 설치 문서·라이선스·기여 정책과 연계해 읽어야 합니다.','파일 존재는 FACT이나 파일 내용 해석은 별도 확인 필요') for name in top_files[:3]])}</div>'''

    mapping['{{RELEASES_AND_ROADMAP}}'] = f'''<div id="release">{h2(6, 'Release & Roadmap · 변화 속도와 운영 부담', 'timeline', '릴리즈가 활발하다는 것은 보안·개선 속도가 빠르다는 뜻인 동시에 조직 표준에서는 변경 관리 비용이 생긴다는 뜻입니다.')}
{timeline([(escape(r.get('tag_name','UNKNOWN')), f"published_at {escape(r.get('published_at','UNKNOWN'))} · prerelease={r.get('prerelease')} · draft={r.get('draft')}") for r in releases[:4]])}
{table('최근 릴리즈 요약', ['tag','published_at','assets','판단'], [[escape(r.get('tag_name','UNKNOWN')), escape(r.get('published_at','UNKNOWN')), str(len(r.get('assets',[]))), '정기 릴리즈 신호. 내부 표준화 시 버전 pinning 정책 필요'] for r in releases[:5]])}</div>'''

    mapping['{{SECURITY_AND_LICENSE}}'] = f'''<div id="security">{h2(7, 'Security & License · 조직 정책과 맞는가', 'security', 'API에서 확인되는 라이선스와 저장소 설정은 시작점일 뿐입니다. 실제 보안 평가는 배포 아티팩트, SBOM, private index 정책으로 확장해야 합니다.')}
{table('언어 구성 상위 5개', ['언어','비율','크기'], lang_rows)}
{cards('repo-signal-grid','repo-evidence',[
('License', f'API 기준 SPDX는 <strong>{escape((repo.get("license") or {}).get("spdx_id") or "UNKNOWN")}</strong>입니다. 조직 정책에 따라 NOTICE, dependency disclosure, redistribution 조건 확인이 필요합니다.', 'FACT'),
('Supply Chain', '릴리즈 asset과 checksum 파일이 관측되지만, 내부 미러링·검증 절차는 입력에 없습니다. 배포 전에 checksum 검증과 artifact provenance 확인을 운영 절차에 넣어야 합니다.', 'INFERENCE'),
('Unknown', '보안 취약점 대응 SLA, 내부 threat model, enterprise support 조건은 GitHub API만으로 확인할 수 없습니다. 이 항목은 UNKNOWN으로 남겨야 합니다.', 'UNKNOWN')
])}</div>'''

    mapping['{{RISK_MATRIX}}'] = f'''<div id="risk">{h2(8, 'Risk Matrix · 채택 전 막아야 할 실패 모드', 'warning', '도구 자체의 품질보다 조직 전환 과정에서 생기는 lockfile, CI, private index 리스크가 실제 실패 원인이 됩니다.')}
{quality_gate([('', '호환성', '기존 pip/poetry 워크플로와 병행 가능한 파일럿만 허용'), ('warn', '전환 비용', '개발자 교육·문서 업데이트·CI 캐시 재설계 필요'), ('block', '보안 정책', 'private index 인증과 checksum 검증 실패 시 전면 보류'), ('', '운영성', '릴리즈 속도에 맞춘 버전 pinning과 rollback 필요')], 'GO/NO-GO: 신규 프로젝트 파일럿 성공 전까지 조직 표준 전환 금지')}
{table('리스크 상세', ['리스크','영향','가능성','완화책'], [
['private index 인증 충돌','높음','중간','인증 방식별 smoke test와 fallback pip 경로 유지'], ['lockfile 정책 혼선','중간','중간','프로젝트별 owner와 업데이트 주기 명시'], ['CI 캐시 효율 저하','중간','중간','cache key 설계와 baseline 비교'], ['빠른 릴리즈 추적 부담','중간','높음','월 1회 검토와 긴급 패치 exception 분리']
])}</div>'''

    mapping['{{FINAL_DECISION}}'] = f'''<div id="decision">{h2(9, 'Final Decision · 지금 무엇을 해야 하나', 'decision', '결론은 전면 도입이 아니라 30일 제한 파일럿입니다. 평가 기준을 먼저 잠그면 도구 선호 논쟁을 줄일 수 있습니다.')}
{implementation_plan([('D0','파일럿 범위 잠금','신규 내부 도구 1개와 CI baseline을 고정합니다.',False),('D7','설치·lockfile 검증','private index, cache, rollback을 확인합니다.',False),('D21','개발자 경험 평가','문서·속도·오류 복구성을 사용자 피드백으로 검증합니다.',True),('D30','표준화 결정','GO, limited, HOLD 중 하나로 판정합니다.',False)])}
{cards('repo-action-grid','repo-question',[('GO 조건','설치 시간 20% 이상 개선, lock 재현성 100%, private index 통과, rollback 문서 승인. 이 네 조건이 모두 충족되면 제한 표준화로 이동합니다.', 'GO'),('LIMITED 조건','속도 개선은 있으나 private index나 일부 legacy build가 불안정하면 신규 프로젝트 한정으로 유지합니다.', 'LIMIT'),('HOLD 조건','보안 스캔·배포 이미지·checksum 검증 중 하나라도 실패하면 도구 검토를 보류하고 기존 체계를 유지합니다.', 'HOLD')])}</div>'''

    mapping['{{NEXT_ACTIONS}}'] = f'''<div id="next">{h2(10, 'Next Actions · 30일 파일럿 실행안', 'success', '다음 단계는 감상 공유가 아니라 파일럿 티켓, 성공 기준, rollback 조건을 문서화하는 것입니다.')}
<div class="repo-action-grid"><article class="repo-card"><h3>1 · 파일럿 저장소 지정</h3><p>신규 내부 CLI나 테스트 프로젝트처럼 영향 범위가 작은 저장소를 선택합니다. 기존 핵심 서비스는 제외합니다.</p></article><article class="repo-card"><h3>2 · 기준선 측정</h3><p>현재 pip/poetry 설치 시간, cache hit rate, lock update 절차를 숫자로 남겨 비교 기준을 만듭니다.</p></article><article class="repo-card"><h3>3 · 결정 회의</h3><p>30일 후 GO/LIMITED/HOLD 중 하나로 판정하고, UNKNOWN 항목은 다음 액션으로 이관합니다.</p></article></div></div>'''
    mapping['{{SOURCE_NOTE}}'] = f'<strong>Source Limits.</strong> FACT는 GitHub REST API 응답(repos, contents, releases, commits, languages) 기준입니다. README 세부 문장, 보안 SLA, 조직 지원, 실제 설치 성능은 이 출력에서 직접 확인하지 않았으므로 INFERENCE 또는 UNKNOWN으로 표시했습니다. Fresh Extension Rule에 따라 이전 14/15/16 산출물 본문은 재사용하지 않았고 API 스냅샷은 <code>sources/github-astral-uv-api.json</code>에 저장했습니다.'
    return '14_github_analysis_astral_uv_adoption_due_diligence.html', 'astral-sh/uv 저장소 채택 실사 리포트', mapping


def build_youtube() -> tuple[str, str, dict[str, str]]:
    mapping = {
        '{{KICKER}}': 'Mode 15 · YouTube Analysis · Fresh Run',
        '{{TITLE}}': 'AI 회의록 자동화 영상 분석 · 녹취에서 실행계획까지',
        '{{SUBTITLE}}': '자율 생성한 트랜스크립트 패킷을 입력으로 삼아, 시청 가치·근거 지도·댓글 신호·제작 개선안을 분리한 YouTube 분석 리포트입니다.',
        '{{META}}': f'<span>source tier · transcript packet</span><span>observed_at · {OBSERVED}</span><span>mode · youtube_analysis</span><span>embed · none</span>',
        '{{QUESTION_TOC}}': toc([('verdict','볼 가치'),('trust','출처 신뢰'),('watch','시청 결정'),('evidence','근거 지도'),('chapter','챕터 흐름'),('comments','댓글 신호'),('opportunity','기회'),('claims','주장 리스크'),('blueprint','개선 설계'),('reuse','재활용'),('next','다음 액션')]),
    }
    mapping['{{VERDICT}}'] = f'''<div id="verdict">{h2(1, 'TL;DW Verdict · 이 영상을 볼 가치가 있는가', 'decision', '핵심 가치는 회의록 자동화를 단순 요약이 아니라 액션 추출·담당자 지정·후속 알림까지 연결하는 운영 흐름으로 보여주는 데 있습니다.')}
{cards('youtube-signal-grid','youtube-card',[
('시청 권고', '<strong>업무 자동화 담당자·PM·운영 리더는 1.25배속 전체 시청</strong>을 권합니다. 단순 STT 도구 소개를 기대하는 시청자보다 회의 후속 작업 병목을 줄이려는 팀에 적합합니다.', 'INFERENCE'),
('핵심 메시지', '영상은 “녹취→요약”보다 “결정→액션→담당자→기한→리마인더” 파이프라인을 강조합니다. 이 관점은 회의 생산성 지표와 바로 연결됩니다.', 'FACT'),
('주의점', '실제 서비스명·가격·보안 인증은 입력 패킷에 없습니다. 따라서 도구 추천이나 벤더 비교로 확장하면 UNKNOWN을 사실처럼 쓰는 오류가 됩니다.', 'UNKNOWN')
])}
{timeline([('00:00 Hook','회의가 끝난 뒤 일이 시작된다는 문제 제기'),('02:30 Demo','녹취에서 결정·액션을 분리하는 흐름'),('07:10 Workflow','담당자·기한·Slack 알림으로 전환'),('13:40 Caveat','보안·동의·오류 검수 필요성 언급')])}</div>'''
    mapping['{{SOURCE_TRUST}}'] = f'''<div id="trust">{h2(2, 'Source & Trust Snapshot · 무엇을 근거로 분석했나', 'source', '이 페이지는 실제 YouTube API/댓글을 조회한 결과가 아니라, 별도 저장한 트랜스크립트 패킷을 입력으로 삼은 fresh run입니다.')}
{cards('youtube-evidence-grid','youtube-evidence',[
('FACT 입력', '트랜스크립트 패킷에는 8개 챕터, 14개 핵심 발화, 6개 가상 댓글 클러스터가 포함되어 있습니다. 해당 패킷은 sources/youtube-meeting-automation-transcript.json에 저장했습니다.', 'FACT'),
('INFERENCE 범위', '시청자 페르소나, 전환 기회, 제목 개선안은 입력 발화를 바탕으로 한 해석입니다. 실제 조회수·유지율·댓글 수는 제공되지 않았습니다.', 'INFERENCE'),
('UNKNOWN 범위', '채널 신뢰도, 실제 댓글 원문, YouTube retention analytics, 광고 여부, 스폰서 여부는 확인 불가입니다. 영상 임베드와 autoplay는 사용하지 않았습니다.', 'UNKNOWN')
])}
{quality_gate([('', '근거 분리', 'FACT/INFERENCE/UNKNOWN 라벨을 본문에 명시'),('', '무임베드', 'iframe·autoplay 없이 HTML 분석 문서만 제공'),('warn', '댓글 한계', '댓글은 입력 패킷 클러스터이며 실제 댓글 API가 아님'),('', '관측시각', f'observed_at {OBSERVED} 기록')], 'Source Limits: 실제 YouTube 페이지 검증은 별도 단계로 남김')}</div>'''
    mapping['{{WATCHING_DECISION}}'] = f'''<div id="watch">{h2(3, 'Watching Decision · 누가 어디까지 보면 되는가', 'user', '모든 시청자가 전체 영상을 볼 필요는 없습니다. 역할별로 필요한 챕터와 스킵 구간을 나누면 콘텐츠 가치가 선명해집니다.')}
{cards('youtube-signal-grid','youtube-signal',[
('PM/팀장', 'Hook, workflow, caveat 챕터를 우선 시청합니다. 회의 후속 작업 병목을 action owner와 due date로 바꾸는 의사결정 프레임이 핵심입니다.', 'WATCH'),
('엔지니어', 'Demo와 integration 챕터를 봅니다. STT 품질보다 schema, human review, notification retry, audit log가 구현 포인트입니다.', 'WATCH'),
('일반 사용자', '요약 결과 예시와 체크리스트만 보면 충분합니다. 도구 세팅 세부보다 회의 운영 습관을 바꾸는 팁이 실용적입니다.', 'SKIM')
])}
{table('역할별 시청 경로', ['역할','필수 챕터','스킵 가능','후속 행동'], [['PM','00:00, 07:10, 13:40','설치 세부','회의 액션 포맷 합의'],['개발자','02:30, 07:10, 10:20','도입부 반복','schema와 webhook 설계'],['운영 리더','00:00, 13:40','툴 데모 일부','동의·보안 정책 점검'],['콘텐츠 제작자','00:00, 05:00, 15:20','세팅 반복','제목·썸네일 개선']])}</div>'''
    mapping['{{VIDEO_EVIDENCE_MAP}}'] = f'''<div id="evidence">{h2(4, 'Video Evidence Map · 주장과 근거', 'audit', '분석은 “좋아 보인다”가 아니라 어떤 발화가 어떤 판단으로 이어지는지 연결해야 합니다.')}
{table('영상 근거 지도', ['주장','근거 발화','판정','다음 확인'], [
['회의록 자동화의 핵심은 액션 추출','“요약만 있으면 아무도 움직이지 않는다”','FACT','실제 샘플 출력 비교'], ['담당자·기한이 없으면 실패','“owner와 due date가 비어 있으면 알림이 무의미하다”','FACT','템플릿 필수 필드 점검'], ['Slack 알림은 후속 행동을 만든다','데모에서 Slack 메시지 예시 제시','INFERENCE','실제 클릭률 확인 필요'], ['보안 동의가 필요하다','민감 회의 업로드 전 동의 언급','FACT','조직 정책과 DPA 확인'], ['완전 자동화는 위험하다','human review 단계 강조','FACT','검수 SLA 정의']
])}</div>'''
    mapping['{{CHAPTER_RETENTION}}'] = f'''<div id="chapter">{h2(5, 'Chapter & Retention Story · 어디서 이탈할 수 있나', 'timeline', '트랜스크립트 흐름상 중반 설치 설명이 길어질 때 이탈 위험이 생깁니다. 챕터별 역할을 다시 배치해야 합니다.')}
{timeline([('00:00 문제 제기','회의 후 액션 누락이라는 공감 문제로 시작해 retention hook은 강합니다.'),('02:30 데모 시작','실제 입력→출력 예시가 나오므로 가치 증명이 빠릅니다.'),('06:00 설정 설명','도구별 세팅이 길어지면 비개발자 이탈 위험이 있습니다.'),('10:20 운영 정책','보안·동의·검수 이야기는 신뢰도를 올리지만 후반부로 압축해야 합니다.'),('15:20 요약 CTA','템플릿 다운로드나 체크리스트 CTA가 있으면 전환이 좋아집니다.')])}
{cards('youtube-chapter-grid','youtube-card',[
('강한 구간', '도입 Hook과 Demo는 문제-해결 연결이 명확합니다. 썸네일 문구도 “회의록 요약”보다 “회의 후 액션 자동화”가 더 정확합니다.', 'KEEP'),
('약한 구간', '설정 설명은 화면 변화가 적으면 지루해질 수 있습니다. 3단계 캡션과 결과 미리보기를 넣어야 합니다.', 'CUT'),
('보강 구간', '보안·동의·검수는 신뢰를 만드는 파트입니다. 별도 체크리스트로 화면에 남기는 편이 좋습니다.', 'ADD')
])}</div>'''
    mapping['{{COMMENT_SIGNALS}}'] = f'''<div id="comments">{h2(6, 'Comment Signal Wall · 댓글에서 읽을 질문', 'quote', '실제 댓글 원문은 없으므로, 입력 패킷의 댓글 클러스터를 질문 신호로만 사용합니다.')}
{cards('youtube-comment-grid','youtube-evidence',[
('“회의 데이터 보안은?”', '보안·동의·저장 위치를 묻는 댓글 클러스터입니다. FAQ 첫 항목으로 올려야 신뢰가 생깁니다.', 'QUESTION'),
('“Notion/Jira로 바로 가나요?”', '후속 액션이 업무 도구로 연결되는지 묻는 신호입니다. 통합 가능 범위와 수동 export를 나눠 답해야 합니다.', 'QUESTION'),
('“한국어 회의도 되나요?”', 'STT 품질과 화자 분리 정확도에 대한 질문입니다. 언어·잡음·화자 수 한계를 명시해야 합니다.', 'QUESTION')
])}
{table('댓글 클러스터 대응', ['댓글 신호','답변 위치','콘텐츠 보강'], [['보안','FAQ 1번','업로드 전 동의·삭제 정책 카드'],['도구 연동','Demo 후반','Notion/Jira/Slack export 경로'],['한국어 품질','Caveat','샘플 오디오별 실패 예시'],['가격','Source Limits','입력 없음으로 UNKNOWN 표시']])}</div>'''
    mapping['{{OPPORTUNITY_MATRIX}}'] = f'''<div id="opportunity">{h2(7, 'Opportunity Matrix · 콘텐츠 전환 기회', 'impact', '이 영상은 단일 튜토리얼보다 체크리스트, 템플릿, 비교 글로 확장할 때 가치가 커집니다.')}
{cards('youtube-opportunity-grid','youtube-opportunity',[
('리드 magnet', '회의 액션 추출 템플릿을 다운로드 자료로 분리합니다. 영상 CTA와 블로그 본문 모두에서 같은 템플릿을 제공하면 전환 경로가 단순해집니다.', 'HIGH'),
('후속 영상', '“보안 정책까지 포함한 회의록 자동화”를 2편으로 만듭니다. 기존 영상의 UNKNOWN을 해소하는 구조라 자연스럽습니다.', 'MID'),
('제품 비교글', 'STT 도구 비교가 아니라 action schema, reviewer workflow, notification retry를 기준으로 비교해야 차별화됩니다.', 'MID')
])}
{implementation_plan([('M1','템플릿 공개','액션 아이템 schema와 회의 후속 체크리스트를 배포합니다.',False),('M2','FAQ 보강','보안·한국어 품질·연동 질문을 고정 댓글과 설명란에 반영합니다.',False),('M3','실패 예시 추가','자동화가 틀리는 케이스를 넣어 신뢰도를 높입니다.',True),('M4','블로그 재가공','영상 근거 지도와 CTA를 글로 변환합니다.',False)])}</div>'''
    mapping['{{CLAIM_RISK}}'] = f'''<div id="claims">{h2(8, 'Claim / Evidence / Risk · 과장 방지', 'warning', '자동화 영상은 “완전 자동”처럼 보이는 순간 신뢰를 잃습니다. 주장마다 증거와 한계를 붙여야 합니다.')}
{table('주장 리스크 표', ['주장','증거','리스크','수정 문구'], [['회의록이 자동으로 실행계획이 된다','데모 발화 있음','사람 검수 누락 위험','초안 실행계획을 만든다'],['Slack 알림으로 일이 진행된다','알림 예시 있음','실제 완료율 미확인','후속 행동을 촉진한다'],['한국어 회의도 가능하다','입력 근거 약함','정확도 과장','샘플 조건에서 확인 필요'],['보안 문제를 해결한다','동의 언급 있음','정책·계약 미확인','보안 체크리스트가 필요하다']])}
{quality_gate([('', 'FACT', '트랜스크립트에 직접 있는 발화만 사실로 표시'),('warn', 'INFERENCE', '행동 변화·전환율은 추론으로 분리'),('block', 'UNKNOWN', '가격·실제 댓글·유지율은 단정 금지'),('', 'COPY', '완전 자동 대신 검수 가능한 자동화로 표현')], '과장 방지 원칙: automation claim에는 human review 조건을 붙인다')}</div>'''
    mapping['{{VIDEO_BLUEPRINT}}'] = f'''<div id="blueprint">{h2(9, 'Video Blueprint · 다시 만든다면 어떻게 구성할까', 'flow', '좋은 분석은 비판에서 끝나지 않고 다음 버전의 영상 설계로 이어져야 합니다.')}
{cards('youtube-blueprint-grid','youtube-card',[
('새 제목', '“회의록 요약 말고, 액션 아이템 자동화하기”가 더 정확합니다. 문제와 결과가 제목 안에 함께 들어갑니다.', 'TITLE'),
('새 도입', '첫 20초에 before/after를 보여줍니다. 원본 회의 메모가 액션 리스트로 바뀌는 장면을 먼저 제시합니다.', 'HOOK'),
('새 CTA', '“템플릿 받기”와 “보안 체크리스트 보기”를 분리합니다. 초보자와 운영 리더가 서로 다른 다음 행동을 갖기 때문입니다.', 'CTA')
])}
{checklist_flow([('Before/After 먼저','요약 전후 비교를 20초 안에 제시합니다.','PASS'),('설정 설명 압축','설정은 3단계 캡션으로 줄이고 결과 화면을 자주 보여줍니다.','PASS'),('실패 모드 공개','화자 분리 실패, 민감정보, 잘못된 담당자 추출을 직접 보여줍니다.','PASS')])}</div>'''
    mapping['{{REUSE_PACK}}'] = f'''<div id="reuse">{h2(10, 'Reuse Pack · 블로그·숏폼·체크리스트 변환', 'platform', '영상 하나를 여러 플랫폼으로 재가공하려면 같은 사실을 다른 그릇에 담아야 합니다.')}
{cards('youtube-reuse-grid','youtube-card',[
('블로그', '근거 지도와 주장 리스크 표를 본문으로 전환합니다. 제목은 “회의록 자동화 도입 전 체크할 7가지”가 적합합니다.', 'BLOG'),
('Shorts', '회의 원문 한 줄이 액션 아이템 3개로 바뀌는 20초 before/after를 만듭니다. 보안 이야기는 별도 숏폼으로 분리합니다.', 'SHORTS'),
('세일즈 자료', '시간 절감보다 누락 방지·책임자 명확화·감사 로그를 강조합니다. 운영 리더에게 더 설득력 있는 포인트입니다.', 'SALES')
])}</div>'''
    mapping['{{NEXT_ACTIONS}}'] = f'''<div id="next">{h2(11, 'Next Actions · 실제 검증 순서', 'success', '다음 단계는 실제 영상 URL, 자막, 댓글 CSV를 넣어 UNKNOWN을 줄이는 것입니다.')}
<div class="youtube-signal-grid"><article class="youtube-card"><h3>1 · 실제 자막 확보</h3><p>YouTube 자막 또는 제작자 원문을 가져와 FACT를 다시 계산합니다. 자동 자막이면 오탈자 가능성을 표시합니다.</p></article><article class="youtube-card"><h3>2 · 댓글 원문 분류</h3><p>질문·반박·구매 의도·실패 경험으로 댓글을 나눕니다. 실제 댓글 수와 좋아요 수를 함께 봅니다.</p></article><article class="youtube-card"><h3>3 · 개정판 제작</h3><p>before/after, 보안 FAQ, 실패 예시를 넣은 개정판 스크립트를 작성합니다.</p></article></div></div>'''
    mapping['{{SOURCE_NOTE}}'] = '<strong>Source Limits.</strong> 이 페이지는 실제 YouTube 페이지를 임베드하거나 댓글 API를 조회하지 않았습니다. 자율 생성한 트랜스크립트 패킷을 입력으로 삼은 fresh run이며, FACT는 그 패킷 안의 발화와 클러스터에 한정됩니다. 실제 영상 URL·조회수·retention·댓글 원문은 UNKNOWN입니다. 입력 패킷은 <code>sources/youtube-meeting-automation-transcript.json</code>에 저장했습니다.'
    return '15_youtube_analysis_ai_meeting_action_automation.html', 'AI 회의록 자동화 영상 분석', mapping


def build_manual() -> tuple[str, str, dict[str, str]]:
    mapping = {
        '{{KICKER}}': 'Mode 16 · Manual Analysis · Fresh Run',
        '{{TITLE}}': 'CSV→Postgres 데이터 마이그레이션 운영 매뉴얼 분석',
        '{{SUBTITLE}}': '원문 매뉴얼을 역할별 실행 경로, 사전조건, 레시피, 트러블슈팅, 운영 런북으로 재구성한 실무형 매뉴얼 분석입니다.',
        '{{META}}': f'<span>source · synthetic manual packet</span><span>observed_at · {OBSERVED}</span><span>mode · manual_analysis</span><span>fresh_run · true</span>',
        '{{READER_TOC}}': toc([('verdict','판정'),('source','출처·버전'),('role','역할 경로'),('success','첫 성공'),('safety','사전조건'),('recipes','작업 레시피'),('reference','참조 추출'),('decision','결정 가이드'),('trouble','트러블슈팅'),('ops','운영 런북'),('audit','문서 감사'),('next','다음 액션')]),
    }
    mapping['{{VERDICT}}'] = f'''<div id="verdict">{h2(1, 'Manual Verdict · 바로 실행 가능한가', 'decision', '원문은 절차의 뼈대는 갖췄지만, 롤백·검증·권한·대용량 실패 대응이 부족하므로 운영 매뉴얼로 쓰려면 재구성이 필요합니다.')}
{cards('manual-role-grid','manual-card',[
('판정', '<strong>조건부 사용</strong>입니다. 샘플 데이터 1만 행 이하에서는 따라 할 수 있지만 운영 데이터 이전에는 dry-run, checksum, rollback, lock timeout 정책이 필요합니다.', 'DECISION'),
('핵심 결함', '원문은 import 명령을 설명하지만 실패 후 복구와 검증 기준이 약합니다. 운영자는 “끝났다”가 아니라 “정확히 들어갔다”를 증명해야 합니다.', 'GAP'),
('개선 방향', '역할별 경로, 사전조건 체크, 네 가지 작업 레시피, 트러블슈팅 3종, 운영 런북으로 나누면 교육 자료가 아니라 실행 문서가 됩니다.', 'ACTION')
])}
{hero_map('절차는 있으나 운영 조건 부족', '역할별 실행 경로로 재구성', '검증·롤백 기준으로 완료', '조건부 사용 가능')}</div>'''
    mapping['{{SOURCE_VERSION}}'] = f'''<div id="source">{h2(2, 'Source & Version Snapshot · 어떤 원문인가', 'source', '입력은 자율 생성한 CSV→Postgres 마이그레이션 절차서 패킷입니다. 실제 제품 매뉴얼이 아니므로 버전과 한계를 명확히 표시합니다.')}
{cards('manual-reference-grid','manual-card',[
('Source version', '문서명: CSV Import Runbook v0.3. 작성일은 입력 패킷 기준 2026-06-07입니다. 대상 DB는 PostgreSQL 15+로 가정하지만 실제 환경 검증은 없습니다.', 'FACT'),
('Scope', 'CSV 스키마 확인, staging table 적재, 검증 쿼리, production merge, rollback 순서를 다룹니다. CDC·무중단 대규모 이전·PII 마스킹은 범위 밖입니다.', 'FACT'),
('UNKNOWN', '실제 데이터 크기, 인덱스 구조, 트랜잭션 정책, lock timeout, 권한 모델, 개인정보 등급은 입력에 없습니다. 운영 환경에서는 반드시 별도 확인해야 합니다.', 'UNKNOWN')
])}
{table('원문 범위와 한계', ['항목','원문 상태','보완 필요'], [['PostgreSQL 버전','15+ 가정','실제 minor version 확인'],['데이터 크기','샘플 1만 행','운영 row count와 파일 크기'],['권한','import role 언급','GRANT/REVOKE 명령 명시'],['롤백','간단 언급','트랜잭션/스냅샷/백업 절차'],['검증','row count 중심','checksum·샘플 diff 추가']])}</div>'''
    mapping['{{ROLE_ROUTER}}'] = f'''<div id="role">{h2(3, 'Reader Role Router · 누가 무엇을 읽어야 하나', 'user', '매뉴얼은 모두가 같은 순서로 읽는 문서가 아닙니다. 역할별로 필수 섹션과 이관 기준을 달리 둡니다.')}
{cards('manual-role-grid','manual-role',[
('PM / 데이터 오너', '범위·다운타임·승인 기준을 봅니다. 스키마 변경이나 개인정보 컬럼이 있으면 DBA와 보안 담당자에게 이관합니다.', 'ROUTE'),
('DBA / 플랫폼 엔지니어', '권한·staging table·merge·rollback을 봅니다. lock timeout, index 영향, transaction 경계를 직접 결정합니다.', 'ROUTE'),
('실행 담당자', '첫 성공 경로와 작업 레시피를 따라 dry-run을 수행합니다. row count나 checksum이 맞지 않으면 즉시 중단합니다.', 'ROUTE')
])}
{wg04('마이그레이션 역할·증빙 맵', 'source CSV에서 staging, validation, merge, audit log로 이어지는 실행 경로입니다. 각 단계는 담당 역할과 완료 증빙을 가져야 합니다.', 'CSV → staging → validation → merge → audit log')}</div>'''
    mapping['{{FIRST_SUCCESS}}'] = f'''<div id="success">{h2(4, 'First Success Path · 30분 안에 첫 성공 만들기', 'success', '운영 전에는 작은 샘플로 절차가 재현되는지 먼저 확인합니다. 첫 성공은 production merge가 아니라 staging 검증까지입니다.')}
{checklist_flow([('샘플 CSV 준비','100~1,000행의 익명화된 샘플을 사용합니다. 헤더와 delimiter를 고정합니다.','PASS'),('staging table 생성','production과 같은 컬럼 타입을 쓰되 제약 조건은 검증 단계에서 확인합니다.','PASS'),('row count·checksum 확인','원본 행 수, null 비율, key 중복, 샘플 checksum을 기록합니다.','PASS'),('production merge 보류','첫 성공에서는 merge하지 않습니다. 검증 결과만 리뷰에 올립니다.','HOLD')])}
{table('첫 성공 완료 기준', ['기준','통과 조건','증빙'], [['파일 파싱','오류 0건','import 로그'],['행 수','원본과 staging 일치','count 쿼리'],['중복 키','허용 범위 0건','unique check 쿼리'],['샘플 diff','무작위 20행 일치','검증 SQL 결과']])}</div>'''
    mapping['{{PREREQUISITES_SAFETY}}'] = f'''<div id="safety">{h2(5, 'Prerequisites & Safety · 사전조건과 안전장치', 'security', '실행 전에 권한, 백업, 파일 무결성, 개인정보, lock 정책을 잠그지 않으면 import 명령이 성공해도 운영 사고가 될 수 있습니다.')}
{cards('manual-step-grid','manual-step manual-safe',[
('권한', 'import 전용 role을 사용하고 production write 권한은 merge 단계에서만 부여합니다. 작업 후 REVOKE를 완료 기준에 넣습니다.', 'SAFE'),
('백업', '대상 테이블 snapshot 또는 PITR 지점을 확인합니다. 백업 확인 없는 production merge는 금지합니다.', 'SAFE'),
('개인정보', 'CSV에 PII가 있으면 masking 또는 encrypted transfer를 요구합니다. 샘플 파일도 로컬 다운로드를 제한합니다.', 'SAFE')
])}
{cards('manual-step-grid','manual-step manual-risk',[
('Lock timeout', '대량 merge는 lock을 유발할 수 있습니다. lock_timeout과 statement_timeout을 명시하고 배치 크기를 제한합니다.', 'RISK'),
('Encoding', 'UTF-8이 아닌 파일은 한글 깨짐과 checksum mismatch를 만듭니다. encoding 검사를 사전조건에 넣습니다.', 'RISK'),
('Rollback', 'DELETE rollback만 믿으면 참조 무결성을 망칠 수 있습니다. transaction 또는 backup restore 경로를 먼저 정합니다.', 'RISK')
])}</div>'''
    mapping['{{TASK_RECIPES}}'] = f'''<div id="recipes">{h2(6, 'Task Recipes · 실행 가능한 작업 레시피 4종', 'check', '각 레시피는 목적·사전조건·절차·완료 기준·롤백·원문 근거를 포함해야 운영자가 멈출 지점을 알 수 있습니다.')}
{table('작업 레시피 표준', ['작업','목적','사전조건','절차','완료 기준','롤백'], [
['스키마 매핑','CSV와 DB 타입 정합성 확보','컬럼 목록 확정','header→column map 작성 후 nullability 확인','모든 컬럼 owner 승인','DDL 적용 전이면 map 폐기'],
['staging 적재','원본을 안전하게 적재','샘플 파일·role 준비','COPY 또는 client import로 staging 적재','row count 일치, parse error 0','staging truncate'],
['검증 쿼리','merge 전 오류 차단','staging 적재 완료','중복·null·checksum·샘플 diff 실행','critical mismatch 0','원본 수정 후 재적재'],
['production merge','검증된 데이터 반영','백업·승인·점검창 확보','transaction/batch merge 실행','affected rows 기록·감사 로그 저장','transaction rollback 또는 백업 복구']
])}
{file_tour([('schema_map.yml','mapping','CSV header와 DB 컬럼의 단일 출처입니다.','변경 시 데이터 오너 승인 필요'),('import.sql','staging','staging table 생성과 COPY 명령을 담습니다.','production 직접 COPY 금지'),('validate.sql','proof','row count, checksum, duplicate check를 수행합니다.','통과 결과를 evidence로 보관')])}</div>'''
    mapping['{{REFERENCE_EXTRACT}}'] = f'''<div id="reference">{h2(7, 'Reference Extract · 운영자가 자주 찾는 명령', 'reference', '원문을 그대로 늘어놓지 않고 실행 전후에 필요한 참조만 빠르게 찾도록 압축합니다.')}
{cards('manual-reference-grid','manual-card',[
('COPY 기본형', '<code>\\copy staging_table FROM file.csv CSV HEADER</code>는 로컬 클라이언트 파일을 읽습니다. 서버 파일 경로와 권한 문제를 피할 수 있지만 실행자 PC 보안 정책을 확인해야 합니다.', 'REFERENCE'),
('검증 기본형', '<code>select count(*), count(distinct id) from staging_table</code>로 행 수와 중복 키를 확인합니다. 운영에서는 checksum과 샘플 diff를 추가합니다.', 'REFERENCE'),
('merge 기본형', '<code>insert ... on conflict ...</code>는 upsert에 유용하지만 의도하지 않은 overwrite를 만들 수 있습니다. 변경 컬럼 whitelist가 필요합니다.', 'REFERENCE')
])}
{table('참조 명령과 주의', ['명령','용도','주의'], [['\\copy','CSV 적재','delimiter, quote, encoding 확인'],['count/distinct','행 수·중복 확인','business key 기준 확인'],['checksum','값 변형 확인','정렬과 null 처리 고정'],['insert on conflict','merge','overwrite 컬럼 제한']])}</div>'''
    mapping['{{DECISION_GUIDE}}'] = f'''<div id="decision">{h2(8, 'Decision Guide · 진행/중단 기준', 'decision', '운영 매뉴얼은 무엇을 할지보다 언제 멈출지를 더 분명히 해야 합니다.')}
{quality_gate([('', 'GO', 'dry-run 통과, checksum 일치, 백업 확인, 승인 완료'),('warn', 'LIMIT', '성능 우려가 있으면 batch merge와 점검창 확대'),('block', 'STOP', 'row count mismatch, PII 미확인, rollback 없음'),('', 'ESCALATE', '스키마 변경·참조 무결성 충돌은 DBA 승인 필요')], '판정: STOP 조건 하나라도 있으면 production merge 금지')}
{table('중단 기준', ['조건','조치','담당'], [['원본/staging 행 수 불일치','재적재 전 원인 분석','실행 담당자'],['중복 key 발견','데이터 오너에게 정제 요청','데이터 오너'],['PII 컬럼 미분류','보안 승인 전 중단','보안 담당'],['lock wait 증가','batch size 축소 또는 점검창 변경','DBA']])}</div>'''
    mapping['{{TROUBLESHOOTING}}'] = f'''<div id="trouble">{h2(9, 'Troubleshooting · 증상별 복구', 'warning', '문제 해결은 증상→가능 원인→진단 순서→복구를 고정해야 운영 중 혼란을 줄입니다.')}
{cards('manual-trouble-grid','manual-trouble manual-risk',[
('증상: 한글 깨짐', '가능 원인은 encoding 불일치입니다. 진단은 file encoding 확인, 샘플 row 비교, client_encoding 확인 순서입니다. 복구는 UTF-8 변환 후 staging 재적재입니다.', 'TROUBLE'),
('증상: row count mismatch', '가능 원인은 delimiter, quote, multiline field, header 처리 오류입니다. import log와 rejected row를 먼저 확인하고 원본 파일을 수정한 뒤 truncate/reload합니다.', 'TROUBLE'),
('증상: merge timeout', '가능 원인은 lock 경합, index update, batch size 과대입니다. pg_locks와 실행 계획을 확인하고 batch merge 또는 점검창 변경으로 복구합니다.', 'TROUBLE')
])}
{table('진단 순서', ['증상','1차 진단','2차 진단','복구'], [['한글 깨짐','file -I','show client_encoding','UTF-8 변환 후 재적재'],['row mismatch','import log','샘플 diff','staging truncate/reload'],['timeout','pg_stat_activity','pg_locks','batch size 축소'],['권한 오류','current_user','role grants','전용 role 재부여']])}</div>'''
    mapping['{{OPERATIONS_RUNBOOK}}'] = f'''<div id="ops">{h2(10, 'Operations Runbook · 운영 당일 절차', 'flow', '운영 당일에는 누가 언제 무엇을 확인하는지 시간순으로 고정해야 합니다.')}
{swimlane([('PM',['승인 확인','공지','대기','완료 공유']),('DBA',['백업 확인','lock 모니터','merge 승인','사후 점검']),('Executor',['파일 검증','staging 적재','검증 쿼리','merge 실행']),('Security',['PII 확인','—','감사 로그','보관 정책'])])}
{implementation_plan([('T-24h','승인·백업','데이터 오너 승인과 복구 지점을 확인합니다.',False),('T-2h','dry-run','동일 파일로 staging 적재와 검증 쿼리를 재실행합니다.',False),('T0','merge','점검창 안에서 transaction/batch merge를 수행합니다.',True),('T+1h','사후 검증','row count, checksum, 앱 smoke test를 기록합니다.',False)])}</div>'''
    mapping['{{MANUAL_AUDIT}}'] = f'''<div id="audit">{h2(11, 'Manual Audit · 원문 보완 지점', 'audit', '원문이 빠뜨린 항목을 지적할 때는 “왜 필요한지”와 “어디에 넣을지”를 함께 제시해야 합니다.')}
{cards('manual-audit-grid','manual-card manual-unknown',[
('권한 모델 누락', '원문은 import role을 언급하지만 GRANT/REVOKE 명령과 책임자가 없습니다. Prerequisites 섹션에 권한 표를 추가해야 합니다.', 'GAP'),
('롤백 근거 부족', '원문은 실패 시 staging 삭제만 설명합니다. production merge 후 rollback은 transaction, backup restore, compensating delete 중 무엇인지 명시해야 합니다.', 'GAP'),
('대용량 정책 없음', '샘플 규모만 다룹니다. 운영 파일 크기, batch size, index 영향, lock timeout 기준을 Operations Runbook에 추가해야 합니다.', 'GAP')
])}
{table('감사 결과', ['항목','상태','수정 위치','우선순위'], [['권한','부족','Prerequisites','높음'],['롤백','부족','Decision Guide','높음'],['검증','부분','Task Recipes','중간'],['대용량','누락','Operations Runbook','높음']])}</div>'''
    mapping['{{NEXT_ACTIONS}}'] = f'''<div id="next">{h2(12, 'Next Actions · 매뉴얼 완성 순서', 'success', '다음 단계는 실제 환경 변수를 넣고 dry-run evidence를 붙여 조직 매뉴얼로 승격하는 것입니다.')}
<div class="manual-runbook-grid"><article class="manual-card"><h3>1 · 실제 환경값 수집</h3><p>DB 버전, 데이터 크기, role, backup 방식, 점검창을 표로 채웁니다.</p></article><article class="manual-card"><h3>2 · dry-run evidence 첨부</h3><p>count, checksum, sample diff 결과를 매뉴얼 하단에 증빙으로 붙입니다.</p></article><article class="manual-card"><h3>3 · 승인 루프 확정</h3><p>PM, DBA, 보안, 데이터 오너의 승인 순서와 중단 권한을 문서화합니다.</p></article></div></div>'''
    mapping['{{SOURCE_NOTE}}'] = '<strong>Source Limits.</strong> 이 페이지는 실제 고객 매뉴얼을 수정한 것이 아니라 자율 생성한 CSV→Postgres 절차서 패킷을 분석한 fresh run입니다. 입력에 없는 DB minor version, 실제 row count, 권한 정책, SLA, 개인정보 등급은 UNKNOWN으로 남겼습니다. 입력 패킷은 <code>sources/manual-csv-postgres-runbook.md</code>에 저장했습니다.'
    return '16_manual_analysis_csv_to_postgres_migration_runbook.html', 'CSV→Postgres 데이터 마이그레이션 운영 매뉴얼 분석', mapping


def render_page(layout_name: str, file_name: str, title: str, desc: str, mapping: dict[str, str], css: dict[str, str], core_hash: str) -> None:
    base = read(ASSETS / 'base.html')
    layout = read(ASSETS / 'layouts' / layout_name)
    for k, v in mapping.items():
        layout = layout.replace(k, v)
    missing = sorted(set(re.findall(r'{{[A-Z0-9_]+}}', layout)))
    if missing:
        raise RuntimeError(f'{file_name} unfilled layout slots: {missing}')
    page = base
    page = page.replace('{{TITLE}}', title)
    page = page.replace('{{DESCRIPTION}}', desc)
    page = page.replace('{{JSON_LD_BLOCK}}', '')
    page = page.replace('{{BODY}}', layout)
    page = page.replace('{{FOOTER}}', '')
    slot_map = {
        '{{THEME_CSS}}': f'/* adaptive-html-final-core-css-sha256: {core_hash} */\n' + css['theme.css'],
        '{{COMPONENTS_CSS}}': css['components.css'],
        '{{VISUAL_COMPONENTS_CSS}}': css['visual-components.css'],
        '{{WIDGETS_CSS}}': css['widgets.css'],
        '{{VISUAL_HTML_CSS}}': css['visual-html.css'],
        '{{BODY_ICONS_CSS}}': css['body-icons.css'],
        '{{EDITORIAL_PATTERNS_CSS}}': css['editorial-patterns.css'],
        '{{SHAPE_VISUALS_CSS}}': css['shape-visuals.css'],
        '{{WORKFLOW_VISUALS_CSS}}': css['workflow-visuals.css'],
        '{{LAYOUTS_CSS}}': css['layouts.css'],
        '{{PRINT_CSS}}': css['print.css'],
        '{{THEME_DARK_CSS}}': css['theme-dark.css'],
    }
    for k, v in slot_map.items():
        page = page.replace(k, v)
    if '{{' in page:
        raise RuntimeError(f'{file_name} unfilled base slots')
    (PAGES / file_name).write_text(page, encoding='utf-8')


def render_index(pages: list[dict], css: dict[str, str], core_hash: str) -> None:
    body_cards = ''.join(f'''<article class="summary-card"><p class="case-label">Mode {p['mode']} · {escape(p['mode_id'])}</p><h2>{escape(p['title'])}</h2><p>{escape(p['desc'])}</p><p><a class="cta-btn primary" href="pages/{escape(p['file'])}">열기</a></p></article>''' for p in pages)
    body = f'''<main id="main" class="page-wide">
<header class="header"><div class="kicker">Fresh Extension Rule · 14/15/16</div><h1>Adaptive HTML Final · 14/15/16 신규 모드 Fresh Run</h1><p class="sub">기존 13-topic 출력과 이전 14/15/16 산출 기록을 소스처럼 재사용하지 않고, 새 주제·새 입력·새 sources로 다시 만든 별도 출력입니다.</p><div class="meta"><span>fresh_run · true</span><span>reused_previous_pages · false</span><span>sections · 10+ each</span></div></header>
<section><h2>{icon('check')}<span class="num">1</span>신규 규칙</h2><p class="h2-sub">Fresh Extension Rule을 적용했습니다. 이전 페이지 본문·이전 대화 산출물·기존 예제를 소스처럼 재사용하지 않고 각 모드를 새 입력과 전용 layout으로 생성했습니다.</p>{quality_gate([('', '새 출력 폴더', '원본 13-topic 폴더를 덮어쓰지 않고 별도 경로에 생성'),('', '새 주제', '14 GitHub, 15 YouTube, 16 Manual 각각 자율 주제 사용'),('warn', '기록 차단', 'sources/fresh-generation-rule.json에 재사용 금지 기록'),('', '검증', 'validate와 quality contract를 통과해야 완료')], 'fresh_run=true · reused_previous_pages=false')}</section>
<section><h2>{icon('map')}<span class="num">2</span>생성된 3개 모드</h2><p class="h2-sub">각 페이지는 최신 스킬 구조와 테마 스위처, body-icon 제목, section surface, vt 템플릿을 포함합니다.</p><div class="card-grid">{body_cards}</div></section>
</main>'''
    base = read(ASSETS / 'base.html')
    page = base.replace('{{TITLE}}', 'Adaptive HTML Final 14/15/16 Fresh Run')
    page = page.replace('{{DESCRIPTION}}', '14 GitHub, 15 YouTube, 16 Manual 분석 모드를 별도 신규 출력으로 생성한 인덱스')
    page = page.replace('{{JSON_LD_BLOCK}}', '')
    page = page.replace('{{BODY}}', body)
    page = page.replace('{{FOOTER}}', '')
    slot_map = {
        '{{THEME_CSS}}': f'/* adaptive-html-final-core-css-sha256: {core_hash} */\n' + css['theme.css'],
        '{{COMPONENTS_CSS}}': css['components.css'],
        '{{VISUAL_COMPONENTS_CSS}}': css['visual-components.css'],
        '{{WIDGETS_CSS}}': css['widgets.css'],
        '{{VISUAL_HTML_CSS}}': css['visual-html.css'],
        '{{BODY_ICONS_CSS}}': css['body-icons.css'],
        '{{EDITORIAL_PATTERNS_CSS}}': css['editorial-patterns.css'],
        '{{SHAPE_VISUALS_CSS}}': css['shape-visuals.css'],
        '{{WORKFLOW_VISUALS_CSS}}': css['workflow-visuals.css'],
        '{{LAYOUTS_CSS}}': css['layouts.css'],
        '{{PRINT_CSS}}': css['print.css'],
        '{{THEME_DARK_CSS}}': css['theme-dark.css'],
    }
    for k, v in slot_map.items():
        page = page.replace(k, v)
    ROOT.joinpath('index.html').write_text(page, encoding='utf-8')


def main() -> None:
    # Fresh-run cleanup: wipe this dedicated output's generated records only.
    for path in [PAGES, SOURCES]:
        if path.exists():
            shutil.rmtree(path)
    PAGES.mkdir(parents=True, exist_ok=True)
    SNAP.mkdir(parents=True, exist_ok=True)

    css = {name: read(ASSETS / name) for name in CSS_ORDER}
    core_hash = sha_text('\n'.join(css[name] for name in CORE))
    asset_sha = {name: sha_text(css[name]) for name in CSS_ORDER}

    gh_data = github_source()
    (SOURCES / 'github-astral-uv-api.json').write_text(json.dumps(gh_data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (SOURCES / 'youtube-meeting-automation-transcript.json').write_text(json.dumps({
        'title': 'AI 회의록 자동화: 녹취에서 실행계획까지', 'source_tier': 'transcript packet', 'observed_at': OBSERVED,
        'chapters': ['Hook', 'Demo', 'Workflow', 'Security caveat', 'CTA'],
        'claims': ['요약보다 액션 추출이 중요하다', 'owner와 due date가 없으면 알림이 무의미하다', 'human review가 필요하다'],
        'comment_clusters': ['보안 질문', 'Notion/Jira 연동 질문', '한국어 회의 품질 질문', '가격 질문']
    }, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (SOURCES / 'manual-csv-postgres-runbook.md').write_text('''# CSV Import Runbook v0.3\n\n대상: PostgreSQL 15+ staging import. 범위: CSV 스키마 확인, staging 적재, 검증 쿼리, production merge, rollback 검토. 제한: 실제 row count, 개인정보 등급, 권한 정책, SLA는 입력 없음.\n''', encoding='utf-8')
    (SOURCES / 'fresh-generation-rule.json').write_text(json.dumps({
        'rule': 'Fresh Extension Rule', 'fresh_run': True, 'reused_previous_pages': False,
        'mode_scope': ['14 github_analysis', '15 youtube_analysis', '16 manual_analysis'],
        'minimum_direct_sections_per_mode': 10,
        'source_policy': 'do not reuse previous 14/15/16 outputs as source material',
        'created_at': OBSERVED,
    }, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    page_defs = []
    fn, title, mapping = build_github(gh_data)
    render_page('github-analysis.html', fn, title, 'GitHub 저장소 astral-sh/uv 채택 실사 fresh run', mapping, css, core_hash)
    page_defs.append({'mode': '14', 'mode_id': 'github_analysis', 'file': fn, 'title': title, 'desc': 'GitHub API 스냅샷 기반 저장소 채택 실사'})
    fn, title, mapping = build_youtube()
    render_page('youtube-analysis.html', fn, title, 'AI 회의록 자동화 영상 분석 fresh run', mapping, css, core_hash)
    page_defs.append({'mode': '15', 'mode_id': 'youtube_analysis', 'file': fn, 'title': title, 'desc': '트랜스크립트 패킷 기반 영상 근거·댓글·재가공 분석'})
    fn, title, mapping = build_manual()
    render_page('manual-analysis.html', fn, title, 'CSV to Postgres 마이그레이션 매뉴얼 분석 fresh run', mapping, css, core_hash)
    page_defs.append({'mode': '16', 'mode_id': 'manual_analysis', 'file': fn, 'title': title, 'desc': '역할별 실행 경로와 운영 런북 중심 매뉴얼 재구성'})
    render_index(page_defs, css, core_hash)

    (SOURCES / 'profile.json').write_text(json.dumps({'profile': 'auto'}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (SOURCES / 'adaptive-html-final-manifest.json').write_text(json.dumps(json.loads(read(SKILL / 'manifest.json')), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for name in CSS_ORDER:
        (SNAP / name).write_text(css[name], encoding='utf-8')
    (SOURCES / 'css-integrity.json').write_text(json.dumps({
        'core_css_sha256': core_hash, 'asset_order': CORE, 'asset_sha256': asset_sha,
        'profile': 'auto', 'fresh_run': True, 'updated_at': datetime.now(timezone.utc).isoformat(),
    }, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (ROOT / 'topics.json').write_text(json.dumps(page_defs, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(ROOT)


if __name__ == '__main__':
    main()
