# Adaptive HTML Final 16모드 예제 갤러리 정밀 분석 리포트

## 1. 기준 상태

- 대상 URL: `http://localhost:8080/skills/adaptive-html-final/examples/index.html?v=543`
- 코드 기준 스킬: `skills/adaptive-html-final/manifest.json` = **v5.8.1 / 16 modes**
- 결정론 진입점: `AGENTS.md`도 현재 파일 기준 **v5.8.1 / 16 modes / 8-theme / auto profile**로 업데이트되어 있음
- 기대 코어 CSS 해시: `7e4e9bd4137c409af3a6cad47eff4c0c9e5b7ce0743ee86a6ab59bef7b2876cb`
- 분석 방식: 16개 모드를 1개씩 순차 처리. 각 모드·각 뷰포트마다 새 Playwright browser context를 만들고 cache-busting query를 붙여 이전 모드 렌더 상태가 다음 모드에 영향을 주지 않게 함.

## 2. 자동 검증 결과

| 게이트 | 결과 | 근거 |
|---|---|---|
| `validate_output.py skills/adaptive-html-final/examples --skill-dir skills/adaptive-html-final --json` | **FAIL** | issues 55건, warnings 2건 |
| `quality_contract_check.py skills/adaptive-html-final/examples` | **FAIL** | github/youtube try 카드 대비 guard 2건 |
| `completion_check.py skills/adaptive-html-final/examples` | **INCOMPLETE** | validate/quality FAIL, governance 77/77 PASS |
| Browser 1280/390 gallery | PASS | index links 16개, theme radios 8개, overflow 없음 |
| Browser 390 mode pages | PASS | 16개 모드 모두 page horizontal overflow 없음 |
| Behavioral JS / forbidden primitive | PASS | audit에서 behavioral script/draggable/contenteditable 0 |

### validate issue type 요약

- `inline_css_hash_mismatch`: 17건
- `inline_core_css_not_verbatim`: 17건
- `theme_dark_css_not_inlined`: 17건
- `missing_profile_json`: 1건
- `expert_decision_grid_section_collision`: 1건
- `toc_map_contract_missing_pills`: 1건
- `missing_css_integrity_manifest`: 1건

### validate issue page 요약

- `02_expert_llm_gateway_report.html`: 4건
- `09_reference_regex.html`: 4건
- `01_beginner_passkey_login.html`: 3건
- `03_article_side_project_signal.html`: 3건
- `04_education_git_rebase_workshop.html`: 3건
- `05_blog_deepwork_4day_retro.html`: 3건
- `06_seo_prompt_engineering_dashboard.html`: 3건
- `07_platform_tech_retro_adaptation.html`: 3건
- `08_skill_audit_codereview_bot.html`: 3건
- `10_comparison_message_queue.html`: 3건
- `11_case_study_search_index_outage.html`: 3건
- `12_landing_pagercalm_brief.html`: 3건
- `13_checklist_data_migration.html`: 3건
- `14_github_analysis_fastapi_starter.html`: 3건
- `15_youtube_vibecoding_gap.html`: 3건
- `16_manual_product_runbook.html`: 3건
- `index.html`: 3건
- `_root`: 2건

## 3. 전역 결론

1. **가장 큰 문제는 최신 스킬 자산과 예제 HTML의 해시/원문 동기화가 깨진 상태**다. 17개 HTML(index + 16 examples)이 모두 현재 기대 코어 해시 `7e4e...`가 아니라 이전 해시 `329b...`를 들고 있고, `layouts.css` byte-for-byte 인라인 및 `theme-dark.css` 원문 인라인 검증을 통과하지 못한다.
2. **8테마 UI와 모바일 폭 자체는 현재 렌더에서 무너지지 않는다.** 1280px/390px 모두 갤러리 및 16개 모드 페이지의 page-level horizontal overflow는 없었다.
3. **최신 스킬의 layout-first / canonical vt-wg 계약은 예제 본문에서 아직 충분히 증명되지 않는다.** 다수 모드가 1순위 vt 템플릿을 실제 본문 markup으로 포함하지 않거나, 추천 wg가 전혀 없다. 지금은 validate가 이 계약을 직접 강제하지 않기 때문에 구조 검증은 통과처럼 보일 수 있다.
4. **섹션 h2 아이콘 계약은 “h2가 있는 섹션” 기준으로는 통과하지만, h2 없는 직접 섹션이 남아 있다.** summary/verdict/toc류 섹션을 예외로 명시할지, 아니면 모든 view 섹션에 제목+body-icon을 붙일지 스킬에 더 분명히 써야 한다.
5. **14/15 신규 분석 모드에는 실제 quality gate 실패가 있다.** `.try` 내부 카드 텍스트 색상 reset이 없어 다크/고대비 테마에서 텍스트 대비 회귀 가능성이 있다.

