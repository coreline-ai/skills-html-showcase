# Blog SEO System

제목은 검색형, 클릭형, 전문가형, 초보자형으로 나눈다.

메타 설명은 120~160자 내외를 목표로 한다. 확인되지 않은 수치와 최신 주장은 넣지 않는다.

SERP preview는 title, slug, meta description을 함께 보여준다.

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
