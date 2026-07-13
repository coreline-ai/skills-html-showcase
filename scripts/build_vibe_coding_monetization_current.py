#!/usr/bin/env python3
"""Rebuild the STORM vibe-coding monetization report with adaptive-html-final.

This version is intentionally layout-first: it reads base.html + expert-report.html,
uses the current manifest/assets, preserves the source report text in-page, and
writes explicit content-preservation evidence so validate OK is not mistaken for
semantic completeness.
"""
from __future__ import annotations

import hashlib
import html
import json
import re
import shutil
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "adaptive-html-final"
ASSETS = SKILL / "assets"
INPUT = Path("/Users/hwanchoi/Downloads/index (1).html")
OUT = ROOT / "output" / "2026-06-19" / "vibe-coding-monetization-current-style"
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
    "summary": "idea",
    "decision": "decision",
    "architecture": "flow",
    "risk": "warning",
    "roadmap": "timeline",
    "validation": "audit",
    "check": "check",
    "source": "source",
}


class TextExtractor(HTMLParser):
    BLOCK_TAGS = {"p", "div", "section", "article", "blockquote", "ul", "ol", "li", "tr", "table", "hr"}
    HEADING_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip = 0
        self.in_li = False
        self.heading: str | None = None
        self.heading_buf: list[str] = []

    def _newline(self) -> None:
        if self.parts and not self.parts[-1].endswith("\n"):
            self.parts.append("\n")

    def handle_starttag(self, tag: str, attrs):
        tag = tag.lower()
        if tag in {"script", "style"}:
            self.skip += 1
            return
        if self.skip:
            return
        if tag in self.HEADING_TAGS:
            self._newline(); self._newline()
            self.heading = tag
            self.heading_buf = []
        elif tag == "li":
            self._newline()
            self.parts.append("- ")
            self.in_li = True
        elif tag == "br":
            self._newline()
        elif tag == "a":
            href = dict(attrs).get("href")
            if href and href.startswith("http"):
                self.parts.append(" [")
                self.parts.append(href)
                self.parts.append("] ")
        elif tag in self.BLOCK_TAGS:
            self._newline()

    def handle_endtag(self, tag: str):
        tag = tag.lower()
        if tag in {"script", "style"}:
            self.skip = max(0, self.skip - 1)
            return
        if self.skip:
            return
        if tag in self.HEADING_TAGS and self.heading == tag:
            marker = {"h1": "#", "h2": "##", "h3": "###", "h4": "####", "h5": "#####", "h6": "######"}[tag]
            txt = re.sub(r"\s+", " ", "".join(self.heading_buf)).strip()
            if txt:
                self.parts.append(f"{marker} {txt}\n")
            self.heading = None
            self.heading_buf = []
        elif tag == "li":
            self.in_li = False
            self._newline()
        elif tag in self.BLOCK_TAGS:
            self._newline()

    def handle_data(self, data: str):
        if self.skip:
            return
        data = re.sub(r"\s+", " ", data)
        if not data.strip():
            return
        if self.heading:
            self.heading_buf.append(data)
        else:
            self.parts.append(data)

    def text(self) -> str:
        txt = "".join(self.parts)
        txt = re.sub(r"[ \t]+\n", "\n", txt)
        txt = re.sub(r"\n{3,}", "\n\n", txt)
        return txt.strip()


def html_to_text(fragment: str) -> str:
    parser = TextExtractor()
    parser.feed(fragment)
    return parser.text()


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text_sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def version() -> str:
    return json.loads(read(SKILL / "manifest.json"))["version"]


def body_icon(token: str) -> str:
    svg = BODY_ICON_DATA[ICON[token]]
    return f'<span class="body-icon body-icon--sm" aria-hidden="true">{svg}</span>'


def h2(num: str, title: str, icon: str, sub: str) -> str:
    return (
        f'<h2>{body_icon(icon)}<span class="num">{esc(num)}</span>{esc(title)}</h2>'
        f'<p class="h2-sub">{esc(sub)}</p>'
    )


def section_between(source: str, section_id: str, next_section_id: str | None) -> str:
    start = source.index(f'<section id="{section_id}">')
    if next_section_id:
        end = source.index(f'<section id="{next_section_id}">', start)
    else:
        end = source.index('<footer class="prov">', start)
    return source[start:end]


def extract_souls(perspectives_html: str) -> list[dict]:
    pattern = re.compile(
        r'<article class="soul" id="(?P<id>[^"]+)">.*?'
        r'<span class="soul-name">(?P<name>.*?)</span>.*?'
        r'<span class="soul-persona">(?P<persona>.*?)</span>.*?'
        r'<p class="soul-sum">(?P<summary>.*?)</p>\s*'
        r'<div class="soul-body">(?P<body>.*?)</div>\s*</article>',
        re.S,
    )
    souls = []
    for m in pattern.finditer(perspectives_html):
        body = m.group("body")
        title_match = re.search(r"<h4>(.*?)</h4>", body, re.S)
        souls.append({
            "id": m.group("id"),
            "name": html_to_text(m.group("name")),
            "persona": html_to_text(m.group("persona")),
            "summary": html_to_text(m.group("summary")),
            "title": html_to_text(title_match.group(1)) if title_match else m.group("id"),
            "text": html_to_text(body),
        })
    return souls


