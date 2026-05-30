# Editorial Design System

`adaptive-html-final`은 13개 모드 구조를 유지하되, 출력물은 고급 한국어 기술 블로그/학습지처럼 보여야 한다.

## 디자인 토큰

> 디자인 토큰의 원천(SoT)은 `references/design-dna.md`다. 이 문서는 그 토큰을 참조한다. 토큰 값이 충돌하면 `design-dna.md`를 기준으로 한다.

고정 방향:

- 배경: 따뜻한 오프화이트 `#f5f5f0`
- 본문: 거의 검정 `#1a1a1a`
- 보조 텍스트: `#4a4a4a`, `#7a7a7a`
- 강조: 빨강 `#e63946`
- 카드: 흰색 + 얇은 border
- 그림자: 거의 사용하지 않음
- radius: 5~12px, 과한 pill/round 금지

## 타이포그래피

- H1/H2: `Noto Serif KR`
- 본문: `Pretendard Variable`
- H1: 31~42px, line-height 1.3 이상
- H2: 24~29px, 위쪽 여백 52~64px
- 본문: 15.5px, line-height 1.75~1.8

긴 한국어 제목은 너무 크게 만들면 품질이 떨어진다. “크게”보다 “읽기 좋은 줄바꿈”이 우선이다.

## 섹션 구조

권장 패턴:

```html
<h2><span class="num">1</span>섹션 제목</h2>
<p class="h2-sub">이 섹션에서 독자가 얻게 될 것을 한 줄로 설명한다.</p>
<p>본문...</p>
```

`h2-sub`는 콘텐츠 리듬을 만드는 핵심 장치다. 단, 전 모드 무조건 강제는 아니다(모드 한정 권장). 공개 아티클·블로그·SEO·전문가 리포트 등 주요 h2에는 `<p class="h2-sub">`를 두는 것을 권장한다.

## 의미 박스

### 용어

```html
<div class="term">
  <div class="label">용어</div>
  <span class="word">PKCE (Proof Key for Code Exchange)</span>
  <div class="meaning">인가 코드 탈취를 막기 위한 OAuth 확장...</div>
</div>
```

### 비유

```html
<div class="analogy">
  <div class="label">비유로 이해하기</div>
  <p>추상 개념을 일상 사례로 설명한다.</p>
</div>
```

### 함정/해결

함정은 `.danger`, 해결은 `.good`으로 가능하면 짝지어 쓴다.

```html
<div class="danger"><div class="label">함정</div><div class="name">잘못된 직관</div><p>설명...</p></div>
<div class="good"><div class="label">해결</div><div class="name">권장 패턴</div><p>설명...</p></div>
```

## 강조

- 짧은 용어: `<em class="t">용어</em>`
- 핵심 구절: `<span class="hl">핵심 문장</span>`
- `.hl`은 글당 2~4개만 사용한다.
- 색상 박스 안에는 `.hl`을 쓰지 않는다.

## 출처

본문 끝 출처는 작고 조용해야 한다.

```html
<aside class="source-note">
  <div class="label">출처와 검토 기준</div>
  <p>OWASP, NIST, RFC 문서를 검토해 작성했습니다.</p>
  <p><a href="sources/index.html">전체 출처 링크 모음 보기</a></p>
</aside>
```

출처가 많으면 본문 말미 출처 목록 또는 `sources/index.html` 허브로 분리하고, 허브를 쓸 경우 산출물에서 함께 생성한다. 비존재 파일을 단정적 링크 타깃으로 강제하지 않는다.

## Golden reference

현재 프로젝트 기준 좋은 예시는 `blog-demos/` 계열이다. 특히 다음 특성을 모방한다.

- 차분한 오프화이트 배경
- serif 제목과 sans 본문 조합
- h2 숫자 원 + h2-sub
- 의미 라벨이 있는 term/analogy/danger/good
- 마지막 검정 `.try` 박스
- source-note로 낮춘 출처

## Box 선택 가이드 (언제 무엇을)

| 박스 | 클래스 | 언제 쓰나 |
|---|---|---|
| 용어 | `.term` | 영어 약자·전문 용어가 처음 등장할 때. 단락에 끼우기보다 직후 별도 박스로. |
| 비유 | `.analogy` | 추상 개념을 도서관·신입사원·요리 등 일상 사례로 풀 때. 첫 줄 비유 도입, 둘째 줄 약점/반전. |
| 함정 | `.danger` | 흔한 실수·안티패턴·잘못된 직관. "이걸 조심하라" 신호. |
| 해결 | `.good` | 함정 박스 직후 짝으로, 또는 단독 권장 패턴. 빨강→녹색 짝 사용이 효과적. |
| 영웅 비유 | `.hero-analogy` | 1번 섹션의 핵심 메시지 1개. `<h3>` 안 `<br>`로 두 줄이면 임팩트↑. |
| 일반 카드 | `.card-block` | 색 의미 없는 중립 묶음. 사례·단계가 여러 개일 때 각각 카드로(+`.case-label` "사례 N"). |
| 인용/프롬프트 | `.prompt-box` | 그대로 옮긴 텍스트(예시 프롬프트, 원문 발췌, 명령 출력). 인용은 짧게. |
| 마무리 | `.try` | 마지막 "시도해볼 것" 3~5개. 검정 박스, 번호 리스트만(표 금지). |

### 자주 발생하는 시각 사고 (피할 것)

1. 박스 안에 박스 중첩 — 금지. 한 단계로 평평하게.
2. `.try` 박스에 표 삽입 — 깨짐. 번호 리스트만.
3. `<br>`로 h2 강제 줄바꿈 → 모바일 잘림. 자연 흐름에 맡긴다.
4. 함정 박스 5개 연속 — 무겁다. 사이에 prose/비유를 끼운다.
