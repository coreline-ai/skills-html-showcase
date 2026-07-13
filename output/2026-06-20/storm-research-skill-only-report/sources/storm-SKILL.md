---
name: storm-research
description: Stanford STORM 방법론(다관점 질문 + 출처 grounding)을 cmux 멀티 페인으로 구현한 딥리서치 오케스트레이터. 메인 Opus가 5개 영혼 페인(회의주의자·경제학자·역사학자·학자·미래학자)을 직접 만들어 claude/codex/kimi에 분산하고, 각 영혼이 출처 강제 딥리서치를 수행해 cmux send로 메인에 보고한다. 그 뒤 4프롬프트 파이프라인(다중관점 스캔→모순 지도→종합→동료 검토)을 돌려 dist/<프로젝트>/index.html 자체완결 리포트를 만든다. 트리거 — "STORM 리서치", "다관점 딥리서치", "5영혼으로 조사", "스톰 방법으로 조사해줘", "여러 LLM으로 병렬 리서치", "/storm-research".
---

# storm-research: STORM 다관점 딥리서치 오케스트레이터

> **메인 Opus는 오케스트레이터다.** 페인 5개를 직접 만들고(요구 7), 영혼들에게 임무를 분배하고,
> 보고를 수집하고, 종합·검토·HTML 산출을 한다. 리서치 노동은 5영혼(claude/codex/kimi)에 위임.
>
> 방법론 SSOT: [`references/storm-pipeline.md`](./references/storm-pipeline.md) ·
> 정직성/출처: [`references/provenance.md`](./references/provenance.md) ·
> cmux 통신: [`references/cmux-orchestration.md`](./references/cmux-orchestration.md) ·
> LLM 분배: [`references/soul-distribution.md`](./references/soul-distribution.md)
>
> 진짜 STORM을 쓰고 싶으면: https://storm.genie.stanford.edu (논문 https://arxiv.org/abs/2402.14207)

## 무엇을 만드는가

하나의 주제 → 5개 모델이 5개 관점으로 출처를 끌어온 딥리서치 → 모순까지 드러낸 종합 글 →
동료 검토 → `dist/<slug>/index.html` 한 장. **단일 LLM 한 번 묻기**가 아니라 "다섯 전문가에게
묻고, 충돌을 통과시킨" 리서치.

## 두 가지 실행 모드

| 모드 | 조건 | 동작 |
|---|---|---|
| **분산 모드 (full)** | cmux 워크스페이스 + claude/codex/kimi 설치 | 5영혼을 5페인에 분산 (이 스킬의 본령) |
| **인라인 폴백 (solo)** | cmux 밖이거나 CLI 부재 | 메인이 4프롬프트를 자기 안에서 순차 실행 (페인 없이) |

진입 시 `Phase 0`이 자동 판별. 분산 불가 시 사용자에게 알리고 solo 폴백 제안.

---

## Phase 0 — 환경 점검 + 주제 확보

```bash
SKILL=~/.claude/skills/storm-research            # 심링크 (로컬 원본을 가리킴)
echo "cmux workspace: ${CMUX_WORKSPACE_ID:-NONE}"
for c in claude codex kimi; do command -v $c >/dev/null && echo "[OK] $c" || echo "[MISSING] $c"; done
```

- `$CMUX_WORKSPACE_ID`가 없으면 → **solo 폴백**(아래 "인라인 폴백" 섹션)으로 안내.
- CLI가 일부만 있으면 → 가용한 것만으로 분배 재조정(예: kimi 없으면 claude 3 / codex 2).
- **주제 확보**: 사용자 주제가 모호하면 한 번만 되묻는다 (범위·기간·지역·관심 각도).
- `slug` 결정 (영문/숫자 kebab, 한글이면 음차 또는 사용자 확인).

> 게이트: 주제 한 줄 + 모드(full/solo)가 확정돼야 Phase 1 진입.

## Phase 1 — 관점 도출 + LLM 분배 확정

1. **관점 결정**: 기본 5영혼 팩 사용 — 회의주의자·경제학자·역사학자·학자·미래학자.
   - 주제가 특정 도메인이면 관점을 **재도출** 가능 (예: 양자컴퓨팅 → 물리학자/암호학자/VC/정책/회의주의자).
     재도출 시 [`references/soul-distribution.md`] 규칙 — **회의주의자는 항상 유지**, charter는 가장 가까운
     기존 영혼 파일을 베이스로 메인이 주제 맞춤 1~2줄만 덧댄다.
