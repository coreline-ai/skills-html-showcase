# adaptive-html-final 사용 가이드

갱신일: 2026-06-07
대상 스킬: `skills/adaptive-html-final` (**v5.7.0**)

> 이 문서는 현행 운영본 기준 사용 가이드입니다. 결정론 실행 규칙의 단일 출처는 루트 [`AGENTS.md`](AGENTS.md) → [`skills/adaptive-html-final/SKILL.md`](skills/adaptive-html-final/SKILL.md) → `references/*`이며, 충돌 시 그 순서를 따릅니다. v4.x 시점의 리뷰·분석·계획 기록은 [`docs/archive/`](docs/archive/README.md)에 보관되어 있습니다.

## 1. 개요

`adaptive-html-final`은 입력 자료(URL, PDF, 텍스트, 이미지 추출문, 메모, 기술 문서, 블로그 초안, SKILL.md/.skill, GitHub URL, YouTube URL/자막, 매뉴얼 원문)를 받아 **고품질 한국어 HTML 콘텐츠**를 만드는 다중 모드 스킬입니다.

기존 계열을 하나로 합친 최종 통합본입니다.

```text
html-for-beginners
  → adaptive-html-blog-writer        (블로그/SEO/플랫폼 상세 규칙)
  → adaptive-html-blog-writer-v2
  → adaptive-html-learning-ultimate  (13모드 라우터·레이아웃·평가체계)
  → adaptive-html-final              (통합 + GitHub/YouTube/Manual 분석 모드 + 비주얼 프로파일 + 8-테마 + 정적 검증 게이트)  ← 현재 운영본
```

운영 원칙:

1. 기본 HTML 생성·블로그·SEO·플랫폼 변환·스킬 감사를 `adaptive-html-final` 하나로 처리합니다.
2. 16개 모드 라우터가 요청을 자동 분류하고, 모드별 레이아웃·글쓰기 규칙·시각 자산을 적용합니다.
3. **외부/동작 JS는 0**입니다. 인터랙션은 `<details>`/`:checked`/`:target`/CSS 애니메이션으로만 구현하며, `<script>`는 JSON-LD(`type="application/ld+json"`)만 허용합니다.
4. 출처가 확인되지 않은 최신 정보·수치·가격은 단정하지 않고 `확인 필요`로 표시합니다.
5. **완료 기준은 `scripts/validate_output.py`가 `OK`를 내는 것**입니다(§9).

## 2. 패키지 현황

| 항목 | 값 |
|---|---|
| 스킬명 | `adaptive-html-final` |
| version | **`5.7.0`** |
| 디렉토리 | `skills/adaptive-html-final/` |
| 설치용 패키지 | `skills/adaptive-html-final.skill` |
| 파일 수 | 90개+ |
| 모드 수 | 16개 |
| 레이아웃 수 | 16개 |
| CSS 자산 | 12개 + `base.html` 템플릿 |
| 비주얼 프로파일 | `widget`(v5) · `diagram`(v6) · `auto`(기본) |
| 테마 | `light` · `light2` · `white` · `dark` · `dark2` · `blue` · `skyblue` · `sepia` — CSS-only 라디오 스위처 |
| vt- SVG→HTML 템플릿 | 21종 |
| wg- 뷰 위젯 | 20종 |
| 본문 시각 자산 | body-icon 32 · editorial-pattern 8 · soft-shape 36 · workflow 도판 10 |
| references | 18종 |
| recipes | 16종 (모드 16/16 완비) |
| schemas | 3종 (blog-meta, quality-report, visual-brief) |
| 스크립트 | `validate_output.py`(정적 게이트), `render_visual_svg.py`(SVG 렌더러) |
| aliases | `adaptive-html-learning-ultimate`, `adaptive-html-blog-writer-v2` |

> 기존 `adaptive-html-learning-ultimate`·`adaptive-html-blog-writer`는 본 스킬에 통합되었고, 두 이름은 manifest의 `aliases`·`merged_from`에 이력으로 보존됩니다.

## 3. 핵심 구조

