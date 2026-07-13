#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import html
import json
import re
import shutil
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "adaptive-html-final"
ASSETS = SKILL / "assets"
STORM = ROOT / "orginal_skill" / "storm-research"
OUT = ROOT / "output" / "2026-06-19" / "storm-research-hybrid-storm-method"
SOURCES = OUT / "sources"

CORE_ORDER = ["theme.css", "components.css", "visual-components.css", "layouts.css", "print.css"]
INLINE_ORDER = [
    "theme.css",
    "components.css",
    "visual-components.css",
    "widgets.css",
    "visual-html.css",
    "body-icons.css",
    "editorial-patterns.css",
    "layouts.css",
    "print.css",
    "theme-dark.css",
]

TOPIC = "STORM식 다관점 리서치가 AI HTML 리포트 생성 파이프라인에 주는 실제 가치와 한계"
SLUG = "storm-research-hybrid-storm-method"

SOURCES_USED = [
    {
        "id": "storm-paper",
        "title": "Assisting in Writing Wikipedia-like Articles From Scratch with Large Language Models",
        "url": "https://arxiv.org/abs/2402.14207",
        "kind": "paper",
        "notes": "STORM 원논문. 다관점 질문·검색 grounding·FreshWiki 평가와 한계의 핵심 근거.",
    },
    {
        "id": "storm-project",
        "title": "Stanford STORM Research Project",
        "url": "https://storm-project.stanford.edu/research/storm/",
        "kind": "project",
        "notes": "NAACL 2024 프로젝트 페이지. pre-writing/writing 단계, +25% 조직성, +10% coverage, 오류 분석 근거.",
    },
    {
        "id": "storm-github",
        "title": "stanford-oval/storm GitHub repository",
        "url": "https://github.com/stanford-oval/storm",
        "kind": "code",
        "notes": "구현·패키지·Co-STORM 통합·모듈형 runner와 검색/모델 구성 근거.",
    },
    {
        "id": "costorm-paper",
        "title": "Into the Unknown Unknowns: Engaged Human Learning through Participation in Language Model Agent Conversations",
        "url": "https://arxiv.org/abs/2408.15232",
        "kind": "paper",
        "notes": "Co-STORM 원논문. unknown unknowns, multi-agent discourse, mind map, human preference 수치 근거.",
    },
    {
        "id": "costorm-acl",
        "title": "Co-STORM ACL Anthology page",
        "url": "https://aclanthology.org/2024.emnlp-main.554/",
        "kind": "paper-page",
        "notes": "EMNLP 2024 정식 메타데이터와 초록. 70%/78% 선호 수치 근거.",
    },
    {
        "id": "local-storm-skill",
        "title": "local orginal_skill/storm-research/SKILL.md",
        "url": "orginal_skill/storm-research/SKILL.md",
        "kind": "local-skill",
        "notes": "이번 하이브리드 실행 방식. full cmux 불가 시 solo fallback + 4프롬프트 파이프라인 규칙.",
    },
]

