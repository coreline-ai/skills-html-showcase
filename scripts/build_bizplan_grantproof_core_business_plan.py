#!/usr/bin/env python3
"""Build a skill-only business plan HTML.

Content source rule for this artifact:
- Business-plan content is derived only from orginal_skill/bizplan/SKILL.md and selected bizplan references.
- adaptive-html-final is used only as the HTML template/rendering system.
- No external market/customer/revenue facts are invented; unknowns stay [확인 필요].
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

OUT = ROOT / "output" / "2026-06-20" / "bizplan-grantproof-core-business-plan"
SOURCES = OUT / "sources"

MODE = "expert_html"
PROFILE = "auto"
LAYOUT = "expert-report.html"
LAYOUT_CLASS = "layout-expert"
PRIMARY_VT = "risk-matrix"
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
    "summary": "audit",
    "decision": "decision",
    "architecture": "database",
    "risk": "warning",
    "roadmap": "timeline",
    "check": "check",
    "final": "success",
    "source": "source",
}

LOCAL_SOURCES = [
    {"name": "bizplan/SKILL.md", "url": "sources/bizplan-SKILL.md", "role": "7대 절대 규칙, 21단계 게이트, HTML 항상 생성 원칙"},
    {"name": "evidence-tagging.md", "url": "sources/evidence-tagging.md", "role": "[사실] [추정] [가정] [목표] [확인 필요] 태그 체계"},
    {"name": "research-engine.md", "url": "sources/research-engine.md", "role": "조사와 작성 분리, source-index.xlsx, 부정적 근거 수집"},
    {"name": "business-core.md", "url": "sources/business-core.md", "role": "business-core.yaml, evidence-ledger, Gate 3/4 논리·숫자 일관성"},
    {"name": "document-types.md", "url": "sources/document-types.md", "role": "정부지원/R&D/IR/제안서 유형별 변환 논리"},
    {"name": "verification.md", "url": "sources/verification.md", "role": "admin·tech·biz·skeptic 4역할 평가위원 시뮬레이션"},
    {"name": "document-output.md", "url": "sources/document-output.md", "role": "HTML 산출·렌더링 검사·제출 체크리스트"},
]

BUSINESS_CORE = """project:
  name: "GrantProof Core"
  document_type: "정부 창업/중소기업 지원사업 기반 사업계획서" # [가정]
  purpose: "사업계획서 작성 과정의 출처·가정·숫자 일관성 검증 SaaS" # [가정]
  status: "skill-only concept draft; 사용자 인터뷰·외부시장조사 전" # [사실] 생성 범위
business:
  definition: "반론을 견디는 사업 논리를 만들기 위한 evidence ledger + business-core compiler" # [가정]
  vision: "사업계획서가 문장 생성물이 아니라 검증 가능한 의사결정 기록이 되게 한다" # [목표]
customer:
  primary_customer: "정부지원사업·R&D·공공제안서를 반복 작성하는 조직" # [확인 필요]
  buyer: "대표/PM/산학협력단/컨설팅 조직 구매책임자" # [확인 필요]
  user: "사업계획서 작성자, 기획자, 컨설턴트, 연구책임자" # [확인 필요]
problem:
  core_problem: "문서마다 수치·가정·출처가 갈라져 평가자가 반론하면 방어가 어렵다" # [가정]
  current_alternatives: "템플릿, 문서 작성 AI, 스프레드시트, 컨설팅" # [가정]
  missing_evidence: "실제 빈도·재작업 비용·탈락 원인 데이터" # [확인 필요]
solution:
  core_mechanism: "business-core.yaml을 단일 출처로 삼고 source-index.xlsx/evidence-ledger.xlsx와 연결한다" # [사실] bizplan 스킬 원칙
  key_features:
    - "Claim 태그: [사실]/[추정]/[가정]/[목표]/[확인 필요]" # [사실]
    - "문서 유형 변환: 정부지원/R&D/IR/제안서" # [사실]
    - "평가위원 4역할 시뮬레이션" # [사실]
market:
  tam: "[확인 필요] 외부 시장조사 전에는 수치 주장 금지"
  sam: "[확인 필요] 반복 작성 조직 세그먼트 정의 필요"
  som: "[확인 필요] 인터뷰 기반 bottom-up 산식 필요"
business_model:
  pricing: "[확인 필요] 좌석형/프로젝트형/기관형 중 인터뷰 후 결정"
