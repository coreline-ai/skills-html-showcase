# storm-research

Stanford **STORM** 방법론(다관점 질문 + 출처 grounding)을 **cmux 멀티 페인**으로 구현한
딥리서치 오케스트레이터 스킬팩.

> 메인 Opus가 5개 영혼 페인을 직접 만들어 **claude/codex/kimi**에 분산하고, 각 영혼이
> 출처 강제 딥리서치를 수행해 **cmux send**로 메인에 보고한다. 그 뒤 4프롬프트 파이프라인을
> 돌려 `dist/<프로젝트>/index.html` 자체완결 리포트를 만든다.

## 구성

```
storm-research/
├── SKILL.md                  # 메인 오케스트레이터 (/storm-research)
├── install.sh                # ~/.claude/skills 로 5개 심링크
├── references/               # 방법론·정직성·cmux·분배 SSOT 4종
├── souls/                    # 5 영혼 charter (회의·경제·역사·학자·미래)
├── prompts/                  # 4 raw 복붙 프롬프트 (scan·contradict·synth·review)
├── skills/                   # 4 독립 프롬프트 스킬 (단독 호출 가능)
│   ├── storm-scan/  storm-contradict/  storm-synthesize/  storm-review/
├── scripts/                  # lib.sh · spawn-souls · dispatch-soul · collect-souls · build-report.mjs
├── templates/                # soul-brief / report.html / report.schema.json
└── dist/                     # 산출: <slug>/index.html + report.json
```

## 설치

```bash
./install.sh            # 로컬 원본 → 전역 심링크 5개
./install.sh --check    # 상태 점검
./install.sh --remove   # 심링크 제거
```

전역 등록되는 스킬: `storm-research`(메인) · `storm-scan` · `storm-contradict` ·
`storm-synthesize` · `storm-review`(4 독립 프롬프트).

## 사용

cmux 워크스페이스 안에서:

```
/storm-research   <주제>
```

또는 단계별 단독 호출: `/storm-scan` → `/storm-contradict` → `/storm-synthesize` → `/storm-review`.

## 출처 / 정직성

이 스킬은 STORM의 **재해석**(재구현 아님). 논문 보고 수치는 **조직성 +25% / coverage +10%**.

- 논문: https://arxiv.org/abs/2402.14207 (Shao et al., NAACL 2024)
- 코드(MIT): https://github.com/stanford-oval/storm
- **진짜 도구**: https://storm.genie.stanford.edu

4프롬프트 워크플로우는 바이럴 X 스레드(@heynavtoor)에서 유래한 커뮤니티 방법이며, 본 스킬은
그것을 원논문과 비판적 답글(@QuantumTumbler "good workflow, bad hype" / @savivila 교정 등)에
근거해 정직하게 재구성했다. 상세: [`references/provenance.md`](./references/provenance.md).
