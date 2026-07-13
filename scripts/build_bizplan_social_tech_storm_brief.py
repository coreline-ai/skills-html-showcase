#!/usr/bin/env python3
"""Build a current adaptive-html-final landing brief from bizplan-social-tech-demo-2026 + STORM research.

Selected topic:
  폐쇄형 보호시설 영상AI 위험상황 신속대응 R&D 실증사업 브리프

The local package has no SKILL.md, so its project corpus is treated as the skill content source.
"""
from __future__ import annotations

import hashlib
import html
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "adaptive-html-final"
ASSETS = SKILL / "assets"
BIZ = ROOT / "orginal_skill" / "bizplan-social-tech-demo-2026"
STORM = ROOT / "orginal_skill" / "storm-research"

OUT = ROOT / "output" / "2026-06-20" / "bizplan-social-tech-demo-2026-storm-brief"
SOURCES = OUT / "sources"

MODE = "landing_brief_html"
PROFILE = "auto"
LAYOUT = "landing-brief.html"
LAYOUT_CLASS = "layout-landing"
PRIMARY_VT = "hero-map"
PRIMARY_WG = "wg-16"

CORE_ORDER = ["theme.css", "components.css", "visual-components.css", "layouts.css", "print.css"]
INLINE_ORDER = [
    ("theme.css", "{{THEME_CSS}}"),
    ("components.css", "{{COMPONENTS_CSS}}"),
    ("visual-components.css", "{{VISUAL_COMPONENTS_CSS}}"),
    ("widgets.css", "{{WIDGETS_CSS}}"),
    ("visual-html.css", "{{VISUAL_HTML_CSS}}"),
    ("body-icons.css", "{{BODY_ICONS_CSS}}"),
    ("editorial-patterns.css", "{{EDITORIAL_PATTERNS_CSS}}"),
    ("shape-visuals.css", "{{SHAPE_VISUALS_CSS}}"),
    ("workflow-visuals.css", "{{WORKFLOW_VISUALS_CSS}}"),
    ("layouts.css", "{{LAYOUTS_CSS}}"),
    ("print.css", "{{PRINT_CSS}}"),
    ("theme-dark.css", "{{THEME_DARK_CSS}}"),
]

BODY_ICON_DATA = {item["id"]: item["svg"] for item in json.loads((ASSETS / "body-icons.json").read_text(encoding="utf-8"))}
ICON = {
    "hero": "landing",
    "value": "impact",
    "flow": "flow",
    "faq": "question",
    "cta": "check",
    "source": "source",
    "risk": "warning",
    "metric": "metric",
}

SOURCE_LIST = [
    {"name": "프로젝트 project.json", "url": "sources/project.json", "role": "공고/RFP/기간/예산/TRL/최종 산출물 메타"},
    {"name": "아이디어 브리프", "url": "sources/idea-brief.md", "role": "RFP 11 한 줄 정의, 고정 요구, 보유 자산, 사업화"},
    {"name": "business-core.yaml", "url": "sources/business-core.yaml", "role": "문제·해결·기술·시장·경쟁·재무·영향 단일 코어"},
    {"name": "종합 리서치 보고서", "url": "sources/research-report.md", "role": "시장·정책·경쟁·기술·특허·논문 조사 요약"},
    {"name": "Executive Summary", "url": "sources/executive-summary.md", "role": "최종 사업계획 요약과 핵심 정량 목표"},
    {"name": "AI and Sustainable Development Goals", "url": "https://arxiv.org/abs/1905.00501", "role": "AI가 SDGs를 지원할 수 있지만 투명성·안전·윤리 규제가 필요하다는 일반 근거"},
    {"name": "Real-world Anomaly Detection in Surveillance Videos", "url": "https://arxiv.org/abs/1801.04264", "role": "감시 영상 이상탐지 데이터셋/약지도 학습의 대표 연구 근거"},
    {"name": "Stanford STORM Research Project", "url": "https://storm-project.stanford.edu/research/storm/", "role": "다관점 질문+출처 grounding 리서치 방식"},
    {"name": "STORM paper · arXiv:2402.14207", "url": "https://arxiv.org/abs/2402.14207", "role": "STORM 방법론 출처"},
]

