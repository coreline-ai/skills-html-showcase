#!/usr/bin/env python3
"""
build_html_deck.py — deck.json → 자립형 HTML 슬라이드 (의존성 0, 순수 표준 라이브러리)

build_pptx.mts 와 **동일한 deck.json 스키마**를 입력받아 16:9 웹 슬라이드로 렌더한다.
(PPTX 와 HTML 미리보기가 같은 소스에서 나오도록 — 단일 출처 유지)

특징:
  - 9개 layout: title / section / bullets / two-column / table / image / stat / quote / closing
  - 4개 테마: navy(기본) / slate / forest / plum (build_pptx.mts 와 동일)
  - 키보드 네비게이션(← → Space / Home End), 슬라이드 번호, F 풀스크린
  - 이미지 base64 임베드(단일 파일 공유), 인쇄 시 슬라이드별 페이지(@media print)
  - 한글 폰트(Pretendard CDN + 시스템 fallback)

사용:
  python3 build_html_deck.py <deck.json> <out.html> [--base-dir <이미지 기준>] [--no-embed]
"""
import argparse
import base64
import html
import json
import mimetypes
import os
import sys

THEMES = {
    "navy":   {"accent": "#1f4e79", "soft": "#eaf0f7", "ink": "#13233a", "bg": "#0f1d30"},
    "slate":  {"accent": "#3f4756", "soft": "#eef0f3", "ink": "#23282f", "bg": "#1c2129"},
    "forest": {"accent": "#1f6b4a", "soft": "#e7f3ec", "ink": "#123528", "bg": "#0f2a1e"},
    "plum":   {"accent": "#6b3fa0", "soft": "#f0e9f8", "ink": "#2e1b47", "bg": "#231533"},
}


def esc(x) -> str:
    return html.escape("" if x is None else str(x))


def data_uri(path: str):
    try:
        mime = mimetypes.guess_type(path)[0] or "image/png"
        with open(path, "rb") as f:
            return f"data:{mime};base64,{base64.b64encode(f.read()).decode('ascii')}"
    except Exception:
        return None


def resolve_img(src, base_dir, embed):
    if not src:
        return None
    if src.startswith(("http://", "https://", "data:")):
        return src
    full = src if os.path.isabs(src) else os.path.join(base_dir, src)
    if not os.path.exists(full):
        return None
    if embed:
        return data_uri(full)
    return full


def kicker_html(s):
    return f'<div class="s-kicker">{esc(s.get("kicker") or s.get("subtitle", ""))}</div>' if (s.get("kicker") or s.get("subtitle")) else ""


def title_html(s):
    return f'<h2 class="s-title">{esc(s["title"])}</h2>' if s.get("title") else ""


def bullets_to_html(bullets):
    out = ["<ul class='s-bullets'>"]
    for b in bullets or []:
        if isinstance(b, dict):
            out.append(f"<li>{esc(b.get('text',''))}")
            if b.get("sub"):
                out.append("<ul>" + "".join(f"<li>{esc(x)}</li>" for x in b["sub"]) + "</ul>")
            out.append("</li>")
        else:
            out.append(f"<li>{esc(b)}</li>")
    out.append("</ul>")
    return "".join(out)


