# Changelog — adaptive-html-final

## v5.2.3 (2026-06-05) — editorial-patterns 가독성 승격

쇼케이스에서 반복 적용하던 일반 가독성 보정을 스킬 기본값으로 승격. 무 JS, `!important` 0, 조건부 자산(`editorial-patterns.css`)만 변경 — **코어 해시 불변**.

### 변경 (`assets/editorial-patterns.css`)
- **`.a11y-card`** 내부 줄 간격 `gap:8px → 12px`, **`.a11y-points`** `gap:5px → 9px` — 접근성 점검 카드의 헤드/제목/PASS·FAIL 줄이 너무 붙던 문제 완화.
- **`.impact-card .body-icon`** `display:grid;margin-bottom:12px` 추가 — impact 카드에서 아이콘이 제목/수치에 바로 붙던 문제 해소(아이콘 ↔ 텍스트 12px 간격).

### 영향·검증
- `editorial-patterns.css`는 조건부 자산이라 **core-css-sha256 불변**. `output/adaptive-html-final-13-topics-20260605_083433/`의 인라인 `editorial-patterns.css`·스냅샷·`css-integrity.json`·source manifest를 v5.2.3로 재생성, `validate_output.py` **OK** 유지.

## v5.2.2 (2026-06-05) — 아이콘 박스 테마 적응 + lede-note 라벨 정렬

쇼케이스/템플릿 점검에서 확정된 보편 결함을 스킬 기본값으로 승격. 무 JS(`:has()`), `!important` 0, 조건부 자산(`body-icons.css`)만 변경 — **코어 해시 불변**.

### 변경 (`assets/body-icons.css`)
- **아이콘 박스 배경 테마 적응**: `.body-icon` 박스 배경이 하드코딩 흰빛 그라디언트라 다크/화이트 테마에서 그대로 떠 보이던 문제를 해소. `:root:has(#ahf-white:checked)`=순백, `:root:has(#ahf-dark:checked)`=카드 표면(`var(--vt-soft)`→`var(--card)`, border `var(--line)`). 라이트는 기존 크림빛 유지. SVG 칠(bi-*)은 이미 토큰 기반이라 그대로 적응.
- **lede-note 라벨 정렬**: `.lede-note .label{display:block}`(고특이도)이 v5.2.1의 `.label:has(>.body-icon){display:flex}`를 무력화하던 문제를 `.lede-note .label:has(>.body-icon)`(0,3,0)로 보강.

### 영향·검증
- `body-icons.css`는 조건부 자산이라 **core-css-sha256 불변**. `output/adaptive-html-final-13-topics-20260605_083433/`의 인라인 `body-icons.css`·스냅샷·`css-integrity.json`(conditional hash)·source manifest를 v5.2.2로 재생성, `validate_output.py` **OK** 유지.
- 같은 결함을 가진 `output/final_20260604/index*.html`(반례 데모)도 향후 재인라인 시 자동 적용.

## v5.2.1 (2026-06-05) — body-icon 정렬 규칙 + 헤더 폭 정련

쇼케이스 인덱스 검수에서 확정된 정렬·폭 개선 2건을 스킬 기본값으로 승격. 전부 무 JS(`:has()`), `!important` 0.

### 변경
- **`assets/body-icons.css`**: `body-icon`을 직접 자식으로 갖는 `.label`/`h1`/`h2`/`h3`를 **flex 왼쪽 아이콘 + 일정 간격(gap 8~10px)**으로 정렬. `.mini-card`/`.card-block` 카드 제목 아이콘은 2줄 제목에서 상단 정렬(`align-self:flex-start`). 헤딩·라벨 전반의 아이콘↔텍스트 간격 일관화.
- **`assets/theme.css`**: `.header` 콘텐츠의 **48rem 단일 측정 캡 해제**(`max-width:none`). 헤더가 `.page`/`.page-wide` 컨테이너 폭에 맞춰 **아래 섹션과 동일 폭**으로 정렬(특히 wide 레이아웃에서 헤더가 768px로 좁던 문제 해소).

### 영향·검증
- `theme.css`가 코어 해시 자산이라 **core-css-sha256 변경** → `output/adaptive-html-final-13-topics-20260605_083433/` 기준선의 인라인 CSS·코어 마커·CSS 스냅샷·`css-integrity.json`을 v5.2.1로 재생성, `validate_output.py` **OK** 유지.
- 인덱스 전용 미세 튜닝(상단 kicker 폰트 11px, 인트로 `text-align:justify`)은 갤러리 취향이라 스킬에 승격하지 않고 해당 `index.html` 페이지-로컬 오버라이드로만 유지.

## v5.2.0 (2026-06-05) — CSS-only 3-테마 시스템 (라이트·완전 화이트·다크)

기존 라이트(크림)/다크 2-테마에 **완전 화이트(순백) 테마**를 추가해 **3-테마**로 확장. 단일 체크박스 토글을 **라디오 3-세그먼트 스위처**(`name=ahf-theme`: `#ahf-light`/`#ahf-white`/`#ahf-dark`)로 교체. 전부 `:has()` 기반 **무 JS**, 코어 CSS 무수정(해시-safe), `!important` 0.

### 추가/변경 (`assets/theme-dark.css` → 테마 시스템)
- **화이트(순백)**: `:root:has(#ahf-white:checked)` — neutral 토큰만 쿨·순백(`--bg/--card #fff`, `--line #e4e4ea`, `--ink #16181d`, `--vt-* #fff`); accent·콜아웃 유지. 라이트(크림 `#f5f5f0`)와 명확히 구분.
- **다크**: `:root:has(#ahf-dark:checked)` + 표면 보정(이전과 동일, proper-black `#0c0d10`).
- **스위처**: `.ahf-themebar` 세그먼트 컨트롤(숨긴 라디오 + 라벨, `input:checked + label`=accent 활성, focus-visible 링). 기본=라이트, 마크업 없으면 라이트 고정.
- 이전 `#theme-toggle` 체크박스(invert) 방식은 3-라디오로 대체.

### 검증
- Playwright 3-테마 전환 실측: body bg 라이트 `#faf9f5` / 화이트 `#ffffff` / 다크 `#0c0d10`. 화이트 ink/bg 17.8:1. self-test 16/16.

### 후속 하드닝 (5.2.0 라인 · 2026-06-05)
- **결정론 문서 동기화** (`AGENTS.md`·`SKILL.md`): 버전 하드코딩 제거(→ `manifest.json` 일치), CSS 순서표·슬롯 인덱스에 `theme-dark.css`/`{{THEME_DARK_CSS}}` 추가(누락됐던 `SHAPE_VISUALS`/`WORKFLOW_VISUALS` 포함), 테마 스위처(`name="ahf-theme"`) 삽입 규칙 + 불변식 "3-테마 단일 계약"(legacy `#theme-toggle` 금지), `auto = 혼합/기본(auto≠diagram)` 명확화, 본문 구조 패턴 **8종**(`accessibility-checklist` 포함, 템플릿 `01..08`) 정정.
- **검증기 강화** (`scripts/validate_output.py`): (1) 조건부 CSS 스냅샷·`asset_sha256` 기록 해시를 현재 스킬과 대조(있을 때만; stale `theme-dark.css` 등 차단), (2) source manifest를 버전만이 아닌 **내용 전체** 비교(`source_manifest_content_mismatch`), (3) legacy `#theme-toggle` 가드(`legacy_theme_toggle`). self-test 16 → **24** (legacy-toggle fixture 3종 추가).
- **M6 모바일 표/매트릭스**: `<table>` 보유 위젯(`wg-06`/`12`/`15`/`16`)을 `.table-scroll`로 래핑(`table_no_mobile_safe_wrapper` 게이트 충족), vt-03 리스크 매트릭스 `.rm-grid`에 모바일 규칙(`minmax` 바닥 + `overflow-x:auto`) 추가.
- 쇼케이스 출력(`13-topics`)을 현재 자산으로 재인라인·재스냅샷, `.skill` 재패키징(stale `__pycache__/*.pyc` 정리).

