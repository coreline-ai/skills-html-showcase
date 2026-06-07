> ⚠️ **ARCHIVED — SUPERSEDED by v5.2.0.** 이 문서는 작성 당시 버전의 시점 고정(point-in-time) 리뷰/분석/계획 기록입니다. 현재 스킬은 **v5.2.0**이며, 여기서 지적된 항목 다수는 이미 해소·초과 달성되었습니다. 최신 사실 기준선은 게이트를 완전 통과한 `output/adaptive-html-final-13-topics-20260605_083433/`이고, 현행 문서는 루트 `README.md`·`AGENTS.md`·`Guide.md`입니다. 아카이브 색인: [`docs/archive/README.md`](README.md).

---

# implement_visual_profile_separation.md

작성 일시: `2026-05-31 (KST)`
개정 이력:
- `2026-05-31` 최초 계획 수립.
- `2026-05-31` **전문가·QA 정밀 리뷰(승인 가능도 58/100) 반영 개정** — 거짓 전제 2건 교정(① v6 골든은 widgets.css 까지 인라인한 **auto 번들**이므로 diagram 골든으로 라벨 불가, ② v5 골든은 코어 해시·버전 드리프트로 이미 `validate` FAILED), 교차 누수 게이트 판정 단위 3층 분리, 신설 Phase -1(기준선 동결)·Phase 3.5(골든 사전 진단), 자체테스트를 SHA256 diff·grep·검증기 JSON 출력 등 객관 측정으로 환산.

이 문서는 adaptive-html-final 스킬에 "비주얼 프로파일(visual profile)" 선택 기능을 추가하기 위한
**단계별 분리 계획(phased plan)**이다. 이번 작업의 범위를 고정하고, 구현이 목적 밖으로 확장되지 않도록
하기 위한 작업 문서다.

> **중요: 이번 차수도 계획 수립(전략 + 분리 계획)만이다. 실제 구현·코드/문서/스킬/매니페스트 수정·v6 콘텐츠 수정은 하지 않는다.**
> 아래 Phase 의 체크박스는 모두 미착수 상태이며, 후속 구현 작업에서 이 문서를 단일 출처로 진행한다.

> **리뷰 반영 요지(거짓 전제 교정):** 기존 계획은 "v5=widget 골든, v6=diagram 골든"을 무조건 전제했으나 실측 결과
> (1) v6 14개 페이지는 마크업이 `vt-`만(`wg-` 0)이지만 인라인 `<style>` 에 `.wg-01~.wg-20`(widgets.css)까지 동시 포함된 **auto 번들**이고,
> (2) v5 는 `validate_output.py` 에서 코어 해시·버전 불일치로 이미 FAILED 다.
> 따라서 **세 기준선을 분리 고정**한다: `auto`=현행 v6 산출 그대로(회귀-0 기준선), `diagram`=v6에서 widgets.css만 제거한 슬림 재생성, `widget`=v5 정합화 산출.

---

## 개발 목적

스킬 기동 시 사용자가 두 비주얼 스타일 중 하나를 선택할 수 있게 한다(단일 스킬 + 프로파일 파라미터 방식).

- **widget 프로파일 (v5 스타일)**: CSS 뷰 위젯 `wg-01`~`wg-20` 라이브러리
  (`assets/widgets.css` + `assets/widget-templates/` 20종) 사용. CSS-only 인터랙션(탭/플로우/아코디언).
  CSS 번들 = 코어5 + `widgets.css`. markup 라이브러리 = `wg-`.
- **diagram 프로파일 (v6 스타일)**: SVG→HTML 템플릿 `vt-` 20종
  (`assets/visual-html.css` + `assets/visual-html-templates/` 20종) 사용. 본문 삽입 정적 in-flow 도식.
  CSS 번들 = 코어5 + `visual-html.css`. markup 라이브러리 = `vt-`.
- **auto 프로파일 (기본 · 현행 v6 산출)**: CSS 번들 = 코어5 + `widgets.css` + `visual-html.css` (합본). markup 라이브러리 = `vt-` 1순위 + 필요 시 `wg-` 보강.
  **현행 v6 산출이 정확히 이 auto 번들이며 byte 수준 회귀-0 기준선이다.**

코어(모드 라우팅 → layout → 코어 CSS 5종)는 100% 공유하고, 프로파일은 "어느 **CSS 번들** / 어느 **markup 라이브러리** /
삽입 단계 / 결정표 컬럼"을 쓸지만 게이트한다. **계약은 "CSS 번들"과 "markup 라이브러리" 두 축으로 분리해 기술한다**(이 둘은 독립이며, auto 번들에서는 CSS에 widgets가 들어가도 markup은 vt-만 쓰는 식으로 어긋날 수 있음).

---

## 개발 범위

- 프로파일 계약 정의(이름/별칭/인자 문법/기본값/선택 규칙) — 문서.
- 라우팅에 프로파일 차원 추가: `AGENTS.md` §3, `SKILL.md` §0.5/§0.6, `references/widget-system.md` /
  `references/visual-html-system.md` 의 mode→wg / mode→vt 매핑을 캐노니컬로 대칭 정리.
- 조립(assembly) 게이트: 프로파일별 CSS 번들 규칙 + `base.html` 슬롯 채우기 규칙 + 삽입 단계(Step 4.6 wg- / Step 4.7 vt-) 게이팅.
- 검증기 프로파일 인지: `scripts/validate_output.py` 에 **always-on `cross_leak_gate`**(선언 프로파일 기준 1층 markup) 신설 + `unfilled_placeholder` 게이트 + `validate(root, skill_dir, profile=None)` 시그니처/`--profile` 확장(기존 호출 호환).
- 골든 사전 진단(Phase 3.5): v5/v6 를 신규 게이트·코어해시·버전으로 실측해 통과/실패 표 확정(라벨링의 단방향 선행).
- 문서/매니페스트: `AGENTS.md`/`SKILL.md` 절차·표 반영, `manifest.json` 버전 `4.6.0` bump + `profiles` 스키마 선언, `README`/`CHANGELOG`.
- 쇼케이스 정렬(세 기준선): `auto`=v6 무변경, `diagram`=v6 슬림 재생성, `widget`=v5 정합화(콘텐츠 무변경)로 라벨/문서화. **v6=diagram 전제는 폐기.**
- 검증/수용(측정가능): auto SHA256 diff 0(Phase -1 baseline), widget/diagram 각각 validate OK·무 JS 0·교차 게이트 통과, 크로스-에이전트 결정론은 인자 명시 경로 한정.

---

## 제외 범위

- **실제 구현 자체(이번 차수)** — 이 문서는 계획 수립만이며, 코드/문서/매니페스트의 실제 변경은 후속 차수에서 한다.
- **v6 콘텐츠 수정** — 별도 보류(Deferred) 섹션으로만 명시. 이번 분리 작업과 분리한다.
- **두 스킬 분리(별도 skill 디렉터리)** — 채택하지 않음. 단일 스킬 + 프로파일 파라미터로 확정.
- **외부/동작 JS 도입** — 어떤 프로파일에서도 금지(아래 불변식 참조).
- **신규 모드/레이아웃/템플릿 추가** — 13모드·layout 13개·wg 20종·vt 20종 외 신규 자산 추가 금지.
- **코어 CSS 5종의 내용 변경** — 코어 해시·`css-integrity.json` 계약을 깨는 어떤 변경도 이번 범위 밖.

---

## 참조 문서

