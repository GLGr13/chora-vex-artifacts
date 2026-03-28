# CHORA ↔ VEX Handshake Contract v0.1

Status: Canonical Draft  
Date: 2026-03-28  

---

## Purpose

Define a fail-closed execution boundary where continuation is externally authorized (CHORA) and locally enforced (VEX).

Execution must not proceed without a valid, signed, context-bound continuation artifact.

---

## Canonical Flow

PROPOSAL
  → CHORA Gate
    → ALLOW | HALT | ESCALATE

ESCALATE
  → EMS
  → RESOLUTION (RESOLVED_ALLOW required)
  → TOKEN ISSUANCE

EXECUTION BOUNDARY
  → VERIFY TOKEN (fail-closed)
  → EXECUTE | DENY

---

## Authority Separation

- CHORA → continuation authority  
- VEX → execution + attestation  
- Rule: execution ≠ authorization  

---

## Continuation Token (v3.1)

- Ed25519 signature  
- RFC8785 JCS canonical payload  

Required fields:

schema  
issuer  
iat  
exp  
ledger_event_id  
resolution_event_id  
source_capsule_root  
nonce  
execution_target  

---

## execution_target Binding (MANDATORY)

aid  
circuit_id  
intent_hash  

Prevents:
- cross-agent reuse  
- cross-context replay  
- intent drift  

---

## Boundary Verification (fail-closed)

Execution allowed only if all pass:

- signature valid  
- time valid  
- nonce match  
- execution_target match  
- custody linkage present  

Else:

DENY  

---

## Mapping to VEX

CHORA → VEX  

continuation token → authorization artifact  
execution boundary → executor.rs  
fail-closed verify → AEM admissibility  
capsule_root → event commitment surface  

---

## Revocation Model

Execution is segmented.

Each segment requires a valid token.

Revocation applies at the next boundary.

---

## Invariants

- No continuation without authorization  
- No recovery without escalation  
- No token without RESOLVED_ALLOW  
- No execution without verification  
- No cross-target reuse  

---

## Canonical Statement

Continuation is permitted only when a valid, signed, time-valid authorization artifact is present and bound to the intended execution target and intent context, and boundary verification is enforced fail-closed.
