# QA Report — operator_manual_html

- Date: 2026-06-21
- Assigned QA agent: Poincare
- Target: `output/2026-06-21/new-mode-pretest/operator-manual-html/index.html`
- Scope: output-only pretest HTML QA + direct fix
- Health score: 91 → 99

## Before findings

- 목차가 첫 섹션 뒤에 있어 독립 목차가 아니라 첫 섹션에 종속된 흐름처럼 보임.
- section-card h2와 설명문 간격이 10px로 다른 산출물보다 좁음.

## Fixes applied

- Reader Role Router 목차를 header 바로 아래, 첫 섹션 앞 독립 nav로 이동했습니다.
- section-card h2 margin-bottom을 10px → 14px로 조정했습니다.
- `#handoff_boundary`의 `.try` 다크 섹션 안 흰 카드에서 본문 색이 옅게 상속되던 문제를 수정했습니다. 흰 카드 계열(`mini-card/evidence-card/gate-card/lane-card`)은 내부 텍스트를 `var(--ink)` / `var(--ink-soft)`로 reset합니다.

## After verification

- TOC가 첫 섹션보다 먼저 존재
- h2 설명 간격 14px
- CAPTURE_REQUIRED 유지
- operator workflow/table/device mock overflow 0
- 행동 JS 0

## Evidence

- Main browser audit: `../_qa/after-browser-audit.json`
- After desktop screenshot: `../_qa/screenshots-after/operator_manual_html-desktop.png`
- After mobile screenshot: `../_qa/screenshots-after/operator_manual_html-mobile.png`
- Handoff contrast audit: `screenshots/handoff-contrast-audit.json`
- Handoff light screenshot: `screenshots/handoff-boundary-after-light.png`
- Handoff rose screenshot: `screenshots/handoff-boundary-after-rose.png`

## Notes

This is still a pre-implementation mode preview. Official `validate_output.py` is intentionally not treated as the completion gate until the new mode is actually registered with layout/assets/source manifest support.
