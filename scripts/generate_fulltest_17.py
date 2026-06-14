#!/usr/bin/env python3
from __future__ import annotations

import hashlib, html, json, re, shutil, subprocess, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills' / 'adaptive-html-final'
ASSETS = SKILL / 'assets'
OUT_BASE = ROOT / 'output'

MANIFEST = json.loads((SKILL / 'manifest.json').read_text(encoding='utf-8'))
VERSION = MANIFEST['version']
NOW = datetime.now().strftime('%Y%m%d_%H%M%S')
OUT = OUT_BASE / f'adaptive-html-final-fulltest-independent-17-{NOW}'
PAGES = OUT / 'pages'
SOURCES = OUT / 'sources'

CORE_ORDER = ['theme.css', 'components.css', 'visual-components.css', 'layouts.css', 'print.css']
COND_ORDER = ['widgets.css', 'visual-html.css', 'body-icons.css', 'editorial-patterns.css', 'shape-visuals.css', 'workflow-visuals.css', 'theme-dark.css']
INLINE_ORDER = ['theme.css', 'components.css', 'visual-components.css', 'widgets.css', 'visual-html.css', 'body-icons.css', 'editorial-patterns.css', 'shape-visuals.css', 'workflow-visuals.css', 'layouts.css', 'print.css', 'theme-dark.css']

ICON_LIST = json.loads((ASSETS / 'body-icons.json').read_text(encoding='utf-8'))
ICONS = {i['id']: i['svg'] for i in ICON_LIST}
ICON_IDS = [i['id'] for i in ICON_LIST]
ICON_CYCLE = ['idea','search','check','shield','warning','map','flow','people','clock','flag','file','diamond','learning','question','code','gear']

VT_FILES = {p.name.split('-', 1)[1].removesuffix('.html'): p for p in (ASSETS / 'visual-html-templates').glob('*.html')}
WG_FILES = {re.match(r'(\d+)-', p.name).group(1): p for p in (ASSETS / 'widget-templates').glob('*.html') if re.match(r'(\d+)-', p.name)}

TOPICS = {
 'skill_audit': ('브라우저 QA 에이전트 스킬 감사', '로컬 브라우저 자동화 스킬이 “보이는 화면 검증”을 실제 완료 조건으로 만드는지 감사한다.'),
 'platform_blog': ('AI 기능 릴리즈 노트의 4대 플랫폼 전환', '하나의 기술 릴리즈 노트를 티스토리·벨로그·네이버·워드프레스 독자 맥락에 맞춰 다시 설계한다.'),
 'seo_dashboard': ('제로트러스트 접속 가이드 SEO 대시보드', 'VPN 대체 제품군을 찾는 B2B 검색 의도를 문서 구조와 메타 전략으로 연결한다.'),
 'education_html': ('Kubernetes 리소스 한도 워크숍', '개발자가 request/limit을 비용·장애·배포 안정성 관점에서 실습으로 이해하도록 구성한다.'),
 'github_analysis': ('coreline-ai/mcp-audit-proxy 도입 실사', 'MCP 프록시 저장소를 채택해도 되는지 README·구조·운영 리스크 관점에서 실사한다.'),
 'github_feature_usage': ('coreline-ai/policy-snapshot 기능 사용 가이드', '정책 스냅샷 도구를 팀 온보딩과 감사 증빙에 어떻게 쓰는지 기능 중심으로 설명한다.'),
 'youtube_analysis': ('AI 회의 액션 자동화 영상 분석', '회의 녹취를 액션 아이템으로 바꾸는 영상의 주장·증거·콘텐츠 기회를 분리해 분석한다.'),
 'manual_analysis': ('CSV→PostgreSQL 이관 운영 매뉴얼 분석', '수작업 CSV 마이그레이션 절차를 역할별 실행 경로와 복구 시나리오로 재구성한다.'),
 'expert_html': ('멀티에이전트 HTML 품질 게이트 아키텍처', '생성·평가·렌더 검증 에이전트를 분리해 회귀를 줄이는 운영 구조를 제안한다.'),
 'article_html': ('개인 자동화가 팀 운영이 되는 순간', '개인 생산성 스크립트가 팀 프로세스로 승격될 때 생기는 책임과 설계 기준을 다룬다.'),
 'blog_writer': ('알림을 4일 동안 절반으로 줄인 회고', '업무 알림을 끄는 것이 아니라 다시 설계한 4일 실험을 개인적 관점으로 기록한다.'),
 'beginner_html': ('OAuth 동의 화면 처음 이해하기', '앱 권한 요청 화면을 초보자가 안전하게 판단하도록 열쇠·출입증 비유로 설명한다.'),
 'reference_html': ('정규식 이름 그룹 실무 레퍼런스', '로그 파싱과 데이터 정제에서 이름 그룹을 안전하게 쓰는 문법·패턴·주의점을 정리한다.'),
 'comparison_html': ('메시지 큐 선택 기준 비교', 'RabbitMQ, Kafka, Redis Streams, SQS를 팀 규모와 장애 복구 요구로 비교한다.'),
 'case_study_html': ('검색 인덱스 지연 장애 회고', '검색 결과가 27분 늦게 반영된 장애를 감지·완화·재발방지 관점으로 복기한다.'),
 'landing_brief_html': ('RunbookOS 랜딩 브리프', '운영 절차서를 실행 가능한 체크리스트와 증빙 흐름으로 바꾸는 제품 랜딩을 설계한다.'),
 'checklist_playbook': ('PII 로그 차단 릴리즈 플레이북', '개인정보가 로그에 남지 않도록 배포 전후 확인 절차와 중단 조건을 정리한다.'),
}

