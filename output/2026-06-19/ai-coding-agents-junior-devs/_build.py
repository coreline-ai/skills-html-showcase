#!/usr/bin/env python3
# 하이브리드 빌더(확장판): storm-research 5영혼 딥리서치 종합 -> adaptive-html-final 5.10.5 expert_html.
# 검증된 expert 예제 scaffold(인라인 코어 CSS·해시·8테마바)를 재사용하고 <main id="main">만 교체.
import json, re, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[3]
SKILL = ROOT / "skills/adaptive-html-final"
EX = SKILL / "examples/02_expert_llm_gateway_report.html"
OUT = pathlib.Path(__file__).resolve().parent / "index.html"

ICONS = {d["id"]: d["svg"] for d in json.load(open(SKILL/"assets/body-icons.json", encoding="utf-8"))}
def ic(key): return f'<span class="body-icon body-icon--sm">{ICONS[key]}</span>'
def a(url, label): return f'<a href="{url}">{label}</a>'
def h2(n, key, title): return f'<h2>{ic(key)}<span class="num">{n}</span>{title}</h2>'

# 출처 URL 상수
U = {
 "stanford":"https://digitaleconomy.stanford.edu/publication/canaries-in-the-coal-mine-six-facts-about-the-recent-employment-effects-of-artificial-intelligence/",
 "nyfed":"https://libertystreeteconomics.newyorkfed.org/2026/05/do-job-postings-show-early-labor-market-effects-of-ai/",
 "yale":"https://budgetlab.yale.edu/research/evaluating-impact-ai-labor-market-novemberdecember-cps-update",
 "signalfire":"https://www.signalfire.com/blog/signalfire-state-of-talent-report-2025",
 "copilotrct":"https://arxiv.org/abs/2302.06590",
 "metr":"https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/",
 "meta":"https://arxiv.org/html/2605.04779v1",
 "anthropic":"https://www.anthropic.com/research/AI-assistance-coding-skills",
 "dora":"https://dora.dev/research/2024/dora-report/",
 "infoq":"https://www.infoq.com/news/2026/04/junior-developer-pipeline-crisis/",
 "so":"https://stackoverflow.blog/2025/12/26/ai-vs-gen-z/",
 "s174":"https://blog.pragmaticengineer.com/section-174/",
 "gartner":"https://fortune.com/2026/05/11/ai-automation-layoffs-gartner-study-roi/",
 "aiwash":"https://fortune.com/2026/05/31/tech-companies-ai-washing-layoffs-wix-block-snap-atlassian-disposable-workers/",
 "cursor":"https://www.cnbc.com/2025/11/13/cursor-ai-startup-funding-round-valuation.html",
 "market":"https://www.grandviewresearch.com/industry-analysis/ai-code-tools-market-report",
 "bls":"https://www.bls.gov/ooh/computer-and-information-technology/software-developers.htm",
 "history":"https://www.ivanturkovic.com/2026/01/22/history-software-simplification-cobol-ai-hype/",
 "atm":"https://www.aei.org/economics/what-atms-bank-tellers-rise-robots-and-jobs/",
 "spreadsheet":"https://www.npr.org/2015/02/27/389585340/how-the-electronic-spreadsheet-revolutionized-business",
 "indeedpre":"https://engineeringprompts.substack.com/p/ai-and-jobs-the-decline-started-before",
 "lowcode":"https://medium.com/softwareimprovementgroup/low-code-wave-of-the-future-or-blast-from-the-past-7fcd618371b2",
 "case":"https://www.datavail.com/blog/low-code-appdev-the-history-and-evolution-of-automated-coding/",
 "offshore":"https://cacmb4.acm.org/magazines/2010/5/87265-globalization-and-offshoring-of-software-revisited",
 "jevons":"https://jimrutt.substack.com/p/jevons-paradox-and-the-fate-of-software",
 "sfstd":"https://sfstandard.com/2026/02/19/ai-writes-code-now-s-left-software-engineers/",
 "ieee":"https://spectrum.ieee.org/ai-effect-entry-level-jobs",
 "csdecline":"https://builtin.com/articles/computer-science-degree-decline-ai",
 "exposurecrit":"https://arxiv.org/pdf/2510.13369",
 "softwareseni":"https://www.softwareseni.com/what-the-data-actually-shows-about-ai-and-junior-developer-employment-decline/",
 "cursor2":"https://thenextweb.com/news/cursor-anysphere-2-billion-funding-50-billion-valuation-ai-coding",
 "copilotusers":"https://techcrunch.com/2025/07/30/github-copilot-crosses-20-million-all-time-users/",
 "byteiota":"https://byteiota.com/developer-hiring-crisis-2026-40-worse-junior-drops-73/",
 "policy":"https://www.mofo.com/resources/insights/260402-trump-administration-releases-national-ai-policy-framework",
}

