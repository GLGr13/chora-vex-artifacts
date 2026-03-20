# CHORA AEM Runtime Enforcement Spec v0.2

Status: Draft
Date: 2026-03-20

---

## 1. Purpose

Define runtime enforcement for direct identity-bound, proof-bound execution binding.

---

## 2. Flow

Attested Intent
-> CHORA decision
-> Signed continuation token
-> Local AEM verification
-> Capability grant
-> Execution

---

## 3. Verification order

The AEM MUST verify, in order:

1. token signature
2. expiry / nonce
3. aid match
4. local hardware identity
5. PCR binding (High Assurance)
6. request_sha256
7. intent_hash
8. circuit_id
9. action_class
10. policy_context_hash
11. requested capability scope

Any failure -> EXECUTION_DENIED

---

## 4. API

POST /verify-and-authorize

Input:

{
  "token": {},
  "runtime_context": {
    "aid": "",
    "request_sha256": "",
    "intent_hash": "",
    "circuit_id": "",
    "action_class": "",
    "policy_context_hash": "",
    "nonce": "",
    "requested_capabilities": []
  }
}

---

## 5. Response

SUCCESS:

{
  "status": "EXECUTION_PERMITTED",
  "capability_grant": {
    "grant_id": "",
    "capabilities": []
  }
}

FAIL:

{
  "status": "EXECUTION_DENIED",
  "reason_code": ""
}

---

## 6. Enforcement rule

Execution MUST NOT start unless:

status == EXECUTION_PERMITTED

---

## 7. Capability enforcement

The capability grant MUST authorize only the specific operations permitted for this token.

Runtime enforcement SHOULD be syscall-level or equivalent boundary-level enforcement.

---

## 8. Profiles

DEV:
- local verification

CANONICAL:
- direct aid binding
- intent_hash + circuit_id verification
- capability grant enforcement

HIGH:
- PCR verification
- silicon-root identity verification
- syscall-level enforcement