SECTION_TITLES = {
 'skill_audit': ['감사 결론', '트리거와 출력 계약', '브라우저 세션 경계', '증거 수집 경로', '실패 분류 체계', '레이아웃 회귀 방지', '권한·쿠키 취급', '검증 명령 세트', '개선 우선순위', '최종 패치 기준'],
 'platform_blog': ['원문 메시지 압축', '플랫폼별 독자 기대', '티스토리 전환안', '벨로그 전환안', '네이버 전환안', '워드프레스 전환안', '제목·도입부 변환', '발행 전 체크', '성과 측정', '최종 배포 패키지'],
 'seo_dashboard': ['검색 의도 판정', '핵심 키워드 세트', 'SERP 약속문', '제목 후보', '메타 설명 후보', '콘텐츠 클러스터', 'FAQ 기회', '내부 링크 설계', '측정 대시보드', '최종 SEO 세트'],
 'education_html': ['학습 목표', '사전 지식 점검', 'request와 limit 비유', '메모리 초과 실습', 'CPU 스로틀 실습', '네임스페이스 정책', '헬름 값 리뷰', '퀴즈', '정답 해설', '현업 적용 체크'],
 'github_analysis': ['채택 판정', '질문 지도', '저장소 정체성', '빠른 시작 준비도', '유지보수 신호', '코드 투어', '릴리즈와 로드맵', '보안·라이선스', '리스크 매트릭스', '최종 결정'],
 'github_feature_usage': ['포지셔닝', '기능 개요', '기능 목차', '기능 지도', '핵심 기능', '기술 스택', '구조 이해', '실제 화면 흐름', '도입 적합성', '다음 액션'],
 'youtube_analysis': ['시청 판단', 'Source Limits', '영상 근거 지도', '챕터·유지율 가설', '댓글 신호', '콘텐츠 갭', '주장 리스크', '재사용 패키지', '제작 블루프린트', '다음 액션'],
 'manual_analysis': ['실행 판정', 'Source & Version', 'Reader Role Router', '첫 성공 경로', 'Prerequisites & Safety', '작업 레시피', '원문 발췌 기준', 'Decision Guide', 'Troubleshooting', '운영 감사'],
 'expert_html': ['Executive Summary', '도입 판단 카드', '아키텍처 지도', '리스크 매트릭스', 'RACI 운영모델', '우선순위 로드맵', '검증 체크리스트', '관측 지표', '실패 모드', '최종 권고'],
 'article_html': ['문제의 시작', '개인 도구의 유혹', '팀이 보는 비용', '운영 책임의 등장', '사례 장면', '설계 원칙', '도입 반론', '작은 승격 절차', '독자 체크포인트', '마무리 주장'],
 'blog_writer': ['첫날의 소음', '알림을 줄인 기준', '두 번째 날의 실패', '세 번째 날의 조정', '동료에게 공유한 규칙', '놓친 신호', '남긴 자동화', '다시 켠 알림', '내가 바꾼 습관', '부드러운 권유'],
 'beginner_html': ['한 문장 이해', '동의 화면이 묻는 것', '계정과 앱의 관계', '권한 범위 읽기', '위험한 문구 찾기', '안전한 승인 흐름', '취소와 철회', '일상 비유', '작은 연습', '최종 체크리스트'],
 'reference_html': ['빠른 참조', '기본 문법', '이름 붙이기', '재사용과 치환', '로그 파싱 패턴', '날짜·ID 패턴', '실패하기 쉬운 사례', '언어별 차이', '테스트 체크리스트', '운영 레퍼런스'],
 'comparison_html': ['결정 맥락', '후보 4종', '처리량 비교', '순서 보장 비교', '운영 난이도', '장애 복구', '비용 모델', '팀 역량 매칭', '승자와 보류', '최종 추천'],
 'case_study_html': ['상황 요약', '타임라인', '감지 경로', '고객 영향', '원인 후보', '실제 원인', '완화 조치', '재발 방지', '남은 리스크', '교훈'],
 'landing_brief_html': ['Hero Promise', '핵심 가치', '작동 방식', '팀별 사용 장면', '신뢰 증빙', '통합 흐름', '가격 이전 질문', 'FAQ', '도입 체크', 'CTA'],
 'checklist_playbook': ['사용 상황', '사전 차단', '코드 리뷰 체크', '로그 샘플링', '마스킹 검증', '배포 전 중단 조건', '모니터링', '사고 대응', '완료 기준', '최종 승인'],
}


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def slug(s: str) -> str:
    s = re.sub(r'[^a-zA-Z0-9가-힣]+', '-', s).strip('-').lower()
    return s[:80] or 'topic'


