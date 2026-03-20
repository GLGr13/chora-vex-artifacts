# CHORA x VEX Execution Binding Contract v0.2

Status: Draft
Date: 2026-03-20

---

## 1. Purpose

Bind CHORA continuation tokens to runtime execution enforcement for a specific attested agent instance, a specific computational intent, and a specific proof/circuit surface.

Execution becomes contingent on a valid, verified, and context-bound token.

---

## 2. Invariant

No valid signed continuation artifact for the specific attested agent instance
-> No execution allowed

---

## 3. Scope

This contract defines:

- signed token binding surface
- runtime verification requirements
- capability-grant semantics
- hardware identity binding
- failure conditions

---

## 4. Required signed binding surface

The continuation token MUST bind at minimum:

- aid
- request_sha256
- intent_hash
- circuit_id
- action_class
- policy_context_hash
- nonce
- exp

---

## 5. Normative rules

### 5.1 Pre-execution requirement

Execution MUST NOT begin without:

- valid token
- valid signature
- valid binding match
- valid identity match
- valid capability grant

### 5.2 Direct identity binding

The token MUST bind directly to `aid`.

The AEM MUST verify `aid` locally against the silicon root / attested runtime identity.

### 5.3 Computational promise binding

The token MUST bind:

- `intent_hash`
- `circuit_id`

`intent_hash` locks the token to the exact computational promise.

`circuit_id` prevents replay of a token across different proof surfaces.

### 5.4 Capability semantics

The token/runtime grant MUST authorize specific capability types, not just generic execution.

Execution MUST be limited to granted capabilities only.

### 5.5 Hardware binding

PCR binding is part of this contract for High Assurance enforcement.

If High Assurance mode is active, PCR mismatch MUST deny execution.

### 5.6 Fail-closed behavior

Any mismatch -> execution denied

---

## 6. Execution model

Token != execution permission

Execution permission is granted only after:

verification -> capability issuance

---

## 7. Capability grant model

Runtime MUST issue a signed or integrity-protected internal capability grant authorizing specific actions.

Examples:
- FsRead("/logs")
- NetConnect("api.exchange.example")
- ToolInvoke("planner.read_only")

Capability grants MUST be fine-grained and non-bypassable at syscall / runtime boundary.

---

## 8. Action classes

- READ_ONLY
- FILE_MUTATION
- NETWORK_CALL
- TOOL_EXECUTION
- CODE_EXECUTION
- PUBLISH

Exact match required.

---

## 9. Identity and hardware

Minimum identity binding:
- aid

High Assurance binding:
- aid
- PCR set / hardware measurement match

---

## 10. Non-authorizing outcomes

- HALT -> no token
- ESCALATE -> no token

Only ALLOW -> token issuance

---

## 11. Failure codes

- TOKEN_INVALID
- TOKEN_EXPIRED
- TOKEN_SIGNATURE_INVALID
- TOKEN_MISMATCH
- TOKEN_REPLAY
- TOKEN_AID_MISMATCH
- TOKEN_INTENT_HASH_MISMATCH
- TOKEN_CIRCUIT_ID_MISMATCH
- TOKEN_PCR_MISMATCH
- TOKEN_CAPABILITY_DENIED

---

## 12. Compliance

DEV:
- local verification
- relaxed hardware requirements

CANONICAL:
- full token binding
- direct aid binding
- intent_hash + circuit_id verification
- capability-grant enforcement

HIGH ASSURANCE:
- PCR binding enforced
- local silicon-root identity verification
- syscall-level non-bypassable capability enforcement