HEADER = (
'<header class="header"><div class="kicker"><span class="kicker-text">EXPERT REPORT · STORM 다관점 딥리서치</span></div>'
'<h1>AI 코딩 에이전트는 주니어 개발자의 사다리를 끊는가</h1>'
'<p class="sub">"AI가 주니어 개발자 일자리를 없앤다"는 머리기사를 회의·경제·역사·학자·미래 다섯 렌즈로 출처 기반 검증한다. 결론부터: 주니어 채용 급감은 실재하지만 원인은 다인(多因)이고, 진짜 위험은 일자리 소멸이 아니라 시차를 두고 도착하는 <strong>경력 사다리·시니어 파이프라인의 공동화</strong>다. 모든 수치·주장에 출처를 박고, 동료 검토로 인과·상관 혼동을 점검했다.</p>'
'<div class="meta"><span>expert_html</span><span>expert-report.html</span><span>profile auto</span><span>adaptive-html-final v5.10.5</span><span>무 JS</span></div>'
'<div class="generated-row"><p class="generated-date">생성 기준: 2026-06-19 KST · STORM 5관점 딥리서치 종합(2023~2026 출처)</p>'
'<div class="lens-strip" aria-label="적용 렌즈"><span class="lens-strip-label">LENS</span><span class="lens-chip">회의(반증)</span><span class="lens-chip">경제(인센티브)</span><span class="lens-chip">역사(선례)</span><span class="lens-chip">학자(증거)</span><span class="lens-chip">미래(궤적)</span></div></div></header>'
)

TOC_ITEMS = [("핵심 결론","section-01"),("다섯 렌즈가 합의한 것","section-02"),("핵심 논쟁 — 원인은 AI인가","section-03"),("생산성 증거의 분열","section-04"),("학습·역량 침식","section-05"),("위험 지도","section-06"),("역사적 선례","section-07"),("시장·인센티브 — 누가 이득을 보나","section-08"),("향후 3~5년 시나리오","section-09"),("권고 — 무엇을 해야 하나","section-10"),("동료 검토와 신뢰도","section-11"),("출처","section-12")]
TOC = ('<nav class="toc-map" aria-label="문서 목차"><span class="label">문서 목차</span><p>5관점 딥리서치를 종합한 핵심 섹션을 chip-nav로 이동합니다.</p><div class="toc-pills">'
       + ''.join(f'<a class="toc-pill" href="#{sid}"><b>{i+1}</b>{t}</a>' for i,(t,sid) in enumerate(TOC_ITEMS)) + '</div></nav>')

S = []

S.append(f'''<section id="section-01">{h2(1,"idea","핵심 결론")}
<div class="lede-note"><div class="label">VERDICT</div><p>주니어 개발자 채용이 2022년 말 이후 가파르게 줄어든 것은 여러 1차 데이터로 <strong>확립된 사실</strong>이다 — 스탠퍼드는 22~25세 AI-노출 직군 고용이 정점 대비 약 20% 감소했다고 보고했고({a(U["stanford"],"Stanford 2025")}), SignalFire는 빅테크 신졸 채용이 2023년 대비 25%·2019년 대비 50% 줄었다고 집계했다({a(U["signalfire"],"SignalFire 2025")}). 그러나 "AI가 그 일자리를 없앴다"는 인과 단정은 증거보다 앞서 있다.</p></div>
<p>다섯 관점을 모두 통과시키면 머리기사가 분해된다. 첫째, 하락은 <strong>ChatGPT 출시 이전</strong>에 이미 시작됐고(테크 채용 순감의 거의 절반 · {a(U["indeedpre"],"Indeed 분석")}), 금리 인상·Section 174 세법·CS 졸업생 2배 과잉공급이라는 비-AI 충격이 동시에 작동했다. 둘째, 생산성 향상은 벤더 실험실에선 +55%지만 독립 현장 실험에선 −19%로 뒤집히고, 메타분석 통합효과는 "중간"(g=0.33)에 그친다. 셋째 — 그리고 가장 견고한 발견 — AI 의존은 주니어의 개념 이해·디버깅 역량을 통계적으로 유의하게 깎는다(d≈0.74).</p>
<p>그래서 진짜 위험은 "올해 일자리가 사라진다"가 아니라 <strong>시차(time-lag)</strong>에 있다: 주니어 대체는 분기 단위로 즉시 측정되지만, 그 대가인 시니어 파이프라인 공동화는 5~8년 뒤 청구서로 도착한다. 이 리포트의 결론은 "주니어의 종말"이 아니라 <strong>"주니어 역할의 재정의를 채용 절벽보다 빨리 해내야 한다"</strong>는 것이며, 그것을 못 하면 산업 전체가 집합적으로 인재 토대를 갉아먹는다.</p></section>''')

