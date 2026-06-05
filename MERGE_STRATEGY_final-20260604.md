# final_20260604 → adaptive-html-final 섹션 병합 전략

> 작성 방식: `output/final_20260604/index.html`(4,135줄) 전 섹션 패턴을 5개 도메인 병렬 분해(52개 패턴 인벤토리) → 4인 전문가 패널 적대적 검토(에디토리얼/비주얼, CSS 아키텍처, 접근성, 스킬-거버넌스) → 종합. 모든 load-bearing 주장은 **출고된 `skills/adaptive-html-final/assets/*.css`에 직접 대조 검증**함.
> 대상 스킬: adaptive-html-final v4.5.0 · 작성일: 2026-06-05 · 전문가 패널 평결: 4/4 "endorse-with-revisions"
> 사용자 규칙: "신규면 추가, 중복이면 교체" — 본 전략은 이 규칙을 **정신은 유지하되 다음과 같이 정련**한다(§3).

## 1. 총평

52개 패턴 중 **실제로 스킬에 병합할 가치가 있는 것은 ~9개**(+갤러리/레퍼런스 재배치 ~3개)뿐이며, **~30개는 페이지 전용 아티팩트**(리듬·정렬 정규화, `.good` 누수 차단 패치, 다크테마 `:is()` 116클래스 열거, 그리고 스킬에 이미 있는 시스템을 페이지가 별도 이름으로 재구현한 "병렬 어휘")로 **스킬에 병합하면 안 된다**.

가장 중요한 구조적 판단:
- **`index.html`은 신뢰할 수 없는 병합 소스다.** 인라인된 "코어 CSS"가 손으로 패치돼 있다(예: `index.html:91`의 `.kicker`는 warm pill인데 출고본 `theme.css:83`은 평범한 uppercase eyebrow). 또 페이지 전역에 존재하지 않는 토큰 `--report-sans`를 쓰고(스킬 내 0건), `!important` 93건을 쓴다. → **"이게 더 예뻐 보인다"는 판단을 페이지 대상으로 내릴 수 없다.** 병합 후보는 오직 출고된 `assets/*.css`와만 diff한다.
- 사용자의 이진 규칙은 정련된다: **"중복=교체"는 "낡은 중복본이 출고되지 않게 한다"는 의미**이며, **스킬 정본(canon)이 페이지 포트보다 더 풍부한 경우엔 KEEP-SKILL(skip)이 곧 그 규칙의 올바른 실현**이다(페이지가 기능을 깎아낸 다운그레이드 포트를 스킬에 역수입하지 않기 위함). 실제로 `#36`은 wg-05의 `<details>`를 제거한 포트이고, `#37`은 wg-06의 variant 매트릭스보다 빈약하다.

## 2. 핵심 발견 (검증 완료)

| # | 발견 | 검증 |
|---|---|---|
| F1 | **코어 해시 동결 집합 = theme/components/visual-components/layouts/print** (5개) | `validate_output.py:255` asset_order. → `layouts.css`도 동결이므로 "layouts.css는 hash-safe"라던 일부 리뷰는 오류(거버넌스 리드가 옳음) |
| F2 | 스킬 `!important`는 `widgets.css:229`·`:411` 2건(허용)뿐, 그 외 0 | grep 검증. 단 **검증기에 `!important` 게이트는 없음** → "병합 시 !important 제거" 노트는 현재 사람 규율에만 의존 |
| F3 | `--report-sans`는 스킬에 0건, 페이지 로컬 토큰(`index.html:512`) | 그대로 병합하면 브라우저 기본 폰트로 렌더되는 사일런트 회귀. 전부 `var(--sans)`/`var(--serif)`로 재작성 |
| F4 | 페이지 인라인 코어가 손패치됨(`.kicker` 드리프트) | 페이지의 css-integrity 마커가 패치된 코어로 재생성됐거나 게이트되지 않은 것 → 릴리스 블로커로 확인 필요 |
| F5 | **`.skill` 패키지가 v4.3.3에 정지**(트리는 v4.5.0, `manifest.design`도 v4.3.3 문자열) | 이미 2 마이너 뒤처짐. "스킬 업데이트" 목표는 **재패키징 없이는 미달성** → 필수 산출물 |
| F6 | 네임스페이스 게이트 휴면 | wg-게이트는 `\bwg-`, vt-게이트는 `vt-shell/vt-frame`, shape은 `shape-figure` 등에서만 발화 → 페이지의 `widget-/vt-adapt-/edge-*/module-/fi-/final-` 접두사는 **어떤 게이트도 트립하지 않음**. `edge-gov-flow`의 `role=img` 텍스트 prune 안티패턴도 사각지대 |

