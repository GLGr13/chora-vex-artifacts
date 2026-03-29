# CHORA Gate Spec v0.4

Status: Draft  
Role: External Continuation Authority  
Scope: Minimal public standard surface for governed execution

---

## 1. Purpose

Define the minimal, non-bypassable continuation authority interface for governed execution systems.

CHORA is not a model.  
CHORA is not a policy engine.

CHORA is an external decision primitive for continuation authority.

---

## 2. Core Principle

Execution MUST NOT proceed unless a valid continuation artifact is present.

A continuation artifact MUST be:

- Signed (Ed25519)
- Time-valid (iat / exp)
- Context-bound (intent + execution target)
- Verifiable (JCS canonical form)

If any condition fails → execution MUST be denied.

---

## 3. Decision Surface

CHORA Gate returns exactly one of:

- ALLOW
- HALT
- ESCALATE

No implicit continuation is permitted.

---

## 4. Escalation Path (EMS)

If ESCALATE:

- Execution is paused
- EMS must resolve

EMS resolution states:

- RESOLVED_ALLOW
- RESOLVED_HALT

Only RESOLVED_ALLOW permits continuation.

---

## 5. Enforcement Boundary

Execution runtimes MUST enforce:

"verify_continuation_token"

If token verification fails:

→ execution MUST NOT start  
→ execution MUST NOT continue  

This boundary MUST be non-bypassable.

---

## 6. Segmented Execution

Execution is divided into bounded segments.

Each segment requires:

→ a valid continuation token

Revocation becomes effective:

→ at the next execution boundary

---

## 7. Cryptographic Requirements

- Canonicalization: RFC 8785 (JCS)
- Hashing: SHA-256
- Signature: Ed25519

Signed payload MUST include:

- schema
- issuer
- iat
- exp
- nonce
- source_capsule_root
- execution_target

---

## 8. Continuation Token

Continuation artifacts MUST conform to:

- Schema: chora.continuation.token.v3 (or newer compatible version)
- Canonicalization: RFC 8785 JCS
- Signature: Ed25519 over canonical payload

Required signed fields:

- schema
- issuer
- iat
- exp
- ledger_event_id
- resolution_event_id
- source_capsule_root
- nonce
- execution_target (aid, circuit_id, intent_hash)

Execution MUST be bound to execution_target.
Any mismatch MUST result in denial.

## 9. Invariants

- No continuation without authorization
- No valid token → no execution
- No EMS resolution → no continuation
- No bypass of verification boundary

---

## 10. Philosophy

CHORA does not improve reasoning.

It enforces whether execution is allowed.

This is a control-plane primitive, not a model capability.
