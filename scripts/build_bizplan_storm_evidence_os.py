#!/usr/bin/env python3
"""Build a current adaptive-html-final HTML page from the local bizplan skill + STORM research.

Topic selected by the STORM solo fallback:
  BizPlan Evidence OS — 증거 원장 기반 사업계획서 작성·검증 SaaS

Important: this script does not invent market/customer/revenue numbers. It keeps the
bizplan skill's evidence tags visible and marks unresolved items as [확인 필요].
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
BIZ = ROOT / "orginal_skill" / "bizplan"
STORM = ROOT / "orginal_skill" / "storm-research"

OUT = ROOT / "output" / "2026-06-20" / "bizplan-storm-evidence-os"
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

PUBLIC_SOURCES = [
    {
        "name": "Stanford STORM Research Project",
        "url": "https://storm-project.stanford.edu/research/storm/",
        "role": "다관점 질문·출처 grounding 기반 pre-writing 방법론",
    },
    {
        "name": "STORM paper · arXiv:2402.14207",
        "url": "https://arxiv.org/abs/2402.14207",
        "role": "STORM의 outline organization·coverage 개선과 source bias/over-association 한계",
    },
]

LOCAL_SOURCES = [
    {
        "name": "bizplan/SKILL.md",
        "url": "sources/bizplan-SKILL.md",
        "role": "7대 절대 규칙, 21단계 워크플로우, business-core.yaml 단일 출처 원칙",
    },
    {
        "name": "evidence-tagging.md",
        "url": "sources/evidence-tagging.md",
        "role": "[사실] [추정] [가정] [목표] [확인 필요] 증거 태깅 문법",
    },
    {
        "name": "research-engine.md",
        "url": "sources/research-engine.md",
        "role": "조사와 작성 분리, 부정적 근거 수집, source-index.xlsx 구축",
    },
    {
        "name": "business-core.md",
        "url": "sources/business-core.md",
        "role": "사업 코어·evidence-ledger·숫자 일관성 게이트",
    },
    {
        "name": "document-types.md",
        "url": "sources/document-types.md",
        "role": "정부지원·R&D·투자덱·제안서별 평가 논리 변환",
    },
    {
        "name": "verification.md",
        "url": "sources/verification.md",
        "role": "평가위원 4역할 시뮬레이션과 점수/결함 반복 루프",
    },
    {
        "name": "document-output.md",
        "url": "sources/document-output.md",
        "role": "HTML 렌더링·깨짐 검사·최종 제출 체크리스트",
    },
]

SOURCE_LIST = LOCAL_SOURCES + PUBLIC_SOURCES

STORM_SCAN = {
    "Skeptic": {
        "persona": "회의주의자",
        "summary": "사업계획서 AI 도구의 가장 큰 리스크는 글을 빠르게 만드는 순간 존재하지 않는 고객·매출·특허·성능을 그럴듯하게 꾸밀 수 있다는 점이다.",
        "body": "bizplan 스킬은 이 위험을 7대 절대 규칙으로 차단한다. 고객·매출·계약·인증·기술 성능·시장 수치를 만들지 않고, 없으면 [확인 필요]로 둔다. 따라서 제품 콘셉트는 '문장 생성기'가 아니라 '거짓을 못 쓰게 막는 증거 원장'이어야 한다.",
    },
    "Economist": {
        "persona": "경제학자",
        "summary": "구매 가치는 문장 품질보다 재작업 감소, 제출 리스크 감소, 여러 서식으로 재활용되는 단일 코어에서 나온다.",
        "body": "가격·시장 규모·고객 수는 아직 [확인 필요]이다. 대신 단일 business-core.yaml에서 정부지원서·R&D 계획서·IR 덱·공공 제안서를 파생시키는 구조는 반복 작업 비용을 줄일 수 있다는 가설을 만든다. 실제 TAM/SAM/SOM은 bottom-up 인터뷰와 유료/공식 자료로 검증해야 한다.",
    },
    "Historian": {
        "persona": "역사학자",
        "summary": "사업계획서 템플릿과 AI 글쓰기 도구는 이미 많다. 차별점은 빈칸 채우기가 아니라 게이트형 사업 논리 설계다.",
        "body": "기존 도구는 보통 문장·목차·톤을 빠르게 만든다. bizplan 스킬은 공고 분석→인터뷰→리서치→코어→서식 매핑→초안→평가위원 검증의 순서를 고정한다. 과거 템플릿 시대와 다른 점은 document generator가 아니라 traceable decision system이라는 점이다.",
    },
    "Academic": {
        "persona": "학자",
        "summary": "STORM의 pre-writing 방식과 bizplan의 조사/작성 분리는 같은 방향을 가리킨다. 먼저 근거를 모으고, 그 다음 글을 쓴다.",
        "body": "STORM은 다양한 관점 질문과 출처 grounding으로 outline을 만들고, source bias transfer와 unrelated-fact over-association을 주의점으로 남긴다. bizplan은 source-index.xlsx와 evidence-ledger.xlsx를 통해 같은 문제를 사업계획서 영역에서 다룬다.",
    },
    "Futurist": {
        "persona": "미래학자",
        "summary": "사업계획서 소프트웨어는 '생성'에서 '검증 가능한 사업 운영체계'로 이동할 가능성이 있다.",
        "body": "미래형 제안서 도구는 고객 인터뷰, 공고 요건, 논문·특허·시장 근거, 재무 모델, 평가위원 질문까지 하나의 코어로 묶는다. 완성 문서는 마지막 출력일 뿐이며, 핵심 자산은 반론을 견디는 evidence graph다.",
    },
}

CONTRADICTIONS = [
    ["AI가 사업계획서 작성 속도를 높인다", "속도가 빨라질수록 허위 고객·매출·특허를 만들 위험도 커진다", "속도 KPI보다 evidence tag coverage와 출처 없는 핵심통계 0건을 제품 KPI로 둔다"],
    ["한 개 business-core.yaml이 여러 문서를 일관되게 만든다", "정부지원서·R&D·IR·제안서는 평가 논리가 서로 다르다", "코어는 단일 출처로 고정하고, 출력은 문서 유형별 평가 논리로 변환한다"],
    ["자동화는 대량 제출을 가능하게 한다", "bizplan 스킬은 인터뷰 우선·공고 분석 우선을 요구한다", "자동화 범위를 작성이 아니라 누락 탐지·근거 연결·서식 변환으로 제한한다"],
    ["시장 기회가 커 보인다", "현재 가격·고객 수·시장 규모는 검증 전이다", "랜딩 문서에는 [확인 필요]를 노출하고, MVP 전 bottom-up 인터뷰를 Gate 1로 둔다"],
    ["평가위원 시뮬레이션은 점수 개선에 도움이 된다", "표면적 문장 게임으로 흐르면 실제 사업성은 개선되지 않는다", "admin·tech·biz·skeptic 4역할이 중대 사실오류·무출처 통계·숫자 불일치를 차단한다"],
]

SYNTHESIS = """# STORM Synthesis · BizPlan Evidence OS

