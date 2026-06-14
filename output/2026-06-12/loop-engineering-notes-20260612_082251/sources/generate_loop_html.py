from __future__ import annotations

import html
import hashlib
import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SKILL = ROOT / "skills" / "adaptive-html-final"
ASSETS = SKILL / "assets"
OUT = ROOT / "output" / "loop-engineering-notes-20260612_082251"
SOURCES = OUT / "sources"
SOURCE_ASSETS = SOURCES / "assets"
INPUT = Path("/Users/iriver/Downloads/loop_engineering_notes.md")


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

SLOT_BY_ASSET = {
    "theme.css": "{{THEME_CSS}}",
    "components.css": "{{COMPONENTS_CSS}}",
    "visual-components.css": "{{VISUAL_COMPONENTS_CSS}}",
    "widgets.css": "{{WIDGETS_CSS}}",
    "visual-html.css": "{{VISUAL_HTML_CSS}}",
    "body-icons.css": "{{BODY_ICONS_CSS}}",
    "editorial-patterns.css": "{{EDITORIAL_PATTERNS_CSS}}",
    "shape-visuals.css": "{{SHAPE_VISUALS_CSS}}",
    "workflow-visuals.css": "{{WORKFLOW_VISUALS_CSS}}",
    "layouts.css": "{{LAYOUTS_CSS}}",
    "print.css": "{{PRINT_CSS}}",
    "theme-dark.css": "{{THEME_DARK_CSS}}",
}


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def slug(value: str) -> str:
    return value.lower().replace(" ", "-").replace("/", "-")


def icon(name: str = "bookmark") -> str:
    shapes = {
        "target": '<circle class="bi-soft" cx="20" cy="20" r="12"/><path class="bi-accent-line" d="M20 10v20M10 20h20"/><circle class="bi-accent" cx="20" cy="20" r="3"/>',
        "map": '<rect class="bi-fill" x="8" y="10" width="24" height="20" rx="3"/><path class="bi-line" d="M16 10v20M24 10v20"/><path class="bi-accent-line" d="M11 24l6-5 6 4 6-6"/>',
        "compare": '<rect class="bi-fill" x="7" y="9" width="11" height="22" rx="3"/><rect class="bi-soft" x="22" y="9" width="11" height="22" rx="3"/><path class="bi-accent-line" d="M12 17h5M23 24h5"/>',
        "timeline": '<path class="bi-line" d="M11 8v24"/><circle class="bi-soft" cx="11" cy="12" r="4"/><circle class="bi-soft" cx="11" cy="22" r="4"/><circle class="bi-accent" cx="11" cy="31" r="3"/><path class="bi-accent-line" d="M18 12h12M18 22h9M18 31h11"/>',
        "question": '<circle class="bi-fill" cx="20" cy="20" r="13"/><path class="bi-accent-line" d="M16 16c1-4 8-4 8 0 0 3-4 3.6-4 7"/><circle class="bi-accent" cx="20" cy="29" r="2"/>',
        "loop": '<path class="bi-accent-line" d="M12 15a10 10 0 0 1 16-3"/><path class="bi-line" d="M28 8v6h-6M28 25a10 10 0 0 1-16 3"/><path class="bi-line" d="M12 32v-6h6"/>',
        "flag": '<path class="bi-line" d="M12 31V9"/><path class="bi-soft" d="M13 10h15l-3 6 3 6H13z"/><circle class="bi-accent" cx="12" cy="31" r="2"/>',
        "check": '<circle class="bi-soft" cx="20" cy="20" r="13"/><path class="bi-accent-line" d="M13 20l5 5 10-11"/>',
        "module": '<rect class="bi-fill" x="8" y="8" width="9" height="9" rx="2"/><rect class="bi-soft" x="23" y="8" width="9" height="9" rx="2"/><rect class="bi-fill" x="8" y="23" width="9" height="9" rx="2"/><rect class="bi-soft" x="23" y="23" width="9" height="9" rx="2"/><path class="bi-accent-line" d="M17 12.5h6M17 27.5h6"/>',
        "review": '<rect class="bi-fill" x="9" y="8" width="22" height="24" rx="4"/><path class="bi-line" d="M14 16h12M14 22h10"/><path class="bi-accent-line" d="M15 28l3 3 7-8"/>',
        "test": '<path class="bi-fill" d="M15 8h10v9l6 10c1 2-.3 5-2.8 5H11.8C9.3 32 8 29 9 27l6-10z"/><path class="bi-accent-line" d="M15 18h10M13 26h14"/>',
        "note": '<rect class="bi-fill" x="10" y="7" width="20" height="26" rx="3"/><path class="bi-line" d="M15 14h10M15 20h10M15 26h7"/><path class="bi-accent-line" d="M27 7v8h-8"/>',
        "memory": '<rect class="bi-fill" x="9" y="11" width="22" height="18" rx="5"/><path class="bi-line" d="M13 11V8M19 11V8M25 11V8M13 32v-3M19 32v-3M25 32v-3"/><circle class="bi-accent" cx="20" cy="20" r="4"/>',
        "governance": '<path class="bi-fill" d="M20 7l11 4v8c0 7-4.5 11.5-11 14-6.5-2.5-11-7-11-14v-8z"/><path class="bi-accent-line" d="M15 20l4 4 7-9"/>',
        "web": '<rect class="bi-fill" x="7" y="10" width="26" height="19" rx="3"/><path class="bi-line" d="M7 16h26"/><circle class="bi-accent" cx="12" cy="13" r="1.5"/><path class="bi-accent-line" d="M13 23h14"/>',
        "quote": '<path class="bi-soft" d="M12 12h8v8c0 5-3 8-8 9v-4c2-.7 3-2 3-4h-3zM23 12h8v8c0 5-3 8-8 9v-4c2-.7 3-2 3-4h-3z"/>',
        "summary": '<rect class="bi-fill" x="9" y="8" width="22" height="24" rx="4"/><path class="bi-accent-line" d="M14 16h12M14 22h12M14 28h8"/>',
        "file": '<path class="bi-fill" d="M12 7h12l6 6v20H12z"/><path class="bi-line" d="M24 7v7h6M16 21h9M16 27h7"/>',
        "checklist": '<rect class="bi-fill" x="9" y="8" width="22" height="24" rx="4"/><path class="bi-accent-line" d="M14 16l2 2 4-5M14 25l2 2 4-5"/><path class="bi-line" d="M23 17h4M23 26h4"/>',
    }
    svg = shapes.get(name, shapes["target"])
    return f'<span class="body-icon"><svg viewBox="0 0 40 40" aria-hidden="true">{svg}</svg></span>'


