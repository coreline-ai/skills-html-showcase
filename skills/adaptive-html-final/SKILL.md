---
name: adaptive-html-final
description: |
  URL, PDF, 텍스트, 이미지 추출문, 메모, 기술 자료, 블로그 초안, SKILL.md/.skill 패키지를 입력받아
  고품질 한국어 HTML 학습자료, 전문가 리포트, 공개 아티클, 교육 모듈, 블로그 원고, SEO 대시보드,
  플랫폼별 블로그 변환, 스킬 감사 리포트, 레퍼런스 매뉴얼, 비교 매트릭스, 케이스 스터디,
  랜딩 브리프, 체크리스트 플레이북, GitHub 저장소 분석 리포트까지 생성하는 최종형 다중 모드 스킬.
  adaptive-html-learning-ultimate의 13개 모드 라우터·레이아웃·평가 루브릭을 뼈대로 삼고 GitHub 분석 모드를 추가한 14개 모드 체계를,
  adaptive-html-blog-writer의 블로그 글쓰기·SEO·플랫폼·박스 선택 상세 규칙을 흡수하고,
  blog-demos급 editorial 디자인 시스템을 유지하고, 필요 시 8000×6000 SVG 인포그래픽 Visual Template System을 섹션별로 배치한다.

  반드시 사용해야 하는 트리거:
  - "HTML로 정리", "초보자용 HTML", "전문가용 HTML", "교육용 HTML", "아티클 HTML", "레퍼런스/매뉴얼 HTML"
  - "블로그 작성", "블로그 글 써줘", "포스팅 작성", "SEO 글", "티스토리/벨로그/네이버/워드프레스용"
  - "비교/장단점/선택 기준", "사례 연구/회고", "랜딩/소개 페이지", "체크리스트/플레이북"
  - "이 문서를 블로그 글로", "이 내용을 글감으로", "제목/도입부/목차/본문/마무리까지"
  - "스킬 분석", "SKILL.md 개선", "한 줄 한 줄 분석", "스킬 통합/감사"
  - "GitHub 저장소 분석", "깃허브 URL 분석", "owner/repo 분석", "README/이슈/릴리스/라이선스 분석"

  기본 출력 원칙:
  - 사용자가 HTML을 원하면 단일 HTML 파일(또는 로컬 assets 연결형)을 만든다.
  - 사용자가 블로그 글을 원하면 Markdown 원고 + SEO 메타 + 필요 시 HTML 버전을 만든다.
  - 사용자가 스킬 분석을 원하면 라인별 진단 + 개선본 SKILL.md를 만든다.
---

# Adaptive HTML Final

> Version 5.3.1 · "완성본 표준화 — 무클래스 섹션 카드뷰·섹션 제목 큰 아이콘·헤더 리듬·source-note·vt-frame 평면을 스킬 기본값으로 승격(회귀 안전)" (이전 5.3.0)

## 0. Identity

이 스킬은 `html-for-beginners` → `adaptive-html-blog-writer` → `adaptive-html-blog-writer-v2` → `adaptive-html-learning-ultimate` 계열을 하나로 합친 최종 통합본이다.
`adaptive-html-learning-ultimate`의 13개 모드 라우터·레이아웃·평가 체계를 뼈대로 두고, GitHub 저장소를 의사결정형 리포트로 바꾸는 `github_analysis`를 14번째 모드로 추가했다. `adaptive-html-blog-writer`의 블로그/SEO/플랫폼/박스 선택 상세 규칙은 references로 흡수했으며, 모든 레이아웃은 skip link 접근성 계약(`id="main"`)을 유지한다.

목표는 단순 HTML 생성이 아니라 다음 파이프라인을 안정적으로 실행하는 것이다.

```text
입력 분석 → 사실/해석/추론 분리 → 독자 수준 판단 → 모드 선택 → 레이아웃 선택
→ 글쓰기/학습/SEO/플랫폼 최적화 → visual brief/이미지 템플릿 판단 → editorial HTML 렌더링 → 품질검수 → 파일/링크 제시
```

## 0.5 Deterministic Operating Spec (harness)

이 스킬은 어떤 에이전트가 실행하든 동일한 입력에 대해 동일한 구조의 출력을 내야 한다(에이전트 무관 재현성). 즉흥적 판단을 줄이고, 아래 결정 규칙과 검증 게이트를 따른다.

**불변식 (절대 위반 금지):**

1. **외부/동작 JS 0.** `<script>`는 `type="application/ld+json"`(JSON-LD)만 허용한다. 그 외 외부 스크립트·인라인 동작 JS·`onclick`/`onload` 등 이벤트 핸들러·`draggable`/`contenteditable` 인터랙션은 금지한다. 인터랙션은 `<details>`/`:checked`/`:target`/CSS 애니메이션으로만 구현한다.
2. **두 위젯 라이브러리는 별개다.**
   - (1) **CSS 뷰 위젯 `wg-01`~`wg-20`** = `assets/widgets.css` + `assets/widget-templates/*.html`. 섹션 보강용 인터랙션 위젯이며 `wg-<id>-` 네임스페이스로 격리된다(Step 4.6).
   - (2) **SVG→HTML 템플릿 `vt-` 21종** = `assets/visual-html.css` + `assets/visual-html-templates/01..21.html`. 본문에 그대로 삽입하는 in-flow 다이어그램(이미지가 아닌 네이티브 HTML 구조도)이다(Step 4.7). 두 라이브러리를 혼동하거나 한쪽으로 대체하지 않는다.
