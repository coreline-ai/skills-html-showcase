# adaptive-html-final Full Skill Analysis

Generated: 2026-06-05 13:52:05 KST
Scope: `skills/adaptive-html-final`, `AGENTS.md`, validator/tests, and `output/adaptive-html-final-13-topics-20260605_083433`

## Verdict

Current showcase output passes the existing validator, but the skill is not yet regression-safe.

The largest gap is not content quality. It is canonicalization: several fixes exist only in generated output or stale snapshots, while the source skill assets and validator do not fully enforce them.

## Specialist Agent Coverage

- Instruction/routing audit: `AGENTS.md`, `SKILL.md`, manifest, mode/layout/writing references.
- Frontend/assets audit: theme CSS, widget CSS/templates, visual HTML templates.
- Validation/governance audit: `validate_output.py`, tests, baseline docs, source snapshots.
- Output/regression audit: generated showcase, visual audit artifacts, route and inline style patterns.

## High Findings

### H1. Version Contract Drift

Evidence:

- `AGENTS.md` still states current version `4.4.0 -> 4.5.0`: `AGENTS.md:17`.
- `AGENTS.md` says output source manifest must match `4.5.0`: `AGENTS.md:112`, `AGENTS.md:128`.
- Current skill declares `5.2.0`: `skills/adaptive-html-final/SKILL.md:27`, `skills/adaptive-html-final/manifest.json:3`.

Risk:

- `AGENTS.md` has higher priority than `SKILL.md`, so agents can deterministically produce stale 4.5.0 metadata and fail current validation.

Recommended patch:

- Update `AGENTS.md` to `5.2.0`.
- Better: avoid hardcoded version text in procedural rules and say source manifest must match `skills/adaptive-html-final/manifest.json`.

### H2. v5.2 Theme System Missing From Deterministic Procedure

Evidence:

- `base.html` includes `{{THEME_DARK_CSS}}`: `skills/adaptive-html-final/assets/base.html:26`.
- `manifest.json` defines `theme_system`, `theme-dark.css`, and `ahf-theme` switcher: `manifest.json:24-36`.
- `AGENTS.md` CSS order and slot index omit `theme-dark.css` / `{{THEME_DARK_CSS}}`: `AGENTS.md:77-89`, `AGENTS.md:198-200`.
- `SKILL.md` Step 5 CSS sequence omits `theme-dark.css`: `SKILL.md:365`.

Risk:

- New outputs can leave the `{{THEME_DARK_CSS}}` slot unresolved or omit the 3-theme system while still following the top-level router.

Recommended patch:

- Add `theme-dark.css` after `print.css`, excluded from core hash, using `{{THEME_DARK_CSS}}`.
- Add explicit body insertion rule for the theme switcher when the user asks for selectable light/white/dark themes.

### H3. Conditional Asset and Source Snapshot Drift Pass Validation

Evidence:

- Current skill `theme-dark.css` is v5.2 `#ahf-light/#ahf-white/#ahf-dark`: `skills/adaptive-html-final/assets/theme-dark.css:1-29`.
- Output snapshot uses stale `#theme-toggle`: `output/.../sources/assets/theme-dark.css:1`, `:37`.
- Output source manifest has `version: 5.2.0`, but still contains stale `dark_theme` instead of current `theme_system`: `output/.../sources/adaptive-html-final-manifest.json:24`.
- `validate_output.py` compares source manifest version only: `scripts/validate_output.py:607-610`.
- CSS integrity checks core 5 assets only and does not enforce all conditional snapshots: `scripts/validate_output.py:384`, `:626`.

Risk:

- A generated package can claim `5.2.0` while embedding old theme behavior and still validate `OK`.

Recommended patch:

- Compare source manifest as canonical JSON or hash, not version string only.
- Validate every listed `sources/assets/*.css` hash against current skill assets, including `widgets.css`, `visual-html.css`, `theme-dark.css`, body/editorial/shape/workflow CSS.
- Add a legacy guard: in v5.2 outputs, `#theme-toggle` should fail unless explicitly marked legacy.

### H4. `wg-01` Overflow Fix Is Output-Only

Evidence:

- Page 10 was fixed with inline styles: `output/.../pages/10-vector-db-pgvector-search-engine-comparison.html:1689-1697`.
- Canonical `widgets.css` still uses `.wg-01-grid{grid-template-columns:repeat(3,1fr)}` and `.wg-01-code{white-space:pre}`: `skills/adaptive-html-final/assets/widgets.css:9`, `:19`.
- Canonical template repeats the same CSS: `assets/widget-templates/01-three-code-approaches.html:9`, `:19`.

Risk:

- Any new `comparison_html` output using `wg-01` can reintroduce mobile/desktop horizontal overflow.

Recommended patch:

```css
.wg-01-grid{grid-template-columns:repeat(3,minmax(0,1fr))}
.wg-01-card,.wg-01-card-head>div{min-width:0}
.wg-01-code{max-width:100%;box-sizing:border-box;white-space:pre-wrap;overflow-wrap:anywhere;word-break:break-word}
.wg-01-code code{white-space:inherit}
```

Apply to both `widgets.css` and `assets/widget-templates/01-three-code-approaches.html`.

### H5. Behavioral Script Gate Is Not Truly Global

Evidence:

- `MiniHTML` records external scripts only when `src` starts with `http`: `validate_output.py:43`.
- Global failure uses that external list: `validate_output.py:410`.
- Inline/local/type-less script blocking mostly lives inside widget/vt gates: `validate_output.py:131`, `:174`.

Risk:

- A page without `wg-`/`vt-` markup can include non-JSON-LD inline or local scripts and pass global validation.

Recommended patch:

- Globally scan all `<script>` tags and fail unless `type="application/ld+json"`.
- Globally fail `draggable=` and `contenteditable=`.
- Add negative fixtures to `tests/test_governance_gates.py` or a new stdlib validator test.

## Medium Findings

### M1. Theme Switcher Contract Is Ambiguous

Evidence:

- CSS and slot exist, but markup is documented as optional: `references/editorial-design-system.md:144-150`.
- User expected a visible light/dark selection button.

Risk:

- Outputs may include theme CSS without visible controls, or use legacy controls.

Recommended patch:

- Add `{{THEME_SWITCHER}}` slot or deterministic body insertion rule.
- Define default: no switcher = light fixed; switcher requested = 3-segment `ahf-themebar`.

### M2. Light/White Active Theme Control Contrast Is Below AA for Small Text

Evidence:

- `--accent:#e63946`, `--on-accent:#ffffff`: `theme.css:8`, `theme.css:37`.
- `.ahf-themebar input:checked + label` uses accent/on-accent at 12px: `theme-dark.css:25-27`.

Risk:

- Active theme segment can fail 4.5:1 contrast for small text.

Recommended patch:

- Darken light accent to at least `#d92f3d`, or introduce an AA-safe `--accent-fill` for small pills/buttons.

### M3. Visual/Profile Naming Drift

Evidence:

- `style=v6 -> diagram`: `AGENTS.md:70`.
- Same doc says `auto = current v6 output`: `AGENTS.md:107`.

Risk:

- Agents can confuse `diagram` with `auto`, causing different CSS bundles and different template/widget insertion.

Recommended patch:

- Define: `v5=widget`, `v6=diagram`, `auto=mixed/default`.
- Remove "auto = v6" language.

### M4. Reference Defaults Can Contradict Canonical vt Table

Evidence:

- Canonical table: `beginner_html -> concept-explainer`, `expert_html -> risk-matrix`: `SKILL.md:64-78`.
- Layout reference still has older "Visual Template Defaults": `references/layout-system.md:37`.

Risk:

- If an agent loads only the layout reference after initial routing, it may choose wrong vt templates.

Recommended patch:

- Rename that section to `SVG Infographic Defaults (hero/appendix only)`.
- Add: "본문 vt selection is only SKILL.md §0.6."

### M5. Editorial Pattern Count Drift

Evidence:

- `AGENTS.md` says 6 patterns: `AGENTS.md:85`, `AGENTS.md:186`.
- `SKILL.md` mentions `01..07`: `SKILL.md:148`.
- `manifest.json` says count 8 including `accessibility-checklist`: `manifest.json:47`.

Risk:

- Accessibility checklist pattern may be omitted in future generated outputs.

Recommended patch:

- Update AGENTS/SKILL to 8 patterns and include `accessibility-checklist`.

### M6. Table and vt Mobile Risks Remain

Evidence:

- `wg-12`, `wg-15`, `wg-16` table sections are not wrapped in a canonical `wg-table-scroll` pattern: `widgets.css:464`, `:589`, `:667`.
- `visual-html.css` risk matrix `.rm-grid` lacks mobile collapse/scroll: `visual-html.css:7`, media bundle around `:25`.

Risk:

- New pages can pass static validation but produce horizontal overflow or clipped table text.

Recommended patch:

- Add widget table scroll utility and update relevant templates.
- Add mobile-safe `.rm-grid` rules.

### M7. Screenshot/Overflow Tooling Is Not Canonical

Evidence:

- Output-local capture script assumes `BASE_URL=http://127.0.0.1:8765` and `/pages/$page`: `_work/capture_visual_audit.sh:4`.
- 8765 was previously serving the wrong root, producing 404 screenshots until 8766 was used.

Risk:

- Visual audit can silently inspect the wrong page/root unless route sentinel checks run first.

Recommended patch:

- Add run manifest with `base_url`, server root, checked routes, expected titles.
- Before capture, assert HTTP 200 and expected `h1`.
- Overflow detector should use page-level `documentElement.scrollWidth` as severity and allowlist internal scroll containers.

## Positive Findings

- `vt-21` dark contrast is canonicalized in source via `.wf-board` local token override: `theme-dark.css:20`.
- `validate_output.py` has useful gates for soft workflow accessibility, shape/workflow SVG, bespoke class prefixes, table wrappers, wide layout prose caps, and CSS governance.
- Current showcase output validates: `HTML files: 14 / OK`.
- Current stdlib governance test passes: `16/16 checks passed`.
- Final screenshot set for pages 6-13 contains 32 images, with desktop width 1440 and mobile width 390.

## Recommended Patch Order

1. Update `AGENTS.md` to current 5.2.0 and add `theme-dark.css` / `{{THEME_DARK_CSS}}` to the deterministic procedure.
2. Canonicalize `wg-01` overflow fix in `widgets.css` and `01-three-code-approaches.html`.
3. Strengthen validator for full conditional asset snapshots, full manifest content, global script/forbidden primitive scan, and legacy `#theme-toggle`.
4. Regenerate the 13-topic output from current 5.2.0 skill assets instead of manually version-bumping stale snapshots.
5. Add visual smoke automation: 390/760/1440 widths, light/white/dark states, page-level scrollWidth, and expected route/title checks.
6. Clean reference drift: profile wording, layout visual defaults, editorial pattern count, baseline docs.

## Completion Checks Run

```bash
python3 skills/adaptive-html-final/scripts/validate_output.py output/adaptive-html-final-13-topics-20260605_083433 --skill-dir skills/adaptive-html-final --json
# ok: true

python3 skills/adaptive-html-final/tests/test_governance_gates.py
# 16/16 checks passed
```

