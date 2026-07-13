#!/usr/bin/env bash
#
# render_diagram.sh — 다이어그램 원본(.mmd/.dot) → PNG/SVG 렌더
#
# 사용:
#   bash render_diagram.sh <src.mmd|src.dot|src.gv> <out.png|out.svg>
#
# 비고:
#   - 입력 확장자로 도구 자동 판단: .mmd → mmdc(mermaid-cli), .dot/.gv → dot(graphviz)
#   - 출력 확장자(.png/.svg)로 포맷 결정.
#   - 필요한 도구가 없으면 설치 안내를 출력하고 비차단 종료(exit 0, 경고만).
#     (다이어그램은 선택 산출물 — 도구 부재로 파이프라인을 멈추지 않는다.)

set -u

usage() {
  echo "사용: bash render_diagram.sh <src.mmd|.dot|.gv> <out.png|.svg>" >&2
  echo "예 : bash render_diagram.sh 07-diagrams/diagram-source/flow.mmd 07-diagrams/images/flow.png" >&2
}

if [ "$#" -lt 2 ]; then
  usage
  exit 1
fi

SRC="$1"
OUT="$2"

if [ ! -f "$SRC" ]; then
  echo "[오류] 입력 파일 없음: $SRC" >&2
  exit 1
fi

# --- 확장자 판단 ---
SRC_EXT="$(echo "${SRC##*.}" | tr '[:upper:]' '[:lower:]')"
OUT_EXT="$(echo "${OUT##*.}" | tr '[:upper:]' '[:lower:]')"

if [ "$OUT_EXT" != "png" ] && [ "$OUT_EXT" != "svg" ]; then
  echo "[오류] 출력 확장자는 png 또는 svg 여야 합니다: $OUT" >&2
  exit 1
fi

mkdir -p "$(dirname "$OUT")"

case "$SRC_EXT" in
  mmd|mermaid)
    MMDC="$(command -v mmdc 2>/dev/null || true)"
    if [ -z "$MMDC" ]; then
      cat >&2 <<'EOF'
[경고] mmdc(mermaid-cli) 가 없어 Mermaid 다이어그램을 렌더하지 못했습니다.
  설치: npm i -g @mermaid-js/mermaid-cli
  (다이어그램은 선택 산출물이므로 파이프라인은 계속 진행합니다.)
EOF
      exit 0
    fi
    echo "[렌더] mermaid: $SRC → $OUT"
    if "$MMDC" -i "$SRC" -o "$OUT" >/dev/null 2>&1; then
      echo "[완료] $OUT"
      exit 0
    else
      echo "[경고] mermaid 렌더 실패 — 원본 문법을 확인하세요: $SRC" >&2
      exit 0
    fi
    ;;
  dot|gv)
    DOT="$(command -v dot 2>/dev/null || true)"
    if [ -z "$DOT" ]; then
      cat >&2 <<'EOF'
[경고] dot(Graphviz) 가 없어 DOT 다이어그램을 렌더하지 못했습니다.
  설치: brew install graphviz  (또는 apt-get install graphviz)
  (다이어그램은 선택 산출물이므로 파이프라인은 계속 진행합니다.)
EOF
      exit 0
    fi
    echo "[렌더] graphviz: $SRC → $OUT (-T$OUT_EXT)"
    if "$DOT" "-T$OUT_EXT" "$SRC" -o "$OUT" >/dev/null 2>&1; then
      echo "[완료] $OUT"
      exit 0
    else
      echo "[경고] graphviz 렌더 실패 — DOT 문법을 확인하세요: $SRC" >&2
      exit 0
    fi
    ;;
  *)
    echo "[오류] 지원하지 않는 입력 확장자: .$SRC_EXT (.mmd / .dot / .gv 만 지원)" >&2
    exit 1
    ;;
esac
