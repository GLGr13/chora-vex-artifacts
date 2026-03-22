# CHORA x VEX Figures

## 1. Deterministic Execution Pipeline

File:
- `chora_execution_pipeline.png`

Purpose:
- Shows the non-bypassable governed execution path:
  Attested Intent -> CHORA Gate -> AEM -> Execution -> VEX Ledger -> Merkle Commitment -> Public Blockchain Anchor

Key invariant:
- No valid authorization artifact -> No execution

## 2. Governed Feedback & Recovery Loops

File:
- `chora_governed_loops.png`

Purpose:
- Shows governance separated from execution:
  - synchronous governance loop (binding)
  - asynchronous audit and learning loop (non-binding)

Key rule:
- Asynchronous loop does NOT affect current execution
