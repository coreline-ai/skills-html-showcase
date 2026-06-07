# Quality Gates

## Theme Gate

- `theme.css`, `components.css`, `layouts.css`를 모두 연결하거나 `base.html`에 inline으로 합친다. 시각 템플릿을 쓰면 `visual-components.css`도 components 뒤에 합친다.
- 인쇄가 필요한 결과물은 `print.css`를 포함한다.
- 색상 토큰을 페이지별로 임의 변경하지 않는다.
- 외부 JS 없이 열려야 한다.
- 공개 블로그형 결과물은 Pretendard Variable + Noto Serif KR 폰트 링크를 head에 포함한다.
- output 폴더에는 사용 CSS snapshot(`sources/assets/*.css`)과 `sources/css-integrity.json`을 남기고, 인라인 CSS의 `adaptive-html-final-core-css-sha256` 주석이 현재 skill asset 합본 해시와 일치해야 한다.

## Layout Gate

- 선택한 모드의 필수 블록이 모두 포함되어야 한다.
- beginner, article, education, blog, case study는 780px 안팎 읽기 폭을 유지한다.
- expert, seo, platform, audit, reference, comparison, landing, checklist는 1020px 이하 분석 폭을 사용한다.
- 모바일에서는 모든 그리드가 1컬럼으로 내려와야 한다.
- table은 `.tbl` wrapper를 쓰거나 모바일 카드로 대체한다.
- 모바일 390px 폭에서 `<caption>`, 긴 한글 제목, 카드 본문이 잘리지 않아야 한다.
- 표 캡션에는 음수 margin, absolute positioning, hidden overflow를 적용하지 않는다.
- 섹션/카드 내부 첫 heading은 과도한 top margin을 만들지 않아야 한다. `section > h2:first-child`, 카드 컴포넌트 첫 h2/h3는 margin-top 0이어야 한다.
- `.winners`, `.tradeoffs`처럼 h3+ul을 담는 의미형 블록은 자동 2컬럼 grid로 찢지 않는다. 실제 2컬럼이 필요하면 내부에 별도 `.grid-2` wrapper를 사용한다.
- case-study timeline은 section 자체 left rule과 내부 card left rule을 동시에 쓰지 않는다. 순서형 목록 번호가 충분히 보이면 굵은 accent left rule 없이 중립 card border만 쓴다.

## Visual Template Gate

- 섹션 이해를 돕는 시각물이 필요하면 장식 사진보다 8000×6000 SVG 인포그래픽을 우선한다.
- 모든 시각물은 `figure.visual-figure` 또는 `.figure-wide` 래퍼를 사용한다.
- `img`에는 `width`, `height`, `alt`가 있고 바로 뒤에 `figcaption`이 있어야 한다.
- SVG 템플릿 내부 카드/텍스트는 8000×6000 캔버스 밖으로 나가지 않아야 한다.
- `quality-gate`의 하단 강조 패널은 납작한 배너로 만들지 말고 충분한 높이와 footer 여백을 둔다.
- 외부 사진은 출처/라이선스/수정 여부를 기록하고, AI 생성 이미지는 사실 보도·인물·제품 증거처럼 사용하지 않는다.

## Editorial Gate

- 첫 화면은 kicker, h1, sub, meta, divider, toc/summary 순서로 안정적이어야 한다.
- H1은 한국어 긴 제목에서 과하게 커지지 않아야 한다.
- 공개 아티클·블로그·SEO·전문가 리포트 등에서는 주요 h2에 `.h2-sub`를 두는 것을 권장한다(모드 한정 권장, 전 모드 무조건 강제 아님).
- `.term`, `.analogy`, `.danger`, `.good`은 가능한 한 `.label`/`.word`/`.name` 구조를 사용한다.
- prose 65~75%, box 25~35% 비율을 목표로 한다.
- `.hl`은 2~4개만 사용하고, 색상 박스 내부에서는 사용하지 않는다.
- 검정 박스는 마지막 `.try` 중심으로 사용한다.
- 검정 `.try` 내부에 흰 카드(`.box`, `.summary-card`, `.cta-box`, `.card-block`, `.mini-card`)를 넣으면 카드 내부 텍스트 색은 반드시 `var(--ink)`/`var(--ink-soft)`로 되돌린다.
- 검정 `.try`/`.try.soft-cta` 내부 `.tag` pill은 흐린 회색을 상속하면 실패다. 밝은 pill 배경과 `var(--ink)` 굵은 텍스트로 읽혀야 한다.
- `blog_writer`의 본문 section h2는 번호 badge 또는 동등한 진행 표시가 있어야 한다. "왜 지금 ..." 같은 첫 섹션만 번호 없이 튀면 실패다.
- SEO `SERP Preview`는 실제 검색결과를 설명하되, 사이트 전체 디자인에서는 literal Google blue/Arial/과대 크기를 그대로 쓰지 않는다. editorial dashboard에 맞는 제목 크기·무게·색 균형을 우선한다.
- SEO premium preview는 `serp-*` 정본 클래스만 사용한다. `seo-result-*`, `seo-snippet-*`, `seo-rule-*`, `seo-variant` 같은 final 페이지 전용 클래스는 출력에 남기지 않는다.

