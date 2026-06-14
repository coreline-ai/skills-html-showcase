# Mode Build Sheet — platform_blog

- mode: `platform_blog`
- topic: B2B SaaS 릴리스 노트의 플랫폼별 재편집
- profile: `auto`
- layout: `assets/layouts/platform-adaptation.html`
- primary vt: `card-grid`
- wg candidates: wg-02
- page: `pages/02_platform_blog_saas_release_notes.html`

## Sections
1. 플랫폼별 독자 차이
2. 티스토리 long-form 전략
3. 브런치식 문제 제기
4. 네이버 검색 유입 구조
5. Velog 개발자 맥락
6. LinkedIn 요약 카드
7. CTA와 출처 배치
8. 반복 발행 캘린더
9. 성과 측정 지표
10. 최종 운영안

## Template mapping

| Section | Pattern |
|---:|---|
| 1 | 플랫폼별 독자 차이 → layout scaffold |
| 2 | 티스토리 long-form 전략 → vt-card-grid |
| 3 | 브런치식 문제 제기 → lede-note/source-note |
| 4 | 네이버 검색 유입 구조 → wg widget |
| 5 | Velog 개발자 맥락 → editorial rail card |
| 6 | LinkedIn 요약 카드 → layout scaffold |
| 7 | CTA와 출처 배치 → vt-card-grid |
| 8 | 반복 발행 캘린더 → lede-note/source-note |
| 9 | 성과 측정 지표 → wg widget |
| 10 | 최종 운영안 → editorial rail card |

## Visual risks

- 390px에서 h2 번호 pill 줄바꿈 금지
- rail 텍스트 좌측 접착 금지
- footer 좌측 붙음 금지
- 비정본 클래스 `template-card-head`/`source-preserve-static` 금지

## Stop condition

validate/quality/completion/render-audit 중 하나라도 실패하면 다음 모드로 넘어가지 않는다.
