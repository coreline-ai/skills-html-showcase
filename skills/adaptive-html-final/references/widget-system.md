# Widget System

`html-effectiveness` 실험에서 검증한 20종 뷰 위젯을 `adaptive-html-final`의 정식 자산으로 편입한다. 각 위젯은 모드별 출력물에 끼워 넣는 "뷰 블록"이며, 외부 사진/라이브러리 없이 시맨틱 HTML + 토큰 기반 CSS로 정보를 보강한다.

기본 철학은 **외부 JS 0**이다. 모든 스니펫은 스크립트 태그 없이 동작하며(20종 전부 `<script>` 0개 확인), 인터랙션이 필요한 곳도 CSS 네이티브 기법(`:checked`, `:target`, `<details>`, `:has()`, `scroll-snap`)으로 근사한다. 드래그앤드롭·라이브 편집·키보드 단축키 같은 "완전 인터랙션"은 선택적 점진 향상(progressive enhancement)으로만 추가한다.

## 사용 규칙

1. **CSS 인라인**: `assets/widgets.css`(약 81KB) 전체를 `base.html`의 `{{WIDGETS_CSS}}` 슬롯에 인라인한다. 별도 `<link>`나 외부 파일 참조를 만들지 않는다. 슬롯 순서는 `THEME → COMPONENTS → VISUAL_COMPONENTS → WIDGETS → VISUAL_HTML → BODY_ICONS → EDITORIAL_PATTERNS → SHAPE_VISUALS → WORKFLOW_VISUALS → LAYOUTS → PRINT`이며, 미사용 조건부 슬롯은 빈 문자열로 치환한다.
2. **네임스페이스**: 모든 위젯 클래스·커스텀 프로퍼티는 `wg-<id>-` 접두사를 쓴다(예: `wg-07-anim`, `--wg07-dur`). id는 2자리(`01`~`20`). 본문 컴포넌트(`components.css`)와의 충돌을 막기 위해 위젯 내부 셀렉터는 반드시 이 네임스페이스 안에서만 작성한다.
3. **외부 JS 0 유지**: 스니펫에 `<script>`를 넣지 않는다. 18(칸반)·20(프롬프트 튜너)처럼 본질이 편집 인터페이스인 위젯은 **CSS 근사를 기본값**으로 제공하고, 완전 인터랙션(드래그 이동·실시간 카운트·라이브 변수 치환·LLM 재생성)은 도입처에서 선택적 점진 향상으로만 얹는다. 스킬 기본 출력은 무 JS 근사 상태를 유지한다.
4. **색 외 단서 의무**: 상태/심각도를 색으로만 구분하지 않는다. 텍스트 라벨·글리프(`●◐○`, `✓`, `!`, `⚠`, `○→●`)·패턴을 병기한다(접근성 색맹 대응).
5. **모션 안전**: 애니메이션을 쓰는 위젯(02·07·11 등)은 `prefers-reduced-motion`에서 정지+최종 상태로 폴백한다.
6. **삽입 위치**: 위젯 블록은 `<main id="main">` 내부의 해당 섹션에 배치하며, 본문 흐름을 끊지 않는 보조 뷰로 쓴다.

## 위젯 20종 카탈로그

인터랙티브 분류 표기는 각 스니펫 파일 선두 주석의 실제 구현 기준이다.

- **CSS-only**: 외부 JS 없이 의도한 인터랙션이 완결됨.
- **부분(css-partial)**: 핵심 표현은 CSS-only, 일부 고급 기능만 JS 필요(기본 출력에는 포함하지 않음).
- **JS 필요(js-needed)**: 완전 인터랙션에 JS가 필수. 스킬 기본은 CSS 근사로 동작.

