#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
SKILL = REPO / "skills" / "adaptive-html-final"
ASSETS = SKILL / "assets"

CORE_ASSETS = [
    "theme.css",
    "components.css",
    "visual-components.css",
    "layouts.css",
    "print.css",
]

INLINE_ASSETS = [
    "theme.css",
    "components.css",
    "visual-components.css",
    "widgets.css",
    "visual-html.css",
    "body-icons.css",
    "editorial-patterns.css",
    "shape-visuals.css",
    "workflow-visuals.css",
    "layouts.css",
    "print.css",
    "theme-dark.css",
]


def read_asset(name: str) -> str:
    return (ASSETS / name).read_text(encoding="utf-8")


def core_hash() -> str:
    core_css = "\n".join(read_asset(name) for name in CORE_ASSETS)
    return hashlib.sha256(core_css.encode("utf-8")).hexdigest()


def combined_style() -> str:
    marker = f"/* adaptive-html-final-core-css-sha256: {core_hash()} */"
    return marker + "\n" + "\n\n".join(read_asset(name).strip("\n") for name in INLINE_ASSETS)


def replace_style(html: str) -> str:
    style = "<style>\n" + combined_style() + "\n</style>"
    return re.sub(r"<style>[\s\S]*?</style>", lambda _m: style, html, count=1)


def set_header(html: str, kicker: str, title: str, sub: str, meta: list[str], generated: str, lenses: list[str]) -> str:
    meta_html = "".join(f"<span>{item}</span>" for item in meta)
    lens_html = "".join(f"<span class=\"lens-chip\">{item}</span>" for item in lenses)
    header = (
        "<header class=\"header\">"
        f"<div class=\"kicker\"><span class=\"kicker-text\">{kicker}</span></div>"
        f"<h1>{title}</h1>"
        f"<p class=\"sub\">{sub}</p>"
        f"<div class=\"meta\">{meta_html}</div>"
        "<div class=\"generated-row\">"
        f"<p class=\"generated-date\">{generated}</p>"
        "<div class=\"lens-strip\" aria-label=\"적용 렌즈\">"
        "<span class=\"lens-strip-label\">LENS</span>"
        f"{lens_html}"
        "</div></div></header>"
    )
    return re.sub(r"<header class=\"header\">[\s\S]*?</header>", header, html, count=1)


def insert_after(html: str, needle: str, block: str) -> str:
    if block.strip() in html:
        return html
    idx = html.find(needle)
    if idx == -1:
        raise RuntimeError(f"needle not found: {needle[:80]}")
    return html[: idx + len(needle)] + "\n" + block + html[idx + len(needle) :]


def insert_before(html: str, needle: str, block: str) -> str:
    if block.strip() in html:
        return html
    idx = html.find(needle)
    if idx == -1:
        raise RuntimeError(f"needle not found: {needle[:80]}")
    return html[:idx] + block + "\n" + html[idx:]


def content_updated(path: Path) -> bool:
    return "adaptive-html-final v5.1.0의" in path.read_text(encoding="utf-8")


def replace_once(html: str, old: str, new: str) -> str:
    if old not in html:
        raise RuntimeError(f"old block not found: {old[:100]}")
    return html.replace(old, new, 1)


def replace_regex_once(html: str, pattern: str, repl: str) -> str:
    new, n = re.subn(pattern, repl, html, count=1, flags=re.S)
    if n != 1:
        raise RuntimeError(f"pattern did not match exactly once: {pattern[:100]}")
    return new


def wrap_first_vt(html: str, slug: str, label: str) -> str:
    marker = f"template-showcase:start {slug}"
    if marker in html:
        return html
    pattern = r"(<section class=\"vt-shell\"><div class=\"vt-frame\">[\s\S]*?</section>)"
    def repl(m: re.Match[str]) -> str:
        return (
            f"\n<!-- {marker} -->\n"
            f"<div class=\"summary-card template-showcase\"><div class=\"label\">TEMPLATE CHECK · {label}</div>\n"
            f"{m.group(1)}\n"
            "</div>\n"
            f"<!-- template-showcase:end {slug} -->"
        )
    return replace_regex_once(html, pattern, repl)


def tune_numbers(html: str, key_numbers: set[int]) -> str:
    def repl(m: re.Match[str]) -> str:
        n = int(m.group(1))
        cls = "no is-key" if n in key_numbers else "no"
        return f"<span class=\"{cls}\" aria-hidden=\"true\">{n}</span>"
    return re.sub(r"<span class=\"no(?: is-key)?\"(?: aria-hidden=\"true\")?>([0-9]+)</span>", repl, html)


def a11y_block(title: str, lead: str, cards: list[tuple[str, str, str, str, str]], release: list[str]) -> str:
    card_html = []
    for area, minutes, heading, pass_text, fail_text in cards:
        card_html.append(
            "<article class=\"a11y-card\">"
            f"<div class=\"a11y-card-head\"><span>{area}</span><span class=\"a11y-time\">{minutes}</span></div>"
            f"<h4>{heading}</h4>"
            "<ul class=\"a11y-points\">"
            f"<li><span class=\"a11y-pass\">PASS</span><span>{pass_text}</span></li>"
            f"<li><span class=\"a11y-fail\">FAIL</span><span>{fail_text}</span></li>"
            "</ul></article>"
        )
    release_html = "".join(f"<li>{item}</li>" for item in release)
    return (
        "\n<section class=\"a11y-check\">"
        f"<h3 class=\"a11y-subhead\"><span class=\"a11y-subnum\">1</span>{title}</h3>"
        f"<p class=\"a11y-lead\">{lead}</p>"
        f"<div class=\"a11y-grid\">{''.join(card_html)}</div>"
        "<div class=\"a11y-rule\"><b>단일 규칙</b><p>상태와 위험도는 색만으로 전달하지 않고 PASS/FAIL/WARN 텍스트를 함께 둔다.</p></div>"
        "<h3 class=\"a11y-subhead\"><span class=\"a11y-subnum\">2</span>실패 모드와 해결</h3>"
        "<div class=\"table-scroll\"><table class=\"tbl\"><caption>접근성 실패 모드 · 증상 · 해결</caption>"
        "<thead><tr><th scope=\"col\">실패 모드</th><th scope=\"col\">증상</th><th scope=\"col\">해결</th></tr></thead>"
        "<tbody><tr><th scope=\"row\">색-단독 상태</th><td>위험과 통과가 색만으로 구분된다.</td><td>라벨과 아이콘/형태 단서를 함께 쓴다.</td></tr>"
        "<tr><th scope=\"row\">키보드 경로 누락</th><td>details, 라디오, CTA에 도달하지 못한다.</td><td>Tab 순서와 focus-visible을 확인한다.</td></tr>"
        "<tr><th scope=\"row\">제목 계층 흔들림</th><td>굵은 문장이 제목 역할을 대신한다.</td><td>h1 1개와 본문 h2 흐름을 유지한다.</td></tr></tbody></table></div>"
        "<div class=\"a11y-release\"><h3 class=\"a11y-subhead\"><span class=\"a11y-subnum\">3</span>릴리스 준비 체크</h3>"
        "<p>아래 항목이 충족되면 v5.1 proper-black 다크 테마와 긴 본문 위젯을 함께 배포할 수 있다.</p>"
        f"<ol>{release_html}</ol></div></section>"
    )


