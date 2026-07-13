# BizPlan Architect — 에이전트 역할 플레이북

이 폴더는 메인 스킬이 `Task` 도구로 서브에이전트를 dispatch할 때 **프롬프트에 녹여 쓸 역할 정의**다. Claude Code의 `.claude/agents` 서브에이전트 정의(YAML frontmatter)가 아니라 순수 마크다운 플레이북이다. 매핑은 PRD §23, 폴더·산출물은 SKILL.md 프로젝트 스캐폴딩, 절대 규칙은 SKILL.md §7대 절대 규칙이 단일 출처다.

## 12개 에이전트

| 파일 | 역할 | 주 산출 위치 |
|---|---|---|
| `orchestrator.md` | 진행관리·작업배정·공고/사업방향 일치 판단·충돌조정·최종통합 (직접 조사 안 함) | `project.json`, `09-audit/revision-log.md` |
| `notice-analyst.md` | 공고·첨부 수집, 자격·배점·일정·서식 분석 | `01-notice-analysis/` |
| `interviewer.md` | 적응형 심층 인터뷰, 모호성 탐지, 경험/증거 추출, 모순 확인 | `02-interview/`, `03-idea-and-title/title-candidates.md` |
| `market-researcher.md` | 사회·경제·산업·시장 조사 | `04-research/market/` |
| `competitor-analyst.md` | 국내외 제품·경쟁회사·대체재 분석 | `04-research/competitors/` |
| `patent-analyst.md` | 특허 검색·패밀리·법적상태·청구항 비교·예비 FTO·권리화 기회 | `04-research/patents/` |
| `paper-analyst.md` | 논문 검색·방법론/성능·재현성·연구공백·TRL | `04-research/papers/` |
| `business-analyst.md` | TAM/SAM/SOM·가격·수익모델·고객확보·매출 추정 | `05-business-core/` (sizing·financial xlsx) |
| `document-designer.md` | 서식 분석·목차 매핑·섹션별 메시지 설계 | `06-template-design/` |
| `visualizer.md` | 표·그래프·다이어그램·구성도 | `07-diagrams/` |
| `editor.md` | 초안 작성·문체/분량 조절·반복 표현 제거 | `08-draft/` |
| `verifier.md` | 사실·출처·특허·논문·숫자·논리·서식 검증 (PRD §20 배점) | `09-audit/` |

## Dispatch 방법

1. **병렬 호출** — 독립적인 단계는 메인이 **단일 메시지에 여러 `Task` 호출**을 넣어 동시 실행한다.
   - Gate 2 리서치: `market-researcher`, `competitor-analyst`, `patent-analyst`, `paper-analyst`, `business-analyst`를 한 번에.
   - Gate 7 검증: `verifier`를 4역할(`admin`/`tech`/`biz`/`skeptic`)로 한 번에.
2. **공통 컨텍스트** — 서브에이전트는 컨텍스트를 공유하지 않으므로 매 dispatch마다 **반드시 명시**한다:
   - ① `business-core.yaml`(현재본) + `research-plan.md` 경로
   - ② 출처 우선순위 10단계 + 증거 태그 규칙(`[사실][추정][가정][목표][확인 필요]`)
   - ③ 산출 파일 경로 (위 표 — SKILL.md 폴더 매핑과 정확히 일치)
   - ④ 7대 절대 규칙 (SKILL.md §7대 절대 규칙)
   - ⑤ 해당 단계 reference 문서 경로(`references/NN-*.md`)
3. **공통 산출 규약** — 각 리서치 에이전트는 자기 영역만 조사해 구조화 산출물(md 또는 xlsx 행)로 반환하고, 모든 자료를 `04-research/source-index.xlsx` 형식으로 출처 기록한다. `patent-analyst`/`paper-analyst`는 "예비 검토·법률 의견 아님 / 논문 성능 ≠ 제품 성능" 경고를 산출물에 명시한다.
4. **서브에이전트 없는 환경** — `Task` 도구가 없으면 메인이 동일 플레이북을 순서대로 직접 수행한다(기능 동일, 속도만 차이).

## 충돌·통합
오케스트레이터가 산출물 간 수치·결론 충돌을 출처 신뢰도·증거 태그로 조정하고, 모든 것을 단일 `business-core.yaml`로 수렴시킨다. `verifier`의 역할별 채점은 메인이 `scorecard.md`로 통합한다.