BizPlan Evidence OS의 제품 정의는 'AI 사업계획서 작성기'가 아니다. 더 정확한 정의는 '사업계획서에 들어가는 모든 주장, 수치, 출처, 가정, 평가자 질문을 하나의 코어에서 추적하는 증거 원장 SaaS'다.

핵심 고객은 [확인 필요]이다. 다만 가설상으로는 정부지원사업·R&D 과제·공공 제안서를 반복 제출하는 스타트업, 연구소, 컨설턴트, 대학 산학협력 조직이 후보가 된다. 이 가설은 인터뷰로 검증해야 하며, 실제 구매자와 사용자를 분리해야 한다.

가장 강한 기능 가설은 세 가지다. 첫째, business-core.yaml이 문제·해결·기술·시장·사업모델·실행·예산을 단일 출처로 유지한다. 둘째, source-index.xlsx와 evidence-ledger.xlsx가 모든 핵심 통계와 주장을 역추적한다. 셋째, 평가위원 4역할 시뮬레이션이 제출 전 반론을 노출한다.

이 산출물은 완성 사업계획서가 아니라 1차 랜딩 브리프다. 가격, 시장 규모, 실제 고객, 구매 전환, 공고별 배점 적합성은 모두 [확인 필요]로 남겨야 한다. 정직한 미완을 숨기지 않는 것이 bizplan 스킬의 핵심 품질이다.
"""

PEER_REVIEW = """# STORM Peer Review

BLOCKER 1: 시장 규모와 매출 잠재력은 아직 출처가 없다. 랜딩 문서에서 숫자로 주장하지 말고 [확인 필요]로 남긴다.

BLOCKER 2: 'AI가 사업계획서를 써준다'는 표현은 너무 넓고 경쟁이 심하다. 포지션을 '증거 원장 + 평가위원 시뮬레이션 + 다중 문서 컴파일러'로 좁힌다.

BLOCKER 3: bizplan 스킬은 AskUserQuestion 기반 인터뷰를 절대 규칙으로 두지만, 이 HTML 산출은 사용자의 인터뷰 없이 만든 데모다. 따라서 실제 사업계획서가 아니라 skill-derived concept brief라고 명시해야 한다.

PASS 조건: 모든 수치가 evidence tag를 가진다. 출처 없는 핵심 통계가 없다. [확인 필요] 항목이 사용자 행동 게이트로 닫힌다. business-core.yaml과 source-index.xlsx가 다음 액션의 중심이다.
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
    body = "".join(
        "<tr>" + "".join((f'<th scope="row">{esc(c)}</th>' if i == 0 else f'<td>{c}</td>') for i, c in enumerate(row)) + "</tr>"
        for row in rows
    )
    return f'<div class="table-scroll"><table><caption>{esc(caption)}</caption><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def markdownish_to_html(text: str) -> str:
    out: list[str] = []
    in_ul = False
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            if in_ul:
                out.append("</ul>")
                in_ul = False
            continue
        if line.startswith("- ") or re.match(r"^\d+\.\s", line):
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            item = re.sub(r"^\d+\.\s+", "", line[2:] if line.startswith("- ") else line)
            out.append(f"<li>{esc(item)}</li>")
            continue
        if in_ul:
            out.append("</ul>")
            in_ul = False
        if line.startswith("# "):
            out.append(f"<h3>{esc(line[2:])}</h3>")
        elif line.startswith("## "):
            out.append(f"<h3>{esc(line[3:])}</h3>")
        else:
            out.append(f"<p>{esc(line)}</p>")
    if in_ul:
        out.append("</ul>")
    return "\n".join(out)


