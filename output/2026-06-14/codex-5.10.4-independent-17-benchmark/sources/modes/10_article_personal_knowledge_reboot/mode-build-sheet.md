# Mode Build Sheet — article_html

- mode: `article_html`
- topic: AI 시대 개인 지식관리의 현실적 재설계
- profile: `auto`
- layout: `assets/layouts/magazine-article.html`
- primary vt: `decision-tree`
- wg candidates: wg-02, wg-04, wg-07, wg-09, wg-10, wg-13, wg-14
- page: `pages/10_article_personal_knowledge_reboot.html`

## Sections
1. 문제 제기
2. 낡은 분류 체계
3. 새로운 읽기 단위
4. 링크보다 질문
5. 요약의 위험
6. 검색과 회상
7. 작은 자동화
8. 개인 워크플로
9. 실패 패턴
10. 결론

## Template mapping

| Section | Pattern |
|---:|---|
| 1 | 문제 제기 → layout scaffold |
| 2 | 낡은 분류 체계 → vt-decision-tree |
| 3 | 새로운 읽기 단위 → lede-note/source-note |
| 4 | 링크보다 질문 → wg widget |
| 5 | 요약의 위험 → editorial rail card |
| 6 | 검색과 회상 → layout scaffold |
| 7 | 작은 자동화 → vt-decision-tree |
| 8 | 개인 워크플로 → lede-note/source-note |
| 9 | 실패 패턴 → wg widget |
| 10 | 결론 → editorial rail card |

## Visual risks

- 390px에서 h2 번호 pill 줄바꿈 금지
- rail 텍스트 좌측 접착 금지
- footer 좌측 붙음 금지
- 비정본 클래스 `template-card-head`/`source-preserve-static` 금지

## Stop condition

validate/quality/completion/render-audit 중 하나라도 실패하면 다음 모드로 넘어가지 않는다.
