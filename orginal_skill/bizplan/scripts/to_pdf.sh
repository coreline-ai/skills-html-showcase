#!/usr/bin/env bash
#
# to_pdf.sh — LibreOffice headless 로 DOCX/PPTX/XLSX → PDF 변환
#
# 사용:
#   bash to_pdf.sh <input.docx|pptx|xlsx> <outdir>
#
# 비고:
#   - soffice(LibreOffice) headless 사용. 없으면 설치 안내 후 종료.
#   - 동시 실행 충돌 방지를 위해 임시 프로파일 디렉토리(-env:UserInstallation) 사용.
#   - 변환 결과 PDF 경로를 마지막 줄에 출력한다.

set -u

usage() {
  echo "사용: bash to_pdf.sh <input.docx|pptx|xlsx> <outdir>" >&2
  echo "예 : bash to_pdf.sh 10-final/final-business-plan.docx 10-final/" >&2
}

# --- 인자 검증 ---
if [ "$#" -lt 2 ]; then
  usage
  exit 1
fi

INPUT="$1"
OUTDIR="$2"

if [ ! -f "$INPUT" ]; then
  echo "[오류] 입력 파일 없음: $INPUT" >&2
  exit 1
fi

# --- soffice 탐색 ---
SOFFICE="$(command -v soffice 2>/dev/null || true)"
if [ -z "$SOFFICE" ]; then
  # macOS 기본 설치 경로 fallback
  if [ -x "/Applications/LibreOffice.app/Contents/MacOS/soffice" ]; then
    SOFFICE="/Applications/LibreOffice.app/Contents/MacOS/soffice"
  fi
fi

if [ -z "$SOFFICE" ]; then
  cat >&2 <<'EOF'
[오류] soffice(LibreOffice) 를 찾을 수 없습니다.
  PDF 변환에는 LibreOffice 가 필요합니다.

  설치:
    macOS : brew install --cask libreoffice
    Ubuntu: sudo apt-get install libreoffice
EOF
  exit 1
fi

mkdir -p "$OUTDIR"

# --- 동시 실행 충돌 방지용 임시 프로파일 ---
PROFILE_DIR="$(mktemp -d "${TMPDIR:-/tmp}/bizplan_soffice.XXXXXX")"
cleanup() { rm -rf "$PROFILE_DIR"; }
trap cleanup EXIT

echo "[변환] $INPUT → PDF (outdir=$OUTDIR)"

"$SOFFICE" \
  --headless \
  --norestore \
  -env:UserInstallation="file://$PROFILE_DIR" \
  --convert-to pdf \
  --outdir "$OUTDIR" \
  "$INPUT" >/dev/null 2>&1
RC=$?

# --- 결과 경로 산출 ---
BASENAME="$(basename "$INPUT")"
STEM="${BASENAME%.*}"
PDF_PATH="$OUTDIR/$STEM.pdf"

if [ "$RC" -ne 0 ] || [ ! -f "$PDF_PATH" ]; then
  echo "[오류] PDF 변환 실패 (rc=$RC). 입력 형식/손상 여부를 확인하세요: $INPUT" >&2
  exit 1
fi

echo "[완료] PDF 생성:"
echo "$PDF_PATH"
exit 0
