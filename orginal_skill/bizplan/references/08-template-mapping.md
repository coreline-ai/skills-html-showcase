# 08 — 공식 서식 분석 + 매핑 (Gate 6 준비)

> **이 문서는 13~14단계 진입 시 Read 한다.** 입력은 `00-source/templates/`의 공식 서식 + `05-business-core/business-core.yaml`.
> 출력은 `06-template-design/`의 `template-structure.yaml` · `template-map.yaml` · `section-outline.md` · `section-evidence-map.md` · `section-visual-map.md`.
> 여기서 Gate 6(서식 준수)을 *준비*하고, 실제 통과는 Final 단계 렌더링 검사에서 확정한다.

---

## 0. 대원칙 — 서식은 손대지 않는다

PRD §29 "공식 서식 손상 방지". 공식 서식은 **평가 통과의 형식 요건**이다. AI가 임의로 바꾸면 탈락한다.

- **원본 보존**: `00-source/templates/`의 원본 파일은 절대 수정하지 않는다. 분석은 읽기 전용.
- **목차·입력위치 그대로**: 공식 항목 순서·제목·표 위치·셀병합을 임의로 재배열하지 않는다. 우리가 만드는 건 "각 칸에 들어갈 내용"이지 "칸 자체"가 아니다.
- **삭제 금지 영역 식별**: 안내문구·서명란·법적 고지 등은 건드리지 않는다. 어디가 입력칸이고 어디가 고정영역인지 먼저 구분한다.
- 서식 변형이 불가피하면(표 깨짐 등) Final에서 `format-damage-report.md`로 보고하고 삽입 가이드를 대체 제공.

---

## 0.1 양식 충실 추종 원칙 (최우선 — 다른 모든 골격보다 앞선다)

> **공고가 양식 파일(.hwp/.hwpx/.docx/.xlsx)을 제공하면, 그 양식의 목차·항목 번호·표 구조를 글자 그대로 따른다. 임의 재구성·재배열·통폐합은 탈락 사유다.** 표준 골격(§8~9)은 *양식이 없을 때만* 쓰는 fallback이다.

### 결정 순서 (BLOCKING — 다른 작업 전에 먼저 판정)

```text
공고에 양식 파일이 첨부되어 있는가?
├─ 예 → 양식을 그대로 추종한다 (FOLLOW_TEMPLATE)
│        · 양식의 목차·번호체계·표 컬럼을 §1~3대로 추출
│        · §8~9 표준 골격은 참고만, 양식이 충돌하면 양식이 이긴다
│        · 양식에 없는 우리 콘텐츠라도 양식 칸 밖에 새 절을 만들지 않는다
└─ 아니오 → 표준 골격을 사용한다 (USE_STANDARD)
            · 문서 유형 판정(PSST / R&D / 투자덱 / 제안서)
            · §8(PSST) 또는 §9(R&D) 또는 §6(자유형식) 골격 사용
            · 사용자에게 골격 확정받은 뒤 template-structure.yaml에 기록
```

`template-structure.yaml`의 `meta` 블록에 이 판정을 명시한다:

```yaml
meta:
  template_mode: FOLLOW_TEMPLATE   # FOLLOW_TEMPLATE | USE_STANDARD
  source_file: "00-source/templates/사업계획서_양식.hwpx"   # USE_STANDARD면 null
  standard_skeleton: null          # USE_STANDARD일 때만 "PSST" / "R&D-IRIS" / "pitch-deck" / "proposal"
```

### 양식 충실 추종 시 7대 준수 사항

| # | 준수 사항 | 위반 예시 (탈락 위험) |
|---|---|---|
| 1 | **항목 번호 글자 그대로** — `1-1`, `가.`, `1)` 체계를 양식과 1:1 일치 | 양식의 `1-1·1-2`를 `1.1·1.2`로 바꿈 |
| 2 | **항목 제목 글자 그대로** — "문제인식(Problem)"을 "문제 정의" 등으로 의역 금지 | 제목 윤문·축약 |
| 3 | **순서 보존** — 양식 순서대로. 우리가 강조하고 싶다고 앞으로 당기지 않음 | 팀 항목을 문제 앞으로 이동 |
| 4 | **표 구조 보존** — 양식 표의 행·열·셀병합 그대로. 컬럼 추가·삭제 금지 | 양식 일반현황 표에 임의 컬럼 추가 |
| 5 | **요약표 위치 보존** — 본문 앞 요약표(일반현황·아이템개요)는 양식이 둔 위치 그대로 | 요약표를 본문 뒤로 이동 |
| 6 | **안내문구 처리** — 회색 예시문은 채워진 내용으로 대체하되 항목 자체는 유지 | 안내문구가 있는 항목을 통째 삭제 |
| 7 | **분량 제한 준수** — 양식이 항목별 페이지/글자수를 정하면 그 안에서 작성 | 한 항목이 한도 2배로 넘침 |