## v5.1.0 (2026-06-05) — 글꼴(Pretendard sans 제목)·헤더 반영 + proper-black 다크 (디자이너 검토)

`output/final_20260604/index.html`의 **글꼴**과 **헤더 섹션(SVG 제외)**을 스킬에 반영하고, 다크 테마를 **"proper black"**으로 교정했다. 전문 시각 디자이너 + 레이아웃 스타일 디자이너 에이전트 2인 검토 결과를 반영. 코어 해시 재베이스라인(`b04221bd…`→`fea7b026…`). 무 JS·코어 `!important` 0 유지.

### 글꼴 — report 룩(sans 제목)
- `--serif` 토큰을 Pretendard sans 스택으로 전환(제목·디스플레이가 Noto Serif KR → Pretendard sans). 진짜 세리프는 `--serif-kr`로 보존하고 `blockquote`/`.pull-quote`/`.core-insight blockquote`에만 적용(에디토리얼 대비).
- 디자이너 검토 반영: sans 제목은 700→**800** 무게 + 트래킹 강화(h1 -.025em/lh1.22, h2 -.02em/lh1.3, h3 -.015em).

### 헤더 — final_20260604 반영(SVG 제외)
- `.kicker`를 **점 달린 pill eyebrow**로(토큰화 → 다크 자동). `.kicker-text` 추가.
- `.generated-row` + `.generated-date` + `.lens-strip` + `.lens-strip-label` + `.lens-chip`(적용 기준 칩) 추가 — 페이지 warm 리터럴을 쿨 토큰으로.
- no-SVG 단일 컬럼 헤더에 **측정 캡**(`.header` 자식 `max-width:48rem`)으로 제목/본문 우측 정렬. 헤더 리듬 재튜닝(kicker→h1 24, meta 24, generated-row 16, `--space-*` 정렬).

### 다크 — proper black (디자이너 P1)
- 팔레트 교정: `--bg #15161a→#0c0d10`(near-black), `--card #1e2026→#1a1c22`(lifted, 카드 분리), `--line→#2c2d34`, `--dark→#000`(true-black `.try` hero), `--code→#070809`.
- **AA 교정**: `--on-accent` 토큰 신설(라이트 `#fff`, 다크 `#0c0d10`) — accent 버튼/배지 흰 텍스트의 AA 미달(라이트 4.17·다크 2.76)을 해소(다크 on-accent 7:1). `.cta-btn.primary`·`h2 .no.is-key`에 적용.
- **다크 커버리지 갭 차단**: `widgets.css`·`visual-html.css`의 흰 카드 `background:#fff` 38곳을 `var(--card)`로 토큰화(라이트 동일, 다크 자동 반전) — 위젯/vt 템플릿이 다크에서 흰 섬으로 남던 문제 해결.
- **"전혀 블랙이 아니다" 근본 원인 수정(실제 렌더 캡쳐로 진단)**: `visual-html.css`가 `body{background:var(--vt-wash)}`로 페이지 배경을 자체 `--vt-*` 토큰(다크 미적용)으로 덮어 다크에서도 `#faf9f5`(밝은 wash)로 남던 버그. theme-dark가 `--vt-paper/--vt-wash/--vt-soft`(+ vt-blue/green/gold 명도 상향)를 다크로 덮도록 추가 → body 배경 `#0c0d10`(near-black) 확정(Playwright 캡쳐 검증). `widgets.css` 흰 글레이즈 `rgba(255,255,255,…)` 7곳→`var(--card)`(wg-11 빗금 보존), `.core-insight` 흰 글레이즈 그라데이션→다크 그라데이션, vt-pill.hot/good/watch 다크 틴트. theme-dark 토글 `th,.table th` 콤마 스코프 누수 수정.
- **양방향 토글 수정(OS 다크에서 화이트 전환 불가 버그)**: 기존 토글은 dark를 "추가"만 해서 OS가 다크면 토글로 라이트 복귀가 불가능했음. **invert 패턴**으로 재작성 — `@media(prefers-color-scheme:dark) :root:not(:has(#theme-toggle:checked))`(OS다크 기본 다크, 토글 시 라이트) + `@media(light/no-preference) :root:has(#theme-toggle:checked)`(OS라이트 토글 시 다크). 4조합(OS×토글) 전부 검증: light/dark/dark/light. 아이콘은 현재 테마 표시(다크=달/라이트=해). 토글 마크업 없으면 OS 자동만 동작.
- **다크 텍스트 대비 감사(Playwright로 전 텍스트 노드 대비 계산 + 풀페이지 캡쳐)**: 안 보이는 텍스트 패치 — `.try .tag`(밝은 pill+`var(--ink)` 텍스트가 다크에서 light-on-light 1.18:1 → 다크 pill `var(--card)`/`var(--line)`로 보정), `visual-html.css`의 `.vt-pill`·`.vt-fit`(`color:#555`)·`.vt-tags span`·`.cf-state`(`#666`)·`#6e6258` + `widgets.css` `#7c7c78` 리터럴 회색 텍스트를 `var(--ink-mute)`로 토큰화(다크 자동 반전). 종합 kitchen-sink(`output/adaptive-html-final-dark-coverage-test`)에서 저대비 텍스트 **0건** 확인.
- theme-dark 토글 블록의 `th,.table th` 셀렉터 스코프 버그 수정(콤마로 인한 라이트 누수 차단).

## v5.0.0 (2026-06-05) — Tranche B: 다크 테마 + 코어 프리미티브 업그레이드 (코어 해시 재베이스라인)

`final_20260604` 병합 Tranche B. **토큰 전용 다크 테마**를 추가하고, 코어 프리미티브(`.cta-box`/`.serp-*`/`.platform-card`)를 "replace-the-primitive"로 제자리 업그레이드했다. 후자가 **코어 5개 동결 자산(theme/components/visual-components/layouts/print)을 수정**하므로 코어 해시가 재베이스라인된다(메이저 범프). 골든 v6는 v4.x 역사 베이스라인으로 남는다. 페이지 발명 어휘(`landing-action-*`/`seo-result-*`/`platform-conversion-*`)는 도입하지 않고 기존 정본 클래스만 강화. 무 JS·`!important` 0(코어) 유지.

### 추가 — 다크 테마 (hash-safe, 코어 무수정)
- `assets/theme-dark.css` — **토큰 전용 `:root` 오버라이드**(37개 색 토큰). `@media(prefers-color-scheme:dark)` 1순위 + **라이트 기본** + 선택적 `:root:has(#theme-toggle:checked)` 강제 다크. 페이지의 116-클래스 `!important` 열거는 폐기. 표면 보정 6개(prompt-box/code/th/status-pill/timeline-card/serp-url)만, `!important` 0.
- `base.html`에 `{{THEME_DARK_CSS}}` 슬롯(print 뒤) + manifest `dark_theme` 블록 + `references/editorial-design-system.md` 다크 테마 절. 선택 토글 버튼(체크박스+라벨, 무 JS).

### 변경 — 코어 프리미티브 업그레이드 (코어 해시 재베이스라인)
- `.cta-box`(components.css): `.cta-actions`/`.cta-btn`(44px 터치, primary/secondary)/`.cta-proof-grid`/`.cta-proof` 추가. translateY hover에 `prefers-reduced-motion` 폴백.
- `.layout-seo .serp-*`(layouts.css): `.serp-desc`/`.serp-dots`(검색 점열)/`.serp-checks`(칩, `.ok`)/`.serp-rule-grid`/`.serp-rule`(`.is-wide`) 추가. 전부 `.layout-seo` 스코프, `--report-sans`→`var(--sans)`, dot hex 토큰화.
- `.layout-platform .platform-card`(layouts.css): 채널 코딩 `.is-search/.is-dev/.is-story/.is-essay` 좌측 보더(토큰) + `.platform-kicker`. 제네릭 충돌 방지 위해 `.layout-platform` 스코프 + `is-` 접두.

