# Accessibility Checklist

스킬 루트(`skills/adaptive-html-final`)에서 아래 명령을 실행해 자동 검증한다.
모든 명령은 기대값과 함께 적혀 있으며, 기대값과 다르면 회귀로 간주한다.

## 1. Skip link 존재 (base.html에 정확히 1개)

```bash
grep -c 'class="skip" href="#main"' assets/base.html
# 기대값: 1
```

- [ ] base.html에 `<a class="skip" href="#main">`가 정확히 1개 있다.

## 2. 16개 레이아웃의 `<main id="main">`가 각각 정확히 1개

```bash
for f in assets/layouts/*.html; do echo -n "$f: "; grep -c 'main id="main"' "$f"; done
# 기대값: 16개 파일 모두 1 (16/16)
```

- [ ] `assets/layouts/*.html` 16개 모두 `main id="main"`가 정확히 1개다(skip link 타깃 보장).

## 3. 단일 h1 (각 레이아웃/예시에 h1 1개)

```bash
for f in assets/layouts/*.html examples/*.html; do echo -n "$f: "; grep -c '<h1' "$f"; done
# 기대값: 모든 파일 1
```

- [ ] 각 레이아웃과 각 예시 HTML에 `<h1`이 정확히 1개다.

## 4. 외부 동작 JS 0건 (메타데이터 JSON-LD만 허용)

```bash
# 동작용 <script>가 있는 파일 목록(있으면 출력됨)
grep -rl '<script' assets examples 2>/dev/null
# 위 목록 중 application/ld+json 외 동작 script가 있는 파일만 출력(있으면 위반)
grep -rl '<script' assets examples 2>/dev/null \
  | xargs grep -L 'application/ld+json' 2>/dev/null
# 기대값: 두 명령 모두 출력 0줄 (동작 script 0건)
```

- [ ] `<script type="application/ld+json">` 메타데이터를 제외하고 동작용 `<script>`나 외부 JS가 0건이다.

## 5. Focus 가시성 (theme.css에 `:focus-visible` 존재)

```bash
grep -c ':focus-visible' assets/theme.css
# 기대값: 1 이상
```

- [ ] theme.css에 `:focus-visible` 키보드 포커스 outline 규칙이 있다.
- [ ] `a / button / summary / [tabindex]`에 가시적 포커스 outline이 적용된다.

## 6. 모션 민감 사용자 대응 (theme.css)

```bash
grep -c 'prefers-reduced-motion' assets/theme.css
# 기대값: 1 이상
```

- [ ] `@media (prefers-reduced-motion: reduce)`로 `scroll-behavior`를 끄는 규칙이 있다.

## 7. 색 대비 (AA 4.5:1)

수동/도구 확인 항목(자동 grep 불가, 변경 시 토큰값으로 추적).

- [ ] `.term .label`, `.danger .label` 계열 라벨 전경색이 배경 대비 4.5:1 이상이다.
- [ ] `.meta`, `.tag` 회색 전경색이 배경 대비 4.5:1 이상이다.
- [ ] 본문 텍스트(`--ink`)가 배경(`--bg` 오프화이트)에서 4.5:1 이상이다.


## 8. 시각 템플릿 접근성

시각 템플릿을 사용한 산출물에 적용한다.

```bash
# 산출물 HTML에서 visual figure가 있으면 alt/figcaption도 있어야 한다.
grep -n 'class="visual-figure"\|class="figure-wide"' output.html
grep -n '<img [^>]*alt=' output.html
grep -n '<figcaption' output.html
```

- [ ] `figure.visual-figure` 또는 `.figure-wide` 안의 이미지에 구체적인 `alt`가 있다.
- [ ] 같은 figure 안에 `figcaption`이 있다.
- [ ] SVG 자체에도 `<title>`과 `<desc>`가 있다.

## v4 디자인 리뷰 반영 게이트

```bash
# 포커스 링이 브랜드 빨강이 아닌 전용 --focus(파랑)를 쓴다 (장식색 분리)
grep -c ':focus-visible{outline:3px solid var(--focus)' output.html   # == 1

# h2 장식 번호 칩이 스크린리더에서 숨겨진다
grep -o '<span class="num"[^>]*>' output.html | grep -c 'aria-hidden="true"'   # == 전체 num 칩 수

# 외부/동작 JS 0 유지 (읽기 진행 바는 CSS animation-timeline, <script> 아님)
grep -rl '<script' output.html | xargs grep -L 'application/ld+json'   # 빈 출력
```

- [ ] 포커스 링이 `--focus`(파랑) + 흰 헤일로다(브랜드 빨강과 분리).
- [ ] 장식 번호 칩(`.num`/`.no`)에 `aria-hidden="true"`가 있다.
- [ ] 모바일(≤760px)에서 목차 링크 등 인터랙티브 타깃이 ≥44px다.
- [ ] 읽기 진행 바(`.reading-progress`)는 CSS 기반(무 JS)이고 `prefers-reduced-motion`에서 숨겨진다.


## 신규 모드 접근성

- [ ] youtube_analysis: iframe/player 없이 텍스트 근거와 타임스탬프 링크를 제공한다.
- [ ] manual_analysis: 역할 라우터와 절차 카드가 heading/list/table 의미를 유지한다.
