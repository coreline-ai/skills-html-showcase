# Visual Template System

고해상도 섹션 이미지는 장식이 아니라 이해·판단·검증을 돕는 정보 구조여야 한다. 기본값은 외부 사진 검색이 아니라 `8000×6000` SVG 인포그래픽 생성이다.

## 선택 원칙

1. 현실 인물·장소·제품·사건 사진이 필요하면 공개 라이선스 이미지를 찾고 출처/라이선스를 남긴다.
2. 절차·비교·정책·리스크·학습 구조는 SVG 인포그래픽으로 직접 만든다.
3. AI 생성 이미지는 메타포/컨셉 이미지가 필요할 때만 쓰고, 사실 이미지처럼 보이게 사용하지 않는다.
4. 모든 이미지는 `figure.visual-figure > img + figcaption` 패턴으로 삽입한다.
5. SVG 원본은 특별한 이유가 없으면 `8000×6000`을 유지한다.

## 모드별 기본 템플릿

| Mode | 기본 템플릿 | 권장 시각물 |
|---|---|---|
| beginner_html | hero-map, checklist-flow | 비유 일러스트, 개념 흐름, 흔한 오해 지도 |
| expert_html | hero-map, matrix, timeline, quality-gate | 운영모델, RACI, 리스크 매트릭스, 90일 로드맵 |
| article_html | hero-map, decision-tree | 키비주얼, 주장 구조도, 쟁점 흐름 |
| education_html | timeline, checklist-flow, hero-map | 학습 경로도, 실습 플로우, 퀴즈 전 체크 |
| github_analysis | hero-map, matrix, timeline, checklist-flow | 저장소 판단 흐름, 리스크, 활동 이력, 채택 체크 |
| github_feature_usage | hero-map, card-grid, decision-tree | 기능 지도, 실제 화면 흐름, 도입 적합성 판단 |
| youtube_analysis | timeline, matrix, quality-gate | 타임스탬프 근거 지도, 주장 위험, 콘텐츠 갭 |
| manual_analysis | hero-map, checklist-flow, quality-gate | 역할별 실행 경로, 안전 조건, 트러블슈팅 흐름 |
| blog_writer | hero-map, timeline | 문제-경험-해결 흐름, 개인 시행착오 지도 |
| seo_dashboard | card-grid, matrix | SERP 프리뷰, 키워드 클러스터, 제목 후보 비교 |
| platform_blog | card-grid, matrix, checklist-flow | 플랫폼별 카드, 발행 체크리스트, 채널 비교 |
| skill_audit | matrix, quality-gate, timeline | 점수 대시보드, 결함 분류, 개선 로드맵 |
| reference_html | card-grid, matrix | 개념/API 맵, 패턴/예제 분류 |
| comparison_html | matrix, decision-tree | 선택 매트릭스, 승자/트레이드오프 지도 |
| case_study_html | timeline, hero-map | 사건 타임라인, 원인-결정-결과 흐름 |
| landing_brief_html | hero-map, card-grid | 가치 제안 구조도, 대상별 메시지 카드 |
| checklist_playbook | checklist-flow, quality-gate | 운영 체크 플로우, 완료 기준, 실패 모드 |

## 템플릿 목록

- `visual-templates/hero-map.svg.tpl` — 상단 대표 구조도, 3단계 전략, 큰 결론.
- `visual-templates/card-grid.svg.tpl` — 모드/카테고리/키워드/플랫폼 카드 그리드.
- `visual-templates/decision-tree.svg.tpl` — 선택 기준, 분기형 판단 흐름.
- `visual-templates/quality-gate.svg.tpl` — 검수 기준, 릴리즈 게이트, 감사 항목.
- `visual-templates/timeline.svg.tpl` — 로드맵, 사건 흐름, 학습 진행.
- `visual-templates/matrix.svg.tpl` — 비교, 점수, 리스크, 우선순위.
- `visual-templates/checklist-flow.svg.tpl` — 운영 절차, 체크리스트, 완료 조건.

## visual brief 형식

`schemas/visual-brief.schema.json`을 따른다.