def render_slide(s, idx, base_dir, embed):
    layout = s.get("layout", "bullets")
    body = ""

    if layout == "title":
        body = (
            f'<div class="cover">'
            + (f'<div class="badge">{esc(s["badge"])}</div>' if s.get("badge") else "")
            + f'<h1>{esc(s.get("title",""))}</h1>'
            + (f'<div class="cover-sub">{esc(s["subtitle"])}</div>' if s.get("subtitle") else "")
            + '<div class="cover-meta">'
            + " · ".join(filter(None, [esc(s.get("author")) if s.get("author") else "",
                                       esc(s.get("date")) if s.get("date") else ""]))
            + "</div></div>"
        )

    elif layout == "section":
        body = (
            '<div class="section-slide">'
            + (f'<div class="sec-index">{esc(s["index"])}</div>' if s.get("index") else "")
            + f'<h2 class="sec-title">{esc(s.get("title",""))}</h2>'
            + (f'<div class="sec-sub">{esc(s["subtitle"])}</div>' if s.get("subtitle") else "")
            + (bullets_to_html(s.get("bullets")) if s.get("bullets") else "")
            + "</div>"
        )

    elif layout == "two-column":
        def col(c):
            if not c:
                return "<div class='col'></div>"
            parts = [f'<div class="col-label">{esc(c.get("label",""))}</div>']
            if c.get("metric"):
                m = c["metric"]
                parts.append(f'<div class="col-metric"><span class="mv">{esc(m.get("value",""))}</span>'
                             f'<span class="ml">{esc(m.get("label",""))}</span></div>')
            for p in c.get("body", []):
                parts.append(f"<p>{esc(p)}</p>")
            if c.get("bullets"):
                parts.append(bullets_to_html(c["bullets"]))
            return f'<div class="col">{"".join(parts)}</div>'
        body = (kicker_html(s) + title_html(s)
                + f'<div class="two-col">{col(s.get("left"))}{col(s.get("right"))}</div>')

    elif layout == "table":
        t = s.get("table", {})
        th = "".join(f"<th>{esc(c)}</th>" for c in t.get("headers", []))
        rows = "".join("<tr>" + "".join(f"<td>{esc(c)}</td>" for c in r) + "</tr>" for r in t.get("rows", []))
        body = (kicker_html(s) + title_html(s)
                + f'<div class="t-wrap"><table><thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table></div>')

    elif layout == "image":
        uri = resolve_img(s.get("image"), base_dir, embed)
        img = (f'<img src="{esc(uri)}" alt="{esc(s.get("caption",""))}"/>' if uri
               else f'<div class="img-missing">[이미지 없음: {esc(s.get("image",""))}]</div>')
        cap = f'<div class="i-cap">{esc(s["caption"])}</div>' if s.get("caption") else ""
        side = "".join(f"<p>{esc(p)}</p>" for p in s.get("body", []))
        body = (kicker_html(s) + title_html(s)
                + f'<div class="img-slide">{img}{cap}{("<div class=i-body>"+side+"</div>") if side else ""}</div>')

    elif layout == "stat":
        cards = "".join(
            f'<div class="stat-card"><div class="sv">{esc(x.get("value",""))}</div>'
            f'<div class="sl">{esc(x.get("label",""))}</div>'
            + (f'<div class="sd">{esc(x["desc"])}</div>' if x.get("desc") else "")
            + "</div>"
            for x in s.get("stats", [])
        )
        note = f'<div class="stat-note">{esc(s["note"])}</div>' if s.get("note") else ""
        body = (kicker_html(s) + title_html(s)
                + f'<div class="stats stats-{min(len(s.get("stats",[]) or [1]),4)}">{cards}</div>{note}')

    elif layout == "quote":
        body = (
            '<div class="quote-slide"><blockquote>'
            + esc(s.get("body", "")) + "</blockquote>"
            + (f'<div class="cite">— {esc(s["cite"])}</div>' if s.get("cite") else "")
            + "</div>"
        )

    elif layout == "closing":
        body = (
            '<div class="cover closing">'
            + f'<h1>{esc(s.get("title","THANK YOU"))}</h1>'
            + (f'<div class="cover-sub">{esc(s["message"])}</div>' if s.get("message") else "")
            + (f'<div class="cta">{esc(s["cta"])}</div>' if s.get("cta") else "")
            + "</div>"
        )

    else:  # bullets (기본)
        body = kicker_html(s) + title_html(s) + bullets_to_html(s.get("bullets"))

    return f'<section class="slide layout-{esc(layout)}" data-idx="{idx}">{body}<div class="pageno">{idx}</div></section>'