STORM_SCAN = {
    "Skeptic": {
        "persona": "회의주의자",
        "summary": "가장 큰 약점은 [가상] 회사·실증처·성능 수치가 실제 제출 전 교체되어야 한다는 점이다.",
        "body": "패키지 project.json과 executive summary는 final-virtual-expanded 상태이며, [가상] 태그의 회사·실증처·실적·PoC 수치를 실제값으로 바꾸지 않으면 제출 리스크가 크다고 명시한다. 또한 research-report는 경쟁사가 이미 낙상·교정·돌봄 도메인에서 선점했음을 보여준다. 따라서 랜딩 브리프는 과장된 '국내 유일'이 아니라 증거 교체와 차별화 보정에 초점을 둔다.",
    },
    "Economist": {
        "persona": "경제학자",
        "summary": "정부 16억 R&D보다 중요한 것은 실증 후 구축형+SaaS의 반복 매출 논리다.",
        "body": "business-core는 16억/2년, TRL5→7, 구축형 시설 납품+관제 SaaS 구독을 핵심 수익모델로 둔다. SOM은 120시설×ARPA 960만으로 11.5억을 잡지만, 가격·점유율·조달 단가는 [확인 필요]이다. 따라서 예산표보다 unit economics와 조달 진입장벽을 더 엄격히 보여야 한다.",
    },
    "Historian": {
        "persona": "역사학자",
        "summary": "지능형 CCTV는 새롭지 않다. 보호시설 특화도 일부 선점되었다.",
        "body": "research-report는 국내 클레버러스, 해외 SafelyYou, care.ai, iOmniscient 등 도메인 강자가 이미 레퍼런스를 보유한다고 정리한다. 차별성은 'AI CCTV' 자체가 아니라 시설5종×위험8종 공통 플랫폼, 국내 privacy-by-design, 자해/자살 미커버 항목, 실증/A/S 체계다.",
    },
    "Academic": {
        "persona": "학자",
        "summary": "기술 목표는 macro-F1 85%보다 항목별 데이터 공백을 정직하게 분리해야 설득력이 생긴다.",
        "body": "business-core와 research-report는 약지도 VAD, skeleton 행동인식, VLM 보조를 기술 축으로 제시한다. 동시에 자해/자살 표준벤치 부재, 실환경 격차, 저조도·가림·밀집·프라이버시 trade-off를 주요 리스크로 둔다. 평가자는 평균 점수보다 항목별 목표와 검증 설계를 본다.",
    },
    "Futurist": {
        "persona": "미래학자",
        "summary": "이 사업의 미래 가치는 '감시 강화'가 아니라 보호시설 안전 운영 OS로 포지셔닝할 때 커진다.",
        "body": "AI for social good은 안전·효율을 만들 수 있지만, 투명성·책임·규제가 같이 설계되지 않으면 역효과가 날 수 있다. 이 사업은 엣지 비식별, 적용제외 zone, IRB·인권 검토, 시설별 위험정의 워크플로우를 제품 핵심으로 넣을 때 사회기술 실증사업의 명분이 선다.",
    },
}

CONTRADICTIONS = [
    ["보호시설 AI 안전은 사고 골든타임을 줄인다", "CCTV/AI 감시는 인권·프라이버시 우려를 키운다", "privacy-by-design을 기능이 아니라 평가·차별화의 중심으로 둔다"],
    ["RFP는 위험 8종 통합 탐지를 요구한다", "자해/자살징후는 표준벤치와 데이터가 부족하다", "항목별 목표와 통합 지표를 분리하고 탐색/정성 목표를 명시한다"],
    ["글로벌 영상분석 시장은 성장한다", "국내 영상보안서비스는 둔화/역성장 신호가 있다", "TAM 과장 대신 공공·시설 세그먼트 bottom-up SOM을 쓴다"],
    ["국내외 경쟁은 이미 존재한다", "RFP는 폐쇄형 보호시설 공통 적용을 요구한다", "단일 도메인 기능 경쟁이 아니라 시설5종×위험8종×국내 규제대응으로 포지셔닝한다"],
    ["사업계획서 산출물이 최종형으로 준비되었다", "핵심 회사·실증처·성능 정보는 [가상]이다", "제출 전 실제값 교체 gate를 CTA로 명시한다"],
]

SYNTHESIS = """# STORM Synthesis · 사회기술 실증 사업 랜딩 브리프

이 패키지의 핵심은 '폐쇄형 보호시설 영상AI'가 아니라 '보호시설 안전 운영 OS'다. RFP 11은 위험상황 8종, 3초 내 경보, CCTV 50대 이상, 실증 2곳, 만족도 80점이라는 고정 목표를 요구한다. 기존 경쟁은 낙상·요양·교정 등 단일 도메인에서 강하지만, 시설5종×위험8종×국내 규제대응을 하나의 공통 플랫폼으로 묶는 포지션이 남는다.

랜딩형 HTML은 심사위원이 3분 안에 보는 구조로 만들어야 한다. 첫 화면은 문제·해결·차별화, 다음은 수치 목표·시장·리스크, 그 다음은 실행 로드맵과 제출 전 gate다. 특히 [가상] 태그의 회사·실증처·PoC 수치를 실제값으로 바꾸는 것을 마지막 CTA로 잠근다.
"""

