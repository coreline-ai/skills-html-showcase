#!/usr/bin/env python3
"""pretest_contract_check.py — output 디렉터리를 official / preview / fail 로 분류.

목적: `output/`의 선검수(pretest) 산출물이 "스킬 완료 official 산출물"로 오인되는 것을 막는다.

판정 규칙(우선순위):
  1) official : validate_output.py 통과(0 issue) AND sources/ 스냅샷 완비 AND pretest 라벨 없음
  2) preview  : pretest 라벨(자기 또는 상위 README/마커)이 있는 경우 — 안전(완료로 오인 안 됨)
  3) fail     : 위 둘 다 아님 — 특히 완료-주장 금지문구를 동반하면 위험(official 오인 가능)

stdlib only. 무 JS HTML 산출물 가정.
사용:
  python3 scripts/pretest_contract_check.py <dir>                 # 단일 output 분류
  python3 scripts/pretest_contract_check.py <dir> --recursive     # 하위 모든 leaf output(=index.html 보유 디렉터리) 분류
  옵션: --json  결과를 JSON으로 출력
종료코드: fail 0건이면 0, fail≥1이면 1 (게이트로 사용 가능)
"""
import sys
import json
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
# 양쪽 배치 호환: 스킬-내부(skills/adaptive-html-final/scripts/)면 validate가 형제 파일,
# repo-root(scripts/)면 skills/ 아래에 있다.
if (HERE / "validate_output.py").is_file():           # 스킬-내부 배치
    VALIDATOR = HERE / "validate_output.py"
    REPO = HERE.parent.parent.parent
else:                                                  # repo-root 배치
    REPO = HERE.parent
    VALIDATOR = REPO / "skills" / "adaptive-html-final" / "scripts" / "validate_output.py"

PRETEST_LABEL_RE = re.compile(r"output-only pretest|선검수|선반영|소스 수정 없이|미반영 가정|pretest", re.IGNORECASE)
FORBIDDEN_CLAIM_RE = re.compile(r"완성 HTML|스킬 적용|스킬 완료|스킬 결과물|공식 산출물|production[- ]ready|프로덕션 적용")
PRETEST_MARKER_FILES = ("pretest-validation.json", "pretest-validation-v2.json")
PRETEST_MARKER_DIRS = ("_bodies", "_qa", "_screenshots")


def _run_validate(d: Path) -> int:
    """validate_output.py <dir> 의 ISSUE 줄 수 반환(실패 시 -1)."""
    try:
        out = subprocess.run(
            [sys.executable, str(VALIDATOR), str(d)],
            capture_output=True, text=True, timeout=180,
        ).stdout
    except Exception:
        return -1
    return sum(1 for ln in out.splitlines() if ln.startswith("ISSUE"))


def _sources_complete(d: Path) -> bool:
    # official 스냅샷 신호: manifest + css-integrity + profile.json (코어 해시 marker는
    # official=validate0 조건의 inline-hash 게이트가 이미 강제하므로 여기에 포섭).
    s = d / "sources"
    return all((s / f).is_file() for f in ("adaptive-html-final-manifest.json", "css-integrity.json", "profile.json"))


def _has_pretest_label(d: Path, repo_root: Path) -> bool:
    """자기 또는 (output/ 까지의) 상위 디렉터리에서 pretest 라벨/마커 탐지."""
    cur = d
    # 자기 + output/ 경계까지 상위로 거슬러 올라가며 마커 탐지
    for _ in range(8):
        for mf in PRETEST_MARKER_FILES:
            if (cur / mf).is_file():
                return True
        for md in PRETEST_MARKER_DIRS:
            if (cur / md).is_dir():
                return True
        readme = cur / "README.md"
        if readme.is_file() and PRETEST_LABEL_RE.search(readme.read_text(encoding="utf-8", errors="ignore")):
            return True
        if cur == repo_root or cur.parent == cur:
            break
        cur = cur.parent
    # index.html 본문 라벨
    idx = d / "index.html"
    if idx.is_file() and PRETEST_LABEL_RE.search(idx.read_text(encoding="utf-8", errors="ignore")):
        return True
    return False