## 3. 병합 모델 (governing model)

### 3.1 의사결정 함수 (패턴마다 적용)
- **ADD** — 스킬에 등가물이 **없고** + 작성자-대면 재사용 가치가 분명할 때만 (예: 접근성 체크리스트).
- **REPLACE** — 스킬 등가물이 있고 + 페이지본이 검증된 개선이며 + **기존 스킬 셀렉터/이름 안으로 접어 넣을 수 있을 때만**(replace-the-primitive-keep-the-name). 페이지의 병렬 클래스명을 도입하지 않는다.
- **MERGE-AS-VARIANT** — 등가물이 있고 페이지가 선택적 처리를 더할 때, 기존 셀렉터의 네임스페이스 opt-in 수식자로 표현(예: `.core-insight--neutral`, `.source-preserve-static`).
- **SKIP-PAGE-ONLY** — 리듬/정렬 정규화, `.good` 누수 차단, 페이지 래퍼 의존 override, 다크테마 열거, **그리고 더 풍부한 스킬 컴포넌트의 출력측 재스킨 포트**.

### 3.2 네임스페이스 + 충돌 규칙 (하드 머지 게이트, 예외 없음)
- (a) 병합되는 모든 패밀리는 **정본 접두사**를 단다: 위젯/거버넌스/상태 → `wg-NN-`(`edge-gov-*`→`wg-16-`, `edge-status-*`→`wg-11-`, `module-*`→`wg-04-`); 다이어그램 → `vt-`/`vt-fi-`; 도형 → `shape-`; 아이콘 → `bi-`; editorial 베어네임(`.chron-/.conn-/.ba-/.md-excerpt`)은 `editorial-patterns.css` 안에서만. 페이지의 발명 어휘(`vt-adapt-*/edge-*/module-*/widget-*/fi-*/final-*`)는 **리네임 없이 코어에 진입 금지**.
- (b) **`components.css` 밖의 어떤 컴포넌트도 베어 콜아웃 클래스(`.good/.danger/.term/.analogy`)를 상태 수식자로 재사용 금지** — 수집된 수식자는 전부 네임스페이스형으로 개명(`.wg-16-fnode--ok`, `.wg-11-col--done`, `.shape-use-card--ok`, `.vt-card--ok`). **이 한 규칙이 `index.html:1937–2037`의 `!important` 중화 패치 더미를 근본에서 제거한다.**

### 3.3 새니타이즈 체크리스트 (모든 ADD/REPLACE/MERGE 후보가 착지 전 통과)
1. 모든 `!important` 제거 · 2. `--report-sans`→`--sans`(또는 `--serif`) · 3. font-weight `820/850/870`→`700/800/900` 스냅 · 4. warm/dark 리터럴을 토큰화(`#eee9df`→`--pill-bg` 등)해 다크모드에 참여 · 5. §3.2 (a)+(b) 재네임스페이스 · 6. 모든 상태/심각도에 **색 외 SR 노출 단서** 부여.

### 3.4 해시 경계
- 동결: `theme/components/visual-components/layouts/print` — 편집 시 `core-css-sha256` 마커 + `css-integrity.json`(core_css_sha256 + per-asset + snapshot) 4종을 **한 번에 원자적으로 재베이스라인**.
- 안전: `editorial-patterns/visual-html/widgets/shape-visuals/workflow-visuals/body-icons` — **가능한 한 이쪽으로 라우팅**.

