# CHORA × VEX Execution Binding Contract v0.1

Status: Draft  
Date: 2026-03-20  

---

## 1. Purpose

Bind CHORA continuation tokens (v3) to runtime execution enforcement.

Execution becomes contingent on a valid, verified, and context-bound token.

---

## 2. Invariant

No valid signed continuation artifact  
→ No execution allowed  

---

## 3. Scope

This contract defines:

- Token binding surface
- Runtime verification requirements
- Execution gating rules
- Failure conditions

---

## 4. Normative Rules

### 4.1 Pre-execution requirement

Execution MUST NOT begin without:

- valid token
- valid signature
- valid binding match

---

### 4.2 Binding surface (MUST match runtime)

- request_sha256  
- action_class  
- policy_context_hash  
- identity  
- nonce  
- exp  

---

### 4.3 Signature

- RFC 8785 JCS canonical payload  
- Ed25519 signature  
- raw UTF-8 canonical bytes  

---

### 4.4 Fail-closed behavior

Any mismatch → execution denied

---

### 4.5 Non-bypassability

Verification MUST be:

- synchronous  
- blocking  
- pre-execution  

---

### 4.6 Token validity

Invalid if:

- expired  
- replayed nonce  
- mismatched context  
- invalid signature  
- unknown schema  

---

## 5. Execution model

Token ≠ execution permission  

Execution permission is granted only after:

verification → capability issuance  

---

## 6. Capability requirement

Runtime MUST issue:

short-lived internal capability token  

Execution MUST depend on this capability.

---

## 7. Action classes (v0.1)

- READ_ONLY  
- FILE_MUTATION  
- NETWORK_CALL  
- TOOL_EXECUTION  
- CODE_EXECUTION  
- PUBLISH  

Exact match required.

---

## 8. Identity

Minimum:

- aid  
- identity_type  

Mismatch → deny

---

## 9. Non-authorizing outcomes

- HALT → no token  
- ESCALATE → no token  

Only ALLOW → token issuance

---

## 10. Failure codes

- TOKEN_INVALID  
- TOKEN_EXPIRED  
- TOKEN_SIGNATURE_INVALID  
- TOKEN_MISMATCH  
- TOKEN_REPLAY  

---

## 11. Compliance

DEV:
- unbound identity  

CANONICAL:
- full binding enforcement  

HIGH ASSURANCE:
- hardware identity  

---

## 12. Deferred

- multi-action tokens  
- ZK binding  
- quorum authorization  
- hardware binding (mandatory)  
