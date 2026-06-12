# Layout Checklist

17개 레이아웃의 mode ↔ 파일 ↔ 필수블록 ↔ 폭클래스를 한눈에 검증한다.
폭 정본(v5.10.3): **모든 모드 레이아웃 = `.page-wide`(1020) + 단락 60rem(960px)** — `.page`(780)는 모드 레이아웃에 쓰지 않는다.
폭클래스: `.page` = `--max-reading`(780px), `.page-wide` = `--max-wide`(1020px).

## 자동 검증 (먼저 실행)

수동 체크 이전에 정적 게이트를 먼저 통과시킨다. 산출물 디렉터리 단위로 실행한다.

```
python3 scripts/validate_output.py <산출물 디렉터리> --skill-dir <스킬 루트>
```

- `OK`가 아니면(`FAILED` + `ISSUE ...`) 릴리즈를 중단하고 해당 회귀를 먼저 고친다.
- `--skill-dir`를 주면 CSS asset hash/snapshot, 인라인 CSS hash marker, source manifest version 동기화까지 함께 검사한다.
- 이 스크립트가 자동으로 막는 항목(h1 1개, `<main id="main">`, 외부 JS 0, 깨진 로컬 참조, caption 음수 margin, semantic section grid selector, visual figure 속성·8000×6000)은 아래 수동 체크의 1차 게이트다. 아래 v4.3.0~v4.3.3 절은 이 스크립트가 검사하는 회귀를 사람이 다시 눈으로 확인하는 보조 게이트다.

| 파일 | mode | 필수 블록 | 폭클래스 |
|---|---|---|---|
| skill-audit-report.html | skill_audit | executive-summary, summary-grid, line-audit, priority-roadmap, try(개선본) | .page-wide (1020) |
| platform-adaptation.html | platform_blog | original-summary, platform-strategy, platform-grid, platform-comparison-table | .page-wide (1020) |
| seo-dashboard.html | seo_dashboard | seo-overview, serp-preview, title-candidates, meta-candidates, keyword-cluster, content-outline | .page-wide (1020) |
| course-module.html | education_html | learning-goals, before-start, lesson-step, example-block, practice-card, quiz-box, answer-box, try | .page-wide (1020) |
| github-analysis.html | github_analysis | github-verdict, github-question-toc, repo-identity, quickstart-readiness, repo-health, code-tour, release-roadmap, security-license, risk-matrix, decision-tree, try | .page-wide (1020) |
| expert-report.html | expert_html | executive-summary, decision-grid, architecture-map, risk-matrix, priority-roadmap, validation-checklist, try | .page-wide (1020) |
| magazine-article.html | article_html | header(lead), pull-quote, article(problem/context/core-argument/case/conclusion), article-takeaway, related-list, source-note | .page-wide (1020) |
| personal-blog-essay.html | blog_writer | header(hook), personal-note, article(why-now/my-view/example/how-to-start/closing), soft-cta, source-note | .page-wide (1020) |
| beginner-learning.html | beginner_html | beginner-zero, beginner-terms, beginner-analogy, beginner-traps, beginner-practice, try | .page-wide (1020) |
| reference-manual.html | reference_html | quick-reference, ref-grid(concepts/API), patterns, examples, try(checklist) | .page-wide (1020) |
| comparison-matrix.html | comparison_html | decision-context, matrix, winners, tradeoffs, try(recommendation) | .page-wide (1020) |
| case-study.html | case_study_html | summary-card, timeline, decisions, results, try(lessons) | .page-wide (1020) |
| landing-brief.html | landing_brief_html | hero-analogy, value-grid, how-it-works, faq, try(CTA) | .page-wide (1020) |
| checklist-playbook.html | checklist_playbook | summary-card, check-grid, failure-modes, try(done criteria) | .page-wide (1020) |
| youtube-analysis.html | youtube_analysis | source trust, evidence map, comment signals, opportunity, source limits | .page-wide (1020) |
| manual-analysis.html | manual_analysis | source/version, role router, first success, safety, troubleshooting | .page-wide (1020) |
| github-feature-usage.html | github_feature_usage | positioning, feature toc/map, tech stack, screens, getting started, fit, pre-adoption, source note | .page-wide (1020) |