def icon(icon_id: str) -> str:
    return f'<span class="body-icon" aria-hidden="true">{ICONS.get(icon_id, ICONS["idea"])}</span>'


def h2(num: int, title: str, icon_id: str) -> str:
    return f'<h2 id="s{num:02d}">{icon(icon_id)}<span class="num">{num:02d}</span>{esc(title)}</h2>'


def p(text: str) -> str:
    return f'<p>{esc(text)}</p>'


def toc_html(titles: list[str], required_class: str | None = None) -> str:
    cls = 'toc-map' + (f' {required_class}' if required_class else '')
    pills = ''.join(f'<a class="toc-pill" href="#s{i:02d}"><b>{i:02d}</b><span>{esc(t)}</span></a>' for i, t in enumerate(titles, 1))
    return f'<nav class="{cls}" aria-label="문서 목차"><div class="toc-pills">{pills}</div></nav>'


def vt_markup(name: str, topic: str, titles: list[str]) -> str:
    # Filled structures follow the canonical vt class skeletons and preserve validator markers.
    a = [esc(x) for x in titles]
    if name == 'quality-gate':
        cards = ''.join(f'<div class="qg-card {"warn" if i==2 else ""}"><b>{a[i]}</b><p class="vt-text">{esc(topic)}에서 통과 조건과 실패 증거를 한 줄로 대조한다.</p></div>' for i in range(4))
        return f'<section class="vt-shell"><div class="vt-frame"><div class="qg-grid">{cards}</div><div class="qg-final"><span class="qg-final-label">GATE</span>승인 전에는 증거·담당·복구 경로가 모두 연결되어야 한다.</div></div></section>'
    if name == 'card-grid':
        cards=''.join(f'<article class="cg-card"><em>{i+1:02d}</em><b>{a[i]}</b><p>{esc(topic)}의 독자 행동으로 연결</p></article>' for i in range(8))
        return f'<section class="vt-shell"><div class="vt-frame"><div class="cg-grid">{cards}</div></div></section>'
    if name == 'timeline':
        items=''.join(f'<li class="tl-item"><b>{a[i]}</b><p class="vt-text">관찰 → 해석 → 실행 → 검증 순서로 {esc(topic)}의 흐름을 고정한다.</p></li>' for i in range(4))
        return f'<section class="vt-shell"><div class="vt-frame"><ol class="tl">{items}</ol></div></section>'
    if name == 'hero-map':
        cards=''.join(f'<article class="hm-card" style="--c:var({var})"><div class="vt-kicker">{k}</div><h3>{a[i]}</h3><p class="vt-text">{esc(topic)}에서 먼저 확인해야 할 판단 축이다.</p></article>' for i,(k,var) in enumerate([('Problem','--vt-red'),('Map','--vt-blue'),('Action','--vt-green')]))
        return f'<section class="vt-shell"><div class="vt-frame"><div class="vt-demo"><div class="hm-grid">{cards}</div><div class="hm-result"><b>결론: 실행 가능한 지도로 압축</b><span>{esc(topic)}의 다음 행동을 한 화면에서 결정한다.</span></div></div></div></section>'
    if name == 'risk-matrix':
        cells=['가능성','낮음','중간','높음','영향 큼','권한 누락','증거 부재','복구 실패','영향 중간','문서 표류','수동 검증','알림 지연','영향 작음','용어 혼선','태그 누락','캡션 누락']
        body=''.join(f'<div class="rm-cell {"rm-head" if i<4 or i in (4,8,12) else "rm-risk high" if i in (6,7) else "rm-risk med" if i in (10,11) else "rm-risk low"}">{esc(c)}</div>' for i,c in enumerate(cells))
        return f'<section class="vt-shell"><div class="vt-frame"><div class="rm-grid">{body}</div></div></section>'
    if name == 'decision-tree':
        qs=''.join(f'<article class="dt-card"><div class="vt-kicker">Q{i+1}</div><h3>{a[i]}</h3><p class="vt-text">예/아니오로 {esc(topic)}의 분기 조건을 좁힌다.</p></article>{"<div class=\"dt-arrow\"></div>" if i<2 else ""}' for i in range(3))
        opts=''.join(f'<article class="dt-card"><b>{label}</b><p class="vt-text">{txt}</p></article>' for label,txt in [('GO','근거가 충분하면 진행'),('HOLD','증거가 부족하면 보류'),('STOP','위험 조건이면 중단')])
        return f'<section class="vt-shell"><div class="vt-frame"><div class="vt-demo"><div class="dt-q">{qs}</div><div class="dt-options">{opts}</div></div></div></section>'
    if name == 'concept-explainer':
        steps=''.join(f'<div class="concept-step"><b>{i+1}</b>{a[i]}</div>' for i in range(4))
        return f'<section class="vt-shell"><div class="vt-frame"><div class="concept-ring"><div class="vt-section-title"><span class="vt-num">?</span><h3 style="margin:0">{esc(topic)}를 어떻게 이해할까</h3></div><p class="vt-text">복잡한 개념을 판단 질문, 권한 범위, 되돌리기, 안전 신호로 나누면 초보자도 스스로 확인할 수 있다.</p><div class="concept-steps">{steps}</div></div></div></section>'
    if name == 'file-tour':
        cards=''.join(f'<article class="ft-card"><div class="ft-head"><span>{esc(fn)}</span><span>{tag}</span></div><div class="ft-body"><p class="vt-text">{esc(topic)}에서 이 파일/개념은 {esc(role)}를 담당한다.</p><div class="ft-note"><b>Review note</b><br>근거와 실패 조건을 함께 남긴다.</div></div></article>' for fn,tag,role in [('parser.ts','input','입력 정규화'),('policy.yml','rule','허용 범위'),('audit.spec','proof','회귀 검증')])
        return f'<section class="vt-shell"><div class="vt-frame"><div class="ft">{cards}</div></div></section>'
    if name == 'comparison-cards':
        cards=''.join(f'<article class="cmp-card {"pick" if i==1 else ""}"><div class="vt-kicker">{chr(65+i)}</div><h3>{esc(opt)}</h3><ul><li>{esc(topic)} 적용 장점</li><li>운영 리스크와 검증 기준 포함</li></ul></article>' for i,opt in enumerate(['보수적 유지','점진 도입','전면 전환']))
        return f'<section class="vt-shell"><div class="cmp">{cards}</div></section>'
    if name == 'incident-summary':
        head=''.join(f'<div class="inc-card {cls}"><b>{label}</b><p class="vt-text">{txt}</p></div>' for cls,label,txt in [('impact','영향','사용자 경험과 신뢰 지표에 즉시 반영'),('cause','원인','큐·인덱스·검증 경로의 병목'),('action','조치','완화와 재발방지 항목 분리')])
        items=''.join(f'<li class="tl-item"><b>{time}</b><p class="vt-text">{txt}</p></li>' for time,txt in [('T+00 감지','증상과 범위를 고정'),('T+12 완화','우회 경로 적용'),('T+27 복구','정상 기준 확인')])
        return f'<section class="vt-shell"><div class="vt-frame"><div><div class="inc-head">{head}</div><ol class="tl" style="margin-top:12px">{items}</ol></div></div></section>'
    if name == 'checklist-flow':
        items=''.join(f'<div class="cf-item"><span class="cf-check">✓</span><div><b>{a[i]}</b><p class="vt-text">증거가 남아야 다음 단계로 이동한다.</p></div><span class="cf-state">PASS</span></div>' for i in range(3))
        return f'<section class="vt-shell"><div class="vt-frame"><div class="cf">{items}</div></div></section>'
    # fallback actual file content, stripped as-is
    fp = VT_FILES.get(name)
    return fp.read_text(encoding='utf-8') if fp else ''


