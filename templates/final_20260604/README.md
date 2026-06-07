# final_20260604 — 고유 작업 자산 (스킬 비참조)

손으로 제작한 비주얼 북극성(완성본) 템플릿. **`adaptive-html-final` 스킬이 참조/검증하지 않는다.**

- `index.html` — **폴더 진입점 대시보드**(허브). 아래 템플릿들을 카드+링크로 모아 브라우저에서 바로 여는 landing_brief 구조. **이 파일만은 `adaptive-html-final` 스킬로 현재 코어(`329b6326…`, 8테마)·body-icon·무 JS 계약을 지켜 생성**했고 스킬 검증기 페이지 게이트(`validate_output.py`)를 0 이슈로 통과한다(폴더 전체는 아래 bespoke 두 파일의 의도적 실패로 FAILED 유지 — 이 폴더는 검증 출력 디렉터리가 아님). 새 템플릿 추가 시 목록에 `mini-card` 한 개를 더한다(정적 HTML이라 자동 스캔 없음).
- `index-standard-width.html` — 기본 폭 종합 완성본 (전 editorial 패턴 + 다이어그램 + 데모 섹션, "Skill Template HTML"). 옛 `index.html`에서 개명(2026-06-07) — 폭 변형 짝과 이름 축을 맞춤. **8테마 적용(2026-06-07)**: 옛 5테마 스위처를 스킬 현재 `theme-dark.css`(8테마 `:root:has` 토큰 + 8라디오 grid 스위처)로 전환.
- `index-beginner-width.html` — 위 파일의 초보자 모드1 780px 읽기 폭 변형(복사본). **8테마 적용(2026-06-07)**: 옛 3테마 → 스킬 8테마 시스템으로 전환.
- `index-all-templates-catalog.html` — 전 템플릿 카탈로그 (`adaptive-html-final-all-templates-demo`에서 이관, 2026-06-07). 전 vt·wg 신선도 검증용 단일 HTML. **현재 스킬 코어 CSS(`9a7dd41…`, 8테마) 기준**으로 위 두 파일(옛 `75efbcaa…`)과 다르다. `sources/`(분리 CSS 사본·manifest)는 빌드 산출물이라 이관하지 않음 — 본 파일은 인라인 CSS로 자체 완결.

## 단독 완결성 (standalone)
- 세 HTML **모두 단일 파일로 독립 렌더** 가능. CSS는 전부 인라인 `<style>`, 로컬 CSS `<link>`·로컬 `<script src>` 의존이 0이다.
- 외부 의존은 CDN 폰트(Pretendard·Noto Serif KR)뿐 — 인터넷이 되면 어느 경로에서 열어도 동일하게 보인다(폰트 미로딩 시 시스템 폰트로 폴백).
- 본문에 보이는 `src="visual.svg"`는 PR 예시 코드 블록(`<pre>`) 안의 **텍스트**이지 실제 `<img>`가 아니므로 깨지는 리소스가 없다.

## 주의 (스킬과의 관계)
- 스킬의 wg/vt 시스템·정본 어휘로 만든 산출물이 **아님**. `edge-gov-*`·`access-check-*` 등 **페이지 발명 클래스**를 사용하므로 스킬의 `bespoke_prefix_gate`에 의도적으로 걸린다.
- 코어 CSS 마커(`75efbcaa…`)는 standard/beginner 두 파일에서 여전히 옛 버전 기준이다(코어 본체·레이아웃은 손제작 보존). **단, 테마 시스템만은 2026-06-07에 스킬 현재 `theme-dark.css` 8테마로 전환**했다 — 기존 5/3테마 스위처를 8라디오(라이트·그레이·화이트·다크·로즈·블루·스카이·세피아)로 교체하고, `:root:has` 토큰이 옛 `body:has` 토큰을 명시도·순서로 덮어쓴다.
- **다크 계열 보정 그룹 합류(2026-06-07 hotfix).** bespoke 다크 보정이 그룹 셀렉터로 걸려 있어(standard `:is(#ahf-dark,#ahf-dark2)`, beginner `#ahf-dark` 단독) 신규 다크 테마 블루(및 beginner의 로즈)가 빠져 깨졌다 → 두 파일 다크 보정 셀렉터를 `:is(#ahf-dark,#ahf-dark2,#ahf-blue)`로 확장(standard 276·beginner 233).
- **다크 3종이 동일하게 보이던 버그 수정(2026-06-07 hotfix2).** 원인: bespoke 그룹 규칙이 토큰(`--bg/--card/--accent…`)을 `:root`가 아닌 **`body`에 직접 재정의**해, 스킬이 `:root`(html)에 건 테마별 토큰을 body 하위에서 클로버(다른 엘리먼트라 명시도 무관·직접 지정 우선) → 다크·로즈·블루가 같은 `#111216` 그레이로 렌더. 수정: (1) 그 토큰 블록 셀렉터 `body:has(…)` → `:root:has(…)`로 변경(스킬의 나중-선언 테마별 `:root:has`가 표준 토큰을 덮어써 테마 구분, `--pill-*` 등 스킬 미정의 토큰은 폴백 유지), (2) body 배경 `#111216!important`·`--copy-surface*` 하드코딩 그레이를 `var(--bg)`·`var(--card/--vt-soft/--line/--accent-soft)`로 토큰화. 결과: dark(중성·코랄)·로즈(웜·모브)·블루(네이비·블루)가 각 토큰으로 구분됨(Playwright 검증).
- 남은 한계: `color-audit` 데모 패널의 테마 라벨/값 셀은 원래 테마 키에 묶여 신규 테마에서 표시가 완전하지 않을 수 있다(페이지 본문 렌더는 정상). (`index-all-templates-catalog.html`은 신규 코어 `9a7dd41…`/8테마.)
- 따라서 `skills/adaptive-html-final/examples`(정합 기준선)에는 편입하지 않으며, manifest·검증기·governance도 이 폴더를 보지 않는다. 순수 디자인 참고/보관용.
