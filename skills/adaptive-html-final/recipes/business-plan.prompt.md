# recipe: business_plan_html (mode 18)

사업계획서/지원서(정부지원·R&D·투자 피치·제안서)를 **증거 기반 단일-HTML 리포트**로 생성한다. 소스 계약: `references/business-plan-system.md`. layout: `assets/layouts/business-plan-report.html`(`layout-business-plan`). 무 JS·8테마·코어 CSS 인라인.

## 6단계 방법론
1. **공고/문서 타입 분석** — govt / R&D / pitch / proposal / internal 분기(`document_type_gate`). 공고 핵심 요건·평가 배점·제출 형식 요약(`notice_summary`).
2. **인터뷰/근거 수집** — 사실 인터뷰·1차 자료를 `interview_findings`·`research_evidence`로 정리. 모든 핵심 주장은 출처원장 행과 연결.
3. **business-core** — 문제→솔루션→제품→기술→시장→실행 사슬(`business_core`). `orginal_skill/bizplan/templates/business-core.yaml` 일반화.
4. **숫자/재무 모델** — TAM/SAM/SOM·가격·매출·원가·인력·일정을 **단일 number_registry(NR-NN)** 로 고정하고(`number_registry`), 재무모델·본문이 같은 NR-id를 참조(`market_finance_model`). 단위경제·산식 명시.
5. **위험·IP·매핑** — 리스크 매트릭스·IP/논문 노트(`risk_and_ip_paper_notes`), 공고 문항↔코어↔NR 매핑(`template_mapping`).
6. **자기검토 시뮬 + 제출 체크** — 4-평가자(행정/기술/사업/회의) **self-review 스코어카드**(`evaluator_scorecard`, 점수+근거 라벨, 외부검증/날조 아님) + 제출 전 체크리스트(`submission_checklist`) + 출처원장(`source_note`).

## 필수 계약 (custom gates)
- **증거 태그**: 핵심 수치/주장에 `[사실]`/`[추정]`/`[가정]`/`[목표]`/`[확인 필요]` 중 하나(`business_plan_evidence_tag_gate`).
- **숫자 레지스트리**: `NR-NN` ≥3, 본문/재무 정합(`business_plan_number_consistency_gate`).
- **출처원장**: in-HTML 정적표 — 발행처·기준시점·접근일·URL 컬럼(`business_plan_source_gate`).
- **평가자 스코어카드**: 행정/기술/사업/회의 4-평가자(`business_plan_status_gate`).

## 정본 컴포넌트
primary_vt `implementation-plan`(`.plan-grid`/`.milestone`) + quality-gate·risk-matrix·timeline·comparison-cards·process-swimlane. wg-16/11/13/18/14. 표는 `.tbl`/`.table-scroll`, 짧은 상태코드는 `.status-pill`. 신규 위젯/코어 CSS 없음(코어 해시 불변).

예제: `examples/18_business_plan_grantproof_core.html`.
