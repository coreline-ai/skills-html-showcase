# Mode Build Sheet — beginner_html

- mode: `beginner_html`
- topic: 패스키 로그인을 처음 이해하는 사람을 위한 안내
- profile: `auto`
- layout: `assets/layouts/beginner-learning.html`
- primary vt: `concept-explainer`
- wg candidates: wg-10, wg-13, wg-15
- page: `pages/12_beginner_passkey_login_guide.html`

## Sections
1. 한 문장 이해
2. 비밀번호와 차이
3. 기기 안의 열쇠
4. 로그인 흐름
5. 분실하면 어떻게 되나
6. 피싱에 강한 이유
7. 서비스 도입 전 확인
8. 사용자 안내 문구
9. 자주 묻는 질문
10. 오늘 해볼 일

## Template mapping

| Section | Pattern |
|---:|---|
| 1 | 한 문장 이해 → layout scaffold |
| 2 | 비밀번호와 차이 → vt-concept-explainer |
| 3 | 기기 안의 열쇠 → lede-note/source-note |
| 4 | 로그인 흐름 → wg widget |
| 5 | 분실하면 어떻게 되나 → editorial rail card |
| 6 | 피싱에 강한 이유 → layout scaffold |
| 7 | 서비스 도입 전 확인 → vt-concept-explainer |
| 8 | 사용자 안내 문구 → lede-note/source-note |
| 9 | 자주 묻는 질문 → wg widget |
| 10 | 오늘 해볼 일 → editorial rail card |

## Visual risks

- 390px에서 h2 번호 pill 줄바꿈 금지
- rail 텍스트 좌측 접착 금지
- footer 좌측 붙음 금지
- 비정본 클래스 `template-card-head`/`source-preserve-static` 금지

## Stop condition

validate/quality/completion/render-audit 중 하나라도 실패하면 다음 모드로 넘어가지 않는다.
