# YouTube Analysis System

`youtube_analysis`는 YouTube 영상을 “요약”으로 끝내지 않고, 시청 판단·근거 검증·댓글 신호·콘텐츠 제작 액션으로 변환하는 모드다. 스킬은 YouTube API/댓글 크롤러/자막 다운로더가 아니며, 사용자가 제공한 URL·메타·트랜스크립트·댓글 또는 브라우징으로 확인 가능한 표면만 사용한다.

## 1. 입력 Tier 계약

| Tier | 입력 | 허용 출력 | 금지 |
|---|---|---|---|
| A | URL + transcript + comments/metadata | Full report: Evidence Map, Comment Wall, Claim/Risk, Opportunity, Blueprint | 댓글 전체 여론 단정 |
| B | URL + metadata/chapter만 | Source Snapshot, TL;DW 가설, Chapter Map, Source Limits | transcript 기반 주장 단정 |
| C | URL만 | 메타 중심 요약, 확인 필요 목록, transcript/comment 요청 | 영상 내용을 FACT로 단정 |

모든 결과물에는 `observed_at` 또는 “분석 기준 시각”을 남긴다. 조회수·좋아요·댓글 수는 변동값이며, 비공개 지표(CTR, retention, revenue, subscribers gain)는 추정하지 않는다.

## 2. 필수 블록

```text
source & trust snapshot
→ TL;DW + watching decision
→ Video Evidence Map
→ chapter / retention story
→ comment signal wall
→ opportunity matrix
→ claim / evidence / risk
→ video blueprint
→ reuse pack
→ next actions
→ source limits
```

## 3. FACT / INFERENCE / UNKNOWN

- **FACT**: transcript, 화면에 보이는 메타, 사용자가 제공한 댓글/챕터에 직접 있는 내용.
- **INFERENCE**: 반복 질문, 제작 기회, 리텐션 가설, 콘텐츠 갭처럼 근거에서 합리적으로 도출한 해석.
- **UNKNOWN**: 비공개 analytics, 확인하지 못한 댓글 전체 여론, 자막 없는 구간의 실제 발화.

각 핵심 판단에는 “근거” 또는 “확인 위치”를 둔다. 근거가 없으면 점수화하지 않고 `확인 필요`로 남긴다.

## 4. 시각화 계약

| 정보 구조 | vt | wg | 사용 이유 |
|---|---|---|---|
| 챕터/시청 흐름 | `timeline` | `wg-13` | 시간 기반 근거 흐름 |
| 주장/위험 | `risk-matrix` | `wg-18` | 단정 위험과 검증 필요 항목 |
| 검증 기준 | `quality-gate` | `wg-16` | 볼지/쓸지/제작할지 결정 게이트 |
| 콘텐츠 기회 | `decision-tree`, `comparison-cards` | `wg-14` | 주제·훅·시리즈 선택 |
| 활동/반응 요약 | `checklist-flow` | `wg-11` | 댓글/메타 신호 요약 |

`wg-15`, `wg-20`은 초보 설명 또는 프롬프트 튜닝 요청이 명시될 때만 조건부 사용한다.

## 5. 금지/주의

- YouTube iframe/player embed 금지.
- autoplay 딥링크 금지. 타임스탬프 링크는 일반 `https://youtu.be/<id>?t=<sec>` 형태만 허용.
- 썸네일·영상 프레임을 output에 임베드/재배포하지 않는다.
- transcript 장문 인용 금지. 필요한 짧은 인용만 쓰고 나머지는 요약한다.
- 댓글은 표본으로만 다루며 전체 시청자 여론으로 단정하지 않는다.
