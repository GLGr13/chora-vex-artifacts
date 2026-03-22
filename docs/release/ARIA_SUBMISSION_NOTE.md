# ARIA Submission Note - CHORA x VEX

This repository contains the public reference artifacts accompanying the ARIA submission for governed AI execution.

## Core claim

Continuation authority must be externalized, enforced, and cryptographically bound to execution.

This system implements that claim as a concrete architecture.

## Enforcement guarantee

Enforcement is implemented at the runtime boundary via `verify_continuation_token`, which prevents execution unless a valid, signed continuation artifact is present.

## Core invariant

No valid authorization artifact -> No execution

This changes the execution model from:

model decides -> system executes

to:

model proposes -> external authority decides -> execution is conditionally allowed

## Architecture summary

Intent -> CHORA Gate -> Authorization Token -> AEM Enforcement -> Execution -> VEX Ledger -> Merkle Commitment -> Public Anchor

- CHORA defines continuation authority
- AEM enforces execution (non-bypassable)
- VEX records governed execution
- Merkle ensures deterministic integrity
- Public anchoring provides external custody

## Governance separation

- Synchronous loop (binding):
  ESCALATE -> Resolution -> Re-evaluation

- Asynchronous loop (non-binding):
  Ledger -> Audit -> Reconstruction -> Feedback

The asynchronous loop does not affect current execution.

## Contract alignment

The execution-binding contract and the architecture diagram are strictly equivalent.

There is no interpretation layer between specification and execution.

## Status

- Execution Binding Contract v1 - locked
- Evidence Capsule v0.3 - locked
- Token Contract v3 - locked
- Cross-system verification - validated
- Runtime enforcement - active

## Outcome

This repository represents a working control-plane system for governed AI execution, not a conceptual proposal.
