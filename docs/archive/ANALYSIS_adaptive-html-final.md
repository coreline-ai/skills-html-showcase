> ⚠️ **ARCHIVED — SUPERSEDED by v5.2.0.** 이 문서는 작성 당시 버전의 시점 고정(point-in-time) 리뷰/분석/계획 기록입니다. 현재 스킬은 **v5.2.0**이며, 여기서 지적된 항목 다수는 이미 해소·초과 달성되었습니다. 최신 사실 기준선은 게이트를 완전 통과한 `output/2026-06-05/adaptive-html-final-13-topics-20260605_083433/`이고, 현행 문서는 루트 `README.md`·`AGENTS.md`·`Guide.md`입니다. 아카이브 색인: [`docs/archive/README.md`](README.md).

---

# adaptive-html-final 정밀 분석 보고서 (v4.5.0)

> 분석 방식: 7개 영역 병렬 분해(오케스트레이션·레이아웃/CSS/접근성·위젯·vt 템플릿·시각 에셋팩·검증/게이트·메타데이터 정합성) → 핵심 쟁점 적대적 검증(실파일·스크립트 실행으로 재확인) → 교차 통합 감사 → 종합 정리
> 분석 대상: `skills/adaptive-html-final` (v4.5.0, 180개 파일)
> 작성일: 2026-06-05 · 직전 보고서: v4.0.0(2026-05-30, 51개 파일)을 본 문서가 대체

## 1. 총평 (Executive Summary)

adaptive-html-final v4.5.0는 13모드 라우터를 뼈대로 **CSS 뷰 위젯 20종(wg-), SVG→HTML 인플로우 다이어그램 21종(vt-), 본문 아이콘 32종(bi-), 본문 구조 패턴 7종, soft-shape SVG 36종, 워크플로우 도판 10종**을 흡수한 대형 통합 스킬이다. v4.0.0 정밀 분석에서 지적했던 4대 약점 — (1) 모드 ID 11/13 불일치, (2) 레이아웃 참조 CSS 39개 미정의, (3) recipes 6/13 커버리지, (4) skip link 회귀 무방비 — 은 **이번 버전에서 모두 해소되었다**(13/13 일치, 미정의 0, 13/13 recipes, `<main id="main">` 정적 게이트화). 가장 중요한 무 JS 불변식은 신규로 추가된 거대 표면(위젯 20 + vt 21 + SVG 46개) 전체에서 **위반 0건**으로 적대적 검증을 통과했고, 네임스페이스 격리(wg-/vt-/wf-/workflow-/shape-/bi-), 8000×6000 viewBox 계약(46/46), 카탈로그↔파일↔클래스 1:1 정합성도 모두 수치로 확인되었다.

실질적 결함은 **동작 생성 경로가 아니라 배포·QA 자기정합성에 집중**되어 있다. 가장 무거운 두 건은 (H1) **패키지 `.skill`이 v4.3.3에 멈춰 있어 v4.4/v4.5 자산 전체가 빠진 상태로 배포된다는 점**, (H2) **`validate_output.py`가 자기 자신의 8개 예제를 8/8 모두 FAILED 처리한다는 점**(무조건 발화 게이트가 단일 파일 데모와 충돌)이다. 둘 다 직접 실행으로 입증했다. 그 밖은 문서-산출물 드리프트(vt "20종" 잔재, table 권고 vs div 구현), 색 외 단서 누락 2건(vt-19/vt-03), 메타데이터 라벨 오류(shape/workflow `decorative:true`) 등 정합성·완성도 과제다.

**전체 성숙도 점수: 86/100 — 생성 경로는 무 JS·접근성·네임스페이스·정합성 모두 견고하며 v4.0 약점이 전부 정리된 상태다. 감점은 (a) 배포 패키지 동기화 실패, (b) 검증 게이트가 자기 예제를 통과 못하는 자기모순, (c) 자동 테스트 러너 부재, (d) 일부 문서 드리프트·색 단서 누락에서 발생한다.**

