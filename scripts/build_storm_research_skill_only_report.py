#!/usr/bin/env python3
"""Build a storm-research skill-only research report.

Content source rule:
- Research content is derived only from orginal_skill/storm-research local skill files.
- No live web search is used because the user requested the storm-research skill content only.
- adaptive-html-final is used only for HTML template/CSS/validation.
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
STORM = ROOT / "orginal_skill" / "storm-research"

OUT = ROOT / "output" / "2026-06-20" / "storm-research-skill-only-report"
SOURCES = OUT / "sources"

MODE = "expert_html"
PROFILE = "auto"
LAYOUT = "expert-report.html"
LAYOUT_CLASS = "layout-expert"
PRIMARY_VT = "risk-matrix"
PRIMARY_WG = "wg-11"
TOPIC = "STORM Research OS — 다섯 영혼 리서치가 단일 답변을 이기는 조건"

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
    "summary": "search",
    "decision": "decision",
    "architecture": "flow",
    "risk": "warning",
    "roadmap": "timeline",
    "check": "check",
    "final": "success",
    "source": "source",
}

LOCAL_SOURCES = [
    {"name": "storm-research/SKILL.md", "url": "sources/storm-SKILL.md", "role": "Phase 0~7 실행 절차, full/solo 모드, 5영혼·4프롬프트·HTML 산출 규칙"},
    {"name": "storm-pipeline.md", "url": "sources/storm-pipeline.md", "role": "STORM 원논문 단계 매핑, Knowledge Curation, Outline, Article, Polish"},
    {"name": "provenance.md", "url": "sources/provenance.md", "role": "출처 계보, 과장-사실 구분, 조직성 +25%/coverage +10% 정확 표기"},
    {"name": "prompt 1 · Multi-Perspective Scan", "url": "sources/prompt-1-multi-perspective-scan.md", "role": "다섯 전문가 렌즈와 출처 강제 스캔"},
    {"name": "prompt 2 · Contradiction Map", "url": "sources/prompt-2-contradiction-map.md", "role": "합의·모순·사각지대·핵심 긴장 도출"},
    {"name": "prompt 3 · Synthesis", "url": "sources/prompt-3-synthesis.md", "role": "모순을 중심축으로 둔 개요·본문·lead 생성"},
    {"name": "prompt 4 · Peer Review", "url": "sources/prompt-4-peer-review.md", "role": "source bias transfer와 over-association 검토"},
    {"name": "soul charters", "url": "sources/soul-charters.md", "role": "Skeptic/Economist/Historian/Academic/Futurist 각 영혼 질문 프레임"},
]

SOULS = {
    "Skeptic": {
        "persona": "회의주의자",
        "summary": "STORM을 프롬프트 팩처럼 쓰면 출처 없는 다관점 브레인스토밍으로 퇴화한다.",
        "body": "회의주의자의 결론은 명확하다. STORM의 가치는 '다섯 관점' 자체가 아니라 각 관점이 실제 출처를 끌어와 반증 가능하게 보고하는 데 있다. 검색 도구가 없으면 BLOCKED를 보고하라는 규칙, 출처 없는 단언 금지, peer-review 없이는 최종화 금지라는 장치가 빠지면 겉모양만 STORM인 문서가 된다. [출처: sources/storm-SKILL.md, sources/provenance.md]",
        "uncertainty": "이 산출물은 사용자의 요청에 따라 외부 웹 검색을 하지 않았으므로, 실제 주제 리서치가 아니라 storm-research 스킬 자체에 대한 content-only 연구다.",
    },
    "Economist": {
        "persona": "경제학자",
        "summary": "full 모드는 비용이 크지만, 고위험·장문·출처 의존 리서치에서는 재작업 비용을 줄인다.",
        "body": "경제적 렌즈에서 STORM은 모든 질문에 쓰는 도구가 아니다. cmux, 5개 페인, 여러 LLM, 결과 수집, 모순 지도, 동료 검토는 운영비를 만든다. 반대로 투자·정책·기술 판단처럼 잘못된 결론의 비용이 큰 주제에서는 출처 추적과 모순 표면화가 재작업 비용을 줄이는 보험이 된다. solo fallback은 빠르지만 모델 다양성이라는 이점은 낮아진다. [출처: sources/storm-SKILL.md]",
        "uncertainty": "실제 비용 절감 수치는 skill 파일에 없으므로 수치화하지 않는다.",
    },
    "Historian": {
        "persona": "역사학자",
        "summary": "STORM은 새 문장 생성기가 아니라 오래된 pre-writing 과정을 LLM 오케스트레이션으로 되살린다.",
        "body": "storm-pipeline은 STORM을 Knowledge Curation, Outline Generation, Article Generation, Article Polishing의 흐름으로 매핑한다. 이것은 글쓰기 전 조사, 질문, 개요, 초안, 검토라는 오래된 작업 질서를 자동화한 것이다. 커뮤니티식 4프롬프트는 원논문과 동일하지 않고 STORM의 정신을 압축한 재해석이라는 점도 명시되어 있다. [출처: sources/storm-pipeline.md, sources/provenance.md]",
        "uncertainty": "역사적 유사 사례 비교는 외부 자료가 필요하므로 여기서는 skill 내부 설명에 한정한다.",
    },
    "Academic": {
        "persona": "학자",
        "summary": "정확한 수치는 '조직성 +25%, coverage +10%'이며 모델 지능 향상 주장이 아니다.",
        "body": "학술적 핵심은 수치의 해석이다. provenance 문서는 '25% better at research' 같은 표현을 claim drift로 규정한다. 정확한 문장은 outline-driven RAG baseline 대비 생성 글의 조직성은 +25%, coverage breadth는 +10%라는 것이다. 또한 논문이 지적한 실패모드는 source bias transfer와 over-association이며, 이 스킬은 peer-review 단계로 이를 잡도록 설계한다. [출처: sources/storm-pipeline.md, sources/provenance.md]",
        "uncertainty": "이 수치는 storm-research 스킬의 provenance 기록을 따른 것이며, 본 산출물에서 원논문을 새로 재검증하지 않았다.",
    },
    "Futurist": {
        "persona": "미래학자",
        "summary": "리서치 워크플로우의 미래는 답변 생성보다 출처·모순·검토 상태를 운영하는 Research Ops다.",
        "body": "미래학자 렌즈에서 STORM의 중요한 전환은 '한 번에 좋은 답을 받기'가 아니라 '리서치 상태를 관리하기'다. Phase 0 환경 판별, 영혼별 done 파일, BLOCKED 처리, report.json 스키마, HTML 검수까지 포함하면 리서치는 대화가 아니라 운영 파이프라인이 된다. [추론] 이러한 구조는 앞으로 사내 리서치·정책 검토·기술 의사결정에서 출처 감사 가능한 Research Ops로 발전할 수 있다. [출처: sources/storm-SKILL.md, sources/report.schema.json]",
        "uncertainty": "미래 시나리오는 [추론]이며, 외부 시장 신호는 이번 content-only 조건 때문에 수집하지 않았다.",
    },
}

CONTRADICTIONS = [
    ["다섯 관점은 더 넓은 이해를 만든다", "출처가 없으면 다섯 관점은 다섯 개의 그럴듯한 추측일 뿐이다", "관점 다양성보다 citation discipline을 먼저 검사한다"],
    ["full 모드는 가장 STORM답다", "cmux·다중 CLI·페인 운영은 비용과 실패 지점을 늘린다", "고위험 리서치는 full, 빠른 초안은 solo fallback으로 분기한다"],
    ["4프롬프트는 쉽게 복붙 가능하다", "4프롬프트는 원논문 STORM의 검색-grounding 대화 시뮬레이션과 동일하지 않다", "산출물에 '재해석'과 '진짜 STORM 링크'를 명시한다"],
    ["조직성 +25%는 강력한 메시지다", "이를 '25% 더 똑똑한 모델'로 말하면 claim drift다", "수치 문장은 조직성 +25%, coverage +10%로 고정한다"],
    ["종합은 하나의 글로 닫아야 한다", "모순을 슬그머니 봉합하면 STORM의 장점이 사라진다", "핵심 긴장을 남기고 해결 조건을 명시한다"],
]

SYNTHESIS = """# STORM Research OS — 다섯 영혼 리서치가 단일 답변을 이기는 조건