def source_details(title: str, text: str, open_: bool = False) -> str:
    open_attr = " open" if open_ else ""
    return (
        f'<details class="source-preserve" style="margin:34px 0 0 24px;border-left:6px solid var(--accent);padding-left:20px"{open_attr}>'
        f'<summary style="padding:20px 24px 20px 34px;display:flex;align-items:center;gap:12px;flex-wrap:wrap"><strong>{esc(title)}</strong><span class="tag">원문 보존</span></summary>'
        f'<div class="source-body" style="padding:0 28px 30px 34px"><div style="border-left:1px solid var(--line);padding:24px 0 2px 24px">{markdownish_to_html(text)}</div></div>'
        "</details>"
    )


def make_storm_markdown() -> tuple[str, str, str, str]:
    scan = ["# Multi-Perspective Scan · BizPlan Evidence OS"]
    for name, row in STORM_SCAN.items():
        scan.extend([f"## {name} · {row['persona']}", row["summary"], row["body"], ""])
    contradiction = "# Contradiction Map\n" + "\n".join(f"- {a} ↔ {b} → {c}" for a, b, c in CONTRADICTIONS)
    return "\n".join(scan), contradiction, SYNTHESIS, PEER_REVIEW


def build_hero(scan_md: str) -> str:
    vt = """
<section class="vt-shell" aria-label="BizPlan Evidence OS 핵심 지도">
  <div class="vt-frame"><div class="vt-demo"><div class="hm-grid">
    <article class="hm-card"><div class="vt-kicker">Problem</div><h3>계획서가 빨리 써질수록 검증 공백도 빨라진다</h3><p class="vt-text">고객·매출·특허·시장 수치가 출처 없이 섞이면 심사 반론을 견디지 못한다.</p></article>
    <article class="hm-card" style="--c:var(--vt-blue)"><div class="vt-kicker">Core</div><h3>business-core.yaml이 단일 출처가 된다</h3><p class="vt-text">문제·해결·시장·실행·예산을 하나의 코어에서 유지하고 문서 유형별로 변환한다.</p></article>
    <article class="hm-card" style="--c:var(--vt-green)"><div class="vt-kicker">Proof</div><h3>source-index와 evaluator simulation으로 닫는다</h3><p class="vt-text">모든 핵심 주장을 원장에 연결하고, admin·tech·biz·skeptic 평가로 출고 검사한다.</p></article>
  </div><div class="hm-result"><b>결론: 사업계획서 생성기가 아니라 증거 운영체계</b><span>완성 문장보다 반론을 견디는 추적 가능성이 제품 가치다.</span></div></div></div>
</section>
"""
    cards = "".join(
        f'<article class="summary-card"><div class="label">{esc(k)} · {esc(v["persona"])}</div><h3>{esc(v["summary"])}</h3><p>{esc(v["body"])}</p></article>'
        for k, v in STORM_SCAN.items()
    )
    toc = """
<nav class="toc-map" id="document-toc" aria-label="문서 목차"><span class="label">문서 목차</span><p>요약, 가치 제안, 실행 방식, FAQ, 다음 게이트, 출처 허브로 이동합니다.</p><div class="toc-pills"><a class="toc-pill" href="#hero"><b>1</b>Hero</a><a class="toc-pill" href="#value"><b>2</b>Value</a><a class="toc-pill" href="#workflow"><b>3</b>Workflow</a><a class="toc-pill" href="#faq"><b>4</b>FAQ</a><a class="toc-pill" href="#cta"><b>5</b>Gate</a><a class="toc-pill" href="#source-note"><b>6</b>Sources</a></div></nav>
"""
    return f"""
<div id="hero"></div>
{toc}
{h2('01', 'Hero · BizPlan Evidence OS', 'hero', 'bizplan 스킬의 7대 절대 규칙과 STORM 다관점 리서치를 결합해 선택한 자유 주제다.')}
<p><strong>BizPlan Evidence OS</strong>는 정부지원사업·R&amp;D 과제·IR 덱·공공 제안서의 문장을 대신 꾸미는 도구가 아니다. 사용자의 현장 사실, 공고 요건, 시장·기술·특허·논문 근거, 재무 가정, 평가위원 질문을 <span class="hl">하나의 추적 가능한 사업 코어</span>로 묶는 증거 원장 SaaS 콘셉트다.</p>
<p>이 데모는 사용자의 실제 인터뷰 없이 만든 <strong>skill-derived concept brief</strong>이므로 완성 사업계획서가 아니다. 가격·시장 규모·고객·매출·전환율은 모두 <span class="tag">[확인 필요]</span>로 남기고, 검증 전에는 핵심 통계로 쓰지 않는다.</p>
{vt}
<h3>STORM 다섯 관점이 남긴 판단</h3>
<div class="card-grid rail-cycle">{cards}</div>
{source_details('STORM Multi-Perspective Scan 원문', scan_md)}
"""


