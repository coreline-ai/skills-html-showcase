# template-catalog — final_20260604 템플릿 HTML 정본

`templates/final_20260604/`에서 이동한 손검수 템플릿 HTML 4종입니다. `adaptive-html-final`의 현행 examples와는 별개로, 사용자가 직접 검수한 시각 패턴·폭·테마·카탈로그 회귀 확인용 **스킬 내부 디자인 카탈로그**로 보관합니다.

## 파일

- `index.html` — 폴더 진입점 대시보드(허브). 템플릿들을 카드+링크로 모아 브라우저에서 바로 여는 landing_brief 구조.
- `index-standard-width.html` — 기본 폭 종합 완성본. 전 editorial 패턴 + 다이어그램 + 데모 섹션을 포함한 “Skill Template HTML”.
- `index-beginner-width.html` — 초보자 모드1 780px 읽기 폭 변형.
- `index-all-templates-catalog.html` — 전 vt·wg 템플릿 카탈로그. 신선도·가로폭·대비 확인용 단일 HTML.

## 스킬과의 관계

- 이 폴더는 `skills/adaptive-html-final/examples/`처럼 17모드 참조 예제 기준선은 아닙니다.
- 다만 스킬 패턴을 역동기화하거나 회귀를 눈으로 확인할 때 쓰는 공식 보관 위치입니다.
- HTML은 모두 단일 파일로 독립 렌더 가능하며, 로컬 서버 기준 예시는 다음과 같습니다.

```text
http://127.0.0.1:8788/skills/adaptive-html-final/template-catalog/index.html
http://127.0.0.1:8788/skills/adaptive-html-final/template-catalog/index-all-templates-catalog.html
```

## 주의

- 일부 파일에는 과거 `final_20260604` 손제작 클래스와 inline CSS가 남아 있습니다.
- 스킬 생성 정본은 여전히 `assets/`, `references/`, `examples/`이며, 이 카탈로그를 그대로 복사 생성하는 것은 금지합니다.