### 양식이 표준 골격과 어긋날 때

- 양식이 PSST 4대 항목과 다른 번호·제목을 쓰면 → **양식을 따른다.** §8 PSST 표는 "이 항목이 답해야 할 평가자 질문"을 참고하는 용도로만 사용한다.
- 양식에 표준 골격의 어떤 표가 없으면 → 억지로 끼워넣지 않는다. 단, 그 데이터가 평가에 유리하면 양식 안의 가장 가까운 항목 본문에 표로 삽입한다(새 절 신설 X).
- 양식에 표준 골격에 없는 항목이 있으면 → 그 항목을 채운다. business-core에 해당 근거가 없으면 07단계로 돌아가 채우거나 `[확인 필요]`.

### template-map.yaml에 추적 의무

양식 추종 모드에서는 **모든 양식 항목이 매핑되어야 한다**(누락 0). 매핑표에 `official_id`(양식의 번호)와 `official_title`(양식의 제목)을 원문 그대로 기록해 Gate 6에서 1:1 대조한다.

---

## 1. 공식 서식 분석 대상 12개

PRD §15. 서식 파일(HWP/HWPX/DOCX/PDF)을 읽고 아래 12항목을 추출해 `template-structure.yaml`로 골격화한다.

| # | 분석 항목 | 추출 내용 | 왜 중요한가 |
|---|---|---|---|
| 1 | 제목 계층 | 대/중/소제목 번호체계(1. → 가. → 1)) | 목차 누락·순서 오류 방지 |
| 2 | 목차 | 공식 항목 전체 목록·순서 | Gate 6 "목차 누락 없음" |
| 3 | 입력 표 | 표별 행·열 정의, 입력 셀 위치 | 어디에 무엇을 쓰는지 |
| 4 | 셀 병합 | 병합 범위 | 변형 시 표 깨짐 |
| 5 | 안내 문구 | "○○○를 기재", 예시문 | 삭제 금지·작성 지침 |
| 6 | 삭제 금지 영역 | 고정 텍스트·서식 영역 | 임의 수정 금지 |
| 7 | 페이지 수 | 항목별/전체 분량 제한 | "지정 분량 준수" |
| 8 | 폰트 | 지정 글꼴 | 형식 요건 |
| 9 | 글자 크기 | 본문/제목 pt | 형식 요건 |
| 10 | 여백 | 상하좌우 mm | 형식 요건 |
| 11 | 서명 영역 | 대표자 서명·날인 위치 | 누락 시 반려 |
| 12 | 첨부 목록 | 필수 첨부서류 리스트 | required-documents와 대조 |

판단기준: 12항목 중 서식에 명시된 것은 전부 추출. 명시 안 된 항목(예: 폰트 미지정)은 `null` + "미지정"으로 기록(추측 금지).

---

## 2. template-structure.yaml — 서식 골격 추출

서식 원본의 **구조만** YAML로 뽑는다(내용 아님). 원본은 그대로 두고 이 YAML이 작업 기준이 된다.

```yaml
meta:
  template_mode: FOLLOW_TEMPLATE   # FOLLOW_TEMPLATE | USE_STANDARD (§0.1)
  standard_skeleton: null          # USE_STANDARD일 때만: "PSST" / "R&D-IRIS" / "pitch-deck" / "proposal"
  source_file: "00-source/templates/사업계획서_양식.hwpx"   # USE_STANDARD면 null
  format: hwpx              # docx / pdf / hwpx
  total_page_limit: 15      # null = 미지정
  font: "맑은 고딕"          # null = 미지정
  font_size_pt: 10
  margins_mm: { top: 20, bottom: 20, left: 20, right: 20 }
  do_not_edit_zones:        # 삭제 금지 영역
    - "표지 상단 기관 로고/안내문"
    - "각 항목 안내문구(회색 글씨)"
  signature_block: "마지막 장 대표자 서명·날인란"

summary_tables:             # 본문 앞 고정 요약표 (PSST 양식은 2개 필수 — §8)
  - name: "일반현황"
    position: "본문 앞 (표지 다음)"
    columns: ["기관명", "아이템명", "업종", "신청자", "설립예정지"]
  - name: "창업아이템 개요(요약)"
    position: "일반현황 다음"
    columns: ["아이템 소개", "차별성", "목표시장", "이미지"]

sections:                   # 공식 목차 = 입력 위치 (순서 보존)
  - id: "1"                 # 양식 번호 글자 그대로 (1, 1-1, 가. ...)
    title: "문제 인식 (Problem)"   # 양식 제목 글자 그대로 (의역 금지)
    page_limit: 3
    input_type: "서술+표"
    guide_text: "창업 아이템의 개발 동기·필요성을 기재"
    subsections:            # 세부 항목 번호도 양식 그대로 보존
      - { id: "1-1", title: "창업 아이템 배경 및 필요성" }
      - { id: "1-2", title: "창업 아이템 목표시장(고객) 현황 분석" }
    tables:
      - name: "시장 현황표"
        columns: ["구분", "현황", "출처"]
        merged_cells: ["A1:A2"]
  - id: "2"
    title: "실현 가능성 (Solution)"
    page_limit: 4
    input_type: "서술+구성도"
    guide_text: "..."

required_attachments:        # 첨부 목록 (required-documents.md와 교차검증)
  - "사업자등록증"
  - "대표자 이력서"
```

