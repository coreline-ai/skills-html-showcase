# Changelog — adaptive-html-final

## v5.10.6 (2026-06-21) — 시각 결함 하드닝(G1~G8) + 검출 게이트 + mode 18 business_plan 병합

validate/quality/completion은 통과하지만 사용자 화면에 남던 누적 시각 결함(G1~G8)을 스킬 본체 차원에서 닫고, 정적으로 못 잡던 결함을 검출 게이트로 승격했다. 직전 Unreleased(manual_analysis 배지 padding) 코어 변경도 본 릴리스에 흡수한다.

- **G1 (작성 계약)**: 좁은 표 열 짧은 상태코드 줄바꿈 — `.status-pill` 정본(`table .status-pill{white-space:nowrap}`) 사용 규칙화(broad `td code` nowrap은 다토큰 코드 회귀 회피).
- **G3 (components.css 코어)**: `.try` 중첩 흰 카드(.box/.summary-card/.cta-box/.card-block/.mini-card) 링크가 다크 전용 `--link-on-dark`(흰 배경 1.65:1)를 상속하던 저대비를 `--accent-2`로 reset(8테마 min 6.09:1). `.try` 직속 링크는 `--link-on-dark` 유지.
- **G4 (editorial-patterns.css)**: `source-preserve` 좌측 rail↔본문 gutter 정본 `.source-body-inner{border-left+padding-left:24px}`.
- **G5 (components.css 코어)**: `.mini-card>.tag:first-child` vertical rhythm 정본(margin-bottom + 후속 h3/p reset).
- **G8 (editorial-patterns.css)**: `.core-insight>:first-child{margin-top:0}` 내부 제목 margin 누수 reset(red gradient 보존 — 의도 카드에 `--neutral` 금지).
- **A5 (theme.css 코어)**: `@media (prefers-contrast: more)` 약 토큰 대비 상향(일반 렌더 영향 0).
- **manual_analysis 배지(layouts.css 코어, 직전 Unreleased 흡수)**: STEP·위험·UNKNOWN 배지에 `padding:3px 10px;margin-bottom:8px` — 좌측 컬러 rail과 라벨 간격 확보.
- **검출 게이트 신설**: G2 diagram 노드 박스 overlap(>4px×4px)·G3 inner-card 링크 대비를 `render-audit.json` micro_layout(`node_overlap_ok`·`inner_card_link_contrast_ok`; `scripts/micro_layout_audit.mjs` 생산, `completion_check.py` 검사)으로, G4·G5·G8은 자산-레벨 정적 가드, G3·G6(TOC가 executive-summary 내부 중첩)·G7(섹션 첫 `<h2>` 앞 빈 anchor)은 per-page 정적 가드로 신설. **거버넌스 162→186**.
- **pretest_contract 게이트(hybrid)**: `scripts/pretest_contract_check.py`(stdlib) — `output/` 산출물을 official/preview/fail로 분류(validate·sources 스냅샷·pretest 라벨·완료-주장 금지문구). governance에 `decide()` self-test(8 case) 등록해 분류 로직 회귀 차단 → **거버넌스 185→186**.
- **mode 19 `storm_research` 병합(버전 업 없음)**: 다관점 STORM 리서치 리포트 모드 — 5관점(회의주의자/경제학자/역사학자/학자/미래학자)·출처 강제·모순 지도·동료검토 게이트·provenance 원장 계약 + custom gate 6종(soul_count·minimum_sources·citation_label·contradiction·peer_review·provenance). primary_vt `process-swimlane` + wg-13/14/18/11/16/04 **재사용**, `page` 폭(60rem 회피) → **신규 위젯/코어 CSS 없음 → 코어 해시 `a64604d0` 불변**. 18→19 모드, examples 18→19, layouts 18→19, **거버넌스 186→199**(+13). v5.10.6 additive 병합(business_plan 선례).
- **mode 18 `business_plan_html` 병합(버전 업 없음)**: 사업계획서/지원서 모드 신규 추가 — 증거태그([사실]/[추정]/[가정]/[목표]/[확인 필요])·단일 숫자 레지스트리(NR-NN)·in-HTML 출처원장(발행처/기준시점/접근일/URL)·4-평가자(행정/기술/사업/회의) **자기검토 스코어카드** 계약 + custom gate 4종(evidence_tag·number_consistency·source·status). primary_vt `implementation-plan` + wg-16/11/13/18/14 **재사용**(신규 위젯/코어 CSS 없음 → 코어 해시 불변). 17→18 모드, examples 17→18, governance +9(176→185). 사용자 결정으로 별도 v5.11.0 없이 본 릴리스에 병합.
- **파급**: 코어 CSS(theme·components·editorial-patterns·layouts) 직접 수정 → **코어 해시 `a73eb204`(직전 미릴리스 배지 수정 흡수본)→`a64604d0`** · examples 18종 재인라인 · `sources/css-integrity.json` · source manifest · `.skill` 재패키징. (v5.10.5 태그 릴리스는 `7e151665`였고, 그 위 미릴리스 배지 수정이 `a73eb204`로 올린 뒤 본 릴리스가 흡수.)

## v5.10.5 (2026-06-15) — 접근성·스코프 하드닝: forced-colors 상태 단서 + .score 스코프 + vt 장식 글리프 aria + 루브릭↔스키마 연결

코어 CSS 5종 무수정(해시 `7e151665` 불변)으로 접근성·스코프 결함만 좁게 닫은 패치. 변경은 조건부 자산 3종 + vt-10 템플릿 + 문서로 한정한다.

- **A1 (theme-dark.css·widgets.css, 조건부)**: forced-colors(Windows 고대비)에서 배경색만으로 선택/체크 상태를 전하던 컨트롤이 상태를 잃던 문제를 `@media(forced-colors:active)`에서 시스템색 `Highlight` outline 단서로 복원. 대상은 테마바 선택 라벨과 wg-02/06/07/12/19/20 선택·체크 상태 및 wg-06 primary. 미디어 가드라 일반 렌더(코어/평상시) 시각 영향 0.
- **A2 (visual-html.css, 조건부)**: 전역 누수 위험이 있던 비스코프 `.score`를 `.tuner .score`로 좁힘(vt-20 prompt-tuner 전용 — 실렌더 시각 무변).
- **A3 (장식 글리프 aria-hidden — vt-10 화살표 + vt-05 체크표)**: flowchart 장식 화살표 `→` 4종(10-flowchart 템플릿+카탈로그)과 checklist-flow 장식 체크표 `✓`/`·`(05 템플릿+예제 13·16+카탈로그)에 `aria-hidden="true"` 부여 — 상태는 동반 `cf-state`(PASS/진행 중/대기) 텍스트가 전달하므로 글리프는 순수 장식. 21-soft-workflow-map 화살표는 이미 부모 `aria-hidden` 상속이라 불변.
- **A4 (references/eval-rubric.md)**: `schemas/quality-report.schema.json` 고아 해소 — 루브릭 점수를 기계 판독 결과로 남기는 스키마 연결(필드 매핑) 1절 추가.
- **파급**: 조건부 자산만 변경 → **코어 해시 `7e151665` 불변**. examples 18종 재인라인·`sources/css-integrity.json`·source manifest·`.skill` 재패키징. 거버넌스 **162** 유지.

## v5.10.4 (2026-06-14) — 마이크로 레이아웃 정본 계약(M1·M4·M7·M10) + 작성 프로토콜

실산출물(2026-06-14 Anthropic 6월 뉴스)이 `validate/quality/completion`을 전부 통과했는데도 사용자 눈검수에서 남은 마이크로 레이아웃 결함을, "검증 OK ≠ 품질 OK" 사례로 취급해 정본에 반영했다. 핵심 원칙: output 산출물은 독립 결과물이며, 여기서 발견한 결함은 **명시적 승격**으로만 스킬에 들어온다.

- **M1 (theme.css, 코어)**: `h2 .no/.num` 번호 pill이 390px에서 2줄로 깨지던 것을 `white-space:nowrap`으로 한 줄·원형 고정(base + 모바일 규칙 양쪽).
- **M4 (visual-html.css, 조건부)**: `.cmp-card .vt-kicker` kicker→title 간격 4px→8px(인접 텍스트 rhythm 하한 충족).
- **M7 (print.css, 코어)**: 인쇄/export 산출물에서 `.reading-progress`를 숨김(`@media print`) — 섹션 라인 오인·검수 방해 제거.
- **M10 (theme.css, 코어)**: `{{FOOTER}}` 슬롯이 `<main>` 밖(body 직속)에 렌더될 때 `.source-note` footer가 viewport 좌측에 붙던 것을 `body>footer` 본문 폭 중앙 정렬로 고정.
- **M2·M3·M6·M9 (작성 프로토콜)**: 별표/tag 접착·rail 텍스트 접착·밋밋한 목록 카드·단색 rail 반복은 스킬 정본 컴포넌트(`lede-note`는 이미 24px rail padding, vt chip은 gap 보유, `tl-color-cycle`은 4색 순환)가 이미 해결한다. 실패는 output이 비정본 클래스(`template-card-head`·`source-preserve-static`)를 발명했기 때문 → `docs/adaptive-html-final-template-authoring-protocol.md`에 "정본 컴포넌트 사용" 규칙으로 고정.
- **파급**: 코어(theme/print) 해시 갱신 → examples 18종 재인라인·`sources/css-integrity.json`·source manifest·`.skill` 재패키징. Phase 3에서 M2/M3 비정본 클래스, M5/M6 flat text-only section, build-evidence 누락/stale 검출 fixture를 추가해 거버넌스 **153→159 checks**로 승격. 이어 17모드 독립 벤치마크 전용 `benchmark-manifest.json`·모드별 `mode-build-sheet.md`·모드별 `build-evidence.json`·`render-audit.micro_layout` 필수 증빙 게이트를 추가해 **159→162 checks**로 승격. 무 JS 유지.

## v5.10.3 (2026-06-12) — 회귀 안전 패치: 다크 대비·인쇄 가독·폭 정본(전 모드 wide) + 자기방어 게이트 6종

3차 전문가 리뷰(렌더 실측) 발견을 dev-plan §4의 회귀 프레임(S0 베이스라인 → 등급별 패치 → 프로브 diff)대로 반영. **라이트 테마 무영향 설계**: #fff→var(--on-accent)는 라이트 4테마에서 byte-동일(on-accent=#ffffff), print.css는 전 규칙 @media print 내부(스크린 영향 0 구조 보장).

### 2026-06-14 모드 정의 Registry 모듈화 (단일 출처화, 5.10.3 유지)

17개 모드의 결정표 데이터가 `AGENTS.md`·`SKILL.md §0.6`·`MODE_TEMPLATE_CONTRACTS`·`widget-system.md`·`manifest`에 중복 분산돼 신규 모드 추가 시 드리프트 위험이 컸다. 이를 `modes/NN-<mode>.json` **단일 출처**로 모듈화했다. 코어 CSS·17모드 산출·버전 불변(5.10.3), validator 동작 byte-동일.

- **Registry 신설**: `modes/01..17-*.json` 17종(id·priority·label·layout·recipe·triggers·required_blocks·layout_placeholders·primary_vt·vt_candidates·vt_markers·wg_candidates·wg_markers·toc_contract·quality_contract·examples·custom_contracts). 권위 출처(`MODE_TEMPLATE_CONTRACTS`·§0.6·layout·recipe)에서 결정론적 추출.
- **validator가 Registry를 읽음(B-full)**: `MODE_TEMPLATE_CONTRACTS`를 `_build_mode_template_contracts_from_registry()`로 전환. **registry-built == 전환 전 literal**(sha 동일)·**examples validate before==after**로 회귀 0 증명. vt 마커 regex 토큰·`wg_candidates`→`recommended_wg` 매핑으로 deep-equal 성립.
- **sync checker**: `scripts/mode_registry.py`(loader)·`scripts/check_mode_registry_sync.py`. Registry ↔ `MODE_TEMPLATE_CONTRACTS`(build==live) ↔ SKILL §0.6 ↔ widget-system ↔ **AGENTS §3 직접 파싱** ↔ manifest ↔ 파일 존재 ↔ toc required_class 일치를 강제(marker 삽입 없이 직접 파싱, AGENTS 드리프트 갭 해소).
- **governance**: registry sync + 신규 모드 dry-run(중복 priority·primary_vt 드리프트·layout 누락·필수필드 누락 검출) 테스트 추가. **144→153 checks**, `manifest.quality.governance_count`·README 표면 동기화.
- **runbook**: `docs/adaptive-html-final-add-mode-runbook.md`(신규 모드 추가 절차 + 안전 매트릭스: 어떤 게이트가 어떤 불완전 추가를 잡는가).

### 2026-06-13 저장소 위생 — 레거시 데모 정리·템플릿 카탈로그 내재화

- **레거시 데모 정리**: 루트 `demo/`의 과거 v2/learning-ultimate/blog demo 쇼케이스 105개 추적 파일을 제거하고, 현행 정본 경로를 `skills/adaptive-html-final/examples/`와 공개 데모 산출물로 단순화했다.
- **템플릿 카탈로그 내재화**: 사용자가 직접 검수한 `templates/final_20260604/` HTML 4종을 `skills/adaptive-html-final/template-catalog/`로 이동해 스킬 내부 디자인 카탈로그로 보관한다. 이 카탈로그는 17모드 examples 기준선이 아니라 vt/wg/테마/폭 회귀 확인과 패턴 역동기화 참고용이다.
- **참조 교정**: README 프로젝트 트리·`AGENTS.md` 단일 출처 표·`editorial-design-system.md`의 golden reference를 현행 examples/template-catalog 구조에 맞춰 정리했다.
- **manifest 기록**: `manifest.template_catalog`에 보관 위치·출처·목적·4개 HTML 파일 목록을 추가해 카탈로그가 임의 폴더가 아니라 스킬 내부 참고 자산임을 명시했다.

### 2026-06-13 정합 보강 — 생성 회귀 방지 정책/게이트

사용자가 반복 지적한 "최신 스킬 헤더가 안 나옴, 아이콘/목차/가로폭/밀착/간격이 흔들림" 문제를 정적 게이트와 완료 아티팩트 계약으로 승격했다. 과거 공개 데모/테스트 산출물은 스킬 정본이 아니며, 최신 기준선은 `skills/adaptive-html-final/examples/`와 신규 산출물이다.

