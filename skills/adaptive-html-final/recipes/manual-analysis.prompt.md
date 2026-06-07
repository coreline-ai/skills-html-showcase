# Manual Analysis Prompt

```text
다음 제품 문서/README/API 스펙/절차서를 `manual_analysis` 모드로 분석해서 역할별 실행 매뉴얼 HTML로 만들어줘.

요구:
- profile=auto
- Source & Version Snapshot, Reader Role Router, First Success, Prerequisites/Safety, Task Recipes, Troubleshooting, Source Limits 포함
- 원문에 없는 버전/권한/SLA/API 제한은 UNKNOWN 또는 확인 필요로 표시
- 누락/stale/모순 지적에는 원문 근거 위치를 남김
- 외부 JS 없이 단일 HTML로 출력

입력:
<매뉴얼/스펙/절차 텍스트 붙여넣기>
```