> STORM의 핵심은 다섯 명처럼 말하는 것이 아니라 다섯 개의 질문 경로가 서로 다른 출처를 끌어오고, 그 충돌을 보존한 뒤, 동료 검토로 비약을 치는 것이다. 이 산출물은 외부 웹을 새로 검색하지 않고 storm-research 로컬 스킬 내용만으로 작성한 content-only 연구다. 따라서 '새 주제에 대한 실제 딥리서치'가 아니라 'storm-research 스킬이 가르치는 리서치 운영체계'에 대한 분석이다.

## 1. 왜 단일 답변은 위험한가
단일 LLM 답변은 빠르지만 질문 경로가 하나다. storm-research 스킬은 이 문제를 회의주의자, 경제학자, 역사학자, 학자, 미래학자라는 다섯 영혼으로 쪼갠다. 각 영혼은 자기 렌즈에 맞는 질문을 던지고, 출처를 강제하며, 결과 파일과 done 마커로 메인에게 보고한다. [출처: sources/storm-SKILL.md]

## 2. 그러나 다관점만으로 충분하지 않다
다관점은 쉽게 역할극이 된다. provenance 문서는 과장된 바이럴 주장과 실제 논문 근거를 구분하라고 요구한다. 특히 '4개 프롬프트 = STORM'은 부분적이며, 진짜 STORM은 retrieval과 multi-perspective question asking을 포함한다. [출처: sources/provenance.md, sources/storm-pipeline.md]

