# adaptive-html-final examples v5.9.1 순차 업데이트 진행 로그

- 목표: manifest 기준 정본 examples 16개를 최신 `adaptive-html-final` 5.9.1 계약에 맞춰 1개 모드씩 순차 확인/업데이트한다.
- 원칙: 한 continuation/session에서 1개 모드만 처리한다.
- 정본 목록 기준: `skills/adaptive-html-final/manifest.json` `examples.files`
- 레거시 examples: manifest 밖 파일은 수정하지 않는다.
- output 폴더: 수정하지 않는다.

## 진행 상태

| 순서 | 모드 | 파일 | 상태 | vt/wg 계약 | 검증 |
|---:|---|---|---|---|---|
| 01 | `beginner_html` | `skills/adaptive-html-final/examples/01_beginner_passkey_login.html` | 완료 | vt `concept-explainer`, wg `wg-10` 포함 | 통과 |
| 02 | `expert_html` | `skills/adaptive-html-final/examples/02_expert_llm_gateway_report.html` | 완료 | vt `risk-matrix`, wg `wg-03` 포함 | 통과 |
| 03 | `article_html` | `skills/adaptive-html-final/examples/03_article_side_project_signal.html` | 완료 | vt `decision-tree`, wg `wg-02` 포함 | 통과 |
| 04 | `education_html` | `skills/adaptive-html-final/examples/04_education_git_rebase_workshop.html` | 완료 | vt `timeline`, wg `wg-06` 포함 | 통과 |
| 05 | `blog_writer` | `skills/adaptive-html-final/examples/05_blog_deepwork_4day_retro.html` | 완료 | vt `timeline`, wg `wg-17` 포함 | 통과 |
| 06 | `seo_dashboard` | `skills/adaptive-html-final/examples/06_seo_prompt_engineering_dashboard.html` | 완료 | vt `card-grid`, wg `wg-11` 포함 | 통과 |
| 07 | `platform_blog` | `skills/adaptive-html-final/examples/07_platform_tech_retro_adaptation.html` | 완료 | vt `card-grid`, wg `wg-02` 포함 | 통과 |
| 08 | `skill_audit` | `skills/adaptive-html-final/examples/08_skill_audit_codereview_bot.html` | 완료 | vt `quality-gate`, wg `wg-03` 포함 | 통과 |
| 09 | `reference_html` | `skills/adaptive-html-final/examples/09_reference_regex.html` | 완료 | vt `file-tour`, wg `wg-04` 포함 | 통과 |
| 10 | `comparison_html` | `skills/adaptive-html-final/examples/10_comparison_message_queue.html` | 완료 | vt `comparison-cards`, wg `wg-01` 포함 | 통과 |
| 11 | `case_study_html` | `skills/adaptive-html-final/examples/11_case_study_search_index_outage.html` | 완료 | vt `incident-summary`, wg `wg-12` 포함 | 통과 |
| 12 | `landing_brief_html` | `skills/adaptive-html-final/examples/12_landing_pagercalm_brief.html` | 완료 | vt `hero-map`, wg `wg-02` 포함 | 통과 |
| 13 | `checklist_playbook` | `skills/adaptive-html-final/examples/13_checklist_data_migration.html` | 완료 | vt `checklist-flow`, wg `wg-11` 포함 | 통과 |
| 14 | `github_analysis` | `skills/adaptive-html-final/examples/14_github_analysis_fastapi_starter.html` | 완료 | vt `hero-map`, wg `wg-11` 포함 | 통과 |
| 15 | `youtube_analysis` | `skills/adaptive-html-final/examples/15_youtube_vibecoding_gap.html` | 완료 | vt `timeline`, wg `wg-11` 포함 | 통과 |
| 16 | `manual_analysis` | `skills/adaptive-html-final/examples/16_manual_product_runbook.html` | 완료 | vt `hero-map`, wg `wg-13` 포함 | 통과 |

## 01 beginner_html 처리 기록

- 처리 시각: 2026-06-08 KST
- 대상 파일: `skills/adaptive-html-final/examples/01_beginner_passkey_login.html`
- 대상 layout: `skills/adaptive-html-final/assets/layouts/beginner-learning.html`
- 최신 manifest: `5.9.1`
- 판정: 이미 최신 5.9.1 계약을 만족해 example 본문 수정 없음.
- 확인한 계약:
  - `profile auto`
  - 8테마 스위처 `name="ahf-theme"` / `.ahf-themebar` 존재
  - core CSS hash marker 존재
  - `body-icon` 존재
  - `h1` 1개
  - vt 계약: `concept-explainer` 구조 포함
  - wg 계약: 권장 위젯 `wg-10` 포함
  - 추가 위젯: `wg-13`, `wg-15`도 인라인 CSS/마크업 포함

