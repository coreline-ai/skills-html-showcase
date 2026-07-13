# 문서 생성 사용 가이드 (document-output)

> SKILL.md 단계 20(Final 출력) 진입 시 Read한다.
> 모든 산출물은 `bizplan-<slug>/10-final/`(또는 해당 단계 폴더)에 만든다.
> 기계적 변환은 CLI가, 판단(서식 매핑·문장)은 클로드가 한다.

핵심 원칙은 PRD §29의 마지막 줄이다:
**"출력 후 렌더링 검사(표 깨짐·공란)를 하고 나서 완료한다. 깨지면 `format-damage-report.md`를 만든다."**
schema/스크립트가 0으로 끝났다고 끝난 것이 아니다. 실제 파일을 열어(또는 PDF로 변환해) 표·그림·공란을 눈으로 확인해야 완료다.

---

## 0. 발동 전 — 의존성 점검

문서 생성 전 한 번:

```bash
python3 ~/.claude/skills/bizplan/scripts/doctor.py
```

- DOCX / XLSX / MD: `python-docx` · `openpyxl` · `PyYAML` 만 있으면 가능.
- PDF: `soffice`(LibreOffice) 필요.
- HWPX / PPTX(node): 스킬 루트에서 `npm install` 1회.
- 다이어그램(선택): `mmdc`(mermaid-cli) 또는 `dot`(Graphviz).

설치 명령은 doctor.py 가 누락 항목별로 출력한다.

```bash
# 파이썬 패키지
pip3 install python-docx openpyxl pyyaml
# PDF (macOS)
brew install --cask libreoffice
# 다이어그램 (선택)
npm i -g @mermaid-js/mermaid-cli      # mmdc
brew install graphviz                  # dot
# HWPX/PPTX node 스크립트 (스킬 루트에서 1회)
cd ~/.claude/skills/bizplan && npm install
```

---

## 1. 포맷별 명령·옵션 표

| 포맷 | 도구 | 명령 | 주요 옵션 | 비고 |
|---|---|---|---|---|
| DOCX | python-docx | `python3 scripts/md_to_docx.py <in.md> <out.docx>` | `--title "제목"` `--subtitle "부제"` | MD→DOCX, 표·헤딩·이미지·코드·인용 |
| HTML(문서) | 순수 python | `python3 scripts/md_to_html.py <in.md> <out.html>` | `--subtitle` `--meta` `--kicker` `--base-dir` `--no-embed` `--no-toc` `--no-legend` | MD→자립형 HTML, 증거태그 배지·자동 목차·인쇄·이미지 base64 (의존성 0) |
| HTML(덱) | 순수 python | `python3 scripts/build_html_deck.py <deck.json> <out.html>` | `--base-dir` `--no-embed` | deck.json→16:9 슬라이드, 키보드 네비·풀스크린·인쇄 (의존성 0) |
| XLSX(spec) | openpyxl | `python3 scripts/build_xlsx.py <spec.yaml\|json> <out.xlsx>` | — | 다중 시트, 헤더 스타일·필터·고정 |
| XLSX(프리셋) | openpyxl | `python3 scripts/build_xlsx.py --preset <name> <out.xlsx>` | `--preset source-index\|claim-chart\|evidence-ledger` | 빈 템플릿(헤더만) |
| PDF | LibreOffice | `bash scripts/to_pdf.sh <input> <outdir>` | — | DOCX/PPTX/XLSX→PDF, 임시 프로파일 |
| 다이어그램 | mermaid/dot | `bash scripts/render_diagram.sh <src> <out.png\|svg>` | — | .mmd→mmdc / .dot·.gv→dot |
| HWPX | kordoc(node) | `npx tsx scripts/build_hwpx.mts <in.md> <out.hwpx>` | — | 한국 정부서식 (node, npm install) |
| PPTX | pptxgenjs(node) | `npx tsx scripts/build_pptx.mts <deck.json> <out.pptx>` | — | 투자 피치덱 (node, npm install) |
| 검증 | python | `python3 scripts/validate_project.py <bizplan-slug 디렉토리>` | — | 게이트별 ✓/✗/⚠ 진단(비차단) |

> **HTML 2종은 의존성이 전혀 없다**(LibreOffice·node 불필요). 어떤 환경에서도 즉시 열리므로 검토·공유·웹 미리보기·인쇄의 기본 산출물이다. 같은 `business-plan-draft.md`(문서)·`deck.json`(덱)에서 DOCX/HWPX·PPTX와 나란히 나오므로 단일 출처가 유지된다.

---

## 2. md_to_docx.py — Markdown → DOCX