생성된 HTML을 릴리즈하기 전 확인한다.

- [ ] 선택 모드와 위 표의 파일/폭클래스가 일치한다.
- [ ] 해당 모드의 필수 블록이 모두 채워졌다.
- [ ] `lang="ko"`가 있다.
- [ ] title/meta description이 있다.
- [ ] h1은 1개다.
- [ ] CSS 기본 4개를 연결한다: `assets/theme.css`, `assets/components.css`, `assets/layouts.css`, `assets/print.css`. 시각 템플릿을 쓰면 `assets/visual-components.css`도 components 뒤에 포함한다.
- [ ] output HTML이 최신 CSS asset 합본을 사용한다. `sources/assets/*.css`, `sources/css-integrity.json`, 인라인 CSS hash marker가 현재 skill asset과 일치한다.
- [ ] 공개 블로그/아티클/SEO라면 Pretendard 폰트 링크가 있다.
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

## v4.3.2 Blog/SEO Polish Regression Gate

`validate_output.py`가 정적으로 막는 blog/SEO 회귀를 레이아웃 관점에서 재확인한다.

- [ ] `.h2-sub` 부제 단락이 `<p class="h2-sub">...</p>`로 올바르게 닫힌다 — `<p class="h2-sub">...</h2>` 형태의 닫는 태그 오류가 없다(`h2_sub_closed_as_h2` 게이트).
- [ ] `blog_writer` 본문 섹션 h2에 CSS counter 기반 번호 badge가 붙는다 — `.layout-blog article>section>h2:first-child::before`가 정의되어 다른 모드와 번호 일관성을 맞춘다(`missing_blog_section_counter` 게이트).
- [ ] `layout-seo .serp-title`이 Google 원문 모사형(`#1a0dab`, `Arial`)이 아니라 editorial UI 토큰(`var(--ink)`, sans, 17~18px, 800 weight)을 쓴다(`seo_serp_title_literal_google_style` 게이트).
- [ ] 검정 `.try`/`.try.soft-cta` 내부 `.tag` pill이 거의 흰 배경 + `var(--ink)` 굵은 텍스트로 재정의되어 `로컬LLM`/`Ollama` 같은 태그 대비가 흐려지지 않는다(`missing_try_tag_contrast_reset` 게이트).

## v4.3.3 Responsive Polish Regression Gate

기존 13개 모드 전수 캡쳐 감사에서 확인된 platform/table/dark CTA 회귀와 신규 github_analysis 레이아웃을 함께 재확인한다. `validate_output.py`가 정적으로 막는 항목이다.

- [ ] `platform-grid`가 semantic `<section>`에 직접 걸리지 않는다 — `<section class="platform-grid">`는 실패다. grid는 내부 wrapper(`.layout-platform .platform-grid:not(section)`)에만 적용한다(`platform_grid_used_as_section`, `platform_grid_selector_allows_section_grid` 게이트).
- [ ] 모든 `<table>`에 `<caption>`이 있다 — caption 없는 표는 실패다(`table_missing_caption` 게이트).
- [ ] 검정 CTA(`.try`, `.try.soft-cta`) 내부 링크가 `--link-on-dark` 토큰으로 밝게 재정의되어 dark 배경에서 4.5:1 이상 대비를 유지한다(`missing_try_dark_link_contrast_reset` 게이트).
- [ ] expert executive summary 4카드가 orphan 없이 2×2로 안정적으로 배치되고, case-study timeline이 단일 대형 카드가 아니라 개별 step card로 보인다.
- [ ] 390px 모바일에서 복잡한 표는 `.mobile-card-table`(`data-label` 기반 행 카드) 패턴으로 잘리지 않게 표시한다.

