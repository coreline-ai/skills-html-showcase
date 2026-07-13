# 신규 모드 4종 QA 수정 요약

- Date: 2026-06-21
- Scope: output-only HTML pretest QA
- Browser audit: `after-browser-audit.json`
- Result: `BROWSER_AUDIT_OK`

## Fixed issues

| Mode | Main fixes |
|---|---|
| `business_plan_html` | 모바일 fixed 목차 버튼 하단 안전 여백 보강 |
| `storm_research` | 모바일 dock 버튼을 목차 1개로 축소, section-head 간격 확대 |
| `social_trend_dashboard` | “검증 필요” 막대 warn 색상으로 변경, h2 간격 확대 |
| `operator_manual_html` | 목차를 첫 섹션 앞 독립 nav로 이동, h2 간격 확대 |

## Shared after checks

- Desktop 1280x720 and mobile 390x844 Playwright render pass
- Console/page errors: 0
- Horizontal overflow: 0
- Missing internal anchors: 0
- `h1`: 1 per page
- `main#main`: present
- Theme radios: 8 per page
- Behavioral script: 0
- `draggable/contenteditable`: 0