SCAN = {
    "topic": TOPIC,
    "mode": "solo-fallback",
    "reason": "CMUX_WORKSPACE_ID와 cmux CLI가 없어 storm-research full 분산 모드 대신 인라인 4프롬프트 파이프라인을 사용했다.",
    "souls": [
        {
            "name": "회의주의자",
            "persona": "가장 강한 반론·검증 실패 모드 탐색",
            "findings": [
                "STORM의 평가상 이득은 조직성·coverage 지표이지, 자동으로 출판 가능한 글을 보장한다는 뜻이 아니다. GitHub README도 출판 품질 문서에는 상당한 편집이 필요하다고 적고, 숙련된 Wikipedia 편집자에게는 pre-writing 단계에서 유용하다고 범위를 제한한다. [출처: https://github.com/stanford-oval/storm]",
                "원논문·프로젝트 페이지가 직접 지목한 실패 모드는 source bias transfer와 unrelated facts over-association이다. 즉 검색 grounding이 있어도 출처 편향과 부당한 연결은 남는다. [출처: https://storm-project.stanford.edu/research/storm/]",
                "따라서 하이브리드 HTML 산출물은 ‘리서치 엔진의 최종판’이 아니라 ‘출처·모순·검토를 보존한 의사결정 초안’으로 배치해야 한다. [추론]",
            ],
            "conclusion": "STORM은 결론 제조기가 아니라 질문·출처·모순을 끌어내는 pre-writing 엔진으로 써야 안전하다.",
            "uncertainty": "상용 deep-research 도구와의 비용/정확도 비교는 같은 벤치마크가 없으므로 이 문서에서는 단정하지 않는다.",
        },
        {
            "name": "경제학자",
            "persona": "비용·운영 레버·ROI 관점",
            "findings": [
                "STORM은 긴 글 생성을 pre-writing과 writing으로 분리한다. 이 분리는 리서치/개요 품질을 먼저 검수해 재작성 비용을 낮추는 운영 레버가 된다. [출처: https://storm-project.stanford.edu/research/storm/]",
                "공식 GitHub 예시는 conversation simulator에는 더 저렴하고 빠른 모델을, article generation에는 더 강한 모델을 쓰는 구성을 제안한다. 즉 비용 최적화의 핵심은 전 단계에 같은 고가 모델을 쓰지 않는 것이다. [출처: https://github.com/stanford-oval/storm]",
                "2024~2025 업데이트에서 `knowledge-storm` 패키지, VectorRM, 다양한 retriever/search integration, LiteLLM 통합이 언급된다. 이는 도입 비용이 ‘프롬프트 하나’가 아니라 검색·모델·문서 저장소 구성 비용을 포함한다는 뜻이다. [출처: https://github.com/stanford-oval/storm]",
            ],
            "conclusion": "경제적 가치는 초안 품질보다 ‘질문/개요 검수 루프를 앞당기는 것’에서 먼저 발생한다.",
            "uncertainty": "실제 조직 ROI는 주제 난도, 검색 API 비용, 편집자 검수 시간에 따라 달라져 별도 계측이 필요하다.",
        },
        {
            "name": "역사학자",
            "persona": "RAG·장문 생성의 반복 패턴 관점",
            "findings": [
                "STORM 프로젝트는 긴 인용 글 생성이 어렵고 평가도 어렵기 때문에 pre-writing과 writing의 두 단계로 나눈다고 설명한다. [출처: https://storm-project.stanford.edu/research/storm/]",
                "프로젝트 페이지는 직접 질문 생성을 지시하면 특히 long-tail 주제에서 피상적 질문으로 흐르기 쉽다고 설명하고, 이를 보완하기 위해 perspective-guided question asking과 simulated conversation을 쓴다. [출처: https://storm-project.stanford.edu/research/storm/]",
                "Co-STORM은 사용자가 모든 질문을 직접 떠올려야 하는 QA 방식의 한계를 ‘unknown unknowns’ 문제로 재정의하고, 여러 LM agent 담화를 관찰·조향하게 만든다. [출처: https://aclanthology.org/2024.emnlp-main.554/]",
            ],
            "conclusion": "역사적 패턴은 ‘답변 생성’보다 ‘좋은 질문을 먼저 만드는 구조’가 장문 품질의 병목이라는 쪽으로 이동한다.",
            "uncertainty": "STORM 계열이 모든 도메인에서 기존 편집 워크플로우를 대체한다는 근거는 없다.",
        },
        {
            "name": "학자",
            "persona": "논문·평가·검증 가능 주장 중심",
            "findings": [
                "STORM 원논문은 Wikipedia-like long-form articles를 생성하기 위해 diverse perspectives, grounded simulated conversation, outline curation을 결합한다고 설명한다. [출처: https://arxiv.org/abs/2402.14207]",
                "FreshWiki 평가에서 outline-driven RAG baseline과 비교해 STORM 산출물이 organized로 판단되는 비율이 25%p 높고, broad in coverage가 10% 높았다고 보고한다. [출처: https://storm-project.stanford.edu/research/storm/]",
                "Co-STORM의 EMNLP 2024 페이지는 사용자가 검색엔진보다 Co-STORM을 선호한 비율 70%, RAG chatbot보다 선호한 비율 78%를 초록에 명시한다. [출처: https://aclanthology.org/2024.emnlp-main.554/]",
            ],
            "conclusion": "검증 가능한 주장은 ‘조직성·coverage·사용자 선호’ 개선까지이며, 사실 정확도 만능 주장은 이 자료만으로는 과장이다.",
            "uncertainty": "수치들은 특정 벤치마크와 연구 설정의 결과이므로, 로컬 스킬 산출물에는 재검증 없이 그대로 일반화하지 않는다.",
        },
        {
            "name": "미래학자",
            "persona": "하이브리드 도구·출판 파이프라인 전망",
            "findings": [
                "Co-STORM은 여러 LM agents가 사용자 대신 질문을 던지고, 사용자는 담화를 관찰하거나 조향한다는 모델이다. [출처: https://aclanthology.org/2024.emnlp-main.554/]",
                "공식 GitHub README는 Co-STORM이 discourse를 hierarchical concept structure인 dynamic mind map으로 조직해 shared conceptual space를 만든다고 설명한다. [출처: https://github.com/stanford-oval/storm]",
                "이 프로젝트의 hybrid 방식은 STORM의 ‘내용 생산/검토’와 adaptive-html-final의 ‘무 JS 단일 HTML·테마·검증 게이트’를 분리하므로, 리서치 품질과 배포 안정성을 각각 다른 계약으로 관리할 수 있다. [추론]",
            ],
            "conclusion": "다음 실용 지점은 ‘STORM으로 출처·모순·검토를 만들고, 검증 가능한 HTML 스킬로 발표물을 고정하는 이중 계약’이다.",
            "uncertainty": "다중 agent 담화가 조직 내 의사결정 품질을 얼마나 높이는지는 실제 사용 로그와 편집자 평가가 필요하다.",
        },
    ],
}

CONTRADICTION_MAP = {
    "consensus": [
        "다섯 관점 모두 STORM의 강점이 최종 문장 생성보다 pre-writing 단계, 특히 질문 생성과 개요 품질에 있다고 본다.",
        "출처 grounding이 있어도 편향 전이와 부당한 연결을 별도 검토해야 한다는 데 합의한다.",
        "하이브리드 산출물은 연구 내용과 HTML 표현 계층을 분리해야 검증 가능성이 높아진다.",
    ],
    "contradictions": [
        {
            "issue": "품질 개선 수치를 도입 근거로 삼을 수 있는가",
            "a": "학자 관점: +25% 조직성, +10% coverage는 명확한 연구 결과이므로 pre-writing 품질 개선 근거가 된다. [출처: https://storm-project.stanford.edu/research/storm/]",
            "b": "회의주의자 관점: 같은 자료가 publication-ready가 아니며 source bias transfer를 경고하므로 최종 품질 보장으로 읽으면 안 된다. [출처: https://github.com/stanford-oval/storm]",
            "why_unresolved": "평가 지표가 조직/coverage 중심이라 factuality·편집 비용·도메인별 안전성까지 포괄하지 않는다.",
        },
        {
            "issue": "자동화는 비용을 줄이는가, 새 비용을 만드는가",
            "a": "경제학자 관점: 개요와 질문을 먼저 검수하면 재작성 비용을 줄일 수 있다. [추론]",
            "b": "경제학자/회의주의자 관점: 검색 API, retriever, 모델 계층, 편집 검수 비용이 새로 생긴다. [출처: https://github.com/stanford-oval/storm]",
            "why_unresolved": "조직별 주제 난도와 편집자 시간 단가가 달라 공통 ROI를 단정할 수 없다.",
        },
        {
            "issue": "사용자가 질문해야 하는가, agent가 질문해야 하는가",
            "a": "Co-STORM 관점: agent들이 사용자를 대신해 질문을 던져 unknown unknowns를 발견하게 한다. [출처: https://aclanthology.org/2024.emnlp-main.554/]",
            "b": "회의주의자 관점: 사용자가 질문을 조향하지 않으면 출처 선택과 프레이밍이 시스템 편향으로 굳을 수 있다. [추론]",
            "why_unresolved": "autonomous discovery와 human steering의 최적 비율은 과업과 위험 수준에 따라 달라진다.",
        },
    ],
    "blind_spots": [
        "한국어·로컬 지식베이스에서 perspective mining과 검색 grounding 품질이 영어 Wikipedia-like 주제만큼 유지되는지 별도 검증이 필요하다.",
        "비공개 내부 문서 기반 리서치에서 개인정보·보안 경계가 어디에 놓여야 하는지 이 자료만으로는 충분하지 않다.",
        "adaptive-html-final 출력의 품질 게이트는 HTML 무결성 검증이지, STORM 리서치 사실성 검증을 자동 대체하지 않는다.",
    ],
    "key_tension": "STORM은 ‘더 똑똑한 최종 저자’인가, 아니면 ‘더 좋은 질문과 개요를 만드는 사전 조사 엔진’인가. 이 하이브리드의 안전한 결론은 후자다.",
}

