# Beginner Comprehension Exam Loop

Use when a manual is meant for first-time operators or when the owner questions whether the guide is actually understandable.

## Pattern

1. Define 2–4 beginner personas by job context, not by generic demographics.
   - Example: sales/CS newcomer, purchasing/warehouse newcomer, accounting newcomer.
   - Each persona should start with “does not know this system” and receive only the manual sections a real reader would use.
2. Tell each persona exactly what to read:
   - workflow selector / top sequence
   - workflow map
   - right-side step/check panel
   - flow-specific focus screenshots
   - common checks / boundary notes
3. Test comprehension with operational questions, not recall questions.
   - Which document number, party, item, amount, quantity, or status should you name?
   - Which document changes stock, which documents change billing/payment state?
   - Where would you start if the work is already mid-flow?
   - What must you not infer from the visible ERP value?
4. Grade as `PASS`, `REQUEST_CHANGES`, or `PASS_BOUNDED`.
   - `PASS`: persona can explain the flow and name the concrete screen/value evidence.
   - `REQUEST_CHANGES`: persona cannot map steps to screens, confuses document effects, or over-infers domain meaning.
   - `PASS_BOUNDED`: acceptable only when the unresolved item is explicitly out of the current reader/task scope, not because a fix is inconvenient.
5. If any persona fails, convert the failure into manual edits:
   - add/replace focus cards
   - align step numbers with screenshots
   - add concrete document IDs, parties, items, quantities, amounts, and statuses
   - add branch/start notes for mid-flow cases
   - add domain boundary notes for accounting/tax/stock-policy interpretations
6. Retest after edits. Do not deploy or close the workflow until the failed comprehension point is either fixed or consciously excluded from scope.

## Strong signal failures

Treat these as blockers for beginner manuals:

- The guide shows a numbered flow but the focus screenshots do not have the same numbered coverage.
- A named document/report/status/effect is represented only by a nearby workspace, list, or earlier document.
- The learner cannot tell whether the UI value is an ERP-internal value vs. a real-world bank/tax/legal/stock-policy conclusion.
- The learner cannot tell whether the sequence is mandatory or a representative checking path.

## Closeout discipline

If the owner says to keep going until no improvement candidates remain, do not leave `PASS_BOUNDED` items that are inside the covered beginner scope. Reopen/add a work item, replace proxy/adjacent evidence with direct evidence, redeploy if needed, rerun remote QA, and close only when the known candidate list is empty for the promised scope.
