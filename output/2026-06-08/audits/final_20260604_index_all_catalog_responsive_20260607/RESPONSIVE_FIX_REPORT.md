# index-all-templates-catalog.html 가로폭 대응 수정 리포트

## 대상

- URL: `http://localhost:8080/templates/final_20260604/index-all-templates-catalog.html`
- 파일: `templates/final_20260604/index-all-templates-catalog.html`
- 검증 뷰포트: 390px, 768px, 1280px

## 캡쳐 기반 발견 사항

| 섹션 | 발견 문제 | 수정 내용 |
|---|---|---|
| wg 09 · arrow key slide deck | 내부 슬라이드 트랙이 390/768/1280에서 화면 밖 슬라이드를 가진 채 `scrollWidth`를 크게 발생 | 카탈로그 화면에서는 슬라이드를 화면 폭에 맞춘 카드 그리드로 펼치도록 변경. 모바일 1열, 넓은 화면 auto-fit grid 적용 |
| index_diff.html 변경 내역 표 | 390px에서 표가 가로 스크롤/잘림 형태로 보임 | 모바일에서 row-card stack 구조로 변환. 데스크톱도 `table-layout:fixed`, `overflow-wrap:anywhere`로 폭 안에서 줄바꿈 |
| wg 06 · component variants | 390px에서 버튼 상태 표의 뒤쪽 열이 보이지 않음 | 모바일에서 Variant별 카드 스택으로 변환. Default/Hover/Focus/Disabled 라벨을 각 행에 표시 |
| wg 16 · implementation plan | 768px에서 리스크 테이블과 플로우 노드가 내부 overflow를 발생 | 900px 이하에서 리스크 테이블을 카드 스택으로 전환. 플로우 노드 화살표를 노드 내부로 보정 |
| wg 03 · annotated pull request | 768px에서 긴 코드 토큰이 내부 overflow 발생 | 900px 이하에서 diff code를 `pre-wrap` + `overflow-wrap:anywhere`로 전환 |
| wg 07 · animation sandbox | 애니메이션 transform이 캡쳐/DOM 기준 내부 overflow를 발생 | 카탈로그 스냅샷에서는 off-canvas decorative motion을 정지해 카드 안에 안정 배치 |
| wg 08 · clickable flow | 숨김 화면의 translate transition이 내부 overflow를 발생 | 카탈로그 보정에서 숨김 screen transform 제거 |
| wg 15 · concept explainer | 원형 노드가 ring 밖으로 배치되어 내부 overflow를 발생 | 노드 위치를 ring 내부로 보정하고 섹션 간 상단 여백 보강 |
| vt 02 · decision tree | 모바일 세로 화살표 pseudo-element가 미세 overflow 발생 | 모바일 화살표 폭/arrowhead 위치 보정 |

## 최종 검증 결과

| Viewport | document scrollWidth | body scrollWidth | 가로 overflow 섹션 |
|---:|---:|---:|---|
| 390 | 390 | 390 | 없음 |
| 768 | 768 | 768 | 없음 |
| 1280 | 1280 | 1280 | 없음 |

## 증거 산출물

- Before audit: `responsive-audit-before.md`
- After audit: `responsive-audit-after.md`
- Key after screenshots: `screenshots-key-after/`
- Full-page after screenshots: `screenshots-key-after/390-full.png`, `768-full.png`, `1280-full.png`

> 참고: 섹션 단위 캡쳐에 보이는 빨간 가로선은 실제 섹션 overflow가 아니라 페이지 최상단 fixed `.reading-progress`가 locator screenshot crop에 포함된 것입니다. 최종 DOM 기준 body/document 가로 overflow는 0입니다.