검증 임시 폴더:

```text
/tmp/ahf-canonical-16-TSGm4h
```

검증 결과:

```text
python3 skills/adaptive-html-final/scripts/validate_output.py /tmp/ahf-canonical-16-TSGm4h --skill-dir skills/adaptive-html-final
HTML files: 17
OK

python3 skills/adaptive-html-final/scripts/quality_contract_check.py /tmp/ahf-canonical-16-TSGm4h
OK — quality contract guard passed (16 HTML content file(s))

python3 skills/adaptive-html-final/tests/test_governance_gates.py
77/77 checks passed
```

## 02 expert_html 처리 기록

- 처리 시각: 2026-06-08 KST
- 대상 파일: `skills/adaptive-html-final/examples/02_expert_llm_gateway_report.html`
- 대상 layout: `skills/adaptive-html-final/assets/layouts/expert-report.html`
- 최신 manifest: `5.9.1`
- 판정: 이미 최신 5.9.1 계약을 만족해 example 본문 수정 없음.
- 확인한 계약:
  - `profile auto`
  - 8테마 스위처 `name="ahf-theme"` / `.ahf-themebar` 존재
  - core CSS hash marker 존재
  - `layout-expert` 존재
  - `body-icon` 존재
  - `h1` 1개
  - vt 계약: `risk-matrix` 구조 포함
  - wg 계약: 권장 위젯 `wg-03` 포함
  - 추가 위젯: `wg-04`, `wg-11`, `wg-12`, `wg-16`, `wg-17`도 인라인 CSS/마크업 포함
  - expert 전용 회귀: `validation-checklist`에 `wg-03`/`wg-17` 오염 없음

검증 임시 폴더:

```text
/tmp/ahf-canonical-16-nWiGlq
```

검증 결과:

```text
python3 skills/adaptive-html-final/scripts/validate_output.py /tmp/ahf-canonical-16-nWiGlq --skill-dir skills/adaptive-html-final
HTML files: 17
OK

python3 skills/adaptive-html-final/scripts/quality_contract_check.py /tmp/ahf-canonical-16-nWiGlq
OK — quality contract guard passed (16 HTML content file(s))

python3 skills/adaptive-html-final/tests/test_governance_gates.py
77/77 checks passed
```

다음 continuation/session 대상:

```text
03 article_html
skills/adaptive-html-final/examples/03_article_side_project_signal.html
```

## 03 article_html 처리 기록

- 처리 시각: 2026-06-08 KST
- 대상 파일: `skills/adaptive-html-final/examples/03_article_side_project_signal.html`
- 대상 layout: `skills/adaptive-html-final/assets/layouts/magazine-article.html`
- 최신 manifest: `5.9.1`
- 판정: 이미 최신 5.9.1 계약을 만족해 example 본문 수정 없음.
- 확인한 계약:
  - `profile auto`
  - 8테마 스위처 `name="ahf-theme"` / `.ahf-themebar` 존재
  - core CSS hash marker 존재
  - `layout-article` 존재
  - `body-icon` 존재
  - `h1` 1개
  - vt 계약: `decision-tree` 구조 포함
  - wg 계약: 권장 위젯 `wg-02` 포함
  - 추가 위젯: `wg-04`, `wg-07`, `wg-09`, `wg-10`, `wg-13`, `wg-14`도 인라인 CSS/마크업 포함
  - legacy `#theme-toggle`, `draggable`, `contenteditable`, 동작 `<script>` 없음

검증 임시 폴더:

```text
/tmp/ahf-canonical-16-0lBf0S
```

검증 결과:

```text
python3 skills/adaptive-html-final/scripts/validate_output.py /tmp/ahf-canonical-16-0lBf0S --skill-dir skills/adaptive-html-final
HTML files: 17
OK

python3 skills/adaptive-html-final/scripts/quality_contract_check.py /tmp/ahf-canonical-16-0lBf0S
OK — quality contract guard passed (16 HTML content file(s))

python3 skills/adaptive-html-final/tests/test_governance_gates.py
77/77 checks passed
```

다음 continuation/session 대상:

```text
04 education_html
skills/adaptive-html-final/examples/04_education_git_rebase_workshop.html
```

## 04 education_html 처리 기록