```text
SKILL.md                       # 라우터, 워크플로우, 불변식, 품질 게이트 (단일 출처)
manifest.json                  # 이름/버전/assets/layouts/modes/profiles/theme_system
README.md / CHANGELOG.md       # 스킬 요약 / 전체 변경 이력
assets/base.html               # 단일 HTML 렌더 골격 (skip link + CSS 슬롯 11종 + {{FOOTER}})
assets/theme.css               # 색상/폰트/폭/타이포 (코어)
assets/components.css          # term/analogy/danger/good/try/table 등 공통 컴포넌트 (코어)
assets/visual-components.css   # visual-figure/figure-wide 래퍼 (코어)
assets/layouts.css             # 모드별 그리드·구조 (코어)
assets/print.css               # 인쇄 대응 (코어)
assets/theme-dark.css          # 8-테마 토큰 오버라이드 (항상 인라인, 코어 해시 제외, print 뒤 맨끝)
assets/widgets.css             # CSS 뷰 위젯 20종 (wg- 네임스페이스, widget/auto 프로파일)
assets/visual-html.css         # SVG→HTML 템플릿 21종 (vt- 네임스페이스, diagram/auto 프로파일)
assets/body-icons.css(.json)   # 본문 compact 아이콘 32종 (bi-, aria-hidden 장식)
assets/editorial-patterns.css  # 본문 구조 패턴 8종 (chronology·core-insight·before-after 등)
assets/shape-visuals.css       # soft-shape 도형 36종 앵커 (8000×6000 SVG)
assets/workflow-visuals.css    # soft 워크플로우 도판 10종 (8000×6000 SVG, ~720px)
assets/layouts/*.html          # 16개 모드별 HTML 골격 (모두 <main id="main">)
assets/widget-templates/*.html       # wg- 위젯 삽입 골격 20종
assets/visual-html-templates/*.html   # vt- 템플릿 삽입 골격 21종
assets/editorial-pattern-templates/*.html  # 패턴 골격 8종
references/*.md                # 필요할 때만 읽는 세부 규칙 (18종)
recipes/*.prompt.md            # 모드별 대표 프롬프트 (16종)
schemas/*.json                 # blog-meta / quality-report / visual-brief
tests/*                        # 품질/레이아웃/접근성/위젯/시각 회귀 체크리스트 + governance 테스트
scripts/validate_output.py     # 정적 품질 게이트 (완료 필수, stdlib-only)
scripts/render_visual_svg.py   # visual brief → 8000×6000 SVG 렌더러
examples/*.html                # 모드별 예시 결과물 (16종 + index)
```

## 4. 동작 파이프라인

단순 HTML 변환기가 아니라 다음 순서로 결과물을 만듭니다.

```text
입력 분석
→ 사실 / 해석 / 추론 / 확인 필요 분리
→ 독자 수준 판단
→ 비주얼 프로파일 결정 (widget / diagram / auto)   ← §5
→ 모드 선택 (16모드 라우터)                          ← §6
→ 레이아웃 선택
→ 글쓰기·학습·SEO·플랫폼 최적화
→ 시각 자산 배치 (vt-/wg- · body-icon · shape · workflow · SVG 인포그래픽)
→ editorial HTML 렌더링 (CSS 합본 + 코어 해시 마커)
→ 정적 품질 게이트 검수 (validate_output.py → OK)
→ 파일/링크 제시
```

중요 원칙:

- 확인되지 않은 최신 정보·가격·수치·정책은 단정하지 않습니다.
- HTML 요청 시 단일 HTML 또는 로컬 assets 연결형 HTML을 생성합니다.
- 외부/동작 JS는 0(JSON-LD만 허용).
- 공개 블로그 품질이 필요하면 Pretendard Variable + Noto Serif KR 폰트를 사용합니다.
- 결과물은 `lang="ko"`, viewport, title, meta description, h1 1개를 보장합니다.

## 5. 비주얼 프로파일 (widget / diagram / auto)

코어(16모드·레이아웃·코어 CSS)는 공유하되, 프로파일이 **어떤 시각 라이브러리를 쓸지** 게이트합니다.

| 프로파일 | 별칭 | 쓰는 라이브러리 | CSS 번들 추가 | 삽입 단계 |
|---|---|---|---|---|
| `widget` | `v5` | wg- 뷰 위젯 20종만 | `widgets.css` | Step 4.6 |
| `diagram` | `v6` | vt- SVG→HTML 템플릿 21종만 | `visual-html.css` | Step 4.7 |
| `auto` | (기본) | 둘 다 | `widgets.css` + `visual-html.css` | 4.6 + 4.7 |

