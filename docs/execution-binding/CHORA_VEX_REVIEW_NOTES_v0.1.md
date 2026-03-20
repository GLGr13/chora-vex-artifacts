# CHORA x VEX Review Notes v0.2

Status: Draft
Date: 2026-03-20

---

## Adopted refinements

- direct identity binding (`aid`)
- `intent_hash` binding
- `circuit_id` binding
- capability-grant semantics
- PCR binding moved into contract

---

## Current model

Attested Intent
-> CHORA decision
-> Signed continuation token
-> Local AEM verification
-> Capability grant
-> Execution

---

## Remaining review focus

1. Is the signed field set complete?
2. Should capability grants be fully token-contained or runtime-derived?
3. What is the minimal PCR binding set for High Assurance?
4. Are there any additional replay surfaces beyond nonce + circuit_id?

---

## Goal

Tighten the loop from ZK proof to silicon-enforced action.

---

## Constraint

No redesign of existing systems.
