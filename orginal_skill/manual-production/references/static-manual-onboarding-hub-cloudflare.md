# Static Manual Onboarding Hub on Cloudflare Pages

Use this when the owner wants every new manual to be shareable from Cloudflare, but not as unrelated one-off URLs. Build a small central `/onboarding/` hub that lets readers choose a manual, then place each bundled manual under `/onboarding/manuals/<manual-id>/`.

## When to use

- The owner says new manuals are separately uploaded to Cloudflare and asks for an onboarding path or selector.
- Several static manual packages exist across project/research directories and need one public entry point.
- An already deployed Pages manual should remain at its existing URL but be discoverable from the new hub.

## Recommended shape

```text
manual-onboarding-cloudflare/
  public/
    index.html                  # redirect or simple link to /onboarding/
    _headers
    _redirects
    onboarding/
      index.html                # manual selector / hub
      manuals/
        <manual-id>/
          index.html
          overview.html
          lessons/
          assets/
  MANIFEST.json
  HANDOFF.md
```

Hub URL:

```text
https://<pages-project>.pages.dev/onboarding/
```

Bundled manual URL:

```text
https://<pages-project>.pages.dev/onboarding/manuals/<manual-id>/
```

## Packaging rules

- Treat the hub as a deployment artifact, not as a source-of-truth rewrite of each manual.
- Copy only public-reader HTML/assets into `public/onboarding/manuals/<manual-id>/`.
- Include first-read companion pages deliberately. For each bundled manual, check for `beginner.html`, `overview.html`, `system-overview.html`, or equivalent learner-facing first-read pages in the source package; copy valid public pages, link them from the manual `index.html`, and record them in the hub/manual manifest. Do not let a companion page exist only in the source tree while the deployed manual selector exposes only the workflow map.
- Exclude internal work artifacts unless the owner explicitly wants them public:
  - `qa/`, `sources/`, `manual/`, `evidence/`, `.hermes/`
  - `STATUS.md`, `HANDOFF.md`
  - capture/render scripts and raw workflow evidence
- Existing Cloudflare Pages manuals can be represented as external cards instead of being copied into the hub. Label them clearly as existing deployments.
- Keep a local `MANIFEST.json` that records bundled manuals, external links, excluded internal paths, and included companion pages.
- Keep a local `HANDOFF.md` with Cloudflare account, Pages project, production URL, preview URL, and verification evidence.

## Flow-map layout hardening

For flow-first grouped-node manuals, the hub deploy check should include a representative Workflow Map layout smoke, not only link checks:

- Multi-column canvases must not be clipped by the card/wrapper. Use a scrollable wrapper such as `.canvas-wrap { overflow: auto; overscroll-behavior-x: contain; }` instead of `overflow: hidden`.
- If the number of columns is data-driven, expose it as a CSS custom property from render code, e.g. `--flow-col-count`, and use it in the grid/min-width calculation: `grid-template-columns: repeat(var(--flow-col-count, 6), minmax(...))` plus a bounded `min-width`.
- Verify at desktop and stacked widths that the selected-flow connectors, cards, and detail panel remain reachable. A page can return 200 and still fail because the rightmost columns or vertical content are hidden.
- When this fix is applied during deployment, update both the source manual package and the Cloudflare `public/onboarding/manuals/<manual-id>/` copy, then redeploy and rerun local/remote probes.

## Cloudflare workflow

Before creating or deploying, confirm the active account:

```bash
npx --yes wrangler@latest whoami
npx --yes wrangler@latest pages project list
```

If the hub project does not exist and a new hub URL is acceptable:

```bash
npx --yes wrangler@latest pages project create <hub-project-name> --production-branch main
npx --yes wrangler@latest pages deploy public --project-name <hub-project-name> --commit-dirty=true
```

Do not create replacement projects for existing production URLs unless the owner accepted a new URL. Project names are account-scoped.

## Verification checklist

Run fresh verification before claiming the hub is ready:

1. Local static smoke, ideally via `python3 -m http.server` from `public/`:
   - `/onboarding/` returns 200.
   - each bundled `/onboarding/manuals/<manual-id>/` returns 200.
   - each declared companion/first-read page such as `beginner.html` or `overview.html` returns 200 and is linked from the manual entry page.
2. Local link/ref probe:
   - scan public HTML `href`, `src`, and `poster` refs;
   - resolve relative paths against each HTML file;
   - ignore external links and JS template literals such as `${...}` only if they are known dynamic placeholders, not literal broken refs.
3. Local rendered-layout probe for newly added/modified manuals:
   - inspect representative Workflow Map pages for `overflow:auto`/reachable scroll when column count exceeds the viewport;
   - compare `scrollWidth`, `clientWidth`, and bounding boxes where useful;
   - ensure no horizontal or vertical clipping hides nodes, connectors, lesson links, or detail content.
4. Deploy to Cloudflare Pages.
5. Production HTTP smoke:
   - `/onboarding/` 200;
   - each bundled manual entry 200;
   - each newly added companion page 200.
6. Remote recursive asset/page probe with a browser-like User-Agent or range GET when HEAD is noisy.
7. Browser smoke:
   - open the hub;
   - open at least the newly added manuals and companion pages by direct URL;
   - check console errors and the representative Workflow Map layout on the deployed URL.

## Reporting

Report separately:

- hub production URL;
- Pages project and Wrangler account used;
- bundled manuals and external manual links;
- public package exclusions;
- HTTP/link/browser verification evidence;
- boundary: deploying the hub does not upgrade each manual's runtime/UI verification claims.
