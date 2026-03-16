# CHORA v220 Canonical Architecture

## Canonical layered architecture

```text
Proposal layer
  -> Validation layer (Sensors + MCS)
  -> Authority layer (CHORA Gate)
  -> Supervisory layer (EMS)
  -> Custody layer
  -> Observability layer (Drift Sensors + Governance Metrics)
```

## Canonical design laws

- No continuation without authorization
- No recovery without escalation
- No decision without custody

## Current implementation state

- CHORA Gate is live on VPS
- Merkle v0.3 public gate path is active
- Phase 3 MCS shadow mode is completed
- Replay harness is locked
- v220 is treated as canonical shell

## Architectural intent

The CHORA Gate is the minimal external decision primitive. It is not the whole system. The mechanism around the gate includes validation, artifact production, replayability, and future supervisory recovery.

MCS sits **upstream** of authorization. This means structurally weak proposals should not pass unexamined into the authority layer.
