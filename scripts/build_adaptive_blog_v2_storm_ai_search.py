#!/usr/bin/env python3
"""Build a current adaptive-html-final article from adaptive-html-blog-writer-v2 + STORM research.

Selected topic:
  AI 검색 시대의 블로그 생존 전략 2026

Inputs are intentionally source-bound:
- adaptive-html-blog-writer-v2 skill rules for mode, writing, SEO, and editorial gates
- storm-research method for 5-perspective scan, contradiction map, synthesis, peer review
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
BLOG_V2_INSTALLED = Path("/Users/hwanchoi/.codex/skills/adaptive-html-blog-writer-v2")
BLOG_V2_PACKAGE = ROOT / "orginal_skill" / "adaptive-html-blog-writer-v2.skill"
STORM_SKILL = ROOT / "orginal_skill" / "storm-research"

OUT = ROOT / "output" / "2026-06-20" / "adaptive-blog-v2-storm-ai-search"
SOURCES = OUT / "sources"

MODE = "article_html"
PROFILE = "auto"
LAYOUT = "magazine-article.html"
LAYOUT_CLASS = "layout-article"
PRIMARY_VT = "decision-tree"
PRIMARY_WG = "wg-14"

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
    "problem": "warning",
    "context": "search",
    "argument": "idea",
    "case": "case",
    "conclusion": "check",
    "takeaway": "decision",
    "seo": "metric",
    "source": "source",
    "storm": "question",
}


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
        f'<details class="source-preserve" style="margin:32px 0 0 18px;border-left:6px solid var(--accent)"{open_attr}>'
        f'<summary style="padding:20px 26px 20px 58px;display:flex;align-items:center;gap:12px;flex-wrap:wrap">'
        f'<strong>{esc(title)}</strong><span class="tag">근거 보존</span></summary>'
        f'<div class="source-body" style="padding:0 28px 30px 58px">'
        f'<div style="border-left:1px solid var(--line);padding:26px 0 2px 24px">{markdownish_to_html(text)}</div>'
        f"</div></details>"
    )


SOURCE_LIST = [
    {
        "name": "Google Search Central · Optimizing for generative AI features",
        "url": "https://developers.google.com/search/docs/fundamentals/ai-optimization-guide",
        "role": "Google이 generative AI search에서도 SEO fundamentals가 유효하다고 설명하는 최신 공식 가이드",
    },
    {
        "name": "Google Search Central · AI features and your website",
        "url": "https://developers.google.com/search/docs/appearance/ai-features",
        "role": "AI Overviews/AI Mode의 query fan-out, technical requirements, Search Console 처리 설명",
    },
    {
        "name": "OpenAI Help Center · ChatGPT Search",
        "url": "https://help.openai.com/en/articles/9237897-chatgpt-search",
        "role": "ChatGPT Search의 citations/Sources 패널 사용자 경험 설명",
    },
    {
        "name": "OpenAI · Introducing ChatGPT search",
        "url": "https://openai.com/index/introducing-chatgpt-search/",
        "role": "ChatGPT search가 timely answers와 relevant web sources 링크를 제공한다는 제품 설명",
    },
    {
        "name": "OpenAI Developers · Overview of OpenAI Crawlers",
        "url": "https://developers.openai.com/api/docs/bots",
        "role": "OAI-SearchBot, GPTBot, ChatGPT-User의 목적과 robots.txt 분리 설명",
    },
    {
        "name": "Cloudflare Blog · Pay per crawl",
        "url": "https://blog.cloudflare.com/introducing-pay-per-crawl/",
        "role": "콘텐츠 소유자가 AI crawler 접근을 allow/charge/block로 제어하는 모델",
    },
    {
        "name": "Cloudflare Docs · What is Pay Per Crawl?",
        "url": "https://developers.cloudflare.com/ai-crawl-control/features/pay-per-crawl/what-is-pay-per-crawl/",
        "role": "Pay per crawl closed beta, HTTP 200/402 기반 접근 제어 설명",
    },
    {
        "name": "Cloudflare Blog · Crawl-to-click gap",
        "url": "https://blog.cloudflare.com/crawlers-click-ai-bots-training/",
        "role": "AI crawling 목적과 referral imbalance에 대한 Cloudflare 데이터",
    },
    {
        "name": "Columbia Journalism Review · ChatGPT Search and publisher content",
        "url": "https://www.cjr.org/tow_center/how-chatgpt-misrepresents-publisher-content.php",
        "role": "AI search citation/attribution의 publisher-side 리스크를 제기하는 비판 자료",
    },
    {
        "name": "Stanford STORM Research Project",
        "url": "https://storm-project.stanford.edu/research/storm/",
        "role": "다관점 질문 + retrieval grounding 리서치 방법론",
    },
    {
        "name": "STORM paper · arXiv 2402.14207",
        "url": "https://arxiv.org/abs/2402.14207",
        "role": "STORM 원논문 추적성",
    },
]


FACT_ROWS = [
    ["Google", "AI Overviews/AI Mode는 query fan-out과 Search index 기반 grounding을 설명한다.", "키워드 하나가 아니라 하위 질문 묶음을 커버해야 한다."],
    ["Google", "AI 기능에 표시되려면 기본적으로 색인·snippet 표시 가능성 등 기존 Search 요건이 전제다.", "기술 SEO를 버리지 말고 crawl/index/snippet을 유지한다."],
    ["OpenAI", "ChatGPT Search는 inline citations 또는 Sources 패널로 출처를 보여줄 수 있다.", "출처로 선택될 때 클릭 가능한 제목·요약·근거 구조가 중요하다."],
    ["OpenAI", "OAI-SearchBot과 GPTBot은 목적이 분리되어 있으며 robots.txt 관리도 독립적이다.", "검색 노출과 모델 학습 허용을 같은 정책으로 보지 않는다."],
    ["Cloudflare", "Pay per crawl은 콘텐츠 소유자가 crawler를 allow/charge/block하도록 설계된 closed beta 기능이다.", "콘텐츠는 트래픽 상품에서 접근권 상품으로도 재정의된다."],
    ["CJR/Tow Center", "AI search가 publisher content를 오인용·오표현할 위험을 제기했다.", "AI 노출은 기회와 동시에 attribution QA 문제다."],
]


STORM_SCAN = {
    "Skeptic": {
        "persona": "회의주의자",
        "summary": "AI 검색은 링크를 준다고 약속하지만, 출처 오인용·클릭 감소·crawler 비대칭이 남는다.",
        "body": "Google과 OpenAI는 links/sources를 제품 경험의 일부로 설명하지만, 출처가 있다는 사실과 출처가 정확히 대표된다는 사실은 다르다. CJR/Tow Center는 ChatGPT Search가 publisher content를 오표현할 수 있다는 위험을 제기했고, Cloudflare는 AI bot crawling과 referral imbalance를 별도 문제로 다룬다. 따라서 블로그 전략은 'AI에 인용되면 성공'이 아니라 '인용되어도 왜곡되지 않게 근거 단위를 설계하고, crawler 정책을 분리 관리하는 것'이어야 한다.",
        "sources": [
            "https://www.cjr.org/tow_center/how-chatgpt-misrepresents-publisher-content.php",
            "https://blog.cloudflare.com/crawlers-click-ai-bots-training/",
            "https://help.openai.com/en/articles/9237897-chatgpt-search",
        ],
    },
    "Economist": {
        "persona": "경제학자",
        "summary": "콘텐츠의 단위 경제가 pageview 광고에서 citation, crawler access, subscription conversion으로 갈라진다.",
        "body": "Cloudflare의 Pay per crawl은 allow/block 사이에 charge라는 세 번째 선택지를 제안한다. Google은 AI 검색에서도 더 깊은 engagement와 conversion 기회가 있을 수 있다고 말하지만, Cloudflare 데이터는 crawling과 referral의 비대칭을 보여준다. 콘텐츠 운영자는 traffic-only KPI를 버리고 citation visibility, crawler policy, subscriber capture, licensing readiness를 함께 보아야 한다.",
        "sources": [
            "https://blog.cloudflare.com/introducing-pay-per-crawl/",
            "https://developers.cloudflare.com/ai-crawl-control/features/pay-per-crawl/what-is-pay-per-crawl/",
            "https://developers.google.com/search/docs/fundamentals/ai-optimization-guide",
        ],
    },
    "Historian": {
        "persona": "역사학자",
        "summary": "SEO는 죽은 것이 아니라 검색 인터페이스가 '목록'에서 '종합 답변'으로 바뀐 것이다.",
        "body": "과거 featured snippet, knowledge panel, zero-click search 때도 'SEO 종료' 논쟁이 있었지만, 실제로는 문서 구조와 출처 신뢰를 더 엄격하게 요구하는 방향으로 진화했다. Google은 AI features에서도 foundational SEO best practices를 유지하라고 설명한다. 차이는 이제 하나의 키워드 순위가 아니라 여러 하위 질문에 걸친 증거 단위가 선택된다는 점이다.",
        "sources": [
            "https://developers.google.com/search/docs/appearance/ai-features",
            "https://developers.google.com/search/docs/fundamentals/ai-optimization-guide",
        ],
    },
    "Academic": {
        "persona": "학자",
        "summary": "RAG와 query fan-out 시대의 글은 주장·근거·한계가 명확히 분리되어야 한다.",
        "body": "Google은 AI search가 Search index 기반 RAG와 query fan-out을 활용한다고 설명한다. STORM 논문도 긴 글의 품질을 높이려면 다양한 관점의 질문과 검색 grounding이 중요하다고 본다. 이 둘을 합치면 좋은 글의 조건은 '문장 감성'보다 구조적 검증성이다. claim, evidence, caveat, next question이 분리되어야 AI와 사람이 모두 안전하게 재사용할 수 있다.",
        "sources": [
            "https://developers.google.com/search/docs/fundamentals/ai-optimization-guide",
            "https://storm-project.stanford.edu/research/storm/",
            "https://arxiv.org/abs/2402.14207",
        ],
    },
    "Futurist": {
        "persona": "미래학자",
        "summary": "블로그는 페이지가 아니라 agent가 예산을 들고 읽는 'source object'가 된다.",
        "body": "Cloudflare는 Pay per crawl의 미래를 agentic world와 연결해 설명한다. OpenAI crawler 문서도 search, training, user action을 서로 다른 user agent와 정책으로 분리한다. 앞으로 콘텐츠는 사람에게 읽히는 글인 동시에 agent가 접근권·출처·요약 가능성을 판단하는 객체가 된다. 블로그 운영자는 UI 글쓰기와 API-like governance를 동시에 설계해야 한다.",
        "sources": [
            "https://blog.cloudflare.com/introducing-pay-per-crawl/",
            "https://developers.openai.com/api/docs/bots",
        ],
    },
}


CONTRADICTIONS = [
    ["SEO는 죽었다", "Google은 AI features에서도 SEO fundamentals가 여전히 관련 있다고 설명한다", "SEO를 버리지 말고 evidence-first SEO로 재정의한다"],
    ["AI 답변은 출처 링크를 준다", "CJR/Tow Center는 publisher content 오표현 위험을 지적한다", "citation-ready 문장과 출처 QA를 함께 설계한다"],
    ["AI crawler를 막으면 보호된다", "검색 노출·학습·사용자 액션 crawler는 목적이 다르다", "robots.txt와 CDN/WAF 정책을 목적별로 분리한다"],
    ["좋은 글이면 충분하다", "query fan-out은 여러 하위 질문과 데이터 소스를 동시에 다룬다", "하나의 글 안에 FAQ·비교·절차·한계를 구조화한다"],
    ["트래픽이 줄면 끝이다", "Pay per crawl과 구독 전환은 접근권/인용 기반 수익 가능성을 보여준다", "pageview뿐 아니라 citation, subscriber, license KPI를 둔다"],
]


SYNTHESIS = """# STORM Synthesis
AI 검색 시대의 블로그 전략은 '검색엔진을 속이는 법'이 아니라 '사람과 모델이 함께 검증할 수 있는 source object를 만드는 법'으로 바뀐다.