- `AGENTS.md` (루트) — 크로스-에이전트 결정론 진입점. §3 결정표 / §4 절차 / §5 불변식 / §6 검증 / §8 자산 인덱스.
- `skills/adaptive-html-final/SKILL.md` — §0.5 Deterministic Operating Spec, §0.6 캐노니컬 결정표, Step 4.6/4.7.
- `skills/adaptive-html-final/references/widget-system.md` — wg- 위젯 선택·삽입·접근성(mode→wg 매핑 정본 후보).
- `skills/adaptive-html-final/references/visual-html-system.md` — vt- 템플릿 선택·삽입·매핑(mode→vt 정본).
- `skills/adaptive-html-final/scripts/validate_output.py` — `widget_static_gate()`/`visual_html_gate()`, 코어 해시, `css-integrity.json` 대조.
- `skills/adaptive-html-final/assets/base.html` — CSS 슬롯 7종 + 본문 슬롯.
- `skills/adaptive-html-final/manifest.json` — `assets` 배열(현재 `profiles` 선언 없음).
- 골든 출력: `output/adaptive-html-final-showcase-v5`(wg- 적용), `output/adaptive-html-final-showcase-v6`(vt- 적용).

---

## 공통 진행 규칙

- 각 Phase 는 앞선 Phase 의 자체 테스트 완료 후에만 시작한다.
- 구현 중 발생한 이슈는 해당 Phase 의 "이슈 및 수정"에 기록하고 그 Phase 안에서 수정한다.
- 체크박스 상태를 실제 진행 상태와 맞게 업데이트한다.
- 문서에 없는 범위 확장(미문서화 신규 기능·무관한 리팩터)은 하지 않는다.
- 한국어로 작성하되 파일 경로·클래스명·인자(`profile=`, `wg-`, `vt-`, `{{WIDGETS_CSS}}` 등)는 영문 그대로 유지한다.
- **(이번 차수 한정)** 모든 Phase 는 계획 검토용이며 실제 변경은 수행하지 않는다. 구현 착수 시 이 문서를 갱신하며 진행한다.

---

## 절대 불변식 (모든 Phase 에서 보존)

1. **외부/동작 JS 0** — `<script type="application/ld+json">` 만 허용. 어떤 프로파일·단계도 이를 깨면 안 된다.
2. **크로스-에이전트 결정론 (인자 명시 경로 한정)** — 프로파일이 라우팅의 첫 입력이 되어야 하며, `AGENTS.md`/`SKILL.md` 에 기계적 절차로
   명시되어 Codex/Gemini 도 동일 결과를 낸다. **결정론 불변식은 "인자(`profile=`/`style=`)가 명시된 경우"로 한정한다.** 미지정 시
   대화형 질문(아래 불변식 7)은 Claude 대화 한정 UX 이며 결정론 보장 대상이 아니다.
3. **기존 스킬 깨지 않기 (auto 회귀 0)** — `auto`(기본)는 현행 v6 산출과 **파일별 SHA256 diff 0건**이어야 한다. 측정 단위는
   "byte 동일"이 아니라 "Phase -1 에서 캡처한 baseline 대비 SHA256 diff 0건". diagram/widget 은 auto 와 다를 수 있다(byte 동일 의무 없음).
4. **코어 해시·`css-integrity.json` 계약 유지 (불변)** — 코어 해시는 항상 코어 5종
   (`theme.css + components.css + visual-components.css + layouts.css + print.css`, 검증기 `asset_order`) 기준이며,
   `widgets.css`/`visual-html.css` 는 코어 해시 대상이 아닌 **조건부 인라인**이다. 어떤 프로파일도 `asset_order`/코어 해시 산식을 바꾸지 않는다.
5. **3층 분리 — 교차 누수 판정 단위 동결.** 프로파일 간 "분리/누수"는 다음 3층으로 **독립** 판정하며, 모든 Phase 의 자체테스트는 이 3층 용어로 통일한다:
   - **(1층) markup 클래스 = 1차 교차 누수 게이트(차단/FAIL 대상).** `diagram` 출력에 `wg-` markup 0, `widget` 출력에 `vt-` markup 0. 판정 기준은 **선언된 프로파일**(`sources/profile.json`)이다.
   - **(2층) CSS 번들 포함 여부 = lint/warn 으로 강등(차단 아님).** 예: widget 출력에 `visual-html.css` 가 섞이면 경고이되 FAIL 아님.
   - **(3층) 코어 해시 = 불변(프로파일 무관, 항상 검증).**
   - `auto` 는 (1층)·(2층) 모두 **비적용**(둘 다 의도된 합본). (3층)은 적용.
6. **3층 분리는 Phase 2(번들)·Phase 3(게이트) 자체테스트에서 동일 용어로 기술**되어야 하며, 계획 내부 모순(예: 번들 포함 여부를 1차 게이트로 격상)을 두지 않는다.
7. **비대화형 분기(자동화 결정론).** `AGENTS.md` 경유 에이전트(Codex/Gemini)는 인자 미지정 시 **무조건 `auto`, 질문 금지**. 대화형 1회 질문은 Claude 대화 UX 한정.

---

## 현재 상태 (실측 — 2026-05-31 재확인)

> 아래는 본 차수 개정 시 리포지토리에서 실제 명령으로 재확인한 사실이다. 모든 자체테스트는 이 측정 명령을 재사용한다.

- **공유 코어 CSS 5종**: `theme.css`, `components.css`, `visual-components.css`, `layouts.css`, `print.css`.
  + 13모드 라우터 + `assets/layouts/*.html` + `assets/base.html`.
- **`base.html` 슬롯(확인 — 7종)**: `{{THEME_CSS}}` `{{COMPONENTS_CSS}}` `{{VISUAL_COMPONENTS_CSS}}`
  `{{WIDGETS_CSS}}` `{{VISUAL_HTML_CSS}}` `{{LAYOUTS_CSS}}` `{{PRINT_CSS}}` — wg+vt 슬롯이 둘 다 존재.
  프로파일별로 미사용 라이브러리 슬롯을 빈 값으로 채우는 처리가 필요.
- **결정표**: `AGENTS.md` §3 표에 "1순위 vt-템플릿" 컬럼과 "권장 wg-위젯" 컬럼이 둘 다 공존(13행).
  `SKILL.md` §0.6 캐노니컬 모드→layout→vt→wg 결정표 존재. mode→wg 정본은 `references/widget-system.md`,
  mode→vt 정본은 `references/visual-html-system.md`.
- **CSS 인라인 순서(`AGENTS.md` §4 표)**: theme→components→visual-components→**widgets→visual-html**→layouts→print.
  코어 해시는 5종만. `widgets.css`/`visual-html.css` 는 "해시 대상 아님" 명시됨.
- **검증기 `scripts/validate_output.py`(실측 시그니처)**:
  - `def validate(root: Path, skill_dir: Path | None = None) -> dict:` (line 196) — **`profile` 인자 없음.**
  - `main()` 인자는 `output_dir`, `--skill-dir`, `--json` 3개뿐(line 333~337) — **프로파일/스타일 인자 없음.**
  - `widget_static_gate(text, style)`(line 103)·`visual_html_gate(text, style)`(line 151)는 페이지 `class="..."`/`class='...'` 에 `wg-`/`vt-` **존재 시에만 자동 트리거**(없으면 아예 안 돎). **항상 켜진 교차 게이트 아님.**
  - 코어 해시 `asset_order = ['theme.css','components.css','visual-components.css','layouts.css','print.css']`(5종, line 201). `css-integrity.json` 은 `root/'sources/css-integrity.json'`(출력 루트 기준) 과 대조. 무 JS(JSON-LD 외 `<script>` 0) 강제.
- **`manifest.json`**: `version` = `"4.5.0"`(line 3). `assets` 배열에 코어 + `widgets.css` + `visual-html.css` + 템플릿 20+20 등록. **`profiles` 키 없음.**
- **`AGENTS.md`**: "profile"/"프로파일" 단어 0회(`grep -ic profile AGENTS.md` = 0). 프로파일 개념 미도입.
- **쇼케이스 골든 실측(핵심 — 기존 라벨 전제 폐기):**
  - `output/adaptive-html-final-showcase-v6`: HTML 14개. markup `class="...wg-NN..."` = **0개 파일**, markup `class="...vt-..."` = **13개 파일**, 그러나 인라인 `<style>` 의 `.wg-01` 정의 = **14개 파일 전부**. ⇒ **CSS 번들 = 코어5+widgets+visual-html 합본(auto 번들)**, markup = vt- 위주. 즉 **diagram 골든이 아니라 auto 골든**이다.
  - `output/adaptive-html-final-showcase-v5`: markup `vt-` 누수 = **0개 파일**(교차 1층 게이트는 통과). 그러나 `validate_output.py` 실행 시 **FAILED** — `source_version_mismatch`(skill 4.5.0 vs v5 4.3.3), `inline_css_hash_mismatch ×16`, `css_integrity_core_hash_mismatch`(expected `bd5665…` actual `541d5e…`), asset/snapshot mismatch. ⇒ widget 골든으로 쓰려면 **4.5.0 코어로 정합화 필요**.

---

## Phase 상태 요약

- [x] **Phase -1 완료 — 기준선 동결(baseline freeze): v6 전체 파일·SHA256·validate JSON 캡처** *(P0 착수 전 필수)* ✅ 21파일·shasum-c 전OK·validate ok=true(html 14)·auto마커(wg-markup0/vt-markup13/inline.wg-01 14)
- [x] Phase 0 완료 — 프로파일 계약 정의(2축 계약표·세 기준선·비대화형 규칙·인자 정규화 전수표) ✅ 계약 명세 본 문서에 동결(2축표·세 기준선 경로·정규화 전수표+의사코드·Step 0.5)
- [x] Phase 1 완료 — 라우팅에 프로파일 차원 추가(프로파일 모드보다 선행 + mode→wg 정본 단일화) ✅ AGENTS §4 Step0+§3 주석·SKILL §0.5/§0.6 오버레이·"코어6종"→"5종해시+조건부" 동기화·mode→wg §0.6↔§3 불일치0
- [x] Phase 2 완료 — 조립(어셈블리) 게이트(세 번들 정의 + 슬롯 비우기 + 코어해시·literal 토큰 불변) ✅ AGENTS §4 프로파일 번들표·슬롯 비우기·Step6/7 게이팅·SKILL 4.6/4.7 게이트; 슬림 어셈블러 U1–U7 OK(82KB widgets 제거·body 무변경); auto=baseline 21/21 OK
- [x] Phase 3 완료 — 검증 프로파일 인지(always-on cross_leak_gate + 정규식 계약 + profile.json + 시그니처 확장) ✅ validate(root,skill_dir,profile=None)·--profile·_resolve_profile(우선순위·별칭·invalid)·cross_leak_gate(diagram wg-NN/widget vt-, 단·이중따옴표·대소문자)·unfilled_placeholder; 단위 13/13·회귀0(baseline==now)
- [x] **Phase 3.5 완료 — 골든 사전 진단** *(P5 라벨링의 단방향 선행)* ✅ dev-plan/golden_prediagnosis.md: v6/auto OK·v6/diagram markup-OK(슬림 아님)·v5/widget FAILED22 → 결론(v6=auto 무변경/diagram 슬림 재생성/v5 정합화)
- [x] Phase 4 완료 — 문서/매니페스트(profiles 스키마 + AGENTS/SKILL/README/CHANGELOG) ✅ **버전 결정 변경: 4.6.0→4.5.0 유지**(4.6.0 bump은 frozen auto 골든 v6의 footer/sources를 건드려 회귀-0을 깨므로 골든 보존 우선; 일관성 manifest=sources=footer=4.5.0 충족). manifest profiles 3종·경로 OK·v6/auto OK·페이지 회귀0(14/14)
- [x] Phase 5 완료 — 쇼케이스 정렬(v5 정합화 선결 + 확정 골든 라벨링) ✅ diagram 슬림 골든(showcase-diagram, body diff0·widgets.css0·vt유지)·v5 정합화(16p <style>교체·body diff0·widget OK)·v6 profile.json(auto); 세 골든 profile.json 자동인지 전수 ok=true·무JS0·cross_leak0
- [x] Phase 6 완료 — 검증/수용(SHA256 diff 0 + validate OK + 교차 게이트 통과, 측정가능 수용) ✅ auto 회귀0(21/21 SHA256 OK, +profile.json만)·세 프로파일 validate OK(auto14/widget16/diagram14)·무JS 0(3종)·교차게이트(diagram wg-0/widget vt-0)·결정론 수렴(5/5)

---

## ✅ 전체 구현 완료 (Phase -1 ~ 6)

모든 Phase 통과. 단 한 가지 계획 대비 결정 변경: **버전 4.6.0 bump → 4.5.0 유지**(frozen auto 골든 v6의 footer/sources를 건드려 회귀-0을 깨므로 골든 보존 우선; manifest=sources=footer=4.5.0 일관성 충족). Deferred(v6 콘텐츠 수정)는 손대지 않음.
- [ ] Deferred — v6 **콘텐츠** 수정 (이번 범위 밖, 보류 / 번들·정합화와 diff 기준으로 구분)

> **Phase 의존 순서(단방향):** Phase -1(기준선) → Phase 0~2 → **Phase 3(게이트) → Phase 3.5(사전진단) → Phase 0 산하 v5 정합화 실행 → Phase 5(라벨링)** → Phase 4(문서/매니페스트는 Phase 0~3 확정 후) → Phase 6(수용). 게이트가 사전진단보다, 사전진단이 라벨링보다 항상 먼저다.

---

## Phase -1. 기준선 동결 (baseline freeze) — P0 착수 전 필수

### 목표
- 현행 v6 산출(= auto 번들)을 **읽기전용 baseline** 로 캡처해, 이후 모든 "회귀 0 / 동일"을 **파일별 SHA256 diff 0건**으로 정량화한다.
- 이 Phase 가 끝나기 전에는 다른 어떤 Phase 도 실행(구현)하지 않는다.

### 구현 태스크
- [ ] v6 전체 파일 목록 캡처(읽기전용): `find output/adaptive-html-final-showcase-v6 -type f | sort > dev-plan/baseline_v6_files.txt`.
- [ ] 파일별 SHA256 캡처: `find output/adaptive-html-final-showcase-v6 -type f -print0 | sort -z | xargs -0 shasum -a 256 > dev-plan/baseline_v6_sha256.txt`.
- [ ] 검증기 baseline JSON 캡처: `python3 skills/adaptive-html-final/scripts/validate_output.py output/adaptive-html-final-showcase-v6 --skill-dir skills/adaptive-html-final --json > dev-plan/baseline_v6_validate.json`.
- [ ] auto 번들 실측 마커 캡처(회귀 비교용): v6 14개 파일의 markup `wg-` 0 / markup `vt-` 13 / 인라인 `.wg-01` 14 를 baseline 메모로 고정.
- [ ] **비교 명령 동결(이후 Phase 6·회귀 테스트가 그대로 재사용):**
  - 파일 집합 diff: `diff <(현재 파일목록) dev-plan/baseline_v6_files.txt`
  - 내용 diff: `shasum -a 256 -c dev-plan/baseline_v6_sha256.txt`  (모든 라인 `OK` 면 diff 0)
  - 또는 `diff <(현재 SHA256) dev-plan/baseline_v6_sha256.txt`

### 영향 파일
- (이번 차수) 캡처 산출물은 `dev-plan/baseline_v6_*` 읽기전용. **v6 원본은 절대 변경하지 않는다.**

