# Static operator guide design system

Use this with `templates/static-operator-guide-template.html` when producing showable manual-package HTML that should stay visually consistent across products, sessions, and agents.

This is a **generic operator-guide design system**. Do not copy product-specific ERPNext, Print Station, Onyx, Cursor, or Refero content into unrelated manuals. Copy the structure, tokens, and component behavior, then fill them with the target product's real workflows and evidence.

## Source style

The current visual standard is adapted from Refero Styles:

- Source URL: `https://styles.refero.design/style/4e3b4717-84c8-4599-baaf-a343c3d619b6`
- Referenced product: Cursor
- Theme phrase: **Warm ivory software studio**

Use the design language, not Cursor-specific product copy: warm ivory surfaces, compact studio density, precise typography, thin borders, layered card elevation, restrained orange outline accents, and contained screenshots/diagrams.

## Design goal

The page should feel like a precise, tactile software-studio manual:

- warm parchment/ivory page background
- compact, high-density but readable operator interface
- precise headings and small utility labels
- subtle card nesting with 4px radii and restrained borders
- workflow map/canvas on the left and selected-flow detail panel on the right
- beginner-facing system overview page/section before deep lessons
- flow-aware lesson/focus section below
- step-aligned focus carousel for screenshots/checks
- annotated review/evidence cards contained within card bounds
- common checks and source boundary section

A simple hero + cards + links layout is a fallback, not the default for showable operator guides.

## Required tokens

Keep these `--og-*` tokens unless the user explicitly requests a different brand skin. They map the Refero/Cursor style into the stable manual namespace so QA can still recognize the shell.

```css
:root{
  /* Refero/Cursor-derived colors */
  --og-bg:#f7f7f4;              /* Canvas Parchment */
  --og-paper:#f7f7f4;           /* primary card/page surface */
  --og-paper-elevated:#e6e5e0;  /* Pebble Gray */
  --og-paper-nested:#cdcdc9;    /* Highlight Beige */
  --og-ink:#262510;             /* Inkwell */
  --og-ink-strong:#141414;      /* Deep Shadow */
  --og-muted:#7a7974;           /* Muted Stone */
  --og-line:#cdcdc9;            /* low-weight separation */
  --og-brand:#f54e00;           /* Onyx Outline */
  --og-brand-2:#34785c;         /* Forest Green Action */
  --og-accent:#c08532;          /* Goldenrod Accent */
  --og-ok:#e6e5e0;
  --og-warn:#f7f0df;
  --og-danger:#f4e6df;
  --og-soft:#e6e5e0;

  /* Typography */
  --og-font:'CursorGothic',ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Noto Sans KR","Segoe UI",Roboto,sans-serif;
  --og-font-mono:'berkeleyMono',ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,"Liberation Mono",monospace;
  --og-font-utility:'Lato',ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Noto Sans KR","Segoe UI",Roboto,sans-serif;
  --og-text-caption:10px;
  --og-text-small:12px;
  --og-text-body:14px;
  --og-text-ui:13px;
  --og-text-heading-sm:22px;
  --og-text-heading:26px;
  --og-text-heading-lg:36px;
  --og-text-display:72px;

  /* Shape / spacing */
  --og-radius:4px;
  --og-radius-prominent:8px;
  --og-page-max:1300px;
  --og-section-gap:43px;
  --og-card-padding:12px;
  --og-gap:8px;
  --og-shadow:rgba(0,0,0,.14) 0 28px 70px 0,rgba(0,0,0,.10) 0 14px 32px 0,oklab(0.263084 -0.00230259 0.0124794 / .10) 0 0 0 1px;
  --og-shadow-subtle:oklab(0.263084 -0.00230259 0.0124794 / .10) 0 0 0 1px,rgba(0,0,0,.18) 0 18px 36px -18px;
}
```

### Token rules

- Use `--og-brand` / Onyx Outline as an **outline, link, badge, or connector accent**, not as a large filled background.
- Use `--og-paper-elevated` for major cards/panels; use `--og-paper-nested` only for nested chips, inset surfaces, or faint separators.
- Use Inkwell/Muted Stone for text and borders; avoid purely achromatic gray for primary text.
- Keep default card/button radius compact: 4px; reserve 8px for prominent containers or screenshot frames.
- Keep `--og-*` names even when adding source-style aliases. QA relies on the manual namespace.

## Typography rules

- Headings and primary UI use `--og-font`; Korean fallback must remain readable through system/Noto Sans KR.
- Utility labels, badges, and small controls may use `--og-font-utility`.
- Code/config/path values use `--og-font-mono` at 12–13px.
- Use precise, restrained letter spacing:
  - display/hero: negative tracking (`-.06em` to `-.03em`)
  - section headings: `-.02em` to `-.01em`
  - badges/eyebrows: positive tracking (`.08em` to `.14em`)
