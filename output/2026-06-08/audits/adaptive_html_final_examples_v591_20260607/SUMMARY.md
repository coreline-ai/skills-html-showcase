# adaptive-html-final examples v5.9.1 update audit

## Scope

- Target: `skills/adaptive-html-final/examples/index.html` and 16 mode example pages.
- Skill source: `skills/adaptive-html-final`.
- Profile: `auto`.
- Version aligned: `5.9.1`.

## Applied changes

1. `manifest.json` version and examples metadata aligned to `5.9.1`.
2. `AGENTS.md` stale version references aligned to `5.9.1`.
3. Latest skill assets re-inlined into all 17 example HTML files as a single verbatim CSS block.
4. `examples/sources` refreshed:
   - `profile.json`
   - `adaptive-html-final-manifest.json`
   - `css-integrity.json`
   - `sources/assets/*.css`
5. v5.9.1 width contract verified:
   - `.mode-template-contract .wg-10-sheet{width:100%;max-width:100%}` is present and applied.
   - 01 desktop wg-10 width: 974px / parent 1020px / ratio 0.955.
6. Additional layout regression found during capture audit and fixed:
   - `section.lead` direct article sections inherited prose `.lead{max-width:820px}`.
   - Added direct-section wrapper reset in `assets/layouts.css` so article cards fill the standard content width without changing text `.lead` utility semantics.

## Validation

```bash
python3 skills/adaptive-html-final/scripts/validate_output.py skills/adaptive-html-final/examples --skill-dir skills/adaptive-html-final
# HTML files: 17
# OK

python3 skills/adaptive-html-final/scripts/quality_contract_check.py skills/adaptive-html-final/examples
# OK — quality contract guard passed (16 HTML content file(s))

python3 skills/adaptive-html-final/scripts/completion_check.py skills/adaptive-html-final/examples
# 완료 통합 검증: 3/3 통과 -> OK
```

## Browser capture audit

- 16 modes × 2 viewports = 32 screenshots.
- Viewports: 1280px desktop, 390px mobile.
- Result: 32 PASS / 0 FAIL.
- Checks: horizontal overflow, direct section width, h2 body-icon presence, v5.9.1 wg-10 full-width contract.
