# Visual HTML System

`adaptive-html-final`의 두 번째 위젯 라이브러리다. 첫 번째인 **CSS 뷰 위젯**(`wg-01`~`20`, `assets/widgets.css`, `references/widget-system.md`)이 인터랙션 중심의 보조 뷰라면, 이 **SVG→HTML 템플릿**(`vt-` 21종)은 종래 대형 SVG 인포그래픽을 대체하는 **본문 삽입형 다이어그램**이다. 두 라이브러리는 역할이 다르며 어느 쪽도 다른 쪽을 대체하지 않는다.

핵심 철학은 스킬 전체와 동일하게 **외부/동작 JS 0**이다. 본문 삽입형 다이어그램에는 `<script>`가 한 줄도 들어가지 않는다. 검색·복사·번역·스크린리더가 그대로 통하고, 모바일에서 자연스럽게 줄바꿈되며, 문서의 한 부분으로 읽힌다(허용되는 유일한 스크립트는 Article/Blog/SEO 모드의 `application/ld+json` JSON-LD 메타데이터뿐이며, 이는 동작 코드가 아니다).

> 도입 이력: 이 라이브러리는 v4.5.0에서 본문 삽입형 HTML 다이어그램으로 편입되었고, 현행 v5.10.3 기준은 `vt-` 21종 + 17모드 §0.6 매핑이다.

## 1. 목적 — 왜 대형 SVG 대신 본문형 HTML인가

`8000×6000` SVG 인포그래픽(`references/visual-template-system.md`)은 hero·다운로드·인쇄/발표 별첨에는 여전히 유효하다. 그러나 본문 한가운데에 끼우면 다음 문제가 생긴다.

- **레이아웃 언어가 다르다.** 대형 래스터/벡터 캔버스는 본문 카드·표·문단과 다른 리듬으로 움직여, 독자가 "이미지를 확대"해야 이해된다.
- **텍스트가 죽는다.** 캔버스 안 글자는 검색·복사·번역·스크린리더 모두에서 빠진다.
- **모바일에서 깨진다.** 고정 종횡비가 좁은 폭에서 잘리거나 과축소된다.

`vt-` 템플릿은 이 모든 것을 실제 HTML 텍스트로 해결한다. 절차·비교·정책·리스크·학습 구조처럼 **본문과 같은 호흡으로 읽혀야 하는 다이어그램**은 SVG가 아니라 이 템플릿으로 만든다.

## 2. 21종 카탈로그

