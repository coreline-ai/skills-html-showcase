# adaptive-html-final 정밀 분석 보고서

> 분석 방식: 7개 전문가 에이전트 병렬 분해 → 쟁점 적대적 검증(critical/high/medium 32건 독립 재확인, 오탐 0) → 교차 통합 감사 → 종합 정리
> 분석 대상: `skills/adaptive-html-final` (v4.0.0, 51개 파일)
> 작성일: 2026-05-30

## 1. 총평 (Executive Summary)

adaptive-html-final v4.0.0은 13개 모드 라우터, editorial 디자인 시스템, 6단계 워크플로우, 품질 게이트를 갖춘 잘 구조화된 통합 스킬이며, 핵심 셀링포인트인 skip link 접근성 수정(`<main id="main">` 13/13)은 적대적 검증으로 완전히 입증되었다(외부 JS 0건, h1 단일 원칙 13/13, manifest↔디스크 layouts 차집합 0도 함께 확인). 7개 영역에서 총 32건의 지적이 모두 confirmed/partial로 사실 확인되었고 false_positive로 완전 기각된 건은 없었으나, 적대적 검증 과정에서 원지적의 심각도가 대거 하향 조정되었다 — 당초 critical 1·high 7 중 검증 후 critical 0·high 0으로, 실제 동작 결함은 없고 대부분이 문서 정합성·QA 커버리지·디자인 시스템 완성도 수준의 개선 과제로 판명되었다. 가장 실질적인 약점은 (1) v4 핵심 수정사항이 테스트에서 회귀 무방비라는 점, (2) manifest와 라우터 모드 ID가 11/13 표기 불일치, (3) 레이아웃 참조 CSS 클래스 39개 미정의, (4) quality-checklist가 SKILL.md 게이트 9개+ 누락이다. 다만 examples가 asset CSS를 link하지 않고 인라인 `<style>`을 쓰기 때문에 미정의 클래스·`.tbl` 미사용 등이 실제 산출물 렌더 파손을 일으키지는 않는다. **전체 성숙도 점수: 78/100 — 기능적으로 견고하고 핵심 접근성 수정이 입증된 출시 가능 수준이나, 메타데이터 정합성·테스트 커버리지·디자인 토큰 완성도에서 후속 정리가 필요한 상태다.**

## 2. 패키지 개요

| 항목 | 수치/구성 | 검증 상태 |
|---|---|---|
| 스킬명 / 버전 | adaptive-html-final / 4.0.0 | manifest·SKILL 일치 (OK) |
| 모드 라우터 | 13개 (P1 skill_audit ~ P13 checklist_playbook) | 라우터·layout-system·디스크 13/13 |
| 레이아웃 템플릿 | 13개 (manifest == 디스크 == 라우터, 차집합 0) | pass |
| CSS 파일 | 4개 (theme 3753B, components 7175B, layouts 4738B, print 372B) | !important 0건 |
| references | 디스크 10개 / SKILL.md §8 인용 9개 | design-dna.md 미인용 |
| recipes | 6개 (audit/beginner/blog/expert/platform/seo) | 6/13 커버 |
| schemas | 2개 (blog-meta, quality-report), Draft 2020-12 통과 | $schema/$id/title 0/2 |
| tests | 4개 마크다운 체크리스트 (~50줄, 자동화 0%) | 수동 전용 |
| examples | 8개 HTML + index (인라인 CSS, 외부 JS 0) | 핵심 게이트 8/8 통과 |
| skip link id=main | 13/13 + base.html:23 `href="#main"` | 검증 완료 |
| 확정 이슈 | critical 0 · high 0 · medium 8 · low 11 | 검증 후 재산정 |

## 3. 영역별 정밀 분석

### 3.1 SKILL.md 오케스트레이션