def wg13_flow(prefix: str, title: str, sub: str, nodes: list[str], fail: str, ok: str, detail: list[tuple[str, str, str]]) -> str:
    ids = [f"{prefix}-s{i}" for i in range(1, 4)]
    detail_html = []
    for did, tag, body in detail:
        detail_html.append(
            f"<details id=\"{prefix}-{did}\" class=\"wg-13-acc\" open>"
            f"<summary><span class=\"wg-13-tag\">{tag}</span>{body[0]}</summary>"
            f"<div class=\"wg-13-body\"><p>{body[1]}</p></div></details>"
        )
    return (
        "<section class=\"wg-13-fc\" aria-label=\"업무 플로우차트\">"
        f"<h3 class=\"wg-13-h\">{title} <span class=\"wg-13-sub\">{sub}</span></h3>"
        "<div class=\"wg-13-flow\">"
        f"<a href=\"#{ids[0]}\" class=\"wg-13-node wg-13-node--start\"><span class=\"wg-13-step\">시작</span>{nodes[0]}</a>"
        "<span class=\"wg-13-arrow\" aria-hidden=\"true\">&darr;</span>"
        f"<a href=\"#{ids[1]}\" class=\"wg-13-node\"><span class=\"wg-13-step\">1</span>{nodes[1]}</a>"
        "<span class=\"wg-13-arrow\" aria-hidden=\"true\">&darr;</span>"
        f"<a href=\"#{ids[2]}\" class=\"wg-13-node wg-13-node--decide\"><span class=\"wg-13-step\">2</span>{nodes[2]}</a>"
        "<div class=\"wg-13-paths\">"
        f"<div class=\"wg-13-path wg-13-path--fail\"><span class=\"wg-13-edge\">아니오 &rarr; 실패 경로</span><a href=\"#{prefix}-fail\" class=\"wg-13-node wg-13-node--fail\"><span class=\"wg-13-step\">!</span>{fail}</a></div>"
        f"<div class=\"wg-13-path wg-13-path--ok\"><span class=\"wg-13-edge\">예 &rarr; 정상 경로</span><a href=\"#{prefix}-ok\" class=\"wg-13-node wg-13-node--end\"><span class=\"wg-13-step\">완료</span>{ok}</a></div>"
        "</div></div>"
        "<div class=\"wg-13-detail\">"
        f"{''.join(detail_html)}"
        f"<details id=\"{prefix}-fail\" class=\"wg-13-acc wg-13-acc--fail\"><summary><span class=\"wg-13-tag wg-13-tag--fail\">실패</span>{fail}</summary><div class=\"wg-13-body\"><p>근거가 부족하면 조건, 문서, 통계, 파라미터, 소유자를 다시 확인한다.</p></div></details>"
        f"<details id=\"{prefix}-ok\" class=\"wg-13-acc wg-13-acc--ok\"><summary><span class=\"wg-13-tag wg-13-tag--ok\">통과</span>{ok}</summary><div class=\"wg-13-body\"><p>결정 근거와 다음 행동을 문서에 남긴다.</p></div></details>"
        "</div></section>"
    )


