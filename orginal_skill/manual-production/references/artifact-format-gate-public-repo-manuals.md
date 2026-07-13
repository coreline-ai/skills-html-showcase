# Artifact-format gate for public repo manuals

Use this when the user asks for a manual for a public GitHub/open-source product and has not explicitly said whether they want a Markdown document, a showable HTML/tutorial package, or a runtime-captured UI guide.

## Problem this prevents

A repo/docs-only request can look like a Markdown-admin-manual task, but many users expect a deployable manual package: `index.html`, lesson pages, source/evidence records, QA, and handoff. Defaulting to a single `.md` file can be a premature artifact decision even if the content is grounded.

## Required gate

Before writing lesson bodies, classify the artifact target:

1. **Markdown/admin reference** — acceptable only when the user asks for a document/runbook or explicitly accepts a docs-only artifact.
2. **Static manual package** — default when the user says “manual” for a product/operator audience and no narrower artifact is specified. Produce at least `index.html`, `lessons/`, `sources/`, `qa/`, `manifest`, `STATUS`, and `HANDOFF`.
3. **Live UI captured tutorial** — required when the user asks for screenshots, click paths, videos, or exact UI walkthroughs. Start/capture the runtime only when safe and approved; otherwise mark UI capture needs.

If ambiguity materially changes the artifact shape, ask the owner before production. If the owner has already corrected the artifact target, proceed with that target and record the correction as a reusable skill lesson.

## Reporting boundary

For repo/docs-only packages, do not claim UI/runtime PASS. Say exactly what was verified: official docs/repo files, compose config syntax, static package refs, and content QA. Put runtime gaps in `qa/` or `STATUS`, not in user-facing HTML.