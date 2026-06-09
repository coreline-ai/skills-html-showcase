# GitHub Analysis System

`github_analysis` 모드는 GitHub 저장소 URL 또는 `owner/repo` 입력을 사용자가 가장 궁금해하는 질문 중심의 HTML 실사 리포트로 바꾼다. 목표는 “저장소 소개”가 아니라 “내가 이 저장소를 어떻게 판단하고 다음에 무엇을 해야 하는가”다.

## 1. 입력과 수집 범위

권장 입력:

- `https://github.com/<owner>/<repo>`
- `<owner>/<repo>`
- GitHub README, 릴리스 노트, 이슈/PR 요약, 파일 트리, 커밋 활동 메모

가능하면 확인할 GitHub 표면:

| 표면 | 확인 항목 | 리포트 쓰임 |
|---|---|---|
| Repository metadata | description, topics, stars/forks/watchers, default branch, archived/disabled 여부 | repo identity, maturity signal |
| README / docs | 설치, quickstart, examples, screenshots, supported platforms | quickstart readiness |
| Contents / file tree | package manifest, src, tests, docs, CI, security, license, layer boundaries | stack map, architecture map, file tour |
| Releases / tags | 최근 릴리스, 버전 규칙, changelog | maintenance, adoption risk |
| Issues / PRs | open/closed 흐름, stale 여부, maintainer response | governance and support signal |
| Contributors / commits | 최근 커밋, contributor spread | bus factor inference |
| Community profile | license, contributing, code of conduct, security policy | trust and governance |
| Languages / dependencies | 주요 언어, lockfile, package metadata | stack and supply-chain hint |

주의: GitHub UI/API로 보이지 않는 조직 내부 보안 설정, 실제 취약점 존재, 비공개 로드맵, maintainer 의도는 단정하지 않는다.

## 2. 사용자 질문형 목차

기본 목차는 공급자 문서 구조가 아니라 독자 질문으로 만든다.

1. **한 줄 결론** — 사용/검토/보류/대체 탐색 중 무엇인가?
2. **이 저장소는 무엇인가** — 목적, 대상 사용자, 핵심 가치.
3. **바로 실행 가능한가** — 설치/quickstart/예제/환경 요구사항.
4. **어디부터 읽으면 되는가** — README, src, docs, tests, config, CI. 복잡한 저장소는 `CODE_TOUR` 안에 Repo Anatomy Pack(기술 스택 전체 지도 → 아키텍처 심화 분석 → 디렉터리 구조 해부)을 포함한다. 디렉터리/파일 투어와 `references 투어`처럼 **짧은 항목이 6개 이상인 평면 목록은 `<ul class="col-list">`(다단 그리드)로 렌더**해 세로 1열 적층의 빈 공간을 없앤다(editorial-pattern-system.md `.col-list`).
5. **살아 있는 프로젝트인가** — 최근 커밋, 릴리스, 이슈/PR 응답, contributor spread.
6. **채택 리스크는 무엇인가** — 라이선스, security policy, test/CI, stale activity, dependency hints.
7. **내 다음 행동은 무엇인가** — 30분 검토, 1일 POC, 보류, 대체안 탐색 체크리스트.

## 3. 판단 모델

점수는 보조 정보다. 별점 같은 인기 지표보다 재현성과 유지보수 신호를 우선한다.

| 영역 | 권장 가중 | 판단 질문 |
|---|---:|---|
| Purpose fit | 15 | 내가 풀려는 문제와 README/설명이 직접 맞는가? |
| Quickstart readiness | 20 | 10~30분 안에 설치/예제를 재현할 수 있는가? |
| Code map clarity | 15 | 주요 파일/디렉터리, 기술 계층, 실행 진입점, 검증 경로를 찾을 수 있는가? |
| Maintenance signal | 20 | 최근 커밋/릴리스/이슈 응답이 살아 있는가? |
| Governance trust | 15 | license, contributing, security policy, CI/test 흔적이 있는가? |
| Adoption risk | 15 | stale, no release, no tests, unclear license 같은 차단 리스크가 있는가? |

점수 카드에는 항상 근거를 함께 쓴다. 근거가 없으면 `확인 불가`로 둔다.

## 4. FACT / INFERENCE / UNKNOWN 규칙

