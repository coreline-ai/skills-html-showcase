# Golden Prompts

16개 모드를 대표하는 골든 프롬프트. 각 항목은 기대 모드와 레이아웃을 명시한다.

1. Docker를 초보자용 HTML 학습자료로 만들어줘.
   - expected_mode: beginner_html
   - expected_layout: beginner-learning.html
2. MCP Gateway 설계를 전문가 리포트 HTML로 검토해줘.
   - expected_mode: expert_html
   - expected_layout: expert-report.html
3. AI 시대 개인 지식 블로그에 대한 공개 아티클을 만들어줘.
   - expected_mode: article_html
   - expected_layout: magazine-article.html
4. GitHub Pages 교육용 HTML을 만들어줘. 퀴즈 포함.
   - expected_mode: education_html
   - expected_layout: course-module.html
5. Mac mini를 개인 AI 서버로 쓰는 블로그 글을 작성해줘.
   - expected_mode: blog_writer
   - expected_layout: personal-blog-essay.html
6. GraphRAG 입문 글의 SEO 제목/메타/태그를 만들어줘.
   - expected_mode: seo_dashboard
   - expected_layout: seo-dashboard.html
7. 같은 글을 티스토리/벨로그/네이버/워드프레스용으로 바꿔줘.
   - expected_mode: platform_blog
   - expected_layout: platform-adaptation.html
8. 이 SKILL.md를 한 줄 한 줄 분석하고 개선본을 만들어줘.
   - expected_mode: skill_audit
   - expected_layout: skill-audit-report.html
9. Kubernetes kubectl 명령어 레퍼런스/매뉴얼 HTML을 만들어줘. 빠른 참조, 개념, 패턴, 예제, 체크리스트 포함.
   - expected_mode: reference_html
   - expected_layout: reference-manual.html
10. Postgres와 MySQL의 장단점과 선택 기준을 비교 매트릭스로 정리해줘. 승자와 트레이드오프, 추천까지.
    - expected_mode: comparison_html
    - expected_layout: comparison-matrix.html
11. 사내 로그 파이프라인을 ELK로 전환한 사례 연구/회고를 작성해줘. 상황, 타임라인, 결정, 결과, 교훈 포함.
    - expected_mode: case_study_html
    - expected_layout: case-study.html
12. 신규 사내 AI 어시스턴트 소개 랜딩 브리프를 만들어줘. 히어로, 가치 제안, 동작 방식, FAQ, CTA 포함.
    - expected_mode: landing_brief_html
    - expected_layout: landing-brief.html
13. 배포 전 점검 체크리스트/운영 플레이북을 만들어줘. 사용 사례, 체크 그리드, 실패 모드, 완료 기준 포함.
    - expected_mode: checklist_playbook
    - expected_layout: checklist-playbook.html
14. https://github.com/coreline-ai/skills-html-showcase 저장소를 사용자가 가장 궁금해할 질문 중심으로 분석해줘. README, 파일 구조, 릴리스/이슈/라이선스/리스크와 다음 행동을 HTML로 정리해줘.
    - expected_mode: github_analysis
    - expected_layout: github-analysis.html


15. YouTube 영상 콘텐츠 갭 분석
   - prompt: `https://youtu.be/example 영상의 transcript와 댓글 메모를 바탕으로 콘텐츠 갭과 다음 영상 기획을 youtube_analysis 모드로 정리해줘.`
   - expected_mode: youtube_analysis
   - expected_layout: youtube-analysis.html

16. 제품 매뉴얼 역할별 실행 문서
   - prompt: `다음 README와 운영 절차서를 사용 설명서/운영 매뉴얼로 재구성하고 누락·위험 작업을 감사해줘.`
   - expected_mode: manual_analysis
   - expected_layout: manual-analysis.html
