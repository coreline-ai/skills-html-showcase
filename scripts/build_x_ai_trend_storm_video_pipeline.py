#!/usr/bin/env python3
"""Build an adaptive-html-final report from x-ai-trend-collector + STORM research.

This is deliberately layout-first:
- local x-ai-trend-collector instructions define the record schema and web-search fallback caveat
- local storm-research instructions define multi-perspective scan / contradiction / synthesis / peer review
- adaptive-html-final assets provide the rendered, no-behavior-JS final HTML
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
X_SKILL = ROOT / "orginal_skill" / "x-ai-trend-collector"
STORM_SKILL = ROOT / "orginal_skill" / "storm-research"

OUT = ROOT / "output" / "2026-06-20" / "x-ai-trend-storm-video-pipeline"
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
    "collection": "search",
    "storm": "question",
    "operating": "flow",
    "risk": "warning",
    "roadmap": "timeline",
    "review": "audit",
    "source": "source",
    "decision": "decision",
    "check": "check",
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
    rendered = markdownish_to_html(text)
    return (
        f'<details class="source-preserve" style="margin:36px 0 0 18px;border-left:6px solid var(--accent)"{open_attr}>'
        f'<summary style="padding:20px 26px 20px 58px;display:flex;align-items:center;gap:12px;flex-wrap:wrap">'
        f'<strong>{esc(title)}</strong><span class="tag">근거 보존</span></summary>'
        f'<div class="source-body" style="padding:0 28px 30px 58px">'
        f'<div style="border-left:1px solid var(--line);padding:26px 0 2px 24px">{rendered}</div>'
        f"</div></details>"
    )


SOURCES_LIST = [
    {
        "name": "OpenAI Help Center · Sora discontinuation",
        "url": "https://help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation",
        "role": "Sora web/app 종료일과 API 종료일 확인",
    },
    {
        "name": "OpenAI API Docs · Video generation with Sora",
        "url": "https://developers.openai.com/api/docs/guides/video-generation",
        "role": "Sora 2/Videos API deprecation 및 rapid iteration vs production-quality 구분",
    },
    {
        "name": "Google Blog · Veo 3.1 and Flow advanced capabilities",
        "url": "https://blog.google/innovation-and-ai/products/veo-updates-flow/",
        "role": "Flow·Veo 3.1의 오디오·편집·제어 기능 확인",
    },
    {
        "name": "Google Blog · Generative media models at I/O 2025",
        "url": "https://blog.google/innovation-and-ai/products/generative-media-models-io-2025/",
        "role": "Veo 3, Imagen 4, Flow 발표와 영상+오디오 방향 확인",
    },
    {
        "name": "Runway · Introducing Gen-4",
        "url": "https://runwayml.com/research/introducing-runway-gen-4",
        "role": "캐릭터·장소·오브젝트 일관성 중심의 제작 흐름 확인",
    },
    {
        "name": "Adobe Blog · Firefly Video Model",
        "url": "https://blog.adobe.com/en/publish/2025/02/12/meet-firefly-video-model-ai-powered-creation-with-unparalleled-creative-control",
        "role": "IP 친화·상업적 안전성 포지셔닝 확인",
    },
    {
        "name": "Luma · Ray",
        "url": "https://lumalabs.ai/ray",
        "role": "multi-keyframe, reframe, footage modification 등 감독형 워크플로우 확인",
    },
    {
        "name": "Pika · Agent / MCP",
        "url": "https://pika.me/",
        "role": "영상·이미지·음악·보이스오버를 에이전트/MCP로 묶는 방향 확인",
    },
    {
        "name": "Kling · VIDEO 3.0 Omni User Guide",
        "url": "https://kling.ai/quickstart/klingai-video-3-omni-model-user-guide",
        "role": "native audio, multimodal input/output, storyboarding, consistency control 확인",
    },
    {
        "name": "Stanford STORM Research Project",
        "url": "https://storm-project.stanford.edu/research/storm/",
        "role": "다관점 질문·검색 grounding 방법론 확인",
    },
    {
        "name": "STORM paper · arXiv 2402.14207",
        "url": "https://arxiv.org/abs/2402.14207",
        "role": "STORM 원논문 추적성",
    },
]


TREND_RECORDS = [
    {
        "cat": "업계·투자 뉴스",
        "author": "OpenAI Help Center",
        "handle": "openai.com",
        "date": "2026-06-17",
        "summary": "Sora 웹·앱은 2026-04-26 종료됐고 API는 2026-09-24 종료 예정으로 공지됐다. AI 영상 파이프라인은 단일 공급자 의존을 줄이고 모델 라우팅·마이그레이션 플랜을 가져야 한다.",
        "url": "https://help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation",
        "views": 0,
        "likes": 0,
    },
    {
        "cat": "신규 모델·제품 출시",
        "author": "OpenAI API Docs",
        "handle": "developers.openai.com",
        "date": "2026-06-20",
        "summary": "Sora 2 문서는 빠른 탐색용 모델과 고품질 출력용 Pro 모델을 구분하지만 Videos API 종료 일정도 함께 명시한다. 기획·러프컷·최종 납품을 분리한 모델 선택표가 필요하다.",
        "url": "https://developers.openai.com/api/docs/guides/video-generation",
        "views": 0,
        "likes": 0,
    },
    {
        "cat": "신규 모델·제품 출시",
        "author": "Google",
        "handle": "blog.google",
        "date": "2025-10-15",
        "summary": "Veo 3.1과 Flow 업데이트는 오디오, Ingredients/Frames to Video, Extend, Insert/Remove 같은 편집 제어를 강화했다. AI 영상은 단발 생성보다 장면 수정·연장·재구성 워크플로우로 이동 중이다.",
        "url": "https://blog.google/innovation-and-ai/products/veo-updates-flow/",
        "views": 0,
        "likes": 0,
    },
    {
        "cat": "신규 모델·제품 출시",
        "author": "Google",
        "handle": "blog.google",
        "date": "2025-05-20",
        "summary": "Google은 Veo 3, Imagen 4, Flow를 함께 발표하며 영상·이미지·스토리텔링 도구를 묶었다. 제작팀 관점에서는 모델 하나보다 프리프로덕션부터 에셋 생성까지 이어지는 제품군 통합이 핵심이다.",
        "url": "https://blog.google/innovation-and-ai/products/generative-media-models-io-2025/",
        "views": 0,
        "likes": 0,
    },
    {
        "cat": "신규 모델·제품 출시",
        "author": "Runway",
        "handle": "runwayml.com",
        "date": "2025-03-31",
        "summary": "Runway Gen-4는 레퍼런스와 지시문만으로 캐릭터·장소·오브젝트 일관성을 유지하는 방향을 강조한다. 브랜드/시리즈형 영상에서는 생성 품질보다 반복 등장 요소의 일관성이 병목이다.",
        "url": "https://runwayml.com/research/introducing-runway-gen-4",
        "views": 0,
        "likes": 0,
    },
    {
        "cat": "실무 팁·도구",
        "author": "Adobe",
        "handle": "blog.adobe.com",
        "date": "2025-02-12",
        "summary": "Adobe Firefly Video Model은 IP 친화·상업적 안전성을 핵심 메시지로 내세운다. 기업용 영상 파이프라인은 생성 품질뿐 아니라 학습 데이터, 권리, 보상, 투명성 검토를 조달 조건으로 삼아야 한다.",
        "url": "https://blog.adobe.com/en/publish/2025/02/12/meet-firefly-video-model-ai-powered-creation-with-unparalleled-creative-control",
        "views": 0,
        "likes": 0,
    },
    {
        "cat": "실무 팁·도구",
        "author": "Luma AI",
        "handle": "lumalabs.ai",
        "date": "2026-06-20",
        "summary": "Luma Ray는 multi-keyframe, 기존 footage 수정, reframe, motion transfer 같은 감독형 제어를 내세운다. 프롬프트 한 번보다 키프레임·비율·성능 전이를 관리하는 제작 표준이 중요해졌다.",
        "url": "https://lumalabs.ai/ray",
        "views": 0,
        "likes": 0,
    },
    {
        "cat": "실무 팁·도구",
        "author": "Pika",
        "handle": "pika.me",
        "date": "2026-06-20",
        "summary": "Pika는 Agent와 MCP를 통해 영상·이미지·음악·오디오·보이스오버 생성/편집을 에이전트 작업공간에 붙이는 방향을 보여준다. 콘텐츠팀의 다음 병목은 모델 사용법보다 에이전트 호출·승인·브랜드 가드레일이다.",
        "url": "https://pika.me/",
        "views": 0,
        "likes": 0,
    },
    {
        "cat": "신규 모델·제품 출시",
        "author": "Kling AI",
        "handle": "kling.ai",
        "date": "2026-02-06",
        "summary": "Kling VIDEO 3.0 Omni는 multimodal input/output, native audio, storyboard control, element consistency를 결합한다. AI 영상 경쟁축은 해상도보다 멀티모달 제어와 내러티브 일관성으로 이동한다.",
        "url": "https://kling.ai/quickstart/klingai-video-3-omni-model-user-guide",
        "views": 0,
        "likes": 0,
    },
    {
        "cat": "연구·논문 동향",
        "author": "Stanford OVAL",
        "handle": "storm-project.stanford.edu",
        "date": "2024-02-22",
        "summary": "STORM은 Retrieval과 Multi-perspective Question Asking으로 긴 글의 사전조사·개요·출처 grounding을 개선하는 방법론이다. 이번 산출물은 이를 AI 영상 트렌드 리서치의 관점 분리와 동료 검토에 적용했다.",
        "url": "https://storm-project.stanford.edu/research/storm/",
        "views": 0,
        "likes": 0,
    },
]


STORM_SCAN = {
    "Skeptic": {
        "persona": "회의주의자",
        "summary": "AI 영상 모델의 빠른 교체와 서비스 종료는 제작 자동화의 가장 큰 운영 리스크다.",
        "body": "OpenAI Sora의 웹·앱 종료와 API 종료 일정은 '최고 모델을 고르면 된다'는 접근을 깨뜨린다. 생산 파이프라인은 특정 생성 모델보다 입력 에셋, 프롬프트 기록, 승인 로그, 대체 모델 라우팅을 중심으로 설계해야 한다. 또한 Adobe가 상업적 안전성을 전면에 내세우는 이유는 권리·투명성·보상 이슈가 기업 도입의 실질 게이트이기 때문이다.",
        "sources": [
            "https://help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation",
            "https://blog.adobe.com/en/publish/2025/02/12/meet-firefly-video-model-ai-powered-creation-with-unparalleled-creative-control",
        ],
    },
    "Economist": {
        "persona": "경제학자",
        "summary": "비용 우위는 모델 단가가 아니라 반복 수정·검수·재사용 자산에서 나온다.",
        "body": "Veo/Flow, Runway Gen-4, Luma Ray, Kling 3.0은 모두 단발 생성보다 제어·수정·일관성을 앞세운다. 이는 영상 제작비의 중심이 렌더링 한 번의 가격이 아니라 재시도 횟수, 에셋 재사용률, 브랜드 검수 속도로 이동한다는 신호다. 작은 팀은 모델별 결과를 비교하는 시간보다 '러프컷은 빠른 모델, 브랜드/납품 컷은 일관성 모델, 권리 민감 컷은 안전성 모델' 같은 라우팅 규칙을 먼저 만들 때 비용이 줄어든다.",
        "sources": [
            "https://blog.google/innovation-and-ai/products/veo-updates-flow/",
            "https://runwayml.com/research/introducing-runway-gen-4",
            "https://lumalabs.ai/ray",
        ],
    },
    "Historian": {
        "persona": "역사학자",
        "summary": "AI 영상은 '텍스트 한 줄로 영화'가 아니라 NLE·CGI·템플릿 제작의 새 자동화 레이어로 흡수되고 있다.",
        "body": "과거 데스크톱 퍼블리싱과 비선형 편집 도구가 전문가를 대체하기보다 제작 단계를 재배치했듯, AI 영상도 프롬프트 장난감에서 편집·리파인·레퍼런스·스토리보드 도구로 이동한다. Google Flow, Runway Gen-4, Kling 3.0 Omni의 공통점은 제작자가 장면, 캐릭터, 오디오, 컷 전환을 반복 통제하게 한다는 점이다.",
        "sources": [
            "https://blog.google/innovation-and-ai/products/generative-media-models-io-2025/",
            "https://kling.ai/quickstart/klingai-video-3-omni-model-user-guide",
        ],
    },
    "Academic": {
        "persona": "학자",
        "summary": "핵심 연구 과제는 시간 일관성, 멀티모달 동기화, 출처·편향 전이다.",
        "body": "STORM 방법론이 경고하는 source bias transfer와 over-association는 AI 영상 트렌드 리포트에도 그대로 적용된다. 이번 자료는 대부분 공급자 공식 페이지라 기능 로드맵을 빠르게 보여주지만, 벤치마크나 독립 사용자 연구는 부족하다. 따라서 결론은 '검증된 성능 순위'가 아니라 '공급자들이 공통으로 밀고 있는 제어 축'으로 읽어야 한다.",
        "sources": [
            "https://storm-project.stanford.edu/research/storm/",
            "https://arxiv.org/abs/2402.14207",
        ],
    },
    "Futurist": {
        "persona": "미래학자",
        "summary": "다음 경쟁은 AI 영상 모델 자체보다 agentic creative stack이다.",
        "body": "Pika의 Agent/MCP, Google Flow의 제작 도구화, Luma의 감독형 제어는 콘텐츠 제작을 '모델 호출'에서 '에이전트가 에셋·샷·오디오·수정 요청을 관리하는 워크플로우'로 바꾼다. 2026년 작은 팀의 승부처는 도구 하나의 마스터리가 아니라 기획→레퍼런스→생성→검수→재편집→배포를 무 JS가 아니라 무마찰로 잇는 운영 설계다.",
        "sources": [
            "https://pika.me/",
            "https://labs.google/fx/tools/flow",
            "https://lumalabs.ai/ray",
        ],
    },
}


CONTRADICTIONS = [
    ["최고 모델 하나를 고르면 된다", "OpenAI Sora 사례처럼 제품·API 수명은 바뀐다", "모델 라우팅·대체 경로·원본 에셋 보존이 더 중요"],
    ["AI 영상은 프롬프트 한 번으로 끝난다", "Veo/Flow·Luma·Kling은 편집·키프레임·스토리보드를 강조한다", "제작 표준은 생성보다 리비전 루프 중심"],
    ["품질이 좋으면 기업 도입된다", "Adobe Firefly는 상업적 안전성과 IP 메시지를 전면화한다", "권리·출처·승인 로그가 조달 게이트"],
    ["자동화가 사람을 줄인다", "일관성·브랜드·오디오·검수는 새 인간 승인 지점을 만든다", "AI는 편집자를 없애기보다 감독/QA의 레버리지를 키움"],
    ["트렌드는 소셜 engagement 순위로 판단한다", "직접 X/API 수집이 없으면 engagement는 검증되지 않는다", "이번 리포트는 웹-search fallback 근거 리포트로 한정"],
]


SYNTHESIS = """# STORM 종합
AI 영상 제작의 2026년 핵심은 '모델 대전'이 아니라 '운영 가능한 제작 시스템'이다. 공식 발표들의 공통 신호는 native audio, reference/character consistency, keyframe/storyboard control, edit/extend/remove 같은 반복 편집 능력, 그리고 상업적 안전성이다.

