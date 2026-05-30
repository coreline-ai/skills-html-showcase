# Quality Gates

## Theme Gate

- `theme.css`, `components.css`, `layouts.css`를 모두 연결하거나 `base.html`에 inline으로 합친다.
- 인쇄가 필요한 결과물은 `print.css`를 포함한다.
- 색상 토큰을 페이지별로 임의 변경하지 않는다.
- 외부 JS 없이 열려야 한다.
- 공개 블로그형 결과물은 Pretendard Variable + Noto Serif KR 폰트 링크를 head에 포함한다.

## Layout Gate

- 선택한 모드의 필수 블록이 모두 포함되어야 한다.
- beginner, article, education, blog, case study는 780px 안팎 읽기 폭을 유지한다.
- expert, seo, platform, audit, reference, comparison, landing, checklist는 1020px 이하 분석 폭을 사용한다.
- 모바일에서는 모든 그리드가 1컬럼으로 내려와야 한다.
- table은 `.tbl` wrapper를 쓰거나 모바일 카드로 대체한다.

## Editorial Gate

- 첫 화면은 kicker, h1, sub, meta, divider, toc/summary 순서로 안정적이어야 한다.
- H1은 한국어 긴 제목에서 과하게 커지지 않아야 한다.
- 주요 h2에는 `.h2-sub`가 있어야 한다.
- `.term`, `.analogy`, `.danger`, `.good`은 가능한 한 `.label`/`.word`/`.name` 구조를 사용한다.
- prose 65~75%, box 25~35% 비율을 목표로 한다.
- `.hl`은 2~4개만 사용하고, 색상 박스 내부에서는 사용하지 않는다.
- 검정 박스는 마지막 `.try` 중심으로 사용한다.

## Content Gate

- 제목은 구체적이어야 한다.
- 첫 문단은 독자에게 얻을 가치를 알려야 한다.
- 마지막에는 다음 행동 또는 체크리스트가 있어야 한다.
- 출처는 본문 흐름을 방해하지 않게 `.source-note`와 source hub로 분리한다.
- skill audit은 개선본 또는 명확한 패치 계획을 포함한다.
- SEO 결과물은 title/meta/tag/final set을 포함한다.
- platform 결과물은 플랫폼별 차이를 실제 발행 관점에서 분리한다.

## HTML Gate

- `lang="ko"`
- viewport 존재
- title/meta description 존재
- h1 1개
- h2 순서 정상
- 내부 링크 깨짐 없음
- 외부 링크는 필요 시 검증
- JSON-LD가 있으면 valid JSON이어야 한다.
