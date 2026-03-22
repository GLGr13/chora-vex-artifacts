# Figure Captions

## Figure 1 - Deterministic governed execution pipeline

An agent-generated intent is externally authorized by the CHORA Gate, producing a signed continuation token bound to the canonical intent hash. Execution is enforced at the Authorization Enforcement Module (AEM), where `verify_continuation_token` ensures that no execution can proceed without a valid authorization artifact.

Upon successful verification, execution proceeds and produces a governed event recorded in the VEX Ledger. The resulting Evidence Capsule is deterministically committed via a Merkle root and anchored to a public blockchain, providing external, verifiable custody.

Core invariant:
No valid authorization artifact -> No execution.

## Figure 2 - Governed feedback and recovery loops external to execution

Governance is structurally separated from the execution path and operates through two distinct loops.

The synchronous loop is binding and routes ESCALATE decisions through resolution and re-evaluation before any further execution may proceed.

The asynchronous loop operates over recorded execution artifacts for audit, reconstruction, and downstream feedback, without affecting the current execution state.

Key rule:
Asynchronous feedback does NOT affect current execution.
