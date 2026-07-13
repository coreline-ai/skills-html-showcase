#!/usr/bin/env python3
"""
md_to_html.py — Markdown → 자립형(self-contained) HTML (의존성 0, 순수 표준 라이브러리)

사업계획서·리서치 보고서·임원 요약 등 MD 산출물을 단일 HTML 파일로 렌더한다.
특징:
  - 한글 타이포(Pretendard CDN + 시스템 폰트 fallback, 오프라인에서도 깨지지 않음)
  - 헤딩(h2/h3) 기반 자동 목차(좌측 고정 사이드바, 모바일 접힘)
  - 증거 태그 색상 배지: [사실] [추정] [가정] [목표] [확인 필요]  (bizplan 7대 절대 규칙 #2 시각화)
  - GFM 표·인용·코드블록·목록(중첩)·수평선·인라인(굵게/기울임/코드/링크)
  - 이미지: 기본 base64 임베드(단일 파일 공유), --no-embed 시 상대경로 유지
  - 인쇄 스타일(@media print): 사이드바 숨김, 페이지 브레이크

사용:
  python3 md_to_html.py <in.md> <out.html> [--title "제목"] [--subtitle "부제"]
                        [--base-dir <이미지 기준 경로>] [--no-embed] [--no-toc]
"""
import argparse
import base64
import html
import mimetypes
import os
import re
import sys

# ── 블록 정규식 (md_to_docx.py와 동일 규약) ──
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
HR_RE = re.compile(r"^\s*([-*_])\1{2,}\s*$")
UL_RE = re.compile(r"^(\s*)[-*+]\s+(.*)$")
OL_RE = re.compile(r"^(\s*)(\d+)[.)]\s+(.*)$")
QUOTE_RE = re.compile(r"^>\s?(.*)$")
IMG_RE = re.compile(r"^\s*!\[([^\]]*)\]\(([^)]+)\)\s*$")
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})\s*([\w+-]*)\s*$")
TABLE_SEP_RE = re.compile(r"^\s*\|?[\s:|-]+\|?\s*$")

# 증거 태그 → CSS 클래스
TAGS = {
    "사실": "fact",
    "추정": "estimate",
    "가정": "assumption",
    "목표": "goal",
    "확인 필요": "todo",
    "확인필요": "todo",
}
TAG_RE = re.compile(r"\[(사실|추정|가정|목표|확인\s*필요)\]")

# 인라인: 코드 → 굵게 → 기울임 → 링크 순으로 처리
CODE_SPAN_RE = re.compile(r"`([^`]+)`")
BOLD_RE = re.compile(r"\*\*([^*]+)\*\*|__([^_]+)__")
ITALIC_RE = re.compile(r"(?<!\*)\*([^*]+)\*(?!\*)|(?<!_)_([^_]+)_(?!_)")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def slugify(text: str, used: set) -> str:
    s = re.sub(r"<[^>]+>", "", text)
    s = re.sub(r"[^\w가-힣\s-]", "", s).strip().replace(" ", "-")
    s = s or "section"
    base, i = s, 2
    while s in used:
        s = f"{base}-{i}"
        i += 1
    used.add(s)
    return s


def render_inline(text: str) -> str:
    """인라인 마크다운 → HTML. 순서: escape → 코드(placeholder) → 태그배지 → 굵게/기울임/링크 → 복원."""
    placeholders = []

    def stash(htmlfrag: str) -> str:
        placeholders.append(htmlfrag)
        return f"\x00{len(placeholders) - 1}\x00"

    # 1) 코드 스팬을 먼저 빼낸다(내부 마크다운 무시)
    def code_sub(m):
        return stash(f"<code>{html.escape(m.group(1))}</code>")
    text = CODE_SPAN_RE.sub(code_sub, text)

    # 2) 나머지 escape
    text = html.escape(text)

    # 3) 증거 태그 배지
    def tag_sub(m):
        raw = m.group(1)
        key = raw.replace(" ", "")
        cls = TAGS.get(raw) or TAGS.get(key, "todo")
        return stash(f'<span class="tag tag-{cls}">{raw}</span>')
    text = TAG_RE.sub(tag_sub, text)

    # 4) 링크
    def link_sub(m):
        label, url = m.group(1), m.group(2)
        safe = html.escape(url, quote=True)
        return stash(f'<a href="{safe}" target="_blank" rel="noopener">{label}</a>')
    text = LINK_RE.sub(link_sub, text)

    # 5) 굵게 / 기울임
    text = BOLD_RE.sub(lambda m: f"<strong>{m.group(1) or m.group(2)}</strong>", text)
    text = ITALIC_RE.sub(lambda m: f"<em>{m.group(1) or m.group(2)}</em>", text)

    # 6) placeholder 복원
    def restore(m):
        return placeholders[int(m.group(1))]
    text = re.sub(r"\x00(\d+)\x00", restore, text)
    return text