- Do not introduce new font families or random weights. Prefer 400, 500 for mono, and 600 only for utility emphasis.

## Fixed component names

Future agents should reuse these classes/regions so QA scripts and reviewers can recognize the manual shape:

| Region/class | Purpose |
| --- | --- |
| `.og-page` | full page wrapper |
| `.og-hero` | title, audience, scope/evidence badges |
| `.og-system-overview` | beginner-facing overview page/section or overview preview block |
| `.og-shell` | two-column workflow map + detail panel |
| `.og-map` | workflow/canvas area |
| `.og-flow-board` | positioned wrapper for workflow cards plus connector SVG |
| `.og-flow-connectors` | SVG path layer for visible flow-to-flow connections and numbered midpoint badges |
| `.og-flow-card` | selectable flow/job card |
| `.og-detail` | selected-flow detail panel |
| `.og-steps` | numbered operational path/check lists |
| `.og-lessons` | flow-aware lesson/focus section |
| `.og-focus-carousel` | one visible focus card at a time |
| `.og-focus-card` | step-aligned screenshot/check card |
| `.og-shot` | annotated screenshot or diagram container |
| `.og-diagram` | fallback concept/flowchart visual when no real screenshot is available |
| `.og-callout` | small screenshot/diagram annotation/callout |
| `.og-review-grid` | review/evidence cards |
| `.og-review-card` | annotated evidence/review card |
| `.og-hl` | inline highlighter underline emphasis for short phrases |
| `.og-common` | common checks, source links, boundaries |

Do not rename these classes casually. Add product-specific modifier classes only when needed.

## Component styling standard

### Page and hero

- `.og-page`: max width 1300px, warm parchment background, compact section spacing.
- `.og-hero`: split or wide content card, Pebble Gray/Canvas Parchment surface, 4–8px radius, layered shadow, thin Highlight Beige border.
- Hero actions should be outlined with Onyx Outline instead of filled orange.

### Workflow map and detail panel

- `.og-shell`: desktop two-column layout; map and detail stay visually paired. Stacked layouts are allowed below the defined breakpoint.
- `.og-map`, `.og-detail`, `.og-lessons`, `.og-common`: elevated studio panels with compact padding, thin border, and `--og-shadow-subtle` or `--og-shadow` depending on prominence.
- `.og-flow-card`: tactile card/button, compact padding, 4px radius, no huge pill cards. Active state should use orange outline/accent and/or subtle Pebble Gray fill, not a solid orange block.
- `.og-flow-connectors`: thin connector paths in muted orange/ink, numbered badges near connector midpoints. Do not replace connector badges with node chips unless the workflow truly needs node-level roles.

### Focus, screenshots, diagrams

- Screenshots and diagrams are contained in card-like structures with 4–8px radii, subtle border, and shadow only when it helps hierarchy.
- Product screenshots can be dark or colorful, but must sit inside bounded frames so they do not dominate the parchment page.
- `.og-diagram` should feel like a compact component map: small mono/utility labels, thin borders, clear arrows, no generic placeholder boxes.
- `.og-callout` should fit content and sit as a restrained annotation, not as a full-height overlay.

### Buttons, chips, badges

- Primary learner actions: transparent/ivory background, `--og-brand` border/text, 4px radius.
- Secondary actions: transparent or Pebble Gray background with Inkwell/Muted Stone text.
- Chips/badges: compact 10–12px utility text, thin border, parchment/pebble surface.
- Avoid large solid accent fills, especially solid Onyx Outline.

## Inline emphasis / highlighter underline

Use `references/highlight-emphasis-patterns.md` when a manual needs a human-readable inline emphasis style. The default class is `.og-hl`: a thin rounded highlighter underline that sits behind the lower 24% of the text, preserves rounded ends across line wraps, and can optionally reveal left-to-right with `.is-animated`.

Example:

```html
<p>저장 전에 <span class="og-hl og-hl--yellow">거래처와 금액</span>을 먼저 확인합니다.</p>
<p>운영 점검은 <span class="og-hl og-hl--blue">health endpoint</span>와 실제 화면을 분리해서 봅니다.</p>
```

Use it sparingly for concrete decisions/checks/values. Do not use it as decoration or as a replacement for screenshot callout boxes.

## Content adaptation rules

### Public repo / developer tool products

Replace ERP transaction evidence with operational evidence:

- install mode or compose profile
- `.env` variable category, not secret values
- auth mode
- provider/model connection state
- connector/sync status
- search result/citation evidence
- agent/action configuration
- CLI command and expected non-secret output
- health endpoint, backup, upgrade, rollback checks

### ERP/admin products