def build_value_props() -> str:
    rows = [
        ["제품 정의", "[가정] 사업계획서 증거 원장 + 다중 문서 컴파일러", "문장 생성기가 아닌 검증 시스템"],
        ["핵심 고객", "[확인 필요] 정부지원/R&D/공공 제안서를 반복 제출하는 조직", "인터뷰로 구매자·사용자 분리 필요"],
        ["단일 출처", "[사실] bizplan 스킬은 business-core.yaml을 모든 문서의 진실원으로 둔다", "숫자·가정·출처 일관성"],
        ["증거 원장", "[사실] source-index.xlsx와 evidence-ledger.xlsx를 통해 Claim ↔ 출처 ↔ 섹션을 연결한다", "출처 없는 핵심통계 0건"],
        ["평가 검증", "[사실] admin·tech·biz·skeptic 4역할 평가위원 시뮬레이션을 수행한다", "반론을 견디는 사업 논리"],
        ["사업성", "[확인 필요] 가격·TAM/SAM/SOM·전환율·CAC/LTV", "공식/유료 자료와 인터뷰로 검증 전까지 주장 금지"],
    ]
    return f"""
<div id="value"></div>
{h2('02', 'Value Props · 반론을 견디는 사업 논리의 제품화', 'value', 'bizplan 스킬의 절대 규칙을 사업 제품의 가치 제안으로 번역했다.')}
{table(rows, 'BizPlan Evidence OS 가치 제안 매트릭스', ['축', '태그가 붙은 주장', '평가/사업 포인트'])}
<div class="impact-grid"><article class="impact-card"><h3>Evidence Ledger</h3><p>모든 Claim은 출처·산식·반영 섹션·counter evidence와 연결된다. 출처가 없으면 삭제가 아니라 <strong>[확인 필요]</strong>로 강등한다.</p></article><article class="impact-card"><h3>Core Compiler</h3><p>하나의 business-core.yaml에서 정부지원서, R&amp;D 계획서, 투자덱, 제안서를 각각 다른 평가 논리로 파생한다.</p></article><article class="impact-card"><h3>Evaluator Simulator</h3><p>행정·기술·사업성·회의주의 평가자가 점수와 치명적 결함을 분리해 재작업 우선순위를 만든다.</p></article><article class="impact-card"><h3>Honest Incomplete</h3><p>검증 전 수치를 멋지게 포장하지 않는다. 모르는 것은 [확인 필요]로 남기는 것이 제품의 신뢰 기능이다.</p></article></div>
<div class="source-note"><h3>비즈니스 코어 초안</h3><p><strong>problem.core_problem:</strong> [가정] 사업계획서 작성자는 공고 요구·시장 수치·기술 근거·재무 가정·평가 질문을 서로 다른 파일에서 관리해 숫자 불일치와 출처 누락을 반복한다.</p><p><strong>solution.core_mechanism:</strong> [가정] business-core.yaml을 중심으로 source-index.xlsx, evidence-ledger.xlsx, market-sizing.xlsx, financial-model.xlsx, evaluator scorecard를 연결해 문서보다 먼저 검증 그래프를 만든다.</p><p><strong>customer.primary_customer:</strong> [확인 필요] 정부지원사업·R&amp;D 과제를 반복 제출하는 스타트업/연구소/컨설팅 조직. 구매자와 실제 작성자는 다를 수 있다.</p><p><strong>business_model.pricing:</strong> [확인 필요] 사용자당 구독, 프로젝트당 패키지, 컨설턴트 좌석형, 기관용 라이선스 중 어느 모델이 맞는지 인터뷰 필요.</p><p><strong>traction:</strong> [확인 필요] 실제 고객·매출·계약·LOI는 현재 이 데모에 존재하지 않는다. 임의 창작 금지.</p></div>
"""


