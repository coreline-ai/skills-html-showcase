# github_feature_usage recipe

다음 GitHub 저장소를 `github_feature_usage` 모드의 한국어 HTML 기능·사용 가이드로 정리해줘.

입력:
- 저장소: `https://github.com/<owner>/<repo>`
- 독자: 이 저장소가 어떤 기능을 제공하고 실제로 어떻게 쓸지 빠르게 판단해야 하는 사용자, PM, 도입 검토자
- 프로파일: `auto`
- 가능하면 실제 화면 캡처 또는 스크린샷 경로: `sources/screenshots/*.png`

반드시 포함:

1. 한 줄 positioning: 이 저장소/제품이 무엇을 해주는지.
2. 기능 지도: 사용자 기능, 관리자 기능, 운영 기능, 연동 기능을 최소 4개 카드로 정리.
3. 핵심 기능 설명: `wg-14` Feature Explainer 또는 동등한 기능 설명 뷰.
4. 기술 스택 전체 지도: 프레임워크, 데이터 저장소, 인증/세션, 배포/운영 요소.
5. 아키텍처 심화 분석: 서비스 코어와 어댑터, 외부 연동, 운영 경계.
6. 디렉토리 구조 해부: 주요 폴더와 파일이 어떤 기능을 담당하는지.
7. 실제 화면: 스크린샷 최소 3장, 각 이미지 `alt`와 1문장 caption.
8. 시작 방법: 전제 조건 → 데모 실행 → 실제 연결 → 운영 확인.
9. 적합/부적합 사용처와 도입 전 체크리스트.
10. Source note: 확인한 README/코드/릴리스/화면, 확인 불가 항목, 분석 시각.

작성 규칙:

- `github_analysis`처럼 리스크 실사 중심으로 쓰지 말고, 기능·사용법·도입 이해 중심으로 쓴다.
- 입력에 없는 버전·라이선스·성능·SLA는 `UNKNOWN`으로 남기고 추정하지 않는다.
- 실제 화면이 없으면 스크린샷 섹션을 기능 지도로 대체하고, source note에 "스크린샷 미수집"을 명시한다.
- 외부/동작 JS는 0이다. JSON-LD 외 `<script>` 금지.
- layout은 `github-feature-usage.html`, class는 `.layout-github-feature`를 사용한다.
- `base.html`의 `ahf-theme` 8테마 라디오 스위처를 유지한다.
- 번호가 있는 모든 h2는 `body-icon body-icon--sm` → `num` → 제목 순서로 작성하고, `body-icons.css`를 인라인한다.
- 직접 섹션은 카드/뷰 표면을 유지하고, grid는 내부 `repo-*grid` 또는 `feature-*grid` wrapper에만 적용한다.
- `diagram` 또는 `auto` 프로파일이면 1순위 vt 템플릿 `hero-map`을 최소 1회 삽입한다.
- `widget` 또는 `auto` 프로파일이면 필요할 때 `wg-14 Feature Explainer`, `wg-04 Module Map`, `wg-16 Implementation Plan`, `wg-11 Weekly Status`, `wg-08 Clickable Flow` 순서로 보강한다.

출력:
- 단일 HTML 파일.
- 가능하면 `sources/profile.json`, `sources/css-integrity.json`, `sources/adaptive-html-final-manifest.json`까지 남기고 `validate_output.py` OK를 확인한다.