작은 팀이 바로 실행할 전략은 단순하다. 먼저 트렌드 수집을 records.json으로 고정하고, 각 아이디어를 콘셉트 보드로 만들며, 러프컷·브랜드 컷·권리 민감 컷에 다른 모델을 라우팅한다. 이후 source asset library, prompt/change log, human approval checklist, distribution package를 표준화한다.

결론: AI 영상 파이프라인의 해자는 '더 멋진 한 컷'이 아니라 '재현 가능한 제작 로그, 레퍼런스 보존, 검수 가능한 권리/브랜드/품질 계약'에서 만들어진다."""


PEER_REVIEW = """# 동료 검토
- BLOCKER 없음: 사용한 자료는 모두 공개 웹 출처이며, 직접 X engagement 수치를 발명하지 않았다.
- 주의 1: 대부분 공급자 공식 페이지라 제품 주장의 편향이 있다. 따라서 '성능 순위'가 아니라 '제품 방향 신호'로만 해석한다.
- 주의 2: OpenAI Sora의 종료 사례를 모든 공급자의 위험으로 과잉 일반화하지 않는다. 다만 운영 설계상 단일 공급자 종속을 줄이라는 교훈으로 사용한다.
- 주의 3: Pika/Luma/Flow의 agentic workflow 신호는 도구 소개 문구에 기반한 추론이다. 실제 팀 ROI는 별도 실험이 필요하다.
- 주의 4: x-ai-trend-collector의 직접 X/API 경로가 아니라 web-search fallback이므로 조회수·좋아요는 모두 0으로 둔다."""


def make_storm_markdown() -> tuple[str, str, str, str]:
    scan = ["# Multi-Perspective Scan · AI 영상 제작 파이프라인 2026"]
    for name, row in STORM_SCAN.items():
        scan.extend([
            f"## {name} · {row['persona']}",
            row["summary"],
            row["body"],
            "출처: " + ", ".join(row["sources"]),
            "",
        ])
    contradiction = "# Contradiction Map\n" + "\n".join(
        f"- {a} ↔ {b} → {c}" for a, b, c in CONTRADICTIONS
    )
    return "\n".join(scan), contradiction, SYNTHESIS, PEER_REVIEW


def build_executive_summary() -> str:
    category_counts: dict[str, int] = {}
    for rec in TREND_RECORDS:
        category_counts[rec["cat"]] = category_counts.get(rec["cat"], 0) + 1
    counts = "".join(
        f'<article class="summary-card"><h3>{esc(cat)}</h3><p>{n}개 근거 · engagement 미추정(0)</p></article>'
        for cat, n in category_counts.items()
    )
    return f"""
{h2('01', 'Executive Summary · AI 영상은 모델 선택에서 제작 운영체계로 이동', 'summary', 'x-ai-trend-collector의 웹검색 fallback 레코드와 STORM 5관점 리서치를 합쳐 현재 adaptive-html-final 전문가 리포트로 재구성했다.')}
<div class="lede-note"><span class="label">핵심 판정</span><p><strong>2026년 AI 영상 제작의 병목은 “어느 모델이 더 예쁜가”가 아니라 기획·레퍼런스·샷 제어·오디오·권리·검수·배포를 반복 가능한 운영 시스템으로 묶는 능력</strong>이다. Sora 종료 일정은 단일 공급자 의존 리스크를 드러냈고, Veo/Flow·Runway·Luma·Kling·Pika·Adobe는 모두 제어·일관성·상업적 안전성·agentic workflow 쪽으로 수렴한다.</p></div>
<div class="card-grid rail-cycle">
  <article class="summary-card"><h3>Trend signal</h3><p>오디오 내장, 스토리보드, 레퍼런스 일관성, keyframe/reframe, agent/MCP가 반복적으로 등장한다.</p></article>
  <article class="summary-card"><h3>Operating signal</h3><p>프롬프트 한 번이 아니라 모델 라우팅, source asset library, approval log, fallback model 표준이 필요하다.</p></article>
  <article class="summary-card"><h3>Risk signal</h3><p>Sora 종료와 Adobe의 상업적 안전성 메시지는 모델 성능보다 제품 수명·권리·조달 게이트가 중요함을 보여준다.</p></article>
  <article class="summary-card"><h3>Action signal</h3><p>작은 팀은 30일 안에 레퍼런스 라이브러리, 러프컷/납품컷 라우팅표, 검수 체크리스트를 만들면 바로 차별화된다.</p></article>
