# github-feature-usage-system — GitHub 기능·도입 가이드 (17번째 모드)

> 레이아웃: `layout-github-feature` / 스캐폴드: `assets/layouts/github-feature-usage.html`
> 트리거: GitHub 저장소를 **"무엇을 해주나 · 어떻게 쓰나 · 어디에 맞나"** 기능·사용법·도입 관점, 실제 화면(스크린샷) 중심으로.

## 1. github_analysis와의 차이 (왜 독립 모드인가)

| | `github_analysis` | `github_feature_usage` |
|---|---|---|
| 질문 | "신뢰·도입해도 되나? 살아있나? 위험은?" | "이게 뭘 해주나? 어떻게 쓰나? 우리에게 맞나?" |
| 무게 | 실사 — health/risk/security/verdict | 사용 설명 — 기능 지도/화면/시작/적합성 |
| 어조 | 의사결정·경고체 | 평가·온보딩 안내체 |
| 독자 | 도입 결정권자·코드 리뷰어 | 평가·온보딩하는 사용자·PM |
| 강조 자산 | wg-11 KPI·risk-matrix·quality-gate | **스크린샷**·wg-14 Feature Explainer·기능 맵 |

형식·어감이 달라 같은 중간 섹션 틀을 쓰면 실패다. 한 저장소에 두 모드를 모두 낼 수 있다(다른 렌즈).

## 2. 섹션 모델 (정본 순서)

1. **positioning** — 한 줄 정체성 + 대상 독자 (`.feature-verdict`)
2. **overview** — 한눈 요약 시그널 (`.feature-overview`, `hm-grid` 또는 `repo-signal-grid`). 정본 출력이 verdict 직후 상단에 두는 hero 개요.
3. **feature toc** — `toc-map` + `toc-pills` + `a.toc-pill > b` 계약 (`.feature-toc`)
4. **feature map** — 기능 지도. `card-grid` 또는 `.feature-map-grid`
5. **core capability** — 핵심 기능. `wg-14` Feature Explainer 우선
6. **tech stack** — 기술 스택 전체 지도
7. **architecture** — 구조 심화 (`wg-04` Module Map)
8. **directory** — 디렉토리 구조 해부 (file-tour)
9. **actual screens** — 실제 화면 스크린샷 갤러리 (아래 계약 필수)
10. **user features** — 사용자 기능을 흐름으로 (가입→…→종료)
11. **admin features** — 관리자 기능 (사용자/권한/세션/감사)
12. **getting started** — 시작 방법(단계형, `wg-16`)
13. **where it fits** — 적합/부적합 시나리오
14. **pre-adoption check** — 도입 전 확인 항목
15. **final verdict** — 최종 판단(기능 이해용/도입용 권고)
16. **next actions** — `.try`
17. **source note** — 출처 한계

> 번호는 표시 순서일 뿐 — feature toc 이후 본문 순서는 위 정본 출력 흐름을 따른다.

## 2.5 컴포넌트 어휘 (정본 출력 기준)

정본 출력은 기능·기술스택·아키텍처·사용자/관리자 기능·도입 확인을 github의 카드/그리드 어휘로 구성한다. `layout-github-feature`는 `layout-github`과 **동일 컴포넌트 vocabulary를 공유**하므로 그대로 쓴다:

- `repo-evidence-grid` / `repo-evidence` — 3열 근거 카드 (기능·기술스택·사용자 기능·도입 확인)
- `repo-signal-grid` / `repo-signal` — 개요·관리자 기능 신호 카드
- `repo-action-grid` / `repo-question` — 최종 판단 행동 카드
- `code-tour` + `repo-card` — 디렉토리/파일 좌우 정렬 행 (file-tour `ft-card`도 가능)
- `hm-grid`(hero-map) — overview·feature map, `wg-14`(Feature Explainer) — core capability
- 모바일 ≤760px에서 `repo-*-grid`는 1열로 붕괴(github과 동일).

## 3. 스크린샷 계약 (이 모드의 시그니처)

- 컨테이너: `<section class="feature-screens"><div class="feature-screens-grid">…`
- 각 화면: `<figure><img src alt><figcaption>설명</figcaption></figure>`
- **최소 3장**, 각 `alt` 필수, `figcaption` 1문장 이상.
- 스크린샷은 `sources/screenshots/`에 두고 상대경로로 참조. 외부 핫링크 금지.
- 화면이 없으면(스크린샷 미수집) "실제 화면" 섹션 대신 기능 지도로 대체하고 source note에 사유를 남긴다.

## 4. 정량 하한 (블록 수 충족 ≠ 완료)

- 기능 지도 카드 **최소 4개**, 각 카드 한 줄 효용.
- 실제 화면 스크린샷 **최소 3장** + caption + alt.
- 사용자/관리자 기능은 단순 나열이 아니라 **흐름/운영 항목**으로 서술.
- 시작 방법은 **단계형**(전제 → 데모 → 실제 연결).
- 주요 h2에 `h2-sub` 부착. 각 섹션이 1문장으로 끝나면 미완성.

## 5. FACT / INFERENCE / UNKNOWN

- README·코드·릴리스에서 확인 가능한 것만 FACT.
- 입력에 없는 **버전·라이선스·성능·SLA**는 UNKNOWN으로 남기고 추정 금지.
- 화면·기능 설명은 관찰된 데모/스크린샷 근거에 한정.

## 6. 완료 게이트 (validate_output.py)

- `mode_primary_vt_missing` / `mode_recommended_wg_missing` — `layout-github-feature` 계약(primary `hero-map`, 권장 `wg-14`/`wg-04`/`wg-16`/`wg-11`/`wg-08`).
- `github_feature_usage_toc_map_missing` — `.feature-toc` + toc-map 계약.
- `github_feature_*` (contract gate) — 섹션 카드 표면, body-icon, 기능 지도/실제 화면 중 하나 이상, 출처 한계.
- 공통: 직접 섹션 h2 body-icon 필수, body-icon 다양성, 표 caption·모바일 wrapper, 무 JS, 코어 CSS verbatim+해시.