3. **비주얼 프로파일 → 14모드 라우터(§3) 순서가 단일 진입점**이다. (a) 먼저 비주얼 프로파일(`widget`=v5 / `diagram`=v6 / `auto`=기본)을 결정한다 — 인자 `profile=widget|diagram|auto` 또는 별칭 `style=v5|v6`를 `trim→lowercase→정규화`(둘 다 오면 `profile=` 우선, 무효 토큰은 `invalid_profile` 실패). 인자 미지정 시 **비대화형(AGENTS.md 경유 Codex/Gemini)은 무조건 `auto`·질문 금지**, 대화형(Claude 대화)은 1회 질문 가능(결정론 보장은 인자 명시 경로 한정). (b) 이어 모드 선택 → 레이아웃 → 프로파일에 따라 vt-템플릿(diagram·auto)·wg-위젯(widget·auto)을 §0.6에서 고른다. 프로파일이 §0.6 결정표의 **어느 열을 쓸지** 게이트한다(widget=wg 열만/diagram=vt 열만/auto=둘 다).
4. **코어 CSS 인라인 + 해시 마커.** 출력은 `theme.css + components.css + visual-components.css + layouts.css + print.css`를 코어로 인라인하고, 인라인 `<style>`에 `adaptive-html-final-core-css-sha256: <64hex>` 주석 마커를 남긴다. `widgets.css`(위젯 사용 시)와 `visual-html.css`(vt-템플릿 사용 시)는 조건부 인라인이며, 인라인 순서는 §5 Step 5의 합본 순서를 따른다.

**운영 원칙:**

- **즉흥 금지.** 모드별 레이아웃·vt-템플릿·wg-위젯은 아래 결정표를 단일 출처로 사용한다. 임의로 다른 템플릿을 끼워 넣지 않는다.
- **결정표 우선.** §0.6 캐노니컬 결정표가 다른 섹션의 가이드(§4.6, §4.7, references)와 충돌하면 결정표가 1순위다.
- **검증 게이트 필수.** 출력 폴더를 만들면 반드시 `scripts/validate_output.py`를 실행하고 `OK`를 확인한다. 게이트 실패 상태로 완료 처리하지 않는다(§7, §10).

## 0.6 Canonical Decision Table (모드 → layout → vt-템플릿 → wg-위젯)

모드별 결정의 **단일 출처(single source of truth)**다. vt-템플릿 열은 본문 삽입 구조도(`assets/visual-html-templates/`), wg-위젯 열은 CSS 뷰 위젯(`assets/widget-templates/`)이며, 각 열의 **첫 항목이 1순위**다.

| Mode | Layout | vt-템플릿 (1순위→) | wg-위젯 (1순위→) |
|---|---|---|---|
| beginner_html | beginner-learning.html | concept-explainer, hero-map, checklist-flow | wg-10, wg-13, wg-15 |
| expert_html | expert-report.html | risk-matrix, raci, quality-gate, implementation-plan, soft-workflow-map | wg-03, wg-04, wg-11, wg-12, wg-16, wg-17 |
| article_html | magazine-article.html | decision-tree, comparison-cards, concept-explainer | wg-02, wg-04, wg-07, wg-09, wg-10, wg-13, wg-14 |
| education_html | course-module.html | timeline, checklist-flow, concept-explainer, soft-workflow-map | wg-06, wg-07, wg-08, wg-13, wg-14, wg-15, wg-20 |
| github_analysis | github-analysis.html | hero-map, quality-gate, file-tour, risk-matrix, timeline, decision-tree, checklist-flow | wg-11, wg-04, wg-14, wg-16, wg-17, wg-18 |
| blog_writer | personal-blog-essay.html | timeline, weekly-status, comparison-cards | wg-17 |
| seo_dashboard | seo-dashboard.html | card-grid, comparison-cards, prompt-tuner | wg-11 |
| platform_blog | platform-adaptation.html | card-grid, comparison-cards, pr-writeup | wg-02 |
| skill_audit | skill-audit-report.html | quality-gate, file-tour, prompt-tuner, implementation-plan, soft-workflow-map | wg-03, wg-11, wg-17 |
| reference_html | reference-manual.html | file-tour, flowchart, card-grid | wg-04, wg-05, wg-06, wg-14, wg-19, wg-20 |
| comparison_html | comparison-matrix.html | comparison-cards, decision-tree, risk-matrix | wg-01, wg-02 |
| case_study_html | case-study.html | incident-summary, timeline, process-swimlane | wg-12 |
| landing_brief_html | landing-brief.html | hero-map, card-grid, feature-flag, soft-workflow-map | wg-02, wg-05, wg-08, wg-09, wg-16 |
| checklist_playbook | checklist-playbook.html | checklist-flow, quality-gate, process-swimlane, implementation-plan, triage-board | wg-11, wg-13, wg-16, wg-18, wg-19 |

vt-템플릿 파일명은 `assets/visual-html-templates/NN-<name>.html`(NN=01..21)이며, 위 이름은 그 `<name>`과 1:1로 대응한다. `diagram`·`auto` 프로파일 출력은 선택된 모드 행의 **1순위 vt-템플릿을 최소 1회** 삽입한다. `widget`·`auto` 프로파일의 wg-위젯은 구조형 정보가 있을 때만 삽입한다(단순 prose/표로 충분하면 과삽입하지 않는다). 넣을 때는 해당 모드 행의 1순위부터 콘텐츠 적합성 순으로 고른다.

> **프로파일 오버레이(§0.5 프로파일 결정 선행):** 위 표의 **Layout 열은 프로파일과 무관하게 공통**이다. `diagram` 프로파일은 **vt-템플릿 열만**, `widget` 프로파일은 **wg-위젯 열만**, `auto`(기본)는 **두 열 모두** 사용한다. 이 표가 mode→wg / mode→vt 매핑의 **단일 출처**이며, §4.6·§4.7·`references/widget-system.md`·`references/visual-html-system.md`·`AGENTS.md` §3은 이 표의 파생/참조다(불일치 시 §0.6 우선).

## 1. Operating Principles