def codeblock(value: str, label: str = "text") -> str:
    return f'<pre><code data-lang="{esc(label)}">{esc(value.strip())}</code></pre>'


def table(caption: str, headers: list[str], rows: list[list[str]]) -> str:
    head = "".join(f"<th>{esc(h)}</th>" for h in headers)
    body_rows = []
    for row in rows:
        body_rows.append("<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>")
    return (
        '<div class="table-scroll"><table>'
        f"<caption>{esc(caption)}</caption><thead><tr>{head}</tr></thead>"
        f"<tbody>{''.join(body_rows)}</tbody></table></div>"
    )


def card_grid(cards: list[tuple[str, str, str]]) -> str:
    items = []
    for title, text, badge in cards:
        items.append(
            '<article class="card">'
            f'<span class="badge">{esc(badge)}</span>'
            f"<h3>{esc(title)}</h3>"
            f"<p>{esc(text)}</p>"
            "</article>"
        )
    return f'<div class="cards three">{"".join(items)}</div>'


def h2(number: str, title: str, icon_name: str = "target") -> str:
    return f'<h2>{icon(icon_name)}<span>{esc(number)} {esc(title)}</span></h2>'


def section(number: str, title: str, lead: str, body: str, icon_name: str = "target") -> str:
    return (
        f'<section id="s{esc(number)}" class="lesson-step">'
        f"{h2(number, title, icon_name)}"
        f'<p class="lead">{esc(lead)}</p>'
        f"{body}</section>"
    )