def extract_report() -> dict:
    source = read(INPUT)
    title = re.search(r"<title[^>]*>(.*?)</title>", source, re.I | re.S)
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", source, re.I | re.S)
    links = sorted({m.strip() for m in re.findall(r'href=["\']([^"\']+)["\']', source, re.I) if m.strip().startswith(("http://", "https://"))})
    perspectives = section_between(source, "perspectives", "contradiction")
    contradiction = section_between(source, "contradiction", "synthesis")
    synthesis = section_between(source, "synthesis", "review")
    review = section_between(source, "review", "sources")
    sources = section_between(source, "sources", None)
    chunks = {
        "perspectives": html_to_text(perspectives),
        "contradiction": html_to_text(contradiction),
        "synthesis": html_to_text(synthesis),
        "review": html_to_text(review),
        "sources": html_to_text(sources),
    }
    all_text = "\n\n".join(chunks.values())
    headings = re.findall(r"<h([1-6])[^>]*>(.*?)</h\1>", source, re.I | re.S)
    headings = [html_to_text(h) for _, h in headings]
    return {
        "title": html_to_text(title.group(1)) if title else "STORM · 바이브코딩으로 수익화하는 방법",
        "h1": html_to_text(h1.group(1)) if h1 else "바이브코딩으로 수익화하는 방법",
        "links": links,
        "souls": extract_souls(perspectives),
        "chunks": chunks,
        "all_text": all_text,
        "headings": headings,
        "source_html_sha256": sha(INPUT),
        "source_html_bytes": INPUT.stat().st_size,
    }


def markdownish_to_html(text: str, max_lines: int | None = None) -> str:
    """Render extracted source text as readable prose instead of a giant code wall."""
    lines = text.splitlines()
    if max_lines is not None:
        lines = lines[:max_lines]
    out: list[str] = []
    in_ul = False
    in_ol = False

    def close_lists() -> None:
        nonlocal in_ul, in_ol
        if in_ul:
            out.append("</ul>")
            in_ul = False
        if in_ol:
            out.append("</ol>")
            in_ol = False

    for raw in lines:
        line = raw.strip()
        if not line:
            close_lists()
            continue
        if line.startswith("- "):
            if in_ol:
                out.append("</ol>"); in_ol = False
            if not in_ul:
                out.append("<ul>"); in_ul = True
            out.append(f"<li>{esc(line[2:])}</li>")
            continue
        m = re.match(r"^(\d+)\.\s+(.*)$", line)
        if m:
            if in_ul:
                out.append("</ul>"); in_ul = False
            if not in_ol:
                out.append("<ol>"); in_ol = True
            out.append(f"<li>{esc(m.group(2))}</li>")
            continue
        close_lists()
        if line.startswith("###### "):
            out.append(f"<h6>{esc(line[7:])}</h6>")
        elif line.startswith("##### "):
            out.append(f"<h5>{esc(line[6:])}</h5>")
        elif line.startswith("#### "):
            out.append(f"<h4>{esc(line[5:])}</h4>")
        elif line.startswith("### "):
            out.append(f"<h3>{esc(line[4:])}</h3>")
        elif line.startswith("## "):
            out.append(f"<h3>{esc(line[3:])}</h3>")
        elif line.startswith("# "):
            out.append(f"<h3>{esc(line[2:])}</h3>")
        elif line.startswith("> "):
            out.append(f"<blockquote><p>{esc(line[2:])}</p></blockquote>")
        else:
            out.append(f"<p>{esc(line)}</p>")
    close_lists()
    return "\n".join(out)


def source_details(title: str, text: str, open_: bool = False) -> str:
    open_attr = " open" if open_ else ""
    rendered = markdownish_to_html(text)
    return (
        f'<details class="source-preserve" style="margin:36px 0 0 18px;border-left:6px solid var(--accent)"{open_attr}>'
        f'<summary style="padding:20px 26px 20px 58px;display:flex;align-items:center;gap:12px;flex-wrap:wrap"><strong>{esc(title)}</strong><span class="tag">원문 보존</span></summary>'
        f'<div class="source-body" style="padding:0 28px 30px 58px">'
        f'<div style="border-left:1px solid var(--line);padding:26px 0 2px 24px">{rendered}</div>'
        f'</div></details>'
    )