| # | 이름 | 용도 / 언제 쓰나 | 권장 모드 | 인터랙티브 분류 + 무JS 구현 기법 | 스니펫 경로 |
|---|---|---|---|---|---|
| 01 | Three Code Approaches | 같은 문제의 구현/대안 코드 3안을 장단점·트레이드오프와 함께 나란히 비교 | comparison_html, expert_html | 부분 — 카드·태그 정적, 코드 블록 `tabindex`로 포커스·가로 스크롤, hover transition. 라이브 실행/구문 토글만 JS | `assets/widget-templates/01-three-code-approaches.html` |
| 02 | Visual Design Directions | 디자인 시안 3방향을 미니 라이브 렌더로 비교·선택 | article_html / landing_brief_html, platform_blog, reference_html | CSS-only — `radio:checked + .card` 인접 셀렉터로 테두리·뱃지·`○→●` 전환. 토큰 편집/export만 JS | `assets/widget-templates/02-visual-design-directions.html` |
| 03 | Annotated Pull Request | 코드/diff에 심각도별 인라인 주석을 단 리뷰·진단 뷰 | skill_audit, expert_html, reference_html | 부분 — severity 색+라벨+아이콘(`!`/`i`), `:target`로 라인 점프. 코멘트 펼침/작성만 JS | `assets/widget-templates/03-annotated-pull-request.html` |
| 04 | Module Map | 아키텍처/모듈 의존 구조를 노드·엣지로 시각화 | expert_html, github_analysis, reference_html, article_html | 부분 — SVG 노드/엣지 정적, 핵심 경로는 색+굵기+범례+경로 칩, hover transition. 클릭 확장·드래그·줌만 JS | `assets/widget-templates/04-module-map.html` |
| 05 | Living Design System | 디자인 토큰(색·타이포·스페이싱)을 접기형으로 문서화 | reference_html, landing_brief_html | 부분 — `<details>/<summary>` 네이티브 접기, 토큰 값 텍스트 노출. 클릭 복사(클립보드 API)만 JS | `assets/widget-templates/05-living-design-system.html` |
| 06 | Component Variants | 컴포넌트 상태/변형(default·hover·disabled·다크)을 매트릭스로 문서화 | reference_html, education_html | CSS-only — `radio:checked ~` 형제로 라이트/다크 토글, 상태는 `.wg-06-is-*` 고정 + statetag 라벨 | `assets/widget-templates/06-component-variants.html` |
| 07 | Animation Sandbox | 애니메이션 프리셋(slide/fade/scale/rotate·duration·easing)을 설명·실연 | reference_html / education_html, article_html | CSS-only — `@keyframes` 자동재생 + `radio:checked + :has()`로 `--wg07-dur/ease` 교체, readout도 `:has()`. 자유값 슬라이더만 JS. `:has()` 미지원 시 기본 프리셋 폴백 | `assets/widget-templates/07-animation-sandbox.html` |
| 08 | Clickable Flow | 화면 전환형 클릭 프로토타입(가입·결제 등 UX 흐름) | landing_brief_html, education_html | CSS-only — `:target` + `:target-within`로 화면 전환, 앵커 링크 네비. 폼 상태 저장만 JS(프로토타입엔 불필요) | `assets/widget-templates/08-clickable-flow.html` |

> **wg-08 static 변형(`.wg-08-static-*`)**: `:target`/`:has`를 쓰지 않는 **읽기 전용 정적 스테퍼**(번호+커넥터, `--hot`/`--ok` 상태). 인터랙션이 불가/불필요한 환경(이식성 우선)에서 클릭 플로우 대신 사용. 마크업: `.wg-08-static > .wg-08-static-step(.wg-08-static-step--hot/--ok) > .wg-08-static-no + div(h3+p)`. `final_20260604`의 `static-flow-*`를 정본 네임스페이스로 개명·토큰화한 것.
| 09 | Arrow-Key Slide Deck | 발표형 슬라이드 덱(좌우 슬라이드 전환) | article_html / landing_brief_html, education_html | **JS 필요** — `scroll-snap`(스와이프) + 점/앵커(`:target`) 2중 CSS-only 경로 제공. 화살표키 이동·자동재생은 JS 필수. 무JS에선 트랙 포커스 후 스크롤/Tab+Enter로 접근 | `assets/widget-templates/09-arrow-key-slide-deck.html` |
| 10 | SVG Figure Sheet | 일러스트/개념도 4종 SVG 시트(개념 도해) | article_html, beginner_html, education_html | CSS-only — 순수 인라인 SVG, fill/stroke 전부 theme 토큰 `var()`, `role=img`+`<title>` 라벨. 정적 시트 | `assets/widget-templates/10-svg-figure-sheet.html` |
| 11 | Weekly Status | 주간 지표/진행률 대시보드 리포트 (거버넌스·운영 상태 보드의 **정본**) | github_analysis, seo_dashboard, expert_html, checklist_playbook | CSS-only — `final_20260604` section 28의 KPI/status board를 정본화. 4 KPI 카드 + 워크스트림 진행률 + 완료/진행/리스크 3열을 기본 구조로 쓰고, 막대 `width%` + `@keyframes` 그로우, 색+점+라벨+`wg-11-fill-risk` **빗금**으로 이중 표기. ≤480px에서 막대 라벨이 위로 적층 | `assets/widget-templates/11-weekly-status.html` |