def data_uri(path: str):
    try:
        mime = mimetypes.guess_type(path)[0] or "image/png"
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("ascii")
        return f"data:{mime};base64,{b64}"
    except Exception:
        return None


def split_row(line: str):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", s)]


class Html:
    def __init__(self, base_dir: str, embed: bool):
        self.out = []
        self.toc = []  # (level, slug, text)
        self.used_slugs = set()
        self.base_dir = base_dir
        self.embed = embed
        self.warnings = 0
        self.has_mermaid = False

    def heading(self, level, text):
        inner = render_inline(text)
        if level in (2, 3):
            slug = slugify(text, self.used_slugs)
            self.toc.append((level, slug, re.sub(r"<[^>]+>", "", inner)))
            self.out.append(f'<h{level} id="{slug}">{inner}</h{level}>')
        else:
            self.out.append(f"<h{level}>{inner}</h{level}>")

    def para(self, text):
        self.out.append(f"<p>{render_inline(text)}</p>")

    def hr(self):
        self.out.append("<hr/>")

    def image(self, alt, src):
        safe_alt = html.escape(alt)
        resolved = src
        if not re.match(r"^https?://|^data:", src):
            full = src if os.path.isabs(src) else os.path.join(self.base_dir, src)
            if self.embed and os.path.exists(full):
                uri = data_uri(full)
                if uri:
                    resolved = uri
                else:
                    self.warnings += 1
            elif os.path.exists(full):
                resolved = full
            else:
                self.warnings += 1
                self.out.append(f'<figure class="img-missing">[이미지 없음: {safe_alt or html.escape(src)}]</figure>')
                return
        cap = f"<figcaption>{safe_alt}</figcaption>" if alt else ""
        self.out.append(f'<figure><img src="{html.escape(resolved, quote=True)}" alt="{safe_alt}"/>{cap}</figure>')

    def blockquote(self, lines):
        body = "".join(f"<p>{render_inline(l)}</p>" for l in lines)
        self.out.append(f"<blockquote>{body}</blockquote>")

    def code_block(self, lang, lines):
        # mermaid 다이어그램은 클라이언트에서 mermaid.js 로 렌더(의존성 0, PNG 불필요)
        if (lang or "").lower() == "mermaid":
            self.has_mermaid = True
            self.out.append(
                '<pre class="mermaid" style="background:#fff;border:1px solid #e6e0d6;'
                'border-radius:10px;text-align:center;padding:18px 8px;color:inherit">'
                f'{html.escape(chr(10).join(lines))}</pre>'
            )
            return
        code = html.escape("\n".join(lines))
        cls = f' data-lang="{html.escape(lang)}"' if lang else ""
        self.out.append(f"<pre{cls}><code>{code}</code></pre>")

    def table(self, header, rows):
        th = "".join(f"<th>{render_inline(c)}</th>" for c in header)
        body = []
        for r in rows:
            cells = "".join(f"<td>{render_inline(c)}</td>" for c in r)
            body.append(f"<tr>{cells}</tr>")
        self.out.append(
            f'<div class="table-wrap"><table><thead><tr>{th}</tr></thead>'
            f'<tbody>{"".join(body)}</tbody></table></div>'
        )

    def lists(self, items):
        # items: list of (ordered:bool, level:int, text:str) → 중첩 렌더
        html_out = []
        stack = []  # (tag, level)
        for ordered, level, text in items:
            tag = "ol" if ordered else "ul"
            # 1) 현재보다 '깊은' 리스트는 모두 닫는다
            while stack and stack[-1][1] > level:
                t, _ = stack.pop()
                html_out.append(f"</li></{t}>")
            # 2) 같은 레벨인데 종류(ol/ul)가 다르면 그 레벨도 닫는다(별도 리스트로 분리)
            if stack and stack[-1][1] == level and stack[-1][0] != tag:
                t, _ = stack.pop()
                html_out.append(f"</li></{t}>")
            # 3) 같은 레벨·같은 종류면 형제 항목, 아니면 새 리스트를 연다
            if stack and stack[-1][1] == level and stack[-1][0] == tag:
                html_out.append(f"</li><li>{render_inline(text)}")
            else:
                html_out.append(f"<{tag}>")
                stack.append((tag, level))
                html_out.append(f"<li>{render_inline(text)}")
        while stack:
            t, _ = stack.pop()
            html_out.append(f"</li></{t}>")
        self.out.append("".join(html_out))


