#!/usr/bin/env python3
"""Render 8000x6000 SVG infographics for adaptive-html-final visual briefs.

Usage:
  python scripts/render_visual_svg.py brief.json output.svg

The script intentionally uses only Python stdlib so the skill works offline.
"""
from __future__ import annotations

import json
import math
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = ROOT / "visual-templates"
DEFAULT_W = 8000
DEFAULT_H = 6000
ACCENTS = ["#e63946", "#3a6280", "#2a7d5a", "#d99a38"]

SVG_CSS = """
text { font-family: Pretendard, -apple-system, BlinkMacSystemFont, "Noto Sans KR", Arial, sans-serif; }
.small { font-size: 92px; fill: #7a7a7a; font-weight: 650; }
.hair { stroke:#d8d8d0; stroke-width:10; }
""".strip()


def e(value: object) -> str:
    return escape(str(value or ""), quote=True)


def char_units(ch: str) -> int:
    """Return display width units for a single character.

    CJK / full-width characters occupy 2 units, everything else 1 unit. This
    keeps Korean (Hangul), CJK ideographs and full-width punctuation from
    overflowing cards/canvas when laid out by character count.
    """
    cp = ord(ch)
    if (
        0x1100 <= cp <= 0x115F          # Hangul Jamo
        or 0x2E80 <= cp <= 0x303E       # CJK radicals, Kangxi, CJK symbols/punct
        or 0x3041 <= cp <= 0x33FF       # Hiragana, Katakana, CJK compat
        or 0x3400 <= cp <= 0x4DBF       # CJK Ext-A
        or 0x4E00 <= cp <= 0x9FFF       # CJK Unified Ideographs
        or 0xA000 <= cp <= 0xA4CF       # Yi
        or 0xAC00 <= cp <= 0xD7A3       # Hangul Syllables
        or 0xF900 <= cp <= 0xFAFF       # CJK Compatibility Ideographs
        or 0xFE30 <= cp <= 0xFE4F       # CJK Compatibility Forms
        or 0xFF00 <= cp <= 0xFF60       # Full-width forms
        or 0xFFE0 <= cp <= 0xFFE6       # Full-width signs
    ):
        return 2
    return 1


def str_units(value: str) -> int:
    """Total display width (in units) of a string."""
    return sum(char_units(ch) for ch in value)


def _wrap_by_units(raw: str, max_units: int) -> list[str]:
    """Greedy word-wrap a single line by display-width units.

    Prefers breaking on whitespace, but falls back to breaking mid-token when
    a single token (e.g. a long CJK run with no spaces) exceeds the budget.
    """
    if max_units < 1:
        max_units = 1
    out: list[str] = []
    cur = ""
    cur_units = 0
    # Tokenise keeping whitespace separators so spaces survive between words.
    tokens: list[str] = []
    buf = ""
    for ch in raw:
        if ch == " ":
            if buf:
                tokens.append(buf)
                buf = ""
            tokens.append(" ")
        else:
            buf += ch
    if buf:
        tokens.append(buf)

    def flush() -> None:
        nonlocal cur, cur_units
        if cur:
            out.append(cur)
        cur = ""
        cur_units = 0

    for tok in tokens:
        tu = str_units(tok)
        if tok == " ":
            # Drop a leading space at the start of a wrapped line.
            if cur_units == 0:
                continue
            if cur_units + 1 > max_units:
                flush()
                continue
            cur += " "
            cur_units += 1
            continue
        if tu <= max_units:
            if cur_units + tu > max_units:
                flush()
            cur += tok
            cur_units += tu
        else:
            # Token longer than the budget: hard-break it by units.
            for ch in tok:
                cu = char_units(ch)
                if cur_units + cu > max_units:
                    flush()
                cur += ch
                cur_units += cu
    flush()
    return out


def _truncate_units(value: str, max_units: int, ellipsis: str = "…") -> str:
    """Truncate a string to max_units display units, appending an ellipsis."""
    if str_units(value) <= max_units:
        return value
    ell_units = str_units(ellipsis)
    budget = max(0, max_units - ell_units)
    acc = ""
    used = 0
    for ch in value:
        cu = char_units(ch)
        if used + cu > budget:
            break
        acc += ch
        used += cu
    return acc + ellipsis