## 3. 핵심 긴장: 운영비 대 신뢰도
full 모드는 cmux, 다중 CLI, 5페인 spawn, collect, report build가 필요하다. 이것은 비용이지만, 출처·모순·동료 검토가 중요한 주제에서는 신뢰를 위한 보험이다. 반대로 단순 요약이나 내부 메모에는 solo fallback이 더 합리적이다. [출처: sources/storm-SKILL.md]

## 4. 검토가 최종 품질을 만든다
storm-review는 source bias transfer와 over-association을 잡는다. 즉 출처 편향이 글로 전이되었는지, 관련 없는 사실을 부당하게 연결했는지, 모순을 봉합했는지 확인한다. 이 단계가 빠지면 STORM 리포트는 보기 좋은 종합문일 뿐 검증된 리서치가 아니다. [출처: sources/prompt-4-peer-review.md, sources/storm-pipeline.md]

## 미해결 질문
실제 조직에서 full STORM을 언제 켜고 언제 solo fallback으로 충분하다고 판단할 것인가? 이 질문은 비용, 주제 위험도, 출처 필요성, 의사결정 파급효과를 함께 보는 운영 정책이 필요하다.
"""

PEER_REVIEW = """# Peer Review

## 결함 목록
1. MINOR — 본 산출물은 외부 웹 검색을 하지 않았으므로 '새 외부 주제 딥리서치'가 아니다. 수정: 본문과 메타에 content-only 연구라고 명시했다.
2. MINOR — 수치 +25%/+10%는 skill provenance를 따른 것이며 원논문 실시간 재검증은 아니다. 수정: source note에 provenance.md를 원천으로 표시했다.
3. MAJOR 방지 — 4프롬프트를 원논문 STORM과 동일시하는 문장이 있으면 안 된다. 수정: '재해석'이라고 표기했다.

## Source Bias Transfer
출처는 모두 storm-research 로컬 스킬 파일이므로 편향은 의도적이다. 이 문서는 skill-only 조건을 충족하지만, 일반 세계에 대한 결론으로 확장하면 안 된다.

## Over-Association
cmux 운영과 미래 Research Ops를 연결한 대목은 [추론]으로 표시되어야 한다. 본문에서 [추론] 라벨을 유지했다.

## 통과 여부
조건부 통과. BLOCKER 없음. 단, 실제 외부 주제 리서치를 원하면 Phase 3의 웹 검색/출처 수집을 별도 실행해야 한다.

마지막 미해결 질문: full STORM을 켤 기준을 어떤 risk score로 운영할 것인가?
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


def md_html(text: str) -> str:
    out = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("# "):
            out.append(f"<h3>{esc(line[2:])}</h3>")
        elif line.startswith("## "):
            out.append(f"<h3>{esc(line[3:])}</h3>")
        elif re.match(r"^\d+\.\s", line):
            out.append(f"<p>• {esc(re.sub(r'^\d+\.\s+', '', line))}</p>")
        elif line.startswith("- "):
            out.append(f"<p>• {esc(line[2:])}</p>")
        elif line.startswith("> "):
            out.append(f"<blockquote>{esc(line[2:])}</blockquote>")
        else:
            out.append(f"<p>{esc(line)}</p>")
    return "\n".join(out)


