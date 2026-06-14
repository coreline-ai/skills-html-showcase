# Adaptive HTML Final Theme Token Strategy

- 작성일: 2026-06-05
- 대상 저장소: `skills-html-showcase`
- 대상 스킬: `skills/adaptive-html-final`
- 관련 출력 샘플:
  - `output/2026-06-04/final_20260604/index.html`
  - `output/2026-06-04/final_20260604/index-beginner-width.html`
- 목적: 현재 HTML 쇼케이스의 배경/표면 색상 혼재를 정리하고, 동일 HTML 구조를 여러 테마로 안정적으로 확장할 수 있는 토큰 기반 디자인 시스템 전략을 정의한다.

---

## 1. Executive Summary

현재 `adaptive-html-final` 쇼케이스는 구조, 섹션 다양성, 위젯 수, visual-template 수는 충분히 풍부하다. 그러나 여러 세대의 템플릿, `vt-*` visual HTML, `wg-*` 위젯, editorial pattern, platform 변환 카드, soft-shape/soft-workflow 섹션이 각각 자기 배경색 규칙을 유지하면서 전체 배경 체계가 중구난방으로 보인다.

전문가 관점에서 지금 필요한 작업은 **새로운 색을 추가하는 것**이 아니라 **색상 역할을 재정의하고 토큰 계층을 단순화하는 것**이다. 특히 배경은 다음 5단계 안에서 대부분 해결해야 한다.

| 계층 | 권장 토큰 | 역할 |
|---|---|---|
| 1 | `--surface-page` | 문서 전체 바탕 |
| 2 | `--surface-section` | 큰 섹션 카드/패널 |
| 3 | `--surface-view` | 섹션 내부 카드/셀/뷰 |
| 4 | `--surface-muted` | 헤더 셀, 보조 그룹, 낮은 위계 영역 |
| 5 | `--surface-inset` | 코드, 미리보기, 프레임, 내부 캔버스 |

현재 사용 중인 `--bg`, `--card`, `--copy-surface`, `--copy-surface-2`, `--copy-surface-3`, `--vt-soft`, `--pill-bg`, `--term-bg`, `--danger-bg`, `--good-bg` 등은 즉시 삭제할 대상이 아니라, 위 역할 토큰으로 매핑해 점진적으로 흡수해야 한다.

핵심 전략은 다음과 같다.

1. **Primitive 색상과 Role 색상을 분리한다.**
2. **컴포넌트는 색상 값을 직접 알지 않고 role token만 사용한다.**
3. **semantic 색상은 카드 전체 배경보다 border/left rail/label 중심으로 제한한다.**
4. **Light/White/Dark의 계층 구조를 동일하게 유지한다.**
5. **향후 테마는 HTML 구조 변경이 아니라 theme preset 교체로 확장한다.**

---

## 2. Current State Diagnosis

### 2.1 현재 강점

현재 쇼케이스는 테마 시스템으로 발전할 수 있는 좋은 기반을 이미 갖고 있다.

| 강점 | 설명 |
|---|---|
| 구조 다양성 | editorial pattern, vt-template, wg-widget, platform card, SEO card, QA gate 등 실사용 패턴이 풍부하다. |
| CSS-only 원칙 | 외부/동작 JS 없이 theme switcher와 상태 표현을 CSS로 처리하는 방향이 좋다. |
| 토큰 기반의 흔적 | `--bg`, `--card`, `--line`, `--accent`, `--good-bg`, `--danger-bg` 등 이미 토큰화된 색이 많다. |
| 검증 가능성 | `validate_output.py`, 무 JS grep, Playwright screenshot/overflow 검증을 자동화하기 쉽다. |
| 쇼케이스 역할 | `index.html`과 `index-beginner-width.html`이 시각 회귀 비교용 샘플로 적합하다. |

### 2.2 현재 문제

현재 배경이 정돈되지 않아 보이는 주된 원인은 다음이다.

