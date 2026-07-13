# Manual Package Handoff

Status: provisional pre-capture package

## What exists

- Manifest: `manifest.yml`
- Lessons: `<lesson range>`
- Preview: `preview-static/index.html`
- Evidence map: `sources/evidence-map.md`
- Capture unblock checklist: `sources/capture-next-checklist.md`
- QA docs: `qa/`

## How to run stable checks

```bash
python3 <skill>/scripts/validate-manual-package.py manifest.yml
python3 <skill>/scripts/manifest_lint.py manifest.yml
python3 <skill>/scripts/glossary_coverage.py glossary.md tracks/**/*.md
python3 <skill>/scripts/verify-preview-package.py preview-static V1-00 V1-18
```

Expected current result:

```text
PASS manual package validation (...)
PASS manifest lint
PASS glossary coverage
PASS preview package verification
```

## How to open preview

```bash
open preview-static/index.html
# or
python3 -m http.server 8080
# then open http://localhost:8080/preview-static/
```

## What not to claim

- Do not claim final manual completion.
- Do not claim live UI truth until target-version UI capture is complete.
- Do not claim screenshots/videos/media exist unless generated and reviewed.
- Do not claim risky workflows are executable without safe fixtures.
- Do not provide accounting/tax/legal/professional advice.

## Next unblock steps

See `sources/capture-next-checklist.md`.

Do not start a stack or capture media until runtime/app readiness, target version/source, safe fixture policy, and stop/report boundaries are recorded.