- 처리 시각: 2026-06-08 KST
- 대상 파일: `skills/adaptive-html-final/examples/04_education_git_rebase_workshop.html`
- 대상 layout: `skills/adaptive-html-final/assets/layouts/course-module.html`
- 최신 manifest: `5.9.1`
- 판정: 이미 최신 5.9.1 계약을 만족해 example 본문 수정 없음.
- 확인한 계약:
  - `profile auto`
  - 8테마 스위처 `name="ahf-theme"` / `.ahf-themebar` 존재
  - core CSS hash marker 존재
  - `layout-education` 존재
  - `body-icon` 존재
  - `h1` 1개
  - vt 계약: `timeline` 구조 포함
  - wg 계약: 권장 위젯 `wg-06` 포함
  - 추가 위젯: `wg-07`, `wg-08`, `wg-13`, `wg-14`, `wg-15`, `wg-20`도 인라인 CSS/마크업 포함
  - legacy `#theme-toggle`, `draggable`, `contenteditable`, 동작 `<script>` 없음

검증 임시 폴더:

```text
/tmp/ahf-canonical-16-Mn0M0N
```

검증 결과:

```text
python3 skills/adaptive-html-final/scripts/validate_output.py /tmp/ahf-canonical-16-Mn0M0N --skill-dir skills/adaptive-html-final
HTML files: 17
OK

python3 skills/adaptive-html-final/scripts/quality_contract_check.py /tmp/ahf-canonical-16-Mn0M0N
OK — quality contract guard passed (16 HTML content file(s))

python3 skills/adaptive-html-final/tests/test_governance_gates.py
77/77 checks passed
```

다음 continuation/session 대상:

```text
05 blog_writer
skills/adaptive-html-final/examples/05_blog_deepwork_4day_retro.html
```

## 05 blog_writer 처리 기록

- 처리 시각: 2026-06-08 KST
- 대상 파일: `skills/adaptive-html-final/examples/05_blog_deepwork_4day_retro.html`
- 대상 layout: `skills/adaptive-html-final/assets/layouts/personal-blog-essay.html`
- 최신 manifest: `5.9.1`
- 판정: 이미 최신 5.9.1 계약을 만족해 example 본문 수정 없음.
- 확인한 계약:
  - `profile auto`
  - 8테마 스위처 `name="ahf-theme"` / `.ahf-themebar` 존재
  - core CSS hash marker 존재
  - `layout-blog` 존재
  - `body-icon` 존재
  - `h1` 1개
  - blog 본문 직접 섹션 h2 6개 모두 `body-icon`과 번호 진행 표시 포함
  - vt 계약: `timeline` 구조(`.vt-shell` + `.tl-item`) 포함
  - wg 계약: 추천 위젯 `wg-17` 포함
  - legacy `#theme-toggle`, `draggable`, `contenteditable`, 동작 `<script>` 없음

검증 임시 폴더:

```text
/tmp/ahf-canonical-16-jiuYJx
```

검증 결과:

```text
python3 skills/adaptive-html-final/scripts/validate_output.py /tmp/ahf-canonical-16-jiuYJx --skill-dir skills/adaptive-html-final
HTML files: 17
OK

python3 skills/adaptive-html-final/scripts/quality_contract_check.py /tmp/ahf-canonical-16-jiuYJx
OK — quality contract guard passed (16 HTML content file(s))

python3 skills/adaptive-html-final/tests/test_governance_gates.py
77/77 checks passed
```

다음 continuation/session 대상:

```text
06 seo_dashboard
skills/adaptive-html-final/examples/06_seo_prompt_engineering_dashboard.html
```

## 06 seo_dashboard 처리 기록

- 처리 시각: 2026-06-08 KST
- 대상 파일: `skills/adaptive-html-final/examples/06_seo_prompt_engineering_dashboard.html`
- 대상 layout: `skills/adaptive-html-final/assets/layouts/seo-dashboard.html`
- 최신 manifest: `5.9.1`
- 판정: 이미 최신 5.9.1 계약을 만족해 example 본문 수정 없음.
- 확인한 계약:
  - `profile auto`
  - 8테마 스위처 `name="ahf-theme"` / `.ahf-themebar` 존재
  - core CSS hash marker 존재
  - `layout-seo` 존재
  - `body-icon` 존재
  - `h1` 1개
  - SEO 본문 섹션 h2 모두 `body-icon` 포함
  - vt 계약: `card-grid` 구조(`.vt-shell` + `.cg-grid`) 포함
  - wg 계약: 추천 위젯 `wg-11` 포함
  - `sources/profile.json`은 `auto`, source manifest 버전은 `5.9.1`
  - legacy `#theme-toggle`, `draggable`, `contenteditable`, 동작 `<script>` 없음

검증 임시 폴더:

```text
/tmp/ahf-canonical-16-6561oR
```

검증 결과:

```text
python3 skills/adaptive-html-final/scripts/validate_output.py /tmp/ahf-canonical-16-6561oR --skill-dir skills/adaptive-html-final
HTML files: 17
OK

python3 skills/adaptive-html-final/scripts/quality_contract_check.py /tmp/ahf-canonical-16-6561oR
OK — quality contract guard passed (16 HTML content file(s))

python3 skills/adaptive-html-final/tests/test_governance_gates.py
77/77 checks passed
```

다음 continuation/session 대상:

```text
07 platform_blog
skills/adaptive-html-final/examples/07_platform_tech_retro_adaptation.html
```

## 07 platform_blog 처리 기록

- 처리 시각: 2026-06-08 KST
- 대상 파일: `skills/adaptive-html-final/examples/07_platform_tech_retro_adaptation.html`
- 대상 layout: `skills/adaptive-html-final/assets/layouts/platform-adaptation.html`
- 최신 manifest: `5.9.1`
- 판정: 이미 최신 5.9.1 계약을 만족해 example 본문 수정 없음.
- 확인한 계약:
  - `profile auto`
  - 8테마 스위처 `name="ahf-theme"` / `.ahf-themebar` 존재
  - core CSS hash marker 존재
  - `layout-platform` 존재
  - `body-icon` 존재
  - `h1` 1개
  - 플랫폼 본문 섹션 h2 모두 `body-icon` 포함
  - vt 계약: `card-grid` 구조(`.vt-shell` + `.cg-grid`) 포함
  - wg 계약: 추천 위젯 `wg-02` 포함
  - `sources/profile.json`은 `auto`, source manifest 버전은 `5.9.1`
  - legacy `#theme-toggle`, `draggable`, `contenteditable`, 동작 `<script>` 없음

검증 임시 폴더:

```text
/tmp/ahf-canonical-16-W1l989
```

검증 결과:

```text
python3 skills/adaptive-html-final/scripts/validate_output.py /tmp/ahf-canonical-16-W1l989 --skill-dir skills/adaptive-html-final
HTML files: 17
OK

python3 skills/adaptive-html-final/scripts/quality_contract_check.py /tmp/ahf-canonical-16-W1l989
OK — quality contract guard passed (16 HTML content file(s))

python3 skills/adaptive-html-final/tests/test_governance_gates.py
77/77 checks passed
```

다음 continuation/session 대상:

```text
08 skill_audit
skills/adaptive-html-final/examples/08_skill_audit_codereview_bot.html
```

## 08 skill_audit 처리 기록

- 처리 시각: 2026-06-08 KST
- 대상 파일: `skills/adaptive-html-final/examples/08_skill_audit_codereview_bot.html`
- 대상 layout: `skills/adaptive-html-final/assets/layouts/skill-audit-report.html`
- 최신 manifest: `5.9.1`
- 판정: 이미 최신 5.9.1 계약을 만족해 example 본문 수정 없음.
- 확인한 계약:
  - `profile auto`
  - 8테마 스위처 `name="ahf-theme"` / `.ahf-themebar` 존재
  - core CSS hash marker 존재
  - `layout-audit` 존재
  - `body-icon` 존재
  - `h1` 1개
  - 감사 본문 섹션 h2 모두 `body-icon` 포함
  - vt 계약: `quality-gate` 구조(`.vt-shell` + `.qg-grid`) 포함
  - wg 계약: 추천 위젯 `wg-03` 포함
  - `sources/profile.json`은 `auto`, source manifest 버전은 `5.9.1`
  - legacy `#theme-toggle`, `draggable`, `contenteditable`, 동작 `<script>` 없음

검증 임시 폴더:

```text
/tmp/ahf-canonical-16-EmFEna
```

검증 결과:

```text
python3 skills/adaptive-html-final/scripts/validate_output.py /tmp/ahf-canonical-16-EmFEna --skill-dir skills/adaptive-html-final
HTML files: 17
OK

python3 skills/adaptive-html-final/scripts/quality_contract_check.py /tmp/ahf-canonical-16-EmFEna
OK — quality contract guard passed (16 HTML content file(s))

python3 skills/adaptive-html-final/tests/test_governance_gates.py
77/77 checks passed
```

다음 continuation/session 대상:

```text
09 reference_html
skills/adaptive-html-final/examples/09_reference_regex.html
```

## 09 reference_html 처리 기록

- 처리 시각: 2026-06-08 KST
- 대상 파일: `skills/adaptive-html-final/examples/09_reference_regex.html`
- 대상 layout: `skills/adaptive-html-final/assets/layouts/reference-manual.html`
- 최신 manifest: `5.9.1`
- 판정: 이미 최신 5.9.1 계약을 만족해 example 본문 수정 없음.
- 확인한 계약:
  - `profile auto`
  - 8테마 스위처 `name="ahf-theme"` / `.ahf-themebar` 존재
  - core CSS hash marker 존재
  - `layout-reference` 존재
  - `body-icon` 존재
  - `h1` 1개
  - 레퍼런스 본문 섹션 h2 모두 `body-icon` 포함
  - 표 `caption` 존재
  - vt 계약: `file-tour` 구조(`.vt-shell` + `.ft-card`) 포함
  - wg 계약: 추천 위젯 `wg-04` 포함
  - `sources/profile.json`은 `auto`, source manifest 버전은 `5.9.1`
  - legacy `#theme-toggle`, `draggable`, `contenteditable`, 동작 `<script>` 없음