규칙:
- `template_mode`를 먼저 채운다(§0.1). `FOLLOW_TEMPLATE`면 `sections`는 양식에서 추출, `USE_STANDARD`면 §8/§9 표준 골격을 그대로 복사한 뒤 `standard_skeleton`에 어느 골격인지 기록.
- `sections` 순서·`title`·`id`·`subsections[].id`는 원본 그대로. `guide_text`(안내문구)는 작성 지침이므로 보존하되 최종 문서에서는 채워진 내용으로 대체.
- `summary_tables`는 PSST 양식의 핵심(§8). 양식에 요약표가 있으면 그대로, 없고 USE_STANDARD면 §8 2종을 넣는다.

---

## 3. template-map.yaml — 공식항목 ↔ 코어 ↔ 근거 ↔ 표현

각 공식 항목을 `business-core.yaml`의 어느 경로에서, 어떤 근거로, 어떻게 표현할지 1:1 매핑. PRD §15 매핑표를 항목 수만큼 확장.

```yaml
mappings:
  - official_id: "1-1"                    # 양식 번호 (FOLLOW_TEMPLATE 필수)
    official_title: "창업 아이템 배경 및 필요성"   # 양식 제목 글자 그대로
    evaluator_question: "이 문제는 실재하고 시급한가? 객관 수치로 증명되는가?"
    core_path: [problem, customer]
    evidence: [src#12, CF#03, EL#08]      # source-index / confirmed-facts / evidence-ledger
    representation: "텍스트 + 문제구조도(As-Is/To-Be) + 시장현황표"
    required_tables: ["시장현황표"]        # §10 카탈로그 표 ID
    page_limit: 3
  - official_id: "1-2"
    official_title: "창업 아이템 목표시장(고객) 현황 분석"
    evaluator_question: "타깃 고객이 명확하고 시장 규모는 출처 있는가?"
    core_path: [market, customer]
    evidence: [market-sizing.xlsx, src#07]
    representation: "TAM/SAM/SOM 동심원 + 목표시장 정의표"
    required_tables: ["시장규모표"]
  - official_id: "2-1"
    official_title: "창업 아이템 현황(준비 정도)"
    evaluator_question: "지금 어디까지 만들었나? 실행 흔적이 있는가?"
    core_path: [solution, technology]
    evidence: [CF#10, src#21]             # 프로토타입·논문
    representation: "MVP 구성도 + 흐름도 + 기능표"
  - official_id: "2-2"
    official_title: "창업 아이템 실현 및 구체화 방안"
    evaluator_question: "경쟁사 대비 구조적 우위가 있는가?"
    core_path: [solution, competitors]
    evidence: [src#21, EL#11]
    representation: "경쟁 비교표(측정기준+근거 컬럼) + 포지셔닝맵"
  - official_id: "3-3"
    official_title: "사업 추진 일정 및 자금 운용 계획"
    evidence: [financial-model.xlsx, budget-rules.md]
    representation: "추진일정 간트 + 자금소요·조달표 + 사업비 명세표"
    required_tables: ["추진일정간트", "자금소요조달표", "사업비명세표"]
  - official_id: "4-1"
    official_title: "대표자 및 팀 역량"
    core_path: [team]
    evidence: [CF#22]
    representation: "팀 역할표(R&R) + 조직도 + 채용계획"
```

판단기준:
- **FOLLOW_TEMPLATE이면 모든 양식 항목이 매핑되어야 한다(누락 0).** `official_id`+`official_title`을 양식 그대로 적어 Gate 6에서 1:1 대조한다.
- `core_path`가 비면 → 해당 코어 칸이 미완. 07단계로 돌아간다.
- `required_tables`는 §10 표 카탈로그의 ID를 적어 어느 표가 어느 항목에 들어가는지 추적한다.
- 표준 매핑 출발점(PRD §15): 문제인식→problem / 실현가능성→solution,technology / 성장전략→market,business_model / 팀→team / 사업비→finance. 공고별 항목명에 맞춰 변주.

