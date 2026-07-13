#!/usr/bin/env python3
"""
Read-only browser/web collector for x-ai-trend-collector.

This helper does NOT use X API credentials and does NOT perform any engagement action.
It normalizes visible browser content into the records.json schema consumed by
build_outputs.py.

Supported inputs:
- --input copied_or_saved_page.html / .txt files from Chrome/Safari/browser tools
- --url public web pages (best-effort urllib fetch; JavaScript-heavy pages may need
  browser copy/save instead)
- stdin when no --input/--url is provided

It is intentionally heuristic: browser-visible metrics can be hidden, rounded, or
unavailable. Missing metrics become 0 rather than guessed.
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen

CATEGORIES = ["신규 모델·제품 출시", "연구·논문 동향", "업계·투자 뉴스", "실무 팁·도구"]
STOPWORDS = {
    "post", "reply", "repost", "like", "likes", "views", "view", "share", "copy", "link",
    "for", "the", "and", "with", "this", "that", "from", "http", "https", "com", "status",
}
URL_RE = re.compile(r"https?://[^\s\"'<>]+")
STATUS_RE = re.compile(r"https?://(?:www\.)?(?:x|twitter)\.com/([^/\s\"'<>]+)/status/(\d+)[^\s\"'<>]*", re.I)
HANDLE_RE = re.compile(r"@([A-Za-z0-9_]{2,20})")
DATE_RE = re.compile(r"\b(20\d{2}[-./]\d{1,2}[-./]\d{1,2}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+20\d{2})\b", re.I)
METRIC_TOKEN_RE = re.compile(r"(?P<num>\d+(?:\.\d+)?)\s*(?P<suf>[kKmM]|만|천)?")


class VisibleTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.skip = 0
        self.parts: list[str] = []
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs):
        if tag in {"script", "style", "noscript", "svg"}:
            self.skip += 1
        for key, value in attrs:
            if key.lower() == "href" and value:
                link = html.unescape(value)
                self.links.append(link)
                # Inject links into visible text so a saved/copy browser page keeps
                # the surrounding article text attached to the source URL.
                self.parts.append(f"\n{link}\n")
        if tag in {"article", "div", "p", "li", "br", "section", "time"}:
            self.parts.append("\n")

    def handle_endtag(self, tag: str):
        if tag in {"script", "style", "noscript", "svg"} and self.skip:
            self.skip -= 1
        if tag in {"article", "p", "li", "section"}:
            self.parts.append("\n")

    def handle_data(self, data: str):
        if not self.skip and data.strip():
            self.parts.append(data.strip())


def html_to_visible(raw: str) -> tuple[str, list[str]]:
    parser = VisibleTextParser()
    parser.feed(raw)
    text = html.unescape("\n".join(parser.parts))
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip(), parser.links


def fetch_url(url: str) -> str:
    req = Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X) AppleWebKit/537.36 Chrome-like read-only collector",
        "Accept": "text/html,application/xhtml+xml,text/plain;q=0.9,*/*;q=0.8",
    })
    with urlopen(req, timeout=20) as res:
        raw = res.read()
    return raw.decode("utf-8", errors="replace")


def metric_to_int(token: str) -> int:
    m = METRIC_TOKEN_RE.search(token.replace(",", ""))
    if not m:
        return 0
    n = float(m.group("num"))
    suf = (m.group("suf") or "").lower()
    if suf == "k" or suf == "천":
        n *= 1_000
    elif suf == "m":
        n *= 1_000_000
    elif suf == "만":
        n *= 10_000
    return int(n)


def classify(text: str) -> str:
    low = text.lower()
    if any(k in low for k in ["paper", "arxiv", "benchmark", "research", "eval", "논문", "연구", "벤치마크"]):
        return "연구·논문 동향"
    if any(k in low for k in ["funding", "raised", "acquire", "ipo", "startup", "enterprise", "투자", "인수", "기업"]):
        return "업계·투자 뉴스"
    if any(k in low for k in ["tool", "agent", "workflow", "automation", "prompt", "코딩", "도구", "자동화", "에이전트"]):
        return "실무 팁·도구"
    return "신규 모델·제품 출시"


def summarize(text: str) -> str:
    cleaned = re.sub(r"https?://\S+", "", text)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    if not cleaned:
        return "브라우저에서 보이는 원문 텍스트가 부족해 요약을 생성하지 못했습니다. 링크를 열어 원문을 확인하세요."
    # Deterministic source-bound summary, not an invented interpretation.
    snippet = cleaned[:220].rstrip()
    return f"브라우저에서 확인된 내용: {snippet}{'…' if len(cleaned) > 220 else ''}"


def guess_author(block: str, handle: str) -> str:
    lines = [ln.strip() for ln in block.splitlines() if ln.strip()]
    for ln in lines[:6]:
        if ln.startswith("@") or "http" in ln.lower():
            continue
        if len(ln) <= 60 and not any(word in ln.lower() for word in ["reply", "repost", "like", "view"]):
            return ln
    return handle or "Unknown"


def guess_metrics(block: str) -> tuple[int, int]:
    views = likes = 0
    for line in block.splitlines():
        low = line.lower()
        if "view" in low or "조회" in low:
            views = max(views, metric_to_int(line))
        if "like" in low or "좋아요" in low or "마음" in low:
            likes = max(likes, metric_to_int(line))
    return views, likes


def blocks_from_text(text: str, links: list[str]) -> list[tuple[str, str]]:
    urls = []
    for url in links + URL_RE.findall(text):
        if STATUS_RE.search(url):
            clean = url.rstrip(").,;]")
            if clean not in urls:
                urls.append(clean)
    if not urls:
        # fallback: split visible feed by blank lines and synthesize no-url records later
        return [("", b) for b in re.split(r"\n\s*\n", text) if len(b.strip()) > 80]
    blocks: list[tuple[str, str]] = []
    positioned = []
    for url in urls:
        pos = text.find(url)
        positioned.append((pos if pos >= 0 else 10**12, url))
    positioned.sort()
    for idx, (pos, url) in enumerate(positioned):
        if pos < 10**12:
            next_pos = positioned[idx + 1][0] if idx + 1 < len(positioned) and positioned[idx + 1][0] < 10**12 else len(text)
            # Saved browser HTML often places href before the visible article text;
            # keep the segment until the next status URL instead of stopping at the
            # first blank line after the link.
            start = max(0, text.rfind("\n\n", 0, pos))
            block = text[start:next_pos]
        else:
            m = STATUS_RE.search(url)
            handle = f"@{m.group(1)}" if m else ""
            block = f"{handle}\n{url}"
        blocks.append((url, block.strip()))
    return blocks


def normalize_sources(sources: list[tuple[str, str]]) -> list[dict]:
    today = dt.date.today().isoformat()
    records: list[dict] = []
    seen = set()
    for idx, (url, block) in enumerate(sources, 1):
        if url and url in seen:
            continue
        seen.add(url or f"no-url-{idx}")
        status = STATUS_RE.search(url or block)
        handle = ""
        if status:
            handle = "@" + status.group(1)
        else:
            hm = HANDLE_RE.search(block)
            handle = "@" + hm.group(1) if hm else ""
        dm = DATE_RE.search(block)
        date = dm.group(1).replace("/", "-").replace(".", "-") if dm else today
        views, likes = guess_metrics(block)
        author = guess_author(block, handle)
        body = "\n".join(ln for ln in block.splitlines() if not URL_RE.search(ln))
        records.append({
            "cat": classify(block),
            "author": author,
            "handle": handle,
            "date": date,
            "summary": summarize(body),
            "url": url,
            "views": views,
            "likes": likes,
        })
    return records


def main() -> int:
    ap = argparse.ArgumentParser(description="Normalize browser-visible social/web feed content into x-ai-trend-collector records.json")
    ap.add_argument("--input", action="append", default=[], help="Copied/saved browser HTML or text file. Repeatable.")
    ap.add_argument("--url", action="append", default=[], help="Public URL to fetch read-only. JavaScript-heavy pages may require --input from saved browser content.")
    ap.add_argument("--output", required=True, help="Output records.json path")
    ap.add_argument("--limit", type=int, default=25)
    args = ap.parse_args()

    chunks: list[str] = []
    source_urls: list[str] = []
    for path in args.input:
        chunks.append(Path(path).read_text(encoding="utf-8", errors="replace"))
    for url in args.url:
        source_urls.append(url)
        chunks.append(fetch_url(url))
    if not chunks and not sys.stdin.isatty():
        chunks.append(sys.stdin.read())
    if not chunks:
        ap.error("provide --input, --url, or stdin")

    all_records: list[dict] = []
    for raw in chunks:
        if re.search(r"<html|<body|<article|<div|href=", raw, re.I):
            text, links = html_to_visible(raw)
        else:
            text, links = raw, []
        all_records.extend(normalize_sources(blocks_from_text(text, links)))

    # Dedupe by URL first, then summary for no-url records.
    out = []
    seen = set()
    for rec in all_records:
        key = rec["url"] or rec["summary"][:120]
        if key in seen:
            continue
        seen.add(key)
        out.append(rec)
        if len(out) >= args.limit:
            break

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "mode": "browser_or_web_readonly",
        "inputs": len(chunks),
        "source_urls": source_urls,
        "records": len(out),
        "output": str(output),
        "caveat": "No X API used. Browser-visible content may omit metrics or require logged-in/manual saved input for JavaScript-heavy pages.",
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
