# 07 — Business Core 확정 (Gate 3·4 실행 프로토콜)

> **이 문서는 11~12단계 진입 시 Read 한다.** 입력은 `02-interview/`의 확정사실 + `04-research/`의 선별근거.
> 출력은 `05-business-core/`의 `business-core.yaml` + `evidence-ledger.xlsx` + `market-sizing.xlsx` + `financial-model.xlsx`.
> Gate 3(사업 논리 사슬)·Gate 4(숫자 일관성)를 여기서 통과시킨다.

---

## 0. 단일 출처 원칙 (왜 코어가 먼저인가)

`business-core.yaml`은 **모든 파생 문서(DOCX/HWPX/PDF/PPTX)의 유일한 진실원**이다. 초안·피치덱·요약서는 코어를 "읽어서" 만들 뿐, 코어를 우회해 수치를 직접 쓰지 않는다.

```text
interview(confirmed-facts) ┐
                           ├─► business-core.yaml ─► template-map ─► draft/* ─► final/*
research(source-index)     ┘         ▲
                                     └─ evidence-ledger / market-sizing / financial-model (수치 백업)
```

규칙:
- 코어의 한 값이 바뀌면 → 파생 4문서를 전부 다시 생성한다 (절대 규칙 #7). 손으로 한 곳만 고치면 숫자가 갈라진다.
- 코어에 없는 수치를 초안에 쓰면 안 된다. 필요하면 먼저 코어에 추가하고 태그·출처를 붙인다.
- 코어는 **확정된 것만** 담는다. 미확정은 값을 비우지 말고 `[확인 필요]`로 명시한다(빈 값 = 누락 사고).

---

## 1. 섹션별 입력 출처 매핑 (어디서 채우는가)

PRD §14 스키마의 각 섹션을 무엇으로 채우는지 고정한다. 출처가 없는 섹션은 채우지 않는다.

| business-core 섹션 | 1차 입력 (인터뷰) | 2차 입력 (리서치) | 기본 태그 |
|---|---|---|---|
| `project` | notice-summary / project.json | 공고 본문 | [사실] |
| `business` (정의·제목·목적·비전) | founder-insight, interview-summary | title-candidates | [사실]+[목표] |
| `customer` | confirmed-facts (구매자/사용자/수혜자) | market 세그먼트 | [사실]/[추정] |
| `problem` | interview 1·3단계 (빈도·심각도·대안) | 통계·동향 자료 | [사실]+[추정] |
| `solution` | interview 4단계 (핵심기능·작동방식) | — | [사실]/[목표] |
| `technology` | interview 4·5단계 (난제·단계·목표성능) | technology-readiness, 논문 | [사실]현상태/[목표]성능 |
| `market` (TAM/SAM/SOM) | — | market-sizing.xlsx (필수 산식) | [추정] |
| `competition` | interview 7단계 | competitors/, 포지셔닝 | [사실]+[추정] |
| `intellectual_property` | confirmed-facts (보유권리) | patents/, claim-chart | [사실]보유/[추정]위험 |
| `research` | — | papers/, research-gap | [사실] |
| `business_model` | interview 6단계 (가격·채널) | 경쟁 가격 벤치마크 | [추정]+[가정] |
| `traction` | confirmed-facts (매출·계약·PoC) | — | [사실]만 (임의 창작 금지) |
| `team` | interview 8단계 (역량·외주·결손) | — | [사실] |
| `execution` | interview 5·10단계 (마일스톤·위험) | — | [목표]+[가정] |
| `finance` | interview (필요자금·자금용도) | financial-model.xlsx | [추정]+[가정] |
| `impact` | interview 10단계 (고용·경제·사회) | 정책 부합 자료 | [목표]+[추정] |

원칙: **인터뷰가 사실의 출처, 리서치가 외부근거의 출처.** 둘 다 없는 칸은 `[확인 필요]`.

---

## 2. 증거 태그 규칙을 코어에 적용

절대 규칙 #2: 코어의 **모든 수치·주장**은 5개 태그 중 하나 + 근거 참조를 가진다.

```text
[사실] 확인된 정보 (인터뷰 확정 or 출처 있는 외부자료)
[추정] 근거+계산식으로 도출한 수치 (산식·출처 행 필수)
[가정] 아직 검증 안 한 전제
[목표] 앞으로 달성하려는 성과
[확인 필요] 추가 자료 필요
```

근거 참조 표기:
- 외부 출처 → `src#NN` (= source-index.xlsx NN행)
- 내부 증거 → `EL#NN` (= evidence-ledger.xlsx NN행)
- 인터뷰 확정 → `CF#NN` (= confirmed-facts.md NN항목)

### 코어 작성 예시 (YAML inline 태그)

```yaml
problem:
  core_problem: "중소 제조사는 설비 고장을 사후에 발견한다"   # [사실] CF#03
  frequency: "라인당 월 2~3회 비계획 정지"                  # [사실] CF#04
  severity: "1회 정지 시 평균 480만원 손실"                # [추정] src#12 산식: 시간당손실×평균정지시간
  current_alternatives: "수기 점검표 + 외주 정비"            # [사실] CF#05

market:
  tam: "국내 스마트팩토리 SW 1.2조원 (2026)"               # [사실] src#07
  sam: "예지정비 SW 1,800억원"                            # [추정] src#07,src#09 → market-sizing!B7
  som: "3년차 54억원 (SAM의 3%)"                          # [목표] market-sizing!B14

traction:
  contracts: "PoC 2건 (A사·B사), 유료계약 0건"             # [사실] CF#18 — 없는 계약 창작 금지

business_model:
  pricing: "월 90만원/라인 구독"                           # [가정] 경쟁사 대비 산정, 미검증
```

판단기준:
- 태그 없는 값 = 폐기 대상. 검증 스크립트는 태그 없는 수치를 잡아낸다.
- `[사실]` 인데 `src#`/`CF#`가 없으면 → 다운그레이드해 `[추정]` 또는 `[확인 필요]`.
- `traction`·`intellectual_property`의 `owned_*`는 **`[사실]`만 허용** (없으면 0/`[확인 필요]`). 절대 규칙 #1.

---

## 3. Gate 3 — 사업 논리 사슬 검증

**문제 → 해결책 → 제품 → 기술 → 시장 → 수익모델 → 실행 → 예산** 사이에 단절이 없어야 통과.

각 화살표마다 "앞 칸이 뒤 칸의 *전제*인가"를 묻는다. 단절 = 앞에서 말한 것이 뒤에서 안 받아지거나, 뒤가 앞 없이 등장하는 것.

### 연결 점검 체크리스트

- [ ] **문제→해결책**: `solution.core_mechanism`이 `problem.core_problem`의 원인을 직접 건드리는가? (증상 완화가 아니라 원인 제거)
- [ ] **해결책→제품**: `solution.key_features`가 전부 핵심 문제에 연결되는가? 문제와 무관한 기능 = 잘라낸다.
- [ ] **제품→기술**: `technology.core_technology`가 제품의 핵심 기능을 실제로 구현하는가? `technology.current_stage`로 지금 가능한 범위가 솔직히 표시됐는가?
- [ ] **기술→시장**: 이 기술로 만든 제품을 `customer.primary_customer`가 정말 사는가? `market.target_segment`가 customer와 동일 정의인가?
- [ ] **시장→수익모델**: `business_model.pricing`이 `customer`의 지불 의사·`competition` 가격과 모순 없는가?
- [ ] **수익모델→실행**: `execution.milestones`가 첫 매출/PoC까지의 경로를 담는가? 자금 없이 가능한 단계와 자금 필요 단계가 구분됐는가?
- [ ] **실행→예산**: `finance.use_of_funds`의 모든 항목이 `execution`의 마일스톤에 대응하는가? 마일스톤에 없는 지출 = 근거 부족.

### 판단기준

- 끊긴 화살표 1개라도 있으면 Gate 3 미통과 → 코어로 돌아가 해당 칸을 보강하거나, 연결되는 인터뷰/리서치를 추가.
- "왜?"를 3번 물어 답이 막히면 단절. 예: 가격 90만원 → 왜? → 경쟁사 대비 → 경쟁사 얼마? → `[확인 필요]` → **단절**(검증 전엔 통과 불가).
- 결과는 `05-business-core/logic-chain-check.md`에 8개 연결의 통과/단절을 기록.

---

## 4. Gate 4 — 숫자 일관성 검증

절대 규칙 #7. **같은 수치가 코어·엑셀·문서 어디서나 동일**해야 한다.

### 일관성 점검 대상 (PRD §19 Gate 4)

TAM/SAM/SOM · 가격 · 고객 수 · 매출 · 비용 · 인력 · 일정 · 사업비

### 교차 대조 절차

1. 코어에서 위 8종 수치를 추출 → `number-registry.md`에 "수치명 / 값 / 단위 / 태그 / 근거행"으로 1행씩.
2. 같은 수치가 `market-sizing.xlsx`·`financial-model.xlsx`·초안 `08-draft/*`·다이어그램에 등장하면 **값·단위가 코어와 일치**하는지 대조.
3. 파생 수치(매출 = 가격 × 고객수)는 **재계산해서 맞는지** 확인. SAM×점유율=SOM, 인력비=인원×단가 등.
4. 단위(원/만원/억원, 명/사/라인, 월/년)가 표마다 다르면 통일.

### 판단기준 (불일치 0이어야 통과)

| 검사 | 통과 기준 |
|---|---|
| 동일 수치 값 일치 | 코어 = 엑셀 = 초안 = 다이어그램 (오차 0) |
| 산식 재계산 | SOM=SAM×점유율, 매출=가격×고객수 등 자동 검산 일치 |
| 단위 통일 | 문서 전체 동일 단위 (혼용 시 환산 명기) |
| 일정 일관 | execution 마일스톤 ↔ 간트 다이어그램 ↔ finance 집행시점 동일 |

- 불일치 발견 시 **코어를 정본으로** 잡고 나머지를 코어에 맞춘다 (역방향 금지).
- 자동 점검: `scripts/validate_project.py`가 number-registry 대비 초안 텍스트의 숫자 토큰을 대조(완전 자동은 아니므로 위 절차로 보완).

---

## 5. evidence-ledger.xlsx — Claim ↔ 출처 ↔ 반영섹션

모든 핵심 주장의 추적표. source-index가 "자료 목록"이라면 ledger는 "주장 단위 연결표"다.

| 컬럼 | 설명 | 예시 |
|---|---|---|
| `ledger_id` | EL#NN | EL#12 |
| `claim` | 주장 1문장 | "예지정비로 비계획정지 40% 감소" |
| `claim_type` | 사실/추정/가정/목표/확인필요 | [추정] |
| `source_ref` | source-index 행 또는 CF#/인터뷰 | src#12, src#15 |
| `calc_or_quote` | 산식 또는 원문 인용 | "정지횟수×감소율, 논문 Table3" |
| `core_path` | 반영된 코어 경로 | problem.severity |
| `target_section` | 반영될 초안 섹션 | 문제인식 |
| `confidence` | 상/중/하 | 중 |
| `counter_evidence` | 반대근거 유무 | "B논문은 25%" (편향 방지) |

규칙: `counter_evidence` 컬럼을 비워두지 말 것 — 반대근거 탐색은 의무(절대 규칙·출처 편향 방지). 없으면 "탐색함, 미발견"이라도 기록.

---

## 6. market-sizing.xlsx — TAM/SAM/SOM 산식 (top-down + bottom-up 둘 다)

PRD §14 `market.calculation`의 근거 시트. **두 방식 모두 계산해 교차검증**한다(한 방식만이면 [확인 필요]).

### 시트 구조

| 행 | 항목 | 값 | 단위 | 산식 / 출처 | 태그 |
|---|---|---|---|---|---|
| top-down TAM | 전체 산업 규모 | 1.2조 | 원 | src#07 | [사실] |
| top-down SAM | 관련 세그먼트 | 1,800억 | 원 | TAM × 세그먼트비중 15% (src#09) | [추정] |
| top-down SOM | 획득 가능 | 54억 | 원 | SAM × 목표점유율 3% | [목표] |
| bottom-up 고객수 | 도달 가능 고객 | 2,000 | 사 | 산업통계 사업장수 (src#11) | [추정] |
| bottom-up ARPU | 고객당 연매출 | 1,080만 | 원 | 월90만×12 | [가정] |
| bottom-up SOM | 고객수×ARPU×침투 | 43~54억 | 원 | 2,000사×1,080만×2~2.5% | [추정] |
| 교차검증 | top-down vs bottom-up | 일치 여부 | — | 54억 ≈ 43~54억 → 정합 | — |

### 방법론 가이드

- **Top-down**: 큰 산업 수치(공신력 출처)에서 비중을 곱해 좁혀온다. `TAM → ×관련비중 → SAM → ×목표점유율 → SOM`. 비중·점유율마다 출처 또는 [가정] 태그.
- **Bottom-up**: 고객 단위에서 쌓아올린다. `도달가능 고객수 × ARPU × 현실적 침투율 = SOM`. 더 방어적이고 평가위원이 신뢰.
- **교차검증**: 두 SOM이 2배 이상 벌어지면 가정 재점검. 수렴하면 신뢰도↑.
- 모든 비중·점유율·침투율은 **출처 있는 [추정]이거나 명시적 [가정]**. 출처 없는 시장수치 창작 = 절대 규칙 #1·#3 위반.
- 결과 SOM은 코어 `market.som`과 동일해야 한다(Gate 4).

---

## 7. financial-model.xlsx — 매출·비용·인력·사업비 가정

PRD §14 `finance` + `business_model.unit_economics`의 백업. 모든 셀은 **가정값 + 태그**를 가진다.

### 시트 구성 (탭)

1. **assumptions** — 가격·고객증가·이탈률·단가 등 입력 가정 (전부 [추정]/[가정] 태그, 근거행)
2. **revenue** — `고객수(t) × ARPU × (1-이탈률)`로 분기/연 매출. 고객수는 SOM 도달 경로와 일치.
3. **cost** — 인건비·외주·인프라·마케팅. 인건비 = 인원 × 단가(시장 출처).
4. **headcount** — 직무별 인원·시점. `team`·`execution`과 일치.
5. **budget(사업비)** — 공고 사업비 항목(인건비/재료비/장비/외주/기타)별 배분. **공고 budget-rules 한도 준수**, 자부담 비율 반영.

### 컬럼 공통

`item / 값 / 단위 / 기간 / 태그 / 근거(src#·EL#·산식)`

판단기준:
- 매출·비용·인력 수치가 코어와 다르면 Gate 4 실패.
- 사업비 합계 = 공고 지원규모 + 자부담 (budget-rules.md와 대조).
- 낙관 단일 시나리오만 두지 말 것 — 최소 보수/기본 2케이스 권장(평가위원 회의적 질문 대비).

---

## 8. Gate 3·4 통과 체크리스트 (다음 단계 진입 전)

- [ ] `business-core.yaml`의 모든 값에 태그(5종 중 1) + 근거참조(src#/EL#/CF#)
- [ ] 빈 값 없음 (미확정은 `[확인 필요]`로 명시)
- [ ] `traction`·`owned_patents`는 [사실]만, 창작 0
- [ ] 논리 사슬 8연결 전부 통과 → `logic-chain-check.md`
- [ ] TAM/SAM/SOM 산식 top-down·bottom-up 둘 다 + 교차검증 → `market-sizing.xlsx`
- [ ] 8종 수치 number-registry 등재, 코어=엑셀=초안 일치 (불일치 0)
- [ ] evidence-ledger의 counter_evidence 컬럼 전 행 기입
- [ ] `project.json` status → `core_locked`, `gates_passed`에 `gate3`,`gate4` 추가