PEER_REVIEW = """# STORM Peer Review

BLOCKER는 두 가지다. 첫째, [가상] 정보를 실제 제출용 근거처럼 보이게 하면 안 된다. 둘째, 인권·개인정보 리스크를 단순 규제 항목으로 밀어내면 사회문제해결 실증사업의 명분이 약해진다.

수정 지시:
- '국내 유일'류 표현 금지. 경쟁 선점 인정 후 통합 범위와 privacy-by-design으로 차별화.
- macro-F1 85%는 항목별 실증DB, 저조도·가림·밀집, 자해/자살 데이터 공백과 함께 설명.
- SOM/매출은 [가정]/[목표]로 보수 표기.
- 제출 전 실제값 교체 gate를 사용자 행동으로 명확히 둔다.
"""


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text_sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def version() -> str:
    return json.loads(read(SKILL / "manifest.json"))["version"]


def esc(text: str) -> str:
    return html.escape(str(text), quote=True)


def body_icon(token: str) -> str:
    return f'<span class="body-icon body-icon--sm" aria-hidden="true">{BODY_ICON_DATA[ICON[token]]}</span>'


def h2(num: str, title: str, icon: str, sub: str) -> str:
    return f'<h2>{body_icon(icon)}<span class="num">{esc(num)}</span>{esc(title)}</h2><p class="h2-sub">{esc(sub)}</p>'


def table(rows: list[list[str]], caption: str, headers: list[str]) -> str:
    head = "".join(f'<th scope="col">{esc(h)}</th>' for h in headers)
    body = "".join("<tr>" + "".join((f'<th scope="row">{esc(c)}</th>' if i == 0 else f'<td>{c}</td>') for i, c in enumerate(row)) + "</tr>" for row in rows)
    return f'<div class="table-scroll"><table><caption>{esc(caption)}</caption><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def markdownish_to_html(text: str) -> str:
    out = []
    in_ul = False
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            if in_ul:
                out.append('</ul>'); in_ul = False
            continue
        if line.startswith('- ') or re.match(r'^\d+\.\s', line):
            if not in_ul:
                out.append('<ul>'); in_ul = True
            item = re.sub(r'^\d+\.\s+', '', line[2:] if line.startswith('- ') else line)
            out.append(f'<li>{esc(item)}</li>')
            continue
        if in_ul:
            out.append('</ul>'); in_ul = False
        if line.startswith('# '): out.append(f'<h3>{esc(line[2:])}</h3>')
        elif line.startswith('## '): out.append(f'<h3>{esc(line[3:])}</h3>')
        else: out.append(f'<p>{esc(line)}</p>')
    if in_ul: out.append('</ul>')
    return '\n'.join(out)


def source_details(title: str, text: str, open_: bool=False) -> str:
    open_attr = ' open' if open_ else ''
    return f'<details class="source-preserve" style="margin:34px 0 0 24px;border-left:6px solid var(--accent);padding-left:20px"{open_attr}><summary style="padding:20px 24px 20px 34px;display:flex;align-items:center;gap:12px;flex-wrap:wrap"><strong>{esc(title)}</strong><span class="tag">원문 보존</span></summary><div class="source-body" style="padding:0 28px 30px 34px"><div style="border-left:1px solid var(--line);padding:24px 0 2px 24px">{markdownish_to_html(text)}</div></div></details>'


def make_storm_markdown():
    scan = ['# Multi-Perspective Scan · 사회기술 실증 사업 브리프']
    for name, row in STORM_SCAN.items():
        scan.extend([f'## {name} · {row["persona"]}', row['summary'], row['body'], ''])
    contradiction = '# Contradiction Map\n' + '\n'.join(f'- {a} ↔ {b} → {c}' for a,b,c in CONTRADICTIONS)
    return '\n'.join(scan), contradiction, SYNTHESIS, PEER_REVIEW