> **상태/거버넌스 보드는 wg-11로 통일**: 별도 `edge-status-*`/색-단독 진행바를 새로 만들지 않는다. final 검수본의 시각 밀도는 `wg-11-kpi-*`, `wg-11-col-*`, `wg-11-tk`, `wg-11-flag`로 흡수했다. 저장소 health, 운영 주간 리포트, 거버넌스 M1/M2 상태판은 모두 wg-11을 재사용한다(WCAG 1.4.1).
| 12 | Incident Timeline | 사고 회고/포스트모템 타임라인 + 액션 체크리스트 | case_study_html, expert_html | 부분 — `checkbox:checked + label` 완료 표시(취소선·체크마크), 타임라인 정적. 상태 저장·집계만 JS | `assets/widget-templates/12-incident-timeline.html` |
| 13 | Annotated Flowchart | 절차·흐름 다이어그램에 단계별 상세 주석 | education_html / beginner_html, checklist_playbook, expert_html, article_html | CSS-only — 단계 박스 앵커로 `<details>` 점프(`:target` 하이라이트), 실패 경로는 danger 색+`!`+'실패 경로' 라벨, 화살표는 텍스트 글리프 | `assets/widget-templates/13-annotated-flowchart.html` |
| 14 | Feature Explainer | 기능 설명 + 탭 전환 코드 예제(CLI/API 등) + FAQ | github_analysis, education_html, reference_html, article_html | CSS-only — `radio:checked ~` 형제로 코드 패널 탭, `<details>` 접기·FAQ. JS 없음 | `assets/widget-templates/14-feature-explainer.html` |
| 15 | Concept Explainer | 개념을 단계 전환·비교표로 푸는 교보재 | beginner_html, education_html, reference_html | CSS-only — `radio:checked ~` 형제로 패널·링 노드 동시 갱신, 비교표 정적, 화살표·경고 글리프. JS 없음 | `assets/widget-templates/15-concept-explainer.html` |
| 16 | Implementation Plan | 실행 계획/로드맵(마일스톤·플로우·리스크·운영 모델) | github_analysis, expert_html, landing_brief_html, checklist_playbook | CSS-only — `final_20260604` section 27의 거버넌스 운영 팩을 정본화. 마일스톤 타임라인 + 데이터/운영 플로우 + 리스크 표를 한 블록에 묶고, 리스크 레벨은 색+`●◐○` 이중 표기. 텍스트 포함 컨테이너에 `role="img"`를 쓰지 않는다. JS 없음 | `assets/widget-templates/16-implementation-plan.html` |
| 17 | PR Writeup | 변경 요약/개발 회고(파일별 접기 + Before/After) | github_analysis, skill_audit, blog_writer, expert_html | CSS-only — 파일별 `<details>/<summary>` 접기, 캐럿 회전은 `[open]`+transition, Before/After 정적 그리드. diff 펼침·인라인 주석만 JS | `assets/widget-templates/17-pr-writeup.html` |
| 18 | Ticket Triage Board | 트리아지/운영 칸반 보드(우선순위·상태) | github_analysis, checklist_playbook, expert_html | **JS 필요** — 정적 칸반이 기본: 우선순위 칩+컬럼 보더 색+도트/카운트, 색 외 `●`/`✓` 단서, hover/focus 리프트 transition. **완전 인터랙션(드래그앤드롭 이동·실시간 카운트)은 선택적 점진 향상으로만 JS 추가**, 스킬 기본은 무JS 근사 | `assets/widget-templates/18-ticket-triage-board.html` |
| 19 | Feature Flag Editor | 배포/피처 플래그 토글 편집 뷰 | checklist_playbook, reference_html, expert_html | 부분 — `checkbox:checked + label`로 트랙 색·노브·ON/OFF 즉시 전환, 경고는 `⚠`+텍스트, 키보드 포커스·focus-visible 링. 의존성 자동 비활성·JSON export·서버 반영만 JS | `assets/widget-templates/19-feature-flag-editor.html` |
| 20 | Prompt Tuner | 프롬프트 템플릿 문서·샘플 전환 뷰 | reference_html, education_html | 부분(편집 본질) — `radio:checked ~ .grid` 형제로 샘플 입력/렌더 탭 전환, `{{...}}` 변수 정적 강조, 칩 라디오 키보드 이동·focus-visible. **완전 인터랙션(라이브 편집·변수 치환·LLM 재생성)은 선택적 점진 향상으로만 JS 추가**, 스킬 기본은 무JS 근사 | `assets/widget-templates/20-prompt-tuner.html` |