- 인자 지정: `profile=widget|diagram|auto` 또는 별칭 `style=v5|v6` (`trim→lowercase→정규화`, `profile=` 우선, 무효 토큰은 `invalid_profile` 실패).
- 미지정 시: **비대화형(AGENTS.md 경유 Codex/Gemini)은 무조건 `auto`·질문 금지**, 대화형(Claude 대화)은 1회 질문 가능.
- 검증기는 `--profile`로 교차 누수를 차단합니다(`diagram`에 `wg-` 마크업 0, `widget`에 `vt-` 마크업 0).
- 모드→vt-/wg- 매핑의 **단일 출처는 SKILL.md §0.6 캐노니컬 결정표**입니다.

> **vt- vs SVG 인포그래픽**: 본문에서 읽혀야 하는 구조도(절차·비교·리스크·RACI·타임라인·플로우)는 `vt-`(네이티브 HTML, 검색·복사·반응형). hero 키비주얼·별첨·다운로드용 한 장 인포그래픽은 8000×6000 SVG(`figure.visual-figure > img`). 둘을 뒤바꾸지 않습니다.

## 6. 16개 모드 사용표

| 우선순위 | 모드 | 언제 쓰나 | 레이아웃 |
|---:|---|---|---|
| 1 | `skill_audit` | SKILL.md/.skill 분석, 개선, 통합, 한 줄 분석 | `skill-audit-report.html` |
| 2 | `platform_blog` | 티스토리, 벨로그, 네이버, 워드프레스 변환 | `platform-adaptation.html` |
| 3 | `seo_dashboard` | SEO 제목, 메타, 태그, 검색 의도 설계 | `seo-dashboard.html` |
| 4 | `education_html` | 강의, 온보딩, 실습, 퀴즈 | `course-module.html` |
| 5 | `github_analysis` | GitHub 저장소 URL/owner/repo 분석, README·이슈·릴리스·라이선스 실사 | `github-analysis.html` |
| 6 | `youtube_analysis` | YouTube URL/자막/댓글 발췌 분석, 타임스탬프 근거, 주장 위험, 재사용 전략 | `youtube-analysis.html` |
| 7 | `manual_analysis` | 제품/운영 매뉴얼 분석, 역할별 실행 경로, 안전 조건, 트러블슈팅 | `manual-analysis.html` |
| 8 | `expert_html` | 전문가 리포트, 아키텍처, 리스크 진단 | `expert-report.html` |
| 9 | `article_html` | 공개 아티클, 매거진형 글, GitHub Pages 글 | `magazine-article.html` |
| 10 | `blog_writer` | 블로그 글, 포스팅, 경험담, 관점 글 | `personal-blog-essay.html` |
| 11 | `beginner_html` | 초보자용 설명, 비유, 용어 풀이 | `beginner-learning.html` |
| 12 | `reference_html` | 레퍼런스, API 문서, 치트시트, 옵션표 | `reference-manual.html` |
| 13 | `comparison_html` | 비교, 장단점, 선택 기준 | `comparison-matrix.html` |
| 14 | `case_study_html` | 사례 연구, 회고, 프로젝트 기록 | `case-study.html` |
| 15 | `landing_brief_html` | 소개 페이지, 랜딩, 요약 페이지 | `landing-brief.html` |
| 16 | `checklist_playbook` | 체크리스트, 운영 절차, 플레이북 | `checklist-playbook.html` |

여러 트리거가 동시에 들어오면 우선순위가 높은 모드를 선택합니다. 사용자가 모드를 명시하면 사용자 지시가 우선입니다. tie-breaker: 교육/강의 + 공개글이 겹치면 `education_html` 우선, GitHub 저장소 URL/`owner/repo` 분석이면 `github_analysis` 우선, YouTube URL/자막/댓글 분석이면 `youtube_analysis` 우선, 매뉴얼 제작·분석·트러블슈팅이면 `manual_analysis` 우선, GitHub Pages 배포가 단독 언급되면 `article_html`.

## 7. 가장 좋은 요청 템플릿

