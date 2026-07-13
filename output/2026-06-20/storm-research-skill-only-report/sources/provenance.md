# 출처 계보 + 과장-사실 구분 (Provenance & Honesty)

> 본 스킬은 바이럴 X 스레드 하나가 아니라 **원논문 + 라이브 도구 + 비판적 답글들**을 함께
> 출처로 삼는다. 작가님 지시: "링크의 원문과 참조 글을 사용해서". 따라서 이 문서는
> 산출물이 *무엇을 근거로 했고, 무엇이 과장인지*를 투명하게 박는다.

---

## 1차 출처 (Primary — 진짜 STORM)

| 자원 | URL | 역할 |
|---|---|---|
| 원논문 (Shao et al., NAACL 2024) | https://arxiv.org/abs/2402.14207 | 방법론 SSOT |
| 코드 (MIT, stanford-oval/storm) | https://github.com/stanford-oval/storm | 구현 참조 |
| 라이브 도구 | https://storm.genie.stanford.edu | **진짜 STORM을 쓰고 싶으면 여기** |
| Stanford STORM 프로젝트 | https://storm-project.stanford.edu/research/storm/ | 연구 페이지 |

## 2차 출처 (Secondary — 바이럴 스레드, "4프롬프트 방법"의 출처)

| 글 | URL | 메모 |
|---|---|---|
| 시드 아티클 — @heynavtoor "The Stanford STORM Method…" | https://x.com/heynavtoor/status/2067194761446920264 | 조회 130만·북마크 9,764. **4프롬프트(Multi-Perspective Scan / Contradiction Map / Synthesis / Peer Review)의 출처** |
| 후속 재홍보 — @heynavtoor | https://x.com/heynavtoor/status/2067281413368611267 | "ask five, from five different experts" |

## 3차 출처 (비판·교정 — 반드시 함께 읽음)

| 관점 | 글 | 핵심 |
|---|---|---|
| 반대 관점 | @QuantumTumbler "Good workflow. Bad hype." | https://x.com/QuantumTumbler/status/2067425115563049044 — 워크플로우는 유용, 마케팅은 과장 |
| AI 탐지 주장 | @pangram "fully AI-generated" | https://x.com/pangram/status/2067365726638223513 — 시드 문서가 AI 생성으로 의심됨(신뢰도 단서 동반) |
| 교정성 답글 | @savivila "Just one link — storm.genie.stanford.edu" | https://x.com/savivila/status/2067417794140868948 — **진짜 도구 링크** |
| 수치 왜곡 | @IhorSkiba "MAKES CLAUDE 25% BETTER AT RESEARCH" | https://x.com/IhorSkiba/status/2067601222488805453 — **claim drift 사례** |
| 다국어 재유통 | @LinearUncle(中)·@AdamPrabata(印尼)·@FinanceYF5(中) | — 바이럴 확산, 내용 검증 없이 번역 전파 |

---

## 과장-사실 구분표 (산출물에 그대로 반영)

| 떠도는 주장 | 사실 | 근거 |
|---|---|---|
| "STORM이 Claude를 25% 더 똑똑하게" / "25% better at research" | **틀림.** 논문은 *조직성(organization) +25%*, *coverage +10%*. 모델 지능이 아니라 **생성된 글의 구조 품질** 지표. | 논문 abstract |
| "4개 프롬프트 = STORM" | **부분적.** 4프롬프트는 STORM의 *정신*(다관점 질문 + 출처 grounding)을 근사한 **커뮤니티 워크플로우**. 논문의 검색-grounding 대화 시뮬레이션과 동일하지 않음. | [`storm-pipeline.md`](./storm-pipeline.md) |
| "소프트웨어/GitHub 불필요, 붙여넣기만" | 4프롬프트 방법은 그렇다. 하지만 **진짜 STORM**은 storm.genie.stanford.edu(무료) 또는 오픈소스. | @savivila |
| 시드 아티클이 권위 있는 1차 자료 | AI 생성 의심됨(@pangram). **권위는 논문에 있다.** | @pangram |

## 본 스킬의 정직성 계약 (Honesty Contract)

1. **모든 영혼은 모든 주장에 출처(URL)를 박는다.** 출처 없는 단언 금지 (작가님 요구 5번).
2. **수치는 정확히.** "25% 조직성 / 10% coverage" — claim drift 금지.
3. **진짜 STORM 링크를 산출물 footer에 항상 표기** (storm.genie.stanford.edu + 논문).
4. **본 스킬은 STORM의 *재구현이 아니라 재해석***임을 HTML 리포트에 명시.
5. **출처 편향·비약은 peer-review 영혼이 점검** (논문이 경고한 source bias transfer / over-association).
