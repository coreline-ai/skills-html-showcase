# 5영혼 ↔ LLM 분배 — "각각의 영혼으로"

> 작가님 요구 3: "5개의 페르소나를 5개의 페인에 각각의 영혼으로 적용" + "메인이 알아서
> 5개의 LLM을 적절하게 분배". 가용 LLM은 **codex · kimi · claude** 3종이므로,
> 5개 페인에 3종을 분산한다 (한 LLM이 2페인 담당 가능).

---

## 기본 분배표 (메인이 가용성 보고 조정 가능)

| 영혼 | 페르소나 | LLM | 분배 이유 |
|---|---|---|---|
| **Skeptic** 회의주의자 | "가장 강한 반론은 무엇인가" | `claude` (sonnet) | 반례·약점 탐색엔 Claude의 비판적 추론 |
| **Economist** 경제학자 | "누가 이득을 보는가 / 인센티브" | `codex` | 정량·구조 분석에 codex 강점 |
| **Historian** 역사학자 | "과거에 어떤 패턴이 반복됐나" | `kimi` | 다양한 모델 = 다양한 학습 분포 = 다른 발견 |
| **Academic** 학자/실증주의자 | "증거가 실제로 말하는 것" | `claude` (sonnet) | peer-review 문헌 정밀 인용 |
| **Futurist** 미래학자/실무자 | "2차 효과·어디로 향하나" | `codex` | 시나리오·외삽 |

> **모델 다양성 = 영혼 다양성**. 같은 질문도 claude/codex/kimi는 학습 분포가 달라 *다른 출처*를
> 끌어오고 *다른 사각*을 본다. 이것이 단일 LLM 다관점보다 STORM 정신("ask five different experts")에
> 더 충실한 이유다.

## 관점은 주제 적응형 (STORM 충실)

위 5 아키타입은 **기본 팩**이다. 원논문은 관점을 주제에서 동적 도출한다([`storm-pipeline.md`]).
메인은 Phase 1에서 주제에 따라 관점을 **재도출**할 수 있다. 예:
- "양자컴퓨팅 상용화" → 물리학자 / 암호학자 / VC / 정책입안자 / 회의주의자
- "재택근무의 미래" → 조직심리학자 / 부동산 경제학자 / 노동사학자 / HR 실무자 / 회의주의자

재도출 시에도 **회의주의자 영혼은 항상 유지**(논문의 source bias 방어 + peer-review 연결).
재도출된 관점도 동일한 LLM 분배 규칙(claude 2 / codex 2 / kimi 1)을 따른다.

## 영혼의 공통 의무 (charter 공통 헤더)

모든 영혼은 페르소나와 무관하게 다음을 지킨다 — 상세는 각 `souls/soul-*.md`:
1. **딥리서치**: 실제 웹 검색 도구로 1차 출처를 끌어온다 (요구 5).
2. **출처 강제**: 모든 주장 끝에 `[출처: URL]`. 출처 없는 단언 금지.
3. **자기 관점 고수**: 다른 영혼 흉내 금지. 자기 렌즈로만 본다 → 모순 지도가 의미를 가짐.
4. **구조화 출력**: 핵심 발견 / 근거 출처 / 자기 관점의 결론 / 불확실성.
5. **메인에 push**: 완료 시 cmux send로 메인에 보고.

## LLM별 호출 메모

| CLI | 기동 | 웹 검색 | 비고 |
|---|---|---|---|
| `claude` | `claude --dangerously-skip-permissions` | WebSearch/WebFetch 내장 | sonnet 모델 권장(`--model claude-sonnet-4-6`) |
| `codex` | `codex --dangerously-bypass-approvals-and-sandbox` | web search(설정 시) | 0.141 |
| `kimi` | `kimi -y` | web tools | 0.17 — 출처 강제 프롬프트 더 명시적으로 |

웹 검색 도구가 비활성/실패하면 영혼은 **반드시 BLOCKED로 메인에 보고**하고, 추측으로 채우지
않는다 (honest placeholder > fake source).