### 3.5 다크 테마 (재설계)
페이지의 `:root:not(:has(#theme-toggle:checked))` + 116클래스 `:is()` `!important` 열거는 **폐기**(임의 생성 콘텐츠를 커버 못 하고, 코어 첫 `!important`를 주입하며, `.good/.danger` 콜아웃 영역까지 침범). 대신:
- `index.html:3117–3129`의 **~40개 토큰 오버라이드 + `color-scheme:dark`만 수확**(이미 AA 검증됨) → 신규 opt-in **`assets/theme-dark.css`**(theme.css 다음 슬롯, hash-safe).
- **`@media(prefers-color-scheme:dark)`를 1순위 게이트**로, 신호 없으면 **라이트가 기본**. 체크박스 토글은 **선택적 오버라이드**로만(토큰 블록에만 `:root:has(#theme-toggle:checked)` 래퍼). 컴포넌트별 규칙 0, `!important` 0.
- **선결조건**: 리터럴을 가진 병합 컴포넌트를 먼저 토큰화하지 않으면 다크모드가 그 컴포넌트에서 조용히 깨진다.

## 4. 결정표

### Tranche A — 해시-safe 가산 병합 (→ v4.6.0, 코어 해시 무변경)
| P | 결정 | 패턴 | 착지 위치 | 핵심 조건 |
|---|---|---|---|---|
| P1 | REPLACE | #18 source-config-excerpt 장문 줄바꿈 | `editorial-patterns.css` `.md-excerpt .code`에 pre-wrap+overflow-wrap | 4패널 만장일치. `.md-excerpt .code`로만 스코프, 베어 `pre`/`.code` 금지. md-excerpt 이름 유지 |
| P1 | REPLACE | #44 edge-status 보드 → **정본 wg-11로 교체** | `widgets.css` wg-11(이미 `wg-11-fill-risk` 줄무늬=색 외 단서 보유) | edge-status-*는 색만으로 심각도 표현(WCAG 1.4.1 회귀) → wg-11 교체가 오히려 회귀 회피. `wg-11-fill-risk` 줄무늬 생존이 수용 기준 |
| P1 | MERGE-VARIANT | #25 vt-19 신규 상태 플래그 아이콘(`fi-*`+3rd warn) | `visual-html.css` `/* 19 flag */` 확장, `vt-fi-*`로 개명, `.switch.warn` 추가 | 진짜 a11y 개선. **단** `fi-`→`vt-fi-` 개명 + `.switch`에 SR 노출 `ON/WARN/OFF` 텍스트 필수(현재 aria-hidden, SR 단서 0) |
| P1 | ADD | #46/#47 접근성 30분 체크 그리드 + 실패모드/릴리스 체크리스트 | **신규 editorial 패턴 08 'accessibility-checklist'** (`editorial-patterns.css` + 템플릿 08 + manifest + ref 행) | 등가물 없음, 온브랜드, PASS/FAIL 리터럴 텍스트(색만 아님). 디톡스: h4 `!important` 제거, `--report-sans`→`--sans`, 다크 리터럴 토큰화 |
| P2 | MERGE-VARIANT | #5 pattern-hero-note(Goal/lede 카드) | `editorial-patterns.css` 콜아웃 variant | shell 쇼케이스 중 유일한 작성자-대면 조각. `.label`을 공유 uppercase/.14em 규약으로 복귀, line-510+668 중복 해소 |
| P2 | MERGE-VARIANT | #13 source-preserve-static(상시 펼침, 무 디스클로저) | `editorial-patterns.css` `.source-preserve` 위 `.source-preserve-static` 수식자 | 무 JS 정적 variant(div+role=group). 클린 머지 |
| P3 | MERGE-VARIANT | #12 core-insight neutral 재스킨 | `.core-insight--neutral` **opt-in 수식자**(베어 `.core-insight` 덮어쓰기 금지) | 베어 덮어쓰면 전 모드 사일런트 회귀. `--report-sans!important` 제거 |
| P3 | MERGE-VARIANT | #15 before/after emphasis-line + ba-bullet | `editorial-patterns.css` `.ba` 패밀리에 추가 | **최종 해결값만** 병합(페이지엔 ba-bullet margin 4연속·emphasis 3연속 override 체인 존재). `ba-bullet`은 장식 aria-hidden |
| P3 | MERGE-VARIANT | #38 static-click-flow → wg-08 static variant | `widgets.css` `wg-08-static-*`, `.static-flow-*`/`.good`→`wg-08-step--ok` 개명 | `:target/:has` 회피 읽기전용 스테퍼(wg-08 대비 이식성↑). 저우선(기존 스테퍼와 중복). 베어 `.good` 충돌 개명 |