def parse(md_lines, h: Html, drop_first_h1: bool = True):
    """첫 번째 H1은 문서 제목으로 헤더에 올라가므로 기본적으로 본문에서 제외(중복 방지)."""
    i, n = 0, len(md_lines)
    first_h1_dropped = not drop_first_h1
    while i < n:
        line = md_lines[i]

        # 코드 펜스
        m = FENCE_RE.match(line)
        if m:
            fence, lang = m.group(1), m.group(2)
            buf = []
            i += 1
            while i < n and not (md_lines[i].strip().startswith(fence[0] * 3)):
                buf.append(md_lines[i])
                i += 1
            i += 1
            h.code_block(lang, buf)
            continue

        if not line.strip():
            i += 1
            continue

        m = HEADING_RE.match(line)
        if m:
            level = len(m.group(1))
            if level == 1 and not first_h1_dropped:
                first_h1_dropped = True  # 문서 제목 = 헤더로 흡수, 본문에선 생략
                i += 1
                continue
            h.heading(level, m.group(2).strip())
            i += 1
            continue

        if HR_RE.match(line):
            h.hr()
            i += 1
            continue

        m = IMG_RE.match(line)
        if m:
            h.image(m.group(1), m.group(2).strip())
            i += 1
            continue

        # 인용 블록
        if QUOTE_RE.match(line):
            buf = []
            while i < n and QUOTE_RE.match(md_lines[i]):
                buf.append(QUOTE_RE.match(md_lines[i]).group(1))
                i += 1
            h.blockquote(buf)
            continue

        # 표: 다음 줄이 구분선이면
        if "|" in line and i + 1 < n and TABLE_SEP_RE.match(md_lines[i + 1]) and "|" in md_lines[i + 1]:
            header = split_row(line)
            i += 2
            rows = []
            while i < n and "|" in md_lines[i] and md_lines[i].strip():
                rows.append(split_row(md_lines[i]))
                i += 1
            h.table(header, rows)
            continue

        # 목록 (연속 수집, 중첩)
        if UL_RE.match(line) or OL_RE.match(line):
            items = []
            while i < n and (UL_RE.match(md_lines[i]) or OL_RE.match(md_lines[i])):
                mu = UL_RE.match(md_lines[i])
                mo = OL_RE.match(md_lines[i])
                if mo:
                    indent, text = mo.group(1), mo.group(3)
                    ordered = True
                else:
                    indent, text = mu.group(1), mu.group(2)
                    ordered = False
                level = len(indent) // 2 + 1
                items.append((ordered, level, text))
                i += 1
            h.lists(items)
            continue

        # 일반 단락 (연속 줄 병합)
        buf = [line.strip()]
        i += 1
        while i < n and md_lines[i].strip() and not _is_block_start(md_lines[i], md_lines[i + 1] if i + 1 < n else ""):
            buf.append(md_lines[i].strip())
            i += 1
        h.para(" ".join(buf))


def _is_block_start(line, nxt):
    return bool(
        HEADING_RE.match(line) or HR_RE.match(line) or UL_RE.match(line) or OL_RE.match(line)
        or QUOTE_RE.match(line) or IMG_RE.match(line) or FENCE_RE.match(line)
        or ("|" in line and TABLE_SEP_RE.match(nxt) and "|" in nxt)
    )


def build_toc(toc):
    if not toc:
        return ""
    items = []
    for level, slug, text in toc:
        cls = "toc-2" if level == 2 else "toc-3"
        # text 는 이미 render_inline 에서 escape됨(태그만 제거) → 재escape 금지(이중 escape 방지)
        items.append(f'<li class="{cls}"><a href="#{slug}">{text}</a></li>')
    return f'<nav class="toc"><div class="toc-title">목차</div><ul>{"".join(items)}</ul></nav>'