- **헤더 정본 전역화**: `header_contract_gate`가 전 `layout-*` 콘텐츠 페이지에서 `kicker`·`h1`·`sub`·`meta`뿐 아니라 `generated-row`·`lens-strip`까지 필수 검사. SEO/Reference 예제 헤더 보정.
- **목차 정본 강화**: 직접 h2 섹션이 4개 이상인 toc-required 페이지와 분석/사용 가이드 모드는 공식 `toc-map` chip-nav를 필수화. examples 17종 중 누락 페이지에 정본 목차와 섹션 anchor 보강.
- **아이콘 순서 게이트**: `h2_icon_order_violation`으로 직접 섹션 h2의 `body-icon → (.num/.no) → title` 순서를 강제해 아이콘 생략뿐 아니라 뒤섞임/밀착 회귀를 차단.
- **body-icon 카탈로그 게이트**: `.body-icon` 래퍼만 맞추고 내부에 Lucide/Feather식 `viewBox="0 0 24 24"` 임의 SVG를 넣는 회귀를 차단. `body_icon_catalog_gate`가 `assets/body-icons.json` 32종, `viewBox="0 0 40 40"`, `bi-*` 토큰 클래스를 강제하고 `body_icon_markup.py` 헬퍼로 생성 단계의 SVG 상상을 줄인다.
- **가로 overflow 방어**: 긴 무공백 URL/코드 토큰이 보호 요소 밖 prose에 노출되면 실패(`long_token_overflow_unprotected`). R4 표 보호 wrapper에 `.tbl`을 인정해 기존 정본 CSS와 게이트를 일치.
- **품질 보조 게이트**: `quality_contract_check.py`가 정본 컴포넌트 없이 raw `<p>`/`<div>`/`<li>`로 섹션을 대량 합성하는 붕어빵/좌측 밀착 패턴을 차단.
- **완료 아티팩트**: `completion_check.py`가 신규 산출물의 `sources/render-audit.json` + 1280/390 screenshot 증빙을 검사한다. 검증기는 Playwright를 직접 구동하지 않고 외부 캡쳐 산출물만 확인하며, 현행 packaged examples는 기준선 예외로 통과.
- **거버넌스**: 신규 catch/pass 테스트를 추가하고 manifest `quality.governance_count` 단일 출처를 **144/144**로 동기화. `.skill` 재패키징으로 byte-match 유지.
- **버전업 방지**: `version_release_approval_issues`가 HEAD와 다른 `manifest.version`을 감지하면 `dev-plan/release-approval-vX.Y.Z.md` 없이는 실패해 승인 없는 patch bump를 차단.

