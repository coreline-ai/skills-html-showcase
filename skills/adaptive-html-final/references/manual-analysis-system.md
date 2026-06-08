# Manual Analysis System

`manual_analysis`는 레퍼런스 문서를 다시 요약하는 모드가 아니라, PDF/HTML/README/제품 메모/API 스펙/절차서에서 추출된 텍스트를 역할별 실행 매뉴얼로 재구성하는 모드다. 스킬은 PDF/OCR 파서가 아니며, 디코딩된 텍스트가 입력으로 들어온다고 가정한다.

## 1. reference_html과 경계

| 구분 | reference_html | manual_analysis |
|---|---|---|
| 목적 | 빠른 참조, API/옵션표, 치트시트 | 사용·운영·복구를 실제로 따라 하는 매뉴얼 |
| 구조 | 개념/API/패턴/예시 | 역할 경로, 첫 성공, 사전조건, 절차, 검증, 문제 해결 |
| 판단 | 정보 조회 중심 | 실행 가능성·누락·위험·stale 감사 중심 |

일반 “매뉴얼 제작/사용 설명서/운영 매뉴얼/트러블슈팅” 요청은 `manual_analysis`가 우선한다. “API 레퍼런스/옵션표/정규식 치트시트”는 `reference_html`이 우선한다.

## 2. 필수 블록과 깊이 하한

```text
source & version snapshot
→ reader role router
→ first success path
→ prerequisites & safety
→ task recipes
→ reference extract
→ decision guide
→ troubleshooting
→ operations runbook
→ manual audit
→ next actions
→ source limits
```

블록 수 충족은 완료 조건이 아니다. 각 블록은 아래 질문에 답하고 깊이 하한을 충족해야 한다(SKILL.md §4 정량 하한과 동일 계약).

| 블록 | 답해야 할 질문 | 깊이 하한 |
|---|---|---|
| source & version snapshot | 어떤 원문·버전이 입력이고 무엇이 승인 대기인가 | FACT/UNKNOWN/OWNER 카드 3종, 카드당 2문장+ (버전 충돌·승인 대기 위치 명시) |
| reader role router | 내 역할은 어디부터 읽나 | 입력에 실재하는 역할만, 역할마다 권장 읽기 순서(§ 참조) + 이관 기준 |
| first success path | 30분 안에 “되는 상태”를 어떻게 경험하나 | 단계 3개+, 단계마다 성공 기준 + 실패 분기 명시 |
| prerequisites & safety | 하기 전에 무엇을 확인하나 | 위험 카드 3종+, 카드마다 복구 조건 또는 판별 방법 |
| task recipes | 반복 작업을 어떻게 표준화하나 | 표준 6필드(목적·사전조건·절차·완료 기준·롤백·원문 근거) + 작성 가능 레시피 최소 4개 식별 |
| reference extract | 원문 추적이 가능한가 | 입력 파일 전체 목록 + “목록 밖 정보는 본문에 없다” 선언 |
| decision guide | 누가 처리하고 언제 이관하나 | 경로 3종+, 경로마다 판정 질문 + 이관 시 필수 첨부 |
| troubleshooting | 증상에서 복구까지 어떻게 가나 | 증상 시나리오 최소 3개(전개 1개 + 식별 목록 가능), 4단 구조(증상→가능 원인→진단 순서→복구) 고정 |
| operations runbook | 정기 점검은 무엇이고 이상 시 어디로 가나 | 주기 3종(일일/주간/릴리스 전), 점검마다 이상 시 분기 경로 |
| manual audit | 매뉴얼 자체의 결함은 무엇인가 | 지적 최소 3건, 건당 원문 위치(파일·항목) 명시 |
| next actions | 초안을 어떻게 확정하나 | 순서 있는 행동 4개+, 승인 대기 해소 계획 포함 |
| source limits | 무엇을 확인하지 못했나 | UNKNOWN 항목 열거 + 소유자 검토 필요 선언 |

## 3. 절차 작성 규칙

각 task recipe는 다음 6필드 표준 구조를 가진다.

```text
목적 → 사전조건 → 절차(번호 단계 + 단계별 예상 화면) → 완료 기준 → 롤백(소요 시간 포함) → 원문 근거
```

- 위험 작업에는 `데이터 삭제`, `권한 변경`, `비용 발생`, `롤백 불가`, `서비스 중단` 라벨을 붙인다.
- 경고는 절차 끝의 “주의” 박스가 아니라 해당 위험 작업의 첫 단계 앞에 배치한다.
- 롤백 필드가 빈 레시피는 발행 금지 — “롤백 불가”도 명시적 기재다.
- 원문 근거 필드는 `파일명 §위치` 형식(예: `ops/rollback.md §2`)으로 적어 원문 갱신 시 추적 가능하게 한다.

## 4. 품질 감사 규칙

- 누락·중복·모순·stale·위험 작업 미표시는 원문 위치/근거가 있을 때만 단정한다.
- 근거가 없으면 `확인 불가` 또는 `UNKNOWN`으로 표시한다.
- 제품 버전, 권한, SLA, API 제한, 운영 상태는 입력 원문에 없으면 추측하지 않는다.
- 입력에 없는 역할(user/admin/dev/operator/support)은 만들지 않는다. 빈 역할 카드 금지.
- 모순 발견 시 어느 쪽도 정본으로 채택하지 않고 양쪽 출처를 병기한 “보류” 상태로 소유자 검토에 회부한다.
- 감사 지적은 결함 유형(누락/낡음/모순/미기재)을 분류해 적는다 — “문서가 부실하다” 같은 무위치 지적은 금지.