## Content Gate

- 제목은 구체적이어야 한다.
- 첫 문단은 독자에게 얻을 가치를 알려야 한다.
- 마지막에는 다음 행동 또는 체크리스트가 있어야 한다.
- 마지막 결론은 “이것은 예제 문서/모드 예시” 설명이 아니라 해당 주제의 실제 판정·권고·다음 행동이어야 한다.
- `/tmp` 임시 스크립트나 일반 루프로 만든 `mini-card`/`col-list` 반복 문서는 실패다. helper script를 쓰더라도 repo 안의 base.html·layout 파일·vt/wg 템플릿을 실제로 읽어 placeholder를 채워야 한다.
- 선택된 layout 파일의 핵심 정보 구조가 본문에 보여야 한다. `layout-*` 클래스만 붙이고 임의 섹션을 나열하면 실패다.
- 8개 이상 섹션 문서에서 `.mini-card`/`.col-list`가 주 구조를 독점하면 실패다. 표·vt-다이어그램·wg-위젯·원문 발췌·체크리스트·의사결정 구조를 섹션 목적에 맞게 섞는다.
- “Generated example”, “전문 예제”, “예제 문서”, “기준 1/2/3”, “placeholder/TBD” 같은 생성 잔여 문구는 실패다.
- 전문가 리포트는 요약 카드 수준을 넘어 운영모델/RACI, 리스크 통제, 로드맵, 검증 증빙까지 포함해야 한다.
- 전문가 리포트의 핵심 표/매트릭스는 특별한 이유가 없으면 5개 안팎 이상의 항목을 포함한다.
- 출처는 본문 흐름을 방해하지 않게 `.source-note`와 source hub로 분리한다.
- 시각 템플릿을 사용했다면 이미지가 장식이 아니라 해당 섹션의 이해·판단·검증을 돕는다.
- skill audit은 개선본 또는 명확한 패치 계획을 포함한다.
- SEO 결과물은 title/meta/tag/final set을 포함한다.
- platform 결과물은 플랫폼별 차이를 실제 발행 관점에서 분리한다.
- platform 변환 전략은 `platform-split`/`platform-route-card`/`platform-output-card` 정본 구조를 사용한다. `platform-transform-*`, `platform-conversion-*`, `platform-branch-*`, `platform-title-*`, `platform-mini-*`는 출력 금지다.

## Skill Execution Fidelity Gate

`validate_output.py OK`는 필요조건이지 충분조건이 아니다. 다음 항목은 산출물 완료 전 수동·보조 자동 검수로 반드시 확인한다.

- **Layout-first**: `assets/layouts/<layout>.html`의 placeholder를 먼저 채우고, 그 다음 필요한 추가 섹션을 붙인다. 처음부터 자유형 `<main>`을 합성하지 않는다.
- **Mode signature**: 각 모드의 핵심 질문이 첫 2~3섹션 안에 보인다. 예: GitHub 분석은 “살아 있는 프로젝트인가/채택해도 되는가”, SEO는 “검색 의도와 SERP 약속”, 교육은 “학습목표→실습→퀴즈→정답”.
- **Reference baseline**: 같은 모드의 `examples/*.html` 또는 사용자가 지정한 정답지보다 헤더·목차·테마바·섹션 카드 밀도·결론 품질이 후퇴하면 실패다.
- **Template diversity**: vt/wg 템플릿은 장식 삽입이 아니라 정보 구조에 맞아야 한다. 같은 카드 그리드를 5회 이상 반복해 정보 구조를 대체하지 않는다.
- **No example voice**: 산출물 내부에서 “예제”, “샘플”, “모드 시연”을 자기 설명으로 쓰지 않는다. 필요한 경우 footer/metadata에만 생성 정보를 둔다.
- **Browser spot check**: 제출 전 가능하면 1280px와 390px 캡처를 확인한다. validator 통과 후에도 시각적으로 기존 검수본보다 낮으면 재작성한다.
- **보조 자동 검사**: 전문/데모/벤치마크 산출물은 `scripts/quality_contract_check.py <output_dir>`를 실행해 placeholder 문구와 반복 구조를 먼저 걸러낸다.