S.append(f'''<section id="section-02">{h2(2,"success","다섯 렌즈가 합의한 것")}
<p>관점이 충돌하는 와중에도 다섯 영혼이 공통으로 인정한 사실들이 있다. 서로 다른 출처가 여러 방향에서 수렴해 신뢰도가 높은 항목들이다.</p>
<ul>
<li><strong>주니어 채용은 실제로 급감했다.</strong> 스탠퍼드 22~25세 AI-노출 직군 고용 ~20%↓({a(U["stanford"],"Stanford")}), SignalFire 빅테크 신졸 채용 2023년 대비 25%↓·2019년 대비 50%↓({a(U["signalfire"],"SignalFire")}), Indeed 소프트웨어 개발 구인 2022년 정점 대비 약 70%↓({a(U["byteiota"],"Indeed/byteiota 2026")}).</li>
<li><strong>충격은 하단에 집중됐고 시니어는 늘었다.</strong> 같은 기간 경력 2~5년차 채용은 27% 증가했다({a(U["signalfire"],"SignalFire")}). "주니어는 줄이고 미드는 늘리는" 구조다.</li>
<li><strong>실험실 생산성 향상은 현장에서 재현되지 않는다.</strong> 벤더(GitHub) 통제실험 +55.8%와 독립기관(METR) −19%가 정면 충돌하며, 메타분석은 실험실 g=0.73 → 기업 g=0.19 → 오픈소스 g=0.01로 효과가 소멸한다({a(U["meta"],"meta-analysis 2026")}).</li>
<li><strong>학습·도제 파이프라인이 침식되고 있다.</strong> Stack Overflow 신규 질문이 ChatGPT 이후 76% 급감했고 이탈은 신규·주니어에 집중됐다({a(U["so"],"Stack Overflow 2025")}); CS 학부 등록도 2025~2026 8.1% 감소했다({a(U["csdecline"],"BuiltIn 2026")}).</li>
<li><strong>CS 졸업생 실업률이 전체 평균의 약 2배(6.1%)다.</strong> 신규 대졸 실업률 상승 폭도 전체 노동자를 앞선다({a(U["signalfire"],"SignalFire")}).</li>
</ul>
<div class="summary-card"><div class="label">수렴 지점</div><p>네 갈래 데이터(고용·채용·생산성·학습)가 같은 방향을 가리킨다 — 충격은 경력 하단에 집중됐고, 생산성 약속은 현장에서 약해지며, 학습 경로가 함께 침식된다. 관점이 충돌하는 것은 "원인"이지 "현상"이 아니다.</p></div></section>''')

S.append(f'''<section id="section-03">{h2(3,"compare","핵심 논쟁 — 원인은 AI인가")}
<p>가장 날카로운 균열은 "원인"에 있다. <strong>회의주의 렌즈</strong>는 AI 인과론을 정면으로 반박한다.</p>
<ul>
<li><strong>타이밍.</strong> 테크 채용 순감의 거의 절반이 ChatGPT 출시(2022.11) 이전에 발생했다 — AI가 주범이면 그 시점에 변곡점이 보여야 하지만, 가장 가파른 하락은 금리 인상·대량 해고와 겹친 2023~2024년이다({a(U["indeedpre"],"Indeed 분석")}).</li>
<li><strong>단면.</strong> 뉴욕 연준은 채용공고에서 "주니어와 시니어 수요가 거의 평행하게 감소했고, 둔화가 엔트리급 고노출 직종에 특별히 집중되지 않았다 — 채용공고 증거는 뚜렷한 AI 주도 수요 감소를 거의 시사하지 않는다"고 결론지었다({a(U["nyfed"],"NY Fed 2026")}). 예일 예산연구소도 ChatGPT 이후 33개월간 경제 전반에서 AI발 노동 교란을 감지하지 못했다({a(U["yale"],"Yale Budget Lab")}).</li>
<li><strong>대안 원인 ①: Section 174.</strong> 2022년부터 미국 소프트웨어 인건비를 당해 전액 비용처리 못 하고 5년(국내)~15년(해외) 분할상각하게 강제 — 현금이 부족한 기업이 "엔지니어를 해고해 세금을 내는" 순수 재무적 동인이며 타이밍이 정확히 겹친다({a(U["s174"],"Pragmatic Engineer")}).</li>
<li><strong>대안 원인 ②: 공급 과잉.</strong> CS 학위 수여가 51,696건(2013–14)→112,720건(2022–23)으로 10년 만에 2배 폭증, 수요가 붕괴하던 시점에 정원이 두 배가 됐다. 해고된 빅테크 엔지니어가 엔트리 자리를 두고 신입과 경쟁한다.</li>
<li><strong>대안 원인 ③: AI 워싱.</strong> 샘 올트먼조차 2026년 "기업들이 어차피 할 감원을 AI 탓으로 돌린다"고 인정했고, MIT 슬론 명예교수는 "AI는 '우리 잘못이 아니라 기술 탓'으로 보이게 하는 완벽한 변명"이라 했다({a(U["aiwash"],"Fortune 2026")}). Gartner의 350개 기업 조사에서 가장 많이 감원한 기업이 재무 수익 개선을 보이지 못했고, 동시에 사상 최대 자사주 매입을 단행했다({a(U["gartner"],"Fortune/Gartner")}).</li>
</ul>
<p>반대편(<strong>경제·미래 렌즈</strong>)은 인과 신호를 제시한다: 하버드의 6,200만 노동자·28.5만 기업 추적 연구가 AI 도입 기업에서 6분기 내 주니어 고용 9~10% 감소(시니어 무변), GPT-4 출시 후 22~25세 AI-노출 직군 ~13% 하락을 보고했다({a(U["infoq"],"InfoQ/Harvard 2026")}). 그러나 같은 데이터셋 안에서도 결과가 갈린다 — "주니어 종말"을 단정한 측의 공동저자조차 별도 분석에서 "지난 1년간 프로그래머 고용이 유의미하게 성장"한 것으로 봤다({a(U["softwareseni"],"분석 비교")}).</p>
<div class="summary-card"><div class="label">핵심 긴장</div><p>"AI가 주니어 일자리를 없앴다"는 서사는 상관(채용 감소 ∥ AI 확산의 동시 발생)을 인과로 미끄러뜨린다. 가장 강한 반증은 타이밍(하락이 ChatGPT 이전 시작)과 단면(주니어·시니어 동반 감소)이며, 이 리포트는 단일 원인 대신 금리·세법·공급과잉·AI의 다인(多因)으로 기술한다.</p></div></section>''')