## 5. 시각화 계약

| 정보 구조 | vt | wg | 사용 이유 |
|---|---|---|---|
| 역할별 매뉴얼 지도 | `hero-map` | `wg-14` | 독자→목표→첫 행동을 첫 화면에서 분기 |
| 첫 성공/절차 | `checklist-flow` | `wg-13`, `wg-16` | 따라 할 단계와 완료 조건 |
| 검수/안전 | `quality-gate` | `wg-18`, `wg-11` | 위험 작업·완료 기준·운영 상태 |
| 출처/구조 투어 | `file-tour` | `wg-04` | 문서 묶음·설정·API reference extract |
| 운영 흐름 | `process-swimlane`, `decision-tree`, `risk-matrix` | `wg-16` | 역할별 운영/복구 플로우 |

프로파일별 선택은 SKILL.md §0.6이 단일 출처다.

## 6. HTML 구성 계약

레이아웃: `assets/layouts/manual-analysis.html` / class `.layout-manual`

- 헤더는 `generated-row`(source snapshot 날짜 + manual status) + `lens-strip`(Role/Safety/Troubleshooting 칩)을 포함한다.
- verdict(`manual-verdict`)는 본문 최상단, Reader Role Router 목차(`toc-map manual-reader-toc`)가 뒤따른다.
- 목차 내부는 공식 카탈로그 `toc-map` chip-nav 구조(`span.label` + 설명 `p` + `.toc-pills` + `a.toc-pill > b`)로 작성한다. 구형 `.toc`/`ol` 또는 `.toc-map` 안의 bare link는 회귀다.
- 번호가 있는 모든 섹션 `h2`는 `body-icon body-icon--sm` → `num` → 제목 순서를 유지하고, 주요 h2에는 `h2-sub`를 붙인다.
- 권장 클래스: `.manual-reference-grid`/`.manual-card`+`.manual-label`(출처·선택 기준), `.manual-role-grid`/`.manual-role`(역할 경로), `.manual-step-grid`/`.manual-step`+`.manual-safe`(첫 성공 단계), `.manual-audit-grid`+`.manual-risk`/`.manual-unknown`(안전·감사), `.manual-trouble-grid`/`.manual-trouble`(4단 트러블슈팅), `.manual-runbook-grid`(운영 주기).
- 평면 파일 목록이 6개 이상이면 `<ul class="col-list">` 다단 그리드로 렌더한다.
- 레시피 표는 visible `<caption>` + `mobile-card-table`(4열 이상) 계약을 따른다.

## 7. 출력 톤

- 제목은 “무엇을 할 수 있게 되는가”를 말한다.
- 처음 1~2개 섹션에서 독자가 자신의 역할과 첫 행동을 찾을 수 있어야 한다.
- 절차는 산문보다 카드/표/체크리스트 중심으로 쓰되, 카드가 1문장으로 끝나면 미완성이다(근거 또는 분기 1문장을 더한다).
- 섹션 사이를 § 상호 참조로 연결한다 — 첫 성공의 실패 분기는 트러블슈팅으로, 런북의 이상 신호는 증상 시나리오로.
- 마지막은 다음 작업, 확인 요청, 원문 보완 필요 항목으로 끝낸다.

## 8. 흔한 실패 패턴 (즉시 재작성 대상)

- **레퍼런스 재요약**: 원문 목차 순서대로 정보를 재배열만 한 출력. 역할·위험·증상 기준 재구성이 없으면 reference_html과 다를 게 없다.
- **넓고 얇은 출력**: 12개 블록 골격에 카드 전부 1문장. 깊이 하한 위반.
- **근거 없는 감사**: “문서가 오래됐다”는 지적에 원문 위치가 없다.
- **롤백 없는 레시피**: 절차와 완료 기준만 있고 실패 시 경로가 없다 — 매뉴얼이 아니라 데모 스크립트다.
- **역할 발명**: 입력에 없는 역할 카드를 채워 넣는다.
- **h2-sub 생략**: 다른 모드와의 디자인 리듬이 깨지는 직접 원인.

## 9. Source note 계약

마지막 `source-note`에는 반드시 다음을 남긴다.

- source snapshot 날짜와 manual status(draft/owner review/확정).
- 입력 원문 목록(§6 reference extract와 일치해야 함).
- 확인 불가 항목: 실제 제품 버전, 권한 정책, SLA, 법무 문구 등.
- 소유자 검토 후 확정 필요하다는 선언(위험 절차가 있는 경우).

## 10. 완료 게이트

- `h1` 하나, `<main id="main" class="page-wide layout-manual">` 유지.
- 헤더 `generated-row`/`lens-strip`, 테마 스위처, 번호 앞 body icon 유지.
- 외부/동작 JS 0.
- 역할 라우터·안전·트러블슈팅 존재 (`validate_output.py`의 manual 계약 게이트).
- 감사 지적에 원문 근거 존재 (`manual_audit_claim_without_source`).
- §2 깊이 하한 충족 — 레시피 4개 식별·6필드, 증상 시나리오 3개·4단, 감사 지적 3건+위치, 카드당 2문장+. 게이트가 잡지 못해도 이 하한 미달은 미완성이다.