traction:
  customers: "[확인 필요] 현재 실제 고객·계약·LOI 없음"
  revenue: "[확인 필요] 실매출 없음; 임의 창작 금지"
execution:
  next_gate: "Gate 1 고객 인터뷰 10건, Gate 2 source-index, Gate 3 business-core MVP" # [목표]
"""

EVIDENCE_LEDGER = [
    ["EL#01", "business-core.yaml은 모든 파생 문서의 유일한 진실원이다", "[사실]", "bizplan/SKILL.md, business-core.md", "제품 핵심 구조"],
    ["EL#02", "모든 수치·주장은 [사실]/[추정]/[가정]/[목표]/[확인 필요] 중 하나로 태깅되어야 한다", "[사실]", "evidence-tagging.md", "신뢰성 원칙"],
    ["EL#03", "출처 없는 핵심 통계는 금지된다", "[사실]", "bizplan/SKILL.md, evidence-tagging.md", "검증 기준"],
    ["EL#04", "GrantProof Core 고객군과 가격은 아직 검증되지 않았다", "[확인 필요]", "사용자 인터뷰 전", "시장/모델 Gate"],
    ["EL#05", "문서 작성 AI가 아니라 증거 원장 SaaS로 포지셔닝한다", "[가정]", "bizplan 철학에서 도출", "차별화 가설"],
]

RISKS = [
    ["출처 없는 시장·매출 수치 삽입", "높음", "높음", "모든 핵심 통계 [확인 필요] 유지, source-index 전까지 숫자 금지"],
    ["사용자 인터뷰 없이 고객 문제 단정", "높음", "높음", "Gate 1 인터뷰를 MVP 첫 번째 잠금으로 둔다"],
    ["AI 작성기와 차별화 불명확", "중간", "높음", "문장 생성 대신 business-core/evidence-ledger/evaluator를 전면화"],
    ["평가위원 시뮬레이션이 표면 점수 게임화", "중간", "중간", "중대 사실오류·무출처 통계·숫자 불일치를 hard blocker로 둔다"],
    ["문서 유형별 평가 논리 혼합", "중간", "중간", "정부지원/R&D/IR/제안서 변환 규칙을 코어 위에서 분리"],
]


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


def h2(num: str, title: str, icon: str, sub: str, anchor: str | None = None) -> str:
    anchor_attr = f' id="{esc(anchor)}"' if anchor else ''
    return f'<h2{anchor_attr}>{body_icon(icon)}<span class="num">{esc(num)}</span>{esc(title)}</h2><p class="h2-sub">{esc(sub)}</p>'


def toc_section() -> str:
    return f"""
{h2('00', 'Document Map · 목차', 'source', '목차는 요약 섹션 안에 끼워 넣지 않고 독립 섹션으로 분리한다.', 'document-toc')}
<nav class="toc-map" id="document-toc-nav" aria-label="문서 목차"><span class="label">문서 목차</span><p>요약, 결정, 구조, 리스크, 로드맵, 검증, 최종 권고, 출처로 이동합니다.</p><div class="toc-pills"><a class="toc-pill" href="#summary"><b>1</b>Summary</a><a class="toc-pill" href="#decisions"><b>2</b>Decisions</a><a class="toc-pill" href="#architecture"><b>3</b>Core</a><a class="toc-pill" href="#risks"><b>4</b>Risk</a><a class="toc-pill" href="#roadmap"><b>5</b>Roadmap</a><a class="toc-pill" href="#validation"><b>6</b>Gate</a></div></nav>
"""


def table(rows: list[list[str]], caption: str, headers: list[str]) -> str:
    head = "".join(f'<th scope="col">{esc(h)}</th>' for h in headers)
    body = "".join("<tr>" + "".join((f'<th scope="row">{esc(c)}</th>' if i == 0 else f'<td>{c}</td>') for i, c in enumerate(row)) + "</tr>" for row in rows)
    return f'<div class="table-scroll"><table><caption>{esc(caption)}</caption><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def md_html(text: str) -> str:
    out = []
    in_pre = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            out.append("</code></pre>" if in_pre else '<pre class="md-excerpt"><code>')
            in_pre = not in_pre
            continue
        if in_pre:
            out.append(esc(line))
        elif line.startswith("# "):
            out.append(f"<h3>{esc(line[2:])}</h3>")
        elif line.startswith("- "):
            out.append(f"<p>• {esc(line[2:])}</p>")
        elif line.strip():
            out.append(f"<p>{esc(line)}</p>")
    if in_pre:
        out.append("</code></pre>")
    return "\n".join(out)


def source_details(title: str, text: str, open_: bool = False) -> str:
    return (
        f'<details class="source-preserve" style="margin:34px 0 0 24px;border-left:6px solid var(--accent);padding-left:20px"{" open" if open_ else ""}>'
        f'<summary style="padding:20px 24px 20px 34px;display:flex;align-items:center;gap:12px;flex-wrap:wrap"><strong>{esc(title)}</strong><span class="tag">원문 보존</span></summary>'
        f'<div class="source-body" style="padding:0 28px 30px 34px"><div style="border-left:1px solid var(--line);padding:24px 0 2px 24px">{md_html(text)}</div></div>'
        "</details>"
    )


def executive_summary() -> str:
    rows = [
        ["사업명", "GrantProof Core", "[가정] 자유주제 정부지원사업형 사업계획서"],
        ["한 줄 정의", "사업계획서 Claim·수치·출처·가정·평가 질문을 연결하는 증거 원장 SaaS", "[가정]"],
        ["핵심 문제", "문서마다 수치와 출처가 분리되어 평가위원 반론에 취약", "[가정] 인터뷰 필요"],
        ["핵심 해법", "business-core.yaml + source-index.xlsx + evidence-ledger.xlsx + evaluator scorecard", "[사실] bizplan 스킬 구조"],
        ["시장/매출", "검증 전 수치 없음", "[확인 필요] 임의 창작 금지"],
        ["완료 기준", "출처 없는 핵심통계 0건, 숫자 불일치 0건, 4역할 평가 통과", "[사실] bizplan 검증 기준"],
    ]
    return f"""
{h2('01', 'Executive Summary · GrantProof Core 사업계획서', 'summary', 'bizplan 스킬 내용만으로 작성한 자유주제 정부지원사업형 사업계획서 초안이다. HTML은 adaptive-html-final 템플릿만 사용했다.', 'summary')}
<p><strong>GrantProof Core</strong>는 사업계획서 작성자가 주장, 수치, 출처, 가정, 평가위원 질문을 한 곳에서 추적하도록 돕는 <span class="hl">정부지원사업 증거 원장 SaaS</span>다. 이 문서는 외부 시장조사를 하지 않았으므로 시장·매출·고객 수를 만들지 않는다. 대신 bizplan 스킬의 원칙에 따라 모르는 항목을 <span class="tag">[확인 필요]</span>로 남긴다.</p>
{table(rows, '사업계획서 핵심 요약', ['항목', '내용', '증거 태그'])}
<div class="core-insight" style="padding-top:16px;padding-bottom:18px"><h3 style="margin:0 0 8px;line-height:1.34">사업계획서의 상품 정의</h3><p>이 사업의 상품은 문장 자동완성이 아니라 <strong>반론을 견디는 사업 논리</strong>다. 사용자가 입력한 아이디어와 공고문을 바로 미문으로 바꾸지 않고, 인터뷰·리서치·business-core.yaml·원장·평가위원 시뮬레이션을 거쳐 제출 가능한 구조로 만든다.</p></div>
<div class="source-note"><h3>사업계획서 본문 초안 · 문제 인식</h3><p><strong>[가정]</strong> 많은 사업계획서 작성 과정은 공고문, 사용자 인터뷰, 시장 리서치, 특허·논문 근거, 재무 가정, 사업비 산식이 서로 다른 문서에 흩어진 상태로 진행된다. 이때 작성자는 최종 제출 직전에 문장만 다듬지만, 평가자는 문장이 아니라 “이 수치의 출처는 무엇인가”, “이 고객은 실제인가”, “이 성능은 연구 환경인가 제품 환경인가”, “이 예산은 실행계획과 연결되는가”를 묻는다. GrantProof Core는 이 질문에 답하기 위해 만들어지는 도구다.</p><p><strong>[확인 필요]</strong> 실제 고객이 얼마나 자주 이런 문제를 겪는지, 재작업 시간이 얼마인지, 탈락 사유 중 출처·숫자 불일치가 어느 비중인지, 컨설턴트와 내부 작성자의 지불 의사가 어느 수준인지는 아직 검증되지 않았다. 따라서 본 초안은 시장 규모나 매출 수치를 제시하지 않고, Gate 1 인터뷰와 Gate 2 리서치를 첫 실행 항목으로 남긴다.</p><h3>사업계획서 본문 초안 · 해결책</h3><p><strong>[사실]</strong> bizplan 스킬은 모든 문서가 하나의 <code>business-core.yaml</code>에서 파생되어야 한다고 규정한다. 또한 핵심 주장은 <code>source-index.xlsx</code>와 <code>evidence-ledger.xlsx</code>로 역추적되어야 하며, 문서 유형이 바뀌어도 TAM/SAM/SOM, 가격, 고객 수, 매출, 비용, 인력, 일정, 사업비는 일관되어야 한다. GrantProof Core는 이 규칙을 제품의 데이터 모델로 삼는다.</p><p><strong>[목표]</strong> 사용자는 Claim을 입력하면 태그를 선택하고, 출처 행을 연결하고, 어느 섹션에 반영되는지 지정한다. 시스템은 태그 없는 수치, 출처 없는 핵심 통계, 코어와 문서의 숫자 불일치, 미답변 평가자 질문을 제출 전 blocker로 표시한다. 최종 문서는 생성되지만, 생성은 마지막 단계이며 핵심 가치는 검증 과정이다.</p><h3>사업계획서 본문 초안 · 성장 전략</h3><p><strong>[확인 필요]</strong> 초기 고객 세그먼트는 정부지원사업·R&amp;D 과제를 반복 제출하는 스타트업, 연구소, 산학협력단, 사업계획서 컨설턴트로 가정한다. 그러나 구매자와 사용자는 다를 수 있다. 대표가 비용을 지불하고 실무자가 작성하거나, 컨설턴트가 여러 고객 프로젝트를 관리하거나, 기관이 내부 표준 프로세스로 도입할 수 있다. 각 세그먼트는 인터뷰를 통해 문제 강도, 현재 대안, 예산권자, 도입 장벽을 분리해야 한다.</p><p><strong>[가정]</strong> 첫 MVP는 대형 문서 편집기가 아니라 “증거 원장 + business-core.yaml + 평가위원 scorecard”의 최소 흐름으로 충분하다. 문서 출력 품질은 현재 프로젝트의 HTML 템플릿처럼 나중에 붙일 수 있지만, 출처와 가정이 비어 있으면 어떤 템플릿도 사업계획서를 강하게 만들 수 없다.</p></div>
"""


def decision_cards() -> str:
    rows = [
        ["D1", "문서 유형", "정부지원사업형으로 시작", "문제인식·실현가능성·성장전략·팀·정책부합 순서로 변환"],
        ["D2", "포지셔닝", "AI 작성기 아님", "증거 원장 + 코어 컴파일러 + 평가위원 시뮬레이터"],
        ["D3", "수치 정책", "시장/매출 수치 금지", "공식 출처와 인터뷰 전까지 [확인 필요]"],
        ["D4", "MVP 범위", "Claim table → source-index → business-core → scorecard", "공식 서식 매핑은 코어 잠금 후"],
        ["D5", "게이트", "Gate 1 인터뷰를 첫 blocker로 둠", "고객 문제를 AI가 단정하지 않음"],
    ]
    cards = "".join(f'<article class="summary-card"><div class="label">{esc(r[0])}</div><h3>{esc(r[1])}</h3><p><strong>{esc(r[2])}</strong><br>{esc(r[3])}</p></article>' for r in rows)
    return f"""
{h2('02', 'Decision Cards · 사업 논리를 잠그는 5개 결정', 'decision', '사업계획서의 전제와 미검증 항목을 분리해 다음 실행의 기준으로 삼는다.', 'decisions')}
<div class="card-grid rail-cycle">{cards}</div>
{table(rows, '초기 사업 의사결정 기록', ['ID', '결정 영역', '결정', '근거/제약'])}
"""


def architecture() -> str:
    rows = [
        ["입력", "공고문·아이디어·인터뷰 답변·회사자료", "Gate 0/1 산출물"],
        ["조사", "시장·경쟁·기술·특허·논문 자료", "source-index.xlsx"],
        ["코어", "문제·해결·제품·시장·사업모델·팀·예산", "business-core.yaml"],
        ["원장", "Claim·태그·출처·반영섹션·counter evidence", "evidence-ledger.xlsx"],
        ["출력", "정부지원서·R&D 계획서·IR 덱·제안서·HTML", "문서 유형별 변환"],
        ["검증", "admin·tech·biz·skeptic 평가", "scorecard/revision-log"],
    ]
    flow = """
