# User-provided DESIGN.md retrofit for static manual packages

Use this when the user provides a `DESIGN.md` and asks to change an already-produced manual/package design to match it.

## Principle

Treat the provided `DESIGN.md` as the design contract and the existing manual content as the content contract. The task is a visual-system retrofit, not a rewrite.

Do not replace long learner-facing pages, beginner companion pages, lesson bodies, screenshots, or workflow structure with a shorter agent-authored summary just because the design is changing.

## Retrofit workflow

1. **Read the provided `DESIGN.md` and extract concrete tokens**
   - Background/canvas color
   - Surface/card color
   - Primary/accent/link colors
   - Typography family, weight, headline size/letter-spacing if specified
   - Radius, elevation/shadow, blur, spacing rhythm
   - Any explicit do/don't rules

2. **Map tokens to the existing package shell**
   - Prefer changing shared CSS (`assets/style.css`) and design variables first.
   - Keep HTML structure and semantic content stable unless the design contract requires a component-level change.
   - If a companion page such as `beginner.html` was user-provided, preserve its original explanatory structure and only add minimal package navigation/metadata or CSS hooks.

3. **Update package bookkeeping**
   - Record the design reference in `manifest`/package metadata where present.
   - Update `STATUS.md` and `HANDOFF.md` with: design source path, files changed, verification run, and remaining boundaries.
   - Add a QA note under `qa/` describing the token checks and browser smoke.

4. **Run deterministic checks**
   - Local link/reference check for every HTML page.
   - Syntax/checks for JS/JSON assets where applicable.
   - Browser smoke via `file://` on entry page and at least one changed companion/lesson page.
   - Console error check.

5. **Verify rendered token conformance**
   - Use browser-side computed styles for representative selectors, not only source inspection.
   - Check at minimum: `body` background, card/surface background, border radius, shadow/elevation, primary/link colors, headline size/weight/tracking, nav blur/backdrop when specified.
   - Count key preserved content elements on sensitive pages, e.g. beginner comic panels, glossary/term boxes, cards/sections, back-navigation.

## PASS wording

Report retrofit completion as:

- changed files
- design source path
- preserved content boundaries
- static/browser checks run
- exact computed-style evidence
- console/error status

Avoid saying the design is globally perfect unless visual QA was actually performed across representative pages and widths.

## Pitfalls

- **Design retrofit turning into content replacement.** If the user supplied a rich beginner/explainer page, do not summarize it into a thinner page while restyling.
- **Source-token-only verification.** CSS can contain the right token while another rule overrides it. Verify computed styles in the browser.
- **Index-only smoke.** If the package has companion pages or lessons with separate CSS structure, open at least one of them directly and through the package navigation.
- **Bookkeeping drift.** A design-source change should be reflected in manifest/status/handoff/QA so the next session knows which spec governed the current look.