| 문제 | 구체 증상 | 영향 |
|---|---|---|
| 배경 단계 과다 | `#fff`, `#fffdfb`, `#f9f7f1`, `#f0eee6`, `#fbfbfb`, `rgba(...)`가 섹션마다 다르게 사용됨 | 같은 레벨의 카드가 다른 위계처럼 보임 |
| 컴포넌트별 색상 독립 | `vt-raci`, `vt-risk`, `seo-snippet`, `variant-card`, `wf-board`가 각자 색을 가짐 | 테마 전환 시 보정 CSS가 계속 늘어남 |
| semantic 색상 과다 사용 | danger/good/gold가 카드 전체 배경에 자주 사용됨 | 정보 강조가 시끄럽고 배경 톤이 깨짐 |
| legacy override 잔존 | 예전 `#theme-toggle`, hardcoded dark/light 스타일이 일부 셀/코드에 새어 나옴 | 특정 텍스트가 안 보이거나 배경이 갑자기 어두워짐 |
| output-level patch 누적 | 산출물 HTML에 보정 CSS가 많이 쌓임 | 원인 추적이 어려워지고 스킬 자산과 산출물이 분리됨 |

### 2.3 가장 큰 리스크

현재 방식으로 계속 보정하면 다음 문제가 커진다.

1. 섹션이 늘어날수록 `body:has(...) .specific-section ...` override가 폭증한다.
2. Light/White/Dark마다 예외 규칙이 생겨 테마 추가 비용이 커진다.
3. `vt-*`, `wg-*`, editorial pattern이 각기 다른 디자인 언어처럼 보인다.
4. 검증은 통과하더라도 전체 디자인 품질은 일관되지 않게 된다.

---

## 3. Target Design Principle

### 3.1 색상은 “예쁜 색”이 아니라 “정보 위계”다

테마 시스템에서 색상은 장식이 아니라 정보 구조다. 따라서 색상은 다음 질문에 답해야 한다.

| 질문 | 토큰 역할 |
|---|---|
| 이 요소가 페이지 바탕인가? | `--surface-page` |
| 독립된 섹션인가? | `--surface-section` |
| 섹션 내부의 정보 카드인가? | `--surface-view` |
| 낮은 위계의 보조 영역인가? | `--surface-muted` |
| 내부 프레임/코드/미리보기인가? | `--surface-inset` |
| 위험/성공/주의 의미인가? | `--semantic-*` |
| 클릭/브랜드 행동인가? | `--accent-*` |

### 3.2 배경색 수를 줄이고, 밝기 차이로 위계를 만든다

좋은 테마는 많은 색을 쓰지 않는다. 같은 hue family 안에서 밝기와 채도만 조금씩 달라야 한다.

권장 원칙:

- 전체 배경 hue는 1개 계열로 제한한다.
- 섹션과 카드 배경은 hue를 바꾸지 말고 lightness만 조절한다.
- semantic 색상은 배경이 아니라 라인, 라벨, 아이콘, 작은 배지에 우선 사용한다.
- 카드 전체 tint는 정말 필요한 경우에만 4~8% 수준으로 사용한다.

### 3.3 컴포넌트는 토큰을 소비하고, 테마는 토큰을 공급한다

나쁜 구조:

```css
.vt-risk-cell { background:#fffdfb; }
.seo-result-card { background:#fffdfb; }
.variant-card.is-disabled { background:#f3f0e8; }
```

좋은 구조:

```css
.vt-risk-cell,
.seo-result-card,
.variant-card {
  background:var(--surface-view);
  border-color:var(--border-subtle);
}

.vt-risk-head,
.vt-raci .h,
.vt-swimlane .role {
  background:var(--surface-muted);
}
```

테마는 이렇게 바뀐다.

```css
[data-theme="warm"] {
  --surface-page:#f5f5f0;
  --surface-section:#ffffff;
  --surface-view:#ffffff;
  --surface-muted:#f9f7f1;
  --surface-inset:#fffdfb;
}
```

