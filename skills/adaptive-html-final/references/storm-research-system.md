# storm_research 정보 구조·판단 기준

`storm_research`는 STORM 다관점 리서치를 단일·무 JS HTML 리포트로 정본화하는 모드(priority 19, `layout-storm`). 핵심 불변식: **무출처 단언 금지**, **단일관점 금지**, **모순 보존**, **자기검증(peer-review) 표기**. 코어 CSS 무변경(기존 vt-/wg- 재사용) → 해시 `a64604d0` 불변.

## 5관점(souls) 어휘 — D-고정
| 관점 | 렌즈 | 주 질문 |
|---|---|---|
| 회의주의자(skeptic) | 반증·과장 차단 | "이 주장의 약한 고리는?" |
| 경제학자(economist) | 비용·인센티브·시장 | "누가 비용을 지불하고 누가 이득을 보나?" |
| 역사학자(historian) | 선례·반복 패턴 | "과거에 비슷한 시도는 어떻게 됐나?" |
| 학자/연구자(scholar) | 이론·증거 위계 | "근거의 질과 재현성은?" |
| 미래학자(futurist) | 2·3차 효과·시나리오 | "이대로면 3년 뒤 무엇이 달라지나?" |

`storm_soul_count_gate`는 ≥4 관점 표기를 강제(단일관점 회귀 차단).

## 출처 계약
- 모든 핵심 발견은 `[출처:URL]` 또는 source_map/provenance_footer 행으로 근거화. `storm_minimum_sources_gate`(URL/[출처] ≥5).
- provenance_footer는 **발행처·기준시점(observed_at)·접근일·URL** 컬럼 ≥3의 정적 출처 원장(`storm_provenance_gate`). 외부 xlsx 의존 대신 in-HTML 정적표.
- 신뢰도 라벨: `[사실]`/`[추정]`/`[확인 필요]` 또는 confidence high/medium/low ≥3건·≥2종(`storm_citation_label_gate`).

## 모순 지도 계약
contradiction_map은 **합의 지점**과 **모순/긴장/충돌 지점**을 함께 보여준다. 관점 충돌 쌍 ≥1. 모순을 임의로 해소하지 말고 보존한 채 synthesis_article로 종합한다(`storm_contradiction_gate`).

## peer-review 게이트
peer_review_gate는 verdict(통과/조건부/반려) + 점검 흔적을 남긴다: **source-bias-transfer**(출처의 편향이 결론으로 전이됐나), **over-association**(약한 상관을 인과로 과장했나). `storm_peer_review_gate`.

## 13 required_blocks 출처
generated_row(헤더 lens-strip) · method_notice(STORM 방법·한계 고지) · research_question · perspective_router(5관점 라우터) · soul_evidence_cards(관점별 근거 카드) · source_map(출처 지도 표) · contradiction_map · synthesis_article(종합) · peer_review_gate · confidence_badges · unresolved_questions(미해결 질문) · provenance_footer(출처 원장) · next_research_actions(후속 리서치 액션).

## 시각 계약
primary_vt=`process-swimlane`(4단계 파이프라인 레인, `.swim`/`.lane-step` 마커 ≥1). 관점 대조는 comparison-cards/wg-14, 미해결은 wg-18 트리아지, 검토 상태는 wg-11로 보강. TOC는 `toc-map storm-question-toc`. 8테마·무 JS(JSON-LD만 허용)·body-icon(catalog 32종)·skip-link `#main` 유지.
