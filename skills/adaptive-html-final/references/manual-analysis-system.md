# Manual Analysis System

`manual_analysis`는 레퍼런스 문서를 다시 요약하는 모드가 아니라, PDF/HTML/README/제품 메모/API 스펙/절차서에서 추출된 텍스트를 역할별 실행 매뉴얼로 재구성하는 모드다. 스킬은 PDF/OCR 파서가 아니며, 디코딩된 텍스트가 입력으로 들어온다고 가정한다.

## 1. reference_html과 경계

| 구분 | reference_html | manual_analysis |
|---|---|---|
| 목적 | 빠른 참조, API/옵션표, 치트시트 | 사용·운영·복구를 실제로 따라 하는 매뉴얼 |
| 구조 | 개념/API/패턴/예시 | 역할 경로, 첫 성공, 사전조건, 절차, 검증, 문제 해결 |
| 판단 | 정보 조회 중심 | 실행 가능성·누락·위험·stale 감사 중심 |

일반 “매뉴얼 제작/사용 설명서/운영 매뉴얼/트러블슈팅” 요청은 `manual_analysis`가 우선한다. “API 레퍼런스/옵션표/정규식 치트시트”는 `reference_html`이 우선한다.

## 2. 필수 블록

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

## 3. 절차 작성 규칙

각 task recipe는 가능한 한 다음 구조를 가진다.

```text
목표 → 사전조건 → 단계 → 기대 결과 → 검증 방법 → 실패 시 조치
```

위험 작업에는 `데이터 삭제`, `권한 변경`, `비용 발생`, `롤백 불가`, `서비스 중단` 라벨을 붙인다.

## 4. 품질 감사 규칙

- 누락·중복·모순·stale·위험 작업 미표시는 원문 위치/근거가 있을 때만 단정한다.
- 근거가 없으면 `확인 불가` 또는 `UNKNOWN`으로 표시한다.
- 제품 버전, 권한, SLA, API 제한, 운영 상태는 입력 원문에 없으면 추측하지 않는다.
- 입력에 없는 역할(user/admin/dev/operator/support)은 만들지 않는다. 빈 역할 카드 금지.

## 5. 시각화 계약

| 정보 구조 | vt | wg | 사용 이유 |
|---|---|---|---|
| 역할별 매뉴얼 지도 | `hero-map` | `wg-14` | 독자→목표→첫 행동을 첫 화면에서 분기 |
| 첫 성공/절차 | `checklist-flow` | `wg-13`, `wg-16` | 따라 할 단계와 완료 조건 |
| 검수/안전 | `quality-gate` | `wg-18`, `wg-11` | 위험 작업·완료 기준·운영 상태 |
| 출처/구조 투어 | `file-tour` | `wg-04` | 문서 묶음·설정·API reference extract |
| 운영 흐름 | `process-swimlane`, `decision-tree`, `risk-matrix` | `wg-16` | 역할별 운영/복구 플로우 |

## 6. 출력 톤

- 제목은 “무엇을 할 수 있게 되는가”를 말한다.
- 처음 1~2개 섹션에서 독자가 자신의 역할과 첫 행동을 찾을 수 있어야 한다.
- 절차는 산문보다 카드/표/체크리스트 중심으로 쓴다.
- 마지막은 다음 작업, 확인 요청, 원문 보완 필요 항목으로 끝낸다.
