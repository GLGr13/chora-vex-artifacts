# CHORA <-> VEX Handshake Specification v1

This document defines the canonical handshake between CHORA (authorization authority)
and VEX (execution + attestation system).

It formalizes the boundary at which continuation authority is transferred and enforced.

---

## 1. Purpose

The handshake ensures that:

- No execution begins without a valid CHORA-issued authorization artifact
- The authorization is cryptographically bound to the intended execution
- Enforcement occurs at a single non-bypassable boundary

Core invariant:

No valid authorization artifact -> No execution

---

## 2. Handshake Overview

The handshake consists of three stages:

1. Intent Submission (VEX -> CHORA)
2. Authorization Decision (CHORA -> Token)
3. Enforcement + Execution (VEX local)

---

## 3. Stage 1 - Intent Submission

VEX submits a canonical intent to CHORA.

### Input (canonicalized via RFC 8785 JCS)

- intent_data (structured request)
- capabilities (optional)
- confidence (optional)

### Derived:

- intent_root = sha256(JCS(intent_data))

This intent_root is the binding reference across all stages.

---

## 4. Stage 2 - Authorization Decision (CHORA)

CHORA evaluates the intent and returns:

- decision: ALLOW | HALT | ESCALATE

If ALLOW, CHORA issues a signed continuation token.

### Continuation Token (v3)

Signed fields:

- schema: chora.continuation.token.v3
- issuer
- iat
- exp
- nonce
- ledger_event_id
- resolution_event_id
- source_capsule_root
- intent_root

Signature:

- Ed25519 over JCS canonical payload

---

## 5. Stage 3 - Enforcement (VEX)

Before execution begins, VEX MUST perform:

`verify_continuation_token(token, intent_root)`

This is the enforcement boundary.

### Verification checks:

- signature validity
- schema correctness
- expiration (exp)
- nonce validity
- intent_root match (critical binding)

---

## 6. Enforcement Properties

The enforcement boundary guarantees:

- No valid token -> execution does not start
- No fallback path exists
- No internal override exists
- Execution is cryptographically contingent on authorization

This boundary is implemented at:

Authorization Enforcement Module (AEM)

---

## 7. Execution Flow

If verification succeeds:

authorization -> enforcement -> execution -> attestation -> commitment -> anchoring

If verification fails:

execution does not occur

---

## 8. Failure Modes

| Condition                     | Outcome        |
|-----------------------------|---------------|
| Missing token               | DENIED        |
| Invalid signature           | DENIED        |
| Expired token               | DENIED        |
| Nonce mismatch              | DENIED        |
| intent_root mismatch        | DENIED        |

No degraded execution path is permitted.

---

## 9. Separation of Responsibilities

| Layer        | Responsibility |
|-------------|---------------|
| CHORA       | Defines continuation authority |
| AEM         | Enforces authorization (non-bypassable) |
| VEX         | Executes and records governed execution |
| Merkle      | Ensures deterministic integrity |
| Anchor      | Provides external custody |

---

## 10. Guarantee

This handshake establishes:

- Externalized continuation authority
- Cryptographically bound execution
- Non-bypassable enforcement

There is no execution without authorization.

---

## Status

- Execution Binding Contract v1 - locked
- Token Contract v3 - locked
- Enforcement boundary - active
- Handshake specification - defined

---

## Outcome

The CHORA <-> VEX boundary is now formally specified.

Execution is no longer an internal decision.

It is a governed, externally authorized, and cryptographically enforced transition.

