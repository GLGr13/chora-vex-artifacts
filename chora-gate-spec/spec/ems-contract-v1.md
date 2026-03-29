# EMS Contract v1

Status: Locked
Role: Supervisory resolution layer after ESCALATE

---

## 1. Purpose

EMS resolves escalated continuation cases.

EMS is entered only after:

CHORA Gate -> ESCALATE

EMS does not replace CHORA.
EMS does not originate authority outside the escalation path.

---

## 2. State Machine

PENDING_REVIEW -> RESOLVED_ALLOW | RESOLVED_HALT

Rules:
- an EMS record must resolve exactly once
- once resolved, it cannot return to PENDING_REVIEW
- once resolved, the result cannot change

---

## 3. Authorization Rule

Continuation is authorized only if:

- ems_status == RESOLVED_ALLOW
- continuation_authorized == true

Otherwise:
- no token
- no execution

---

## 4. Canonical Law

No recovery without escalation.
No continuation without resolution.

---

## 5. Minimal Record Shape

- schema
- ts_utc
- ems_status
- ledger_event_id
- source_capsule_root
- resolution_note
- resolution_event_id
- continuation_authorized
- resolution_ts_utc

---

## 6. Invariants

- No EMS resolution -> no continuation
- No RESOLVED_ALLOW -> no token
- No bypass around EMS for escalated cases
