# Large Open-Source Product Inventory Checklist

Use this when the product is too large to fully operate in Phase 1, especially ERP/CRM/accounting/manufacturing systems.

## Phase 1 closeout sections

1. **Access and source list**
   - Repo path/URL/commit or release.
   - Live/demo/staging access status.
   - Public docs URLs and extraction quality.
   - Workspace/menu/schema/report/page sources.
   - Suitability and limits for each source.

2. **Module / work-area inventory**
   - Area name.
   - Evidence status: `확인됨`, `추정`, `미확인`.
   - Source path/URL/screenshot/command output.
   - User-facing relevance.
   - Permission/version/config dependency.

3. **Manualization decision table**
   - Area/module.
   - Reader job.
   - Main screens or entities.
   - Document / omit / bug / impossible state / out of scope / owner decision.
   - Difficulty and domain risk.
   - Required live UI capture.

4. **Separate-manual candidates**
   - Installation/infrastructure/admin operations.
   - Developer/API/customization docs.
   - Portal/customer-facing surfaces.
   - Advanced domain tracks.

5. **Domain risk gates**
   - Accounting, tax, legal, medical, payroll, security, compliance.
   - Decide before drafting: expert review required, general feature description only, or excluded.

6. **Phase 2 owner decisions**
   - Product version/release basis.
   - Primary audience and excluded audiences.
   - Localization/translation policy.
   - Demo data, sample company, currency/tax setup.
   - Role/permission profiles for capture.
   - First release scope.

7. **Skill feedback**
   - Skill feedback.
   - Process friction.
   - Suggested skill patch.

## ERP-style extra checks

- Fixed product version and build/date.
- Sample company, fiscal year, currency, warehouse, tax, and chart-of-accounts assumptions.
- Role-based screen differences.
- Submit/cancel/amend flows and irreversible-ish consequences.
- Ledger, inventory valuation, tax, payment, or compliance side effects.
- Original visible menu labels to preserve or bilingualize.
- Distinguish module/menu coverage from business workflow coverage.

## Public docs extraction caution

If an extracted page title/content does not match the requested URL, mark it as `docs extraction risk` and do not use it as sole evidence. Cross-check important definitions and paths against live UI, repo config, or source files.
