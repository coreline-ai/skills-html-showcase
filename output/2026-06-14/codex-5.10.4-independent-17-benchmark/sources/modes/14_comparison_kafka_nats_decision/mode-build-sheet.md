# Mode Build Sheet — comparison_html

- mode: `comparison_html`
- topic: Kafka와 NATS 도입 기준 비교
- profile: `auto`
- layout: `assets/layouts/comparison-matrix.html`
- primary vt: `comparison-cards`
- wg candidates: wg-01, wg-02
- page: `pages/14_comparison_kafka_nats_decision.html`

## Sections
1. 선택 결론
2. 메시지 모델
3. 운영 복잡도
4. 지연시간
5. 내구성
6. 스케일링
7. 개발자 경험
8. 비용 구조
9. 리스크 매트릭스
10. 결정 가이드

## Template mapping

| Section | Pattern |
|---:|---|
| 1 | 선택 결론 → layout scaffold |
| 2 | 메시지 모델 → vt-comparison-cards |
| 3 | 운영 복잡도 → lede-note/source-note |
| 4 | 지연시간 → wg widget |
| 5 | 내구성 → editorial rail card |
| 6 | 스케일링 → layout scaffold |
| 7 | 개발자 경험 → vt-comparison-cards |
| 8 | 비용 구조 → lede-note/source-note |
| 9 | 리스크 매트릭스 → wg widget |
| 10 | 결정 가이드 → editorial rail card |

## Visual risks

- 390px에서 h2 번호 pill 줄바꿈 금지
- rail 텍스트 좌측 접착 금지
- footer 좌측 붙음 금지
- 비정본 클래스 `template-card-head`/`source-preserve-static` 금지

## Stop condition

validate/quality/completion/render-audit 중 하나라도 실패하면 다음 모드로 넘어가지 않는다.