def bullets(items: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{item}</li>" for item in items) + "</ul>"


def source_preserve(title: str, lines: list[str]) -> str:
    return (
        f'<div class="source-preserve source-preserve-static" role="group" aria-label="{esc(title)}">'
        f'<div class="source-preserve-title">{esc(title)}</div>'
        f'<div class="source-body">{codeblock(chr(10).join(lines))}</div>'
        "</div>"
    )


def build_css() -> tuple[str, str, dict[str, str]]:
    core_text = "\n".join((ASSETS / name).read_text() for name in CORE_ASSETS)
    core_hash = hashlib.sha256(core_text.encode()).hexdigest()
    asset_hashes: dict[str, str] = {}
    css_parts: dict[str, str] = {}
    SOURCE_ASSETS.mkdir(parents=True, exist_ok=True)
    for name in INLINE_ASSETS:
        text = (ASSETS / name).read_text()
        asset_hashes[name] = hashlib.sha256(text.encode()).hexdigest()
        shutil.copy2(ASSETS / name, SOURCE_ASSETS / name)
        css_parts[name] = text
    css_parts["theme.css"] = (
        f"/* adaptive-html-final-core-css-sha256: {core_hash} */\n"
        + css_parts["theme.css"]
    )
    return core_hash, "\n".join(css_parts[name] for name in INLINE_ASSETS), asset_hashes


def build_integrity(core_hash: str, asset_hashes: dict[str, str]) -> dict[str, object]:
    return {
        "core_css_sha256": core_hash,
        "asset_order": CORE_ASSETS,
        "conditional_asset_order": [
            "widgets.css",
            "visual-html.css",
            "body-icons.css",
            "editorial-patterns.css",
            "shape-visuals.css",
            "workflow-visuals.css",
            "theme-dark.css",
        ],
        "inline_order": INLINE_ASSETS,
        "asset_sha256": asset_hashes,
    }


def build_toc() -> str:
    items = [
        ("1", "핵심 개념"),
        ("2", "문제의식"),
        ("3", "루프 기본 구조"),
        ("4", "핵심 질문"),
        ("5", "자유개선 루프"),
        ("6", "신규 기능 규칙"),
        ("7", "종료 조건"),
        ("8", "구성 요소"),
        ("9", "역할 분리"),
        ("10", "테스트 확장"),
        ("11", "문제 기록"),
        ("12", "메모리"),
        ("13", "운영 규칙"),
        ("14", "웹앱 예시"),
        ("15", "한 문장 정의"),
        ("16", "핵심 요약"),
    ]
    links = "".join(
        f'<a class="toc-pill" href="#s{num}"><b>{num}</b>{esc(title)}</a>'
        for num, title in items
    )
    return (
        '<nav class="toc-map" aria-label="학습 목차">'
        "<h2>이 문서의 학습 순서</h2>"
        "<p>원문 16개 장을 교육 모듈로 재배치했다. 순서대로 읽으면 개념 → 구조 → 운영 규칙 → 적용 예시로 이어진다.</p>"
        f'<div class="toc-pills">{links}</div></nav>'
    )


def build_vt_timeline() -> str:
    return """
<section class="vt-shell" aria-label="루프 엔지니어링 기본 순환">
  <div class="vt-frame">
    <ol class="tl">
      <li class="tl-item"><b>목표 정의</b><p class="vt-text">사람은 결과물과 성공 기준을 정한다.</p></li>
      <li class="tl-item"><b>조사와 생성</b><p class="vt-text">에이전트가 사례를 찾고 프롬프트 또는 해결안을 만든다.</p></li>
      <li class="tl-item"><b>테스트 수행</b><p class="vt-text">성공과 실패를 분리할 수 있는 케이스로 실제 검증한다.</p></li>
      <li class="tl-item"><b>실패 분석</b><p class="vt-text">무엇이 깨졌는지 기록하고 원인과 수정안을 분리한다.</p></li>
      <li class="tl-item"><b>개선과 기억</b><p class="vt-text">개별 수정, 전체 재검증, 성공/실패 패턴 저장을 반복한다.</p></li>
    </ol>
  </div>
</section>
""".strip()


def build_wg_flow() -> str:
    return """
<section class="wg-13-fc" aria-label="자유개선 루프 플로우차트">
  <h3 class="wg-13-h">자유개선 루프 <span class="wg-13-sub">새 기능 제안까지 허용하는 반복 구조</span></h3>
  <div class="wg-13-flow">
    <a href="#wg-13-loop-goal" class="wg-13-node wg-13-node--start"><span class="wg-13-step">시작</span>목표 입력</a>
    <span class="wg-13-arrow" aria-hidden="true">&darr;</span>
    <a href="#wg-13-loop-research" class="wg-13-node"><span class="wg-13-step">1</span>조사와 사례 수집</a>
    <span class="wg-13-arrow" aria-hidden="true">&darr;</span>
    <a href="#wg-13-loop-test" class="wg-13-node"><span class="wg-13-step">2</span>초안 생성과 테스트</a>
    <span class="wg-13-arrow" aria-hidden="true">&darr;</span>
    <div class="wg-13-branch">
      <a href="#wg-13-loop-gate" class="wg-13-node wg-13-node--decide"><span class="wg-13-step">3</span>종료 조건 충족?</a>
      <div class="wg-13-paths">
        <div class="wg-13-path wg-13-path--fail">
          <span class="wg-13-edge">아니오 &rarr; 개선 경로</span>
          <a href="#wg-13-loop-improve" class="wg-13-node wg-13-node--fail"><span class="wg-13-step">!</span>문제 기록과 재시도</a>
        </div>
        <div class="wg-13-path wg-13-path--ok">
          <span class="wg-13-edge">예 &rarr; 정착 경로</span>
          <a href="#wg-13-loop-memory" class="wg-13-node"><span class="wg-13-step">4</span>패턴 저장</a>
          <span class="wg-13-arrow" aria-hidden="true">&darr;</span>
          <a href="#wg-13-loop-end" class="wg-13-node wg-13-node--end"><span class="wg-13-step">완료</span>최종 승인</a>
        </div>
      </div>
    </div>
  </div>
  <div class="wg-13-detail">
    <h4 class="wg-13-dh">단계 상세 <span class="wg-13-dnote">각 단계는 실패 원인을 남긴 뒤 다음 반복의 입력이 된다.</span></h4>
    <details id="wg-13-loop-goal" class="wg-13-acc" open><summary><span class="wg-13-tag">시작</span>목표 입력</summary><div class="wg-13-body"><p>사람은 원하는 결과, 품질 기준, 금지 조건을 먼저 정의한다.</p></div></details>
    <details id="wg-13-loop-research" class="wg-13-acc" open><summary><span class="wg-13-tag">1단계</span>조사와 사례 수집</summary><div class="wg-13-body"><p>좋은 사례와 실패 사례를 모두 수집해 비교 기준을 만든다.</p></div></details>
    <details id="wg-13-loop-test" class="wg-13-acc" open><summary><span class="wg-13-tag">2단계</span>초안 생성과 테스트</summary><div class="wg-13-body"><p>프롬프트, 코드, 문서 초안을 만들고 정상/엣지/회귀 케이스로 검증한다.</p></div></details>
    <details id="wg-13-loop-gate" class="wg-13-acc" open><summary><span class="wg-13-tag">3단계</span>종료 조건 충족 여부</summary><div class="wg-13-body"><p>정확도, 회귀 없음, 재현성, 사용성, 저장 완료를 동시에 본다.</p></div></details>
    <details id="wg-13-loop-improve" class="wg-13-acc wg-13-acc--fail" open><summary><span class="wg-13-tag wg-13-tag--fail">개선</span>문제 기록과 재시도</summary><div class="wg-13-body"><p>실패 유형, 원인, 수정안, 재테스트 결과를 남기고 다음 루프로 연결한다.</p></div></details>
    <details id="wg-13-loop-memory" class="wg-13-acc" open><summary><span class="wg-13-tag">4단계</span>패턴 저장</summary><div class="wg-13-body"><p>성공 조건, 실패 패턴, 좋은 프롬프트, 금지 패턴을 메모리에 저장한다.</p></div></details>
    <details id="wg-13-loop-end" class="wg-13-acc wg-13-acc--ok" open><summary><span class="wg-13-tag wg-13-tag--ok">완료</span>최종 승인</summary><div class="wg-13-body"><p>사람은 전체 루프 결과를 검토하고 다음 운영 기준으로 승인한다.</p></div></details>
  </div>
</section>
""".strip()


def build_body(raw: str) -> str:
    sections: list[str] = []

    sections.append(
        section(
            "1",
            "핵심 개념",
            "루프 엔지니어링은 좋은 프롬프트 한 번이 아니라, 좋은 결과가 나올 때까지 스스로 개선되는 반복 시스템을 설계하는 일이다.",
            """
<div class="core-insight"><strong>핵심 전환</strong><p>사람은 프롬프트 작성자에서 루프 설계자, 목표 정의자, 최종 승인자로 이동한다. 에이전트는 조사, 실행, 테스트, 실패 분석, 개선, 검증, 기억을 반복한다.</p></div>
<div class="impact-grid">
  <article><b>입력</b><p>목표, 품질 기준, 금지 조건</p></article>
  <article><b>반복</b><p>조사 → 생성 → 테스트 → 분석 → 개선</p></article>
  <article><b>축적</b><p>성공 패턴, 실패 원인, 재사용 프롬프트</p></article>
</div>
""",
            "target",
        )
    )

    problem_flow = """기존 방식:
사람 → 프롬프트 작성 → AI 실행 → 사람이 결과 확인 → 사람이 수정

루프 엔지니어링 방식:
사람 → 목표 정의 → 에이전트가 프롬프트 생성 → 실행 → 테스트 → 실패 분석 → 개선 → 검증 → 메모리 저장 → 반복"""
    sections.append(
        section(
            "2",
            "문제의식",
            "앞으로 중요한 것은 사람이 매번 다시 고치는 흐름이 아니라, 에이전트가 스스로 테스트하고 실패를 다음 입력으로 바꾸는 구조다.",
            f"""
<div class="before-after">
  <article><h3>기존 프롬프트 중심</h3><p>사람이 프롬프트를 만들고, 결과를 확인하고, 다시 수정한다. 실패가 시스템 자산으로 남기 어렵다.</p></article>
  <article><h3>루프 엔지니어링 중심</h3><p>에이전트가 프롬프트를 만들고, 스스로 테스트하고, 실패하면 개선하며, 검증 결과를 기억한다.</p></article>
</div>
{codeblock(problem_flow)}
""",
            "compare",
        )
    )

    loop_steps = [
        "목표 정의",
        "에이전트가 조사",
        "해결 방법 또는 프롬프트 생성",
        "테스트 케이스 생성",
        "실제 테스트 수행",
        "문제점 기록",
        "실패 원인 분석",
        "개선 프롬프트 또는 수정안 작성",
        "개별 수정 및 재테스트",
        "전체 테스트 재실행",
        "성공/실패 패턴을 메모리에 저장",
        "종료 조건 충족 여부 확인",
        "부족하면 반복",
    ]
    sections.append(
        section(
            "3",
            "루프의 기본 구조",
            "반복 자체보다 중요한 것은 반복할 때마다 남는 자산이다.",
            build_vt_timeline()
            + table(
                "13단계 루프 기본 구조",
                ["순서", "단계", "산출물"],
                [[str(i), esc(step), esc("다음 단계의 입력 또는 검증 근거")] for i, step in enumerate(loop_steps, 1)],
            ),
            "timeline",
        )
    )

    role_table = table(
        "평가자와 검증자 분리 모델",
        ["역할", "하는 일", "판단 기준"],
        [
            ["작성자 Agent", "프롬프트·코드·문서 초안을 만든다.", "목표를 얼마나 잘 구현했는가"],
            ["평가자 Agent", "결과물을 기준에 따라 평가하고 약점을 찾는다.", "품질 기준을 얼마나 정확히 적용했는가"],
            ["검증자 Agent", "테스트·재현·회귀 확인을 수행한다.", "실패를 실제로 잡아냈는가"],
            ["기록자 Agent", "성공/실패 패턴과 재사용 지식을 남긴다.", "다음 루프에 쓸 수 있게 정리했는가"],
        ],
    )
    sections.append(
        section(
            "4",
            "루프 엔지니어링의 핵심 질문",
            "좋은 루프는 평가 도구, 자산 축적, 역할 분리를 갖춘다.",
            card_grid(
                [
                    ("신뢰할 만한 평가 도구", "주관적 만족이 아니라 테스트 케이스, 자동 검증, 비교 기준으로 판단한다.", "Q1"),
                    ("매번 나아지는 구조", "실패가 사라지지 않고 프롬프트, 테스트, 금지 패턴, 체크리스트로 쌓인다.", "Q2"),
                    ("역할의 분리", "작성자와 평가자가 같으면 자기 합리화가 생기므로 검증자를 분리한다.", "Q3"),
                ]
            )
            + role_table
            + codeblock("조사 → 검증 → 정립 → 참조\n즉흥 답변 → 체계적 지식 생성"),
            "question",
        )
    )

    free_loop_rows = [
        ["1", "목표 입력", "사람이 원하는 결과와 금지 조건을 정의한다."],
        ["2", "자료 조사", "좋은 사례와 실패 사례를 함께 찾는다."],
        ["3", "프롬프트 초안", "에이전트가 해결안 또는 프롬프트를 만든다."],
        ["4", "테스트 케이스", "정상/엣지/실패/회귀 케이스를 만든다."],
        ["5", "실행", "초안을 실제로 돌린다."],
        ["6", "검증", "테스트 통과 여부와 품질 기준을 확인한다."],
        ["7", "실패 분석", "실패 유형, 원인, 수정안을 분리해 기록한다."],
        ["8", "개선", "개별 수정과 전체 재검증을 수행한다."],
        ["9", "새 기능 제안", "목표를 더 잘 달성할 개선 기능을 제안하되 별도 검증을 요구한다."],
    ]
    sections.append(
        section(
            "5",
            "자유개선 루프 아이디어",
            "에이전트가 기존 요구만 수행하지 않고 필요한 새 기능도 제안할 수 있도록 하되, 제안과 적용을 분리해 통제한다.",
            build_wg_flow()
            + table("자유개선 루프 운영 단계", ["순서", "단계", "의미"], free_loop_rows),
            "loop",
        )
    )

    sections.append(
        section(
            "6",
            "신규 기능 제안 규칙",
            "새 기능 제안은 허용하지만 무단 적용은 금지한다. 제안, 승인, 검증의 선이 분명해야 한다.",
            table(
                "신규 기능 제안 승인 기준",
                ["조건", "질문", "처리"],
                [
                    ["목표 직접 기여", "이 기능이 원래 목표 달성에 직접 도움이 되는가?", "근거와 기대 효과를 요구한다."],
                    ["복잡도 통제", "새 기능 때문에 시스템이 과도하게 복잡해지는가?", "작게 실험하고 되돌릴 수 있어야 한다."],
                    ["리스크 명시", "부작용과 실패 가능성이 무엇인가?", "실패 케이스를 먼저 추가한다."],
                    ["분리 승인", "제안과 적용이 분리되어 있는가?", "사람 승인 전 적용하지 않는다."],
                    ["효과 검증", "적용 후 실제 지표가 좋아졌는가?", "전후 비교 또는 테스트 통과를 남긴다."],
                ],
            ),
            "flag",
        )
    )

    termination = [
        ["목표 충족", "결과물이 처음 정의한 목표를 만족한다.", "필수 기능/문서/출력이 빠지지 않는다."],
        ["테스트 통과", "정상·예외·회귀 케이스가 모두 통과한다.", "실패가 재현되지 않는다."],
        ["새 문제 없음", "개선 과정에서 새로운 문제가 생기지 않는다.", "이전 동작이 유지된다."],
        ["기억 완료", "성공 패턴과 실패 패턴이 저장된다.", "다음 작업에서 참조 가능하다."],
        ["승인 가능", "사람이 최종 판단할 수 있을 만큼 근거가 정리된다.", "요약과 근거가 함께 있다."],
    ]
    sections.append(
        section(
            "7",
            "명확한 종료 조건",
            "루프가 무한히 도는 것을 막으려면 종료 조건이 먼저 있어야 한다.",
            table("종료 조건 체크", ["조건", "의미", "확인 방법"], termination)
            + source_preserve(
                "실패 예시",
                [
                    "목표: 로그인 기능 개선",
                    "종료 조건 없음",
                    "결과: UI 수정 → 에러 메시지 수정 → 보안 개선 → 소셜 로그인 추가 → 가입 플로우 변경 → 끝나지 않음",
                    "",
                    "따라서 루프는 항상 종료 조건과 함께 설계해야 합니다.",
                ],
            ),
            "check",
        )
    )

    components = [
        ["목표 정의", "무엇을 만들고 무엇을 금지할지 정한다.", "결과물 기준"],
        ["조사 루프", "관련 사례와 반례를 수집한다.", "근거 목록"],
        ["생성 루프", "프롬프트·코드·문서·설계안을 만든다.", "초안"],
        ["테스트 루프", "정상/실패/엣지 케이스를 실행한다.", "검증 결과"],
        ["분석 루프", "실패 원인과 수정 방향을 분리한다.", "이슈 기록"],
        ["개선 루프", "작게 수정하고 다시 검증한다.", "패치와 재테스트"],
        ["메모리 루프", "다음에 재사용할 지식을 저장한다.", "성공/실패 패턴"],
        ["종료 판단", "완료, 반복, 중단을 결정한다.", "최종 판단"],
    ]
    sections.append(
        section(
            "8",
            "루프 엔지니어링의 구성 요소",
            "구성 요소를 나누면 어떤 단계가 비어 있는지 빠르게 찾을 수 있다.",
            table("구성 요소와 산출물", ["구성 요소", "역할", "남는 자산"], components),
            "module",
        )
    )

    sections.append(
        section(
            "9",
            "평가자와 검증자 분리 모델",
            "루프의 신뢰도는 작성자와 평가자가 분리될 때 올라간다.",
            card_grid(
                [
                    ("작성자는 생성에 집중", "좋은 초안을 만드는 데 집중한다. 자기 결과를 과하게 신뢰하지 않는다.", "Writer"),
                    ("평가자는 약점을 찾음", "누락, 모순, 품질 저하, 요구 불일치를 찾는다.", "Reviewer"),
                    ("검증자는 재현함", "실제 테스트와 회귀 확인으로 판단을 증명한다.", "Verifier"),
                ]
            )
            + role_table,
            "review",
        )
    )

    test_expansion = [
        ["정상 케이스", "의도한 입력에서 기대 결과가 나온다.", "대표 성공 경로"],
        ["경계 케이스", "최소/최대/빈 값/긴 입력을 넣는다.", "조건문 누락 탐지"],
        ["실패 케이스", "잘못된 입력과 오류 상황을 넣는다.", "에러 처리 검증"],
        ["회귀 케이스", "이미 고친 문제가 다시 발생하지 않는지 본다.", "과거 실패 방지"],
        ["비교 케이스", "기존 방식과 개선 방식의 차이를 본다.", "효과 측정"],
        ["사용성 케이스", "사람이 결과를 이해하고 사용할 수 있는지 본다.", "실제 적용성"],
    ]
    sections.append(
        section(
            "10",
            "테스트 케이스 확장 방식",
            "루프가 좋아지려면 테스트도 같이 자라야 한다.",
            table("테스트 케이스 확장 기준", ["종류", "설명", "목적"], test_expansion),
            "test",
        )
    )

    failure_template = """문제 ID:
발생 단계:
입력:
기대 결과:
실제 결과:
실패 유형:
추정 원인:
수정 방향:
재테스트 결과:
메모리 저장 여부:"""
    sections.append(
        section(
            "11",
            "문제 기록 포맷",
            "실패를 잘 기록해야 다음 루프가 똑똑해진다.",
            '<div class="md-excerpt">'
            "<h3>기록 원칙</h3>"
            "<p>문제 기록은 감상이 아니라 재현 가능한 단서여야 한다. 입력, 기대 결과, 실제 결과, 원인, 수정 방향을 분리한다.</p>"
            f"{codeblock(failure_template)}"
            "</div>",
            "note",
        )
    )

    memory_items = [
        ["성공한 프롬프트 패턴", "다음 생성 루프의 시작점으로 재사용한다."],
        ["실패한 프롬프트 패턴", "반복하지 말아야 할 금지 패턴으로 저장한다."],
        ["좋았던 테스트 케이스", "검증 품질을 높이는 기본 세트가 된다."],
        ["자주 발생한 오류 유형", "초기 점검 체크리스트가 된다."],
        ["검증에 효과적인 기준", "평가자/검증자 모델의 판단 근거가 된다."],
        ["새 기능 제안 중 채택된 것", "다음 제품 개선 루프의 후보가 된다."],
    ]
    sections.append(
        section(
            "12",
            "메모리 저장 항목",
            "메모리는 로그가 아니라 다음 루프의 입력으로 쓰일 수 있는 구조화된 지식이어야 한다.",
            table("메모리에 저장할 항목", ["항목", "활용 방식"], memory_items),
            "memory",
        )
    )

    ops_rules = [
        "<strong>한 번에 너무 많은 것을 바꾸지 않는다.</strong> 그래야 실패 원인을 추적할 수 있다.",
        "<strong>모든 실패를 기록한다.</strong> 기록되지 않은 실패는 다음 루프를 똑똑하게 만들지 못한다.",
        "<strong>종료 조건을 먼저 정한다.</strong> 목표 없는 반복은 루프가 아니라 소모다.",
        "<strong>제안과 적용을 분리한다.</strong> 신규 기능은 별도 승인과 검증을 거친다.",
        "<strong>검증자는 작성자와 분리한다.</strong> 자기 결과를 자기 기준으로만 통과시키지 않는다.",
        "<strong>성공 패턴도 저장한다.</strong> 실패만큼 성공 조건도 재사용 가능한 자산이다.",
        "<strong>회귀 테스트를 유지한다.</strong> 개선이 과거 정답을 망가뜨리지 않아야 한다.",
    ]
    sections.append(
        section(
            "13",
            "루프 엔지니어링 운영 규칙",
            "운영 규칙은 루프를 통제하고 회귀를 막는 안전장치다.",
            '<ol class="checklist">' + "".join(f"<li>{item}</li>" for item in ops_rules) + "</ol>",
            "governance",
        )
    )

    web_example = [
        ["목표", "웹앱 완성도를 높인다.", "사용자 관점의 품질 기준을 먼저 둔다."],
        ["에이전트 조사", "비슷한 서비스의 UI/UX와 기능 흐름을 조사한다.", "좋은 사례와 실패 사례를 함께 모은다."],
        ["문제 도출", "현재 앱의 부족한 기능과 불편한 흐름을 찾는다.", "기능 누락, 설명 부족, 오류 상태를 구분한다."],
        ["개선 제안", "검색, 필터, 온보딩, 빈 상태, 오류 메시지 등을 제안한다.", "목표 기여와 복잡도를 함께 본다."],
        ["구현", "승인된 항목만 작게 수정한다.", "한 번에 하나씩 적용한다."],
        ["검증", "브라우저 캡처, 모바일/데스크톱, 회귀 테스트를 수행한다.", "눈에 보이는 품질과 기능을 모두 확인한다."],
        ["기록", "성공한 패턴과 실패한 패턴을 메모리에 남긴다.", "다음 앱 개선 루프에 재사용한다."],
    ]
    sections.append(
        section(
            "14",
            "실제 적용 예시: 웹앱 자유개선 루프",
            "웹앱 개선 루프는 UI, 기능, 오류, 회귀, 사용성을 함께 본다.",
            table("웹앱 자유개선 루프 적용 예시", ["단계", "작업", "주의점"], web_example),
            "web",
        )
    )

    sections.append(
        section(
            "15",
            "한 문장 정의",
            "루프 엔지니어링은 AI에게 일을 시키는 기술이 아니라, AI가 스스로 더 잘 일하도록 반복 구조를 설계하는 기술이다.",
            '<blockquote class="core-insight"><p>“AI에게 일을 시키는 기술”에서 “AI가 스스로 더 잘 일하도록 만드는 구조를 설계하는 기술”로 이동하는 것이다.</p></blockquote>',
            "quote",
        )
    )

    sections.append(
        section(
            "16",
            "핵심 요약",
            "프롬프트보다 루프, 답변보다 검증, 성공보다 실패 기록, 실행보다 개선 구조가 중요하다.",
            bullets(
                [
                    "핵심은 프롬프트 작성이 아니라 개선 루프 설계다.",
                    "에이전트는 조사, 생성, 테스트, 실패 분석, 개선, 검증, 기억을 반복해야 한다.",
                    "반복할 때마다 테스트 케이스, 실패 기록, 성공 패턴, 금지 패턴이 남아야 한다.",
                    "작성자, 평가자, 검증자를 분리하면 신뢰도가 올라간다.",
                    "종료 조건이 없으면 루프는 계속 확장되어 끝나지 않는다.",
                    "새 기능 제안은 허용하되 승인과 검증을 분리해야 한다.",
                ]
            ),
            "summary",
        )
    )

    raw_preserved = (
        '<section id="original" class="lesson-step">'
        f"{h2('17', '원문 전체 보존', 'file')}"
        '<p class="lead">아래는 입력 파일의 원문 전체다. 교육형 재구성에서 빠진 내용이 없도록 원문을 접기 영역으로 함께 보존했다.</p>'
        '<details class="box" open><summary>loop_engineering_notes.md 전체 보기</summary>'
        f"{codeblock(raw, 'markdown')}"
        "</details></section>"
    )

    quiz = f"""
<h2>{icon('question')}<span>학습 확인 퀴즈</span></h2>
<ol>
  <li>루프 엔지니어링에서 사람의 역할은 무엇으로 바뀌는가?</li>
  <li>작성자와 검증자를 분리해야 하는 이유는 무엇인가?</li>
  <li>신규 기능 제안이 바로 적용되면 어떤 문제가 생길 수 있는가?</li>
  <li>종료 조건 없이 웹앱 개선 루프를 돌리면 어떤 일이 벌어지는가?</li>
</ol>
""".strip()

    answer = f"""
<h2>{icon('check')}<span>정답 및 해설</span></h2>
<ol>
  <li>프롬프트 작성자가 아니라 루프 설계자, 목표 정의자, 최종 승인자에 가까워진다.</li>
  <li>작성자가 자기 결과를 스스로 통과시키는 자기 합리화를 줄이고, 실패를 더 잘 발견하기 위해서다.</li>
  <li>목표와 무관한 기능 확장, 복잡도 증가, 회귀, 검증 없는 변경이 발생할 수 있다.</li>
  <li>검색, UI, 보안, 소셜 로그인처럼 범위가 계속 넓어져 끝나지 않는 작업이 된다.</li>
</ol>
""".strip()

    review = f"""
<h2>{icon('checklist')}<span>실무 적용 체크리스트</span></h2>
<ul>
  <li>목표, 성공 기준, 금지 조건을 먼저 썼다.</li>
  <li>정상/실패/엣지/회귀 테스트 케이스가 있다.</li>
  <li>작성자와 검증자의 역할이 분리되어 있다.</li>
  <li>실패 기록 포맷이 고정되어 있다.</li>
  <li>성공/실패 패턴을 다음 루프에서 참조할 수 있다.</li>
  <li>종료 조건과 최종 승인 기준이 명확하다.</li>
</ul>
""".strip()

    return f"""
<main id="main" class="page layout-education">
  <header class="header">
    <div class="kicker"><span class="kicker-text">COURSE MODULE · LOOP ENGINEERING</span></div>
    <h1>루프 엔지니어링 정리</h1>
    <p class="sub">조사, 실행, 테스트, 실패 분석, 개선, 검증, 기억을 반복하는 에이전트 운영 구조를 학습 문서로 재구성했다.</p>
    <div class="meta"><span>education_html</span><span>course-module.html</span><span>profile auto</span><span>adaptive-html-final 5.10.2</span><span>무 JS</span></div>
    <div class="generated-row"><p class="generated-date">생성 기준: 2026-06-12 KST · 최신 스킬 반영</p><div class="lens-strip" aria-label="적용 렌즈"><span class="lens-strip-label">LENS</span><span class="lens-chip">루프 설계</span><span class="lens-chip">검증자 분리</span><span class="lens-chip">메모리 축적</span><span class="lens-chip">운영 체크리스트</span></div></div>
  </header>
  <section class="summary-card">
    <h2>{icon('summary')}<span>핵심 요약</span></h2>
    <div class="label">Learning Goal</div>
    <p><strong>루프 엔지니어링은 프롬프트를 잘 쓰는 기술에서, 반복·검증·기억 구조를 설계하는 기술로 이동한다.</strong> 이 문서는 원문의 모든 내용을 학습 순서, 표, 플로우차트, 퀴즈, 원문 보존 영역으로 재구성한다.</p>
  </section>
  <section class="learning-goals">
    <h2>{icon('target')}<span>학습 목표</span></h2>
    <ul>
      <li>루프 엔지니어링이 프롬프트 작성과 어떻게 다른지 설명할 수 있다.</li>
      <li>목표 정의, 조사, 생성, 테스트, 실패 분석, 개선, 검증, 메모리 저장의 역할을 구분할 수 있다.</li>
      <li>신규 기능 제안, 종료 조건, 검증자 분리, 문제 기록 포맷을 실제 작업에 적용할 수 있다.</li>
    </ul>
  </section>
  <section class="before-start">
    <h2>{icon('map')}<span>문서 사용 방법</span></h2>
    <p>이 HTML은 원문을 요약만 한 것이 아니라, 모든 원문 내용을 교육형 섹션과 표, 플로우차트, 퀴즈, 원문 보존 영역으로 재배치한 버전이다.</p>
    {build_toc()}
  </section>
  {''.join(sections)}
  {raw_preserved}
  <section class="quiz-box">{quiz}</section>
  <section class="answer-box">{answer}</section>
  <section class="try">{review}</section>
  <aside class="source-note">
    <h2>{icon('note')}<span>출처와 생성 기준</span></h2>
    <p>입력 원문: <code>/Users/iriver/Downloads/loop_engineering_notes.md</code>. 최신 로컬 <code>adaptive-html-final</code> 스킬 자산을 사용했고, 8개 테마 스위처와 vt/wg 템플릿을 포함했다.</p>
  </aside>
</main>
""".strip()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCES.mkdir(parents=True, exist_ok=True)
    SOURCE_ASSETS.mkdir(parents=True, exist_ok=True)

    raw = INPUT.read_text()
    core_hash, css, asset_hashes = build_css()

    base = (ASSETS / "base.html").read_text()
    base = base.replace("{{TITLE}}", "루프 엔지니어링 정리")
    base = base.replace(
        "{{DESCRIPTION}}",
        "에이전트가 조사, 실행, 테스트, 실패 분석, 개선, 검증, 기억을 반복하도록 만드는 루프 엔지니어링 교육 문서.",
    )
    for name in INLINE_ASSETS:
        base = base.replace(SLOT_BY_ASSET[name], (ASSETS / name).read_text())
    base = base.replace(
        (ASSETS / "theme.css").read_text(),
        f"/* adaptive-html-final-core-css-sha256: {core_hash} */\n" + (ASSETS / "theme.css").read_text(),
        1,
    )
    json_ld = {
        "@context": "https://schema.org",
        "@type": "LearningResource",
        "name": "루프 엔지니어링 정리",
        "inLanguage": "ko",
        "learningResourceType": "교육 모듈",
        "educationalLevel": "intermediate",
        "description": "AI 에이전트 운영을 반복 가능한 개선 루프로 설계하는 방법을 설명하는 교육 문서.",
    }
    base = base.replace(
        "{{JSON_LD_BLOCK}}",
        '<script type="application/ld+json">'
        + json.dumps(json_ld, ensure_ascii=False)
        + "</script>",
    )
    base = base.replace("{{BODY}}", build_body(raw))
    base = base.replace("{{FOOTER}}", "")

    unresolved = re.findall(r"\{\{[A-Z0-9_]+\}\}", base)
    if unresolved:
        raise RuntimeError(f"Unresolved template placeholder remains: {sorted(set(unresolved))}")

    (OUT / "index.html").write_text(base)
    (SOURCES / "profile.json").write_text(json.dumps({"profile": "auto"}, ensure_ascii=False, indent=2) + "\n")
    manifest_text = (SKILL / "manifest.json").read_text()
    (SOURCES / "adaptive-html-final-manifest.json").write_text(manifest_text)
    (SOURCES / "css-integrity.json").write_text(
        json.dumps(build_integrity(core_hash, asset_hashes), ensure_ascii=False, indent=2) + "\n"
    )
    (SOURCES / "input-loop_engineering_notes.md").write_text(raw)


if __name__ == "__main__":
    main()