<div class="connection"><div class="connection-row"><span>Gate 0/1</span><strong>공고·인터뷰</strong><em>사용자 사실과 제약</em></div><div class="connection-row"><span>Gate 2</span><strong>리서치</strong><em>source-index 구축</em></div><div class="connection-row"><span>Gate 3/4</span><strong>business-core.yaml</strong><em>논리·숫자 단일 출처</em></div><div class="connection-row"><span>Gate 6/7</span><strong>문서 출력·평가</strong><em>반론 통과 후 제출</em></div></div>
"""
    return f"""
{h2('03', 'Architecture · business-core.yaml 중심 운영 구조', 'architecture', '하나의 코어에서 여러 문서가 파생되고, 모든 주장은 원장으로 역추적된다.', 'architecture')}
{flow}
{table(rows, 'GrantProof Core 시스템 구조', ['계층', '역할', 'bizplan 원천'])}
{source_details('business-core.yaml 초안', '```yaml\n' + BUSINESS_CORE + '\n```', open_=False)}
"""


def risk_matrix() -> str:
    vt = """
<section class="vt-shell" aria-label="사업 리스크 매트릭스">
  <div class="vt-frame">
    <div class="rm-grid"><div class="rm-cell rm-head">가능성</div><div class="rm-cell rm-head">낮음</div><div class="rm-cell rm-head">중간</div><div class="rm-cell rm-head">높음</div><div class="rm-cell rm-head">영향 큼</div><div class="rm-cell rm-risk med">문서 유형 혼합</div><div class="rm-cell rm-risk high">시장 수치 창작</div><div class="rm-cell rm-risk high">인터뷰 생략</div><div class="rm-cell rm-head">영향 중간</div><div class="rm-cell rm-risk low">서식 지연</div><div class="rm-cell rm-risk med">평가 게임화</div><div class="rm-cell rm-risk med">출처 입력 이탈</div><div class="rm-cell rm-head">영향 작음</div><div class="rm-cell rm-risk low">용어 불일치</div><div class="rm-cell rm-risk low">태그 누락</div><div class="rm-cell rm-risk low">디자인 편차</div></div>
  </div>