SYNTHESIS = {
    "lead": "STORM식 다관점 리서치의 실질 가치는 최종 문장을 대신 써주는 데 있지 않다. 더 정확한 위치는 ‘질문을 다양화하고, 출처를 묶고, 모순을 드러내는 pre-writing 엔진’이다. 따라서 이 프로젝트의 안전한 하이브리드는 storm-research가 만든 내용만 사용하고, 표현·테마·무결성은 adaptive-html-final v5.10.5의 HTML 계약으로 고정하는 방식이다.",
    "sections": [
        {
            "title": "1. 무엇이 검증됐나",
            "body": "STORM 원논문은 diverse perspectives, grounded simulated conversation, outline curation을 결합해 long-form article pre-writing을 개선하는 시스템을 제안한다. Stanford 프로젝트 페이지는 FreshWiki 평가에서 organized 판단이 25%p, coverage breadth가 10% 높았다고 요약한다. 그러나 이 수치는 글쓰기 품질의 특정 차원을 말하며 사실 검증 만능이나 출판-ready를 뜻하지 않는다.",
        },
        {
            "title": "2. 왜 질문 생성이 병목인가",
            "body": "프로젝트 페이지는 직접 prompting만으로는 long-tail 주제에서 피상적 질문이 나오기 쉽다고 설명한다. STORM은 관점을 먼저 부여하고, 검색 기반 답변으로 이해가 갱신될 때 후속 질문을 유도한다. 이는 HTML 리포트 생성에서도 ‘본문을 바로 쓰기’보다 ‘질문·개요·출처를 먼저 잠그기’가 품질 병목이라는 교훈으로 이어진다.",
        },
        {
            "title": "3. 어디서 실패하는가",
            "body": "논문과 프로젝트 페이지가 직접 경고한 실패 모드는 source bias transfer와 over-association이다. 다시 말해, 출처를 붙였다고 해서 편향이 사라지지 않고, 서로 관련 없는 사실을 자연스러운 이야기로 엮는 위험이 남는다. 그래서 storm-research 파이프라인의 peer review 단계는 장식이 아니라 필수 게이트다.",
        },
        {
            "title": "4. 하이브리드 출력의 운영 해석",
            "body": "이 산출물은 STORM의 HTML 빌더를 쓰지 않고, storm-research의 스캔·모순 지도·종합·동료 검토 내용만 가져온다. 그런 다음 adaptive-html-final의 expert_html 레이아웃, risk-matrix vt 템플릿, wg-16 구현 계획 위젯, CSS 해시·source snapshot 검증으로 표현 계층을 고정한다. 내용 검증과 표현 검증을 분리하는 것이 핵심이다.",
        },
    ],
    "unresolved": [
        "내부 문서/한국어 자료에서 STORM식 perspective mining이 동일하게 효과적인지 검증이 필요하다.",
        "다중 LLM을 실제로 병렬 실행할 때 비용·속도·출처 품질이 단일 LLM solo fallback보다 얼마나 나은지 계측해야 한다.",
        "HTML 품질 게이트가 통과해도 리서치 사실성은 별도 출처 감사와 peer review를 유지해야 한다.",
    ],
}

PEER_REVIEW = {
    "verdict": "조건부 통과 + MINOR 반영",
    "confidence": {"source_diversity": "중", "citation_fidelity": "상", "certainty_honesty": "상"},
    "defects": [
        {
            "severity": "MAJOR",
            "type": "출처 편향 전이",
            "finding": "핵심 근거가 Stanford 원논문·프로젝트·GitHub에 집중되어 있어 자기 설명 편향이 있다.",
            "fix": "HTML의 source note와 validation checklist에 ‘독립 외부 벤치마크 미확인’을 명시한다.",
        },
        {
            "severity": "MINOR",
            "type": "부당한 연결 위험",
            "finding": "Co-STORM 사용자 선호 수치를 이 프로젝트의 HTML 하이브리드 효과로 연결하면 비약이다.",
            "fix": "Co-STORM 수치는 multi-agent discourse의 근거로만 쓰고, adaptive-html-final 효과와 직접 연결하지 않는다.",
        },
        {
            "severity": "MINOR",
            "type": "미인용 운영 주장",
            "finding": "ROI·비용 절감 문장은 자료에서 직접 측정된 값이 아니다.",
            "fix": "경제성 문장은 [추론]으로 표시하고 계측 필요 항목으로 이동한다.",
        },
    ],
    "most_important_open_question": "실제 팀 문서 생산에서 STORM식 다관점 리서치가 편집 시간과 오류율을 어느 정도 줄이는가?",
}


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def icon(icon_id: str) -> str:
    return subprocess.check_output(
        ["python3", str(SKILL / "scripts" / "body_icon_markup.py"), icon_id, "--class", "body-icon--sm"],
        cwd=ROOT,
        text=True,
    ).strip()


