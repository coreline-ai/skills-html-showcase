# release-approval-v5.10.5.md

승인 일시: `2026-06-15 KST`
승인 출처: 사용자 직접 지시 — "A 개발 계획 세우고 개발 진행" (묶음 A 승인).

이 문서는 AGENTS.md §2.1("버전 변경은 사용자 명시 승인 또는 `dev-plan/release-approval-vX.Y.Z.md`가 있을 때만 허용")의 승인 기록이다.

## 승인 범위 (묶음 A)

v5.10.4 → **v5.10.5** "접근성·스코프 하드닝" — **코어 CSS 5종 불변(해시 7e151665 유지)** 패치.

- **A1 (P2)** forced-colors/고대비 상태 단서: 테마바 + 핵심 wg 컨트롤(선택/체크 상태)이 배경색만으로 상태를 전달해 Windows 고대비에서 소실되는 문제를 `@media (forced-colors: active)` border/outline 단서로 보강. (theme-dark.css·widgets.css — 조건부 자산)
- **A2 (P3)** `visual-html.css`의 비스코프 `.score` 셀렉터를 `.tuner .score`로 스코프.
- **A3 (P3)** `visual-html-templates/10-flowchart.html`의 `<div class="fc-arrow">→</div>`에 `aria-hidden="true"` 추가(+ 해당 마크업을 쓰는 예제 동기화).
- **A4 (P3)** `quality-report.schema.json` 고아 해소 — `references/eval-rubric.md`에 참조 1줄.
- **A5 (P3, 버전무관)** `dev-plan/implement_20260611_152118.md` trailing whitespace 정리.

## 제외 (이번 차수 아님)
- 묶음 B: `visual-html.css:3 body{background}` 전역 부작용 스코프화 — 전 예제 bg 미세 변경이라 별도 회귀 검증 후 결정.
- 코어 CSS(theme/components/visual-components/layouts/print) 변경 없음.
- output/ 관련 변경 없음(보존 원칙).

## 커밋 정책
**커밋·푸시 금지. 사용자 요청 시에만 수행.** 본 차수는 워킹트리 구현 + 검증까지만.

## 범위 갱신 (2026-06-15 — 사용자 지시: "수정 항목을 모아 한 버전에")

v5.10.6을 따로 만들지 않고 남은 항목을 이 5.10.5(미커밋 스테이징)에 합친다.

- **B2 추가 (A3 연장, a11y)**: checklist-flow(vt-05) 장식 글리프 `✓`/`·`에 `aria-hidden="true"`. 상태는 동반 `cf-state`(PASS/진행 중/대기) 텍스트가 전달하므로 글리프는 순수 장식. 적용: 05 템플릿(3) + 예제 13(5)·16(3) + 카탈로그(3). CSS 무변경 → 코어 해시·css-integrity 영향 없음.
- **B1 평가 후 드롭 (결함 아님)**: `visual-html.css:3 body{background:var(--vt-wash)}`은 누수 버그가 아니라 **의도된 bg-추종 토큰**. 측정: 8테마 중 6개 `--vt-wash`==`--bg` 동일, 라이트 `#f5f5f0`vs`#faf9f5`(거의 식별불가), blue `#0a1a3c`vs`#0d1320`만 약간. 스코프/제거 시 검증된 예제의 라이트·blue 배경이 바뀌어 이득 없는 시각 회귀 위험 → 변경하지 않음.