| 타입 | 정의 | 문장 예시 |
|---|---|---|
| FACT | 입력이나 GitHub 표면에서 직접 확인한 사실 | “README에는 Docker quickstart가 있다.” |
| INFERENCE | 관측 사실에서 합리적으로 도출한 판단 | “최근 6개월 릴리스가 없으므로 외부 채택 전 POC 검증이 필요하다.” |
| UNKNOWN | 접근권한/자료 부족으로 확인할 수 없는 것 | “비공개 보안 알림 설정 여부는 확인할 수 없다.” |

금지:

- “취약점 없음”, “안전함”, “프로덕션 검증 완료”처럼 외부에서 확인할 수 없는 보안/품질 단정.
- star 수만으로 품질을 단정.
- README 문구를 사실 검증 없이 제품 약속으로 재표현.

## 5. HTML 구성 계약

레이아웃: `assets/layouts/github-analysis.html` / class `.layout-github`

필수 블록:

```text
GENERATED_ROW
VERDICT
QUESTION_TOC
REPO_IDENTITY
QUICKSTART_READINESS
REPO_HEALTH
CODE_TOUR
RELEASES_AND_ROADMAP
SECURITY_AND_LICENSE
RISK_MATRIX
FINAL_DECISION
NEXT_ACTIONS
SOURCE_NOTE
```

권장 클래스:

- `.repo-signal-grid` — 3열 신호 카드.
- `.repo-identity-grid` — owner/repo, license, default branch, topics.
- `.repo-health-grid` — activity, release, issue/PR, contributors, tests/CI.
- `.repo-evidence-grid` — 핵심 판단별 근거 카드.
- `.repo-unknown` — 확인 불가 또는 자료 부족 카드.
- `.repo-score` — 보조 점수 pill. 점수 단독 사용 금지.

시각 계약:

- `base.html`의 `ahf-theme` 라디오 3-세그먼트 스위처를 유지한다. `theme-dark.css`만 있고 전환 버튼이 없으면 실패다.
- 헤더는 `generated-row` + `lens-strip`를 포함해 최신 13-topics 헤더 리듬과 맞춘다.
- 질문형 목차는 공식 카탈로그의 `toc-map` chip-nav 계약을 따른다. 레이아웃 wrapper는 `toc-map github-question-toc`, 내부는 `span.label` + 설명 `p` + `.toc-pills` + `a.toc-pill > b` 구조이며, 구형 `.toc`/`ol` 목차나 bare link 목차는 회귀다.
- 번호가 있는 모든 섹션 `h2`는 `body-icon body-icon--sm`을 번호 앞에 둔다. 예: `body-icon` → `num` → 제목.
- `body-icons.css`를 조건부 자산으로 인라인하고 `sources/assets/body-icons.css`와 `css-integrity.json`에도 기록한다.
- `.layout-github>section`은 카드/뷰 표면으로 감싸되, 내부 grid wrapper(`repo-*grid`)에만 grid를 적용한다.

### CODE_TOUR 하위 패턴: Repo Anatomy Pack

복잡한 저장소(플러그인/스킬/어댑터/평가 스크립트/멀티 런타임처럼 계층이 많은 구조)는 `CODE_TOUR` 섹션 안에 다음 3개 블록을 순서대로 넣는다. 새 `wg-*`/`vt-*` 번호를 만들지 않고 기존 자산과 editorial 패턴만 조합한다.

1. **기술 스택 전체 지도**
   - 목적: 언어·프레임워크 나열이 아니라 `지식 계층 / 통합 계층 / 검증 계층 / 설정 계층`처럼 저장소가 움직이는 계층을 보여준다.
   - 구조: `<div class="table-scroll"><table>...</table></div>`를 기본으로 쓰고, `<caption>`은 필수다.
   - 열 권장: `계층`, `구성 요소`, `기술/형식`, `역할`, `근거`.
   - 보조: 핵심 계층 3개만 요약할 때는 `.repo-evidence-grid` + `.repo-evidence`를 사용한다.

2. **아키텍처 심화 분석**
   - 목적: 입력이 어떤 통합 계층을 지나 지식/검증 계층으로 이동하고 어떤 결과를 만드는지 설명한다.
   - 구조: `.repo-evidence-grid`로 설계 패턴/흐름/리스크 카드를 배치한다. 모듈 의존이 실제로 중요할 때만 `wg-04 Module Map`을 추가한다.
   - 대표 도판이 필요하면 `workflow-figure` + `assets/workflow-svgs/04-layered-stack.svg`를 섹션 상단에 둔다. 핵심 정보는 반드시 HTML 텍스트/표로 반복해 이미지 내부 라벨에 의존하지 않는다.