CSS_TEMPLATE = """
:root{--accent:%(accent)s;--soft:%(soft)s;--ink:%(ink)s;--deepbg:%(bg)s}
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%%;background:var(--deepbg);
  font-family:"Pretendard","Pretendard Variable",-apple-system,"Apple SD Gothic Neo","Malgun Gothic",system-ui,sans-serif}
.deck{display:flex;align-items:center;justify-content:center;min-height:100vh;padding:24px}
.slide{position:relative;width:min(96vw,1280px);aspect-ratio:16/9;background:#fff;color:var(--ink);
  border-radius:14px;box-shadow:0 24px 60px rgba(0,0,0,.45);padding:6%% 7%%;overflow:hidden;
  display:none;flex-direction:column;justify-content:center}
.slide.active{display:flex}
.s-kicker{color:var(--accent);font-weight:800;font-size:1.05vw;letter-spacing:.12em;text-transform:uppercase;margin-bottom:1.2vw}
.s-title{font-size:3vw;font-weight:800;line-height:1.25;margin-bottom:1.6vw;color:var(--ink)}
.s-bullets{list-style:none;font-size:1.7vw;line-height:1.7}
.s-bullets>li{position:relative;padding-left:1.6vw;margin:.7vw 0}
.s-bullets>li::before{content:"";position:absolute;left:0;top:.85vw;width:.7vw;height:.7vw;background:var(--accent);border-radius:50%%}
.s-bullets ul{list-style:none;font-size:1.3vw;color:#555;margin:.3vw 0 .3vw 1.6vw}
.s-bullets ul li{padding-left:1.2vw;position:relative}
.s-bullets ul li::before{content:"–";position:absolute;left:0;color:var(--accent)}
/* cover */
.cover{height:100%%;display:flex;flex-direction:column;justify-content:center;
  background:linear-gradient(135deg,var(--accent),var(--deepbg));color:#fff;
  margin:-6%% -7%%;padding:6%% 7%%;border-radius:14px}
.cover h1{font-size:4vw;font-weight:800;line-height:1.2}
.cover-sub{font-size:1.9vw;opacity:.92;margin-top:1.4vw}
.cover-meta{font-size:1.1vw;opacity:.75;margin-top:2.4vw}
.cover .badge{display:inline-block;align-self:flex-start;background:rgba(255,255,255,.18);
  padding:.4vw 1.2vw;border-radius:30px;font-size:1vw;font-weight:700;margin-bottom:1.6vw}
.closing .cta{margin-top:2vw;font-size:1.4vw;font-weight:700;background:rgba(255,255,255,.16);
  align-self:flex-start;padding:.6vw 1.4vw;border-radius:10px}
/* section */
.section-slide{border-left:.5vw solid var(--accent);padding-left:2.4vw}
.sec-index{font-size:1.4vw;font-weight:800;color:var(--accent)}
.sec-title{font-size:3.6vw;font-weight:800;margin:.6vw 0}
.sec-sub{font-size:1.6vw;color:#555}
/* two-column */
.two-col{display:grid;grid-template-columns:1fr 1fr;gap:2.4vw;margin-top:1vw}
.col{background:var(--soft);border-radius:10px;padding:2vw}
.col-label{font-weight:800;font-size:1.5vw;color:var(--accent);margin-bottom:1vw}
.col p{font-size:1.3vw;line-height:1.6;margin:.4vw 0}
.col-metric{margin:.6vw 0 1vw}
.col-metric .mv{font-size:2.8vw;font-weight:800;color:var(--ink)}
.col-metric .ml{font-size:1.1vw;color:#666;margin-left:.6vw}
.col ul{list-style:none;font-size:1.25vw;line-height:1.6}
.col ul li{padding-left:1.2vw;position:relative;margin:.3vw 0}
.col ul li::before{content:"";position:absolute;left:0;top:.7vw;width:.5vw;height:.5vw;background:var(--accent);border-radius:50%%}
/* table */
.t-wrap{overflow:auto;margin-top:1vw}
table{border-collapse:collapse;width:100%%;font-size:1.25vw}
th,td{border:1px solid #e3ddd2;padding:.7vw 1vw;text-align:left}
thead th{background:var(--accent);color:#fff;font-weight:700}
tbody tr:nth-child(even){background:var(--soft)}
/* image */
.img-slide{display:flex;flex-direction:column;align-items:center;gap:1vw;margin-top:.6vw}
.img-slide img{max-width:100%%;max-height:62vh;border-radius:10px;border:1px solid #e3ddd2}
.i-cap{font-size:1.1vw;color:#666}
.i-body{font-size:1.3vw;color:#444;align-self:stretch}
.img-missing{color:#b03030;background:#fff3f3;border:1px dashed #e0a0a0;padding:2vw;border-radius:10px;font-size:1.2vw}
/* stat */
.stats{display:grid;gap:1.8vw;margin-top:1.4vw}
.stats-1{grid-template-columns:1fr}.stats-2{grid-template-columns:1fr 1fr}
.stats-3{grid-template-columns:repeat(3,1fr)}.stats-4{grid-template-columns:repeat(4,1fr)}
.stat-card{background:var(--soft);border-radius:12px;padding:2vw;text-align:center;border-top:.4vw solid var(--accent)}
.stat-card .sv{font-size:3.4vw;font-weight:800;color:var(--accent);line-height:1.1}
.stat-card .sl{font-size:1.3vw;font-weight:700;margin-top:.6vw}
.stat-card .sd{font-size:1vw;color:#666;margin-top:.4vw}
.stat-note{font-size:1vw;color:#888;margin-top:1.4vw;text-align:center}
/* quote */
.quote-slide{text-align:center;max-width:80%%;margin:0 auto}
.quote-slide blockquote{font-size:2.6vw;font-weight:700;line-height:1.5;color:var(--ink)}
.quote-slide blockquote::before{content:"\\201C";color:var(--accent);font-size:4vw;vertical-align:-.6vw;margin-right:.2vw}
.quote-slide .cite{font-size:1.3vw;color:#666;margin-top:1.6vw}
/* chrome */
.pageno{position:absolute;right:2.4vw;bottom:1.8vw;font-size:1vw;color:#bbb;font-weight:700}
.layout-title .pageno,.layout-closing .pageno{display:none}
.nav{position:fixed;bottom:18px;left:50%%;transform:translateX(-50%%);display:flex;gap:10px;align-items:center;
  background:rgba(0,0,0,.45);backdrop-filter:blur(6px);padding:8px 14px;border-radius:30px;color:#fff;font-size:13px}
.nav button{background:rgba(255,255,255,.15);color:#fff;border:none;width:30px;height:30px;border-radius:50%%;cursor:pointer;font-size:15px}
.nav button:hover{background:rgba(255,255,255,.3)}
.nav .count{min-width:64px;text-align:center;font-weight:700}
.hint{position:fixed;top:14px;right:16px;color:rgba(255,255,255,.5);font-size:12px}
@media print{
  @page{size:landscape;margin:0}
  body,html{background:#fff}
  .deck{display:block;padding:0}
  .slide{display:flex!important;width:100%%;aspect-ratio:auto;height:100vh;box-shadow:none;border-radius:0;page-break-after:always}
  .nav,.hint{display:none!important}
}
"""

