# Business Plan System (mode 18 · business_plan_html)

`orginal_skill/bizplan`을 `adaptive-html-final`의 무-JS 단일-HTML 모드로 정본화한 계약. layout `layout-business-plan`(`assets/layouts/business-plan-report.html`), recipe `recipes/business-plan.prompt.md`, 예제 `examples/18_business_plan_grantproof_core.html`. 코어 CSS 무변경(implementation-plan vt + wg-16/11/13/18/14 재사용).

## 증거 태그 어휘 (D5, 고정)
모든 핵심 수치·주장은 다음 5종 중 하나를 동반한다: `[사실]`(검증된 출처) · `[추정]`(근거 있는 추정) · `[가정]`(전제) · `[목표]`(달성 목표치) · `[확인 필요]`(미검증). 외부 변형/영문 태그는 1차 범위 외. 게이트: `business_plan_evidence_tag_gate`.

## 단일 숫자 레지스트리 (D1)
TAM/SAM/SOM·가격·매출·원가·인력·일정 등 핵심 수치는 **`number_registry`** 블록에 `NR-NN` 식별자·레이블·값·단위·산식·출처ref·증거태그로 고정한다. 본문·`market_finance_model`은 같은 `NR-id`를 참조해 정합을 유지한다(레지스트리 ↔ 본문 diff, 정규식 스캔 아님). 게이트: `business_plan_number_consistency_gate`(NR-NN ≥3).

## 출처원장 (D3)
xlsx evidence-ledger 대신 **in-HTML 정적 테이블**: 컬럼 = 발행처(publisher)·기준시점(as-of)·접근일(access-date)·URL(+ 주장/근거 연결). 게이트: `business_plan_source_gate`(컬럼 ≥3).

## 평가자 스코어카드 (D4)
**행정/기술/사업/회의**(admin/tech/biz/skeptic) 4-평가자 **자기검토 시뮬레이션** — 점수는 외부검증이나 날조가 아니라 적대적 self-review이며 각 점수에 근거 라벨을 동반한다(bizplan 규칙#1 날조 금지 준수). 게이트: `business_plan_status_gate`.

## document_type 분기
공고 분석 결과로 govt / R&D / pitch / proposal / internal 중 하나를 선언(`document_type_gate`)해 평가 배점·필수 블록 강조를 조정한다.

## 13 required_blocks
generated_row · document_type_gate · notice_summary · interview_findings · research_evidence · business_core · number_registry · market_finance_model · template_mapping · risk_and_ip_paper_notes · evaluator_scorecard · submission_checklist · source_note. (출처: `docs/orginal-skill-new-mode-entry-extraction-20260621.md` §4.1 — 정본 13종은 스켈레톤 JSON 기준.)