| no | slug | 이름 | 용도 / 언제 쓰나 | 핵심 클래스 네임스페이스 |
|---|---|---|---|---|
| 01 | hero-map | Hero Map | 상단 대표 구조도: 문제→지도→행동 3단 + 큰 결론 | `.hm-grid` `.hm-card` `.hm-result` |
| 02 | decision-tree | Decision Tree | 선택 기준·분기형 판단 흐름 | `.dt-q` `.dt-card` `.dt-arrow` `.dt-options` |
| 03 | risk-matrix | Risk Matrix | 확률×영향 리스크 매트릭스, 우선순위 | `.rm-grid` `.rm-cell` `.rm-head` `.rm-risk`(`.high/.med/.low`) |
| 04 | timeline | Timeline | 로드맵·사건 흐름·학습 진행 | `.tl` `.tl-item` |
| 05 | checklist-flow | Checklist Flow | 운영 절차·체크리스트·완료 조건 | `.cf` `.cf-item` `.cf-check` `.cf-state` |
| 06 | quality-gate | Quality Gate | 검수 기준·릴리즈 게이트·감사 항목 | `.qg-grid` `.qg-card`(`.warn/.block`) `.qg-final` |
| 07 | card-grid | Card Grid | 모드/카테고리/키워드/플랫폼 카드 분류 | `.cg-grid` `.cg-card` |
| 08 | raci | RACI | 역할·책임 매트릭스(R/A/C/I) | `.raci` `.h` `.task` `.r` `.a` |
| 09 | file-tour | File Tour | 파일/디렉터리 구조 안내 + 주석 | `.ft` `.ft-card` `.ft-head` `.ft-body` `.ft-note` |
| 10 | flowchart | Flowchart | 좌→우 절차 노드 흐름 | `.fc` `.fc-node`(`.hot`) `.fc-arrow` |
| 11 | weekly-status | Weekly Status | 주간 지표·진행률 대시보드 | `.vt-four` `.vt-stat` `.wk-bars` `.wk-row` `.wk-bar` `.wk-fill` `.wk-cols` `.wk-col` |
| 12 | incident-summary | Incident Summary | 사고 회고: 영향·원인·조치 요약 | `.inc-head` `.inc-card`(`.impact/.cause/.action`) |
| 13 | comparison-cards | Comparison Cards | 후보 N개 나란히 비교, 승자 강조 | `.cmp` `.cmp-card`(`.pick`) |
| 14 | process-swimlane | Process Swimlane | 역할별 레인으로 나눈 프로세스 | `.swim` `.lane` `.lane-label` `.lane-step`(`.blank`) |
| 15 | concept-explainer | Concept Explainer | 개념을 요약→구조→근거→행동 4단으로 풀기 | `.concept-ring` `.concept-steps` `.concept-step` |
| 16 | implementation-plan | Implementation Plan | 마일스톤·리스크가 있는 실행 계획 | `.plan-grid` `.milestone` `.plan-risk` |
| 17 | pr-writeup | PR Writeup | 변경 요약·diff·파일별 워크스루 | `.pr-box` `.pr-diff` `.pr-add` `.pr-del` `.pr-walk` `.pr-file` |
| 18 | triage-board | Triage Board | 트리아지/운영 칸반(상태 컬럼) | `.board` `.board-col` `.ticket`(`.active`) |
| 19 | feature-flag | Feature Flag | 배포/피처 플래그 토글 현황 | `.flag-list` `.flag` `.switch`(`.off`) |
| 20 | prompt-tuner | Prompt Tuner | 프롬프트 템플릿·점수 튜닝 뷰 | `.tuner` `.tune-box` `.score`(`span.on`) |
| 21 | soft-workflow-map | Soft Workflow Map | 입력 ∥ 중앙 대시보드 ∥ 결과로 수렴하는 AI/에이전트 프로세스 맵(소프트 카드뷰). `hero-map`이 단일 축이라면 이건 좌우 카드가 중앙 집계 패널로 수렴하는 3컬럼형 | `.wf-board` `.wf-map` `.wf-col` `.wf-card` `.wf-center` `.wf-metrics` `.wf-pipes` |

> 공통 셸·요소 네임스페이스는 모든 템플릿이 공유한다: `.vt-shell` `.vt-frame` `.vt-demo` `.vt-kicker` `.vt-title` `.vt-text` `.vt-section-title` `.vt-num` `.vt-pill`(`.hot/.good/.watch`) `.vt-list` `.vt-two` `.vt-four` `.vt-stat` 등. 색 토큰은 `--vt-red/--vt-blue/--vt-green/--vt-gold`이며 모두 스킬 테마 토큰(`var(--accent)`, `var(--line)`, `var(--ink)` …) 위에서 파생된다. 카드별 강조색은 인라인 `style="--c:var(--vt-blue)"`로 바꾼다.

## 3. 모드 → 템플릿 매핑 (캐노니컬, 단일 출처)

각 모드의 **첫 번째 항목이 1순위**다. 이 표가 모드별 템플릿 선택의 유일한 정본이며, 다른 문서의 매핑과 충돌하면 이 표를 따른다.