### 인터랙티브 분류 집계

| 분류 | 개수 | 위젯 |
|---|---|---|
| CSS-only (완전 무JS) | 11 | 02, 06, 07, 08, 10, 11, 13, 14, 15, 16, 17 |
| 부분 (css-partial, 핵심만 무JS) | 7 | 01, 03, 04, 05, 12, 19, 20 |
| JS 필요 (완전 인터랙션, 기본은 CSS 근사) | 2 | 09, 18 |

> 참고: "편집 인터페이스" 본질을 가진 18(칸반)·20(프롬프트 튜너)는 사용 규칙상 "완전 인터랙션은 선택적 점진 향상" 대상으로 함께 묶어 관리한다. 위 집계는 각 스니펫 파일 선두 주석의 실제 구현 분류(09·18이 js-needed, 20은 css-partial)를 그대로 반영한 것이다. 어느 기준으로 보든 무JS 11 / 부분 7 / JS 2 비율은 동일하다.

## 모드 → 권장 위젯 매핑

각 모드에서 우선 고려할 위젯을 근거 매핑 기준으로 정리한다. 굵은 항목이 1순위 추천이다.

| Mode | 권장 위젯 | 쓰임 |
|---|---|---|
| skill_audit | **03 Annotated PR**, 11 Weekly Status, **17 PR Writeup** | 코드/diff 진단, 감사 진행 상태, 변경 요약 |
| expert_html | **04 Module Map**, **16 Implementation Plan**, 01, 03, 11, 12, 13, 17, 18, 19 | 아키텍처·실행계획·리포트·코드 리뷰·회고. 단, `.validation-checklist` 안에는 `wg-03`/`wg-17`을 넣지 않는다(검증 섹션은 증빙 매트릭스·quality-gate 전용). |
| article_html | **02 Visual Design Directions**, **10 SVG Figure Sheet**, 04, 07, 09, 13, 14 | 시안 비교·일러스트·발표·흐름 |
| education_html | **14 Feature Explainer**, **15 Concept Explainer**, 06, 07, 08, 09, 10, 13, 20 | 학습/탭 코드·개념·인터랙션 설명·UX 흐름 |
| github_analysis | **11 Weekly Status**, **04 Module Map**, **14 Feature Explainer**, **16 Implementation Plan**, 17, 18 | 저장소 활동/건강도, 코드 구조, quickstart, 후속 실행, PR·이슈 신호 |
| youtube_analysis | **11 Weekly Status**, **13 Annotated Flowchart**, **14 Feature Explainer**, **16 Implementation Plan**, 18 | 영상 메타/댓글 신호, 타임스탬프 흐름, 콘텐츠 기회, 제작 실행 |
| manual_analysis | **04 Module Map**, **13 Annotated Flowchart**, **16 Implementation Plan**, **18 Ticket Triage Board**, 11, 14 | 문서 구조, 절차, 운영 계획, 문제/위험 트리아지 |
| beginner_html | **15 Concept Explainer**, 10, 13 | 개념 교육·개념도·절차 |
| blog_writer | **17 PR Writeup** | 개발 회고 |
| seo_dashboard | **11 Weekly Status** | 지표 대시보드 |
| platform_blog | **02 Visual Design Directions** | 플랫폼별 렌더 비교 |
| reference_html | **05 Living Design System**, **06 Component Variants**, **14 Feature Explainer**, **20 Prompt Tuner**, 02, 03, 04, 07, 15, 19 | 디자인 토큰·컴포넌트·API·프롬프트·패턴 문서 |
| comparison_html | **01 Three Code Approaches** | 구현/대안 코드 비교 |
| case_study_html | **12 Incident Timeline** | 사고 회고/포스트모템 |
| landing_brief_html | **08 Clickable Flow**, 02, 05, 09, 16 | 프로토타입·시안·발표·로드맵 |
| checklist_playbook | **13 Annotated Flowchart**, **18 Ticket Triage Board**, **19 Feature Flag Editor**, 11, 12, 16 | 절차·트리아지·플래그·운영 체크 |

### github_analysis 조합 가이드