def build_how_it_works(contradiction_md: str) -> str:
    wg = """
<section class="wg-16" aria-labelledby="wg-16-title"><header class="wg-16-head"><p class="wg-16-kicker">Implementation Plan · Evidence OS MVP</p><h2 id="wg-16-title" class="wg-16-h">인터뷰에서 제출 직전 평가위원 시뮬레이션까지</h2><p class="wg-16-lead">자동 작성보다 먼저 공고·인터뷰·리서치·코어·원장·서식·검증 게이트를 통과시킵니다.</p></header><div class="wg-16-panel"><h3 class="wg-16-h3">마일스톤 타임라인</h3><ol class="wg-16-ms"><li class="wg-16-ms-item wg-16-active"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">M1 · Gate 0~2 수집/인터뷰/리서치</span><span class="wg-16-badge wg-16-bd-active">MVP 1</span></div><p class="wg-16-ms-desc">공고 분석, 질문 transcript, source-index, 부정적 근거 수집을 한 화면에 묶습니다.</p></div></li><li class="wg-16-ms-item"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">M2 · Gate 3~4 business-core·number registry</span><span class="wg-16-badge">MVP 2</span></div><p class="wg-16-ms-desc">business-core.yaml, evidence-ledger, market-sizing, financial-model을 동기화합니다.</p></div></li><li class="wg-16-ms-item"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">M3 · Gate 6~7 document compiler·evaluator audit</span><span class="wg-16-badge">MVP 3</span></div><p class="wg-16-ms-desc">공식 서식 매핑, HTML/DOCX/PPTX 출력, 4역할 평가위원 시뮬레이션을 연결합니다.</p></div></li></ol><h3 class="wg-16-h3">데이터 플로우</h3><div class="wg-16-flow" aria-label="BizPlan Evidence OS 데이터 플로우"><div class="wg-16-fnode">공고·아이디어<span class="wg-16-fnode-s">notice + interview</span></div><div class="wg-16-fnode">리서치 원천<span class="wg-16-fnode-s">source-index</span></div><div class="wg-16-fnode wg-16-fnode-good">사업 코어<span class="wg-16-fnode-s">business-core.yaml</span></div><div class="wg-16-fnode wg-16-fnode-hot">증거 원장<span class="wg-16-fnode-s">evidence-ledger</span></div><div class="wg-16-fnode wg-16-fnode-q">평가/출력<span class="wg-16-fnode-s">scorecard + HTML</span></div></div><h3 class="wg-16-h3">리스크 평가</h3><div class="wg-16-table-wrap"><div class="table-scroll"><table class="wg-16-table"><caption>BizPlan Evidence OS MVP 리스크 — 가능성·영향·완화책</caption><thead><tr><th scope="col">리스크</th><th scope="col">가능성</th><th scope="col">영향</th><th scope="col">완화책</th></tr></thead><tbody><tr><th scope="row">사용자 인터뷰 없이 자동 완성 기대</th><td><span class="wg-16-lv wg-16-lv-hi">높음</span></td><td><span class="wg-16-lv wg-16-lv-hi">높음</span></td><td>AskUserQuestion Gate와 [확인 필요] 잠금 표시</td></tr><tr><th scope="row">출처 입력이 번거로워 이탈</th><td><span class="wg-16-lv wg-16-lv-mid">중</span></td><td><span class="wg-16-lv wg-16-lv-hi">높음</span></td><td>브라우저 저장·문서 업로드·자동 source-index 보조</td></tr><tr><th scope="row">평가위원 점수가 문장 게임화</th><td><span class="wg-16-lv wg-16-lv-mid">중</span></td><td><span class="wg-16-lv wg-16-lv-mid">중</span></td><td>무출처 통계·숫자 불일치·중대 사실오류를 hard blocker로 둠</td></tr></tbody></table></div></div></div></section>
"""
    return f"""
<div id="workflow"></div>
{h2('03', 'How It Works · 21단계 게이트를 MVP 플로우로 압축', 'flow', 'landing_brief_html 권장 wg-16 구현 계획 위젯으로 bizplan 워크플로우를 제품 실행 단계로 바꿨다.')}
{wg}
<h3>Contradiction Map · 숨기지 말아야 할 긴장</h3>
{table(CONTRADICTIONS, 'STORM Contradiction Map', ['주장 A', '충돌 근거', '실행 해석'])}
{source_details('Contradiction Map 원문', contradiction_md, open_=True)}
"""


def build_faq(synthesis_md: str, peer_md: str) -> str:
    return f"""
<div id="faq"></div>
{h2('04', 'FAQ · 평가자와 구매자가 바로 물을 질문', 'faq', '회의적인 반론을 제품 요구사항으로 전환했다.')}
<div class="card-grid rail-cycle"><article class="summary-card"><h3>Q1. 그냥 ChatGPT로 사업계획서를 쓰면 안 되나?</h3><p>쓸 수 있다. 하지만 bizplan 스킬의 핵심은 문장 생성이 아니라 <strong>AI 임의 창작 금지</strong>, 사실/추정/가정/목표 분리, 출처 없는 핵심통계 0건이다. Evidence OS는 빠른 문장보다 추적 가능한 근거를 제품화한다.</p></article><article class="summary-card"><h3>Q2. 실제 시장이 있는가?</h3><p><span class="tag">[확인 필요]</span> 아직 이 데모에는 공식 시장 수치와 구매 인터뷰가 없다. 다음 단계는 고객군별 인터뷰와 bottom-up SOM 산식이다. 수치 없이 시장이 크다고 주장하지 않는다.</p></article><article class="summary-card"><h3>Q3. 사업계획서 컨설턴트를 대체하는가?</h3><p>[가정] 대체보다 보강에 가깝다. 컨설턴트가 쓰는 판단과 사용자 경험을 코어·원장·평가 루프로 구조화해 재작업과 오류를 줄이는 방향이 더 설득력 있다.</p></article><article class="summary-card"><h3>Q4. MVP에서 가장 먼저 만들어야 할 것은?</h3><p>문서 에디터보다 먼저 <strong>Claim table → source-index → business-core.yaml → scorecard</strong>의 최소 흐름이다. 출력 HTML/DOCX/PPTX는 코어가 잠긴 뒤에야 신뢰를 얻는다.</p></article></div>
{source_details('STORM Synthesis 원문', synthesis_md)}
{source_details('STORM Peer Review 원문', peer_md)}
"""


