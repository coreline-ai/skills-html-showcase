---
name: bizplan
description: 공고문과 사업 아이디어를 분석하고, 사용자를 심층 인터뷰한 뒤 시장·기술·경쟁사·특허·논문을 조사하여 정부지원사업·R&D 과제·투자 피치덱·기업/공공 제안서를 설계·작성하는 사업 논리 설계 시스템. 빈칸을 문장으로 채우는 생성기가 아니라 공고 분석 → 심층 인터뷰 → 가설 → 리서치 → 사업 논리 설계 → 공식 서식 매핑 → 초안 → 평가위원 검증의 순서로 작동한다. 산출물 DOCX/HWPX/PDF/PPTX/XLSX/MD. 트리거 — "사업계획서 써줘", "사업계획서 작성", "정부지원사업 지원서", "창업지원 사업계획서", "R&D 계획서", "기술개발 과제 계획서", "투자 피치덱 만들어", "IR 덱", "제안서 작성", "공고문 분석해서 사업계획서", "지원사업 신청서", "사업계획서 검토", "이 공고 분석해줘", "/bizplan".
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, WebSearch, WebFetch, AskUserQuestion, Task
---

# BizPlan Architect — 사업을 질문하고, 근거를 찾고, 논리를 설계한다

> 좋은 사업계획서는 글을 잘 써서 만들어지는 것이 아니다.
> 사업을 깊이 질문하고, 근거를 찾고, 반론을 견딜 수 있도록 논리를 설계했을 때 만들어진다.

이 스킬의 상품은 "문장 채우기"가 아니라 **반론을 견디는 사업 논리**다.
원문·공고 = 재료, 인터뷰·리서치 = 근거, `business-core.yaml` = 설계도, 공식 서식 = 납품 틀, 평가위원 시뮬 = 출고 검사.

**모든 문서는 단 하나의 `business-core.yaml`에서 파생한다.** 같은 사업의 정부지원서·R&D 계획서·투자덱·제안서는 같은 코어를 서로 다른 평가 논리로 변환한 것이다.

사용자가 주는 것: 공고문 URL/파일 + 막연한 사업 아이디어·키워드 (완성된 계획 불필요).
결과물: 프로젝트 폴더(`10-final/`)의 제출용 DOCX/HWPX/PDF/PPTX + 검증 통과 기록 + 제출 체크리스트.

역할 분담 — **기계적 변환(문서 생성·수집·검증 스크립트)은 CLI가, 판단(인터뷰·리서치·사업 논리·문장·서식 매핑)은 클로드가** 한다.

---

## 🚫 7대 절대 규칙 (매 단계 위에 둔다 — 위반 시 산출물 폐기)

1. **AI 임의 창작 금지.** 고객·매출·계약·특허·인증·기술 성능·시장 수치를 만들어내지 않는다. 없으면 `[확인 필요]`로 둔다. (PRD §5.7, §26)
2. **사실/추정/가정/목표 분리.** 모든 수치·주장에 `[사실] [추정] [가정] [목표] [확인 필요]` 태그를 붙인다. (PRD §5.6 — `references/evidence-tagging.md`)
3. **출처 없는 핵심 통계 금지.** 핵심 근거가 되는 수치는 반드시 `source-index.xlsx`에 출처·발행기관·발행일·기준시점·접근일·URL이 기록되어야 한다.
4. **조사와 작성의 분리.** 먼저 리서치 보고서를 완성하고, 그 다음 사업계획서에 쓸 근거를 *선별*한다. 조사 전에 결론을 쓰지 않는다. (PRD §5.3)
5. **인터뷰 우선.** 첫 설명만으로 사업을 단정하지 않는다. 문서 작성 전에 심층 인터뷰를 끝낸다. (PRD §5.1)
6. **특허·논문은 예비 검토.** AI 특허 분석은 법률 의견이 아니다. 침해·무효·권리범위 최종 판단은 변리사 검토 대상으로 표시. 논문 성능은 연구 환경 ≠ 제품 성능으로 구분. (PRD §11.6, §12)
7. **숫자 일관성.** TAM/SAM/SOM·가격·고객수·매출·비용·인력·일정·사업비는 문서 전체에서 동일해야 한다. 코어가 바뀌면 파생 문서를 모두 갱신.

> 이 7개는 PRD §29 "위험요소와 대응"의 코드화다. 슬그머니 어기는 것이 이 스킬 1순위 사고 유형이다.

---

