# 16모드 예제 최신화 적용 리포트 — goal2

## 적용 기준

- 대상: `http://localhost:8080/skills/adaptive-html-final/examples/index.html?v=543`
- 스킬 버전: `skills/adaptive-html-final/manifest.json` 기준 v5.8.1
- 기대 core CSS hash: `7e4e9bd4137c409af3a6cad47eff4c0c9e5b7ce0743ee86a6ab59bef7b2876cb`
- 처리 규칙: 01→16 순서로 각 파일을 개별 패치. 각 모드 처리 후 `/tmp/ahf_goal2_mode_NN_cache`를 생성/삭제하고, 브라우저 검증은 모드·뷰포트마다 새 Playwright browser context + cache-busting query로 수행.

## 실제 변경 내용

1. `examples/index.html` + 16개 예제 HTML에 최신 core CSS 5종과 `theme-dark.css` 원문을 재인라인했다.
2. `skills/adaptive-html-final/examples/sources/`를 생성/동기화했다.
   - `profile.json`: `auto`
   - `css-integrity.json`: current core/conditional asset hashes
   - `adaptive-html-final-manifest.json`: current manifest snapshot
   - `sources/assets/*.css`: 현재 스킬 CSS 스냅샷
3. `02_expert_llm_gateway_report.html`의 `section.decision-grid`를 `section.decision-section > div.decision-grid`로 정본화했다.
4. `09_reference_regex.html`의 `toc-map`을 `.toc-pills` + `a.toc-pill > b` 정본 구조로 바꿨다.
5. 14/15의 `.try` 내부 카드 대비 guard를 추가했다.
6. 01~16 각 모드에 부족한 1순위 vt / 추천 wg를 실제 본문 섹션으로 보강했다.
7. 제목 없는 직접 섹션에 `h2 + body-icon`을 보강했고, `.try` h2도 body-icon을 갖도록 맞췄다.
8. `validate_output.py`에 다음 강제 gate를 추가했다.
   - `mode_template_contract_gate`: mode별 1순위 vt + 추천 wg 사용 강제
   - `direct_section_title_icon_policy_gate`: 직접 섹션 h2/body-icon 강제
   - `body_icon_diversity_gate`: 동일 SVG 아이콘 반복 방지
   - `_inner_html` 긴 문서 처리 보정
9. `SKILL.md`에 위 gate와 계약을 문서화했다.

## 검증 결과

| 검증 | 결과 |
|---|---|
| `validate_output.py skills/adaptive-html-final/examples --skill-dir skills/adaptive-html-final --json` | OK, issues 0, warnings 0 |
| `quality_contract_check.py skills/adaptive-html-final/examples` | OK |
| `completion_check.py skills/adaptive-html-final/examples` | 3/3 PASS |
| gallery 1280/390 browser audit | overflow 없음, links 16, theme radios 8 |
| 16개 모드 390 browser audit | 전부 overflow 없음 |

## 모드별 최종 확인

| # | mode | file | direct sections | themes | 390 overflow | core hash | primary vt | recommended wg | status |
|---:|---|---|---:|---:|---|---|---|---|---|
| 01 | `beginner_html` | `01_beginner_passkey_login.html` | 9 | 8 | OK | OK | OK | wg-10 | OK |
| 02 | `expert_html` | `02_expert_llm_gateway_report.html` | 10 | 8 | OK | OK | OK | wg-03 | OK |
| 03 | `article_html` | `03_article_side_project_signal.html` | 11 | 8 | OK | OK | OK | wg-02 | OK |
| 04 | `education_html` | `04_education_git_rebase_workshop.html` | 14 | 8 | OK | OK | OK | wg-06 | OK |
| 05 | `blog_writer` | `05_blog_deepwork_4day_retro.html` | 9 | 8 | OK | OK | OK | wg-17 | OK |
| 06 | `seo_dashboard` | `06_seo_prompt_engineering_dashboard.html` | 12 | 8 | OK | OK | OK | wg-11 | OK |
| 07 | `platform_blog` | `07_platform_tech_retro_adaptation.html` | 13 | 8 | OK | OK | OK | wg-02 | OK |
| 08 | `skill_audit` | `08_skill_audit_codereview_bot.html` | 9 | 8 | OK | OK | OK | wg-03 | OK |
| 09 | `reference_html` | `09_reference_regex.html` | 14 | 8 | OK | OK | OK | wg-04 | OK |
| 10 | `comparison_html` | `10_comparison_message_queue.html` | 9 | 8 | OK | OK | OK | wg-01 | OK |
| 11 | `case_study_html` | `11_case_study_search_index_outage.html` | 12 | 8 | OK | OK | OK | wg-12 | OK |
| 12 | `landing_brief_html` | `12_landing_pagercalm_brief.html` | 9 | 8 | OK | OK | OK | wg-02 | OK |
| 13 | `checklist_playbook` | `13_checklist_data_migration.html` | 9 | 8 | OK | OK | OK | wg-11 | OK |
| 14 | `github_analysis` | `14_github_analysis_fastapi_starter.html` | 12 | 8 | OK | OK | OK | wg-11 | OK |
| 15 | `youtube_analysis` | `15_youtube_vibecoding_gap.html` | 11 | 8 | OK | OK | OK | wg-11 | OK |
| 16 | `manual_analysis` | `16_manual_product_runbook.html` | 12 | 8 | OK | OK | OK | wg-13 | OK |