---

## 4. Proposed Token Architecture

### 4.1 3계층 토큰 모델

테마 시스템은 다음 3계층으로 분리한다.

```txt
Primitive Token → Semantic Token → Component Role Token
```

| 계층 | 예시 | 설명 |
|---|---|---|
| Primitive | `--color-warm-000`, `--color-red-600` | 팔레트 원천 색상. 컴포넌트에서 직접 사용 금지. |
| Semantic | `--semantic-danger-bg`, `--semantic-success-border` | 의미 색상. 상태/위험/성공 등에서 사용. |
| Role | `--surface-section`, `--text-primary`, `--border-subtle` | 실제 컴포넌트가 사용하는 계약. |

### 4.2 Primitive palette 예시

Warm Editorial 기준 primitive는 다음처럼 단순하게 시작한다.

```css
:root {
  --warm-000:#ffffff;
  --warm-025:#fffdfb;
  --warm-050:#f9f7f1;
  --warm-075:#f5f5f0;
  --warm-100:#ece8df;
  --warm-200:#d8d8d0;
  --warm-300:#c9bdad;

  --ink-900:#1a1a1a;
  --ink-700:#4a4a4a;
  --ink-500:#6a6a6a;

  --red-600:#e63946;
  --red-700:#b72d38;
  --red-050:#fce4e6;

  --green-600:#1f6f4e;
  --green-050:#eef7f1;

  --gold-600:#c98a2e;
  --gold-050:#fffaf2;
}
```

### 4.3 Role token 표준안

컴포넌트는 아래 role token만 사용하도록 점진적으로 전환한다.

| Role Token | 현재 매핑 후보 | 용도 |
|---|---|---|
| `--surface-page` | `--bg` | 전체 body 배경 |
| `--surface-section` | `--copy-surface`, `--card` | 큰 섹션/패널 |
| `--surface-view` | `--copy-surface`, `--card` | 카드/셀/리스트 아이템 |
| `--surface-muted` | `--copy-surface-3`, `--vt-soft` | 헤더 셀, 역할 셀, 보조 영역 |
| `--surface-inset` | `--copy-surface-2`, `--code` 일부 | 코드/미리보기/내부 프레임 |
| `--surface-hover` | `--copy-hover`, `--pill-bg-hover` | hover/target highlight |
| `--border-subtle` | `--copy-line`, `--line` | 기본 선 |
| `--border-strong` | `--copy-line-strong` | 구획 강조선 |
| `--text-primary` | `--ink` | 제목/중요 텍스트 |
| `--text-secondary` | `--ink-soft` | 본문/설명 |
| `--text-muted` | `--ink-mute`, `--chip-ink` | 메타/보조 |
| `--accent` | `--accent` | 브랜드/주 CTA |
| `--accent-strong` | `--accent-2` | 강조 텍스트/라벨 |

### 4.4 Semantic token 표준안

semantic 색상은 전체 배경을 뒤덮지 않고, 가급적 left rail, border, label에 사용한다.

| Semantic Token | 용도 |
|---|---|
| `--danger-surface` | 위험 카드의 아주 약한 tint, 기본값은 대부분 사용하지 않음 |
| `--danger-border` | left rail / border |
| `--danger-text` | danger label |
| `--success-surface` | 성공 카드의 약한 tint |
| `--success-border` | 성공 left rail / border |
| `--success-text` | 성공 label |
| `--warning-surface` | 주의/검토 tint |
| `--warning-border` | gold left rail / border |
| `--warning-text` | gold label |
| `--info-surface` | 정보/analogy tint |
| `--info-border` | blue/gray border |
| `--info-text` | info label |

권장 카드 패턴:

```css
.card.is-danger,
.card.is-success,
.card.is-warning {
  background:var(--surface-view);
  border-color:var(--border-subtle);
  border-left-width:4px;
}

.card.is-danger { border-left-color:var(--danger-border); }
.card.is-success { border-left-color:var(--success-border); }
.card.is-warning { border-left-color:var(--warning-border); }
```

