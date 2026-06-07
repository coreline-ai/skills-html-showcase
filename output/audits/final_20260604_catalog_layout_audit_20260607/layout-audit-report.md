# index-all-templates-catalog.html 레이아웃/가독성 1차 감사

- 대상: `http://localhost:8080/templates/final_20260604/index-all-templates-catalog.html`
- 감사 시각: 2026-06-07 KST
- 캡쳐 범위: header + 직접 섹션 41개(vt 21 + wg 20)
- 캡쳐 폴더:
  - 1280px: `output/audits/final_20260604_catalog_layout_audit_20260607/sections-1280/`
  - 390px: `output/audits/final_20260604_catalog_layout_audit_20260607/sections-390/`
- 지표:
  - 1280px 전체 가로 overflow: 없음 (`scrollWidth=1280`, `clientWidth=1280`)
  - 390px 전체 가로 overflow: 있음 (`scrollWidth=393`, `clientWidth=390`)

## 우선순위 이슈

### P0 — 모바일에서 실제 내용이 잘림/보이지 않음

1. `vt 03 · risk matrix`
   - 390px에서 우측 컬럼이 잘려 보임.
   - 영향: 가능성/영향 매트릭스의 일부 열을 읽을 수 없어 템플릿 의미가 깨짐.
   - 증거: `sections-390/03_vt-03-risk-matrix.png`

2. `vt 19 · feature flag`
   - 390px에서 토글 카드가 오른쪽으로 밀려 ON/OFF 토글 일부가 화면 밖으로 잘림.
   - 영향: 상태 값이 잘려 보이고 전체 행 폭이 모바일에 맞지 않음.
   - 증거: `sections-390/19_vt-19-feature-flag.png`

3. `wg 04 · module map`
   - 390px에서 그래프가 오른쪽으로 잘림. `cart`, `order`, `logger` 등 우측 노드/연결선 일부가 화면 밖에 있음.
   - 영향: 의존성 그래프가 핵심 템플릿인데 모바일에서 구조를 온전히 볼 수 없음.
   - 증거: `sections-390/25_wg-04-module-map.png`

4. `wg 03 · annotated pull request`
   - 390px에서 diff code 줄이 오른쪽에서 잘림. 아이콘이 경계에 붙고, 긴 코드가 자연스럽게 스크롤/랩되지 않음.
   - 영향: 코드 리뷰 템플릿의 핵심인 변경 줄이 끝까지 안 보임.
   - 증거: `sections-390/24_wg-03-annotated-pull-request.png`

5. `wg 16 · implementation plan`
   - 390px에서 리스크 평가 테이블의 뒤쪽 열이 사라짐. 캡쳐에서는 `리스크`, `가능성` 정도만 보이고 `영향`, `완화책` 열이 누락된 것처럼 보임.
   - 영향: 표의 판단 정보가 절반 이상 보이지 않음.
   - 증거: `sections-390/37_wg-16-implementation-plan.png`

6. `vt 21 · soft workflow map`
   - 390px에서 상단 우측 `AI`/아이콘 영역이 컨테이너 안에서 잘림.
   - 영향: 전체 도판은 세로 스택으로 어느 정도 전환되지만 헤더 장식/상태 영역이 모바일 폭에 맞지 않음.
   - 증거: `sections-390/21_vt-21-soft-workflow-map.png`

### P1 — 색상/텍스트 대비 또는 텍스트 크기 불안정

7. `wg 20 · prompt tuner`
   - 데스크톱에서 `샘플 입력`, `렌더 결과` 패널이 비어 있어 미완성/비활성처럼 보임.
   - `{{message}}`, `{{tone}}` 변수 칩은 노랑/갈색 대비가 낮아 작은 화면에서 흐릿함.
   - 증거: `sections-1280/41_wg-20-prompt-tuner.png`

8. `wg 02 · visual design directions`
   - 팔레트 swatch 안의 `bg`, `ink`, `accent`, `blue` 텍스트가 9px 수준으로 작고, 일부 색상 조합은 대비가 낮음.
   - 영향: 카탈로그가 색상 토큰을 보여주는 영역인데 토큰명이 잘 읽히지 않음.
   - 증거: `sections-1280/23_wg-02-visual-design-directions.png`, `sections-390/23_wg-02-visual-design-directions.png`

9. `vt 19 · feature flag`
   - `WARN` 텍스트/아이콘의 주황색 대비가 낮음.
   - 영향: 경고 상태를 빠르게 식별하기 어렵고, 모바일 잘림과 합쳐져 상태 가독성이 더 떨어짐.
   - 증거: `sections-1280/19_vt-19-feature-flag.png`

10. `wg 13 · annotated flowchart`
    - 단계 칩/보조 태그 중 일부가 10px 수준이고, 금색 칩의 흰 글자 대비가 낮음.
    - 영향: 데스크톱에서는 치명적이지 않지만 카탈로그 품질 기준으로 텍스트 크기 균형이 약함.
    - 증거: `sections-1280/34_wg-13-annotated-flowchart.png`

11. `vt 21 · soft workflow map`
    - 흰 카드 안의 주황색 심볼형 아이콘 대비가 낮음.
    - 영향: 장식 요소라 P0은 아니지만, 다수 반복되어 전체 도판이 흐릿해 보임.
    - 증거: `sections-1280/21_vt-21-soft-workflow-map.png`

### P2 — 레이아웃 균형/정보 밀도 개선 후보

12. Header
    - 현재 header는 `전 템플릿 카탈로그 — vt 21 + wg 20`, 간단 설명, hash chip만 있어 최신 쇼케이스 헤더에 비해 정보 구조가 빈약함.
    - 문제 성격: 깨짐은 아니지만, 카탈로그 대표 화면치고 메타/lens/generated row가 부족하고 시각적 밀도가 낮음.
    - 증거: `sections-1280/00_header.png`

13. `wg 05 · living design system`
    - 섹션 높이가 매우 큼(1280px 기준 약 2374px). 토큰표 자체는 정상이나 한 섹션 안에 색상·상태·타입·스페이싱·반경이 모두 들어가 스크롤 부담이 큼.
    - 문제 성격: 레이아웃 깨짐은 아니지만, 카탈로그 탐색성 관점에서는 분리/접힘 처리가 더 적합.
    - 증거: `sections-1280/26_wg-05-living-design-system.png`

14. `wg 08 · clickable flow`, `wg 09 · arrow key slide deck`
    - 데스크톱에서는 중앙 프로토타입이 좁고 양쪽 여백이 큰 편.
    - 문제 성격: 깨짐은 아니지만 전체 카탈로그에서 다른 템플릿보다 활용 폭이 낮아 보임.
    - 증거: `sections-1280/29_wg-08-clickable-flow.png`, `sections-1280/30_wg-09-arrow-key-slide-deck.png`

## 정상으로 보이는 주요 섹션

- vt 01, 02, 04, 05, 06, 07, 08, 09, 10, 11, 12, 13, 14, 15, 16, 17, 18, 20은 1280px 기준 큰 깨짐 없음.
- wg 01, 06, 07, 11, 12, 14, 15, 17, 18, 19는 1280px 기준 큰 깨짐 없음.

## 수정 우선순위 제안

1. 모바일/좁은 폭 잘림 우선: vt03, vt19, wg04, wg03, wg16, vt21.
2. 텍스트 대비/크기: wg20 변수칩, wg02 swatch label, vt19 WARN, wg13 step chip, vt21 icon tone.
3. 정보 구조 정리: header 최신 쇼케이스형으로 보강, wg05 분리/접힘, wg08/wg09 데스크톱 폭 활용 개선.
