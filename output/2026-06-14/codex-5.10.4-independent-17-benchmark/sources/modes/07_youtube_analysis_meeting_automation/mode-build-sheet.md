# Mode Build Sheet — youtube_analysis

- mode: `youtube_analysis`
- topic: AI 회의록 자동화 영상의 실행 가능성 분석
- profile: `auto`
- layout: `assets/layouts/youtube-analysis.html`
- primary vt: `timeline`
- wg candidates: wg-11, wg-13, wg-14, wg-16, wg-18
- page: `pages/07_youtube_analysis_meeting_automation.html`

## Sections
1. 영상 결론
2. 챕터별 흐름
3. 핵심 주장
4. 데모와 실제 차이
5. 도구 스택
6. 자동화 파이프라인
7. 댓글의 반론
8. 콘텐츠 갭
9. 실행 체크리스트
10. 다음 실험

## Template mapping

| Section | Pattern |
|---:|---|
| 1 | 영상 결론 → layout scaffold |
| 2 | 챕터별 흐름 → vt-timeline |
| 3 | 핵심 주장 → lede-note/source-note |
| 4 | 데모와 실제 차이 → wg widget |
| 5 | 도구 스택 → editorial rail card |
| 6 | 자동화 파이프라인 → layout scaffold |
| 7 | 댓글의 반론 → vt-timeline |
| 8 | 콘텐츠 갭 → lede-note/source-note |
| 9 | 실행 체크리스트 → wg widget |
| 10 | 다음 실험 → editorial rail card |

## Visual risks

- 390px에서 h2 번호 pill 줄바꿈 금지
- rail 텍스트 좌측 접착 금지
- footer 좌측 붙음 금지
- 비정본 클래스 `template-card-head`/`source-preserve-static` 금지

## Stop condition

validate/quality/completion/render-audit 중 하나라도 실패하면 다음 모드로 넘어가지 않는다.