def table(rows: list[list[str]], caption: str, headers: list[str]) -> str:
    head = "".join(f'<th scope="col">{esc(h)}</th>' for h in headers)
    body = "".join(
        "<tr>" + "".join((f'<th scope="row">{esc(c)}</th>' if i == 0 else f'<td>{c}</td>') for i, c in enumerate(row)) + "</tr>"
        for row in rows
    )
    return f'<div class="table-scroll"><table><caption>{esc(caption)}</caption><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def build_executive_summary(data: dict) -> str:
    return f"""
{h2('01', 'Executive Summary · 수익화 병목은 제작에서 검증·유통·운영으로 이동', 'summary', '원문 STORM 리포트의 결론을 먼저 배치했다. 핵심은 “빨리 만드는 능력”보다 돈을 받는 책임 구조를 먼저 설계해야 한다는 점이다.')}
<div class="lede-note"><span class="label">핵심 판정</span><p>바이브코딩은 제품 제작비를 낮추지만, 수익화의 병목은 고객 접근, 문제 선택, 보안·품질 검증, 환불·지원·운영 책임으로 이동한다. 따라서 “앱을 많이 만들기”가 아니라 <strong>검증 가능한 좁은 문제를 유료로 해결하는 운영 모델</strong>이 먼저다.</p></div>
<div class="card-grid rail-cycle">
  <article class="summary-card"><h3>회의주의자 경고</h3><p>METR RCT의 19% 감속, micro SaaS 92% 실패, AI 코드 취약점 2.74배, Apple 크랙다운을 수익화 내러티브의 4대 균열로 제시한다.</p></article>
  <article class="summary-card"><h3>경제학자 판독</h3><p>코딩비 하락의 이익은 도구·인프라·유통 플랫폼이 먼저 흡수하고, 개인은 고객 접근권·검증·운영 책임을 팔아야 한다.</p></article>
  <article class="summary-card"><h3>역사학자 비유</h3><p>앱스토어·노코드·부트캠프·크리에이터 경제와 유사하게 진입장벽 하락은 곧 경쟁 과잉과 플랫폼 종속을 낳았다.</p></article>
  <article class="summary-card"><h3>학술적 정리</h3><p>AI 생산성 효과는 작업 난이도와 검수 비용에 따라 달라진다. “항상 빨라진다”는 주장은 근거가 부족하다.</p></article>
  <article class="summary-card"><h3>미래학자 신호</h3><p>에이전트 앱스토어, 인스턴트 체크아웃, pay-per-crawl, 규제 강화는 기회이자 rent extraction 구조다.</p></article>
</div>
{table([
  ['희소성 변화', '코드 생성 자체의 희소성은 낮아지고, 고객 맥락·신뢰·운영 책임의 희소성이 상승한다.', '고객 인터뷰와 도메인 검증부터 시작'],
  ['수익 분포', '성공담은 power-law와 생존자 편향을 강하게 탄다.', 'MRR 캡처보다 비용·유지율·환불률을 요구'],
  ['생산성', 'AI의 이득은 작업 복잡도·코드베이스 성숙도·검수 수준에 따라 뒤집힌다.', '작업별 실제 시간 측정'],
  ['품질·보안', 'AI 생성 코드의 취약점·중복·churn 위험이 지속 수익을 위협한다.', 'trust receipt와 사람 검수 판매'],
  ['플랫폼', '유통 채널은 기회지만 수수료·정책·차단 리스크를 동반한다.', '직접 고객 리스트와 백업 결제 채널 확보'],
], '원문 전체에서 수렴한 5개 판단', ['판단', '원문 근거', '실행 기준'])}
"""


def build_decision_cards(data: dict) -> str:
    soul_cards = []
    for soul in data["souls"]:
        soul_cards.append(
            f'<article class="mini-card" style="padding-top:22px"><span class="tag" style="display:inline-flex;margin-bottom:16px">{esc(soul["name"])} · {esc(soul["persona"])}</span><h3 style="margin-top:0;margin-bottom:12px">{esc(soul["title"])}</h3><p style="margin-top:0">{esc(soul["summary"])}</p></article>'
        )
    details = "\n".join(source_details(f'{s["persona"]} 원문 전문 · {s["title"]}', s["text"], open_=i == 0) for i, s in enumerate(data["souls"]))
    return f"""
{h2('02', 'Decision Cards · 다섯 관점이 남긴 실제 의사결정 질문', 'decision', '원문의 “5 영혼”을 그대로 보존하면서 각 관점이 수익화 전략에 던지는 질문을 카드로 재배치했다.')}
<div class="card-grid rail-cycle">
  {''.join(soul_cards)}
</div>
<div class="core-insight core-insight--plain-text"><blockquote>결정 질문은 “AI로 무엇을 만들까?”가 아니라 “누가 어떤 위험을 줄이기 위해 돈을 낼까?”다.</blockquote><p>제작 속도는 진입권이고, 가격을 만드는 것은 신뢰·도메인 책임·검증 가능성이다.</p></div>
{details}
"""