def build_hero(scan_md: str) -> str:
    vt = """
<section class="vt-shell" aria-label="사업 핵심 지도">
  <div class="vt-frame"><div class="vt-demo"><div class="hm-grid">
    <article class="hm-card"><div class="vt-kicker">Problem</div><h3>보호시설 사고 골든타임</h3><p class="vt-text">낙상·자해·폭행·이탈을 인력 관제로만 감당하기 어렵다.</p></article>
    <article class="hm-card" style="--c:var(--vt-blue)"><div class="vt-kicker">Solution</div><h3>영상AI 8종 탐지·3초 경보</h3><p class="vt-text">엣지 skeleton, 약지도 이상탐지, VLM 보조를 통합한다.</p></article>
    <article class="hm-card" style="--c:var(--vt-green)"><div class="vt-kicker">Moat</div><h3>privacy-by-design 공통 플랫폼</h3><p class="vt-text">시설5종×위험8종×국내 규제대응으로 차별화한다.</p></article>
  </div><div class="hm-result"><b>RFP 11 맞춤 판정</b><span>기술개발보다 실증·규제·실제값 교체 gate가 승부처다.</span></div></div></div>
</section>
"""
    cards = ''.join(f'<article class="summary-card"><div class="label">{esc(k)} · {esc(v["persona"])}</div><h3>{esc(v["summary"])}</h3><p>{esc(v["body"])}</p></article>' for k,v in STORM_SCAN.items())
    toc = """
<nav class="toc-map" id="document-toc" aria-label="문서 목차"><span class="label">문서 목차</span><p>사업 한눈 요약, 가치 제안, 작동 방식, FAQ, 제출 전 게이트로 이동합니다.</p><div class="toc-pills"><a class="toc-pill" href="#hero"><b>1</b>Hero</a><a class="toc-pill" href="#value"><b>2</b>Value</a><a class="toc-pill" href="#workflow"><b>3</b>Workflow</a><a class="toc-pill" href="#faq"><b>4</b>FAQ</a><a class="toc-pill" href="#cta"><b>5</b>Gate</a><a class="toc-pill" href="#source-note"><b>6</b>Sources</a></div></nav>
"""
    return f"""
<div id="hero"></div>
{toc}
{h2('01', 'Hero · 폐쇄형 보호시설 공통 영상AI 안전 플랫폼', 'hero', 'bizplan-social-tech-demo-2026 패키지의 RFP 11 사업계획 내용을 현재 랜딩 브리프 구조로 재구성했다.')}
<p>한 줄로 말하면, 이 사업은 폐쇄형 보호시설의 인력 중심 CCTV 관제를 <span class="hl">위험상황 8종 자동탐지와 3초 내 신속경보</span>로 바꾸는 사회문제해결 R&D 실증이다. 단순 AI CCTV가 아니라, 치매·요양·교정·정신·아동보호시설에 공통 적용되는 안전 운영 플랫폼으로 포지셔닝한다.</p>
{vt}
<h3>STORM 다섯 관점이 남긴 판단</h3>
<div class="card-grid rail-cycle">{cards}</div>
{source_details('STORM Multi-Perspective Scan 원문', scan_md)}
"""


def build_value_props() -> str:
    rows = [
        ['RFP/예산', '과기정통부 공고 제2026-668호 / RFP 11 / 단일형', '정부 16억, 2년, TRL5→7'],
        ['문제', '낙상·자해·폭행·이탈 등 생명안전 사고와 인력 관제 한계', '사회문제 해결성'],
        ['해결', '영상AI 위험 8종 탐지, 위험수준별 3초 내 경보', '측정 가능한 성과지표'],
        ['차별화', '시설5종×위험8종 공통 플랫폼 + privacy-by-design', '경쟁 선점 인정 후 재포지셔닝'],
        ['사업화', '구축형 시설 납품 + 관제 SaaS + 공공조달', '실증 레퍼런스→확산'],
        ['제출 리스크', '[가상] 회사·실증처·성능 수치 실제값 교체 필요', '마지막 게이트로 잠금'],
    ]
    return f"""
<div id="value"></div>
{h2('02', 'Value Props · 심사위원이 3분 안에 봐야 할 여섯 문장', 'value', '사업계획서 긴 본문을 문제·해결·차별화·사업화·제출 리스크로 압축했다.')}
{table(rows, '랜딩 브리프 핵심 가치 제안', ['축', '핵심 메시지', '심사 포인트'])}
<div class="impact-grid"><article class="impact-card"><h3>사회성</h3><p>보호시설 생명안전 사고의 골든타임을 줄이고 돌봄·관제 인력 부담을 낮춘다.</p></article><article class="impact-card"><h3>기술성</h3><p>skeleton 행동인식, 약지도 VAD, VLM 보조를 엣지 비식별 구조와 결합한다.</p></article><article class="impact-card"><h3>사업성</h3><p>실증처 레퍼런스를 구축형 납품과 SaaS 관제 구독으로 확장한다.</p></article><article class="impact-card"><h3>정직성</h3><p>경쟁 선점과 데이터 공백을 숨기지 않고 평가 대응 논리로 바꾼다.</p></article></div>
<div class="source-note"><h3>사업 코어 상세 해석</h3><p><strong>고객:</strong> 1차 고객은 치매전담·요양시설이고 확장 고객은 교정·정신응급·아동보호시설이다. 사용자와 구매자는 다르다. 현장 사용자는 관제요원·간호·요양보호사·교도관이며, 구매자는 시설 운영법인·공공 발주처·지자체가 된다. 이 차이를 구분해야 제품 기능 설명이 구매 논리로 바뀐다.</p><p><strong>기술:</strong> 제안 코어는 CCTV 영상 입력, 엣지 skeleton 추출, 약지도 영상이상탐지, 위험수준별 신속 경보, 관제·현장요원·관할기관 연계 흐름이다. 핵심 난제는 평균 F1이 아니라 자해/자살징후 같은 희소 이벤트, 저조도·가림·밀집, 프라이버시와 정확도 사이의 trade-off다.</p><p><strong>시장:</strong> TAM은 시설 수와 CCTV 채널에서 충분해 보이지만, 국내 영상보안서비스 둔화 신호가 있어 단순 성장시장 주장만으로는 약하다. 그래서 공공·시설 세그먼트, KISA 인증, 실증 레퍼런스, 조달 가능성을 엮은 bottom-up SOM이 필요하다.</p><p><strong>경쟁:</strong> 클레버러스, SafelyYou, care.ai, iOmniscient 같은 직접·해외 경쟁은 이미 도메인별 강점을 갖고 있다. 이 브리프는 경쟁을 축소하지 않고, 단일 도메인 강자와 달리 시설5종×위험8종×국내 규제대응을 통합하는 공통 플랫폼으로 재정렬한다.</p><p><strong>규제:</strong> 보호시설 CCTV는 안전성과 인권성이 동시에 걸린다. privacy-by-design은 부록 문구가 아니라 엣지 처리, 골격 비식별, 적용제외 zone, 접근권한, 로그, IRB/동의 구조까지 들어가는 핵심 설계 요구다.</p></div>
"""


