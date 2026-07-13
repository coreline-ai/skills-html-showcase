# Multi-Perspective Scan · AI 영상 제작 파이프라인 운영 매뉴얼 2026
## Skeptic · 회의주의자
질문: AI 영상 생성 도구를 쓰면 제작 속도는 빨라지지만, 신뢰와 권리 문제가 더 커지는 것 아닌가?
가장 큰 위험은 생성 성공을 배포 가능 상태로 착각하는 것이다.
OpenAI는 Sora 책임 출시 설명에서 provenance signal, C2PA, watermark, likeness consent를 강조했지만 해당 페이지는 2026년 4월 26일 기준 Sora product no longer available이라고 표시한다. YouTube는 현실적으로 보이는 합성/변형 콘텐츠 disclosure를 요구하고, C2PA/Content Credentials가 있어도 플랫폼 표시·유지 여부는 별도 운영 문제다. 따라서 매뉴얼은 생성 버튼보다 먼저 권리·출처·라벨링 게이트를 둬야 한다.
출처: https://openai.com/index/launching-sora-responsibly/, https://blog.youtube/news-and-events/disclosing-ai-generated-content/, https://support.google.com/youtube/answer/15447836?hl=en, https://c2pa.org/

## Economist · 경제학자
질문: AI 영상의 진짜 비용 절감은 어디서 발생하고, 어디서 비용이 다시 생기는가?
초안 제작 비용은 낮아지지만 검수·재생성·권리 확인·라벨링 비용이 새 병목이 된다.
Veo, Runway, Firefly 같은 도구는 prompt adherence, visual fidelity, creative control, native audio를 내세운다. 그러나 실무 비용은 첫 clip 생성보다 shot list 정리, reference asset 승인, iteration 기록, platform disclosure, provenance 보존에서 생긴다. 운영자는 생성 횟수가 아니라 '승인된 컷 비율'과 '재작업 사유'를 KPI로 잡아야 한다.
출처: https://deepmind.google/models/veo/, https://ai.google.dev/gemini-api/docs/video, https://runwayml.com/research/introducing-runway-gen-4.5, https://blog.adobe.com/en/publish/2025/02/12/meet-firefly-video-model-ai-powered-creation-with-unparalleled-creative-control

## Historian · 역사학자
질문: 기존 영상 제작 파이프라인에서 무엇은 그대로 남고 무엇만 바뀌는가?
기획·스토리보드·편집·검수는 남고, 생성 도구는 중간 제작 단계를 짧게 바꾼다.
AI 영상은 pre-production을 생략하게 만드는 것이 아니라 더 중요하게 만든다. Veo 문서는 prompts, reference images, first/last frame, resolution, duration 같은 제작 변수의 명시를 요구한다. 이는 전통적인 콘티·샷리스트·후반 검수와 같은 사고 방식이다. 달라진 것은 카메라 장비보다 prompt와 provenance ledger가 중심 자료가 된다는 점이다.
출처: https://ai.google.dev/gemini-api/docs/video, https://helpx.adobe.com/firefly/web/get-started/learn-the-basics/content-credentials-overview.html, https://c2pa.org/

## Academic · 학자
질문: 매뉴얼이 사용자를 보호하려면 어떤 증거 계층을 써야 하는가?
도구 설명, 파일 메타데이터, 플랫폼 라벨, 사람 검수 결과를 서로 다른 증거로 분리해야 한다.
C2PA는 origin/edit history를 표준화하려 하지만, YouTube는 creator disclosure, YouTube generative tools, valid Content Credentials를 서로 다른 label source로 설명한다. Google은 SynthID와 C2PA를 함께 확장하고 있다고 설명한다. 연구 관점에서 이들은 모두 '신호'이지 단독 최종 진실이 아니다. 매뉴얼은 evidence ledger를 만들어 각 컷의 tool, prompt, source asset, human reviewer, label decision을 별도로 저장해야 한다.
출처: https://support.google.com/youtube/answer/15447836?hl=en, https://c2pa.org/, https://blog.google/innovation-and-ai/products/identifying-ai-generated-media-online/, https://deepmind.google/models/synthid/

## Futurist · 미래학자
질문: 2026년 이후 AI 영상 팀의 운영 시스템은 어떤 형태가 될까?
단일 생성 앱보다 '프롬프트·권리·provenance·라벨·배포'를 묶은 제작 운영 원장이 핵심이 된다.
Google은 verification capability를 Gemini/Search/Chrome으로 확장한다고 말하고, Adobe는 Content Credentials cloud/Inspect 흐름을 설명한다. 앞으로 팀의 차별점은 어떤 모델을 쓰느냐보다 어떤 컷을 왜 승인했는지 재현 가능한 원장을 남기는 능력이 된다. 단, 저작권·초상권·광고표시는 지역과 맥락에 따라 달라져 법무/플랫폼 정책 확인이 필요하다.
출처: https://helpx.adobe.com/firefly/web/get-started/learn-the-basics/content-credentials-overview.html, https://blog.google/innovation-and-ai/products/identifying-ai-generated-media-online/, https://www.copyright.gov/ai/, https://www.ftc.gov/business-guidance/advertising-marketing/endorsements-influencers-reviews