### 자체 테스트
- [ ] `baseline_v6_files.txt` 라인 수 = `find … -type f` 현재 개수와 동일(0 누락).
- [ ] `shasum -a 256 -c dev-plan/baseline_v6_sha256.txt` 전 라인 `OK`(캡처 직후 self-consistency).
- [ ] `baseline_v6_validate.json` 이 유효 JSON 이고 `html_count == 14`.
- [ ] baseline 메모의 markup/inline 마커 수치가 본 문서 "현재 상태" 실측치와 일치.

### 이슈 및 수정
- [ ] 발견 이슈 없음

### 완료 조건
- [ ] baseline 3종(files/sha256/validate) 캡처 완료
- [ ] 비교 명령 동결 완료
- [ ] 자체 테스트 완료 / Phase 0 진행 가능

### 위험 / 롤백
- 위험: baseline 캡처 후 v6 가 우발적으로 변경되면 회귀 기준 무효 → v6 디렉터리는 읽기전용 취급, 변경 금지 규칙 명문화.
- 롤백: 캡처 산출물 삭제 후 재캡처(원본 무변경이라 무손실).

---

## Phase 0. 프로파일 계약 정의 (문서)

### 목표
- 프로파일의 이름·별칭·인자 문법·기본값·선택 규칙을 한 곳에 확정해, 이후 모든 Phase 의 단일 출처로 삼는다.
- **세 기준선(auto/diagram/widget)을 파일 경로까지 명시해 동결**하고, 계약표를 "CSS 번들"·"markup 라이브러리" **2축**으로 분리한다.

### 구현 태스크
- [ ] 프로파일 이름 확정: `widget` / `diagram` / `auto`.
- [ ] **세 기준선 동결(파일 경로 명시)** — 아래 표를 본 문서 정본으로 고정:

  | 프로파일 | 기준선 정의 | 파일 경로 | byte 기준 |
  | --- | --- | --- | --- |
  | `auto` | 현행 v6 산출(코어5+widgets+visual-html, markup=vt-) **그대로** | `output/adaptive-html-final-showcase-v6` | **회귀-0 기준선** (Phase -1 baseline 과 SHA256 diff 0) |
  | `diagram` | v6 에서 **widgets.css 만 제거**한 슬림 재생성(콘텐츠 무변경, CSS 번들만 변경) | (Phase 5 에서 신규 생성) | v6 와 byte 다름이 **정상** |
  | `widget` | v5 **정합화** 산출(4.5.0 코어로 sources/스냅샷/manifest 리프레시 + widgets.css 인라인, 콘텐츠 무변경) | `output/adaptive-html-final-showcase-v5`(정합화 후) | v6 와 byte 다름이 **정상** |

- [ ] **2축 계약표 작성(핵심 — CSS 번들 ⊥ markup 라이브러리)**:

  | 프로파일 | CSS 번들 | markup 라이브러리 | 삽입 단계 | §3 결정표 컬럼 |
  | --- | --- | --- | --- | --- |
  | `widget` | 코어5 + `widgets.css` | `wg-` | Step 4.6(wg-) | "권장 wg-위젯" |
  | `diagram` | 코어5 + `visual-html.css` | `vt-` | Step 4.7(vt-) | "1순위 vt-템플릿" |
  | `auto` | 코어5 + `widgets.css` + `visual-html.css` | `vt-` 1순위 + `wg-` 보강 | Step 4.6 + 4.7 | 두 컬럼 모두 |

  > 명문화: "auto=현행 byte 동일"을 **회귀 기준**으로 못박되, diagram/widget 은 auto 와 다를 수 있음(CSS 번들·byte 모두). auto 번들은 CSS에 widgets가 있어도 markup은 vt- 위주인 합본이다.
- [ ] 별칭 확정: `style=v5`→`widget`, `style=v6`→`diagram`. `auto` 별칭 없음.
- [ ] **인자 정규화 전수표 동결**(`profile=widget|diagram|auto` 와 `style=v5|v6` 둘 다 수용):

  | 입력(원문) | 정규화 절차 | 결과 |
  | --- | --- | --- |
  | `profile=widget` / `PROFILE = Widget` / ` profile= WIDGET ` | trim → lowercase → 정규화 | `widget` |
  | `profile=diagram` | 〃 | `diagram` |
  | `profile=auto` / (미지정) | 〃 / 기본값 | `auto` |
  | `style=v5` | 별칭→캐노니컬 | `widget` |
  | `style=v6` | 별칭→캐노니컬 | `diagram` |
  | `profile=widget` + `style=v6` (충돌) | **profile= 우선**, 경고는 stderr/로그만 | `widget` |
  | `style=v7` / `profile=foo` / 오타·범위밖 | **ISSUE FAIL(`invalid_profile`)**, 조용한 auto 폴백 **금지** | FAIL |

- [ ] **정규화 의사코드 동결(1개):**
  ```
  def resolve_profile(args) -> str:           # args: 원문 토큰 dict
      def norm(v): return v.strip().lower()
      p = norm(args.get("profile", "")) or None
      s = norm(args.get("style", "")) or None
      style_map = {"v5": "widget", "v6": "diagram"}
      cand = None
      if p is not None and s is not None:      # 충돌: profile 우선, 경고만(HTML·sources 비기록)
          log_warn("profile= and style= both given; profile= wins")
          cand = p
      elif p is not None:
          cand = p
      elif s is not None:
          cand = style_map.get(s)              # 무효 style -> None
          if cand is None: return FAIL("invalid_profile", s)
      else:
          return "auto"                        # 미지정 기본값
      if cand not in {"widget", "diagram", "auto"}:
          return FAIL("invalid_profile", cand) # 조용한 auto 폴백 금지
      return cand
  ```
  > 경고/오류 메시지는 **stderr/로그에만** 남기고 HTML 본문·`sources/` 에는 기록하지 않는다.
- [ ] 기본값 확정: 인자 미지정 시 `auto`.
- [ ] **선택 규칙 확정(분기 명시)**:
  - **비대화형(AGENTS.md 경유 Codex/Gemini)**: 인자 미지정 시 **무조건 `auto`, 질문 금지**. 결정론 보장 대상.
  - **대화형(Claude 대화 한정 UX)**: 인자 미지정 시 1회 질문 가능. 결정론 불변식 비대상.
  - 어느 경로든 인자가 **명시**되면 질문 없이 정규화 결과로 고정.
- [ ] **Step 0.5(profile.json 기록) 계약 명시**: §4 절차에 "결정된 프로파일을 `output/sources/profile.json`(`{"profile":"widget|diagram|auto"}`)으로 기록"을 css-integrity/manifest 스냅샷 단계에 끼운다. **auto 도 기록한다.** 검증기 1차 입력(Phase 3).

### 영향 파일
- (이번 차수) 본 문서 내 계약 명세만. 후속 구현 시 `SKILL.md` §0.5, `AGENTS.md` §2/§4 에 반영 예정.

### 자체 테스트 (객관 측정)
- [ ] 2축 계약표가 3프로파일 × (CSS 번들 / markup 라이브러리 / 삽입단계 / §3 컬럼) 전 셀을 빠짐없이 채운다(빈 셀 0).
- [ ] 세 기준선 표가 각 행에 **파일 경로**와 byte 기준을 명시한다(`auto`=회귀-0, diagram/widget=다름 정상).
- [ ] `auto` 정의가 "현행 v6 산출과 SHA256 diff 0"임을 문장화(Phase -1 baseline 연결).
- [ ] 정규화 전수표의 모든 유효 입력이 단일 캐노니컬로 수렴, 무효/충돌 입력이 각각 `invalid_profile` FAIL / `profile=` 우선으로 결정론 처리됨을 표로 확인.
- [ ] 비대화형 경로(미지정→auto·질문금지)와 대화형 경로(미지정→1회 질문)가 분리 명시되고, "인자 명시 시 결정론 고정"이 두 경로 공통임을 확인.
- [ ] Step 0.5(profile.json 기록, auto 포함)가 §4 어느 단계에 삽입되는지 명시.