핵심은 네 가지다. 첫째, Google의 설명처럼 기본 SEO는 여전히 필요하다. 크롤링, 색인, snippet, 내부 링크, 텍스트 가용성, visible text와 structured data의 일치는 버려도 되는 과거 기술이 아니다. 둘째, query fan-out은 하나의 키워드보다 여러 하위 질문을 동시에 다룬다. 그래서 글은 단일 주장보다 정의, 비교, 절차, FAQ, 한계, 원문 출처를 함께 가져야 한다. 셋째, ChatGPT Search와 AI Overviews가 링크를 제공하더라도 attribution 품질은 자동 보장되지 않는다. 넷째, Cloudflare의 pay per crawl은 콘텐츠가 pageview뿐 아니라 crawler access와 agentic budget의 대상이 될 수 있음을 보여준다.

따라서 좋은 블로그 글의 새 기준은 '읽기 좋은 에세이 + 검증 가능한 근거 블록 + crawler 정책 + 수익 전환 경로'다."""


PEER_REVIEW = """# STORM Peer Review
- BLOCKER 없음: 공식 문서와 비판 자료를 분리했고, 확인되지 않은 수치나 수익 효과를 단정하지 않았다.
- 주의 1: Google과 OpenAI 자료는 제품 제공자 관점이다. 낙관적 claim은 실행 지침으로 쓰되, 독립 검증이 필요한 주장으로 취급한다.
- 주의 2: Cloudflare의 Pay per crawl은 closed/private beta 성격이므로 즉시 적용 가능한 보편 표준처럼 쓰면 안 된다.
- 주의 3: CJR/Tow Center 분석은 publisher risk를 보여주는 비판 자료이며, 모든 AI search citation이 틀린다는 의미로 과장하면 안 된다.
- 주의 4: 'SEO는 죽었다/살았다'의 이분법보다, content evidence architecture로 재정의하는 결론이 더 안전하다."""


def make_storm_markdown() -> tuple[str, str, str, str]:
    scan = ["# Multi-Perspective Scan · AI 검색 시대의 블로그 생존 전략 2026"]
    for name, row in STORM_SCAN.items():
        scan.extend([
            f"## {name} · {row['persona']}",
            row["summary"],
            row["body"],
            "출처: " + ", ".join(row["sources"]),
            "",
        ])
    contradiction = "# Contradiction Map\n" + "\n".join(f"- {a} ↔ {b} → {c}" for a, b, c in CONTRADICTIONS)
    return "\n".join(scan), contradiction, SYNTHESIS, PEER_REVIEW


def build_problem(scan_md: str) -> str:
    cards = "".join(
        f'<article class="mini-card" style="padding-top:22px"><span class="tag" style="display:inline-flex;margin-bottom:16px">{esc(name)} · {esc(row["persona"])}</span><h3 style="margin-top:0;margin-bottom:12px">{esc(row["summary"])}</h3><p style="margin-top:0">{esc(row["body"])}</p></article>'
        for name, row in STORM_SCAN.items()
    )
    return f"""
{h2('01', '문제 제기 · 블로그는 이제 “페이지”가 아니라 “근거 객체”다', 'problem', 'adaptive-html-blog-writer-v2의 블로그/아티클 흐름대로, 먼저 독자가 왜 지금 읽어야 하는지 분명히 한다.')}
<p>AI Overviews, AI Mode, ChatGPT Search가 보편화되면 블로그 운영자는 같은 질문을 반복하게 된다. “검색 트래픽이 줄면 글은 끝난 걸까?” 답은 단순하지 않다. Google은 generative AI search에서도 기본 SEO가 여전히 관련 있다고 설명하고, OpenAI는 ChatGPT Search에서 출처와 Sources 패널을 보여준다. 동시에 Cloudflare와 CJR/Tow Center는 crawler 경제와 attribution 리스크를 제기한다.</p>
<p>그래서 이 글의 결론은 낙관도 비관도 아니다. <span class="hl">블로그 글은 사람에게 읽히는 글인 동시에 AI가 인용·요약·비교·검증할 수 있는 source object가 되어야 한다.</span> 예쁜 문장만으로는 부족하고, 기계가 읽을 수 있는 근거 구조만으로도 부족하다. 둘을 동시에 만족시키는 편집 설계가 필요하다.</p>
<div class="card-grid rail-cycle">{cards}</div>
{source_details('STORM Multi-Perspective Scan 원문', scan_md, open_=False)}
"""


def build_context() -> str:
    return f"""
{h2('02', '맥락 · “SEO가 끝났다”보다 더 정확한 변화', 'context', '사실, 해석, 실행을 분리해 확인되지 않은 최신성을 단정하지 않는다.')}
{table(FACT_ROWS, 'Fact / Interpretation / Action split — adaptive-html-blog-writer-v2 방식', ['근거 축', '확인 가능한 사실', '실행 해석'])}
<div class="analogy"><div class="label">비유로 이해하기</div><p>예전 블로그는 도서관 서가에 꽂힌 책에 가까웠다. 제목과 목차가 좋으면 사람이 찾아왔다. AI 검색 시대의 블로그는 도서관 책이면서 동시에 연구 조교가 인용할 카드 카탈로그다. 카드에 제목, 주장, 근거, 한계, 원문 링크가 명확해야 조교가 잘못 인용할 확률이 낮아진다.</p></div>
<div class="danger"><div class="label">함정</div><div class="name">AEO/GEO라는 새 이름만 붙이고 기존 글을 그대로 둔다</div><p>Google은 AI search 최적화를 별도 꼼수로 보지 않고, search experience 최적화의 연장으로 설명한다. 이름을 바꾸는 것보다 non-commodity content, technical eligibility, visible evidence 구조가 중요하다.</p></div>
<div class="good"><div class="label">해결</div><div class="name">증거 블록을 먼저 설계한다</div><p>정의, 비교표, 단계, FAQ, 출처, 반례, 업데이트 날짜, 저자/검토 기준을 글 안에 분리한다. 사람에게는 읽기 리듬이 되고 AI에는 인용 가능한 단위가 된다.</p></div>
"""


def build_core_argument(contradiction_md: str) -> str:
    vt = """
