#!/usr/bin/env bash
# storm-research: 로컬 스킬을 ~/.claude/skills 로 심링크 등록
#
# 메인 스킬 1개 + 독립 프롬프트 스킬 4개 = 총 5개 심링크.
# 로컬 원본은 이 레포에 있고, 전역에서는 심링크로만 접근한다 (작가님 지시).
#
# 사용법:
#   ./install.sh           # 심링크 생성/갱신
#   ./install.sh --check   # 상태만 점검 (생성 안 함)
#   ./install.sh --remove  # 심링크 제거

set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$HOME/.claude/skills"

# 심링크 매핑: <전역_스킬명>  <로컬_원본_상대경로>
MAP=(
  "storm-research:."
  "storm-scan:skills/storm-scan"
  "storm-contradict:skills/storm-contradict"
  "storm-synthesize:skills/storm-synthesize"
  "storm-review:skills/storm-review"
)

MODE="install"
case "${1:-}" in
  --check)  MODE="check" ;;
  --remove) MODE="remove" ;;
  "")       MODE="install" ;;
  *)        echo "usage: $0 [--check|--remove]" >&2; exit 2 ;;
esac

mkdir -p "$SKILLS_DIR"

ok=0; warn=0
for entry in "${MAP[@]}"; do
  name="${entry%%:*}"
  rel="${entry#*:}"
  src="$ROOT/$rel"
  dst="$SKILLS_DIR/$name"

  if [ "$MODE" = "remove" ]; then
    if [ -L "$dst" ]; then rm "$dst"; echo "[removed] $dst"; else echo "[skip]    $dst (심링크 아님/없음)"; fi
    continue
  fi

  # 원본에 SKILL.md 존재 확인
  if [ ! -f "$src/SKILL.md" ]; then
    echo "[WARN]    $name: 원본에 SKILL.md 없음 ($src/SKILL.md)"; warn=$((warn+1)); continue
  fi

  if [ "$MODE" = "check" ]; then
    if [ -L "$dst" ] && [ "$(readlink "$dst")" = "$src" ]; then
      echo "[OK]      $name -> $src"; ok=$((ok+1))
    elif [ -e "$dst" ]; then
      echo "[CONFLICT] $name: 이미 존재 ($(readlink "$dst" 2>/dev/null || echo '실제 디렉토리'))"; warn=$((warn+1))
    else
      echo "[MISSING] $name (미설치)"; warn=$((warn+1))
    fi
    continue
  fi

  # install
  if [ -L "$dst" ]; then
    rm "$dst"
  elif [ -e "$dst" ]; then
    echo "[WARN]    $name: 심링크가 아닌 실제 항목이 이미 있음 — 건너뜀 ($dst)"; warn=$((warn+1)); continue
  fi
  ln -s "$src" "$dst"
  echo "[linked]  $name -> $src"; ok=$((ok+1))
done

echo ""
echo "완료: $ok 성공 / $warn 경고 (모드=$MODE, 대상=$SKILLS_DIR)"
[ "$MODE" = "install" ] && echo "→ Claude Code 재시작 또는 새 세션에서 /storm-research, /storm-scan 등 사용 가능"
exit 0
