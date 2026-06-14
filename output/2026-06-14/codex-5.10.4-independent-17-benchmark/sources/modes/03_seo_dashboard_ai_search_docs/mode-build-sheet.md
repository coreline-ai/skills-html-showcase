# Mode Build Sheet — seo_dashboard

- mode: `seo_dashboard`
- topic: AI 검색 시대의 기술 문서 SEO 대시보드
- profile: `auto`
- layout: `assets/layouts/seo-dashboard.html`
- primary vt: `card-grid`
- wg candidates: wg-11
- page: `pages/03_seo_dashboard_ai_search_docs.html`

## Sections
1. 검색 의도 요약
2. 핵심 키워드 군
3. 제목·메타 개선
4. SERP 약속 카드
5. 본문 구조 점검
6. 내부 링크 설계
7. 스키마와 FAQ
8. 콘텐츠 갭
9. 발행 후 측정
10. 우선순위 로드맵

## Template mapping

| Section | Pattern |
|---:|---|
| 1 | 검색 의도 요약 → layout scaffold |
| 2 | 핵심 키워드 군 → vt-card-grid |
| 3 | 제목·메타 개선 → lede-note/source-note |
| 4 | SERP 약속 카드 → wg widget |
| 5 | 본문 구조 점검 → editorial rail card |
| 6 | 내부 링크 설계 → layout scaffold |
| 7 | 스키마와 FAQ → vt-card-grid |
| 8 | 콘텐츠 갭 → lede-note/source-note |
| 9 | 발행 후 측정 → wg widget |
| 10 | 우선순위 로드맵 → editorial rail card |

## Visual risks

- 390px에서 h2 번호 pill 줄바꿈 금지
- rail 텍스트 좌측 접착 금지
- footer 좌측 붙음 금지
- 비정본 클래스 `template-card-head`/`source-preserve-static` 금지

## Stop condition

validate/quality/completion/render-audit 중 하나라도 실패하면 다음 모드로 넘어가지 않는다.