### Tranche B — 코어-해시 프리미티브 업그레이드 + 다크 (→ v5.0.0, **단일 원자 재베이스라인**, 사용자 승인 시에만)
| P | 결정 | 패턴 | 착지 위치 | 핵심 조건 |
|---|---|---|---|---|
| P2 | MERGE-VARIANT | #11 다크 테마 | **신규 `assets/theme-dark.css`**(토큰 전용, prefers-color-scheme 1순위, 라이트 기본) | §3.5. 116클래스 열거 폐기. 리터럴 컴포넌트 선토큰화 필요. **사용자 승인 필요** |
| P2 | REPLACE | #49 landing CTA 패널(`landing-action-*`) | 기존 `.cta-box`(`components.css:33`, 코어-해시) **제자리 업그레이드** | 구조 델타만 수확(44px 버튼, panel/proof 구조). `--report-sans!important` 제거, 그림자 토큰화, hover에 prefers-reduced-motion. `landing-action-*` 신규 패밀리 도입 금지 |
| P2 | REPLACE | #50 SEO SERP 미리보기 + 랭킹규칙 그리드(`seo-result-*`) | `.layout-seo .serp-box`(`layouts.css:48`, 코어-해시) 업그레이드 | 모든 셀렉터를 `.layout-seo` 하위 스코프, `--report-sans!important` 제거, dot hex 토큰화, dot aria-hidden 유지. `seo-result-*` 신규 패밀리 금지 |
| P2 | REPLACE | #51 플랫폼 변환 카드 + 브랜치 그리드(`platform-conversion-*`) | `.layout-platform .platform-card`(`layouts.css:55`, 코어-해시) 업그레이드 | base 정의(2601–2816)만, 리듬 블록(2818–2913) 제외. `.search/.dev/.story/.essay` 채널 수식자를 `.layout-platform` 하위로 스코프, h3 `--report-sans!important`×4 제거, 다크 리터럴 토큰화 |

### Phase 3 — 갤러리/레퍼런스 재배치 (hash-safe, A/B 어디든 동승 가능)
| P | 결정 | 패턴 | 착지 위치 |
|---|---|---|---|
| P3 | MERGE-VARIANT | #19 body-icon 갤러리 + #21 soft-shape 테마 갤러리 | **인-스킬 데모/카탈로그 템플릿**으로 승격(신규 `galleries/` 또는 editorial-pattern-templates/), `references/body-icon-system.md:83-85`·`references/visual-template-system.md:113/119`의 **외부 output 경로 링크를 인-스킬 파일로 재지정**. `body-icons.css`/`shape-visuals.css`는 **프리미티브 전용 유지** |
| P3 | MERGE-VARIANT | #4 pattern-shell/nav/meta | **데모 하네스로만** 문서화(`references/editorial-pattern-system.md`), 코어 editorial 콘텐츠 패턴 아님. `.pattern-meta span` 이중정의(510+596) 1개로 해소 |

