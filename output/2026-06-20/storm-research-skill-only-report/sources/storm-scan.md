# Multi-Perspective Scan · STORM Research OS — 다섯 영혼 리서치가 단일 답변을 이기는 조건
## Skeptic · 회의주의자
### 고유 결론
STORM을 프롬프트 팩처럼 쓰면 출처 없는 다관점 브레인스토밍으로 퇴화한다.
### 발견
회의주의자의 결론은 명확하다. STORM의 가치는 '다섯 관점' 자체가 아니라 각 관점이 실제 출처를 끌어와 반증 가능하게 보고하는 데 있다. 검색 도구가 없으면 BLOCKED를 보고하라는 규칙, 출처 없는 단언 금지, peer-review 없이는 최종화 금지라는 장치가 빠지면 겉모양만 STORM인 문서가 된다. [출처: sources/storm-SKILL.md, sources/provenance.md]
### 불확실성
이 산출물은 사용자의 요청에 따라 외부 웹 검색을 하지 않았으므로, 실제 주제 리서치가 아니라 storm-research 스킬 자체에 대한 content-only 연구다.

## Economist · 경제학자
### 고유 결론
full 모드는 비용이 크지만, 고위험·장문·출처 의존 리서치에서는 재작업 비용을 줄인다.
### 발견
경제적 렌즈에서 STORM은 모든 질문에 쓰는 도구가 아니다. cmux, 5개 페인, 여러 LLM, 결과 수집, 모순 지도, 동료 검토는 운영비를 만든다. 반대로 투자·정책·기술 판단처럼 잘못된 결론의 비용이 큰 주제에서는 출처 추적과 모순 표면화가 재작업 비용을 줄이는 보험이 된다. solo fallback은 빠르지만 모델 다양성이라는 이점은 낮아진다. [출처: sources/storm-SKILL.md]
### 불확실성
실제 비용 절감 수치는 skill 파일에 없으므로 수치화하지 않는다.

## Historian · 역사학자
### 고유 결론
STORM은 새 문장 생성기가 아니라 오래된 pre-writing 과정을 LLM 오케스트레이션으로 되살린다.
### 발견
storm-pipeline은 STORM을 Knowledge Curation, Outline Generation, Article Generation, Article Polishing의 흐름으로 매핑한다. 이것은 글쓰기 전 조사, 질문, 개요, 초안, 검토라는 오래된 작업 질서를 자동화한 것이다. 커뮤니티식 4프롬프트는 원논문과 동일하지 않고 STORM의 정신을 압축한 재해석이라는 점도 명시되어 있다. [출처: sources/storm-pipeline.md, sources/provenance.md]
### 불확실성
역사적 유사 사례 비교는 외부 자료가 필요하므로 여기서는 skill 내부 설명에 한정한다.

## Academic · 학자
### 고유 결론
정확한 수치는 '조직성 +25%, coverage +10%'이며 모델 지능 향상 주장이 아니다.
### 발견
학술적 핵심은 수치의 해석이다. provenance 문서는 '25% better at research' 같은 표현을 claim drift로 규정한다. 정확한 문장은 outline-driven RAG baseline 대비 생성 글의 조직성은 +25%, coverage breadth는 +10%라는 것이다. 또한 논문이 지적한 실패모드는 source bias transfer와 over-association이며, 이 스킬은 peer-review 단계로 이를 잡도록 설계한다. [출처: sources/storm-pipeline.md, sources/provenance.md]
### 불확실성
이 수치는 storm-research 스킬의 provenance 기록을 따른 것이며, 본 산출물에서 원논문을 새로 재검증하지 않았다.

## Futurist · 미래학자
### 고유 결론
리서치 워크플로우의 미래는 답변 생성보다 출처·모순·검토 상태를 운영하는 Research Ops다.
### 발견
미래학자 렌즈에서 STORM의 중요한 전환은 '한 번에 좋은 답을 받기'가 아니라 '리서치 상태를 관리하기'다. Phase 0 환경 판별, 영혼별 done 파일, BLOCKED 처리, report.json 스키마, HTML 검수까지 포함하면 리서치는 대화가 아니라 운영 파이프라인이 된다. [추론] 이러한 구조는 앞으로 사내 리서치·정책 검토·기술 의사결정에서 출처 감사 가능한 Research Ops로 발전할 수 있다. [출처: sources/storm-SKILL.md, sources/report.schema.json]
### 불확실성
미래 시나리오는 [추론]이며, 외부 시장 신호는 이번 content-only 조건 때문에 수집하지 않았다.

