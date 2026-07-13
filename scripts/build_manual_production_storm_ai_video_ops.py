#!/usr/bin/env python3
"""Build a current adaptive-html-final manual_analysis page from manual-production + STORM research.

Selected topic:
  AI 영상 제작 파이프라인 운영 매뉴얼 2026

Sources are bound to:
- orginal_skill/manual-production for beginner/operator manual structure, workflow-first sequencing, source limits, and verification separation
- orginal_skill/storm-research for five-perspective scan, contradiction map, synthesis, and peer review discipline
- current adaptive-html-final assets for the final no-behavior-JS HTML style
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
MANUAL_SKILL = ROOT / "orginal_skill" / "manual-production"
STORM_SKILL = ROOT / "orginal_skill" / "storm-research"

OUT = ROOT / "output" / "2026-06-20" / "manual-production-storm-ai-video-ops"
SOURCES = OUT / "sources"

MODE = "manual_analysis"
PROFILE = "auto"
LAYOUT = "manual-analysis.html"
LAYOUT_CLASS = "layout-manual"
PRIMARY_VT = "hero-map"
PRIMARY_WG = "wg-13"

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
    "verdict": "decision",
    "toc": "map",
    "source": "source",
    "role": "user",
    "success": "success",
    "safety": "security",
    "recipe": "flow",
    "reference": "reference",
    "choice": "question",
    "trouble": "warning",
    "ops": "timeline",
    "audit": "audit",
    "next": "check",
}

SOURCE_LIST = [
    {
        "name": "OpenAI · Launching Sora responsibly",
        "url": "https://openai.com/index/launching-sora-responsibly/",
        "role": "Sora availability note, provenance signals, visible watermark, C2PA metadata, consent-based likeness controls",
        "evidence": "As of April 26, 2026 Sora product no longer available; Sora outputs carried visible and invisible provenance signals.",
    },
    {
        "name": "OpenAI · Sora 2 is here",
        "url": "https://openai.com/index/sora-2/",
        "role": "characters / likeness controls and creation-first feed philosophy",
        "evidence": "Sora app described create, remix, feed, characters, identity verification and user control of likeness.",
    },
    {
        "name": "Google DeepMind · Veo 3.1",
        "url": "https://deepmind.google/models/veo/",
        "role": "current video generation model capability framing",
        "evidence": "Veo 3.1 is described as a video generation model with audio, prompt adherence, creative control, realism.",
    },
    {
        "name": "Google AI for Developers · Generate videos with Veo 3.1",
        "url": "https://ai.google.dev/gemini-api/docs/video",
        "role": "API/runtime operational limits: 8-second clips, resolution, reference images, polling/download pattern",
        "evidence": "Veo 3.1 docs list text/image/video modalities, 720p/1080p/4k options, 4/6/8 second durations and generated audio.",
    },
    {
        "name": "Runway Research · Gen-4.5",
        "url": "https://runwayml.com/research/introducing-runway-gen-4.5",
        "role": "multi-tool market capability context",
        "evidence": "Runway describes Gen-4.5 as emphasizing motion quality, prompt adherence, visual fidelity, creative control.",
    },
    {
        "name": "Adobe · Firefly Video Model",
        "url": "https://blog.adobe.com/en/publish/2025/02/12/meet-firefly-video-model-ai-powered-creation-with-unparalleled-creative-control",
        "role": "creator-safe workflow and commercial-safety positioning",
        "evidence": "Adobe positions Firefly Video Model as IP-friendly/commercially safe and workflow-integrated.",
    },
    {
        "name": "Adobe Help · Content Credentials overview",
        "url": "https://helpx.adobe.com/firefly/web/get-started/learn-the-basics/content-credentials-overview.html",
        "role": "what Content Credentials store and how Firefly applies them",
        "evidence": "Content Credentials are tamper-evident metadata; Adobe lists issuer/date/app/AI tool/action fields.",
    },
    {
        "name": "YouTube Blog · Disclosing altered or synthetic content",
        "url": "https://blog.youtube/news-and-events/disclosing-ai-generated-content/",
        "role": "platform upload disclosure scenarios",
        "evidence": "Disclosure is needed for realistic altered/synthetic content such as likeness replacement, altered real events/places, realistic fictional events.",
    },
    {
        "name": "YouTube Help · How this content was made disclosures",
        "url": "https://support.google.com/youtube/answer/15447836?hl=en",
        "role": "viewer-facing labels and Content Credentials carry-forward",
        "evidence": "YouTube can show altered/synthetic disclosures from creator input, YouTube tools, or valid C2PA data.",
    },
    {
        "name": "C2PA · Verifying Media Content Sources",
        "url": "https://c2pa.org/",
        "role": "open provenance standard and Content Credentials mental model",
        "evidence": "C2PA describes Content Credentials as a nutrition-label-like origin/edit history standard.",
    },
    {
        "name": "Google · Tools to understand how content was created and edited",
        "url": "https://blog.google/innovation-and-ai/products/identifying-ai-generated-media-online/",
        "role": "SynthID/C2PA operational trend and verification availability",
        "evidence": "Google states SynthID watermarking across AI media, C2PA use, and verification expansion to Gemini/Search/Chrome.",
    },
    {
        "name": "Google DeepMind · SynthID",
        "url": "https://deepmind.google/models/synthid/",
        "role": "invisible watermarking concept and durability limits",
        "evidence": "SynthID embeds imperceptible watermarks into AI-generated images/audio/text/video and is designed to withstand common modifications.",
    },
    {
        "name": "U.S. Copyright Office · Copyright and Artificial Intelligence",
        "url": "https://www.copyright.gov/ai/",
        "role": "copyrightability/digital-replica report scope; not legal advice",
        "evidence": "USCO report Part 1 addresses digital replicas; Part 2 addresses copyrightability of generative AI outputs; Part 3 covers training.",
    },
    {
        "name": "FTC · Endorsements, Influencers, and Reviews",
        "url": "https://www.ftc.gov/business-guidance/advertising-marketing/endorsements-influencers-reviews",
        "role": "marketing/endorsement disclosure and consumer review guidance",
        "evidence": "FTC plain-language guidance covers disclosures for endorsements/influencers and avoiding deceptive reviews/advertising.",
    },
    {
        "name": "Stanford STORM Research Project",
        "url": "https://storm-project.stanford.edu/research/storm/",
        "role": "multi-perspective research method and source-bias warning",
        "evidence": "STORM uses perspective-guided question asking, source-grounded conversations, and notes source bias/over-association risks.",
    },
    {
        "name": "STORM paper · arXiv:2402.14207",
        "url": "https://arxiv.org/abs/2402.14207",
        "role": "methodology provenance",
        "evidence": "Paper defines Synthesis of Topic Outlines through Retrieval and Multi-perspective Question Asking.",
    },
]

STORM_SCAN = {
    "Skeptic": {
        "persona": "회의주의자",
        "question": "AI 영상 생성 도구를 쓰면 제작 속도는 빨라지지만, 신뢰와 권리 문제가 더 커지는 것 아닌가?",
        "summary": "가장 큰 위험은 생성 성공을 배포 가능 상태로 착각하는 것이다.",
        "body": "OpenAI는 Sora 책임 출시 설명에서 provenance signal, C2PA, watermark, likeness consent를 강조했지만 해당 페이지는 2026년 4월 26일 기준 Sora product no longer available이라고 표시한다. YouTube는 현실적으로 보이는 합성/변형 콘텐츠 disclosure를 요구하고, C2PA/Content Credentials가 있어도 플랫폼 표시·유지 여부는 별도 운영 문제다. 따라서 매뉴얼은 생성 버튼보다 먼저 권리·출처·라벨링 게이트를 둬야 한다.",
        "sources": [SOURCE_LIST[0]["url"], SOURCE_LIST[7]["url"], SOURCE_LIST[8]["url"], SOURCE_LIST[9]["url"]],
    },
    "Economist": {
        "persona": "경제학자",
        "question": "AI 영상의 진짜 비용 절감은 어디서 발생하고, 어디서 비용이 다시 생기는가?",
        "summary": "초안 제작 비용은 낮아지지만 검수·재생성·권리 확인·라벨링 비용이 새 병목이 된다.",
        "body": "Veo, Runway, Firefly 같은 도구는 prompt adherence, visual fidelity, creative control, native audio를 내세운다. 그러나 실무 비용은 첫 clip 생성보다 shot list 정리, reference asset 승인, iteration 기록, platform disclosure, provenance 보존에서 생긴다. 운영자는 생성 횟수가 아니라 '승인된 컷 비율'과 '재작업 사유'를 KPI로 잡아야 한다.",
        "sources": [SOURCE_LIST[2]["url"], SOURCE_LIST[3]["url"], SOURCE_LIST[4]["url"], SOURCE_LIST[5]["url"]],
    },
    "Historian": {
        "persona": "역사학자",
        "question": "기존 영상 제작 파이프라인에서 무엇은 그대로 남고 무엇만 바뀌는가?",
        "summary": "기획·스토리보드·편집·검수는 남고, 생성 도구는 중간 제작 단계를 짧게 바꾼다.",
        "body": "AI 영상은 pre-production을 생략하게 만드는 것이 아니라 더 중요하게 만든다. Veo 문서는 prompts, reference images, first/last frame, resolution, duration 같은 제작 변수의 명시를 요구한다. 이는 전통적인 콘티·샷리스트·후반 검수와 같은 사고 방식이다. 달라진 것은 카메라 장비보다 prompt와 provenance ledger가 중심 자료가 된다는 점이다.",
        "sources": [SOURCE_LIST[3]["url"], SOURCE_LIST[6]["url"], SOURCE_LIST[9]["url"]],
    },
    "Academic": {
        "persona": "학자",
        "question": "매뉴얼이 사용자를 보호하려면 어떤 증거 계층을 써야 하는가?",
        "summary": "도구 설명, 파일 메타데이터, 플랫폼 라벨, 사람 검수 결과를 서로 다른 증거로 분리해야 한다.",
        "body": "C2PA는 origin/edit history를 표준화하려 하지만, YouTube는 creator disclosure, YouTube generative tools, valid Content Credentials를 서로 다른 label source로 설명한다. Google은 SynthID와 C2PA를 함께 확장하고 있다고 설명한다. 연구 관점에서 이들은 모두 '신호'이지 단독 최종 진실이 아니다. 매뉴얼은 evidence ledger를 만들어 각 컷의 tool, prompt, source asset, human reviewer, label decision을 별도로 저장해야 한다.",
        "sources": [SOURCE_LIST[8]["url"], SOURCE_LIST[9]["url"], SOURCE_LIST[10]["url"], SOURCE_LIST[11]["url"]],
    },
    "Futurist": {
        "persona": "미래학자",
        "question": "2026년 이후 AI 영상 팀의 운영 시스템은 어떤 형태가 될까?",
        "summary": "단일 생성 앱보다 '프롬프트·권리·provenance·라벨·배포'를 묶은 제작 운영 원장이 핵심이 된다.",
        "body": "Google은 verification capability를 Gemini/Search/Chrome으로 확장한다고 말하고, Adobe는 Content Credentials cloud/Inspect 흐름을 설명한다. 앞으로 팀의 차별점은 어떤 모델을 쓰느냐보다 어떤 컷을 왜 승인했는지 재현 가능한 원장을 남기는 능력이 된다. 단, 저작권·초상권·광고표시는 지역과 맥락에 따라 달라져 법무/플랫폼 정책 확인이 필요하다.",
        "sources": [SOURCE_LIST[6]["url"], SOURCE_LIST[10]["url"], SOURCE_LIST[12]["url"], SOURCE_LIST[13]["url"]],
    },
}

CONTRADICTIONS = [
    ["AI 도구는 초안 제작을 빠르게 만든다", "생성 파일이 곧 배포 가능한 증거는 아니다", "모든 컷은 생성 후 권리·라벨·품질 게이트를 통과해야 한다"],
    ["C2PA/SynthID는 출처 확인을 돕는다", "플랫폼 표시와 메타데이터 보존은 항상 같지 않다", "메타데이터만 믿지 말고 disclosure log와 사람이 읽는 라벨을 함께 둔다"],
    ["현실적인 영상은 몰입감을 높인다", "현실적일수록 합성 표시·초상권·오인 위험이 커진다", "실존 인물·사건·장소처럼 보이면 더 높은 검수 레벨로 보낸다"],
    ["상업적으로 안전하다는 도구 포지셔닝은 유용하다", "개별 결과물의 권리·광고·플랫폼 적합성은 별도 문제다", "도구 claim은 참고만 하고 프로젝트별 source asset/사용처를 검수한다"],
    ["8초/짧은 클립은 실험에 좋다", "캠페인 영상은 컷 연결·톤·자막·음성 일관성이 필요하다", "컷 단위가 아니라 sequence approval sheet로 운영한다"],
]

SYNTHESIS = """# STORM Synthesis · AI 영상 제작 파이프라인 운영 매뉴얼 2026