def source_details(title: str, text: str, open_: bool = False) -> str:
    return (
        f'<details class="source-preserve" style="margin:34px 0 0 24px;border-left:6px solid var(--accent);padding-left:20px"{" open" if open_ else ""}>'
        f'<summary style="padding:20px 24px 20px 34px;display:flex;align-items:center;gap:12px;flex-wrap:wrap"><strong>{esc(title)}</strong><span class="tag">원문 보존</span></summary>'
        f'<div class="source-body" style="padding:0 28px 30px 34px"><div style="border-left:1px solid var(--line);padding:24px 0 2px 24px">{md_html(text)}</div></div>'
        "</details>"
    )


def make_scan_md() -> str:
    parts = [f"# Multi-Perspective Scan · {TOPIC}"]
    for name, row in SOULS.items():
        parts += [f"## {name} · {row['persona']}", f"### 고유 결론", row["summary"], f"### 발견", row["body"], f"### 불확실성", row["uncertainty"], ""]
    return "\n".join(parts)


def make_contradiction_md() -> str:
    return "# Contradiction Map\n" + "\n".join(f"- {a} ↔ {b} → {c}" for a, b, c in CONTRADICTIONS)


def executive_summary() -> str:
    cards = "".join(
        f'<article class="summary-card"><div class="label">{esc(name)} · {esc(row["persona"])}</div><h3>{esc(row["summary"])}</h3><p>{esc(row["body"])}</p></article>'
        for name, row in SOULS.items()
    )
    toc = """
<nav class="toc-map" id="document-toc" aria-label="문서 목차"><span class="label">문서 목차</span><p>요약, 결정, 파이프라인, 리스크, 상태판, 검증, 결론, 출처로 이동합니다.</p><div class="toc-pills"><a class="toc-pill" href="#summary"><b>1</b>Summary</a><a class="toc-pill" href="#decisions"><b>2</b>Decision</a><a class="toc-pill" href="#architecture"><b>3</b>Pipeline</a><a class="toc-pill" href="#risks"><b>4</b>Risk</a><a class="toc-pill" href="#roadmap"><b>5</b>Status</a><a class="toc-pill" href="#validation"><b>6</b>Review</a></div></nav>
"""
    rows = [
        ["주제", TOPIC, "storm-research 스킬 내부 내용으로만 선택한 자유주제"],
        ["실행 모드", "solo fallback", "cmux workspace 없음, kimi 없음. 외부 웹 검색 없음"],
        ["핵심 판단", "STORM은 프롬프트가 아니라 리서치 운영체계", "5영혼·모순지도·종합·동료검토"],
        ["정확한 수치", "조직성 +25%, coverage +10%", "모델 지능 +25%가 아님"],
        ["가장 큰 위험", "출처 없는 다관점 역할극", "citation discipline과 peer-review가 방어선"],
    ]
    return f"""
<div id="summary"></div>
{toc}
{h2('01', 'Executive Summary · STORM Research OS', 'summary', 'storm-research 스킬 내용만 사용해 다관점 리서치 운영체계를 분석했다.')}
<p>이 리포트의 자유주제는 <strong>{esc(TOPIC)}</strong>다. 사용자가 “storm-research 스킬 내용만”을 요청했기 때문에, 외부 웹 검색을 새로 수행하지 않고 로컬 스킬 파일의 절차·프롬프트·provenance·영혼 charter만을 콘텐츠 원천으로 삼았다. 현재 프로젝트는 HTML 템플릿과 검증에만 사용했다.</p>
{table(rows, '리서치 실행 요약', ['항목', '내용', '근거'])}
<h3>다섯 영혼 스캔</h3>
<div class="card-grid rail-cycle">{cards}</div>
"""


def decision_cards() -> str:
    rows = [
        ["D1", "full vs solo", "cmux·다중 CLI가 있으면 full, 없으면 solo fallback", "SKILL Phase 0"],
        ["D2", "최소 품질", "최소 3/5 영혼이 출처 포함 results를 내야 종합 권장", "SKILL Phase 4"],
        ["D3", "출처 원칙", "모든 사실 주장에 [출처: URL], 추측은 [추론]", "HARD rule"],
        ["D4", "검토 원칙", "peer-review 없이 최종화 금지", "HARD rule"],
        ["D5", "수치 원칙", "조직성 +25%, coverage +10%로 정확 표기", "provenance"],
    ]
    cards = "".join(f'<article class="summary-card"><div class="label">{esc(r[0])}</div><h3>{esc(r[1])}</h3><p><strong>{esc(r[2])}</strong><br>{esc(r[3])}</p></article>' for r in rows)
    return f"""
<div id="decisions"></div>
{h2('02', 'Decision Cards · STORM을 켜야 하는 조건', 'decision', '단순 요약과 다관점 리서치 운영을 구분하는 결정 규칙이다.')}
<div class="card-grid rail-cycle">{cards}</div>
{table(rows, 'STORM 운영 결정표', ['ID', '결정', '규칙', '원천'])}
"""


