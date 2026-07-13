# STORM Research OS — 다섯 영혼 리서치가 단일 답변을 이기는 조건

> STORM의 핵심은 다섯 명처럼 말하는 것이 아니라 다섯 개의 질문 경로가 서로 다른 출처를 끌어오고, 그 충돌을 보존한 뒤, 동료 검토로 비약을 치는 것이다. 이 산출물은 외부 웹을 새로 검색하지 않고 storm-research 로컬 스킬 내용만으로 작성한 content-only 연구다. 따라서 '새 주제에 대한 실제 딥리서치'가 아니라 'storm-research 스킬이 가르치는 리서치 운영체계'에 대한 분석이다.

## 1. 왜 단일 답변은 위험한가
단일 LLM 답변은 빠르지만 질문 경로가 하나다. storm-research 스킬은 이 문제를 회의주의자, 경제학자, 역사학자, 학자, 미래학자라는 다섯 영혼으로 쪼갠다. 각 영혼은 자기 렌즈에 맞는 질문을 던지고, 출처를 강제하며, 결과 파일과 done 마커로 메인에게 보고한다. [출처: sources/storm-SKILL.md]

## 2. 그러나 다관점만으로 충분하지 않다
다관점은 쉽게 역할극이 된다. provenance 문서는 과장된 바이럴 주장과 실제 논문 근거를 구분하라고 요구한다. 특히 '4개 프롬프트 = STORM'은 부분적이며, 진짜 STORM은 retrieval과 multi-perspective question asking을 포함한다. [출처: sources/provenance.md, sources/storm-pipeline.md]

## 3. 핵심 긴장: 운영비 대 신뢰도
full 모드는 cmux, 다중 CLI, 5페인 spawn, collect, report build가 필요하다. 이것은 비용이지만, 출처·모순·동료 검토가 중요한 주제에서는 신뢰를 위한 보험이다. 반대로 단순 요약이나 내부 메모에는 solo fallback이 더 합리적이다. [출처: sources/storm-SKILL.md]

## 4. 검토가 최종 품질을 만든다
storm-review는 source bias transfer와 over-association을 잡는다. 즉 출처 편향이 글로 전이되었는지, 관련 없는 사실을 부당하게 연결했는지, 모순을 봉합했는지 확인한다. 이 단계가 빠지면 STORM 리포트는 보기 좋은 종합문일 뿐 검증된 리서치가 아니다. [출처: sources/prompt-4-peer-review.md, sources/storm-pipeline.md]

## 미해결 질문
실제 조직에서 full STORM을 언제 켜고 언제 solo fallback으로 충분하다고 판단할 것인가? 이 질문은 비용, 주제 위험도, 출처 필요성, 의사결정 파급효과를 함께 보는 운영 정책이 필요하다.