## HTML Gate

- `lang="ko"`
- viewport 존재
- title/meta description 존재
- h1 1개
- h2 순서 정상
- 내부 링크 깨짐 없음
- 외부 링크는 필요 시 검증
- JSON-LD가 있으면 valid JSON이어야 한다.


## v4.3.0 Layout Regression Gate

- 섹션 wrapper(`section.matrix`, `section.serp-preview`, `section.value-grid`, `section.check-grid`, `section.priority-roadmap` 등)에 `display:grid`를 직접 적용하지 않는다.
- h2, `.h2-sub`, 본문 문단, `.tbl`은 카드 grid item으로 쪼개지면 실패다. 실제 카드/매트릭스는 내부 `.card-grid`, `.grid-2`, `.grid-3`, `.matrix:not(section)` wrapper로 분리한다.
- 390px와 1280px에서 `documentElement.scrollWidth <= clientWidth`를 확인한다. 단, `.tbl` 내부 스크롤은 허용한다.

## v4.3.1 Design Polish Regression Gate

- `section>h2:first-child` reset이 빠지면 실패다.
- `.try .summary-card p/li`, `.try .cta-box p/li`, `.try .box p/li`가 흐린 dark-section 색을 상속하면 실패다.
- `.winners:not(section), .tradeoffs:not(section)`에 `display:grid`가 직접 걸려 있으면 실패다.
- `.layout-case .timeline`과 `.timeline-card`가 동시에 left border를 만들면 실패다.
- `.timeline-card`에 2px 이상 굵은 accent left rule을 넣으면 실패다. 순서형 타임라인은 번호와 heading 위계로 충분히 구분한다.
- 순서형 `.timeline-card`는 marker가 카드 모서리에 붙지 않도록 왼쪽 padding을 충분히 둔다.
- 표 안의 `.status-pill`은 `white-space:nowrap`, `justify-content:center`, `text-align:center`로 유지한다. 긴 등급명이 좁은 원형 배지처럼 세로로 쪼개지면 실패다.


## v4.3.2 Blog/SEO Polish Regression Gate

- `.try .tag`/`.try.soft-cta .tag`는 `color:var(--ink)` 계열의 충분한 대비를 가져야 한다.
- `.layout-blog article>section>h2:first-child::before` counter badge가 빠지면 실패다.
- `.layout-seo .serp-title`에 `#1a0dab` 또는 `Arial`을 직접 고정하면 실패다. 검색결과 메타포보다 페이지 전체 시각 균형이 우선이다.
- `<p class="h2-sub">`는 반드시 `</p>`로 닫는다. `</h2>`로 닫힌 legacy markup은 실패다.


## v4.3.3 Responsive Polish Regression Gate

- 검정 `.try`/`.try.soft-cta` 내부 링크는 `--link-on-dark` 또는 동등한 밝은 색을 사용해 4.5:1 이상 대비를 확보한다.
- `.platform-grid`는 내부 wrapper로만 사용한다. `<section class="platform-grid">`는 실패다.
- 모든 `<table>`에는 visible `<caption>`이 있어야 한다.
- 모바일에서 4열 이상 text-heavy table은 `.mobile-card-table` 또는 동등한 카드 변환 패턴을 우선한다.
- case-study timeline은 하나의 긴 카드 안에 모든 사건을 넣지 않는다. 각 사건은 개별 step/card로 구분되어야 한다.
- 자동 overflow 메트릭은 `documentElement.scrollWidth > clientWidth`를 1차 실패로 보고, `.skip:not(:focus)` clipped는 접근성 패턴으로 allowlist 처리한다.


