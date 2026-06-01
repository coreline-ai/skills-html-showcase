# Editorial Pattern System

기존 13개 모드를 늘리지 않고, **필요한 섹션에 선택 삽입하는 작은 본문 구조 패턴 6종**이다. 큰 SVG 시스템이 아니라 본문 흐름에 붙는 카드·타임라인·콜아웃 중심이며, 외부/동작 JS 0, 스킬 디자인 토큰 + body icon(`bi-`)을 쓴다.

- **자산**: `assets/editorial-patterns.css`(패턴 CSS) + `assets/editorial-pattern-templates/01..06.html`(삽입 골격) + body icon(`assets/body-icons.css`)
- **프로파일 무관**: widget/diagram/auto 어디서나 사용(본문 구조 보조). 조건부 인라인(`{{EDITORIAL_PATTERNS_CSS}}` 슬롯).

## 6종 패턴

| pattern | 이름 | 아이콘 | 추천 모드 |
|---|---|---|---|
| `chronology` | 증류 연대기 (timeline) | `timeline` | expert_html · case_study_html · skill_audit · education_html |
| `source-preserve` | 원문 보존 카드 | `source` | reference_html · article_html · blog_writer · skill_audit |
| `core-insight` | 핵심 아이디어 callout | `idea` | article_html · blog_writer · expert_html · landing_brief_html |
| `connection` | 연결 분석 카드 | `connection` | reference_html · skill_audit · article_html · comparison_html |
| `before-after` | Before / After 윤문 | `edit` | platform_blog · blog_writer · skill_audit · comparison_html |
| `impact-grid` | 콘텐츠 전환 impact grid | `impact` | platform_blog · landing_brief_html · seo_dashboard · checklist_playbook |

## 삽입 규칙

- 해당 섹션 목적에 맞는 패턴만 **선택 삽입**한다. 한 페이지에 과용 금지(특히 `core-insight`는 **페이지당 1개**가 가장 강하다).
- 골격은 `assets/editorial-pattern-templates/NN-*.html`를 복사해 **콘텐츠만 교체**(클래스·구조 유지). `editorial-patterns.css`를 인라인한다.
- 아이콘이 들어가는 패턴(impact-grid 등)은 `aria-hidden` body icon을 쓴다(장식, 의미는 텍스트로).
- 무 JS: `source-preserve`는 `<details>`(네이티브 접기)만 사용. 동작 JS 금지.

## 적용 갤러리

`output/adaptive-html-final-editorial-pattern-demo-v1/index.html` (6 패턴 도입 데모).
