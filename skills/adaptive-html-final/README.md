# Adaptive HTML Final (v5.10.3)

`adaptive-html-learning-ultimate`(13모드 라우터·레이아웃·평가체계)에 GitHub 실사 분석, GitHub 기능·사용법·도입 가이드, YouTube 분석, Manual 분석 모드를 더한 17모드 체계와 `adaptive-html-blog-writer`(블로그·SEO·플랫폼 상세 규칙)를 하나로 합친 **최종 통합 한국어 HTML 콘텐츠 생성 스킬**입니다.

> **v5.10.3 현재 요약**
> - 17번째 모드 `github_feature_usage`: GitHub 저장소를 "무엇을 해주나·어떻게 쓰나·어디에 맞나" 관점의 기능·사용법·도입 가이드 HTML로 변환. 실제 화면(스크린샷)·기능 지도·기술 스택·아키텍처·디렉터리 구조 해부를 포함한다.
> - 15번째 모드 `youtube_analysis`: YouTube URL/자막/댓글 발췌를 Video Evidence Map, FACT/INFERENCE/UNKNOWN, 댓글 신호, Claim Risk, 재사용 전략 중심의 HTML 분석 리포트로 변환.
> - 16번째 모드 `manual_analysis`: 제품/운영 매뉴얼을 Source & Version Snapshot, Reader Role Router, First Success Path, Prerequisites/Safety, Troubleshooting, Operations Runbook 중심의 역할별 실행 매뉴얼로 재구성.
> - 신규 레이아웃 `assets/layouts/github-feature-usage.html`, 전략 문서 `references/github-feature-usage-system.md`, recipe, 계약 게이트, 17번째 예제 `examples/17_github_feature_usage_coreline_auth.html`를 추가.

> **현행 요약 (v4.1 → v4.5.0)**
> - **v4.1**(정밀 분석 패치): 접근성 테스트 체크리스트 추가, 13개 모드 ID를 SKILL.md 라우터와 통일(`{id, layout}` 매핑), recipes 13/13 완비, blog-meta·quality-report 스키마 보강, 미정의 CSS 클래스 39개 정의로 차집합 0 달성.
> - **v4.2**(Visual Template System): 8000×6000 SVG 인포그래픽 템플릿 7종(`visual-templates/*.svg.tpl`)과 stdlib-only 렌더러 `scripts/render_visual_svg.py`, `assets/visual-components.css`, `schemas/visual-brief.schema.json`, SKILL.md Step 4.5 Visual Brief Planning 도입.
> - **v4.3.x**(반응형 폴리시 회귀 게이트): dark CTA 링크/태그 대비 회복(`--link-on-dark`), `platform-grid`를 inner wrapper 전용으로 제한, 390px용 `mobile-card-table` 패턴, case timeline을 개별 step card로 분리, blog 섹션 자동 번호·SEO SERP title 조정 — 그리고 이 모든 회귀를 정적으로 막는 `scripts/validate_output.py` 게이트.
> - **v4.4.0**(뷰 위젯 시스템): 뷰 위젯 시스템(20종, CSS-only, `assets/widgets.css`) 정식 편입 — `wg-<id>-` 네임스페이스·무 JS 위젯 템플릿 `assets/widget-templates/*.html`, 선택·삽입·접근성 규칙 `references/widget-system.md`, 위젯 게이트 `tests/widget-checklist.md`.
> - **v4.5.0**(SVG→HTML 템플릿 편입 & 하네스 정형화): SVG→HTML 뷰 템플릿 21종(`assets/visual-html.css`)과 본문 삽입 다이어그램 `assets/visual-html-templates/01..21.html`(`vt-`), 캐노니컬 모드→vt 매핑·결정론 진입점, 선택·삽입 규칙 `references/visual-html-system.md`. 무 JS 0 유지.
> - **v4.5.0**(비주얼 프로파일 선택): 기동 시 비주얼 스타일 선택 — `profile=widget|diagram|auto`(별칭 `style=v5|v6`). 코어(17모드·레이아웃·코어 CSS)는 공유, 프로파일이 라이브러리·삽입단계·CSS 번들만 게이트. 검증기 `--profile`로 교차 누수 차단. `manifest.json` `profiles` 선언. 분리 계획: 루트 `implement_visual_profile_separation.md`.

### 비주얼 프로파일 (스킬 기동 시 선택)

| 프로파일 | 별칭 | 라이브러리 | CSS 번들 | 골든 |
|---|---|---|---|---|
| `widget` | `style=v5` | CSS 뷰 위젯 `wg-01~20` | 코어5 + `widgets.css` | showcase-v5(정합화) |
| `diagram` | `style=v6` | SVG→HTML `vt-` 21종 | 코어5 + `visual-html.css` | showcase-v6 슬림 |
| `auto`(기본) | — | 둘 다(vt- 1순위 + wg- 보강) | 코어5 + 둘 다 | showcase-v6 |