<div class="vt-shell">
  <div class="vt-frame">
    <div class="vt-demo"><div class="dt-q"><article class="dt-card"><div class="vt-kicker">Q1</div><h3>사람에게 먼저 가치가 있나?</h3><p class="vt-text">경험·데이터·비교·절차가 없으면 AI가 요약해도 남는 것이 없다.</p></article><div class="dt-arrow"></div><article class="dt-card"><div class="vt-kicker">Q2</div><h3>근거 단위가 분리됐나?</h3><p class="vt-text">claim, evidence, caveat, update date가 구분되어야 citation-ready다.</p></article><div class="dt-arrow"></div><article class="dt-card"><div class="vt-kicker">Q3</div><h3>crawler 정책이 분리됐나?</h3><p class="vt-text">검색 노출, 학습, 사용자 요청 접근은 같은 정책으로 다루면 안 된다.</p></article></div><div class="dt-options"><article class="dt-card"><b>Publish</b><p class="vt-text">인간 독자용 글로 발행</p></article><article class="dt-card" style="--c:var(--vt-gold)"><b>Citation Pack</b><p class="vt-text">FAQ·표·출처 허브 추가</p></article><article class="dt-card" style="--c:var(--vt-green)"><b>Govern</b><p class="vt-text">robots/CDN/crawler 정책 분리</p></article></div></div>
  </div>