## 4. 모드별 분석 표

| # | mode | 섹션 수 | 390 overflow | validate | quality | h2 없는 섹션 | 1순위 vt | 추천 wg 감지 | 최신 스킬 대비 보강 필요 |
|---:|---|---:|---|---:|---:|---:|---|---|---|
| 01 | `beginner_html` | 8 | OK | 3 | 0 | 1 | OK | - | primary vt concept-explainer는 감지되지만, summary-card가 h2 없이 시작한다. auto 프로파일 예제라면 wg-10/13/15 중 최소 1개를 넣을지 명확히 결정 필요. |
| 02 | `expert_html` | 9 | OK | 4 | 0 | 2 | 보강 | - | expert 전용 P0: validate의 expert_decision_grid_section_collision. section.decision-grid를 section.decision-section + 내부 .decision-grid wrapper로 교체. 1순위 vt risk-matrix도 본문 템플릿으로 명시 필요. |
| 03 | `article_html` | 10 | OK | 3 | 0 | 2 | 보강 | - | article의 1순위 vt decision-tree가 감지되지 않는다. 초반 pull quote/context 섹션 h2 없는 구조를 예외로 둘지, 섹션 타이틀을 보강할지 결정 필요. |
| 04 | `education_html` | 13 | OK | 3 | 0 | 5 | 보강 | - | education은 13섹션이나 learning-goals/before-start 등 5개 섹션이 h2 없이 시작한다. 1순위 vt timeline 미감지, 교육 위젯(wg-06/07/08/13/14/15/20)도 본문에는 없음. |
| 05 | `blog_writer` | 8 | OK | 3 | 0 | 0 | 보강 | - | blog는 article 내부 섹션 구조는 정상이고 마지막 try도 보인다. 다만 1순위 vt timeline 및 wg-17 PR/writeup 계열 보강은 감지되지 않는다. |
| 06 | `seo_dashboard` | 11 | OK | 3 | 0 | 1 | 보강 | - | SEO는 card-grid 1순위 vt와 wg-11이 감지되지 않는다. seo-overview h2 없는 카드 시작부의 제목/아이콘 정책 보강 필요. |
| 07 | `platform_blog` | 12 | OK | 3 | 0 | 1 | 보강 | - | platform은 1순위 vt card-grid 대신 risk-matrix 계열이 감지된다. 플랫폼별 변환 카드라면 card-grid/pr-writeup 구조와 wg-02 시각 방향을 더 명확히 써야 한다. |
| 08 | `skill_audit` | 8 | OK | 3 | 0 | 1 | 보강 | - | skill_audit는 quality-gate 1순위 vt가 감지되지 않는다. 목적/구조/라인감사/개선안은 있으나 qg/file-tour/prompt-tuner 템플릿 계약을 더 강제해야 한다. |
| 09 | `reference_html` | 13 | OK | 4 | 0 | 2 | 보강 | - | reference 전용 P0: toc_map_contract_missing_pills. .toc-map bare ol/a 구조를 .toc-pills + a.toc-pill>b로 고쳐야 한다. 1순위 file-tour vt/wg reference 위젯도 감지되지 않는다. |
| 10 | `comparison_html` | 8 | OK | 3 | 0 | 1 | 보강 | - | comparison은 comparison-cards 1순위 vt와 wg-01/02가 감지되지 않는다. 비교 모드는 현재 표/카드가 있어도 canonical comparison-cards를 최소 1회 넣도록 보강 필요. |
| 11 | `case_study_html` | 11 | OK | 3 | 0 | 1 | 보강 | - | case study는 incident-summary 1순위 vt와 wg-12가 감지되지 않는다. 장애 회고라면 incident-summary + timeline/process-swimlane를 명확히 분리해야 한다. |
| 12 | `landing_brief_html` | 8 | OK | 3 | 0 | 1 | 보강 | - | landing은 hero-map 1순위 vt와 랜딩 추천 wg가 감지되지 않는다. value/how/FAQ 구조는 있으나 hero-map/feature-flag/soft-workflow-map 중 하나를 정본으로 넣는 것이 필요. |
| 13 | `checklist_playbook` | 8 | OK | 3 | 0 | 1 | 보강 | - | checklist는 checklist-flow 1순위 vt와 wg-11/13/16/18/19가 감지되지 않는다. check-grid만으로는 최신 템플릿 계약을 충분히 증명하지 못한다. |
| 14 | `github_analysis` | 11 | OK | 3 | 1 | 1 | 보강 | - | github 전용 P0: try_card_contrast_guard_missing. 또한 hero-map 1순위 vt와 추천 wg가 감지되지 않는다. repo-card 내부 p/li 텍스트 색상 reset CSS 필요. |
| 15 | `youtube_analysis` | 11 | OK | 3 | 1 | 1 | OK | wg-11 | youtube 전용 P0: try_card_contrast_guard_missing. timeline 1순위 vt와 wg-11은 감지된다. 다만 h2 없는 verdict 카드와 반복 아이콘(9개 중 unique 4)이 남아 있어 섹션 의미별 icon map 보강 필요. |
| 16 | `manual_analysis` | 12 | OK | 3 | 0 | 1 | OK | wg-13 | manual은 hero-map/checklist-flow 일부와 wg-13이 감지된다. 다만 h2 없는 verdict 카드와 반복 아이콘(10개 중 unique 4)이 남아 있어 manual role/safety/troubleshoot별 icon map 보강 필요. |