### 게이트 (부수 개선)
- 자산 린터를 **주석-인식**(`/* */` 마스킹)으로 교정(prose 속 `!important` 오탐 차단) + `theme-dark.css`를 `important_in_core_css` 린트 대상에 편입. self-test 16/16.

### 비고
- 코어 해시 변경: v4.x `3e6a8bfa…` → v5 `b04221bd…`. 기존 출력물은 재검증 시 해시 불일치(재생성 필요). 새 데모는 v5 해시로 재생성됨.

## v4.6.0 (2026-06-05) — final_20260604 섹션 Tranche A 흡수 & 병합 보호 게이트

`output/final_20260604/index.html`(무신뢰 디자인 소스)의 섹션 패턴 중 **재사용 가치가 검증된 9종을 흡수**했다. 페이지 발명 어휘(`access-*`/`edge-*`/`pattern-hero-note`/`static-flow-*`/`vt-flag`/`fi-*`)는 모두 **정본 네임스페이스로 개명**하고, `!important`·`--report-sans`·warm 리터럴·베어 콜아웃 충돌을 제거한 뒤 토큰화했다. 코어-해시 5개 자산(theme/components/visual-components/layouts/print)은 **무변경**(전부 hash-safe 경로). 무 JS 원칙 유지.

### 추가 (Phase 0 — 병합 보호 거버넌스 게이트)
- `scripts/validate_output.py` — 자산 린터 3종(`important_in_core_css`, `forbidden_report_font_token`, `bare_callout_modifier`) + 출력 게이트 2종(`bespoke_namespace_class` denylist, `role_img_buries_text` 일반화). `--skill-dir` 제공 시 스킬 자산을 린트.
- `tests/test_governance_gates.py` — 게이트 16개 체크 stdlib 자체 테스트(회귀 방어).

### 추가/변경 (Phase 1 — Tranche A 9종 병합)
- editorial 패턴 **08 `accessibility-checklist`** 신규(`a11y-*`): 30분 점검 그리드 + 실패 모드 표(caption+`.table-scroll`) + 다크 릴리스 체크. 상태는 PASS/FAIL **텍스트 칩**(색 외 단서). `editorial-pattern-templates/08-accessibility-checklist.html`, manifest editorial_patterns 7→8.
- callout·헬퍼(opt-in, 패턴 수 미증가): `.lede-note`(←pattern-hero-note), `.source-preserve-static`, `.core-insight--neutral`, before/after `.ba-emphasis-line`+`.ba-bullet`.
- `.md-excerpt .code` 긴 줄 줄바꿈(`pre-wrap`+`overflow-wrap:anywhere`).
- vt-19 feature-flag **3-상태 토글**(`.switch.on/.warn/.off`) + 가시·SR 텍스트 라벨(`.flag-state`) — 색-단독 회귀 해소.
- `wg-11` ≤480px 라벨 적층 + 상태/거버넌스 보드 정본 통일(빗금 `wg-11-fill-risk` 비색 단서 보존).
- `wg-08-static-*` — `:target/:has` 없는 읽기전용 스테퍼(←static-flow-*).

### 추가 (Phase 3 — 인-스킬 갤러리)
- `galleries/body-icons-catalog.html`(32종)·`galleries/soft-shapes-catalog.html`(36종) — 외부 `output/` 경로 링크를 인-스킬 데모로 재배치. `body-icons.css`/`shape-visuals.css`는 프리미티브 전용 유지. manifest에 catalog/gallery 필드 등록.
- `pattern-shell`을 **데모 하네스**(콘텐츠 패턴 아님, 정식 출력에선 denylist)로 문서화.

### 비고
- Tranche B(토큰 전용 다크 테마 + CTA/SERP/platform 코어-해시 제자리 업그레이드)는 v5.0.0에서 별도 진행. 전략: `MERGE_STRATEGY_final-20260604.md`.

## v4.5.0 (2026-05-31) — SVG→HTML 템플릿 편입 & 하네스 정형화

SVG로 그리던 본문 삽입 다이어그램을 순수 HTML+CSS 뷰 템플릿(`vt-`)으로 정식 편입하고, 이후 vt-21 `soft-workflow-map`까지 포함해 현재 21종으로 확장했다. 모드→템플릿 결정론 진입점과 정적 게이트로 하네스를 정형화했으며, 무 JS 원칙(외부/동작 JS 0, JSON-LD만 허용)은 전 항목에서 유지된다.

### 추가
- `assets/visual-html.css` — SVG→HTML 뷰 템플릿 21종 스타일.
- `assets/visual-html-templates/01..21.html` 21종 — `vt-` 본문 삽입 다이어그램 골격(hero-map, decision-tree, risk-matrix, timeline, checklist-flow, quality-gate, card-grid, raci, file-tour, flowchart, weekly-status, incident-summary, comparison-cards, process-swimlane, concept-explainer, implementation-plan, pr-writeup, triage-board, feature-flag, prompt-tuner, soft-workflow-map).
- `references/visual-html-system.md` — 캐노니컬 모드→vt 템플릿 매핑(첫=1순위, 단일 출처), 선택·삽입 규칙.
- `AGENTS.md` — 결정론 진입점(모드 입력→vt 선택을 단일 출처로 고정).

### 캐노니컬 모드→vt 매핑 (첫=1순위, 단일 출처)
- beginner_html: concept-explainer, hero-map, checklist-flow
- expert_html: risk-matrix, raci, quality-gate, implementation-plan, soft-workflow-map
- article_html: decision-tree, comparison-cards, concept-explainer
- education_html: timeline, checklist-flow, concept-explainer, soft-workflow-map
- blog_writer: timeline, weekly-status, comparison-cards
- seo_dashboard: card-grid, comparison-cards, prompt-tuner
- platform_blog: card-grid, comparison-cards, pr-writeup
- skill_audit: quality-gate, file-tour, prompt-tuner, implementation-plan, soft-workflow-map
- reference_html: file-tour, flowchart, card-grid
- comparison_html: comparison-cards, decision-tree, risk-matrix
- case_study_html: incident-summary, timeline, process-swimlane
- landing_brief_html: hero-map, card-grid, feature-flag, soft-workflow-map
- checklist_playbook: checklist-flow, quality-gate, process-swimlane, implementation-plan, triage-board

### 변경
- `SKILL.md`: 모드→vt 결정표 추가(캐노니컬 매핑을 단일 출처로 참조).
- `assets/base.html`: `{{WIDGETS_CSS}}` 슬롯 바로 뒤에 `{{VISUAL_HTML_CSS}}` 슬롯 추가(인라인 순서 widgets → visual-html → layouts 유지).
- `scripts/validate_output.py`: `vt-` 게이트 추가(visual-html 템플릿 사용 시 정적 검사).
- `manifest.json`: 버전 4.5.0, assets에 `assets/visual-html.css` 추가, `visual_html_templates` 배열(01~21) 등록, changes 항목 추가, updated 2026-05-31.

### 적용 데모
- `showcase-v6` — 동결 시점 기준 SVG→HTML 템플릿 20종을 모드별로 적용한 골든 갤러리(vt-21은 후순위 편입이라 골든 본문에는 필수 등장하지 않음).

### 검증
- `assets/visual-html-templates/*.html` 21종 모두 외부/동작 `<script>` 0건(무 JS 0, JSON-LD만 허용).
- `manifest.json` `python json.load` 유효성 통과, `visual_html_templates` 21개 실제 파일 경로 일치.