</div>
"""
    rows = [[a, b, c] for a, b, c in CONTRADICTIONS]
    return f"""
{h2('03', '핵심 주장 · AI 검색용 글쓰기는 키워드가 아니라 “증거 건축”이다', 'argument', 'article_html의 1순위 vt decision-tree를 사용해 의사결정 흐름을 본문 안에 넣었다.')}
<p>이제 글 한 편은 하나의 키워드에 답하는 문서가 아니라 여러 하위 질문에 동시에 대응하는 지식 묶음이어야 한다. Google이 설명한 query fan-out은 사용자의 질문을 여러 관련 검색으로 확장한다. 이 말은 한 글이 “무엇인가”, “왜 중요한가”, “어떻게 하는가”, “무엇과 다른가”, “언제 하지 말아야 하는가”를 모두 다룰수록 선택될 접점이 늘어난다는 뜻이다.</p>
<figure aria-label="AI 검색 시대 블로그 의사결정 트리"><figcaption>vt decision-tree · 글을 발행하기 전 점검할 세 질문</figcaption>{vt}</figure>
{table(rows, 'STORM Contradiction Map — 이분법 대신 실행 기준으로 바꾸기', ['주장 A', '충돌 근거', '실행 해석'])}
{source_details('Contradiction Map 원문', contradiction_md, open_=True)}
"""


def build_case_study(synthesis_md: str) -> str:
    wg14 = """