3. **디렉터리 구조 해부**
   - 목적: 단순 tree dump가 아니라 `폴더 → 역할 → 읽는 이유 → 주의점`을 연결한다.
   - 구조: `vt-file-tour`를 우선 사용하고, 실제 tree가 필요한 경우 `md-excerpt` 또는 `.code` 블록으로 보존한다.
   - README에 있는 파일 트리가 실제 contents와 다르면 `FACT`로 차이를 적고, 오래된 tree는 `UNKNOWN`/한계로 분리한다.

작성 금지:

- `wg-21`, `vt-22`처럼 새 번호를 임의로 만들지 않는다.
- `.repo-stack-*`, `.repo-architecture-*` 같은 새 CSS 네임스페이스를 즉흥 추가하지 않는다. 새 CSS가 필요하면 별도 패치에서 `layouts.css` 코어 해시·스냅샷·검증을 함께 갱신한다.
- 기술 스택을 인기 기술 키워드 목록으로만 나열하지 않는다. 각 항목은 파일/README/package manifest 같은 근거와 연결한다.

## 6. vt-/wg- 선택

프로파일별 선택은 SKILL.md §0.6이 단일 출처다.

| 라이브러리 | 우선순위 | 쓰임 |
|---|---|---|
| vt-hero-map | 1 | 목적 → 신호 → 권장 행동 요약 |
| vt-quality-gate | 2 | 채택 전 최소 검증 기준 |
| vt-file-tour | 3 | README/src/tests/docs/CI/security 파일 투어, 디렉터리 구조 해부 |
| vt-risk-matrix | 4 | 채택 리스크 우선순위 |
| vt-timeline | 5 | 커밋/릴리스/이슈 흐름 |
| vt-decision-tree | 6 | 사용/검토/보류/대체 탐색 판단 |
| wg-11 Weekly Status | 1 | repo health 지표 요약 |
| wg-04 Module Map | 2 | 모듈/패키지 의존 경로, 아키텍처 심화 분석 보강 |
| wg-14 Feature Explainer | 3 | quickstart/API/CLI 사용법 |
| wg-16 Implementation Plan | 4 | POC/도입 계획 |
| wg-17 PR Writeup / wg-18 Triage Board | 선택 | PR/이슈 흐름이 중요한 경우만 |

## 7. Source note 계약

마지막 `source-note`에는 반드시 다음을 남긴다.

- 분석 기준 시각 또는 “입력 기준”.
- 확인한 GitHub 표면: README, contents, releases, issues, PRs, license 등.
- API/접근 한계: 비인증 60 req/h, 인증 5,000 req/h 같은 rate limit에 걸린 경우 표시.
- 확인 불가 항목: security alerts, private roadmap, internal CI secrets, 실제 취약점 여부 등.
- **공개용 output 기본값**: `sources/`에는 CSS 무결성 스냅샷, manifest, 요약 JSON만 둔다. 분석 대상 저장소 전체 복사본(`sources/<repo>-snapshot/`)은 공개 산출물에 포함하지 않는다. 재현/감사용 전체 snapshot이 필요하면 별도 비공개 output 또는 archive로 분리하고, 공개 HTML에는 `source_preservation_policy: public-output-summary-only` 같은 메타데이터만 남긴다.

## 8. 완료 게이트

- `h1`은 하나, `<main id="main" class="page-wide layout-github">` 유지.
- 헤더 `generated-row`/`lens-strip`, 테마 스위처, 번호 앞 body icon을 유지.
- 외부/동작 JS 0.
- 핵심 표에는 visible `<caption>`.
- `repo-*grid`는 내부 wrapper에만 적용하고 semantic section 자체에 grid를 직접 걸지 않는다.
- 리스크/상태는 색 외 라벨을 병기한다.
- 긴 URL/패키지명/commit SHA는 `overflow-wrap:anywhere` 가능한 컴포넌트 안에 둔다.
- `UNKNOWN`을 단점처럼 벌점화하기보다 한계로 분리한다.
- 공개용 output에는 분석 대상 저장소 전체 snapshot 디렉터리를 포함하지 않는다. 필요한 경우 요약 JSON·파일 목록·커밋 SHA·확인한 표면만 남긴다.