def wrapped(value: str, max_chars: int = 18, max_lines: int = 3) -> list[str]:
    """Width-aware word wrap.

    ``max_chars`` is interpreted as a display-width budget in units where CJK /
    full-width glyphs count as 2 and ASCII as 1, so Korean long-form text and
    ``lines`` arrays stay inside their cards/canvas.
    """
    if not value:
        return []
    lines: list[str] = []
    for raw in str(value).split("\n"):
        parts = _wrap_by_units(raw, max_chars) or [raw]
        lines.extend(parts)
    return lines[:max_lines]


def text_lines(lines: list[str], x: int, y: int, size: int = 120, fill: str = "#1a1a1a", weight: int = 700, leading: float = 1.24, anchor: str = "start") -> str:
    if not lines:
        return ""
    out = [f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}">']
    for i, line in enumerate(lines):
        dy = 0 if i == 0 else int(size * leading)
        out.append(f'<tspan x="{x}" dy="{dy}">{e(line)}</tspan>')
    out.append("</text>")
    return "\n".join(out)


def header(title: str, subtitle: str) -> str:
    return "\n".join([
        '<text x="560" y="620" font-size="122" fill="#e63946" font-weight="900" letter-spacing="22">ADAPTIVE HTML VISUAL</text>',
        text_lines(wrapped(title, 28, 2), 560, 980, 300, "#1a1a1a", 900, 1.08),
        text_lines(wrapped(subtitle, 48, 2), 570, 1280, 118, "#4a4a4a", 560, 1.28),
    ])


def footer(text: str | None) -> str:
    label = text or "8000×6000 SVG · scalable infographic"
    return f'<text x="7440" y="5600" font-size="84" text-anchor="end" fill="#7a7a7a" font-weight="700">{e(label)}</text>'


def card(x: int, y: int, w: int, h: int, title: str, lines: list[str], accent: str, tag: str | None = None, title_size: int = 135, body_size: int = 92) -> str:
    parts = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="96" fill="#ffffff" stroke="#d8d8d0" stroke-width="12"/>',
        f'<rect x="{x}" y="{y}" width="24" height="{h}" rx="12" fill="{accent}"/>',
    ]
    top = y + 165
    if tag:
        parts.append(f'<text x="{x+110}" y="{top}" font-size="78" fill="{accent}" font-weight="900" letter-spacing="6">{e(tag)}</text>')
        top += 165
    parts.append(text_lines(wrapped(title, 18, 2), x + 110, top, title_size, "#1a1a1a", 900, 1.12))
    parts.append(text_lines(lines[:4], x + 110, top + 210, body_size, "#4a4a4a", 560, 1.32))
    return "\n".join(parts)


def item_lines(item: dict, width: int = 28, max_lines: int = 3) -> list[str]:
    if item.get("lines"):
        # Apply the same width-aware wrapping to the explicit ``lines`` array so
        # long Korean / full-width entries never pass through unprocessed and
        # overflow the card. Each source line may wrap into several rendered
        # lines; the combined result is capped at ``max_lines``.
        out: list[str] = []
        for raw in item["lines"]:
            for wrapped_line in wrapped(str(raw), width, max_lines):
                out.append(_truncate_units(wrapped_line, width))
                if len(out) >= max_lines:
                    return out[:max_lines]
        return out[:max_lines]
    return wrapped(str(item.get("description", "")), width, max_lines)


