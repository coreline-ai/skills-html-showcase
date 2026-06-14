# Mode Build Sheet — landing_brief_html

- mode: `landing_brief_html`
- topic: 팀 지식베이스 자동 정리 도구 랜딩 브리프
- profile: `auto`
- layout: `assets/layouts/landing-brief.html`
- primary vt: `hero-map`
- wg candidates: wg-02, wg-05, wg-08, wg-09, wg-16
- page: `pages/16_landing_knowledgebase_autosummary.html`

## Sections
1. 제품 한 줄
2. 대상 사용자
3. 핵심 약속
4. 기능 카드
5. AI 파이프라인
6. 사용 전후
7. 가격 신호
8. 신뢰 장치
9. 도입 CTA
10. 다음 액션

## Template mapping

| Section | Pattern |
|---:|---|
| 1 | 제품 한 줄 → layout scaffold |
| 2 | 대상 사용자 → vt-hero-map |
| 3 | 핵심 약속 → lede-note/source-note |
| 4 | 기능 카드 → wg widget |
| 5 | AI 파이프라인 → editorial rail card |
| 6 | 사용 전후 → layout scaffold |
| 7 | 가격 신호 → vt-hero-map |
| 8 | 신뢰 장치 → lede-note/source-note |
| 9 | 도입 CTA → wg widget |
| 10 | 다음 액션 → editorial rail card |

## Visual risks

- 390px에서 h2 번호 pill 줄바꿈 금지
- rail 텍스트 좌측 접착 금지
- footer 좌측 붙음 금지
- 비정본 클래스 `template-card-head`/`source-preserve-static` 금지

## Stop condition

validate/quality/completion/render-audit 중 하나라도 실패하면 다음 모드로 넘어가지 않는다.