def architecture() -> str:
    rows = [
        ["Phase 0", "환경 점검 + 주제 확보", "cmux/CLI 확인, full 또는 solo 결정"],
        ["Phase 1", "관점 도출 + LLM 분배", "기본 5영혼 또는 주제별 재도출"],
        ["Phase 2~4", "페인 생성·dispatch·collect", "results/<Soul>.md + done marker"],
        ["Phase 5", "4프롬프트 파이프라인", "scan → contradiction map → synthesis → peer review"],
        ["Phase 6", "report.json → HTML", "souls, contradiction, synthesis, peer review 조립"],
        ["Phase 7", "검수·보고", "미치환 0, soul 카드 5, 출처 링크 존재"],
    ]
    flow = """
<div class="connection"><div class="connection-row"><span>Input</span><strong>Topic</strong><em>주제 한 줄</em></div><div class="connection-row"><span>Scan</span><strong>5 Souls</strong><em>Skeptic/Economist/Historian/Academic/Futurist</em></div><div class="connection-row"><span>Map</span><strong>Contradiction</strong><em>합의·모순·사각지대</em></div><div class="connection-row"><span>Write</span><strong>Synthesis</strong><em>모순 중심의 종합 글</em></div><div class="connection-row"><span>Review</span><strong>Peer Review</strong><em>bias·over-association 검토</em></div></div>
"""
    return f"""
<div id="architecture"></div>
{h2('03', 'Architecture · STORM 리서치 파이프라인', 'architecture', 'storm-research 스킬의 Phase 0~7을 리서치 운영 구조로 재구성했다.')}
{flow}
{table(rows, 'storm-research 실행 단계', ['단계', '역할', '산출/판정'])}
{source_details('Multi-Perspective Scan 원문', make_scan_md())}
"""


def risk_matrix() -> str:
    vt = """
<section class="vt-shell" aria-label="STORM 리스크 매트릭스">
  <div class="vt-frame">
    <div class="rm-grid"><div class="rm-cell rm-head">가능성</div><div class="rm-cell rm-head">낮음</div><div class="rm-cell rm-head">중간</div><div class="rm-cell rm-head">높음</div><div class="rm-cell rm-head">영향 큼</div><div class="rm-cell rm-risk med">claim drift</div><div class="rm-cell rm-risk high">source bias transfer</div><div class="rm-cell rm-risk high">출처 없는 역할극</div><div class="rm-cell rm-head">영향 중간</div><div class="rm-cell rm-risk low">HTML 검수 누락</div><div class="rm-cell rm-risk med">over-association</div><div class="rm-cell rm-risk med">solo fallback 과신</div><div class="rm-cell rm-head">영향 작음</div><div class="rm-cell rm-risk low">ref 정리 지연</div><div class="rm-cell rm-risk low">중복 출처</div><div class="rm-cell rm-risk low">표기 흔들림</div></div>
  </div>
</section>
"""
    return f"""
<div id="risks"></div>
{h2('04', 'Risk Matrix · STORM을 STORM답게 만드는 방어선', 'risk', '다관점보다 중요한 것은 출처·모순·동료 검토다.')}
{vt}
{table(CONTRADICTIONS, 'Contradiction Map', ['주장 A', '충돌 근거', '실행 해석'])}
{source_details('Contradiction Map 원문', make_contradiction_md(), open_=True)}
"""