### 이슈 및 수정
- [ ] 발견 이슈 없음

### 완료 조건
- [ ] 계약 명세 완료
- [ ] 자체 테스트 완료
- [ ] 다음 Phase 진행 가능

### 위험 / 롤백
- 위험: 별칭/인자 문법이 후속 Phase 와 어긋나면 전체 재작업. → Phase 0 에서 표를 동결(freeze)하고 변경 시 본 문서 갱신.
- 롤백: 문서 변경만이므로 git 이전 커밋으로 복원.

---

## Phase 1. 라우팅에 프로파일 차원 추가

### 목표
- 라우팅을 "코어(모드→layout) + 프로파일 오버레이(widget→wg컬럼 / diagram→vt컬럼)"로 재구조화하고,
  프로파일을 모드보다 먼저 결정하도록 절차를 고정한다.

### 구현 태스크
- [ ] **`AGENTS.md` §4 절차에 "0. 프로파일 결정(모드 결정보다 선행)"을 번호 절차로 박는다** — Step 0(프로파일) → Step 0.5(profile.json 기록) → 기존 모드 결정 순. 프로파일이 라우팅의 첫 입력.
- [ ] `AGENTS.md` §3 결정표를 코어(Mode→layout) + 프로파일 오버레이(vt 컬럼 / wg 컬럼)로 재해석(데이터 보존). **§3 헤더에 "프로파일별 컬럼 사용" 주석 추가**(widget=wg컬럼만 / diagram=vt컬럼만 / auto=두 컬럼).
- [ ] `SKILL.md` §0.5 에 프로파일 결정 단계 추가, §0.6 결정표에 프로파일 오버레이 해석 주석 추가.
- [ ] **불변식 동기화(거짓 "코어 6종" 제거):** `AGENTS.md` 불변식 6 과 `references/visual-html-system.md` §5 의 "코어 6종" 표현을 **"코어 5종 해시 + (widgets/visual-html) 조건부 인라인"** 으로 통일(코어 해시 산식 불변 재확인).
- [ ] **mode→wg 정본 단일화:** mode→wg 매핑 정본을 `SKILL.md` §0.6 으로 단일화하고, §0.6 ↔ §4.6 ↔ `AGENTS.md` §3 wg 컬럼 ↔ `references/widget-system.md` **4곳을 grep 으로 1:1 대조**(중복 정의 시 §0.6 우선, 나머지는 참조).
- [ ] 프로파일별 컬럼 사용 규칙 명문화: `widget`=wg컬럼만, `diagram`=vt컬럼만, `auto`=vt 1순위 + wg 보강(현행).

### 영향 파일
- `AGENTS.md` (§3, §4, 불변식 6)
- `skills/adaptive-html-final/SKILL.md` (§0.5, §0.6, §4.6)
- `skills/adaptive-html-final/references/widget-system.md`
- `skills/adaptive-html-final/references/visual-html-system.md` (§5)

### 자체 테스트 (객관 측정)
- [ ] 13모드 × 3프로파일에 대해 (layout, 사용 컬럼) 조합이 표에서 유일하게 결정된다(중복/누락 0).
- [ ] "프로파일이 모드보다 먼저"가 `AGENTS.md` §4 Step 0 / `SKILL.md` §0.5 양쪽에서 동일 문구로 명시된다.
- [ ] **mode→wg 4곳 일치 grep**: §0.6·§4.6·`AGENTS.md` §3·`widget-system.md` 에서 각 mode 의 wg 매핑이 동일(불일치 0건). 측정: 각 소스에서 `mode→wg` 쌍을 추출해 diff 0.
- [ ] "코어 6종" 문자열이 `AGENTS.md`·`visual-html-system.md` 에서 0건(`grep -rn "코어 6종\|core 6\|6종" …` → 0), "코어 5종"+"조건부 인라인" 표현으로 대체됨.
- [ ] `auto` 경로가 기존 §0.6 결과(vt 1순위 + wg 보강)와 동일함을 표로 대조.

### 이슈 및 수정
- [ ] 발견 이슈 없음

### 완료 조건
- [ ] 구현 완료 / 자체 테스트 완료 / 다음 Phase 진행 가능

### 위험 / 롤백
- 위험: §3 표 재구조화 중 기존 vt/wg 매핑값 손실 → 재구조화 전 §3 표 원본을 백업 블록으로 보존 후 비교.
- 위험: AGENTS.md(정본)와 SKILL.md(보조) 우선순위 충돌 → 충돌 시 AGENTS.md 우선 규칙 재확인.
- 롤백: 문서 변경만이므로 커밋 단위 복원.

---

## Phase 2. 조립(어셈블리) 게이트

### 목표
- 프로파일별 CSS 번들 규칙과 `base.html` 슬롯 채우기, 삽입 단계 게이팅을 기계적 절차로 고정한다.

### 구현 태스크
- [ ] CSS 번들 규칙 명문화(Phase 0 핵심결정1 = 세 기준선과 동일):
  - `widget` = 코어 5종 + `widgets.css`(`{{WIDGETS_CSS}}` 채움, `{{VISUAL_HTML_CSS}}` 빈 값).
  - `diagram` = 코어 5종 + `visual-html.css`(`{{VISUAL_HTML_CSS}}` 채움, `{{WIDGETS_CSS}}` 빈 값).
  - `auto` = 코어 5종 + 둘 다(= 현행 v6 번들).
- [ ] `base.html` 슬롯 채우기 규칙: 미사용 라이브러리 슬롯은 **빈 문자열**로 치환(슬롯 삭제 아님, 플레이스홀더 잔존 금지).
- [ ] **빈 슬롯 개행 정규화:** 합본 단계에서 빈 슬롯 치환으로 생긴 잉여 빈 줄을 제거(개행 정규화)해, auto 번들이 baseline 과 SHA256 동일하도록 보장. 빈 슬롯이 byte 차이를 만들지 않게 한다.
- [ ] 인라인 순서 불변 확인: theme→components→visual-components→(widgets)→(visual-html)→layouts→print
  (`AGENTS.md` §4 표 순서 유지, 미사용 항목만 생략).
- [ ] 삽입 단계 게이팅: Step 4.6(wg-)는 `widget`/`auto` 에서만, Step 4.7(vt-)는 `diagram`/`auto` 에서만 실행.
- [ ] 코어 해시 마커는 프로파일과 무관하게 코어 5종 기준 유지(조건부 인라인은 해시에서 제외) 명시.

### 영향 파일
- `AGENTS.md` (§4 CSS 인라인 표 + 삽입 단계 6/7)
- `skills/adaptive-html-final/SKILL.md` (Step 4.6, Step 4.7, §4 합본 순서 문단)
- `skills/adaptive-html-final/assets/base.html` (슬롯 자체는 유지; 채우기·개행 정규화 규칙만 문서화)