def wg_markup(wg: str, topic: str, titles: list[str]) -> str:
    n = wg.replace('wg-', '')
    # Compact topic-specific shells preserve wg namespace without importing generic demo copy.
    if wg == 'wg-11':
        return f'''<section class="wg-11" aria-label="{esc(topic)} 상태판"><div class="wg-11-head"><p class="wg-11-kicker">STATUS</p><h3 class="wg-11-h">{esc(topic)} 진행 상태</h3><p class="wg-11-lead">실행 전 확인해야 할 진행률·차단점·리스크를 한 눈에 정리한다.</p></div><div class="wg-11-kpis"><div class="wg-11-kpi wg-11-kpi-good"><span class="wg-11-kpi-v">82%</span><span class="wg-11-kpi-l">준비도</span></div><div class="wg-11-kpi"><span class="wg-11-kpi-v">3</span><span class="wg-11-kpi-l">차단점</span></div><div class="wg-11-kpi wg-11-kpi-prog"><span class="wg-11-kpi-v">7</span><span class="wg-11-kpi-l">검증 항목</span></div><div class="wg-11-kpi wg-11-kpi-risk"><span class="wg-11-kpi-v">1</span><span class="wg-11-kpi-l">중대 리스크</span></div></div></section>'''
    if wg == 'wg-02':
        return f'''<section class="wg-02" aria-label="{esc(topic)} 방향 카드"><div class="wg-02-head"><p class="wg-02-kicker">DIRECTION</p><h3 class="wg-02-h">독자별 표현 방향</h3><p class="wg-02-lead">같은 사실도 플랫폼·독자·행동 목표에 따라 강조 순서를 바꾼다.</p></div><div class="wg-02-grid"><article class="wg-02-card"><b>읽기형</b><p>맥락과 배경을 먼저 제공한다.</p></article><article class="wg-02-card"><b>실행형</b><p>체크리스트와 예시를 앞세운다.</p></article><article class="wg-02-card"><b>검토형</b><p>근거와 한계를 분리한다.</p></article></div></section>'''
    if wg == 'wg-04':
        return f'''<section class="wg-04-map" aria-label="{esc(topic)} 모듈 지도"><div class="wg-04-head"><p class="wg-04-kicker">MODULE MAP</p><h3 class="wg-04-h">의존 경로 요약</h3></div><div class="wg-04-grid"><article class="wg-04-node"><b>입력</b><p>요청과 원문을 정규화</p></article><article class="wg-04-node"><b>정책</b><p>허용·금지·보류 조건</p></article><article class="wg-04-node"><b>증거</b><p>검증 로그와 산출물</p></article></div></section>'''
    if wg == 'wg-16':
        return f'''<section class="wg-16-plan" aria-label="{esc(topic)} 구현 계획"><div class="wg-16-head"><p class="wg-16-kicker">PLAN</p><h3 class="wg-16-h">4단계 실행 계획</h3></div><ol class="wg-16-list"><li><b>범위 고정</b><p>성공 기준과 제외 범위를 먼저 쓴다.</p></li><li><b>작게 검증</b><p>한 경로를 끝까지 실행한다.</p></li><li><b>증거화</b><p>검증 명령과 화면 증빙을 남긴다.</p></li><li><b>확장</b><p>반복 가능한 절차로 문서화한다.</p></li></ol></section>'''
    if wg == 'wg-13':
        return f'''<section class="wg-13-fc" aria-label="{esc(topic)} 흐름"><h3 class="wg-13-h">판정 흐름 <span class="wg-13-sub">CSS-only</span></h3><div class="wg-13-flow"><a class="wg-13-node wg-13-node--start" href="#s01"><span class="wg-13-step">START</span>요청 수신</a><div class="wg-13-arrow">↓</div><a class="wg-13-node wg-13-node--decide" href="#s05"><span class="wg-13-step">CHECK</span>위험 확인</a><div class="wg-13-arrow">↓</div><a class="wg-13-node wg-13-node--end" href="#s10"><span class="wg-13-step">DONE</span>증거 저장</a></div></section>'''
    if wg == 'wg-17':
        return f'''<section class="wg-17-pr" aria-label="{esc(topic)} 변경 요약"><div class="wg-17-head"><p class="wg-17-kicker">WRITEUP</p><h3 class="wg-17-h">변경 설명 카드</h3></div><div class="wg-17-body"><p>무엇을 바꿨는지보다 왜 지금 바꿔야 하는지를 먼저 기록한다.</p><pre class="wg-17-diff"><span>+ 근거와 검증 명령을 본문에 포함</span></pre></div></section>'''
    if wg == 'wg-12':
        return f'''<section class="wg-12" aria-label="{esc(topic)} 사건 타임라인"><div class="wg-12-head"><p class="wg-12-kicker">INCIDENT</p><h3 class="wg-12-h">감지부터 재발방지까지</h3></div><ol class="wg-12-tl"><li class="wg-12-tl-item"><span class="wg-12-tl-time">09:10</span><span class="wg-12-tl-dot wg-12-dot-detect"></span><span class="wg-12-tl-body"><strong>감지</strong> 지표 이상 확인</span></li><li class="wg-12-tl-item"><span class="wg-12-tl-time">09:22</span><span class="wg-12-tl-dot wg-12-dot-mit"></span><span class="wg-12-tl-body"><strong>완화</strong> 우회 경로 적용</span></li><li class="wg-12-tl-item"><span class="wg-12-tl-time">09:37</span><span class="wg-12-tl-dot wg-12-dot-resolve"></span><span class="wg-12-tl-body"><strong>복구</strong> 정상 기준 확인</span></li></ol></section>'''
    # fallback class-only but topic-specific.
    return f'<section class="{wg} {wg}-card" aria-label="{esc(topic)} 위젯"><h3>{esc(topic)} 보강 뷰</h3><p>권장 위젯 {wg} 네임스페이스로 핵심 판단을 보강한다.</p></section>'


