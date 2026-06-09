# Export Contract

## Engine

Use Node Playwright Chromium. The HTML outputs may rely on CSS `:has()`, CSS-only radios, inline CSS, large SVG, print CSS, and no behavioral JavaScript. Non-Chromium converters can silently break themes or rendering fidelity.

## Output structure

```text
<output_dir>/exports/
  pdf/<slug>.pdf
  png/<slug>__<theme>.png
  webp/<slug>__<theme>.webp
  export-manifest.json
```

Root HTML files are named by basename. `pages/*.html` files use `pages__<basename>`.

## Manifest checks

A good export has:

```json
{
  "summary": { "failed": 0 },
  "html_sha256_unchanged": true,
  "sources_sha256_unchanged": true,
  "validate_issues_unchanged": true
}
```

`light,light2,white,dark,dark2,blue,skyblue,sepia` are requested by default. Any requested theme without a matching DOM radio is skipped and recorded, which is normal for older three-theme or five-theme outputs.

## Exit codes

| Situation | Exit |
|---|---:|
| Success | 0 |
| Required pdf/png failure, HTML mutation, validate drift | 1 |
| Usage error, unknown option, v2 option | 2 |
| Preconditions: missing dir, no HTML, Chromium unavailable | 3 |
| sharp unavailable without `--require-webp` | 0 with webp skipped |
| sharp unavailable with `--require-webp` | 1 |

## Safety

- Keep export artifacts ignored: `output/**/exports/`.
- Do not commit generated PDF/PNG/WebP files unless the user explicitly asks.
- The script should refuse output directories outside repo `output/` and refuse symlinked export directories for `--clean`.