```text
[입력 자료/URL/파일/주제]를 [목적/독자]용 [모드]로 만들어줘.
출력은 [단일 HTML/Markdown+HTML/플랫폼별 원고]로, 프로파일은 [widget/diagram/auto]로 해줘.
반드시 포함: [목차, 용어 풀이, 예시, 리스크, FAQ, CTA 등]
주의: [최신 정보는 확인 필요 표시, 외부 JS 금지, 모바일 안전 표 등]
저장 위치/파일명: [원하는 경로]
```

예시:

```text
이 문서를 초보자용 HTML 학습자료로 만들어줘. 프로파일은 auto.
전문 용어는 용어 박스로 풀고, 일상 비유, 함정/해결, 마지막 실습 체크리스트를 넣어줘.
단일 HTML 파일로 저장해줘.
```

## 8. 모드별 예시 프롬프트

각 모드의 완성형 프롬프트는 `skills/adaptive-html-final/recipes/*.prompt.md` 16종에 정리되어 있습니다. 대표 예시:

### 초보자 학습자료

```text
Docker 개념을 beginner_html 모드로 HTML 학습자료로 만들어줘.
목차, 핵심 비유, 용어 박스, 흔한 오해, 실습 체크리스트를 포함해줘.
```

### 전문가 리포트

```text
이 아키텍처 메모를 expert_html 모드로 전문가 리포트 HTML로 정리해줘.
Executive Summary, 운영모델/RACI, 리스크 매트릭스(4개+), 우선순위 로드맵, 검증 체크리스트를 포함해줘.
핵심 표는 5행 이상으로.
```

### GitHub 저장소 분석

```text
https://github.com/coreline-ai/skills-html-showcase 저장소를 github_analysis 모드로 분석해줘.
사용자가 가장 궁금해할 질문 중심 목차, quickstart 가능성, 파일 투어, 유지보수 신호, 라이선스/보안 리스크, 다음 행동 체크리스트를 포함해줘.
FACT / INFERENCE / UNKNOWN을 분리하고 단일 HTML로 저장해줘.
```

### YouTube 영상 분석

```text
이 YouTube URL/자막을 youtube_analysis 모드로 분석해줘.
타임스탬프별 Video Evidence Map, FACT/INFERENCE/UNKNOWN, 댓글 반복 신호, Claim Risk, 재사용 패키지를 포함해줘.
iframe/embed 없이 단일 HTML로 저장해줘.
```

### 매뉴얼 분석

```text
이 제품 설명서와 FAQ를 manual_analysis 모드로 HTML 매뉴얼로 재구성해줘.
Source & Version Snapshot, Reader Role Router, First Success Path, Prerequisites/Safety, Troubleshooting, Operations Runbook을 포함해줘.
오래된 내용은 원문 위치와 확인 불가로 표시해줘.
```

### 블로그 글