2. **LLM 분배** (기본): `Skeptic:claude, Economist:codex, Historian:kimi, Academic:claude, Futurist:codex`.
   가용성에 따라 조정. **모델 다양성 = 영혼 다양성** (같은 질문도 다른 모델은 다른 출처를 끌어옴).
3. **RUN_DIR 결정**: `RUN_DIR="$SKILL/dist/<slug>"` (한 run의 모든 상태가 여기 모임).

## Phase 2 — 메인이 5개 페인을 만든다 (요구 7)

```bash
source "$SKILL/scripts/lib.sh"
export RUN_DIR="$SKILL/dist/<slug>"; mkdir -p "$RUN_DIR"
MAIN_REF=$(storm_register_main "")     # 현재 페인을 "Main"으로 명명 + ref 등록

"$SKILL/scripts/spawn-souls.sh" --run-dir "$RUN_DIR" --main-ref "$MAIN_REF" \
  --mapping "Skeptic:claude,Economist:codex,Historian:kimi,Academic:claude,Futurist:codex"
```

- spawn-souls가 5개 새 페인을 만들고 각 CLI를 **권한 완전 허용 모드**로 기동
  (claude `--dangerously-skip-permissions` / codex `--dangerously-bypass-approvals-and-sandbox` / kimi `-y`).
- ref 매핑은 `$RUN_DIR/pane-refs.json`에 저장. 이후 모든 송수신이 이걸 참조.
- 안착(settle) 대기까지 spawn-souls가 처리.

> 게이트: `cmux tree`에 5개 영혼 페인 + Main이 보여야 진행. 안 보이면 `cmux-surface.sh refresh` 후 재확인.

## Phase 3 — 딥리서치 분배 (출처 강제, 병렬) (요구 5)

5영혼에게 **동시에** 임무를 분배한다. 각 dispatch는 charter + 주제 + 경로/ref를 합친 브리프를 만들어 보낸다.

```bash
TOPIC="<주제>"
for S in Skeptic Economist Historian Academic Futurist; do
  "$SKILL/scripts/dispatch-soul.sh" --run-dir "$RUN_DIR" --soul "$S" \
    --topic "$TOPIC" --main-ref "$MAIN_REF"
done
```

각 영혼은 브리프(`templates/soul-brief.md.tmpl` + `souls/soul-*.md`)대로:
1. **실제 웹 검색**으로 1차 출처 수집 (도구 없으면 BLOCKED 보고, 추측 금지).
2. 모든 주장에 `[출처: URL]`. 추측은 `[추론]` 라벨.
3. 결과를 `$RUN_DIR/results/<Soul>.md`에 기록.
4. `touch $RUN_DIR/done/<Soul>.done` + **메인에 `cmux send` push** (요구 4: 영혼이 스스로 메인에 보고).

> 양방향 통신: 영혼이 완료/차단/진행을 `cmux send --surface <MAIN_REF>`로 메인에 직접 push한다.
> 메인(이 세션)은 그 메시지를 실시간으로 받는다. 동시에 done 파일이 신뢰 1순위.

## Phase 4 — 수집 (push 수신 + done 폴링)

```bash
"$SKILL/scripts/collect-souls.sh" --run-dir "$RUN_DIR" \
  --souls "Skeptic,Economist,Historian,Academic,Futurist" --timeout 900
```

- 영혼의 push 메시지가 이 세션에 도착하면 그때그때 인지. collect-souls는 done 파일/마커로 최종 확정.
- **BLOCKED 영혼 처리**: 해당 페인 `cmux capture-pane`으로 사유 확인 → (검색 도구 문제면) 재지시,
  또는 사용자에게 보고하고 그 관점은 "출처 확보 실패"로 표기(가짜 출처로 채우지 않음).
- TIMEOUT 영혼: capture-pane로 진행 확인 후 연장/스킵 결정 (사용자 질의).

> 게이트: 최소 3/5 영혼이 출처 포함 results를 냈을 때 종합 진입 권장. 그 이하면 사용자에게 보고.

## Phase 5 — 4프롬프트 파이프라인 (메인 Opus가 직접)

Phase 3~4의 5영혼 딥리서치가 **프롬프트 1(Multi-Perspective Scan)의 분산 강화판**이다.
이제 메인이 나머지 3프롬프트를 aggregated 자료 위에서 실행한다:

1. **모순 지도** — `prompts/2-contradiction-map.md`. 5 results를 `{{SCAN_OUTPUT}}`로 넣어 합의/모순/사각/핵심긴장 도식화.
   (단독 스킬 `/storm-contradict` 와 동일 로직 — 메인이 인라인 수행.)
