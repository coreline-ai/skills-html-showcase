#!/usr/bin/env python3
"""Build a current adaptive-html-final education module from adaptive-html-learning-ultimate-merged + STORM research.

Selected topic:
  AI 튜터 시대의 4주 학습 시스템

The build is source-bound:
- adaptive-html-learning-ultimate-merged package rules for education_html, fact/opinion/inference split, quiz/answer gates
- storm-research local skill method for five-perspective scan, contradiction map, synthesis, peer review
- current adaptive-html-final assets for the final no-behavior-JS HTML
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
MERGED_PACKAGE = ROOT / "orginal_skill" / "adaptive-html-learning-ultimate-merged.skill"
STORM_SKILL = ROOT / "orginal_skill" / "storm-research"

OUT = ROOT / "output" / "2026-06-20" / "learning-ultimate-storm-ai-study-system"
SOURCES = OUT / "sources"

MODE = "education_html"
PROFILE = "auto"
LAYOUT = "course-module.html"
LAYOUT_CLASS = "layout-education"
PRIMARY_VT = "timeline"
PRIMARY_WG = "wg-15"

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
    "goals": "learning",
    "start": "question",
    "lesson": "idea",
    "example": "case",
    "practice": "timeline",
    "quiz": "check",
    "answer": "success",
    "review": "decision",
    "source": "source",
    "warning": "warning",
    "research": "search",
}

SOURCE_LIST = [
    {
        "name": "OpenAI · Introducing study mode",
        "url": "https://openai.com/index/chatgpt-study-mode/",
        "role": "step-by-step guidance, active participation, cognitive load, metacognition, knowledge checks",
        "used_for": "AI tutor design principle: answer-first 대신 guided learning",
    },
    {
        "name": "Google · Guided Learning in Gemini",
        "url": "https://blog.google/products-and-platforms/products/education/guided-learning/",
        "role": "questions, step-by-step breakdowns, multimodal responses, quizzes, active learning",
        "used_for": "멀티모달/퀴즈/질문형 학습 companion 설계",
    },
    {
        "name": "Khanmigo · Khan Academy AI tutor",
        "url": "https://www.khanmigo.ai/",
        "role": "doesn’t just give answers; guides learners; safety/supervision for minors",
        "used_for": "답을 찾게 하는 튜터와 보호자/학교 감독 경계",
    },
    {
        "name": "UNESCO · Guidance for generative AI in education and research",
        "url": "https://www.unesco.org/en/articles/guidance-generative-ai-education-and-research",
        "role": "human-centered approach, privacy and institutional readiness concerns",
        "used_for": "AI 학습 도구의 정책·프라이버시·연령 적합성 리스크",
    },
    {
        "name": "UNESCO · Artificial intelligence in education",
        "url": "https://www.unesco.org/en/digital-education/artificial-intelligence",
        "role": "human-centered, inclusive, equitable AI in education framing",
        "used_for": "교육에서 AI를 인간 역량 보강으로 제한하는 원칙",
    },
    {
        "name": "Dunlosky et al. · Effective learning techniques",
        "url": "https://pubmed.ncbi.nlm.nih.gov/26173288/",
        "role": "practice testing and distributed practice as high utility; rereading/highlighting low utility",
        "used_for": "4주 학습 루프의 retrieval/spacing 근거",
    },
    {
        "name": "IES What Works Clearinghouse · Organizing Instruction and Study",
        "url": "https://ies.ed.gov/ncee/wwc/practiceguide/1",
        "role": "space learning over time, interleave examples with exercises, use quizzing",
        "used_for": "주차별 분산·인터리빙·퀴즈 설계",
    },
    {
        "name": "Education Endowment Foundation · Metacognition and Self-Regulated Learning",
        "url": "https://educationendowmentfoundation.org.uk/education-evidence/guidance-reports/metacognition",
        "role": "planning, monitoring, evaluating learning; metacognition and self-regulation",
        "used_for": "학습 전·중·후 자기점검 루틴",
    },
    {
        "name": "Stanford STORM Research Project",
        "url": "https://storm-project.stanford.edu/research/storm/",
        "role": "multi-perspective question asking and retrieval-grounded outline synthesis",
        "used_for": "이번 산출물의 STORM식 리서치 절차",
    },
    {
        "name": "STORM paper · arXiv:2402.14207",
        "url": "https://arxiv.org/abs/2402.14207",
        "role": "Synthesis of Topic Outlines through Retrieval and Multi-perspective Question Asking",
        "used_for": "다관점 질문 → 충돌 지도 → 교육 모듈화 절차",
    },
]

FACT_ROWS = [
    ["OpenAI Study Mode", "빠른 정답 대신 단계별 안내, Socratic prompts, self-reflection, knowledge checks를 강조한다.", "AI 튜터 프롬프트는 '정답'보다 '힌트→시도→피드백' 순서로 둔다."],
    ["Google Guided Learning", "질문·단계별 breakdown·이미지/다이어그램/영상/퀴즈로 깊은 이해를 돕는다고 설명한다.", "설명만 긴 글보다 '보여주고, 물어보고, 다시 풀게 하는' 구조가 낫다."],
    ["Khanmigo", "답만 주지 않고 학습자가 스스로 답을 찾도록 안내하며, 미성년자는 부모/학교 파트너십 조건을 둔다.", "개인 학습에서도 보호자·교사·데이터 경계를 명시한다."],
    ["UNESCO", "GenAI 확산 속도가 규제·기관 준비보다 빠르며 프라이버시/검증 공백을 지적한다.", "AI 학습 루틴에는 개인정보 최소화와 사용금지 상황이 필요하다."],
    ["Dunlosky et al.", "practice testing과 distributed practice는 높은 utility 평가를 받았다.", "복습은 다시 읽기가 아니라 회상 테스트와 간격 반복으로 설계한다."],
    ["IES WWC", "시간을 두고 학습을 분산하고, worked example과 문제풀이를 섞고, 퀴즈로 재노출하라고 권고한다.", "4주 계획은 설명→예시→문제→퀴즈→간격 재등장으로 짠다."],
    ["EEF", "계획·모니터링·평가 전략을 명시적으로 가르치는 metacognition/self-regulation을 강조한다.", "AI 튜터는 학습자에게 '내가 무엇을 모르는지'를 말하게 해야 한다."],
]

STORM_SCAN = {
    "Skeptic": {
        "persona": "회의주의자",
        "question": "AI 튜터가 학습을 돕는다는 말은 정답 대행을 포장한 것 아닌가?",
        "summary": "가장 큰 실패 모드는 '즉시 답변'이 학습자의 회상·시도·오류 경험을 빼앗는 것이다.",
        "body": "OpenAI와 Google 모두 quick answers가 아니라 step-by-step 또는 deeper understanding을 강조한다. Khanmigo도 답을 주기보다 학습자가 찾도록 안내한다고 설명한다. 반대로 UNESCO는 프라이버시와 기관 검증 준비 부족을 지적한다. 따라서 AI 튜터를 쓰려면 정답 제공을 기본값으로 두지 않고, 사용 금지 상황과 데이터 경계를 함께 둬야 한다.",
        "sources": [SOURCE_LIST[0]["url"], SOURCE_LIST[1]["url"], SOURCE_LIST[2]["url"], SOURCE_LIST[3]["url"]],
    },
    "Economist": {
        "persona": "경제학자",
        "question": "AI 튜터의 경제적 가치는 어디에서 생기고 어디에서 과장되는가?",
        "summary": "가치는 교사를 대체하는 데서보다 피드백 지연을 줄이고 교사의 관찰 시간을 늘리는 데서 난다.",
        "body": "AI 튜터는 24시간 힌트·퀴즈·요약을 제공할 수 있어 피드백 비용을 낮춘다. 하지만 Khanmigo의 교사용 기능과 학교/구역 파트너십처럼 실제 교육 현장에서는 교사·부모·기관의 판단이 여전히 필요하다. 생산성 KPI는 '답변 수'가 아니라 '학생이 스스로 해결한 문제 수, 오류 설명 품질, 재시도율'이어야 한다.",
        "sources": [SOURCE_LIST[1]["url"], SOURCE_LIST[2]["url"], SOURCE_LIST[4]["url"]],
    },
    "Historian": {
        "persona": "역사학자",
        "question": "이번 AI 학습 붐은 이전 에듀테크 붐과 무엇이 다르고 무엇이 반복되는가?",
        "summary": "기술은 바뀌었지만 오래 버틴 학습 원리는 retrieval, spacing, feedback, metacognition이다.",
        "body": "새 도구는 매번 '개인화 혁명'을 약속했다. 그러나 Dunlosky 리뷰와 IES 가이드는 분산 학습, 연습 테스트, 예시와 문제의 교차, 퀴즈 재노출 같은 오래된 원칙을 다시 확인한다. AI 튜터의 차별점은 이 원칙을 매일 적용하도록 대화형으로 유지시킬 수 있다는 점이지, 원칙을 대체한다는 점이 아니다.",
        "sources": [SOURCE_LIST[5]["url"], SOURCE_LIST[6]["url"], SOURCE_LIST[7]["url"]],
    },
    "Academic": {
        "persona": "학자",
        "question": "AI 튜터가 학습 과학과 맞물리려면 최소 설계 조건은 무엇인가?",
        "summary": "설명은 회상 문제와 자기평가를 동반할 때 학습 활동이 된다.",
        "body": "OpenAI는 active participation, cognitive load, metacognition, knowledge checks를 명시한다. EEF는 planning, monitoring, evaluating을 포함한 자기조절 전략을 강조한다. 그러므로 좋은 AI 학습 루프는 '목표 진단 → 짧은 설명 → 학습자 회상 → 오답 피드백 → 간격 재등장 → 자기평가' 순서여야 한다.",
        "sources": [SOURCE_LIST[0]["url"], SOURCE_LIST[5]["url"], SOURCE_LIST[7]["url"]],
    },
    "Futurist": {
        "persona": "미래학자",
        "question": "AI 학습 경험은 앞으로 어떤 제품 형태로 수렴할까?",
        "summary": "개인화 대화창보다 중요한 것은 학습자의 기억 상태를 유지하는 adaptive study loop다.",
        "body": "Google은 multimodal responses와 interactive quizzes를, OpenAI는 progress tracking과 deeper personalization 가능성을 언급한다. 미래의 학습 제품은 '멋진 설명'을 넘어 학습자의 오답, 회상 성공률, 다음 재노출 시점, 프로젝트 적용 사례를 기록하는 루프가 될 가능성이 높다. 단, UNESCO의 human-centered 원칙처럼 최종 판단과 보호는 인간 쪽에 남겨야 한다.",
        "sources": [SOURCE_LIST[0]["url"], SOURCE_LIST[1]["url"], SOURCE_LIST[4]["url"]],
    },
}

CONTRADICTIONS = [
    ["즉시 도움은 학습 장벽을 낮춘다", "즉시 정답은 회상·시도·오류 경험을 빼앗는다", "정답 공개 전 반드시 '내 시도'와 '힌트 1개' 단계를 둔다"],
    ["개인화는 학습 효율을 높인다", "개인화에는 민감 데이터와 정책 공백 리스크가 따른다", "개인정보를 주제 밖으로 입력하지 않고 학교/조직 정책을 먼저 확인한다"],
    ["긴 설명은 이해감을 준다", "보존되는 기억은 회상 테스트와 간격 반복에서 강해진다", "모든 설명 뒤에는 3분 회상 문제와 다음 복습 일정을 붙인다"],
    ["AI가 교사 시간을 아낀다", "교사 판단과 학생 안전 감독은 자동화하기 어렵다", "AI는 초안과 피드백 보조, 교사는 목표·평가·개입을 맡는다"],
    ["멀티모달 자료는 흥미를 높인다", "이미지·영상만 소비하면 이해 착각이 생긴다", "자료 보기 후 개념을 말로 재구성하고 문제에 적용한다"],
]

SYNTHESIS = """# STORM Synthesis · AI 튜터 시대의 4주 학습 시스템

