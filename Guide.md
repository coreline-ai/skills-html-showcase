# adaptive-html-final 사용 가이드

작성일: 2026-05-30
대상 스킬: `skills/adaptive-html-final` (v4.0.0)

## 1. 개요

`adaptive-html-final`은 입력 자료(URL, PDF, 텍스트, 이미지 추출문, 메모, 기술 문서, 블로그 초안, SKILL.md/.skill)를 받아 **고품질 한국어 HTML 콘텐츠**를 만드는 다중 모드 스킬입니다.

이 스킬은 기존 두 스킬을 하나로 합친 최종 통합본입니다.

```text
html-for-beginners
  → adaptive-html-blog-writer        (블로그/SEO/플랫폼 상세 규칙)
  → adaptive-html-learning-ultimate  (13모드 라우터·레이아웃·평가체계)
  → adaptive-html-final              (둘을 통합 + 접근성 버그 수정)  ← 현재 운영본
```

운영 원칙:

1. 기본 HTML 생성·블로그·SEO·플랫폼 변환·스킬 감사 모두 `adaptive-html-final` 하나로 처리합니다.
2. 13개 모드 라우터가 요청을 자동 분류하고, 모드별 레이아웃과 글쓰기 규칙을 적용합니다.
3. 출처가 확인되지 않은 최신 정보·수치·가격은 단정하지 않고 `확인 필요`로 표시합니다.

## 2. 패키지 현황

| 항목 | 값 |
|---|---|
| 스킬명 | `adaptive-html-final` |
| version | `4.0.0` |
| 압축 해제 디렉토리 | `skills/adaptive-html-final/` |
| 설치용 패키지 | `skills/adaptive-html-final.skill` |
| 파일 수 | 51개 |
| 모드 수 | 13개 |
| 레이아웃 수 | 13개 |
| CSS 자산 | 4개 + base template |
| 스키마 | JSON 정상 (blog-meta, quality-report) |
| aliases | `adaptive-html-learning-ultimate`, `adaptive-html-blog-writer-v2` |

> 기존 `adaptive-html-learning-ultimate-20260530-final.skill`과 `adaptive-html-blog-writer.skill`은 본 스킬에 통합되어 삭제되었습니다. 두 이름은 manifest의 `aliases`·`merged_from`에 이력으로 보존됩니다.

## 3. 핵심 구조

```text
SKILL.md                    # 스킬 라우터, 워크플로우, 품질 기준
manifest.json               # 이름, 버전, assets/layouts/modes, merged_from/aliases
README.md                   # 스킬 요약
assets/base.html            # 단일 HTML 렌더링 기본 골격 (skip link 포함)
assets/theme.css            # 색상, 폰트, 폭, 기본 타이포그래피
assets/components.css       # term/analogy/danger/good/try/table 등 공통 컴포넌트
assets/layouts.css          # 모드별 그리드와 시각 구조
assets/print.css            # 인쇄 대응
assets/layouts/*.html       # 13개 모드별 HTML 골격 (모두 <main id="main">)
references/*.md             # 필요할 때만 읽는 세부 작성 규칙 (10종)
recipes/*.prompt.md         # 대표 요청 프롬프트 (6종)
schemas/*.json              # 블로그 메타/품질 리포트 스키마
tests/*.md                  # 품질/레이아웃/시각 회귀 체크리스트
examples/*.html             # 예시 결과물 (7종 + index)
```

## 4. 동작 파이프라인

이 스킬은 단순 HTML 변환기가 아니라 다음 순서로 결과물을 만듭니다.

```text
입력 분석
→ 사실 / 해석 / 추론 / 확인 필요 분리
→ 독자 수준 판단
→ 모드 선택
→ 레이아웃 선택
→ 글쓰기·학습·SEO·플랫폼 최적화
→ editorial HTML 렌더링
→ 품질 검수
→ 파일/링크 제시
```

중요 원칙:

- 확인되지 않은 최신 정보, 가격, 수치, 정책은 단정하지 않습니다.
- 사용자가 HTML을 요구하면 단일 HTML 또는 로컬 assets 연결형 HTML을 생성합니다.
- 외부 JS는 쓰지 않습니다.
- 공개 블로그 품질이 필요하면 Pretendard Variable + Noto Serif KR 폰트를 사용합니다.
- 결과물은 `lang="ko"`, viewport, title, meta description, h1 1개를 보장해야 합니다.

## 5. 13개 모드 사용표

| 우선순위 | 모드 | 언제 쓰나 | 레이아웃 |
|---:|---|---|---|
| 1 | `skill_audit` | SKILL.md/.skill 분석, 개선, 통합 | `skill-audit-report.html` |
| 2 | `platform_blog` | 티스토리, 벨로그, 네이버, 워드프레스 변환 | `platform-adaptation.html` |
| 3 | `seo_dashboard` | SEO 제목, 메타, 태그, 검색 의도 설계 | `seo-dashboard.html` |
| 4 | `education_html` | 강의, 온보딩, 실습, 퀴즈 | `course-module.html` |
| 5 | `expert_html` | 전문가 리포트, 아키텍처, 리스크 진단 | `expert-report.html` |
| 6 | `article_html` | 공개 아티클, 매거진형 글, GitHub Pages 글 | `magazine-article.html` |
| 7 | `blog_writer` | 블로그 글, 포스팅, 경험담, 관점 글 | `personal-blog-essay.html` |
| 8 | `beginner_html` | 초보자용 설명, 비유, 용어 풀이 | `beginner-learning.html` |
| 9 | `reference_html` | 레퍼런스, 매뉴얼, API 문서 | `reference-manual.html` |
| 10 | `comparison_html` | 비교, 장단점, 선택 기준 | `comparison-matrix.html` |
| 11 | `case_study_html` | 사례 연구, 회고, 프로젝트 기록 | `case-study.html` |
| 12 | `landing_brief_html` | 소개 페이지, 랜딩, 요약 페이지 | `landing-brief.html` |
| 13 | `checklist_playbook` | 체크리스트, 운영 절차, 플레이북 | `checklist-playbook.html` |

주의: 여러 트리거가 동시에 들어오면 기본적으로 우선순위가 높은 모드가 선택됩니다. 단, 사용자가 모드를 명시하면 사용자 지시가 우선입니다.

## 6. 가장 좋은 요청 템플릿

```text
[입력 자료/URL/파일/주제]를 [목적/독자]용 [모드]로 만들어줘.
출력은 [단일 HTML/Markdown+HTML/플랫폼별 원고]로 해줘.
반드시 포함: [목차, 용어 풀이, 예시, 리스크, FAQ, CTA 등]
주의: [최신 정보는 확인 필요 표시, 외부 JS 금지, 모바일 안전 표 등]
저장 위치/파일명: [원하는 경로]
```

예시:

```text
이 문서를 초보자용 HTML 학습자료로 만들어줘.
전문 용어는 용어 박스로 풀고, 일상 비유, 함정/해결, 마지막 실습 체크리스트를 넣어줘.
단일 HTML 파일로 저장해줘.
```

## 7. 모드별 예시 프롬프트

### 초보자 학습자료

```text
Docker 개념을 beginner_html 모드로 HTML 학습자료로 만들어줘.
목차, 핵심 비유, 용어 박스, 흔한 오해, 실습 체크리스트를 포함해줘.
```

### 전문가 리포트

```text
이 아키텍처 메모를 expert_html 모드로 전문가 리포트 HTML로 정리해줘.
Executive Summary, 리스크 매트릭스, 우선순위 로드맵, 검증 체크리스트를 포함해줘.
```

### 블로그 글

```text
이 주제로 blog_writer 모드 블로그 글을 작성해줘.
제목 후보 8개, 추천 제목, 메타 설명, 목차, 본문, FAQ, CTA, 태그를 포함해줘.
필요하면 HTML 버전도 같이 만들어줘.
```

### SEO 대시보드