1. 목적 먼저, 형식은 나중.
2. 단순 요약보다 구조화와 풀어쓰기.
3. 확인되지 않은 사실은 단정하지 않는다.
4. HTML은 단일 파일 또는 로컬 assets 연결형을 우선한다.
5. 공통 editorial 디자인 DNA는 유지하고, 정보 구조는 모드별로 분리한다.
6. 블로그 글은 제목, 메타, 목차, 본문, FAQ/오해, CTA, 태그까지 발행 가능한 수준으로 만든다.
7. 교육 자료는 학습 목표, 예제, 실습, 퀴즈, 정답 해설을 갖춘다.
8. 전문가 리포트는 결론, 리스크, 우선순위, 검증 기준을 첫 화면에 가깝게 둔다.
9. 스킬 감사는 목적, 트리거, 입력/출력, 워크플로우, 품질 게이트, 완료 기준을 평가하고 개선본까지 제시한다.
10. 결과물은 사용자가 복사, 다운로드, 로컬 링크로 확인할 수 있어야 한다.
11. 전문가/감사/레퍼런스 모드는 “요약 카드만 있는 결과물”로 끝내지 말고, 표·RACI·로드맵·체크리스트 등 실행 가능한 상세 근거를 충분히 제공한다.
12. 섹션 이해를 돕는 이미지가 필요하면 장식 사진보다 8000×6000 SVG 인포그래픽을 우선하고, 사진/AI 이미지는 현실성·메타포 목적이 분명할 때만 사용한다.
13. GitHub 저장소 분석은 README 미화가 아니라 사용/채택/감사 의사결정을 돕는 실사 리포트로 작성하며, 관측 사실·추론·확인 불가를 명확히 분리한다.

## 2. Supported Input Types

- URL
- PDF 링크 또는 PDF 파일
- 직접 붙여넣은 텍스트
- 이미지에서 추출한 텍스트
- 메모/아이디어/키워드
- 기존 블로그 초안
- 리서치 노트/기술 문서/제품 문서
- SKILL.md 또는 `.skill` 패키지
- GitHub 저장소 URL(`https://github.com/owner/repo`) 또는 `owner/repo`

입력이 불완전해도 멈추지 않는다. 합리적인 기본값으로 진행하되, 사실 확인이 필요한 내용은 `확인 필요`로 표시한다.

## 3. Mode Router

| Priority | Mode | Trigger | Layout |
|---:|---|---|---|
| 1 | skill_audit | 스킬 분석, SKILL.md 개선, .skill 통합, 한 줄 분석 | skill-audit-report.html |
| 2 | platform_blog | 티스토리, 벨로그, 네이버, 워드프레스, 플랫폼별 | platform-adaptation.html |
| 3 | seo_dashboard | SEO, 제목, 메타, 태그, 검색 의도 | seo-dashboard.html |
| 4 | education_html | 교육, 강의, 온보딩, 실습, 퀴즈 | course-module.html |
| 5 | github_analysis | GitHub 저장소 URL, owner/repo, README/Issues/Releases/License 분석 | github-analysis.html |
| 6 | expert_html | 전문가, 리포트, 진단, 아키텍처, 리스크 | expert-report.html |
| 7 | article_html | 공개 글, 아티클, 기사, GitHub Pages | magazine-article.html |
| 8 | blog_writer | 블로그 글, 포스팅, 경험담, 내 생각 | personal-blog-essay.html |
| 9 | beginner_html | 초보자, 쉽게, 비유로, 입문 | beginner-learning.html |
| 10 | reference_html | 레퍼런스, 매뉴얼, API 문서 | reference-manual.html |
| 11 | comparison_html | 비교, 장단점, 선택 기준 | comparison-matrix.html |
| 12 | case_study_html | 사례 연구, 회고, 프로젝트 기록 | case-study.html |
| 13 | landing_brief_html | 소개 페이지, 랜딩, 요약 페이지 | landing-brief.html |
| 14 | checklist_playbook | 체크리스트, 운영 절차, 플레이북 | checklist-playbook.html |

여러 트리거가 동시에 감지되면 Priority가 높은 모드를 우선한다. 단, 사용자가 명시적으로 특정 모드를 지정하면 그 지시가 우선한다.

트리거 충돌 tie-breaker: 교육/강의 트리거와 공개글 트리거가 겹치면 `education_html`을 우선하고, GitHub 저장소 URL/`owner/repo` 분석이 명확하면 `github_analysis`를 우선한다. 단, GitHub Pages 배포가 단독으로 언급되면 `article_html`을 선택한다.

## 4. Design System

모든 HTML 출력은 현재 editorial design system을 유지한다.

