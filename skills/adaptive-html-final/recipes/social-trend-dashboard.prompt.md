# recipe: social_trend_dashboard (무JS 소셜 트렌드 대시보드)

소셜 신호(X/트위터·커뮤니티 등) 수집 결과를 **무 JS 정적 대시보드** 단일 HTML로 정본화한다. 코어 CSS 무변경(기존 vt comparison-cards·정적 .tbl·card-grid 재사용, `page` 폭) → 코어 해시 `a64604d0` 불변, 버전 5.10.6 유지(additive).

## 언제 쓰나 (triggers)
"소셜 트렌드", "X/트위터 트렌드 대시보드", "AI 도구 시장 신호", "records.json 대시보드", "무JS 차트 트렌드 리포트".

## 수집 5단계
1. **scope** — 수집 범위·기간·플랫폼·키워드를 고정(scope_brief).
2. **source policy** — 경로·접근 한계·읽기 전용 원칙(source_policy). **상호작용(좋아요/리포스트/팔로우/답글) 0회 — read-only 수집만**(`trend_read_only_gate`).
3. **record schema** — `records.json` 8필드(cat·author·handle·date·summary·url·views·likes) 정규화(`trend_record_schema_gate`). 표/코드블록으로 스키마 고정.
4. **dedupe/append** — URL 정규화→대조→**append/update**(행 무한 증식 금지). `trend_url_dedupe_gate`.
5. **사전분류·사전정렬 정적 렌더** — 분포/비교는 동작형 차트 금지(`trend_no_js_chart_gate`), **사전정렬 정적 표(.tbl) + comparison-cards(.cmp-card)**로 다운컨버트. 미확인 지표는 **0/unknown**으로 두고 추정 금지 caveat 표기(`trend_metric_honesty_gate`).

## 필수 블록 (11)
scope_brief · source_policy · record_schema · collection_summary · category_distribution · top_signals · evidence_cards · dedupe_append_policy · metric_caveats · verification_notes · next_actions.

## 정본 컴포넌트 (신규 CSS 없음 · 코어 해시 불변)
- **레이아웃**: `assets/layouts/social-trend-dashboard.html` — `<main id="main" class="page layout-social-trend">`. **`page-wide` 금지**(theme.css 60rem 등재=코어 변경).
- **primary_vt**: `comparison-cards`(마커 `.cmp-card`/`.cmp`) — 카테고리/신호 분포 비교(막대 차트 다운컨버트). card-grid는 vt가 아닌 본문 컴포넌트(`.mini-card`)로 메트릭 타일에 사용.
- **vt 후순위**: timeline(append/update 파이프라인), risk-matrix, quality-gate(수집 자가검증).
- **wg**: wg-11(수집 상태판)·wg-13(신호 흐름)·wg-18(미해결 트리아지)·wg-14(기능 설명)·wg-02(시안 비교).
- 표=사전정렬 `.tbl`/`.table-scroll`+caption, 상태/건수=`.status-pill`, dedupe 키=`.term`, 8테마 라디오, 코어 CSS byte-verbatim 인라인 + 해시 마커. 무 JS(`<canvas>`/chart.js 금지, JSON-LD만 허용).

## custom gate 5종 (악성 fixture 선실패 → 정상 통과)
trend_record_schema_gate(8필드 ≥6) · trend_url_dedupe_gate(dedupe+append) · trend_metric_honesty_gate(0/unknown+추정금지 caveat) · trend_read_only_gate(읽기전용+상호작용 0) · trend_no_js_chart_gate(canvas/chart.js 금지 + 정적 차트 surface).

## 산출 시
records는 본문 내 `<pre>` 예시(실데이터 아님 — source-note에 "예시 데이터" 고지). output 산출물은 sources/profile.json(auto)·css-integrity·render-audit를 남긴다.