S.append(f'''<section id="section-04">{h2(4,"metric","생산성 증거의 분열")}
<p>"AI가 개발자를 빠르게 만든다"는 명제는 측정 맥락에 따라 결론이 뒤집힌다. 숫자를 출처와 함께 늘어놓으면 분열이 분명하다.</p>
<div class="tbl table-scroll"><table><caption>AI 코딩 생산성 — 측정 맥락별 효과(출처 명시)</caption><thead><tr><th>측정</th><th>효과</th><th>맥락 · 출처</th></tr></thead><tbody>
<tr><td>GitHub 통제실험</td><td>+55.8% 빠름 (p&lt;0.001)</td><td>단일 인공 과제(HTTP 서버), 벤더 후원 · {a(U["copilotrct"],"Cui et al. 2023")}</td></tr>
<tr><td>메타분석(23연구·27효과)</td><td>g=0.33 (중간), I²=99%</td><td>실험실 0.73 · 기업 0.19(비유의) · 오픈소스 0.01 · {a(U["meta"],"meta 2026")}</td></tr>
<tr><td>METR 현장 RCT</td><td>−19% (느려짐)</td><td>숙련 OSS 16명·246이슈, 본인은 +20% 착각 · {a(U["metr"],"METR 2025")}</td></tr>
<tr><td>MS·Accenture 현장</td><td>주당 PR +7.5~21.8%</td><td>개발자 ~1,974명, "suggestive" · {a(U["copilotrct"],"Cui/Demirer")}</td></tr>
<tr><td>DORA 2024</td><td>전달 안정성 −7.2%</td><td>AI 채택 25%↑당, 배치 크기 증가가 원인 · {a(U["dora"],"Google DORA")}</td></tr>
</tbody></table></div>
<p>주목할 반전: 메타분석에서 <strong>경험 수준(초급 vs 숙련)에 의한 조절효과는 통계적으로 유의하지 않았다</strong>(QM(2)=3.97, p=0.138). "주니어가 AI로 가장 큰 이득을 본다"는 벤더 서사는 단일 실험실 결과의 일반화였다. PR·라인 수 증가는 "생산성 대용"일 뿐 품질·재작업·디버깅 비용을 상쇄하며(DORA 안정성 −7.2%가 그 증거), 응답자 39%는 AI 코드 신뢰가 "거의 없음"이라 답했다({a(U["dora"],"DORA 2024")}). 즉 시장은 "검증된 효율"이 아니라 "기대된 효율"과 단기 인건비 차익에 반응하고 있다.</p></section>''')

S.append(f'''<section id="section-05">{h2(5,"learning","학습·역량 침식")}
<p>생산성보다 견고한 발견은 학습 쪽에 있다. Anthropic의 주니어 중심 RCT(52명)에서 AI군의 개념 퀴즈 평균은 <strong>50%</strong>로 직접 코딩군 <strong>67%</strong>보다 약 2등급 낮았고(<strong>Cohen\'s d=0.738, p=0.01</strong>), 격차는 디버깅 문항에서 가장 컸다({a(U["anthropic"],"Anthropic 2026")}). 메타분석에서도 학습 통합효과는 g=0.14로 0과 구분되지 않았고, 시험 중 AI 금지 시 g=−0.06·AI 허용 시 g=0.76 — 즉 측정된 건 "실력 습득"이 아니라 <strong>"도구 의존 성과"</strong>였다({a(U["meta"],"meta 2026")}). "생산성은 실력의 지름길이 아니다"가 현재 학계의 수렴점이다.</p>
<p>아래는 그 위험을 구체화한 코드 리뷰다: AI가 "테스트를 통과하는" 인증 검사 코드를 냈지만, 보안 의미를 모른 채 수용하면 주니어가 놓치는 결함을 시니어 리뷰가 잡아낸다 — 디버깅 평가에서 주니어 AI군이 가장 약했던 지점과 정확히 겹친다.</p>'''
'<section class="wg-03" aria-labelledby="wg-03-title"><header class="wg-03-head"><p class="wg-03-kicker">코드 리뷰 · AI 생성 코드의 함정</p><h2 id="wg-03-title" class="wg-03-title">PR · AI가 작성한 토큰 검증 핸들러</h2><div class="wg-03-meta"><span class="wg-03-chip">auth/verify.ts</span><span class="wg-03-chip wg-03-chip-add">+4</span><span class="wg-03-chip wg-03-chip-del">−1</span><span class="wg-03-chip">리뷰어 1명</span></div><nav class="wg-03-jump" aria-label="노트 점프"><span class="wg-03-jump-label">노트로 이동:</span><a href="#wg-03-n1" class="wg-03-jump-link wg-03-sev-critical">L3 critical</a><a href="#wg-03-n2" class="wg-03-jump-link wg-03-sev-warn">L4 warn</a></nav></header>'
'<div class="wg-03-grid"><div class="wg-03-diff" role="table" aria-label="코드 diff">'
'<div class="wg-03-row wg-03-ctx" role="row"><span class="wg-03-ln" aria-hidden="true">1</span><code class="wg-03-code">export function verify(token: string) {</code></div>'
'<div class="wg-03-row wg-03-ctx" role="row"><span class="wg-03-ln" aria-hidden="true">2</span><code class="wg-03-code">  const p = jwt.decode(token);</code></div>'
'<div class="wg-03-row wg-03-add" role="row"><span class="wg-03-ln" aria-hidden="true">3</span><code class="wg-03-code">  return p.exp &gt; Date.now()/1000; // "동작함"</code></div>'
'<div class="wg-03-row wg-03-add" role="row"><span class="wg-03-ln" aria-hidden="true">4</span><code class="wg-03-code">}</code></div>'
'</div><div class="wg-03-notes"><div class="wg-03-note wg-03-sev-critical" id="wg-03-n1"><div class="wg-03-note-loc">L3 · critical</div><div class="wg-03-note-head">서명 미검증</div><div class="wg-03-note-body"><code>jwt.decode</code>는 서명을 검증하지 않는다. 공격자가 <code>exp</code>를 위조하면 통과된다 — <code>jwt.verify(token, secret)</code>를 써야 한다. AI가 통과하는 코드를 냈지만 보안 의미를 모른 채 수용하면 놓친다.</div></div><div class="wg-03-note wg-03-sev-warn" id="wg-03-n2"><div class="wg-03-note-loc">L4 · warn</div><div class="wg-03-note-head">널 가드 부재</div><div class="wg-03-note-body"><code>decode</code>가 null을 반환하면 런타임 에러. 디버깅 평가에서 주니어 AI군이 가장 약했던 지점과 정확히 겹친다.</div></div></div></div></section></section>')

