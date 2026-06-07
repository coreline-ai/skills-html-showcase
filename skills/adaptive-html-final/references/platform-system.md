# Platform System

플랫폼별로 제목·구조·발행 형식을 발행 관점에서 분리한다. 무 JS 원칙과 일치하도록 동작용 script는 넣지 않는다.

`final_20260604` section 46~47의 검수본을 정본화해, `platform_blog`는 단순 플랫폼별 요약이 아니라 **같은 사실을 플랫폼별 그릇으로 바꾸는 변환 전략**을 보여준다.

## Tistory

- 검색형 제목, 목차, HTML 호환성, 본문 중간 소제목, 하단 태그를 중시한다.
- `<h2>`,`<h3>`,`<p>`,`<ul>`,`<blockquote>` 중심으로 구성. 과도한 script 금지.
- 목차는 수동 앵커 또는 단순 리스트. 문단은 짧게(3~5문장).

## Velog

- Markdown 중심, 코드블럭, 개발자 문체, 짧은 문제/해결 흐름을 중시한다.
- 코드블럭·체크리스트·비교표 선호. 긴 HTML/CSS 삽입은 피한다.
- 태그 5~8개(기술 키워드 중심).

## Naver Blog

- 짧은 문단, 경험형 서술, 검색 친화적 반복 키워드를 사용한다.
- H태그보다 소제목 문장 중심, 정보성 + 경험형 문체.
- 이미지 삽입 위치를 제안한다.

## WordPress/GitHub Pages

- slug, meta, JSON-LD, 내부 링크 설계, canonical, schema 구조를 고려한다.
- HTML 버전 생성에 가장 적합. Article JSON-LD·canonical placeholder 포함 가능.

## Premium transform structure

`platform_blog`의 `{{PLATFORM_STRATEGY}}`와 `{{PLATFORM_CARDS}}`는 가능하면 아래 정본 클래스를 쓴다.

### 1) 변환 전략 카드

- `.platform-split`: 왼쪽 anchor, 오른쪽 플랫폼별 분기 카드 2열.
- `.platform-anchor`: 변환의 핵심 사실/한 문장 약속. 의도적으로 어두운 패널이며, 라이트/화이트/다크 모두에서 CTA처럼 보인다.
- `.platform-route-grid` > `.platform-route-card`: 검색형/개발자형/스토리형/에세이형 분기.
- `.platform-analogy`: 사용자가 이해할 비유 또는 “같은 사실, 다른 그릇” 원칙.

```html
<div class="platform-split">
  <article class="platform-anchor">
    <span class="platform-kicker">Core fact</span>
    <h3>같은 사실은 유지하고, 입구만 플랫폼에 맞춘다</h3>
    <p>검색형은 문제/해결, 개발자형은 코드/근거, 스토리형은 경험/맥락을 먼저 보여준다.</p>
  </article>
  <div>
    <div class="platform-route-grid">
      <article class="platform-route-card is-search"><div><span class="platform-kicker">Search</span><h3>검색형 제목</h3><p>질문과 답을 앞에 둔다.</p></div></article>
      <article class="platform-route-card is-dev"><div><span class="platform-kicker">Dev</span><h3>구현형 제목</h3><p>코드와 재현 조건을 앞에 둔다.</p></div></article>
    </div>
    <article class="platform-analogy"><h3>비유</h3><p>같은 원재료를 도시락/코스요리/간편식으로 포장하는 차이다.</p></article>
  </div>
</div>
```

### 2) 플랫폼별 변환 카드

- `.platform-output-grid` > `.platform-output-card`.
- 카드 상태는 `.is-search`, `.is-dev`, `.is-story`, `.is-essay`로 표현한다.
- 제목 프롬프트는 `.platform-prompt-box`, 태그는 `.platform-tags`, 주의사항은 `.platform-guard`.
- 금지: `platform-transform-*`, `platform-conversion-*`, `platform-branch-*`, `platform-title-*`, `platform-mini-*` 같은 final 페이지 전용 prefix를 출력에 넣지 않는다.

```html
<div class="platform-output-grid">
  <article class="platform-output-card is-search">
    <span class="platform-kicker">Tistory / Naver</span>
    <h3>검색 의도형 카드</h3>
    <p class="platform-prompt-box">제목: 문제 키워드 + 결과 약속 + 대상</p>
    <ul><li>H2는 질문형</li><li>태그는 검색어 중심</li></ul>
    <div class="platform-tags"><span>검색형</span><span>FAQ</span></div>
  </article>
  <article class="platform-output-card is-dev">
    <span class="platform-kicker">Velog / GitHub Pages</span>
    <h3>개발자 검증형 카드</h3>
    <p>재현 조건, 코드, 실패 케이스를 먼저 배치한다.</p>
  </article>
</div>
<article class="platform-guard"><span class="platform-kicker">Guardrail</span><h3>플랫폼만 바꾸고 사실은 바꾸지 않는다</h3><p>확인되지 않은 수치·최신성·성능 주장은 플랫폼별 변환 과정에서도 추가하지 않는다.</p></article>
```
