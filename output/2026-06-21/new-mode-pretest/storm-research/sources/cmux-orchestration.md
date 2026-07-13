# cmux 영혼 오케스트레이션 — 페인 생성·통신·수집

> **메인 Opus가 모든 페인을 만든다** (작가님 요구 7번). 영혼은 쓰고 보고하는 워커.
> 통신은 **cmux send 양방향** — 메인→영혼(브리프 전달), 영혼→메인(결과 push) (요구 4번).
>
> 기반: `~/.claude/skills/cmux-harness`의 검증된 프로토콜을 STORM 5영혼용으로 특화.
> 송수신 헬퍼는 본 스킬 `scripts/lib.sh`에 자급자족 버전으로 vendoring.

---

## 전제

- cmux 터미널 내부에서 메인 실행 (`$CMUX_WORKSPACE_ID` 자동 설정).
- cmux CLI: `/Applications/cmux.app/Contents/Resources/bin/cmux` (PATH에 있으면 `cmux`).
- CLI 3종 설치 확인됨: `claude`, `codex`(0.141), `kimi`(0.17).

## 핵심 제약 — cmux는 탭 이름을 안 받는다

`cmux --surface`는 **surface ref(`surface:N`)만** 받는다(탭 이름 X). 따라서:
1. 페인 생성 시 반환된 ref를 `.storm/pane-refs.json`에 영혼 이름과 매핑 저장.
2. 모든 송수신은 `lib.sh`의 `resolve_soul <name>`로 ref를 조회.
3. 캐시 손실 시 `cmux tree` 파싱 폴백.

## 페인 레이아웃 (메인이 생성)

```
┌─────────────┬─────────────┐
│   Main      │  Skeptic    │   Main: 오케스트레이터 (이 Opus 세션)
│  (Opus)     │  (claude)   │   Skeptic/Academic: claude (sonnet)
├──────┬──────┼──────┬──────┤   Economist/Futurist: codex
│Econo │Histo │Acade │Futur │   Historian: kimi
│(codex)│(kimi)│(claude)│(codex)│
└──────┴──────┴──────┴──────┘
```

5영혼 = 5개 새 페인. 메인은 자기 페인을 제외하고 5개를 `cmux new-pane`으로 생성한다.

## 메시지 전송 규약 (핵심)

`cmux send`는 **키 입력만** 주입한다. 개행은 별도 `send-key Enter`. 한글·긴 메시지에서
Enter가 텍스트 중간에 끼는 race를 막으려면 사이에 `sleep 0.3`. → `lib.sh`의 `soul_send`가 캡슐화.

```bash
# 짧은 지시
soul_send Skeptic "read .storm/<proj>/briefs/skeptic.md 그리고 실행"
# 내부: cmux send --surface <ref> "<text>"; sleep 0.3; cmux send-key --surface <ref> Enter
```

**긴 브리프는 파일로.** 메시지에 직접 긴 텍스트를 send하지 말고, 브리프를 파일에 쓴 뒤
"read <파일> 후 실행" 한 줄만 보낸다 (입력 유실 최소화).

## 양방향 통신 부트스트랩 (ABSOLUTE — 영혼 첫 통신 시 필수)

메인이 영혼과 **처음 통신할 때**, 영혼에게 역방향 송신법을 가르친다. 모든 브리프에 포함:

> "너는 메인(오케스트레이터)에게 직접 메시지를 보낼 수 있다. 방법:
>  `cmux send --surface <MAIN_REF> '<영혼명> <상태>: <내용>'` 실행 후
>  `cmux send-key --surface <MAIN_REF> Enter`.
>  완료(DONE)·차단(BLOCKED)·중요 진행(PROGRESS) 시 반드시 이 방법으로 push하라.
>  `<MAIN_REF>`는 브리프 상단에 적힌 값이다."

**왜**: done 파일·화면 마커는 메인이 *폴링*해야만 보인다. 영혼이 역방향 send로 push하면
메인이 실시간으로 완료를 안다. 파일 시그널은 신뢰 1순위(push 유실 대비), send는 지연 제거용 —
**대체가 아니라 병행**. (작가님 요구 4: "각 터미널이 스스로 메인에게 메시지를 보내도록".)

## 완료 시그널 프로토콜 (파일 1순위 + send push + 화면 마커 폴백)

각 영혼은 작업 완료 시 정확히 이 순서로:
1. 결과를 `.storm/<proj>/results/<soul>.md`에 쓴다 (인용 포함 — **이게 산출물**).
2. `touch .storm/<proj>/done/<soul>.done` (진짜 완료 신호 — 메인 폴링 1순위).
3. 메인에 push: `cmux send --surface <MAIN_REF> "<soul> DONE: <한 줄 요약>"` + Enter.
4. 화면 마지막 줄에 마커: `STORM_SOUL_DONE` (또는 차단 시 `STORM_SOUL_BLOCKED`).

메인의 `collect-souls.sh`는 (1) done 파일을 1순위 폴링, (2) send push를 실시간 수신,
(3) 화면 마커를 폴백으로 사용한다.

## 타임아웃 기본값

| 동작 | 타임아웃 |
|---|---|
| CLI 프롬프트 준비 | 60초 |
| 영혼 딥리서치 1회 | 8~12분 |
| 전체 5영혼 수집 | 15분 (병렬이므로 가장 느린 영혼 기준) |

초과 시 메인이 `cmux capture-pane`으로 상태 확인 → 사용자에게 계속/중단 질의.

## 권한 완전 허용 기동 플래그 (페인 spawn 시)

| CLI | 플래그 |
|---|---|
| claude | `--dangerously-skip-permissions` |
| codex | `--dangerously-bypass-approvals-and-sandbox` |
| kimi | `-y` (`--yolo`) |

리서치 중 권한 프롬프트로 멈추지 않게 모든 영혼은 권한 허용 모드로 기동.
(`lib.sh`가 `--help`로 실제 플래그를 재검증 후 적용 — 버전업 대비.)
