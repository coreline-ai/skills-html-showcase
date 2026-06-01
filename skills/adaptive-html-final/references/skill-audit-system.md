# Skill Audit System

진단 기준:

1. 목적 명확성
2. 트리거 정확성
3. 입력/출력 명확성
4. 워크플로우 실행 가능성
5. 금지 규칙과 안전 경계
6. 실패 대응
7. 품질 게이트
8. 완료 기준
9. 예시 프롬프트
10. 패키지 구조
11. progressive disclosure 설계
12. assets/references/scripts 분리 적절성

## Output shape

- Executive diagnosis
- Score table
- Line/section findings
- 개선 우선순위
- 최종 개선본 또는 패치 계획
- 검증 체크리스트

## 발췌·예시 출력 표기 규칙 (세부)

- **SKILL.md / 마크다운 / 코드 원문·개선본 발췌는 코드 블럭으로 표기한다.** `.prompt-box`의 `<p>`+`<br>` 텍스트가 아니라 `md-excerpt` 패턴(`<figure class="md-excerpt"><figcaption class="case-label">…발췌 · SKILL.md</figcaption><pre class="code"><code>…</code></pre></figure>`)을 써서, `##`·`-`·`1.`·`name:` 같은 **마크다운 문법이 실제 소스처럼 보이게** 한다(editorial-pattern-system.md 참조). `<br>`이 아닌 실제 줄바꿈으로 작성.
- **"좋은 출력은 어떻게 생겼나" 같은 주석 달린 PR/diff 예시는 wg-03(Annotated PR) 위젯**을 쓴다. diff 코드는 다크 패널(`var(--code)`)에 밝은 텍스트로 보여야 하며(코어 `code{}` 밝은 배경이 덮지 않게 `.wg-03-code{background:none}` 유지), diff(좌)와 리뷰 노트(우)는 `align-items:stretch`로 **같은 높이로 통일**(틈 없이)한다.