## 🗣️ 사용자 상호작용 규칙 (ABSOLUTE — 위반 시 즉시 교정)

**사용자에게 묻는 모든 질문은 항상 `AskUserQuestion` 도구를 사용한다.** 평문으로 질문을 나열하고 답을 기다리지 않는다. 적용 범위 = 문서 유형 확정, RFP·과제 선택, 심층 인터뷰 문답, 모호어 구체화, 검증 단계 확인, 진행 분기 등 **사용자 입력이 필요한 모든 지점.**

- 서술형 답변이 필요한 인터뷰 질문도 예외 없다 — 대표 보기 2~4개(+자동 제공되는 "Other")를 제시하고, 사용자가 "Other"에 자유 서술하거나 보기를 골라 답하게 한다. 보기는 사용자가 답을 떠올리게 하는 *단서*다.
- 한 번에 최대 3~4문항(인터뷰는 `references/02-interview-engine.md` 규칙대로 3문항). 답변을 받은 즉시 transcript·산출물에 기록하고, 모호하면 다음 `AskUserQuestion` 묶음으로 구체화한다.
- 예외는 단 하나 — 사용자가 "직접 길게 서술하겠다"고 자청한 경우. 그 답변만 대화로 받는다(도구 강제는 *질문을 던지는 쪽*에 적용).

---

## 🚦 발동 시 첫 행동

1. **스킬 루트 확인.** CLI는 스킬 루트(전역 설치 시 심볼릭 링크 `~/.claude/skills/bizplan/`)에서 실행한다.
   파이썬 의존성 확인: `python3 ~/.claude/skills/bizplan/scripts/doctor.py` — 없는 패키지(python-docx/openpyxl/python-pptx)와 도구(soffice)를 보고. HWPX/PPTX node 스크립트는 스킬 루트에서 `npm install` 1회.
2. **작업 디렉토리.** 프로젝트 폴더는 **스킬 폴더 내 `dist/bizplan-<slug>/`** 에 만든다(기본). `new_project.py`는 `--dir` 없이 호출하면 자동으로 스킬 `dist/`에 생성한다. (사용자가 특정 위치를 원하면 `--dir`로 지정.)
3. **문서 유형 게이트 (BLOCKING — 가장 중요한 분기).** 어떤 종류의 문서인지 먼저 확정한다. 평가 논리가 완전히 다르다.

   | 유형 | 핵심 평가 논리 | 가중 중점 |
   |---|---|---|
   | 정부 창업/중소기업 지원사업 | 문제인식·실현가능성·성장전략·팀·정책부합 | 사업성 15 / 균형 |
   | R&D 기술개발·산학협력 과제 | 기술난제·정량목표·검증계획·특허·논문·사업화 | 기술성·특허논문 근거 |
   | 투자용 피치덱 | 큰 문제·왜 지금·시장규모·성장지표·경쟁우위·팀 | 시장성·트랙션 |
   | 기업·공공기관 제안서 | 고객문제·제안범위·수행방법·역할·일정·실적 | 수행능력·신뢰 |
   | 내부 신사업/자유형식 | 위 중 사용자가 지정 | 지정 |

   판단이 애매하면 `AskUserQuestion`으로 1회 확정한다. 유형별 변환 규칙은 `references/11-document-types.md`.
4. **공고 유무 확인.** 공고(URL/파일)가 있으면 Gate 0부터, 없으면(투자덱·내부 신사업 등) Gate 1(인터뷰)부터 시작한다.

---

## 프로젝트 스캐폴딩 (모든 산출물의 집)

새 프로젝트는 PRD §22 구조를 그대로 만든다. 한 번에:

```bash
# --dir 생략 시 스킬 폴더 내 dist/ 에 자동 생성 (기본)
python3 ~/.claude/skills/bizplan/scripts/new_project.py \
  --slug "<영문-slug>" \
  --name "<프로젝트명>" --type "<문서유형>" --org "<신청기관>" --deadline "<YYYY-MM-DD>"
# → dist/bizplan-<slug>/ 생성
```

생성되는 폴더(= 단계별 산출물 위치, 이 매핑이 **단일 출처**다):

