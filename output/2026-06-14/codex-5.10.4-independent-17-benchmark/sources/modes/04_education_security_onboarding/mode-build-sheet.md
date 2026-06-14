# Mode Build Sheet — education_html

- mode: `education_html`
- topic: 사내 보안 온보딩 90분 실습 과정
- profile: `auto`
- layout: `assets/layouts/course-module.html`
- primary vt: `timeline`
- wg candidates: wg-06, wg-07, wg-08, wg-13, wg-14, wg-15, wg-20
- page: `pages/04_education_security_onboarding.html`

## Sections
1. 학습 목표
2. 선수 지식
3. 위협 모델 빠른 지도
4. 실습 환경 준비
5. 피싱 판별 훈련
6. 권한 최소화 실습
7. 로그 해석 과제
8. 퀴즈와 해설
9. 현업 적용 체크
10. 다음 학습 경로

## Template mapping

| Section | Pattern |
|---:|---|
| 1 | 학습 목표 → layout scaffold |
| 2 | 선수 지식 → vt-timeline |
| 3 | 위협 모델 빠른 지도 → lede-note/source-note |
| 4 | 실습 환경 준비 → wg widget |
| 5 | 피싱 판별 훈련 → editorial rail card |
| 6 | 권한 최소화 실습 → layout scaffold |
| 7 | 로그 해석 과제 → vt-timeline |
| 8 | 퀴즈와 해설 → lede-note/source-note |
| 9 | 현업 적용 체크 → wg widget |
| 10 | 다음 학습 경로 → editorial rail card |

## Visual risks

- 390px에서 h2 번호 pill 줄바꿈 금지
- rail 텍스트 좌측 접착 금지
- footer 좌측 붙음 금지
- 비정본 클래스 `template-card-head`/`source-preserve-static` 금지

## Stop condition

validate/quality/completion/render-audit 중 하나라도 실패하면 다음 모드로 넘어가지 않는다.