핵심 합의는 하나다. AI 튜터는 답변기가 아니라 학습 루프 관리자여야 한다. 제품들은 이미 quick answers에서 guided understanding으로 방향을 잡고 있고, 학습 과학은 practice testing, distributed practice, metacognition을 반복해서 강조한다. 둘을 합치면 실전 루프는 다섯 단계가 된다.

1. Diagnose — 목표, 현재 수준, 헷갈리는 지점을 먼저 말하게 한다.
2. Explain — 짧게 설명하고 예시를 하나만 준다.
3. Retrieve — 화면을 덮고 학습자가 스스로 떠올려 말한다.
4. Feedback — 오답의 원인을 하나만 교정하고 다시 시도한다.
5. Space — 다음 재노출 날짜와 변형 문제를 기록한다.

4주 설계는 Week 1 개념 지도, Week 2 회상·오답, Week 3 적용 프로젝트, Week 4 전이·평가로 구성한다. AI는 매일 질문을 던지고, 학습자는 매일 짧게 답하고, 주말에는 사람/동료/교사가 결과물을 점검한다.
"""

PEER_REVIEW = """# STORM Peer Review

검토 결과: 낙관 편향을 줄이기 위해 UNESCO와 Khanmigo의 safety/supervision 경계를 반드시 본문에 넣어야 한다. 또한 제품 기능 소개가 학습 효과 증거처럼 읽히지 않도록 OpenAI/Google/Khanmigo는 '제품 설계 방향'으로, Dunlosky/IES/EEF는 '학습 과학 근거'로 분리해야 한다.

