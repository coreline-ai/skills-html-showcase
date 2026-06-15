# Eval Rubric

적용 범위: 이 루브릭은 0~5점 정성평가 도구다. 출시 가부는 `references/quality-gates.md`(출시 게이트)로 판정하고, 블로그 산출물의 점수화는 `references/blog-seo-system.md`의 Blog Quality Score(블로그 전용 100점)를 사용한다. 세 도구는 목적이 다르므로 함께 보완적으로 쓴다.

## Hard Fail 먼저 확인

아래 항목 중 하나라도 해당하면 점수화하지 않고 재작성한다.

- 선택 layout 파일의 정보 구조를 적용하지 않고 `layout-*` 클래스만 붙인 자유형 `<main>`이다.
- 같은 카드/리스트 패턴이 대부분 섹션을 차지해 모드별 특성이 보이지 않는다.
- “Generated example”, “전문 예제”, “예제 문서”, “기준 1/2/3”, `placeholder/TBD` 같은 임시 생성 문구가 남아 있다.
- 마지막 결론이 해당 주제의 판단·권고가 아니라 “이 결과물은 예제다”라는 자기 설명이다.
- 같은 모드의 기존 검수 예제보다 헤더·목차·섹션 밀도·템플릿 다양성·시각 완성도가 명백히 후퇴했다.

각 항목 0~5점.

| 항목 | 기준 |
|---|---|
| Mode Fit | 요청과 모드가 맞는가 |
| Layout Fit | 정보 구조가 목적에 맞는가 |
| Design DNA | 현재 editorial 테마가 유지되는가 |
| Content Depth | 설명/예시/주의/행동이 충분한가 |
| SEO/A11y | 메타/heading/모바일이 적절한가 |
| Factuality | 확인 필요를 단정하지 않는가 |
| Source Handling | 출처를 과하게 노출하지 않고 검증 가능하게 제공하는가 |
| Template Fidelity | 선택 모드의 layout/vt/wg 계약을 실제 정보 구조로 사용했는가 |
| Section Diversity | 카드·표·다이어그램·체크리스트·원문 발췌가 목적별로 배치되어 붕어빵 반복이 아닌가 |

총점 36점 이상이면 통과, 30~35점은 보완 후 통과, 29점 이하는 재작성. Hard Fail 항목이 있으면 총점과 무관하게 재작성.

## 기계 판독용 결과 스키마

이 루브릭의 평가 결과를 구조화해 남길 때는 `schemas/quality-report.schema.json`(Quality Report) 형식을 따른다. 스키마의 `mode`/`layout`은 모드·레이아웃 적합도, `rubric`은 위 9개 항목 점수, `total`은 총점, `verdict`은 통과/보완/재작성 판정, `gates`는 Hard Fail·출시 게이트 결과, `notes`는 보완 메모에 대응한다.
