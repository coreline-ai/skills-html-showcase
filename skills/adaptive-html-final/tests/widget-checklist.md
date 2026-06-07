# Widget Checklist

뷰 위젯 시스템(`assets/widgets.css` + `assets/widget-templates/*.html` 20종)의 무 JS·네임스페이스·접근성 게이트.
스킬 루트(`skills/adaptive-html-final`)에서 아래 명령을 실행해 자동 검증한다. 기대값과 다르면 회귀로 간주한다.

## 1. 외부/동작 JS 0건 (위젯 자산 전체)

```bash
# 동작용 <script>가 있는 위젯 파일 목록(있으면 출력됨, 메타데이터 JSON-LD만 예외 허용)
grep -rl '<script' assets/widgets.css assets/widget-templates 2>/dev/null \
  | xargs grep -L 'application/ld+json' 2>/dev/null
# 기대값: 출력 0줄

# 인라인 이벤트 핸들러도 0건
grep -roE 'on(click|input|change|load|mouseover|keydown|keyup|submit)=' assets/widget-templates | wc -l
# 기대값: 0
```

- [ ] `widgets.css`와 `widget-templates/*.html`에 동작용 `<script>`/외부 JS가 0건이다.
- [ ] `onclick` 등 인라인 이벤트 핸들러가 0건이다.

## 2. `wg-<id>-` 네임스페이스 충돌 0건

```bash
# 위젯 CSS 셀렉터가 wg-NN 네임스페이스 밖으로 새는지(있으면 출력됨)
grep -oE '\.wg-[a-z0-9-]+' assets/widgets.css | grep -vE '^\.wg-[0-9]{2}' | sort -u
# 기대값: 출력 0줄

# 네임스페이스 종류가 정확히 20종(wg-01 ~ wg-20)
grep -oE 'wg-[0-9]{2}' assets/widgets.css | sort -u | wc -l
# 기대값: 20
```

- [ ] 모든 위젯 셀렉터가 `wg-<id>-`(2자리) 네임스페이스 안에 있다(네임스페이스 밖 `.wg-` 0건).
- [ ] 네임스페이스가 `wg-01`~`wg-20` 정확히 20종이고 theme/components/layouts 클래스와 충돌하지 않는다.

## 3. 인터랙션은 details / :checked / :target / CSS-anim만

```bash
# 허용 외 인터랙션 원시요소(있으면 출력됨)
grep -roE 'contenteditable|draggable="true"|<dialog' assets/widget-templates
# 기대값: 출력 0줄

# 인터랙티브 위젯은 허용 기법(<details> / :checked radio·checkbox / :target href="#wg-" /
#   @keyframes·animation)만 쓴다. 정적 위젯(04·10·16 등)은 인터랙션이 없어도 통과다 —
#   금지된 것은 "허용 외 인터랙션"뿐이다. 아래는 인터랙티브 위젯이 허용 기법을 쓰는지 표시한다.
for f in assets/widget-templates/*.html; do
  echo -n "$(basename "$f"): "
  if grep -qE '<details|type="(radio|checkbox)"|href="#wg-|@keyframes|animation:' "$f"; then
    echo "interactive(allowed CSS primitive)"
  else
    echo "static(ok — 인터랙션 없음, 금지요소 없으면 통과)"
  fi
done
# 기대값: 모든 파일이 interactive(allowed...) 또는 static(ok...). 그 외 출력 없음.
```

- [ ] 인터랙션은 `<details>/<summary>`, `:checked`(radio/checkbox+label), `:target`(`href="#wg-"` 앵커), CSS 애니메이션/transition만 사용한다.
- [ ] `contenteditable`/`draggable`/`<dialog>` 등 JS 전제 원시요소가 0건이다.
- [ ] `:target` 앵커는 `#wg-` 네임스페이스 id만 가리킨다(오프사이트/외부 점프 없음).

## 4. 색 외 단서 + 포커스 가시성

```bash
# 위젯 CSS에 :focus-visible 포커스 링이 있다
grep -c ':focus-visible' assets/widgets.css
# 기대값: 1 이상

# 모션 위젯이 prefers-reduced-motion 폴백을 가진다
grep -c 'prefers-reduced-motion' assets/widgets.css
# 기대값: 1 이상
```

- [ ] 상태/등급/선택을 색만으로 구분하지 않는다(아이콘·라벨·테두리·글리프 `●◐○`/`✓`/`!`/`⚠` 병기).
- [ ] 인터랙티브 요소(`summary`, label이 제어하는 input, 앵커, `[tabindex]`)에 `:focus-visible` outline이 있다.
- [ ] 애니메이션 위젯이 `@media (prefers-reduced-motion: reduce)`에서 정지+최종 상태로 폴백한다.