def render_card_grid(items: list[dict]) -> str:
    body: list[str] = []
    cols, x0, y0, cw, ch, gapx, gapy = 4, 430, 1540, 1680, 650, 170, 190
    for i, item in enumerate(items[:16]):
        col, row = i % cols, i // cols
        x, y = x0 + col * (cw + gapx), y0 + row * (ch + gapy)
        w = cw
        accent = item.get("accent") or ACCENTS[i % len(ACCENTS)]
        body.append(f'<rect x="{x}" y="{y}" width="{w}" height="{ch}" rx="86" fill="#fff" stroke="#d8d8d0" stroke-width="12"/>')
        body.append(f'<circle cx="{x+150}" cy="{y+165}" r="72" fill="{accent}"/>')
        body.append(f'<text x="{x+150}" y="{y+190}" font-size="76" fill="#fff" text-anchor="middle" font-weight="900">{i+1}</text>')
        # label is a single unwrapped line — width-clip by units so a long (e.g. CJK) label cannot exceed the card width
        body.append(f'<text x="{x+270}" y="{y+154}" font-size="72" fill="#e63946" font-weight="900" letter-spacing="2">{e(_truncate_units(str(item.get("label") or item.get("title") or ""), 26))}</text>')
        body.append(text_lines(wrapped(str(item.get("title", "")), 15, 2), x + 270, y + 315, 98, "#1a1a1a", 900, 1.1))
        body.append(text_lines(item_lines(item, 20, 2), x + 270, y + 455, 70, "#4a4a4a", 560, 1.25))
    return "\n".join(body)


def render_hero_map(items: list[dict]) -> str:
    body: list[str] = []
    x_positions = [520, 3020, 5520]
    for i, item in enumerate((items + [{}, {}, {}])[:3]):
        body.append(card(x_positions[i], 1660, 1960, 1360, str(item.get("title", f"Step {i+1}")), item_lines(item, 24, 4), item.get("accent") or ACCENTS[i], str(item.get("label") or f"STEP {i+1}"), 150, 104))
    if len(items) > 3:
        summary = items[3]
        body.append(card(720, 3540, 6560, 1120, str(summary.get("title", "추천 결론")), item_lines(summary, 78, 3), summary.get("accent") or "#1a1a1a", None, 150, 104))
    return "\n".join(body)


def render_decision_tree(items: list[dict]) -> str:
    body: list[str] = []
    top = (items + [{}, {}])[:2]
    body.append(card(580, 1580, 2500, 900, str(top[0].get("title", "질문 1")), item_lines(top[0], 28, 3), top[0].get("accent") or "#e63946", str(top[0].get("label") or "Q1"), 130, 88))
    body.append(card(4920, 1580, 2500, 900, str(top[1].get("title", "질문 2")), item_lines(top[1], 28, 3), top[1].get("accent") or "#3a6280", str(top[1].get("label") or "Q2"), 130, 88))
    body.append('<path d="M3080 2030 C3700 2030 4300 2030 4920 2030" fill="none" stroke="#1a1a1a" stroke-width="18" stroke-linecap="round"/>')
    body.append('<polygon points="4900,2030 4720,1930 4720,2130" fill="#1a1a1a"/>')
    xs = [580, 2990, 5400]
    for j, item in enumerate((items[2:] + [{}, {}, {}])[:3]):
        body.append(card(xs[j], 3040, 2020, 1040, str(item.get("title", f"선택 {j+1}")), item_lines(item, 25, 3), item.get("accent") or ACCENTS[(j+2) % len(ACCENTS)], str(item.get("label") or "OPTION"), 130, 86))
    return "\n".join(body)