def build_how_it_works(contradiction_md: str) -> str:
    wg = """
<section class="wg-16" aria-labelledby="wg-16-title"><header class="wg-16-head"><p class="wg-16-kicker">Implementation Plan · RFP 11</p><h2 id="wg-16-title" class="wg-16-h">TRL5에서 TRL7로 가는 24개월 실증 로드맵</h2><p class="wg-16-lead">위험 8종 정의, 실증DB 구축, 신속경보 시스템, 현장 실증, 시험인증을 하나의 단계로 묶습니다.</p></header><div class="wg-16-panel"><h3 class="wg-16-h3">마일스톤 타임라인</h3><ol class="wg-16-ms"><li class="wg-16-ms-item wg-16-active"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">M1 · 위험 8종 정의·PoC 보정</span><span class="wg-16-badge wg-16-bd-active">0~6개월</span></div><p class="wg-16-ms-desc">낙상·실신·자해·자살징후·폭행·금지구역 접근·통제구역 이탈 기준을 확정합니다.</p></div></li><li class="wg-16-ms-item"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">M2 · 실증DB·경보 시스템</span><span class="wg-16-badge">7~15개월</span></div><p class="wg-16-ms-desc">실증DB와 3초 경보 파이프라인을 만들고 통합 F1 80%를 검증합니다.</p></div></li><li class="wg-16-ms-item"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">M3 · 현장 실증·시험인증</span><span class="wg-16-badge">16~24개월</span></div><p class="wg-16-ms-desc">2개 이상 시설, CCTV 50대 이상, 만족도 80점, 최종 F1 85% 목표를 확인합니다.</p></div></li></ol><h3 class="wg-16-h3">데이터 플로우</h3><div class="wg-16-flow" aria-label="영상AI 실증 데이터 플로우"><div class="wg-16-fnode">CCTV<span class="wg-16-fnode-s">현장 영상</span></div><div class="wg-16-fnode">엣지 비식별<span class="wg-16-fnode-s">skeleton</span></div><div class="wg-16-fnode wg-16-fnode-good">위험 탐지<span class="wg-16-fnode-s">8종 분류</span></div><div class="wg-16-fnode wg-16-fnode-hot">3초 경보<span class="wg-16-fnode-s">현장 대응</span></div></div></div></section>
"""
    return f"""
<div id="workflow"></div>
{h2('03', 'How It Works · 기술개발보다 실증 흐름이 먼저 보인다', 'flow', 'landing_brief_html 권장 wg-16 구현 계획 위젯으로 연구개발·실증·시험인증 경로를 구조화했다.')}
{wg}
<h3>Contradiction Map · 사업계획서에 반드시 남길 긴장</h3>
{table(CONTRADICTIONS, 'STORM Contradiction Map', ['주장 A', '충돌 근거', '실행 해석'])}
{source_details('Contradiction Map 원문', contradiction_md, open_=True)}
"""