python-docx 만 사용하는 자체 라인 파서. 마크다운 라이브러리 의존 없음.

지원 문법:
- ATX 헤딩 `#`~`######`
- 단락(연속 줄 병합), 굵게 `**...**`, 기울임 `*...*`, 인라인코드 `` `...` ``, 링크 `[text](url)`
- 순서/비순서 목록(들여쓰기 중첩)
- GFM 파이프 표 — `|---|` 구분선 인식, 첫 행 굵게, 'Table Grid' 스타일
- 코드블록(```), 인용(`>`), 수평선(`---`)
- 이미지 `![alt](path)` — 상대경로는 **md 파일 기준**으로 해석. 파일이 있으면 삽입, 없으면 경고 후 `[이미지: alt]` 텍스트로 대체

한글 폰트(맑은 고딕/Malgun Gothic)를 본문·헤딩·표에 적용한다. 폰트가 없는 환경에서도 오류 없이 기본 글꼴로 진행한다.

```bash
python3 scripts/md_to_docx.py 04-research/research-report.md \
  04-research/research-report.docx --title "리서치 보고서" --subtitle "스마트팜 사업"
```

견고성: 인라인/표 파싱이 실패해도 죽지 않고 해당 줄을 일반 단락(또는 텍스트 강등)으로 처리한다. 변환 후 경고 건수를 출력하므로, 경고가 있으면 해당 부분을 DOCX/PDF로 확인한다.

---

## 3. build_xlsx.py — YAML/JSON spec → XLSX

### 3.1 spec 으로 시트 구성

```yaml
# market-sizing.yaml
sheets:
  - name: "TAM-SAM-SOM"
    freeze_header: true
    columns: ["구분", "정의", "산식", "값(원)", "출처ID"]
    widths: [10, 30, 40, 16, 10]
    rows:
      - ["TAM", "전체 시장", "사업체수 × ARPU", 1200000000000, "S001"]
      - ["SAM", "유효 시장", "TAM × 도달가능비율", 360000000000, "S002"]
      - ["SOM", "수익 시장(3년)", "SAM × 목표점유율", 18000000000, "S003"]
```

```bash
python3 scripts/build_xlsx.py market-sizing.yaml 05-business-core/market-sizing.xlsx
```

- 헤더: 굵게 + 파란 배경 + 흰 글자 + 자동 필터 + 첫 행 고정.
- 숫자/날짜는 셀 타입 보존(정수·실수·`YYYY-MM-DD`), 긴 텍스트는 줄바꿈(wrap).
- 열 너비는 `widths` 지정 또는 내용 기반 자동(상한 60).
- 최상위가 list 면 시트 리스트로, dict + `columns` 면 단일 시트로 해석한다.
- spec 은 `.yaml` 또는 `.json` 모두 가능.

### 3.2 프리셋(빈 템플릿) — spec 없이

표준 표 산출물의 헤더만 만든 다음, 클로드가 행을 채워 다시 spec 으로 재생성하거나 직접 입력한다.

```bash
python3 scripts/build_xlsx.py --preset source-index   04-research/source-index.xlsx
python3 scripts/build_xlsx.py --preset claim-chart     04-research/patents/claim-chart.xlsx
python3 scripts/build_xlsx.py --preset evidence-ledger 05-business-core/evidence-ledger.xlsx
```

프리셋 컬럼(규약 일치):

| 프리셋 | 컬럼 | 입력 가이드 |
|---|---|---|
| `source-index` | id / 제목 / 발행기관 / 저자 / 발행일 / 기준시점 / 접근일 / URL / 사용가능주장 / 신뢰도 / 반영위치 / stance / priority_rank | 신뢰도=상·중·하 · stance=우호·중립·부정·반대 · priority_rank=1~10 |
| `claim-chart` | 청구항요소 / 사용자제품 / 일치여부 / 비고 / 위험도 | 일치여부=일치·부분일치·불일치 · 위험도=상·중·하(변리사 검토 표시) |
| `evidence-ledger` | claim_text / claim_type / source / confidence / target_section / verification_status | claim_type=사실·추정·가정·목표·확인필요 · confidence=상·중·하 |

A1 셀에 입력 가이드가 셀 주석으로 들어간다.

---

## 4. to_pdf.sh — DOCX/PPTX/XLSX → PDF

```bash
bash scripts/to_pdf.sh 10-final/final-business-plan.docx 10-final/
# → 마지막 줄에 생성된 PDF 경로 출력: 10-final/final-business-plan.pdf
```

- `soffice --headless --convert-to pdf --outdir <outdir>` 사용.
- 동시 실행(병렬 변환) 충돌 방지를 위해 매 실행 임시 프로파일(`-env:UserInstallation`)을 만들고 종료 시 정리한다.
- `soffice` 가 없으면 명확한 오류 + 설치 안내 후 종료(rc=1). macOS 앱 번들 경로(`/Applications/LibreOffice.app/...`)도 fallback 으로 탐색.

---

## 5. render_diagram.sh — 다이어그램 원본 → PNG/SVG

```bash
bash scripts/render_diagram.sh 07-diagrams/diagram-source/flow.mmd 07-diagrams/images/flow.png
bash scripts/render_diagram.sh 07-diagrams/diagram-source/arch.dot 07-diagrams/images/arch.svg
```

- 입력 확장자로 도구 자동 판단: `.mmd`→`mmdc`(mermaid-cli), `.dot`/`.gv`→`dot`(Graphviz).
- 출력 확장자 `.png`/`.svg` 로 포맷 결정.
- **도구가 없으면 설치 안내를 출력하고 비차단 종료(exit 0).** 다이어그램은 선택 산출물이라 파이프라인을 멈추지 않는다. 대신 원본(.mmd/.dot)은 `07-diagrams/diagram-source/`에 항상 보존한다.

---

## 6. HWPX / PPTX (node — 다른 에이전트 담당)

이 두 포맷은 node 스크립트로 만든다. 첫 실행 전 스킬 루트에서 `npm install`.

```bash
cd ~/.claude/skills/bizplan && npm install   # 1회
# HWPX (kordoc) — 한국 정부서식
npx tsx scripts/build_hwpx.mts 08-draft/final.md 10-final/final-business-plan.hwpx
# PPTX (pptxgenjs) — 투자 피치덱
npx tsx scripts/build_pptx.mts data/deck.json 10-final/pitch-deck.pptx
```

(`build_hwpx.mts` / `build_pptx.mts` 의 구현·deck.json 스키마는 별도 가이드 참조.)

---

## 6b. HTML 2종 — 자립형 웹 산출물 (의존성 0, 순수 python)

LibreOffice·node 없이 표준 라이브러리만으로 동작한다. 산출물은 **단일 HTML 파일**(이미지 base64 임베드)이라 메일·메신저로 그대로 공유되고, 브라우저로 즉시 열려 1차 검수에도 쓰인다. 두 스크립트는 사업계획서/덱과 **같은 소스**(`business-plan-draft.md`, `deck.json`)를 입력으로 받아 단일 출처를 유지한다.

### md_to_html.py — 사업계획서/보고서 본문 → HTML
```bash
python3 scripts/md_to_html.py 08-draft/business-plan-draft.md 10-final/final-business-plan.html \
  --subtitle "중소벤처기업부 창업도약패키지 제출용" --meta "2026-06-17 · ㈜회사명" \
  --base-dir 07-diagrams/images          # MD의 ![](...) 다이어그램을 base64로 임베드
```
- **증거 태그 배지**: 본문의 `[사실] [추정] [가정] [목표] [확인 필요]` 를 색상 배지로 시각화(7대 절대 규칙 #2). 상단에 범례 자동 삽입(`--no-legend` 로 끔).
- 헤딩(h2/h3) 기반 **자동 목차** 사이드바(모바일 접힘), GFM 표·중첩 목록·인용·코드·링크 지원, `@media print` 인쇄 스타일.
- 옵션: `--no-embed`(이미지 상대경로 유지) · `--no-toc` · `--kicker "R&D 과제"`(상단 라벨). 제목 미지정 시 첫 H1 자동 사용.
- 리서치 보고서(`04-research/research-report.md`)·임원 요약도 같은 명령으로 HTML 미리보기 생성 가능.

### build_html_deck.py — deck.json → 16:9 슬라이드 HTML
```bash
python3 scripts/build_html_deck.py data/deck.json 10-final/pitch-deck.html
```
- `build_pptx.mts` 와 **동일한 deck.json 스키마**(layout 9종·테마 navy/slate/forest/plum). PPTX와 HTML 덱이 한 소스에서 나온다.
- 키보드 네비게이션(← → Space / Home End), `F` 풀스크린, 슬라이드 번호, `@media print` 슬라이드별 페이지. 이미지 base64 임베드.

---

## 7. 표준 워크플로우

```text
MD 초안(08-draft/*.md)
   │  md_to_docx.py
   ▼
DOCX(business-plan-draft.docx / final-business-plan.docx)
   │  to_pdf.sh
   ▼
PDF(검토·제출용)

코어 데이터(business-core.yaml 파생)
   │  build_xlsx.py (spec 또는 preset)
   ▼
XLSX(source-index / claim-chart / evidence-ledger / market-sizing / financial-model)

다이어그램 (초안 md 의 ```mermaid 블록)
   │  ① HTML: 원본 md → md_to_html (mermaid 자동 렌더)
   │  ② DOCX/HWPX/PDF: prerender_mermaid.py 로 PNG 치환한 render.md → 변환  ★필수
   ▼
PNG(07-diagrams/images/fig-NN.png)  →  render.md 에 ![](png) → DOCX/PDF 에 그림 포함

# ⚠️ DOCX/HWPX/PDF 는 반드시 prerender 후 변환 (코드블록 그대로면 다이어그램 깨짐 — 2026-06-18)
python3 scripts/prerender_mermaid.py 08-draft/business-plan-draft.md \
  08-draft/business-plan-draft.render.md \
  --img-dir 07-diagrams/images --src-dir 07-diagrams/diagram-source --prefix fig

투자덱 데이터(deck.json) → build_pptx.mts → PPTX → to_pdf.sh → PDF
정부서식(MD) → build_hwpx.mts → HWPX

[항상 생성 · 의존성 0]
사업계획서 MD ─ md_to_html.py ─▶ final-business-plan.html  (공유·웹 미리보기·인쇄·1차 검수)
deck.json ──── build_html_deck.py ─▶ pitch-deck.html        (16:9 슬라이드)
```

단계별 산출 위치는 SKILL.md "프로젝트 스캐폴딩"의 폴더 매핑이 단일 출처다.

---

## 8. 출력 후 렌더링 검사 (PRD §29 — 완료 직전 필수)

스크립트가 0으로 끝나도 아직 완료가 아니다. 아래를 확인한 뒤에만 완료를 선언한다.

1. **DOCX/HWPX/PPTX → PDF 변환** 후 PDF 를 연다(`to_pdf.sh`).
2. 점검 체크리스트:
   - [ ] 표가 깨지지 않았는가(셀 병합 누락·컬럼 밀림·빈 셀 폭주)
   - [ ] 그림이 정상 삽입되었는가(빈 자리·`[이미지: ...]` 텍스트 잔존 여부)
   - [ ] 한글 폰트가 정상 표시되는가(□ 두부 글자 없음)
   - [ ] 공란/빈 섹션이 없는가(`[확인 필요]` 잔존이 본문에 노출되지 않았는가)
   - [ ] 수치가 코어·엑셀·문서에서 동일한가(7대 규칙 #7 숫자 일관성)
3. 프로젝트 전체 진단: `python3 scripts/validate_project.py bizplan-<slug>/`
   — 게이트별 ✓/✗/⚠ 와 모호어·출처 행 수를 보고(비차단 진단).
4. **깨진 부분이 있으면** `10-final/format-damage-report.md` 를 만들어
   (어느 파일 / 어느 표·그림 / 증상 / 원인 추정 / 재생성 방법)을 기록하고, 원인을 고쳐 재생성한다.

---

## 9. 트러블슈팅

| 증상 | 원인 | 해결 |
|---|---|---|
| `python-docx 가 없습니다` | 패키지 미설치 | `pip3 install python-docx` |
| DOCX 한글이 □ 로 표시 | 뷰어에 한글 글꼴 없음 | 맑은 고딕/나눔고딕 설치, 또는 PDF 로 확인 |
| 표가 텍스트로 강등됨 | 파이프 표에 구분선 `|---|` 누락 | 헤더 다음 줄에 `|---|---|` 추가 |
| 이미지가 `[이미지: ...]` 로 나옴 | 경로 오류(상대경로 기준은 md 위치) | 경로 수정 또는 먼저 `render_diagram.sh` 로 PNG 생성 |
| `soffice 를 찾을 수 없습니다` | LibreOffice 미설치 | `brew install --cask libreoffice` |
| PDF 변환이 멈춤/충돌 | soffice 인스턴스 동시 실행 | to_pdf.sh 는 임시 프로파일로 회피. 그래도 충돌 시 기존 soffice 종료 |
| `mmdc/dot 가 없어 렌더 못함`(경고) | 다이어그램 도구 미설치 | 선택 도구 — 설치하거나 원본만 보존하고 진행 |
| XLSX 숫자가 텍스트로 저장됨 | 천단위 콤마/단위 문자 포함 | spec 에서 순수 숫자만 입력(단위는 컬럼명·별도 셀로) |
| YAML spec 파싱 실패 | 들여쓰기/탭 혼용 | 공백 들여쓰기 통일, `columns`/`rows` 구조 확인 |
| node 스크립트 실행 안 됨 | `npm install` 미실행 | 스킬 루트에서 `npm install` |
