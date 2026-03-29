# MCS Sensor Channel v1

Status: Draft
Role: Structural validation upstream of authority

---

## 1. Purpose

MCS validates structural admissibility before a proposal reaches CHORA Gate.

MCS does not authorize continuation.

It only determines whether a proposal is structurally fit to reach authority.

---

## 2. Function

MCS checks for:

- premise declaration
- regime definition
- contradiction detection
- completeness
- confidence alignment

If structural validity fails, the proposal should not continue toward execution.

---

## 3. Relationship to CHORA

MCS is upstream of CHORA Gate.

MCS may:
- pass a proposal forward
- block a proposal
- emit structured signals

MCS must NOT:
- issue authorization
- replace Gate decisions
- bypass EMS or runtime enforcement

---

## 4. Output Status

MCS may emit:

- PASS
- FAIL
- INCOMPLETE

These are structural outcomes, not authority decisions.

---

## 5. Invariants

- diagnosis does not equal authority
- structural validation does not equal permission
- no MCS output can substitute for ALLOW
- CHORA remains the sole continuation authority

---

## 6. Philosophy

MCS gives CHORA structured eyes.

CHORA still decides.
