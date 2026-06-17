# 17모드 독립(fresh) 데모 생성 프롬프트

> 목적: `adaptive-html-final` 17개 모드 각각을 **서로 영향 없이 완전히 독립**으로 데모 1개씩 생성한다.
> 실행: **모드당 1개의 격리 서브에이전트**(컨텍스트 독립). 한 모드가 끝나면 다음 모드를 fresh 컨텍스트로 시작 — 17회 반복.
> 버전 규율: 현재 정본 **v5.10.5 유지**(코어 해시 `a73eb204`), 버전 표면/CHANGELOG는 건드리지 않음. 산출물은 `output/`에만.

---

## A. 각 서브에이전트가 받는 작업 프롬프트 (복붙용 — {MODE}/{TOPIC}/{LAYOUT}/{REF}/{VT1}/{WG1}/{NN}/{SLUG} 치환)

```
너는 adaptive-html-final 스킬로 단일 모드 데모 HTML 1개를 "완전히 새롭게(fresh)" 생성한다.
다른 모드/이전 대화/기존 예제 본문을 콘텐츠 소스로 재사용하지 마라(스킬의 Fresh Extension Rule).
스킬 정본 자산(SKILL.md·layout·vt/wg 템플릿·core CSS)은 읽어서 사용한다 — 이건 재사용이 아니라 스킬 사용이다.

[대상]
- 모드: {MODE}   레이아웃: assets/layouts/{LAYOUT}
- 주제(새 소재): {TOPIC}
- 1순위 vt: {VT1}   1순위 wg: {WG1}
- 구조 참조 예제(읽기 전용, 본문 복붙 금지): skills/adaptive-html-final/examples/{REF}
- 출력 폴더: output/2026-06-15/demo17/{NN}_{MODE}_{SLUG}/

[절차]
1. skills/adaptive-html-final/SKILL.md 의 §0.6 결정표에서 {MODE} 행, §4 해당 모드 필수 블록·정량 하한을 읽는다.
   assets/layouts/{LAYOUT} 정보 구조와 {REF} 의 본문 구조(클래스 어휘·body-icon 사용·toc-map·h2-sub)를 읽어 기준선으로 삼는다.
2. 셸 재사용: {REF} 의 <head>+<style>(인라인 코어/조건부 CSS, 코어 해시 마커 a73eb204)+테마바+skip+reading-progress 를 byte 그대로 쓰고,
   <main>...</main> 안과 <title>/meta description 만 {TOPIC} 의 새 본문으로 교체한다. CSS는 절대 새로 작성/주입하지 않는다(커스텀 CSS 0).
3. 본문 작성 규칙(스킬 계약):
   - <main id="main" class="page-wide layout-...">, h1 1개, kicker→h1→sub→generated-row→meta 헤더.
   - 직접 h2 섹션 ≥10개. 각 직접 섹션 h2는 body-icon(assets/body-icons.json 의 40×40 SVG 원문, 의미별로 다양하게) + 필요 시 .num + 제목.
   - 4섹션+ 콘텐츠는 공식 toc-map 계약(toc-map+toc-pills+a.toc-pill>b). 주요 h2에 <p class="h2-sub">.
   - 모드 1순위 vt({VT1}) 최소 1회 본문 삽입(diagram/auto). 적합하면 1순위 wg({WG1}) 1개.
   - 모드별 필수 블록·정량 하한(SKILL §4) 충족. 코드가 필요하면 <pre class="code">(HTML escape). 표는 .tbl.table-scroll.mobile-card-table.
   - 결론은 예제 설명이 아니라 그 주제의 실제 판단/권고. "예제/placeholder/기준 1/2/3" 문구 금지.
4. 출력 폴더 구성:
   - index.html (위 산출물)
   - assets/favicon.png  ← skills/adaptive-html-final/examples/assets/favicon.png 복사
   - sources/  ← examples/sources 에서 css-integrity.json·adaptive-html-final-manifest.json·assets/*.css 복사
   - sources/profile.json = {"profile":"auto"}
   - sources/fresh-generation-rule.json = {"fresh_run":true,"reused_previous_pages":false,"mode_scope":["{MODE}"],"topic":"{TOPIC}"}
5. 게이트(통과까지 수정):
   - python3 skills/adaptive-html-final/scripts/validate_output.py <out> --skill-dir skills/adaptive-html-final  → issues 0
   - python3 skills/adaptive-html-final/scripts/quality_contract_check.py <out>  → OK
6. 렌더 증빙: NODE_PATH=$PWD/node_modules 로 Playwright 1280/390 캡처 → sources/screenshots/{1280,390}.png,
   sources/render-audit.json(viewports 1280/390 overflow_ok=true), sources/build-evidence.json(mode/profile/layout/primary_vt/section_mapping + 사용한 스킬 파일 ≥5개 path+sha256).
   python3 skills/adaptive-html-final/scripts/completion_check.py <out>  → 4/4 OK
7. 보고: 출력 경로, 모드/레이아웃, 직접 섹션 수, 사용 vt/wg, 게이트 결과(validate/quality/completion), 1280/390 overflow 결과.

[하드 규칙] 외부/동작 JS 0(JSON-LD만) · 커스텀 CSS 0(스킬 셸 그대로) · 코어 해시 a73eb204 유지 · 버전 라벨 v5.10.5 · output/ 밖 수정 금지 · 스킬 파일/예제 수정 금지.
```