**강점**
- 모드 우선순위 충돌 해소 규칙이 명시적(`SKILL.md:84` "Priority 높은 모드 우선, 단 명시 지정 시 사용자 지시 우선"), `references/mode-selection.md:19`와 일관.
- skip link 수정 주장이 13/13 실증(`base.html:23 href="#main"` ↔ 모든 레이아웃 `id="main"`).
- CSS 결합 순서(theme→components→layouts→print)·폰트 링크가 Step5·Section4 주장과 정확히 일치(`base.html:14-18`).
- Fact/Opinion/Inference/TODO_CHECK 분리로 환각 억제 설계가 견고(`SKILL.md:159-168` + 운영원칙).

**문제점**
| severity | 문제 | file:line | 수정안 |
|---|---|---|---|
| medium | manifest.modes와 라우터 모드 ID가 11/13 표기 불일치(통합 이슈) | `SKILL.md:70-82` vs `manifest.json:28-42` | 단일 ID 규약으로 통일 |
| medium | quality-checklist가 SKILL Gates 9개+ 미반영(통합 이슈) | `SKILL.md:213-228` | 1:1 매핑 재작성 |
| low | Required Components(§5)에 `.faq/.cta-box/.box` 누락 — landing_brief 필수 FAQ와 자기모순 | `SKILL.md:109-131` vs `components.css:2`, `landing-brief.html:7` | §5에 추가, `.kicker/.sub/.meta/.lead/.pull-quote` 골격 컴포넌트도 보완 |
| low | design-dna.md가 §8 References에서 누락 | `SKILL.md:235-243` | 추가 또는 editorial-design-system.md로 통합 |
| low | `SKILL.md:208`이 비존재 `sources/index.html`을 링크 타깃으로 지시 | `SKILL.md:208` (+`editorial-design-system.md:84`, `layout-checklist.md:14`) | 일반화('source hub') 또는 실제 생성 |
| low | 트리거 키워드 교차 분산(GitHub Pages/블로그) — 라우팅 모호성 | `SKILL.md:75-76` | tie-breaker 본문 노출 |
| low | 품질 게이트 일부가 측정 불가 정성 표현('느낌','자연스럽다') | `SKILL.md:203,205,217` | CSS clamp 상한 준수 등으로 치환 |
| low | description frontmatter 장문(~870자, 1745는 바이트 오측정) | `SKILL.md:3-23` | 핵심 1~2문장 + 대표 트리거로 압축 |

> 검증 정정: 원지적의 sources 경로(high)·키워드 분산(medium)·description(medium)·정성기준(medium)은 라인오기·바이트 오측정·예제 반증 등으로 모두 low 하향. `SKILL.md:99`는 공개/오프라인 폰트 규칙을 이미 명시하고 있어 관련 처방 일부는 충족 상태.

### 3.2 CSS 디자인 시스템

**강점**
- 디자인 토큰을 `:root`에 색/폰트/반경/폭으로 체계 분리, 컴포넌트가 일관되게 `var()` 참조(`theme.css:1-32`).
- `!important` 0건(전 파일) — 우선순위를 selector 구조로만 해결.
- 반응형 1컬럼 전환이 모든 멀티컬럼 그리드에 빠짐없이 정의(`components.css:77-82`, `layouts.css:33,49`).
- 한글 가독성 배려: `word-break:keep-all`, `line-height:1.8`, `clamp()` 반응형 타이포.

