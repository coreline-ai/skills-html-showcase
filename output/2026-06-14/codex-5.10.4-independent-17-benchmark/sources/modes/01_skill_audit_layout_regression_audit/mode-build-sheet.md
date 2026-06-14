# Mode Build Sheet — skill_audit

- mode: `skill_audit`
- topic: AI 문서 생성 스킬의 레이아웃 회귀 감사
- profile: `auto`
- layout: `assets/layouts/skill-audit-report.html`
- primary vt: `quality-gate`
- wg candidates: wg-03, wg-11, wg-17
- page: `pages/01_skill_audit_layout_regression_audit.html`

## Sections
1. 감사 결론
2. 정본 자산 사용 여부
3. 헤더·목차 계약
4. 섹션 표면 밀도
5. 아이콘 카탈로그 일치
6. 마이크로 레이아웃 리스크
7. 검증기와 눈검수의 차이
8. 재발 방지 게이트
9. 운영 적용 순서
10. 최종 판정

## Template mapping

| Section | Pattern |
|---:|---|
| 1 | 감사 결론 → layout scaffold |
| 2 | 정본 자산 사용 여부 → vt-quality-gate |
| 3 | 헤더·목차 계약 → lede-note/source-note |
| 4 | 섹션 표면 밀도 → wg widget |
| 5 | 아이콘 카탈로그 일치 → editorial rail card |
| 6 | 마이크로 레이아웃 리스크 → layout scaffold |
| 7 | 검증기와 눈검수의 차이 → vt-quality-gate |
| 8 | 재발 방지 게이트 → lede-note/source-note |
| 9 | 운영 적용 순서 → wg widget |
| 10 | 최종 판정 → editorial rail card |

## Visual risks

- 390px에서 h2 번호 pill 줄바꿈 금지
- rail 텍스트 좌측 접착 금지
- footer 좌측 붙음 금지
- 비정본 클래스 `template-card-head`/`source-preserve-static` 금지

## Stop condition

validate/quality/completion/render-audit 중 하나라도 실패하면 다음 모드로 넘어가지 않는다.