def build_architecture(data: dict) -> str:
    wg16 = """
<div class="wg-16" aria-labelledby="wg-16-title">
  <header class="wg-16-head">
    <p class="wg-16-kicker">구현 계획서 · monetization operating model</p>
    <h3 id="wg-16-title" class="wg-16-h">좁은 업종 productized service → 70% 자동화 → SaaS/템플릿 확장</h3>
    <p class="wg-16-lead">원문의 방어 가능한 플레이북을 실행 순서로 바꿨다. 핵심은 먼저 팔고, 손으로 납품하고, 반복되는 70%만 제품화하는 것이다.</p>
  </header>
  <div class="wg-16-panel">
    <h3 class="wg-16-h3">마일스톤 타임라인</h3>
    <ol class="wg-16-ms">
      <li class="wg-16-ms-item wg-16-active"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">M1 · 0~30일: 유료 문제 후보 검증</span><span class="wg-16-badge wg-16-bd-active">현재 단계</span></div><p class="wg-16-ms-desc">고객 인터뷰 20건, 현재 대체 비용, 구매 승인자, 실패 비용을 확인한다.</p></div></li>
      <li class="wg-16-ms-item"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">M2 · 31~60일: concierge 납품</span><span class="wg-16-badge">예정</span></div><p class="wg-16-ms-desc">앱 없이 결과를 납품하고, 예외·승인·검수 규칙을 기록한다.</p></div></li>
      <li class="wg-16-ms-item"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">M3 · 61~90일: 반복 70% 자동화</span><span class="wg-16-badge">예정</span></div><p class="wg-16-ms-desc">반복되는 입력·변환·검수 단계만 바이브코딩으로 제품화한다.</p></div></li>
      <li class="wg-16-ms-item"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">M4 · 90일+: trust receipt 상품화</span><span class="wg-16-badge">예정</span></div><p class="wg-16-ms-desc">검수 범위, 한계, 변경 로그, SLA, 감사 흔적을 프리미엄으로 판매한다.</p></div></li>
    </ol>
    <h3 class="wg-16-h3">데이터 플로우</h3>
    <div class="wg-16-flow" aria-label="수익화 데이터 플로우">
      <div class="wg-16-fnode">고객 고통<span class="wg-16-fnode-s">대체 비용</span></div>
      <div class="wg-16-fnode wg-16-fnode-hot">유료 파일럿<span class="wg-16-fnode-s">pre-sell</span></div>
      <div class="wg-16-fnode">수작업 납품<span class="wg-16-fnode-s">concierge</span></div>
      <div class="wg-16-fnode wg-16-fnode-good">반복 자동화<span class="wg-16-fnode-s">70%</span></div>
      <div class="wg-16-fnode wg-16-fnode-q">신뢰 패키지<span class="wg-16-fnode-s">SLA·audit</span></div>
    </div>
    <h3 class="wg-16-h3">운영 리스크</h3>
    <div class="wg-16-table-wrap"><div class="table-scroll"><table class="wg-16-table"><caption>바이브코딩 수익화 운영 리스크</caption><thead><tr><th scope="col">리스크</th><th scope="col">가능성</th><th scope="col">영향</th><th scope="col">완화책</th></tr></thead><tbody>
      <tr><th scope="row">고객획득비 과소평가</th><td><span class="wg-16-lv wg-16-lv-hi">높음</span></td><td><span class="wg-16-lv wg-16-lv-hi">높음</span></td><td>앱 개발 전 선판매와 채널 테스트</td></tr>
      <tr><th scope="row">검수 없는 코드 품질 부채</th><td><span class="wg-16-lv wg-16-lv-mid">중</span></td><td><span class="wg-16-lv wg-16-lv-hi">높음</span></td><td>사람 검수, 보안 체크, trust receipt</td></tr>
      <tr><th scope="row">플랫폼 정책 변경</th><td><span class="wg-16-lv wg-16-lv-mid">중</span></td><td><span class="wg-16-lv wg-16-lv-hi">높음</span></td><td>직접 고객 리스트, 대체 결제/배포 경로</td></tr>
    </tbody></table></div></div>
  </div>
</div>
"""
    raci = table([
        ['Founder/Builder', '고객 인터뷰, 파일럿 납품, 자동화 범위 결정', '문제 웨지·가격·납품 범위'],
        ['Domain Reviewer', '업무 규칙·예외·위험 검수', '승인 규칙·오류 기준·책임 한계'],
        ['Security/QA', 'AI 생성물 보안·품질 체크', '검수표·배포 전 차단 기준'],
        ['Customer Sponsor', '예산·성과 기준·재구매 판정', '대체 비용·성공 지표'],
        ['Platform/Channel Owner', '유통·정책·수수료 리스크 관리', '백업 채널·고객 리스트'],
    ], '수익화 운영 RACI — 누가 어떤 책임을 져야 하는가', ['역할', '책임', '증빙 산출물'])
    return f"""
{h2('03', 'Operating Model · 앱보다 먼저 팔 수 있는 책임 구조', 'architecture', '전문가 리포트 모드의 필수 블록인 운영 모델/RACI와 90일 실행 계획을 포함했다.')}
{wg16}
{raci}
"""