| 모드 | 1순위 | 그 외 권장 |
|---|---|---|
| beginner_html | **concept-explainer** | hero-map, checklist-flow |
| expert_html | **risk-matrix** | raci, quality-gate, implementation-plan, soft-workflow-map |
| article_html | **decision-tree** | comparison-cards, concept-explainer |
| education_html | **timeline** | checklist-flow, concept-explainer, soft-workflow-map |
| github_analysis | **hero-map** | quality-gate, file-tour, risk-matrix, timeline, decision-tree, checklist-flow |
| github_feature_usage | **hero-map** | card-grid, file-tour, decision-tree |
| youtube_analysis | **timeline** | risk-matrix, quality-gate, decision-tree, comparison-cards, checklist-flow |
| manual_analysis | **hero-map** | checklist-flow, quality-gate, file-tour, process-swimlane, decision-tree, risk-matrix |
| blog_writer | **timeline** | weekly-status, comparison-cards |
| seo_dashboard | **card-grid** | comparison-cards, prompt-tuner |
| platform_blog | **card-grid** | comparison-cards, pr-writeup |
| skill_audit | **quality-gate** | file-tour, prompt-tuner, implementation-plan, soft-workflow-map |
| reference_html | **file-tour** | flowchart, card-grid |
| comparison_html | **comparison-cards** | decision-tree, risk-matrix |
| case_study_html | **incident-summary** | timeline, process-swimlane |
| landing_brief_html | **hero-map** | card-grid, feature-flag, soft-workflow-map |
| checklist_playbook | **checklist-flow** | quality-gate, process-swimlane, implementation-plan, triage-board |

### github_analysis 권장 삽입 순서

GitHub 저장소 분석은 첫 화면에서 판단 구조가 보여야 하므로 `hero-map`을 1순위로 사용한다. 이후 저장소 구조 설명은 `file-tour`, 채택 리스크는 `risk-matrix`, 검증 기준은 `quality-gate`, 최근 활동은 `timeline`, 최종 선택은 `decision-tree`, 다음 행동은 `checklist-flow`로 보강한다.

- `hero-map`: 프로젝트 목적 → 저장소 신호 → 추천 행동.
- `file-tour`: README, package/manifest, src, tests, docs, CI, security 관련 파일 경로.
- `risk-matrix`: 유지보수 정체, 빠진 라이선스, 취약한 quickstart, 테스트 부재, 릴리스 부재 등.
- `quality-gate`: 사용/검토/보류 판단을 위한 최소 검증 조건.

### github_feature_usage 권장 삽입 순서

GitHub 기능·사용 가이드는 첫 화면에서 "무엇을 해주는가"가 보여야 하므로 `hero-map`을 1순위로 사용한다. 이후 기능 분류는 `card-grid`, 디렉터리 구조 해부는 `file-tour`, 도입 적합성 판단은 `decision-tree`로 보강한다.

- `hero-map`: 제품 정체성 → 핵심 기능 → 시작 행동.
- `card-grid`: 사용자 기능, 관리자 기능, 운영 기능, 연동 기능.
- `file-tour`: 기능과 연결되는 주요 디렉터리/파일.
- `decision-tree`: 맞는 사용처, 맞지 않는 사용처, 도입 전 확인.


### youtube_analysis 권장 삽입 순서

YouTube 분석은 `timeline`을 1순위로 사용해 영상 흐름·타임스탬프 근거를 먼저 보여준다. 주장 위험은 `risk-matrix`, 검증 기준은 `quality-gate`, 볼지/제작할지 선택은 `decision-tree`, 대안 콘텐츠 비교는 `comparison-cards`, 다음 행동은 `checklist-flow`로 보강한다.

### manual_analysis 권장 삽입 순서

Manual 분석은 `hero-map`을 1순위로 사용해 독자 역할·목표·첫 행동을 첫 화면에서 분기한다. 실행 절차는 `checklist-flow`, 안전/완료 기준은 `quality-gate`, 원문 구조는 `file-tour`, 운영 흐름은 `process-swimlane`, 선택 기준은 `decision-tree`, 위험 작업은 `risk-matrix`로 보강한다.

## 4. SVG vs HTML 선택 규칙

