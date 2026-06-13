#!/usr/bin/env python3
"""Adaptive HTML qualitative contract guard.

This checker intentionally complements, not replaces, validate_output.py.
validate_output.py verifies deterministic HTML/CSS/no-JS contracts; this file
guards against low-quality "stamp-template" outputs that still happen to be
valid HTML.

It is intentionally conservative:
- checks body markup, not inlined CSS;
- skips index pages as navigation shells;
- reports hard failures only for obvious placeholder/generic/repetition smells.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


FORBIDDEN_TEXT_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("generated_example_phrase", re.compile(r"Generated example|mode example", re.I)),
    ("example_document_phrase", re.compile(r"전문\s*예제|예제\s*문서")),
    ("placeholder_phrase", re.compile(r"\bPLACEHOLDER\b|Lorem ipsum|TBD|TODO\s*:", re.I)),
    # Self-referential "template/widget usage proof" meta prose (SKILL.md §7 / Step 4.1 #6 금지).
    # A real document must end in actual judgment, not a description of which vt/wg it used.
    # These exact phrases shipped in the v5.x examples' "모드 정본 템플릿 적용 확인" appendix; the
    # vt/wg must be embedded in-body with real topic data instead (see examples 15/16/17).
    ("template_demo_meta_phrase", re.compile(
        r"모드\s*정본\s*템플릿\s*적용\s*확인"
        r"|실제\s*HTML\s*템플릿으로\s*삽입했습니다"
        r"|보강\s*템플릿으로\s*포함했습니다"
        r"|시각적으로\s*확인하기\s*위한\s*섹션")),
    # Contract-scaffold hook that must never ship in an output BODY (the CSS rule in <head> is fine).
    ("template_contract_scaffold", re.compile(r"""data-ahf-contract\s*=\s*["']?mode-template""")),
]

REPEATED_PLACEHOLDER_PATTERNS: list[tuple[str, re.Pattern[str], int]] = [
    ("numbered_generic_criteria", re.compile(r"기준\s*[0-9]+"), 3),
    ("numbered_generic_section", re.compile(r"섹션\s*[0-9]+"), 3),
]

TRY_CARD_CONTRAST_CLASSES = (
    "repo-card",
    "repo-signal",
    "repo-question",
    "repo-evidence",
    "youtube-card",
    "youtube-signal",
    "youtube-evidence",
    "youtube-opportunity",
    "manual-card",
    "manual-step",
    "manual-role",
    "manual-trouble",
)

CANONICAL_CONTENT_PATTERN = re.compile(
    r"\b(?:box|card|grid|summary-card|toc-map|source-note|source-box|source-list|term|analogy|danger|good|"
    r"tbl|table-scroll|matrix|vt-|wg-|flow|timeline|checklist|quality|risk|decision|repo-|youtube-|manual-|"
    r"serp-|platform-|landing-|case-|feature-|text-bullet-view|core-insight|conn-grid|impact-grid|ba\b|"
    r"a11y-check|chron-list|source-preserve|md-excerpt)\b",
    re.I,
)
PROSE_RELAXED_LAYOUTS = {"layout-blog", "layout-article"}


@dataclass
class Issue:
    file: Path
    code: str
    detail: str

    def format(self, root: Path) -> str:
        try:
            rel = self.file.relative_to(root)
        except ValueError:
            rel = self.file
        return f"ISSUE {rel}: {self.code} — {self.detail}"


def body_fragment(html: str) -> str:
    match = re.search(r"<body\b[^>]*>(.*)</body>", html, re.I | re.S)
    if match:
        return match.group(1)
    body_start = html.lower().find("<body")
    return html[body_start:] if body_start >= 0 else html


def class_tokens(markup: str) -> list[str]:
    tokens: list[str] = []
    for raw in re.findall(r'class=["\']([^"\']+)["\']', markup):
        tokens.extend(raw.split())
    return tokens