### 본문 아이콘 세트 편입 (2026-06-01)
본문용 compact 아이콘 32종을 정식 편입했다. 섹션 제목·콜아웃·카드 옆에 의미를 보조하는 인라인 SVG 장식(외부/동작 JS 0, `aria-hidden="true"`)이며 스킬 디자인 토큰을 쓴다.
- `assets/body-icons.css` — `bi-` 네임스페이스 렌더 CSS(8 클래스: line/accent-line/fill/soft/accent/accent-box/dot/dot-box) + `.body-icon`/`--sm`/`--plain` 래퍼. 프로파일 무관 조건부 인라인.
- `assets/body-icons.json` — 32종 `{id, label, usage, svg}`(viewBox 0 0 40 40). id: idea·source·timeline·connection·edit·check·impact·reference·warning·success·question·compare·decision·metric·search·file·code·database·security·user·flow·map·quote·note·learning·platform·audit·case·landing·api·prompt·experiment.
- `references/body-icon-system.md` — 32종 카탈로그·모드별 추천·삽입/접근성 규칙.
- `assets/base.html`: `{{BODY_ICONS_CSS}}` 슬롯 추가(visual-html 뒤). `manifest.json`: assets + `body_icons` 메타(count 32).
- `scripts/validate_output.py`: body-icon 게이트(아이콘 사용 시 body-icons.css 인라인·`aria-hidden` 강제).

### wg-03 PR diff 가시성·정렬 수정 + md-excerpt 패턴 (2026-06-01)
skill_audit "좋은 출력은 어떻게 생겼나"(주석 달린 PR) 섹션의 두 결함과 SKILL.md 발췌 표기를 보강했다.
- `assets/widgets.css` wg-03: diff 코드가 안 보이던 버그 수정 — `<code class="wg-03-code">`가 코어 `code{background:#ececea}`(밝음)에 덮여 밝은 텍스트가 밝은 배경에 묻혔다. `.wg-03-diff code,.wg-03-code{background:none;border:0;border-radius:0;font-size:inherit}` 리셋으로 다크 diff 패널에 코드가 보이게. (wg-01/13/14는 `.wg-XX-code`에 다크 배경을 직접 줘서 무관.)
- `assets/widgets.css` wg-03 정렬: `.wg-03-grid{align-items:stretch}` + `.wg-03-diff{align-self:stretch}`로 diff(좌)·리뷰 노트(우)를 **같은 높이로 통일**(이전 `align-items:start`로 좌측이 짧아 우측과 틈 발생).
- `assets/editorial-patterns.css` + `editorial-pattern-templates/07-md-excerpt.html`: **md-excerpt 패턴** 추가(7번째) — SKILL.md/마크다운/코드 발췌를 `.prompt-box` 텍스트가 아니라 다크 코드 블럭(`pre.code`)에 마크다운 소스 그대로 표기.
- `references/skill-audit-system.md`·`editorial-pattern-system.md`: 발췌=코드블럭, 주석 PR=wg-03 다크 diff·stretch 정렬 규칙 명문화. `manifest.json` editorial_patterns count 6→7.
- 적용: showcase-v5 page 08 — wg-03 diff 코드 가시·좌우 475=475 균등, SKILL.md 발췌 3종 코드블럭화(콘텐츠 무변경). validate OK·무 JS 0.

### 자체 검증 회귀 게이트 강화 R1–R5 (2026-06-01)
지금까지 실측 수정한 결함이 다시 발생하지 않도록 `scripts/validate_output.py`에 정적 회귀 게이트 5종을 추가하고, `references/quality-gates.md`에 "v4.5.0 Regression Gate"로 명문화했다.
- **R1 `platform_grid_wrapper_misuse`** — `div.platform-grid`에 `<h2>`/`.card-grid`/`.h2-sub`를 중첩하면 검출(카드 직접 보유만 허용, 섹션 래퍼는 `<section>` 사용).
- **R2 `wg03_diff_code_bg_not_reset`** — wg-03 **마크업** 사용 시 `.wg-03-diff code{background:none}` 리셋 누락 검출(다크 diff 코드 가시성).
- **R3 `wg03_grid_not_stretch`** — `.wg-03-grid{align-items:stretch}` 누락 검출(좌우 컬럼 높이 통일).
- **R4 `table_no_mobile_safe_wrapper`** — `.table-scroll`/카드 변환 없는 `<table>` 검출(모바일 가로 넘침 방지).
- **R5 `wide_layout_prose_cap_missing`** — `.page-wide` 분석 폭 레이아웃에 본문 60rem 상한 override 누락 검출(와이드 섹션 본문이 1/3만 차는 문제).
- 검증: R2/R3은 인라인 widgets.css의 CSS 텍스트가 아니라 **wg-03 마크업 사용**에서만 발동하도록 정밀화(widget/auto 프로파일 오발동 0). 3 프로파일 골든(widget/auto/diagram) 전부 `OK` 유지, 픽스처 10/10 통과.

### vt-21 soft-workflow-map 편입 (8816, 전문가 검토 반영, 2026-06-01)
크림톤 "AI 카드뷰" 워크플로우 맵을 본문 삽입 HTML+CSS 다이어그램으로 vt- 라이브러리에 **vt-21**로 편입(20→21종). 아키텍처/IA + QA/접근성 2인 전문가 검토 후 진행.
- `assets/visual-html-templates/21-soft-workflow-map.html` — `vt-shell`/`vt-frame` 셸 + `wf-` 접두사. 좌 3카드 ∥ 중앙 대시보드(코드창·미니대시·지표·파이프) ∥ 우 3카드 수렴형(기존 hero-map 단일 축과 구별).
- **접근성 수정(전문가 지적 반영)**: 원본의 `role="img"`+단일 `aria-label`은 내부 카드/지표 텍스트 12블록을 스크린리더에서 prune하므로 **제거**. 텍스트는 일반 DOM 노출, 순수 장식(`wf-codewin`·`wf-dash`·`wf-pipes`·`wf-bottom`·`wf-icon`·`wf-aistack`)에만 `aria-hidden`. raster PNG 제외(SVG-first·자기완결).
- `assets/visual-html.css`에 `.wf-*` 추가(스킬 토큰화, 코어 해시 비대상). 모바일 계약: `@820px` wf-map 1컬럼, `@520px` 지표 1컬럼·장식 connector 숨김.
- 매핑: expert/education/skill_audit/landing_brief의 **후순위**(1순위 불변 → 골든 v6 회귀-0 보존). SKILL §0.6/§4.7·AGENTS §3/§8.2·`references/visual-html-system.md`(카탈로그 21·접근성 규칙) 반영.
- 게이트: `soft_workflow_gate`(opt-in `wf-board`) — role=img 금지·장식 aria-hidden·raster 금지·모바일 접힘·CSS 인라인. 렌더 1280/390px overflow 0, 무 JS 0 확인.