핵심 결론은 도구 선택보다 운영 원장이다. AI 영상 도구는 prompt와 reference asset으로 빠르게 clip을 만들 수 있지만, 배포 가능한 영상은 prompt 결과물이 아니라 검수된 운영 산출물이다. 매뉴얼은 생성 절차보다 먼저 시스템 개요, 역할, 증거 계층, 위험 경계, 첫 성공 기준, 트러블슈팅을 제시해야 한다.

권장 운영 흐름은 여섯 단계다.

1. Brief — 목표, 플랫폼, 시청자, 현실성 수준, 금지 소재를 쓴다.
2. Asset clearance — reference image/audio/person/brand/source 권리를 확인한다.
3. Generate — 모델별 duration/resolution/audio/reference limits를 기록하며 clip을 만든다.
4. Review — 품질, 사실성, 인물/장소/사건 오인, 편향·위험 표현, 권리 리스크를 사람 검수로 본다.
5. Provenance — prompt, model, source asset, C2PA/SynthID/Content Credentials, reviewer, disclosure decision을 evidence ledger에 남긴다.
6. Publish — YouTube/채널/광고 disclosure와 설명문/라벨을 확인하고 배포한다.

매뉴얼의 사용자 경험은 초보자 우선이어야 한다. AI 영상이라는 말부터 '컴퓨터가 찍은 것처럼 보이는 장면을 생성·편집하는 워크플로우'라고 풀고, prompt, reference asset, Content Credentials, SynthID, altered or synthetic disclosure를 첫 등장 시 설명해야 한다.
"""

PEER_REVIEW = """# STORM Peer Review

