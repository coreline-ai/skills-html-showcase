# Platform System

플랫폼별로 제목·구조·발행 형식을 발행 관점에서 분리한다. 무 JS 원칙과 일치하도록 동작용 script는 넣지 않는다.

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