def heading_texts(markup: str, tag: str) -> list[str]:
    texts: list[str] = []
    for raw in re.findall(fr"<{tag}\b[^>]*>(.*?)</{tag}>", markup, re.I | re.S):
        text = re.sub(r"<[^>]+>", " ", raw)
        text = re.sub(r"\s+", " ", text).strip()
        if text:
            texts.append(text)
    return texts


def inner_html(text: str, open_end: int, tag: str) -> str:
    depth = 1
    window = text[open_end:]
    for mm in re.finditer(r"<(/?)" + re.escape(tag) + r"\b", window, re.I):
        depth += -1 if mm.group(1) else 1
        if depth == 0:
            return window[: mm.start()]
    return window[:200000]


def direct_child_blocks(html: str, tag: str):
    depth = 0
    tag_l = tag.lower()
    void_tags = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
    token_re = re.compile(r"<(/?)([a-zA-Z][\w:-]*)([^>]*)>", re.I)
    for m in token_re.finditer(html):
        closing = bool(m.group(1))
        name = m.group(2).lower()
        attrs = m.group(3) or ""
        self_closing = attrs.rstrip().endswith("/") or name in void_tags
        if not closing and name == tag_l and depth == 0:
            yield attrs, inner_html(html, m.end(), tag_l)
        if closing:
            depth = max(depth - 1, 0)
        elif not self_closing:
            depth += 1


def layout_class(markup: str) -> str | None:
    mo = re.search(r"<main\b([^>]*)>", markup, re.I)
    if not mo:
        return None
    cm = re.search(r'class\s*=\s*["\']([^"\']*)', mo.group(1), re.I)
    return next((c for c in (cm.group(1).split() if cm else []) if c.startswith("layout-")), None)


def raw_section_synthesis_issues(path: Path, body: str) -> list[Issue]:
    """Block stamp-template sections built only from raw p/div/li blocks.

    This is intentionally a quality-contract check, not a structural validator:
    prose-heavy article/blog pages get a relaxed threshold, while report/manual/
    checklist pages must mix canonical boxes, cards, tables, vt/wg, or editorial
    patterns instead of raw paragraph stacks that cause left-stuck/overlap output.
    """
    layout = layout_class(body)
    if not layout:
        return []
    main = re.search(r"<main\b[^>]*>", body, re.I)
    if not main:
        return []
    main_inner = inner_html(body, main.end(), "main")
    sections = list(direct_child_blocks(main_inner, "section"))
    for _attrs, article_inner in direct_child_blocks(main_inner, "article"):
        sections.extend(direct_child_blocks(article_inner, "section"))
    if len(sections) < 5:
        return []

    raw_sections: list[str] = []
    for attrs, section in sections:
        cm = re.search(r'class\s*=\s*["\']([^"\']*)', attrs, re.I)
        classes = set((cm.group(1) if cm else "").split())
        if "try" in classes:
            continue
        text_blocks = len(re.findall(r"<(?:p|li|div)\b", section, re.I))
        if text_blocks < 4:
            continue
        if CANONICAL_CONTENT_PATTERN.search(attrs + " " + section):
            continue
        h2 = re.search(r"<h2\b[^>]*>([\s\S]*?)</h2>", section, re.I)
        title = re.sub(r"<[^>]+>", " ", h2.group(1) if h2 else "").strip()[:60] or "(untitled)"
        raw_sections.append(title)

    if not raw_sections:
        return []
    if layout in PROSE_RELAXED_LAYOUTS:
        limit = max(4, int(len(sections) * 0.5))
    else:
        limit = max(2, int(len(sections) * 0.25))
    if len(raw_sections) > limit:
        return [
            Issue(
                path,
                "raw_section_synthesis_overuse",
                f"정본 컴포넌트 없이 raw p/div/li 중심 섹션이 {len(raw_sections)}개 > 허용 {limit}개입니다. 예: {', '.join(raw_sections[:3])}",
            )
        ]
    return []