def h2(num: int, title: str, icon_id: str, key: bool = False) -> str:
    cls = "num is-key" if key else "num"
    return f'<h2>{icon(icon_id)}<span class="{cls}">{num}</span>{esc(title)}</h2>'


def css_bundle() -> tuple[dict[str, str], dict]:
    asset_text = {name: (ASSETS / name).read_text(encoding="utf-8") for name in INLINE_ORDER}
    core = "\n".join(asset_text[name] for name in CORE_ORDER)
    core_hash = hashlib.sha256(core.encode("utf-8")).hexdigest()
    slots = {
        "THEME_CSS": f"/* adaptive-html-final-core-css-sha256: {core_hash} */\n" + asset_text["theme.css"],
        "COMPONENTS_CSS": asset_text["components.css"],
        "VISUAL_COMPONENTS_CSS": asset_text["visual-components.css"],
        "WIDGETS_CSS": asset_text["widgets.css"],
        "VISUAL_HTML_CSS": asset_text["visual-html.css"],
        "BODY_ICONS_CSS": asset_text["body-icons.css"],
        "EDITORIAL_PATTERNS_CSS": asset_text["editorial-patterns.css"],
        "SHAPE_VISUALS_CSS": "",
        "WORKFLOW_VISUALS_CSS": "",
        "LAYOUTS_CSS": asset_text["layouts.css"],
        "PRINT_CSS": asset_text["print.css"],
        "THEME_DARK_CSS": asset_text["theme-dark.css"],
    }
    integrity = {
        "core_css_sha256": core_hash,
        "asset_order": CORE_ORDER,
        "profile": "auto",
        "asset_sha256": {name: hashlib.sha256(asset_text[name].encode("utf-8")).hexdigest() for name in INLINE_ORDER},
    }
    return slots, integrity


def href_for(url: str) -> str:
    if url.startswith(("http://", "https://", "mailto:")):
        return url
    return "../../../" + url.lstrip("/")


def source_link(src_id: str) -> str:
    item = next(s for s in SOURCES_USED if s["id"] == src_id)
    return f'<a href="{esc(href_for(item["url"]))}">{esc(item["title"])}</a>'


def source_chips(ids: list[str]) -> str:
    return "".join(f'<span class="tag">{esc(next(s["kind"] for s in SOURCES_USED if s["id"] == sid))}</span>' for sid in ids)


def build_executive_summary(version: str) -> str:
    return f'''
{h2(1, "Executive Summary · 안전한 결론", "idea", True)}
<p class="h2-sub">storm-research는 내용을 만들고, adaptive-html-final은 최신 v{esc(version)} 스타일과 검증 계약으로 표현을 고정했습니다.</p>
<nav class="toc-map" aria-label="리포트 목차"><span class="label">Report TOC</span><p>요약, 의사결정, 파이프라인, 리스크, 30일 실행, 검증 기준 순서로 읽습니다.</p><div class="toc-pills"><a class="toc-pill" href="#main"><b>00</b>요약</a><a class="toc-pill" href="#storm-decision"><b>01</b>판정</a><a class="toc-pill" href="#storm-architecture"><b>02</b>하이브리드 구조</a><a class="toc-pill" href="#storm-risk"><b>03</b>모순·리스크</a><a class="toc-pill" href="#storm-roadmap"><b>04</b>실행 계획</a><a class="toc-pill" href="#storm-validation"><b>05</b>검증</a></div></nav>
<div class="summary-grid card-grid rail-cycle">
  <article class="summary-card"><div class="label">Verdict</div><h3>Pre-writing 엔진으로 채택</h3><p>STORM은 최종 저자가 아니라 질문·출처·개요·모순을 만드는 사전 조사 엔진으로 쓸 때 가장 안전합니다.</p></article>
  <article class="summary-card"><div class="label">Evidence</div><h3>조직성 +25%p · coverage +10%</h3><p>Stanford 프로젝트는 outline-driven RAG baseline 대비 조직성과 폭 지표 개선을 보고합니다. {source_link('storm-project')}</p></article>
  <article class="summary-card"><div class="label">Guardrail</div><h3>출처 편향·부당 연결 주의</h3><p>논문이 직접 지목한 실패 모드이므로 peer review와 source note를 필수로 둡니다. {source_link('storm-paper')}</p></article>
</div>
<div class="hero-analogy"><div class="tag">Hybrid contract</div><h3>내용은 STORM, 표현은 adaptive-html-final</h3><p>{esc(SYNTHESIS['lead'])}</p></div>
'''


def build_decision_cards() -> str:
    cards = [
        ("Adopt", "도입하되 범위 제한", "STORM은 리서치 질문·개요·모순 지도까지 책임지고, 최종 사실 판정은 출처 감사와 편집자 검수에 남깁니다."),
        ("Do not claim", "25% 더 똑똑하다는 표현 금지", "수치는 조직성 25%p, coverage 10% 개선입니다. 모델 지능이나 사실 정확도 향상으로 바꾸면 claim drift입니다."),
        ("Hybrid", "HTML 출력은 별도 계약", "storm-research의 산출 텍스트만 사용하고, HTML은 v5.10.5 레이아웃·테마·무JS·해시 검증으로 고정합니다."),
        ("Measure", "ROI는 계측 후 판단", "검색 API, LLM 계층, 편집 시간, 재작성 감소율을 함께 봐야 경제성을 말할 수 있습니다."),
    ]
    body = "\n".join(
        f'<article class="decision-card"><span class="case-label">{esc(k)}</span><h3>{esc(t)}</h3><p>{esc(d)}</p></article>'
        for k, t, d in cards
    )
    return f'''
<div id="storm-decision"></div>
{h2(2, "의사결정 카드 · 이 하이브리드를 어떻게 써야 하나", "decision", True)}
<p class="h2-sub">다섯 관점 스캔과 동료 검토를 통과한 운영 판정입니다.</p>
<div class="decision-grid grid-2">{body}</div>
<div class="table-scroll"><table class="table"><caption>STORM 주장과 안전한 해석</caption><thead><tr><th>항목</th><th>자료에 있는 사실</th><th>이 프로젝트의 해석</th><th>금지할 과장</th></tr></thead><tbody>
<tr><th scope="row">품질 수치</th><td>조직성 +25%p, coverage +10%</td><td>개요·사전조사 품질 개선 근거</td><td>모델이 25% 더 똑똑함</td></tr>
<tr><th scope="row">출력 품질</th><td>편집자에게 pre-writing 단계에서 유용</td><td>최종 글 전 검수 초안으로 사용</td><td>출판-ready 자동 기사</td></tr>
<tr><th scope="row">Co-STORM</th><td>unknown unknowns 탐색과 mind map 지원</td><td>질문 발견과 조향형 리서치에 적합</td><td>모든 리서치 자동 대체</td></tr>
</tbody></table></div>
'''


