# Capture-Blocked ERP/Manual Slice Pattern

This reference was distilled from an ERPNext v15 Korean manual production run where the local capture lab was blocked because Docker CLI existed but the daemon was unreachable. The durable pattern is not the Docker failure; it is how to keep a large manual moving without fabricating UI truth.

## When to use

Use this pattern when:

- The target product/version is known.
- Live UI capture is required for final steps/media.
- Capture lab is temporarily unavailable.
- You still need useful scaffold/provisional content.

## Pattern

1. Keep production gated and explicitly state capture/media remains blocked.
2. Draft only conceptual/operator onboarding content.
3. Mark every UI-specific path, button, label, state transition, and media need as `UI_CAPTURE_REQUIRED`.
4. For risky workflows, keep wording read-only and add manifest fields:
   - `risky_action: true`
   - `safe_fixture_required: true`
   - `safe_fixture_available: false`
   - `risk_handling: read_only_explanation_until_safe_fixture_ready`
5. Distinguish `risky_action` from `domain_expert_required`:
   - A report lesson may not mutate data but may still need expert review for interpretation risk.
   - An invoice/payment lesson may be both action-risky and domain-risky.
6. Update glossary and risk register as new labels/risk classes appear.
7. Run manifest lint and a file-presence/content-marker verification before closeout.
8. Do not create screenshots/videos/HTML or claim final manual completion.

## Useful provisional lesson headings

- Status / UI capture / safe fixture line
- Source evidence with evidence tier
- Purpose
- Operating concept
- Read-only flow or things to understand
- UI capture requirements
- Safety / exclusions

## Evidence-tier reminder

Repo workspace/menu JSON and DocType source can justify outline coverage, but not final user-facing instructions. Final screen steps need live target-version UI evidence.

## Closeout evidence to include

- Files created/updated.
- Manifest lint result.
- Artifact verification result: missing/empty files, expected lesson IDs, risky safe-fixture fields, no media directory, capture markers present.
- Explicit constraints observed.
- Skill/process feedback.
