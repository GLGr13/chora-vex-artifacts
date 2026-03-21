# CHORA x VEX Execution Binding Contract v1

Status: Locked Draft
Date: 2026-03-21

---

## 1. Purpose

This contract defines the minimum non-bypassable binding required for CHORA authorization to become a mandatory precondition for execution.

Core invariant:

No valid authorization artifact -> no execution

---

## 2. Roles

CHORA Gate:
- Non-bypassable decision plane
- Returns: ALLOW / HALT / ESCALATE

AEM:
- Non-bypassable enforcement boundary
- Blocks execution unless authorization is verified

VEX:
- Custody layer
- Records governed execution → Merkle → external anchor

---

## 3. Core Invariants

- No authorization artifact -> no execution
- Authority != enforcement
- Verification occurs before execution
- System fails closed
- Custody must be reconstructible

---

## 4. Authorization Artifact (v3 baseline)

Signed payload (RFC8785 JCS, Ed25519):

- schema
- issuer
- iat
- exp
- ledger_event_id
- resolution_event_id
- source_capsule_root
- nonce

---

## 5. Execution Binding Requirements

Execution authorization MUST bind to:

- agent instance (aid)
- request (request_sha256)
- attested intent (intent_hash)
- proof surface (circuit_id)
- action scope (action_class)
- policy context (policy_context_hash)
- custody lineage (source_capsule_root)

---

## 6. Hardware Binding (High Assurance)

If enabled:

- PCR must match
- local silicon identity must verify

Mismatch -> EXECUTION_DENIED

---

## 7. Execution Gating

Execution flow:

Attested Intent
-> CHORA decision
-> Signed token
-> AEM verification
-> Capability grant
-> Execution

Execution MUST NOT start unless:

status == EXECUTION_PERMITTED

---

## 8. AEM Verification Order

1. token present
2. JCS canonical integrity
3. signature valid
4. iat / exp
5. nonce (no replay)
6. lineage fields valid
7. custody linkage valid
8. aid match
9. request_sha256 match
10. intent_hash match
11. circuit_id match
12. policy_context match
13. action_class match
14. capability scope valid
15. PCR (if enabled)

Failure -> EXECUTION_DENIED

---

## 9. Capability Enforcement

Execution must be restricted to granted capabilities only.

Enforcement SHOULD occur at syscall boundary or equivalent.

---

## 10. Failure Conditions

Deny execution on:

- missing token
- invalid signature
- expired token
- replay detected
- aid mismatch
- intent mismatch
- circuit mismatch
- policy mismatch
- capability violation
- PCR mismatch

---

## 11. Custody Linkage

Execution produces:

- governed event record (VEX)
- Merkle commitment
- external anchor

Must allow full reconstruction of:

intent -> decision -> authorization -> execution -> custody

---

## 12. Compliance Profiles

DEV:
- basic verification

CANONICAL:
- full binding + capability enforcement

HIGH ASSURANCE:
- hardware identity + PCR + syscall enforcement

---

## 13. Minimal Flow

1. Intent created
2. Validated (Sensors + MCS)
3. CHORA decision
4. Token issued
5. Runtime waits
6. AEM verifies
7. Capability granted
8. Execution
9. Custody recorded

---

## 14. Canonical Statement

CHORA is the decision plane.
AEM is the enforcement boundary.

No token -> no execution.
