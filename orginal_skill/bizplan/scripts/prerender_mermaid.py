#!/usr/bin/env python3
"""prerender_mermaid.py — md 안의 ```mermaid 코드블록을 PNG로 렌더하고 ![](png)로 치환한다.

목적: HTML 산출물은 ```mermaid 를 브라우저가 자동 렌더하지만, DOCX/HWPX/PDF 는
코드블록을 그대로 텍스트로 출력해 다이어그램이 깨진다. 이 스크립트로 DOCX/PDF용
"렌더 md"를 만들어 PNG 가 임베드되게 한다. (원본 md 는 HTML 용으로 그대로 둔다.)

사용:
  python3 prerender_mermaid.py <in.md> <out.md> --img-dir 07-diagrams/images \
      --src-dir 07-diagrams/diagram-source [--prefix scene]

동작:
  1. ```mermaid ... ``` 블록을 순서대로 추출
  2. 각 블록을 <src-dir>/<prefix>-NN.mmd 로 보존
  3. 로컬 mmdc(node_modules/.bin/mmdc)로 <img-dir>/<prefix>-NN.png 렌더(배경 흰색·고해상)
  4. out.md 에서 코드블록을 ![alt](상대경로 png) 로 치환 (out.md 위치 기준 상대경로)
  5. 렌더 실패 블록은 원본 코드블록을 유지(비차단)
"""
import re, os, sys, subprocess, argparse, json

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MMDC = os.path.join(SKILL_ROOT, "node_modules", ".bin", "mmdc")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("in_md")
    ap.add_argument("out_md")
    ap.add_argument("--img-dir", required=True, help="PNG 출력 디렉토리")
    ap.add_argument("--src-dir", required=True, help=".mmd 원본 보존 디렉토리")
    ap.add_argument("--prefix", default="diagram")
    ap.add_argument("--width", default="1600")
    a = ap.parse_args()

    os.makedirs(a.img_dir, exist_ok=True)
    os.makedirs(a.src_dir, exist_ok=True)
    text = open(a.in_md, encoding="utf-8").read()
    out_dir = os.path.dirname(os.path.abspath(a.out_md)) or "."

    # 다이어그램 폰트 통일 (Pretendard) — mermaid config
    config_path = os.path.join(a.src_dir, "_mmdc-config.json")
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump({"themeVariables": {"fontFamily": "Pretendard, sans-serif"}}, f)

    if not os.path.exists(MMDC):
        print(f"[prerender] ⚠ mmdc 없음({MMDC}) — 코드블록 유지. npm install @mermaid-js/mermaid-cli")

    pat = re.compile(r"```mermaid[ \t]*\n(.*?)\n```", re.DOTALL)
    count = [0]
    rendered = [0]

    def repl(m):
        count[0] += 1
        n = count[0]
        code = m.group(1)
        name = f"{a.prefix}-{n:02d}"
        mmd = os.path.join(a.src_dir, name + ".mmd")
        png = os.path.join(a.img_dir, name + ".png")
        with open(mmd, "w", encoding="utf-8") as f:
            f.write(code)
        if os.path.exists(MMDC):
            r = subprocess.run(
                [MMDC, "-i", mmd, "-o", png, "-b", "white", "-w", a.width, "-c", config_path],
                capture_output=True, text=True,
            )
            if r.returncode != 0:
                print(f"[prerender] ✗ {name} 렌더 실패: {r.stderr.strip()[:120]}")
        if os.path.exists(png):
            rendered[0] += 1
            rel = os.path.relpath(png, out_dir)
            return f"![{name}]({rel})"
        return m.group(0)  # 실패 시 원본 유지

    new = pat.sub(repl, text)
    with open(a.out_md, "w", encoding="utf-8") as f:
        f.write(new)
    print(f"[prerender] mermaid 블록 {count[0]}개 중 {rendered[0]}개 PNG 렌더 → {a.out_md}")


if __name__ == "__main__":
    main()
