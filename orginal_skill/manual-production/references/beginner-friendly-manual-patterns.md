# Beginner-Friendly Manual Patterns

Source inspiration: `html-for-beginners` style guide. This reference adapts the useful beginner-learning patterns into generic operator/admin manual production. It does **not** import that skill's harness-specific output paths or fixed visual tokens.

## Core posture

A manual is for someone who does not yet know the system. Do not write a compressed expert summary. Write the missing mental model:

1. What is this screen/task for?
2. When would the operator use it?
3. What input must already exist?
4. What changes after the action?
5. What visible state proves it worked?
6. What mistake should the beginner avoid?

For ERP/admin products, this is especially important because one visible screen can affect another module later. Explain the consequence in plain language before teaching the click path.

## Required beginner aids

| Aid | Use when | Manual-production adaptation |
| --- | --- | --- |
| Concept primer | A lesson begins with a workflow or domain object the reader may not know | Add a short “먼저, 이게 뭔가?” paragraph/card before steps |
| One-line mental model | A section needs orientation | Add a brief “한 줄로 보면…” summary, but do not compress the rest |
| Term explanation | English acronyms, ERP DocTypes, statuses, permissions, or domain terms first appear | Write `English term + Korean meaning + plain meaning`; optionally add analogy |
| Everyday analogy | Abstract relationship, cross-module effect, or status lifecycle is hard | Use office/store/warehouse/order metaphors, not project-internal analogies |
| Danger/good pair | Common beginner mistake exists | Put the mistake and the recommended action next to each other |
| Review card | A screen/video is shown | Explain purpose, what to look at, and what is intentionally not covered |
| Takeaway/checklist | A lesson ends | Give 3–5 concrete checks the beginner can perform now |

## Beginner-first lesson shape

For each production lesson, prefer this shape unless the domain requires otherwise:

1. **Concept primer** — what this workflow/object is and why it exists.
2. **Mental model** — one short summary of how to think about it.
3. **Prerequisites** — what master data, role, or safe fixture is needed.
4. **Flow map** — trigger → preparation → action → review → output.
5. **Step path** — only after the above, show screens/clicks.
6. **Danger/good pair** — common mistake + safer habit.
7. **Review checks** — what visible labels/status/report prove the step.

This complements, not replaces, `manual-verification`: the verifier should check whether these beginner aids are present when needed and whether they explain actual product behavior.

## Copy rules

- Prefer plain Korean over internal or expert shorthand.
- Do not merely translate labels; explain why the user sees them.
- Do not over-compress. The goal is easier understanding, not shortest possible copy.
- Use concrete, safe sample values only when they cannot be mistaken for real business advice.
- Explain consequences before risky actions: Submit, Cancel, Amend, invoice/payment, stock mutation, permissions, public publishing.
- Avoid tables for dense beginner guidance when stacked cards are clearer on mobile.
- Do not nest colored boxes; keep the page visually flat.
- Keep prose/card balance. If every paragraph is a box, the page becomes noisy.
- Never leak user memories, project status, Hermes/peer details, or production-tool names into learner-facing copy.

## What not to import from html-for-beginners

- Do not use `/mnt/user-data/outputs` or `present_files` in Hermes.
- Do not assume `web_fetch`; use Hermes web/file/OCR tools as appropriate.
- Do not force its red/off-white design tokens over the operator-guide design system. Import the teaching pattern, not the exact style.
- Do not treat article/PDF explanation flow as a replacement for real-system inventory and live UI verification.
