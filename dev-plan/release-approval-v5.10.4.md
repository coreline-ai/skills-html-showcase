# Release Approval — adaptive-html-final v5.10.4

- **승인자**: 사용자(kyounghwan.choi) — "1,2 순차 패치 진행 5.10.4 승격은 관련 문서 빠짐 없이 모두 업데이트 해줘" (2026-06-14)
- **이전 버전**: 5.10.3 → **신규 버전**: 5.10.4
- **승인 일자**: 2026-06-14
- **결정 근거**: [dev-plan/implement_20260614_174756.md](./implement_20260614_174756.md) §선행 결정 게이트 — D1=a(코어 CSS 반영), D2=b(5.10.4 승격).

## 범위 (마이크로 레이아웃 정본 계약 + 작성 프로토콜)

실산출물(2026-06-14 Anthropic 6월 뉴스)이 validate/quality/completion을 통과하고도 사용자 눈검수에서 남은 마이크로 레이아웃 결함을 정본으로 승격한다(output 독립 원칙의 의도적 승격).

| Code | 결함 | 반영 | 자산 분류 |
|---|---|---|---|
| M1 | h2 번호 pill 390px 2줄 깨짐 | `theme.css` `white-space:nowrap` | 코어-해시 |
| M4 | cmp-card kicker→title 간격 4px | `visual-html.css` 8px | 조건부 |
| M7 | 인쇄/export reading-progress 섹션 라인 오인 | `print.css` `@media print` 숨김 | 코어-해시 |
| M10 | body-level footer viewport 좌측 붙음 | `theme.css` `body>footer` 본문폭 중앙 | 코어-해시 |
| M2·M3·M6·M9 | 비정본 클래스 발명에 의한 접착·단조 | 작성 프로토콜 문서화(정본 컴포넌트 사용) | 비-CSS |

## 파급 / 정합 처리

- 코어(theme/print) 해시 갱신 → examples 18종 재인라인 + `sources/css-integrity.json` + source manifest 동기화 + `.skill` 재패키징.
- 버전 표면 전면 갱신(현행만): manifest(version·examples.version·changes·releases·updated·purpose), SKILL.md 헤더, CHANGELOG, README(root·skill), AGENTS, Guide, references/visual-html-system, add-mode-runbook, examples visible meta/footer, 출하 예제 내 구버전 CSS 주석 버전 태그 제거.
- 과거 changelog 헤딩·감사 기록·게이트 도입 버전 마커(`Gate X (v5.10.3)` 등)는 역사적 기준선으로 보존(AGENTS §2.1 governance 원칙).
- 거버넌스 카운트 **159**(build-evidence·render-audit 게이트 포함; M-CSS는 코어 반영, M2~M6·M9는 작성 프로토콜).
- 무 JS·8테마·17모드 산출 계약 불변.
