# Mode Selection

우선순위:

1. skill_audit
2. platform_blog
3. seo_dashboard
4. education_html
5. github_analysis
6. expert_html
7. article_html
8. blog_writer
9. beginner_html
10. reference_html
11. comparison_html
12. case_study_html
13. landing_brief_html
14. checklist_playbook

명시적 요청이 있으면 명시적 요청이 우선한다. “블로그 HTML”처럼 복합 요청이면 `blog_writer`를 선택하고 HTML 렌더링을 추가한다. “스킬 분석/통합/감사”는 `skill_audit`을 우선한다. GitHub 저장소 URL 또는 `owner/repo`를 주고 저장소 이해·분석·채택 판단을 요청하면 `github_analysis`를 선택한다.

## Quick trigger map

- 쉽게/초보자/비유 → beginner_html
- 전문가/리포트/리스크/아키텍처 → expert_html
- GitHub 저장소 URL/깃허브 URL/owner/repo/README·Issues·Releases·License 분석 → github_analysis
- 아티클/공개 글/기사 → article_html
- 교육/강의/실습/퀴즈 → education_html
- 블로그/경험담/내 생각 → blog_writer
- SEO/검색/제목/메타/태그 → seo_dashboard
- 티스토리/벨로그/네이버/워드프레스 → platform_blog
- SKILL.md/.skill/스킬 감사/스킬 통합 → skill_audit
- 매뉴얼/API/reference → reference_html
- 비교/장단점/선택 기준 → comparison_html
- 사례/회고/프로젝트 기록 → case_study_html
- 랜딩/소개/요약 페이지 → landing_brief_html
- 체크리스트/운영 절차/플레이북 → checklist_playbook

## github_analysis 선택 기준

`github_analysis`는 “저장소를 읽고 내가 무엇을 해야 하는가?”에 답하는 모드다. 단순 README 재요약이 아니라 다음 질문을 목차화한다.

1. 이 프로젝트는 무엇을 해결하는가?
2. 지금 바로 실행하거나 도입할 수 있는가?
3. 어떤 파일/디렉터리부터 보면 되는가?
4. 최근에도 유지보수되고 있는가?
5. 라이선스·보안·공급망상 확인해야 할 리스크는 무엇인가?
6. 내 다음 행동은 사용, 검토, 보류, 대체 탐색 중 무엇인가?

### 충돌 처리

- GitHub Pages “배포 방법”이 주제이면 `article_html` 또는 `education_html`을 우선한다.
- 특정 저장소 URL이 있고 저장소 품질·구조·활동·리스크 분석이 목적이면 `github_analysis`를 우선한다.
- 저장소 분석 결과를 다시 전문가 리포트로 확장해 달라는 명시가 있으면 사용자 지정 모드(`expert_html`)가 우선이다.