- **다크 대비 P1**: widgets.css "카탈로그 reverse-sync" 층의 하드코딩 `color:#fff` 3규칙(wg-01 pick/rank·wg-02 cta·wg-06 btn·wg-07 pill·wg-09 next·wg-17 no·wg-20 chip)을 `var(--on-accent)`로 — 다크 트리오 대비 1.92→8.6+ (실측). wg-13-decide(4.69 AA 통과)·wg-20-var(자체 7.10)는 의도적 제외.
- **wg-07 애니메이션 복원**: 정적화(`animation:none`) 제거 — 879행 카탈로그 메모("미반영")와 코드 일치화, prefers-reduced-motion 블록이 접근성 보장.
- **인쇄 P1**: print.css에 `.try p/li/ol/ul/a/.label/.tag{color:#111}`(실측 1.3:1 소실 수정), `::details-content{content-visibility:visible}`(아코디언 인쇄 펼침), href 출력 `a[href^="http"]` 한정(내부 앵커 잡문자 제거), `.ahf-themebar` 인쇄 숨김. theme-dark.css에 다크 트리오 인쇄 시 라이트 토큰 강제 블록 + `#ahf-dark`에 `--danger-accent:#ff6b75`.
- **폭 정본 A 채택**: 전 17모드 = `.page-wide` + 단락 60rem(960px). 골격 5종(beginner/article/blog/education/case) page→page-wide 승격, theme.css 60rem 목록에 4모드 × (section·article>section) 24셀렉터 추가 — 예제 01/03/04/05 단락 736→960px. `references/layout-system.md`에 폭 정본 성문화.
- **게이트 6종 신설**: `on_accent_pairing_violation`(accent 배경+#fff 잉크 lint) · `theme_token_contrast_fail`(테마별 accent-2/on-accent 대비 ≥4.5 정적 검증) · `print_try_ink_missing` · `layout_width_consistency_issues`(골격↔예제 폭 일치 + wide 골격 60rem 등재) · 테마 스위처 **8/8 강제**(3/8→) · `skill_package_version_stale`(.skill zip 버전 = manifest). R5 wide 목록 +4모드.
- **거버넌스**: 신설 게이트 catch/pass + 미커버 게이트 7종(widget_static/visual_html/cross_leak/mode_template_contract/direct_section_title_icon/body_icon_diversity/analysis_toc_map) 잠금 — 88→117 checks.
- **도구**: exporter `--require-webp`가 정상 skip(no_dom_radio)을 실패 처리하던 오판 수정(sharp_unavailable만 실패, 루트 사본 동기) · 렌더러 2줄 제목-부제 겹침 수정(1줄 출력 byte-동일).
- **문서·콘텐츠**: 체크리스트 4종 모드17 동기화(layout-checklist 고아행·"14개" 부패 수리), widget-system h2 강등 규칙 성문화+갤러리 링크 examples/로, editorial 03/05 메타 placeholder→실콘텐츠, Guide --profile 선택 표기.
- **.skill 재패키징**: v5.7.0(16모드) 동결 zip → 현행 v5.10.3 (게이트가 향후 stale 차단).
- **후속 정밀감사 보강**: 예제 visible meta/footer·manifest `examples.purpose`·README/visual-html 현행 문구의 구버전 표기를 v5.10.3으로 정리하고, `output_visible_version_stale`·`current_version_surface_issues`·`.skill` byte-match 게이트를 추가해 manifest 버전만 맞고 표면/zip이 stale인 상태를 차단. 이어 `manifest.quality.governance_count`를 현행 게이트 수 단일 출처로 추가하고 README 현행 표기·실제 self-test count 동기화 게이트를 잠금. `.skill` byte-match 비교에서 `.pytest_cache/`, `__pycache__/`, `*.pyc`, `.DS_Store` 환경 노이즈를 명시 제외. legacy profile alias 표면을 정본 문서·manifest에서 제거하고 parser-only compatibility로 격하하는 게이트를 추가. 거버넌스 124/124.
- 검증: examples 18종 재인라인(코어 해시 갱신) + 프로브 diff = 의도 변화(D1~D6)만 — 베이스라인 `dev-plan/baseline_v5102_probes.json`.

## v5.10.2 (2026-06-10) — github-feature 단락 폭 결함 수정 + R5 게이트 정밀화

전문가 리뷰의 **렌더 실측**에서 발견: `layout-github-feature`(17번째 모드)가 넓은 레이아웃인데도 본문 단락이 46rem(736px)로 좁게 렌더됐다. 형제 `layout-github`은 60rem(960px)인데, v5.10.0에서 17번째 모드 추가 시 theme.css의 60rem 단락 오버라이드 목록 갱신이 누락된 것. 카드·그리드는 974px인데 단락만 736px라 "넓은 화면인데 텍스트만 좁은" 비대칭이 발생했다.

- **theme.css**: 60rem 오버라이드 셀렉터에 `.page-wide.layout-github-feature>section>p/ul/ol` 추가 → github_analysis·expert 등 다른 wide 레이아웃과 동일하게 960px. (코어 CSS 변경 → 코어 해시 `189dd1c5…`→`24d2e3b4…`, theme.css 해시 갱신)
- **R5 게이트 강화**(`validate_output.py`): 기존엔 "스타일에 `60rem` 문자열이 있으면 통과"라, 새 wide 레이아웃이 목록에서 빠져도 못 잡는 blind spot이 있었다(이번 결함이 v5.10.0에서 안 잡힌 이유). 이제 **해당 layout의 `.page-wide.<layout>>section>p` 셀렉터가 실제 존재하는지** 검사하고, wide 인식 목록에 `github-feature`를 추가(github보다 먼저 매칭).
- **examples 18종 재인라인** + `examples/sources/assets/theme.css`·`css-integrity.json`(core+theme.css 해시) 동기화.
- **버전 선언 동기화 + 게이트**: 과거 bump가 manifest/CHANGELOG만 갱신하고 놓쳤던 프로즈 버전 표기를 정리 — SKILL.md 헤더·AGENTS.md(현재 버전 ×3)·README(배지+현행 라벨+changelog 미러)·Guide·skills/README·examples 17 kicker를 모두 5.10.2로 통일. 재발 방지로 `skill_md_version_mismatch` 게이트 신설(SKILL.md `> Version`이 manifest.version과 불일치 시 실패) + 거버넌스 테스트 2종(86→88).
- 측정 확인: github-feature 단락 736px→960px, 형제 레이아웃과 동일. governance·validate·completion_check 통과 유지.

## v5.10.1 (2026-06-10) — 예제 정본화(부록 안티패턴 제거) + 자기정합 게이트 3종

v5.10.0 직후 후속 품질·거버넌스 하드닝. **코어 CSS·17모드·자산은 불변**(core 해시 동일)이라 patch 릴리스다. 전문가 상세 리뷰에서 드러난 "게이트는 통과하지만 스킬 자신의 규칙은 위반"하던 지점을 닫고, 구조적 리스크를 런타임 게이트 + 거버넌스 테스트로 성문화했다.

- **examples 01–14 정본화**: 각 예제 말미의 `mode-template-contract` 부록(자기참조 메타 문구 + 모드 무관 off-topic 위젯 + 부록 전용 vt)을 제거하고, 15–17과 동일하게 **1순위 vt를 본문 콘텐츠 섹션에 실제 주제 데이터로 내장** + **모드 권장 wg 1종을 주제 맞춤으로** 재구성. SKILL §7/Step 4.1(예제 말투·붕어빵·"본문 삽입 증명용 섹션" 금지)을 예제 스스로 준수. (15·16·17은 이미 정본 패턴이라 무변경.)
- **quality_contract 메타문구 게이트**: `quality_contract_check.py`에 `template_demo_meta_phrase`(모드 정본 템플릿 적용 확인/실제 HTML 템플릿으로 삽입했습니다/보강 템플릿으로 포함…)·`template_contract_scaffold`(`data-ahf-contract="mode-template"`) 추가 — 부록형 메타 잔존을 본문에서 차단.
- **manifest 자기정합 게이트**: `manifest_version_consistency_gate` 신설·배선 — `examples.version`/`changes[0]`/`releases[0]`/`updated`가 top-level `version`·CHANGELOG 최신과 어긋나면 실패. v5.10.0 시점 manifest 스테일니스(examples.version 5.9.2·updated 구값·releases 누락) 해소.
- **결정표 자기정합 게이트**: `decision_table_consistency_gate` 신설·배선 — **SKILL §0.6 ↔ validator `MODE_TEMPLATE_CONTRACTS` ↔ `references/widget-system.md` mode→wg 매핑** 3자 일치를 강제. 이에 맞춰 widget-system.md 모드별 권장 wg 표를 §0.6 정본으로 정렬(expert/education/reference/checklist에서 비정본 wg 제거).
- **references 스테일 정리**: `visual-html-system.md` "스킬 4.4.0→4.5.0/20종 적용"을 현행(v5.10.x·21종·17모드 §0.6)으로 재서술, dangling 외부 갤러리 링크(showcase-v6)를 현행 레퍼런스 `examples/`로 재지정. README 재현 명령을 `13-topics`(드리프트로 FAILED) → `examples/`(OK)로 교체.
- **거버넌스 테스트**: manifest·결정표 자기정합 회귀 테스트 추가(**80→86 checks**). `validate_output.py`는 examples 18파일 **OK** 유지, `completion_check.py` 3/3.

## v5.10.0 (2026-06-09) — 17번째 모드 `github_feature_usage` 추가 (GitHub 기능·도입 가이드)

GitHub 저장소를 **"무엇을 해주나·어떻게 쓰나·어디에 맞나"** 기능·사용법·도입 가이드(실제 화면 중심)로 바꾸는 독립 모드 신설. `github_analysis`(실사/리스크/투자판단)와 어조·형식이 달라 별도 레이아웃으로 분리.

- **레이아웃**: `layout-github-feature` + 스캐폴드 `assets/layouts/github-feature-usage.html`. 섹션 모델 = positioning → feature toc → 기능 지도 → 핵심 기능(wg-14) → 기술스택 → 아키텍처 → 디렉토리 → **실제 화면(스크린샷 갤러리)** → 사용자/관리자 기능 → 시작 방법 → 적합성 → 도입 전 확인 → 최종 판단 → next actions → source note.
- **layouts.css**: `layout-github-feature` 섹션 카드 표면(=github 동일) + `.feature-map-grid`·`.feature-screens-grid`(figure/img/figcaption) 추가.
- **검증기**: `MODE_TEMPLATE_CONTRACTS`에 `layout-github-feature`(primary `hero-map`, 권장 `wg-14`/`wg-04`/`wg-16`/`wg-11`/`wg-08`) 등록, toc-map 필수 목록 + `github_feature_usage_contract_gate`(섹션 카드·body-icon·기능지도/실제화면·출처한계) 신설·배선.
- **SKILL.md**: 16→17 모드, §0.6 결정표 행, manifest 기준 트리거 Priority 6 + github_analysis와의 tie-breaker(실사 vs 사용설명), §4 섹션 모델·정량 하한, 템플릿 추천 목록.
- **references**: `github-feature-usage-system.md` 신설(섹션 모델·스크린샷 계약·실사와의 차이·완료 게이트).
- **manifest**: modes 17개·layouts에 `github-feature-usage.html` 등록, version 5.10.0.
- 코어(layouts.css) 변경으로 core 해시 갱신 → **examples 17종 v5.10.0 재인라인 + `examples/sources` 스냅샷·css-integrity 동기화**.
- **github_feature_usage 예제 편입**: smoke output(github-feature-usage-coreline-auth)을 `examples/17_github_feature_usage_coreline_auth.html`로 복사·정합(`layout-github`→`layout-github-feature`, `github-question-toc`→`feature-toc`, `github-verdict`→`feature-verdict`). 실제 화면 스크린샷 8장을 `examples/assets/screenshots/`에 동봉, `examples/index.html` 갤러리에 17번 카드 추가. 디렉터리 검증 0 issue.
- **외부 세리프 폰트 링크 20건 제거**: examples 전반의 `fonts.googleapis.com/css2?family=Noto+Serif+KR` 링크 삭제(v5.9.2 금지·미사용 dead link, `--serif`=Pretendard라 시각 영향 0) → `forbidden_noto_serif_kr_in_output` 해소.
- **wg-03-grid 정합 교정**: 카탈로그-싱크에서 `align-items:start`로 바뀌어 R3 게이트(`wg03_grid_not_stretch`, diff/notes 동일높이)를 위반하던 것을 카탈로그·스킬 모두 `stretch`(정본)로 복원.
- **문서 정합 회귀 방지**: `references/widget-system.md`의 모드별 권장 wg 표를 §0.6 정본과 동기화하고, `SKILL.md` §0.6 ↔ `MODE_TEMPLATE_CONTRACTS` ↔ `widget-system.md` 교차검증 및 `visual-html-system.md` 역사적 갤러리/20종 문구 stale 감지 게이트 추가. 거버넌스 **86/86**.

## v5.9.2 (2026-06-08) — 폰트·decision-tree·toc-map 회귀 방지

- **외부 세리프 폰트 금지**: `Noto Serif KR` 링크·스택·과거 `--serif-kr` 토큰을 제거하고 Pretendard/system sans로 통일. pull-quote/core-insight도 Pretendard 굵은 본문 리듬으로 고정.
- **vt-02 decision-tree 정합성**: 공식 템플릿을 3카드 상단 행으로 보정하고, 카드 제목 margin/line-height 회귀를 `visual-html.css`에서 차단.
- **toc-map 목차 회귀 방지**: 공식 카탈로그의 `toc-map` chip-nav를 analysis 목차 정본으로 승격. `github/youtube/manual` layout wrapper를 `toc-map *-toc`로 맞추고, validator가 구형 `.toc`/bare link 목차를 실패 처리한다.
- **manual layout 보정**: direct section 안의 `div#anchor > h2` 구조도 제목 margin reset 대상에 포함해 카드 상단 85px 공백을 제거. 라이트 테마 `--danger-accent` 누락과 fallback을 보정해 RISK/TROUBLE 왼쪽 라인이 보이게 하고, `qg-final` 판정 문구를 14px/800으로 맞춤.

## v5.9.1 (2026-06-07) — wg-10 figure sheet 모드 데모 섹션 한정 full-width

- **wg-10 svg figure sheet**: `.mode-template-contract .wg-10-sheet{width:100%;max-width:100%}` 추가. 모드 정본 템플릿 데모 섹션 안에서만 카드 전체 폭(1280px 620→974)으로 풀고, 일반 본문의 wg-10은 620px 유지 → 본문 가독성 보존. 스코프 한정 패치(전역 확장 회피).
- 직계 자식 `>` 대신 descendant 셀렉터로 적용(생성기가 위젯을 figure/div로 감싸도 동작). source-order로 base를 덮어 `!important` 불필요.
- examples 17종 재인라인 + `examples/sources` 스냅샷·css-integrity 갱신. 거버넌스 77/77, examples 검증 0 issue.
- **section.lead wrapper reset**: article 예제의 `<section class="lead">`가 theme.css의 prose용 `.lead{max-width:820px}`를 상속해 직접 섹션 카드가 1020→820px로 좁아지는 문제를 layouts.css에서 직접 섹션 한정으로 해소. 텍스트 `.lead` 유틸은 유지.

## v5.9.0 (2026-06-07) — 카탈로그 reverse-sync 반응형·폭·대비 계약 + 시각 정본 게이트

`templates/final_20260604` 카탈로그에서 검증한 시각 QA 패치를 스킬 자산(`visual-html.css`·`widgets.css`)에 정식 편입. 추가 규칙은 모두 source-order로 base를 덮어 `!important` 없이 적용했고, 조건부 CSS만 바뀌어 core 해시는 불변.

- **반응형/overflow(모바일·태블릿)**: vt-03 risk matrix 1열·vt-19 feature-flag·vt-21 soft-workflow·vt-02 화살표 pseudo 중앙정렬·vt-12 타임라인; wg-03 diff(≤900)·wg-04 SVG·wg-06 변형표→Variant 카드(≤760)·wg-07 애니메이션 이동폭 축소·wg-08 뷰포트 가변·wg-15 ring 노드 내측·wg-16 리스크표 카드화(≤900)+플로우 노드 보정.
- **카드 전체 폭(1280px)**: wg-14·wg-15·wg-17 내부 본문 780(max-reading)→974로 확장, 내부 블록 100%·긴 branch/tag/code 줄바꿈·모바일 Before/After 1열·파일 summary 그리드. wg-15는 넓은 화면 ring↔설명 좌우 배치.
- **대비 통일**: wg-02 팔레트 라벨 solid-bg 가독성, CTA/뱃지/wg-13/wg-17/wg-01 강조색 accent-2, wg-20-var solid.
- **vt-12 타임라인 스텝 번호**: 기본 ol marker 제거 → `counter-reset`/`counter-increment`로 빨간 원 안 1·2·3 명시, 390px 선/숫자/카드 미겹침.
- **카탈로그 1:1 동기화(사용자 지시)**: wg-09 가로 슬라이드 deck→반응형 카드 그리드(scroll-snap 제거), wg-07 애니메이션 정적화. 향후 카탈로그↔자산 동기화가 mechanical하도록 일치.
- **시각 정본 게이트 3종 추가**: `direct_section_title_icon_policy_gate`(제목 없는 카드 시작 금지+직접 섹션 h2 body-icon 필수), `body_icon_diversity_gate`(동일 SVG 반복 주입 차단), `mode_template_contract_gate`(diagram/auto는 모드 1순위 vt, widget/auto는 권장 wg 사용 강제).
- **examples 17종 재인라인** + `examples/sources` 자산 스냅샷·`css-integrity.json` 해시 갱신(verbatim·무결성 검증 통과). 거버넌스 77/77, 허용 외 `!important` 0.

## v5.8.1 (2026-06-07) — generated-date 모바일 오버플로 수정(코어)

16모드 예제 전수 캡처 QA(1280/390px, `docs/screenshots/examples-qa-20260607/`)에서 발견된 P0 레이아웃 결함 수정.

- **코어 수정**: `theme.css` `.generated-date`를 `flex:0 0 auto` → `flex:1 1 auto;min-width:0;overflow-wrap:anywhere`. 긴 observed_at/input tier 한 줄이 모바일 390px에서 페이지 가로 스크롤(15번 520px·16번 473px)을 만들던 문제 해소. 긴 헤더 메타를 쓰는 youtube/manual 모드에서 발현.
- **재동기화**: examples 01~16 + index 17개 파일의 인라인 코어 CSS·`adaptive-html-final-core-css-sha256` 마커를 새 해시로 일괄 갱신(verbatim 검증 통과).
- **QA 기록**: 폰트 스케일은 16모드 전수 동일(h1 42/27, h2 29/23, p 16/16) 합격. 관찰 항목 — ⑫ p 15px, 마이크로 폰트(<11px) 5곳, 모바일 표 스크롤 컨테이너 처리(⑧⑩⑪⑭)는 수용 범위로 기록.

## v5.8.0 (2026-06-07) — youtube/manual 깊이 계약 + 넓고-얇음 게이트

8mode 데모에서 youtube/manual 출력이 섹션 수는 최다(12~13 h2)인데 본문은 타 모드의 절반(섹션당 ~310자 vs ~835자+)으로 나온 품질 격차의 근본 원인 4종을 수정했다.

- **예제 증보(앵커 교정)**: `examples/15`(2,916→6,101자)·`examples/16`(2,914→5,973자)를 함대 수준으로 재작성. Evidence Map 6행·타임라인 5항목, 레시피 6필드·감사 지적 3건+원문 위치, h2-sub 9개씩, 무 JS 유지.
- **SKILL.md 정량 하한**: §4 youtube_analysis(Evidence Map 5행+, 타임라인 4항목+, 카드당 2문장+)·manual_analysis(레시피 4개 식별·6필드, 증상 시나리오 3개·4단, 감사 지적 3건+위치) 깊이 하한 명문화. §7 품질 게이트 2줄 추가. “블록 수 충족 ≠ 완료”.
- **참조 문서 증보**: `references/youtube-analysis-system.md`(57→117줄)·`manual-analysis-system.md`(64→127줄) — 블록별 깊이 하한 표, HTML 구성 계약, 흔한 실패 패턴, source note 계약, 완료 게이트 추가(github-analysis-system 수준 정합).
- **검증기 게이트 2종**: `mode_section_depth_too_thin`(layout-* 모드 페이지, h2≥6에서 섹션당 가시 텍스트 평균 400자 미만 차단)과 `profile_vt_template_missing`(diagram/auto 프로파일 모드 페이지의 vt- 0개 = §0.6 위반 차단). index/galleries는 제외. governance 51/51.
- **주의(의도된 breaking)**: 기존 출력 중 vt- 없는 auto 출력과 넓고-얇은 출력은 이제 validate FAILED가 정상이다. 재생성 대상으로 취급한다.

## v5.7.0 (2026-06-07) — YouTube Analysis + Manual Analysis 15·16번째 모드

기존 v5.6.0 QA 보정(core-insight 인용 폰트·risk-* 카드 간격)을 포함한 상태에서 `adaptive-html-final`을 16모드로 확장했다.

- **신규 모드 2종**: `youtube_analysis`(YouTube URL/자막/댓글 → Video Evidence Map, FACT/INFERENCE/UNKNOWN, 댓글 신호, Claim Risk, 재사용 전략)과 `manual_analysis`(매뉴얼 원문 → Source & Version, Reader Role Router, First Success, Safety, Troubleshooting, Runbook) 추가.
- **레이아웃/자산**: `assets/layouts/youtube-analysis.html`, `assets/layouts/manual-analysis.html`, `.layout-youtube`, `.layout-manual`, wide prose-cap 셀렉터 추가.
- **전략/프롬프트**: `references/youtube-analysis-system.md`, `references/manual-analysis-system.md`, `recipes/youtube-analysis.prompt.md`, `recipes/manual-analysis.prompt.md` 추가.
- **검증기**: `validate_output.py`에 YouTube no-embed/evidence/source-limits/observed_at 계약과 Manual role/safety/troubleshooting/source-limits 계약 추가. governance 36/36.
- **예제/산출물**: `examples/15_youtube_vibecoding_gap.html`, `examples/16_manual_product_runbook.html`, output smoke 2종 추가. baseline 4종과 examples 01~16/index는 v5.7.0 자산·manifest·integrity로 재동기화.
- **품질 계약 보강**: layout-first 실행 계약, 임시 제너레이터 금지, 예제/placeholder 문구 금지, 카드/리스트 반복 방지, 기존 검수 예제 대비 후퇴 금지 규칙을 SKILL.md·quality/eval/layout/test 문서에 추가. 보조 검사 `scripts/quality_contract_check.py`로 “validator OK지만 붕어빵 출력”인 회귀를 사전 차단.

## v5.6.0 (2026-06-06) — core-insight 인용 폰트·risk-* 카드 간격(완성본 정합)

final_20260604(완성본) 패턴에 맞춘 2건 QA 수정.

- **core-insight 인용 폰트**: `.core-insight blockquote` `var(--sans)`(Pretendard) → **`var(--sans)` + `font-weight:800` + `letter-spacing:-.02em`**(Pretendard 굵게) — 인용구도 Pretendard 없이 굵은 산세리프로 통일. editorial-patterns.css(CONDITIONAL).
- **risk-\* 우선순위 카드 간격**: `.risk-high/.risk-mid/.risk-low`를 완성본 `.access-check-rule` 방식으로 — `border-left:5px`(라인만) → **자체 카드(`border:1px`+`border-left:4px`+`padding:14px 16px`)**. host(decision-card 유무) 무관하게 좌측 색 라인과 항상 동일 간격. layouts.css(CORE) → 코어 해시 재산정·베이스라인 4종 재동기화.

## v5.5.9 (2026-06-06) — 모바일 표 카드화(#4 정석)

4열 이상 표 42개(examples 14모드)를 `.mobile-card-table` + 헤더 기반 `data-label`로 retrofit. ≤760px에서 thead 숨김·행→카드 전환으로 우측 컬럼 잘림 완전 해소. 스킬 CSS(.mobile-card-table)는 기존, 마크업만 정합. 코어 불변 → 베이스라인 영향 없음.

## v5.5.8 (2026-06-06) — col-list 다단 수정(#6)

`<div class="col-list"><ul>`(바깥 div에 클래스 → grid 미적용) → 정본 `<ul class="col-list">`로 정정(examples 09·10). col-list를 문장 항목에도 자연스럽게: `minmax(170px)→minmax(min(100%,230px))`, 모바일 1열. editorial-patterns.css(CONDITIONAL) 변경 → 베이스라인 재동기화.

## v5.5.7 (2026-06-06) — 레이아웃 QA 수정(캡처 기반)

실제 예제 캡처 QA로 발견한 레이아웃 문제 수정.

- **#2 expert decision-grid**: `.layout-expert .decision-grid:not(section)` → `:not(section)` 제거. `<section class="decision-grid">`도 3열 반응형 grid(세로 적층 회귀 해소, github 패턴과 일치).
- **#3 blog 번호 중복**: `h2:first-child:has(.num)::before{content:none}` — `.num`(빨간 원) 있으면 layout-blog 자동 카운터(회색 원) 숨김(이중 번호 제거).
- **#7 github 좌측 강조선**: 전 섹션 `border-left:4px accent` 반복 제거 → `.github-verdict`(한 줄 결론) 한 곳만(경고 리포트 느낌 해소).
- **#4 모바일 표**: ≤520px에서 일반 표 `min-width:0`(우측 컬럼 잘림 착시 제거). 중요·다열 표는 `.mobile-card-table` 권장.
- **테마바**: box-shadow `0 6px18 .18`→`0 3px10 .10`(상단 그림자 과함 완화).
- examples 14모드 전부 8테마 셸로 재생성(테마바 계약 통일), 09 reference 목차를 `.toc-map`+`.toc-pills` 칩 구조로 교정.

### 영향
- layouts.css·components.css(코어) 수정 → 코어 해시 리베이스, 베이스라인 4종 전체 재동기화. validate 4/4 OK, governance 32/32.

## v5.5.6 (2026-06-06) — 테마 라벨 개선

의미 불명확한 숫자 라벨을 색 성격 기반으로 변경: **라이트2→그레이**(쿨 뉴트럴), **다크2→로즈**(웜 로즈/모브). id(`ahf-light2`/`ahf-dark2`)는 토큰·게이트 안정성을 위해 유지하고 보이는 라벨만 변경.

## v5.5.5 (2026-06-06) — 세피아 테마 추가(8테마)

**세피아**(따뜻한 종이빛 #f4ecd8 + 시에나 accent #a85c32, 저블루라이트 리딩) 추가. 장문 가독성에 최적. 8테마 → 테마바 4+4 균일 그리드.

### 변경
- `theme-dark.css`: `:root:has(#ahf-sepia:checked)` 라이트 종이빛 토큰 블록.
- `body-icons.css`: 세피아 전용 종이빛 아이콘 박스(`linear-gradient(--card,--bg)`).
- `base.html`: 세피아 라디오(8번째).

### 적용
- examples/01 반영(8테마·4+4 균일 확인), 베이스라인 4종 재동기화.

## v5.5.4 (2026-06-06) — 테마 스위처 정형화 버튼 그리드

가변폭 알약(ragged wrap) → **균일폭 버튼 4열 그리드**로 정렬. 7테마가 동일 크기 버튼으로 4+3 배치.

### 변경
- `theme-dark.css` `.ahf-themebar`: `display:grid;grid-template-columns:repeat(4,1fr);width:276px`, 라벨 `justify-content:center;border-radius:9px`, hover 배경. 모든 버튼 폭 동일(검증 63px×7).

### 적용
- examples/01 반영, 베이스라인 4종 재동기화.

## v5.5.3 (2026-06-06) — 스카이블루 테마 추가(7테마)

**스카이블루**(라이트 배경 #eef4fb + 블루 분위기 accent #2f6fdb) 추가. 7테마(라이트·라이트2·스카이블루·화이트·다크·다크2·블루).

### 변경
- `theme-dark.css`: `:root:has(#ahf-skyblue:checked)` 라이트 토큰 블록(블루 accent/analogy). 테마바 `max-width:286px`로 7개 2줄(4+3).
- `body-icons.css`: 흰 아이콘 박스 그룹에 skyblue 합류(`:is(#ahf-white,#ahf-light2,#ahf-skyblue)`).
- `base.html`: 스카이 라디오.

### 적용
- examples/01 반영(7테마·2줄 확인), 베이스라인 4종 재동기화.

## v5.5.2 (2026-06-06) — 테마 스위처 2줄 wrap

6테마로 길어진 `.ahf-themebar`를 **2줄(3+3)** 로 wrap. `display:flex;flex-wrap:wrap;justify-content:flex-end;max-width:208px;border-radius:16px`.

### 적용
- theme-dark.css `.ahf-themebar` 한 줄→두 줄. examples/01 반영, 베이스라인 4종 재동기화.

## v5.5.1 (2026-06-06) — 블루 테마 추가(6테마)

다크2의 완전 토큰 구조를 표본으로 **블루 테마(딥 네이비 #0d1320 + blue accent #5b9cf0)** 추가. 6테마(라이트·라이트2·화이트·다크·다크2·블루).

### 변경
- `theme-dark.css`: `:root:has(#ahf-blue:checked)` 토큰 블록(term/analogy/danger/good/hl/vt 전 토큰) + 다크 동반 규칙을 `:is(#ahf-dark,#ahf-dark2,#ahf-blue)` 공유.
- `body-icons.css`: 아이콘 박스 다크 적응에 #ahf-blue 합류.
- `base.html`: 테마바에 블루 라디오.
- `validate_output.py`: 테마 게이트 라디오 수 `≥3`(확장 테마 자유 추가) 허용. governance 6-radio 통과 케이스 추가.

### 적용
- examples/01에 우선 적용(6테마 작동 확인). 베이스라인 4종 재동기화.

## v5.5.0 (2026-06-06) — CSS-only 5-테마 확장(라이트2·다크2)

final_20260604 표준의 **라이트2(쿨 뉴트럴 gray-blue)·다크2(웜 로즈/모브)** 를 정식 테마로 승격. 3-테마 → 5-테마(라이트·라이트2·화이트·다크·다크2).

### 변경
- `assets/theme-dark.css`: `:root:has(#ahf-light2/#ahf-dark2:checked)` 토큰 블록 추가, 다크 동반 규칙을 `:is(#ahf-dark,#ahf-dark2)` 공유로 전환, 5-세그먼트 스위처.
- `assets/base.html`: 테마바에 라이트2·다크2 라디오/라벨 추가(라이트 기본 유지).
- `scripts/validate_output.py`: 테마 스위처 게이트가 3개(light/white/dark) 또는 5개(+light2/dark2) 허용. 확장 시 light2·dark2 쌍 강제.
- governance 테스트에 5-radio 통과 + 반쪽 확장 거부 케이스 추가.

### 적용
- examples/01_beginner_passkey_login.html에 우선 적용(5-테마 작동 확인). 나머지 예제·산출물은 후속 롤아웃.

## v5.4.2 (2026-06-06) — 텍스트 전용 뷰 bullet(text-bullet-view)

`final_20260604` section 7의 `assets/editorial-patterns.css` code-path bullet 리듬을 정본 헬퍼로 승격. 체크리스트/요약 카드처럼 **텍스트만 있는 뷰**가 카드 안에서 밋밋하게 보일 때, 기존 `.ba-bullet`을 재사용해 작은 써클 마커를 붙인다. 이미 아이콘·번호·상태칩이 있는 뷰에는 중복 적용하지 않는 opt-in 규칙이다.

### 추가 (`assets/editorial-patterns.css`, CONDITIONAL)
- `.text-bullet-view`: flex row + 문장 정렬.
- `.text-bullet-view > .ba-bullet`: 라이트/화이트/다크 토큰 보정. 기존 `.ba-bullet` 재사용, 새 마커 시스템을 만들지 않음.

### 문서
- editorial-pattern-system.md: `text-bullet-view` 마크업과 자동 판단 규칙 추가.
- SKILL.md: editorial-patterns.css opt-in 헬퍼 목록에 `text-bullet-view` 추가.

### 영향
- CONDITIONAL 변경 → 코어 해시 불변. 텍스트만 있는 카드/체크 항목에만 opt-in으로 적용해 기존 레이아웃 회귀 0.

## v5.4.1 (2026-06-06) — 평면 리스트 자동 다단(col-list)

짧은 항목(파일명·태그·키워드)이 6개 이상인 평면 `ul`/`ol`이 세로 1열로 적층돼 가로 공백을 낭비하던 문제를, **다단 그리드(auto-fill, 폭을 꽉 채워 ≈3개+/행)** 로 자동 처리하는 정본 유틸 `col-list`를 신설. 밀도 판단을 스킬이 기본값으로 수행.

### 추가 (`assets/editorial-patterns.css`, CONDITIONAL)
- `ul.col-list`/`ol.col-list` 그리드 + `.col-list li code` 처리. 560px 이하 2열. 스킬 토큰.

### 문서
- editorial-pattern-system.md: `.col-list` 헬퍼 + **자동 판단 규칙**(짧은 항목 6+ → 기본 다단). github-analysis-system.md: references/파일 투어에 col-list 명시.

### 영향
- CONDITIONAL 변경 → 인라인 베이스라인(13-topics, windows-audio, github-analysis) 재인라인+스냅샷+integrity 갱신. 코어 해시 불변. validate OK, governance 29/29.

## v5.4.0 (2026-06-06) — 템플릿 목차 chip-nav(toc-map) 정본 승격

`final_20260604` 쇼케이스에만 있던 **템플릿 목차**(번호 pill이 한 줄에서 wrap 되는 chip-row) 레이아웃을 정본 컴포넌트로 승격. 데모용 `imported-toc-*` 어휘는 denylist에 남기고, 정식 출력용 정본 클래스 `toc-map`/`toc-pills`/`toc-pill`을 신설.

### 추가 (`assets/editorial-patterns.css`, CONDITIONAL)
- `.toc-map`(카드) + `.toc-pills`(flex-wrap) + `.toc-pill`(번호 pill) + `.toc-pill b`(번호 배지) — 모두 스킬 토큰 사용, 3테마 자동 적응(배지 `--accent-soft`/`--accent-2`). 무 JS.
- 리스트형 `.toc`(components.css)와 별개의 opt-in 컴포넌트. 항목이 많거나 가로로 훑게 할 때 사용.

### 문서
- references/editorial-pattern-system.md `callout·변형 헬퍼`에 `toc-map` 마크업/사용 규약 추가. SKILL.md asset 설명 갱신.

### 영향
- CONDITIONAL 자산 변경 → 이를 인라인하는 베이스라인 2종(13-topics, windows-audio) 재인라인+스냅샷+integrity 갱신. 코어 해시 불변. validate 4/4 OK, governance 29/29.

## v5.3.6 (2026-06-06) — code-tour 카드 좌우 정렬

`어디부터 읽으면 되는가`(code-tour)의 repo-card가 파일명(위)+역할(아래)로 세로 적층돼 빈약/날것이던 레이아웃을, **좌우 정렬 row(파일명 좌 · 역할 우)** 로 변경.

### 변경 (`assets/layouts.css`)
- `.layout-github .code-tour .repo-card{display:flex;justify-content:space-between;align-items:baseline}` + h3/p 마진·크기 정리, 패딩 축소.

### 영향
- 코어(layouts.css) 리베이스 → 베이스라인 4종 v5.3.6 재생성, validate OK.

## v5.3.5 (2026-06-06) — 표 풀폭 복원 + 링크 단일행

v5.3.4에서 table을 width:auto로 줄여 빈 공간이 생기던 문제를 되돌림. **풀폭 채움(width:100%)** 유지하면서 효율 배치.

### 변경 (`assets/components.css`)
- `table{width:auto→100%}`, `min-width:420px` 복원 → 표가 컨테이너 폭을 채움(빈 공간 없음).
- `th,td{overflow-wrap:break-word;word-break:keep-all}` 유지 → 긴 토큰(validate_output.py)이 공간 있으면 단일행, 슬랙은 내용 많은 열(설명)이 흡수.
- `td a,th a{overflow-wrap:normal}` 추가 → 표 내 링크(예: commit)가 squeeze된 열에서 `comm/it`로 쪼개지던 문제 해소(링크는 한 토큰 유지).

### 영향
- 코어(components.css) 리베이스 → 베이스라인 4종 v5.3.5 재생성, validate OK.

## v5.3.4 (2026-06-06) — 표 셀 줄바꿈/열폭 정돈 + `.pull-quote--note` 변형 + 검정 `.try` 안 `.hl` 가독성 수정

> 정정: 원래 동일한 `v5.3.4` 번호로 **두 번** 기록돼 있던 항목을 하나로 병합(릴리스 번호 중복 제거).

표 셀의 `overflow-wrap:anywhere`가 auto-layout 최소폭을 ~1글자로 만들어, 공간이 남는데도 긴 토큰(예: `validate_output.py`)이 2줄로 쪼개지고 짧은 열은 과폭이 되던(날것의) 문제 수정. 더불어 본문 인라인 면책/주석 문구가 editorial pull-quote(세리프 20px italic)로 과하게 잡히던 문제와, 검정 `.try` hero CTA 안에서 `.hl`(노란 언더라인 밴드)이 밝은 본문색과 겹쳐 강조어가 묻히던 문제를 **추가형(additive) 규칙**으로 해결. 기존 `.pull-quote`·`.hl` 규칙은 그대로 두어 전 모드 회귀 0.

### 변경 (`assets/components.css`)
- `td,th`를 `overflow-wrap:anywhere` 그룹에서 제외.
- `th,td`에 `overflow-wrap:break-word;word-break:keep-all` 적용 → 열폭이 내용(가장 긴 단어) 기준으로 잡혀 공간 있으면 단일행, 긴 URL/SHA는 넘칠 때만 분리, 한국어는 어절 단위 줄바꿈.
- `.pull-quote--note`(additive): 본문 sans(`var(--sans)`)·15px·upright·`--ink-mute` — pull-quote가 아닌 인라인 주석/면책용 compact 변형(opt-in).
- `.try .hl`(additive): 어두운 `.try` 안에서 언더라인 그라디언트를 솔리드 칩(`background-color:var(--c)`)+`color:var(--ink)`로 전환해 강조어가 선명히 보이도록 보정(`!important` 미사용, `.try .hl` 스코프 한정).

### 영향·검증
- 코어(components.css) 리베이스 → 베이스라인 4종 v5.3.4 재생성, 인라인 core CSS·해시 마커·`sources/assets/components.css`·`css-integrity.json`·매니페스트 콘텐츠 보존 재동기화. governance 29/29, validate OK.

## v5.3.3 (2026-06-06) — github_analysis Next Actions를 검정 hero로 복원

v5.3.2에서 `.try`를 라이트 카드로 바꿨으나, 의도는 **base 검정 hero CTA 유지**였음. `.layout-github>section`(카드)에서 `.try`를 `:not(.try)`로 제외하고 `.layout-github>.try` 오버라이드 전부 제거 → base `.try{background:var(--dark);color:#f5f5f0}`(라이트/화이트/다크 모두 검정 패널 + 라이트 텍스트) 적용.

- `assets/layouts.css`: `.layout-github>section:not(.try)`, `.layout-github>.try` 오버라이드 삭제.
- 코어 리베이스 → 베이스라인 4종 v5.3.3 재생성, validate OK.

## v5.3.2 (2026-06-06) — github_analysis Next Actions(.try) 배경 버그 수정

`layout-github`의 최종 `.try`(Next Actions)가 텍스트만 `var(--ink)`로 바꾸고 배경은 base `.try{background:var(--dark)}`(라이트에서 검정)를 그대로 둬, **라이트 테마에서 검정 배경 + 어두운 텍스트(거의 안 보임)** 로 나오던 버그 수정.

### 변경 (`assets/layouts.css`)
- `.layout-github>.try`에 `background:var(--card)` + border(+left accent) 추가 → 라이트=라이트 카드/어두운 텍스트, 다크=다크 카드/밝은 텍스트로 테마 추종.
- `.label`(accent-2)·`strong`(ink)·`a`(accent-2)·`h2 .no/.num`(accent bg) 대비 보정.

### 영향·검증
- 코어(layouts.css) 변경 → core-css-sha256 리베이스. 게이트 통과 베이스라인 4종(13-topics·github_analysis·windows-audio·grok-india) v5.3.2 재생성, validate OK.

## v5.3.1 (2026-06-06) — 완성본(reference) 표준화: 페이지-로컬 디자인을 스킬 기본값으로 승격

`windows-audio-pcm-reference`(완성본, v5.2.3)에만 page-local로 있던 핵심 디자인을 **스킬 기본값으로 승격**해, 신규 출력(예: github_analysis v5.3.0)이 완성본과 다르게 회귀하던 문제를 근본 해소. 무 JS, `!important` 0.

### 승격 (회귀 안전 배치)
- **layouts.css(코어)**: `.page/.page-wide > section:not([class])`(+article) 무클래스 콘텐츠 섹션을 카드 뷰(`var(--card)`+border+radius+padding)로 감싸고 첫 h2 top-margin 리셋. 13-topics 전 13모드에서 이미 검증된 규칙.
- **theme.css(코어)**: `.header .kicker` 폰트 11px·축소 패딩, `.header .sub{text-align:justify;word-break:keep-all}` — 헤더 리듬 표준화.
- **components.css(코어)**: `.source-note{background:transparent}` — 최하단 노트 평면.
- **body-icons.css(조건부)**: `h2/h3 > .body-icon{42px}` — 섹션 제목 앞 큰 아이콘.
- **visual-html.css(조건부)**: `.vt-frame{background:transparent;border:0}` — 다이어그램 내부 박스 평면(외곽 vt-shell 단일 뷰).

### 회귀 방지 결정
- **core-insight는 승격 제외**: bare `.core-insight` 전역 오버라이드는 accent-gradient hero 콜아웃을 전 모드 회귀시키므로, 기존 `.core-insight--neutral` opt-in 모디파이어로만 평면 처리(스킬 안전장치 유지).

### 영향·검증
- 코어 자산(theme/components/layouts) 변경 → **core-css-sha256 리베이스**. 게이트 통과 베이스라인(13-topics·github_analysis·windows-audio-reference)을 v5.3.1로 재생성(재인라인·코어 마커·스냅샷·css-integrity), page-local 중복 제거, `validate_output.py` **OK** 유지.

## v5.3.0 (2026-06-06) — GitHub Analysis 14번째 모드 추가

GitHub 저장소 URL 또는 `owner/repo` 입력을 사용자 질문 중심의 HTML 실사 리포트로 변환하는 `github_analysis` 모드를 추가했다. 목적은 README 재요약이 아니라 “이 저장소를 이해·실행·채택·감사해도 되는가?”를 판단하게 하는 것이다.

### 추가
- **신규 모드**: `github_analysis` — priority 5, layout `github-analysis.html`, class `.layout-github`.
- **신규 레이아웃**: `assets/layouts/github-analysis.html` — verdict, question toc, repo identity, quickstart readiness, repo health, code tour, releases/roadmap, security/license, risk matrix, final decision, next actions, source note.
- **신규 CSS**: `assets/layouts.css`에 `.layout-github` repo signal/card/grid 스타일 추가.
- **와이드 폭 보정**: `assets/theme.css`의 `.page-wide` prose override에 `.layout-github`를 포함해 GitHub 분석 본문이 1020px 와이드 레이아웃 리듬을 따른다.
- **신규 전략 문서**: `references/github-analysis-system.md` — FACT/INFERENCE/UNKNOWN 분리, GitHub 표면별 수집 항목, 판단 모델, source note 계약.
- **신규 recipe**: `recipes/github-analysis.prompt.md`.
- **개발 계획**: `dev-plan/implement_20260606_003800.md`.

### 매핑
- vt 1순위: `hero-map`; 보강: `quality-gate`, `file-tour`, `risk-matrix`, `timeline`, `decision-tree`, `checklist-flow`.
- wg 1순위: `wg-11 Weekly Status`; 보강: `wg-04 Module Map`, `wg-14 Feature Explainer`, `wg-16 Implementation Plan`, `wg-17 PR Writeup`, `wg-18 Ticket Triage Board`.

### 영향·검증
- `manifest.json` 버전 `5.3.0`, modes/layouts 14개로 갱신.
- `AGENTS.md`, `SKILL.md`, `references/mode-selection.md`, layout/visual/widget/writing references, tests/golden prompts/checklists, README/Guide 동기화.
- `layouts.css`가 코어 CSS 자산이라 신규 출력의 core-css-sha256은 재계산이 필요하다. 기존 `13-topics` 산출물은 v5.2.3 캐노니컬 기준선으로 유지하며, 14-mode 쇼케이스 재생성은 후속 작업이다.

## v5.2.3 (2026-06-05) — editorial-patterns 가독성 승격

쇼케이스에서 반복 적용하던 일반 가독성 보정을 스킬 기본값으로 승격. 무 JS, `!important` 0, 조건부 자산(`editorial-patterns.css`)만 변경 — **코어 해시 불변**.

### 변경 (`assets/editorial-patterns.css`)
- **`.a11y-card`** 내부 줄 간격 `gap:8px → 12px`, **`.a11y-points`** `gap:5px → 9px` — 접근성 점검 카드의 헤드/제목/PASS·FAIL 줄이 너무 붙던 문제 완화.
- **`.impact-card .body-icon`** `display:grid;margin-bottom:12px` 추가 — impact 카드에서 아이콘이 제목/수치에 바로 붙던 문제 해소(아이콘 ↔ 텍스트 12px 간격).

### 영향·검증
- `editorial-patterns.css`는 조건부 자산이라 **core-css-sha256 불변**. `13-topics` 공개 데모 산출물의 인라인 `editorial-patterns.css`·스냅샷·`css-integrity.json`·source manifest를 v5.2.3로 재생성, `validate_output.py` **OK** 유지.

## v5.2.2 (2026-06-05) — 아이콘 박스 테마 적응 + lede-note 라벨 정렬

쇼케이스/템플릿 점검에서 확정된 보편 결함을 스킬 기본값으로 승격. 무 JS(`:has()`), `!important` 0, 조건부 자산(`body-icons.css`)만 변경 — **코어 해시 불변**.

### 변경 (`assets/body-icons.css`)
- **아이콘 박스 배경 테마 적응**: `.body-icon` 박스 배경이 하드코딩 흰빛 그라디언트라 다크/화이트 테마에서 그대로 떠 보이던 문제를 해소. `:root:has(#ahf-white:checked)`=순백, `:root:has(#ahf-dark:checked)`=카드 표면(`var(--vt-soft)`→`var(--card)`, border `var(--line)`). 라이트는 기존 크림빛 유지. SVG 칠(bi-*)은 이미 토큰 기반이라 그대로 적응.
- **lede-note 라벨 정렬**: `.lede-note .label{display:block}`(고특이도)이 v5.2.1의 `.label:has(>.body-icon){display:flex}`를 무력화하던 문제를 `.lede-note .label:has(>.body-icon)`(0,3,0)로 보강.

### 영향·검증
- `body-icons.css`는 조건부 자산이라 **core-css-sha256 불변**. `13-topics` 공개 데모 산출물의 인라인 `body-icons.css`·스냅샷·`css-integrity.json`(conditional hash)·source manifest를 v5.2.2로 재생성, `validate_output.py` **OK** 유지.
- 같은 결함을 가진 `final_20260604` 반례 데모도 향후 재인라인 시 자동 적용.

## v5.2.1 (2026-06-05) — body-icon 정렬 규칙 + 헤더 폭 정련

쇼케이스 인덱스 검수에서 확정된 정렬·폭 개선 2건을 스킬 기본값으로 승격. 전부 무 JS(`:has()`), `!important` 0.

### 변경
- **`assets/body-icons.css`**: `body-icon`을 직접 자식으로 갖는 `.label`/`h1`/`h2`/`h3`를 **flex 왼쪽 아이콘 + 일정 간격(gap 8~10px)**으로 정렬. `.mini-card`/`.card-block` 카드 제목 아이콘은 2줄 제목에서 상단 정렬(`align-self:flex-start`). 헤딩·라벨 전반의 아이콘↔텍스트 간격 일관화.
- **`assets/theme.css`**: `.header` 콘텐츠의 **48rem 단일 측정 캡 해제**(`max-width:none`). 헤더가 `.page`/`.page-wide` 컨테이너 폭에 맞춰 **아래 섹션과 동일 폭**으로 정렬(특히 wide 레이아웃에서 헤더가 768px로 좁던 문제 해소).

### 영향·검증
- `theme.css`가 코어 해시 자산이라 **core-css-sha256 변경** → `13-topics` 공개 데모 기준선의 인라인 CSS·코어 마커·CSS 스냅샷·`css-integrity.json`을 v5.2.1로 재생성, `validate_output.py` **OK** 유지.
- 인덱스 전용 미세 튜닝(상단 kicker 폰트 11px, 인트로 `text-align:justify`)은 갤러리 취향이라 스킬에 승격하지 않고 해당 `index.html` 페이지-로컬 오버라이드로만 유지.

## v5.2.0 (2026-06-05) — CSS-only 3-테마 시스템 (라이트·완전 화이트·다크)

기존 라이트(크림)/다크 2-테마에 **완전 화이트(순백) 테마**를 추가해 **3-테마**로 확장. 단일 체크박스 토글을 **라디오 3-세그먼트 스위처**(`name=ahf-theme`: `#ahf-light`/`#ahf-white`/`#ahf-dark`)로 교체. 전부 `:has()` 기반 **무 JS**, 코어 CSS 무수정(해시-safe), `!important` 0.

### 추가/변경 (`assets/theme-dark.css` → 테마 시스템)
- **화이트(순백)**: `:root:has(#ahf-white:checked)` — neutral 토큰만 쿨·순백(`--bg/--card #fff`, `--line #e4e4ea`, `--ink #16181d`, `--vt-* #fff`); accent·콜아웃 유지. 라이트(크림 `#f5f5f0`)와 명확히 구분.
- **다크**: `:root:has(#ahf-dark:checked)` + 표면 보정(이전과 동일, proper-black `#0c0d10`).
- **스위처**: `.ahf-themebar` 세그먼트 컨트롤(숨긴 라디오 + 라벨, `input:checked + label`=accent 활성, focus-visible 링). 기본=라이트, 마크업 없으면 라이트 고정.
- 이전 `#theme-toggle` 체크박스(invert) 방식은 3-라디오로 대체.

### 검증
- Playwright 3-테마 전환 실측: body bg 라이트 `#faf9f5` / 화이트 `#ffffff` / 다크 `#0c0d10`. 화이트 ink/bg 17.8:1. self-test 16/16.

### 후속 하드닝 (5.2.0 라인 · 2026-06-05)
- **결정론 문서 동기화** (`AGENTS.md`·`SKILL.md`): 버전 하드코딩 제거(→ `manifest.json` 일치), CSS 순서표·슬롯 인덱스에 `theme-dark.css`/`{{THEME_DARK_CSS}}` 추가(누락됐던 `SHAPE_VISUALS`/`WORKFLOW_VISUALS` 포함), 테마 스위처(`name="ahf-theme"`) 삽입 규칙 + 불변식 "3-테마 단일 계약"(legacy `#theme-toggle` 금지), `auto = 혼합/기본(auto≠diagram)` 명확화, 본문 구조 패턴 **8종**(`accessibility-checklist` 포함, 템플릿 `01..08`) 정정.
- **검증기 강화** (`scripts/validate_output.py`): (1) 조건부 CSS 스냅샷·`asset_sha256` 기록 해시를 현재 스킬과 대조(있을 때만; stale `theme-dark.css` 등 차단), (2) source manifest를 버전만이 아닌 **내용 전체** 비교(`source_manifest_content_mismatch`), (3) legacy `#theme-toggle` 가드(`legacy_theme_toggle`). self-test 16 → **24** (legacy-toggle fixture 3종 추가).
- **M6 모바일 표/매트릭스**: `<table>` 보유 위젯(`wg-06`/`12`/`15`/`16`)을 `.table-scroll`로 래핑(`table_no_mobile_safe_wrapper` 게이트 충족), vt-03 리스크 매트릭스 `.rm-grid`에 모바일 규칙(`minmax` 바닥 + `overflow-x:auto`) 추가.
- 쇼케이스 출력(`13-topics`)을 현재 자산으로 재인라인·재스냅샷, `.skill` 재패키징(stale `__pycache__/*.pyc` 정리).

## v5.1.0 (2026-06-05) — 글꼴(Pretendard sans 제목)·헤더 반영 + proper-black 다크 (디자이너 검토)

`final_20260604` 디자인 소스의 **글꼴**과 **헤더 섹션(SVG 제외)**을 스킬에 반영하고, 다크 테마를 **"proper black"**으로 교정했다. 전문 시각 디자이너 + 레이아웃 스타일 디자이너 에이전트 2인 검토 결과를 반영. 코어 해시 재베이스라인(`b04221bd…`→`fea7b026…`). 무 JS·코어 `!important` 0 유지.

### 글꼴 — report 룩(sans 제목)
- `--serif` 토큰을 Pretendard sans 스택으로 전환(제목·디스플레이가 Pretendard → Pretendard sans). 진짜 세리프는 `--sans`로 보존하고 `blockquote`/`.pull-quote`/`.core-insight blockquote`에만 적용(에디토리얼 대비).
- 디자이너 검토 반영: sans 제목은 700→**800** 무게 + 트래킹 강화(h1 -.025em/lh1.22, h2 -.02em/lh1.3, h3 -.015em).

### 헤더 — final_20260604 반영(SVG 제외)
- `.kicker`를 **점 달린 pill eyebrow**로(토큰화 → 다크 자동). `.kicker-text` 추가.
- `.generated-row` + `.generated-date` + `.lens-strip` + `.lens-strip-label` + `.lens-chip`(적용 기준 칩) 추가 — 페이지 warm 리터럴을 쿨 토큰으로.
- no-SVG 단일 컬럼 헤더에 **측정 캡**(`.header` 자식 `max-width:48rem`)으로 제목/본문 우측 정렬. 헤더 리듬 재튜닝(kicker→h1 24, meta 24, generated-row 16, `--space-*` 정렬).

### 다크 — proper black (디자이너 P1)
- 팔레트 교정: `--bg #15161a→#0c0d10`(near-black), `--card #1e2026→#1a1c22`(lifted, 카드 분리), `--line→#2c2d34`, `--dark→#000`(true-black `.try` hero), `--code→#070809`.
- **AA 교정**: `--on-accent` 토큰 신설(라이트 `#fff`, 다크 `#0c0d10`) — accent 버튼/배지 흰 텍스트의 AA 미달(라이트 4.17·다크 2.76)을 해소(다크 on-accent 7:1). `.cta-btn.primary`·`h2 .no.is-key`에 적용.
- **다크 커버리지 갭 차단**: `widgets.css`·`visual-html.css`의 흰 카드 `background:#fff` 38곳을 `var(--card)`로 토큰화(라이트 동일, 다크 자동 반전) — 위젯/vt 템플릿이 다크에서 흰 섬으로 남던 문제 해결.
- **"전혀 블랙이 아니다" 근본 원인 수정(실제 렌더 캡쳐로 진단)**: `visual-html.css`가 `body{background:var(--vt-wash)}`로 페이지 배경을 자체 `--vt-*` 토큰(다크 미적용)으로 덮어 다크에서도 `#faf9f5`(밝은 wash)로 남던 버그. theme-dark가 `--vt-paper/--vt-wash/--vt-soft`(+ vt-blue/green/gold 명도 상향)를 다크로 덮도록 추가 → body 배경 `#0c0d10`(near-black) 확정(Playwright 캡쳐 검증). `widgets.css` 흰 글레이즈 `rgba(255,255,255,…)` 7곳→`var(--card)`(wg-11 빗금 보존), `.core-insight` 흰 글레이즈 그라데이션→다크 그라데이션, vt-pill.hot/good/watch 다크 틴트. theme-dark 토글 `th,.table th` 콤마 스코프 누수 수정.
- **양방향 토글 수정(OS 다크에서 화이트 전환 불가 버그)**: 기존 토글은 dark를 "추가"만 해서 OS가 다크면 토글로 라이트 복귀가 불가능했음. **invert 패턴**으로 재작성 — `@media(prefers-color-scheme:dark) :root:not(:has(#theme-toggle:checked))`(OS다크 기본 다크, 토글 시 라이트) + `@media(light/no-preference) :root:has(#theme-toggle:checked)`(OS라이트 토글 시 다크). 4조합(OS×토글) 전부 검증: light/dark/dark/light. 아이콘은 현재 테마 표시(다크=달/라이트=해). 토글 마크업 없으면 OS 자동만 동작.
- **다크 텍스트 대비 감사(Playwright로 전 텍스트 노드 대비 계산 + 풀페이지 캡쳐)**: 안 보이는 텍스트 패치 — `.try .tag`(밝은 pill+`var(--ink)` 텍스트가 다크에서 light-on-light 1.18:1 → 다크 pill `var(--card)`/`var(--line)`로 보정), `visual-html.css`의 `.vt-pill`·`.vt-fit`(`color:#555`)·`.vt-tags span`·`.cf-state`(`#666`)·`#6e6258` + `widgets.css` `#7c7c78` 리터럴 회색 텍스트를 `var(--ink-mute)`로 토큰화(다크 자동 반전). 종합 kitchen-sink 데모에서 저대비 텍스트 **0건** 확인.
- theme-dark 토글 블록의 `th,.table th` 셀렉터 스코프 버그 수정(콤마로 인한 라이트 누수 차단).

## v5.0.0 (2026-06-05) — Tranche B: 다크 테마 + 코어 프리미티브 업그레이드 (코어 해시 재베이스라인)

`final_20260604` 병합 Tranche B. **토큰 전용 다크 테마**를 추가하고, 코어 프리미티브(`.cta-box`/`.serp-*`/`.platform-card`)를 "replace-the-primitive"로 제자리 업그레이드했다. 후자가 **코어 5개 동결 자산(theme/components/visual-components/layouts/print)을 수정**하므로 코어 해시가 재베이스라인된다(메이저 범프). 골든 v6는 v4.x 역사 베이스라인으로 남는다. 페이지 발명 어휘(`landing-action-*`/`seo-result-*`/`platform-conversion-*`)는 도입하지 않고 기존 정본 클래스만 강화. 무 JS·`!important` 0(코어) 유지.

### 추가 — 다크 테마 (hash-safe, 코어 무수정)
- `assets/theme-dark.css` — **토큰 전용 `:root` 오버라이드**(37개 색 토큰). `@media(prefers-color-scheme:dark)` 1순위 + **라이트 기본** + 선택적 `:root:has(#theme-toggle:checked)` 강제 다크. 페이지의 116-클래스 `!important` 열거는 폐기. 표면 보정 6개(prompt-box/code/th/status-pill/timeline-card/serp-url)만, `!important` 0.
- `base.html`에 `{{THEME_DARK_CSS}}` 슬롯(print 뒤) + manifest `dark_theme` 블록 + `references/editorial-design-system.md` 다크 테마 절. 선택 토글 버튼(체크박스+라벨, 무 JS).

### 변경 — 코어 프리미티브 업그레이드 (코어 해시 재베이스라인)
- `.cta-box`(components.css): `.cta-actions`/`.cta-btn`(44px 터치, primary/secondary)/`.cta-proof-grid`/`.cta-proof` 추가. translateY hover에 `prefers-reduced-motion` 폴백.
- `.layout-seo .serp-*`(layouts.css): `.serp-desc`/`.serp-dots`(검색 점열)/`.serp-checks`(칩, `.ok`)/`.serp-rule-grid`/`.serp-rule`(`.is-wide`) 추가. 전부 `.layout-seo` 스코프, `--report-sans`→`var(--sans)`, dot hex 토큰화.
- `.layout-platform .platform-card`(layouts.css): 채널 코딩 `.is-search/.is-dev/.is-story/.is-essay` 좌측 보더(토큰) + `.platform-kicker`. 제네릭 충돌 방지 위해 `.layout-platform` 스코프 + `is-` 접두.

### 게이트 (부수 개선)
- 자산 린터를 **주석-인식**(`/* */` 마스킹)으로 교정(prose 속 `!important` 오탐 차단) + `theme-dark.css`를 `important_in_core_css` 린트 대상에 편입. self-test 16/16.

### 비고
- 코어 해시 변경: v4.x `3e6a8bfa…` → v5 `b04221bd…`. 기존 출력물은 재검증 시 해시 불일치(재생성 필요). 새 데모는 v5 해시로 재생성됨.

## v4.6.0 (2026-06-05) — final_20260604 섹션 Tranche A 흡수 & 병합 보호 게이트

`final_20260604`(무신뢰 디자인 소스)의 섹션 패턴 중 **재사용 가치가 검증된 9종을 흡수**했다. 페이지 발명 어휘(`access-*`/`edge-*`/`pattern-hero-note`/`static-flow-*`/`vt-flag`/`fi-*`)는 모두 **정본 네임스페이스로 개명**하고, `!important`·`--report-sans`·warm 리터럴·베어 콜아웃 충돌을 제거한 뒤 토큰화했다. 코어-해시 5개 자산(theme/components/visual-components/layouts/print)은 **무변경**(전부 hash-safe 경로). 무 JS 원칙 유지.

### 추가 (Phase 0 — 병합 보호 거버넌스 게이트)
- `scripts/validate_output.py` — 자산 린터 3종(`important_in_core_css`, `forbidden_report_font_token`, `bare_callout_modifier`) + 출력 게이트 2종(`bespoke_namespace_class` denylist, `role_img_buries_text` 일반화). `--skill-dir` 제공 시 스킬 자산을 린트.
- `tests/test_governance_gates.py` — 게이트 16개 체크 stdlib 자체 테스트(회귀 방어).

### 추가/변경 (Phase 1 — Tranche A 9종 병합)
- editorial 패턴 **08 `accessibility-checklist`** 신규(`a11y-*`): 30분 점검 그리드 + 실패 모드 표(caption+`.table-scroll`) + 다크 릴리스 체크. 상태는 PASS/FAIL **텍스트 칩**(색 외 단서). `editorial-pattern-templates/08-accessibility-checklist.html`, manifest editorial_patterns 7→8.
- callout·헬퍼(opt-in, 패턴 수 미증가): `.lede-note`(←pattern-hero-note), `.source-preserve-static`, `.core-insight--neutral`, before/after `.ba-emphasis-line`+`.ba-bullet`.
- `.md-excerpt .code` 긴 줄 줄바꿈(`pre-wrap`+`overflow-wrap:anywhere`).
- vt-19 feature-flag **3-상태 토글**(`.switch.on/.warn/.off`) + 가시·SR 텍스트 라벨(`.flag-state`) — 색-단독 회귀 해소.
- `wg-11` ≤480px 라벨 적층 + 상태/거버넌스 보드 정본 통일(빗금 `wg-11-fill-risk` 비색 단서 보존).
- `wg-08-static-*` — `:target/:has` 없는 읽기전용 스테퍼(←static-flow-*).

### 추가 (Phase 3 — 인-스킬 갤러리)
- `galleries/body-icons-catalog.html`(32종)·`galleries/soft-shapes-catalog.html`(36종) — 외부 산출물 경로 링크를 인-스킬 데모로 재배치. `body-icons.css`/`shape-visuals.css`는 프리미티브 전용 유지. manifest에 catalog/gallery 필드 등록.
- `pattern-shell`을 **데모 하네스**(콘텐츠 패턴 아님, 정식 출력에선 denylist)로 문서화.

### 비고
- Tranche B(토큰 전용 다크 테마 + CTA/SERP/platform 코어-해시 제자리 업그레이드)는 v5.0.0에서 별도 진행. 전략: `MERGE_STRATEGY_final-20260604.md`.

## v4.5.0 (2026-05-31) — SVG→HTML 템플릿 편입 & 하네스 정형화

SVG로 그리던 본문 삽입 다이어그램을 순수 HTML+CSS 뷰 템플릿(`vt-`)으로 정식 편입하고, 이후 vt-21 `soft-workflow-map`까지 포함해 현재 21종으로 확장했다. 모드→템플릿 결정론 진입점과 정적 게이트로 하네스를 정형화했으며, 무 JS 원칙(외부/동작 JS 0, JSON-LD만 허용)은 전 항목에서 유지된다.

### 추가
- `assets/visual-html.css` — SVG→HTML 뷰 템플릿 21종 스타일.
- `assets/visual-html-templates/01..21.html` 21종 — `vt-` 본문 삽입 다이어그램 골격(hero-map, decision-tree, risk-matrix, timeline, checklist-flow, quality-gate, card-grid, raci, file-tour, flowchart, weekly-status, incident-summary, comparison-cards, process-swimlane, concept-explainer, implementation-plan, pr-writeup, triage-board, feature-flag, prompt-tuner, soft-workflow-map).
- `references/visual-html-system.md` — 캐노니컬 모드→vt 템플릿 매핑(첫=1순위, 단일 출처), 선택·삽입 규칙.
- `AGENTS.md` — 결정론 진입점(모드 입력→vt 선택을 단일 출처로 고정).

### 캐노니컬 모드→vt 매핑 (첫=1순위, 단일 출처)
- beginner_html: concept-explainer, hero-map, checklist-flow
- expert_html: risk-matrix, raci, quality-gate, implementation-plan, soft-workflow-map
- article_html: decision-tree, comparison-cards, concept-explainer
- education_html: timeline, checklist-flow, concept-explainer, soft-workflow-map
- blog_writer: timeline, weekly-status, comparison-cards
- seo_dashboard: card-grid, comparison-cards, prompt-tuner
- platform_blog: card-grid, comparison-cards, pr-writeup
- skill_audit: quality-gate, file-tour, prompt-tuner, implementation-plan, soft-workflow-map
- reference_html: file-tour, flowchart, card-grid
- comparison_html: comparison-cards, decision-tree, risk-matrix
- case_study_html: incident-summary, timeline, process-swimlane
- landing_brief_html: hero-map, card-grid, feature-flag, soft-workflow-map
- checklist_playbook: checklist-flow, quality-gate, process-swimlane, implementation-plan, triage-board

### 변경
- `SKILL.md`: 모드→vt 결정표 추가(캐노니컬 매핑을 단일 출처로 참조).
- `assets/base.html`: `{{WIDGETS_CSS}}` 슬롯 바로 뒤에 `{{VISUAL_HTML_CSS}}` 슬롯 추가(인라인 순서 widgets → visual-html → layouts 유지).
- `scripts/validate_output.py`: `vt-` 게이트 추가(visual-html 템플릿 사용 시 정적 검사).
- `manifest.json`: 버전 4.5.0, assets에 `assets/visual-html.css` 추가, `visual_html_templates` 배열(01~21) 등록, changes 항목 추가, updated 2026-05-31.

### 적용 데모
- `showcase-v6` — 동결 시점 기준 SVG→HTML 템플릿 20종을 모드별로 적용한 골든 갤러리(vt-21은 후순위 편입이라 골든 본문에는 필수 등장하지 않음).

### 검증
- `assets/visual-html-templates/*.html` 21종 모두 외부/동작 `<script>` 0건(무 JS 0, JSON-LD만 허용).
- `manifest.json` `python json.load` 유효성 통과, `visual_html_templates` 21개 실제 파일 경로 일치.

### 본문 아이콘 세트 편입 (2026-06-01)
본문용 compact 아이콘 32종을 정식 편입했다. 섹션 제목·콜아웃·카드 옆에 의미를 보조하는 인라인 SVG 장식(외부/동작 JS 0, `aria-hidden="true"`)이며 스킬 디자인 토큰을 쓴다.
- `assets/body-icons.css` — `bi-` 네임스페이스 렌더 CSS(8 클래스: line/accent-line/fill/soft/accent/accent-box/dot/dot-box) + `.body-icon`/`--sm`/`--plain` 래퍼. 프로파일 무관 조건부 인라인.
- `assets/body-icons.json` — 32종 `{id, label, usage, svg}`(viewBox 0 0 40 40). id: idea·source·timeline·connection·edit·check·impact·reference·warning·success·question·compare·decision·metric·search·file·code·database·security·user·flow·map·quote·note·learning·platform·audit·case·landing·api·prompt·experiment.
- `references/body-icon-system.md` — 32종 카탈로그·모드별 추천·삽입/접근성 규칙.
- `assets/base.html`: `{{BODY_ICONS_CSS}}` 슬롯 추가(visual-html 뒤). `manifest.json`: assets + `body_icons` 메타(count 32).
- `scripts/validate_output.py`: body-icon 게이트(아이콘 사용 시 body-icons.css 인라인·`aria-hidden` 강제).

### wg-03 PR diff 가시성·정렬 수정 + md-excerpt 패턴 (2026-06-01)
skill_audit "좋은 출력은 어떻게 생겼나"(주석 달린 PR) 섹션의 두 결함과 SKILL.md 발췌 표기를 보강했다.
- `assets/widgets.css` wg-03: diff 코드가 안 보이던 버그 수정 — `<code class="wg-03-code">`가 코어 `code{background:#ececea}`(밝음)에 덮여 밝은 텍스트가 밝은 배경에 묻혔다. `.wg-03-diff code,.wg-03-code{background:none;border:0;border-radius:0;font-size:inherit}` 리셋으로 다크 diff 패널에 코드가 보이게. (wg-01/13/14는 `.wg-XX-code`에 다크 배경을 직접 줘서 무관.)
- `assets/widgets.css` wg-03 정렬: `.wg-03-grid{align-items:stretch}` + `.wg-03-diff{align-self:stretch}`로 diff(좌)·리뷰 노트(우)를 **같은 높이로 통일**(이전 `align-items:start`로 좌측이 짧아 우측과 틈 발생).
- `assets/editorial-patterns.css` + `editorial-pattern-templates/07-md-excerpt.html`: **md-excerpt 패턴** 추가(7번째) — SKILL.md/마크다운/코드 발췌를 `.prompt-box` 텍스트가 아니라 다크 코드 블럭(`pre.code`)에 마크다운 소스 그대로 표기.
- `references/skill-audit-system.md`·`editorial-pattern-system.md`: 발췌=코드블럭, 주석 PR=wg-03 다크 diff·stretch 정렬 규칙 명문화. `manifest.json` editorial_patterns count 6→7.
- 적용: showcase-v5 page 08 — wg-03 diff 코드 가시·좌우 475=475 균등, SKILL.md 발췌 3종 코드블럭화(콘텐츠 무변경). validate OK·무 JS 0.

### 자체 검증 회귀 게이트 강화 R1–R5 (2026-06-01)
지금까지 실측 수정한 결함이 다시 발생하지 않도록 `scripts/validate_output.py`에 정적 회귀 게이트 5종을 추가하고, `references/quality-gates.md`에 "v4.5.0 Regression Gate"로 명문화했다.
- **R1 `platform_grid_wrapper_misuse`** — `div.platform-grid`에 `<h2>`/`.card-grid`/`.h2-sub`를 중첩하면 검출(카드 직접 보유만 허용, 섹션 래퍼는 `<section>` 사용).
- **R2 `wg03_diff_code_bg_not_reset`** — wg-03 **마크업** 사용 시 `.wg-03-diff code{background:none}` 리셋 누락 검출(다크 diff 코드 가시성).
- **R3 `wg03_grid_not_stretch`** — `.wg-03-grid{align-items:stretch}` 누락 검출(좌우 컬럼 높이 통일).
- **R4 `table_no_mobile_safe_wrapper`** — `.table-scroll`/카드 변환 없는 `<table>` 검출(모바일 가로 넘침 방지).
- **R5 `wide_layout_prose_cap_missing`** — `.page-wide` 분석 폭 레이아웃에 본문 60rem 상한 override 누락 검출(와이드 섹션 본문이 1/3만 차는 문제).
- 검증: R2/R3은 인라인 widgets.css의 CSS 텍스트가 아니라 **wg-03 마크업 사용**에서만 발동하도록 정밀화(widget/auto 프로파일 오발동 0). 3 프로파일 골든(widget/auto/diagram) 전부 `OK` 유지, 픽스처 10/10 통과.

### vt-21 soft-workflow-map 편입 (8816, 전문가 검토 반영, 2026-06-01)
크림톤 "AI 카드뷰" 워크플로우 맵을 본문 삽입 HTML+CSS 다이어그램으로 vt- 라이브러리에 **vt-21**로 편입(20→21종). 아키텍처/IA + QA/접근성 2인 전문가 검토 후 진행.
- `assets/visual-html-templates/21-soft-workflow-map.html` — `vt-shell`/`vt-frame` 셸 + `wf-` 접두사. 좌 3카드 ∥ 중앙 대시보드(코드창·미니대시·지표·파이프) ∥ 우 3카드 수렴형(기존 hero-map 단일 축과 구별).
- **접근성 수정(전문가 지적 반영)**: 원본의 `role="img"`+단일 `aria-label`은 내부 카드/지표 텍스트 12블록을 스크린리더에서 prune하므로 **제거**. 텍스트는 일반 DOM 노출, 순수 장식(`wf-codewin`·`wf-dash`·`wf-pipes`·`wf-bottom`·`wf-icon`·`wf-aistack`)에만 `aria-hidden`. raster PNG 제외(SVG-first·자기완결).
- `assets/visual-html.css`에 `.wf-*` 추가(스킬 토큰화, 코어 해시 비대상). 모바일 계약: `@820px` wf-map 1컬럼, `@520px` 지표 1컬럼·장식 connector 숨김.
- 매핑: expert/education/skill_audit/landing_brief의 **후순위**(1순위 불변 → 골든 v6 회귀-0 보존). SKILL §0.6/§4.7·AGENTS §3/§8.2·`references/visual-html-system.md`(카탈로그 21·접근성 규칙) 반영.
- 게이트: `soft_workflow_gate`(opt-in `wf-board`) — role=img 금지·장식 aria-hidden·raster 금지·모바일 접힘·CSS 인라인. 렌더 1280/390px overflow 0, 무 JS 0 확인.

### Soft Shape 도형 36종 편입 (8817, 전문가 검토 반영, 2026-06-01)
"본문 설명 시작부 보조 도형" 36종을 신규 무거운 라이브러리 대신 **visual-template-system(8000×6000 SVG)의 soft-shape 카탈로그**로 흡수(전문가 합의: 캔버스·`figure.visual-figure` 매체 동일 → 중복 최소화).
- `assets/shape-svgs/*.svg` 36종(8000×6000 warm SVG, `<title>/<desc>` 접근성, 무 JS) + `assets/shape-catalog.json`(id/label/usage).
- `assets/shape-visuals.css`(`.shape-figure`/`.shape-lead`/`.shape-grid`, 프로파일 무관 조건부) + `base.html` `{{SHAPE_VISUALS_CSS}}` 슬롯(editorial 뒤). 코어 해시 비대상.
- 삽입 표준: `<figure class="shape-figure"><img class="shape-img" …8000×6000 alt="…"></figure>`(visual-figure 아님 — 앵커라 figcaption 선택). `alt`는 `shape_visual_gate`가, svg 존재는 `broken_local_ref`가 검사. 도형은 시각 앵커, 핵심 정보는 HTML 텍스트.
- 경계: 글자 옆 장식=`bi-`(40×40), 본문 구조도=`vt-`(HTML), 시작부 프리뷰=soft-shape(8000×6000 img) — 상호 비대체.
- `references/visual-template-system.md`(카탈로그 36·삽입 패턴·모드별 추천)·SKILL §4.5/자산맵·AGENTS §8.1·`manifest.json` `shape_visuals` 메타 반영.
- 게이트: `shape_visual_gate`(opt-in `shape-figure/img/lead/grid`) — CSS 인라인·빈 alt 금지·네임스페이스 누수. 두 편입 모두 신규 게이트 opt-in이라 3 프로파일 골든 `OK` 바이트 불변(회귀 0). 버전은 4.5.0 유지(frozen 골든 v6의 sources 버전 보존 — bump 시 `source_version_mismatch`).

### Soft Workflow 도판 10종 편입 (8819, 전문가 검토 반영, 2026-06-01)
8817·8816의 후속 — soft 스타일 8000×6000 SVG 워크플로우 도판 10종을 visual-template-system에 흡수(아키텍처/IA + QA/접근성 2인 검토). soft-shape(작은 앵커)와 달리 "본문 대표 도판/섹션 상단 구조도/랜딩 카드"용 **와이드**.
- `assets/workflow-svgs/01..10.svg` — Linear Pipeline·Radial Agent Hub·Decision Router·Layered Stack·Quality Funnel·Knowledge Graph·Agent Swarm·Timeline Delivery·Comparison Board·Governance Operating Model. 8000×6000, `<title>/<desc>` 접근성, 무 JS, warm cream. + `assets/workflow-catalog.json`(id/label/usage 정규화).
- `assets/workflow-visuals.css` — `.workflow-figure`(와이드 ~720px, `object-fit:contain`, 모바일 고정 height 금지)·`.workflow-grid`(2열→1열). `{{WORKFLOW_VISUALS_CSS}}` 슬롯(shape 뒤), 프로파일 무관·코어 해시 비대상.
- **네임스페이스 `workflow-` 신설**(전문가 지적: `wf-`는 vt-21 `soft_workflow_gate`가 점유 → 금지, `shape-` 재사용은 420px라 도판 뭉갬 → 별도). cross_leak(`vt-[a-z]`/`wg-\d2`) 충돌 0.
- 삽입: `figure.workflow-figure`(visual-figure 아님 → figcaption 권장·강제 아님) + `img.workflow-img`(alt 필수). **경계**: bi-(40×40) < shape-(420px 앵커) < workflow-(720px 대표 도판) < vt-(검색가능 HTML). workflow 도판은 placeholder 노드라 vt- 대체 금지(독자가 본문에서 읽어야 할 절차/비교는 vt-).
- 게이트 `workflow_visual_gate`(opt-in `workflow-figure/img/grid`) — CSS 인라인·빈 alt 금지·네임스페이스 누수·**로컬 SVG 8000×6000 해상도 계약**. 또 QA 지적대로 **`<style>` 제거 후 body만 스캔**해 CSS 주석 속 예시 `<img>` 오발동을 구조적 차단(기존 `shape_visual_gate`도 동일 백포트).
- 검증: 3 프로파일 골든(widget/auto/diagram) `OK` 바이트 불변, workflow 픽스처 4/4 + CSS주석 오발동 회귀 통과, 실제 도판 페이지 렌더 1280/390px overflow 0·무 JS 0. version 4.5.0 유지.

### 본문 구조 패턴 7종 편입 (2026-06-01)
첨부 HTML의 좋은 구조만 추려 기존 13모드 안에서 선택 삽입하는 **작은 본문 구조 패턴 라이브러리**로 편입했고, 이후 `md-excerpt`를 추가해 현재 7종으로 확장했다(새 모드 미추가). 외부/동작 JS 0, 스킬 토큰 + body icon 활용, 프로파일 무관.
- `assets/editorial-patterns.css` — 7 패턴 CSS: `chron-list`(증류 연대기)·`source-preserve`(원문 보존 details)·`core-insight`(핵심 명제 callout)·`conn-grid`(연결 분석 카드)·`ba`(Before/After 윤문)·`impact-grid`(콘텐츠 전환)·`md-excerpt`(마크다운/코드 발췌). 기존 클래스와 충돌 0.
- `assets/editorial-pattern-templates/01..07.html` — 콘텐츠만 교체하는 삽입 골격 7종.
- `references/editorial-pattern-system.md` — 7종 카탈로그·모드별 추천(예: chronology→expert/case_study, source-preserve→reference/article, core-insight는 페이지당 1개, md-excerpt→skill_audit/reference)·과삽입 금지·삽입 규칙.
- `assets/base.html`: `{{EDITORIAL_PATTERNS_CSS}}` 슬롯(body-icons 뒤). `manifest.json`: assets + `editorial_patterns` 메타(count 7).
- `scripts/validate_output.py`: editorial-pattern 게이트(패턴 사용 시 editorial-patterns.css 인라인 강제).

### 비주얼 프로파일 선택 (2026-06-01)
스킬 기동 시 비주얼 스타일을 고를 수 있게 단일 스킬 + 프로파일 파라미터를 도입했다. 코어(13모드 라우터·레이아웃·코어 CSS 5종)는 100% 공유하고, 프로파일이 라이브러리·삽입 단계·CSS 번들·결정표 컬럼만 게이트한다. 무 JS 0·코어 해시 계약 불변. (버전은 4.5.0 유지 — 4.6.0 bump은 frozen auto 골든 v6의 footer/sources를 건드려 회귀-0을 깨므로 골든 보존을 위해 보류; 버전 일관성은 manifest=sources=footer=4.5.0으로 충족.)
- **프로파일 3종**: `widget`(=v5, CSS 뷰 위젯 `wg-`, 코어5+`widgets.css`) / `diagram`(=v6, SVG→HTML `vt-`, 코어5+`visual-html.css`) / `auto`(기본, 둘 다 = 현행 v6 산출).
- **선택 규칙**: 인자 `profile=widget|diagram|auto` 또는 별칭 `style=v5|v6`(`trim→lowercase→정규화`, 둘 다 오면 `profile=` 우선, 무효=`invalid_profile` 실패·조용한 폴백 금지). 미지정 시 비대화형(AGENTS.md 경유 Codex/Gemini)=무조건 `auto`·질문 금지, 대화형(Claude)=1회 질문. 결정론은 인자 명시 경로 한정.
- `manifest.json`: `profiles` 스키마(이름·별칭·css·templates·markup·steps) + `profile_selection` 설명 추가.
- `AGENTS.md`: §4 "0. 프로파일 결정(모드 선행)"·"0.5 profile.json 기록"·§3 프로파일별 컬럼 주석·§4 프로파일별 CSS 번들표·삽입 단계 6/7 게이팅·불변식6 "5종 해시+조건부 인라인".
- `SKILL.md`: §0.5 비주얼 프로파일 선행·§0.6 프로파일 오버레이(단일 출처)·Step 4.6/4.7 프로파일 게이트.
- `scripts/validate_output.py`: `validate(root, skill_dir, profile=None)`·`--profile`·`_resolve_profile`(우선순위 인자>profile.json>폴백, 별칭·invalid)·always-on `cross_leak_gate`(diagram `wg-\d{2}`/widget `vt-[a-z]`, 단·이중따옴표·대소문자, `cross_leak` ISSUE)·`unfilled_placeholder` 게이트. **기존 3인자 호출 회귀 0**(baseline 동일).
- `references/visual-html-system.md`: "코어 6종"→"코어 5종 해시 + 조건부 인라인" 동기화.
- 골든: `auto`=showcase-v6(무변경)·`diagram`=v6 슬림(widgets.css 제거)·`widget`=showcase-v5(정합화). 각 `sources/profile.json` 동봉.
- 분리 계획·검증: 루트 `implement_visual_profile_separation.md`(Phase -1~6, 전문가·QA 리뷰 반영), `dev-plan/golden_prediagnosis.md`.

## v4.4.0 (2026-05-31) — 뷰 위젯 시스템 편입

코드/디자인/리뷰/운영형 정보를 위한 뷰 위젯(view widget) 20종을 스킬 본체에 정식 편입했다. 모든 위젯은 스킬 디자인 토큰을 재사용하고 외부 JS 없이 동작하며, 레이아웃 골격 위에 섹션 목적에 맞게 선택·삽입한다.

### 추가
- `assets/widgets.css` — 위젯 20종 스타일. 모든 선택자는 `wg-<id>-` 네임스페이스(`wg-01`~`wg-20`)로 격리되어 기존 theme/components/layouts와 충돌하지 않는다.
- `assets/widget-templates/*.html` 20종 — 위젯별 삽입 골격. 헤더 주석에 인터랙티브 분류(`css-only`/`css-partial`/`js-needed`)와 무 JS 근사 범위를 명시.
- `references/widget-system.md` — 위젯 선택 기준, 모드별 권장 매핑, 무 JS 인터랙션(`<details>`/`:checked`/`:target`/CSS 애니메이션) 규칙, 접근성(색 외 단서·포커스) 가이드.
- `tests/widget-checklist.md` — 위젯 게이트(외부 JS 0, `wg-<id>-` 네임스페이스 충돌 0, 인터랙션 기법 한정, 색 외 단서·포커스, 18·20 무 JS 근사) grep 명령+기대값.

### 위젯 20종 (인터랙티브 분류)
- CSS-only(완전 무JS) 11종: 02 Visual Design Directions, 06 Component Variants, 07 Animation Sandbox, 08 Clickable Flow, 10 SVG Figure Sheet, 11 Weekly Status, 13 Annotated Flowchart, 14 Feature Explainer, 15 Concept Explainer, 16 Implementation Plan, 17 PR Writeup.
- CSS 부분 7종: 01 Three Code Approaches, 03 Annotated PR, 04 Module Map, 05 Living Design System, 09 Arrow-Key Slide Deck, 12 Incident Timeline, 19 Feature Flag Editor.
- JS 필요 2종: 18 Ticket Triage Board(칸반), 20 Prompt Tuner. 완전 인터랙션(드래그·실시간 토큰)에만 JS가 필요하며, 스킬 기본값은 정적/`:checked` 상태의 **무 JS 근사**로 삽입하고 실시간 동작은 선택적 점진 향상으로만 둔다.

### 변경
- `SKILL.md`: 워크플로우에 Step 4.6 View Widget Selection & Insertion 추가(레이아웃 골격에 적합 위젯을 widgets.css 기반·무 JS로 삽입). §4 Design System 자산 맵과 §8 References에 widgets.css / widget-templates / widget-system.md 등재, 모드별 권장 위젯 한 줄 가이드 추가.
- `assets/base.html`: `{{WIDGETS_CSS}}` 슬롯을 통해 위젯 CSS를 합본하도록 적용(theme → components → visual-components → widgets → layouts → print 순서).
- `manifest.json`: 버전 4.4.0, assets에 `assets/widgets.css` 추가, changes에 위젯 시스템 편입 항목, updated 2026-05-31.

### 검증
- `assets/widgets.css`에서 `wg-01`~`wg-20` 네임스페이스 20종 확인, 네임스페이스 밖으로 새는 `.wg-` 선택자 0건.
- `assets/widget-templates/*.html` 20종 모두 외부/동작 `<script>` 0건. 18·20도 `<script>` 0건(무 JS 근사).
- 인터랙티브 분류 집계 11/7/2 일치(`css-only` 11, `css-partial` 7, `js-needed` 2).
- `manifest.json` `python json.load` 유효성 통과.

### 편입 완성도 마감 (전문가 리뷰 반영, 2026-05-31)
편입 준비도 리뷰(평균 84/100, 최저 항목 "편입 완성도" 72)에서 지적된 P0/P1을 반영해 "강제·메타데이터·문서 정합"의 2차 표면 편입을 마감했다. 무 JS 원칙(외부/동작 JS 0)은 전 항목에서 유지된다.
- `scripts/validate_output.py`: 위젯 정적 게이트 편입 — 출력에 `wg-` 클래스가 있으면 (a) widgets.css 인라인, (b) `wg-<id>-` 밖 `.wg-` 누수 0, (c) 위젯 영역 비-JSON-LD `<script>` 0, (d) `draggable`/`contenteditable` 0을 정적 실패로 검사.
- `manifest.json`: `visual_templates`와 대칭으로 `widget_templates` 배열(01~20) 등록.
- `tests/widget-checklist.md`: 회귀 규칙 2건 추가 — `role="tab"` 사용 시 `aria-selected` 필수/라벨 `tabindex·role` 금지(이중 탭 스톱 금지), `:target-within` 단독 의존 금지(`:target` 폴백 필수).
- `references/widget-system.md`: forward/reverse 매핑 불일치 2건 정합(landing_brief_html↔05, education_html↔10), 배정 원칙("콘텐츠 적합성 우선") 및 적용 갤러리 발견 링크 명시.
- `references/editorial-design-system.md`: 하이라이트 역할-색 1:1 규칙 명문화 — 본문 핵심 강조는 노랑 `.hl` 단일, `.hl.blue`/`.hl.pink`는 별도 의미 한정.
- `assets/widgets.css`: 위젯 08 `:target-within`에 `:has(:target)`/`:target ~` 폴백 추가(Chrome/FF 보강, 실측 동작 확인), `.wg-08-screen{outline:none}` 정리 후 `:focus-visible` 링 복원, wg-03/05/08/17에 `var(--focus)` 3px 포커스 링 일관 적용.
- `assets/widget-templates/14·15`: 커스텀 탭/스텝 라벨의 `role="tab"·tabindex="0"`과 `role="tablist"/tabpanel` 제거 → 네이티브 라디오 시맨틱 위임(이중 탭 스톱·미완성 ARIA 해소). 탭 전환은 `#id:checked`+`for=` 기제로 그대로 동작.
- `recipes/*.md` 5종(comparison·audit·reference·case-study·checklist): 모드 1순위 위젯 삽입 지시 추가.
- `README.md`: v4.4.0 갱신, 위젯 4종 자산 등재, tests "6종" 정정.
- 검증: 무 JS 0(스킬 assets·v5 전 페이지 전수), validate 위젯 게이트 통과, Chromium 실측 — 04 탭·09 스텝·12 플로우 전환 정상, 13 `.hl` 단일색(#ffe9a3), 포커스 링 3px.

## v4.3.3 (2026-05-30) — responsive polish regression gate

13개 모드 전수 캡쳐 감사에서 확인된 dark CTA 링크 대비, platform section/grid 구조, 모바일 표 밀도, case timeline 단일 대형 카드 문제를 스킬 CSS와 정적 게이트에 반영했다.

### 변경
- `assets/theme.css`: `--link-on-dark` 토큰 추가. h2 번호 badge는 숫자와 짧은 라벨 모두 안전하게 보이도록 `min-width + auto width` pill로 조정.
- `assets/components.css`: `.try a`, `.try.soft-cta a`를 밝은 링크 색으로 재정의해 검정 CTA 내부 링크 대비를 4.5:1 이상으로 회복.
- `assets/components.css`: `.mobile-card-table` 패턴 추가. 390px 모바일에서 복잡한 표를 행 카드 형태로 표시할 수 있도록 `data-label` 기반 카드 테이블 스타일 제공.
- `assets/layouts.css`: `.layout-platform .platform-grid:not(section)`로 제한해 semantic section wrapper에 grid가 직접 걸리는 회귀를 방지.
- `assets/layouts.css`: expert executive summary 4카드 orphan 배치를 2×2로 안정화. case-study timeline은 단일 대형 카드 대신 개별 step card로 보이도록 조정.
- `scripts/validate_output.py`: `section.platform-grid`, caption 없는 table, dark CTA link reset 누락, platform-grid direct selector를 정적 실패로 추가.
- `adaptive-html-final-showcase` 데모의 `_work/create_v3_from_v2.py`: v3 데모에 platform wrapper 분리, audit roadmap section 분리, landing table caption, mobile card table labels를 자동 적용.

### 검증
- 대상 페이지: 02 executive summary, 05 dark CTA, 07 platform cards, 08 audit roadmap/table, 10 comparison table, 11 case timeline, 12 landing table, 13 checklist table.
- 390px/1440px Playwright 재캡쳐 및 `validate_output.py --skill-dir` 검증 대상으로 지정.

## v4.3.2 (2026-05-30) — blog/SEO polish regression gate

05 블로그 CTA와 06 SEO SERP Preview 캡쳐 검수에서 확인된 dark-section 태그 대비, 블로그 섹션 번호 누락, SERP 제목 스타일 불균형, `h2-sub` 닫는 태그 오류를 스킬 CSS·생성기·정적 게이트에 반영했다.

### 변경
- `assets/components.css`: 검정 `.try`/`.try.soft-cta` 내부 `.tag` pill을 거의 흰 배경 + `var(--ink)` 굵은 텍스트로 재정의해 `로컬LLM`, `Ollama` 같은 태그가 흐려지지 않도록 수정.
- `assets/layouts.css`: `blog_writer` 본문 섹션 h2에 CSS counter 기반 번호 badge를 자동 부여해 다른 모드와 시각적 일관성을 맞춤.
- `assets/layouts.css`: `layout-seo .serp-title`을 Google 원문 모사형 파란색/Arial/20px에서 editorial UI에 맞는 `var(--ink)`, sans, 17~18px, 800 weight로 조정.
- `assets/layouts.css`: `.try.soft-cta .label`이 일반 문단 색을 상속하지 않도록 accent 색상 복구.
- `scripts/validate_output.py`: `.h2-sub`가 `</h2>`로 닫히는 HTML 오류, dark `.try` 태그 대비 reset 누락, blog counter 누락, SEO SERP title의 literal Google style 회귀를 실패 처리.
- `adaptive-html-final-showcase` 데모의 `_work/create_v3_from_v2.py`: legacy HTML의 `<p class="h2-sub">...</h2>` 패턴을 재생성 중 자동 교정.

### 검증
- 대상 페이지: 05 블로그 `가볍게 시작해보기`, 05 `왜 지금 로컬 AI인가`, 06 `SERP Preview`.
- 390px/1440px Playwright 재캡쳐 및 `validate_output.py --skill-dir` 검증 대상으로 지정.

## v4.3.1 (2026-05-30) — design polish regression gate

사용자 캡쳐 검수에서 확인된 카드 상단 여백, dark-section 내부 흰 카드 대비, audit 강점/리스크 grid 오배치, case timeline 이중 왼쪽선 문제를 스킬 CSS와 정적 게이트에 반영했다.

### 변경
- `assets/theme.css`: `section > h2:first-child`와 주요 카드 컴포넌트 첫 h2/h3의 top margin을 0으로 리셋해 카드 내부 상단 공백을 제거.
- `assets/theme.css`: muted text token을 더 진하게 조정해 h2-sub/caption/meta가 흐려 보이는 문제를 완화.
- `assets/components.css`: `.try` 안의 `.box/.summary-card/.cta-box/.card-block/.mini-card` 내부 텍스트 색상을 밝은 카드 기준으로 재설정해 흰 카드에서 텍스트가 흐려지는 문제 방지.
- `assets/components.css`: `.try .cta-box`의 accent left rule을 복구해 CTA 카드의 시각적 의도를 유지.
- `assets/components.css`: `.timeline-card` 왼쪽 padding을 보강해 ordered-list marker가 카드 모서리에 붙지 않도록 수정.
- `assets/components.css`: 표 내부 `.status-pill`을 nowrap/center 정렬로 고정해 `Unacceptable`, `GPAI (별도 트랙)`이 좁은 원형 배지처럼 세로로 깨지는 문제 방지.
- `assets/layouts.css`: `.winners:not(section)`, `.tradeoffs:not(section)`의 자동 2컬럼 grid를 제거하고 card block으로 변경. `layout-case .timeline` section left rule 제거.
- `SKILL.md`, `references/quality-gates.md`, `references/layout-system.md`: first-heading margin, dark card contrast, winners/tradeoffs grid, timeline left-rule 중복, CSS asset integrity 방지 규칙 추가.
- `scripts/validate_output.py`: 위 회귀 패턴과 CSS asset hash/snapshot 검사를 정적 게이트에 추가.

### 검증
- 대상 페이지: 04 교육 실습 카드, 06 SEO Final SEO Set, 08 skill audit 강점/리스크, 11 case timeline, 12 landing 다음 행동.
- Playwright 캡쳐 재검증 대상으로 지정.

## v4.3.0 (2026-05-30) — layout-safe v3 및 자동 검증 게이트

`adaptive-html-final-showcase-v2` 전수 캡쳐 감사에서 확인된 섹션 wrapper/grid class 충돌, 모바일 overflow, caption 음수 margin, source sync 불일치, gallery 예외 미정의를 스킬 본체에 반영했다.

### 변경
- `assets/layouts.css`: `section.matrix`, `section.serp-preview`, `section.value-grid`, `section.check-grid`, `section.priority-roadmap`, `section.winners`, `section.tradeoffs` 등 semantic section wrapper에 `display:grid`가 직접 적용되지 않도록 수정. 실제 그리드는 내부 `.card-grid`, `.grid-2`, `.grid-3`, `.matrix:not(section)` 등으로 분리.
- `assets/layouts.css`: `layout-education`의 미정의 `var(--good)`를 `var(--good-bg)`로 교정.
- `assets/components.css`/`assets/theme.css`: 긴 URL·코드·영문 토큰 overflow를 줄이기 위해 `overflow-wrap` 안전 규칙 추가, `.caption` 음수 margin 금지.
- `SKILL.md`, `references/quality-gates.md`, `tests/layout-checklist.md`, `tests/visual-regression-checklist.md`: section wrapper와 inner grid 분리 규칙 및 390px/1280px 검증 기준 추가.
- `scripts/validate_output.py`: 생성된 output 디렉터리를 정적으로 검사하는 게이트 추가(h1, `#main`, 로컬 참조, 외부 JS, caption 음수 margin, semantic grid selector, visual figure, source manifest sync).

### 검증
- `validate_output.py`로 v2의 기존 결함(caption negative margin, semantic section grid selector, source version mismatch)을 재현.
- v3 쇼케이스는 공통 CSS를 재주입하고 source를 v4.3.0과 동기화하도록 생성.
- Playwright 390px/1440px 렌더 검증 대상으로 지정.

## v4.2.1 (2026-05-30) — quality-gate SVG 레이아웃 보정

사용자 검수에서 `품질 게이트` 인포그래픽의 하단 “삽입 전 필수 검수” 카드가 납작한 배너처럼 보이고 footer와 시각적으로 붙는 문제가 확인되어 수정했다.

### 변경
- `scripts/render_visual_svg.py`의 `quality-gate` 렌더링을 세로 6행 구조에서 2×3 카드 그리드 + 충분한 높이의 노란 `PRE-FLIGHT` 패널로 변경.
- `references/visual-template-system.md`, `references/quality-gates.md`, `tests/visual-regression-checklist.md`에 하단 강조 패널 안전 규칙 추가.
- 강조 노란색(`#FFD400`)은 최종 검수/핵심 CTA 등 한 지점에만 쓰도록 정리.

### 검증
- quality-gate 샘플 SVG 렌더링 성공, 원본 8000×6000 유지.
- 주요 카드 max bottom 5060px로 footer(5600px)와 충분한 여백 확보.
- 로컬 데모 페이지 390px/1280px Playwright 스크린샷 재검증.

## v4.2.0 (2026-05-30) — Visual Template System 도입

14-image-strategy-demo.html에서 검증한 8000×6000 SVG 인포그래픽 전략을 스킬 본체에 반영했다. 이제 스킬은 모드/섹션 목적에 따라 사진 검색, SVG 인포그래픽 생성, AI 컨셉 이미지 사용을 구분하고, 기본값으로 목적형 SVG 인포그래픽을 우선한다.

### 추가
- `assets/visual-components.css` — `figure.visual-figure`, `.figure-wide`, figcaption, visual rule grid, visual pipeline 반응형 스타일.
- `visual-templates/*.svg.tpl` 7종 — hero-map, card-grid, decision-tree, quality-gate, timeline, matrix, checklist-flow.
- `scripts/render_visual_svg.py` — visual brief JSON을 8000×6000 SVG로 렌더링하는 stdlib-only 스크립트.
- `schemas/visual-brief.schema.json` — 시각 템플릿 입력 스키마.
- `references/visual-template-system.md` — 모드별 기본 템플릿, 이미지 선택 원칙, HTML 삽입 패턴, 품질 게이트.

### 변경
- `SKILL.md` 워크플로우에 Step 4.5 Visual Brief Planning 추가.
- `base.html`에 선택적 `{{VISUAL_COMPONENTS_CSS}}` 슬롯 추가.
- `manifest.json` 버전 4.2.0, assets/templates/scripts/schemas 메타데이터 갱신.
- quality/layout/visual/accessibility 체크리스트에 8000×6000 SVG, alt, figcaption, 캔버스 잘림 방지 게이트 추가.

### 검증
- visual brief 샘플 7종 렌더링 성공.
- 생성 SVG 7개 모두 XML 파싱 성공, width/height 8000×6000 확인.
- Python 스크립트 py_compile 통과.

## v4.1.0 (2026-05-30) — 정밀 분석 보고서 P0~P2 자동 패치

ANALYSIS_adaptive-html-final.md(7-전문가 분석 + 적대적 검증)에서 확정된 이슈 19건(medium 8 · low 11)을 8개 파일-분리 클러스터로 자동 패치 → 검증 → 재검증했다. 동작 결함은 원래 0건이었고, 본 패치는 메타데이터 정합성·테스트 커버리지·디자인 토큰 완성도를 끌어올렸다.

검증: 독립 스크립트 검증 15개 그룹 전부 통과 (id=main 13/13, 단일 h1 13/13, 외부 JS 0, 미정의 CSS 클래스 0, manifest 13모드 매핑 일치, recipes 13/13, schema 유효, 폭 토큰 780/1020 통일, .skill 라운드트립 완전 일치).

### P0 — 출시 신뢰성
- **M1** 접근성 회귀 가드 신설 — `tests/accessibility-checklist.md`: skip link, `<main id="main">` 13/13, 단일 h1, 외부 JS 0, `:focus-visible`를 grep 명령+기대값으로 자동검증.
- **M3** 모드 ID 규약 단일화 — `manifest.modes`를 라우터 표준 13개 ID의 `{id, layout}` 객체 배열로 교체. `references/layout-system.md`의 단축 명칭도 표준 ID로 교정(mode-selection.md는 이미 일치).
- **M5** `tests/quality-checklist.md` 재작성 — SKILL.md §7 게이트 1:1 매핑 + 모드별 조건부 게이트(교육→퀴즈/정답, 전문가→리스크/검증, 블로그·SEO→제목/메타/태그, 감사→개선본). 누락 게이트 9건 보강.

### P1 — 정합성·커버리지
- **M2** 레이아웃이 쓰던 미정의 CSS 클래스 39개를 `layouts.css`에 전부 정의(헤더 공통 11 + 그리드성 7은 모바일 1컬럼 + 섹션 래퍼 20+). 차집합 0.
- **M4** 누락 7개 모드 recipe 신규 생성 → `recipes/` 총 13/13 (article, education, reference, comparison, case-study, landing-brief, checklist).
- **M6** `tests/layout-checklist.md`를 13레이아웃 표(파일|mode|필수블록|폭클래스)로 재작성. 폭 토큰 780/1020 통일.
- **M7/M8** `theme.css`에 `:focus-visible` 추가, `tests/visual-regression-checklist.md` 폭 임계치 780/1020 교정 + 주관 항목 정량화.
- **golden-prompts** P9~P13(reference/comparison/case_study/landing/checklist) 추가 + 전 항목 `expected_mode`/`expected_layout` 명시 → 13모드 대표.

### P2 — 문서·디자인 완성도
- **L1** `editorial-design-system.md` 구버전 명칭(v2/7모드) → final/13모드.
- **L2** `examples/index.html` v2 브랜딩 → v4.1.0 / 13-mode.
- **L3** `design-dna.md`를 디자인 토큰 SoT로 명시 + SKILL.md §8 References 등재.
- **L4** SKILL.md §5 Required Components에 `.faq/.cta-box/.box` + 골격 컴포넌트 추가, `components.css`에 해당 클래스 정의.
- **L5** `base.html`에 선택적 `{{FOOTER}}` 슬롯 추가(footer CSS 고아 해소).
- **L6** 출처 허브 경로를 일반화 표기로(비존재 절대경로 강제 제거).
- **L7** `blog-meta.schema.json`을 예시 11필드와 1:1 정합(title_variants 4키, search_intent enum, slug/target_reader/estimated_reading_time/platform_notes) + `$schema`/`$id`/`title`.
- **L8** `quality-report.schema.json`을 루브릭 구조(0~5 점수 + total + verdict + gates)로 확장 + 메타 식별자. eval-rubric/quality-gates/Blog Score 적용범위 명시.
- **L9** 콜아웃 raw hex → `:root` 토큰 12종, AA 미달 색(.term/.danger/.good 라벨, .meta, .tag) 4.5:1 이상으로 상향, `prefers-reduced-motion` scroll 해제, print.css `print-color-adjust`/`break-inside`/`.skip{display:none}`.
- **L10** h2-sub 강도를 '모드 한정 권장'으로 SKILL/quality-gates/editorial-design-system 통일, 트리거 tie-breaker 한 줄 추가.
- **L11** 공개/SEO 예시 03/05/06에 폰트 링크(Pretendard + Pretendard) 추가.

### 메타
- version 4.0.0 → 4.1.0. 파일 수 51 → 59 (+accessibility-checklist, +recipe 7).
- 패치 전 백업: `/tmp/adaptive-html-final.pre-patch`, `/tmp/adaptive-html-final.skill.bak`.

## v4.0.0 (2026-05-30) — 통합 최초본
- `adaptive-html-learning-ultimate`(13모드 라우터·레이아웃·평가체계) + `adaptive-html-blog-writer`(블로그/SEO/플랫폼/박스 상세 규칙) 병합.
- skip link 접근성 버그 수정: 13개 레이아웃 `<main id="main">` 통일.
- 이름·메타데이터 일원화(aliases/merged_from).