def build_wg16_plan() -> str:
    return '''
<div class="wg-16" aria-labelledby="wg-16-title">
  <header class="wg-16-head">
    <p class="wg-16-kicker">HYBRID IMPLEMENTATION · 30D</p>
    <h3 id="wg-16-title" class="wg-16-h">STORM 내용 → adaptive-html-final 출력 전환 계획</h3>
    <p class="wg-16-lead">리서치 품질과 HTML 품질을 서로 다른 게이트로 분리해, 한쪽의 성공을 다른 쪽의 성공으로 과장하지 않습니다.</p>
  </header>
  <div class="wg-16-panel">
    <h3 class="wg-16-h3">마일스톤 타임라인</h3>
    <ol class="wg-16-ms">
      <li class="wg-16-ms-item wg-16-done"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">M0 · 주제와 solo fallback 확정</span><span class="wg-16-badge wg-16-bd-done">완료</span></div><p class="wg-16-ms-desc">cmux 부재를 기록하고 5관점 인라인 스캔으로 전환.</p></div></li>
      <li class="wg-16-ms-item wg-16-done"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">M1 · 출처 기반 스캔·모순 지도</span><span class="wg-16-badge wg-16-bd-done">완료</span></div><p class="wg-16-ms-desc">Stanford paper/project/GitHub/Co-STORM 공식 자료만 핵심 근거로 사용.</p></div></li>
      <li class="wg-16-ms-item wg-16-active"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">M2 · HTML 고정·검증</span><span class="wg-16-badge wg-16-bd-active">진행</span></div><p class="wg-16-ms-desc">expert_html + risk-matrix + wg-16 + source snapshot 검증.</p></div></li>
      <li class="wg-16-ms-item"><div class="wg-16-ms-mark"><span class="wg-16-ms-node"></span></div><div class="wg-16-ms-card"><div class="wg-16-ms-top"><span class="wg-16-ms-name">M3 · 다음 워크스트림</span><span class="wg-16-badge">예정</span></div><p class="wg-16-ms-desc">cmux full 모드와 다중 LLM 비용/품질 계측 비교.</p></div></li>
    </ol>
    <h3 class="wg-16-h3">데이터 플로우</h3>
    <div class="wg-16-flow" aria-label="하이브리드 생성 플로우">
      <div class="wg-16-fnode">주제 선택<span class="wg-16-fnode-s">free topic</span></div>
      <div class="wg-16-fnode wg-16-fnode-q">5관점 스캔<span class="wg-16-fnode-s">storm solo</span></div>
      <div class="wg-16-fnode wg-16-fnode-hot">모순·검토<span class="wg-16-fnode-s">bias check</span></div>
      <div class="wg-16-fnode wg-16-fnode-good">HTML 렌더<span class="wg-16-fnode-s">v5.10.5</span></div>
      <div class="wg-16-fnode">검증 산출<span class="wg-16-fnode-s">validate</span></div>
    </div>
    <h3 class="wg-16-h3">운영 리스크</h3>
    <div class="wg-16-table-wrap"><div class="table-scroll"><table class="wg-16-table"><caption>하이브리드 운영 리스크와 완화책</caption><thead><tr><th scope="col">리스크</th><th scope="col">가능성</th><th scope="col">영향</th><th scope="col">완화책</th></tr></thead><tbody>
      <tr><th scope="row">출처 편향 전이</th><td><span class="wg-16-lv wg-16-lv-mid">중</span></td><td><span class="wg-16-lv wg-16-lv-hi">높음</span></td><td>source note와 peer review 결함 목록을 본문에 노출</td></tr>
      <tr><th scope="row">Co-STORM 수치 과잉 일반화</th><td><span class="wg-16-lv wg-16-lv-mid">중</span></td><td><span class="wg-16-lv wg-16-lv-mid">중</span></td><td>사용자 선호 수치는 담화 모델 근거로만 제한</td></tr>
      <tr><th scope="row">HTML 검증을 사실 검증으로 오해</th><td><span class="wg-16-lv wg-16-lv-lo">낮음</span></td><td><span class="wg-16-lv wg-16-lv-hi">높음</span></td><td>validate_output은 표현 게이트임을 검증 섹션에 분리 표기</td></tr>
    </tbody></table></div></div>
  </div>
</div>
'''


def build_architecture() -> str:
    source_rows = "\n".join(
        f'<tr><th scope="row">{esc(s["id"])}</th><td><a href="{esc(href_for(s["url"]))}">{esc(s["title"])}</a></td><td>{esc(s["kind"])}</td><td>{esc(s["notes"])}</td></tr>'
        for s in SOURCES_USED
    )
    return f'''
<div id="storm-architecture"></div>
{h2(3, "하이브리드 구조 · 내용과 표현을 분리한다", "flow")}
<p class="h2-sub">storm-research는 리서치 내용만, adaptive-html-final은 최신 스타일·무JS·검증 계약만 담당합니다.</p>
{build_wg16_plan()}
<div class="table-scroll"><table class="table"><caption>이번 STORM 리서치에 사용한 출처와 역할</caption><thead><tr><th>ID</th><th>출처</th><th>종류</th><th>사용한 근거</th></tr></thead><tbody>{source_rows}</tbody></table></div>
<div class="source-note"><div class="label">Fact / Inference split</div><p><strong>FACT</strong>는 위 출처에 직접 있는 주장입니다. <strong>INFERENCE</strong>는 하이브리드 설계에 대한 이 프로젝트의 해석이며, ROI·운영 비용은 확인 필요로 남깁니다.</p></div>
'''