def build_faq(synthesis_md: str, peer_md: str) -> str:
    return f"""
<div id="faq"></div>
{h2('04', 'FAQ · 평가자가 바로 물을 질문', 'faq', '사업계획서의 약점을 숨기지 않고 방어 가능한 문장으로 바꿨다.')}
<div class="card-grid rail-cycle"><article class="summary-card"><h3>Q1. 경쟁사가 이미 있는데 왜 이 팀인가?</h3><p>낙상·요양·교정 단일 도메인 강자는 인정한다. 차별화는 시설5종×위험8종 공통 플랫폼, 국내 privacy-by-design, 실증·A/S·조달 적용성에 둔다.</p></article><article class="summary-card"><h3>Q2. F1 85%가 현실적인가?</h3><p>전체 평균만 제시하지 않는다. 낙상·폭행은 상대적으로 성숙, 자해·자살징후는 데이터 공백이 크므로 항목별 목표·실증DB·정성/탐색 목표를 분리한다.</p></article><article class="summary-card"><h3>Q3. 개인정보·인권 리스크는?</h3><p>엣지 처리, 골격 비식별, 적용제외 zone, 접근 로그, IRB/현장동의 체계를 기술·운영 핵심으로 둔다. 규제 대응은 부록이 아니라 제품 가치다.</p></article><article class="summary-card"><h3>Q4. 제출 전 가장 큰 gate는?</h3><p>[가상] 회사명·재무·실증처·MOU·특허·PoC 성능·납품 실적을 실제 증빙으로 교체해야 한다. 교체 전 제출은 허위기재 리스크다.</p></article></div>
{source_details('STORM Synthesis 원문', synthesis_md)}
{source_details('STORM Peer Review 원문', peer_md, open_=False)}
"""


def build_cta() -> str:
    rows = [
        ['실제값 교체', '[가상] 회사·실증처·성능·특허·납품 실적', 'IRIS 제출 전 필수'],
        ['법무부/수요처', '수요기관 접점·실증 의향서·MOU', '평가 리스크 완화'],
        ['성능 근거', '위험유형별 PoC 측정조건, 실증DB 설계', '기술성 방어'],
        ['규제 설계', '개인정보·인권·IRB·비식별 처리', '사회성/정책성 방어'],
        ['NTIS/FTO', '중복과제·특허 claim chart', '탈락/분쟁 예방'],
    ]
    return f"""
<div id="cta"></div>
{h2('05', 'CTA · 제출 전 5대 잠금 게이트', 'cta', '완성처럼 보이는 초안을 실제 제출 가능한 계획서로 바꾸는 마지막 체크리스트다.')}
{table(rows, '제출 전 잠금 게이트', ['Gate', '교체·확인 대상', '효과'])}
<div class="try soft-cta"><h2>최종 한 줄</h2><p>이 사업은 “AI가 CCTV를 더 잘 본다”가 아니라, <strong>보호시설 안전사고의 골든타임을 줄이면서 인권·개인정보 리스크를 기술 설계로 낮추는 사회기술 실증</strong>으로 제출해야 한다.</p></div>
"""


def build_source_note() -> str:
    links = ''.join(f'<li><a href="{esc(s["url"])}" target="_blank" rel="noopener noreferrer">{esc(s["name"])}</a> — {esc(s["role"])}</li>' for s in SOURCE_LIST)
    return f"""
<div id="source-note"></div>
{h2('06', 'Source Hub · 스킬 패키지와 리서치 근거', 'source', 'bizplan-social-tech-demo-2026 원본과 STORM 산출물을 분리 보관했다.')}
<p>보조 파일: <a href="sources/storm-scan.md">storm-scan.md</a> · <a href="sources/storm-contradiction-map.md">contradiction-map.md</a> · <a href="sources/storm-synthesis.md">synthesis.md</a> · <a href="sources/storm-peer-review.md">peer-review.md</a> · <a href="sources/bizplan-application.json">bizplan 적용 기록</a></p><ol class="refs">{links}</ol>
"""


