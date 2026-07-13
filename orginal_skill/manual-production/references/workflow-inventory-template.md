# Workflow Inventory Template

Use this before writing the manual. Fill from the real app/system, not from memory.

| Area | Menu / Entry Point | Route / Screen | User Goal | Visible States / Filters | Primary Actions | Risk Level | Document? | Decision / Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Example | Content > Banners | `/admin/banners` | Manage homepage banners | Active, Draft | Create, Edit, Reorder | Public output | Document | Verify public homepage after save |

## Decision Values

- `Document`: normal, useful workflow for the target reader.
- `Omit`: real but irrelevant to this manual's reader/scope.
- `Bug`: visible behavior is broken or misleading.
- `Impossible state`: UI exposes a state/filter/status that cannot occur in the product model.
- `Owner decision`: requires product/business choice before documenting.
- `Out of scope`: belongs to a different manual or role.

## Required Checks

- Capture the exact label shown in the UI.
- Record whether the action changes production/public/customer-visible data.
- For filters/statuses, verify there is at least one reachable entity or code path that can produce the state.
- For CMS/admin workflows, identify the public/output screen where success must be verified.
- If two routes look similar, note the difference explicitly instead of merging them by memory.