</section>
"""
    return f"""
{h2('04', 'Risk Matrix · 허위 완성보다 정직한 미완을 선택', 'risk', 'bizplan의 7대 절대 규칙을 사업 리스크 관리 체계로 전환했다.', 'risks')}
{vt}
{table(RISKS, '핵심 리스크와 완화책', ['리스크', '가능성', '영향', '완화책'])}
"""


def roadmap() -> str:
    wg = """
<section class="wg-16" aria-labelledby="wg-16-title"><header class="wg-16-head"><p class="wg-16-kicker">Implementation Plan · Skill-only Business Plan</p><h2 id="wg-16-title" class="wg-16-h">90일 지원사업 제출 준비 로드맵</h2><p class="wg-16-lead">공식 지원서 작성보다 먼저 증거 태그·코어·평가 게이트를 검증합니다.</p></header><div class="wg-16-panel"><h3 class="wg-16-h3">마일스톤 타임라인</h3><ol class="wg-16-ms"><li class="wg-16-ms-item wg-16-active"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">M1 · 지원사업 공고·문제 검증</span><span class="wg-16-badge wg-16-bd-active">0~30일</span></div><p class="wg-16-ms-desc">공고 배점·지원 자격·서식 제약을 확보하고, 고객 문제 인터뷰는 [확인 필요]로 둡니다.</p></div></li><li class="wg-16-ms-item"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">M2 · Evidence Ledger 제출 원장</span><span class="wg-16-badge">31~60일</span></div><p class="wg-16-ms-desc">Claim table, source-index, evidence tag, number-registry를 연결합니다.</p></div></li><li class="wg-16-ms-item"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">M3 · 제출본 변환·평가위원 시뮬레이션</span><span class="wg-16-badge">61~90일</span></div><p class="wg-16-ms-desc">정부지원/R&D/IR/제안서 템플릿 변환과 4역할 scorecard를 만든다.</p></div></li></ol><h3 class="wg-16-h3">데이터 플로우</h3><div class="wg-16-flow" aria-label="GrantProof Core 데이터 플로우"><div class="wg-16-fnode">Interview<span class="wg-16-fnode-s">CF/assumption</span></div><div class="wg-16-fnode">Research<span class="wg-16-fnode-s">source-index</span></div><div class="wg-16-fnode wg-16-fnode-good">Core<span class="wg-16-fnode-s">business-core.yaml</span></div><div class="wg-16-fnode wg-16-fnode-hot">Ledger<span class="wg-16-fnode-s">claim/evidence</span></div><div class="wg-16-fnode wg-16-fnode-q">Scorecard<span class="wg-16-fnode-s">4 evaluators</span></div></div><h3 class="wg-16-h3">리스크 평가</h3><div class="wg-16-table-wrap"><div class="table-scroll"><table class="wg-16-table"><caption>로드맵 리스크 — 가능성·영향·완화책</caption><thead><tr><th scope="col">리스크</th><th scope="col">가능성</th><th scope="col">영향</th><th scope="col">완화책</th></tr></thead><tbody><tr><th scope="row">인터뷰 응답 부족</th><td><span class="wg-16-lv wg-16-lv-mid">중</span></td><td><span class="wg-16-lv wg-16-lv-hi">높음</span></td><td>세그먼트별 질문 카드와 follow-up-items 자동화</td></tr><tr><th scope="row">원장 입력 피로</th><td><span class="wg-16-lv wg-16-lv-hi">높음</span></td><td><span class="wg-16-lv wg-16-lv-mid">중</span></td><td>source-index 자동 초안 + 사용자 승인</td></tr><tr><th scope="row">문서 출력 품질 과신</th><td><span class="wg-16-lv wg-16-lv-mid">중</span></td><td><span class="wg-16-lv wg-16-lv-hi">높음</span></td><td>scorecard 85점, 무출처 통계 0건 전까지 제출 금지</td></tr></tbody></table></div></div></div></section>
"""
    return f"""
{h2('05', 'Priority Roadmap · 문서보다 원장부터 만든다', 'roadmap', '90일 안에 검증해야 할 MVP 순서를 bizplan 게이트에 맞춰 배치했다.', 'roadmap')}
{wg}
"""


def validation_checklist() -> str:
    rows = [
        ["Gate 0", "공고/첨부 확보", "[확인 필요] 자유주제라 공고 없음. 실제 지원사업 선택 시 재실행"],
        ["Gate 1", "심층 인터뷰", "[확인 필요] 고객·구매자·문제 빈도·현재 대안 확인 필요"],
        ["Gate 2", "리서치", "[확인 필요] 시장·경쟁·기술·특허·논문 조사 전"],
        ["Gate 3", "사업 논리", "[가정] 문제→해결→코어→원장→출력 사슬은 성립"],
        ["Gate 4", "숫자 일관성", "[확인 필요] 숫자를 만들지 않았으므로 불일치는 없지만 모델도 없음"],
        ["Gate 7", "평가위원 시뮬레이션", "[목표] admin/tech/biz/skeptic scorecard로 반복"],
    ]
    ledger = [[x[0], x[1], x[2], x[3], x[4]] for x in EVIDENCE_LEDGER]
    return f"""
{h2('06', 'Validation Checklist · 완료가 아니라 제출 전 미완 목록', 'check', 'bizplan 기준으로 이 사업계획서가 어디까지 사실이고 어디부터 검증 전인지 분리했다.', 'validation')}
{table(rows, '게이트별 현재 판정', ['Gate', '검사', '현재 상태'])}
{table(ledger, 'Evidence Ledger 초안', ['ID', 'Claim', '태그', '근거', '반영 위치'])}
<div class="accessibility-checklist"><h3>제출 금지 조건</h3><ul><li>시장 규모·매출·고객 수를 출처 없이 숫자로 제시하면 실패.</li><li>실제 고객·계약·LOI를 만들면 실패.</li><li>business-core.yaml과 파생 문서의 숫자가 갈라지면 실패.</li><li>평가위원 4역할 중 하나라도 중대 사실오류를 잡으면 실패.</li></ul></div>
"""


def final_recommendation() -> str:
    return f"""