def render_quality_gate(items: list[dict]) -> str:
    """Render quality gates as a balanced 2x3 grid plus a substantial preflight panel.

    Avoid skinny bottom banners: they become unreadable and visually broken when
    scaled down in mobile article layouts.
    """
    body: list[str] = []
    x0, y0, cw, ch, gapx, gapy = 560, 1580, 3340, 700, 300, 190
    gate_items = (items or [])[:6]
    for i, item in enumerate(gate_items):
        col, row = i % 2, i // 2
        x, y = x0 + col * (cw + gapx), y0 + row * (ch + gapy)
        title = str(item.get("title", f"Gate {i+1}"))
        desc = str(item.get("description") or " ".join(item_lines(item, 44, 2)))
        accent = item.get("accent") or ["#2a7d5a", "#3a6280", "#d99a38", "#e63946", "#1a1a1a", "#2a7d5a"][i % 6]
        body.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="104" fill="#ffffff" stroke="#d8d8d0" stroke-width="12"/>')
        body.append(f'<rect x="{x}" y="{y}" width="30" height="{ch}" rx="15" fill="{accent}"/>')
        body.append(f'<circle cx="{x+210}" cy="{y+190}" r="92" fill="{accent}"/>')
        body.append(f'<path d="M{x+160} {y+190} L{x+198} {y+232} L{x+285} {y+136}" fill="none" stroke="#fff" stroke-width="32" stroke-linecap="round" stroke-linejoin="round"/>')
        body.append(text_lines(wrapped(title, 18, 1), x + 360, y + 185, 126, "#1a1a1a", 950))
        body.append(text_lines(wrapped(desc, 34, 2), x + 360, y + 330, 82, "#4a4a4a", 620, 1.22))
        body.append(text_lines(["검수 후 삽입 · 모바일 확인 · 출처 기록"], x + 360, y + 500, 66, "#7a7a7a", 650))

    preflight = items[6] if len(items) > 6 else {}
    pre_title = str(preflight.get("title") or "삽입 전 필수 검수")
    pre_desc = str(preflight.get("description") or "예쁜 이미지보다 오해 없이 바로 이해되는 이미지가 우선입니다.")
    y = 4300
    body.append('<rect x="560" y="4300" width="6880" height="760" rx="128" fill="#ffd400" stroke="#1a1a1a" stroke-width="18"/>')
    body.append('<rect x="560" y="4300" width="38" height="760" rx="19" fill="#e63946"/>')
    body.append('<circle cx="6950" cy="4560" r="190" fill="#fff4a3" opacity="0.8"/>')
    body.append(text_lines(wrapped(pre_title, 24, 1), 780, y + 255, 170, "#1a1a1a", 950))
    body.append(text_lines(wrapped(pre_desc, 54, 1), 780, y + 455, 96, "#1a1a1a", 720))
    body.append(text_lines(["8000×6000 · alt · figcaption · source · mobile 390px · no overflow"], 780, y + 625, 78, "#5a3a00", 700))
    body.append('<text x="7200" y="4990" font-size="82" text-anchor="end" fill="#1a1a1a" font-weight="900">PRE-FLIGHT</text>')
    return "\n".join(body)


def render_timeline(items: list[dict]) -> str:
    body: list[str] = ['<line x1="1100" y1="1600" x2="1100" y2="5000" stroke="#e63946" stroke-width="26" stroke-linecap="round"/>']
    y0, gap = 1660, 680
    for i, item in enumerate(items[:6]):
        y = y0 + i * gap
        accent = item.get("accent") or ACCENTS[i % len(ACCENTS)]
        body.append(f'<circle cx="1100" cy="{y}" r="105" fill="{accent}"/>')
        body.append(f'<text x="1100" y="{y+34}" font-size="92" fill="#fff" text-anchor="middle" font-weight="900">{i+1}</text>')
        body.append(card(1420, y - 210, 5700, 420, str(item.get("title", f"Step {i+1}")), item_lines(item, 72, 2), accent, str(item.get("label") or ""), 110, 80))
    return "\n".join(body)


def render_matrix(items: list[dict]) -> str:
    body: list[str] = []
    cols = max(2, min(4, math.ceil(math.sqrt(len(items) or 1))))
    x0, y0, cw, ch, gapx, gapy = 560, 1580, 1640, 760, 170, 180
    for i, item in enumerate(items[:12]):
        col, row = i % cols, i // cols
        x, y = x0 + col * (cw + gapx), y0 + row * (ch + gapy)
        body.append(card(x, y, cw, ch, str(item.get("title", f"항목 {i+1}")), item_lines(item, 20, 3), item.get("accent") or ACCENTS[i % len(ACCENTS)], str(item.get("label") or item.get("score") or ""), 108, 76))
    return "\n".join(body)


def render_checklist_flow(items: list[dict]) -> str:
    body: list[str] = []
    x0, y0 = 760, 1560
    for i, item in enumerate(items[:8]):
        y = y0 + i * 430
        body.append(f'<rect x="{x0}" y="{y}" width="6480" height="300" rx="80" fill="#fff" stroke="#d8d8d0" stroke-width="12"/>')
        body.append(f'<circle cx="{x0+180}" cy="{y+150}" r="70" fill="{item.get("accent") or "#2a7d5a"}"/>')
        body.append(f'<text x="{x0+180}" y="{y+176}" font-size="70" fill="#fff" text-anchor="middle" font-weight="900">✓</text>')
        body.append(text_lines([str(item.get("title", f"Check {i+1}"))], x0 + 330, y + 124, 102, "#1a1a1a", 900))
        body.append(text_lines(wrapped(str(item.get("description") or " ".join(item_lines(item))), 72, 1), x0 + 330, y + 235, 72, "#4a4a4a", 560))
    return "\n".join(body)