def build_cta() -> str:
    rows = [
        ["Gate 1", "[확인 필요] 실제 고객 10명 인터뷰", "구매자·사용자·현재 대안·지불 의사 분리"],
        ["Gate 2", "[확인 필요] 공식/유료 자료 기반 시장·경쟁 조사", "출처 없는 TAM/SAM/SOM 주장 금지"],
        ["Gate 3", "business-core.yaml MVP 스키마", "문제→해결→제품→기술→시장→수익→실행→예산 사슬"],
        ["Gate 4", "evidence-ledger.xlsx + number-registry", "가격·고객수·매출·비용·일정 불일치 0건"],
        ["Gate 7", "4역할 평가위원 시뮬레이션", "중대 사실오류·무출처 통계·숫자 불일치 hard blocker"],
    ]
    return f"""
<div id="cta"></div>
{h2('05', 'CTA · 지금 당장 다음 단계로 잠글 5개 게이트', 'cta', '이 콘셉트를 실제 사업계획서로 착각하지 않도록 검증 행동을 명확히 남겼다.')}
{table(rows, 'BizPlan Evidence OS 다음 검증 게이트', ['Gate', '해야 할 일', '완료 기준'])}
<div class="try soft-cta"><h2>{body_icon('cta')}최종 한 줄</h2><p>이 주제의 강점은 “AI가 사업계획서를 써준다”가 아니라, <strong>거짓을 못 쓰게 만들고 반론을 먼저 보여주는 사업계획서 증거 운영체계</strong>라는 포지션이다.</p></div>
"""


def build_source_note() -> str:
    links = "".join(
        f'<li><a href="{esc(s["url"])}" target="_blank" rel="noopener noreferrer">{esc(s["name"])}</a> — {esc(s["role"])}</li>'
        for s in SOURCE_LIST
    )
    return f"""
<div id="source-note"></div>
{h2('06', 'Source Hub · 사용한 스킬 내용과 STORM 근거', 'source', '로컬 bizplan 스킬 파일과 STORM 산출물을 분리해 보존했다.')}
<p>보조 파일: <a href="sources/storm-scan.md">storm-scan.md</a> · <a href="sources/storm-contradiction-map.md">contradiction-map.md</a> · <a href="sources/storm-synthesis.md">synthesis.md</a> · <a href="sources/storm-peer-review.md">peer-review.md</a> · <a href="sources/bizplan-application.json">bizplan 적용 기록</a></p><ol class="refs">{links}</ol>
"""


