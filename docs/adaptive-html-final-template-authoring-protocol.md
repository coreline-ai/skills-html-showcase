# adaptive-html-final — 공식 템플릿 기반 작성 프로토콜

> 도입: v5.10.4 ([release-approval](../dev-plan/release-approval-v5.10.4.md)). 목적: "validate/quality/completion은 통과하는데 사용자 눈검수에서 어긋나는" 문제를 끊는다. **LLM은 HTML을 작성한다. 단, 공식 layout/vt/wg/body-icon/editorial 템플릿 파일을 실제로 읽고 그 구조를 유지해 작성해야 한다.** 검증기는 보조 수단이며, 브라우저 캡쳐와 수동 구조 검토까지 통과해야 완료다.

## 0. 핵심 원칙

- 검증 OK는 **필요조건**이지 완료가 아니다. "검증 통과"와 "결과물 품질 통과"를 분리해서 보고한다.
- **비정본 클래스 발명 금지.** 실산출물 결함(M2·M3·M6·M9)의 실제 원인은 `template-card-head`·`source-preserve-static` 같은 **스킬에 없는 클래스를 즉석에서 만든 것**이었다. 스킬 정본 컴포넌트는 이미 간격·색을 해결해 둔다.
- output 산출물은 **독립 테스트 결과물**이며, 스킬 입력/정본이 아니다.

## 1. 모드 시작 전 반드시 읽을 파일 (build-evidence 대상)

1. `AGENTS.md` (라우팅 결정표)
2. `skills/adaptive-html-final/SKILL.md`
3. 해당 `skills/adaptive-html-final/modes/NN-<mode>.json` (실행 정본)
4. 해당 `assets/layouts/<layout>.html`
5. 1순위 `assets/visual-html-templates/NN-*.html`
6. 사용할 `assets/widget-templates/NN-*.html`
7. `assets/body-icons.json` (catalog id만 사용)
8. 필요 시 `template-catalog/*.html`

판정 기준: 생성물 `sources/build-evidence.json`에 위 파일의 **경로 + sha256 + 섹션 매핑 + 사용 이유**를 남긴다. 기록이 없으면 "공식 템플릿 사용"으로 인정하지 않는다(동일 문제 Z1).

## 2. Mode Build Sheet (작성 시작 전 필수)

| 항목 | 내용 |
|---|---|
| mode | 공식 모드 id |
| topic | 신규 독립 주제(이전 모드 주제·문체 재사용 금지) |
| layout file read | 실제 읽은 layout 파일 경로 |
| primary vt file read | 실제 읽은 1순위 vt 파일 경로 |
| wg file read | 실제 읽은 wg 파일 경로 |
| body icon ids | 사용할 catalog id 목록 |
| section plan | 10개 이상 섹션 제목과 역할 |
| template mapping | 어느 섹션에 어떤 공식 template을 넣는지 |
| visual risk | 폭·대비·간격·번호 pill·rail 색 리스크 |
| stop condition | 다음 단계 중단 조건 |

## 3. 마이크로 레이아웃 계약 — 실패 예시 → 올바른 처리 (M1~M10)

실산출물(2026-06-14 뉴스)에서 검증 통과 후에도 남은 결함. 코어/조건부 CSS로 닫은 것(M1·M4·M7·M10)과 작성 규칙으로 닫는 것(M2·M3·M5·M6·M9)을 구분한다.

| Code | 실패 예시 | 올바른 처리 |
|---|---|---|
| M1 | `<h2>`의 번호 pill이 390px에서 `16`→`1/6`처럼 2줄로 깨짐 | 스킬 정본 `.no/.num` 사용(v5.10.4부터 `white-space:nowrap` 내장). 별도 pill 클래스 발명 금지. |
| M2 | `근거 ★★★`처럼 label과 점수/별표/tag를 같은 inline에 붙임. 비정본 `template-card-head .tag` 발명. | 점수/별표/tag는 `.tag-list` 또는 별도 row로 분리(gap ≥8px). 카드 머리글은 정본 vt/editorial 컴포넌트의 `.vt-kicker`·chip 구조 사용. |
| M3 | 좌측 accent rail view 첫 텍스트가 rail에 붙음. 비정본 `source-preserve-static` 사용. | 정본 `.lede-note`(rail+24px padding 내장)·`.source-note` 사용. rail형 view 첫 텍스트는 rail 기준 ≥18px. |
| M4 | 카드 kicker→title→body 간격이 4px 이하로 답답 | 정본 `.cmp-card`(v5.10.4부터 kicker 하단 8px)·`.tl-item` 사용. 인접 텍스트 block 간격 ≥8~12px. |
| M5 | `<section><p>` 직접 문단이 view 없이 밋밋하게 노출 | 텍스트-only 정보도 `lede-note`·`source-note`·`core-insight`·`summary-card`·`impact-card`·`chron-card` 중 하나로 감싼다. `main article>section>p:not(.h2-sub)` 직접 노출 금지. |
| M6 | 날짜·원문 목록 mini-card가 surface만 있고 밋밋 | 목록 카드도 좌측 accent rail 또는 명확한 view treatment 적용. 정본 timeline/card-grid 패턴 사용. |
| M7 | 상단 fixed reading-progress가 섹션 라인처럼 보여 검수 방해 | 인쇄/export에서는 자동 숨김(v5.10.4 `print.css`). 검수용은 progress bar를 섹션 라인으로 오인하지 않게 확인. |
| M8 | output index 카드 rail이 전체 높이 fill로 카드마다 크기 달라 보임 | (output index/template shell 영역 — 스킬 자산 아님) rail은 고정 높이/inset, 색은 토큰 다색. |
| M9 | 반복 카드 rail이 전부 `var(--accent)` 한 색이라 단조 | 정본 `.tl-color-cycle`(4색 순환) 사용. 반복 rail은 `--vt-red/--vt-blue/--vt-green/--vt-gold` 중 3종 이상을 의미 있게 순환. `var(--accent)` 단일 반복 금지. |
| M10 | `{{FOOTER}}`가 `<main>` 밖에 렌더돼 `.source-note` footer가 viewport 좌측에 붙음 | 정본 `body>footer`(v5.10.4 본문폭 중앙정렬) 사용. footer를 임의 위치/폭으로 두지 않는다. |