## 2. 패키지 개요

| 항목 | 수치/구성 | 검증 상태 |
|---|---|---|
| 스킬명 / 버전 | adaptive-html-final / 4.5.0 | manifest·SKILL·CHANGELOG·README 4.5.0 일치 (OK) |
| 디스크 파일 | 180개 (html 70 · svg 46 · md 37 · css 11 · tpl 7 · json 7 · py 2) | — |
| 모드 라우터 | 13개 | manifest.modes ↔ §3 라우터 ↔ disk **13/13 일치** (v4.0 11/13 → 해소) |
| 레이아웃 | 13개 | manifest ↔ disk 차집합 **0** |
| 코어 CSS | theme/components/visual-components/layouts/print | 미정의 클래스 **0** (v4.0 39 → 해소), `!important` **0** |
| 위젯 (wg-) | 20종 + widgets.css | 외부/동작 JS **0**, 네임스페이스 누수 **0** |
| vt 템플릿 | 21종 + visual-html.css | JS **0**, 미정의 클래스 **0**, 전부 in-flow 네이티브 HTML |
| body-icons (bi-) | 32종 | json 32 ↔ css 클래스 1:1, 전부 aria-hidden 장식 |
| editorial patterns | 7종(`md-excerpt` 포함) | 템플릿 7개 disk 확인 |
| shape SVG | 36종 | viewBox 8000×6000 36/36, catalog 36↔파일 36 |
| workflow SVG | 10종 | viewBox 8000×6000 10/10, catalog 10↔파일 10 |
| recipes | 13개 | **13/13 모드 커버** (v4.0 6/13 → 해소) |
| schemas | 3개 (blog-meta/quality-report/visual-brief) | Draft 2020-12, `$schema/$id/title` 보유, visual-brief↔렌더러 7 enum 일치 |
| skip link | base.html `href="#main"` ↔ 13개 `<main id="main">` | **13/13** + main-id 정적 게이트화 |
| 확정 이슈 | critical 0 · high 2 · medium 8 · low 11 | 직접 검증 후 산정 |

## 3. 영역별 정밀 분석

### 3.1 SKILL.md 오케스트레이션 + 결정론 운영 사양(§0.5/§0.6)

**강점**
- §0.6 캐노니컬 결정표가 **13모드 전부**를 커버하고, §3 라우터·`mode-selection.md`·`manifest.modes`와 모드 집합이 동일. 모드별 vt·wg 열이 모두 채워짐.
- §0.6의 vt 슬러그 21개가 `visual-html-templates/NN-*.html`에 1:1 해소, wg-01~20도 전부 실파일. 댕글링 참조 0.
- 프로파일 라우터가 SKILL §0.5(L51)·manifest `profiles`(L254-298)·AGENTS §4에서 동일: `profile=` 우선, `v5→widget`/`v6→diagram`, `trim→lowercase→정규화`, 무효 토큰 → `invalid_profile` 하드 실패(무음 폴백 없음), 비대화형 → 강제 `auto`. 열 게이트(widget=wg열/diagram=vt열/auto=둘다)도 §0.6 오버레이·Step 4.6/4.7과 일치.
- 무 JS 불변식(JSON-LD만 허용)이 L47/355/371/394/460에서 일관. Article/Blog/SEO의 JSON-LD 허용(L374)은 부분집합 허가로 모순 아님.
- base.html 슬롯 순서가 Step 5 합본 순서(THEME→COMPONENTS→VISUAL_COMPONENTS→WIDGETS→VISUAL_HTML→…→LAYOUTS→PRINT)와 일치.