수정 지시:
- AI 튜터 기능과 학습 효과를 동일시하지 않는다.
- 미성년자·학교·조직 데이터 사용에는 정책/보호자/교사 경계를 둔다.
- 4주 계획은 설명 소비보다 retrieval/spacing/practice 비중이 높게 보이도록 한다.
- 모든 주장에는 source hub를 붙이고, 검증되지 않은 미래 예측은 '가능성'으로 표기한다.
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
    return (
        f'<h2>{body_icon(icon)}<span class="num">{esc(num)}</span>{esc(title)}</h2>'
        f'<p class="h2-sub">{esc(sub)}</p>'
    )


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
        if re.match(r"^\d+\.\s", line):
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{esc(re.sub(r'^\d+\.\s+', '', line))}</li>")
            continue
        if line.startswith("- "):
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{esc(line[2:])}</li>")
            continue
        if in_ul:
            out.append("</ul>")
            in_ul = False
        if line.startswith("### "):
            out.append(f"<h3>{esc(line[4:])}</h3>")
        elif line.startswith("## "):
            out.append(f"<h3>{esc(line[3:])}</h3>")
        elif line.startswith("# "):
            out.append(f"<h3>{esc(line[2:])}</h3>")
        else:
            out.append(f"<p>{esc(line)}</p>")
    if in_ul:
        out.append("</ul>")
    return "\n".join(out)


def source_details(title: str, text: str, open_: bool = False) -> str:
    open_attr = " open" if open_ else ""
    return (
        f'<details class="source-preserve" style="margin:34px 0 0 24px;border-left:6px solid var(--accent);padding-left:20px"{open_attr}>'
        f'<summary style="padding:20px 24px 20px 34px;display:flex;align-items:center;gap:12px;flex-wrap:wrap">'
        f'<strong>{esc(title)}</strong><span class="tag">원문 보존</span></summary>'
        f'<div class="source-body" style="padding:0 28px 30px 34px">'
        f'<div style="border-left:1px solid var(--line);padding:24px 0 2px 24px">{markdownish_to_html(text)}</div>'
        f"</div></details>"
    )


def make_storm_markdown() -> tuple[str, str, str, str]:
    scan = ["# Multi-Perspective Scan · AI 튜터 시대의 4주 학습 시스템"]
    for name, row in STORM_SCAN.items():
        scan.extend([
            f"## {name} · {row['persona']}",
            f"질문: {row['question']}",
            row["summary"],
            row["body"],
            "출처: " + ", ".join(row["sources"]),
            "",
        ])
    contradiction = "# Contradiction Map\n" + "\n".join(f"- {a} ↔ {b} → {c}" for a, b, c in CONTRADICTIONS)
    return "\n".join(scan), contradiction, SYNTHESIS, PEER_REVIEW


def build_learning_goals(scan_md: str) -> str:
    cards = "".join(
        f'<article class="summary-card"><div class="label">{esc(name)} · {esc(row["persona"])}</div><h3>{esc(row["summary"])}</h3><p>{esc(row["body"])}</p></article>'
        for name, row in STORM_SCAN.items()
    )
    toc = """
<nav class="toc-map" id="document-toc" aria-label="문서 목차"><span class="label">문서 목차</span>
<p>adaptive-html-learning-ultimate-merged의 교육 모듈 흐름에 맞춰 목표, 준비, 수업, 예제, 실습, 퀴즈, 정답, 검토, 출처로 이동합니다.</p>
<div class="toc-pills">
<a class="toc-pill" href="#goals"><b>1</b>학습 목표</a>
<a class="toc-pill" href="#before"><b>2</b>시작 전</a>
<a class="toc-pill" href="#lesson"><b>3</b>개념 수업</a>
<a class="toc-pill" href="#example"><b>4</b>예제</a>
<a class="toc-pill" href="#practice"><b>5</b>실습</a>
<a class="toc-pill" href="#quiz"><b>6</b>퀴즈</a>
<a class="toc-pill" href="#answers"><b>7</b>정답</a>
<a class="toc-pill" href="#review"><b>8</b>검토</a>
<a class="toc-pill" href="#source-note"><b>9</b>출처</a>
</div></nav>
"""
    return f"""
{toc}
<div id="goals"></div>
{h2('01', '학습 목표 · AI 튜터를 답변기가 아니라 학습 루프 관리자로 쓰기', 'goals', '교육형 산출물의 첫 블록은 학습자가 끝나고 무엇을 할 수 있어야 하는지부터 고정한다.')}
<div class="summary-card"><div class="label">최종 산출물</div><p><strong>4주 뒤 학습자는</strong> AI에게 답을 대신 받는 사람이 아니라, 목표 진단·회상 테스트·오답 설명·간격 복습·프로젝트 적용을 스스로 운영하는 사람이 된다. 이 페이지는 제품 소개가 아니라 학습 루틴 설계서다.</p></div>
<div class="impact-grid">
  <article class="impact-card"><h3>이해</h3><p>Study Mode, Guided Learning, Khanmigo가 공통으로 말하는 '답보다 과정'의 의미를 설명한다.</p></article>
  <article class="impact-card"><h3>설계</h3><p>retrieval practice, distributed practice, metacognition을 AI 대화 루프에 넣는다.</p></article>
  <article class="impact-card"><h3>안전</h3><p>UNESCO식 human-centered 원칙과 개인정보/미성년자/기관 정책 경계를 적용한다.</p></article>
  <article class="impact-card"><h3>실행</h3><p>4주 동안 매일 25분으로 수행 가능한 학습 계획과 퀴즈를 만든다.</p></article>
</div>
<h3>STORM 다섯 관점이 남긴 핵심 질문</h3>
<div class="card-grid rail-cycle">{cards}</div>
{source_details('STORM Multi-Perspective Scan 원문', scan_md, open_=False)}
"""


