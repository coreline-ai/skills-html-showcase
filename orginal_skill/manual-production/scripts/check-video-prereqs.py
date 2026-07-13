#!/usr/bin/env python3
"""Check common tutorial-video prerequisites for manual-production.

Usage:
  python check-video-prereqs.py

This script is intentionally read-only and generic. It reports missing tools so an agent can guide installation.
"""
from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass


@dataclass
class Check:
    name: str
    command: list[str]
    required: bool = True


CHECKS = [
    Check("node", ["node", "--version"]),
    Check("npm", ["npm", "--version"]),
    Check("hyperframes", ["npx", "--yes", "hyperframes@0.6.33", "--help"]),
    Check("playwright", ["npx", "playwright", "--version"]),
    Check("ffmpeg", ["ffmpeg", "-version"]),
    Check("ffprobe", ["ffprobe", "-version"]),
]


def run(check: Check) -> tuple[bool, str]:
    exe = check.command[0]
    if shutil.which(exe) is None:
        return False, f"{exe} not found"
    try:
        p = subprocess.run(check.command, text=True, capture_output=True, timeout=45)
    except Exception as exc:
        return False, str(exc)
    output = (p.stdout or p.stderr).strip().splitlines()
    summary = output[0] if output else f"exit {p.returncode}"
    return p.returncode == 0, summary


def main() -> int:
    failed = []
    for check in CHECKS:
        ok, summary = run(check)
        status = "PASS" if ok else "FAIL"
        print(f"{status} {check.name}: {summary}")
        if not ok and check.required:
            failed.append(check.name)
    if failed:
        print("\nMissing required tools:", ", ".join(failed))
        return 1
    print("\nAll tutorial-video prerequisites are available.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