**문제점**
| severity | 문제 | file:line | 수정안 |
|---|---|---|---|
| medium | SKILL.md가 `AGENTS.md §3/§4`를 게이트 근거로 4회 인용하나 `AGENTS.md`는 스킬 패키지 밖(레포 루트)에 있음 — 스킬 디렉터리만 로드하는 에이전트는 해소 불가 | `SKILL.md:82,312,346` (+레포 루트) | AGENTS.md를 스킬에 동봉하거나, 결정론 진입점 규칙을 SKILL.md 내부에 자기완결로 재서술 |
| low | vt 라이브러리를 "20종"으로 표기(다른 모든 곳·manifest는 21) | `SKILL.md:446`, `manifest.json:192`(changelog) | "21종"·`01..21.html`로 수정 |
| low | §4.7 prefix 예시(`hm-/dt-/rm-` 등)에 vt-21의 합법 prefix `wf-`가 빠짐 | `SKILL.md:353` | `wf-`(soft-workflow-map) 예시 추가 |
| low | Step 5 합본 순서 서술이 base.html이 실제 방출하는 BODY_ICONS/EDITORIAL_PATTERNS/SHAPE/WORKFLOW 4개 슬롯을 누락(프로파일 무관 add-on) | `SKILL.md:364` vs `base.html:20-23` | layouts.css 앞에 들어가는 4개 슬롯 명시 |

### 3.2 레이아웃 13종 + 코어 CSS + 접근성

**강점**
- **skip link 13/13**: `base.html:30 href="#main"` ↔ 13개 레이아웃 전부 `<main id="main">`(각 1개). 단일 `<h1>`도 13/13.
- **코어 CSS 클래스 미정의 0**: base+13레이아웃에서 사용된 94개 클래스가 5개 코어 CSS에 전부 정의됨(파이썬 차집합 0). v4.0의 "39개 미정의"는 해소 확인.
- `!important` **0건**(5개 코어 CSS 전체).
- 접근성 프리미티브: `focus-visible` 전역 링(`theme.css:57`, 비브랜드 블루 `--focus:#1a56db`), `prefers-reduced-motion` 3곳(`theme.css:56,61`, `components.css:74`), skip link 포커스 노출(`theme.css:75-76`), `.reading-progress` `aria-hidden`.
- AA 대비 실측: `--ink-mute:#666`(5.25:1), `--chip-ink:#6a6a6a`(5.18:1), `--ink-soft:#4a4a4a`(8.1+) 모두 4.5 초과. `--accent:#e63946`(4.17)은 본문 텍스트 color로 미사용(배경/보더/진행바 한정)이라 위반 아님.
- 반응형 안전장치: long-token 래핑(`theme.css:68-69`, `components.css:20`), pre/table 가로 스크롤(`components.css:77,80`), grid `min-width:0`, `mobile-card-table` 카드 스택 구현(`components.css:195-204`).

**문제점**
| severity | 문제 | file:line | 수정안 |
|---|---|---|---|
| low | 죽은 셀렉터 `.layout-skill-audit`(HTML은 `layout-audit` 사용) — 무해한 고아 한정자 | `theme.css:81` | 제거 또는 의도된 변형이면 HTML 클래스 정합 |
| low | `mobile-card-table`는 `<td data-label>` 주입이 전제인데 13레이아웃은 콘텐츠 슬롯이라 미주입 — 기전은 정상이나 활성화가 생성 콘텐츠 의존 | `components.css:202` | `layout-system.md`에 td `data-label`+`.mobile-card-table` 래핑 요건 문서화 |

### 3.3 CSS 뷰 위젯 시스템(wg-01~20, v4.4.0)