</div>
<div class="card-grid rail-cycle">{counts}</div>
{table([
    ['최종 결론', 'AI 영상은 생성 도구가 아니라 제작 운영체계로 다뤄야 한다.', 'tool-by-tool 비교보다 workflow contract 작성'],
    ['모델 라우팅', '러프컷/브랜드컷/권리 민감 컷을 한 공급자에 묶지 않는다.', '속도·품질·권리·연속성 기준표'],
    ['자산 관리', '레퍼런스 이미지, 캐릭터 룩, 프롬프트, 시드, 승인 로그가 재사용 자산이다.', 'source asset library'],
    ['검수 기준', '오디오·스토리·브랜드·권리·워터마크/출처를 컷마다 확인한다.', 'human approval checklist'],
    ['트렌드 수집', '직접 X/API가 없으면 engagement를 추정하지 않는다.', 'views/likes=0 + source-bound records'],
], 'AI 영상 파이프라인 2026 핵심 판단', ['항목', '판정', '실행 산출물'])}
"""


def build_decision_cards(scan_md: str) -> str:
    cards = []
    details = []
    for idx, (name, row) in enumerate(STORM_SCAN.items()):
        cards.append(
            f'<article class="mini-card" style="padding-top:22px"><span class="tag" style="display:inline-flex;margin-bottom:16px">{esc(name)} · {esc(row["persona"])}</span><h3 style="margin-top:0;margin-bottom:12px">{esc(row["summary"])}</h3><p style="margin-top:0">{esc(row["body"])}</p></article>'
        )
        details.append(source_details(f'{name} · {row["persona"]} 관점 원문', f'{row["summary"]}\n\n{row["body"]}\n\n출처: ' + ', '.join(row["sources"]), open_=idx == 0))
    return f"""
{h2('02', 'Decision Cards · STORM 다섯 관점이 남긴 의사결정 질문', 'storm', '회의주의자·경제학자·역사학자·학자·미래학자 관점을 분리해 단일 모델 홍보문으로 수렴하지 않게 했다.')}
<div class="card-grid rail-cycle">{''.join(cards)}</div>
<div class="core-insight core-insight--plain-text"><blockquote>질문은 “어떤 AI 영상 모델이 제일 강한가?”가 아니라 “어떤 제작 단계에서 어떤 실패비용을 줄이는가?”다.</blockquote><p>모델 성능보다 더 오래 남는 것은 에셋 보존, 승인 로그, 리비전 루프, 권리 검수, 배포 패키지다.</p></div>
{''.join(details)}
{source_details('STORM Multi-Perspective Scan 통합 원문', scan_md, open_=False)}
"""


def build_collection_section() -> str:
    rows = []
    for rec in TREND_RECORDS:
        rows.append([
            rec["cat"],
            f'{esc(rec["author"])}<br><a href="{esc(rec["url"])}" target="_blank" rel="noopener noreferrer">원문</a>',
            rec["date"],
            esc(rec["summary"]),
        ])
    return f"""
{h2('03', 'Trend Records · x-ai-trend-collector 방식의 근거 레코드', 'collection', '직접 X/API가 아니라 공개 웹-search fallback으로 수집했기 때문에 모든 engagement metric은 0으로 두고 출처 URL을 dedupe key로 삼았다.')}
<div class="lede-note"><span class="label">수집 한계</span><p>직접 X/API·로그인 브라우저 수집이 아니라 공개 웹 근거 기반입니다. 따라서 “인기 X 포스트 순위”가 아니며 조회수·좋아요는 추정하지 않았습니다. 이 출력의 목적은 <strong>AI 영상 제작 파이프라인 의사결정에 필요한 source-bound trend record</strong>를 만드는 것입니다.</p></div>
{table(rows, 'x-ai-trend-collector records.json 요약 — URL dedupe / metrics unknown=0', ['카테고리', '출처', '날짜', '한국어 요약'])}
"""


def build_operating_model() -> str:
    wg16 = """
