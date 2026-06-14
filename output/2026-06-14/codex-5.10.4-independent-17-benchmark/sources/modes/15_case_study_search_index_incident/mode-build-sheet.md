# Mode Build Sheet — case_study_html

- mode: `case_study_html`
- topic: 검색 인덱스 장애 37분 복구 사례
- profile: `auto`
- layout: `assets/layouts/case-study.html`
- primary vt: `incident-summary`
- wg candidates: wg-12
- page: `pages/15_case_study_search_index_incident.html`

## Sections
1. 사건 개요
2. 영향 범위
3. 타임라인
4. 탐지 신호
5. 초기 오판
6. 복구 조치
7. 고객 커뮤니케이션
8. 재발 방지
9. 남은 리스크
10. 회고 결론

## Template mapping

| Section | Pattern |
|---:|---|
| 1 | 사건 개요 → layout scaffold |
| 2 | 영향 범위 → vt-incident-summary |
| 3 | 타임라인 → lede-note/source-note |
| 4 | 탐지 신호 → wg widget |
| 5 | 초기 오판 → editorial rail card |
| 6 | 복구 조치 → layout scaffold |
| 7 | 고객 커뮤니케이션 → vt-incident-summary |
| 8 | 재발 방지 → lede-note/source-note |
| 9 | 남은 리스크 → wg widget |
| 10 | 회고 결론 → editorial rail card |

## Visual risks

- 390px에서 h2 번호 pill 줄바꿈 금지
- rail 텍스트 좌측 접착 금지
- footer 좌측 붙음 금지
- 비정본 클래스 `template-card-head`/`source-preserve-static` 금지

## Stop condition

validate/quality/completion/render-audit 중 하나라도 실패하면 다음 모드로 넘어가지 않는다.