**강점**
- **무 JS 불변식 완전 충족**: 20개 템플릿 + widgets.css에서 `<script>`(JSON-LD조차) 0, `on*` 핸들러 0, `addEventListener`/`javascript:`/`draggable`/`contenteditable`/`<dialog>` 0. widget-checklist §1/§3/§5 전부 통과.
- 18(triage-board)·20(prompt-tuner) 무 JS 근사 실증: 18은 입력 없는 정적 보드, 20은 `radio:checked` CSS 탭. 둘 다 "실시간 편집은 JS 필요" 캡션 명시.
- 네임스페이스 누수 0: `.wg-NN-` 외 일반 클래스 사용 0, 충돌 0. 정의된 541개 `.wg-*` 중 미정의는 구조 래퍼 2개(`wg-04-edges`, `wg-12-ck`)뿐이며 자식이 전부 스타일됨(설계상 정상).
- 인터랙션 분류(CSS-only 11 / partial 7 / JS-needed 2)가 파일 헤더 주석·`widget-system.md:51-53`·SKILL.md:324와 일치. `role="tab"` 미사용(라디오로 ARIA 함정 회피).

**문제점**
| severity | 문제 | file:line | 수정안 |
|---|---|---|---|
| low(doc) | "JS-needed = 18·20" 외부 서술과 실제 분류(JS-needed=09·18, 20은 partial)가 축이 다름 — `widget-system.md:55`가 이미 명시 화해 | `widget-system.md:53,55` | 외부 설명 시 "18/20=편집본질 묶음, 분류는 09·18" 구분 표기 |

### 3.4 SVG→HTML 인플로우 다이어그램(vt-01~21, v4.5.0)

**강점**
- **무 JS 0**: 21개 템플릿에서 `<script>`/`on*`/`addEventListener`/`draggable`/`contenteditable`/CSS `expression()` 0.
- **진짜 in-flow 네이티브 HTML**: `<img>`/`<svg>`/`<canvas>`/`background-image` 0. div/span + 시맨틱(`section`×21, `article`×32, `h3`×13)으로 CSS 드로잉. "이미지도 인라인 SVG도 아님" 주장 입증.
- 미정의 클래스 0(사용 115 ⊆ 정의 143). 네임스페이스: `wf-`는 vt-21에서만 등장(SKILL.md:277 예약과 일치), `workflow-` 오용 0.
- vt-21 접근성: `role="img"` 0, `aria-hidden`은 장식 요소에만, 카드 텍스트/지표값은 DOM 유지(프루닝 방지) — CHANGELOG 주장과 정확히 일치.
- §0.6 모드→vt 매핑이 `visual-html-system.md` §3과 바이트 단위 일치. manifest 21↔disk 21.

**문제점**
| severity | 문제 | file:line | 수정안 |
|---|---|---|---|
| medium | 문서는 raci/risk-matrix에 `<table>`/`<caption>` 권고하나 두 템플릿 모두 `<div>` 그리드(행/열 헤더 연결·`scope` 없음) — 가이드 vs 산출물 자기모순 | `visual-html-system.md:113` vs `08-raci.html:3`, `03-risk-matrix.html:3` | 실제 `<table>`+`<th scope>`로 전환하거나 doc 규칙을 div-grid 현실에 맞게 완화 |
| medium | vt-19 feature-flag 토글이 on/off를 **색만으로** 전달(`<span class="switch off">` 빈 요소, 텍스트·aria 없음) — 문서의 "색 외 단서 의무" 위반 | `19-feature-flag.html:3`; 규칙 `visual-html-system.md:112` | ON/OFF 텍스트 토큰 또는 `aria-label`/visually-hidden 라벨 추가 |
| low | vt-03 risk severity(high/med/low)가 보더 색만으로 표현(셀 텍스트는 위험명) | `03-risk-matrix.html:3` | "높음/중간/낮음" 토큰/필 추가 |
| low | `08-raci.html`의 빈 `class=""` 7개 — 무해하나 노이즈 | `08-raci.html:3` | 빈 속성 제거 또는 `.c/.i` 부여 |

### 3.5 시각 에셋팩(body-icons·editorial-patterns·shape·workflow, v4.5.0)