```text
assets/theme.css       = 공통 색상/폰트/폭/분위기
assets/components.css  = 공통 박스/표/코드/태그/하이라이트
assets/visual-components.css = visual-figure/figure-wide/인포그래픽 래퍼
assets/widgets.css     = CSS 뷰 위젯 20종 (wg-<id>- 네임스페이스, 무 JS)
assets/widget-templates/*.html = 뷰 위젯별 삽입 골격 20종
assets/visual-html.css = SVG→HTML 시각 템플릿 21종 스타일 (vt- 네임스페이스, 본문 삽입 in-flow 다이어그램, 무 JS)
assets/visual-html-templates/01..21.html = SVG→HTML 템플릿 삽입 골격 21종 (vt-, 이미지가 아닌 네이티브 구조도; 21=soft-workflow-map)
assets/body-icons.css  = 본문용 compact 아이콘 32종 스타일 (bi- 네임스페이스, aria-hidden 장식, 무 JS) — 프로파일 무관, references/body-icon-system.md
assets/body-icons.json = 본문 아이콘 32종 데이터 (id/label/usage/svg, viewBox 0 0 40 40)
assets/editorial-patterns.css = 본문 구조 패턴 8종 스타일 (chronology·source-preserve·core-insight·connection·before-after·impact-grid·md-excerpt·accessibility-checklist, 무 JS) — 프로파일 무관, references/editorial-pattern-system.md
assets/editorial-pattern-templates/01..08.html = 패턴 삽입 골격 8종 (콘텐츠만 교체)
assets/shape-visuals.css = soft-shape 도형 표시 스타일 (.shape-figure/.shape-lead/.shape-grid, 무 JS) — 프로파일 무관, references/visual-template-system.md
assets/shape-svgs/*.svg = 본문 설명 시작부 보조 도형 36종 (8000×6000 warm SVG, <title>/<desc> 접근성)
assets/shape-catalog.json = 도형 36종 데이터 (id/label/usage)
assets/workflow-visuals.css = soft 워크플로우 도판 표시 스타일 (.workflow-figure ~720px/.workflow-grid, 무 JS) — 프로파일 무관, references/visual-template-system.md
assets/workflow-svgs/*.svg = soft 워크플로우 SVG 도판 10종 (8000×6000, pipeline/hub/router/stack/funnel/graph/swarm/timeline/board/governance)
assets/workflow-catalog.json = 워크플로우 도판 10종 데이터 (id/label/usage)
assets/layouts.css     = 모드별 구조 차이
assets/print.css       = 인쇄 대응
assets/base.html       = 단일 HTML 렌더링 기본 골격
assets/layouts/*.html  = 모드별 골격
visual-templates/*.svg.tpl = 8000×6000 SVG 인포그래픽 템플릿
scripts/render_visual_svg.py = visual brief → SVG 렌더러
```

공개 블로그 품질이 필요하면 `<head>`에 Pretendard Variable + Noto Serif KR 폰트 링크를 포함한다. 오프라인/내부 문서이면 fallback으로도 동작한다.

**SVG vs HTML 시각화 선택 규칙:** 본문 흐름 안에서 읽혀야 하는 구조도(절차·비교·리스크·RACI·타임라인·플로우 등)는 **SVG→HTML 템플릿(`vt-`)**을 쓴다. 이미지가 아니라 텍스트로 검색·복사·반응형이 되는 네이티브 HTML 다이어그램이므로 본문에 그대로 삽입한다(Step 4.7). 반대로 **hero 키비주얼·별첨 도판·다운로드용 한 장 인포그래픽**처럼 문서에서 분리해도 되는 큰 시각물은 `8000×6000` **SVG**(`visual-templates/*.svg.tpl` → `figure.visual-figure > img`)로 만든다(Step 4.5). 한 문서에 둘을 함께 써도 되지만, 본문 구조도를 SVG 이미지로, hero/별첨을 vt-HTML로 뒤바꾸지 않는다.

금지:
- 과한 SaaS 랜딩페이지 스타일
- 무거운 그라디언트와 큰 그림자 남발
- 검정 hero 박스 남발 (`.try` 마지막 CTA 중심)
- 출처 링크 6개 초과 대량 나열
- 외부 JS 의존성
- 본문 가독성을 해치는 다단 레이아웃

## 5. Required Components

골격 컴포넌트 (theme.css / components.css):

```text
.kicker .sub .meta .lead
.pull-quote
```

공통 컴포넌트:

```text
.term .label .word .meaning
.analogy .label
.danger .label .name
.good .label .name
.hero-analogy
.try
.code / pre / code
.table + .tbl
.toc
.faq
.cta-box
.box
.tag / .tag-list
.card-grid / .mini-card
.card-block / .case-label
.prompt-box
.summary-card
.source-note
.hl / .hl.blue / .hl.pink
.h2-sub
.visual-figure / .figure-wide / figcaption
```

## 6. Workflow

### Step 1 — Request Understanding

내부적으로 다음을 정리한다.

```json
{
  "goal": "사용자가 얻고 싶은 최종 결과",
  "mode": "선택된 모드",
  "audience": "초보자/전문가/일반 독자/검색 유입 독자/학습자",
  "platform": "generic/tistory/velog/naver/wordpress/github-pages",
  "format": "html/markdown/both/skill-package",
  "source_type": "url/pdf/text/file/idea/skill",
  "verification_need": "low/medium/high",
  "layout": "selected layout template",
  "visual_need": "none/low/medium/high",
  "visual_strategy": "none/source_image/svg_infographic/ai_concept/hybrid"
}
```

### Step 2 — Source Handling

- URL/PDF/최신 정보가 포함되면 가능한 범위에서 근거를 확인한다.
- 사용자가 붙여넣은 텍스트는 입력 원문으로 취급한다.
- 이미지 OCR 텍스트는 오탈자 가능성을 표시한다.
- SKILL.md/.skill은 구조와 트리거를 먼저 파악한다.
- 아이디어만 있으면 최신 사실을 단정하지 않고 구조 설계 중심으로 작성한다.

### Step 3 — Fact / Opinion / Inference Split

```text
FACT       = 입력 또는 확인 가능한 출처에 직접 있는 사실
OPINION    = 작성자의 해석 또는 관점
INFERENCE  = 주어진 정보에서 합리적으로 추론한 내용
TODO_CHECK = 추가 확인이 필요한 주장
```

블로그/아티클/리포트에서 TODO_CHECK를 사실처럼 쓰지 않는다.

### Step 4 — Content Planning

모드별 필수 블록을 채운다.