### SKIP — 스킬에 병합하지 않음 (~30개, 1개 노트로 통합)
- (a) 페이지가 발명한 **제2의 vt-01..21 어휘**(`vt-adapt-*/vt-flow-node/...`, 정본 `.hm-/.rm-/.ft-/.fc-/.wf-` 내부와 평행) → **#1 시스템 발산**으로 오너에게 보고, 이름 수입 금지. editorial 룩이 필요하면 기존 클래스 위 opt-in `.vt-demo.is-editorial` 스킨으로.
- (b) 더 풍부한 스킬 컴포넌트의 **출력측 재스킨 포트**(wg-04/05/06, wg-01/02/03/13/14/18) → KEEP-SKILL(정련된 사용자 규칙).
- (c) 섹션 스코프 **리듬/정렬 정규화 + `.good` 누수 차단 패치**(1937–2037) → 패턴이 아니라 증상. **두 근본 원인(`.good` 수식자 충돌 + `--report-sans` 브리지)을 해결하면 이 ~20개 항목은 자동 소멸**.
- 기타 #7 imported-toc·#8/#16 warm pill·#9 lens-chip → 코어-해시 `components.css`에 warm hex(다크모드 미참여)를 넣고 기존 정본 칩(`.meta span/.tag`)과 중복 → skip. 원하면 `.tag`의 토큰 기반 수식자로만.

## 5. 리스크