### 자체 테스트 (객관 측정)
- [ ] (1층 markup) `widget` 출력에 `vt-` markup 클래스 0건, `diagram` 출력에 `wg-` markup 클래스 0건 — grep `class=["'][^"']*\bvt-` / `\bwg-\d{2}\b`.
- [ ] (2층 CSS 번들·warn) `widget` 출력에 `visual-html.css` 마커(예 `.vt-shell` 정의) 0건, `diagram` 출력에 `widgets.css` 마커(`.wg-01` 정의) 0건 — **번들 누락은 lint/warn 으로 보고**(차단 아님, Phase 3 와 동일 3층 용어).
- [ ] (3층 코어해시 불변) 세 프로파일 모두 코어 해시 마커가 코어 5종 기준 **동일 값**(프로파일 무관).
- [ ] 미사용 슬롯이 빈 값으로 치환되어 `{{...}}` 플레이스홀더 잔존 **0건**(grep `\{\{[A-Z_]+\}\}` → 0).
- [ ] **literal 토큰 잔존 확인**(검증기 규칙이 의존하는 텍스트가 번들 변경 후에도 남아있는지): `section>h2:first-child`, `.layout-blog …::before`, `.try .summary-card`, `--link-on-dark` 가 해당 번들 적용 프로파일 출력에 잔존(0건 아님 = 정상). 측정: 각 토큰 grep count ≥ 1.
- [ ] **`auto` 합본 = baseline 일치(SHA256 diff 0):** auto 재합본 산출이 Phase -1 `baseline_v6_sha256.txt` 와 `shasum -a 256 -c` 전 라인 `OK`. 개행 정규화 효과 포함.

### 이슈 및 수정
- [ ] 발견 이슈 없음

### 완료 조건
- [ ] 구현 완료 / 자체 테스트 완료 / 다음 Phase 진행 가능

### 위험 / 롤백
- 위험: 미사용 CSS 미인라인으로 클래스가 남으면 깨진 스타일 → 삽입 단계 게이팅과 슬롯 비우기를 한 묶음으로 검증.
- 위험: 인라인 순서 변경 시 검증기의 특정 규칙(예: `section>h2:first-child`)에 영향 → 순서는 절대 변경하지 않고 항목만 생략.
- 롤백: `base.html` 미변경(슬롯 유지)이라 문서 규칙만 되돌리면 됨.

---

## Phase 3. 검증 프로파일 인지

### 목표
- `validate_output.py` 가 프로파일을 인지해 해당 게이트를 적용하고, 교차 누수(cross-leak)를 0으로 강제한다.

### 구현 태스크
- [ ] **시그니처 확장(호환 유지):** `validate(root, skill_dir=None, profile=None)` 로 확장(line 196). `main()` 에 `--profile widget|diagram|auto`(선택, default=None) 추가(line 333~337 인자에 한 줄). **기존 3인자/3옵션 호출은 그대로 동작**해야 한다.
- [ ] **프로파일 입력 우선순위(확정):** `--profile` 인자(1순위) → `sources/profile.json` 선언(2순위) → 둘 다 없으면 `None`(기존 동작 폴백: 교차 게이트 미적용, 클래스 존재 자동 트리거만). profile.json 은 `{"profile":"widget|diagram|auto"}`. 인자가 선언보다 우선.
- [ ] **`cross_leak_gate(text, declared_profile)` 를 별도 always-on 함수로 신설**(기존 `widget_static_gate`/`visual_html_gate` 와 분리). 판정 기준은 **선언된 프로파일**(자동 트리거 아님). 정규식 계약:
  - `diagram`: `\bwg-\d{2}\b` 매치 **0건**(단·이중따옴표 `class=` 속성 모두 커버, 대소문자 무시).
  - `widget`: `\bvt-[a-z]` 매치 **전반 0건**, 단 **bare 도식 클래스 화이트리스트**는 제외(예: `vt-shell`/`vt-frame` 같은 구조 클래스만이 아니라, widget 출력에서 정당하게 쓰일 수 있는 항목은 화이트리스트로 명시 — 화이트리스트 목록을 본 Phase 에서 동결).
  - 단·이중 따옴표 변형: `class="…vt-…"` / `class='…vt-…'` 모두 매치.
  - `auto`: cross_leak_gate **비적용**(1·2층 모두). (3층 코어해시는 적용.)
- [ ] **교차 누수 전용 ISSUE 타입 신설:** `cross_leak`(예 `{'type':'cross_leak','profile':'diagram','found':'wg-03','file':...}`). 기존 ISSUE 타입과 구분.
- [ ] **`{{...}}` unfilled_placeholder 게이트 신설:** 출력에 `{{[A-Z_]+}}` 잔존 시 ISSUE(`unfilled_placeholder`). 프로파일 무관 always-on.
- [ ] 기존 `widget_static_gate()`/`visual_html_gate()` 는 (자동 트리거 동작 유지) 그대로 두고, cross_leak 은 별도 함수로 추가(역할 분리).
- [ ] 무 JS·코어 해시·`css-integrity.json` 대조 기존 로직은 프로파일과 무관하게 유지(3층 불변).

### 영향 파일
- `skills/adaptive-html-final/scripts/validate_output.py` (시그니처 확장 + `cross_leak_gate` + `unfilled_placeholder` + `--profile`)
- (선택) `skills/adaptive-html-final/tests/widget-checklist.md`, `tests/quality-checklist.md` 동기화 검토.

### 자체 테스트 (객관 측정 — 3층 용어 통일)
- [ ] (1층) `--profile diagram` + `wg-NN` 주입 픽스처 → `cross_leak` ISSUE + FAILED. 누수 0 픽스처 → OK.
- [ ] (1층) `--profile widget` + 화이트리스트 밖 `vt-` 주입 → `cross_leak` ISSUE + FAILED. 화이트리스트 클래스만 있으면 OK.
- [ ] (정규식 커버) 단따옴표 `class='…vt-…'`·대문자 `VT-`·`WG-` 변형이 모두 매치됨을 픽스처로 확인.
- [ ] `--profile auto` 는 cross_leak_gate 미적용으로 v6(auto 골든) `OK`(3층 코어해시만).
- [ ] `unfilled_placeholder` 게이트: `{{WIDGETS_CSS}}` 잔존 픽스처 → ISSUE, 정상 출력 → 0건.
- [ ] (3층) 세 프로파일 모두 무 JS(JSON-LD 외 `<script>` 0)·코어 해시 일치 통과.
- [ ] **회귀 0:** 기존 3인자 호출 `validate_output.py <dir> --skill-dir <skill> --json`(--profile 없음)이 변경 전과 동일 결과(profile.json 없을 때 cross_leak 미적용). 측정: Phase -1 `baseline_v6_validate.json` 와 신버전 출력 diff 0.
- [ ] `profile.json` 자동 인지 vs `--profile` override 우선순위가 픽스처로 확인(인자 우선).

### 이슈 및 수정
- [ ] 발견 이슈 없음

### 완료 조건
- [ ] 구현 완료 / 자체 테스트 완료 / 다음 Phase(3.5) 진행 가능

### 위험 / 롤백
- 위험: `--profile`/`profile=None` 확장이 기존 호출부 호환을 깨면 안 됨 → 인자·파라미터 모두 default=None, 회귀 0 테스트 필수.
- 위험: cross_leak 정규식이 화이트리스트를 누락해 widget 정상 출력을 오탐 → 화이트리스트를 본 Phase 에서 동결하고 픽스처로 양/음성 모두 검증.
- 위험: 교차 게이트를 2층(CSS 번들)까지 차단으로 격상하면 불변식 5 위배 → CSS 번들은 warn, markup 만 FAIL.
- 롤백: 단일 스크립트 변경이므로 파일 단위 git 복원.

---

## Phase 3.5. 골든 사전 진단 (Phase 5 라벨링의 단방향 선행)

### 목표
- v5/v6 를 **Phase 3 신규 게이트 + 코어 해시 + 버전**으로 실측해, 각 골든이 어느 프로파일에서 **통과/실패**하는지 확정 표를 만든다.
- 이로써 Phase 5 는 "확정 골든 라벨링"만 하면 되도록 의존성을 단방향으로 고정한다(게이트 → 사전진단 → v5 정합화 → 라벨링).