## B. 17모드 → 주제 배정표 (기존 examples와 겹치지 않는 새 소재)

| NN | mode | layout | 참조예제(REF) | 1순위 vt | 1순위 wg | 주제(TOPIC) | slug |
|----|------|--------|----------------|----------|----------|-------------|------|
| 01 | skill_audit | skill-audit-report.html | 08_skill_audit_codereview_bot.html | quality-gate | wg-03 | "회의록 자동 요약 봇" SKILL.md 감사·개선 | meeting-summary-bot-audit |
| 02 | platform_blog | platform-adaptation.html | 07_platform_tech_retro_adaptation.html | card-grid | wg-02 | 신규 오픈소스 릴리스 글을 4개 플랫폼으로 변환 | oss-release-platforms |
| 03 | seo_dashboard | seo-dashboard.html | 06_seo_prompt_engineering_dashboard.html | card-grid | wg-11 | "벡터 데이터베이스 입문" 글 SEO 설계 | vector-db-seo |
| 04 | education_html | course-module.html | 04_education_git_rebase_workshop.html | timeline | wg-06 | Kubernetes 입문 3일 워크숍(Pod→Deployment→Service) | k8s-intro-workshop |
| 05 | github_analysis | github-analysis.html | 14_github_analysis_fastapi_starter.html | hero-map | wg-11 | github.com/tiangolo/sqlmodel 저장소 실사 | sqlmodel-due-diligence |
| 06 | github_feature_usage | github-feature-usage.html | 17_github_feature_usage_coreline_auth.html | hero-map | wg-14 | Caddy 웹서버 기능·도입 가이드 | caddy-feature-usage |
| 07 | youtube_analysis | youtube-analysis.html | 15_youtube_vibecoding_gap.html | timeline | wg-11 | "분산 시스템 설계 기초" 강연 영상 분석 | distsys-talk-analysis |
| 08 | manual_analysis | manual-analysis.html | 16_manual_product_runbook.html | hero-map | wg-04 | Nginx 리버스 프록시 운영 매뉴얼 | nginx-reverse-proxy-manual |
| 09 | expert_html | expert-report.html | 02_expert_llm_gateway_report.html | risk-matrix | wg-16 | 단일 DB → 읽기 복제본 도입 타당성 진단 | read-replica-feasibility |
| 10 | article_html | magazine-article.html | 03_article_side_project_signal.html | decision-tree | wg-02 | 왜 모노레포로 가는가 — 코드 공유의 무게중심 | monorepo-argument |
| 11 | blog_writer | personal-blog-essay.html | 05_blog_deepwork_4day_retro.html | timeline | wg-17 | 사이드 프로젝트 12개 1년 회고 | side-project-12-retro |
| 12 | beginner_html | beginner-learning.html | 01_beginner_passkey_login.html | concept-explainer | wg-10 | OAuth 2.0 / OIDC 처음 이해하기 | oauth-oidc-beginner |
| 13 | reference_html | reference-manual.html | 09_reference_regex.html | file-tour | wg-04 | HTTP 상태 코드 실무 레퍼런스 | http-status-reference |
| 14 | comparison_html | comparison-matrix.html | 10_comparison_message_queue.html | comparison-cards | wg-01 | PostgreSQL vs MySQL vs SQLite 선택 기준 | rdbms-comparison |
| 15 | case_study_html | case-study.html | 11_case_study_search_index_outage.html | incident-summary | wg-12 | 결제 이중 청구 장애 사후 분석 | double-billing-postmortem |
| 16 | landing_brief_html | landing-brief.html | 12_landing_pagercalm_brief.html | hero-map | wg-02 | 팀 온콜 자동화 SaaS "OnCallZero" 소개 | oncallzero-landing |
| 17 | checklist_playbook | checklist-playbook.html | 13_checklist_data_migration.html | checklist-flow | wg-11 | 프로덕션 DB 인덱스 추가 안전 플레이북 | prod-index-playbook |

> 산출물 부모 폴더: `output/2026-06-15/demo17/`. 각 모드는 `{NN}_{MODE}_{SLUG}/index.html`.
> 주제는 제안값 — 마음에 안 드는 모드는 교체 가능.
