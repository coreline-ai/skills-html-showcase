#!/usr/bin/env bash
# storm-research: 공유 헬퍼 — cmux 경로/플래그 탐지 + surface ref 매핑 + 영혼 송신
#
# 다른 스크립트에서 `source lib.sh` 후 사용. 단독 실행 시 self-test.
#
# 핵심 상태: $RUN_DIR/pane-refs.json  (영혼명 -> surface:N, 그리고 "main" -> surface:N)
#   RUN_DIR 은 한 리서치 run 의 작업 디렉토리 (예: <skill>/dist/<slug>).

set -uo pipefail

# --- cmux 바이너리 위치 ---
storm_cmux_bin() {
  if command -v cmux >/dev/null 2>&1; then echo "cmux"; return 0; fi
  local cand="/Applications/cmux.app/Contents/Resources/bin/cmux"
  [ -x "$cand" ] && { echo "$cand"; return 0; }
  echo "cmux"  # 최후 폴백 (PATH에 기대)
}
CMUX="$(storm_cmux_bin)"

# --- 권한 완전 허용 플래그 탐지 (버전업 대비 --help 재검증) ---
storm_flag_claude() {
  claude --help 2>&1 | grep -q -- "--dangerously-skip-permissions" \
    && echo "--dangerously-skip-permissions" || echo ""
}
storm_flag_codex() {
  local h; h=$(codex --help 2>&1)
  if echo "$h" | grep -q -- "--dangerously-bypass-approvals-and-sandbox"; then
    echo "--dangerously-bypass-approvals-and-sandbox"
  elif echo "$h" | grep -q -- "--full-auto"; then echo "--full-auto"
  else echo ""; fi
}
storm_flag_kimi() {
  local h; h=$(kimi --help 2>&1 || true)
  if echo "$h" | grep -qE -- "(^| )-y(,| )|--yolo"; then echo "-y"
  elif echo "$h" | grep -q -- "--dangerously-skip-permissions"; then echo "--dangerously-skip-permissions"
  else echo ""; fi
}

# CLI별 기동 커맨드 (모델 포함)
storm_launch_cmd() {
  local cli="$1"
  case "$cli" in
    claude) echo "claude --model claude-sonnet-4-6 $(storm_flag_claude)" ;;
    codex)  echo "codex $(storm_flag_codex)" ;;
    kimi)   echo "kimi $(storm_flag_kimi)" ;;
    *)      echo "ERROR: unknown cli '$cli'" >&2; return 1 ;;
  esac
}

# --- RUN_DIR / refs 파일 ---
storm_refs_file() { echo "${RUN_DIR:?RUN_DIR not set}/pane-refs.json"; }

storm_refs_init() {
  local f; f="$(storm_refs_file)"
  mkdir -p "$(dirname "$f")"
  [ -f "$f" ] || echo '{}' > "$f"
}

storm_is_ref() { case "$1" in surface:*[0-9]*) return 0;; *) return 1;; esac; }

storm_register() {  # name ref
  local name="$1" ref="$2" f; f="$(storm_refs_file)"
  storm_is_ref "$ref" || { echo "ERROR: '$ref' not a surface ref" >&2; return 1; }
  storm_refs_init
  python3 - "$f" "$name" "$ref" <<'PY'
import json,sys
f,name,ref=sys.argv[1],sys.argv[2],sys.argv[3]
d=json.load(open(f)); d[name]=ref; json.dump(d,open(f,'w'),indent=2)
PY
  echo "registered: $name -> $ref" >&2
}

storm_resolve() {  # name -> surface:N  (이미 ref면 통과; 캐시 없으면 tree 폴백)
  local name="$1"
  storm_is_ref "$name" && { echo "$name"; return 0; }
  local f; f="$(storm_refs_file)"
  if [ -f "$f" ]; then
    local ref; ref=$(python3 - "$f" "$name" <<'PY'
import json,sys
try:
    d=json.load(open(sys.argv[1])); print(d.get(sys.argv[2],''))
except Exception: print('')
PY
)
    storm_is_ref "$ref" && { echo "$ref"; return 0; }
  fi
  # tree 폴백: 탭 이름으로 surface 찾기
  local ref; ref=$($CMUX tree 2>/dev/null | grep -oE "surface:[0-9]+ \[terminal\] \"$name\"" | grep -oE 'surface:[0-9]+' | head -1)
  storm_is_ref "$ref" && { storm_register "$name" "$ref" >/dev/null 2>&1; echo "$ref"; return 0; }
  echo "ERROR: cannot resolve '$name' to surface ref" >&2
  return 1
}