<h2>{body_icon('final')}Final Recommendation · 지금은 '투자 유치'가 아니라 '검증 MVP' 단계</h2>
<p>GrantProof Core는 바로 매출 예측을 제시할 단계가 아니다. bizplan 스킬 기준으로는 <strong>Gate 1 고객 인터뷰</strong>와 <strong>Gate 2 리서치</strong>가 비어 있으므로, 완성 사업계획서가 아니라 <strong>사업 논리 설계 초안</strong>이다.</p>
<p>다음 작업은 단순한 문서 예쁘게 만들기가 아니다. 실제 공고문, 고객 인터뷰, source-index, evidence-ledger, market-sizing, financial-model을 채운 뒤 다시 HTML/DOCX/PPTX를 파생해야 한다.</p>
"""


def source_note() -> str:
    links = "".join(f'<li><a href="{esc(s["url"])}" target="_blank" rel="noopener noreferrer">{esc(s["name"])}</a> — {esc(s["role"])}</li>' for s in LOCAL_SOURCES)
    return f"""
{h2('07', 'Source Note · 콘텐츠 원천은 bizplan 스킬만 사용', 'source', 'adaptive-html-final은 HTML 골격·CSS·검증만 제공했고, 사업계획 내용은 bizplan 원칙에서 파생했다.')}
<p>보조 파일: <a href="sources/business-core.yaml">business-core.yaml</a> · <a href="sources/evidence-ledger.json">evidence-ledger.json</a> · <a href="sources/source-list.json">source-list.json</a> · <a href="sources/bizplan-application.json">bizplan-application.json</a></p><ol class="refs">{links}</ol>
"""


def copy_sources() -> dict:
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
    ]
    for src, name in copy_map:
        shutil.copyfile(src, SOURCES / name)
    (SOURCES / "business-core.yaml").write_text(BUSINESS_CORE + "\n", encoding="utf-8")
    (SOURCES / "evidence-ledger.json").write_text(json.dumps(EVIDENCE_LEDGER, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (SOURCES / "source-list.json").write_text(json.dumps(LOCAL_SOURCES, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (SOURCES / "bizplan-application.json").write_text(json.dumps({
        "skill": "bizplan",
        "content_source_rule": "business-plan content uses only local orginal_skill/bizplan files; no STORM and no external market data",
        "html_template_rule": "adaptive-html-final v5.10.5 used only for base/layout/css/widget/validation",
        "selected_topic": "GrantProof Core — 정부지원사업 증거 원장 SaaS",
        "document_type": "정부 창업/중소기업 지원사업형 사업계획서",
        "mode": MODE,
        "profile": PROFILE,
        "disclaimer": "사용자 인터뷰와 외부 시장조사 전이므로 실제 제출용 최종본이 아니라 스킬 기반 사업 논리 초안이다.",
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    shutil.copyfile(SKILL / "manifest.json", SOURCES / "adaptive-html-final-manifest.json")
    (SOURCES / "profile.json").write_text(json.dumps({"profile": PROFILE}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    placeholder_map = {
        "layout": LAYOUT,
        "EXECUTIVE_SUMMARY": "business plan summary + tagged assumptions",
        "DECISION_CARDS": "5 decision cards for positioning and gates",
        "ARCHITECTURE": "business-core.yaml and evidence-ledger architecture",
        "RISK_MATRIX": "vt risk-matrix + risk table",
        "PRIORITY_ROADMAP": "wg-16 90-day MVP roadmap",
        "VALIDATION_CHECKLIST": "bizplan gate status + evidence ledger",
        "FINAL_RECOMMENDATION": "honest incomplete recommendation",
        "SOURCE_NOTE": "bizplan-only source hub",
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
        "skills/adaptive-html-final/assets/layouts/expert-report.html",
        "skills/adaptive-html-final/assets/visual-html-templates/03-risk-matrix.html",
        "skills/adaptive-html-final/assets/widget-templates/16-implementation-plan.html",
        "orginal_skill/bizplan/SKILL.md",
        "orginal_skill/bizplan/references/evidence-tagging.md",
        "orginal_skill/bizplan/references/04-research-engine.md",
        "orginal_skill/bizplan/references/07-business-core.md",
        "orginal_skill/bizplan/references/11-document-types.md",
        "orginal_skill/bizplan/references/12-verification.md",
        "orginal_skill/bizplan/references/document-output.md",
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
        "input_snapshots": ["sources/business-core.yaml", "sources/evidence-ledger.json", "sources/bizplan-application.json"],
        "research_route": "No web/STORM; business-plan content derived only from local bizplan skill files",
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


def render(integrity: dict) -> str:
    layout = read(ASSETS / "layouts" / LAYOUT)
    meta = f"<span>{MODE}</span><span>{LAYOUT}</span><span>profile {PROFILE}</span><span>adaptive-html-final v{version()}</span><span>content: bizplan only</span>"
    repl = {
        "{{KICKER}}": '<span class="kicker-text">bizplan skill-only business plan</span>',
        "{{TITLE}}": "GrantProof Core 사업계획서",
        "{{SUBTITLE}}": "정부지원사업 신청서의 주장·수치·출처·가정·평가 질문을 하나의 business-core.yaml로 추적하는 증거 원장 SaaS 초안",
        "{{META}}": meta,
        "{{EXECUTIVE_SUMMARY}}": executive_summary(),
        "{{DECISION_CARDS}}": decision_cards(),
        "{{ARCHITECTURE}}": architecture(),
        "{{RISK_MATRIX}}": risk_matrix(),
        "{{PRIORITY_ROADMAP}}": roadmap(),
        "{{VALIDATION_CHECKLIST}}": validation_checklist(),
        "{{FINAL_RECOMMENDATION}}": final_recommendation(),
        "{{SOURCE_NOTE}}": source_note(),
    }
    body = layout
    for k, v in repl.items():
        body = body.replace(k, v)
    body = body.replace(
        '<section class="executive-summary">',
        f'<section class="document-toc-section">{toc_section()}</section>\n  <section class="executive-summary">',
        1,
    )
    body = body.replace(
        "</div></header>",
        "</div><div class=\"generated-row\"><p class=\"generated-date\">생성 기준: 2026-06-20 KST · bizplan content-only · adaptive-html-final template-only · expert_html · layout-first</p><div class=\"lens-strip\" aria-label=\"적용 렌즈\"><span class=\"lens-strip-label\">LENS</span><span class=\"lens-chip\">Business Core</span><span class=\"lens-chip\">Evidence Tag</span><span class=\"lens-chip\">Source Ledger</span><span class=\"lens-chip\">Evaluator Gate</span><span class=\"lens-chip\">Honest Incomplete</span></div></div></header>",
        1,
    )
    title = f"GrantProof Core 사업계획서 · bizplan skill-only · adaptive-html-final v{version()}"
    description = "bizplan 스킬 내용만으로 만든 자유주제 정부지원사업형 사업계획서 HTML. adaptive-html-final은 템플릿과 검증에만 사용."
    json_ld = json.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": description,
        "inLanguage": "ko",
        "datePublished": "2026-06-20",
        "author": {"@type": "Organization", "name": "adaptive-html-final"},
        "keywords": ["bizplan", "사업계획서", "business-core.yaml", "evidence-ledger", "source-index", "평가위원 시뮬레이션"],
    }, ensure_ascii=False)
    doc = read(ASSETS / "base.html")
    slots = {
        "{{TITLE}}": title,
        "{{DESCRIPTION}}": description,
        "{{JSON_LD_BLOCK}}": f'<script type="application/ld+json">{json_ld}</script>',
        "{{BODY}}": body,
        "{{FOOTER}}": "",
    }
    slots.update(css_slots(integrity))
    for k, v in slots.items():
        doc = doc.replace(k, v)
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
        "GrantProof Core",
        "bizplan",
        "business-core.yaml",
        "source-index.xlsx",
        "evidence-ledger.xlsx",
        "[사실]",
        "[가정]",
        "[확인 필요]",
        "평가위원",
        "Gate 1",
        "Source Note",
    ]
    missing = [m for m in required if m not in visible]
    evidence = {
        "source_rule": "bizplan content only; adaptive-html-final template only",
        "source_count": len(LOCAL_SOURCES),
        "required_markers_missing": missing,
        "output_visible_text_chars": len(visible),
        "pass": not missing and len(visible) > 8000,
    }
    (SOURCES / "content-preservation.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not evidence["pass"]:
        raise RuntimeError(str(evidence))


def main() -> None:
    integrity = copy_sources()
    doc = render(integrity)
    (OUT / "index.html").write_text(doc, encoding="utf-8")
    content_evidence(doc)
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