**강점**
- 4대 카운트 디스크 일치: body-icons.json **32**, editorial-pattern-templates **7**(`07-md-excerpt.html` 존재), shape-svgs **36**·shape-catalog **36**, workflow-svgs **10**·workflow-catalog **10**.
- viewBox 계약 100%: shape 36 + workflow 10 = 46/46 모두 `0 0 8000 6000`. body-icons는 compact `0 0 40 40`(스펙 일치).
- 무 JS 0: 46개 SVG에서 `<script>`/`onload`/SMIL `<animate>` 0.
- 네임스페이스: `workflow-visuals.css`는 `wf-` 미사용(vt-21 예약 준수), shape-/bi- 격리.
- 카탈로그↔파일↔클래스 1:1(드리프트 0). 46 SVG 전부 `<title>`+`<desc>`+`role="img"`+`aria-labelledby`, body-icons 32 전부 `aria-hidden`.

**문제점**
| severity | 문제 | file:line | 수정안 |
|---|---|---|---|
| medium | manifest가 shape_visuals·workflow_visuals를 `"decorative": true`로 태깅하나, 같은 항목 `render`/`visual-template-system.md:112,196`은 **비공백 alt 필수**(게이트 강제)이고 SVG에 `role="img"`+title/desc 내장 — 즉 정보성 명명 이미지이지 장식 아님. 진짜 장식은 body-icons뿐 | `manifest.json` shape_visuals/workflow_visuals | shape/workflow는 `decorative:false`(또는 제거), `true`는 body_icons만 유지 |
| info | workflow SVG 내부 노드 라벨은 설계상 placeholder(`visual-template-system.md:197`) — 의미는 인접 HTML/figcaption에. `role="img"`+title로 "명명 이미지" 안내되므로 작성자가 내부 라벨 의존 금지 가이드 준수 필요 | `workflow-svgs/*.svg` | 코드 변경 불필요, 가이드 준수 확인 |

### 3.6 검증/품질 게이트(scripts·tests·schemas·recipes)

**강점**
- §0.5 불변식 대부분 자동화: 무 JS(`external_script`/`widget_behavioral_script`/`visual_html_behavioral_script`), 코어 CSS 인라인 해시 마커, 단일 h1, `<main id="main">`, local-ref 존재, table caption, 8000×6000 SVG figure 구조, source-version sync, CSS-integrity 매니페스트.
- **v4 셀링포인트(skip link main-id)가 이제 정적 게이트화** — v4.0 "회귀 무방비" 대비 개선(`validate_output.py:279-280`).
- v4.3.x 회귀 검사 9종+ 전부 존재(caption 음수 margin, 시맨틱 섹션 grid, try-card/tag/link 대비, blog counter, SERP literal-Google, platform-grid 오용 등).
- 신규 v4.5 자산도 조건부 게이트 보유(widget/vt/body-icon/shape/`wf-board`/`workflow-figure` SVG + R1-R5 + 프로파일 keyed cross_leak). 위젯 게이트 합성 페이지 발화 확인.
- 스키마 3종 모두 Draft 2020-12 `$schema/$id/title` 보유, 파싱 OK. **visual-brief의 7 enum이 render_visual_svg.py RENDERERS 7키와 정확히 일치**.
- **recipes 13/13** 모드 1:1 매핑(v4.0 6/13 → 해소).