```text
이 주제로 blog_writer 모드 블로그 글을 작성해줘.
제목 후보 8개, 추천 제목, 메타 설명, 목차, 본문, FAQ, CTA, 태그를 포함해줘. 필요하면 HTML 버전도.
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

### 비교 매트릭스 / 운영 체크리스트

```text
A/B/C 도구를 comparison_html 모드로 비교 HTML로. 선택 기준, 장단점, 추천 상황, 최종 의사결정 표 포함.
배포 전 점검 절차를 checklist_playbook 모드로 HTML 플레이북으로. 체크 그리드, 실패 모드, 완료 기준 포함.
```

## 9. HTML 생성 시 내부 사용법 + 검증

스킬을 직접 운용할 때 순서:

1. 비주얼 프로파일을 결정합니다(`widget`/`diagram`/`auto`). 비대화형이면 `auto`.
2. `SKILL.md` §3 라우터로 모드를, §0.6 캐노니컬 결정표로 레이아웃·vt-·wg-를 고릅니다.
3. 필요할 때만 `references/*.md`를 추가로 읽습니다.
4. 해당 모드의 `assets/layouts/*.html` 골격을 선택하고 `assets/base.html`에 삽입합니다.
5. CSS는 다음 순서로 합칩니다.
   `theme → components → visual-components → widgets(widget/auto) → visual-html(diagram/auto) → body-icons(사용 시) → editorial-patterns(사용 시) → shape-visuals(사용 시) → workflow-visuals(사용 시) → layouts → print → theme-dark(항상, 맨끝)`
   - **코어 해시 대상은 5종**(`theme + components + visual-components + layouts + print`)이며, 인라인 `<style>`에 `adaptive-html-final-core-css-sha256: <64hex>` 마커를 남깁니다. `theme-dark.css`는 해시 제외.
6. 공개 블로그면 title/meta/OG/JSON-LD 후보를 넣습니다.
7. 결과 폴더를 만들면 `sources/assets/*.css` 스냅샷, `sources/css-integrity.json`, `sources/adaptive-html-final-manifest.json`을 남깁니다.
8. **정적 게이트를 실행합니다(완료 필수):**

```bash
# cwd = 저장소 루트
python3 skills/adaptive-html-final/scripts/validate_output.py \
  <output_dir> \
  --skill-dir skills/adaptive-html-final --profile <widget|diagram|auto>
```

마지막 줄이 `OK`여야만 완료입니다. `FAILED`/`ISSUE`면 수정 후 재실행하고, 상세가 필요하면 `--json`을 붙입니다.

관련 references: `editorial-design-system.md`(디자인 DNA·박스 선택), `writing-system.md`(제목·도입부·밀도·톤), `blog-seo-system.md`(메타·SERP·태그·점수), `platform-system.md`, `visual-html-system.md`(vt-), `widget-system.md`(wg-), `visual-template-system.md`(SVG·shape·workflow), `body-icon-system.md`, `editorial-pattern-system.md`, `mode-selection.md`, `layout-system.md`, `skill-audit-system.md`, `eval-rubric.md`, `quality-gates.md`, `design-dna.md`.

## 9.5. HTML → PDF/PNG/WebP export

`scripts/export_output.mjs`는 검증 완료된 HTML 산출물을 공유·인쇄·썸네일용 파일로 변환하는 **빌드 타임 보조 도구**입니다. 스킬 본체와 출력 HTML을 수정하지 않으며, export 전후 HTML SHA와 `validate_output.py --json` 이슈 불변성을 `exports/export-manifest.json`에 기록합니다.

동일 절차를 다른 저장소에서 재사용할 때는 별도 스킬 [`skills/html-exporter`](skills/html-exporter/)를 사용합니다.

```bash
# 최초 1회
npm install

# 기본: pdf,png,webp + light,light2,white,dark,dark2,blue,skyblue,sepia 요청
node scripts/export_output.mjs output/final_20260604 --clean

# 특정 포맷/테마만
node scripts/export_output.mjs output/final_20260604 \
  --formats pdf,png \
  --themes light,dark \
  --scale 1 \
  --viewport 1280x900
```

| 구분 | v1 결정 |
|---|---|
| 렌더 엔진 | Node Playwright Chromium. `:has()` 기반 테마·인라인 CSS·대형 SVG 때문에 비-Chromium 변환기는 사용하지 않습니다 |
| 출력 위치 | `<output_dir>/exports/pdf`, `exports/png`, `exports/webp`, `exports/export-manifest.json` |
| 테마 | `light,light2,white,dark,dark2,blue,skyblue,sepia`를 요청하되 DOM radio가 없는 테마는 skip으로 기록 |
| PNG | full-page screenshot. `--scale` 요청값은 페이지 높이에 따라 `scale_used`로 자동 강등될 수 있습니다 |
| WebP | PNG master에서 `sharp`로 파생. 긴 변 16383px 초과 시 WebP만 downscale, PNG master는 보존 |
| PDF | fresh page/context에서 print PDF 1종 생성, controls/themebar는 export에서 숨김 |
| 안전성 | `output/` 내부 디렉터리만 허용, `--clean`은 요청 포맷 export 디렉터리만 삭제, symlink는 거부 |

v1 허용 옵션은 `--formats`, `--themes`, `--scale`, `--viewport`, `--require-webp`, `--clean`뿐입니다. `--pdf-media`, `--pdf-themes`, `--show-controls`, `--concurrency`, `--webp-mode`, `--offline`, `--strict-fonts` 등은 v2 reserve라 v1에서는 `not implemented in v1`과 함께 exit 2로 종료합니다.

## 10. 품질 게이트 요약

`validate_output.py`가 자동 강제하는 핵심 + 수동 점검 항목(전체 35항목은 SKILL.md §7):

- [ ] `validate_output.py`가 `OK`. **외부/동작 JS 0**(JSON-LD만 허용).
- [ ] 선택 모드가 §0.6 캐노니컬 결정표(모드→layout→vt-→wg-)와 일치.
- [ ] 코어 CSS 해시 마커가 현재 skill asset 해시와 일치(`css-integrity.json` 포함).
- [ ] 프로파일 교차 누수 0(`diagram`에 wg-, `widget`에 vt- 마크업 없음).
- [ ] `lang="ko"`, viewport, title, meta description, h1 1개, `<main id="main">`.
- [ ] 주요 h2에 `.h2-sub` 또는 동등 부제.
- [ ] 모바일 390px에서 제목·표 캡션·카드 텍스트가 잘리지 않음. 4열+ 표는 `.mobile-card-table` 등 카드형 대체.
- [ ] semantic section에 grid/card CSS를 직접 걸지 않음. 모든 table에 visible `<caption>`.
- [ ] 시각 템플릿 SVG는 8000×6000 이상, `<img width height alt>` + `<figcaption>`.
- [ ] 교육용=퀴즈/정답, 전문가용=executive summary·운영모델/RACI·리스크·로드맵·검증 기준, SEO/블로그=제목·메타·태그.
- [ ] 확인되지 않은 최신 정보/수치/가격을 단정하지 않음.

## 11. 빌드 완성도 기준선 (Canonical Baseline)

현재 스킬 v5.7.0 기준으로 15·16 신규 모드의 smoke 산출물은 정적 품질 게이트를 통과했습니다. 기존 13-topic 캐노니컬 산출물은 v5.2.3 기준선으로 보존합니다:

```text
output/adaptive-html-final-13-topics-20260605_083433/   (v5.2.3 기준선, HTML 14개, 게이트 OK)
output/youtube-analysis-vibecoding-gap-20260607_001503/      (v5.7.0 youtube_analysis, 게이트 OK)
output/manual-analysis-product-runbook-20260607_001503/      (v5.7.0 manual_analysis, 게이트 OK)
```

13-topic 디렉토리는 13개 토픽을 v5.2.3의 강력한 정적 게이트(코어 해시·교차 누수·무 JS·접근성·모바일 안전 표·시각 자산 계약)에 맞춰 빌드한 **빌드 완성도 검증 기준선**입니다. 신규 산출물을 만들 때는 이 구조(`sources/` 스냅샷 + `css-integrity.json` + 코어 해시 마커)를 따르고, 게이트 `OK`를 완료 기준으로 삼습니다.

> 참고: v4~v5.0 시점에 생성된 일부 `output/`·`examples/`는 그 사이 코어 CSS가 진화하면서 해시가 드리프트해 현재 게이트에서 `FAILED`가 날 수 있습니다(시점 고정 산출물). 최신 신규 모드 smoke 기준선은 위 2개 output 디렉토리이며, 전체 16-mode 갤러리 재생성은 별도 릴리스 작업입니다.

## 12. 추천 운영 규칙

1. 모든 HTML 콘텐츠 작업은 `adaptive-html-final` 하나로 호출합니다.
2. 블로그=`blog_writer`, 플랫폼 변환=`platform_blog`, SEO 설계=`seo_dashboard`, 스킬 분석=`skill_audit`(최우선)을 명시합니다.
3. "쉽게/초보자/비유"는 `beginner_html`.
4. 최신 정보·URL·PDF가 포함되면 출처를 먼저 확인하고, 불가 항목은 `확인 필요`로 표시합니다.
5. 결과물은 단일 HTML 기본, 유지보수가 필요하면 assets 연결형.
6. **출력 폴더를 만들면 반드시 `validate_output.py`로 `OK`를 확인합니다.**
7. 최종 응답에는 선택 모드·프로파일·생성 파일·핵심 구성·검증 결과만 짧게 보고합니다.

## 13. 한 줄 요약

`adaptive-html-final`(**v5.7.0**)은 16개 모드 라우터 + editorial 디자인 시스템에 **비주얼 프로파일(widget·diagram·auto)·8-테마·vt-/wg- 시각 라이브러리·정적 품질 게이트**까지 갖춘, 외부 JS 0의 결정론적 단일 통합 운영본입니다.