CSS = """
:root{--bg:#fdfcfa;--fg:#1a1814;--muted:#6b6459;--line:#e6e0d6;--accent:#1f4e79;--accent-soft:#eaf0f7;--code:#f4f1ec}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--fg);
  font-family:"Pretendard","Pretendard Variable",-apple-system,"Apple SD Gothic Neo","Malgun Gothic","맑은 고딕",system-ui,sans-serif;
  font-size:16px;line-height:1.75;-webkit-font-smoothing:antialiased}
.layout{display:flex;max-width:1180px;margin:0 auto;gap:40px;padding:0 24px}
.toc{position:sticky;top:0;align-self:flex-start;width:240px;max-height:100vh;overflow:auto;padding:32px 0;flex:0 0 240px}
.toc-title{font-weight:800;font-size:13px;letter-spacing:.08em;color:var(--muted);margin-bottom:12px}
.toc ul{list-style:none;margin:0;padding:0}
.toc li{margin:2px 0}
.toc a{color:var(--muted);text-decoration:none;font-size:13.5px;display:block;padding:3px 10px;border-left:2px solid transparent;border-radius:0 4px 4px 0}
.toc a:hover{color:var(--accent);background:var(--accent-soft);border-left-color:var(--accent)}
.toc-3 a{padding-left:24px;font-size:12.5px}
main{flex:1;min-width:0;padding:48px 0 120px}
header.doc-head{border-bottom:3px solid var(--accent);padding-bottom:20px;margin-bottom:36px}
header.doc-head .kicker{color:var(--accent);font-weight:800;font-size:12px;letter-spacing:.14em;text-transform:uppercase}
header.doc-head h1{font-size:30px;line-height:1.3;margin:8px 0 6px;font-weight:800}
header.doc-head .sub{color:var(--muted);font-size:15px}
header.doc-head .meta{color:var(--muted);font-size:12.5px;margin-top:10px}
h1,h2,h3,h4{line-height:1.35;font-weight:800}
h2{font-size:22px;margin:42px 0 14px;padding-top:8px;border-top:1px solid var(--line)}
h3{font-size:18px;margin:28px 0 10px;color:#2a2620}
h4{font-size:15.5px;margin:20px 0 8px;color:var(--muted)}
p{margin:12px 0}
a{color:var(--accent)}
strong{font-weight:800}
ul,ol{margin:12px 0;padding-left:24px}
li{margin:5px 0}
hr{border:none;border-top:1px solid var(--line);margin:32px 0}
code{background:var(--code);padding:1px 6px;border-radius:5px;font-size:.88em;
  font-family:"SF Mono",ui-monospace,Menlo,Consolas,monospace}
pre{background:#1e1b16;color:#f0ece4;padding:16px 18px;border-radius:10px;overflow:auto;font-size:13px}
pre code{background:none;color:inherit;padding:0}
blockquote{margin:18px 0;padding:12px 20px;background:var(--accent-soft);border-left:4px solid var(--accent);border-radius:0 8px 8px 0;color:#2a2620}
blockquote p{margin:4px 0}
.table-wrap{overflow-x:auto;margin:18px 0}
table{border-collapse:collapse;width:100%;font-size:14px}
th,td{border:1px solid var(--line);padding:9px 12px;text-align:left;vertical-align:top}
thead th{background:var(--accent);color:#fff;font-weight:700}
tbody tr:nth-child(even){background:#faf8f4}
figure{margin:20px 0;text-align:center}
figure img{max-width:100%;height:auto;border:1px solid var(--line);border-radius:8px}
figcaption{color:var(--muted);font-size:13px;margin-top:8px}
.img-missing{color:#b03030;background:#fff3f3;border:1px dashed #e0a0a0;padding:10px;border-radius:8px;font-size:13px}
/* 증거 태그 배지 */
.tag{display:inline-block;font-size:11.5px;font-weight:800;padding:1px 8px;border-radius:20px;margin-right:3px;vertical-align:1px;letter-spacing:.02em}
.tag-fact{background:#e3f4e7;color:#1c7a3e;border:1px solid #b6e0c2}
.tag-estimate{background:#e5eefb;color:#1f4e9c;border:1px solid #b9d2f2}
.tag-assumption{background:#fbf3da;color:#9a7411;border:1px solid #ecd99a}
.tag-goal{background:#efe7fb;color:#6b3fb0;border:1px solid #d6c4f0}
.tag-todo{background:#fde4e4;color:#b32424;border:1px solid #f2bcbc}
.legend{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 28px;padding:14px 16px;background:#fff;border:1px solid var(--line);border-radius:10px;font-size:12.5px}
.legend b{color:var(--muted);font-weight:800;margin-right:4px}
.menu-toggle{display:none}
@media (max-width:880px){
  .layout{flex-direction:column;gap:0}
  .toc{position:static;width:auto;max-height:none;flex:none;padding:0;
    border:1px solid var(--line);border-radius:10px;margin:24px 0;padding:16px;display:none}
  .toc.open{display:block}
  .menu-toggle{display:inline-block;margin:20px 0 0;padding:8px 14px;border:1px solid var(--line);
    background:#fff;border-radius:8px;font-weight:700;cursor:pointer}
  main{padding:16px 0 80px}
}
@media print{
  .toc,.menu-toggle{display:none!important}
  body{background:#fff;font-size:11pt}
  .layout{max-width:none;padding:0}
  h2{page-break-after:avoid}
  table,figure,blockquote,pre{page-break-inside:avoid}
  a{color:var(--fg);text-decoration:none}
}
"""

