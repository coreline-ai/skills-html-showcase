# Phase-Gated ERP/Open-Source Manual Production

Use this reference when producing manuals for large apps where source code, docs, and live UI can disagree.

## Phase gates

1. **Inventory**: list source paths/URLs, menu/workspace evidence, workflow candidates, confirmed/inferred/unconfirmed status, exclusions, and risks. Stop for verdict.
2. **Outline Gate**: recommend bounded v1 scope, audience tracks, lesson boundaries, source evidence, capture needs, excluded risks, and owner decisions. Do not write lesson body prose. Stop.
3. **Readiness/Slice**: plan capture environment and sample fixtures; propose manifest/scaffold; draft only non-risky slices and mark missing UI details as `UI_CAPTURE_REQUIRED`. Stop.
4. **Production**: write lesson bodies and create media only from verified target-version UI/source evidence. Risky actions require safe demo fixtures.
5. **QA/Handoff**: run technical QA and content QA separately; report completed/verified/unresolved/out-of-scope.

## Evidence hierarchy

1. Target-version live UI with the relevant role = final source for user-facing steps/media.
2. Workspace/menu config = inventory/outline evidence only.
3. DocType/report/source definitions = feature/field candidates only.
4. Official docs = concept/terminology support; cross-check for staleness or extraction errors.
5. README/dev/infra docs = admin/setup tracks, not ordinary operator lessons by default.

## Required status flags

- `confirmed`: concrete path/URL/screenshot/command output supports the claim.
- `inferred`: plausible from repo/docs but not live-UI verified.
- `unconfirmed`: must become a gate question or risk.
- `UI_CAPTURE_REQUIRED`: no final step wording, screenshot, video, or exact label until live UI verifies it.

## Risk gates

For submit/cancel/amend, stock reconciliation, payments, invoices, accounting/tax/legal/compliance, payroll, or destructive/public actions:

- Use safe demo fixtures only.
- If fixtures/reset are unavailable, convert to read-only explanation and mark media blocked.
- Do not give domain advice (tax/accounting/legal) without explicit expert/source validation.

## Portable templates to keep in the skill pack

- `templates/manual-manifest.yml`
- `templates/lesson-boundary.yml`
- `templates/media-review-card.yml`
- `templates/glossary.md`
- `templates/hyperframes-storyboard.yml`
- `templates/driverjs-tour.yml`

## Media pipeline rule

HyperFrames and Driver.js are production aids, not evidence substitutes. Record source capture, composition/render, embed/playback, content QA, and technical QA as separate states.