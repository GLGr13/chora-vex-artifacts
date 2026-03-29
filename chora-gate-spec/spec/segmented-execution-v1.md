# Segmented Execution v1

Status: Locked
Role: Runtime execution model

---

## 1. Principle

Execution is bounded continuation, not continuous permission.

Execution proceeds in explicit segments.

Each segment requires a valid continuation token before it may execute.

---

## 2. Execution Loop

segment_n
-> present continuation token
-> verify token
-> execute bounded step
-> reach execution boundary
-> repeat

---

## 3. Boundary Requirements

- execution must expose explicit continuation boundaries
- execution without defined boundaries is non-compliant
- boundaries must be visible to the enforcement module

---

## 4. Verification Requirements

Reject token if:

- signature verification fails
- JCS canonicalization is invalid
- token is expired
- nonce mismatch is detected
- nonce reuse is detected
- source_capsule_root mismatches expected authority root
- schema is not recognized

---

## 5. Revocation Semantics

CHORA does not rely on interrupting running code mid-step.

Execution is intentionally segmented.

Revocation becomes effective at the next execution boundary.

---

## 6. Canonical Runtime Law

Make unverified continuation unreachable.
