# Layout Checklist

13개 레이아웃의 mode ↔ 파일 ↔ 필수블록 ↔ 폭클래스를 한눈에 검증한다.
폭클래스: `.page` = `--max-reading`(780px), `.page-wide` = `--max-wide`(1020px).

| 파일 | mode | 필수 블록 | 폭클래스 |
|---|---|---|---|
| skill-audit-report.html | skill_audit | executive-summary, summary-grid, line-audit, priority-roadmap, try(개선본) | .page-wide (1020) |
| platform-adaptation.html | platform_blog | original-summary, platform-strategy, platform-grid, platform-comparison-table | .page-wide (1020) |
| seo-dashboard.html | seo_dashboard | seo-overview, serp-preview, title-candidates, meta-candidates, keyword-cluster, content-outline | .page-wide (1020) |
| course-module.html | education_html | learning-goals, before-start, lesson-step, example-block, practice-card, quiz-box, answer-box, try | .page (780) |
| expert-report.html | expert_html | executive-summary, decision-grid, architecture-map, risk-matrix, priority-roadmap, validation-checklist, try | .page-wide (1020) |
| magazine-article.html | article_html | header(lead), pull-quote, article(problem/context/core-argument/case/conclusion), article-takeaway, related-list, source-note | .page (780) |
| personal-blog-essay.html | blog_writer | header(hook), personal-note, article(why-now/my-view/example/how-to-start/closing), soft-cta, source-note | .page (780) |
| beginner-learning.html | beginner_html | beginner-zero, beginner-terms, beginner-analogy, beginner-traps, beginner-practice, try | .page (780) |
| reference-manual.html | reference_html | quick-reference, ref-grid(concepts/API), patterns, examples, try(checklist) | .page-wide (1020) |
| comparison-matrix.html | comparison_html | decision-context, matrix, winners, tradeoffs, try(recommendation) | .page-wide (1020) |
| case-study.html | case_study_html | summary-card, timeline, decisions, results, try(lessons) | .page (780) |
| landing-brief.html | landing_brief_html | hero-analogy, value-grid, how-it-works, faq, try(CTA) | .page-wide (1020) |
| checklist-playbook.html | checklist_playbook | summary-card, check-grid, failure-modes, try(done criteria) | .page-wide (1020) |

생성된 HTML을 릴리즈하기 전 확인한다.

- [ ] 선택 모드와 위 표의 파일/폭클래스가 일치한다.
- [ ] 해당 모드의 필수 블록이 모두 채워졌다.
- [ ] `lang="ko"`가 있다.
- [ ] title/meta description이 있다.
- [ ] h1은 1개다.
- [ ] CSS 기본 4개를 연결한다: `assets/theme.css`, `assets/components.css`, `assets/layouts.css`, `assets/print.css`. 시각 템플릿을 쓰면 `assets/visual-components.css`도 components 뒤에 포함한다.
- [ ] output HTML이 최신 CSS asset 합본을 사용한다. `sources/assets/*.css`, `sources/css-integrity.json`, 인라인 CSS hash marker가 현재 skill asset과 일치한다.
- [ ] 공개 블로그/아티클/SEO라면 Pretendard/Noto Serif KR 폰트 링크가 있다.
- [ ] H1이 한국어 긴 제목에서 과도하게 크지 않다(`clamp()` 상한 42px 유지).
- [ ] 주요 h2에 `.h2-sub`가 있다(모드 한정 권장).
- [ ] `.term`, `.analogy`, `.danger`, `.good`, `.try`, `.source-note` 중 5개 이상을 적절히 사용한다.
- [ ] `.hl`은 2~4개이며 색상 박스 내부에 없다.
- [ ] 출처 링크가 많으면 본문 말미 출처 목록 또는 `sources/index.html` 허브로 분리한다.
- [ ] 모바일 폭에서 그리드가 1컬럼이다.
- [ ] 표는 `.tbl` wrapper 또는 모바일 안전 구조다.
- [ ] 모바일 390px에서 표 캡션, 긴 제목, 카드 텍스트가 잘리지 않는다.
- [ ] 시각 템플릿을 사용했다면 `.visual-figure`/`.figure-wide`, `img[width][height][alt]`, `figcaption`이 있다.
- [ ] SVG 원본은 8000×6000 이상이며 내부 카드/텍스트가 캔버스 하단이나 측면에 걸려 잘리지 않는다.
- [ ] `<caption>`에 음수 margin/absolute/hidden overflow를 적용하지 않았다.
- [ ] 외부 동작 JS를 사용하지 않는다.


## v4.3.0 Layout Regression Gate

- 섹션 wrapper(`section.matrix`, `section.serp-preview`, `section.value-grid`, `section.check-grid`, `section.priority-roadmap` 등)에 `display:grid`를 직접 적용하지 않는다.
- h2, `.h2-sub`, 본문 문단, `.tbl`은 카드 grid item으로 쪼개지면 실패다. 실제 카드/매트릭스는 내부 `.card-grid`, `.grid-2`, `.grid-3`, `.matrix:not(section)` wrapper로 분리한다.
- 390px와 1280px에서 `documentElement.scrollWidth <= clientWidth`를 확인한다. 단, `.tbl` 내부 스크롤은 허용한다.

## v4.3.1 Design Polish Regression Gate

- [ ] `section>h2:first-child` 또는 동등한 첫 heading margin reset이 있다.
- [ ] `.try` 내부 밝은 카드(`.box/.summary-card/.cta-box/.card-block/.mini-card`)는 카드 내부 p/li/strong 색상을 light-surface 토큰으로 되돌린다.
- [ ] `.winners:not(section)`, `.tradeoffs:not(section)`에 `display:grid`를 직접 걸지 않는다.
- [ ] case-study timeline은 section wrapper와 내부 timeline card가 동시에 left border를 만들지 않는다.