**문제점**
| severity | 문제 | file:line | 수정안 |
|---|---|---|---|
| medium | `.tbl` 가로스크롤 래퍼 정의만 되고 미사용 — `min-width:420px` 표가 <430px에서 페이지 가로 오버플로 | `components.css:60-61`; 실사용 0건 | 산출물에서 `<div class="tbl">` 강제, 빌드에 bare-table 검출 게이트 |
| medium | 키보드 포커스 가시성 부재 — `:focus-visible` 0건 (`.skip:focus`만) | `theme.css:45-48` | `a/summary/[tabindex]:focus-visible{outline:2px solid var(--accent)}` 추가 |
| low | `prefers-reduced-motion`이 `scroll-behavior:smooth` 미해제 (실 영향=skip 링크 1곳) | `theme.css:34`, `components.css:54` | `@media(reduced-motion){html{scroll-behavior:auto}}` |
| low | 박스 글자색·강조보더 raw hex 산재(토큰화 안 됨) | `components.css:19-35` | `--term-ink/--analogy-ink` 등 토큰화 |
| low | AA(4.5:1) 대비 경계미달: `.term .label` 4.18:1, `.meta/.tag` ~4.1:1, `.danger .label` 3.76:1 | `components.css:20,58`, `theme.css:58` | 전경색 한 단계 진하게(#8a5e10/#6a6a6a 검증됨) |
| low | print.css에 `print-color-adjust`·페이지나눔 누락 | `print.css:1-8` | `*{print-color-adjust:exact}`, `pre/table/.tbl/blockquote{break-inside:avoid}`, `.skip{display:none}` |
| (참고) | Google Fonts preconnect 누락, `.lead` 중복 선언, `.page-wide` 데드 토큰 의심 | `base.html:11-13`, `theme.css:54-55,31/50` | 점진 개선 |

> 검증 정정: 원지적 high 2건(`.tbl`, 포커스)은 모두 confirmed이나 medium 하향 — UA 기본 포커스링이 살아있고(`outline:none` 미사용) `.tbl` 영향은 폭 넓은 표 포함 <430px 화면에 국한. 단, layouts/*.html에는 `<table>` 0건이라 표 래핑 강제 대상은 산출물 경로뿐.

### 3.3 HTML 레이아웃 템플릿

**강점**
- skip link(#main) ↔ `<main id="main">` 13/13 완벽 검증 (v4 핵심 수정 성공).
- h1 단일 원칙 13/13, 외부 JS 의존 0건(`SKILL.md:105,194` 준수).
- skip link CSS가 포커스 시에만 노출되는 정석 구현(`theme.css:47-48`), `lang="ko"`·viewport·OG 메타 base 일괄 보장.

**문제점**
| severity | 문제 | file:line | 수정안 |
|---|---|---|---|
| medium | 레이아웃 참조 39개 CSS 클래스 미정의(구조 wrapper + *-header 변형) | `expert-report.html:6-9` 등 vs `*.css` 0건 | 시각구조형은 layouts.css 정의 추가/내부 클래스 사용 안내, 의미형은 '구조 전용'으로 문서화 |
| low | `<footer>` 랜드마크 0/13인데 `theme.css:69-70`은 footer 스타일 정의(orphaned CSS + contentinfo 부재) | `base.html:22-25`, `theme.css:69-70` | `{{BODY}}` 뒤 `<footer>` 슬롯 추가 또는 CSS 제거 (단 source-note aside가 일부 기능 대체 중) |
| low | nav 랜드마크 1/13 — 단 유일 목차는 이미 `<nav aria-label>`로 적정 | `beginner-learning.html:4` | 실질 no-op, related-list 정도만 선택 보강 |
| low | comparison `.matrix`가 grid로 정의돼 '비교=표' 기대와 시맨틱 불일치 | `layouts.css:40`, `comparison-matrix.html:5` | 비교 데이터는 `<table scope/caption>` 권장 |
| low | 골격에 h2 0/13 (슬롯 위임) — h2-sub/계층 게이트 미보장 | grep `<h2>` 0건 | section 슬롯에 제목 패턴 주석 또는 자동 점검 |

> 검증 정정: 원지적 footer(high)는 confirmed이나, 13개 전부 `<aside class="source-note">` 출처/메타 슬롯 보유 → 실익은 contentinfo 랜드마크 + 데드 CSS 해소로 한정되어 low. nav(medium)는 비시맨틱 목차가 실제 0개라 low/partial.

### 3.4 references 작성규칙

**강점**
- blog-writer 상세 규칙 8/8 흡수(제목 4계열·도입부 3유형·밀도 50/20/15/15·톤 매핑·100점·메타·플랫폼·박스).
- 13모드 라우터가 mode-selection↔SKILL↔실파일 3중 일치, 13레이아웃이 폭 규칙(780/1020)까지 정합.
- 깨진 Markdown 표 0건, 플랫폼별 발행 규칙 4개 모두 발행 관점 분리.

**문제점**
| severity | 문제 | file:line | 수정안 |
|---|---|---|---|
| low | 구버전 명칭 잔재 'adaptive-html-blog-writer-v2 / 7개 모드' | `editorial-design-system.md:3` | 'adaptive-html-final은 13개 모드'로 교체(잔재는 이 1곳뿐) |
| low | blog-seo-system 메타 예시(11필드)가 schema(7필드)보다 많아 '준수' 단언과 불일치 | `blog-seo-system.md:31` vs `blog-meta.schema.json:9-33` | 4필드 추가 또는 예시 축소 |
| low | 평가체계 4종 상호참조·우선순위 없이 병존 | `eval-rubric.md:15`, `blog-seo-system.md:49`, `quality-gates.md`, `SKILL.md:213-228` | 각 체계 적용범위 명시 + 연결 1줄 |
| low | h2-sub 강제 강도 3문서 상이(무조건/모드한정/완화) | `quality-gates.md:25` vs `editorial-design-system.md:37` vs `SKILL.md:204/218` | 모드 한정으로 정렬(SKILL.md:204 포함) |
| low | design-dna.md ↔ editorial-design-system.md 토큰 중복 + §8 미등재 | `design-dna.md:5-22` | 단일 출처화 |
| (참고) | platform-system 상·하단 중복, writing-system blog 흐름 용어 비매핑 | `platform-system.md:3-24`, `writing-system.md:28` | 병합/매핑표 추가 |

> 검증 정정: 원지적 v2 명칭(high)은 confirmed·정확하나 문서 정합 한정 영향이라 low. SKILL.md의 'ultimate'는 의도된 계보 표기이므로 결함 아님.

### 3.5 manifest/schema/recipe

**강점**
- manifest JSON 유효, name/version 정확, layouts 13/13 차집합 0(python set 비교).
- 두 schema 모두 Draft 2020-12 메타스키마 통과, merged_from 계보가 SKILL.md 서술과 일치.
- README가 v4 핵심 상태(7+6=13모드, 레이아웃, recipes/schemas)와 일치.

**문제점**
| severity | 문제 | file:line | 수정안 |
|---|---|---|---|
| medium | manifest.modes ↔ 라우터 ID 11/13 불일치(3종 규약 공존) | `manifest.json:28-42` vs `SKILL.md:70-82` vs `layout-system.md` | 단일 ID 규약, modes를 `{id, layout}` 객체 배열로 |
| medium | recipe 6/13 — 7모드 공백 | `recipes/` | 누락 7개 `*.prompt.md` 추가(필수 아닌 완결성 보완) |
| low | blog-meta.schema가 예시 4필드 미정의 | `blog-meta.schema.json:9-34` | 4필드 + title_variants 4키 + search_intent enum 추가 |
| low | quality-report.schema가 rubric/gates 구조 미반영(미소비 고아 스키마) | `quality-report.schema.json:16-28` | rubric 객체+total+verdict로 확장(소비지점 함께 고려) |
| low | 두 schema에 $schema/$id/title 누락 | `*.schema.json:1` | 메타 식별자 추가 |
| low | aliases가 이전 스킬명을 alias·integrate 양쪽 중복 노출 | `manifest.json:48-56` | deprecates 의미 구분 |

> 검증 정정: 원지적 modes 불일치(high)는 confirmed이나 소비 로더 부재·런타임 파손 없음으로 low~medium. recipe 공백(medium)은 README가 recipe를 '대표 프롬프트'로만 규정해 필수 위반 아님.

### 3.6 tests 품질보증

**강점**
- 핵심 HTML 불변식(lang/viewport/title/meta/h1/외부JS) 다수가 체크리스트에 명시.
- visual-regression이 디자인 DNA(오프화이트, h2 빨간 원형 번호)를 회귀 대상으로 포착 시도.
- golden-prompts가 상위 8개 모드를 1:1 정확 대표, SKILL 트리거 문구 충실 반영.

**문제점**
| severity | 문제 | file:line | 수정안 |
|---|---|---|---|
| medium | v4 핵심 skip link/id=main이 4개 테스트 어디에도 검증 항목 없음(회귀 무방비) | `tests/*` 전체 grep 0건 | grep 기반 자동검증 항목 추가, 13개 레이아웃 CI 강제 |
| medium | golden-prompts 8/13 — P9~13(reference/comparison/case_study/landing/checklist) 5모드 누락 | `golden-prompts.md:3-10` | 5개 프롬프트 + expected_mode/layout 명시 |
| medium | quality-checklist가 SKILL Gates 16개 중 9개+ 누락(모드별 산출물·사실성) | `quality-checklist.md:3-16` vs `SKILL.md:213-228` | SoT를 quality-gates.md로 고정, 1:1 매핑 + 조건부 게이트 |
| medium | layout-checklist가 13레이아웃 미열거 + 폭 임계치 3종 불일치 | `layout-checklist.md` / `visual:5` vs `quality-gates:14-15` vs `theme.css:30-31` | 레이아웃별 표 재작성, 폭을 토큰값에 고정 |
| medium | 체크 항목이 측정기준 없는 주관 항목, baseline/diff 도구 부재 | `visual:3,7`, `quality:8` | 정량화(computed font-size ≤42px, 토큰 동등 비교, 픽셀 diff <0.1%) |
| low | golden-prompts에 expected 출력 부재, 7번이 6번 컨텍스트 의존 | `golden-prompts.md:1-11` | expected 필드 첨부, 7번 자체완결화 |
| low | 본문 폭 임계치 760/980 vs 780/1020 vs examples 인라인 3종 충돌 | `visual:5` vs `quality-gates:14-15` vs `theme.css:30-31` | reconcile 후 토큰 고정 |

> 검증 정정: 원지적 skip link 미검증은 critical→medium(자동 CI가 아닌 수동 체크리스트 커버리지 갭). golden/quality/layout 누락(high)은 모두 confirmed이나 런타임 결함 아닌 QA 커버리지 공백이라 medium.

### 3.7 examples 산출물 준수

**강점**
- 8/8 핵심 게이트 통과: lang/viewport/title/meta-desc/단일 h1/`main id=main`/skip link/외부 JS 0/완전 자기완결 인라인 CSS. 모드 블록 7/7, index는 카탈로그.

**문제점**
| severity | 문제 | file:line | 수정안 |
|---|---|---|---|
| low | 공개/SEO 예시 03/05/06 폰트 CDN `<link>` 부재 → Noto Serif KR 미탑재 시 serif 폴백 | `base.html:11-13` vs examples `<link>` 0건 | 03/05/06에 폰트 링크 추가(SKILL.md:99 규칙이 이미 '공개=링크 포함' 규정) |
| low | 표 `.tbl` 래퍼 부재(인라인 CSS라 현재 오버플로 없음) | `02:65, 06:67, 07:67` | 표준화 위해 `.tbl` 도입(의무 위반은 아님) |
| low | h2-sub 8/8 부재(번호 패턴만) | grep h2-sub 0건, `theme.css:62` | 핵심 h2에 p.h2-sub 추가 또는 게이트 완화 |
| low | index.html v2 브랜딩('Blog Writer v2 / 7 templates / 2차 버전') | `index:63` | 'Adaptive HTML Final v4.0.0 13-mode'로 갱신 |
| (참고) | 03/05 본문 in-doc 태그 부재, meta description 14~39자(120~160 표준 미달) | `index:64`, examples meta | 점진 개선 |

> 검증 정정: 폰트(medium)·`.tbl`(medium)·h2-sub(medium) 원지적은 모두 partial로 low 하향 — 규칙이 OR 조건('모바일 안전 구조' 택일)이거나 인라인 CSS에 min-width가 없어 기능 파손 없음, 폰트는 graceful fallback 동작.

## 4. 교차 통합 감사 결과

### 4.1 cross_checks 상태표
| # | 검사 항목 | 상태 | 핵심 |
|---|---|---|---|
| (a) | modes ↔ manifest ↔ recipes ↔ layouts 1:1 | **warn** | layouts 13/13 일치; modes ID 11개 표기 불일치; recipe 6/13; 표기 규약 3종 공존 |
| (b) | 레이아웃 사용 CSS 클래스 미정의 | **fail** | 39개 미정의 확정(article-header만 예외). 완화: section/.header 상속 + 내부 클래스로 렌더, examples는 인라인 CSS |
| (c) | SKILL §8 References ↔ 실제 파일 | **warn** | 9개 인용 OK, design-dna.md(디스크 존재) 미인용 |
| (d) | 13개 레이아웃 `<main id="main">` | **pass** | 13/13 + base.html:23 타깃 일치. 단 tests에 검증 항목 0건 |
| (e) | 전문가 리포트 간 상호 모순 | **warn** | 아래 4건 모순 |

### 4.2 커버리지
| 지표 | 값 |
|---|---|
| layouts_total | 13 (차집합 0) |
| modes_total | 13 (단 manifest↔라우터 11개 표기 불일치) |
| recipes_total | 6 / 13 |
| recipe 없는 모드 | article, education, reference, comparison, case_study, landing_brief, checklist_playbook |
| 미인용 reference | design-dna.md |
| 미정의 CSS 클래스 | 39개 (구조 wrapper 24 + *-header 11 + beginner-* 4) |
| examples 렌더 영향 | 없음 (인라인 `<style>`, asset CSS link 0건) |

### 4.3 전문가 리포트 간 모순 (검증으로 정정된 항목)
| 모순 | 원주장 | 검증 결과 |
|---|---|---|
| sources 허브 | 오케스트레이션: "SKILL.md만 잘못 명시, 실제 허브=examples/index.html" | 실제 3곳(SKILL:208 + editorial:84 + layout-checklist:14)에 존재; examples/index.html은 데모 갤러리이지 출처 허브 아님 |
| GitHub Pages 라우팅 | "의미적으로 틀린 article 우선 선택 위험" | education(P4) > article(P6)이라 예제(04)는 올바르게 education 라우팅 — 인과 반증됨 |
| 본문 폭 | tests: "760/980 vs 780/1020 2종" | 실제 3종 — theme.css 780/1020 vs examples 인라인 760/980 |
| `.tbl` 래퍼 | CSS: "layouts/*.html도 감싸야" | layouts 13개에 `<table>` 0건 — 표는 examples에만 존재 |

## 5. 통합 이슈 트래커

확정 이슈 19건 (검증 후 critical 0 · high 0 · medium 8 · low 11). false_positive 0건.

### Critical / High
없음. (원지적 critical 1·high 7은 검증에서 전원 medium 이하로 하향)

### Medium (8건)
| # | 이슈 | components | 근거 |
|---|---|---|---|
| M1 | tests에 skip link/id=main 검증 항목 0건 — v4 핵심 회귀 무방비 | tests, layouts | `tests/*` grep 0건; `README:11`, `SKILL:30` |
| M2 | 레이아웃 참조 39개 CSS 클래스 미정의 | layouts, CSS | `expert-report.html:6-9` 등 vs `*.css` |
| M3 | manifest.modes ID 11/13 불일치(3종 규약) | manifest, SKILL, references | `manifest:28-42` vs `SKILL:70-82` |
| M4 | recipe 6/13 — 7모드 공백 | manifest/recipe | `recipes/` |
| M5 | quality-checklist가 SKILL Gates 9개+ 누락 | tests, SKILL | `quality-checklist:3-16` vs `SKILL:213-228` |
| M6 | layout-checklist 13레이아웃 미열거 + 폭 3종 불일치 | tests, CSS | `layout-checklist`, `visual:5`, `theme.css:30-31` |
| M7 | `.tbl` 미사용 — min-width:420px 표 <430px 가로 오버플로 | CSS, examples | `components.css:60-61` |
| M8 | 키보드 포커스 가시성 — `:focus-visible` 0건 | CSS | `theme.css:45-48` |

### Low (11건)
| # | 이슈 | 근거 |
|---|---|---|
| L1 | editorial-design-system.md:3 구버전 명칭 잔재 | `editorial-design-system.md:3` |
| L2 | examples/index.html v2 브랜딩 ↔ manifest v4.0.0 | `index:63` |
| L3 | design-dna.md §8 미인용 + 토큰 중복 | `SKILL:235-243` |
| L4 | Required Components에 .faq/.cta-box/.box 누락(landing_brief 자기모순) | `SKILL:109-131` vs `components.css:2` |
| L5 | footer 랜드마크 0/13인데 theme.css는 정의(orphaned CSS) | `theme.css:69-70` |
| L6 | sources/index.html 비존재 경로 3곳 참조 | `SKILL:208`, `editorial:84`, `layout-checklist:14` |
| L7 | blog-meta.schema 예시 4필드 미정의 | `blog-meta.schema.json:9-34` |
| L8 | 평가체계 4종 미연계 + schema 메타식별자 누락 + quality-report 구조 미반영 | `eval-rubric:15` 등 |
| L9 | 디자인 토큰 미완성(raw hex/AA 대비/print/reduced-motion) | `components.css:19-35` 등 |
| L10 | 트리거 키워드 교차 분산 + h2-sub 강도 3문서 상이 + description 장문 | `SKILL:75-76,204/218` |
| L11 | examples 03/05/06 폰트 link 부재(graceful fallback) + h2-sub 부재 | `base.html:11-13` |

### 기각된 지적
적대적 검증 결과 **false_positive로 완전 기각된 지적은 없음**(confirmed 다수 + partial 다수, false_positives: []). 다만 다음 원주장은 검증에서 **사실 오류로 정정**되어 본문 이슈에서 근거를 교체했다:
- "실제 출처 허브는 examples/index.html" → 오류(데모 갤러리임). sources 경로 문제 자체는 L6로 유지.
- "GitHub Pages가 의미적으로 틀린 article로 라우팅될 위험" → 예제로 반증됨(education이 우선). 잔여 모호성만 L10으로 유지.
- "본문 폭 2종 불일치" → 실제 3종으로 정정(M6).
- ".tbl 래퍼를 layouts/*.html에서도 강제" → layouts에 `<table>` 0건이라 대상은 산출물 경로뿐(M7).
- "description 1745자" → UTF-8 바이트 오측정, 실제 ~870자(L10).
- 라인 인용 off-by-one 다수(SKILL 206→208, 202→203, 215→217, 216→218 등)는 본문에서 정확한 라인으로 교정.

## 6. 우선순위 액션 플랜

### P0 — 출시 신뢰성 직결 (즉시)
- **M1**: quality-checklist 또는 신규 accessibility-checklist에 "`<a class="skip" href="#main">` 존재 AND `<main id="main">` 정확히 1개" 항목 추가. 13개 레이아웃에 `grep` 기반 자동검증을 CI로 강제(마크업은 13/13 정합 → 수정이 아닌 회귀방지).
- **M3**: 단일 모드 ID 규약 확정. 권장: 라우터·mode-selection의 접미사형(beginner_html…)을 SoT로 삼고 manifest.modes를 `{id, layout}` 객체 배열로 교체, layout-system/Step4의 checklist 변형도 함께 정렬.
- **M5**: quality-checklist를 `SKILL.md:213-228`과 1:1 매핑 재작성. 누락 9개(디자인토큰 215/계층 217/모바일1컬럼 219/미확인정보 221/출처추측 222/블로그메타 223/교육퀴즈 224/전문가산출물 225/스킬감사개선본 227) 보강, 모드별은 조건부 게이트('교육용이면→퀴즈+정답'). SoT는 quality-gates.md로 고정해 drift 방지.

### P1 — 정합성·커버리지 (단기)
- **M2**: 미정의 39개 클래스를 (a) 시각구조형(risk-matrix/priority-roadmap/winners/tradeoffs/architecture-map/serp-preview)은 layouts.css 정의 추가 또는 내부 클래스(.decision-grid/.serp-box/.winner-card) 사용을 골격 주석으로 안내, (b) 의미형(decisions/results)은 references에 '구조 전용 클래스'로 명시.
- **M4**: 누락 7개 모드 `*.prompt.md` 추가(`SKILL.md:177-187` 필수 블록 트리거 한 문장씩) → 13/13.
- **M6**: layout-checklist를 '파일명|필수블록|폭클래스(.page/.page-wide)' 표로 재작성. 폭 임계치를 reconcile(examples 인라인 760/980 ↔ theme.css 780/1020 중 택일) 후 "`--max-reading/--max-wide` 토큰값과 일치"로 고정.
- **M7 + M8**: `theme.css`에 `:focus-visible` 추가, 산출물 표를 `.tbl`로 래핑하고 빌드에 bare-table 검출 게이트 추가.
- **golden-prompts**: P9~13 5개 프롬프트 + expected_mode/layout 명시(M2 영역의 라우팅 회귀 탐지).

### P2 — 문서·디자인 완성도 (점진)
- **L1/L2/L3/L4/L6**: editorial-design-system.md:3 구버전 명칭 교체, examples/index.html v4 브랜딩 갱신, design-dna.md §8 등재/통합, Required Components에 `.faq/.cta-box/.box`+골격 컴포넌트 추가, sources/index.html 경로 일반화 또는 실제 생성.
- **L7/L8**: blog-meta.schema 4필드+title_variants 4키+search_intent enum 추가, 평가체계 4종 적용범위 1줄씩 명시, 두 schema에 $schema/$id/title 추가.
- **L9**: 박스 글자색·강조선 토큰화, AA 미달 색 진하게, print.css `print-color-adjust`/break-inside, reduced-motion `scroll-behavior:auto` 추가.
- **L5/L10/L11**: footer 슬롯 추가 또는 데드 CSS 제거, h2-sub 강도 통일, 트리거 tie-breaker 본문 노출, description 압축, examples 03/05/06 폰트 link 보강.

## 7. 한 줄 결론

기능적으로 견고하고 v4 핵심 접근성 수정이 13/13 입증된 출시 가능 수준의 스킬이나, 동작 결함은 0건이며 남은 과제는 전부 메타데이터 정합성·테스트 커버리지·디자인 토큰 완성도라는 점에서 — P0 3건(skip link 회귀 게이트·모드 ID 통일·quality-checklist 재작성)만 처리하면 신뢰성 있게 운영 가능한 78/100 성숙도의 패키지다.

---

### 부록 — 분석 메타데이터
- 투입 에이전트: 41개 (전문가 7 + 검증관 32 + 통합감사 1 + 종합 1)
- 소비 토큰: ≈1.34M · 도구 호출 470회 · 소요 ≈48분
- 검증 방식: 각 critical/high/medium 지적을 독립 검증관이 해당 파일을 직접 열어 confirmed/partial/false_positive 판정 (기본값=의심)
