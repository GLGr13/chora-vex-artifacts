# CHORA × VEX Full Run Simulation v0.1

Status: Draft
Date: 2026-03-20

---

## Purpose

Demonstrate the end-to-end execution-binding flow from CHORA authorization to runtime enforcement.

---

## ALLOW Path

1. Agent proposes NETWORK_CALL
2. MCS returns PASS
3. CHORA Gate returns ALLOW
4. Continuation token v3 is issued
5. Runtime verifies:
   - signature valid
   - binding valid
   - nonce unused
   - token not expired
6. Runtime issues short-lived capability
7. Execution is permitted
8. Evidence capsule is generated
9. Ledger entry is recorded

Result:
EXECUTED

---

## DENY Path

1. Agent proposes NETWORK_CALL
2. MCS returns PASS
3. CHORA Gate returns ALLOW
4. Continuation token v3 is issued
5. Runtime verification fails:
   - action_class mismatch

Result:
EXECUTION_DENIED

Execution never begins.

---

## Key Property

Execution requires:

authorization + verification + binding

---

## What this demonstrates

- No execution without token
- No execution with invalid token
- No execution on mismatched runtime context
- No bypass path after enforcement is active
