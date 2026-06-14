#!/usr/bin/env python3
"""Generate a 17-mode independent benchmark output from canonical skill examples.

The generator intentionally reuses the official example HTML as structural shells,
then rewrites the visible editorial layer with separate benchmark topics and
writes per-mode build sheets/evidence. It is not a general content generator;
it is a deterministic benchmark harness for completion/micro-layout gates.
"""
from __future__ import annotations

import hashlib
import html
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "adaptive-html-final"
EXAMPLES = SKILL / "examples"
MODES_DIR = SKILL / "modes"
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "output" / "2026-06-14" / "codex-5.10.4-independent-17-benchmark"

TOPICS = {
    "skill_audit": ("AI 문서 생성 스킬의 레이아웃 회귀 감사", [
        "감사 결론", "정본 자산 사용 여부", "헤더·목차 계약", "섹션 표면 밀도", "아이콘 카탈로그 일치", "마이크로 레이아웃 리스크", "검증기와 눈검수의 차이", "재발 방지 게이트", "운영 적용 순서", "최종 판정"
    ]),
    "platform_blog": ("B2B SaaS 릴리스 노트의 플랫폼별 재편집", [
        "플랫폼별 독자 차이", "티스토리 long-form 전략", "브런치식 문제 제기", "네이버 검색 유입 구조", "Velog 개발자 맥락", "LinkedIn 요약 카드", "CTA와 출처 배치", "반복 발행 캘린더", "성과 측정 지표", "최종 운영안"
    ]),
    "seo_dashboard": ("AI 검색 시대의 기술 문서 SEO 대시보드", [
        "검색 의도 요약", "핵심 키워드 군", "제목·메타 개선", "SERP 약속 카드", "본문 구조 점검", "내부 링크 설계", "스키마와 FAQ", "콘텐츠 갭", "발행 후 측정", "우선순위 로드맵"
    ]),
    "education_html": ("사내 보안 온보딩 90분 실습 과정", [
        "학습 목표", "선수 지식", "위협 모델 빠른 지도", "실습 환경 준비", "피싱 판별 훈련", "권한 최소화 실습", "로그 해석 과제", "퀴즈와 해설", "현업 적용 체크", "다음 학습 경로"
    ]),
    "github_analysis": ("Postgres 백업 자동화 저장소 도입 실사", [
        "도입 결론", "저장소 신호", "기능 범위", "아키텍처 흔적", "릴리스와 유지보수", "보안·라이선스", "운영 리스크", "대체안 비교", "파일 투어", "채택 조건"
    ]),
    "github_feature_usage": ("오픈소스 인증 모듈 기능·사용법 가이드", [
        "무엇을 해결하나", "핵심 기능 지도", "설치 전 조건", "첫 실행 흐름", "설정 파일 해석", "관리자 기능", "사용자 기능", "확장 포인트", "실제 화면 읽기", "도입 전 체크"
    ]),
    "youtube_analysis": ("AI 회의록 자동화 영상의 실행 가능성 분석", [
        "영상 결론", "챕터별 흐름", "핵심 주장", "데모와 실제 차이", "도구 스택", "자동화 파이프라인", "댓글의 반론", "콘텐츠 갭", "실행 체크리스트", "다음 실험"
    ]),
    "manual_analysis": ("CSV→Postgres 마이그레이션 운영 런북", [
        "런북 결론", "역할별 사용법", "사전조건과 안전장치", "첫 성공 경로", "작업 레시피", "검증 쿼리", "STOP 기준", "트러블슈팅", "운영 교대 기록", "다음 개선"
    ]),
    "expert_html": ("멀티 에이전트 HTML 품질 게이트 아키텍처", [
        "전문가 결론", "문제 구조", "아키텍처 원칙", "품질 게이트 계층", "렌더 감사 모델", "증거 파일 계약", "운영 리스크", "조직 역할", "도입 로드맵", "최종 권고"
    ]),
    "article_html": ("AI 시대 개인 지식관리의 현실적 재설계", [
        "문제 제기", "낡은 분류 체계", "새로운 읽기 단위", "링크보다 질문", "요약의 위험", "검색과 회상", "작은 자동화", "개인 워크플로", "실패 패턴", "결론"
    ]),
    "blog_writer": ("4일간 AI 코드리뷰 루프를 돌린 회고", [
        "첫날의 착각", "둘째 날의 반복", "셋째 날의 증거", "넷째 날의 전환", "도구가 잘한 일", "사람이 봐야 한 일", "레이아웃 회귀", "검증의 한계", "다음 루틴", "개인 결론"
    ]),
    "beginner_html": ("패스키 로그인을 처음 이해하는 사람을 위한 안내", [
        "한 문장 이해", "비밀번호와 차이", "기기 안의 열쇠", "로그인 흐름", "분실하면 어떻게 되나", "피싱에 강한 이유", "서비스 도입 전 확인", "사용자 안내 문구", "자주 묻는 질문", "오늘 해볼 일"
    ]),
    "reference_html": ("HTTP 캐시 헤더 실무 레퍼런스", [
        "빠른 참조", "Cache-Control", "ETag", "Last-Modified", "stale-while-revalidate", "브라우저와 CDN", "금지 조합", "디버깅 명령", "상황별 처방", "체크리스트"
    ]),
    "comparison_html": ("Kafka와 NATS 도입 기준 비교", [
        "선택 결론", "메시지 모델", "운영 복잡도", "지연시간", "내구성", "스케일링", "개발자 경험", "비용 구조", "리스크 매트릭스", "결정 가이드"
    ]),
    "case_study_html": ("검색 인덱스 장애 37분 복구 사례", [
        "사건 개요", "영향 범위", "타임라인", "탐지 신호", "초기 오판", "복구 조치", "고객 커뮤니케이션", "재발 방지", "남은 리스크", "회고 결론"
    ]),
    "landing_brief_html": ("팀 지식베이스 자동 정리 도구 랜딩 브리프", [
        "제품 한 줄", "대상 사용자", "핵심 약속", "기능 카드", "AI 파이프라인", "사용 전후", "가격 신호", "신뢰 장치", "도입 CTA", "다음 액션"
    ]),
    "checklist_playbook": ("월말 데이터 품질 점검 플레이북", [
        "플레이북 결론", "시작 전 준비", "소유자 확인", "스키마 점검", "누락값 점검", "중복 레코드", "품질 게이트", "장애 시 분기", "승인 기록", "완료 보고"
    ]),
}

