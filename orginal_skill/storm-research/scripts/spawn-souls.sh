#!/usr/bin/env bash
# storm-research: 메인 Opus가 5개 영혼 페인을 생성하고 각 LLM을 권한 허용 모드로 기동.
# (작가님 요구 7: "모든 페인은 메인 오퍼스가 제작하라.")
#
# 사용법:
#   spawn-souls.sh --run-dir <abs> --main-ref <surface:N> \
#                  [--mapping "Skeptic:claude,Economist:codex,Historian:kimi,Academic:claude,Futurist:codex"]
#
# 기본 매핑: claude 2 / codex 2 / kimi 1 (references/soul-distribution.md SSOT).
# 각 영혼 = 새 페인 = 하나의 영혼. 메인 페인은 건드리지 않는다.

set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "$SCRIPT_DIR/lib.sh"

RUN_DIR=""; MAIN_REF=""
MAPPING="Skeptic:claude,Economist:codex,Historian:kimi,Academic:claude,Futurist:codex"

while [ $# -gt 0 ]; do
  case "$1" in
    --run-dir)  RUN_DIR="$2"; shift 2 ;;
    --main-ref) MAIN_REF="$2"; shift 2 ;;
    --mapping)  MAPPING="$2"; shift 2 ;;
    *) echo "unknown arg: $1" >&2; exit 2 ;;
  esac
done

[ -n "$RUN_DIR" ] || { echo "ERROR: --run-dir required" >&2; exit 2; }
[ -n "${CMUX_WORKSPACE_ID:-}" ] || { echo "ERROR: not inside a cmux workspace (\$CMUX_WORKSPACE_ID unset)" >&2; exit 1; }
export RUN_DIR
mkdir -p "$RUN_DIR"/{briefs,results,done}
storm_refs_init

log(){ echo "[spawn-souls] $*" >&2; }

# --- 메인 ref 등록 ---
if [ -n "$MAIN_REF" ]; then
  storm_register main "$MAIN_REF" >/dev/null
else
  MAIN_REF=$(storm_register_main "") || true
fi
[ -n "$MAIN_REF" ] && log "main ref = $MAIN_REF" || log "WARN: main ref 미상 — dispatch 시 --main-ref 명시 권장"

# --- 페인 생성 방향 (균형 분할) ---
# 5개 영혼: 첫 영혼은 오른쪽, 이후 아래로 쌓되 cmux가 자동 타일링.
DIRS=(right down down down down)

IFS=',' read -ra PAIRS <<< "$MAPPING"
i=0
for pair in "${PAIRS[@]}"; do
  soul="${pair%%:*}"; cli="${pair#*:}"
  dir="${DIRS[$i]:-down}"
  log "creating pane '$soul' (cli=$cli, dir=$dir)…"

  ref=$(storm_make_pane "$dir" "$soul") || { log "ERROR: pane '$soul' 생성 실패"; i=$((i+1)); continue; }

  launch=$(storm_launch_cmd "$cli") || { log "ERROR: unknown cli '$cli'"; i=$((i+1)); continue; }
  # 권한 플래그 미탐지 경고
  case "$cli" in
    claude) [ -n "$(storm_flag_claude)" ] || log "WARN: claude bypass flag 미탐지 (권한 프롬프트 가능)";;
    codex)  [ -n "$(storm_flag_codex)" ]  || log "WARN: codex bypass flag 미탐지";;
    kimi)   [ -n "$(storm_flag_kimi)" ]   || log "WARN: kimi bypass flag 미탐지";;
  esac

  storm_soul_send "$soul" "$launch" || log "WARN: launch send to $soul 실패"
  # cli별 매핑 기록
  python3 - "$RUN_DIR/pane-refs.json" "${soul}__cli" "$cli" <<'PY'
import json,sys
f,k,v=sys.argv[1:4]; d=json.load(open(f)); d[k]=v; json.dump(d,open(f,'w'),indent=2)
PY
  i=$((i+1))
done

# --- CLI 기동 안착 대기 (settle 기반) ---
wait_settled() {  # name timeout
  local name="$1" timeout="${2:-60}" ref end prev cur
  ref=$(storm_resolve "$name") || return 1
  end=$(( $(date +%s) + timeout )); prev=""
  while [ "$(date +%s)" -lt "$end" ]; do
    cur=$($CMUX capture-pane --surface "$ref" --lines 40 2>/dev/null | tail -8)
    if [ -n "$cur" ] && [ "$cur" = "$prev" ]; then return 0; fi   # 2회 연속 동일 = 안착
    prev="$cur"; sleep 3
  done
  return 0  # 타임아웃이어도 진행 (dispatch가 재확인)
}

log "waiting for CLIs to settle…"
for pair in "${PAIRS[@]}"; do
  soul="${pair%%:*}"
  wait_settled "$soul" 60 &
done
wait

log "done. layout:"
$CMUX tree 2>/dev/null | grep -E "surface:[0-9]+ \[" || $CMUX list-panes
log "refs: $(cat "$RUN_DIR/pane-refs.json" | tr -d '\n ')"
