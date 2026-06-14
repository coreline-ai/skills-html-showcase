# Mode Build Sheet — github_feature_usage

- mode: `github_feature_usage`
- topic: 오픈소스 인증 모듈 기능·사용법 가이드
- profile: `auto`
- layout: `assets/layouts/github-feature-usage.html`
- primary vt: `hero-map`
- wg candidates: wg-14, wg-04, wg-16, wg-11, wg-08
- page: `pages/06_github_feature_usage_auth_module.html`

## Sections
1. 무엇을 해결하나
2. 핵심 기능 지도
3. 설치 전 조건
4. 첫 실행 흐름
5. 설정 파일 해석
6. 관리자 기능
7. 사용자 기능
8. 확장 포인트
9. 실제 화면 읽기
10. 도입 전 체크

## Template mapping

| Section | Pattern |
|---:|---|
| 1 | 무엇을 해결하나 → layout scaffold |
| 2 | 핵심 기능 지도 → vt-hero-map |
| 3 | 설치 전 조건 → lede-note/source-note |
| 4 | 첫 실행 흐름 → wg widget |
| 5 | 설정 파일 해석 → editorial rail card |
| 6 | 관리자 기능 → layout scaffold |
| 7 | 사용자 기능 → vt-hero-map |
| 8 | 확장 포인트 → lede-note/source-note |
| 9 | 실제 화면 읽기 → wg widget |
| 10 | 도입 전 체크 → editorial rail card |

## Visual risks

- 390px에서 h2 번호 pill 줄바꿈 금지
- rail 텍스트 좌측 접착 금지
- footer 좌측 붙음 금지
- 비정본 클래스 `template-card-head`/`source-preserve-static` 금지

## Stop condition

validate/quality/completion/render-audit 중 하나라도 실패하면 다음 모드로 넘어가지 않는다.
