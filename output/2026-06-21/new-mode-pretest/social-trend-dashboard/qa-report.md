# QA Report — social_trend_dashboard

- Date: 2026-06-21
- Assigned QA agent: Tesla
- Target: `output/2026-06-21/new-mode-pretest/social-trend-dashboard/index.html`
- Scope: output-only pretest HTML QA + direct fix
- Health score: 94 → 99

## Before findings

- collection_summary의 “검증 필요” 막대가 good/green으로 표시되어 완료 상태처럼 오해될 수 있음.
- h2와 보조문 간격이 12px으로 business/operator 기준보다 살짝 좁음.

## Fixes applied

- “검증 필요” 상태 막대를 warn/orange 계열로 변경했습니다.
- h2 margin-bottom을 12px → 14px로 맞췄습니다.

## After verification

- 검증 필요 status-fill.warn 확인
- h2 설명 간격 14px
- 무JS 차트/카드 유지
- records schema/dedupe/caveat 섹션 유지
- overflow 0, 행동 JS 0

## Evidence

- Main browser audit: `../_qa/after-browser-audit.json`
- After desktop screenshot: `../_qa/screenshots-after/social_trend_dashboard-desktop.png`
- After mobile screenshot: `../_qa/screenshots-after/social_trend_dashboard-mobile.png`

## Notes

This is still a pre-implementation mode preview. Official `validate_output.py` is intentionally not treated as the completion gate until the new mode is actually registered with layout/assets/source manifest support.
