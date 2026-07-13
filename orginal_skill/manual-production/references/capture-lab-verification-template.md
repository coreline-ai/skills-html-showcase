# Capture Lab Verification Attempt Template

Use this whenever manual production depends on a reproducible browser/app environment for screenshots, Driver.js tours, HyperFrames compositions, or recorded videos.

## Rule

Capture planning is not capture readiness. Record each runtime layer separately.

Registry manifest availability is **not** equivalent to successful local pull/run. A stack is not ready until the app is reachable in a browser and source/version/sample-data state are recorded.

## Closeout template

```md
# Capture Lab Verification Attempt

## Target

- Product/app:
- Target version:
- Capture purpose:
- Environment type: local_docker | local_dev | cloud_demo | staging | other
- Real data allowed: no

## Runtime checks

| Layer | Command / evidence | Result | Interpretation |
| --- | --- | --- | --- |
| CLI installed | `<runtime> --version` |  | CLI exists / missing |
| Daemon/service reachable | `<runtime> info` or health check |  | reachable / blocked |
| Image/tag or artifact exists | manifest/tag check |  | exists / missing / not enough |
| Pull/build succeeds | pull/build command |  | success / blocked / not attempted |
| Stack starts | compose/dev-server command |  | success / blocked / not attempted |
| App ready | HTTP/browser check |  | ready / blocked / not attempted |
| Version/source visible | app screen/API/source note |  | verified / unverified |
| Stack stopped/reported | ps/stop/log evidence |  | stopped / running with id / not started |
```

## If blocked

Record exact stderr/stdout. Do not produce screenshots, videos, HTML embeds, or final UI steps from an unverified environment.

```md
Blocked at layer:
Exact evidence:
Next unblock command:
Fallback candidates:
```

## If started

Before closeout, record:

- Process/container IDs.
- URL/port.
- Login/sample credential source if non-secret demo.
- Stop command or reason it remains running.
- Current running/stopped state.

## Media gate

Only proceed to screenshots/video when all are true:

- CLI/runtime reachable.
- App ready in browser.
- Target version/source recorded.
- Demo fixture/sample data policy recorded.
- Risky-action policy resolved for the lesson.
```