**문제점**
| severity | 문제 | file:line | 수정안 |
|---|---|---|---|
| **high** | `validate_output.py`가 **자기 예제 8/8을 FAILED 처리**. 무조건 발화 게이트(`missing_inline_css_hash_marker`, `missing_section_first_heading_margin_reset`, `missing_try_*_contrast_reset`, `missing_blog_section_counter`, `seo_serp_title_literal_google_style`, `platform_grid_selector_allows_section_grid`)가 해당 컴포넌트 미사용·최소 인라인 데모에서도 무조건 요구됨. `python3 scripts/validate_output.py examples/ --skill-dir .` → 8개 전부 FAILED(직접 실행 확인) | `validate_output.py:296-318` | (a) 코어 CSS 해시 마커/관련 클래스 탐지 시에만 게이트하도록 조건화, 또는 (b) 예제를 full-bundle 인라인 폴더로 재배포. 현 상태로는 스킬이 자기 예제를 통과 못함 |
| medium | skip link **앵커**(`<a href="#main">`) 미게이트 — 타깃 `<main id="main">`만 검사. 링크 자체가 사라져도 통과 가능 | `validate_output.py:279-280` | `main_id` 참일 때 `<a href="#main">` 존재 검사 추가로 셀링포인트 완전 방어 |
| medium | `quality-checklist.md`가 v4.5 게이트 미반영 — 스크립트가 "자동 강제"한다 주장(L3)하나 widget/vt/body-icon/shape/`wf-board`/profile/R1-R5 행이 전무 | `tests/quality-checklist.md:1-51` | 신규 자산 조건부 게이트 행을 v4.3.x처럼 1:1 추가 |
| medium | 자동 테스트 러너/CI 부재 — `tests/*.md` 6종 전부 수동 체크리스트, `*.py`/`pytest`/`.github` 없음. 게이트 로직 자체가 회귀 무방비 | `tests/`, `validate_output.py`(자가 테스트 없음) | good/bad 픽스처에 대해 게이트를 실행·단언하는 최소 pytest/`run-tests.sh` 추가 |
| low | widget/visual 체크리스트는 **에셋 라이브러리**를 grep, validate_output은 **생성 산출물**을 검사 — 책임 분담이 어디에도 미문서화 | `tests/widget-checklist.md:3-10` | 분담 1줄 명시 |
| low | visual-brief.schema.json `$id` 호스트만 상이(`adaptive-html-final.local` vs 타 2종 `meewang.kr`) | `schemas/visual-brief.schema.json:3` | 호스트 정합 |
| low | `cross_leak_gate`는 프로파일 미선언 시 무음 skip — 기본 호출은 교차 누수 보호 미적용 | `validate_output.py:234-235` | 의도된 동작이나 quality-gates.md에 명시 |

### 3.7 메타데이터 정합성(manifest↔disk↔SKILL↔examples↔.skill)

**강점**
- 모드 라우터 13/13(id·layout 차집합 0, v4.0 "11/13" 해소), 레이아웃 13/13, 자산 15/15, widget_templates 20/20, visual_html_templates 21/21, visual_templates(.tpl) 7/7 — **전부 드리프트 0**.
- `.tpl` 7개는 `render_visual_svg.py`가 실사용(고아 아님). design-dna.md 이제 인용(`SKILL.md:435`, v4.0 해소).
- 예제 7종: 단일 h1, 인라인 `<style>`만, **외부/동작 JS 0**, 외부 자산 CSS 링크 0(03/05/06의 link는 Google Fonts).
- 버전 4.5.0이 manifest/SKILL/CHANGELOG/README 전부 일치.

**문제점**
| severity | 문제 | file:line | 수정안 |
|---|---|---|---|
| **high** | **패키지 `.skill`이 v4.3.3에 정지** — 현 디렉터리 4.5.0보다 두 마이너 뒤. zip 내부 manifest `version:4.3.3`, references 11개(disk 15), `widgets.css`/`visual-html.css`/`body-icons.*`/`editorial-patterns.*`/`shape-svgs/`/`workflow-svgs/`/`widget-templates/`/`visual-html-templates/` **전부 부재**. 설치자는 v4.4/v4.5 기능을 받지 못함 | `skills/adaptive-html-final.skill` (직접 unzip 확인) | 현 v4.5.0 디렉터리로 `.skill` 재패키징 |
| medium | §8 References 목록이 `body-icon-system.md`·`editorial-pattern-system.md` 누락(본문·manifest는 인용, disk 존재, 15중 13만 등재) | `SKILL.md:421-434` | §8에 두 reference 추가 |
| low | `editorial_patterns` 서술 카운트 불일치 — 구조 `count:7`(md-excerpt 포함)은 정확하나 v4.5 changelog 텍스트는 6개만 나열 | `manifest.json:194` | changelog 텍스트 "7종"·md-excerpt 포함으로 수정 |

