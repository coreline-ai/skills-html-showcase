# STORM식 다관점 리서치가 AI HTML 리포트 생성 파이프라인에 주는 실제 가치와 한계 — 다중 관점 스캔

- 실행 모드: solo-fallback
- 사유: CMUX_WORKSPACE_ID와 cmux CLI가 없어 storm-research full 분산 모드 대신 인라인 4프롬프트 파이프라인을 사용했다.

## 1. 회의주의자 관점

역할: 가장 강한 반론·검증 실패 모드 탐색

### 발견
- STORM의 평가상 이득은 조직성·coverage 지표이지, 자동으로 출판 가능한 글을 보장한다는 뜻이 아니다. GitHub README도 출판 품질 문서에는 상당한 편집이 필요하다고 적고, 숙련된 Wikipedia 편집자에게는 pre-writing 단계에서 유용하다고 범위를 제한한다. [출처: https://github.com/stanford-oval/storm]
- 원논문·프로젝트 페이지가 직접 지목한 실패 모드는 source bias transfer와 unrelated facts over-association이다. 즉 검색 grounding이 있어도 출처 편향과 부당한 연결은 남는다. [출처: https://storm-project.stanford.edu/research/storm/]
- 따라서 하이브리드 HTML 산출물은 ‘리서치 엔진의 최종판’이 아니라 ‘출처·모순·검토를 보존한 의사결정 초안’으로 배치해야 한다. [추론]

결론: STORM은 결론 제조기가 아니라 질문·출처·모순을 끌어내는 pre-writing 엔진으로 써야 안전하다.
불확실성: 상용 deep-research 도구와의 비용/정확도 비교는 같은 벤치마크가 없으므로 이 문서에서는 단정하지 않는다.

## 2. 경제학자 관점

역할: 비용·운영 레버·ROI 관점

### 발견
- STORM은 긴 글 생성을 pre-writing과 writing으로 분리한다. 이 분리는 리서치/개요 품질을 먼저 검수해 재작성 비용을 낮추는 운영 레버가 된다. [출처: https://storm-project.stanford.edu/research/storm/]
- 공식 GitHub 예시는 conversation simulator에는 더 저렴하고 빠른 모델을, article generation에는 더 강한 모델을 쓰는 구성을 제안한다. 즉 비용 최적화의 핵심은 전 단계에 같은 고가 모델을 쓰지 않는 것이다. [출처: https://github.com/stanford-oval/storm]
- 2024~2025 업데이트에서 `knowledge-storm` 패키지, VectorRM, 다양한 retriever/search integration, LiteLLM 통합이 언급된다. 이는 도입 비용이 ‘프롬프트 하나’가 아니라 검색·모델·문서 저장소 구성 비용을 포함한다는 뜻이다. [출처: https://github.com/stanford-oval/storm]

결론: 경제적 가치는 초안 품질보다 ‘질문/개요 검수 루프를 앞당기는 것’에서 먼저 발생한다.
불확실성: 실제 조직 ROI는 주제 난도, 검색 API 비용, 편집자 검수 시간에 따라 달라져 별도 계측이 필요하다.

## 3. 역사학자 관점

역할: RAG·장문 생성의 반복 패턴 관점

### 발견
- STORM 프로젝트는 긴 인용 글 생성이 어렵고 평가도 어렵기 때문에 pre-writing과 writing의 두 단계로 나눈다고 설명한다. [출처: https://storm-project.stanford.edu/research/storm/]
- 프로젝트 페이지는 직접 질문 생성을 지시하면 특히 long-tail 주제에서 피상적 질문으로 흐르기 쉽다고 설명하고, 이를 보완하기 위해 perspective-guided question asking과 simulated conversation을 쓴다. [출처: https://storm-project.stanford.edu/research/storm/]
- Co-STORM은 사용자가 모든 질문을 직접 떠올려야 하는 QA 방식의 한계를 ‘unknown unknowns’ 문제로 재정의하고, 여러 LM agent 담화를 관찰·조향하게 만든다. [출처: https://aclanthology.org/2024.emnlp-main.554/]

결론: 역사적 패턴은 ‘답변 생성’보다 ‘좋은 질문을 먼저 만드는 구조’가 장문 품질의 병목이라는 쪽으로 이동한다.
불확실성: STORM 계열이 모든 도메인에서 기존 편집 워크플로우를 대체한다는 근거는 없다.

## 4. 학자 관점

역할: 논문·평가·검증 가능 주장 중심

### 발견
- STORM 원논문은 Wikipedia-like long-form articles를 생성하기 위해 diverse perspectives, grounded simulated conversation, outline curation을 결합한다고 설명한다. [출처: https://arxiv.org/abs/2402.14207]
- FreshWiki 평가에서 outline-driven RAG baseline과 비교해 STORM 산출물이 organized로 판단되는 비율이 25%p 높고, broad in coverage가 10% 높았다고 보고한다. [출처: https://storm-project.stanford.edu/research/storm/]
- Co-STORM의 EMNLP 2024 페이지는 사용자가 검색엔진보다 Co-STORM을 선호한 비율 70%, RAG chatbot보다 선호한 비율 78%를 초록에 명시한다. [출처: https://aclanthology.org/2024.emnlp-main.554/]

결론: 검증 가능한 주장은 ‘조직성·coverage·사용자 선호’ 개선까지이며, 사실 정확도 만능 주장은 이 자료만으로는 과장이다.
불확실성: 수치들은 특정 벤치마크와 연구 설정의 결과이므로, 로컬 스킬 산출물에는 재검증 없이 그대로 일반화하지 않는다.

## 5. 미래학자 관점

역할: 하이브리드 도구·출판 파이프라인 전망

### 발견
- Co-STORM은 여러 LM agents가 사용자 대신 질문을 던지고, 사용자는 담화를 관찰하거나 조향한다는 모델이다. [출처: https://aclanthology.org/2024.emnlp-main.554/]
- 공식 GitHub README는 Co-STORM이 discourse를 hierarchical concept structure인 dynamic mind map으로 조직해 shared conceptual space를 만든다고 설명한다. [출처: https://github.com/stanford-oval/storm]
- 이 프로젝트의 hybrid 방식은 STORM의 ‘내용 생산/검토’와 adaptive-html-final의 ‘무 JS 단일 HTML·테마·검증 게이트’를 분리하므로, 리서치 품질과 배포 안정성을 각각 다른 계약으로 관리할 수 있다. [추론]

결론: 다음 실용 지점은 ‘STORM으로 출처·모순·검토를 만들고, 검증 가능한 HTML 스킬로 발표물을 고정하는 이중 계약’이다.
불확실성: 다중 agent 담화가 조직 내 의사결정 품질을 얼마나 높이는지는 실제 사용 로그와 편집자 평가가 필요하다.

## 통합 참고 출처

- Assisting in Writing Wikipedia-like Articles From Scratch with Large Language Models: https://arxiv.org/abs/2402.14207
- Stanford STORM Research Project: https://storm-project.stanford.edu/research/storm/
- stanford-oval/storm GitHub repository: https://github.com/stanford-oval/storm
- Into the Unknown Unknowns: Engaged Human Learning through Participation in Language Model Agent Conversations: https://arxiv.org/abs/2408.15232
- Co-STORM ACL Anthology page: https://aclanthology.org/2024.emnlp-main.554/
- local orginal_skill/storm-research/SKILL.md: orginal_skill/storm-research/SKILL.md
