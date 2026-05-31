# adaptive-html-final 디자인 품질 전문가 리뷰 (v4)

> 7개 디자인 전문가 페르소나가 v4 쇼케이스의 **실측 렌더 26종**(데스크탑 풀페이지 14 + 모바일 390px 6 + SVG 6)을 직접 보며 검토 → 디자인 총괄(Design Lead) 종합
> 작성일: 2026-05-31

## 1. 종합 총평

adaptive-html-final v4는 **토큰 시스템과 한국어 에디토리얼 조판의 토대가 시니어급으로 견고한** 시스템이다. 단일 accent(#e63946) + 크림 배경(#f5f5f0) + Noto Serif KR/Pretendard 페어링이 13개 모드 전반에서 흔들림 없이 반복되어 "한 제품"으로 즉시 읽히고, 한글 본문 조판(line-height 1.8, keep-all, word-break), 색-의미 매핑(term/analogy/danger/good), 접근성 보정(보조 텍스트 AA, reduced-motion, skip link, 표의 data-label 카드화)은 단순 통과를 넘어 "디자인 품질로서의 완성도"에 도달해 있다. 그러나 **시스템 품질이 운용(편집) 전략과 데이터 인코딩으로 이어지지 못한 지점에서 점수가 갈린다** — 색 틴트 박스의 백투백 적층("박스의 벽")과 빨강 accent의 남용으로 강조의 화폐가치가 소진되고, 첫 화면 임팩트가 약해 "표지 없는 문서"로 시작하며, SVG 인포그래픽은 면적·두께가 데이터값이 아닌 하드코딩 상수라 차트가 데이터를 배신한다. 또한 spacing 토큰 축 부재와 타입 스케일 과잉 분화는 다음 성숙 단계를 막는 구조 부채다. **요약하면 "토큰은 A급, 운용·인코딩은 B급" — 밀도를 빼고 강조를 아끼며 데이터를 진짜로 연결하는 결정만으로 한 단계 도약 가능한 시스템이다.**

**디자인 성숙도 점수: 74 / 100**
**한 줄 결론: 토대는 시니어급, 운용은 미들급. "덜어내기·아껴쓰기·데이터 연결" 세 가지 편집 결정이 도약의 열쇠다.**

> 가중 산식: 본체 6개 페르소나(아트72·타이포79·UX74·접근성82·반응형78·디자인시스템78) 각 1.0, 별도 SVG 파이프라인의 데이터시각화(58)는 0.5 → (72+79+74+82+78+78 + 58×0.5) ÷ 6.5 ≈ **73.8 ≈ 74**

## 2. 페르소나별 점수·핵심

| 페르소나 | 점수 | 강점 1 | 핵심 개선 1 |
|---|---|---|---|
| 아트 디렉터 / 비주얼 | 72 | 단일 accent+크림+serif/sans 톤 일관성이 13페이지 흔들림 없음 | 틴트 박스 적층("박스의 벽") 밀도 30~40% 감축 |
| 타이포그래피 | 79 | serif 제목/sans 본문 + 한글 조판 기본기(1.8/keep-all)가 토큰 단위로 정교 | page-wide에서 산문 폭이 90자+ → 가독 한계 초과 |
| UX/정보구조(IA) | 74 | 첫 화면 "무엇·왜·어디로" 스캔 경로 명확, 의사결정 IA 우수 | 긴 페이지 진행감(스크롤 스파이·진행 바) 전무 |
| 인클루시브/접근성 | 82 | 보조 텍스트 AA 토큰화·색 외 단서·reduced-motion 모범 | 포커스 링이 장식색(빨강)과 동일 → 변별성 약함 |
| 데이터 시각화 | 58 | Risk Heatmap/Evidence Pyramid 색 인코딩은 직관적 | placeholder 라벨 + treemap/sankey 면적·두께가 상수(데이터 배신) |
| 반응형/모바일 | 78 | 표의 data-label 카드화가 접근성까지 갖춘 모범 구현 | 터치 타깃 44px 미달(네비·칩·TOC) |
| 디자인 시스템 / 브랜드 | 78 | 13모드 통일성 + 콜아웃 의미 토큰 추출 성숙 | spacing 토큰 축 전무(px 리터럴 108곳) |

## 3. 잘하고 있는 것 (공통 강점)

- **브랜드 톤 일관성**: 단일 accent + 크림 배경 + serif/sans 페어링이 13모드 동일 적용 → 시리즈 신뢰감. 콜아웃·다크 try·빨강 원형번호 h2 시그니처가 "한 제품"임을 즉시 전달.
- **한글 에디토리얼 조판 기본기**: line-height 1.8·keep-all·overflow-wrap 토큰화, 780px 표준 컬럼 50~55자/줄로 한글 가독 권장 폭에 정확히 안착.
- **색-의미 매핑 + 색 외 단서**: term/analogy/danger/good이 좌측 바 + 텍스트 라벨 + 틴트 3중 단서 → 색맹·흑백에서도 정보 보존.
- **접근성 토대**: 보조 텍스트 AA(5.1~5.7:1), reduced-motion(scroll·hl), skip link·랜드마크·다크 링크 대비 10.5:1.
- **표의 모바일 카드화**: data-label + scope + .mobile-card-table로 760px 이하 "라벨:값" 카드 재배열 — 업계 모범.
- **의미 토큰 레이어 출현**: 콜아웃 색을 raw hex→의미 토큰(--term-ink 등) 추출 — SoT 수렴 노력의 증거.

## 4. 개선 이슈 트래커 (중복 제거·통합)

| 이슈 | severity | 근거 페르소나 | 개선안 (요약) |
|---|---|---|---|
| 빨강 accent 남용 — 강조 화폐 소진 | critical | 아트, 디자인시스템 | 숫자 칩 ink 아웃라인 기본형, 핵심 1~2섹션만 빨강. kicker/label→--accent-2, danger→--accent-2로 "경고/브랜드 빨강" 분리 |
| 틴트 박스 적층("박스의 벽") — 강조 평준화 | critical | 아트, 타이포 | 섹션당 callout 1~2개·동색 연속 금지, term/good 흰 배경+좌측 바, margin 16/20→28/32, 색면 30~40% 감축 |
| SVG: placeholder 라벨 + 면적/두께가 상수(treemap 순위 역전, sankey 흐름 보존 위반) | critical (SVG 파이프라인) | 데이터 시각화 | 렌더 입력을 도메인 데이터로, treemap 면적=value(squarified), sankey stroke=value×k + in=out assert, placeholder 시 QA fail |
| 첫 화면 임팩트 부재 — "표지 없는 문서" | high | 아트, 타이포, IA | index h1 clamp 40~72px·lh 1.08 + 헤더 색면/그리드 배너. 본문 kicker hairline+64px 상단 패딩 |
| page-wide 산문 폭 가독 한계 초과(90자+) | high | 타이포, IA | `.page-wide > p/ul/ol{max-width:46rem}` — 표·그리드·코드만 전폭 ("wide layout / narrow prose") |
| 긴 페이지 진행감 부재 | high | UX/IA | ~30줄 IntersectionObserver → 목차 active(aria-current) + top:0 4px 진행 바, reduced-motion 대응 |
| 목차/메타 모드별 불일치 | high | UX/IA | 전 모드 헤더 직후 nav.toc 의무화, SEO 예정 H2는 .outline-card, 메타 칩 순서 통일 |
| 포커스 링이 장식색(빨강)과 동일 | high | 접근성 | outline 3px #1a56db + offset 2px + 흰 box-shadow 헤일로, 다크 try는 흰 outline 오버라이드 |
| h2 원형번호 SR 노출(aria-hidden 부재) | high | 접근성 | `<span class="no" aria-hidden="true">`, 체크리스트 grep 회귀 항목 |
| 터치 타깃 44px 미달(네비·칩·TOC) | high | 반응형, 접근성 | 모바일 네비/TOC min-height:44px, 칩 32px, 패딩으로 히트영역 확대 |
| spacing 토큰 축 전무(px 리터럴 108곳) | high | 디자인시스템 | 8px 베이스 --space-1~8 도입, 마진/패딩 토큰 스냅 |
| 타입 스케일 과잉 분화(19종) | high | 디자인시스템, 타이포 | --fs-xs~2xl 6~7단 수렴, 반px 폐기, h3 serif 통일 |
| 수직 리듬 단조 | medium | 아트 | 핵심 표/그리드 풀블리드 폭 변주, section 96/32 차등, 페이지당 대형 pull-quote 1회 |
| 표 회색 균질(스프레드시트 인상) | medium | 아트 | th 잉크 다크+흰 텍스트, tbody zebra, 추천 열 --good-bg, 셀 패딩 10/14 |
| 다크 try/푸터 위치 불일치 | medium | 아트 | 다크 try를 모든 페이지 마지막 고정, index 푸터 동일 톤, 상단 margin 80px |
| 모바일 첫 화면 밀도 부족 | medium | 반응형 | 헤더 margin 42→28·padding 32→22, lead 18→16 |
| data-label 표기 불일치 | medium | 반응형 | 빌드 시 th→data-label 자동 주입, 즉시는 공백 통일 |
| page-nav 비활성 노출·CTA 약함 | medium | UX/IA | "이전 없음" 제거, 다음 글 weight 600+화살표, .try 1차 액션 알약 버튼 |
| 잔여 raw hex·try override 60줄 | medium | 디자인시스템 | --warn/--ok/--surface-sunken 토큰화, .try 의미 토큰 재바인딩(60→10줄) |
| 인라인 하이라이트 다색 노이즈 | low | 아트 | 페이지당 1색(노랑)·단락당 1회, em.t는 ink 굵게+accent-2 밑줄 |
| index 카드 위계 평탄 | low | 아트 | 카드 상단 4px 모드 컬러 띠, 대표 2~3개 span 2, 캡처 썸네일 |
| 영문/숫자 자간이 음수 트래킹에 끌림 | low | 타이포 | 칩/태그/표헤더/code letter-spacing 0~.02em 리셋, 숫자 tabular-nums |
| 콜아웃 명명 비대칭 | low | 디자인시스템 | .callout 베이스 + BEM 슬롯 표준화 |
| status-pill nowrap·라벨열 폭 부족(390px) | low | 반응형 | 카드 모드 nowrap 해제, 라벨열 minmax(104px,40%) |
| 리스크 등급 도형 위계 부재 | low | 접근성, 데이터시각화 | 등급 셀 도형+색+텍스트 삼중 인코딩(●▲◆○) |

## 5. 우선순위 향상 로드맵

### Quick Wins — impact 高 / effort 低 (1~3일, 토큰·CSS 한 곳 수정으로 13페이지 일괄)
1. **빨강 accent 빈도 제한** — h2 `.no/.num`을 ink 아웃라인 기본형으로, 핵심 1~2섹션만 빨강 솔리드. kicker/label/danger → --accent-2.
2. **page-wide 산문 폭 가두기** — `.page-wide > p/ul/ol{max-width:46rem}`. 표·그리드·코드만 전폭.
3. **포커스 링 재설계** — `:focus-visible{outline:3px solid #1a56db;outline-offset:2px;box-shadow:0 0 0 2px #fff}`, .try는 흰 outline 오버라이드.
4. **h2 원형번호 aria-hidden** — `<span class="no" aria-hidden="true">`. CSS 변경 0.
5. **모바일 터치 타깃 44px** — 네비/TOC min-height:44px, 칩 32px.
6. **모바일 헤더 리듬 압축** — 헤더 margin 42→28, padding 32→22, lead 18→16.
7. **data-label 표기 통일** — 11셀 공백 포함으로 즉시 통일.

### 중기 — impact 中~高 / effort 中 (1~2주, 편집 규칙·신규 토큰·소량 JS)
8. **틴트 박스 밀도 30~40% 감축** — 섹션당 1~2개·동색 연속 금지·margin 28/32·term/good 흰 배경.
9. **읽기 진행 바 + 목차 스크롤 스파이** — ~30줄 IntersectionObserver, aria-current + 4px 진행 바.
10. **spacing 토큰 8px 스케일** — --space-1~8 정의 후 108곳 스냅.
11. **타입 스케일 6~7단 수렴 + h3 serif 통일**.
12. **전 모드 목차·메타 표준화**.
13. **표 editorial 강화** — th 잉크 다크, zebra, 추천 열 강조.
14. **try override 토큰 재바인딩** — 60줄→10줄.

### 전략과제 — impact 高 / effort 高 (스프린트 단위, 구조·파이프라인)
15. **index 표지 + 갤러리 재설계** — h1 72px급, 헤더 배너, 카드 모드 컬러 띠+span 2+썸네일.
16. **수직 리듬 변주 시스템** — 폭 변주·간격 차등·대형 pull-quote.
17. **와이드(≥1100px) sticky 사이드 목차** — grid(220px+본문), .toc sticky.
18. **SVG 인포그래픽 데이터 구동 전환 + 무결성 검증** — placeholder→도메인 데이터, treemap 면적=value, sankey in=out assert, 수치 라벨/범례 의무화, 렌더 후 QA 게이트.

## 6. Top 10 고임팩트 개선

| # | 개선 | impact | effort | 근거 | 한 줄 실행법 |
|---|---|---|---|---|---|
| 1 | 빨강 accent 빈도 제한(숫자 칩 아웃라인화) | 高 | 低 | 아트·디자인시스템 | `.no/.num` ink 아웃라인, kicker/label/danger → --accent-2 |
| 2 | page-wide 산문 폭 46rem 가두기 | 高 | 低 | 타이포·IA | `.page-wide > p/ul/ol{max-width:46rem}` |
| 3 | 포커스 링 재설계(파랑+흰 헤일로) | 高 | 低 | 접근성 | :focus-visible outline 3px #1a56db + box-shadow 흰 헤일로 |
| 4 | h2 원형번호 aria-hidden | 高 | 低 | 접근성 | `<span class="no" aria-hidden="true">` |
| 5 | 모바일 터치 타깃 44px | 高 | 低 | 반응형·접근성 | 네비/TOC min-height:44px, 칩 32px |
| 6 | 틴트 박스 밀도 30~40% 감축 | 高 | 中 | 아트·타이포 | 섹션당 1~2개·동색 연속 금지·margin 28/32 |
| 7 | 읽기 진행 바 + 목차 스크롤 스파이 | 高 | 中 | UX/IA | ~30줄 IntersectionObserver + 4px 진행 바 |
| 8 | spacing 토큰 8px 스케일 | 高 | 中 | 디자인시스템 | --space-1~8 후 108곳 스냅 |
| 9 | 타입 스케일 6~7단 수렴 + h3 serif | 高 | 中 | 디자인시스템·타이포 | --fs-xs~2xl, 반px 폐기, h3 serif |
| 10 | index 표지 + 갤러리 재설계 | 高 | 中~高 | 아트·IA | h1 72px급, 헤더 배너, 카드 컬러 띠+span 2 |

> SVG 데이터 구동 전환(전략 #18)은 별도 파이프라인이라 Top 10 제외. SVG를 본문에 임베드할 계획이면 11위로 승격.

## 7. 한 줄 결론

토큰과 조판은 이미 시니어급이다 — **이제 필요한 건 새 기능이 아니라 "덜어내는 편집 결정"이다.** 빨강을 아끼고, 박스를 비우고, 와이드 산문을 가두고, 데이터를 진짜로 연결하면, 이 시스템은 "잘 만든 문서"에서 "전문가급 매거진"으로 한 단계 올라선다.

---
### 부록 — 리뷰 메타
- 투입: 디자인 페르소나 7 + 종합 1, 실측 렌더 26종(데스크탑 풀페이지 14 + 모바일 390px 6 + SVG 6)
- 소비: 약 397K 토큰 · 도구 호출 128회
- 렌더 원본: `/tmp/design_review/*.png`
