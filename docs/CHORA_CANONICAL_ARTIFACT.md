# CHORA — Canonical Governance Artifact

## Definition

CHORA externalizes continuation authority.

The model proposes.  
The Gate decides.

## Decision

- ALLOW
- HALT
- ESCALATE

## Flow

Proposal → MCS → Gate → Capsule → Execution

## MCS Role

MCS can override:
- ALLOW → HALT
- ALLOW → ESCALATE

## Custody

- external_non_bypass
- no continuation without authorization

## Enforcement

Execution requires:
- valid capsule_root
- valid signature
- valid continuation token

## Design Laws

- No continuation without authorization
- No recovery without escalation
- No decision without custody

## Position

CHORA uses v0.3 as a governance commitment layer.
