# YouTube Analysis System

`youtube_analysis`는 YouTube 영상을 “요약”으로 끝내지 않고, 시청 판단·근거 검증·댓글 신호·콘텐츠 제작 액션으로 변환하는 모드다. 스킬은 YouTube API/댓글 크롤러/자막 다운로더가 아니며, 사용자가 제공한 URL·메타·트랜스크립트·댓글 또는 브라우징으로 확인 가능한 표면만 사용한다.

## 1. 입력 Tier 계약

| Tier | 입력 | 허용 출력 | 금지 |
|---|---|---|---|
| A | URL + transcript + comments/metadata | Full report: Evidence Map, Comment Wall, Claim/Risk, Opportunity, Blueprint | 댓글 전체 여론 단정 |
| B | URL + metadata/chapter만 | Source Snapshot, TL;DW 가설, Chapter Map, Source Limits | transcript 기반 주장 단정 |
| C | URL만 | 메타 중심 요약, 확인 필요 목록, transcript/comment 요청 | 영상 내용을 FACT로 단정 |

모든 결과물에는 `observed_at` 또는 “분석 기준 시각”을 남긴다. 조회수·좋아요·댓글 수는 변동값이며, 비공개 지표(CTR, retention, revenue, subscribers gain)는 추정하지 않는다.

Tier가 낮아지면 본문 톤 전체가 강등된다. Tier C에서 Tier A급 단정 문장이 하나라도 나오면 그 리포트는 실패다. 반대로 Tier A인데 transcript 인용 근거가 없는 주장만 나열되면 입력을 낭비한 것이다.

## 2. 필수 블록과 깊이 하한

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

블록 수 충족은 완료 조건이 아니다. 각 블록은 아래 질문에 답하고 깊이 하한을 충족해야 한다(SKILL.md §4 정량 하한과 동일 계약).

| 블록 | 답해야 할 질문 | 깊이 하한 |
|---|---|---|
| source & trust snapshot | 무엇이 입력이고 어디까지 믿을 수 있나 | FACT/INFERENCE/UNKNOWN 카드 3종, 카드당 2문장+ (tier 영향 포함) |
| TL;DW + watching decision | 누가 봐야 하고 누가 건너뛰나 | 추천/스킵/시청 후 행동 카드, 판단 기준 명시 |
| Video Evidence Map | 영상의 주장은 무엇에 기반하나 | 표 최소 5행(주장·근거·판정·다음 확인), 타임라인 최소 4항목 + 항목당 판정 근거 1문장+ |
| chapter / retention story | 편집 구조가 시청 지속을 어떻게 만드나 | KPI 위젯 + 해석 prose 2문장+ + 구조 분석 목록 |
| comment signal wall | 댓글은 어떤 수요/감정 신호인가 | 카드 3종, 카드당 2문장+ (표본 한계 명시 1회 필수) |
| opportunity matrix | 어떤 후속물을 만들 가치가 있나 | 기회 카드 3개+, 카드마다 수요 근거 + 제작 난이도 판단 |
| claim / evidence / risk | 과장 위험은 어디 있나 | risk-matrix + 상위 리스크별 완화 행동 목록(고위험 전부) |
| video blueprint | 다음 영상은 어떻게 설계하나 | Hook/Proof/Action에 구간 시간 배분 + 원 영상의 강점/약점 반영 근거 |
| reuse pack | 채널별로 무엇을 가져가나 | 포맷 3종+, 포맷마다 가져갈 섹션 번호 명시 |
| next actions | 독자가 지금 무엇을 하나 | 순서 있는 행동 4개+, UNKNOWN 승격 계획 포함 |
| source limits | 무엇을 확인하지 못했나 | tier 명시 + 확인 불가 항목 열거 |

## 3. FACT / INFERENCE / UNKNOWN

- **FACT**: transcript, 화면에 보이는 메타, 사용자가 제공한 댓글/챕터에 직접 있는 내용.
- **INFERENCE**: 반복 질문, 제작 기회, 리텐션 가설, 콘텐츠 갭처럼 근거에서 합리적으로 도출한 해석.
- **UNKNOWN**: 비공개 analytics, 확인하지 못한 댓글 전체 여론, 자막 없는 구간의 실제 발화.

각 핵심 판단에는 “근거” 또는 “확인 위치”를 둔다. 근거가 없으면 점수화하지 않고 `확인 필요`로 남긴다.

라벨 운영 규칙:

- 라벨은 장식이 아니다. FACT 라벨이 붙은 문장에는 타임스탬프나 댓글 위치 같은 검증 좌표가 있어야 한다.
- UNKNOWN에는 “무엇이 확보되면 FACT로 승격되는지”를 함께 적는다. 승격 조건 없는 UNKNOWN은 빈칸과 같다.
- 제작자가 스스로 한계를 인정한 발화는 반증 FACT로서 인용 우선순위가 가장 높다(제목·썸네일 기대치 보정에 직접 쓰인다).

## 4. 시각화 계약