PARAGRAPH_BANK = [
    "이 섹션은 공식 스킬 자산의 레이아웃을 유지하면서 주제별 판단 기준을 먼저 제시한다. 사용자는 긴 설명을 읽기 전에 무엇을 보류하고 무엇을 실행할지 확인할 수 있어야 한다.",
    "핵심은 단순 요약이 아니라 실행 가능한 구분이다. 근거가 충분한 항목, 추가 확인이 필요한 항목, 즉시 멈춰야 하는 항목을 같은 표면 안에서 분리한다.",
    "뷰 표면은 장식이 아니라 정보 구조다. 왼쪽 색상 라인과 카드 내부 간격은 읽는 사람이 위험도와 우선순위를 빠르게 구분하도록 돕는다.",
    "검증 결과가 OK여도 시각 밀도와 텍스트 리듬이 무너지면 산출물은 완료가 아니다. 따라서 각 섹션은 브라우저에서 폭과 대비를 함께 확인한다.",
    "운영 문서는 마지막 결론보다 중간 판단의 추적 가능성이 중요하다. 누가 어떤 조건에서 다음 단계로 넘겼는지 남겨야 재현성이 생긴다.",
    "현재 페이지는 이전 모드 HTML을 참조하지 않는 독립 벤치마크 항목이다. 다만 공식 자산 파일과 검증 계약은 동일하게 사용해 회귀 여부를 비교할 수 있게 했다.",
    "모호한 표현은 실행 단계에서 비용을 만든다. 그래서 각 카드에는 판단 단서, 확인 위치, 실패 시 대응을 짧은 문장으로 남긴다.",
    "모바일 390px에서도 숫자 pill, rail 텍스트, 태그 간격이 붙지 않아야 한다. 좁은 화면에서 깨지는 요소는 데스크톱에서 보기 좋아도 실패로 간주한다.",
    "출처와 한계는 별도의 면책 문구가 아니라 본문 흐름 안에 들어와야 한다. 그래야 읽는 사람이 다음 확인 작업을 놓치지 않는다.",
    "최종 권고는 단정적이어야 하지만 근거는 분리되어야 한다. 실행, 보류, 재검토를 한 문장 안에 섞지 않는 것이 품질 기준이다.",
]