def check_html(path: Path) -> list[Issue]:
    html = path.read_text(encoding="utf-8")
    body = body_fragment(html)
    issues: list[Issue] = []

    for code, pattern in FORBIDDEN_TEXT_PATTERNS:
        if pattern.search(body):
            issues.append(Issue(path, code, "임시/예제 생성 문구가 본문에 남아 있습니다."))

    for code, pattern, max_allowed in REPEATED_PLACEHOLDER_PATTERNS:
        hits = pattern.findall(body)
        if len(hits) >= max_allowed:
            issues.append(
                Issue(
                    path,
                    code,
                    f"'{hits[0]}'류 placeholder가 {len(hits)}회 반복됩니다.",
                )
            )

    tokens = class_tokens(body)
    section_count = len(re.findall(r"<section\b", body, re.I))
    if section_count >= 8:
        mini_count = tokens.count("mini-card")
        col_count = tokens.count("col-list")
        mini_limit = max(18, section_count * 2)
        col_limit = max(6, int(section_count * 0.75))
        if mini_count > mini_limit:
            issues.append(
                Issue(
                    path,
                    "mini_card_overuse",
                    f".mini-card {mini_count}개 > 허용 {mini_limit}개. 카드 반복 틀로 보입니다.",
                )
            )
        if col_count > col_limit:
            issues.append(
                Issue(
                    path,
                    "col_list_overuse",
                    f".col-list {col_count}개 > 허용 {col_limit}개. 동일 리스트 틀이 과도합니다.",
                )
            )

    h3s = heading_texts(body, "h3")
    normalized: dict[str, int] = {}
    for h3 in h3s:
        key = re.sub(r"\s+", " ", h3).strip()
        normalized[key] = normalized.get(key, 0) + 1
    repeated = [(title, count) for title, count in normalized.items() if count >= 3]
    if repeated:
        title, count = sorted(repeated, key=lambda item: item[1], reverse=True)[0]
        issues.append(Issue(path, "repeated_heading", f"같은 h3 '{title}'가 {count}회 반복됩니다."))

    conclusion_tail = body[-2500:]
    if re.search(r"이\s*(문서|페이지|결과물)은\s*(예제|샘플)", conclusion_tail):
        issues.append(Issue(path, "example_conclusion", "마지막 결론이 실제 판단이 아니라 예제 설명입니다."))

    if 'class="try"' in body or "class='try'" in body or " try " in body:
        for card_class in TRY_CARD_CONTRAST_CLASSES:
            if card_class in body and f".try .{card_class} p" not in html:
                issues.append(
                    Issue(
                        path,
                        "try_card_contrast_guard_missing",
                        f".try 내부 .{card_class} 카드가 있지만 p/li 텍스트 색상 reset CSS가 없습니다.",
                    )
                )
                break

    issues.extend(raw_section_synthesis_issues(path, body))

    return issues


def iter_html_files(root: Path) -> list[Path]:
    if root.is_file():
        return [root]
    candidates: list[Path] = []
    for path in sorted(root.rglob("*.html")):
        rel_parts = set(path.relative_to(root).parts)
        if {"sources", "exports"} & rel_parts:
            continue
        candidates.append(path)
    files: list[Path] = []
    has_content_pages = any(path.name != "index.html" for path in candidates)
    for path in candidates:
        if path.name == "index.html":
            # In multi-page outputs index is a navigation shell. In single-page
            # outputs index.html is the content page and must be checked.
            if has_content_pages:
                continue
        files.append(path)
    return files


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check adaptive-html-final qualitative anti-regression contract.")
    parser.add_argument("target", help="HTML file or output/example directory")
    args = parser.parse_args(argv)

    root = Path(args.target).resolve()
    if not root.exists():
        print(f"FAILED: target not found: {root}", file=sys.stderr)
        return 2

    files = iter_html_files(root)
    issues: list[Issue] = []
    for path in files:
        issues.extend(check_html(path))

    if issues:
        print(f"FAILED: {len(issues)} quality contract issue(s)")
        for issue in issues:
            print(issue.format(root))
        return 1

    print(f"OK — quality contract guard passed ({len(files)} HTML content file(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