<section class="wg-14" aria-labelledby="wg-14-title">
  <p class="wg-14-kicker">기능 안내 · Blog Source Object</p>
  <h2 id="wg-14-title" class="wg-14-h">AI 검색 시대의 블로그 리라이트 팩</h2>
  <p class="wg-14-lead">기존 글을 검색형 문서에서 citation-ready source object로 바꾸는 최소 구조입니다.</p>
  <div class="wg-14-tldr" role="note" aria-label="핵심 요약"><span class="wg-14-tldr-tag">TL;DR</span><p class="wg-14-tldr-body"><strong>글을 더 길게 쓰는 것이 아니라</strong> 주장·근거·한계·업데이트·출처를 분리해 사람이 읽고 AI가 인용하기 쉽게 만드는 작업입니다.</p></div>
  <div class="wg-14-acc">
    <details class="wg-14-sec" open><summary class="wg-14-sum"><span class="wg-14-sum-no">01</span> 무엇을 해결하나요 <span class="wg-14-chev" aria-hidden="true"></span></summary><div class="wg-14-sec-body"><p>AI 검색은 답을 조합합니다. 글 안에 근거가 섞여 있으면 일부만 잘려 나가거나 오해될 수 있습니다.</p><ul class="wg-14-list"><li>핵심 주장 3개 이하로 제한</li><li>각 주장마다 출처·반례·업데이트 날짜 명시</li><li>FAQ와 비교표를 별도 블록으로 분리</li></ul></div></details>
    <details class="wg-14-sec"><summary class="wg-14-sum"><span class="wg-14-sum-no">02</span> 동작 방식 <span class="wg-14-chev" aria-hidden="true"></span></summary><div class="wg-14-sec-body"><ol class="wg-14-flow"><li><span class="wg-14-flow-n">1</span>사람 독자용 lead를 먼저 쓴다.</li><li><span class="wg-14-flow-n">2</span>근거 표와 FAQ를 추가한다.</li><li><span class="wg-14-flow-n">3</span>crawler 정책과 source hub를 붙인다.</li></ol></div></details>
  </div>
  <h3 class="wg-14-h3">자주 묻는 질문</h3>
  <div class="wg-14-faq">
    <details class="wg-14-q" open><summary class="wg-14-q-sum">AEO/GEO를 따로 해야 하나요?</summary><p class="wg-14-q-a">Google 관점에서는 generative AI search 최적화도 Search 최적화의 연장입니다. 새 약어보다 좋은 콘텐츠와 기술 요건이 우선입니다.</p></details>
    <details class="wg-14-q"><summary class="wg-14-q-sum">출처 링크만 많으면 충분한가요?</summary><p class="wg-14-q-a">아닙니다. 출처가 어떤 주장에 연결되는지, 한계가 무엇인지, 업데이트 기준이 무엇인지가 더 중요합니다.</p></details>
  </div>