# --- 영혼에게 송신: send(키입력) + sleep + Enter (race 방지) ---
storm_soul_send() {  # name text
  local name="$1" text="$2" ref
  ref=$(storm_resolve "$name") || { echo "ERROR: resolve failed for $name" >&2; return 1; }
  $CMUX send --surface "$ref" "$text" || { echo "ERROR: send to $name ($ref) failed" >&2; return 1; }
  sleep 0.3
  $CMUX send-key --surface "$ref" Enter || { echo "ERROR: Enter to $name ($ref) failed" >&2; return 1; }
  return 0
}

# --- 페인 생성 + 탭 이름 + ref 등록 ---
storm_make_pane() {  # direction tabname  -> echoes surface ref
  local dir="$1" tab="$2" out ref
  out=$($CMUX new-pane --type terminal --direction "$dir" 2>&1)
  ref=$(echo "$out" | grep -oE "surface:[0-9]+" | head -1)
  [ -z "$ref" ] && { echo "ERROR: create pane '$tab' failed: $out" >&2; return 1; }
  $CMUX rename-tab --surface "$ref" "$tab" >/dev/null 2>&1 || true
  storm_register "$tab" "$ref" >/dev/null
  echo "$ref"
}

# --- 현재(메인) 페인 ref 자동 감지 + 등록 ---
# 전략: `cmux identify` 의 focused.surface_ref 로 현재 페인 ref 를 직접 회수(가장 안정적),
#       그 ref 로 탭을 "Main" 으로 명명. (rename-tab 은 --surface 명시 필수 — 기본 --tab 해석은 실패.)
storm_register_main() {
  local ref="${1:-}"
  if [ -z "$ref" ]; then
    ref=$($CMUX identify 2>/dev/null | grep -oE '"surface_ref"[[:space:]]*:[[:space:]]*"surface:[0-9]+"' | grep -oE 'surface:[0-9]+' | head -1)
    [ -z "$ref" ] && ref="${CMUX_SURFACE_ID:-}"   # 폴백: 환경변수(UUID 도 cmux가 수용)
  fi
  if [ -n "$ref" ]; then
    $CMUX rename-tab --surface "$ref" "Main" >/dev/null 2>&1 || true
    # UUID였다면 identify로 surface:N 재회수
    if ! storm_is_ref "$ref"; then
      ref=$($CMUX identify 2>/dev/null | grep -oE '"surface_ref"[[:space:]]*:[[:space:]]*"surface:[0-9]+"' | grep -oE 'surface:[0-9]+' | head -1)
    fi
  fi
  if storm_is_ref "$ref"; then storm_register main "$ref" >/dev/null; echo "$ref"; return 0; fi
  echo "" ; return 1
}

# --- self-test (직접 실행 시에만; source 시엔 skip) ---
if [ "${BASH_SOURCE[0]:-}" = "${0:-}" ]; then
  echo "[lib.sh self-test]"
  echo "cmux        : $CMUX  ($($CMUX version 2>/dev/null | head -1 || echo 'n/a'))"
  echo "claude flag : $(storm_flag_claude)"
  echo "codex flag  : $(storm_flag_codex)"
  echo "kimi flag   : $(storm_flag_kimi)"
  echo "launch claude: $(storm_launch_cmd claude)"
  echo "launch codex : $(storm_launch_cmd codex)"
  echo "launch kimi  : $(storm_launch_cmd kimi)"
  RUN_DIR="${RUN_DIR:-/tmp/storm-selftest}"; mkdir -p "$RUN_DIR"
  storm_refs_init; storm_register testsoul surface:99 >/dev/null
  echo "resolve test : $(storm_resolve testsoul)"
  echo "is_ref check : $(storm_is_ref surface:99 && echo yes || echo no)"
  rm -rf /tmp/storm-selftest
  echo "[ok]"
fi