### 구현 태스크
- [ ] v6 사전진단: `--profile auto` / `--profile diagram` 각각으로 `validate_output.py … --json` 실행, cross_leak·코어해시·버전 결과 캡처. (예상: auto=OK, diagram=2층 widgets 잔존 warn + markup vt- 만 → 1층 통과지만 "diagram 슬림"이 아니라 "auto 번들"임이 드러남.)
- [ ] v5 사전진단: `--profile widget` 으로 실행, 코어해시·버전 실패 항목 캡처(예상: `source_version_mismatch` 4.5.0 vs 4.3.3, `inline_css_hash_mismatch ×16`, `css_integrity_core_hash_mismatch` `bd5665…`↔`541d5e…`, asset/snapshot mismatch → FAILED. 단 1층 `vt-` 누수 0).
- [ ] **사전진단 확정 표 작성**: (골든 × 프로파일) → {1층 markup, 2층 번들 warn, 3층 코어해시, 버전, 종합 OK/FAIL} 셀 전부 채움.
- [ ] 표에서 도출되는 결론 명문화: ① v6 는 그대로 **auto 골든**(diagram 아님), ② diagram 골든은 **신규 슬림 재생성 필요**, ③ widget 골든은 **v5 정합화 필요**.

### 영향 파일
- (이번 차수) 진단 결과는 `dev-plan/golden_prediagnosis.md`(또는 본 문서 표)에만 기록. **골든 원본 무변경.**

### 자체 테스트 (객관 측정)
- [ ] v6 `--profile auto` 종합 `OK`(baseline validate JSON 과 일치).
- [ ] v6 `--profile diagram` 결과가 "markup vt- 만 + widgets.css 2층 잔존(warn)"으로 캡처되어 **diagram 슬림과 다름**이 표로 확정.
- [ ] v5 `--profile widget` 종합 `FAILED` + 실패 타입 목록(`source_version_mismatch`/`inline_css_hash_mismatch`/`css_integrity_core_hash_mismatch`)이 실측 캡처와 일치.
- [ ] 확정 표의 모든 셀이 채워지고, Phase 5 가 참조할 "라벨링 vs 재생성 vs 정합화" 분기가 명시됨.

### 이슈 및 수정
- [ ] 발견 이슈 없음

### 완료 조건
- [ ] 사전진단 표 확정 / 자체 테스트 완료 / Phase 5 진행 가능(라벨링 입력 확보)

### 위험 / 롤백
- 위험: 게이트(Phase 3) 미완 상태에서 진단하면 무의미 → Phase 3 완료가 선행 조건(상태 요약의 단방향 순서 준수).
- 롤백: 진단 문서 삭제로 무손실(골든 무변경).

---

## Phase 4. 문서 / 매니페스트

### 목표
- 프로파일 선택 절차·표를 정본 문서에 반영하고, `manifest.json` 에 프로파일을 선언한다.
- **프로파일 도입 버전을 확정**(예: `4.6.0`)하고, 골든 3종 sources/manifest 를 일괄 동기화한다.

### 구현 태스크
- [ ] **프로파일 도입 버전 확정:** 현 `manifest.json` `version` = `4.5.0` → 프로파일 도입 minor bump `4.6.0`(SemVer, 신기능). 버전 상수를 manifest·CHANGELOG·골든 sources 가 공유.
- [ ] `AGENTS.md` / `SKILL.md` 에 프로파일 선택 절차·표 최종 반영(Phase 0~3 결과 동기화).
- [ ] **`manifest.json` `profiles` 스키마 추가**(이름·자산경로 명시):
  ```json
  "profiles": {
    "widget":  {"css": ["widgets.css"], "templates": "widget-templates/", "markup": "wg-"},
    "diagram": {"css": ["visual-html.css"], "templates": "visual-html-templates/", "markup": "vt-"},
    "auto":    {"css": ["widgets.css", "visual-html.css"], "templates": ["widget-templates/", "visual-html-templates/"], "markup": ["vt-", "wg-"]}
  }
  ```
- [ ] **골든 3종 sources/manifest 일괄 동기화:** auto(v6)·diagram(슬림)·widget(v5 정합화)의 `sources/adaptive-html-final-manifest.json` 버전을 `4.6.0` 로 통일하고 `profile.json` 동봉.
- [ ] `skills/adaptive-html-final/README.md` 에 프로파일 사용법(인자 문법·기본값·별칭) 추가.
- [ ] `skills/adaptive-html-final/CHANGELOG.md` 에 `4.6.0` 프로파일 도입 항목 추가.

### 영향 파일
- `AGENTS.md`, `skills/adaptive-html-final/SKILL.md`
- `skills/adaptive-html-final/manifest.json` (version 4.6.0 + profiles)
- `skills/adaptive-html-final/README.md`, `skills/adaptive-html-final/CHANGELOG.md`
- 골든 3종 `output/.../sources/` (manifest 버전·profile.json)
- (선택) 루트 `README.md`

### 자체 테스트 (객관 측정)
- [ ] `python3 -c "import json;json.load(open('skills/adaptive-html-final/manifest.json'))"` 통과(유효 JSON) + `version == "4.6.0"` + `profiles` 3종 존재.
- [ ] **profiles 자산경로 대조:** profiles 의 모든 `css`/`templates` 경로가 `assets/` 아래 실제 파일과 1:1 일치(`test -e` 전부 통과, 누락 0).
- [ ] `AGENTS.md`/`SKILL.md`/manifest 의 프로파일 정의가 Phase 0 계약(2축 표·정규화)과 100% 일치(grep 대조 불일치 0).
- [ ] 골든 3종 sources manifest 버전이 모두 `4.6.0`, 각 `profile.json` 의 `profile` 값이 라벨과 일치(auto/diagram/widget).
- [ ] CHANGELOG/README 에 인자 문법·기본값·별칭이 계약과 동일하게 기재.

### 이슈 및 수정
- [ ] 발견 이슈 없음

### 완료 조건
- [ ] 구현 완료 / 자체 테스트 완료 / 다음 Phase 진행 가능

### 위험 / 롤백
- 위험: manifest 의 자산 매핑이 실제 파일과 어긋나면 결정론 깨짐 → 경로를 실측 목록과 대조.
- 롤백: 문서/manifest 변경만이므로 커밋 단위 복원.

---

## Phase 5. 쇼케이스 정렬 (확정 골든 라벨링)

### 목표
- Phase 3.5 사전진단 표를 근거로 **세 골든을 확정**한다: `auto`=v6(무변경), `diagram`=v6 슬림 재생성, `widget`=v5 정합화.
- v5 정합화는 **콘텐츠 무변경**(번들/메타만)이며 Deferred 의 "v6 콘텐츠 수정"과 diff 기준으로 분리한다.

### 구현 태스크
- [ ] **(선결) v5 정합화** — 4.5.0/4.6.0 코어로 v5 의 `sources/`(css-integrity.json, manifest, 스냅샷) 리프레시 + widgets.css 인라인 확인. **본문 콘텐츠는 손대지 않는다.** Phase 3.5 의 v5 FAIL 항목(버전/코어해시/스냅샷)을 해소.
  - 콘텐츠 무변경 증명: 정합화 전후 **본문 텍스트(스크립트/스타일 제외) diff 0**. 측정: 각 페이지에서 `<body>` 텍스트만 추출해 before/after diff.