S.append(f'''<section id="section-06">{h2(6,"warning","위험 지도")}
<p>다섯 관점이 지목한 위험을 가능성×영향으로 배치하면, 가장 큰 위험은 즉각적 일자리 소멸이 아니라 시차를 두고 누적되는 구조적 위험이다.</p>'''
'<section class="vt-shell"><div class="vt-frame"><div class="vt-demo">'
'<div class="rm-grid"><div class="rm-cell rm-head">영향 \\ 가능성</div><div class="rm-cell rm-head">낮음</div><div class="rm-cell rm-head">중간</div><div class="rm-cell rm-head">높음</div>'
'<div class="rm-cell rm-head">큼</div><div class="rm-cell rm-risk low">단기 대량 실직(전면 대체)</div><div class="rm-cell rm-risk high">시니어 파이프라인 공동화</div><div class="rm-cell rm-risk high">경력 사다리 단절(진입 트랙 소멸)</div>'
'<div class="rm-cell rm-head">중간</div><div class="rm-cell rm-risk low">AI 학습데이터 품질 저하 루프</div><div class="rm-cell rm-risk med">주니어 디버깅 역량 침식</div><div class="rm-cell rm-risk med">"AI 숙련" 진입장벽 상승</div>'
'<div class="rm-cell rm-head">작음</div><div class="rm-cell rm-risk low">도구 종속·구독비 증가</div><div class="rm-cell rm-risk low">채용 라벨-실채용 괴리</div><div class="rm-cell rm-risk med">CS 전공 등록 급감(8.1%↓)</div></div>'
'</div></div></section>'
f'<p>붉은 칸(가능성 높음·영향 큼)은 모두 <strong>지연형</strong> 위험이다. 마이크로소프트 엔지니어(Russinovich·Hanselman)가 공개 경고한 "좁아지는 피라미드(narrowing pyramid)" — 주니어가 아키텍처·표준을 배우던 진입 작업이 사라지면 미래 시니어가 자라날 토대가 사라진다. 더 나아가 유능한 시니어 감소가 다시 AI 학습데이터·코드 품질을 떨어뜨리는 <strong>3차 피드백 루프</strong>까지 이어지며, 일부 추정은 2032년경 테크리드/아키텍트 60~70% 부족을 경고한다({a(U["infoq"],"InfoQ 2026")}). SF 빅테크 주니어가 스스로를 "Claude Code의 프록시"라 부르고 자기 산출물의 절반만 이해한다는 증언({a(U["sfstd"],"SF Standard 2026")})은 이 침식이 이미 진행 중임을 보여준다.</p></section>''')