<div class="wg-16" aria-labelledby="wg-16-title">
  <header class="wg-16-head">
    <p class="wg-16-kicker">구현 계획서 · AI Video Operating System</p>
    <h3 id="wg-16-title" class="wg-16-h">Trend intake → concept board → model routing → approval log → distribution kit</h3>
    <p class="wg-16-lead">AI 영상 제작은 생성 버튼이 아니라 운영 파이프라인이다. 아래 5단계를 표준화하면 모델이 바뀌어도 산출 품질과 책임 구조가 유지된다.</p>
  </header>
  <div class="wg-16-panel">
    <h3 class="wg-16-h3">마일스톤 타임라인</h3>
    <ol class="wg-16-ms">
      <li class="wg-16-ms-item wg-16-done"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">M0 · Trend record schema 고정</span><span class="wg-16-badge wg-16-bd-done">완료</span></div><p class="wg-16-ms-desc">카테고리, 작성자, 날짜, 요약, URL, views/likes=0 규칙을 고정한다.</p></div></li>
      <li class="wg-16-ms-item wg-16-active"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">M1 · 0~30일: 제작 계약 표준화</span><span class="wg-16-badge wg-16-bd-active">현재</span></div><p class="wg-16-ms-desc">콘셉트 보드, 레퍼런스 라이브러리, 모델 라우팅표, 승인 체크리스트를 만든다.</p></div></li>
      <li class="wg-16-ms-item"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">M2 · 31~60일: 리비전 루프 계측</span><span class="wg-16-badge">예정</span></div><p class="wg-16-ms-desc">프롬프트/시드/모델/출력/검수 로그를 컷 단위로 기록한다.</p></div></li>
      <li class="wg-16-ms-item"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">M3 · 61~90일: 배포 패키지 자동화</span><span class="wg-16-badge">예정</span></div><p class="wg-16-ms-desc">플랫폼별 컷다운, 썸네일, 자막, 메타데이터, 권리 고지를 묶는다.</p></div></li>
    </ol>
    <h3 class="wg-16-h3">데이터 플로우</h3>
    <div class="wg-16-flow" aria-label="AI 영상 제작 데이터 플로우">
      <div class="wg-16-fnode">트렌드 수집<span class="wg-16-fnode-s">records.json</span></div>
      <div class="wg-16-fnode wg-16-fnode-good">콘셉트 보드<span class="wg-16-fnode-s">shot·audience</span></div>
      <div class="wg-16-fnode">모델 라우팅<span class="wg-16-fnode-s">speed·quality·rights</span></div>
      <div class="wg-16-fnode wg-16-fnode-hot">검수 로그<span class="wg-16-fnode-s">brand·audio·IP</span></div>
      <div class="wg-16-fnode wg-16-fnode-q">배포 키트<span class="wg-16-fnode-s">formats·metadata</span></div>
    </div>
    <h3 class="wg-16-h3">리스크 평가</h3>
    <div class="wg-16-table-wrap"><div class="table-scroll"><table class="wg-16-table"><caption>AI 영상 제작 운영 리스크</caption><thead><tr><th scope="col">리스크</th><th scope="col">가능성</th><th scope="col">영향</th><th scope="col">완화책</th></tr></thead><tbody>
      <tr><th scope="row">공급자 API/제품 종료</th><td><span class="wg-16-lv wg-16-lv-mid">중</span></td><td><span class="wg-16-lv wg-16-lv-hi">높음</span></td><td>대체 모델 라우팅표와 원본 에셋 보존</td></tr>
      <tr><th scope="row">권리·상업적 안전성 불확실</th><td><span class="wg-16-lv wg-16-lv-mid">중</span></td><td><span class="wg-16-lv wg-16-lv-hi">높음</span></td><td>소스·라이선스·승인 로그와 민감 컷 분리</td></tr>
      <tr><th scope="row">캐릭터/브랜드 일관성 붕괴</th><td><span class="wg-16-lv wg-16-lv-hi">높음</span></td><td><span class="wg-16-lv wg-16-lv-mid">중</span></td><td>레퍼런스 라이브러리, keyframe, human QA</td></tr>
    </tbody></table></div></div>
  </div>
