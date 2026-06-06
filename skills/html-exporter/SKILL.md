---
name: html-exporter
description: |
  Use when the user wants to export completed local HTML output directories to PDF, PNG, or WebP using Chromium/Playwright.
  Especially use for adaptive-html-final outputs with CSS-only ahf-theme radios, :has() selectors, inline CSS, large SVG, no-JS constraints,
  theme-by-theme screenshots, export manifests, HTML SHA stability checks, and browser-openable PDF/PNG/WebP links.
  Trigger examples: "HTML PDF로 변환", "PDF/PNG/WebP export", "테마별 스크린샷", "PDF 링크 제공", "output 폴더 변환".
---

# HTML Exporter

Build-time helper for exporting finished HTML output directories to PDF, PNG, and WebP without modifying the source HTML.

## Core contract

- Use Chromium/Playwright for rendering. Do **not** use WeasyPrint/wkhtmltopdf for `:has()` theme outputs.
- Treat source HTML as read-only. Do not inject JS or write generated `.html` outside `exports/`.
- Write artifacts only under `<output_dir>/exports/{pdf,png,webp}/` plus `<output_dir>/exports/export-manifest.json`.
- Request themes `light,light2,white,dark,dark2` by default; capture only DOM radios that exist: `input[name="ahf-theme"]#ahf-<theme>`.
- Hide export controls at render time only: `.ahf-themebar`, `.reading-progress`, `.skip`, `.ahf-color-audit`.
- Confirm regression safety from manifest: `html_sha256_unchanged`, `sources_sha256_unchanged`, `validate_issues_unchanged`.

## Quick workflow

1. Identify the output directory, usually `output/<name>`.
2. If the project already has `scripts/export_output.mjs`, use it. Otherwise copy this skill's `scripts/export_output.mjs` into the project `scripts/` directory.
3. Ensure `package.json` contains:
   - script: `"export:output": "node scripts/export_output.mjs"`
   - dependency: `"playwright"`
   - optionalDependency: `"sharp"`
   - no root `"type":"module"` required.
4. Run install if needed:

```bash
npm install
```

5. Export:

```bash
npm run export:output -- output/<dir> --clean
```

6. Report:
   - command used and exit code
   - manifest path
   - PDF/PNG/WebP counts
   - skipped themes and why
   - HTML/source/validate unchanged booleans
   - localhost links for useful PDFs/PNGs when a local server is expected.

## Common commands

```bash
# Default: pdf,png,webp + light,light2,white,dark,dark2
npm run export:output -- output/final_20260604 --clean

# PDF only
npm run export:output -- output/final_20260604 --formats pdf --clean

# Dark PNG only, lower scale
npm run export:output -- output/final_20260604 --formats png --themes dark --scale 1 --clean
```

## Allowed v1 options

- `--formats pdf,png,webp`
- `--themes light,light2,white,dark,dark2`
- `--scale 1|2|3`
- `--viewport 1280x900`
- `--require-webp`
- `--clean`

Reject v2-only options if passed: `--concurrency`, `--pdf-media`, `--pdf-themes`, `--show-controls`, `--offline`, `--strict-fonts`, `--webp-mode`, `--pdf-format`, `--pdf-margin`, `--webp-quality`, `--webp-max-edge`.

## Links

If a server is running from repo root on port 8080, provide links like:

```text
http://localhost:8080/output/<dir>/exports/pdf/index.pdf
http://localhost:8080/output/<dir>/exports/png/index__dark.png
```

If no server is running, suggest:

```bash
python3 -m http.server 8080
```

## Reference

For implementation-level details and manifest fields, read `references/export-contract.md` only when needed.