def build_risk_matrix() -> str:
    contradictions = "\n".join(
        f'<tr><th scope="row">{esc(c["issue"])}</th><td>{esc(c["a"])}</td><td>{esc(c["b"])}</td><td>{esc(c["why_unresolved"])}</td></tr>'
        for c in CONTRADICTION_MAP["contradictions"]
    )
    blind = "".join(f'<li>{esc(x)}</li>' for x in CONTRADICTION_MAP["blind_spots"])
    return f'''
<div id="storm-risk"></div>
{h2(4, "모순 지도와 리스크 매트릭스", "warning", True)}
<p class="h2-sub">STORM의 강점과 한계를 봉합하지 않고, 실제 운영 리스크로 재배치합니다.</p>
<section class="vt-shell"><div class="vt-frame"><div class="rm-grid"><div class="rm-cell rm-head">가능성</div><div class="rm-cell rm-head">낮음</div><div class="rm-cell rm-head">중간</div><div class="rm-cell rm-head">높음</div><div class="rm-cell rm-head">영향 큼</div><div class="rm-cell rm-risk low">HTML 검증 오해</div><div class="rm-cell rm-risk med">출처 편향 전이</div><div class="rm-cell rm-risk high">부당 연결을 결론으로 승격</div><div class="rm-cell rm-head">영향 중간</div><div class="rm-cell rm-risk low">테마/링크 누락</div><div class="rm-cell rm-risk med">ROI 단정</div><div class="rm-cell rm-risk med">Co-STORM 수치 과잉 일반화</div><div class="rm-cell rm-head">영향 작음</div><div class="rm-cell rm-risk low">출처 목록 과밀</div><div class="rm-cell rm-risk low">용어 혼동</div><div class="rm-cell rm-risk low">중복 카드</div></div></div></section>
<div class="table-scroll"><table class="table"><caption>다섯 관점이 만든 핵심 모순</caption><thead><tr><th>충돌 대상</th><th>A 입장</th><th>B 입장</th><th>미해결 이유</th></tr></thead><tbody>{contradictions}</tbody></table></div>
<div class="danger"><div class="label">Key tension</div><div class="name">{esc(CONTRADICTION_MAP['key_tension'])}</div><p>이 긴장을 유지해야 STORM 산출물을 과장하지 않고, HTML 출력 검증과 리서치 사실성 검증을 분리할 수 있습니다.</p></div>
<div class="box"><p><strong>남은 사각지대</strong></p><ul>{blind}</ul></div>
'''


def build_roadmap() -> str:
    synth_rows = "\n".join(
        f'<article class="card-block rail-blue"><span class="case-label">Synthesis</span><h3>{esc(sec["title"])}</h3><p>{esc(sec["body"])}</p></article>'
        for sec in SYNTHESIS["sections"]
    )
    unresolved = "".join(f'<li>{esc(x)}</li>' for x in SYNTHESIS["unresolved"])
    return f'''
<div id="storm-roadmap"></div>
{h2(5, "30일 실행 로드맵", "timeline")}
<p class="h2-sub">오늘의 하이브리드 산출물을 일회성 데모가 아니라 반복 가능한 파이프라인으로 만들기 위한 후속 계획입니다.</p>
<div class="card-grid rail-cycle">{synth_rows}</div>
<div class="table-scroll"><table class="table"><caption>30일 검증 계획</caption><thead><tr><th>기간</th><th>작업</th><th>성공 기준</th><th>산출물</th></tr></thead><tbody>
<tr><th scope="row">D0~D3</th><td>storm-research solo/full 결과 비교 샘플 3건 수집</td><td>같은 주제에서 출처 다양성·모순 수·편집 시간 기록</td><td>comparison log</td></tr>
<tr><th scope="row">D4~D10</th><td>HTML 출력 품질 게이트 자동화</td><td>validate/quality/render audit가 한 명령으로 재현</td><td>render-audit.json</td></tr>
<tr><th scope="row">D11~D20</th><td>한국어 내부 문서 주제 테스트</td><td>확인 필요·UNKNOWN 라벨이 유지되고 가짜 출처 0건</td><td>peer-review sheet</td></tr>
<tr><th scope="row">D21~D30</th><td>비용·편집 시간 ROI 측정</td><td>초안 작성/수정/검수 시간을 수동 리서치 기준과 비교</td><td>ROI dashboard</td></tr>
</tbody></table></div>
<div class="good"><div class="label">Unresolved</div><div class="name">가장 중요한 미해결 질문</div><p>{esc(PEER_REVIEW['most_important_open_question'])}</p><ul>{unresolved}</ul></div>
'''


