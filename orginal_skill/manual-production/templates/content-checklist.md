# Content QA Checklist

## Global checks

- [ ] Lesson scope matches manifest.
- [ ] Source evidence is listed with evidence tier.
- [ ] UI-specific labels/buttons/routes are either captured or marked `UI_CAPTURE_REQUIRED`.
- [ ] Korean explanation keeps visible UI English labels in parentheses where needed.
- [ ] No real data, customer data, credentials, or secrets.
- [ ] No tax/accounting/legal/professional advice unless explicitly reviewed.
- [ ] Risky actions have safe fixture policy or read-only/blocked handling.
- [ ] Exclusions are stated for out-of-scope domains.
- [ ] Promotion criteria are clear.

## Lesson-specific checks

| Lesson | Check | Status |
| --- | --- | --- |
| {{LESSON_ID}} | Conceptual flow is correct and non-final if no live UI evidence | pending |
| {{LESSON_ID}} | All UI steps are capture-gated | pending |
| {{LESSON_ID}} | Risk handling matches manifest | pending |

## Promotion criteria

A lesson cannot move to final/handoff until:

- content QA passes;
- technical/media QA passes if media is required;
- manifest status and QA fields are updated;
- reviewer notes and caveats are recorded.