def update_beginner(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = set_header(
        html,
        "BEGINNER HTML · LOCAL RAG",
        "로컬 RAG 개인 지식 금고 입문",
        "메모, PDF, 링크를 질문 가능한 개인 지식 금고로 바꾸는 첫 설계. 서재·사서·책갈피 비유로 검색-근거-답변 흐름을 잡는다.",
        ["beginner_html", "beginner-learning.html", "profile auto", "adaptive-html-final v5.1.0", "무 JS"],
        "Generated · 2026-06-05 08:34 KST",
        ["서재 비유", "근거 우선", "문서 10개", "질문 20개", "상위 근거 3개"],
    )
    html = insert_after(
        html,
        "</section>\n<section class=\"vt-shell\"><div class=\"vt-frame\"><div class=\"concept-ring\"",
        "<div class=\"lede-note\"><span class=\"label\">Goal</span><p>이 글의 목표는 멋진 챗봇을 완성하는 것이 아니라, 검색된 근거를 읽고 고치는 감각을 만드는 것이다.</p></div>\n<section class=\"vt-shell\"><div class=\"vt-frame\"><div class=\"concept-ring\"",
    ).replace("</section>\n<section class=\"vt-shell\"><div class=\"vt-frame\"><div class=\"concept-ring\"\n<div class=\"lede-note\"", "</section>\n<div class=\"lede-note\"")
    html = html.replace("<div class=\"lede-note\"><span class=\"label\">Goal</span><p>이 글의 목표는 멋진 챗봇을 완성하는 것이 아니라, 검색된 근거를 읽고 고치는 감각을 만드는 것이다.</p></div>\n<section class=\"vt-shell\"><div class=\"vt-frame\"><div class=\"concept-ring\"", "<div class=\"lede-note\"><span class=\"label\">Goal</span><p>이 글의 목표는 멋진 챗봇을 완성하는 것이 아니라, 검색된 근거를 읽고 고치는 감각을 만드는 것이다.</p></div>\n<section class=\"vt-shell\"><div class=\"vt-frame\"><div class=\"concept-ring\"")
    html = wrap_first_vt(html, "vt-15 concept-explainer", "vt-15 concept-explainer")
    html = tune_numbers(html, {1, 9})
    html = replace_once(
        html,
        "<p>처음부터 완벽한 크기를 찾으려 하지 않는다. 질문 20개를 만든 뒤, 각 질문에서 상위 검색 결과 3개가 납득되는지 보며 조정한다. 청크 설계는 숫자 맞추기가 아니라 검색 결과를 읽고 고치는 반복 작업이다.</p></section>",
        "<p>처음부터 완벽한 크기를 찾으려 하지 않는다. 질문 20개를 만든 뒤, 각 질문에서 상위 검색 결과 3개가 납득되는지 보며 조정한다. 청크 설계는 숫자 맞추기가 아니라 검색 결과를 읽고 고치는 반복 작업이다.</p>"
        "<div class=\"ba\"><div class=\"ba-col before\"><span class=\"ba-label\">Before</span><p>문서를 500자마다 기계적으로 자른다.</p></div><div class=\"ba-arrow\" aria-hidden=\"true\">&rarr;</div><div class=\"ba-col after\"><span class=\"ba-label\">After</span><p>질문 하나에 답할 만큼 제목·문맥·출처를 함께 보존한다.</p></div></div></section>",
    )
    html = replace_once(
        html,
        "<p>검색 실패의 원인은 여러 가지다. 문서 자체가 없을 수 있고, 청크가 너무 잘게 잘렸을 수 있으며, 질문 표현과 문서 표현이 다를 수 있다. 원인을 나눠야 모델 튜닝, 청크 수정, 문서 보강 중 무엇을 해야 할지 결정할 수 있다.</p>\n\n\n<!-- template-showcase:start wg-13 annotated-flowchart -->",
        "<p>검색 실패의 원인은 여러 가지다. 문서 자체가 없을 수 있고, 청크가 너무 잘게 잘렸을 수 있으며, 질문 표현과 문서 표현이 다를 수 있다. 원인을 나눠야 모델 튜닝, 청크 수정, 문서 보강 중 무엇을 해야 할지 결정할 수 있다.</p>"
        "<div class=\"core-insight core-insight--neutral\"><blockquote>답변을 평가하기 전에 검색 조각부터 읽는다.</blockquote><p>RAG의 첫 품질 게이트는 모델이 아니라 회수된 근거다.</p></div>\n\n\n<!-- template-showcase:start wg-13 annotated-flowchart -->",
    )
    a11y = a11y_block(
        "초보자 산출물 접근성 30분 점검",
        "접기 위젯, 라디오 교보재, 다크 CTA가 섞여 있으므로 색·키보드·제목 구조를 함께 확인한다.",
        [
            ("키보드", "8분", "details/라디오/CTA 접근", "모든 details와 라디오 위젯에 Tab으로 도달", "마우스로만 열리는 정보가 있음"),
            ("대비", "7분", "렌즈 칩과 다크 CTA", "meta chip과 lens-chip이 AA 대비 유지", "흐린 칩 텍스트가 배경에 묻힘"),
            ("구조", "10분", "템플릿 텍스트 노출", "h1 1개와 vt/wg 텍스트가 DOM에 노출", "도식이 이미지처럼만 보임"),
        ],
        ["상위 검색 조각 3개는 텍스트로도 읽힌다.", "상태 라벨은 PASS/FAIL/WARN 텍스트를 병기한다.", "모든 입력·details·CTA에 가시 포커스가 있다.", "무 JS 원칙을 유지한다."],
    )
    html = insert_after(html, "<!-- template-showcase:end wg-15 concept-explainer -->", a11y)
    html = replace_once(
        html,
        "<section class=\"try\"><div class=\"label\">NEXT ACTION</div><h2>바로 실행할 일</h2><ol><li>반복해서 다시 찾는 문서 10개를 고른다.</li><li>사실 확인형, 비교형, 절차형, 원인 분석형 질문 20개를 만든다.</li><li>각 질문의 기대 근거 문단을 표시한다.</li><li>상위 검색 결과 3개부터 채점한다.</li><li>로컬/원격 처리 단계를 표로 분리한다.</li></ol></section>",
        "<section class=\"try\"><div class=\"label\">NEXT ACTION</div><h2>오늘 30분 안에 만드는 첫 지식 금고</h2><p>오늘의 목표는 완성된 챗봇이 아니라, 질문 20개와 검색 결과 확인표 1개다.</p><ol><li>반복해서 다시 찾는 문서 10개를 고른다.</li><li>각 문서에 제목·날짜·출처·원문 위치를 붙인다.</li><li>사실 확인형·비교형·절차형·원인 분석형 질문 20개를 만든다.</li><li>질문마다 상위 검색 조각 3개를 먼저 읽는다.</li><li>답변에는 출처, 한계, 모르는 부분을 함께 남긴다.</li></ol></section>",
    )
    html = replace_once(
        html,
        "<aside class=\"source-note\"><div class=\"label\">Source Note</div><p>전담 beginner_html 에이전트의 초보자 교육 설계를 바탕으로 확장했다. 특정 벤더 성능, 가격, 최신 수치 주장은 넣지 않았다.</p></aside>",
        "<aside class=\"source-note\"><div class=\"label\">Source Note</div><p>전담 beginner_html 에이전트 결과를 반영해 adaptive-html-final v5.1.0의 generated-row/lens-strip, lede-note, before-after, core-insight, a11y-checklist 패턴으로 재보강했다.</p></aside>",
    )
    path.write_text(html, encoding="utf-8")


def update_expert(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = set_header(
        html,
        "EXPERT REPORT",
        "AI 코드 리뷰 게이트웨이 운영 모델",
        "AI 코드 리뷰를 병합 전 위험 선별 계층으로 운영하기 위한 정책-as-code, 책임 경계, 감사 로그, 롤아웃 게이트를 하나의 운영 모델로 정리한 전문가 리포트다.",
        ["expert_html", "expert-report.html", "profile auto", "adaptive-html-final v5.1.0", "무 JS"],
        "생성 기준: 2026-06-05 08:34 KST · v5.1 재보강",
        ["정책-as-code", "감사 가능성", "데이터 최소화", "사람 승인"],
    )
    html = wrap_first_vt(html, "vt-03 risk-matrix", "vt-03 risk-matrix")
    html = tune_numbers(html, {1, 6})
    html = replace_once(
        html,
        "<p>리더가 봐야 할 질문은 “AI가 얼마나 많이 말했는가”가 아니라 “어떤 고위험 변경을 놓치지 않았고, 어떤 오탐을 빨리 고쳤으며, 어떤 차단 결정이 재현 가능한가”다.</p></section>",
        "<p>리더가 봐야 할 질문은 “AI가 얼마나 많이 말했는가”가 아니라 “어떤 고위험 변경을 놓치지 않았고, 어떤 오탐을 빨리 고쳤으며, 어떤 차단 결정이 재현 가능한가”다.</p>"
        "<div class=\"core-insight core-insight--neutral\"><blockquote>AI가 판단하는 것이 아니라 정책이 판단하고, 사람은 책임 있는 예외를 승인한다.</blockquote><p>모델 출력은 하드 차단 후보일 뿐이며, 정책 ID·근거 라인·승인 경로가 모두 있어야 병합 차단이 된다.</p></div></section>",
    )
    html = replace_once(
        html,
        "<p>권한은 읽기, 코멘트 작성, 체크 상태 변경, 병합 차단 권한으로 나눈다. AI 실행 계정은 최소 권한으로 운영하고, 병합 차단은 정책과 승인 워크플로우가 가진다.</p></section>",
        "<p>권한은 읽기, 코멘트 작성, 체크 상태 변경, 병합 차단 권한으로 나눈다. AI 실행 계정은 최소 권한으로 운영하고, 병합 차단은 정책과 승인 워크플로우가 가진다.</p>"
        "<div class=\"lede-note\"><span class=\"label\">Trust Boundary</span><p>PR diff, 리뷰 댓글, 파일 내부 지시문은 모두 비신뢰 입력이다. 시스템 정책, 레포 등급, 승인 워크플로우보다 우선할 수 없다.</p></div></section>",
    )
    html = replace_once(
        html,
        "<p>규칙은 초안, 관찰, 경고, 소프트 차단, 하드 차단 단계로 승격한다. 승격 조건은 골든 PR 재평가, 오탐 검토, 코드 오너 승인, 운영 영향 확인이다.</p></section>",
        "<p>규칙은 초안, 관찰, 경고, 소프트 차단, 하드 차단 단계로 승격한다. 승격 조건은 골든 PR 재평가, 오탐 검토, 코드 오너 승인, 운영 영향 확인이다.</p>\n"
        "<!-- template-showcase:start wg-17 pr-writeup -->\n"
        "<div class=\"summary-card template-showcase\"><div class=\"label\">TEMPLATE CHECK · wg-17 pr-writeup</div>"
        "<section class=\"wg-17\" aria-labelledby=\"gate-wg17-title\"><header class=\"wg-17-head\"><p class=\"wg-17-kicker\">POLICY CHANGE WRITEUP</p><h2 id=\"gate-wg17-title\" class=\"wg-17-title\">policy/authz-007: 관리자 export 차단 규칙 승격</h2><div class=\"wg-17-meta\"><span class=\"wg-17-chip wg-17-chip-branch\">draft &rarr; soft-block</span><span class=\"wg-17-chip wg-17-chip-add\">+evidence_required</span><span class=\"wg-17-chip wg-17-chip-del\">-comment-only</span></div></header>"
        "<div class=\"wg-17-block\"><h3 class=\"wg-17-h3\"><span class=\"wg-17-h3-no\">1</span> Before / After</h3><div class=\"wg-17-ba\"><div class=\"wg-17-ba-col wg-17-ba-before\"><p class=\"wg-17-ba-tag\">Before</p><ul class=\"wg-17-ba-list\"><li>코멘트만 남김</li><li>승인 경로 없음</li><li>evidence 필드 임의</li></ul></div><div class=\"wg-17-ba-arrow\" aria-hidden=\"true\">&rarr;</div><div class=\"wg-17-ba-col wg-17-ba-after\"><p class=\"wg-17-ba-tag\">After</p><ul class=\"wg-17-ba-list\"><li>soft-block 판정</li><li>code owner 승인</li><li>evidence_required 고정</li></ul></div></div></div>"
        "<div class=\"wg-17-block\"><h3 class=\"wg-17-h3\"><span class=\"wg-17-h3-no\">2</span> 파일별 워크스루</h3><details class=\"wg-17-file\" open><summary class=\"wg-17-summary\"><span class=\"wg-17-file-name\">policies/authz-007.yaml</span><span class=\"wg-17-file-stat\"><span class=\"wg-17-add\">승격</span></span><span class=\"wg-17-caret\" aria-hidden=\"true\"></span></summary><div class=\"wg-17-file-body\"><p class=\"wg-17-p\">관리자 export 경로는 권한 검증 근거와 감사 이벤트를 동시에 요구한다.</p></div></details><details class=\"wg-17-file\"><summary class=\"wg-17-summary\"><span class=\"wg-17-file-name\">exceptions/export-admin.yaml</span><span class=\"wg-17-file-stat\"><span class=\"wg-17-add\">만료일</span></span><span class=\"wg-17-caret\" aria-hidden=\"true\"></span></summary><div class=\"wg-17-file-body\"><p class=\"wg-17-p\">예외는 위험 수용 기록이며 만료일 없는 예외는 정책 위반으로 본다.</p></div></details></div></section></div>\n"
        "<!-- template-showcase:end wg-17 pr-writeup -->\n</section>",
    )
    a11y = a11y_block(
        "게이트웨이 접근성 30분 점검",
        "PR 노트 점프, details, CTA, override 경로가 길게 섞이므로 색 외 단서와 키보드 경로를 함께 잠근다.",
        [
            ("키보드", "8분", "PR 노트 점프와 details", "노트 점프, details, CTA까지 Tab으로 도달", "마우스 클릭 없이는 override 사유를 열 수 없음"),
            ("대비·상태", "7분", "critical/warn/PASS/FAIL 병기", "심각도는 텍스트 라벨과 형태 단서를 함께 가짐", "critical이 색만으로 표현됨"),
            ("구조", "10분", "표 caption과 도식 텍스트", "h1 1개, 표 caption, vt/wg 텍스트가 DOM에 있음", "도식 컨테이너에 role=img로 텍스트가 묻힘"),
        ],
        ["키보드 전 경로와 가시 포커스를 확인한다.", "AA 대비와 비색 단서를 확인한다.", "모든 표는 caption과 table-scroll을 가진다.", "동작 JS 0을 유지한다."],
    )
    html = insert_after(html, "<!-- template-showcase:end wg-12 incident-timeline -->", a11y)
    html = replace_once(
        html,
        "<section class=\"try\"><div class=\"label\">NEXT ACTION</div><h2>바로 실행할 일</h2><ol><li>최근 PR 100개로 관찰 모드 기준선을 만든다.</li><li>정책 규칙의 최소 필드를 코드로 정의한다.</li><li>하드 차단 후보를 보안·데이터·인증 영역으로 제한한다.</li><li>예외 승인과 감사 로그 필수 필드를 먼저 구현한다.</li><li>모델 변경 시 골든 PR 재평가를 운영 캘린더에 넣는다.</li></ol></section>",
        "<section class=\"try\"><div class=\"label\">NEXT ACTION</div><h2>관찰 모드 30일을 먼저 잠근다</h2><p>최근 PR 100개로 기준선을 만들고, 정책 최소 필드와 감사 로그 필드를 먼저 코드화한다. 차단 권한은 지표와 승인 경로가 안정된 뒤 부여한다.</p><ol><li>최근 PR 100개 기준선을 만든다.</li><li>정책 최소 필드 8개를 점검한다.</li><li>고심각 finding 정밀도와 override 사유 품질을 같이 본다.</li><li>감사 로그 완전성을 릴리스 게이트로 둔다.</li><li>모델 변경 시 골든 PR 재평가를 운영 캘린더에 넣는다.</li></ol></section>",
    )
    html = replace_once(
        html,
        "<aside class=\"source-note\"><div class=\"label\">Source Note</div><p>전담 expert_html 에이전트의 운영 모델을 바탕으로 확장했으며, 보안 개발 통제 관점은 NIST SSDF와 OWASP SAMM 계열의 일반 원칙에 맞춰 서술했다.</p></aside>",
        "<aside class=\"source-note\"><div class=\"label\">Source Note</div><p>전담 expert_html 에이전트 결과를 반영해 adaptive-html-final v5.1.0의 generated-row/lens-strip, wg-17 policy writeup, a11y-checklist, proper-black dark CSS를 적용했다.</p></aside>",
    )
    path.write_text(html, encoding="utf-8")


def update_article(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = set_header(
        html,
        "ARTICLE HTML",
        "작은 팀의 운영 문서는 어떻게 제품 속도를 바꾸는가",
        "작은 팀에서 문서화가 느린 행정이 아니라 반복 판단을 줄이는 운영 설계가 되는 순간을 다룬 공개 아티클이다.",
        ["article_html", "magazine-article.html", "profile auto", "adaptive-html-final v5.1.0", "무 JS"],
        "Generated · 2026-06-05 08:34 KST · v5.1.0 refresh",
        ["반복 판단", "결정 기준", "소유자/폐기", "제품 속도"],
    )
    html = wrap_first_vt(html, "vt-02 decision-tree", "vt-02 decision-tree")
    html = tune_numbers(html, {7})
    html = insert_before(
        html,
        "<!-- template-showcase:start vt-02 decision-tree -->",
        "<div class=\"lede-note\"><span class=\"label\">LEDE</span><p>이 글의 질문은 문서를 더 많이 쓰자는 것이 아니다. 작은 팀이 같은 판단을 매번 새로 하지 않도록, 어떤 기준을 한 화면에 남겨야 제품 속도가 유지되는지를 묻는다.</p></div>"
        "<div class=\"source-preserve source-preserve-static\" role=\"group\" aria-labelledby=\"article-source-rule\"><div id=\"article-source-rule\" class=\"source-preserve-title\">작성 전제 보존 · article source</div><div class=\"source-body\"><p><strong>운영 문서 기준:</strong> 운영 문서는 지식 보관소가 아니라 반복 판단을 줄이는 기준선이다. 배포, 장애, 고객 응대, 온보딩처럼 다시 등장하는 질문을 중심으로 설명한다.</p></div></div>",
    )
    html = replace_once(
        html,
        "<p>이 네 가지가 없으면 문서는 설명문이 된다. 설명문은 읽을 수는 있지만 행동을 바꾸지 못한다.</p></section>",
        "<p>이 네 가지가 없으면 문서는 설명문이 된다. 설명문은 읽을 수는 있지만 행동을 바꾸지 못한다.</p>"
        "<figure class=\"md-excerpt\"><figcaption>운영 문서 1페이지 골격 · markdown excerpt</figcaption><pre class=\"code\"><code>## 운영 문서 최소 골격\n- 사용 상황:\n- 결정 기준:\n- 예외:\n- 소유자:\n- 폐기 조건:\n- 다음 점검일:</code></pre></figure></section>",
    )
    a11y = a11y_block(
        "30분 문서 접근성 점검",
        "공개 아티클은 decision-tree, 표, 링크, CTA가 길게 이어지므로 텍스트 분기와 키보드 경로를 함께 확인한다.",
        [
            ("키보드/링크", "8분", "목차·표·접힌 정보 접근", "목차·표·접힌 정보에 도달 가능", "마우스로만 열리는 정보가 있음"),
            ("대비/상태", "7분", "PASS/FAIL/WARN 병기", "상태 텍스트가 색과 함께 표시됨", "위험·정상이 색만으로 표시됨"),
            ("구조/제목", "10분", "h1 1개와 h2 흐름", "h1 1개, h2 10개, 표 caption 있음", "굵은 문장으로 제목을 대신함"),
        ],
        ["decision-tree는 텍스트로도 같은 분기를 설명한다.", "CTA는 충분한 터치 영역을 가진다.", "모션 없이도 모든 정보가 이해된다.", "표는 table-scroll로 감싼다."],
    )
    html = replace_once(
        html,
        "<p>해법은 단순하다. 모든 운영 문서에는 소유자, 마지막 업데이트 시점, 폐기 조건이 있어야 한다.</p></section>",
        "<p>해법은 단순하다. 모든 운영 문서에는 소유자, 마지막 업데이트 시점, 폐기 조건이 있어야 한다.</p>" + a11y + "</section>",
    )
    new_wg13 = (
        "<!-- template-showcase:start wg-13 annotated-flowchart -->\n"
        "<div class=\"summary-card template-showcase\"><div class=\"label\">TEMPLATE CHECK · wg-13 annotated-flowchart</div>"
        + wg13_flow(
            "article-wg13",
            "다음 결정에서 문서를 쓰는 흐름",
            "반복 질문을 기준 문서로 전환",
            ["반복 질문 발생", "기존 기준 확인", "기준이 맞는가?"],
            "임시 결정 + 갱신 요청",
            "기준 적용 + 결정 기록 업데이트",
            [
                ("s1", "질문", ("반복 질문 식별", "지난 2주간 세 번 이상 등장한 질문만 후보로 올린다.")),
                ("s2", "기준", ("기존 기준 확인", "이미 문서가 있으면 소유자와 폐기 조건이 최신인지 먼저 본다.")),
                ("s3", "판정", ("기준 적합성 판단", "조건·예외·담당자로 설명 가능하면 운영 문서로 유지한다.")),
            ],
        )
        + "</div>\n<!-- template-showcase:end wg-13 annotated-flowchart -->"
    )
    html = replace_regex_once(
        html,
        r"<!-- template-showcase:start wg-17 pr-writeup -->[\s\S]*?<!-- template-showcase:end wg-17 pr-writeup -->",
        new_wg13,
    )
    html = replace_once(
        html,
        "<section class=\"try\"><div class=\"label\">NEXT ACTION</div><h2>바로 실행할 일</h2><ol><li>지난 2주간 반복된 질문 5개를 적는다.</li><li>실패 비용이 큰 질문 2개만 한 화면 문서로 만든다.</li><li>첫 문단을 “이 문서는 언제 쓰는가”로 시작한다.</li><li>각 문서에 소유자와 폐기 조건을 붙인다.</li><li>다음 회의에서 문서를 실제로 열어 기준으로 사용한다.</li></ol></section>",
        "<section class=\"try\"><div class=\"label\">NEXT ACTION</div><h2>이번 주에는 문서 2개만 고른다</h2><p>지난 2주간 세 번 이상 반복된 질문 중 실패 비용이 큰 2개를 고르고, 사용 상황·중단 기준·소유자·폐기 조건만 먼저 쓴다.</p><ol><li>반복 질문 5개를 적는다.</li><li>실패 비용이 큰 질문 2개를 고른다.</li><li>첫 문단을 “이 문서는 언제 쓰는가”로 시작한다.</li><li>각 문서에 소유자와 폐기 조건을 붙인다.</li><li>다음 회의에서 문서를 실제로 열어 기준으로 사용한다.</li></ol></section>",
    )
    html = replace_once(
        html,
        "<aside class=\"source-note\"><div class=\"label\">Source Note</div><p>전담 article_html 에이전트의 공개 아티클 구조를 바탕으로 확장했다. 특정 회사의 내부 지표가 아니라 작은 팀 운영 원칙을 일반화한 예시다.</p></aside>",
        "<aside class=\"source-note\"><div class=\"label\">Source Note</div><p>전담 article_html 에이전트 결과를 반영해 adaptive-html-final v5.1.0의 lede-note, source-preserve, md-excerpt, a11y-checklist, 권장 wg-13 플로우를 적용했다.</p></aside>",
    )
    path.write_text(html, encoding="utf-8")


def update_education(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = set_header(
        html,
        "COURSE MODULE",
        "PostgreSQL 쿼리 플랜 읽기 3주 교육 모듈",
        "EXPLAIN과 EXPLAIN ANALYZE를 숫자 암기가 아니라 실행 경로와 병목 가설을 읽는 도구로 배우는 실습 중심 커리큘럼이다.",
        ["education_html", "course-module.html", "profile auto", "adaptive-html-final v5.1.0", "무 JS"],
        "생성 기준: 2026-06-05 08:34 KST · v5.1 재보강",
        ["3주 실습형", "EXPLAIN 중심", "무 JS", "평가 루브릭 포함"],
    )
    html = wrap_first_vt(html, "vt-04 timeline", "vt-04 timeline")
    html = tune_numbers(html, {1, 10})
    html = replace_once(
        html,
        "<p>학습자는 `EXPLAIN`, `EXPLAIN ANALYZE` 결과에서 scan, join, sort, aggregate 노드를 구분하고, 예상 row와 실제 row의 차이를 근거로 병목 가설을 세운다.</p></section>",
        "<p>학습자는 <code>EXPLAIN</code>, <code>EXPLAIN ANALYZE</code> 결과에서 scan, join, sort, aggregate 노드를 구분하고, 예상 row와 실제 row의 차이를 근거로 병목 가설을 세운다.</p>"
        "<div class=\"summary-card template-showcase\"><div class=\"label\">TEMPLATE CHECK · wg-15 concept-explainer</div><section class=\"wg-15\" aria-labelledby=\"edu-wg15-title\"><p class=\"wg-15-kicker\">개념 교보재 · 플랜 독해</p><h2 id=\"edu-wg15-title\" class=\"wg-15-h\">쿼리 플랜을 읽는 4단계 사고법</h2><p class=\"wg-15-lead\">노드 이름을 외우기보다 한 단계씩 근거를 좁힌다.</p><div class=\"concept-steps\"><div class=\"concept-step\"><b>1</b>노드 식별</div><div class=\"concept-step\"><b>2</b>row 차이 확인</div><div class=\"concept-step\"><b>3</b>병목 가설 수립</div><div class=\"concept-step\"><b>4</b>단일 변경 실험</div></div></section></div></section>",
    )
    html = replace_once(
        html,
        "</tbody></table></div></section>\n<section><h2><span class=\"no\" aria-hidden=\"true\">3</span>실행 계획 기본 문법</h2>",
        "</tbody></table></div><div class=\"summary-card template-showcase\"><div class=\"label\">TEMPLATE CHECK · wg-08 static-stepper</div><div class=\"wg-08-static\" aria-label=\"쿼리 플랜 학습 흐름\"><div class=\"wg-08-static-step wg-08-static-step--hot\"><span class=\"wg-08-static-no\">1</span><div><h3>읽기</h3><p>용어를 외우지 않고 같은 쿼리를 다른 조건에서 다시 읽는다.</p></div></div><div class=\"wg-08-static-step\"><span class=\"wg-08-static-no\">2</span><div><h3>비교</h3><p>같은 쿼리를 다른 인덱스, 조건, 파라미터로 비교한다.</p></div></div><div class=\"wg-08-static-step\"><span class=\"wg-08-static-no\">3</span><div><h3>진단</h3><p>row estimate 차이와 loops를 근거로 병목 후보를 세운다.</p></div></div><div class=\"wg-08-static-step wg-08-static-step--ok\"><span class=\"wg-08-static-no\">4</span><div><h3>발표</h3><p>변경 전후 플랜과 남은 리스크를 동료에게 설명한다.</p></div></div></div></div></section>\n<section><h2><span class=\"no\" aria-hidden=\"true\">3</span>실행 계획 기본 문법</h2>",
    )
    new_flow = (
        "<!-- template-showcase:start wg-13 annotated-flowchart -->\n"
        "<div class=\"summary-card template-showcase\"><div class=\"label\">TEMPLATE CHECK · wg-13 annotated-flowchart</div>"
        + wg13_flow(
            "edu-wg13",
            "느린 쿼리 개선 플로우",
            "근거 불충분 시 재확인",
            ["쿼리 선택", "변경 전 플랜 캡처", "row estimate 차이가 충분한가?"],
            "통계/파라미터/캐시 재확인",
            "단일 변경 적용 후 비교",
            [
                ("s1", "선택", ("느린 쿼리 선택", "실제 사용 빈도와 영향이 있는 쿼리 하나만 고른다.")),
                ("s2", "캡처", ("변경 전 플랜 캡처", "SQL, 파라미터 성격, 실행 환경, 측정 시점을 함께 남긴다.")),
                ("s3", "근거", ("row estimate 차이 확인", "예상 rows와 실제 rows, loops, actual time을 함께 읽는다.")),
            ],
        )
        + "</div>\n<!-- template-showcase:end wg-13 annotated-flowchart -->"
    )
    html = replace_regex_once(
        html,
        r"<!-- template-showcase:start wg-13 annotated-flowchart -->[\s\S]*?<!-- template-showcase:end wg-13 annotated-flowchart -->",
        new_flow,
    )
    a11y = a11y_block(
        "교육 자료 접근성 30분 점검",
        "긴 강의 자료는 radio, details, table, dark CTA가 함께 쓰이므로 수강자가 키보드와 다크 모드에서도 같은 정보를 얻어야 한다.",
        [
            ("키보드", "8분", "라디오·details·앵커 흐름", "모든 라디오·details·앵커 흐름을 Tab으로 이동", "학습 흐름이 마우스로만 작동"),
            ("대비", "7분", "proper-black 다크 대비", "본문·칩·상태 라벨이 AA 대비 유지", "다크에서 상태 라벨이 흐림"),
            ("구조", "10분", "h1/h2/table 구조", "h1 1개, h2 번호 1-10, 표 caption과 table-scroll 있음", "표 제목이나 번호 흐름이 사라짐"),
        ],
        ["색만으로 상태를 구분하지 않는다.", "PASS/FAIL/WARN 텍스트를 병기한다.", "모든 표는 caption이 있다.", "EXPLAIN ANALYZE 안전 주의 문구를 유지한다."],
    )
    html = insert_after(html, "<!-- template-showcase:end wg-20 prompt-tuner -->", a11y)
    html = replace_once(
        html,
        "<tbody><tr><td>플랜 독해</td><td>노드와 실행 흐름을 구분한다.</td><td>상위/하위 노드의 입력 관계를 설명한다.</td></tr><tr><td>병목 가설</td><td>수치 근거로 의심 지점을 정한다.</td><td>예상 rows와 실제 rows 차이를 근거로 말한다.</td></tr><tr><td>실험 통제</td><td>한 번에 하나만 바꾼다.</td><td>인덱스와 쿼리 재작성을 동시에 적용하지 않는다.</td></tr><tr><td>재현성</td><td>환경과 플랜을 남긴다.</td><td>동료가 같은 SQL로 비교할 수 있다.</td></tr></tbody>",
        "<tbody><tr><td>플랜 독해</td><td>노드와 실행 흐름을 구분한다.</td><td>상위/하위 노드 관계를 설명한다.</td></tr><tr><td>수치 근거</td><td>cost만이 아니라 actual time, rows, loops를 함께 읽는다.</td><td>수치 3종 이상으로 병목 근거를 제시한다.</td></tr><tr><td>가설 품질</td><td>병목 후보를 최소 2개 제시하고 우선순위를 둔다.</td><td>가설마다 확인할 evidence line을 붙인다.</td></tr><tr><td>실험 통제</td><td>한 번에 하나만 바꾸고 변경 전후를 비교한다.</td><td>인덱스와 쿼리 재작성을 동시에 적용하지 않는다.</td></tr><tr><td>재현성</td><td>SQL, 파라미터 성격, 실행 환경, 플랜 캡처를 남긴다.</td><td>동료가 같은 SQL로 비교할 수 있다.</td></tr></tbody>",
    )
    html = replace_once(
        html,
        "<aside class=\"source-note\"><div class=\"label\">Source Note</div><p>전담 education_html 에이전트의 커리큘럼을 바탕으로 확장했으며, PostgreSQL 공식 문서의 EXPLAIN/ANALYZE 개념과 planner 통계 설명에 맞춰 서술했다.</p></aside>",
        "<aside class=\"source-note\"><div class=\"label\">Source Note</div><p>전담 education_html 에이전트 결과를 반영해 adaptive-html-final v5.1.0의 generated-row/lens-strip, wg-08 static-stepper, PostgreSQL 전용 wg-13 플로우, a11y-checklist를 적용했다.</p></aside>",
    )
    path.write_text(html, encoding="utf-8")


def update_blog(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = set_header(
        html,
        "PERSONAL BLOG",
        "두 번째 뇌를 다시 작게 만든 30일 기록",
        "노트를 더 많이 저장하는 대신 다시 꺼내 쓸 수 있는 크기로 줄인 30일 지식관리 회고다.",
        ["blog_writer", "personal-blog-essay.html", "profile auto", "adaptive-html-final v5.1.0", "무 JS"],
        "Generated · 2026-06-05 08:34 KST",
        ["회수율", "30일 회고", "작은 시스템"],
    )
    html = wrap_first_vt(html, "vt-04 timeline", "vt-04 timeline")
    html = tune_numbers(html, {1, 9})
    html = insert_before(
        html,
        "<!-- template-showcase:start vt-04 timeline -->",
        "<div class=\"lede-note\"><span class=\"label\">Goal</span><p>이 글은 노트 앱을 더 잘 꾸미는 법이 아니라, 30일 동안 저장량을 줄여 회수율을 올린 기준을 기록한다. 독자는 오늘 지울 노트, 고칠 제목, 남길 회고 문장을 바로 정할 수 있어야 한다.</p></div>",
    )
    html = replace_once(
        html,
        "<p>가장 큰 실패는 “분류를 잘하면 생각도 좋아질 것”이라는 착각이었다. 실제로 필요한 것은 완벽한 위치가 아니라 다시 읽을 이유였다.</p></section>",
        "<p>가장 큰 실패는 “분류를 잘하면 생각도 좋아질 것”이라는 착각이었다. 실제로 필요한 것은 완벽한 위치가 아니라 다시 읽을 이유였다.</p>"
        "<div class=\"source-preserve source-preserve-static\" role=\"group\" aria-labelledby=\"source-small-brain-rule\"><div id=\"source-small-brain-rule\" class=\"source-preserve-title\">실험 원문 기준 · raw rule preserved</div><div class=\"source-body\"><p><strong>30일 기준:</strong> 더 많이 저장하지 않는다. 다시 쓸 수 없는 노트는 빚으로 본다. 새 노트에는 질문, 관찰, 다음 행동 중 하나를 반드시 남긴다.</p></div></div></section>",
    )
    html = replace_once(
        html,
        "<p>작아진 시스템은 무너지지 않는 시스템이 아니라, 무너져도 다시 세우기 쉬운 시스템이었다.</p>\n\n\n<!-- template-showcase:start vt-13 comparison-cards -->",
        "<p>작아진 시스템은 무너지지 않는 시스템이 아니라, 무너져도 다시 세우기 쉬운 시스템이었다.</p>"
        "<div class=\"ba\"><div class=\"ba-col before\"><span class=\"ba-label\">Before</span><p>많이 저장할수록 안심했고, 태그와 폴더를 늘리면 생각도 정리될 거라고 믿었다.</p></div><div class=\"ba-arrow\" aria-hidden=\"true\">&rarr;</div><div class=\"ba-col after\"><span class=\"ba-label\">After</span><p>다시 꺼내 쓸 수 있을 때만 저장하고, 제목·링크·회고가 다음 행동을 돕는지 먼저 본다.</p></div></div>\n\n\n<!-- template-showcase:start vt-13 comparison-cards -->",
    )
    a11y = a11y_block(
        "블로그 배포 전 접근성 30분 점검",
        "링크, 접기 위젯, 다크 CTA가 섞인 긴 글이므로 배포 전 키보드 경로, 대비, 제목 계층을 확인한다.",
        [
            ("키보드", "8분", "timeline, details, CTA 접근", "timeline, details, CTA까지 Tab으로 도달", "접힌 파일 워크스루를 열 수 없음"),
            ("대비", "7분", "meta/lens/proper-black 대비", "meta chip, lens chip, proper-black CTA가 AA 대비 유지", "다크 CTA 내부 텍스트가 흐림"),
            ("구조", "10분", "numbered h2와 vt/wg 흐름", "h1 1개, numbered h2 10개, vt/wg 보강이 제목 계층을 깨지 않음", "보강 블록이 본문 흐름을 끊음"),
        ],
        ["키보드 전 경로와 가시 포커스를 확인한다.", "proper-black CTA 대비를 확인한다.", "vt/wg 텍스트가 DOM에 남아 있다.", "동작 JS 0을 유지한다."],
    )
    html = insert_after(html, "</section>\n<aside class=\"source-note\">", a11y + "\n<aside class=\"source-note\">").replace("</section>\n<aside class=\"source-note\">\n<section class=\"a11y-check\"", "</section>\n<section class=\"a11y-check\"")
    html = replace_once(
        html,
        "<aside class=\"source-note\"><div class=\"label\">Source Note</div><p>전담 blog_writer 에이전트의 개인 회고 구조를 바탕으로 확장했다. 특정 노트 앱 비교가 아니라 작게 유지되는 개인 지식관리 습관을 다룬다.</p></aside>",
        "<aside class=\"source-note\"><div class=\"label\">Source Note</div><p>개인 지식관리 30일 회고 구조를 유지하되, adaptive-html-final v5.1.0의 header/generated-row/lens-strip, lede-note, source-preserve, before-after, a11y-checklist 패턴으로 보강했다.</p></aside>",
    )
    path.write_text(html, encoding="utf-8")


def update_index(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = set_header(
        html,
        "ADAPTIVE HTML FINAL",
        "13개 모드 신규 주제 쇼케이스",
        "최신 adaptive-html-final v5.1.0 기준으로 13개 신규 주제와 1~5번 모드 상세 보강을 확인할 수 있는 HTML 모음이다.",
        ["created 2026-06-05 08:34:33", "profile auto", "13 modes", "adaptive-html-final v5.1.0", "validate target"],
        "Refresh · 2026-06-05 KST · v5.1.0 proper-black dark",
        ["1~5 병렬 에이전트", "vt/wg 템플릿", "a11y 패턴", "무 JS"],
    )
    if "1~5번은 병렬 에이전트 분석을 통합" not in html:
        html = replace_once(
            html,
            "<section class=\"summary-card\"><div class=\"label\">Overview</div><p>이번 출력은 `adaptive-html-final`의 13개 모드를 각각 다른 신규 주제에 적용한 쇼케이스다. 폴더는 날짜/시간 기준으로 생성했고, CSS 코어 해시와 source manifest를 함께 남겼다.</p></section>",
            "<section class=\"summary-card\"><div class=\"label\">Overview</div><p>이번 출력은 <code>adaptive-html-final</code> v5.1.0의 13개 모드를 각각 다른 신규 주제에 적용한 쇼케이스다. 1~5번은 병렬 에이전트 분석을 통합해 generated-row/lens-strip, proper-black dark, editorial pattern, a11y-checklist, 권장 vt/wg 배치를 다시 보강했다.</p></section>",
        )
    path.write_text(html, encoding="utf-8")


def rebase_sources() -> None:
    sources = ROOT / "sources"
    assets_dir = sources / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    for name in INLINE_ASSETS:
        shutil.copyfile(ASSETS / name, assets_dir / name)
    shutil.copyfile(SKILL / "manifest.json", sources / "adaptive-html-final-manifest.json")
    (sources / "profile.json").write_text(json.dumps({"profile": "auto"}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    asset_hashes = {
        name: hashlib.sha256(read_asset(name).encode("utf-8")).hexdigest()
        for name in INLINE_ASSETS
    }
    integrity = {
        "core_css_sha256": core_hash(),
        "asset_order": CORE_ASSETS,
        "conditional_asset_order": [name for name in INLINE_ASSETS if name not in CORE_ASSETS],
        "asset_sha256": asset_hashes,
        "profile": "auto",
        "skill_version": json.loads((SKILL / "manifest.json").read_text(encoding="utf-8"))["version"],
    }
    (sources / "css-integrity.json").write_text(json.dumps(integrity, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    pages = ROOT / "pages"
    content_updates = [
        update_beginner,
        update_expert,
        update_article,
        update_education,
        update_blog,
    ]
    content_paths = [
        pages / "01-local-rag-personal-knowledge-vault.html",
        pages / "02-ai-code-review-gateway-operating-model.html",
        pages / "03-small-team-operating-docs-product-speed.html",
        pages / "04-postgres-query-plan-3week-course.html",
        pages / "05-small-second-brain-30days-retro.html",
    ]
    for updater, page_path in zip(content_updates, content_paths):
        if not content_updated(page_path):
            updater(page_path)
    update_index(ROOT / "index.html")

    for html_path in [ROOT / "index.html", *sorted(pages.glob("*.html"))]:
        html_path.write_text(replace_style(html_path.read_text(encoding="utf-8")), encoding="utf-8")
    rebase_sources()
    print(f"Updated pages 01-05 and rebased CSS to v5.1.0 core {core_hash()}")


if __name__ == "__main__":
    main()
