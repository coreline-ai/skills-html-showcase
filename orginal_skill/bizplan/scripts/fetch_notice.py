#!/usr/bin/env python3
"""
fetch_notice.py — 공고 페이지 + 첨부파일 수집기 (PRD §7.2 / SKILL.md Gate 0)

동작:
  ① 공고 페이지 HTML 저장(00-source/notice/page.html) + 본문 텍스트 추출(notice/page.txt)
  ② 페이지 내 링크 중 첨부파일(.pdf .hwp .hwpx .doc .docx .xls .xlsx .zip) 탐색 → attachments/ 다운로드
  ③ ZIP 은 해제해 분류(attachments/<원본명>_unzipped/)
  ④ 다운로드 성공/실패 목록을 00-source/fetch-report.md 로 기록
  ⑤ User-Agent 설정, 타임아웃, 일부 실패해도 부분 성공 보고

규칙:
  - 로그인/유료 자료는 우회하지 않는다. 차단(401/403/402/로그인 리다이렉트)은
    fetch-report.md 에 "수동 다운로드 필요"로 표기한다.
  - requests 가 있으면 사용하고 없으면 표준 라이브러리(urllib) 로 동작한다.
  - SSL 검증 실패 시 명확히 안내한다(자동 우회하지 않음 — 사용자 판단).

사용:
  python3 scripts/fetch_notice.py <url> --out <00-source 경로>
  python3 scripts/fetch_notice.py https://example.gov/notice/123 --out bizplan-foo/00-source
"""
import argparse
import os
import re
import ssl
import sys
import zipfile
from datetime import datetime, timezone
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse, unquote

# ── 선택적 requests 사용 (없으면 urllib) ──────────────────────────────────────
try:
    import requests  # type: ignore

    _HAVE_REQUESTS = True
except Exception:  # pragma: no cover - 환경 의존
    _HAVE_REQUESTS = False

import urllib.error
import urllib.request

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36 bizplan-fetch/1.0"
)
TIMEOUT = 30  # 초
ATTACH_EXTS = (".pdf", ".hwp", ".hwpx", ".doc", ".docx", ".xls", ".xlsx", ".zip")
MAX_BYTES = 80 * 1024 * 1024  # 첨부 1개 상한 80MB (방어적)