선택 규칙: 인자 우선(`trim→lowercase→정규화`, `profile=` 우선, 무효는 `invalid_profile` 실패). 미지정 시 비대화형(Codex/Gemini 등 AGENTS.md 경유)=무조건 `auto`, 대화형(Claude)=1회 질문. 결정론은 인자 명시 경로 한정.

## 핵심

- 11개 핵심/실사/사용 가이드 모드: beginner, expert, article, education, github_analysis, github_feature_usage, youtube_analysis, manual_analysis, blog, seo, platform
- 6개 확장 모드: skill_audit, reference, comparison, case_study, landing_brief, checklist_playbook
- 디자인 유지: 오프화이트 배경, Pretendard 단일 산세리프, h2 빨간 원번호, h2-sub, 의미 박스, source-note
- 블로그 강점 흡수: 제목 4계열·도입부 3유형·본문 밀도·블로그 메타 스키마·플랫폼별 규칙·박스 선택 가이드(references 상세)
- 접근성 수정: 17개 레이아웃 `<main>`에 `id="main"` 통일 (skip link 정상 동작)

## 통합 내역

| 출처 | 가져온 것 |
|---|---|
| adaptive-html-learning-ultimate@3.0.0 | 13모드 라우터, 13개 레이아웃, 평가 루브릭, recipes, schemas, 레이어드 CSS |
| adaptive-html-blog-writer@2.0.0 | blog-seo / writing / platform / editorial-design references 상세본, SKILL.md 트리거·출력 원칙 |

## 주요 파일

- `SKILL.md`: 최종 워크플로우와 모드 라우터
- `assets/theme.css`: 공통 editorial 테마
- `assets/components.css`: 박스/하이라이트/표/출처 컴포넌트
- `assets/visual-components.css`: `figure.visual-figure`/figcaption/visual grid·pipeline 등 시각 인포그래픽 삽입용 반응형 스타일
- `assets/widgets.css`: 뷰 위젯 20종 CSS-only 스타일 (`wg-<id>-` 네임스페이스, 무 JS)
- `assets/widget-templates/*.html`: 뷰 위젯 템플릿 20종 (01~20)
- `assets/visual-html.css`: SVG→HTML 뷰 템플릿 21종 (`assets/visual-html-templates/01..21.html`, `vt-` 본문 삽입 다이어그램, 무 JS)
- `assets/layouts.css`: 모드별 레이아웃 차이
- `assets/base.html`: 단일 HTML 렌더링 골격
- `assets/print.css`: 인쇄 대응
- `assets/layouts/*.html`: 17개 레이아웃 템플릿
- `assets/layouts/github-analysis.html`: GitHub 저장소 분석 전용 레이아웃
- `assets/layouts/github-feature-usage.html`: GitHub 기능·사용법·도입 가이드 전용 레이아웃
- `assets/layouts/youtube-analysis.html`: YouTube 영상 분석 전용 레이아웃
- `assets/layouts/manual-analysis.html`: 매뉴얼 제작/분석 전용 레이아웃
- `template-catalog/`: final_20260604 손검수 템플릿 HTML 정본 4종(예제 기준선이 아닌 디자인 카탈로그)
- `visual-templates/*.svg.tpl`: 8000×6000 SVG 인포그래픽 템플릿 7종 (hero-map, card-grid, decision-tree, quality-gate, timeline, matrix, checklist-flow)
- `scripts/render_visual_svg.py`: visual brief JSON을 8000×6000 SVG로 렌더링하는 stdlib-only 스크립트
- `scripts/validate_output.py`: 생성된 output 디렉터리를 검사하는 정적 품질 게이트 (h1·`#main`·로컬 참조·caption·grid 회귀·source sync·visual figure 등)
- `references/github-analysis-system.md`: GitHub 저장소 분석 정보 구조·판단 기준
- `references/github-feature-usage-system.md`: GitHub 기능·사용법·도입 가이드 정보 구조·스크린샷 계약
- `references/youtube-analysis-system.md`: YouTube 근거 지도·댓글 신호·주장 위험 분석 기준
- `references/manual-analysis-system.md`: 역할별 매뉴얼·안전 조건·트러블슈팅 작성 기준
- `references/*.md`: 필요 시 로드하는 세부 규칙 (`widget-system.md` 위젯 선택·삽입·접근성 규칙, `visual-html-system.md` SVG→HTML 템플릿 모드→vt 매핑·삽입 규칙 포함)
- `recipes/*.md`: 대표 요청 프롬프트 (17모드)
- `tests/*.md`: 검증 체크리스트 6종 (accessibility, golden-prompts, layout, quality, visual-regression, widget-checklist)
- `schemas/*.json`: 메타/품질/시각 스키마 3종 (blog-meta, quality-report, visual-brief)