S.append(f'''<section id="section-07">{h2(7,"timeline","역사적 선례")}
<p>"프로그래머 없는 개발"이라는 약속은 새롭지 않다. 역사 렌즈는 60년치 선례를 끌어온다 — 그리고 그 선례는 낙관과 경고를 동시에 준다.</p>
<ul>
<li><strong>COBOL(1959)</strong>: 업무 관리자가 직접 코딩하게 하려고 영어식 구문으로 설계됐지만, "프로그래머를 없애려 만든 언어가 컴퓨팅 역사상 가장 오래간 일자리 창출원"이 됐다({a(U["history"],"Turkovic 2026")}).</li>
<li><strong>4GL "Applications Development Without Programmers"(1982)</strong>: James Martin의 약속과 달리 "비프로그래머가 만든·유지보수한 앱은 극소수"였고 수요는 계속 증가했다({a(U["lowcode"],"SIG")}).</li>
<li><strong>CASE 도구(1990~1995)</strong>: 100개+ 업체·200개 도구, 시장 $4.8B(1990)→$12.11B(1995)로 폭증했지만 생성 코드의 비효율로 1990년대 중반 소멸 — 프로그래머 수요는 견고했다({a(U["case"],"Datavail")}).</li>
<li><strong>오프쇼어링(1999~2005)</strong>: 미 SW 일자리 2000~2004년 154,000개 감소·인도 +150,000명, 그러나 선진국 IT '총' 고용 영향은 측정되지 않았고 2005년까지 회복됐다 — 닷컴 붕괴와 분리가 어려웠다({a(U["offshore"],"CACM")}).</li>
<li><strong>ATM vs 창구직원</strong>: ATM 40만 대가 깔리는 동안 창구직은 50만→60만으로 늘었다(은행이 지점을 늘려서). 단 2010년대 모바일뱅킹이라는 "더 완전한 자동화"가 오자 결국 감소했다({a(U["atm"],"AEI/Bessen")}).</li>
<li><strong>스프레드시트 vs 부기 사무원</strong>: 부기·회계 사무원직 40만 개 소멸, 그러나 회계사직 60만 개 증가 — '직업 총량'이 아니라 '특정 하위 등급'이 통째로 증발한 사례다({a(U["spreadsheet"],"NPR")}).</li>
<li><strong>전문가 시스템·1차 AI 겨울(1965~1973)</strong>: Simon·Minsky의 과장된 예측이 1973년 Lighthill 보고서로 무너지며 자금이 붕괴했다 — 현재가 닮은 hype 사이클 국면의 직접 선례다({a(U["history"],"Turkovic")}).</li>
</ul>
<p>반복되는 종결 양식은 "역할 이동 + Jevons형 수요 증가"였고, BLS는 여전히 소프트웨어 개발자 고용을 2034년까지 ~15% 성장 전망한다({a(U["jevons"],"Jevons 분석")}). <strong>그러나 이번이 다른 점</strong>: 과거 추상화는 '루틴 작업'을 없애되 진입로는 남겼는데, 지금은 진입 등급(주니어)과 학습 경로를 <em>동시에</em> 직격한다.</p>
<div class="summary-card"><div class="label">역사의 두 얼굴</div><p>"이번에도 괜찮다"(COBOL·노코드·ATM)와 "이번엔 다르다"(스프레드시트가 부기 사무원 등급을 통째로 소멸)가 모두 역사적 근거를 갖는다. 결과는 코딩 에이전트가 <strong>부분 보조</strong>에 머무느냐 <strong>직무 대체</strong>로 가느냐에 달려 있다 — ATM 낙관론의 무비판 적용은 틀린 유비가 될 수 있다.</p></div></section>''')

S.append(f'''<section id="section-08">{h2(8,"platform","시장·인센티브 — 누가 이득을 보나")}
<p>경제 렌즈의 첫 질문은 "누가 이득을 보는가(Cui bono)?"다. 돈의 흐름을 따라가면 채용 결정의 동력이 보인다.</p>
<ul>
<li><strong>시장 규모</strong>: AI 코딩 도구 시장은 2025년 약 73.7억 달러, 2030년 ~257~260억 달러(CAGR 25~27%) 전망({a(U["market"],"Grand View 2025")}).</li>
<li><strong>벤더 성장</strong>: GitHub Copilot 유료 구독자 130만(2024 Q2)→470만(2026.1), 누적 사용자 2,000만 돌파({a(U["copilotusers"],"TechCrunch 2025")}). Cursor(Anysphere) ARR 1억(2024)→10억(2025)→20억 달러(2026.2), 밸류에이션 4억→293억 달러, 500억 달러 라운드 협상({a(U["cursor"],"CNBC")} · {a(U["cursor2"],"TNW 2026")}).</li>
<li><strong>인센티브의 핵심</strong>: 주니어 인건비(미 개발자 중위 $133,080·하위 10% $79,850 · {a(U["bls"],"BLS 2024")})를 좌석 구독료(정액 월 $39~40, 에이전트형 $150~600)와 토큰 과금으로 치환하려는 기업·벤더의 동기가 정렬돼 있다 — 고정비(임금)→변동비(구독) 전환.</li>
<li><strong>채용 데이터</strong>: "entry-level" 라벨 공고는 2023.10~2024.11 약 47% 증가했지만 실제 주니어 채용은 같은 기간 ~73% 감소(라벨-실채용 괴리), 빅테크 신규 졸업생은 전체 채용의 7%에 불과({a(U["byteiota"],"byteiota")} · {a(U["signalfire"],"SignalFire")}).</li>
</ul>
<div class="summary-card"><div class="label">Cui bono</div><p>이득: 도구 벤더(Anysphere 293억 달러)·모델사(토큰 매출)·VC(단기 회수), 그리고 시니어·미드(레버리지·협상력 ↑). 비용: 주니어·신졸(채용 25~73%↓), CS 대학·부트캠프, 미래의 시니어 파이프라인. 생산성 이득은 불확실(METR −19%)한데 채용 축소는 즉시 실행된다 — AI는 "비용 절감 명분"으로 기능하고, "기대"가 "검증"을 앞질러 채용을 이끈다.</p></div></section>''')