</div>
"""
    raci = table([
        ["Creative Director", "콘셉트, 샷 우선순위, 브랜드 톤 결정", "콘셉트 보드·승인 코멘트"],
        ["AI Video Operator", "모델 라우팅, 프롬프트·키프레임·리비전 실행", "prompt/change log"],
        ["Rights/Brand Reviewer", "상업적 안전성, 레퍼런스 권리, 금지 요소 검수", "rights checklist"],
        ["Editor/Post", "오디오, 컷다운, 자막, 플랫폼 포맷 마감", "distribution kit"],
        ["Trend Analyst", "records.json 갱신, 출처 URL 검증, 과장 제거", "weekly trend brief"],
    ], "AI 영상 파이프라인 RACI", ["역할", "책임", "증빙"])
    return f"""
{h2('04', 'Operating Model · 90일 안에 만들 AI 영상 제작 운영체계', 'operating', 'expert_html의 운영 모델 블록에 wg-16 implementation-plan 위젯을 삽입했다.')}
{wg16}
{raci}
"""


def build_risk_matrix(contradiction_md: str) -> str:
    vt = """
<div class="vt-shell">
  <div class="vt-frame">
    <div class="rm-grid"><div class="rm-cell rm-head">가능성</div><div class="rm-cell rm-head">낮음</div><div class="rm-cell rm-head">중간</div><div class="rm-cell rm-head">높음</div><div class="rm-cell rm-head">영향 큼</div><div class="rm-cell rm-risk med">공식 자료 편향</div><div class="rm-cell rm-risk high">API/제품 종료</div><div class="rm-cell rm-risk high">권리·IP 리스크</div><div class="rm-cell rm-head">영향 중간</div><div class="rm-cell rm-risk low">트렌드 과장</div><div class="rm-cell rm-risk med">리비전 비용 폭증</div><div class="rm-cell rm-risk med">캐릭터 일관성 붕괴</div><div class="rm-cell rm-head">영향 작음</div><div class="rm-cell rm-risk low">툴 UI 변경</div><div class="rm-cell rm-risk low">메타데이터 누락</div><div class="rm-cell rm-risk low">포맷 재작업</div></div>
  </div>
