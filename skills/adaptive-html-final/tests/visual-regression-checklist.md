# Visual Regression Checklist

주관 판단을 줄이기 위해 정량 기준으로 검증한다(임계치는 theme.css 토큰값 기준).

## 자동 검증 (먼저 실행)

390px/1440px 재캡쳐 이전에 정적 게이트를 먼저 통과시킨다. 산출물 디렉터리 단위로 실행한다.

```
python3 scripts/validate_output.py <산출물 디렉터리> --skill-dir <스킬 루트>
```

- `OK`가 아니면(`FAILED` + `ISSUE ...`) 캡쳐/릴리즈를 중단하고 회귀를 먼저 고친다.
- `--skill-dir`를 주면 CSS asset hash/snapshot, 인라인 CSS hash marker, source manifest version 동기화까지 확인한다.
- 이 스크립트는 dark CTA 링크 대비(`--link-on-dark`), platform section grid, table caption 누락, blog section counter, SEO SERP literal style 등 아래 v4.3.0~v4.3.3 절의 회귀를 정적으로 막는다. 통과 후 Playwright 390px/1440px 캡쳐로 시각 확인한다.

- [ ] 배경색이 따뜻한 오프화이트다 — `--bg` = `#f5f5f0`(hex 동등).
- [ ] h2 앞 번호가 빨간 원형이다 — `.no`/`.num`이 `var(--accent)` 배경, `border-radius:50%`, 약 34x34px 원형 유지.
- [ ] 본문 폭이 토큰값을 따른다 — `.page` ≤ `--max-reading`(780px), `.page-wide` ≤ `--max-wide`(1020px).
- [ ] h1이 과도하게 크지 않다 — `font-size:clamp(31px, 4vw, 42px)` 상한 42px 유지(computed ≤ 42px).
- [ ] 박스 시스템이 유지된다 — `.term`/`.analogy`/`.danger`/`.good`/`.try` 카드 보더·배경 토큰 유지.
- [ ] 와이드 SaaS 랜딩페이지처럼 변질되지 않았다 — hero 그라디언트/큰 그림자 남발 없음, 본문 폭 토큰 초과 없음.
- [ ] 모바일(390px)에서 그리드가 1컬럼으로 내려온다 — `*-grid` 계열 `grid-template-columns:1fr` 미디어쿼리 적용.

- [ ] 시각 템플릿 사용 시 `.visual-figure` 이미지가 컨테이너 폭을 넘지 않는다 — `img{width:100%;height:auto}` 적용.
- [ ] SVG 원본 크기는 8000×6000 이상이고 내부 도형의 최대 bottom/right가 viewBox 안쪽에 있다.
- [ ] 모바일(390px)에서 `figcaption`이 잘리지 않고, 이미지 주변 패딩이 과도하지 않다.
- [ ] quality-gate 하단 강조 패널은 납작한 배너가 아니며, 주요 카드 bottom ≤ 5200px, footer와 겹치지 않는다.


## v4.3.0 Layout Regression Gate

- 섹션 wrapper(`section.matrix`, `section.serp-preview`, `section.value-grid`, `section.check-grid`, `section.priority-roadmap` 등)에 `display:grid`를 직접 적용하지 않는다.
- h2, `.h2-sub`, 본문 문단, `.tbl`은 카드 grid item으로 쪼개지면 실패다. 실제 카드/매트릭스는 내부 `.card-grid`, `.grid-2`, `.grid-3`, `.matrix:not(section)` wrapper로 분리한다.
- 390px와 1280px에서 `documentElement.scrollWidth <= clientWidth`를 확인한다. 단, `.tbl` 내부 스크롤은 허용한다.

## v4.3.1 Design Polish Regression Gate

- [ ] `section>h2:first-child` 또는 동등한 첫 heading margin reset이 있다.
- [ ] `.try` 내부 밝은 카드(`.box/.summary-card/.cta-box/.card-block/.mini-card`)는 카드 내부 p/li/strong 색상을 light-surface 토큰으로 되돌린다.
- [ ] `.winners:not(section)`, `.tradeoffs:not(section)`에 `display:grid`를 직접 걸지 않는다.
- [ ] case-study timeline은 section wrapper와 내부 timeline card가 동시에 left border를 만들지 않는다.

## v4.3.2 Blog/SEO Polish Regression Gate

05 블로그 CTA, 06 SEO SERP Preview 캡쳐에서 확인된 회귀를 정량 기준으로 재확인한다(`validate_output.py`가 정적으로 막는다).

- [ ] 검정 `.try`/`.try.soft-cta` 내부 `.tag` pill이 거의 흰 배경 + `var(--ink)` 굵은 텍스트로 보인다 — `로컬LLM`, `Ollama` 등 태그 대비 4.5:1 이상(`missing_try_tag_contrast_reset` 게이트).
- [ ] `blog_writer` 본문 섹션 h2 앞에 CSS counter 번호 badge가 보인다 — 다른 모드와 번호 시각 일관성 유지(`missing_blog_section_counter` 게이트).
- [ ] `layout-seo .serp-title`이 Google 원문 파란색/Arial/20px가 아니라 `var(--ink)`/sans/17~18px/800 weight로 보인다(`seo_serp_title_literal_google_style` 게이트).
- [ ] `.h2-sub` 부제가 `</h2>`로 닫히는 HTML 오류 없이 렌더된다(`h2_sub_closed_as_h2` 게이트).

## v4.3.3 Responsive Polish Regression Gate

13개 모드 전수 캡쳐 감사(02/05/07/08/10/11/12/13 페이지)에서 확인된 dark CTA 링크 대비, platform grid 구조, 표 caption, 모바일 표 밀도, case timeline 회귀를 정량 기준으로 재확인한다.

- [ ] 검정 CTA(`.try`, `.try.soft-cta`) 내부 링크가 `--link-on-dark` 밝은 색으로 보인다 — dark 배경에서 대비 4.5:1 이상(`missing_try_dark_link_contrast_reset` 게이트).
- [ ] `platform-grid`가 `<section>`에 직접 걸리지 않아 h2/문단이 grid item으로 쪼개지지 않는다 — grid는 `.layout-platform .platform-grid:not(section)` 내부 wrapper에만(`platform_grid_used_as_section`, `platform_grid_selector_allows_section_grid` 게이트).
- [ ] 모든 `<table>`에 `<caption>`이 보인다(`table_missing_caption` 게이트).
- [ ] 390px 모바일에서 복잡한 표가 `.mobile-card-table`(`data-label` 기반 행 카드)로 잘리지 않고 보인다.
- [ ] expert executive summary 4카드가 2×2로 안정 배치되고, case-study timeline이 단일 대형 카드가 아니라 개별 step card로 보인다.


## 신규 모드 시각 회귀

- [ ] youtube_analysis: 390px에서 evidence/comment/opportunity grid가 1열로 접힌다.
- [ ] manual_analysis: role/task/troubleshooting grid가 1열로 접히고 긴 절차 표는 table-scroll 또는 mobile-card-table을 쓴다.
- [ ] 8테마에서 두 신규 모드의 카드 배경·텍스트 대비가 유지된다.
