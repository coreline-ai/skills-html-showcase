#!/usr/bin/env python3
"""adaptive-html-final 완료 통합 검증 루프 (공통 패치 ④⑥⑦⑧).

`validate_output.py OK`는 필요조건일 뿐 완료 기준이 아니다(§0.5 #6, #7).
이 스크립트는 산출물 하나(또는 디렉터리)에 대해 아래 3종을 한 번에 강제한다.

  1) validate_output.py   — HTML/자산/무JS/시각계약(섹션 surface·h2 아이콘·테마)·해시 정합
  2) quality_contract_check.py — 붕어빵/얇은 문서·placeholder·반복 차단
  3) test_governance_gates.py  — 게이트 함수 회귀(스킬 전역)

셋 다 통과해야 exit 0. 추가로 ⑧ 캡쳐 검증(1280px/390px)을 리마인더로 안내한다.
사용: python3 scripts/completion_check.py <output_dir>
"""
from __future__ import annotations

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


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: python3 scripts/completion_check.py <output_dir>")
        return 2
    target = Path(sys.argv[1])
    if not target.exists():
        print(f"target not found: {target}")
        return 2

    results = {
        "validate_output": run("1/3 validate_output (시각계약·정합)",
                               [str(SCRIPTS / "validate_output.py"), str(target), "--skill-dir", str(SKILL)]),
        "quality_contract": run("2/3 quality_contract (붕어빵·얇음 차단)",
                                [str(SCRIPTS / "quality_contract_check.py"), str(target)]),
        "governance": run("3/3 governance (게이트 회귀)",
                          [str(TESTS / "test_governance_gates.py")]),
    }

    print("\n=== ⑧ 캡쳐 검증 리마인더 ===")
    print("1280px / 390px 스크린샷으로 모바일 overflow·레이아웃 어긋남을 눈으로 확인하고 증거를 남길 것"
          " (자동화 아님 — 별도 캡쳐 단계).")

    passed = sum(results.values())
    print("\n" + "=" * 48)
    print(f"완료 통합 검증: {passed}/3 통과  ->  {'OK (캡쳐 확인 후 완료)' if passed == 3 else 'INCOMPLETE — 위 FAIL 해소 필요'}")
    print("=" * 48)
    return 0 if passed == 3 else 1


if __name__ == "__main__":
    sys.exit(main())