</div>
"""
    return f"""
{h2('05', 'Risk Matrix · 모델 대전 뒤에 숨은 운영 리스크', 'risk', 'expert_html 모드의 1순위 vt risk-matrix를 사용해 모순 지도를 실행 리스크로 변환했다.')}
<figure aria-label="AI 영상 제작 운영 위험 매트릭스"><figcaption>vt risk-matrix · STORM 모순 지도 기반</figcaption>{vt}</figure>
{table(CONTRADICTIONS, 'STORM Contradiction Map — 봉합하지 않고 남긴 핵심 긴장', ['주장 A', '충돌 근거', '실행 해석'])}
{source_details('Contradiction Map 원문', contradiction_md, open_=True)}
"""


def build_roadmap(synthesis_md: str) -> str:
    return f"""
{h2('06', 'Priority Roadmap · 작은 팀을 위한 30/60/90일 실행표', 'roadmap', '다관점 종합을 실제 제작팀 운영 루프로 변환했다.')}
<div class="impact-grid">
  <article><strong>0~7일</strong><p>trend records 10건을 고정하고 source URL·요약·한계를 기록한다.</p></article>
  <article><strong>8~30일</strong><p>러프컷/납품컷/권리민감컷 모델 라우팅표와 레퍼런스 라이브러리를 만든다.</p></article>
  <article><strong>31~60일</strong><p>프롬프트·시드·모델·결과·승인 로그를 컷 단위로 남기는 QA 루프를 운영한다.</p></article>
  <article><strong>61~90일</strong><p>플랫폼별 컷다운, 자막, 썸네일, 메타데이터, rights note를 배포 키트로 자동화한다.</p></article>
</div>
{table([
    ['Trend intake', 'x-ai-trend-collector schema로 웹 근거 수집', 'records.json, Excel, supporting dashboard'],
    ['Concept board', '누구에게 어떤 영상 메시지를 만들지 정리', 'audience·offer·shot list'],
    ['Model routing', '속도/품질/권리/일관성 기준으로 모델 선택', 'routing matrix'],
    ['Asset memory', '캐릭터·제품·장소·로고 레퍼런스 보존', 'source asset library'],
    ['Approval loop', '브랜드·권리·오디오·자막·사실성 체크', 'human approval checklist'],
    ['Distribution kit', '각 플랫폼 규격과 메타데이터로 마감', 'shorts/reels/ads package'],
], 'AI 영상 제작 파이프라인 실행 순서', ['단계', '내용', '산출물'])}
{source_details('STORM Synthesis 원문', synthesis_md, open_=True)}
"""


def build_review(peer_md: str) -> str:
    return f"""
{h2('07', 'Peer Review · 과장·출처 편향·직접 X 미수집 한계', 'review', 'STORM peer review 계약에 따라 source bias transfer와 over-association를 명시적으로 점검했다.')}
{table([
    ['PASS', '출처 없는 수치·engagement 추정 없음', 'views/likes는 모두 0으로 고정'],
    ['CAUTION', '공급자 공식 페이지 중심', '성능 순위가 아니라 방향 신호로 제한'],
    ['CAUTION', 'OpenAI Sora 종료를 전체 시장 종료로 과잉 일반화 금지', '단일 공급자 종속 리스크로만 사용'],
    ['CAUTION', 'Pika/Luma/Flow의 agentic workflow는 제품 소개 기반 추론', '팀 ROI는 별도 파일럿 필요'],
    ['PASS', '최종 adaptive HTML은 외부/동작 JS 없이 생성', 'JSON-LD만 허용'],
], '동료 검토 결과', ['판정', '검토 항목', '반영'])}
<div class="accessibility-checklist"><h3>완료 기준</h3><ul><li>records.json과 STORM 산출물이 sources에 남아야 한다.</li><li>최종 HTML은 adaptive-html-final v{version()} manifest와 CSS snapshot을 포함해야 한다.</li><li>검증은 validate_output, quality_contract, render_audit, completion_check까지 통과해야 한다.</li></ul></div>
{source_details('Peer Review 원문', peer_md, open_=True)}
"""


def build_final_recommendation() -> str:
    return f"""
{h2('08', 'Next Actions · 바로 실행할 제작 루프', 'check', '이번 주에 바로 적용할 수 있는 AI 영상 제작 체크리스트다.')}
<ol>
  <li><strong>Trend:</strong> 매주 10개 record를 추가하고 URL·요약·metrics=0/unknown 규칙을 유지한다.</li>
  <li><strong>Brief:</strong> 한 영상마다 목적, 대상, CTA, 금지 요소, 레퍼런스 자산을 한 장으로 고정한다.</li>
  <li><strong>Route:</strong> 러프컷은 빠른 모델, 브랜드/캐릭터 컷은 일관성 모델, 민감 광고는 상업적 안전성 기준으로 나눈다.</li>
  <li><strong>Generate:</strong> 프롬프트·모델·파라미터·출력 파일명을 컷 단위로 로그화한다.</li>
  <li><strong>Review:</strong> 오디오 싱크, 브랜드 일관성, 권리, 자막, 플랫폼 규격을 사람 검수로 통과시킨다.</li>
  <li><strong>Package:</strong> Shorts/Reels/Ads별 컷다운, 썸네일, 설명문, 출처/권리 노트를 함께 묶는다.</li>
