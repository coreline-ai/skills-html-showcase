# Editorial Pattern System

현행 17개 모드와 별개로 새 모드를 늘리지 않고, **필요한 섹션에 선택 삽입하는 작은 본문 구조 패턴 8종**이다. 큰 SVG 시스템이 아니라 본문 흐름에 붙는 카드·타임라인·콜아웃·마크다운 발췌·접근성 체크리스트 중심이며, 외부/동작 JS 0, 스킬 디자인 토큰 + body icon(`bi-`)을 쓴다.

- **자산**: `assets/editorial-patterns.css`(패턴 CSS) + `assets/editorial-pattern-templates/01..08.html`(삽입 골격) + body icon(`assets/body-icons.css`)
- **프로파일 무관**: widget/diagram/auto 어디서나 사용(본문 구조 보조). 조건부 인라인(`{{EDITORIAL_PATTERNS_CSS}}` 슬롯).

## 8종 패턴

| pattern | 이름 | 아이콘 | 추천 모드 |
|---|---|---|---|
| `chronology` | 증류 연대기 (timeline) | `timeline` | expert_html · case_study_html · skill_audit · education_html · github_analysis |
| `source-preserve` | 원문 보존 카드 | `source` | reference_html · article_html · blog_writer · skill_audit · github_analysis |
| `core-insight` | 핵심 아이디어 callout | `idea` | article_html · blog_writer · expert_html · landing_brief_html · github_analysis |
| `connection` | 연결 분석 카드 | `connection` | reference_html · skill_audit · article_html · comparison_html · github_analysis |
| `before-after` | Before / After 윤문 | `edit` | platform_blog · blog_writer · skill_audit · comparison_html |
| `md-excerpt` | SKILL.md/마크다운/코드 원문 발췌 | `source` | skill_audit · reference_html · article_html · github_analysis |
| `impact-grid` | 콘텐츠 전환 impact grid | `impact` | platform_blog · landing_brief_html · seo_dashboard · checklist_playbook |
| `accessibility-checklist` | 접근성 30분 점검 + 실패 모드 + 릴리스 체크 | `shield` | skill_audit · checklist_playbook · expert_html · reference_html |

## 삽입 규칙

- 해당 섹션 목적에 맞는 패턴만 **선택 삽입**한다. 한 페이지에 과용 금지(특히 `core-insight`는 **페이지당 1개**가 가장 강하다).
- 골격은 `assets/editorial-pattern-templates/NN-*.html`를 복사해 **콘텐츠만 교체**(클래스·구조 유지). `editorial-patterns.css`를 인라인한다.
- 아이콘이 들어가는 패턴(impact-grid 등)은 `aria-hidden` body icon을 쓴다(장식, 의미는 텍스트로).
- 무 JS: `source-preserve`는 `<details>`(네이티브 접기)만 사용. 동작 JS 금지.

## 적용 갤러리

`adaptive-html-final-editorial-pattern-demo-v1` 공개 데모 (초기 6 패턴 도입 데모; 현재는 `md-excerpt`·`accessibility-checklist`를 포함해 8종).

## md-excerpt (SKILL.md/코드 발췌)

SKILL.md·마크다운·코드 원문 발췌는 `.prompt-box`(텍스트 인용)가 아니라 **코드 블럭으로 표기**해 실제 마크다운 소스처럼 보이게 한다:

```html
<figure class="md-excerpt">
  <figcaption class="case-label">개선본 발췌 · SKILL.md</figcaption>
  <pre class="code"><code>name: ...\n## TRIGGER\n- ...</code></pre>
</figure>
```

`pre.code`(다크 코드 블럭)에 마크다운 소스를 그대로 넣고, `<br>`/문단이 아니라 실제 줄바꿈으로 작성한다. `##`·`-`·`1.`·`name:` 등 마크다운 문법이 소스로 드러나야 한다.

## accessibility-checklist (접근성 30분 점검)

배포 전 접근성 점검을 본문에 삽입하는 패턴. `final_20260604`의 `access-*`/`edge-*` 페이지 어휘를 **`a11y-` 정본 네임스페이스**로 개명해 흡수했다(베어 `.good` 충돌·`!important`·`--report-sans` 제거).

- **3블록 구성**: `.a11y-check`(점검 그리드 `.a11y-grid` > `.a11y-card`) → `.a11y-subhead`(번호 매긴 소제목) + 실패 모드 표 + `.a11y-notes`(trap/solution/case) → `.a11y-release`(다크 릴리스 체크리스트).
- **색 외 단서 의무**: 상태는 `.a11y-pass`/`.a11y-fail` **텍스트 칩(PASS/FAIL)**으로 — 색만으로 구분하지 않는다(WCAG 1.4.1).
- **표**: `<caption>` 필수, `.table-scroll`로 감싸 모바일 가로 스크롤(품질 게이트 R4).
- **다크 패널**: `.a11y-release`는 `var(--dark)` 배경 + 의도적 반전 텍스트로, `components.css`의 `.try` 다크 CTA와 동일한 규약(라이트/다크 테마 양쪽에서 의도적으로 어둡게 유지).
- 골격: `assets/editorial-pattern-templates/08-accessibility-checklist.html` 복사 후 콘텐츠만 교체.

## callout·변형 헬퍼 (opt-in, 패턴 수 미증가)

`final_20260604`에서 흡수한 작은 변형들. 모두 **opt-in 수식자/헬퍼**라 8종 패턴 수에 포함하지 않으며, 베어 콜아웃을 덮어쓰지 않는다.

- **`.lede-note`** — Goal/도입 강조 카드(좌측 accent rail). 페이지의 `pattern-hero-note`를 정본 callout으로 개명. `.label`은 공유 uppercase 규약(`.08em`/weight 800/accent-2)을 따른다. 마크업: `<div class="lede-note"><span class="label">Goal</span><p>…</p></div>`.
- **`.source-preserve-static`** — `source-preserve`의 **접기 없는 정적 변형**(`<details>` 대신 `<div class="source-preserve source-preserve-static">` + `.source-preserve-title`(div) + `.source-body`, `role="group"`/`aria-labelledby`). 무 JS.
- **`.core-insight--neutral`** — `core-insight`의 그라데이션 없는 중립 변형. **베어 `.core-insight`를 덮어쓰지 않는다**(opt-in). blockquote는 `var(--sans)`.
- **`.core-insight--plain-text`** — 사고 원인·SLO 판단처럼 핵심 문장이지만 hero quote까지는 아닌 경우 쓰는 일반 본문 크기 변형. **베어 `.core-insight`를 덮어쓰지 않는다**(opt-in). blockquote는 `var(--fs-base)`/sans/normal letter-spacing으로 낮춘다.
- **before/after 강조** — `.ba-emphasis-line`(강조 문장) + `.ba-bullet`(장식 마커, `aria-hidden="true"`). `.ba-col.after .ba-bullet`는 accent, 기본은 `--ink-mute`(토큰화, warm 리터럴 미사용).
- **`.toc-map`(템플릿 목차 chip-nav)** — 섹션 목차를 **번호 pill이 한 줄에서 wrap 되는 chip-row**로 보여주는 정본 목차 카드(`final_20260604`의 `imported-toc-*` 데모를 정본 이름으로 승격). 리스트형 `.toc`(components.css)와 별개의 opt-in 컴포넌트로, 항목이 6개 이상이거나 가로로 훑게 하고 싶을 때 쓴다. 번호 배지는 `--accent-soft`/`--accent-2` 토큰으로 8테마 자동 적응. 마크업:
  ```html
  <section class="toc-map" aria-labelledby="toc-map-title">
    <div class="label" id="toc-map-title">템플릿 목차</div>
    <p>이 페이지에서 확인할 영역을 섹션 순서대로 묶었습니다.</p>
    <nav class="toc-pills" aria-label="섹션 목차">
      <a class="toc-pill" href="#p1"><b>1</b>첫 섹션</a>
      <a class="toc-pill" href="#p2"><b>2</b>둘째 섹션</a>
    </nav>
  </section>
  ```
  주의: 데모용 `imported-toc-*` 어휘는 `bespoke_namespace_class` denylist에 그대로 남으므로 정식 출력에는 **`toc-map`/`toc-pills`/`toc-pill`** 정본 클래스만 쓴다. `github_analysis`/`github_feature_usage`/`youtube_analysis`/`manual_analysis`의 상단 목차는 이 계약이 필수이며, 구형 `.toc` 리스트 목차로 폴백하지 않는다.