```text
dist/bizplan-<slug>/
├── project.json              # 프로젝트 메타 + 진행 상태(status, gates_passed)
├── 00-source/                # notice/ attachments/ templates/ company/ user-files/
├── 01-notice-analysis/       # notice-summary.md eligibility-check.md evaluation-criteria.md
│                             # required-documents.md budget-rules.md schedule.md
│                             # format-constraints.md disqualification-risks.md notice-analysis.docx
├── 02-interview/             # idea-brief.md keyword-map.yaml initial-hypotheses.md missing-information.md
│                             # interview-transcript.md interview-summary.md founder-insight.md
│                             # confirmed-facts.md assumptions.md contradictions.md follow-up-items.md
├── 03-idea-and-title/        # title-candidates.md  research-plan.md
├── 04-research/
│   ├── market/  competitors/  technology/
│   ├── patents/              # patent-landscape.docx patent-list.xlsx patent-family-map.md
│   │                         # claim-chart.xlsx preliminary-fto-report.docx patent-risk-map.md patent-opportunity.md
│   ├── papers/               # paper-review-report.docx paper-evidence-table.xlsx technology-trend-map.md
│   │                         # benchmark-comparison.xlsx research-gap-analysis.md technology-readiness.md
│   ├── research-report.md / .docx
│   └── source-index.xlsx
├── 05-business-core/         # business-core.yaml evidence-ledger.xlsx market-sizing.xlsx financial-model.xlsx
├── 06-template-design/       # template-structure.yaml template-map.yaml section-outline.md
│                             # section-evidence-map.md section-visual-map.md
├── 07-diagrams/              # diagram-source/  images/
├── 08-draft/                 # section별 *.md  +  business-plan-draft.docx
├── 09-audit/                 # evaluator-*.md  scorecard.md  revision-log.md
└── 10-final/                 # final-business-plan.{docx,hwpx,pdf,html}  pitch-deck.{pptx,html}
                              # executive-summary.docx  submission-checklist.md
```

`project.json`의 `status`와 `gates_passed[]`로 재개 지점을 추적한다. 실패한 단계부터 다시 실행하고 처음부터 재생성하지 않는다 (PRD §26 성능·재현성).

---

## 21단계 워크플로우 — 7개 게이트로 묶음

각 단계는 산출물을 먼저 쓰고(증분 저장), 게이트를 통과해야 다음으로 간다. 상세 프로토콜은 `references/`에 있으니 **해당 단계 진입 시 반드시 Read**한다.

### Gate 0 — 공고와 자료 수집  · `references/01-notice-analysis.md`
1. 공고 URL/파일 접수 → `00-source/notice/`에 본문 저장, 첨부 링크 탐색·다운로드(PDF/HWP/HWPX/DOCX/XLSX/ZIP), ZIP 해제·분류, 최신/구버전 구분, **다운로드 실패 목록 명시**.
   - 헬퍼: `scripts/fetch_notice.py <url> --out 00-source/`. 로그인 필요·유료 자료는 우회하지 않고 사용자에게 요청.
2. 공고 분석 → `01-notice-analysis/`의 8개 산출물. 평가항목·배점, 자격, 사업비 기준, 서식·분량 제한, 제외·중복 제한, 일정, 의무성과를 추출.
   - **통과 조건**: 공고 본문 확보, 필수 첨부 확보(또는 누락 보고), 평가 배점표 작성, 서식 제약 확보.

### Gate 1 — 사업 아이디어 + 심층 인터뷰  · `references/02-interview-engine.md`, `references/03-title-design.md`
3. 아이디어 접수 → `02-interview/idea-brief.md`, `keyword-map.yaml`, `initial-hypotheses.md`, `missing-information.md`. 키워드를 12개 영역(고객/사용자/문제/제품/기술/산업/시장/정책/경쟁/사업모델/성과/위험)으로 확장.
4. **과제명 가설 질문**(인터뷰 초기) → 사용자 제목을 최초 가설로 `03-idea-and-title/title-candidates.md`에 저장.
5. **적응형 심층 인터뷰** — 고정 설문 일괄 제시 금지. 한 번에 **최대 3문항**. 10단계(동기→고객→현재방식→제품/기술→구현→시장/모델→경쟁→팀→성과→비전)를 답변에 따라 적응적으로. 모호어("많은 고객/효율적/혁신적/AI 활용/글로벌")는 즉시 수치·사례로 구체화 요청.
   - 인터뷰는 **항상 `AskUserQuestion` 도구로 진행**(§🗣️ 사용자 상호작용 규칙 — 서술형도 보기+Other 제시)하고 `interview-transcript.md`에 기록. 종료 시 `interview-summary.md`·`founder-insight.md`·`confirmed-facts.md`·`assumptions.md`·`contradictions.md`·`follow-up-items.md` 작성.
   - **통과 조건**: 핵심 13항목(§8.5)이 구체화되었거나 `[확인 필요]`로 분류됨. 모호어 잔존 0.