---

## 5. Theme Preset Strategy

### 5.1 기본 제공 테마 3종

현재 UI에 이미 Light / White / Dark가 있으므로 이것을 공식 기본 테마로 삼는다.

| 테마 | 목적 | 시각 톤 |
|---|---|---|
| Light | 기본 editorial 문서 | warm neutral, 부드러운 종이 질감 |
| White | SaaS 문서/레퍼런스 | pure white, gray border, 깔끔한 UI 문서 |
| Dark | 야간/개발자/프레젠테이션 | slate/ink 기반, 낮은 채도 accent |

### 5.2 추가 확장 후보

토큰 체계가 안정화되면 다음 테마를 확장할 수 있다.

| 테마 | 적합한 모드 | 설명 |
|---|---|---|
| Warm Editorial | article, blog, beginner | 현재 방향. 따뜻하고 읽기 좋은 종이 느낌. |
| Clean White | reference, seo, platform | 거의 흰색 기반. 대시보드/문서 시스템에 적합. |
| Slate Technical | expert, skill_audit, checklist | 기술 리포트/운영 문서용 청회색 계열. |
| Sand Learning | education, beginner | 학습자료용. 부드러운 베이지, 낮은 대비의 보조색. |
| Blue Gray Report | expert, comparison | 전문 리포트용. 차분한 blue-gray와 red accent. |
| Mono Print | reference, checklist | 인쇄/배포용. 색 최소화, 선과 타이포 중심. |

### 5.3 테마 프리셋 구조

최종적으로는 `theme-dark.css` 하나에 모든 것을 넣기보다 다음 구조를 권장한다.

```txt
assets/
  theme.css                  # 기본 primitive + role token
  theme-presets.css          # light/white/dark/warm/slate 등 preset
  theme-compat.css           # legacy token alias
  components.css             # role token만 소비
  visual-html.css            # role token만 소비
  widgets.css                # role token만 소비
```

현재 AGENTS 기준에서는 자산 순서가 고정되어 있으므로 초기에는 파일을 늘리기보다 `theme-dark.css` 또는 기존 theme 슬롯 내부에 preset block을 두고, 안정화 후 manifest/validator를 갱신하는 방식이 안전하다.

---

## 6. Component Token Contract

### 6.1 공통 표면 계약

모든 섹션/카드/뷰는 다음 계약을 우선 따른다.

```css
.pattern-shell,
.source-note,
.imported-toc-card,
.final-vt-section > .vt-adapt-demo {
  background:var(--surface-section);
  border-color:var(--border-subtle);
}

.vt-adapt-card,
.vt-risk-cell,
.vt-raci div,
.vt-swimlane div,
.seo-result-card,
.variant-card,
.widget-soft-card {
  background:var(--surface-view);
  border-color:var(--border-subtle);
}

.vt-risk-head,
.vt-raci .h,
.vt-swimlane .h,
.vt-swimlane .role,
.vt-file-head {
  background:var(--surface-muted);
  color:var(--text-primary);
}
```

### 6.2 위젯/비주얼 템플릿 네임스페이스별 전략

| 네임스페이스 | 현재 문제 | 전략 |
|---|---|---|
| `vt-*` | 각 템플릿이 자체 `--vt-soft`, `--vt-wash`를 사용 | `--vt-*`를 role token alias로 매핑 |
| `wg-*` | 위젯마다 surface, preview, node 색이 다름 | widget component root에서 role token 사용 |
| editorial patterns | 기존 문서형 카드와 callout 색이 혼재 | callout은 semantic rail 중심으로 전환 |
| platform sections | conversion/guard/branch card 색이 강함 | 기본 view 배경 + semantic rail로 정리 |
| soft workflow | hardcoded warm gradient가 강함 | 테마별 별도 illustration preset 또는 quiet mode 제공 |
| SVG/shape | 이미지 캔버스 배경이 theme와 충돌 | SVG 자체 색상과 figure mat token 분리 |