```json
{
  "type": "card-grid",
  "title": "21개 모드별 최적 이미지 타입",
  "subtitle": "모드마다 정보 구조를 보강하는 시각물을 붙입니다",
  "items": [
    {"label": "beginner", "title": "비유 일러스트", "description": "개념을 생활 장면으로 설명"},
    {"label": "expert", "title": "운영모델 지도", "description": "RACI·리스크·로드맵을 한 장에 정리"}
  ],
  "footer": "8000×6000 SVG · scalable infographic"
}
```

렌더링:

```bash
python scripts/render_visual_svg.py visual-brief.json media/visual.svg
```

## HTML 삽입 패턴

```html
<figure class="visual-figure is-hero">
  <img src="media/visual.svg" width="8000" height="6000" alt="섹션의 핵심 구조를 설명하는 구체적인 대체 텍스트">
  <figcaption>이미지가 말하는 결론을 한 문장으로 쓴다.</figcaption>
</figure>
```

## quality-gate 레이아웃 안전 규칙

- `quality-gate`는 2열×3행 카드 그리드와 하단 `PRE-FLIGHT` 패널로 구성한다.
- 하단 강조 패널은 납작한 배너로 만들지 말고 높이 700px 안팎의 충분한 카드로 만든다.
- 모든 주요 카드의 bottom은 5200px 이하, footer 텍스트는 5600px 근처에 둬 최소 350px 이상 여백을 확보한다.
- 노란 강조색(`#FFD400`)은 최종 검수/핵심 CTA처럼 한 곳에만 사용해 시선을 집중시킨다.

## 품질 게이트

- SVG 원본은 `8000×6000` 이상이다.
- 이미지가 장식이 아니라 섹션의 이해·판단·검증을 돕는다.
- `alt`와 `figcaption`이 모두 있다.
- 모바일 390px에서 이미지와 캡션이 잘리지 않는다.
- SVG 내부 카드/텍스트가 캔버스 밖으로 나가지 않는다.
- 외부 사진을 사용하면 URL, 저작자, 라이선스, 수정 여부를 남긴다.
- AI 생성 이미지는 사실 보도/인물/제품 증거처럼 사용하지 않는다.

## Soft Shape 도형 카탈로그 (본문 설명 시작부 보조)

위 인포그래픽이 "정보 자체를 SVG가 전달"하는 hero/별첨용이라면, **soft-shape 도형 36종**(`assets/shape-svgs/<id>.svg`)은 같은 `8000×6000` SVG·`figure.visual-figure` 매체를 쓰되 **본문 설명 시작부의 작은 시각 앵커**로 쓴다. 제목 아래에 대표 도형 1개를 두고 그 아래에서 문장으로 풀면, 독자가 긴 설명 전에 구조를 먼저 잡는다. **도형은 시각 앵커일 뿐 핵심 정보는 항상 HTML 텍스트로 둔다**(도형 안 글자에 의존 금지). warm cream 톤·`<title>/<desc>` 접근성·무 JS.

### 삽입 패턴

```html
<!-- 단독: 섹션 상단 대표 도형(작게). figcaption은 선택이지만 결론을 한 줄로 적으면 좋다 -->
<figure class="shape-figure">
  <img class="shape-img" src="assets/shape-svgs/branch-tree.svg" width="8000" height="6000" alt="조건에 따라 경로가 갈리는 분기 구조">
  <figcaption>사용자 조건에 따라 처리 경로가 달라진다.</figcaption>
</figure>

<!-- 리드: 도형 + 옆 설명을 나란히(설명이 옆 텍스트이므로 figcaption 생략) -->
<div class="shape-lead">
  <figure class="shape-figure">
    <img class="shape-img" src="assets/shape-svgs/funnel-filter.svg" width="8000" height="6000" alt="후보를 단계적으로 좁히는 퍼널">
  </figure>
  <div class="shape-lead-body"><h3>후보 좁히기</h3><p>…</p></div>
</div>
```

