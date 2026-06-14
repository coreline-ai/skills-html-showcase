#!/usr/bin/env python3
"""adaptive-html-final 완료 통합 검증 루프 (공통 패치 ④⑥⑦⑧).

`validate_output.py OK`는 필요조건일 뿐 완료 기준이 아니다(§0.5 #6, #7).
이 스크립트는 산출물 하나(또는 디렉터리)에 대해 아래 3종을 한 번에 강제한다.

  1) validate_output.py   — HTML/자산/무JS/시각계약(섹션 surface·h2 아이콘·테마)·해시 정합
  2) quality_contract_check.py — 붕어빵/얇은 문서·placeholder·반복 차단
  3) test_governance_gates.py  — 게이트 함수 회귀(스킬 전역)

셋 + render-audit 아티팩트 검증이 통과해야 exit 0. 검증기는 Playwright를 직접
구동하지 않고 외부 캡쳐 단계가 남긴 `sources/render-audit.json`과 screenshot
파일 존재·overflow_ok 값만 확인한다. 현행 스킬 examples 기준선은 패키지
자기검증을 위해 아티팩트가 없어도 통과시키되, 신규 출력물은 아티팩트 필수다.
사용: python3 scripts/completion_check.py <output_dir>
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
SCRIPTS = SKILL / "scripts"
TESTS = SKILL / "tests"


def run(label: str, argv: list[str]) -> bool:
    print(f"\n=== {label} ===")
    r = subprocess.run([sys.executable, *argv], capture_output=True, text=True)
    out = (r.stdout or "").strip()
    tail = "\n".join(out.splitlines()[-8:])
    if tail:
        print(tail)
    if r.returncode != 0 and r.stderr.strip():
        print(r.stderr.strip()[-800:])
    print(f"-> {'PASS' if r.returncode == 0 else 'FAIL'} ({label})")
    return r.returncode == 0


def is_skill_examples(target: Path) -> bool:
    try:
        return target.resolve() == (SKILL / "examples").resolve()
    except Exception:
        return False


def check_build_evidence(target: Path) -> bool:
    """Check official-template read evidence for new outputs.

    This is not a claim that an LLM "behaved well". It is a durable artifact
    contract: the output must name the official files it used and record each
    file's current sha256. Missing/stale evidence means the output cannot be
    treated as an official adaptive-html-final build, even if HTML validation is
    green.
    """
    if is_skill_examples(target):
        return True
    repo_root = SKILL.parent.parent
    evidence_path = target / "sources" / "build-evidence.json"
    if not evidence_path.exists():
        print(f"missing: {evidence_path}")
        return False
    try:
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"build-evidence parse error: {exc}")
        return False
    ok = True
    files = evidence.get("files")
    if not isinstance(files, list) or len(files) < 5:
        print("build-evidence: files must list at least 5 official inputs")
        ok = False
    required_keys = {"mode", "profile", "layout", "primary_vt", "section_mapping"}
    missing = sorted(k for k in required_keys if not evidence.get(k))
    if missing:
        print(f"build-evidence: missing top-level keys: {', '.join(missing)}")
        ok = False
    for idx, row in enumerate(files or [], 1):
        rel = row.get("path") if isinstance(row, dict) else None
        digest = row.get("sha256") if isinstance(row, dict) else None
        if not isinstance(rel, str) or not rel.strip() or not isinstance(digest, str):
            print(f"build-evidence: invalid file row #{idx}")
            ok = False
            continue
        p = (repo_root / rel).resolve()
        try:
            p.relative_to(repo_root.resolve())
        except ValueError:
            print(f"build-evidence: path escapes repo: {rel}")
            ok = False
            continue
        if not p.exists() or not p.is_file():
            print(f"build-evidence: referenced file missing: {rel}")
            ok = False
            continue
        actual = hashlib.sha256(p.read_bytes()).hexdigest()
        if actual != digest:
            print(f"build-evidence: sha256 mismatch: {rel}")
            ok = False
    return ok


def check_render_audit(target: Path) -> bool:
    """Check externally-produced render evidence.

    Expected schema (minimal):
      {
        "viewports": {
          "1280": {"scrollWidth": 1280, "clientWidth": 1280,
                   "overflow_ok": true, "screenshot": "sources/screenshots/1280.png"},
          "390":  {"scrollWidth": 390,  "clientWidth": 390,
                   "overflow_ok": true, "screenshot": "sources/screenshots/390.png"}
        }
      }
    """
    print("\n=== 4/4 build-evidence + render-audit (official files·1280/390 overflow·screenshot artifact) ===")
    target = target.resolve()
    evidence_ok = check_build_evidence(target)
    audit_path = target / "sources" / "render-audit.json"
    if not audit_path.exists():
        if is_skill_examples(target):
            print("SKIP (examples baseline): render-audit artifact not required for packaged reference examples.")
            print("-> PASS (render-audit examples exception)")
            return True
        print(f"missing: {audit_path}")
        print("-> FAIL (render-audit)")
        return False
    try:
        audit = json.loads(audit_path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"parse error: {exc}")
        print("-> FAIL (render-audit)")
        return False
    viewports = audit.get("viewports") or {}
    ok = True
    for key in ("1280", "390"):
        row = viewports.get(key) or {}
        if row.get("overflow_ok") is not True:
            sw = row.get("scrollWidth")
            cw = row.get("clientWidth")
            print(f"viewport {key}: overflow_ok must be true (scrollWidth={sw}, clientWidth={cw})")
            ok = False
        shot = row.get("screenshot")
        if not isinstance(shot, str) or not shot.strip():
            print(f"viewport {key}: screenshot path missing")
            ok = False
            continue
        shot_path = (target / shot).resolve()
        try:
            shot_path.relative_to(target)
        except ValueError:
            print(f"viewport {key}: screenshot path escapes target: {shot}")
            ok = False
            continue
        if not shot_path.exists() or not shot_path.is_file():
            print(f"viewport {key}: screenshot file not found: {shot}")
            ok = False
    ok = ok and evidence_ok
    print(f"-> {'PASS' if ok else 'FAIL'} (build-evidence + render-audit)")
    return ok


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: python3 scripts/completion_check.py <output_dir>")
        return 2
    target = Path(sys.argv[1])
    if not target.exists():
        print(f"target not found: {target}")
        return 2

    results = {
        "validate_output": run("1/4 validate_output (시각계약·정합)",
                               [str(SCRIPTS / "validate_output.py"), str(target), "--skill-dir", str(SKILL)]),
        "quality_contract": run("2/4 quality_contract (붕어빵·얇음 차단)",
                                [str(SCRIPTS / "quality_contract_check.py"), str(target)]),
        "governance": run("3/4 governance (게이트 회귀)",
                          [str(TESTS / "test_governance_gates.py")]),
        "render_audit": check_render_audit(target),
    }

    passed = sum(results.values())
    print("\n" + "=" * 48)
    print(f"완료 통합 검증: {passed}/4 통과  ->  {'OK' if passed == 4 else 'INCOMPLETE — 위 FAIL 해소 필요'}")
    print("=" * 48)
    return 0 if passed == 4 else 1


if __name__ == "__main__":
    sys.exit(main())