### Gate 2 — 리서치 (조사와 작성 분리)  · `references/04-research-engine.md`, `05-patent-analysis.md`, `06-paper-analysis.md`
6. **조사 계획** → `03-idea-and-title/research-plan.md` (목적·핵심질문·키워드·한영 동의어·대상국가·기간·우선출처·필요수치·검증할 가설).
7. 시장·산업·경쟁·기술 조사 → `04-research/market/`, `competitors/`, `technology/`. **모든 자료를 즉시 `source-index.xlsx`에 등재**(출처 10단계 우선순위, 기준일·접근일·신뢰도·반영위치). **부정적 근거·실패사례·경쟁 강점도 의무 수집**(출처 편향 방지).
8. 특허 권리 분석 → `04-research/patents/` 7산출물. 독립 청구항 요소 분해 → 사용자 제품과 claim-chart 비교 → 위험 분류 → 회피 가능성 → 권리화 기회 → 변리사 검토 대상 표시.
9. 논문·연구 동향 분석 → `04-research/papers/` 6산출물. 방법론·데이터·지표·재현성·TRL·연구공백. 조건 다른 벤치마크 단순 비교 금지, 프리프린트 ≠ 동료평가 구분.
10. **종합 리서치 보고서** → `04-research/research-report.md`(+`.docx`). PRD §13.2의 21개 목차, 각 섹션은 `결론→근거→표/그래프→해석→사업영향→반영위치` 형식.
    - **대량 리서치는 서브에이전트 병렬 dispatch** (아래 §병렬 리서치). 통과 조건: 국내외 시장·경쟁·특허·논문 조사 완료, 부정적 근거 포함, 모든 핵심 수치 출처 기록.

### Gate 3·4 — 사업 코어 + 숫자 확정  · `references/07-business-core.md`, `references/13-financial-models.md`
11. **Business Core 확정** → `05-business-core/business-core.yaml` (PRD §14 전체 스키마). 인터뷰 확정사실 + 리서치 선별근거를 결합. 모든 항목 값에 evidence 태그.
12. **수치 모델은 엑셀 수식으로 계산**(손계산 금지) → `evidence-ledger.xlsx`(Claim ↔ 출처 ↔ 섹션), `market-sizing.xlsx`(TAM/SAM/SOM `=고객수*단가*빈도`), `financial-model.xlsx`(5개년 추정손익·사업비 명세·단위경제성). 입력 셀만 가정값(태그·출처), 합계·비율은 전부 `=` 수식. **재무표 5종 설계·수식·spec 예시는 `references/13-financial-models.md`**.
    - **Gate 3 통과**: 문제→해결책→제품→기술→시장→수익모델→실행→예산 논리 사슬에 단절 없음.
    - **Gate 4 통과**: 위 모든 수치가 코어·엑셀·문서에서 동일. 불일치 0. (엑셀 수식이라 검산 가능)