def build_risk_matrix(data: dict) -> str:
    vt = """
<div class="vt-shell">
  <div class="vt-frame">
    <div class="rm-grid"><div class="rm-cell rm-head">가능성</div><div class="rm-cell rm-head">낮음</div><div class="rm-cell rm-head">중간</div><div class="rm-cell rm-head">높음</div><div class="rm-cell rm-head">영향 큼</div><div class="rm-cell rm-risk med">성공 사례 생존자 편향</div><div class="rm-cell rm-risk high">플랫폼 정책·수수료 변경</div><div class="rm-cell rm-risk high">검수 없는 보안/품질 부채</div><div class="rm-cell rm-head">영향 중간</div><div class="rm-cell rm-risk low">템플릿 빠른 복제</div><div class="rm-cell rm-risk med">METR 결과 과잉 전이</div><div class="rm-cell rm-risk med">고객획득비 과소평가</div><div class="rm-cell rm-head">영향 작음</div><div class="rm-cell rm-risk low">문구 과장</div><div class="rm-cell rm-risk low">가격표 부재</div><div class="rm-cell rm-risk low">데모 완성도 착시</div></div>
  </div>
</div>
"""
    contradiction_table = table([
        ['AI는 개발을 빠르게 한다', '경험 많은 개발자+성숙 코드베이스 RCT에서는 19% 느려졌다', '작업별 실제 시간·검수 비용을 분리 측정'],
        ['플랫폼은 새로운 기회다', '플랫폼은 수수료·정책·차단으로 rent를 가져간다', '직접 고객 리스트와 백업 배포 경로 병행'],
        ['비개발자도 수익화 가능하다', '디버깅·보안·운영 책임은 사라지지 않는다', '책임 한계와 사람 검수를 상품에 포함'],
        ['성공담은 가능성을 보여준다', '성공한 사람만 말하는 생존자 편향이 크다', '실패율·순수익·유지율을 함께 요구'],
        ['AI 모델은 계속 좋아진다', '규제·플랫폼·복잡도 임계값도 같이 움직인다', '모델 진보를 가격 방어로 착각하지 않기'],
    ], '원문 모순 지도 — 봉합하지 않고 남긴 충돌', ['주장 A', '주장 B', '실행 해석'])
    return f"""
{h2('04', 'Risk Matrix · 속도 신화와 운영 현실의 충돌', 'risk', 'expert_html의 1순위 vt 템플릿 risk-matrix를 원문 모순 지도에 맞춰 삽입했다.')}
<figure aria-label="바이브코딩 수익화 위험 매트릭스"><figcaption>vt risk-matrix · 원문 모순 지도를 실행 리스크로 변환</figcaption>{vt}</figure>
{contradiction_table}
{source_details('모순 지도 원문 전문', data['chunks']['contradiction'], open_=True)}
"""


def build_roadmap(data: dict) -> str:
    playbook = table([
        ['7일 복제 기능 금지', '고객 기록·승인 규칙·독점 데이터·전문가 판단처럼 90일 누적되는 자산을 설계한다.', '도메인별 검수표와 예외 DB'],
        ['좁은 업종 productized service', '처음부터 SaaS를 만들지 말고, concierge로 팔고 70%만 자동화한다.', '수작업 납품 3건과 반복 패턴'],
        ['가격은 대체 비용 기준', 'AI로 빨리 만든 시간을 기준으로 가격을 낮추지 않는다.', '고객이 직접 해결할 때 드는 시간·인건비·리스크'],
        ['신뢰 영수증 판매', '검수 범위, 한계, 로그, SLA, 감사 흔적을 차별점으로 둔다.', 'trust receipt 패키지'],
        ['채널 의존 분산', '앱스토어·마켓플레이스만 믿지 않고 직접 고객 리스트를 만든다.', '이메일 리스트·콘텐츠·파트너 채널'],
    ], '방어 가능한 플레이북 — 원문 종합을 실행 항목으로 변환', ['원칙', '실행 의미', '산출물'])
    return f"""
{h2('05', 'Priority Roadmap · 원문 종합을 90일 실행표로 바꾸기', 'roadmap', '원문 “③ 종합”의 7개 소절과 미해결 질문을 압축하지 않고, 실행 로드맵과 원문 보존 블록으로 함께 제공한다.')}
<div class="impact-grid">
  <article><strong>0~7일</strong><p>좁은 고객군, 대체 비용, 유료 의향을 검증한다.</p></article>
  <article><strong>8~30일</strong><p>앱 없이 결과 샘플과 수작업 납품으로 결제 신호를 얻는다.</p></article>
  <article><strong>31~60일</strong><p>반복되는 70%만 자동화하고 예외·승인 규칙을 쌓는다.</p></article>
  <article><strong>61~90일</strong><p>SLA·검수 로그·trust receipt를 붙여 가격 방어를 만든다.</p></article>
</div>
{playbook}
{source_details('종합 원문 전문 · 다섯 전문가가 충돌을 통과해 내린 결론', data['chunks']['synthesis'], open_=True)}
"""


