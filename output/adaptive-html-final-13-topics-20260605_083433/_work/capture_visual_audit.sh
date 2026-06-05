#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://127.0.0.1:8765}"
OUT_DIR="$1"
shift

mkdir -p "$OUT_DIR"

for page in "$@"; do
  name="${page%.html}"
  url="$BASE_URL/pages/$page"
  echo "capture $page"
  npx playwright screenshot --channel chrome --viewport-size=1440,1100 --full-page --color-scheme=light --wait-for-selector=main --wait-for-timeout=800 "$url" "$OUT_DIR/${name}__desktop-light.png"
  npx playwright screenshot --channel chrome --viewport-size=1440,1100 --full-page --color-scheme=dark --wait-for-selector=main --wait-for-timeout=800 "$url" "$OUT_DIR/${name}__desktop-dark.png"
  npx playwright screenshot --channel chrome --viewport-size=390,900 --full-page --color-scheme=light --wait-for-selector=main --wait-for-timeout=800 "$url" "$OUT_DIR/${name}__mobile-light.png"
  npx playwright screenshot --channel chrome --viewport-size=390,900 --full-page --color-scheme=dark --wait-for-selector=main --wait-for-timeout=800 "$url" "$OUT_DIR/${name}__mobile-dark.png"
done