- beginner: toc, hero analogy, terms, analogy, danger/good, practice, try
- expert: executive summary, decision cards, operating model/RACI, risk matrix, roadmap, validation checklist. 핵심 표는 최소 5행 이상, 리스크·검증·실행계획은 각각 4개 이상 작성한다.
- article: lead, pull quote, argument, case, takeaway
- education: goals, before start, lesson, example, practice, quiz, answer
- github_analysis: verdict, question toc, repo identity, quickstart readiness, health signals, code/file tour, release/activity timeline, security/license, risk matrix, final decision, next actions, source limits. GitHub UI/REST에서 확인 가능한 FACT와 합리적 INFERENCE, UNKNOWN을 분리하고 각 핵심 판단에 근거 링크/근거 필드를 둔다.
- blog: hook, personal note, view, example, how-to, soft CTA
- seo: primary keyword, SERP preview, title candidates, meta candidates, tag cluster
- platform: original summary, platform cards, comparison table, publish checklist
- skill_audit: purpose, trigger score, workflow score, line/section diagnosis, improved skill
- reference: quick reference, concepts/API, patterns, examples, checklist
- comparison: decision context, matrix, winners, tradeoffs, recommendation
- case study: situation, timeline, decisions, results, lessons
- landing brief: hero, value props, how it works, FAQ, CTA
- checklist: use case, check grid, failure modes, done criteria

### Step 4.5 — Visual Brief Planning (SVG 인포그래픽 — hero/별첨/다운로드 전용)

> **우선순위 (충돌 해소):** 본문에 삽입하는 구조도·다이어그램은 **§0.6 캐노니컬 결정표 + Step 4.7 의 vt- HTML 템플릿이 정본(SoT)**이다. 이 Step 4.5 의 `svg_infographic`·아래 "모드별 기본 템플릿"은 본문 인라인용이 아니라 **hero 한 장 요약·별첨·인쇄/다운로드용 8000×6000 SVG**에만 적용한다. 같은 이름(hero-map·timeline 등)이 두 곳에 나오지만, **본문 삽입 선택은 항상 §0.6 을 따른다.**

섹션 이해를 돕는 시각물이 필요하면 `references/visual-template-system.md`를 읽고 `schemas/visual-brief.schema.json` 형식으로 visual brief를 만든다.

본문 설명 **시작부의 작은 시각 앵커**가 필요하면 같은 문서의 **Soft Shape 도형 36종**(`assets/shape-svgs/<id>.svg`)을 `figure.shape-figure`(또는 `.shape-lead`/`.shape-grid`)로 삽입한다(`assets/shape-visuals.css`, `{{SHAPE_VISUALS_CSS}}` 슬롯, 프로파일 무관). `img.shape-img`에 비어있지 않은 `alt` 필수, figcaption은 선택. 도형은 시각 앵커일 뿐 핵심 정보는 항상 HTML 텍스트로 둔다.

섹션 **상단 대표 도판·랜딩 설명 카드**가 필요하면 **Soft Workflow 도판 10종**(`assets/workflow-svgs/<id>.svg`, pipeline·hub·router·stack·funnel·graph·swarm·timeline·board·governance)을 `figure.workflow-figure`(와이드 ~720px, figcaption 권장)로 삽입한다(`assets/workflow-visuals.css`, `{{WORKFLOW_VISUALS_CSS}}` 슬롯, 프로파일 무관). `wf-` 접두사 금지(vt-21 점유), `workflow-` 풀네임.

경계: 글자 옆 장식=`bi-`(40×40) · 시작부 작은 앵커=soft-shape(420px) · 본문 대표 도판/랜딩 카드=workflow 도판(720px SVG) · 본문 검색가능 구조도=`vt-`(HTML). 상호 비대체이며, 독자가 본문에서 바로 읽어야 하는 절차·비교는 workflow 도판이 아니라 vt-를 쓴다.

기본 판단:

```text
현실 인물·장소·제품·사건 사진이 핵심 → source_image
절차·비교·정책·리스크·학습 구조 → svg_infographic
메타포·컨셉 이미지가 필요하나 사실 이미지가 아님 → ai_concept
여러 섹션에 사진+도식이 모두 필요 → hybrid
```

SVG 인포그래픽 모드별 기본(별첨/hero용 — 본문 삽입은 §0.6 vt- 결정표가 정본):

```text
beginner_html      → hero-map, checklist-flow
expert_html        → hero-map, matrix, timeline, quality-gate
article_html       → hero-map, decision-tree
education_html     → timeline, checklist-flow
github_analysis    → hero-map, file-tour, risk-matrix, quality-gate
blog_writer        → hero-map, timeline
seo_dashboard      → card-grid, matrix
platform_blog      → card-grid, matrix, checklist-flow
skill_audit        → matrix, quality-gate, timeline
reference_html     → card-grid, matrix
comparison_html    → matrix, decision-tree
case_study_html    → timeline, hero-map
landing_brief_html → hero-map, card-grid
checklist_playbook → checklist-flow, quality-gate
```

`svg_infographic`를 선택하면 `visual-templates/*.svg.tpl`와 `scripts/render_visual_svg.py`를 사용해 원본 8000×6000 SVG를 만들고, HTML에는 `figure.visual-figure > img + figcaption` 패턴으로 삽입한다.

### Step 4.6 — View Widget Selection & Insertion

> **프로파일 게이트:** 이 단계는 **`widget`·`auto` 프로파일에서만** 실행한다(`diagram` 프로파일은 생략). CSS 번들에 `widgets.css`가 포함된다(§0.5 invariant 3, AGENTS.md §4).

레이아웃 골격이 정해진 뒤, 섹션 목적에 맞는 뷰 위젯(view widget)을 골라 본문에 삽입한다. 위젯은 `assets/widgets.css`(스킬 디자인 토큰 기반)와 `assets/widget-templates/*.html` 20종으로 제공되며, **외부 JS 없이** 동작한다. 필요할 때만 `references/widget-system.md`를 읽는다.

판단 순서:

1. 섹션이 단순 prose/표/카드로 충분하면 위젯을 넣지 않는다(위젯은 선택적 보강이다).
2. 코드 비교·디자인 시안·diff·아키텍처·타임라인·플로우·트리아지 등 구조형 정보면 적합 위젯 1~2개를 고른다.
3. 위젯은 `wg-<id>-` 네임스페이스 클래스만 쓰고, 마크업은 `assets/widget-templates/NN-*.html` 골격을 복사해 콘텐츠만 바꾼다. `widgets.css`는 `base.html`의 `{{WIDGETS_CSS}}` 슬롯에 합본하거나, 사용한 위젯의 CSS만 인라인한다.
4. 인터랙션은 `<details>/:checked/:target/CSS 애니메이션`만 사용한다. 색 외 단서(아이콘·라벨·테두리)와 포커스 가시성을 함께 유지한다.
5. 완전 인터랙션에 JS가 필요한 위젯(18 칸반, 20 프롬프트 튜너)은 스킬 기본값으로 **무 JS 근사**(정적/`:checked` 상태)로 삽입하고, 실시간 동작은 선택적 점진 향상으로만 남긴다.

인터랙티브 분류(20종): CSS-only 완전 무JS 11종 / CSS 부분 7종 / JS 필요 2종.

모드별 권장 위젯(한 줄 가이드):

```text
comparison_html    → 01 Three Code Approaches, 02 Visual Design Directions
expert_html        → 03 Annotated PR, 04 Module Map, 11 Weekly Status, 12 Incident Timeline, 16 Implementation Plan, 17 PR Writeup
reference_html     → 04 Module Map, 05 Living Design System, 06 Component Variants, 14 Feature Explainer, 19 Feature Flag Editor, 20 Prompt Tuner
education_html     → 06 Component Variants, 07 Animation Sandbox, 08 Clickable Flow, 13 Annotated Flowchart, 14 Feature Explainer, 15 Concept Explainer, 20 Prompt Tuner
github_analysis    → 11 Weekly Status, 04 Module Map, 14 Feature Explainer, 16 Implementation Plan, 17 PR Writeup, 18 Ticket Triage Board
beginner_html      → 10 SVG Figure Sheet, 13 Annotated Flowchart, 15 Concept Explainer
article_html       → 02 Visual Design Directions, 04 Module Map, 07 Animation Sandbox, 09 Slide Deck, 10 SVG Figure Sheet, 13 Annotated Flowchart, 14 Feature Explainer
landing_brief_html → 02 Visual Design Directions, 05 Living Design System, 08 Clickable Flow, 09 Slide Deck, 16 Implementation Plan
seo_dashboard      → 11 Weekly Status
case_study_html    → 12 Incident Timeline
checklist_playbook → 11 Weekly Status, 13 Annotated Flowchart, 16 Implementation Plan, 18 Ticket Triage Board, 19 Feature Flag Editor
skill_audit        → 03 Annotated PR, 11 Weekly Status, 17 PR Writeup
blog_writer        → 17 PR Writeup
platform_blog      → 02 Visual Design Directions
```

### Step 4.7 — SVG→HTML Visual Template Insertion (vt-)

> **프로파일 게이트:** 이 단계는 **`diagram`·`auto` 프로파일에서만** 실행한다(`widget` 프로파일은 생략). CSS 번들에 `visual-html.css`가 포함된다(§0.5 invariant 3, AGENTS.md §4).
> `diagram`·`auto` 출력에서는 선택 모드의 1순위 vt-템플릿을 최소 1회 삽입한다. 후순위 템플릿으로 대체해야 할 때도 §0.6 같은 행의 순서를 따른다.

본문 안에서 읽혀야 하는 구조도는 이미지가 아니라 **SVG→HTML 템플릿(`vt-`)**으로 삽입한다. `assets/visual-html.css`(스킬 디자인 토큰 재사용)와 `assets/visual-html-templates/01..21.html` 21종으로 제공되며, **외부 JS 없이** 동작하는 네이티브 in-flow 다이어그램이다(이미지처럼 분리되지 않고 문서의 일부로 읽힌다). 자세한 규칙은 필요할 때 `references/visual-html-system.md`를 읽는다.

판단 순서:

1. 해당 섹션을 §0.6 캐노니컬 결정표의 vt-템플릿 1순위부터 콘텐츠 적합성 순으로 매칭한다. `diagram`·`auto` 프로파일의 1순위 vt-템플릿은 최소 1회 삽입하며, 후순위 템플릿은 1순위가 해당 섹션 정보 구조에 명백히 부적합할 때만 쓴다.
2. `assets/visual-html-templates/NN-<name>.html` 골격을 복사해 콘텐츠만 바꾼다. `vt-` 네임스페이스 클래스와 템플릿별 짧은 접두사(`hm-`, `dt-`, `rm-` 등)만 사용한다.
3. `visual-html.css`는 `base.html`의 `{{VISUAL_HTML_CSS}}` 슬롯에 합본하거나, 사용한 템플릿의 CSS만 인라인한다(인라인 순서는 Step 5 참고).
4. 인터랙션은 §0.5 불변식과 동일하게 `<details>`/`:checked`/`:target`/CSS 애니메이션만 쓴다. 동작 `<script>`는 0이어야 한다(JSON-LD 제외).
5. hero 키비주얼·별첨 도판·다운로드 한 장 인포그래픽은 vt-가 아니라 `8000×6000` SVG(Step 4.5)로 만든다. 본문 구조도와 hero/별첨의 매체를 뒤바꾸지 않는다(§4 선택 규칙).

vt-템플릿 21종(파일명 `<name>`): hero-map, decision-tree, risk-matrix, timeline, checklist-flow, quality-gate, card-grid, raci, file-tour, flowchart, weekly-status, incident-summary, comparison-cards, process-swimlane, concept-explainer, implementation-plan, pr-writeup, triage-board, feature-flag, prompt-tuner, soft-workflow-map.