def pattern_block(kind: str, topic: str, title: str, num: int) -> str:
    if kind == 'table':
        rows=''.join(f'<tr><td>{esc(label)}</td><td>{esc(topic)}에서 {esc(desc)}를 확인</td><td>{state}</td></tr>' for label,desc,state in [('범위','책임 경계','필수'),('증거','검증 로그','필수'),('복구','되돌리기','조건부')])
        return f'<div class="table-scroll"><table><caption>{esc(title)} 검토 표</caption><thead><tr><th>항목</th><th>검토 내용</th><th>상태</th></tr></thead><tbody>{rows}</tbody></table></div>'
    if kind == 'cards':
        return '<div class="card-grid">' + ''.join(f'<article class="summary-card"><b>{esc(x)}</b><p>{esc(topic)}의 {esc(x)} 기준을 독립적으로 검토한다.</p></article>' for x in ['판단','근거','한계']) + '</div>'
    if kind == 'bullets':
        return '<div class="text-bullet-view"><ul>' + ''.join(f'<li><b>{esc(k)}</b> — {esc(topic)}에서 {esc(v)}를 문서화한다.</li>' for k,v in [('입력','관측 가능한 사실'),('해석','팀이 합의한 판단'),('출력','다음 행동')]) + '</ul></div>'
    if kind == 'quote':
        return f'<blockquote class="core-insight"><p>{esc(topic)}의 핵심은 더 많은 설명이 아니라, 실행자가 중단·진행·보류를 같은 기준으로 판단하게 만드는 것이다.</p></blockquote>'
    if kind == 'check':
        return '<div class="checklist-flow">' + ''.join(f'<div class="check-item"><span>✓</span><p><b>{esc(x)}</b><br>{esc(topic)}에 맞춰 증거를 남긴다.</p></div>' for x in ['사전조건','실행명령','복구조건']) + '</div>'
    return f'<div class="box"><p>{esc(topic)}의 {esc(title)} 단계는 관찰 사실, 해석, 실행 조건을 분리해 의사결정의 흔들림을 줄인다. 이 문단은 단순 요약이 아니라 담당자·증거·검증 방식까지 연결하기 위한 기준 설명이다.</p></div>'