### 6.3 코드/프리뷰/표 계약

코드, 표, SERP, module map은 다크/라이트에서 가장 쉽게 깨지는 영역이다.

| 요소 | 권장 토큰 |
|---|---|
| code block | `--surface-code`, `--text-code`, `--border-code` |
| inline code | `--surface-inline-code`, `--text-inline-code` |
| table header | `--surface-muted`, `--text-primary` |
| table cell | `--surface-view`, `--text-secondary` |
| preview frame | `--surface-inset`, `--border-subtle` |
| SVG graph text | `--text-primary`, `--text-secondary` as `fill` |

---

## 7. Migration Strategy

### 7.1 원칙

마이그레이션은 산출물 HTML에 override를 계속 쌓는 방식이 아니라, 스킬 자산을 정리하는 방향이어야 한다.

우선순위:

1. `output/2026-06-04/final_20260604/*.html`에서 발견한 문제를 증거로 기록한다.
2. 해당 문제의 원인이 되는 자산 CSS/템플릿을 찾는다.
3. `assets/theme.css`, `assets/visual-html.css`, `assets/widgets.css`, `assets/editorial-patterns.css`에 role token 기반으로 반영한다.
4. output-level override는 임시 패치로만 두고, 최종적으로 자산 레벨로 흡수한다.

### 7.2 Phase 0 — Inventory

목표: 현재 쓰이는 배경색과 hardcoded 색을 전부 파악한다.

작업:

- `assets/*.css`에서 `background`, `background-color`, `box-shadow`, `rgba`, `#fff`, `#f...` 검색
- `visual-html-templates/*.html`, `widget-templates/*.html`에서 inline style 확인
- `output/2026-06-04/final_20260604/index*.html`의 임시 보정 블록 목록화
- 컬러 토큰 표를 기준으로 실제 렌더링 색상 수집

산출물:

```txt
reports/theme-color-inventory.json
reports/theme-hardcoded-backgrounds.md
```

### 7.3 Phase 1 — Token Alias Layer

목표: 기존 토큰을 깨지 않고 새 role token을 추가한다.

예:

```css
:root {
  --surface-page:var(--bg);
  --surface-section:var(--card);
  --surface-view:var(--card);
  --surface-muted:#f9f7f1;
  --surface-inset:#fffdfb;
  --surface-hover:#fff7f5;

  --border-subtle:var(--line);
  --border-strong:#c9bdad;

  --text-primary:var(--ink);
  --text-secondary:var(--ink-soft);
  --text-muted:var(--ink-mute);
}
```

이 단계에서는 컴포넌트를 대규모 수정하지 않는다. 기존 토큰과 새 토큰을 연결하는 안전한 compatibility layer를 만든다.

### 7.4 Phase 2 — Surface Unification

목표: 같은 위계의 배경을 같은 토큰으로 통일한다.

우선 통일 대상:

| 우선순위 | 대상 | 변경 방향 |
|---:|---|---|
| 1 | `pattern-shell`, `source-note`, `imported-toc-card` | `--surface-section` |
| 2 | `vt-adapt-card`, `vt-risk-cell`, `vt-check-item`, `vt-raci div`, `vt-swimlane div` | `--surface-view` |
| 3 | `vt-risk-head`, `vt-raci .h`, `vt-swimlane .role`, `vt-file-head` | `--surface-muted` |
| 4 | `seo-snippet-preview`, `module-map`, `static-flow`, `variant-card` | `--surface-view` 또는 `--surface-inset` |
| 5 | hardcoded dark panels | theme preset token으로 대체 |

### 7.5 Phase 3 — Semantic Rail Refactor

목표: semantic 색을 카드 전체 배경에서 left rail/border/label로 제한한다.

변경 예:

```css
.vt-adapt-card.good,
.vt-adapt-card.gold,
.vt-adapt-card.accent {
  background:var(--surface-view);
  border-color:var(--border-subtle);
  border-left-width:4px;
}

.vt-adapt-card.good { border-left-color:var(--success-border); }
.vt-adapt-card.gold { border-left-color:var(--warning-border); }
.vt-adapt-card.accent { border-left-color:var(--danger-border); }
```

### 7.6 Phase 4 — Theme Presets

목표: Light/White/Dark를 공식 preset으로 정리하고, 이후 Warm/Sand/Slate를 확장한다.

추천 계약:

```html
<body data-theme="warm">
```

단, 현재 스킬은 JS-free와 radio `:checked` 방식을 쓰고 있으므로 당장은 다음 계약을 유지한다.

```html
<input type="radio" name="ahf-theme" id="ahf-light" checked>
<input type="radio" name="ahf-theme" id="ahf-white">
<input type="radio" name="ahf-theme" id="ahf-dark">
```

그리고 CSS에서 preset을 공급한다.

```css
body:has(#ahf-light:checked) { ... }
body:has(#ahf-white:checked) { ... }
body:has(#ahf-dark:checked) { ... }
```

### 7.7 Phase 5 — Asset-level Integration

목표: output-level 보정을 스킬 자산으로 흡수한다.

주요 대상 파일:

| 파일 | 작업 |
|---|---|
| `assets/theme.css` | primitive/role token 추가 |
| `assets/theme-dark.css` | 3-theme preset 정리, legacy toggle 제거 |
| `assets/visual-html.css` | `vt-*` hardcoded surface 제거 |
| `assets/widgets.css` | widget surface 통일 |
| `assets/editorial-patterns.css` | callout/section surface 통일 |
| `assets/shape-visuals.css` | figure mat와 SVG background 분리 |
| `assets/workflow-visuals.css` | soft workflow quiet mode 도입 |
| `scripts/validate_output.py` | theme contract 검증 추가 |

---

## 8. Regression-Zero Policy

사용자가 요구한 “회귀 0” 기준을 색상 시스템에도 적용한다.

### 8.1 변경 가능 항목

- 같은 위계의 배경색 통일
- 텍스트 대비 개선
- light/white/dark theme token 정리
- shadow 제거/완화
- hardcoded 색을 token으로 치환
- semantic card를 rail 중심으로 변경

### 8.2 변경 금지 항목

- 섹션 순서 변경
- 13 mode routing 변경
- `vt-` / `wg-` 네임스페이스 변경
- 동작 JS 추가
- HTML 의미 구조 손상
- 검증기 core hash 대상 CSS를 임의 byte 수정하는 작업
- 원본 wide layout을 beginner width로 강제하는 작업

### 8.3 검증 기준

| Gate | 기준 |
|---|---|
| No behavioral JS | JSON-LD 외 script 0 |
| Theme switch | Light/White/Dark 모두 선택 가능 |
| Width preservation | `index.html`은 wide, `index-beginner-width.html`은 beginner width 유지 |
| Mobile overflow | 390px overflow 0 |
| Text contrast | 주요 텍스트와 버튼이 보일 것 |
| Surface consistency | 같은 역할의 카드가 같은 배경을 쓸 것 |
| Dark preservation | 다크에서 그래프/SVG/표 텍스트가 보일 것 |
| Snapshot QA | 핵심 섹션 스크린샷 비교 |

---

## 9. Recommended QA Matrix

### 9.1 샘플 페이지

| 페이지 | 목적 |
|---|---|
| `output/2026-06-04/final_20260604/index.html` | wide showcase, 원래 가로폭 보존 검증 |
| `output/2026-06-04/final_20260604/index-beginner-width.html` | 780px beginner reading width 검증 |
| `output/adaptive-html-final-13-topics-*/pages/01-local-rag-personal-knowledge-vault.html` | white/light reference 비교 |

### 9.2 핵심 섹션 체크리스트