</section>
"""
    return f"""
{h2('04', '사례 · 기존 블로그 글을 7일 안에 source object로 바꾸기', 'case', 'adaptive-html-blog-writer-v2의 blog/article 필수 요소인 사례, 실행, FAQ, CTA를 한 섹션에 묶었다.')}
<p>예를 들어 “AI 영상 제작 파이프라인” 같은 긴 글이 있다고 하자. 기존 SEO 글은 제목, 서론, 도구 목록, 결론으로 끝난다. AI 검색 시대의 리라이트는 다르다. 먼저 독자가 바로 얻을 결론을 제시하고, 도구 목록을 기능별 비교표로 바꾸며, 각 주장 옆에 출처와 확인 날짜를 둔다. 그 다음 FAQ를 사용자의 follow-up question처럼 작성한다.</p>
{wg14}
{table([
    ['Day 1', '글의 핵심 주장 3개만 남기고 나머지는 FAQ/부록으로 내린다.', 'claim map'],
    ['Day 2', '각 주장에 근거 URL, 반례, 확인일을 붙인다.', 'evidence table'],
    ['Day 3', '정의·비교·절차·체크리스트 블록을 분리한다.', 'answer blocks'],
    ['Day 4', '검색 노출/학습/사용자 액션 crawler 정책을 확인한다.', 'robots/CDN note'],
    ['Day 5', 'source hub와 JSON-LD/visible text 일치 여부를 점검한다.', 'source hub'],
    ['Day 6', 'Search Console/Analytics에서 쿼리·전환·체류를 분리해 본다.', 'measurement sheet'],
    ['Day 7', '사람 독자가 읽는 흐름을 다시 다듬고 발행한다.', 'published article'],
], '7일 리라이트 플랜', ['일정', '작업', '산출물'])}
{source_details('STORM Synthesis 원문', synthesis_md, open_=False)}
"""


def build_conclusion(peer_md: str) -> str:
    return f"""
{h2('05', '결론 · 글쓰기 실력과 콘텐츠 거버넌스가 같은 일이 된다', 'conclusion', '마지막은 행동 제안과 검증 기준으로 닫는다.')}
<p>AI 검색은 블로그를 죽이지 않는다. 대신 약한 블로그를 더 빨리 무의미하게 만든다. 복붙 요약, 일반론, 출처 없는 주장, 도구 목록 나열은 AI 답변 안에서 녹아 없어지기 쉽다. 반대로 원본 경험, 비교 데이터, 명확한 절차, 출처와 한계가 있는 글은 사람이 읽어도 좋고 AI가 인용해도 덜 위험하다.</p>
<p>따라서 다음 블로그 전략은 “키워드 20개 더 넣기”가 아니다. <span class="hl blue">한 글을 작은 연구 보고서처럼 설계하고, 작은 제품 문서처럼 유지하고, 작은 라이선스 객체처럼 통제하는 것</span>이다. 이것이 adaptive-html-blog-writer-v2가 말하는 목적 중심 글쓰기와 STORM식 다관점 grounding이 만나는 지점이다.</p>
<div class="accessibility-checklist"><h3>발행 전 체크리스트</h3><ul><li>첫 3문단 안에 독자가 얻을 가치가 보이는가?</li><li>claim/evidence/caveat/update date가 분리되어 있는가?</li><li>AI answer가 잘라가도 오해되지 않는 정의·표·FAQ가 있는가?</li><li>Search 노출, training, user action crawler 정책을 구분했는가?</li><li>출처 링크가 본문을 방해하지 않고 source hub로 정리되어 있는가?</li></ul></div>
{source_details('STORM Peer Review 원문', peer_md, open_=True)}
"""


def build_takeaway() -> str:
    return f"""
{h2('06', 'Takeaway · 2026 블로그 운영 원칙 5개', 'takeaway', '독자가 바로 실행할 수 있도록 최종 요약을 작고 선명하게 남긴다.')}
<div class="card-grid rail-cycle">
  <article class="summary-card"><h3>1. SEO는 버리지 않는다</h3><p>AI 검색도 색인, 크롤링, snippet, 내부 링크, 텍스트 가용성 같은 기본 요건 위에서 동작한다.</p></article>
  <article class="summary-card"><h3>2. 키워드보다 질문 묶음</h3><p>query fan-out에 맞춰 정의, 비교, 절차, FAQ, 반례를 한 주제 클러스터로 설계한다.</p></article>
  <article class="summary-card"><h3>3. 출처는 장식이 아니다</h3><p>출처 링크를 많이 붙이는 것이 아니라 어떤 주장에 어떤 출처가 연결되는지 보여준다.</p></article>
  <article class="summary-card"><h3>4. crawler 정책을 분리한다</h3><p>검색 노출, 모델 학습, 사용자 요청 접근은 서로 다른 목적이므로 같은 차단 규칙으로 다루지 않는다.</p></article>
  <article class="summary-card"><h3>5. 수익 KPI를 넓힌다</h3><p>pageview 외에 citation, subscriber conversion, licensing/crawl access 가능성을 함께 본다.</p></article>
