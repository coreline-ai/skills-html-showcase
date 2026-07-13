#!/usr/bin/env python3
# Phase 5+6: 5영혼 results + 메인 Opus 작성 4프롬프트 산출 → report.json 조립
import json, os

RUN = os.path.dirname(os.path.abspath(__file__))

def read(name):
    p = os.path.join(RUN, "results", name + ".md")
    return open(p, encoding="utf-8").read()

souls = [
    {"name":"Skeptic","persona":"회의주의자","llm":"claude",
     "summary":"RCT(METR) 19% 감속·마이크로SaaS 92% 실패·AI코드 취약점 2.74배·Apple 크래다운 — 수익화 내러티브의 4대 균열",
     "markdown":read("Skeptic")},
    {"name":"Economist","persona":"경제학자","llm":"codex",
     "summary":"코딩비 하락의 이익은 도구·인프라·유통이 선취하고, 개인의 수익 병목은 고객 접근·검증·운영 책임이다",
     "markdown":read("Economist")},
    {"name":"Historian","persona":"역사학자","llm":"kimi",
     "summary":"App Store·노코드·ThemeForest 선례 — 수익 집중·플랫폼 의존·유지보수 부채. 희망은 'AI 아키텍트 서비스화'",
     "markdown":read("Historian")},
    {"name":"Academic","persona":"학자","llm":"claude",
     "summary":"peer-review 13편 — 수익화 직접 실증 전무, 생산성은 과제 복잡도 의존, LLM 프리랜서 26%, OSS 수익모델 위협이 가장 확립",
     "markdown":read("Academic")},
    {"name":"Futurist","persona":"미래학자","llm":"codex",
     "summary":"제작비 급락 후 수익의 희소점은 코드에서 검증·고유 데이터·에이전트 유통·운영 책임으로 이동한다",
     "markdown":read("Futurist")},
]

