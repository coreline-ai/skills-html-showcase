# recipe: strategy_os (AI 전략 운영체계 대시보드)

기술 신호(새 AI 모델·레포·기능·규제·경쟁사)를 **회사 전체의 행동으로 바꾸는 운영체계**를 단일·무 JS HTML 대시보드로 정본화한다. 원본 JS 인터랙티브 대시보드의 시각·콘텐츠 프레임워크를 **무-JS**로 재현. 코어 CSS 무변경(기존 vt-/wg- 재사용, `page` 폭) → 코어 해시 `a64604d0` 불변, 버전 5.10.6 유지(additive).

## 언제 쓰나 (triggers)
"AI 전략 대시보드", "회사 전략 운영체계", "부서별 관점 대시보드", "기술 신호 운영", "전략 OS", `/strategy-os`.

## 핵심 철학
기술 뉴스는 **목적이 아니라 재료**다. 신호가 어느 **전사 목표(North Star)**에 영향을 주는지 먼저 매핑하고 → 관련 부서만 움직여 → 실행 증거를 만들고 → 경영 판단까지 잇는다.

## 6블록 콘텐츠 프레임워크 (원본 구조 → 무-JS)
1. **north_star** — 전사 목표 5종(신규 매출·운영비 절감·실행 속도·제품 차별화·위험 최소화). 신호는 이 목표에 미치는 영향으로 해석.
2. **signal_scenarios** — 신호 시나리오 **≥4종**(새 모델·새 레포·새 기능·규제/보안·경쟁사). 원본의 JS 시나리오 스위처는 **comparison-cards/정적 표로 다운컨버트**(무-JS). 시나리오별 긴급도·요약·추천 결정 표기.
3. **department_perspectives** — 10개 부서를 신호별 **주관/협업/참고(lead/partner/inform)** 역할로 배정(모든 부서를 울리지 않음). 부서별 KPI·핵심 질문·산출물.
4. **execution_workflow** — 관심→검증→제품/고객 증거→경영 판단 순 실행 단계(process-swimlane 또는 steps). **decision_scorecard**: 전략 적합도·기술 가능성·고객 증거·위험 통제·실행 준비 5지표 + 현재 병목.
5. **decision_framework** — 경영 판단 4지선다: **전면 도입 / 조건부 진행 / 관찰 목록 / 보류·중단**. 모든 결정에 근거·담당·재검토 조건.
6. **operating_rhythm** — Daily(신호 수집)·Weekly(부서 라우팅)·Monthly(실행 리뷰)·Quarterly(전략·예산 재배분).

## 정본 컴포넌트 (신규 CSS 없음 · 코어 해시 불변)
- **레이아웃**: `assets/layouts/strategy-os-dashboard.html` — `<main id="main" class="page layout-strategy-os">`. **`page-wide` 금지**(theme.css 60rem 등재=코어 변경).
- **primary_vt**: `process-swimlane`(실행 파이프라인 5단계, `.swim`/`.lane-step`). 신호 비교는 comparison-cards, 부서는 card-grid `.mini-card`, 점수는 quality-gate, 리듬은 timeline.
- **무-JS 필수**: 원본 `<script>`(scenarioData·renderScenario)·`onclick`·`data-scenario`를 **이식 금지**(`strategy_no_js_switcher_gate`). 정적 비교 또는 radio `:checked`로만 재현. 허용 스크립트는 JSON-LD뿐.
- 8테마 라디오·body-icon(catalog 32종)·skip-link `#main`·코어 CSS byte-verbatim 인라인 + 해시 마커.

## custom gate 5종 (악성 fixture 선실패 → 정상 통과)
strategy_north_star_gate · strategy_signal_scenarios_gate(≥4) · strategy_department_roles_gate(주관/협업/참고) · strategy_decision_framework_gate(판단 ≥3) · strategy_no_js_switcher_gate(JS 훅 금지).