def build_validation(data: dict) -> str:
    return f"""
{h2('06', 'Validation Checklist · 동료 검토에서 남은 조건부 판정', 'validation', '원문의 peer review를 검증 섹션으로 별도 보존했다. BLOCKER는 없지만 직접 실증 부재와 과잉 전이 위험을 명시한다.')}
{table([
  ['MINOR', '일부 보안·품질 수치가 블로그/기업 자료에 의존', '보안 수치는 확정값보다 신뢰 패키지 설계 근거로 사용'],
  ['MAJOR→완화', 'METR −19%를 비개발자+그린필드에 직접 전이하면 과잉 일반화', '복잡도 임계값 미측정으로 남기고 작업별 측정을 요구'],
  ['MINOR', 'Cursor/Lovable/Replit ARR은 기업 자기발표', '플랫폼/도구 회사가 이득을 먼저 가져간다는 경제학적 신호로만 사용'],
  ['MINOR', '성공담과 실패율 모두 편향 가능', '수익 약속 대신 유료 파일럿·순수익·유지율 검증으로 전환'],
  ['핵심 공백', '바이브코딩→개인 수익화 직접 종단 연구가 없음', '모든 전략 권고를 삼각측량과 실험 과제로 표기'],
], '동료 검토 지적과 이번 재구성 반영', ['등급', '검토 이슈', '반영 방식'])}
<div class="accessibility-checklist"><h3>완료 기준</h3><ul><li>원문 5개 관점, 모순 지도, 종합, 동료 검토, 출처 허브가 페이지 안에 보존되어야 한다.</li><li>최신 스킬 manifest와 CSS asset snapshot이 출력 sources에 남아야 한다.</li><li>390px/1280px 렌더에서 가로 overflow가 없어야 한다.</li><li>검증 OK만으로 끝내지 않고 content-preservation 증빙을 남겨야 한다.</li></ul></div>
{source_details('동료 검토 원문 전문', data['chunks']['review'], open_=True)}
"""


def build_final_recommendation() -> str:
    return f"""
{h2('07', 'Next Actions · 지금 할 일은 앱 완성이 아니라 유료 문제 검증', 'check', '마지막은 원문 결론을 실행 가능한 7일 루프로 닫는다.')}
<ol>
  <li><strong>Day 1:</strong> 이미 돈을 쓰는 좁은 업종과 반복 업무를 하나 고른다.</li>
  <li><strong>Day 2:</strong> 고객의 현재 대체 비용, 실패 비용, 승인자를 적는다.</li>
  <li><strong>Day 3:</strong> 앱 없이 수작업 결과 샘플을 만들어 보여준다.</li>
  <li><strong>Day 4:</strong> 반복되는 입력·변환·검수 단계만 바이브코딩으로 자동화한다.</li>
  <li><strong>Day 5:</strong> 검수표, 한계 고지, 변경 로그, SLA 초안을 작성한다.</li>
  <li><strong>Day 6:</strong> 유료 파일럿 3건을 제안하고 결제/거절 이유를 기록한다.</li>
  <li><strong>Day 7:</strong> 템플릿·체크리스트·데모를 공개하고 다음 인터뷰를 잡는다.</li>
</ol>
<p><strong>성공 기준:</strong> 첫 주의 결과는 완성 앱이 아니라 유료 의향, 납품 범위, 검수 로그, 반복 자동화 후보여야 한다.</p>
"""


def build_source_note(data: dict) -> str:
    top_links = data["links"][:18]
    links_html = "".join(f'<li><a href="{esc(u)}" target="_blank" rel="noopener noreferrer">{esc(u)}</a></li>' for u in top_links)
    return f"""
<h2>{body_icon('source')}<span class="num">08</span>Source Hub · 원본과 내용 보존 증빙</h2>
<p class="h2-sub">이 페이지는 `/Users/hwanchoi/Downloads/index (1).html`을 입력 원문으로 사용했다. 외부 조사를 새로 수행하지 않았고, 원문 링크와 전문은 sources와 본문 details에 보존했다.</p>
<div class="source-note"><p><strong>원본 제목:</strong> {esc(data['title'])} · <strong>원본 H1:</strong> {esc(data['h1'])} · <strong>고유 외부 링크:</strong> {len(data['links'])}개 · <strong>원본 HTML SHA-256:</strong> <code>{data['source_html_sha256']}</code></p><p><a href="sources/original-index.html">원본 HTML 스냅샷</a> · <a href="sources/original-text.md">원문 텍스트 전문</a> · <a href="sources/content-preservation.json">내용 보존 증빙</a> · <a href="sources/input-sources.json">출처 링크 JSON</a></p></div>
<ol class="refs">{links_html}</ol>
{source_details('통합 출처 원문 전문', data['chunks']['sources'], open_=False)}
"""


