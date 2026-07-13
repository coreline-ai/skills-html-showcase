# Static Manual Deployment to Free Hosting

Use this when a showable manual is ready to be shared from a free external static host such as Cloudflare Pages, GitHub Pages, Netlify, or Vercel.

## Default recommendation

For static HTML manuals with local screenshots/videos and no backend, prefer **Cloudflare Pages** when available:

- generous free tier and CDN delivery;
- supports direct folder deploys via Wrangler;
- easy project URL and custom-domain path later;
- can be paired with Cloudflare Access if the manual must become private.

GitHub Pages is acceptable for simple public Git-based docs. Netlify drag-and-drop is useful for quick temporary review. Vercel is fine when the project already standardizes on Vercel, but is often unnecessary for a plain static manual.

## Clean packaging rule

Do not deploy the whole working artifact directory by default. Build a clean public directory containing only:

- `index.html` or the intended public entry pages;
- assets actually referenced by public HTML (`src`, `href`, `poster`);
- dynamically generated public assets that are referenced from inline data/JS rather than literal HTML attributes, such as workflow-topic video filenames or poster paths;
- minimal hosting metadata such as `_headers`.

When the shell generates lesson/video markup from JavaScript data, a naive HTML-attribute crawler can miss assets. Pair the crawler with one of these explicit inclusions: read the manifest/data object and copy its media paths, scan inline code for known public asset path patterns, or include a bounded public media allowlist such as `video/*.mp4` plus matching posters. Verify the resulting package file list before deploy.

Exclude internal and production-support material unless explicitly intended for readers:

- `qa/`, `sources/`, `.hermes/`, handoffs, status files;
- capture/probe/record scripts;
- raw working screenshots or Driver.js frame dumps not linked from the manual;
- render/composition directories used only to create videos;
- peer/Hermes/workflow evidence.

## Version-lock / handoff rule

Before deploying, identify the **accepted source of truth** for the exact visual/content version. If a peer/controller says a staging directory is already prepared, deploy that directory as-is. Do **not** regenerate the package, re-copy from source, patch missing-looking UI markers, or restore an older “locked” invariant unless the current gate explicitly asks for it. In manual projects, two previously valid variants can conflict (for example, node-level role chips vs arrow-midpoint badges). Treat the latest gate/handoff as authoritative and verify its explicit token/visual invariants before touching files.

If a deploy or verification step reveals a mismatch:

1. HOLD further deploys and writes.
2. Report exactly which source path, staging path, deployment URL, and token scan were used.
3. Wait for the controller/owner to choose the restore target.
4. When re-approved, deploy the current staging directory unchanged and verify production only.

## Direct Cloudflare Pages deploy pattern

Prerequisites: Wrangler authenticated for Pages deploys.

```bash
npx --yes wrangler@latest whoami
npx --yes wrangler@latest pages project create <project-name> --production-branch main
npx --yes wrangler@latest pages deploy /path/to/public-dir --project-name <project-name> --commit-dirty=true
```

### Authentication and account pitfalls

- Run `wrangler whoami` immediately before deploy and record the email/account ID in the deployment evidence. Cloudflare Pages project names are account-scoped; the same human may be logged into the wrong Cloudflare account for the intended production URL.
- If OAuth was previously authorized but deploy returns `Authentication error [code: 10000]`, refresh Wrangler login instead of retrying the deploy loop.
- On a local macOS session, prefer `npx --yes wrangler@latest login` with the default browser-open flow when possible. If using `--browser=false`, do not reuse old OAuth URLs: Wrangler binds each URL to a fresh `state` and temporary localhost callback server. A stale callback can produce `Received query string parameter doesn't match the one sent` or a `localhost refused` browser error after the server times out.
- If the callback fails, kill the old login process and start a fresh one. If necessary use `--callback-host 127.0.0.1 --callback-port 8976`, but note Wrangler still redirects the browser to `localhost:8976`; verify the temporary server is actually listening before asking the user to approve.

### Project-not-found rule

If deploy fails with `Project not found`, do **not** immediately create a new project when the user expects to preserve an existing production URL. First compare:

- intended production URL/project from the latest handoff;
- `wrangler whoami` account email/account ID;
- `wrangler pages project list` in the active account.

Only create a new Pages project after deciding that a new public URL is acceptable. Creating a project with the same requested name in a different account can yield a suffixed Pages hostname such as `<project>-<suffix>.pages.dev`; that is a valid new deployment, but it is **not** an overwrite of the original `<project>.pages.dev` production URL.

### New-account deployment rule

When the owner explicitly asks to deploy the manual into a different/new Cloudflare account:

1. Treat the old production URL as out of scope unless the owner also says to update or delete it.
2. Confirm active Wrangler identity with `whoami` and record the new account email/account ID.
3. Run `pages project list` in the new account before creating anything.
4. If the target project name is available, create it in the new account and record the production alias Cloudflare assigns. A suffixed alias such as `<project>-<suffix>.pages.dev` is expected and should be reported as the new sharing URL, not treated as a failed deploy.
5. After deploy, compare the new production URL against the old one with a lightweight HTTP/SHA/token check so the report proves which URL changed and which one stayed untouched.
6. Update `HANDOFF.md` or the deployment handoff with both account identities, both URLs, and the final verdict.

### Dynamic-asset sync rule

Before a redeploy, verify that staging/public deploy directories include assets referenced from JavaScript data as well as literal HTML attributes. In static interactive manuals, screenshots or media can be selected dynamically by workflow tabs and will not appear in simple `src`/`href` scans. If remote smoke shows broken images but local refs look complete, sync the bounded public media directory from the accepted showable artifact (for example `screenshots/`), redeploy, and rerun remote asset + browser-tab checks. Record this as a package-sync correction, not as a content redesign.

## Verification after deploy

Verify the production alias, not only the unique preview URL:

```bash
curl -I -L https://<project-name>.pages.dev/
```

Then run a remote asset probe against the deployed HTML:

- fetch the HTML from the public URL;
- extract local `src`, `href`, and `poster` refs;
- `HEAD` or `GET` each local ref via the public base URL;
- require refs count to match the expected public set and missing refs to be zero.

Cloudflare/static-host quirk: if a bulk `HEAD` probe reports 403/blocked for many otherwise-visible assets while direct browser/curl page checks pass, do not immediately classify the deployment as broken. Re-probe with a browser-like `User-Agent` and a bounded `GET`/`Range: bytes=0-0` request for each public file or referenced asset. Treat the range GET/browser probe as the reachability evidence, and record the original HEAD behavior as a probe-method caveat rather than an asset failure.

Browser smoke should include:

- open the production URL;
- switch every workflow/topic tab used by the manual shell;
- confirm key generated counts/invariants if the page has synchronized workflow state;
- open at least one screenshot/modal and confirm image/caption;
- check browser console and JS errors.

## Reporting

Report:

- production URL for sharing;
- preview/deployment URL if useful, clearly secondary;
- host/project name;
- what was included/excluded from the public package;
- HTTP, asset, interaction, modal/media, and console verification evidence;
- caveats that remain non-blocking polish rather than deployment blockers.

Do not claim domain-specific accounting/tax/payroll correctness just because the static site deployed successfully.