검증 임시 폴더:

```text
/tmp/ahf-canonical-16-sVc0uK
```

검증 결과:

```text
python3 skills/adaptive-html-final/scripts/validate_output.py /tmp/ahf-canonical-16-sVc0uK --skill-dir skills/adaptive-html-final
HTML files: 17
OK

python3 skills/adaptive-html-final/scripts/quality_contract_check.py /tmp/ahf-canonical-16-sVc0uK
OK — quality contract guard passed (16 HTML content file(s))

python3 skills/adaptive-html-final/tests/test_governance_gates.py
77/77 checks passed
```

다음 continuation/session 대상:

```text
10 comparison_html
skills/adaptive-html-final/examples/10_comparison_message_queue.html
```

## 10 comparison_html 처리 기록

- 처리 시각: 2026-06-08 KST
- 대상 파일: `skills/adaptive-html-final/examples/10_comparison_message_queue.html`
- 대상 layout: `skills/adaptive-html-final/assets/layouts/comparison-matrix.html`
- 최신 manifest: `5.9.1`
- 판정: 이미 최신 5.9.1 계약을 만족해 example 본문 수정 없음.
- 확인한 계약:
  - `profile auto`
  - 8테마 스위처 `name="ahf-theme"` / `.ahf-themebar` 존재
  - core CSS hash marker 존재
  - `layout-compare` 존재
  - `body-icon` 존재
  - `h1` 1개
  - 비교 본문 섹션 h2 모두 `body-icon` 포함
  - 표 `caption` 존재
  - vt 계약: `comparison-cards` 구조(`.vt-shell` + `.cmp-card`) 포함
  - wg 계약: 추천 위젯 `wg-01` 포함
  - `sources/profile.json`은 `auto`, source manifest 버전은 `5.9.1`
  - legacy `#theme-toggle`, `draggable`, `contenteditable`, 동작 `<script>` 없음

검증 임시 폴더:

```text
/tmp/ahf-canonical-16-gAGThH
```

검증 결과:

```text
python3 skills/adaptive-html-final/scripts/validate_output.py /tmp/ahf-canonical-16-gAGThH --skill-dir skills/adaptive-html-final
HTML files: 17
OK

python3 skills/adaptive-html-final/scripts/quality_contract_check.py /tmp/ahf-canonical-16-gAGThH
OK — quality contract guard passed (16 HTML content file(s))

python3 skills/adaptive-html-final/tests/test_governance_gates.py
77/77 checks passed
```

다음 continuation/session 대상:

```text
11 case_study_html
skills/adaptive-html-final/examples/11_case_study_search_index_outage.html
```

## 11 case_study_html 처리 기록

- 처리 시각: 2026-06-08 KST
- 대상 파일: `skills/adaptive-html-final/examples/11_case_study_search_index_outage.html`
- 대상 layout: `skills/adaptive-html-final/assets/layouts/case-study.html`
- 최신 manifest: `5.9.1`
- 판정: 이미 최신 5.9.1 계약을 만족해 example 본문 수정 없음.
- 확인한 계약:
  - `profile auto`
  - 8테마 스위처 `name="ahf-theme"` / `.ahf-themebar` 존재
  - core CSS hash marker 존재
  - `layout-case` 존재
  - `body-icon` 존재
  - `h1` 1개
  - case study 본문 섹션 h2 모두 `body-icon` 포함
  - 표 `caption` 존재
  - vt 계약: `incident-summary` 구조(`.vt-shell` + `.inc-head` + `.inc-card`) 포함
  - wg 계약: 추천 위젯 `wg-12` 포함
  - case timeline 회귀 확인: `.layout-case .timeline{border-left:0}`, `.layout-case .timeline-card{border-left:0}`, 개별 `li::before` 번호 카드 존재
  - `sources/profile.json`은 `auto`, source manifest 버전은 `5.9.1`
  - legacy `#theme-toggle`, `draggable`, `contenteditable`, 동작 `<script>` 없음

검증 임시 폴더:

```text
/tmp/ahf-canonical-16-f2B19w
```

검증 결과:

```text
python3 skills/adaptive-html-final/scripts/validate_output.py /tmp/ahf-canonical-16-f2B19w --skill-dir skills/adaptive-html-final
HTML files: 17
OK

python3 skills/adaptive-html-final/scripts/quality_contract_check.py /tmp/ahf-canonical-16-f2B19w
OK — quality contract guard passed (16 HTML content file(s))

python3 skills/adaptive-html-final/tests/test_governance_gates.py
77/77 checks passed
```

다음 continuation/session 대상:

```text
12 landing_brief_html
skills/adaptive-html-final/examples/12_landing_pagercalm_brief.html
```

## 12 landing_brief_html 처리 기록

- 처리 시각: 2026-06-08 KST
- 대상 파일: `skills/adaptive-html-final/examples/12_landing_pagercalm_brief.html`
- 대상 layout: `skills/adaptive-html-final/assets/layouts/landing-brief.html`
- 최신 manifest: `5.9.1`
- 판정: 이미 최신 5.9.1 계약을 만족해 example 본문 수정 없음.
- 확인한 계약:
  - `profile auto`
  - 8테마 스위처 `name="ahf-theme"` / `.ahf-themebar` 존재
  - core CSS hash marker 존재
  - `layout-landing` 존재
  - `body-icon` 존재
  - `h1` 1개
  - landing 본문 섹션 h2 모두 `body-icon` 포함
  - 표 `caption` 존재
  - vt 계약: `hero-map` 구조(`.vt-shell` + `.hm-grid`) 포함
  - wg 계약: 추천 위젯 `wg-02` 포함
  - 현재 12번 정본 본문에는 `wg-16` 마크업 없음(스타일 번들만 공통 포함)
  - `sources/profile.json`은 `auto`, source manifest 버전은 `5.9.1`
  - legacy `#theme-toggle`, `draggable`, `contenteditable`, 동작 `<script>` 없음

검증 임시 폴더:

```text
/tmp/ahf-canonical-16-wkjdm2
```

검증 결과:

```text
python3 skills/adaptive-html-final/scripts/validate_output.py /tmp/ahf-canonical-16-wkjdm2 --skill-dir skills/adaptive-html-final
HTML files: 17
OK

python3 skills/adaptive-html-final/scripts/quality_contract_check.py /tmp/ahf-canonical-16-wkjdm2
OK — quality contract guard passed (16 HTML content file(s))

python3 skills/adaptive-html-final/tests/test_governance_gates.py
77/77 checks passed
```

다음 continuation/session 대상:

```text
13 checklist_playbook
skills/adaptive-html-final/examples/13_checklist_data_migration.html
```

## 13 checklist_playbook 처리 기록

- 처리 시각: 2026-06-08 KST
- 대상 파일: `skills/adaptive-html-final/examples/13_checklist_data_migration.html`
- 대상 layout: `skills/adaptive-html-final/assets/layouts/checklist-playbook.html`
- 최신 manifest: `5.9.1`
- 판정: 이미 최신 5.9.1 계약을 만족해 example 본문 수정 없음.
- 확인한 계약:
  - `profile auto`
  - 8테마 스위처 `name="ahf-theme"` / `.ahf-themebar` 존재
  - core CSS hash marker 존재
  - `layout-checklist` 존재
  - `body-icon` 존재
  - `h1` 1개
  - checklist 본문 섹션 h2 모두 `body-icon` 포함
  - 표 `caption` 존재
  - vt 계약: `checklist-flow` 구조(`.vt-shell` + `.cf-item`) 포함
  - wg 계약: 추천 위젯 `wg-11` 포함
  - 현재 13번 정본 본문에는 `wg-16` 마크업 없음(스타일 번들만 공통 포함)
  - `sources/profile.json`은 `auto`, source manifest 버전은 `5.9.1`
  - legacy `#theme-toggle`, `draggable`, `contenteditable`, 동작 `<script>` 없음

검증 임시 폴더:

```text
/tmp/ahf-canonical-16-8JlOvD
```

검증 결과:

```text
python3 skills/adaptive-html-final/scripts/validate_output.py /tmp/ahf-canonical-16-8JlOvD --skill-dir skills/adaptive-html-final
HTML files: 17
OK

python3 skills/adaptive-html-final/scripts/quality_contract_check.py /tmp/ahf-canonical-16-8JlOvD
OK — quality contract guard passed (16 HTML content file(s))

python3 skills/adaptive-html-final/tests/test_governance_gates.py
77/77 checks passed
```

다음 continuation/session 대상:

```text
14 github_analysis
skills/adaptive-html-final/examples/14_github_analysis_fastapi_starter.html
```

## 14 github_analysis 처리 기록

