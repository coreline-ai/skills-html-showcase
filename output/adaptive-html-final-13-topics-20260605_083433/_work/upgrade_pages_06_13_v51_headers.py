#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "pages"


HEADERS = {
    "06-ai-meeting-notes-automation-seo.html": {
        "kicker": "SEO DASHBOARD · AI MEETING NOTES",
        "title": "AI 회의록 자동화 검색 허브",
        "sub": "검색 의도, SERP 문안, 키워드 클러스터, 보안 FAQ, 전환 CTA를 한 화면에서 점검하는 SEO 대시보드다.",
        "meta": ["seo_dashboard", "seo-dashboard.html", "profile auto", "adaptive-html-final v5.1.0", "무 JS"],
        "lenses": ["card-grid", "comparison", "prompt-tuner", "검색 의도", "전환 CTA"],
    },
    "07-conference-talk-platform-adaptation.html": {
        "kicker": "PLATFORM BLOG · CONFERENCE TALK",
        "title": "컨퍼런스 발표를 플랫폼별 글로 변환하기",
        "sub": "한 번의 발표 자료를 티스토리, 벨로그, 네이버, 워드프레스 글로 나눠 발행하는 플랫폼별 변환 설계다.",
        "meta": ["platform_blog", "platform-adaptation.html", "profile auto", "adaptive-html-final v5.1.0", "무 JS"],
        "lenses": ["card-grid", "comparison", "pr-writeup", "플랫폼별 톤", "발행 체크"],
    },
    "08-release-checklist-skill-audit.html": {
        "kicker": "SKILL AUDIT · RELEASE CHECKLIST",
        "title": "배포 체크리스트 생성 스킬 감사 리포트",
        "sub": "배포 전 체크리스트 생성 스킬을 목적, 트리거, 실패 대응, 품질 게이트, 패치 계획 관점에서 감사한다.",
        "meta": ["skill_audit", "skill-audit-report.html", "profile auto", "adaptive-html-final v5.1.0", "무 JS"],
        "lenses": ["quality-gate", "file-tour", "prompt-tuner", "PR writeup", "패치 계획"],
    },
    "09-webhook-signature-verification-reference.html": {
        "kicker": "REFERENCE MANUAL · WEBHOOK SECURITY",
        "title": "Webhook 서명 검증 레퍼런스",
        "sub": "Webhook 요청이 실제 발신자에게서 왔고 중간에 변조되지 않았는지 확인하는 보안 레퍼런스다.",
        "meta": ["reference_html", "reference-manual.html", "profile auto", "adaptive-html-final v5.1.0", "무 JS"],
        "lenses": ["file-tour", "flowchart", "feature flag", "test tuner", "보안 운영"],
    },
    "10-vector-db-pgvector-search-engine-comparison.html": {
        "kicker": "COMPARISON MATRIX · VECTOR SEARCH",
        "title": "벡터 검색 선택 기준: 전용 Vector DB vs pgvector vs 검색 엔진",
        "sub": "문서 검색과 추천 시스템을 만들 때 어떤 저장소를 고를지 기능, 운영, 비용, 전환 가능성으로 비교한다.",
        "meta": ["comparison_html", "comparison-matrix.html", "profile auto", "adaptive-html-final v5.1.0", "무 JS"],
        "lenses": ["comparison-cards", "decision-tree", "risk-matrix", "MVP 판단", "운영 비용"],
    },
    "11-reservation-reminder-delay-case-study.html": {
        "kicker": "CASE STUDY · INCIDENT REVIEW",
        "title": "예약 알림 지연 사고 케이스 스터디",
        "sub": "예약 알림이 42분 지연된 가상 사고를 영향, 원인, 조치, 재발 방지 관점에서 기록한다.",
        "meta": ["case_study_html", "case-study.html", "profile auto", "adaptive-html-final v5.1.0", "무 JS"],
        "lenses": ["incident-summary", "timeline", "swimlane", "SEV-2", "후속 조치"],
    },
    "12-localnote-team-knowledge-landing.html": {
        "kicker": "LANDING BRIEF · LOCALNOTE",
        "title": "LocalNote 팀 지식관리 랜딩 브리프",
        "sub": "회의록, 의사결정, 운영 문서를 한곳에서 찾고 연결하는 작은 팀용 지식관리 제품 브리프다.",
        "meta": ["landing_brief_html", "landing-brief.html", "profile auto", "adaptive-html-final v5.1.0", "무 JS"],
        "lenses": ["hero-map", "card-grid", "feature-flag", "제품 메시지", "온보딩"],
    },
    "13-ai-feature-release-safety-playbook.html": {
        "kicker": "CHECKLIST PLAYBOOK · AI RELEASE",
        "title": "AI 기능 출시 전 안전성 플레이북",
        "sub": "AI 기능을 출시하기 전에 데이터, 품질, 보안, 운영, 사용자 커뮤니케이션을 점검하는 실무 플레이북이다.",
        "meta": ["checklist_playbook", "checklist-playbook.html", "profile auto", "adaptive-html-final v5.1.0", "무 JS"],
        "lenses": ["checklist-flow", "quality-gate", "triage-board", "feature flag", "rollback"],
    },
}


def header_html(spec: dict[str, list[str] | str]) -> str:
    meta = "".join(f"<span>{item}</span>" for item in spec["meta"])
    lenses = "".join(f"<span class=\"lens-chip\">{item}</span>" for item in spec["lenses"])
    return (
        "<header class=\"header\">"
        f"<div class=\"kicker\"><span class=\"kicker-text\">{spec['kicker']}</span></div>"
        f"<h1>{spec['title']}</h1>"
        f"<p class=\"sub\">{spec['sub']}</p>"
        f"<div class=\"meta\">{meta}</div>"
        "<div class=\"generated-row\">"
        "<p class=\"generated-date\">Generated · 2026-06-05 08:34 KST</p>"
        "<div class=\"lens-strip\" aria-label=\"적용 렌즈\">"
        "<span class=\"lens-strip-label\">LENS</span>"
        f"{lenses}"
        "</div></div></header>"
    )


def main() -> None:
    for filename, spec in HEADERS.items():
        path = PAGES / filename
        html = path.read_text(encoding="utf-8")
        new_header = header_html(spec)
        updated, count = re.subn(r"<header class=\"header\">[\s\S]*?</header>", new_header, html, count=1)
        if count != 1:
            raise RuntimeError(f"header replacement failed for {filename}: {count}")
        path.write_text(updated, encoding="utf-8")
        print(f"updated {filename}")


if __name__ == "__main__":
    main()
