# Adaptive HTML Final (v4.3.3)

`adaptive-html-learning-ultimate`(13모드 라우터·레이아웃·평가체계)와 `adaptive-html-blog-writer`(블로그·SEO·플랫폼 상세 규칙)를 하나로 합친 **최종 통합 한국어 HTML 콘텐츠 생성 스킬**입니다.

> **현행 요약 (v4.1 → v4.3.3)**
> - **v4.1**(정밀 분석 패치): 접근성 테스트 체크리스트 추가, 13개 모드 ID를 SKILL.md 라우터와 통일(`{id, layout}` 매핑), recipes 13/13 완비, blog-meta·quality-report 스키마 보강, 미정의 CSS 클래스 39개 정의로 차집합 0 달성.
> - **v4.2**(Visual Template System): 8000×6000 SVG 인포그래픽 템플릿 7종(`visual-templates/*.svg.tpl`)과 stdlib-only 렌더러 `scripts/render_visual_svg.py`, `assets/visual-components.css`, `schemas/visual-brief.schema.json`, SKILL.md Step 4.5 Visual Brief Planning 도입.
> - **v4.3.x**(반응형 폴리시 회귀 게이트): dark CTA 링크/태그 대비 회복(`--link-on-dark`), `platform-grid`를 inner wrapper 전용으로 제한, 390px용 `mobile-card-table` 패턴, case timeline을 개별 step card로 분리, blog 섹션 자동 번호·SEO SERP title 조정 — 그리고 이 모든 회귀를 정적으로 막는 `scripts/validate_output.py` 게이트.

## 핵심

- 7개 핵심 모드: beginner, expert, article, education, blog, seo, platform
- 6개 확장 모드: skill_audit, reference, comparison, case_study, landing_brief, checklist_playbook
- 디자인 유지: 오프화이트 배경, Pretendard + Noto Serif KR, h2 빨간 원번호, h2-sub, 의미 박스, source-note
- 블로그 강점 흡수: 제목 4계열·도입부 3유형·본문 밀도·블로그 메타 스키마·플랫폼별 규칙·박스 선택 가이드(references 상세)
- 접근성 수정: 13개 레이아웃 `<main>`에 `id="main"` 통일 (skip link 정상 동작)

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
- `assets/layouts.css`: 모드별 레이아웃 차이
- `assets/base.html`: 단일 HTML 렌더링 골격
- `assets/print.css`: 인쇄 대응
- `assets/layouts/*.html`: 13개 레이아웃 템플릿
- `visual-templates/*.svg.tpl`: 8000×6000 SVG 인포그래픽 템플릿 7종 (hero-map, card-grid, decision-tree, quality-gate, timeline, matrix, checklist-flow)
- `scripts/render_visual_svg.py`: visual brief JSON을 8000×6000 SVG로 렌더링하는 stdlib-only 스크립트
- `scripts/validate_output.py`: 생성된 output 디렉터리를 검사하는 정적 품질 게이트 (h1·`#main`·로컬 참조·caption·grid 회귀·source sync·visual figure 등)
- `references/*.md`: 필요 시 로드하는 세부 규칙
- `recipes/*.md`: 대표 요청 프롬프트 (13모드)
- `tests/*.md`: 검증 체크리스트 5종 (accessibility, golden-prompts, layout, quality, visual-regression)
- `schemas/*.json`: 메타/품질/시각 스키마 3종 (blog-meta, quality-report, visual-brief)
