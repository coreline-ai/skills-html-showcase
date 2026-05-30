# Changelog — adaptive-html-final

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
