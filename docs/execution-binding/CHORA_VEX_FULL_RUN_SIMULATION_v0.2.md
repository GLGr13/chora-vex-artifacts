# CHORA x VEX Full Run Simulation v0.2

Status: Draft
Date: 2026-03-20

---

## Purpose

Demonstrate direct identity-bound, proof-bound, capability-scoped execution enforcement.

---

## ALLOW Path

1. Agent finalizes attested intent
2. Intent Merkle root becomes `intent_hash`
3. Proof surface identified by `circuit_id`
4. CHORA Gate returns ALLOW
5. Continuation token issued with:
   - aid
   - intent_hash
   - circuit_id
   - action_class
   - nonce / expiry
6. AEM verifies:
   - signature valid
   - aid matches local silicon identity
   - PCR binding valid
   - intent_hash matches
   - circuit_id matches
   - nonce unused
   - token not expired
7. AEM issues fine-grained capability grant
8. Runtime allows only granted operations
9. Evidence capsule generated
10. Ledger entry recorded

Result:
EXECUTED

---

## DENY Path: circuit mismatch

Token valid, but `circuit_id` mismatch

Result:
EXECUTION_DENIED

Execution never begins.

---

## DENY Path: PCR mismatch

Token valid, but PCR binding mismatch in High Assurance mode

Result:
EXECUTION_DENIED

Execution never begins.

---

## Key Property

Execution requires:

authorization + identity binding + proof binding + capability grant

---

## What this demonstrates

- No execution without token
- No execution for the wrong attested instance
- No execution for the wrong proof surface
- No execution outside granted capabilities
- No bypass path after enforcement is active
