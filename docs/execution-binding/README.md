# CHORA x VEX - Execution Binding (v0.1)

Status: Draft (Alignment Review)  
Date: 2026-03-20  

---

## Overview

This package introduces the next step in CHORA x VEX alignment:

-> Making execution cryptographically contingent on CHORA authorization

---

## What is already locked

- CHORA v220 architecture
- Evidence Capsule v0.3 (Merkle + Ed25519)
- Token Contract v3 (JCS + Ed25519)
- Cross-language verification (Python + Node)
- Capsule reproducibility (byte-for-byte)

---

## What this package introduces

1. Execution Binding Contract v0.1  
2. AEM Runtime Enforcement Spec v0.1  
3. Full Run Simulation (ALLOW + DENY paths)  
4. Review Notes for alignment  

---

## Core invariant

No valid signed continuation artifact  
-> No execution allowed  

---

## Conceptual shift

Before:
- CHORA decides (ALLOW / HALT / ESCALATE)

Now:
- ALLOW is not sufficient
- Execution requires verified token binding at runtime

---

## Structure

- CHORA_VEX_EXECUTION_BINDING_CONTRACT_v0.1.md
- CHORA_AEM_RUNTIME_SPEC_v0.1.md
- CHORA_VEX_FULL_RUN_SIMULATION_v0.1.md
- CHORA_VEX_REVIEW_NOTES_v0.1.md

---

## Alignment goal

Define the minimal, non-bypassable layer between:

CHORA authorization -> VEX execution

---

## Status

Proposed for alignment review with VEX