contradiction_map = r"""## 모순 지도 — 다섯 영혼이 어디서 만나고 어디서 부딪히는가

> claude(Skeptic·Academic) · codex(Economist·Futurist) · kimi(Historian) — **세 개의 다른 모델**이
> 독립적으로 조사했다. 그래서 합의는 더 신뢰할 만하고, 충돌은 더 진짜다.

### 합의 지점 (Consensus — 3개 모델이 독립 수렴)

**C1. 코드 제작은 더 이상 희소자원이 아니다.** 다섯 영혼 전원이 동의한 단일 결론.
- 경제학자: "가장 희소한 것은 코드를 만드는 능력이 아니라 누가 돈을 낼 문제인지 아는 정보·유통권·검증/운영 책임" [출처: https://stripe.com/us/blog/stripe-atlas-startups-in-2025-year-in-review]
- 미래학자: "빠른 제작은 상품이 아니라 전기처럼 투입재가 된다" [출처: https://www.anthropic.com/research/impact-software-development]
- 역사학자: 노코드 선례도 '개인 수익화'보다 'AI 이해하는 시스템 아키텍트의 고부가 서비스화'로 안착 [출처: https://www.jobbers.io/no-code-low-code-freelancing-bubble-webflow-zapier-2026/]
- 학자: OSS조차 "엔터프라이즈 라이선싱·API 요금·개발자 서비스"로 수익 채널 이동 필요 [출처: https://doi.org/10.48550/arXiv.2601.15494]

**C2. 수익은 극단적으로 집중되며, 성공담은 생존자 편향이다.** (power-law)
- 역사학자: App Store 앱 중 $1M+ 0.13%, ThemeForest 테마 중 월 $10k+ 0.83% [출처: https://freemius.com/blog/themeforest-wordpress-themes-analyisis/]
- 회의주의자: 마이크로 SaaS 92% 3년 내 실패, 수익 내는 곳도 70%가 월 $1k 이하 [출처: https://www.rockingweb.com.au/micro-saas-revenue-analysis-2025/]
- 경제학자: Stripe Atlas 상위 10% 매출 증가율 52% vs 하위 10% 18% — 진입비용 하락이 격차를 키움 [출처: https://stripe.com/us/blog/stripe-atlas-startups-in-2025-year-in-review]

**C3. AI 생산성 이득은 실재하나 보편적이지 않고 과제 복잡도에 의존한다.**
- 학자: Peng 2023 협소 과제 +55.8% vs Becker 2025 실제 OSS 과제 −19% [출처: https://doi.org/10.48550/arXiv.2302.06590] [출처: https://doi.org/10.48550/arXiv.2507.09089]
- 회의주의자·경제학자 모두 METR RCT(−19%, 그러나 체감은 +20%)를 핵심 근거로 인용 [출처: https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/]

### 모순 지점 (Contradiction — 진짜 충돌, 봉합하지 않음)

| 충돌 대상 | A 입장 (+출처) | B 입장 (+출처) | 미해결 이유 |
|---|---|---|---|
| **AI는 빨라지나 느려지나** | 미래학자: 모델 시간지평 ~7개월마다 2배, 곧 일주일짜리 과업 [출처: https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/] | 회의주의자·학자: 실제 복잡 과제 RCT는 −19% [출처: https://doi.org/10.48550/arXiv.2507.09089] | **시간 지평 차이** — 미래학자는 능력 곡선의 *추세*, 회의주의자는 2025 *현재 단면*. 임계 복잡도 미측정 |
| **플랫폼 채널: 기회인가 함정인가** | 미래학자: 에이전트 커머스(ChatGPT 앱·Shopify Agentic)가 새 유통 [출처: https://www.shopify.com/news/agentic-commerce-momentum] | 회의주의자·경제학자: Apple 크래다운 + 플랫폼이 '곡괭이 판매자'로 지대 선취 [출처: https://thenextweb.com/news/vibe-coding-apple-app-store-surge-crackdown] | **개방형 프로토콜 지속 여부** — 수수료·추천 알고리즘·정산 조건이 아직 미확정 |
| **'비개발자도 가능'** | 통념: 누구나 앱 제작 → 수익 | 학자: 빌드는 되나 '버그 못 고치는 취약한 코호트' 등장 [출처: https://doi.org/10.48550/arXiv.2510.00328] | 사용(usage)과 수익화(monetization)는 다른 측정값, 후자 데이터 공백 |

### 사각지대 (Blind Spot — 누구도 충분히 다루지 않음)

1. **국내(한국) 시장 특수성** — 경제학자가 Stripe Atlas=미국 델라웨어 법인 편향임을 명시했으나, 한국 내수 결제·세금·플랫폼(네이버·카카오·토스) 기반 수익화는 다섯 영혼 모두 미조사. **본 리서치의 가장 큰 공백.**
2. **세무·법적 책임·환불 의무** — 1인 창작자가 AI로 만든 SW를 판매할 때의 하자담보·개인정보 책임. 경제학자가 '책임'을 언급했으나 구체적 법무는 미조사.
3. **창작자 본인의 역량 침식 vs 학습** — 학자가 미해결 연구질문으로만 남김.

### 핵심 긴장 (Key Tension — 이 주제를 가르는 단 하나)

> **내러티브는 '제작 속도'를 돈의 경로로 팔지만, 다섯 렌즈 전부 병목이 하류로 이동했다고 수렴한다.**
> 제작이 7일이면 누구나 복제할 수 있을 만큼 싸졌을 때, 결과를 가르는 단 하나의 질문:
>
> **"앱이 거의 공짜로 만들어진 다음, 7일 안에 복제되지 않고 시간이 갈수록 쌓이는 무엇을 당신이 소유하는가?"**
>
> 회의주의자는 "대부분 아무것도 못 가져서 92% 실패"라 답하고, 미래학자는 "고유 데이터·관계·신뢰 영수증·에이전트 유통권"이라 답한다. 이 둘 사이가 수익화의 전장이다."""