### Step 5 — HTML Rendering

1. `assets/base.html` 또는 로컬 CSS 연결형 HTML을 사용한다.
2. 선택된 `assets/layouts/*.html` 골격을 적용한다.
3. CSS는 `theme.css + components.css + visual-components.css + widgets.css(widget·auto) + visual-html.css(diagram·auto) + body-icons.css(본문 아이콘 사용 시) + editorial-patterns.css(본문 패턴 사용 시) + shape-visuals.css(soft-shape 사용 시) + workflow-visuals.css(workflow 도판 사용 시) + layouts.css + print.css + theme-dark.css(3-테마 토큰 오버라이드, 항상)` 순서로 합친다. 코어 해시는 `theme.css + components.css + visual-components.css + layouts.css + print.css` 5종만 대상이며(`theme-dark.css`는 코어 해시 제외, print 뒤 맨끝), `base.html`의 각 CSS 슬롯은 미사용 시 빈 문자열로 치환한다. `base.html`의 `ahf-theme` 라디오 3-세그먼트 스위처는 기본 필수 UI이며 라이트/화이트/다크 전환을 무 JS로 제공한다.
4. 섹션 wrapper와 grid/card wrapper를 분리한다. `section.matrix`, `section.serp-preview`, `section.value-grid`, `section.check-grid`, `section.priority-roadmap` 같은 semantic section에는 `display:grid`를 직접 걸지 말고, 내부에 `.card-grid`, `.grid-2`, `.grid-3`, `.matrix:not(section)` 같은 별도 wrapper를 둔다.
   - `section > h2:first-child`는 내부 top margin이 0이어야 한다. 섹션 간 간격은 `section{margin}`으로 제어하고, 카드 내부 첫 heading의 `margin-top:64px`가 빈 공간을 만들게 두지 않는다.
   - 검정 `.try` 섹션 안에 흰색 `.box`, `.summary-card`, `.cta-box`, `.card-block`, `.mini-card`를 넣으면 반드시 카드 안쪽 텍스트 색을 `var(--ink)`/`var(--ink-soft)`로 되돌린다. `.try p/li{color:#d0d0c8}` 상속이 흰 카드에 새어 들어가면 실패다.
   - `.winners:not(section)`, `.tradeoffs:not(section)`는 h3+ul 구조를 임의 2컬럼 grid로 만들지 않는다. 카드형 block으로 두거나 내부에 별도 `.grid-2`를 둔다.
   - case-study timeline은 section 자체와 내부 timeline card가 동시에 left rule을 갖지 않도록 한다. 순서형 목록 번호가 충분히 보이면 내부 card의 굵은 accent left rule도 쓰지 않는다.
5. `<html lang="ko">`, viewport, title, meta description, h1 1개를 보장한다.
6. 외부 JS 라이브러리를 사용하지 않는다.
7. 표는 필요한 경우에만 사용하고 모바일에서 깨지면 카드로 바꾼다.
   - `<caption>`은 보이는 제목으로 유지한다. 음수 margin, absolute positioning, overflow hidden 등으로 캡션/텍스트를 잘라내지 않는다.
8. Article/Blog/SEO 모드에는 JSON-LD를 추가할 수 있다.
9. 시각 템플릿은 `<figure class="visual-figure"> <img width="8000" height="6000" alt="..."> <figcaption>...</figcaption> </figure>` 구조로 삽입한다.
10. `assets/base.html`은 `{{BODY}}` 다음 줄에 선택적 `{{FOOTER}}` 슬롯을 둔다.
11. 결과 폴더를 만들면 사용한 CSS asset snapshot과 합본 해시를 남긴다. 권장 위치는 `sources/assets/*.css`, `sources/css-integrity.json`, 인라인 CSS 주석 `adaptive-html-final-core-css-sha256: ...`이다.
12. `scripts/validate_output.py <output_dir> --skill-dir <skill_dir>`로 정적 게이트를 실행하고, 가능하면 Playwright 390/1280px 렌더 검증까지 수행한다. 푸터가 필요하면 이 슬롯에 채우고, 불필요하면 비워서 footer 없이 렌더링한다.

### Step 6 — Visual Composition Gate

- 첫 화면은 `kicker → h1 → sub → meta → divider → toc/summary` 흐름을 기본으로 한다.
- 긴 한국어 H1은 42px 이하 느낌으로 유지한다.
- 주요 h2에는 `<p class="h2-sub">...</p>`를 붙인다.
- 본문은 prose 65~75%, box 25~35% 정도가 좋다.
- `.hl`은 글당 2~4개만 사용하고, 색상 박스 안에서는 사용하지 않는다.
- `.hero-analogy`는 흰 카드 + accent border 형태가 기본이다.
- 출처가 많으면 `.source-note`에 요약 + `sources/index.html` 링크를 둔다.
- 주요 섹션의 이미지가 필요하면 장식용 배경보다 `hero-map`, `card-grid`, `matrix`, `timeline`, `quality-gate`, `checklist-flow` 같은 목적형 인포그래픽을 우선한다.

## 7. Quality Gates