| 섹션 | 확인 항목 |
|---|---|
| Header | theme bar, color table, title wrapping, wide width 유지 |
| Template Goal | left rail, background, text color |
| 8 hero-map | view 카드 배경 통일 |
| 10 risk-matrix | header/cell 배경 계층 |
| 11 checklist-flow | PASS pill, row background |
| 14 raci | header/role cell muted background |
| 17 weekly-status | KPI 카드 4개 가독성 |
| 20 process-swimlane | RACI와 같은 header/role 색상 |
| 25 feature-flag | toggle visibility, dark icon contrast |
| 26 soft-workflow-map | light에서 너무 튀지 않는지 |
| 41 SERP Preview | preview/result/rule card surface 통일 |
| 42 Module Map | dark graph text visibility |
| 44 Component Variants | primary/disabled button text visibility |
| 45 Static Click Flow | circle number visibility |
| 46~47 platform cards | dark leftover background 제거 |
| Color Token Table | 색상 셀, 값, 긴 토큰명 overflow 없음 |

### 9.3 자동 검증 명령 후보

```bash
# no behavioral JS
grep -rniE '<script(?![^>]*type=["'"']application/ld\+json)' output/2026-06-04/final_20260604/*.html || echo "NO behavioral script (OK)"

# forbidden primitives
grep -rniE 'draggable=|contenteditable=' output/2026-06-04/final_20260604/*.html && echo "FORBIDDEN primitive found" || echo "NO forbidden primitive (OK)"

# full validator, asset-level 생성물에 적용
python3 <repo-root>/skills/adaptive-html-final/scripts/validate_output.py \
  output/2026-06-04/final_20260604 \
  --skill-dir <repo-root>/skills/adaptive-html-final
```

---

## 10. Implementation Blueprint

### 10.1 새 토큰 도입 순서

1. `theme.css`에 role token alias 추가
2. `theme-dark.css`에 Light/White/Dark preset 정리
3. 기존 token과 새 token을 1:1 매핑
4. `visual-html.css`에서 가장 많이 보이는 surface부터 치환
5. `widgets.css` 치환
6. editorial/platform/shape/workflow CSS 치환
7. 출력 HTML에서 임시 보정 CSS 제거
8. validator에 theme contract 검사 추가

### 10.2 컴포넌트 변경 우선순위

| 순서 | 이유 | 대상 |
|---:|---|---|
| 1 | 페이지 전체 인상 결정 | `pattern-shell`, `source-note`, `imported-toc-card` |
| 2 | 반복 빈도 높음 | `vt-adapt-card`, `vt-risk-cell`, `vt-check-item` |
| 3 | 표/매트릭스 계열 | `vt-raci`, `vt-swimlane`, `vt-risk-grid` |
| 4 | 이질감 큼 | `seo-snippet`, `module-map`, `component-variants` |
| 5 | hardcoded 많음 | `soft-workflow-map`, SVG/shape figure |
| 6 | semantic 색상 | good/gold/accent/danger variants |

### 10.3 최종 CSS 레이어 권장안

CSS cascade layer를 쓸 수 있다면 다음 구조가 이상적이다.

```css
@layer tokens, base, components, templates, widgets, themes, utilities;

@layer tokens {
  :root { ... }
}

@layer themes {
  body:has(#ahf-light:checked) { ... }
  body:has(#ahf-white:checked) { ... }
  body:has(#ahf-dark:checked) { ... }
}

@layer components {
  .pattern-shell { background:var(--surface-section); }
}
```

단, 현재 검증기와 core hash 정책이 있으므로 도입 전 validator 영향 검토가 필요하다.

---

## 11. Theme Quality Rubric

테마 품질은 다음 10점 척도로 평가한다.

