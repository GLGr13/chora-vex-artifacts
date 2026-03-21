# Contract v1 <-> Architecture Diagram Mapping

This document defines the explicit 1:1 mapping between the Execution Binding Contract v1
and the CHORA x VEX architecture diagram.

## Core Invariant

No valid signed continuation artifact -> No execution allowed

---

## Mapping

| Contract Layer        | Diagram Component                          | Enforcement Meaning |
|----------------------|--------------------------------------------|--------------------|
| Authorization        | CHORA Gate                                 | External continuation authority (ALLOW / HALT / ESCALATE) |
| Enforcement          | Authorization Enforcement Module (AEM)     | Non-bypassable execution boundary (token required) |
| Execution            | Execution                                  | Execution only proceeds if authorized |
| Attestation          | VEX Ledger                                 | Governed execution event recorded |
| Commitment           | Merkle Commitment                          | Deterministic capsule root |
| Custody / Witness    | Public Blockchain Anchor                   | External verifiable anchoring |

---

## Execution Chain

authorization -> enforcement -> execution -> attestation -> commitment -> anchoring

---

## Design Guarantee

The system enforces strict separation:

- CHORA defines authority
- AEM enforces execution
- VEX records governed execution
- Merkle ensures deterministic integrity
- Anchor provides external custody

No layer can be bypassed without breaking the chain.

---

## Outcome

The contract and diagram are structurally equivalent representations of the same system.

No reinterpretation layer exists between specification and execution.