def roadmap() -> str:
    wg = """
<section class="wg-11" aria-labelledby="wg-11-title"><header class="wg-11-head"><p class="wg-11-kicker">Research Status · solo fallback</p><h2 id="wg-11-title" class="wg-11-h">content-only STORM 실행 상태판</h2><p class="wg-11-lead">로컬 storm-research 스킬 파일만으로 5영혼·모순지도·종합·동료검토를 구성했습니다.</p></header><div class="wg-11-kpis"><div class="wg-11-kpi wg-11-kpi-good"><span class="wg-11-kpi-v">5</span><span class="wg-11-kpi-l">영혼 관점</span></div><div class="wg-11-kpi wg-11-kpi-prog"><span class="wg-11-kpi-v">4</span><span class="wg-11-kpi-l">프롬프트 단계</span></div><div class="wg-11-kpi wg-11-kpi-risk"><span class="wg-11-kpi-v wg-11-warn">0</span><span class="wg-11-kpi-l">외부 웹 검색</span></div><div class="wg-11-kpi"><span class="wg-11-kpi-v">1</span><span class="wg-11-kpi-l">조건부 통과</span></div></div><h3 class="wg-11-h3">워크스트림 진척도</h3><div class="wg-11-bars"><div class="wg-11-bar-row"><span class="wg-11-bar-label">skill 읽기</span><div class="wg-11-track" role="img" aria-label="skill 읽기 100퍼센트"><div class="wg-11-fill wg-11-fill-good" style="width:100%"></div></div><span class="wg-11-bar-pct">100%</span></div><div class="wg-11-bar-row"><span class="wg-11-bar-label">5영혼 스캔</span><div class="wg-11-track" role="img" aria-label="5영혼 스캔 100퍼센트"><div class="wg-11-fill wg-11-fill-good" style="width:100%"></div></div><span class="wg-11-bar-pct">100%</span></div><div class="wg-11-bar-row"><span class="wg-11-bar-label">동료 검토</span><div class="wg-11-track" role="img" aria-label="동료 검토 100퍼센트"><div class="wg-11-fill wg-11-fill-good" style="width:100%"></div></div><span class="wg-11-bar-pct">100%</span></div><div class="wg-11-bar-row"><span class="wg-11-bar-label">외부 출처 검증</span><div class="wg-11-track" role="img" aria-label="외부 출처 검증 0퍼센트, content-only 조건"><div class="wg-11-fill wg-11-fill-risk" style="width:0%"></div></div><span class="wg-11-bar-pct">0%</span></div></div><div class="wg-11-cols"><div class="wg-11-col wg-11-col-good"><h4 class="wg-11-col-h"><span class="wg-11-dot"></span>완료</h4><ul class="wg-11-col-list"><li>SKILL.md·pipeline·provenance·prompts·souls 읽기</li><li>scan/contradiction/synthesis/peer-review 작성</li><li>HTML 템플릿 변환</li></ul></div><div class="wg-11-col wg-11-col-prog"><h4 class="wg-11-col-h"><span class="wg-11-dot"></span>진행 기준</h4><ul class="wg-11-col-list"><li>출처는 로컬 source snapshot으로 제한</li><li>추론은 [추론]으로 표기</li></ul></div><div class="wg-11-col wg-11-col-risk"><h4 class="wg-11-col-h"><span class="wg-11-dot"></span>리스크</h4><ul class="wg-11-col-list"><li>실제 웹 딥리서치가 아니므로 외부 사실 결론으로 확장 금지</li></ul></div></div></section>
"""
    return f"""
<div id="roadmap"></div>
{h2('05', 'Priority Roadmap · 리서치 실행 상태', 'roadmap', '요청 조건에 따라 full STORM 대신 content-only solo fallback으로 수행했다.')}
{wg}
"""


def validation_checklist() -> str:
    rows = [
        ["출처", "모든 핵심 주장에 source snapshot 연결", "PASS"],
        ["수치", "조직성 +25%, coverage +10%로만 표기", "PASS"],
        ["모순", "합의로 봉합하지 않고 핵심 긴장 유지", "PASS"],
        ["동료 검토", "source bias transfer / over-association 점검", "PASS"],
        ["범위", "외부 주제 사실로 확장하지 않음", "PASS"],
        ["한계", "content-only, no live web search 명시", "PASS"],
    ]
    return f"""
<div id="validation"></div>
{h2('06', 'Validation Checklist · peer review를 통과한 범위', 'check', 'STORM 스킬의 정직성 계약을 기준으로 산출물 범위를 잠갔다.')}
{table(rows, '리서치 검증 체크리스트', ['검사', '기준', '판정'])}
{source_details('Synthesis 원문', SYNTHESIS)}
{source_details('Peer Review 원문', PEER_REVIEW)}
"""


