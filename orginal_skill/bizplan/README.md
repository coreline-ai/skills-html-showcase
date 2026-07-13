# BizPlan Architect (`/bizplan`)

공고문과 막연한 사업 아이디어에서 출발해, **심층 인터뷰 → 시장·기술·경쟁·특허·논문 리서치 → 사업 논리 설계 → 공식 서식 매핑 → 초안 → 평가위원 검증**의 순서로 정부지원사업·R&D 과제·투자 피치덱·기업/공공 제안서를 작성하는 Claude Code 스킬.

빈칸을 문장으로 채우는 생성기가 아니라, **반론을 견디는 사업 논리**를 설계하는 시스템이다. 모든 문서는 단 하나의 `business-core.yaml`에서 파생하고, 모든 핵심 수치는 `source-index.xlsx`의 출처를 가진다.

## 사용법

```
/bizplan
```
또는 "이 공고 분석해서 사업계획서 써줘", "R&D 계획서 작성", "투자 피치덱 만들어" 등으로 호출.

사용자가 주는 것: 공고 URL/파일 + 키워드 수준의 아이디어 (완성된 계획 불필요).
받는 것: 프로젝트 폴더 `10-final/`의 제출용 DOCX/HWPX/PDF/PPTX + 검증 통과 기록 + 제출 체크리스트.

## 7대 절대 규칙

1. AI 임의 창작 금지 (고객·매출·특허·성능을 만들지 않음, 없으면 `[확인 필요]`)
2. 사실/추정/가정/목표 분리 (`[사실][추정][가정][목표][확인 필요]` 태그)
3. 출처 없는 핵심 통계 금지 (`source-index.xlsx` 등재)
4. 조사와 작성의 분리 (리서치 완료 후 근거 선별)
5. 인터뷰 우선 (작성 전 심층 인터뷰)
6. 특허·논문은 예비 검토 (법률 의견 아님 / 논문 성능 ≠ 제품 성능)
7. 숫자 일관성 (코어가 바뀌면 모든 파생 문서 갱신)

## 구조

| 경로 | 내용 |
|---|---|
| `SKILL.md` | 메인 플레이북 — 21단계 / 7게이트 / 산출물 파일명 규약 / 7대 절대 규칙 |
| `PRD.md` | 제품 요구사항 정의서 (단일 참조 원천) |
| `references/01~12 + evidence-tagging + document-output` | 단계별 상세 실행 프로토콜 |
| `templates/business-core.yaml` | 모든 문서가 파생하는 사업 코어 스키마 |
| `agents/` | 12개 서브에이전트 역할 플레이북 (리서치·검증 병렬 dispatch용) |
| `scripts/` | 문서 생성·수집·검증 도구 |

## 의존성

```bash
python3 ~/.claude/skills/bizplan/scripts/doctor.py   # 의존성 점검
```

- **필수**: `python-docx`, `openpyxl`, `PyYAML` (DOCX/XLSX/MD)
- **PDF**: LibreOffice (`soffice`)
- **HWPX/PPTX**: Node.js ≥20 + 스킬 루트에서 `npm install` (kordoc, pptxgenjs)
- **다이어그램(선택)**: `mmdc`(mermaid-cli), `dot`(graphviz)

## 산출물 포맷

MD · **HTML** · DOCX · HWPX · PDF · PPTX · XLSX — 7포맷 전부 검증됨.

- **HTML 2종은 의존성이 전혀 없다**(순수 python). `md_to_html.py`(사업계획서 본문 → 증거태그 배지·자동 목차·인쇄, 단일 파일), `build_html_deck.py`(deck.json → 16:9 슬라이드). 공유·웹 미리보기·1차 검수에 가장 안전한 기본 산출물이라 유형과 무관하게 항상 생성된다.

## 설치 (전역 심링크)

```bash
ln -s /Users/futurewave/Documents/dev/vibelabs-skills/bizplan ~/.claude/skills/bizplan
```