| 정보 구조 | vt | wg | 사용 이유 |
|---|---|---|---|
| 챕터/시청 흐름 | `timeline` | `wg-13` | 시간 기반 근거 흐름 |
| 주장/위험 | `risk-matrix` | `wg-18` | 단정 위험과 검증 필요 항목 |
| 검증 기준 | `quality-gate` | `wg-16` | 볼지/쓸지/제작할지 결정 게이트 |
| 콘텐츠 기회 | `decision-tree`, `comparison-cards` | `wg-14` | 주제·훅·시리즈 선택 |
| 활동/반응 요약 | `checklist-flow` | `wg-11` | 댓글/메타 신호 요약 |

`wg-15`, `wg-20`은 초보 설명 또는 프롬프트 튜닝 요청이 명시될 때만 조건부 사용한다. 프로파일별 선택은 SKILL.md §0.6이 단일 출처다.

## 5. HTML 구성 계약

레이아웃: `assets/layouts/youtube-analysis.html` / class `.layout-youtube`

- 헤더는 `generated-row`(observed_at + input tier) + `lens-strip`(FACT/INFERENCE/UNKNOWN 칩)을 포함한다.
- verdict(`youtube-verdict`)는 본문 최상단에 두고, 질문 중심 목차(`toc-map youtube-question-toc`)가 뒤따른다.
- 목차 내부는 공식 카탈로그 `toc-map` chip-nav 구조(`span.label` + 설명 `p` + `.toc-pills` + `a.toc-pill > b`)로 작성한다. 구형 `.toc`/`ol` 또는 `.toc-map` 안의 bare link는 회귀다.
- 번호가 있는 모든 섹션 `h2`는 `body-icon body-icon--sm` → `num` → 제목 순서를 유지하고, 주요 h2에는 `h2-sub`를 붙인다.
- 권장 클래스: `.youtube-signal-grid`(신뢰도 카드), `.youtube-evidence-grid`/`.youtube-card`(판단 카드), `.youtube-comment-grid`(댓글 신호), `.youtube-opportunity-grid`/`.youtube-opportunity`+`.youtube-badge`(기회 매트릭스), `.youtube-blueprint-grid`(설계), `.youtube-reuse-grid`(재가공).
- Evidence Map 표는 visible `<caption>` + `mobile-card-table`(4열 이상) 계약을 따른다.

## 6. 흔한 실패 패턴 (즉시 재작성 대상)

- **넓고 얇은 출력**: 11개 블록을 전부 만들었지만 카드가 전부 1문장. 깊이 하한 위반이며 게이트 통과와 무관하게 미완성이다.
- **라벨만 있는 분리**: FACT/INFERENCE 칩은 있는데 본문 문장에 검증 좌표가 없다.
- **요약 영상화**: Evidence Map 없이 줄거리 요약으로 채운다. 이 모드의 존재 이유 부정.
- **타임스탬프 발명**: 입력에 없는 구간 시간을 그럴듯하게 만들어낸다. 입력 tier가 낮으면 “구조 예시”임을 명시한다.
- **h2-sub 생략**: 다른 모드와의 디자인 리듬이 깨져 품질이 낮아 보이는 직접 원인.

## 7. Source note 계약

마지막 `source-note`에는 반드시 다음을 남긴다.

- 입력 tier와 분석 기준 시각(observed_at).
- 확인한 표면: transcript 범위, 댓글 표본 크기/수집 방식, 챕터/메타.
- 확인 불가 항목: 전체 댓글 여론, 비공개 analytics, 자막 없는 구간, 후속 업데이트.
- 임베드/autoplay 미사용 선언(의도적 정책임을 명시).

## 8. 금지/주의

- YouTube iframe/player embed 금지.
- autoplay 딥링크 금지. 타임스탬프 링크는 일반 `https://youtu.be/<id>?t=<sec>` 형태만 허용.
- 썸네일·영상 프레임을 output에 임베드/재배포하지 않는다.
- transcript 장문 인용 금지. 필요한 짧은 인용만 쓰고 나머지는 요약한다.
- 댓글은 표본으로만 다루며 전체 시청자 여론으로 단정하지 않는다.

## 9. 완료 게이트

- `h1` 하나, `<main id="main" class="page-wide layout-youtube">` 유지.
- 헤더 `generated-row`/`lens-strip`, 테마 스위처, 번호 앞 body icon 유지.
- 외부/동작 JS 0. embed/autoplay 0 (`validate_output.py`의 `youtube_embed_or_autoplay_forbidden`).
- Evidence Map과 Source Limits 존재 (`youtube_evidence_map_missing`/`youtube_source_limits_missing`).
- FACT/INFERENCE/UNKNOWN 라벨과 observed_at 존재 (`youtube_fact_inference_unknown_labels_missing`/`youtube_observed_at_missing`).
- §2 깊이 하한 충족 — 표 5행+, 타임라인 4항목+, 카드당 2문장+. 게이트가 잡지 못해도 이 하한 미달은 미완성이다.
