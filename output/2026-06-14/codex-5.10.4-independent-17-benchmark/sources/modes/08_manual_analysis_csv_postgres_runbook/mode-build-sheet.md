# Mode Build Sheet — manual_analysis

- mode: `manual_analysis`
- topic: CSV→Postgres 마이그레이션 운영 런북
- profile: `auto`
- layout: `assets/layouts/manual-analysis.html`
- primary vt: `hero-map`
- wg candidates: wg-04, wg-13, wg-16, wg-18, wg-11, wg-14
- page: `pages/08_manual_analysis_csv_postgres_runbook.html`

## Sections
1. 런북 결론
2. 역할별 사용법
3. 사전조건과 안전장치
4. 첫 성공 경로
5. 작업 레시피
6. 검증 쿼리
7. STOP 기준
8. 트러블슈팅
9. 운영 교대 기록
10. 다음 개선

## Template mapping

| Section | Pattern |
|---:|---|
| 1 | 런북 결론 → layout scaffold |
| 2 | 역할별 사용법 → vt-hero-map |
| 3 | 사전조건과 안전장치 → lede-note/source-note |
| 4 | 첫 성공 경로 → wg widget |
| 5 | 작업 레시피 → editorial rail card |
| 6 | 검증 쿼리 → layout scaffold |
| 7 | STOP 기준 → vt-hero-map |
| 8 | 트러블슈팅 → lede-note/source-note |
| 9 | 운영 교대 기록 → wg widget |
| 10 | 다음 개선 → editorial rail card |

## Visual risks

- 390px에서 h2 번호 pill 줄바꿈 금지
- rail 텍스트 좌측 접착 금지
- footer 좌측 붙음 금지
- 비정본 클래스 `template-card-head`/`source-preserve-static` 금지

## Stop condition

validate/quality/completion/render-audit 중 하나라도 실패하면 다음 모드로 넘어가지 않는다.
