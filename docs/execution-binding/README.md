# CHORA x VEX - Execution Binding (v0.2)

Status: Draft (Alignment Review)
Date: 2026-03-20

---

## Overview

This package introduces the next step in CHORA x VEX alignment:

-> identity-bound, proof-bound execution enforcement

---

## What is already locked

- CHORA v220 architecture
- Evidence Capsule v0.3 (Merkle + Ed25519)
- Token Contract v3 (JCS + Ed25519)
- Cross-language verification (Python + Node)
- Capsule reproducibility (byte-for-byte)

---

## What this package now introduces

1. Execution Binding Contract v0.2
2. AEM Runtime Enforcement Spec v0.2
3. Full Run Simulation v0.2
4. Review Notes v0.2

---

## Core invariant

No valid signed continuation artifact for the specific attested agent instance
-> No execution allowed

---

## Binding surface now includes

- direct identity binding (`aid`)
- `intent_hash`
- `circuit_id`
- capability-grant semantics
- PCR binding for High Assurance

---

## Conceptual shift

Before:
- CHORA decides (ALLOW / HALT / ESCALATE)

Now:
- ALLOW is not sufficient
- Execution requires a verified token bound to:
  - the attested agent instance
  - the computational promise
  - the proof surface
  - the granted capability scope

---

## Structure

- CHORA_VEX_EXECUTION_BINDING_CONTRACT_v0.2.md
- CHORA_AEM_RUNTIME_SPEC_v0.2.md
- CHORA_VEX_FULL_RUN_SIMULATION_v0.2.md
- CHORA_VEX_REVIEW_NOTES_v0.2.md

---

## Alignment goal

Define the minimal, non-bypassable layer between:

CHORA authorization -> local AEM verification -> capability grant -> VEX execution

---

## Status

Refined for alignment review with VEX