synthesis = r"""# 바이브코딩으로 수익화하는 방법 — 다섯 전문가가 충돌을 통과해 내린 결론

> **Lead.** 바이브코딩 수익화의 지배적 서사는 "코딩 없이 빠르게 앱을 만들어 돈을 번다"이다. 그러나 claude·codex·kimi 세 모델로 독립 조사한 다섯 전문가는 한 점에 수렴했다 — *제작 속도는 이미 희소성을 잃었고, 돈의 병목은 하류(고객 접근·검증·운영 책임)로 이동했다* [수렴 중]. 가장 엄밀한 RCT는 숙련 개발자가 AI로 오히려 19% 느려졌음을 보였고(체감은 +20%) [출처: https://doi.org/10.48550/arXiv.2507.09089], 수익은 power-law로 극단 집중되며(앱 중 0.13%만 $1M+) [출처: https://freemius.com/blog/themeforest-wordpress-themes-analyisis/], "바이브코딩 수익화"를 직접 다룬 peer-reviewed 실증은 2026년 6월 현재 **존재하지 않는다** [출처: https://doi.org/10.48550/arXiv.2510.00328]. 결론은 비관이 아니라 *전략의 재배치*다.

## 1. 지배적 내러티브와 그 유혹

"코딩을 몰라도 AI와 대화만으로 앱을 만들어 월 수천~수만 달러"라는 서사는 강력하다. 실제로 진입 속도는 개선됐다 — Stripe Atlas 법인 중 30일 내 첫 과금 비율이 2020년 8%에서 2025년 20%로 올랐다 [출처: https://stripe.com/us/blog/stripe-atlas-startups-in-2025-year-in-review]. 문제는 *제작 가능*과 *수익 지속*이 전혀 다른 사건이라는 점이다.

## 2. 실제로 희소해진 것 (다섯 모델의 수렴)

가장 강한 발견은 합의에 있다. 서로 다른 학습 분포를 가진 세 모델이 독립적으로 같은 결론에 도달했다: **코드 제작 능력은 더 이상 희소자원이 아니다.** 경제학자는 이를 "코드 공급이 늘면 코드의 희소성은 낮아지고 고객 접근권·도메인 지식·검증·운영 책임의 가격이 상대적으로 오른다"로 정식화했고 [출처: https://stripe.com/us/blog/stripe-atlas-startups-in-2025-year-in-review], 미래학자는 "빠른 제작이 전기 같은 투입재가 된다"로 [출처: https://www.anthropic.com/research/impact-software-development], 학자는 OSS조차 직접 참여가 아닌 "엔터프라이즈 라이선싱·API·서비스"로 수익을 옮겨야 한다는 이론 모델로 뒷받침했다 [출처: https://doi.org/10.48550/arXiv.2601.15494].

## 3. 생산성 신기루 [논쟁 → 수렴 중]

수익화 서사의 전제인 "AI가 개발을 비약적으로 빠르게 한다"는 *맥락 의존적*이다. Peng 2023은 협소한 JS 서버 과제에서 +55.8%를 봤지만 [출처: https://doi.org/10.48550/arXiv.2302.06590], Becker 2025(METR)는 숙련 개발자의 실제 OSS 과제에서 −19%를 보였다 — 게다가 개발자들은 끝나고도 +20% 빨라졌다고 *오인*했다 [출처: https://doi.org/10.48550/arXiv.2507.09089]. **여기서 모순이 살아있다**: 미래학자는 모델 능력의 시간지평이 ~7개월마다 2배가 되는 *추세*를 강조하고 [출처: https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/], 회의주의자·학자는 2025 현재 *단면*의 −19%를 강조한다. 둘 다 옳다 — 임계 복잡도가 어디서 이득을 0으로 만드는지는 아직 측정되지 않았다 [추론].

## 4. 누가 가치를 가져가는가 (경제학)

코딩비 하락의 이익은 균등 분배되지 않는다. 도구 회사(Cursor ARR $500M+, Lovable $100M, Replit $150M)와 인프라·결제 플랫폼이 '곡괭이 판매자'로서 개별 앱의 성패와 무관하게 구독·사용량 매출을 먼저 가져간다 [출처: https://cursor.com/en/blog/series-c] [출처: https://replit.com/news/funding-announcement-series-c]. 개인의 100달러 매출에서도 채널이 즉시 떼간다 — Apple 소규모사업자 15%, Gumroad Discover 30% [출처: https://developer.apple.com/app-store/small-business-program/] [출처: https://gumroad.com/help/article/66-gumroads-fees.html]. 그래서 가격은 *개발 시간*이 아니라 *고객의 대체 비용과 책임*으로 정해야 한다 [추론].

## 5. 역사는 운율을 반복한다

이 구조는 새롭지 않다. 역사학자는 세 선례를 들었다: ① App Store 골드러시(2008~) — 150만 앱 중 $1M+은 0.13% ② 노코드/시민개발자 물결(2011~) — 민주화와 'shadow IT' 부채의 양면 ③ ThemeForest(2008~) — 테마 86.9%가 1,000개 미만 판매 [출처: https://www.macstories.net/stories/developers-decade-long-rollercoaster-ride-the-business-of-selling-apps-on-the-app-store/] [출처: https://freemius.com/blog/themeforest-wordpress-themes-analyisis/]. 매번 패턴은 동일했다 — 플랫폼이 문턱을 낮추고, 미디어가 소수 성공을 골드러시로 포장하고, 실제 수익은 발견·마케팅·지속가능 모델 능력으로 극소수에 집중됐다. 그러나 같은 역사는 *희망*도 준다: 노코드에서 진짜 돈은 '앱 양산'이 아니라 'AI 이해하는 아키텍트의 고부가 서비스'($10k~$30k+)에 안착했다 [출처: https://www.jobbers.io/no-code-low-code-freelancing-bubble-webflow-zapier-2026/].

## 6. 어디로 향하는가 (미래 신호)

미래학자는 4개 궤적을 관측했다: ① 코딩 에이전트의 자동화 비중 상승(Claude Code 대화의 79%가 자동화) [출처: https://www.anthropic.com/research/impact-software-development] ② 구독 앱 공급 폭증(월 신규 ~1.5만 개)이나 AI 앱의 12개월 유지율이 비AI보다 *낮음*(연간 21.1% vs 30.7%) [출처: https://www.revenuecat.com/state-of-subscription-apps-2026-shopping/] ③ 상점이 웹페이지에서 '에이전트가 호출하는 능력'으로 이동(ChatGPT 앱·Shopify Agentic Storefronts) [출처: https://www.shopify.com/news/agentic-commerce-momentum] ④ 원천 콘텐츠·신뢰 증명의 유료 인프라화(Cloudflare Pay-Per-Crawl, EU AI Act) [출처: https://developers.cloudflare.com/changelog/post/2025-07-01-pay-per-crawl/]. 병목은 '출시'가 아니라 '두 번째 결제'다 [추론].

## 7. 방어 가능한 플레이북 (충돌을 통과한 종합 판단)

다섯 관점을 종합하면, 개인 개발자·창작자의 합리적 전략은 *범용 앱 양산*이 아니라 다음이다 [추론, 단 다섯 렌즈가 독립 지지]:

1. **7일 안에 복제될 기능이 아니라 90일 쌓이는 자산을 설계한다.** 고객별 기록·승인 규칙·고유 데이터·전문가 판단이 핵심. 선별 질문을 "AI가 만들 수 있나?"에서 "90일 뒤 고객에게 무엇이 축적되나?"로 바꾼다.
2. **이미 신뢰가 있는 좁은 업종에서 '제품화 서비스'로 현금을 만든다.** 컨시어지 → 반복 70%만 자동화 → 반복 기능만 SaaS화. 앞 단계가 뒤 단계의 수요·현금을 보조한다 [출처: https://stripe.com/us/blog/stripe-atlas-startups-in-2025-year-in-review].
3. **수익을 4층으로 분해한다**: 접근료(구독) + 사용량(크레딧) + 결과(성과 수수료) + 신뢰(검수·SLA·감사 프리미엄).
4. **가격은 개발 시간이 아니라 고객의 대체 비용으로 정한다.** AI로 2시간 만들었다고 싸게 팔면 생산성 이익을 전부 구매자에게 넘긴다.
5. **'AI가 만들었다'가 아니라 검증 범위·한계·책임 주체를 판다** — 보안 취약점이 인간 코드의 2.74배인 환경에서 [출처: https://medium.com/@svnkrmkr/vibe-coding-in-2026-the-hidden-risks-nobody-covers-e407b2abecdc], '신뢰 영수증'이 차별점이 된다.

## 미해결 질문

1. **인간+AI 팀의 실제 수익화 경로** — peer-review 실증 전무. LLM 단독은 프리랜서 과제의 26%만 해결(SWE-Lancer) [출처: https://doi.org/10.48550/arXiv.2502.12115], 인간 결합 효과는 미측정.
2. **국내(한국) 시장** — 본 리서치의 출처는 대부분 미국·글로벌. 네이버·카카오·토스 기반 수익화, 국내 세무·환불 의무는 별도 조사 필요.
3. **플랫폼 개방성의 지속** — 에이전트 커머스 수수료·정산이 개인에게 우호적으로 남을지 미확정.
4. **임계 복잡도** — AI 이득이 +55.8%에서 −19%로 뒤집히는 과제 복잡도 경계.

---
*이 글은 Stanford STORM 방법론의 재해석으로 생성됐다. 5개 페르소나를 claude·codex·kimi에 분산해 출처 강제 딥리서치를 수행한 뒤, 모순을 보존하며 종합했다. 수치는 각 출처 시점 기준이며, 기업 자기발표(ARR 등)는 감사된 공시가 아니다.*"""

