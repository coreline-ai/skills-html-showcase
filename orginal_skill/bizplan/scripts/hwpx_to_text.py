#!/usr/bin/env python3
"""
hwpx_to_text.py — HWPX(한/글 OWPML) → 평문 텍스트 추출 (의존성 0, 표준 라이브러리)

공고문·첨부 HWPX를 읽기 위한 도구. fetch_notice.py 가 받은 HWPX를 분석 단계에서 텍스트로 변환한다.
HWPX 는 zip 컨테이너이고 본문은 Contents/section*.xml 의 <hp:t> 요소에 있다.
표(<hp:tbl>/<hp:tc>)는 셀별 텍스트를 [ | ] 구분으로 근사 추출한다(완벽한 표 복원 아님).

* .hwp(구버전 바이너리/OLE)는 지원하지 않는다 → 한/글 또는 변환 도구 필요(보고만).

사용:
  python3 hwpx_to_text.py <in.hwpx> [out.txt]      # out 생략 시 stdout
"""
import html as _html
import re
import sys
import zipfile

SECTION_RE = re.compile(r"Contents/section\d+\.xml$")
T_RE = re.compile(r"<hp:t>(.*?)</hp:t>", re.S)
PARA_SPLIT = re.compile(r"<hp:p\b")
CELL_SPLIT = re.compile(r"<hp:tc\b")
TBL_RE = re.compile(r"<hp:tbl\b")


def _clean(s: str) -> str:
    s = re.sub(r"<[^>]+>", "", s)          # 잔여 인라인 태그 제거
    s = _html.unescape(s)
    return s.replace("​", "").strip()


def extract(path: str) -> str:
    out = []
    with zipfile.ZipFile(path) as z:
        sections = sorted(n for n in z.namelist() if SECTION_RE.match(n))
        if not sections:  # 일부 HWPX 는 section 경로가 다를 수 있음 → 전체 xml fallback
            sections = sorted(n for n in z.namelist() if n.endswith(".xml") and "ection" in n)
        for n in sections:
            xml = z.read(n).decode("utf-8", "ignore")
            # 표 셀은 ' | ' 로 잇고, 문단은 줄바꿈으로
            # 간이 처리: 문단 단위 분할 후 각 문단의 <hp:t> 이어붙임.
            for para in PARA_SPLIT.split(xml)[1:]:
                # 표 셀 경계를 파이프로 표시(셀 안에 문단이 또 있을 수 있으나 근사)
                cells = CELL_SPLIT.split(para)
                if len(cells) > 1:
                    parts = []
                    for c in cells:
                        ts = "".join(T_RE.findall(c))
                        t = _clean(ts)
                        if t:
                            parts.append(t)
                    line = " | ".join(parts)
                else:
                    line = _clean("".join(T_RE.findall(para)))
                if line:
                    out.append(line)
    # 과도한 빈 줄 정리
    text = "\n".join(out)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    src = sys.argv[1]
    try:
        text = extract(src)
    except zipfile.BadZipFile:
        print(f"[오류] HWPX(zip) 가 아님: {src}  (.hwp 구버전은 미지원)", file=sys.stderr)
        return 2
    if len(sys.argv) >= 3:
        with open(sys.argv[2], "w", encoding="utf-8") as f:
            f.write(text)
        print(f"[완료] {sys.argv[2]}  ({len(text)}자)")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