### Soft Shape 도형 36종 편입 (8817, 전문가 검토 반영, 2026-06-01)
"본문 설명 시작부 보조 도형" 36종을 신규 무거운 라이브러리 대신 **visual-template-system(8000×6000 SVG)의 soft-shape 카탈로그**로 흡수(전문가 합의: 캔버스·`figure.visual-figure` 매체 동일 → 중복 최소화).
- `assets/shape-svgs/*.svg` 36종(8000×6000 warm SVG, `<title>/<desc>` 접근성, 무 JS) + `assets/shape-catalog.json`(id/label/usage).
- `assets/shape-visuals.css`(`.shape-figure`/`.shape-lead`/`.shape-grid`, 프로파일 무관 조건부) + `base.html` `{{SHAPE_VISUALS_CSS}}` 슬롯(editorial 뒤). 코어 해시 비대상.
- 삽입 표준: `<figure class="shape-figure"><img class="shape-img" …8000×6000 alt="…"></figure>`(visual-figure 아님 — 앵커라 figcaption 선택). `alt`는 `shape_visual_gate`가, svg 존재는 `broken_local_ref`가 검사. 도형은 시각 앵커, 핵심 정보는 HTML 텍스트.
- 경계: 글자 옆 장식=`bi-`(40×40), 본문 구조도=`vt-`(HTML), 시작부 프리뷰=soft-shape(8000×6000 img) — 상호 비대체.
- `references/visual-template-system.md`(카탈로그 36·삽입 패턴·모드별 추천)·SKILL §4.5/자산맵·AGENTS §8.1·`manifest.json` `shape_visuals` 메타 반영.
- 게이트: `shape_visual_gate`(opt-in `shape-figure/img/lead/grid`) — CSS 인라인·빈 alt 금지·네임스페이스 누수. 두 편입 모두 신규 게이트 opt-in이라 3 프로파일 골든 `OK` 바이트 불변(회귀 0). 버전은 4.5.0 유지(frozen 골든 v6의 sources 버전 보존 — bump 시 `source_version_mismatch`).

### Soft Workflow 도판 10종 편입 (8819, 전문가 검토 반영, 2026-06-01)
8817·8816의 후속 — soft 스타일 8000×6000 SVG 워크플로우 도판 10종을 visual-template-system에 흡수(아키텍처/IA + QA/접근성 2인 검토). soft-shape(작은 앵커)와 달리 "본문 대표 도판/섹션 상단 구조도/랜딩 카드"용 **와이드**.
- `assets/workflow-svgs/01..10.svg` — Linear Pipeline·Radial Agent Hub·Decision Router·Layered Stack·Quality Funnel·Knowledge Graph·Agent Swarm·Timeline Delivery·Comparison Board·Governance Operating Model. 8000×6000, `<title>/<desc>` 접근성, 무 JS, warm cream. + `assets/workflow-catalog.json`(id/label/usage 정규화).
- `assets/workflow-visuals.css` — `.workflow-figure`(와이드 ~720px, `object-fit:contain`, 모바일 고정 height 금지)·`.workflow-grid`(2열→1열). `{{WORKFLOW_VISUALS_CSS}}` 슬롯(shape 뒤), 프로파일 무관·코어 해시 비대상.
- **네임스페이스 `workflow-` 신설**(전문가 지적: `wf-`는 vt-21 `soft_workflow_gate`가 점유 → 금지, `shape-` 재사용은 420px라 도판 뭉갬 → 별도). cross_leak(`vt-[a-z]`/`wg-\d2`) 충돌 0.
- 삽입: `figure.workflow-figure`(visual-figure 아님 → figcaption 권장·강제 아님) + `img.workflow-img`(alt 필수). **경계**: bi-(40×40) < shape-(420px 앵커) < workflow-(720px 대표 도판) < vt-(검색가능 HTML). workflow 도판은 placeholder 노드라 vt- 대체 금지(독자가 본문에서 읽어야 할 절차/비교는 vt-).
- 게이트 `workflow_visual_gate`(opt-in `workflow-figure/img/grid`) — CSS 인라인·빈 alt 금지·네임스페이스 누수·**로컬 SVG 8000×6000 해상도 계약**. 또 QA 지적대로 **`<style>` 제거 후 body만 스캔**해 CSS 주석 속 예시 `<img>` 오발동을 구조적 차단(기존 `shape_visual_gate`도 동일 백포트).
- 검증: 3 프로파일 골든(widget/auto/diagram) `OK` 바이트 불변, workflow 픽스처 4/4 + CSS주석 오발동 회귀 통과, 실제 도판 페이지 렌더 1280/390px overflow 0·무 JS 0. version 4.5.0 유지.

### 본문 구조 패턴 7종 편입 (2026-06-01)
첨부 HTML의 좋은 구조만 추려 기존 13모드 안에서 선택 삽입하는 **작은 본문 구조 패턴 라이브러리**로 편입했고, 이후 `md-excerpt`를 추가해 현재 7종으로 확장했다(새 모드 미추가). 외부/동작 JS 0, 스킬 토큰 + body icon 활용, 프로파일 무관.
- `assets/editorial-patterns.css` — 7 패턴 CSS: `chron-list`(증류 연대기)·`source-preserve`(원문 보존 details)·`core-insight`(핵심 명제 callout)·`conn-grid`(연결 분석 카드)·`ba`(Before/After 윤문)·`impact-grid`(콘텐츠 전환)·`md-excerpt`(마크다운/코드 발췌). 기존 클래스와 충돌 0.
- `assets/editorial-pattern-templates/01..07.html` — 콘텐츠만 교체하는 삽입 골격 7종.
- `references/editorial-pattern-system.md` — 7종 카탈로그·모드별 추천(예: chronology→expert/case_study, source-preserve→reference/article, core-insight는 페이지당 1개, md-excerpt→skill_audit/reference)·과삽입 금지·삽입 규칙.
- `assets/base.html`: `{{EDITORIAL_PATTERNS_CSS}}` 슬롯(body-icons 뒤). `manifest.json`: assets + `editorial_patterns` 메타(count 7).
- `scripts/validate_output.py`: editorial-pattern 게이트(패턴 사용 시 editorial-patterns.css 인라인 강제).

### 비주얼 프로파일 선택 (2026-06-01)
스킬 기동 시 비주얼 스타일을 고를 수 있게 단일 스킬 + 프로파일 파라미터를 도입했다. 코어(13모드 라우터·레이아웃·코어 CSS 5종)는 100% 공유하고, 프로파일이 라이브러리·삽입 단계·CSS 번들·결정표 컬럼만 게이트한다. 무 JS 0·코어 해시 계약 불변. (버전은 4.5.0 유지 — 4.6.0 bump은 frozen auto 골든 v6의 footer/sources를 건드려 회귀-0을 깨므로 골든 보존을 위해 보류; 버전 일관성은 manifest=sources=footer=4.5.0으로 충족.)
- **프로파일 3종**: `widget`(=v5, CSS 뷰 위젯 `wg-`, 코어5+`widgets.css`) / `diagram`(=v6, SVG→HTML `vt-`, 코어5+`visual-html.css`) / `auto`(기본, 둘 다 = 현행 v6 산출).
- **선택 규칙**: 인자 `profile=widget|diagram|auto` 또는 별칭 `style=v5|v6`(`trim→lowercase→정규화`, 둘 다 오면 `profile=` 우선, 무효=`invalid_profile` 실패·조용한 폴백 금지). 미지정 시 비대화형(AGENTS.md 경유 Codex/Gemini)=무조건 `auto`·질문 금지, 대화형(Claude)=1회 질문. 결정론은 인자 명시 경로 한정.
- `manifest.json`: `profiles` 스키마(이름·별칭·css·templates·markup·steps) + `profile_selection` 설명 추가.
- `AGENTS.md`: §4 "0. 프로파일 결정(모드 선행)"·"0.5 profile.json 기록"·§3 프로파일별 컬럼 주석·§4 프로파일별 CSS 번들표·삽입 단계 6/7 게이팅·불변식6 "5종 해시+조건부 인라인".
- `SKILL.md`: §0.5 비주얼 프로파일 선행·§0.6 프로파일 오버레이(단일 출처)·Step 4.6/4.7 프로파일 게이트.
- `scripts/validate_output.py`: `validate(root, skill_dir, profile=None)`·`--profile`·`_resolve_profile`(우선순위 인자>profile.json>폴백, 별칭·invalid)·always-on `cross_leak_gate`(diagram `wg-\d{2}`/widget `vt-[a-z]`, 단·이중따옴표·대소문자, `cross_leak` ISSUE)·`unfilled_placeholder` 게이트. **기존 3인자 호출 회귀 0**(baseline 동일).
- `references/visual-html-system.md`: "코어 6종"→"코어 5종 해시 + 조건부 인라인" 동기화.
- 골든: `auto`=showcase-v6(무변경)·`diagram`=v6 슬림(widgets.css 제거)·`widget`=showcase-v5(정합화). 각 `sources/profile.json` 동봉.
- 분리 계획·검증: 루트 `implement_visual_profile_separation.md`(Phase -1~6, 전문가·QA 리뷰 반영), `dev-plan/golden_prediagnosis.md`.

