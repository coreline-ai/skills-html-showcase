#!/usr/bin/env bash
# storm-research: 한 영혼에게 딥리서치 브리프를 조립해 전달.
# 브리프 = soul-brief 템플릿(공통 프로토콜 + 실제 경로/ref) + 해당 영혼 charter.
#
# 사용법:
#   dispatch-soul.sh --run-dir <abs> --soul <Skeptic> --topic "<주제>" \
#                    --main-ref <surface:N> [--soul-file <abs charter path>]
#
# --soul-file 생략 시 souls/soul-<lowercase-soul>.md 자동 탐색.

set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
# shellcheck source=lib.sh
source "$SCRIPT_DIR/lib.sh"

RUN_DIR=""; SOUL=""; TOPIC=""; MAIN_REF=""; SOUL_FILE=""
while [ $# -gt 0 ]; do
  case "$1" in
    --run-dir)   RUN_DIR="$2"; shift 2 ;;
    --soul)      SOUL="$2"; shift 2 ;;
    --topic)     TOPIC="$2"; shift 2 ;;
    --main-ref)  MAIN_REF="$2"; shift 2 ;;
    --soul-file) SOUL_FILE="$2"; shift 2 ;;
    *) echo "unknown arg: $1" >&2; exit 2 ;;
  esac
done

[ -n "$RUN_DIR" ] && [ -n "$SOUL" ] && [ -n "$TOPIC" ] || {
  echo "usage: dispatch-soul.sh --run-dir <abs> --soul <name> --topic <str> [--main-ref <ref>] [--soul-file <path>]" >&2; exit 2; }
export RUN_DIR
mkdir -p "$RUN_DIR"/{briefs,results,done}

# 메인 ref 해석 (인자 > 캐시)
if [ -z "$MAIN_REF" ]; then MAIN_REF=$(storm_resolve main 2>/dev/null || echo ""); fi
[ -n "$MAIN_REF" ] || { echo "WARN: main ref 미상 — 영혼이 역방향 push 못 함" >&2; MAIN_REF="surface:UNKNOWN"; }

# charter 파일 탐색
if [ -z "$SOUL_FILE" ]; then
  lc=$(echo "$SOUL" | tr '[:upper:]' '[:lower:]')
  SOUL_FILE="$SKILL_DIR/souls/soul-${lc}.md"
fi
[ -f "$SOUL_FILE" ] || { echo "ERROR: charter not found: $SOUL_FILE" >&2; exit 1; }

RESULTS_PATH="$RUN_DIR/results/${SOUL}.md"
DONE_PATH="$RUN_DIR/done/${SOUL}.done"
BRIEF_PATH="$RUN_DIR/briefs/${SOUL}.md"
TMPL="$SKILL_DIR/templates/soul-brief.md.tmpl"
[ -f "$TMPL" ] || { echo "ERROR: template missing: $TMPL" >&2; exit 1; }

# --- 템플릿 렌더 (python 파일-인자 방식: 특수문자/슬래시/한글 안전) ---
python3 - "$TMPL" "$BRIEF_PATH" "$SOUL" "$TOPIC" "$MAIN_REF" "$RESULTS_PATH" "$DONE_PATH" "$SOUL_FILE" <<'PY'
import sys
tmpl_path,out_path,soul,topic,mainref,results,done,charter_path=sys.argv[1:9]
tmpl=open(tmpl_path).read()
charter=open(charter_path).read()
for k,v in {
  "{{SOUL}}":soul, "{{TOPIC}}":topic, "{{MAIN_REF}}":mainref,
  "{{RESULTS_PATH}}":results, "{{DONE_PATH}}":done, "{{SOUL_CHARTER}}":charter,
}.items():
    tmpl=tmpl.replace(k,v)
open(out_path,'w').write(tmpl)
print(out_path)
PY

echo "[dispatch] brief -> $BRIEF_PATH" >&2

# --- 영혼에게 "이 브리프 읽고 실행" 한 줄 송신 ---
MSG="read ${BRIEF_PATH} 그리고 그 안의 임무를 처음부터 끝까지 수행하라. 출처 없는 주장 금지, 완료 시 메인에 cmux send push."
storm_soul_send "$SOUL" "$MSG" || { echo "ERROR: send to $SOUL 실패" >&2; exit 1; }
echo "[dispatch] $SOUL 에게 임무 전송 완료 (main_ref=$MAIN_REF)" >&2