Use business evidence:

- document number/status
- party/customer/vendor/item
- quantity/amount only if visible in evidence
- approval/submission state
- downstream report or stock/accounting effect
- risk/permission boundary

## System overview page / section

For non-trivial manuals, include a beginner-facing system overview before detailed workflows. Use `references/system-overview-page-for-beginners.md`. This is the `html-for-beginners` teaching posture adapted to operator guides: explain what the system is, who uses it, the major parts, what data/work item flows through it, common beginner confusions, and the recommended reading path.

The overview should be linked from the hero or top navigation as `시스템 개요` and should include at least one `.og-diagram` / component map / lifecycle map / annotated screenshot. Keep the warm ivory `og-*` design system; do not copy the `html-for-beginners` article skin. The overview is not a status page, not a source map, and not an architecture dump.

## Workflow-map visual connection rule

The Workflow Map must show visible relationships between flows or stages. Do not render it as disconnected cards unless the manual is explicitly a simple feature index. The default template uses `.og-flow-board` + `.og-flow-connectors` to draw SVG connector paths between cards, with numbered badges near the connector midpoint. By default, connect flows in their listed order; when the real product has branches, add `next:["target-flow-id"]` to each `guideData` flow and draw those branches instead.

Connection QA requirements:

- at least one visible connector exists when there is more than one flow card;
- connector endpoints follow the same flow IDs used by tabs/detail/focus state;
- connector labels are not duplicated node chips — they represent movement/relationship between cards;
- narrow/stacked layouts may simplify the connector geometry, but must not make the flow feel like unrelated tiles.

## Focus-lesson visual evidence rule

Every Focus lesson card needs a visual teaching surface. Preferred order:

1. real screenshot or focused crop from the target UI/system;
2. generated diagram/flowchart/concept map derived from verified source evidence;
3. explicit capture-needed boundary only when the phase is capture-blocked.

Do **not** leave a plain empty placeholder or text-only focus card. If a real screenshot is impossible because the source is repo/docs/config, create a learner-facing diagram with `.og-diagram` nodes such as `Install mode → env boundary → health check`, `Connector → sync status → citation`, or `Provider → key boundary → connection test`. The diagram is not decoration; it must teach what the reader should distinguish or verify.

## Refero-derived do/don't rules

### Do

- Use warm ivory/parchment surfaces as the base, with Pebble Gray elevation and Highlight Beige nesting.
- Use compact spacing: 8px related gaps, ~12px card padding, ~43px major section rhythm.
- Use layered shadows for elevated content cards; avoid arbitrary shadow recipes.
- Reserve orange Onyx Outline for outlined actions, links, connector badges, or focus accents.
- Keep screenshots, diagrams, and UI imagery contained inside cards.
- Prefer precise small labels, monospace snippets, and clear hierarchy over large decorative blocks.

### Don't

- Do not turn the style into a generic blue SaaS dashboard skin.
- Do not use solid orange backgrounds for primary CTAs or large panels.
- Do not introduce random fonts, heavy border radii, or large pill-shaped components.
- Do not use achromatic black/gray as if the design were neutral grayscale; use Inkwell and Muted Stone.
- Do not let product screenshots become unbounded background imagery.
- Do not vary body letter spacing or over-style long Korean paragraphs.

## Visual QA checklist

- [ ] Page uses the generic operator-guide shell, not ad-hoc one-off CSS.
- [ ] The shell uses warm ivory Refero-derived `--og-*` tokens: `--og-bg:#f7f7f4`, Inkwell text, Muted Stone secondary text, Onyx Outline accent, 4px default radius, compact spacing.
- [ ] Orange accent is used as outline/link/connector emphasis, not as a large filled background.
- [ ] `.og-shell` has map + detail panel on desktop and stacks cleanly on narrow widths.
- [ ] Workflow Map has visible connectors/arrow-badge paths between flows when more than one flow exists; cards do not read as isolated tiles.
- [ ] Detail panel height matches map height on desktop when both columns are visible.
- [ ] Flow selection changes title, steps, checks, focus cards, and review copy consistently.
- [ ] Focus carousel cards have a real screenshot/crop or a meaningful diagram/flowchart/concept map; no text-only empty placeholders remain.
- [ ] Inline highlights, if used, follow `.og-hl` rules: short meaningful phrases, visible without hover, multi-line safe, and no unsupported status implication.
- [ ] Focus carousel shows one card at a time and hot-node/card controls select the matching slide where implemented.
- [ ] Review/evidence cards contain annotations when teaching recognition; plain crops are not used as teaching cards.
- [ ] Visible copy is learner-facing and product/domain-specific, not project-management/status language.
- [ ] `manual-verification` records technical QA separately from content/usefulness QA.