## 증거 산출물

- Audit JSON: `output/audits/adaptive_html_final_examples_16_modes_goal2_20260607/examples-16-mode-audit.json`
- Audit summary: `output/audits/adaptive_html_final_examples_16_modes_goal2_20260607/examples-16-mode-audit.md`
- Gallery audit: `output/audits/adaptive_html_final_examples_16_modes_goal2_20260607/gallery-index-audit.json`
- Screenshots: `output/audits/adaptive_html_final_examples_16_modes_goal2_20260607/screenshots/`
- Completion log: `/tmp/completion_after_skilldoc.txt`


## 최종 재검증 — 2026-06-07

| 요구사항 | 현재 증거 | 판정 |
|---|---|---|
| 예제 17개 HTML 최신 core CSS + `theme-dark.css` 원문 재주입 | `validate_output.py`의 `inline_core_css_not_verbatim` / `theme_dark_css_not_inlined` 이슈 0, HTML 17개 OK | PASS |
| `sources/profile.json`, `css-integrity.json`, manifest 스냅샷 정책 | `skills/adaptive-html-final/examples/sources/` 하위 3종 + `sources/assets/*.css` 존재, manifest v5.8.1 일치 | PASS |
| 02 Expert `decision-grid` 구조 | `section.decision-section > div.decision-grid` 구조, `section.decision-grid` 미사용 | PASS |
| 09 Reference `toc-map` 정본화 | 목차 내부가 `.toc-pills` + `.toc-pill` 링크 구조로 구성됨 | PASS |
| 14/15 `.try` 카드 대비 guard | `.try .repo-card ...`, `.try .youtube-card ...` 대비 guard 인라인 | PASS |
| mode별 1순위 vt / 추천 wg 강제 | `validate_output.py`의 `mode_template_contract_gate` 추가 및 17 HTML 검증 OK | PASS |
| h2 없는 섹션 정책 + body-icon 다양성 gate | `direct_section_title_icon_policy_gate`, `body_icon_diversity_gate` 추가 및 검증 OK | PASS |
| 01→16 순차 처리 + 캐시 영향 0 | 모드별 임시 `/tmp/ahf_goal2_mode_NN_cache` 생성/삭제 방식으로 처리, 현재 잔여 캐시 0 | PASS |
| 1280/390 레이아웃 확인 | `examples-16-mode-audit.json`, `gallery-index-audit.json`, `screenshots/` 생성. 전체 overflow 없음 | PASS |

최종 명령 로그:

```bash
python3 skills/adaptive-html-final/scripts/validate_output.py skills/adaptive-html-final/examples --skill-dir skills/adaptive-html-final
# HTML files: 17 / OK

python3 skills/adaptive-html-final/scripts/quality_contract_check.py skills/adaptive-html-final/examples
# OK — quality contract guard passed (16 HTML content file(s))

python3 skills/adaptive-html-final/scripts/completion_check.py skills/adaptive-html-final/examples
# validate PASS, quality_contract PASS, governance 77/77 PASS, 완료 통합 검증 3/3 OK
```
