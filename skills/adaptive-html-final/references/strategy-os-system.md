# strategy_os 정보 구조·판단 기준

`strategy_os`는 기술 신호를 전사 행동으로 바꾸는 운영체계를 단일·무 JS HTML 대시보드로 정본화하는 모드(priority 21, `layout-strategy-os`). 원본 JS 인터랙티브 대시보드(`company_ai_strategy_dashboard.html` — "기술 인텔리전스 운영체계")의 시각 8종·전략-OS 콘텐츠 프레임워크를 **무-JS**로 흡수한 것이다. 코어 CSS 무변경 → 해시 `a64604d0` 불변.

## 핵심 불변식
1. **기술보다 목표 우선** — 신호는 재료. North Star(전사 목표)에 미치는 영향으로 해석(`strategy_north_star_gate`).
2. **신호 유형별 분기** — 신호 ≥4종(새 모델/새 레포/새 기능/규제·보안/경쟁사), 유형마다 다른 부서·판단(`strategy_signal_scenarios_gate`).
3. **부서 역할 차등** — 모든 부서를 울리지 않고 신호별 주관/협업/참고(lead/partner/inform) 배정(`strategy_department_roles_gate`).
4. **경영 판단 4지선다** — 전면 도입/조건부 진행/관찰 목록/보류·중단. 근거·담당·재검토 조건 동반(`strategy_decision_framework_gate`).
5. **무-JS 재현** — 원본 JS 시나리오 시뮬레이터를 이식하지 않는다. 정적 비교(comparison-cards/표) 또는 radio `:checked`로만(`strategy_no_js_switcher_gate`).

## 전사 목표(North Star) 5종
신규 매출 · 운영비 절감 · 실행 속도 · 제품 차별화 · 위험 최소화. 신호의 가치는 이 목표 기여로 측정.

## 신호 시나리오 (원본 5종)
| 신호 | 긴급도 | 주관 부서 | 추천 결정(예) |
|---|---|---|---|
| 새 AI 모델 | 높음 | 제품·개발 | 재실험·추적 |
| 새 GitHub 레포 | 중간 | 개발·법무/보안 | 조건부 진행 |
| 새 플랫폼 기능 | 중간 | 제품 | 점진 도입 |
| 규제·보안 변화 | 높음 | 법무·보안 | 조건부 진행 |
| 경쟁사 발표 | 낮음 | 전략기획 | 관찰 목록 |

원본의 JS 스위처(`scenarioData`)는 **comparison-cards 정적 비교**로 다운컨버트한다.

## 10개 부서 관점
전략기획·제품·개발·영업·마케팅·운영·고객지원·재무·법무/보안·HR·교육. 각 부서: KPI · 핵심 질문 · 산출물. 신호별로 주관/협업/참고 역할이 바뀐다.

## 실행 워크플로 & 점수
관심→공식 정보 검증→기술 PoC→기능 가설→법무/재무 검토→고객 파일럿→경영 판단. decision_scorecard 5지표(전략 적합도·기술 가능성·고객 증거·위험 통제·실행 준비)로 의사결정 준비도를 정렬하고 **현재 병목**을 명시.

## 운영 리듬
Daily 신호 수집·검증 / Weekly 부서 라우팅 / Monthly 실행 포트폴리오 리뷰 / Quarterly 전략·예산 재배분. 일회성 문서가 아니라 반복 운영 루프.

## 시각 계약
primary_vt=`process-swimlane`(실행 파이프라인). 신호=comparison-cards, 부서=card-grid `.mini-card`(역할 배지), 점수=quality-gate/bar, 리듬=timeline. 8테마·무 JS·body-icon·skip-link `#main`. 본문 데이터는 예시이며 실제 회사 구조에 맞춰 교체함을 source-note에 고지.
