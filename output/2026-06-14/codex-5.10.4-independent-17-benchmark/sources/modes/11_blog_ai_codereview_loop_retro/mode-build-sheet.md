# Mode Build Sheet — blog_writer

- mode: `blog_writer`
- topic: 4일간 AI 코드리뷰 루프를 돌린 회고
- profile: `auto`
- layout: `assets/layouts/personal-blog-essay.html`
- primary vt: `timeline`
- wg candidates: wg-17
- page: `pages/11_blog_ai_codereview_loop_retro.html`

## Sections
1. 첫날의 착각
2. 둘째 날의 반복
3. 셋째 날의 증거
4. 넷째 날의 전환
5. 도구가 잘한 일
6. 사람이 봐야 한 일
7. 레이아웃 회귀
8. 검증의 한계
9. 다음 루틴
10. 개인 결론

## Template mapping

| Section | Pattern |
|---:|---|
| 1 | 첫날의 착각 → layout scaffold |
| 2 | 둘째 날의 반복 → vt-timeline |
| 3 | 셋째 날의 증거 → lede-note/source-note |
| 4 | 넷째 날의 전환 → wg widget |
| 5 | 도구가 잘한 일 → editorial rail card |
| 6 | 사람이 봐야 한 일 → layout scaffold |
| 7 | 레이아웃 회귀 → vt-timeline |
| 8 | 검증의 한계 → lede-note/source-note |
| 9 | 다음 루틴 → wg widget |
| 10 | 개인 결론 → editorial rail card |

## Visual risks

- 390px에서 h2 번호 pill 줄바꿈 금지
- rail 텍스트 좌측 접착 금지
- footer 좌측 붙음 금지
- 비정본 클래스 `template-card-head`/`source-preserve-static` 금지

## Stop condition

validate/quality/completion/render-audit 중 하나라도 실패하면 다음 모드로 넘어가지 않는다.