### Gate 6 (서식) 준비 — 공식 서식 매핑 + 표/다이어그램  · `references/08-template-mapping.md`, `09-diagrams.md`, `13-financial-models.md`
13. **양식 충실 추종(최우선).** 공고가 양식(.hwp/.docx)을 제공하면 **목차·항목번호·표 구조를 글자 그대로** 따른다(임의 재구성 금지). 양식 없을 때만 표준 골격(창업=PSST 4항목+요약표 2개 / R&D=7항목+평가기준표). → `06-template-design/template-structure.yaml`.
14. 서식 매핑 → `template-map.yaml`(공식항목 ↔ core 경로 ↔ 근거 ↔ 표현), `section-outline.md`, `section-evidence-map.md`, `section-visual-map.md`. **필수 표/도표 11종**(추진일정 간트·사업비 명세·성과지표·추진체계도·연구팀편성·시장규모 등)을 빠짐없이 배치.
15. 표·다이어그램 제작:
    - **금액·수치 표**(시장규모·재무·사업비·성과지표·단위경제성) → `build_xlsx.py`(수식) → `xlsx_to_image.sh`로 PNG 캡쳐 → 본문 삽입. (`13-financial-models.md`)
    - **개념 다이어그램**(문제구조·아키텍처·추진체계·로드맵) → `diagram-source/`(.mmd 보존) → HTML은 ```mermaid 자동 렌더 / DOCX·HWPX용은 PNG. 한 그림 한 메시지, 노드 5~9, 흑백 식별.

### Draft — 초안 작성 (디테일·분량 충실)  · `references/10-drafting.md`, `11-document-types.md`
16. 목차별 초안 → `08-draft/<section>.md`. 섹션마다 `평가자 질문 → 한 문장 답 → 근거(출처 1:1) → 표/그래프/도식 → 상세 → 다음 연결 → 출처/수치 확인` 순.
    - **디테일 원칙**: 주장마다 근거 1:1, 추상어→정량 수치, 측정기준·출처·조회일 명시. 경쟁분석은 "측정기준+근거" 컬럼 비교표+포지셔닝맵. **정량목표=활동→결과→숫자+조건/측정/시기+세계최고수준 비교** / 정성목표=측정가능 상태변화.
    - **분량**: 공고 페이지 제한 준수가 1순위(초과=감점), 제한 내에서 표·도식으로 밀도를 높여 디테일 확보. filler·빈 섹션 금지.
17. 유형별 변환 적용(§발동 3번 표) → `business-plan-draft.docx` 통합.

### Gate 5·7 — 검증·반복 + 평가위원 시뮬  · `references/12-verification.md`
18. **평가위원 4역할 시뮬레이션** → `09-audit/evaluator-admin.md`(행정·서식), `evaluator-tech.md`(기술·산업), `evaluator-biz.md`(사업성), `evaluator-skeptic.md`(회의적 반대). 각자 PRD §20 배점표로 채점 → `scorecard.md`.
19. 오류·약점 수정 → `revision-log.md`에 기록하며 반복. 자동 검증: `scripts/validate_project.py bizplan-<slug>/`.
    - **통과 기준**: 전체 ≥85점, 개별영역 70% 미만 0, 중대 사실오류 0, 출처 없는 핵심통계 0, 숫자 불일치 0.

### Final — 출력 + 제출  · `references/document-output.md`
20. 최종 파일 생성 → `10-final/`. `final-business-plan.{docx,hwpx,pdf,html}`, `pitch-deck.{pptx,html}`(투자덱), `executive-summary.docx`.
    - **⚠️ 다이어그램 PNG 사전렌더 (DOCX/HWPX/PDF 필수)**: 초안 md 의 ```mermaid 는 HTML 만 자동렌더되고 DOCX/PDF 에선 깨진다. **변환 전 `scripts/prerender_mermaid.py`로 PNG 치환한 `*.render.md` 를 만들어** DOCX/HWPX/PDF 변환에 쓴다. (`references/10-drafting.md §11.6`)
    - DOCX: `scripts/md_to_docx.py <render.md>`. HWPX: `scripts/build_hwpx.mts <render.md>`(kordoc). PDF: `scripts/to_pdf.sh`(soffice). PPTX: `scripts/build_pptx.mts`. XLSX: `scripts/build_xlsx.py`.
    - **HTML(항상 생성)**: 사업계획서 본문 → `scripts/md_to_html.py 08-draft/business-plan-draft.md 10-final/final-business-plan.html --base-dir 07-diagrams/images`(다이어그램 base64 임베드, 단일 파일). 투자덱 → `scripts/build_html_deck.py <deck.json> 10-final/pitch-deck.html`. 의존성이 없어 검토·공유·웹 미리보기·인쇄에 가장 안전한 기본 산출물이므로 **유형과 무관하게 본문 HTML은 항상 만든다**.
    - **출력 후 렌더링 검사**(표 깨짐·공란) 후 완료. 깨지면 `format-damage-report.md` 생성. HTML은 브라우저로 바로 열어 검사할 수 있어 1차 픽셀 검수에 활용한다.
21. 제출 체크리스트 → `10-final/submission-checklist.md`. PRD §30 완료기준 14항목 전수 확인 + 필수서류·서명·분량·서식 최종 점검.

---

## 병렬 리서치 — 서브에이전트 dispatch (PRD §23 에이전트 구성)

리서치(Gate 2)와 평가위원 시뮬(Gate 7)은 독립적이므로 `Task` 도구로 병렬화한다. 에이전트 역할 정의는 `agents/`에 있고, 각 에이전트는 **자기 영역만 조사해 구조화 산출물(md/xlsx 행)로 반환**한다.