## 3.6 시각 결함 하드닝 — 실패 예시 → 올바른 처리 (G1~G8, v5.10.6)

validate/quality/completion은 통과하지만 화면에 남던 누적 결함. 코어/조건부 CSS로 닫은 것(G3·G4·G5·G8)·작성 규칙(G1)·검출 게이트(G2·G6·G7)를 구분한다.

| Code | 실패 예시 | 올바른 처리 |
|---|---|---|
| G1 | 좁은 표 첫 열에서 상태코드 `<code>100</code>`가 `10`+`0`으로 줄바꿈 | 상태코드형 짧은 코드는 정본 `.status-pill` 사용(`table .status-pill{white-space:nowrap}` 내장). 긴 인라인 코드(공백 포함 다토큰)는 `.tbl`/`.table-scroll` overflow에 맡긴다. bare `<code>`에 broad nowrap 적용 금지(예제 09 regex 회귀). |
| G2 | `wg-04` 결정트리/다이어그램 SVG 노드 박스가 서로 겹침 | 노드 좌표 간 간격 확보. 신규 산출물은 `micro_layout_audit.mjs`로 `node_overlap_ok`(>4px×4px=fail) 검증. 정적으로 못 잡으므로 render-audit 차수 필수. |
| G3 | `.try` 안 흰 카드(.summary-card 등) 링크가 다크 전용 `--link-on-dark`(흰 배경 1.65:1) | inner-card 링크는 `--accent-2`(8테마 min 6.09:1). 정본 components.css가 이미 reset하므로 inline 색 지정 금지. `.try` **직속** 링크만 `--link-on-dark` 유지. |
| G4 | `source-preserve` 좌측 accent rail에 본문 텍스트가 붙음 | 본문을 `.source-body-inner`(좌측 미세 라인 + padding-left:24px 정본)로 감싼다. inline style 보정 금지. |
| G5 | `.mini-card` 첫 `.tag`(예: `Skeptic`)와 아래 제목/본문이 붙어 보임 | 정본 `.mini-card>.tag:first-child` 리듬(margin-bottom + 후속 h3/p reset) 사용. inline 간격 보정 금지. |
| G6 | 목차(`toc-map`)를 `executive-summary` 첫 콘텐츠 섹션 **안**에 넣음 | TOC는 `main` 직속 독립 `<section class="document-toc-section">`. `executive-summary`/첫 콘텐츠 섹션 내부 중첩 금지(per-page 게이트 강제). |
| G7 | 섹션 첫 요소가 빈 `<div id>`/`<a id>`이고 그 뒤가 `<h2>` → `section>h2:first-child` margin reset 풀림 | anchor는 빈 선행 요소가 아니라 `<h2 id="…">`에 직접 부여한다. |
| G8 | red gradient 의도 `.core-insight`에 간격 보정용 `core-insight--neutral`을 붙여 그라데이션 소실 / 내부 제목 상단 여백 과다 | `--neutral`을 spacing 보정 용도로 붙이지 않는다(red gradient 유지). 내부 제목 간격은 정본 `.core-insight>:first-child{margin-top:0}`가 처리. |

## 4. 금지 사항 (동일 문제 Z1~Z8 대응)

- `generate_fulltest_17.py`류 자체 `wg_markup()`/`section_inner()`로 17개를 찍어내는 임시 대량 생성기.
- 공식 template을 흉내 낸 유사 `wg-*`/`vt-*` class shell 직접 작성.
- 이전 모드 HTML을 다음 모드의 구조/문체/주제 예시로 열람.
- 2개 이상 모드 동시 생성. 한 모드 완료(검증+브라우저) 전 다음 모드 시작.
- 검증 실패를 임시 CSS/마커로 우회. 사용자가 지적한 문제를 "검증 통과"로 덮기.

## 5. 완료 보고 양식

| No | Mode | Topic | File | Sections | Official layout | Official vt | Official wg | Validate | Quality | Completion | Browser | Manual QA |
|---:|---|---|---|---:|---|---|---|---|---|---|---|---|

- 검증 한계를 별도 섹션으로 적는다. 실패/수정 이력을 숨기지 않는다.
- `completion_check.py OK`와 "사용자 눈검수 통과"를 분리한다.

## 참조

- [SKILL.md](../skills/adaptive-html-final/SKILL.md)
- [references/visual-html-system.md](../skills/adaptive-html-final/references/visual-html-system.md) · [widget-system.md](../skills/adaptive-html-final/references/widget-system.md) · [editorial-pattern-system.md](../skills/adaptive-html-final/references/editorial-pattern-system.md)
- [dev-plan/implement_20260614_174756.md](../dev-plan/implement_20260614_174756.md) · [release-approval-v5.10.4.md](../dev-plan/release-approval-v5.10.4.md)