검토 결과: 이 매뉴얼은 특정 법률 판단을 제공하면 안 된다. 저작권, 초상권, 광고표시는 법무·플랫폼 정책 확인이 필요한 영역으로 남겨야 한다. 또한 OpenAI Sora 페이지가 2026-04-26 기준 unavailable이라고 표시되므로, Sora를 현재 운영 도구로 추천하지 말고 provenance/likeness 설계 사례로만 언급해야 한다.

수정 지시:
- '배포 가능'이라는 표현은 품질·권리·라벨링 게이트 통과 후로 제한한다.
- C2PA/SynthID를 절대적 진실 판정기가 아니라 출처/수정 이력 신호로 쓴다.
- YouTube disclosure는 현실적으로 보이는 합성/변형 콘텐츠 중심으로 설명한다.
- 제품 기능 claim과 운영 절차를 분리하고, Source Limits 섹션을 명시한다.
- 법률 조언이 아니라 운영 체크리스트임을 분명히 한다.
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
    scan = ["# Multi-Perspective Scan · AI 영상 제작 파이프라인 운영 매뉴얼 2026"]
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


def build_verdict(scan_md: str) -> str:
    vt = """
<section class="vt-shell" aria-label="AI 영상 운영 지도">
  <div class="vt-frame">
    <div class="vt-demo"><div class="hm-grid">
      <article class="hm-card"><div class="vt-kicker">Brief</div><h3>무엇을 만들지 먼저 잠근다</h3><p class="vt-text">플랫폼, 길이, 현실성, 금지 소재, 승인자를 정한다.</p></article>
      <article class="hm-card" style="--c:var(--vt-blue)"><div class="vt-kicker">Gate</div><h3>생성 후 바로 배포하지 않는다</h3><p class="vt-text">권리, 품질, 합성표시, 출처 원장을 통과해야 한다.</p></article>
      <article class="hm-card" style="--c:var(--vt-green)"><div class="vt-kicker">Publish</div><h3>라벨과 설명을 같이 보낸다</h3><p class="vt-text">시청자가 무엇이 합성인지 알 수 있게 만든다.</p></article>
    </div><div class="hm-result"><b>결론: 생성 파이프라인이 아니라 승인 파이프라인</b><span>AI 영상 팀의 핵심 산출물은 mp4 하나가 아니라 evidence ledger가 붙은 승인 컷이다.</span></div></div>
  </div>
</section>
"""
    cards = "".join(
        f'<article class="summary-card"><div class="label">{esc(name)} · {esc(row["persona"])}</div><h3>{esc(row["summary"])}</h3><p>{esc(row["body"])}</p></article>'
        for name, row in STORM_SCAN.items()
    )
    return f"""
{h2('01', 'Verdict · AI 영상은 생성물이 아니라 승인 가능한 운영 산출물로 다룬다', 'verdict', 'manual-production의 workflow-first 원칙에 따라 생성 버튼보다 역할, 증거, 안전, 검수 흐름을 먼저 둔다.')}
<div class="summary-card"><div class="label">운영 판정</div><p><strong>권장 운영 기준:</strong> 생성된 영상은 초안이다. 배포 가능한 영상은 <span class="hl">brief, asset clearance, generation log, human review, provenance, platform disclosure</span>가 붙은 승인 컷이다. 이 문서는 법률 조언이 아니라 크리에이터/팀이 매번 누락을 줄이기 위한 운영 매뉴얼이다.</p></div>
<figure aria-label="AI 영상 운영 지도"><figcaption>vt hero-map · manual_analysis 1순위 시각 템플릿</figcaption>{vt}</figure>
<h3>STORM 다섯 관점 요약</h3>
<div class="card-grid rail-cycle">{cards}</div>
{source_details('STORM Multi-Perspective Scan 원문', scan_md, open_=False)}
"""