def _has_forbidden_claim(d: Path) -> list:
    hits = []
    for p in sorted(d.rglob("*")):
        if p.is_file() and p.suffix in (".html", ".md"):
            if FORBIDDEN_CLAIM_RE.search(p.read_text(encoding="utf-8", errors="ignore")):
                hits.append(str(p.relative_to(d)))
    return hits


def decide(issues: int, sources_ok: bool, pretest: bool, claims: list) -> tuple:
    """순수 결정 함수: (verdict, reasons). IO 없음 → 단위 테스트 가능."""
    reasons = []
    if issues == 0 and sources_ok and not pretest:
        reasons.append("validate 0 issue + sources/ 완비 + pretest 라벨 없음")
        return "official", reasons
    if pretest:
        reasons.append(f"pretest 라벨 탐지 (validate {issues} issue, sources {'완비' if sources_ok else '없음'})")
        if claims:
            reasons.append(f"⚠️ preview인데 완료-주장 문구 존재({len(claims)}곳): {', '.join(claims[:3])} — 라벨/문구 정리 권장")
        return "preview", reasons
    if issues != 0:
        reasons.append(f"validate {issues} issue(미통과)")
    if not sources_ok:
        reasons.append("sources/ 스냅샷 없음")
    if claims:
        reasons.append(f"❌ 완료-주장 금지문구 존재({len(claims)}곳): {', '.join(claims[:3])} — official 오인 위험")
    else:
        reasons.append("official도 아니고 pretest 라벨도 없음 — 분류 불가, 라벨 필요")
    return "fail", reasons


def classify(d: Path, repo_root: Path) -> dict:
    issues = _run_validate(d)
    sources_ok = _sources_complete(d)
    pretest = _has_pretest_label(d, repo_root)
    claims = _has_forbidden_claim(d)
    verdict, reasons = decide(issues, sources_ok, pretest, claims)

    return {
        "dir": str(d),
        "verdict": verdict,
        "validate_issues": issues,
        "sources_complete": sources_ok,
        "pretest_labeled": pretest,
        "forbidden_claims": claims,
        "reasons": reasons,
    }


def _find_leaf_outputs(root: Path) -> list:
    out = []
    for idx in sorted(root.rglob("index.html")):
        d = idx.parent
        # sources/ 내부 등 자산 디렉터리의 index는 제외
        if d.name in ("sources", "assets", "_bodies", "_qa", "_screenshots"):
            continue
        out.append(d)
    return out


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    recursive = "--recursive" in argv
    as_json = "--json" in argv
    if not args:
        print("usage: pretest_contract_check.py <dir> [--recursive] [--json]", file=sys.stderr)
        return 2
    root = Path(args[0]).resolve()
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 2

    targets = _find_leaf_outputs(root) if recursive else [root]
    results = [classify(d, REPO) for d in targets]

    if as_json:
        print(json.dumps({"results": results}, ensure_ascii=False, indent=2))
    else:
        sym = {"official": "✅", "preview": "🟡", "fail": "❌"}
        for r in results:
            rel = Path(r["dir"]).relative_to(REPO) if str(r["dir"]).startswith(str(REPO)) else r["dir"]
            print(f"{sym[r['verdict']]} {r['verdict'].upper():8} {rel}")
            for rs in r["reasons"]:
                print(f"     - {rs}")
        n_fail = sum(1 for r in results if r["verdict"] == "fail")
        n_prev = sum(1 for r in results if r["verdict"] == "preview")
        n_off = sum(1 for r in results if r["verdict"] == "official")
        print(f"\n요약: official {n_off} · preview {n_prev} · fail {n_fail}  (총 {len(results)})")

    return 1 if any(r["verdict"] == "fail" for r in results) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
