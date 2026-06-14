# Mode Build Sheet — github_analysis

- mode: `github_analysis`
- topic: Postgres 백업 자동화 저장소 도입 실사
- profile: `auto`
- layout: `assets/layouts/github-analysis.html`
- primary vt: `hero-map`
- wg candidates: wg-11, wg-04, wg-14, wg-16, wg-17, wg-18
- page: `pages/05_github_analysis_pg_backup_due_diligence.html`

## Sections
1. 도입 결론
2. 저장소 신호
3. 기능 범위
4. 아키텍처 흔적
5. 릴리스와 유지보수
6. 보안·라이선스
7. 운영 리스크
8. 대체안 비교
9. 파일 투어
10. 채택 조건

## Template mapping

| Section | Pattern |
|---:|---|
| 1 | 도입 결론 → layout scaffold |
| 2 | 저장소 신호 → vt-hero-map |
| 3 | 기능 범위 → lede-note/source-note |
| 4 | 아키텍처 흔적 → wg widget |
| 5 | 릴리스와 유지보수 → editorial rail card |
| 6 | 보안·라이선스 → layout scaffold |
| 7 | 운영 리스크 → vt-hero-map |
| 8 | 대체안 비교 → lede-note/source-note |
| 9 | 파일 투어 → wg widget |
| 10 | 채택 조건 → editorial rail card |

## Visual risks

- 390px에서 h2 번호 pill 줄바꿈 금지
- rail 텍스트 좌측 접착 금지
- footer 좌측 붙음 금지
- 비정본 클래스 `template-card-head`/`source-preserve-static` 금지

## Stop condition

validate/quality/completion/render-audit 중 하나라도 실패하면 다음 모드로 넘어가지 않는다.