| 상황 | 선택 |
|---|---|
| 본문 흐름 한가운데, 독자가 바로 읽고 판단해야 하는 구조도 | **HTML 템플릿(`vt-`)** |
| 절차·비교·정책·리스크·학습 구조 (텍스트가 정보의 핵심) | **HTML 템플릿(`vt-`)** |
| 모바일 390px에서 잘림 없이 줄바꿈되어야 하는 다이어그램 | **HTML 템플릿(`vt-`)** |
| 페이지 상단 hero용 큰 요약 한 장 | SVG 인포그래픽(`8000×6000`) 가능 |
| 다운로드·인쇄·발표 슬라이드 별첨 | SVG 인포그래픽 |
| 실제 인물·장소·제품·사건 증거 | 공개 라이선스 사진(출처·라이선스 명시) |
| 메타포/컨셉 일러스트 | AI 생성(사실 이미지로 오인되지 않게) |

원칙: **본문에 끼우는 구조도는 HTML 템플릿이 기본값**이다. SVG는 큰 요약·별첨, 사진/일러스트는 사실/감성 보강으로 역할을 분리한다.

## 5. 삽입법

1. **템플릿 복사**: `assets/visual-html-templates/<no>-<slug>.html`(예: `15-concept-explainer.html`)의 마크업을 복사해 콘텐츠만 교체한다. 파일은 이미 `vt-shell` → `vt-frame` 래퍼로 감싸져 있다.

   ```html
   <section class="vt-shell">
     <div class="vt-frame">
       <!-- 여기에 vt-demo / hm-grid / dt-q 등 템플릿 본문 -->
     </div>
   </section>
   ```

2. **CSS 인라인**: `assets/visual-html.css` 전체를 출력 HTML `<head>`의 `<style>`에 인라인한다. 별도 `<link>`나 외부 파일 참조를 만들지 않는다(외부 의존 0 유지). 이 CSS는 스킬 테마 토큰 위에서 동작하므로 코어 CSS 다음에 둔다.

3. **삽입 위치**: 다이어그램 블록은 `<main id="main">` 안의 해당 섹션에 배치하며, 본문 흐름을 끊지 않는 보조 뷰로 쓴다.

4. **무 JS**: 복사한 마크업에 `<script>`를 절대 추가하지 않는다. 모든 `vt-` 템플릿은 정적이며 인터랙션이 없다(인터랙션이 필요하면 그것은 이 라이브러리가 아니라 CSS 뷰 위젯 `wg-` 쪽 일이다).

### 코어 CSS 5종 해시 + 조건부 인라인과의 관계

스킬의 **코어 CSS는 5종**(`theme.css` → `components.css` → `visual-components.css` → `layouts.css` → `print.css`)이며, 이 합본의 SHA-256만 해시 대상이고 인라인 블록 선두에 마커를 남긴다.

```css
/* adaptive-html-final-core-css-sha256: <hash> */
```

`widgets.css`·`visual-html.css`는 **코어 5종 해시에 포함되지 않는 조건부 인라인 라이브러리 CSS**다(프로파일에 따라 포함 여부가 갈림 — diagram=visual-html만/widget=widgets만/auto=둘 다). `vt-` 템플릿을 실제로 사용한 출력물(diagram·auto)에서만 `visual-html.css`를 코어 인라인 블록 **다음에**(widgets 슬롯 뒤) 이어 인라인한다. 출력 폴더를 만들면 사용한 CSS 스냅샷과 합본 해시를 `sources/assets/*.css`, `sources/css-integrity.json`에 남기고 인라인 CSS 마커와 일치시킨다(`scripts/validate_output.py`로 검증).

## 6. 무 JS · 접근성 · 반응형 규칙

