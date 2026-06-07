# Layout System

| Mode | Layout | Width | Core Blocks | Visual Emphasis |
|---|---|---:|---|---|
| beginner_html | beginner-learning.html | 780 | toc, hero, term, analogy, traps, practice | h2-sub, term/analogy/danger/good, final try |
| expert_html | expert-report.html | 1020 | executive summary, risk, roadmap, validation | report cards, compact tables |
| article_html | magazine-article.html | 780 | lead, quote, argument, case, takeaway | prose rhythm, pull quote |
| education_html | course-module.html | 780 | goals, practice, quiz, answer | learning cards, details answers |
| github_analysis | github-analysis.html | 1020 | verdict, question toc, repo identity, quickstart, health signals, file tour, risks, final decision | evidence cards, repo signal grids, vt hero/file/risk views |
| youtube_analysis | youtube-analysis.html | 1020 | source trust, TL;DW, evidence map, chapter flow, comment signals, opportunity, source limits | timeline/risk/quality views, evidence cards |
| manual_analysis | manual-analysis.html | 1020 | source snapshot, role router, first success, prerequisites, recipes, troubleshooting, audit | hero/checklist/quality/file views, role cards |
| blog_writer | personal-blog-essay.html | 780 | hook, view, CTA | essay sections, restrained boxes |
| seo_dashboard | seo-dashboard.html | 1020 | SERP, candidates, tags | SERP card, tables/cards |
| platform_blog | platform-adaptation.html | 1020 | cards, comparison, checklist | platform grid |
| skill_audit | skill-audit-report.html | 1020 | diagnosis, scores, line audit, improved skill | audit rows, score cards |
| reference_html | reference-manual.html | 1020 | quick reference, concepts, patterns, examples | reference grid |
| comparison_html | comparison-matrix.html | 1020 | context, matrix, winners, tradeoffs | decision cards |
| case_study_html | case-study.html | 780 | situation, timeline, decisions, results | timeline |
| landing_brief_html | landing-brief.html | 1020 | hero, value props, how-it-works, FAQ, CTA | restrained editorial landing |
| checklist_playbook | checklist-playbook.html | 1020 | use case, check grid, failure modes, done criteria | operation cards |

모든 레이아웃은 `source-note`를 마지막에 둘 수 있어야 한다.

## Layout Safety Notes

- 섹션 간 간격은 `section{margin}`으로 통제한다. `section > h2:first-child`와 카드 컴포넌트 첫 h2/h3는 `margin-top:0`이어야 하며, 카드 안쪽에 큰 빈 상단 여백을 만들지 않는다.
- 의미형 section wrapper는 normal flow를 유지한다. `section.priority-roadmap`, `section.timeline`, `section.value-grid` 등에 직접 grid를 걸지 않는다.
- `.winners:not(section)`, `.tradeoffs:not(section)`는 h3+ul을 담는 텍스트 카드로 취급한다. h3와 목록을 2컬럼 grid item으로 나누지 말고, 실제 비교 카드가 필요할 때만 내부 `.grid-2`를 추가한다.
- 검정 `.try` 안에 밝은 카드가 들어가면 카드 내부 텍스트 색상 상속을 반드시 리셋한다.
- 검정 `.try` 안의 `.tag` pill은 dark-section의 흐린 텍스트를 상속하지 말고 밝은 pill + 진한 텍스트로 표시한다.
- `blog_writer`는 에세이 톤을 유지하되, section h2 앞에는 CSS counter 기반 번호 badge를 붙여 다른 모드와 진행감을 맞춘다.
- `seo_dashboard`의 SERP preview 제목은 검색결과의 의미만 차용하고, 색상/폰트/크기는 editorial dashboard의 균형을 따른다. 상세 미리보기는 `serp-shell`/`serp-box`/`serp-rule-grid` 정본 구조를 사용한다.
- `.platform-grid`는 section이 아니라 section 내부 wrapper에만 붙인다.
- `platform_blog`의 변환 전략은 `platform-split`/`platform-anchor`/`platform-route-grid`, 플랫폼별 산출 카드는 `platform-output-grid`/`platform-output-card`를 사용한다. final 페이지 전용 `platform-transform-*`류 prefix는 쓰지 않는다.
- 모바일에서 4열 이상 표가 빽빽하면 `.mobile-card-table` 패턴으로 행 카드화한다.
- case-study timeline은 단일 대형 카드보다 개별 step card가 기본이다.
- `github_analysis`는 `.repo-signal-grid` 같은 내부 wrapper에만 grid를 적용하고, `.repo-health`/`.security-license` 같은 semantic section 자체를 grid로 만들지 않는다.
- GitHub에서 확인할 수 없는 보안 설정·비공개 취약점·내부 운영 상태는 `확인 불가` 카드로 남기고 추측 점수를 만들지 않는다.
- `youtube_analysis`는 `.youtube-*-grid` 같은 내부 wrapper에만 grid를 적용하고, semantic section 자체를 grid로 만들지 않는다. iframe/embed는 금지한다.
- `manual_analysis`는 `.manual-*-grid` 같은 내부 wrapper에만 grid를 적용하고, 입력에 없는 역할 카드를 만들지 않는다.
- 검정 `.try` 안의 링크는 `--link-on-dark`를 써서 충분한 대비를 확보한다.
- case-study timeline의 왼쪽 강조선은 section 또는 내부 card 중 하나만 사용한다.


## Visual Template Defaults

| Mode | Default visual templates | Purpose |
|---|---|---|
| beginner_html | hero-map, checklist-flow | 비유·개념 흐름·오해 방지 |
| expert_html | hero-map, matrix, timeline, quality-gate | 운영모델·RACI·리스크·로드맵·검증 |
| article_html | hero-map, decision-tree | 주장 구조·쟁점 흐름 |
| education_html | timeline, checklist-flow | 학습 경로·실습 절차·퀴즈 전 체크 |
| github_analysis | hero-map, file-tour, risk-matrix, quality-gate | 저장소 판단 흐름·코드 구조·리스크·검증 기준 |
| youtube_analysis | timeline, risk-matrix, quality-gate | 영상 근거 흐름·주장 리스크·검증 기준 |
| manual_analysis | hero-map, checklist-flow, quality-gate, file-tour | 역할별 경로·절차·안전 게이트·출처 구조 |
| blog_writer | hero-map, timeline | 경험 흐름·문제 해결 여정 |
| seo_dashboard | card-grid, matrix | 키워드 클러스터·SERP·제목 후보 비교 |
| platform_blog | card-grid, matrix, checklist-flow | 플랫폼별 변환·발행 체크 |
| skill_audit | matrix, quality-gate, timeline | 점수 진단·결함 분류·개선 로드맵 |
| reference_html | card-grid, matrix | 개념/API/패턴 분류 |
| comparison_html | matrix, decision-tree | 선택 매트릭스·트레이드오프 판단 |
| case_study_html | timeline, hero-map | 사건 타임라인·원인-결정-결과 |
| landing_brief_html | hero-map, card-grid | 가치 제안·대상별 메시지 |
| checklist_playbook | checklist-flow, quality-gate | 운영 절차·완료 기준·실패 모드 |