```text
[ ] `scripts/validate_output.py`가 OK다(완료 필수 게이트). 외부/동작 JS 0(JSON-LD만 허용).
[ ] 요청 목적과 선택 모드가 §0.6 캐노니컬 결정표(모드→layout→vt-→wg-)와 일치한다.
[ ] 선택 모드의 필수 블록이 모두 있다.
[ ] 공통 디자인 토큰을 임의 변경하지 않았다.
[ ] output HTML이 최신 CSS asset 합본을 사용한다. `sources/css-integrity.json`와 인라인 CSS hash가 현재 skill asset hash와 일치한다.
[ ] h1은 하나다.
[ ] h2/h3 계층이 자연스럽다.
[ ] 주요 h2에 h2-sub 또는 동등한 부제가 있다.
[ ] 모바일 1컬럼 전환이 가능하다.
[ ] 모바일 390px 기준에서 제목, 표 캡션, 카드 텍스트가 잘리지 않는다.
[ ] semantic section wrapper에 grid/card CSS가 직접 적용되지 않는다. h2/h2-sub/body/table은 grid item으로 쪼개지지 않는다.
[ ] `.platform-grid`는 section 자체가 아니라 내부 wrapper에만 적용했다.
[ ] 모든 table에는 visible caption이 있다.
[ ] 4열 이상 모바일 표는 `.mobile-card-table` 또는 동등한 카드형 대체가 있다.
[ ] section/card 내부 첫 h2/h3가 과도한 top margin을 만들지 않는다.
[ ] `.try` 안의 밝은 카드 텍스트가 검정 섹션의 흐린 색을 상속받지 않는다.
[ ] `.try`/`.try.soft-cta` 내부 태그 pill은 충분한 대비로 읽힌다.
[ ] `.try`/`.try.soft-cta` 내부 링크는 충분한 대비로 읽힌다.
[ ] `blog_writer` 본문 section h2에는 번호 badge 또는 동등한 진행 표시가 있다.
[ ] SEO SERP Preview 제목은 literal Google blue/Arial/과대 크기 고정이 아니라 페이지 디자인과 균형을 이룬다.
[ ] `<p class="h2-sub">`가 `</h2>`로 잘못 닫히지 않았다.
[ ] `.winners/.tradeoffs` 같은 의미형 블록이 h3와 ul을 서로 다른 grid column으로 찢지 않는다.
[ ] timeline section과 timeline card의 left rule이 중복되지 않으며, 순서형 목록에는 굵은 accent left rule을 추가하지 않는다.
[ ] 긴 URL/코드/영문 토큰은 `overflow-wrap:anywhere` 등으로 본문 폭을 넘지 않는다.
[ ] 시각 템플릿을 사용한 경우 SVG 원본은 8000×6000 이상이고, `<img width height alt>`와 `<figcaption>`이 있다.
[ ] 시각 템플릿 내부 카드/텍스트가 캔버스 밖으로 나가지 않으며 모바일에서 잘리지 않는다.
[ ] 외부 사진/AI 이미지를 사용한 경우 출처·라이선스·생성 여부를 표시했고 사실 이미지처럼 오해되지 않는다.
[ ] 확인되지 않은 최신 정보/수치/가격을 단정하지 않았다.
[ ] 출처나 메타 정보를 추측하지 않았다.
[ ] 블로그/아티클은 제목, 메타 설명, 태그 또는 키워드가 있다.
[ ] 교육용은 퀴즈와 정답이 있다.
[ ] 전문가용은 executive summary, 운영모델/RACI 또는 동등한 실행 구조, 리스크 매트릭스, 로드맵, 검증 기준이 모두 있다.
[ ] 전문가용은 각 핵심 섹션이 1~2문장 요약만으로 끝나지 않고 의사결정에 필요한 근거·담당·산출물·검증 방법을 포함한다.
[ ] 스킬 감사는 개선본까지 포함한다.
[ ] 출처 대량 목록은 source-note/source hub로 정리했다.
```

## 8. References

필요할 때만 읽는다.

- `references/design-dna.md` — 디자인 토큰 원천
- `references/editorial-design-system.md` — 현재 디자인 DNA와 컴포넌트 규칙
- `references/mode-selection.md` — 14개 모드 라우팅
- `references/layout-system.md` — 레이아웃별 블록
- `references/writing-system.md` — 모드별 글쓰기 원칙
- `references/github-analysis-system.md` — GitHub 저장소 분석 리포트 정보 구조·판단 기준·출처 한계
- `references/blog-seo-system.md` — 제목/메타/SERP/태그
- `references/platform-system.md` — 플랫폼별 변환 규칙
- `references/skill-audit-system.md` — 스킬 감사 기준
- `references/eval-rubric.md` — 0~5점 평가 루브릭
- `references/quality-gates.md` — 최종 검수
- `references/visual-template-system.md` — 8000×6000 SVG 인포그래픽 템플릿 선택·삽입·검수
- `references/visual-html-system.md` — SVG→HTML 시각 템플릿(`vt-`) 21종 선택·삽입·무 JS 인터랙션·검수 (`assets/visual-html.css`, `assets/visual-html-templates/`)
- `references/widget-system.md` — CSS 뷰 위젯 20종 선택·삽입·무 JS 인터랙션·접근성 규칙 (`assets/widgets.css`, `assets/widget-templates/`)

## 9. Output Rules

사용자가 파일 생성을 요청하면 `.html` 파일, 필요 시 `.skill` 패키지 또는 ZIP을 생성한다. 최종 응답에는 선택 모드, 생성 파일/링크, 핵심 변경점, 검증 결과를 짧게 설명한다.

## 10. Completion Criteria

1. 모드와 레이아웃이 명확히 선택되었다.
2. 콘텐츠가 목적별 정보 구조를 따른다.
3. HTML이 독립 실행 가능하거나 로컬 assets 경로가 명확하다.
4. 시각 템플릿을 사용했다면 원본 SVG/이미지 경로, alt, figcaption, 출처 정책이 명확하다.
5. 품질 게이트가 통과되었다.
6. **`scripts/validate_output.py <output_dir> --skill-dir <skill_dir>`를 실행해 결과가 `OK`다.** (외부/동작 JS 0, 코어 CSS 해시 일치, `wg-`/`vt-` 사용 시 해당 CSS 인라인 등 정적 게이트 통과). 게이트가 `FAILED`면 완료가 아니다.
7. 사용자가 다운로드하거나 바로 열 수 있다.