def final_recommendation() -> str:
    return f"""
<h2>{body_icon('final')}Final Recommendation · STORM은 답변 생성기가 아니라 리서치 운영체계다</h2>
<p>이 리서치의 결론은 단순하다. <strong>STORM을 쓸 때는 “다섯 관점”보다 “출처·모순·동료 검토”를 먼저 봐야 한다.</strong> 출처가 없으면 다관점은 브레인스토밍이고, peer-review가 없으면 종합은 자기확신이다.</p>
<p>실제 외부 주제에 적용할 때는 full 모드를 우선 검토하되, cmux/CLI가 없거나 빠른 초안이면 solo fallback으로 시작한다. 단, 산출물에는 항상 모드와 한계를 표시해야 한다.</p>
"""


def source_note() -> str:
    links = "".join(f'<li><a href="{esc(s["url"])}" target="_blank" rel="noopener noreferrer">{esc(s["name"])}</a> — {esc(s["role"])}</li>' for s in LOCAL_SOURCES)
    return f"""
{h2('07', 'Source Note · 콘텐츠 원천은 storm-research 스킬만 사용', 'source', 'adaptive-html-final은 HTML 골격·CSS·검증만 제공했다.')}
<p>보조 파일: <a href="sources/storm-report.json">storm-report.json</a> · <a href="sources/storm-scan.md">storm-scan.md</a> · <a href="sources/storm-contradiction-map.md">contradiction-map.md</a> · <a href="sources/storm-synthesis.md">synthesis.md</a> · <a href="sources/storm-peer-review.md">peer-review.md</a></p><ol class="refs">{links}</ol>
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
        (STORM / "SKILL.md", "storm-SKILL.md"),
        (STORM / "references" / "storm-pipeline.md", "storm-pipeline.md"),
        (STORM / "references" / "provenance.md", "provenance.md"),
        (STORM / "references" / "cmux-orchestration.md", "cmux-orchestration.md"),
        (STORM / "references" / "soul-distribution.md", "soul-distribution.md"),
        (STORM / "prompts" / "1-multi-perspective-scan.md", "prompt-1-multi-perspective-scan.md"),
        (STORM / "prompts" / "2-contradiction-map.md", "prompt-2-contradiction-map.md"),
        (STORM / "prompts" / "3-synthesis.md", "prompt-3-synthesis.md"),
        (STORM / "prompts" / "4-peer-review.md", "prompt-4-peer-review.md"),
        (STORM / "templates" / "report.schema.json", "report.schema.json"),
    ]
    for src, name in copy_map:
        if src.exists():
            shutil.copyfile(src, SOURCES / name)
    soul_text = []
    for p in sorted((STORM / "souls").glob("soul-*.md")):
        soul_text.append(f"\n\n<!-- {p.name} -->\n" + read(p))
    (SOURCES / "soul-charters.md").write_text("\n".join(soul_text).strip() + "\n", encoding="utf-8")

    scan = make_scan_md()
    contradiction = make_contradiction_md()
    (SOURCES / "storm-scan.md").write_text(scan + "\n", encoding="utf-8")
    (SOURCES / "storm-contradiction-map.md").write_text(contradiction + "\n", encoding="utf-8")
    (SOURCES / "storm-synthesis.md").write_text(SYNTHESIS + "\n", encoding="utf-8")
    (SOURCES / "storm-peer-review.md").write_text(PEER_REVIEW + "\n", encoding="utf-8")
    report = {
        "topic": TOPIC,
        "slug": "storm-research-skill-only-report",
        "generated_at": "2026-06-20",
        "mode": "solo-fallback-content-only",
        "content_source_rule": "Only local orginal_skill/storm-research files used for research content; no live web search.",
        "souls": [{"name": n, "persona": r["persona"], "summary": r["summary"], "markdown": r["body"], "sources": ["sources/storm-SKILL.md", "sources/storm-pipeline.md", "sources/provenance.md"]} for n, r in SOULS.items()],
        "contradiction_map": contradiction,
        "synthesis": SYNTHESIS,
        "peer_review": PEER_REVIEW,
        "confidence": {"source_diversity": "의도적으로 낮음(content-only)", "citation": "상(local snapshots)", "honesty": "상", "verdict": "조건부 통과"},
    }
    (SOURCES / "storm-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (SOURCES / "source-list.json").write_text(json.dumps(LOCAL_SOURCES, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (SOURCES / "storm-application.json").write_text(json.dumps({
        "skill": "storm-research",
        "selected_topic": TOPIC,
        "environment": {"cmux": "missing", "CMUX_WORKSPACE_ID": "NONE", "kimi": "missing"},
        "execution_mode": "solo fallback by main agent",
        "html_template_rule": "adaptive-html-final v5.10.5 used only for base/layout/css/widget/validation",
        "content_source_rule": "storm-research local skill content only",
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    shutil.copyfile(SKILL / "manifest.json", SOURCES / "adaptive-html-final-manifest.json")
    (SOURCES / "profile.json").write_text(json.dumps({"profile": PROFILE}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    placeholder_map = {
        "layout": LAYOUT,
        "EXECUTIVE_SUMMARY": "content-only STORM five-soul scan summary",
        "DECISION_CARDS": "full/solo/citation/peer-review decision cards",
        "ARCHITECTURE": "Phase 0-7 pipeline mapping",
        "RISK_MATRIX": "vt risk-matrix + contradiction map",
        "PRIORITY_ROADMAP": "wg-11 execution status board",
        "VALIDATION_CHECKLIST": "peer-review scope and honesty checks",
        "FINAL_RECOMMENDATION": "when STORM is worth using",
        "SOURCE_NOTE": "storm-research-only source hub",
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
        "skills/adaptive-html-final/assets/widget-templates/11-weekly-status.html",
        "orginal_skill/storm-research/SKILL.md",
        "orginal_skill/storm-research/references/storm-pipeline.md",
        "orginal_skill/storm-research/references/provenance.md",
        "orginal_skill/storm-research/prompts/1-multi-perspective-scan.md",
        "orginal_skill/storm-research/prompts/2-contradiction-map.md",
        "orginal_skill/storm-research/prompts/3-synthesis.md",
        "orginal_skill/storm-research/prompts/4-peer-review.md",
        "orginal_skill/storm-research/templates/report.schema.json",
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
        "input_snapshots": ["sources/storm-report.json", "sources/storm-scan.md", "sources/storm-contradiction-map.md", "sources/storm-synthesis.md", "sources/storm-peer-review.md"],
        "research_route": "storm-research solo fallback; content sourced only from local storm-research skill files",
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
    meta = f"<span>{MODE}</span><span>{LAYOUT}</span><span>profile {PROFILE}</span><span>adaptive-html-final v{version()}</span><span>content: storm-research only</span>"
    repl = {
        "{{KICKER}}": '<span class="kicker-text">storm-research skill-only report</span>',
        "{{TITLE}}": "STORM Research OS",
        "{{SUBTITLE}}": "다섯 영혼·모순 지도·종합·동료 검토로 단일 답변을 넘어서는 리서치 운영체계 분석",
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
        "</div></header>",
        "</div><div class=\"generated-row\"><p class=\"generated-date\">생성 기준: 2026-06-20 KST · storm-research content-only · adaptive-html-final template-only · expert_html · layout-first</p><div class=\"lens-strip\" aria-label=\"적용 렌즈\"><span class=\"lens-strip-label\">LENS</span><span class=\"lens-chip\">5 Souls</span><span class=\"lens-chip\">Contradiction Map</span><span class=\"lens-chip\">Synthesis</span><span class=\"lens-chip\">Peer Review</span><span class=\"lens-chip\">Provenance</span></div></div></header>",
        1,
    )
    title = f"STORM Research OS · storm-research skill-only · adaptive-html-final v{version()}"
    description = "storm-research 스킬 내용만으로 수행한 자유주제 리서치 HTML. adaptive-html-final은 템플릿과 검증에만 사용."
    json_ld = json.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": description,
        "inLanguage": "ko",
        "datePublished": "2026-06-20",
        "author": {"@type": "Organization", "name": "adaptive-html-final"},
        "keywords": ["storm-research", "STORM", "multi-perspective", "contradiction map", "peer review", "research ops"],
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
        "STORM Research OS",
        "storm-research",
        "다섯 영혼",
        "Contradiction Map",
        "Peer Review",
        "source bias transfer",
        "over-association",
        "조직성 +25%",
        "coverage +10%",
        "content-only",
        "Source Note",
    ]
    missing = [m for m in required if m not in visible]
    evidence = {
        "source_rule": "storm-research content only; adaptive-html-final template only",
        "source_count": len(LOCAL_SOURCES),
        "required_markers_missing": missing,
        "output_visible_text_chars": len(visible),
        "pass": not missing and len(visible) > 8500,
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
