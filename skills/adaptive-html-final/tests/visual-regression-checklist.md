# Visual Regression Checklist

주관 판단을 줄이기 위해 정량 기준으로 검증한다(임계치는 theme.css 토큰값 기준).

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