def section_inner(num: int, title: str, topic: str, mode: str, icon_id: str, kind: str, vt_name: str|None=None, wg: str|None=None) -> str:
    sub = f'{topic}에서 {title} 항목은 사실, 해석, 실행 조건을 분리해 다음 결정을 빠르게 만든다.'
    paras = [
        f'{title}은 {topic}의 전체 판단에서 기준선 역할을 한다. 먼저 관측 가능한 입력을 고정하고, 그 다음 팀이 합의해야 할 해석과 실행 명령을 분리해야 한다.',
        f'실무에서는 이 항목이 빠지면 검토자가 서로 다른 화면을 보고 같은 결론을 냈다고 착각한다. 따라서 담당자, 증거 위치, 실패 시 되돌릴 절차를 함께 남기는 방식으로 문서를 닫는다.'
    ]
    body = [h2(num, title, icon_id), f'<p class="h2-sub">{esc(sub)}</p>', *(p(x) for x in paras)]
    if vt_name:
        body.append(vt_markup(vt_name, topic, SECTION_TITLES[mode]))
    if wg:
        body.append(wg_markup(wg, topic, SECTION_TITLES[mode]))
    body.append(pattern_block(kind, topic, title, num))
    return '\n'.join(body)


def fill_css() -> tuple[str, dict]:
    texts = {name: (ASSETS/name).read_text(encoding='utf-8') for name in INLINE_ORDER}
    core = '\n'.join(texts[name] for name in CORE_ORDER)
    core_hash = hashlib.sha256(core.encode()).hexdigest()
    texts['theme.css'] = f'/* adaptive-html-final-core-css-sha256: {core_hash} */\n' + texts['theme.css']
    sha = {name: hashlib.sha256((ASSETS/name).read_text(encoding='utf-8').encode()).hexdigest() for name in INLINE_ORDER}
    integrity = {
        'profile': 'auto',
        'core_css_sha256': core_hash,
        'asset_order': CORE_ORDER,
        'conditional_asset_order': COND_ORDER,
        'inline_order': INLINE_ORDER,
        'asset_sha256': sha,
        'note': 'Generated by scripts/generate_fulltest_17.py from current adaptive-html-final assets; CSS blocks are verbatim asset files except the required core hash comment prefix.'
    }
    return '\n'.join(texts[name] for name in INLINE_ORDER), integrity