## v4.4.0 (2026-05-31) — 뷰 위젯 시스템 편입

코드/디자인/리뷰/운영형 정보를 위한 뷰 위젯(view widget) 20종을 스킬 본체에 정식 편입했다. 모든 위젯은 스킬 디자인 토큰을 재사용하고 외부 JS 없이 동작하며, 레이아웃 골격 위에 섹션 목적에 맞게 선택·삽입한다.

### 추가
- `assets/widgets.css` — 위젯 20종 스타일. 모든 선택자는 `wg-<id>-` 네임스페이스(`wg-01`~`wg-20`)로 격리되어 기존 theme/components/layouts와 충돌하지 않는다.
- `assets/widget-templates/*.html` 20종 — 위젯별 삽입 골격. 헤더 주석에 인터랙티브 분류(`css-only`/`css-partial`/`js-needed`)와 무 JS 근사 범위를 명시.
- `references/widget-system.md` — 위젯 선택 기준, 모드별 권장 매핑, 무 JS 인터랙션(`<details>`/`:checked`/`:target`/CSS 애니메이션) 규칙, 접근성(색 외 단서·포커스) 가이드.
- `tests/widget-checklist.md` — 위젯 게이트(외부 JS 0, `wg-<id>-` 네임스페이스 충돌 0, 인터랙션 기법 한정, 색 외 단서·포커스, 18·20 무 JS 근사) grep 명령+기대값.

### 위젯 20종 (인터랙티브 분류)
- CSS-only(완전 무JS) 11종: 02 Visual Design Directions, 06 Component Variants, 07 Animation Sandbox, 08 Clickable Flow, 10 SVG Figure Sheet, 11 Weekly Status, 13 Annotated Flowchart, 14 Feature Explainer, 15 Concept Explainer, 16 Implementation Plan, 17 PR Writeup.
- CSS 부분 7종: 01 Three Code Approaches, 03 Annotated PR, 04 Module Map, 05 Living Design System, 09 Arrow-Key Slide Deck, 12 Incident Timeline, 19 Feature Flag Editor.
- JS 필요 2종: 18 Ticket Triage Board(칸반), 20 Prompt Tuner. 완전 인터랙션(드래그·실시간 토큰)에만 JS가 필요하며, 스킬 기본값은 정적/`:checked` 상태의 **무 JS 근사**로 삽입하고 실시간 동작은 선택적 점진 향상으로만 둔다.

### 변경
- `SKILL.md`: 워크플로우에 Step 4.6 View Widget Selection & Insertion 추가(레이아웃 골격에 적합 위젯을 widgets.css 기반·무 JS로 삽입). §4 Design System 자산 맵과 §8 References에 widgets.css / widget-templates / widget-system.md 등재, 모드별 권장 위젯 한 줄 가이드 추가.
- `assets/base.html`: `{{WIDGETS_CSS}}` 슬롯을 통해 위젯 CSS를 합본하도록 적용(theme → components → visual-components → widgets → layouts → print 순서).
- `manifest.json`: 버전 4.4.0, assets에 `assets/widgets.css` 추가, changes에 위젯 시스템 편입 항목, updated 2026-05-31.

### 검증
- `assets/widgets.css`에서 `wg-01`~`wg-20` 네임스페이스 20종 확인, 네임스페이스 밖으로 새는 `.wg-` 선택자 0건.
- `assets/widget-templates/*.html` 20종 모두 외부/동작 `<script>` 0건. 18·20도 `<script>` 0건(무 JS 근사).
- 인터랙티브 분류 집계 11/7/2 일치(`css-only` 11, `css-partial` 7, `js-needed` 2).
- `manifest.json` `python json.load` 유효성 통과.

