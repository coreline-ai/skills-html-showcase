# Risky Action Policy for User Manuals

Use this for workflows that can change business state, external visibility, ledgers, stock, payments, legal/compliance state, or user permissions.

## Rule

Do not capture or instruct risky actions against production data. Use a disposable demo fixture, or convert the lesson to read-only explanation.

## Common risky actions

- Submit, Cancel, Amend, Approve, Publish, Send, Pay, Reconcile, Close.
- Stock reconciliation, stock entry submit, inventory valuation changes.
- Invoice/payment/journal entry submit, ledger-affecting actions.
- User/role/permission changes.
- External emails, customer portal publication, payment gateway actions.

## Required fields before media production

```yaml
risky_action: true
safe_fixture_required: true
safe_fixture_available: false
risk_handling: read_only_explanation # demo_capture | read_only_explanation | blocked
reset_plan: null
```

## Gate decisions

- `demo_capture`: only if fake data, disposable environment, and reset/rollback plan are verified.
- `read_only_explanation`: allowed when UI can be shown without executing the action.
- `unsaved_form_capture`: allowed for screen-reading lessons when no suitable demo document exists and the operator only opens a New form, optionally observes fields/placeholders, and does not click Save/Submit or create persistent data. Record it explicitly as screen evidence, not a completed transaction walkthrough.
- `blocked`: use when neither safe fixture nor read-only/unsaved evidence exists.

## Review card requirements

Every risky media/review card must state:

- Environment and version.
- Fake data used.
- Action performed or explicitly not performed.
- Reset/rollback method.
- Excluded professional advice, if applicable.
