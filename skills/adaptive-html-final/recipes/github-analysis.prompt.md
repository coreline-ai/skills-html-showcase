# github_analysis recipe

다음 GitHub 저장소를 `github_analysis` 모드의 한국어 HTML 리포트로 분석해줘.

입력:
- 저장소: `https://github.com/<owner>/<repo>`
- 독자: 이 저장소를 도입/학습/감사할지 판단해야 하는 개발자 또는 기술 리더
- 프로파일: `auto`

반드시 포함:

1. 한 줄 verdict: 사용 / 검토 / 보류 / 대체 탐색 중 권장 행동.
2. 질문 중심 목차: 무엇인가, 바로 실행 가능한가, 어디부터 볼까, 살아 있는가, 리스크는 무엇인가, 다음 행동은 무엇인가.
3. Repo identity: owner/repo, 목적, 주요 언어, topics, license, default branch, archive 여부.
4. Quickstart readiness: README 설치/실행/예제/환경 요구사항과 재현 가능성.
5. Repo health: 최근 커밋/릴리스/이슈/PR/기여자/CI·테스트 흔적.
6. Code tour: README, src, docs, tests, CI, security/license 관련 파일 투어.
7. Risk matrix: 라이선스 불명확, 릴리스 부재, 테스트/CI 부재, stale issue 등 채택 리스크.
8. Final decision: 내가 다음에 해야 할 30분 검토/1일 POC/보류 체크리스트.
9. Source note: 분석 기준 시각, 확인한 GitHub 표면, API/접근 한계, 확인 불가 항목.
10. 최신 시각 계약: 상단 라이트/화이트/다크 스위처, `generated-row`/`lens-strip` 헤더, 번호형 h2 앞 body icon, 섹션 카드/뷰 표면.

작성 규칙:

- FACT / INFERENCE / UNKNOWN을 분리한다.
- GitHub에서 확인할 수 없는 보안 설정, 실제 취약점, 비공개 로드맵은 단정하지 않는다.
- README 문구를 그대로 홍보 문구처럼 반복하지 말고 사용자의 의사결정 질문으로 재구성한다.
- 외부/동작 JS는 0이다. JSON-LD 외 `<script>` 금지.
- layout은 `github-analysis.html`, class는 `.layout-github`를 사용한다.
- `base.html`의 `ahf-theme` 라디오 3개 스위처를 유지한다.
- header에는 `generated-row`와 `lens-strip`를 넣는다.
- 번호가 있는 모든 h2는 `body-icon body-icon--sm` → `num` → 제목 순서로 작성하고, `body-icons.css`를 인라인한다.
- `.layout-github>section` 카드/뷰 표면을 유지하고 grid는 내부 `repo-*grid` wrapper에만 적용한다.
- `diagram` 또는 `auto` 프로파일이면 1순위 vt 템플릿 `hero-map`을 최소 1회 삽입한다.
- `widget` 또는 `auto` 프로파일이면 필요할 때 `wg-11 Weekly Status`, `wg-04 Module Map`, `wg-14 Feature Explainer`, `wg-16 Implementation Plan` 순서로 보강한다.

출력:
- 단일 HTML 파일.
- 가능하면 `sources/profile.json`, `sources/css-integrity.json`, `sources/adaptive-html-final-manifest.json`까지 남기고 `validate_output.py` OK를 확인한다.
