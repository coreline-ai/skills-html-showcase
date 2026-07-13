# Static standalone lesson depth pattern

Use this when a static operator-guide package contains standalone `lessons/*.html` pages in addition to an index/workflow map.

## Failure pattern

A package can pass index/workflow-map QA while the standalone lesson pages remain too thin: hero text plus a short ordered list that merely repeats the index summary. This is not an operator lesson.

## Production requirement

Every standalone lesson page should teach a bounded job by itself. Include, at minimum:

1. **Purpose and target operator** — who uses this lesson and what decision it supports.
2. **When to use** — the trigger/condition for choosing this procedure.
3. **Prerequisites** — credentials, deployment mode, source data, config ownership, or safety conditions needed before starting.
4. **Step-by-step operator checks** — numbered actions/checks with concrete values, commands, routes, status fields, or source paths where available.
5. **Per-step cautions** — the common wrong conclusion or unsafe shortcut for that step.
6. **Common mistakes** — cross-step misunderstandings to avoid.
7. **Verification/readback** — what evidence proves the lesson goal, and what does not.
8. **Source/evidence links** — official docs, repo paths, screenshots, or UI evidence used to write the lesson.
9. **Next decision/branch** — where the operator goes if the check passes, fails, or requires a larger workflow.
10. **Verification boundary** — what the static page does not prove, especially live UI labels, deployment success, security policy, connector sync quality, or organization-specific data behavior.

## Docs-derived static manuals

When the package is built from public docs rather than live UI:

- Prefer concrete docs-derived commands and configuration names, but do not invent live UI success evidence.
- Add source URLs to `sources/source-map.md` whenever a lesson cites a new official page.
- Replace unverifiable version claims with bounded instructions such as “check the current `go.mod`/official docs before source build.”
- Avoid plan/edition-specific claims unless the cited source proves them; otherwise phrase as “depending on plan/configuration.”

## Verification pattern

Add deterministic QA that counts all standalone lessons and verifies required sections. For each page, record:

- step count
- caution count
- required section headings
- source-reference count
- unsupported/high-risk terms removed
- local `href`/`src` references reachable

Browser-smoke at least the thinnest page and one long page via `file://`; verify section presence, step/caution counts, source evidence, next branch, and boundary text from the rendered page.