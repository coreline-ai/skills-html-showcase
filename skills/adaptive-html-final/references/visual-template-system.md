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
  "title": "13개 모드별 최적 이미지 타입",
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
python scripts/render_visual_svg.py visual-brief.json output/media/visual.svg
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