def copy_sources(scan_md, contradiction_md, synthesis_md, peer_md):
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir(parents=True); (OUT/'pages').mkdir(); SOURCES.mkdir(); (SOURCES/'assets').mkdir(); (SOURCES/'screenshots').mkdir()
    for src, name in [
        (BIZ/'project.json', 'project.json'),
        (BIZ/'02-interview/idea-brief.md', 'idea-brief.md'),
        (BIZ/'05-business-core/business-core.yaml', 'business-core.yaml'),
        (BIZ/'04-research/research-report.md', 'research-report.md'),
        (BIZ/'08-draft/executive-summary.md', 'executive-summary.md'),
    ]:
        shutil.copyfile(src, SOURCES/name)
    (SOURCES/'source-list.json').write_text(json.dumps(SOURCE_LIST, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    (SOURCES/'storm-scan.md').write_text(scan_md+'\n', encoding='utf-8')
    (SOURCES/'storm-contradiction-map.md').write_text(contradiction_md+'\n', encoding='utf-8')
    (SOURCES/'storm-synthesis.md').write_text(synthesis_md+'\n', encoding='utf-8')
    (SOURCES/'storm-peer-review.md').write_text(peer_md+'\n', encoding='utf-8')
    (SOURCES/'storm-report.json').write_text(json.dumps({'topic':'폐쇄형 보호시설 영상AI 위험상황 신속대응 R&D 실증사업 브리프','mode':'solo-fallback-by-main-agent','souls':STORM_SCAN,'contradictions':CONTRADICTIONS,'synthesis':synthesis_md,'peer_review':peer_md}, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    (SOURCES/'bizplan-application.json').write_text(json.dumps({'skill_package':'bizplan-social-tech-demo-2026','skill_md_found':False,'source_path':str(BIZ.relative_to(ROOT)),'selected_mode':MODE,'topic':'RFP 11 폐쇄형 보호시설 영상AI 위험상황 신속대응','applied_rules':['local project corpus used as skill content','STORM five-perspective scan','landing brief structure','explicit virtual-value replacement gate','current adaptive-html-final v'+version()]}, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    shutil.copyfile(SKILL/'manifest.json', SOURCES/'adaptive-html-final-manifest.json')
    (SOURCES/'profile.json').write_text(json.dumps({'profile':PROFILE}, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    (SOURCES/'layout-placeholder-map.json').write_text(json.dumps({'layout':LAYOUT,'HERO':'vt hero-map + STORM scan','VALUE_PROPS':'RFP value table','HOW_IT_WORKS':'wg-16 roadmap + contradiction map','FAQ':'evaluation questions','CTA':'submission gates','SOURCE_NOTE':'source hub'}, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    asset_hashes = {}
    for name,_ in INLINE_ORDER:
        src=ASSETS/name
        if src.exists(): shutil.copyfile(src, SOURCES/'assets'/name); asset_hashes[name]=sha(src)
    core_blob='\n'.join(read(ASSETS/name) for name in CORE_ORDER)
    integrity={'generated_at':datetime.now(timezone.utc).isoformat(),'skill':'adaptive-html-final','version':version(),'profile':PROFILE,'mode':MODE,'layout':LAYOUT,'core_css_sha256':text_sha(core_blob),'asset_order':CORE_ORDER,'asset_sha256':asset_hashes,'inline_order':[n for n,_ in INLINE_ORDER]}
    (SOURCES/'css-integrity.json').write_text(json.dumps(integrity, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    evidence_files = ['AGENTS.md','skills/adaptive-html-final/SKILL.md','skills/adaptive-html-final/manifest.json','skills/adaptive-html-final/assets/base.html','skills/adaptive-html-final/assets/layouts/landing-brief.html','skills/adaptive-html-final/assets/visual-html-templates/01-hero-map.html','skills/adaptive-html-final/assets/widget-templates/16-implementation-plan.html','orginal_skill/bizplan-social-tech-demo-2026/project.json','orginal_skill/bizplan-social-tech-demo-2026/02-interview/idea-brief.md','orginal_skill/bizplan-social-tech-demo-2026/05-business-core/business-core.yaml','orginal_skill/bizplan-social-tech-demo-2026/04-research/research-report.md','orginal_skill/bizplan-social-tech-demo-2026/08-draft/executive-summary.md','orginal_skill/storm-research/SKILL.md','orginal_skill/storm-research/references/storm-pipeline.md','orginal_skill/storm-research/references/provenance.md']
    evidence={'mode':MODE,'profile':PROFILE,'layout':LAYOUT,'layout_class':LAYOUT_CLASS,'primary_vt':PRIMARY_VT,'primary_wg':PRIMARY_WG,'section_mapping':json.loads((SOURCES/'layout-placeholder-map.json').read_text()),'files':[{'path':p,'sha256':sha(ROOT/p)} for p in evidence_files if (ROOT/p).exists()],'input_snapshots':['sources/storm-scan.md','sources/storm-contradiction-map.md','sources/storm-synthesis.md','sources/storm-peer-review.md','sources/bizplan-application.json'],'research_route':'storm-research solo fallback; local bizplan corpus plus public research links'}
    (SOURCES/'build-evidence.json').write_text(json.dumps(evidence, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    return integrity


def css_slots(integrity):
    slots={}
    for name,slot in INLINE_ORDER:
        css=read(ASSETS/name) if (ASSETS/name).exists() else ''
        if name=='theme.css': css=f"/* adaptive-html-final-core-css-sha256: {integrity['core_css_sha256']} */\n"+css
        if name in ('shape-visuals.css','workflow-visuals.css'): css=''
        slots[slot]=css.rstrip()
    return slots


def render(scan_md, contradiction_md, synthesis_md, peer_md, integrity):
    layout=read(ASSETS/'layouts'/LAYOUT)
    meta=f'<span>{MODE}</span><span>{LAYOUT}</span><span>profile {PROFILE}</span><span>adaptive-html-final v{version()}</span><span>bizplan-social-tech-demo-2026</span>'
    repl={'{{KICKER}}':'<span class="kicker-text">bizplan-social-tech-demo-2026 × STORM Research</span>','{{TITLE}}':'폐쇄형 보호시설 영상AI 실증사업 브리프','{{SUBTITLE}}':'RFP 11 사업계획 패키지를 현재 프로젝트 최신 랜딩 스타일로 재구성한 사회기술 데모 HTML','{{META}}':meta,'{{HERO}}':build_hero(scan_md),'{{VALUE_PROPS}}':build_value_props(),'{{HOW_IT_WORKS}}':build_how_it_works(contradiction_md),'{{FAQ}}':build_faq(synthesis_md, peer_md),'{{CTA}}':build_cta(),'{{SOURCE_NOTE}}':build_source_note()}
    body=layout
    for k,v in repl.items(): body=body.replace(k,v)
    body=body.replace('</div></header>','</div><div class="generated-row"><p class="generated-date">생성 기준: 2026-06-20 KST · STORM solo research · landing_brief_html · layout-first</p><div class="lens-strip" aria-label="적용 렌즈"><span class="lens-strip-label">LENS</span><span class="lens-chip">사회기술</span><span class="lens-chip">RFP 11</span><span class="lens-chip">실증확산</span><span class="lens-chip">privacy-by-design</span><span class="lens-chip">제출 게이트</span></div></div></header>',1)
    title='폐쇄형 보호시설 영상AI 실증사업 브리프 · bizplan STORM'
    description=f'bizplan-social-tech-demo-2026 패키지와 STORM 리서치로 만든 RFP 11 사회기술 실증사업 HTML 랜딩 브리프. adaptive-html-final v{version()} 스타일.'
    json_ld=json.dumps({'@context':'https://schema.org','@type':'Article','headline':title,'description':description,'inLanguage':'ko','datePublished':'2026-06-20','author':{'@type':'Organization','name':'adaptive-html-final'},'keywords':['사회문제해결 R&D','영상AI','폐쇄형 보호시설','지능형 CCTV','privacy-by-design','사업계획서']}, ensure_ascii=False)
    doc=read(ASSETS/'base.html')
    slots={'{{TITLE}}':title,'{{DESCRIPTION}}':description,'{{JSON_LD_BLOCK}}':f'<script type="application/ld+json">{json_ld}</script>','{{BODY}}':body,'{{FOOTER}}':''}
    slots.update(css_slots(integrity))
    for k,v in slots.items(): doc=doc.replace(k,v)
    leftovers=sorted(set(re.findall(r'{{[^}]+}}', doc)))
    if leftovers: raise RuntimeError(f'unresolved placeholders: {leftovers}')
    return re.sub(r'\n{4,}','\n\n\n',doc)


def content_evidence(doc):
    visible=re.sub(r'<style\b[^>]*>[\s\S]*?</style>','',doc,flags=re.I)
    visible=re.sub(r'<script\b[^>]*>[\s\S]*?</script>','',visible,flags=re.I)
    visible=re.sub(r'<[^>]+>',' ',visible); visible=re.sub(r'\s+',' ',html.unescape(visible))
    req=['폐쇄형 보호시설 영상AI','bizplan-social-tech-demo-2026','STORM','RFP 11','privacy-by-design','시설5종','위험8종','[가상]','Contradiction Map','Source Hub']
    missing=[x for x in req if x not in visible]
    evidence={'storm_soul_count':len(STORM_SCAN),'source_count':len(SOURCE_LIST),'required_markers_missing':missing,'output_visible_text_chars':len(visible),'pass':not missing and len(visible)>8000}
    (SOURCES/'content-preservation.json').write_text(json.dumps(evidence, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    if not evidence['pass']: raise RuntimeError(str(evidence))


def main():
    scan, contradiction, synthesis, peer = make_storm_markdown()
    integrity=copy_sources(scan, contradiction, synthesis, peer)
    doc=render(scan, contradiction, synthesis, peer, integrity)
    (OUT/'index.html').write_text(doc, encoding='utf-8')
    content_evidence(doc)
    print(OUT.relative_to(ROOT))

if __name__ == '__main__': main()