- [ ] **diagram 슬림 재생성** — v6 콘텐츠를 그대로 두고 widgets.css 만 제외한 번들로 재생성(Phase 2 번들 규칙 적용). v6 와 byte 다름 정상, 콘텐츠 무변경.
- [ ] 골든 라벨/문서화: `output/.../v6`→`auto`, diagram 슬림 산출→`diagram`, `output/.../v5`(정합화 후)→`widget`.
- [ ] 각 골든에 `sources/profile.json` 동봉(auto/diagram/widget).
- [ ] (선택) 쇼케이스 홈에 프로파일 안내 텍스트(무 JS, 정적).

### 영향 파일
- `output/adaptive-html-final-showcase-v6/` (auto 라벨 — 무변경, profile.json 추가만)
- `output/adaptive-html-final-showcase-v5/` (widget — 정합화: sources/메타 리프레시, 콘텐츠 무변경)
- diagram 슬림 골든 (신규 디렉터리)
- (선택) 쇼케이스 인덱스/홈 문서

### 자체 테스트 (객관 측정 — 3층 용어)
- [ ] **auto(v6) 무변경:** `shasum -a 256 -c dev-plan/baseline_v6_sha256.txt`(profile.json 추가분 제외) 전 라인 `OK`(SHA256 diff 0).
- [ ] **widget(v5 정합화):** `--profile widget` 으로 `validate_output.py` 종합 `OK`(Phase 3.5 의 버전/코어해시/스냅샷 FAIL 0), 무 JS 0, 1층 `vt-` 누수 0.
- [ ] **widget 콘텐츠 무변경 증명:** v5 `<body>` 텍스트 정합화 전후 diff 0.
- [ ] **diagram(슬림):** `--profile diagram` 으로 종합 `OK`, 1층 `wg-` markup 0, 2층 widgets.css 0(번들에서 제외됨), 무 JS 0. v6 와 byte 다름은 허용.
- [ ] 세 골든의 `profile.json` 값이 manifest `profiles` 키와 라벨에 일치.

### 이슈 및 수정
- [ ] 발견 이슈 없음

### 완료 조건
- [ ] 구현 완료 / 자체 테스트 완료 / 다음 Phase 진행 가능

### 위험 / 롤백
- 위험: v5 정합화가 콘텐츠까지 건드리면 Deferred 경계 위반 → 본문 `<body>` 텍스트 diff 0 로 게이트.
- 위험: diagram 슬림 재생성이 콘텐츠를 바꾸면 안 됨 → v6 본문 텍스트와 diagram 본문 텍스트 diff 0 확인(번들/스타일만 차이).
- 롤백: auto(v6)는 무변경이라 안전. widget/diagram 은 신규/메타 변경이라 디렉터리 단위 복원.

---

## Phase 6. 검증 / 수용

### 목표
- 전체 수용 기준을 한 번에 검증한다.

### 구현 태스크
- [ ] **auto 회귀 0(측정 정의):** auto 산출 파일별 SHA256 이 Phase -1 `dev-plan/baseline_v6_sha256.txt` 와 **diff 0건**. 측정: `shasum -a 256 -c dev-plan/baseline_v6_sha256.txt` 전 라인 `OK`.
- [ ] **widget 수용:** `--profile widget` `validate_output.py` 종합 `OK` + 무 JS 0 + 1층 `vt-` 누수 0(cross_leak 0).
- [ ] **diagram 수용:** `--profile diagram` 종합 `OK` + 무 JS 0 + 1층 `wg-` 누수 0(cross_leak 0).
- [ ] **크로스-에이전트 결정론(인자 명시 경로 한정):** 동일 인자(`profile=`/`style=`)로 Codex/Gemini/Claude 가 동일 라우팅 결과. 미지정 경로는 비대화형=auto·대화형=질문이라 결정론 수용 대상에서 제외(불변식 2·7 재확인).

### 영향 파일
- 검증 실행만(코드/문서 변경 없음). 필요 시 위 Phase 로 되돌아가 수정.

### 자체 테스트 (객관 측정)
- [ ] auto: `shasum -a 256 -c dev-plan/baseline_v6_sha256.txt` 전 라인 `OK`(diff 0건).
- [ ] widget·diagram 각각: `validate_output.py … --profile … --skill-dir … --json` 의 `ok == true`.
- [ ] 무 JS grep(3프로파일): JSON-LD 외 `<script` 매치 0건 — `grep -rc '<script' … | grep -v 'application/ld+json'`.
- [ ] 교차 게이트(3층 1층): diagram `\bwg-\d{2}\b` markup 0 / widget 화이트리스트 밖 `vt-` 0 — `cross_leak` ISSUE 0.
- [ ] 결정론: `profile=widget`/`style=v5` 등 명시 인자가 정규화 전수표대로 동일 캐노니컬로 수렴(인자 명시 경로만).

### 이슈 및 수정
- [ ] 발견 이슈 없음

### 완료 조건
- [ ] 구현 완료 / 자체 테스트 완료 / 전체 수용 완료(측정 기준 충족)

### 위험 / 롤백
- 위험: `auto` SHA256 diff 가 0 이 아니면 Phase 2 의 슬롯/개행 정규화 오류 → Phase 2 로 회귀.
- 위험: 미지정 경로를 결정론 수용 대상으로 오인 → 수용 기준을 "인자 명시 경로"로 한정(불변식 2).
- 롤백: 각 Phase 가 독립 커밋이면 문제 Phase 만 복원.

---

## Deferred (이번 분리와 분리 — 보류)

> 경계 기준 = **본문 콘텐츠 diff**. "콘텐츠 무변경(번들/메타/정합화)"은 본 차수, "콘텐츠 변경"은 Deferred.

- **본 차수(콘텐츠 무변경):** v5 정합화(코어 4.6.0 sources/스냅샷/manifest 리프레시), diagram 슬림 번들 재생성, profile.json 동봉.
  ⇒ 모두 `<body>` 텍스트 diff 0 으로 증명되어야 하며, 게이트 통과를 위한 메타/번들 변경만 허용.
- **Deferred(콘텐츠 변경 — 보류):** `output/adaptive-html-final-showcase-v6` 등의 **본문 콘텐츠 자체 개선/수정**.
  이번 작업에서는 v6 를 `auto` 골든으로 "라벨링/대조"만 하고, 콘텐츠는 손대지 않는다(`<body>` 텍스트 diff 0 의무).

---

## 잔여 리스크 / 후속 과제

- **(교정)** v6 는 diagram 골든이 아니라 **auto 골든**(widgets.css 까지 인라인). diagram 골든은 슬림 **재생성**으로 별도 확보(Phase 5).
- **(교정)** v5 는 코어 해시·버전 드리프트(4.5.0 vs 4.3.3, `bd5665…`↔`541d5e…`)로 이미 `validate` FAILED → widget 골든은 **정합화** 필요(Phase 5 선결, 콘텐츠 무변경).
- **(해결)** 교차 누수 판정 = **3층 분리**(1층 markup=FAIL, 2층 CSS 번들=warn, 3층 코어해시=불변). 계획 내부 모순 제거(불변식 5·6).
- **(해결)** 인자 문법: `profile=widget|diagram|auto` 와 `style=v5|v6` 둘 다 수용, trim→lowercase→정규화→`profile=` 우선. 무효/범위밖은 `invalid_profile` FAIL(조용한 auto 폴백 금지).
- **(해결)** 비대화형(AGENTS.md 경유)은 미지정 시 무조건 auto·질문 금지. 결정론 불변식은 인자 명시 경로 한정.
- **(해결)** 검증기 프로파일 입력: `--profile`(1순위) → `sources/profile.json`(2순위) → 없으면 폴백. `validate(root, skill_dir, profile=None)` 로 호환 확장.
- 후속: diagram 슬림 골든의 시각 회귀(콘텐츠는 같으나 widgets 인터랙션 부재)는 Playwright 스냅샷으로 별도 확인 검토(본 차수 범위 밖).