- **`.col-list`(평면 리스트 자동 다단)** — 짧은 항목(파일명·태그·키워드 등)이 **6개 이상**인 평면 `ul`/`ol`은 세로 1열로 적층하지 말고 `class="col-list"`를 붙여 **다단 그리드(auto-fill, 폭을 꽉 채워 ≈3개+/행)** 로 렌더한다. 가로 공백 낭비와 "빈약한 긴 목록"을 막는 **밀도 판단의 기본값**이다. 마크업: `<ul class="col-list"><li><code>a.md</code></li>…</ul>`. 기존 산출물 호환을 위해 `<div class="col-list"><ul>…</ul></div>` 래퍼형도 정본 지원하며, 이 경우 설명 문장이 붙은 항목을 고려해 행 간격과 줄간격을 더 넉넉하게 둔다.
  - **자동 판단 규칙(작성자가 매번 손보지 않아도 되게):** 항목이 모두 한 줄(짧은 토큰)이고 개수가 6개 이상이면 `col-list`를 **기본 적용**한다. 항목에 설명 문장이 붙는 리스트(긴 본문)는 일반 리스트를 유지한다. github_analysis의 `references 투어`, 태그 목록, 파일/모듈 인덱스가 대표 사례다.
- **`.text-bullet-view`(텍스트 전용 뷰 bullet)** — 체크리스트/요약 카드처럼 **텍스트만 있는 뷰가 카드 안에서 밋밋하게 보일 때** `final_20260604` section 7의 작은 써클 bullet 리듬을 정본으로 적용한다. `text-bullet-view`는 레이아웃만 담당하고, 마커는 기존 `.ba-bullet`을 재사용한다. 마크업: `<div class="check-item text-bullet-view"><span class="ba-bullet" aria-hidden="true"></span><span>확인할 문장</span></div>`.
  - **자동 판단 규칙:** 아이콘/번호/상태칩 없이 문장만 들어 있는 카드형 항목이 3개 이상 반복되면 `text-bullet-view`를 기본 적용한다. 이미 `cf-check`, `body-icon`, 번호 pill, 상태 badge가 있는 뷰에는 중복 장식이므로 적용하지 않는다.
- **rail utilities (`rail-cycle`, `rail-red/blue/green/gold`, `multi-rail`)** — 텍스트만 있는 mini-card/summary-card/card-block/box가 4개 이상 반복될 때 좌측 rail을 단색 `accent`로만 반복하지 않는다. 부모에 `rail-cycle`을 붙이면 자식 카드 rail이 `--vt-red → --vt-blue → --vt-green → --vt-gold`로 순환한다. 개별 의미가 분명하면 `rail-red`, `rail-blue`, `rail-green`, `rail-gold`를 직접 붙인다. 하단 takeaway/판정 카드처럼 한 개의 넓은 텍스트 뷰는 `multi-rail`로 4색 세로 rail을 적용한다. 마크업: `<div class="card-grid rail-cycle"><article class="mini-card">…</article></div>` / `<aside class="source-note multi-rail">…</aside>`.
  - **자동 판단 규칙:** 타임라인/날짜/단계/정책 프레임처럼 동일 위계 카드가 4개 이상이고 왼쪽 rail이 있으면 `rail-cycle`이 기본값이다. 이미 `risk-matrix`, `quality-gate`, `incident-summary`처럼 의미별 색이 내장된 vt 템플릿에는 중복 적용하지 않는다.

## 데모 하네스 (pattern-shell) — 생성 출력 아님

`final_20260604` 쇼케이스는 패턴들을 한 페이지에 묶어 보여주려고 `.pattern-shell`/`.pattern-head`/`.pattern-nav`/`.pattern-meta` 섹션 스캐폴딩을 쓴다. 이는 **데모/쇼케이스 하네스**일 뿐 작성자가 본문에 삽입하는 콘텐츠 패턴이 아니므로 **스킬 콘텐츠 CSS(`editorial-patterns.css`)에 넣지 않는다**.

- 실제 생성물에서는 **패턴을 직접** 본문 섹션에 삽입한다(쇼케이스 셸로 감싸지 않는다).
- `pattern-shell`·`pattern-nav`·`pattern-head`·`pattern-meta`는 `validate_output.py`의 `bespoke_namespace_class` denylist에 포함되어 **정식 출력에 등장하면 게이트 실패**한다(쇼케이스 전용 어휘이기 때문).
- 인-스킬 카탈로그/데모는 `galleries/`(body-icons·soft-shapes)와 각 `*-templates/`의 골격 파일로 충분하다.
