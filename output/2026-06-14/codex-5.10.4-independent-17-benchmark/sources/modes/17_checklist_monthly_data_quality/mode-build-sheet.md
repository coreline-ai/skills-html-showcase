# Mode Build Sheet — checklist_playbook

- mode: `checklist_playbook`
- topic: 월말 데이터 품질 점검 플레이북
- profile: `auto`
- layout: `assets/layouts/checklist-playbook.html`
- primary vt: `checklist-flow`
- wg candidates: wg-11, wg-13, wg-16, wg-18, wg-19
- page: `pages/17_checklist_monthly_data_quality.html`

## Sections
1. 플레이북 결론
2. 시작 전 준비
3. 소유자 확인
4. 스키마 점검
5. 누락값 점검
6. 중복 레코드
7. 품질 게이트
8. 장애 시 분기
9. 승인 기록
10. 완료 보고

## Template mapping

| Section | Pattern |
|---:|---|
| 1 | 플레이북 결론 → layout scaffold |
| 2 | 시작 전 준비 → vt-checklist-flow |
| 3 | 소유자 확인 → lede-note/source-note |
| 4 | 스키마 점검 → wg widget |
| 5 | 누락값 점검 → editorial rail card |
| 6 | 중복 레코드 → layout scaffold |
| 7 | 품질 게이트 → vt-checklist-flow |
| 8 | 장애 시 분기 → lede-note/source-note |
| 9 | 승인 기록 → wg widget |
| 10 | 완료 보고 → editorial rail card |

## Visual risks

- 390px에서 h2 번호 pill 줄바꿈 금지
- rail 텍스트 좌측 접착 금지
- footer 좌측 붙음 금지
- 비정본 클래스 `template-card-head`/`source-preserve-static` 금지

## Stop condition

validate/quality/completion/render-audit 중 하나라도 실패하면 다음 모드로 넘어가지 않는다.
