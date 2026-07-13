# Tool Compatibility Targets

Use this when a project manifest exposes a gap in portable manual-production scripts.

## Context

- Project/package:
- Manifest path:
- Current phase:
- Tool patch status: not_ready | ready_for_validation | validated

## Expected behavior

| Tool | Expected behavior | Must not do | Status |
| --- | --- | --- | --- |
| `manifest_lint.py` | Validate required phase/risk/media/QA fields | Treat pre-capture status as final | pending |
| `validate-manual-package.py` | PASS or actionable warnings for active schema mode | Require final-only fields in pre-capture mode | pending |
| `build-static-manual.py` | Generate provisional preview only when requested and bannered | Create partial output before schema preflight | pending |
| `build-evidence-map.py` | Generate lesson/evidence-tier/live-UI-needs matrix | Claim source evidence is live UI unless explicit | pending |
| `glossary_coverage.py` | PASS or list missing labels/false positives | Treat heuristic PASS as domain/content QA | pending |

## Stable checks before tool patch

Record only tools known to be ready. Do not run incompatible builders unless the purpose is explicitly to capture mismatch evidence.

```text
manifest_lint:
glossary_coverage:
not_run:
```

## Patched-tool validation

```text
validate-manual-package:
build-static-manual:
build-evidence-map:
glossary_coverage:
```

## Result

- PASS:
- WARNINGS:
- BLOCKERS:
- Follow-up skill patch:
