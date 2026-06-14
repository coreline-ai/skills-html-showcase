#!/bin/bash
# usage: _runmode.sh <render_basename.py> "<mode label>"
# Commits the render script, runs it, validates (review), and commits the page only if OK.
set -u
cd "$(git rev-parse --show-toplevel)" || exit 1
git checkout ahf-17-modes-independent-build 2>/dev/null
OUT=$(cat /tmp/ahf_outdir.txt)
[ -f "$OUT/_work/_finalize.py" ] || git checkout HEAD -- "$OUT" 2>/dev/null
git add -f "$OUT/_work/$1" && git commit -q -m "ahf-17modes: $2 render script" 2>/dev/null
python3 "$OUT/_work/$1" >/dev/null 2>&1 || { echo "RENDER FAIL $1"; exit 1; }
R=$(python3 skills/adaptive-html-final/scripts/validate_output.py "$OUT" --skill-dir skills/adaptive-html-final | tail -1)
Q=$(python3 skills/adaptive-html-final/scripts/quality_contract_check.py "$OUT" | tail -1)
echo "validate=$R | $Q"
if [ "$R" = "OK" ] && echo "$Q" | grep -q "^OK"; then
  git add -f "$OUT" && git commit -q -m "ahf-17modes: $2 (validated OK)" && echo "COMMITTED $2"
else
  echo "--- issues ---"
  python3 skills/adaptive-html-final/scripts/validate_output.py "$OUT" --skill-dir skills/adaptive-html-final --json 2>&1 | python3 -c "import sys,json;d=json.load(sys.stdin);[print(i.get('page','')[:46],i.get('type'),str(i.get('detail',''))[:40]) for i in d['issues'][:8]]"
fi