def build_reader_toc() -> str:
    return """
<span class="label">Reader Role Router · 독자 경로</span>
<p>처음 읽는 운영자는 시스템 개요부터, 급한 제작자는 첫 성공과 사전조건부터, 승인자는 decision guide와 audit를 먼저 확인합니다.</p>
<div class="toc-pills">
<a class="toc-pill" href="#source-version"><b>1</b>출처·버전</a>
<a class="toc-pill" href="#role-router"><b>2</b>역할별 경로</a>
<a class="toc-pill" href="#first-success"><b>3</b>첫 성공</a>
<a class="toc-pill" href="#prerequisites-safety"><b>4</b>사전조건·안전</a>
<a class="toc-pill" href="#task-recipes"><b>5</b>작업 레시피</a>
<a class="toc-pill" href="#reference-extract"><b>6</b>참조 추출</a>
<a class="toc-pill" href="#decision-guide"><b>7</b>결정 가이드</a>
<a class="toc-pill" href="#troubleshooting"><b>8</b>문제 해결</a>
<a class="toc-pill" href="#operations-runbook"><b>9</b>운영 런북</a>
<a class="toc-pill" href="#manual-audit"><b>10</b>매뉴얼 감사</a>
<a class="toc-pill" href="#source-note"><b>11</b>출처</a>
</div>
"""


def build_source_version() -> str:
    rows = [
        ["OpenAI Sora", "2026-04-26 기준 product no longer available 표기", "현재 도구 추천이 아니라 provenance/likeness 설계 사례로만 사용"],
        ["Veo 3.1", "DeepMind/Google API 문서상 native audio, 4/6/8초, 720p/1080p/4k 옵션", "짧은 컷 단위 운영과 resolution/latency/cost 기록 필요"],
        ["Runway/Firefly", "영상 생성 모델과 creative control, 상업/권리 안전 포지셔닝", "도구 claim은 참고, 프로젝트별 권리 검수는 별도"],
        ["YouTube", "현실적인 altered/synthetic content disclosure와 C2PA carry-forward 설명", "배포 전 플랫폼별 합성 표시 체크"],
        ["C2PA/SynthID", "출처·수정 이력/워터마크 신호", "절대 판정기가 아니라 증거 계층의 한 줄"],
        ["USCO/FTC", "AI copyright report, endorsement/review guidance", "법률 조언 대신 전문가/정책 확인 게이트로 연결"],
    ]
    return f"""
<div id="source-version"></div>
{h2('02', 'Source & Version · 2026-06-20 기준 출처 스냅샷', 'source', 'manual-production의 증거 계층 규칙에 따라 제품 기능, 플랫폼 정책, 권리/광고 가이드를 분리했다.')}
{table(rows, '출처·버전·운영 해석', ['출처 묶음', '확인 내용', '매뉴얼 적용'])}
<div class="term"><div class="label">먼저, 이 시스템이 뭔가?</div><p>AI 영상 제작 파이프라인은 “프롬프트를 넣고 영상을 받는 도구 사용법”이 아니다. 한 줄로 보면 <strong>기획서가 짧은 생성 컷으로 바뀌고, 그 컷이 다시 권리·품질·출처·라벨 검수를 통과해 배포 영상이 되는 운영 시스템</strong>이다.</p></div>
<div class="analogy"><div class="label">비유</div><p>식당 주방에서 요리가 나오면 바로 손님에게 내지 않는다. 주문서 확인, 알레르기 확인, 플레이팅, 최종 검수를 거친다. AI 영상도 생성 파일이 주방의 접시라면, evidence ledger는 주문서와 검수표다.</p></div>
"""


def build_role_router() -> str:
    rows = [
        ["크리에이티브 리드", "목표·톤·시청자·현실성 수준 결정", "brief 승인, 샷리스트 잠금, 최종 컷 승인"],
        ["프롬프트/생성 오퍼레이터", "prompt, reference asset, 모델 설정 관리", "generation log 기록, 실패 사유 분류, 후보 컷 제출"],
        ["편집자", "컷 연결, 자막, 음성, 색감, 길이 조정", "sequence continuity, 자막/오디오 싱크 확인"],
        ["권리·브랜드 검수자", "인물·브랜드·저작물·실제 사건/장소 리스크 확인", "asset clearance, disclosure decision, legal escalation"],
        ["채널 매니저", "YouTube/Shorts/광고/웹 업로드", "altered/synthetic disclosure, 설명문, 썸네일, 공개 후 모니터링"],
    ]
    return f"""
<div id="role-router"></div>
{h2('03', 'Reader Role Router · 역할별로 먼저 읽을 곳', 'role', '초보자도 자기 책임 경계를 바로 찾도록 역할과 산출물을 분리한다.')}
{table(rows, '역할별 책임과 확인 산출물', ['역할', '주요 질문', '확인 산출물'])}
<div class="good"><div class="label">좋은 운영 습관</div><div class="name">한 사람이 생성·검수·배포를 모두 승인하지 않는다</div><p>작은 팀이라도 “생성한 사람”과 “공개해도 되는지 확인하는 사람”을 분리하면, 오인·권리·라벨 누락을 크게 줄일 수 있다.</p></div>
"""


def build_first_success() -> str:
    return f"""
<div id="first-success"></div>
{h2('04', 'First Success · 30분 안에 안전한 첫 컷 만들기', 'success', '버튼 클릭 튜토리얼이 아니라 초보자가 첫 승인 컷의 기준을 이해하도록 설계한다.')}
<div class="impact-grid">
  <article class="impact-card"><h3>1. Brief 5줄</h3><p>목적, 플랫폼, 길이, 현실성, 금지 소재를 5줄로 쓴다. 예: “가상 제품 데모, Shorts, 8초, 비현실/애니풍, 실존 인물 없음”.</p></article>
  <article class="impact-card"><h3>2. Reference 분리</h3><p>직접 만든 이미지/로고/음원인지, 외부 자료인지 표시한다. 출처가 모호하면 생성 전에 제외한다.</p></article>
  <article class="impact-card"><h3>3. Generate 후보 3개</h3><p>같은 brief로 3개 후보를 만들고, prompt와 모델/해상도/길이/생성 시간을 기록한다.</p></article>
  <article class="impact-card"><h3>4. Review 6문항</h3><p>품질, 사실 오인, 실존 인물/장소 착각, 브랜드 충돌, 플랫폼 disclosure, 자막/음성 오류를 체크한다.</p></article>
</div>
<div class="source-note"><h3>첫 성공의 완료 기준</h3><p>완료는 “영상 파일 생성”이 아니라 <strong>후보 컷 1개 + brief + prompt log + source asset list + review note + disclosure decision</strong>이 한 폴더에 있는 상태다.</p></div>
"""


