# Focused Showable Slice Expansion

Use this when a first live-UI tutorial slice exists but the screenshots are full-page and too small to teach the next operator task clearly.

## When to apply

- The owner wants a showable tutorial artifact, not a Markdown-heavy planning package.
- A first HTML/screenshots/video slice already exists.
- Visual QA says full-page screenshots load but labels are small or low-contrast.
- The next safe slice can be navigation/read-only rather than a destructive business transaction.

## Default second slice pattern

Prefer a navigation expansion before risky workflows:

1. Keep the first `showable-artifacts/index.html` as the entry page.
2. Add a second page such as `showable-artifacts/navigation.html` and link to it from the index.
3. Capture focused crops, not only full-page screenshots:
   - sidebar/module list;
   - Home/workspace card area;
   - global search or command palette result;
   - read-only module workspaces such as Stock, Buying, CRM.
4. Record a short video clip for screen movement only, e.g. Home → Stock → Buying → CRM → Home.
5. Keep the second slice read-only: no create, submit, cancel, payment, posting, stock mutation, delete, or fixture-changing action.
6. Update `STATUS.md`, `HANDOFF.md`, and the live capture log so they name the second page and media paths.

## Verification checklist

Run a deterministic reference check before closeout:

```bash
python - <<'PY'
from pathlib import Path
from html.parser import HTMLParser
class P(HTMLParser):
    def __init__(self): super().__init__(); self.refs=[]
    def handle_starttag(self, tag, attrs):
        d=dict(attrs)
        if tag in ('img','source','video'):
            for k in ('src','poster'):
                if k in d: self.refs.append(d[k])
missing=[]; empty=[]
for html_name in ['showable-artifacts/index.html','showable-artifacts/navigation.html']:
    html=Path(html_name)
    assert html.exists() and html.stat().st_size > 0
    p=P(); p.feed(html.read_text(encoding='utf-8'))
    for r in p.refs:
        fp=html.parent/r
        if not fp.exists(): missing.append((html_name,r))
        elif fp.stat().st_size == 0: empty.append((html_name,r))
print('missing_refs', missing or 'none')
print('empty_refs', empty or 'none')
print('index_links_navigation', 'navigation.html' in Path('showable-artifacts/index.html').read_text(encoding='utf-8'))
PY
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 showable-artifacts/video/<clip>.mp4
curl -I --max-time 10 http://localhost:8080 | head -n 1
```

Then open the HTML in a browser and visually check:

- header and safety notice render;
- video player is visible;
- focused crops are readable;
- captions are present;
- no missing-image icons or layout collapse;
- any broad workspace screenshots with tiny text are called out as caveats, not ignored.

## Copy and safety notes

- User-facing tutorial pages should explain what the operator sees, not the production process.
- Safety notices should be user-relevant and concrete: “menu navigation/read-only only; no Submit/Cancel/payment/stock mutation performed.”
- Keep process terms such as `slice`, `artifact`, `Playwright`, `ffmpeg`, `peer`, `blocked`, and `not final` in status/handoff files, not visible tutorial copy.
- Do not convert Accounting/Selling/Stock workspace screenshots into accounting, tax, legal, payroll, or inventory-control advice.
