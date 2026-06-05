> ⚠️ **ARCHIVED — SUPERSEDED by v5.2.0.** 이 문서는 작성 당시 버전의 시점 고정(point-in-time) 리뷰/분석/계획 기록입니다. 현재 스킬은 **v5.2.0**이며, 여기서 지적된 항목 다수는 이미 해소·초과 달성되었습니다. 최신 사실 기준선은 게이트를 완전 통과한 `output/adaptive-html-final-13-topics-20260605_083433/`이고, 현행 문서는 루트 `README.md`·`AGENTS.md`·`Guide.md`입니다. 아카이브 색인: [`docs/archive/README.md`](README.md).

---

# adaptive-html-final v4.3.3 — 전문가 리뷰

> 6개 전문가 에이전트 병렬 리뷰 + 핵심 High 지적 적대적 검증
> 영역: 오케스트레이션/메타 · CSS 디자인시스템 · HTML 템플릿/접근성 · 비주얼 템플릿 시스템 · references/recipes/schemas/tests · 쇼케이스 산출물 QA
> 작성일: 2026-05-31

## 1. 총평

**성숙도: 88 / 100 — 출시 등급. 기능적 결함 0건, 남은 과제는 문서 동기화·테스트 drift·접근성 폴리시·1건의 잠재 버그.**

v4.1(직전 리뷰 78점, 확정 이슈 19건) 이후 자동 패치 + Visual Template System(v4.2) + 반응형 폴리시(v4.3.x)를 거치며 크게 성숙했다. 6개 영역 전수 검증 결과:

- **정합성이 매우 높다**: 13개 모드 ID가 SKILL.md 라우터·manifest·mode-selection·layout-system 4개 문서에서 완전 일치(차집합 0), layouts 13/13·references 11/11·visual-templates 7/7 모두 디스크와 1:1.
- **코드 품질 견고**: CSS 미정의 클래스 **0**, `!important` **0**, AA 대비 28개 조합 중 26 통과, 반응형 1컬럼 전환 전 그리드 적용. HTML은 `main id="main"` **13/13**, 단일 h1 **13/13**, 외부 JS **0**.
- **산출물 전수 합격**: v3 쇼케이스 16개(index+01~15) 코어 품질 게이트 **전수 PASS**. v4.3.x 반응형 폴리시(dark CTA 링크 11:1, platform grid, mobile-card-table, case timeline)가 CSS·마크업 양쪽에서 실제 반영 확인.
- **비주얼 시스템 동작**: `render_visual_svg.py` stdlib 전용·`py_compile` 통과·7/7 렌더, 20개 SVG 데모 viewBox(8000) 초과 **0/20**(이전에 수정한 03·13·18·19·20 정상 유지 확인).

가장 실질적인 약점은 (1) **스킬 자체 README가 v4.1.0에 고정**되어 manifest/CHANGELOG(v4.3.3)와 어긋나고 `.skill` 패키지에도 구버전이 번들된 점, (2) **v4.3.x 회귀 게이트가 markdown 테스트에 미반영**(`validate_output.py`에만 존재)이라 수동 체크리스트가 drift된 점, (3) `render_visual_svg.py`의 **문자수 기반 래핑**이 한국어 장문/`lines` 입력에서 가로 오버플로를 일으킬 수 있는 **잠재 버그**(현재 데모·스키마 준수 입력에선 미발현)다.

## 2. 영역별 요약

| 영역 | 등급 | 핵심 |
|---|---|---|
| 오케스트레이션/메타 | 🟢 우수 | 4문서 모드 매핑 13/13 일치 · Step 4.5 템플릿 7/7 정합. 단 스킬 README v4.1.0 고정(high) |
| CSS 디자인 시스템 | 🟢 우수 | 미정의 0 · !important 0 · AA 26/28 · v4.3 폴리시 실반영. `.kicker`·`.try .label` 대비 미달(medium) |
| HTML 템플릿/접근성 | 🟢 우수 | main/h1/JS 전수 통과. `<main tabindex="-1">`·banner landmark는 개선 여지(low) |
| 비주얼 템플릿 시스템 | 🟡 양호 | 7/7 렌더 · 20/20 SVG 정상. 문자수 래핑 잠재 오버플로 + 스키마 미검증(high-latent/medium) |
| refs/recipes/schemas/tests | 🟡 양호 | recipes 13/13 · schemas 3/3 · golden 13/13. quality-checklist 과대표현 + v4.3.x 게이트 drift(high) |
| 쇼케이스 산출물 QA | 🟢 우수 | 16/16 전수 PASS, 위반 0 |