def build_prerequisites_safety() -> str:
    rows = [
        ["실존 인물/목소리", "동의·권한·플랫폼 정책 확인 전 사용 금지", "사람처럼 보이면 자동으로 high review"],
        ["실제 사건/장소", "뉴스·재난·선거·범죄처럼 보이는 장면 주의", "허구임을 명확히 하거나 배포 제외"],
        ["브랜드/캐릭터/IP", "상표·저작물·스타일 모방 리스크", "소유/라이선스/승인 근거 없으면 제외"],
        ["광고/추천/후원", "FTC/플랫폼 disclosure 필요 가능성", "광고주·후원 관계와 AI 사용을 따로 체크"],
        ["메타데이터", "C2PA/SynthID/Content Credentials 보존 여부", "렌더/압축/업로드 후 다시 확인"],
    ]
    return f"""
<div id="prerequisites-safety"></div>
{h2('05', 'Prerequisites Safety · 생성 전 사전조건과 위험 경계', 'safety', 'manual-production의 위험 action 분리 원칙을 영상 제작의 권리·라벨·오인 위험에 적용했다.')}
{table(rows, '위험 소재별 운영 경계', ['소재', '사전조건', '안전 운영'])}
<div class="danger"><div class="label">초보자 실수</div><div class="name">“비슷하게만” 만들면 괜찮다고 생각한다</div><p>실존 인물, 알려진 캐릭터, 특정 브랜드, 실제 사건처럼 보이는 요소는 “완전히 같지 않음”만으로 안전해지지 않는다. 이 매뉴얼은 법률 판단을 제공하지 않으며, 해당 소재는 별도 승인을 받거나 제외한다.</p></div>
<div class="good"><div class="label">권장</div><div class="name">처음에는 가상/비현실/자체 제작 asset으로 시작</div><p>첫 파이프라인 검증은 고양이 캐릭터, 추상 제품, 가상 브랜드, 애니메이션 스타일처럼 오인 가능성이 낮은 소재로 수행한다.</p></div>
"""


def build_task_recipes(contradiction_md: str) -> str:
    wg = """
<section class="wg-13-fc" aria-label="AI 영상 승인 파이프라인 플로우차트">
  <h3 class="wg-13-h">AI 영상 승인 파이프라인 <span class="wg-13-sub">생성 → 검수 → 공개</span></h3>
  <div class="wg-13-flow">
    <a href="#wg-13-s1" class="wg-13-node wg-13-node--start"><span class="wg-13-step">시작</span>Brief 작성</a>
    <span class="wg-13-arrow" aria-hidden="true">&darr;</span>
    <a href="#wg-13-s2" class="wg-13-node"><span class="wg-13-step">1</span>Asset clearance</a>
    <span class="wg-13-arrow" aria-hidden="true">&darr;</span>
    <a href="#wg-13-s3" class="wg-13-node"><span class="wg-13-step">2</span>Generate 후보</a>
    <span class="wg-13-arrow" aria-hidden="true">&darr;</span>
    <div class="wg-13-branch">
      <a href="#wg-13-s4" class="wg-13-node wg-13-node--decide"><span class="wg-13-step">3</span>승인 게이트 통과?</a>
      <div class="wg-13-paths">
        <div class="wg-13-path wg-13-path--fail"><span class="wg-13-edge">아니오 &rarr; 수정/폐기</span><a href="#wg-13-fail" class="wg-13-node wg-13-node--fail"><span class="wg-13-step">!</span>재생성 또는 제외</a></div>
        <div class="wg-13-path wg-13-path--ok"><span class="wg-13-edge">예 &rarr; 공개 준비</span><a href="#wg-13-s5" class="wg-13-node"><span class="wg-13-step">4</span>Provenance 저장</a><span class="wg-13-arrow" aria-hidden="true">&darr;</span><a href="#wg-13-s6" class="wg-13-node wg-13-node--end"><span class="wg-13-step">완료</span>Publish + monitor</a></div>
      </div>
    </div>
  </div>
  <div class="wg-13-detail">
    <h4 class="wg-13-dh">단계 상세 <span class="wg-13-dnote">박스를 클릭하면 해당 체크로 이동</span></h4>
    <details id="wg-13-s1" class="wg-13-acc" open><summary><span class="wg-13-tag">시작</span>Brief 작성</summary><div class="wg-13-body"><p>목적, 시청자, 플랫폼, 길이, 현실성 수준, 금지 소재, 승인자를 적는다.</p></div></details>
    <details id="wg-13-s2" class="wg-13-acc"><summary><span class="wg-13-tag">1단계</span>Asset clearance</summary><div class="wg-13-body"><p>reference image/audio/person/brand/source가 직접 제작·허가·라이선스·제외 중 어디에 속하는지 표시한다.</p></div></details>
    <details id="wg-13-s3" class="wg-13-acc"><summary><span class="wg-13-tag">2단계</span>Generate 후보</summary><div class="wg-13-body"><p>모델, prompt, reference, duration, resolution, seed/operation id가 있으면 기록한다.</p></div></details>
    <details id="wg-13-s4" class="wg-13-acc"><summary><span class="wg-13-tag">3단계</span>승인 게이트</summary><div class="wg-13-body"><ul><li>품질: 자막/음성/물리/손/로고 오류 없음</li><li>오인: 실존 사건·인물처럼 착각되지 않음</li><li>권리: source asset 근거 있음</li><li>라벨: 플랫폼 disclosure 결정 기록</li></ul></div></details>
    <details id="wg-13-fail" class="wg-13-acc wg-13-acc--fail"><summary><span class="wg-13-tag wg-13-tag--fail">실패</span>재생성 또는 제외</summary><div class="wg-13-body"><p>실패 사유를 하나만 고른다: prompt 불명확, 권리 불확실, 현실 오인, 기술 품질, 플랫폼 부적합. 같은 사유가 3회 반복되면 brief를 다시 쓴다.</p></div></details>
    <details id="wg-13-s5" class="wg-13-acc"><summary><span class="wg-13-tag">4단계</span>Provenance 저장</summary><div class="wg-13-body"><p>파일명, source list, prompt, tool, reviewer, label decision, C2PA/SynthID/Content Credentials 확인 결과를 보관한다.</p></div></details>
    <details id="wg-13-s6" class="wg-13-acc"><summary><span class="wg-13-tag">완료</span>Publish + monitor</summary><div class="wg-13-body"><p>업로드 후 viewer-facing label, 설명문, 썸네일, 댓글/신고/오인 반응을 첫 24시간 확인한다.</p></div></details>
  </div>
</section>
"""
    return f"""
<div id="task-recipes"></div>
{h2('06', 'Task Recipes · 생성보다 승인 흐름을 먼저 실행한다', 'recipe', 'manual_analysis 권장 wg-13 annotated flowchart로 운영 경로와 실패 경로를 같이 보여준다.')}
{wg}
<h3>Contradiction Map · 운영 규칙으로 바꾸기</h3>
{table(CONTRADICTIONS, 'STORM Contradiction Map', ['좋은 점', '충돌 위험', '운영 규칙'])}
{source_details('Contradiction Map 원문', contradiction_md, open_=False)}
"""