S.append(f'''<section id="section-09">{h2(9,"flow","향후 3~5년 시나리오")}
<p>미래 렌즈는 현재 신호에 닻을 내린 세 시나리오를 제시한다(예측은 [추론]으로 표시). 분기점은 "주니어 소멸"이 아니라 <strong>역할 재정의·도제 재건이 채용 절벽보다 빠른가</strong>이다.</p>
<div class="summary-card"><div class="label">낙관 — 역할 상승 (role uplift)</div><p>전제: AI가 자동화보다 증강으로 정착(스탠퍼드: 증강 직군은 고용 무변), IBM식 "주니어 재설계" 확산, 추상화가 시장을 키운 역사 반복. [추론] "주니어 개발자"는 사라지지 않고 <strong>AI 오케스트레이터·검증자(verifier)</strong>로 재정의된다. 신규 직무(에이전트 운영, eval 엔지니어, AI 산출물 QA, 도메인-AI 통역사)가 흡수하고, 도제·아프렌티스십이 사라진 OJT를 대체한다 — 단 "AI 숙련"이 채용 하한선이 되어 진입 장벽 자체는 높아진다.</p></div>
<div class="summary-card"><div class="label">기준 — 좁아진 피라미드의 시차 비용</div><p>전제: 엔트리 공고 67% 감소·CS 등록 8% 감소가 관성으로 이어지고, 대부분 기업은 의도적으로 투자하지 않으며, 시니어 생산성 부스트가 단기 비용 논리를 계속 이긴다. [추론] 2024~2026의 채용 절벽이 <strong>2029~2032년 미드/시니어 공급 부족</strong>으로 시차 발현된다. 기업들은 희소해진 미드 인재를 두고 임금 경쟁을 벌이고 뒤늦게 도제를 재가동한다 — 진입은 어렵지만 진입한 소수는 가속 성장하는 K자형 양극화.</p></div>
<div class="summary-card"><div class="label">비관 — 사다리 절단 (severed ladder)</div><p>전제: "코딩은 사실상 해결됐다"·"엔트리 화이트칼라 절반 소멸 1~5년"류 궤적이 실현되고, 시니어도 산출물의 절반만 이해하는 역량 침식이 누적되며, 자본 비용이 채용 동결을 장기화한다. [추론] 엔트리 트랙이 구조적으로 단절돼 신규 인력의 "permanent underclass" 우려가 현실화. 시니어 파이프라인이 마르고 코드·학습데이터 품질 저하가 자동화 천장을 낮추는 3차 피드백 루프가 작동한다.</p></div>
<p><strong>핵심 긴장은 시간 비대칭</strong>이다: 주니어 대체는 분기 단위로 즉시 측정되지만, 그 대가인 파이프라인 공동화는 5~8년 뒤 도착한다. 합리적인 개별 기업의 단기 최적화가 산업 전체의 인재 토대를 집합적으로 갉아먹는 구조다. 규제 신호(미 National AI Policy Framework 2026)도 등장했지만 사후적이다({a(U["policy"],"MoFo 2026")}).</p></section>''')

S.append(f'''<section class="decision-section" id="section-10">{h2(10,"decision","권고 — 무엇을 해야 하나")}
<p>증거가 인과를 단정하지 못하더라도, 위험 지도가 가리키는 방향은 분명하다. 의사결정자 유형별 권고를 카드로 정리한다.</p>
<div class="decision-grid">
<article class="decision-card"><h3>{ic("check")}기업 — 주니어에 의도적으로 투자</h3><p>주니어를 "값싼 코더"가 아니라 "AI 산출물 검증자·도메인 통역사"로 재설계하라. IBM은 CHRO 주도로 엔트리 채용을 3배 확대하고 "고객 니즈 해석·AI 산출물 검증"에 배치했다({a(U["infoq"],"IBM 사례")}). 단기 인건비 차익보다 2029년 이후 미드레벨 공급을 확보하는 것이 합리적이다.</p></article>
<article class="decision-card"><h3>{ic("warning")}주니어 — 검증·디버깅 역량을 지켜라</h3><p>AI 산출물을 그대로 수용하지 말고 "왜 동작하는가"를 설명할 수 있어야 한다. 학습 RCT가 보여준 d=0.74 격차는 AI를 끄고 직접 푸는 연습으로 좁혀진다. InfoSec·AI 엔지니어 직무는 두 자릿수 성장 중이니({a(U["ieee"],"IEEE Spectrum")}) "AI 숙련"을 기본기 위에 얹어라.</p></article>
<article class="decision-card"><h3>{ic("audit")}교육·정책 — 도제 경로를 재건</h3><p>OJT가 사라진 자리를 표준화된 도제·코호트 멘토링으로 메워야 한다. 미 행정부 National AI Policy Framework(2026)와 PwC·WEF의 엔트리급 일자리 대화가 신호다({a(U["policy"],"정책 프레임워크")}). 늦으면 한두 코호트의 공백은 회복 불가다.</p></article>
</div></section>''')