RENDERERS = {
    "hero-map": render_hero_map,
    "card-grid": render_card_grid,
    "decision-tree": render_decision_tree,
    "quality-gate": render_quality_gate,
    "timeline": render_timeline,
    "matrix": render_matrix,
    "checklist-flow": render_checklist_flow,
}


# Length constraints mirrored from schemas/visual-brief.schema.json so the
# renderer enforces them defensively even when callers skip validation (M4).
MAX_TITLE = 80
MAX_SUBTITLE = 160
MAX_FOOTER = 160
MAX_ITEM_TITLE = 60
MAX_ITEM_LABEL = 40
MAX_ITEM_DESC = 180
MAX_ITEM_LINE = 80


def _clip(value: object, max_len: int) -> str:
    """Truncate to the schema maxLength (character count) with an ellipsis."""
    s = str(value or "")
    if len(s) <= max_len:
        return s
    return s[: max(0, max_len - 1)] + "…"


def _sanitize_item(item: dict) -> dict:
    """Return a copy of an item with text fields clipped to schema maxLengths."""
    out = dict(item)
    if "title" in out:
        out["title"] = _clip(out.get("title"), MAX_ITEM_TITLE)
    if "label" in out:
        out["label"] = _clip(out.get("label"), MAX_ITEM_LABEL)
    if "description" in out:
        out["description"] = _clip(out.get("description"), MAX_ITEM_DESC)
    if out.get("lines"):
        out["lines"] = [_clip(v, MAX_ITEM_LINE) for v in out["lines"]]
    return out


def render(brief: dict) -> str:
    typ = brief.get("type")
    if typ not in RENDERERS:
        valid = ", ".join(sorted(RENDERERS))
        raise ValueError(
            f"unknown visual type {typ!r}; expected one of: {valid}"
        )
    width = int(brief.get("width", DEFAULT_W))
    height = int(brief.get("height", DEFAULT_H))
    if width < 8000 or height < 6000:
        raise ValueError("visual SVG must be at least 8000x6000")
    template_path = TEMPLATE_DIR / f"{typ}.svg.tpl"
    if not template_path.exists():
        raise FileNotFoundError(template_path)
    items = [_sanitize_item(it) for it in (brief.get("items") or [])]
    title = _clip(brief.get("title", ""), MAX_TITLE)
    subtitle = _clip(brief.get("subtitle", ""), MAX_SUBTITLE)
    footer_text = _clip(brief["footer"], MAX_FOOTER) if brief.get("footer") else None
    item_svg = RENDERERS[typ](items)
    replacements = {
        "{{WIDTH}}": str(width),
        "{{HEIGHT}}": str(height),
        "{{TITLE}}": e(title),
        "{{SUBTITLE}}": e(subtitle),
        "{{SVG_CSS}}": SVG_CSS,
        "{{HEADER}}": header(title, subtitle),
        "{{ITEMS}}": item_svg,
        "{{FOOTER}}": footer(footer_text),
    }
    svg = template_path.read_text(encoding="utf-8")
    for key, value in replacements.items():
        svg = svg.replace(key, value)
    return svg


def main(argv: list[str]) -> int:
    if len(argv) not in (2, 3):
        print("Usage: render_visual_svg.py brief.json [output.svg]", file=sys.stderr)
        return 2
    brief_path = Path(argv[1])
    try:
        brief = json.loads(brief_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"error: brief file not found: {brief_path}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"error: invalid JSON in {brief_path}: {exc}", file=sys.stderr)
        return 2
    try:
        svg = render(brief)
    except (ValueError, KeyError, FileNotFoundError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    out = Path(argv[2]) if len(argv) == 3 else Path(brief.get("output", brief_path.with_suffix(".svg")))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(svg, encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
