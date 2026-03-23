# CHORA Runtime Contracts v1

**Status:** LOCKED  
**Date:** 2026-03-23  

This document defines the runtime governance contracts for CHORA:

- Interop (CHORA ↔ VEX)
- EMS (Escalation Management System)
- Segmented Execution Model

Core principle:

> No valid continuation artifact → No execution.

---

## 1. Overview

CHORA defines a governed execution model where:

> Continuation authority is externalized, cryptographically enforced, and non-bypassable.

---

## 2. Core Laws (LOCKED)

- No continuation without authorization  
- No recovery without escalation  
- No continuation without resolution  
- No valid continuation artifact → No execution  

---

## 3. CHORA–VEX Interop Spec v0.1

### Roles

CHORA:
- returns ALLOW / HALT / ESCALATE  

EMS:
- resolves ESCALATE → RESOLVED_ALLOW / RESOLVED_HALT  

VEX / AEM:
- enforces execution  
- denies execution without valid token  

---

### Gate Request

POST /gate

{
  "nonce": "unique-boundary-nonce",
  "action": {
    "class": "execution_step",
    "payload_hash": "sha256"
  }
}

---

## 4. CHORA EMS Contract v1

### Entry Condition

CHORA Gate outcome == ESCALATE

---

### State Machine

PENDING_REVIEW → RESOLVED_ALLOW | RESOLVED_HALT

---

### Authorization Rule

ems_status == RESOLVED_ALLOW  
AND continuation_authorized == true

---

### Non-Bypass Law

No EMS resolution → No token → No execution

---

## 5. CHORA Segmented Execution Model v1

### Principle

Execution is bounded continuation.

---

### Execution Loop

segment → token → verify → execute → boundary → repeat

---

### Requirements

- token required at every boundary  
- invalid token → execution denied  
- nonce replay → denied  

---

### Revocation

Execution halts by absence of valid continuation.

---

## 6. Canonical Flow

VEX → CHORA → decision  
→ EMS (if needed)  
→ token issuance  
→ execution boundary → verify → execute  

---

## 7. System Invariants

- No continuation without authorization  
- No recovery without escalation  
- No continuation without resolution  
- No token → no execution  

---

## 8. Status

CHORA Runtime Contracts v1 — LOCKED

---

## Final Statement

Execution is not permitted — it is continuously authorized.
