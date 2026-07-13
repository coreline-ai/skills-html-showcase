#!/usr/bin/env python3
"""
doctor.py — bizplan 문서 생성 의존성 점검

발동 시 첫 행동에서 실행. 없는 의존성과 설치 명령을 안내한다.
"""
import importlib.util
import shutil
import subprocess
import sys

PY_PKGS = {
    "docx": ("python-docx", "pip3 install python-docx"),
    "openpyxl": ("openpyxl", "pip3 install openpyxl"),
    "pptx": ("python-pptx", "pip3 install python-pptx"),
    "yaml": ("PyYAML", "pip3 install pyyaml"),
}
TOOLS = {
    "soffice": ("LibreOffice (PDF 변환)", "brew install --cask libreoffice"),
    "node": ("Node.js (HWPX/PPTX 스크립트)", "brew install node"),
    "npx": ("npx (node 스크립트 실행)", "Node.js 설치 시 포함"),
    "mmdc": ("mermaid-cli (다이어그램, 선택)", "npm i -g @mermaid-js/mermaid-cli"),
    "dot": ("Graphviz (다이어그램, 선택)", "brew install graphviz"),
}


def main() -> int:
    ok, missing = [], []

    for mod, (name, install) in PY_PKGS.items():
        if importlib.util.find_spec(mod):
            ok.append(f"  ✓ python:{name}")
        else:
            missing.append(f"  ✗ python:{name}  →  {install}")

    for binname, (desc, install) in TOOLS.items():
        if shutil.which(binname):
            ok.append(f"  ✓ {binname} ({desc})")
        else:
            missing.append(f"  ✗ {binname} ({desc})  →  {install}")

    print("=== bizplan doctor ===")
    print("\n".join(ok) if ok else "  (없음)")
    if missing:
        print("\n[누락 — 해당 포맷 출력 전 설치 필요]")
        print("\n".join(missing))
        print("\n* HTML(md_to_html.py·build_html_deck.py)은 의존성 0 — 항상 동작.")
        print("* DOCX/XLSX/MD 는 python-docx·openpyxl·PyYAML 만으로 가능.")
        print("* PDF 는 soffice, HWPX/PPTX 는 node + (스킬루트에서) npm install 필요.")
    else:
        print("\n[모든 의존성 충족]  · HTML 2종은 의존성 0으로 항상 동작")

    # node_modules 안내
    try:
        import os
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if os.path.exists(os.path.join(root, "package.json")) and not os.path.exists(os.path.join(root, "node_modules")):
            print(f"\n[안내] HWPX/PPTX 사용 전: cd {root} && npm install")
    except Exception:
        pass

    return 0 if not missing else 0  # 점검은 항상 0 (차단 아님, 안내용)


if __name__ == "__main__":
    raise SystemExit(main())