def build_before_start() -> str:
    return f"""
<div id="before"></div>
{h2('02', '시작 전 · AI 학습의 성공 조건과 금지선', 'start', 'fact/opinion/inference를 분리하고, 학습 전에 필요한 용어와 경계 조건을 먼저 확인한다.')}
{table(FACT_ROWS, 'Fact / Interpretation / Action split — learning-ultimate-merged 적용', ['근거 축', '확인 가능한 사실', '실행 해석'])}
<div class="danger"><div class="label">먼저 금지</div><div class="name">개인정보·시험 부정·미성년자 단독 사용</div><p>학교·회사·시험·미성년자 학습에서 AI 도구를 쓸 때는 정책과 보호자/교사 경계를 먼저 확인한다. UNESCO가 지적한 규제·프라이버시 공백은 학습 효율보다 먼저 처리해야 한다.</p></div>
<div class="good"><div class="label">먼저 준비</div><div class="name">오늘의 목표를 한 문장으로 쓰기</div><p>AI에게 “이 단원을 알려줘”라고 시작하지 말고 “나는 25분 안에 X를 설명하고 Y 문제 2개를 풀 수 있어야 한다”라고 시작한다. 목표가 작을수록 힌트와 퀴즈 품질이 올라간다.</p></div>
<div class="concept-grid">
  <article class="summary-card"><h3>Retrieval</h3><p>답을 다시 읽는 것이 아니라 머릿속에서 꺼내는 활동. AI 설명 뒤 3분 동안 화면을 덮고 직접 말한다.</p></article>
  <article class="summary-card"><h3>Spacing</h3><p>오늘 배운 것을 내일·3일 뒤·1주 뒤 다시 만나게 하는 간격 설계. 잊기 직전에 다시 꺼낸다.</p></article>
  <article class="summary-card"><h3>Metacognition</h3><p>무엇을 알고 모르는지, 어떤 전략이 먹히는지 계획·점검·평가하는 활동. AI에게도 자기평가를 요구한다.</p></article>
</div>
"""


def build_concept_lesson(contradiction_md: str) -> str:
    vt = """
<section class="vt-shell" aria-label="4주 AI 학습 루프 타임라인">
  <div class="vt-frame">
    <ol class="tl">
      <li class="tl-item"><b>Week 1 · 진단과 개념 지도</b><p class="vt-text">목표를 쪼개고, 개념 지도를 만들고, AI에게 정답 대신 질문과 힌트를 요청한다.</p></li>
      <li class="tl-item"><b>Week 2 · 회상과 오답</b><p class="vt-text">설명 소비를 줄이고 매일 3분 회상, 오답 원인 1개, 변형 문제 1개를 반복한다.</p></li>
      <li class="tl-item"><b>Week 3 · 적용 프로젝트</b><p class="vt-text">작은 산출물을 만들고 AI를 코드/글/문제 피드백 보조자로 둔다. 최종 판단은 학습자가 한다.</p></li>
      <li class="tl-item"><b>Week 4 · 전이와 평가</b><p class="vt-text">새 문맥으로 옮겨 풀고, 설명·문제풀이·프로젝트 결과를 사람 기준으로 점검한다.</p></li>
    </ol>
  </div>
</section>
"""
    return f"""
<div id="lesson"></div>
{h2('03', '개념 수업 · AI 튜터는 다섯 단계 루프를 관리해야 한다', 'lesson', 'education_html의 1순위 vt timeline을 사용해 4주 학습 흐름을 시각화했다.')}
<p>AI 튜터의 핵심은 더 긴 설명이 아니다. 좋은 루프는 <span class="hl">진단 → 짧은 설명 → 회상 → 피드백 → 간격 재등장</span>이다. OpenAI와 Google의 제품 설명은 과정 중심 안내, 질문, 지식 점검을 강조하고, Dunlosky·IES·EEF 계열 학습 과학은 회상 테스트, 간격 복습, 자기조절을 강조한다. 이 둘이 만나는 지점이 4주 루프다.</p>
<figure aria-label="4주 학습 시스템 타임라인"><figcaption>vt timeline · AI 튜터 시대의 4주 학습 루프</figcaption>{vt}</figure>
<h3>Contradiction Map · 낙관과 경계 사이의 실행 기준</h3>
{table(CONTRADICTIONS, 'STORM Contradiction Map — 충돌을 실행 규칙으로 바꾸기', ['좋은 점', '위험', '운영 규칙'])}
{source_details('Contradiction Map 원문', contradiction_md, open_=True)}
"""