MODE_ORDER = [
    "skill_audit", "platform_blog", "seo_dashboard", "education_html", "github_analysis", "github_feature_usage", "youtube_analysis", "manual_analysis", "expert_html", "article_html", "blog_writer", "beginner_html", "reference_html", "comparison_html", "case_study_html", "landing_brief_html", "checklist_playbook",
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def slug(s: str) -> str:
    table = {
        "skill_audit": "skill_audit_layout_regression_audit",
        "platform_blog": "platform_blog_saas_release_notes",
        "seo_dashboard": "seo_dashboard_ai_search_docs",
        "education_html": "education_security_onboarding",
        "github_analysis": "github_analysis_pg_backup_due_diligence",
        "github_feature_usage": "github_feature_usage_auth_module",
        "youtube_analysis": "youtube_analysis_meeting_automation",
        "manual_analysis": "manual_analysis_csv_postgres_runbook",
        "expert_html": "expert_multi_agent_quality_architecture",
        "article_html": "article_personal_knowledge_reboot",
        "blog_writer": "blog_ai_codereview_loop_retro",
        "beginner_html": "beginner_passkey_login_guide",
        "reference_html": "reference_http_cache_headers",
        "comparison_html": "comparison_kafka_nats_decision",
        "case_study_html": "case_study_search_index_incident",
        "landing_brief_html": "landing_knowledgebase_autosummary",
        "checklist_playbook": "checklist_monthly_data_quality",
    }
    return table[s]


def find_template(kind: str, name: str) -> str:
    if kind == "vt":
        matches = sorted((SKILL / "assets" / "visual-html-templates").glob(f"*-{name}.html"))
    else:
        idx = name.replace("wg-", "")
        matches = sorted((SKILL / "assets" / "widget-templates").glob(f"{idx}-*.html"))
    if not matches:
        return ""
    return str(matches[0].relative_to(ROOT))


def replace_h2s(text: str, titles: list[str]) -> str:
    i = 0
    def repl(m: re.Match[str]) -> str:
        nonlocal i
        title = titles[i % len(titles)]
        i += 1
        attrs, inner = m.group(1), m.group(2)
        prefix = ""
        pm = re.match(r"^((?:\s*<span\b.*?</span>\s*)+)(.*)$", inner, flags=re.S)
        if pm:
            prefix = pm.group(1)
        return f"<h2{attrs}>{prefix}{html.escape(title)}</h2>"
    return re.sub(r"<h2([^>]*)>(.*?)</h2>", repl, text, flags=re.S)


def replace_h2_subs(text: str, mode: str, topic: str, titles: list[str]) -> str:
    i = 0
    def repl(m: re.Match[str]) -> str:
        nonlocal i
        title = titles[i % len(titles)]
        i += 1
        sentence = f"{topic}에서 '{title}' 판단을 실행 단위로 분리하고, 근거·리스크·다음 행동을 한 화면에서 확인하도록 재구성했다."
        return f'<p class="h2-sub">{html.escape(sentence)}</p>'
    return re.sub(r'<p class="h2-sub">.*?</p>', repl, text, flags=re.S)


def replace_paragraphs(text: str, topic: str) -> str:
    snippets = [f"{topic}: {p}" for p in PARAGRAPH_BANK]
    idx = 0
    def repl(m: re.Match[str]) -> str:
        nonlocal idx
        open_tag, body, close_tag = m.groups()
        if 'class="h2-sub"' in open_tag or "class='h2-sub'" in open_tag or 'generated-date' in open_tag:
            return m.group(0)
        if 'generated-row' in body or 'adaptive-html-final' in body:
            return m.group(0)
        visible = re.sub(r"<.*?>", "", body).strip()
        # Preserve terse labels/chips/cards that are intentionally nowrap in the
        # canonical templates. Long prose belongs in h2-sub/lede/editorial cards,
        # not in these compact fields.
        if len(visible) < 80:
            return m.group(0)
        snippet = snippets[idx % len(snippets)]
        idx += 1
        return f"{open_tag}{html.escape(snippet)}{close_tag}"
    return re.sub(r"(<p\b[^>]*>)(.*?)(</p>)", repl, text, flags=re.S)


def add_build_note(text: str, mode: str, topic: str, titles: list[str]) -> str:
    note = f'''
<div class="lede-note">
  <span class="label">INDEPENDENT BENCHMARK</span>
  <p>{html.escape(topic)}를 {mode} 모드의 독립 신규 주제로 구성했다. 이 페이지는 공식 layout/vt/wg/body-icon 자산을 그대로 사용하고, 섹션은 {len(titles)}개 이상의 판단 단위로 분리했다.</p>
</div>
'''
    m = re.search(r"</header>", text)
    if m:
        return text[:m.end()] + note + text[m.end():]
    return note + text


def update_head(text: str, title: str, description: str) -> str:
    text = re.sub(r"<title>.*?</title>", f"<title>{html.escape(title)}</title>", text, flags=re.S)
    text = re.sub(r'(<meta\s+name="description"\s+content=")[^"]*(">)', lambda m: m.group(1)+html.escape(description, quote=True)+m.group(2), text)
    text = re.sub(r'(<meta\s+property="og:title"\s+content=")[^"]*(">)', lambda m: m.group(1)+html.escape(title, quote=True)+m.group(2), text)
    text = re.sub(r'(<meta\s+property="og:description"\s+content=")[^"]*(">)', lambda m: m.group(1)+html.escape(description, quote=True)+m.group(2), text)
    return text


def update_h1(text: str, title: str) -> str:
    return re.sub(r"(<h1[^>]*>).*?(</h1>)", lambda m: m.group(1)+html.escape(title)+m.group(2), text, count=1, flags=re.S)


def load_modes() -> list[dict]:
    modes = []
    for p in sorted(MODES_DIR.glob("*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        d["_path"] = p
        modes.append(d)
    return sorted(modes, key=lambda d: int(d["priority"]))


def evidence_for(mode: dict, page_rel: str, topic: str, sections: list[str]) -> dict:
    rels = [
        "AGENTS.md",
        "skills/adaptive-html-final/SKILL.md",
        "skills/adaptive-html-final/manifest.json",
        str(mode["_path"].relative_to(ROOT)),
        "skills/adaptive-html-final/assets/base.html",
    ]
    if mode.get("layout_file"):
        rels.append("skills/adaptive-html-final/" + mode["layout_file"])
    vt = find_template("vt", mode.get("primary_vt", ""))
    if vt:
        rels.append(vt)
    for wg in (mode.get("wg_candidates") or [])[:2]:
        wgf = find_template("wg", wg)
        if wgf:
            rels.append(wgf)
    rels += [
        "skills/adaptive-html-final/assets/body-icons.json",
        "skills/adaptive-html-final/references/body-icon-system.md",
        "docs/adaptive-html-final-template-authoring-protocol.md",
        "docs/adaptive-html-final-17-mode-sequential-runbook.md",
    ]
    seen = []
    for r in rels:
        if r not in seen and (ROOT / r).exists():
            seen.append(r)
    return {
        "mode": mode["id"],
        "topic": topic,
        "profile": "auto",
        "layout": Path(mode.get("layout_file", "")).name,
        "primary_vt": mode.get("primary_vt"),
        "page": page_rel,
        "sections": sections,
        "section_mapping": {f"{i:02d}": f"{title} — layout={Path(mode.get('layout_file','')).name}, primary_vt={mode.get('primary_vt')}, wg={', '.join((mode.get('wg_candidates') or [])[:2])}" for i, title in enumerate(sections, 1)},
        "files": [{"path": r, "sha256": sha(ROOT / r)} for r in seen],
    }


def build_sheet(mode: dict, topic: str, sections: list[str], page_rel: str) -> str:
    wg = mode.get("wg_candidates") or []
    lines = [
        f"# Mode Build Sheet — {mode['id']}",
        "",
        f"- mode: `{mode['id']}`",
        f"- topic: {topic}",
        "- profile: `auto`",
        f"- layout: `{mode.get('layout_file')}`",
        f"- primary vt: `{mode.get('primary_vt')}`",
        f"- wg candidates: {', '.join(wg) if wg else 'none'}",
        f"- page: `{page_rel}`",
        "",
        "## Sections",
    ]
    for i, title in enumerate(sections, 1):
        lines.append(f"{i}. {title}")
    lines += [
        "",
        "## Template mapping",
        "",
        "| Section | Pattern |",
        "|---:|---|",
    ]
    patterns = ["layout scaffold", f"vt-{mode.get('primary_vt')}", "lede-note/source-note", "wg widget", "editorial rail card"]
    for i, title in enumerate(sections, 1):
        lines.append(f"| {i} | {html.escape(title)} → {patterns[(i-1)%len(patterns)]} |")
    lines += [
        "",
        "## Visual risks",
        "",
        "- 390px에서 h2 번호 pill 줄바꿈 금지",
        "- rail 텍스트 좌측 접착 금지",
        "- footer 좌측 붙음 금지",
        "- 비정본 클래스 `template-card-head`/`source-preserve-static` 금지",
        "",
        "## Stop condition",
        "",
        "validate/quality/completion/render-audit 중 하나라도 실패하면 다음 모드로 넘어가지 않는다.",
    ]
    return "\n".join(lines) + "\n"


def build_index(rows: list[dict], version: str) -> str:
    text = (EXAMPLES / "index.html").read_text(encoding="utf-8")
    text = text.replace("Adaptive HTML Final · 16모드 예제 갤러리", "Adaptive HTML Final · 17모드 독립 벤치마크")
    text = text.replace("Adaptive HTML Final · 17모드 예제 갤러리", "Adaptive HTML Final · 17모드 독립 벤치마크")
    text = re.sub(
        r"<h1>.*?</h1>",
        "<h1>Adaptive HTML Final · 17모드 독립 벤치마크</h1>",
        text,
        count=1,
        flags=re.S,
    )
    text = re.sub(
        r"(<meta\\s+name=\"description\"\\s+content=\")[^\"]*(\">)",
        lambda m: m.group(1) + f"adaptive-html-final {version} 17개 모드 독립 신규 주제 벤치마크" + m.group(2),
        text,
    )
    for row in rows:
        text = text.replace(f'href="{row["source_file"]}"', f'href="{row["file"]}"')
        text = text.replace(row["source_title"], row["topic"])
    return text


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "pages").mkdir(parents=True)
    (OUT / "sources" / "modes").mkdir(parents=True)
    shutil.copytree(EXAMPLES / "assets", OUT / "assets")
    for dirname in ("workflow-svgs", "shape-svgs"):
        src_dir = SKILL / "assets" / dirname
        if src_dir.exists():
            shutil.copytree(src_dir, OUT / "assets" / dirname)
    shutil.copytree(EXAMPLES / "sources" / "assets", OUT / "sources" / "assets")
    for name in ["css-integrity.json", "profile.json", "adaptive-html-final-manifest.json"]:
        shutil.copy2(EXAMPLES / "sources" / name, OUT / "sources" / name)
    (OUT / "sources" / "profile.json").write_text(json.dumps({"profile":"auto"}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    shutil.copy2(SKILL / "manifest.json", OUT / "sources" / "adaptive-html-final-manifest.json")

    manifest = json.loads((SKILL / "manifest.json").read_text(encoding="utf-8"))
    version = manifest["version"]
    modes = load_modes()
    rows = []
    for no, mode in enumerate(modes, 1):
        mode_id = mode["id"]
        topic, sections = TOPICS[mode_id]
        ex_rel = mode["examples"][0]["file"]
        src = SKILL / ex_rel
        original = src.read_text(encoding="utf-8")
        original_h1 = re.search(r"<h1[^>]*>(.*?)</h1>", original, flags=re.S)
        source_title = re.sub(r"<.*?>", "", original_h1.group(1)).strip() if original_h1 else src.stem
        page_stem = f"{no:02d}_{slug(mode_id)}"
        page_rel = f"pages/{page_stem}.html"
        dst = OUT / page_rel
        title = f"{topic}"
        desc = f"adaptive-html-final {version} {mode_id} 독립 벤치마크 — {topic}"
        text = original
        text = update_head(text, title, desc)
        text = update_h1(text, title)
        text = replace_h2s(text, sections)
        text = replace_h2_subs(text, mode_id, topic, sections)
        text = replace_paragraphs(text, topic)
        text = add_build_note(text, mode_id, topic, sections)
        text = text.replace('href="assets/', 'href="../assets/').replace('src="assets/', 'src="../assets/')
        dst.write_text(text, encoding="utf-8")

        mode_dir = OUT / "sources" / "modes" / page_stem
        mode_dir.mkdir(parents=True)
        ev = evidence_for(mode, page_rel, topic, sections)
        (mode_dir / "build-evidence.json").write_text(json.dumps(ev, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
        (mode_dir / "mode-build-sheet.md").write_text(build_sheet(mode, topic, sections, page_rel), encoding="utf-8")
        rows.append({
            "no": no,
            "mode": mode_id,
            "topic": topic,
            "file": page_rel,
            "evidence": f"sources/modes/{page_stem}/build-evidence.json",
            "build_sheet": f"sources/modes/{page_stem}/mode-build-sheet.md",
            "sections": len(sections),
            "source_file": Path(ex_rel).name,
            "source_title": source_title,
        })

    top_ev = {
        "mode": "independent_17_mode_benchmark",
        "topic": "17 official modes with separate new topics",
        "profile": "auto",
        "layout": "multi-page-index",
        "primary_vt": "mixed",
        "section_mapping": {str(r["no"]): f"{r['mode']} -> {r['topic']}" for r in rows},
        "files": [{"path": r, "sha256": sha(ROOT / r)} for r in [
            "AGENTS.md",
            "skills/adaptive-html-final/SKILL.md",
            "skills/adaptive-html-final/manifest.json",
            "docs/adaptive-html-final-17-mode-sequential-runbook.md",
            "scripts/generate_independent_17_benchmark.py",
        ] if (ROOT / r).exists()],
    }
    (OUT / "sources" / "build-evidence.json").write_text(json.dumps(top_ev, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    benchmark = {
        "kind": "adaptive-html-final-17-mode-independent-benchmark",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "skill_version": version,
        "profile": "auto",
        "mode_count": 17,
        "pages": rows,
    }
    (OUT / "sources" / "benchmark-manifest.json").write_text(json.dumps(benchmark, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    (OUT / "index.html").write_text(build_index(rows, version), encoding="utf-8")
    print(OUT)

if __name__ == "__main__":
    main()