## 4. v4.0.0 → v4.5.0 변화 요약(회귀/해소 추적)

| v4.0.0 지적(검증 후) | v4.5.0 상태 |
|---|---|
| 모드 ID 11/13 불일치 (medium) | **해소** — 13/13 일치 |
| 레이아웃 참조 CSS 39개 미정의 (medium) | **해소** — 미정의 0 |
| quality-checklist가 SKILL 게이트 9개+ 미반영 (medium) | **부분 회귀** — v4.3.x는 반영, 신규 v4.5 게이트(widget/vt/body-icon/shape/wf) 또 누락(§3.6 medium) |
| design-dna.md §8 미인용 (low) | **해소** — 인용됨 |
| recipes 6/13 | **해소** — 13/13 |
| skip link 회귀 무방비 | **개선** — main-id 정적 게이트화(단 앵커 자체는 여전히 미게이트, §3.6 medium) |
| schemas $schema/$id/title 0/2 | **해소** — 3/3 보유 |
| (신규 표면) | 위젯 20·vt 21·SVG 46 전부 무 JS·네임스페이스·viewBox·정합성 통과 |
| (신규 결함) | `.skill` 패키지 v4.3.3 정지(H1), 검증기가 자기 예제 8/8 실패(H2) |

## 5. 우선순위 처방(권장 순서)

1. **[H1] `.skill` 재패키징** — 현 v4.5.0 디렉터리로 zip 재생성. 배포본이 두 메이저 기능 세트(위젯·vt·아이콘·shape·workflow)를 통째로 누락 중인 가장 시급한 건.
2. **[H2] 검증기 자기모순 해소** — 무조건 발화 7개 게이트를 "코어 CSS 해시 마커/관련 컴포넌트 탐지 시"로 조건화하거나 예제를 full-bundle로 재배포. 스킬이 자기 예제를 통과해야 게이트 신뢰 가능.
3. **[M] skip link 앵커 게이트 추가** + **quality-checklist에 v4.5 게이트 행 동기화** + **최소 pytest 픽스처 러너** — 셀링포인트와 신규 표면을 회귀 방어.
4. **[M] vt-19 토글·vt-03 severity 색 외 단서 추가**, **raci/risk-matrix table 전환 또는 doc 완화**, **shape/workflow `decorative:false` 정정**, **§8에 2개 reference 등재**.
5. **[L] 문서 드리프트 정리** — vt "20종"→21, editorial 6→7, §4.7에 wf- 예시, Step 5 슬롯 4종, `.layout-skill-audit` 죽은 셀렉터, visual-brief `$id` 호스트.

## 6. 검증 메모

- H1(.skill v4.3.3)·H2(예제 8/8 FAILED)·vt-19 색 단서·raci div-grid는 본 분석에서 **직접 unzip / 스크립트 실행 / grep**으로 재확인했다.
- 무 JS 0, 네임스페이스 누수 0, viewBox 46/46, 미정의 클래스 0(코어·vt), 카운트 정합(32/7/36/10/20/21)은 각 영역 에이전트가 파이썬 차집합·grep으로 수치 산출했고 오탐 기각 없음.
- editorial-patterns "6 vs 7"은 **구조 `count:7`이 정답**(disk에 `07-md-excerpt.html` 존재)이며 changelog 텍스트만 6으로 뒤처짐 — false alarm을 정정함.
- critical(출력 파손) 결함은 발견되지 않았다. 두 high는 모두 배포·QA 자기정합성 영역으로, 생성 경로 자체의 런타임 결함이 아니다.