</div>
"""


def build_related_topics() -> str:
    return f"""
{h2('07', 'SEO Pack · 발행 가능한 제목·메타·태그', 'seo', 'adaptive-html-blog-writer-v2의 블로그/SEO 규칙에 맞춰 검색형, 클릭형, 전문가형 제목을 함께 제안한다.')}
{table([
    ['Primary keyword', 'AI 검색 블로그 전략', '검색 의도: AI Overviews/ChatGPT Search 시대 콘텐츠 운영법'],
    ['Secondary cluster', 'AI Overviews SEO, ChatGPT Search 출처, query fan-out, Pay per crawl, crawler policy', 'FAQ와 내부 링크 후보로 확장'],
    ['검색형 제목', 'AI 검색 시대의 블로그 전략: SEO는 죽지 않았고 글의 구조가 바뀐다', '과장 없는 검색 유입형'],
    ['전문가형 제목', 'Query fan-out과 Pay per crawl 이후의 콘텐츠 운영 아키텍처', 'B2B/마케터/퍼블리셔 대상'],
    ['클릭형 제목', 'AI가 답을 가져가는 시대, 블로그는 무엇으로 살아남나', '낚시성 없이 문제를 선명하게 제시'],
    ['Meta description', 'AI Overviews, ChatGPT Search, Pay per crawl 이후 블로그 글을 citation-ready source object로 바꾸는 2026 콘텐츠 전략.', '150자 안팎'],
    ['Tags', 'AI 검색, SEO, GEO, 콘텐츠 전략, ChatGPT Search, AI Overviews, Cloudflare', '플랫폼 공통 태그'],
], '발행용 SEO 세트', ['항목', '권장안', '메모'])}
<div class="try soft-cta"><h2>이번 주 실행</h2><p>가장 트래픽이 많거나 전환에 가까운 글 하나를 고르고, claim/evidence/caveat/update date 표를 추가하세요. 그 다음 FAQ 5개와 source hub를 붙이면 AI 검색 시대 리라이트의 절반은 끝납니다.</p></div>
"""


def build_source_note() -> str:
    links_html = "".join(
        f'<li><a href="{esc(src["url"])}" target="_blank" rel="noopener noreferrer">{esc(src["name"])}</a> — {esc(src["role"])}</li>'
        for src in SOURCE_LIST
    )
    return f"""