def build_validation() -> str:
    defects = "\n".join(
        f'<tr><th scope="row"><span class="tag">{esc(d["severity"])}</span></th><td>{esc(d["type"])}</td><td>{esc(d["finding"])}</td><td>{esc(d["fix"])}</td></tr>'
        for d in PEER_REVIEW["defects"]
    )
    confidence = PEER_REVIEW["confidence"]
    return f'''
<div id="storm-validation"></div>
{h2(6, "동료 검토와 완료 기준", "audit")}
<p class="h2-sub">storm-review의 적대적 검토 결과를 HTML 산출물 안에 남겨 과장·편향·비약을 차단합니다.</p>
<div class="summary-grid card-grid rail-cycle">
  <article class="summary-card"><div class="label">Peer review verdict</div><h3>{esc(PEER_REVIEW['verdict'])}</h3><p>BLOCKER는 없지만 출처 편향과 ROI 단정 위험을 본문에 반영했습니다.</p></article>
  <article class="summary-card"><div class="label">Citation fidelity</div><h3>{esc(confidence['citation_fidelity'])}</h3><p>핵심 수치와 방법론 주장은 공식 논문·프로젝트·GitHub 출처로 제한했습니다.</p></article>
  <article class="summary-card"><div class="label">Certainty honesty</div><h3>{esc(confidence['certainty_honesty'])}</h3><p>비용 절감·한국어 성능·조직 ROI는 추론 또는 확인 필요로 분리했습니다.</p></article>
</div>
<div class="table-scroll"><table class="table"><caption>storm-review 결함 목록과 반영 조치</caption><thead><tr><th>심각도</th><th>유형</th><th>지적</th><th>반영</th></tr></thead><tbody>{defects}</tbody></table></div>
<div class="source-note"><div class="label">HTML validation scope</div><p><code>validate_output.py</code>와 <code>quality_contract_check.py</code>는 무JS·CSS 해시·레이아웃·본문 구조 검증입니다. 리서치 사실성 검증은 위 출처 표와 peer review 결함 목록으로 별도 관리합니다.</p></div>
'''


def build_final_recommendation(version: str) -> str:
    return f'''
{h2(7, "최종 권고 · 지금은 이렇게 쓰자", "success", True)}
<p>이 하이브리드는 <strong>STORM 리서치 산출을 최종 문서로 착각하지 않고</strong>, adaptive-html-final v{esc(version)}의 검증 가능한 HTML 표현으로 고정하는 방식일 때 실용적입니다. 다음 실행에서는 cmux full 모드가 가능할 때 5개 영혼을 실제 병렬로 돌리고, 이번 solo fallback 결과와 출처 다양성·모순 수·편집 시간을 비교하세요.</p>
<div class="summary-card"><p><strong>바로 적용할 운영 규칙</strong></p><ul><li>storm-research 결과는 scan/contradiction/synthesis/review 네 파일로 남긴다.</li><li>HTML에는 sources manifest와 peer review 결함 목록을 반드시 포함한다.</li><li>검증 OK를 리서치 사실성 OK로 말하지 않는다.</li></ul></div>
<div class="tag-list"><span class="tag">storm-research solo</span><span class="tag">expert_html</span><span class="tag">profile auto</span><span class="tag">adaptive-html-final v{esc(version)}</span><span class="tag">no behavioral JS</span></div>
'''


def build_source_note() -> str:
    links = "".join(f'<li><a href="{esc(href_for(s["url"]))}">{esc(s["title"])}</a> — {esc(s["notes"])}</li>' for s in SOURCES_USED)
    return f'''
<div class="label">Sources & provenance</div>
<p>이 HTML의 본문 내용은 storm-research solo fallback으로 만든 스캔·모순 지도·종합·동료 검토 결과만 사용했습니다. 표현 계층은 adaptive-html-final 최신 자산을 사용했습니다.</p>
<ol>{links}</ol>
'''


def build_meta(version: str) -> str:
    generated = datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%d %H:%M KST")
    return f'''<span>mode=expert_html</span><span>layout=expert-report.html</span><span>profile=auto</span><span>storm=solo fallback</span><span>adaptive-html-final v{esc(version)}</span><div class="generated-row"><p class="generated-date">Generated {esc(generated)}</p><div class="lens-strip" aria-label="적용 렌즈"><span class="lens-strip-label">LENS</span><span class="lens-chip">STORM scan</span><span class="lens-chip">contradiction map</span><span class="lens-chip">peer review</span><span class="lens-chip">HTML gate</span></div></div>'''


def render_html() -> None:
    version = json.loads((SKILL / "manifest.json").read_text(encoding="utf-8"))["version"]
    slots, integrity = css_bundle()
    layout = (ASSETS / "layouts" / "expert-report.html").read_text(encoding="utf-8")
    layout_replacements = {
        "KICKER": '<span class="kicker-text">STORM RESEARCH · HYBRID HTML REPORT</span>',
        "TITLE": "STORM식 다관점 리서치 하이브리드 진단",
        "SUBTITLE": "storm-research 스킬로 주제를 정하고 다섯 관점 리서치·모순 지도·종합·동료 검토를 만든 뒤, 현재 프로젝트 최신 adaptive-html-final 스타일로 고정한 전문가 리포트입니다.",
        "META": build_meta(version),
        "EXECUTIVE_SUMMARY": build_executive_summary(version),
        "DECISION_CARDS": build_decision_cards(),
        "ARCHITECTURE": build_architecture(),
        "RISK_MATRIX": build_risk_matrix(),
        "PRIORITY_ROADMAP": build_roadmap(),
        "VALIDATION_CHECKLIST": build_validation(),
        "FINAL_RECOMMENDATION": build_final_recommendation(version),
        "SOURCE_NOTE": build_source_note(),
    }
    for key, value in layout_replacements.items():
        layout = layout.replace("{{" + key + "}}", value)
    leftovers = re.findall(r"\{\{[A-Z_]+\}\}", layout)
    if leftovers:
        raise SystemExit(f"unfilled layout placeholders: {sorted(set(leftovers))}")

    base = (ASSETS / "base.html").read_text(encoding="utf-8")
    replacements = {
        "TITLE": "STORM식 다관점 리서치 하이브리드 진단",
        "DESCRIPTION": "storm-research 스킬의 다관점 리서치 내용을 adaptive-html-final v5.10.5 전문가 리포트 스타일로 렌더링한 하이브리드 HTML.",
        "JSON_LD_BLOCK": "",
        "BODY": layout,
        "FOOTER": "",
        **slots,
    }
    for key, value in replacements.items():
        base = base.replace("{{" + key + "}}", value)
    leftovers = re.findall(r"\{\{[A-Z_]+\}\}", base)
    if leftovers:
        raise SystemExit(f"unfilled base placeholders: {sorted(set(leftovers))}")

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "pages").mkdir(exist_ok=True)
    (OUT / "index.html").write_text(base, encoding="utf-8")
    write_sources(integrity)