JS = """
document.querySelectorAll('.menu-toggle').forEach(function(b){
  b.addEventListener('click',function(){document.querySelector('.toc').classList.toggle('open');});
});
"""

LEGEND = (
    '<div class="legend"><b>증거 표기</b>'
    '<span class="tag tag-fact">사실</span>확인된 정보 '
    '<span class="tag tag-estimate">추정</span>근거·계산식 '
    '<span class="tag tag-assumption">가정</span>미검증 전제 '
    '<span class="tag tag-goal">목표</span>달성 성과 '
    '<span class="tag tag-todo">확인 필요</span>추가 자료 필요</div>'
)


def main() -> int:
    ap = argparse.ArgumentParser(description="Markdown → 자립형 HTML (bizplan)")
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--title", default="")
    ap.add_argument("--subtitle", default="")
    ap.add_argument("--kicker", default="BUSINESS PLAN")
    ap.add_argument("--meta", default="", help="헤더 메타 줄(기관·날짜 등)")
    ap.add_argument("--base-dir", default="", help="이미지 상대경로 기준(기본: 입력 md 폴더)")
    ap.add_argument("--no-embed", action="store_true", help="이미지 base64 임베드 끄기(상대경로 유지)")
    ap.add_argument("--no-toc", action="store_true", help="목차 사이드바 끄기")
    ap.add_argument("--no-legend", action="store_true", help="증거 표기 범례 끄기")
    args = ap.parse_args()

    if not os.path.exists(args.input):
        print(f"[오류] 입력 파일 없음: {args.input}", file=sys.stderr)
        return 1

    with open(args.input, encoding="utf-8") as f:
        md = f.read().splitlines()

    base_dir = args.base_dir or os.path.dirname(os.path.abspath(args.input))
    h = Html(base_dir=base_dir, embed=not args.no_embed)
    parse(md, h)

    # 제목 자동 추출(첫 H1)
    title = args.title
    if not title:
        for line in md:
            m = HEADING_RE.match(line)
            if m and len(m.group(1)) == 1:
                title = re.sub(r"<[^>]+>", "", render_inline(m.group(2).strip()))
                break
        title = title or os.path.basename(args.input)

    toc_html = "" if args.no_toc else build_toc(h.toc)
    legend_html = "" if args.no_legend else LEGEND
    head = (
        '<header class="doc-head">'
        f'<div class="kicker">{html.escape(args.kicker)}</div>'
        f"<h1>{html.escape(title)}</h1>"
        + (f'<div class="sub">{html.escape(args.subtitle)}</div>' if args.subtitle else "")
        + (f'<div class="meta">{html.escape(args.meta)}</div>' if args.meta else "")
        + "</header>"
    )
    toggle = '<button class="menu-toggle">☰ 목차</button>' if toc_html else ""
    body = "\n".join(h.out)

    # mermaid 다이어그램이 있으면 클라이언트 렌더 스크립트 추가(의존성 0, PNG 불필요)
    mermaid_script = ""
    if h.has_mermaid:
        mermaid_script = (
            '<script type="module">'
            "import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';"
            "mermaid.initialize({startOnLoad:true,theme:'neutral'});"
            "</script>"
        )

    doc = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{html.escape(title)}</title>
<link rel="stylesheet" as="style" crossorigin
  href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css"/>
<style>{CSS}</style>
</head>
<body>
<div class="layout">
{toc_html}
<main>
{head}
{toggle}
{legend_html}
{body}
</main>
</div>
<script>{JS}</script>
{mermaid_script}
</body>
</html>"""

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(doc)

    msg = f"[완료] HTML 생성: {args.output}  (목차 {len(h.toc)}개"
    if h.warnings:
        msg += f", 이미지 경고 {h.warnings}건"
    msg += ")"
    print(msg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