- 처리 시각: 2026-06-08 KST
- 대상 파일: `skills/adaptive-html-final/examples/14_github_analysis_fastapi_starter.html`
- 대상 layout: `skills/adaptive-html-final/assets/layouts/github-analysis.html`
- 최신 manifest: `5.9.1`
- 판정: 이미 최신 5.9.1 계약을 만족해 example 본문 수정 없음.
- 확인한 계약:
  - `profile auto`
  - 8테마 스위처 `name="ahf-theme"` / `.ahf-themebar` 존재
  - core CSS hash marker 존재
  - `layout-github` 존재
  - `body-icon` 존재
  - `h1` 1개
  - GitHub 본문 섹션 h2 모두 `body-icon` 포함
  - 목차는 `toc-map` + `toc-pills` canonical chip nav 구조
  - 모드 필수 블록: verdict, question toc, repo identity, quickstart readiness, health signals, code/file tour, release/activity timeline, security/license, risk matrix, final decision, next actions, source limits 포함
  - FACT / INFERENCE / UNKNOWN 구분 포함
  - 표 `caption` 존재
  - vt 계약: `hero-map` 구조(`.vt-shell` + `.hm-grid`) 포함
  - wg 계약: 추천 위젯 `wg-11` 포함
  - `sources/profile.json`은 `auto`, source manifest 버전은 `5.9.1`
  - legacy `#theme-toggle`, `draggable`, `contenteditable`, 동작 `<script>` 없음

검증 임시 폴더:

```text
/tmp/ahf-canonical-16-mX7bBC
```

검증 결과:

```text
python3 skills/adaptive-html-final/scripts/validate_output.py /tmp/ahf-canonical-16-mX7bBC --skill-dir skills/adaptive-html-final
HTML files: 17
OK

python3 skills/adaptive-html-final/scripts/quality_contract_check.py /tmp/ahf-canonical-16-mX7bBC
OK — quality contract guard passed (16 HTML content file(s))

python3 skills/adaptive-html-final/tests/test_governance_gates.py
77/77 checks passed
```

다음 continuation/session 대상:

```text
15 youtube_analysis
skills/adaptive-html-final/examples/15_youtube_vibecoding_gap.html
```

## 15 youtube_analysis 처리 기록

- 처리 시각: 2026-06-08 KST
- 대상 파일: `skills/adaptive-html-final/examples/15_youtube_vibecoding_gap.html`
- 대상 layout: `skills/adaptive-html-final/assets/layouts/youtube-analysis.html`
- 최신 manifest: `5.9.1`
- 판정: 이미 최신 5.9.1 계약을 만족해 example 본문 수정 없음.
- 확인한 계약:
  - `profile auto`
  - 8테마 스위처 `name="ahf-theme"` / `.ahf-themebar` 존재
  - core CSS hash marker 존재
  - `layout-youtube` 존재
  - `body-icon` 존재
  - `h1` 1개
  - YouTube 본문 섹션 h2 모두 `body-icon` 포함
  - 모드 필수 블록: source & trust snapshot, TL;DW + watching decision, Video Evidence Map, chapter/retention story, comment signal wall, opportunity matrix, claim/evidence/risk, video blueprint, reuse pack, next actions, source limits 포함
  - FACT / INFERENCE / UNKNOWN 구분 포함
  - Evidence Map 표는 5행 이상, timeline 항목은 4개 이상
  - YouTube iframe/embed 없음
  - 표 `caption` 존재
  - vt 계약: `timeline` 구조(`.vt-shell` + `.tl-item`) 포함
  - 보강 vt: `risk-matrix` 구조(`.rm-grid`) 포함
  - wg 계약: 추천 위젯 `wg-11` 포함
  - `sources/profile.json`은 `auto`, source manifest 버전은 `5.9.1`
  - legacy `#theme-toggle`, `draggable`, `contenteditable`, 동작 `<script>` 없음

검증 임시 폴더:

```text
/tmp/ahf-canonical-16-8ji2SN
```

검증 결과:

```text
python3 skills/adaptive-html-final/scripts/validate_output.py /tmp/ahf-canonical-16-8ji2SN --skill-dir skills/adaptive-html-final
HTML files: 17
OK

python3 skills/adaptive-html-final/scripts/quality_contract_check.py /tmp/ahf-canonical-16-8ji2SN
OK — quality contract guard passed (16 HTML content file(s))

python3 skills/adaptive-html-final/tests/test_governance_gates.py
77/77 checks passed
```

다음 continuation/session 대상:

```text
16 manual_analysis
skills/adaptive-html-final/examples/16_manual_product_runbook.html
```

## 16 manual_analysis 처리 기록