def write_sources(integrity: dict) -> None:
    (SOURCES / "assets").mkdir(parents=True, exist_ok=True)
    for name in INLINE_ORDER:
        shutil.copyfile(ASSETS / name, SOURCES / "assets" / name)
    (SOURCES / "css-integrity.json").write_text(json.dumps(integrity, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    shutil.copyfile(SKILL / "manifest.json", SOURCES / "adaptive-html-final-manifest.json")
    (SOURCES / "profile.json").write_text(json.dumps({"profile": "auto"}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    report = {
        "topic": TOPIC,
        "slug": SLUG,
        "storm_mode": SCAN["mode"],
        "sources": SOURCES_USED,
        "scan": SCAN,
        "contradiction_map": CONTRADICTION_MAP,
        "synthesis": SYNTHESIS,
        "peer_review": PEER_REVIEW,
    }
    (SOURCES / "storm-research-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (SOURCES / "storm-scan.md").write_text(build_scan_markdown(), encoding="utf-8")
    (SOURCES / "storm-contradiction-map.md").write_text(build_contradiction_markdown(), encoding="utf-8")
    (SOURCES / "storm-synthesis.md").write_text(build_synthesis_markdown(), encoding="utf-8")
    (SOURCES / "storm-peer-review.md").write_text(build_peer_review_markdown(), encoding="utf-8")

    evidence_files = [
        "AGENTS.md",
        "skills/adaptive-html-final/SKILL.md",
        "skills/adaptive-html-final/manifest.json",
        "skills/adaptive-html-final/assets/base.html",
        "skills/adaptive-html-final/assets/layouts/expert-report.html",
        "skills/adaptive-html-final/assets/visual-html-templates/03-risk-matrix.html",
        "skills/adaptive-html-final/assets/widget-templates/16-implementation-plan.html",
        "orginal_skill/storm-research/SKILL.md",
        "orginal_skill/storm-research/prompts/1-multi-perspective-scan.md",
        "orginal_skill/storm-research/prompts/2-contradiction-map.md",
        "orginal_skill/storm-research/prompts/3-synthesis.md",
        "orginal_skill/storm-research/prompts/4-peer-review.md",
        "scripts/build_storm_research_hybrid.py",
    ]
    build_evidence = {
        "mode": "expert_html",
        "topic": TOPIC,
        "profile": "auto",
        "layout": "expert-report.html",
        "primary_vt": "risk-matrix",
        "recommended_wg": "wg-16",
        "section_mapping": {
            "EXECUTIVE_SUMMARY": "storm synthesis lead + decision summary",
            "DECISION_CARDS": "storm contradiction decisions",
            "ARCHITECTURE": "storm pipeline + adaptive-html-final hybrid flow",
            "RISK_MATRIX": "risk-matrix vt + contradiction map",
            "PRIORITY_ROADMAP": "30-day operational validation plan",
            "VALIDATION_CHECKLIST": "storm peer review + HTML validation scope",
            "FINAL_RECOMMENDATION": "safe use recommendation",
        },
        "files": [{"path": rel, "sha256": sha(ROOT / rel)} for rel in evidence_files if (ROOT / rel).exists()],
    }
    (SOURCES / "build-evidence.json").write_text(json.dumps(build_evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_scan_markdown() -> str:
    lines = [f"# {TOPIC} — 다중 관점 스캔", "", f"- 실행 모드: {SCAN['mode']}", f"- 사유: {SCAN['reason']}", ""]
    for idx, soul in enumerate(SCAN["souls"], 1):
        lines += [f"## {idx}. {soul['name']} 관점", "", f"역할: {soul['persona']}", "", "### 발견"]
        lines += [f"- {x}" for x in soul["findings"]]
        lines += ["", f"결론: {soul['conclusion']}", f"불확실성: {soul['uncertainty']}", ""]
    lines += ["## 통합 참고 출처", ""]
    lines += [f"- {s['title']}: {s['url']}" for s in SOURCES_USED]
    return "\n".join(lines) + "\n"


def build_contradiction_markdown() -> str:
    lines = [f"# {TOPIC} — 모순 지도", "", "## 합의 지점"]
    lines += [f"- {x}" for x in CONTRADICTION_MAP["consensus"]]
    lines += ["", "## 모순 지점", ""]
    for c in CONTRADICTION_MAP["contradictions"]:
        lines += [f"### {c['issue']}", f"- A: {c['a']}", f"- B: {c['b']}", f"- 미해결 이유: {c['why_unresolved']}", ""]
    lines += ["## 사각지대"] + [f"- {x}" for x in CONTRADICTION_MAP["blind_spots"]]
    lines += ["", "## 핵심 긴장", CONTRADICTION_MAP["key_tension"], ""]
    return "\n".join(lines)


def build_synthesis_markdown() -> str:
    lines = [f"# {TOPIC}", "", f"> {SYNTHESIS['lead']}", ""]
    for s in SYNTHESIS["sections"]:
        lines += [f"## {s['title']}", s["body"], ""]
    lines += ["## 미해결 질문"] + [f"- {x}" for x in SYNTHESIS["unresolved"]]
    lines += ["", "## 참고 출처"] + [f"- {s['url']}" for s in SOURCES_USED]
    return "\n".join(lines) + "\n"


def build_peer_review_markdown() -> str:
    lines = [f"# Peer Review: {TOPIC}", "", f"통과 판정: {PEER_REVIEW['verdict']}", "", "## 결함 목록"]
    lines += [f"- {d['severity']} / {d['type']}: {d['finding']} → {d['fix']}" for d in PEER_REVIEW["defects"]]
    lines += ["", "## 신뢰도 배지"]
    lines += [f"- {k}: {v}" for k, v in PEER_REVIEW["confidence"].items()]
    lines += ["", f"가장 중요한 미해결 질문: {PEER_REVIEW['most_important_open_question']}", ""]
    return "\n".join(lines)


if __name__ == "__main__":
    render_html()
    print((OUT / "index.html").relative_to(ROOT))