```text
GraphRAG 입문 글의 seo_dashboard를 만들어줘.
검색 의도, primary/secondary keyword, SERP preview, 제목 후보 10개, 메타 설명 후보, 최종 SEO set을 포함해줘.
```

### 플랫폼별 변환

```text
이 글을 platform_blog 모드로 티스토리, 벨로그, 네이버, 워드프레스용으로 각각 변환해줘.
각 플랫폼별 제목, 본문 구조, 태그, 발행 체크리스트를 나눠줘.
```

### 스킬 감사

```text
이 SKILL.md를 skill_audit 모드로 분석해줘.
목적, 트리거, 입력/출력, 워크플로우, 품질 게이트, 완료 기준을 평가하고 개선본까지 제시해줘.
```

### 비교 매트릭스

```text
A/B/C 도구를 comparison_html 모드로 비교 HTML로 만들어줘.
선택 기준, 장단점, 추천 상황, 최종 의사결정 표를 포함해줘.
```

### 운영 체크리스트

```text
배포 전 점검 절차를 checklist_playbook 모드로 HTML 플레이북으로 만들어줘.
체크 그리드, 실패 모드, 완료 기준을 포함해줘.
```

## 8. HTML 생성 시 내부 사용법

스킬을 직접 운용할 때는 다음 순서를 따릅니다.

1. `SKILL.md`에서 요청과 맞는 모드를 고릅니다.
2. 필요한 경우에만 `references/*.md`를 추가로 읽습니다.
3. 해당 모드의 `assets/layouts/*.html` 템플릿을 선택합니다.
4. `assets/base.html`에 body를 삽입합니다.
5. CSS는 `theme.css → components.css → layouts.css → print.css` 순서로 합칩니다.
6. 공개 블로그면 title/meta/OG/JSON-LD 후보를 넣습니다.
7. 최종 품질 게이트를 확인합니다.

관련 references:

- `editorial-design-system.md` — 디자인 DNA, 컴포넌트 규칙, **박스 선택 가이드**, 시각 사고 방지
- `writing-system.md` — 모드별 글쓰기 + **제목 4계열·도입부 3유형·본문 밀도·톤 매핑**
- `blog-seo-system.md` — 제목/메타/SERP/태그 + **Blog Metadata Schema·Blog Quality Score(100점)**
- `platform-system.md` — 티스토리/벨로그/네이버/워드프레스 **발행 관점 세부 규칙**
- `mode-selection.md`, `layout-system.md`, `skill-audit-system.md`, `eval-rubric.md`, `quality-gates.md`, `design-dna.md`

## 9. 품질 게이트 요약

최소 통과 조건:

- [ ] 선택 모드와 요청 목적이 맞다.
- [ ] 선택 모드의 필수 블록이 있다.
- [ ] `lang="ko"`, viewport, title, meta description이 있다.
- [ ] h1은 1개다.
- [ ] 주요 h2에 `.h2-sub` 또는 동등한 부제가 있다.
- [ ] 모바일에서 그리드가 1컬럼으로 내려간다.
- [ ] 표는 `.tbl` wrapper 또는 모바일 안전 구조다.
- [ ] 외부 JS를 사용하지 않는다.
- [ ] 확인되지 않은 최신 정보/수치/가격을 단정하지 않는다.
- [ ] 출처가 많으면 `.source-note`와 source hub로 분리한다.
- [ ] 교육용은 퀴즈와 정답이 있다.
- [ ] 전문가용은 리스크와 검증 기준이 있다.
- [ ] SEO/블로그는 제목, 메타 설명, 태그 또는 키워드가 있다.

## 10. v4.0.0 통합 내역

`adaptive-html-final`은 기존 두 스킬을 합치면서 다음을 적용했습니다.

### 10.1 블로그/SEO 상세 references 흡수

`adaptive-html-blog-writer`의 더 풍부한 reference 4종을 그대로 가져왔습니다.