### 편입 완성도 마감 (전문가 리뷰 반영, 2026-05-31)
편입 준비도 리뷰(평균 84/100, 최저 항목 "편입 완성도" 72)에서 지적된 P0/P1을 반영해 "강제·메타데이터·문서 정합"의 2차 표면 편입을 마감했다. 무 JS 원칙(외부/동작 JS 0)은 전 항목에서 유지된다.
- `scripts/validate_output.py`: 위젯 정적 게이트 편입 — 출력에 `wg-` 클래스가 있으면 (a) widgets.css 인라인, (b) `wg-<id>-` 밖 `.wg-` 누수 0, (c) 위젯 영역 비-JSON-LD `<script>` 0, (d) `draggable`/`contenteditable` 0을 정적 실패로 검사.
- `manifest.json`: `visual_templates`와 대칭으로 `widget_templates` 배열(01~20) 등록.
- `tests/widget-checklist.md`: 회귀 규칙 2건 추가 — `role="tab"` 사용 시 `aria-selected` 필수/라벨 `tabindex·role` 금지(이중 탭 스톱 금지), `:target-within` 단독 의존 금지(`:target` 폴백 필수).
- `references/widget-system.md`: forward/reverse 매핑 불일치 2건 정합(landing_brief_html↔05, education_html↔10), 배정 원칙("콘텐츠 적합성 우선") 및 적용 갤러리 발견 링크 명시.
- `references/editorial-design-system.md`: 하이라이트 역할-색 1:1 규칙 명문화 — 본문 핵심 강조는 노랑 `.hl` 단일, `.hl.blue`/`.hl.pink`는 별도 의미 한정.
- `assets/widgets.css`: 위젯 08 `:target-within`에 `:has(:target)`/`:target ~` 폴백 추가(Chrome/FF 보강, 실측 동작 확인), `.wg-08-screen{outline:none}` 정리 후 `:focus-visible` 링 복원, wg-03/05/08/17에 `var(--focus)` 3px 포커스 링 일관 적용.
- `assets/widget-templates/14·15`: 커스텀 탭/스텝 라벨의 `role="tab"·tabindex="0"`과 `role="tablist"/tabpanel` 제거 → 네이티브 라디오 시맨틱 위임(이중 탭 스톱·미완성 ARIA 해소). 탭 전환은 `#id:checked`+`for=` 기제로 그대로 동작.
- `recipes/*.md` 5종(comparison·audit·reference·case-study·checklist): 모드 1순위 위젯 삽입 지시 추가.
- `README.md`: v4.4.0 갱신, 위젯 4종 자산 등재, tests "6종" 정정.
- 검증: 무 JS 0(스킬 assets·v5 전 페이지 전수), validate 위젯 게이트 통과, Chromium 실측 — 04 탭·09 스텝·12 플로우 전환 정상, 13 `.hl` 단일색(#ffe9a3), 포커스 링 3px.

## v4.3.3 (2026-05-30) — responsive polish regression gate

13개 모드 전수 캡쳐 감사에서 확인된 dark CTA 링크 대비, platform section/grid 구조, 모바일 표 밀도, case timeline 단일 대형 카드 문제를 스킬 CSS와 정적 게이트에 반영했다.

### 변경
- `assets/theme.css`: `--link-on-dark` 토큰 추가. h2 번호 badge는 숫자와 짧은 라벨 모두 안전하게 보이도록 `min-width + auto width` pill로 조정.
- `assets/components.css`: `.try a`, `.try.soft-cta a`를 밝은 링크 색으로 재정의해 검정 CTA 내부 링크 대비를 4.5:1 이상으로 회복.
- `assets/components.css`: `.mobile-card-table` 패턴 추가. 390px 모바일에서 복잡한 표를 행 카드 형태로 표시할 수 있도록 `data-label` 기반 카드 테이블 스타일 제공.
- `assets/layouts.css`: `.layout-platform .platform-grid:not(section)`로 제한해 semantic section wrapper에 grid가 직접 걸리는 회귀를 방지.
- `assets/layouts.css`: expert executive summary 4카드 orphan 배치를 2×2로 안정화. case-study timeline은 단일 대형 카드 대신 개별 step card로 보이도록 조정.
- `scripts/validate_output.py`: `section.platform-grid`, caption 없는 table, dark CTA link reset 누락, platform-grid direct selector를 정적 실패로 추가.
- `output/adaptive-html-final-showcase/_work/create_v3_from_v2.py`: v3 데모에 platform wrapper 분리, audit roadmap section 분리, landing table caption, mobile card table labels를 자동 적용.

### 검증
- 대상 페이지: 02 executive summary, 05 dark CTA, 07 platform cards, 08 audit roadmap/table, 10 comparison table, 11 case timeline, 12 landing table, 13 checklist table.
- 390px/1440px Playwright 재캡쳐 및 `validate_output.py --skill-dir` 검증 대상으로 지정.

## v4.3.2 (2026-05-30) — blog/SEO polish regression gate

05 블로그 CTA와 06 SEO SERP Preview 캡쳐 검수에서 확인된 dark-section 태그 대비, 블로그 섹션 번호 누락, SERP 제목 스타일 불균형, `h2-sub` 닫는 태그 오류를 스킬 CSS·생성기·정적 게이트에 반영했다.

### 변경
- `assets/components.css`: 검정 `.try`/`.try.soft-cta` 내부 `.tag` pill을 거의 흰 배경 + `var(--ink)` 굵은 텍스트로 재정의해 `로컬LLM`, `Ollama` 같은 태그가 흐려지지 않도록 수정.
- `assets/layouts.css`: `blog_writer` 본문 섹션 h2에 CSS counter 기반 번호 badge를 자동 부여해 다른 모드와 시각적 일관성을 맞춤.
- `assets/layouts.css`: `layout-seo .serp-title`을 Google 원문 모사형 파란색/Arial/20px에서 editorial UI에 맞는 `var(--ink)`, sans, 17~18px, 800 weight로 조정.
- `assets/layouts.css`: `.try.soft-cta .label`이 일반 문단 색을 상속하지 않도록 accent 색상 복구.
- `scripts/validate_output.py`: `.h2-sub`가 `</h2>`로 닫히는 HTML 오류, dark `.try` 태그 대비 reset 누락, blog counter 누락, SEO SERP title의 literal Google style 회귀를 실패 처리.
- `output/adaptive-html-final-showcase/_work/create_v3_from_v2.py`: legacy HTML의 `<p class="h2-sub">...</h2>` 패턴을 재생성 중 자동 교정.

### 검증
- 대상 페이지: 05 블로그 `가볍게 시작해보기`, 05 `왜 지금 로컬 AI인가`, 06 `SERP Preview`.
- 390px/1440px Playwright 재캡쳐 및 `validate_output.py --skill-dir` 검증 대상으로 지정.

## v4.3.1 (2026-05-30) — design polish regression gate

사용자 캡쳐 검수에서 확인된 카드 상단 여백, dark-section 내부 흰 카드 대비, audit 강점/리스크 grid 오배치, case timeline 이중 왼쪽선 문제를 스킬 CSS와 정적 게이트에 반영했다.

### 변경
- `assets/theme.css`: `section > h2:first-child`와 주요 카드 컴포넌트 첫 h2/h3의 top margin을 0으로 리셋해 카드 내부 상단 공백을 제거.
- `assets/theme.css`: muted text token을 더 진하게 조정해 h2-sub/caption/meta가 흐려 보이는 문제를 완화.
- `assets/components.css`: `.try` 안의 `.box/.summary-card/.cta-box/.card-block/.mini-card` 내부 텍스트 색상을 밝은 카드 기준으로 재설정해 흰 카드에서 텍스트가 흐려지는 문제 방지.
- `assets/components.css`: `.try .cta-box`의 accent left rule을 복구해 CTA 카드의 시각적 의도를 유지.
- `assets/components.css`: `.timeline-card` 왼쪽 padding을 보강해 ordered-list marker가 카드 모서리에 붙지 않도록 수정.
- `assets/components.css`: 표 내부 `.status-pill`을 nowrap/center 정렬로 고정해 `Unacceptable`, `GPAI (별도 트랙)`이 좁은 원형 배지처럼 세로로 깨지는 문제 방지.
- `assets/layouts.css`: `.winners:not(section)`, `.tradeoffs:not(section)`의 자동 2컬럼 grid를 제거하고 card block으로 변경. `layout-case .timeline` section left rule 제거.
- `SKILL.md`, `references/quality-gates.md`, `references/layout-system.md`: first-heading margin, dark card contrast, winners/tradeoffs grid, timeline left-rule 중복, CSS asset integrity 방지 규칙 추가.
- `scripts/validate_output.py`: 위 회귀 패턴과 CSS asset hash/snapshot 검사를 정적 게이트에 추가.

### 검증
- 대상 페이지: 04 교육 실습 카드, 06 SEO Final SEO Set, 08 skill audit 강점/리스크, 11 case timeline, 12 landing 다음 행동.
- Playwright 캡쳐 재검증 대상으로 지정.

## v4.3.0 (2026-05-30) — layout-safe v3 및 자동 검증 게이트

`adaptive-html-final-showcase-v2` 전수 캡쳐 감사에서 확인된 섹션 wrapper/grid class 충돌, 모바일 overflow, caption 음수 margin, source sync 불일치, gallery 예외 미정의를 스킬 본체에 반영했다.

### 변경
- `assets/layouts.css`: `section.matrix`, `section.serp-preview`, `section.value-grid`, `section.check-grid`, `section.priority-roadmap`, `section.winners`, `section.tradeoffs` 등 semantic section wrapper에 `display:grid`가 직접 적용되지 않도록 수정. 실제 그리드는 내부 `.card-grid`, `.grid-2`, `.grid-3`, `.matrix:not(section)` 등으로 분리.
- `assets/layouts.css`: `layout-education`의 미정의 `var(--good)`를 `var(--good-bg)`로 교정.
- `assets/components.css`/`assets/theme.css`: 긴 URL·코드·영문 토큰 overflow를 줄이기 위해 `overflow-wrap` 안전 규칙 추가, `.caption` 음수 margin 금지.
- `SKILL.md`, `references/quality-gates.md`, `tests/layout-checklist.md`, `tests/visual-regression-checklist.md`: section wrapper와 inner grid 분리 규칙 및 390px/1280px 검증 기준 추가.
- `scripts/validate_output.py`: 생성된 output 디렉터리를 정적으로 검사하는 게이트 추가(h1, `#main`, 로컬 참조, 외부 JS, caption 음수 margin, semantic grid selector, visual figure, source manifest sync).

### 검증
- `validate_output.py`로 v2의 기존 결함(caption negative margin, semantic section grid selector, source version mismatch)을 재현.
- v3 쇼케이스는 공통 CSS를 재주입하고 source를 v4.3.0과 동기화하도록 생성.
- Playwright 390px/1440px 렌더 검증 대상으로 지정.

## v4.2.1 (2026-05-30) — quality-gate SVG 레이아웃 보정

사용자 검수에서 `품질 게이트` 인포그래픽의 하단 “삽입 전 필수 검수” 카드가 납작한 배너처럼 보이고 footer와 시각적으로 붙는 문제가 확인되어 수정했다.

### 변경
- `scripts/render_visual_svg.py`의 `quality-gate` 렌더링을 세로 6행 구조에서 2×3 카드 그리드 + 충분한 높이의 노란 `PRE-FLIGHT` 패널로 변경.
- `references/visual-template-system.md`, `references/quality-gates.md`, `tests/visual-regression-checklist.md`에 하단 강조 패널 안전 규칙 추가.
- 강조 노란색(`#FFD400`)은 최종 검수/핵심 CTA 등 한 지점에만 쓰도록 정리.

### 검증
- quality-gate 샘플 SVG 렌더링 성공, 원본 8000×6000 유지.
- 주요 카드 max bottom 5060px로 footer(5600px)와 충분한 여백 확보.
- 로컬 데모 페이지 390px/1280px Playwright 스크린샷 재검증.

## v4.2.0 (2026-05-30) — Visual Template System 도입

14-image-strategy-demo.html에서 검증한 8000×6000 SVG 인포그래픽 전략을 스킬 본체에 반영했다. 이제 스킬은 모드/섹션 목적에 따라 사진 검색, SVG 인포그래픽 생성, AI 컨셉 이미지 사용을 구분하고, 기본값으로 목적형 SVG 인포그래픽을 우선한다.

### 추가
- `assets/visual-components.css` — `figure.visual-figure`, `.figure-wide`, figcaption, visual rule grid, visual pipeline 반응형 스타일.
- `visual-templates/*.svg.tpl` 7종 — hero-map, card-grid, decision-tree, quality-gate, timeline, matrix, checklist-flow.
- `scripts/render_visual_svg.py` — visual brief JSON을 8000×6000 SVG로 렌더링하는 stdlib-only 스크립트.
- `schemas/visual-brief.schema.json` — 시각 템플릿 입력 스키마.
- `references/visual-template-system.md` — 모드별 기본 템플릿, 이미지 선택 원칙, HTML 삽입 패턴, 품질 게이트.

### 변경
- `SKILL.md` 워크플로우에 Step 4.5 Visual Brief Planning 추가.
- `base.html`에 선택적 `{{VISUAL_COMPONENTS_CSS}}` 슬롯 추가.
- `manifest.json` 버전 4.2.0, assets/templates/scripts/schemas 메타데이터 갱신.
- quality/layout/visual/accessibility 체크리스트에 8000×6000 SVG, alt, figcaption, 캔버스 잘림 방지 게이트 추가.

### 검증
- visual brief 샘플 7종 렌더링 성공.
- 생성 SVG 7개 모두 XML 파싱 성공, width/height 8000×6000 확인.
- Python 스크립트 py_compile 통과.

## v4.1.0 (2026-05-30) — 정밀 분석 보고서 P0~P2 자동 패치

ANALYSIS_adaptive-html-final.md(7-전문가 분석 + 적대적 검증)에서 확정된 이슈 19건(medium 8 · low 11)을 8개 파일-분리 클러스터로 자동 패치 → 검증 → 재검증했다. 동작 결함은 원래 0건이었고, 본 패치는 메타데이터 정합성·테스트 커버리지·디자인 토큰 완성도를 끌어올렸다.

검증: 독립 스크립트 검증 15개 그룹 전부 통과 (id=main 13/13, 단일 h1 13/13, 외부 JS 0, 미정의 CSS 클래스 0, manifest 13모드 매핑 일치, recipes 13/13, schema 유효, 폭 토큰 780/1020 통일, .skill 라운드트립 완전 일치).

### P0 — 출시 신뢰성
- **M1** 접근성 회귀 가드 신설 — `tests/accessibility-checklist.md`: skip link, `<main id="main">` 13/13, 단일 h1, 외부 JS 0, `:focus-visible`를 grep 명령+기대값으로 자동검증.
- **M3** 모드 ID 규약 단일화 — `manifest.modes`를 라우터 표준 13개 ID의 `{id, layout}` 객체 배열로 교체. `references/layout-system.md`의 단축 명칭도 표준 ID로 교정(mode-selection.md는 이미 일치).
- **M5** `tests/quality-checklist.md` 재작성 — SKILL.md §7 게이트 1:1 매핑 + 모드별 조건부 게이트(교육→퀴즈/정답, 전문가→리스크/검증, 블로그·SEO→제목/메타/태그, 감사→개선본). 누락 게이트 9건 보강.

### P1 — 정합성·커버리지
- **M2** 레이아웃이 쓰던 미정의 CSS 클래스 39개를 `layouts.css`에 전부 정의(헤더 공통 11 + 그리드성 7은 모바일 1컬럼 + 섹션 래퍼 20+). 차집합 0.
- **M4** 누락 7개 모드 recipe 신규 생성 → `recipes/` 총 13/13 (article, education, reference, comparison, case-study, landing-brief, checklist).
- **M6** `tests/layout-checklist.md`를 13레이아웃 표(파일|mode|필수블록|폭클래스)로 재작성. 폭 토큰 780/1020 통일.
- **M7/M8** `theme.css`에 `:focus-visible` 추가, `tests/visual-regression-checklist.md` 폭 임계치 780/1020 교정 + 주관 항목 정량화.
- **golden-prompts** P9~P13(reference/comparison/case_study/landing/checklist) 추가 + 전 항목 `expected_mode`/`expected_layout` 명시 → 13모드 대표.

### P2 — 문서·디자인 완성도
- **L1** `editorial-design-system.md` 구버전 명칭(v2/7모드) → final/13모드.
- **L2** `examples/index.html` v2 브랜딩 → v4.1.0 / 13-mode.
- **L3** `design-dna.md`를 디자인 토큰 SoT로 명시 + SKILL.md §8 References 등재.
- **L4** SKILL.md §5 Required Components에 `.faq/.cta-box/.box` + 골격 컴포넌트 추가, `components.css`에 해당 클래스 정의.
- **L5** `base.html`에 선택적 `{{FOOTER}}` 슬롯 추가(footer CSS 고아 해소).
- **L6** 출처 허브 경로를 일반화 표기로(비존재 절대경로 강제 제거).
- **L7** `blog-meta.schema.json`을 예시 11필드와 1:1 정합(title_variants 4키, search_intent enum, slug/target_reader/estimated_reading_time/platform_notes) + `$schema`/`$id`/`title`.
- **L8** `quality-report.schema.json`을 루브릭 구조(0~5 점수 + total + verdict + gates)로 확장 + 메타 식별자. eval-rubric/quality-gates/Blog Score 적용범위 명시.
- **L9** 콜아웃 raw hex → `:root` 토큰 12종, AA 미달 색(.term/.danger/.good 라벨, .meta, .tag) 4.5:1 이상으로 상향, `prefers-reduced-motion` scroll 해제, print.css `print-color-adjust`/`break-inside`/`.skip{display:none}`.
- **L10** h2-sub 강도를 '모드 한정 권장'으로 SKILL/quality-gates/editorial-design-system 통일, 트리거 tie-breaker 한 줄 추가.
- **L11** 공개/SEO 예시 03/05/06에 폰트 링크(Pretendard + Noto Serif KR) 추가.

### 메타
- version 4.0.0 → 4.1.0. 파일 수 51 → 59 (+accessibility-checklist, +recipe 7).
- 패치 전 백업: `/tmp/adaptive-html-final.pre-patch`, `/tmp/adaptive-html-final.skill.bak`.

## v4.0.0 (2026-05-30) — 통합 최초본
- `adaptive-html-learning-ultimate`(13모드 라우터·레이아웃·평가체계) + `adaptive-html-blog-writer`(블로그/SEO/플랫폼/박스 상세 규칙) 병합.
- skip link 접근성 버그 수정: 13개 레이아웃 `<main id="main">` 통일.
- 이름·메타데이터 일원화(aliases/merged_from).