JS = """
const slides=[...document.querySelectorAll('.slide')];let cur=0;
const count=document.querySelector('.count');
function show(i){cur=Math.max(0,Math.min(slides.length-1,i));
  slides.forEach((s,k)=>s.classList.toggle('active',k===cur));
  if(count)count.textContent=(cur+1)+' / '+slides.length;
  location.hash=cur+1;}
function next(){show(cur+1)}function prev(){show(cur-1)}
document.addEventListener('keydown',e=>{
  if(['ArrowRight',' ','PageDown'].includes(e.key)){e.preventDefault();next()}
  else if(['ArrowLeft','PageUp'].includes(e.key)){e.preventDefault();prev()}
  else if(e.key==='Home')show(0);else if(e.key==='End')show(slides.length-1);
  else if(e.key==='f'||e.key==='F'){if(!document.fullscreenElement)document.documentElement.requestFullscreen();else document.exitFullscreen()}});
const h=parseInt((location.hash||'').slice(1));show(isNaN(h)?0:h-1);
"""


def main() -> int:
    ap = argparse.ArgumentParser(description="deck.json → 자립형 HTML 슬라이드 (bizplan)")
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--base-dir", default="")
    ap.add_argument("--no-embed", action="store_true")
    args = ap.parse_args()

    if not os.path.exists(args.input):
        print(f"[오류] 입력 파일 없음: {args.input}", file=sys.stderr)
        return 1
    try:
        with open(args.input, encoding="utf-8") as f:
            deck = json.load(f)
    except json.JSONDecodeError as e:
        print(f"[오류] deck.json 파싱 실패: {e}", file=sys.stderr)
        return 1

    base_dir = args.base_dir or os.path.dirname(os.path.abspath(args.input))
    embed = not args.no_embed
    theme = THEMES.get(deck.get("theme", "navy"), THEMES["navy"])
    slides = deck.get("slides", [])
    if not slides:
        print("[오류] slides 가 비어 있습니다.", file=sys.stderr)
        return 1

    rendered = "\n".join(render_slide(s, i + 1, base_dir, embed) for i, s in enumerate(slides))
    css = CSS_TEMPLATE % theme
    title = deck.get("title", "Pitch Deck")

    doc = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{esc(title)}</title>
<link rel="stylesheet" as="style" crossorigin
  href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css"/>
<style>{css}</style>
</head>
<body>
<div class="hint">← → 이동 · F 풀스크린</div>
<div class="deck">
{rendered}
</div>
<div class="nav"><button onclick="prev()">‹</button><span class="count"></span><button onclick="next()">›</button></div>
<script>{JS}</script>
</body>
</html>"""

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"[완료] HTML 덱 생성: {args.output}  (슬라이드 {len(slides)}개 / 테마 {deck.get('theme','navy')})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
