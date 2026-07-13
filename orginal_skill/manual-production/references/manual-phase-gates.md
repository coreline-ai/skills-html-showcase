# Manual Phase Gates and Evidence Discipline

Use this reference when a manual is being produced in stages, especially for large products, open-source apps, ERP/business systems, or when another reviewer/owner is gating progress.

## Phase gate workflow

1. **Phase 1 — Inventory only**
   - Identify source hierarchy, available app/menu/workspace metadata, public docs, repo docs, and live UI availability.
   - Produce a module/workflow inventory and manualization judgment table.
   - Do not write final lesson prose, bulk translations, screenshots, or videos.
   - Separate `confirmed`, `inferred`, and `unconfirmed` evidence.

2. **Phase 2 — Outline gate only**
   - Recommend bounded scope and audience tracks.
   - Define lesson boundaries only: lesson id, title, audience, prerequisites, source evidence, capture needs, excluded risks.
   - Draft a manifest structure, not lesson bodies.
   - Mark which lessons require real UI capture before drafting.
   - List owner decisions required before production.

3. **Phase 3 — Draft/media production**
   - Write user-facing lesson text only after the relevant workflow has enough evidence.
   - Capture screenshots/videos from the agreed live/demo environment.
   - Keep risky/destructive actions on safe fixtures or demo data only.

4. **Phase 4 — QA/correction/final handoff**
   - Run technical QA and content QA separately.
   - Report completed, verified, unresolved, out-of-scope, and risky items separately.

## STOP discipline

When an owner/reviewer is gating phases:

- Stop after each phase closeout.
- Do not start the next phase after `PASS` unless the owner explicitly instructs you to start it.
- End phase closeouts with the exact gate marker requested by the owner, e.g. `STOP — awaiting gate verdict`.

## Phase 2 closeout template

Use this structure for outline-gate handoffs. Keep it boundary-level; do not include step-by-step instructions or translated manual prose.

1. **Recommended bounded scope**
   - Primary v1 scope.
   - Explicit deferrals and separate-track candidates.

2. **Audience tracks**
   - 2–3 possible tracks.
   - One recommended primary track and why.

3. **Lesson boundary table**
   - Lesson id.
   - Title.
   - Audience.
   - Prerequisites.
   - Source evidence.
   - Screen/capture needs.
   - Excluded risks.

4. **Manifest draft**
   - Proposed directory/manifest fields only.
   - Lesson status should remain `outline_only` or equivalent.

5. **Capture-required list**
   - Lessons that cannot move to body drafting before live UI capture.
   - Risky lessons that require demo fixtures or read-only treatment.

6. **Owner decisions before production**
   - Version/environment.
   - Audience/scope.
   - Localization/label policy.
   - Domain expert gates.
   - Risky action handling.

7. **Process feedback**
   - Skill feedback.
   - Process friction.
   - Suggested reusable skill/tooling patch.

## Evidence tier guidance

When repo/docs/live UI differ, label each evidence source by tier:

- `live_ui`: captured or inspected target-version UI. Final source for user-facing steps.
- `workspace_config`: menu/workspace/sidebar configuration. Good for coverage, not final UI truth.
- `doctype_source`: schema/model/report/page source. Good for candidates/fields, not workflow wording.
- `official_docs`: concept or workflow reference. Cross-check before final steps.
- `owner_decision`: scope/version/risk policy decided by operator/oracle.
- `unverified`: known need or assumption without evidence.

## Evidence status rules

Every inventory or outline claim should be labeled, explicitly or implicitly, as one of:

- **Confirmed**: backed by a concrete repo path, URL, screenshot, command output, or live UI observation.
- **Inferred**: supported by adjacent evidence but not yet verified in the live UI.
- **Unconfirmed**: needs an owner decision, live check, domain expert, or additional source.

Do not treat source-code menu/workspace JSON, README files, or public docs extraction as final UI truth. They are planning evidence until verified against the actual target version and role.

## Source hierarchy for large/open-source products

Prefer this order when available:

1. Live UI in the agreed version/environment, with role/permission context.
2. App workspace/menu/sidebar metadata for structural inventory.
3. DocType/report/page definitions for feature and field candidates.
4. Official public docs for concepts and intended workflow.
5. README/dev docs for installation/developer/admin context, usually separate from end-user manuals.

If extraction from public docs has missing content, mismatched titles, or summaries that omit steps, record it as a docs extraction risk and cross-check with repo/live UI.

## ERP/business-system checklist

Before drafting user-facing steps for ERP/accounting/inventory systems, decide:

- Target product version.
- Primary audience track: operations admin, business user, reporting user, or specialist.
- Demo/capture environment and sample data policy.
- UI language/label policy, including whether to use bilingual labels like `판매 주문(Sales Order)`.
- Whether accounting, tax, payroll, legal, healthcare, security, or other regulated domains require expert review.
- Which actions affect ledgers, inventory valuation, external communication, or irreversible-ish document states such as submit/cancel/amend.

## Menu inventory vs workflow inventory

Menu/module lists are coverage evidence, not a finished manual outline. Re-group lessons by user goals and operational flows. For example, a sales lesson may need evidence from customer, item, quotation, sales order, invoice, payment, and report screens rather than one module only.