## v4.5.0 Regression Gate (실측 수정 잠금)

실제 쇼케이스에서 발견·수정한 결함을 재발 방지용으로 고정한다. `scripts/validate_output.py`의 R1–R5 자동 게이트와 1:1 대응하므로, 빌드 후 이 항목들을 함께 점검한다.

- **R1 — platform-grid 래퍼 오용 금지.** `class="platform-grid"`인 `<div>`는 `.platform-card`를 **직접** 담는 카드 그리드다. 그 안에 `<h2>`, `.h2-sub`, `.card-grid`를 다시 중첩하면 `:not(section)` 2컬럼 grid 규칙에 걸려 레이아웃이 깨진다. 섹션 래퍼가 필요하면 `<section id="...">`를 쓰고 `platform-grid` 클래스는 제거한다. (자동: `platform_grid_wrapper_misuse`)
- **R2 — wg-03 diff 코드 가시성.** wg-03(Annotated PR) diff 코드는 다크 패널 위 밝은 텍스트여야 한다. 코어 `code{background:#ececea}`(밝은 배경)가 덮으면 텍스트가 안 보인다. `.wg-03-diff code,.wg-03-code{background:none}` 리셋을 유지한다. (자동: `wg03_diff_code_bg_not_reset` — wg-03 **마크업** 사용 시에만 검사)
- **R3 — wg-03 좌우 컬럼 높이 통일.** diff(좌)/리뷰 노트(우)는 `.wg-03-grid{align-items:stretch}`로 같은 높이여야 한다. `start`면 짧은 쪽 아래에 틈이 생겨 뷰가 어긋난다. (자동: `wg03_grid_not_stretch`)
- **R4 — 표 모바일 안전.** components.css `table{min-width:420px}` 때문에 모든 `<table>`은 `.table-scroll`(overflow-x:auto) 래핑 또는 `.mobile-card-table`/`.final-matrix` 카드 변환으로 모바일 가로 넘침을 막아야 한다. (자동: `table_no_mobile_safe_wrapper`)
- **R5 — 와이드 리포트 본문 폭 상한.** `.page-wide`의 분석 폭 레이아웃(expert/compare/seo/platform/landing/case/checklist/reference/audit/skill-audit)은 본문 `p/ul/ol`을 60rem로 넓힌다(`.page-wide.layout-*>section>p{max-width:60rem}`). 기본 46rem만 상속하면 와이드 섹션에서 본문이 1/3만 차서 깨져 보인다. (자동: `wide_layout_prose_cap_missing`)
- **md-excerpt — SKILL.md/마크다운/코드 발췌 표기.** "개선본 발췌 · SKILL.md" 같은 원문/마크다운 발췌는 `.prompt-box`의 `<p>`+`<br>` 텍스트가 아니라 `md-excerpt` 패턴(`<figure class="md-excerpt"><figcaption class="case-label">…</figcaption><pre class="code"><code>…</code></pre></figure>`)으로, `##`·`-`·`name:` 같은 마크다운 문법이 실제 소스처럼 코드 블럭에 보이게 한다. 실제 줄바꿈으로 작성한다. (skill-audit-system.md "발췌·예시 출력 표기 규칙" 참조)


## YouTube / Manual Mode Gates

### youtube_analysis

- `layout-youtube`가 있고 `.layout-youtube>section` 카드 셸 CSS가 인라인되어야 한다.
- `Video Evidence Map` 또는 한국어 동등 섹션이 있어야 한다.
- `Source Limits` 또는 출처 한계/확인 필요 섹션이 있어야 한다.
- `FACT`/`INFERENCE`/`UNKNOWN` 중 최소 2종 이상을 표시한다.
- `observed_at` 또는 “분석 기준 시각”을 표시한다.
- YouTube iframe/embed/autoplay 링크는 금지한다.

### manual_analysis

- `layout-manual`이 있고 `.layout-manual>section` 카드 셸 CSS가 인라인되어야 한다.
- `Source & Version Snapshot`, `Reader Role Router`, `Prerequisites/Safety`, `Troubleshooting`, `Source Limits` 또는 한국어 동등 섹션이 있어야 한다.
- 누락·stale·모순 지적에는 원문 근거/위치가 필요하며, 근거가 없으면 `확인 불가`로 쓴다.
- 입력에 없는 역할 카드는 만들지 않는다.