---

## 4. section-outline.md / section-evidence-map.md / section-visual-map.md

template-map을 세 관점으로 분해해 초안 작성(16단계)에 넘긴다.

### section-outline.md — 목차 + 핵심 메시지
```markdown
## 1. 문제 인식
- key_message: "중소 제조사는 설비 고장을 사후 발견해 라인당 월 480만원 손실"  # 한 문장 답
- subsections: [문제 정의, 발생 빈도·심각도, 현재 대안의 한계]
- page_limit: 3
## 2. 실현 가능성
- key_message: "..."
```

### section-evidence-map.md — 섹션별 근거 배치
```markdown
## 1. 문제 인식
| 주장 | 근거 | 태그 |
|---|---|---|
| 월 480만원 손실 | src#12 (산식) | [추정] |
| 사후 발견 관행 | CF#03 | [사실] |
```
규칙: 각 섹션의 핵심 주장마다 근거행 1개 이상. 출처 없는 핵심통계 = Gate 통과 불가(절대 규칙 #3).

### section-visual-map.md — 섹션별 시각자료 계획
```markdown
## 1. 문제 인식
- diagram: 문제구조도 (problem-tree) → 07-diagrams/
- table: 시장현황표
## 4. 성장 전략
- chart: TAM/SAM/SOM 동심원 + 매출 추이 막대
- diagram: 경쟁 포지셔닝 2x2
```
규칙: 각 시각자료는 `references/09-diagrams.md`의 21종 + 포맷 규칙을 따른다. 실데이터/개념 구분 표시.

---

## 5. §17.1 섹션 작성 YAML 스키마

각 섹션 초안을 작성할 때 채우는 단일 스키마. `08-draft/<section>.md` 상단 frontmatter로 둔다.

```yaml
section:
  official_id:         # 공식 서식의 항목 번호 (FOLLOW_TEMPLATE이면 양식 그대로, 예 "1-1")
  official_title:      # 공식 서식의 항목명 (template-structure와 일치 — 의역 금지)
  evaluator_question:  # 이 항목에서 평가자가 확인하려는 질문
  key_message:         # 한 문장 핵심 답변
  supporting_claims:   # 핵심 메시지를 받치는 주장 목록 (각 태그 부착)
  evidence:            # src#/EL#/CF# 근거 참조 목록
  quantitative_goals:  # 정량목표 (§12 공식: 활동→결과→숫자+조건+측정방법+달성시기+비교근거)
  qualitative_goals:   # 정성목표 (§12 공식: 측정 가능한 상태 변화)
  text:                # 서술식 본문 (개요)
  tables:              # 삽입 표 목록 (제목·단위·기준일·출처 — §10 카탈로그 ID 병기)
  charts:              # 그래프 목록
  diagrams:            # 다이어그램 참조 (07-diagrams/images/*)
  images:              # 실사/캡처 이미지
  source_notes:        # 출처 각주
  missing_items:       # [확인 필요] 잔존 항목 (제출 전 사용자 확인)
```

판단기준:
- `evaluator_question` 없이 쓰지 않는다 — 평가자가 안 묻는 내용은 분량 낭비.
- `key_message`는 정확히 한 문장. 두 주장이면 섹션을 쪼갠다.
- `missing_items`가 비어야 이상적. 남으면 사용자 확인 후 채우거나 `[확인 필요]`로 명시 제출.
- `evidence`의 모든 참조는 실재해야(source-index/ledger에 행 존재).

---

## 6. 공고에 정해진 서식이 없을 때 — 기본 목차 골격

투자덱·내부 신사업·자유형식은 공식 서식이 없다. 이때 문서 유형별 표준 목차를 제안하고 사용자 확정 후 진행(PRD §18 중점과 일치).

> **창업지원사업·R&D 과제는 양식이 없을 때 §8(창업 PSST) / §9(R&D IRIS) 표준 골격을 쓴다.** 아래 6번은 투자덱·내부 신사업·제안서용 간이 목차다.

### 투자 피치덱 (PPTX)
```text
1. 문제 (Problem) — 크고 시급한 고통
2. 해결책 (Solution) — 독특한 접근
3. 왜 지금인가 (Why now)
4. 제품 (Product / 데모)
5. 시장 규모 (TAM/SAM/SOM)
6. 비즈니스 모델
7. 트랙션 / 성장지표
8. 경쟁 우위
9. 팀
10. 투자금 사용처 (Ask & Use of funds)
```

### 내부 신사업 계획서 (DOCX)
```text
1. 배경·문제 정의
2. 사업 개요·목표
3. 시장·고객 분석
4. 솔루션·제품 구성
5. 비즈니스 모델·수익성
6. 경쟁·차별성
7. 실행 로드맵·일정
8. 조직·필요 자원
9. 투자/예산 계획
10. 기대효과·리스크
```

### 기업·공공 제안서 (DOCX)
```text
1. 고객 현황·문제 이해
2. 제안 범위·목표
3. 수행 방법·방법론
4. 추진 체계·역할분담
5. 일정 계획
6. 품질·리스크 관리
7. 비용 산정
8. 유사 수행 실적
```

규칙: 기본 골격도 `template-structure.yaml`로 똑같이 기록해 이후 단계가 동일하게 작동하게 한다. 자유형식이라도 코어→매핑→초안 흐름은 변하지 않는다.

---

## 7. Gate 6 준비 체크리스트 (초안 단계 진입 전)

- [ ] `template-structure.yaml`에 `template_mode` 판정(FOLLOW_TEMPLATE / USE_STANDARD) 명시 (§0.1)
- [ ] FOLLOW_TEMPLATE이면: 항목 번호·제목·순서·표 구조를 양식 그대로 보존(의역·재배열 0)
- [ ] USE_STANDARD이면: `standard_skeleton`에 골격 종류 기록 + §8/§9 골격 그대로 복사
- [ ] `template-structure.yaml`에 12항목 + 공식 목차 순서 보존 + `subsections[].id`
- [ ] 본문 앞 요약표(PSST 2종 §8 / 양식 제공분) `summary_tables`에 기록
- [ ] 삭제 금지 영역·서명란·페이지 한도·폰트/크기/여백 기록(미지정은 "미지정")
- [ ] `template-map.yaml`에 모든 공식 항목 ↔ `official_id` ↔ core_path ↔ evidence ↔ representation ↔ required_tables
- [ ] 매핑 안 된 공식 항목 0개 (FOLLOW_TEMPLATE이면 양식 항목 100% 매핑)
- [ ] §10 필수 표/도표 11종 중 문서 유형에 해당하는 표가 어느 항목에 들어가는지 `required_tables`로 추적
- [ ] 정량/정성 목표 항목은 §12 공식(활동→결과→숫자+조건+측정+시기+비교근거)으로 작성
- [ ] section-outline / evidence-map / visual-map 3종 생성, 섹션마다 key_message + 근거 + 시각계획
- [ ] required_attachments ↔ `01-notice-analysis/required-documents.md` 대조 완료
- [ ] 공고 서식 없으면 §8/§9/§6 골격을 사용자 확정 후 structure.yaml에 기록
- [ ] `project.json` outputs에 06-template-design 산출물 경로 등재

---

## 8. 창업 PSST 표준 골격 (양식 없을 때의 기본 — `standard_skeleton: "PSST"`)

> 출처: `docs/improvement-research-2026-06-18.md` §A. 2018 중기부 표준. 예비/초기/도약 패키지 공통. **양식이 제공되면 §0.1대로 양식이 이긴다.**

### 8.1 본문 앞 요약표 2개 (고정 — 본문 전에 배치)

**표 ① 일반현황** (`summary-general`)

| 기관(사업자)명 | 아이템명 | 업종(주력 제품·서비스) | 신청자(대표자) | 설립(예정)지 |
|---|---|---|---|---|
| [확인 필요] | … | … | … | … |

**표 ② 창업아이템 개요(요약)** (`summary-item`)

| 구분 | 내용 |
|---|---|
| 아이템 소개 | 핵심 기능·소비자·사용처를 1~2문장 |
| 차별성 | 경쟁 대비 차별점 + 현재 개발 단계 |
| 목표시장 | 진입 목표 시장(고객·규모) |
| 이미지 | 제품·서비스 대표 이미지/캡처 |

> 요약표는 평가자가 가장 먼저 보는 30초 인상이다. 본문에 쓴 핵심 수치와 **반드시 일치**(7대 규칙 #7).

### 8.2 PSST 4대 항목 세부 (1-1 ~ 4-2)

| 번호 | 항목 | 평가자가 확인하는 질문 | 들어갈 표/도식 | core_path |
|---|---|---|---|---|
| **1-1** | 문제인식: 배경·필요성 | 이 문제는 실재·시급한가? **객관 수치·인터뷰 증빙**으로 증명되나? (As-Is/To-Be) | 문제구조도, 시장현황표 | problem |
| **1-2** | 문제인식: 목표시장(고객) 현황 분석 | 타깃 고객이 명확하고 시장규모는 출처 있나? | TAM/SAM/SOM 동심원, 목표시장 정의표 | market, customer |
| **2-1** | 실현가능성: 현황(준비 정도) | 지금 어디까지 만들었나? **실행 흔적**(MVP·설계·외주견적)이 있나? | MVP 구성도, 시스템 흐름도, 기능표 | solution, technology |
| **2-2** | 실현가능성: 실현·구체화 방안 | 경쟁사 대비 **구조적 우위**가 있나? 진입장벽은? | 경쟁 비교표(측정기준+근거), 포지셔닝맵, SWOT | solution, competitors |
| **3-1** | 성장전략: 사업모델(BM) | 어떻게 돈을 버나? (수익모델 1문장) | 비즈니스 모델 도식, 수익구조표 | business_model |
| **3-2** | 성장전략: 사업화 추진전략 | 어떻게 시장에 진입·확산하나? CAC/채널은? | 채널표, 진입전략 매트릭스, CAC/LTV표 | business_model, market |
| **3-3** | 성장전략: 추진일정+자금운용 | 일정·예산이 현실적이고 정합적인가? | 추진일정 간트, 자금소요·조달표, 사업비 명세표 | execution, finance |
| **4-1** | 팀구성: 대표·팀 역량 | 이 팀이 해낼 수 있나? (경력·R&R·채용) | 팀 역할표(R&R), 조직도, 채용계획표 | team |
| **4-2** | 팀구성: 중장기 사회적가치 | 고용·지역·ESG 등 사회적 기여는? | 고용계획표, 사회적가치 지표표 | team, impact |

> 1번(문제)·2번(해결)은 **현장 증거**(인터뷰 N명·사진·사전예약·전환데이터)와 **실행 흔적**으로 정량 입증한다. 아이디어 단계 머묾·시장규모 무출처·수익모델 모호·매출 과도추정은 탈락 공통결함(연구노트 §C).

---

## 9. R&D 연구개발계획서 표준 골격 (`standard_skeleton: "R&D-IRIS"`)

> 출처: 연구노트 §A. IRIS 표준서식 7대 항목. **양식이 제공되면 §0.1대로 양식이 이긴다.**

### 9.1 7대 항목

| 번호 | 항목 | 핵심 내용 | 들어갈 표/도식 |
|---|---|---|---|
| **1** | 개발 필요성 | 국내외 기술·시장 현황, 정책 부합성 | 기술동향 비교표, 정책 부합 매트릭스 |
| **2** | 개발 목표·내용 | 최종/단계 목표 + **평가기준 표(정량목표)** + 개발 내용·방법 + 수행일정 | **평가기준 표**, 추진일정 매트릭스 |
| **3** | 추진전략·체계 | 추진 방법·전략 + **추진체계도** | 추진체계도, 추진전략 매트릭스 |
| **4** | 연구역량 | 수행기관·연구팀 역량 + **연구팀 편성표** | 연구팀 편성표, 인프라·장비표 |
| **5** | 활용방안·기대효과 | 과학기술적·경제산업적·사회적 효과 | 기대효과 3분류표 |
| **6** | 사업화 전략 | 시장규모·투자·해외진출·고용 | TAM/SAM/SOM, 사업화 로드맵 |
| **7** | 안전·보안 | 연구실 안전·기술보안·생명윤리 | 안전관리 계획표 |
| 별첨 | 사업비 사용계획 | 직접비+간접비 명세 | **사업비 명세표** |

### 9.2 평가기준 표 (항목 2 내부 — 정성/정량 5개·가중치 합 100)

> R&D 평가의 핵심. 각 평가지표는 §12 정량목표 공식으로 작성하고 **세계최고수준 비교근거**를 필수로 단다.

| 평가지표(정성/정량) | 단위 | 측정방법(조건·환경) | 달성목표(최종) | 가중치(%) | 세계최고수준 비교근거 |
|---|---|---|---|---|---|
| 예: 평균 이동거리(정량) | m | 무풍 실내, 0.5m 높이, 10회 평균 | ≥100 | 30 | MIT 동일환경 60m (src#NN) |
| 예: 에너지 효율(정량) | % | KS 표준 측정 | ≥85 | 25 | 국내 최고 78% (src#NN) |
| 예: 응답시간(정량) | ms | 부하 1000TPS | ≤50 | 20 | 글로벌 SOTA 45ms (src#NN) |
| 예: 인증 획득(정성) | 건 | 제3자 인증기관 | KC+CE 2건 | 15 | — |
| 예: 시제품 완성도(정성) | TRL | NASA TRL 기준 | TRL 7 | 10 | — |
| **합계** | | | | **100** | |

규칙: 가중치 합은 정확히 100. 정량지표는 측정방법·조건·달성시기·비교근거 4요소 결합(§12). 평가항목 설정근거는 별도 표(§10)로 "왜 이 지표를 골랐는가"를 1:1로 설명한다.

---

## 10. 필수 표/도표 11종 카탈로그

> 출처: 연구노트 §A 11종 + §G 재무표. 각 표의 컬럼 구조 + 어느 항목에 들어가는지 + 엑셀 캡처 대상 여부. 재무 산식·캡처 실무는 `references/financial-models.md`(연구노트 §G/§H) 참조.

| ID | 표/도표 | 컬럼 구조(핵심) | 들어가는 항목 | 엑셀 캡처 | 비고 |
|---|---|---|---|---|---|
| `summary-general` | 일반현황 | 기관명·아이템명·업종·신청자·설립예정지 | PSST 본문 앞 | — | 양식 제공 시 그대로 |
| `summary-item` | 아이템개요(요약) | 구분(소개·차별성·목표시장·이미지)·내용 | PSST 본문 앞 | — | 이미지 1컷 포함 |
| `gantt-schedule` | 추진일정(간트) | 세부활동·담당·시작·종료·산출물 / 월별 바 | PSST 3-3, R&D 2 | ○ | 분기/월 단위 |
| `fund-plan` | 자금소요·조달 | 소요(항목·금액)·조달(정부지원·자부담 현금/현물)·합계·비중 | PSST 3-3 | ○ | 핵심 합계 셀 강조 |
| `market-size` | 시장규모(TAM/SAM/SOM) | 구분·산정식·금액·근거출처 / 동심원 도식 | PSST 1-2·3-2, R&D 6 | ○ | SOM=3년 내 실제 매출(보수적) |
| `eval-criteria` | 평가기준=정량목표 | 지표(정성/정량)·단위·측정방법·달성목표·가중치·비교근거 | R&D 2 | ○ | 가중치 합 100, §12 공식 |
| `eval-rationale` | 평가항목 설정근거 | 평가지표·선정 이유·관련 기술난제·국내외 수준 | R&D 2 부속 | — | "왜 이 지표" 1:1 설명 |
| `schedule-matrix` | 추진일정 매트릭스 | 단계/연차 × 핵심 마일스톤·정량목표·점검시점 | R&D 2 | ○ | 간트와 정합 |
| `org-chart` | 추진체계도 | 주관·참여기관·역할 노드 + 연결선(협력·보고) | R&D 3, PSST 4-1 | — | 다이어그램(§09-diagrams) |
| `research-team` | 연구팀 편성표 | 성명·소속·직급·담당역할·참여율(%)·주요경력 | R&D 4, PSST 4-1 | ○ | 참여율 합리성 |
| `budget-detail` | 사업비 명세표 | 비목(인건비·재료비·장비비·연구수당·간접비)·산식·금액·재원 | PSST 3-3, R&D 별첨 | ○ | 연구수당=인건비×0.2 이내 |

### 표 작성 공통 규칙

- **단위·기준연도·출처를 표 상/하단에 명시**(백만원·명·% / 2026년 기준 / 출처: KOSIS, 조회일 …).
- 표가 길면 **분할**(연도 Y1~3/Y4~5, 비목 직접비/간접비 블록) — 폰트 축소보다 분할.
- 엑셀 캡처 대상(○)은 캡처 전 **핵심 결과 셀 강조**(SOM·영업이익·정부지원금합계·LTV/CAC) — 이미지는 사후편집 불가(연구노트 §H).
- 캡션("표 N. 제목") + 인라인 삽입. 원본 .xlsx는 별첨.
- `section-visual-map.md`에 표 ID를 적어 어느 항목에 어떤 표가 들어가는지 1:1 추적.

---

## 11. 표 ↔ 항목 매핑 빠른 참조 (어느 표가 어디에)

```text
PSST                              R&D (IRIS)
─────────────────                ─────────────────
요약 앞   summary-general          항목1  (기술동향 비교표)
요약 앞   summary-item             항목2  eval-criteria, schedule-matrix
1-1       (문제구조도)             항목3  org-chart
1-2       market-size              항목4  research-team
2-2       (경쟁비교표·포지셔닝맵)  항목6  market-size
3-2       (CAC/LTV·채널표)         별첨   budget-detail
3-3       gantt-schedule, fund-plan, budget-detail
4-1       research-team(팀역할), org-chart
```

> `template-map.yaml`의 각 매핑에 `required_tables: [...]`로 위 ID를 적는다. Gate 6 체크리스트에서 "유형에 해당하는 표가 모두 어느 항목에 배치됐는지" 대조.

---

## 12. 정량/정성 목표 작성 공식 (평가위원 지적 사전 차단)

> 출처: 연구노트 §B. 평가표(eval-criteria)·PSST 성과목표·R&D 항목2에 그대로 적용.

### 12.1 정량목표 공식

```text
정량목표 = 활동 → 직접 결과 → 숫자 + 조건/환경 + 측정방법 + 달성시기 + 세계최고수준 비교근거
```

- **숫자부터 쓰지 말 것.** "○○ 활동을 통해 △△" 순으로 인과를 먼저 세운다.
- 숫자에는 **출처/산정근거**를 붙인다(계약건수·국내/해외 매출 분리 등).
- 측정 가능하도록 **조건·환경 + 측정방법 + 달성시기**를 결합한다.
- **세계최고수준 보유국·수준과 비교**해 목표의 의미를 증명한다(특히 R&D).

### 12.2 정성목표 공식

```text
정성목표 = 측정 가능한 상태 변화 (추상적 형용사 금지)
```

목표는 하나의 흐름으로 연결한다(콘텐츠→유통→매출→조직). **투자유치는 목표가 아니라 성과의 결과**로 배치한다.

### 12.3 좋은/나쁜 예시

| 구분 | ❌ 나쁜 예 | ✅ 좋은 예 |
|---|---|---|
| 정량(성능) | "이동거리 향상" | "이온풍 비행기 **평균 이동거리 ≥100m** (무풍 실내·0.5m 높이·10회 평균, 2027.12). 근거: MIT 동일환경 60m (src#NN)" |
| 정량(매출) | "매출 10억 달성" | "B2B 계약 12건 확보를 통해 **3차연도 매출 480백만원**(국내 360+해외 120, 계약 파이프라인 src#NN)" |
| 정량(효율) | "고효율 달성" | "**에너지 효율 ≥85%** (KS C IEC 표준 측정, 2026.6). 국내 최고 78% 대비 +7%p (src#NN)" |
| 정성(조직) | "인지도 향상" | "**정규인력 5명 고용으로 1인 창업 → 조직 단위 전환**(2027.12, 4대보험 가입 기준)" |
| 정성(품질) | "품질 개선" | "**제3자 인증기관 KC+CE 2건 획득**으로 양산 적합성 확보(2027.6)" |

### 12.4 불리한 표현 교정 (연구노트 §E)

- "국내 유일" → "유사사례 미확인(부록 N)"
- "100% 개선" → "동일조건 대비 X%(부록 N)"
- 무출처 형용사 → 정량 수치 + 측정조건 + 출처

---

## 13. template-structure.yaml / template-map.yaml 스키마 보강 요약

§2·§3·§5의 보강을 한눈에. **굵게**가 이번에 추가/강화된 필드.

```yaml
# template-structure.yaml
meta:
  template_mode:        # ★ FOLLOW_TEMPLATE | USE_STANDARD
  standard_skeleton:    # ★ USE_STANDARD일 때 "PSST"/"R&D-IRIS"/"pitch-deck"/"proposal"
  source_file: ...
summary_tables:         # ★ 본문 앞 요약표 (PSST 2종 / 양식 제공분)
  - { name, position, columns }
sections:
  - id:                 # ★ 양식 번호 글자 그대로
    title:              # 양식 제목 글자 그대로 (의역 금지)
    subsections:        # ★ [{id, title}] 세부 항목 번호 보존
    tables: [{name, columns, merged_cells}]
required_attachments: [...]
```

```yaml
# template-map.yaml
mappings:
  - official_id:        # ★ 양식 번호 (FOLLOW_TEMPLATE 필수)
    official_title:     # 양식 제목 글자 그대로
    evaluator_question: # ★ 평가자 질문
    core_path: [...]
    evidence: [...]
    representation: ...
    required_tables: [] # ★ §10 카탈로그 표 ID
```

```yaml
# section frontmatter (§5)
section:
  official_id:          # ★ 양식 번호
  ...
  quantitative_goals:   # ★ §12 정량목표 공식 산출물
  qualitative_goals:    # ★ §12 정성목표
  tables:               # §10 카탈로그 ID 병기
```

---

## 14. 양식 추종 자가 점검 (초안 진입 직전 30초)

> 작성 시작 전에 의식적으로 거부할 안티패턴.

- [ ] 양식이 있는데 표준 골격으로 임의 재구성하고 있지 않은가? → 양식이 이긴다(§0.1)
- [ ] 양식 항목 번호를 `1-1`→`1.1`처럼 바꾸지 않았는가?
- [ ] 양식 항목 제목을 의역·축약하지 않았는가?
- [ ] 양식 순서를 강조 의도로 재배열하지 않았는가?
- [ ] 양식 표에 임의 컬럼을 추가/삭제하지 않았는가?
- [ ] 정량목표를 숫자만 쓰고 조건·측정·시기·비교근거를 빠뜨리지 않았는가? (§12)
- [ ] 모든 양식 항목이 template-map에 매핑됐는가? (누락 0)
- [ ] 핵심 수치가 요약표·본문·엑셀에서 일치하는가? (7대 규칙 #7)