def copy_sources(scan_md: str, contradiction_md: str, synthesis_md: str, peer_md: str) -> dict:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    (OUT / "pages").mkdir()
    SOURCES.mkdir()
    (SOURCES / "assets").mkdir()
    (SOURCES / "screenshots").mkdir()

    copy_map = [
        (BIZ / "SKILL.md", "bizplan-SKILL.md"),
        (BIZ / "references" / "evidence-tagging.md", "evidence-tagging.md"),
        (BIZ / "references" / "04-research-engine.md", "research-engine.md"),
        (BIZ / "references" / "07-business-core.md", "business-core.md"),
        (BIZ / "references" / "11-document-types.md", "document-types.md"),
        (BIZ / "references" / "12-verification.md", "verification.md"),
        (BIZ / "references" / "document-output.md", "document-output.md"),
        (STORM / "SKILL.md", "storm-SKILL.md"),
        (STORM / "references" / "storm-pipeline.md", "storm-pipeline.md"),
        (STORM / "references" / "provenance.md", "storm-provenance.md"),
    ]
    for src, name in copy_map:
        if src.exists():
            shutil.copyfile(src, SOURCES / name)

    (SOURCES / "source-list.json").write_text(json.dumps(SOURCE_LIST, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (SOURCES / "storm-scan.md").write_text(scan_md + "\n", encoding="utf-8")
    (SOURCES / "storm-contradiction-map.md").write_text(contradiction_md + "\n", encoding="utf-8")
    (SOURCES / "storm-synthesis.md").write_text(synthesis_md + "\n", encoding="utf-8")
    (SOURCES / "storm-peer-review.md").write_text(peer_md + "\n", encoding="utf-8")
    (SOURCES / "storm-report.json").write_text(
        json.dumps(
            {
                "topic": "BizPlan Evidence OS — 증거 원장 기반 사업계획서 작성·검증 SaaS",
                "mode": "solo-fallback-by-main-agent",
                "environment": {"cmux": "missing", "kimi": "missing"},
                "public_sources": PUBLIC_SOURCES,
                "souls": STORM_SCAN,
                "contradictions": CONTRADICTIONS,
                "synthesis": synthesis_md,
                "peer_review": peer_md,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (SOURCES / "bizplan-application.json").write_text(
        json.dumps(
            {
                "skill": "bizplan",
                "source_path": str(BIZ.relative_to(ROOT)),
                "selected_topic": "BizPlan Evidence OS",
                "selected_document_type": "landing_brief_html concept brief, not a final grant plan",
                "selected_mode": MODE,
                "profile": PROFILE,
                "applied_bizplan_rules": [
                    "AI 임의 창작 금지",
                    "사실/추정/가정/목표/확인 필요 태그 노출",
                    "business-core.yaml 단일 출처 원칙",
                    "조사와 작성 분리",
                    "source-index/evidence-ledger 추적",
                    "4역할 평가위원 시뮬레이션",
                ],
                "disclaimer": "사용자 인터뷰와 시장조사가 아직 없으므로 완성 사업계획서가 아니라 스킬 기반 콘셉트 브리프다.",
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    shutil.copyfile(SKILL / "manifest.json", SOURCES / "adaptive-html-final-manifest.json")
    (SOURCES / "profile.json").write_text(json.dumps({"profile": PROFILE}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    placeholder_map = {
        "layout": LAYOUT,
        "HERO": "vt hero-map + STORM scan + topic disclaimer",
        "VALUE_PROPS": "evidence-tagged value proposition matrix + business-core sketch",
        "HOW_IT_WORKS": "wg-16 implementation plan + contradiction map",
        "FAQ": "buyer/evaluator questions + synthesis/peer review preserved",
        "CTA": "five validation gates",
        "SOURCE_NOTE": "local bizplan sources + public STORM sources",
    }
    (SOURCES / "layout-placeholder-map.json").write_text(json.dumps(placeholder_map, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    asset_hashes = {}
    for name, _slot in INLINE_ORDER:
        src = ASSETS / name
        if src.exists():
            shutil.copyfile(src, SOURCES / "assets" / name)
            asset_hashes[name] = sha(src)
    core_blob = "\n".join(read(ASSETS / name) for name in CORE_ORDER)
    integrity = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "skill": "adaptive-html-final",
        "version": version(),
        "profile": PROFILE,
        "mode": MODE,
        "layout": LAYOUT,
        "core_css_sha256": text_sha(core_blob),
        "asset_order": CORE_ORDER,
        "asset_sha256": asset_hashes,
        "inline_order": [name for name, _slot in INLINE_ORDER],
    }
    (SOURCES / "css-integrity.json").write_text(json.dumps(integrity, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    evidence_files = [
        "AGENTS.md",
        "skills/adaptive-html-final/SKILL.md",
        "skills/adaptive-html-final/manifest.json",
        "skills/adaptive-html-final/assets/base.html",
        "skills/adaptive-html-final/assets/layouts/landing-brief.html",
        "skills/adaptive-html-final/assets/visual-html-templates/01-hero-map.html",
        "skills/adaptive-html-final/assets/widget-templates/16-implementation-plan.html",
        "orginal_skill/bizplan/SKILL.md",
        "orginal_skill/bizplan/references/evidence-tagging.md",
        "orginal_skill/bizplan/references/04-research-engine.md",
        "orginal_skill/bizplan/references/07-business-core.md",
        "orginal_skill/bizplan/references/11-document-types.md",
        "orginal_skill/bizplan/references/12-verification.md",
        "orginal_skill/bizplan/references/document-output.md",
        "orginal_skill/storm-research/SKILL.md",
        "orginal_skill/storm-research/references/storm-pipeline.md",
        "orginal_skill/storm-research/references/provenance.md",
    ]
    evidence = {
        "mode": MODE,
        "profile": PROFILE,
        "layout": LAYOUT,
        "layout_class": LAYOUT_CLASS,
        "primary_vt": PRIMARY_VT,
        "primary_wg": PRIMARY_WG,
        "section_mapping": placeholder_map,
        "files": [{"path": p, "sha256": sha(ROOT / p)} for p in evidence_files if (ROOT / p).exists()],
        "input_snapshots": [
            "sources/bizplan-SKILL.md",
            "sources/evidence-tagging.md",
            "sources/business-core.md",
            "sources/storm-scan.md",
            "sources/storm-contradiction-map.md",
            "sources/storm-synthesis.md",
            "sources/storm-peer-review.md",
            "sources/bizplan-application.json",
        ],
        "research_route": "storm-research solo fallback; local bizplan skill + public STORM sources; no invented business statistics",
    }
    (SOURCES / "build-evidence.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return integrity


def css_slots(integrity: dict) -> dict[str, str]:
    slots = {}
    for name, slot in INLINE_ORDER:
        css = read(ASSETS / name) if (ASSETS / name).exists() else ""
        if name == "theme.css":
            css = f"/* adaptive-html-final-core-css-sha256: {integrity['core_css_sha256']} */\n" + css
        if name in ("shape-visuals.css", "workflow-visuals.css"):
            css = ""
        slots[slot] = css.rstrip()
    return slots


def render(scan_md: str, contradiction_md: str, synthesis_md: str, peer_md: str, integrity: dict) -> str:
    layout = read(ASSETS / "layouts" / LAYOUT)
    meta = (
        f"<span>{MODE}</span><span>{LAYOUT}</span><span>profile {PROFILE}</span>"
        f"<span>adaptive-html-final v{version()}</span><span>bizplan × STORM solo fallback</span>"
    )
    repl = {
        "{{KICKER}}": '<span class="kicker-text">bizplan skill × STORM Research × adaptive-html-final</span>',
        "{{TITLE}}": "BizPlan Evidence OS",
        "{{SUBTITLE}}": "증거 태그·business-core.yaml·평가위원 시뮬레이션으로 사업계획서 생성의 허위 위험을 줄이는 콘셉트 브리프",
        "{{META}}": meta,
        "{{HERO}}": build_hero(scan_md),
        "{{VALUE_PROPS}}": build_value_props(),
        "{{HOW_IT_WORKS}}": build_how_it_works(contradiction_md),
        "{{FAQ}}": build_faq(synthesis_md, peer_md),
        "{{CTA}}": build_cta(),
        "{{SOURCE_NOTE}}": build_source_note(),
    }
    body = layout
    for key, value in repl.items():
        body = body.replace(key, value)
    body = body.replace(
        "</div></header>",
        "</div><div class=\"generated-row\"><p class=\"generated-date\">생성 기준: 2026-06-20 KST · bizplan 로컬 스킬 · STORM solo fallback · landing_brief_html · layout-first</p><div class=\"lens-strip\" aria-label=\"적용 렌즈\"><span class=\"lens-strip-label\">LENS</span><span class=\"lens-chip\">Evidence Tagging</span><span class=\"lens-chip\">Business Core</span><span class=\"lens-chip\">Source Ledger</span><span class=\"lens-chip\">Evaluator Simulation</span><span class=\"lens-chip\">Honest Incomplete</span></div></div></header>",
        1,
    )

    title = f"BizPlan Evidence OS · bizplan STORM · adaptive-html-final v{version()}"
    description = "bizplan 스킬의 증거 태깅·business-core.yaml·평가위원 검증을 STORM 다관점 리서치로 재구성한 현재 프로젝트 최신 스타일 HTML 브리프."
    json_ld = json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": title,
            "description": description,
            "inLanguage": "ko",
            "datePublished": "2026-06-20",
            "author": {"@type": "Organization", "name": "adaptive-html-final"},
            "keywords": ["bizplan", "사업계획서", "증거 원장", "business-core.yaml", "STORM", "R&D 계획서", "평가위원 시뮬레이션"],
        },
        ensure_ascii=False,
    )
    doc = read(ASSETS / "base.html")
    slots = {
        "{{TITLE}}": title,
        "{{DESCRIPTION}}": description,
        "{{JSON_LD_BLOCK}}": f'<script type="application/ld+json">{json_ld}</script>',
        "{{BODY}}": body,
        "{{FOOTER}}": "",
    }
    slots.update(css_slots(integrity))
    for key, value in slots.items():
        doc = doc.replace(key, value)
    leftovers = sorted(set(re.findall(r"{{[^}]+}}", doc)))
    if leftovers:
        raise RuntimeError(f"unresolved placeholders: {leftovers}")
    return re.sub(r"\n{4,}", "\n\n\n", doc)


def content_evidence(doc: str) -> None:
    visible = re.sub(r"<style\b[^>]*>[\s\S]*?</style>", "", doc, flags=re.I)
    visible = re.sub(r"<script\b[^>]*>[\s\S]*?</script>", "", visible, flags=re.I)
    visible = re.sub(r"<[^>]+>", " ", visible)
    visible = re.sub(r"\s+", " ", html.unescape(visible))
    required = [
        "BizPlan Evidence OS",
        "bizplan",
        "STORM",
        "business-core.yaml",
        "source-index.xlsx",
        "evidence-ledger.xlsx",
        "[사실]",
        "[확인 필요]",
        "평가위원",
        "Contradiction Map",
        "Source Hub",
    ]
    missing = [marker for marker in required if marker not in visible]
    evidence = {
        "storm_soul_count": len(STORM_SCAN),
        "source_count": len(SOURCE_LIST),
        "required_markers_missing": missing,
        "output_visible_text_chars": len(visible),
        "pass": not missing and len(visible) > 8500,
    }
    (SOURCES / "content-preservation.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not evidence["pass"]:
        raise RuntimeError(str(evidence))


def main() -> None:
    scan, contradiction, synthesis, peer = make_storm_markdown()
    integrity = copy_sources(scan, contradiction, synthesis, peer)
    doc = render(scan, contradiction, synthesis, peer, integrity)
    (OUT / "index.html").write_text(doc, encoding="utf-8")
    content_evidence(doc)
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
