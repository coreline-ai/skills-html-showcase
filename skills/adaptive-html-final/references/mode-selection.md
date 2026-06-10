# Mode Selection

우선순위:

1. skill_audit
2. platform_blog
3. seo_dashboard
4. education_html
5. github_analysis
6. github_feature_usage
7. youtube_analysis
8. manual_analysis
9. expert_html
10. article_html
11. blog_writer
12. beginner_html
13. reference_html
14. comparison_html
15. case_study_html
16. landing_brief_html
17. checklist_playbook

명시적 요청이 있으면 명시적 요청이 우선한다. “블로그 HTML”처럼 복합 요청이면 `blog_writer`를 선택하고 HTML 렌더링을 추가한다. “스킬 분석/통합/감사”는 `skill_audit`을 우선한다. GitHub 저장소 URL 또는 `owner/repo`를 주고 저장소 이해·분석·채택 판단을 요청하면 `github_analysis`를 선택한다. 단, 같은 GitHub URL이라도 목적이 기능 소개·사용법·도입 가이드·실제 화면 중심 설명이면 `github_feature_usage`를 선택한다. YouTube URL/트랜스크립트/댓글/영상 콘텐츠 갭 분석이 목적이면 `youtube_analysis`를 선택한다. 사용 설명서·운영 매뉴얼·절차서·트러블슈팅 제작/분석은 `manual_analysis`를 선택한다.

## Quick trigger map

- 쉽게/초보자/비유 → beginner_html
- 전문가/리포트/리스크/아키텍처 → expert_html
- GitHub 저장소 URL/깃허브 URL/owner/repo/README·Issues·Releases·License 실사·리스크 분석 → github_analysis
- GitHub 저장소 기능 소개/사용법/도입 가이드/실제 화면·스크린샷 중심 설명 → github_feature_usage
- YouTube URL/youtu.be/Shorts/영상 요약/트랜스크립트/댓글 분석/콘텐츠 갭 → youtube_analysis
- 매뉴얼 분석/사용 설명서/운영 매뉴얼/절차서/트러블슈팅/제품 가이드 → manual_analysis
- 아티클/공개 글/기사 → article_html
- 교육/강의/실습/퀴즈 → education_html
- 블로그/경험담/내 생각 → blog_writer
- SEO/검색/제목/메타/태그 → seo_dashboard
- 티스토리/벨로그/네이버/워드프레스 → platform_blog
- SKILL.md/.skill/스킬 감사/스킬 통합 → skill_audit
- API reference/옵션표/치트시트/빠른 참조 → reference_html
- 비교/장단점/선택 기준 → comparison_html
- 사례/회고/프로젝트 기록 → case_study_html
- 랜딩/소개/요약 페이지 → landing_brief_html
- 체크리스트/운영 절차/플레이북 → checklist_playbook

## github_analysis 선택 기준

`github_analysis`는 “저장소를 읽고 도입해도 되는가?”에 답하는 실사 모드다. 단순 README 재요약이 아니라 다음 질문을 목차화한다.

1. 이 프로젝트는 무엇을 해결하는가?
2. 지금 바로 실행하거나 도입할 수 있는가?
3. 어떤 파일/디렉터리부터 보면 되는가?
4. 최근에도 유지보수되고 있는가?
5. 라이선스·보안·공급망상 확인해야 할 리스크는 무엇인가?
6. 내 다음 행동은 사용, 검토, 보류, 대체 탐색 중 무엇인가?

## github_feature_usage 선택 기준

`github_feature_usage`는 “이 저장소/제품이 무엇을 해주고 어떻게 써야 하는가?”에 답하는 기능·사용법·도입 가이드 모드다. 리스크 실사보다 사용자·PM·도입 검토자가 바로 이해할 수 있는 기능 지도와 실제 화면 흐름을 우선한다.

1. 한 줄로 어떤 제품/모듈인가?
2. 사용자는 어떤 핵심 기능을 쓸 수 있는가?
3. 관리자·운영자는 어떤 기능을 관리하는가?
4. 실제 화면 또는 스크린샷에서 어떤 흐름이 보이는가?
5. 어떤 기술 스택·아키텍처·디렉터리 구조를 이해하면 도입이 쉬운가?
6. 어디에 잘 맞고, 어디에는 맞지 않는가?
7. 도입 전 확인해야 할 최소 조건과 다음 행동은 무엇인가?

## youtube_analysis 선택 기준

`youtube_analysis`는 “이 영상을 볼지, 믿을지, 재사용/제작에 쓸지”에 답하는 모드다.

1. 핵심 주장은 무엇인가?
2. 어느 타임스탬프/트랜스크립트가 근거인가?
3. 댓글·챕터·메타에서 반복 신호는 무엇인가?
4. FACT / INFERENCE / UNKNOWN은 어떻게 갈리는가?
5. 제작자/학습자의 다음 행동은 무엇인가?

URL만 있으면 Tier C로 제한해 Source Limits를 전면에 둔다. transcript/comment가 있을 때만 Evidence Map을 FACT로 확장한다.

## manual_analysis 선택 기준

`manual_analysis`는 “이 문서를 보고 실제로 따라 할 수 있는가?”에 답하는 모드다.

1. 독자 역할별 첫 행동은 무엇인가?
2. 사전조건·권한·위험 작업은 무엇인가?
3. 절차의 기대 결과와 검증 방법은 무엇인가?
4. 실패 시 어떤 증상/원인/해결로 복구하는가?
5. 원문 매뉴얼의 누락·중복·모순·stale 위험은 무엇인가?

### 충돌 처리

- GitHub Pages “배포 방법”이 주제이면 `article_html` 또는 `education_html`을 우선한다.
- 특정 저장소 URL이 있고 저장소 품질·구조·활동·리스크 분석이 목적이면 `github_analysis`를 우선한다.
- 특정 저장소 URL이 있고 기능·사용법·도입 가이드·실제 화면 설명이 목적이면 `github_feature_usage`를 우선한다.
- 한 요청 안에 `github_analysis`와 `github_feature_usage` 의도가 같이 있으면 사용자가 명시한 모드를 따른다. 명시가 없고 “리스크/건전성/라이선스/활동성/채택 판단”이 핵심이면 `github_analysis`, “기능/사용법/스크린샷/적합한 사용처/도입 가이드”가 핵심이면 `github_feature_usage`다.
- YouTube URL이 있고 영상 내용·댓글·트랜스크립트·콘텐츠 갭 분석이 목적이면 `youtube_analysis`를 우선한다.
- “매뉴얼”이라는 단어만 있어도 역할별 실행/운영/복구 문서가 목적이면 `manual_analysis`를 우선한다.
- API 옵션표·정규식·CLI 플래그처럼 빠른 참조가 목적이면 `reference_html`을 우선한다.
- 저장소 분석 결과를 다시 전문가 리포트로 확장해 달라는 명시가 있으면 사용자 지정 모드(`expert_html`)가 우선이다.