- 도형은 `figure.shape-figure`(visual-figure 아님)로 삽입한다. **`img`에는 비어있지 않은 `alt`가 필수**(도형 의미를 적되 핵심 정보는 본문 HTML 텍스트로). `alt`는 `shape_visual_gate`가, svg 파일 존재는 `broken_local_ref`가 검사한다. **figcaption은 선택**(앵커·갤러리라서 — visual-figure의 figcaption 강제를 피하려고 visual-figure를 쓰지 않는다). `.shape-figure`(폭 제한)·`.shape-lead`(2단)·`.shape-grid`(갤러리)는 `assets/shape-visuals.css`(프로파일 무관 조건부 인라인, `{{SHAPE_VISUALS_CSS}}` 슬롯)가 제공한다.
- 한 페이지에 도형을 남발하지 않는다(섹션 도입 1개 안팎). 갤러리(`.shape-grid`)는 "여러 개념을 균등 나열"할 때만.

### bi-(본문 아이콘)·vt-(다이어그램)와의 경계

- **글자 옆 1줄 장식 = `bi-`**(40×40 인라인 아이콘, `aria-hidden`). **문단/섹션 위 구조 프리뷰 = soft-shape figure**(8000×6000 img). **검색·복사·반응형이 필요한 본문 구조도 = `vt-`**(HTML 다이어그램) — 이 셋은 크기·매체·역할이 다르며 서로 대체하지 않는다. 도형을 vt- 다이어그램 대용으로 쓰지 않는다.

### 36종 카탈로그

**인-스킬 비주얼 카탈로그**: `galleries/soft-shapes-catalog.html`(36종 도형을 `.shape-grid`로 렌더한 레퍼런스 데모, `assets/shape-catalog.json`+`assets/shape-svgs/`에서 생성 — 생성 출력 아님). 아래는 동일 카탈로그의 텍스트 표.

| id | 이름 | 언제 쓰나 |
|---|---|---|
| `bar-metric` | 막대 지표 | 수치 비교를 간단히 보여줄 때 |
| `blob-idea` | 블롭 아이디어 | 정형화 전의 아이디어를 표현할 때 |
| `branch-tree` | 분기 트리 | 선택지와 하위 경로를 보여줄 때 |
| `checklist-done` | 체크리스트 | 완료 조건과 점검 항목을 보여줄 때 |
| `circle-focus` | 원형 포커스 | 핵심 개념 하나를 강조할 때 |
| `code-window` | 코드 윈도우 | 개발·자동화 흐름을 설명할 때 |
| `connector-nodes` | 연결 노드 | 관계와 의존성을 설명할 때 |
| `conversation-bubble` | 대화 버블 | 인터뷰·피드백·메시지를 설명할 때 |
| `cycle-loop` | 순환 루프 | 반복 개선 사이클을 설명할 때 |
| `diamond-decision` | 다이아몬드 결정 | 선택 지점과 판단 조건을 나타낼 때 |
| `document-card` | 문서 카드 | 자료·문서·레퍼런스 대입용 |
| `donut-ratio` | 도넛 비율 | 구성비나 점유율을 설명할 때 |
| `flow-arrow` | 흐름 화살표 | 입력→처리→결과 흐름을 보여줄 때 |
| `funnel-filter` | 퍼널 필터 | 후보를 좁혀가는 과정을 보여줄 때 |
| `grid-set` | 그리드 묶음 | 여러 항목을 균등하게 나열할 때 |
| `hex-system` | 육각 시스템 | 모듈/시스템 구성요소를 말할 때 |
| `ladder-growth` | 성장 사다리 | 점진적 성숙도나 레벨업을 보여줄 때 |
| `line-chart` | 라인 차트 | 시간에 따른 추세를 보여줄 때 |
| `matrix-quadrant` | 사분면 매트릭스 | 2축 기준의 판단표를 보여줄 때 |
| `orbit-context` | 오비트 맥락 | 중심 개념 주변 요소를 설명할 때 |
| `pill-label` | 필 라벨 | 상태·분류·태그를 부드럽게 보여줄 때 |
| `pyramid-levels` | 피라미드 단계 | 기초→상위 단계 구조를 말할 때 |
| `quote-source` | 원문 인용 | 원문 보존 또는 출처를 보여줄 때 |
| `rounded-rect` | 라운드 카드 | 정리된 정보 블록을 설명할 때 |
| `search-lens` | 검색 렌즈 | 검색·탐색·리서치 단계를 말할 때 |
| `shield-check` | 쉴드 검증 | 보안·품질·검수 기준을 말할 때 |
| `spark-card` | 스파크 카드 | 짧은 성과 요약을 보여줄 때 |
| `stack-layers` | 스택 레이어 | 계층·레이어·의존성을 설명할 때 |
| `star-insight` | 스타 인사이트 | 중요 발견이나 추천을 강조할 때 |
| `swimlane-process` | 스윔레인 | 역할별 병렬 진행을 보여줄 때 |
| `target-goal` | 타깃 목표 | 목표와 기준선을 맞출 때 |
| `timeline-steps` | 타임라인 단계 | 시간 순서의 진행을 보여줄 때 |
| `triangle-priority` | 삼각 우선순위 | 위계와 우선순위를 보여줄 때 |
| `venn-overlap` | 벤 다이어그램 | 겹치는 조건과 공통분모를 설명할 때 |
| `warning-gap` | 경고 갭 | 위험·누락·주의점을 강조할 때 |
| `wave-change` | 웨이브 변화 | 변동·추세·감정 흐름을 보여줄 때 |

