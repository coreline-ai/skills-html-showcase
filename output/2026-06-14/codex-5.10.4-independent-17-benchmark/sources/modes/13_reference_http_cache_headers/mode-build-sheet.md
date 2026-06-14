# Mode Build Sheet — reference_html

- mode: `reference_html`
- topic: HTTP 캐시 헤더 실무 레퍼런스
- profile: `auto`
- layout: `assets/layouts/reference-manual.html`
- primary vt: `file-tour`
- wg candidates: wg-04, wg-05, wg-06, wg-14, wg-19, wg-20
- page: `pages/13_reference_http_cache_headers.html`

## Sections
1. 빠른 참조
2. Cache-Control
3. ETag
4. Last-Modified
5. stale-while-revalidate
6. 브라우저와 CDN
7. 금지 조합
8. 디버깅 명령
9. 상황별 처방
10. 체크리스트

## Template mapping

| Section | Pattern |
|---:|---|
| 1 | 빠른 참조 → layout scaffold |
| 2 | Cache-Control → vt-file-tour |
| 3 | ETag → lede-note/source-note |
| 4 | Last-Modified → wg widget |
| 5 | stale-while-revalidate → editorial rail card |
| 6 | 브라우저와 CDN → layout scaffold |
| 7 | 금지 조합 → vt-file-tour |
| 8 | 디버깅 명령 → lede-note/source-note |
| 9 | 상황별 처방 → wg widget |
| 10 | 체크리스트 → editorial rail card |

## Visual risks

- 390px에서 h2 번호 pill 줄바꿈 금지
- rail 텍스트 좌측 접착 금지
- footer 좌측 붙음 금지
- 비정본 클래스 `template-card-head`/`source-preserve-static` 금지

## Stop condition

validate/quality/completion/render-audit 중 하나라도 실패하면 다음 모드로 넘어가지 않는다.