- `blog-seo-system.md` — SEO 세부 규칙 + Blog Metadata Schema + Blog Quality Score(100점) 추가
- `writing-system.md` — 제목 생성 4계열, 도입부 3유형, 본문 밀도 비율, 톤 매핑 추가
- `platform-system.md` — 플랫폼별(티스토리/벨로그/네이버/워드프레스) 발행 관점 세부 규칙 추가
- `editorial-design-system.md` — 박스 선택 가이드(언제 무엇을), 시각 사고 방지 규칙 추가

### 10.2 접근성 버그 수정 (skip link)

`assets/base.html`의 skip link는 `#main`을 가리킵니다.

```html
<a class="skip" href="#main">본문 바로가기</a>
```

기존에는 7개 레이아웃의 `<main>`에 `id="main"`이 없어 링크가 동작하지 않았습니다. v4에서 **13개 레이아웃 전체**의 `<main>`을 다음과 같이 통일했습니다.

```html
<main id="main" class="page layout-...">
```

### 10.3 SKILL.md 강화

YAML `description`에 **명시적 트리거 목록**과 **기본 출력 원칙**(HTML/블로그 글/스킬 분석별)을 추가해 모드 자동 선택의 정확도를 높였습니다.

### 10.4 이름·메타데이터 일원화

package/디렉토리/manifest/SKILL의 이름을 `adaptive-html-final`로 정렬하고, `merged_from`·`aliases`·`changes`·`updated`를 manifest에 기록했습니다.

## 11. 향후 보강 후보 (선택)

아직 적용하지 않았지만 운영 품질을 더 올릴 수 있는 항목입니다.

- recipes 확장: 현재 6종(audit, beginner, blog, expert, platform, seo) → `reference`, `comparison`, `case-study`, `landing-brief`, `checklist`, `article`, `education` 추가
- 렌더링/검증 스크립트: `scripts/render_html.py`(base+CSS+layout+body 조립), `scripts/validate_skill.py`(manifest 경로·JSON·layout id·h1/meta 검사), `scripts/package_skill.sh`(.skill 재패키징)

## 12. 추천 운영 규칙

1. 모든 HTML 콘텐츠 작업은 `adaptive-html-final` 하나로 호출합니다.
2. 블로그 글 작성은 `blog_writer`, 플랫폼 변환은 `platform_blog`, SEO 설계는 `seo_dashboard`를 명시합니다.
3. 사용자가 "쉽게", "초보자", "비유"라고 하면 `beginner_html`을 사용합니다.
4. 사용자가 "스킬 분석", "SKILL.md 개선", ".skill 통합"이라고 하면 `skill_audit`을 최우선으로 사용합니다.
5. 최신 정보나 URL/PDF가 포함되면 출처 확인을 먼저 하고, 확인 불가 항목은 `확인 필요`로 표시합니다.
6. 결과물은 단일 HTML을 기본으로 하되, 유지보수가 필요하면 assets 연결형으로 생성합니다.
7. 최종 응답에는 선택 모드, 생성 파일, 핵심 구성, 검증 결과만 짧게 보고합니다.

## 13. 빠른 사용 예시 모음

```text
adaptive-html-final로 이 URL을 초보자용 HTML 학습자료로 만들어줘.
```

```text
이 내용을 전문가용 HTML 리포트로 정리해줘. 리스크와 검증 기준을 앞쪽에 배치해줘.
```

```text
이 초안을 티스토리/벨로그/네이버/워드프레스용으로 각각 변환해줘.
```

```text
이 주제의 SEO 대시보드를 만들어줘. 제목 후보 10개와 meta description 3개를 포함해줘.
```

```text
이 SKILL.md를 분석하고 문제점, 개선 우선순위, 최종 개선본까지 만들어줘.
```

```text
이 비교 내용을 comparison_html 모드로 HTML 비교 매트릭스로 만들어줘.
```

## 14. 한 줄 요약

`adaptive-html-final`(v4.0.0)은 13개 모드 라우터와 editorial 디자인 시스템에, 블로그/SEO/플랫폼/박스 선택 상세 규칙까지 흡수하고 skip link 접근성 버그를 수정한 **단일 통합 운영본**입니다.