### 모드별 도형 추천 (참고 — 결정 게이트 아님)

soft-shape는 선택적 보조라 §0.6 결정표(vt-/wg-)에 넣지 않는다. 아래는 자주 맞는 조합 참고일 뿐이다.

| 모드 | 자주 맞는 도형 |
|---|---|
| beginner_html | circle-focus, blob-idea, cycle-loop |
| expert_html | matrix-quadrant, shield-check, hex-system |
| article_html | branch-tree, venn-overlap, conversation-bubble |
| education_html | timeline-steps, ladder-growth, checklist-done |
| comparison_html | venn-overlap, matrix-quadrant, diamond-decision |
| reference_html | stack-layers, hex-system, document-card |
| seo_dashboard | funnel-filter, bar-metric, line-chart |
| case_study_html | timeline-steps, wave-change, warning-gap |
| checklist_playbook | checklist-done, funnel-filter, target-goal |
| landing_brief_html | target-goal, star-insight, spark-card |

## Soft Workflow Template 10종 (본문 대표 도판 / 랜딩 카드)

soft-shape가 "시작부의 **작은** 개념 앵커(420px)"라면, **soft workflow 도판 10종**(`assets/workflow-svgs/<id>.svg`)은 같은 8000×6000 SVG·warm cream 매체를 쓰되 **본문 대표 도판·섹션 상단 구조도·랜딩 설명 카드**용 **와이드(~720px)** 도판이다. AI/에이전트 워크플로우의 형식(파이프라인·허브·라우터·계층·퍼널·그래프·스웜·타임라인·보드·거버넌스)을 한 장으로 보여준다. 무 JS, `<title>/<desc>` 접근성, 라벤더 점선 connector·오렌지/퍼플/민트 포인트.

### 삽입 패턴

```html
<figure class="workflow-figure">
  <img class="workflow-img" src="assets/workflow-svgs/02-radial-hub.svg" width="8000" height="6000" alt="중앙 AI 허브와 주변 역할 에이전트가 방사형으로 연결된 구조">
  <figcaption>중앙 오케스트레이터가 역할별 에이전트를 호출·수렴한다.</figcaption>
</figure>

<!-- 여러 형식을 비교/나열할 때만 -->
<div class="workflow-grid">
  <figure class="workflow-figure"><img class="workflow-img" src="assets/workflow-svgs/01-linear-pipeline.svg" width="8000" height="6000" alt="입력→처리→결과 일직선 파이프라인"></figure>
  <figure class="workflow-figure"><img class="workflow-img" src="assets/workflow-svgs/05-quality-funnel.svg" width="8000" height="6000" alt="입력을 검토·필터링해 좁히는 퍼널"></figure>
</div>
```