</ol>
<p><strong>성공 기준:</strong> 더 예쁜 데모가 아니라 같은 콘셉트를 다른 모델로 재생성해도 브랜드·권리·스토리·배포 품질이 유지되는 것이다.</p>
"""


def build_source_note() -> str:
    links_html = "".join(
        f'<li><a href="{esc(src["url"])}" target="_blank" rel="noopener noreferrer">{esc(src["name"])}</a> — {esc(src["role"])}</li>'
        for src in SOURCES_LIST
    )
    return f"""
<h2>{body_icon('source')}<span class="num">09</span>Source Hub · 근거·스킬·보조 산출물</h2>
<p class="h2-sub">이번 출력은 x-ai-trend-collector의 record schema/web-search fallback, storm-research의 5관점·모순·종합·동료 검토, adaptive-html-final v{version()}의 expert_html 레이아웃을 결합했다.</p>
<div class="source-note"><p><strong>보조 산출물:</strong> <a href="sources/x-ai-trend-records.json">records.json</a> · <a href="sources/storm-scan.md">storm-scan.md</a> · <a href="sources/storm-contradiction-map.md">contradiction-map.md</a> · <a href="sources/storm-synthesis.md">synthesis.md</a> · <a href="sources/storm-peer-review.md">peer-review.md</a> · <a href="sources/x-ai-trend-collector-artifacts/AI_영상_트렌드_리포트.xlsx">x-ai-trend Excel</a> · <a href="sources/x-ai-trend-collector-artifacts/AI_영상_트렌드_대시보드.html">x-ai-trend dashboard</a></p><p><strong>중요:</strong> 최종 adaptive-html-final HTML은 무 동작 JS 계약을 지키며, x-ai-trend-collector의 원본 dashboard는 supporting artifact로만 둔다.</p></div>
<ol class="refs">{links_html}</ol>
"""


def copy_sources(scan_md: str, contradiction_md: str, synthesis_md: str, peer_md: str) -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "pages").mkdir(parents=True, exist_ok=True)
    SOURCES.mkdir(parents=True, exist_ok=True)
    (SOURCES / "assets").mkdir(parents=True, exist_ok=True)
    (SOURCES / "screenshots").mkdir(parents=True, exist_ok=True)
    (SOURCES / "x-ai-trend-collector-artifacts").mkdir(parents=True, exist_ok=True)

    (SOURCES / "x-ai-trend-records.json").write_text(json.dumps(TREND_RECORDS, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (SOURCES / "source-list.json").write_text(json.dumps(SOURCES_LIST, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (SOURCES / "storm-scan.md").write_text(scan_md + "\n", encoding="utf-8")
    (SOURCES / "storm-contradiction-map.md").write_text(contradiction_md + "\n", encoding="utf-8")
    (SOURCES / "storm-synthesis.md").write_text(synthesis_md + "\n", encoding="utf-8")
    (SOURCES / "storm-peer-review.md").write_text(peer_md + "\n", encoding="utf-8")
    (SOURCES / "storm-report.json").write_text(json.dumps({
        "topic": "AI 영상 제작 파이프라인 2026",
        "mode": "solo-fallback-by-main-agent",
        "souls": STORM_SCAN,
        "contradictions": CONTRADICTIONS,
        "synthesis": synthesis_md,
        "peer_review": peer_md,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (SOURCES / "collection-caveat.md").write_text(
        "Direct X/API collection was unavailable in this run, so public web-search evidence was normalized into x-ai-trend-collector records. Engagement metrics are set to 0 rather than guessed.\n",
        encoding="utf-8",
    )
    shutil.copyfile(SKILL / "manifest.json", SOURCES / "adaptive-html-final-manifest.json")
    (SOURCES / "profile.json").write_text(json.dumps({"profile": PROFILE}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (SOURCES / "layout-placeholder-map.json").write_text(json.dumps({
        "layout": LAYOUT,
        "KICKER": "x-ai trend collector + STORM research",
        "TITLE": "AI 영상 제작 파이프라인 2026",
        "SUBTITLE": "AI 영상 트렌드 수집과 다관점 리서치 기반 전문가 리포트",
        "EXECUTIVE_SUMMARY": "핵심 판단과 카테고리 분포",
        "DECISION_CARDS": "STORM 5관점 카드와 원문 details",
        "ARCHITECTURE": "x-ai trend records 표",
        "RISK_MATRIX": "vt risk-matrix + contradiction map",
        "PRIORITY_ROADMAP": "30/60/90일 실행표 + synthesis",
        "VALIDATION_CHECKLIST": "peer review와 검증 기준",
        "FINAL_RECOMMENDATION": "즉시 실행 체크리스트",
        "SOURCE_NOTE": "출처 허브와 보조 산출물",
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
        "skills/adaptive-html-final/assets/layouts/expert-report.html",
        "skills/adaptive-html-final/assets/visual-html-templates/03-risk-matrix.html",
        "skills/adaptive-html-final/assets/widget-templates/16-implementation-plan.html",
        "skills/adaptive-html-final/references/layout-system.md",
        "skills/adaptive-html-final/references/writing-system.md",
        "orginal_skill/x-ai-trend-collector/SKILL.md",
        "orginal_skill/x-ai-trend-collector/references/web-search-fallback.md",
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
            "sources/x-ai-trend-records.json",
            "sources/storm-scan.md",
            "sources/storm-contradiction-map.md",
            "sources/storm-synthesis.md",
            "sources/storm-peer-review.md",
        ],
        "collection_route": "x-ai-trend-collector web-search fallback; metrics unknown=0",
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
        f'<span>adaptive-html-final v{version()}</span><span>x-ai records {len(TREND_RECORDS)}건</span>'
        f'<div class="generated-row"><p class="generated-date">생성 기준: 2026-06-20 KST · x-ai-trend-collector web fallback · STORM solo synthesis · layout-first</p>'
        f'<div class="lens-strip" aria-label="적용 렌즈"><span class="lens-strip-label">LENS</span><span class="lens-chip">회의주의</span><span class="lens-chip">경제학</span><span class="lens-chip">역사</span><span class="lens-chip">학술</span><span class="lens-chip">미래</span></div></div>'
    )
    body = layout
    replacements = {
        "{{KICKER}}": '<span class="kicker-text">x-ai-trend-collector × STORM × adaptive-html-final</span>',
        "{{TITLE}}": "AI 영상 제작 파이프라인 2026",
        "{{SUBTITLE}}": "공개 웹 기반 AI 영상 트렌드 레코드와 STORM 다관점 리서치를 결합해, 현재 프로젝트 최신 expert_html 스타일로 만든 하이브리드 리포트입니다.",
        "{{META}}": meta_inner,
        "{{EXECUTIVE_SUMMARY}}": build_executive_summary(),
        "{{DECISION_CARDS}}": build_decision_cards(scan_md),
        "{{ARCHITECTURE}}": build_collection_section() + build_operating_model(),
        "{{RISK_MATRIX}}": build_risk_matrix(contradiction_md),
        "{{PRIORITY_ROADMAP}}": build_roadmap(synthesis_md),
        "{{VALIDATION_CHECKLIST}}": build_review(peer_md),
        "{{FINAL_RECOMMENDATION}}": build_final_recommendation(),
        "{{SOURCE_NOTE}}": build_source_note(),
    }
    for key, value in replacements.items():
        body = body.replace(key, value)
    toc = (
        '<nav class="toc-map" id="document-toc" aria-label="문서 목차"><span class="label">문서 목차</span>'
        '<p>x-ai trend records, STORM 관점, 운영 모델, 리스크, 실행표로 이동합니다.</p>'
        '<div class="toc-pills">'
        '<a class="toc-pill" href="#executive-summary"><b>1</b>Executive</a>'
        '<a class="toc-pill" href="#decision-cards"><b>2</b>STORM</a>'
        '<a class="toc-pill" href="#collection"><b>3</b>Records</a>'
        '<a class="toc-pill" href="#operating"><b>4</b>Operating</a>'
        '<a class="toc-pill" href="#risk-matrix"><b>5</b>Risk</a>'
        '<a class="toc-pill" href="#roadmap"><b>6</b>Roadmap</a>'
        '<a class="toc-pill" href="#validation"><b>7</b>Review</a>'
        '<a class="toc-pill" href="#source-note"><b>8</b>Sources</a>'
        '</div></nav>'
    )
    body = body.replace('</header>\n  <section class="executive-summary">', '</header>\n  ' + toc + '\n  <section class="executive-summary" id="executive-summary">')
    body = body.replace('<section class="decision-section">', '<section class="decision-section" id="decision-cards">')
    body = body.replace('<section class="architecture-map">', '<section class="architecture-map" id="collection">')
    body = body.replace('<section class="risk-matrix">', '<section class="risk-matrix" id="risk-matrix">')
    body = body.replace('<section class="priority-roadmap">', '<section class="priority-roadmap" id="roadmap">')
    body = body.replace('<section class="validation-checklist">', '<section class="validation-checklist" id="validation">')
    body = body.replace('<section class="try">', '<section class="try" id="next-actions">')
    body = body.replace('<aside class="source-note">', '<aside class="source-note" id="source-note">')
    body = body.replace('<h2><span class="body-icon body-icon--sm"', '<h2><span class="body-icon body-icon--sm"', 1)
    # Add an anchor near the operating model without changing the official layout class.
    body = body.replace('<div class="wg-16" aria-labelledby="wg-16-title">', '<div id="operating" class="wg-16" aria-labelledby="wg-16-title">', 1)

    title = "AI 영상 제작 파이프라인 2026 · x-ai trend STORM report"
    description = f"x-ai-trend-collector web fallback records와 STORM 다관점 리서치를 adaptive-html-final v{version()} expert_html 스타일로 결합한 AI 영상 제작 파이프라인 리포트."
    json_ld = json.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": description,
        "inLanguage": "ko",
        "datePublished": "2026-06-20",
        "author": {"@type": "Organization", "name": "adaptive-html-final"},
        "about": ["AI video generation", "creative workflow", "STORM research", "trend intelligence"],
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
    required = [
        "AI 영상 제작 파이프라인 2026",
        "x-ai-trend-collector",
        "직접 X/API",
        "회의주의자",
        "경제학자",
        "역사학자",
        "미래학자",
        "Contradiction Map",
        "Peer Review",
        "views/likes는 모두 0",
    ]
    visible = re.sub(r"<style\b[^>]*>[\s\S]*?</style>", "", doc, flags=re.I)
    visible = re.sub(r"<script\b[^>]*>[\s\S]*?</script>", "", visible, flags=re.I)
    visible = re.sub(r"<[^>]+>", " ", visible)
    visible = re.sub(r"\s+", " ", html.unescape(visible))
    missing = [x for x in required if x not in visible]
    evidence = {
        "records_count": len(TREND_RECORDS),
        "storm_soul_count": len(STORM_SCAN),
        "source_count": len(SOURCES_LIST),
        "required_markers_missing": missing,
        "output_visible_text_chars": len(visible),
        "pass": not missing and len(visible) > 9000,
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
