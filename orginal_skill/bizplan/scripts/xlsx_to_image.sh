#!/bin/bash
# xlsx_to_image.sh — XLSX(수식 포함) → PNG 캡쳐 (사업계획서 본문 삽입용)
#
# soffice 가 수식을 계산하고 인쇄영역을 렌더 → pdftocairo 로 시트(페이지)별 PNG.
# build_xlsx.py 가 fit-to-page·landscape·셀강조를 넣어두면 깔끔하게 잡힌다(2026-06-18 개선).
#
# 사용:
#   bash xlsx_to_image.sh <in.xlsx> <out_prefix> [DPI=150]
#   → <out_prefix>-1.png, <out_prefix>-2.png ... (시트/페이지별)
set -euo pipefail

IN="${1:-}"; OUT="${2:-}"; DPI="${3:-150}"
if [ -z "$IN" ] || [ -z "$OUT" ]; then
  echo "usage: bash xlsx_to_image.sh <in.xlsx> <out_prefix> [DPI]" >&2; exit 1
fi
[ -f "$IN" ] || { echo "[오류] 입력 파일 없음: $IN" >&2; exit 1; }
command -v soffice >/dev/null || { echo "[오류] soffice 없음 → brew install --cask libreoffice" >&2; exit 2; }

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

# 1) XLSX → PDF (soffice 가 수식 계산·인쇄영역 적용). 동시실행 충돌 방지 임시 프로파일.
soffice --headless -env:UserInstallation="file://$TMP/li" \
  --convert-to pdf --outdir "$TMP" "$IN" >/dev/null 2>&1 || true
PDF="$TMP/$(basename "${IN%.*}").pdf"
[ -f "$PDF" ] || { echo "[오류] PDF 변환 실패(soffice). 파일 확인: $IN" >&2; exit 3; }

# 2) PDF → PNG (페이지=시트별)
OUTDIR=$(dirname "$OUT"); mkdir -p "$OUTDIR"
if command -v pdftocairo >/dev/null; then
  pdftocairo -png -r "$DPI" "$PDF" "$OUT"
elif command -v pdftoppm >/dev/null; then
  pdftoppm -png -r "$DPI" "$PDF" "$OUT"
else
  echo "[오류] pdftocairo/pdftoppm 없음 → brew install poppler" >&2; exit 4
fi

# 3) 여백 trim (ImageMagick 있으면)
TRIM=""
command -v magick >/dev/null && TRIM="magick"
[ -z "$TRIM" ] && command -v convert >/dev/null && TRIM="convert"
if [ -n "$TRIM" ]; then
  for f in "${OUT}"-*.png; do
    [ -f "$f" ] && "$TRIM" "$f" -trim +repage "$f" >/dev/null 2>&1 || true
  done
fi

CNT=$(ls "${OUT}"-*.png 2>/dev/null | wc -l | tr -d ' ')
echo "[완료] ${CNT}개 PNG 생성 → ${OUT}-*.png (DPI ${DPI})"
ls "${OUT}"-*.png 2>/dev/null || true
