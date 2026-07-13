# QA Report — business_plan_html

- Date: 2026-06-21
- Assigned QA agent: Halley
- Target: `output/2026-06-21/new-mode-pretest/business-plan-html/index.html`
- Scope: output-only pretest HTML QA + direct fix
- Health score: 96 → 98

## Before findings

- 공식 validate_output.py는 신규 모드 미등록 pretest 구조라 실패하지만, 화면 QA 대상 이슈는 아님.
- 모바일 fixed 목차 버튼이 마지막 내용과 가까워질 수 있는 low risk 확인.

## Fixes applied

- 모바일에서 fixed 목차 버튼과 하단 콘텐츠가 겹치지 않도록 안전 하단 여백을 보존했습니다.

## After verification

- 데스크톱/모바일 overflow 0
- h2 본문 간격 14px 유지
- TOC가 첫 섹션보다 먼저 독립 카드로 존재
- h1 1개, main#main, theme radios 8, 행동 JS 0

## Evidence

- Main browser audit: `../_qa/after-browser-audit.json`
- After desktop screenshot: `../_qa/screenshots-after/business_plan_html-desktop.png`
- After mobile screenshot: `../_qa/screenshots-after/business_plan_html-mobile.png`

## Notes

This is still a pre-implementation mode preview. Official `validate_output.py` is intentionally not treated as the completion gate until the new mode is actually registered with layout/assets/source manifest support.
