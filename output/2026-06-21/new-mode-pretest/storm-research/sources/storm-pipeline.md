# STORM 파이프라인 — 원논문 충실 매핑

> **단일 출처**: Shao et al., *"Assisting in Writing Wikipedia-like Articles From Scratch with Large Language Models"*, NAACL 2024.
> 논문 https://arxiv.org/abs/2402.14207 · 코드(MIT) https://github.com/stanford-oval/storm · 라이브 도구 https://storm.genie.stanford.edu
>
> 이 문서는 본 스킬의 5영혼·4프롬프트 파이프라인이 **원논문의 어느 단계를 구현하는지** 추적성을 박는다.
> 과장 없이 — 논문이 실제로 말한 것만. 과장-사실 구분은 [`provenance.md`](./provenance.md).

---

## STORM = Synthesis of Topic Outlines through Retrieval and Multi-perspective question asking

핵심 통찰(논문 §1): **"좋은 질문을 하는 것이 좋은 리서치의 절반"**. 사람 전문가는 주제에 대해
*다양한 관점*에서 질문하고, *신뢰할 수 있는 출처*에 근거(grounding)해 답을 채운다. STORM은
이 사전조사(pre-writing) 과정을 LLM으로 시뮬레이션한다.

## 원논문 4 모듈 (코드의 `STORMWikiRunner` 실행 순서)

| 단계 | 코드 플래그 | 입력 | 출력 | 본 스킬 매핑 |
|---|---|---|---|---|
| **1. Knowledge Curation** | `do_research=True` | 주제 | 관점별 대화 로그 + 인용된 출처 모음 | **5영혼 딥리서치** (페인 분산) |
| **2. Outline Generation** | `do_generate_outline=True` | 수집 정보 | 계층적 개요 | **storm-synthesize**의 개요 단계 |
| **3. Article Generation** | `do_generate_article=True` | 개요 + 출처 | 인용 포함 본문 | **storm-synthesize**의 집필 단계 |
| **4. Article Polishing** | `do_polish_article=True` | 본문 | 요약(lead) 추가 + 중복 제거 | **storm-review** + HTML 정리 |

### 1단계 내부 — Knowledge Curation (가장 중요)

논문의 두 핵심 메커니즘이 여기 있다:

#### (a) Perspective-Guided Question Asking (관점 유도 질문)
- 주제와 **유사한 기존 위키 문서들**(related topics)을 surveying 하여, 그 문서들의
  목차(table of contents) 구조에서 **서로 다른 관점(perspective)** N개를 LLM이 도출한다.
- 각 관점은 "그 주제를 어떤 렌즈로 보는 작성자"다. 관점이 질문 생성을 **제어(control)** 한다 →
  관점이 다르면 질문이 달라지고, 질문이 다르면 발견하는 정보가 달라진다.
- **본 스킬의 차이**: STORM은 관점을 주제에서 동적으로 도출한다. 본 스킬은 기본값으로
  5개 아키타입(회의주의자·경제학자·역사학자·학자·미래학자)을 제공하되, 메인이 주제에 맞게
  관점을 **재도출**할 수 있다(§참조: 메인 SKILL.md Phase 1). 둘 다 지원.

#### (b) Simulated Conversation (시뮬레이션 대화 + 검색 grounding)
- 각 관점은 **"위키 작성자(질문자)"** 역할로, **"주제 전문가(답변자)"** 와 다중 턴 대화를 한다.
- 작성자가 질문 → 전문가가 답하기 위해 질문을 **검색 쿼리로 분해** → 인터넷 검색 →
  **신뢰할 수 있는 출처만 필터링** → 출처에 근거해 답변(인용 포함).
- 작성자는 대화 히스토리를 보고 **후속 질문(follow-up)** 을 던져 이해를 갱신한다.
- 산출: 관점별 대화 로그 + 그 안에 인용된 모든 출처의 모음(reference store).

> **본 스킬 구현**: 5영혼이 각각 별도 LLM 페인에서 "작성자+전문가"를 한 몸으로 수행한다.
> 즉 자기 관점의 질문을 스스로 던지고, **실제 웹 검색 도구로 출처를 끌어와** 답을 채운 뒤,
> 모든 주장에 인용을 박아 보고한다. 이게 1단계 Knowledge Curation의 분산 구현이다.

### 2~4단계 — Writing Stage

- **Outline**: 먼저 LLM 내부지식으로 초안 개요 → 수집한 대화/출처로 **정제**.
- **Article**: 개요의 각 섹션을, 그 섹션에 매칭되는 출처들을 retrieval 해 인용과 함께 집필.
- **Polish**: 전체를 요약하는 lead 문단 추가, 중복 제거.

## Co-STORM (확장판) — 본 스킬의 "모순 지도"가 차용

논문 후속 Co-STORM은 협업적 담화(collaborative discourse)를 도입한다:
- **LLM 전문가들** (질문/답변), **moderator**(생각을 자극하는 질문 생성),
  **사람 사용자**(관찰 또는 능동 개입).
- 정보를 계층적으로 조직하는 **동적 mind map**으로 공유 개념 공간을 만든다.

> **본 스킬 매핑**: **storm-contradict**(모순 지도)가 Co-STORM의 moderator 역할 +
> mind map의 "관점 간 긴장(tension) 표면화"를 차용한다. 5영혼이 *어디서 서로 부딪히는지*를
> 명시적으로 도식화 → 단일 관점이 놓치는 "아무도 못 본 것"을 드러낸다.

## 논문이 보고한 한계 (반드시 산출물에 반영)

전문가 평가에서 grounded long-form 생성의 두 문제가 지적됨(논문 §결론):
1. **Source bias transfer** — 출처의 편향이 글로 전이됨.
2. **Over-association of unrelated facts** — 관련 없는 사실들을 부당하게 연결.

> **본 스킬의 방어선**: **storm-review**(동료 검토 영혼)가 이 두 가지를 전담 점검한다.
> (1) 출처 다양성·편향 점검, (2) 인과/연결의 비약 점검. peer-review 없이 종합본을 최종화 금지.

## 평가 결과 (정확한 수치 — 과장 금지)

논문 자체 평가(FreshWiki, outline-driven RAG baseline 대비):
- **조직성(organization)**: +25% (절대값 개선)
- **포괄성/coverage breadth**: +10%

> "25% better at research" 같은 표현은 **claim drift**다. 정확히는 *조직성 25%*, *coverage 10%*.
> 자세한 과장 사례는 [`provenance.md`](./provenance.md).