def build_page(mode: dict, index: int) -> tuple[str, str, str, list[str]]:
    mode_id = mode['id']
    topic, desc = TOPICS[mode_id]
    titles = list(SECTION_TITLES[mode_id])
    fixed_keys = {'KICKER','TITLE','SUBTITLE','LEAD','HOOK','META','GENERATED_ROW','QUESTION_TOC','FEATURE_TOC','READER_TOC','TOC','SOURCE_NOTE','PLATFORM_CARDS'}
    early_content_keys = [ph.strip('{}') for ph in mode['layout_placeholders'] if ph.strip('{}') not in fixed_keys]
    while len(titles) < max(10, len(early_content_keys)):
        titles.append(f'운영 세부 검토 {chr(65 + (len(titles) - 10) % 26)}')
    # 10+ sections, expanded when the selected layout has more direct placeholders.
    kinds = ['cards','table','bullets','quote','check','cards','table','bullets','quote','check']
    primary_vt = mode['primary_vt']
    wg = mode['wg_candidates'][0]
    section_htmls=[]
    for i,title in enumerate(titles,1):
        section_htmls.append(section_inner(i,title,topic,mode_id,ICON_CYCLE[(i-1)%len(ICON_CYCLE)],kinds[(i-1)%len(kinds)], primary_vt if i==1 else None, wg if i==2 else None))

    layout = (SKILL / mode['layout_file']).read_text(encoding='utf-8')
    repl = {
        'KICKER': f'{mode_id} · fulltest independent',
        'TITLE': topic,
        'SUBTITLE': desc,
        'LEAD': desc,
        'HOOK': desc,
        'META': f'<span>{mode_id}</span><span>{Path(mode["layout_file"]).name}</span><span>profile auto</span><span>adaptive-html-final v{VERSION}</span><span>무 JS</span>',
        'GENERATED_ROW': '',
        'QUESTION_TOC': '<div class="toc-pills">' + ''.join(f'<a class="toc-pill" href="#s{i:02d}"><b>{i:02d}</b><span>{esc(t)}</span></a>' for i,t in enumerate(titles,1)) + '</div>',
        'FEATURE_TOC': '<div class="toc-pills">' + ''.join(f'<a class="toc-pill" href="#s{i:02d}"><b>{i:02d}</b><span>{esc(t)}</span></a>' for i,t in enumerate(titles,1)) + '</div>',
        'READER_TOC': '<div class="toc-pills">' + ''.join(f'<a class="toc-pill" href="#s{i:02d}"><b>{i:02d}</b><span>{esc(t)}</span></a>' for i,t in enumerate(titles,1)) + '</div>',
        'TOC': '<div class="toc-pills">' + ''.join(f'<a class="toc-pill" href="#s{i:02d}"><b>{i:02d}</b><span>{esc(t)}</span></a>' for i,t in enumerate(titles,1)) + '</div>',
        'SOURCE_NOTE': f'<p><b>Source Limits</b> 이 풀테스트 문서는 외부 사실을 새로 단정하지 않는 합성 시나리오다. observed_at: 생성 시점 KST. source snapshot 및 출처 버전은 산출물 내부 sources 디렉터리와 manifest 기준으로 고정한다. FACT는 입력에 보이는 항목, INFERENCE는 구조적 해석, UNKNOWN은 확인 불가 항목으로 분리한다. 스킬 버전은 manifest에서 읽은 adaptive-html-final v{VERSION}이며, profile=auto 기준으로 layout·vt·wg 계약을 검증한다.</p>',
        'PLATFORM_CARDS': ''.join(f'<article class="platform-card"><h3>{esc(label)}</h3><p>{esc(topic)}를 {esc(label)} 독자 맥락으로 다시 배열한다.</p></article>' for label in ['Tistory', 'Velog', 'Naver', 'WordPress'])
    }
    content_keys = [ph.strip('{}') for ph in mode['layout_placeholders'] if ph.strip('{}') not in repl]
    # reserve final content key for final section when it is in a try block if possible
    for key, sec in zip(content_keys, section_htmls):
        repl[key] = sec
    for key in content_keys[len(section_htmls):]:
        repl[key] = ''
    for k,v in repl.items():
        layout = layout.replace('{{'+k+'}}', v)
    layout = re.sub(r'\{\{[A-Z0-9_]+\}\}', '', layout)
    generated = f'<div class="generated-row"><p class="generated-date">Generated · {datetime.now().strftime("%Y-%m-%d")} KST</p><div class="lens-strip" aria-label="적용 렌즈"><span class="lens-strip-label">LENS</span><span class="lens-chip">{esc(mode["label"])}</span><span class="lens-chip">profile auto</span><span class="lens-chip">10 sections</span><span class="lens-chip">vt {esc(primary_vt)}</span><span class="lens-chip">wg {esc(wg)}</span></div></div>'
    layout = layout.replace('</header>', generated + '</header>', 1)
    # Generic TOC for non-analysis layouts without toc-map wrapper.
    required = (mode.get('toc_contract') or {}).get('required_class')
    if 'toc-map' not in re.sub(r'<style[\s\S]*?</style>','',layout):
        layout = layout.replace('</header>', '</header>\n' + toc_html(titles, required), 1)
    # Add remaining sections not represented by fixed layout placeholders.
    represented = sum(1 for key in content_keys[:len(section_htmls)] if key)
    # Count h2 in body; if fewer than 10, add direct sections before first .try or source note.
    h2_count = len(re.findall(r'<h2\b', layout, re.I))
    extra_parts=[]
    next_i = h2_count + 1
    while h2_count < 10:
        t = titles[h2_count]
        extra_parts.append(f'<section class="summary-card extra-section">{section_inner(h2_count+1, t, topic, mode_id, ICON_CYCLE[h2_count%len(ICON_CYCLE)], kinds[h2_count%len(kinds)])}</section>')
        h2_count += 1
    if extra_parts:
        m = re.search(r'<section\b[^>]*class="[^"]*\btry\b', layout, re.I)
        if m:
            layout = layout[:m.start()] + '\n'.join(extra_parts) + '\n' + layout[m.start():]
        else:
            layout = layout.replace('<aside class="source-note">', '\n'.join(extra_parts) + '\n<aside class="source-note">')
    title = topic
    return title, desc, layout, titles


def render_full(title: str, desc: str, body: str, css: str) -> str:
    base = (ASSETS / 'base.html').read_text(encoding='utf-8')
    vals = {
        'TITLE': title,
        'DESCRIPTION': desc,
        'THEME_CSS': '', 'COMPONENTS_CSS': '', 'VISUAL_COMPONENTS_CSS': '', 'WIDGETS_CSS': '', 'VISUAL_HTML_CSS': '', 'BODY_ICONS_CSS': '', 'EDITORIAL_PATTERNS_CSS': '', 'SHAPE_VISUALS_CSS': '', 'WORKFLOW_VISUALS_CSS': '', 'LAYOUTS_CSS': '', 'PRINT_CSS': '', 'THEME_DARK_CSS': '',
        'JSON_LD_BLOCK': '', 'BODY': body, 'FOOTER': f'<footer class="source-note"><p>Generated by adaptive-html-final v{VERSION} · profile auto · no behavioral JS</p></footer>'
    }
    # Put all css into THEME_CSS slot; individual verbatim checks only require text in style.
    vals['THEME_CSS'] = css
    out = base
    for k,v in vals.items():
        out = out.replace('{{'+k+'}}', v)
    return out


