# CHORA x VEX - Execution Binding Surface

This directory defines the canonical execution-binding layer for governed AI execution.

It specifies how authorization, enforcement, and execution are structurally connected.

---

## Core invariant

No valid authorization artifact -> No execution

---

## Components

### 1. Execution Binding Contract

- CHORA_VEX_EXECUTION_BINDING_CONTRACT_v1.md

Defines the formal contract governing execution authorization.

---

### 2. Contract <-> Diagram Mapping

- CONTRACT_V1_DIAGRAM_MAPPING.md

Provides a strict 1:1 mapping between the contract and the architecture diagram.

No interpretation layer exists between specification and execution.

---

### 3. Handshake Specification

- CHORA_VEX_HANDSHAKE_SPEC_v1.md

Defines the CHORA <-> VEX handshake:

- Intent submission (VEX -> CHORA)
- Authorization decision (CHORA -> token)
- Enforcement boundary (AEM via verify_continuation_token)

This is the exact boundary where continuation authority becomes enforceable.

---

## Enforcement boundary

Enforcement is implemented at:

`verify_continuation_token`

This is the single non-bypassable execution gate.

---

## Execution chain

authorization -> enforcement -> execution -> attestation -> commitment -> anchoring

---

## Status

- Execution Binding Contract v1 - locked
- Token Contract v3 - locked
- Handshake Specification v1 - locked
- Enforcement boundary - active

---

## Outcome

This directory defines a complete, non-bypassable execution binding surface.

Execution is:

- externally authorized
- cryptographically bound
- enforced at runtime
