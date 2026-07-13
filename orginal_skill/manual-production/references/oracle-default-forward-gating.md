# Oracle Default-Forward Gating

Use this when a manual-production run is both a real deliverable and a test of the portable skill itself.

## Problem

Large manuals produce many owner-decision candidates: target version, audience, label policy, capture environment, safe fixture policy, media tooling, and deferred domains. Treating every candidate as a user question stalls the work and hides whether the skill can operate as a production system.

## Rule

If the user has stated the goal is to complete the distributable skill and exemplar manual, the oracle should set conservative defaults and continue the gated loop.

Ask the user only when a decision is:

- unsafe or irreversible;
- externally visible/published;
- credential/payment/real-data related;
- a material scope change;
- not reasonably defaultable from the stated goal.

## Default pattern

Record defaults in `sources/owner-decisions.md`, `manifest.yml`, or the worklog:

```yaml
decisions:
  target_version: ERPNext v15 stable
  audience: operations_admin + business_user
  label_policy: Korean explanation + visible English label
  capture_source: reproducible local/demo environment preferred
  risky_actions: safe fixture only; otherwise read-only/blocked
  excluded_domains:
    - tax/accounting/legal advice
    - payroll/compliance
```

Then send the peer the next narrow phase instruction with:

- what is now decided;
- what remains caveated;
- exactly what to produce;
- exactly what not to produce;
- the required STOP line.

## Pitfall

Do not confuse `owner decision` with `owner question`. Many owner decisions can be made by the oracle as safe defaults. The worklog should preserve them as override points, not blockers.