<h2>{body_icon('source')}<span class="num">08</span>Source Hub · 출처와 스킬 적용 증빙</h2>
<p class="h2-sub">출처 목록은 본문 흐름을 방해하지 않도록 별도 허브에 모았다. STORM은 solo fallback으로 수행했으며, adaptive-html-blog-writer-v2의 article/blog/SEO 품질 게이트를 현재 adaptive-html-final v{version()} 스타일에 맞춰 적용했다.</p>
<div class="source-note"><p><strong>보조 산출물:</strong> <a href="sources/storm-scan.md">storm-scan.md</a> · <a href="sources/storm-contradiction-map.md">contradiction-map.md</a> · <a href="sources/storm-synthesis.md">synthesis.md</a> · <a href="sources/storm-peer-review.md">peer-review.md</a> · <a href="sources/source-list.json">source-list.json</a> · <a href="sources/adaptive-blog-v2-application.json">blog-writer-v2 적용 기록</a></p></div>
<ol class="refs">{links_html}</ol>
"""


def copy_sources(scan_md: str, contradiction_md: str, synthesis_md: str, peer_md: str) -> dict:
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
        "topic": "AI 검색 시대의 블로그 생존 전략 2026",
        "mode": "solo-fallback-by-main-agent",
        "souls": STORM_SCAN,
        "contradictions": CONTRADICTIONS,
        "synthesis": synthesis_md,
        "peer_review": peer_md,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (SOURCES / "adaptive-blog-v2-application.json").write_text(json.dumps({
        "skill": "adaptive-html-blog-writer-v2",
        "source_package": str(BLOG_V2_PACKAGE.relative_to(ROOT)),
        "selected_mode": MODE,
        "audience": "블로그 운영자, SEO 담당자, 콘텐츠 팀, 1인 창작자",
        "format": "html",
        "platform": "generic / github-pages",
        "applied_rules": [
            "fact/opinion/inference split",
            "article lead, argument, case, takeaway",
            "SEO title/meta/tag candidates",
            "source-note/source hub for more than 6 links",
            "no external behavior JS",
        ],
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    shutil.copyfile(SKILL / "manifest.json", SOURCES / "adaptive-html-final-manifest.json")
    (SOURCES / "profile.json").write_text(json.dumps({"profile": PROFILE}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (SOURCES / "layout-placeholder-map.json").write_text(json.dumps({
        "layout": LAYOUT,
        "KICKER": "adaptive-html-blog-writer-v2 + STORM",
        "TITLE": "AI 검색 시대의 블로그 생존 전략 2026",
        "LEAD": "공개 아티클 리드",
        "PULL_QUOTE": "핵심 주장",
        "PROBLEM": "문제 제기 + STORM 관점",
        "CONTEXT": "Fact / Interpretation / Action",
        "CORE_ARGUMENT": "vt decision-tree + contradiction map",
        "CASE_STUDY": "wg-14 feature explainer + 7일 리라이트",
        "CONCLUSION": "동료 검토 + 결론",
        "TAKEAWAY": "5개 운영 원칙",
        "RELATED_TOPICS": "SEO pack",
        "SOURCE_NOTE": "source hub",
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
        "skills/adaptive-html-final/assets/layouts/magazine-article.html",
        "skills/adaptive-html-final/assets/visual-html-templates/02-decision-tree.html",
        "skills/adaptive-html-final/assets/widget-templates/14-feature-explainer.html",
        "skills/adaptive-html-final/references/writing-system.md",
        "skills/adaptive-html-final/references/layout-system.md",
        "orginal_skill/adaptive-html-blog-writer-v2.skill",
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
            "sources/adaptive-blog-v2-application.json",
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
        f'<span>adaptive-html-final v{version()}</span><span>adaptive-html-blog-writer-v2</span>'
        f'<div class="generated-row"><p class="generated-date">생성 기준: 2026-06-20 KST · STORM solo research · blog/article/SEO gates · layout-first</p>'
        f'<div class="lens-strip" aria-label="적용 렌즈"><span class="lens-strip-label">LENS</span><span class="lens-chip">SEO</span><span class="lens-chip">출처</span><span class="lens-chip">Crawler</span><span class="lens-chip">수익</span><span class="lens-chip">미래</span></div></div>'
    )
    body = layout
    replacements = {
        "{{KICKER}}": '<span class="kicker-text">adaptive-html-blog-writer-v2 × STORM Research</span>',
        "{{TITLE}}": "AI 검색 시대의 블로그 생존 전략 2026",
        "{{LEAD}}": "AI Overviews, AI Mode, ChatGPT Search, Pay per crawl 이후에도 SEO는 끝나지 않았다. 다만 블로그 글의 단위가 ‘키워드용 페이지’에서 ‘인용 가능한 근거 객체’로 바뀌고 있다.",
        "{{META}}": meta_inner,
        "{{PULL_QUOTE}}": "<p>좋은 블로그 글은 이제 읽기 좋은 에세이이면서, AI가 잘못 인용하기 어렵게 설계된 작은 연구 보고서여야 한다.</p>",
        "{{PROBLEM}}": build_problem(scan_md),
        "{{CONTEXT}}": build_context(),
        "{{CORE_ARGUMENT}}": build_core_argument(contradiction_md),
        "{{CASE_STUDY}}": build_case_study(synthesis_md),
        "{{CONCLUSION}}": build_conclusion(peer_md),
        "{{TAKEAWAY}}": build_takeaway(),
        "{{RELATED_TOPICS}}": build_related_topics(),
        "{{SOURCE_NOTE}}": build_source_note(),
    }
    for key, value in replacements.items():
        body = body.replace(key, value)
    toc = (
        '<nav class="toc-map" id="document-toc" aria-label="문서 목차"><span class="label">문서 목차</span>'
        '<p>문제 제기, 사실 분리, 핵심 주장, 사례, 결론, SEO pack으로 이동합니다.</p>'
        '<div class="toc-pills">'
        '<a class="toc-pill" href="#problem"><b>1</b>Problem</a>'
        '<a class="toc-pill" href="#context"><b>2</b>Context</a>'
        '<a class="toc-pill" href="#argument"><b>3</b>Argument</a>'
        '<a class="toc-pill" href="#case-study"><b>4</b>Case</a>'
        '<a class="toc-pill" href="#conclusion"><b>5</b>Conclusion</a>'
        '<a class="toc-pill" href="#seo-pack"><b>6</b>SEO Pack</a>'
        '<a class="toc-pill" href="#source-note"><b>7</b>Sources</a>'
        '</div></nav>'
    )
    body = body.replace('</header>\n  <aside class="pull-quote">', '</header>\n  ' + toc + '\n  <aside class="pull-quote">')
    body = body.replace('<article><section>', '<article><section id="problem">', 1)
    body = body.replace('</section><section>', '</section><section id="context">', 1)
    body = body.replace('</section><section>', '</section><section id="argument">', 1)
    body = body.replace('</section><section>', '</section><section id="case-study">', 1)
    body = body.replace('</section><section>', '</section><section id="conclusion">', 1)
    body = body.replace('<section class="box article-takeaway">', '<section class="box article-takeaway" id="takeaway">')
    body = body.replace('<section class="related-list">', '<section class="related-list" id="seo-pack">')
    body = body.replace('<aside class="source-note">', '<aside class="source-note" id="source-note">')

    title = "AI 검색 시대의 블로그 생존 전략 2026 · adaptive blog v2 STORM"
    description = f"adaptive-html-blog-writer-v2와 STORM 리서치로 만든 AI Overviews, ChatGPT Search, Pay per crawl 시대의 블로그/SEO 전략 HTML 리포트. adaptive-html-final v{version()} 스타일."
    json_ld = json.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": description,
        "inLanguage": "ko",
        "datePublished": "2026-06-20",
        "author": {"@type": "Organization", "name": "adaptive-html-final"},
        "keywords": ["AI 검색", "블로그 전략", "SEO", "ChatGPT Search", "AI Overviews", "Pay per crawl"],
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
        "AI 검색 시대의 블로그 생존 전략 2026",
        "adaptive-html-blog-writer-v2",
        "STORM",
        "회의주의자",
        "경제학자",
        "역사학자",
        "Fact / Interpretation / Action",
        "Contradiction Map",
        "SEO Pack",
        "Pay per crawl",
    ]
    missing = [x for x in required if x not in visible]
    evidence = {
        "storm_soul_count": len(STORM_SCAN),
        "source_count": len(SOURCE_LIST),
        "required_markers_missing": missing,
        "output_visible_text_chars": len(visible),
        "pass": not missing and len(visible) > 10000,
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
    print(OUT)


if __name__ == "__main__":
    main()