def build_example() -> str:
    return f"""
<div id="example"></div>
{h2('04', '예제 · “AI 영상 제작 파이프라인”을 배우는 하루', 'example', '사용자 IDE에 열려 있던 실제 관심사를 예시로 삼아, 정답 대행이 아닌 학습 대화를 보여준다.')}
<div class="before-after">
  <article><div class="label">나쁜 요청</div><p>“AI 영상 제작 파이프라인 전체를 정리해줘. 바로 써먹게 답 줘.”</p><p>결과: 읽기 좋은 요약은 얻지만, 다음 날 스스로 단계와 판단 기준을 설명하기 어렵다.</p></article>
  <article><div class="label">좋은 요청</div><p>“나는 25분 안에 기획→스크립트→이미지→음성→편집→검수 흐름을 외워서 설명하고 싶어. 먼저 나한테 3문항 진단 질문을 하고, 틀린 부분만 힌트로 도와줘.”</p><p>결과: AI가 질문자·피드백자·간격 복습 알림 역할을 하며 학습자가 회상한다.</p></article>
</div>
<div class="source-note"><h3>샘플 학습 대화</h3><p><strong>AI:</strong> 먼저 아무 자료 없이 60초 안에 파이프라인 단계를 말해보세요. 모르면 “건너뜀”이라고 적어도 됩니다.</p><p><strong>학습자:</strong> 기획, 대본, 영상 생성, 편집, 업로드… 음성은 어디에 들어가는지 헷갈립니다.</p><p><strong>AI:</strong> 좋아요. 지금의 오답 원인은 “제작 자산”과 “후반 작업”이 섞인 것입니다. 힌트 하나만 줄게요: 사람 목소리·배경음·자막 타이밍은 어느 단계에서 품질 차이를 가장 크게 만들까요?</p><p><strong>학습자:</strong> 음성/자막을 별도 단계로 빼고, 편집 전에 검수해야겠네요.</p></div>
<div class="good"><div class="label">핵심</div><div class="name">AI가 적게 말할수록 학습자가 많이 떠올린다</div><p>예제의 목적은 정답을 숨기는 것이 아니다. 정답까지 가는 시간을 학습자가 직접 밟게 만드는 것이다.</p></div>
"""


def build_practice(synthesis_md: str) -> str:
    wg15 = """
<section class="wg-15" aria-labelledby="wg-15-title">
  <p class="wg-15-kicker">개념 교보재 · AI Tutor Study Loop</p>
  <h2 id="wg-15-title" class="wg-15-h">정답기가 아니라 회상 루프 관리자</h2>
  <p class="wg-15-lead">AI 튜터의 역할을 설명자, 질문자, 피드백자, 복습 스케줄러로 나누면 학습 효과와 안전 경계를 함께 관리할 수 있습니다.</p>
  <h3 class="wg-15-h3">두 사용법 비교</h3>
  <div class="table-scroll"><table class="wg-15-table"><caption class="wg-15-cap">AI 튜터 사용 방식 비교</caption><thead><tr><th scope="col">기준</th><th scope="col">정답 대행 모드</th><th scope="col">학습 루프 모드</th></tr></thead><tbody>
    <tr><th scope="row">첫 질문</th><td><span class="wg-15-bad">답부터 알려줘</span></td><td><span class="wg-15-good">먼저 진단 질문 3개</span></td></tr>
    <tr><th scope="row">설명 길이</th><td>긴 요약</td><td>짧은 설명 + 회상 문제</td></tr>
    <tr><th scope="row">피드백</th><td>정답 확인</td><td>오답 원인 1개와 재시도</td></tr>
    <tr><th scope="row">복습</th><td>다시 읽기</td><td>내일·3일 뒤·1주 뒤 재노출</td></tr>
  </tbody></table></div>
  <h3 class="wg-15-h3">단계별로 실행하기</h3>
  <div class="wg-15-steps">
    <input type="radio" name="wg-15-step" id="wg-15-s1" class="wg-15-step-in" checked>
    <input type="radio" name="wg-15-step" id="wg-15-s2" class="wg-15-step-in">
    <input type="radio" name="wg-15-step" id="wg-15-s3" class="wg-15-step-in">
    <div class="wg-15-stepnav">
      <label class="wg-15-stepbtn" for="wg-15-s1"><span class="wg-15-stepnum">1</span> 진단</label>
      <label class="wg-15-stepbtn" for="wg-15-s2"><span class="wg-15-stepnum">2</span> 회상</label>
      <label class="wg-15-stepbtn" for="wg-15-s3"><span class="wg-15-stepnum">3</span> 간격</label>
    </div>
    <div class="wg-15-stage">
      <div class="wg-15-ring" aria-hidden="true"><span class="wg-15-node wg-15-na">목표</span><span class="wg-15-node wg-15-nb">힌트</span><span class="wg-15-node wg-15-nc">퀴즈</span><span class="wg-15-node wg-15-nd wg-15-new">복습</span><span class="wg-15-key wg-15-k1">오답</span><span class="wg-15-key wg-15-k2">성공</span><span class="wg-15-center">Study Loop</span></div>
      <div class="wg-15-panels">
        <div class="wg-15-panel wg-15-p1"><h4 class="wg-15-pt">1. 목표와 현재 수준을 먼저 말한다</h4><p>AI에게 설명을 요청하기 전, 오늘 끝나고 스스로 할 수 있어야 할 행동을 한 문장으로 적습니다.</p><p class="wg-15-note-line">예: “오늘은 변수 개념을 말로 설명하고 예제 2개를 풀겠다.”</p></div>
        <div class="wg-15-panel wg-15-p2"><h4 class="wg-15-pt">2. 설명 뒤에는 반드시 회상한다</h4><p>AI의 설명을 읽은 뒤 화면을 덮고 3분 동안 핵심을 말합니다. 모르면 다시 설명을 요청하기보다 힌트 하나만 받습니다.</p><p class="wg-15-note-line">회상이 어렵게 느껴지는 순간이 학습이 일어나는 지점입니다.</p></div>
        <div class="wg-15-panel wg-15-p3"><h4 class="wg-15-pt">3. 다음 재노출을 예약한다</h4><p>오늘 맞힌 문제도 내일·3일 뒤·1주 뒤 변형 문제로 다시 만납니다. AI는 일정표를 만들고 학습자는 직접 풉니다.</p><p class="wg-15-note-line">복습은 다시 읽기가 아니라 다시 꺼내기입니다.</p></div>
      </div>
    </div>
  </div>
</section>
"""
    return f"""
<div id="practice"></div>
{h2('05', '실습 · 4주 실행 플레이북', 'practice', '교육형 필수 블록인 practice를 표, 위젯, 체크 루틴으로 구성했다.')}
<p>아래 계획은 매일 25분 기준이다. 시간이 더 있다면 설명 시간을 늘리지 말고 문제 수와 회상 횟수를 늘린다. AI는 매번 “정답 공개 전 힌트 1개” 규칙을 따른다.</p>
{wg15}
{table([
    ['Week 1', '개념 지도 만들기', 'AI에게 진단 질문 3개 요청 → 내가 아는 것/모르는 것 분리 → 짧은 설명 → 3분 회상', '개념 지도 1장'],
    ['Week 2', '오답 로그 만들기', '매일 변형 문제 2개 → 오답 원인 1개만 피드백 → 내 언어로 다시 설명', '오답 로그 10개'],
    ['Week 3', '작은 프로젝트 적용', '배운 개념으로 글/코드/문제 풀이 산출물 작성 → AI는 리뷰어 역할만 수행', '프로젝트 초안'],
    ['Week 4', '전이와 평가', '새 문맥 문제 5개 → 사람/동료/교사에게 설명 → 부족한 개념만 재학습', '최종 설명 녹음/문서'],
], '4주 AI 튜터 학습 계획', ['주차', '목표', '매일 25분 루틴', '산출물'])}
<div class="try"><h3>오늘 바로 쓸 프롬프트</h3><p>“너는 답을 바로 주지 않는 학습 코치야. 먼저 내 목표와 현재 수준을 진단하는 질문 3개를 해줘. 내가 답하면 오답 원인을 하나만 짚고, 힌트 1개와 회상 문제 1개를 줘. 마지막에는 내일 복습할 변형 문제를 만들어줘.”</p></div>
{source_details('STORM Synthesis 원문', synthesis_md, open_=False)}
"""


