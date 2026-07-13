# STORM식 다관점 리서치가 AI HTML 리포트 생성 파이프라인에 주는 실제 가치와 한계 — 모순 지도

## 합의 지점
- 다섯 관점 모두 STORM의 강점이 최종 문장 생성보다 pre-writing 단계, 특히 질문 생성과 개요 품질에 있다고 본다.
- 출처 grounding이 있어도 편향 전이와 부당한 연결을 별도 검토해야 한다는 데 합의한다.
- 하이브리드 산출물은 연구 내용과 HTML 표현 계층을 분리해야 검증 가능성이 높아진다.

## 모순 지점

### 품질 개선 수치를 도입 근거로 삼을 수 있는가
- A: 학자 관점: +25% 조직성, +10% coverage는 명확한 연구 결과이므로 pre-writing 품질 개선 근거가 된다. [출처: https://storm-project.stanford.edu/research/storm/]
- B: 회의주의자 관점: 같은 자료가 publication-ready가 아니며 source bias transfer를 경고하므로 최종 품질 보장으로 읽으면 안 된다. [출처: https://github.com/stanford-oval/storm]
- 미해결 이유: 평가 지표가 조직/coverage 중심이라 factuality·편집 비용·도메인별 안전성까지 포괄하지 않는다.

### 자동화는 비용을 줄이는가, 새 비용을 만드는가
- A: 경제학자 관점: 개요와 질문을 먼저 검수하면 재작성 비용을 줄일 수 있다. [추론]
- B: 경제학자/회의주의자 관점: 검색 API, retriever, 모델 계층, 편집 검수 비용이 새로 생긴다. [출처: https://github.com/stanford-oval/storm]
- 미해결 이유: 조직별 주제 난도와 편집자 시간 단가가 달라 공통 ROI를 단정할 수 없다.

### 사용자가 질문해야 하는가, agent가 질문해야 하는가
- A: Co-STORM 관점: agent들이 사용자를 대신해 질문을 던져 unknown unknowns를 발견하게 한다. [출처: https://aclanthology.org/2024.emnlp-main.554/]
- B: 회의주의자 관점: 사용자가 질문을 조향하지 않으면 출처 선택과 프레이밍이 시스템 편향으로 굳을 수 있다. [추론]
- 미해결 이유: autonomous discovery와 human steering의 최적 비율은 과업과 위험 수준에 따라 달라진다.

## 사각지대
- 한국어·로컬 지식베이스에서 perspective mining과 검색 grounding 품질이 영어 Wikipedia-like 주제만큼 유지되는지 별도 검증이 필요하다.
- 비공개 내부 문서 기반 리서치에서 개인정보·보안 경계가 어디에 놓여야 하는지 이 자료만으로는 충분하지 않다.
- adaptive-html-final 출력의 품질 게이트는 HTML 무결성 검증이지, STORM 리서치 사실성 검증을 자동 대체하지 않는다.

## 핵심 긴장
STORM은 ‘더 똑똑한 최종 저자’인가, 아니면 ‘더 좋은 질문과 개요를 만드는 사전 조사 엔진’인가. 이 하이브리드의 안전한 결론은 후자다.