| 항목 | 0점 | 10점 |
|---|---|---|
| Surface hierarchy | 카드 단계가 구분 안 됨 | page/section/view/muted/inset이 명확함 |
| Color harmony | 섹션마다 다른 색감 | 같은 계열의 밝기 차이로 통일됨 |
| Semantic restraint | 빨강/초록/노랑 배경 과다 | rail/label 중심으로 절제됨 |
| Text contrast | 일부 텍스트 안 보임 | 모든 테마에서 본문/버튼/표 텍스트 명확 |
| Component portability | 컴포넌트별 override 필요 | role token만 바꾸면 작동 |
| Dark consistency | 일부 카드만 light/dark 잔존 | 모든 view가 같은 dark 계층 |
| White theme cleanliness | 회색/베이지가 섞여 지저분 | white + cool gray 체계로 깔끔 |
| Light editorial tone | 종이 느낌 없음 | warm neutral로 부드럽고 읽기 좋음 |
| Visual template integration | vt/wg가 따로 놂 | 문서 본문과 같은 리듬 |
| Regression safety | 수정 때마다 깨짐 | Playwright/validator로 안정 확인 |

목표 점수:

- Phase 1 후: 6/10
- Phase 2 후: 7.5/10
- Phase 3 후: 8.5/10
- Phase 5 후: 9/10 이상

---

## 12. Key Decisions

1. **배경 토큰은 최대 5단계로 제한한다.**
2. **semantic 색상은 기본적으로 카드 전체 배경이 아니라 left rail/border/label에 사용한다.**
3. **`index.html`의 wide width와 `index-beginner-width.html`의 beginner width는 서로 다른 검증 축으로 보존한다.**
4. **현재 output-level 패치는 임시 검증 샘플이며, 장기적으로는 `skills/adaptive-html-final/assets/*`에 흡수한다.**
5. **Light/White/Dark는 단순 색상 변경이 아니라 같은 surface hierarchy를 공유해야 한다.**
6. **테마 추가는 HTML 구조 변경 없이 token preset 추가로만 가능해야 한다.**

---

## 13. Next Action Plan

### 바로 다음 작업

- [ ] `assets/theme.css`에 role token alias 추가
- [ ] `assets/theme-dark.css`에서 radio theme contract와 preset token 정리
- [ ] `visual-html.css`의 `vt-*` surface를 role token으로 1차 치환
- [ ] `widgets.css`의 widget card/background를 role token으로 1차 치환
- [ ] `output/2026-06-04/final_20260604/index*.html`에서 찾은 임시 보정 목록을 asset-level task로 분해

### 그 다음 작업

- [ ] `reports/theme-color-inventory.json` 생성 스크립트 작성
- [ ] Playwright screenshot QA 스크립트 작성
- [ ] validator에 다음 항목 추가 검토
  - legacy `#theme-toggle` 금지
  - `name="ahf-theme"` 계약 확인
  - hardcoded background 허용 목록 검사
  - mobile 390px overflow 확인

### 완료 기준

- [ ] `index.html` wide layout 유지
- [ ] `index-beginner-width.html` beginner width 유지
- [ ] Light/White/Dark 모두 surface hierarchy 동일
- [ ] 주요 섹션에서 배경 계층 혼란 제거
- [ ] output-level emergency override 감소
- [ ] 검증기 `OK`

---

## 14. Closing Opinion

현재 페이지는 “색이 많아서 나쁜 상태”가 아니라, **색상 역할이 아직 정리되지 않은 상태**다. 구조와 패턴은 이미 충분히 풍부하므로, 색상 템플릿만 안정화하면 같은 HTML을 다양한 목적의 문서 테마로 확장할 수 있다.

가장 중요한 방향은 다음 한 문장으로 요약된다.

> 컴포넌트는 색을 직접 고르지 말고, 역할 토큰만 소비하게 만든다. 테마는 그 역할 토큰에 서로 다른 색상 계열을 공급한다.

이 원칙만 지키면 `adaptive-html-final`은 단일 HTML 생성 스킬을 넘어, **테마 가능한 editorial HTML design system**으로 발전할 수 있다.