## 3. 통합 이슈 트래커 (검증 후)

### 🔴 High

| # | 이슈 | 근거 | 수정안 |
|---|---|---|---|
| H1 | 스킬 자체 `README.md`가 **v4.1.0** 고정 — Visual System(v4.2)·반응형(v4.3.x) 미반영. `.skill` 패키지에도 구버전 번들 | `skills/adaptive-html-final/README.md:1,5` vs `manifest.json` `4.3.3` ✅검증됨 | 헤더·요약을 v4.3.3로 갱신, 파일목록에 visual-components.css·visual-templates·scripts·tests 추가 후 `.skill` 재패키징 |
| H2 | v4.3.2/v4.3.3 회귀 게이트가 markdown 테스트(layout/visual-regression)에 **미반영** — `validate_output.py`에만 구현 → 수동 체크리스트 drift | `tests/layout-checklist.md:46-57`, `tests/visual-regression-checklist.md:19-30` | 두 체크리스트에 v4.3.2/4.3.3 절 추가 + `validate_output.py` 실행 단계 명시 |
| H3 | `quality-checklist.md`가 "SKILL §7을 **1:1 매핑**"이라 표방하나 실제 34개 중 **22개만** 수록(과대표현) | `tests/quality-checklist.md:3` ✅검증됨 | 문구를 "핵심 발췌(상세 CSS 게이트는 validate_output.py 강제)"로 정정 또는 누락 12개 보강 |
| H4 | (잠재) `render_visual_svg.py` `wrapped()`가 **문자수 기반** → 한국어 전각 장문/`lines` 배열 입력 시 카드·캔버스 가로 오버플로. *현재 데모·스키마 준수 입력에선 미발현* | `scripts/render_visual_svg.py:35-42,83-86` — 검증: 207자 한국어가 단일 런으로 미래핑 생성됨 | CJK 폭 인지 래핑(전각=2) 도입 + 렌더러에서 `type`·길이 사전 검증(maxLength truncate) |

### 🟡 Medium