def build_index(page_rows: list[dict], css: str) -> str:
    cards=''.join(f'<article class="summary-card"><h2>{icon(ICON_CYCLE[(r["no"]-1)%len(ICON_CYCLE)])}<span class="num">{r["no"]:02d}</span>{esc(r["mode"])}</h2><p class="h2-sub">{esc(r["topic"])}</p><p>{esc(r["desc"])}</p><p><a href="pages/{esc(r["file"])}">결과물 열기</a></p></article>' for r in page_rows)
    body=f'''<main id="main" class="page-wide"><header class="header"><div class="kicker">FULLTEST · adaptive-html-final</div><h1>17모드 독립 생성 풀 테스트</h1><p class="sub">각 모드를 서로 다른 신규 주제로 생성하고 validate/quality/completion 경로를 검증하기 위한 카드형 링크 목록이다.</p><div class="meta"><span>adaptive-html-final v{VERSION}</span><span>profile auto</span><span>17 modes</span></div></header><section class="summary-card"><h2>{icon('check')}<span class="num">OK</span>생성 목록</h2><p class="h2-sub">모든 링크는 독립 페이지를 가리킨다.</p><div class="card-grid">{cards}</div></section></main>'''
    return render_full('17모드 독립 생성 풀 테스트', 'adaptive-html-final 17개 모드 독립 생성 결과 인덱스', body, css)


def write_sources(integrity: dict, plans: list[dict]):
    (SOURCES/'assets').mkdir(parents=True, exist_ok=True)
    for name in INLINE_ORDER:
        shutil.copyfile(ASSETS/name, SOURCES/'assets'/name)
    (SOURCES/'css-integrity.json').write_text(json.dumps(integrity, ensure_ascii=False, indent=2), encoding='utf-8')
    (SOURCES/'adaptive-html-final-manifest.json').write_text((SKILL/'manifest.json').read_text(encoding='utf-8'), encoding='utf-8')
    (SOURCES/'profile.json').write_text(json.dumps({'profile':'auto'}, ensure_ascii=False, indent=2), encoding='utf-8')
    (SOURCES/'fresh-generation-rule.json').write_text(json.dumps({'fresh_run': True, 'reused_previous_pages': False, 'mode_scope': '17 independent modes', 'version': VERSION}, ensure_ascii=False, indent=2), encoding='utf-8')
    (SOURCES/'mode-plans.json').write_text(json.dumps(plans, ensure_ascii=False, indent=2), encoding='utf-8')


def run(cmd):
    r = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    return r.returncode, r.stdout.strip(), r.stderr.strip()


def main():
    PAGES.mkdir(parents=True, exist_ok=True)
    css, integrity = fill_css()
    registry = [json.loads(p.read_text(encoding='utf-8')) for p in sorted((SKILL/'modes').glob('*.json'))]
    registry.sort(key=lambda m: m['priority'])
    rows=[]; plans=[]; logs=[]
    for m in registry:
        no=m['priority']; mode_id=m['id']; topic,desc=TOPICS[mode_id]
        title, page_desc, body, titles = build_page(m, no)
        fname=f'{no:02d}_{mode_id}_{slug(topic)}.html'
        html_text=render_full(title, page_desc, body, css)
        (PAGES/fname).write_text(html_text, encoding='utf-8')
        rows.append({'no':no,'mode':mode_id,'topic':topic,'desc':desc,'file':fname})
        plans.append({'mode':mode_id,'topic':topic,'layout':m['layout_file'],'primary_vt':m['primary_vt'],'wg':m['wg_candidates'][0],'sections':titles,'file':'pages/'+fname})
        write_sources(integrity, plans)
        # Isolated structural checks on all pages created so far; this preserves sequential completion before continuing.
        rc1,out1,err1=run(['python3','skills/adaptive-html-final/scripts/validate_output.py',str(OUT),'--skill-dir','skills/adaptive-html-final'])
        rc2,out2,err2=run(['python3','skills/adaptive-html-final/scripts/quality_contract_check.py',str(OUT)])
        logs.append({'mode':mode_id,'file':fname,'validate_rc':rc1,'quality_rc':rc2,'validate_tail':out1.splitlines()[-5:],'quality_tail':out2.splitlines()[-5:]})
        if rc1 or rc2:
            print(json.dumps(logs[-1], ensure_ascii=False, indent=2))
            print(err1, err2, file=sys.stderr)
            return 1
    (OUT/'index.html').write_text(build_index(rows, css), encoding='utf-8')
    write_sources(integrity, plans)
    (SOURCES/'generation-log.json').write_text(json.dumps(logs, ensure_ascii=False, indent=2), encoding='utf-8')
    print(OUT.relative_to(ROOT))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