S.append(f'''<section id="section-11">{h2(11,"audit","동료 검토와 신뢰도")}
<p>회의주의 영혼을 검토자로 두고(저자≠검토자) 종합본의 약점을 점검했다. STORM 논문이 경고한 출처 편향 전이·과잉 연결·모순 봉합을 의도적으로 점검한다.</p>
<ul>
<li><strong>출처 편향 전이</strong>: 생산성 "+55%"는 벤더(GitHub) 후원 단일 실험 수치이므로 독립 RCT(METR −19%)·메타분석(g=0.33)과 병기해 균형을 맞췄다. 벤더 수치를 단독 인용하지 않았다.</li>
<li><strong>상관≠인과 보존</strong>: "AI가 주니어 일자리를 없앴다"는 인과 단정을 채택하지 않았다. 타이밍·단면 반증을 본문에 살려 두고 다인(금리·세법·공급과잉·AI)으로 기술했다.</li>
<li><strong>방법론 한계 노출</strong>: 가장 인용되는 스탠퍼드 ADP 연구는 ① 진입·퇴출 기업을 제거한 <strong>균형표본</strong>이라 스타트업 붕괴(주니어가 많은 곳)를 놓칠 수 있고, ② 저자 스스로 "결과가 GenAI 외 요인에 영향받았을 수 있다"고 경고하며, ③ <strong>반사실(AI 없었으면 회복?)이 모델링되지 않았다</strong>({a(U["softwareseni"],"방법론 비평")}).</li>
<li><strong>측정도구 불안정</strong>: "AI 노출 점수" 자체가 지수 간 상관이 약하거나 음(Webb vs Acemoglu)이고, 단일 선형모델은 실업위험 변동의 <strong>29.1%만 설명</strong>한다 — 노동자의 스킬·학력이 노출과 채용을 동시에 결정하는 내생성을 통제하지 못한다({a(U["exposurecrit"],"arXiv 비평")}).</li>
<li><strong>사각(blind spot)</strong>: 데이터 대부분이 미국 중심이며 비-미국 노동시장은 미검증이다. 또 프로덕션에서 AI 생성 주니어 코드의 장기 품질·보안 결과를 측정한 연구는 아직 부족하다.</li>
</ul>
<div class="lede-note"><div class="label">CONFIDENCE</div><p>주니어 채용 감소 = <strong>[확립]</strong>. 학습·역량 침식 = <strong>[수렴 중]</strong>. AI의 인과 기여도 = <strong>[논쟁]</strong>. 파이프라인 공동화의 미래 비용 = <strong>[추론]</strong>. <strong>verdict</strong>: 머리기사("AI가 주니어를 없앤다")는 인과를 과장하지만, 그 밑의 구조적 위험(사다리·파이프라인)은 진짜이며 시차를 두고 청구된다.</p></div></section>''')

SOURCES = [
 ("Stanford Digital Economy Lab — Canaries in the Coal Mine (2025)",U["stanford"]),("NY Fed — Job Postings and AI labor effects (2026)",U["nyfed"]),
 ("Yale Budget Lab — Evaluating AI labor impact",U["yale"]),("SignalFire — State of Talent Report 2025",U["signalfire"]),
 ("Cui, Demirer et al. — Copilot RCT (arXiv 2023)",U["copilotrct"]),("METR — AI experienced OSS dev study (2025)",U["metr"]),
 ("Programming productivity/learning meta-analysis (2026)",U["meta"]),("Anthropic — AI assistance and coding skills (2026)",U["anthropic"]),
 ("Google Cloud DORA Report 2024",U["dora"]),("InfoQ — Junior Developer Pipeline Crisis / Harvard (2026)",U["infoq"]),
 ("Stack Overflow — AI vs Gen Z (2025)",U["so"]),("Section 174 — Pragmatic Engineer",U["s174"]),
 ("Fortune/Gartner — AI layoffs ROI (2026)",U["gartner"]),("Fortune — AI-washing layoffs (2026)",U["aiwash"]),
 ("CNBC — Cursor valuation (2025)",U["cursor"]),("Grand View Research — AI code tools market",U["market"]),
 ("BLS — Software Developers OOH (2024)",U["bls"]),("History of software simplification — Turkovic (2026)",U["history"]),
 ("AEI — ATMs and bank tellers (Bessen)",U["atm"]),("NPR — Spreadsheet revolution (2015)",U["spreadsheet"]),
 ("CACM — Offshoring of software revisited",U["offshore"]),("Indeed — AI and jobs: decline started before",U["indeedpre"]),
 ("SF Standard — AI writes the code now (2026)",U["sfstd"]),("IEEE Spectrum — AI effect on entry-level jobs",U["ieee"]),
 ("BuiltIn — CS degree decline (2026)",U["csdecline"]),("AI exposure-score critique (arXiv)",U["exposurecrit"]),
 ("SoftwareSeni — what the data actually shows",U["softwareseni"]),("MoFo — National AI Policy Framework (2026)",U["policy"]),
]
src_lis = ''.join(f'<li>{a(u,t)}</li>' for t,u in SOURCES)
S.append(f'''<section id="section-12">{h2(12,"reference","출처")}
<aside class="source-note"><div class="label">{ic("reference")}Source Note · STORM 5관점 딥리서치</div><p>본 리포트는 storm-research 스킬(회의·경제·역사·학자·미래 5관점)이 실제 웹검색으로 수집한 1차·2차 출처를 adaptive-html-final 5.10.5 expert_html로 종합한 하이브리드 산출물이다. 모든 핵심 수치·주장에 출처를 박았고, 예측은 [추론]으로 라벨했다. 미래 시나리오는 현재 신호의 외삽이며 단정이 아니다. 출처 {len(SOURCES)}건:</p>
<ol>{src_lis}</ol></aside></section>''')

MAIN_INNER = HEADER + TOC + ''.join(S)
ex = EX.read_text(encoding="utf-8")
new = re.sub(r'(<main\s+id="main"[^>]*>)[\s\S]*(</main>)', lambda m: m.group(1)+MAIN_INNER+m.group(2), ex, count=1)
OUT.write_text(new, encoding="utf-8")
import re as _re
vis=_re.sub(r'<[^>]+>',' ',_re.sub(r'<style[\s\S]*?</style>','',MAIN_INNER)); vis=_re.sub(r'\s+',' ',vis).strip()
print("빌드 완료:", OUT, "| 크기:", len(new), "bytes | 섹션:", len(S), "| 본문 visible:", len(vis), "자 | 출처:", len(SOURCES))