def build_quiz() -> str:
    return f"""
<div id="quiz"></div>
{h2('06', '퀴즈 · 이해 착각을 걷어내는 7문항', 'quiz', 'learning-ultimate-merged의 교육 산출물 조건에 맞춰 문제와 정답 섹션을 분리했다.')}
<ol class="checklist">
  <li><strong>객관식:</strong> AI 튜터를 학습 루프 관리자로 만들기 위한 가장 좋은 첫 요청은? A. 전체 답을 요약해줘 B. 먼저 진단 질문 3개를 해줘 C. 관련 영상을 추천해줘 D. 시험 정답만 알려줘</li>
  <li><strong>단답:</strong> 설명을 읽은 뒤 화면을 덮고 스스로 떠올리는 학습 활동을 무엇이라고 부르는가?</li>
  <li><strong>판단:</strong> “AI가 길게 설명해주면 복습은 다시 읽기만 해도 충분하다.” 맞는가, 틀린가?</li>
  <li><strong>적용:</strong> 오늘 배운 개념을 내일 다시 복습하게 하려면 AI에게 무엇을 요청해야 하는가?</li>
  <li><strong>리스크:</strong> UNESCO 관점에서 교육용 GenAI 사용 전에 확인해야 할 경계 2가지를 쓰라.</li>
  <li><strong>설계:</strong> 25분 학습 세션을 진단·설명·회상·피드백·간격 재등장으로 나누어 5줄 계획으로 쓰라.</li>
  <li><strong>전이:</strong> 내가 배운 개념을 새 문맥에 적용하는 문제를 AI에게 만들게 할 때 피해야 할 요청 방식은?</li>
</ol>
"""


def build_answer_key() -> str:
    return f"""
<div id="answers"></div>
{h2('07', '정답과 해설 · 답보다 판단 근거를 확인하기', 'answer', '정답은 간단히, 해설은 실제 행동 기준으로 적었다.')}
<ol class="checklist">
  <li><strong>B.</strong> 진단 질문이 먼저다. 목표와 현재 수준 없이 받은 설명은 쉽게 과잉·과소 설명이 된다.</li>
  <li><strong>Retrieval practice / 회상 연습.</strong> 다시 읽기보다 기억에서 꺼내는 활동이다.</li>
  <li><strong>틀림.</strong> Dunlosky 리뷰와 IES 가이드의 핵심은 practice testing, distributed practice, quizzing이다.</li>
  <li><strong>변형 문제와 재노출 일정.</strong> “내일 3분 회상 문제 2개와 3일 뒤 변형 문제 1개를 만들어줘”처럼 요청한다.</li>
  <li><strong>예시 답:</strong> 개인정보/데이터 보호, 미성년자·학교 정책, 도구 검증 상태, 인간 감독 여부.</li>
  <li><strong>예시 계획:</strong> 3분 목표/진단 → 7분 짧은 설명 → 5분 화면 덮고 회상 → 7분 오답 피드백/재시도 → 3분 다음 복습 예약.</li>
  <li><strong>피해야 할 방식:</strong> “답과 풀이를 모두 보여줘.” 대신 “문제만 먼저 내고, 내가 푼 뒤 힌트와 피드백을 줘.”라고 요청한다.</li>
</ol>
"""