- 메인은 오케스트레이터(`agents/orchestrator.md`)다. 직접 조사하지 말고 분배·통합·충돌조정만.
- 단일 메시지에 여러 `Task` 호출 → 동시 실행: `market-researcher`, `competitor-analyst`, `patent-analyst`, `paper-analyst`, `business-analyst`.
- 각 서브에이전트에게 **반드시 전달**: ① `business-core.yaml`(현재본) + `research-plan.md` 경로 ② 출처 우선순위·증거 태그 규칙 ③ 산출 파일 경로 ④ 7대 절대 규칙. (서브에이전트는 컨텍스트를 공유하지 않으므로 명시 필수.)
- 검증(Gate 7)도 4역할을 병렬 dispatch → 메인이 scorecard 통합.

서브에이전트가 없는 환경이면 메인이 순차 진행한다(기능 동일, 속도만 차이).

---

## 문서 생성 빠른 참조

| 포맷 | 도구 | 명령 | 비고 |
|---|---|---|---|
| DOCX | python-docx | `python3 scripts/md_to_docx.py <in.md> <out.docx> [--template ...]` | 표·헤딩·이미지 |
| **HTML(문서)** | **순수 python** | `python3 scripts/md_to_html.py <in.md> <out.html> [--subtitle ... --meta ...]` | **자립형·증거태그 배지·목차·인쇄·이미지 임베드 + ```mermaid 블록 자동 렌더 (의존성 0)** |
| **HTML(덱)** | **순수 python** | `python3 scripts/build_html_deck.py <deck.json> <out.html>` | **deck.json 그대로 16:9 슬라이드·키보드 네비 (의존성 0)** |
| XLSX | openpyxl | `python3 scripts/build_xlsx.py <spec.yaml> <out.xlsx>` | source-index/claim-chart/재무모델. **`=` 수식 셀 지원**(soffice가 계산), landscape·fit-to-page 인쇄설정 자동 |
| **XLSX→이미지** | **soffice+poppler** | `bash scripts/xlsx_to_image.sh <in.xlsx> <out_prefix> [DPI]` | **수식 표 → 시트별 PNG(`-1.png`…). 본문 삽입용. → `references/13-financial-models.md`** |
| PDF | LibreOffice | `bash scripts/to_pdf.sh <in.docx\|pptx> <outdir>` | soffice headless |
| HWPX | kordoc(node) | `npx tsx scripts/build_hwpx.mts <in.md> <out.hwpx>` | 한국 정부서식 |
| PPTX | pptxgenjs(node) | `npx tsx scripts/build_pptx.mts <deck.json> <out.pptx>` | 피치덱 |
| 다이어그램(개별) | mermaid/dot | `bash scripts/render_diagram.sh <src> <out.png>` | .mmd/.dot 단건 PNG 렌더 |
| **다이어그램(일괄)** | **mmdc** | `python3 scripts/prerender_mermaid.py <in.md> <out.render.md> --img-dir 07-diagrams/images --src-dir 07-diagrams/diagram-source --prefix fig` | **md 의 ```mermaid 전부 → PNG 치환. DOCX/HWPX/PDF 변환 전 필수**(HTML은 원본 md 자동렌더) |
| **HWPX 읽기** | **순수 python** | `python3 scripts/hwpx_to_text.py <in.hwpx> [out.txt]` | **공고·첨부 HWPX → 텍스트(분석용, 의존성 0). .hwp 구버전 미지원** |

HTML 2종은 **의존성이 전혀 없어 어떤 환경에서도 즉시 동작**한다(공유·웹 미리보기·인쇄용). 같은 `business-plan-draft.md`·`deck.json`에서 DOCX/HWPX·PPTX와 나란히 나오므로 단일 출처가 유지된다. **다이어그램은 초안 md에 ```mermaid 코드블록으로 넣으면 HTML 산출물에서 자동 렌더**(PNG 불필요); DOCX/HWPX용 PNG가 필요하면 `render_diagram.sh`(mmdc/dot).

상세·옵션·트러블슈팅은 `references/document-output.md`. node 스크립트 첫 실행 전 스킬 루트에서 `npm install`.

---

## 마인드셋

> "이 주장은 회의적인 반대 평가자의 질문을 견디는가?"
> "이 수치의 출처는 source-index 몇 번 행인가?"
> "이건 [사실]인가 [목표]인가?"
>
> **schema 통과는 이정표가 아니라 출발점이다.** 모든 문서는 하나의 코어에서 나오고, 모든 수치는 하나의 출처를 가진다.
> AI가 대신 꾸며주는 도구가 아니라, 사용자의 현장 경험·기술·시장 증거·특허·논문·실행계획을 연결해 **지원하거나 투자할 이유가 보이는 사업**으로 만드는 시스템이다.