- 도판은 `figure.workflow-figure`(visual-figure 아님)로 와이드(~720px) 표시한다. **`img.workflow-img`에 비어있지 않은 `alt` 필수**, **figcaption 권장**(도판 결론 한 줄). `alt`·8000×6000 해상도·네임스페이스는 `workflow_visual_gate`가 검사한다(`assets/workflow-visuals.css`, `{{WORKFLOW_VISUALS_CSS}}` 슬롯, 프로파일 무관).
- **내부 노드의 작은 라벨에 의미를 의존하지 말 것**(현재 자산의 내부 노드는 placeholder다). 핵심 정보는 인접 본문 HTML 텍스트와 figcaption에 둔다. 모바일에서 고정 height로 도판을 누르지 말고 4:3 비율(`object-fit:contain`)을 유지한다.
- **`wf-` 접두사 금지**(vt-21 soft-workflow-map의 `wf-board`/`wf-map` 게이트가 점유). 반드시 `workflow-` 풀네임.

### 매체 경계 (SVG 도판 vs HTML vt- vs soft-shape) — 정본

| 상황 / 의도 | 선택 | 매체·클래스 |
|---|---|---|
| 본문에서 **읽고 판단**해야 하는 구조도(절차·비교·리스크·RACI·타임라인) | **vt-** (HTML, 검색·복사·반응형) | `assets/visual-html-templates/` |
| 좌∥중앙대시보드∥우 **수렴형 AI 프로세스 맵**을 본문에서 읽힘 | **vt-21** soft-workflow-map | `.wf-board` (HTML) |
| 섹션 **설명 시작부의 작은 시각 앵커**(개념 1개) | **soft-shape** | `figure.shape-figure`(~420px) |
| 섹션 **상단 대표 도판 / 랜딩 설명 카드**(워크플로우 한 장, 와이드) | **workflow 도판(8819)** | `figure.workflow-figure`(~720px) |
| 다운로드·인쇄·발표 별첨 한 장 인포그래픽 | visual-template SVG | `figure.visual-figure` |

> **중복 회피**: workflow 도판은 placeholder 노드라 vt-처럼 본문 정보를 담지 못한다. 독자가 본문 한가운데서 절차·비교를 **바로 읽어야** 하면 workflow 도판이 아니라 vt-(flowchart/decision-tree/comparison-cards/timeline 등)를 쓴다. workflow 도판은 figcaption으로 결론을 요약하는 **대표 키비주얼/랜딩 카드**일 때만 선택한다(vt- 대체 금지).

### 10종 카탈로그

| no | id | 이름 | 언제 쓰나 |
|---|---|---|---|
| 01 | `01-linear-pipeline` | Linear Pipeline | 입력에서 결과까지 일직선 흐름을 보여주는 기본 자동화 파이프라인 |
| 02 | `02-radial-hub` | Radial Agent Hub | 중앙 AI 허브와 주변 역할/에이전트 관계를 보여주는 방사형 구조 |
| 03 | `03-decision-router` | Decision Router | 조건에 따라 다른 경로로 라우팅되는 판단 구조 |
| 04 | `04-layered-stack` | Layered Stack | 데이터·모델·검증·출력의 계층 구조를 보여주는 레이어형 |
| 05 | `05-quality-funnel` | Quality Funnel | 많은 입력을 검토·필터링해 최종 결과로 좁혀가는 퍼널형 |
| 06 | `06-knowledge-graph` | Knowledge Graph | 출처·개념·판단 사이 연결 관계를 보여주는 네트워크형 |
| 07 | `07-agent-swarm` | Agent Swarm | 여러 전문가 에이전트가 동시에 기여하는 병렬 협업 구조 |
| 08 | `08-timeline-delivery` | Timeline Delivery | 단계별 산출과 검증을 시간순으로 보여주는 타임라인형 |
| 09 | `09-comparison-board` | Comparison Board | 대안 A/B/C를 나란히 비교하고 선택 기준을 보여주는 보드형 |
| 10 | `10-governance-operating` | Governance Operating Model | 역할·정책·품질 게이트가 맞물리는 운영 모델 구조 |

권장 모드(참고, 결정 게이트 아님): expert_html·skill_audit(02·07·10 운영/에이전트), education_html·blog_writer(01·08 흐름), comparison_html(09), reference_html(04·06 구조), landing_brief_html(02·05 대표 도판).
