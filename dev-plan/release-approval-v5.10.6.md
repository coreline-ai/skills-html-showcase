# release-approval-v5.10.6.md

승인 일시: `2026-06-21 KST`
승인 출처: 사용자 직접 지시 — "5.10.6 으로 승격 전에 모든 항목 패치 진행 하고 승격 순으로 진행" + "Phase 4를 바로 진행하고 이어서 Phase 5로 5.10.6를 마무리".

이 문서는 AGENTS.md §2.1("버전 변경은 사용자 명시 승인 또는 `dev-plan/release-approval-vX.Y.Z.md`가 있을 때만 허용")의 승인 기록이다. 계획: [implement_20260618_221706.md](implement_20260618_221706.md).

## 승인 범위

v5.10.5 → **v5.10.6** "시각 결함 하드닝(G1~G8) + 검출 게이트 신설" — **코어 CSS 직접 수정 패치**(D1=코어 직접 확정).

- **코어 해시**: `a73eb204`(직전 미릴리스 배지 수정 흡수본; v5.10.5 태그 릴리스는 `7e151665`) → **`a64604d0`**. examples 18종 재인라인·`sources/css-integrity.json`·source manifest·`.skill`(263파일/2.93MB) 재패키징.
- **거버넌스**: `162` → **`186`** (신규 게이트 catch/pass: G-series 14 + business_plan 9 + pretest_contract 1 = 24건).

### CSS/패턴/계약 하드닝
- **G1** (작성 계약): 좁은 표 짧은 상태코드 줄바꿈 → `.status-pill` 정본(`table .status-pill{white-space:nowrap}` 기존). broad `td code` nowrap은 예제 09 regex 다토큰 코드 회귀 회피로 채택 안 함.
- **G3** (`components.css` 코어): `.try` 중첩 흰 카드(.box/.summary-card/.cta-box/.card-block/.mini-card) 링크 `--link-on-dark`(흰 배경 1.65:1) → `--accent-2` reset(8테마 min **6.09:1**). `.try` 직속 링크는 `--link-on-dark` 유지.
- **G4** (`editorial-patterns.css`): `source-preserve` 좌측 gutter 정본 `.source-body-inner`.
- **G5** (`components.css` 코어): `.mini-card>.tag:first-child` vertical rhythm.
- **G8** (`editorial-patterns.css`): `.core-insight>:first-child{margin-top:0}` + red gradient 보존(`--neutral` 금지 규칙).
- **A5** (`theme.css` 코어): `@media (prefers-contrast: more)` 약 토큰 대비 상향(렌더 영향 0).
- **U0 흡수**: 직전 Unreleased(manual_analysis 배지 padding, `layouts.css` 코어)를 본 릴리스로 승격.

### 검출 게이트 신설 (악성 fixture 먼저 → governance++)
- **G2** render-audit `node_overlap_ok`(diagram 노드 박스 overlap >4px×4px) + **G3** `inner_card_link_contrast_ok` — `scripts/micro_layout_audit.mjs`(Playwright) 생산, `completion_check.py` 검사. 검증기는 무 JS 불변(JSON만 읽음).
- **G4·G5·G8** 자산-레벨 정적 가드(`skill_asset_lint`), **G3·G6·G7** per-page 정적 가드(`validate()`). G6/G7 DOM 가드는 기존 examples 18/18 무회귀 확인.

## 범위 확장 (2026-06-21) — mode 18 `business_plan` 5.10.6 병합 (버전 업 없음)

사용자 결정으로 **`business_plan_html`(mode 18)을 별도 v5.11.0 없이 본 5.10.6 릴리스에 병합**한다([implement_20260621_150500.md](implement_20260621_150500.md)). 코어 CSS 무변경(implementation-plan vt + 기존 wg-16/11/13/18/14 재사용, layout 전용 CSS를 layouts.css에 넣지 않음) → **코어 해시 `a64604d0` 불변**·기존 18 예제 재인라인 불필요. 추가분(additive): `modes/18-business-plan.json`·layout 템플릿·recipe·references·4 custom gates·신규 예제 1개 + governance_count·mode count(17→18)·examples count 증가. CHANGELOG v5.10.6 엔트리·본 문서에 mode 18 줄 흡수. **버전 문자열 5.10.6 유지.** `version_release_approval` 게이트는 본 문서 존재로 충족. (※ 빌드 완료 시 본 절에 mode 18 게이트/example/governance 최종 수치 추가.)

## 제외 (이번 차수 아님)
- **strategy-os** → 소스 `company_ai_strategy_dashboard.html` 미커밋으로 **slot 21+ 보류**(mode 18도 5.11.0도 아님; [implement_20260620_201946.md](implement_20260620_201946.md) SUPERSEDED).
- **storm_research·social_trend** 신규 모드 → 각 후속 차수([implement_20260621_130535.md](implement_20260621_130535.md)). operator_manual은 manual_analysis 흡수/보류.
- theme-token 마이그레이션·AGENTS §2.2 생성비용 최적화·export 재검증·output 보존 정책·visual-html 잔여 토큰화 → 별도 로드맵. repo `scripts/build_*.py` untracked은 비대상(W3b).

## 검증 (자체 테스트)
- `test_governance_gates.py` **186/186**.
- `validate_output.py examples --skill-dir` OK(inline hash·verbatim·snapshot·.skill byte-match) — 코어 해시 `a64604d0` 일관.
- `quality_contract_check.py examples` OK(18 file). 버전 표면(manifest/SKILL/README/AGENTS/Guide/examples/visual-html-system/sources) 5.10.6 + governance 186 일괄 동기화.

## 커밋 정책
**커밋·푸시 금지. 사용자 요청 시에만 수행.** 본 차수는 워킹트리 구현 + 검증 + 전문가 리뷰까지.