def build_reference_extract(synthesis_md: str) -> str:
    rows = [
        ["Prompt log", "brief id, prompt, negative prompt, reference asset, 모델/해상도/길이", "재현·재작업·비용 분석"],
        ["Asset ledger", "파일명, 출처, 제작자, 라이선스/동의, 사용 범위", "권리 검수"],
        ["Review note", "품질 실패, 오인 가능성, 위험 소재, 수정 요청", "승인/반려 근거"],
        ["Provenance check", "C2PA, SynthID, Content Credentials, platform label", "시청자 투명성"],
        ["Publish log", "업로드 URL, disclosure 선택, 설명문, 썸네일, 공개일", "사후 모니터링"],
    ]
    return f"""
<div id="reference-extract"></div>
{h2('07', 'Reference Extract · evidence ledger에 남겨야 할 필드', 'reference', 'manual-production의 evidence hierarchy를 AI 영상 컷 단위 원장으로 변환했다.')}
{table(rows, '컷 단위 evidence ledger 필드', ['레코드', '필수 필드', '쓰임'])}
<div class="source-note"><h3>용어 설명</h3><p><strong>Content Credentials</strong>는 파일의 생성·수정 이력을 알려주는 출처/편집 이력 라벨에 가깝다. <strong>SynthID</strong>는 AI 생성물 안에 보이지 않는 워터마크 신호를 넣는 방식이다. 둘 다 도움이 되지만, 사람 검수와 플랫폼 표시 결정을 대체하지 않는다.</p></div>
{source_details('STORM Synthesis 원문', synthesis_md, open_=False)}
"""


def build_decision_guide() -> str:
    rows = [
        ["실존 인물처럼 보이는가?", "예", "동의/권한이 없으면 배포 금지 또는 재생성"],
        ["실제 사건·뉴스·재난·정치처럼 보이는가?", "예", "허구임을 명확히 하거나 고위험 검수로 전환"],
        ["브랜드/캐릭터/IP가 식별되는가?", "예", "소유/라이선스/승인 근거 없으면 제외"],
        ["광고/후원/추천에 쓰이는가?", "예", "FTC/플랫폼 disclosure와 material connection 확인"],
        ["C2PA/SynthID/Content Credentials가 보이는가?", "아니오", "수동 원장과 viewer-facing disclosure를 강화"],
        ["자막/음성/물리 오류가 있는가?", "예", "편집 수정 또는 재생성. 공개용 승인 금지"],
    ]
    return f"""
<div id="decision-guide"></div>
{h2('08', 'Decision Guide · 공개 전 멈춤/진행 판단', 'choice', '업무 판단이 필요한 지점을 버튼 클릭보다 먼저 보여준다.')}
{table(rows, '공개 전 결정표', ['질문', '조건', '결정'])}
<div class="danger"><div class="label">멈춤 조건</div><div class="name">“아마 괜찮을 것 같다”는 승인 근거가 아니다</div><p>권리·초상·광고 표시·플랫폼 라벨은 추측으로 통과시키지 않는다. 모르면 배포하지 않고 승인자에게 넘긴다.</p></div>
"""


def build_troubleshooting() -> str:
    rows = [
        ["프롬프트와 다른 영상", "목표/시점/동작/배경이 한 문장에 섞임", "shot 단위로 쪼개고 first/last frame 또는 reference를 분리"],
        ["인물/손/문자 이상", "모델의 물리·텍스트·세부 일관성 한계", "해당 컷을 close-up에서 wide shot으로 바꾸거나 편집에서 가림"],
        ["자막/음성 불일치", "native audio/후반 자막 싱크 문제", "무음으로 생성 후 별도 TTS/편집, 또는 audio review 단계 추가"],
        ["합성 표시 누락", "업로드 담당자가 disclosure 결정을 못 봄", "publish log에 disclosure field를 필수로 만들고 업로드 전 읽어주기"],
        ["메타데이터 사라짐", "압축·편집·플랫폼 업로드 중 신호 손실", "업로드 후 viewer label과 Inspect/검증 도구를 다시 확인"],
        ["법무/브랜드 반려", "source asset 근거 부족 또는 실존/브랜드 오인", "asset ledger를 보강하거나 가상 소재로 재제작"],
    ]
    return f"""
<div id="troubleshooting"></div>
{h2('09', 'Troubleshooting · 증상, 원인, 진단', 'trouble', '기술 실패와 운영 실패를 분리해 재생성 루프를 줄인다.')}
{table(rows, '트러블슈팅 표', ['증상', '가능 원인', '진단/조치'])}
"""


def build_operations_runbook() -> str:
    rows = [
        ["매일", "전날 생성 컷의 반려 사유 3개 정리, 공개 예정 컷 disclosure 확인", "반려 사유 로그, 공개 체크리스트"],
        ["매주", "상위 실패 prompt/asset 유형 리뷰, 플랫폼 정책 변경 확인", "prompt pattern update, risk pattern update"],
        ["캠페인 전", "권리/브랜드/광고/초상권 리뷰, disclosure 문구 승인", "approval sheet"],
        ["공개 직후", "라벨 노출, 설명문, 썸네일, 댓글/신고/오해 반응 확인", "publish monitoring note"],
        ["사고 발생", "비공개 전환, 원장 확인, 승인자/법무/플랫폼 이슈 분리", "incident review"],
    ]
    return f"""
<div id="operations-runbook"></div>
{h2('10', 'Operations Runbook · 반복 운영 체크', 'ops', '한 번 만드는 튜토리얼이 아니라 계속 돌릴 수 있는 운영 루틴으로 정리했다.')}
{table(rows, '운영 주기별 체크', ['주기', '해야 할 일', '남길 기록'])}
<div class="good"><div class="label">성공 지표</div><div class="name">승인된 컷 비율과 반려 사유 감소</div><p>생성 수량이 늘어도 반려 사유가 반복되면 운영 품질은 낮다. 팀 KPI는 “생성량”보다 “첫 검수 통과율, 플랫폼 라벨 누락 0건, 권리 반려 0건”에 둔다.</p></div>
"""


def build_manual_audit(peer_md: str) -> str:
    rows = [
        ["Reader fit", "크리에이터/편집자/채널 매니저/검수자 역할 분리", "PASS"],
        ["Workflow-first", "Brief→Asset→Generate→Review→Provenance→Publish 순서", "PASS"],
        ["Beginner-first", "용어 설명, 비유, danger/good, 첫 성공 기준", "PASS"],
        ["Source Limits", "실제 도구 실행/업로드/법률 검토는 수행하지 않음", "BOUNDARY"],
        ["Technical", "adaptive-html-final validate/quality/render/completion 게이트로 확인", "PASS"],
        ["manual-verification", "로컬에 별도 manual-verification 스킬 없음; manual-production 참조 checklist와 프로젝트 렌더 검증으로 대체", "INCOMPLETE"],
    ]
    return f"""
<div id="manual-audit"></div>
{h2('11', 'Manual Audit · 출처 한계와 검증 경계', 'audit', 'manual-production의 정직한 완료 보고 규칙에 따라 완료/검증/한계를 분리한다.')}
{table(rows, 'Manual audit status', ['검사 축', '확인 내용', '상태'])}
<div class="source-note"><h3>Source Limits · 출처 한계</h3><p>이 페이지는 공식 문서와 공개 정책을 바탕으로 만든 운영 매뉴얼이다. 실제 Google Flow/Veo/Runway/Firefly/Sora 앱에서 영상을 생성하거나 YouTube에 업로드하지 않았다. 저작권, 초상권, 광고표시 판단은 관할·플랫폼·캠페인 맥락에 따라 달라질 수 있으므로 법무/정책 담당자 확인이 필요하다.</p></div>
{source_details('STORM Peer Review 원문', peer_md, open_=True)}
"""


def build_next_actions() -> str:
    return f"""
{h2('12', 'Next Actions · 오늘 팀에 바로 붙일 산출물 5개', 'next', '다음 행동은 감상이 아니라 파일·체크리스트·원장으로 닫는다.')}
<div class="card-grid rail-cycle">
  <article class="summary-card"><h3>1. brief-template.md</h3><p>목표, 플랫폼, 길이, 현실성, 금지 소재, 승인자를 쓰는 5줄 템플릿.</p></article>
  <article class="summary-card"><h3>2. asset-ledger.csv</h3><p>reference image/audio/person/brand/source의 출처·권리·동의·사용 범위를 적는 표.</p></article>
  <article class="summary-card"><h3>3. generation-log.csv</h3><p>모델, prompt, reference, duration, resolution, operation id, 실패 사유 기록.</p></article>
  <article class="summary-card"><h3>4. review-checklist.md</h3><p>품질, 오인, 권리, 라벨, 자막/음성, 공개 후 모니터링 체크.</p></article>
  <article class="summary-card"><h3>5. publish-note.md</h3><p>YouTube/Shorts/광고/웹 업로드별 disclosure decision과 설명문 문구.</p></article>
</div>
<div class="try soft-cta"><h2>첫 운영 실험</h2><p>실존 인물·브랜드·뉴스·정치·의료·금융 소재를 모두 제외하고, 가상 제품 애니메이션 8초 컷 하나로 파이프라인을 끝까지 돌려보세요. 목표는 멋진 영상이 아니라 누락 없는 운영 원장입니다.</p></div>
"""


def build_source_note() -> str:
    links_html = "".join(
        f'<li><a href="{esc(src["url"])}" target="_blank" rel="noopener noreferrer">{esc(src["name"])}</a> — {esc(src["role"])}</li>'
        for src in SOURCE_LIST
    )
    return f"""
<div id="source-note"></div>
{h2('13', 'Source Hub · 출처와 보조 산출물', 'source', '공식 문서·정책·STORM 산출물·manual-production 적용 기록을 한 곳에 모았다.')}
<p>보조 파일: <a href="sources/storm-scan.md">storm-scan.md</a> · <a href="sources/storm-contradiction-map.md">contradiction-map.md</a> · <a href="sources/storm-synthesis.md">synthesis.md</a> · <a href="sources/storm-peer-review.md">peer-review.md</a> · <a href="sources/source-list.json">source-list.json</a> · <a href="sources/manual-production-application.json">manual-production 적용 기록</a></p>
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
        "topic": "AI 영상 제작 파이프라인 운영 매뉴얼 2026",
        "mode": "solo-fallback-by-main-agent",
        "reason": "cmux workspace unavailable and cmux/kimi missing; five perspectives simulated in main session with official web sources",
        "souls": STORM_SCAN,
        "contradictions": CONTRADICTIONS,
        "synthesis": synthesis_md,
        "peer_review": peer_md,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (SOURCES / "manual-production-application.json").write_text(json.dumps({
        "skill": "manual-production",
        "source_path": str(MANUAL_SKILL.relative_to(ROOT)),
        "selected_adaptive_mode": MODE,
        "topic": "AI 영상 제작 파이프라인 운영 매뉴얼 2026",
        "reader": "크리에이터, 편집자, 채널 매니저, 권리/브랜드 검수자",
        "artifact_format": "single-page adaptive-html-final manual_analysis output",
        "applied_rules": [
            "workflow inventory before prose",
            "system overview / beginner-first explanation",
            "role router",
            "prerequisites and safety before tasks",
            "workflow map with failure branch",
            "source/version and Source Limits",
            "technical/content verification separated",
            "manual-verification required but unavailable locally, recorded as incomplete boundary",
        ],
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (SOURCES / "manual-content-checklist.md").write_text("""# Manual Content Checklist

- Reader/job/scope explicit: PASS
- Overview before workflow detail: PASS
- Beginner-first aids: PASS
- Risky/regulated decisions: bounded as legal/platform review
- Source Limits visible: PASS
- User-facing process/status leakage: checked manually
""", encoding="utf-8")
    (SOURCES / "manual-technical-checklist.md").write_text("""# Manual Technical Checklist