- **외부/동작 JS 0 (불변식)**: `vt-` 템플릿에는 어떤 스크립트도 넣지 않는다. JSON-LD(`application/ld+json`)만 예외로 허용되며 이는 메타데이터이지 동작 코드가 아니다.
- **색 외 단서 의무**: 상태/심각도를 색만으로 구분하지 않는다. `.rm-risk.high/.med/.low`, `.qg-card.warn/.block`, `.inc-card.impact/.cause/.action`, `.vt-pill.hot/.good/.watch` 등은 항상 텍스트 라벨을 함께 둔다(색맹 대응).
- **feature-flag(19)는 3-상태 + 텍스트 라벨**: 토글(`.switch.on/.warn/.off`)은 색·노브 위치만으로 상태를 전달하므로 `aria-hidden="true"` 장식으로 두고, 의미는 인접한 `.flag-state.on/.warn/.off`의 **가시 텍스트(ON/WARN/OFF)**가 전달한다(스크린리더 노출 + 색맹 대응). 형태 단서로 `.flag-state:before` 점이 상태별로 원/사각/링으로 달라진다.
- **시맨틱 마크업**: 카드는 `<article>`, 목록은 `<ul>/<li>`, 제목 계층(`h2/h3`)을 유지한다. 표형 템플릿(raci·risk-matrix)도 의미가 표면 `<table>`/`<caption>`을 우선한다.
- **`role="img"`로 텍스트를 가두지 말 것 (vt-21 soft-workflow-map 핵심 규칙)**: 실제 본문 텍스트를 담은 컨테이너(`.wf-board`/`.wf-map`)에 `role="img"`+단일 `aria-label`을 걸면 스크린리더가 내부 카드 텍스트(`.wf-card`의 `<strong>`/`<p>`)와 지표(`.wf-metric`)를 **전부 prune**해 정보가 사라진다. 따라서 프레임에는 `role="img"`를 쓰지 않는다. 순수 장식 그래픽(`.wf-codewin`·`.wf-dash`·`.wf-pipes`·`.wf-bottom`·`.wf-icon`·`.wf-aistack`)에만 `aria-hidden="true"`를 부여하고, 카드·지표 텍스트는 일반 DOM으로 노출한다. 이미지 안에 작은 텍스트를 박제하지 말고 본문 정보는 HTML 텍스트로 둔다.
- **링크 터치 타깃**: `.vt-nav a`, `.vt-source a` 등 링크는 `min-height` 44px 안팎을 보장한다(모바일 탭 영역).
- **반응형 브레이크포인트 2단**:
  - `@media(max-width:920px)` — 멀티컬럼 그리드(hm-grid·dt-q·qg-grid·cmp·board·tuner 등)를 1컬럼으로, `decision-tree` 화살표는 가로→세로로, `flowchart` 화살표는 90도 회전, `swimlane`은 레인 라벨을 칩으로 전환.
  - `@media(max-width:760px)` — `.vt-shell`/`.vt-frame` 패딩 축소, `.vt-shell-head` 세로 적층, `card-grid`·`concept-steps`를 1컬럼으로, 링크 터치 타깃 44px 재확보.
- **모션 안전**: 정적 템플릿이라 자동 모션이 없지만, 도입처에서 트랜지션을 얹는 경우 `prefers-reduced-motion`에서 최종 상태로 폴백한다.
- **모바일 무손실**: 390px에서 카드/표/캡션 텍스트가 잘리지 않아야 한다(품질 게이트 항목과 동일).

## 7. 적용 갤러리

- 카탈로그·전략 원본: `output/adaptive-html-final-html-view-templates-20-v1/`(초기 20종 라이브 데모 + `SVG_TO_HTML_TEMPLATE_STRATEGY.md`; 이후 21번째 `soft-workflow-map`이 후순위 템플릿으로 편입됨).
- 현행 17모드 참조 예제: **`skills/adaptive-html-final/examples/`** — v5.10.3 스킬 자산 기준의 17모드 레퍼런스이며, §0.6의 1순위 vt 계약과 8테마/무JS 검증을 통과해야 한다.
- 역사적 적용 갤러리: **`output/adaptive-html-final-showcase-v6`** — v4.5 동결 시점의 모드별 페이지와 QA 스크린샷 확인용이다. 현재 17모드 기준선이나 21종 완전 적용 증거로 사용하지 않는다.

## 관련 문서

- `references/widget-system.md` — CSS 뷰 위젯 `wg-01`~`20`(인터랙션 보조 뷰, 이 라이브러리와 별개).
- `references/visual-template-system.md` — `8000×6000` SVG 인포그래픽(hero·별첨용, HTML 템플릿이 대체하는 대상).
- `references/mode-selection.md` — 17개 모드 라우팅.
