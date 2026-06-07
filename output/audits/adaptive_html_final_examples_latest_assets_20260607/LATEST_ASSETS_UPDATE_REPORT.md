# adaptive-html-final examples 최신 assets 동기화 리포트

## 대상

- URL: `http://localhost:8080/skills/adaptive-html-final/examples/index.html?v=543`
- 대상 파일: `skills/adaptive-html-final/examples/index.html` + 16개 모드 HTML
- 스킬 버전: `skills/adaptive-html-final/manifest.json` 기준 `5.8.1`
- 적용 프로파일: `auto`

## 발견 원인

최신 `skills/adaptive-html-final/assets/widgets.css`와 `visual-html.css`가 변경되었지만, `examples/` 내부 HTML 인라인 CSS 및 `examples/sources/assets/` 스냅샷은 이전 버전이라 검증기가 아래 문제를 보고했습니다.

- `profile_required_css_not_inlined`: 17개 HTML에서 `widgets.css`, `visual-html.css` 최신 원문 미반영
- `css_integrity_conditional_hash_mismatch`: `widgets.css`, `visual-html.css`
- `output_css_snapshot_mismatch`: `sources/assets/widgets.css`, `sources/assets/visual-html.css`

## 적용 내용

1. 예제 HTML 17개 전체의 `adaptive-html-final-v581-sync` 인라인 스타일을 최신 assets 원문으로 재생성했습니다.
2. `examples/sources/profile.json`을 `auto`로 재확인했습니다.
3. `examples/sources/adaptive-html-final-manifest.json`을 현재 manifest와 동기화했습니다.
4. `examples/sources/css-integrity.json`을 현재 core/conditional asset hash로 갱신했습니다.
5. `examples/sources/assets/*.css`를 현재 `skills/adaptive-html-final/assets/*.css`와 byte 일치하도록 갱신했습니다.
6. 16모드 전체에 대해 390px / 1280px Playwright 캡쳐 감사를 다시 수행했습니다.

## 최종 검증

| 검증 | 결과 |
|---|---|
| `validate_output.py skills/adaptive-html-final/examples --skill-dir skills/adaptive-html-final` | OK, HTML files 17 |
| `quality_contract_check.py skills/adaptive-html-final/examples` | OK |
| `completion_check.py skills/adaptive-html-final/examples` | 3/3 PASS, governance 77/77 PASS |
| 16모드 Playwright 390px audit | 전부 overflow 없음, h2/icon 누락 0 |
| 16모드 Playwright 1280px audit | 전부 overflow 없음, h2/icon 누락 0 |
| `git diff --check` | OK |

## 16모드 브라우저 감사 요약

| # | Mode | 390 overflow | 1280 overflow | Missing h2/icon | Theme radios | 상태 |
|---:|---|---|---|---:|---:|---|
| 01 | beginner_html | OK | OK | 0 | 8 | OK |
| 02 | expert_html | OK | OK | 0 | 8 | OK |
| 03 | article_html | OK | OK | 0 | 8 | OK |
| 04 | education_html | OK | OK | 0 | 8 | OK |
| 05 | blog_writer | OK | OK | 0 | 8 | OK |
| 06 | seo_dashboard | OK | OK | 0 | 8 | OK |
| 07 | platform_blog | OK | OK | 0 | 8 | OK |
| 08 | skill_audit | OK | OK | 0 | 8 | OK |
| 09 | reference_html | OK | OK | 0 | 8 | OK |
| 10 | comparison_html | OK | OK | 0 | 8 | OK |
| 11 | case_study_html | OK | OK | 0 | 8 | OK |
| 12 | landing_brief_html | OK | OK | 0 | 8 | OK |
| 13 | checklist_playbook | OK | OK | 0 | 8 | OK |
| 14 | github_analysis | OK | OK | 0 | 8 | OK |
| 15 | youtube_analysis | OK | OK | 0 | 8 | OK |
| 16 | manual_analysis | OK | OK | 0 | 8 | OK |

## 증거 산출물

- Audit JSON: `output/audits/adaptive_html_final_examples_latest_assets_20260607/examples-latest-assets-audit.json`
- Audit MD: `output/audits/adaptive_html_final_examples_latest_assets_20260607/examples-latest-assets-audit.md`
- Screenshots: `output/audits/adaptive_html_final_examples_latest_assets_20260607/screenshots/`