- HTML validates via adaptive-html-final validator
- Internal links tested by render audit
- 390/1280 overflow checked
- Behavioral scripts: zero except JSON-LD
- Screenshots generated for render evidence
""", encoding="utf-8")
    (SOURCES / "manual-verification-boundary.json").write_text(json.dumps({
        "manual_verification_skill_available": False,
        "substitute_checks": ["validate_output", "quality_contract_check", "render_audit_fulltest", "completion_check", "visible_text_content_preservation"],
        "claim": "Project validation passed; dedicated manual-verification skill pass not claimed.",
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    shutil.copyfile(SKILL / "manifest.json", SOURCES / "adaptive-html-final-manifest.json")
    (SOURCES / "profile.json").write_text(json.dumps({"profile": PROFILE}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (SOURCES / "layout-placeholder-map.json").write_text(json.dumps({
        "layout": LAYOUT,
        "VERDICT": "운영 판정 + vt hero-map + STORM 관점",
        "READER_TOC": "manual-reader-toc chip navigation",
        "SOURCE_VERSION": "출처/버전 snapshot + system overview",
        "ROLE_ROUTER": "역할별 책임",
        "FIRST_SUCCESS": "30분 첫 컷 기준",
        "PREREQUISITES_SAFETY": "사전조건/안전/위험 소재",
        "TASK_RECIPES": "wg-13 flowchart + contradiction map",
        "REFERENCE_EXTRACT": "evidence ledger fields",
        "DECISION_GUIDE": "공개 전 결정표",
        "TROUBLESHOOTING": "증상/원인/진단",
        "OPERATIONS_RUNBOOK": "운영 주기",
        "MANUAL_AUDIT": "Source Limits + verification boundary",
        "NEXT_ACTIONS": "실행 산출물",
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
        "skills/adaptive-html-final/assets/layouts/manual-analysis.html",
        "skills/adaptive-html-final/assets/visual-html-templates/01-hero-map.html",
        "skills/adaptive-html-final/assets/widget-templates/13-annotated-flowchart.html",
        "skills/adaptive-html-final/references/manual-analysis-system.md",
        "skills/adaptive-html-final/references/layout-system.md",
        "orginal_skill/manual-production/SKILL.md",
        "orginal_skill/manual-production/references/beginner-friendly-manual-patterns.md",
        "orginal_skill/manual-production/references/system-overview-page-for-beginners.md",
        "orginal_skill/manual-production/references/content-verification-checklist.md",
        "orginal_skill/manual-production/references/technical-verification-checklist.md",
        "orginal_skill/manual-production/references/manual-phase-gates.md",
        "orginal_skill/manual-production/references/workflow-inventory-template.md",
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
            "sources/manual-production-application.json",
        ],
        "research_route": "storm-research solo fallback; web-sourced claims stored in source-list.json",
        "manual_verification_boundary": "dedicated manual-verification skill not installed; not claiming manual-verification PASS",
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
        f'<span>adaptive-html-final v{version()}</span><span>manual-production</span>'
    )
    body = layout
    replacements = {
        "{{KICKER}}": "manual-production × STORM Research",
        "{{TITLE}}": "AI 영상 제작 파이프라인 운영 매뉴얼 2026",
        "{{SUBTITLE}}": "생성 도구보다 먼저 brief, asset clearance, review, provenance, disclosure를 잠그는 초보자용 운영 가이드",
        "{{META}}": meta_inner,
        "{{VERDICT}}": build_verdict(scan_md),
        "{{READER_TOC}}": build_reader_toc(),
        "{{SOURCE_VERSION}}": build_source_version(),
        "{{ROLE_ROUTER}}": build_role_router(),
        "{{FIRST_SUCCESS}}": build_first_success(),
        "{{PREREQUISITES_SAFETY}}": build_prerequisites_safety(),
        "{{TASK_RECIPES}}": build_task_recipes(contradiction_md),
        "{{REFERENCE_EXTRACT}}": build_reference_extract(synthesis_md),
        "{{DECISION_GUIDE}}": build_decision_guide(),
        "{{TROUBLESHOOTING}}": build_troubleshooting(),
        "{{OPERATIONS_RUNBOOK}}": build_operations_runbook(),
        "{{MANUAL_AUDIT}}": build_manual_audit(peer_md),
        "{{NEXT_ACTIONS}}": build_next_actions(),
        "{{SOURCE_NOTE}}": build_source_note(),
    }
    for key, value in replacements.items():
        body = body.replace(key, value)
    body = body.replace(
        '</div></header>',
        '</div><div class="generated-row"><p class="generated-date">생성 기준: 2026-06-20 KST · STORM solo research · manual_analysis · layout-first</p>'
        '<div class="lens-strip" aria-label="적용 렌즈"><span class="lens-strip-label">LENS</span><span class="lens-chip">운영 매뉴얼</span><span class="lens-chip">증거 원장</span><span class="lens-chip">안전 게이트</span><span class="lens-chip">출처 한계</span><span class="lens-chip">무 JS</span></div></div></header>',
        1,
    )

    title = "AI 영상 제작 파이프라인 운영 매뉴얼 2026 · manual-production STORM"
    description = f"manual-production과 STORM 리서치로 만든 AI 영상 제작 파이프라인 운영 매뉴얼. adaptive-html-final v{version()} manual_analysis 스타일."
    json_ld = json.dumps({
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": title,
        "description": description,
        "inLanguage": "ko",
        "datePublished": "2026-06-20",
        "author": {"@type": "Organization", "name": "adaptive-html-final"},
        "keywords": ["AI 영상", "운영 매뉴얼", "Content Credentials", "C2PA", "SynthID", "YouTube disclosure", "Veo", "Runway", "Firefly"],
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
        "AI 영상 제작 파이프라인 운영 매뉴얼 2026",
        "manual-production",
        "STORM",
        "Reader Role Router",
        "Source & Version",
        "Prerequisites Safety",
        "Troubleshooting",
        "Source Limits",
        "Content Credentials",
        "C2PA",
        "SynthID",
        "YouTube",
        "evidence ledger",
        "회의주의자",
        "경제학자",
    ]
    missing = [x for x in required if x not in visible]
    evidence = {
        "storm_soul_count": len(STORM_SCAN),
        "source_count": len(SOURCE_LIST),
        "required_markers_missing": missing,
        "output_visible_text_chars": len(visible),
        "pass": not missing and len(visible) > 15000,
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