# ── HTML 파서: 링크 수집 + 본문 텍스트 추출 ──────────────────────────────────
class _Extractor(HTMLParser):
    """앵커 href 수집 + 스크립트/스타일 제외 본문 텍스트 추출."""

    _SKIP = {"script", "style", "noscript", "head", "title"}
    _BLOCK = {"p", "div", "br", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6", "section", "article"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, str]] = []  # (href, 링크텍스트)
        self._text_parts: list[str] = []
        self._skip_depth = 0
        self._cur_link: str | None = None
        self._cur_link_text: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag in self._SKIP:
            self._skip_depth += 1
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self._cur_link = href
                self._cur_link_text = []
        if tag in self._BLOCK:
            self._text_parts.append("\n")

    def handle_endtag(self, tag):
        if tag in self._SKIP and self._skip_depth > 0:
            self._skip_depth -= 1
        if tag == "a" and self._cur_link is not None:
            self.links.append((self._cur_link, " ".join(self._cur_link_text).strip()))
            self._cur_link = None
            self._cur_link_text = []
        if tag in self._BLOCK:
            self._text_parts.append("\n")

    def handle_data(self, data):
        if self._skip_depth > 0:
            return
        self._text_parts.append(data)
        if self._cur_link is not None:
            self._cur_link_text.append(data.strip())

    def get_text(self) -> str:
        raw = "".join(self._text_parts)
        # 다중 공백/개행 정리
        lines = [re.sub(r"[ \t]+", " ", ln).strip() for ln in raw.splitlines()]
        out: list[str] = []
        blank = False
        for ln in lines:
            if not ln:
                if not blank:
                    out.append("")
                blank = True
            else:
                out.append(ln)
                blank = False
        return "\n".join(out).strip()


# ── HTTP 헬퍼 ─────────────────────────────────────────────────────────────────
class FetchError(Exception):
    def __init__(self, message: str, manual: bool = False) -> None:
        super().__init__(message)
        self.manual = manual  # 수동 다운로드 필요 여부


def _http_get(url: str, *, binary: bool) -> tuple[bytes, str, str]:
    """URL 을 GET 한다. (본문bytes, content_type, final_url) 반환. 차단/오류 시 FetchError."""
    if _HAVE_REQUESTS:
        try:
            r = requests.get(url, headers={"User-Agent": UA}, timeout=TIMEOUT, allow_redirects=True, stream=binary)
            status = r.status_code
            final_url = r.url
            if status in (401, 402, 403):
                raise FetchError(f"접근 차단(HTTP {status}) — 로그인/권한 필요", manual=True)
            if status >= 400:
                raise FetchError(f"HTTP {status}")
            if binary:
                data = b""
                for chunk in r.iter_content(64 * 1024):
                    data += chunk
                    if len(data) > MAX_BYTES:
                        raise FetchError(f"첨부 크기 초과(>{MAX_BYTES // (1024*1024)}MB) — 수동 다운로드 권장", manual=True)
            else:
                data = r.content
            return data, r.headers.get("Content-Type", ""), final_url
        except requests.exceptions.SSLError as e:  # type: ignore
            raise FetchError(f"SSL 검증 실패 — 사이트 인증서를 확인하세요(자동 우회 안 함): {e}", manual=True)
        except FetchError:
            raise
        except requests.exceptions.RequestException as e:  # type: ignore
            raise FetchError(f"요청 실패: {e}")

    # ── urllib fallback ──
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            ct = resp.headers.get("Content-Type", "")
            final_url = resp.geturl()
            data = b""
            while True:
                chunk = resp.read(64 * 1024)
                if not chunk:
                    break
                data += chunk
                if len(data) > MAX_BYTES:
                    raise FetchError(f"첨부 크기 초과(>{MAX_BYTES // (1024*1024)}MB) — 수동 다운로드 권장", manual=True)
            return data, ct, final_url
    except urllib.error.HTTPError as e:
        if e.code in (401, 402, 403):
            raise FetchError(f"접근 차단(HTTP {e.code}) — 로그인/권한 필요", manual=True)
        raise FetchError(f"HTTP {e.code}")
    except ssl.SSLError as e:
        raise FetchError(f"SSL 검증 실패 — 사이트 인증서를 확인하세요(자동 우회 안 함): {e}", manual=True)
    except urllib.error.URLError as e:
        reason = getattr(e, "reason", e)
        if isinstance(reason, ssl.SSLError):
            raise FetchError(f"SSL 검증 실패 — 사이트 인증서를 확인하세요(자동 우회 안 함): {reason}", manual=True)
        raise FetchError(f"연결 실패: {reason}")


def _safe_name(url: str) -> str:
    """URL 에서 안전한 파일명 추출."""
    path = urlparse(url).path
    name = unquote(os.path.basename(path)) or "download"
    name = re.sub(r"[^\w가-힣.\-]+", "_", name).strip("_")
    return name or "download"


def _looks_login(final_url: str, original: str) -> bool:
    """로그인 페이지로 리다이렉트됐는지 휴리스틱 판정."""
    fu = final_url.lower()
    return any(k in fu for k in ("login", "signin", "auth", "sso")) and "login" not in original.lower()


# ── 메인 ──────────────────────────────────────────────────────────────────────
def main() -> int:
    ap = argparse.ArgumentParser(description="bizplan 공고 페이지+첨부 수집기")
    ap.add_argument("url", help="공고 페이지 URL")
    ap.add_argument("--out", required=True, help="00-source 디렉토리 경로")
    args = ap.parse_args()

    out_root = os.path.abspath(args.out)
    notice_dir = os.path.join(out_root, "notice")
    attach_dir = os.path.join(out_root, "attachments")
    os.makedirs(notice_dir, exist_ok=True)
    os.makedirs(attach_dir, exist_ok=True)

    report: list[str] = []
    report.append(f"# 공고 수집 보고서\n")
    report.append(f"- 수집 시각: {_now()}")
    report.append(f"- 대상 URL: {args.url}")
    report.append(f"- HTTP 클라이언트: {'requests' if _HAVE_REQUESTS else 'urllib(표준 라이브러리)'}")
    report.append("")

    # ── ① 페이지 HTML + 본문 텍스트 ──
    page_html = ""
    extractor: _Extractor | None = None
    try:
        data, ct, final_url = _http_get(args.url, binary=False)
        page_html = data.decode("utf-8", errors="replace")
        with open(os.path.join(notice_dir, "page.html"), "w", encoding="utf-8") as f:
            f.write(page_html)
        extractor = _Extractor()
        extractor.feed(page_html)
        text = extractor.get_text()
        with open(os.path.join(notice_dir, "page.txt"), "w", encoding="utf-8") as f:
            f.write(text)
        report.append("## ① 공고 페이지")
        report.append(f"- [성공] page.html ({len(page_html):,} chars), page.txt ({len(text):,} chars)")
        if _looks_login(final_url, args.url):
            report.append(f"- ⚠ **로그인 페이지로 리다이렉트된 듯합니다** ({final_url}) — 수동 확인 필요")
        report.append("")
    except FetchError as e:
        report.append("## ① 공고 페이지")
        tag = "수동 다운로드 필요" if e.manual else "실패"
        report.append(f"- [{tag}] {e}")
        report.append("")
        _write_report(out_root, report)
        print(f"[부분 실패] 페이지 수집 실패: {e}", file=sys.stderr)
        # 페이지를 못 받으면 첨부도 탐색 불가 → 여기서 종료(부분 보고는 남김)
        return 2

    # ── ② 첨부 링크 탐색 ──
    base = final_url if final_url else args.url
    candidates: list[tuple[str, str]] = []  # (절대URL, 라벨)
    seen: set[str] = set()
    for href, label in (extractor.links if extractor else []):
        if not href or href.startswith(("javascript:", "mailto:", "#")):
            continue
        absu = urljoin(base, href)
        ext = os.path.splitext(urlparse(absu).path)[1].lower()
        if ext in ATTACH_EXTS and absu not in seen:
            seen.add(absu)
            candidates.append((absu, label))

    report.append("## ② 첨부파일")
    report.append(f"- 탐지된 첨부 후보: {len(candidates)}개")
    report.append("")

    ok, fail, manual = 0, 0, 0
    downloaded: list[str] = []
    if not candidates:
        report.append("- (다운로드 가능한 첨부 링크 패턴을 찾지 못했습니다. 페이지가 JS 로 링크를 생성하거나, "
                       "첨부가 별도 다운로드 시스템에 있을 수 있습니다 — page.html 을 직접 확인하세요.)")
        report.append("")

    for absu, label in candidates:
        fname = _safe_name(absu)
        dest = os.path.join(attach_dir, fname)
        # 동일 파일명 충돌 회피
        if os.path.exists(dest):
            stem, ext = os.path.splitext(fname)
            n = 1
            while os.path.exists(os.path.join(attach_dir, f"{stem}_{n}{ext}")):
                n += 1
            dest = os.path.join(attach_dir, f"{stem}_{n}{ext}")
        try:
            data, ct, _fu = _http_get(absu, binary=True)
            with open(dest, "wb") as f:
                f.write(data)
            ok += 1
            downloaded.append(dest)
            size_kb = len(data) / 1024
            lbl = f" — {label}" if label else ""
            report.append(f"- [성공] `{os.path.basename(dest)}` ({size_kb:,.0f} KB){lbl}")
        except FetchError as e:
            if e.manual:
                manual += 1
                report.append(f"- [수동 다운로드 필요] {absu}\n    - 사유: {e}")
            else:
                fail += 1
                report.append(f"- [실패] {absu}\n    - 사유: {e}")

    report.append("")

    # ── ③ ZIP 해제·분류 ──
    zips = [d for d in downloaded if d.lower().endswith(".zip")]
    if zips:
        report.append("## ③ ZIP 해제")
        for zp in zips:
            outdir = os.path.splitext(zp)[0] + "_unzipped"
            try:
                os.makedirs(outdir, exist_ok=True)
                extracted: list[str] = []
                with zipfile.ZipFile(zp) as zf:
                    for member in zf.namelist():
                        # zip-slip 방어
                        target = os.path.realpath(os.path.join(outdir, member))
                        if not target.startswith(os.path.realpath(outdir) + os.sep) and target != os.path.realpath(outdir):
                            report.append(f"- [건너뜀] 위험한 경로 무시: {member}")
                            continue
                        zf.extract(member, outdir)
                        if not member.endswith("/"):
                            extracted.append(member)
                report.append(f"- [성공] `{os.path.basename(zp)}` → {os.path.basename(outdir)}/ ({len(extracted)}개 파일)")
                # 확장자별 분류 요약
                by_ext: dict[str, int] = {}
                for m in extracted:
                    e = os.path.splitext(m)[1].lower() or "(확장자없음)"
                    by_ext[e] = by_ext.get(e, 0) + 1
                if by_ext:
                    report.append("    - 분류: " + ", ".join(f"{k} {v}개" for k, v in sorted(by_ext.items())))
            except zipfile.BadZipFile:
                report.append(f"- [실패] `{os.path.basename(zp)}` — 손상되었거나 ZIP 이 아닙니다")
        report.append("")

    # ── ④ 요약 ──
    report.append("## 요약")
    report.append(f"- 첨부 성공 {ok}개 / 실패 {fail}개 / 수동 필요 {manual}개")
    if manual:
        report.append("- ⚠ 일부 자료는 로그인/권한/크기 제한으로 **수동 다운로드**가 필요합니다(위 목록 참조).")
    report.append("")

    _write_report(out_root, report)

    print(f"[완료] 페이지 저장 + 첨부 성공 {ok} / 실패 {fail} / 수동 {manual}")
    print(f"  보고서: {os.path.join(out_root, 'fetch-report.md')}")
    # 부분 성공도 0 으로 종료(페이지는 받았으므로). 페이지 자체 실패만 비0(위에서 처리).
    return 0


def _write_report(out_root: str, lines: list[str]) -> None:
    with open(os.path.join(out_root, "fetch-report.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines).rstrip() + "\n")


def _now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


if __name__ == "__main__":
    raise SystemExit(main())