| # | 이슈 | 근거 | 수정안 |
|---|---|---|---|
| M1 | 스킬 README 파일목록이 구버전(5-CSS만) — visual-components.css·visual-templates·scripts·tests 누락 | `skills/adaptive-html-final/README.md:22-34` | H1과 함께 갱신 |
| M2 | `.kicker`(3.81:1), `.try .label`(4.18:1) AA 4.5:1 **미달**(소형 굵은 라벨 2종) | `theme.css:70`, `components.css:94` | kicker→`--accent-2`(#b72d38), dark 라벨→`--link-on-dark`/더 밝은 accent |
| M3 | `quality-report.schema.json` rubric 6키 ↔ `eval-rubric.md` 7항목 불일치(total 0~100 vs 35점) | `schemas/quality-report.schema.json:26-43` vs `references/eval-rubric.md:9-17` | rubric 키를 eval-rubric 7항목과 정렬 |
| M4 | 렌더러가 `visual-brief.schema.json`을 검증 안 함 → maxLength/maxItems 안전장치 미작동(H4 원인) | `scripts/render_visual_svg.py:214-224` | stdlib 수준 최소 검증(type 존재·필드 길이 truncate) |

### 🟢 Low

| # | 이슈 | 근거 |
|---|---|---|
| L1 | raw hex 토큰화 일부 누락(.prompt-box·code·th 등) + 미사용 토큰 `--dark-soft` | `components.css:68,76,84`, `theme.css:38` |
| L2 | `<header>`가 `<main>` 내부(banner landmark 없음) · `<main>`에 `tabindex="-1"` 없음 · 12개 레이아웃 nav landmark 없음 | 각 `layouts/*.html:2-3`, `base.html:24` |
| L3 | education_html 기본 템플릿 `visual-template-system.md`만 hero-map 추가(불일치) · schema `$id` 도메인 불일치(meewang.kr vs .local) · recipes 형식 비일관(5단문/8상세) | `references/visual-template-system.md:20`, `schemas/*.json:3` |
| L4 | 렌더러 `ValueError` uncaught traceback · schema에 `output` 필드 미정의 · 20 데모는 7종 프로그램 템플릿 산출물이 아닌 별도 수작업 자산(문서-자산 범위 표기 필요) | `scripts/render_visual_svg.py:218,247`, `schemas/visual-brief.schema.json:7` |
| L5 | 쇼케이스 README "74 files"는 `.pyc` 2개 포함(실제 소스 72) | `README.md:137` |

## 4. 검증으로 입증된 강점

| 항목 | 결과 |
|---|---|
| 모드 매핑(라우터·manifest·mode-selection·layout-system) | **13/13** 일치, 차집합 0 |
| Step 4.5 비주얼 템플릿(schema enum·렌더러·.svg.tpl) | **7/7** 정합 |
| CSS 미정의 클래스 / `!important` | **0 / 0** |
| AA 대비(4.5:1) | 28개 조합 중 **26 통과** (callout 4종 5.1~9.3:1) |
| HTML main id=main / 단일 h1 / 외부 JS | **13/13 / 13/13 / 0건** |
| 비주얼: py_compile / 7종 렌더 / 20 SVG viewBox 내 | **통과 / 7-7 / 20-20** |
| 직전 수정 유지(03·13·18·19·20 SVG) | 정상 유지 확인 |
| 쇼케이스 산출물(index+01~15) | **16/16 전수 PASS** |
| v4.3.x 반응형 폴리시 실반영 | dark CTA 11:1 · platform grid · mobile-card-table · case timeline |
| recipes / schemas / golden-prompts | **13/13 / 3/3 유효 / 13/13** |

## 5. 우선순위 액션 플랜

### P0 — 문서 신뢰성 (즉시)
- **H1 + M1**: 스킬 `README.md`를 v4.3.3로 갱신(Visual System·반응형 폴리시·파일목록) → `.skill` 재패키징.
- **H3**: `quality-checklist.md`의 "1:1 매핑" 문구 정정 또는 누락 게이트 보강.
- **H2**: `layout-checklist`·`visual-regression-checklist`에 v4.3.2/4.3.3 절 + `validate_output.py` 실행 단계 추가.

### P1 — 견고성·접근성 (단기)
- **H4 + M4**: `render_visual_svg.py`에 CJK 폭 인지 래핑 + 렌더 전 type/길이 검증(말줄임) 도입.
- **M2**: `.kicker`·`.try .label` 색을 AA 통과값으로 상향.
- **M3**: `quality-report.schema.json` rubric을 `eval-rubric.md` 7항목과 정렬.

### P2 — 폴리시 (점진)
- **L1~L5**: 잔여 raw hex 토큰화·미사용 토큰 제거, `<main tabindex="-1">`·banner landmark·nav 보강, schema `$id` 도메인 통일·`output` 필드 추가·렌더러 친절한 에러 처리, recipes 형식 통일, 문서 수치/자산 범위 표기 정정.

## 6. 한 줄 결론

기능 결함 0·산출물 전수 합격·핵심 접근성/정합성이 입증된 **88/100 출시 등급** 스킬이며, P0 3건(스킬 README 동기화·quality-checklist 정정·v4.3.x 테스트 게이트 반영)만 처리하면 문서-코드 정합까지 완결된다.

---
### 부록 — 리뷰 메타
- 투입: 전문가 에이전트 6개 병렬(오케스트레이션/CSS/HTML/비주얼/refs·tests/쇼케이스) + High 3건 적대적 검증
- 소비: 약 343K 토큰 · 도구 호출 149회
