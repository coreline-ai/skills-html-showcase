# Mode Build Sheet — expert_html

- mode: `expert_html`
- topic: 멀티 에이전트 HTML 품질 게이트 아키텍처
- profile: `auto`
- layout: `assets/layouts/expert-report.html`
- primary vt: `risk-matrix`
- wg candidates: wg-03, wg-04, wg-11, wg-12, wg-16, wg-17
- page: `pages/09_expert_multi_agent_quality_architecture.html`

## Sections
1. 전문가 결론
2. 문제 구조
3. 아키텍처 원칙
4. 품질 게이트 계층
5. 렌더 감사 모델
6. 증거 파일 계약
7. 운영 리스크
8. 조직 역할
9. 도입 로드맵
10. 최종 권고

## Template mapping

| Section | Pattern |
|---:|---|
| 1 | 전문가 결론 → layout scaffold |
| 2 | 문제 구조 → vt-risk-matrix |
| 3 | 아키텍처 원칙 → lede-note/source-note |
| 4 | 품질 게이트 계층 → wg widget |
| 5 | 렌더 감사 모델 → editorial rail card |
| 6 | 증거 파일 계약 → layout scaffold |
| 7 | 운영 리스크 → vt-risk-matrix |
| 8 | 조직 역할 → lede-note/source-note |
| 9 | 도입 로드맵 → wg widget |
| 10 | 최종 권고 → editorial rail card |

## Visual risks

- 390px에서 h2 번호 pill 줄바꿈 금지
- rail 텍스트 좌측 접착 금지
- footer 좌측 붙음 금지
- 비정본 클래스 `template-card-head`/`source-preserve-static` 금지

## Stop condition

validate/quality/completion/render-audit 중 하나라도 실패하면 다음 모드로 넘어가지 않는다.