GitHub 분석은 위젯을 과삽입하지 않는다. `wg-11`로 최근 활동·릴리스·이슈 상태 같은 관측 신호를 요약하고, 저장소 구조가 복잡할 때만 `wg-04`를 추가한다. 실행/설치가 핵심이면 `wg-14`, 채택 후 계획이 필요하면 `wg-16`, PR/이슈 흐름을 보여줄 필요가 있을 때만 `wg-17` 또는 `wg-18`을 쓴다.

### 위젯 → 모드 역참조

빠른 선택을 위한 역방향 인덱스다.

| # | 이름 | 권장 모드(1순위 먼저) |
|---|---|---|
| 01 | Three Code Approaches | comparison_html, expert_html |
| 02 | Visual Design Directions | article_html / landing_brief_html, platform_blog, reference_html |
| 03 | Annotated Pull Request | skill_audit, expert_html, reference_html |
| 04 | Module Map | manual_analysis, github_analysis, expert_html, reference_html, article_html |
| 05 | Living Design System | reference_html, landing_brief_html |
| 06 | Component Variants | reference_html, education_html |
| 07 | Animation Sandbox | reference_html / education_html, article_html |
| 08 | Clickable Flow | landing_brief_html, education_html |
| 09 | Arrow-Key Slide Deck | article_html / landing_brief_html, education_html |
| 10 | SVG Figure Sheet | article_html, beginner_html, education_html |
| 11 | Weekly Status | youtube_analysis, github_analysis, manual_analysis, seo_dashboard, expert_html, checklist_playbook |
| 12 | Incident Timeline | case_study_html, expert_html |
| 13 | Annotated Flowchart | manual_analysis, youtube_analysis, education_html / beginner_html, checklist_playbook, expert_html, article_html |
| 14 | Feature Explainer | youtube_analysis, manual_analysis, github_analysis, education_html, reference_html, article_html |
| 15 | Concept Explainer | beginner_html, education_html, reference_html |
| 16 | Implementation Plan | manual_analysis, youtube_analysis, github_analysis, expert_html, landing_brief_html, checklist_playbook |
| 17 | PR Writeup | github_analysis, skill_audit, blog_writer, expert_html |
| 18 | Ticket Triage Board | manual_analysis, youtube_analysis, github_analysis, checklist_playbook, expert_html |
| 19 | Feature Flag Editor | checklist_playbook, reference_html, expert_html |
| 20 | Prompt Tuner | reference_html, education_html |

## 무JS 인터랙션 기법 요약

위젯이 외부 JS 없이 인터랙션을 구현할 때 쓰는 CSS 네이티브 패턴:

- **탭/선택 전환** — `input[type=radio]:checked ~`/`+` 형제·인접 셀렉터(02·06·14·15·20), `:has()`로 변수 교체(07).
- **접기/펼치기** — 네이티브 `<details>/<summary>`(05·13·14·17), `[open]` 상태 + transition.
- **화면/앵커 점프** — `:target`·`:target-within`(03·08·13), `scroll-snap`(09).
- **완료/토글 상태** — `checkbox:checked + label`(12·19).
- **모션** — `@keyframes` 자동재생(02·07·11) + `prefers-reduced-motion` 폴백.
- **접근성** — 색 외 글리프/라벨 병기, SVG `role=img`+`<title>`(10·16), focus-visible 링(19·20).

## 품질 게이트

위젯을 출력물에 편입할 때 다음을 확인한다.

- `widgets.css`가 `{{WIDGETS_CSS}}` 슬롯에 인라인되어 있고 외부 참조가 없다.
- 모든 위젯 셀렉터가 `wg-<id>-` 네임스페이스 안에 있다.
- 출력 HTML에 `<script>`가 0개다(점진 향상 JS를 의도적으로 추가한 경우 제외, 그 경우에도 무JS 폴백이 동작).
- 상태/심각도가 색 외 단서(텍스트·글리프·패턴)를 함께 가진다.
- 모션 위젯이 `prefers-reduced-motion`에서 정지+최종 상태로 폴백한다.
- 18·20을 무JS 상태로 넣었다면 "정적 근사" 임을 캡션/주석으로 밝힌다.
- 모바일 390px에서 위젯 내부 카드·코드·SVG가 잘리거나 넘치지 않는다.

> 배정 원칙: 콘텐츠 적합성 우선(모드 1순위와 다를 수 있음).
>
> 위젯 적용 갤러리: `output/adaptive-html-final-showcase-v5`
