# CHORA AEM Runtime Enforcement Spec v0.1

Status: Draft
Date: 2026-03-20

---

## 1. Purpose

Define runtime enforcement interface for execution binding.

---

## 2. Flow

Request → Token → Verify → Capability → Execute

---

## 3. API

POST /verify-and-authorize

Input:

{
  "token": {},
  "runtime_context": {}
}

---

## 4. Response

SUCCESS:

{
  "status": "EXECUTION_PERMITTED",
  "capability": {}
}

FAIL:

{
  "status": "EXECUTION_DENIED",
  "reason_code": ""
}

---

## 5. Enforcement rule

Execution MUST NOT start unless:

status == EXECUTION_PERMITTED

---

## 6. Capability

- short-lived
- internal
- non-exported

---

## 7. Mandatory hook

Must run before:

- network
- file
- tool
- execution

---

## 8. Non-bypassability

Forbidden:

- async validation
- post-execution checks

---

## 9. Reference pattern

auth = verify(token, ctx)

if auth != "EXECUTION_PERMITTED":
    deny()

execute()

---

## 10. Profiles

DEV:
- local verification

CANONICAL:
- full binding

HIGH:
- hardware + ledger
