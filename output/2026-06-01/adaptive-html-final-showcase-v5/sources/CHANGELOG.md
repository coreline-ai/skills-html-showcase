# Changelog — adaptive-html-final

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
