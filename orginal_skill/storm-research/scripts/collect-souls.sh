#!/usr/bin/env bash
# storm-research: 5영혼의 완료를 폴링하고 결과를 수집한다.
# 1순위 = done 파일(.done), 폴백 = 화면 마커(STORM_SOUL_DONE/BLOCKED).
# 영혼의 역방향 cmux send push 는 메인 세션(Opus)이 실시간 수신하므로 여기선 파일 기준.
#
# 사용법:
#   collect-souls.sh --run-dir <abs> --souls "Skeptic,Economist,Historian,Academic,Futurist" [--timeout 900]
#
# 출력: 각 영혼 상태 표 + 완료된 results 경로 목록. 모두 완료면 exit 0, 타임아웃이면 exit 124.

set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "$SCRIPT_DIR/lib.sh"

RUN_DIR=""; SOULS="Skeptic,Economist,Historian,Academic,Futurist"; TIMEOUT=900
while [ $# -gt 0 ]; do
  case "$1" in
    --run-dir) RUN_DIR="$2"; shift 2 ;;
    --souls)   SOULS="$2"; shift 2 ;;
    --timeout) TIMEOUT="$2"; shift 2 ;;
    *) echo "unknown arg: $1" >&2; exit 2 ;;
  esac
done
[ -n "$RUN_DIR" ] || { echo "ERROR: --run-dir required" >&2; exit 2; }
export RUN_DIR
IFS=',' read -ra LIST <<< "$SOULS"

done_for() {  # soul -> 0 if done
  local soul="$1"
  [ -f "$RUN_DIR/done/${soul}.done" ] && return 0
  # 폴백: 화면 마커
  local ref; ref=$(storm_resolve "$soul" 2>/dev/null) || return 1
  $CMUX capture-pane --surface "$ref" --lines 60 2>/dev/null | grep -qE 'STORM_SOUL_DONE' && return 0
  return 1
}
blocked_for() {  # soul -> 0 if blocked
  local soul="$1"
  local ref; ref=$(storm_resolve "$soul" 2>/dev/null) || return 1
  $CMUX capture-pane --surface "$ref" --lines 60 2>/dev/null | grep -qE 'STORM_SOUL_BLOCKED' && return 0
  return 1
}

# bash 3.2 호환 — 연관배열(declare -A) 미사용. 상태는 done 파일/마커로 매 루프 재판정.
status_of() {  # soul -> DONE | BLOCKED | PENDING  (done 파일 1순위)
  local soul="$1"
  done_for "$soul" && { echo DONE; return; }
  blocked_for "$soul" && { echo BLOCKED; return; }
  echo PENDING
}

END=$(( $(date +%s) + TIMEOUT ))
echo "[collect] 폴링 시작 (timeout=${TIMEOUT}s) — souls: $SOULS" >&2
PREV=""
while [ "$(date +%s)" -lt "$END" ]; do
  all_done=1; CUR=""
  for s in "${LIST[@]}"; do
    st=$(status_of "$s"); CUR="$CUR $s:$st"
    [ "$st" = "DONE" ] || all_done=0
  done
  # 상태 변화 시에만 로그
  [ "$CUR" != "$PREV" ] && { echo "[collect]$CUR" >&2; PREV="$CUR"; }
  [ "$all_done" -eq 1 ] && break
  sleep 10
done

echo ""
echo "=== 영혼 상태 ==="
final_ok=1; done_cnt=0
for s in "${LIST[@]}"; do
  st=$(status_of "$s"); rp="$RUN_DIR/results/${s}.md"
  if [ "$st" = "DONE" ] && [ -f "$rp" ]; then
    echo "  [DONE]    $s -> $rp ($(wc -l < "$rp" | tr -d ' ') lines)"; done_cnt=$((done_cnt+1))
  elif [ "$st" = "DONE" ]; then
    echo "  [DONE?]   $s -> 완료 신호 있으나 results 파일 없음 ($rp)"; final_ok=0
  elif [ "$st" = "BLOCKED" ]; then
    echo "  [BLOCKED] $s -> 차단됨 (capture-pane 확인 필요)"; final_ok=0
  else
    echo "  [TIMEOUT] $s -> 미완료"; final_ok=0
  fi
done
echo "완료: $done_cnt/${#LIST[@]}"

[ "$final_ok" -eq 1 ] && exit 0 || exit 124
