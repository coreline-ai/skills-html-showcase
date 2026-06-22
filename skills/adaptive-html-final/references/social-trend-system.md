# social_trend_dashboard 정보 구조·판단 기준

`social_trend_dashboard`는 소셜 신호 수집 결과를 **무 JS 정적 대시보드** 단일 HTML로 정본화하는 모드(priority 20, `layout-social-trend`). 핵심 불변식: **읽기 전용 수집**, **레코드 스키마 고정**, **URL dedupe/append**, **지표 정직성(없는 숫자 날조 금지)**, **무JS 차트(정적 표/카드 다운컨버트)**. 코어 CSS 무변경 → 해시 `a64604d0` 불변.

## records 스키마 (8필드)
| 필드 | 의미 |
|---|---|
| cat | 카테고리/분류 |
| author | 작성자/계정명 |
| handle | 핸들(@) |
| date | 게시일 |
| summary | 한 줄 요약 |
| url | 원문 링크(=dedupe 키) |
| views | 조회수(미확인=0/unknown) |
| likes | 반응수(미확인=0/unknown) |

`trend_record_schema_gate`는 ≥6 필드 정의를 강제. 스키마는 본문 `<pre>`/표로 고정한다.

## URL dedupe/append 정책
URL 정규화(쿼리·트래킹 파라미터 제거)→기존 레코드와 대조→**append**(신규) 또는 **update**(기존 갱신). 같은 url로 행을 무한 증식하지 않는다. `trend_url_dedupe_gate`.

## 지표 정직성
확인되지 않은 수치는 **0 또는 unknown**으로 두고, 추정/날조하지 않는다. metric_caveats 섹션에 "미확인=0/unknown, 추정 금지" caveat를 명시. `trend_metric_honesty_gate`.

## 읽기 전용 수집
좋아요·리포스트·팔로우·답글·DM·북마크 등 **상호작용을 0회 수행**한다(read-only). source_policy에 명시. `trend_read_only_gate`.

## 무JS 차트 (핵심 판정)
동작형 차트(`<canvas>`/chart.js) **금지**. 분포/비교는 **사전정렬 정적 표(.tbl)** + **comparison-cards(.cmp-card)**로 다운컨버트한다. `trend_no_js_chart_gate`가 canvas/chart.js를 차단하고 정적 차트 surface 존재를 확인한다. 허용 스크립트는 JSON-LD뿐.

## 11 required_blocks
scope_brief · source_policy · record_schema · collection_summary(수집 메트릭 타일=.mini-card) · category_distribution(comparison-cards 분포) · top_signals(사전정렬 .tbl) · evidence_cards · dedupe_append_policy · metric_caveats · verification_notes(quality-gate 자가검증) · next_actions.

## 시각 계약
primary_vt=`comparison-cards`(`.cmp-card`/`.cmp` 마커 ≥1). collection_summary는 card-grid `.mini-card` 타일, append/update는 timeline, 검증은 quality-gate. TOC는 구조적(직접 h2 ≥4면 toc-map 필요). 8테마·무 JS·body-icon(catalog 32종)·skip-link `#main` 유지. records는 예시 데이터(실데이터 아님)임을 source-note에 고지.
