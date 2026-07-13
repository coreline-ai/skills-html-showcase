# Capture Next Checklist

Use this when capture is blocked today, but the next safe executable checks are known.

## Boundary

This checklist is not permission to run a long-lived app stack. It sequences checks from low-risk readiness to monitored stack start.

## 1. Runtime/daemon reachability

```bash
<runtime> --version
<runtime> info
<runtime> ps
```

Expected:

```text
CLI installed:
Daemon/service reachable:
Current running workloads:
```

## 2. Pull-only / artifact fetch

```bash
<runtime> pull <image:tag>
```

Record image digest/tag/platform. Pull success is not app readiness.

## 3. Compose/config prep without start

```bash
<runtime> compose -f <compose-file> config
```

Record config render success/failure and unresolved variables.

## 4. Monitored stack start — only when authorized

```bash
<runtime> compose -f <compose-file> up -d
<runtime> compose -f <compose-file> ps
<runtime> compose -f <compose-file> logs --tail=100
```

Record container IDs, ports, and health state.

## 5. App-ready check

```bash
curl -I <url>
# plus browser login check in safe demo/staging only
```

## 6. Stop/report

```bash
<runtime> compose -f <compose-file> ps
<runtime> compose -f <compose-file> down
```

If keeping it running is explicitly requested, record IDs, ports, logs path, owner, and stop command.

## Hard stops

- No real data.
- No v16/latest as proof for v15.
- No screenshots/video before app-ready + target version/source are recorded.
- No unreported background services.
