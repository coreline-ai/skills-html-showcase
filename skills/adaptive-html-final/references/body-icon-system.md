# Body Icon System

`adaptive-html-final`의 **본문용 compact 아이콘 세트**다. 32종의 인라인 SVG 아이콘으로, 섹션 제목·콜아웃·카드 옆에 **의미를 보조**하는 장식 요소다. 외부/동작 JS 0, `aria-hidden="true"` 장식용, 스킬 디자인 토큰(`--accent`/`--ink-mute`/`--card`/`--hl-yellow`/`--line`)을 그대로 쓴다.

- **자산**: `assets/body-icons.css`(렌더 CSS, `bi-` 네임스페이스) + `assets/body-icons.json`(32종 `{id,label,usage,svg}`)
- **viewBox**: 모든 아이콘 `0 0 40 40`. 클래스: `bi-line`·`bi-accent-line`·`bi-fill`·`bi-soft`·`bi-accent`·`bi-accent-box`·`bi-dot`·`bi-dot-box` (8종)
- **프로파일 무관**: widget/diagram/auto 어느 프로파일에서도 사용 가능(장식 보조). 조건부 인라인(`{{BODY_ICONS_CSS}}` 슬롯).

## 삽입법

`assets/body-icons.json`에서 `id`로 SVG를 찾아 `.body-icon` 래퍼와 함께 삽입한다(장식이므로 항상 `aria-hidden="true"` 유지, 의미는 옆 텍스트가 전달).

```html
<!-- 박스형(기본 42px) -->
<span class="body-icon"><svg viewBox="0 0 40 40" aria-hidden="true">…</svg></span>
<!-- 소형(제목 옆) -->
<span class="body-icon body-icon--sm">…</span>
<!-- 무박스(인라인) -->
<span class="body-icon body-icon--plain">…</span>
```

- **위치**: 섹션 제목(h2/h3) 앞, 콜아웃(term/danger/good) 라벨 옆, 카드 헤더, source-note 라벨 등 **의미가 분명한 곳에만**. 한 화면에 과용 금지(섹션당 1~3개 권장).
- **접근성**: 아이콘은 `aria-hidden="true"`(장식). 의미는 반드시 인접 텍스트로 전달(아이콘만으로 정보 전달 금지). 색 외 단서 유지.
- **반복 금지**: 한 문서의 직접 섹션 h2에 동일 SVG를 전부 반복하지 않는다. 섹션의 정보 역할에 맞춰 최소 4종 이상을 섞고, manual/reference/github/youtube처럼 섹션 기능이 뚜렷한 모드는 각 주요 섹션마다 의미 아이콘을 다르게 고른다.
- **무 JS**: 정적 인라인 SVG만. 애니메이션/호버 동작 JS 금지.

## 32종 카탈로그

| id | 라벨 | 용도(언제) |
|---|---|---|
| `idea` | 핵심 아이디어 | 핵심 통찰·한 문장 결론 |
| `source` | 원문/출처 | 원문 보존·source note |
| `timeline` | 연대기 | 사건 흐름·증류 과정 |
| `connection` | 연결 | 관련 노트·의존 관계 |
| `edit` | 윤문/편집 | before-after·문장 개선 |
| `check` | 체크 | 실행 체크리스트 |
| `impact` | 효과 | 기대 효과·전환 카드 |
| `reference` | 참조 | 레퍼런스·매뉴얼 |
| `warning` | 주의 | 리스크·경고·금지 |
| `success` | 완료 | 통과·성공·확정 |
| `question` | 질문 | 검색 의도·문제 정의 |
| `compare` | 비교 | 선택지·장단점 |
| `decision` | 결정 | 판단 기준·의사결정 |
| `metric` | 지표 | 대시보드·측정 |
| `search` | 검색 | 탐색·리서치 |
| `file` | 파일 | 파일 투어·구조 안내 |
| `code` | 코드 | 구현·예시 코드 |
| `database` | 데이터 | DB·저장소·인덱스 |
| `security` | 보안 | 권한·인증·안전 |
| `user` | 사용자 | 페르소나·대상 |
| `flow` | 흐름 | 프로세스·플로우 |
| `map` | 지도 | 구조도·맵 |
| `quote` | 인용 | 핵심 문장·인용구 |
| `note` | 노트 | 메모·영구노트 |
| `learning` | 학습 | 교육 목표·실습 |
| `platform` | 플랫폼 | 채널 변환·발행 |
| `audit` | 감사 | 검토·품질 게이트 |
| `case` | 사례 | 케이스·회고 |
| `landing` | 랜딩 | 가치 제안·전환 |
| `api` | API | 엔드포인트·계약 |
| `prompt` | 프롬프트 | 입력·튜닝·템플릿 |
| `experiment` | 실험 | 테스트·가설 |

## 모드별 추천 아이콘 (단일 출처 가이드)

| Mode | 추천 아이콘 |
|---|---|
| `beginner_html` | `idea` · `question` · `learning` |
| `expert_html` | `warning` · `decision` · `metric` · `security` |
| `article_html` | `idea` · `quote` · `connection` |
| `education_html` | `learning` · `check` · `timeline` |
| `github_analysis` | `file` · `metric` · `security` · `decision` |
| `blog_writer` | `idea` · `timeline` · `note` |
| `seo_dashboard` | `search` · `question` · `compare` |
| `platform_blog` | `platform` · `edit` · `compare` |
| `skill_audit` | `audit` · `check` · `warning` |
| `reference_html` | `reference` · `api` · `file` · `code` |
| `comparison_html` | `compare` · `decision` · `metric` |
| `case_study_html` | `case` · `timeline` · `impact` |
| `landing_brief_html` | `landing` · `impact` · `success` |
| `checklist_playbook` | `check` · `warning` · `success` · `flow` |

> 콘텐츠 요소 매핑: source-note→`source`, danger/주의→`warning`, good/권장→`success`, 핵심 강조(`.hl`)→`idea`/`quote`, 코드 블록→`code`, 비교표→`compare`, 결정 박스→`decision`. 의미가 모호하면 넣지 않는다(장식 과용 금지).

## 적용 갤러리

**인-스킬 카탈로그**: `galleries/body-icons-catalog.html`(32종 전체 데모 — id·라벨·용도). 스킬 패키지에 동봉된 레퍼런스 데모이며 `assets/body-icons.json`에서 생성된다(생성 출력 아님). `assets/body-icons.css`는 프리미티브 전용으로 유지한다.