def copy_sources(data: dict) -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCES.mkdir(parents=True, exist_ok=True)
    (SOURCES / "assets").mkdir(parents=True, exist_ok=True)
    (SOURCES / "screenshots").mkdir(parents=True, exist_ok=True)
    (OUT / "pages").mkdir(parents=True, exist_ok=True)
    shutil.copyfile(INPUT, SOURCES / "original-index.html")
    (SOURCES / "original-text.md").write_text(data["all_text"] + "\n", encoding="utf-8")
    (SOURCES / "extracted-content.json").write_text(json.dumps({k: v for k, v in data.items() if k not in {"all_text"}}, ensure_ascii=False, indent=2), encoding="utf-8")
    (SOURCES / "input-sources.json").write_text(json.dumps({"source_count": len(data["links"]), "links": data["links"]}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    shutil.copyfile(SKILL / "manifest.json", SOURCES / "adaptive-html-final-manifest.json")
    (SOURCES / "profile.json").write_text(json.dumps({"profile": PROFILE}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (SOURCES / "layout-placeholder-map.json").write_text(json.dumps({
        "layout": LAYOUT,
        "KICKER": "STORM 리서치 재구성",
        "TITLE": "바이브코딩 수익화 전략 리포트",
        "SUBTITLE": "원문 STORM 리포트 재구성",
        "EXECUTIVE_SUMMARY": "핵심 수렴 판단 + 5개 판단 표",
        "DECISION_CARDS": "5개 영혼 카드 + 각 관점 원문 전문 details",
        "ARCHITECTURE": "wg-16 운영 모델 + RACI",
        "RISK_MATRIX": "vt risk-matrix + 모순 지도 원문",
        "PRIORITY_ROADMAP": "90일 플레이북 + 종합 원문",
        "VALIDATION_CHECKLIST": "동료 검토 표 + 원문",
        "FINAL_RECOMMENDATION": "7일 실행 루프",
        "SOURCE_NOTE": "원본/출처/내용보존 증빙",
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    asset_hashes = {}
    for name, _ in INLINE_ORDER:
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
        "skills/adaptive-html-final/assets/layouts/expert-report.html",
        "skills/adaptive-html-final/assets/visual-html-templates/03-risk-matrix.html",
        "skills/adaptive-html-final/assets/widget-templates/16-implementation-plan.html",
        "skills/adaptive-html-final/references/layout-system.md",
        "skills/adaptive-html-final/references/writing-system.md",
        "skills/adaptive-html-final/references/quality-gates.md",
    ]
    evidence = {
        "mode": MODE,
        "profile": PROFILE,
        "layout": LAYOUT,
        "primary_vt": PRIMARY_VT,
        "primary_wg": PRIMARY_WG,
        "section_mapping": json.loads((SOURCES / "layout-placeholder-map.json").read_text(encoding="utf-8")),
        "files": [{"path": p, "sha256": sha(ROOT / p)} for p in evidence_files if (ROOT / p).exists()],
        "user_input_snapshot": "sources/original-index.html",
        "source_html_sha256": data["source_html_sha256"],
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


def render(data: dict, integrity: dict) -> str:
    layout = read(ASSETS / "layouts" / LAYOUT)
    meta_inner = (
        f'<span>{MODE}</span><span>{LAYOUT}</span><span>profile {PROFILE}</span><span>adaptive-html-final v{version()}</span><span>원문 링크 {len(data["links"])}개</span>'
        f'<div class="generated-row"><p class="generated-date">생성 기준: 2026-06-19 KST · 원본 HTML 재구성 · layout-first</p>'
        f'<div class="lens-strip" aria-label="적용 렌즈"><span class="lens-strip-label">LENS</span><span class="lens-chip">회의주의</span><span class="lens-chip">경제학</span><span class="lens-chip">역사</span><span class="lens-chip">학술</span><span class="lens-chip">미래</span></div></div>'
    )
    body = layout
    replacements = {
        "{{KICKER}}": '<span class="kicker-text">STORM · Multi-Perspective Research Remake</span>',
        "{{TITLE}}": "바이브코딩 수익화 전략 리포트",
        "{{SUBTITLE}}": "사용자가 제공한 STORM HTML의 다중 관점·모순 지도·종합·동료 검토를 현재 adaptive-html-final 전문가 리포트 레이아웃으로 다시 구성했습니다.",
        "{{META}}": meta_inner,
        "{{EXECUTIVE_SUMMARY}}": build_executive_summary(data),
        "{{DECISION_CARDS}}": build_decision_cards(data),
        "{{ARCHITECTURE}}": build_architecture(data),
        "{{RISK_MATRIX}}": build_risk_matrix(data),
        "{{PRIORITY_ROADMAP}}": build_roadmap(data),
        "{{VALIDATION_CHECKLIST}}": build_validation(data),
        "{{FINAL_RECOMMENDATION}}": build_final_recommendation(),
        "{{SOURCE_NOTE}}": build_source_note(data),
    }
    for key, value in replacements.items():
        body = body.replace(key, value)
    # Add official toc-map immediately after header inside the layout main.
    toc = '<nav class="toc-map" aria-label="문서 목차"><span class="label">문서 목차</span><p>원문 보존 블록과 실행 판단을 함께 이동합니다.</p><div class="toc-pills"><a class="toc-pill" href="#main"><b>0</b>Header</a><a class="toc-pill" href="#executive-summary"><b>1</b>Executive Summary</a><a class="toc-pill" href="#decision-cards"><b>2</b>5 Perspectives</a><a class="toc-pill" href="#architecture"><b>3</b>Operating Model</a><a class="toc-pill" href="#risk-matrix"><b>4</b>Risk Matrix</a><a class="toc-pill" href="#roadmap"><b>5</b>Roadmap</a><a class="toc-pill" href="#validation"><b>6</b>Peer Review</a><a class="toc-pill" href="#source-note"><b>7</b>Source Hub</a></div></nav>'
    body = body.replace('</header>\n  <section class="executive-summary">', '</header>\n  ' + toc + '\n  <section class="executive-summary" id="executive-summary">')
    body = body.replace('<section class="decision-section">', '<section class="decision-section" id="decision-cards">')
    body = body.replace('<section class="architecture-map">', '<section class="architecture-map" id="architecture">')
    body = body.replace('<section class="risk-matrix">', '<section class="risk-matrix" id="risk-matrix">')
    body = body.replace('<section class="priority-roadmap">', '<section class="priority-roadmap" id="roadmap">')
    body = body.replace('<section class="validation-checklist">', '<section class="validation-checklist" id="validation">')
    body = body.replace('<section class="try">', '<section class="try" id="next-actions">')
    body = body.replace('<aside class="source-note">', '<aside class="source-note" id="source-note">')

    title = "바이브코딩 수익화 전략 리포트 · adaptive-html-final"
    description = "사용자 제공 STORM HTML을 adaptive-html-final v5.10.5 expert_html 레이아웃으로 재구성한 문서."
    json_ld = json.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": description,
        "inLanguage": "ko",
        "datePublished": "2026-06-19",
        "author": {"@type": "Organization", "name": "adaptive-html-final"},
    }, ensure_ascii=False)
    doc = read(ASSETS / "base.html")
    slots = {"{{TITLE}}": title, "{{DESCRIPTION}}": description, "{{JSON_LD_BLOCK}}": f'<script type="application/ld+json">{json_ld}</script>', "{{BODY}}": body, "{{FOOTER}}": ""}
    slots.update(css_slots(integrity))
    for key, value in slots.items():
        doc = doc.replace(key, value)
    leftovers = sorted(set(re.findall(r"{{[^}]+}}", doc)))
    if leftovers:
        raise RuntimeError(f"unresolved placeholders: {leftovers}")
    doc = re.sub(r"\n{4,}", "\n\n\n", doc)
    return doc


def content_preservation_check(data: dict, doc: str) -> dict:
    visible = html_to_text(doc)
    required = [
        "회의주의자 관점", "경제학자 관점", "역사학자 관점", "학자 관점", "미래학자 관점",
        "모순 지도", "다섯 전문가가 충돌을 통과해 내린 결론", "동료 검토", "통합 출처",
    ]
    missing = [r for r in required if r not in visible]
    result = {
        "source_text_chars": len(data["all_text"]),
        "output_visible_text_chars": len(visible),
        "source_headings_count": len(data["headings"]),
        "preserved_soul_count": len(data["souls"]),
        "required_markers_missing": missing,
        "ratio_output_to_source": round(len(visible) / max(1, len(data["all_text"])), 3),
        "pass": not missing and len(data["souls"]) == 5 and len(visible) >= len(data["all_text"]) * 0.85,
    }
    (SOURCES / "content-preservation.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not result["pass"]:
        raise RuntimeError(f"content preservation failed: {result}")
    return result


def main() -> None:
    data = extract_report()
    integrity = copy_sources(data)
    doc = render(data, integrity)
    (OUT / "index.html").write_text(doc, encoding="utf-8")
    content_preservation_check(data, doc)
    print(OUT)


if __name__ == "__main__":
    main()