def build_review(peer_md: str) -> str:
    return f"""
<div id="review"></div>
{h2('08', '최종 검토 · AI 학습 세션이 진짜 학습인지 판별하기', 'review', '검증 OK만으로 품질 완료가 아니므로 학습·안전·출처 관점의 손검수 기준을 남긴다.')}
<div class="accessibility-checklist"><h3>수업 전 체크리스트</h3><ul><li>정답 공개 전 학습자 시도 단계가 있는가?</li><li>설명 뒤 회상 문제와 오답 피드백이 있는가?</li><li>복습 일정이 오늘·내일·3일 뒤·1주 뒤로 분산되어 있는가?</li><li>개인정보, 시험 부정, 미성년자/학교 정책 경계가 적혀 있는가?</li><li>제품 기능 주장과 학습 과학 근거가 분리되어 있는가?</li><li>AI가 만든 결과를 사람/교사/동료가 검토할 접점이 있는가?</li></ul></div>
<div class="danger"><div class="label">정직한 한계</div><div class="name">제품 기능은 학습 효과 자체가 아니다</div><p>Study Mode, Guided Learning, Khanmigo는 학습 지향 설계를 보여주는 제품 근거다. 실제 학습 효과는 학습자, 과목, 사용 맥락, 감독, 평가 방식에 따라 달라진다. 그래서 본 페이지는 '효과 보장'이 아니라 '효과 가능성을 높이는 운영 루프'를 제시한다.</p></div>
{source_details('STORM Peer Review 원문', peer_md, open_=True)}
"""


def build_source_note() -> str:
    links_html = "".join(
        f'<li><a href="{esc(src["url"])}" target="_blank" rel="noopener noreferrer">{esc(src["name"])}</a> — {esc(src["used_for"])}</li>'
        for src in SOURCE_LIST
    )
    return f"""
<div id="source-note"></div>
{h2('09', 'Source Hub · 출처와 스킬 적용 증빙', 'source', '출처 10개, STORM 산출물, merged skill 적용 기록, current adaptive-html-final 스냅샷을 분리 보관했다.')}
<p>STORM은 현재 로컬 환경에서 cmux/kimi 없이 solo fallback으로 재해석했다. 다만 관점 분리, 충돌 지도, 출처 허브, peer review 기록은 storm-research 스킬의 구조를 따랐다.</p>
<div class="source-note"><p><strong>보조 산출물:</strong> <a href="sources/storm-scan.md">storm-scan.md</a> · <a href="sources/storm-contradiction-map.md">contradiction-map.md</a> · <a href="sources/storm-synthesis.md">synthesis.md</a> · <a href="sources/storm-peer-review.md">peer-review.md</a> · <a href="sources/source-list.json">source-list.json</a> · <a href="sources/learning-ultimate-application.json">learning-ultimate 적용 기록</a></p></div>
<ol class="refs">{links_html}</ol>
"""


