# Blog SEO System

제목은 검색형, 클릭형, 전문가형, 초보자형으로 나눈다.

메타 설명은 120~160자 내외를 목표로 한다. 확인되지 않은 수치와 최신 주장은 넣지 않는다.

SERP preview는 title, slug, meta description을 함께 보여준다. `final_20260604` section 41의 검수본을 정본화해, 단순 텍스트 상자가 아니라 **검색 결과 약속 카드**로 구성한다.

## Required SEO blocks

- primary keyword
- secondary keyword cluster
- title candidates
- meta description candidates
- SERP preview
- final SEO set
- FAQ 후보
- internal link 후보

## Tone

검색 유입 독자에게 즉시 가치를 전달하되, 낚시성 제목과 과장된 최신성 표현은 피한다.

## SEO 세부 규칙

- Primary keyword는 제목 앞쪽 또는 첫 문단 안에 자연스럽게 넣는다(억지 반복 금지).
- H2에는 검색 의도를 반영한다.
- FAQ는 실제 사용자가 물을 법한 질문으로 만든다.
- meta description은 클릭 이유를 포함한다. 태그는 5~10개가 적당하다.

## SERP premium card 구조

`seo_dashboard`의 `{{SERP_PREVIEW}}`에는 가능하면 아래 구조를 쓴다. Google UI를 그대로 복제하지 않고, editorial dashboard 톤에 맞춘다.

- 바깥: `.serp-shell` 2열. 왼쪽은 미리보기, 오른쪽은 약속/규칙 카드.
- 미리보기: `.serp-box` 안에 `.serp-dots`, `.serp-result`, `.serp-url`, `.serp-title`, `.serp-desc`, `.serp-checks`.
- 규칙: `.serp-rule-grid` > `.serp-rule`; 중요한 규칙은 `.serp-rule.is-wide`.
- 변형: 제목/메타 대안은 `.serp-variant-strip` > `.serp-variant`.
- 금지: `seo-result-*`, `seo-snippet-*`, `seo-rule-*`, `seo-variant` 같은 final 페이지 전용 prefix를 출력에 넣지 않는다. 모두 `serp-*` 정본 클래스만 사용한다.

예시 골격:

```html
<div class="serp-shell">
  <div class="serp-box">
    <div class="serp-dots">검색 결과 미리보기</div>
    <article class="serp-result">
      <p class="serp-url">example.com/guide</p>
      <h3 class="serp-title">검색 의도와 약속이 보이는 제목</h3>
      <p class="serp-desc">120~160자 안에서 누가, 무엇을, 왜 클릭해야 하는지 설명한다.</p>
    </article>
    <div class="serp-checks"><span class="ok">의도 일치</span><span>과장 없음</span></div>
  </div>
  <div class="serp-rule-grid">
    <article class="serp-rule is-wide"><span class="serp-rule-kicker">Promise</span><h3>제목과 본문 첫 화면의 약속을 일치</h3><p>클릭 후 바로 확인되는 가치를 제목에 쓴다.</p></article>
    <article class="serp-rule"><span class="serp-rule-kicker">Avoid</span><h3>최신/무료/완벽 같은 단정 금지</h3><p>확인 가능한 범위만 말한다.</p></article>
    <article class="serp-rule"><span class="serp-rule-kicker">Fit</span><h3>독자 수준을 제목에 반영</h3><p>초보자/전문가/비교/체크리스트 의도를 구분한다.</p></article>
  </div>
</div>
```

## Blog Metadata Schema (`schemas/blog-meta.schema.json` 준수)

아래 11필드 예시는 `schemas/blog-meta.schema.json`이 정의하는 필드와 동일하다(스키마와 1:1로 정합 유지).

```json
{
  "title_recommended": "추천 제목",
  "title_variants": { "search": [], "click": [], "expert": [], "beginner": [] },
  "slug": "kebab-case-slug",
  "meta_description": "120~160자 설명",
  "target_reader": "대상 독자",
  "search_intent": "informational/commercial/tutorial/opinion/news",
  "keywords_primary": [],
  "keywords_secondary": [],
  "tags": [],
  "estimated_reading_time": "N분",
  "platform_notes": []
}
```

## Blog Quality Score (100점)

| 항목 | 점수 |
|---|---:|
| 제목/검색 의도 | 15 |
| 도입부 흡입력 | 15 |
| 구조/목차 | 15 |
| 설명/예시 균형 | 15 |
| 신뢰성/검증 | 15 |
| SEO 메타 | 10 |
| 결론/CTA | 10 |
| 플랫폼 적합성 | 5 |