## 5. 18·20은 무 JS 근사

JS 없이 완전 인터랙션이 불가능한 18(Ticket Triage Board, 칸반)·20(Prompt Tuner)은
스킬 기본값으로 무 JS 근사(정적/`:checked` 상태)로 삽입한다. 실시간 동작은 선택적 점진 향상으로만 둔다.

```bash
# 18, 20 템플릿에 동작용 <script>가 0건
echo -n "18: "; grep -c '<script' assets/widget-templates/18-ticket-triage-board.html
echo -n "20: "; grep -c '<script' assets/widget-templates/20-prompt-tuner.html
# 기대값: 둘 다 0
```

- [ ] 18 칸반은 동작용 JS 없이 정적 컬럼 + 우선순위 칩/도트/카운트(색 외 단서)로 핵심 정보를 보여준다.
- [ ] 20 프롬프트 튜너는 동작용 JS 없이 `:checked` 탭 + `{{...}}` 변수 강조로 샘플을 보여준다.
- [ ] 18·20을 무 JS 상태로 삽입했음을 캡션/주석으로 밝히고, 드래그·실시간 치환은 선택적 점진 향상으로만 추가한다.

## 6. 인터랙티브 분류 집계 (11 / 7 / 2)

```bash
# 템플릿 헤더 주석의 분류 라벨 집계
for f in assets/widget-templates/*.html; do grep -oE 'css-only|css-partial|js-needed' "$f" | head -1; done \
  | sort | uniq -c
# 기대값: css-only 11, css-partial 7, js-needed 2
```

- [ ] CSS-only(완전 무JS) 11종 / CSS 부분 7종 / JS 필요 2종 비율이 유지된다.

## 7. 회귀 규칙: 탭 ARIA & :target-within 폴백

ARIA 탭과 CSS-only `:target` 인터랙션에서 반복 발견된 두 결함을 정적으로 막는다.

### 7-1. `role="tab"` 사용 시 `aria-selected` 필수 / 이중 탭 스톱 금지

`role="tab"`을 붙인 요소는 `aria-selected`(true/false)를 반드시 가진다. 또한 `:checked` radio를 제어하는 `<label>`에 `tabindex`/`role`을 얹으면 input(radio)과 label이 둘 다 탭 스톱이 되어 "이중 탭 스톱"이 생긴다 — radio가 이미 포커스 가능하므로 라벨에서 `tabindex`/`role`을 제거한다.

```bash
# (a) role="tab"인데 같은 태그에 aria-selected가 없는 경우(있으면 출력됨 = 회귀)
grep -roE '<[^>]*role="tab"[^>]*>' assets/widget-templates 2>/dev/null \
  | grep -v 'aria-selected'
# 기대값: 출력 0줄

# (b) radio를 감싸거나 가리키는 <label>에 tabindex 또는 role이 붙은 경우(있으면 출력됨 = 이중 탭 스톱)
grep -roE '<label[^>]*(tabindex|role)=' assets/widget-templates 2>/dev/null
# 기대값: 출력 0줄
```

- [ ] `role="tab"` 요소는 모두 `aria-selected="true|false"`를 가진다(없으면 회귀).
- [ ] `:checked` radio를 제어하는 `<label>`에 `tabindex`/`role`이 없다(radio가 탭 스톱이므로 라벨 중복 금지 = 이중 탭 스톱 금지).

### 7-2. `:target-within` 단독 의존 금지 (`:target` 형제 폴백 필수)

`:target-within`은 지원 범위가 좁다. 이 셀렉터를 쓰는 파일은 동일 파일 안에 일반 `:target` 형제 폴백 규칙을 반드시 함께 둔다. `:target-within`만 단독으로 쓰면 미지원 환경에서 화면 전환이 죽는다.

```bash
# :target-within을 쓰면서 같은 파일에 일반 :target 폴백이 없는 파일(있으면 출력됨 = 회귀)
for f in $(grep -rl ':target-within' assets/widgets.css assets/widget-templates 2>/dev/null); do
  grep -qE ':target([^-]|$)' "$f" || echo "$f"
done
# 기대값: 출력 0줄(:target-within 사용 파일은 전부 :target 폴백을 동반)
```

- [ ] `:target-within`을 쓰는 모든 파일에 일반 `:target` 형제 폴백 규칙이 함께 있다(`:target-within` 단독 의존 0건).


## 신규 모드 위젯 매핑

- youtube_analysis: wg-11/13/14/16/18 기본, wg-15/20 조건부.
- manual_analysis: wg-04/13/16/18/11/14 기본.
- 두 모드 모두 wg-NN 네임스페이스 밖의 임의 widget-* 클래스 금지.