def copy_sources(scan_md: str, contradiction_md: str, synthesis_md: str, peer_md: str) -> dict:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "pages").mkdir(parents=True, exist_ok=True)
    SOURCES.mkdir(parents=True, exist_ok=True)
    (SOURCES / "assets").mkdir(parents=True, exist_ok=True)
    (SOURCES / "screenshots").mkdir(parents=True, exist_ok=True)

    (SOURCES / "source-list.json").write_text(json.dumps(SOURCE_LIST, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (SOURCES / "storm-scan.md").write_text(scan_md + "\n", encoding="utf-8")
    (SOURCES / "storm-contradiction-map.md").write_text(contradiction_md + "\n", encoding="utf-8")
    (SOURCES / "storm-synthesis.md").write_text(synthesis_md + "\n", encoding="utf-8")
    (SOURCES / "storm-peer-review.md").write_text(peer_md + "\n", encoding="utf-8")
    (SOURCES / "storm-report.json").write_text(json.dumps({
        "topic": "AI 튜터 시대의 4주 학습 시스템",
        "mode": "solo-fallback-by-main-agent",
        "method": "five perspectives, contradiction map, synthesis, peer review, official web sources",
        "souls": STORM_SCAN,
        "contradictions": CONTRADICTIONS,
        "synthesis": synthesis_md,
        "peer_review": peer_md,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (SOURCES / "learning-ultimate-application.json").write_text(json.dumps({
        "skill": "adaptive-html-learning-ultimate-merged",
        "source_package": str(MERGED_PACKAGE.relative_to(ROOT)),
        "selected_mode": MODE,
        "audience": "AI 학습자, 교육자, 자기주도 학습 설계자, AI 도구를 쓰는 실무자",
        "format": "single HTML education module",
        "applied_rules": [
            "input analysis and mode routing",
            "fact/opinion/inference split",
            "education_html blocks: goals, before_start, lesson, example, practice, quiz, answer",
            "source hub for more than 6 links",
            "quiz and answer key included",
            "no external behavior JS",
            "mobile/reading flow/accessible table captions",
        ],
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    shutil.copyfile(SKILL / "manifest.json", SOURCES / "adaptive-html-final-manifest.json")
    (SOURCES / "profile.json").write_text(json.dumps({"profile": PROFILE}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (SOURCES / "layout-placeholder-map.json").write_text(json.dumps({
        "layout": LAYOUT,
        "KICKER": "adaptive-html-learning-ultimate-merged + STORM",
        "TITLE": "AI 튜터 시대의 4주 학습 시스템",
        "SUBTITLE": "제품 기능이 아니라 학습 루프 설계로 읽는 Study Mode, Guided Learning, Khanmigo, UNESCO, retrieval practice",
        "META": "mode/profile/version/lens",
        "LEARNING_GOALS": "목표 + STORM 다섯 관점 + 목차",
        "BEFORE_START": "사실/해석/실행 분리 + 안전 경계",
        "CONCEPT_LESSON": "vt timeline + contradiction map",
        "EXAMPLE": "AI 영상 제작 파이프라인 학습 예제",
        "PRACTICE": "wg-15 concept explainer + 4주 플레이북",
        "QUIZ": "7문항 퀴즈",
        "ANSWER_KEY": "정답과 해설",
        "REVIEW_CHECKLIST": "품질/안전 손검수",
        "SOURCE_NOTE": "출처 허브와 스킬 적용 증빙",
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

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
        "inline_order": [name for name, _ in INLINE_ORDER],
    }
    (SOURCES / "css-integrity.json").write_text(json.dumps(integrity, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    evidence_files = [
        "AGENTS.md",
        "skills/adaptive-html-final/SKILL.md",
        "skills/adaptive-html-final/manifest.json",
        "skills/adaptive-html-final/assets/base.html",
        "skills/adaptive-html-final/assets/layouts/course-module.html",
        "skills/adaptive-html-final/assets/visual-html-templates/04-timeline.html",
        "skills/adaptive-html-final/assets/widget-templates/15-concept-explainer.html",
        "skills/adaptive-html-final/references/writing-system.md",
        "skills/adaptive-html-final/references/layout-system.md",
        "orginal_skill/adaptive-html-learning-ultimate-merged.skill",
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
        "section_mapping": json.loads((SOURCES / "layout-placeholder-map.json").read_text(encoding="utf-8")),
        "files": [{"path": p, "sha256": sha(ROOT / p)} for p in evidence_files if (ROOT / p).exists()],
        "input_snapshots": [
            "sources/storm-scan.md",
            "sources/storm-contradiction-map.md",
            "sources/storm-synthesis.md",
            "sources/storm-peer-review.md",
            "sources/learning-ultimate-application.json",
        ],
        "research_route": "storm-research solo fallback; web-sourced claims stored in source-list.json",
    }
    (SOURCES / "build-evidence.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return integrity


def css_slots(integrity: dict) -> dict:
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
    meta_inner = (
        f'<span>{MODE}</span><span>{LAYOUT}</span><span>profile {PROFILE}</span>'
        f'<span>adaptive-html-final v{version()}</span><span>learning-ultimate-merged</span>'
    )
    body = layout
    replacements = {
        "{{KICKER}}": '<span class="kicker-text">adaptive-html-learning-ultimate-merged × STORM Research</span>',
        "{{TITLE}}": "AI 튜터 시대의 4주 학습 시스템",
        "{{SUBTITLE}}": "Study Mode, Guided Learning, Khanmigo, UNESCO, retrieval practice를 STORM으로 엮어 만든 교육형 HTML 모듈",
        "{{META}}": meta_inner,
        "{{LEARNING_GOALS}}": build_learning_goals(scan_md),
        "{{BEFORE_START}}": build_before_start(),
        "{{CONCEPT_LESSON}}": build_concept_lesson(contradiction_md),
        "{{EXAMPLE}}": build_example(),
        "{{PRACTICE}}": build_practice(synthesis_md),
        "{{QUIZ}}": build_quiz(),
        "{{ANSWER_KEY}}": build_answer_key(),
        "{{REVIEW_CHECKLIST}}": build_review(peer_md),
        "{{SOURCE_NOTE}}": build_source_note(),
    }
    for key, value in replacements.items():
        body = body.replace(key, value)
    body = body.replace(
        '</div></header>',
        '</div><div class="generated-row"><p class="generated-date">생성 기준: 2026-06-20 KST · STORM solo research · education_html · layout-first</p>'
        '<div class="lens-strip" aria-label="적용 렌즈"><span class="lens-strip-label">LENS</span><span class="lens-chip">학습 과학</span><span class="lens-chip">AI 튜터</span><span class="lens-chip">안전</span><span class="lens-chip">4주 실행</span><span class="lens-chip">퀴즈</span></div></div></header>',
        1,
    )

    title = "AI 튜터 시대의 4주 학습 시스템 · learning ultimate STORM"
    description = f"adaptive-html-learning-ultimate-merged와 STORM 리서치로 만든 AI 튜터 시대의 4주 학습 시스템 교육형 HTML. adaptive-html-final v{version()} 스타일."
    json_ld = json.dumps({
        "@context": "https://schema.org",
        "@type": "LearningResource",
        "name": title,
        "description": description,
        "inLanguage": "ko",
        "datePublished": "2026-06-20",
        "learningResourceType": "CourseModule",
        "educationalLevel": "self-directed adult learning",
        "author": {"@type": "Organization", "name": "adaptive-html-final"},
        "keywords": ["AI 튜터", "Study Mode", "Guided Learning", "Khanmigo", "retrieval practice", "distributed practice", "metacognition"],
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
    for key, value in slots.items():
        doc = doc.replace(key, value)
    leftovers = sorted(set(re.findall(r"{{[^}]+}}", doc)))
    if leftovers:
        raise RuntimeError(f"unresolved placeholders: {leftovers}")
    doc = re.sub(r"\n{4,}", "\n\n\n", doc)
    return doc


def content_evidence(doc: str) -> None:
    visible = re.sub(r"<style\b[^>]*>[\s\S]*?</style>", "", doc, flags=re.I)
    visible = re.sub(r"<script\b[^>]*>[\s\S]*?</script>", "", visible, flags=re.I)
    visible = re.sub(r"<[^>]+>", " ", visible)
    visible = re.sub(r"\s+", " ", html.unescape(visible))
    required = [
        "AI 튜터 시대의 4주 학습 시스템",
        "adaptive-html-learning-ultimate-merged",
        "STORM",
        "회의주의자",
        "경제학자",
        "역사학자",
        "Fact / Interpretation / Action",
        "Contradiction Map",
        "4주 AI 튜터 학습 계획",
        "퀴즈",
        "정답과 해설",
        "Source Hub",
    ]
    missing = [x for x in required if x not in visible]
    evidence = {
        "storm_soul_count": len(STORM_SCAN),
        "source_count": len(SOURCE_LIST),
        "required_markers_missing": missing,
        "output_visible_text_chars": len(visible),
        "pass": not missing and len(visible) > 12000,
    }
    (SOURCES / "content-preservation.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not evidence["pass"]:
        raise RuntimeError(f"content preservation failed: {evidence}")


def main() -> None:
    scan_md, contradiction_md, synthesis_md, peer_md = make_storm_markdown()
    integrity = copy_sources(scan_md, contradiction_md, synthesis_md, peer_md)
    doc = render(scan_md, contradiction_md, synthesis_md, peer_md, integrity)
    (OUT / "index.html").write_text(doc, encoding="utf-8")
    content_evidence(doc)
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