## 5. 수정/보강 우선순위

### P0 — 바로 고쳐야 하는 정합성 실패

1. **예제 17개 HTML 전체 자산 재주입**
   - 대상: `skills/adaptive-html-final/examples/index.html`, `01_*.html`~`16_*.html`
   - 조치: 현재 `assets/theme.css`, `components.css`, `visual-components.css`, `layouts.css`, `print.css`, `theme-dark.css`를 원문 그대로 재인라인하고 코어 해시 마커를 `7e4e9bd4137c409af3a6cad47eff4c0c9e5b7ce0743ee86a6ab59bef7b2876cb`로 갱신.
   - 완료 기준: `inline_css_hash_mismatch`, `inline_core_css_not_verbatim`, `theme_dark_css_not_inlined` 0건.
2. **examples 산출물 메타/sources 구성 정리**
   - 대상: `skills/adaptive-html-final/examples/sources/profile.json`, `sources/css-integrity.json`, `sources/adaptive-html-final-manifest.json` 및 `sources/assets/*.css` 필요 여부 결정.
   - 조치: examples를 검증 대상 산출물로 유지할 거면 표준 output처럼 sources를 둔다. 아니면 validate에서 examples 패키지 예외를 명시한다.
3. **02 expert_html decision-grid collision 수정**
   - `section.decision-grid` 금지. `section.decision-section` 안에 내부 wrapper `.decision-grid`를 둔다.
4. **09 reference_html toc-map 정본화**
   - `.toc-map` bare list를 `.toc-pills` + `a.toc-pill > b` 구조로 바꾼다.
5. **14/15 try card contrast guard 추가**
   - `.try .repo-card p/li`, `.try .youtube-card p/li` 또는 공통 `.try [class$="-card"] p/li` 색상 reset을 추가해 다크/고대비 테마에서 텍스트가 묻히지 않게 한다.

### P1 — 최신 스킬 품질 계약을 더 강제해야 하는 부분

1. **auto profile 예제의 1순위 vt 최소 1회 삽입을 검증기로 강제**
   - 현재 15/16 일부를 제외하면 다수 모드에서 1순위 vt가 markup으로 감지되지 않는다.
   - `quality_contract_check.py` 또는 `validate_output.py`에 mode→primary vt marker gate를 추가하는 것이 안전하다.
2. **추천 wg는 “구조형 정보가 있을 때만”이라는 예외를 명시하되, 예제 갤러리는 스킬 능력치 showcase이므로 최소 1개 wg를 각 모드에 넣는 정책이 필요**
   - 현재 본문 wg 감지는 15(`wg-11`), 16(`wg-13`) 위주다.
3. **h2 없는 직접 섹션 정책 정리**
   - summary/verdict/toc를 예외로 둘 거면 validator와 SKILL에 “titleless intro card allowed”를 명시.
   - 사용자 검수 기준에 맞추려면 모든 직접 section/view에 `h2 + body-icon`을 부여.
4. **섹션 아이콘 의미 다양성 gate 강화**
   - 15/16은 h2 icon이 9~10개 있으나 unique SVG가 4개뿐이다. manual/youtube 전용 icon map을 SKILL에 고정하고 반복 비율을 검사한다.
5. **Layout-first 템플릿 사용 증명 강화**
   - `assets/layouts/*.html` placeholder와 실제 예제 섹션 class가 대응되는지 검사하는 gate를 추가하면 “layout-* class만 붙인 자유형 합성” 회귀를 줄일 수 있다.

## 6. 증거 산출물

- JSON: `output/2026-06-08/audits/adaptive_html_final_examples_16_modes_20260607/examples-16-mode-audit.json`
- 요약 MD: `output/2026-06-08/audits/adaptive_html_final_examples_16_modes_20260607/examples-16-mode-audit.md`
- 갤러리 index audit: `output/2026-06-08/audits/adaptive_html_final_examples_16_modes_20260607/gallery-index-audit.json`
- 스크린샷: `output/2026-06-08/audits/adaptive_html_final_examples_16_modes_20260607/screenshots/`