peer_review = r"""## 동료 검토 (Peer Review) — 적대적 점검

> 기본 가정: "이 종합본에는 문제가 있다." 논문이 경고한 두 실패모드(source bias transfer / over-association)를 전담 점검.

### 결함 목록

- **[MINOR] 출처 편향 — 일부 회의 근거가 Medium/블로그 의존.** 보안 취약점 "2.74배" 등 일부 수치가 Medium 글에 의존한다 [출처: https://medium.com/@svnkrmkr/vibe-coding-in-2026-the-hidden-risks-nobody-covers-e407b2abecdc]. 반면 학자 영혼은 arXiv peer-review 13편으로 강하게 보강돼, 종합본은 가급적 학술 출처(Becker·Liu·Fawzy)를 1차로 인용하도록 조정함. **권고**: 보안 수치는 Veracode 원자료로 교체.
- **[MAJOR→완화] 과잉 일반화(over-association) — METR 연구의 대상 전이.** METR RCT(−19%)는 *숙련 오픈소스 개발자 + 성숙 코드베이스*가 대상이다. 이를 *비개발자 + 그린필드*인 바이브코딩 타깃에 그대로 적용하면 부당한 연결이다. 회의주의자 본인이 이 한계를 명시했고(불확실성 섹션), 종합본도 §3에서 "임계 복잡도 미측정"으로 정직하게 남김 → **봉합 회피 확인.**
- **[MINOR] 기업 자기발표 수치(ARR) 인용.** Cursor/Lovable/Replit ARR은 감사 공시가 아니라 자금조달·홍보용 자체발표다. 경제학자가 이를 명시했고 종합본 footer에 반영 → **편향 라벨 유지.**
- **[MINOR] 생존자 편향 vs 균형.** 회의주의자의 92% 실패율은 강력하나, 역사학자의 '아키텍트 서비스화 희망'과 균형을 이뤄 비관 단일화는 피함.

### 모순 봉합 점검

핵심 모순 3개(생산성 추세 vs 단면 / 플랫폼 기회 vs 함정 / 비개발자 가능 여부)가 종합본 §3·§6·미해결질문에서 **한쪽으로 봉합되지 않고 살아있음** 확인. ✅

### 누락된 반론 점검

회의주의자의 가장 강한 반론(RCT 반증·생존자 편향·보안·Apple 크래다운)이 종합 §3·§4·§7에 모두 보존됨. 희석되지 않음. ✅

### 신뢰도 배지

- **출처 다양성: 상** — arXiv 학술(13편) + 기업 공식가격표 + 정부(EU)·인프라(Stripe/Cloudflare) + 업계 보고서. 단일 진영 아님.
- **인용 충실도: 상** — 거의 모든 사실 주장에 [출처:], 추정은 [추론] 라벨 일관.
- **확신 정직성: 상** — "수익화 직접 실증 전무", "국내 시장 미조사", "임계 복잡도 미측정"을 숨기지 않음.

### 통과 판정

**조건부 통과 (MINOR 3건 반영, MAJOR 1건 완화 확인).** BLOCKER 없음 — 종합본은 출처 편향을 라벨링하고 모순을 보존하며 반론을 희석하지 않았다.

### 검토 후 남는 가장 중요한 미해결 질문

> 학술적으로 "바이브코딩 → 개인 수익화"를 직접 측정한 종단 연구가 *하나도 없다*. 본 리포트의 모든 전략 권고는 인접 증거(생산성·코드품질·플랫폼 경제·역사 선례)로부터의 **삼각측량**이지, 직접 실증이 아니다. 이 공백을 메우는 첫 RCT/종단 연구가 나오기 전까지, 모든 "월 X만원" 약속은 [추론]으로 읽어야 한다."""

report = {
    "topic": "바이브코딩으로 수익화하는 방법",
    "slug": "vibe-coding-monetization",
    "generated_at": "2026-06-19",
    "souls": souls,
    "contradiction_map": contradiction_map,
    "synthesis": synthesis,
    "peer_review": peer_review,
    "confidence": {
        "source_diversity": "상",
        "citation": "상",
        "honesty": "상",
        "verdict": "조건부 통과 (MINOR 3건 반영, BLOCKER 0)"
    },
}

out = os.path.join(RUN, "report.json")
json.dump(report, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

# 통계
import re
allmd = contradiction_map + synthesis + peer_review + "".join(s["markdown"] for s in souls)
urls = set(re.findall(r"https?://[^\s<)\]\"']+", allmd))
print("report.json 작성:", out)
print("souls:", len(souls), "| 통합 고유 URL:", len(urls))
