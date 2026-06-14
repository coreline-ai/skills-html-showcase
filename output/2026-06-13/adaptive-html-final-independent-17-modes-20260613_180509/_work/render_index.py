#!/usr/bin/env python3
"""Index — 17모드 독립 생성 링크 인덱스 (navigation shell, no layout- class).
quality_contract_check는 content 페이지가 있으면 index를 건너뛴다. validate_output만 통과하면 된다.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _finalize import build_page, write_sources  # noqa: E402

MODES = [
    ("01", "skill_audit", "회의록 → 릴리스 노트 자동 변환 스킬 감사", "pages/01_skill_audit_meeting_to_release_notes.html"),
    ("02", "platform_blog", "온콜 알림 정책 개편기 플랫폼별 변환", "pages/02_platform_blog_oncall_alert_policy.html"),
    ("03", "seo_dashboard", "사내 문서 검색 구축 SEO 대시보드", "pages/03_seo_dashboard_internal_doc_search.html"),
    ("04", "education_html", "Rust 소유권과 빌림 입문 4주 모듈", "pages/04_education_html_rust_ownership.html"),
    ("05", "github_analysis", "경량 작업 큐 라이브러리 도입 실사", "pages/05_github_analysis_taskq_due_diligence.html"),
    ("06", "github_feature_usage", "셀프호스트 업타임 모니터 도입 가이드", "pages/06_github_feature_usage_upkeep_monitor.html"),
    ("07", "youtube_analysis", "LLM 비용 70% 절감 토크 영상 분석", "pages/07_youtube_analysis_llm_cost_talk.html"),
    ("08", "manual_analysis", "사내 Kubernetes 운영 런북 재구성", "pages/08_manual_analysis_k8s_runbook.html"),
    ("09", "expert_html", "멀티리전 결제 시스템 아키텍처 진단", "pages/09_expert_html_multiregion_payments.html"),
    ("10", "article_html", "관측 가능성은 로그를 모으는 일이 아니다", "pages/10_article_html_observability.html"),
    ("11", "blog_writer", "사이드 프로젝트를 6개월 만에 접고 배운 것", "pages/11_blog_writer_side_project_retro.html"),
    ("12", "beginner_html", "HTTPS와 TLS 핸드셰이크 입문", "pages/12_beginner_html_https_tls_handshake.html"),
    ("13", "reference_html", "cron 표현식 & 스케줄링 레퍼런스", "pages/13_reference_html_cron_scheduling.html"),
    ("14", "comparison_html", "React 상태관리 비교 (RTK·Zustand·Jotai)", "pages/14_comparison_html_react_state.html"),
    ("15", "case_study_html", "정산 배치 8시간 지연 장애 사후 분석", "pages/15_case_study_html_settlement_batch_delay.html"),
    ("16", "landing_brief_html", "팀 지식베이스 SaaS 'Cortex' 랜딩 브리프", "pages/16_landing_brief_html_cortex.html"),
    ("17", "checklist_playbook", "프로덕션 DB 스키마 마이그레이션 플레이북", "pages/17_checklist_playbook_db_schema_migration.html"),
]

cards = "".join(
    f'<a class="mini-card" href="{href}"><span class="case-label">{no}</span><h3>{mode}</h3><p>{topic}</p></a>'
    for no, mode, topic, href in MODES
)

body = f'''
<main id="main" class="page-wide">
  <header class="header">
    <div class="kicker"><span class="kicker-text">adaptive-html-final · 17모드 독립 생성</span></div>
    <h1>17개 공식 모드 독립 HTML 인덱스</h1>
    <p class="sub">adaptive-html-final 스킬의 공식 17개 모드 각각을 서로 다른 자유 주제로, 모드별 독립 빌드로 생성한 결과 모음이다. 각 페이지는 본문 섹션 10개 이상, 8테마 스위처, 모드별 1순위 vt·권장 wg를 포함하며 정적 검증을 통과했다.</p>
    <div class="meta"><span>profile auto</span><span>17 / 17 모드</span><span>각 페이지 validate + quality OK</span><span>무 동작 JS</span></div>
  </header>
  <section class="summary-card">
    <h2>이 모음에 대하여</h2>
    <p class="h2-sub">모드마다 독립 컨텍스트처럼 새 빌드로 작성했고, 이전 모드의 본문을 다음 모드의 템플릿으로 재사용하지 않았다.</p>
    <p>각 모드는 §3 결정표의 layout·1순위 vt·권장 wg를 따른다. 본문은 카드·표·vt 다이어그램·wg 위젯·editorial 패턴·체크리스트를 정보 구조에 맞게 섞어, 같은 카드/리스트를 반복하지 않도록 구성했다. 모든 페이지는 8테마(라이트~세피아) 스위처와 toc-map 목차, 마지막 대비 섹션(.try)을 공유한다.</p>
  </section>
  <div class="card-grid">{cards}</div>
  <aside class="source-note"><p><strong>생성 정보.</strong> adaptive-html-final v5.10.3 · profile=auto · 17모드 독립 순차 생성. 각 페이지는 <code>validate_output.py</code>와 <code>quality_contract_check.py</code>를 통과했다. 본문의 주제·수치는 모드 설명을 위한 예시 시나리오이며 특정 실제 사건·제품을 단정하지 않는다.</p></aside>
</main>'''

out = build_page("index.html", title="adaptive-html-final 17모드 독립 생성 인덱스",
                 description="adaptive-html-final 스킬의 공식 17개 모드를 독립 주제로 모드별 독립 빌드한 결과 링크 인덱스.",
                 body=body)
write_sources()
print("WROTE", out)