2. **종합** — `prompts/3-synthesis.md`. 스캔 + 모순 지도 → 개요 → 본문(인용 유지) → lead. 한 관점 수렴 금지.
3. **동료 검토** — `prompts/4-peer-review.md`. 종합본의 출처 편향 전이·부당한 연결·미인용·모순 봉합 점검.
   **회의주의자 영혼**의 결과를 검토 관점으로 활용 (저자≠검토자 분리). BLOCKER 있으면 종합으로 되돌림.

> 출처는 전 단계에서 절대 누락 금지. 각 산출을 메인이 변수로 보관 (다음 단계 입력 + report.json 조립).

## Phase 6 — HTML 리포트 산출 (요구 6)

5영혼 results + 모순 지도 + 종합 + 동료 검토를 `report.json`으로 조립해 빌드한다.

```bash
# report.json 스키마: templates/report.schema.json
node "$SKILL/scripts/build-report.mjs" "$RUN_DIR/report.json" "$SKILL/dist"
# -> $SKILL/dist/<slug>/index.html  (자체완결, 네트워크 무의존)
```

`report.json` 조립 시 (메인이 작성):
- `souls[]`: 각 `results/<Soul>.md` 내용 + name/persona/llm/summary.
- `contradiction_map` / `synthesis` / `peer_review`: Phase 5 산출.
- `confidence`: 동료 검토의 신뢰도 배지 (출처 다양성/인용/정직성/verdict).
- `all_sources` 생략 가능 — 빌더가 모든 텍스트에서 URL 자동 수집·중복 제거.

> dist 폴더 구조: `dist/<slug>/index.html` + `report.json` (요구 6: 프로젝트 폴더의 dist 안에 개별 프로젝트 폴더).

## Phase 7 — 검수 + 보고 + 정리

1. **HTML 검수**: 브라우저 페인 또는 `open`으로 열어 육안 확인. 미치환 `{{}}` 0, soul 카드 5, 출처 링크 존재.
2. **사용자 보고**: 핵심 긴장 1문장 + verdict + 산출 경로(`dist/<slug>/index.html`).
3. **페인 정리** (선택, 사용자 확인 후): `cmux close-surface --surface <ref>`로 영혼 페인 종료(주의: `close-pane`은 없는 명령), 또는 다음 주제 재사용 위해 유지.

---

## 인라인 폴백 (solo 모드 — cmux/CLI 없을 때)

분산 불가 환경이면 메인이 4프롬프트를 자기 안에서 순차 실행한다 (페인 없음):
1. `prompts/1-multi-perspective-scan.md` — 메인이 5관점을 한 세션에서 (가능하면 sub-agent 5개 병렬로) 리서치 + 출처.
2. → 2 모순 지도 → 3 종합 → 4 동료 검토.
3. `report.json` 조립 → `build-report.mjs` → `dist/<slug>/index.html`.

품질은 분산 모드보다 낮다(모델 다양성 없음) — 가능하면 cmux 분산 모드를 권장한다.

## 단독 호출 가능한 4개 자식 스킬

이 파이프라인의 각 단계는 독립 스킬로도 호출된다 (전역 심링크):
- `/storm-scan` — 다중 관점 스캔 (Phase 1+3)
- `/storm-contradict` — 모순 지도 (Phase 5.1)
- `/storm-synthesize` — 종합 (Phase 5.2)
- `/storm-review` — 동료 검토 (Phase 5.3)

## 절대 규칙 (HARD)

1. **출처 없는 단언 금지** — 모든 영혼·종합이 `[출처: URL]`. 추측은 `[추론]`. 가짜 출처·가짜 수치 금지.
2. **메인이 모든 페인을 만든다** — 영혼은 자기 페인을 못 만든다 (요구 7).
3. **양방향 통신** — 영혼은 cmux send로 메인에 스스로 보고 (요구 4).
4. **수치 정확** — STORM 효과는 "조직성 +25% / coverage +10%". "25% 더 똑똑"은 claim drift (provenance.md).
5. **동료 검토 없이 최종화 금지** — 논문이 경고한 source bias transfer / over-association를 반드시 점검.
6. **TSX/regex 자동편집 등 무관 규칙 비적용** — 이 스킬은 리서치·HTML 산출 전용.

## 설치 (로컬 원본 + 전역 심링크)

```bash
cd <이 레포>/storm-research && ./install.sh        # ~/.claude/skills 에 5개 심링크
./install.sh --check                               # 상태 점검
```
