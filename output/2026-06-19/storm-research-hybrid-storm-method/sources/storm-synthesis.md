# STORM식 다관점 리서치가 AI HTML 리포트 생성 파이프라인에 주는 실제 가치와 한계

> STORM식 다관점 리서치의 실질 가치는 최종 문장을 대신 써주는 데 있지 않다. 더 정확한 위치는 ‘질문을 다양화하고, 출처를 묶고, 모순을 드러내는 pre-writing 엔진’이다. 따라서 이 프로젝트의 안전한 하이브리드는 storm-research가 만든 내용만 사용하고, 표현·테마·무결성은 adaptive-html-final v5.10.5의 HTML 계약으로 고정하는 방식이다.

## 1. 무엇이 검증됐나
STORM 원논문은 diverse perspectives, grounded simulated conversation, outline curation을 결합해 long-form article pre-writing을 개선하는 시스템을 제안한다. Stanford 프로젝트 페이지는 FreshWiki 평가에서 organized 판단이 25%p, coverage breadth가 10% 높았다고 요약한다. 그러나 이 수치는 글쓰기 품질의 특정 차원을 말하며 사실 검증 만능이나 출판-ready를 뜻하지 않는다.

## 2. 왜 질문 생성이 병목인가
프로젝트 페이지는 직접 prompting만으로는 long-tail 주제에서 피상적 질문이 나오기 쉽다고 설명한다. STORM은 관점을 먼저 부여하고, 검색 기반 답변으로 이해가 갱신될 때 후속 질문을 유도한다. 이는 HTML 리포트 생성에서도 ‘본문을 바로 쓰기’보다 ‘질문·개요·출처를 먼저 잠그기’가 품질 병목이라는 교훈으로 이어진다.

## 3. 어디서 실패하는가
논문과 프로젝트 페이지가 직접 경고한 실패 모드는 source bias transfer와 over-association이다. 다시 말해, 출처를 붙였다고 해서 편향이 사라지지 않고, 서로 관련 없는 사실을 자연스러운 이야기로 엮는 위험이 남는다. 그래서 storm-research 파이프라인의 peer review 단계는 장식이 아니라 필수 게이트다.

## 4. 하이브리드 출력의 운영 해석
이 산출물은 STORM의 HTML 빌더를 쓰지 않고, storm-research의 스캔·모순 지도·종합·동료 검토 내용만 가져온다. 그런 다음 adaptive-html-final의 expert_html 레이아웃, risk-matrix vt 템플릿, wg-16 구현 계획 위젯, CSS 해시·source snapshot 검증으로 표현 계층을 고정한다. 내용 검증과 표현 검증을 분리하는 것이 핵심이다.

## 미해결 질문
- 내부 문서/한국어 자료에서 STORM식 perspective mining이 동일하게 효과적인지 검증이 필요하다.
- 다중 LLM을 실제로 병렬 실행할 때 비용·속도·출처 품질이 단일 LLM solo fallback보다 얼마나 나은지 계측해야 한다.
- HTML 품질 게이트가 통과해도 리서치 사실성은 별도 출처 감사와 peer review를 유지해야 한다.

## 참고 출처
- https://arxiv.org/abs/2402.14207
- https://storm-project.stanford.edu/research/storm/
- https://github.com/stanford-oval/storm
- https://arxiv.org/abs/2408.15232
- https://aclanthology.org/2024.emnlp-main.554/
- orginal_skill/storm-research/SKILL.md
