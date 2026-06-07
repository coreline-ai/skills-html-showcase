# 01 beginner passkey 가로 너비 미충족 원인 분석

## 결론

`01_beginner_passkey_login.html`의 가로 너비 미충족은 최신 스킬 assets 누락이 아니라, 현재 최신 assets 안에 남아 있는 폭 제한 정책 때문입니다.

- `widgets.css`, `visual-html.css`, `layouts.css`, `theme-dark.css`는 01 HTML에 모두 인라인되어 있음
- `examples/sources/assets/widgets.css`, `visual-html.css`도 현재 skill assets와 byte 일치
- `validate_output.py`, `quality_contract_check.py`, `completion_check.py`는 모두 통과 상태

## 실제 측정

1280px에서 `main.page-wide.layout-beginner`의 직접 섹션 폭은 약 `1020px`입니다. 그러나 내부 prose와 일부 위젯은 아래처럼 제한됩니다.

| 대상 | 실제 폭 | 원인 |
|---|---:|---|
| section card | 1020px | `.page-wide`가 `--max-wide` 기준으로 넓게 잡힘 |
| 일반 `p`, `ol`, `ul`, `.h2-sub` | 736px | `theme.css`의 `.page-wide>section>p/ul/ol { max-width:46rem }` |
| `wg-10-sheet` | 620px | `widgets.css`의 `.wg-10-sheet { max-width:620px; margin:0 auto }` |

## 원인 CSS

### 1. 넓은 섹션 안의 본문 읽기폭 제한

`skills/adaptive-html-final/assets/theme.css`

```css
.page-wide>section>p,
.page-wide>section>ul,
.page-wide>section>ol,
.page-wide>article>p,
.page-wide>article>ul,
.page-wide>article>ol,
.page-wide>p {
  max-width: 46rem;
}
```

이 규칙은 prose readability를 위한 정책입니다. 즉 카드/섹션은 넓고, 설명 문단은 좁게 유지합니다. 그래서 1280px에서 섹션은 1020px인데 본문은 736px로 보입니다.

### 2. beginner 모드가 60rem 예외 목록에서 빠져 있음

같은 `theme.css`에는 일부 모드만 section prose를 `60rem`까지 넓히는 예외가 있습니다.

```css
.page-wide.layout-github>section>p,
.page-wide.layout-youtube>section>p,
.page-wide.layout-manual>section>p,
.page-wide.layout-expert>section>p,
...
.page-wide.layout-reference>section>p,
.page-wide.layout-audit>section>p {
  max-width: 60rem;
}
```

하지만 `layout-beginner`는 이 예외 목록에 없습니다. 따라서 beginner는 기본 `46rem` 정책을 탑니다.

### 3. `wg-10` 위젯 자체가 620px 고정 성격

`skills/adaptive-html-final/assets/widgets.css`

```css
.wg-10-sheet {
  font-family: var(--sans);
  color: var(--ink);
  max-width: 620px;
  margin: 0 auto;
}
```

`01_beginner_passkey_login.html`의 `모드 정본 템플릿 적용 확인` 섹션에는 추천 위젯으로 `wg-10`이 들어가는데, 이 위젯은 assets 원본에서 620px로 제한되어 있습니다. 그래서 섹션 폭 1020px 안에서 가운데 620px만 사용합니다.

## 판정

| 질문 | 답 |
|---|---|
| 최신 스킬 assets가 01 HTML에 없는가? | 아니오. 최신 assets는 인라인되어 있음 |
| `widgets.css` / `visual-html.css` 스냅샷이 오래됐는가? | 현재는 최신과 byte 일치 |
| 검증 실패인가? | 아니오. 검증은 통과 |
| 왜 가로폭이 안 차 보이는가? | `theme.css`의 prose max-width 46rem + `widgets.css`의 `wg-10` max-width 620px 때문 |
| 스킬에 추가로 필요한가? | 예. “넓은 카드 안의 핵심 위젯은 full width 가능” 정책이 assets에 아직 없음 |

## 스킬 반영 필요 사항

최소 패치 방향은 둘 중 하나입니다.

### A안 — beginner prose만 더 넓힘

`theme.css`의 60rem 예외 목록에 `layout-beginner`를 추가합니다.

```css
.page-wide.layout-beginner>section>p,
.page-wide.layout-beginner>section>ul,
.page-wide.layout-beginner>section>ol {
  max-width: 60rem;
}
```

효과: 일반 본문과 `.h2-sub`가 736px에서 약 960px까지 넓어집니다.

### B안 — mode-template-contract 내부 위젯은 full width

`widgets.css` 또는 `layouts.css`에 아래 같은 계약을 추가합니다.

```css
.mode-template-contract > .wg-10-sheet {
  width: 100%;
  max-width: 100%;
}
```

효과: `모드 정본 템플릿 적용 확인` 섹션의 `wg-10`이 섹션 폭을 채웁니다.

### 권장

- prose는 읽기폭 제한을 유지할 가치가 있으므로 무조건 full-width로 풀지 않는 것이 좋습니다.
- 다만 `mode-template-contract`는 “스킬 템플릿 적용 증명 섹션”이므로, 여기에 들어가는 추천 위젯은 섹션 폭을 더 적극적으로 쓰는 편이 맞습니다.
- 따라서 **B안 우선**, 필요 시 `layout-beginner`에만 60rem 예외를 추가하는 순서가 안전합니다.