- 처리 시각: 2026-06-08 KST
- 대상 파일: `skills/adaptive-html-final/examples/16_manual_product_runbook.html`
- 대상 layout: `skills/adaptive-html-final/assets/layouts/manual-analysis.html`
- 최신 manifest: `5.9.1`
- 판정: 최신 5.9.1 계약 중 수동 감사 기준을 강화하기 위해 example 본문 일부 보강.
- 수정 내용:
  - `Task Recipes` 섹션에 `h2-sub` 보조 설명 추가
  - `Troubleshooting` 섹션을 4개 시나리오로 확장
  - 각 트러블슈팅 시나리오를 `증상 → 가능 원인 → 진단 순서 → 복구` 4단 구조로 전개
- 확인한 계약:
  - `profile auto`
  - 8테마 스위처 `name="ahf-theme"` / `.ahf-themebar` 존재
  - core CSS hash marker 존재
  - `layout-manual` 존재
  - `body-icon` 존재
  - `h1` 1개
  - manual 본문 주요 섹션 h2에 `body-icon` 및 `h2-sub` 포함
  - 모드 필수 블록: source & version snapshot, reader role router, first success path, prerequisites & safety, task recipes, reference extract, decision guide, troubleshooting, operations runbook, manual audit, next actions, source limits 포함
  - 역할 라우터에 역할별 권장 읽기 순서와 이관 기준 포함
  - task recipe 표준 구조 6필드(`목적`, `사전조건`, `절차`, `완료 기준`, `롤백`, `원문 근거`) 포함
  - 작성 가능 레시피 4개 이상 식별
  - troubleshooting 시나리오 4개를 4단 구조로 전개
  - manual audit 지적 3건 이상에 원문 위치 포함
  - 표 `caption` 존재
  - vt 계약: `hero-map` 구조(`.vt-shell` + `.hm-grid`) 포함
  - 보강 vt: `checklist-flow` 구조(`.cf-item`) 포함
  - wg 계약: 추천 위젯 `wg-13` 포함
  - `sources/profile.json`은 `auto`, source manifest 버전은 `5.9.1`
  - legacy `#theme-toggle`, `draggable`, `contenteditable`, 동작 `<script>` 없음

검증 임시 폴더:

```text
/tmp/ahf-canonical-16-QQkFbh
```

검증 결과:

```text
python3 skills/adaptive-html-final/scripts/validate_output.py /tmp/ahf-canonical-16-QQkFbh --skill-dir skills/adaptive-html-final
HTML files: 17
OK

python3 skills/adaptive-html-final/scripts/quality_contract_check.py /tmp/ahf-canonical-16-QQkFbh
OK — quality contract guard passed (16 HTML content file(s))

python3 skills/adaptive-html-final/tests/test_governance_gates.py
77/77 checks passed
```

다음 continuation/session 대상:

```text
없음 — manifest 기준 정본 16개 모두 완료
```

## 최종 완료 감사

- 감사 시각: 2026-06-08 KST
- manifest 버전: `5.9.1`
- manifest `examples.files`: 17개(`index.html` + 정본 모드 HTML 16개)
- 정본 모드 HTML: `01_`부터 `16_`까지 16개 존재
- 진행표 상태: 16개 행 모두 `완료` / `통과`
- 처리 기록 섹션: `01`부터 `16`까지 16개 존재
- source snapshot:
  - `sources/profile.json`: `auto`
  - `sources/adaptive-html-final-manifest.json`: `5.9.1`
  - `sources/css-integrity.json` core asset order: `theme.css,components.css,visual-components.css,layouts.css,print.css`
  - core CSS SHA-256: `ba385ece7fe071ac7377b2b42d41d68a9dbfe2b91557d632f5d48277020863e3`
- 최종 검증 범위: `/tmp/ahf-canonical-16-QQkFbh`
  - 포함 HTML: `index.html` + 정본 모드 HTML 16개
  - manifest 밖 레거시 examples 제외
  - `output/` 폴더 제외
- 최종 검증:

```text
python3 skills/adaptive-html-final/scripts/validate_output.py /tmp/ahf-canonical-16-QQkFbh --skill-dir skills/adaptive-html-final
HTML files: 17
OK

python3 skills/adaptive-html-final/scripts/quality_contract_check.py /tmp/ahf-canonical-16-QQkFbh
OK — quality contract guard passed (16 HTML content file(s))

python3 skills/adaptive-html-final/tests/test_governance_gates.py
77/77 checks passed
```

- 최종 변경 범위:
  - 수정: `skills/adaptive-html-final/examples/16_manual_product_runbook.html`
  - 추가/갱신: `dev-plan/adaptive-html-final-examples-v591-sequential-progress.md`
  - 수정하지 않음: core assets, `sources/`, `output/`, manifest 밖 레거시 examples