1. **베어 `.good` 충돌(최고 레버리지)** — `components.css:38`이 slot 2에서 로드돼 `.good`가 이후 슬롯으로 하향 누수. 11개 패밀리가 `.good`를 green/ok 수식자로 재사용 → 각각 `!important` 중화 패치를 낳음. 완화: §3.2(b) 하드 게이트 + 검증기에 "비콜아웃 셀렉터의 베어 `.good/.danger/.term/.analogy` 거부" 룰.
2. **`!important` 부채 + 게이트 공백** — 검증기에 `!important` 게이트 자체가 없음(F2). 완화: 병합 전에 `important_in_core_css` 게이트 추가(동결 5 + editorial/visual-html/shape/workflow/body-icons에서 0, widgets.css 2건 allowlist).
3. **`--report-sans` 깨진 토큰**(F3) — 완화: forbidden-token 게이트.
4. **코어 드리프트/신뢰불가 소스**(F4) — 완화(릴리스 블로커): `validate_output.py`를 `index.html`에 돌려 `css_integrity_core_hash_mismatch` 발화 여부 확인. 병합 후보를 페이지 인라인 규칙과 절대 diff하지 않음.
5. **해시 경계 오기**(F1) — `layouts.css` 동결. 완화: 가능한 hash-safe로 라우팅, 불가피한 코어 편집은 단일 원자 재베이스라인.
6. **다크 `:has()` 취약 + 반전된 기본** — `:root:not(:has())`는 다크가 기본 + OS 무시 → :has() 미지원 구형에서 우연히만 라이트로 폴백, OS-라이트 광과민 사용자에게 강제 다크. 완화: §3.5.
7. **네임스페이스 게이트 휴면**(F6) — 페이지 접두사가 어떤 게이트도 안 침. 완화: bespoke 접두사 denylist로 게이트 확장 + `role=img` prune 게이트를 `.wf-board` 너머로 확장.
8. **색 외 단서** — vt-03 risk-matrix·vt-18 triage dot 여전히 색만, edge-status-fill 색만(#44 wg-11 교체로 치유), vt-19 `.switch` SR 텍스트 없음. 완화: #44는 줄무늬 보존, #25는 SR `ON/WARN/OFF` 추가, 정본 `.rm-risk`에 shape/text 단서 후속.
9. **`.skill` 재패키징 공백**(F5) — 완화: 버전 범프 + design 필드 갱신 + 해시 재생성 + CHANGELOG + 재집(필수 산출물).

## 6. 단계별 롤아웃

- **Phase 0 — 거버넌스 선결(모든 CSS 병합 전).** (a) `validate_output.py`를 `index.html`에 실행해 `css_integrity_core_hash_mismatch` 기록, `.kicker` 드리프트 reconcile, 페이지를 "무드보드(스펙 아님)"로 확정. (b) **같은 버전 범프에 신규 정적 게이트 착지**: `important_in_core_css`, `--report-sans` forbidden-token, 베어 콜아웃 수식자 거부, 휴면 wg-/vt-/shape-/role=img 게이트를 bespoke-접두사 denylist로 확장. (c) §7 오픈 퀘스천 사용자 승인.
- **Phase 1 — Tranche A(해시-safe 가산, v4.6.0).** §4 Tranche A 전부, 각 항목 새니타이즈 체크리스트 통과. 모든 변경에 Phase-0 게이트 실행.
- **Phase 2 — Tranche B(코어-해시 프리미티브 업그레이드 + 다크, v5.0.0, 단일 원자 재베이스라인).** 사용자 승인 시에만. #49/#50/#51 제자리 업그레이드 + theme-dark.css. 한 커밋에서 4종 해시 일관 재생성. 선결: 리터럴 컴포넌트 선토큰화.
- **Phase 3 — 갤러리 + 레퍼런스 재배치(hash-safe).** #19/#21 인-스킬 데모 승격, 외부 경로 링크 재지정, #4 데모 하네스 문서화. 프리미티브 전용 유지.
- **Phase 4 — 검증·패키징·버전 범프(필수 마감).** `examples/` + **사후 재생성 쇼케이스**에 게이트 재실행(다음 디자인 리뷰가 정직하도록 index.html을 병합 후 스킬에서 재생성). SKILL.md/manifest 버전 범프(A만=v4.6.0 / B·다크 포함=v5.0.0), stale `manifest.json:140` design 필드 갱신, tranche별 CHANGELOG, **`.skill` 재집**(v4.3.3→현행 공백 해소).

## 7. 사용자 결정 필요 (open questions)

1. **다크 테마** — 출시 여부와 기본값? (권장: 토큰 전용 `theme-dark.css`, `prefers-color-scheme` 1순위 + 라이트 기본 + 선택적 토글 오버라이드. 페이지의 116클래스 `!important` 열거 폐기. v5.0.0 플래그십 + 코어 재베이스라인.)
2. **코어-해시 프리미티브의 'replace' 범위**(#49/#50/#51 CTA/SERP/platform) — Tranche B로 지금 진행(코어 재베이스라인) vs 보류(그러면 Tranche A가 해시 무변경 클린 v4.6.0로 선출시).
3. **정련된 사용자 규칙 사인오프** — "정본이 더 풍부하면 KEEP-SKILL(skip)" 트리아지(실 병합 ~9 + 재배치 ~3 + skip ~30) 수용 여부.
4. **골든/쇼케이스 재생성** — 병합 후 스킬에서 쇼케이스를 재생성해 재리뷰(권장). 기존 `output/final_20260604`는 교체 vs 히스토리 아티팩트로 보존?
5. **vt-01..21 병렬 어휘** — 리네임 수입 거부 + 필요 시 opt-in `.vt-demo.is-editorial` 스킨, 그리고 이 포크를 #1 시스템 발견으로 오너에게 보고하는 방향 수용 여부.

## 부록 — 전문가 패널 평결
- 에디토리얼/비주얼 디자인 리드: endorse-with-revisions (병합본이 스킬 현행을 실제 개선하는지, 디자인 언어 분절 방지에 집중)
- CSS 아키텍처/유지보수 리드: endorse-with-revisions (`!important`·베어클래스 누수·`:is()` 열거의 일반화 불가 지적, 토큰 전용 다크 처방)
- 접근성 리드: endorse-with-revisions (토글 포커스/키보드/prefers-color-scheme, 색-단독 단서, 무 JS 준수)
- 스킬-시스템/거버넌스 리드: endorse-with-revisions (manifest/ref/게이트/골든 v6 회귀, 코어 vs 신규 ref 귀속, 재패키징·버전 범프)

> 전체 52패턴 인벤토리 + 4개 리뷰 원본은 워크플로 산출물(run `wf_e4c0f76f-4c6`)에 보존됨.
